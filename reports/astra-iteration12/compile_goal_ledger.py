"""Compile implementation tracking from saved static_goal_judgment results.

This stdlib-only report helper reads immutable analysis data and frozen report
definitions. It neither runs analyzers nor imports, executes, builds or tests a
target project. The five-goal/thirty-obligation ledger is an implementation
index, not a replacement benchmark for the two original complete reports.

Default inputs are the future codepatchbay-v14.sqlite3/winwincode-v14.sqlite3
and CORE_FREEZE.json in this directory. Existing outputs are refused.
"""

from __future__ import annotations

import argparse
from collections import Counter
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import tempfile
from typing import Any

VERSION = "saved-goal-implementation-ledger-2"
HERE = Path(__file__).resolve().parent
REPORTS = HERE.parent
ORIGINAL = REPORTS / "astra-iteration4"
LOCK = REPORTS.parent / ".analysis-tools/goal-source-query.lock"
DEFINITIONS = {
    "CPB-01": ("codepatchbay", "pipeline", tuple(f"P{i}" for i in range(1, 7))),
    "CPB-02": ("codepatchbay", "status", tuple(f"S{i}" for i in range(1, 6))),
    "CPB-03": ("codepatchbay", "atomicity", tuple(f"A{i}" for i in range(1, 8))),
    "WWC-01": ("winwincode", "navigation", tuple(f"N{i}" for i in range(1, 8))),
    "WWC-02": ("winwincode", "device", tuple(f"D{i}" for i in range(1, 6))),
}
FROZEN_HASHES = {
    "astra-iteration4/GOAL_ACCEPTANCE.md": "9b6f4fda6aa24f055e288690e76405779e36758f8ba986799f78f2f96aa8d118",
    "astra-iteration4/goal-ledger.template.json": "d33f48b4f0908458b587e3ad4a97d3b40eb46e3b7eb291d04d053155a5c6ad04",
    "astra-baseline/capability-baseline.json": "16b4b05c8818fa1eecf396132ebe2ea29a8f0068801165f0649da379d9041dd7",
    "astra-baseline/CODEPATCHBAY_ANALYSIS.md": "863f5dfe52ced7129a0bda499afa4a89b30d2db9396c654a5120204cfe422900",
    "astra-baseline/WINWINCODE_ANALYSIS.md": "b3f8b1def361595e2bd3540a6bca5381ef4ad2a71d4f3c49535bf3f24f212950",
}
_SCOPE_KEYS = ("source_roots", "excluded_paths", "symlinks_skipped", "scan_errors", "unsupported_files")
_METADATA_KEYS = ("id", "project_id", "project_name", "root", "source_hash", "policy_hash",
                  "analyzer_version", "detector_version", "schema_version", "status")


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=True, sort_keys=True,
        separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()


def file_hash(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def reject_constant(value: str) -> None:
    raise ValueError(f"Nonfinite JSON value is not report evidence: {value}")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"), parse_constant=reject_constant)


def walk(value: Any, pointer: str = ""):
    yield pointer, value
    if isinstance(value, dict):
        for key, child in value.items():
            token = str(key).replace("~", "~0").replace("/", "~1")
            yield from walk(child, pointer + "/" + token)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, pointer + "/" + str(index))


def at_pointer(value: Any, pointer: str) -> Any:
    if pointer and not pointer.startswith("/"):
        raise ValueError("JSON pointer must be absolute")
    for token in pointer[1:].split("/") if pointer else []:
        token = token.replace("~1", "/").replace("~0", "~")
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def ensure_frozen_definitions() -> tuple[dict, dict]:
    inventory = {}
    for relative, expected in FROZEN_HASHES.items():
        path = REPORTS / relative
        actual = file_hash(path)
        if actual != expected:
            raise ValueError(f"Frozen original file changed: {relative}")
        inventory[relative] = {"sha256": actual, "size_bytes": path.stat().st_size}
    template = read_json(ORIGINAL / "goal-ledger.template.json")
    if template.get("goal_count") != 5 or template.get("required_obligation_count") != 30:
        raise ValueError("Original implementation index changed")
    if [goal.get("id") for goal in template["goals"]] != list(DEFINITIONS):
        raise ValueError("Original goal IDs/order changed")
    for goal in template["goals"]:
        repository, _, required = DEFINITIONS[goal["id"]]
        if goal.get("repository") != repository or goal.get("claim", {}).get("source_claim_id") != goal["id"]:
            raise ValueError("Original goal/repository/claim identity changed")
        if [item.get("id") for item in goal["obligations"]] != [goal["id"] + "." + key for key in required]:
            raise ValueError("Original necessary obligation IDs changed")
        if any(item.get("required") is not True for item in goal["obligations"]):
            raise ValueError("Original required obligation was removed")
    return template, inventory


