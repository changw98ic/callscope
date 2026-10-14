"""Conditional source lineage and publication boundaries, never target execution.

Only authenticated captured declarations/CALLS and original CSTs are consumed.
Finite record/boolean expressions are abstract model data, not runnable target
functions. A selected branch and normal preceding operations are conditions;
IO durability, callback activation and remote postconditions remain unproved.
"""
from __future__ import annotations

from collections import defaultdict
import itertools
import json
from typing import Any

from .conditional_gate_relations import _Summary, _abstract, _truth, _UNKNOWN, _walk_data
from .semantic_sources import unwrap
from .static_contracts import _literal_string

VERSION = "captured-conditional-lineage-publication-1"
MODEL = "finite-conditional-event-lineage-publication-source-v1"
LINEAGE_ROLES = frozenset({"completion", "callback_runner", "status_parser", "superseder", "event_writer",
                           "lineage_builder", "event_authority", "queue_authority"})
PUBLICATION_ROLES = frozenset({"finalizer", "pr_boundary", "push_boundary", "git_executor", "local_git_executor", "review_bundle"})
_FUNCTIONS = {"function_declaration", "function_expression", "arrow_function", "method_definition"}
_ERASED = {"comment", "type_annotation", "type_arguments", "type_parameters"}
_PATH_LIMIT = 128


def _field(node: Any, name: str) -> Any:
    return node.child_by_field_name(name) if node is not None else None


def _children(node: Any) -> list[Any]:
    return [child for child in node.named_children if child.type not in _ERASED and not child.type.endswith("_type")] if node is not None else []


def _operand(node: Any) -> Any:
    node = unwrap(node)
    while node is not None and node.type == "await_expression":
        node = unwrap(next(iter(_children(node)), None))
    return node


def _inside(outer: Any, inner: Any) -> bool:
    return bool(outer is not None and inner is not None and outer.start_byte <= inner.start_byte and inner.end_byte <= outer.end_byte)


def _key(document: Any, node: Any) -> str | None:
    if node is None:
        return None
    return document.text(node) if node.type in {"identifier", "property_identifier", "shorthand_property_identifier", "shorthand_property_identifier_pattern"} else _literal_string(document.text(node)) if node.type == "string" else None


def _record(document: Any, original: Any) -> dict[str, Any]:
    node = _operand(original)
    if node is None or node.type != "object":
        return {}
    result = {}
    for child in _children(node):
        if child.type == "pair":
            key, value = _key(document, _field(child, "key")), _field(child, "value")
        elif child.type == "shorthand_property_identifier":
            key, value = document.text(child), child
        else:
            continue
        if key is not None:
            result[key] = value
    return result


def _body_owner(node: Any) -> Any:
    while node is not None and node.type not in _FUNCTIONS:
        node = node.parent
    return node


def _abrupt(node: Any) -> bool:
    if node is None:
        return False
    if node.type in {"return_statement", "throw_statement"}:
        return True
    if node.type == "statement_block":
        return any(_abrupt(child) for child in _children(node))
    return node.type == "if_statement" and _abrupt(_field(node, "consequence")) and _abrupt(_field(node, "alternative"))


