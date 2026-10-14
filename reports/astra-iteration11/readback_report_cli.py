"""Prepare/run the normal trusted CLI export from closed v13 saved reports.

Run only after the coordinator announces that both formal stores are closed.
This helper uses only the standard library and takes the common source-query
flock internally. It never imports a target or invokes scan/detection/tests.
The CLI's ordinary Store initialization is recorded, not called read-only.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import sqlite3
import subprocess
from urllib.parse import quote

DIRECTORY = Path(__file__).resolve().parent
ROOT = DIRECTORY.parents[1]
PYTHON = ROOT / ".analysis-tools/runtime/bin/python"
LOCK = ROOT / ".analysis-tools/goal-source-query.lock"
EXPECTED_TOOL_HASH = "c4c127375f044133c328c1fd17782df277426bf64e4bed0be8779602088fafee"
EXPECTED_VERSIONS = {"package_version": "0.13.0", "publication_series": "v13",
    "analyzer_version": "static-multilang-13", "detector_version": "call-rules-12-report-relations", "schema_version": "2"}
OUTPUT = DIRECTORY / "winwincode-cli-report-readback.md"
RECORD = DIRECTORY / "CLI_REPORT_READBACK.json"
CHUNK_SIZE = 1024 * 1024
TABLES = {"snapshots", "findings", "project_latest", "decisions", "sqlite_sequence"}


def digest_file(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for data in iter(lambda: stream.read(CHUNK_SIZE), b""):
            result.update(data)
    return result.hexdigest()


def json_digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True,
        separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def normalized_relative(value: object, *, python: bool = False) -> str:
    if not isinstance(value, str):
        raise RuntimeError("Freeze contains a non-string path")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or str(path) != value or "\\" in value:
        raise RuntimeError("Freeze contains an unsafe relative path")
    if python and not value.endswith(".py"):
        raise RuntimeError("Freeze inventory includes a non-Python module")
    return value


def freeze_identity() -> dict:
    path = DIRECTORY / "CORE_FREEZE.json"
    freeze = json.loads(path.read_text(encoding="utf-8"))
    if any(freeze.get(key) != expected for key, expected in EXPECTED_VERSIONS.items()):
        raise RuntimeError("This helper requires the frozen v13 publication")
    if freeze.get("tool_identity", {}).get("source_hash") != EXPECTED_TOOL_HASH:
        raise RuntimeError("Recorded tool hash differs from the identified v13 freeze")
    expected = freeze.get("package_source_sha256")
    if not isinstance(expected, dict) or not expected:
        raise RuntimeError("Freeze has no exact package inventory")
    for name in expected:
        normalized_relative(name, python=True)
    actual = {}
    tool_hash = hashlib.sha256()
    package = ROOT / "callscope"
    for source in sorted(package.rglob("*.py")):
        name = source.relative_to(package).as_posix()
        raw = source.read_bytes()
        actual[name] = hashlib.sha256(raw).hexdigest()
        tool_hash.update(name.encode())
        tool_hash.update(b"\0")
        tool_hash.update(raw)
        tool_hash.update(b"\0")
    archive = {source.relative_to(DIRECTORY / "frozen-core-source").as_posix(): digest_file(source)
        for source in sorted((DIRECTORY / "frozen-core-source").rglob("*.py"))}
    if actual != expected or archive != expected or tool_hash.hexdigest() != EXPECTED_TOOL_HASH:
        raise RuntimeError("Current package or frozen archive changed after freeze")
    pyproject_hash = freeze.get("pyproject_sha256")
    if (digest_file(ROOT / "pyproject.toml") != pyproject_hash
            or digest_file(DIRECTORY / "frozen-core-source/pyproject.delivery.toml") != pyproject_hash):
        raise RuntimeError("Delivery pyproject changed after freeze")
    for name, expected_hash in freeze.get("policy_files", {}).items():
        if digest_file(DIRECTORY / normalized_relative(name)) != expected_hash:
            raise RuntimeError("Frozen policy changed: " + name)
    for name, expected_hash in freeze.get("benchmark_reports", {}).items():
        if digest_file(DIRECTORY.parent / normalized_relative(name)) != expected_hash:
            raise RuntimeError("Original benchmark changed: " + name)
    return {"freeze_sha256": digest_file(path), "tool_identity": freeze["tool_identity"],
        "package_module_count": len(actual), "pyproject_sha256": pyproject_hash,
        "policy_files": freeze["policy_files"], "effective_policy_sha256": freeze["effective_policy_sha256"],
        **EXPECTED_VERSIONS}


def wal_state(database: Path) -> dict:
    path = Path(str(database) + "-wal")
    size = path.stat().st_size if path.exists() else 0
    return {"path": str(path), "exists": path.exists(), "size_bytes": size, "empty_or_absent": size == 0}


def prerequisites(identity: dict) -> dict:
    publications = {}
    for repository in ("codepatchbay", "winwincode"):
        path = DIRECTORY / (repository + "-integration.json")
        publication = json.loads(path.read_text(encoding="utf-8"))
        if (publication.get("database_closed") is not True
                or publication.get("database_wal_empty_or_absent") is not True
                or publication.get("publication_series") != "v13"):
            raise RuntimeError("Formal publication is not closed: " + repository)
        if any(publication.get(key) != value for key, value in EXPECTED_VERSIONS.items()
                if key != "publication_series"):
            raise RuntimeError("Formal publication version identity differs: " + repository)
        if publication.get("policy_hash") != identity["effective_policy_sha256"][repository]:
            raise RuntimeError("Formal saved policy differs: " + repository)
        if publication.get("stats", {}).get("component_versions", {}).get("tool") != identity["tool_identity"]:
            raise RuntimeError("Formal saved tool identity differs: " + repository)
        database = DIRECTORY / (repository + "-v13.sqlite3")
        if not database.is_file() or not wal_state(database)["empty_or_absent"]:
            raise RuntimeError("Formal database is missing or has a nonempty WAL: " + repository)
        publications[repository] = {"integration_sha256": digest_file(path), "snapshot_id": publication["snapshot_id"],
            "source_hash": publication["source_hash"], "policy_hash": publication["policy_hash"],
            "database": str(database), "database_closed": True, "wal": wal_state(database)}
    return publications


@contextmanager
def query_lock():
    with LOCK.open("a", encoding="utf-8") as stream:
        fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def identifier(value: str) -> str:
    if not value or not value.replace("_", "").isalnum():
        raise RuntimeError("Unexpected SQLite identifier")
    return '"' + value + '"'


def database_state(database: Path, expected: dict) -> dict:
    """Stream hashes of every logical row, including the saved source TEXT.

    sqlite3 incremental BLOB reads can stream existing TEXT bytes without
    deserializing snapshot_json or loading the full snapshot in this process.
    The connection is immutable/read-only and closes before invoking CLI.
    """
    connection = sqlite3.connect("file:" + quote(str(database), safe="/") + "?mode=ro&immutable=1", uri=True)
    try:
        if not hasattr(connection, "blobopen"):
            raise RuntimeError("Trusted Python needs sqlite3 incremental BLOB reads")
        tables = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if tables != TABLES:
            raise RuntimeError("Unexpected formal store table set")
        selected = connection.execute("SELECT id,source_hash,policy_hash,analyzer_version,detector_version,schema_version "
            "FROM snapshots WHERE id=?", (expected["snapshot_id"],)).fetchone()
        if (selected is None or selected[1] != expected["source_hash"] or selected[2] != expected["policy_hash"]
                or selected[3:] != (EXPECTED_VERSIONS["analyzer_version"], EXPECTED_VERSIONS["detector_version"],
                    EXPECTED_VERSIONS["schema_version"])):
            raise RuntimeError("Selected saved snapshot metadata does not match formal integration")
        schema = [list(row) for row in connection.execute(
            "SELECT type,name,tbl_name,rootpage,sql FROM sqlite_master ORDER BY type,name")]
        table_records = {}
        for table in sorted(tables):
            columns = [row[1] for row in connection.execute("PRAGMA table_info(" + identifier(table) + ")")]
            expressions = ["rowid"]
            for column in columns:
                name = identifier(column)
                expressions.extend(["typeof(" + name + ")", "CASE WHEN typeof(" + name + ") IN ('integer','real') THEN "
                    + name + " ELSE NULL END", "CASE WHEN typeof(" + name + ") IN ('text','blob') THEN length(CAST("
                    + name + " AS BLOB)) ELSE NULL END"])
            digest, count = hashlib.sha256(), 0
            for row in connection.execute("SELECT " + ",".join(expressions) + " FROM " + identifier(table) + " ORDER BY rowid"):
                rowid, values = row[0], []
                for index, column in enumerate(columns):
                    kind, scalar, byte_count = row[1 + index * 3:4 + index * 3]
                    if kind in {"text", "blob"}:
                        content = hashlib.sha256()
                        if byte_count <= CHUNK_SIZE:
                            # Small indexed/system-table cells need no BLOB
                            # handle. The saved source TEXT is streamed below.
                            value = connection.execute("SELECT CAST(" + identifier(column) + " AS BLOB) FROM "
                                + identifier(table) + " WHERE rowid=?", (rowid,)).fetchone()[0]
                            content.update(value)
                        else:
                            with connection.blobopen(table, column, rowid, readonly=True) as blob:
                                for data in iter(lambda: blob.read(CHUNK_SIZE), b""):
                                    content.update(data)
                        values.append([column, kind, byte_count, content.hexdigest()])
                    elif kind in {"integer", "real", "null"}:
                        values.append([column, kind, scalar])
                    else:
                        raise RuntimeError("Unexpected SQLite value kind")
                digest.update(json.dumps([rowid, values], ensure_ascii=True, separators=(",", ":"),
                    allow_nan=False).encode())
                digest.update(b"\n")
                count += 1
            table_records[table] = {"row_count": count, "row_content_sha256": digest.hexdigest()}
        logical = {"schema": schema, "tables": table_records,
            "application_id": connection.execute("PRAGMA application_id").fetchone()[0],
            "user_version": connection.execute("PRAGMA user_version").fetchone()[0]}
    finally:
        connection.close()
    return {"database_file_sha256": digest_file(database), "database_size_bytes": database.stat().st_size,
        "logical_content_sha256": json_digest(logical), "table_records": table_records,
        "schema_sha256": json_digest(schema), "application_id": logical["application_id"],
        "user_version": logical["user_version"], "wal": wal_state(database),
        "fingerprint_connection": "sqlite3 mode=ro&immutable=1; incremental existing TEXT/BLOB reads"}


def same_bytes(first: Path, second: Path) -> bool:
    if first.stat().st_size != second.stat().st_size:
        return False
    with first.open("rb") as left, second.open("rb") as right:
        while True:
            a, b = left.read(CHUNK_SIZE), right.read(CHUNK_SIZE)
            if a != b:
                return False
            if not a:
                return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", required=True,
        help="perform the saved-report CLI export after both formal integrations report closed stores")
    parser.parse_args()
    for path in (OUTPUT, RECORD):
        if path.exists():
            raise FileExistsError("Readback outputs are exclusive; preserve existing artifact: " + str(path))
    with query_lock():
        for path in (OUTPUT, RECORD):
            if path.exists():
                raise FileExistsError("Readback output already exists: " + str(path))
        identity = freeze_identity()
        publications = prerequisites(identity)
        expected = publications["winwincode"]
        database = Path(expected["database"])
        reference = DIRECTORY / "winwincode-automatic-report.md"
        reference_hash = digest_file(reference)
        if not PYTHON.is_file():
            raise RuntimeError("Fixed trusted Python is missing")
        before = database_state(database, expected)
        command = [str(PYTHON), "-m", "callscope", "report", "--db", str(database),
            "--snapshot", expected["snapshot_id"], "--format", "markdown", "--output", str(OUTPUT)]
        environment = dict(os.environ)
        environment.update(PYTHONPATH=str(ROOT), PYTHONDONTWRITEBYTECODE="1", PYTHONNOUSERSITE="1")
        started = datetime.now(timezone.utc).isoformat()
        print(json.dumps({"state": "normal_saved_report_cli_export_started", "snapshot_id": expected["snapshot_id"],
            "tool_identity": identity["tool_identity"], "target_executed": False}), flush=True)
        process = subprocess.run(command, cwd=ROOT, env=environment, text=True, capture_output=True, check=False)
        after = database_state(database, expected)
        unchanged_identity = freeze_identity() == identity
        after_publications = prerequisites(identity)
        unchanged_publications = ({name: {key: value for key, value in entry.items() if key != "wal"}
            for name, entry in after_publications.items()} == {name: {key: value for key, value in entry.items() if key != "wal"}
            for name, entry in publications.items()})
        unchanged_reference = digest_file(reference) == reference_hash
        output_exists = OUTPUT.is_file()
        exported_hash = digest_file(OUTPUT) if output_exists else None
        byte_match = output_exists and same_bytes(reference, OUTPUT)
        logical_unchanged = before["logical_content_sha256"] == after["logical_content_sha256"]
        record = {"kind": "normal_saved_report_cli_readback", "repository": "winwincode", "started_at": started,
            "completed_at": datetime.now(timezone.utc).isoformat(), "snapshot_id": expected["snapshot_id"],
            "source_hash": expected["source_hash"], "policy_hash": expected["policy_hash"],
            "identity": identity, "formal_publications": publications,
            "formal_publications_after_cli": after_publications,
            "command": command, "cwd": str(ROOT), "fixed_pythonpath": str(ROOT),
            "fixed_pythondontwritebytecode": "1", "fixed_python_no_user_site": "1",
            "returncode": process.returncode, "stdout": process.stdout, "stderr": process.stderr,
            "reference_artifact": str(reference), "reference_sha256": reference_hash,
            "exported_artifact": str(OUTPUT), "exported_sha256": exported_hash,
            "markdown_bytes_equal": bool(byte_match), "markdown_sha256_equal": exported_hash == reference_hash,
            "database_before": before, "database_after": after,
            "logical_database_rows_schema_and_identity_unchanged": logical_unchanged,
            "database_physical_bytes_unchanged": before["database_file_sha256"] == after["database_file_sha256"],
            "ordinary_tool_store_initialization": {"normal_store_constructor_invoked": process.returncode == 0,
                "connection_was_not_readonly": True, "source_contract": "Store.__init__ performs WAL/synchronous/application_id/user_version and CREATE IF NOT EXISTS setup",
                "initialization_physical_effects_were_permitted_and_measured": True,
                "publish_scan_or_decision_command_invoked": False},
            "freeze_identity_unchanged": unchanged_identity,
            "integration_and_prerequisite_state_unchanged": unchanged_publications,
            "formal_markdown_unchanged": unchanged_reference, "common_lock": str(LOCK),
            "target_worktree_opened": False, "target_executed": False, "target_imported": False,
            "target_tests_run": False, "target_build_run": False, "analysis_rescanned": False,
            "tool_test_suite_run": False, "synthetic_fixture_used": False}
        record["successful_readback"] = bool(process.returncode == 0 and byte_match and logical_unchanged
            and after["wal"]["empty_or_absent"] and unchanged_identity and unchanged_publications and unchanged_reference)
        with RECORD.open("x", encoding="utf-8") as stream:
            json.dump(record, stream, ensure_ascii=False, indent=2, allow_nan=False)
            stream.write("\n")
        print(json.dumps({"record": str(RECORD), "successful_readback": record["successful_readback"],
            "markdown_bytes_equal": record["markdown_bytes_equal"], "logical_database_unchanged": logical_unchanged}), flush=True)
        return 0 if record["successful_readback"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
