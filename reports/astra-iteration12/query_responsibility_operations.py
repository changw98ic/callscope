"""Query actual saved v13 sources for the new finite responsibility extractor."""
from __future__ import annotations
import argparse
import fcntl
import hashlib
import json
from pathlib import Path
import sqlite3
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE.parent / "astra-iteration11"))
from render_report_summaries import _SavedJSON, _OptionalProjection


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", choices=["codepatchbay", "winwincode"])
    parser.add_argument("--supplemental-policy", type=Path)
    args = parser.parse_args()
    with (ROOT / ".analysis-tools/goal-source-query.lock").open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        from callscope.store import _snapshot_from_json
        module = ROOT / "callscope/responsibility_operations.py"
        before = hashlib.sha256(module.read_bytes()).hexdigest()
        from callscope.responsibility_operations import extract_responsibility_operations, _selector_records
        database = HERE.parent / "astra-iteration11" / (args.repository + "-v13.sqlite3")
        connection = sqlite3.connect("file:" + str(database) + "?mode=ro&immutable=1", uri=True)
        row = connection.execute("SELECT snapshot_json,detector_version,schema_version FROM snapshots ORDER BY sequence DESC LIMIT 1").fetchone()
        connection.close()
        snapshot = _snapshot_from_json(*row)
        del row
        selection = {"snapshot": True,
            "functional_chains": [{"rule_id": True, "finding_id": True, "evidence_id": True,
                "source_scope": True, "source_facts": [{"id": True, "kind": True, "origin": True, "location": True}]}],
            "judgments": [{"goal_id": True, "finding_id": True, "evidence_id": True, "saved_evidence_pointer": True,
                "obligations": [{"id": True, "status": True, "necessary_gaps": True,
                    "evidence": _OptionalProjection({"production_assembly": True, "channels": True})}]}]}
        report_path = HERE.parent / "astra-iteration11" / (args.repository + "-automatic-report.json")
        report, report_hash = _SavedJSON(report_path).load(selection)
        print("captured_sources_loaded", args.repository, snapshot.id, flush=True)
        supplemental = []
        policy_hash = None
        if args.supplemental_policy:
            policy_raw = args.supplemental_policy.read_bytes()
            policy_hash = hashlib.sha256(policy_raw).hexdigest()
            proposed = json.loads(policy_raw)
            old = {(selector["file"], selector["symbol"]) for selector, _ in _selector_records(snapshot.config, "")}
            for selector, pointer in _selector_records(proposed.get("report_claims", []), "/report_claims"):
                if (selector["file"], selector["symbol"]) in old:
                    continue
                parts = pointer.split("/")
                rule = proposed["report_claims"][int(parts[2])]
                supplemental.append({"selector": selector, "context": {"rule_id": rule.get("id"),
                    "selection_artifact_path": str(args.supplemental_policy), "selection_artifact_sha256": policy_hash,
                    "selection_artifact_pointer": pointer, "not_saved_snapshot_policy": True}})
        extraction = extract_responsibility_operations(snapshot, report, supplemental_selectors=supplemental)
        after = hashlib.sha256(module.read_bytes()).hexdigest()
        metadata = {"development_query": True, "not_formal_v14_result": True,
            "saved_snapshot_id": snapshot.id, "saved_source_hash": snapshot.source_hash,
            "saved_policy_hash": snapshot.policy_hash, "saved_report_sha256": report_hash,
            "report_projection_only_omits_unused_fields": True,
            "supplemental_development_policy_sha256": policy_hash,
            "supplemental_development_selector_count": len(supplemental),
            "current_module_sha256": before, "query_module_bytes_stable": before == after,
            "target_executed": False, "target_imported": False, "target_tests_run": False, "target_build_run": False}
        output = {**metadata, "extraction": extraction}
        path = HERE / ("responsibility-operations-" + args.repository + "-development.json")
        path.write_text(json.dumps(output, ensure_ascii=False, separators=(",", ":")) + "\n")
        samples = {}
        for operation in extraction["operations"]:
            if len(samples.setdefault(operation["operation_kind"], [])) < 2:
                samples[operation["operation_kind"]].append(operation)
        (HERE / ("responsibility-operation-samples-" + args.repository + ".json")).write_text(json.dumps({**metadata, "samples": samples}, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps({"repository": args.repository, "operations": len(extraction["operations"]),
            "kinds": extraction["operation_kind_counts"], "scope": extraction["scope"]["selected_declaration_count"],
            "budget": extraction["budget"], "gaps": extraction["analysis_gaps"], "stable": before == after}, ensure_ascii=False), flush=True)
        explanation_module = ROOT / "callscope/architecture_responsibilities.py"
        explanation_before = hashlib.sha256(explanation_module.read_bytes()).hexdigest()
        from callscope.architecture_responsibilities import _explain_operations
        explanations = _explain_operations(snapshot, report, extraction)
        explanation_stable = explanation_before == hashlib.sha256(explanation_module.read_bytes()).hexdigest()
        (HERE / ("responsibility-explanations-" + args.repository + "-development.json")).write_text(json.dumps({**metadata,
            "explanation_module_sha256": explanation_before, "explanation_module_bytes_stable": explanation_stable,
            "explanations": explanations}, ensure_ascii=False, separators=(",", ":")) + "\n")
        print("explanations_saved", args.repository, flush=True)


if __name__ == "__main__":
    main()
