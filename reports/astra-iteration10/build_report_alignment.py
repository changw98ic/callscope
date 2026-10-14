"""Map original whole-report scope to saved automatic artifacts, without rating.

This standard-library helper consumes the frozen report catalog, the two future
automatic-report/configured-findings JSON artifacts and goal-ledger.json. It
does not invoke a detector, read a target worktree, open an analysis database,
import a target, run tests or use benchmark prose as machine evidence.

Missing formal artifacts fail explicitly. Existing outputs are never replaced.
"""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Any

VERSION = "saved-whole-report-scope-alignment-1"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REPOSITORIES = ("codepatchbay", "winwincode")
ORIGINAL_HASHES = {
    "codepatchbay": "863f5dfe52ced7129a0bda499afa4a89b30d2db9396c654a5120204cfe422900",
    "winwincode": "b3f8b1def361595e2bd3540a6bca5381ef4ad2a71d4f3c49535bf3f24f212950",
}
GOALS = {"codepatchbay": ("CPB-01", "CPB-02", "CPB-03"), "winwincode": ("WWC-01", "WWC-02")}

# Human navigation from catalog domains to already-defined analysis IDs.  These
# assignments are never used to generate a finding, a source fact or a result.
CHAINS = {
    ("codepatchbay", 8): ("cpb-report-engine-stage-chain", "cpb-report-job-audit-best-effort"),
    ("codepatchbay", 9): ("cpb-report-agent-execution-policy", "cpb-report-trusted-probe-command-source", "cpb-report-unsupported-probe-evidence"),
    ("codepatchbay", 10): ("cpb-report-conditional-delivery-result",),
    ("winwincode", 7): ("wwc-report-chat-delivery-workrun-requests", "wwc-report-workrun-state-guards"),
    ("winwincode", 8): ("wwc-report-worker-bootstrap-entries", "wwc-report-worker-production-construction", "wwc-report-worker-typed-dispatch"),
    ("winwincode", 9): ("wwc-report-production-adapter-embedded-kernel", "wwc-report-adapter-durable-exact-turn",
        "wwc-report-submission-intent-kernel-order", "wwc-report-kernel-create-session-interface",
        "wwc-report-kernel-submit-turn-interface", "wwc-report-kernel-reconcile-exact-interface"),
    ("winwincode", 11): ("wwc-report-device-provider-deployment",),
}
SECTION_GOALS = {
    ("codepatchbay", 2): GOALS["codepatchbay"], ("codepatchbay", 6): ("CPB-01", "CPB-03"),
    ("codepatchbay", 7): ("CPB-01",), ("codepatchbay", 8): ("CPB-01",),
    ("codepatchbay", 10): ("CPB-02",), ("codepatchbay", 11): GOALS["codepatchbay"],
    ("codepatchbay", 12): ("CPB-01",), ("codepatchbay", 13): ("CPB-02",), ("codepatchbay", 14): ("CPB-03",),
    ("codepatchbay", 15): GOALS["codepatchbay"],
    ("winwincode", 2): GOALS["winwincode"], ("winwincode", 6): ("WWC-01", "WWC-02"),
    ("winwincode", 7): ("WWC-02",), ("winwincode", 12): GOALS["winwincode"],
    ("winwincode", 13): ("WWC-01",), ("winwincode", 14): ("WWC-02",),
    ("winwincode", 15): GOALS["winwincode"],
}
STRUCTURAL_CATEGORIES = {"report_metadata", "architecture_and_ownership", "architecture_and_findings",
    "architecture_and_deployment", "coverage_and_unreviewed", "capability_priorities"}


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=True, sort_keys=True,
        separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reject_constant(value: str):
    raise ValueError("Nonfinite JSON is not saved report evidence: " + value)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"), parse_constant=reject_constant)


def at_pointer(value: Any, pointer: str) -> Any:
    if pointer and not pointer.startswith("/"):
        raise ValueError("JSON pointer must be absolute")
    for token in pointer[1:].split("/") if pointer else []:
        token = token.replace("~1", "/").replace("~0", "~")
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


