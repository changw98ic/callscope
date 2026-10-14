"""Finite captured-record and message-correlation relations.

The input is the report engine's authenticated saved source roles.  Declaration
identity, record projection, enum destructuring and SQL argument positions are
kept separate.  A projection agreement is never a claim that two wire payloads
have equal values, and this module creates no CALLS edges.
"""
from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from .semantic_sources import unwrap
from .static_contracts import _literal_string

VERSION = "captured-message-identity-relations-1"
MODEL = "finite-captured-record-message-identities-v1"
SQL_MODEL = "captured-literal-sql-positional-bindings-v1"
_FUNCTIONS = {"function_declaration", "function_expression", "arrow_function", "method_definition",
    "function_item", "closure_expression", "generator_function_declaration", "generator_function"}
_BLOCKS = {"statement_block", "block"}
_LIMIT = 65536


def _f(node: Any, name: str) -> Any:
    return node.child_by_field_name(name) if node is not None else None


def _c(node: Any) -> list[Any]:
    return [child for child in node.named_children if child.type not in {"comment", "line_comment", "block_comment"}] if node is not None else []


def _u(node: Any) -> Any:
    node = unwrap(node)
    while node is not None and node.type in {"reference_expression", "try_expression", "await_expression", "parenthesized_expression"}:
        node = unwrap(_f(node, "value") or _f(node, "argument") or next(iter(_c(node)), None))
    return node


def _inside(parent: Any, node: Any) -> bool:
    return bool(parent is not None and node is not None and parent.start_byte <= node.start_byte and node.end_byte <= parent.end_byte)


def _parents(node: Any):
    while node is not None:
        yield node
        node = node.parent


def _hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode()).hexdigest()


