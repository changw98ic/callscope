"""Locator-only policy wrapper for finite selected-field source summaries."""

from __future__ import annotations

from collections import Counter
from typing import Any

from .models import Evidence, Finding, GraphSnapshot
from .field_summaries import summarize_field, VERSION as SUMMARY_VERSION, MODEL_ID, READ_MODEL_ID
from .static_contracts import _digest, _issue, _path, _string
from .value_analysis import _json_data

VERSION = "static-field-contracts-4-ir"
POLICY_VERSION = "static-field-policy-v2"


def _field_path(value: Any) -> bool:
    return isinstance(value, list) and 0 < len(value) <= 8 and all(_string(part) and len(part) <= 256 and "\\" not in part for part in value)


def validate_field_rule(rule: Any) -> None:
    _json_data(rule)
    if not isinstance(rule, dict) or set(rule) != {"id", "type", "severity", "subject", "sink", "evaluation", "models", "provenance", "applicability"}:
        raise ValueError("field_contracts 仅接受固定主体/终点字段 locators、模型、来源与条件。")
    if not _string(rule["id"]) or rule["type"] != "parameter_field_flow" or not isinstance(rule["severity"], str) or rule["severity"] not in {"high", "medium", "low", "info"}:
        raise ValueError("字段合同 id/type/severity 无效。")
    subject = rule["subject"]
    if not isinstance(subject, dict) or set(subject) != {"file", "symbol", "parameter_index", "field_path"} or not _path(subject["file"]) or not _string(subject["symbol"]) or type(subject["parameter_index"]) is not int or not 0 <= subject["parameter_index"] <= 32 or not _field_path(subject["field_path"]):
        raise ValueError("subject 需要项目内 file、精确 symbol、parameter_index、field_path；不能配置中间传播链。")
    sink = rule["sink"]
    if not isinstance(sink, dict) or not _field_path(sink.get("field_path")):
        raise ValueError("sink 需要 selected field_path。")
    if sink.get("kind") == "call_argument":
        if set(sink) != {"kind", "callee", "argument_index", "field_path"} or not _string(sink["callee"]) or any(not part.replace("$", "_").isidentifier() for part in sink["callee"].split(".")) or type(sink["argument_index"]) is not int or not 0 <= sink["argument_index"] <= 32:
            raise ValueError("call_argument sink 需要唯一源码 callee selector、argument_index、field_path。")
    elif sink.get("kind") == "return":
        if set(sink) != {"kind", "field_path"}:
            raise ValueError("return sink 不可填返回结果/字段集合/预制证明。")
    else:
        raise ValueError("sink.kind 仅支持 call_argument 或 return。")
    if rule["evaluation"] != "all_direct_sites" or rule["models"] not in ([MODEL_ID], [MODEL_ID, READ_MODEL_ID]):
        raise ValueError("仅支持 all_direct_sites 与显式固定版本 own-enumerable-field-copy 模型。")
    provenance = rule["provenance"]
    if not isinstance(provenance, dict) or set(provenance) - {"authority", "reviewer", "author_approved", "source_doc", "note"} or not _string(provenance.get("authority")) or not _string(provenance.get("source_doc")) or type(provenance.get("author_approved")) is not bool:
        raise ValueError("provenance 仅是来源标签，不读取 source_doc 或将评审说明当工具证明。")
    applicability = rule["applicability"]
    if not isinstance(applicability, dict) or set(applicability) - {"kind", "conditions", "counterexamples"} or applicability.get("kind") != "conditional" or not isinstance(applicability.get("conditions"), list) or not applicability["conditions"] or not all(_string(item) for item in applicability["conditions"]):
        raise ValueError("字段合同必须保留明确 conditional 适用条件。")
    if not isinstance(applicability.get("counterexamples", []), list) or not all(_string(item) for item in applicability.get("counterexamples", [])):
        raise ValueError("反证只能是说明文本，不填机器键集合/证明路径。")