class _Inputs:
    def __init__(self):
        self.documents: dict[str, Any] = {}
        self.paths: dict[str, Path] = {}
        self.hashes: dict[str, str] = {}
        self.references: dict[str, dict] = {}

    def load(self, name: str, path: Path) -> Any:
        path = path.resolve(strict=True)
        content = path.read_bytes()
        self.paths[name], self.hashes[name] = path, hashlib.sha256(content).hexdigest()
        self.documents[name] = json.loads(content.decode("utf-8"), parse_constant=reject_constant)
        return self.documents[name]

    def ref(self, name: str, pointer: str, origin: str, context: dict | None = None,
            finding_id: str | None = None, evidence_id: str | None = None) -> dict:
        value = at_pointer(self.documents[name], pointer)
        result = {"artifact": os.path.relpath(self.paths[name], HERE), "artifact_sha256": self.hashes[name],
            "json_pointer": pointer, "target_value_sha256": digest(value), "origin": origin,
            "canonical_hash_encoding": "json_sorted_ascii_compact_sha256"}
        if context:
            result["snapshot_identity"] = deepcopy(context)
        if finding_id is not None:
            result["finding_id"] = finding_id
        if evidence_id is not None:
            result["evidence_id"] = evidence_id
        key = digest(result)
        self.references.setdefault(key, result)
        return deepcopy(result)

    def unchanged(self):
        for name, path in self.paths.items():
            if file_hash(path) != self.hashes[name]:
                raise ValueError("Input changed during alignment: " + name)
        for reference in self.references.values():
            name = next(name for name, path in self.paths.items()
                if os.path.relpath(path, HERE) == reference["artifact"])
            if digest(at_pointer(self.documents[name], reference["json_pointer"])) != reference["target_value_sha256"]:
                raise ValueError("Copied pointer target changed")


def validate_catalog(catalog: dict) -> None:
    reports = catalog.get("original_reports", [])
    if [report.get("repository") for report in reports] != list(REPOSITORIES):
        raise ValueError("Catalog original repositories/order changed")
    if sum(len(report.get("sections", [])) for report in reports) != 32 or sum(len(report.get("statements", [])) for report in reports) != 130:
        raise ValueError("Original 32-section/130-statement catalog must remain complete")
    all_ids = set()
    for report in reports:
        path = (ROOT / report["file"]).resolve(strict=True)
        if not path.is_relative_to(ROOT / "reports/astra-baseline"):
            raise ValueError("Original report must be the frozen benchmark artifact")
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != ORIGINAL_HASHES[report["repository"]] or report.get("source_hash") != ORIGINAL_HASHES[report["repository"]] or report.get("bytes") != len(data):
            raise ValueError("Original report identity changed")
        for item in [*report["sections"], *report["statements"]]:
            if item["id"] in all_ids:
                raise ValueError("Duplicate original catalog item")
            all_ids.add(item["id"])
            source = item["source"]
            start, end = source["start_byte"], source["end_byte"]
            if source["file"] != report["file"] or source["source_hash"] != report["source_hash"] or not 0 <= start <= end <= len(data) or hashlib.sha256(data[start:end]).hexdigest() != source["span_hash"]:
                raise ValueError("Original catalog span no longer matches raw benchmark")


def _snapshot_context(report: dict) -> dict:
    snapshot = report.get("snapshot", {})
    required = {"id", "project_id", "source_hash", "policy_hash", "component_versions"}
    if not isinstance(snapshot, dict) or not required <= set(snapshot):
        raise ValueError("Automatic report lacks its saved snapshot identity")
    return {key: deepcopy(snapshot[key]) for key in required}


def _same_header(details: dict, context: dict):
    if any(details.get(key) != context[field] for key, field in (("snapshot_id", "id"), ("source_hash", "source_hash"), ("policy_hash", "policy_hash"))):
        raise ValueError("Automatic finding details and project report belong to different contexts")


def _unique(values: list[dict], key: str) -> dict[str, tuple[int, dict]]:
    result = {}
    for index, value in enumerate(values):
        name = value.get(key)
        if not isinstance(name, str) or not name or name in result:
            raise ValueError("Missing/duplicate saved identity: " + key)
        result[name] = index, value
    return result


