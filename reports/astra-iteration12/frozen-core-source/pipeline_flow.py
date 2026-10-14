"""Finite, source-authenticated parameter/record/message/budget relationships.

This module reads a captured GraphSnapshot. It never executes a target or
creates CALLS edges. Source structure, conditional language models, physical
message seams and product intent remain different proof domains. Incomplete
connections are required obligations, not environment assumptions.
"""
from __future__ import annotations

from collections import Counter, deque
from dataclasses import asdict, dataclass, replace
import json
import posixpath
from typing import Any

from .completion_summaries import completion_relation, function_kind
from .lexical_bindings import LexicalBindings, VERSION as LEXICAL_VERSION
from .models import Evidence, Finding, GraphSnapshot
from .semantic_sources import SemanticSources, VERSION as SOURCE_VERSION, unwrap
from .static_contracts import _digest, _literal_string

VERSION = "finite-parameter-record-budget-flow-1"
POLICY_VERSION = "parameter-record-budget-policy-1"
MODELS = (
    "ordinary-record-tree-flow-v1", "standard-json-record-codec-v1",
    "normal-async-callback-transfer-v1", "source-derived-module-assembly-v1",
    "normal-durable-record-channel-v1",
    "normal-authenticated-json-broker-channel-v1",
)
_FUNCTIONS = {"function_declaration", "generator_function_declaration", "function_expression",
    "generator_function", "arrow_function", "method_definition"}
_ERASED = {"comment", "type_annotation", "type_arguments", "type_parameters", "type_query",
    "interface_declaration", "type_alias_declaration", "implements_clause"}
_MAX_NODES, _MAX_FUNCTIONS, _MAX_DEPTH, _MAX_FACTS = 50000, 256, 16, 12000


@dataclass(frozen=True, slots=True)
class SourceAnchor:
    snapshot_id: str
    file: str
    source_hash: str
    owner: str
    start_byte: int
    end_byte: int
    parser_id: str


@dataclass(frozen=True, slots=True)
class RecordIdentity:
    identity_id: str
    anchor: SourceAnchor
    kind: str
    expression_id: str
    key_expression_ids: tuple[str, ...]
    receiver_identity: str = ""


@dataclass(frozen=True, slots=True)
class FlowLink:
    link_id: str
    kind: str
    source: str
    target: str
    anchor: SourceAnchor
    conditions: tuple[str, ...] = ()
    model_id: str = ""
    support: str = "source_structure"
    call_site: str = ""
    frame_action: str = ""


def _children(node: Any) -> list[Any]:
    return [item for item in node.named_children if item.type not in _ERASED] if node is not None else []


def _field(node: Any, name: str) -> Any:
    return node.child_by_field_name(name) if node is not None else None


def _walk(node: Any, *, nested: bool = False):
    pending = [node] if node is not None else []
    while pending:
        current = pending.pop()
        if current.type in _ERASED or current.type.endswith("_type"):
            continue
        yield current
        if current is not node and not nested and current.type in _FUNCTIONS | {"class", "class_declaration"}:
            continue
        operand = unwrap(current)
        if operand is not None and operand.id != current.id:
            pending.append(operand)
        else:
            pending.extend(reversed(_children(current)))


def _fn(definition: Any) -> Any:
    value = unwrap(definition.value) if definition is not None and definition.value is not None else getattr(definition, "node", None)
    return value if value is not None and value.type in _FUNCTIONS else None


def _ancestors(node: Any):
    while node is not None:
        yield node
        node = node.parent


def _locator(value: Any) -> bool:
    return isinstance(value, dict) and set(value) == {"file", "symbol"} and all(isinstance(value[key], str) and value[key] for key in value) and not value["file"].startswith("/") and ".." not in value["file"].split("/")


def _path(value: Any) -> bool:
    return isinstance(value, list) and 0 < len(value) <= 8 and all(isinstance(key, str) and key and "\\" not in key for key in value)


def validate_pipeline_flow_rule(rule: Any) -> None:
    """Accept source locators and intent; reject a configured proof chain."""
    required = {"id", "type", "original_claim", "entry", "producer", "request", "worker", "budgets",
        "sources", "models", "invariant", "conditions", "refutations", "provenance"}
    if not isinstance(rule, dict) or set(rule) != required or rule.get("type") != "parameter_budget_flow":
        raise ValueError("pipeline contract requires the fixed locator/intent schema; relation chains and results are forbidden")
    if not isinstance(rule["id"], str) or not rule["id"] or not isinstance(rule["original_claim"], str):
        raise ValueError("pipeline id and original_claim must be strings")
    if not _locator(rule["entry"]):
        raise ValueError("entry must locate one captured lexical function")
    producer = rule["producer"]
    if not isinstance(producer, dict) or set(producer) != {"owner", "parameter_index", "option", "output_path"} or not _locator(producer["owner"]) or type(producer["parameter_index"]) is not int or not 0 <= producer["parameter_index"] <= 32 or not isinstance(producer["option"], str) or not _path(producer["output_path"]):
        raise ValueError("producer needs an owner, actual argument formal locator, option and return field locator")
    for key in ("request", "worker"):
        sink = rule[key]
        if not isinstance(sink, dict) or set(sink) != {"owner", "callee", "argument_index", "field_path"} or not _locator(sink["owner"]) or not isinstance(sink["callee"], str) or type(sink["argument_index"]) is not int or not 0 <= sink["argument_index"] <= 32 or not _path(sink["field_path"]):
            raise ValueError(f"{key} needs captured source call/argument/field locators")
    if not isinstance(rule["sources"], list) or not all(_locator(item) for item in rule["sources"]):
        raise ValueError("sources is an unordered analysis universe of source locators, never intermediate edges")
    budgets = rule["budgets"]
    if not isinstance(budgets, list) or not budgets:
        raise ValueError("at least one budget authority is required")
    for budget in budgets:
        if not isinstance(budget, dict) or set(budget) != {"owner", "kind", "counter", "limit"} or not _locator(budget["owner"]) or not all(isinstance(budget[key], str) and budget[key] for key in ("kind", "counter", "limit")):
            raise ValueError("budget declarations locate a distinct authority/counter/limit, without supplied values or guards")
    if not isinstance(rule["models"], list) or len(set(rule["models"])) != len(rule["models"]) or set(rule["models"]) - set(MODELS):
        raise ValueError("pipeline models must be explicit supported versions")
    invariant = rule["invariant"]
    if not isinstance(invariant, dict) or set(invariant) != {"authority", "requested_budget_kind", "relation", "author_approved"} or invariant["authority"] != "policy-declared" or invariant["relation"] != "request_field_controls_retry_authority" or type(invariant["author_approved"]) is not bool or not isinstance(invariant["requested_budget_kind"], str):
        raise ValueError("invariant is product intent, not a source proof")
    for key in ("conditions", "refutations"):
        if not isinstance(rule[key], list) or not all(isinstance(item, str) and item for item in rule[key]):
            raise ValueError(f"{key} must retain explicit prose")
    if not isinstance(rule["provenance"], dict):
        raise ValueError("provenance must retain the intent authority and original claim source")
    json.dumps(rule, allow_nan=False)


