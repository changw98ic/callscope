"""Conditional execution, finalization, terminal publication and projection.

This adapter consumes the report-chain engine's authenticated source roles.
All intermediate fields, formulas, callback arguments and guards come from
saved syntax. Ordinary storage/provider ports remain explicit source seams;
there is no target execution, remote-success or exactly-once theorem.
"""
from __future__ import annotations

from itertools import product
from typing import Any

from .semantic_sources import unwrap
from .static_contracts import _literal_string

VERSION = "captured-conditional-delivery-source-1"
_ROLES = {"finalizer", "failure_result", "worker", "publication", "writer", "assignment_sync",
    "reconcile", "attempt_read", "queue_projection", "finalizer_contract", "git_readback", "journal", "recovery"}
_FUNCTIONS = {"function_declaration", "function_expression", "arrow_function", "method_definition"}
_ERASED = {"comment", "type_annotation", "type_arguments", "type_parameters", "interface_declaration",
    "type_alias_declaration", "type_query", "import_type", "function_type"}


def _field(node: Any, key: str) -> Any:
    return node.child_by_field_name(key) if node is not None else None


def _children(node: Any) -> list[Any]:
    return [child for child in node.named_children if child.type not in _ERASED and not child.type.endswith("_type")] if node is not None else []


def _inside(outer: Any, inner: Any) -> bool:
    return bool(outer is not None and inner is not None and outer.start_byte <= inner.start_byte and inner.end_byte <= outer.end_byte)


def _operand(node: Any) -> Any:
    node = unwrap(node)
    while node is not None and node.type == "await_expression":
        node = unwrap(next(iter(_children(node)), None))
    return node