def authenticate_freeze(freeze_path: Path, original_inventory: dict) -> tuple[dict, dict]:
    """Authenticate publication inputs without loading or importing an analyzer."""
    freeze_path = freeze_path.resolve(strict=True)
    freeze = read_json(freeze_path)
    benchmarks = {key: value["sha256"] for key, value in original_inventory.items()
                  if key.endswith("_ANALYSIS.md")}
    if freeze.get("benchmark_reports") != benchmarks:
        raise ValueError("Frozen publication benchmark differs from the two original reports")
    expected_names = {repository + "-policy.json" for repository in ("codepatchbay", "winwincode")}
    if set(freeze.get("policy_files", {})) != expected_names:
        raise ValueError("Frozen publication must identify both original repository policy inputs")
    policies = {}
    for repository in ("codepatchbay", "winwincode"):
        name = repository + "-policy.json"
        path = freeze_path.parent / name
        expected = freeze["policy_files"][name]
        if file_hash(path) != expected:
            raise ValueError(f"Publication policy bytes differ from the frozen manifest: {name}")
        config = read_json(path)
        goals = config.get("goal_contracts", [])
        actual = [(rule.get("goal_id"), rule.get("analyzer")) for rule in goals]
        expected_goals = [(goal, adapter) for goal, (repo, adapter, _) in DEFINITIONS.items() if repo == repository]
        if actual != expected_goals or any(rule.get("id") != rule.get("contract", {}).get("id") for rule in goals):
            raise ValueError(f"Frozen policy goal/adapter/inner-rule mapping differs: {repository}")
        normalized = deepcopy(config)
        # These published files already declare every configuration default.
        # The frozen loader additionally canonicalizes the order of these two
        # data-only lists. Mirror those exact transformations without importing
        # validators, analyzers or the target, and compare the entire result.
        section = normalized["analysis"]
        section["support_inputs"] = sorted(section["support_inputs"])
        section["rust_helper_profiles"] = sorted(section["rust_helper_profiles"],
            key=lambda profile: (profile["crate_root"], profile["id"], profile["workspace_manifest"]))
        policies[repository] = {"config": normalized, "path": str(path.resolve()),
            "file_sha256": expected, "file_json_canonical_sha256": digest(config),
            "canonical_policy_sha256": digest(normalized),
            "loader_list_canonicalization": {"support_inputs": "sorted_paths",
                "rust_helper_profiles": "sorted_crate_root_id_workspace_manifest",
                "frozen_module_sha256": {name: freeze["module_sha256"][name]
                    for name in ("config", "input_capture", "rust_helpers")}}}
    return freeze, policies


@contextmanager
def source_read_lock():
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    with LOCK.open("a") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def authenticate_source(record: dict) -> tuple[bytes, int]:
    content = record.get("content")
    if not isinstance(content, str):
        raise ValueError("Saved source is not a text record")
    data = content.encode("utf-8")
    expected = record.get("hash")
    if expected == hashlib.sha256(data).hexdigest():
        return data, 0
    if expected == hashlib.sha256(b"\xef\xbb\xbf" + data).hexdigest():
        return data, 3
    raise ValueError(f"Saved source text/hash mismatch: {record.get('path')}")


