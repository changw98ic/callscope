"""Immutable static-analysis snapshots and independent reviewer decisions.

Only JSON from the shared models is persisted. Nothing in this module imports
or executes a target project. The SQLite triggers protect append-only records
through the ordinary application connection; the audit hash chain is not a
claim that a database administrator cannot alter or truncate the database.
"""

from __future__ import annotations

from dataclasses import asdict, fields
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import sqlite3
from threading import RLock
from typing import Any, Iterable, TypeVar
from uuid import uuid4

from .models import (
    Diagnostic,
    Edge,
    Evidence,
    Finding,
    GraphSnapshot,
    Node,
    SourceFile,
)


_Model = TypeVar("_Model")
_DATABASE_VERSION = 1
_APPLICATION_ID = 0x43414C4C
_ACTIONS = frozenset({"accept_risk", "false_positive", "fix_planned"})
_GENESIS_HASH = "0" * 64


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _json(value: Any) -> str:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    )


def _object(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("Stored model must be a JSON object")
    return value


def _model(cls: type[_Model], value: Any) -> _Model:
    """Ignore unknown compatibility fields; never deserialize executable data."""
    obj = _object(value)
    allowed = {item.name for item in fields(cls)}
    try:
        return cls(**{key: val for key, val in obj.items() if key in allowed})
    except TypeError as exc:
        raise ValueError(f"Invalid stored {cls.__name__}: {exc}") from exc


def _list(obj: dict[str, Any], name: str) -> list[Any]:
    value = obj.get(name, [])
    if not isinstance(value, list):
        raise ValueError(f"Stored field {name!r} must be a JSON array")
    return value


def _parser_version(obj: dict[str, Any]) -> str:
    recorded = obj.get("parser_version")
    return recorded if isinstance(recorded, str) and recorded.strip() else "legacy-unknown"


def _snapshot_versions(
    obj: dict[str, Any], detector_version: str | None, schema_version: str | None,
) -> None:
    """Use the persisted run identity, not this process's model defaults."""
    for key, recorded in (
        ("detector_version", detector_version), ("schema_version", schema_version),
    ):
        valid_recorded = isinstance(recorded, str) and bool(recorded.strip())
        present = obj.get(key)
        if not isinstance(present, str) or not present.strip():
            obj[key] = recorded if valid_recorded else "legacy-unknown"
        elif valid_recorded and present != recorded:
            raise ValueError(f"Stored snapshot {key} disagrees with its metadata")
    # Older JSON has no parser identity; the dataclass default is this host's
    # version and must never be assigned to a historical analysis implicitly.
    obj["parser_version"] = _parser_version(obj)


def _snapshot_from_json(
    value: str, detector_version: str | None = None, schema_version: str | None = None,
) -> GraphSnapshot:
    obj = _object(json.loads(value))
    _snapshot_versions(obj, detector_version, schema_version)
    obj["nodes"] = [_model(Node, item) for item in _list(obj, "nodes")]
    obj["edges"] = [_model(Edge, item) for item in _list(obj, "edges")]
    obj["files"] = [_model(SourceFile, item) for item in _list(obj, "files")]
    obj["diagnostics"] = [
        _model(Diagnostic, item) for item in _list(obj, "diagnostics")
    ]
    return _model(GraphSnapshot, obj)


def _finding_from_json(value: str) -> Finding:
    obj = _object(json.loads(value))
    obj["evidence"] = [_model(Evidence, item) for item in _list(obj, "evidence")]
    return _model(Finding, obj)


def _text(value: Any, name: str, maximum: int | None = None) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    normalized = value.strip()
    if maximum is not None and len(normalized) > maximum:
        raise ValueError(f"{name} exceeds {maximum} characters")
    return normalized


def _expiry(value: str | None) -> str | None:
    if value is None:
        return None
    raw = _text(value, "expires_at", 128)
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        moment = datetime.fromisoformat(raw)
    except ValueError as exc:
        raise ValueError("expires_at must be an ISO8601 datetime") from exc
    if moment.tzinfo is None or moment.utcoffset() is None:
        raise ValueError("expires_at must include a timezone")
    moment = moment.astimezone(timezone.utc)
    if moment <= datetime.now(timezone.utc):
        raise ValueError("expires_at must be in the future")
    return moment.isoformat()


_SCHEMA = """
BEGIN IMMEDIATE;
CREATE TABLE IF NOT EXISTS snapshots (
    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
    id TEXT NOT NULL UNIQUE,
    project_id TEXT NOT NULL,
    project_name TEXT NOT NULL,
    root TEXT NOT NULL,
    created_at TEXT NOT NULL,
    published_at TEXT NOT NULL,
    source_hash TEXT NOT NULL,
    policy_hash TEXT NOT NULL,
    analyzer_version TEXT NOT NULL,
    detector_version TEXT NOT NULL,
    schema_version TEXT NOT NULL,
    status TEXT NOT NULL,
    stats_json TEXT NOT NULL,
    snapshot_json TEXT NOT NULL,
    finding_count INTEGER NOT NULL CHECK (finding_count >= 0),
    UNIQUE (project_id, id)
);
CREATE INDEX IF NOT EXISTS snapshots_project_sequence
    ON snapshots (project_id, sequence DESC);
CREATE TABLE IF NOT EXISTS findings (
    snapshot_id TEXT NOT NULL REFERENCES snapshots (id),
    id TEXT NOT NULL,
    ordinal INTEGER NOT NULL,
    finding_json TEXT NOT NULL,
    PRIMARY KEY (snapshot_id, id)
);
CREATE TABLE IF NOT EXISTS project_latest (
    project_id TEXT PRIMARY KEY,
    snapshot_id TEXT NOT NULL,
    published_at TEXT NOT NULL,
    FOREIGN KEY (project_id, snapshot_id)
        REFERENCES snapshots (project_id, id)
);
CREATE TABLE IF NOT EXISTS decisions (
    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
    id TEXT NOT NULL UNIQUE,
    snapshot_id TEXT NOT NULL,
    finding_id TEXT NOT NULL,
    action TEXT NOT NULL
        CHECK (action IN ('accept_risk', 'false_positive', 'fix_planned')),
    reason TEXT NOT NULL,
    actor TEXT NOT NULL,
    created_at TEXT NOT NULL,
    expires_at TEXT,
    previous_hash TEXT NOT NULL,
    entry_hash TEXT NOT NULL,
    content_json TEXT NOT NULL,
    FOREIGN KEY (snapshot_id, finding_id)
        REFERENCES findings (snapshot_id, id)
);
CREATE INDEX IF NOT EXISTS decisions_finding_sequence
    ON decisions (snapshot_id, finding_id, sequence DESC);
CREATE TRIGGER IF NOT EXISTS snapshots_no_update
    BEFORE UPDATE ON snapshots BEGIN
        SELECT RAISE(ABORT, 'Analysis snapshots are append-only');
    END;
CREATE TRIGGER IF NOT EXISTS snapshots_no_delete
    BEFORE DELETE ON snapshots BEGIN
        SELECT RAISE(ABORT, 'Analysis snapshots are append-only');
    END;
CREATE TRIGGER IF NOT EXISTS findings_no_update
    BEFORE UPDATE ON findings BEGIN
        SELECT RAISE(ABORT, 'Analysis findings are append-only');
    END;
CREATE TRIGGER IF NOT EXISTS findings_no_delete
    BEFORE DELETE ON findings BEGIN
        SELECT RAISE(ABORT, 'Analysis findings are append-only');
    END;
CREATE TRIGGER IF NOT EXISTS decisions_no_update
    BEFORE UPDATE ON decisions BEGIN
        SELECT RAISE(ABORT, 'Reviewer decisions are append-only');
    END;
CREATE TRIGGER IF NOT EXISTS decisions_no_delete
    BEFORE DELETE ON decisions BEGIN
        SELECT RAISE(ABORT, 'Reviewer decisions are append-only');
    END;
PRAGMA user_version = 1;
COMMIT;
"""


class Store:
    """A serialized SQLite connection safe for calls from HTTP worker threads.

    ``publish`` returns False for an identical existing analysis and still
    selects it as that project's latest snapshot. Conflicting facts under the
    same ID raise ValueError. The original creation time is preserved on a
    repeated scan. Missing snapshot reads return None or an empty finding list;
    decisions require both the snapshot and its finding to exist.
    """

    def __init__(self, path: str | Path):
        self.path = str(path)
        if self.path != ":memory:":
            database = Path(path).expanduser().resolve()
            database.parent.mkdir(parents=True, exist_ok=True)
            self.path = str(database)
        self._lock = RLock()
        self._connection = sqlite3.connect(
            self.path, timeout=30, isolation_level=None, check_same_thread=False,
        )
        self._connection.row_factory = sqlite3.Row
        try:
            self._connection.execute("PRAGMA foreign_keys = ON")
            self._connection.execute("PRAGMA busy_timeout = 30000")
            application_id = self._connection.execute(
                "PRAGMA application_id"
            ).fetchone()[0]
            version = self._connection.execute("PRAGMA user_version").fetchone()[0]
            if application_id not in (0, _APPLICATION_ID):
                raise ValueError("The selected SQLite file belongs to another application")
            if version > _DATABASE_VERSION:
                raise ValueError("The selected store uses a newer database schema")
            self._connection.execute("PRAGMA journal_mode = WAL")
            self._connection.execute("PRAGMA synchronous = FULL")
            self._connection.executescript(_SCHEMA)
            self._connection.execute(f"PRAGMA application_id = {_APPLICATION_ID}")
        except BaseException:
            self._connection.close()
            raise

    def close(self) -> None:
        with self._lock:
            self._connection.close()

    def __enter__(self) -> Store:
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    def publish(self, snapshot: GraphSnapshot, findings: Iterable[Finding]) -> bool:
        if not isinstance(snapshot, GraphSnapshot):
            raise ValueError("snapshot must be a GraphSnapshot")
        if snapshot.id != _text(snapshot.id, "snapshot.id"):
            raise ValueError("snapshot.id must not have surrounding whitespace")
        if snapshot.project_id != _text(snapshot.project_id, "snapshot.project_id"):
            raise ValueError("snapshot.project_id must not have surrounding whitespace")
        _text(snapshot.detector_version, "snapshot.detector_version")
        _text(snapshot.schema_version, "snapshot.schema_version")
        _text(snapshot.parser_version, "snapshot.parser_version")
        snapshot_object = asdict(snapshot)
        snapshot_json = _json(snapshot_object)
        finding_documents: dict[str, str] = {}
        for finding in findings:
            if not isinstance(finding, Finding):
                raise ValueError("findings must contain Finding models")
            if finding.id != _text(finding.id, "finding.id"):
                raise ValueError("finding.id must not have surrounding whitespace")
            if finding.id in finding_documents:
                raise ValueError(f"Duplicate finding ID: {finding.id}")
            if finding.snapshot_id and finding.snapshot_id != snapshot.id:
                raise ValueError("Every finding must belong to the published snapshot")
            document = asdict(finding)
            document["snapshot_id"] = snapshot.id
            finding_documents[finding.id] = _json(document)
        with self._lock:
            connection = self._connection
            connection.execute("BEGIN IMMEDIATE")
            try:
                published_at = _utc_now()
                existing = connection.execute(
                    """SELECT snapshot_json, detector_version, schema_version
                    FROM snapshots WHERE id = ?""",
                    (snapshot.id,),
                ).fetchone()
                inserted = existing is None
                if existing is not None:
                    old_object = _object(json.loads(existing["snapshot_json"]))
                    _snapshot_versions(
                        old_object, existing["detector_version"], existing["schema_version"],
                    )
                    comparable = dict(snapshot_object)
                    # The optional v2 support evidence defaults to empty when
                    # reading legacy snapshots; it adds no facts to those runs.
                    if "input_evidence" not in old_object and not comparable.get("input_evidence"):
                        comparable.pop("input_evidence", None)
                    old_object.pop("created_at", None)
                    comparable.pop("created_at", None)
                    old_findings = {
                        row["id"]: row["finding_json"]
                        for row in connection.execute(
                            "SELECT id, finding_json FROM findings WHERE snapshot_id = ?",
                            (snapshot.id,),
                        )
                    }
                    if (
                        _json(old_object) != _json(comparable)
                        or old_findings != finding_documents
                        or existing["detector_version"] != snapshot.detector_version
                        or existing["schema_version"] != snapshot.schema_version
                    ):
                        raise ValueError("Snapshot ID already exists with different immutable facts")
                else:
                    connection.execute(
                        """INSERT INTO snapshots
                        (id, project_id, project_name, root, created_at, published_at,
                         source_hash, policy_hash, analyzer_version, detector_version,
                         schema_version, status, stats_json, snapshot_json, finding_count)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (
                            snapshot.id, snapshot.project_id, snapshot.project_name,
                            snapshot.root, snapshot.created_at, published_at,
                            snapshot.source_hash, snapshot.policy_hash,
                            snapshot.analyzer_version, snapshot.detector_version,
                            snapshot.schema_version,
                            snapshot.status, _json(snapshot.stats), snapshot_json,
                            len(finding_documents),
                        ),
                    )
                    connection.executemany(
                        """INSERT INTO findings (snapshot_id, id, ordinal, finding_json)
                        VALUES (?, ?, ?, ?)""",
                        [
                            (snapshot.id, finding_id, ordinal, document)
                            for ordinal, (finding_id, document) in enumerate(
                                finding_documents.items()
                            )
                        ],
                    )
                connection.execute(
                    """INSERT INTO project_latest (project_id, snapshot_id, published_at)
                    VALUES (?, ?, ?)
                    ON CONFLICT (project_id) DO UPDATE SET
                        snapshot_id = excluded.snapshot_id,
                        published_at = excluded.published_at""",
                    (snapshot.project_id, snapshot.id, published_at),
                )
                connection.commit()
                return inserted
            except BaseException:
                connection.rollback()
                raise

    def latest(self, project_id: str | None = None) -> GraphSnapshot | None:
        with self._lock:
            row = self._connection.execute(
                """SELECT s.snapshot_json, s.detector_version, s.schema_version
                FROM project_latest p
                JOIN snapshots s ON s.project_id = p.project_id AND s.id = p.snapshot_id
                WHERE (? IS NULL OR p.project_id = ?)
                ORDER BY p.published_at DESC, s.sequence DESC LIMIT 1""",
                (project_id, project_id),
            ).fetchone()
            return _snapshot_from_json(
                row["snapshot_json"], row["detector_version"], row["schema_version"],
            ) if row else None

    def get_snapshot(self, snapshot_id: str) -> GraphSnapshot | None:
        with self._lock:
            row = self._connection.execute(
                """SELECT snapshot_json, detector_version, schema_version
                FROM snapshots WHERE id = ?""", (snapshot_id,),
            ).fetchone()
            return _snapshot_from_json(
                row["snapshot_json"], row["detector_version"], row["schema_version"],
            ) if row else None

    def list_snapshots(self, project_id: str | None = None) -> list[dict[str, Any]]:
        with self._lock:
            rows = self._connection.execute(
                """SELECT s.id, s.project_id, s.project_name, s.root, s.created_at,
                    s.published_at, s.source_hash, s.policy_hash, s.analyzer_version,
                    s.detector_version, s.schema_version, s.status, s.stats_json,
                    s.snapshot_json,
                    s.finding_count,
                    CASE WHEN p.snapshot_id = s.id THEN 1 ELSE 0 END AS is_latest
                FROM snapshots s LEFT JOIN project_latest p ON p.project_id = s.project_id
                WHERE (? IS NULL OR s.project_id = ?)
                ORDER BY s.sequence DESC""",
                (project_id, project_id),
            ).fetchall()
            items = []
            for row in rows:
                item = dict(row)
                snapshot_obj = _object(json.loads(item.pop("snapshot_json")))
                item["parser_version"] = _parser_version(snapshot_obj)
                item["stats"] = _object(json.loads(item.pop("stats_json")))
                item["is_latest"] = bool(item["is_latest"])
                items.append(item)
            return items

    def get_findings(self, snapshot_id: str) -> list[Finding]:
        with self._lock:
            rows = self._connection.execute(
                """SELECT finding_json FROM findings WHERE snapshot_id = ?
                ORDER BY ordinal, id""", (snapshot_id,),
            ).fetchall()
            return [_finding_from_json(row["finding_json"]) for row in rows]

    def record_decision(
        self, snapshot_id: str, finding_id: str, action: str, reason: str,
        actor: str = "local", expires_at: str | None = None,
    ) -> dict[str, Any]:
        snapshot_id = _text(snapshot_id, "snapshot_id")
        finding_id = _text(finding_id, "finding_id")
        action = _text(action, "action")
        if action not in _ACTIONS:
            raise ValueError("action must be accept_risk, false_positive, or fix_planned")
        reason = _text(reason, "reason", 10000)
        actor = _text(actor, "actor", 256)
        expires_at = _expiry(expires_at)
        with self._lock:
            connection = self._connection
            connection.execute("BEGIN IMMEDIATE")
            try:
                snapshot_exists = connection.execute(
                    "SELECT 1 FROM snapshots WHERE id = ?", (snapshot_id,),
                ).fetchone()
                if snapshot_exists is None:
                    raise KeyError(f"Unknown snapshot: {snapshot_id}")
                finding_exists = connection.execute(
                    "SELECT 1 FROM findings WHERE snapshot_id = ? AND id = ?",
                    (snapshot_id, finding_id),
                ).fetchone()
                if finding_exists is None:
                    raise KeyError(f"Unknown finding in snapshot {snapshot_id}: {finding_id}")
                previous = connection.execute(
                    "SELECT entry_hash FROM decisions ORDER BY sequence DESC LIMIT 1"
                ).fetchone()
                content = {
                    "id": uuid4().hex,
                    "snapshot_id": snapshot_id,
                    "finding_id": finding_id,
                    "action": action,
                    "reason": reason,
                    "actor": actor,
                    "created_at": _utc_now(),
                    "expires_at": expires_at,
                    "previous_hash": previous["entry_hash"] if previous else _GENESIS_HASH,
                }
                content_json = _json(content)
                entry_hash = sha256(content_json.encode("utf-8")).hexdigest()
                cursor = connection.execute(
                    """INSERT INTO decisions
                    (id, snapshot_id, finding_id, action, reason, actor, created_at,
                     expires_at, previous_hash, entry_hash, content_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        content["id"], snapshot_id, finding_id, action, reason, actor,
                        content["created_at"], expires_at, content["previous_hash"],
                        entry_hash, content_json,
                    ),
                )
                connection.commit()
                return {**content, "entry_hash": entry_hash, "sequence": cursor.lastrowid}
            except BaseException:
                connection.rollback()
                raise

    def list_decisions(
        self, snapshot_id: str | None = None, finding_id: str | None = None,
    ) -> list[dict[str, Any]]:
        with self._lock:
            rows = self._connection.execute(
                """SELECT sequence, entry_hash, content_json FROM decisions
                WHERE (? IS NULL OR snapshot_id = ?) AND (? IS NULL OR finding_id = ?)
                ORDER BY sequence DESC""",
                (snapshot_id, snapshot_id, finding_id, finding_id),
            ).fetchall()
            return [
                {
                    **_object(json.loads(row["content_json"])),
                    "entry_hash": row["entry_hash"], "sequence": row["sequence"],
                }
                for row in rows
            ]

    def verify_audit_chain(self) -> dict[str, Any]:
        """Check local chain consistency; detecting tail removal needs an external anchor."""
        with self._lock:
            rows = self._connection.execute(
                "SELECT * FROM decisions ORDER BY sequence"
            ).fetchall()
            expected_previous = _GENESIS_HASH
            for row in rows:
                try:
                    content = _object(json.loads(row["content_json"]))
                    expected_hash = sha256(_json(content).encode("utf-8")).hexdigest()
                    aligned = all(
                        content.get(key) == row[key]
                        for key in (
                            "id", "snapshot_id", "finding_id", "action", "reason",
                            "actor", "created_at", "expires_at", "previous_hash",
                        )
                    )
                except (ValueError, TypeError):
                    expected_hash, aligned = "", False
                if (
                    not aligned or row["previous_hash"] != expected_previous
                    or row["entry_hash"] != expected_hash
                ):
                    return {
                        "valid": False, "entries": len(rows),
                        "first_invalid_sequence": row["sequence"],
                    }
                expected_previous = row["entry_hash"]
            return {"valid": True, "entries": len(rows), "head_hash": expected_previous}