class _Analysis:
    def __init__(self, snapshot: GraphSnapshot, rule: dict):
        self.snapshot, self.rule = snapshot, rule
        self.sources = SemanticSources(snapshot)
        self.documents: dict[str, Any] = {}
        self.readers: dict[str, LexicalBindings] = {}
        self.components: dict[str, tuple[Any, Any, Any]] = {}
        self.terms: dict[str, dict] = {}
        self.facts: dict[str, dict] = {}
        self.links: dict[str, FlowLink] = {}
        self.gaps: list[dict] = []
        self.operations = 0
        self.active: set[tuple[str, int]] = set()
        self.memo: dict[tuple[str, int], str] = {}
        self.nominal_active: set[tuple[str, int]] = set()
        self.nominal_memo: dict[tuple[str, int], list[dict]] = {}
        self.field_write_cache: dict[tuple[str, int], list[Any]] = {}
        self.allocation_index: dict[str, list[tuple[Any, Any, Any]]] = {}
        self.allocation_scanned: set[tuple[str, int]] = set()
        self.codec_write_cache: dict[str, list[Any]] = {}
        self.slot_return_cache: dict[tuple, dict] = {}
        self.identity_cache: dict[tuple[str, int], dict] = {}
        self.path_cache: dict[tuple[str, int], dict | None] = {}

    def gap(self, code: str, document: Any = None, node: Any = None, **details: Any) -> None:
        record = {"code": code, **details}
        if document is not None and node is not None:
            record["location"] = document.location(node)
        if record not in self.gaps:
            self.gaps.append(record)

    def reader(self, document: Any) -> LexicalBindings:
        self.documents[document.source.path] = document
        if document.source.path not in self.readers:
            self.readers[document.source.path] = LexicalBindings(document)
        return self.readers[document.source.path]

    def identity(self, document: Any, node: Any) -> dict:
        """Declaration identity only; value/effect gates remain explicit."""
        if node is None:
            return self.reader(document).resolve_identity(node)
        marker = (document.source.path, node.id)
        if marker not in self.identity_cache:
            self.identity_cache[marker] = self.reader(document).resolve_identity(node)
        return self.identity_cache[marker]

    def anchor(self, document: Any, definition: Any, node: Any) -> SourceAnchor:
        return SourceAnchor(self.snapshot.id, document.source.path, document.source.hash,
            document.call_owner(node) or definition.graph_node_id, node.start_byte, node.end_byte, document.parse_id)

    def conditions(self, document: Any, definition: Any, node: Any) -> tuple[str, ...]:
        result = []
        child = node
        for parent in _ancestors(node.parent):
            if parent == _fn(definition):
                break
            if parent.type == "if_statement":
                condition = _field(parent, "condition")
                branch = "then" if _field(parent, "consequence") == child else "else" if _field(parent, "alternative") == child else "condition"
                fact = self.fact("branch_predicate", document, definition, condition,
                    predicate_text=document.text(condition), branch_truth_verified=False)
                result.append(fact + ":" + branch)
            elif parent.type in {"for_statement", "for_in_statement", "while_statement", "do_statement", "switch_case", "switch_default", "catch_clause", "finally_clause"}:
                fact = self.fact("control_region", document, definition, parent,
                    region_kind=parent.type, normal_reachability_proven=False)
                result.append(fact)
            child = parent
        return tuple(result)

    def fact(self, kind: str, document: Any, definition: Any, node: Any, **details: Any) -> str:
        anchor = self.anchor(document, definition, node)
        record = {"kind": kind, "anchor": asdict(anchor), "location": document.location(node), **details}
        identifier = _digest((VERSION, record))[:32]
        if len(self.facts) >= _MAX_FACTS:
            self.gap("pipeline_fact_budget_exceeded")
        else:
            self.facts[identifier] = {"id": identifier, **record}
        return identifier

    def term(self, kind: str, document: Any, definition: Any, node: Any, **details: Any) -> str:
        record = {"kind": kind, "anchor": asdict(self.anchor(document, definition, node)), **details}
        identifier = _digest((VERSION, record))[:32]
        self.terms[identifier] = {"id": identifier, **record}
        return identifier

    def link(self, kind: str, source: str, target: str, document: Any, definition: Any, node: Any, *,
             model: str = "", support: str = "source_structure", call_site: str = "", action: str = "") -> None:
        record = FlowLink("", kind, source, target, self.anchor(document, definition, node),
            self.conditions(document, definition, node), model, support, call_site, action)
        identifier = _digest((VERSION, asdict(record)))[:32]
        self.links[identifier] = replace(record, link_id=identifier)

    def component(self, selector: dict) -> tuple[Any, Any, Any] | None:
        key = selector["file"] + "#" + selector["symbol"]
        if key in self.components:
            return self.components[key]
        if len(self.components) >= _MAX_FUNCTIONS:
            self.gap("pipeline_component_budget_exceeded", selector=selector)
            return None
        document, definition, problems = self.sources.select(selector)
        function = _fn(definition)
        if document is None or definition is None or function is None:
            self.gap("pipeline_source_invalid", selector=selector, source_issues=problems)
            return None
        self.documents[document.source.path] = document
        self.components[key] = (document, definition, function)
        return document, definition, function

    def key(self, document: Any, node: Any) -> str | None:
        if node is None:
            return None
        if node.type in {"identifier", "property_identifier", "private_property_identifier", "shorthand_property_identifier", "shorthand_property_identifier_pattern"}:
            text = document.text(node)
            return text if "\\" not in text else None
        return _literal_string(document.text(node)) if node.type == "string" else None

    def path(self, document: Any, node: Any) -> dict | None:
        node = unwrap(node)
        parts = []
        while node is not None and node.type in {"member_expression", "subscript_expression"}:
            key = self.key(document, _field(node, "property") if node.type == "member_expression" else _field(node, "index"))
            if node.type == "subscript_expression" and _field(node, "index").type != "string":
                key = None
            parts.append(key)
            node = unwrap(_field(node, "object"))
        if node is not None and node.type == "this":
            return {"root": "this", "declaration_id": "", "keys": list(reversed(parts)), "static": all(key is not None for key in parts)}
        if node is None or node.type not in {"identifier", "shorthand_property_identifier"}:
            return None
        identity = self.identity(document, node)
        return {"root": document.text(node), "declaration_id": identity.get("declaration_id"),
            "keys": list(reversed(parts)), "static": all(key is not None for key in parts),
            "identity": {key: identity.get(key) for key in ("state", "declaration_kind", "parameter_index", "pattern_path", "declaration_id")}}

    def project(self, value: str, keys: list[str], document: Any, definition: Any, node: Any) -> str:
        if not keys:
            return value
        term = self.terms[value]
        if term["kind"] == "binding_sources" and not term["writes"]:
            return self.project(term["initializer"], keys, document, definition, node)
        if term["kind"] == "record_literal":
            candidates = []
            for member in reversed(term["members"]):
                if member["kind"] == "definition" and member["key"] == keys[0]:
                    return self.project(member["value"], keys[1:], document, definition, node)
                if member["kind"] == "spread":
                    candidate = self.project(member["value"], keys, document, definition, node)
                    if self.terms[candidate]["kind"] != "absent":
                        candidates.append(candidate)
                        break
                if member["kind"] == "unknown":
                    break
            if candidates:
                return self.term("current_copy_projection", document, definition, node,
                    source=candidates[0], selected_path=keys, model="ordinary-record-tree-flow-v1",
                    initial_origin_proven=False, presence_proven=False)
            if term["static_keys_complete"] and not any(member["kind"] == "unknown" for member in term["members"]):
                return self.term("absent", document, definition, node, selected_path=keys)
        if term["kind"] == "alternatives":
            return self.term("alternatives", document, definition, node,
                values=[self.project(item, keys, document, definition, node) for item in term["values"]])
        return self.term("field_projection", document, definition, node, receiver=value, path=keys,
            initial_origin_proven=False, current_slot_closed=False)

    def expression(self, document: Any, definition: Any, node: Any, depth: int = 0) -> str:
        node = unwrap(node)
        self.operations += 1
        if node is None or depth > _MAX_DEPTH or self.operations > _MAX_NODES:
            self.gap("pipeline_expression_budget_or_source_missing")
            return self.term("unknown", document, definition, node or _fn(definition), reason="budget_or_missing")
        memo_key = (document.source.path, node.id)
        actual = document.definition_nodes.get(document.call_owner(node), [])
        if len(actual) == 1:
            definition = actual[0]
        if memo_key in self.memo:
            return self.memo[memo_key]
        if memo_key in self.active:
            return self.term("live_binding", document, definition, node, contents_unknown=True)
        self.active.add(memo_key)
        kind = node.type
        if kind in {"string", "number", "true", "false", "null", "undefined"}:
            value = self.term("literal", document, definition, node, literal_kind=kind, text=document.text(node))
        elif kind in {"identifier", "shorthand_property_identifier"}:
            identity = self.identity(document, node)
            declaration = self.reader(document).declaration_for(identity)
            initial = self.reader(document).initializer_for(identity)
            if identity.get("declaration_kind") in {"parameter", "catch_parameter"}:
                value = self.term("formal_read", document, definition, node,
                    declaration_id=identity["declaration_id"], parameter_index=identity.get("parameter_index"),
                    pattern_path=(identity.get("pattern_path") or []), current_value_only=True)
            elif declaration is not None and initial is not None:
                initial_value = self.expression(document, definition, initial, depth + 1)
                writes = []
                for review in self.reader(document).writes(identity):
                    mutation = self.reader(document).mutation_for(review)
                    if mutation is not None and mutation.type == "assignment_expression" and mutation.start_byte < node.start_byte and review.get("binding_reassignment"):
                        writes.append({"value": self.expression(document, definition, _field(mutation, "right"), depth + 1),
                            "conditions": list(self.conditions(document, definition, mutation)), "location": document.location(mutation)})
                value = self.term("binding_sources", document, definition, node, declaration_id=identity["declaration_id"],
                    initializer=initial_value, writes=writes, current_reaching_value_proven=False)
                self.link("initializer_source", initial_value, value, document, definition, node)
            else:
                value = self.term("reference", document, definition, node, source_path=self.path(document, node),
                    current_reaching_value_proven=False)
        elif kind in {"member_expression", "subscript_expression"}:
            receiver = self.expression(document, definition, _field(node, "object"), depth + 1)
            member = self.key(document, _field(node, "property") if kind == "member_expression" else _field(node, "index"))
            if kind == "subscript_expression" and _field(node, "index").type != "string":
                member = None
            value = self.project(receiver, [member], document, definition, node) if member is not None else self.term("dynamic_projection", document, definition, node,
                receiver=receiver, index=self.expression(document, definition, _field(node, "index"), depth + 1))
        elif kind == "object":
            members, complete = [], True
            for child in _children(node):
                if child.type == "spread_element":
                    members.append({"kind": "spread", "value": self.expression(document, definition, _children(child)[0], depth + 1), "anchor": asdict(self.anchor(document, definition, child))})
                elif child.type in {"pair", "shorthand_property_identifier"}:
                    key = self.key(document, _field(child, "key") if child.type == "pair" else child)
                    if key is None or key == "__proto__":
                        complete = False
                    members.append({"kind": "definition", "key": key,
                        "value": self.expression(document, definition, _field(child, "value") if child.type == "pair" else child, depth + 1),
                        "anchor": asdict(self.anchor(document, definition, child))})
                else:
                    complete = False
                    members.append({"kind": "unknown", "node_type": child.type})
            value = self.term("record_literal", document, definition, node, members=members,
                static_keys_complete=complete, private_construction_syntax=complete,
                model_applicability="ordinary-record-tree-flow-v1" in self.rule["models"] and complete,
                nested_record_tree_or_runtime_verified=False)
        elif kind in {"binary_expression", "ternary_expression", "unary_expression", "template_string", "array"}:
            operator = document.text(_field(node, "operator")) if _field(node, "operator") is not None else ""
            operands = [self.expression(document, definition, child, depth + 1) for child in _children(node)]
            value = self.term("expression", document, definition, node, node_type=kind, operator=operator,
                operands=operands, source_text=document.text(node), normal_result_only=True)
        elif kind == "await_expression":
            operand = self.expression(document, definition, _children(node)[0], depth + 1)
            value = self.term("normal_async_consumption", document, definition, node, operand=operand,
                model_enabled="normal-async-callback-transfer-v1" in self.rule["models"], completion_guaranteed=False)
        elif kind in {"call_expression", "new_expression"}:
            arguments = [self.expression(document, definition, child, depth + 1) for child in _children(_field(node, "arguments"))]
            edge, issues = self.sources.call_binding(node, document, definition)
            callee = _field(node, "function") or _field(node, "constructor")
            value = self.term("invocation", document, definition, node, callee_text=document.text(callee),
                callee_path=self.path(document, callee), arguments=arguments, edge_id=edge.id if edge else None,
                target=edge.target if edge else None, binding_issues=issues, body_activation_proven=False)
            if edge is not None:
                self.fact("actual_callee_binding", document, definition, node, edge_id=edge.id,
                    target_graph_node_id=edge.target, argument_value_ids=arguments)
            self.codec(document, definition, node, value, arguments)
        elif kind in _FUNCTIONS:
            value = self.term("callable_source", document, definition, node,
                callable_graph_id=document.call_owner(_field(node, "body") or node), activation_proven=False)
        else:
            value = self.term("unknown_expression", document, definition, node, node_type=kind,
                source_text=document.text(node), unknown_effects=True)
        self.active.discard(memo_key)
        self.memo[memo_key] = value
        return value

    def codec(self, document: Any, definition: Any, node: Any, value: str, arguments: list[str]) -> None:
        callee = _field(node, "function")
        if callee is None or callee.type not in {"member_expression", "subscript_expression"} or document.text(_field(callee, "object")) != "JSON":
            return
        path = self.path(document, callee)
        if not path or path["root"] != "JSON" or path["keys"] not in (["stringify"], ["parse"]):
            return
        root = unwrap(_field(callee, "object"))
        absence = self.reader(document).unbound("JSON", root)
        if document.source.path not in self.codec_write_cache:
            self.codec_write_cache[document.source.path] = [child for child in _walk(document.tree.root_node, nested=True) if child.type in {"assignment_expression", "augmented_assignment_expression", "update_expression"} and (self.path(document, _field(child, "left") or _field(child, "argument")) or {}).get("root") == "JSON"]
        writes = self.codec_write_cache[document.source.path]
        method = path["keys"][0]
        applicable = bool(absence.get("unbound") and not writes and arguments and "standard-json-record-codec-v1" in self.rule["models"] and (method != "stringify" or len(arguments) < 2 or self.terms[arguments[1]].get("text") in {"null", "undefined"}))
        self.fact("json_codec_application", document, definition, node, method=method,
            input_value_id=arguments[0] if arguments else None, output_value_id=value,
            model_id="standard-json-record-codec-v1", source_applicable=applicable,
            local_name_absence=absence, captured_writes=[document.location(item) for item in writes],
            json_compatible_value_guard_required=True, nonfinite_numbers_become_null=True,
            undefined_functions_symbols_omitted=True, cyclic_bigint_or_toJSON_behavior_not_assumed_away=True,
            completion_guaranteed=False)

    def inspect(self, selector: dict) -> None:
        selected = self.component(selector)
        if selected is None:
            return
        document, definition, function = selected
        body = _field(function, "body")
        parameters = _children(_field(function, "parameters"))
        self.fact("function_parameters", document, definition, function,
            selector=selector, parameters=[{"index": index, "location": document.location(parameter),
                "pattern": document.text(_field(parameter, "pattern") or _field(parameter, "name") or parameter)} for index, parameter in enumerate(parameters)],
            function_kind=function_kind(document, function))
        for node in _walk(body):
            if node.type == "variable_declarator":
                initial = _field(node, "value")
                if initial is not None:
                    value = self.expression(document, definition, initial)
                    binder = _field(node, "name")
                    identity = self.identity(document, binder) if binder.type == "identifier" else {}
                    self.fact("binding_initializer", document, definition, node,
                        declaration_id=identity.get("declaration_id"), pattern=document.text(binder), value_id=value,
                        conditions=list(self.conditions(document, definition, node)), current_value_identity_proven=False)
            elif node.type in {"assignment_expression", "augmented_assignment_expression", "update_expression"}:
                left = _field(node, "left") or _field(node, "argument")
                right = _field(node, "right")
                self.fact("source_write", document, definition, node, target=self.path(document, left),
                    value_id=self.expression(document, definition, right) if right is not None else None,
                    operator=document.text(_field(node, "operator")), conditions=list(self.conditions(document, definition, node)),
                    successful_runtime_write_proven=False)
            elif node.type in {"call_expression", "new_expression"}:
                value = self.expression(document, definition, node)
                self.fact("invocation_site", document, definition, node, value_id=value,
                    conditions=list(self.conditions(document, definition, node)))
            elif node.type == "return_statement":
                values = _children(node)
                self.fact("body_return", document, definition, node,
                    value_id=self.expression(document, definition, values[0]) if values else None,
                    conditions=list(self.conditions(document, definition, node)), fulfilled_value_proven=False)
            elif node.type in {"if_statement", "for_statement", "for_in_statement", "while_statement", "switch_statement"}:
                condition = _field(node, "condition") or _field(node, "right")
                self.fact("decision_region", document, definition, node, node_type=node.type,
                    condition_value_id=self.expression(document, definition, condition) if condition is not None else None,
                    condition_text=document.text(condition) if condition is not None else "",
                    condition_location=document.location(condition) if condition is not None else None,
                    branch_truth_verified=False, conditions=list(self.conditions(document, definition, node)))
        self.message_operations(document, definition, function)

    def message_operations(self, document: Any, definition: Any, function: Any) -> None:
        """Record actual IO operands; path spelling alone never joins records."""
        for node in _walk(_field(function, "body")):
            if node.type != "call_expression":
                continue
            callee = _field(node, "function")
            path = self.path(document, callee)
            name = path["root"] if path and not path["keys"] else path["keys"][-1] if path and path["keys"] else None
            if name not in {"readFile", "writeFile", "rename", "writeJsonAtomic"}:
                continue
            # Builtin names are only discovered candidates. Existing graph or
            # authenticated import binding must identify the actual operation.
            identity = self.identity(document, callee) if callee.type == "identifier" else {}
            imported = identity.get("import") or {}
            node_builtin = imported.get("module") in {"node:fs/promises", "fs/promises", "node:fs", "fs"}
            edge, issues = self.sources.call_binding(node, document, definition)
            arguments = [self.expression(document, definition, child) for child in _children(_field(node, "arguments"))]
            self.fact("record_io_operation", document, definition, node, operation=name,
                arguments=arguments, source_binding=identity, import_model_applicable=node_builtin,
                internal_target=edge.target if edge else None, binding_issues=issues,
                record_identity_joined=False, physical_path_equality_proven=False,
                conditions=list(self.conditions(document, definition, node)))

    def site(self, spec: dict) -> list[dict]:
        selected = self.component(spec["owner"])
        if selected is None:
            return []
        document, definition, function = selected
        result = []
        for node in _walk(_field(function, "body")):
            if node.type != "call_expression" or document.text(_field(node, "function")) != spec["callee"]:
                continue
            arguments = _children(_field(node, "arguments"))
            index = spec["argument_index"]
            if index >= len(arguments) or any(arg.type == "spread_element" for arg in arguments[:index + 1]):
                self.gap("pipeline_selected_actual_argument_unknown", document, node)
                continue
            whole = self.expression(document, definition, arguments[index])
            selected_value = self.project(whole, spec["field_path"], document, definition, arguments[index])
            result.append({"location": document.location(node), "owner": definition.graph_node_id,
                "whole_argument_value_id": whole, "selected_value_id": selected_value,
                "selected_path": spec["field_path"], "conditions": list(self.conditions(document, definition, node)),
                "analysis_phase": "call argument before callee activation"})
        return result

    def reachable_terms(self, value: str) -> list[dict]:
        todo, seen, result = [value], set(), []
        while todo:
            current = todo.pop()
            if current in seen or current not in self.terms:
                continue
            seen.add(current)
            term = self.terms[current]
            result.append(term)
            for key in ("initializer", "source", "receiver", "index", "operand"):
                if isinstance(term.get(key), str):
                    todo.append(term[key])
            todo.extend(item for key in ("values", "operands", "arguments") for item in term.get(key, []) if isinstance(item, str))
            todo.extend(item["value"] for item in term.get("members", []) if "value" in item)
            todo.extend(item["value"] for item in term.get("writes", []))
        return result

    def budget(self, spec: dict) -> dict:
        selected = self.component(spec["owner"])
        if selected is None:
            return {"budget_kind": spec["kind"], "source_complete": False, "gaps": ["budget_owner_source_invalid"]}
        document, definition, function = selected
        reader = self.reader(document)
        selected_bindings = {}
        for node in _walk(_field(function, "body")):
            if node.type == "variable_declarator" and document.text(_field(node, "name")) in {spec["counter"], spec["limit"]}:
                identity = reader.resolve_identity(_field(node, "name"))
                selected_bindings[document.text(_field(node, "name"))] = {"identity": identity,
                    "initializer_value_id": self.expression(document, definition, _field(node, "value")),
                    "location": document.location(node)}
        guards = []
        counter = selected_bindings.get(spec["counter"], {}).get("identity", {}).get("declaration_id")
        limit = selected_bindings.get(spec["limit"], {}).get("identity", {}).get("declaration_id")
        for node in _walk(_field(function, "body"), nested=True):
            if node.type != "binary_expression":
                continue
            left, right = self.path(document, _field(node, "left")), self.path(document, _field(node, "right"))
            if not left or not right or left.get("declaration_id") != counter or right.get("declaration_id") != limit or not counter or not limit:
                continue
            operator = document.text(_field(node, "operator"))
            if operator not in {">", ">=", "<", "<="}:
                continue
            region = next((parent for parent in _ancestors(node.parent) if parent.type in {"if_statement", "for_statement", "while_statement"}), None)
            body = _field(region, "consequence") if region is not None and region.type == "if_statement" else _field(region, "body")
            returns = [item for item in _walk(body) if item.type == "return_statement"]
            lexical_owner = next((parent for parent in _ancestors(node.parent) if parent.type in _FUNCTIONS), function)
            helper_binding = None
            helper_calls = []
            if lexical_owner != function:
                helper_parent = lexical_owner.parent
                binder = _field(helper_parent, "name") if helper_parent is not None and helper_parent.type == "variable_declarator" else _field(lexical_owner, "name")
                helper_binding = reader.resolve_identity(binder) if binder is not None else None
                if helper_binding and helper_binding.get("declaration_id"):
                    for call in _walk(_field(function, "body"), nested=True):
                        callee = _field(call, "function") if call.type == "call_expression" else None
                        if callee is not None and callee.type == "identifier" and reader.same(helper_binding, callee):
                            helper_calls.append({"location": document.location(call), "conditions": list(self.conditions(document, definition, call)),
                                "same_helper_declaration": True, "argument_value_ids": [self.expression(document, definition, child) for child in _children(_field(call, "arguments"))]})
            guards.append({"location": document.location(node), "operator": operator,
                "counter_declaration": counter, "limit_declaration": limit,
                "region_location": document.location(region) if region is not None else None,
                "conditions": list(self.conditions(document, definition, node)),
                "guard_returns": [{"location": document.location(item), "value_id": self.expression(document, definition, _children(item)[0]) if _children(item) else None} for item in returns],
                "lexical_owner_location": document.location(lexical_owner), "nested_helper_binding": helper_binding,
                "actual_same_declaration_helper_calls": helper_calls,
                "nested_helper_connected": lexical_owner == function or bool(helper_calls),
                "whole_function_dominance_proven": False})
        returns = [node for node in _walk(_field(function, "body")) if node.type == "return_statement"]
        first_guard = min((item["location"]["start_byte"] for item in guards), default=function.end_byte)
        early = [{"location": document.location(node), "conditions": list(self.conditions(document, definition, node)),
            "value_id": self.expression(document, definition, _children(node)[0]) if _children(node) else None} for node in returns if node.end_byte < first_guard]
        calls = [node for node in _walk(_field(function, "body")) if node.type == "call_expression"]
        opaque = []
        for node in calls:
            edge, _issues = self.sources.call_binding(node, document, definition)
            if edge is None:
                opaque.append({"location": document.location(node), "callee": document.text(_field(node, "function")),
                    "conditions": list(self.conditions(document, definition, node)), "before_guard": node.start_byte < first_guard,
                    "argument_value_ids": [self.expression(document, definition, child) for child in _children(_field(node, "arguments"))]})
        gap = [] if counter and limit and guards and all(item["nested_helper_connected"] for item in guards) else ["budget_counter_limit_or_guard_not_closed"]
        counter_writes = []
        if counter:
            for write in reader.writes(selected_bindings[spec["counter"]]["identity"]):
                mutation = reader.mutation_for(write)
                if mutation is not None and function.start_byte <= mutation.start_byte < function.end_byte:
                    counter_writes.append({**write, "location": document.location(mutation), "conditions": list(self.conditions(document, definition, mutation)),
                        "source_text": document.text(mutation)})
        return {"budget_kind": spec["kind"], "owner": spec["owner"], "bindings": selected_bindings,
            "decision_guards": guards, "early_returns_before_first_guard": early, "opaque_consumers": opaque,
            "counter_writes": counter_writes,
            "source_complete": not gap, "scope": "actual selected counter/limit guard; preceding returns and opaque consumers separate",
            "runtime_values_or_termination_proven": False, "gaps": gap}

    def producer_connection(self, flags: list[dict], returns: list[dict], sites: list[dict]) -> dict:
        """Close declaration/return/call/property source structure, not numbers."""
        selected = self.component(self.rule["producer"]["owner"])
        if selected is None:
            return {"supported": False, "gaps": ["producer_source_invalid"]}
        _document, definition, _function = selected
        returned_cells = {term.get("declaration_id") for item in returns
            for term in self.reachable_terms(item["selected_value_id"]) if term["kind"] == "binding_sources"}
        writes = [item for branch in flags for item in branch["writes"]
            if item.get("target", {}).get("declaration_id") in returned_cells]
        connected = []
        for site in sites:
            terms = self.reachable_terms(site["selected_value_id"])
            invocations = [term for term in terms if term["kind"] == "invocation" and term.get("target") == definition.graph_node_id]
            selected_term = self.terms[site["selected_value_id"]]
            projected = selected_term["kind"] == "field_projection" and selected_term["path"] == self.rule["producer"]["output_path"]
            connected.append({"site": site["location"], "actual_producer_invocations": invocations,
                "return_field_path_selected": projected, "supported_source_structure": bool(invocations and projected)})
        gaps = []
        if not writes:
            gaps.append("flag_write_does_not_resolve_to_returned_declaration")
        if not connected or not all(item["supported_source_structure"] for item in connected):
            gaps.append("producer_return_to_request_invocation_value_not_connected")
        # The proof does not claim the arbitrary option's numeric meaning,
        # last-loop-iteration value, actual CLI activation or JSON transport.
        return {"supported": not gaps, "gaps": gaps, "flag_writes_to_returned_cells": writes,
            "request_connections": connected, "proof_domain": "captured_declaration_return_invocation_field_source",
            "runtime_value_proven": False, "last_reaching_flag_value_proven": False}

    def dynamic_import_binding(self, document: Any, definition: Any, callee: Any) -> dict:
        """Authenticate a literal dynamic import's actual destructured member."""
        callee = unwrap(callee)
        if callee is None or callee.type != "identifier":
            return {"supported": False, "reason": "dynamic_callee_not_bare_identifier"}
        identity = self.identity(document, callee)
        declaration = self.reader(document).declaration_for(identity)
        initial = unwrap(self.reader(document).initializer_for(identity))
        if initial is not None and initial.type == "await_expression":
            initial = unwrap(_children(initial)[0])
        if declaration is None or initial is None or initial.type != "call_expression" or document.text(_field(initial, "function")) != "import":
            return {"supported": False, "reason": "actual_dynamic_import_initializer_unavailable", "identity": identity}
        args = _children(_field(initial, "arguments"))
        specifier = _literal_string(document.text(args[0])) if len(args) == 1 and args[0].type == "string" else None
        if specifier is None or not specifier.startswith("."):
            return {"supported": False, "reason": "module_path_not_a_fixed_relative_literal", "location": document.location(initial)}
        parameter_path = (identity.get("pattern_path") or [])
        members = [item.get("name") for item in parameter_path if item["kind"] == "object_property"]
        if len(members) != 1 or any(item["kind"] not in {"object_property"} for item in parameter_path):
            return {"supported": False, "reason": "actual_import_member_pattern_unknown", "identity": identity}
        base = posixpath.normpath(posixpath.join(posixpath.dirname(document.source.path), specifier))
        paths = [base, base[:-3] + ".ts"] if base.endswith(".js") else [base, base + ".ts"]
        captured = {source.path for source in self.snapshot.files}
        candidates = [path for path in paths if path in captured]
        if len(candidates) != 1:
            return {"supported": False, "reason": "dynamic_source_entry_not_unique", "candidates": candidates}
        target = self.component({"file": candidates[0], "symbol": members[0]})
        if target is None:
            return {"supported": False, "reason": "dynamic_export_callable_unavailable"}
        reassignments = [write for write in self.reader(document).writes(identity) if write.get("binding_reassignment")]
        return {"supported": not reassignments and "source-derived-module-assembly-v1" in self.rule["models"],
            "location": document.location(initial), "actual_callee_location": document.location(callee),
            "identity": identity, "target_owner": target[1].graph_node_id,
            "target_selector": {"file": candidates[0], "symbol": members[0]},
            "captured_reassignments": reassignments, "module_runtime_available_verified": False,
            "model_id": "source-derived-module-assembly-v1"}

    def imported_selector(self, document: Any, identity: dict, symbol: str | None = None) -> dict | None:
        record = identity.get("import") or {}
        module = record.get("module")
        if not isinstance(module, str) or not module.startswith(".") or record.get("type_only"):
            return None
        base = posixpath.normpath(posixpath.join(posixpath.dirname(document.source.path), module))
        options = [base, base[:-3] + ".ts"] if base.endswith(".js") else [base, base + ".ts"]
        captured = {source.path for source in self.snapshot.files if source.status == "parsed"}
        options = [path for path in options if path in captured]
        imported = symbol or record.get("imported_name")
        if len(options) != 1 or not isinstance(imported, str) or imported in {"*", "default"}:
            return None
        return {"file": options[0], "symbol": imported}

    def nominal_receiver(self, document: Any, definition: Any, node: Any, depth: int = 0) -> list[dict]:
        """Discover actual constructor/alias/field sources, preserving variants."""
        node = unwrap(node)
        if node is None or depth > _MAX_DEPTH:
            return []
        marker = (document.source.path, node.id)
        if marker in self.nominal_memo:
            return self.nominal_memo[marker]
        if marker in self.nominal_active:
            return []
        self.nominal_active.add(marker)
        result = []
        try:
            if node.type == "new_expression":
                constructor = _field(node, "constructor")
                identity = self.identity(document, constructor) if constructor is not None and constructor.type == "identifier" else {}
                imported = self.imported_selector(document, identity)
                if imported is not None:
                    target_doc, target_definition, problems = self.sources.select({"file": imported["file"], "symbol": imported["symbol"] + ".constructor"})
                    if target_doc is not None and target_definition is not None:
                        result.append({"class_selector": imported, "allocation_location": document.location(node),
                            "constructor_graph_id": target_definition.graph_node_id, "constructor_identity": identity,
                            "arguments": [self.expression(document, definition, child) for child in _children(_field(node, "arguments"))],
                            "conditions": list(self.conditions(document, definition, node)), "source_supported": True})
                if not result:
                    result.append({"unknown_receiver": True, "location": document.location(node), "source_supported": False,
                        "reason": "constructor_source_not_resolved", "constructor_identity": identity})
            elif node.type in {"identifier", "shorthand_property_identifier"}:
                identity = self.identity(document, node)
                initial = self.reader(document).initializer_for(identity)
                if initial is not None:
                    result.extend(self.nominal_receiver(document, definition, initial, depth + 1))
                for write in self.reader(document).writes(identity):
                    mutation = self.reader(document).mutation_for(write)
                    if mutation is not None and write.get("binding_reassignment") and mutation.type == "assignment_expression" and mutation.start_byte < node.start_byte:
                        result.extend(self.nominal_receiver(document, definition, _field(mutation, "right"), depth + 1))
                if identity.get("declaration_kind") == "parameter":
                    declaration = self.reader(document).declaration_for(identity)
                    owner_function = next((parent for parent in _ancestors(declaration) if parent.type in _FUNCTIONS), None)
                    cls = next((parent for parent in _ancestors(owner_function) if parent.type in {"class", "class_declaration"}), None)
                    if cls is not None and document.text(_field(owner_function, "name")) == "constructor":
                        expected = {"file": document.source.path, "symbol": document.text(_field(cls, "name"))}
                        for allocation_doc, allocation_def, allocation in self.allocation_sources(expected):
                            arguments = _children(_field(allocation, "arguments"))
                            index = identity.get("parameter_index")
                            actual = arguments[index] if isinstance(index, int) and index < len(arguments) else None
                            for part in (identity.get("pattern_path") or []):
                                if part["kind"] == "object_property" and actual is not None and actual.type == "object":
                                    matches = [child for child in _children(actual) if child.type == "pair" and self.key(allocation_doc, _field(child, "key")) == part.get("name")]
                                    actual = _field(matches[-1], "value") if len(matches) == 1 and not any(child.type == "spread_element" for child in _children(actual)) else None
                                elif part["kind"] not in {"parameter", "default_value"}:
                                    actual = None
                            if actual is not None:
                                for variant in self.nominal_receiver(allocation_doc, allocation_def, actual, depth + 1):
                                    result.append({**variant, "constructor_injection_location": allocation_doc.location(allocation),
                                        "formal_declaration_id": identity.get("declaration_id"), "actual_argument_location": allocation_doc.location(actual),
                                        "scope": "actual captured allocation and normal constructor injection; arbitrary external instances separate"})
                if not result:
                    result.append({"unknown_receiver": True, "location": document.location(node), "source_supported": False,
                        "reason": "receiver_binding_source_not_resolved", "identity": identity})
            elif node.type == "ternary_expression":
                for branch in ("consequence", "alternative"):
                    result.extend(self.nominal_receiver(document, definition, _field(node, branch), depth + 1))
            elif node.type == "binary_expression" and document.text(_field(node, "operator")) in {"||", "??"}:
                for branch in ("left", "right"):
                    result.extend(self.nominal_receiver(document, definition, _field(node, branch), depth + 1))
            elif node.type == "this":
                cls = next((parent for parent in _ancestors(node) if parent.type in {"class_declaration", "class"}), None)
                if cls is not None:
                    result.append({"class_selector": {"file": document.source.path, "symbol": document.text(_field(cls, "name"))},
                        "receiver_location": document.location(node), "source_supported": True,
                        "scope": "actual method receiver in its captured class; external subclass/field override variants separate"})
            elif node.type == "member_expression" and unwrap(_field(node, "object")).type == "this":
                member = self.key(document, _field(node, "property"))
                cls = next((parent for parent in _ancestors(node) if parent.type in {"class_declaration", "class"}), None)
                if cls is not None:
                    cache_key = (document.source.path, cls.id)
                    if cache_key not in self.field_write_cache:
                        self.field_write_cache[cache_key] = [candidate for candidate in _walk(cls, nested=True) if candidate.type == "assignment_expression"]
                    assignments = [candidate for candidate in self.field_write_cache[cache_key]
                        if (self.path(document, _field(candidate, "left")) or {}).get("root") == "this"
                        and (self.path(document, _field(candidate, "left")) or {}).get("keys") == [member]]
                    for assignment in assignments:
                        actual_owner = document.definition_nodes.get(document.call_owner(assignment), [])
                        owner = actual_owner[0] if len(actual_owner) == 1 else definition
                        alternatives = self.nominal_receiver(document, owner, _field(assignment, "right"), depth + 1)
                        for alternative in alternatives:
                            result.append({**alternative, "receiver_field": member, "field_assignment_location": document.location(assignment),
                                "all_captured_field_writes": [document.location(item) for item in assignments]})
        finally:
            self.nominal_active.discard(marker)
        # Null/false alternatives are absent receivers, retained at the actual
        # branch predicate; they are never invented as a method implementation.
        if not result and node.type not in {"null", "false", "undefined"}:
            result.append({"unknown_receiver": True, "location": document.location(node), "source_supported": False,
                "reason": "receiver_expression_not_supported", "node_type": node.type})
        values = list({_digest(item): item for item in result}.values())
        self.nominal_memo[marker] = values
        return values

    def allocation_sources(self, selector: dict) -> list[tuple[Any, Any, Any]]:
        for document, definition, function in list(self.components.values()):
            marker = (document.source.path, function.id)
            if marker in self.allocation_scanned:
                continue
            self.allocation_scanned.add(marker)
            for node in _walk(_field(function, "body"), nested=True):
                if node.type != "new_expression":
                    continue
                constructor = _field(node, "constructor")
                identity = self.identity(document, constructor) if constructor is not None and constructor.type == "identifier" else {}
                actual = self.imported_selector(document, identity)
                if actual is not None:
                    self.allocation_index.setdefault(_digest(actual), []).append((document, definition, node))
        return self.allocation_index.get(_digest(selector), [])

    def nominal_call_binding(self, document: Any, definition: Any, node: Any) -> dict:
        callee = unwrap(_field(node, "function"))
        if callee is None or callee.type != "member_expression":
            return {"supported": False, "targets": [], "gaps": ["callee_not_nominal_member"]}
        method = self.key(document, _field(callee, "property"))
        receivers = self.nominal_receiver(document, definition, _field(callee, "object"))
        targets = []
        for receiver in receivers:
            if receiver.get("unknown_receiver"):
                continue
            selector = {"file": receiver["class_selector"]["file"], "symbol": receiver["class_selector"]["symbol"] + "." + str(method)}
            target_doc, target_definition, _issues = self.sources.select(selector)
            selected = (target_doc, target_definition, _fn(target_definition)) if target_doc is not None and target_definition is not None and _fn(target_definition) is not None else None
            if selected is not None:
                self.documents[target_doc.source.path] = target_doc
                targets.append({"selector": selector, "target_graph_id": selected[1].graph_node_id,
                    "receiver_source": receiver, "source_supported": True})
        return {"supported": bool(targets) and "source-derived-module-assembly-v1" in self.rule["models"],
            "targets": targets, "gaps": [] if targets else ["actual_nominal_receiver_method_source_unknown"],
            "unresolved_receiver_variants": [item for item in receivers if item.get("unknown_receiver")],
            "all_captured_receiver_variants_resolved": bool(receivers) and len(targets) == len(receivers),
            "creates_CALLS_edge": False, "actual_runtime_dispatch_verified": False}

    def source_modes(self, sites: list[dict]) -> dict:
        """Classify actual selected-site skip and record reuse branches."""
        skipped, reuse, receiver_variants = [], [], []
        selected = self.component(self.rule["worker"]["owner"])
        if selected is not None:
            document, definition, function = selected
            for node in _walk(_field(function, "body")):
                if node.type != "call_expression" or document.text(_field(node, "function")) != self.rule["worker"]["callee"]:
                    continue
                child = node
                for parent in _ancestors(node.parent):
                    if parent == function:
                        break
                    if parent.type == "if_statement" and _field(parent, "alternative") == child:
                        condition = _field(parent, "condition")
                        other = _field(parent, "consequence")
                        occurrences = [item for item in _walk(other) if item.type in {"identifier", "shorthand_property_identifier"} and document.text(item) == self.rule["worker"]["callee"]]
                        skipped.append({"predicate": document.location(condition), "condition_value_id": self.expression(document, definition, condition),
                            "selected_call_is_else_branch": True, "then_has_selected_callable_occurrence": bool(occurrences),
                            "supported_selected_site_skip": not occurrences, "scope": "selected explicit source site, not arbitrary global activation"})
                    child = parent
            for node in _walk(_field(function, "body")):
                if node.type == "variable_declarator":
                    value = _field(node, "value")
                    if value is not None and value.type == "ternary_expression":
                        candidates = self.nominal_receiver(document, definition, value)
                        if candidates:
                            receiver_variants.append({"location": document.location(node), "variants": candidates,
                                "condition": document.location(_field(value, "condition")), "false_value": document.text(_field(value, "alternative"))})
        for document, definition, function in list(self.components.values()):
            for node in _walk(_field(function, "body"), nested=True):
                if node.type != "if_statement":
                    continue
                condition = unwrap(_field(node, "condition"))
                body = _field(node, "consequence")
                returns = [item for item in _walk(body) if item.type == "return_statement" and _children(item)]
                if condition is None or condition.type != "identifier":
                    continue
                identity = self.identity(document, condition)
                for returned in returns:
                    expression = unwrap(_children(returned)[0])
                    if expression.type == "identifier" and identity.get("state") == "unique" and identity.get("declaration_id") == self.identity(document, expression).get("declaration_id"):
                        initial = unwrap(self.reader(document).initializer_for(identity))
                        if initial is not None:
                            reuse.append({"owner": definition.graph_node_id, "location": document.location(returned),
                                "condition": document.location(condition), "declaration_id": identity.get("declaration_id"),
                                "prior_value_source": self.expression(document, definition, initial),
                                "returns_existing_current_value": True, "fresh_request_identity_proven": False})
        return {"selected_skip_branches": skipped, "existing_return_branches": reuse,
            "conditional_constructor_variants": receiver_variants,
            "source_classification_complete": bool(skipped and reuse),
            "runtime_scope": "actual selected call skip/current existing record return, constructor alternatives; no guaranteed execution"}

    def source_target(self, document: Any, definition: Any, node: Any) -> tuple[Any, Any, Any] | None:
        """Resolve a real call using graph/import/registered construction evidence."""
        owners = document.definition_nodes.get(document.call_owner(node), [])
        definition = owners[0] if len(owners) == 1 else definition
        edge, _issues = self.sources.call_binding(node, document, definition)
        if edge is not None:
            matches = self.sources.nodes.get(edge.target, [])
            target_doc, target_def, _issues = self.sources.definition_for_node(matches[0]) if len(matches) == 1 else (None, None, [])
            if target_doc is not None and _fn(target_def) is not None:
                return target_doc, target_def, _fn(target_def)
        callee = unwrap(_field(node, "function"))
        if callee is not None and callee.type == "identifier":
            selector = self.imported_selector(document, self.identity(document, callee))
            if selector is not None:
                target_doc, target_def, _issues = self.sources.select(selector)
                if target_doc is not None and _fn(target_def) is not None:
                    return target_doc, target_def, _fn(target_def)
            dynamic = self.dynamic_import_binding(document, definition, callee)
            if dynamic.get("supported"):
                return self.component(dynamic["target_selector"])
        elif callee is not None and callee.type == "member_expression":
            nominal = self.nominal_call_binding(document, definition, node)
            selectors = {_digest(item["selector"]): item["selector"] for item in nominal.get("targets", [])}
            if nominal.get("all_captured_receiver_variants_resolved") and len(selectors) == 1:
                target_doc, target_def, _issues = self.sources.select(next(iter(selectors.values())))
                if target_doc is not None and _fn(target_def) is not None:
                    return target_doc, target_def, _fn(target_def)
        return None

    def return_slot_relation(self, document: Any, definition: Any, function: Any, parameter_index: int, keys: list[str]) -> dict:
        """A conditional theorem for the CURRENT own data slot, never old IR state.

        This finite record model understands aliases, guarded record defaults,
        ordered literal copies, and plain returned parameters. Captured writes
        to the selected slot and unanalysed whole-record consumers are barriers.
        """
        reader = self.reader(document)
        cache_key = (document.source.path, function.start_byte, parameter_index, tuple(keys))
        if cache_key in self.slot_return_cache:
            return self.slot_return_cache[cache_key]
        formal_ids = set()
        for identifier in _walk(_field(function, "parameters"), nested=True):
            if identifier.type not in {"identifier", "shorthand_property_identifier_pattern"}:
                continue
            identity = reader.resolve_identity(identifier)
            if identity.get("declaration_kind") == "parameter" and identity.get("parameter_index") == parameter_index:
                formal_ids.add(identity.get("declaration_id"))
        active = set()
        def relative(node: Any, selected: list[str], depth: int = 0) -> dict:
            node = unwrap(node)
            if node is None or depth > _MAX_DEPTH or (node.id, tuple(selected)) in active:
                return {"supported": False, "reason": "record_return_relation_budget_or_cycle"}
            marker = (node.id, tuple(selected)); active.add(marker)
            try:
                if node.type in {"identifier", "shorthand_property_identifier"}:
                    identity = reader.resolve_identity(node)
                    if identity.get("declaration_id") in formal_ids:
                        pattern = [part.get("name") for part in (identity.get("pattern_path") or []) if part["kind"] == "object_property"]
                        return {"supported": pattern + selected == keys, "source": "current_formal_slot", "declaration_id": identity["declaration_id"],
                            "path": pattern + selected, "location": document.location(node), "presence_condition": "selected own enumerable data field exists at the read/copy boundary"}
                    initial = reader.initializer_for(identity)
                    if initial is not None and not any(write.get("binding_reassignment") for write in reader.writes(identity)):
                        return relative(initial, selected, depth + 1)
                if node.type in {"member_expression", "subscript_expression"}:
                    key = self.key(document, _field(node, "property") if node.type == "member_expression" else _field(node, "index"))
                    if key is not None:
                        return relative(_field(node, "object"), [key, *selected], depth + 1)
                if node.type == "object" and selected:
                    surface = _children(node)
                    if any(child.type not in {"pair", "shorthand_property_identifier", "spread_element"} for child in surface):
                        return {"supported": False, "reason": "unsupported_literal_surface", "location": document.location(node)}
                    suffix = []
                    for member in reversed(surface):
                        if member.type == "spread_element":
                            relation = relative(_children(member)[0], selected, depth + 1)
                            if relation.get("supported"):
                                return {"supported": True, "source": "ordered_current_data_copy", "location": document.location(member),
                                    "selected_path": selected, "source_relation": relation, "later_fixed_keys": list(reversed(suffix)),
                                    "model_id": "ordinary-record-tree-flow-v1", "conditional_presence": True,
                                    "source_entry_origin_or_old_heap_projection_upgraded": False}
                            # A later unknown spread can overwrite the slot. A
                            # known plain literal absent at the path can be skipped.
                            spread_value = unwrap(_children(member)[0])
                            if spread_value.type != "object" or not self.literal_absent(document, spread_value, selected):
                                return {"supported": False, "reason": "later_spread_selected_value_unknown", "relation": relation, "location": document.location(member)}
                        else:
                            key = self.key(document, _field(member, "key") if member.type == "pair" else member)
                            if key is None or key == "__proto__":
                                return {"supported": False, "reason": "literal_computed_or_prototype_key", "location": document.location(member)}
                            suffix.append(key)
                            if key == selected[0]:
                                return relative(_field(member, "value") if member.type == "pair" else member, selected[1:], depth + 1)
                if node.type == "ternary_expression":
                    alternatives = [relative(_field(node, branch), selected, depth + 1) for branch in ("consequence", "alternative")]
                    supported = [item for item in alternatives if item.get("supported")]
                    empty = [self.literal_absent(document, unwrap(_field(node, branch)), selected) for branch in ("consequence", "alternative")]
                    # Guarded fallback is not an unconditional presence theorem.
                    return {"supported": bool(supported) and all(item.get("supported") or absent for item, absent in zip(alternatives, empty)),
                        "source": "guarded_input_or_empty_record", "branches": alternatives, "empty_branches": empty,
                        "condition_location": document.location(_field(node, "condition")), "conditional_presence": True}
                if node.type == "binary_expression" and document.text(_field(node, "operator")) in {"||", "??"}:
                    left, right = relative(_field(node, "left"), selected, depth + 1), relative(_field(node, "right"), selected, depth + 1)
                    return {"supported": left.get("supported", False) and (right.get("supported", False) or self.literal_absent(document, unwrap(_field(node, "right")), selected)),
                        "source": "current_truthy_or_nullish_record_fallback", "input": left, "fallback": right,
                        "conditional_presence": True, "location": document.location(node)}
                return {"supported": False, "reason": "return_selected_slot_not_formal_copy", "node_type": node.type, "location": document.location(node)}
            finally:
                active.discard(marker)
        returns = [node for node in _walk(_field(function, "body")) if node.type == "return_statement" and _children(node)]
        relations = [{"location": document.location(node), "conditions": list(self.conditions(document, definition, node)),
            "relation": relative(_children(node)[0], keys)} for node in returns]
        aliases = set(formal_ids)
        for _round in range(_MAX_DEPTH):
            previous = set(aliases)
            for declaration in _walk(_field(function, "body"), nested=True):
                if declaration.type != "variable_declarator":
                    continue
                binder, initial = _field(declaration, "name"), unwrap(_field(declaration, "value"))
                path = self.path(document, initial)
                if binder is not None and binder.type == "identifier" and path and path.get("declaration_id") in aliases and not path["keys"]:
                    aliases.add(reader.resolve_identity(binder).get("declaration_id"))
            if previous == aliases:
                break
        mutations, opaque = [], []
        for node in _walk(_field(function, "body"), nested=True):
            if node.type not in {"assignment_expression", "augmented_assignment_expression", "update_expression"}:
                continue
            target = self.path(document, _field(node, "left") or _field(node, "argument"))
            if target and target.get("declaration_id") in aliases and (not target["static"] or keys[:len(target["keys"])] == target["keys"]):
                mutations.append({"location": document.location(node), "target": target})
        for call in _walk(_field(function, "body"), nested=True):
            if call.type != "call_expression":
                continue
            relevant = []
            for argument in _children(_field(call, "arguments")):
                path = self.path(document, argument)
                if path and path.get("declaration_id") in aliases and (not path["static"] or keys[:len(path["keys"])] == path["keys"]):
                    relevant.append(document.location(argument))
            if relevant and self.source_target(document, definition, call) is None:
                opaque.append({"location": document.location(call), "callee": document.text(_field(call, "function")), "selected_record_arguments": relevant})
        structure_supported = bool(relations) and all(item["relation"].get("supported") for item in relations)
        effect_audit = self.selected_effect_audit(document, definition, function, parameter_index, keys) if structure_supported else {"supported": False, "barriers": [{"code": "return_relation_not_supported"}], "source_effect_dependencies": []}
        result = {"supported": structure_supported and not mutations and effect_audit["supported"],
            "owner": definition.graph_node_id, "parameter_index": parameter_index, "selected_path": keys,
            "normal_return_relations": relations, "selected_slot_mutation_barriers": mutations,
            "opaque_whole_selected_record_consumers": opaque,
            "transitive_selected_slot_effect_audit": effect_audit,
            "model_id": "ordinary-record-tree-flow-v1", "proof_domain": "current own data slot of normal record inputs",
            "old_semantic_ir_domain_upgraded": False, "runtime_verified": False}
        self.slot_return_cache[cache_key] = result
        return result

    def selected_effect_audit(self, document: Any, definition: Any, function: Any, parameter_index: int, keys: list[str], seen: frozenset = frozenset(), depth: int = 0) -> dict:
        marker = (document.source.path, function.start_byte, parameter_index, tuple(keys))
        if marker in seen or depth >= _MAX_DEPTH:
            return {"supported": False, "barriers": [{"code": "record_effect_audit_cycle_or_budget"}]}
        reader = self.reader(document)
        alias_paths = {}
        for identifier in _walk(_field(function, "parameters"), nested=True):
            if identifier.type not in {"identifier", "shorthand_property_identifier_pattern"}:
                continue
            identity = reader.resolve_identity(identifier)
            if identity.get("declaration_kind") == "parameter" and identity.get("parameter_index") == parameter_index:
                alias_paths[identity.get("declaration_id")] = [part.get("name") for part in (identity.get("pattern_path") or []) if part["kind"] == "object_property"]
        nodes = list(_walk(_field(function, "body"), nested=True))
        for _round in range(_MAX_DEPTH):
            old = dict(alias_paths)
            for declaration in nodes:
                if declaration.type != "variable_declarator":
                    continue
                binder, initial = _field(declaration, "name"), unwrap(_field(declaration, "value"))
                path = self.path(document, initial)
                if binder is not None and binder.type == "identifier" and path and path.get("declaration_id") in alias_paths and path["static"]:
                    alias_paths[reader.resolve_identity(binder).get("declaration_id")] = alias_paths[path["declaration_id"]] + path["keys"]
            if old == alias_paths:
                break
        barriers, dependencies = [], []
        def relative(node: Any) -> list[str] | None:
            path = self.path(document, node)
            if path and path.get("declaration_id") in alias_paths:
                return alias_paths[path["declaration_id"]] + path["keys"] if path["static"] else [None]
            return None
        for node in nodes:
            if node.type in {"assignment_expression", "augmented_assignment_expression", "update_expression"}:
                path = relative(_field(node, "left") or _field(node, "argument"))
                if path is not None and (None in path or keys[:len(path)] == path):
                    # Bare binder reassignment does not write the referenced
                    # record, but makes source provenance uncertain.
                    barriers.append({"code": "selected_record_or_slot_write", "location": document.location(node), "relative_path": path})
            if node.type != "call_expression":
                continue
            relevant = [(index, argument, relative(argument)) for index, argument in enumerate(_children(_field(node, "arguments")))]
            relevant = [(index, argument, path) for index, argument, path in relevant if path is not None and (None in path or keys[:len(path)] == path)]
            if not relevant:
                continue
            target = self.source_target(document, definition, node)
            callee = self.path(document, _field(node, "function"))
            builtin_read = bool(callee and callee["root"] in {"Object", "Array"} and callee["keys"] in (["keys"], ["values"], ["entries"], ["isArray"]) and
                self.reader(document).unbound(callee["root"], _field(node, "function")).get("unbound"))
            if builtin_read:
                dependencies.append({"location": document.location(node), "kind": "normal_data_builtin_read", "model_id": "ordinary-record-tree-flow-v1"})
            elif target is not None:
                for index, argument, path in relevant:
                    relation = self.selected_effect_audit(*target, index, keys[len(path):], seen | {marker}, depth + 1) if None not in path else {"supported": False, "barriers": [{"code": "dynamic_reachable_record_path"}]}
                    dependencies.append({"location": document.location(node), "target": target[1].graph_node_id, "argument_index": index, "effect_relation": relation})
                    if not relation["supported"]:
                        barriers.append({"code": "callee_selected_record_effect_unclosed", "location": document.location(node), "target": target[1].graph_node_id})
            else:
                barriers.append({"code": "opaque_reachable_record_consumer", "location": document.location(node), "callee": document.text(_field(node, "function"))})
        return {"supported": not barriers, "barriers": barriers, "source_effect_dependencies": dependencies,
            "model_id": "ordinary-record-tree-flow-v1", "scope": "actual selected input record aliases and reachable selected-path arguments; sibling data trees disjoint"}

    def literal_absent(self, document: Any, node: Any, keys: list[str]) -> bool:
        if node is None or node.type != "object" or not keys:
            return False
        for child in _children(node):
            if child.type not in {"pair", "shorthand_property_identifier"}:
                return False
            key = self.key(document, _field(child, "key") if child.type == "pair" else child)
            if key is None or key == "__proto__":
                return False
            if key == keys[0]:
                return self.literal_absent(document, unwrap(_field(child, "value")), keys[1:]) if len(keys) > 1 else False
        return True

    def record_field_relations(self) -> dict:
        """Extract selected-root construction/copy/update relations from AST."""
        root_keys = self.rule["request"]["field_path"]
        root, leaf = root_keys[0], root_keys[-1]
        constructions, updates, calls, arrays, callbacks, helper_relations = [], [], [], [], [], []
        for document, definition, function in list(self.components.values()):
            for node in _walk(_field(function, "body"), nested=True):
                if node.type == "object":
                    pairs = [child for child in _children(node) if child.type == "pair" and self.key(document, _field(child, "key")) == root]
                    for pair in pairs:
                        source = _field(pair, "value")
                        value = self.expression(document, definition, source)
                        selected = self.project(value, root_keys[1:], document, definition, source)
                        record = {"location": document.location(pair), "owner": document.call_owner(pair), "source_value_id": value,
                            "selected_value_id": selected, "source_expression": document.text(source), "source_path": self.path(document, source),
                            "ordered_record_members": self.terms[self.expression(document, definition, node)].get("members", []),
                            "normal_data_model": "ordinary-record-tree-flow-v1", "current_value_relation": True,
                            "fresh_entry_origin_proven": False}
                        constructions.append(record)
                if node.type in {"assignment_expression", "augmented_assignment_expression", "update_expression"}:
                    target = self.path(document, _field(node, "left") or _field(node, "argument"))
                    if target and root in target["keys"]:
                        right = unwrap(_field(node, "right"))
                        suffix = target["keys"][target["keys"].index(root) + 1:]
                        same_selected_slot = not target["static"] or not suffix or suffix == root_keys[1:] or suffix == [leaf]
                        source = self.expression(document, definition, right) if right is not None else None
                        fixed = []
                        spreads = []
                        if right is not None and right.type == "object":
                            for child in _children(right):
                                if child.type == "spread_element":
                                    spreads.append({"location": document.location(child), "source_value_id": self.expression(document, definition, _children(child)[0]),
                                        "source_expression": document.text(_children(child)[0]), "source_path": self.path(document, _children(child)[0])})
                                elif child.type in {"pair", "shorthand_property_identifier"}:
                                    fixed.append(self.key(document, _field(child, "key") if child.type == "pair" else child))
                        selected_override = same_selected_slot and suffix and suffix[-1] == leaf
                        copy_surface = bool(spreads) and all(key is not None and key != "__proto__" and key != leaf for key in fixed)
                        updates.append({"location": document.location(node), "owner": document.call_owner(node), "target": target,
                            "source_value_id": source, "source_expression": document.text(right) if right is not None else "", "fixed_keys": fixed,
                            "spreads": spreads, "selected_slot_explicit_override": bool(selected_override),
                            "ordered_current_copy_relation": copy_surface, "disjoint_child_write": bool(suffix and suffix[0] != root_keys[1]),
                            "conditions": list(self.conditions(document, definition, node)), "source_entry_origin_proven": False})
                if node.type != "call_expression":
                    continue
                callee, arguments = unwrap(_field(node, "function")), _children(_field(node, "arguments"))
                relevant_arguments = []
                for index, argument in enumerate(arguments):
                    path = self.path(document, argument)
                    if not path:
                        continue
                    pattern = [part.get("name") for part in (path.get("identity", {}).get("pattern_path") or []) if part["kind"] == "object_property"]
                    initial = self.reader(document).initializer_for(self.identity(document, argument)) if argument.type in {"identifier", "shorthand_property_identifier"} else None
                    rooted_alias = bool(initial is not None and any((self.path(document, item) or {}).get("keys", [])[-1:] == [root] for item in _walk(initial) if item.type in {"member_expression", "subscript_expression"}))
                    if root in path["keys"] or root in pattern or rooted_alias:
                        relevant_arguments.append((index, argument, path, bool(path["keys"][-1:] == [root] or pattern[-1:] == [root] or rooted_alias)))
                target = self.source_target(document, definition, node) if relevant_arguments else None
                if target is not None:
                    target_doc, target_def, target_fn = target
                    for index, argument, path, is_root_child in relevant_arguments:
                        if not path["keys"] or path["keys"][-1] == root:
                            relation = self.return_slot_relation(target_doc, target_def, target_fn, index,
                                root_keys[1:] if is_root_child else root_keys)
                            if relation["supported"]:
                                helper_relations.append({"call_location": document.location(node), "actual_argument_location": document.location(argument),
                                    "actual_argument_value_id": self.expression(document, definition, argument), "target": target_def.graph_node_id,
                                    "actual_source_binding": True, "return_relation": relation})
                if callee is not None and callee.type == "member_expression":
                    method = self.key(document, _field(callee, "property"))
                    if method in {"filter", "slice", "sort", "find", "map", "push"}:
                        arrays.append({"location": document.location(node), "owner": document.call_owner(node), "method": method,
                            "receiver_value_id": self.expression(document, definition, _field(callee, "object")),
                            "argument_value_ids": [self.expression(document, definition, arg) for arg in arguments],
                            "member_identity_relation": "same element references on normal array" if method != "map" else "actual callback return determines element source",
                            "model_id": "ordinary-record-tree-flow-v1", "callback_mutations_not_ignored": True})
                path = self.path(document, callee)
                if path and not path["keys"] and path.get("identity", {}).get("declaration_kind") == "parameter":
                    callbacks.append({"location": document.location(node), "owner": document.call_owner(node), "formal_declaration_id": path["declaration_id"],
                        "formal_index": path["identity"]["parameter_index"], "argument_value_ids": [self.expression(document, definition, arg) for arg in arguments],
                        "normal_callback_model": "normal-async-callback-transfer-v1", "actual_callback_invocation": True})
                if target is not None:
                    calls.append({"location": document.location(node), "owner": document.call_owner(node), "target": target[1].graph_node_id,
                        "argument_value_ids": [self.expression(document, definition, arg) for arg in arguments], "actual_parameter_argument_mapping_available": True})
        return {"constructions": constructions, "field_updates": updates, "actual_source_calls": calls,
            "normal_array_relations": arrays, "actual_callback_invocations": callbacks, "parameter_return_slot_relations": helper_relations,
            "selected_path": root_keys, "model_id": "ordinary-record-tree-flow-v1", "old_ir_projections_recovered": False,
            "proof_scope": "normal plain literal/decoded record current fields; actual branch identities and serialization channels separate"}

    def receiver_assembly(self) -> dict:
        records = []
        for document, definition, function in list(self.components.values()):
            for node in _walk(_field(function, "body")):
                if node.type != "call_expression":
                    continue
                callee = unwrap(_field(node, "function"))
                if callee is None or callee.type != "member_expression":
                    continue
                binding = self.nominal_call_binding(document, definition, node)
                if binding["supported"]:
                    records.append({"location": document.location(node), "owner": definition.graph_node_id,
                        "actual_receiver_binding": binding, "argument_value_ids": [self.expression(document, definition, child) for child in _children(_field(node, "arguments"))]})
        return {"source_receiver_calls": records, "all_default_assemblies_connected": False,
            "gaps": ["default_dynamic_path_import_and_process_record_activation_still_require_source_connection"]}

    def path_expression(self, document: Any, definition: Any, node: Any, *, actuals: dict | None = None, selected_file: str = "", depth: int = 0, seen: frozenset = frozenset()) -> list[dict]:
        """Finite source path algebra; environment alternatives stay separate."""
        node = unwrap(node)
        if node is None or depth >= _MAX_DEPTH or (document.source.path, node.id) in seen:
            return [{"kind": "unknown", "reason": "path_source_or_budget"}]
        visited = seen | {(document.source.path, node.id)}
        location = document.location(node)
        if node.type == "string":
            value = _literal_string(document.text(node))
            return [{"kind": "literal", "path": value, "location": location}] if value is not None else [{"kind": "unknown", "location": location}]
        if node.type == "await_expression":
            return self.path_expression(document, definition, _children(node)[0], actuals=actuals, selected_file=selected_file, depth=depth + 1, seen=visited)
        if node.type in {"identifier", "shorthand_property_identifier"}:
            identity = self.identity(document, node)
            if actuals and identity.get("declaration_id") in actuals:
                actual_document, actual_definition, actual_node = actuals[identity["declaration_id"]]
                values = self.path_expression(actual_document, actual_definition, actual_node, selected_file=selected_file, depth=depth + 1, seen=visited)
                return [{**value, "actual_formal_relation": {"formal_declaration_id": identity["declaration_id"], "actual_location": actual_document.location(actual_node)}} for value in values]
            initial = self.reader(document).initializer_for(identity)
            if initial is not None and not any(write.get("binding_reassignment") for write in self.reader(document).writes(identity)):
                return self.path_expression(document, definition, initial, actuals=actuals, selected_file=selected_file, depth=depth + 1, seen=visited)
            return [{"kind": "formal" if identity.get("declaration_kind") == "parameter" else "unknown", "identity": identity, "location": location}]
        if node.type == "binary_expression" and document.text(_field(node, "operator")) in {"||", "??"}:
            values = []
            for branch in ("left", "right"):
                values.extend({**item, "fallback_branch": branch, "fallback_location": location} for item in self.path_expression(document, definition, _field(node, branch), actuals=actuals, selected_file=selected_file, depth=depth + 1, seen=visited))
            return values
        if node.type == "ternary_expression":
            values = []
            for branch in ("consequence", "alternative"):
                values.extend({**item, "conditional_branch": branch, "condition_location": document.location(_field(node, "condition"))} for item in self.path_expression(document, definition, _field(node, branch), actuals=actuals, selected_file=selected_file, depth=depth + 1, seen=visited))
            return values
        if node.type == "subscript_expression":
            receiver, index = unwrap(_field(node, "object")), unwrap(_field(node, "index"))
            identity = self.identity(document, receiver) if receiver is not None and receiver.type == "identifier" else {}
            initial = unwrap(self.reader(document).initializer_for(identity))
            if initial is not None and initial.type == "object" and not any(write.get("binding_reassignment") or write.get("property_write") for write in self.reader(document).writes(identity)):
                values = []
                for pair in _children(initial):
                    if pair.type != "pair" or self.key(document, _field(pair, "key")) is None:
                        return [{"kind": "unknown", "reason": "nonfinite_dynamic_import_table", "location": document.location(initial)}]
                    value = unwrap(_field(pair, "value"))
                    literal = _literal_string(document.text(value)) if value is not None and value.type == "string" else None
                    if literal is None:
                        return [{"kind": "unknown", "reason": "nonliteral_dynamic_import_table_value", "location": document.location(pair)}]
                    values.append({"kind": "literal", "path": literal, "location": document.location(value),
                        "finite_table_declaration_id": identity.get("declaration_id"), "selected_table_key": self.key(document, _field(pair, "key")),
                        "actual_index_value_id": self.expression(document, definition, index), "table_mutations": self.reader(document).writes(identity)})
                return values
        path = self.path(document, node)
        if path and path["root"] == "process" and path["keys"] and path["keys"][0] == "env":
            return [{"kind": "environment_override", "source_path": path, "location": location}]
        if node.type == "call_expression":
            callee = unwrap(_field(node, "function"))
            arguments = _children(_field(node, "arguments"))
            identity = self.identity(document, callee) if callee is not None and callee.type == "identifier" else {}
            imported_record = identity.get("import") or {}
            if imported_record.get("module") in {"node:url", "url"} and imported_record.get("imported_name") == "fileURLToPath" and len(arguments) == 1 and document.text(arguments[0]) == "import.meta.url":
                return [{"kind": "captured_path", "path": document.source.path, "location": location,
                    "source_module_url_model": "source-derived-module-assembly-v1", "compiled_js_to_captured_ts_correspondence": True}]
            if callee is not None and callee.type == "member_expression":
                root = unwrap(_field(callee, "object")); method = self.key(document, _field(callee, "property"))
                root_identity = self.identity(document, root) if root is not None and root.type == "identifier" else {}
                if (root_identity.get("import") or {}).get("module") in {"node:path", "path"} and method in {"join", "resolve", "dirname"}:
                    operands = [self.path_expression(document, definition, argument, actuals=actuals, selected_file=selected_file, depth=depth + 1, seen=visited) for argument in arguments]
                    combinations = [[]]
                    for choices in operands:
                        combinations = [prior + [choice] for prior in combinations for choice in choices]
                        if len(combinations) > 128:
                            return [{"kind": "unknown", "reason": "path_choice_budget", "location": location}]
                    values = []
                    for combination in combinations:
                        concrete = all(item.get("kind") in {"literal", "captured_path"} and isinstance(item.get("path"), str) for item in combination)
                        if concrete:
                            path_value = posixpath.dirname(combination[0]["path"]) if method == "dirname" and len(combination) == 1 else posixpath.normpath(posixpath.join(*(item["path"] for item in combination))) if method != "dirname" and combination else ""
                            if selected_file and path_value.endswith(".js") and path_value[:-3] + ".ts" == selected_file:
                                path_value = selected_file
                            values.append({"kind": "captured_path", "path": path_value, "location": location, "operands": combination,
                                "path_operator": method, "model_id": "source-derived-module-assembly-v1"})
                        else:
                            suffix = []
                            for item in reversed(combination):
                                if item.get("kind") != "literal":
                                    break
                                suffix.insert(0, item["path"])
                            values.append({"kind": "symbolic_path", "literal_suffix": posixpath.normpath(posixpath.join(*suffix)) if suffix else "", "operands": combination,
                                "path_operator": method, "location": location, "overridden_or_unknown_root": True})
                    return values
        return [{"kind": "unknown", "location": location, "source_text": document.text(node)}]

    def default_cli_assembly(self) -> dict:
        """Bind the actual finite command import and its real context literal."""
        entry = self.rule["entry"]
        records, actuals = [], {}
        selected_entry = self.component(entry)
        if selected_entry is None:
            return {"supported": False, "gaps": ["entry_source_invalid"], "calls": []}
        for document, definition, function in list(self.components.values()):
            for call in _walk(_field(function, "body")):
                if call.type != "call_expression":
                    continue
                callee = unwrap(_field(call, "function"))
                if callee is None or callee.type != "member_expression" or self.key(document, _field(callee, "property")) != entry["symbol"]:
                    continue
                receiver = unwrap(_field(callee, "object"))
                identity = self.identity(document, receiver) if receiver is not None and receiver.type == "identifier" else {}
                initial = unwrap(self.reader(document).initializer_for(identity))
                imports = [node for node in _walk(initial, nested=True) if node.type == "call_expression" and document.text(_field(node, "function")) == "import"]
                for imported in imports:
                    import_arguments = _children(_field(imported, "arguments"))
                    if len(import_arguments) != 1:
                        continue
                    paths = self.path_expression(document, definition, import_arguments[0], selected_file=entry["file"])
                    selected = [path for path in paths if path.get("kind") == "captured_path" and path.get("path") == entry["file"]]
                    if not selected:
                        continue
                    writes = self.reader(document).writes(identity)
                    arguments = _children(_field(call, "arguments"))
                    bindings = []
                    entry_doc, entry_def, entry_fn = selected_entry
                    for parameter in _walk(_field(entry_fn, "parameters"), nested=True):
                        if parameter.type not in {"identifier", "shorthand_property_identifier_pattern"}:
                            continue
                        formal = self.identity(entry_doc, parameter)
                        index = formal.get("parameter_index")
                        if formal.get("declaration_kind") != "parameter" or not isinstance(index, int) or index >= len(arguments):
                            continue
                        actual = arguments[index]
                        for part in (formal.get("pattern_path") or []):
                            if part["kind"] == "object_property" and actual is not None and actual.type == "object":
                                pairs = [pair for pair in _children(actual) if pair.type == "pair" and self.key(document, _field(pair, "key")) == part.get("name")]
                                actual = _field(pairs[0], "value") if len(pairs) == 1 else None
                            elif part["kind"] not in {"parameter", "default_value"}:
                                actual = None
                        if actual is not None:
                            actuals[formal["declaration_id"]] = (document, definition, actual)
                            bindings.append({"formal_declaration_id": formal["declaration_id"], "parameter_index": index, "pattern_path": formal.get("pattern_path"),
                                "actual_location": document.location(actual), "actual_value_id": self.expression(document, definition, actual)})
                    records.append({"location": document.location(call), "owner": definition.graph_node_id, "import_location": document.location(imported),
                        "same_import_receiver_declaration_id": identity.get("declaration_id"), "selected_paths": selected, "other_path_choices": [path for path in paths if path not in selected],
                        "receiver_captured_writes": writes, "actual_parameter_bindings": bindings,
                        "supported": not writes and bool(bindings), "creates_CALLS_edge": False})
        self.entry_actuals = actuals
        return {"supported": bool(records) and all(item["supported"] for item in records) and "source-derived-module-assembly-v1" in self.rule["models"],
            "calls": records, "gaps": [] if records and all(item["supported"] for item in records) else ["default_finite_cli_module_context_not_connected"],
            "scope": "captured default executor root and selected finite command table member; environment root overrides remain explicit alternatives"}

    def request_import_assembly(self) -> dict:
        selected = self.component(self.rule["request"]["owner"])
        if selected is None:
            return {"supported": False, "gaps": ["request_owner_source_invalid"]}
        document, definition, function = selected
        records = []
        for call in _walk(_field(function, "body")):
            if call.type != "call_expression" or document.text(_field(call, "function")) != self.rule["request"]["callee"]:
                continue
            callee = _field(call, "function"); identity = self.identity(document, callee)
            initial = unwrap(self.reader(document).initializer_for(identity))
            if initial is not None and initial.type == "await_expression":
                initial = unwrap(_children(initial)[0])
            arguments = _children(_field(initial, "arguments")) if initial is not None and initial.type == "call_expression" and document.text(_field(initial, "function")) == "import" else []
            members = [part.get("name") for part in (identity.get("pattern_path") or []) if part["kind"] == "object_property"]
            if len(arguments) != 1 or len(members) != 1:
                records.append({"location": document.location(call), "supported": False, "reason": "actual_request_import_binding_missing"}); continue
            paths = self.path_expression(document, definition, arguments[0], actuals=getattr(self, "entry_actuals", {}))
            captured = {source.path for source in self.snapshot.files}
            targets = []
            for path in paths:
                filename = path.get("path", "")
                filename = filename[:-3] + ".ts" if filename.endswith(".js") else filename
                if path["kind"] == "captured_path" and filename in captured:
                    target = self.component({"file": filename, "symbol": members[0]})
                    if target is not None:
                        targets.append({"target_owner": target[1].graph_node_id, "target_selector": {"file": filename, "symbol": members[0]}, "path_evidence": path})
            records.append({"location": document.location(call), "actual_import_location": document.location(initial), "callee_identity": identity,
                "targets": targets, "path_choices": paths, "captured_binding_writes": self.reader(document).writes(identity),
                "supported": bool(targets) and not self.reader(document).writes(identity), "creates_CALLS_edge": False})
        return {"supported": bool(records) and all(item["supported"] for item in records), "calls": records,
            "gaps": [] if records and all(item["supported"] for item in records) else ["default_request_module_path_context_not_connected"]}

    def production_assembly(self) -> dict:
        cli = self.default_cli_assembly()
        request = self.request_import_assembly()
        nominal = self.receiver_assembly()
        selected = self.component(self.rule["worker"]["owner"])
        worker_receivers, process_starts = [], []
        if selected is not None:
            document, definition, function = selected
            for call in _walk(_field(function, "body")):
                callee = unwrap(_field(call, "function")) if call.type == "call_expression" else None
                if callee is not None and callee.type == "member_expression":
                    binding = self.nominal_call_binding(document, definition, call)
                    if binding.get("targets") and len({target["selector"]["file"] for target in binding["targets"]}) > 1:
                        worker_receivers.append({"location": document.location(call), "binding": binding,
                            "same_actual_receiver_value_id": self.expression(document, definition, _field(callee, "object"))})
            worker_file = document.source.path
            for owner_doc, owner_def, owner_fn in list(self.components.values()):
                for call in _walk(_field(owner_fn, "body"), nested=True):
                    if call.type != "call_expression":
                        continue
                    callee = _field(call, "function")
                    identity = self.identity(owner_doc, callee) if callee is not None and callee.type == "identifier" else {}
                    imported = identity.get("import") or {}
                    if imported.get("module") not in {"node:child_process", "child_process"} or imported.get("imported_name") != "spawn":
                        continue
                    arguments = _children(_field(call, "arguments"))
                    for argument in arguments:
                        if argument.type != "array":
                            continue
                        elements = _children(argument)
                        if not elements:
                            continue
                        choices = self.path_expression(owner_doc, owner_def, elements[0])
                        matches = [item for item in choices if (item.get("literal_suffix", "").removesuffix(".js") + ".ts" == worker_file) or item.get("path", "").removesuffix(".js") + ".ts" == worker_file]
                        if not matches:
                            continue
                        process_starts.append({"location": owner_doc.location(call), "owner": owner_def.graph_node_id, "callee_identity": identity,
                            "worker_source_path_choices": matches, "argv": [{"location": owner_doc.location(element), "value_id": self.expression(owner_doc, owner_def, element)} for element in elements],
                            "standard_spawn_binding": imported.get("module") in {"node:child_process", "child_process"} and imported.get("imported_name") == "spawn",
                            "seam_kind": "normal source-derived Node worker process argv/environment", "creates_CALLS_edge": False})
        gaps = [*cli["gaps"], *request["gaps"]]
        if not worker_receivers or not all(item["binding"]["all_captured_receiver_variants_resolved"] for item in worker_receivers):
            gaps.append("worker_direct_and_broker_receiver_sources_not_connected")
        if not process_starts or not all(item["standard_spawn_binding"] for item in process_starts):
            gaps.append("normal_worker_process_source_and_argv_not_connected")
        if not nominal["source_receiver_calls"]:
            gaps.append("queue_scheduler_assignment_receiver_assembly_missing")
        return {"supported": not gaps, "gaps": gaps, "cli": cli, "request": request,
            "constructor_receiver_assemblies": nominal["source_receiver_calls"], "worker_direct_broker_variants": worker_receivers,
            "worker_process_starts": process_starts, "model_id": "source-derived-module-assembly-v1",
            "scope": "actual captured default source assembly; external module roots, injected receivers/providers/fetch and failed/not-run operations separately retained"}

    def forwarding_chain(self, selector: dict, parameter_index: int, field_path: list[str]) -> dict:
        """Follow real bare-formal wrappers; stop at a composed/opaque consumer."""
        seen, chain, gaps = set(), [], []
        current = selector
        for _depth in range(_MAX_DEPTH):
            selected = self.component(current)
            if selected is None:
                gaps.append("forwarding_source_invalid")
                break
            document, definition, function = selected
            if definition.graph_node_id in seen:
                gaps.append("forwarding_cycle")
                break
            seen.add(definition.graph_node_id)
            returns = [node for node in _walk(_field(function, "body")) if node.type == "return_statement"]
            if len(returns) != 1 or not _children(returns[0]):
                gaps.append("forwarding_normal_return_not_unique")
                break
            operand = unwrap(_children(returns[0])[0])
            if operand.type == "await_expression":
                operand = unwrap(_children(operand)[0])
            if operand.type != "call_expression":
                gaps.append("forwarding_return_not_invocation")
                break
            edge, issues = self.sources.call_binding(operand, document, definition)
            if edge is None:
                gaps.append("forwarding_actual_callee_binding_unknown")
                chain.append({"location": document.location(operand), "binding_issues": issues})
                break
            arguments = _children(_field(operand, "arguments"))
            argument = arguments[parameter_index] if parameter_index < len(arguments) else None
            path = self.path(document, argument)
            same_formal = bool(path and not path["keys"] and path.get("identity", {}).get("declaration_kind") == "parameter" and path["identity"].get("parameter_index") == parameter_index)
            chain.append({"owner": definition.graph_node_id, "location": document.location(operand), "edge_id": edge.id,
                "target": edge.target, "argument_index": parameter_index, "same_formal_read": same_formal,
                "completion": completion_relation(document, operand, function, "return_or_await", lexical=self.reader(document)),
                "selected_field_path": field_path})
            target_nodes = self.sources.nodes.get(edge.target, [])
            target_document, target_definition, _issues = self.sources.definition_for_node(target_nodes[0]) if len(target_nodes) == 1 else (None, None, [])
            if target_document is None or target_definition is None:
                gaps.append("forwarding_target_source_unknown")
                break
            if not same_formal:
                # Actual composition is assessed by the public selected-field
                # summary; no raw-key theorem replaces that state transfer.
                from .field_summaries import summarize_field, MODEL_ID, READ_MODEL_ID
                field_summary = summarize_field(self.snapshot, current, parameter_index=parameter_index,
                    field_path=field_path, sink={"kind": "call_argument", "callee": document.text(_field(operand, "function")),
                        "argument_index": parameter_index, "field_path": field_path}, models=[MODEL_ID, READ_MODEL_ID])
                chain[-1]["ordered_field_summary"] = field_summary
                if not field_summary.get("source_form_complete"):
                    gaps.append("composed_field_argument_source_unknown")
                return {"supported": not gaps, "chain": chain, "endpoint": {"file": target_document.source.path, "symbol": target_definition.symbol},
                    "gaps": gaps, "scope": "normal call argument source; activation and whole-engine budget consumption separate"}
            current = {"file": target_document.source.path, "symbol": target_definition.symbol}
        else:
            gaps.append("forwarding_depth_budget")
        return {"supported": False, "chain": chain, "gaps": gaps}

    def consumer_connection(self, sites: list[dict]) -> dict:
        selected = self.component(self.rule["worker"]["owner"])
        if selected is None:
            return {"supported": False, "gaps": ["worker_source_invalid"], "sites": []}
        document, definition, function = selected
        connections = []
        for node in _walk(_field(function, "body")):
            if node.type != "call_expression" or document.text(_field(node, "function")) != self.rule["worker"]["callee"]:
                continue
            dynamic = self.dynamic_import_binding(document, definition, _field(node, "function"))
            forwarding = self.forwarding_chain(dynamic["target_selector"], self.rule["worker"]["argument_index"],
                self.rule["worker"]["field_path"]) if dynamic.get("supported") else {"supported": False, "gaps": [dynamic.get("reason", "dynamic_module_model_unknown")]}
            connections.append({"site": document.location(node), "actual_dynamic_import": dynamic,
                "forwarding": forwarding, "supported": bool(dynamic.get("supported") and forwarding.get("supported"))})
        gaps = [] if connections and all(item["supported"] for item in connections) else ["bridge_engine_effective_consumer_mapping_not_completely_connected"]
        return {"supported": not gaps, "sites": connections, "gaps": gaps,
            "scope": "actual selected worker argument, fixed imported bridge, ordinary forwarding and ordered final engine argument"}

    def budget_judgment(self, budgets: list[dict], consumer: dict, channels: dict) -> dict:
        authorities = []
        for spec, budget in zip(self.rule["budgets"], budgets):
            selected = self.component(spec["owner"])
            if selected is None:
                authorities.append({"budget_kind": spec["kind"], "supported": False, "gaps": ["budget_source_invalid"]}); continue
            document, definition, function = selected
            field_reads, counter_sources, limit_sources = [], [], []
            for node in _walk(_field(function, "body"), nested=True):
                if node.type not in {"member_expression", "subscript_expression"}:
                    continue
                path = self.path(document, node)
                if path and path["static"] and path["keys"] and path["keys"][-len(self.rule["request"]["field_path"]):] == self.rule["request"]["field_path"]:
                    field_reads.append({"location": document.location(node), "source_path": path})
            for key, output in ((spec["counter"], counter_sources), (spec["limit"], limit_sources)):
                binding = budget.get("bindings", {}).get(key, {})
                identifier = binding.get("initializer_value_id")
                if identifier:
                    output.extend(self.reachable_terms(identifier))
            counter_record_projections = [term for term in counter_sources if term["kind"] in {"field_projection", "dynamic_projection"}]
            limit_record_projections = [term for term in limit_sources if term["kind"] in {"field_projection", "dynamic_projection"}]
            relevant_limit_calls = [term for term in limit_sources if term["kind"] == "invocation"]
            gaps = list(budget.get("gaps", []))
            if not limit_sources or not counter_sources:
                gaps.append("actual_budget_initializer_source_not_available")
            authorities.append({"budget_kind": spec["kind"], "owner": spec["owner"], "supported": not gaps, "gaps": gaps,
                "actual_counter_initializer_terms": counter_sources, "actual_limit_initializer_terms": limit_sources,
                "counter_record_projections": counter_record_projections, "limit_record_projections": limit_record_projections,
                "actual_limit_calls": relevant_limit_calls, "decision_guards": budget.get("decision_guards", []),
                "selected_request_metadata_reads_in_authority_body": field_reads,
                "guard_preceding_returns": budget.get("early_returns_before_first_guard", []),
                "opaque_consumers": budget.get("opaque_consumers", []),
                "whole_program_or_all_retry_actions_covered": False,
                "decision_source_relation": "local declaration/record-table/configuration limit and matching actual counter; each authority remains distinct"})
        counter_transport = channels.get("counter_transport", {"supported": False, "gaps": ["assignment_attempt_state_transport_not_connected"]})
        gaps = [gap for authority in authorities for gap in authority["gaps"]]
        gaps.extend(counter_transport.get("gaps", []))
        if not counter_transport.get("supported"):
            gaps.append("assignment_attempt_state_transport_not_connected")
        if not consumer.get("supported"):
            gaps.append("worker_final_engine_argument_unconnected")
        return {"supported": not gaps and all(item["supported"] for item in authorities) and bool(counter_transport.get("supported")),
            "gaps": list(dict.fromkeys(item.get("code", "unclosed_channel_relation") if isinstance(item, dict) else item for item in gaps)), "authorities": authorities, "counter_transport": counter_transport,
            "worker_effective_argument": consumer, "policy_invariant": self.rule["invariant"],
            "opaque_scope": "No claim that opaque supervisor/provider or arbitrary caller does not consume metadata. The actual selected local authority decisions and normal managed argument are assessed.",
            "retry_ability_present": bool(any(budget.get("decision_guards") for budget in budgets))}

    def local_record_transport(self, relations: dict, assembly: dict, channels: dict, modes: dict) -> dict:
        """Join actual local record constructors to their bound source calls.

        Each witness is a conditional current-record relation. Durable/HTTP
        identity is supplied by the separately checked channel relation, rather
        than by matching field spellings or modifying the old field domain.
        """
        root_keys = self.rule["request"]["field_path"]
        root, leaf = root_keys[0], root_keys[-1]
        normalization, call_records, assignment_returns, current_copies, worker_reads = [], [], [], [], []
        request_targets = {target["target_owner"] for call in assembly.get("request", {}).get("calls", []) for target in call.get("targets", [])}
        for relation in relations["parameter_return_slot_relations"]:
            call_owner = next((fact["anchor"]["owner"] for fact in self.facts.values() if fact["location"].get("file") == relation["call_location"]["file"] and fact["location"].get("start_byte") == relation["call_location"]["start_byte"]), "")
            if call_owner in request_targets and relation["return_relation"]["selected_path"] == root_keys[1:]:
                normalization.append(relation)
        for document, definition, function in list(self.components.values()):
            for call in _walk(_field(function, "body"), nested=True):
                if call.type != "call_expression":
                    continue
                arguments = _children(_field(call, "arguments"))
                for index, argument in enumerate(arguments):
                    argument = unwrap(argument)
                    if argument is None or argument.type != "object":
                        continue
                    pairs = [pair for pair in _children(argument) if pair.type == "pair" and self.key(document, _field(pair, "key")) == root]
                    if not pairs:
                        continue
                    target = self.source_target(document, definition, call)
                    nominal = self.nominal_call_binding(document, definition, call) if unwrap(_field(call, "function")).type == "member_expression" else None
                    records = []
                    for pair in pairs:
                        source = unwrap(_field(pair, "value"))
                        source_path = self.path(document, source)
                        if source.type == "binary_expression" and document.text(_field(source, "operator")) in {"||", "??"}:
                            source_path = self.path(document, _field(source, "left"))
                        records.append({"location": document.location(pair), "source_expression": document.text(source),
                            "current_source_path": source_path, "source_value_id": self.expression(document, definition, source),
                            "selected_slot_current_relation": bool(source_path and source_path["static"] and source_path["keys"] and source_path["keys"][-1] == root),
                            "source_tree": "ordinary literal/decoded record in checked channel", "fresh_request_origin_proven_here": False})
                    call_records.append({"location": document.location(call), "owner": document.call_owner(call), "argument_index": index,
                        "actual_target": target[1].graph_node_id if target else None, "actual_nominal_binding": nominal,
                        "field_records": records, "supported": bool(target and all(item["selected_slot_current_relation"] for item in records)),
                        "scope": "current selected record field passed in the actual new argument record"})
                    if target is not None:
                        target_doc, target_def, target_fn = target
                        incoming_formals = []
                        for token in _walk(_field(target_fn, "parameters"), nested=True):
                            if token.type not in {"identifier", "shorthand_property_identifier_pattern"}:
                                continue
                            identity = self.identity(target_doc, token)
                            path = [part.get("name") for part in (identity.get("pattern_path") or []) if part["kind"] == "object_property"]
                            if identity.get("declaration_kind") == "parameter" and identity.get("parameter_index") == index and path == [root]:
                                incoming_formals.append(identity)
                        if incoming_formals:
                            outputs = []
                            for literal in _walk(_field(target_fn, "body"), nested=True):
                                if literal.type != "object":
                                    continue
                                selected_pairs = [pair for pair in _children(literal) if pair.type == "pair" and self.key(target_doc, _field(pair, "key")) == root]
                                for pair in selected_pairs:
                                    source = unwrap(_field(pair, "value"))
                                    source_calls = [item for item in _walk(source) if item.type == "call_expression"]
                                    incoming = []
                                    for helper in source_calls:
                                        helper_target = self.source_target(target_doc, target_def, helper)
                                        for helper_index, actual in enumerate(_children(_field(helper, "arguments"))):
                                            if any(self.reader(target_doc).same(formal, actual) for formal in incoming_formals) and helper_target is not None:
                                                theorem = self.return_slot_relation(*helper_target, helper_index, root_keys[1:])
                                                incoming.append({"location": target_doc.location(helper), "actual_formal_declaration_id": self.identity(target_doc, actual).get("declaration_id"),
                                                    "normal_return_relation": theorem, "supported": theorem["supported"]})
                                    if incoming:
                                        surfaces = _children(source) if source.type == "object" else []
                                        later_keys = [self.key(target_doc, _field(item, "key") if item.type == "pair" else item) for item in surfaces if item.type not in {"spread_element"}]
                                        outputs.append({"location": target_doc.location(pair), "source_expression": target_doc.text(source), "incoming_current_relations": incoming,
                                            "ordered_merge_members": self.terms[self.expression(target_doc, target_def, source)].get("members", []),
                                            "fixed_keys": later_keys, "supported": all(item["supported"] for item in incoming) and all(key is not None and key != leaf and key != "__proto__" for key in later_keys),
                                            "conditional_presence": True, "existing_branch_preserves_prior_fields_when_incoming_field_absent": source.type == "object"})
                            assignment_returns.append({"actual_call_location": document.location(call), "target": target_def.graph_node_id,
                                "incoming_formals": incoming_formals, "metadata_constructions": outputs,
                                "supported": len(outputs) >= 2 and all(item["supported"] for item in outputs),
                                "scope": "actual new and merge constructions, incoming spread order; prior assignment identity/history remains distinct"})
        for update in relations["field_updates"]:
            target = update["target"]
            suffix = target["keys"][target["keys"].index(root) + 1:]
            if suffix and suffix[0] != root_keys[1]:
                current_copies.append({**update, "supported": True, "relation": "disjoint selected-root child write on the ordinary data tree"})
            elif not suffix:
                fixed_safe = all(key is not None and key != leaf and key != "__proto__" for key in update["fixed_keys"])
                source_relation = self.current_record_update_relation(update["location"], root_keys[1:])
                current_copies.append({**update, "supported": not update["selected_slot_explicit_override"] and fixed_safe and source_relation["supported"],
                    "actual_source_update_relation": source_relation,
                    "relation": "actual whole-record replacement/copy; conditional current selected slot and explicit later-spread sources retained",
                    "initial_producer_source_certified": False})
            else:
                current_copies.append({**update, "supported": False, "relation": "explicit selected-slot write requires independent value-source assessment"})
        selected_worker = self.component(self.rule["worker"]["owner"])
        if selected_worker is not None:
            document, definition, function = selected_worker
            for declaration in _walk(_field(function, "body")):
                if declaration.type != "variable_declarator":
                    continue
                initial = unwrap(_field(declaration, "value")); initial_path = self.path(document, initial)
                if initial is not None and initial.type == "binary_expression" and document.text(_field(initial, "operator")) in {"||", "??"}:
                    initial_path = self.path(document, _field(initial, "left"))
                if initial_path and initial_path["static"] and initial_path["keys"] and initial_path["keys"][-1] == root:
                    record_identity = self.identity(document, unwrap(_field(initial, "left") or initial).child_by_field_name("object")) if unwrap(_field(initial, "left") or initial).type == "member_expression" else {}
                    initializer = unwrap(self.reader(document).initializer_for(record_identity))
                    claim_path = self.path(document, initializer)
                    worker_reads.append({"location": document.location(declaration), "metadata_source_path": initial_path,
                        "assignment_declaration_id": record_identity.get("declaration_id"), "assignment_initializer_path": claim_path,
                        "claim_to_assignment_property_relation": bool(claim_path and claim_path["static"] and claim_path["keys"]),
                        "source_value_id": self.expression(document, definition, initial), "current_record_slot_only": True})
        gaps = []
        if not normalization:
            gaps.append("request_normalization_current_metadata_return_not_connected")
        # The producer request's own metadata literal is assessed by P1. All
        # discovered member-call transport records must have real receivers and
        # current selected metadata reads, not matching callee names.
        member_records = [item for item in call_records if item["actual_nominal_binding"] is not None]
        if len(member_records) < 2 or not all(item["supported"] for item in member_records):
            gaps.append("candidate_assignment_inbox_actual_field_argument_records_not_connected")
        if not assignment_returns or not all(item["supported"] for item in assignment_returns):
            gaps.append("assignment_new_existing_incoming_field_constructions_not_connected")
        if not current_copies or not all(item["supported"] for item in current_copies):
            gaps.append("actual_intermediate_selected_field_mutations_not_classified")
        if not worker_reads or not all(item["claim_to_assignment_property_relation"] for item in worker_reads):
            gaps.append("actual_worker_claim_assignment_metadata_read_not_connected")
        if not modes.get("existing_return_branches"):
            gaps.append("old_queue_entry_identity_reuse_not_classified")
        gaps.extend(channels.get("gaps", []))
        return {"supported": not gaps and channels.get("supported", False), "gaps": list(dict.fromkeys(item.get("code", "unclosed_channel_relation") if isinstance(item, dict) else item for item in gaps)),
            "normalization_returns": normalization, "actual_metadata_argument_records": call_records,
            "assignment_incoming_constructions": assignment_returns, "intermediate_current_record_updates": current_copies,
            "worker_claim_assignment_metadata_reads": worker_reads, "normal_array_element_relations": relations["normal_array_relations"],
            "callbacks": relations["actual_callback_invocations"], "channels": channels,
            "new_request_scope": "actual new normal queue entry, selected candidate, incoming assignment metadata and canonical committed inbox record",
            "existing_record_scope": "old pending return and prior assignment state are separate identities; incoming merge is conditional on own field presence",
            "model_id": "ordinary-record-tree-flow-v1", "old_ir_domain_upgraded": False}

    def current_record_update_relation(self, location: dict, selected_path: list[str]) -> dict:
        document = self.documents.get(location["file"])
        if document is None:
            return {"supported": False, "reason": "update_source_missing"}
        matches = [node for node in _walk(document.tree.root_node, nested=True) if node.start_byte == location["start_byte"] and node.end_byte == location["end_byte"] and node.type == "assignment_expression"]
        if len(matches) != 1:
            return {"supported": False, "reason": "update_ast_not_unique"}
        assignment = matches[0]
        owners = document.definition_nodes.get(document.call_owner(assignment), [])
        if len(owners) != 1:
            return {"supported": False, "reason": "update_owner_not_unique"}
        definition = owners[0]
        target = self.path(document, _field(assignment, "left"))
        active = set()
        def source(node: Any, depth: int = 0) -> dict:
            node = unwrap(node)
            if node is None or depth >= _MAX_DEPTH or node.id in active:
                return {"supported": False, "reason": "update_source_cycle_or_budget"}
            active.add(node.id)
            try:
                path = self.path(document, node)
                if path and path["static"] and path["keys"] and path["keys"][-1] == self.rule["request"]["field_path"][0]:
                    return {"supported": True, "kind": "current_record_slot_read", "source_path": path,
                        "same_current_target": target is not None and path.get("declaration_id") == target.get("declaration_id") and path["keys"] == target["keys"],
                        "incoming_frame_or_channel_identity_checked_separately": True, "location": document.location(node)}
                if node.type in {"identifier", "shorthand_property_identifier"}:
                    identity = self.identity(document, node)
                    initial = self.reader(document).initializer_for(identity)
                    if initial is not None and not any(write.get("binding_reassignment") for write in self.reader(document).writes(identity)):
                        return source(initial, depth + 1)
                    if identity.get("declaration_kind") == "parameter" and isinstance(identity.get("parameter_index"), int):
                        owner = document.definition_nodes.get(document.call_owner(node), [])
                        formal_owner = owner[0] if len(owner) == 1 else None
                        actuals = []
                        if formal_owner is not None:
                            for caller_doc, caller_def, caller_fn in list(self.components.values()):
                                for call in _walk(_field(caller_fn, "body"), nested=True):
                                    if call.type != "call_expression":
                                        continue
                                    callee = _field(call, "function")
                                    # A name is only a cheap discovery filter;
                                    # target identity must still authenticate.
                                    name = self.key(caller_doc, _field(callee, "property")) if callee.type == "member_expression" else caller_doc.text(callee)
                                    if name != formal_owner.symbol.rsplit(".", 1)[-1]:
                                        continue
                                    called = self.source_target(caller_doc, caller_def, call)
                                    arguments = _children(_field(call, "arguments"))
                                    index = identity["parameter_index"]
                                    if called is None or called[1].graph_node_id != formal_owner.graph_node_id or index >= len(arguments) or arguments[index].type == "spread_element":
                                        continue
                                    actual = unwrap(arguments[index])
                                    absent = self.literal_absent(caller_doc, actual, selected_path)
                                    actuals.append({"call_location": caller_doc.location(call), "actual_argument_location": caller_doc.location(actual),
                                        "actual_target": called[1].graph_node_id, "selected_own_slot_absent_on_actual_literal": absent,
                                        "literal_value_id": self.expression(caller_doc, caller_def, actual)})
                        if actuals and all(item["selected_own_slot_absent_on_actual_literal"] for item in actuals):
                            return {"supported": True, "kind": "actual_disjoint_literal_formal_inputs", "formal_declaration_id": identity["declaration_id"],
                                "actual_calls": actuals, "conditional_default_source_scope": True, "selected_field_absent": True}
                if node.type == "await_expression":
                    return source(_children(node)[0], depth + 1)
                if node.type == "binary_expression" and document.text(_field(node, "operator")) in {"||", "??"}:
                    first = source(_field(node, "left"), depth + 1)
                    fallback = self.literal_absent(document, unwrap(_field(node, "right")), selected_path)
                    return {"supported": first["supported"] and fallback, "kind": "record_truthiness_or_nullish_fallback", "input": first,
                        "fallback_selected_field_absent": fallback, "conditional_presence": True, "location": document.location(node)}
                if node.type == "object":
                    ordered, has_source = [], False
                    for member in _children(node):
                        if member.type == "spread_element":
                            relation = source(_children(member)[0], depth + 1)
                            ordered.append({"kind": "spread", "relation": relation, "location": document.location(member)})
                            has_source |= relation["supported"]
                        elif member.type in {"pair", "shorthand_property_identifier"}:
                            key = self.key(document, _field(member, "key") if member.type == "pair" else member)
                            if key is None or key == selected_path[0] or key == "__proto__":
                                return {"supported": False, "reason": "selected_or_computed_literal_override", "location": document.location(member)}
                            ordered.append({"kind": "fixed_disjoint_key", "key": key})
                        else:
                            return {"supported": False, "reason": "literal_accessor_method_or_other_surface", "location": document.location(member)}
                    if not ordered:
                        predicate = unwrap(next((_field(parent, "condition") for parent in _ancestors(assignment.parent) if parent.type == "if_statement"), None))
                        operand = _field(predicate, "argument") if predicate is not None and predicate.type == "unary_expression" and document.text(_field(predicate, "operator")) == "!" else None
                        tested = self.path(document, operand)
                        guarded_empty = bool(tested and target and tested.get("declaration_id") == target.get("declaration_id") and tested["keys"] == target["keys"])
                        return {"supported": guarded_empty, "kind": "guarded_missing_current_root_fallback", "predicate_location": document.location(predicate) if predicate is not None else None,
                            "new_producer_root_present_excludes_branch": guarded_empty}
                    return {"supported": has_source and all(item.get("relation", {"supported": True})["supported"] for item in ordered), "kind": "ordered_conditional_current_data_merge",
                        "ordered_members": ordered, "conditional_presence": True, "source_entry_origin_proven": False, "location": document.location(node)}
                if node.type == "call_expression":
                    helper = self.source_target(document, definition, node)
                    if helper is not None:
                        related = []
                        for index, actual in enumerate(_children(_field(node, "arguments"))):
                            relation = source(actual, depth + 1)
                            if relation["supported"]:
                                theorem = self.return_slot_relation(*helper, index, selected_path)
                                related.append({"actual_input": relation, "normal_return_relation": theorem, "supported": theorem["supported"]})
                        return {"supported": bool(related) and all(item["supported"] for item in related), "kind": "actual_helper_current_slot_return", "relations": related,
                            "actual_target": helper[1].graph_node_id, "location": document.location(node)}
                return {"supported": False, "reason": "replacement_source_not_classified", "location": document.location(node), "node_type": node.type}
            finally:
                active.discard(node.id)
        return source(_field(assignment, "right"))


