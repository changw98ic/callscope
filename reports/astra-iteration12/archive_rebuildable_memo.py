"""Reversibly reclaim only the root-reviewed standalone frontend memo paths.

This tool opens raw memo bytes for hashing/compression, never a database
connection, target module, CocoIndex environment, test or build process.
"""
from __future__ import annotations

import datetime
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import tarfile
import traceback

HERE = Path(__file__).resolve().parent
REPORTS = HERE.parent
PLAN = HERE / "CACHE_RECLAIM_PLAN.json"
ARCHIVE = HERE / "rebuildable-memo-archive.tar.gz"
PARTIAL = HERE / ("rebuildable-memo-archive.tar.gz.partial-" + str(os.getpid()))
MANIFEST = HERE / "CACHE_RECLAIM_ARCHIVE_MANIFEST.json"
RESULT = HERE / "CACHE_RECLAIM_RESULT.json"
CHUNK = 1024 * 1024
PROCESS_CHECKS = []
_INFRASTRUCTURE = {"tail", "cloud-agent-log", "caas-prefix-tra", "dockerd", "containerd",
    "codex", "codex-linux-san", "bwrap", "bash", "sh", "ps", "cat"}


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def free_bytes():
    value = os.statvfs(REPORTS)
    return value.f_bavail * value.f_frsize


def hash_file(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def save(path, value):
    with path.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())


def fingerprint(info):
    return {"device": info.st_dev, "inode": info.st_ino, "logical_bytes": info.st_size,
        "allocated_bytes": info.st_blocks * 512, "link_count": info.st_nlink,
        "mtime_ns": info.st_mtime_ns, "ctime_ns": info.st_ctime_ns}


def inspect(item):
    root = Path(item["path"])
    if (not root.is_relative_to(REPORTS) or not root.name.endswith(".sqlite3.cocoindex")
            or root.resolve(strict=True) != root or root.is_symlink()):
        raise ValueError("cache path/namespace or symlink differs from reviewed plan")
    parent = root
    while parent != REPORTS:
        if stat.S_ISLNK(parent.lstat().st_mode):
            raise ValueError("symlink in candidate ancestry")
        parent = parent.parent
    files = {}
    for directory, names, filenames in os.walk(root, followlinks=False):
        parent = Path(directory)
        for name in names:
            if (parent / name).is_symlink():
                raise ValueError("symlink directory in cache")
        for name in filenames:
            path = parent / name
            info = path.lstat()
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                raise ValueError("non-regular, symlink or hardlinked cache file")
            files[str(path.relative_to(root))] = (path, info)
    expected = {record["relative_path"]: record for record in item["files"]}
    if set(files) != set(expected) or set(files) != {"mdb/data.mdb", "mdb/lock.mdb"}:
        raise ValueError("cache file set differs from plan/observed LMDB layout")
    for name, (_, info) in files.items():
        actual = fingerprint(info)
        if any(actual[key] != expected[name][key] for key in (
                "device", "inode", "logical_bytes", "allocated_bytes", "link_count")):
            raise ValueError("cache file identity/size/link count differs from reviewed plan: " + name)
    return files


