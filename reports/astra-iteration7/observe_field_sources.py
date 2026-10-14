"""Normal selected-field queries over an existing captured source snapshot.

No target code or test suite is imported or executed. Development output is
not a new publication; the captured-source identity and current query identity
are recorded separately.
"""
import argparse
import json
from pathlib import Path
from callscope.store import Store
from callscope.models import project_id_for
from callscope.field_summaries import summarize_field, VERSION
from callscope.analysis_inputs import tool_identity


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("label")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    old = directory.parent / "astra-iteration6"
    policy = json.loads((old / "codepatchbay-policy.json").read_text())
    store = Store(old / "codepatchbay-v9.sqlite3")
    try:
        snapshot = store.latest(project_id_for(directory.parents[2] / "codepatchbay"))
        rows = []
        for rule in policy["field_contracts"][:None if args.all else 1]:
            subject = rule["subject"]
            summary = summarize_field(snapshot, {"file": subject["file"], "symbol": subject["symbol"]},
                parameter_index=subject["parameter_index"], field_path=subject["field_path"],
                sink=rule["sink"], models=rule["models"])
            compact = {"id": rule["id"], "selected_shape_complete": summary["selected_shape_complete"],
                "source_form_complete": summary["source_form_complete"], "budget": summary["summary_budget"],
                "assessments": [{key: site.get(key) for key in ("site_location", "field_presence",
                    "selected_field_shape_closed", "whole_object_shape_closed", "source_form_relation",
                    "pre_completion_source_form_relation", "gaps", "effect_barrier_count")}
                    for site in summary["assessments"]],
                "helpers": [fact for fact in summary["source_facts"] if fact["operation"] == "actual_helper_selected_return_summary"],
                "literal_shapes": [fact for fact in summary["source_facts"] if fact["operation"] == "new_literal_object_shape"],
                "analysis_gaps": summary["analysis_gaps"]}
            rows.append({"rule": rule["id"], "summary": summary, "compact": compact})
            print(json.dumps({"id": rule["id"], "selected_shape_complete": summary["selected_shape_complete"],
                "source_form_complete": summary["source_form_complete"], "budget": summary["summary_budget"],
                "sites": [{"line": site["site_location"]["line"], "presence": site["field_presence"],
                    "closed": site["selected_field_shape_closed"], "relation": site["source_form_relation"]}
                    for site in summary["assessments"]], "helper_returns": [{"line": fact["location"]["line"],
                    "target": fact["target_graph_node_id"], "presence": fact["selected_field_presence"],
                    "closed": fact["selected_field_shape_closed"], "whole_closed": fact["whole_object_shape_closed"]}
                    for fact in compact["helpers"]]}, ensure_ascii=False), flush=True)
        output = {"kind": "development_saved_source_queries", "captured_snapshot_id": snapshot.id,
            "captured_source_hash": snapshot.source_hash, "current_query_tool_identity": tool_identity(),
            "query_component_version": VERSION, "published": False, "target_executed": False,
            "target_tests_run": False, "tool_test_suite_run": False, "observations": rows}
        (directory / (args.label + ".json")).write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    finally:
        store.close()


if __name__ == "__main__":
    main()
