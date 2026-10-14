"""Capture explicitly declared support documents as inert UTF-8 text.

This staging helper reads no directory inventory and performs no TOML, schema,
code, package-manager, or Git evaluation. It uses the trusted source reader's
descriptor walk for the declared paths only. ``hash`` identifies original bytes;
``text_hash`` identifies decoded UTF-8 text after removing an optional BOM.
"""

from hashlib import sha256
import os
from pathlib import Path, PurePosixPath, PureWindowsPath

from .models import Diagnostic


INPUT_CAPTURE_VERSION = "support-input-capture-1"
MAX_SUPPORT_INPUT_BYTES = 16 * 1024 * 1024


def _validate_paths(paths: list[str]) -> list[str]:
    if not isinstance(paths, list):
        raise ValueError("support input paths must be an explicit list of relative strings")
    seen = set()
    for index, relative in enumerate(paths):
        if (not isinstance(relative, str) or not relative.strip()
                or "\\" in relative or "\x00" in relative
                or any(ord(character) < 32 or ord(character) == 127 for character in relative)):
            raise ValueError(f"support input paths[{index}] must be a non-empty canonical relative path")
        posix = PurePosixPath(relative)
        if (posix.is_absolute() or PureWindowsPath(relative).drive
                or any(component in {"", ".", ".."} for component in relative.split("/"))
                or str(posix) != relative):
            raise ValueError(f"support input path must remain inside the project root: {relative!r}")
        if relative in seen:
            raise ValueError(f"duplicate support input path: {relative!r}")
        seen.add(relative)
    return sorted(seen)


def _failure(relative: str, message: str, *, digest: str = "", size: int | None = None,
             status: str = "read_error") -> dict:
    return {"path": relative, "hash": digest, "content": "", "status": status,
            "error": message, "kind": "support_input", "text_hash": None, "size_bytes": size}


def capture_support_inputs(root: Path, paths: list[str], max_bytes: int) -> tuple[dict[str, dict], list[Diagnostic]]:
    """Capture each declared path once; do not discover or expand other paths.

    Invalid configuration raises ValueError before any repository I/O. Missing,
    unsafe, changing, unreadable, oversized, or undecodable inputs remain explicit
    records with diagnostics. A read_error must not be treated as a cache hit.
    An empty successfully read file has status captured and the empty-text SHA;
    failed records have no text_hash, so empty content never implies success.
    """
    if not isinstance(root, Path):
        raise ValueError("root must be the explicit project Path")
    if type(max_bytes) is not int or not 1 <= max_bytes <= MAX_SUPPORT_INPUT_BYTES:
        raise ValueError("max_bytes must be an integer between 1 and 16777216")
    from .analyzer import _secure_bytes
    declared = _validate_paths(paths)
    records, diagnostics = {}, []
    nofollow_available = (
        bool(getattr(os, "O_NOFOLLOW", 0))
        and bool(getattr(os, "O_DIRECTORY", 0))
        and os.open in getattr(os, "supports_dir_fd", set())
    )
    for relative in declared:
        if not nofollow_available:
            message = "Safe no-follow descriptor-relative reads are unavailable on this platform"
            records[relative] = _failure(relative, message)
            diagnostics.append(Diagnostic("warning", "support_input_no_follow_unavailable", message, relative))
            continue
        try:
            # _secure_bytes opens root and every path component with O_NOFOLLOW,
            # requires a regular file, hashes the actual stream even on oversize,
            # and rejects a file whose metadata changes during that read.
            data, digest, size = _secure_bytes(root, relative, max_bytes)
        except (OSError, NotImplementedError) as error:
            message = str(error) or type(error).__name__
            records[relative] = _failure(relative, message)
            diagnostics.append(Diagnostic("warning", "support_input_read_error", message, relative))
            continue
        if data is None:
            message = f"Support input is {size} bytes and exceeds the {max_bytes}-byte capture limit"
            records[relative] = _failure(relative, message, digest=digest, size=size, status="too_large")
            diagnostics.append(Diagnostic("warning", "support_input_too_large", message, relative))
            continue
        try:
            content = data.decode("utf-8-sig")
        except UnicodeError as error:
            message = str(error)
            records[relative] = _failure(relative, message, digest=digest, size=size)
            diagnostics.append(Diagnostic("warning", "support_input_encoding_error", message, relative))
            continue
        records[relative] = {
            "path": relative, "hash": digest, "content": content, "status": "captured",
            "error": None, "kind": "support_input", "text_hash": sha256(content.encode("utf-8")).hexdigest(),
            "size_bytes": size,
        }
    return records, diagnostics
