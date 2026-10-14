"""Normal current-tool field queries over immutable previous captured sources.

This is an unpublished development observation, not tests or acceptance. The
target repositories are never imported, executed, built or read by this query.
"""
import argparse
import json
from pathlib import Path
import sqlite3

from callscope.analysis_inputs import tool_identity
from callscope.field_summaries import summarize_field
from callscope.store import _snapshot_from_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rule")
    args = parser.parse_args()
    query_identity = tool_identity()
    directory = Path(__file__).resolve().parent
    previous = directory.parent / "astra-iteration8"
    connection = sqlite3.connect("file:" + str(previous / "codepatchbay-v10.sqlite3") + "?mode=ro&immutable=1", uri=True)
    row = connection.execute("SELECT snapshot_json,detector_version,schema_version FROM snapshots ORDER BY sequence DESC LIMIT 1").fetchone()
    connection.close()
    snapshot = _snapshot_from_json(*row)
    rules = json.loads((previous / "codepatchbay-policy.json").read_text())["field_contracts"]
    results = []
    for rule in rules:
        if args.rule and rule["id"] != args.rule:
            continue
        subject = rule["subject"]
        summary = summarize_field(snapshot,{"file":subject["file"],"symbol":subject["symbol"]},
            parameter_index=subject["parameter_index"],field_path=subject["field_path"],sink=rule["sink"],models=rule["models"])
        results.append({"rule_id":rule["id"],"summary":summary})
        print(json.dumps({"rule_id":rule["id"],"source_complete":summary["source_complete"],
            "sites":[{"line":site["site_location"]["line"],"source_form":site["source_form_relation"],
                "local_copy_supported":site["local_copy_retention_supported"],
                "copy_gaps":[item["witness"]["gaps"] for item in site["local_copy_retention"]],
                "relation_count":len(site["source_relations"]["relations"]),
                "syntax_gaps":site["source_relations"]["analysis_gaps"]} for site in summary["assessments"]]},ensure_ascii=False),flush=True)
    output = {"published":False,"kind":"current_tool_queries_over_previous_captured_sources",
        "captured_snapshot_id":snapshot.id,"captured_tool_identity":snapshot.stats["component_versions"]["tool"],
        "query_tool_identity":query_identity,"query_tool_identity_after":tool_identity(),
        "query_core_bytes_stable":query_identity==tool_identity(),"source_hash":snapshot.source_hash,"results":results,
        "target_executed":False,"target_tests_run":False,"target_build_run":False,"tool_test_suite_run":False,
        "full_goal_acceptance_computed":False}
    filename = "PREFREEZE_ENGINE_OBSERVATIONS.json" if args.rule else "PREFREEZE_FIELD_OBSERVATIONS.json"
    (directory / filename).write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n")


if __name__ == "__main__":
    main()