def validate_locations(value: Any, sources: dict[str, dict], snapshot_id: str) -> dict:
    verified, unique, saved_span_hashes, coordinate_only_spans = 0, set(), 0, 0
    for pointer, item in walk(value):
        if not isinstance(item, dict) or not item.get("file") or not item.get("source_hash"):
            continue
        file = item["file"]
        if file not in sources:
            raise ValueError(f"Location refers to an uncaptured source: {file}")
        source = sources[file]
        if item["source_hash"] != source["hash"]:
            raise ValueError(f"Original source file SHA mismatch: {file} at {pointer}")
        if "snapshot_id" in item and item["snapshot_id"] != snapshot_id:
            raise ValueError(f"Source record belongs to a different snapshot: {file} at {pointer}")
        data, prefix = authenticate_source(source)
        start, end = item.get("start_byte"), item.get("end_byte")
        if start is not None or end is not None:
            if type(start) is not int or type(end) is not int or not 0 <= start <= end <= len(data):
                raise ValueError(f"Source span is incomplete or outside original text: {file}")
            if "span_hash" in item:
                if item["span_hash"] != hashlib.sha256(data[start:end]).hexdigest():
                    raise ValueError(f"Original span SHA mismatch: {file}:{start}:{end} at {pointer}; "
                                     f"saved={item.get('span_hash')!r}, actual={hashlib.sha256(data[start:end]).hexdigest()}")
                saved_span_hashes += 1
            else:
                # A flow anchor can save authenticated original coordinates
                # without declaring a span hash. Check its bytes/bounds, retain
                # that source form, and do not invent a saved hash or a gap.
                coordinate_only_spans += 1
            for key, expected in (("original_file_start_byte", start + prefix),
                                  ("original_file_end_byte", end + prefix), ("raw_prefix_bytes", prefix)):
                if key in item and item[key] != expected:
                    raise ValueError(f"Original byte/BOM coordinate mismatch: {file}:{key}")
            for key, offset in (("line", start), ("end_line", end)):
                if key in item and item[key] != data[:offset].count(b"\n") + 1:
                    raise ValueError(f"Original line coordinate mismatch: {file}:{key}")
            column_base = item.get("column_base", 1)
            for key, offset in (("column", start), ("end_column", end)):
                if key in item and item.get("column_unit", "utf8_bytes") == "utf8_bytes":
                    expected = offset - (data.rfind(b"\n", 0, offset) + 1) + column_base
                    if item[key] != expected:
                        raise ValueError(f"Original column coordinate mismatch: {file}:{key}")
        identity = item.get("parse_identity")
        if isinstance(identity, dict):
            if identity.get("snapshot_id") not in {None, snapshot_id}:
                raise ValueError("Location parse identity belongs to a different snapshot")
            text_hash = identity.get("original_text_utf8_sha256")
            if text_hash is not None and text_hash != hashlib.sha256(data).hexdigest():
                raise ValueError("Original parse text SHA mismatch")
        verified += 1
        unique.add((file, item["source_hash"], start, end, item.get("span_hash")))
    return {"authenticated_location_records": verified, "unique_authenticated_locations": len(unique),
            "authenticated_saved_span_hash_records": saved_span_hashes,
            "authenticated_coordinate_spans_without_saved_span_hash": coordinate_only_spans,
            "absent_original_span_hash_fabricated": False, "source_location_sampling": False}