class _Relations:
    def __init__(self, analysis: Any):
        self.a, self.s = analysis, _Summary(analysis)
        self.facts: dict[str, dict] = {}
        self.call_cache: dict[tuple, list] = {}
        self.guard_cache: dict[tuple, list] = {}
        self.expression_cache: dict[tuple, dict] = {}

    @staticmethod
    def compact(value: Any) -> Any:
        """Keep each authenticated/derived fact once in analysis.source_facts.

        A reference is an evidence address, never a fresh source fact or CALLS
        edge. Concrete finite values and unknown expression terms are retained.
        """
        if isinstance(value, dict):
            if value.get("origin") == "source-derived" and value.get("id") and value.get("location"):
                return {"kind": "source_fact_reference", "id": value["id"], "source_fact_id": value["id"],
                        "source_fact_kind": value["kind"]}
            return {key: _Relations.compact(child) for key, child in value.items()}
        if isinstance(value, list):
            return [_Relations.compact(child) for child in value]
        return value

    def fact(self, kind: str, document: Any, node: Any, **data: Any) -> dict:
        data = self.compact(data)
        key = json.dumps([kind, document.source.path, node.start_byte, node.end_byte, data], sort_keys=True)
        if key not in self.facts:
            self.facts[key] = self.a.fact(kind, document, node, state_lineage_version=VERSION, **data)
        return self.facts[key]

    def calls(self, role: str, *, root: Any = None, nested: bool = False) -> list[tuple[Any, dict]]:
        document, _, function = self.a.roles[role]
        root = root or _field(function, "body")
        key = (role, root.id if root is not None else None, nested)
        if key not in self.call_cache:
            self.call_cache[key] = [(node, self.s.call(role, document, node))
                for node in self.a.nodes(document, root, nested=nested) if node.type == "call_expression"]
        return self.call_cache[key]

    def actual(self, role: str, target: str, *, root: Any = None, nested: bool = False) -> list[tuple[Any, dict]]:
        target_id = self.a.roles[target][1].graph_node_id
        return [(node, fact) for node, fact in self.calls(role, root=root, nested=nested)
                if fact.get("actual_callee_graph_node_id") == target_id]

    def expr(self, role: str, node: Any, env: dict | None = None, *, expand: bool = False, depth: int = 0) -> dict:
        document = self.a.roles[role][0]
        if depth > 32:
            self.s.truncated = True
            return {"kind": "unknown", "reason": "conditional_record_expression_depth_limit"}
        key = (role, node.id if node is not None else None, expand, depth) if not env else None
        if key is not None and key in self.expression_cache:
            return self.expression_cache[key]
        env = dict(env or {})
        if expand and depth < 8 and node is not None:
            for reference in self.a.nodes(document, node):
                if reference.type not in {"identifier", "shorthand_property_identifier"}:
                    continue
                record = self.a.lexical(document).resolve_identity(reference)
                identity = record.get("declaration_id")
                if record.get("state") != "unique" or not identity or identity in env:
                    continue
                declaration = self.a.lexical(document).declaration_for(record)
                if (declaration is None or declaration.type != "variable_declarator" or declaration.parent is None
                        or declaration.parent.type != "lexical_declaration"
                        or not document.text(declaration.parent).lstrip().startswith("const ")
                        or declaration.end_byte > reference.start_byte):
                    continue
                value = _field(declaration, "value")
                if value is not None and value.type not in _FUNCTIONS:
                    env[identity] = self.expr(role, value, env, expand=True, depth=depth + 1)
        value = self.s.expr(role, document, node, env)
        # Object members are applied in actual CST order. A later unknown
        # spread can overwrite every earlier known field. Explicit fields
        # after that frontier become known again; nested records obey the same
        # rule. Never turn the Summary's unordered raw field inventory into a
        # value/lineage proof.
        record_node = _operand(node)
        if (record_node is not None and record_node.type == "object" and value.get("kind") == "record"
                and any(child.type not in {"pair", "shorthand_property_identifier", "spread_element"}
                        for child in _children(record_node))):
            value = {"kind": "unknown", "reason": "unsupported_object_member_shape",
                "location": document.location(record_node)}
        if record_node is not None and record_node.type == "object" and value.get("kind") == "record":
            fields, spreads, order = {}, [], []
            for child in _children(record_node):
                if child.type == "pair":
                    field = _key(document, _field(child, "key"))
                    if field is not None:
                        fields[field] = self.expr(role, _field(child, "value"), env, depth=depth + 1)
                        order.append({"field": field})
                elif child.type == "shorthand_property_identifier":
                    field = document.text(child)
                    fields[field] = self.expr(role, child, env, depth=depth + 1)
                    order.append({"field": field})
                elif child.type == "spread_element":
                    spread = self.expr(role, next(iter(_children(child)), None), env, depth=depth + 1)
                    if spread.get("kind") == "record" and not spread.get("spreads"):
                        fields.update(spread["fields"])
                        order.append({"known_plain_spread_fields": sorted(spread["fields"])})
                    else:
                        fields.clear()
                        spreads.append(spread)
                        order.append({"unknown_spread_clears_prior_fields": True})
            value = {"kind": "record", "fields": fields, "spreads": spreads,
                "source_member_order": order, "later_unknown_spread_invalidates_prior_fields": True}
        # Only a captured unshadowed Boolean constructor is interpreted. It is
        # a registered primitive model, not a trusted target helper result.
        if value.get("kind") == "opaque_call" and value.get("source") == "Boolean":
            call = _operand(node)
            callee = _field(call, "function")
            proof = self.a.lexical(document).unbound("Boolean", callee) if callee is not None else {}
            if proof.get("local_declaration_absent") and len(value.get("arguments", [])) == 1:
                value = {"kind": "modeled_boolean_coercion", "operand": value["arguments"][0],
                         "model": MODEL, "source_call_fact_id": value["call_fact_id"]}
        if key is not None:
            self.expression_cache[key] = value
        return value

    def arguments(self, role: str, call: Any, env: dict | None = None) -> list[dict]:
        return [self.expr(role, node, env) for node in _children(_field(call, "arguments"))]

    def bind(self, source_role: str, target_role: str, call: Any, env: dict | None = None) -> tuple[dict, list[dict]]:
        source_doc = self.a.roles[source_role][0]
        target_doc, _, function = self.a.roles[target_role]
        actuals = _children(_field(call, "arguments"))
        result, rows = {}, []
        for index, parameter in enumerate(_children(_field(function, "parameters"))):
            if index >= len(actuals):
                continue
            pattern = _operand(_field(parameter, "pattern") or _field(parameter, "name") or parameter)
            if pattern is None:
                continue
            if pattern.type == "identifier":
                items = [(pattern, actuals[index], None)]
            elif pattern.type == "object_pattern":
                actual_fields = _record(source_doc, actuals[index])
                items = []
                for binder in _children(pattern):
                    if binder.type == "shorthand_property_identifier_pattern":
                        key, identifier = source_doc.text(binder) if target_doc is source_doc else target_doc.text(binder), binder
                    elif binder.type == "pair_pattern":
                        key, identifier = _key(target_doc, _field(binder, "key")), _field(binder, "value")
                    else:
                        continue
                    if key in actual_fields:
                        items.append((identifier, actual_fields[key], key))
            else:
                continue
            for binder, actual, key in items:
                identity = self.s.identity(target_doc, binder)
                if identity:
                    result[identity] = self.expr(source_role, actual, env)
                    rows.append({"parameter_index": index, "destructured_field": key,
                        "formal_declaration_id": identity, "actual_origin": result[identity],
                        "actual_location": source_doc.location(actual), "formal_location": target_doc.location(binder)})
        return result, rows

    def guards(self, role: str, before: Any = None, *, root: Any = None, nested: bool = False) -> list[dict]:
        document, _, function = self.a.roles[role]
        selected_root = root or _field(function, "body")
        cache_key = (role, selected_root.id if selected_root is not None else None, nested)
        if cache_key in self.guard_cache:
            return [fact for fact in self.guard_cache[cache_key]
                    if before is None or fact["location"]["start_byte"] < before.start_byte]
        result = []
        for node in self.a.nodes(document, selected_root, nested=nested):
            if node.type != "if_statement":
                continue
            then, other = _field(node, "consequence"), _field(node, "alternative")
            if not (_abrupt(then) or _abrupt(other)):
                continue
            result.append(self.fact("conditional_abrupt_source_guard", document, node,
                role=role, condition=self.expr(role, _field(node, "condition"), expand=True),
                condition_source=document.text(_field(node, "condition")),
                consequence_abrupt=_abrupt(then), alternative_abrupt=_abrupt(other),
                owner_location=document.location(_body_owner(node)),
                direct_owner_body_statement=node.parent == _field(_body_owner(node), "body"),
                containing_conditions=self.a.branch_context(document, node, _body_owner(node)),
                abrupt_sources=[self.a.expression(document, child) for child in self.a.nodes(document, node)
                    if child.type in {"return_statement", "throw_statement"}],
                is_global_all_paths_dominance_proof=False, branch_runtime_selected=False))
        self.guard_cache[cache_key] = result
        return [fact for fact in result if before is None or fact["location"]["start_byte"] < before.start_byte]


