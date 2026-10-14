"""Finite record, codec and projection relations from authenticated saved CST.

The caller supplies an already loaded report analysis.  Role locators are data;
expected edges, fields, branches and successful outcomes are never supplied by
policy.  This adapter emits lexical reference dependencies and source attempts,
not heap-equality, transaction, durable-success or command-execution theorems.
"""
from __future__ import annotations

from typing import Any

from .semantic_sources import unwrap
from .static_contracts import _literal_string

VERSION = "captured-record-projection-relations-1"
MODEL = "finite-record-codec-projection-source-v1"
KINDS = frozenset({"event_index_projection", "trusted_command_lineage", "unsupported_record_retention"})
_FUNCTIONS = frozenset({"function_declaration", "function_expression", "arrow_function", "method_definition"})
_IDS = frozenset({"identifier", "shorthand_property_identifier", "shorthand_property_identifier_pattern"})
_NODE_LIMIT = 100000


def _field(node: Any, key: str) -> Any:
    return node.child_by_field_name(key) if node is not None else None


def _children(node: Any) -> list[Any]:
    return [child for child in node.named_children if child.type not in {
        "comment", "type_annotation", "type_arguments", "type_parameters", "interface_declaration",
        "type_alias_declaration", "type_query", "import_type"} and not child.type.endswith("_type")] if node is not None else []


def _inside(outer: Any, inner: Any) -> bool:
    return bool(outer is not None and inner is not None and outer.start_byte <= inner.start_byte and inner.end_byte <= outer.end_byte)


def _operand(node: Any) -> Any:
    node = unwrap(node)
    while node is not None and node.type == "await_expression":
        node = unwrap(next(iter(_children(node)), None))
    return node


def _ancestors(node: Any):
    while node is not None:
        yield node
        node = node.parent


