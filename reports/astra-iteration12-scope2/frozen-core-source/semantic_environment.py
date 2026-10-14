"""Finite captured-source guards for explicitly assumed standard host APIs.

An accepted audit enables a registered static model. It never authenticates
the running host, excludes opaque cross-document effects, or creates CALLS.
Known syntax blockers and the residual host premise are reported separately.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any

from .lexical_bindings import LexicalBindings, VERSION as LEXICAL_VERSION
from .semantic_sources import VERSION as SOURCE_VERSION, walk, unwrap
from .static_contracts import _literal_string

VERSION = "captured-builtin-environment-1"
PROFILE_VERSION = "standard-host-syntax-environment-v1"
_NODE_BUDGET = 100_000
_BARRIER_SAMPLES = 32
_ALIAS_ROUND_BUDGET = 64
_HOST_ROOTS = {"globalThis", "window", "self", "global"}
_IDENTIFIERS = {"identifier", "shorthand_property_identifier", "shorthand_property_identifier_pattern", "undefined"}
_FUNCTIONS = {"function_declaration", "generator_function_declaration", "function_expression",
    "generator_function", "arrow_function", "method_definition"}
_TYPE_CONTEXTS = {"type_annotation", "type_alias_declaration", "interface_declaration", "type_query",
    "type_arguments", "type_parameters", "implements_clause", "import_type", "function_type"}
_PROFILES = {
    "Object": {"id": "object-standard-interface-1", "constructor": False,
        # Occurrence registration does not interpret receivers or source
        # objects, prove purity, or authorize a field-copy semantic contract.
        "members": {"assign", "freeze", "keys", "values", "entries", "fromEntries", "hasOwn", "is", "getPrototypeOf", "getOwnPropertyNames", "getOwnPropertySymbols"},
        "prototype_members": {"hasOwnProperty", "toString", "toLocaleString", "valueOf", "isPrototypeOf", "propertyIsEnumerable"},
        "requested_members": {"freeze", "prototype"}},
    "Promise": {"id": "promise-standard-interface-1", "constructor": True,
        "members": {"all", "allSettled", "any", "race", "resolve", "reject"},
        "prototype_members": set(), "requested_members": {"all"}},
    "Set": {"id": "set-standard-constructor-1", "constructor": True,
        "members": set(), "prototype_members": set(), "requested_members": set()},
    "URLSearchParams": {"id": "url-search-params-standard-constructor-1", "constructor": True,
        "members": set(), "prototype_members": set(), "requested_members": set()},
    "String": {"id": "string-standard-interface-1", "constructor": True,
        "members": {"fromCharCode", "fromCodePoint", "raw"}, "prototype_members": {"indexOf", "slice"},
        "requested_members": {"indexOf", "slice"}},
    "encodeURIComponent": {"id": "encode-uri-component-standard-function-1", "constructor": False,
        "members": set(), "prototype_members": set(), "requested_members": set()},
    "undefined": {"id": "undefined-standard-value-1", "constructor": False,
        "members": set(), "prototype_members": set(), "requested_members": set()},
}


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True,
        separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()


def _field(node: Any, name: str) -> Any:
    return node.child_by_field_name(name) if node is not None else None


def _ancestors(node: Any):
    while node is not None:
        yield node
        node = node.parent


def _erased(node: Any) -> bool:
    return any(parent.type in _TYPE_CONTEXTS or parent.type.endswith("_type") for parent in _ancestors(node))


class BuiltinEnvironment:
    """Audit one authenticated document, with a fixed finite usage registry.

    The registry's read/call shapes are model premises, not inferred callee
    purity. Consumers must separately enable their semantic models and retain
    their object, callback, default-expression and escape guards.
    """

    def __init__(self, document: Any):
        self.document = document
        self.lexical = LexicalBindings(document)
        self.nodes = []
        self.budget_exceeded = False
        for node in walk(document.tree.root_node):
            if len(self.nodes) == _NODE_BUDGET:
                self.budget_exceeded = True
                break
            self.nodes.append(node)
        self._cache: dict[tuple, dict] = {}
        self._identities: dict[int, dict] = {}
        self._host_alias_cache: tuple[dict[str, dict], set[int], bool] | None = None

    def _access(self, node: Any) -> tuple[Any, list[Any]]:
        node, parts = unwrap(node), []
        while node is not None and node.type in {"member_expression", "subscript_expression"}:
            key_node = _field(node, "property") if node.type == "member_expression" else _field(node, "index")
            key = None
            if key_node is not None:
                if node.type == "member_expression" and key_node.type in {"property_identifier", "identifier"} and "\\" not in self.document.text(key_node):
                    key = self.document.text(key_node)
                elif key_node.type == "string":
                    key = _literal_string(self.document.text(key_node))
            parts.insert(0, key)
            node = unwrap(_field(node, "object"))
        return node, parts

    def _pattern_targets(self, node: Any) -> list[Any]:
        node = unwrap(node)
        if node is None:
            return []
        if node.type in _IDENTIFIERS or node.type in {"member_expression", "subscript_expression"}:
            return [node]
        if node.type in {"assignment_pattern", "object_assignment_pattern"}:
            return self._pattern_targets(_field(node, "left"))
        if node.type == "pair_pattern":
            return self._pattern_targets(_field(node, "value"))
        if node.type in {"array_pattern", "object_pattern", "rest_pattern", "parenthesized_expression"}:
            return [target for child in node.named_children for target in self._pattern_targets(child)]
        return [node]

    def _binder(self, node: Any) -> bool:
        parent = node.parent
        while parent is not None and parent.type in {"array_pattern", "object_pattern", "pair_pattern", "rest_pattern",
                "assignment_pattern", "object_assignment_pattern", "required_parameter", "optional_parameter", "formal_parameters"}:
            if parent.type in {"assignment_pattern", "object_assignment_pattern"} and _field(parent, "left") is not node:
                return False
            if parent.type in {"required_parameter", "optional_parameter"} and _field(parent, "value") == node:
                return False
            node, parent = parent, parent.parent
        if parent is None:
            return False
        if parent.type == "variable_declarator":
            return _field(parent, "name") == node
        if parent.type in _FUNCTIONS or parent.type in {"class", "class_expression", "class_declaration", "internal_module", "enum_declaration", "import_specifier", "namespace_import", "import_clause"}:
            return node == _field(parent, "name") or node == _field(parent, "alias") or node == _field(parent, "parameters") or node == _field(parent, "parameter") or parent.type == "import_clause"
        if parent.type == "catch_clause":
            return _field(parent, "parameter") == node
        if parent.type == "for_in_statement":
            return any(child.type in {"var", "let", "const"} for child in parent.children) and _field(parent, "left") == node
        return False

    def _outer_access(self, node: Any) -> Any:
        current = node
        while current.parent is not None:
            parent = current.parent
            if parent.type in {"parenthesized_expression", "as_expression", "satisfies_expression", "non_null_expression", "type_assertion"} and unwrap(parent) == unwrap(current):
                current = parent
            elif parent.type in {"member_expression", "subscript_expression"} and _field(parent, "object") == current:
                current = parent
            else:
                break
        return current

    def _identity(self, node: Any) -> dict:
        if node is None or node.type not in _IDENTIFIERS:
            return {}
        if node.id not in self._identities:
            self._identities[node.id] = self.lexical.resolve(node)
        return self._identities[node.id]

    def _host_aliases(self) -> tuple[dict[str, dict], set[int], bool]:
        """Track possible host origins by declaration, never equal values.

        Only a simple lexical destination and finite transparent/conditional
        expression are modeled. Unknown alternate operands stay unknown. A
        recorded origin lets the audit find later visible member writes; it
        does not authenticate that destination's actual receiver at a query.
        """
        if self._host_alias_cache is not None:
            return self._host_alias_cache
        aliases: dict[str, dict] = {}
        permitted_origins: set[int] = set()
        contexts = []
        for node in self.nodes:
            if _erased(node):
                continue
            if node.type == "variable_declarator":
                target, value = _field(node, "name"), _field(node, "value")
            elif node.type == "assignment_expression":
                target, value = _field(node, "left"), _field(node, "right")
            else:
                continue
            if target is not None and target.type == "identifier" and value is not None:
                contexts.append((node, target, value))

        def origins(node: Any) -> tuple[list[Any], bool]:
            node = unwrap(node)
            if node is None:
                return [], True
            if node.type in {"identifier", "member_expression", "subscript_expression"}:
                root, parts = self._access(node)
                if root is None or root.type != "identifier":
                    return [], True
                if self.document.text(root) in _HOST_ROOTS and all(part in _HOST_ROOTS for part in parts):
                    return [node], False
                if parts or self.document.text(root) not in {record["name"] for record in aliases.values()}:
                    return [], True
                identity = self._identity(root)
                if not parts and identity.get("identity_complete") and identity.get("binding_id") in aliases:
                    return [node], True
                return [], True
            if node.type == "binary_expression" and self.document.text(_field(node, "operator")) in {"??", "||"}:
                left, left_unknown = origins(_field(node, "left"))
                right, right_unknown = origins(_field(node, "right"))
                return [*left, *right], left_unknown or right_unknown
            if node.type == "ternary_expression":
                left, left_unknown = origins(_field(node, "consequence"))
                right, right_unknown = origins(_field(node, "alternative"))
                return [*left, *right], left_unknown or right_unknown
            return [], True

        complete = False
        for _round in range(_ALIAS_ROUND_BUDGET):
            changed = False
            for context, target, value in contexts:
                leaves, alternatives_unknown = origins(value)
                if not leaves:
                    continue
                identity = self._identity(target)
                if not identity.get("identity_complete"):
                    continue
                binding_id = identity["binding_id"]
                if binding_id not in aliases:
                    aliases[binding_id] = {"binding_id": binding_id, "name": identity["name"], "declaration_kind": identity["declaration_kind"],
                        "declaration_location": identity["declaration_location"], "scope_span": identity["scope_span"],
                        "may_alias_standard_host_root": True, "runtime_receiver_verified": False,
                        "value_stability_verified": False, "origins": []}
                    changed = True
                origin_record = {"storage_location": self.document.location(context),
                    "expression_location": self.document.location(value),
                    "alternative_receiver_not_certified": alternatives_unknown,
                    "source_locations": [self.document.location(leaf) for leaf in leaves]}
                if origin_record not in aliases[binding_id]["origins"]:
                    aliases[binding_id]["origins"].append(origin_record)
                for leaf in leaves:
                    # Transparent wrappers retain the same captured value
                    # origin and coordinates; no container or return path is
                    # implicitly admitted as another alias.
                    permitted_origins.add(self._outer_access(leaf).id)
            if not changed:
                complete = True
                break
        self._host_alias_cache = aliases, permitted_origins, complete
        return self._host_alias_cache

    def _host_transport(self, expression: Any) -> bool:
        """Allow only a host value contained in an actual call argument.

        A conditional/assignment/storage path is an alias barrier. Ordinary
        literal containers passed directly to a call remain opaque transport;
        this does not certify the callee or any resulting runtime effects.
        """
        current = expression
        while current.parent is not None:
            parent = current.parent
            if parent.type in {"parenthesized_expression", "as_expression", "satisfies_expression", "non_null_expression", "type_assertion"}:
                current = parent
                continue
            if parent.type == "pair" and _field(parent, "value") == current:
                current = parent
                continue
            if parent.type in {"object", "array"}:
                current = parent
                continue
            if parent.type == "arguments" and parent.parent is not None and parent.parent.type in {"call_expression", "new_expression"}:
                return True
            return False
        return False

    def audit(self, name: str, at: Any, member: str | None = None) -> dict:
        doc = self.document
        member = member or None
        key = (getattr(doc, "parse_id", ""), name, member, getattr(at, "id", None))
        if key in self._cache:
            return deepcopy(self._cache[key])
        profile = _PROFILES.get(name)
        valid_at = at is not None and doc.contains(at)
        source_ready = (doc.kind in {"typescript", "tsx"} and doc.source.status == "parsed"
            and not doc.tree.root_node.has_error and bool(getattr(doc, "parse_id", ""))
            and doc.parse_provenance.get("literal_authority") == "original_saved_source_text_only")
        blockers: list[dict] = []
        blocker_keys: set[tuple] = set()
        opaque: list[dict] = []
        opaque_keys: set[tuple] = set()

        def evidence(code: str, node: Any, **details: Any) -> dict:
            return {"code": code, "location": doc.location(node) if node is not None and doc.contains(node) else None, **details}

        def block(code: str, node: Any = None, **details: Any) -> None:
            identity = (code, getattr(node, "start_byte", None), getattr(node, "end_byte", None))
            if identity not in blocker_keys:
                blocker_keys.add(identity)
                blockers.append(evidence(code, node, **details))

        def unknown_effect(code: str, node: Any, **details: Any) -> None:
            identity = (code, node.start_byte, node.end_byte)
            if identity not in opaque_keys:
                opaque_keys.add(identity)
                opaque.append(evidence(code, node, **details))

        if not valid_at or not source_ready:
            block("source_or_query_not_authenticated", at if valid_at else None)
        if profile is None or member is not None and member not in profile["requested_members"]:
            block("standard_interface_profile_not_registered", at if valid_at else None)
        if self.budget_exceeded:
            block("environment_node_budget_exceeded", None, node_budget=_NODE_BUDGET)
        absence = self.lexical.unbound(name, at) if valid_at and source_ready and isinstance(name, str) else {
            "state": "unknown", "local_declaration_absent": False, "runtime_builtin_verified": False}
        if absence.get("state") != "unbound" or not absence.get("local_declaration_absent"):
            block("local_standard_name_not_absent", at if valid_at else None, lexical_absence=absence)

        aliases, permitted_origins, alias_complete = ({}, set(), False)
        if source_ready and valid_at and profile is not None and not self.budget_exceeded:
            aliases, permitted_origins, alias_complete = self._host_aliases()
            if not alias_complete:
                block("host_alias_propagation_budget_exceeded", None, round_budget=_ALIAS_ROUND_BUDGET)

        def alias_identity(root: Any) -> dict | None:
            if root is None or root.type != "identifier":
                return None
            if doc.text(root) not in {record["name"] for record in aliases.values()}:
                return None
            identity = self._identity(root)
            return aliases.get(identity.get("binding_id")) if identity.get("identity_complete") else None

        def root_kind(node: Any) -> tuple[str | None, list[Any]]:
            root, parts = self._access(node)
            text = doc.text(root) if root is not None else ""
            if text == name:
                return "api", parts
            if text in _HOST_ROOTS or alias_identity(root) is not None:
                host_parts = list(parts)
                while host_parts and host_parts[0] in _HOST_ROOTS:
                    host_parts.pop(0)
                if not host_parts:
                    return "host_root", host_parts
                if host_parts[0] is None:
                    return "computed_host", host_parts
                if host_parts[0] == name:
                    return "api", host_parts[1:]
                if name in host_parts:
                    return "computed_host", host_parts
            return None, parts

        if source_ready and valid_at and profile is not None and not self.budget_exceeded:
            query_expression = (_field(at, "function") if at.type == "call_expression" else
                _field(at, "constructor") if at.type == "new_expression" else at)
            query_root, _ = self._access(query_expression)
            query_kind, _ = root_kind(query_expression)
            if query_kind in {"api", "computed_host"} and alias_identity(query_root) is not None:
                block("query_provider_only_possible_host_alias", query_expression,
                    alias_binding_id=alias_identity(query_root)["binding_id"])
            for node in self.nodes:
                if _erased(node):
                    continue
                if node.type == "with_statement":
                    block("with_scope_not_closed", node)
                if node.type in {"identifier", "property_identifier", "shorthand_property_identifier", "shorthand_property_identifier_pattern"} and "\\" in doc.text(node):
                    block("escaped_identifier_or_member_not_decoded", node)
                if node.type in {"identifier", "shorthand_property_identifier"} and doc.text(node) == "eval" and not self._binder(node):
                    block("eval_value_or_scope_effect_unknown", node)
                if node.type == "call_expression":
                    function = _field(node, "function")
                    root, parts = self._access(function)
                    if doc.text(root) == "eval" or parts[-1:] == ["eval"]:
                        block("eval_call_or_scope_effect_unknown", node)
                    # A prototype-changing operation cannot be ignored because
                    # its syntactic receiver has a different builtin spelling.
                    if parts[-1:] in (["setPrototypeOf"], ["__defineGetter__"], ["__defineSetter__"]):
                        block("prototype_mutator_call", node)
                mutation = node.type in {"assignment_expression", "augmented_assignment_expression", "update_expression", "for_in_statement"}
                deleting = node.type == "unary_expression" and doc.text(_field(node, "operator")) == "delete"
                if mutation or deleting:
                    if node.type == "for_in_statement" and any(child.type in {"var", "let", "const", "lexical_declaration", "variable_declaration"} for child in node.children):
                        continue
                    left = _field(node, "left") or _field(node, "argument")
                    for target in self._pattern_targets(left):
                        kind, parts = root_kind(target)
                        target_root, _ = self._access(target)
                        if kind in {"api", "computed_host"}:
                            block("standard_api_explicit_delete" if deleting else "standard_api_explicit_write", node,
                                access_parts=parts, mutation_target_location=doc.location(target))
                        if kind == "host_root" and (parts or alias_identity(target_root) is None):
                            block("host_root_explicit_delete" if deleting else "host_root_explicit_write", node,
                                mutation_target_location=doc.location(target))
                        if any(part in {"prototype", "__proto__"} for part in parts):
                            block("captured_prototype_write", node, access_parts=parts)
                        if target.type not in _IDENTIFIERS | {"member_expression", "subscript_expression"}:
                            block("unsupported_mutation_target", node, mutation_target_type=target.type)
                # Identify actual API or host-root values before permitting
                # registered static member calls. Alias/escape is a blocker;
                # bare host transport is an explicit residual host premise.
                if node.type in _IDENTIFIERS and (doc.text(node) in {name, *_HOST_ROOTS} or alias_identity(node) is not None) and not self._binder(node):
                    if node.parent is not None and node.parent.type in {"member_expression", "subscript_expression"} and _field(node.parent, "object") != node:
                        continue
                    expression = self._outer_access(node)
                    kind, parts = root_kind(expression)
                    if kind is None:
                        continue
                    parent = expression.parent
                    direct_call = parent is not None and parent.type == "call_expression" and _field(parent, "function") == expression
                    constructor = parent is not None and parent.type == "new_expression" and _field(parent, "constructor") == expression
                    if kind == "host_root":
                        root, _ = self._access(expression)
                        alias = alias_identity(root)
                        local_assignment = (alias is not None and parent is not None
                            and parent.type in {"assignment_expression", "augmented_assignment_expression", "for_in_statement"}
                            and _field(parent, "left") == expression)
                        if expression.id in permitted_origins:
                            unknown_effect("finite_possible_host_alias_origin", expression,
                                runtime_receiver_verified=False, standard_host_environment_required=True)
                        elif local_assignment:
                            unknown_effect("possible_host_alias_local_rebinding", expression,
                                alias_binding_id=alias["binding_id"], value_stability_verified=False)
                        elif not self._host_transport(expression):
                            block("host_root_alias_or_escape", expression)
                        else:
                            unknown_effect("opaque_host_root_transport", expression,
                                effect_verified=False, standard_host_environment_required=True)
                        continue
                    if kind == "computed_host":
                        block("computed_host_api_access", expression, access_parts=parts)
                        continue
                    root, _ = self._access(expression)
                    if doc.text(root) in _HOST_ROOTS:
                        host_absence = self.lexical.unbound(doc.text(root), root)
                        if not host_absence.get("local_declaration_absent"):
                            block("host_api_root_binding_not_absent", expression, lexical_absence=host_absence)
                    if any(part is None for part in parts):
                        block("computed_standard_api_member", expression, access_parts=parts)
                        continue
                    if any(part in {"prototype", "__proto__"} for part in parts):
                        allowed = parts[:1] == ["prototype"] and len(parts) >= 2 and parts[1] in profile["prototype_members"] and parts[2:] in ([], ["call"]) and direct_call
                        if not allowed:
                            block("standard_prototype_access_or_escape", expression, access_parts=parts)
                        continue
                    if parts:
                        if len(parts) != 1 or parts[0] not in profile["members"]:
                            block("standard_same_root_member_outside_profile", expression, access_parts=parts)
                        elif not direct_call:
                            block("standard_api_member_alias_or_escape", expression, access_parts=parts)
                    elif constructor and profile["constructor"]:
                        pass
                    elif direct_call and name in {"String", "encodeURIComponent"}:
                        pass
                    elif name == "undefined" and not direct_call and not constructor:
                        # The primitive may be returned, stored or passed as a
                        # value. Explicit writes/member access and local
                        # shadowing are still audited; it is not an API object.
                        pass
                    else:
                        block("standard_api_value_alias_or_escape", expression)

        scope = next((node for node in _ancestors(at) if node.type in _FUNCTIONS | {"program", "statement_block", "catch_clause", "for_statement", "for_in_statement"}), None) if valid_at else None
        scope_identity = {"file": doc.source.path, "source_hash": doc.source.hash,
            "scope_span": {"node_type": scope.type, "start_byte": scope.start_byte, "end_byte": scope.end_byte} if scope else None}
        scope_identity["id"] = _digest(scope_identity)
        supported = not blockers
        result = {"version": VERSION, "state": "supported_in_registered_model" if supported else "unknown", "supported": supported,
            "name": name, "member": member,
            "source": {"file": doc.source.path, "source_hash": doc.source.hash, "snapshot_id": getattr(doc, "snapshot_id", ""),
                "semantic_parse_id": getattr(doc, "parse_id", ""), "semantic_source_version": SOURCE_VERSION,
                "parser_version": doc.parser_version, "at_location": doc.location(at) if valid_at else None,
                "audit_scope": "authenticated_document", "scan_complete": source_ready and not self.budget_exceeded,
                "node_budget": _NODE_BUDGET, "nodes_reviewed": len(self.nodes), "budget_exceeded": self.budget_exceeded,
                "decision_computed_before_sampling": True},
            "scope_identity": scope_identity, "lexical_absence": absence,
            "model": {"registry_version": PROFILE_VERSION, "profile_id": profile["id"] if profile else None,
                "standard_host_environment": "assumption", "runtime_builtin_verified": False,
                "provider_or_external_mutation_verified": False,
                "member_registration_semantics": "fixed syntax interface occurrence only; argument and receiver effects require separate consumer guards",
                "member_argument_effects_verified": False, "member_call_purity_verified": False,
                "allowed_static_member_interfaces": sorted(profile["members"]) if profile else [],
                "allowed_prototype_member_interfaces": sorted(profile["prototype_members"]) if profile else [],
                "assumptions": ["the explicitly registered host interfaces retain their standard behavior",
                    "opaque calls, host transport and other captured documents do not replace the modeled standard interfaces",
                    "captured alias/prototype/write barriers may not be overridden by this premise"]},
            "policy": {"role_configuration_consulted": False, "consumer_registration_required": True,
                "semantic_contract_registration_verified": False, "invocation": "explicit_fixed_interface_audit"},
            "unresolved": {"barrier_count": len(blockers), "reason_codes": sorted({item["code"] for item in blockers}),
                "samples": blockers[:_BARRIER_SAMPLES], "truncated": len(blockers) > _BARRIER_SAMPLES},
            "opaque_effects": {"count": len(opaque), "samples": opaque[:_BARRIER_SAMPLES],
                "truncated": len(opaque) > _BARRIER_SAMPLES, "effects_verified": False,
                "outside_document_effects_verified": False, "fixed_standard_host_premise_required": True},
            "host_aliases": {"model": "finite-captured-may-host-alias-1", "count": len(aliases),
                "propagation_complete_within_model": alias_complete, "round_budget": _ALIAS_ROUND_BUDGET,
                "samples": list(aliases.values())[:_BARRIER_SAMPLES], "truncated": len(aliases) > _BARRIER_SAMPLES,
                "runtime_receiver_verified": False, "same_runtime_object_verified": False,
                "supported_storage": "unique simple lexical destination; transparent/??/||/conditional possible origins",
                "unsupported_container_storage_is_barrier": True},
            "locations": [item["location"] for item in blockers[:_BARRIER_SAMPLES] if item["location"] is not None],
            "lexical_model_version": LEXICAL_VERSION}
        self._cache[key] = result
        return deepcopy(result)