def _lineage(r: _Relations) -> dict:
    a = r.a
    document, _, function = a.roles["completion"]
    selected = []
    for registration, runner_call in r.actual("completion", "callback_runner"):
        callbacks = [arg for arg in _children(_field(registration, "arguments")) if arg.type in _FUNCTIONS]
        for callback in callbacks:
            for guard in a.nodes(document, _field(callback, "body")):
                if guard.type != "if_statement":
                    continue
                consequence = _field(guard, "consequence")
                supersede = r.actual("completion", "superseder", root=consequence)
                lineage = r.actual("completion", "lineage_builder", root=consequence)
                if len(supersede) != 1 or len(lineage) != 1:
                    continue
                condition = _operand(_field(guard, "condition"))
                candidate_refs = [child for child in a.nodes(document, condition) if child.type == "identifier"]
                predicate_sources = []
                for reference in candidate_refs:
                    record = a.lexical(document).resolve_identity(reference)
                    declaration = a.lexical(document).declaration_for(record)
                    initializer = _operand(_field(declaration, "value"))
                    if initializer is not None and initializer.type == "call_expression":
                        fact = r.s.call("completion", document, initializer)
                        if fact.get("actual_callee_graph_node_id") == a.roles["status_parser"][1].graph_node_id:
                            predicate_sources.append(fact)
                if not predicate_sources:
                    a.gap("lineage_guard_status_parser_result_binding_missing", document, guard)
                    continue
                first, second = supersede[0][0], lineage[0][0]
                direct = _children(consequence)
                first_statement = next((statement for statement in direct if _inside(statement, first)), None)
                second_statement = next((statement for statement in direct if _inside(statement, second)), None)
                ordered = first_statement is not None and second_statement is not None and direct.index(first_statement) < direct.index(second_statement)
                awaited = all(node.parent is not None and node.parent.type == "await_expression" for node in (first, second))
                supersede_env, supersede_bindings = r.bind("completion", "superseder", first)
                lineage_env, lineage_bindings = r.bind("completion", "lineage_builder", second)
                event_calls = r.actual("superseder", "event_writer")
                queue_calls = r.actual("lineage_builder", "queue_authority")
                event_records, queue_records = [], []
                for call, fact in event_calls:
                    arguments = r.arguments("superseder", call, supersede_env)
                    writer_env, writer_bindings = r.bind("superseder", "event_writer", call, supersede_env)
                    authority = [{"actual_call": target_fact,
                        "arguments": r.arguments("event_writer", target_call, writer_env)}
                        for target_call, target_fact in r.actual("event_writer", "event_authority")]
                    for index, value in enumerate(arguments):
                        if value.get("kind") == "record" and any(field.get("kind") == "literal" and isinstance(field.get("value"), str) for field in value["fields"].values()):
                            event_records.append({"call_fact_id": fact["id"], "argument_index": index,
                                "fields": value["fields"], "spreads": value.get("spreads", []), "all_arguments": arguments,
                                "event_writer_formal_actual_bindings": writer_bindings,
                                "actual_authority_forwarding": authority})
                for call, fact in queue_calls:
                    arguments = r.arguments("lineage_builder", call, lineage_env)
                    for index, value in enumerate(arguments):
                        if value.get("kind") == "record" and any(field.get("kind") == "record" for field in value["fields"].values()):
                            queue_records.append({"call_fact_id": fact["id"], "argument_index": index,
                                "fields": value["fields"], "all_arguments": arguments})
                shared = []
                for event in event_records:
                    for key, value in event["fields"].items():
                        if value.get("kind") != "input" or not value.get("declaration_id"):
                            continue
                        for queue in queue_records:
                            for path, field in _data_paths(queue["fields"]):
                                if field == value:
                                    shared.append({"event_field": key, "queue_field_path": path,
                                        "captured_origin_declaration_id": value["declaration_id"],
                                        "source_origin": value, "heap_or_runtime_identity_proven": False})
                selected.append(r.fact("conditional_supersession_lineage_source_relation", document, guard,
                    actual_guard=r.expr("completion", _field(guard, "condition")),
                    guard_source=document.text(_field(guard, "condition")),
                    status_guard_result_sources=predicate_sources,
                    callback_registration_call=runner_call, callback_location=document.location(callback),
                    supersede_call=supersede[0][1], lineage_call=lineage[0][1],
                    source_order_supersede_before_lineage=ordered, both_calls_awaited=awaited,
                    superseder_formal_actual_bindings=supersede_bindings, lineage_formal_actual_bindings=lineage_bindings,
                    event_records=event_records, queue_records=queue_records, shared_source_field_origins=shared,
                    conditions=["the registered callback is activated and reaches this actual captured branch",
                        "all preceding source calls and the first awaited operation complete normally",
                        "ordinary stable record/closure values; no Proxy, getters or external mutation"],
                    callback_activation_proven=False, event_durability_proven=False,
                    enqueue_always_reached_for_branch_proven=False, all_recovery_or_lineage_creation_proven=False))
    runner_doc, _, runner_fn = a.roles["callback_runner"]
    runner_params = _children(_field(runner_fn, "parameters"))
    runner_invocations = []
    for call, fact in r.calls("callback_runner"):
        callee = _operand(_field(call, "function"))
        identity = r.s.identity(runner_doc, callee)
        if not identity:
            continue
        for index, parameter in enumerate(runner_params):
            binder = _field(parameter, "pattern") or _field(parameter, "name") or parameter
            if r.s.identity(runner_doc, binder) == identity:
                runner_invocations.append(r.fact("captured_callback_parameter_invocation", runner_doc, call,
                    parameter_index=index, parameter_declaration_id=identity, actual_call=fact,
                    awaited=call.parent is not None and call.parent.type == "await_expression",
                    containing_conditions=a.branch_context(runner_doc, call, runner_fn), callback_runtime_activated=False))
    forwarding = []
    for call, fact in r.actual("event_writer", "event_authority"):
        forwarding.append(r.fact("event_writer_actual_authority_interface", a.roles["event_writer"][0], call,
            actual_call=fact, arguments=r.arguments("event_writer", call), durable_write_success_proven=False))
    parser_doc, _, parser_fn = a.roles["status_parser"]
    parser_sources = [a.expression(parser_doc, node) for node in a.nodes(parser_doc, _field(parser_fn, "body"))
                      if node.type in {"return_statement", "if_statement"}]
    parser_links = r.actual("completion", "status_parser", nested=True)
    lineage_doc, _, lineage_fn = a.roles["lineage_builder"]
    event_read_sources = [r.fact("lineage_materialized_record_source", lineage_doc, node,
        initializer_source=r.expr("lineage_builder", _field(node, "value")),
        captured_record_declaration_id=r.s.identity(lineage_doc, _field(node, "name")),
        runtime_record_or_task_identity_proven=False)
        for node in a.nodes(lineage_doc, _field(lineage_fn, "body"))
        if node.type == "variable_declarator" and _operand(_field(node, "value")) is not None
        and _operand(_field(node, "value")).type == "call_expression"
        and any(child.type == "await_expression" for child in a.nodes(lineage_doc, _field(node, "value")))]
    if not selected or not runner_invocations or not forwarding or not parser_links:
        a.gap("conditional_lineage_required_source_relation_missing", selected=len(selected),
            callback_invocations=len(runner_invocations), event_authority_links=len(forwarding), parser_links=len(parser_links))
    supported = bool(selected and runner_invocations and forwarding and parser_links and all(
        row["source_order_supersede_before_lineage"] and row["both_calls_awaited"] and row["event_records"]
        and row["queue_records"] and row["shared_source_field_origins"] for row in selected))
    statements = []
    if supported:
        for row in selected:
            literals = [{key: value["value"] for key, value in event["fields"].items()
                if value.get("kind") == "literal"} for event in row["event_records"]]
            origins = [{"event_field": value["event_field"], "queue_field": value["queue_field_path"],
                "input": value["source_origin"].get("name")} for value in row["shared_source_field_origins"]]
            statements.append("所选回调到达实际条件 " + row["guard_source"]
                + " 且前序 await 正常完成时，源码先调用 supersession 接口，再调用 lineage 接口；"
                + "前一接口向已绑定事件写者传递的字面字段为 " + json.dumps(literals, ensure_ascii=False, separators=(",", ":"))
                + "。后续 queue 入参中与该事件共享同一词法输入的字段为 " + json.dumps(origins, ensure_ascii=False, separators=(",", ":"))
                + "；lineage helper 内的提前返回、抛出及外部操作失败仍可阻止实际入队。")
    return {"lineage_relations": selected, "callback_invocation_sources": runner_invocations,
        **({"statement": "\n".join(statements), "interpretation":
            "这里闭合的是实际状态条件、事件字面字段及旧任务到后续任务的字段来源；并未证明回调必然激活、事件持久化成功、每次创建新任务或覆盖全部恢复路径。"} if supported else {}),
        "event_authority_interfaces": forwarding, "status_parser_source": parser_sources,
        "parser_call_sources": [fact for _, fact in parser_links],
        "lineage_record_load_sources": event_read_sources,
        "entry_countercase_guards": r.guards("completion", nested=True),
        "lineage_builder_countercase_guards": r.guards("lineage_builder"),
        "scoped_source_supported": supported,
        "relation_witnesses": [{"subject": row["guard_source"],
            "source_order_supersede_before_lineage": row["source_order_supersede_before_lineage"],
            "event_literal_fields": [{key: value for key, value in event["fields"].items() if value.get("kind") == "literal"}
                                      for event in row["event_records"]],
            "shared_source_field_origins": row["shared_source_field_origins"],
            "event_durability_proven": False, "all_lineage_creation_proven": False} for row in selected]}


