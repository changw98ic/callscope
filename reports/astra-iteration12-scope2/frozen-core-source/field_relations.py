"""Finite source-expression relations beside selected-field heap assessments.

Only authenticated saved AST, lexical declarations and existing CALLS edges
are inputs.  A static member path identifies expression syntax, never a stable
receiver object.  These records do not modify semantic_ir or certify Set,
current heap contents, original parameter values, or Promise fulfillment.
"""
from __future__ import annotations

from typing import Any

from .completion_summaries import function_kind
from .semantic_sources import unwrap
from .static_contracts import _digest, _literal_string

VERSION = "captured-field-source-relations-1"
PROOF_DOMAIN = "captured_ast_and_lexical_binding"
_LIMIT, _DEPTH, _RELATIONS = 4096, 12, 256
_FUNCTIONS = frozenset({"function_declaration", "generator_function_declaration",
    "function_expression", "generator_function", "arrow_function", "method_definition"})
_NESTED = _FUNCTIONS | {"class", "class_declaration", "class_expression"}
_TYPE_ONLY_NODES = frozenset({"type_annotation", "type_alias_declaration", "interface_declaration", "type_query",
    "type_arguments", "type_parameters", "implements_clause", "import_type", "function_type"})
_ERASED = _TYPE_ONLY_NODES | {"comment"}
_TYPE_WRAPPERS = frozenset({"as_expression", "satisfies_expression", "type_assertion", "non_null_expression"})
_CONTROL_UNKNOWN = frozenset({"for_statement", "for_in_statement", "while_statement",
    "do_statement", "switch_statement", "try_statement", "with_statement",
    "labeled_statement"})
_WRITES = frozenset({"assignment_expression", "augmented_assignment_expression",
    "update_expression"})
_LIMITATIONS = (
    "source paths identify lexical declarations and member syntax, not stable receiver identities",
    "ordinary Set attempts may invoke setters or Proxy effects; successful writes and indirect mutation are unknown",
    "current reaching binding reads do not prove equality with the initial parameter value",
    "source construction plans do not certify current copy surfaces, selected slot presence or reaching value origin",
    "normal source order is conditional on the selected operations being reached normally",
    "body return expressions do not prove async fulfillment, callee activation or transport",
)


def _children(node: Any) -> list[Any]:
    return [child for child in node.named_children
        if child.type not in _ERASED and not child.type.endswith("_type")] if node is not None else []


def _runtime_children(node: Any) -> list[Any]:
    """Match the field adapter's type erasure without importing its module."""
    if node.type in _TYPE_WRAPPERS:
        operand = unwrap(node)
        if operand is not None and operand.id != node.id:
            return [operand]
    return _children(node)


def _field(node: Any, name: str) -> Any:
    return node.child_by_field_name(name) if node is not None else None


def _inside(outer: Any, inner: Any) -> bool:
    return bool(outer is not None and inner is not None
        and outer.start_byte <= inner.start_byte and inner.end_byte <= outer.end_byte)


def _function(definition: Any) -> Any:
    node = unwrap(definition.value) if definition is not None and definition.value is not None else getattr(definition, "node", None)
    return node if node is not None and node.type in _FUNCTIONS else None


def _identity(record: dict) -> dict:
    """Declaration facts only; reader value-stability is deliberately excluded."""
    return {key: record.get(key) for key in ("state", "identity_complete", "declaration_id",
        "declaration_kind", "parameter_index", "name", "declaration_location", "binder_location")}