class _Records:
    def __init__(self, analysis: Any):
        self.a = analysis
        self.roles = analysis.roles
        self.records: dict[str, list[dict]] = {role: [] for role in self.roles}
        self.calls: dict[str, list[dict]] = {role: [] for role in self.roles}
        self.call_nodes: dict[str, Any] = {}
        self.bindings: dict[str, list[dict]] = {role: [] for role in self.roles}
        self.returns: dict[str, list[dict]] = {role: [] for role in self.roles}
        self.assignments: dict[str, list[dict]] = {role: [] for role in self.roles}
        self.guards: dict[str, list[dict]] = {role: [] for role in self.roles}
        self.operations = 0
        self.incomplete = False
        self.identity_cache: dict[tuple[str, int], dict] = {}
        self.expr_cache: dict[tuple[str, int], dict] = {}
        self.binding_nodes: dict[tuple[str, str], Any] = {}

    def fact(self, kind: str, document: Any, node: Any, **details: Any) -> dict:
        return self.a.fact(kind, document, node, record_relations_version=VERSION, **details)

    def identity(self, document: Any, node: Any) -> dict:
        node = unwrap(node)
        if node is None or node.type not in _IDS:
            return {}
        key = (document.source.path, node.id)
        if key not in self.identity_cache:
            raw = self.a.lexical(document).resolve_identity(node)
            self.identity_cache[key] = {key: raw.get(key) for key in (
                "state", "declaration_id", "declaration_kind", "declaration_location", "binder_location",
                "identity_complete", "binding_path", "parameter_index")}
        return self.identity_cache[key]

    def path(self, document: Any, node: Any) -> dict | None:
        node = _operand(node)
        if node is None:
            return None
        if node.type in _IDS:
            identity = self.identity(document, node)
            return {"binding_id": identity["declaration_id"], "members": [], "binding": identity} if identity.get("state") == "unique" and identity.get("declaration_id") else None
        if node.type in {"member_expression", "subscript_expression"}:
            base = self.path(document, _field(node, "object"))
            prop = _field(node, "property") if node.type == "member_expression" else unwrap(_field(node, "index"))
            key = self.key(document, prop) if node.type == "member_expression" or prop is not None and prop.type == "string" else None
            return {**base, "members": [*base["members"], key]} if base and key is not None else None
        return None

    def key(self, document: Any, node: Any) -> str | None:
        if node is None:
            return None
        if node.type in _IDS | {"property_identifier"}:
            raw = document.text(node)
            return raw if "\\" not in raw else None
        return _literal_string(document.text(node)) if node.type == "string" else None

    def expression(self, document: Any, node: Any) -> dict:
        node = _operand(node)
        if node is None:
            return {"kind": "missing"}
        key = (document.source.path, node.id)
        if key in self.expr_cache:
            return self.expr_cache[key]
        refs = []
        # Each use is joined by captured binder identity, never name equality.
        for part in self.a.nodes(document, node):
            if part.type in _IDS:
                identity = self.identity(document, part)
                refs.append({"location": document.location(part), "name": document.text(part), **identity})
        result = {"kind": node.type, "location": document.location(node), "source": document.text(node)[:8192],
            "source_truncated": len(document.text(node)) > 8192, "reference_path": self.path(document, node),
            "references": refs, "reference_dependencies_only": True, "runtime_value_or_heap_identity_proven": False}
        self.expr_cache[key] = result
        return result

    def context(self, document: Any, node: Any, root: Any) -> dict:
        owner = next((parent for parent in _ancestors(node.parent) if parent.type in _FUNCTIONS), root)
        callbacks = [document.location(parent) for parent in _ancestors(node.parent)
            if parent != root and parent.type in _FUNCTIONS and _inside(root, parent)]
        return {"lexical_owner_location": document.location(owner), "nested_callable_locations": callbacks,
            "callback_activation_proven": False, "branch_context": self.a.branch_context(document, node, owner)}

    def record(self, document: Any, node: Any, role: str, function: Any) -> dict:
        fields, overwrites = [], []
        preceding: set[str] = set()
        spreads = []
        for index, member in enumerate(_children(node)):
            key, value = None, None
            if member.type == "pair":
                key, value = self.key(document, _field(member, "key")), _field(member, "value")
            elif member.type in _IDS:
                key, value = self.key(document, member), member
            elif member.type == "spread_element":
                value = next(iter(_children(member)), None)
                spreads.append({"index": index, "location": document.location(member),
                    "expression": self.expression(document, value), "can_override_preceding_fields": bool(preceding),
                    "preceding_keys": sorted(preceding), "actual_runtime_keys_proven": False})
                continue
            fields.append({"index": index, "key": key, "value": self.expression(document, value),
                "location": document.location(member), "overrides_previous_explicit_key": key in preceding if key else False})
            if key in preceding:
                overwrites.append(key)
            if key is not None:
                preceding.add(key)
        return self.fact("ordered_record_field_source", document, node, role=role,
            fields=fields, spreads=spreads, repeated_explicit_keys=overwrites,
            fixed_explicit_shape=not spreads and all(item["key"] is not None for item in fields) and not overwrites,
            **self.context(document, node, function), final_runtime_field_values_proven=False)

    def scan(self) -> None:
        for role, (document, definition, function) in self.roles.items():
            nodes = self.a.nodes(document, _field(function, "body"), nested=True)
            for node in nodes:
                self.operations += 1
                if self.operations > _NODE_LIMIT:
                    self.incomplete = True
                    self.a.gap("record_relations_ast_budget_exceeded", document, node)
                    return
                context = self.context(document, node, function)
                if node.type == "object":
                    self.records[role].append(self.record(document, node, role, function))
                elif node.type == "variable_declarator":
                    binder, value = _field(node, "name"), _field(node, "value")
                    names = [part for part in self.a.nodes(document, binder) if part.type in _IDS]
                    for name in names:
                        identity = self.identity(document, name)
                        if identity.get("state") == "unique" and identity.get("declaration_id"):
                            self.binding_nodes[(role, identity["declaration_id"])] = node
                    self.bindings[role].append(self.fact("record_local_binding_source", document, node, role=role,
                        bindings=[{"name": document.text(name), **self.identity(document, name)} for name in names],
                        binder_source=document.text(binder), initializer=self.expression(document, value),
                        **context, reaching_value_or_no_overwrite_proven=False))
                elif node.type in {"assignment_expression", "augmented_assignment_expression"}:
                    self.assignments[role].append(self.fact("record_assignment_source_attempt", document, node, role=role,
                        left=self.expression(document, _field(node, "left")), right=self.expression(document, _field(node, "right")),
                        **context, assignment_success_proven=False))
                elif node.type in {"return_statement", "throw_statement", "continue_statement"}:
                    value = _field(node, "argument") or next(iter(_children(node)), None)
                    self.returns[role].append(self.fact("record_completion_source", document, node, role=role,
                        completion_kind=node.type, expression=self.expression(document, value), **context,
                        activation_or_completion_proven=False))
                elif node.type == "if_statement":
                    self.guards[role].append(self.fact("record_conditional_guard_source", document, node, role=role,
                        condition=self.expression(document, _field(node, "condition")),
                        then_location=document.location(_field(node, "consequence")) if _field(node, "consequence") is not None else None,
                        else_location=document.location(_field(node, "alternative")) if _field(node, "alternative") is not None else None,
                        **context, predicate_truth_proven=False))
                elif node.type == "call_expression":
                    callee = _field(node, "function")
                    args = _children(_field(node, "arguments"))
                    owner = document.call_owner(node)
                    candidates = document.definition_nodes.get(owner, [])
                    actual_owner = candidates[0] if len(candidates) == 1 else definition
                    edge, issues = self.a.sources.call_binding(node, document, actual_owner)
                    fact = self.fact("record_call_source_attempt", document, node, role=role,
                        callee_source=document.text(callee), callee=self.expression(document, callee),
                        arguments=[self.expression(document, arg) for arg in args],
                        authenticated_call_edge_id=edge.id if edge is not None else None,
                        actual_callee_graph_node_id=edge.target if edge is not None else None,
                        owner_graph_node_id=owner, binding_gaps=issues, **context,
                        execution_or_effect_success_proven=False)
                    self.calls[role].append(fact)
                    self.call_nodes[fact["id"]] = node

    def links(self) -> list[dict]:
        roles_by_id = {definition.graph_node_id: role for role, (_, definition, _) in self.roles.items()}
        result = []
        for role, calls in self.calls.items():
            document, _, function = self.roles[role]
            for call in calls:
                target = roles_by_id.get(call["actual_callee_graph_node_id"])
                if target is None or not call["authenticated_call_edge_id"]:
                    continue
                node = self.call_nodes[call["id"]]
                target_document, _, target_function = self.roles[target]
                parameters = _children(_field(target_function, "parameters"))
                result.append(self.fact("record_authenticated_role_transfer_source", document, node,
                    from_role=role, to_role=target, call_fact_id=call["id"],
                    authenticated_call_edge_id=call["authenticated_call_edge_id"],
                    actual_callee_graph_node_id=call["actual_callee_graph_node_id"],
                    argument_formal_sources=[{"index": index, "actual": argument,
                        "formal_source": target_document.text(parameters[index]),
                        "formal_location": target_document.location(parameters[index])}
                        for index, argument in enumerate(call["arguments"]) if index < len(parameters)],
                    arguments_are_captured_source_only=True, callee_activation_or_value_preservation_proven=False))
        return result

    def calls_to(self, role: str, target: str) -> list[dict]:
        if target not in self.roles:
            return []
        graph_id = self.roles[target][1].graph_node_id
        return [call for call in self.calls.get(role, []) if call["actual_callee_graph_node_id"] == graph_id
            and call["authenticated_call_edge_id"]]

    def initializer(self, role: str, expression: Any) -> Any:
        document = self.roles[role][0]
        path = self.path(document, expression)
        declaration = self.binding_nodes.get((role, path["binding_id"])) if path and not path["members"] else None
        return _operand(_field(declaration, "value"))

    def is_target_call(self, role: str, expression: Any, target: str) -> bool:
        expression = _operand(expression)
        return expression is not None and any(self.call_nodes[call["id"]] == expression for call in self.calls_to(role, target))

    def collection_returns(self, role: str) -> list[dict]:
        """Join literal push records to returned collection references."""
        if role not in self.roles:
            return []
        document, _, function = self.roles[role]
        records_by_span = {(record["location"]["start_byte"], record["location"]["end_byte"]): record for record in self.records[role]}
        result = []
        for call in self.calls[role]:
            node = self.call_nodes[call["id"]]
            callee = _field(node, "function")
            path = self.path(document, callee)
            if not path or path["members"] != ["push"]:
                continue
            args = _children(_field(node, "arguments"))
            if len(args) != 1:
                continue
            record = records_by_span.get((args[0].start_byte, args[0].end_byte))
            if record is None:
                continue
            returned = []
            for completion in self.returns[role]:
                if completion["completion_kind"] != "return_statement" or completion["nested_callable_locations"]:
                    continue
                for reference in completion["expression"]["references"]:
                    if reference.get("declaration_id") == path["binding_id"]:
                        returned.append(completion["id"])
            if returned:
                result.append(self.fact("record_literal_collection_append_return_source", document, node, role=role,
                    collection_binding_id=path["binding_id"], record_fact_id=record["id"],
                    push_call_fact_id=call["id"], return_fact_ids=returned,
                    ordinary_array_push_required=True, record_reaches_return_on_normal_uninterrupted_path_only=True,
                    collection_mutation_durability_or_all_inputs_proven=False))
        return result

    def local_dependencies(self) -> list[dict]:
        result = []
        for role, (document, _, function) in self.roles.items():
            declarations = {identity["declaration_id"]: binding for binding in self.bindings[role]
                for identity in binding["bindings"] if identity.get("state") == "unique" and identity.get("declaration_id")}
            for call in self.calls[role]:
                node = self.call_nodes[call["id"]]
                for index, argument in enumerate(call["arguments"]):
                    for ref in argument["references"]:
                        binding = declarations.get(ref.get("declaration_id"))
                        if binding and binding["location"]["start_byte"] < call["location"]["start_byte"]:
                            result.append(self.fact("record_local_initializer_dependency", document, node, role=role,
                                call_fact_id=call["id"], argument_index=index,
                                local_binding_fact_id=binding["id"], declaration_id=ref["declaration_id"],
                                initializer=binding["initializer"],
                                dependency_kind="same_captured_lexical_declaration_reference",
                                intervening_writes_or_opaque_effects_excluded=False, value_preservation_proven=False))
        return result

    def callback_transfers(self) -> list[dict]:
        """Match literal callback actuals to calls of the same callee formal.

        This is a source seam.  It does not repair CALLS or claim the callback
        runs; its invocation arguments can nevertheless be inspected exactly.
        """
        result = []
        for role, calls in self.calls.items():
            document, _, function = self.roles[role]
            for call in calls:
                node = self.call_nodes[call["id"]]
                arguments = _children(_field(node, "arguments"))
                for target in self.roles:
                    if call not in self.calls_to(role, target):
                        continue
                    target_document, _, target_function = self.roles[target]
                    parameters = _children(_field(target_function, "parameters"))
                    for index, actual in enumerate(arguments):
                        actual = _operand(actual)
                        if index >= len(parameters) or actual is None or actual.type not in _FUNCTIONS:
                            continue
                        binder = _field(parameters[index], "pattern") or _field(parameters[index], "name")
                        identity = self.identity(target_document, binder)
                        matches = [candidate for candidate in self.calls[target]
                            if (candidate["callee"].get("reference_path") or {}).get("binding_id") == identity.get("declaration_id")]
                        if identity.get("state") != "unique" or not matches:
                            continue
                        result.append(self.fact("record_literal_callback_formal_invocation_source", document, actual,
                            from_role=role, provider_role=target, call_fact_id=call["id"], argument_index=index,
                            callback_parameter_source=document.text(_field(actual, "parameters")),
                            callback_location=document.location(actual), provider_formal=identity,
                            provider_invocation_fact_ids=[candidate["id"] for candidate in matches],
                            provider_invocation_arguments=[candidate["arguments"] for candidate in matches],
                            callback_activation_or_argument_runtime_identity_proven=False,
                            synthesized_call_edge=False))
        return result

    def normal_orders(self, role: str, left: str, right: str) -> list[dict]:
        """Order distinct statements in the same lexical block, not API effects."""
        if role not in self.roles:
            return []
        document, _, function = self.roles[role]
        result = []
        for first in self.calls_to(role, left):
            first_node = self.call_nodes[first["id"]]
            for second in self.calls_to(role, right):
                second_node = self.call_nodes[second["id"]]
                common = [parent for parent in _ancestors(first_node.parent) if parent.type == "statement_block" and _inside(parent, second_node)]
                if not common:
                    continue
                block = common[0]
                first_statement = next((node for node in _ancestors(first_node) if node.parent == block), None)
                second_statement = next((node for node in _ancestors(second_node) if node.parent == block), None)
                if first_statement is None or second_statement is None or first_statement.end_byte > second_statement.start_byte:
                    continue
                result.append(self.fact("record_conditional_normal_statement_order", document, second_statement,
                    role=role, before_call_fact_id=first["id"], after_call_fact_id=second["id"],
                    enclosing_block_location=document.location(block),
                    conditions=["the same captured invocation reaches both statements normally",
                        "earlier awaited calls complete normally and intervening guards allow continuation"],
                    transaction_or_commit_atomicity_proven=False, all_paths_reach_second_proven=False))
        return result

    def codec_calls(self) -> list[dict]:
        result = []
        for role, calls in self.calls.items():
            document = self.roles[role][0]
            for call in calls:
                callee = call["callee"]
                # Standard JSON is a registered source contract only if the
                # lexical name is the unshadowed global rather than a local.
                node = self.call_nodes[call["id"]]
                member = _field(node, "function")
                root = _field(member, "object")
                prop = _field(member, "property")
                codec = self.key(document, prop)
                if root is None or document.text(root) != "JSON" or codec not in {"parse", "stringify"}:
                    continue
                identity = self.identity(document, root)
                if identity.get("state") == "unique":
                    continue
                result.append(self.fact("record_json_codec_source_attempt", document, node, role=role,
                    call_fact_id=call["id"], codec=codec, arguments=call["arguments"],
                    model_id=MODEL, standard_global_required=True,
                    actual_json_serializability_roundtrip_or_write_success_proven=False))
        return result

    def summarize(self) -> dict:
        self.scan()
        return {"roles": sorted(self.roles), "role_transfers": self.links(),
            "local_initializer_dependencies": self.local_dependencies(),
            "literal_callback_transfers": self.callback_transfers(), "json_codec_attempts": self.codec_calls(),
            "record_fields": self.records, "local_bindings": self.bindings,
            "assignment_attempts": self.assignments, "completion_sources": self.returns,
            "guards": self.guards, "calls": self.calls,
            "operations": self.operations, "operation_limit": _NODE_LIMIT,
            "incomplete": self.incomplete}