def _data_paths(value: Any, path: str = ""):
    if isinstance(value, dict):
        if value.get("kind"):
            yield path, value
        if value.get("kind") == "record":
            for key, child in value["fields"].items():
                yield from _data_paths(child, path + "/" + key)
        elif "kind" not in value:
            for key, child in value.items():
                yield from _data_paths(child, path + "/" + key)


def _finite_value(value: dict, bindings: dict) -> Any:
    if value.get("kind") == "modeled_boolean_coercion":
        answer = _truth(_finite_value(value["operand"], bindings))
        return _UNKNOWN if answer is None else answer
    if value.get("kind") == "binary":
        op = value["operator"]
        left = _finite_value(value["left"], bindings)
        if op in {"&&", "||"}:
            truth = _truth(left)
            if truth is None:
                return _UNKNOWN
            return _finite_value(value["right"], bindings) if truth == (op == "&&") else left
        right = _finite_value(value["right"], bindings)
        if left is _UNKNOWN or right is _UNKNOWN:
            return _UNKNOWN
        if op in {"===", "!=="}:
            equal = type(left) is type(right) and left == right
            return equal if op == "===" else not equal
        return _UNKNOWN
    if value.get("kind") == "not":
        truth = _truth(_finite_value(value["operand"], bindings))
        return _UNKNOWN if truth is None else not truth
    return _abstract(value, bindings)


