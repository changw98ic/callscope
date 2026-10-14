"""Compute one actual task rule from the saved snapshot and normal report API.

No target program, fixture or old whole-scope report analysis is executed.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import asdict
import fcntl
import hashlib
import json
from pathlib import Path
import sqlite3
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE.parent / "astra-iteration11"))
sys.path.insert(0, str(HERE.parent / "astra-iteration12"))
from render_report_summaries import _SavedJSON
from report_shared_references import validate_shared_references


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def inventory() -> dict:
    return {str(path.relative_to(ROOT / "callscope")): digest(path)
        for path in sorted((ROOT / "callscope").rglob("*.py"))}


def write_json(path: Path, value):
    with path.open("w") as stream:
        json.dump(value, stream, ensure_ascii=False, separators=(",", ":"))
        stream.write("\n")


def source_anchor_check(extraction: dict) -> dict:
    cached = {}
    failures = []
    for identity, location in extraction["source_location_index"].items():
        file = location["file"]
        if file not in cached:
            cached[file] = (ROOT.parent / "codepatchbay" / file).read_bytes()
        raw = cached[file]
        prefix = location.get("raw_prefix_bytes", 0)
        data = raw[prefix:]
        start, end = location["start_byte"], location["end_byte"]
        checks = {"raw_source_hash": hashlib.sha256(raw).hexdigest() == location["source_hash"],
            "span_hash": hashlib.sha256(data[start:end]).hexdigest() == location["span_hash"],
            "valid_span": 0 <= start <= end <= len(data),
            "byte_map": location.get("original_file_start_byte", start + prefix) == start + prefix
                and location.get("original_file_end_byte", end + prefix) == end + prefix}
        if not all(checks.values()):
            failures.append({"location_id": identity, "file": file, "checks": checks})
    return {"source_files": len(cached), "source_anchors": len(extraction["source_location_index"]),
        "failures": failures, "all_source_hashes_spans_and_byte_maps_match": not failures}


def main():
    rule_path = HERE / "cpb-task-read-projection-rule.json"
    rule = json.loads(rule_path.read_text())
    with (ROOT / ".analysis-tools/goal-source-query.lock").open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        from callscope.store import _snapshot_from_json
        from callscope.report_chain_analysis import analyze_report_claims, validate_report_claim
        from callscope.project_report import build_project_report, render_markdown
        from callscope.analysis_inputs import tool_identity
        validate_report_claim(rule)
        before = inventory()
        connection = sqlite3.connect("file:" + str(HERE.parent / "astra-iteration11/codepatchbay-v13.sqlite3")
            + "?mode=ro&immutable=1", uri=True)
        row = connection.execute("SELECT snapshot_json,detector_version,schema_version FROM snapshots ORDER BY sequence DESC LIMIT 1").fetchone()
        connection.close()
        snapshot = _snapshot_from_json(*row)
        del row
        print(json.dumps({"state": "captured_v13_source_loaded", "snapshot_id": snapshot.id}), flush=True)
        findings = analyze_report_claims(snapshot, [rule])
        print(json.dumps({"state": "actual_rule_finding_computed", "finding_count": len(findings),
            "assessment": findings[0].evidence[0].details.get("assessment")}), flush=True)
        report = build_project_report(snapshot, findings)
        write_json(HERE / "cpb-task-development-findings.json", [asdict(finding) for finding in findings])
        write_json(HERE / "cpb-task-development-report.json", report)
        (HERE / "cpb-task-development-report.md").write_text(render_markdown(report))
        extraction = report["architecture"]["responsibility_explanations"]
        current_ids = {operation["id"] for operation in extraction["operations"]}
        previous_path = HERE.parent / "astra-iteration12/responsibility-operations-codepatchbay-development.json"
        previous, previous_hash = _SavedJSON(previous_path).load({"saved_snapshot_id": True,
            "current_module_sha256": True, "extraction": {"operations": [{"id": True}]}})
        if previous["saved_snapshot_id"] != snapshot.id or previous["current_module_sha256"] != before["responsibility_operations.py"]:
            raise ValueError("previous operation count is not comparable to this actual snapshot/module")
        previous_ids = {operation["id"] for operation in previous["extraction"]["operations"]}
        after = inventory()
        shared = validate_shared_references(report)
        anchors = source_anchor_check(extraction)
        checks = {"development_query": True, "not_formal_scope2_result": True,
            "source": {"snapshot_id": snapshot.id, "source_hash": snapshot.source_hash,
                "saved_policy_hash": snapshot.policy_hash, "rule_sha256": digest(rule_path),
                "rule_not_saved_snapshot_policy": True, "current_tool_identity": tool_identity()},
            "normal_analyze_report_claims_called": True, "actual_finding_ids": [finding.id for finding in findings],
            "new_findings_fabricated": False, "fixture_used": False,
            "normal_build_project_report_called": True, "normal_render_markdown_called": True,
            "functional_chains": [{"rule_id": chain["rule_id"], "assessment": chain["assessment"],
                "analysis_gaps": chain["analysis_gaps"], "source_fact_count": len(chain["source_facts"])}
                for chain in report["functional_chains"]],
            "responsibility_operations": {"count": len(current_ids),
                "kind_counts": dict(sorted(Counter(operation["operation_kind"] for operation in extraction["operations"]).items())),
                "owner_count": len(extraction["declaration_explanations"]),
                "analysis_gaps": extraction["analysis_gaps"], "explanation_source_gaps": extraction["explanation_source_gaps"],
                "budget": extraction["operation_extraction_budget"]},
            "operation_id_union": {"previous_actual_artifact": str(previous_path.relative_to(ROOT)),
                "previous_artifact_sha256": previous_hash, "previous_count": len(previous_ids),
                "task_count": len(current_ids), "overlap_count": len(current_ids & previous_ids),
                "additional_count": len(current_ids - previous_ids), "union_count": len(current_ids | previous_ids),
                "operation_limit": extraction["operation_extraction_budget"]["limits"]["operations"],
                "within_operation_limit": len(current_ids | previous_ids) <= extraction["operation_extraction_budget"]["limits"]["operations"],
                "union_is_id_accounting_not_a_new_full_scope_analysis": True},
            "shared_reference_check": shared, "source_anchor_check": anchors,
            "core_module_bytes_stable": before == after,
            "changed_core_modules": [name for name in sorted(before.keys() | after.keys()) if before.get(name) != after.get(name)],
            "artifacts": {name: {"sha256": digest(HERE / name), "bytes": (HERE / name).stat().st_size}
                for name in ["cpb-task-development-findings.json", "cpb-task-development-report.json", "cpb-task-development-report.md"]},
            "target_executed": False, "target_imported": False, "target_tests_run": False, "target_build_run": False}
        write_json(HERE / "cpb-task-DEVELOPMENT-READBACK.json", checks)
        print(json.dumps(checks, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
