"""Finite completion relations over authenticated, saved JS/TS syntax.

An ordinary call, an awaited fulfillment, a returned Promise and an iterator
are different facts.  These summaries do not execute a body, prove invocation
activation, solve arbitrary control flow, or establish resource lifetime.
``normal_value_relation_closed`` is conditional on the selected invocation
fulfilling normally and the selected return being reached.  Catch/early-exit
paths remain explicit; a finally or unsupported default RHS rejects closure.
"""

from __future__ import annotations

from typing import Any

VERSION = "captured-completion-summaries-1"
_FUNCTIONS = frozenset({"function_declaration", "generator_function_declaration",
    "function_expression", "generator_function", "arrow_function", "method_definition"})
_WRAPPERS = frozenset({"parenthesized_expression", "as_expression", "satisfies_expression",
    "non_null_expression", "type_assertion", "instantiation_expression"})
_COMMENTS = frozenset({"comment", "line_comment", "block_comment"})
_SAMPLE = 16
_NODE_LIMIT = 16384
_CONSUMPTIONS = frozenset({"return_or_await", "await", "return", "return_result"})


def _children(node: Any) -> list[Any]:
    return [child for child in node.named_children if child.type not in _COMMENTS] if node is not None else []


def _walk(node: Any):
    """Walk the selected body, without borrowing a nested callable's result."""
    pending = [node] if node is not None else []
    count = 0
    while pending:
        current = pending.pop()
        count += 1
        if count > _NODE_LIMIT:
            raise ValueError("completion_ast_budget_exceeded")
        yield current
        if current.type in _FUNCTIONS:
            continue
        pending.extend(reversed(current.named_children))


def _unwrap(node: Any, *, include_await: bool = False) -> Any:
    while node is not None and (node.type in _WRAPPERS or include_await and node.type == "await_expression"):
        expression = node.child_by_field_name("expression") or node.child_by_field_name("argument")
        if expression is None:
            children = [child for child in _children(node) if child.type not in {"type_arguments", "type_identifier", "type_annotation"}]
            expression = children[0] if len(children) == 1 else None
        if expression is None or expression == node:
            break
        node = expression
    return node


def _contains(document: Any, node: Any) -> bool:
    return bool(document is not None and node is not None and callable(getattr(document, "contains", None))
        and document.contains(node))


def _location(document: Any, node: Any) -> dict | None:
    if not _contains(document, node):
        return None
    location = document.location(node)
    return {key: location[key] for key in ("file", "line", "column", "end_line", "end_column",
        "start_byte", "end_byte", "original_file_start_byte", "original_file_end_byte", "source_hash",
        "span_hash", "semantic_parse_id", "coordinate_space", "column_unit", "column_base", "raw_prefix_bytes")
        if key in location}


def _identity(record: dict) -> dict:
    result = {key: record.get(key) for key in ("state", "identity_complete", "declaration_id", "binding_id",
        "declaration_kind", "name", "file", "source_hash", "parameter_index", "declaration_span", "binder_span")
        if key in record}
    result["runtime_value_known"] = False
    return result


def _unknown(reason: str, **details: Any) -> dict:
    return {"version": VERSION, "state": "unknown", "reason": reason,
        "normal_value_relation_closed": False, "completion_guaranteed": False,
        "body_activation_proved": False, "runtime_verified": False,
        "exception_paths_unknown": True, **details}


