"""Compose the current explanation module from an actual saved extraction.

The full saved snapshot is read once under the common source-query lock.
No target code is imported or executed and the extraction is not recomputed.
"""
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
    args = parser.parse_args()
    with (ROOT / ".analysis-tools/goal-source-query.lock").open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        from callscope.store import _snapshot_from_json
        database = HERE.parent / "astra-iteration11" / f"{args.repository}-v13.sqlite3"
        connection = sqlite3.connect("file:" + str(database) + "?mode=ro&immutable=1", uri=True)
        row = connection.execute("SELECT snapshot_json,detector_version,schema_version FROM snapshots ORDER BY sequence DESC LIMIT 1").fetchone()
        connection.close()
        snapshot = _snapshot_from_json(*row)
        del row
        extraction_path = HERE / f"responsibility-operations-{args.repository}-development.json"
        extraction_bytes = extraction_path.read_bytes()
        extraction_document = json.loads(extraction_bytes)
        extraction_hash = hashlib.sha256(extraction_bytes).hexdigest()
        del extraction_bytes
        extraction = extraction_document.pop("extraction")
        source_module = ROOT / "callscope/responsibility_operations.py"
        if extraction_document["current_module_sha256"] != hashlib.sha256(source_module.read_bytes()).hexdigest():
            raise ValueError("saved extraction is not the current extractor module")
        if not extraction_document["query_module_bytes_stable"]:
            raise ValueError("source extraction module was not stable")
        selection = {"snapshot": True, "judgments": [{"goal_id": True, "finding_id": True,
            "evidence_id": True, "saved_evidence_pointer": True,
            "obligations": [{"id": True, "status": True, "necessary_gaps": True,
                "evidence": _OptionalProjection({"production_assembly": True, "channels": True})}]}]}
        report, report_hash = _SavedJSON(HERE.parent / "astra-iteration11" / f"{args.repository}-automatic-report.json").load(selection)
        if report_hash != extraction_document["saved_report_sha256"]:
            raise ValueError("saved report changed after extraction")
        module = ROOT / "callscope/architecture_responsibilities.py"
        before = hashlib.sha256(module.read_bytes()).hexdigest()
        from callscope.architecture_responsibilities import _explain_operations
        explanations = _explain_operations(snapshot, report, extraction)
        stable = before == hashlib.sha256(module.read_bytes()).hexdigest()
        document = {**extraction_document, "explanation_module_sha256": before,
            "explanation_module_bytes_stable": stable,
            "source_extraction_reused_without_cst_recomputation": True,
            "source_extraction_artifact_sha256": extraction_hash,
            "explanations": explanations}
        output = HERE / f"responsibility-explanations-{args.repository}-development.json"
        output.write_text(json.dumps(document, ensure_ascii=False, separators=(",", ":")) + "\n")
        print(json.dumps({"repository": args.repository, "snapshot_id": snapshot.id,
            "operations": len(extraction["operations"]), "explanation_module_sha256": before,
            "explanation_module_bytes_stable": stable,
            "computed_source_contract_seams": len(explanations.get("computed_source_contract_seams", [])),
            "analysis_gaps": explanations.get("analysis_gaps", []),
            "target_executed": False, "target_imported": False,
            "target_tests_run": False, "target_build_run": False}, ensure_ascii=False), flush=True)
        if not stable:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