def validate_goal_finding(finding: dict, context: dict, rules: dict[str, dict],
                          node_ids: set[str], edge_ids: set[str]) -> tuple[int, dict]:
    if finding.get("type") != "static_goal_judgment" or finding.get("snapshot_id") != context["id"]:
        raise ValueError("Finding type/snapshot identity does not match the chosen saved snapshot")
    matching = [(index, evidence) for index, evidence in enumerate(finding.get("evidence", []))
                if evidence.get("kind") == "static_whole_judgment"]
    if len(matching) != 1:
        raise ValueError("Registered goal must have one original whole-judgment evidence record")
    index, evidence = matching[0]
    details = evidence.get("details", {})
    goal_id = details.get("goal_id")
    if goal_id not in DEFINITIONS or finding.get("rule_id") not in rules:
        raise ValueError("Goal finding has no matching captured configured goal")
    rule = rules[finding["rule_id"]]
    repository, adapter, required = DEFINITIONS[goal_id]
    if context["repository"] != repository or details.get("analyzer") != adapter or rule.get("goal_id") != goal_id or rule.get("analyzer") != adapter:
        raise ValueError(f"Actual goal/adapter/repository mapping mismatch: {goal_id}")
    if rule.get("contract", {}).get("id") != rule["id"]:
        raise ValueError("Registered rule/inner contract IDs differ")
    for key in ("source_hash", "policy_hash"):
        if details.get(key) != context[key]:
            raise ValueError("Registered goal source/policy identity differs from its snapshot")
    if details.get("snapshot_id") != context["id"] or details.get("contract_hash") != digest(rule):
        raise ValueError("Registered goal snapshot/contract identity differs from actual captured policy")
    registry = context["component_versions"].get("goal_contracts", {}).get("registry")
    if details.get("version") != registry:
        raise ValueError("Registered goal extractor version differs from recorded tool components")
    fingerprint = digest({"version": registry, "project": context["project_id"], "rule": rule})
    if finding.get("fingerprint") != fingerprint or finding.get("id") != digest({"snapshot": context["id"], "fingerprint": fingerprint})[:24]:
        raise ValueError("Original registered finding ID formula does not match stored content")
    if evidence.get("id") != digest({"snapshot": context["id"], "fingerprint": fingerprint, "details": details})[:24]:
        raise ValueError("Original registered evidence ID formula does not match stored content")
    if any(value not in node_ids for value in finding.get("node_ids", [])) or any(value not in edge_ids for value in finding.get("edge_ids", [])):
        raise ValueError("Finding references a node/edge outside its captured graph")
    obligations = details.get("obligations", [])
    if not isinstance(obligations, list) or len(obligations) != len(required) or set(item.get("id") for item in obligations) != set(required):
        raise ValueError(f"Original required obligation IDs not fully accounted: {goal_id}")
    if details.get("required_obligation_ids") != list(required):
        raise ValueError("Registry's required obligation list was altered")
    for record in obligations:
        if record.get("status") not in {"supported", "partial", "unknown", "refuted"}:
            raise ValueError("Adapter obligation status is not a saved explicit assessment")
    for key in ("necessary_gaps", "adapter_judgments"):
        if not isinstance(details.get(key), list):
            raise ValueError(f"Saved registered {key} missing")
    embedded_ids: dict[tuple[str, str], str] = {}
    for adapter_finding in details["adapter_judgments"]:
        if adapter_finding.get("snapshot_id") != context["id"] or adapter_finding.get("rule_id") != rule["id"]:
            raise ValueError("Embedded adapter finding is from a different snapshot/rule")
        for embedded in [adapter_finding, *adapter_finding.get("evidence", [])]:
            identity = embedded.get("id")
            if not isinstance(identity, str) or not identity:
                raise ValueError("Embedded finding/evidence ID missing")
            kind = "finding" if "fingerprint" in embedded else "evidence"
            key = kind, identity
            body = digest(embedded)
            if key in embedded_ids and embedded_ids[key] != body:
                raise ValueError("One embedded finding/evidence ID carries different stored content")
            embedded_ids[key] = body
    return index, details