def _explicit(record: dict, key: str, literal: str | None = None) -> bool:
    return any(item["key"] == key and (literal is None or item["value"]["source"] == literal) for item in record["fields"])


def _projection_fields(r: _Records) -> dict:
    """Derive the actual callback-state and replay-state record joins."""
    publication, replay, serialization = [], [], []
    for role in {"update", "rebuild"} & r.roles.keys():
        document, _, function = r.roles[role]
        for node in r.a.nodes(document, _field(function, "body"), nested=True):
            if node.type != "assignment_expression":
                continue
            left, right = _operand(_field(node, "left")), _operand(_field(node, "right"))
            if left is None or left.type != "subscript_expression":
                continue
            collection = r.path(document, _field(left, "object"))
            initializer = r.initializer(role, right)
            if not collection or initializer is None:
                continue
            if role == "update" and collection["members"] == ["jobs"] and initializer.type == "ternary_expression":
                consequence = r.path(document, _field(initializer, "consequence"))
                alternate = r.path(document, _field(initializer, "alternative"))
                owner = next((parent for parent in _ancestors(node.parent) if parent.type in _FUNCTIONS), function)
                parameter = next(iter(_children(_field(owner, "parameters"))), None)
                binder = _field(parameter, "pattern") or _field(parameter, "name") or parameter
                parameter_identity = r.identity(document, binder)
                condition = r.expression(document, _field(initializer, "condition"))
                if (consequence and consequence["members"] == ["state"] and consequence["binding_id"] == parameter_identity.get("declaration_id")
                        and alternate and not alternate["members"]):
                    writer_arguments = [call["arguments"][1].get("reference_path") for call in r.calls_to(role, "index_writer") if len(call["arguments"]) > 1]
                    same_record = [path for path in writer_arguments if path and path["binding_id"] == collection["binding_id"] and not path["members"]]
                    if same_record:
                        publication.append(r.fact("record_projection_state_to_index_writer_source", document, node,
                            callback_parameter=parameter_identity, projection_state_source=consequence,
                            fallback_state_source=alternate, selection_guard=condition,
                            assigned_collection_source=collection, selected_record_key_source=document.text(_field(left, "index")),
                            writer_call_fact_ids=[call["id"] for call in r.calls_to(role, "index_writer")],
                            source_assignment_and_writer_reference_connected=True,
                            heap_preservation_lock_activation_or_physical_publish_proven=False))
            elif role == "rebuild" and r.is_target_call(role, initializer, "materializer"):
                arguments = _children(_field(initializer, "arguments"))
                input_initializer = r.initializer(role, arguments[0]) if arguments else None
                if not r.is_target_call(role, input_initializer, "event_reader"):
                    continue
                # The rebuilt record contains exactly this jobs collection,
                # and the same record binder is the actual writer argument.
                compatible_records = []
                for call in r.calls_to(role, "index_writer"):
                    call_node = r.call_nodes[call["id"]]
                    actuals = _children(_field(call_node, "arguments"))
                    index_record = r.initializer(role, actuals[1]) if len(actuals) > 1 else None
                    if index_record is None or index_record.type != "object":
                        continue
                    for member in _children(index_record):
                        key = r.key(document, _field(member, "key")) if member.type == "pair" else r.key(document, member)
                        value = _field(member, "value") if member.type == "pair" else member
                        source = r.path(document, value)
                        if key == "jobs" and source and source["binding_id"] == collection["binding_id"]:
                            compatible_records.append(call["id"])
                if compatible_records:
                    replay.append(r.fact("record_event_replay_to_rebuilt_index_source", document, node,
                        event_read_source=r.expression(document, input_initializer),
                        materializer_call_source=r.expression(document, initializer),
                        assigned_collection_source=collection, writer_call_fact_ids=compatible_records,
                        branch_context=r.context(document, node, function)["branch_context"],
                        source_record_path_connected=True, full_replay_correctness_or_durability_proven=False))
    if "append" in r.roles:
        document, _, function = r.roles["append"]
        for call in r.calls_to("append", "durable_append"):
            node = r.call_nodes[call["id"]]
            args = _children(_field(node, "arguments"))
            initializer = r.initializer("append", args[1]) if len(args) > 1 else None
            if not r.is_target_call("append", initializer, "serializer"):
                continue
            serialization.append(r.fact("record_serialized_event_to_durable_append_source", document, node,
                writer_call_fact_id=call["id"], serializer_call_source=r.expression(document, initializer),
                serialized_argument=r.expression(document, args[1]),
                writer_path_source=r.expression(document, args[0]), **r.context(document, node, function),
                serialized_bytes_or_successful_durable_write_proven=False))
    return {"projection_state_publications": publication, "replay_index_publications": replay,
        "serialized_event_appends": serialization}


