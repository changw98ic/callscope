"""Finite, authenticated source operations for responsibility explanations.

Selectors and old Finding/Evidence IDs provide navigation context only.  The
operations themselves are computed from captured CST, lexical binders and
existing call bindings.  No directory or function name is a responsibility
classifier; opaque methods are never promoted to known persistence effects.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import json
from types import SimpleNamespace
from typing import Any

from .lexical_bindings import LexicalBindings, VERSION as LEXICAL_VERSION
from .message_identity_relations import _Messages, VERSION as FIELD_SOURCE_VERSION
from .report_chain_analysis import _Analysis, VERSION as CALL_SOURCE_VERSION
from .semantic_sources import SemanticSources, VERSION as SOURCE_VERSION, unwrap
from .static_contracts import _literal_string

VERSION = "captured-responsibility-source-operations-1"
MODEL = "finite-captured-responsibility-operations-v1"
OPERATION_KINDS = frozenset({"record_construction", "record_field_projection", "record_copy_projection",
    "field_write", "call_argument_transfer", "protocol_literal_field", "guard_rejection", "return_transfer",
    "normal_source_order", "binding_initializer", "binding_update"})
_CALLABLES = {"function_declaration", "generator_function_declaration", "function_expression", "generator_function",
    "arrow_function", "method_definition", "function_item", "closure_expression"}
_BLOCKS = {"statement_block", "block", "program", "source_file"}
_TAGS = {"command", "query", "type", "method", "protocol", "kind", "event", "messageType", "message_type",
    "schemaVersion", "schema_version"}
_TYPE_ONLY = {"type_annotation", "type_arguments", "type_parameters", "interface_declaration", "type_alias_declaration",
    "type_query", "import_type", "function_type", "type_predicate_annotation", "implements_clause"}
_LIMITS = {"selected_declarations": 512, "visited_nodes": 262144, "operations": 16384,
    "relationships": 32768, "source_references_per_operation": 96, "source_text_characters": 384}


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def _f(node: Any, key: str) -> Any:
    return node.child_by_field_name(key) if node is not None else None


def _c(node: Any) -> list[Any]:
    return [child for child in node.named_children if child.type not in {"comment", "line_comment", "block_comment"}] if node is not None else []


def _compact(value: Any) -> Any:
    """Keep authenticated spans/hashes; do not duplicate old source bodies."""
    if isinstance(value, dict):
        return {key: _compact(child) for key, child in value.items() if key not in {
            "source_excerpt", "source_line", "parse_identity", "source_excerpt_truncated"}}
    if isinstance(value, list):
        return [_compact(child) for child in value]
    return value


def _u(node: Any) -> Any:
    node = unwrap(node)
    while node is not None and node.type in {"reference_expression", "try_expression", "await_expression", "parenthesized_expression"}:
        node = unwrap(_f(node, "value") or _f(node, "argument") or next(iter(_c(node)), None))
    return node


def _parents(node: Any):
    while node is not None:
        yield node
        node = node.parent


def _inside(parent: Any, node: Any) -> bool:
    return bool(parent is not None and node is not None and parent.start_byte <= node.start_byte and node.end_byte <= parent.end_byte)


def _pointer(parent: str, key: Any) -> str:
    return parent + "/" + str(key).replace("~", "~0").replace("/", "~1")


def _selector_records(value: Any, pointer: str):
    """Read data locators only; no configured path/outcome becomes a fact."""
    if isinstance(value, dict):
        if isinstance(value.get("file"), str) and isinstance(value.get("symbol"), str):
            yield {"file": value["file"], "symbol": value["symbol"]}, pointer
        for key, child in value.items():
            if isinstance(child, (dict, list)):
                yield from _selector_records(child, _pointer(pointer, key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _selector_records(child, _pointer(pointer, index))


class _Operations:
    def __init__(self, snapshot: Any, report: dict, supplemental_selectors: list[dict] | None = None):
        self.snapshot, self.report = snapshot, report
        self.sources = SemanticSources(snapshot)
        self.lexicals: dict[str, LexicalBindings] = {}
        context = SimpleNamespace(snapshot=snapshot, sources=self.sources, lexical=self.lexical)
        self.fields = _Messages(context)
        self.call_context = _Analysis(snapshot, {"sources": [], "models": []}, self.sources)
        self.selected: dict[tuple[str, str], list[dict]] = defaultdict(list)
        self.fact_refs: dict[tuple[str, int, int], list[dict]] = defaultdict(list)
        self.operations: list[dict] = []
        self.by_node: dict[tuple[str, int, str, int | None], dict] = {}
        self.ast_for_operation: dict[str, tuple[Any, Any]] = {}
        self.gaps: list[dict] = []
        self.visited_nodes = 0
        self.relationship_count = 0
        self.incomplete = False
        self.source_location_checks = Counter()
        self.non_cst_fact_counts = Counter()
        self.owner_cache: dict[tuple[str, int], dict] = {}
        self.authentication_cache: dict[tuple, bool] = {}
        self.source_location_index: dict[str, dict] = {}
        self.evidence_reference_index: dict[str, dict] = {}
        self.supplemental_selectors = supplemental_selectors or []

    def pooled(self, value: Any) -> Any:
        """Index full anchors/context once; callers retain usable thin refs."""
        if isinstance(value, dict):
            if {"file", "source_hash", "start_byte", "end_byte", "span_hash"}.issubset(value):
                keys = ("file", "source_hash", "start_byte", "end_byte", "span_hash", "line", "column", "end_line", "end_column",
                    "semantic_parse_id", "coordinate_space", "raw_prefix_bytes", "original_file_start_byte", "original_file_end_byte")
                location = {key: value[key] for key in keys if key in value}
                identity = _digest(location)[:24]
                self.source_location_index[identity] = location
                return {**{key: value[key] for key in ("file", "line", "column", "start_byte", "end_byte", "source_hash") if key in value},
                    "location_ref": "/source_location_index/" + identity,
                    "pointer_scope": "this_responsibility_extraction_or_explanation_object"}
            if "source_artifact_pointer" in value and "reference_role" in value:
                reference = _compact(value)
                identity = _digest(reference)[:24]
                self.evidence_reference_index[identity] = reference
                return {**{key: value[key] for key in ("rule_id", "goal_id", "reference_role") if value.get(key) is not None},
                    "evidence_ref": "/evidence_reference_index/" + identity,
                    "pointer_scope": "this_responsibility_extraction_or_explanation_object"}
            return {key: self.pooled(child) for key, child in value.items() if key not in {
                "source_excerpt", "source_line", "parse_identity", "source_excerpt_truncated"}}
        if isinstance(value, list):
            return [self.pooled(child) for child in value]
        return value

    def lexical(self, document: Any) -> LexicalBindings:
        if document.source.path not in self.lexicals:
            self.lexicals[document.source.path] = LexicalBindings(document)
        return self.lexicals[document.source.path]

    def gap(self, code: str, **details: Any) -> None:
        value = {"code": code, **details}
        if value not in self.gaps:
            self.gaps.append(value)

    def text(self, document: Any, node: Any) -> str:
        return document.text(node)[:_LIMITS["source_text_characters"]] if node is not None else ""

    def authenticate(self, location: Any) -> bool:
        if not isinstance(location, dict):
            return False
        keys = ("file", "source_hash", "start_byte", "end_byte", "span_hash")
        if any(key not in location for key in keys):
            return False
        key = tuple(location[name] for name in keys)
        if key in self.authentication_cache:
            return self.authentication_cache[key]
        document, problems = self.sources.load(location["file"])
        start, end = location["start_byte"], location["end_byte"]
        valid = bool(document is not None and not problems and type(start) is int and type(end) is int
            and 0 <= start <= end <= len(document.data) and document.source.hash == location["source_hash"]
            and hashlib.sha256(document.data[start:end]).hexdigest() == location["span_hash"])
        self.authentication_cache[key] = valid
        self.source_location_checks["matched" if valid else "mismatch"] += 1
        if not valid:
            self.gap("responsibility_existing_source_location_not_authenticated", location={name: location.get(name) for name in keys})
        return valid

    def collect_selections(self) -> None:
        for index, record in enumerate(self.supplemental_selectors):
            selector = record.get("selector", {}) if isinstance(record, dict) else {}
            if not isinstance(selector.get("file"), str) or not isinstance(selector.get("symbol"), str):
                self.gap("responsibility_supplemental_locator_invalid", index=index)
                continue
            context = record.get("context", {})
            self.selected[selector["file"], selector["symbol"]].append({
                **context, "reference_role": "development_selection_context", "old_finding_proves_new_operation": False,
                "source_artifact_pointer": None, "supplemental_selector_index": index,
                "locator_is_new_operation_evidence": False})
        for index, chain in enumerate(self.report.get("functional_chains", [])):
            base = {"rule_id": chain.get("rule_id"), "goal_id": None,
                "finding_id": chain.get("finding_id"), "evidence_id": chain.get("evidence_id"),
                "reference_role": "selection_context", "old_finding_proves_new_operation": False}
            pointer = f"/functional_chains/{index}"
            for offset, source in enumerate(chain.get("source_scope", {}).get("selected_definitions", [])):
                if isinstance(source, dict) and isinstance(source.get("file"), str) and isinstance(source.get("symbol"), str):
                    self.selected[source["file"], source["symbol"]].append({**base,
                        "source_artifact_pointer": pointer + f"/source_scope/selected_definitions/{offset}"})
            for offset, fact in enumerate(chain.get("source_facts", [])):
                location = fact.get("location") if isinstance(fact, dict) else None
                if isinstance(fact, dict) and (fact.get("origin") == "captured-document-text" or
                        isinstance(location, dict) and location.get("coordinate_space") == "captured_document_text_utf8"):
                    self.non_cst_fact_counts["captured_document_text_facts_not_interpreted_as_cst"] += 1
                    continue
                if self.authenticate(location):
                    key = location["file"], location["start_byte"], location["end_byte"]
                    self.fact_refs[key].append({**base, "reference_role": "authenticated_existing_source_location",
                        "source_artifact_pointer": pointer + f"/source_facts/{offset}", "fact_id": fact.get("id"),
                        "saved_fact_kind": fact.get("kind"), "source_location_authenticated": True})
        judgments = {value.get("goal_id"): (index, value) for index, value in enumerate(self.report.get("judgments", []))}
        for index, contract in enumerate(self.snapshot.config.get("goal_contracts", [])):
            matching = judgments.get(contract.get("goal_id"))
            if matching is None:
                continue
            judgment_index, judgment = matching
            base = {"rule_id": contract.get("id"), "goal_id": contract.get("goal_id"),
                "finding_id": judgment.get("finding_id"), "evidence_id": judgment.get("evidence_id"),
                "reference_role": "selection_context", "old_finding_proves_new_operation": False,
                "source_artifact_pointer": f"/judgments/{judgment_index}",
                "saved_evidence_pointer": judgment.get("saved_evidence_pointer")}
            for source, pointer in _selector_records(contract.get("contract", {}), f"/goal_contracts/{index}/contract"):
                self.selected[source["file"], source["symbol"]].append({**base,
                    "snapshot_policy_pointer": pointer, "policy_selector_is_data_only": True})

    def owner(self, document: Any, node: Any) -> dict:
        callable_node = next((part for part in _parents(node.parent) if part.type in _CALLABLES), None)
        if callable_node is None:
            return {"file": document.source.path, "symbol": "<captured-module>", "graph_node_id": None,
                "location": document.location(document.tree.root_node), "binding_state": "captured_source_only"}
        key = document.source.path, callable_node.id
        if key in self.owner_cache:
            return self.owner_cache[key]
        definition = document.definition_for_ast(callable_node)
        graph_id = getattr(definition, "graph_node_id", None) if definition is not None else None
        graph_nodes = self.sources.nodes.get(graph_id, [])
        issues = []
        if len(graph_nodes) == 1:
            _, _, issues = self.sources.definition_for_node(graph_nodes[0])
        symbol = getattr(definition, "symbol", None) if definition is not None else None
        result = {"file": document.source.path,
            "symbol": symbol or "<" + callable_node.type + "@" + str(callable_node.start_point.row + 1) + ":" + str(callable_node.start_point.column + 1) + ">",
            "graph_node_id": graph_id, "location": document.location(callable_node),
            "binding_state": "authenticated_internal_declaration" if len(graph_nodes) == 1 and not issues else "captured_source_only",
            "graph_binding_gaps": issues, "runtime_activation_proven": False}
        self.owner_cache[key] = result
        return result

    def context(self, document: Any, node: Any) -> tuple[list[dict], dict]:
        function = next((part for part in _parents(node.parent) if part.type in _CALLABLES), None)
        guards = []
        for parent in _parents(node.parent):
            if parent == function:
                break
            if parent.type in {"if_statement", "if_expression"}:
                branch = "then" if _inside(_f(parent, "consequence"), node) else "else" if _inside(_f(parent, "alternative"), node) else "condition"
                guards.append({"kind": "if", "branch": branch, "condition_source": self.text(document, _f(parent, "condition")),
                    "location": document.location(parent), "condition_truth_proven": False})
            elif parent.type in {"match_arm", "switch_case", "switch_default", "catch_clause", "finally_clause",
                    "for_statement", "for_in_statement", "while_statement", "for_expression", "while_expression", "loop_expression"}:
                guards.append({"kind": parent.type, "source": self.text(document, _f(parent, "pattern") or _f(parent, "condition") or parent),
                    "location": document.location(parent), "activation_proven": False})
        current = node
        while current.parent is not None and current.parent.type not in _BLOCKS and current.parent != function:
            current = current.parent
        block = current.parent if current.parent is not None and current.parent.type in _BLOCKS else None
        siblings = _c(block)
        order = {"statement_location": document.location(current), "statement_index": next((index for index, part in enumerate(siblings) if part == current), None),
            "block_location": document.location(block) if block is not None else None,
            "normal_reaching_required": True, "runtime_order_or_completion_proven": False,
            "nested_callable_activation_proven": False}
        return list(reversed(guards)), order

    def path(self, document: Any, node: Any) -> dict | None:
        value = self.fields.path(document, node)
        if value is None:
            return None
        identity = value.get("binding") or {}
        return {"root_declaration_id": value["root"], "root_name": value["root_name"], "member_path": value["members"],
            "binding": {"declaration_id": identity.get("declaration_id"), "kind": identity.get("declaration_kind"),
                "location": identity.get("declaration_location"), "state": identity.get("state")},
            "copy_operations": value.get("copy_operations", []), "runtime_referent_identity_proven": False}

    def operand(self, document: Any, node: Any) -> dict:
        if node is None:
            return {"node_kind": "missing", "source_text": "", "binding": None, "member_path": None}
        value = self.path(document, node)
        return {"node_kind": node.type, "source_text": self.text(document, node),
            "source_text_truncated": len(document.text(node)) > _LIMITS["source_text_characters"],
            "location": document.location(node), "source_path": value,
            "binding": value.get("binding") if value else None, "member_path": value.get("member_path") if value else None,
            "runtime_value_proven": False}

    def add(self, kind: str, document: Any, node: Any, references: list[dict], *, operands: dict, subject: dict | None = None,
            slot: int | None = None) -> dict | None:
        key = document.source.path, node.id, kind, slot
        if key in self.by_node:
            previous = self.by_node[key]
            for reference in references:
                if reference not in previous["source_evidence_refs"]:
                    previous["source_evidence_refs"].append(reference)
            previous["source_evidence_reference_count"] = len(previous["source_evidence_refs"])
            return previous
        if len(self.operations) >= _LIMITS["operations"]:
            self.incomplete = True
            return None
        location = document.location(node)
        extra = self.fact_refs.get((document.source.path, node.start_byte, node.end_byte), [])
        refs = []
        for reference in [*references, *extra]:
            if reference not in refs:
                refs.append(reference)
        owner = self.owner(document, node)
        guards, order = self.context(document, node)
        operation = {"id": _digest({"version": VERSION, "snapshot": self.snapshot.id, "source": document.source.hash,
                "file": document.source.path, "span": [node.start_byte, node.end_byte], "kind": kind, "slot": slot})[:24],
            "operation_kind": kind, "actual_owner": owner, "source_locations": [location],
            "source_evidence_refs": refs[:_LIMITS["source_references_per_operation"]],
            "source_evidence_reference_count": len(refs), "source_evidence_references_truncated": len(refs) > _LIMITS["source_references_per_operation"],
            "operands": operands, "subject": subject or {}, "guards": guards, "source_order": order,
            "relationships": [], "proof_domain": "authenticated_captured_cst_lexical_and_existing_call_relations",
            "limitations": {"source_relation_only": True, "runtime_operation_or_effect_proven": False,
                "opaque_call_effects_known": False, "unique_owner_or_authorization_proven": False,
                "creates_calls_edge": False, "old_scope_context_is_not_a_new_operation_judgment": True}}
        self.by_node[key] = operation
        self.operations.append(operation)
        self.ast_for_operation[operation["id"]] = document, node
        return operation

    def relate(self, source: dict, target: dict, kind: str, *, binding_state: str, **details: Any) -> None:
        if source["id"] == target["id"]:
            return
        if self.relationship_count >= _LIMITS["relationships"]:
            self.incomplete = True
            return
        relation = {"kind": kind, "from_operation_id": source["id"], "to_operation_id": target["id"],
            "binding_state": binding_state, "conditions": ["captured statements and expressions are reached normally in the selected source context"],
            "runtime_value_or_effect_proven": False, **details}
        if relation not in target["relationships"]:
            target["relationships"].append(relation)
            self.relationship_count += 1

    def record(self, document: Any, node: Any, references: list[dict]) -> None:
        parsed = self.fields.record(document, node)
        fields = []
        parent = node.parent
        bound = None
        if parent is not None and parent.type in {"variable_declarator", "let_declaration"} and _inside(_f(parent, "value"), node):
            bound = self.path(document, _f(parent, "name") or _f(parent, "pattern"))
        for name, field in parsed["fields"].items():
            value = field["node"]
            fields.append({"name": name, "source_text": self.text(document, value), "source_path": self.path(document, value),
                "binding": (self.path(document, value) or {}).get("binding"), "location": field["location"],
                "closed": parsed["closed"], "runtime_field_presence_or_value_proven": False})
        construction = self.add("record_construction", document, node, references,
            operands={"source_text": self.text(document, node), "node_kind": node.type,
                "record_type_source": parsed.get("type_source"), "record_fields": fields,
                "closed_captured_shape": parsed["closed"], "result_binding": bound,
                "ordinary_data_semantics_not_automatically_assumed": True},
            subject={"field_names": [field["name"] for field in fields], "record_type_source": parsed.get("type_source")})
        for name, field in parsed["fields"].items():
            value = field["node"]
            source = self.path(document, value)
            if source is not None:
                projection = self.add("record_field_projection", document, value, references, slot=value.start_byte,
                    operands={**self.operand(document, value), "field_name": name,
                        "output_record_location": document.location(node)}, subject={"field_name": name, "source_path": source})
                if construction and projection:
                    self.relate(projection, construction, "field_projection_from_record", binding_state="captured_source_only",
                        field_name=name, relation_meaning="the captured field initializer references this lexical path; no current heap value equality")
            if name in _TAGS:
                literal = _literal_string(document.text(_u(value)))
                scoped = _u(value).type in {"scoped_identifier", "scoped_type_identifier", "member_expression"}
                if literal is not None or scoped:
                    self.add("protocol_literal_field", document, value, references, slot=value.start_byte,
                        operands={**self.operand(document, value), "field_name": name, "literal_value": literal,
                            "enum_member_source": document.text(_u(value)) if scoped else None,
                            "record_location": document.location(node), "protocol_transport_semantics_proven": False},
                        subject={"field_name": name})
        body = _f(node, "body") if node.type == "struct_expression" else node
        for child in _c(body):
            if child.type in {"spread_element", "base_field_initializer"}:
                value = _f(child, "value") or next(iter(_c(child)), None)
                self.add("record_copy_projection", document, child, references,
                    operands={**self.operand(document, value), "copy_form": child.type,
                        "destination_record_location": document.location(node), "current_copy_surface_or_retention_proven": False})

    def target_parameter(self, document: Any, call: Any, edge: Any, index: int) -> dict | None:
        target_nodes = self.sources.nodes.get(edge.target, []) if edge is not None else []
        if len(target_nodes) != 1:
            return None
        target_document, definition, gaps = self.sources.definition_for_node(target_nodes[0])
        if target_document is None or definition is None or gaps:
            return None
        function = unwrap(definition.value) if definition.value is not None else definition.node
        parameters = _c(_f(function, "parameters"))
        callee = _f(call, "function")
        if parameters and parameters[0].type == "self_parameter" and callee is not None and callee.type == "field_expression":
            index += 1
        if index >= len(parameters):
            return None
        parameter = parameters[index]
        pattern = _f(parameter, "pattern") or _f(parameter, "name") or (parameter if parameter.type in {"identifier", "self"} else None)
        return {"file": target_document.source.path, "symbol": definition.symbol, "formal_parameter_index": index,
            "source_text": self.text(target_document, parameter), "location": target_document.location(parameter),
            "source_path": self.path(target_document, pattern),
            "callee_activation_or_parameter_runtime_value_proven": False}

    def call(self, document: Any, node: Any, references: list[dict]) -> None:
        owner_id = document.call_owner(node)
        definitions = document.definition_nodes.get(owner_id, [])
        edge, gaps = self.sources.call_binding(node, document, definitions[0]) if len(definitions) == 1 else (None, [{"code": "source_callable_has_no_unique_graph_binding"}])
        captured = self.call_context.raw_edge(document, node)
        callee = _f(node, "function") or _f(node, "constructor")
        receiver = _f(callee, "object") or _f(callee, "value")
        target_nodes = self.sources.nodes.get(edge.target, []) if edge is not None else []
        binding_state = "authenticated_internal_call" if edge is not None else "captured_call_site_unknown" if captured is not None else "captured_source_only"
        target = {"source_text": self.text(document, callee), "target_symbol": target_nodes[0].qualname if len(target_nodes) == 1 else None,
            "target_graph_node_id": edge.target if edge is not None else None, "binding_state": binding_state,
            "authenticated_call_edge_id": edge.id if edge is not None else None,
            "captured_call_edge_id": captured.id if captured is not None else None,
            "captured_resolution": captured.resolution if captured is not None else None,
            "binding_gaps": gaps, "unknown_port_effects_remain_unknown": edge is None}
        arguments = _c(_f(node, "arguments"))
        for index, argument in enumerate(arguments or [None]):
            arg = _u(argument)
            literal_fields = self.fields.record(document, arg)["fields"] if arg is not None and arg.type in {"object", "struct_expression"} else {}
            self.add("call_argument_transfer", document, node, references, slot=index if argument is not None else None,
                operands={"source_text": self.text(document, node), "node_kind": node.type, "callee": target,
                    "receiver": self.operand(document, receiver) if receiver is not None else None,
                    "argument_index": index if argument is not None else None, "argument_count": len(arguments),
                    "argument": self.operand(document, argument) if argument is not None else None,
                    "target_parameter": self.target_parameter(document, node, edge, index) if argument is not None and edge is not None else None,
                    "record_fields": [{"name": name, "source_text": self.text(document, value["node"]),
                        "source_path": self.path(document, value["node"]), "location": value["location"]} for name, value in literal_fields.items()],
                    "interface_kind": "ordinary_captured_call_site", "wire_or_storage_effect_inferred": False},
                subject={"callee_source": self.text(document, callee), "argument_index": index if argument is not None else None})

    def extract_function(self, document: Any, function: Any, references: list[dict]) -> None:
        pending = list(reversed(_c(_f(function, "body"))))
        while pending:
            node = pending.pop()
            self.visited_nodes += 1
            if self.visited_nodes > _LIMITS["visited_nodes"]:
                self.incomplete = True
                return
            if node.type in _TYPE_ONLY or node.type.endswith("_type"):
                continue
            # Nested captured callable bodies are kept as distinct lexical
            # owners. Their activation never follows from enclosing syntax.
            pending.extend(reversed(_c(node)))
            if node.type in {"object", "struct_expression"}:
                self.record(document, node, references)
            elif node.type in {"call_expression", "new_expression"}:
                self.call(document, node, references)
            elif node.type in {"variable_declarator", "let_declaration"}:
                target = _f(node, "name") or _f(node, "pattern")
                value = _f(node, "value")
                source_path = self.path(document, target)
                if source_path is not None and not source_path["member_path"] and value is not None:
                    self.add("binding_initializer", document, node, references,
                        operands={"source_text": self.text(document, node), "node_kind": node.type,
                            "target": self.operand(document, target), "value": self.operand(document, value),
                            "assignment_operator": "=", "runtime_initialization_proven": False},
                        subject={"target_path": source_path, "write_target_kind": "local_binding"})
            elif node.type in {"assignment_expression", "augmented_assignment_expression", "compound_assignment_expr", "update_expression"}:
                target = _f(node, "left") or _f(node, "argument")
                value = _f(node, "right")
                source_path = self.path(document, target)
                if source_path is not None and source_path["member_path"]:
                    self.add("field_write", document, node, references,
                        operands={"source_text": self.text(document, node), "node_kind": node.type,
                            "target": self.operand(document, target), "value": self.operand(document, value),
                            "assignment_operator": document.text(_f(node, "operator")), "assignment_success_proven": False},
                        subject={"target_path": source_path})
                elif source_path is not None:
                    self.add("binding_update", document, node, references,
                        operands={"source_text": self.text(document, node), "node_kind": node.type,
                            "target": self.operand(document, target), "value": self.operand(document, value),
                            "assignment_operator": document.text(_f(node, "operator")), "actual_update_count_or_numeric_result_proven": False},
                        subject={"target_path": source_path, "write_target_kind": "local_binding"})
            elif node.type in {"return_statement", "return_expression", "throw_statement"}:
                value = _f(node, "value") or _f(node, "argument") or next(iter(_c(node)), None)
                returned = self.add("return_transfer", document, node, references,
                    operands={"source_text": self.text(document, node), "node_kind": node.type,
                        "exit_kind": "throw" if node.type == "throw_statement" else "return",
                        "value": self.operand(document, value), "async_fulfillment_or_return_effect_proven": False})
                control = next((part for part in _parents(node.parent) if part.type in {"if_statement", "if_expression", "match_arm", *_CALLABLES}), None)
                if control is not None and control.type not in _CALLABLES:
                    condition = _f(control, "condition") or _f(control, "pattern")
                    rejection = self.add("guard_rejection", document, node, references,
                        operands={"source_text": self.text(document, node), "node_kind": node.type,
                            "condition_source": self.text(document, condition), "condition_location": document.location(condition) if condition is not None else document.location(control),
                            "exit_kind": "throw" if node.type == "throw_statement" else "Err_return" if value is not None and self.text(document, _u(value)).startswith("Err(") else "return",
                            "exit_source": self.text(document, value), "guard_truth_or_rejection_observed": False,
                            "return_is_error_or_business_rejection_proven": False})
                    if returned and rejection:
                        self.relate(rejection, returned, "explicit_return_value", binding_state="captured_source_only")

    def relationships(self) -> None:
        constructions = [value for value in self.operations if value["operation_kind"] == "record_construction"]
        arguments = [value for value in self.operations if value["operation_kind"] == "call_argument_transfer"]
        bound_records = defaultdict(list)
        for record in constructions:
            binding = record["operands"].get("result_binding")
            if binding:
                bound_records[binding["root_declaration_id"]].append(record)
        for argument in arguments:
            operand = argument["operands"].get("argument")
            if operand is None:
                continue
            path = operand.get("source_path")
            arg_location = operand["location"]
            for record in constructions:
                location = record["source_locations"][0]
                if location["file"] == arg_location["file"] and location["start_byte"] == arg_location["start_byte"] and location["end_byte"] == arg_location["end_byte"]:
                    self.relate(record, argument, "record_literal_as_argument", binding_state=argument["operands"]["callee"]["binding_state"],
                        actual_argument_index=argument["operands"]["argument_index"], literal_expression_identity=True)
            if path is not None and not path["member_path"]:
                for record in bound_records.get(path["root_declaration_id"], []):
                    if record["source_locations"][0]["end_byte"] <= arg_location["start_byte"]:
                        self.relate(record, argument, "lexical_value_to_argument", binding_state="captured_source_only",
                            same_lexical_binding=True, intervening_writes_and_heap_effects_excluded=False,
                            relation_meaning="a constructed record and this argument reference the same captured local declaration; current record fields are not certified")
        for returned in (value for value in self.operations if value["operation_kind"] == "return_transfer"):
            value = returned["operands"].get("value") or {}
            location = value.get("location") or {}
            for record in constructions:
                source = record["source_locations"][0]
                if all(source.get(key) == location.get(key) for key in ("file", "start_byte", "end_byte")):
                    self.relate(record, returned, "explicit_return_value", binding_state="captured_source_only",
                        same_returned_literal_expression=True, async_fulfillment_proven=False)
        uses = defaultdict(list)
        for operation in self.operations:
            operand = operation["operands"]
            paths = [operand.get("source_path"), (operand.get("argument") or {}).get("source_path"),
                (operand.get("value") or {}).get("source_path")]
            for path in paths:
                if path is not None and path.get("root_declaration_id"):
                    uses[path["root_declaration_id"]].append(operation)
        for argument in arguments:
            callee = argument["operands"]["callee"]
            formal = argument["operands"].get("target_parameter") or {}
            path = formal.get("source_path") or {}
            if callee.get("binding_state") != "authenticated_internal_call" or not path.get("root_declaration_id"):
                continue
            for use in uses.get(path["root_declaration_id"], []):
                if use["actual_owner"].get("graph_node_id") != callee.get("target_graph_node_id"):
                    continue
                self.relate(argument, use, "authenticated_argument_parameter_projection", binding_state="authenticated_internal_call",
                    authenticated_call_edge_id=callee["authenticated_call_edge_id"], formal_parameter=formal,
                    actual_argument_index=argument["operands"]["argument_index"], callee_activation_proven=False,
                    current_heap_field_retention_proven=False)
        statement_groups = defaultdict(lambda: defaultdict(list))
        for operation in self.operations:
            order = operation["source_order"]
            block = order.get("block_location")
            if block and order.get("statement_index") is not None:
                statement_groups[(block["file"], block["start_byte"], block["end_byte"])][order["statement_index"]].append(operation)
        for _, statements in sorted(statement_groups.items()):
            ordered = sorted(statements)
            for before_index, after_index in zip(ordered, ordered[1:]):
                before, after = statements[before_index][0], statements[after_index][0]
                document, node = self.ast_for_operation[after["id"]]
                sequence = self.add("normal_source_order", document, node, after["source_evidence_refs"], slot=before_index,
                    operands={"before_operation_id": before["id"], "after_operation_id": after["id"],
                        "before_statement_index": before_index, "after_statement_index": after_index,
                        "normal_reaching_required": True, "causal_dependency_proven": False})
                if sequence:
                    self.relate(before, sequence, "normal_source_before", binding_state="captured_source_only",
                        source_order_is_not_value_flow=True)
                    self.relate(sequence, after, "normal_source_before", binding_state="captured_source_only",
                        source_order_is_not_value_flow=True)

    def run(self) -> dict:
        header = self.report.get("snapshot", {})
        if any(header.get(key) != getattr(self.snapshot, attribute) for key, attribute in
                (("id", "id"), ("source_hash", "source_hash"), ("policy_hash", "policy_hash"))):
            self.gap("responsibility_report_snapshot_identity_mismatch")
        else:
            self.collect_selections()
            for index, ((file, symbol), references) in enumerate(sorted(self.selected.items())):
                if index >= _LIMITS["selected_declarations"]:
                    self.incomplete = True
                    break
                document, definition, issues = self.sources.select({"file": file, "symbol": symbol})
                if document is None or definition is None or issues:
                    self.gap("responsibility_selected_declaration_unavailable", file=file, symbol=symbol, source_gaps=issues)
                    continue
                function = unwrap(definition.value) if definition.value is not None else definition.node
                if function is None or function.type not in _CALLABLES:
                    # Set/constant locators are valid old evidence, but they
                    # are not silently reclassified as responsible functions.
                    continue
                self.extract_function(document, function, references)
                if self.incomplete:
                    break
            self.relationships()
        if self.fields.incomplete:
            self.incomplete = True
            self.gap("responsibility_field_source_helper_budget_incomplete")
        if self.incomplete:
            self.gap("responsibility_source_operation_budget_exceeded", limits=_LIMITS)
        self.operations = [self.pooled(value) for value in self.operations]
        self.operations.sort(key=lambda value: (value["actual_owner"]["file"], value["source_locations"][0]["start_byte"], value["operation_kind"], value["id"]))
        for operation in self.operations:
            operation["content_sha256"] = _digest(operation)
        return {"version": VERSION, "model": MODEL,
            "snapshot_identity": {"snapshot_id": self.snapshot.id, "source_hash": self.snapshot.source_hash,
                "policy_hash": self.snapshot.policy_hash}, "operations": self.operations,
            "source_location_index": dict(sorted(self.source_location_index.items())),
            "evidence_reference_index": dict(sorted(self.evidence_reference_index.items())),
            "operation_kind_counts": dict(sorted(Counter(value["operation_kind"] for value in self.operations).items())),
            "analysis_gaps": self.gaps, "source_location_authentication": dict(self.source_location_checks),
            "scope": {"selected_declaration_count": len(self.selected), "selected_declarations_are_navigation_not_behavior": True,
                "source_selections": [{"file": file, "symbol": symbol} for file, symbol in sorted(self.selected)],
                "whole_repository_operations_enumerated": False,
                "input_report_text_used_as_expected_answer": False, "finding_ids_are_navigation_context": True,
                "ordinary_call_bindings_and_opaque_ports_are_separate": True,
                "protocol_literal_fields_do_not_establish_wire_connectivity": True,
                "source_bodies_and_old_fact_trees_duplicated": False,
                "non_cst_fact_counts": dict(self.non_cst_fact_counts),
                "non_cst_document_facts_are_valid_separate_evidence_not_operation_cst": True},
            "budget": {"visited_nodes": self.visited_nodes, "operations": len(self.operations),
                "relationships": self.relationship_count, "limits": _LIMITS, "incomplete": self.incomplete},
            "component_versions": {"semantic_sources": SOURCE_VERSION, "lexical_bindings": LEXICAL_VERSION,
                "field_source_relations": FIELD_SOURCE_VERSION, "existing_call_source_relations": CALL_SOURCE_VERSION},
            "flags": {"source_operations_only": True, "unique_fact_owner_proven": False,
                "authorization_proven": False, "opaque_storage_effects_known": False,
                "wire_or_runtime_value_identity_proven": False, "creates_calls_edge": False,
                "target_executed": False, "target_tests_run": False, "target_build_run": False}}


def extract_responsibility_operations(snapshot: Any, report: dict, *, supplemental_selectors: list[dict] | None = None) -> dict:
    """Extract finite source operations; prior result IDs only locate context."""
    return _Operations(snapshot, report, supplemental_selectors).run()
