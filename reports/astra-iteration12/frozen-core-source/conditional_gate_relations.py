"""Finite conditional gate summaries over authenticated, captured JavaScript.

This is an abstract interpreter for a deliberately small CST vocabulary.  It
does not compile, import or execute target programs.  Opaque calls stay opaque;
normal source continuation and plain, stable data properties are assumptions,
not inferred runtime effects.  Selectors identify declarations only.
"""
from __future__ import annotations

import itertools
import json
from typing import Any

from .semantic_sources import unwrap
from .static_contracts import _literal_string

VERSION = "captured-conditional-gate-relations-1"
MODEL = "finite-js-plain-record-gate-conditions-v1"
GROUPS = {
    "readiness": frozenset({"readiness_entry", "readiness_predicate"}),
    "completion": frozenset({"completion_evaluator", "mutating_predicate", "gate_result"}),
    "access_audit": frozenset({"access_server", "response_writer", "audit_opener"}),
}
_FUNCTIONS = {"function_declaration", "function_expression", "arrow_function", "method_definition",
              "generator_function", "generator_function_declaration"}
_ERASED = {"comment", "type_annotation", "type_arguments", "type_parameters"}
_LIMIT = 256


def _field(node: Any, key: str) -> Any:
    return node.child_by_field_name(key) if node is not None else None


def _children(node: Any) -> list[Any]:
    return [child for child in node.named_children if child.type not in _ERASED
            and not child.type.endswith("_type")] if node is not None else []


def _operand(node: Any) -> Any:
    node = unwrap(node)
    while node is not None and node.type == "await_expression":
        node = unwrap(next(iter(_children(node)), None))
    return node


def _key(document: Any, node: Any) -> str | None:
    if node is None:
        return None
    if node.type in {"identifier", "property_identifier", "shorthand_property_identifier",
                     "shorthand_property_identifier_pattern"}:
        return document.text(node)
    return _literal_string(document.text(node)) if node.type == "string" else None


def _inside(outer: Any, inner: Any) -> bool:
    return bool(outer is not None and inner is not None and outer.start_byte <= inner.start_byte
                and inner.end_byte <= outer.end_byte)


def _literal(value: Any) -> dict:
    return {"kind": "literal", "value": value}


def _not(value: dict) -> dict:
    if value.get("kind") == "not":
        return value["operand"]
    return {"kind": "not", "operand": value}


def _same(a: dict, b: dict) -> bool:
    return a == b


def _must_abrupt(node: Any) -> bool:
    if node is None:
        return False
    if node.type in {"return_statement", "throw_statement"}:
        return True
    if node.type == "statement_block":
        return any(_must_abrupt(child) for child in _children(node))
    return node.type == "if_statement" and _must_abrupt(_field(node, "consequence")) and _must_abrupt(_field(node, "alternative"))