def _mode_partition(r: _Relations) -> dict:
    document, _, function = r.a.roles["finalizer"]
    candidates = []
    for statement in _children(_field(function, "body")):
        if statement.type != "lexical_declaration":
            continue
        for declaration in _children(statement):
            value = _operand(_field(declaration, "value"))
            fields = _record(document, value)
            if len(fields) < 3:
                continue
            simple = [node for node in fields.values() if _operand(node).type in {"binary_expression", "unary_expression", "identifier"}]
            if len(simple) >= 3:
                expression = r.expr("finalizer", value, expand=True)
                comparisons = [node for node in _walk_data(expression) if isinstance(node, dict)
                    and node.get("kind") == "binary" and node.get("operator") in {"===", "!=="}
                    and node.get("left", {}).get("kind") == "input" and node.get("right", {}).get("kind") == "literal"
                    and isinstance(node["right"].get("value"), str)]
                by_id = defaultdict(set)
                for node in comparisons:
                    by_id[node["left"]["declaration_id"]].add(node["right"]["value"])
                if len(by_id) == 1:
                    candidates.append((declaration, expression, by_id))
    if len(candidates) != 1:
        r.a.gap("publication_boolean_plan_not_unique", candidates=len(candidates))
        return {"complete": False, "rows": []}
    declaration, expression, domains = candidates[0]
    enum_id, literals = next(iter(domains.items()))
    guards = r.guards("finalizer", before=declaration)
    boolean_formals = []
    for node in r.a.nodes(document, _field(function, "parameters")):
        if node.type not in {"object_assignment_pattern", "assignment_pattern"}:
            continue
        binder = _field(node, "left") or _field(node, "name") or next(iter(_children(node)), None)
        default = _field(node, "right") or _field(node, "value")
        if binder is not None and default is not None and _operand(default).type in {"true", "false"}:
            identity = r.s.identity(document, binder)
            if identity:
                boolean_formals.append({"declaration_id": identity, "name": document.text(binder),
                    "default_literal": document.text(default) == "true", "source": document.location(node)})
    boolean_ids = {row["declaration_id"] for row in boolean_formals}
    # Find only the relevant mode/opt-in guard slice, not every function path.
    relevant = []
    for guard in guards:
        if not guard.get("direct_owner_body_statement"):
            continue
        condition = guard["condition"]
        inputs = {item["declaration_id"] for item in _walk_data(condition) if isinstance(item, dict) and item.get("kind") == "input"}
        members = [item for item in _walk_data(condition) if isinstance(item, dict) and item.get("kind") in {"opaque_call", "get", "opaque_expression"}]
        if enum_id in inputs and not members and inputs - {enum_id} <= boolean_ids:
            relevant.append(guard)
            for item in _walk_data(condition):
                if (isinstance(item, dict) and item.get("kind") == "binary" and item.get("operator") in {"===", "!=="}
                        and item.get("left", {}).get("declaration_id") == enum_id
                        and item.get("right", {}).get("kind") == "literal" and isinstance(item["right"].get("value"), str)):
                    literals.add(item["right"]["value"])
    flags = sorted({item["declaration_id"] for guard in relevant for item in _walk_data(guard["condition"])
        if isinstance(item, dict) and item.get("kind") == "input" and item.get("declaration_id") != enum_id})
    if len(flags) > 4 or (len(literals) + 1) * 2 ** len(flags) > _PATH_LIMIT:
        r.a.gap("publication_mode_partition_budget_or_input_shape_unknown")
        return {"complete": False, "rows": []}
    rows = []
    for enum in [*sorted(literals), "<other-than-source-mode-literals>"]:
        for flag_values in itertools.product([False, True], repeat=len(flags)):
            bindings = {enum_id: enum, **dict(zip(flags, flag_values))}
            results = [_truth(_finite_value(guard["condition"], bindings)) for guard in relevant]
            blocked = next((guard["id"] for guard, result in zip(relevant, results) if result is True and guard["consequence_abrupt"]), None)
            fields = {}
            for key, value in expression.get("fields", {}).items():
                actual = _finite_value(value, bindings)
                fields[key] = actual if type(actual) is bool else {"unknown": True, "source_expression": value}
            rows.append({"mode_cell": enum, "boolean_input_cells": dict(zip(flags, flag_values)),
                "selected_prefix_guard_blocks": blocked, "prefix_guard_values_complete": all(value is not None for value in results),
                "source_plan_fields": fields, "plan_is_not_actual_remote_effect": True})
    return {"complete": bool(relevant and rows) and all(row["prefix_guard_values_complete"] for row in rows),
        "enum_declaration_id": enum_id, "source_enum_literals": sorted(literals), "boolean_input_declaration_ids": flags,
        "source_boolean_default_formals": boolean_formals,
        "only_direct_owner_body_prefix_mode_guards_interpreted": True,
        "other_local_state_and_nested_branch_guards_not_boolean_options": True,
        "plan_source": r.fact("publication_boolean_plan_source", document, declaration,
            expression=expression, plan_effect_or_reaching_proven=False),
        "selected_prefix_guards": relevant, "rows": rows,
        "scope": "Only actual enum/opt-in Boolean guards and the declared Boolean plan; all other source preconditions remain required.",
        "ordinary_boolean_options_and_unshadowed_standard_Boolean_model_required": True}