def read_repository(path: Path, repository: str, requested_snapshot: str | None,
                    freeze: dict, frozen_policy: dict) -> dict:
    path = path.resolve(strict=True)
    wal = Path(str(path) + "-wal")
    if wal.exists() and wal.stat().st_size:
        raise ValueError("Formal database has an unclosed WAL; wait for publisher checkpoint/close: " + str(path))
    connection = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    try:
        connection.execute("PRAGMA query_only=ON")
        connection.execute("BEGIN")
        if requested_snapshot is None:
            rows = connection.execute("SELECT snapshot_id FROM project_latest").fetchall()
            if len(rows) != 1:
                raise ValueError("Choose --snapshot explicitly when DB has multiple latest projects")
            requested_snapshot = rows[0]["snapshot_id"]
        columns = ",".join(_METADATA_KEYS)
        row = connection.execute(f"SELECT {columns},stats_json,finding_count,json_extract(snapshot_json,'$.config') AS config_json,"
            "json_extract(snapshot_json,'$.parser_version') AS parser_version,json_extract(snapshot_json,'$.input_evidence') AS inputs_json,"
            "json_extract(snapshot_json,'$.id','$.project_id','$.project_name','$.root','$.source_hash','$.policy_hash',"
            "'$.analyzer_version','$.detector_version','$.schema_version','$.status') AS metadata_json FROM snapshots WHERE id=?",
            (requested_snapshot,)).fetchone()
        if row is None:
            raise ValueError("Requested original snapshot is missing")
        context = {key: row[key] for key in _METADATA_KEYS}
        if json.loads(row["metadata_json"]) != [context[key] for key in _METADATA_KEYS]:
            raise ValueError("Snapshot JSON/table original identities disagree")
        stats = json.loads(row["stats_json"], parse_constant=reject_constant)
        config = json.loads(row["config_json"], parse_constant=reject_constant)
        inputs = json.loads(row["inputs_json"] or "{}", parse_constant=reject_constant)
        context.update(repository=repository, component_versions=stats["component_versions"],
                       parser_version=row["parser_version"], database_path=str(path), database_sha256=file_hash(path))
        if context["component_versions"].get("tool") != freeze.get("tool_identity"):
            raise ValueError("Saved tool identity does not match the provided frozen tool")
        for key in ("analyzer_version", "detector_version", "schema_version"):
            if context[key] != freeze.get(key):
                raise ValueError(f"Saved {key} differs from frozen tool")
        if digest(config) != context["policy_hash"]:
            raise ValueError("Saved policy SHA does not match its original bytes/model")
        if config != frozen_policy["config"] or context["policy_hash"] != frozen_policy["canonical_policy_sha256"]:
            raise ValueError("Saved normalized policy differs from the frozen publication input")
        context["frozen_policy_input"] = {key: value for key, value in frozen_policy.items() if key != "config"}
        versions = json.dumps(context["component_versions"], ensure_ascii=True, sort_keys=True, separators=(",", ":"))
        if context["parser_version"] != versions:
            raise ValueError("Snapshot parser/component identity differs")
        expected_snapshot = digest({key: context[key] for key in
            ("project_id", "source_hash", "policy_hash", "analyzer_version", "detector_version", "schema_version", "parser_version")})
        if expected_snapshot != context["id"]:
            raise ValueError("Original snapshot ID formula differs from saved context")
        sources, file_records = {}, []
        for source_row in connection.execute("SELECT value FROM snapshots,json_each(snapshot_json,'$.files') WHERE snapshots.id=?", (requested_snapshot,)):
            record = json.loads(source_row["value"], parse_constant=reject_constant)
            if record["path"] in sources:
                raise ValueError("Source path is duplicated in the captured snapshot")
            sources[record["path"]] = record
            file_records.append([record["path"], record["hash"], record["status"], record["module"], record.get("error")])
        scope = {key: stats[key] for key in _SCOPE_KEYS}
        if digest({"files": file_records, "scope": scope, "support_inputs": inputs}) != context["source_hash"]:
            raise ValueError("Original source/scope/support-input aggregate SHA differs")
        for record in inputs.values():
            if record.get("status") == "captured":
                authenticate_source(record)
                if record.get("text_hash") != hashlib.sha256(record["content"].encode()).hexdigest():
                    raise ValueError("Original support-input text SHA differs")
                if record["path"] in sources and record["hash"] != sources[record["path"]]["hash"]:
                    raise ValueError("Support input and source path disagree")
                sources.setdefault(record["path"], record)
        node_ids = {item[0] for item in connection.execute("SELECT json_extract(value,'$.id') FROM snapshots,json_each(snapshot_json,'$.nodes') WHERE snapshots.id=?", (requested_snapshot,))}
        edge_ids = {item[0] for item in connection.execute("SELECT json_extract(value,'$.id') FROM snapshots,json_each(snapshot_json,'$.edges') WHERE snapshots.id=?", (requested_snapshot,))}
        count = connection.execute("SELECT count(*) FROM findings WHERE snapshot_id=?", (requested_snapshot,)).fetchone()[0]
        if count != row["finding_count"]:
            raise ValueError("Original saved finding count differs from published metadata")
        rules = {rule["id"]: rule for rule in config.get("goal_contracts", [])}
        if len(rules) != len(config.get("goal_contracts", [])):
            raise ValueError("Configured original goal rule IDs are duplicated")
        findings = []
        for finding_row in connection.execute("SELECT id,ordinal,finding_json FROM findings WHERE snapshot_id=? AND json_extract(finding_json,'$.type')='static_goal_judgment' ORDER BY ordinal", (requested_snapshot,)):
            finding = json.loads(finding_row["finding_json"], parse_constant=reject_constant)
            if finding_row["id"] != finding.get("id"):
                raise ValueError("Finding table/JSON ID differs")
            evidence_index, details = validate_goal_finding(finding, context, rules, node_ids, edge_ids)
            finding["_report_tracking"] = {"database_ordinal": finding_row["ordinal"],
                "original_finding_json_sha256": hashlib.sha256(finding_row["finding_json"].encode()).hexdigest(),
                "goal_evidence_index": evidence_index, "location_validation": validate_locations(finding, sources, requested_snapshot)}
            findings.append(finding)
        expected_goals = {goal for goal, (name, _, _) in DEFINITIONS.items() if name == repository}
        actual_goals = [finding["evidence"][finding["_report_tracking"]["goal_evidence_index"]]["details"]["goal_id"] for finding in findings]
        if len(actual_goals) != len(expected_goals) or set(actual_goals) != expected_goals:
            raise ValueError(f"Original {repository} goal findings are missing/duplicated or mapped to the wrong repository")
        manifest = [{"file": file, "source_hash": source["hash"], "status": source["status"],
            "text_utf8_sha256": hashlib.sha256(source["content"].encode()).hexdigest() if isinstance(source.get("content"), str) else None}
            for file, source in sorted(sources.items())]
        return {"context": context, "config": config, "source_manifest": manifest, "findings": findings,
                "all_finding_count": count, "captured_goal_finding_count": len(findings),
                "stored_original_graph_preserved": True, "graph_nodes_referenced": len(node_ids), "graph_edges_referenced": len(edge_ids)}
    finally:
        connection.close()