def repository_results(inputs: _Inputs, repository: str, report: dict, findings: list[dict], ledger: dict) -> dict:
    context = _snapshot_context(report)
    if report.get("report_scope", {}).get("whole_report_reproduction_claimed") is not False:
        raise ValueError("Report scope must explicitly retain the whole-report boundary")
    if any(report.get(key) is not False for key in ("target_executed", "target_tests_run", "target_build_run", "runtime_functionality_verified")):
        raise ValueError("Alignment expects explicitly static, nonexecuted report inputs")
    if not isinstance(findings, list):
        raise ValueError("Configured findings must be saved original finding documents")
    by_finding = _unique(findings, "id")
    judgments = _unique(report.get("judgments", []), "goal_id")
    chains = _unique(report.get("functional_chains", []), "rule_id")
    by_ledger = _unique(ledger.get("goals", []), "id")
    if set(judgments) != set(GOALS[repository]):
        raise ValueError("Formal report must preserve this repository's original goal IDs")
    for finding in findings:
        if finding.get("snapshot_id") != context["id"]:
            raise ValueError("Configured finding belongs to another snapshot")

    def saved_evidence(row: dict, expected_kind: str) -> tuple[int, int, dict, dict]:
        if row.get("finding_id") not in by_finding:
            raise ValueError("Report finding pointer does not reference an actual configured finding")
        finding_index, finding = by_finding[row["finding_id"]]
        expected_type = "static_goal_judgment" if expected_kind == "static_whole_judgment" else "static_report_claim"
        if finding.get("type") != expected_type:
            raise ValueError("Report points to a different configured finding type")
        selected = [(index, evidence) for index, evidence in enumerate(finding.get("evidence", [])) if evidence.get("id") == row.get("evidence_id")]
        if len(selected) != 1 or selected[0][1].get("kind") != expected_kind:
            raise ValueError("Report evidence pointer is missing, duplicated or has a different kind")
        evidence_index, evidence = selected[0]
        details = evidence["details"]
        _same_header(details, context)
        if row.get("saved_evidence_pointer") != f"/evidence/{evidence_index}/details":
            raise ValueError("Report's finding-relative evidence pointer differs")
        if not isinstance(details.get("contract_hash"), str) or not details["contract_hash"]:
            raise ValueError("Saved assessment lacks its own contract identity")
        return finding_index, evidence_index, finding, details

    goals = {}
    for goal_id, (report_index, row) in judgments.items():
        fi, ei, finding, details = saved_evidence(row, "static_whole_judgment")
        if details.get("goal_id") != goal_id or details.get("analyzer") != row.get("analysis_type"):
            raise ValueError("Report goal/analyzer differs from its original finding")
        keys = ("assessment", "complete_assessment", "full_goal_supported", "derived_judgment", "conditions", "refutations", "obligations", "necessary_gaps", "adapter_judgments")
        if any(row.get(key) != details.get(key) for key in keys):
            raise ValueError("Automatic report changed a saved goal result")
        ledger_index, ledger_goal = by_ledger[goal_id]
        if ledger_goal.get("repository") != repository or ledger_goal.get("registered_judgment") != details:
            raise ValueError("Goal ledger and actual saved judgment differ")
        identity = {**context, "contract_hash": details["contract_hash"], "rule_id": finding["rule_id"]}
        refs = [inputs.ref(repository+":report", f"/judgments/{report_index}", "saved_automatic_registered_judgment", identity, finding["id"], row["evidence_id"]),
            inputs.ref(repository+":findings", f"/{fi}/evidence/{ei}/details", "original_saved_finding_evidence", identity, finding["id"], row["evidence_id"]),
            inputs.ref("ledger", f"/goals/{ledger_index}/registered_judgment", "saved_implementation_ledger_result", identity, finding["id"], row["evidence_id"])]
        goals[goal_id] = {"kind": "saved_registered_judgment", "goal_id": goal_id,
            "assessment": deepcopy(details["assessment"]), "complete_assessment": deepcopy(details["complete_assessment"]),
            "full_goal_supported": deepcopy(details["full_goal_supported"]), "derived_judgment": deepcopy(details.get("derived_judgment")),
            "necessary_gaps": deepcopy(details.get("necessary_gaps", [])), "refs": refs,
            "source_of_status": "copied_saved_result_not_independently_rated", "paragraph_equivalence_assessed": False}
    source_chains = {}
    for rule_id, (report_index, row) in chains.items():
        fi, ei, finding, details = saved_evidence(row, "static_report_chain_analysis")
        pairs = (("claim_type", "claim_type"), ("assessment", "assessment"), ("pattern", "pattern"),
            ("source_facts", "source_facts"), ("source_scope", "scope"), ("analysis_gaps", "analysis_gaps"),
            ("trusted_models", "trusted_models"), ("policy_declarations", "policy_declarations"))
        if rule_id != finding.get("rule_id") or any(row.get(report_key) != details.get(source_key) for report_key, source_key in pairs):
            raise ValueError("Automatic report changed a saved source-chain result")
        identity = {**context, "contract_hash": details["contract_hash"], "rule_id": rule_id}
        refs = [inputs.ref(repository+":report", f"/functional_chains/{report_index}", "saved_source_chain_report", identity, finding["id"], row["evidence_id"]),
            inputs.ref(repository+":findings", f"/{fi}/evidence/{ei}/details", "original_saved_source_chain_evidence", identity, finding["id"], row["evidence_id"]),
            inputs.ref(repository+":findings", f"/{fi}/evidence/{ei}/details/source_facts", "complete_automatic_source_facts", identity, finding["id"], row["evidence_id"])]
        source_chains[rule_id] = {"kind": "saved_source_chain", "rule_id": rule_id,
            "assessment": deepcopy(details.get("assessment", {})), "source_scope": deepcopy(details.get("scope", {})),
            "analysis_gaps": deepcopy(details.get("analysis_gaps", [])), "source_fact_count": len(details.get("source_facts", [])),
            "source_facts_fully_preserved_by_pointer": True, "refs": refs,
            "full_domain_or_runtime_reproduction_claimed": False, "paragraph_equivalence_assessed": False}
    return {"context": context, "goals": goals, "chains": source_chains, "report": report}