def active_references(roots, file_records):
    references = {str(root): [] for root in roots}
    inspection_errors = []
    for process in Path("/proc").iterdir():
        if not process.name.isdigit():
            continue
        try:
            comm = (process / "comm").read_text().strip()
            owner_uid = process.stat().st_uid
        except OSError:
            continue
        argv, argv_readable = [], False
        try:
            argv = [part.decode("utf-8", "replace") for part in (process / "cmdline").read_bytes().split(b"\0") if part]
            argv_readable = True
        except OSError:
            pass
        worker = any(part.endswith("callscope/cocoindex_worker.py") or part == "cocoindex_worker.py" for part in argv)
        worker = worker or any(part == "-m" and index + 1 < len(argv)
            and argv[index + 1] == "callscope.cocoindex_worker" for index, part in enumerate(argv))
        trusted_helpers = [part for part in argv if part.startswith(str(REPORTS) + "/") and part.endswith(".py")]
        trusted_helpers.extend(str(REPORTS.parent / part) for part in argv if part.startswith("reports/")
            and part.endswith(".py") and (REPORTS.parent / part).is_file()
            and (REPORTS.parent / part).resolve().is_relative_to(REPORTS))
        classification = ("active_fixed_cocoindex_worker" if worker else "this_archive_tool" if int(process.name) == os.getpid()
            else "known_infrastructure_process" if comm in _INFRASTRUCTURE
            else "trusted_report_or_static_source_helper_not_fixed_cocoindex_worker" if trusted_helpers
            else "unclassified_process")
        metadata = {"pid": int(process.name), "owner_uid": owner_uid, "process_name": comm,
            "cmdline_readable": argv_readable, "fixed_cocoindex_worker": worker,
            "trusted_helper_paths": trusted_helpers, "classification": classification, "unreadable_metadata": []}
        if worker:
            for root in roots:
                references[str(root)].append({"kind": "active_fixed_cocoindex_worker", "pid": int(process.name)})
        for label, directory in (("fd", process / "fd"), ("mapped_file", process / "map_files")):
            try:
                entries = list(directory.iterdir())
            except (FileNotFoundError, ProcessLookupError):
                continue
            except OSError as error:
                metadata["unreadable_metadata"].append({"kind": label, "error": type(error).__name__})
                continue
            for entry in entries:
                try:
                    target = os.readlink(entry).removesuffix(" (deleted)")
                except PermissionError as error:
                    metadata["unreadable_metadata"].append({"kind": label + "_link", "error": type(error).__name__})
                    continue
                except OSError:
                    continue
                for root in roots:
                    if target == str(root) or target.startswith(str(root) + "/"):
                        references[str(root)].append({"pid": int(process.name), "process_name": comm,
                            "kind": label, "path": target})
        try:
            target = os.readlink(process / "cwd")
        except PermissionError as error:
            metadata["unreadable_metadata"].append({"kind": "cwd", "error": type(error).__name__})
            target = ""
        except OSError:
            target = ""
        for root in roots:
            if target == str(root) or target.startswith(str(root) + "/"):
                references[str(root)].append({"pid": int(process.name), "process_name": comm,
                    "kind": "cwd", "path": target})
        if metadata["unreadable_metadata"] and classification == "unclassified_process":
            inspection_errors.append({"pid": int(process.name), "kind": "unclassified_process_metadata_unreadable",
                "process_name": comm})
        PROCESS_CHECKS.append(metadata)
    inodes = {}
    for root, files in file_records.items():
        for path, info in files.values():
            inodes[(info.st_dev, info.st_ino)] = (root, path)
    for line in Path("/proc/locks").read_text().splitlines():
        for field in line.split():
            pieces = field.split(":")
            if len(pieces) != 3:
                continue
            try:
                key = (os.makedev(int(pieces[0], 16), int(pieces[1], 16)), int(pieces[2]))
            except ValueError:
                continue
            if key in inodes:
                root, path = inodes[key]
                references[str(root)].append({"kind": "kernel_lock", "path": str(path), "record": line})
    return references, inspection_errors


class HashingReader:
    def __init__(self, stream):
        self.stream = stream
        self.digest = hashlib.sha256()
        self.size = 0

    def read(self, size=-1):
        block = self.stream.read(size)
        self.digest.update(block)
        self.size += len(block)
        return block


def open_regular(path, expected):
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    stream = os.fdopen(descriptor, "rb")
    if fingerprint(os.fstat(stream.fileno())) != expected:
        stream.close()
        raise ValueError("file changed before regular-byte read")
    return stream


def verify_archive(path, members):
    expected = {entry["archive_member"]: entry for entry in members}
    found = set()
    with path.open("rb") as raw, gzip.GzipFile(fileobj=raw, mode="rb") as compressed:
        with tarfile.open(fileobj=compressed, mode="r|") as archive:
            for entry in archive:
                if not entry.isfile() or entry.name not in expected or entry.name in found:
                    raise ValueError("unexpected or duplicate archive member")
                record = expected[entry.name]
                if entry.size != record["logical_bytes"]:
                    raise ValueError("archive member size mismatch")
                stream = archive.extractfile(entry)
                if stream is None:
                    raise ValueError("archive regular member unreadable")
                with stream:
                    actual = hashlib.file_digest(stream, "sha256").hexdigest()
                if actual != record["sha256"]:
                    raise ValueError("archive readback member hash mismatch")
                found.add(entry.name)
        # Consume padding/footer too, so gzip CRC and terminal stream errors are checked.
        while compressed.read(CHUNK):
            pass
    if found != set(expected):
        raise ValueError("archive readback member set mismatch")
    return {"member_count": len(found), "all_member_hashes_match": True,
        "gzip_stream_consumed_and_crc_checked": True, "archive_sha256": hash_file(path)}