class _Summary:
    def __init__(self, analysis: Any):
        self.a = analysis
        self.by_target = {definition.graph_node_id: role for role, (_, definition, _) in analysis.roles.items()}
        self.call_facts = {node.id: fact for fact in analysis.source_facts
                           if fact.get("kind") == "captured_call_step"
                           for item in [analysis.call_nodes.get(fact["id"])] if item
                           for node in [item[2]]}
        self.predicates: dict[str, dict] = {}
        self.expression_cache: dict[tuple[str, int, str], dict] = {}
        self.truncated = False

    def identity(self, document: Any, node: Any) -> str | None:
        if node is None or node.type not in {"identifier", "shorthand_property_identifier",
                                             "shorthand_property_identifier_pattern"}:
            return None
        record = self.a.lexical(document).resolve_identity(node)
        return record.get("declaration_id") if record.get("state") == "unique" and record.get("identity_complete") else None

    def fact(self, kind: str, document: Any, node: Any, **details: Any) -> dict:
        return self.a.fact(kind, document, node, conditional_gate_version=VERSION, **details)

    def call(self, role: str, document: Any, node: Any) -> dict:
        if node.id not in self.call_facts:
            _, definition, function = self.a.roles[role]
            self.call_facts[node.id] = self.a.call(role, document, definition, function, node)
        return self.call_facts[node.id]

    def expr(self, role: str, document: Any, original: Any, env: dict, depth: int = 0) -> dict:
        node = _operand(original)
        if node is None:
            return {"kind": "missing"}
        if depth > 32:
            self.truncated = True
            return {"kind": "unknown", "reason": "conditional_expression_depth_limit"}
        literal = _literal_string(document.text(node))
        if literal is not None:
            return _literal(literal)
        if node.type in {"true", "false", "null", "number"}:
            raw = document.text(node)
            if raw in {"true", "false", "null"}:
                return _literal({"true": True, "false": False, "null": None}[raw])
            try:
                return _literal(json.loads(raw))
            except ValueError:
                pass
        if node.type in {"identifier", "shorthand_property_identifier"}:
            identity = self.identity(document, node)
            if identity and identity in env:
                return env[identity]
            return {"kind": "input", "name": document.text(node), "declaration_id": identity}
        if node.type in {"member_expression", "subscript_expression"}:
            root = self.expr(role, document, _field(node, "object"), env, depth + 1)
            key = _key(document, _field(node, "property") or _field(node, "index"))
            if root.get("kind") == "record" and key in root["fields"]:
                return root["fields"][key]
            return {"kind": "get", "object": root, "key": key,
                    "optional": any(child.type == "optional_chain" for child in node.children)}
        if node.type == "object":
            fields, spreads = {}, []
            for child in _children(node):
                if child.type == "pair":
                    key = _key(document, _field(child, "key"))
                    value = self.expr(role, document, _field(child, "value"), env, depth + 1)
                elif child.type == "shorthand_property_identifier":
                    key, value = document.text(child), self.expr(role, document, child, env, depth + 1)
                elif child.type == "spread_element":
                    spreads.append(self.expr(role, document, next(iter(_children(child)), None), env, depth + 1))
                    continue
                else:
                    spreads.append({"kind": "unknown", "source_type": child.type})
                    continue
                if key is None or key in fields or key == "__proto__":
                    return {"kind": "unknown", "reason": "non_plain_record"}
                fields[key] = value
            return {"kind": "record", "fields": fields, "spreads": spreads}
        if node.type == "binary_expression":
            return {"kind": "binary", "operator": document.text(_field(node, "operator")),
                    "left": self.expr(role, document, _field(node, "left"), env, depth + 1),
                    "right": self.expr(role, document, _field(node, "right"), env, depth + 1)}
        if node.type == "unary_expression":
            operand = _field(node, "argument") or next(iter(_children(node)), None)
            op = document.text(_field(node, "operator")) or next((child.type for child in node.children if not child.is_named), "")
            return _not(self.expr(role, document, operand, env, depth + 1)) if op == "!" else {
                "kind": "unary", "operator": op, "operand": self.expr(role, document, operand, env, depth + 1)}
        if node.type == "array":
            return {"kind": "array", "items": [self.expr(role, document, child, env, depth + 1)
                                                   for child in _children(node)]}
        if node.type in {"call_expression", "new_expression"}:
            fact = self.call(role, document, node)
            args = [self.expr(role, document, item, env, depth + 1) for item in _children(_field(node, "arguments"))]
            target = self.by_target.get(fact.get("actual_callee_graph_node_id"))
            if target in self.predicates and len(args) == 1:
                summary = self.predicates[target]
                return {"kind": "predicate_application", "predicate_role": target,
                        "callee_graph_node_id": fact["actual_callee_graph_node_id"],
                        "authenticated_call_edge_id": fact["authenticated_call_edge_id"],
                        "argument": args[0], "summary": summary}
            return {"kind": "opaque_call", "source": fact["callee_source"], "arguments": args,
                    "call_fact_id": fact["id"], "actual_target_role": target,
                    "return_value_or_effect_proven": False}
        return {"kind": "opaque_expression", "source_type": node.type,
                "location": document.location(node), "source": document.text(node)[:1024]}

    def paths(self, role: str) -> list[dict]:
        document, _, function = self.a.roles[role]
        initial = {"guards": [], "env": {}, "trace": []}
        def block(node: Any, states: list[dict]) -> tuple[list[dict], list[dict]]:
            statements = _children(node) if node is not None and node.type == "statement_block" else [node] if node is not None else []
            done = []
            for statement in statements:
                continuing = []
                for state in states:
                    if len(done) + len(continuing) > _LIMIT:
                        self.truncated = True
                        break
                    if statement.type in {"lexical_declaration", "variable_declaration"}:
                        env = dict(state["env"])
                        for declaration in _children(statement):
                            if declaration.type != "variable_declarator":
                                continue
                            name = _field(declaration, "name")
                            identity = self.identity(document, name)
                            if identity:
                                env[identity] = self.expr(role, document, _field(declaration, "value"), env)
                        continuing.append({**state, "env": env})
                    elif statement.type == "if_statement":
                        condition = self.expr(role, document, _field(statement, "condition"), state["env"])
                        fact = self.fact("conditional_gate_predicate", document, _field(statement, "condition"),
                                         role=role, expression=condition, runtime_selected=False)
                        for branch, truth in [("consequence", True), ("alternative", False)]:
                            next_state = {**state, "env": dict(state["env"]),
                                "guards": [*state["guards"], {"condition": condition, "equals_truth": truth,
                                                              "predicate_fact_id": fact["id"]}]}
                            live, terminated = block(_field(statement, branch), [next_state])
                            continuing.extend(live)
                            done.extend(terminated)
                    elif statement.type in {"return_statement", "throw_statement"}:
                        returned = self.expr(role, document, next(iter(_children(statement)), None), state["env"])
                        fact = self.fact("conditional_gate_abrupt_completion", document, statement, role=role,
                            completion_kind=statement.type, path_conditions=state["guards"], returned_value=returned,
                            normal_preceding_operations_required=True, runtime_completion_proven=False)
                        done.append({"conditions": state["guards"], "completion_kind": statement.type,
                                     "value": returned, "fact_id": fact["id"], "location": document.location(statement)})
                    elif statement.type == "statement_block":
                        live, terminated = block(statement, [state])
                        continuing.extend(live)
                        done.extend(terminated)
                    elif statement.type in {"expression_statement", "empty_statement"}:
                        # Nonlocal effects and opaque calls are not interpreted.
                        value = _operand(next(iter(_children(statement)), None))
                        if value is not None and value.type in {"assignment_expression", "augmented_assignment_expression", "update_expression"}:
                            self.a.gap("conditional_gate_expression_write_not_interpreted", document, value, role=role)
                        continuing.append(state)
                    else:
                        self.a.gap("conditional_gate_statement_not_interpreted", document, statement,
                                   role=role, statement_type=statement.type)
                        continuing.append(state)
                states = continuing[:_LIMIT]
                if not states:
                    break
            return states, done
        active, done = block(_field(function, "body"), [initial])
        if active:
            self.a.gap("conditional_gate_function_fallthrough_unknown", role=role, paths=len(active))
        return done

    def predicate(self, role: str) -> dict:
        document, _, function = self.a.roles[role]
        parameters = _children(_field(function, "parameters"))
        binders = [_field(node, "pattern") or _field(node, "name") or node for node in parameters]
        identifiers = [binder for binder in binders if binder is not None and binder.type == "identifier"]
        parameter = self.identity(document, identifiers[0]) if len(identifiers) == 1 else None
        paths = self.paths(role)
        result = {"role": role, "parameter_declaration_id": parameter, "return_paths": paths,
                  "plain_stable_input_model_required": True,
                  "all_return_values_boolean_literals": bool(paths) and all(path["value"].get("kind") == "literal"
                      and type(path["value"].get("value")) is bool for path in paths)}
        self.predicates[role] = result
        return result