def function_kind(document: Any, function: Any) -> dict:
    """Classify this exact caller/callee AST, independently of its activation."""
    result = {"version": VERSION, "kind": "unknown", "ordinary": False, "async": False,
        "generator": False, "invocation_result": "unknown", "body_throw_effect": "unknown",
        "body_activation_proved": False, "runtime_verified": False,
        "location": _location(document, function), "reason": None, "thenable_identity_not_inferred": True}
    if not _contains(document, function) or function.type not in _FUNCTIONS:
        result["reason"] = "function_ast_not_in_authenticated_document"
        return result
    if any(child.type in {"get", "set"} for child in function.children):
        result["reason"] = "accessor_is_not_an_ordinary_invoked_method"
        return result
    body = function.child_by_field_name("body")
    if body is None:
        result["reason"] = "callable_body_unavailable"
        return result
    try:
        own_yield = any(node.type in {"yield_expression", "yield_statement"} for node in _walk(body))
    except ValueError as error:
        result["reason"] = str(error)
        return result
    asynchronous = any(child.type == "async" for child in function.children)
    generator = (function.type in {"generator_function", "generator_function_declaration"}
        or any(child.type == "*" for child in function.children) or own_yield)
    kind = ("async_generator" if asynchronous else "generator") if generator else ("ordinary_async" if asynchronous else "ordinary_sync")
    result.update(kind=kind, ordinary=not generator, **{"async": asynchronous}, generator=generator,
        invocation_result="async_iterator" if generator and asynchronous else "iterator" if generator else "promise" if asynchronous else "arbitrary_value_or_throw",
        body_throw_effect="async_iteration_rejection" if generator and asynchronous else "deferred_iteration_throw" if generator else "promise_rejection" if asynchronous else "synchronous_throw",
        own_yield_present=own_yield, reason="iterator_activation_not_modeled" if generator else None)
    return result


def _pure_default(node: Any) -> bool:
    node = _unwrap(node)
    if node is None:
        return False
    if node.type in {"null", "true", "false", "number", "string"}:
        return True
    if node.type == "array":
        return all(_pure_default(child) for child in _children(node)) and not any(child.type == "," for child in node.children)
    if node.type == "object":
        for pair in _children(node):
            key, value = pair.child_by_field_name("key"), pair.child_by_field_name("value")
            if pair.type != "pair" or key is None or key.type not in {"property_identifier", "string", "number"} or not _pure_default(value):
                return False
        return True
    return False


def _default_origin(document: Any, node: Any, reader: Any, depth: int = 0, seen: frozenset = frozenset()) -> bool:
    if _pure_default(node):
        return True
    node = _unwrap(node)
    if node is None or node.type != "identifier" or depth >= 4:
        return False
    identity = reader.resolve(node)
    declaration = reader.declaration_for(identity)
    key = identity.get("declaration_id")
    if (identity.get("state") != "unique" or not identity.get("identity_complete") or key in seen
            or identity.get("declaration_kind") != "const" or declaration is None or declaration.type != "variable_declarator"
            or any(record.get("binding_reassignment") or record.get("possible_effect") for record in reader.writes(identity))):
        return False
    initializer = declaration.child_by_field_name("value")
    if _unwrap(initializer) is not None and _unwrap(initializer).type in {"object", "array"}:
        return False  # Stored aggregate getters/member mutation are not literal RHS purity.
    # Bare reads of a stable captured const literal introduce no assignment to
    # another formal. Initialization/TDZ exceptions are still not proved away.
    return _default_origin(document, initializer, reader, depth + 1, seen | {key})


def _defaults(document: Any, function: Any, reader: Any) -> dict:
    params = function.child_by_field_name("parameters") or function.child_by_field_name("parameter")
    sources = []
    try:
        nodes = list(_walk(params))
    except ValueError as error:
        return {"state": "unknown", "reason": str(error), "count": 0, "samples": []}
    for node in nodes:
        value = node.child_by_field_name("value") if node.type in {"required_parameter", "optional_parameter"} else node.child_by_field_name("right") if node.type in {"assignment_pattern", "object_assignment_pattern"} else None
        if value is not None:
            sources.append({"location": _location(document, value), "source_literal_rhs_only": _default_origin(document, value, reader)})
    return {"state": "source_literal_rhs_only" if all(source["source_literal_rhs_only"] for source in sources) else "unknown",
        "count": len(sources), "samples": sources[:_SAMPLE], "truncated": len(sources) > _SAMPLE,
        "parameter_initialization_runtime_verified": False,
        "destructuring_getters_and_runtime_exceptions_verified": False}


