"""Compact observations copied from actual development source-query records."""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> None:
    result = {"kind": "copied_development_source_query_observations", "formal_scan": False,
        "target_executed": False, "target_tests_run": False, "target_build_run": False, "queries": []}
    for name in ("lifecycle-source-query.json", "ownership-codepatchbay-source-query.json", "ownership-winwincode-source-query.json"):
        path = ROOT / name
        document = json.loads(path.read_text(encoding="utf-8"))
        entry = {"artifact": name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            **{key: document[key] for key in ("base_snapshot_id", "base_source_hash", "base_policy_hash", "module_sha256",
                "module_bytes_stable_during_query")}, "analyses": []}
        for index, analysis in enumerate(document["analyses"]):
            pattern = analysis["pattern"]
            copied = {"id": analysis["id"], "type": analysis["type"], "json_pointer": f"/analyses/{index}",
                "scoped_source_supported": pattern["scoped_source_supported"],
                "source_fact_counts": dict(Counter(fact["kind"] for fact in analysis["source_facts"])),
                "budgets": analysis["budgets"], "analysis_gaps": analysis["analysis_gaps"],
                "all_selected_graph_bindings_closed": all(analysis["source_graph_bindings_closed"].values())}
            if analysis["type"] == "browser_async_lifecycle":
                copied["relation_counts"] = {key: len(pattern[key]) for key in ("generation_argument_relations",
                    "nullable_context_consumer_relations", "closed_result_disposal_consumers",
                    "locally_guarded_publication_fact_ids", "post_suspension_without_local_guard_fact_ids",
                    "initial_synchronous_setup_fact_ids")}
                by_id = {fact["id"]: fact for fact in analysis["source_facts"]}
                copied["post_suspension_without_local_guard_sources"] = [
                    {"fact_id": identifier, "lexical_source_owner": by_id[identifier]["lexical_source_owner"],
                        "location": by_id[identifier]["location"], "target": by_id[identifier]["target"],
                        "lacking_local_guard_is_a_defect": False}
                    for identifier in pattern["post_suspension_without_local_guard_fact_ids"]]
                copied["all_stale_results_rejected_proven"] = pattern["all_stale_results_rejected_proven"]
            else:
                copied["ownership_assessment"] = pattern["ownership_assessment"]
                copied["captured_resource_writer_groups"] = pattern["captured_resource_writer_groups"]
                copied["canonical_authority_proven"] = pattern["canonical_authority_proven"]
            entry["analyses"].append(copied)
        result["queries"].append(entry)
    modules = {entry["module_sha256"] for entry in result["queries"]}
    if len(modules) != 1 or not all(entry["module_bytes_stable_during_query"] for entry in result["queries"]):
        raise RuntimeError("development observations have inconsistent module bytes")
    output = ROOT / "LIFECYCLE_OWNERSHIP_OBSERVATIONS.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(str(output))


if __name__ == "__main__":
    main()