def _publication(r: _Relations) -> dict:
    a = r.a
    partition = _mode_partition(r)
    document, _, function = a.roles["finalizer"]
    effects = []
    for target in ("pr_boundary", "push_boundary", "local_git_executor", "review_bundle"):
        for call, fact in r.actual("finalizer", target):
            effects.append(r.fact("conditional_publication_interface_frontier", document, call,
                target_role=target, actual_call=fact, actual_callee_source=fact["callee_source"],
                arguments=r.arguments("finalizer", call),
                containing_conditions=a.branch_context(document, call, function),
                preceding_abrupt_source_guards=r.guards("finalizer", before=call),
                source_order_position=call.start_byte, callee_or_remote_effect_success_proven=False))
    pr_doc, _, pr_fn = a.roles["pr_boundary"]
    pr_guards = r.guards("pr_boundary")
    pr_frontiers = []
    for call, fact in r.calls("pr_boundary"):
        callee = _operand(_field(call, "function"))
        if callee is None or callee.type != "identifier":
            continue
        record = a.lexical(pr_doc).resolve_identity(callee)
        declaration = a.lexical(pr_doc).declaration_for(record)
        initializer = _operand(_field(declaration, "value"))
        if initializer is None or initializer.type not in {"ternary_expression", "conditional_expression"}:
            continue
        functions = [node for node in a.nodes(pr_doc, initializer, nested=True) if node.type in _FUNCTIONS]
        if len(functions) >= 2:
            pr_frontiers.append(r.fact("conditional_injected_or_default_transport_frontier", pr_doc, call,
                actual_call=fact, transport_binding=record, conditional_transport_source=a.expression(pr_doc, initializer),
                preceding_abrupt_source_guards=[guard for guard in pr_guards if guard["location"]["start_byte"] < call.start_byte],
                preceding_awaited_source_calls=[step for node, step in r.calls("pr_boundary") if node.start_byte < call.start_byte
                    and node.parent is not None and node.parent.type == "await_expression"],
                opaque_effect_frontier=True, provider_binding_repaired=False, remote_creation_or_authorization_success_proven=False))
    options_relations = _publication_options(r, pr_guards, pr_frontiers)
    push_doc, _, push_fn = a.roles["push_boundary"]
    push_commands = []
    for call, fact in r.actual("push_boundary", "git_executor", nested=True):
        arguments = _children(_field(call, "arguments"))
        for argument in arguments:
            array = _operand(argument)
            if array is None or array.type != "array" or not _children(array):
                continue
            literal = _literal_string(push_doc.text(_children(array)[0]))
            if literal is not None:
                push_commands.append(r.fact("captured_git_command_interface", push_doc, call,
                    actual_call=fact, command_literal=literal, argument_sources=r.arguments("push_boundary", call),
                    containing_conditions=a.branch_context(push_doc, call, _body_owner(call)),
                    preceding_source_calls=[step for node, step in r.calls("push_boundary", root=_field(_body_owner(call), "body"))
                        if node.start_byte < call.start_byte and node.parent is not None and node.parent.type == "await_expression"],
                    command_executed=False, remote_transport_or_authority_success_proven=False))
    direct_opaque = []
    for call, fact in r.calls("finalizer"):
        callee = _operand(_field(call, "function"))
        if callee is None or callee.type != "identifier":
            continue
        identity = r.s.identity(document, callee)
        if not identity or fact.get("actual_callee_graph_node_id"):
            continue
        record = a.lexical(document).resolve_identity(callee)
        declaration = a.lexical(document).declaration_for(record)
        initializer = _operand(_field(declaration, "value"))
        if record.get("parameter_index") is None and (initializer is None or initializer.type not in {"ternary_expression", "conditional_expression"}):
            continue
        contexts = a.branch_context(document, call, function)
        if contexts:
            direct_opaque.append(r.fact("conditional_opaque_publication_callback", document, call,
                actual_call=fact, callee_declaration_id=identity, arguments=r.arguments("finalizer", call),
                declaration_source=a.expression(document, declaration) if declaration is not None else None,
                containing_conditions=contexts, preceding_abrupt_source_guards=r.guards("finalizer", before=call),
                opaque_effect_frontier=True, artificial_calls_edge_created=False, callback_effect_proven=False))
    remote_commands = [row for row in push_commands if row["command_literal"] == "push"]
    git_doc, _, git_fn = a.roles["git_executor"]
    executor_calls = [r.fact("structured_git_executor_source_interface", git_doc, call,
        actual_call=fact, arguments=r.arguments("git_executor", call),
        opaque_execution_frontier=True, command_or_remote_success_proven=False)
        for call, fact in r.calls("git_executor")
        if any(_literal_string(git_doc.text(argument)) == "git" for argument in _children(_field(call, "arguments")))]
    callback_defaults = _optional_callback_interfaces(r, push_commands)
    prefix_guards = partition.get("selected_prefix_guards", [])
    earliest_mode_guard = min((guard["location"]["start_byte"] for guard in prefix_guards), default=None)
    earlier_alternatives = [{"interface_fact_id": row["id"], "callee_source": row["actual_callee_source"],
        "containing_conditions": row["containing_conditions"], "source_order_position": row["source_order_position"],
        "selected_mode_guard_fact_ids": [guard["id"] for guard in prefix_guards],
        "precedes_selected_mode_permission_guards": True,
        "effect_or_no_io_postcondition_proven": False}
        for row in effects if row["target_role"] == "review_bundle" and earliest_mode_guard is not None
        and row["source_order_position"] < earliest_mode_guard]
    if not partition.get("complete") or not effects or not pr_frontiers or not remote_commands or not options_relations or not executor_calls:
        a.gap("conditional_publication_boundary_required_source_relation_missing",
            finite_partition_complete=partition.get("complete"), interfaces=len(effects), pr_frontiers=len(pr_frontiers),
            remote_git_commands=len(remote_commands), options_relations=len(options_relations), git_executor_interfaces=len(executor_calls))
    supported = bool(partition.get("complete") and effects and pr_frontiers and remote_commands and options_relations and executor_calls)
    fact_lookup = {fact["id"]: fact for fact in a.source_facts}
    consumer_conditions = sorted({fact_lookup[consumer["id"]]["original_condition"]
        for row in options_relations for consumer in row["actual_guard_consumers"]
        if fact_lookup[consumer["id"]].get("blocks_selected_transport_on_true")})
    plan_fields = sorted(partition.get("plan_source", {}).get("expression", {}).get("fields", {}))
    statement = ("源码实际模式字面量为 " + json.dumps(partition.get("source_enum_literals", []), ensure_ascii=False)
        + "，声明的 plan 字段为 " + json.dumps(plan_fields, ensure_ascii=False)
        + "。有限表组合这些模式与源码中的布尔 opt-in，并保留字段 unknown；plan 不是已发生的写入。"
        + "PR 调用的真实选项绑定到 callee 形参后，源码中早于条件 transport 且成立时 return 的条件包括 "
        + json.dumps(consumer_conditions, ensure_ascii=False) + "。"
        + ("另有实际 review-bundle 分支在所选模式/权限 guard 之前调用其他接口，不能把后续 guard 推广为整个函数无本地 IO 的保证。"
            if earlier_alternatives else "")
        + "远端命令接口的实际 Git 首参数为 " + json.dumps(sorted({row["command_literal"] for row in remote_commands}), ensure_ascii=False)
        + "；注入 callback、授权结果、命令执行及远端后置条件保持未知。")
    return {"finite_mode_permission_relation": partition, "conditional_effect_interfaces": effects,
        **({"statement": statement, "interpretation":
            "区分的是实际枚举/opt-in 条件、PR 提前返回和源码发布接口；配置允许与真实外写成功是不同证据。可空通用 callback 的默认值与所选 caller 提供的字段另列，未推广为全项目必然授权。"} if supported else {}),
        "pull_request_boundary_guards": pr_guards, "pull_request_transport_frontiers": pr_frontiers,
        "pull_request_options_and_guard_bindings": options_relations,
        "git_command_frontiers": push_commands, "remote_git_command_frontiers": remote_commands,
        "git_executor_source_interfaces": executor_calls, "opaque_callback_frontiers": direct_opaque,
        "optional_callback_source_interfaces": callback_defaults,
        "earlier_alternate_interface_witnesses": earlier_alternatives,
        "scoped_source_supported": supported,
        "relation_witnesses": [{"interface": row["target_role"], "callee_source": row["actual_callee_source"],
            "conditions": row["containing_conditions"], "normal_source_position": row["source_order_position"],
            "effect_success_proven": False} for row in effects],
        "selected_mode_guard_witnesses": [{"guard_fact_id": guard["id"], "condition_source": guard["condition_source"],
            "condition": guard["condition"], "consequence_abrupt": guard["consequence_abrupt"]} for guard in prefix_guards],
        "option_guard_witnesses": [{"boundary_fact_id": row["actual_boundary_call"]["id"],
            "option_fields": sorted(row["source_options_fields"]),
            "formal_actual_bindings": row["formal_actual_bindings"],
            "consumer_guard_fact_ids": [guard["id"] for guard in row["actual_guard_consumers"]]} for row in options_relations],
        "scope": {"mode_guards_do_not_cover_earlier_review_bundle_branch": bool(earlier_alternatives),
            "global_no_local_io_postcondition_proven": False,
            "all_generic_push_configurations_have_an_authorizer_proven": False,
            "source_plan_fields_are_not_actual_effect_execution": True,
            "all_recovery_paths_or_external_postconditions_proven": False}}