def _ancestors(node: Any):
    while node is not None:
        yield node
        node = node.parent


def _owner(call: Any) -> Any:
    return next((node for node in _ancestors(call.parent) if node.type in _FUNCTIONS), None)


def _transparent_parent(node: Any) -> Any:
    current = node
    while current.parent is not None and current.parent.type in _WRAPPERS and _unwrap(current.parent) == _unwrap(current):
        current = current.parent
    return current


def _consumption(call: Any, function: Any) -> dict:
    transparent = _transparent_parent(call)
    parent = transparent.parent
    directly_awaited = bool(parent is not None and parent.type == "await_expression"
        and _unwrap(parent, include_await=True) == call)
    expression = _transparent_parent(parent) if directly_awaited else transparent
    returned = bool(expression.parent is not None and expression.parent.type == "return_statement"
        and len(_children(expression.parent)) == 1 and _children(expression.parent)[0] == expression)
    body = function.child_by_field_name("body")
    arrow_return = bool(function.type == "arrow_function" and body is not None and body.type != "statement_block"
        and _unwrap(body, include_await=True) == call)
    returned = returned or arrow_return
    kind = "direct_return_after_await" if returned and directly_awaited else "direct_await" if directly_awaited else "direct_return_invocation_result" if returned else "not_directly_consumed"
    return {"kind": kind, "direct_await": directly_awaited, "returned_directly": returned,
        "returned_without_await": returned and not directly_awaited,
        "returned_promise_fulfillment_verified": False,
        "resource_held_until_promise_settlement_verified": False}


def _conditions(document: Any, node: Any, function: Any) -> list[dict]:
    result = []
    child = node
    for parent in _ancestors(node.parent):
        if parent == function:
            break
        if parent.type in _FUNCTIONS:
            result.append({"kind": "nested_callable", "location": _location(document, parent)})
            break
        if parent.type == "if_statement":
            branch = "consequence" if parent.child_by_field_name("consequence") == child else "alternative" if parent.child_by_field_name("alternative") == child else "condition"
            result.append({"kind": "if", "branch": branch, "condition": _location(document, parent.child_by_field_name("condition"))})
        elif parent.type in {"for_statement", "for_in_statement", "while_statement", "do_statement", "switch_case", "switch_default", "ternary_expression"}:
            result.append({"kind": parent.type, "location": _location(document, parent), "execution_condition_evaluated": False})
        elif parent.type == "try_statement":
            branch = "body" if parent.child_by_field_name("body") == child else "handler" if parent.child_by_field_name("handler") == child else "finalizer" if parent.child_by_field_name("finalizer") == child else "unknown"
            result.append({"kind": "try", "branch": branch, "location": _location(document, parent),
                "handler_present": parent.child_by_field_name("handler") is not None,
                "finalizer_present": parent.child_by_field_name("finalizer") is not None})
        child = parent
    return result


def _lexical(document: Any, lexical: Any) -> Any:
    if lexical is not None:
        if getattr(lexical, "document", None) is not document:
            raise ValueError("lexical_reader_document_mismatch")
        return lexical
    reader = getattr(document, "_completion_lexical_reader", None)
    if reader is None:
        from .lexical_bindings import LexicalBindings
        reader = LexicalBindings(document)
        document._completion_lexical_reader = reader
    return reader


def _callee_identity(document: Any, call: Any, reader: Any) -> dict:
    callee = _unwrap(call.child_by_field_name("function"))
    if callee is None or callee.type != "identifier":
        return {"state": "unknown", "reason": "callee_value_not_a_bare_lexical_identifier",
            "exact_callable_value_identity": False, "runtime_binding_verified": False}
    identity = reader.resolve(callee)
    writes = reader.writes(identity) if identity.get("state") == "unique" and identity.get("identity_complete") else []
    effects = [record for record in writes if record.get("binding_reassignment") or record.get("possible_effect")
        and (not record.get("member_write") or not record.get("mutation_target_complete"))]
    return {"state": identity.get("state", "unknown"), "identity": _identity(identity),
        "exact_callable_value_identity": identity.get("state") == "unique" and identity.get("identity_complete", False),
        "captured_binding_writes_closed": not effects and identity.get("state") == "unique",
        "captured_binding_effect_count": len(effects), "runtime_binding_verified": False}