def _projection(r: _Records, result: dict) -> dict:
    required = {"mutation", "append", "durable_append", "projection", "locked_projection", "update", "index_writer",
        "refresh", "retry", "rebuild", "rebuild_entry", "list", "divergence", "classification", "doctor", "materializer", "serializer", "event_reader"}
    missing = sorted(required - r.roles.keys())
    orders = r.normal_orders("mutation", "append", "refresh")
    append_durable = r.calls_to("append", "durable_append")
    refresh_update = r.calls_to("refresh", "update")
    rebuild_writes = r.calls_to("rebuild", "index_writer")
    update_writes = r.calls_to("update", "index_writer")
    callbacks = [item for item in result["literal_callback_transfers"]
        if item["from_role"] == "update" and item["provider_role"] == "locked_projection"]
    projection_returns = [record for record in r.records.get("projection", []) if _explicit(record, "state")]
    field_joins = _projection_fields(r)
    # These are source data dependencies, not assertions that IO committed.
    witnesses = {"event_append_precedes_index_refresh_on_normal_reaching": bool(orders),
        "append_calls_selected_durable_writer": bool(append_durable),
        "index_refresh_calls_selected_updater": bool(refresh_update),
        "index_update_calls_selected_index_writer": bool(update_writes),
        "index_rebuild_calls_same_index_writer": bool(rebuild_writes),
        "locked_projection_supplies_literal_update_callback": bool(callbacks),
        "projection_returns_explicit_state_field": bool(projection_returns),
        "event_serializer_result_is_actual_durable_writer_argument": bool(field_joins["serialized_event_appends"]),
        "projection_callback_state_is_written_to_same_index_record": bool(field_joins["projection_state_publications"]),
        "read_events_materialized_state_flows_to_rebuilt_index_writer": bool(field_joins["replay_index_publications"]),
        "retry_has_captured_catch": any(record["callee_source"].endswith("write") for record in r.calls.get("retry", []))
            and any(item["branch_context"] and any(branch["kind"] == "catch_clause" for branch in item["branch_context"])
                for item in r.returns.get("retry", []))}
    if missing:
        r.a.gap("record_projection_roles_missing", roles=missing)
    for key, supported in witnesses.items():
        if not supported:
            r.a.gap("record_projection_relation_not_closed", relation=key)
    result.update({"normal_append_then_refresh_orders": orders, "field_joins": field_joins, "relation_witnesses": witnesses,
        "record_boundary": {"event_append_and_index_publication_are_separate_source_calls": bool(orders),
            "single_event_and_index_transaction_proven": False, "event_durability_or_index_write_success_proven": False,
            "all_crash_recovery_interleavings_proven": False, "index_divergence_implies_event_loss": False},
        "scoped_source_supported": not missing and all(witnesses.values()) and not r.incomplete})
    return result


