"""Locator-only, finite local budget source forms over immutable snapshots.

Only ordinary ``for`` headers and comparison/abrupt-branch guards are selected.
Names locate candidate declarations; captured lexical identities establish the
actual operands and writes. No target file is opened, expression evaluated,
budget amount configured, CALLS manufactured, or runtime termination proved.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import math
import re
from typing import Any

from .completion_summaries import VERSION as COMPLETION_VERSION, completion_relation, function_kind
from .lexical_bindings import LexicalBindings, VERSION as LEXICAL_VERSION
from .models import Evidence, Finding, GraphSnapshot
from .semantic_sources import SemanticSources, VERSION as SOURCE_VERSION, unwrap

VERSION = "static-local-budget-contracts-1"
POLICY_VERSION = "static-local-budget-policy-v1"
MODEL_ID = "captured-local-budget-source-v1"
_FUNCTIONS = {"function_declaration", "generator_function_declaration", "function_expression",
    "generator_function", "arrow_function", "method_definition"}
_COMMENTS = {"comment", "line_comment", "block_comment"}
_COMPARISONS = {"<", "<=", ">", ">="}
_NODE_LIMIT = 16384
_SITE_LIMIT = 128
_ORIGIN_DEPTH = 4
_SAMPLE = 16


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True,
        separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()


def _data(value: Any, depth: int = 0, budget: list[int] | None = None) -> None:
    budget = [8192] if budget is None else budget
    budget[0] -= 1
    if budget[0] < 0 or depth > 32:
        raise ValueError("预算合同超出有限 JSON 大小。")
    if value is None or type(value) in {bool, int}:
        return
    if type(value) is float and math.isfinite(value):
        return
    if type(value) is str and len(value) <= 16384 and "\x00" not in value:
        return
    if type(value) is list:
        for item in value:
            _data(item, depth + 1, budget)
        return
    if type(value) is dict and all(type(key) is str for key in value):
        for key, item in value.items():
            _data(key, depth + 1, budget)
            _data(item, depth + 1, budget)
        return
    raise ValueError("预算合同必须为有限 data-only JSON。")


def _string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and len(value) <= 4096 and "\x00" not in value


def _path(value: Any) -> bool:
    return (_string(value) and not value.startswith("/") and "\\" not in value
        and not re.match(r"^[A-Za-z]:", value)
        and all(part not in {"", ".", ".."} for part in value.split("/")))


def _name(value: Any) -> bool:
    return _string(value) and len(value) <= 256 and "\\" not in value and value.replace("$", "_").isidentifier()


def validate_budget_rule(rule: Any) -> None:
    """Allow role locators and conditions, never comparisons or budget values."""
    _data(rule)
    required = {"id", "type", "severity", "subject", "counter", "limit", "evaluation", "models", "provenance", "applicability"}
    if not isinstance(rule, dict) or set(rule) != required:
        raise ValueError("budget_contracts 仅接受固定主体、局部 counter/limit 定位器与条件。")
    if (not _string(rule["id"]) or not isinstance(rule["type"], str)
            or rule["type"] not in {"bounded_for_loop", "counter_exhaustion_guard"}
            or not isinstance(rule["severity"], str) or rule["severity"] not in {"high", "medium", "low", "info"}):
        raise ValueError("预算 id/type/severity 无效。")
    subject = rule["subject"]
    if not isinstance(subject, dict) or set(subject) != {"file", "symbol"} or not _path(subject["file"]) or not _string(subject["symbol"]):
        raise ValueError("subject 需要项目内 file 和精确 symbol。")
    for role in ("counter", "limit"):
        locator = rule[role]
        if not isinstance(locator, dict) or set(locator) != {"kind", "name"} or locator["kind"] != "local_binding" or not _name(locator["name"]):
            raise ValueError("counter/limit 仅接受 local_binding/name；不能填数值或来源。")
    if rule["counter"]["name"] == rule["limit"]["name"]:
        raise ValueError("counter 与 limit 定位器不能同名。")
    if rule["evaluation"] != "all_lexical_sites" or rule["models"] != [MODEL_ID]:
        raise ValueError("仅支持 all_lexical_sites 和固定局部预算源码模型。")
    provenance = rule["provenance"]
    if not isinstance(provenance, dict) or set(provenance) - {"authority", "reviewer", "author_approved", "source_doc", "note"} or not _string(provenance.get("authority")) or not _string(provenance.get("source_doc")) or type(provenance.get("author_approved")) is not bool:
        raise ValueError("provenance 是来源标签，不读取 source_doc 或作为预填证明。")
    applicability = rule["applicability"]
    if not isinstance(applicability, dict) or set(applicability) - {"kind", "conditions", "counterexamples"} or applicability.get("kind") != "conditional" or not isinstance(applicability.get("conditions"), list) or not applicability["conditions"] or not all(_string(item) for item in applicability["conditions"]):
        raise ValueError("预算合同必须保留明确 conditional 适用条件。")
    if not isinstance(applicability.get("counterexamples", []), list) or not all(_string(item) for item in applicability.get("counterexamples", [])):
        raise ValueError("counterexamples 只能为说明文字。")


def _children(node: Any) -> list[Any]:
    return [child for child in node.named_children if child.type not in _COMMENTS] if node is not None else []


def _walk(node: Any, *, nested: bool = True) -> list[Any]:
    values, pending = [], [node] if node is not None else []
    while pending:
        current = pending.pop()
        if len(values) >= _NODE_LIMIT:
            raise ValueError("budget_ast_budget_exceeded")
        values.append(current)
        if not nested and current != node and current.type in _FUNCTIONS:
            continue
        pending.extend(reversed(current.named_children))
    return values


def _ancestors(node: Any):
    while node is not None:
        yield node
        node = node.parent


def _inside(outer: Any, inner: Any) -> bool:
    return outer is not None and inner is not None and outer.start_byte <= inner.start_byte and inner.end_byte <= outer.end_byte


def _function(definition: Any) -> Any:
    return definition.node if definition.node.type in _FUNCTIONS else unwrap(definition.value)


def _owner(node: Any) -> Any:
    return next((parent for parent in _ancestors(node.parent) if parent.type in _FUNCTIONS), None)


def _op(document: Any, node: Any) -> str:
    operator = node.child_by_field_name("operator") if node is not None else None
    if operator is not None:
        return document.text(operator)
    # Plain assignment '=' has no named operator field in this grammar.
    return next((child.type for child in node.children if child.type in {"=", "+=", "-=", "++", "--"}), "") if node is not None else ""


def _integer(document: Any, node: Any) -> int | None:
    node = unwrap(node)
    if node is None or node.type != "number":
        return None
    text = document.text(node)
    return int(text) if re.fullmatch(r"0|[1-9][0-9]{0,15}", text) else None


def _identity(record: dict) -> dict:
    result = {key: record.get(key) for key in ("state", "identity_complete", "declaration_id", "binding_id",
        "name", "declaration_kind", "file", "source_hash", "declaration_span", "binder_span", "scope_span", "parameter_index") if key in record}
    result["runtime_value_known"] = False
    return result


def _terminal(statement: Any) -> Any:
    values = _children(statement) if statement is not None and statement.type == "statement_block" else [statement]
    value = values[-1] if values else None
    return value if value is not None and value.type in {"return_statement", "throw_statement", "break_statement", "continue_statement"} else None


class _Context:
    def __init__(self, snapshot: GraphSnapshot, sources: SemanticSources):
        self.snapshot, self.sources = snapshot, sources
        self.documents: dict[str, Any] = {}
        self.readers: dict[str, LexicalBindings] = {}
        counts = Counter(node.id for node in snapshot.nodes)
        self.nodes = {node.id: node for node in snapshot.nodes if counts[node.id] == 1}
        self.node_ids: set[str] = set()
        self.edge_ids: set[str] = set()
        self.gaps: list[dict] = []

    def gap(self, code: str, message: str, document: Any = None, node: Any = None) -> None:
        value = {"code": code, "message": message}
        if document is not None and node is not None:
            value["location"] = self.ref(document, node)
        self.gaps.append(value)

    def ref(self, document: Any, node: Any) -> dict | None:
        if node is None:
            return None
        value = document.location(node)
        value["node_type"] = node.type
        value["source_excerpt"] = value.get("source_excerpt", "")[:1000]
        value["source_excerpt_truncated"] = value.get("source_excerpt_truncated", False) or node.end_byte - node.start_byte > 1000
        return value

    def reader(self, document: Any) -> LexicalBindings:
        if document.source.path not in self.readers:
            self.readers[document.source.path] = LexicalBindings(document)
        return self.readers[document.source.path]

    def attach(self, document: Any, definition: Any) -> str | None:
        graph_id = getattr(definition, "graph_node_id", "")
        target = self.nodes.get(graph_id)
        if target is not None:
            source, actual, gaps = self.sources.definition_for_node(target)
            if source is document and actual is definition and not gaps:
                self.node_ids.add(graph_id)
                return graph_id
        return None

    def owner(self, document: Any, node: Any, subject: Any) -> dict:
        function = _owner(node)
        if node.type in _FUNCTIONS:
            function = node
        definition = document.definition_for_ast(function) if function is not None else None
        graph_id = self.attach(document, definition) if definition is not None else None
        return {"location": self.ref(document, function), "symbol": definition.symbol if definition is not None else None,
            "graph_node_id": graph_id, "nested_callable": function is not None and function != subject,
            "kind": function_kind(document, function), "activation_proven": False}

    def conditions(self, document: Any, node: Any, subject: Any) -> list[dict]:
        values, child = [], node
        for parent in _ancestors(node.parent if node is not None else None):
            if parent == subject:
                break
            if parent.type == "if_statement":
                branch = "consequence" if parent.child_by_field_name("consequence") == child else "alternative" if parent.child_by_field_name("alternative") == child else "condition"
                values.append({"kind": "if", "branch": branch, "condition": self.ref(document, parent.child_by_field_name("condition"))})
            elif parent.type in {"for_statement", "for_in_statement", "while_statement", "do_statement", "try_statement", "catch_clause", "finally_clause", "switch_case", "switch_default"}:
                values.append({"kind": parent.type, "location": self.ref(document, parent), "execution_condition_evaluated": False})
            elif parent.type in _FUNCTIONS:
                values.append({"kind": "nested_callable", "owner": self.owner(document, parent, subject), "activation_proven": False})
            child = parent
        return values

    def writes(self, document: Any, identity: dict, subject: Any) -> dict:
        reader = self.reader(document)
        records = reader.writes(identity)
        facts = []
        shapes_complete = identity.get("state") == "unique" and identity.get("identity_complete", False)
        for record in records:
            mutation = reader.mutation_for(record)
            precise = bool(record.get("identity_match_known") and record.get("binding_reassignment")
                and record.get("mutation_target_complete") and not record.get("possible_effect"))
            amount = _integer(document, mutation.child_by_field_name("right")) if mutation is not None else None
            operator = _op(document, mutation)
            increment_form = bool(precise and mutation is not None and (
                mutation.type == "augmented_assignment_expression" and operator in {"+=", "-="} and amount is not None
                or mutation.type == "update_expression" and operator in {"++", "--"}))
            if record.get("possible_effect") or record.get("binding_reassignment") and not increment_form:
                shapes_complete = False
            facts.append({"kind": record.get("kind"), "location": self.ref(document, mutation) if mutation is not None else record.get("source_location"),
                "identity_match_known": record.get("identity_match_known", False), "binding_reassignment": record.get("binding_reassignment", False),
                "possible_effect": record.get("possible_effect", False), "member_write": record.get("member_write", False),
                "increment_source_form": increment_form, "operator": operator, "literal_amount": amount,
                "scope_inside_subject": _inside(subject, mutation), "owner": self.owner(document, mutation, subject) if mutation is not None else None,
                "conditions": self.conditions(document, mutation, subject) if mutation is not None else [], "execution_proven": False})
        return {"supported_captured_write_forms_scanned": True, "record_count": len(records), "source_increment_shapes_complete": shapes_complete,
            "facts": facts[:_SITE_LIMIT], "truncated": len(facts) > _SITE_LIMIT,
            "complex_alias_or_arbitrary_call_effects_closed": False,
            "runtime_counter_domain_proven": False, "attempts_completed_from_write_count_proven": False}

    def call(self, document: Any, call: Any) -> tuple[dict, Any, Any]:
        function = _owner(call)
        edge, gaps = self.sources.call_binding(call, document, function)
        fact = {"location": self.ref(document, call), "callee_source": document.text(call.child_by_field_name("function"))[:512],
            "binding_state": "unknown", "issues": gaps[:_SAMPLE], "issue_count": len(gaps), "activation_proven": False,
            "completion": completion_relation(document, call, function, lexical=self.reader(document))}
        if edge is None or edge.target not in self.nodes:
            return fact, None, None
        target = self.nodes[edge.target]
        target_doc, definition, issues = self.sources.definition_for_node(target)
        if target_doc is None or definition is None or issues:
            fact["target_issues"] = issues[:_SAMPLE]
            return fact, None, None
        self.documents[target_doc.source.path] = target_doc
        self.node_ids.add(target.id)
        self.edge_ids.add(edge.id)
        function = _function(definition)
        fact.update(binding_state="snapshot_resolved", edge_id=edge.id, target_graph_node_id=edge.target,
            target_declaration=self.ref(target_doc, definition.node), function_kind=function_kind(target_doc, function))
        return fact, target_doc, function

    def origin(self, document: Any, node: Any, depth: int = 0, seen: frozenset = frozenset(), helper_depth: int = 0) -> dict:
        node = unwrap(node)
        if node is None:
            return {"state": "unknown", "reason": "no_initializer_or_expression"}
        value = {"state": "source_form", "location": self.ref(document, node), "form": node.type, "runtime_value_proven": False}
        if depth > _ORIGIN_DEPTH:
            return {**value, "state": "unknown", "reason": "origin_depth_budget"}
        number = _integer(document, node)
        if number is not None:
            return {**value, "literal_integer": number}
        if node.type == "string":
            from .static_contracts import _literal_string
            return {**value, "literal_string": _literal_string(document.text(node))}
        if node.type in {"true", "false", "null"}:
            return {**value, "literal_kind": node.type}
        if node.type == "identifier":
            reader = self.reader(document)
            identity = reader.resolve(node)
            value["binding"] = _identity(identity)
            key = identity.get("declaration_id")
            declaration = reader.declaration_for(identity)
            if identity.get("state") != "unique" or not identity.get("identity_complete") or key in seen:
                return {**value, "state": "unknown", "reason": "binding_unknown_or_origin_cycle"}
            if declaration is not None and declaration.type == "variable_declarator":
                writes = reader.writes(identity)
                effects = [item for item in writes if item.get("binding_reassignment") or item.get("possible_effect")]
                value["captured_binding_effect_count"] = len(effects)
                value["initializer"] = self.origin(document, declaration.child_by_field_name("value"), depth + 1, seen | {key}, helper_depth)
                value["reaching_value_origin_proven"] = False
            else:
                value["source_form_role"] = identity.get("declaration_kind")
            return value
        if node.type in {"member_expression", "subscript_expression"}:
            value["receiver"] = self.origin(document, node.child_by_field_name("object"), depth + 1, seen, helper_depth)
            field = node.child_by_field_name("property") or node.child_by_field_name("index")
            value["field_source"] = self.ref(document, field)
            value["property_identity_or_getter_proven"] = False
            if node.type == "subscript_expression":
                value["index_source"] = self.origin(document, field, depth + 1, seen, helper_depth)
            return value
        if node.type == "binary_expression":
            value.update(operator=_op(document, node), left=self.origin(document, node.child_by_field_name("left"), depth + 1, seen, helper_depth),
                right=self.origin(document, node.child_by_field_name("right"), depth + 1, seen, helper_depth), operator_evaluated=False)
            return value
        if node.type == "ternary_expression":
            value.update(condition=self.ref(document, node.child_by_field_name("condition")),
                consequence=self.origin(document, node.child_by_field_name("consequence"), depth + 1, seen, helper_depth),
                alternative=self.origin(document, node.child_by_field_name("alternative"), depth + 1, seen, helper_depth), selected_branch_proven=False)
            return value
        if node.type == "call_expression":
            arguments = _children(node.child_by_field_name("arguments"))
            value["arguments"] = [self.origin(document, argument, depth + 1, seen, helper_depth) for argument in arguments[:_SAMPLE]]
            value["argument_count"] = len(arguments)
            value["arguments_truncated"] = len(arguments) > _SAMPLE
            binding, helper_doc, helper_function = self.call(document, node)
            value["call_binding"] = binding
            value["normalization_semantics_proven"] = False
            if helper_doc is not None and helper_function is not None and helper_depth < 1:
                value["helper_source"] = self.helper(helper_doc, helper_function)
            else:
                value["helper_source_state"] = "helper_hop_limit" if helper_depth >= 1 else "actual_helper_binding_unknown"
            return value
        if node.type in {"object", "array"}:
            fields = _children(node)
            value["entries"] = [{"key": self.ref(document, item.child_by_field_name("key")),
                "value": self.origin(document, item.child_by_field_name("value"), depth + 1, seen, helper_depth)} if item.type == "pair"
                else self.origin(document, item, depth + 1, seen, helper_depth) for item in fields[:_SAMPLE]]
            value["entry_count"] = len(fields)
            value["entries_truncated"] = len(fields) > _SAMPLE
            value["runtime_aggregate_membership_proven"] = False
            return value
        return {**value, "state": "unknown", "reason": "unsupported_origin_expression"}

    def helper(self, document: Any, function: Any) -> dict:
        kind = function_kind(document, function)
        if not kind["ordinary"]:
            return {"state": "unknown", "reason": "helper_callable_kind_unknown", "kind": kind}
        body = function.child_by_field_name("body")
        nodes = _walk(body, nested=False)
        returns = [node for node in nodes if node.type == "return_statement"]
        declarations = [node for node in nodes if node.type == "variable_declarator"]
        guards = [node for node in nodes if node.type == "if_statement"]
        params = _children(function.child_by_field_name("parameters"))
        return {"state": "source_body_available", "location": self.ref(document, function), "kind": kind,
            "parameter_sources": [self.ref(document, param) for param in params[:_SAMPLE]],
            "declaration_count": len(declarations), "declarations": [{"location": self.ref(document, declaration),
                "initializer": self.origin(document, declaration.child_by_field_name("value"), helper_depth=1)} for declaration in declarations[:_SAMPLE]],
            "guard_count": len(guards), "guards": [{"condition": self.ref(document, guard.child_by_field_name("condition")),
                "consequence_tail": self.ref(document, _terminal(guard.child_by_field_name("consequence")))} for guard in guards[:_SAMPLE]],
            "return_count": len(returns), "returns": [{"location": self.ref(document, returned),
                "expression": self.origin(document, _children(returned)[0] if len(_children(returned)) == 1 else None, helper_depth=1),
                "conditions": self.conditions(document, returned, function)} for returned in returns[:_SAMPLE]],
            "truncated": any(len(items) > _SAMPLE for items in (params, declarations, guards, returns)),
            "normalization_interpreted": False, "parameter_argument_runtime_mapping_proven": False, "numeric_threshold_proven": False,
            "exception_paths_unknown": True, "runtime_activation_proven": False, "all_path_completion_proven": False}


def _comparison(context: _Context, document: Any, node: Any, rule: dict, subject: Any) -> dict | None:
    if node.type != "binary_expression" or _op(document, node) not in _COMPARISONS:
        return None
    left, right = unwrap(node.child_by_field_name("left")), unwrap(node.child_by_field_name("right"))
    if left is None or right is None or left.type != "identifier" or right.type != "identifier":
        return None
    names = {document.text(left), document.text(right)}
    if names != {rule["counter"]["name"], rule["limit"]["name"]}:
        return None
    counter_node, limit_node = (left, right) if document.text(left) == rule["counter"]["name"] else (right, left)
    reader = context.reader(document)
    counter_identity, limit_identity = reader.resolve(counter_node), reader.resolve(limit_node)
    counter_declaration, limit_declaration = reader.declaration_for(counter_identity), reader.declaration_for(limit_identity)
    identities_closed = all(record.get("state") == "unique" and record.get("identity_complete") for record in (counter_identity, limit_identity))
    declarations_inside = all(declaration is not None and declaration.type == "variable_declarator" and _inside(subject, declaration)
        for declaration in (counter_declaration, limit_declaration))
    return {"location": context.ref(document, node), "operator": _op(document, node), "counter_side": "left" if counter_node == left else "right",
        "counter_binding": _identity(counter_identity), "limit_binding": _identity(limit_identity),
        "counter_declaration": context.ref(document, counter_declaration), "limit_declaration": context.ref(document, limit_declaration),
        "counter_initializer": context.origin(document, counter_declaration.child_by_field_name("value")) if counter_declaration is not None and declarations_inside else {"state": "unknown"},
        "limit_origin": context.origin(document, limit_declaration.child_by_field_name("value")) if limit_declaration is not None and declarations_inside else {"state": "unknown"},
        "captured_local_binding_relation_complete": identities_closed and declarations_inside,
        "owner": context.owner(document, node, subject), "conditions": context.conditions(document, node, subject),
        "numeric_operands_proven": False, "comparison_execution_proven": False,
        "_node": node, "_counter_node": counter_node, "_limit_node": limit_node,
        "_counter_identity": counter_identity, "_limit_identity": limit_identity,
        "_counter_declaration": counter_declaration, "_limit_declaration": limit_declaration}


def _guard(context: _Context, document: Any, comparison: dict, rule: dict, subject: Any) -> dict | None:
    node = comparison["_node"]
    guard = next((parent for parent in _ancestors(node.parent) if parent.type == "if_statement"
        and _inside(parent.child_by_field_name("condition"), node)), None)
    if guard is None:
        return None
    condition = guard.child_by_field_name("condition")
    exact = unwrap(condition) == node
    branches = {}
    for branch in ("consequence", "alternative"):
        statement = guard.child_by_field_name(branch)
        tail = _terminal(statement)
        statements = _children(statement) if statement is not None and statement.type == "statement_block" else [statement] if statement is not None else []
        actions = []
        for action in statements[:_SAMPLE]:
            expressions = _children(action) if action.type in {"expression_statement", "return_statement", "throw_statement"} else []
            expression = unwrap(expressions[0]) if len(expressions) == 1 else None
            awaited = expression is not None and expression.type == "await_expression"
            inner = unwrap(_children(expression)[0]) if awaited and len(_children(expression)) == 1 else expression
            action_call = inner if inner is not None and inner.type == "call_expression" else None
            actions.append({"statement_type": action.type, "location": context.ref(document, action),
                "direct_await_source": awaited, "call_source": context.ref(document, action_call),
                "completion": completion_relation(document, action_call, _owner(action_call), lexical=context.reader(document)) if action_call is not None else None,
                "owner": context.owner(document, action, subject), "execution_or_normal_fulfillment_proven": False})
        branches[branch] = {"location": context.ref(document, statement), "terminal_tail": context.ref(document, tail),
            "terminal_form": tail.type if tail is not None else None, "direct_source_action_count": len(statements),
            "direct_source_actions": actions, "source_actions_truncated": len(statements) > _SAMPLE,
            "normal_prefix_reachability_proven": False, "comparison_guarantees_exit_proven": False}
    shape = exact and any(value["terminal_tail"] is not None for value in branches.values())
    return {"pattern": rule["type"], "source_form_state": "source_backed_local_pattern" if shape else "unknown",
        "guard": context.ref(document, guard), "full_condition": context.ref(document, condition),
        "comparison_is_entire_condition": exact, "condition_polarity": "direct_comparison" if exact else "compound_or_negated_unknown",
        "branches": branches, "interpreted_exhaustion_polarity_proven": False, "guard_dominates_subject_execution": False}


def _loop(context: _Context, document: Any, comparison: dict, rule: dict, subject: Any) -> dict | None:
    node = comparison["_node"]
    loop = next((parent for parent in _ancestors(node.parent) if parent.type == "for_statement"
        and _inside(parent.child_by_field_name("condition"), node)), None)
    if loop is None:
        return None
    condition = loop.child_by_field_name("condition")
    initializer, update = loop.child_by_field_name("initializer"), unwrap(loop.child_by_field_name("increment"))
    declaration = comparison["_counter_declaration"]
    initial = _integer(document, declaration.child_by_field_name("value")) if declaration is not None else None
    update_target = unwrap(update.child_by_field_name("left") or update.child_by_field_name("argument")) if update is not None else None
    update_identity = context.reader(document).resolve(update_target) if update_target is not None and update_target.type == "identifier" else {}
    operator = _op(document, update)
    amount = _integer(document, update.child_by_field_name("right")) if update is not None else None
    update_shape = bool(update is not None and update_target is not None and update_target.type == "identifier"
        and context.reader(document).same(comparison["_counter_identity"], update_identity)
        and (update.type == "augmented_assignment_expression" and operator in {"+=", "-="} and amount is not None
            or update.type == "update_expression" and operator in {"++", "--"}))
    shape = bool(unwrap(condition) == node and _inside(initializer, declaration) and initial is not None and update_shape)
    body = loop.child_by_field_name("body")
    abrupt = [candidate for candidate in _walk(body, nested=False) if candidate.type in {"return_statement", "throw_statement", "break_statement", "continue_statement"}]
    return {"pattern": rule["type"], "source_form_state": "source_backed_local_pattern" if shape else "unknown",
        "loop": context.ref(document, loop), "condition_is_entire_comparison": unwrap(condition) == node,
        "initializer": context.ref(document, initializer), "initial_literal": initial,
        "update": {"location": context.ref(document, update), "operator": operator, "literal_amount": amount,
            "same_counter_binding": update_shape, "execution_proven": False},
        "abrupt_source_count": len(abrupt), "abrupt_source_samples": [{"location": context.ref(document, item),
            "conditions": context.conditions(document, item, subject)} for item in abrupt[:_SAMPLE]],
        "abrupt_sources_truncated": len(abrupt) > _SAMPLE, "numeric_bound_proven": False,
        "termination_proven": False, "actual_iteration_count_proven": False}


def _summary(context: _Context, rule: dict) -> dict:
    document, definition, gaps = context.sources.select(rule["subject"])
    context.gaps.extend(gaps)
    result = {"schema": "callscope.local-budget-evidence.v1", "version": VERSION, "policy_version": POLICY_VERSION,
        "model_id": MODEL_ID, "snapshot_id": context.snapshot.id, "subject": rule["subject"], "assessments": [],
        "evaluation": "all_lexical_sites", "source_scope": "selected subject lexical tree; nested callable activation remains unknown",
        "candidate_scope": "guard/header conditions directly referencing the configured local names; aliases and transitive helper consumption are not exhaustively enumerated",
        "all_transitive_reference_coverage_proven": False,
        "shared_model_versions": {"semantic_sources": SOURCE_VERSION, "lexical": LEXICAL_VERSION, "completion": COMPLETION_VERSION},
        "source_form_complete": False, "numeric_bound_proven": False, "runtime_budget_consumption_proven": False,
        "whole_function_domination_proven": False, "whole_project_unconsumed_check_performed": False, "termination_proven": False}
    if document is None or definition is None:
        result["assessments"] = [{"source_form_state": "unknown", "reason": "subject_source_or_definition_unavailable"}]
        return result
    context.documents[document.source.path] = document
    result["subject_graph_node_id"] = context.attach(document, definition)
    function = _function(definition)
    result["subject_kind"] = function_kind(document, function)
    if function is None or not result["subject_kind"]["ordinary"]:
        result["assessments"] = [{"source_form_state": "unknown", "reason": "subject_callable_kind_unknown"}]
        return result
    body = function.child_by_field_name("body")
    nodes = _walk(body)
    reader = context.reader(document)
    candidate_counts = {}
    for role in ("counter", "limit"):
        candidates = [node for node in nodes if node.type == "variable_declarator"
            and node.child_by_field_name("name") is not None and node.child_by_field_name("name").type == "identifier"
            and document.text(node.child_by_field_name("name")) == rule[role]["name"]]
        candidate_counts[role] = len(candidates)
    result["locator_declaration_counts"] = candidate_counts
    locators_unique = all(value == 1 for value in candidate_counts.values())
    if not locators_unique:
        context.gap("budget_local_locator_ambiguous_or_missing", "所选词法范围中 local_binding 定位器未唯一命中，不能按同名猜预算。", document, function)
    assessments = []
    seen_sites = set()
    covered_regions = set()
    for node in nodes:
        comparison = _comparison(context, document, node, rule, function)
        if comparison is None:
            continue
        pattern = _loop(context, document, comparison, rule, function) if rule["type"] == "bounded_for_loop" else _guard(context, document, comparison, rule, function)
        if pattern is None:
            continue
        site_key = (pattern["pattern"], node.start_byte, node.end_byte)
        if site_key in seen_sites:
            continue
        seen_sites.add(site_key)
        covered_regions.add((pattern["pattern"], (pattern.get("guard") or pattern.get("loop"))["start_byte"]))
        if len(assessments) >= _SITE_LIMIT:
            raise ValueError("budget_site_budget_exceeded")
        counter_writes = context.writes(document, comparison["_counter_identity"], function)
        limit_writes = reader.writes(comparison["_limit_identity"])
        limit_effects = [item for item in limit_writes if item.get("binding_reassignment") or item.get("possible_effect")]
        pattern.update(comparison={key: value for key, value in comparison.items() if not key.startswith("_")},
            counter_writes=counter_writes, limit_binding_effect_count=len(limit_effects),
            selected_binding_identity_relation_complete=comparison["captured_local_binding_relation_complete"],
            locator_names_unique=locators_unique, runtime_limit_value_proven=False, runtime_counter_value_proven=False,
            phase_or_job_budget_equivalence_proven=False, guard_or_loop_activation_proven=False)
        if not locators_unique or not comparison["captured_local_binding_relation_complete"]:
            pattern["source_form_state"] = "unknown"
            pattern["reason"] = "local_operand_declaration_identity_unknown_or_locator_ambiguous"
        assessments.append(pattern)
    # Retain related source conditions that the finite direct-identifier model
    # did not recognize. Sampling never removes them from the completeness bit.
    candidate_count = 0
    candidate_kind = "if_statement" if rule["type"] == "counter_exhaustion_guard" else "for_statement"
    for region in nodes:
        if region.type != candidate_kind:
            continue
        condition = region.child_by_field_name("condition")
        references = [item for item in _walk(condition) if item.type == "identifier"
            and document.text(item) in {rule["counter"]["name"], rule["limit"]["name"]}]
        names = {document.text(item) for item in references}
        if names != {rule["counter"]["name"], rule["limit"]["name"]}:
            continue
        candidate_count += 1
        if (rule["type"], region.start_byte) in covered_regions:
            continue
        if len(assessments) >= _SITE_LIMIT:
            raise ValueError("budget_site_budget_exceeded")
        assessments.append({"pattern": rule["type"], "source_form_state": "unknown",
            "reason": "related_condition_outside_direct_operand_model", "location": context.ref(document, region),
            "condition": context.ref(document, condition), "owner": context.owner(document, region, function),
            "selected_local_reference_count": len(references),
            "reference_samples": [{"location": context.ref(document, item), "binding": _identity(reader.resolve(item))} for item in references[:_SAMPLE]],
            "reference_samples_truncated": len(references) > _SAMPLE,
            "numeric_bound_proven": False, "runtime_budget_consumption_proven": False})
        context.gap("budget_related_source_condition_unknown", "相关 guard/header 源条件不属于有限直接操作数形状，保留unknown而不静默排除。", document, region)
    result["related_guard_or_header_candidate_count"] = candidate_count
    if not assessments:
        assessments.append({"source_form_state": "unknown", "reason": "selected_local_pattern_not_found",
            "interpretation": "zero matching source sites is not a whole-project unconsumed-budget finding"})
        context.gap("budget_local_site_unavailable", "所选范围未找到契约有限形状，缺site不能作为通过或全程序未消费证据。", document, function)
    result["assessments"] = assessments
    result["source_form_complete"] = bool(locators_unique and assessments and all(item["source_form_state"] == "source_backed_local_pattern" for item in assessments))
    context.gap("budget_numeric_values_and_execution_unknown", "局部初始化/比较/更新来源不证明实际数值域、限额选择、执行次数、终止或异常完成。", document, function)
    if any(item.get("comparison", {}).get("owner", {}).get("nested_callable") for item in assessments):
        context.gap("budget_nested_guard_activation_unknown", "嵌套闭包读取外层绑定是源码捕获关系，不证明父函数每条路径调用该检查。", document, function)
    return result


def _finding(snapshot: GraphSnapshot, rule: dict, summary: dict, context: _Context) -> Finding:
    fingerprint = _digest({"version": VERSION, "policy_version": POLICY_VERSION, "model": MODEL_ID,
        "project": snapshot.project_id, "rule": rule})
    counts = Counter(item.get("source_form_state", "unknown") for item in summary.get("assessments", []))
    details = {**summary, "contract_hash": _digest(rule), "policy_hash": snapshot.policy_hash,
        "source_hash": snapshot.source_hash, "assessment_counts": dict(sorted(counts.items())),
        "analysis_gap_count": len(context.gaps), "analysis_gap_samples": context.gaps[:64], "analysis_gaps_truncated": len(context.gaps) > 64,
        "captured_source_inputs": [{"file": path, "source_hash": document.source.hash, "status": document.source.status,
            "parser_version": document.parser_version, "parse_provenance": document.parse_provenance} for path, document in sorted(context.documents.items())],
        "provenance": rule.get("provenance", {}), "applicability": rule.get("applicability", {}),
        "target_code_executed": False, "interpretation": "局部预算源码形状与实际声明/调用出处；不裁定完整P5、跨层预算等价或全项目消费。"}
    locations = [item.get("comparison", {}).get("location") for item in summary.get("assessments", []) if item.get("comparison", {}).get("location")]
    description = "从保存 AST 提取所选计数器/阈值绑定、guard或for形状、增量来源及未知条件；不证明运行次数或完整预算执行。"
    evidence = Evidence(id=_digest({"snapshot": snapshot.id, "fingerprint": fingerprint, "details": details})[:24],
        kind="static_budget_analysis", message=description, locations=locations, node_ids=sorted(context.node_ids), edge_ids=sorted(context.edge_ids), details=details)
    return Finding(id=_digest({"snapshot": snapshot.id, "fingerprint": fingerprint})[:24], type="static_local_budget",
        severity=rule.get("severity", "info"), status="uncertain", title="局部预算来源与检查形状待复核", description=description,
        node_ids=sorted(context.node_ids), edge_ids=sorted(context.edge_ids), evidence=[evidence], rule_id=rule.get("id", "invalid-budget-rule"),
        fingerprint=fingerprint, snapshot_id=snapshot.id, metadata={"budget_analyzer_version": VERSION, "budget_policy_version": POLICY_VERSION,
            "assessment_counts": dict(sorted(counts.items())), "source_form_complete": summary.get("source_form_complete", False),
            "numeric_bound_proven": False, "termination_proven": False, "runtime_budget_consumption_proven": False,
            "whole_function_domination_proven": False, "whole_project_unconsumed_check_performed": False,
            "provenance": rule.get("provenance", {}), "applicability": rule.get("applicability", {})})


def analyze_budget_contracts(snapshot: GraphSnapshot, rules: list[dict]) -> list[Finding]:
    """Preserve positive source forms and unknown assessments, all uncertain."""
    if not isinstance(snapshot, GraphSnapshot):
        raise ValueError("budget analysis requires a captured GraphSnapshot")
    sources = SemanticSources(snapshot)
    if not isinstance(rules, list) or len(rules) > 256:
        context = _Context(snapshot, sources)
        context.gap("budget_rules_invalid", "budget_contracts 必须为最多256项JSON列表。")
        return [_finding(snapshot, {"id": "invalid-budget-contracts", "severity": "info"},
            {"assessments": [{"source_form_state": "unknown", "reason": "invalid_rules"}]}, context)]
    ids = Counter(rule.get("id") for rule in rules if isinstance(rule, dict) and isinstance(rule.get("id"), str))
    findings = []
    for index, rule in enumerate(rules):
        context = _Context(snapshot, sources)
        try:
            validate_budget_rule(rule)
            if ids[rule["id"]] != 1:
                raise ValueError("预算合同 id 重复，不能覆盖。")
            summary = _summary(context, rule)
        except (ValueError, TypeError, RecursionError, OverflowError) as error:
            context.gap("budget_rule_or_analysis_unknown", str(error)[:1000])
            original_id = rule.get("id") if isinstance(rule, dict) else None
            summary = {"original_rule_id": original_id if isinstance(original_id, str) else None,
                "assessments": [{"source_form_state": "unknown", "reason": str(error)[:1000]}]}
            severity = rule.get("severity") if isinstance(rule, dict) else None
            rule = {"id": f"invalid-budget-rule-{index}", "severity": severity if isinstance(severity, str)
                and severity in {"high", "medium", "low", "info"} else "info"}
        findings.append(_finding(snapshot, rule, summary, context))
    return findings
