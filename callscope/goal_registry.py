"""Data-only whole-judgment adapters with explicit necessary obligations.

An adapter's local relation is never sufficient to complete a goal. This
registry retains every required obligation and exposes incomplete judgments.
Target programs, tests and builds are never invoked.
"""
from __future__ import annotations

from dataclasses import asdict
from importlib import import_module
from typing import Any

from .models import Evidence, Finding, GraphSnapshot
from .static_contracts import _digest, _string
from .value_analysis import _json_data

VERSION = "static-whole-judgment-registry-1"
POLICY_VERSION = "static-goal-policy-v1"
_ADAPTERS = {
    "status": ("status_analysis", "validate_status_rule", "analyze_status_contracts", ("S1", "S2", "S3", "S4", "S5")),
    "pipeline": ("pipeline_flow", "validate_pipeline_flow_rule", "analyze_pipeline_flows", ("P1", "P2", "P3", "P4", "P5", "P6")),
    "navigation": ("navigation_completion", "validate_navigation_completion_rule", "analyze_navigation_completions", ("N1", "N2", "N3", "N4", "N5", "N6", "N7")),
    "device": ("device_flow", "validate_device_flow_rule", "analyze_device_flows", ("D1", "D2", "D3", "D4", "D5")),
    "atomicity": ("atomicity_completion", "validate_atomicity_completion_rule", "analyze_atomicity_completions", ("A1", "A2", "A3", "A4", "A5", "A6", "A7")),
}


def _adapter(name: str):
    module, validator, analyze, obligations = _ADAPTERS[name]
    implementation = import_module("." + module, __package__)
    return implementation, getattr(implementation, validator), getattr(implementation, analyze), obligations


def validate_goal_rule(rule: Any) -> None:
    _json_data(rule)
    if not isinstance(rule, dict) or set(rule) != {"id", "goal_id", "analyzer", "contract"}:
        raise ValueError("goal_contracts require id/goal_id/analyzer/contract; results and intermediate proofs are not configurable")
    if not _string(rule["id"]) or not _string(rule["goal_id"]) or not isinstance(rule["analyzer"],str) or rule["analyzer"] not in _ADAPTERS:
        raise ValueError("Invalid whole-judgment identity or fixed analyzer")
    if not isinstance(rule["contract"], dict) or rule["contract"].get("id") != rule["id"]:
        raise ValueError("Inner contract identity must match the registered goal rule")
    _, validate, _, _ = _adapter(rule["analyzer"])
    validate(rule["contract"])


def component_versions(rules: list[dict]) -> dict:
    result = {"registry": VERSION, "policy_schema": POLICY_VERSION, "adapters": {}}
    for name in sorted({rule["analyzer"] for rule in rules}):
        implementation, _, _, _ = _adapter(name)
        result["adapters"][name] = {"analyzer": implementation.VERSION,
            "policy_schema": getattr(implementation, "POLICY_VERSION", "adapter-validated-v1")}
    return result


