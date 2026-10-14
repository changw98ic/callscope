"""Remap the five frozen goals to v11 saved evidence, without running analyzers.

This helper reads CallScope report JSON only. It preserves the original five
claims, thirty required obligations and previous assessment statuses. Rewriting
a source-fact array index requires an exact source/operation identity match;
changed positive field judgments abort publication for explicit review.
"""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OLD = ROOT / "reports/astra-iteration8"
ORIGINAL = ROOT / "reports/astra-iteration4"
VERSION = "saved-goal-evidence-remapper-1"
SNAPSHOT_KEYS = ("id", "project_id", "root", "status", "source_hash", "policy_hash",
                 "analyzer_version", "detector_version", "schema_version", "component_versions")
FACT_SEMANTIC_KEYS = ("selected_field_path", "selected_field_presence",
    "selected_field_shape_closed", "whole_object_shape_closed", "actual_literal_keys",
    "actual_excluded_keys", "exclusions_closed", "copy_model_supported")
FIELD_RULES = ("cpb-astra-field-engine-options", "cpb-astra-field-queue-agent-input",
               "cpb-astra-field-agent-metadata-return")
_INPUT_CACHE, _INPUT_HASHES, _TARGET_HASHES = {}, {}, {}


def sha(path: Path) -> str:
    path = path.resolve()
    if path in _INPUT_HASHES:
        return _INPUT_HASHES[path]
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
        separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def load(path: Path):
    path = path.resolve(strict=True)
    if not path.is_relative_to(ROOT / "reports") or path.suffix != ".json":
        raise ValueError("Read only saved CallScope report JSON.")
    if path not in _INPUT_CACHE:
        raw = path.read_bytes()
        _INPUT_HASHES[path] = hashlib.sha256(raw).hexdigest()
        _INPUT_CACHE[path] = json.loads(raw)
    return _INPUT_CACHE[path]


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def at_pointer(value, pointer):
    for part in pointer.lstrip("/").split("/") if pointer else []:
        part = part.replace("~1", "/").replace("~0", "~")
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def target_digest(artifact, pointer):
    # Loaded summary inputs remain immutable throughout this report operation.
    key = (id(artifact), pointer)
    if key not in _TARGET_HASHES:
        _TARGET_HASHES[key] = digest(at_pointer(artifact, pointer))
    return _TARGET_HASHES[key]


def find_finding(summary, rule_id):
    matches = [(index, finding) for index, finding in enumerate(summary["rule_findings"])
               if finding.get("rule_id") == rule_id]
    if len(matches) != 1:
        raise ValueError(f"Expected one saved finding for {rule_id}; found {len(matches)}.")
    return matches[0]


def details(finding):
    matches = [(index, evidence["details"]) for index, evidence in enumerate(finding["evidence"])
               if "contract_hash" in evidence.get("details", {})]
    if len(matches) != 1:
        raise ValueError("Expected one finite-contract details record.")
    return matches[0]


def fact_identity(fact):
    location = fact.get("location", {})
    return tuple(fact.get(key) for key in ("operation", "owner", "target_graph_node_id")) + tuple(
        location.get(key) for key in ("file", "start_byte", "end_byte", "source_hash", "span_hash"))


def snapshot(summary):
    result = {key: deepcopy(summary[key]) for key in SNAPSHOT_KEYS if key != "component_versions"}
    result["component_versions"] = deepcopy(summary["stats"]["component_versions"])
    return result


def new_ref(summary, finding_index, evidence_index, relative_pointer, origin, interpretation):
    finding = summary["rule_findings"][finding_index]
    detail = finding["evidence"][evidence_index]["details"]
    artifact = "codepatchbay-summary.json"
    pointer = f"/rule_findings/{finding_index}/evidence/{evidence_index}/details{relative_pointer}"
    target = at_pointer(summary, pointer)
    return {"origin": origin, "artifact": artifact, "artifact_sha256": sha(HERE / artifact),
        "json_pointer": pointer, "target_value_sha256": target_digest(summary, pointer),
        "snapshot_id": summary["id"], "finding_id": finding["id"],
        "rule_id": finding["rule_id"], "contract_hash": detail["contract_hash"],
        "interpretation": interpretation}