def _result_origin(document: Any, call: Any, function: Any, reader: Any, nodes: list[Any]) -> dict:
    """Close one source result origin, without claiming that it dominates return."""
    body = function.child_by_field_name("body")
    if function.type == "arrow_function" and body is not None and body.type != "statement_block":
        if _unwrap(body, include_await=True) == call:
            return {"state": "source_normal_value_origin", "kind": "implicit_arrow_return",
                "return_location": _location(document, body), "return_conditions": [],
                "return_reached_verified": False, "alternative_null_false_return_count": 0}
        return {"state": "unknown", "reason": "implicit_arrow_return_not_the_selected_call"}
    returns = [node for node in nodes if node.type == "return_statement"]
    nonempty = [node for node in returns if len(_children(node)) != 1 or _children(node)[0].type not in {"null", "false"}]
    if len(nonempty) != 1:
        return {"state": "unknown", "reason": "nonempty_return_not_unique", "return_count": len(returns)}
    returned = nonempty[0]
    values = _children(returned)
    value = _unwrap(values[0], include_await=True) if len(values) == 1 else None
    common = {"return_location": _location(document, returned), "return_conditions": _conditions(document, returned, function),
        "alternative_null_false_return_count": len(returns) - len(nonempty), "return_reached_verified": False}
    if value == call:
        return {"state": "source_normal_value_origin", "kind": "direct_return", **common}
    if value is None or value.type != "identifier":
        return {"state": "unknown", "reason": "returned_value_is_not_direct_or_bare_local", **common}
    identity = reader.resolve(value)
    declaration = reader.declaration_for(identity)
    if (identity.get("state") != "unique" or not identity.get("identity_complete") or declaration is None
            or declaration.type != "variable_declarator" or declaration.child_by_field_name("value") is not None
            or declaration.parent is None or declaration.parent.parent != body
            or identity.get("declaration_kind") not in {"let", "var"}):
        return {"state": "unknown", "reason": "result_not_an_uninitialized_outer_local", **common}
    writes = reader.writes(identity)
    effects = [record for record in writes if record.get("possible_effect") and (
        not record.get("member_write") or not record.get("mutation_target_complete"))]
    assignments = [record for record in writes if record.get("identity_match_known") and record.get("binding_reassignment")]
    assignment = reader.mutation_for(assignments[0]) if len(assignments) == 1 and not effects else None
    left = _unwrap(assignment.child_by_field_name("left")) if assignment is not None else None
    right = _unwrap(assignment.child_by_field_name("right")) if assignment is not None else None
    matches = bool(assignment is not None and assignment.type == "assignment_expression"
        and left is not None and left.type == "identifier" and reader.same(left, value)
        and right is not None and right.type == "await_expression" and _unwrap(right, include_await=True) == call
        and declaration.end_byte < assignment.start_byte < returned.start_byte
        and _owner(call) == function and _owner(assignment) == function)
    return {"state": "source_normal_value_origin" if matches else "unknown",
        "kind": "single_await_assignment_then_return" if matches else "unknown",
        "reason": None if matches else "await_assignment_origin_not_closed",
        "binding_identity": _identity(identity), "declaration": _location(document, declaration),
        "assignment": _location(document, assignment), "write_count": len(assignments), "effect_count": len(effects),
        "assignment_conditions": _conditions(document, assignment, function) if assignment is not None else [],
        "assignment_dominates_return_proved": False, **common}