def reference(archive: dict, artifact_path: Path, artifact_sha: str, repository: str,
              finding_index: int, evidence_index: int, suffix: str, origin: str) -> dict:
    pointer = f"/repositories/{repository}/findings/{finding_index}/evidence/{evidence_index}/details{suffix}"
    value = at_pointer(archive, pointer)
    finding = archive["repositories"][repository]["findings"][finding_index]
    evidence = finding["evidence"][evidence_index]
    context = archive["repositories"][repository]["context"]
    return {"origin": origin, "artifact": os.path.relpath(artifact_path, HERE),
        "artifact_sha256": artifact_sha, "json_pointer": pointer, "target_value_sha256": digest(value),
        "snapshot_id": context["id"], "source_hash": context["source_hash"], "policy_hash": context["policy_hash"],
        "tool_identity": context["component_versions"]["tool"], "finding_id": finding["id"],
        "evidence_id": evidence["id"], "rule_id": finding["rule_id"],
        "contract_hash": evidence["details"]["contract_hash"], "canonical_hash_encoding": "json_sorted_ascii_compact_sha256"}


def compile_ledger(template: dict, original_inventory: dict, archive: dict,
                   archive_path: Path, archive_sha: str, freeze_path: Path) -> dict:
    ledger = deepcopy(template)
    ledger["kind"] = "saved_goal_implementation_tracking_ledger"
    ledger["benchmark_boundary"] = {"functional_benchmark": "the_two_original_complete_analysis_reports",
        "goal_ledger_role": "original_five_goals_thirty_relations_implementation_tracking",
        "adds_new_ratings_or_reviewer_approval": False, "does_not_replace_report_benchmark": True}
    ledger["acceptance_contract"]["path"] = "../astra-iteration4/GOAL_ACCEPTANCE.md"
    ledger["frozen_observations"]["path"] = "../astra-baseline/capability-baseline.json"
    for goal in ledger["goals"]:
        repository, adapter, required = DEFINITIONS[goal["id"]]
        records = archive["repositories"][repository]["findings"]
        selected = [(index, finding, finding["_report_tracking"]["goal_evidence_index"])
                    for index, finding in enumerate(records)
                    if finding["evidence"][finding["_report_tracking"]["goal_evidence_index"]]["details"]["goal_id"] == goal["id"]]
        if len(selected) != 1:
            raise ValueError("Goal evidence selection ceased to be unique")
        finding_index, finding, evidence_index = selected[0]
        details = finding["evidence"][evidence_index]["details"]
        ref = lambda suffix, origin: reference(archive, archive_path, archive_sha, repository, finding_index, evidence_index, suffix, origin)
        goal["registered_judgment"] = deepcopy(details)
        goal["witness"] = [ref("", "saved_automatic_registered_judgment")]
        goal["source"] = []
        goal["model"] = []
        goal["policy"] = [ref("/contract_hash", "policy-declared")]
        goal["gaps"] = deepcopy(details["necessary_gaps"])
        goal["conditions"] = deepcopy(details.get("conditions", []))
        goal["refutations"] = deepcopy(details.get("refutations", []))
        goal["adapter"] = adapter
        goal["assessment"] = {"status": details["assessment"],
            "complete_assessment": details["complete_assessment"], "full_goal_supported": details["full_goal_supported"],
            "origin": "copied_saved_registered_result_not_independently_rated",
            "unclosed_required_obligations": [goal["id"] + "." + item["id"] for item in details["obligations"] if item.get("status") not in {"supported", "refuted"}],
            "derived_judgment": deepcopy(details.get("derived_judgment"))}
        # Category references retain the adapter's original source/model/policy
        # containers. No list length or locator label is used as a pass signal.
        source_keys = {"source_facts", "source_trace", "source_relations", "source_evidence", "source", "relations"}
        model_keys = {"model_applications", "standard_models", "trusted_models", "model_applicability", "model", "models"}
        policy_keys = {"policy_declared", "provenance", "applicability", "policy"}
        for pointer, value in walk(details.get("adapter_judgments", []), "/adapter_judgments"):
            if not value or not pointer:
                continue
            key = pointer.rsplit("/", 1)[-1]
            # Generic source/model/policy keys describe a category only at an
            # actual saved adapter summary or obligation. Do not reclassify an
            # expression member named "source" or "model" as a trusted fact.
            parent = pointer.rsplit("/", 1)[0]
            category_boundary = parent.endswith("/details") or "/details/obligations/" in parent and parent.rsplit("/", 1)[-1].isdigit()
            if key in {"source", "relations", "model", "models", "policy"} and not category_boundary:
                continue
            if key in source_keys:
                goal["source"].append(ref(pointer, "source-derived"))
            elif key in model_keys:
                goal["model"].append(ref(pointer, "trusted-model"))
            elif key in policy_keys:
                goal["policy"].append(ref(pointer, "policy-declared"))
        by_id = {item["id"]: (index, item) for index, item in enumerate(details["obligations"])}
        for obligation, key in zip(goal["obligations"], required):
            index, item = by_id[key]
            obligation["recorded_result"] = deepcopy(item)
            obligation["witness"] = [ref(f"/obligations/{index}", "saved_automatic_obligation_result")]
            obligation["source"], obligation["model"], obligation["policy"] = [], [], []
            for field, keys, origin in (("source", source_keys, "source-derived"),
                                       ("model", model_keys, "trusted-model"),
                                       ("policy", policy_keys, "policy-declared")):
                obligation[field] = [ref(f"/obligations/{index}/{name}", origin)
                                     for name in sorted(keys) if item.get(name)]
            obligation["gaps"] = deepcopy(item.get("necessary_gaps", item.get("gaps", [])))
            obligation["assessment"] = {"status": item["status"],
                "origin": "copied_saved_adapter_result_not_independently_rated",
                "reason": deepcopy(item.get("assessment", item.get("reason")))}
    goal_counts = Counter(goal["assessment"]["status"] for goal in ledger["goals"])
    obligation_counts = Counter(item["assessment"]["status"] for goal in ledger["goals"] for item in goal["obligations"])
    ledger["assessment"] = {"goal_status_counts": dict(goal_counts), "obligation_status_counts": dict(obligation_counts),
        "status": "recorded_saved_implementation_results", "new_rating_computed": False,
        "unclosed_required_obligations": [item["id"] for goal in ledger["goals"] for item in goal["obligations"] if item["assessment"]["status"] not in {"supported", "refuted"}]}
    ledger["evaluation"] = {"method": "copy_and_authenticate_saved_static_goal_judgment_results",
        "original_files": original_inventory, "source_template": {"path": "../astra-iteration4/goal-ledger.template.json",
            "sha256": FROZEN_HASHES["astra-iteration4/goal-ledger.template.json"]},
        "snapshots": [value["context"] for value in archive["repositories"].values()],
        "freeze": {"path": os.path.relpath(freeze_path, HERE), "sha256": file_hash(freeze_path)},
        "artifact_inventory": [{"path": os.path.relpath(archive_path, HERE), "sha256": archive_sha}],
        "source_location_sampling": False, "original_claim_definitions_unchanged": True}
    ledger["report_builder"] = {"version": VERSION, "source_sha256": file_hash(Path(__file__)),
        "target_workspace_read": False, "target_code_imported_or_executed": False,
        "target_tests_run": False, "target_build_run": False, "tool_test_suite_run": False,
        "analyzer_invoked": False, "reviewer_approval_added": False}
    ledger["interpretation"] = "原五目标和30关系的真实保存结果索引；所有状态来自自动产物，源码/模型/政策/条件/反证和必要未知保留。全文报告仍是功能基准。"
    return ledger


