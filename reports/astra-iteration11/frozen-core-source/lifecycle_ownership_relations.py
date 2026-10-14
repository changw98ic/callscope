"""Finite browser continuation guards and captured resource-writing roles.

Inputs are authenticated saved CST declarations supplied by report-chain
analysis. Selectors never supply guards, writers, expected state or outcomes.
These relations concern captured lexical tokens and conditional source order;
they do not prove browser activation, resource uniqueness or authorization.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Any

from .semantic_sources import unwrap
from .static_contracts import _literal_string

VERSION = "captured-lifecycle-ownership-relations-1"
LIFECYCLE_MODEL = "browser-continuation-guard-source-v1"
OWNERSHIP_MODEL = "captured-resource-writer-source-v1"
TYPES = frozenset({"browser_async_lifecycle", "resource_writer_ownership"})
_FUNCTIONS = frozenset({"function_declaration", "generator_function_declaration", "function_expression",
    "generator_function", "arrow_function", "method_definition", "function_item", "closure_expression"})
_WRITES = frozenset({"assignment_expression", "augmented_assignment_expression", "update_expression"})
_BLOCKS = frozenset({"statement_block", "block"})
_STANDARD_CONTROLLER = "AbortController"


def _field(node: Any, key: str) -> Any:
    return node.child_by_field_name(key) if node is not None else None


def _children(node: Any) -> list[Any]:
    return [child for child in node.named_children if child.type not in {"comment", "type_annotation",
        "type_arguments", "type_parameters"} and not child.type.endswith("_type")] if node is not None else []


def _inside(outer: Any, inner: Any) -> bool:
    return bool(outer is not None and inner is not None and outer.start_byte <= inner.start_byte
        and inner.end_byte <= outer.end_byte)


def _owner(node: Any) -> Any:
    while node is not None and node.type not in _FUNCTIONS:
        node = node.parent
    return node


def _operand(node: Any) -> Any:
    node = unwrap(node)
    while node is not None and node.type in {"await_expression", "reference_expression", "try_expression"}:
        node = unwrap(_field(node, "value") or _field(node, "argument") or next(iter(_children(node)), None))
    return node


class _Relations:
    def __init__(self, analysis: Any):
        self.a = analysis
        self.identities: dict[tuple[str, int], dict | None] = {}
        self.counters: dict[tuple, list[dict]] = defaultdict(list)
        self.disposals: dict[tuple, list[dict]] = defaultdict(list)
        self.closed_writes: dict[tuple, list[dict]] = defaultdict(list)
        self.continuations: list[dict] = []

    def identity(self, document: Any, node: Any) -> dict | None:
        node = unwrap(node)
        if node is None or node.type not in {"identifier", "shorthand_property_identifier",
                "shorthand_property_identifier_pattern", "self"}:
            return None
        key = (document.source.path, node.id)
        if key not in self.identities:
            result = (self.a.identity(document, node) if document.kind == "rust"
                else self.a.lexical(document).resolve_identity(node))
            if document.kind == "rust" and result.get("state") == "captured_unique_rust_binder":
                result = {**result, "name": document.text(node), "identity_complete": False,
                    "macro_namespace_complete": False}
                self.identities[key] = result
            else:
                self.identities[key] = result if result.get("state") == "unique" and result.get("identity_complete") else None
        return self.identities[key]

    def path(self, document: Any, node: Any) -> dict | None:
        node = unwrap(node)
        if node is None:
            return None
        identity = self.identity(document, node)
        if identity:
            return {"root_declaration_id": identity["declaration_id"], "root_name": identity["name"],
                "members": [], "root_declaration_location": identity.get("declaration_location"),
                "root_identity": identity, "runtime_resource_identity_proven": False}
        if node.type == "this":
            enclosing = node.parent
            while enclosing is not None and enclosing.type not in {"class_declaration", "class"}:
                enclosing = enclosing.parent
            if enclosing is not None:
                return {"root_declaration_id": "source-this:" + document.source.path + ":" + str(enclosing.start_byte),
                    "root_name": "this", "members": [], "root_declaration_location": document.location(enclosing),
                    "root_identity": None, "runtime_resource_identity_proven": False}
        if node.type in {"member_expression", "subscript_expression", "field_expression"}:
            root = _field(node, "object") or _field(node, "value")
            prop = _field(node, "property") or _field(node, "field") or _field(node, "index")
            parent = self.path(document, root)
            key = document.text(prop) if prop is not None and prop.type in {"property_identifier", "field_identifier",
                "identifier"} and node.type != "subscript_expression" else _literal_string(document.text(prop)) if prop is not None else None
            if parent and key is not None:
                return {**parent, "members": [*parent["members"], key]}
            if parent and prop is not None and node.type == "subscript_expression":
                location = document.location(prop)
                # Keep an opaque captured index site, never its inferred key.
                # Equal text at another site does not establish equal values.
                return {**parent, "members": [*parent["members"], "[captured-index:" + location["span_hash"] + ":" +
                    str(prop.start_byte) + "]"], "computed_member_sites": [*parent.get("computed_member_sites", []), location],
                    "computed_indices_value_equality_proven": False}
        return None

    @staticmethod
    def key(path: dict | None) -> tuple | None:
        return (path["root_declaration_id"], tuple(path["members"])) if path else None

    def operator(self, document: Any, node: Any) -> str:
        operator = _field(node, "operator")
        return document.text(operator) if operator is not None else next((child.type for child in node.children
            if not child.is_named and child.type in {"++", "--", "+=", "-=", "=", "!==", "!=", "===", "==", "||", "&&"}), "")

    def nodes(self, document: Any, function: Any) -> list[Any]:
        return self.a.nodes(document, _field(function, "body"))

    def fact(self, kind: str, document: Any, node: Any, **details: Any) -> dict:
        owner = _owner(node)
        definition = document.definition_for_ast(owner) if owner is not None else None
        return self.a.fact(kind, document, node, relation_component=VERSION,
            lexical_source_owner={"graph_node_id": definition.graph_node_id if definition else None,
                "symbol": definition.symbol if definition else None,
                "location": document.location(owner) if owner is not None else None}, **details)

    def mutation(self, document: Any, node: Any) -> tuple[Any, Any]:
        left = _field(node, "left") or _field(node, "argument")
        if left is None and node.type == "update_expression":
            left = next(iter(_children(node)), None)
        return left, _field(node, "right")

    def precedes(self, before: Any, after: Any, function: Any) -> bool:
        """Same callable, earlier direct sibling of an ancestor block only."""
        if _owner(before) != function or _owner(after) != function:
            return False
        current = after
        while current is not None and current != function:
            block = current.parent
            if block is not None and block.type in _BLOCKS:
                for statement in _children(block):
                    if statement == current:
                        break
                    if _inside(statement, before):
                        # No guard buried in a sibling branch becomes a dominator.
                        branch = before
                        while branch.parent is not None and branch.parent != block:
                            if branch.parent.type not in {"expression_statement", "lexical_declaration",
                                    "variable_declaration", "variable_declarator", "await_expression"}:
                                return False
                            branch = branch.parent
                        return True
            current = block
        return False

    def abrupt(self, node: Any) -> Any:
        if node is not None and node.type in {"return_statement", "throw_statement", "return_expression"}:
            return node
        children = _children(node)
        if node is not None and node.type in _BLOCKS and children and children[-1].type in {
                "return_statement", "throw_statement", "return_expression"} and all(child.type in {
                    "expression_statement", "lexical_declaration", "variable_declaration"} for child in children[:-1]):
            return children[-1]
        return None

    def disjuncts(self, document: Any, node: Any) -> list[Any]:
        node = unwrap(node)
        if node is not None and node.type == "binary_expression" and self.operator(document, node) == "||":
            return [*self.disjuncts(document, _field(node, "left")), *self.disjuncts(document, _field(node, "right"))]
        return [node] if node is not None else []

    def parameter_ids(self, document: Any, function: Any) -> set[str]:
        values = set()
        ancestor = function
        while ancestor is not None:
            if ancestor.type in _FUNCTIONS:
                params = _field(ancestor, "parameters") or _field(ancestor, "parameter")
                for node in self.a.nodes(document, params):
                    identity = self.identity(document, node)
                    if identity and identity.get("declaration_kind") == "parameter":
                        values.add(identity["declaration_id"])
            ancestor = ancestor.parent
        return values

    def controllers(self, document: Any, function: Any) -> list[dict]:
        result = []
        nodes = self.nodes(document, function)
        for declaration in nodes:
            if declaration.type != "variable_declarator":
                continue
            value = unwrap(_field(declaration, "value"))
            callee = _field(value, "constructor") if value is not None and value.type == "new_expression" else None
            name = _field(declaration, "name")
            identity = self.identity(document, name)
            if callee is None or callee.type != "identifier" or document.text(callee) != _STANDARD_CONTROLLER or not identity:
                continue
            controller_binding = self.a.lexical(document).resolve_identity(callee)
            # A locally declared lookalike cannot inherit the standard API model.
            if controller_binding.get("state") == "unique" or "unresolved_lexical_binding" not in controller_binding.get("gaps", []):
                continue
            installed = []
            token = self.path(document, name)
            for mutation in nodes:
                if mutation.type != "assignment_expression":
                    continue
                left, right = self.mutation(document, mutation)
                destination = self.path(document, left)
                if self.key(self.path(document, right)) == self.key(token) and destination:
                    installed.append(self.fact("lifecycle_controller_installed_in_captured_slot", document, mutation,
                        controller_token=token, shared_slot=destination,
                        disposal_source_fact_ids=[item["id"] for item in self.disposals.get(self.key(destination), [])],
                        source_model=LIFECYCLE_MODEL, runtime_controller_or_abort_effect_proven=False))
            result.append(self.fact("lifecycle_standard_controller_source_construction", document, declaration,
                controller_token=token, installed_source_fact_ids=[item["id"] for item in installed],
                standard_global_binding_assumption=_STANDARD_CONTROLLER,
                source_model=LIFECYCLE_MODEL, standard_global_runtime_identity_proven=False))
        return result

    def invalidations(self) -> list[dict]:
        values = []
        seen = set()
        for role, (document, _, selected) in self.a.roles.items():
            for node in self.a.nodes(document, _field(selected, "body"), nested=True):
                marker = (document.source.path, node.id)
                if marker in seen:
                    continue
                seen.add(marker)
                if node.type in _WRITES:
                    left, right = self.mutation(document, node)
                    token = self.path(document, left)
                    operator = self.operator(document, node)
                    increment = operator == "++" or operator == "+=" and right is not None and document.text(right) == "1"
                    if token and increment:
                        fact = self.fact("lifecycle_counter_increment_source", document, node,
                            selected_role=role, counter_token=token, operator=operator,
                            source_model=LIFECYCLE_MODEL, runtime_generation_increment_proven=False)
                        self.counters[self.key(token)].append(fact)
                        values.append(fact)
                    if token and right is not None and right.type == "true":
                        fact = self.fact("lifecycle_truthy_invalidation_source", document, node,
                            selected_role=role, invalidation_token=token, assigned_literal=True,
                            source_model=LIFECYCLE_MODEL, runtime_closed_state_proven=False)
                        self.closed_writes[self.key(token)].append(fact)
                        values.append(fact)
                elif node.type == "call_expression":
                    callee = unwrap(_field(node, "function"))
                    receiver = self.path(document, _field(callee, "object"))
                    member = _field(callee, "property")
                    method = document.text(member) if member is not None else None
                    if receiver and method in {"abort", "close", "dispose"}:
                        fact = self.fact("lifecycle_disposal_source_call", document, node, selected_role=role,
                            receiver_token=receiver, disposal_member=method,
                            source_model=LIFECYCLE_MODEL, call_activation_or_resource_release_proven=False)
                        self.disposals[self.key(receiver)].append(fact)
                        values.append(fact)
        return values

    def guards(self, document: Any, function: Any) -> list[tuple[Any, dict]]:
        params = self.parameter_ids(document, function)
        values = []
        for node in self.nodes(document, function):
            if node.type != "if_statement":
                continue
            abrupt = self.abrupt(_field(node, "consequence"))
            if abrupt is None:
                continue
            blockers = []
            for term in self.disjuncts(document, _field(node, "condition")):
                path = self.path(document, term)
                if path and self.key(path) in self.closed_writes:
                    blockers.append({"kind": "captured_truthy_invalidation_token", "token": path,
                        "invalidation_source_fact_ids": [fact["id"] for fact in self.closed_writes[self.key(path)]],
                        "location": document.location(term)})
                if path and path["members"][-2:] == ["signal", "aborted"]:
                    blockers.append({"kind": "captured_abort_signal_truthy", "token": path,
                        "location": document.location(term), "standard_signal_runtime_identity_proven": False})
                if term.type == "binary_expression" and self.operator(document, term) in {"!==", "!="}:
                    left, right = self.path(document, _field(term, "left")), self.path(document, _field(term, "right"))
                    for own, current in ((left, right), (right, left)):
                        if own and current and own["root_declaration_id"] in params and self.key(current) in self.counters:
                            blockers.append({"kind": "captured_generation_token_inequality", "captured_parameter_token": own,
                                "current_counter_token": current, "operator": self.operator(document, term),
                                "invalidation_source_fact_ids": [fact["id"] for fact in self.counters[self.key(current)]],
                                "location": document.location(term)})
            if blockers:
                fact = self.fact("lifecycle_conditional_abrupt_guard", document, node,
                    blocker_terms=blockers, abrupt_location=document.location(abrupt),
                    condition_source=document.text(_field(node, "condition")),
                    source_model=LIFECYCLE_MODEL, condition_runtime_truth_proven=False,
                    normal_continuation_requires_each_recorded_disjunct_false=True)
                values.append((node, fact))
        return values

    def tracked_target(self, document: Any, node: Any, function: Any) -> dict | None:
        if node.type in _WRITES:
            left, right = self.mutation(document, node)
            path = self.path(document, left)
            if path is None:
                return None
            declaration = path.get("root_declaration_location")
            # Local variable assignment is not a shared-result publication.
            if (not path["members"] and declaration and function.start_byte <= declaration["start_byte"]
                    and declaration["end_byte"] <= function.end_byte):
                return None
            return {"kind": "captured_assignment_target", "target_token": path,
                "assigned_value_source": document.text(right) if right is not None else None,
                "runtime_write_proven": False}
        if node.type != "call_expression":
            return None
        callee = unwrap(_field(node, "function"))
        if callee is not None and callee.type == "member_expression":
            receiver = self.path(document, _field(callee, "object"))
            member = _field(callee, "property")
            if receiver and member is not None and document.text(member) in {
                    "replaceChildren", "append", "appendChild", "prepend", "replaceState", "pushState"}:
                return {"kind": "captured_browser_mutator_form", "target_token": receiver,
                    "member": document.text(member), "browser_api_runtime_identity_or_effect_proven": False}
        # Calls to captured functions are retained as effect-opaque source
        # frontiers, never interpreted as writes merely from a method name.
        definition = document.definition_for_ast(function)
        edge, problems = self.a.sources.call_binding(node, document, definition) if definition is not None else (None, [])
        raw = self.a.raw_edge(document, node)
        return {"kind": "captured_effect_opaque_call_frontier", "callee_source": document.text(callee),
            "captured_site_edge_id": raw.id if raw is not None else None,
            "authenticated_call_edge_id": edge.id if edge is not None else None,
            "actual_callee_graph_node_id": edge.target if edge is not None else None,
            "binding_gaps": problems, "physical_write_or_effect_proven": False}

    def nullable_context_relations(self) -> list[dict]:
        """Actual nullable record providers and call-result rejection guards."""
        providers = {}
        for role, (document, definition, function) in self.a.roles.items():
            returns = []
            for node in self.nodes(document, function):
                if node.type != "return_statement":
                    continue
                value = unwrap(_field(node, "value") or _field(node, "argument") or next(iter(_children(node)), None))
                if value is not None and value.type in {"null", "object"}:
                    returns.append((node, value))
            if {value.type for _, value in returns} != {"null", "object"}:
                continue
            record = self.fact("lifecycle_nullable_context_record_provider", document, function,
                selected_role=role, return_sources=[{"location": document.location(node),
                    "return_kind": value.type, "returned_source": self.a.expression(document, value),
                    "branch_context": self.a.branch_context(document, node, function)} for node, value in returns],
                authentication_authority_or_runtime_context_validity_proven=False,
                source_model=LIFECYCLE_MODEL)
            providers[definition.graph_node_id] = record
        result = []
        for role, (document, _, function) in self.a.roles.items():
            for call in self.a.calls_by_role.get(role, []):
                provider = providers.get(call.get("actual_callee_graph_node_id"))
                if provider is None or not call.get("authenticated_call_edge_id"):
                    continue
                node = self.a.call_nodes[call["id"]][2]
                binding = node.parent
                while binding is not None and binding.type not in {"variable_declarator", *_FUNCTIONS}:
                    binding = binding.parent
                if binding is None or binding.type != "variable_declarator" or _operand(_field(binding, "value")) != node:
                    continue
                token = self.path(document, _field(binding, "name"))
                if token is None:
                    continue
                for guard in self.nodes(document, function):
                    condition = unwrap(_field(guard, "condition")) if guard.type == "if_statement" else None
                    if condition is None or condition.type != "binary_expression" or self.operator(document, condition) not in {"===", "=="}:
                        continue
                    left, right = unwrap(_field(condition, "left")), unwrap(_field(condition, "right"))
                    reference = left if right is not None and right.type == "null" else right if left is not None and left.type == "null" else None
                    abrupt = self.abrupt(_field(guard, "consequence"))
                    if self.key(self.path(document, reference)) != self.key(token) or abrupt is None or not self.precedes(binding, guard, function):
                        continue
                    result.append(self.fact("lifecycle_nullable_context_consumer_rejection", document, guard,
                        selected_role=role, provider_source_fact_id=provider["id"],
                        authenticated_call_fact_id=call["id"], authenticated_call_edge_id=call["authenticated_call_edge_id"],
                        result_token=token, operator=self.operator(document, condition),
                        abrupt_location=document.location(abrupt), source_model=LIFECYCLE_MODEL,
                        runtime_scope_authorization_or_selected_scope_validity_proven=False))
        return result

    def generation_handoffs(self) -> list[dict]:
        """Copy of a captured counter, then actual selected-callee argument."""
        target_roles = {definition.graph_node_id: role for role, (_, definition, _) in self.a.roles.items()}
        results = []
        for role, (document, _, function) in self.a.roles.items():
            captures = []
            for node in self.nodes(document, function):
                if node.type != "variable_declarator":
                    continue
                name, value = _field(node, "name"), unwrap(_field(node, "value"))
                token, counter = self.path(document, name), self.path(document, value)
                increments = self.counters.get(self.key(counter), [])
                if token is None or counter is None or not increments:
                    continue
                reached = [item for item in increments if item["location"]["file"] == document.source.path
                    and item["lexical_source_owner"]["location"] == document.location(function)
                    and item["location"]["end_byte"] <= node.start_byte]
                if not reached:
                    continue
                record = self.fact("lifecycle_counter_token_capture_source", document, node,
                    selected_role=role, captured_token=token, counter_token=counter,
                    source_increment_fact_ids=[item["id"] for item in reached],
                    source_model=LIFECYCLE_MODEL, opaque_reentrancy_or_current_counter_value_proven=False)
                captures.append((node, token, record))
            for call in self.a.calls_by_role.get(role, []):
                target_role = target_roles.get(call.get("actual_callee_graph_node_id"))
                if target_role is None or not call.get("authenticated_call_edge_id"):
                    continue
                target_document, target_definition, target_function = self.a.roles[target_role]
                # This is a lexical argument relation, never a protocol or
                # same-name cross-language connection.
                if target_document is not document:
                    continue
                call_node = self.a.call_nodes[call["id"]][2]
                params = _field(target_function, "parameters") or _field(target_function, "parameter")
                identities = {}
                for param in self.a.nodes(target_document, params):
                    identity = self.identity(target_document, param)
                    if identity and identity.get("declaration_kind") == "parameter":
                        identities[identity["parameter_index"]] = identity
                for index, argument in enumerate(_children(_field(call_node, "arguments"))):
                    actual = self.path(document, argument)
                    formal = identities.get(index)
                    if actual is None or formal is None:
                        continue
                    for capture_node, capture_token, capture in captures:
                        if self.key(actual) != self.key(capture_token) or not self.precedes(capture_node, call_node, function):
                            continue
                        results.append(self.fact("lifecycle_generation_argument_to_selected_callable", document, call_node,
                            selected_role=role, target_role=target_role, target_symbol=target_definition.symbol,
                            captured_token_source_fact_id=capture["id"], argument_index=index,
                            target_parameter_declaration_id=formal["declaration_id"],
                            target_parameter_location=formal["binder_location"],
                            authenticated_call_fact_id=call["id"], authenticated_call_edge_id=call["authenticated_call_edge_id"],
                            source_model=LIFECYCLE_MODEL, runtime_callee_activation_or_generation_freshness_proven=False))
        return results

    def lifecycle(self) -> dict:
        invalidations = self.invalidations()
        context_relations = self.nullable_context_relations()
        generation_handoffs = self.generation_handoffs()
        role_results = []
        all_continuations = []
        seen = set()
        for role, (document, definition, function) in self.a.roles.items():
            functions = [function]
            for node in self.a.nodes(document, _field(function, "body"), nested=True):
                if node.type not in _FUNCTIONS or node.type in {"function_declaration", "generator_function_declaration"}:
                    continue
                parent = node.parent
                while parent is not None and parent != function and parent.type not in {
                        "function_declaration", "generator_function_declaration"}:
                    parent = parent.parent
                if parent == function:
                    functions.append(node)
            components = []
            for current in functions:
                marker = (document.source.path, current.id)
                if marker in seen:
                    continue
                seen.add(marker)
                nodes = self.nodes(document, current)
                awaits = [node for node in nodes if node.type == "await_expression"]
                guard_records = self.guards(document, current)
                if not awaits and not guard_records:
                    continue
                controllers = self.controllers(document, current)
                targets = []
                for node in nodes:
                    target = self.tracked_target(document, node, current)
                    if target is None:
                        continue
                    # Assignment writes and call effects happen after their
                    # operand/argument evaluation. An await inside that RHS
                    # invalidates an earlier guard just like a prior statement.
                    publication_point = node.end_byte
                    prior_awaits = [suspension for suspension in awaits if suspension.end_byte <= publication_point
                        and not _inside(suspension, node)]
                    if not prior_awaits and not guard_records:
                        continue
                    preceding = [(guard, fact) for guard, fact in guard_records if self.precedes(guard, node, current)]
                    current_guards = [(guard, fact) for guard, fact in preceding if not any(
                        guard.end_byte < suspension.start_byte < publication_point for suspension in prior_awaits)]
                    record = self.fact("lifecycle_continuation_publication_source", document, node,
                        selected_role=role, selected_role_owner=definition.symbol,
                        nested_callback=current != function, target=target,
                        prior_suspension_locations=[document.location(item) for item in prior_awaits],
                        source_phase="after_captured_suspension" if prior_awaits else
                            "guarded_synchronous_continuation" if current_guards else "initial_synchronous_setup",
                        normal_preceding_guard_fact_ids=[fact["id"] for _, fact in preceding],
                        guards_after_last_captured_suspension_fact_ids=[fact["id"] for _, fact in current_guards],
                        recorded_blocker_kinds=sorted({term["kind"] for _, fact in current_guards for term in fact["blocker_terms"]}),
                        conditional_stale_blockers_preserved=bool(current_guards),
                        lacking_local_guard_is_a_defect=False, inherited_parent_guard_promoted=False,
                        browser_activation_or_effect_proven=False, source_model=LIFECYCLE_MODEL)
                    targets.append(record)
                    all_continuations.append(record)
                components.append({"callable_location": document.location(current), "nested_callback": current != function,
                    "suspension_count": len(awaits), "guard_fact_ids": [fact["id"] for _, fact in guard_records],
                    "controller_fact_ids": [fact["id"] for fact in controllers],
                    "publication_fact_ids": [fact["id"] for fact in targets],
                    "callback_activation_proven": False})
            role_results.append({"role": role, "selected_symbol": definition.symbol, "callable_components": components})
        disposal_consumers = self.closed_result_consumers()
        protected = [item for item in all_continuations if item["conditional_stale_blockers_preserved"]]
        unguarded = [item for item in all_continuations if not item["conditional_stale_blockers_preserved"]]
        late_unguarded = [item for item in unguarded if item["source_phase"] == "after_captured_suspension"]
        return {"relation_component_version": VERSION, "lifecycle_sources": role_results,
            "invalidation_fact_ids": [item["id"] for item in invalidations],
            "continuation_publication_fact_ids": [item["id"] for item in all_continuations],
            "locally_guarded_publication_fact_ids": [item["id"] for item in protected],
            "without_local_guard_publication_fact_ids": [item["id"] for item in unguarded],
            "post_suspension_without_local_guard_fact_ids": [item["id"] for item in late_unguarded],
            "initial_synchronous_setup_fact_ids": [item["id"] for item in unguarded
                if item["source_phase"] == "initial_synchronous_setup"],
            "closed_result_disposal_consumers": disposal_consumers,
            "nullable_context_consumer_relations": context_relations,
            "generation_argument_relations": generation_handoffs,
            "scoped_source_supported": bool(protected and self.counters and self.disposals and generation_handoffs
                and context_relations) and not self.a.incomplete,
            "all_async_callbacks_guarded_proven": False, "all_stale_results_rejected_proven": False,
            "unique_browser_runtime_binding_proven": False, "all_resources_released_proven": False,
            "scope_conditions": ["selected captured callables and nested callbacks are invoked and their recorded branches are reached normally",
                "generation tokens compare captured lexical declarations, without asserting current counter values",
                "standard AbortController/DOM behavior is an explicit source model, not observed browser behavior",
                "a parent guard is never inherited across a nested callback or an intervening suspension"],
            "unreviewed_scope": ["complete browser event ordering and activation", "opaque imported mounts and subscriptions",
                "all DOM effects, underlying network cancellation, hidden aliases and arbitrary callback reentrancy"]}

    def closed_result_consumers(self) -> list[dict]:
        results, seen = [], set()
        for role, (document, _, function) in self.a.roles.items():
            for node in self.a.nodes(document, _field(function, "body"), nested=True):
                if node.type != "if_statement" or (document.source.path, node.id) in seen:
                    continue
                seen.add((document.source.path, node.id))
                condition = self.path(document, unwrap(_field(node, "condition")))
                branch = _field(node, "consequence")
                abrupt = self.abrupt(branch)
                if not condition or self.key(condition) not in self.closed_writes or abrupt is None:
                    continue
                for call in self.a.nodes(document, branch):
                    if call.type != "call_expression":
                        continue
                    callee = unwrap(_field(call, "function"))
                    receiver = self.path(document, _field(callee, "object"))
                    prop = _field(callee, "property")
                    if not receiver or prop is None or document.text(prop) not in {"close", "dispose"}:
                        continue
                    owner = _owner(call)
                    identity = receiver.get("root_identity") or {}
                    if identity.get("declaration_kind") != "parameter" or owner is None:
                        continue
                    results.append(self.fact("lifecycle_truthy_result_disposal_consumer", document, node,
                        selected_role=role, condition_token=condition, returned_result_parameter=receiver,
                        disposal_location=document.location(call), abrupt_location=document.location(abrupt),
                        close_before_normal_return=call.end_byte <= abrupt.start_byte,
                        promise_fulfillment_and_callback_activation_proven=False,
                        disposed_effects_reverted_proven=False, source_model=LIFECYCLE_MODEL))
        return results

    def ownership(self) -> dict:
        writers, references, frontiers, guards = [], [], [], []
        grouped: dict[tuple, list[dict]] = defaultdict(list)
        for role, (document, definition, function) in self.a.roles.items():
            nodes = self.nodes(document, function)
            for node in nodes:
                if node.type in {"variable_declarator", "let_declaration"}:
                    binder = _field(node, "name") or _field(node, "pattern")
                    value = _operand(_field(node, "value"))
                    path = self.path(document, binder)
                    if path and value is not None and value.type in {"object", "struct_expression"}:
                        record = self.fact("resource_captured_record_construction", document, node, selected_role=role,
                            selected_definition=definition.symbol, resource_token=path,
                            operation_source="captured_record_initializer", assigned_expression=self.a.expression(document, value),
                            branch_context=self.a.branch_context(document, node, function), source_model=OWNERSHIP_MODEL,
                            runtime_write_or_exclusive_ownership_proven=False, authorization_of_write_proven=False)
                        writers.append(record)
                        grouped[self.key(path)].append(record)
                elif node.type in _WRITES:
                    left, right = self.mutation(document, node)
                    path = self.path(document, left)
                    if not path:
                        continue
                    record = self.fact("resource_captured_writer", document, node, selected_role=role,
                        selected_definition=definition.symbol, resource_token=path,
                        operation_source=self.operator(document, node), assigned_expression=self.a.expression(document, right),
                        branch_context=self.a.branch_context(document, node, function),
                        source_model=OWNERSHIP_MODEL, runtime_write_or_exclusive_ownership_proven=False,
                        authorization_of_write_proven=False)
                    writers.append(record)
                    grouped[self.key(path)].append(record)
                elif node.type in {"identifier", "shorthand_property_identifier", "member_expression", "field_expression"}:
                    parent = node.parent
                    if parent is not None and parent.type in {"member_expression", "field_expression"}:
                        continue
                    path = self.path(document, node)
                    if path:
                        references.append((role, document, node, path, definition.symbol))
                elif node.type in {"if_statement", "if_expression"} and self.abrupt(_field(node, "consequence")) is not None:
                    guards.append(self.fact("resource_captured_rejection_guard", document, node, selected_role=role,
                        condition=self.a.expression(document, _field(node, "condition")),
                        authorization_or_domain_invariant_proven=False, source_model=OWNERSHIP_MODEL))
            for call in self.a.calls_by_role.get(role, []):
                if call.get("authenticated_call_edge_id") or call.get("arguments"):
                    call_node = self.a.call_nodes[call["id"]][2]
                    callee = unwrap(_field(call_node, "function"))
                    receiver = self.path(document, _field(callee, "object") or _field(callee, "value"))
                    frontiers.append({"source_call_fact_id": call["id"], "role": role,
                        "authenticated_callee_graph_node_id": call.get("actual_callee_graph_node_id"),
                        "authenticated_call_edge_id": call.get("authenticated_call_edge_id"),
                        "captured_callee_source": call["callee_source"],
                        "captured_receiver_token": receiver,
                        "arguments": call["arguments"], "activation_and_physical_effect_proven": False})
        consumers = []
        for role, document, node, path, symbol in references:
            matching = [writer for token, entries in grouped.items() if token[0] == path["root_declaration_id"]
                and (not token[1] or not path["members"] or tuple(path["members"][:len(token[1])]) == token[1]) for writer in entries]
            if matching:
                consumers.append(self.fact("resource_captured_same_token_reference", document, node,
                    selected_role=role, selected_definition=symbol, referenced_token=path,
                    captured_writer_fact_ids=[writer["id"] for writer in matching],
                    read_after_write_or_same_runtime_object_proven=False, source_model=OWNERSHIP_MODEL))
        groups = [{"captured_root_declaration_id": token[0], "captured_members": list(token[1]),
            "writer_fact_ids": [writer["id"] for writer in entries],
            "selected_writer_symbols": sorted({writer["selected_definition"] for writer in entries}),
            "unique_owner_or_authorization_proven": False} for token, entries in sorted(grouped.items())]
        return {"relation_component_version": VERSION, "captured_resource_writer_groups": groups,
            "writer_fact_ids": [writer["id"] for writer in writers],
            "same_token_reference_fact_ids": [item["id"] for item in consumers],
            "source_rejection_guard_fact_ids": [item["id"] for item in guards],
            "call_record_and_effect_frontiers": frontiers,
            "scoped_source_supported": bool(writers and frontiers) and not self.a.incomplete,
            "responsibility_interpretation": "Selected captured functions write the recorded lexical fields and pass the recorded arguments; directory names assign no responsibility.",
            "ownership_assessment": "partial_captured_writers_and_consumers",
            "unique_fact_owner_proven": False, "canonical_authority_proven": False,
            "all_mutations_authorized_proven": False, "all_storage_resources_bound_proven": False,
            "whole_repository_ownership_inferred": False,
            "unreviewed_scope": ["aliases, interprocedural heap identity and external persistence semantics",
                "all writers outside selected declarations", "authorization and canonical authority contracts",
                "architectural documentation consistency and all deployment branches"]}


def analyze_pattern(analysis: Any) -> dict:
    relations = _Relations(analysis)
    kind = analysis.rule.get("type")
    if kind == "browser_async_lifecycle":
        if LIFECYCLE_MODEL not in analysis.rule.get("models", []):
            analysis.gap("lifecycle_source_model_not_registered")
            return {"scoped_source_supported": False, "relation_component_version": VERSION}
        return relations.lifecycle()
    if kind == "resource_writer_ownership":
        if OWNERSHIP_MODEL not in analysis.rule.get("models", []):
            analysis.gap("resource_writer_source_model_not_registered")
            return {"scoped_source_supported": False, "relation_component_version": VERSION}
        return relations.ownership()
    analysis.gap("lifecycle_ownership_pattern_type_not_supported", requested_type=kind)
    return {"scoped_source_supported": False, "relation_component_version": VERSION}
