"""Summarize published static artifacts without reading or running target code."""

from collections import Counter
import hashlib
import json
from pathlib import Path


def main():
    directory = Path(__file__).resolve().parent
    baseline_path = directory.parent / "astra-baseline" / "capability-baseline.json"
    baseline_bytes = baseline_path.read_bytes()
    baseline = json.loads(baseline_bytes)
    repositories = []
    contracts = []
    counts = Counter()
    for name in ("codepatchbay", "winwincode"):
        summary = json.loads((directory / f"{name}-summary.json").read_text())
        integration = json.loads((directory / f"{name}-integration.json").read_text())
        comparison = json.loads((directory / f"{name}-baseline-v6-and-v5.json").read_text())
        current = comparison["current"]
        counts.update(current["counts"])
        stats = summary["stats"]
        positives = [observation for observation in current["observations"]
                     if observation["expected_static_outcome"] in
                     ("confirmed_static_call", "confirmed_static_path")]
        repositories.append({
            "repository": name,
            "commit": current["repository"]["commit"],
            "snapshot_id": summary["id"], "snapshot_status": summary["status"],
            "source_hash": summary["source_hash"], "policy_hash": summary["policy_hash"],
            "component_versions": stats["component_versions"],
            "files_total": stats["files_total"], "files_parsed": stats["files_parsed"],
            "files_failed": stats["files_failed"], "nodes": stats["nodes"], "edges": stats["edges"],
            "calls_by_resolution": summary["calls_by_resolution"],
            "support_inputs_count": stats["support_inputs_count"],
            "support_inputs_incomplete": stats["support_inputs_incomplete"],
            "static_contracts_count": stats["static_contracts_count"],
            "value_contracts_count": stats["value_contracts_count"],
            "cold_and_warm": [{key: scan[key] for key in ("phase", "snapshot_id", "created", "maintenance")}
                              for scan in integration["scans"]],
            "frozen_positive_total": len(positives),
            "frozen_positive_reproduced": sum(observation["status"] == "reproduced"
                                                for observation in positives),
            "baseline_counts": current["counts"],
            "source_checks": current["source_checks"],
            "changes_since_v5": comparison["changes"],
            "observations": [{key: observation[key] for key in
                              ("id", "status", "expected_static_outcome", "expectation_satisfied")}
                             for observation in current["observations"]],
        })
        for finding in summary["rule_findings"]:
            if finding["type"].startswith(("static_contract_", "static_value_")):
                contracts.append({"repository": name, "finding": finding,
                    "interpretation": "configured finite source-fact review; not autonomous business-defect proof"})
    ledger = {
        "schema_version": 1,
        "baseline_id": baseline["baseline_id"], "baseline_status": baseline["status"],
        "baseline_sha256": hashlib.sha256(baseline_bytes).hexdigest(),
        "baseline_total": len(baseline["observations"]),
        "status_counts": dict(counts), "repositories": repositories,
        "configured_finite_contract_findings_count": len(contracts),
        "target_executed": False, "target_imported": False,
        "target_tests_run": False, "target_build_run": False,
        "interpretation": "Frozen source-observation reproduction and separately configured source facts; not functional coverage",
    }
    for filename, data in (("capability-ledger.json", ledger),
                           ("finite-contract-witnesses.json", contracts)):
        (directory / filename).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"baseline_total": ledger["baseline_total"], "status_counts": ledger["status_counts"],
                      "configured_finite_contract_findings_count": len(contracts)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
