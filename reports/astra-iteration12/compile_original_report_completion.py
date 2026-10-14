"""Reconcile saved automatic report bodies with the finite original report scope.

This reads artifacts only. It does not analyze target code or create target-code
findings. Prior semantic examples are exact saved-body locators, not answers
supplied to the analyzer. A partial invocation cannot close the two-report goal.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DIRECTORY = ROOT / "reports/astra-iteration12-scope2"


def sha(path):
    return hashlib.file_digest(path.open("rb"), "sha256").hexdigest()


def load(path):
    return json.loads(path.read_text())


def rel(path):
    return str(path.resolve().relative_to(ROOT))


def thin_statement(statement):
    owner = statement["actual_owner"]
    return {
        "formal_statement_pointer": statement["formal_statement_pointer"],
        "text": statement["text"],
        "actual_owner": {key: owner.get(key) for key in ("file", "symbol", "graph_node_id", "location", "binding_state")},
        "operation_id": statement["operation_id"],
        "operation_kind": statement["operation_kind"],
        "formal_operation_pointer": "/architecture/responsibility_explanations" + statement["operation_pointer"],
        "source_evidence_refs": statement["source_evidence_refs"],
        "operand_source_text": statement["operand_source_text"],
    }


SUPPLEMENT_RULES = {
    "codepatchbay-responsibility-row-34": ["cpb-task-read-projection"],
    "codepatchbay-responsibility-row-39": ["cpb-review-fixed-state-lineage", "cpb-finalizer-conditional-publication"],
    "cpb-events-delivery": ["cpb-review-fixed-state-lineage", "cpb-finalizer-conditional-publication"],
    "winwincode-responsibility-row-37": ["wwc-delivery-evidence-frozen-contract-slice"],
    "wwc-evidence-delivery": ["wwc-delivery-evidence-frozen-contract-slice"],
}
SEMANTIC_NOTES = {
    "codepatchbay-responsibility-row-34": "当前自动正文实际呈现命令参数/提交，以及 task 的 queue/job 读取、raw 字段投影、sanitize 和 render 实参来源；保持动态接口及传递依赖副作用边界，未证明全传递纯度。",
    "codepatchbay-responsibility-row-39": "服务记录/投影、审计和恢复接口有真实自动正文；新增实际 FIXED/事件/lineage 同源字段关系，以及模式、opt-in、PR 提前返回条件，保持远端效果未知。",
    "cpb-events-delivery": "事件持久写者、index 投影和重建/doctor 的有限来源与失败边界分开保存；FIXED 条件下的 job_superseded 字面记录和后续 lineage 字段同源有实际自动解释，GitHub/dry-run 的模式/授权条件与本地/远端效果分开。",
    "winwincode-responsibility-row-37": "当前自动来源覆盖产品 authority/WorkRun，以及候选冻结提交、角色、WorkRun/attempt/lease/fencing 和 Runtime/Candidate evidence-source 的有限合同盘点；不升级成所有角色授权或外部真实性证明。",
    "wwc-evidence-delivery": "当前实际记录、getter 来源、形实参和 guard 覆盖候选冻结提交、角色、WorkRun/attempt/lease/fencing、Runtime/Candidate evidence-source、来源序号和 outbox/ack；原未审外部真实性和适配器深层语义仍排除。",
    "wwc-browser-protocol": "浏览器 scope/generation/abort 和 boot 端口分支有实际保存来源；client/dispatcher 正文及生成 JSON/Serde 的有限消息模型解释所选命令接缝，未制造普通 CALLS 边或宣称网络请求已经成功。",
}
SUPPLEMENT_BODY_FILES = {
    "cpb-task-read-projection": "TASK_FINITE_CONTENT_DEVELOPMENT_READBACK.json",
    "wwc-delivery-evidence-frozen-contract-slice": "WWC_DELIVERY_EVIDENCE_FINITE_CONTENT_DEVELOPMENT_READBACK.json",
}


def repository_readback(repository):
    path = DIRECTORY / ("ORIGINAL_" + repository.upper() + "_CONTENT_READBACK.json")
    result = load(path)
    artifact = next(item for item in result["inputs"] if item["repository"] == repository)
    integration_path = DIRECTORY / (repository + "-integration.json")
    integration = load(integration_path)
    problems = list(result["input_issues"])
    problems += result["formal_freeze_identity_and_scope_readback"][repository]["identity_or_scope_issues"]
    validation = result["responsibility_reference_validation"][repository]
    problems += validation["reference_issues"]
    for seam in result["computed_seam_actual_source_pointer_readback"].get(repository, []):
        problems += seam.get("source_reference_issues", [])
    snapshot = artifact["snapshot"]
    if result["mode"] != "formal" or artifact["mode"] != "formal":
        problems.append("Input is not a formal saved-report readback")
    if integration.get("database_closed") is not True or integration.get("database_wal_empty_or_absent") is not True:
        problems.append("Formal integration has not closed the database/WAL")
    for key in ("snapshot_id", "source_hash", "policy_hash"):
        expected = snapshot["id" if key == "snapshot_id" else key]
        if integration.get(key) != expected:
            problems.append("Integration identity differs: " + key)
    result["_path"] = path
    result["_problems"] = problems
    result["_statements"] = validation["actual_statements"]
    result["_lookup"] = collections.defaultdict(list)
    for statement in result["_statements"]:
        owner = statement["actual_owner"]
        result["_lookup"][(owner["file"], owner["symbol"], statement["text"])].append(statement)
    result["_prior"] = {item["id"]: item for item in result["prior_five_and_31_current_results"]}
    result["_additional"] = {item["rule_id"]: item for item in result["additional_original_finite_clause_content"]}
    for item in result["_prior"].values():
        actual = item.get("new_formal_readback")
        if not actual:
            problems.append("Original finite entry missing or duplicated: " + item["id"])
            continue
        required_analysis_gaps = [gap for gap in actual.get("analysis_gaps", [])
            if not (isinstance(gap, dict) and gap.get("source_only") is True
                and gap.get("necessary_to_scoped_source_relations") is not True)]
        if actual.get("necessary_gaps") or required_analysis_gaps:
            problems.append("Original finite entry has necessary/analysis gaps: " + item["id"])
        if item["kind"] == "registered_condition_judgment":
            if actual.get("assessment") != "scoped_static_judgment_reproduced" or actual.get("complete_assessment") is not True or actual.get("full_goal_supported") is not True:
                problems.append("Original condition judgment not reproduced: " + item["id"])
        elif actual.get("assessment", {}).get("scoped_source_supported") is not True or not actual.get("source_fact_refs"):
            problems.append("Original finite source relation lacks supported source/facts: " + item["id"])
    result["_identity"] = {
        "report_file": Path(artifact["file"]).name,
        "repository_relative_report_file": artifact["file"],
        "report_sha256": artifact["sha256"],
        "snapshot_id": snapshot["id"],
        "source_hash": snapshot["source_hash"],
        "policy_hash": snapshot["policy_hash"],
        "tool_source_hash": snapshot["component_versions"]["tool"]["source_hash"],
        "generating_tool_source_hash": artifact["generating_components"]["generating_tool_identity"]["source_hash"],
        "formal_readback_file": path.name,
        "formal_readback_sha256": sha(path),
        "integration_file": integration_path.name,
        "integration_sha256": sha(integration_path),
        "database_closed": True,
        "database_wal_empty_or_absent": True,
        "reference_or_identity_issues": problems,
        "reported_unmodeled_or_unparsed_scope": result["formal_freeze_identity_and_scope_readback"][repository]["coverage"],
    }
    return result


def reconcile_unit(unit, contract_unit, readback):
    problems = []
    statements = []
    for example in unit["actual_automatic_body_examples"]:
        actual = readback["_lookup"][(example["file"], example["actual_owner"], example["text"])]
        if not actual:
            problems.append({"kind": "prior_actual_source_body_not_found", "file": example["file"], "owner": example["actual_owner"], "text": example["text"]})
        else:
            statements.append(thin_statement(actual[0]))
    related = contract_unit.get("prior_related_entries", contract_unit.get("related_entries", []))
    relations = []
    for identifier in dict.fromkeys(related + SUPPLEMENT_RULES.get(unit["id"], [])):
        if identifier in readback["_prior"]:
            prior = readback["_prior"][identifier]["new_formal_readback"]
            relations.append({"id": identifier, **{key: prior.get(key) for key in ("pointer", "finding_id", "evidence_id", "assessment", "actual_derived_judgment", "actual_conditions", "actual_pattern_scope", "analysis_gaps", "necessary_gaps")}})
        elif identifier in readback["_additional"]:
            extra = readback["_additional"][identifier]
            chain = extra["actual_chain"]
            relations.append({"id": identifier, "pointer": extra["actual_chain_pointer"], "finding_id": chain["finding_id"], "evidence_id": chain["evidence_id"], "assessment": chain["assessment"], "actual_automatic_pattern": chain["pattern"]})
        elif identifier != "wwc-device-documentation-deployment-comparison":
            problems.append({"kind": "expected_finite_relation_missing", "id": identifier})
    supplementary = []
    captured_source_fact_readbacks = []
    for identifier in SUPPLEMENT_RULES.get(unit["id"], []):
        extra = readback["_additional"].get(identifier)
        if not extra:
            continue
        chain = extra["actual_chain"]
        if chain["assessment"].get("scoped_source_supported") is not True:
            problems.append({"kind": "supplementary_source_relation_not_supported", "id": identifier})
        # Locate the already-read finite examples in the current normal body.
        # Do not copy every operation or treat a candidate count as completion.
        examples_file = SUPPLEMENT_BODY_FILES.get(identifier)
        if examples_file:
            examples = load(HERE / examples_file)
            for operation in examples["actual_source_operations_and_generated_bodies"]:
                for example in operation["actual_generated_statements"]:
                    owner = example["actual_owner"]
                    actual = readback["_lookup"][(owner["file"], owner["symbol"], example["text"])]
                    if not actual:
                        problems.append({"kind": "finite_supplement_body_not_found", "id": identifier, "file": owner["file"], "owner": owner["symbol"], "text": example["text"]})
                    else:
                        supplementary.append(thin_statement(actual[0]))
            for fact in examples.get("frozen_commit_getter_actual_source_facts", []):
                expected_location = fact["location"]
                matches = [(index, actual) for index, actual in enumerate(chain.get("source_facts", []))
                    if actual.get("kind") == fact.get("kind") and all(
                        actual.get("location", {}).get(key) == expected_location.get(key)
                        for key in ("file", "source_hash", "start_byte", "end_byte", "span_hash"))]
                if len(matches) != 1:
                    problems.append({"kind": "finite_frozen_commit_getter_source_not_matched", "rule": identifier})
                else:
                    index, actual = matches[0]
                    captured_source_fact_readbacks.append({
                        "formal_source_fact_pointer": extra["actual_chain_pointer"] + "/source_facts/" + str(index),
                        "actual_fact": actual,
                        "same_captured_source_bytes_as_finite_semantic_readback": True,
                        "finite_semantic_readback_file": rel(HERE / examples_file),
                        "source_fact_is_not_missing_because_implicit_Rust_return_has_no_generic_statement": True,
                    })
    return {
        "id": unit["id"], "repository": unit["repository"],
        "original_anchors": unit["original_anchors"],
        "actual_semantic_readback": SEMANTIC_NOTES.get(unit["id"], unit["actual_content_readback"]),
        "actual_formal_automatic_body": statements,
        "actual_formal_supplementary_body": supplementary,
        "captured_source_fact_readbacks": captured_source_fact_readbacks,
        "actual_formal_finite_relations": relations,
        "original_finite_clauses": contract_unit.get("original_finite_clauses_to_find_in_actual_output"),
        "remaining_finite_source_content_gaps": problems,
        "finite_original_content_addressed": not problems and not readback["_problems"],
        "meaning_is_not_inferred_from_role_labels_or_counts": True,
        "runtime_effects_proven": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", action="append", choices=("codepatchbay", "winwincode"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--finalize", action="store_true", help="Require both formal reports and completed documentation/baseline identity artifacts")
    args = parser.parse_args()
    repositories = args.repository or ["codepatchbay", "winwincode"]
    contract = load(HERE / "REPORT_COMPLETION_CONTRACT.json")
    audit = load(HERE / "REPORT_COMPLETION_LAST_DEVELOPMENT_SEMANTIC_AUDIT.json")
    reports = {repository: repository_readback(repository) for repository in repositories}
    units = {item["id"]: item for item in contract["pending_original_explanations"] + contract["original_main_chain_reconciliation"]}
    output = {
        "schema": "original-finite-report-content-completion-1", "mode": "formal",
        "artifact_path_base": "this_file_parent", "repositories": {key: value["_identity"] for key, value in reports.items()},
        "scope": "Original already-read finite source content of the unchanged complete Astra reports; no added review of original unreviewed domains.",
        "original_responsibility_rows": [reconcile_unit(item, units[item["id"]], reports[item["repository"]]) for item in audit["original_fourteen_responsibility_rows"] if item["repository"] in reports],
        "original_main_chain_domains": [reconcile_unit(item, units[item["id"]], reports[item["repository"]]) for item in audit["original_ten_domains"] if item["repository"] in reports],
        "retained_source_only_boundaries": [{"repository": repository, "id": item["id"],
            "formal_pointer": item["new_formal_readback"]["pointer"] + "/analysis_gaps",
            "actual_gaps": item["new_formal_readback"].get("analysis_gaps", [])}
            for repository, report in reports.items() for item in report["_prior"].values()
            if item.get("new_formal_readback", {}).get("analysis_gaps")],
        "saved_finite_source_seams": {repository: [{
            "formal_seam_pointer": item["pointer"],
            "actual_automatic_explanation": {key: item["actual_seam"].get(key) for key in (
                "kind", "text", "source_analysis_pointer", "source_obligation_pointer", "source_relation_refs", "models",
                "supported_source_relation", "scope", "source_gaps", "conditions", "transport_model", "scope_boundaries",
                "network_success_verified", "creates_calls_edge", "generated_support_upgraded_to_implementation",
                "source_statement_relation_closed") if key in item["actual_seam"]},
            "actual_source_pointer_reference_issues": item.get("source_reference_issues", []),
        } for item in report["computed_seam_actual_source_pointer_readback"].get(repository, [])] for repository, report in reports.items()},
        "reader_identity": {"file": rel(HERE / "readback_report_completion.py"), "sha256": sha(HERE / "readback_report_completion.py")},
        "reconciliation_identity": {"file": rel(Path(__file__)), "sha256": sha(Path(__file__))},
        "input_semantic_mapping": {"file": rel(HERE / "REPORT_COMPLETION_LAST_DEVELOPMENT_SEMANTIC_AUDIT.json"), "sha256": sha(HERE / "REPORT_COMPLETION_LAST_DEVELOPMENT_SEMANTIC_AUDIT.json")},
        "original_scope_boundaries": contract["original_excluded_and_negative_inference_boundaries"],
        "not_required_to_finish": contract["not_required_to_finish"],
        "paragraph_scoring_performed": False, "functional_coverage_percentage_computed": False,
        "target_source_read": False, "database_read": False, "analyzer_run": False,
        "target_executed": False, "target_tests_run": False, "target_build_run": False,
        "astra_re_review_or_approval": False, "manual_new_target_judgments_generated": False,
    }
    gaps = [problem for report in reports.values() for problem in report["_problems"]]
    gaps.extend({"id": unit["id"], "problems": unit["remaining_finite_source_content_gaps"]} for key in ("original_responsibility_rows", "original_main_chain_domains") for unit in output[key] if unit["remaining_finite_source_content_gaps"])
    output["remaining_known_original_source_content_gaps"] = gaps
    output["completion_assessment"] = {
        "complete": False,
        "status": "formal_content_reconciliation_requires_documentation_and_baseline_readback",
        "reason": "This compiler records actual bodies and references. Final two-report assessment also requires actual three-aspect documentation, original-five/31 source results and frozen-observation/publication identity readbacks; field occurrence or item count cannot close it.",
    }
    if args.finalize:
        if set(reports) != {"codepatchbay", "winwincode"}:
            raise ValueError("Final assessment requires both formally closed saved reports")
        documentation = reports["winwincode"]["documentation_aspects"]
        if not documentation or any(item["reference_or_scope_issues"] or item["necessary_gaps"]
                or item["all_required_source_aspects_supported"] is not True
                or item["input_context"] != "actual_saved_formal_report" for item in documentation):
            raise ValueError("Actual finite documentation comparison is not closed")
        comparison_path = DIRECTORY / "ORIGINAL_BASELINE_COMPARISON.json"
        identity_path = DIRECTORY / "PUBLICATION_IDENTITY.json"
        comparison, identity = load(comparison_path), load(identity_path)
        if comparison.get("publication_identity_verified") is not True or identity.get("verified") is not True:
            raise ValueError("Frozen comparison/publication identity is not verified")
        for item in comparison["repositories"]:
            expected = reports[item["repository"]]["_identity"]
            if item["snapshot_id"] != expected["snapshot_id"] or item["changes"]:
                raise ValueError("Frozen observations changed or differ from the formal snapshot")
        for item in identity["repositories"]:
            expected = reports[item["repository"]]["_identity"]
            target = item["target_identity"]
            if not all(item["publication_identity_checks"].values()) or not all(target.get(key) is True for key in (
                    "commit_matches", "live_referenced_source_hashes_match", "saved_referenced_source_hashes_match")):
                raise ValueError("Actual publication/source identity checks are not closed")
            for key in ("source_hash", "policy_hash"):
                if item["metadata"][key] != expected[key]:
                    raise ValueError("Publication source/policy identity differs")
            if item["metadata"]["id"] != expected["snapshot_id"]:
                raise ValueError("Publication snapshot identity differs")
        for repository, report in reports.items():
            md_path = DIRECTORY / (repository + "-automatic-report.md")
            output["repositories"][repository]["markdown_file"] = md_path.name
            output["repositories"][repository]["markdown_sha256"] = sha(md_path)
            output["repositories"][repository]["markdown_generator"] = report["inputs"][0]["generating_components"]["markdown"]
        output["documentation_aspects"] = documentation
        output["prior_five_judgments_and_finite_source_relations"] = []
        for repository, report in reports.items():
            for item in report["_prior"].values():
                actual = item["new_formal_readback"]
                facts = actual.get("source_fact_refs", [])
                canonical = json.dumps(facts, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode()
                output["prior_five_judgments_and_finite_source_relations"].append({
                    "id": item["id"], "repository": repository, "kind": item["kind"],
                    **{key: actual.get(key) for key in ("pointer", "finding_id", "evidence_id", "assessment", "complete_assessment", "full_goal_supported",
                        "necessary_gaps", "analysis_gaps", "actual_derived_judgment", "actual_conditions", "actual_pattern_scope")},
                    "actual_refutations_pointer": actual["pointer"] + "/refutations" if item["kind"] == "registered_condition_judgment" else None,
                    "actual_source_facts_pointer": actual["pointer"] + "/source_facts" if item["kind"] != "registered_condition_judgment" else None,
                    "actual_source_fact_ids": [fact["id"] for fact in facts],
                    "source_fact_reference_set_sha256": hashlib.sha256(canonical).hexdigest(),
                    "source_fact_reference_readback_file": report["_path"].name,
                    "preservation_not_a_functional_coverage_denominator": True,
                })
        output["frozen_observation_and_publication_readback"] = {
            "comparison_file": comparison_path.name, "comparison_sha256": sha(comparison_path),
            "identity_file": identity_path.name, "identity_sha256": sha(identity_path),
            "actual_comparison": comparison, "implementation_identity": identity["implementation"],
            "publication_identity_verified": identity["verified"],
            "comparison_does_not_redefine_original_finite_report_scope": True,
        }
        output["artifact_reader_projection_history"] = reports["codepatchbay"].get("artifact_reader_projection_history")
        output["completion_assessment"] = {
            "complete": not gaps,
            "status": "original_already_read_finite_source_report_content_addressed" if not gaps else "original_finite_source_content_gap_remains",
            "reason": "The actual saved automatic bodies, finite source-model statements, three document/source comparisons and source references address each original already-read finite clause. Both formal identities and unchanged frozen observations are read back. Original unreviewed domains and source-only effect limits are preserved.",
            "whole_program_functional_completeness_proven": False,
            "runtime_or_business_success_verified": False,
            "complete_original_report_verbatim_reproduction_claimed": False,
            "exceeds_all_original_report_content_claimed": False,
            "completion_from_version_label_or_item_count": False,
        }
        if gaps:
            raise ValueError("Known finite original content gaps remain; cannot finalize")
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"file": rel(args.output), "sha256": sha(args.output), "repositories": repositories, "remaining_source_gaps": gaps, "complete": output["completion_assessment"]["complete"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
