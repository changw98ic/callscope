"""Project closed formal report artifacts for the original-report scope ledger.

No database, analyzer, target source or lock is opened. Large source-fact and
adapter-judgment arrays remain on disk. This creates navigation evidence only;
it neither rates original prose nor changes a saved analysis assessment.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from render_report_summaries import _SavedJSON, _COUNT

HERE = Path(__file__).resolve().parent
_PATTERN_KEYS = (
    "scoped_source_supported", "source_relations_only", "source_only", "version", "trusted_model",
    "ownership_assessment", "responsibility_interpretation", "captured_resource_writer_groups",
    "unique_fact_owner_proven", "canonical_authority_proven", "all_mutations_authorized_proven",
    "all_storage_resources_bound_proven", "whole_repository_ownership_inferred", "unreviewed_scope",
    "groups", "unproved_relations", "record_boundary", "command_boundary", "retention_boundary",
    "field_joins", "relation_witnesses", "source_return_conditions_computed",
    "normal_append_then_refresh_orders", "expected_evidence_noninterference_proven",
    "silent_drop_for_all_inputs_excluded", "audit_subject_equivalence_to_other_systems_proven",
    "remote_success_proven", "exactly_once_proven", "all_recovery_complete_proven",
    "all_active_states_or_attempts_proven", "whole_domain_state_machine_closed",
    "runtime_schedule_or_termination_proven", "state_table_dependency_quantifier_linked",
    "finite_effective_state_relation", "dependency_blocker_relation", "persisted_selection_recheck_relation",
    "runtime_transport_or_physical_effect_proven", "whole_project_identity_complete", "limits",
    "all_async_callbacks_guarded_proven", "all_stale_results_rejected_proven",
    "unique_browser_runtime_binding_proven", "all_resources_released_proven", "scope_conditions",
    "components",
)
SELECTION = {
    "version": True, "snapshot": True,
    "coverage": {"files_selected": True, "files_parsed": True, "file_statuses": True,
        "unparsed_files": True, "selection_scope": True, "excluded": True, "meaning": True},
    "architecture": {"meaning": True, "captured_writer_references": True},
    "judgments": [{key: True for key in ("goal_id", "finding_id", "evidence_id", "analysis_type",
        "assessment", "summary", "complete_assessment", "full_goal_supported", "necessary_gaps", "saved_evidence_pointer")}],
    "functional_chains": [{"rule_id": True, "finding_id": True, "evidence_id": True,
        "claim_type": True, "assessment": True, "source_scope": True, "analysis_gaps": True,
        "saved_evidence_pointer": True, "pattern": {key: True for key in _PATTERN_KEYS},
        "source_facts": _COUNT}],
    "source_relation_index": True, "overlapping_source_selections": True, "report_scope": True,
    "runtime_functionality_verified": True, "target_executed": True, "target_tests_run": True,
    "target_build_run": True,
}


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        result = hashlib.file_digest(stream, "sha256").hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", choices=("codepatchbay", "winwincode"))
    args = parser.parse_args()
    repository = args.repository
    integration_path = HERE / f"{repository}-integration.json"
    integration = json.loads(integration_path.read_text())
    if not integration.get("database_closed") or not integration.get("database_wal_empty_or_absent"):
        raise ValueError("formal publication must be closed before scope projection")
    freeze = json.loads((HERE / "CORE_FREEZE.json").read_text())
    report, report_hash = _SavedJSON(HERE / f"{repository}-automatic-report.json").load(SELECTION)
    for index, chain in enumerate(report["functional_chains"]):
        chain["source_fact_count"] = chain.pop("source_facts")
        chain["formal_entry_pointer"] = f"/functional_chains/{index}"
        chain["source_facts_pointer"] = f"/functional_chains/{index}/source_facts"
    snapshot = report["snapshot"]
    snapshot_id = snapshot.get("id") or snapshot.get("snapshot_id")
    if snapshot_id != integration["snapshot_id"]:
        raise ValueError("formal report/integration snapshot mismatch")
    artifact = {"kind": "closed_formal_scope_projection", "repository": repository,
        "report_file": f"{repository}-automatic-report.json", "report_sha256": report_hash,
        "integration_file_sha256": digest(integration_path), "freeze_file_sha256": digest(HERE / "CORE_FREEZE.json"),
        "expected_frozen_tool_hash": freeze["tool_identity"]["source_hash"],
        "source_facts_replaced_by_counts_and_original_pointers": True,
        "new_analysis_or_rating_performed": False, "database_opened": False,
        "formal_projection": report}
    output = HERE / f"scope-{repository}-formal-observations.json"
    output.write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + "\n")
    mapping_path = HERE / "scope-pointer-map.json"
    mapping = json.loads(mapping_path.read_text())
    by_id = {entry["rule_id"]: entry for entry in report["functional_chains"]}
    if len(by_id) != len(report["functional_chains"]):
        raise ValueError("duplicate formal rule id")
    for entry in mapping["entries"] + mapping.get("preserved_partial_source_context_queries", []):
        if entry["repository"] != repository:
            continue
        chain = by_id.get(entry["rule_id"])
        if chain is None:
            raise ValueError("formal scope rule absent: " + entry["rule_id"])
        prefix = chain["formal_entry_pointer"]
        entry.update({"formal_state": chain["assessment"]["state"], "formal_entry_pointer": prefix,
            "formal_assessment_pointer": prefix + "/assessment", "formal_pattern_pointer": prefix + "/pattern",
            "formal_source_facts_pointer": prefix + "/source_facts", "formal_gaps_pointer": prefix + "/analysis_gaps",
            "formal_source_scope_pointer": prefix + "/source_scope", "formal_finding_id": chain["finding_id"],
            "formal_evidence_id": chain["evidence_id"], "formal_report_sha256": report_hash,
            "formal_snapshot_id": snapshot_id, "formal_source_fact_count": chain["source_fact_count"],
            "formal_analysis_gaps": chain["analysis_gaps"], "formal_assessment": chain["assessment"]})
    consumed = mapping.setdefault("formal_repositories_consumed", [])
    if repository not in consumed:
        consumed.append(repository)
    mapping["formal_results_consumed"] = True
    mapping["both_formal_repositories_consumed"] = set(consumed) == {"codepatchbay", "winwincode"}
    mapping_path.write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"repository": repository, "snapshot_id": snapshot_id, "report_sha256": report_hash,
        "chains": [{"rule": entry["rule_id"], "state": entry["assessment"]["state"],
            "pointer": entry["formal_entry_pointer"], "gaps": entry["analysis_gaps"],
            "source_facts": entry["source_fact_count"]} for entry in report["functional_chains"]]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