class _Delivery:
    def __init__(self, analysis: Any):
        self.a = analysis
        self.parts: dict[str, dict] = {}

    def nodes(self, role: str, *, nested: bool = False) -> list[Any]:
        document, _, function = self.a.roles[role]
        return self.a.nodes(document, _field(function, "body"), nested=nested)

    def identity(self, document: Any, node: Any) -> dict | None:
        node = unwrap(node)
        if node is None or node.type not in {"identifier", "shorthand_property_identifier", "shorthand_property_identifier_pattern"}:
            return None
        identity = self.a.lexical(document).resolve(node)
        return identity if identity.get("state") == "unique" and identity.get("identity_complete") else None

    def path(self, document: Any, node: Any) -> tuple[str, tuple[str, ...]] | None:
        node = unwrap(node)
        if node is None:
            return None
        identity = self.identity(document, node)
        if identity:
            return identity["declaration_id"], ()
        if node.type in {"member_expression", "subscript_expression"}:
            root = self.path(document, _field(node, "object"))
            child = _field(node, "property") if node.type == "member_expression" else unwrap(_field(node, "index"))
            key = self.key(document, child) if node.type == "member_expression" or child is not None and child.type == "string" else None
            return (root[0], (*root[1], key)) if root and key is not None else None
        return None

    def key(self, document: Any, node: Any) -> str | None:
        if node is None:
            return None
        if node.type in {"identifier", "property_identifier", "shorthand_property_identifier"}:
            text = document.text(node)
            return text if "\\" not in text else None
        return _literal_string(document.text(node)) if node.type == "string" else None

    def literal(self, document: Any, node: Any) -> Any:
        node = unwrap(node)
        if node is None:
            return None
        if node.type == "string":
            return _literal_string(document.text(node))
        return True if node.type == "true" else False if node.type == "false" else None

    def operator(self, document: Any, node: Any) -> str:
        return document.text(_field(node, "operator"))

    def declarations(self, role: str) -> list[tuple[Any, Any, dict]]:
        document = self.a.roles[role][0]
        result = []
        for node in self.nodes(role):
            if node.type == "variable_declarator":
                identity = self.identity(document, _field(node, "name"))
                value = unwrap(_field(node, "value"))
                if identity and value is not None:
                    result.append((node, value, identity))
        return result

    def refs(self, document: Any, node: Any) -> set[str]:
        return {identity["declaration_id"] for part in self.a.nodes(document, node)
            if (identity := self.identity(document, part)) is not None}

    def call_node(self, record: dict) -> Any:
        return self.a.call_nodes[record["id"]][2]

    def calls(self, role: str, target: str, *, source_candidate: bool = False) -> list[dict]:
        definition = self.a.roles[target][1]
        records = [call for call in self.a.calls_by_role[role]
            if call["actual_callee_graph_node_id"] == definition.graph_node_id and call["authenticated_call_edge_id"]]
        if not source_candidate:
            return records
        document, _, function = self.a.roles[role]
        target_document, _, target_function = self.a.roles[target]
        def enclosing_class(node: Any) -> Any:
            while node is not None:
                if node.type in {"class_declaration", "class"}:
                    return node
                node = node.parent
            return None
        owner_class, target_class = enclosing_class(function), enclosing_class(target_function)
        if document is not target_document or owner_class is None or owner_class != target_class:
            return records
        target_name = self.key(document, _field(target_function, "name"))
        edges = {edge.id: edge for edge in self.a.snapshot.edges}
        for call in self.a.calls_by_role[role]:
            if call["actual_callee_graph_node_id"] is not None:
                continue
            node = self.call_node(call)
            callee = unwrap(_field(node, "function"))
            receiver = unwrap(_field(callee, "object"))
            edge = edges.get(call.get("captured_site_edge_id"))
            if (callee is None or callee.type != "member_expression" or receiver is None or receiver.type != "this"
                    or self.key(document, _field(callee, "property")) != target_name
                    or edge is None or edge.source != call["owner_graph_node_id"]
                    or edge.candidates != [definition.graph_node_id] or edge.resolution not in {"dynamic", "candidate"}):
                continue
            records.append(self.a.fact("delivery_same_class_method_source_candidate", document, node,
                captured_call_fact_id=call["id"], candidate_callee_graph_node_id=definition.graph_node_id,
                captured_site_edge_id=edge.id, captured_resolution=edge.resolution,
                selected_candidate_definition_location=target_document.location(target_function),
                source_class_location=document.location(owner_class), arguments=call["arguments"],
                actual_callee_graph_node_id=None, authenticated_call_edge_id=None,
                current_receiver_method_or_runtime_dispatch_proven=False))
        return records

    def authenticate_call(self, role: str, document: Any, node: Any, target_role: str) -> dict | None:
        current = node.parent
        while current is not None and current.type not in _FUNCTIONS:
            current = current.parent
        owner = document.definition_for_ast(current) if current is not None else None
        edge, issues = self.a.sources.call_binding(node, document, owner)
        if edge is None or edge.target != self.a.roles[target_role][1].graph_node_id:
            self.a.gap("delivery_nested_call_binding_unknown", document, node, target_role=target_role, source_issues=issues)
            return None
        return self.a.fact("delivery_actual_nested_call", document, node, role=role,
            actual_callee_graph_node_id=edge.target, owner_graph_node_id=edge.source, authenticated_call_edge_id=edge.id,
            arguments=[self.a.expression(document, child) for child in _children(_field(node, "arguments"))],
            callback_activation_proven=False, normal_result_or_effect_proven=False)

    def pairs(self, document: Any, node: Any) -> list[tuple[str, Any]]:
        node = unwrap(node)
        if node is None or node.type != "object":
            return []
        result = []
        for part in _children(node):
            if part.type == "pair":
                key = self.key(document, _field(part, "key"))
                if key is not None:
                    result.append((key, unwrap(_field(part, "value"))))
            elif part.type == "shorthand_property_identifier":
                key = self.key(document, part)
                if key is not None:
                    result.append((key, part))
        return result

    def branch_exit(self, node: Any, kind: str) -> Any:
        if node is None:
            return None
        if node.type == kind:
            return node
        children = _children(node)
        if node.type == "statement_block" and children and children[-1].type == kind and all(
                child.type in {"expression_statement", "lexical_declaration", "variable_declaration"} for child in children[:-1]):
            return children[-1]
        return None

    def finalizer(self) -> dict:
        document, _, function = self.a.roles["finalizer"]
        declarations = self.declarations("finalizer")
        matches = []
        for require_node, require_value, require_id in declarations:
            if require_value.type != "binary_expression" or self.operator(document, require_value) != "&&":
                continue
            enabled, success = unwrap(_field(require_value, "left")), unwrap(_field(require_value, "right"))
            if enabled is None or success is None or enabled.type != success.type or enabled.type != "binary_expression":
                continue
            enabled_path = self.path(document, _field(enabled, "left"))
            execution_path = self.path(document, _field(success, "left"))
            success_literal = self.literal(document, _field(success, "right"))
            if (self.operator(document, enabled) != "===" or self.literal(document, _field(enabled, "right")) is not True
                    or self.operator(document, success) != "===" or type(success_literal) is not str or not enabled_path or not execution_path):
                continue
            for ok_node, ok_value, ok_id in declarations:
                if ok_value.type != "binary_expression" or self.operator(document, ok_value) != "||":
                    continue
                not_required, result_ok = unwrap(_field(ok_value, "left")), unwrap(_field(ok_value, "right"))
                if (not_required is None or not_required.type != "unary_expression" or self.operator(document, not_required) != "!"
                        or self.path(document, _field(not_required, "argument")) != (require_id["declaration_id"], ())
                        or result_ok is None or result_ok.type != "binary_expression" or self.operator(document, result_ok) != "==="
                        or self.literal(document, _field(result_ok, "right")) is not True):
                    continue
                finalizer_path = self.path(document, _field(result_ok, "left"))
                if finalizer_path is None:
                    continue
                for persisted_node, persisted_value, persisted_id in declarations:
                    if persisted_value.type != "ternary_expression" or self.path(document, _field(persisted_value, "condition")) != (ok_id["declaration_id"], ()):
                        continue
                    if self.path(document, _field(persisted_value, "consequence")) != (execution_path[0], ()):
                        continue
                    failure = _operand(_field(persisted_value, "alternative"))
                    failure_calls = [call for call in self.calls("finalizer", "failure_result") if self.call_node(call).id == failure.id] if failure is not None else []
                    if len(failure_calls) != 1:
                        continue
                    call_args = _children(_field(failure, "arguments"))
                    if len(call_args) < 2 or self.path(document, call_args[0]) != (execution_path[0], ()) or self.path(document, call_args[1]) != (finalizer_path[0], ()):
                        continue
                    publications = []
                    for call in self.a.calls_by_role["finalizer"]:
                        node = self.call_node(call)
                        args = _children(_field(node, "arguments"))
                        if len(args) != 2 or unwrap(args[1]).type != "object":
                            continue
                        payload = self.pairs(document, args[1])
                        persisted_fields = [key for key, value in payload if self.path(document, value) == (persisted_id["declaration_id"], ())]
                        finalization_fields = [(key, value) for key, value in payload if value is not None and value.type == "object"
                            and {require_id["declaration_id"], ok_id["declaration_id"]} <= self.refs(document, value)]
                        if persisted_fields and finalization_fields:
                            publications.append(self.a.fact("delivery_conditional_persisted_result_payload", document, node,
                                call_fact_id=call["id"], writer_port=self.a.expression(document, _field(node, "function")),
                                result_path_argument=self.a.expression(document, args[0]), payload=self.a.expression(document, args[1]),
                                persisted_job_result_fields=persisted_fields, finalization_fields=[key for key, _ in finalization_fields],
                                write_runtime_success_proven=False))
                    if not publications:
                        continue
                    truth_table = [{"auto_finalize_enabled": auto, "execution_success_status": completed,
                        "finalizer_ok": finalized, "finalization_required": auto and completed,
                        "finalization_ok": not (auto and completed) or finalized,
                        "persisted_result_source": "execution_result" if not (auto and completed) or finalized else "failure_result"}
                        for auto, completed, finalized in product((False, True), repeat=3)]
                    fact = self.a.fact("delivery_execution_success_requires_conditional_finalization", document, require_node,
                        required_expression=self.a.expression(document, require_value), ok_expression=self.a.expression(document, ok_value),
                        persisted_expression=self.a.expression(document, persisted_value), execution_success_literal=success_literal,
                        metadata_enable_path=enabled_path, execution_status_path=execution_path, finalizer_ok_path=finalizer_path,
                        failure_call_fact_id=failure_calls[0]["id"], truth_table=truth_table, publications=publications,
                        actual_execution_or_finalizer_success_proven=False)
                    matches.append({"fact": fact, "supported": True})
        failure_document, _, failure_function = self.a.roles["failure_result"]
        returns = [node for node in self.nodes("failure_result") if node.type == "return_statement"]
        failure_objects = [self.a.expression(failure_document, next(iter(_children(node)), None)) for node in returns]
        result = {"supported": len(matches) == 1 and bool(failure_objects), "conditional_finalization": matches,
            "failure_result_constructions": failure_objects, "remote_finalization_success_proven": False}
        if not result["supported"]:
            self.a.gap("delivery_finalization_formula_or_persistence_unclosed", document, function)
        return result

    def worker(self) -> dict:
        worker_document, _, worker_function = self.a.roles["worker"]
        publication_calls = self.calls("worker", "publication")
        callbacks = []
        for call in publication_calls:
            node = self.call_node(call)
            for argument in _children(_field(node, "arguments")):
                for key, value in self.pairs(worker_document, argument):
                    if value is None or value.type != "arrow_function":
                        continue
                    nested = self.a.nodes(worker_document, _field(value, "body"))
                    for candidate in (part for part in nested if part.type == "call_expression"):
                        edge, _ = self.a.sources.call_binding(candidate, worker_document, worker_document.definition_for_ast(value))
                        if edge is not None and edge.target == self.a.roles["finalizer"][1].graph_node_id:
                            nested_fact = self.authenticate_call("worker", worker_document, candidate, "finalizer")
                            callbacks.append(self.a.fact("delivery_worker_finalizer_callback_installation", worker_document, value,
                                publication_call_fact_id=call["id"], production_callback_field=key,
                                finalizer_call=nested_fact, finalizer_arguments=[self.a.expression(worker_document, child) for child in _children(_field(candidate, "arguments"))],
                                callback_parameters=[self.a.expression(worker_document, child) for child in _children(_field(value, "parameters"))],
                                actual_callback_activation_proven=False))
        document, _, function = self.a.roles["publication"]
        writer_calls = self.calls("publication", "writer")
        declarations = self.declarations("publication")
        captured = []
        for call in self.a.calls_by_role["publication"]:
            node = self.call_node(call)
            for argument in _children(_field(node, "arguments")):
                if argument.type != "arrow_function":
                    continue
                writes = [part for part in self.a.nodes(document, _field(argument, "body")) if part.type == "assignment_expression" and unwrap(_field(part, "right")) is not None and unwrap(_field(part, "right")).type == "object"]
                abrupt = [part for part in self.a.nodes(document, _field(argument, "body")) if part.type == "if_statement"
                    and self.branch_exit(_field(part, "consequence"), "throw_statement") is not None]
                if writes and abrupt:
                    captured.append(self.a.fact("delivery_deferred_single_publication_capture", document, argument,
                        capture_call_fact_id=call["id"], assignments=[self.a.expression(document, write) for write in writes],
                        rejecting_capture_guards=[self.a.expression(document, _field(guard, "condition")) for guard in abrupt],
                        physical_write_deferred_to_writer_call_ids=[call["id"] for call in writer_calls],
                        physical_capture_write_or_exactly_once_proven=False))
        guards = [self.a.fact("delivery_worktree_publication_source_guard", document, node,
            condition=self.a.expression(document, _field(node, "condition")),
            consequence=self.a.expression(document, _field(node, "consequence")),
            publication_writer_call_ids=[call["id"] for call in writer_calls], actual_cleanup_or_retention_success_proven=False)
            for node in self.nodes("publication") if node.type == "if_statement" and node.start_byte < (writer_calls[0]["location"]["start_byte"] if writer_calls else function.end_byte)]
        sync_calls = self.calls("worker", "assignment_sync")
        result = {"supported": bool(callbacks and captured and writer_calls and sync_calls), "finalizer_callback_installations": callbacks,
            "deferred_capture": captured, "publication_guards": guards, "verified_writer_calls": writer_calls,
            "assignment_sync_calls": sync_calls, "direct_assignment_sync_sequence": self.a.sequence("assignment_sync"),
            "successful_execution_equals_completed_assignment_or_remote_delivery": False}
        if not result["supported"]:
            self.a.gap("delivery_worker_publication_or_sync_connection_unclosed", worker_document, worker_function)
        return result

    def writer(self) -> dict:
        document, _, function = self.a.roles["writer"]
        records = self.a.calls_by_role["writer"]
        writes = [call for call in records if call.get("call_is_entire_binding_initializer") and call.get("result_binding_source")
            and len(_children(_field(self.call_node(call), "arguments"))) == 2]
        matches = []
        for write in writes:
            write_node = self.call_node(write)
            args = _children(_field(write_node, "arguments"))
            file_path = self.path(document, args[0])
            intended_path = self.path(document, args[1])
            binding = write["result_binding_source"]
            if not file_path or not intended_path or not binding.get("declaration_id"):
                continue
            created, invalid = [], []
            for guard in (node for node in self.nodes("writer") if node.type == "if_statement"):
                condition = unwrap(_field(guard, "condition"))
                if condition is None or condition.type != "binary_expression" or self.path(document, _field(condition, "left")) != (binding["declaration_id"], ()):
                    continue
                right, operator = self.literal(document, _field(condition, "right")), self.operator(document, condition)
                if operator == "===" and right is True and self.branch_exit(_field(guard, "consequence"), "return_statement") is not None:
                    created.append(self.a.expression(document, guard))
                if operator == "!==" and right is False and self.branch_exit(_field(guard, "consequence"), "throw_statement") is not None:
                    invalid.append(self.a.expression(document, guard))
            reads = []
            for record in records:
                node = self.call_node(record)
                arguments = _children(_field(node, "arguments"))
                if record["authenticated_call_edge_id"] and arguments and self.path(document, arguments[0]) == file_path and node.start_byte > write_node.end_byte:
                    reads.append(record)
            equality = []
            for guard in (node for node in self.nodes("writer") if node.type == "if_statement"):
                condition = unwrap(_field(guard, "condition"))
                call = unwrap(_field(condition, "argument")) if condition is not None and condition.type == "unary_expression" and self.operator(document, condition) == "!" else None
                if call is None or call.type != "call_expression" or self.branch_exit(_field(guard, "consequence"), "throw_statement") is None:
                    continue
                callee = self.identity(document, _field(call, "function"))
                imported = callee.get("import") or {} if callee else {}
                arguments = _children(_field(call, "arguments"))
                if imported.get("module") == "node:util" and imported.get("imported_name") == "isDeepStrictEqual" and len(arguments) == 2 and self.path(document, arguments[1]) == intended_path:
                    equality.append(self.a.fact("delivery_existing_result_equality_conflict_guard", document, guard,
                        compared_existing=self.a.expression(document, arguments[0]), intended=self.a.expression(document, arguments[1]),
                        imported_comparator=imported, source_mismatch_throws=True, physical_readback_or_equality_verified=False))
            if created and invalid and reads and equality:
                matches.append(self.a.fact("delivery_terminal_writer_created_or_verified_existing", document, write_node,
                    writer_call_fact_id=write["id"], file_binding_path=file_path, intended_binding_path=intended_path,
                    created_result_branches=created, invalid_writer_result_guards=invalid, same_file_readback_calls=reads,
                    existing_equality_conflict_guards=equality, source_returns=[self.a.expression(document, node) for node in self.nodes("writer") if node.type == "return_statement"],
                    remote_success_or_global_exactly_once_proven=False))
        result = {"supported": len(matches) == 1, "write_or_readback_cases": matches,
            "runtime_persistence_or_idempotency_verified": False}
        if not result["supported"]:
            self.a.gap("delivery_terminal_write_readback_relation_unclosed", document, function)
        return result

    def reconcile(self) -> dict:
        document, _, function = self.a.roles["queue_projection"]
        validations = {role: self.calls("queue_projection", role) for role in ("finalizer_contract", "git_readback", "journal", "recovery")}
        declarations = self.declarations("queue_projection")
        validation_groups = []
        for node, value, identity in declarations:
            if value.type != "binary_expression" or self.operator(document, value) != "&&":
                continue
            required = [validations[role] for role in ("finalizer_contract", "git_readback", "journal")]
            if all(any(_inside(value, self.call_node(call)) for call in records) for records in required):
                validation_groups.append(self.a.fact("delivery_reconciler_conjunctive_success_evidence", document, node,
                    validation_binding_id=identity["declaration_id"], expression=self.a.expression(document, value),
                    validator_calls={role: records for role, records in validations.items() if role != "recovery"},
                    all_conjunctive_call_ids=[call["id"] for call in self.a.calls_by_role["queue_projection"] if _inside(value, self.call_node(call))],
                    checks_actually_succeed_or_remote_receipts_truthful_proven=False))
        conditional_results = []
        for node, value, identity in declarations:
            if value.type == "ternary_expression" and any(part.type == "object" for part in _children(value)):
                conditional_results.append(self.a.fact("delivery_reconciler_effective_result_construction", document, node,
                    binding_id=identity["declaration_id"], expression=self.a.expression(document, value),
                    source_condition_reference_ids=sorted(self.refs(document, _field(value, "condition"))),
                    source_branch_or_current_result_value_proven=False))
        reader_calls = self.calls("reconcile", "attempt_read", source_candidate=True)
        sequences = {role: self.a.sequence(role) for role in ("attempt_read", "queue_projection", "finalizer_contract", "git_readback", "journal", "recovery")}
        record = self.a.fact("delivery_attempt_finalizer_journal_projection_conditions", document, function,
            selected_attempt_reader_calls=reader_calls, validation_groups=validation_groups,
            effective_result_constructions=conditional_results, recovery_plan_calls=validations["recovery"],
            source_conditions=sequences, queue_projection_calls=self.a.calls_by_role["queue_projection"],
            execution_attempt_result_and_queue_projection_are_distinct=True,
            all_recovery_paths_complete_or_eventually_converge_proven=False, remote_delivery_success_proven=False)
        result = {"supported": bool(reader_calls and len(validation_groups) == 1 and conditional_results
            and all(validations.values()) and all(sequences[role]["conditions"] for role in ("attempt_read", "finalizer_contract", "git_readback", "journal", "recovery"))),
            "projection_conditions": record, "storage_and_queue_mutation_runtime_success_proven": False}
        if not result["supported"]:
            self.a.gap("delivery_reconciler_attempt_finalizer_journal_conditions_unclosed", document, function)
        return result

    def run(self) -> dict:
        missing = sorted(_ROLES - set(self.a.roles))
        if missing:
            self.a.gap("delivery_source_roles_missing", roles=missing)
            return {"version": VERSION, "scoped_source_supported": False, "missing_roles": missing}
        for name in ("finalizer", "worker", "writer", "reconcile"):
            self.parts[name] = getattr(self, name)()
        supported = all(part["supported"] for part in self.parts.values()) and not self.a.incomplete
        return {"version": VERSION, "scoped_source_supported": supported, "components": self.parts,
            "source_execution_result": "original execution result or finalizer-failure construction, selected by extracted conditional formula",
            "source_delivery_result": "deferred result publication subject to cleanup/retention/fence and created-or-equal-readback branches",
            "source_projection_result": "current attempt, finalizer contract, mode readback, journal and recovery conditions before queue projection",
            "target_execution_observed": False, "remote_success_proven": False, "exactly_once_proven": False,
            "all_recovery_complete_proven": False, "all_function_paths_or_hidden_effects_proven": False,
            "interpretation": "The captured normal source chain separates execution, terminal delivery and queue projection; external I/O and provider outcomes remain conditional."}


def analyze_pattern(analysis: Any) -> dict:
    """Fixed report pattern, with all intermediates extracted from saved source."""
    return _Delivery(analysis).run()
