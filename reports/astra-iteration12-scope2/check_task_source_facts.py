"""Authenticate real task report source-fact anchors without a database read."""
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def main():
    path = HERE / "cpb-task-development-report.json"
    raw_report = path.read_bytes()
    report = json.loads(raw_report)
    files = {}
    failures = []
    facts = []
    for chain_index, chain in enumerate(report["functional_chains"]):
        for fact_index, fact in enumerate(chain["source_facts"]):
            location = fact.get("location", {})
            file = location.get("file")
            if file not in files:
                files[file] = (ROOT.parent / "codepatchbay" / file).read_bytes()
            original = files[file]
            prefix = location.get("raw_prefix_bytes", 0)
            data = original[prefix:]
            start, end = location["start_byte"], location["end_byte"]
            checks = {"source_hash": hashlib.sha256(original).hexdigest() == location["source_hash"],
                "span_hash": hashlib.sha256(data[start:end]).hexdigest() == location["span_hash"],
                "valid_span": 0 <= start <= end <= len(data),
                "byte_map": location.get("original_file_start_byte", start + prefix) == start + prefix
                    and location.get("original_file_end_byte", end + prefix) == end + prefix,
                "coordinate_space": location.get("coordinate_space") == "captured_text_utf8"}
            pointer = f"/functional_chains/{chain_index}/source_facts/{fact_index}"
            facts.append({"id": fact["id"], "kind": fact["kind"], "source_pointer": pointer,
                "file": file, "line": location.get("line"), "checks": checks})
            if not all(checks.values()):
                failures.append({"id": fact["id"], "source_pointer": pointer, "checks": checks})
    output = {"development_only": True, "normal_report_sha256": hashlib.sha256(raw_report).hexdigest(),
        "actual_snapshot_identity": report["snapshot"], "facts_checked": len(facts), "source_files": len(files),
        "facts": facts, "failures": failures, "all_fact_anchors_match": not failures,
        "database_opened": False, "analysis_recomputed": False,
        "target_executed": False, "target_imported": False, "target_tests_run": False, "target_build_run": False}
    (HERE / "cpb-task-SOURCE_FACT_READBACK.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"facts_checked": len(facts), "source_files": len(files),
        "all_fact_anchors_match": not failures, "failures": failures}))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
