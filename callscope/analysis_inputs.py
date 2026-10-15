"""Identity of trusted tool code and the actual static analysis runtime."""

import hashlib
from pathlib import Path

from ._vendor.axon import ADAPTER_VERSION, UPSTREAM_COMMIT


def tool_identity() -> dict:
    package = Path(__file__).resolve().parent
    digest = hashlib.sha256()
    for path in sorted(package.rglob("*.py")):
        digest.update(path.relative_to(package).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    vendor = package / '_vendor/codegraph'
    if vendor.is_dir():
        for path in sorted(vendor.rglob('*')):
            if path.is_file():
                digest.update(path.relative_to(package).as_posix().encode())
                digest.update(b'\0')
                digest.update(path.read_bytes())
                digest.update(b'\0')
    return {"source_hash": digest.hexdigest(), "graph_backend": ADAPTER_VERSION,
            "axon_commit": UPSTREAM_COMMIT,
            "codegraph_commit": "8f1f842b5b828175992d2ce2cdf673b955b2cce9" if vendor.is_dir() else None}
