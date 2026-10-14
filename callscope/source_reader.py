"""Capture configured source files as data using POSIX no-follow descriptors."""

from collections import Counter
import io
import os
from pathlib import Path
import tokenize

from .analyzer import _excluded, _open_directory, _secure_bytes, _source_roots
from .models import Diagnostic, SourceFile

EXTENSIONS = {
    ".py": "python", ".pyi": "python-stub",
    ".ts": "typescript", ".tsx": "typescript", ".js": "typescript", ".jsx": "typescript",
    ".mjs": "typescript", ".cjs": "typescript", ".mts": "typescript", ".cts": "typescript",
    ".rs": "rust", ".go": "go", ".java": "java", ".kt": "kotlin", ".swift": "swift",
    ".c": "c", ".h": "c", ".cc": "cpp", ".cpp": "cpp", ".cs": "csharp",
    ".rb": "ruby", ".php": "php", ".lua": "lua", ".sh": "shell",
}
_TOOL_STATE = {".beads", ".agents", ".analysis-tools", "target", "dist-tests", "coverage"}


def scan_sources(root: Path, config: dict):
    analysis = config["analysis"]
    languages = set(analysis["languages"])
    exclusions = analysis["exclude"]
    roots = _source_roots(root, analysis["source_roots"])
    candidates = {}
    excluded = set()
    links = set()
    errors = []
    diagnostics = []
    visited = set()
    pending = [path.relative_to(root).as_posix() for path in roots]
    while pending:
        relative = pending.pop()
        if relative in visited:
            continue
        visited.add(relative)
        if relative != "." and (_excluded(relative, exclusions, directory=True) or Path(relative).name in _TOOL_STATE):
            excluded.add(relative)
            continue
        descriptor = None
        try:
            descriptor = _open_directory(root, relative)
            with os.scandir(descriptor) as iterator:
                entries = sorted(iterator, key=lambda entry: entry.name)
            for entry in entries:
                path = entry.name if relative == "." else relative + "/" + entry.name
                if _excluded(path, exclusions, directory=entry.is_dir(follow_symlinks=False)):
                    excluded.add(path)
                    continue
                if entry.is_symlink():
                    links.add(path)
                    diagnostics.append(Diagnostic("warning", "symlink_skipped", "不跟随符号链接，相关覆盖未知", path))
                elif entry.is_dir(follow_symlinks=False):
                    if entry.name in _TOOL_STATE:
                        excluded.add(path)
                    else:
                        pending.append(path)
                elif entry.is_file(follow_symlinks=False):
                    language = EXTENSIONS.get(Path(path).suffix.lower())
                    if language:
                        candidates[path] = language
        except OSError as exc:
            errors.append({"path": relative, "error": str(exc)})
            diagnostics.append(Diagnostic("warning", "directory_read_error", str(exc), relative))
        finally:
            if descriptor is not None:
                os.close(descriptor)
    files = []
    unsupported = []
    for path, language in sorted(candidates.items()):
        try:
            data, digest, size = _secure_bytes(root, path, analysis["max_file_bytes"])
            if data is None:
                files.append(SourceFile(path, digest, "", "too_large", language, f"源码 {size} 字节超过读取上限"))
                diagnostics.append(Diagnostic("warning", "source_too_large", "源码超限，不能完整分析", path))
                continue
            try:
                encoding = tokenize.detect_encoding(io.BytesIO(data).readline)[0] if language == "python" else "utf-8-sig"
                content = data.decode(encoding)
            except (UnicodeError, LookupError, SyntaxError) as exc:
                files.append(SourceFile(path, digest, "", "read_error", language, str(exc)))
                diagnostics.append(Diagnostic("warning", "source_encoding_error", str(exc), path))
                continue
            status = "captured" if language in languages else "unsupported"
            reason = None if status == "captured" else "此源码语言不在当前分析能力或配置范围中"
            files.append(SourceFile(path, digest, content, status, language, reason))
            if status == "unsupported":
                unsupported.append({"path": path, "language": language})
        except OSError as exc:
            files.append(SourceFile(path, "", "", "read_error", language, str(exc)))
            diagnostics.append(Diagnostic("warning", "source_read_error", str(exc), path))
    if unsupported:
        counts = Counter(item["language"] for item in unsupported)
        diagnostics.append(Diagnostic("warning", "unsupported_sources", f"扫描范围包含未分析语言文件：{dict(sorted(counts.items()))}"))
    return files, diagnostics, {
        "source_roots": analysis["source_roots"], "excluded_paths": sorted(excluded),
        "symlinks_skipped": sorted(links), "scan_errors": errors, "unsupported_files": unsupported,
    }