def _command(r: _Records, result: dict) -> dict:
    required = {"loader", "policy_parser", "spec_parser", "resolver", "executor", "command_runner", "runner"}
    missing = sorted(required - r.roles.keys())
    edges = {(item["from_role"], item["to_role"]) for item in result["role_transfers"]}
    expected = {("loader", "policy_parser"), ("policy_parser", "spec_parser"),
        ("runner", "loader"), ("runner", "resolver"), ("runner", "command_runner"), ("command_runner", "executor")}
    # map(trustedProbeSpec) is a function-value source seam, not a CALLS edge.
    callback_sources = []
    if "policy_parser" in r.roles and "spec_parser" in r.roles:
        document = r.roles["policy_parser"][0]
        definition = r.roles["spec_parser"][1]
        for call in r.calls["policy_parser"]:
            node = r.call_nodes[call["id"]]
            for argument in _children(_field(node, "arguments")):
                if argument.type == "identifier":
                    identity = r.identity(document, argument)
                    declaration = identity.get("declaration_location") or {}
                    if (identity.get("state") == "unique" and declaration.get("start_byte") == definition.node.start_byte
                            and document.source.path == r.roles["spec_parser"][0].source.path):
                        callback_sources.append(r.fact("record_parser_callback_source_seam", document, argument,
                            call_fact_id=call["id"], source_role="spec_parser", callback_binding=identity,
                            callback_activation_or_array_map_result_proven=False, synthesized_call_edge=False))
    source_specs = [record for record in r.records.get("spec_parser", [])
        if all(_explicit(record, key) for key in ("predicateId", "executable", "args"))]
    dependencies = [item for item in result["local_initializer_dependencies"] if item["role"] in {"runner", "executor", "loader"}]
    command_joins, loader_joins, executor_joins = [], [], []
    if "runner" in r.roles:
        document, _, function = r.roles["runner"]
        for call in r.calls_to("runner", "command_runner"):
            node = r.call_nodes[call["id"]]
            arguments = _children(_field(node, "arguments"))
            initializer = r.initializer("runner", arguments[0]) if arguments else None
            if not r.is_target_call("runner", initializer, "resolver"):
                continue
            actuals = _children(_field(initializer, "arguments"))
            policy_initializer = r.initializer("runner", actuals[1]) if len(actuals) > 1 else None
            if r.is_target_call("runner", policy_initializer, "loader"):
                command_joins.append(r.fact("record_loaded_policy_lookup_to_command_argument_source", document, node,
                    command_call_fact_id=call["id"], resolver_source=r.expression(document, initializer),
                    policy_loader_source=r.expression(document, policy_initializer),
                    command_actual_source=r.expression(document, arguments[0]),
                    field_values_or_opaque_heap_mutation_excluded=False))
    if "loader" in r.roles:
        document = r.roles["loader"][0]
        for call in r.calls_to("loader", "policy_parser"):
            node = r.call_nodes[call["id"]]
            arguments = _children(_field(node, "arguments"))
            initializer = r.initializer("loader", arguments[0]) if arguments else None
            if initializer is None or initializer.type != "call_expression":
                continue
            callee = _field(initializer, "function")
            if document.text(callee) != "JSON.parse":
                continue
            decoded = _children(_field(initializer, "arguments"))
            raw_path = r.path(document, decoded[0]) if decoded else None
            if not raw_path or raw_path["members"] != ["stdout"]:
                continue
            raw_declaration = r.binding_nodes.get(("loader", raw_path["binding_id"]))
            command = _operand(_field(raw_declaration, "value"))
            if command is None or command.type != "call_expression" or not r.a.execfile_alias(document, _field(command, "function")).get("supported"):
                continue
            loader_joins.append(r.fact("record_execfile_stdout_json_to_policy_parser_source", document, node,
                parser_call_fact_id=call["id"], json_decode_source=r.expression(document, initializer),
                raw_execfile_source=r.expression(document, command),
                conditions=["registered ordinary Node execFile/promisify and JSON.parse source models"],
                external_git_response_or_policy_authenticity_verified=False))
    if "executor" in r.roles:
        document, _, function = r.roles["executor"]
        formals = _children(_field(function, "parameters"))
        binder = _field(formals[0], "pattern") or _field(formals[0], "name") if formals else None
        formal = r.identity(document, binder)
        for call in r.calls["executor"]:
            node = r.call_nodes[call["id"]]
            args = _children(_field(node, "arguments"))
            if len(args) < 3 or not r.a.execfile_alias(document, _field(node, "function")).get("supported"):
                continue
            executable, argv = r.path(document, args[0]), r.path(document, args[1])
            shell_false = args[2].type == "object" and any(r.key(document, _field(member, "key")) == "shell"
                and _field(member, "value") is not None and _field(member, "value").type == "false" for member in _children(args[2]) if member.type == "pair")
            if (executable and argv and executable["binding_id"] == argv["binding_id"] == formal.get("declaration_id")
                    and executable["members"] == ["executable"] and argv["members"] == ["args"] and shell_false):
                executor_joins.append(r.fact("record_selected_command_fields_to_structured_exec_source", document, node,
                    call_fact_id=call["id"], formal_source=formal, executable_source=executable,
                    argv_source=argv, shell_false_literal_source=True,
                    command_value_stability_or_execution_verified=False))
    witnesses = {"all_selected_direct_role_call_transfers": (expected - {("policy_parser", "spec_parser")}).issubset(edges),
        "policy_parser_references_spec_parser_callback": ("policy_parser", "spec_parser") in edges or bool(callback_sources),
        "parsed_policy_spec_has_explicit_command_fields": bool(source_specs),
        "selected_call_arguments_have_local_initializer_dependencies": bool(dependencies),
        "execfile_stdout_json_decode_is_actual_policy_parser_input": bool(loader_joins),
        "loaded_policy_lookup_result_is_actual_command_runner_input": bool(command_joins),
        "executor_reads_executable_and_args_from_same_command_formal": bool(executor_joins)}
    for key, supported in witnesses.items():
        if not supported:
            r.a.gap("record_command_relation_not_closed", relation=key)
    if missing:
        r.a.gap("record_command_roles_missing", roles=missing)
    result.update({"parser_callback_sources": callback_sources, "relation_witnesses": witnesses,
        "loader_codec_joins": loader_joins, "lookup_command_joins": command_joins,
        "executor_field_joins": executor_joins,
        "trusted_policy_spec_record_ids": [record["id"] for record in source_specs],
        "command_boundary": {"command_argument_origin_is_source_record_dependency": True,
            "expected_evidence_never_influences_any_branch_proven": False,
            "expected_evidence_as_executable_source_proven": False,
            "command_executed": False, "trusted_head_authenticity_runtime_verified": False,
            "opaque_effects_or_mutated_heap_excluded": False},
        "scoped_source_supported": not missing and all(witnesses.values()) and not r.incomplete})
    return result


