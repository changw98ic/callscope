"""Finite status production, predicate and rejecting-consumer source relations.

Selectors locate source roles. Handler keys, fields, collection membership,
projection calls, actual arguments and rejection branches are read from saved
AST and authenticated CALLS edges. No target module or function is executed.
The conclusion concerns a current ordinary projected record at selected normal
source guards; it neither grants recovery policy nor predicts runtime success.
"""
from __future__ import annotations

from collections import Counter
from pathlib import PurePosixPath
from typing import Any

from .completion_summaries import function_kind
from .lexical_bindings import LexicalBindings
from .models import Evidence, Finding, GraphSnapshot
from .semantic_environment import BuiltinEnvironment
from .semantic_sources import SemanticSources, unwrap
from .static_contracts import _digest, _literal_string, _path, _string
from .value_analysis import _json_data

VERSION = "finite-status-classification-1"
POLICY_VERSION = "static-status-policy-v1"
MODEL_ID = "ordinary-record-status-predicate-normal-projection-v1"
_FUNCTIONS = {"function_declaration", "function_expression", "arrow_function", "method_definition",
    "generator_function", "generator_function_declaration"}
_TYPE_ONLY = {"comment", "type_annotation", "type_arguments", "type_parameters", "interface_declaration",
    "type_alias_declaration", "type_query", "import_type", "implements_clause", "function_type"}
_UNKNOWN = object()
_NODE_LIMIT, _DEPTH = 131072, 12
_ROLES = {"producer", "predicate", "consumer", "authority", "recoverability"}


def validate_status_rule(rule: Any) -> None:
    _json_data(rule)
    required = {"id", "type", "severity", *_ROLES, "invariant", "models", "provenance", "applicability"}
    if not isinstance(rule, dict) or set(rule) != required or not _string(rule["id"]) or rule["type"] != "status_classification_flow":
        raise ValueError("status rule requires exact source roles and a classification invariant")
    if rule["severity"] not in {"info", "low", "medium", "high"}:
        raise ValueError("invalid status severity")
    for role in _ROLES:
        selector = rule[role]
        if not isinstance(selector, dict) or set(selector) != {"file", "symbol"} or not _path(selector["file"]) or not _string(selector["symbol"]):
            raise ValueError("status roles contain only exact file/symbol locators")
    invariant = rule["invariant"]
    if not isinstance(invariant, dict) or set(invariant) != {"kind", "status", "status_field", "identity_field"} or invariant["kind"] != "terminal_classification_consistency" or not all(_string(invariant[key]) for key in ("status", "status_field", "identity_field")):
        raise ValueError("status invariant contains only business status and identity tokens")
    if rule["models"] != [MODEL_ID]:
        raise ValueError("status model must be explicitly registered")
    provenance = rule["provenance"]
    if not isinstance(provenance, dict) or set(provenance) - {"authority", "reviewer", "author_approved", "source_doc", "note"} or not _string(provenance.get("authority")) or not _string(provenance.get("source_doc")) or type(provenance.get("author_approved")) is not bool:
        raise ValueError("status provenance requires an authority/source label and author approval flag")
    applicability = rule["applicability"]
    if not isinstance(applicability, dict) or set(applicability) - {"kind", "conditions", "counterexamples"} or applicability.get("kind") != "conditional" or not isinstance(applicability.get("conditions"), list) or not applicability["conditions"] or not all(_string(item) for item in applicability["conditions"]):
        raise ValueError("status rule must retain explicit conditional scope")
    if not isinstance(applicability.get("counterexamples", []), list) or not all(_string(item) for item in applicability.get("counterexamples", [])):
        raise ValueError("status counterexamples are descriptive policy labels, not computed relations")


def _children(node: Any) -> list[Any]:
    return [child for child in node.named_children if child.type not in _TYPE_ONLY and not child.type.endswith("_type")] if node is not None else []


def _field(node: Any, name: str) -> Any:
    return node.child_by_field_name(name) if node is not None else None


def _fn(definition: Any) -> Any:
    node = unwrap(definition.value) if definition is not None and definition.value is not None else getattr(definition, "node", None)
    return node if node is not None and node.type in _FUNCTIONS else None


def _inside(outer: Any, inner: Any) -> bool:
    return bool(outer is not None and inner is not None and outer.start_byte <= inner.start_byte and inner.end_byte <= outer.end_byte)


def _await_operand(node: Any) -> Any:
    node = unwrap(node)
    while node is not None and node.type == "await_expression":
        node = unwrap(next(iter(_children(node)), None))
    return node