def _section_number(section: dict) -> int:
    return int(section["id"].rsplit(":", 1)[-1])


def map_section(inputs: _Inputs, repository: str, report_index: int, section_index: int,
                section: dict, results: dict) -> dict:
    domain = (repository, _section_number(section))
    goal_ids = SECTION_GOALS.get(domain, ())
    claim_ids = CHAINS.get(domain, ())
    goal_results = [deepcopy(results["goals"][identifier]) for identifier in goal_ids]
    chain_results = [deepcopy(results["chains"][identifier]) for identifier in claim_ids if identifier in results["chains"]]
    missing = [{"analysis_id": identifier, "reason": "No corresponding saved source-chain report result is available."}
        for identifier in claim_ids if identifier not in results["chains"]]
    remaining = ["All semantic statements outside the saved selected judgment/source-chain scopes remain unreviewed.",
        "Catalog paragraph or filename correspondence is not proof that its entire wording has been automatically reproduced."]
    if domain in {("codepatchbay", 6), ("codepatchbay", 7), ("winwincode", 6)}:
        remaining.append("Related complete judgments provide only their saved entry/protocol/budget scope; every command candidate, readiness path, general HTTP/WS route and recovery branch is not inferred from them.")
    if section["category"] in STRUCTURAL_CATEGORIES:
        remaining.append("Project declarations, directories and graph dependencies have not been converted into a comprehensive interpretation of responsibilities or fact ownership.")
    refs = [inputs.ref("catalog", f"/original_reports/{report_index}/sections/{section_index}", "unchanged_original_report_catalog")]
    refs.extend(ref for result in [*goal_results, *chain_results] for ref in result["refs"])
    structural = []
    if section["category"] in STRUCTURAL_CATEGORIES:
        for pointer in ("/snapshot", "/project_declarations", "/architecture", "/coverage", "/overlapping_source_selections", "/report_scope"):
            structural.append(inputs.ref(repository+":report", pointer, "saved_structural_and_scope_inventory", results["context"]))
        refs.extend(structural)
    unreviewed = section["category"] in {"coverage_and_unreviewed", "boundary", "capability_priorities"}
    if goal_results or chain_results:
        availability = "corresponding_saved_automatic_results_available"
    elif structural:
        availability = "structural_inventory_only_no_comprehensive_responsibility_interpretation"
    else:
        availability = "benchmark_scope_preserved_without_corresponding_automatic_judgment"
    return {"original": deepcopy(section), "domain": {"repository": repository, "catalog_section_id": section["id"],
            "goal_ids": list(goal_ids), "report_claim_ids": list(claim_ids), "mapping_origin": "fixed_human_domain_navigation_not_machine_evidence"},
        "correspondence": {"availability": availability, "saved_goal_results": goal_results, "saved_chain_results": chain_results,
            "structural_inventory_refs": structural, "missing_saved_analysis_ids": missing,
            "automatic_responsibility_semantics_fully_interpreted": False,
            "remaining_report_scope": remaining,
            "original_section_text_equivalence_assessed": False, "scope_beyond_selected_results_remains_unreviewed": True,
            "original_unreviewed_and_counterevidence_scope_retained": unreviewed,
            "file_or_selector_coincidence_implies_reproduction": False},
        "automatic_evidence_refs": refs}