def _retention(r: _Records, result: dict) -> dict:
    required = {"runner", "plan", "ledger", "verification", "artifact_writer"}
    missing = sorted(required - r.roles.keys())
    emitted = [record for record in r.records.get("runner", []) if _explicit(record, "emitFailedClaim", "true")]
    plan_true = [record for record in r.records.get("plan", []) if _explicit(record, "emitFailedClaim", "true")]
    propagated = [assignment for assignment in r.assignments.get("plan", [])
        if (assignment["left"].get("reference_path") or {}).get("members") == ["emitFailedClaim"] and assignment["right"]["source"] == "true"]
    ledger_guards = [guard for guard in r.guards.get("ledger", []) if "emitFailedClaim" in guard["condition"]["source"]]
    # A bounded boolean shape establishes marker=true disables this one skip.
    guard_truths = []
    if "ledger" in r.roles:
        document, _, function = r.roles["ledger"]
        for node in r.a.nodes(document, _field(function, "body")):
            if node.type != "if_statement":
                continue
            condition = _operand(_field(node, "condition"))
            if condition is None or condition.type != "binary_expression" or document.text(_field(condition, "operator")) != "&&":
                continue
            right = _operand(_field(condition, "right"))
            if right is None or right.type != "unary_expression" or document.text(_field(right, "operator")) != "!":
                continue
            argument = _operand(_field(right, "argument") or next(iter(_children(right)), None))
            path = r.path(document, argument)
            consequence = _field(node, "consequence")
            if not path or path["members"] != ["emitFailedClaim"] or consequence is None or consequence.type != "continue_statement":
                continue
            guard_truths.append(r.fact("record_true_marker_excludes_selected_skip", document, node,
                marker_reference=path, guard_source=document.text(condition),
                finite_source_cases=[{"marker": True, "other_conjunct": False, "skip_guard": False},
                    {"marker": True, "other_conjunct": True, "skip_guard": False}],
                model_id=MODEL, conditions=["ordinary boolean property reads; this guard is reached with this marker true"],
                all_other_filters_or_prior_exceptions_excluded=False))
    writes = r.calls_to("verification", "artifact_writer")
    content_records = []
    content_joins = []
    for record in r.records.get("verification", []):
        if _explicit(record, "kind", '"evidence-ledger"') and _explicit(record, "content"):
            content_records.append(record)
    if "verification" in r.roles:
        document, _, function = r.roles["verification"]
        for call in writes:
            node = r.call_nodes[call["id"]]
            arguments = _children(_field(node, "arguments"))
            if len(arguments) < 2 or arguments[1].type != "object":
                continue
            payload = arguments[1]
            kind = next((_field(member, "value") for member in _children(payload) if member.type == "pair" and r.key(document, _field(member, "key")) == "kind"), None)
            content = next((_operand(_field(member, "value")) for member in _children(payload) if member.type == "pair" and r.key(document, _field(member, "key")) == "content"), None)
            if kind is None or _literal_string(document.text(kind)) != "evidence-ledger" or content is None or content.type != "call_expression":
                continue
            if document.text(_field(content, "function")) != "JSON.stringify":
                continue
            encoded = _children(_field(content, "arguments"))
            ledger = r.initializer("verification", encoded[0]) if encoded else None
            if r.is_target_call("verification", ledger, "ledger"):
                content_joins.append(r.fact("record_ledger_result_json_to_artifact_content_source", document, node,
                    writer_call_fact_id=call["id"], ledger_call_source=r.expression(document, ledger),
                    content_codec_source=r.expression(document, content),
                    conditions=["the selected branch and write call are reached normally with ordinary JSON serialization"],
                    artifact_commit_or_physical_bytes_verified=False))
    runner_returns = r.collection_returns("runner")
    ledger_returns = r.collection_returns("ledger")
    emitted_ids = {record["id"] for record in emitted}
    emitted_returns = [item for item in runner_returns if item["record_fact_id"] in emitted_ids]
    precedence_sources = []
    if "plan" in r.roles:
        document, _, function = r.roles["plan"]
        for node in r.a.nodes(document, _field(function, "body")):
            if node.type != "if_statement":
                continue
            condition = _operand(_field(node, "condition"))
            consequence = _field(node, "consequence")
            if condition is None or condition.type != "call_expression" or consequence is None or consequence.type != "continue_statement":
                continue
            callee = _field(condition, "function")
            path = r.path(document, callee)
            if not path or path["members"] != ["has"]:
                continue
            receiver = _field(callee, "object")
            initializer = r.initializer("plan", receiver)
            if initializer is None or initializer.type != "new_expression" or document.text(_field(initializer, "constructor")) != "Set":
                continue
            add_calls = [call for call in r.calls["plan"] if (call["callee"].get("reference_path") or {}).get("binding_id") == path["binding_id"]
                and (call["callee"].get("reference_path") or {}).get("members") == ["add"] and call["location"]["start_byte"] > node.end_byte]
            if add_calls:
                precedence_sources.append(r.fact("record_seen_explicit_key_skips_later_input_source", document, node,
                    membership_source=r.expression(document, condition), seen_collection=path,
                    following_add_call_fact_ids=[call["id"] for call in add_calls],
                    conditions=["ordinary Set membership and the captured iteration body are reached"],
                    later_matching_input_skipped_on_this_guard=True, all_input_record_preservation_proven=False))
    witnesses = {"runner_emits_explicit_true_failure_record": bool(emitted),
        "plan_initializes_and_propagates_true_marker": bool(plan_true and propagated),
        "failure_records_append_to_returned_runner_collection": bool(emitted_returns),
        "true_marker_excludes_selected_invalid_record_skip": bool(guard_truths),
        "ledger_claims_append_to_returned_evidence_collection": bool(ledger_returns),
        "verification_calls_runner_plan_ledger": all(r.calls_to("verification", role) for role in ("runner", "plan", "ledger")),
        "verification_passes_actual_ledger_result_json_to_artifact_writer": bool(content_joins)}
    for key, supported in witnesses.items():
        if not supported:
            r.a.gap("record_retention_relation_not_closed", relation=key)
    if missing:
        r.a.gap("record_retention_roles_missing", roles=missing)
    result.update({"true_failure_record_ids": [record["id"] for record in emitted],
        "plan_true_record_ids": [record["id"] for record in plan_true],
        "true_marker_assignment_ids": [record["id"] for record in propagated],
        "ledger_marker_guard_ids": [record["id"] for record in ledger_guards],
        "true_marker_guard_cases": guard_truths, "ledger_artifact_content_record_ids": [record["id"] for record in content_records],
        "runner_collection_return_joins": emitted_returns, "ledger_collection_return_joins": ledger_returns,
        "ledger_artifact_content_joins": content_joins,
        "explicit_key_precedence_counter_sources": precedence_sources,
        "relation_witnesses": witnesses,
        "retention_boundary": {"selected_marker_excludes_invalid_record_skip": bool(guard_truths),
            "all_inputs_have_valid_checklist_identity": False,
            "explicit_hard_gate_observation_override_excluded": False,
            "spread_fields_cannot_override_prior_entry_fields": False,
            "all_input_retention_or_artifact_durability_proven": False,
            "probe_executed": False},
        "scoped_source_supported": not missing and all(witnesses.values()) and not r.incomplete})
    return result