class _Analysis:
    def __init__(self, snapshot: GraphSnapshot, rule: dict):
        self.snapshot, self.rule = snapshot, rule
        self.sources = SemanticSources(snapshot)
        self.lexicals: dict[str, LexicalBindings] = {}
        self.environments: dict[str, BuiltinEnvironment] = {}
        self.source: list[dict] = []
        self.gaps: list[dict] = []
        self.operations = 0
        self.incomplete = False
        self.status = rule["invariant"]["status"]
        self.status_field = rule["invariant"]["status_field"]
        self.identity_field = rule["invariant"]["identity_field"]
        self.roles: dict[str, tuple[Any, Any, Any]] = {}
        self.node_cache: dict[tuple[int, bool], list[Any]] = {}
        self.aggregate_cache: dict[tuple, dict] = {}

    def gap(self, code: str, document: Any = None, node: Any = None, **details: Any) -> dict:
        record = {"code": code, "origin": "unresolved", "location": document.location(node) if document is not None and node is not None and document.contains(node) else None, **details}
        if record not in self.gaps:
            self.gaps.append(record)
        return record

    def fact(self, kind: str, document: Any, node: Any, **details: Any) -> dict:
        result = {"kind": kind, "origin": "source-derived", "snapshot_id": self.snapshot.id,
            "location": document.location(node), **details}
        result["id"] = _digest({"version": VERSION, **result})[:24]
        self.source.append(result)
        return result

    def nodes(self, node: Any, *, nested: bool = False) -> list[Any]:
        key = (node.id, nested) if node is not None else None
        if key is not None and key in self.node_cache:
            return self.node_cache[key]
        result = []
        pending = [node] if node is not None else []
        while pending:
            current = pending.pop()
            self.operations += 1
            if self.operations > _NODE_LIMIT:
                self.incomplete = True
                break
            if current.type in _TYPE_ONLY or current.type.endswith("_type"):
                continue
            result.append(current)
            if current != node and not nested and current.type in _FUNCTIONS | {"class", "class_declaration"}:
                continue
            pending.extend(reversed(_children(current)))
        if key is not None and not self.incomplete:
            self.node_cache[key] = result
        return result

    def lexical(self, document: Any) -> LexicalBindings:
        if document.source.path not in self.lexicals:
            self.lexicals[document.source.path] = LexicalBindings(document)
        return self.lexicals[document.source.path]

    def identity(self, document: Any, node: Any) -> dict | None:
        node = unwrap(node)
        if node is None or node.type not in {"identifier", "shorthand_property_identifier", "shorthand_property_identifier_pattern"}:
            return None
        identity = self.lexical(document).resolve(node)
        return identity if identity.get("state") == "unique" and identity.get("identity_complete") else None

    def name(self, document: Any, node: Any) -> str | None:
        if node is None:
            return None
        if node.type in {"identifier", "property_identifier", "shorthand_property_identifier"}:
            text = document.text(node)
            return text if text and "\\" not in text else None
        return _literal_string(document.text(node)) if node.type == "string" else None

    def path(self, document: Any, node: Any) -> tuple[str, tuple[str, ...]] | None:
        node = unwrap(node)
        if node is None:
            return None
        if node.type in {"identifier", "shorthand_property_identifier"}:
            identity = self.identity(document, node)
            return (identity["declaration_id"], ()) if identity else None
        if node.type in {"member_expression", "subscript_expression"}:
            root = self.path(document, _field(node, "object"))
            child = _field(node, "property") if node.type == "member_expression" else unwrap(_field(node, "index"))
            key = self.name(document, child) if node.type == "member_expression" or child is not None and child.type == "string" else None
            return (root[0], (*root[1], key)) if root is not None and key is not None else None
        return None

    def parameters(self, document: Any, function: Any) -> list[dict | None]:
        return [self.identity(document, _field(parameter, "pattern") or _field(parameter, "name") or parameter)
            for parameter in _children(_field(function, "parameters"))]

    def select(self, role: str) -> tuple[Any, Any, Any]:
        document, definition, issues = self.sources.select(self.rule[role])
        function = _fn(definition)
        if issues or document is None or function is None:
            self.gap("status_role_source_invalid", role=role, source_issues=issues)
        self.roles[role] = (document, definition, function)
        return document, definition, function

    def owner(self, document: Any, node: Any) -> Any:
        current = node
        while current is not None and current.type not in _FUNCTIONS:
            current = current.parent
        return document.definition_for_ast(current) if current is not None else None

    def binding(self, document: Any, call: Any, *, required: bool = True) -> tuple[Any, Any, Any, Any]:
        edge, issues = self.sources.call_binding(call, document, self.owner(document, call))
        if edge is None:
            if required:
                self.gap("status_actual_call_binding_unknown", document, call, source_issues=issues)
            return None, None, None, None
        targets = self.sources.nodes.get(edge.target, [])
        target_document, target_definition, problems = self.sources.definition_for_node(targets[0]) if len(targets) == 1 else (None, None, [])
        if problems or target_document is None or _fn(target_definition) is None:
            if required:
                self.gap("status_call_target_source_invalid", document, call, source_issues=problems)
            return None, None, None, None
        return edge, target_document, target_definition, _fn(target_definition)

    def call_fact(self, document: Any, call: Any) -> tuple[dict | None, Any, Any, Any]:
        edge, target_document, target_definition, target = self.binding(document, call)
        if edge is None:
            return None, None, None, None
        args = _children(_field(call, "arguments"))
        params = self.parameters(target_document, target)
        mappings = [{"argument_index": index, "argument_location": document.location(argument),
            "argument_binding_path": self.path(document, argument), "formal_declaration_id": params[index]["declaration_id"] if index < len(params) and params[index] else None,
            "formal_location": target_document.location(_children(_field(target, "parameters"))[index]) if index < len(params) else None}
            for index, argument in enumerate(args)]
        fact = self.fact("actual_call_argument_formal_mapping", document, call, edge_id=edge.id,
            source_graph_node_id=edge.source, target_graph_node_id=edge.target, mappings=mappings,
            function_kind=function_kind(target_document, target), invocation_or_fulfillment_guaranteed=False)
        return fact, target_document, target_definition, target

    def initializer(self, document: Any, node: Any) -> Any:
        identity = self.identity(document, node)
        return unwrap(self.lexical(document).initializer_for(identity)) if identity else None

    def imported_declaration(self, document: Any, identity: dict) -> tuple[Any, Any]:
        imported = identity.get("import")
        if not imported:
            return document, self.lexical(document).declaration_for(identity)
        module = imported.get("module")
        if not isinstance(module, str) or not module.startswith(".") or imported.get("imported_name") in {None, "*", "default"}:
            return None, None
        raw = PurePosixPath(document.source.path).parent / module
        normalized: list[str] = []
        for part in raw.parts:
            if part == "..":
                if not normalized:
                    return None, None
                normalized.pop()
            elif part != ".":
                normalized.append(part)
        base = PurePosixPath(*normalized)
        candidates = [str(base), *(str(base.with_suffix(suffix)) for suffix in (".ts", ".tsx", ".js"))]
        matches = []
        for path in dict.fromkeys(candidates):
            if path not in self.sources.files:
                continue
            provider, definition, issues = self.sources.select({"file": path, "symbol": imported["imported_name"]})
            if provider is not None and definition is not None and not issues:
                parent = definition.node.parent
                while parent is not None and parent.type in {"lexical_declaration", "variable_declaration"}:
                    parent = parent.parent
                if parent is not None and parent.type == "export_statement":
                    matches.append((provider, definition.node))
        return matches[0] if len(matches) == 1 else (None, None)

    def aggregate_audit(self, document: Any, identity: dict, *, kind: str) -> dict:
        key = (document.source.hash, identity["declaration_id"], kind)
        if key in self.aggregate_cache:
            return self.aggregate_cache[key]
        nodes = self.nodes(document.tree.root_node, nested=True)
        roots = {identity["declaration_id"]}
        names = {identity.get("name")}
        aliases = []
        for _ in range(_DEPTH):
            previous = len(roots)
            for declaration in (node for node in nodes if node.type == "variable_declarator"):
                rhs = unwrap(_field(declaration, "value"))
                if rhs is None or rhs.type != "identifier" or document.text(rhs) not in names:
                    continue
                path = self.path(document, rhs)
                binder = self.identity(document, _field(declaration, "name"))
                if path is not None and path == (path[0], ()) and path[0] in roots and binder:
                    roots.add(binder["declaration_id"])
                    names.add(binder["name"])
                    aliases.append(document.location(declaration))
            if len(roots) == previous:
                break
        blockers = []
        read_uses = []
        for node in nodes:
            target = _field(node, "left") if node.type in {"assignment_expression", "augmented_assignment_expression"} else _field(node, "argument") if node.type == "update_expression" or node.type == "unary_expression" and document.text(_field(node, "operator")) == "delete" else None
            root = unwrap(target)
            while root is not None and root.type in {"member_expression", "subscript_expression"}:
                root = unwrap(_field(root, "object"))
            if root is not None and root.type == "identifier" and document.text(root) in names:
                path = self.path(document, root)
                if path is not None and path[0] in roots:
                    blockers.append({"kind": "captured_aggregate_write", "location": document.location(node)})
            if node.type != "call_expression":
                continue
            callee = unwrap(_field(node, "function"))
            if callee is not None and callee.type in {"member_expression", "subscript_expression"}:
                receiver = unwrap(_field(callee, "object"))
                if receiver is not None and receiver.type == "identifier" and document.text(receiver) in names:
                    path = self.path(document, receiver)
                    if path is not None and path[0] in roots:
                        method = self.name(document, _field(callee, "property"))
                        permitted = kind == "handler_table" or method == "has"
                        (read_uses if permitted else blockers).append({"kind": "modeled_read_use" if permitted else "captured_mutator_or_unknown_method",
                            "method": method, "location": document.location(node)})
            for argument in _children(_field(node, "arguments")):
                argument = unwrap(argument)
                if argument is not None and argument.type == "identifier" and document.text(argument) in names:
                    path = self.path(document, argument)
                    if path is not None and path[0] in roots:
                        blockers.append({"kind": "captured_aggregate_argument_escape", "location": document.location(node)})
        result = {"kind": kind, "declaration_id": identity["declaration_id"], "source_file": document.source.path,
            "alias_declaration_ids": sorted(roots - {identity["declaration_id"]}), "alias_locations": aliases,
            "modeled_read_uses": read_uses, "captured_write_or_escape_blockers": blockers,
            "captured_source_audit_complete": not self.incomplete, "supported": not blockers and not self.incomplete,
            "external_or_reflective_world_verified": False}
        self.aggregate_cache[key] = result
        return result

    def collection(self, document: Any, receiver: Any) -> dict | None:
        identity = self.identity(document, receiver)
        if identity is None:
            return None
        provider, declaration = self.imported_declaration(document, identity)
        initializer = unwrap(_field(declaration, "value"))
        if provider is None or initializer is None or initializer.type != "new_expression":
            return None
        constructor = _field(initializer, "constructor")
        arguments = _children(_field(initializer, "arguments"))
        if constructor is None or provider.text(constructor) != "Set" or len(arguments) != 1 or unwrap(arguments[0]).type != "array":
            return None
        elements = _children(unwrap(arguments[0]))
        members = [self.name(provider, element) if element.type == "string" else None for element in elements]
        if any(member is None for member in members):
            return None
        previous = "["
        for child in unwrap(arguments[0]).children:
            if child.type == "comment":
                continue
            if child.type == "," and previous in {"[", ","}:
                return None
            previous = child.type
        if provider.source.path not in self.environments:
            self.environments[provider.source.path] = BuiltinEnvironment(provider)
        audit = self.environments[provider.source.path].audit("Set", initializer)
        if not audit.get("supported"):
            self.gap("status_set_environment_not_supported", provider, initializer, audit=audit)
            return None
        use_audit = self.aggregate_audit(document, identity, kind="set")
        provider_identity = self.identity(provider, _field(declaration, "name"))
        provider_audit = self.aggregate_audit(provider, provider_identity, kind="set") if provider_identity else {"supported": False}
        if not use_audit["supported"] or not provider_audit["supported"]:
            self.gap("status_captured_set_mutation_or_escape", document, receiver, use_audit=use_audit, provider_audit=provider_audit)
            return None
        return self.fact("authenticated_set_receiver_and_initializer", document, receiver,
            receiver_declaration_id=identity["declaration_id"], receiver_import=identity.get("import"),
            provider_declaration_location=provider.location(declaration), provider_initializer_location=provider.location(initializer),
            members=sorted(set(members)), initialization_members_closed=True, standard_environment_audit=audit,
            actual_use_instance_audit=use_audit, provider_instance_audit=provider_audit,
            current_runtime_set_verified=False, membership_stability_is_explicit_model_premise=True)

    def has(self, document: Any, node: Any) -> dict | None:
        node = unwrap(node)
        if node is None or node.type != "call_expression":
            return None
        callee = unwrap(_field(node, "function"))
        if callee is None or callee.type != "member_expression" or self.name(document, _field(callee, "property")) != "has":
            return None
        arguments = _children(_field(node, "arguments"))
        receiver = self.collection(document, _field(callee, "object"))
        if receiver is None or len(arguments) != 1:
            return None
        return {"node": node, "receiver": receiver, "argument": arguments[0], "argument_path": self.path(document, arguments[0])}

    def eval(self, document: Any, node: Any, environment: dict[str, Any], depth: int = 0) -> Any:
        node = unwrap(node)
        if node is None or depth >= _DEPTH:
            return _UNKNOWN
        if node.type == "string":
            return _literal_string(document.text(node))
        if node.type in {"true", "false", "null", "undefined"}:
            return {"true": True, "false": False, "null": None, "undefined": None}[node.type]
        if node.type in {"identifier", "shorthand_property_identifier"}:
            identity = self.identity(document, node)
            return environment.get(identity["declaration_id"], _UNKNOWN) if identity else _UNKNOWN
        if node.type in {"member_expression", "subscript_expression"}:
            receiver = self.eval(document, _field(node, "object"), environment, depth + 1)
            child = _field(node, "property") if node.type == "member_expression" else _field(node, "index")
            key = self.name(document, child)
            if receiver is None and any(item.type == "optional_chain" for item in node.children):
                return None
            return receiver.get(key, None) if isinstance(receiver, dict) and key is not None else _UNKNOWN
        if node.type == "unary_expression":
            value = self.eval(document, _field(node, "argument"), environment, depth + 1)
            operator = document.text(_field(node, "operator"))
            return not bool(value) if value is not _UNKNOWN and operator == "!" else "string" if type(value) is str and operator == "typeof" else _UNKNOWN
        if node.type == "binary_expression":
            left = self.eval(document, _field(node, "left"), environment, depth + 1)
            operator = document.text(_field(node, "operator"))
            if operator == "||" and left is not _UNKNOWN and bool(left):
                return left
            if operator == "&&" and left is not _UNKNOWN and not bool(left):
                return left
            right = self.eval(document, _field(node, "right"), environment, depth + 1)
            if left is _UNKNOWN or right is _UNKNOWN:
                return _UNKNOWN
            if operator == "||":
                return right
            if operator == "&&":
                return right
            if operator in {"===", "!=="}:
                equal = type(left) is type(right) and left == right
                return equal if operator == "===" else not equal
        if node.type == "ternary_expression":
            condition = self.eval(document, _field(node, "condition"), environment, depth + 1)
            if condition is not _UNKNOWN:
                return self.eval(document, _field(node, "consequence" if bool(condition) else "alternative"), environment, depth + 1)
        if node.type == "call_expression":
            membership = self.has(document, node)
            if membership is not None:
                value = self.eval(document, membership["argument"], environment, depth + 1)
                return value in membership["receiver"]["members"] if type(value) is str else _UNKNOWN
            callee = unwrap(_field(node, "function"))
            arguments = _children(_field(node, "arguments"))
            if callee is not None and callee.type == "member_expression" and self.name(document, _field(callee, "property")) == "includes" and len(arguments) == 1:
                receiver = unwrap(_field(callee, "object"))
                members = [self.eval(document, child, environment, depth + 1) for child in _children(receiver)] if receiver is not None and receiver.type == "array" else []
                value = self.eval(document, arguments[0], environment, depth + 1)
                if members and all(item is not _UNKNOWN for item in members) and value is not _UNKNOWN:
                    return value in members
            edge, target_document, _, target = self.binding(document, node, required=False)
            if edge is not None:
                params = self.parameters(target_document, target)
                values = [self.eval(document, argument, environment, depth + 1) for argument in arguments]
                if len(values) <= len(params) and all(value is not _UNKNOWN for value in values) and all(params[index] is not None for index in range(len(values))):
                    child_env = {params[index]["declaration_id"]: value for index, value in enumerate(values)}
                    return self.function_eval(target_document, target, child_env, depth + 1)
        return _UNKNOWN

    def function_eval(self, document: Any, function: Any, environment: dict[str, Any], depth: int = 0) -> Any:
        for statement in _children(_field(function, "body")):
            if statement.type == "if_statement":
                condition = self.eval(document, _field(statement, "condition"), environment, depth + 1)
                if condition is _UNKNOWN:
                    return _UNKNOWN
                if bool(condition):
                    selected = _field(statement, "consequence")
                    returned = self.direct_exit(selected, "return_statement")
                    if returned is not None:
                        return self.eval(document, next(iter(_children(returned)), None), environment, depth + 1)
                    return _UNKNOWN
            elif statement.type == "return_statement":
                return self.eval(document, next(iter(_children(statement)), None), environment, depth + 1)
            elif statement.type not in _TYPE_ONLY:
                return _UNKNOWN
        return _UNKNOWN

    def direct_exit(self, branch: Any, kind: str) -> Any:
        """Only direct straight-line branch completion, never a nested hit."""
        if branch is None:
            return None
        if branch.type == kind:
            return branch
        if branch.type != "statement_block":
            return None
        statements = _children(branch)
        if not statements or statements[-1].type != kind:
            return None
        if any(statement.type not in {"expression_statement", "lexical_declaration", "variable_declaration"}
                for statement in statements[:-1]):
            return None
        return statements[-1]

    def same_context_arguments(self, document: Any, function: Any, call_fact: dict | None) -> bool:
        params = self.parameters(document, function)
        mappings = call_fact.get("mappings", []) if call_fact is not None else []
        return (len(params) >= 3 and len(mappings) >= 3
            and all(params[index] is not None and mappings[index]["argument_binding_path"] == (params[index]["declaration_id"], ())
                for index in range(3)))

    def table_entry(self, document: Any, function: Any, table_id: str) -> bool:
        returned_paths = [self.path(document, next(iter(_children(node)), None)) for node in self.returns(function)]
        returned_ids = {path[0] for path in returned_paths if path is not None and not path[1]}
        for call in self.nodes(_field(function, "body")):
            if call.type != "call_expression":
                continue
            callee = unwrap(_field(call, "function"))
            if callee is None or callee.type != "subscript_expression" or self.path(document, _field(callee, "object")) != (table_id, ()):
                continue
            args = _children(_field(call, "arguments"))
            if args and self.path(document, args[0]) in {(identity, ()) for identity in returned_ids}:
                return True
        return False

    def returns(self, function: Any) -> list[Any]:
        return [node for node in self.nodes(_field(function, "body")) if node.type == "return_statement"]

    def producer(self) -> dict:
        document, definition, function = self.roles["producer"]
        if function is None:
            return {"complete": False}
        body = self.nodes(_field(function, "body"))
        returned = self.returns(function)
        state_paths = [self.path(document, next(iter(_children(node)), None)) for node in returned]
        state_ids = {path[0] for path in state_paths if path is not None and not path[1]}
        event_params = self.parameters(document, function)
        handlers = []
        for call in (node for node in body if node.type == "call_expression"):
            callee = unwrap(_field(call, "function"))
            if callee is None or callee.type != "subscript_expression":
                continue
            index_path = self.path(document, _field(callee, "index"))
            table_identity = self.identity(document, _field(callee, "object"))
            initializer = self.initializer(document, _field(callee, "object"))
            arguments = _children(_field(call, "arguments"))
            if table_identity is None or initializer is None or initializer.type != "object" or index_path is None or len(index_path[1]) != 1 or not arguments:
                continue
            state_path = self.path(document, arguments[0])
            if state_path is None or state_path[0] not in state_ids or state_path[1]:
                continue
            event_arg = self.path(document, arguments[1]) if len(arguments) > 1 else None
            if event_arg != (index_path[0], ()):
                continue
            table_members = _children(initializer)
            keys = [self.name(document, _field(member, "name") if member.type == "method_definition" else _field(member, "key")) for member in table_members]
            table_audit = self.aggregate_audit(document, table_identity, kind="handler_table")
            table_closed = all(key is not None for key in keys) and len(keys) == len(set(keys)) and table_audit["supported"]
            for member, key in zip(table_members, keys):
                if member.type != "method_definition":
                    continue
                params = self.parameters(document, member)
                if not params or params[0] is None:
                    continue
                writes = [node for node in self.nodes(_field(member, "body")) if node.type == "assignment_expression"
                    and self.path(document, _field(node, "left")) == (params[0]["declaration_id"], (self.status_field,))]
                matching = [node for node in writes if self.eval(document, _field(node, "right"), {}) == self.status]
                if not matching:
                    continue
                dispatches = []
                # Find every same-table source entry, including single-event
                # advance paths, without manufacturing a dynamic CALLS edge.
                for candidate in self.nodes(document.tree.root_node, nested=True):
                    if candidate.type != "call_expression":
                        continue
                    target = unwrap(_field(candidate, "function"))
                    if target is None or target.type != "subscript_expression" or not self.lexical(document).same(self.identity(document, _field(target, "object")) or {}, table_identity):
                        continue
                    args = _children(_field(candidate, "arguments"))
                    if len(args) != len(params):
                        continue
                    entry_definition = self.owner(document, candidate)
                    entry_function = _fn(entry_definition)
                    entry_params = self.parameters(document, entry_function)
                    selector_path = self.path(document, _field(target, "index"))
                    event_path = self.path(document, args[1]) if len(args) > 1 else None
                    event_source_closed = selector_path is not None and event_path == (selector_path[0], ())
                    ancestor = candidate.parent
                    loop = None
                    while ancestor is not None and ancestor != entry_function:
                        if ancestor.type == "for_in_statement":
                            loop = ancestor
                            break
                        ancestor = ancestor.parent
                    if loop is not None:
                        event_source_closed = event_source_closed and self.path(document, _field(loop, "left")) == event_path
                        loop_source = self.path(document, _field(loop, "right"))
                        event_source_closed = event_source_closed and bool(entry_params and entry_params[0]) and loop_source == (entry_params[0]["declaration_id"], ())
                    else:
                        event_source_closed = event_source_closed and any(param is not None and event_path == (param["declaration_id"], ()) for param in entry_params)
                    entry_closed = event_source_closed and self.table_entry(document, entry_function, table_identity["declaration_id"])
                    dispatches.append(self.fact("finite_handler_table_dispatch_argument_mapping", document, candidate,
                        table_declaration_id=table_identity["declaration_id"], table_location=document.location(initializer), table_static_keys_closed=table_closed,
                        selected_event_key=key, handler_location=document.location(member),
                        selector_expression_location=document.location(_field(target, "index")),
                        mappings=[{"argument_index": index, "argument_binding_path": self.path(document, argument),
                            "argument_location": document.location(argument), "formal_declaration_id": params[index]["declaration_id"] if params[index] else None}
                            for index, argument in enumerate(args)],
                        entry_function_location=document.location(entry_function), event_loop_location=document.location(loop) if loop else None,
                        event_source_parameter_or_iteration_closed=event_source_closed, returned_state_same_dispatch_argument=entry_closed,
                        dynamic_dispatch_graph_edge_created=False, activation_conditional=True))
                identity_writes = [node for node in body if node.type == "assignment_expression"
                    and self.path(document, _field(node, "left")) == (state_path[0], (self.identity_field,))
                    and self.path(document, _field(node, "right")) == (index_path[0], (self.identity_field,))]
                status_write = self.fact("selected_status_handler_write", document, matching[0],
                    status_value=self.status, status_field=self.status_field, state_formal_declaration_id=params[0]["declaration_id"],
                    event_key=key, handler_location=document.location(member), producer_return_binding_id=state_path[0],
                    dispatch_relation_ids=[item["id"] for item in dispatches], event_to_state_identity_write_locations=[document.location(node) for node in identity_writes])
                allowed_writers = []
                for other, other_key in zip(table_members, keys):
                    if other.type != "method_definition":
                        continue
                    other_params = self.parameters(document, other)
                    if not other_params or other_params[0] is None:
                        continue
                    for write in self.nodes(_field(other, "body")):
                        if write.type == "assignment_expression" and self.path(document, _field(write, "left")) == (other_params[0]["declaration_id"], (self.status_field,)):
                            allowed_writers.append({"event_key": other_key, "location": document.location(write), "value_expression": document.text(_field(write, "right"))})
                handlers.append({"event_key": key, "status_write": status_write, "dispatches": dispatches,
                    "table_declaration_id": table_identity["declaration_id"], "event_selector_field": index_path[1][0],
                    "table_source_mutation_audit": table_audit, "all_table_status_writers": allowed_writers,
                    "complete": table_closed and bool(identity_writes) and bool(dispatches) and len(writes) == len(matching) == 1
                        and all(item["event_source_parameter_or_iteration_closed"] and item["returned_state_same_dispatch_argument"] for item in dispatches)})
        if len(handlers) != 1:
            self.gap("status_producer_handler_not_unique", document, function, matching_handlers=len(handlers))
        return handlers[0] if len(handlers) == 1 else {"complete": False}

    def predicate(self) -> dict:
        document, _, function = self.roles["predicate"]
        if function is None:
            return {"complete": False}
        params = self.parameters(document, function)
        if len(params) != 1 or params[0] is None:
            return {"complete": False}
        memberships = [self.has(document, node) for node in self.nodes(_field(function, "body")) if node.type == "call_expression"]
        memberships = [item for item in memberships if item is not None]
        expected = (params[0]["declaration_id"], (self.status_field,))
        selected = []
        for membership in memberships:
            argument = unwrap(membership["argument"])
            status_argument = _field(argument, "left") if argument is not None and argument.type == "binary_expression" and document.text(_field(argument, "operator")) == "||" else argument
            if self.path(document, status_argument) == expected:
                selected.append(membership)
        cases = []
        for identity_present, status_value in ((True, self.status), (False, self.status), (True, None)):
            job = {self.status_field: status_value}
            if identity_present:
                job[self.identity_field] = "nonempty-identity"
            result = self.function_eval(document, function, {params[0]["declaration_id"]: job})
            cases.append({"identity_present": identity_present, "status": status_value,
                "predicate_result": result if result is not _UNKNOWN else None, "evaluation_closed": result is not _UNKNOWN})
        complete = len(selected) == 1 and all(case["evaluation_closed"] for case in cases)
        fact = self.fact("finite_status_predicate_truth_table", document, function,
            parameter_declaration_id=params[0]["declaration_id"], receiver=selected[0]["receiver"] if len(selected) == 1 else None,
            actual_membership_locations=[document.location(item["node"]) for item in selected],
            status_default_locations=[document.location(item["argument"]) for item in selected], cases=cases,
            early_identity_and_status_default_semantics_derived=True, complete=complete)
        return {"complete": complete, "fact": fact, "cases": cases,
            "members": selected[0]["receiver"]["members"] if len(selected) == 1 else []}

    def projection_origin(self, document: Any, call: Any) -> dict:
        fact, reader_document, _, reader_function = self.call_fact(document, call)
        if fact is None:
            return {"complete": False}
        returns = self.returns(reader_function)
        cases = []
        for statement in returns:
            expression = unwrap(next(iter(_children(statement)), None))
            if expression is None or expression.type != "member_expression":
                continue
            component = self.name(reader_document, _field(expression, "property"))
            projection_call = _await_operand(_field(expression, "object"))
            if projection_call is None or projection_call.type != "call_expression":
                continue
            projection_fact, projection_document, _, projection_function = self.call_fact(reader_document, projection_call)
            if projection_fact is None:
                continue
            projection_returns = self.returns(projection_function)
            projection_context_closed = self.same_context_arguments(reader_document, reader_function, projection_fact)
            producer_definition = self.roles["producer"][1]
            producer_table_id = self.producer_table_id
            event_reads = []
            for declaration in self.nodes(_field(projection_function, "body")):
                if declaration.type != "variable_declarator":
                    continue
                rhs = _await_operand(_field(declaration, "value"))
                if rhs is None or rhs.type != "call_expression":
                    continue
                read_edge, _, _, _ = self.binding(projection_document, rhs, required=False)
                if read_edge is not None:
                    read_relation, _, _, _ = self.call_fact(projection_document, rhs)
                    if self.same_context_arguments(projection_document, projection_function, read_relation):
                        event_reads.append({"binding_path": self.path(projection_document, _field(declaration, "name")), "relation": read_relation})
            branches = []
            for returned in projection_returns:
                result = unwrap(next(iter(_children(returned)), None))
                if result is None or result.type != "object":
                    continue
                members = [pair for pair in _children(result) if pair.type == "pair" and self.name(projection_document, _field(pair, "key")) == component]
                if len(members) != 1:
                    continue
                value = unwrap(_field(members[0], "value"))
                origin_calls = []
                branch_closed = False
                if value is not None and value.type == "call_expression":
                    origin_fact, _, origin_definition, _ = self.call_fact(projection_document, value)
                    if origin_fact:
                        origin_calls.append(origin_fact)
                        arguments = _children(_field(value, "arguments"))
                        branch_closed = (origin_definition.graph_node_id == producer_definition.graph_node_id and len(arguments) == 1
                            and any(self.path(projection_document, arguments[0]) == read["binding_path"] for read in event_reads))
                elif value is not None and value.type == "identifier":
                    identity = self.identity(projection_document, value)
                    initializer = self.initializer(projection_document, value)
                    if initializer is not None and initializer.type == "call_expression":
                        origin_calls.append(self.fact("projection_branch_clone_initializer", projection_document, initializer,
                            binding_id=identity["declaration_id"] if identity else None, runtime_clone_success_proven=False))
                    for candidate in self.nodes(_field(projection_function, "body")):
                        if candidate.type == "assignment_expression" and self.path(projection_document, _field(candidate, "left")) == self.path(projection_document, value):
                            rhs = _await_operand(_field(candidate, "right"))
                            if rhs is not None and rhs.type == "call_expression":
                                update, _, _, _ = self.call_fact(projection_document, rhs)
                                if update:
                                    origin_calls.append(update)
                                    _, advance_document, _, advance_function = self.binding(projection_document, rhs)
                                    args = _children(_field(rhs, "arguments"))
                                    branch_closed = bool(producer_table_id and self.table_entry(advance_document, advance_function, producer_table_id)
                                        and args and self.path(projection_document, args[0]) == self.path(projection_document, value)
                                        and initializer is not None and initializer.type == "call_expression")
                parts = _children(result)
                member_index = next(index for index, part in enumerate(parts) if part.id == members[0].id)
                selected_tail_closed = all(part.type == "pair" and self.name(projection_document, _field(part, "key")) not in {None, component, "__proto__"}
                    for part in parts[member_index + 1:])
                branches.append(self.fact("normal_projection_return_component_origin", projection_document, returned,
                    selected_component=component, component_value_location=projection_document.location(value),
                    component_binding_path=self.path(projection_document, value), origin_calls=origin_calls,
                    producer_or_same_table_advance_source_closed=branch_closed,
                    same_job_event_read_relations=event_reads, selected_component_last_definition_closed=selected_tail_closed,
                    selected_status_value_assumed_from_current_projection=True,
                    exact_checkpoint_state_or_digest_equality_claimed=False))
            cases.append(self.fact("normal_reader_return_projection_component", reader_document, statement,
                selected_component=component, projection_call_relation=projection_fact,
                all_projection_return_count=len(projection_returns), selected_component_return_count=len(branches),
                same_context_arguments_forwarded=projection_context_closed,
                projection_return_branches=branches, reader_call_relation=fact,
                normal_data_fulfillment_model_required=True))
        complete = bool(returns) and len(cases) == len(returns) and all(item["same_context_arguments_forwarded"] and item["all_projection_return_count"] > 0
            and item["all_projection_return_count"] == item["selected_component_return_count"]
            and all(branch["producer_or_same_table_advance_source_closed"] and branch["selected_component_last_definition_closed"]
                for branch in item["projection_return_branches"]) for item in cases)
        return {"complete": complete, "reader_call": fact, "return_cases": cases}

    def rejecting_guards(self, document: Any, function: Any) -> list[tuple[Any, Any]]:
        result = []
        for node in self.nodes(_field(function, "body")):
            if node.type != "if_statement":
                continue
            consequence = _field(node, "consequence")
            thrown = self.direct_exit(consequence, "throw_statement")
            if thrown is not None:
                result.append((node, thrown))
        return result

    def consumer(self, predicate: dict) -> dict:
        document, _, function = self.roles["consumer"]
        target_definition = self.roles["predicate"][1]
        if function is None or target_definition is None:
            return {"complete": False}
        matches = []
        for guard, thrown in self.rejecting_guards(document, function):
            condition = unwrap(_field(guard, "condition"))
            if condition is None or condition.type != "unary_expression" or document.text(_field(condition, "operator")) != "!":
                continue
            call = unwrap(_field(condition, "argument"))
            if call is None or call.type != "call_expression":
                continue
            edge, _, _, _ = self.binding(document, call, required=False)
            if edge is None or edge.target != target_definition.graph_node_id:
                continue
            arguments = _children(_field(call, "arguments"))
            if len(arguments) != 1 or arguments[0].type != "identifier":
                continue
            original = self.identity(document, arguments[0])
            initializer = _await_operand(self.initializer(document, arguments[0]))
            if original is None or original.get("declaration_kind") != "const" or initializer is None or initializer.type != "call_expression":
                continue
            origin = self.projection_origin(document, initializer)
            consumer_params = self.parameters(document, function)
            reader_mapping = origin.get("reader_call", {}).get("mappings", [])
            identity_forwarded = (len(consumer_params) >= 3 and len(reader_mapping) >= 3
                and all(consumer_params[index] is not None
                    and reader_mapping[index]["argument_binding_path"] == (consumer_params[index]["declaration_id"], ())
                    for index in range(3)))
            predicate_call, _, _, _ = self.call_fact(document, call)
            cases = []
            for identity_present in (True, False):
                value = {self.status_field: self.status}
                if identity_present:
                    value[self.identity_field] = "nonempty-identity"
                environment = {original["declaration_id"]: value}
                selected = None
                for earlier, error in self.rejecting_guards(document, function):
                    if earlier.start_byte > guard.start_byte:
                        continue
                    evaluated = self.eval(document, _field(earlier, "condition"), environment)
                    if evaluated is _UNKNOWN:
                        break
                    if bool(evaluated):
                        selected = self.fact("derived_consumer_rejection_case", document, error,
                            identity_present=identity_present, current_status=self.status,
                            selected_guard_location=document.location(earlier), error_source_expression=document.text(error),
                            predicate_guard_reached=earlier.id == guard.id,
                            predicate_guard_rejects=earlier.id == guard.id, consumer_rejects=True,
                            source_branch_rejects_before_later_recovery_return=True)
                        break
                    if earlier.id == guard.id:
                        selected = self.fact("derived_consumer_terminal_guard_pass_case", document, guard,
                            identity_present=identity_present, current_status=self.status,
                            selected_guard_location=document.location(guard), error_source_expression=None,
                            predicate_guard_reached=True, predicate_guard_rejects=False, consumer_rejects=False,
                            recovery_permission_or_later_guard_success_proven=False)
                        break
                cases.append(selected)
            fact = self.fact("projection_to_same_original_predicate_rejection", document, guard,
                original_declaration_id=original["declaration_id"], original_initializer_location=document.location(initializer),
                projection_origin=origin, actual_predicate_call=predicate_call,
                same_root_project_job_identity_arguments_forwarded=identity_forwarded,
                rejection_location=document.location(thrown), cases=cases)
            matches.append({"complete": origin["complete"] and identity_forwarded and predicate_call is not None and all(cases)
                and bool(cases[0]["predicate_guard_reached"]) and not bool(cases[1]["predicate_guard_reached"]), "fact": fact})
        if len(matches) != 1:
            self.gap("status_consumer_guard_not_unique", document, function, matching_guards=len(matches))
        return matches[0] if len(matches) == 1 else {"complete": False}

    def normal_return_of_call(self, document: Any, function: Any, call: Any) -> dict:
        returned = self.returns(function)
        origins = []
        nodes = self.nodes(_field(function, "body"))
        for statement in returned:
            value = _await_operand(next(iter(_children(statement)), None))
            if value is not None and value.id == call.id:
                origins.append({"return_location": document.location(statement), "source_call_location": document.location(call), "direct_call_return": True})
                continue
            path = self.path(document, value)
            if path is None or path[1]:
                continue
            initializer = _await_operand(self.initializer(document, value))
            if initializer is not None and initializer.id == call.id:
                origins.append({"return_location": document.location(statement), "source_call_location": document.location(call), "return_binding_path": path})
                continue
            writes = [node for node in nodes if node.type == "assignment_expression" and self.path(document, _field(node, "left")) == path]
            matching = [write for write in writes if _await_operand(_field(write, "right")) is not None
                and _await_operand(_field(write, "right")).id == call.id]
            if len(writes) == len(matching) == 1:
                origins.append({"return_location": document.location(statement), "source_call_location": document.location(call),
                    "return_binding_path": path, "callback_result_assignment_location": document.location(matching[0])})
        return {"complete": bool(returned) and len(origins) == len(returned), "all_normal_return_count": len(returned),
            "return_origins": origins, "source_call_itself_fulfills_normally_required": True}

    def callback_forwarding(self, document: Any, call: Any, callback_index: int, depth: int = 0) -> dict:
        if depth >= _DEPTH:
            return {"complete": False}
        relation, target_document, _, target = self.call_fact(document, call)
        params = self.parameters(target_document, target) if target is not None else []
        if relation is None or callback_index >= len(params) or params[callback_index] is None:
            return {"complete": False}
        callback_id = params[callback_index]["declaration_id"]
        body = self.nodes(_field(target, "body"))
        invocations = [node for node in body if node.type == "call_expression" and self.path(target_document, _field(node, "function")) == (callback_id, ())]
        if invocations:
            return_relation = self.normal_return_of_call(target_document, target, invocations[0]) if len(invocations) == 1 else {"complete": False}
            return {"complete": return_relation["complete"], "call_relation": relation,
                "callback_invocation_locations": [target_document.location(node) for node in invocations],
                "callback_result_normal_return_relation": return_relation,
                "callback_fulfillment_and_release_success_conditional": True}
        forwards = []
        for candidate in (node for node in body if node.type == "call_expression"):
            for index, argument in enumerate(_children(_field(candidate, "arguments"))):
                if self.path(target_document, argument) == (callback_id, ()):
                    child = self.callback_forwarding(target_document, candidate, index, depth + 1)
                    return_relation = self.normal_return_of_call(target_document, target, candidate)
                    if child["complete"] and return_relation["complete"]:
                        child["forwarding_normal_return_relation"] = return_relation
                        forwards.append(child)
        return {"complete": len(forwards) == 1, "call_relation": relation, "callback_forwarding": forwards}

    def incoming_type_normalizer(self, document: Any, argument: Any, event_field: str | None) -> dict:
        initializer = self.initializer(document, argument)
        if initializer is None or initializer.type != "call_expression":
            return {"complete": False}
        relation, target_document, _, target = self.call_fact(document, initializer)
        args = _children(_field(initializer, "arguments"))
        params = self.parameters(target_document, target) if target is not None else []
        returned = self.returns(target) if target is not None else []
        if relation is None or len(args) != 1 or len(params) != 1 or params[0] is None or len(returned) != 1:
            return {"complete": False}
        value = unwrap(next(iter(_children(returned[0])), None))
        if value is None or value.type != "ternary_expression":
            return {"complete": False}
        condition = unwrap(_field(value, "condition"))
        left = unwrap(_field(condition, "left")) if condition is not None and condition.type == "binary_expression" else None
        string_test = (condition is not None and target_document.text(_field(condition, "operator")) == "==="
            and left is not None and left.type == "unary_expression" and target_document.text(_field(left, "operator")) == "typeof"
            and self.path(target_document, _field(left, "argument")) == (params[0]["declaration_id"], ())
            and self.eval(target_document, _field(condition, "right"), {}) == "string")
        same_value = self.path(target_document, _field(value, "consequence")) == (params[0]["declaration_id"], ())
        input_path = self.path(document, args[0])
        fallback = self.eval(target_document, _field(value, "alternative"), {})
        complete = string_test and same_value and type(fallback) is str and input_path is not None and input_path[1] == (event_field,)
        return {"complete": complete, "actual_normalizer_call_relation": relation,
            "normalizer_return_location": target_document.location(returned[0]), "input_binding_path": input_path,
            "actual_input_member_location": document.location(args[0]), "string_input_returns_same_current_value": string_test and same_value,
            "non_string_fallback": fallback if fallback is not _UNKNOWN else None,
            "initial_external_event_value_identity_claimed": False}

    def durable_append_boundary(self, document: Any, call: Any) -> dict | None:
        edge, target_document, _, target = self.binding(document, call, required=False)
        if edge is None:
            return None
        nodes = self.nodes(_field(target, "body"))
        params = self.parameters(target_document, target)
        if len(params) < 2 or params[0] is None or params[1] is None:
            return None
        handles = []
        for assignment in (node for node in nodes if node.type == "assignment_expression"):
            rhs = _await_operand(_field(assignment, "right"))
            if rhs is None or rhs.type != "call_expression":
                continue
            callee = unwrap(_field(rhs, "function"))
            imported = self.identity(target_document, callee)
            args = _children(_field(rhs, "arguments"))
            imported_source = (imported.get("import") or {}) if imported else {}
            if (imported_source.get("module") == "node:fs/promises" and imported_source.get("imported_name") == "open"
                    and args and self.path(target_document, args[0]) == (params[0]["declaration_id"], ())):
                handles.append((self.path(target_document, _field(assignment, "left")), rhs))
        boundaries = []
        for candidate in (node for node in nodes if node.type == "call_expression"):
            callee = unwrap(_field(candidate, "function"))
            if callee is None or callee.type != "member_expression" or self.name(target_document, _field(callee, "property")) != "write":
                continue
            receiver = self.path(target_document, _field(callee, "object"))
            if any(receiver == handle[0] for handle in handles):
                boundaries.append(target_document.location(candidate))
        if not boundaries:
            return None
        return self.fact("actual_file_handle_append_boundary", document, call,
            edge_id=edge.id, target_graph_node_id=edge.target, target_location=target_document.location(target),
            file_parameter_id=params[0]["declaration_id"], serialized_parameter_id=params[1]["declaration_id"],
            imported_file_open_locations=[target_document.location(item[1]) for item in handles], file_handle_write_locations=boundaries,
            durability_runtime_success_proven=False)

    def authority(self, producer: dict) -> dict:
        document, _, function = self.roles["authority"]
        producer_definition = self.roles["producer"][1]
        if function is None or producer_definition is None:
            return {"complete": False}
        results = []
        for candidate in self.nodes(_field(function, "body"), nested=True):
            if candidate.type != "if_statement":
                continue
            condition = unwrap(_field(candidate, "condition"))
            if condition is None or condition.type != "binary_expression" or document.text(_field(condition, "operator")) != "&&":
                continue
            left = self.has(document, _field(condition, "left"))
            right = unwrap(_field(condition, "right"))
            allowed = self.has(document, _field(right, "argument")) if right is not None and right.type == "unary_expression" and document.text(_field(right, "operator")) == "!" else None
            if left is None or allowed is None or left["argument_path"] is None or left["argument_path"][1] != (self.status_field,):
                continue
            returned = self.direct_exit(_field(candidate, "consequence"), "return_statement")
            if returned is None or self.eval(document, next(iter(_children(returned)), None), {}) is not None:
                continue
            state_argument = unwrap(_field(left["argument"], "object"))
            state_init = self.initializer(document, state_argument)
            edge, _, _, _ = self.binding(document, state_init, required=False) if state_init is not None and state_init.type == "call_expression" else (None, None, None, None)
            if edge is None or edge.target != producer_definition.graph_node_id:
                continue
            state_fact, _, _, _ = self.call_fact(document, state_init)
            actual_arguments = _children(_field(state_init, "arguments"))
            event_read = _await_operand(self.initializer(document, actual_arguments[0])) if len(actual_arguments) == 1 else None
            read_fact, _, _, _ = self.call_fact(document, event_read) if event_read is not None and event_read.type == "call_expression" else (None, None, None, None)
            authority_params = self.parameters(document, function)
            read_mapping = read_fact.get("mappings", []) if read_fact is not None else []
            same_identity = (len(authority_params) >= 3 and len(read_mapping) >= 3
                and all(authority_params[index] is not None
                    and read_mapping[index]["argument_binding_path"] == (authority_params[index]["declaration_id"], ())
                    for index in range(3)))
            callback = candidate.parent
            while callback is not None and callback.type not in _FUNCTIONS:
                callback = callback.parent
            parent_call = callback.parent if callback is not None else None
            while parent_call is not None and parent_call.type != "call_expression":
                parent_call = parent_call.parent
            if callback is None or parent_call is None:
                continue
            args = _children(_field(parent_call, "arguments"))
            index = next((index for index, argument in enumerate(args) if argument.id == callback.id), None)
            forwarding = self.callback_forwarding(document, parent_call, index) if index is not None else {"complete": False}
            outer_return = self.normal_return_of_call(document, function, parent_call)
            type_origin = self.incoming_type_normalizer(document, allowed["argument"], producer.get("event_selector_field"))
            callback_body = _field(callback, "body")
            later_calls = [node for node in self.nodes(callback_body) if node.type == "call_expression" and node.start_byte > candidate.end_byte]
            suffix_facts = []
            append_boundaries = []
            for call in later_calls:
                binding, _, _, _ = self.binding(document, call, required=False)
                if binding is not None:
                    suffix_facts.append({"edge_id": binding.id, "target_graph_node_id": binding.target, "location": document.location(call)})
                    boundary = self.durable_append_boundary(document, call)
                    if boundary is not None:
                        append_boundaries.append(boundary)
            terminal = self.status in left["receiver"]["members"]
            allowed_writers = [writer for writer in producer.get("all_table_status_writers", []) if writer["event_key"] in allowed["receiver"]["members"]]
            fact = self.fact("authority_terminal_seal_and_allowed_exception", document, candidate,
                terminal_receiver=left["receiver"], allow_receiver=allowed["receiver"], current_status=self.status,
                current_status_is_terminal=terminal, event_read_relation=read_fact, state_projection_relation=state_fact,
                same_root_project_job_identity_arguments_forwarded=same_identity,
                incoming_event_type_expression_location=document.location(allowed["argument"]),
                incoming_type_normalizer_origin=type_origin,
                rejected_case={"current_status": self.status, "incoming_type_membership": "outside_allowlist", "callback_return": None,
                    "later_same_callback_calls_unreachable_on_rejection": suffix_facts},
                allowed_case={"current_status": self.status, "incoming_type_membership": "inside_allowlist", "seal_guard_rejects": False},
                callback_return_location=document.location(returned), callback_forwarding=forwarding,
                callback_result_to_outer_return=outer_return, actual_later_durable_append_boundaries=append_boundaries,
                allowed_status_mutating_handlers=allowed_writers,
                immutable_terminal_history_claimed=False, all_journals_or_all_event_writers_protected=False)
            results.append({"complete": terminal and same_identity and read_fact is not None and state_fact is not None
                    and forwarding["complete"] and outer_return["complete"] and type_origin["complete"] and bool(append_boundaries),
                "fact": fact, "terminal_members": left["receiver"]["members"], "allow_members": allowed["receiver"]["members"]})
        if len(results) != 1:
            self.gap("status_authority_seal_not_unique", document, function, matching_seals=len(results))
        return results[0] if len(results) == 1 else {"complete": False}

    def recoverability(self) -> dict:
        document, _, function = self.roles["recoverability"]
        if function is None:
            return {"complete": False}
        params = self.parameters(document, function)
        if len(params) != 1 or params[0] is None:
            return {"complete": False}
        result = self.function_eval(document, function, {params[0]["declaration_id"]: {
            self.identity_field: "nonempty-identity", self.status_field: self.status}})
        fact = self.fact("independent_recoverability_predicate_scope", document, function,
            current_status=self.status, valid_identity=True, recoverability_result=result if result is not _UNKNOWN else None,
            result_closed=result is not _UNKNOWN, terminal_consistency_does_not_grant_recovery=True)
        return {"complete": result is not _UNKNOWN, "fact": fact}

    def run(self) -> dict:
        for role in sorted(_ROLES):
            self.select(role)
        producer = self.producer()
        self.producer_table_id = producer.get("table_declaration_id")
        predicate = self.predicate()
        consumer = self.consumer(predicate)
        authority = self.authority(producer)
        recoverability = self.recoverability()
        valid_result = next((case["predicate_result"] for case in predicate.get("cases", []) if case["identity_present"] and case["status"] == self.status), None)
        differing = authority.get("complete", False) and predicate.get("complete", False) and (self.status in authority.get("terminal_members", [])) != bool(valid_result)
        policy = {"origin": "policy-declared", "contract_hash": _digest(self.rule), "invariant": self.rule["invariant"],
            "role_locators": {role: self.rule[role] for role in sorted(_ROLES)}, "provenance": self.rule["provenance"],
            "classification_comparison_only": True, "required_recovery_permission_declared": False}
        model = {"origin": "trusted-model", "id": MODEL_ID,
            "premises": ["selected records are ordinary data records; status is the stated current primitive value and identity-field reads have no getter or Proxy effects",
                "authenticated Set constructors and selected has/includes operations obey standard semantics; selected module sets retain captured initialized membership",
                "captured private static handler-table own method dispatch obeys ordinary data lookup and argument passing, without table replacement or Proxy/accessor effects",
                "selected ordinary record return/await chains fulfill normally without callable then or accessor assimilation",
                "claims concern selected source guards reached on a normal prefix; callbacks and I/O are not guaranteed to activate or succeed"],
            "runtime_environment_verified": False, "projection_value_or_history_replayed": False}
        summaries = {"S1": producer, "S2": predicate, "S3": consumer, "S4": authority, "S5": recoverability}
        obligations = []
        for suffix, summary in summaries.items():
            closed = bool(summary.get("complete") and not self.incomplete)
            if suffix == "S5":
                closed = closed and bool(producer.get("complete") and predicate.get("complete") and consumer.get("complete") and authority.get("complete"))
            obligations.append({"id": suffix, "assessment": "scoped_static_judgment_reproduced" if closed else "partial_obligations_supported",
                "status": "supported" if closed else "partial",
                "full_obligation_supported": closed, "source": [summary], "model": [model], "policy": [policy],
                "gaps": [] if closed else [{"origin": "unresolved", "code": "status_required_relation_unclosed", "obligation": suffix}],
                "runtime_verified": False})
        complete = bool(obligations and all(item["full_obligation_supported"] for item in obligations) and not self.gaps)
        if not complete and self.gaps:
            for obligation in obligations:
                obligation["full_obligation_supported"] = False
                obligation["status"] = "partial"
                obligation["assessment"] = "partial_obligations_supported"
                obligation["gaps"].extend(self.gaps)
        judgment = {"kind": "conditional_terminal_classification_difference" if differing else "conditional_terminal_classification_comparison",
            "status": self.status, "valid_identity_predicate_result": valid_result,
            "authority_terminal_membership": self.status in authority.get("terminal_members", []),
            "classification_differs": differing, "recovery_is_required_or_authorized": False,
            "terminal_state_can_be_illegally_mutated": False}
        consumer_cases = consumer.get("fact", {}).get("cases", [])
        full_supported = bool(complete and differing and consumer_cases and consumer_cases[0]
            and consumer_cases[0].get("predicate_guard_rejects"))
        assessment = "scoped_static_judgment_reproduced" if full_supported else "claim_refuted_or_narrowed" if complete else "partial_obligations_supported"
        return {"analyzer_version": VERSION, "policy_version": POLICY_VERSION, "snapshot_id": self.snapshot.id,
            "source_hash": self.snapshot.source_hash, "policy_hash": self.snapshot.policy_hash, "contract_hash": _digest(self.rule),
            "obligations": obligations, "assessment": assessment,
            "complete_assessment": complete, "full_goal_supported": full_supported, "source": self.source, "model": [model], "policy": [policy],
            "original_claim": {"invariant": self.rule["invariant"], "source_doc": self.rule["provenance"]["source_doc"],
                "author_approved": self.rule["provenance"]["author_approved"]},
            "conditions": [*self.rule["applicability"]["conditions"], *model["premises"]],
            "refutations": {"invalid_identity_early_predicate_truth_does_not_pass_consumer_identity_guard": consumer.get("fact", {}).get("cases", []),
                "authority_blocks_nonallowlisted_later_mutations": authority.get("fact"),
                "allowed_handlers_can_change_current_status": authority.get("fact", {}).get("allowed_status_mutating_handlers", []),
                "terminal_consistency_does_not_establish_recovery_entitlement": recoverability.get("fact"),
                "original_policy_counterexamples": self.rule["applicability"].get("counterexamples", [])},
            "judgment": judgment, "derived_judgment": judgment,
            "analysis_gaps": self.gaps, "remaining_gaps": [gap for obligation in obligations for gap in obligation["gaps"]],
            "necessary_gaps": [gap for obligation in obligations for gap in obligation["gaps"]],
            "source_budget": {"operations": self.operations, "limit": _NODE_LIMIT, "incomplete": self.incomplete},
            "captured_sources": [{"file": path, "hash": document.source.hash, "parse_id": document.parse_id}
                for path, (document, _) in sorted(self.sources.cache.items()) if document is not None],
            "target_executed": False, "runtime_verified": False, "full_functionality_proven": False}


