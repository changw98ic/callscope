"""Finite, source-derived architecture report chains over saved snapshots.

Report selectors locate declarations, not expected calls, branches or outcomes.
This module never reads a benchmark report, target worktree or target runtime.
Its evidence domain is conditional normal source order and captured construction;
it is deliberately separate from the five original anomaly judgments.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
import posixpath
from typing import Any

from .completion_summaries import function_kind
from .lexical_bindings import LexicalBindings, VERSION as LEXICAL_VERSION
from .models import Evidence, Finding, GraphSnapshot
from .semantic_sources import SemanticSources, VERSION as SOURCE_VERSION, unwrap
from .static_contracts import _literal_string, _path, _string
from .value_analysis import _json_data

VERSION = "captured-report-source-chains-1"
POLICY_VERSION = "static-report-claim-policy-v1"
CONTROL_MODEL = "captured-normal-statement-control-v1"
COMMAND_MODEL = "node-structured-execfile-source-contract-v1"
CONSTRUCTION_MODEL = "source-derived-production-construction-v1"
TYPES = frozenset({"guarded_call_sequence", "best_effort_finalization",
    "structured_command_source", "unsupported_method_evidence", "state_guard_sequence",
    "deployment_provider_split", "conditional_delivery_result", "agent_execution_policy"})
_MODELS = frozenset({CONTROL_MODEL, COMMAND_MODEL, CONSTRUCTION_MODEL})
_FUNCTIONS = frozenset({"function_declaration", "generator_function_declaration", "function_expression",
    "generator_function", "arrow_function", "method_definition", "function_item", "closure_expression"})
_ERASED = frozenset({"comment", "line_comment", "block_comment", "type_annotation", "type_arguments",
    "type_parameters", "interface_declaration", "type_alias_declaration", "type_query", "import_type",
    "implements_clause", "function_type"})
_BLOCKS = frozenset({"statement_block", "block"})
_LOOPS = frozenset({"for_statement", "for_in_statement", "while_statement", "do_statement",
    "loop_expression", "for_expression", "while_expression"})
_CONTROL = frozenset({"if_statement", "if_expression", "switch_statement", "match_expression",
    "try_statement", "catch_clause", "finally_clause", "match_arm", *_LOOPS})
_NODE_LIMIT, _FACT_LIMIT, _CALL_LIMIT, _DEPTH = 131072, 8192, 4096, 8


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True,
        separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()


def validate_report_claim(rule: Any) -> None:
    """Accept only data locators and registered conditional source models."""
    _json_data(rule)
    required = {"id", "type", "severity", "sources", "models", "provenance", "applicability"}
    if (not isinstance(rule, dict) or set(rule) != required or not _string(rule["id"])
            or not isinstance(rule["type"], str) or rule["type"] not in TYPES):
        raise ValueError("report_claims require exact data-only source locators and a supported type")
    if not isinstance(rule["severity"], str) or rule["severity"] not in {"info", "low", "medium", "high"}:
        raise ValueError("invalid report claim severity")
    selectors = rule["sources"]
    if not isinstance(selectors, list) or not 1 <= len(selectors) <= 32:
        raise ValueError("report sources require 1..32 declaration locators")
    seen = set()
    for selector in selectors:
        if (not isinstance(selector, dict) or set(selector) != {"role", "file", "symbol"}
                or not _string(selector["role"]) or not _path(selector["file"]) or not _string(selector["symbol"])
                or selector["role"] in seen):
            raise ValueError("source roles contain only unique role and exact file/symbol")
        seen.add(selector["role"])
    models = rule["models"]
    if (not isinstance(models, list) or not models or not all(isinstance(model, str) for model in models) or len(models) != len(set(models))
            or any(model not in _MODELS for model in models) or CONTROL_MODEL not in models):
        raise ValueError("report models require registered normal source control")
    if rule["type"] == "structured_command_source" and COMMAND_MODEL not in models:
        raise ValueError("structured command claims require the explicit Node source contract")
    if rule["type"] == "deployment_provider_split" and CONSTRUCTION_MODEL not in models:
        raise ValueError("deployment claims require source construction, not global target binding")
    minimum = {"structured_command_source": {"loader", "resolver", "executor", "runner"},
        "deployment_provider_split": {"boundary", "bootstrap", "installation", "provider"}}
    if not minimum.get(rule["type"], set()).issubset(seen):
        raise ValueError("missing source role locators for the selected finite report pattern")
    if rule["type"] == "state_guard_sequence" and len(selectors) < 2:
        raise ValueError("state guard comparison requires at least two exact functions")
    provenance = rule["provenance"]
    if (not isinstance(provenance, dict) or set(provenance) - {"authority", "reviewer", "author_approved", "source_doc", "note"}
            or not _string(provenance.get("authority")) or not _string(provenance.get("source_doc"))
            or type(provenance.get("author_approved")) is not bool):
        raise ValueError("report provenance is a label and requires an explicit approval flag")
    applicability = rule["applicability"]
    if (not isinstance(applicability, dict) or set(applicability) - {"kind", "conditions", "counterexamples"}
            or applicability.get("kind") != "conditional" or not isinstance(applicability.get("conditions"), list)
            or not applicability["conditions"] or not all(_string(item) for item in applicability["conditions"])
            or not isinstance(applicability.get("counterexamples", []), list)
            or not all(_string(item) for item in applicability.get("counterexamples", []))):
        raise ValueError("report applicability must retain conditional scope and descriptive counterexamples")


def _field(node: Any, key: str) -> Any:
    return node.child_by_field_name(key) if node is not None else None


def _children(node: Any) -> list[Any]:
    return [child for child in node.named_children if child.type not in _ERASED
        and not child.type.endswith("_type")] if node is not None else []


def _inside(outer: Any, inner: Any) -> bool:
    return bool(outer is not None and inner is not None and outer.start_byte <= inner.start_byte
        and inner.end_byte <= outer.end_byte)


def _ancestors(node: Any):
    while node is not None:
        yield node
        node = node.parent


def _fn(definition: Any) -> Any:
    node = unwrap(definition.value) if definition.value is not None else definition.node
    return node if node is not None and node.type in _FUNCTIONS else None


def _body(node: Any) -> Any:
    body = _field(node, "body")
    if body is None and node is not None and node.type in {"async_block", "gen_block"}:
        body = next((child for child in _children(node) if child.type in _BLOCKS), None)
    return body


def _operand(node: Any) -> Any:
    node = unwrap(node)
    while node is not None and node.type in {"await_expression", "try_expression", "reference_expression"}:
        children = _children(node)
        node = unwrap(_field(node, "value") or _field(node, "argument") or (children[-1] if children else None))
    return node


def _static_key(document: Any, node: Any) -> str | None:
    node = unwrap(node)
    if node is None:
        return None
    if node.type in {"identifier", "property_identifier", "field_identifier", "shorthand_property_identifier"}:
        return document.text(node)
    if node.type in {"string", "string_literal"}:
        return _literal_string(document.text(node))
    return None


class _Analysis:
    def __init__(self, snapshot: GraphSnapshot, rule: dict, sources: SemanticSources):
        self.snapshot, self.rule, self.sources = snapshot, rule, sources
        self.roles: dict[str, tuple[Any, Any, Any]] = {}
        self.source_facts: list[dict] = []
        self.gaps: list[dict] = []
        self.lexicals: dict[str, LexicalBindings] = {}
        self.node_cache: dict[tuple[str, int, bool], list[Any]] = {}
        self.calls_by_role: dict[str, list[dict]] = {}
        self.role_binding_closed: dict[str, bool] = {}
        self.call_nodes: dict[str, tuple[Any, Any, Any]] = {}
        self.operations, self.incomplete = 0, False

    def gap(self, code: str, document: Any = None, node: Any = None, **details: Any) -> dict:
        value = {"code": code, "origin": "unresolved", **details}
        if document is not None and node is not None and document.contains(node):
            value["location"] = document.location(node)
        if value not in self.gaps:
            self.gaps.append(value)
        return value

    def fact(self, kind: str, document: Any, node: Any, **details: Any) -> dict:
        value = {"kind": kind, "origin": "source-derived", "snapshot_id": self.snapshot.id,
            "location": document.location(node), **details}
        value["id"] = _digest({"version": VERSION, **value})[:24]
        if len(self.source_facts) >= _FACT_LIMIT:
            self.incomplete = True
            self.gap("report_fact_budget_exceeded")
        else:
            self.source_facts.append(value)
        return value

    def nodes(self, document: Any, root: Any, *, nested: bool = False) -> list[Any]:
        if root is None:
            return []
        key = (document.source.path, root.id, nested)
        if key in self.node_cache:
            return self.node_cache[key]
        values, pending = [], [root]
        while pending:
            node = pending.pop()
            self.operations += 1
            if self.operations > _NODE_LIMIT:
                self.incomplete = True
                self.gap("report_ast_budget_exceeded", document, node)
                break
            values.append(node)
            if not nested and node != root and node.type in _FUNCTIONS | {"class_declaration", "class", "impl_item"}:
                continue
            pending.extend(reversed(_children(node)))
        self.node_cache[key] = values
        return values

    def lexical(self, document: Any) -> LexicalBindings:
        if document.source.path not in self.lexicals:
            self.lexicals[document.source.path] = LexicalBindings(document)
        return self.lexicals[document.source.path]

    def identity(self, document: Any, node: Any) -> dict:
        if document.kind == "rust":
            # Finite plain binders only; this is not a Rust type/namespace or
            # macro-expansion resolver. Receiver/callee binding stays in CALLS.
            name = document.text(node)
            function = next((parent for parent in _ancestors(node.parent) if parent.type in _FUNCTIONS), None)
            candidates = []
            ancestors = {parent.id for parent in _ancestors(node)}
            def binders(pattern: Any) -> list[Any]:
                if pattern is None:
                    return []
                if pattern.type in {"identifier", "self"}:
                    return [pattern]
                if pattern.type in {"tuple_pattern", "reference_pattern", "mut_pattern", "captured_pattern"}:
                    return [value for child in _children(pattern) if child.type != "mutable_specifier" for value in binders(child)]
                return []
            if function is not None:
                for parameter in _children(_field(function, "parameters")):
                    pattern = _field(parameter, "pattern") or (parameter if parameter.type in {"self_parameter", "identifier"} else None)
                    names = [child for child in self.nodes(document, pattern) if child.type == "self"] if pattern is not None and pattern.type == "self_parameter" else binders(pattern)
                    for binder in names:
                        if document.text(binder) == name:
                            candidates.append((function, parameter, binder, "captured_rust_parameter"))
                for declaration in self.nodes(document, _field(function, "body")):
                    if declaration.type != "let_declaration" or declaration.start_byte > node.start_byte:
                        continue
                    scope = next((parent for parent in _ancestors(declaration.parent) if parent.type in _BLOCKS), None)
                    if scope is None or scope.id not in ancestors:
                        continue
                    for binder in binders(_field(declaration, "pattern")):
                        if document.text(binder) == name:
                            candidates.append((scope, declaration, binder, "captured_rust_local"))
            if candidates:
                # The smallest visible captured lexical scope wins; multiple
                # preceding shadows in that scope retain ambiguity.
                scope_size = min(scope.end_byte - scope.start_byte for scope, _, _, _ in candidates)
                candidates = [value for value in candidates if value[0].end_byte - value[0].start_byte == scope_size]
            if len(candidates) == 1:
                scope, declaration, binder, kind = candidates[0]
                identity = {"file": document.source.path, "source_hash": document.source.hash,
                    "snapshot_id": self.snapshot.id, "declaration_start": declaration.start_byte,
                    "declaration_end": declaration.end_byte, "binder_start": binder.start_byte,
                    "binder_end": binder.end_byte, "scope_start": scope.start_byte, "scope_end": scope.end_byte}
                return {"state": "captured_unique_rust_binder", "declaration_id": _digest({"version": VERSION, **identity}),
                    "declaration_kind": kind, "declaration_location": document.location(declaration),
                    "binder_location": document.location(binder), "identity_scope": "plain captured binder syntax only",
                    "macro_namespace_complete": False, "runtime_value_identity_proven": False}
            return {"state": "captured_rust_reference", "location": document.location(node),
                "text": name, "plain_binder_candidates": len(candidates), "runtime_value_identity_proven": False}
        binding = self.lexical(document).resolve(node)
        return {key: binding.get(key) for key in ("state", "declaration_id", "declaration_kind",
            "declaration_location", "binder_location", "parameter_index", "identity_complete")}

    def expression(self, document: Any, node: Any, depth: int = 0) -> dict:
        node = unwrap(node)
        if node is None:
            return {"kind": "missing"}
        base = {"kind": node.type, "location": document.location(node)}
        if depth >= _DEPTH:
            return {**base, "source_structure_complete": False, "gap": "expression_depth_limit"}
        literal = _literal_string(document.text(node))
        if literal is not None:
            return {**base, "literal": literal}
        raw = document.text(node)
        if node.type in {"true", "false", "boolean_literal"} and raw in {"true", "false"}:
            return {**base, "literal": raw == "true"}
        if node.type in {"number", "integer_literal"}:
            return {**base, "literal_source": raw}
        if node.type in {"identifier", "shorthand_property_identifier", "self"}:
            return {**base, "reference": self.identity(document, node), "name": raw}
        if node.type in {"member_expression", "subscript_expression", "field_expression"}:
            root = _field(node, "object") or _field(node, "value") or (node.named_children[0] if node.named_children else None)
            prop = _field(node, "property") or _field(node, "field") or _field(node, "index")
            return {**base, "object": self.expression(document, root, depth + 1),
                "member": _static_key(document, prop), "member_location": document.location(prop) if prop is not None else None,
                "current_referent_value_proven": False}
        if node.type in {"object", "struct_expression"}:
            return {**base, "construction": self.object(document, node, depth + 1)}
        if node.type in {"array", "array_expression"}:
            return {**base, "items": [self.expression(document, child, depth + 1) for child in _children(node)],
                "runtime_array_value_proven": False}
        if node.type in {"await_expression", "try_expression", "reference_expression", "parenthesized_expression"}:
            return {**base, "operand": self.expression(document, _operand(node), depth + 1)}
        if node.type in {"template_string", "raw_string_literal", "scoped_identifier", "scoped_type_identifier"}:
            return {**base, "source": raw[:4096], "children": [self.expression(document, child, depth + 1)
                for child in _children(node)]}
        if node.type in {"call_expression", "new_expression"}:
            callee = _field(node, "function") or _field(node, "constructor")
            return {**base, "callee_source": document.text(callee), "callee_expression": self.expression(document, callee, depth + 1),
                "arguments": [self.expression(document, child, depth + 1)
                for child in _children(_field(node, "arguments"))], "call_effects_or_result_proven": False}
        if node.type in {"binary_expression", "unary_expression", "assignment_expression", "augmented_assignment_expression"}:
            operator = _field(node, "operator")
            token = document.text(operator) if operator is not None else next((child.type for child in node.children
                if not child.is_named and child.type not in {"(", ")"}), "")
            return {**base, "operator": token, "operands": [self.expression(document, child, depth + 1)
                for child in _children(node)], "runtime_predicate_or_assignment_proven": False}
        if node.type in {"return_expression", "return_statement", "throw_statement"}:
            return {**base, "returned_expression": self.expression(document,
                _field(node, "value") or _field(node, "argument") or next(iter(_children(node)), None), depth + 1),
                "runtime_completion_proven": False}
        return {**base, "source": raw[:4096], "source_truncated": len(raw) > 4096,
            "runtime_value_proven": False}

    def object(self, document: Any, node: Any, depth: int = 0) -> dict:
        fields, parts, complete = {}, [], True
        for member in _children(node):
            if member.type in {"pair", "field_initializer"}:
                key = _static_key(document, _field(member, "key") or _field(member, "field"))
                value = _field(member, "value")
            elif member.type in {"shorthand_property_identifier", "shorthand_field_initializer"}:
                value = next(iter(_children(member)), member)
                key = _static_key(document, value)
            else:
                complete = False
                parts.append({"kind": member.type, "location": document.location(member), "value_unknown": True})
                continue
            if key is None or key == "__proto__" or key in fields:
                complete = False
            item = {"key": key, "value": self.expression(document, value, depth + 1), "location": document.location(member)}
            parts.append(item)
            if key is not None:
                fields[key] = item
        return {"fields": fields, "parts": parts, "fixed_data_source_shape_complete": complete,
            "runtime_object_or_presence_proven": False}

    def branch_context(self, document: Any, node: Any, function: Any) -> list[dict]:
        values = []
        for parent in _ancestors(node.parent):
            if parent == function:
                break
            if parent.type in {"if_statement", "if_expression"}:
                condition = _field(parent, "condition")
                branch = "then" if _inside(_field(parent, "consequence"), node) else "else" if _inside(_field(parent, "alternative"), node) else "condition"
                values.append({"kind": "if", "branch": branch, "condition": self.expression(document, condition),
                    "location": document.location(parent), "condition_truth_proven": False})
            elif parent.type in {"catch_clause", "finally_clause", "match_arm", *_LOOPS}:
                values.append({"kind": parent.type, "location": document.location(parent), "activation_proven": False})
        return list(reversed(values))

    def raw_edge(self, document: Any, call: Any) -> Any:
        owner = document.call_owner(call)
        function = _field(call, "function") or _field(call, "constructor")
        if document.kind == "rust":
            while function is not None and function.type == "generic_function":
                function = _field(function, "function")
            anchor = f"{document.source.path}:{owner}:{call.start_byte}:{call.end_byte}"
            expected = "rust-call:" + hashlib.sha256(anchor.encode()).hexdigest()[:24]
        else:
            version = self.snapshot.stats.get("component_versions", {}).get("typescript", {}).get("analyzer")
            expected = _digest([version, owner, document.source.path, call.start_byte, call.end_byte,
                "new" if call.type == "new_expression" else "call"])[:24]
        edges = [edge for edge in self.sources.edges.get((document.source.path, call.start_point.row + 1, call.start_point.column), [])
            if edge.id == expected and edge.source == owner and edge.expression == document.text(function)[:600]]
        return edges[0] if len(edges) == 1 else None

    def call(self, role: str, document: Any, definition: Any, function: Any, node: Any) -> dict:
        actual_owner = document.call_owner(node)
        owner_defs = document.definition_nodes.get(actual_owner, [])
        owner = owner_defs[0] if len(owner_defs) == 1 else definition
        edge, issues = self.sources.call_binding(node, document, owner)
        raw = self.raw_edge(document, node)
        callee = _field(node, "function") or _field(node, "constructor")
        arguments = _children(_field(node, "arguments"))
        binding = None
        for parent in _ancestors(node.parent):
            if parent.type in _FUNCTIONS:
                break
            if parent.type in {"variable_declarator", "let_declaration"} and _inside(_field(parent, "value"), node):
                binding = parent
                break
        binding_name = _field(binding, "name") or _field(binding, "pattern")
        result_binding = self.identity(document, binding_name) if binding_name is not None else None
        result = self.fact("captured_call_step", document, node, role=role,
            owner_graph_node_id=actual_owner, callee_source=document.text(callee),
            arguments=[self.expression(document, argument) for argument in arguments],
            actual_callee_graph_node_id=edge.target if edge is not None else None,
            authenticated_call_edge_id=edge.id if edge is not None else None,
            captured_site_edge_id=raw.id if raw is not None else None,
            binding_state="authenticated_internal_call" if edge is not None else "external_or_unknown_call",
            captured_resolution=raw.resolution if raw is not None else "source_site_only",
            binding_gaps=issues, branch_context=self.branch_context(document, node, function),
            result_binding_source=result_binding,
            call_is_entire_binding_initializer=_operand(_field(binding, "value")) == node if binding is not None else False,
            callee_activation_proven=False, call_runtime_success_proven=False)
        self.call_nodes[result["id"]] = (document, function, node)
        return result

    def load(self) -> None:
        for selector in self.rule["sources"]:
            document, definition, issues = self.sources.select({key: selector[key] for key in ("file", "symbol")})
            if document is None or definition is None or issues:
                self.gap("report_source_role_unavailable", role=selector["role"], selector=selector, source_gaps=issues)
                continue
            function = _fn(definition)
            if function is None:
                self.gap("report_source_role_not_callable", document, definition.node, role=selector["role"])
                continue
            graph_nodes = self.sources.nodes.get(definition.graph_node_id, [])
            if len(graph_nodes) != 1:
                self.gap("report_source_role_graph_identity_unknown", document, function, role=selector["role"])
                continue
            authenticated, actual, issues = self.sources.definition_for_node(graph_nodes[0])
            if authenticated is not document or actual is not definition or issues:
                graph = graph_nodes[0]
                # A fully parsed, exact saved body can provide source-only
                # counterevidence even if macro/conditional binding makes its
                # graph declaration unsuitable as a unique runtime callee.
                # No CALLS or active declaration is repaired by this fallback.
                source_only = (graph.file == document.source.path and graph.line == function.start_point.row + 1
                    and graph.end_line == function.end_point.row + 1
                    and document.definition_for_ast(definition.node) is definition
                    and not any(graph.metadata.get(key) for key in {"duplicate_definition", "multiple_module_contexts",
                        "module_identity_collision", "declaration_only"}))
                self.gap("report_source_role_graph_binding_limited", document, function,
                    role=selector["role"], source_gaps=issues, source_body_available=source_only,
                    declaration_binding_limits={key: graph.metadata.get(key) for key in {
                        "conditional_definition", "attribute_macros_unknown", "binding_uncertain"} if graph.metadata.get(key)})
                if not source_only:
                    continue
                self.role_binding_closed[selector["role"]] = False
            else:
                self.role_binding_closed[selector["role"]] = True
            self.roles[selector["role"]] = document, definition, function
            self.fact("report_source_role", document, function, role=selector["role"],
                graph_node_id=definition.graph_node_id, function_kind=function_kind(document, function),
                source_selector=selector, source_graph_binding_closed=self.role_binding_closed[selector["role"]])
            body = _field(function, "body")
            nodes = self.nodes(document, body)
            calls = [node for node in nodes if node.type in {"call_expression", "new_expression"}]
            if len(calls) > _CALL_LIMIT:
                self.incomplete = True
                self.gap("report_call_budget_exceeded", document, function, role=selector["role"])
            self.calls_by_role[selector["role"]] = [self.call(selector["role"], document, definition, function, node)
                for node in calls[:_CALL_LIMIT]]

    def direct_block(self, node: Any, function: Any) -> tuple[Any, Any] | None:
        body = _body(function)
        current = node
        while current is not None and current != body:
            if current.parent == body:
                return body, current
            current = current.parent
        return None

    def sequence(self, role: str, *, region: Any = None) -> dict:
        document, definition, function = self.roles[role]
        function = region if region is not None else function
        body = _body(function)
        calls = [call for call in self.calls_by_role[role] if _inside(body, self.call_nodes[call["id"]][2])]
        steps, guards, writes, conditions, opaque, links = [], [], [], [], [], []
        for child in _children(body):
            ids = [call["id"] for call in calls if _inside(child, self.call_nodes[call["id"]][2])]
            if ids:
                step = self.fact("direct_statement_call_step", document, child, role=role,
                    call_ids=ids, source_order_index=len(steps), statement_kind=child.type,
                    conditional_normal_reaching_only=True)
                steps.append(step)
            if child.type in _LOOPS | {"switch_statement", "match_expression", "try_statement"}:
                opaque.append(document.location(child))
        for node in self.nodes(document, body):
            if node.type in {"if_statement", "if_expression"}:
                condition = _field(node, "condition")
                consequence = _field(node, "consequence")
                alternate = _field(node, "alternative")
                branches = []
                for label, branch in (("then", consequence), ("else", alternate)):
                    if branch is None:
                        continue
                    returns = [part for part in self.nodes(document, branch) if part.type in {"return_statement", "return_expression", "throw_statement", "break_statement", "continue_statement"}]
                    branches.append({"branch": label, "abrupt_source_expressions": [self.expression(document, part) for part in returns],
                        "branch_all_paths_abrupt_proven": self.simple_abrupt(branch),
                        "call_ids": [call["id"] for call in calls if _inside(branch, self.call_nodes[call["id"]][2])]})
                record = self.fact("source_guard_and_abrupt_branch", document, node, role=role,
                    condition=self.expression(document, condition), branches=branches,
                    branch_context=self.branch_context(document, node, function), runtime_predicate_proven=False)
                conditions.append(record)
                reference_ids = set()
                pending = [record["condition"]]
                while pending:
                    value = pending.pop()
                    if isinstance(value, dict):
                        reference = value.get("reference", {})
                        if reference.get("state") == "unique" and reference.get("declaration_id"):
                            reference_ids.add(reference["declaration_id"])
                        pending.extend(value.values())
                    elif isinstance(value, list):
                        pending.extend(value)
                for call in calls:
                    binding = call.get("result_binding_source") or {}
                    if (call["call_is_entire_binding_initializer"] and binding.get("declaration_id") in reference_ids
                            and call["location"]["end_byte"] <= node.start_byte):
                        links.append(self.fact("call_result_binding_guard_source", document, node, role=role,
                            call_fact_id=call["id"], guard_fact_id=record["id"], result_binding_id=binding["declaration_id"],
                            source_reference_connected=True, actual_result_stability_or_predicate_truth_proven=False))
                if self.direct_block(node, function) and self.direct_block(node, function)[1] == node:
                    subsequent = [call["id"] for call in calls if self.direct_block(self.call_nodes[call["id"]][2], function)
                        and self.direct_block(self.call_nodes[call["id"]][2], function)[1].start_byte > node.end_byte]
                    excluded = [branch["branch"] for branch in branches if branch["branch_all_paths_abrupt_proven"]]
                    if excluded and subsequent:
                        guards.append(self.fact("normal_reaching_excludes_abrupt_guard_branch", document, node,
                            role=role, guard_fact_id=record["id"], excluded_branches=excluded,
                            subsequent_call_ids=subsequent, model_id=CONTROL_MODEL,
                            statement_order_proven=True, predicate_truth_proven=False,
                            activation_or_termination_proven=False))
            if node.type in {"assignment_expression", "augmented_assignment_expression"}:
                left, right = _field(node, "left"), _field(node, "right")
                writes.append(self.fact("ordered_source_assignment_attempt", document, node, role=role,
                    left=self.expression(document, left), right=self.expression(document, right),
                    branch_context=self.branch_context(document, node, function), write_runtime_success_proven=False))
            if node.type == "try_expression":
                self.fact("result_try_normal_continuation", document, node, role=role,
                    operand=self.expression(document, _operand(node)), model_id=CONTROL_MODEL,
                    error_case_exits_current_function_conditionally=True, actual_result_or_execution_proven=False)
        order = []
        # Statement ordering is not ordering of sibling/nested call arguments.
        for first, second in zip(steps, steps[1:]):
            if first["location"]["end_byte"] <= second["location"]["start_byte"]:
                order.append(self.fact("conditional_direct_statement_order", document,
                    next(child for child in _children(body) if child.start_byte == second["location"]["start_byte"]),
                    role=role, before_step_id=first["id"], after_step_id=second["id"], model_id=CONTROL_MODEL,
                    conditions=["both direct statements normally reached in the same invocation",
                        "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"],
                    all_paths_reach_next_proven=False))
        return {"role": role, "steps": steps, "orders": order, "guards": guards,
            "conditions": conditions, "call_result_guard_source_links": links,
            "assignment_attempts": writes, "opaque_direct_control_regions": opaque,
            "source_region_location": document.location(function),
            "region_kind": function.type, "future_or_callback_activation_proven": False,
            "all_function_paths_or_effects_accounted": False}

    def simple_abrupt(self, node: Any) -> bool:
        if node is None:
            return False
        if node.type in {"return_statement", "return_expression", "throw_statement", "break_statement", "continue_statement"}:
            return True
        children = _children(node)
        return node.type in _BLOCKS | {"expression_statement"} and len(children) == 1 and self.simple_abrupt(children[0])

    def best_effort(self) -> dict:
        candidates = []
        for role, (document, definition, function) in self.roles.items():
            for node in self.nodes(document, _field(function, "body")):
                if node.type != "try_statement":
                    continue
                handler = _field(node, "handler") or next((child for child in _children(node) if child.type == "catch_clause"), None)
                finalizer = _field(node, "finalizer") or next((child for child in _children(node) if child.type == "finally_clause"), None)
                catch_body = _field(handler, "body")
                body = _field(node, "body")
                empty = handler is not None and not _children(catch_body) and finalizer is None
                calls = [call for call in self.calls_by_role[role] if _inside(body, self.call_nodes[call["id"]][2])]
                if not calls:
                    continue
                candidates.append(self.fact("caught_call_failure_scope", document, node, role=role,
                    call_ids=[call["id"] for call in calls], catch_location=document.location(handler) if handler else None,
                    catch_body_location=document.location(catch_body) if catch_body else None,
                    failure_swallowed_by_empty_catch_source=empty, finally_present=finalizer is not None,
                    enclosing_branch_context=self.branch_context(document, node, function),
                    runtime_failure_or_finalization_success_proven=False))
        grouped = {}
        for record in candidates:
            if not record["failure_swallowed_by_empty_catch_source"]:
                continue
            for call_id in record["call_ids"]:
                call = next(item for items in self.calls_by_role.values() for item in items if item["id"] == call_id)
                if call["actual_callee_graph_node_id"]:
                    grouped.setdefault(call["actual_callee_graph_node_id"], []).append(record["id"])
        repeats = {key: values for key, values in grouped.items() if len(set(values)) >= 2}
        if not repeats:
            self.gap("best_effort_repeated_authenticated_target_not_found")
        return {"caught_scopes": candidates, "repeated_authenticated_targets": repeats,
            "scoped_source_supported": bool(repeats) and not self.incomplete,
            "audit_subject_equivalence_to_other_systems_proven": False}

    def import_binding(self, document: Any, local: str) -> dict | None:
        candidates = []
        for node in self.nodes(document, document.tree.root_node):
            if node.type != "import_statement":
                continue
            module = _literal_string(document.text(_field(node, "source")))
            for spec in self.nodes(document, node, nested=True):
                if spec.type != "import_specifier":
                    continue
                name, alias = _field(spec, "name"), _field(spec, "alias")
                if document.text(alias or name) == local:
                    candidates.append({"module": module, "imported": document.text(name),
                        "location": document.location(spec)})
        return candidates[0] if len(candidates) == 1 else None

    def imported_literal_source(self, document: Any, reference: Any) -> dict | None:
        if reference is None or reference.type != "identifier":
            return None
        binding = self.lexical(document).resolve(reference)
        record = self.import_binding(document, document.text(reference))
        if (binding.get("state") != "unique" or binding.get("declaration_kind") != "import" or not record
                or not record.get("module", "").startswith(".")):
            return None
        target = posixpath.normpath(posixpath.join(posixpath.dirname(document.source.path), record["module"]))
        if target.startswith("../") or target.startswith("/"):
            return None
        candidates = [target]
        if target.endswith((".js", ".mjs", ".cjs")):
            stem = target.rsplit(".", 1)[0]
            candidates.extend([stem + ".ts", stem + ".tsx"])
        present = [candidate for candidate in candidates if candidate in self.sources.files]
        if len(present) != 1:
            return None
        target_document, target_definition, issues = self.sources.select({"file": present[0], "symbol": record["imported"]})
        if target_document is None or target_definition is None or issues or target_definition.callable:
            return None
        value = unwrap(target_definition.value)
        if value is None:
            return None
        literal = _literal_string(target_document.text(value))
        declaration = target_definition.node
        parent = declaration.parent
        if literal is None or parent is None or not any(child.type == "const" for child in parent.children):
            return None
        exported = next((ancestor for ancestor in _ancestors(declaration.parent) if ancestor.type == "export_statement"), None)
        if exported is None:
            return None
        return self.fact("captured_imported_literal_source", target_document, declaration,
            importing_reference_location=document.location(reference), import_source=record,
            source_literal=literal, runtime_module_resolution_verified=False)

    def execfile_alias(self, document: Any, callee: Any) -> dict:
        callee = unwrap(callee)
        if callee is None or callee.type != "identifier":
            return {"supported": False, "gap": "execfile_callee_not_identifier"}
        name = document.text(callee)
        direct = self.import_binding(document, name)
        identity = self.lexical(document).resolve(callee)
        if (direct and identity.get("state") == "unique" and identity.get("declaration_kind") == "import"
                and direct["module"] == "node:child_process" and direct["imported"] == "execFile"):
            return {"supported": True, "source_kind": "captured_execfile_import", "import": direct,
                "binding": self.identity(document, callee), "runtime_standard_api_verified": False}
        bindings = [node for node in self.nodes(document, document.tree.root_node)
            if node.type == "variable_declarator" and document.text(_field(node, "name")) == name]
        if len(bindings) != 1:
            return {"supported": False, "gap": "execfile_alias_declaration_not_unique"}
        declaration = bindings[0]
        initializer = unwrap(_field(declaration, "value"))
        if initializer is None or initializer.type != "call_expression":
            return {"supported": False, "gap": "execfile_alias_initializer_unknown"}
        wrapper = unwrap(_field(initializer, "function"))
        args = _children(_field(initializer, "arguments"))
        if wrapper is None or wrapper.type != "identifier" or len(args) != 1 or args[0].type != "identifier":
            return {"supported": False, "gap": "execfile_promisify_source_unknown"}
        wrapped = self.import_binding(document, document.text(args[0]))
        adapter = self.import_binding(document, document.text(wrapper))
        wrapped_identity = self.lexical(document).resolve(args[0])
        adapter_identity = self.lexical(document).resolve(wrapper)
        binding = self.lexical(document).resolve(callee)
        initializer_identity = self.lexical(document).resolve(_field(declaration, "name"))
        same = (binding.get("state") == "unique" and initializer_identity.get("state") == "unique"
            and binding.get("declaration_id") == initializer_identity.get("declaration_id")
            and binding.get("declaration_kind") == "const")
        supported = bool(same and wrapped and adapter and wrapped["module"] == "node:child_process"
            and wrapped["imported"] == "execFile" and adapter["module"] == "node:util" and adapter["imported"] == "promisify"
            and all(item.get("state") == "unique" and item.get("declaration_kind") == "import"
                for item in (wrapped_identity, adapter_identity)))
        return {"supported": supported, "source_kind": "captured_promisified_execfile_import",
            "declaration_location": document.location(declaration), "execfile_import": wrapped,
            "promisify_import": adapter, "binding": self.identity(document, callee),
            "model_id": COMMAND_MODEL, "runtime_standard_api_verified": False}

    def command_source(self) -> dict:
        result = {"loaders": [], "lookups": [], "executions": [], "internal_role_calls": [],
            "argument_reference_transfers": [], "runtime_command_executed": False,
            "expected_evidence_noninterference_proven": False}
        role_nodes = {definition.graph_node_id: role for role, (_, definition, _) in self.roles.items()}
        for role, calls in self.calls_by_role.items():
            document, definition, function = self.roles[role]
            for call in calls:
                _, _, node = self.call_nodes[call["id"]]
                target_role = role_nodes.get(call["actual_callee_graph_node_id"])
                if target_role:
                    relation = self.fact("authenticated_report_role_call", document, node,
                        from_role=role, to_role=target_role, call_fact_id=call["id"],
                        actual_callee_graph_node_id=call["actual_callee_graph_node_id"])
                    result["internal_role_calls"].append(relation)
                    target_document, _, target_function = self.roles[target_role]
                    formals = _children(_field(target_function, "parameters"))
                    for index, (argument, formal) in enumerate(zip(_children(_field(node, "arguments")), formals)):
                        actual_arguments = _children(_field(node, "arguments"))
                        if any(item.type in {"spread_element", "rest_pattern"} for item in actual_arguments[:index + 1]):
                            self.gap("report_argument_formal_spread_mapping_unknown", document, argument)
                            continue
                        binder = unwrap(_field(formal, "pattern") or _field(formal, "name") or formal)
                        identity = self.identity(target_document, binder) if binder is not None else {}
                        result["argument_reference_transfers"].append(self.fact("authenticated_role_argument_formal_source", document, argument,
                            from_role=role, to_role=target_role, argument_index=index,
                            argument=self.expression(document, argument), formal=identity,
                            formal_location=target_document.location(formal), role_call_fact_id=relation["id"],
                            argument_value_field_or_activation_proven=False))
                callee = _field(node, "function") or _field(node, "constructor")
                args = _children(_field(node, "arguments"))
                if role == "resolver":
                    descriptor = self.expression(document, callee)
                    if descriptor.get("member") is not None:
                        result["lookups"].append(self.fact("captured_policy_member_lookup", document, node,
                            callee=descriptor, arguments=call["arguments"],
                            standard_map_behavior_assumed=False, resolved_result_field_value_proven=False))
                if role not in {"loader", "executor"}:
                    continue
                alias = self.execfile_alias(document, callee)
                if not alias.get("supported"):
                    continue
                if role == "loader":
                    prefix_sources = []
                    if len(args) >= 2 and args[1].type == "array":
                        for item in _children(args[1]):
                            if item.type == "template_string":
                                fragments = [child for child in _children(item) if child.type == "string_fragment"]
                                substitutions = [child for child in _children(item) if child.type == "template_substitution"]
                                imported = [self.imported_literal_source(document, part) for substitution in substitutions
                                    for part in _children(substitution) if part.type == "identifier"]
                                prefix_sources.append({"location": document.location(item),
                                    "literal_fragments": [document.text(fragment) for fragment in fragments],
                                    "imported_literal_sources": [value for value in imported if value is not None],
                                    "template_runtime_value_proven": False})
                    result["loaders"].append(self.fact("captured_trusted_command_policy_read", document, node,
                        execfile_alias=alias, arguments=call["arguments"],
                        argument_template_sources=prefix_sources,
                        source_command_is_git_show=(len(call["arguments"]) >= 2
                            and call["arguments"][0].get("literal") == "git"
                            and bool(call["arguments"][1].get("items"))
                            and call["arguments"][1]["items"][0].get("literal") == "show"),
                        source_revision_prefix_is_head=any(item["literal_fragments"] == ["HEAD:"]
                            and len(item["imported_literal_sources"]) == 1 for item in prefix_sources),
                        command_origin="source arguments of the registered Node execFile contract",
                        git_revision_or_policy_authenticity_runtime_verified=False))
                elif len(args) >= 3:
                    options_node = unwrap(args[2])
                    options = self.object(document, options_node) if options_node is not None and options_node.type == "object" else {}
                    first, second = self.expression(document, args[0]), self.expression(document, args[1])
                    first_ref = first.get("object", {}).get("reference", {})
                    second_ref = second.get("object", {}).get("reference", {})
                    same = (first_ref.get("state") == "unique" and second_ref.get("state") == "unique"
                        and first_ref.get("declaration_id") == second_ref.get("declaration_id")
                        and first_ref.get("declaration_kind") == "parameter")
                    shell = options.get("fields", {}).get("shell", {}).get("value", {}).get("literal")
                    result["executions"].append(self.fact("structured_execfile_parameter_source", document, node,
                        execfile_alias=alias, executable_source=first, arguments_source=second,
                        same_parameter_field_source=same, shell_literal_source=shell,
                        options=options, shell_false_source_confirmed=options.get("fixed_data_source_shape_complete", False) and shell is False,
                        runtime_standard_api_or_command_result_proven=False))
        # Role links authenticate calls; they do not imply heap stability or
        # source fields survive arbitrary code between those calls.
        good_exec = any(item["same_parameter_field_source"] and item["shell_false_source_confirmed"] for item in result["executions"])
        good_loader = any(item["source_command_is_git_show"] and item["source_revision_prefix_is_head"] for item in result["loaders"])
        good_lookup = any(item["callee"].get("member") == "get"
            and item["callee"].get("object", {}).get("reference", {}).get("declaration_kind") == "parameter"
            for item in result["lookups"])
        links = {(item["from_role"], item["to_role"]) for item in result["internal_role_calls"]}
        good_links = ("runner", "loader") in links and ("runner", "resolver") in links
        reachable, pending = {"runner"}, ["runner"]
        while pending:
            current = pending.pop()
            for left, right in links:
                if left == current and right not in reachable:
                    reachable.add(right)
                    pending.append(right)
        result["captured_role_call_path_to_executor"] = "executor" in reachable
        result["scoped_source_supported"] = bool(good_loader and good_lookup and good_exec and good_links
            and "executor" in reachable and not self.incomplete)
        self.gap("structured_command_intermediate_values_and_external_effects_not_fully_proven",
            source_only=True, runtime_or_full_noninterference_proven=False)
        return result

    def emission(self) -> dict:
        records, collections, memberships, consumer_guards, assignments = [], [], [], [], []
        documents = {document.source.path: document for document, _, _ in self.roles.values()}
        for document in documents.values():
            for declaration in self.nodes(document, document.tree.root_node):
                if declaration.type != "variable_declarator":
                    continue
                initializer = unwrap(_field(declaration, "value"))
                name = _field(declaration, "name")
                if initializer is None or initializer.type != "new_expression" or name is None or name.type != "identifier":
                    continue
                arguments = _children(_field(initializer, "arguments"))
                if len(arguments) != 1 or arguments[0].type != "array":
                    continue
                values = [_literal_string(document.text(child)) for child in _children(arguments[0])]
                if not values or any(value is None for value in values):
                    continue
                binding = self.identity(document, name)
                if binding.get("state") != "unique" or binding.get("declaration_kind") != "const":
                    continue
                collections.append(self.fact("captured_fixed_string_collection_source", document, declaration,
                    constructor_source=document.text(_field(initializer, "constructor")),
                    binding=binding, literal_members=values, runtime_collection_contents_or_membership_proven=False))
        for role, (document, definition, function) in self.roles.items():
            for node in self.nodes(document, _field(function, "body")):
                if node.type in {"if_statement", "if_expression"}:
                    condition = _field(node, "condition")
                    consumer_guards.append(self.fact("record_marker_consumption_guard_source", document, node,
                        role=role, condition=self.expression(document, condition),
                        actual_marker_consumer_result_proven=False))
                    for child in self.nodes(document, condition):
                        if child.type != "call_expression":
                            continue
                        callee = self.expression(document, _field(child, "function"))
                        root = callee.get("object", {}).get("reference", {})
                        matching = [item for item in collections if item["binding"].get("declaration_id") == root.get("declaration_id")
                            and root.get("state") == "unique"]
                        if matching:
                            memberships.append(self.fact("captured_collection_condition_source", document, child,
                                role=role, callee=callee, arguments=[self.expression(document, argument)
                                    for argument in _children(_field(child, "arguments"))],
                                collection_fact_ids=[item["id"] for item in matching],
                                conditional_branch_location=document.location(node), standard_collection_truth_proven=False))
                elif node.type in {"assignment_expression", "augmented_assignment_expression"}:
                    assignments.append(self.fact("record_marker_assignment_attempt", document, node, role=role,
                        left=self.expression(document, _field(node, "left")), right=self.expression(document, _field(node, "right")),
                        branch_context=self.branch_context(document, node, function), assignment_success_proven=False))
        for role, (document, definition, function) in self.roles.items():
            for call in self.calls_by_role[role]:
                _, _, node = self.call_nodes[call["id"]]
                for arg in _children(_field(node, "arguments")):
                    arg = unwrap(arg)
                    if arg is None or arg.type != "object":
                        continue
                    payload = self.object(document, arg)
                    flags = {key: item["value"]["literal"] for key, item in payload["fields"].items()
                        if type(item["value"].get("literal")) is bool}
                    if not flags:
                        continue
                    context = self.branch_context(document, node, function)
                    records.append(self.fact("conditional_structured_record_emission", document, node, role=role,
                        call_fact_id=call["id"], marker_fields=flags, payload=payload, branch_context=context,
                        marker_fields_are_explicit_definition_source_only=True,
                        marker_values_at_runtime_or_argument_endpoint_proven=False,
                        record_persisted_or_marker_consumer_proven=False))
        if not records:
            self.gap("structured_emission_marker_not_found")
        true_keys = {key for record in records for key, value in record["marker_fields"].items() if value is True}
        consumers = [record for record in assignments if record["left"].get("member") in true_keys
            and record["right"].get("literal") is True]
        if not memberships:
            self.gap("unsupported_method_source_collection_condition_missing")
        if not consumers:
            self.gap("record_marker_consumer_assignment_not_connected")
        self.gap("structured_record_markers_do_not_prove_all_input_retention_or_persistence", source_only=True)
        return {"record_emissions": records, "fixed_string_collection_sources": collections,
            "source_collection_conditions": memberships, "marker_consumption_guard_sources": consumer_guards,
            "marker_assignment_attempts": assignments, "connected_true_marker_assignments": consumers,
            "scoped_source_supported": bool(records and memberships and consumers) and not self.incomplete,
            "marker_field_business_meaning_inferred": False, "silent_drop_for_all_inputs_excluded": False}

    def state_guards(self) -> dict:
        sequences = {role: self.sequence(role) for role in self.roles}
        shared: dict[str, list[dict]] = {}
        predicates = []
        for role, (document, definition, function) in self.roles.items():
            body = _field(function, "body")
            calls = self.calls_by_role[role]
            direct = [call for call in calls if self.direct_block(self.call_nodes[call["id"]][2], function)
                and not call["branch_context"]]
            if direct:
                first = min(direct, key=lambda item: (item["location"]["start_byte"], item["location"]["end_byte"]))
                if first["actual_callee_graph_node_id"]:
                    shared.setdefault(first["actual_callee_graph_node_id"], []).append({"role": role,
                        "call_fact_id": first["id"], "location": first["location"]})
            for node in self.nodes(document, body, nested=True):
                if node.type in {"macro_invocation", "binary_expression", "unary_expression"}:
                    scope = next((parent for parent in _ancestors(node.parent) if parent.type in _FUNCTIONS), function)
                    predicates.append(self.fact("state_selection_predicate_source", document, node, role=role,
                        expression=self.expression(document, node),
                        nested_predicate_callable=scope != function, callback_activation_proven=False,
                        macro_expansion_or_iterator_effects_proven=False))
        repeated = {target: sites for target, sites in shared.items() if len({site["role"] for site in sites}) >= 2}
        if not repeated:
            self.gap("repeated_first_authenticated_guard_call_not_found")
        self.gap("iterator_selection_and_macro_runtime_semantics_not_fully_proven", source_only=True)
        return {"sequences": sequences, "repeated_first_callee": repeated,
            "selection_predicate_sources": predicates,
            "scoped_source_supported": bool(repeated and predicates) and not self.incomplete,
            "all_active_states_or_attempts_proven": False}

    def deployment(self) -> dict:
        boundary_document, _, boundary_function = self.roles.get("boundary", (None, None, None))
        returns = []
        if boundary_document is not None:
            for node in self.nodes(boundary_document, _field(boundary_function, "body")):
                if node.type in {"return_expression", "return_statement", "call_expression"}:
                    returns.append(self.fact("boundary_result_source", boundary_document, node,
                        expression=self.expression(boundary_document, node), runtime_result_proven=False))
        constructions, member_writes, argument_sources = [], [], []
        for role in {"bootstrap", "installation", "provider"} & self.roles.keys():
            document, definition, function = self.roles[role]
            for call in self.calls_by_role[role]:
                _, _, node = self.call_nodes[call["id"]]
                callee = _field(node, "function") or _field(node, "constructor")
                constructions.append(self.fact("production_construction_call_source", document, node, role=role,
                    call_fact_id=call["id"], callee=self.expression(document, callee), arguments=call["arguments"],
                    actual_callee_graph_node_id=call["actual_callee_graph_node_id"],
                    model_id=CONSTRUCTION_MODEL, global_receiver_dispatch_proven=False))
            for node in self.nodes(document, _field(function, "body")):
                if node.type == "assignment_expression":
                    member_writes.append(self.fact("provider_installation_assignment_source", document, node, role=role,
                        left=self.expression(document, _field(node, "left")), right=self.expression(document, _field(node, "right")),
                        runtime_installed_value_proven=False))
        # Keeping each deployment's source distinct is itself useful negative
        # counterevidence to inferring absence from one unsupported boundary.
        supported = bool(returns and any(item["role"] == "bootstrap" for item in constructions)
            and any(item["role"] == "installation" for item in member_writes)
            and any(item["role"] == "provider" for item in constructions))
        self.gap("deployment_candidate_chain_not_global_dispatch_or_credential_availability",
            source_only=True, full_provider_flow_proven=False)
        return {"boundary_results": returns, "production_constructions": constructions,
            "installation_assignments": member_writes, "argument_sources": argument_sources,
            "scoped_source_supported": supported and not self.incomplete,
            "deployments_or_provider_implementations_equivalent": False,
            "unsupported_boundary_implies_project_capability_absent": False}

    def analyze(self) -> dict:
        self.load()
        if self.rule["type"] == "conditional_delivery_result":
            from .report_delivery_analysis import analyze_pattern
            pattern = analyze_pattern(self)
        elif self.rule["type"] == "agent_execution_policy":
            from .report_agent_policy_analysis import analyze_pattern
            pattern = analyze_pattern(self)
        elif self.rule["type"] == "best_effort_finalization":
            pattern = self.best_effort()
        elif self.rule["type"] == "structured_command_source":
            pattern = self.command_source()
        elif self.rule["type"] == "unsupported_method_evidence":
            pattern = self.emission()
        elif self.rule["type"] == "state_guard_sequence":
            pattern = self.state_guards()
        elif self.rule["type"] == "deployment_provider_split":
            pattern = self.deployment()
        else:
            sequences = {role: self.sequence(role) for role in self.roles}
            nested = []
            for role, (document, definition, function) in self.roles.items():
                for node in self.nodes(document, _body(function)):
                    if node.type not in {"async_block", "gen_block"}:
                        continue
                    nested.append(self.fact("deferred_source_region_sequence", document, node,
                        role=role, sequence=self.sequence(role, region=node),
                        conditions=["this deferred captured body is activated and the recorded statements are reached normally"],
                        body_activation_proven=False, future_fulfillment_proven=False,
                        nested_calls_promoted_to_resolved=False))
            pattern = {"sequences": sequences, "nested_source_regions": nested,
                "scoped_source_supported": bool(sequences) and (any(value["orders"] for value in sequences.values())
                    or any(value["sequence"]["orders"] for value in nested)) and not self.incomplete}
        all_sources = len(self.roles) == len(self.rule["sources"])
        source_structure = bool(all_sources and pattern.get("scoped_source_supported") and not self.incomplete)
        bindings_closed = all_sources and all(self.role_binding_closed.values())
        supported = source_structure and bindings_closed
        return {"version": VERSION, "policy_version": POLICY_VERSION,
            "snapshot_id": self.snapshot.id, "source_hash": self.snapshot.source_hash,
            "policy_hash": self.snapshot.policy_hash, "contract_hash": _digest(self.rule),
            "claim_type": self.rule["type"], "source_facts": self.source_facts,
            "pattern": pattern, "analysis_gaps": self.gaps,
            "scope": {"selected_definitions": self.rule["sources"], "source_role_count": len(self.roles),
                "required_source_role_count": len(self.rule["sources"]), "all_selected_sources_authenticated": all_sources,
                "all_selected_source_graph_bindings_closed": bindings_closed,
                "direct_bodies_exclude_nested_callable_execution": True,
                "nested_state_predicates_are_source_only": True, "whole_repository_audited": False,
                "original_report_text_consumed_as_evidence": False},
            "assessment": {"state": "scoped_source_relations_supported" if supported else "partial_source_relations" if self.source_facts else "unknown",
                "scoped_source_supported": supported, "captured_source_structure_supported": source_structure,
                "normal_control_model_registered": CONTROL_MODEL in self.rule["models"],
                "runtime_verified": False, "full_functionality_proven": False,
                "whole_report_reproduced": False, "original_five_goal_acceptance_computed": False},
            "trusted_models": [{"origin": "trusted-model", "id": model, "runtime_verified": False,
                "conditions": ["only recorded captured source expressions and conditional normal reaching are interpreted",
                    "opaque calls, actual field values, physical effects and all-function termination remain unproved"]}
                for model in self.rule["models"]],
            "policy_declarations": {"origin": "policy-declared", "provenance": self.rule["provenance"],
                "applicability": self.rule["applicability"], "descriptive_counterexamples_are_computed_evidence": False},
            "component_versions": {"report_chains": VERSION, "semantic_sources": SOURCE_VERSION, "lexical_bindings": LEXICAL_VERSION},
            "budgets": {"operations": self.operations, "operation_limit": _NODE_LIMIT,
                "fact_limit": _FACT_LIMIT, "incomplete": self.incomplete},
            "target_executed": False, "target_tests_run": False, "target_build_run": False}


def _finding(snapshot: GraphSnapshot, rule: dict, details: dict) -> Finding:
    fingerprint = _digest({"version": VERSION, "policy_version": POLICY_VERSION,
        "project": snapshot.project_id, "rule": rule})
    node_set, edge_set = {node.id for node in snapshot.nodes}, {edge.id for edge in snapshot.edges}
    node_ids = sorted({fact.get(key) for fact in details.get("source_facts", [])
        for key in ("graph_node_id", "actual_callee_graph_node_id", "owner_graph_node_id")} & node_set)
    edge_ids = sorted({fact.get(key) for fact in details.get("source_facts", [])
        for key in ("authenticated_call_edge_id", "captured_site_edge_id")} & edge_set)
    evidence = Evidence(_digest({"snapshot": snapshot.id, "fingerprint": fingerprint, "details": details})[:24],
        "static_report_chain_analysis", "保存源码的架构主链、保护和反证关系；结论限所选正常源控制范围。",
        [fact["location"] for fact in details.get("source_facts", []) if fact.get("location")], node_ids, edge_ids, details)
    assessment = details.get("assessment", {})
    return Finding(_digest({"snapshot": snapshot.id, "fingerprint": fingerprint})[:24], "static_report_claim",
        rule.get("severity", "info"), "uncertain", "架构报告源码链关系", "机器抽取所选主链、守卫、构造及反证；未审范围和未知保持。",
        node_ids, edge_ids, [evidence], rule.get("id", "invalid-report-claim"), fingerprint, snapshot.id,
        {"report_chain_version": VERSION, "claim_type": rule.get("type"), "assessment": assessment,
            "source_fact_count": len(details.get("source_facts", [])), "source_fact_counts": dict(sorted(Counter(
                fact["kind"] for fact in details.get("source_facts", [])).items())),
            "original_five_goal_acceptance_computed": False, "whole_report_reproduced": False,
            "runtime_verified": False})


def analyze_report_claims(snapshot: GraphSnapshot, rules: list[dict]) -> list[Finding]:
    """Generate report-chain findings solely from authenticated saved source."""
    if not isinstance(rules, list):
        return [_finding(snapshot, {}, {"source_facts": [], "analysis_gaps": [{"code": "invalid_report_claims_array"}],
            "assessment": {"state": "unknown", "scoped_source_supported": False}})]
    counts = Counter(rule.get("id") for rule in rules if isinstance(rule, dict) and isinstance(rule.get("id"), str))
    sources = SemanticSources(snapshot)
    results = []
    for rule in rules:
        safe = rule if isinstance(rule, dict) else {}
        try:
            validate_report_claim(rule)
            if counts[rule["id"]] != 1:
                raise ValueError("duplicate report claim id")
            details = _Analysis(snapshot, rule, sources).analyze()
        except (ValueError, TypeError, KeyError, AttributeError, RecursionError, OverflowError) as error:
            details = {"version": VERSION, "snapshot_id": snapshot.id, "source_facts": [],
                "analysis_gaps": [{"code": "report_claim_analysis_unknown", "origin": "unresolved", "reason": str(error)[:400]}],
                "assessment": {"state": "unknown", "scoped_source_supported": False,
                    "runtime_verified": False, "whole_report_reproduced": False}}
        results.append(_finding(snapshot, safe, details))
    return results
