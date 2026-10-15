"""Run a fixed trusted static pipeline in a Python -I subprocess.

This is an analysis-tool process, not a target-code executor. It imports no
target packages, runs no target command and reads only captured source JSON.
"""

from dataclasses import asdict
import importlib.util
import json
from pathlib import Path
import sys


def _bootstrap():
    package = Path(__file__).resolve().parent
    spec = importlib.util.spec_from_file_location("callscope", package / "__init__.py",
                                                submodule_search_locations=[str(package)])
    module = importlib.util.module_from_spec(spec)
    sys.modules["callscope"] = module
    spec.loader.exec_module(module)


def main():
    _bootstrap()
    import cocoindex as coco
    from callscope.analysis import execute_frontend, frontend_versions
    from callscope.analysis_inputs import tool_identity
    from callscope.cocoindex_runner import COCOINDEX_VERSION, PROTOCOL_VERSION, canonical, request_fingerprint
    from callscope.models import SourceFile, project_id_for
    from callscope.parsers import language_parser
    from callscope.language_catalog import CODEGRAPH_LANGUAGES

    if coco.__version__ != COCOINDEX_VERSION:
        raise RuntimeError(f"需要 CocoIndex {COCOINDEX_VERSION}，实际为 {coco.__version__}")
    request = json.load(sys.stdin)
    payload = request["payload"]
    if payload["protocol"] != PROTOCOL_VERSION or request_fingerprint(payload) != request["request_fingerprint"]:
        raise ValueError("worker 请求协议/指纹不匹配")
    implementation = tool_identity()
    if payload["tool_identity"] != implementation:
        raise RuntimeError("worker 与调用端的工具代码不同；请重新扫描")
    languages = payload["policy"]["analysis"]["languages"]
    versions = {language: frontend_versions(language) for language in languages}
    # Dependency initialization happens before memo lookup. Missing or broken
    # parsers fail the update rather than becoming permanently cached results.
    for language in languages:
        if any(source["language"] == language and source["status"] == "captured" for source in payload["files"]):
            if language == "typescript":
                language_parser("typescript")
                language_parser("tsx")
            elif language == "rust":
                language_parser("rust")
            elif language in CODEGRAPH_LANGUAGES:
                from callscope.codegraph_frontend import ensure_runtime
                ensure_runtime()
    computed = []
    uncached = []

    def compute(language: str, root: str, files_json: str, policy_json: str) -> str:
        files = [SourceFile(**value) for value in json.loads(files_json)]
        result = execute_frontend(language, files, Path(root), json.loads(policy_json))
        # Runtime/initialization failures are not memoizable static evidence.
        transient_codes = {"ts_parser_failure", "rust_parser_unavailable", "rust_parser_failure", "language_frontend_failed",
                           "codegraph_runtime_unavailable", "codegraph_frontend_failed", "codegraph_parser_failure"}
        if any(item.code in transient_codes for item in result["diagnostics"]):
            raise RuntimeError("语言前端运行失败，未缓存该结果；请查看解析依赖或重新扫描")
        computed.append(language)
        return canonical({**result, **{name: [asdict(value) for value in result[name]]
                         for name in ("nodes", "edges", "files", "diagnostics")}})

    @coco.fn(memo=True, version=1, logic_tracking="self")
    def analyze_language(language: str, root: str, files_json: str, policy_json: str, identity_json: str) -> str:
        # identity_json participates in CocoIndex's actual persistent memo key;
        # explicit arguments include all trusted implementation/parser versions.
        return compute(language, root, files_json, policy_json)

    @coco.fn(version=1, logic_tracking="self")
    def maintain(payload_json: str) -> str:
        current = json.loads(payload_json)
        result = {}
        policy_json = canonical(current["policy"])
        identity_json = canonical({"tool": implementation, "versions": versions,
                                   "engine": coco.__version__, "protocol": PROTOCOL_VERSION})
        for language in current["policy"]["analysis"]["languages"]:
            sources = [source for source in current["files"] if source["language"] == language]
            files_json = canonical(sources)
            # A read failure is retryable. Do not memoize that entire bundle.
            support_records = current["policy"]["analysis"].get("_captured_support_inputs", {})
            if (any(source["status"] == "read_error" for source in sources)
                    or any(record.get("status") != "captured" for record in support_records.values())):
                uncached.append(language)
                encoded = compute(language, current["root"], files_json, policy_json)
            else:
                encoded = analyze_language(language, current["root"], files_json, policy_json, identity_json)
            result[language] = json.loads(encoded)
        return canonical(result)

    environment = coco.Environment(coco.Settings(db_path=Path(request["cache_path"])), name="callscope-static")
    try:
        app = coco.App(coco.AppConfig(name="callscope-" + project_id_for(payload["root"]),
                                     environment=environment, max_inflight_components=1), maintain, canonical(payload))
        results = json.loads(app.update_blocking(report_to_stdout=False))
    finally:
        environment.close()
    if tool_identity() != implementation:
        raise RuntimeError("worker 分析期间工具发生变化；未发布快照")
    response = {"request_fingerprint": request["request_fingerprint"], "tool_identity": implementation,
                "versions": versions, "results": results,
                "maintenance": {"backend": "cocoindex", "version": coco.__version__, "protocol": PROTOCOL_VERSION,
                                "granularity": "language", "global_detection": "full"},
                "runtime": {"engine": "cocoindex", "version": coco.__version__,
                            "recomputed_languages": sorted(set(computed)),
                            "reused_languages": sorted(set(languages) - set(computed)),
                            "uncached_languages": sorted(set(uncached)), "global_detection": "full"}}
    json.dump(response, sys.stdout, ensure_ascii=True, separators=(",", ":"), allow_nan=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
