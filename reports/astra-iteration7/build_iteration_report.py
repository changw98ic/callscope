"""Build compact v8/v9/v10 identity and field comparisons from saved artifacts.

This only reads report artifacts, never target code. Observation counts and
selected field assessments do not compute precision or full goal acceptance.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path


def load(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact_fields(summary):
    result = []
    for finding in summary["rule_findings"]:
        if finding["type"] != "static_parameter_field_flow":
            continue
        details = next((item["details"] for item in finding["evidence"]
                        if "assessments" in item.get("details", {})), {})
        result.append({"rule_id": finding["rule_id"], "status": finding["status"],
                       "metadata": finding["metadata"],
                       "summary_budget": details.get("summary_budget"),
                       "assessment_counts": details.get("assessment_counts"),
                       "sites": [{"location": {key: site.get("site_location", {}).get(key)
                                                for key in ("file", "line", "column")},
                                  **{key: site.get(key) for key in
                                     ("field_presence", "selected_field_shape_closed", "whole_object_shape_closed",
                                      "source_form_relation", "pre_completion_source_form_relation", "gaps")}}
                                 for site in details.get("assessments", [])],
                       "helper_returns": [{"location": {key: fact.get("location", {}).get(key)
                                                        for key in ("file", "line", "column")},
                                           **{key: fact.get(key) for key in
                                              ("target_graph_node_id", "selected_field_presence",
                                               "selected_field_shape_closed", "whole_object_shape_closed")}}
                                          for fact in details.get("source_facts", [])
                                          if fact.get("operation") == "actual_helper_selected_return_summary"]})
    return result


def main():
    directory = Path(__file__).resolve().parent
    baseline_path = directory.parent / "astra-baseline" / "capability-baseline.json"
    baseline = load(baseline_path)
    template_path = directory.parent / "astra-iteration4" / "goal-ledger.template.json"
    goal_template = load(template_path)
    acceptance_path = directory.parent / "astra-iteration4" / "GOAL_ACCEPTANCE.md"
    if goal_template["goal_count"] != 5 or goal_template["required_obligation_count"] != 30:
        raise RuntimeError("Original five-goal/30-obligation acceptance contract changed")
    counts = Counter()
    repositories, contracts, comparison_rows = [], [], []
    for name in ("codepatchbay", "winwincode"):
        summary = load(directory / f"{name}-summary.json")
        integration = load(directory / f"{name}-integration.json")
        comparison = load(directory / f"{name}-baseline-v10-and-v9.json")
        current = comparison["current"]
        counts.update(current["counts"])
        positives = [item for item in current["observations"]
                     if item["expected_static_outcome"] in ("confirmed_static_call", "confirmed_static_path")]
        versions = []
        policies = []
        for version, dirname in (("v8", "astra-iteration5"), ("v9", "astra-iteration6"),
                                 ("v10", directory.name)):
            artifacts = directory.parent / dirname
            saved = load(artifacts / f"{name}-summary.json")
            policy_path = artifacts / f"{name}-policy.json"
            policy = load(policy_path)
            policies.append(policy)
            versions.append({"version": version, "snapshot_id": saved["id"],
                             "source_hash": saved["source_hash"], "policy_hash": saved["policy_hash"],
                             "policy_bytes_sha256": digest(policy_path),
                             "component_versions": saved["stats"]["component_versions"],
                             "field_assessments": compact_fields(saved)})
        same_source = len({item["source_hash"] for item in versions}) == 1
        same_v9_v10_policy = versions[1]["policy_bytes_sha256"] == versions[2]["policy_bytes_sha256"]
        same_v9_v10_policy_hash = versions[1]["policy_hash"] == versions[2]["policy_hash"]
        if not same_source or not same_v9_v10_policy or not same_v9_v10_policy_hash:
            raise RuntimeError(f"{name}: frozen target source or v9-v10 policy identity changed")
        comparison_rows.append({"repository": name, "versions": versions,
                                "target_source_identical_all_three": same_source,
                                "v9_v10_policy_bytes_identical": same_v9_v10_policy,
                                "v9_v10_policy_hash_identical": same_v9_v10_policy_hash,
                                "v8_v9_policy_bytes_identical": versions[0]["policy_bytes_sha256"] == versions[1]["policy_bytes_sha256"],
                                "v8_v9_field_contracts_identical": policies[0].get("field_contracts", []) == policies[1].get("field_contracts", []),
                                "changed_policy_sections_v8_v9": sorted(key for key in policies[0].keys() | policies[1].keys()
                                                                         if policies[0].get(key) != policies[1].get(key))})
        repositories.append({"repository": name, "snapshot_id": summary["id"], "status": summary["status"],
                             "source_hash": summary["source_hash"], "policy_hash": summary["policy_hash"],
                             "component_versions": summary["stats"]["component_versions"],
                             "files_total": summary["stats"]["files_total"],
                             "files_parsed": summary["stats"]["files_parsed"],
                             "files_failed": summary["stats"]["files_failed"],
                             "calls_by_resolution": summary["calls_by_resolution"],
                             "cold_and_warm": [{key: scan[key] for key in ("phase", "snapshot_id", "created", "maintenance")}
                                               for scan in integration["scans"]],
                             "frozen_positive_total": len(positives),
                             "frozen_positive_reproduced": sum(item["status"] == "reproduced" for item in positives),
                             "baseline_counts": current["counts"], "changes_since_v9": comparison["changes"],
                             "source_checks": current["source_checks"]})
        contracts.extend({"repository": name, "finding": item,
                          "interpretation": "Configured finite static source/model relations; full goal acceptance remains separate"}
                         for item in summary["rule_findings"] if item["type"].startswith("static_"))
    ledger = {"schema_version": 1, "baseline_id": baseline["baseline_id"], "baseline_status": baseline["status"],
              "baseline_sha256": digest(baseline_path), "baseline_total": len(baseline["observations"]),
              "status_counts": dict(counts), "repositories": repositories,
              "configured_finite_contract_findings_count": len(contracts),
              "original_goal_acceptance": {"path": "../astra-iteration4/GOAL_ACCEPTANCE.md",
                                           "sha256": digest(acceptance_path), "goal_count": 5,
                                           "required_obligation_count": 30,
                                           "template_path": "../astra-iteration4/goal-ledger.template.json",
                                           "template_sha256": digest(template_path)},
              "full_goal_acceptance_computed": False, "precision_metric_computed": False,
              "target_executed": False, "target_imported": False,
              "target_tests_run": False, "target_build_run": False, "tool_test_suite_run": False,
              "interpretation": "Frozen observation reproduction and selected field relations; no precision, recall, project coverage, or full-goal pass rate inferred"}
    outputs = (("capability-ledger.json", ledger), ("finite-contract-witnesses.json", contracts),
               ("FIELD_VERSION_COMPARISON.json", {"repositories": comparison_rows,
                                                   "precision_metric_computed": False,
                                                   "full_goal_acceptance_computed": False}))
    for filename, value in outputs:
        (directory / filename).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"baseline_total": ledger["baseline_total"], "status_counts": ledger["status_counts"],
                      "configured_finite_contract_findings_count": len(contracts)}))


if __name__ == "__main__":
    main()