def append_ref(item, category, ref):
    item[category].append(deepcopy(ref))
    item["witness"].append(deepcopy(ref))


def main():
    previous = load(OLD / "goal-ledger.json")
    ledger = deepcopy(previous)
    template = load(ORIGINAL / "goal-ledger.template.json")
    if sha(ORIGINAL / "GOAL_ACCEPTANCE.md") != ledger["acceptance_contract"]["sha256"]:
        raise ValueError("Frozen goal acceptance contract changed.")
    if sha(ORIGINAL / "goal-ledger.template.json") != ledger["evaluation"]["source_template"]["sha256"]:
        raise ValueError("Frozen original goal template changed.")
    summaries = {name: load(HERE / f"{name}-summary.json")
                 for name in ("codepatchbay", "winwincode")}
    old_summaries = {name: load(OLD / f"{name}-summary.json") for name in summaries}
    freeze = load(HERE / "CORE_FREEZE.json")
    for name, summary in summaries.items():
        old_summary = old_summaries[name]
        if summary["source_hash"] != old_summary["source_hash"] or summary["policy_hash"] != old_summary["policy_hash"]:
            raise ValueError(f"{name}: source or unchanged-policy identity differs.")
        if summary["stats"]["component_versions"]["tool"]["source_hash"] != freeze["tool_identity"]["source_hash"]:
            raise ValueError(f"{name}: scan does not match the current freeze.")

    fact_maps, fact_changes = {}, []
    references = [record for record in walk(ledger)
                  if all(key in record for key in ("artifact", "artifact_sha256", "json_pointer"))]
    for reference in references:
        name = reference["artifact"].removesuffix("-summary.json")
        if name not in summaries:
            raise ValueError("Unexpected formal goal reference artifact.")
        new_summary, old_summary = summaries[name], old_summaries[name]
        pointer = reference["json_pointer"]
        old_target = at_pointer(old_summary, pointer)
        finding_index, finding = find_finding(new_summary, reference["rule_id"])
        evidence_index, detail = details(finding)
        if detail["contract_hash"] != reference["contract_hash"]:
            raise ValueError("The original configured contract changed.")
        suffix = re.sub(r"^/rule_findings/\d+/evidence/\d+/details", "", pointer)
        if suffix == pointer:
            raise ValueError(f"Unsupported original reference shape: {pointer}")
        match = re.fullmatch(r"/source_facts/(\d+)(.*)", suffix)
        if match and isinstance(detail.get("source_facts"), list):
            old_fact_index, tail = int(match.group(1)), match.group(2)
            old_detail = at_pointer(old_summary, pointer.split("/source_facts/")[0])
            old_fact = old_detail["source_facts"][old_fact_index]
            identity = fact_identity(old_fact)
            candidates = [(index, fact) for index, fact in enumerate(detail["source_facts"])
                          if fact_identity(fact) == identity]
            if len(candidates) != 1:
                raise ValueError(f"{reference['rule_id']} old fact {old_fact_index}: expected one exact source identity; found {len(candidates)}.")
            new_fact_index, new_fact = candidates[0]
            remap_key = (name, reference["rule_id"], old_fact_index)
            fact_maps[remap_key] = {"old_index": old_fact_index, "new_index": new_fact_index,
                "rule_id": reference["rule_id"], "source_identity": list(identity)}
            for key in FACT_SEMANTIC_KEYS:
                if key in old_fact and new_fact.get(key) != old_fact[key]:
                    fact_changes.append({"rule_id": reference["rule_id"], "old_index": old_fact_index,
                        "new_index": new_fact_index, "key": key, "old": old_fact[key], "new": new_fact.get(key)})
            suffix = f"/source_facts/{new_fact_index}{tail}"
        new_pointer = f"/rule_findings/{finding_index}/evidence/{evidence_index}/details{suffix}"
        new_target = at_pointer(new_summary, new_pointer)
        if suffix.startswith("/assessments/") and re.fullmatch(r"/assessments/\d+", suffix) and isinstance(old_target, dict):
            for key in ("source_form_relation", "pre_completion_source_form_relation", "selected_field_shape_closed", "field_presence", "whole_object_shape_closed"):
                if key in old_target and new_target.get(key) != old_target[key]:
                    fact_changes.append({"rule_id": reference["rule_id"], "pointer": new_pointer,
                        "key": key, "old": old_target[key], "new": new_target.get(key)})
        reference.update({"artifact_sha256": sha(HERE / reference["artifact"]),
            "json_pointer": new_pointer, "snapshot_id": new_summary["id"],
            "finding_id": finding["id"], "target_value_sha256": target_digest(new_summary, new_pointer)})
    if fact_changes:
        unique = {digest(item): item for item in fact_changes}
        raise ValueError("Saved semantic statements changed and require explicit source review before ledger publication: " + json.dumps(list(unique.values()), ensure_ascii=False))

    snapshot_ids = {old_summaries[name]["id"]: summaries[name]["id"] for name in summaries}
    for record in walk(ledger):
        if record.get("snapshot_id") in snapshot_ids:
            record["snapshot_id"] = snapshot_ids[record["snapshot_id"]]
    for goal in ledger["goals"]:
        original = next(item for item in template["goals"] if item["id"] == goal["id"])
        if goal["claim"] != original["claim"]:
            raise ValueError("Original complete claim changed.")
        name = goal["repository"]
        summary = summaries[name]
        goal["snapshot"] = snapshot(summary)
        for contract in (goal["contract_identity"], *goal["additional_contract_identities"]):
            _, finding = find_finding(summary, contract["rule_id"])
            contract.update({"finding_id": finding["id"], "finding_type": finding["type"],
                "finding_status": finding["status"], "policy_hash": summary["policy_hash"]})
        for obligation, source in zip(goal["obligations"], original["obligations"], strict=True):
            if any(obligation[key] != source[key] for key in ("id", "title", "required", "requirement")):
                raise ValueError("Original required obligation changed.")

    cpb = summaries["codepatchbay"]
    goal = next(item for item in ledger["goals"] if item["id"] == "CPB-01")
    p3 = next(item for item in goal["obligations"] if item["id"] == "CPB-01.P3")
    p4 = next(item for item in goal["obligations"] if item["id"] == "CPB-01.P4")
    relation_sites, retention_sites, field_statuses, field_fact_counts = [], [], Counter(), {}
    for rule_id in FIELD_RULES:
        finding_index, finding = find_finding(cpb, rule_id)
        evidence_index, detail = details(finding)
        field_fact_counts[rule_id] = len(detail["source_facts"])
        for assessment_index, assessment in enumerate(detail["assessments"]):
            field_statuses.update([assessment["source_form_relation"]])
            relative = f"/assessments/{assessment_index}"
            relations = assessment.get("source_relations")
            if not isinstance(relations, dict) or not relations.get("version"):
                raise ValueError("Current saved field site has no authenticated source-relations record.")
            site_location = assessment["site_location"]
            relation_location = relations.get("site_location", {})
            if any(relation_location.get(key) != site_location.get(key) for key in
                    ("file", "start_byte", "end_byte", "source_hash", "span_hash")):
                raise ValueError("Source structure relations belong to a different selected AST site.")
            if relations.get("proof_domain") != "captured_ast_and_lexical_binding":
                raise ValueError("A new semantic relation domain requires independent scope review.")
            if any(relations.get(key) is not False for key in
                   ("selected_heap_projection_upgraded", "runtime_value_verified",
                    "original_parameter_value_identity_proven", "promise_fulfillment_proven")):
                raise ValueError("Source structure relations improperly promote a value/heap/Promise judgment.")
            relation_ref = new_ref(cpb, finding_index, evidence_index, relative + "/source_relations", "source-derived",
                "实际保存AST/词法声明/目标位置生成的局部结构关系；区分实参形参接线、当前binding引用、别名、ordered spread和显式写键扫描。只有原源码范围和声明身份闭合，不认证入口heap、运行值、Set/callee effects、fulfilled或运输。")
            obligation = p4 if rule_id == FIELD_RULES[0] else p3
            for item in (obligation, goal):
                append_ref(item, "source", relation_ref)
            relation_sites.append(relation_ref)
            for retention_index, retention in enumerate(assessment.get("local_copy_retention", [])):
                witness = retention.get("witness", {})
                if witness.get("supported") is not True:
                    continue
                if rule_id != FIELD_RULES[2] or site_location.get("line") != 489:
                    raise ValueError("A new supported copy site needs separate claim-scope review.")
                if witness.get("record") != "CopyRetentionWitness" or witness.get("observation", {}).get("selected_key") != "maxRetries":
                    raise ValueError("Unexpected current-copy-time typed witness identity.")
                if witness.get("later_definition_keys") != ["agents", "agent"]:
                    raise ValueError("Current-copy-time suffix does not match the reviewed real object literal.")
                if any(retention.get(key) is not False for key in
                       ("initial_parameter_origin_proven", "presence_proven", "runtime_value_verified",
                        "fulfilled_value_proven", "transport_proven")):
                    raise ValueError("Copy-time conditional witness improperly promotes initial origin/presence/runtime/Promise/transport.")
                retention_ref = new_ref(cpb, finding_index, evidence_index,
                    relative + f"/local_copy_retention/{retention_index}", "trusted-model",
                    "在实际whole-surface copy正常完成且该时刻自有可枚举maxRetries存在的条件下，fresh私有字面对象的后续固定agents/agent定义不改写该键，复制时值/引用保留到该字面对象结束。来源只从copy时刻起算；不证明入口metadata字段、presence、嵌套内容、async fulfilled、activation或运输，不修复原source projection未知。")
                for item in (p3, goal):
                    append_ref(item, "model", retention_ref)
                retention_sites.append(retention_ref)
    if len(relation_sites) != 5:
        raise ValueError("Expected all five originally selected field sites, without changing the denominator.")
    if len(retention_sites) != 1:
        raise ValueError("Expected one reviewed current-copy-time conditional retention witness.")
    p3_note = "正式保存五处AST/词法来源关系，queue的显式metadata子键写入和agent别名/当前return绑定分开报告；agent字面return的实际copy-time maxRetries若存在可保留到literal endpoint。四个原endpoint仍unknown；入口字段、shared child/Set effects、async fulfilled及new-existing/scheduler/assignment/JSON/inbox/broker运输未闭合。"
    p3["assessment"]["reason"] = p3_note
    p3["gaps"][0]["reason"] = p3_note
    for gap in goal["gaps"]:
        if gap["obligation_id"] == "CPB-01.P3":
            gap["reason"] = p3_note

    evaluation = ledger["evaluation"]
    evaluation["snapshots"] = [snapshot(summary) for summary in summaries.values()]
    evaluation["implementation"] = {"package_version": freeze["package_version"],
        "schema_version": freeze["schema_version"], "analyzer_version": freeze["analyzer_version"],
        "detector_version": freeze["detector_version"], "source_hash": freeze["tool_identity"]["source_hash"]}
    inventory = [(f"{name}-summary.json", "formal_saved_automatic_evidence") for name in summaries]
    inventory += [(f"{name}-baseline-v11-and-v10.json", "separate_frozen_observation_comparison") for name in summaries]
    inventory.append(("CORE_FREEZE.json", "formal_implementation_identity"))
    evaluation["artifact_inventory"] = [{"path": name, "sha256": sha(HERE / name), "role": role} for name, role in inventory]
    evaluation["excluded_from_automatic_witnesses"] += ["PREFREEZE_SOURCE_REVIEW.md", "IR_DOMAIN_REVIEW.md", "RELATION_DESIGN.md"]
    evaluation["reason"] = "保留原五claim/30义务及评审类别，人工核对正式v11保存证据；旧数组事实按operation/owner/target与原源码hash/span唯一重映射，新增source关系和copy-time条件见证单列，不用开发观察补正式结果。"
    evaluation["remapped_indexed_field_fact_count"] = len(fact_maps)
    evaluation["indexed_field_fact_mappings"] = list(fact_maps.values())
    evaluation["field_source_relation_delta"] = {"original_obligation": "CPB-01.P3",
        "obligation_status_changed": False, "source_relation_sites": relation_sites,
        "local_copy_retention_sites": retention_sites, "source_structure_site_count": len(relation_sites),
        "current_copy_time_retention_site_count": len(retention_sites),
        "entry_parameter_origin_proven": False, "field_presence_proven": False,
        "fulfilled_value_proven": False, "transport_proven": False,
        "full_goal_supported": False, "counts_are_not_goal_coverage": True}
    old_delta = evaluation.pop("field_precision_delta")
    evaluation["retained_v10_field_scope"] = old_delta
    evaluation["report_remapper"] = {"version": VERSION, "source_sha256": sha(Path(__file__)),
        "source_ledger": "../astra-iteration8/goal-ledger.json", "source_ledger_sha256": sha(OLD / "goal-ledger.json"),
        "automatic_assessment_performed": False, "target_code_imported_or_executed": False,
        "analyzer_executed": False, "tests_run": False}
    ledger["assessment"]["field_path_assessment_counts"] = dict(field_statuses)
    ledger["assessment"]["field_source_fact_counts"] = field_fact_counts
    ledger["assessment"].update({"captured_source_relation_sites": len(relation_sites),
        "current_copy_time_retention_sites_supported": len(retention_sites),
        "local_copy_retention_is_not_entry_source_or_transport": True,
        "field_transport_goal_achieved": False})
    ledger["interpretation"] = "原五claim/30必要义务定义、顺序及required完整保留。v11新增实际保存源码的结构关系与agent return的copy-time局部条件见证，P3仍partial；engine既有正常前缀来源形式范围保持。四个原field endpoint仍unknown，五个完整目标仍0/5。来源事实、selected site、copy-time条件见证与原26调用观察均不是目标覆盖或通过率。"
    statuses = Counter(obligation["assessment"]["status"] for item in ledger["goals"] for obligation in item["obligations"])
    if dict(statuses) != ledger["assessment"]["obligation_status_counts"]:
        raise ValueError("Frozen prior obligation assessment counts changed.")
    checked = 0
    for reference in walk(ledger):
        if not all(key in reference for key in ("artifact", "artifact_sha256", "json_pointer")):
            continue
        artifact = load(HERE / reference["artifact"])
        target = at_pointer(artifact, reference["json_pointer"])
        if sha(HERE / reference["artifact"]) != reference["artifact_sha256"] or target_digest(artifact, reference["json_pointer"]) != reference["target_value_sha256"]:
            raise ValueError("Final reference content identity mismatch.")
        checked += 1
    evaluation["references_checked_during_authoring"] = checked
    if any(hashlib.sha256(path.read_bytes()).hexdigest() != expected for path, expected in _INPUT_HASHES.items()):
        raise ValueError("A saved input changed while authoring the ledger.")
    evaluation["saved_inputs_stable_during_authoring"] = True
    output = HERE / "goal-ledger.json"
    if output.exists():
        raise ValueError("Refuse to overwrite an existing final ledger.")
    output.write_text(json.dumps(ledger, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"artifact": str(output), "sha256": sha(output), "references": checked,
        "indexed_facts_remapped": len(fact_maps), "obligation_status_counts": dict(statuses),
        "complete_goals": 0, "source_relation_sites": len(relation_sites),
        "current_copy_time_retention_sites": len(retention_sites)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