def _finding(snapshot: GraphSnapshot, rule: dict, summary: dict) -> Finding:
    fingerprint = _digest({"version": VERSION, "summary_version": SUMMARY_VERSION, "policy_version": POLICY_VERSION,
        "project": snapshot.project_id, "rule": rule})
    nodes = {node.id for node in snapshot.nodes}
    edges = {edge.id for edge in snapshot.edges}
    node_ids = sorted(({summary.get("subject_graph_node_id", "")} | {fact.get(key, "") for fact in summary.get("source_facts", [])
        for key in ("graph_node_id", "target_graph_node_id")}) & nodes)
    edge_ids = sorted(({fact.get("edge_id", "") for fact in summary.get("source_facts", [])}
        | {site.get("edge_id", "") for site in summary.get("assessments", [])}) & edges)
    counts = Counter(site.get("source_form_relation", "unknown") for site in summary.get("assessments", []))
    relation_counts = Counter(relation["kind"] for site in summary.get("assessments", [])
        for relation in site.get("source_relations", {}).get("relations", []))
    local_copy_count = sum(bool(site.get("local_copy_retention_supported")) for site in summary.get("assessments", []))
    details = {**summary, "field_analyzer_version": VERSION, "policy_version": POLICY_VERSION,
        "policy_hash": snapshot.policy_hash, "contract_hash": _digest(rule), "assessment_counts": dict(sorted(counts.items())),
        "source_relation_counts": dict(sorted(relation_counts.items())), "local_copy_retention_supported_site_count": local_copy_count,
        "provenance": rule.get("provenance", {}), "applicability": rule.get("applicability", {}),
        "interpretation": "每个合同仅其所选段；源式形式不等于运行值保留，多个规则不能相加证明消息/跨进程全链"}
    locations = [fact["location"] for fact in summary.get("source_facts", []) if fact.get("location")]
    evidence = Evidence(_digest({"snapshot": snapshot.id, "fingerprint": fingerprint, "details": details})[:24],
        "static_field_analysis", "参数字段来源形式摘要与模型/完成态/效果缺口。", locations, node_ids, edge_ids, details)
    return Finding(_digest({"snapshot": snapshot.id, "fingerprint": fingerprint})[:24], "static_parameter_field_flow",
        rule.get("severity", "info"), "uncertain", "参数字段来源摘要待复核", "有限对象复制、真实绑定和返回段独立评估；字段存在性与运行值仍需按条件审阅。",
        node_ids, edge_ids, [evidence], rule.get("id", "invalid-field-rule"), fingerprint, snapshot.id,
        {"field_analyzer_version": VERSION, "field_summary_version": SUMMARY_VERSION, "assessment_counts": dict(sorted(counts.items())),
            "source_relation_counts": dict(sorted(relation_counts.items())), "local_copy_retention_supported_site_count": local_copy_count,
            "selected_field_shape_complete": summary.get("selected_shape_complete", False), "source_form_complete": summary.get("source_form_complete", False),
            "reaching_value_origin_proven": False, "transport_proven": False, "full_functionality_proven": False,
            "assessment_count": len(summary.get("assessments", [])), "provenance": rule.get("provenance", {}), "applicability": rule.get("applicability", {})})


def analyze_field_contracts(snapshot: GraphSnapshot, rules: list[dict]) -> list[Finding]:
    """Always return an assessment finding for valid configured endpoints."""
    if not isinstance(rules, list):
        return [_finding(snapshot, {"id": "invalid-field-contracts", "severity": "info"},
            {"analysis_gaps": [_issue("field_rules_invalid", "field_contracts 必须是列表。")], "assessments": []})]
    counts = Counter(rule.get("id") for rule in rules if isinstance(rule, dict) and isinstance(rule.get("id"), str))
    findings = []
    for index, rule in enumerate(rules):
        try:
            validate_field_rule(rule)
            if counts[rule["id"]] != 1:
                raise ValueError("字段合同 ID 重复，不能覆盖。")
        except (ValueError, TypeError, RecursionError, OverflowError) as error:
            findings.append(_finding(snapshot, {"id": f"invalid-field-rule-{index}", "severity": "info"},
                {"analysis_gaps": [_issue("field_rule_invalid", str(error))], "assessments": []}))
            continue
        subject = rule["subject"]
        summary = summarize_field(snapshot, {"file": subject["file"], "symbol": subject["symbol"]},
            parameter_index=subject["parameter_index"], field_path=subject["field_path"], sink=rule["sink"], models=rule["models"])
        findings.append(_finding(snapshot, rule, summary))
    return findings