def analyze_pattern(analysis: Any, kind: str | None = None) -> dict:
    """Return a finite pattern using the report engine's loaded source roles.

    Role requirements are fixed by the registered implementation, not by a
    configuration carrying desired outcomes.  Fields, calls and guards are
    always computed from saved source.  Limits remain alongside supported
    source relations, rather than being removed to manufacture completion.
    """
    selected = kind or analysis.rule.get("type")
    if selected not in KINDS:
        analysis.gap("record_relations_unknown_pattern", pattern=selected)
        return {"scoped_source_supported": False, "version": VERSION}
    reader = _Records(analysis)
    result = reader.summarize()
    if selected == "event_index_projection":
        result = _projection(reader, result)
    elif selected == "trusted_command_lineage":
        result = _command(reader, result)
    else:
        result = _retention(reader, result)
    limitations = {
        "event_index_projection": ("record_projection_physical_commit_and_all_recovery_not_proven",
            ["captured references do not prove IO success or one event/index transaction",
             "rebuild and doctor branches are source paths, not a completed recovery or crash-interleaving proof"]),
        "trusted_command_lineage": ("record_command_source_dependencies_do_not_prove_full_heap_noninterference",
            ["same lexical declarations connect selected initializers and call arguments; arbitrary heap effects remain unmodeled",
             "expectedEvidence can still affect separate oracle path/provenance branches; no all-branch noninterference claim"]),
        "unsupported_record_retention": ("record_true_marker_does_not_prove_all_input_or_artifact_retention",
            ["missing identities/checklist matches, explicit-key precedence, aborts and exceptions remain separate guards",
             "observation spreads may override earlier fields; artifact write/commit effects are not proved"]),
    }
    code, boundaries = limitations[selected]
    analysis.gap(code, source_only=True, necessary_to_scoped_source_relations=False, boundaries=boundaries)
    result["unproved_relations"] = boundaries
    result.update({"version": VERSION, "model_id": MODEL,
        "source_relations_only": True, "runtime_functionality_verified": False,
        "all_selected_roles_bound": len(analysis.roles) == len(analysis.rule["sources"]),
        "target_executed": False, "target_tests_run": False, "target_build_run": False})
    return result