def main():
    plan = json.loads(PLAN.read_text())
    plan_hash = hash_file(PLAN)
    result = {"kind": "reversible_rebuildable_memo_reclaim", "started_at_utc": now(),
        "reviewed_plan_sha256": plan_hash, "status": "checking", "archive": str(ARCHIVE),
        "free_bytes_before": free_bytes(), "removed": [], "skipped": [], "errors": [],
        "bytecode_caches_preserved": [item["path"] for item in plan["items"] if item["kind"] != "cocoindex_frontend_memo"],
        "target_executed": False, "target_tests_run": False, "target_build_run": False,
        "cocoindex_environment_opened": False, "formal_database_opened": False,
        "common_query_lock_acquired": False, "uncompressed_tar_created": False,
        "activity_check_scope": "Fixed trusted CocoIndex runner lifecycle, visible FD/maps/cwd and LMDB kernel locks; inaccessible known infrastructure mappings are recorded, not treated as hidden CocoIndex workers.",
        "root_technical_direction": "Known infrastructure proc metadata permissions do not block reversible derived memo reclaim when no active fixed Python CocoIndex worker exists; retain unreadable metadata details."}
    preserved = {}
    try:
        if ARCHIVE.exists() or MANIFEST.exists() or RESULT.exists():
            raise ValueError("refuse to replace an existing reclaim archive/result")
        for entry in plan["preserve_analysis_database_files"]:
            path = Path(entry["path"])
            preserved[str(path)] = fingerprint(path.lstat())
        candidates = [item for item in plan["items"] if item["kind"] == "cocoindex_frontend_memo"]
        if len(candidates) != 23:
            raise ValueError("reviewed plan does not contain exactly 23 memo directories")
        inspected, selected = {}, []
        for item in candidates:
            try:
                files = inspect(item)
                inspected[str(item["path"])] = files
                selected.append(item)
            except (OSError, ValueError) as error:
                result["skipped"].append({"path": item["path"], "stage": "pre_archive_identity", "reason": str(error)})
        refs, errors = active_references([Path(item["path"]) for item in selected], inspected)
        result["pre_archive_process_inspection_errors"] = errors
        ready = []
        for item in selected:
            if refs[item["path"]] or errors:
                result["skipped"].append({"path": item["path"], "stage": "pre_archive_active_references",
                    "references": refs[item["path"]], "inspection_errors": errors})
            else:
                ready.append(item)
        if not ready:
            result["status"] = "no_eligible_memo_directories"
            return
        members = []
        print(json.dumps({"stage": "archive_start", "directories": len(ready), "free_bytes": free_bytes()}), flush=True)
        with PARTIAL.open("xb") as raw:
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=1, mtime=0) as compressed:
                with tarfile.open(fileobj=compressed, mode="w|", format=tarfile.PAX_FORMAT) as archive:
                    for item in ready:
                        root = Path(item["path"])
                        for name, (path, info) in sorted(inspected[str(root)].items()):
                            before = fingerprint(info)
                            member_name = str(path.relative_to(REPORTS))
                            archive_info = tarfile.TarInfo(member_name)
                            archive_info.size = info.st_size
                            archive_info.mode = stat.S_IMODE(info.st_mode)
                            archive_info.mtime = info.st_mtime
                            archive_info.uid, archive_info.gid = info.st_uid, info.st_gid
                            with open_regular(path, before) as source:
                                reader = HashingReader(source)
                                archive.addfile(archive_info, reader)
                                after = fingerprint(os.fstat(source.fileno()))
                            if before != after or fingerprint(path.lstat()) != before or reader.size != info.st_size:
                                raise ValueError("source memo changed during streaming archive")
                            members.append({"original_path": str(path), "cache_directory": str(root),
                                "archive_member": member_name, "logical_bytes": info.st_size,
                                "allocated_bytes": info.st_blocks * 512, "sha256": reader.digest.hexdigest(),
                                "source_identity": before})
                        print(json.dumps({"stage": "archived_directory", "path": str(root), "member_count": len(members)}), flush=True)
            raw.flush()
            os.fsync(raw.fileno())
        print(json.dumps({"stage": "archive_readback_start", "compressed_bytes": PARTIAL.stat().st_size}), flush=True)
        verified = verify_archive(PARTIAL, members)
        PARTIAL.rename(ARCHIVE)
        manifest = {"kind": "rebuildable_memo_stream_archive_manifest", "created_at_utc": now(),
            "reviewed_plan_sha256": plan_hash, "archive": str(ARCHIVE), "archive_sha256": verified["archive_sha256"],
            "archive_bytes": ARCHIVE.stat().st_size, "compression": "gzip level 1; no uncompressed tar",
            "restore_base_directory": str(REPORTS), "members": members,
            "readback_verification": verified, "formal_database_or_report_files_archived_or_removed": False}
        save(MANIFEST, manifest)
        result.update({"status": "archive_verified_before_reclaim", "archive_sha256": verified["archive_sha256"],
            "archive_bytes": ARCHIVE.stat().st_size, "manifest": str(MANIFEST), "manifest_sha256": hash_file(MANIFEST),
            "archive_readback_verification": verified, "archived_directory_count": len(ready)})
        save(RESULT, result)
        # Each directory is revalidated independently immediately before removal.
        for item in ready:
            root = Path(item["path"])
            try:
                current = inspect(item)
                for path, info in current.values():
                    record = next(member for member in members if member["original_path"] == str(path))
                    if fingerprint(info) != record["source_identity"]:
                        raise ValueError("memo identity/metadata changed since archived copy")
                    with open_regular(path, record["source_identity"]) as source:
                        actual = hashlib.file_digest(source, "sha256").hexdigest()
                        after = fingerprint(os.fstat(source.fileno()))
                    if actual != record["sha256"] or after != record["source_identity"]:
                        raise ValueError("memo bytes changed since verified archived copy")
                refs, errors = active_references([root], {str(root): current})
                if refs[str(root)] or errors:
                    result["skipped"].append({"path": str(root), "stage": "pre_delete_activity",
                        "references": refs[str(root)], "inspection_errors": errors})
                    continue
                # rmtree's fd-based implementation avoids following a replaced symlink.
                if not shutil.rmtree.avoids_symlink_attacks:
                    raise ValueError("platform lacks fd-based safe directory removal")
                shutil.rmtree(root)
                result["removed"].append({"path": str(root), "file_count": len(current),
                    "planned_allocated_bytes": item["actual_allocated_bytes"],
                    "matching_archive_member_count": sum(member["cache_directory"] == str(root) for member in members),
                    "identity_bytes_activity_rechecked": True})
                save(RESULT, result)
                print(json.dumps({"stage": "reclaimed_directory", "path": str(root), "free_bytes": free_bytes()}), flush=True)
            except (OSError, ValueError) as error:
                result["skipped"].append({"path": str(root), "stage": "pre_delete_or_remove", "reason": str(error)})
        checks = [{"path": path, "identity_metadata_unchanged": fingerprint(Path(path).lstat()) == expected}
            for path, expected in preserved.items()]
        result["preserved_formal_database_metadata_checks"] = checks
        if not all(entry["identity_metadata_unchanged"] for entry in checks):
            raise ValueError("a protected formal database identity changed during operation")
        result["status"] = "reclaimed_all_reviewed_memo" if len(result["removed"]) == 23 else "partially_reclaimed_verified_archive_preserved"
    except Exception as error:
        result["status"] = "error_originals_retained_except_previously_recorded_verified_removals"
        result["errors"].append({"type": type(error).__name__, "message": str(error), "traceback": traceback.format_exc()})
        if PARTIAL.exists():
            result["incomplete_archive_path"] = str(PARTIAL)
            result["incomplete_archive_bytes"] = PARTIAL.stat().st_size
    finally:
        result["completed_at_utc"] = now()
        result["free_bytes_after"] = free_bytes()
        result["free_byte_change"] = result["free_bytes_after"] - result["free_bytes_before"]
        result["reviewed_plan_bytes_unchanged"] = hash_file(PLAN) == plan_hash
        result["process_metadata_observations"] = PROCESS_CHECKS
        save(RESULT, result)
        print(json.dumps({key: result.get(key) for key in ("status", "archive_bytes", "archive_sha256", "free_bytes_after", "free_byte_change")}
            | {"removed_directories": len(result["removed"]), "skipped": len(result["skipped"]), "errors": len(result["errors"])}), flush=True)


if __name__ == "__main__":
    main()