def artifact_bytes(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()


def validate_output_path(path: Path) -> Path:
    path = path.resolve()
    if not path.is_relative_to(HERE) or path.suffix != ".json":
        raise ValueError("Write new JSON artifacts inside this iteration only")
    if path.exists():
        raise ValueError("Existing artifacts are never overwritten")
    return path


def write_new(path: Path, value: dict) -> str:
    path = validate_output_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = artifact_bytes(value)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".goal-tracking-", suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(raw)
        os.link(temporary, path)
    finally:
        if temporary:
            temporary.unlink(missing_ok=True)
    return hashlib.sha256(raw).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--formal-artifacts-closed", action="store_true",
                        help="Publisher has explicitly closed both formal scans and their databases")
    for repository in ("codepatchbay", "winwincode"):
        parser.add_argument("--" + repository + "-db", type=Path, default=HERE / (repository + "-v14.sqlite3"))
        parser.add_argument("--" + repository + "-snapshot")
    parser.add_argument("--freeze", type=Path, default=HERE / "CORE_FREEZE.json")
    parser.add_argument("--output", type=Path, default=HERE / "goal-ledger.json")
    parser.add_argument("--evidence-output", type=Path, default=HERE / "GOAL_JUDGMENT_EVIDENCE.json")
    args = parser.parse_args()
    if not args.formal_artifacts_closed:
        parser.error("Run only after the publisher explicitly closes both formal scans; pass --formal-artifacts-closed then")
    try:
        if args.output.resolve() == args.evidence_output.resolve() or args.output.exists() or args.evidence_output.exists():
            raise ValueError("Choose two different new outputs; existing artifacts are never overwritten")
        validate_output_path(args.output)
        validate_output_path(args.evidence_output)
        template, inventory = ensure_frozen_definitions()
        freeze, frozen_policies = authenticate_freeze(args.freeze, inventory)
        archive = {"schema_version": 1, "kind": "original_saved_registered_goal_judgments",
            "created_at": datetime.now(timezone.utc).isoformat(), "compiler_version": VERSION,
            "freeze": deepcopy(freeze), "repositories": {}, "analyzers_rerun": False,
            "original_reports_are_the_functional_benchmark": True}
        with source_read_lock():
            for repository in ("codepatchbay", "winwincode"):
                archive["repositories"][repository] = read_repository(getattr(args, repository + "_db"), repository,
                    getattr(args, repository + "_snapshot"), freeze, frozen_policies[repository])
        tools = [value["context"]["component_versions"]["tool"] for value in archive["repositories"].values()]
        if tools[0] != tools[1]:
            raise ValueError("The two registered result sets use different tool identities")
        evidence_sha = hashlib.sha256(artifact_bytes(archive)).hexdigest()
        ledger = compile_ledger(template, inventory, archive, args.evidence_output, evidence_sha, args.freeze)
        references = [item for _, item in walk(ledger) if isinstance(item, dict) and "json_pointer" in item and "artifact_sha256" in item]
        if any(item["target_value_sha256"] != digest(at_pointer(archive, item["json_pointer"])) for item in references):
            raise ValueError("Output witness pointer/hash does not match copied original evidence")
        # Finish validation before publishing either output. No result is
        # fabricated when a database, source identity or pointer is invalid.
        if write_new(args.evidence_output, archive) != evidence_sha:
            raise ValueError("Published evidence serialization differs from the validated archive")
        write_new(args.output, ledger)
    except (OSError, ValueError, KeyError, TypeError, sqlite3.Error, RecursionError) as error:
        parser.error(str(error))
    print(json.dumps({"output": str(args.output), "evidence_output": str(args.evidence_output),
        "goal_count": 5, "required_obligation_count": 30, "reference_count": len(references),
        "status_counts_copied_from_saved_results": ledger["assessment"], "new_rating_computed": False,
        "target_executed": False, "target_tests_run": False, "target_build_run": False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