def build_alignment(inputs: _Inputs, catalog: dict, results: dict) -> dict:
    output_reports = []
    for report_index, original in enumerate(catalog["original_reports"]):
        repository = original["repository"]
        sections = [map_section(inputs, repository, report_index, index, section, results[repository]) for index, section in enumerate(original["sections"])]
        by_title = {section["original"]["title"]: section for section in sections}
        if len(by_title) != len(sections):
            raise ValueError("Original section title is not unique within its report")
        statements = []
        for statement_index, statement in enumerate(original["statements"]):
            parent = by_title.get(statement["section_title"])
            if parent is None:
                raise ValueError("Original statement has no preserved parent section")
            refs = [inputs.ref("catalog", f"/original_reports/{report_index}/statements/{statement_index}", "unchanged_original_paragraph_or_table_row")]
            refs.extend(deepcopy(parent["automatic_evidence_refs"]))
            statements.append({"original": deepcopy(statement), "parent_catalog_section_id": parent["original"]["id"],
                "domain_navigation": deepcopy(parent["domain"]), "automatic_evidence_refs": refs,
                "automatic_statement_reproduction": "not_rated_by_scope_alignment",
                "evidence_scope": "Evidence corresponds to the parent domain; it does not certify every sentence, recommendation, or unreviewed item in this paragraph.",
                "original_boundaries_and_unreviewed_scope_preserved": True,
                "file_or_locator_matching_is_automatic_judgment": False})
        output_reports.append({"repository": repository, "original_report": {key: deepcopy(original[key]) for key in ("file", "source_hash", "bytes")},
            "automatic_snapshot_identity": deepcopy(results[repository]["context"]), "sections": sections, "statements": statements,
            "declared_scope": {"whole_report_reproduction_claimed": False, "architecture_responsibility_semantics_comprehensively_derived": False,
                "source_only_chains_are_not_complete_runtime_functionality": True, "original_unreviewed_scope_still_unreviewed": True}})
    result = {"schema": "callscope.saved-original-whole-report-alignment.v1", "builder_version": VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(), "kind": "saved_automatic_results_to_original_scope_navigation",
        "purpose": "Map actual saved judgments, source-chain evidence and structural inventories to the unchanged original whole-report benchmark; no new rating or approval.",
        "original_reports": output_reports,
        "catalog_preservation": {"section_count": 32, "statement_count": 130, "all_catalog_items_preserved": True,
            "baseline_observations": deepcopy(catalog.get("baseline_observations", [])),
            "target_source_hashes": deepcopy(catalog.get("target_source_hashes", [])),
            "counts_are_navigation_inventory_not_functional_coverage": True},
        "saved_result_inventory": {repository: {"goal_ids": list(results[repository]["goals"]), "report_claim_ids": list(results[repository]["chains"]),
            "goal_statuses_copied_from_saved_results": {key: value["assessment"] for key, value in results[repository]["goals"].items()},
            "chain_states_copied_from_saved_results": {key: value["assessment"].get("state") for key, value in results[repository]["chains"].items()}}
            for repository in REPOSITORIES},
        "overlapping_source_selections": {repository: {"saved_result": deepcopy(results[repository]["report"].get("overlapping_source_selections", [])),
            "evidence_ref": inputs.ref(repository+":report", "/overlapping_source_selections", "saved_overlap_inventory_not_extra_coverage", results[repository]["context"]),
            "duplicate_source_selections_are_extra_functional_coverage": False} for repository in REPOSITORIES},
        "report_scope": {"whole_report_reproduction_claimed": False, "entire_report_exceeded_claimed": False,
            "new_functional_pass_rate_computed": False, "paragraph_semantic_equivalence_computed": False,
            "unmodeled_domains_are_not_approved": True, "benchmark_text_used_to_generate_machine_evidence": False,
            "meaning": "Specific saved judgments and selected source chains can support comparable code-level report content; broader responsibility interpretation, unreviewed areas and literal whole-report reproduction are not supplied by this mapping."},
        "builder_behavior": {"only_saved_json_and_frozen_report_text_read": True, "detector_invoked": False,
            "target_workspace_read": False, "target_imported_or_executed": False, "target_tests_run": False,
            "target_build_run": False, "tool_test_suite_run": False, "reviewer_approval_added": False},
        "artifact_inventory": [{"name": name, "file": os.path.relpath(path, HERE), "sha256": inputs.hashes[name]}
            for name, path in inputs.paths.items()],
        "unique_evidence_reference_count": len(inputs.references)}
    return result


