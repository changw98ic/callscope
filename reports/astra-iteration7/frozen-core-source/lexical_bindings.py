"""Captured TS/JS declaration identities, separate from reaching values.

This is a narrow compatibility facade over the existing source-value reader.
It never reads files, evaluates an expression, follows an alias as an equal
declaration, or creates a CALLS edge. ``same=False`` means sameness was not
proved; it is not a proof that two runtime resources differ.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any

from .semantic_sources import walk, unwrap
from .value_analysis import VERSION as VALUE_READER_VERSION, _Reader, _binding_scope, _bound_names, _key

VERSION = "captured-lexical-bindings-2"
_IDENTIFIERS = {"identifier", "shorthand_property_identifier", "shorthand_property_identifier_pattern"}
_FUNCTIONS = {"function_declaration", "generator_function_declaration", "function_expression",
    "generator_function", "arrow_function", "method_definition"}
_IDENTITY_GAPS = {"with_dynamic_scope", "unresolved_lexical_binding", "duplicate_or_shadow_binding",
    "escaped_binding_or_write_not_decoded"}
_VALUE_ONLY_GAPS = {"mutable_binding_reaching_value_not_modeled", "binding_not_initialized_before_use",
    "visible_binding_or_member_write"}


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True,
        separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()


def _ancestors(node: Any):
    while node is not None:
        yield node
        node = node.parent


def _inside(outer: Any, inner: Any) -> bool:
    return outer is not None and inner is not None and outer.start_byte <= inner.start_byte and inner.end_byte <= outer.end_byte


def _function(node: Any) -> Any:
    return next((item for item in _ancestors(node) if item.type in _FUNCTIONS), None)


class _UnsupportedPattern(ValueError):
    pass


class LexicalBindings:
    def __init__(self, document: Any):
        self.document = document
        self.root = document.tree.root_node
        self.all_nodes = list(walk(self.root))
        self.reader = _Reader(document, self.root, self.root)
        self._cache: dict[int, dict] = {}
        self._declarations: dict[str, dict] = {}
        self._writes_cache: dict[str, list[dict]] = {}
        self._mutation_nodes: dict[str, Any] = {}
        self._aliases: dict[str, list[dict]] | None = None
        self._alias_gaps: dict[str, list[dict]] = {}
        self._evals = [node for node in self.all_nodes if node.type == "call_expression"
            and node.child_by_field_name("function") is not None
            and any(child.type in {"identifier", "property_identifier"} and document.text(child) == "eval"
                for child in walk(node.child_by_field_name("function")))]

    def _unknown(self, name: str, reason: str, *, state: str = "unknown", **details: Any) -> dict:
        return {"version": VERSION, "state": state, "identity_complete": False,
            "name": name, "declaration_id": None, "binding_id": None,
            "value": {"stable": False, "runtime_value_known": False, "reasons": [reason]},
            "gaps": [reason], **details}

    def _binders(self, pattern: Any, path: list[dict] | None = None) -> list[tuple[Any, list[dict]]]:
        """Enumerate only finite, static binding patterns, never their values."""
        path = path or []
        if pattern is None:
            raise _UnsupportedPattern("missing_binding_pattern")
        kind = pattern.type
        if kind in {"identifier", "shorthand_property_identifier_pattern"}:
            name = self.document.text(pattern)
            if not name or "\\" in name:
                raise _UnsupportedPattern("escaped_binding_pattern")
            return [(pattern, path)]
        if kind in {"required_parameter", "optional_parameter"}:
            parameter_path = [*path, {"kind": "default_value"}] if pattern.child_by_field_name("value") is not None else path
            return self._binders(pattern.child_by_field_name("pattern") or pattern.child_by_field_name("name"), parameter_path)
        if kind in {"assignment_pattern", "object_assignment_pattern"}:
            # The RHS is a read/effect expression, never another binder. Its
            # assignments remain in the separate full-document write review.
            return self._binders(pattern.child_by_field_name("left"), [*path, {"kind": "default_value"}])
        if kind == "rest_pattern":
            children = [child for child in pattern.named_children if child.type != "comment"]
            if (len(children) != 1 or children[0].type != "identifier"
                    or not any(item["kind"] in {"object_rest", "array_rest"} for item in path)):
                raise _UnsupportedPattern("unsupported_rest_binder_shape")
            return self._binders(children[0], path)
        if kind == "formal_parameters":
            values = []
            for index, child in enumerate(item for item in pattern.named_children if item.type not in {"comment", "type_annotation"}):
                values.extend(self._binders(child, [*path, {"kind": "parameter", "index": index}]))
            return values
        if kind == "array_pattern":
            values, index = [], 0
            for child in pattern.children:
                if child.type == ",":
                    index += 1
                elif child.is_named and child.type != "comment":
                    item_path = [*path, {"kind": "array_index", "index": index}]
                    if child.type == "rest_pattern":
                        item_path.append({"kind": "array_rest", "values_not_modeled": True})
                    values.extend(self._binders(child, item_path))
            return values
        if kind == "object_pattern":
            values = []
            for child in pattern.named_children:
                if child.type == "comment":
                    continue
                if child.type == "shorthand_property_identifier_pattern":
                    values.extend(self._binders(child, [*path, {"kind": "object_property", "name": self.document.text(child)}]))
                elif child.type == "object_assignment_pattern":
                    left = child.child_by_field_name("left")
                    if left is None or left.type not in {"identifier", "shorthand_property_identifier_pattern"}:
                        raise _UnsupportedPattern("unsupported_object_default_binder")
                    values.extend(self._binders(child, [*path, {"kind": "object_property", "name": self.document.text(left)}]))
                elif child.type == "rest_pattern":
                    values.extend(self._binders(child, [*path, {"kind": "object_rest", "excluded_keys_not_interpreted": True}]))
                elif child.type == "pair_pattern":
                    key = child.child_by_field_name("key")
                    value = child.child_by_field_name("value")
                    if key is None or key.type not in {"property_identifier", "identifier"} or "\\" in self.document.text(key):
                        raise _UnsupportedPattern("computed_or_quoted_binding_pattern")
                    values.extend(self._binders(value, [*path, {"kind": "object_property", "name": self.document.text(key)}]))
                else:
                    raise _UnsupportedPattern("default_rest_or_unsupported_binding_pattern")
            return values
        raise _UnsupportedPattern("default_rest_or_unsupported_binding_pattern")

    def _pattern(self, binding: dict) -> Any:
        node = binding["node"]
        if node.type == "variable_declarator":
            return node.child_by_field_name("name")
        if binding["kind"] == "parameter" or binding["kind"] == "loop_binding":
            return node
        if node.type in {"import_specifier", "namespace_import"}:
            return node.child_by_field_name("alias") or node.child_by_field_name("name")
        if node.type == "import_clause":
            names = [child for child in node.named_children if child.type == "identifier"]
            return names[0] if len(names) == 1 else None
        if binding["kind"] == "expression_self_name":
            return node
        return node.child_by_field_name("name")

    def _resolve_identity(self, identifier_node: Any) -> dict:
        if identifier_node is None or not self.document.contains(identifier_node):
            return self._unknown("", "identifier_not_in_captured_document")
        if identifier_node.id in self._cache:
            return deepcopy(self._cache[identifier_node.id])
        name = self.document.text(identifier_node)
        if self.document.kind == "rust":
            return self._unknown(name, "unsupported_lexical_language")
        if identifier_node.type not in _IDENTIFIERS or "\\" in name or not name.replace("$", "_").isidentifier():
            return self._unknown(name, "escaped_or_unsupported_identifier")
        # A caller may resolve the actual binder token itself. Use its genuine
        # parent context, but retain the reader's TDZ/value uncertainty.
        binding = dict(self.reader.binding(name, identifier_node))
        reason = binding.get("reason", "")
        if reason in _IDENTITY_GAPS or not binding.get("node") or not binding.get("scope"):
            result = self._unknown(name, reason or "declaration_identity_missing",
                state="ambiguous" if reason == "duplicate_or_shadow_binding" else "unknown",
                reader_version=VALUE_READER_VERSION)
            self._cache[identifier_node.id] = result
            return deepcopy(result)
        if not binding.get("known") and reason not in _VALUE_ONLY_GAPS:
            return self._unknown(name, "reader_unknown_reason_not_an_identity_model", reader_reason=reason,
                reader_version=VALUE_READER_VERSION)
        scope, declaration = binding["scope"], binding["node"]
        owner = _function(identifier_node)
        body = owner.child_by_field_name("body") if owner is not None else None
        if (owner is not None and body is not None and identifier_node.start_byte < body.start_byte
                and _inside(body, declaration) and binding["kind"] != "parameter"):
            return self._unknown(name, "parameter_default_body_scope_not_visible")
        evals = [node for node in self._evals if any(_key(item) == _key(scope) for item in _ancestors(node))
            or _function(node) == _function(identifier_node)]
        if evals:
            return self._unknown(name, "direct_eval_scope_not_closed",
                eval_locations=[self.document.location(node) for node in evals], reader_version=VALUE_READER_VERSION)
        if any(item.type == "ambient_declaration" for item in _ancestors(declaration)):
            return self._unknown(name, "ambient_value_has_no_captured_implementation")
        try:
            matches = [(binder, path) for binder, path in self._binders(self._pattern(binding)) if self.document.text(binder) == name]
        except _UnsupportedPattern as error:
            return self._unknown(name, str(error), reader_version=VALUE_READER_VERSION)
        if len(matches) != 1:
            return self._unknown(name, "duplicate_or_unidentified_pattern_binder", state="ambiguous")
        binder, pattern_path = matches[0]
        kind = binding["kind"]
        if kind == "mutable":
            kind = next((child.type for child in declaration.parent.children if child.type in {"var", "let"}), "mutable")
        elif kind == "parameter" and scope.type == "catch_clause":
            kind = "catch_parameter"
        elif kind in {"declaration", "opaque_declaration"}:
            kind = {"function_declaration": "function", "generator_function_declaration": "function",
                "class_declaration": "class", "enum_declaration": "enum", "internal_module": "namespace"}.get(declaration.type, declaration.type)
        import_record = None
        if kind == "import":
            statement = next((item for item in _ancestors(declaration) if item.type == "import_statement"), None)
            source = statement.child_by_field_name("source") if statement else None
            type_only = any(child.type == "type" for child in declaration.children) or bool(statement and any(child.type == "type" for child in statement.children))
            if type_only:
                return self._unknown(name, "type_only_import_is_not_runtime_binding")
            from .static_contracts import _literal_string
            import_record = {"module": _literal_string(self.document.text(source)) if source else None,
                "imported_name": "*" if declaration.type == "namespace_import" else self.document.text(declaration.child_by_field_name("name")) if declaration.type == "import_specifier" else "default",
                "type_only": False, "provider_resolved": False}
        parameter_index = next((item["index"] for item in pattern_path if item["kind"] == "parameter"), 0 if kind in {"parameter", "catch_parameter"} else None)
        identity = {"file": self.document.source.path, "source_hash": self.document.source.hash,
            "declaration_span": {"node_type": declaration.type, "start_byte": declaration.start_byte, "end_byte": declaration.end_byte},
            "binder_span": {"node_type": binder.type, "start_byte": binder.start_byte, "end_byte": binder.end_byte},
            "scope_span": {"node_type": scope.type, "start_byte": scope.start_byte, "end_byte": scope.end_byte}}
        declaration_id = _digest({"version": VERSION, **identity})
        value_reasons = [] if binding.get("known") else [reason or "reaching_value_not_modeled"]
        if _inside(declaration, identifier_node) and declaration.type == "variable_declarator":
            value_reasons.append("declaration_initializer_or_binder_is_not_initialized_value")
        if binding.get("destructured") or any(item["kind"] in {"array_index", "object_property"} for item in pattern_path):
            value_reasons.append("destructuring_value_not_modeled")
        if any(item["kind"] == "default_value" for item in pattern_path):
            value_reasons.append("default_value_expression_not_modeled")
        if any(item["kind"] in {"object_rest", "array_rest"} for item in pattern_path):
            value_reasons.append("rest_values_and_excluded_keys_not_modeled")
        result = {"version": VERSION, "reader_version": VALUE_READER_VERSION,
            "state": "unique", "identity_complete": True, "name": name,
            "declaration_id": declaration_id, "binding_id": declaration_id,
            "declaration_kind": kind, **identity,
            "declaration_location": self.document.location(declaration), "binder_location": self.document.location(binder),
            "scope_location": self.document.location(scope), "parameter_index": parameter_index,
            "pattern_path": pattern_path, "import": import_record,
            "value": {"stable": not value_reasons, "runtime_value_known": False, "reasons": value_reasons},
            "gaps": [], "snapshot_id": getattr(self.document, "snapshot_id", ""),
            "limitations": ["identity denotes a captured lexical declaration, not an object/resource or alias identity",
                "no reaching values, target activation, hidden calls or external heap mutation are proved",
                "write records include captured syntax and possible effects, not executed writes"]}
        self._declarations[declaration_id] = {"declaration": declaration, "binder": binder,
            "initializer": binding.get("initializer"), "scope": scope, "record": result}
        self._cache[identifier_node.id] = result
        return deepcopy(result)

    def resolve(self, identifier_node: Any) -> dict:
        result = self._resolve_identity(identifier_node)
        if result.get("state") == "unique":
            review = self.writes(result)
            result["captured_write_review_count"] = len(review)
            if review:
                result["value"]["stable"] = False
                reasons = result["value"]["reasons"]
                if "captured_write_or_possible_effect" not in reasons:
                    reasons.append("captured_write_or_possible_effect")
            result["value"]["model"] = "captured_lexical_origin_only"
            result["value"]["heap_state_verified"] = False
        return result

    def unbound(self, name: str, at_node: Any) -> dict:
        """Prove only absence of a captured local declaration, never a builtin.

        In particular an expression token of CST type ``undefined`` is not
        evidence for the standard singleton when a local binding can shadow it.
        """
        result = {"version": VERSION, "name": name, "state": "unknown", "unbound": False,
            "local_declaration_absent": False, "runtime_builtin_verified": False, "gaps": []}
        if (not isinstance(name, str) or not name.replace("$", "_").isidentifier()
                or "\\" in name or at_node is None or not self.document.contains(at_node)
                or self.document.kind == "rust"):
            result["gaps"] = ["unsupported_lexical_absence_query"]
            return result
        result["location"] = self.document.location(at_node)
        ancestors = {_key(item) for item in _ancestors(at_node)}
        evals = [node for node in self._evals if _function(node) == _function(at_node)
            or (_function(node) is not None and _key(_function(node)) in ancestors)]
        if evals:
            result.update(gaps=["eval_scope_not_closed"], eval_locations=[self.document.location(node) for node in evals])
            return result
        binding = self.reader.binding(name, at_node)
        reason = binding.get("reason", "")
        if binding.get("node") is not None:
            result.update(state="bound", declaration_location=self.document.location(binding["node"]))
            return result
        if reason != "unresolved_lexical_binding":
            result.update(state="ambiguous" if reason == "duplicate_or_shadow_binding" else "unknown",
                gaps=[reason or "lexical_absence_not_closed"])
            return result
        # Fail closed if an unsupported visible binding pattern contains this
        # spelling. It could be a binder the compatibility reader did not model.
        for node in self.all_nodes:
            pattern, scope = None, None
            if node.type == "variable_declarator":
                pattern = node.child_by_field_name("name")
                scope = _binding_scope(node, node.parent is not None and node.parent.type == "variable_declaration")
            elif node.type in _FUNCTIONS | {"catch_clause"} and _key(node) in ancestors:
                pattern = node.child_by_field_name("parameters") or node.child_by_field_name("parameter")
                scope = node
            elif node.type == "for_in_statement":
                keyword = next((child.type for child in node.children if child.type in {"var", "let", "const"}), "")
                if keyword:
                    pattern = node.child_by_field_name("left")
                    scope = _binding_scope(node, True) if keyword == "var" else node
            if pattern is not None and scope is not None and _key(scope) in ancestors and any(
                    self.document.text(child) == name for child in walk(pattern)):
                result.update(gaps=["possible_unmodeled_binder"], possible_binding_location=self.document.location(pattern))
                return result
        result.update(state="unbound", unbound=True, local_declaration_absent=True)
        result["limitations"] = ["no captured local binding is not proof of a standard runtime value",
            "global/member/alias effects and external mutation need separate effect guards"]
        return result

    def same(self, a: Any, b: Any) -> bool:
        first = a if isinstance(a, dict) else self.resolve(a)
        second = b if isinstance(b, dict) else self.resolve(b)
        return bool(first.get("state") == second.get("state") == "unique"
            and first.get("identity_complete") and second.get("identity_complete")
            and first.get("declaration_id") and first.get("declaration_id") == second.get("declaration_id"))

    def _identity(self, value: Any) -> str | None:
        if isinstance(value, str):
            return value if value in self._declarations else None
        if isinstance(value, dict) and value.get("state") == "unique" and value.get("identity_complete"):
            identity = value.get("declaration_id")
            return identity if identity in self._declarations else None
        return None

    def declaration_for(self, identity: Any) -> Any | None:
        key = self._identity(identity)
        return self._declarations[key]["declaration"] if key else None

    def initializer_for(self, identity: Any) -> Any | None:
        key = self._identity(identity)
        return self._declarations[key]["initializer"] if key else None

    def _roots(self, node: Any) -> list[tuple[Any, bool, bool]]:
        node = unwrap(node)
        if node is None:
            return []
        if node.type in _IDENTIFIERS:
            return [(node, False, True)]
        if node.type in {"member_expression", "subscript_expression"}:
            roots = self._roots(node.child_by_field_name("object"))
            return [(root, True, complete) for root, _, complete in roots]
        try:
            return [(binder, False, True) for binder, _ in self._binders(node)]
        except _UnsupportedPattern:
            # Some leaves may be default-expression reads. Preserve them as
            # possible effects, never as confirmed mutation targets.
            return [(child, False, False) for child in walk(node) if child.type in _IDENTIFIERS]

    def _alias_index(self) -> dict[str, list[dict]]:
        if self._aliases is not None:
            return self._aliases
        aliases: dict[str, list[dict]] = {}
        for node in self.all_nodes:
            if node.type not in {"variable_declarator", "assignment_expression"}:
                continue
            binder = node.child_by_field_name("name") if node.type == "variable_declarator" else node.child_by_field_name("left")
            value = unwrap(node.child_by_field_name("value") if node.type == "variable_declarator" else node.child_by_field_name("right"))
            if binder is None or binder.type != "identifier" or value is None or value.type != "identifier":
                continue
            origin, alias = self._resolve_identity(value), self._resolve_identity(binder)
            if origin["state"] == alias["state"] == "unique" and origin["declaration_id"] != alias["declaration_id"]:
                aliases.setdefault(origin["declaration_id"], []).append({"alias_declaration_id": alias["declaration_id"],
                    "initializer_location": self.document.location(value), "runtime_alias_verified": False})
            elif origin["state"] == "unique" and alias["state"] != "unique":
                self._alias_gaps.setdefault(origin["declaration_id"], []).append({
                    "kind": "unresolved_alias_boundary", "identity_match_known": False, "possible_effect": True,
                    "source_location": self.document.location(node), "location": self.document.location(node),
                    "reason": "a captured identifier copy has an unresolved alias declaration",
                    "alias_state": alias["state"], "alias_gaps": alias.get("gaps", []),
                    "runtime_execution_verified": False, "binding_reassignment": False})
        self._aliases = aliases
        return aliases

    def writes(self, identity: Any) -> list[dict]:
        """Review all supported captured writes and possible simple-alias effects.

        An empty result does not close complex aliases, callback activation,
        external mutation or arbitrary call effects. Consumers need their own
        escape/effect model before claiming heap or resource stability.
        """
        target_id = self._identity(identity)
        if target_id is None:
            return [{"kind": "unknown_identity", "identity_match_known": False, "reason": "no_unique_captured_declaration"}]
        if target_id in self._writes_cache:
            return deepcopy(self._writes_cache[target_id])
        declaration = self._declarations[target_id]
        aliases = self._alias_index()
        possible = {target_id}
        pending = [target_id]
        while pending:
            current = pending.pop()
            for alias in aliases.get(current, []):
                alias_id = alias["alias_declaration_id"]
                if alias_id not in possible:
                    possible.add(alias_id)
                    pending.append(alias_id)
        results = [dict(gap, id=_digest({"version": VERSION, "declaration_id": target_id,
            "alias_gap": gap}), declaration_id=target_id,
            root_location=gap["source_location"], member_write=False, mutation_target_complete=False)
            for possible_id in sorted(possible) for gap in self._alias_gaps.get(possible_id, [])]
        for mutation in self.all_nodes:
            if mutation.type not in {"assignment_expression", "augmented_assignment_expression", "update_expression", "for_in_statement", "unary_expression"}:
                continue
            if mutation.type == "for_in_statement" and any(child.type in {"const", "let", "var", "lexical_declaration", "variable_declaration"} for child in mutation.children):
                continue
            if mutation.type == "unary_expression":
                operator = mutation.child_by_field_name("operator")
                if operator is None or self.document.text(operator) != "delete":
                    continue
            left = mutation.child_by_field_name("left") or mutation.child_by_field_name("argument")
            for root, member, target_complete in self._roots(left):
                binding = self._resolve_identity(root)
                root_id = binding.get("declaration_id")
                alias_effect = bool(target_complete and member and root_id in possible and root_id != target_id)
                direct = target_complete and root_id == target_id and binding.get("state") == "unique"
                unsupported_target = not target_complete and root_id in possible
                uncertain = bool(binding.get("state") != "unique" and (
                    self.document.text(root) == declaration["record"]["name"] or "\\" in self.document.text(root))
                    and any(_key(item) == _key(declaration["scope"]) for item in _ancestors(root)))
                if not (direct or alias_effect or uncertain or unsupported_target):
                    continue
                location = self.document.location(mutation)
                write_id = _digest({"version": VERSION, "declaration_id": target_id,
                    "mutation": _key(mutation), "root": _key(root)})
                self._mutation_nodes[write_id] = mutation
                results.append({"id": write_id, "kind": "unsupported_target_possible_write" if unsupported_target else "possible_alias_member_write" if alias_effect else "unresolved_possible_write" if uncertain else "member_write" if member else mutation.type,
                    "declaration_id": target_id, "root_declaration_id": root_id,
                    "identity_match_known": direct, "possible_effect": alias_effect or uncertain or unsupported_target,
                    "mutation_target_complete": target_complete,
                    "source_location": location, "location": location,
                    "root_location": self.document.location(root),
                    "closure": _function(root) != _function(declaration["binder"]),
                    "member_write": member, "binding_reassignment": direct and not member,
                    "runtime_execution_verified": False})
        results.sort(key=lambda item: (item["source_location"]["start_byte"], item["root_location"]["start_byte"], item["id"]))
        self._writes_cache[target_id] = results
        return deepcopy(results)

    def mutation_for(self, write: Any) -> Any | None:
        key = write if isinstance(write, str) else write.get("id") if isinstance(write, dict) else None
        return self._mutation_nodes.get(key)