class _Messages:
    def __init__(self, analysis: Any):
        self.a = analysis
        self.relations: list[dict] = []
        self.parts: dict[str, dict] = {}
        self.operations = 0
        self.incomplete = False
        self._nodes: dict[tuple[str, int], list[Any]] = {}
        self._identities: dict[tuple[str, int], dict] = {}

    def nodes(self, document: Any, root: Any) -> list[Any]:
        if root is None:
            return []
        key = document.source.path, root.id
        if key in self._nodes:
            return self._nodes[key]
        pending, result = [root], []
        while pending:
            node = pending.pop()
            self.operations += 1
            if self.operations > _LIMIT:
                self.incomplete = True
                break
            result.append(node)
            if node is not root and node.type in _FUNCTIONS:
                continue
            pending.extend(reversed(_c(node)))
        self._nodes[key] = result
        return result

    def role(self, name: str) -> tuple | None:
        return self.a.roles.get(name)

    def fact(self, kind: str, document: Any, node: Any, **details: Any) -> dict:
        result = self.a.fact(kind, document, node, extractor_version=VERSION,
            creates_calls_edge=False, target_code_executed=False, **details)
        self.relations.append(result)
        return result

    def gap(self, code: str, document: Any = None, node: Any = None, **details: Any) -> None:
        self.a.gap(code, document, node, **details)

    def identity(self, document: Any, node: Any) -> dict:
        """Finite captured binders; no name-only cross-function equivalence."""
        if node is None:
            return {"state": "missing"}
        key = document.source.path, node.id
        if key in self._identities:
            return self._identities[key]
        if document.kind != "rust":
            source = self.a.lexical(document).resolve_identity(node)
            result = {key: source.get(key) for key in ("state", "identity_complete", "declaration_id",
                "declaration_kind", "parameter_index", "declaration_location", "binder_location")}
        else:
            name = document.text(node)
            ancestors = list(_parents(node))
            function = next((parent for parent in ancestors if parent.type in _FUNCTIONS), None)
            candidates = []
            if function is not None:
                for parameter in _c(_f(function, "parameters")) if _f(function, "parameters") is not None else []:
                    binder = _f(parameter, "pattern") or (parameter if parameter.type == "identifier" else None)
                    if parameter.type == "self_parameter":
                        binder = next((part for part in _c(parameter) if part.type == "self"), None)
                    if binder is not None and binder.type in {"identifier", "self"} and document.text(binder) == name:
                        candidates.append((function, parameter, binder, "parameter"))
                for declaration in self.nodes(document, _f(function, "body")):
                    if declaration.type != "let_declaration":
                        continue
                    binder = _f(declaration, "pattern")
                    if declaration.end_byte > node.start_byte and not _inside(binder, node):
                        continue
                    scope = next((part for part in _parents(declaration.parent) if part.type in _BLOCKS), None)
                    binders = [part for part in self.nodes(document, binder) if part.type == "identifier"
                        and not (part.parent is not None and part.parent.type == "tuple_struct_pattern" and _f(part.parent, "type") == part)
                        and not any(parent.type in {"scoped_identifier", "scoped_type_identifier"}
                            for parent in _parents(part.parent) if _inside(binder, parent))] if binder is not None else []
                    for captured in binders:
                        if scope is not None and _inside(scope, node) and document.text(captured) == name:
                            candidates.append((scope, declaration, captured, "local"))
                for arm in (parent for parent in ancestors if parent.type == "match_arm"):
                    pattern = _f(arm, "pattern") or next(iter(_c(arm)), None)
                    if pattern is None:
                        continue
                    for binder in self.nodes(document, pattern):
                        if binder.type != "identifier" or document.text(binder) != name:
                            continue
                        if binder.parent is not None and binder.parent.type in {"tuple_struct_pattern", "captured_pattern"}:
                            candidates.append((arm, pattern, binder, "enum_arm"))
            if candidates:
                size = min(scope.end_byte - scope.start_byte for scope, _, _, _ in candidates)
                candidates = [value for value in candidates if value[0].end_byte - value[0].start_byte == size]
                # Rust sequential shadowing: the last preceding binder in the
                # same captured block is the selected lexical declaration.
                last = max(declaration.start_byte for _, declaration, _, _ in candidates)
                candidates = [value for value in candidates if value[1].start_byte == last]
            if len(candidates) == 1:
                scope, declaration, binder, kind = candidates[0]
                result = {"state": "unique", "identity_complete": True,
                    "declaration_id": _hash({"version": VERSION, "snapshot": self.a.snapshot.id,
                        "file": document.source.path, "hash": document.source.hash,
                        "declaration": [declaration.start_byte, declaration.end_byte],
                        "binder": [binder.start_byte, binder.end_byte]}),
                    "declaration_kind": "captured_rust_" + kind,
                    "declaration_location": document.location(declaration), "binder_location": document.location(binder),
                    "macro_namespace_complete": False, "runtime_value_identity_proven": False}
            else:
                result = {"state": "unknown", "plain_binder_candidates": len(candidates), "name": name}
        self._identities[key] = result
        return result

    def path(self, document: Any, node: Any, *, copies: bool = True) -> dict | None:
        node = _u(node)
        if node is None:
            return None
        if node.type in {"identifier", "self", "this", "shorthand_property_identifier", "shorthand_field_identifier"}:
            if node.type == "this":
                function = next((parent for parent in _parents(node) if parent.type in _FUNCTIONS), None)
                owner = next((parent for parent in _parents(function) if parent.type in {"class", "class_declaration"}), None)
                identity = {"state": "captured_this", "declaration_id": _hash({"file": document.source.path,
                    "source": document.source.hash, "owner": [owner.start_byte, owner.end_byte] if owner is not None else None})}
            else:
                identity = self.identity(document, node)
            if identity.get("state") not in {"unique", "captured_this"} or not identity.get("declaration_id"):
                return None
            return {"root": identity["declaration_id"], "root_name": document.text(node), "members": [],
                "binding": identity, "location": document.location(node), "copy_operations": []}
        if node.type in {"member_expression", "field_expression"}:
            root = self.path(document, _f(node, "object") or _f(node, "value"), copies=copies)
            member = _f(node, "property") or _f(node, "field")
            if root is not None and member is not None and member.type in {"property_identifier", "field_identifier", "integer_literal"}:
                return {**root, "members": [*root["members"], document.text(member)], "location": document.location(node)}
        if copies and node.type == "call_expression":
            callee = _f(node, "function")
            if callee is not None and callee.type in {"member_expression", "field_expression"} and not _c(_f(node, "arguments")):
                member = _f(callee, "property") or _f(callee, "field")
                name = document.text(member) if member is not None else ""
                if name in {"clone", "to_owned"}:
                    result = self.path(document, _f(callee, "object") or _f(callee, "value"))
                    if result is not None:
                        return {**result, "location": document.location(node),
                            "copy_operations": [*result["copy_operations"], {"method": name, "location": document.location(node),
                                "ordinary_generated_data_clone_model_required": True}]}
        return None

    def same(self, document: Any, left: Any, right: Any) -> bool:
        lpath, rpath = self.path(document, left), self.path(document, right)
        return bool(lpath and rpath and (lpath["root"], lpath["members"]) == (rpath["root"], rpath["members"]))

    def record(self, document: Any, node: Any) -> dict:
        node = _u(node)
        if node is None or node.type not in {"object", "struct_expression"}:
            return {"closed": False, "fields": {}, "node": node}
        body = _f(node, "body") if node.type == "struct_expression" else node
        if body is None:
            body = next((part for part in _c(node) if part.type == "field_initializer_list"), None)
        fields, complete = {}, True
        for part in _c(body) if body is not None else []:
            if part.type in {"pair", "field_initializer"}:
                key = _f(part, "key") or _f(part, "field")
                value = _f(part, "value")
            elif part.type in {"shorthand_property_identifier", "shorthand_field_initializer"}:
                value = next(iter(_c(part)), part)
                key = value
            else:
                complete = False
                continue
            name = document.text(key) if key is not None and key.type in {"property_identifier", "field_identifier", "identifier", "shorthand_property_identifier"} else _literal_string(document.text(key)) if key is not None else None
            if name is None or name in fields or name == "__proto__" or value is None:
                complete = False
                continue
            fields[name] = {"node": value, "location": document.location(part), "path": self.path(document, value)}
        return {"closed": complete, "fields": fields, "node": node,
            "type_source": document.text(_f(node, "name")) if node.type == "struct_expression" else None}

    def public_record(self, document: Any, record: dict) -> dict:
        return {"closed_captured_shape": record["closed"], "type_source": record.get("type_source"),
            "fields": {name: {"location": value["location"], "source_path": value["path"],
                "expression": self.a.expression(document, value["node"])} for name, value in record["fields"].items()},
            "ordinary_data_model_required": True, "runtime_record_value_proven": False}

    def body(self, role: str) -> tuple[Any, Any, Any, list[Any]] | None:
        component = self.role(role)
        if component is None:
            self.gap("message_required_source_role_missing", role=role)
            return None
        document, definition, function = component
        return document, definition, function, self.nodes(document, _f(function, "body"))

    def calls(self, document: Any, nodes: list[Any], name: str) -> list[Any]:
        result = []
        for node in nodes:
            if node.type != "call_expression":
                continue
            callee = _f(node, "function")
            while callee is not None and callee.type == "generic_function":
                callee = _f(callee, "function")
            member = _f(callee, "property") or _f(callee, "field")
            if document.text(member or callee).rsplit("::", 1)[-1] == name:
                result.append(node)
        return result

    def call_relation(self, role: str, document: Any, call: Any, target_role: str) -> dict:
        """Authenticate existing edges or a finite same-module declaration seam."""
        target = self.role(target_role)
        if target is None:
            return {"supported": False, "reason": "target_role_missing"}
        tdoc, tdef, tfn = target
        facts = [value for value in self.a.calls_by_role.get(role, [])
            if value["location"]["start_byte"] == call.start_byte and value["location"]["end_byte"] == call.end_byte]
        if len(facts) == 1 and facts[0].get("actual_callee_graph_node_id") == tdef.graph_node_id and facts[0].get("authenticated_call_edge_id"):
            return {"supported": True, "kind": "existing_authenticated_call", "fact_id": facts[0]["id"],
                "edge_id": facts[0]["authenticated_call_edge_id"], "target_role": target_role}
        callee = _f(call, "function")
        name = _f(tfn, "name")
        if (document is tdoc and document.kind == "rust" and callee is not None and callee.type == "identifier"
                and name is not None and document.text(callee) == document.text(name)
                and tfn.parent.type in {"source_file", "declaration_list"}):
            owner = self.role(role)
            owner_fn = owner[2] if owner is not None else None
            shadows = [node for node in self.nodes(document, _f(owner_fn, "body"))
                if node.type in {"let_declaration", "function_item"} and node.end_byte <= call.start_byte
                and any(part.type == "identifier" and document.text(part) == document.text(name)
                    for part in self.nodes(document, _f(node, "pattern") or _f(node, "name")))]
            parameter_shadows = [part for part in self.nodes(document, _f(owner_fn, "parameters"))
                if part.type == "identifier" and document.text(part) == document.text(name)]
            if not shadows and not parameter_shadows:
                return {"supported": True, "kind": "captured_same_module_function_relation",
                    "target_role": target_role, "target_location": document.location(tfn),
                    "scope": "unique captured top-level declaration and no captured local binder shadows this value name",
                    "macro_expansion_or_runtime_activation_proven": False, "creates_calls_edge": False}
        return {"supported": False, "target_role": target_role,
            "reason": "captured_call_target_not_authenticated", "creates_calls_edge": False}

    def arg(self, call: Any, index: int) -> Any:
        arguments = _c(_f(call, "arguments")) if call is not None else []
        return arguments[index] if index < len(arguments) else None

    def assignments(self, document: Any, nodes: list[Any]) -> list[tuple[Any, Any, Any]]:
        result = []
        for node in nodes:
            if node.type in {"assignment_expression", "compound_assignment_expr"}:
                result.append((node, _f(node, "left"), _f(node, "right")))
            elif node.type in {"variable_declarator", "let_declaration"}:
                result.append((node, _f(node, "name") or _f(node, "pattern"), _f(node, "value")))
        return result

    def field_records(self, role: str) -> list[tuple[Any, dict]]:
        item = self.body(role)
        if item is None:
            return []
        document, _, function, nodes = item
        result = []
        for node in nodes:
            if node.type not in {"object", "struct_expression"}:
                continue
            record = self.record(document, node)
            self.fact("message_captured_record_fields", document, node, role=role,
                record=self.public_record(document, record), branch_context=self.a.branch_context(document, node, function))
            result.append((node, record))
        return result

    def enum_consumers(self, role: str) -> list[dict]:
        item = self.body(role)
        if item is None:
            return []
        document, _, function, nodes = item
        records = []
        for arm in (node for node in nodes if node.type == "match_arm"):
            pattern = _f(arm, "pattern") or next(iter(_c(arm)), None)
            value = _f(arm, "value")
            if pattern is None or value is None:
                continue
            tuples = [part for part in self.nodes(document, pattern) if part.type == "tuple_struct_pattern"]
            if len(tuples) != 1:
                continue
            tuple_pattern = tuples[0]
            binders = [part for part in _c(tuple_pattern) if part.type == "identifier"]
            constructor = _f(tuple_pattern, "type") or next((part for part in _c(tuple_pattern) if part.type in {"scoped_identifier", "scoped_type_identifier"}), None)
            if len(binders) != 1 or constructor is None:
                continue
            name = document.text(binders[0])
            references = [part for part in self.nodes(document, value) if part.type == "identifier" and document.text(part) == name]
            consumers = []
            for call in (part for part in self.nodes(document, value) if part.type == "call_expression"):
                for index, argument in enumerate(_c(_f(call, "arguments"))):
                    path = self.path(document, argument)
                    if path is not None and path["root_name"] == name and path["binding"].get("declaration_kind") == "captured_rust_enum_arm":
                        consumers.append({"callee_source": document.text(_f(call, "function")), "argument_index": index,
                            "argument": path, "call_location": document.location(call),
                            "ordinary_receiver_dispatch_proven": False})
            record = self.fact("message_enum_arm_consumers", document, arm, role=role,
                constructor=document.text(constructor), binder_location=document.location(binders[0]),
                field_and_argument_references=[document.location(part) for part in references], consumers=consumers,
                enum_variant_is_active_proven=False, branch_context=self.a.branch_context(document, arm, function))
            records.append(record)
        return records

    def chat(self) -> dict:
        item = self.body("chat_create")
        if item is None:
            return {"supported": False}
        document, _, function, nodes = item
        assignments = self.assignments(document, nodes)
        commands = self.calls(document, nodes, "command")
        emissions = []
        for call in commands:
            path = self.path(document, self.arg(call, 0))
            if path is not None:
                emissions.append(self.fact("message_request_emission_projection", document, call,
                    role="chat_create", request=path, branch_context=self.a.branch_context(document, call, function),
                    receiver_source=document.text(_f(_f(call, "function"), "object")),
                    transport_or_response_truth_proven=False))
        retained = []
        for assignment, left, right in assignments:
            target = self.path(document, left)
            value = _u(right)
            if target is None or value is None:
                continue
            if target["members"] and target["members"][-1].endswith("Request"):
                retained.append(self.fact("message_retained_request_assignment", document, assignment,
                    target=target, source=self.a.expression(document, right),
                    source_record=self.public_record(document, self.record(document, right)) if value.type == "object" else None,
                    branch_context=self.a.branch_context(document, assignment, function),
                    source_conditional_retention_only=True, runtime_retry_success_proven=False))
        aliases = []
        for assignment, left, right in assignments:
            target, source = self.path(document, left), self.path(document, right)
            if target is not None and source is not None and not target["members"]:
                aliases.append(self.fact("message_local_binding_projection", document, assignment,
                    target=target, source=source, current_heap_alias_proven=False,
                    ordinary_record_read_at_initializer_only=True))
        delivery = [value for value in aliases if value["source"]["members"][-3:] == ["createRequest", "payload", "deliveryId"]]
        roots = {value["source"]["root"] for value in delivery}
        send_fields = {tuple(value["request"]["members"]) for value in emissions if value["request"]["root"] in roots}
        records = self.field_records("chat_create")
        delivery_projections = []
        if len(delivery) == 1:
            delivery_root = delivery[0]["target"]["root"]
            for node, record in records:
                value = record["fields"].get("deliveryId")
                if value is not None and value["path"] is not None and value["path"]["root"] == delivery_root and not value["path"]["members"]:
                    delivery_projections.append(self.fact("message_delivery_identity_record_projection", document, node,
                        source_binding=delivery[0]["target"], target_field=value["location"],
                        record=self.public_record(document, record), runtime_wire_identity_proven=False))
        comparisons = []
        for node in nodes:
            if node.type != "binary_expression":
                continue
            left, right = self.path(document, _f(node, "left")), self.path(document, _f(node, "right"))
            if left is None or right is None:
                continue
            if left["members"][-1:] == right["members"][-1:] == ["requestId"] and left["root"] != right["root"]:
                comparisons.append(self.fact("message_response_request_id_comparison", document, node,
                    left=left, right=right, source_operator=document.text(_f(node, "operator")),
                    branch_context=self.a.branch_context(document, node, function), response_identity_assumed=False))
        builder = self.body("chat_items_builder")
        builder_fields = []
        if builder is not None:
            bdoc, _, bfn, bnodes = builder
            for node, record in self.field_records("chat_items_builder"):
                for name, value in record["fields"].items():
                    if value["path"] is not None:
                        builder_fields.append(self.fact("message_builder_field_projection", bdoc, value["node"],
                            field=name, source=value["path"], output_record_location=bdoc.location(node)))
        retained_roots = {value["target"]["root"] for value in retained}
        creation = []
        for assignment, left, right in assignments:
            record = self.record(document, right)
            if not {"createRequest", "inputKey", "created"}.issubset(record["fields"]):
                continue
            path = self.path(document, left)
            if path is not None:
                creation.append({"assignment_location": document.location(assignment), "target": path,
                    "record": self.public_record(document, record), "branch_context": self.a.branch_context(document, assignment, function)})
        attempt_aliases = [value for value in aliases if value["target"]["root"] in roots and not value["source"]["members"]
            and any(initial["target"]["root"] == value["source"]["root"] for initial in creation)]
        builder_calls = self.calls(document, nodes, "workItemsCreateCommand")
        builder_links = [self.call_relation("chat_create", document, call, "chat_items_builder") for call in builder_calls]
        expected_emissions = {("createRequest",), ("itemsRequest",), ("startRequest",)}
        base_supported = bool(len(delivery) == 1 and send_fields == expected_emissions and len(delivery_projections) >= 2
            and len(comparisons) >= 2 and len(creation) == 1 and len(attempt_aliases) == 1
            and len(retained_roots) == 1 and retained_roots == roots and builder_fields
            and len(builder_links) == 1 and builder_links[0]["supported"])
        result = {"supported": base_supported, "delivery_projection": delivery,
            "emitted_request_fields": [list(path) for path in sorted(send_fields)], "emissions": emissions,
            "retained_request_assignments": retained, "local_binding_projections": aliases,
            "delivery_record_projections": delivery_projections, "response_request_id_comparisons": comparisons,
            "builder_field_projections": builder_fields,
            "initial_attempt_assignments": creation, "current_attempt_aliases": attempt_aliases,
            "builder_call_relations": builder_links,
            "scope": "one captured Chat create body and its selected fixed-record builder; requests are separate identities linked through the retained delivery field",
            "runtime_retry_or_transport_proven": False, "all_chat_commands_covered": False}
        if not base_supported:
            self.gap("message_chat_selected_identity_slice_incomplete", document, function,
                derived_counts={"delivery_aliases": len(delivery), "request_projection_sets": len(send_fields),
                    "delivery_record_projections": len(delivery_projections), "response_comparisons": len(comparisons),
                    "initial_attempt_records": len(creation), "retained_roots": len(retained_roots), "builder_fields": len(builder_fields)})
        return result

    def worker(self) -> dict:
        dispatch = self.enum_consumers("worker_control")
        components = {}
        for role in ("run_key_from_dispatch", "worker_start", "adapter_ensure_thread", "adapter_submit", "adapter_persist", "adapter_session_for_thread", "session_identity", "adapter_profile"):
            item = self.body(role)
            if item is None:
                components[role] = {"supported": False}
                continue
            document, _, function, nodes = item
            records = self.field_records(role)
            projections = []
            for node, record in records:
                for name, value in record["fields"].items():
                    if value["path"] is not None:
                        projections.append(self.fact("message_record_field_projection", document, value["node"], role=role,
                            field=name, source=value["path"], record_location=document.location(node),
                            record_type_source=record.get("type_source"), ordinary_generated_record_clone_model_required=True))
            field_names = {value["field"] for value in projections}
            callback_projections = []
            if role == "adapter_session_for_thread":
                for call in self.calls(document, nodes, "map"):
                    callback = _u(self.arg(call, 0))
                    if callback is None or callback.type != "closure_expression":
                        continue
                    body = _f(callback, "body")
                    path = self.path(document, body)
                    if path is not None:
                        callback_projections.append(self.fact("message_deferred_map_field_projection", document, callback,
                            role=role, source=path, receiver_source=document.text(_f(_f(call, "function"), "value")),
                            source_callback_parameter=True, callback_activation_proven=False,
                            normal_option_map_model_required=True))
            calls = []
            for name in {"ensure_thread", "reconcile_turn_exact", "persist_run", "save_run", "create_session", "run_key_for_thread", "production_agent_session_config", "resolve_agent_session_config"}:
                for call in self.calls(document, nodes, name):
                    calls.append(self.fact("message_interface_argument_projections", document, call, role=role,
                        method_source_name=name, callee_source=document.text(_f(call, "function")),
                        arguments=[{"location": document.location(arg), "source_path": self.path(document, arg),
                            "record": self.public_record(document, self.record(document, arg)) if _u(arg).type in {"object", "struct_expression"} else None}
                            for arg in _c(_f(call, "arguments"))],
                        branch_context=self.a.branch_context(document, call, function), runtime_dispatch_proven=False))
            writes = []
            for assignment, left, right in self.assignments(document, nodes):
                path = self.path(document, left)
                if path is not None and path["members"]:
                    writes.append(self.fact("message_record_field_assignment", document, assignment, role=role,
                        target=path, value_source=self.a.expression(document, right),
                        branch_context=self.a.branch_context(document, assignment, function), durable_commit_proven=False))
            ordered = []
            submission_joins = []
            if role == "adapter_submit":
                intents = [value for value in writes if value["target"]["members"][-1:] == ["phase"]
                    and "SubmissionIntent" in json.dumps(value["value_source"])]
                persists = [value for value in calls if value["method_source_name"] == "persist_run"]
                reconciles = [value for value in calls if value["method_source_name"] == "reconcile_turn_exact"]
                for intent in intents:
                    for persist in persists:
                        for reconcile in reconciles:
                            locations = [value["location"] for value in (intent, persist, reconcile)]
                            if locations[0]["start_byte"] < locations[1]["start_byte"] < locations[2]["start_byte"]:
                                ordered.append(self.fact("message_submission_intent_persist_reconcile_order", document, function,
                                    intent_fact_id=intent["id"], persist_fact_id=persist["id"], reconcile_fact_id=reconcile["id"],
                                    same_selected_body=True, normal_reaching_required=True,
                                    crash_consistency_or_exactly_once_proven=False))
                for reconcile in self.calls(document, nodes, "reconcile_turn_exact"):
                    session_argument = self.path(document, self.arg(reconcile, 0))
                    submission_argument = self.path(document, self.arg(reconcile, 1))
                    goal_argument = self.path(document, self.arg(reconcile, 2))
                    session_declarations = [(left, right) for _, left, right in self.assignments(document, nodes)
                        if self.same(document, left, self.arg(reconcile, 0))]
                    session_calls = [call for _, right in session_declarations
                        for call in self.calls(document, self.nodes(document, right), "session_for_thread")]
                    tuple_candidates = []
                    for declaration in (part for part in nodes if part.type == "let_declaration"):
                        pattern = _f(declaration, "pattern")
                        if pattern is None or pattern.type != "tuple_pattern":
                            continue
                        binders = _c(pattern)
                        if len(binders) != 2 or submission_argument is None or document.text(binders[1]) != submission_argument["root_name"]:
                            continue
                        outputs = []
                        for candidate in self.nodes(document, _f(declaration, "value")):
                            if candidate.type != "tuple_expression" or len(_c(candidate)) != 2:
                                continue
                            projection = self.path(document, _c(candidate)[1])
                            if projection is not None:
                                outputs.append({"source": projection, "tuple_location": document.location(candidate),
                                    "branch_context": self.a.branch_context(document, candidate, function)})
                        if outputs:
                            tuple_candidates.append({"declaration_location": document.location(declaration),
                                "output_binding_location": document.location(binders[1]), "second_output_projections": outputs,
                                "all_captured_tuple_outputs_use_stored_submission_id": all(value["source"]["members"][-2:] == ["record", "submission_id"] for value in outputs)})
                    session_links = [self.call_relation(role, document, call, "adapter_session_for_thread") for call in session_calls]
                    persisted_keys = [self.path(document, self.arg(call, 0)) for call in self.calls(document, nodes, "persist_run")]
                    run_keys = [self.path(document, self.arg(call, 0)) for call in self.calls(document, nodes, "get_mut")
                        if (self.path(document, _f(_f(call, "function"), "value")) or {}).get("members") == ["runs"]]
                    same_run_key = bool(len(persisted_keys) == 1 and run_keys and persisted_keys[0] is not None
                        and all(value is not None and value["root"] == persisted_keys[0]["root"] and value["members"] == persisted_keys[0]["members"] for value in run_keys))
                    joined = bool(session_argument is not None and submission_argument is not None and goal_argument is not None
                        and len(session_links) == 1 and session_links[0]["supported"] and len(tuple_candidates) == 1
                        and tuple_candidates[0]["all_captured_tuple_outputs_use_stored_submission_id"] and same_run_key)
                    submission_joins.append(self.fact("message_stored_submission_identity_reconcile_source_join", document, reconcile,
                        session_argument=session_argument, submission_id_argument=submission_argument, goal_argument=goal_argument,
                        session_lookup_relations=session_links, stored_submission_tuple_sources=tuple_candidates,
                        same_selected_run_lookup_and_persist_key=same_run_key,
                        supported=joined, history_or_runtime_turn_identity_proven=False))
            required = {"run_key_from_dispatch": {"job_id", "attempt", "fencing_token", "payload_digest"},
                "worker_start": {"run_key", "job", "lease", "worker_session_id", "workspace", "workspace_revision"},
                "adapter_ensure_thread": {"job", "kernel_session_id", "canonical_thread_id", "worker_session_id"},
                "session_identity": {"codex_thread_id", "worker_session_id"}}
            supported = required.get(role, set()).issubset(field_names)
            if role == "adapter_submit":
                supported = bool(ordered and submission_joins and all(value["supported"] for value in submission_joins)
                    and any(value["method_source_name"] == "run_key_for_thread" for value in calls))
            if role == "adapter_persist":
                supported = any(value["method_source_name"] == "save_run" and len(value["arguments"]) == 2
                    and all(arg["source_path"] is not None for arg in value["arguments"]) for value in calls)
            if role == "adapter_session_for_thread":
                supported = bool(calls and any(value["source"]["members"][-2:] == ["record", "kernel_session_id"] for value in callback_projections))
            if role == "run_key_from_dispatch":
                selected = [value for value in projections if value["field"] in required[role]]
                expected = {"job_id": ["job", "job_id"], "attempt": ["job", "attempt"],
                    "fencing_token": ["lease", "fencing_token"], "payload_digest": ["job", "payload_digest"]}
                supported = supported and len({value["source"]["root"] for value in selected}) == 1 and len(selected) == 4
                supported = supported and all(value["source"]["members"] == expected[value["field"]] for value in selected)
            if role == "worker_start":
                selected = [value for value in projections if value.get("record_type_source") == "CodexThreadStart"]
                roots = {value["field"]: value["source"] for value in selected}
                supported = (supported and set(required[role]).issubset(roots)
                    and roots["job"]["root"] == roots["lease"]["root"]
                    and roots["job"]["members"] == ["job"] and roots["lease"]["members"] == ["lease"]
                    and len({roots[name]["root"] for name in ("worker_session_id", "workspace", "workspace_revision")}) == 1)
            if role == "adapter_profile":
                selected = [value for value in calls if value["method_source_name"] == "resolve_agent_session_config"]
                supported = bool(len(selected) == 1 and len(selected[0]["arguments"]) >= 3
                    and selected[0]["arguments"][2]["source_path"] is not None
                    and selected[0]["arguments"][2]["source_path"]["members"] == ["execution_profile"])
            components[role] = {"supported": bool(supported), "field_projections": projections,
                "interface_arguments": calls, "record_writes": writes, "normal_orders": ordered,
                "deferred_callback_projections": callback_projections,
                "submission_identity_source_joins": submission_joins}
            if not supported:
                self.gap("message_worker_selected_component_incomplete", document, function, role=role,
                    captured_field_names=sorted(field_names), missing_fields=sorted(required.get(role, set()) - field_names))
        typed_job = [value for value in dispatch if value["constructor"].endswith("::JobDispatchMessage")
            and any(consumer["callee_source"].endswith("accept_dispatch") for consumer in value["consumers"])]
        dispatch_item = self.body("worker_dispatch")
        dispatch_links = []
        if dispatch_item is not None:
            document, _, function, nodes = dispatch_item
            key_calls = self.calls(document, nodes, "from_dispatch")
            starts = self.calls(document, nodes, "start_dispatch")
            assignments = self.assignments(document, nodes)
            for key_call in key_calls:
                binder = next((left for _, left, right in assignments if _u(right) == key_call), None)
                if binder is None:
                    continue
                for start in starts:
                    same_dispatch = self.same(document, self.arg(key_call, 0), self.arg(start, 0))
                    same_run_key = self.same(document, binder, self.arg(start, 1))
                    key_relation = self.call_relation("worker_dispatch", document, key_call, "run_key_from_dispatch")
                    start_relation = self.call_relation("worker_dispatch", document, start, "worker_start")
                    dispatch_links.append(self.fact("message_dispatch_run_key_start_source_join", document, start,
                        same_dispatch_parameter_source=same_dispatch, same_local_run_key_source=same_run_key,
                        key_constructor_relation=key_relation, start_interface_relation=start_relation,
                        dispatch_argument=self.path(document, self.arg(start, 0)), run_key_argument=self.path(document, self.arg(start, 1)),
                        supported=bool(same_dispatch and same_run_key and key_relation["supported"] and start_relation["supported"]),
                        runtime_values_proven=False))
        if not dispatch_links or not all(value["supported"] for value in dispatch_links):
            self.gap("message_dispatch_run_key_source_join_incomplete")
        ensure = self.body("adapter_ensure_thread")
        profile_links = []
        if ensure is not None:
            document, _, function, nodes = ensure
            for call in self.calls(document, nodes, "production_agent_session_config"):
                path = self.path(document, self.arg(call, 2))
                relation = self.call_relation("adapter_ensure_thread", document, call, "adapter_profile")
                profile_links.append(self.fact("message_adapter_job_profile_consumer_source_join", document, call,
                    source_job=path, profile_consumer_relation=relation,
                    supported=bool(path is not None and path["members"] == ["job"] and relation["supported"]),
                    profile_settings_or_provider_success_proven=False))
        return {"supported": bool(typed_job and dispatch_links and all(value["supported"] for value in dispatch_links)
                and profile_links and all(value["supported"] for value in profile_links)
                and all(value["supported"] for value in components.values())),
            "typed_message_consumers": dispatch, "components": components,
            "dispatch_run_key_source_joins": dispatch_links,
            "profile_consumer_source_joins": profile_links,
            "scope": "captured typed JobDispatch arm, explicit borrowed start record, selected adapter run and Kernel session/turn interfaces",
            "generic_codex_receiver_globally_bound": False, "execution_profile_projection_to_selected_consumer_only": True,
            "all_profile_settings_fully_traced": False,
            "kernel_session_equals_product_or_worker_session": False,
            "authority_and_result_values_proven": False, "all_worker_messages_covered": False}

    def correlations(self, role: str) -> list[dict]:
        item = self.body(role)
        if item is None:
            return []
        document, _, function, nodes = item
        records = []
        for arm in (node for node in nodes if node.type == "match_arm"):
            pattern = _f(arm, "pattern") or next(iter(_c(arm)), None)
            value = _f(arm, "value")
            if pattern is None or value is None:
                continue
            constructors = [part for part in self.nodes(document, pattern) if part.type in {"scoped_identifier", "scoped_type_identifier"}
                and document.text(part).startswith("ExecutionPortMessage::")]
            families = [part for part in self.nodes(document, value) if part.type == "scoped_identifier"
                and document.text(part).startswith("Family::")]
            calls = self.calls(document, self.nodes(document, value), "correlation")
            if len(constructors) != 1 or len(families) != 1 or len(calls) != 1:
                continue
            argument = _u(self.arg(calls[0], 0))
            if argument is None or argument.type != "tuple_expression":
                continue
            projections = [self.path(document, part) for part in _c(argument)]
            helper = self.call_relation(role, document, calls[0], "outbox_correlate")
            closed = bool(projections and all(part is not None and part["binding"].get("declaration_kind") == "captured_rust_enum_arm" for part in projections)
                and len({part["root"] for part in projections if part is not None}) == 1 and helper["supported"])
            records.append(self.fact("message_typed_correlation_projection", document, arm, role=role,
                message_variant=document.text(constructors[0]), family=document.text(families[0]),
                ordered_fields=projections, source_shape_closed=closed,
                correlation_call_location=document.location(calls[0]),
                selected_correlation_helper=helper,
                conditional_match_arm_source=document.text(pattern),
                equal_payload_values_assumed=False, hash_collision_freedom_proven=False))
        return records

    def sql_source(self, role: str) -> list[dict]:
        item = self.body(role)
        if item is None:
            return []
        document, _, function, nodes = item
        result = []
        for call in self.calls(document, nodes, "execute"):
            sql_node = _u(self.arg(call, 0))
            sql = _literal_string(document.text(sql_node)) if sql_node is not None else None
            params = _u(self.arg(call, 1))
            if sql is None or params is None or params.type != "macro_invocation":
                continue
            macro = _f(params, "macro") or next(iter(_c(params)), None)
            tree = next((part for part in _c(params) if part.type == "token_tree"), None)
            if macro is None or document.text(macro) != "params" or tree is None:
                continue
            groups, group = [], []
            for child in tree.children:
                if child.type in {"[", "]"}:
                    continue
                if child.type == ",":
                    if group:
                        groups.append(group)
                    group = []
                else:
                    group.append(child)
            if group:
                groups.append(group)
            arguments = []
            for index, group in enumerate(groups, 1):
                text = document.data[group[0].start_byte:group[-1].end_byte].decode("utf-8")
                # Restricted macro token grammar.  No macro expansion or Rust
                # execution is inferred; unsupported calls retain raw syntax.
                simple = re.fullmatch(r"\s*([A-Za-z_][A-Za-z_0-9]*)(\s*\.\s*[A-Za-z_][A-Za-z_0-9]*)*\s*", text)
                arguments.append({"position": index, "source": text,
                    "captured_simple_member_path": re.split(r"\s*\.\s*", text.strip()) if simple else None,
                    "source_root_binding": self.identity(document, group[0]) if group[0].type in {"identifier", "self"} else None,
                    "macro_expansion_or_runtime_value_proven": False,
                    "token_span": {"start_byte": group[0].start_byte, "end_byte": group[-1].end_byte}})
            result.append(self.fact("message_literal_sql_positional_source", document, call, role=role,
                sql=sql, placeholders=sorted(set(re.findall(r"\?([1-9][0-9]*)", sql))),
                arguments=arguments, params_macro_location=document.location(params),
                source_binding_model=SQL_MODEL, sql_executed=False, durable_effect_proven=False))
        return result

    def outbox(self) -> dict:
        requests = self.correlations("outbox_metadata")
        responses = self.correlations("outbox_response_target")
        pairs = []
        for request in requests:
            if not request["source_shape_closed"]:
                continue
            for response in responses:
                if not response["source_shape_closed"] or request["family"] != response["family"]:
                    continue
                rkeys = [part["members"] for part in request["ordered_fields"]]
                akeys = [part["members"] for part in response["ordered_fields"]]
                if rkeys != akeys:
                    continue
                pairs.append({"relation_kind": "request_response_correlation_projection_agreement",
                    "request_fact_id": request["id"], "response_fact_id": response["id"],
                    "request_variant": request["message_variant"], "response_variant": response["message_variant"],
                    "family": request["family"], "ordered_field_paths": rkeys,
                    "agreement_domain": "ordered field projections passed to the captured same correlation helper",
                    "equal_wire_values_or_accepted_response_proven": False, "creates_calls_edge": False})
        sql = {role: self.sql_source(role) for role in ("outbox_retain", "outbox_ack")}
        correlation = self.body("outbox_correlate")
        codec = []
        if correlation is not None:
            document, _, function, nodes = correlation
            for call in self.calls(document, nodes, "to_vec") + self.calls(document, nodes, "digest"):
                codec.append(self.fact("message_correlation_codec_operand", document, call,
                    callee_source=document.text(_f(call, "function")),
                    arguments=[self.a.expression(document, arg) for arg in _c(_f(call, "arguments"))],
                    codec_runtime_or_digest_collision_proven=False))
        ack = self.body("outbox_ack")
        guard_facts = []
        if ack is not None:
            document, _, function, nodes = ack
            for call in self.calls(document, nodes, "accepted_response") + self.calls(document, nodes, "response_target"):
                guard_facts.append(self.fact("message_ack_authority_source_guard", document, call,
                    arguments=[self.a.expression(document, arg) for arg in _c(_f(call, "arguments"))],
                    branch_context=self.a.branch_context(document, call, function),
                    caller_supplied_domain_validation_independently_proven=False))
        deletion = [fact for fact in sql["outbox_ack"] if re.search(r"DELETE\s+FROM\s+execution_outbox\s+WHERE\s+family\s*=\s*\?1\s+AND\s+correlation_key\s*=\s*\?2", fact["sql"], re.I)
            and "acknowledgement_required = 1" in fact["sql"]]
        insertion = [fact for fact in sql["outbox_retain"] if "INSERT INTO execution_outbox" in fact["sql"] and "frame_json" in fact["sql"]]
        retain_joins = []
        retain = self.body("outbox_retain")
        if retain is not None:
            document, _, function, nodes = retain
            assignments = self.assignments(document, nodes)
            encodes = self.calls(document, nodes, "to_vec")
            metadata_calls = self.calls(document, nodes, "metadata")
            for encode in encodes:
                frame = next((left for _, left, right in assignments if right is not None and _inside(right, encode)), None)
                if frame is None:
                    continue
                for metadata_call in metadata_calls:
                    meta = next((left for _, left, right in assignments if right is not None and _inside(right, metadata_call)), None)
                    same_message = self.same(document, self.arg(encode, 0), self.arg(metadata_call, 0))
                    same_frame = self.same(document, frame, self.arg(metadata_call, 1))
                    helper = self.call_relation("outbox_retain", document, metadata_call, "outbox_metadata")
                    for insert in insertion:
                        match = re.search(r"INSERT\s+INTO\s+execution_outbox\s*\((.*?)\)\s*VALUES\s*\((.*?)\)", insert["sql"], re.I | re.S)
                        columns = [part.strip() for part in match[1].split(",")] if match else []
                        placeholders = [part.strip() for part in match[2].split(",")] if match else []
                        positional, positional_ids = {}, {}
                        for column, placeholder in zip(columns, placeholders):
                            position = int(placeholder[1:]) if re.fullmatch(r"\?[1-9][0-9]*", placeholder) else 0
                            if 1 <= position <= len(insert["arguments"]):
                                positional[column] = re.sub(r"\s+", "", insert["arguments"][position - 1]["source"])
                                positional_ids[column] = (insert["arguments"][position - 1].get("source_root_binding") or {}).get("declaration_id")
                        expected_meta = document.text(meta) if meta is not None else ""
                        expected_frame = document.text(frame)
                        projected = {name: positional.get(name) == expected_meta + "." + name
                            for name in ("delivery_id", "family", "correlation_key")}
                        projected["frame_json"] = positional.get("frame_json") == expected_frame
                        meta_id = self.identity(document, meta).get("declaration_id")
                        frame_id = self.identity(document, frame).get("declaration_id")
                        same_binders = bool(meta_id and frame_id and all(positional_ids.get(name) == meta_id
                            for name in ("delivery_id", "family", "correlation_key")) and positional_ids.get("frame_json") == frame_id)
                        retain_joins.append(self.fact("message_frame_metadata_insert_source_join", document, encode,
                            same_message_parameter=same_message, same_encoded_frame_binding=same_frame,
                            metadata_helper_relation=helper, sql_fact_id=insert["id"],
                            sql_column_argument_sources=positional, metadata_and_frame_projections=projected,
                            source_column_binder_ids=positional_ids, same_captured_sql_binders=same_binders,
                            supported=bool(meta is not None and same_message and same_frame and helper["supported"] and same_binders and all(projected.values())),
                            standard_serde_codec_and_normal_sql_model_required=True,
                            stored_bytes_or_physical_transaction_success_proven=False))
        deletion_bindings = []
        if ack is not None:
            document, _, function, nodes = ack
            declarations = [node for node in nodes if node.type == "let_declaration"
                and any(call.type == "call_expression" for call in self.calls(document, self.nodes(document, _f(node, "value")), "response_target"))]
            for declaration in declarations:
                pattern = _f(declaration, "pattern")
                binders = [node for node in self.nodes(document, pattern) if node.type == "identifier"
                    and not (node.parent is not None and node.parent.type == "tuple_struct_pattern" and _f(node.parent, "type") == node)]
                for fact in deletion:
                    args = fact["arguments"]
                    if len(binders) == 2 and len(args) == 2:
                        expected = [document.text(binder) for binder in binders]
                        first = re.sub(r"\s+", "", args[0]["source"])
                        second = re.sub(r"\s+", "", args[1]["source"])
                        expected_ids = [self.identity(document, binder).get("declaration_id") for binder in binders]
                        actual_ids = [(arg.get("source_root_binding") or {}).get("declaration_id") for arg in args]
                        supported = (first == expected[0] + ".as_str()" and second == expected[1]
                            and all(expected_ids) and expected_ids == actual_ids)
                        deletion_bindings.append(self.fact("message_ack_return_tuple_sql_parameter_binding", document, declaration,
                            tuple_binders=[document.location(binder) for binder in binders],
                            returned_family_sql_position=1, returned_correlation_sql_position=2,
                            sql_fact_id=fact["id"], supported=supported,
                            returned_binder_ids=expected_ids, sql_argument_binder_ids=actual_ids,
                            restricted_macro_tokens_only=True, value_or_database_effect_proven=False))
        supported = bool(pairs and insertion and retain_joins and all(value["supported"] for value in retain_joins)
            and deletion and deletion_bindings and all(value["supported"] for value in deletion_bindings)
            and len(codec) >= 2 and len(guard_facts) >= 2)
        if not supported:
            self.gap("message_outbox_selected_correlation_slice_incomplete", pairs=len(pairs), insertions=len(insertion), deletions=len(deletion), codec_steps=len(codec), guards=len(guard_facts))
        return {"supported": supported, "request_projections": requests, "response_projections": responses,
            "projection_agreements": pairs, "sql_positional_sources": sql, "correlation_codec_sources": codec,
            "ack_gate_sources": guard_facts, "scope": "only closed enum-arm direct tuple correlations and literal outbox insert/delete source seams",
            "ack_return_tuple_sql_bindings": deletion_bindings,
            "frame_metadata_sql_insert_joins": retain_joins,
            "all_message_families_covered": False, "outcome_helper_tuple_expanded": False,
            "sequence_to_ack_sequence_rename_value_proven": False,
            "external_ack_truth_or_exactly_once_proven": False, "physical_store_commit_proven": False}

    def run(self) -> dict:
        if "chat_create" in self.a.roles:
            self.parts["chat_request_identity"] = self.chat()
        if "worker_control" in self.a.roles:
            self.parts["worker_adapter_identity"] = self.worker()
        if "outbox_metadata" in self.a.roles:
            self.parts["outbox_ack_correlation"] = self.outbox()
        if not self.parts:
            self.gap("message_identity_pattern_has_no_recognized_role_group")
        if self.incomplete:
            self.gap("message_identity_operation_budget_exceeded", limit=_LIMIT, operations=self.operations)
        models = set(self.a.rule.get("models", []))
        required_models = {MODEL} | ({SQL_MODEL} if "outbox_ack_correlation" in self.parts else set())
        if not required_models.issubset(models):
            self.gap("message_identity_model_not_registered", missing=sorted(required_models - models))
        return {"version": VERSION, "components": self.parts,
            "scoped_source_supported": bool(self.parts and all(part["supported"] for part in self.parts.values())
                and required_models.issubset(models) and not self.incomplete),
            "relation_fact_ids": [value["id"] for value in self.relations],
            "budget": {"operations": self.operations, "limit": _LIMIT, "incomplete": self.incomplete},
            "proof_domain": "captured lexical binders, finite field/record projections, enum arms and registered literal SQL source bindings",
            "models": sorted(required_models), "source_only": True, "creates_calls_edge": False,
            "runtime_transport_or_physical_effect_proven": False, "whole_project_identity_complete": False,
            "limits": ["member paths identify source projections, not globally stable heap cells",
                "Rust Clone/borrow projections require ordinary generated data semantics; arbitrary trait behavior is not inferred",
                "generic adapter calls remain contextual source interfaces, never global unique targets",
                "correlation tuple agreement is a field-domain agreement; payload equality is checked by source consumers, not assumed",
                "SQL parameters are captured token positions under the registered literal source model; no database is executed",
                "retries, rejected/replayed acks, all crash windows and external authenticity are not fully proved"]}


def analyze_pattern(analysis: Any) -> dict:
    """Return conditional source relations for data-only selected role groups."""
    return _Messages(analysis).run()