def _registered(snapshot: GraphSnapshot, rule: dict, findings: list[Finding], required: tuple[str, ...]) -> Finding:
    records = [asdict(finding) for finding in findings]
    details = [evidence.details for finding in findings for evidence in finding.evidence]
    summaries = [detail for detail in details if "obligations" in detail]
    summary = summaries[0] if len(summaries) == 1 else {}
    registry_gaps = []
    expected_identity = {"snapshot_id":snapshot.id,"source_hash":snapshot.source_hash,
        "policy_hash":snapshot.policy_hash,"contract_hash":_digest(rule["contract"])}
    identity_matches = all(summary.get(key)==value for key,value in expected_identity.items())
    if not identity_matches:
        registry_gaps.append({"code":"goal_adapter_context_identity_invalid"})
    obligations = summary.get("obligations", [])
    if isinstance(obligations, dict):
        mapping_valid = all(isinstance(value,dict) and value.get("id",key)==key for key,value in obligations.items())
        obligations = [{**value,"id":key} for key,value in obligations.items()] if mapping_valid else []
    if not isinstance(obligations, list) or any(not isinstance(item,dict) or not _string(item.get("id")) for item in obligations):
        obligations = []
    identifiers = [item["id"] for item in obligations]
    accounted = len(identifiers) == len(required) and set(identifiers) == set(required)
    if not accounted:
        registry_gaps.append({"code":"goal_required_obligation_identity_incomplete"})
    necessary_gaps = summary.get("necessary_gaps")
    gaps_explicit = isinstance(necessary_gaps,list)
    if not gaps_explicit:
        registry_gaps.append({"code":"goal_necessary_gap_certificate_missing"})
    obligation_gap_free = all(isinstance(item.get("necessary_gaps",item.get("gaps")),list)
        and not item.get("necessary_gaps",item.get("gaps")) for item in obligations)
    if not obligation_gap_free:
        registry_gaps.append({"code":"goal_obligation_necessary_gap_unclosed"})
    analysis_gaps = summary.get("analysis_gaps",[])
    if not isinstance(analysis_gaps,list) or analysis_gaps:
        registry_gaps.append({"code":"goal_adapter_analysis_gap_unclosed"})
    for label in ("coverage","source_budget","analysis_budget","budget"):
        coverage = summary.get(label,{})
        if not isinstance(coverage,dict) or any(coverage.get(flag,False) for flag in ("incomplete","truncated","budget_exceeded","exhausted")):
            registry_gaps.append({"code":"goal_adapter_coverage_incomplete","field":label})
    # Adapters must still certify their source/model applicability. A complete
    # list of labels or boolean set in policy never supplies that certificate.
    complete = bool(accounted and all(isinstance(item.get("status"),str) and item["status"] in {"supported","refuted"} for item in obligations)
        and summary.get("complete_assessment") is True and gaps_explicit and not necessary_gaps and not registry_gaps)
    supported = bool(complete and all(item.get("status") == "supported" for item in obligations)
        and summary.get("full_goal_supported") is True)
    assessment = "scoped_static_judgment_reproduced" if supported else summary.get("assessment", "unknown_or_source_invalid")
    if not supported and assessment == "scoped_static_judgment_reproduced":
        assessment = "partial_obligations_supported"
    if complete and not supported and assessment != "claim_refuted_or_narrowed":
        complete = False
    payload = {"version": VERSION, "policy_version": POLICY_VERSION, "goal_id": rule["goal_id"],
        "analyzer": rule["analyzer"], "snapshot_id": snapshot.id, "source_hash": snapshot.source_hash,
        "policy_hash": snapshot.policy_hash, "contract_hash": _digest(rule),
        "required_obligation_ids": list(required), "necessary_obligations_accounted": accounted,
        "obligations": obligations, "assessment": assessment, "full_goal_supported": supported,
        "complete_assessment": complete,
        "adapter_context_identity_matches":identity_matches,
        "adapter_judgments": records, "conditions": summary.get("conditions", []),
        "refutations": summary.get("refutations", summary.get("counterexamples", [])),
        "necessary_gaps": [*(necessary_gaps if gaps_explicit else []),*registry_gaps],
        "original_claim": summary.get("original_claim"), "derived_judgment": summary.get("derived_judgment"),
        "target_executed": False, "target_tests_run": False, "target_build_run": False}
    locations = [location for finding in findings for evidence in finding.evidence for location in evidence.locations]
    nodes = sorted({node for finding in findings for node in finding.node_ids})
    edges = sorted({edge for finding in findings for edge in finding.edge_ids})
    fingerprint = _digest({"version": VERSION, "project": snapshot.project_id, "rule": rule})
    evidence = Evidence(_digest({"snapshot": snapshot.id, "fingerprint": fingerprint, "details": payload})[:24],
        "static_whole_judgment", "必要源码关系及模型适用性逐项评估。", locations, nodes, edges, payload)
    return Finding(_digest({"snapshot": snapshot.id, "fingerprint": fingerprint})[:24], "static_goal_judgment",
        "info", "uncertain", "完整静态条件判断" if supported else "完整静态反驳或收窄" if complete else "静态判断尚有必要缺口",
        "在声明范围内逐项核对；完整字段、分派、控制、保护关系不能由局部事实替代。",
        nodes, edges, [evidence], rule["id"], fingerprint, snapshot.id,
        {"goal_id": rule["goal_id"], "analyzer": rule["analyzer"], "full_goal_supported": supported,
            "complete_assessment": complete,
            "assessment": assessment, "required_obligation_count": len(required),
            "necessary_obligations_accounted": accounted, "runtime_value_verified": False})


def analyze_goal_contracts(snapshot: GraphSnapshot, rules: list[dict]) -> list[Finding]:
    findings = []
    for rule in rules:
        validate_goal_rule(rule)
        _, _, analyze, required = _adapter(rule["analyzer"])
        findings.append(_registered(snapshot,rule,analyze(snapshot,[rule["contract"]]),required))
    return findings