def completion_relation(document: Any, call: Any, function: Any,
                        consumption: str = "return_or_await", *, lexical: Any = None) -> dict:
    """Describe how a containing caller consumes this exact call expression.

    ``function`` is the caller AST in ``document``, never a callee from another
    source file.  Consumers separately authenticate the callee/argument mapping.
    A direct return forwards the invocation result; it does not prove Promise
    fulfillment.  ``return_result`` also recognizes a unique lexical await
    assignment/return origin under its recorded normal-prefix conditions.
    """
    if consumption not in _CONSUMPTIONS:
        raise ValueError("unsupported completion consumption")
    kind = function_kind(document, function)
    base = {"consumption": consumption, "function_kind": kind, "call_location": _location(document, call),
        "direct_await": False, "returned_directly": False, "returned_without_await": False,
        "whole_function_completion_proved": False, "resource_lifetime_proved": False,
        "invocation_binding_proved": False, "exception_paths_unknown": True,
        "normal_relation_scope": "selected captured invocation fulfills normally; selected return, if any, is reached",
        "normal_relation_preconditions": ["the selected invocation actually executes and fulfills normally",
            "the selected consuming expression or return is reached", "standard JS/TS execution semantics"],
        "dominance_proved": False, "control_gaps": []}
    if not kind["ordinary"]:
        return _unknown("ordinary_caller_required", **base)
    if not _contains(document, call) or call.type != "call_expression" or _owner(call) != function:
        return _unknown("call_not_owned_by_selected_caller", **base)
    body = function.child_by_field_name("body")
    if not (body.start_byte <= call.start_byte < body.end_byte):
        return _unknown("call_in_parameter_default_or_outside_body", **base)
    try:
        nodes = list(_walk(body))
        reader = _lexical(document, lexical)
    except ValueError as error:
        return _unknown(str(error), **base)
    syntax = _consumption(call, function)
    defaults = _defaults(document, function, reader)
    conditions = _conditions(document, call, function)
    finalizers = [node for node in nodes if node.type == "try_statement" and node.child_by_field_name("finalizer") is not None]
    abrupt = [node for node in nodes if node.type in {"return_statement", "throw_statement", "break_statement", "continue_statement"}
        and node.end_byte <= call.start_byte]
    gaps = []
    if finalizers:
        gaps.append("finally_return_or_value_effects_not_modeled")
    if defaults["state"] == "unknown":
        gaps.append("default_rhs_effects_not_modeled")
    if any(condition["kind"] in {"for_statement", "for_in_statement", "while_statement", "do_statement", "switch_case", "switch_default", "ternary_expression"} for condition in conditions):
        gaps.append("loop_switch_or_conditional_invocation_control_not_modeled")
    base.update(syntax, default_rhs=defaults, conditions=conditions, callee_identity=_callee_identity(document, call, reader),
        control_gaps=gaps, preceding_abrupt_count=len(abrupt),
        preceding_abrupt_samples=[{"location": _location(document, node), "conditions": _conditions(document, node, function)} for node in abrupt[:_SAMPLE]],
        preceding_abrupt_truncated=len(abrupt) > _SAMPLE,
        exception_region_count=sum(node.type in {"catch_clause", "finally_clause"} for node in nodes),
        finalizer_count=len(finalizers))
    origin = None
    if consumption == "return_result":
        origin = _result_origin(document, call, function, reader, nodes)
        base["result_origin"] = origin
    syntax_matches = (syntax["direct_await"] if consumption == "await" else syntax["returned_directly"] if consumption == "return"
        else origin is not None and origin["state"] == "source_normal_value_origin" if consumption == "return_result"
        else syntax["direct_await"] or syntax["returned_directly"])
    if not syntax_matches or gaps:
        return _unknown("finite_consumption_relation_not_closed" if gaps else "requested_consumption_not_found", **base)
    return {"version": VERSION, "state": "source_normal_completion_relation", "reason": None,
        "normal_value_relation_closed": True, "completion_guaranteed": False, "body_activation_proved": False,
        "runtime_verified": False, **base}