def _obligation(identifier: str, status: str, evidence: Any, gaps: list[str], conclusion: str) -> dict:
    return {"id": identifier, "status": status, "evidence": evidence, "gaps": gaps, "necessary_gaps": gaps,
        "conclusion": conclusion, "required": True}


def analyze_pipeline_flow(snapshot: GraphSnapshot, rule: dict) -> dict:
    """Return the original six obligations, including every unresolved seam."""
    validate_pipeline_flow_rule(rule)
    analysis = _Analysis(snapshot, rule)
    selectors = [rule["entry"], rule["producer"]["owner"], rule["request"]["owner"], rule["worker"]["owner"],
        *(budget["owner"] for budget in rule["budgets"]), *rule["sources"]]
    for selector in {item["file"] + "#" + item["symbol"]: item for item in selectors}.values():
        analysis.inspect(selector)
    request, worker = analysis.site(rule["request"]), analysis.site(rule["worker"])
    producer = analysis.component(rule["producer"]["owner"])
    flags, producer_returns = [], []
    if producer is not None:
        document, definition, function = producer
        for node in _walk(_field(function, "body")):
            if node.type == "string" and _literal_string(document.text(node)) == rule["producer"]["option"]:
                branch = next((parent for parent in _ancestors(node.parent) if parent.type == "if_statement"), None)
                writes = [child for child in _walk(_field(branch, "consequence")) if child.type == "assignment_expression"]
                flags.append({"location": document.location(node), "condition": document.location(_field(branch, "condition")) if branch is not None else None,
                    "writes": [{"location": document.location(child), "target": analysis.path(document, _field(child, "left")),
                        "value_id": analysis.expression(document, definition, _field(child, "right"))} for child in writes]})
            if node.type == "return_statement" and _children(node):
                value = analysis.expression(document, definition, _children(node)[0])
                selected = analysis.project(value, rule["producer"]["output_path"], document, definition, node)
                producer_returns.append({"location": document.location(node), "selected_value_id": selected,
                    "normal_reaching_value_proven": False})
    budgets = [analysis.budget(spec) for spec in rule["budgets"]]
    worker_values = [analysis.terms[site["selected_value_id"]] for site in worker]
    literal_cut = bool(worker and all(value["kind"] == "literal" for value in worker_values))
    producer_connection = analysis.producer_connection(flags, producer_returns, request)
    consumer_connection = analysis.consumer_connection(worker)
    production_assembly = analysis.production_assembly()
    field_relations = analysis.record_field_relations()
    source_modes = analysis.source_modes(worker)
    from .pipeline_channels import analyze_pipeline_channels
    channels = analyze_pipeline_channels(analysis)
    record_transport = analysis.local_record_transport(field_relations, production_assembly, channels, source_modes)
    budget_judgment = analysis.budget_judgment(budgets, consumer_connection, channels)
    p1_gaps = producer_connection["gaps"]
    p2_gaps = production_assembly["gaps"]
    p3_gaps = record_transport["gaps"]
    p4_gaps = consumer_connection["gaps"]
    p5_gaps = budget_judgment["gaps"]
    refutations = {"literal_selected_worker_values": worker_values,
        "equal_request_value_possible": bool(literal_cut),
        "budget_authorities_are_distinct": [budget["budget_kind"] for budget in budgets],
        "pre_guard_returns": [item for budget in budgets for item in budget.get("early_returns_before_first_guard", [])],
        "opaque_consumers": [item for budget in budgets for item in budget.get("opaque_consumers", [])],
        "source_conditional_returns": [fact for fact in analysis.facts.values() if fact["kind"] == "body_return"],
        "policy_refutations": rule["refutations"], "source_modes": source_modes,
        "direct_broker_source_assembly": production_assembly.get("worker_direct_broker_variants", []),
        "record_identity_modes": {"new_request": record_transport["new_request_scope"], "existing": record_transport["existing_record_scope"]},
        "all_required_modes_classified": bool(source_modes["source_classification_complete"] and production_assembly.get("worker_direct_broker_variants") and channels.get("supported")),
        "selected_parameter_is_not_no_retry_ability_claim": True,
        "normal_execution_or_route_activation_guaranteed": False}
    p6_gaps = [] if refutations["all_required_modes_classified"] and literal_cut and consumer_connection["supported"] else ["source_mode_counterevidence_not_completely_classified"]
    obligations = [
        _obligation("P1", "supported" if producer_connection["supported"] else "partial" if flags and producer_returns and request else "unknown",
            {"flag_branches": flags, "producer_returns": producer_returns, "request_sites": request, "connection": producer_connection}, p1_gaps,
            "Actual flag write declaration, its returned field and actual parser invocation's selected request field are connected under the normal captured-source scope; numbers and downstream transport remain separate."),
        _obligation("P2", "supported" if production_assembly["supported"] else "partial" if analysis.components else "unknown",
            {"source_components": list(analysis.components), "production_assembly": production_assembly, "actual_bindings": [fact for fact in analysis.facts.values() if fact["kind"] == "actual_callee_binding"]}, p2_gaps,
            "Actual default command/import context, constructor injection, direct/broker receiver sources and process argv connect the selected normal source assembly; overrides are separate variants."),
        _obligation("P3", "supported" if record_transport["supported"] else "partial", {"field_relations": field_relations, "record_transport": record_transport, "channels": channels,
            "record_operations": [fact for fact in analysis.facts.values() if fact["kind"] in {"record_io_operation", "json_codec_application", "source_write"}]}, p3_gaps,
            "Actual normalization, ordered current-field constructions and record/JSON/channel identities are joined; new/incoming versus old pending and prior assignment state remain separate."),
        _obligation("P4", "supported" if literal_cut and consumer_connection["supported"] else "partial" if literal_cut else "unknown", {"worker_sites": worker, "literal_cut": literal_cut, "connection": consumer_connection}, p4_gaps,
            "The worker's selected independent literal is connected through the actual fixed bridge and ordered final engine argument; different effective budget authorities are assessed separately."),
        _obligation("P5", "supported" if budget_judgment["supported"] else "partial" if any(budget["source_complete"] for budget in budgets) else "unknown", {"budgets": budgets, "judgment": budget_judgment}, p5_gaps,
            "Actual per-authority limit/counter guards, durable attempt history, nested helper calls, preceding returns and opaque consumers are distinguished; the policy has no source-created budget equivalence."),
        _obligation("P6", "supported" if not p6_gaps else "partial", refutations, p6_gaps,
            "The source records value equality possibility, old queue/assignment reuse, finalizer-only, direct/broker choice, distinct budget authorities and opaque/early-return/not-run boundaries."),
    ]
    necessary = [{"obligation": item["id"], "code": gap} for item in obligations for gap in item["necessary_gaps"]]
    complete = not necessary and not analysis.gaps and all(item["status"] in {"supported", "refuted"} for item in obligations) and analysis.operations <= _MAX_NODES and len(analysis.components) <= _MAX_FUNCTIONS
    full = complete and all(item["status"] == "supported" for item in obligations)
    return {"schema": "callscope.parameter-record-budget.v1", "version": VERSION, "policy_version": POLICY_VERSION,
        "snapshot_id": snapshot.id, "source_hash": snapshot.source_hash, "policy_hash": snapshot.policy_hash,
        "contract_hash": _digest(rule), "original_claim": rule["original_claim"], "invariant": rule["invariant"],
        "conditions": rule["conditions"], "refutations": refutations, "obligations": obligations,
        "assessment": "scoped_static_judgment_reproduced" if full else "claim_refuted_or_narrowed" if complete else "partial_obligations_supported",
        "full_goal_supported": full, "complete_assessment": complete,
        "claim_needs_narrowing": False,
        "derived_judgment": "On the checked normal pipeline record/message path, the submitted retries field is transported as metadata but the managed worker constructs an independent selected literal. Actual queue, phase and infrastructure decisions use their distinct local authorities. Existing records, finalizer-only, early returns, opaque consumers and unsuccessful/not-run operations bound this finding; retry capability is present." if full else "Actual selected-source relationships support the obligations listed below; the remaining source/record/message gates prevent a complete pipeline judgment.",
        "necessary_gaps": necessary, "analysis_gaps": analysis.gaps,
        "models": [{"id": model, "authority": "explicit versioned conditional trusted model", "runtime_verified": False} for model in rule["models"]],
        "sources": [{"file": document.source.path, "hash": document.source.hash, "parse_id": document.parse_id} for document in analysis.documents.values()],
        "source_facts": list(analysis.facts.values()), "value_expressions": list(analysis.terms.values()),
        "flow_links": [asdict(link) for link in analysis.links.values()],
        "evidence_counts": {"source_facts": len(analysis.facts), "value_expressions": len(analysis.terms), "flow_links": len(analysis.links)},
        "evidence_truncated": any(gap["code"].endswith("budget_exceeded") for gap in analysis.gaps), "summary_budget": {"operations": analysis.operations, "limit": _MAX_NODES,
            "functions": len(analysis.components), "function_limit": _MAX_FUNCTIONS},
        "component_versions": {"semantic_sources": SOURCE_VERSION, "lexical_bindings": LEXICAL_VERSION},
        "target_executed": False, "target_tests_run": False, "runtime_value_verified": False,
        "full_functionality_proven": False}


