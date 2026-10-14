"""Compare v10 saved snapshots against frozen v9 baseline evaluation artifacts.

The original 26-observation baseline and the unchanged 1.3 evaluator are used.
Old stores are never opened: their published evaluation JSON is preserved.
"""
import argparse
import hashlib
import json
from pathlib import Path
from callscope.baseline import evaluate_baseline, load_baseline
from callscope.store import Store
from callscope.models import project_id_for
from publication_identity import check_identity, check_snapshot, write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", choices=("codepatchbay", "winwincode"))
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    check_identity(directory)
    baseline = load_baseline(directory.parent / "astra-baseline" / "capability-baseline.json")
    with Store(directory / f"{args.repository}-v10.sqlite3") as store:
        snapshot = store.latest(project_id_for(directory.parents[2] / args.repository))
    if snapshot is None:
        raise RuntimeError("No v10 published snapshot")
    check_snapshot(directory, snapshot)
    current = evaluate_baseline(snapshot, baseline, args.repository)
    previous_path = directory.parent / "astra-iteration6" / f"{args.repository}-baseline-v9-and-v8.json"
    previous = json.loads(previous_path.read_text())["current"]
    for key in ("baseline_id", "baseline_total", "evaluator_version", "evaluator_source_hash"):
        if current[key] != previous[key]:
            raise RuntimeError(f"Baseline comparison changed frozen {key}")
    if current["evaluator_version"] != "frozen-static-baseline-1.3" or current["baseline_total"] != 26:
        raise RuntimeError("Baseline evaluator or observation count changed")
    if current["snapshot"]["source_hash"] != previous["snapshot"]["source_hash"]:
        raise RuntimeError("Target source identity changed since v9")
    before = {item["id"]: item for item in previous["observations"]}
    changes = [{"id": item["id"], "before": before[item["id"]]["status"], "after": item["status"],
                "before_expectation_satisfied": before[item["id"]].get("expectation_satisfied"),
                "after_expectation_satisfied": item.get("expectation_satisfied")}
               for item in current["observations"]
               if item["status"] != before[item["id"]]["status"] or
               item.get("expectation_satisfied") != before[item["id"]].get("expectation_satisfied")]
    result = {"current": current, "previous": previous, "changes": changes,
              "previous_result_origin": str(previous_path.relative_to(directory.parent)),
              "previous_artifact_sha256": hashlib.sha256(previous_path.read_bytes()).hexdigest(),
              "previous_store_opened": False,
              "interpretation": "Frozen source-observation reproduction only; not precision, recall, business pass rate, or goal acceptance.",
              "target_executed": False, "target_tests_run": False, "tool_test_suite_run": False}
    write_json(directory / f"{args.repository}-baseline-v10-and-v9.json", result)
    print(json.dumps({"repository": args.repository, "counts": current["counts"], "changes": changes}))


if __name__ == "__main__":
    main()