def _optional_callback_interfaces(r: _Relations, commands: list[dict]) -> list[dict]:
    """Expose source defaults/guards for callable parameters, without binding IO."""
    a = r.a
    document, _, function = a.roles["push_boundary"]
    parameters = _field(function, "parameters")
    defaults = []
    for node in a.nodes(document, parameters):
        if node.type not in {"object_assignment_pattern", "assignment_pattern"}:
            continue
        binder = _field(node, "left") or _field(node, "name") or next(iter(_children(node)), None)
        value = _field(node, "right") or _field(node, "value")
        if binder is None or value is None or _operand(value).type != "null":
            continue
        identity = r.s.identity(document, binder)
        if not identity:
            continue
        invocations = [(call, fact) for call, fact in r.calls("push_boundary", nested=True)
            if r.s.identity(document, _operand(_field(call, "function"))) == identity]
        if not invocations:
            continue
        caller_fields = []
        name = document.text(binder)
        for call, fact in r.actual("finalizer", "push_boundary"):
            arguments = _children(_field(call, "arguments"))
            source_fields = _record(a.roles["finalizer"][0], arguments[0]) if arguments else {}
            if name in source_fields:
                caller_fields.append({"actual_call_fact_id": fact["id"], "source_field": name,
                    "value_source": a.expression(a.roles["finalizer"][0], source_fields[name])})
        defaults.append(r.fact("optional_publication_callback_source_interface", document, node,
            parameter_name=name, formal_declaration_id=identity, default_source=r.expr("push_boundary", value),
            selected_caller_field_sources=caller_fields,
            actual_invocations=[{"actual_call": fact,
                "containing_conditions": a.branch_context(document, call, _body_owner(call)),
                "awaited": call.parent is not None and call.parent.type == "await_expression",
                "source_position": call.start_byte} for call, fact in invocations],
            captured_command_fact_ids=[row["id"] for row in commands],
            injected_callable_activation_or_authorization_success_proven=False,
            omitted_default_is_not_a_mandatory_callback_proof=True))
    return defaults


