"""Isolated CocoIndex adapter. Target text travels only as JSON data."""

from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import sysconfig
from importlib import metadata

from .models import Diagnostic, Edge, Node, SourceFile

COCOINDEX_VERSION = "1.0.25"
PROTOCOL_VERSION = 1


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":"), allow_nan=False)


def request_fingerprint(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def trusted_interpreter():
    bundled = Path(__file__).resolve().parent.parent / ".analysis-tools" / "runtime" / "bin" / "python"
    if bundled.is_file():
        return str(bundled)
    paths = list({sysconfig.get_path("purelib"), sysconfig.get_path("platlib")})
    for distribution in metadata.distributions(path=paths):
        if distribution.metadata.get("Name", "").casefold() == "cocoindex" and distribution.version == COCOINDEX_VERSION:
            return sys.executable
    return None


class CocoIndexRunner:
    def __init__(self, cache_path: str | Path):
        interpreter = trusted_interpreter()
        if not interpreter:
            raise RuntimeError("缺少固定 CocoIndex 1.0.25 工具依赖；安装 callscope[maintenance] 或显式选择 --engine full")
        self.interpreter = interpreter
        self.cache_path = Path(cache_path).absolute()
        self.last_run = None

    def run(self, root, policy, captured, implementation):
        payload = {"protocol": PROTOCOL_VERSION, "root": str(root), "policy": policy,
                   "files": [asdict(source) for source in captured], "tool_identity": implementation}
        fingerprint = request_fingerprint(payload)
        request = {"payload": payload, "request_fingerprint": fingerprint,
                   "cache_path": str(self.cache_path)}
        package = Path(__file__).resolve().parent
        # Isolated mode ignores PYTHONPATH, cwd modules and user site packages.
        # The script bootstraps only this explicit, trusted CallScope package.
        completed = subprocess.run(
            [self.interpreter, "-I", str(package / "cocoindex_worker.py")],
            input=canonical(request), text=True, encoding="utf-8", capture_output=True,
            cwd=package, timeout=3600, check=False,
        )
        if completed.returncode:
            raise RuntimeError("CocoIndex 更新失败，旧快照保留：" + completed.stderr[-4000:].strip())
        try:
            response = json.loads(completed.stdout)
        except (ValueError, TypeError) as exc:
            raise RuntimeError("CocoIndex worker 返回无效 JSON；未发布快照") from exc
        if response.get("request_fingerprint") != fingerprint or response.get("tool_identity") != implementation:
            raise RuntimeError("CocoIndex 返回的分析输入身份不匹配；未发布快照")
        maintenance = response.get("maintenance", {})
        if maintenance != {"backend": "cocoindex", "version": COCOINDEX_VERSION, "protocol": PROTOCOL_VERSION,
                           "granularity": "language", "global_detection": "full"}:
            raise RuntimeError("CocoIndex worker 引擎版本或协议不匹配")
        languages = policy["analysis"]["languages"]
        if set(response["versions"]) != set(languages) or set(response["results"]) != set(languages):
            raise RuntimeError("CocoIndex worker 未返回所有请求的语言结果")
        results = {}
        for language in languages:
            raw = response["results"][language]
            result = {name: [model(**value) for value in raw[name]] for name, model in (
                ("nodes", Node), ("edges", Edge), ("files", SourceFile), ("diagnostics", Diagnostic))}
            result["stats"] = raw["stats"]
            expected_files = {source.path: source for source in captured if source.language == language}
            returned_files = {source.path: source for source in result["files"]}
            if len(returned_files) != len(result["files"]) or set(returned_files) != set(expected_files):
                raise RuntimeError("缓存结果的文件集合与捕获输入不一致")
            if any(source.hash != expected_files[path].hash or source.content != expected_files[path].content
                   or source.language != expected_files[path].language for path, source in returned_files.items()):
                raise RuntimeError("缓存结果的源码证据与捕获输入不一致")
            results[language] = result
        self.last_run = response["runtime"]
        return {"results": results, "versions": response["versions"], "maintenance": maintenance}
