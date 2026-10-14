"""Verify or restore the standalone memo archive; never open a database."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import tarfile

HERE = Path(__file__).resolve().parent
REPORTS = HERE.parent
MANIFEST = HERE / "CACHE_RECLAIM_ARCHIVE_MANIFEST.json"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--restore", action="store_true", help="Restore only after all original cache roots are absent")
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text())
    archive_path = HERE / "rebuildable-memo-archive.tar.gz"
    with archive_path.open("rb") as stream:
        if hashlib.file_digest(stream, "sha256").hexdigest() != manifest["archive_sha256"]:
            raise ValueError("archive SHA256 differs from the recorded manifest")
    expected = {entry["archive_member"]: entry for entry in manifest["members"]}
    if len(expected) != len(manifest["members"]):
        raise ValueError("duplicate manifest member")
    roots = set()
    for name, record in expected.items():
        relative = PurePosixPath(name)
        original = Path(record["original_path"])
        root = Path(record["cache_directory"])
        if (relative.is_absolute() or ".." in relative.parts or str(REPORTS / name) != str(original)
                or not root.is_relative_to(REPORTS) or not root.name.endswith(".sqlite3.cocoindex")
                or original.relative_to(root).as_posix() not in {"mdb/data.mdb", "mdb/lock.mdb"}):
            raise ValueError("member is not an expected standalone memo path")
        if args.restore and (root.exists() or root.is_symlink()):
            raise ValueError("cache root already exists; refusing to merge or overwrite: " + str(root))
        if root.parent.resolve(strict=True) != root.parent:
            raise ValueError("cache parent contains a symlink")
        roots.add(root)
    staging = HERE / (".memo-restore-stage-" + str(os.getpid()))
    if args.restore:
        staging.mkdir(exist_ok=False)
    found = set()
    try:
        with tarfile.open(archive_path, mode="r|gz") as archive:
            for member in archive:
                if not member.isfile() or member.name not in expected or member.name in found:
                    raise ValueError("unexpected archive member")
                record = expected[member.name]
                if member.size != record["logical_bytes"]:
                    raise ValueError("archive member size mismatch")
                stream = archive.extractfile(member)
                if stream is None:
                    raise ValueError("cannot read archived memo bytes")
                output = staging / member.name
                if args.restore:
                    output.parent.mkdir(parents=True, exist_ok=True)
                digest = hashlib.sha256()
                with stream:
                    if args.restore:
                        with output.open("xb") as target:
                            while block := stream.read(1024 * 1024):
                                digest.update(block)
                                target.write(block)
                            target.flush()
                            os.fsync(target.fileno())
                        output.chmod(member.mode & 0o777)
                    else:
                        while block := stream.read(1024 * 1024):
                            digest.update(block)
                if digest.hexdigest() != record["sha256"]:
                    raise ValueError("restored member SHA256 mismatch")
                found.add(member.name)
        if found != set(expected):
            raise ValueError("archive member set mismatch")
        restored = []
        if args.restore:
            for root in sorted(roots):
                if root.exists() or root.is_symlink():
                    raise ValueError("cache appeared during restoration; no overwrite")
                (staging / root.relative_to(REPORTS)).rename(root)
                restored.append(str(root))
        print(json.dumps({"archive_sha256": manifest["archive_sha256"], "verified_members": len(found),
            "restored_cache_roots": restored, "formal_databases_or_reports_modified": False,
            "cocoindex_or_target_code_executed": False}, ensure_ascii=False))
    finally:
        if args.restore and staging.exists():
            shutil.rmtree(staging)


if __name__ == "__main__":
    main()