class _Collector:
    def __init__(self, sources: Any, document: Any, definition: Any, lexical: Any,
                 site: Any, subject_parameter: dict, sink: dict,
                 field_path: list[str], branch_conditions: list[dict]):
        self.sources, self.document, self.definition = sources, document, definition
        self.lexical, self.site, self.function = lexical, site, _function(definition)
        self.subject, self.sink, self.field_path = subject_parameter, sink, list(field_path)
        self.conditions = branch_conditions
        self.operations = 0
        self.incomplete = False
        self.relations: list[dict] = []
        self.copy_plans: list[dict] = []
        self.gaps: list[dict] = []
        self.excluded_nested: list[dict] = []
        self.prefix_controls: list[dict] = []
        self.phase = "body_return_expression_before_promise_assimilation" if site is not None and site.type == "return_statement" else "call_argument_before_callee_activation"
        self.context_id = _digest({"version": VERSION, "snapshot": getattr(document, "snapshot_id", ""),
            "source": getattr(getattr(document, "source", None), "hash", ""),
            "owner": getattr(definition, "graph_node_id", ""),
            "site": (site.start_byte, site.end_byte) if site is not None else None,
            "subject": subject_parameter.get("declaration_id"), "sink": sink,
            "field_path": field_path, "branch_conditions": branch_conditions})[:24]

    def tick(self) -> bool:
        self.operations += 1
        if self.operations > _LIMIT:
            self.incomplete = True
            return False
        return True

    def location(self, node: Any) -> dict | None:
        return self.document.location(node) if node is not None and self.document.contains(node) else None

    def gap(self, code: str, node: Any = None, **details: Any) -> None:
        record = {"code": code, "location": self.location(node), **details}
        if record not in self.gaps:
            self.gaps.append(record)

    def name(self, node: Any) -> str | None:
        if node is None:
            return None
        text = self.document.text(node)
        if node.type in {"identifier", "property_identifier", "shorthand_property_identifier"}:
            return text if text and "\\" not in text else None
        if node.type == "string":
            text = _literal_string(text)
            return text if text is not None and not any(0xD800 <= ord(char) <= 0xDFFF for char in text) else None
        return None

    def path(self, node: Any) -> dict | None:
        """Resolve root declaration even when one member key is dynamic."""
        current = unwrap(node)
        parts: list[str | None] = []
        depth = 0
        while current is not None and current.type in {"member_expression", "subscript_expression"}:
            depth += 1
            if depth > _DEPTH or not self.tick():
                self.incomplete = True
                return None
            child = _field(current, "property") if current.type == "member_expression" else unwrap(_field(current, "index"))
            key = self.name(child) if current.type == "member_expression" or child is not None and child.type == "string" else None
            parts.append(key)
            current = unwrap(_field(current, "object"))
        if current is None or current.type not in {"identifier", "shorthand_property_identifier"}:
            return None
        identity = self.lexical.resolve(current)
        if identity.get("state") != "unique" or not identity.get("identity_complete") or not identity.get("declaration_id"):
            return None
        return {"root_declaration": _identity(identity), "member_keys": list(reversed(parts)),
            "static_path_complete": all(key is not None for key in parts),
            "location": self.location(node), "root_reference_location": self.location(current),
            "referent_identity_proven": False, "initial_parameter_value_identity_proven": False}

    def operand(self, node: Any, depth: int = 0) -> dict:
        node = unwrap(node)
        if node is None or depth >= _DEPTH or not self.tick():
            if depth >= _DEPTH:
                self.incomplete = True
            return {"kind": "unknown", "location": self.location(node), "structure_complete": False}
        kind = node.type
        result: dict = {"kind": kind, "location": self.location(node),
            "expression_id": _digest({"version": VERSION, "source": self.document.source.hash,
                "parse": self.document.parse_id, "snapshot": self.document.snapshot_id,
                "span": (node.start_byte, node.end_byte)})[:24], "structure_complete": True}
        if kind in {"identifier", "shorthand_property_identifier", "member_expression", "subscript_expression"}:
            result["source_path"] = self.path(node)
            result["binding_identity_complete"] = result["source_path"] is not None
            result["kind"] = "binding_reference" if kind in {"identifier", "shorthand_property_identifier"} else "member_access"
            if kind in {"member_expression", "subscript_expression"} and result["source_path"] is None:
                result["receiver"] = self.operand(_field(node, "object"), depth + 1)
            source_path = result["source_path"]
            if kind == "subscript_expression" and (source_path is None or not source_path["static_path_complete"]):
                result["index"] = self.operand(_field(node, "index"), depth + 1)
        elif kind in {"string", "number", "true", "false", "null", "undefined"}:
            result["kind"] = "literal_source_expression"
            result["literal_kind"] = kind
            result["source_text"] = self.document.text(node)
            result["runtime_literal_identity_verified"] = False
        elif kind in {"binary_expression", "assignment_expression", "augmented_assignment_expression"}:
            result["operator"] = self.document.text(_field(node, "operator"))
            result["left"] = self.operand(_field(node, "left"), depth + 1)
            result["right"] = self.operand(_field(node, "right"), depth + 1)
        elif kind in {"unary_expression", "update_expression", "await_expression"}:
            result["operator"] = self.document.text(_field(node, "operator")) or ("await" if kind == "await_expression" else "")
            argument = _field(node, "argument") or next(iter(_children(node)), None)
            result["argument"] = self.operand(argument, depth + 1)
        elif kind in {"call_expression", "new_expression"}:
            result["callee"] = self.operand(_field(node, "function") or _field(node, "constructor"), depth + 1)
            result["arguments"] = [self.operand(child, depth + 1) for child in _children(_field(node, "arguments"))]
            result["callee_runtime_identity_or_purity_proven"] = False
        elif kind == "ternary_expression":
            result["condition"] = self.operand(_field(node, "condition"), depth + 1)
            result["consequence"] = self.operand(_field(node, "consequence"), depth + 1)
            result["alternative"] = self.operand(_field(node, "alternative"), depth + 1)
        elif kind == "object":
            result["kind"] = "object_construction"
            result["parts"] = self.object_parts(node, depth + 1)
            result["explicit_key_coverage_complete"] = (not self.incomplete
                and len(result["parts"]) == len(_children(node))
                and all(part["kind"] in {"spread", "static_data_property"} for part in result["parts"]))
            result["new_literal_destination"] = True
            result["whole_shape_closed"] = False
        else:
            result["kind"] = "unknown_source_expression"
            result["node_type"] = kind
            result["structure_complete"] = False
        return result

    def object_parts(self, node: Any, depth: int = 0) -> list[dict]:
        parts = []
        for index, child in enumerate(_children(node)):
            if not self.tick():
                break
            part = {"index": index, "location": self.location(child)}
            if child.type == "spread_element":
                part.update(kind="spread", operand=self.operand(next(iter(_children(child)), None), depth + 1))
            elif child.type in {"pair", "shorthand_property_identifier"}:
                key = self.name(_field(child, "key") if child.type == "pair" else child)
                value = _field(child, "value") if child.type == "pair" else child
                part.update(kind="static_data_property" if key is not None and key != "__proto__" else "unknown_member",
                    key=key, operand=self.operand(value, depth + 1))
            else:
                part.update(kind="unknown_member", node_type=child.type, key=None)
            parts.append(part)
        return parts

    def membership(self, node: Any) -> list[dict]:
        result = []
        current = node.parent if node is not None else None
        while current is not None and current != self.function:
            if current.type == "if_statement":
                condition = _field(current, "condition")
                branch = "then" if _inside(_field(current, "consequence"), node) else "else" if _inside(_field(current, "alternative"), node) else "condition"
                selected = []
                for record in self.conditions:
                    location = record.get("location", {})
                    if condition is not None and location.get("start_byte") == condition.start_byte and location.get("end_byte") == condition.end_byte and location.get("file") == self.document.source.path:
                        selected.append(record.get("branch"))
                compatibility = "alternative_selected_branch" if selected and branch not in selected and branch != "condition" else "on_selected_branch" if selected else "conditional_branch_not_selected_by_this_assessment"
                result.append({"condition_location": self.location(condition), "branch": branch,
                    "selected_path_relation": compatibility, "runtime_condition_truth_proven": False})
            current = current.parent
        return list(reversed(result))

    def relation(self, kind: str, node: Any, payload: dict, *, status: str = "proven_source_structure", phase: str | None = None) -> dict:
        record = {"kind": kind, "status": status, "proof_domain": PROOF_DOMAIN,
            "phase": phase or self.phase, "location": self.location(node),
            "owner_graph_node_id": self.definition.graph_node_id,
            "source_context": self.context_id, "branch_membership": self.membership(node),
            "selected_site_branch_conditions": self.conditions, "payload": payload,
            "selected_heap_projection_upgraded": False, "runtime_value_verified": False}
        record["id"] = _digest({"version": VERSION, **record})[:24]
        if len(self.relations) < _RELATIONS:
            self.relations.append(record)
        else:
            self.incomplete = True
        return record

    def prefix(self) -> list[Any]:
        """Enumerate direct runtime syntax before the complete selected site."""
        nodes = []
        pending = [_field(self.function, "body")]
        while pending:
            node = pending.pop()
            if node is None or node.start_byte >= self.site.start_byte:
                continue
            if node.type in _TYPE_ONLY_NODES or node.type.endswith("_type"):
                continue
            if not self.tick():
                break
            if node.type in _NESTED:
                self.excluded_nested.append(self.location(node))
                continue
            if node.type in _CONTROL_UNKNOWN:
                self.prefix_controls.append(self.location(node))
            if node.end_byte <= self.site.start_byte:
                nodes.append(node)
            pending.extend(reversed(_runtime_children(node)))
        return nodes

    def order_basis(self, node: Any, successor: Any = None) -> dict | None:
        """Common block siblings prove conditional source order, not CFG reachability."""
        successor = self.site if successor is None else successor
        ancestors: dict[int, tuple[Any, Any]] = {}
        child, parent = node, node.parent
        while parent is not None and parent != self.function:
            if parent.type in _CONTROL_UNKNOWN | _NESTED:
                return None
            if parent.type == "statement_block":
                ancestors[parent.id] = (parent, child)
            child, parent = parent, parent.parent
        child, parent = successor, successor.parent
        while parent is not None and parent != self.function:
            if parent.type in _CONTROL_UNKNOWN | _NESTED:
                return None
            if parent.id in ancestors:
                block, before = ancestors[parent.id]
                siblings = _children(block)
                left = next((index for index, item in enumerate(siblings) if item.id == before.id), None)
                right = next((index for index, item in enumerate(siblings) if item.id == child.id), None)
                if left is not None and right is not None and left < right:
                    return {"owning_block_location": self.location(block), "predecessor_statement_location": self.location(before),
                        "successor_statement_location": self.location(child), "predecessor_statement_index": left,
                        "successor_statement_index": right, "order": "before_if_both_reached_normally",
                        "arbitrary_control_reachability_proven": False}
            child, parent = parent, parent.parent
        return None

    def construction(self, node: Any, selected_key: str | None, *, destination: dict | None = None) -> dict:
        operand = self.operand(node)
        parts = operand.get("parts", [])
        record = self.relation("ordered_object_construction", node, {"construction": operand,
            "destination_declaration": destination, "explicit_static_keys": [part["key"] for part in parts if part["kind"] == "static_data_property"],
            "explicit_key_coverage_complete": operand.get("explicit_key_coverage_complete", False)}, phase="initializer_expression" if destination else self.phase)
        spreads = [part for part in parts if part["kind"] == "spread"]
        for spread in spreads:
            tail = parts[spread["index"] + 1:]
            fixed = (operand.get("explicit_key_coverage_complete", False)
                and all(part["kind"] == "static_data_property" for part in tail))
            later = [part["key"] for part in tail if part["kind"] == "static_data_property"]
            plan = {"construction_relation_id": record["id"], "construction_location": self.location(node),
                "spread_location": spread["location"], "spread_operand": spread["operand"], "spread_index": spread["index"],
                "selected_key": selected_key, "is_last_spread": spread is spreads[-1],
                "later_parts": tail, "later_static_definition_keys": later,
                "later_parts_all_static_data_definitions": fixed,
                "selected_key_disjoint_from_later_static_definitions": selected_key is not None and fixed and selected_key not in later,
                "explicit_key_coverage_complete": operand.get("explicit_key_coverage_complete", False),
                "proof_domain": PROOF_DOMAIN, "phase": record["phase"],
                "local_copy_value_theorem_proven": False, "copy_surface_model_applied": False,
                "original_parameter_value_identity_proven": False, "selected_field_presence_proven": False}
            plan["id"] = _digest({"version": VERSION, "source_context": self.context_id, **plan})[:24]
            self.copy_plans.append(plan)
        return record

    def selected(self) -> tuple[Any, dict]:
        if self.site.type == "return_statement":
            expression = unwrap(next(iter(_children(self.site)), None))
            operand = self.operand(expression)
            if expression is not None and expression.type == "object":
                construction = self.construction(expression, self.sink.get("field_path", [None])[0])
                self.relation("body_return_ordered_copy_structure", self.site,
                    {"construction_relation_id": construction["id"], "return_operand": operand,
                        "function_kind": function_kind(self.document, self.function),
                        "promise_fulfillment_proven": False, "reaching_source_value_identity_proven": False})
            else:
                path = self.path(expression)
                kind = "body_return_reaching_binding_reference" if path is not None and not path["member_keys"] else "body_return_expression_structure"
                self.relation(kind, self.site, {"return_operand": operand, "function_kind": function_kind(self.document, self.function),
                    "read_is_current_reaching_binding": path is not None and not path["member_keys"],
                    "initial_parameter_value_identity_proven": False, "promise_fulfillment_proven": False},
                    status="proven_source_structure" if operand.get("structure_complete") else "unknown_source_structure")
            return expression, operand
        arguments = _children(_field(self.site, "arguments"))
        index = self.sink.get("argument_index")
        expression = arguments[index] if type(index) is int and 0 <= index < len(arguments) else None
        operand = self.operand(expression)
        edge, issues = self.sources.call_binding(self.site, self.document, self.definition)
        for issue in issues:
            self.gap("source_relation_call_binding_unknown", self.site, source_issue=issue)
        formal = None
        if edge is not None and expression is not None and not any(item.type == "spread_element" for item in arguments[:index + 1]):
            targets = self.sources.nodes.get(edge.target, [])
            target_document, target_definition, problems = self.sources.definition_for_node(targets[0]) if len(targets) == 1 else (None, None, [])
            target_function = _function(target_definition)
            parameters = _children(_field(target_function, "parameters"))
            if target_document is not None and not problems and index < len(parameters):
                formal = {"target_graph_node_id": edge.target, "parameter_index": index,
                    "location": target_document.location(parameters[index]), "function_kind": function_kind(target_document, target_function)}
        self.relation("actual_argument_formal_binding", self.site, {"argument_index": index,
            "argument_operand": operand, "edge_id": edge.id if edge else None, "formal": formal,
            "callee_activation_proven": False, "argument_selected_field_value_proven": False},
            status="proven_source_structure" if formal is not None else "unknown_source_structure")
        return expression, operand

    def collect(self) -> dict:
        result = {"version": VERSION, "proof_domain": PROOF_DOMAIN, "phase": self.phase,
            "source_context": self.context_id, "site_location": self.location(self.site),
            "branch_conditions": self.conditions, "subject_parameter": _identity(self.subject),
            "selected_operand": None, "relations": [], "copy_plans": [], "direct_write_scan": None,
            "coverage": {}, "analysis_gaps": [], "limitations": list(_LIMITATIONS),
            "selected_heap_projection_upgraded": False, "runtime_value_verified": False,
            "original_parameter_value_identity_proven": False, "promise_fulfillment_proven": False}
        loaded, issues = self.sources.load(self.document.source.path)
        actual_parameter_ids = set()
        if self.function is not None:
            for parameter in _children(_field(self.function, "parameters")):
                binder = unwrap(_field(parameter, "pattern") or _field(parameter, "name") or parameter)
                if binder is not None and binder.type == "identifier":
                    identity = self.lexical.resolve(binder)
                    if identity.get("state") == "unique" and identity.get("identity_complete"):
                        actual_parameter_ids.add(identity["declaration_id"])
        valid = (loaded is self.document and not issues and self.lexical.document is self.document
            and self.function is not None and self.document.contains(self.site)
            and _inside(_field(self.function, "body"), self.site)
            and self.document.definition_for_ast(self.definition.node) is self.definition
            and self.document.call_owner(self.site) == self.definition.graph_node_id
            and self.site.type in {"call_expression", "return_statement"}
            and self.subject.get("state") == "unique" and self.subject.get("identity_complete")
            and self.subject.get("declaration_id") in actual_parameter_ids)
        if not valid:
            self.incomplete = True
            self.gap("source_relation_inputs_not_authenticated", self.site, source_issues=issues)
        else:
            expression, operand = self.selected()
            result["selected_operand"] = operand
            selected_path = self.path(expression)
            roots = {self.subject["declaration_id"]}
            if selected_path is not None:
                roots.add(selected_path["root_declaration"]["declaration_id"])
            nodes = self.prefix()
            declarations = [node for node in nodes if node.type == "variable_declarator"]
            # Follow only actual const alias initializers and upstream literal
            # spreads. These are source dependency edges, never value equality.
            changed = True
            alias_records = []
            while changed and self.tick():
                changed = False
                for declaration in declarations:
                    binder = unwrap(_field(declaration, "name"))
                    if binder is None or binder.type != "identifier":
                        continue
                    identity = self.lexical.resolve(binder)
                    if identity.get("state") != "unique":
                        continue
                    initializer = unwrap(_field(declaration, "value"))
                    source = self.path(initializer)
                    destination_id = identity["declaration_id"]
                    if identity.get("declaration_kind") == "const" and source is not None:
                        source_id = source["root_declaration"]["declaration_id"]
                        if source_id in roots or destination_id in roots:
                            before = len(roots)
                            roots.update((source_id, destination_id))
                            changed |= len(roots) != before
                            if destination_id not in {item[0] for item in alias_records}:
                                alias_records.append((destination_id, declaration, identity, initializer))
                    if destination_id in roots and initializer is not None and initializer.type == "object":
                        for child in _children(initializer):
                            if child.type == "spread_element":
                                source = self.path(next(iter(_children(child)), None))
                                if source is not None:
                                    before = len(roots)
                                    roots.add(source["root_declaration"]["declaration_id"])
                                    changed |= len(roots) != before
            for _, declaration, identity, initializer in alias_records:
                source_path = self.path(initializer)
                bare_binding = source_path is not None and not source_path["member_keys"]
                self.relation("lexical_alias_initializer" if bare_binding else "lexical_value_initializer", declaration,
                    {"destination_declaration": _identity(identity), "source_operand": self.operand(initializer),
                        "initialization_alias_only": bare_binding, "current_referent_contents_proven": False,
                        "source_and_destination_current_value_equality_proven": False}, phase="initializer_expression")
            for declaration in declarations:
                binder, initializer = unwrap(_field(declaration, "name")), unwrap(_field(declaration, "value"))
                if binder is None or binder.type != "identifier" or initializer is None or initializer.type != "object":
                    continue
                identity = self.lexical.resolve(binder)
                if identity.get("declaration_id") in roots:
                    selected_key = selected_path["member_keys"][0] if selected_path and selected_path["member_keys"] and identity.get("declaration_id") == selected_path["root_declaration"]["declaration_id"] else (self.field_path[0] if identity.get("declaration_id") == self.subject["declaration_id"] and self.field_path else None)
                    self.construction(initializer, selected_key, destination=_identity(identity))
            writes, unmatched = [], []
            previous_write = None
            for node in nodes:
                delete = node.type == "unary_expression" and self.document.text(_field(node, "operator")) == "delete"
                if node.type not in _WRITES and not delete:
                    continue
                target = _field(node, "left") if node.type in {"assignment_expression", "augmented_assignment_expression"} else _field(node, "argument")
                target = unwrap(target)
                target_path = self.path(target)
                if target_path is None:
                    unmatched.append(self.location(node))
                    continue
                if target_path["root_declaration"]["declaration_id"] not in roots:
                    continue
                if not target_path["member_keys"]:
                    self.relation("explicit_lexical_binding_write", node, {"target": target_path,
                        "operator": self.document.text(_field(node, "operator")), "reaching_binding_value_proven": False}, phase="ordinary_set_attempt")
                    continue
                event = self.relation("explicit_member_set_attempt" if node.type == "assignment_expression" else "explicit_member_mutation_attempt", node,
                    {"target": target_path, "operator": "delete" if delete else self.document.text(_field(node, "operator")) or "=",
                        "right_operand": self.operand(_field(node, "right")) if not delete and node.type != "update_expression" else None,
                        "successful_write_proven": False, "ordinary_set_effects_excluded": False}, phase="ordinary_set_attempt")
                writes.append(event)
                basis = self.order_basis(node)
                if basis is not None:
                    self.relation("normal_prefix_program_order", node,
                        {"predecessor_relation_id": event["id"], "selected_site_location": self.location(self.site), **basis})
                if previous_write is not None:
                    previous_node, previous_event = previous_write
                    sequence_basis = self.order_basis(previous_node, node)
                    if sequence_basis is not None:
                        self.relation("normal_prefix_program_order", node,
                            {"predecessor_relation_id": previous_event["id"], "successor_relation_id": event["id"],
                                "predecessor_branch_membership": previous_event["branch_membership"],
                                "successor_branch_membership": event["branch_membership"], **sequence_basis})
                previous_write = (node, event)
                membership = self.membership(node)
                if membership:
                    self.relation("conditional_member_set_attempt", node,
                        {"set_attempt_relation_id": event["id"], "branch_membership": membership,
                            "other_branch_successful_mutation_or_alias_identity_proven": False}, phase="ordinary_set_attempt")
            expected = ([*selected_path["member_keys"], *self.sink.get("field_path", [])]
                if selected_path is not None else list(self.field_path))
            expected_root = selected_path["root_declaration"]["declaration_id"] if selected_path else self.subject["declaration_id"]
            matches = [event["id"] for event in writes if event["payload"]["target"]["root_declaration"]["declaration_id"] == expected_root
                and event["payload"]["target"]["member_keys"] == expected]
            potentially_matching = [event["id"] for event in writes if event["payload"]["target"]["root_declaration"]["declaration_id"] == expected_root
                and not event["payload"]["target"]["static_path_complete"]]
            # Some controls encode a write without an assignment-expression
            # node, e.g. the iteration target of ``for (obj.key of values)``.
            # Traversing their syntax is not a complete write interpretation.
            complete = not self.incomplete and not unmatched and not self.prefix_controls
            scan = self.relation("selected_key_direct_write_scan", self.site,
                {"scope": "selected_outer_function_direct_source_prefix_before_complete_selected_site",
                    "scope_location": self.location(_field(self.function, "body")), "end_before_byte": self.site.start_byte,
                    "root_declaration_id": expected_root, "selected_member_path": expected,
                    "scoped_enumeration_complete": complete, "explicit_static_target_match_ids": matches,
                    "dynamic_possible_target_ids": potentially_matching, "all_relevant_member_attempt_ids": [event["id"] for event in writes],
                    "unresolved_target_locations": unmatched, "nested_callable_class_bodies_excluded": self.excluded_nested,
                    "unmodeled_control_or_write_regions": self.prefix_controls,
                    "verdict": "explicit_static_target_match_seen" if matches else "unknown_selected_target_match" if potentially_matching or not complete else "no_explicit_static_target_match",
                    "no_indirect_mutation_proven": False, "own_selected_key_presence_or_preservation_proven": False},
                status="proven_source_structure" if matches or complete and not potentially_matching else "unknown_source_structure")
            result["direct_write_scan"] = scan
        if self.operations > _LIMIT:
            self.gap("source_relation_ast_budget_exhausted", self.site)
        if len(self.relations) >= _RELATIONS and self.incomplete:
            self.gap("source_relation_fact_budget_exhausted", self.site)
        if self.incomplete and result["direct_write_scan"] is not None:
            # A negative scan cannot survive a later fact/output truncation.
            scan = result["direct_write_scan"]
            scan["status"] = "unknown_source_structure"
            scan["payload"]["scoped_enumeration_complete"] = False
            if not scan["payload"]["explicit_static_target_match_ids"]:
                scan["payload"]["verdict"] = "unknown_selected_target_match"
            scan["id"] = _digest({"version": VERSION, **{key: value for key, value in scan.items() if key != "id"}})[:24]
        result.update(relations=self.relations, copy_plans=self.copy_plans,
            analysis_gaps=self.gaps, coverage={"operations": self.operations, "operation_limit": _LIMIT,
                "relation_limit": _RELATIONS, "incomplete": self.incomplete,
                "direct_prefix_enumeration_complete": valid and not self.incomplete,
                "direct_prefix_write_coverage_complete": bool(result["direct_write_scan"]
                    and result["direct_write_scan"]["payload"]["scoped_enumeration_complete"]
                    and not result["direct_write_scan"]["payload"]["dynamic_possible_target_ids"]),
                "unsupported_control_regions": self.prefix_controls,
                "nested_callable_class_bodies_excluded": self.excluded_nested,
                "all_function_paths_or_callee_effects_accounted": False})
        return result


def collect_site_relations(sources: Any, document: Any, definition: Any, lexical: Any,
                           site: Any, *, subject_parameter: dict, sink: dict,
                           field_path: list[str], branch_conditions: list[dict]) -> dict:
    """Describe one selected saved-source site without upgrading its IR result.

    ``subject_parameter`` is the unique LexicalBindings declaration record.
    ``branch_conditions`` are this site's actual adapter guard records, not
    configured intermediate expressions. All returned IDs bind the saved
    source/parse/snapshot identity, selected site and branch context.
    """
    return _Collector(sources, document, definition, lexical, site,
        subject_parameter, sink, field_path, branch_conditions).collect()
