"""Explain finite architectural work from authenticated captured operations.

Directory names, method-name resemblance and benchmark prose supply no facts.
The reusable operation extractor owns CST, writer and binding analysis. This
module turns its actual operations and explicit relationships into bounded
human-readable explanations with evidence pointers and preserved unknowns.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import json
from typing import Any

VERSION = "captured-architecture-responsibilities-1"
_KINDS = frozenset({"record_construction", "record_field_projection", "record_copy_projection",
    "field_write", "call_argument_transfer", "protocol_literal_field", "guard_rejection",
    "return_transfer", "normal_source_order", "binding_initializer", "binding_update"})
_RELATIONS = frozenset({"lexical_value_to_argument", "record_literal_as_argument",
    "field_projection_from_record", "explicit_return_value", "normal_source_before",
    "authenticated_argument_parameter_projection"})
_DISPLAY = {"statements_per_declaration": 24, "relationship_examples": 384,
    "field_examples": 12, "source_characters": 360, "reuse_examples": 128}

# These labels are navigation over existing evidence contexts, not a classifier
# or a source of responsibility assertions. Every body statement below is built
# from an actual operation, independent of the label or the project's name.
_NAVIGATION = (
    ("cpb-entry", "命令参数、提交与结果投影", ("CPB-01", "CPB-03", "cpb-report-readiness-abrupt-guard")),
    ("cpb-orchestration", "候选、assignment、attempt 与 worker 接线", ("CPB-01", "cpb-report-conditional-delivery-result")),
    ("cpb-engine", "引擎上下文端口、阶段与完成条件", ("CPB-01", "cpb-report-engine-stage-chain", "cpb-report-completion-gate-conditions")),
    ("cpb-evidence", "结构化证据、命令来源与消费", ("cpb-report-trusted-probe-command-source", "cpb-report-unsupported-probe-evidence",
        "cpb-trusted-command-lineage", "cpb-unsupported-record-retention", "cpb-report-completion-gate-conditions")),
    ("cpb-storage", "事件、服务实现、交付与投影", ("CPB-02", "cpb-event-index-projection", "cpb-report-conditional-delivery-result",
        "cpb-captured-record-resource-writers")),
    ("cpb-policy", "Agent、审计与配置分支", ("cpb-report-agent-execution-policy", "cpb-report-access-audit-response",
        "cpb-report-job-audit-best-effort")),
    ("wwc-client", "浏览器表现、上下文与请求形状", ("WWC-01", "WWC-02", "wwc-browser-continuation-lifecycle",
        "wwc-report-chat-delivery-workrun-requests", "wwc-report-chat-retained-request-identities")),
    ("wwc-product", "产品状态与有限拒绝条件", ("WWC-02", "wwc-report-workrun-state-guards", "wwc-report-workrun-finite-selection",
        "wwc-captured-record-resource-writers")),
    ("wwc-worker", "Worker 执行记录、控制消息与装配", ("wwc-report-worker-bootstrap-entries", "wwc-report-worker-production-construction",
        "wwc-report-worker-typed-dispatch", "wwc-report-worker-adapter-record-identities")),
    ("wwc-kernel", "adapter 持久记录与 Kernel 接口", ("wwc-report-production-adapter-embedded-kernel",
        "wwc-report-adapter-durable-exact-turn", "wwc-report-submission-intent-kernel-order",
        "wwc-report-kernel-create-session-interface", "wwc-report-kernel-submit-turn-interface",
        "wwc-report-kernel-reconcile-exact-interface", "wwc-report-outbox-ack-correlation-fields")),
    ("wwc-device", "Device 与 provider 的条件装配", ("WWC-02", "wwc-report-device-provider-deployment")),
)


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True,
        separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def _dict(value: Any) -> dict:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list:
    return value if isinstance(value, list) else []


def _clip(value: Any, *, limit: int | None = None) -> str:
    if value is None:
        return "未保存"
    if isinstance(value, dict):
        for key in ("source_text", "name", "symbol", "source_path"):
            if key in value and value[key] is not None:
                return _clip(value[key], limit=limit)
        value = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    elif isinstance(value, list):
        value = ".".join(_clip(item, limit=80) for item in value)
    elif not isinstance(value, str):
        value = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    value = value.replace("\r", "\\r").replace("\n", "\\n")
    bound = _DISPLAY["source_characters"] if limit is None else limit
    return value if len(value) <= bound else value[:bound] + "…［展示截断；完整操作保留］"


def _owner_label(operation: dict) -> str:
    owner = _dict(operation.get("actual_owner"))
    location = _dict(owner.get("location"))
    file = owner.get("file") or location.get("file")
    symbol = owner.get("symbol") or owner.get("graph_node_id")
    return str(file or "位置未保留") + "::" + str(symbol or "声明未唯一识别")


def _binding_path(operation: dict) -> str:
    operands, subject = _dict(operation.get("operands")), operation.get("subject")
    if isinstance(subject, str) and subject:
        return _clip(subject)
    if isinstance(subject, dict):
        target = _dict(subject.get("target_path")) or _dict(subject.get("source_path"))
        if target.get("root_name") is not None:
            return _clip([target["root_name"], *_list(target.get("member_path"))])
        if subject.get("field_name") is not None:
            return _clip(subject["field_name"])
        for key in ("source_text", "source_path", "name"):
            if subject.get(key) is not None:
                return _clip(subject[key])
    binding = _dict(operands.get("binding"))
    root = binding.get("name") or binding.get("source_text")
    path = operands.get("member_path")
    if root and isinstance(path, list):
        return _clip([root, *path])
    if path:
        return _clip(path)
    return _clip(operands.get("source_text"))


def _operation_text(operation: dict) -> tuple[str, list[dict]]:
    kind, operands = operation.get("operation_kind"), _dict(operation.get("operands"))
    source = _clip(operands.get("source_text"))
    gaps = []
    if kind == "record_construction":
        fields = _list(operands.get("record_fields"))
        examples = []
        for field in fields[:_DISPLAY["field_examples"]]:
            item = _dict(field)
            name = _clip(item.get("name"))
            value = _clip(item.get("source_text"), limit=160)
            examples.append(name + " ← " + value)
        if examples:
            suffix = "；其余字段见完整操作" if len(fields) > len(examples) else ""
            return "构造捕获记录，字段按源码次序为「" + "；".join(examples) + "」" + suffix + "。不据构造形式推断物理持久化。", gaps
        if not fields and operands.get("closed_captured_shape") is True:
            return "构造捕获的空记录「" + source + "」；没有从空记录形式推断额外字段或持久效果。", gaps
        return "具有捕获记录构造「" + source + "」；该记录的可枚举字段为空或保留开放形状，未把展开来源补成确定字段。", gaps
    if kind == "record_field_projection":
        return "以字段投影形式「" + source + "」关联路径「" + _binding_path(operation) + "」；只描述捕获来源，不证明当时的字段值。", gaps
    if kind == "record_copy_projection":
        return "保留记录复制/展开来源「" + source + "」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。", gaps
    if kind == "field_write":
        return "包含赋值/更新「" + source + "」，捕获目标为「" + _binding_path(operation) + "」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。", gaps
    if kind == "binding_initializer":
        value = _dict(operands.get("value"))
        return "捕获 binding「" + _binding_path(operation) + "」的初始化来源为「" + _clip(value.get("source_text")) + "」；保留该声明与初始化表达式，不推任意后续读取的当前值。", gaps
    if kind == "binding_update":
        return "对捕获 binding「" + _binding_path(operation) + "」存在源更新「" + source + "」；循环和分支条件见操作上下文，未推执行次数或最终数值。", gaps
    if kind == "call_argument_transfer":
        callee = _dict(operands.get("callee"))
        index = operands.get("argument_index")
        argument = _dict(operands.get("argument"))
        source = _clip(argument.get("source_text"))
        empty_call = operands.get("argument_count") == 0 and index is None and operands.get("argument") is None
        position = "第 " + str(index + 1) + " 个实参" if isinstance(index, int) and not isinstance(index, bool) and index >= 0 else "实参（位置未保存）"
        if not empty_call and (not isinstance(index, int) or isinstance(index, bool) or index < 0):
            gaps.append({"code": "call_argument_position_unavailable"})
        authenticated = (callee.get("binding_state") == "authenticated_internal_call"
            and isinstance(callee.get("target_graph_node_id"), str) and bool(callee["target_graph_node_id"]))
        destination = callee.get("target_symbol") or callee.get("source_text")
        if empty_call:
            return ("以无显式实参的调用形式「" + _clip(callee.get("source_text")) + "」调用" +
                ("已绑定接口「" + _clip(destination) + "」" if authenticated else "尚未唯一绑定的目标") +
                "；没有据调用存在断言激活、存储或网络效果。"), gaps
        if authenticated:
            formal = _dict(operands.get("target_parameter"))
            suffix = "，对应捕获形参「" + _clip(formal["source_text"]) + "」" if formal.get("source_text") else ""
            return "将「" + source + "」作为" + position + "交给已绑定接口「" + _clip(destination) + "」" + suffix + "。该普通调用关系不替代进程或网络协议关系。", gaps
        return "在调用形式「" + _clip(callee.get("source_text")) + "」中提供" + position + "「" + source + "」；目标绑定为「" + _clip(callee.get("binding_state")) + "」，不指定唯一实现或物理效果。", gaps
    if kind == "protocol_literal_field":
        return "记录消息形状中的固定文本字段「" + _binding_path(operation) + "」及捕获形式「" + source + "」。单个文本字段不是跨语言调用或传输成功的证明。", gaps
    if kind == "guard_rejection":
        condition, exit_kind = operands.get("condition_source"), operands.get("exit_kind")
        if condition is None or exit_kind not in {"return", "throw", "Err_return"}:
            gaps.append({"code": "guard_condition_or_abrupt_kind_unavailable"})
        return "条件「" + _clip(condition) + "」的捕获提前退出分支为「" + _clip(exit_kind) + "：" + _clip(operands.get("exit_source")) + "」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。", gaps
    if kind == "return_transfer":
        return "以「" + source + "」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。", gaps
    if kind == "normal_source_order":
        return ("保留同一块中的正常源码顺序：语句位置「" + _clip(operands.get("before_statement_index")) +
            "」的操作「" + _clip(operands.get("before_operation_id")) + "」先于语句位置「" +
            _clip(operands.get("after_statement_index")) + "」的操作「" + _clip(operands.get("after_operation_id")) +
            "」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。"), gaps
    return "该操作类型尚无职责解释模板，完整源记录保留。", [{"code": "responsibility_operation_kind_not_supported", "operation_kind": kind}]


def _operation_reference(operation: dict, index: int) -> dict:
    pointer = "/operations/" + str(index)
    anchors = [{key: value for key, value in location.items() if key in {"file", "line", "column", "start_byte",
        "end_byte", "location_ref"}} for location in _list(operation.get("source_locations")) if isinstance(location, dict)]
    return {"operation_id": operation.get("id"), "operation_pointer": pointer,
        "operation_pointer_scope": "this_responsibility_explanation_object",
        "source_evidence_refs_pointer": pointer + "/source_evidence_refs",
        "source_locations_pointer": pointer + "/source_locations", "source_locations": anchors}


def _owner_key(operation: dict) -> tuple:
    owner = _dict(operation.get("actual_owner"))
    location = _dict(owner.get("location"))
    if location.get("file") and isinstance(location.get("start_byte"), int) and isinstance(location.get("end_byte"), int):
        return (str(location["file"]), str(location.get("source_hash", "")), location["start_byte"], location["end_byte"],
            str(owner.get("graph_node_id") or ""))
    if location.get("file") and isinstance(location.get("location_ref"), str):
        return (str(location["file"]), "location_ref", location["location_ref"], "", str(owner.get("graph_node_id") or ""))
    # An unresolved owner must not merge merely because names resemble.
    return (str(owner.get("file") or ""), "unknown", -1, -1, str(operation.get("id")))


def _statement(operation: dict, index: int) -> dict:
    text, gaps = _operation_text(operation)
    return {"id": _digest([VERSION, "statement", operation.get("id")])[:24],
        "text": text, "operation_kind": operation.get("operation_kind"),
        **_operation_reference(operation, index), "source_gaps": gaps,
        "statement_basis": "authenticated_captured_operation_and_explicit_source_conditions",
        "guards": operation.get("guards", []), "source_order": operation.get("source_order", []),
        "limitations": operation.get("limitations", []), "runtime_effect_proven": False}


def _presentation_rank(operation: dict, selected_targets: set[str]) -> tuple:
    """Prefer explicit interfaces and values using source structure alone.

    This changes examples, never the extracted facts, scope or assessment. In
    particular, no method spelling, directory label or benchmark role ranks an
    operation as more important. Unknown calls remain available independently.
    """
    kind, operands = operation.get("operation_kind"), _dict(operation.get("operands"))
    relations = {item.get("kind") for item in _list(operation.get("relationships")) if isinstance(item, dict)}
    if kind == "call_argument_transfer":
        callee, parameter = _dict(operands.get("callee")), _dict(operands.get("target_parameter"))
        target = callee.get("target_graph_node_id")
        bound = callee.get("binding_state") == "authenticated_internal_call" and bool(target)
        owner_file = _dict(operation.get("actual_owner")).get("file")
        cross_file = bool(owner_file and parameter.get("file") and owner_file != parameter["file"])
        argument = _dict(operands.get("argument"))
        index = operands.get("argument_index")
        return (int(bound), int(bound and target in selected_targets), int(cross_file),
            int("authenticated_argument_parameter_projection" in relations),
            int(bool(operands.get("record_fields"))), int(bool(argument)),
            int(bool(argument.get("source_path"))), -index if isinstance(index, int) else -999)
    if kind == "record_construction":
        fields = _list(operands.get("record_fields"))
        return (int("record_literal_as_argument" in relations or "explicit_return_value" in relations),
            int(operands.get("closed_captured_shape") is True), min(len(fields), _DISPLAY["field_examples"]))
    if kind == "guard_rejection":
        return (int(operands.get("exit_kind") in {"throw", "Err_return"}),
            int(bool(operands.get("condition_source"))), int(bool(operands.get("exit_source"))))
    if kind in {"field_write", "binding_initializer", "binding_update"}:
        value = _dict(operands.get("value"))
        path = _dict(_dict(operation.get("subject")).get("target_path"))
        return (int(bool(relations - {"normal_source_before"})), int(bool(value.get("source_path"))),
            int(bool(path.get("member_path"))), int(bool(operation.get("guards"))))
    if kind == "return_transfer":
        return (int("explicit_return_value" in relations), int(bool(operands.get("source_path"))),
            int(bool(operands.get("source_text"))))
    return (int(bool(relations - {"normal_source_before"})),)


def _presentation_key(operation: dict) -> tuple:
    kind, operands = operation.get("operation_kind"), _dict(operation.get("operands"))
    if kind == "call_argument_transfer":
        callee = _dict(operands.get("callee"))
        return (kind, callee.get("target_graph_node_id") or callee.get("source_text"), callee.get("binding_state"))
    if kind == "guard_rejection":
        return (kind, operands.get("condition_source"), operands.get("exit_kind"))
    if kind in {"field_write", "binding_initializer", "binding_update", "record_field_projection"}:
        return (kind, _binding_path(operation))
    if kind == "record_construction":
        return (kind, tuple(_dict(field).get("name") for field in _list(operands.get("record_fields"))))
    return (kind,)


def _selected_statement_indices(operations: list[tuple[int, dict]], selected_targets: set[str]) -> list[int]:
    # Preserve every actual kind, then diverse bound interfaces, state paths and
    # conditions. Source order remains the final display order, not causation.
    by_kind: dict[str, list[int]] = defaultdict(list)
    for position, (_, operation) in enumerate(operations):
        by_kind[str(operation.get("operation_kind"))].append(position)
    chosen = [max(positions, key=lambda p: (_presentation_rank(operations[p][1], selected_targets), -p))
        for positions in by_kind.values()]
    seen = {_presentation_key(operations[position][1]) for position in chosen}
    priorities = {kind: index for index, kind in enumerate(("call_argument_transfer", "field_write",
        "guard_rejection", "binding_update", "record_construction", "return_transfer", "binding_initializer",
        "record_field_projection", "record_copy_projection", "protocol_literal_field", "normal_source_order"))}
    candidates = sorted(range(len(operations)), key=lambda p: (
        priorities.get(operations[p][1].get("operation_kind"), 99),
        tuple(-part for part in _presentation_rank(operations[p][1], selected_targets)), p))
    for position in candidates:
        if len(chosen) >= _DISPLAY["statements_per_declaration"]:
            break
        key = _presentation_key(operations[position][1])
        if key not in seen:
            chosen.append(position)
            seen.add(key)
    for position in candidates:
        if len(chosen) >= _DISPLAY["statements_per_declaration"]:
            break
        if position not in chosen:
            chosen.append(position)
    return sorted(chosen[:_DISPLAY["statements_per_declaration"]])


def _declarations(operations: list[dict]) -> list[dict]:
    groups: dict[tuple, list[tuple[int, dict]]] = defaultdict(list)
    for index, operation in enumerate(operations):
        groups[_owner_key(operation)].append((index, operation))
    declarations = []
    selected_targets = {owner["graph_node_id"] for operation in operations
        if (owner := _dict(operation.get("actual_owner"))).get("graph_node_id")}
    for key, entries in sorted(groups.items()):
        selected = _selected_statement_indices(entries, selected_targets)
        first = entries[0][1]
        statements = [_statement(entries[position][1], entries[position][0]) for position in selected]
        priorities = {kind: index for index, kind in enumerate(("record_construction", "call_argument_transfer",
            "field_write", "binding_initializer", "binding_update", "guard_rejection", "return_transfer", "record_field_projection", "record_copy_projection",
            "protocol_literal_field", "normal_source_order"))}
        statement_positions = {statement["operation_id"]: position for position, statement in enumerate(statements)}
        ranked = sorted(selected, key=lambda position: (
            priorities.get(entries[position][1].get("operation_kind"), 99),
            tuple(-part for part in _presentation_rank(entries[position][1], selected_targets)), position))
        summary_statements, summary_kinds = [], set()
        for position in ranked:
            operation = entries[position][1]
            statement = statements[statement_positions[operation["id"]]]
            if statement["operation_kind"] not in summary_kinds:
                summary_statements.append(statement)
                summary_kinds.add(statement["operation_kind"])
            if len(summary_statements) == 7:
                break
        # A second distinct authenticated interface is useful when an adapter
        # first prepares a record and later hands it to another selected port.
        # It is explicitly chosen from real bindings, not a method-name guess.
        summary_targets = {_dict(_dict(entries[position][1].get("operands")).get("callee")).get("target_graph_node_id")
            for position in selected if any(item["operation_id"] == entries[position][1].get("id") for item in summary_statements)}
        for position in ranked:
            operation = entries[position][1]
            callee = _dict(_dict(operation.get("operands")).get("callee"))
            target = callee.get("target_graph_node_id")
            if (len(summary_statements) < 8 and operation.get("operation_kind") == "call_argument_transfer"
                    and callee.get("binding_state") == "authenticated_internal_call" and target in selected_targets
                    and target not in summary_targets):
                summary_statements.append(statements[statement_positions[operation["id"]]])
                summary_targets.add(target)
        declarations.append({"id": _digest([VERSION, "declaration", key])[:24],
            "actual_owner": first.get("actual_owner", {}), "label": _owner_label(first),
            "summary": " ".join(statement["text"] for statement in summary_statements),
            "summary_statement_ids": [statement["id"] for statement in summary_statements],
            "operation_kind_counts": dict(sorted(Counter(item.get("operation_kind", "unknown") for _, item in entries).items())),
            "statements": statements, "all_operation_refs": [_operation_reference(item, index) for index, item in entries],
            "derived_work_roles": _work_roles(entries),
            "presentation_truncated": len(entries) != len(selected), "operation_count": len(entries),
            "source_operations_remain_available": True,
            "presentation_selection": "Source-structural diversity, authenticated selected/cross-file interfaces, actual record/value relationships and explicit condition exits; no business-name or directory ranking.",
            "responsibility_meaning": "Only the recorded operations and handoffs in this exact source declaration are explained.",
            "unique_fact_owner_proven": False, "all_mutations_authorized_proven": False})
    return declarations


def _work_roles(entries: list[tuple[int, dict]]) -> list[dict]:
    """Finite source-work roles, classified by operations, never owner names."""
    definitions = (
        ("record_construction", "构造记录", {"record_construction"}),
        ("field_updates", "更新捕获字段", {"field_write"}),
        ("binding_updates", "初始化与更新捕获 binding", {"binding_initializer", "binding_update"}),
        ("record_projection", "组织字段与复制来源", {"record_field_projection", "record_copy_projection"}),
        ("conditional_exit", "按捕获条件提前退出", {"guard_rejection"}),
        ("result_projection", "返回表达式或结果记录", {"return_transfer"}),
        ("message_shape", "提供消息形状中的固定字段", {"protocol_literal_field"}),
    )
    result = []
    for kind, label, operation_kinds in definitions:
        refs = [_operation_reference(operation, index) for index, operation in entries
            if operation.get("operation_kind") in operation_kinds]
        if refs:
            result.append({"kind": kind, "label": label, "operation_refs": refs,
                "meaning": "Responsibility limited to the recorded captured source work; no unique owner or runtime activation."})
    for state, kind, label in (("authenticated_internal_call", "bound_interface_arguments", "调用已绑定接口并保留实参位置"),
            (None, "opaque_interface_arguments", "保留未唯一绑定的调用形式与实参位置")):
        refs = [_operation_reference(operation, index) for index, operation in entries
            if operation.get("operation_kind") == "call_argument_transfer" and
                ((_dict(_dict(operation.get("operands")).get("callee")).get("binding_state") == state)
                    if state is not None else (_dict(_dict(operation.get("operands")).get("callee")).get("binding_state")
                        != "authenticated_internal_call"))]
        if refs:
            result.append({"kind": kind, "label": label, "operation_refs": refs,
                "meaning": "Actual ordinary call argument work; opaque calls do not imply storage, provider or wire effects."})
    return result


def _relationship_text(relationship: dict, origin: dict, destination: dict) -> str:
    kind = relationship.get("kind")
    left, right = _owner_label(origin), _owner_label(destination)
    if kind == "lexical_value_to_argument":
        return "「" + left + "」的捕获词法 binding 来源关联到「" + right + "」的实参位置；关系不推出隐藏写入之后的值或堆对象身份。"
    if kind == "record_literal_as_argument":
        return "「" + left + "」中的实际记录 literal 语法位置直接构成「" + right + "」的调用实参；没有把记录构造解释为持久提交。"
    if kind == "field_projection_from_record":
        return "「" + left + "」的捕获记录与「" + right + "」中的字段投影存在显式源关系；当前值和全部覆盖路径另保留。"
    if kind == "explicit_return_value":
        return "「" + left + "」的捕获来源被「" + right + "」的显式 return 消费；未据此证明调用方激活或运行结果。"
    if kind == "normal_source_before":
        return "「" + left + "」中的源操作在所记录的正常顺序上先于「" + right + "」的源操作；这不新增因果、事务或消息身份连接。"
    if kind == "authenticated_argument_parameter_projection":
        return "「" + left + "」的实际已绑定调用实参与确切形参声明对应，该形参由「" + right + "」的捕获字段/实参/return 来源引用；保留调用激活、当前字段值和隐藏效果边界。"
    return "未解释的源关系仍保留完整记录。"


def _relationships(operations: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    by_id = {operation.get("id"): (index, operation) for index, operation in enumerate(operations)}
    links, gaps, seen = [], [], set()
    for operation in operations:
        for relationship in _list(operation.get("relationships")):
            if not isinstance(relationship, dict):
                gaps.append({"code": "responsibility_relationship_not_an_object", "operation_id": operation.get("id")})
                continue
            marker = _digest(relationship)
            if marker in seen:
                continue
            seen.add(marker)
            kind = relationship.get("kind")
            origin = by_id.get(relationship.get("from_operation_id"))
            destination = by_id.get(relationship.get("to_operation_id"))
            if kind not in _RELATIONS or origin is None or destination is None:
                gaps.append({"code": "responsibility_relationship_endpoint_or_kind_unavailable",
                    "relationship": relationship})
                continue
            links.append({"id": _digest([VERSION, "relationship", marker])[:24],
                "kind": kind, "text": _relationship_text(relationship, origin[1], destination[1]),
                "source_relationship": relationship,
                "from": _operation_reference(origin[1], origin[0]), "to": _operation_reference(destination[1], destination[0]),
                "conditions": relationship.get("conditions", []),
                "binding_state": relationship.get("binding_state"), "runtime_or_physical_effect_proven": False,
                "ordinary_call_promoted_to_wire_relation": False,
                "source_order_promoted_to_value_or_causal_connection": False})
    transfers = [link for link in links if link["kind"] != "normal_source_before"]
    orders = [link for link in links if link["kind"] == "normal_source_before"]
    return transfers, orders, gaps


def _reuse(operations: list[dict], snapshot: Any) -> list[dict]:
    nodes: dict[str, list[Any]] = defaultdict(list)
    for node in snapshot.nodes:
        nodes[node.id].append(node)
    targets: dict[str, list[tuple[int, dict]]] = defaultdict(list)
    for index, operation in enumerate(operations):
        callee = _dict(_dict(operation.get("operands")).get("callee"))
        target = callee.get("target_graph_node_id")
        if (operation.get("operation_kind") == "call_argument_transfer"
                and callee.get("binding_state") == "authenticated_internal_call"
                and isinstance(target, str) and len(nodes.get(target, [])) == 1):
            targets[target].append((index, operation))
    result = []
    for target, entries in sorted(targets.items()):
        owners = {_owner_key(operation) for _, operation in entries}
        if len(owners) < 2:
            continue
        node = nodes[target][0]
        result.append({"target_graph_node_id": target, "target_symbol": node.qualname, "target_file": node.file,
            "text": "所选的 " + str(len(owners)) + " 个确切声明通过已绑定调用复用「" + node.qualname +
                "」；复用本身不构成职责混乱或唯一资源所有权的判断。",
            "calling_declarations": sorted({_owner_label(operation) for _, operation in entries}),
            "operation_refs": [_operation_reference(operation, index) for index, operation in entries],
            "source_scope": "only authenticated operations in selected report scopes", "god_object_inferred": False,
            "unique_implementation_or_effect_proven": False})
    return result


def _communication(operations: list[dict]) -> dict:
    internal, opaque, protocol, empty = [], [], [], []
    for index, operation in enumerate(operations):
        if operation.get("operation_kind") == "call_argument_transfer":
            callee = _dict(_dict(operation.get("operands")).get("callee"))
            reference = _operation_reference(operation, index)
            if _dict(operation.get("operands")).get("argument_count") == 0:
                empty.append(reference)
                continue
            if callee.get("binding_state") == "authenticated_internal_call" and callee.get("target_graph_node_id"):
                internal.append(reference)
            else:
                opaque.append(reference)
        elif operation.get("operation_kind") == "protocol_literal_field":
            protocol.append(_operation_reference(operation, index))
    return {"authenticated_ordinary_call_argument_refs": internal, "opaque_call_argument_refs": opaque,
        "message_literal_field_refs": protocol, "zero_argument_call_refs": empty,
        "ordinary_call_count_is_not_wire_coverage": True,
        "matching_literals_promoted_to_wire_connection": False,
        "cross_language_or_process_calls_created": False,
        "meaning": "Ordinary authenticated calls, opaque effect/dispatch frontiers and captured message fields are separate. A matching method or literal does not establish a transport or end-to-end identity relation."}


def _source_anchors(value: Any, *, limit: int = 24) -> dict:
    """Compact actual prior-source anchors, never interpret purpose strings."""
    owners, locations, seen = set(), [], set()
    pending, visited, truncated = [value], 0, False
    while pending:
        current = pending.pop()
        visited += 1
        if visited > 65536:
            truncated = True
            break
        if isinstance(current, dict):
            if isinstance(current.get("file"), str) and isinstance(current.get("line"), int) and current.get("source_hash"):
                key = current["file"], current.get("start_byte"), current.get("end_byte")
                if key not in seen:
                    seen.add(key)
                    if len(locations) < limit:
                        locations.append({name: current[name] for name in ("file", "line", "column", "start_byte",
                            "end_byte", "source_hash", "span_hash") if name in current})
                    else:
                        truncated = True
                owner = _dict(current.get("anchor")).get("owner")
                if isinstance(owner, str) and owner:
                    owners.add(owner)
            if isinstance(current.get("owner"), str) and current["owner"].startswith(("ts:", "rust:")):
                owners.add(current["owner"])
            pending.extend(child for name, child in reversed(list(current.items())) if name not in {
                "source_excerpt", "source_line", "parse_identity", "parse_provenance"} and isinstance(child, (dict, list)))
        elif isinstance(current, list):
            pending.extend(reversed(current))
    return {"source_locations": locations, "captured_owner_graph_node_ids": sorted(owners),
        "presentation_truncated": truncated, "full_source_records_preserved_at_pointer": True}


def _path_choice(choice: Any) -> str:
    item = _dict(choice)
    path = item.get("path") or item.get("literal_suffix")
    if path:
        return str(item.get("kind", "captured")) + ":" + _clip(path)
    source = _dict(item.get("source_path"))
    if source.get("root") is not None:
        return str(item.get("kind", "captured")) + ":" + _clip([source["root"], *_list(source.get("keys"))])
    return _clip(item.get("kind") or "unresolved_path_choice")


def _protocol_contract_seams(snapshot: Any, report: dict) -> list[dict]:
    """Present an existing finite codec/message proof without re-inferring it.

    Generated raw support is legitimate protocol-model evidence, but does not
    become an implementation selector or a cross-language ordinary call edge.
    All joins below use the actual saved model/obligation/relation identities.
    """
    model_id, analyzer = "captured-device-json-serde-dispatch-v1", "static-device-spec-protocol-flow-1"
    required = {"generated_typescript_wire_record_path", "wire_record_field_mapping_and_default",
        "command_json_http_record_transport", "server_json_body_to_dispatcher",
        "typed_application_family_dispatch", "typed_command_update_dispatch"}
    result = []
    for judgment_index, judgment in enumerate(_list(report.get("judgments"))):
        if not isinstance(judgment, dict):
            continue
        for adapter_index, adapter in enumerate(_list(judgment.get("adapter_judgments"))):
            for evidence_index, evidence in enumerate(_list(_dict(adapter).get("evidence"))):
                details = _dict(_dict(evidence).get("details"))
                if (details.get("analyzer_version") != analyzer or details.get("snapshot_id") != snapshot.id
                        or details.get("source_hash") != snapshot.source_hash or details.get("policy_hash") != snapshot.policy_hash):
                    continue
                pointer = f"/judgments/{judgment_index}/adapter_judgments/{adapter_index}/evidence/{evidence_index}/details"
                models = [(index, model) for index, model in enumerate(_list(details.get("models")))
                    if isinstance(model, dict) and model.get("model_id") == model_id and model.get("version") == analyzer
                    and _dict(model.get("applicability")).get("accepted") is True and isinstance(model.get("model_record_id"), str)]
                for obligation_index, obligation in enumerate(_list(details.get("obligations"))):
                    if (not isinstance(obligation, dict) or obligation.get("status") != "supported"
                            or obligation.get("complete") is not True or obligation.get("necessary_gaps") != []):
                        continue
                    identifiers = set(_list(obligation.get("evidence_relation_ids")))
                    candidates: dict[str, list[tuple[int, dict]]] = defaultdict(list)
                    for relation_index, relation in enumerate(_list(details.get("relations"))):
                        if (isinstance(relation, dict) and relation.get("kind") in required
                                and relation.get("relation_id") in identifiers
                                and relation.get("obligation_id") == obligation.get("id")
                                and relation.get("model_id") == model_id and relation.get("extractor_version") == analyzer
                                and relation.get("snapshot_id") == snapshot.id and relation.get("source_hash") == snapshot.source_hash
                                and relation.get("manufactured_call_edge") is False and _dict(relation.get("location")).get("source_hash")):
                            candidates[relation["kind"]].append((relation_index, relation))
                    if set(candidates) != required or any(len(values) != 1 for values in candidates.values()):
                        continue
                    typescript = candidates["generated_typescript_wire_record_path"][0][1]
                    mapping = candidates["wire_record_field_mapping_and_default"][0][1]
                    transport = candidates["command_json_http_record_transport"][0][1]
                    server = candidates["server_json_body_to_dispatcher"][0][1]
                    application = candidates["typed_application_family_dispatch"][0][1]
                    dispatch = candidates["typed_command_update_dispatch"][0][1]
                    accepted = [(index, model) for index, model in models
                        if model["model_record_id"] == mapping.get("model_record_id") == transport.get("model_record_id")]
                    if (len(accepted) != 1 or not isinstance(mapping.get("wire_field"), str)
                            or mapping["wire_field"] != typescript.get("wire_field")
                            or not isinstance(transport.get("command_path"), str)
                            or transport["command_path"] != server.get("message_path")
                            or not isinstance(dispatch.get("command"), str)
                            or dispatch["command"] != application.get("command")
                            or typescript.get("command_type") != dispatch.get("typed_request_variant")
                            or dispatch.get("typed_request_variant") != application.get("typed_request_variant")
                            or not isinstance(obligation.get("transport_model"), str)):
                        continue
                    model_index, model = accepted[0]
                    selected = sorted((values[0] for values in candidates.values()), key=lambda item: item[0])
                    facts = [relation for _, relation in selected]
                    text = ("所选命令「" + _clip(dispatch["command"]) + "」的生成 TypeScript 记录按「"
                        + _clip(typescript.get("command_type")) + " → payload:" + _clip(typescript.get("payload_type"))
                        + " → spec:" + _clip(typescript.get("spec_type")) + "」组织字段「" + _clip(mapping["wire_field"])
                        + "」（optional=" + _clip(typescript.get("field_optional")) + "）。已认证 Serde 模型将它映射到 Rust 字段「"
                        + _clip(mapping.get("rust_field")) + ":" + _clip(mapping.get("rust_type")) + "」，缺失值为「"
                        + _clip(mapping.get("absent_wire_value")) + "」，源属性为「" + "；".join(_clip(value) for value in _list(mapping.get("source_attributes")))
                        + "」。在原普通 JSON/已认证 Serde 及成功消息模型条件下，实际「" + _clip(transport.get("method"))
                        + " " + _clip(transport["command_path"]) + "」序列化记录与 Server 的同一路径解码/dispatcher 记录相接，typed variant 为「"
                        + _clip(dispatch.get("typed_request_variant")) + "」。这是所选协议字段与消息关系，不把 HTTP 已发生、所有 query/WS codec 或跨语言普通调用当成已证明。")
                    result.append({"kind": "finite_generated_json_serde_message_source_relation", "text": text,
                        "goal_id": judgment.get("goal_id"), "finding_id": judgment.get("finding_id"),
                        "evidence_id": judgment.get("evidence_id"), "adapter_finding_id": _dict(adapter).get("id"),
                        "adapter_evidence_id": _dict(evidence).get("id"), "obligation_id": obligation.get("id"),
                        "obligation_status": obligation["status"], "source_analysis_pointer": pointer,
                        "source_obligation_pointer": pointer + f"/obligations/{obligation_index}",
                        "source_relation_refs": [{"relation_id": relation["relation_id"], "kind": relation["kind"],
                            "source_class": relation.get("source_class"), "source_pointer": pointer + f"/relations/{index}"}
                            for index, relation in selected],
                        "models": [{"id": model_id, "version": model["version"], "model_record_id": model["model_record_id"],
                            "applicability_accepted": True, "source_pointer": pointer + f"/models/{model_index}"}],
                        "conditions": details.get("conditions", []), "transport_model": obligation["transport_model"],
                        "scope_boundaries": details.get("scope_boundaries", []), "supported_source_relation": True,
                        **_source_anchors(facts), "source_gaps": [], "creates_calls_edge": False,
                        "generated_support_upgraded_to_implementation": False,
                        "runtime_transport_or_physical_effect_proven": False, "network_success_verified": False,
                        "all_http_query_or_websocket_contracts_proven": False})
    return result


def _computed_contract_seams(snapshot: Any, report: dict) -> list[dict]:
    """Reuse actual prior finite source models for non-CALLS boundaries.

    In particular a Node process, committed inbox/queue and authenticated JSON
    channel must not be inferred from a call name in the operation extractor.
    These are independent saved model relations with their original pointers.
    """
    identity = _dict(report.get("snapshot"))
    if (identity.get("id") != snapshot.id or identity.get("source_hash") != snapshot.source_hash
            or identity.get("policy_hash") != snapshot.policy_hash):
        return []
    result = []
    channel_names = {"protected_queue_json_record": "受保护 queue 的 JSON 记录交接",
        "worker_inbox_file_record": "inbox 文件记录的提交、领取与消费",
        "authenticated_worker_broker_json": "认证 broker 的 JSON 请求、分派与响应",
        "persisted_assignment_attempt_counter": "持久 assignment/attempt 记录到消费者的交接"}
    for judgment_index, judgment in enumerate(_list(report.get("judgments"))):
        if not isinstance(judgment, dict):
            continue
        for obligation_index, obligation in enumerate(_list(judgment.get("obligations"))):
            if not isinstance(obligation, dict):
                continue
            evidence = _dict(obligation.get("evidence"))
            pointer = f"/judgments/{judgment_index}/obligations/{obligation_index}/evidence"
            context = {"goal_id": judgment.get("goal_id"), "obligation_id": obligation.get("id"),
                "finding_id": judgment.get("finding_id"), "evidence_id": judgment.get("evidence_id"),
                "obligation_status": obligation.get("status"), "source_analysis_pointer": pointer,
                "prior_judgment_is_not_new_whole_architecture_approval": True}
            assembly = _dict(evidence.get("production_assembly"))
            if assembly.get("model_id") == "source-derived-module-assembly-v1":
                cli = _dict(assembly.get("cli"))
                for index, call in enumerate(_list(cli.get("calls"))):
                    if not isinstance(call, dict):
                        continue
                    selected = [_path_choice(choice) for choice in _list(call.get("selected_paths"))]
                    alternatives = [_path_choice(choice) for choice in _list(call.get("other_path_choices"))]
                    if not selected:
                        continue
                    result.append({"kind": "finite_dynamic_command_source_assembly", **context,
                        "source_analysis_pointer": pointer + f"/production_assembly/cli/calls/{index}",
                        "text": "所选默认装配的源模型列出动态命令 import 的候选路径「" + "；".join(selected) +
                            "」。其他捕获路径分支为「" + ("；".join(alternatives) if alternatives else "该条记录没有其他选择") +
                            "」；这是有限路径与实际形参关系，不把所有候选当必然普通调用。",
                        "supported_source_relation": call.get("supported") is True,
                        "model_id": assembly["model_id"], "scope": cli.get("scope"),
                        "source_gaps": cli.get("gaps", []), **_source_anchors(call),
                        "creates_calls_edge": False, "runtime_activation_proven": False})
                for index, start in enumerate(_list(assembly.get("worker_process_starts"))):
                    if not isinstance(start, dict) or start.get("standard_spawn_binding") is not True:
                        continue
                    choices = [_path_choice(choice) for choice in _list(start.get("worker_source_path_choices"))]
                    result.append({"kind": "captured_standard_node_worker_process_seam", **context,
                        "source_analysis_pointer": pointer + f"/production_assembly/worker_process_starts/{index}",
                        "text": "捕获的标准 Node spawn 导入通过实际 argv 源关系选择 worker 路径「" + "；".join(choices) +
                            "」；进程接线独立于普通函数 CALLS，未据此宣称进程已经启动或 worker 已执行。",
                        "captured_owner_graph_node_id": start.get("owner"), "model_id": assembly["model_id"],
                        "scope": assembly.get("scope"), "supported_source_relation": True,
                        **_source_anchors(start), "creates_calls_edge": False, "runtime_activation_proven": False})
                for index, variant in enumerate(_list(assembly.get("worker_direct_broker_variants"))):
                    binding = _dict(_dict(variant).get("binding"))
                    targets = [_dict(item).get("selector") for item in _list(binding.get("targets"))]
                    if not targets:
                        continue
                    result.append({"kind": "conditional_captured_receiver_assembly", **context,
                        "source_analysis_pointer": pointer + f"/production_assembly/worker_direct_broker_variants/{index}",
                        "text": "同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「" +
                            "；".join(_clip(item) for item in targets) +
                            "」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。",
                        "captured_targets": targets,
                        "supported_source_relation": binding.get("all_captured_receiver_variants_resolved") is True,
                        "model_id": assembly["model_id"], "scope": assembly.get("scope"),
                        **_source_anchors(variant), "global_receiver_dispatch_proven": False,
                        "creates_calls_edge": False, "runtime_activation_proven": False})
            channels = _dict(evidence.get("channels"))
            if (channels.get("snapshot_id") != snapshot.id or channels.get("source_hash") != snapshot.source_hash
                    or channels.get("policy_hash") != snapshot.policy_hash or channels.get("source_only") is not True
                    or channels.get("creates_calls_edges") is not False):
                continue
            for key in ("queue", "inbox", "broker", "counter_transport"):
                channel = _dict(channels.get(key))
                label = channel_names.get(channel.get("kind"))
                if label is None:
                    continue
                parts = {name: value.get("supported") for name, value in channel.items()
                    if isinstance(value, dict) and type(value.get("supported")) is bool}
                receipt_keys = _list(_dict(channel.get("writer")).get("receipt_keys"))
                response_keys = _list(_dict(channel.get("response")).get("handler_fields"))
                anchors = _source_anchors(channel)
                result.append({"kind": channel["kind"], **context,
                    "source_analysis_pointer": pointer + "/channels/" + key,
                    "text": "已有条件源码模型记录「" + label + "」的源操作与条件；实际部件关系为「" +
                        "；".join(name + "=" + str(value).lower() for name, value in parts.items()) +
                        "」，捕获参与声明为「" + "；".join(anchors["captured_owner_graph_node_ids"][:12]) +
                        "」。" + ("记录/响应字段为「" + "；".join(map(str, [*receipt_keys, *response_keys])) + "」。" if receipt_keys or response_keys else "") +
                        "持久消息和协议关系保持独立，执行、交付与队列投影没有合并成一个成功。",
                    "supported_source_relation": channel.get("supported") is True, "source_part_states": parts,
                    "receipt_field_names": receipt_keys, "response_field_names": response_keys,
                    "model_version": channels.get("version"), "models": channels.get("models", []),
                    "conditions": channels.get("conditions", []), "source_gaps": channels.get("gaps", []),
                    **anchors, "creates_calls_edge": False,
                    "runtime_transport_or_physical_effect_proven": False})
    result.extend(_protocol_contract_seams(snapshot, report))
    # The finite event/lineage and publication models retain their own facts
    # and countercases. Reuse their computed source statement, rather than
    # rebuilding a state transition from similarly named calls or fields.
    for index, chain in enumerate(_list(report.get("functional_chains"))):
        if not isinstance(chain, dict):
            continue
        pattern = _dict(chain.get("pattern"))
        if (pattern.get("model") != "finite-conditional-event-lineage-publication-source-v1"
                or pattern.get("scoped_source_supported") is not True
                or pattern.get("source_statement_relation_closed") is not True
                or not isinstance(pattern.get("statement"), str)
                or not pattern["statement"]
                or not _list(pattern.get("relation_witnesses"))):
            continue
        facts = _list(chain.get("source_facts"))
        result.append({"kind": "finite_conditional_state_or_publication_source_relation",
            "rule_id": chain.get("rule_id"), "finding_id": chain.get("finding_id"),
            "evidence_id": chain.get("evidence_id"), "text": pattern["statement"],
            "interpretation": pattern.get("interpretation"),
            "source_analysis_pointer": f"/functional_chains/{index}/pattern",
            "source_facts_pointer": f"/functional_chains/{index}/source_facts",
            "relation_witnesses_pointer": f"/functional_chains/{index}/pattern/relation_witnesses",
            "source_fact_ids": [fact["id"] for fact in facts if isinstance(fact, dict) and isinstance(fact.get("id"), str)],
            "supported_source_relation": True, "model_version": pattern.get("version"),
            "models": [pattern.get("trusted_model", {})],
            "conditions": pattern.get("source_conditions", []),
            "source_gaps": [*_list(chain.get("analysis_gaps")), *_list(pattern.get("necessary_gaps"))],
            "countercases_and_scope_preserved_at_source_analysis_pointer": True,
            **_source_anchors(facts), "creates_calls_edge": False,
            "runtime_transport_or_physical_effect_proven": False})
    return result


def _navigation(operations: list[dict], declarations: list[dict]) -> list[dict]:
    by_context: dict[str, set[str]] = defaultdict(set)
    for operation in operations:
        for reference in _list(operation.get("source_evidence_refs")):
            if not isinstance(reference, dict):
                continue
            for key in ("rule_id", "goal_id"):
                if isinstance(reference.get(key), str):
                    by_context[reference[key]].add(operation["id"])
    result = []
    for identifier, label, contexts in _NAVIGATION:
        present = [context for context in contexts if by_context.get(context)]
        ids = sorted({operation_id for context in present for operation_id in by_context[context]})
        if not ids:
            continue
        declaration_ids = [entry["id"] for entry in declarations if any(
            reference.get("operation_id") in ids for reference in entry["all_operation_refs"])]
        result.append({"id": identifier, "label": label, "source_context_ids": present,
            "operation_ids": ids, "declaration_explanation_ids": declaration_ids,
            "navigation_only": True, "label_is_evidence_or_responsibility_assertion": False,
            "original_paragraph_fully_reproduced_from_label": False})
    return result


def _explain_operations(snapshot: Any, report: dict, extraction: dict) -> dict:
    """Compose an actual extractor result; also reused by source-query helpers."""
    operations = _list(extraction.get("operations"))
    snapshot_identity = {"snapshot_id": snapshot.id, "source_hash": snapshot.source_hash,
        "policy_hash": snapshot.policy_hash}
    report_identity = _dict(report.get("snapshot"))
    gaps = list(_list(extraction.get("analysis_gaps")))
    if (report_identity.get("id") != snapshot.id or report_identity.get("source_hash") != snapshot.source_hash
            or report_identity.get("policy_hash") != snapshot.policy_hash):
        gaps.append({"code": "responsibility_report_snapshot_identity_mismatch"})
        operations = []
    if extraction.get("snapshot_identity") != snapshot_identity:
        gaps.append({"code": "responsibility_operation_extraction_identity_mismatch"})
        operations = []
    valid, seen = [], set()
    for index, operation in enumerate(operations):
        if (not isinstance(operation, dict) or not isinstance(operation.get("id"), str)
                or operation["id"] in seen or not operation.get("source_locations")):
            gaps.append({"code": "responsibility_operation_identity_or_source_unavailable", "operation_index": index})
            continue
        seen.add(operation["id"])
        valid.append(operation)
    declarations = _declarations(valid)
    transfers, orders, relationship_gaps = _relationships(valid)
    gaps.extend(relationship_gaps)
    reuse = _reuse(valid, snapshot)
    explanation_gaps = [gap for entry in declarations for statement in entry["statements"] for gap in statement["source_gaps"]]
    return {"version": VERSION, "operation_extractor_version": extraction.get("version"),
        "snapshot_identity": snapshot_identity, "operation_extraction_identity": extraction.get("snapshot_identity"),
        "operations": valid, "declaration_explanations": declarations,
        "source_location_index": extraction.get("source_location_index", {}),
        "evidence_reference_index": extraction.get("evidence_reference_index", {}),
        "source_index_pointer_scope": "this_responsibility_explanation_object",
        "explicit_source_transfers": transfers, "normal_source_orders": orders,
        "authenticated_interface_reuse": reuse, "communication_boundaries": _communication(valid),
        "computed_source_contract_seams": _computed_contract_seams(snapshot, report),
        "navigation": _navigation(valid, declarations),
        "analysis_gaps": gaps, "explanation_source_gaps": explanation_gaps,
        "operation_extraction_scope": extraction.get("scope", {}),
        "operation_extraction_flags": extraction.get("flags", {}),
        "operation_extraction_budget": extraction.get("budget", {}),
        "presentation_limits": dict(_DISPLAY),
        "assessment": {"state": "finite_source_responsibility_explanations_available" if valid else "unknown",
            "explanation_generated_from_actual_operations": bool(valid),
            "source_directories_used_to_assign_responsibility": False,
            "method_names_used_to_infer_responsibility": False,
            "reference_report_text_used_as_evidence": False,
            "whole_report_reproduced": False, "whole_repository_ownership_proven": False,
            "unique_fact_owner_proven": False, "all_operations_authorized_proven": False,
            "runtime_or_physical_effects_verified": False,
            "functional_coverage_percentage_computed": False},
        "meaning": "Exact declarations are explained by actual captured record/field operations, authenticated argument handoffs and explicit guard/source relations. Business labels are navigation only; execution, delivery and projection are not collapsed into one success.",
        "unreviewed_scope": ["all writers or all routes outside selected captured scopes",
            "arbitrary heap aliases, hidden effects, callback activation and runtime reaching values",
            "complete authorization, physical persistence, provider success and full recovery state machines"],
        "target_executed": False, "target_tests_run": False, "target_build_run": False}


def build_responsibility_explanations(snapshot: Any, report: dict) -> dict:
    """Build concrete source-backed explanations, never an architectural grade."""
    from .responsibility_operations import extract_responsibility_operations
    return _explain_operations(snapshot, report, extract_responsibility_operations(snapshot, report))