def _publication_options(r: _Relations, pr_guards: list[dict], frontiers: list[dict]) -> list[dict]:
    """Replay only captured plain Object.assign option shapes, never effects."""
    a = r.a
    document, _, function = a.roles["finalizer"]
    target_doc, _, target_fn = a.roles["pr_boundary"]
    result = []
    all_calls = r.calls("finalizer")
    def patches(reference: Any, before: Any) -> tuple[dict, list[dict]]:
        identity = r.s.identity(document, reference)
        fields, records = {}, []
        if not identity:
            return fields, records
        for call, fact in all_calls:
            if call.start_byte >= before.start_byte:
                continue
            callee = _operand(_field(call, "function"))
            if callee is None or callee.type != "member_expression" or _key(document, _field(callee, "property")) != "assign":
                continue
            receiver = _field(callee, "object")
            if document.text(receiver) != "Object" or not a.lexical(document).unbound("Object", receiver).get("local_declaration_absent"):
                continue
            arguments = _children(_field(call, "arguments"))
            if len(arguments) < 2 or r.s.identity(document, arguments[0]) != identity:
                continue
            for argument in arguments[1:]:
                value = r.expr("finalizer", argument, expand=True)
                if value.get("kind") == "record" and not value.get("spreads"):
                    fields.update(value["fields"])
                else:
                    fields.clear()
                records.append(r.fact("captured_plain_options_assign_patch", document, call,
                    actual_call=fact, target_declaration_id=identity, source_argument_location=document.location(argument),
                    source_argument=value, registered_Object_assign_model=True,
                    ordinary_target_source_no_getters_proxy_external_mutation_required=True))
        return fields, records
    for call, fact in r.actual("finalizer", "pr_boundary"):
        arguments = _children(_field(call, "arguments"))
        if not arguments:
            continue
        original = _operand(arguments[0])
        records = []
        if original.type == "identifier":
            fields, records = patches(original, call)
        elif original.type == "object":
            fields = {}
            for child in _children(original):
                if child.type == "spread_element":
                    spread = _operand(next(iter(_children(child)), None))
                    if spread is not None and spread.type == "identifier":
                        fields, found = patches(spread, call)
                        records.extend(found)
                    else:
                        fields.clear()
                elif child.type == "pair":
                    key = _key(document, _field(child, "key"))
                    if key is not None:
                        fields[key] = r.expr("finalizer", _field(child, "value"), expand=True)
                    else:
                        fields.clear()
                elif child.type == "shorthand_property_identifier":
                    fields[document.text(child)] = r.expr("finalizer", child, expand=True)
                else:
                    fields.clear()
        else:
            continue
        bindings, binding_rows = {}, []
        for parameter in _children(_field(target_fn, "parameters")):
            pattern = _operand(_field(parameter, "pattern") or _field(parameter, "name") or parameter)
            if pattern is None or pattern.type != "object_pattern":
                continue
            for binder in _children(pattern):
                identifier = binder
                if binder.type in {"object_assignment_pattern", "assignment_pattern"}:
                    identifier = _field(binder, "left") or _field(binder, "name") or next(iter(_children(binder)), None)
                elif binder.type == "pair_pattern":
                    identifier = _field(binder, "value")
                key = _key(target_doc, identifier)
                identity = r.s.identity(target_doc, identifier)
                if key in fields and identity:
                    bindings[identity] = fields[key]
                    binding_rows.append({"source_option_field": key, "source_value": fields[key],
                        "callee_formal_declaration_id": identity, "formal_location": target_doc.location(identifier)})
        if not binding_rows:
            a.gap("publication_options_callee_destructuring_binding_missing", document, call)
            continue
        consumers = []
        for guard in a.nodes(target_doc, _field(target_fn, "body")):
            if guard.type != "if_statement" or guard.parent != _field(target_fn, "body") or not _abrupt(_field(guard, "consequence")):
                continue
            condition = _field(guard, "condition")
            refs = {r.s.identity(target_doc, node) for node in a.nodes(target_doc, condition) if node.type == "identifier"}
            if not refs.intersection(bindings):
                continue
            consumers.append(r.fact("publication_options_consumed_by_abrupt_guard", target_doc, guard,
                original_condition=target_doc.text(condition), composed_condition=r.expr("pr_boundary", condition, bindings),
                bound_formal_ids=sorted(refs.intersection(bindings)),
                blocks_selected_transport_on_true=[frontier["actual_call"]["id"] for frontier in frontiers
                    if guard.end_byte < frontier["location"]["start_byte"]],
                callback_or_io_effect_before_this_guard_excluded=False, runtime_guard_selected=False))
        result.append(r.fact("publication_call_options_to_callee_guards", document, call,
            actual_boundary_call=fact, source_options_fields=fields, source_assign_patches=records,
            formal_actual_bindings=binding_rows, actual_guard_consumers=consumers,
            branch_conditions=a.branch_context(document, call, function),
            normal_plain_record_scope_only=True, remote_or_PR_success_proven=False))
    return result


def analyze_pattern(analysis: Any) -> dict:
    r = _Relations(analysis)
    roles = LINEAGE_ROLES if analysis.rule["type"] == "conditional_state_lineage" else PUBLICATION_ROLES
    missing = sorted(roles - set(analysis.roles))
    start = len(analysis.gaps)
    if missing:
        analysis.gap("state_lineage_publication_roles_missing", missing=missing)
        result = {"scoped_source_supported": False}
    else:
        result = _lineage(r) if analysis.rule["type"] == "conditional_state_lineage" else _publication(r)
    gaps = analysis.gaps[start:]
    result.update(version=VERSION, model=MODEL, necessary_gaps=gaps,
        scoped_source_supported=bool(result.get("scoped_source_supported") and not gaps and not analysis.incomplete),
        target_executed=False, target_tests_run=False, target_build_run=False,
        trusted_model={"id": MODEL, "origin": "trusted-model", "normal_source_order_and_stable_plain_records": True,
            "finite_literal_boolean_enum_abstract_interpretation_only": True,
            "opaque_calls_callback_activation_io_durability_and_remote_success_unproved": True},
        all_project_functionality_proven=False)
    statements_closed = bool(result["scoped_source_supported"]
        and all(analysis.role_binding_closed.get(role, False) for role in roles))
    if not statements_closed:
        result.pop("statement", None)
        result.pop("interpretation", None)
    result["source_statement_relation_closed"] = statements_closed
    result["source_fact_reference_contract"] = {
        "kind": "single-flat-source-facts-with-id-references",
        "lookup": "Resolve source_fact_id against this same analysis.source_facts[].id; no target graph edge is created.",
        "fact_count": len(analysis.source_facts)}
    return r.compact(result)
