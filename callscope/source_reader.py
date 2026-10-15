"""Capture configured source files as data using POSIX no-follow descriptors."""

from collections import Counter
from dataclasses import replace
import io
import os
from pathlib import Path
import stat
import subprocess
import tokenize

from .analyzer import _excluded, _open_directory, _secure_bytes, _source_roots
from .models import Diagnostic, SourceFile
from .language_catalog import EXTENSIONS, CODEGRAPH_LANGUAGES, language_for_path
_TOOL_STATE = {".beads", ".agents", ".analysis-tools", "target", "dist-tests", "coverage"}


def scan_sources(root: Path, config: dict):
    analysis = config["analysis"]
    languages = set(analysis["languages"])
    exclusions = analysis["exclude"]
    roots = _source_roots(root, analysis["source_roots"])
    candidates = {}
    inventory = set()
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
                    inventory.add(path)
        except OSError as exc:
            errors.append({"path": relative, "error": str(exc)})
            diagnostics.append(Diagnostic("warning", "directory_read_error", str(exc), relative))
        finally:
            if descriptor is not None:
                os.close(descriptor)
    files = []
    unsupported = []
    unrecognized = []

    def marker_exists(path):
        # Theme markers can sit beside a narrower selected source root. Inspect
        # metadata through the same no-follow parent boundary, never read a
        # marker via a symlink or execute its contents.
        descriptor = None
        try:
            relative = Path(path)
            descriptor = _open_directory(root, relative.parent.as_posix())
            info = os.stat(relative.name, dir_fd=descriptor, follow_symlinks=False)
            return stat.S_ISREG(info.st_mode)
        except OSError:
            return False
        finally:
            if descriptor is not None:
                os.close(descriptor)

    for path in sorted(inventory):
        language = language_for_path(path, known_paths=inventory, path_exists=marker_exists)
        if language:
            candidates[path] = language
        else:
            unrecognized.append({"path": path, "extension": Path(path).suffix.lower()})
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
    classification_changes = []
    classification_failed = False
    # Headers and .inc fragments can use a different language than their suffix.
    # The shipped upstream classifier sees captured data, never a target path.
    # An explicitly native-only policy does not acquire a Node dependency.
    classify = [source for source in files if source.language in CODEGRAPH_LANGUAGES
                and Path(source.path).suffix.lower() in {'.h', '.inc'}
                and source.status in {'captured', 'unsupported'}]
    if classify and languages & CODEGRAPH_LANGUAGES:
        try:
            from .codegraph_frontend import classify_files
            identified = classify_files(classify)
            if any(language not in CODEGRAPH_LANGUAGES for language in identified.values()):
                raise RuntimeError('Classifier returned an unregistered CodeGraph language')
            for index, source in enumerate(files):
                language = identified.get(source.path, source.language)
                if language != source.language:
                    status = 'captured' if language in languages else 'unsupported'
                    classification_changes.append({'path': source.path, 'extension_language': source.language,
                                                   'content_language': language})
                    files[index] = replace(source, language=language, status=status,
                                           error=None if status == 'captured' else '此源码语言不在当前分析能力或配置范围中')
            unsupported = [{'path': source.path, 'language': source.language}
                           for source in files if source.status == 'unsupported']
        except (OSError, RuntimeError, ValueError, KeyError, subprocess.SubprocessError) as error:
            classification_failed = True
            diagnostics.append(Diagnostic('warning', 'codegraph_classification_failed',
                                          'Content language classification unavailable; extension classification retained: ' + str(error)))
    if unsupported:
        counts = Counter(item["language"] for item in unsupported)
        diagnostics.append(Diagnostic("warning", "unsupported_sources", f"扫描范围包含未分析语言文件：{dict(sorted(counts.items()))}"))
    return files, diagnostics, {
        "source_roots": analysis["source_roots"], "excluded_paths": sorted(excluded),
        "symlinks_skipped": sorted(links), "scan_errors": errors, "unsupported_files": unsupported,
        "content_language_classification_changes": classification_changes,
        "content_language_classification_failed": classification_failed,
        "file_inventory": {"regular_files_seen": len(inventory), "recognized_source_files": len(candidates),
                           "unrecognized_files": unrecognized,
                           "meaning": "No-follow file-path inventory only; unrecognized files are not parsed source or functional coverage."},
    }
