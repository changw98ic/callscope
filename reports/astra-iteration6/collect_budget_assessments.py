"""Export configured local-budget evidence from saved formal static snapshots.

No target is imported, executed, built or tested. Local source assessments do
not decide which budget consumes an upstream parameter or full goal acceptance.
"""
import json
from pathlib import Path


def main():
    directory = Path(__file__).resolve().parent
    repositories = []
    for name in ("codepatchbay", "winwincode"):
        summary = json.loads((directory / f"{name}-summary.json").read_text())
        selected = [finding for finding in summary["rule_findings"]
                    if finding["type"] == "static_local_budget"]
        repositories.append({
            "repository": name, "snapshot_id": summary["id"],
            "source_hash": summary["source_hash"], "policy_hash": summary["policy_hash"],
            "component_versions": summary["stats"]["component_versions"],
            "configured_budget_contracts_count": summary["stats"]["budget_contracts_count"],
            "assessment_findings_count": len(selected), "assessments": selected,
            "meaning": "Captured lexical budget source operations only; activation, runtime values and upstream parameter consumption are separate.",
        })
    artifact = {"kind": "published_static_local_budget_assessments", "repositories": repositories,
                "target_executed": False, "target_tests_run": False, "target_build_run": False,
                "full_goal_acceptance_computed": False}
    (directory / "budget-assessments.json").write_text(
        json.dumps(artifact, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"configured": sum(item["configured_budget_contracts_count"] for item in repositories),
                      "assessment_findings": sum(item["assessment_findings_count"] for item in repositories)}))


if __name__ == "__main__":
    main()