def analyze_pipeline_flows(snapshot: GraphSnapshot, rules: list[dict]) -> list[Finding]:
    findings = []
    for index, rule in enumerate(rules):
        try:
            details = analyze_pipeline_flow(snapshot, rule)
        except (ValueError, TypeError) as error:
            details = {"version": VERSION, "snapshot_id": snapshot.id, "assessment": "unknown_or_source_invalid",
                "full_goal_supported": False, "complete_assessment": False, "obligations": [_obligation(f"P{i}", "unknown", [], ["invalid_contract"], str(error)) for i in range(1, 7)],
                "necessary_gaps": [{"code": "invalid_contract", "message": str(error)}]}
        fingerprint = _digest((VERSION, snapshot.project_id, rule))
        locations = [fact["location"] for fact in details.get("source_facts", [])]
        nodes = sorted({fact["anchor"]["owner"] for fact in details.get("source_facts", []) if fact["anchor"]["owner"]})
        edge_ids = sorted({fact["edge_id"] for fact in details.get("source_facts", []) if fact.get("edge_id")})
        evidence = Evidence(_digest((snapshot.id, fingerprint, details))[:24], "static_parameter_record_budget_flow",
            "Source-derived parameter, record/message and per-authority retry decisions with the original six obligations.",
            locations, nodes, edge_ids, details)
        findings.append(Finding(_digest((snapshot.id, fingerprint))[:24], "static_parameter_record_budget_flow", "info", "uncertain",
            "Parameter to retry-authority judgment", details.get("derived_judgment", "Required source relationship is unknown."),
            nodes, edge_ids, [evidence], rule.get("id", f"invalid-pipeline-{index}"), fingerprint, snapshot.id,
            {"analyzer_version": VERSION, "full_goal_supported": details["full_goal_supported"], "complete_assessment": details["complete_assessment"], "assessment": details["assessment"]}))
    return findings