def _finding(snapshot: GraphSnapshot, rule: dict, details: dict) -> Finding:
    fingerprint = _digest({"version": VERSION, "policy_version": POLICY_VERSION, "project_id": snapshot.project_id, "rule": rule})
    facts = details.get("source", [])
    node_ids = sorted({fact.get(key) for fact in facts for key in ("source_graph_node_id", "target_graph_node_id") if fact.get(key)})
    edge_ids = sorted({fact["edge_id"] for fact in facts if fact.get("edge_id")})
    evidence = Evidence(_digest({"snapshot": snapshot.id, "fingerprint": fingerprint, "details": details})[:24],
        "static_status_classification", "Finite status production, projected record, predicate and rejecting guard relations.",
        [fact["location"] for fact in facts if fact.get("location")], node_ids, edge_ids, details)
    return Finding(_digest({"snapshot": snapshot.id, "fingerprint": fingerprint})[:24], "static_status_classification_flow",
        rule.get("severity", "info"), "uncertain", "Conditional status classification and rejection",
        "Current projected status is classified at authenticated predicates and concrete rejecting source guards; recovery policy remains separate.",
        node_ids, edge_ids, [evidence], rule.get("id", "invalid-status-rule"), fingerprint, snapshot.id,
        {"status_analyzer_version": VERSION, "status_policy_version": POLICY_VERSION,
            "complete_assessment": details.get("complete_assessment", False),
            "full_goal_supported": details.get("full_goal_supported", False), "assessment": details.get("assessment", "unknown_or_source_invalid"),
            "runtime_verified": False, "full_functionality_proven": False})


def analyze_status_contracts(snapshot: GraphSnapshot, rules: list[dict]) -> list[Finding]:
    if not isinstance(rules, list):
        return [_finding(snapshot, {"id": "invalid-status-rules", "severity": "info"},
            {"analysis_gaps": [{"code": "status_rules_invalid"}], "obligations": [], "full_goal_supported": False})]
    counts = Counter(rule.get("id") for rule in rules if isinstance(rule, dict) and isinstance(rule.get("id"), str))
    findings = []
    for index, rule in enumerate(rules):
        try:
            validate_status_rule(rule)
            if counts[rule["id"]] != 1:
                raise ValueError("duplicate status rule id")
            details = _Analysis(snapshot, rule).run()
        except (ValueError, TypeError, AttributeError, RecursionError, IndexError) as error:
            details = {"analysis_gaps": [{"code": "status_rule_or_source_invalid", "message": str(error)[:300]}],
                "obligations": [], "assessment": "unknown_or_source_invalid", "full_goal_supported": False}
        findings.append(_finding(snapshot, rule if isinstance(rule, dict) else {"id": f"invalid-status-rule-{index}", "severity": "info"}, details))
    return findings