def write_new(path: Path, value: dict):
    path = path.resolve()
    if not path.is_relative_to(HERE) or path.suffix != ".json":
        raise ValueError("Write a new JSON artifact within this iteration")
    if path.exists():
        raise ValueError("Existing alignment outputs are immutable; choose another output")
    payload = (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+"\n").encode("utf-8")
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".report-alignment-", suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(payload)
        os.link(temporary, path)
    finally:
        if temporary:
            temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=HERE/"REPORT_ALIGNMENT_CATALOG.json")
    parser.add_argument("--goal-ledger", type=Path, default=HERE/"goal-ledger.json")
    for repository in REPOSITORIES:
        parser.add_argument("--"+repository+"-report", type=Path, default=HERE/(repository+"-automatic-report.json"))
        parser.add_argument("--"+repository+"-findings", type=Path, default=HERE/(repository+"-configured-findings.json"))
    parser.add_argument("--output", type=Path, default=HERE/"REPORT_ALIGNMENT_RESULTS.json")
    args = parser.parse_args()
    try:
        inputs = _Inputs()
        catalog = inputs.load("catalog", args.catalog)
        validate_catalog(catalog)
        ledger = inputs.load("ledger", args.goal_ledger)
        if ledger.get("kind") != "saved_goal_implementation_tracking_ledger" or ledger.get("goal_count") != 5 or ledger.get("required_obligation_count") != 30:
            raise ValueError("Expected the actual saved five-goal implementation ledger, not its old template or a development approximation")
        results = {}
        for repository in REPOSITORIES:
            report = inputs.load(repository+":report", getattr(args, repository+"_report"))
            findings = inputs.load(repository+":findings", getattr(args, repository+"_findings"))
            results[repository] = repository_results(inputs, repository, report, findings, ledger)
        output = build_alignment(inputs, catalog, results)
        inputs.unchanged()
        write_new(args.output, output)
    except (OSError, ValueError, KeyError, TypeError, IndexError, RecursionError) as error:
        parser.error(str(error))
    print(json.dumps({"output": str(args.output), "sections_preserved": 32, "statements_preserved": 130,
        "reference_count": output["unique_evidence_reference_count"], "whole_report_reproduction_claimed": False,
        "new_functional_pass_rate_computed": False, "detector_or_target_invoked": False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