def _walk_data(value: Any):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from _walk_data(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_data(child)


class _Missing:
    pass


_MISSING = _Missing()
_UNKNOWN = object()


def _truth(value: Any) -> bool | None:
    if value is _UNKNOWN:
        return None
    if value is _MISSING or value is None or value is False or value == 0 or value == "":
        return False
    return True


def _abstract(expr: dict, bindings: dict) -> Any:
    """Interpret only our finite JSON summary, never source text or Python eval."""
    kind = expr.get("kind")
    if kind == "literal":
        return expr.get("value")
    if kind == "input":
        return bindings.get(expr.get("declaration_id"), _UNKNOWN)
    if kind == "get":
        value = _abstract(expr["object"], bindings)
        if isinstance(value, dict):
            return value.get(expr["key"], _MISSING)
        return _MISSING if expr.get("optional") and (value is None or value is _MISSING) else _UNKNOWN
    if kind == "not":
        truth = _truth(_abstract(expr["operand"], bindings))
        return _UNKNOWN if truth is None else not truth
    if kind == "binary":
        first, op = _abstract(expr["left"], bindings), expr["operator"]
        if op in {"&&", "||"}:
            truth = _truth(first)
            if truth is None:
                return _UNKNOWN
            return _abstract(expr["right"], bindings) if truth == (op == "&&") else first
        second = _abstract(expr["right"], bindings)
        if first is _UNKNOWN or second is _UNKNOWN:
            return _UNKNOWN
        if op in {"===", "!=="}:
            equal = type(first) is type(second) and first == second
            return equal if op == "===" else not equal
        if op in {"==", "!="} and (first is None or second is None):
            equal = (first is None or first is _MISSING) and (second is None or second is _MISSING)
            return equal if op == "==" else not equal
        return _UNKNOWN
    if kind == "predicate_application":
        value = _abstract(expr["argument"], bindings)
        if value is _UNKNOWN:
            return _UNKNOWN
        return _apply_predicate(expr["summary"], value)
    return _UNKNOWN


def _apply_predicate(summary: dict, value: Any) -> Any:
    bindings = {summary["parameter_declaration_id"]: value}
    matches = []
    for path in summary["return_paths"]:
        matched = True
        for guard in path["conditions"]:
            truth = _truth(_abstract(guard["condition"], bindings))
            if truth is None:
                return _UNKNOWN
            if truth != guard["equals_truth"]:
                matched = False
                break
        if matched:
            matches.append(_abstract(path["value"], bindings))
    return matches[0] if len(matches) == 1 else _UNKNOWN


def _enum_partition(summary: dict) -> dict:
    """Derive finite property/literal domains from the actual predicate IR."""
    parameter = summary["parameter_declaration_id"]
    def closed(expr: dict) -> bool:
        kind = expr.get("kind")
        if kind == "literal":
            return type(expr.get("value")) is bool
        if kind == "input":
            return expr.get("declaration_id") == parameter
        if kind == "not":
            return closed(expr["operand"])
        if kind == "binary" and expr.get("operator") in {"&&", "||"}:
            return closed(expr["left"]) and closed(expr["right"])
        if kind == "binary" and expr.get("operator") in {"===", "!=="}:
            left, right = expr["left"], expr["right"]
            if right.get("kind") != "literal":
                left, right = right, left
            return (right.get("kind") == "literal" and isinstance(right.get("value"), (str, bool))
                and left.get("kind") == "get" and left.get("object", {}).get("kind") == "input"
                and left["object"].get("declaration_id") == parameter)
        return False
    if not all(closed(guard["condition"]) for path in summary["return_paths"] for guard in path["conditions"]) or not all(
            closed(path["value"]) for path in summary["return_paths"]):
        return {"complete": False, "reason": "predicate_exceeds_plain_record_boolean_strict_enum_comparison_model"}
    domains: dict[str, set] = {}
    for item in _walk_data(summary["return_paths"]):
        if not isinstance(item, dict) or item.get("kind") != "binary" or item.get("operator") not in {"===", "!=="}:
            continue
        left, right = item["left"], item["right"]
        if right.get("kind") != "literal":
            left, right = right, left
        if (left.get("kind") == "get" and left.get("object", {}).get("kind") == "input"
                and left["object"].get("declaration_id") == parameter and right.get("kind") == "literal"
                and isinstance(right.get("value"), (str, bool))):
            domains.setdefault(left["key"], set()).add(right["value"])
    dimension = {key: sorted(values, key=repr) for key, values in sorted(domains.items())}
    products = 1
    for values in dimension.values():
        products *= len(values) + 1
    if not parameter or not dimension or products > _LIMIT:
        return {"complete": False, "reason": "predicate_enum_domain_unavailable_or_exceeds_budget"}
    rows = []
    # Each property has literal cells and one equivalence class for all other
    # plain values: only ===/!== against captured literals can observe it.
    other = "<other-than-captured-literals>"
    if any(other in values for values in dimension.values()):
        return {"complete": False, "reason": "partition_other_marker_collides_with_source_literal"}
    for values in itertools.product(*[[*values, other] for values in dimension.values()]):
        record = dict(zip(dimension, values))
        result = _apply_predicate(summary, record)
        rows.append({"property_cells": record, "boolean_result": result if type(result) is bool else None,
                     "unknown": type(result) is not bool})
    absent = [{"input_cell": cell, "boolean_result": (value if type(value) is bool else None),
               "unknown": type(value) is not bool}
              for cell, raw in [("missing", _MISSING), ("null", None)]
              for value in [_apply_predicate(summary, raw)]]
    return {"complete": all(not row["unknown"] for row in [*rows, *absent]),
            "ordinary_record_partition_complete": all(not row["unknown"] for row in rows),
            "dimensions_derived_from_source_literals": dimension, "record_partitions": rows,
            "absent_input_partitions": absent, "record_cell_count": len(rows),
            "other_cell_semantics": "all other stable plain property values indistinguishable to captured strict comparisons",
            "ordinary_record_no_getters_or_proxy_required": True, "runtime_inputs_exercised": False}


def _readiness(summary: _Summary) -> dict:
    a = summary.a
    predicate = summary.predicate("readiness_predicate")
    document, _, function = a.roles["readiness_entry"]
    body = _field(function, "body")
    statements = _children(body)
    relations = []
    for guard in statements:
        if guard.type != "if_statement":
            continue
        condition = _operand(_field(guard, "condition"))
        if condition is None or condition.type != "call_expression":
            continue
        call = summary.call("readiness_entry", document, condition)
        if call.get("actual_callee_graph_node_id") != a.roles["readiness_predicate"][1].graph_node_id:
            continue
        args = _children(_field(condition, "arguments"))
        if len(args) != 1:
            continue
        identity = summary.identity(document, args[0])
        initializers = [node for statement in statements[:statements.index(guard)]
            for node in a.nodes(document, statement) if node.type == "variable_declarator"
            and summary.identity(document, _field(node, "name")) == identity]
        if len(initializers) != 1 or identity is None:
            continue
        declaration = initializers[0]
        initializer = _operand(_field(declaration, "value"))
        consequence = _field(guard, "consequence")
        abrupt = _must_abrupt(consequence)
        later_calls = [node for statement in statements[statements.index(guard) + 1:]
            for node in a.nodes(document, statement) if node.type == "call_expression"]
        predicate_return = predicate["return_paths"]
        returned = predicate_return[0]["value"] if len(predicate_return) == 1 else None
        result = summary.fact("source_predicate_abrupt_guard_dominates_later_calls", document, guard,
            role="readiness_entry", actual_predicate_call=call, predicate_summary=predicate,
            argument_binding_declaration_id=identity, argument_initializer=summary.expr("readiness_entry", document, initializer, {}),
            source_predicate_expression=returned, true_branch_always_abrupt=abrupt,
            returned_values=[a.expression(document, node) for node in a.nodes(document, consequence)
                             if node.type == "return_statement"],
            later_call_sites=[{"location": document.location(node),
                               "callee_source": document.text(_field(node, "function")),
                               "guard_true_blocks_normal_reaching": abrupt} for node in later_calls],
            conditions=["the selected entry and predicate declarations are active",
                        "the initializer and opaque calls before the return complete normally",
                        "the predicate reads the same stable ordinary result record; no getters, Proxy or external mutation"],
            source_order_not_runtime_enqueue_success=True)
        relations.append(result)
    if not relations:
        a.gap("readiness_predicate_abrupt_dominance_not_found")
    partition = _enum_partition(predicate)
    if not partition.get("ordinary_record_partition_complete"):
        a.gap("readiness_predicate_ordinary_record_partition_unknown")
    return {"relations": relations, "predicate_finite_partition": partition, "scoped_source_supported": bool(relations)
            and partition.get("ordinary_record_partition_complete", False)
            and all(item["true_branch_always_abrupt"] and item["later_call_sites"] for item in relations),
            "readiness_implementation_success_or_external_state_proven": False}


def _completion(summary: _Summary) -> dict:
    a = summary.a
    mutation = summary.predicate("mutating_predicate")
    partition = _enum_partition(mutation)
    paths = summary.paths("completion_evaluator")
    constructor_doc, _, constructor_fn = a.roles["gate_result"]
    constructor_returns = [node for node in a.nodes(constructor_doc, _field(constructor_fn, "body"))
                           if node.type == "return_statement"]
    constructor = [summary.expr("gate_result", constructor_doc, next(iter(_children(node)), None), {})
                   for node in constructor_returns]
    parameters = [_field(node, "pattern") or _field(node, "name") or node
                  for node in _children(_field(constructor_fn, "parameters"))]
    parameter_ids = [summary.identity(constructor_doc, node) for node in parameters]
    returned_paths = []
    for path in paths:
        value = path["value"]
        valid = value.get("kind") == "opaque_call" and value.get("actual_target_role") == "gate_result"
        arguments = value.get("arguments", []) if valid else []
        construction = None
        if valid and len(constructor_returns) == 1 and len(arguments) == len(parameter_ids) and all(parameter_ids):
            constructor_env = dict(zip(parameter_ids, arguments))
            construction = summary.expr("gate_result", constructor_doc,
                next(iter(_children(constructor_returns[0])), None), constructor_env)
        returned_paths.append({**path, "authenticated_result_constructor": valid,
            "constructor_arguments": arguments, "returned_plain_record": construction,
            "predicate_roles_used": sorted({item["predicate_role"] for item in _walk_data(path["conditions"])
                                            if isinstance(item, dict) and item.get("kind") == "predicate_application"})})
    document, _, function = a.roles["completion_evaluator"]
    predicates = [node for node in a.nodes(document, _field(function, "body")) if node.type == "if_statement"]
    consumer_relations = []
    for node in predicates:
        location = document.location(_field(node, "condition"))
        computed = [fact["expression"] for fact in a.source_facts
                    if fact.get("kind") == "conditional_gate_predicate" and fact.get("role") == "completion_evaluator"
                    and fact["location"]["start_byte"] == location["start_byte"]]
        variants = {json.dumps(value, sort_keys=True): value for value in computed}
        condition = next(iter(variants.values())) if len(variants) == 1 else None
        returns = [item for item in returned_paths if _inside(node, next((candidate for candidate in a.nodes(document, node)
                   if candidate.type == "return_statement" and candidate.start_byte == item["location"]["start_byte"]), None))]
        consumer_relations.append(summary.fact("completion_gate_condition_consumes_result", document, node,
            condition_source=a.expression(document, _field(node, "condition")),
            condition_abstract_form=condition, condition_variants=list(variants.values()),
            local_predicate_roles=sorted({item["predicate_role"] for value in variants.values() for item in _walk_data(value)
                if isinstance(item, dict) and item.get("kind") == "predicate_application"}),
            opaque_result_fields=[{"field": item["key"], "producer": item["object"]}
                for value in variants.values() for item in _walk_data(value) if isinstance(item, dict)
                and item.get("kind") == "get" and item.get("object", {}).get("kind") == "opaque_call"],
            affected_return_fact_ids=[item["fact_id"] for item in returns],
            normal_source_order_index=len(consumer_relations), branch_runtime_selected=False))
    supported = (bool(paths) and partition.get("complete") and mutation["all_return_values_boolean_literals"]
                 and all(path["authenticated_result_constructor"] and path["returned_plain_record"] is not None
                         for path in returned_paths)
                 and len(constructor) == 1 and constructor[0].get("kind") == "record")
    if not supported:
        a.gap("completion_gate_finite_conditions_incomplete", finite_mutating_partition_complete=partition.get("complete"),
              result_constructor_return_count=len(constructor))
    return {"mutating_predicate": mutation, "mutating_finite_enum_partition": partition,
            "gate_return_paths": returned_paths, "condition_consumers": consumer_relations,
            "result_constructor_source": constructor, "scoped_source_supported": bool(supported),
            "checklist_internal_checks_proven": False, "external_verdict_or_evidence_truth_proven": False,
            "conditions_directly_depending_on_mutating_predicate": [item["id"] for item in consumer_relations
                if "mutating_predicate" in item["local_predicate_roles"]],
            "conditions_without_direct_mutating_dependency": [item["id"] for item in consumer_relations
                if not item["local_predicate_roles"]],
            "statement": "Return records, local condition dependencies and source order are computed separately. Path conditions retain prior short circuits; local conditions describe the current gate only. No target inputs were executed."}


def _member_parts(document: Any, node: Any) -> tuple[Any, str | None]:
    node = _operand(node)
    if node is None or node.type not in {"member_expression", "subscript_expression"}:
        return None, None
    return _field(node, "object"), _key(document, _field(node, "property") or _field(node, "index"))


def _access_audit(summary: _Summary) -> dict:
    a = summary.a
    document, _, function = a.roles["access_server"]
    open_target = a.roles["audit_opener"][1].graph_node_id
    writer_target = a.roles["response_writer"][1].graph_node_id
    opener_calls = [call for call in a.calls_by_role.get("access_server", [])
                    if call.get("actual_callee_graph_node_id") == open_target]
    relations = []
    for opener in opener_calls:
        opener_node = a.call_nodes[opener["id"]][2]
        parent = opener_node.parent
        while parent is not None and parent.type not in {"variable_declarator", *_FUNCTIONS}:
            parent = parent.parent
        audit_identity = summary.identity(document, _field(parent, "name")) if parent is not None and parent.type == "variable_declarator" else None
        if not audit_identity:
            continue
        for attempt in a.nodes(document, _field(function, "body"), nested=True):
            if attempt.type != "try_statement" or _field(attempt, "handler") is None:
                continue
            block = _field(attempt, "body")
            statements = _children(block)
            if len(statements) != 1 or statements[0].type != "expression_statement":
                continue
            expression = next(iter(_children(statements[0])), None)
            call_node = _operand(expression)
            if expression is None or expression.type != "await_expression" or call_node is None or call_node.type != "call_expression":
                continue
            receiver, member = _member_parts(document, _field(call_node, "function"))
            if summary.identity(document, receiver) != audit_identity:
                continue
            # Model any actual awaited method on this authenticated opener's
            # result; its name and response fields are source results.
            outer = attempt.parent
            if outer is None or outer.type != "statement_block":
                continue
            following = _children(outer)[_children(outer).index(attempt) + 1:]
            send_calls = [node for statement in following for node in a.nodes(document, statement)
                          if node.type == "call_expression" and summary.call("access_server", document, node).get("actual_callee_graph_node_id") == writer_target]
            handler = _field(attempt, "handler")
            assignments = [node for node in a.nodes(document, _field(handler, "body"))
                           if node.type == "assignment_expression" and _field(node, "right") is not None
                           and _field(node, "right").type == "object" and node.parent is not None
                           and node.parent.type == "expression_statement" and node.parent.parent == _field(handler, "body")]
            for assignment in assignments:
                identity = summary.identity(document, _field(assignment, "left"))
                if not identity:
                    continue
                fields = summary.expr("access_server", document, _field(assignment, "right"), {})
                for send in send_calls:
                    args = _children(_field(send, "arguments"))
                    references = [node for argument in args for node in a.nodes(document, argument)
                                  if node.type == "identifier" and summary.identity(document, node) == identity]
                    if not references:
                        continue
                    callback = attempt.parent
                    while callback is not None and callback.type not in _FUNCTIONS:
                        callback = callback.parent
                    if callback is None:
                        continue
                    registration = callback.parent
                    while registration is not None and registration.type not in {"call_expression", *_FUNCTIONS}:
                        registration = registration.parent
                    relation = summary.fact("awaited_access_audit_response_replacement", document, attempt,
                        opener_call_fact_id=opener["id"], opener_result_declaration_id=audit_identity,
                        actual_awaited_method=member, awaited_call_location=document.location(call_node),
                        audit_arguments=[a.expression(document, arg) for arg in _children(_field(call_node, "arguments"))],
                        response_binding_declaration_id=identity, failure_response=fields,
                        catch_assignment_location=document.location(assignment),
                        actual_response_writer_call=summary.call("access_server", document, send),
                        response_field_arguments=[a.expression(document, arg) for arg in args],
                        callback_location=document.location(callback),
                        registration_location=document.location(registration) if registration is not None and registration.type == "call_expression" else None,
                        catch_return_or_throw_before_response=any(node.type in {"return_statement", "throw_statement"}
                            for node in a.nodes(document, _field(handler, "body"))),
                        conditions=["the captured registered request callback is invoked and reaches the awaited audit call",
                            "the selected opener, callback and response writer declarations are active",
                            "the audit await rejects or throws and catch logging completes normally",
                            "normal plain response object properties; no getters, Proxy or external mutation",
                            "intervening header operations and the response writer complete normally"],
                        callback_activation_proven=False, audit_write_durability_proven=False,
                        business_mutation_rollback_proven=False, actual_http_response_delivery_proven=False)
                    relations.append(relation)
    writer_document, _, writer_function = a.roles["response_writer"]
    parameter_ids = [summary.identity(writer_document, _field(node, "pattern") or _field(node, "name") or node)
                     for node in _children(_field(writer_function, "parameters"))]
    forwards = []
    for node in a.nodes(writer_document, _field(writer_function, "body")):
        if node.type != "call_expression":
            continue
        receiver, member = _member_parts(writer_document, _field(node, "function"))
        receiver_id = summary.identity(writer_document, receiver)
        if receiver_id is None or receiver_id not in parameter_ids:
            continue
        for index, argument in enumerate(_children(_field(node, "arguments"))):
            parameter = summary.identity(writer_document, argument)
            if parameter is not None and parameter in parameter_ids:
                forwards.append(summary.fact("response_writer_parameter_forwarding", writer_document, node,
                    receiver_parameter_index=parameter_ids.index(receiver_id), source_member=member,
                    source_argument_index=index, value_parameter_index=parameter_ids.index(parameter),
                    value_parameter_declaration_id=parameter,
                    standard_http_method_effect_assumed=False, actual_response_delivery_proven=False))
    writer_calls = [a.expression(writer_document, node) for node in a.nodes(writer_document, _field(writer_function, "body"))
                    if node.type == "call_expression"]
    if not relations:
        a.gap("awaited_access_audit_response_replacement_not_found")
    if not forwards:
        a.gap("access_response_writer_parameter_forwarding_unknown")
    value_relations = []
    forwarded_relation_ids = set()
    for relation in relations:
        send = a.call_nodes[relation["actual_response_writer_call"]["id"]][2]
        arguments = _children(_field(send, "arguments"))
        mappings = []
        for forwarding in forwards:
            index = forwarding["value_parameter_index"]
            if index >= len(arguments):
                continue
            root, field = _member_parts(document, arguments[index])
            if (summary.identity(document, root) != relation["response_binding_declaration_id"]
                    or field not in relation["failure_response"].get("fields", {})):
                continue
            mappings.append({"failure_response_field": field,
                "failure_field_abstract_value": relation["failure_response"]["fields"][field],
                "selected_writer_argument_index": index,
                "writer_parameter_declaration_id": forwarding["value_parameter_declaration_id"],
                "actual_destination_member": forwarding["source_member"],
                "destination_argument_index": forwarding["source_argument_index"],
                "source_forwarding_fact_id": forwarding["id"],
                "source_value_relation_proven_under_record_model": True,
                "external_method_effect_or_http_delivery_proven": False})
        if mappings:
            forwarded_relation_ids.add(relation["id"])
            value_relations.append(summary.fact("access_failure_response_field_forwarding", document, send,
                response_replacement_fact_id=relation["id"], field_mappings=mappings,
                actual_response_delivery_proven=False))
        if not mappings:
            a.gap("access_failure_response_field_to_writer_parameter_unknown")
    return {"response_replacement_relations": relations, "response_writer_source_calls": writer_calls,
            "response_writer_parameter_forwarding": forwards,
            "response_value_relations": value_relations,
            "scoped_source_supported": bool(relations) and bool(forwards)
                and all(relation["id"] in forwarded_relation_ids and not relation["catch_return_or_throw_before_response"]
                        for relation in relations),
            "job_audit_subject_equivalence_claimed": False, "all_http_security_or_business_mutations_proven": False}


def analyze_pattern(analysis: Any) -> dict:
    """Adapter for report_chain_analysis._Analysis after authenticated load()."""
    summary = _Summary(analysis)
    groups = {}
    for group, roles in GROUPS.items():
        present = roles.intersection(analysis.roles)
        if not present:
            continue
        if present != roles:
            analysis.gap("conditional_gate_source_roles_missing", group=group, missing=sorted(roles - present))
            continue
        gap_start = len(analysis.gaps)
        groups[group] = {"readiness": _readiness, "completion": _completion,
                         "access_audit": _access_audit}[group](summary)
        groups[group]["necessary_gaps"] = analysis.gaps[gap_start:]
        groups[group]["scoped_source_supported"] = bool(groups[group].get("scoped_source_supported")) and not groups[group]["necessary_gaps"]
    if not groups:
        analysis.gap("conditional_gate_no_supported_source_group")
    if summary.truncated:
        analysis.gap("conditional_gate_summary_budget_exceeded")
    return {"version": VERSION, "model": MODEL, "groups": groups,
            "scoped_source_supported": bool(groups) and all(group.get("scoped_source_supported") for group in groups.values())
                and not summary.truncated and not analysis.incomplete,
            "source_return_conditions_computed": True, "target_code_executed": False,
            "runtime_verified": False, "all_project_functionality_proven": False,
            "trusted_model": {"origin": "trusted-model", "id": MODEL,
                "ordinary_boolean_and_strict_literal_equality": True,
                "finite_enum_cells_derived_from_source_literals": True,
                "captured_lexical_binding_identity_is_not_heap_identity": True,
                "opaque_calls_must_complete_normally_for_following_source_to_be_reached": True,
                "getters_proxy_external_mutation_and_concurrency_excluded": True},
            "budgets": {"summary_path_limit": _LIMIT, "truncated": summary.truncated}}
