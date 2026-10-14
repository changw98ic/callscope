"""Finite, source-authenticated UI/protocol/conditional-authority judgments.

Roles are locators.  A role is never an injected dependency merely because its
name appears in policy.  Ordinary module binding, object construction, method
forwarding and generated wire-record relationships are checked separately.
No target program, generated module, build script or macro is executed.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib
import json
from pathlib import PurePosixPath
import re
from typing import Any

from .lexical_bindings import LexicalBindings, VERSION as LEXICAL_VERSION
from .completion_summaries import function_kind, VERSION as COMPLETION_VERSION
from .models import Evidence, Finding, GraphSnapshot, SourceFile
from .rust_helpers import classify_helpers, _declared_provider, SERDE_PROFILE, MODEL_VERSION as RUST_HELPER_VERSION
from .semantic_sources import SemanticSources, SemanticDocument, _authenticated_text, unwrap, walk

VERSION = "static-device-spec-protocol-flow-1"
POLICY_VERSION = "static-device-spec-protocol-policy-v1"
MODEL_ID = "captured-device-json-serde-dispatch-v1"
_FUNCTIONS = {"function_declaration", "function_expression", "arrow_function",
    "method_definition", "function_item", "closure_expression"}
_ROLES = {"producer", "port_factory", "view_model", "application", "application_route",
    "observer_factory", "cache_factory", "client_factory", "neutral_factory",
    "generated_transport", "http_factory", "server_dispatcher", "server_family",
    "server_application_dispatcher", "server_delivery_dispatcher", "server_update",
    "server_map", "server_resolve", "server_take", "authority_installer",
    "authority_specification", "authority_decoder", "authority_device_target", "chat_producer",
    "server_router", "server_http_command", "server_http_parser", "criterion_values"}
_IDENTITY = ("file", "source_hash", "start_byte", "end_byte", "span_hash")
_LIMIT = 200000


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True,
        separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def _path(value: Any) -> bool:
    return isinstance(value, str) and bool(value) and not value.startswith("/") and "\\" not in value and all(
        part not in {"", ".", ".."} for part in value.split("/"))


def validate_device_flow_rule(rule: Any) -> None:
    required = {"id", "severity", "roles", "protocol", "models", "provenance", "applicability"}
    if not isinstance(rule, dict) or set(rule) != required:
        raise ValueError("device flow requires locator roles, protocol identity, models and provenance")
    if not isinstance(rule["id"], str) or not rule["id"] or rule["severity"] not in {"high", "medium", "low", "info"}:
        raise ValueError("invalid device flow id/severity")
    if not isinstance(rule["roles"], dict) or set(rule["roles"]) != _ROLES:
        raise ValueError("device flow needs the complete set of locator roles")
    for role, selector in rule["roles"].items():
        if not isinstance(selector, dict) or set(selector) != {"file", "symbol"} or not _path(selector["file"]) or not isinstance(selector["symbol"], str) or not selector["symbol"]:
            raise ValueError(f"invalid {role} locator")
    protocol = rule["protocol"]
    keys = {"command", "schema_version", "wire_field", "rust_field", "command_enum_variant",
        "command_request_variant", "command_type", "payload_type", "spec_type", "command_discriminator_type",
        "request_type", "rust_file", "typescript_file", "rust_domain_file", "schema_version_type", "schema_version_variant", "serde_profile"}
    if not isinstance(protocol, dict) or set(protocol) != keys or not all(isinstance(protocol[key], str) and protocol[key] for key in keys - {"serde_profile"}):
        raise ValueError("protocol identifies declarations and fields; it cannot contain precomputed mappings")
    if not _path(protocol["rust_file"]) or not _path(protocol["typescript_file"]) or not _path(protocol["rust_domain_file"]):
        raise ValueError("protocol source paths must be repository-relative")
    profile = protocol["serde_profile"]
    if not isinstance(profile, dict) or set(profile) != {"id", "crate_root", "workspace_manifest"} or profile["id"] != SERDE_PROFILE or not _path(profile["crate_root"]) or not _path(profile["workspace_manifest"]):
        raise ValueError("serde profile must name an authenticated supported provider")
    if rule["models"] != [MODEL_ID]:
        raise ValueError("unsupported device flow model")
    provenance = rule["provenance"]
    if not isinstance(provenance, dict) or not {"authority", "source_doc", "author_approved"} <= set(provenance) or not isinstance(provenance["authority"], str) or not isinstance(provenance["source_doc"], str) or type(provenance["author_approved"]) is not bool:
        raise ValueError("provenance must retain source and author approval")
    applicability = rule["applicability"]
    if not isinstance(applicability, dict) or set(applicability) != {"kind", "conditions"} or applicability["kind"] != "conditional" or not isinstance(applicability["conditions"], list) or not applicability["conditions"] or not all(isinstance(value, str) and value for value in applicability["conditions"]):
        raise ValueError("device flow must preserve explicit conditional applicability")


@dataclass
class _Role:
    name: str
    doc: SemanticDocument
    definition: Any
    syntax: Any
    source_class: str

    @property
    def body(self):
        return self.syntax.child_by_field_name("body") or self.syntax


def _children(node: Any) -> list[Any]:
    return [child for child in node.named_children if child.type not in {"comment", "line_comment", "block_comment"}] if node is not None else []


def _runtime(node: Any, root: Any = None):
    """Enumerate one lexical body, excluding nested closures and type syntax."""
    if node is None:
        return
    root = node if root is None else root
    yield node
    if node is not root and node.type in _FUNCTIONS | {"class_declaration", "class_expression"}:
        return
    if node.type in {"type_annotation", "type_arguments", "type_parameters", "interface_declaration"} or node.type.endswith("_type"):
        return
    for child in _children(node):
        yield from _runtime(child, root)


def _literal(doc: Any, node: Any) -> Any:
    node = unwrap(node)
    if node is None:
        return None
    if node.type in {"string", "string_literal"}:
        text = doc.text(node)
        if text[:1] == '"':
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return None
        if text[:1] == "'" and "\\" not in text:
            return text[1:-1]
    if node.type in {"true", "false", "true_literal", "false_literal"}:
        return doc.text(node) == "true"
    return None


def _member(doc: Any, node: Any) -> tuple[Any | None, list[str]]:
    node = unwrap(node)
    if node is None:
        return None, []
    if node.type == "member_expression":
        root, keys = _member(doc, node.child_by_field_name("object"))
        prop = node.child_by_field_name("property")
        return (root, [*keys, doc.text(prop)]) if root is not None and prop is not None and prop.type in {"property_identifier", "identifier"} else (None, [])
    if node.type == "field_expression":
        root, keys = _member(doc, node.child_by_field_name("value"))
        prop = node.child_by_field_name("field")
        return (root, [*keys, doc.text(prop)]) if root is not None and prop is not None else (None, [])
    if node.type in {"identifier", "shorthand_property_identifier", "self"}:
        return node, []
    return None, []


def _callee(role: _Role, call: Any) -> str:
    function = unwrap(call.child_by_field_name("function")) if call is not None else None
    if function is None:
        return ""
    if function.type == "generic_function":
        function = function.child_by_field_name("function")
    root, keys = _member(role.doc, function)
    return ".".join([role.doc.text(root), *keys]) if root is not None else role.doc.text(function)


def _arguments(call: Any) -> list[Any]:
    return _children(call.child_by_field_name("arguments")) if call is not None else []


def _strip(node: Any) -> Any:
    node = unwrap(node)
    while node is not None and node.type in {"await_expression", "try_expression", "reference_expression"}:
        children = _children(node)
        if len(children) != 1:
            return node
        node = unwrap(children[0])
    return node


def _text(role: _Role, node: Any) -> str:
    return re.sub(r"\s+", "", role.doc.text(node))


def _attributes(node: Any) -> list[Any]:
    attrs = []
    previous = node.prev_named_sibling
    while previous is not None and previous.type in {"attribute_item", "line_comment", "block_comment"}:
        if previous.type == "attribute_item":
            attrs.append(previous)
        previous = previous.prev_named_sibling
    return list(reversed(attrs))


def _item(doc: Any, name: str, kinds: set[str]) -> Any | None:
    candidates = [node for node in doc.tree.root_node.named_children if node.type in kinds
        and doc.text(node.child_by_field_name("name")) == name]
    return candidates[0] if len(candidates) == 1 else None


def _rust_fields(doc: Any, node: Any) -> dict[str, dict]:
    body = node.child_by_field_name("body") if node is not None else None
    result = {}
    for field in _children(body):
        if field.type != "field_declaration":
            continue
        name = doc.text(field.child_by_field_name("name"))
        attrs = _attributes(field)
        renames = [re.fullmatch(r'#\[serde\(rename\s*=\s*"([^"\\]+)"\)\]', doc.text(attr).strip()) for attr in attrs]
        wire_names = [match.group(1) for match in renames if match]
        result[name] = {"syntax": field, "attributes": attrs, "attribute_text": [doc.text(attr) for attr in attrs],
            "wire_name": wire_names[0] if len(wire_names) == 1 else None,
            "type": doc.text(field.child_by_field_name("type"))}
    return result


def _rust_variants(doc: Any, node: Any) -> list[dict]:
    body = node.child_by_field_name("body") if node is not None else None
    variants = []
    for variant in _children(body):
        if variant.type != "enum_variant":
            continue
        name = doc.text(variant.child_by_field_name("name"))
        attrs = _attributes(variant)
        renames = [re.fullmatch(r'#\[serde\(rename\s*=\s*"([^"\\]+)"\)\]', doc.text(attr).strip()) for attr in attrs]
        wire_names = [match.group(1) for match in renames if match]
        body_node = variant.child_by_field_name("body")
        variants.append({"name": name, "wire_name": wire_names[0] if len(wire_names) == 1 else None,
            "syntax": variant, "attributes": attrs, "type": doc.text(body_node).strip("()") if body_node is not None else None})
    return variants


def _typescript_type(doc: Any, name: str) -> Any | None:
    declarations = [node for node in walk(doc.tree.root_node) if node.type == "type_alias_declaration"
        and doc.text(node.child_by_field_name("name")) == name]
    return declarations[0] if len(declarations) == 1 else None


def _typescript_fields(doc: Any, node: Any) -> dict[str, dict]:
    value = node.child_by_field_name("value") if node is not None else None
    if value is None or value.type != "object_type":
        return {}
    fields = {}
    for child in _children(value):
        if child.type != "property_signature":
            continue
        name_node = child.child_by_field_name("name")
        name = _literal(doc, name_node) if name_node is not None and name_node.type == "string" else doc.text(name_node)
        type_node = child.child_by_field_name("type")
        fields[name] = {"syntax": child, "type": doc.text(type_node).lstrip(":").strip(),
            "optional": any(token.type == "?" for token in child.children)}
    return fields


def _role_for_document(name: str, doc: Any, source_class: str, node: Any) -> _Role:
    class _Definition:
        symbol = doc.text(node.child_by_field_name("name")) or name
        local_name = symbol
        graph_node_id = ""
    return _Role(name, doc, _Definition(), node, source_class)


def _fields(role: _Role, node: Any) -> tuple[dict[str, Any], bool]:
    node = unwrap(node)
    if node is None or node.type != "object":
        return {}, False
    result: dict[str, Any] = {}
    for child in _children(node):
        if child.type == "pair":
            key, value = child.child_by_field_name("key"), child.child_by_field_name("value")
            name = role.doc.text(key) if key is not None and key.type in {"property_identifier", "identifier"} else _literal(role.doc, key)
        elif child.type == "shorthand_property_identifier":
            name, value = role.doc.text(child), child
        elif child.type == "method_definition":
            key = child.child_by_field_name("name")
            name, value = role.doc.text(key), child
            prefix = role.doc.text(child)[:max(0, key.start_byte-child.start_byte)] if key is not None else ""
            if re.search(r"\b(?:get|set)\b", prefix):
                return {}, False
        else:
            return {}, False
        if not isinstance(name, str) or not name or name == "__proto__" or name in result or value is None:
            return {}, False
        result[name] = value
    return result, True


class _Engine:
    def __init__(self, snapshot: GraphSnapshot, sources: SemanticSources, rule: dict):
        self.snapshot, self.sources, self.rule = snapshot, sources, rule
        self.roles: dict[str, _Role] = {}
        self.documents: dict[str, tuple[SemanticDocument, str]] = {}
        self.bindings: dict[str, LexicalBindings] = {}
        self.relations: list[dict] = []
        self.gaps: list[dict] = []
        self.models: list[dict] = []
        self.obligations: list[dict] = []
        self.counterexamples: list[dict] = []
        self.operations = 0

    def gap(self, obligation: str, code: str, message: str, **details):
        item = {"obligation_id": obligation, "code": code, "message": message, "source_class": "unresolved", **details}
        self.gaps.append(item)
        return None

    def require(self, condition: bool, obligation: str, code: str, message: str, **details) -> bool:
        self.operations += 1
        if self.operations > _LIMIT:
            self.gap(obligation, "device_operation_budget", "source analysis operation budget exhausted")
            return False
        if not condition:
            self.gap(obligation, code, message, **details)
        return bool(condition)

    def load(self, path: str, obligation: str) -> tuple[SemanticDocument | None, str]:
        if path in self.documents:
            return self.documents[path]
        document, problems = self.sources.load(path)
        if document is not None:
            self.documents[path] = (document, "source-derived")
            return self.documents[path]
        captured = self.snapshot.input_evidence.get(path)
        if not isinstance(captured, dict) or captured.get("status") != "captured" or captured.get("error") is not None or captured.get("path") != path or not isinstance(captured.get("content"), str):
            self.gap(obligation, "device_source_unavailable", "required captured source is unavailable", file=path, problems=problems)
            return None, "unresolved"
        text, raw_hash = captured["content"], captured.get("hash", captured.get("sha256"))
        source = SourceFile(path, raw_hash or "", text, "support_input", "rust" if path.endswith(".rs") else "typescript")
        authenticated, errors = _authenticated_text(source)
        if errors:
            self.gap(obligation, "device_support_hash_invalid", "support-input bytes failed authentication", file=path, problems=errors)
            return None, "unresolved"
        try:
            document = SemanticDocument(source, source.language, self.snapshot, authenticated, None)
            if document.tree.root_node.has_error:
                self.gap(obligation, "device_support_parse_gap", "support-input CST is incomplete", file=path)
                return None, "unresolved"
            document.index_definitions(self.snapshot.config)
        except (ValueError, RuntimeError, TypeError, ImportError, AttributeError) as error:
            self.gap(obligation, "device_support_parse_failure", str(error), file=path)
            return None, "unresolved"
        self.documents[path] = (document, "support-input-derived")
        return self.documents[path]

    def role(self, name: str, obligation: str) -> _Role | None:
        if name in self.roles:
            return self.roles[name]
        selector = self.rule["roles"][name]
        document, source_class = self.load(selector["file"], obligation)
        if document is None:
            return None
        definitions = document.definitions.get(selector["symbol"], [])
        if not self.require(len(definitions) == 1, obligation, "device_role_not_unique", "locator did not select one exact lexical declaration", role=name, selector=selector, count=len(definitions)):
            return None
        definition = definitions[0]
        syntax = unwrap(definition.value) if definition.value is not None else definition.node
        role = _Role(name, document, definition, syntax, source_class)
        self.roles[name] = role
        self.bindings.setdefault(document.source.path, LexicalBindings(document))
        self.fact("role_locator", obligation, role, definition.node,
            role_name=name, locator=selector, injected_dependency_proven=False)
        return role

    def fact(self, kind: str, obligation: str, role: _Role, node: Any, **payload) -> dict:
        owner=node
        while owner is not None and owner.type not in _FUNCTIONS | {"generator_function_declaration", "generator_function", "async_block", "gen_block"}:
            owner=owner.parent
        declaration=role.doc.definition_for_ast(owner) if owner is not None else None
        owner_location=role.doc.location(owner) if owner is not None else None
        owner_symbol=declaration.symbol if declaration is not None else None
        lexical_owner=owner_symbol or (f"source:{owner.type}:{role.doc.source.path}:{owner.start_byte}:{owner.end_byte}" if owner is not None else "module:"+role.doc.module)
        record = {"kind": kind, "obligation_id": obligation, "source_class": role.source_class,
            "snapshot_id": self.snapshot.id, "source_hash": self.snapshot.source_hash,
            "extractor_version": VERSION, "model_id": MODEL_ID,
            "selected_role_owner": role.definition.symbol, "lexical_owner": lexical_owner,
            "source_owner": {"kind":owner.type if owner is not None else "module", "symbol":owner_symbol,
                "location":owner_location, "identity_basis":"nearest_actual_cst_callable_or_async_block",
                "runtime_activation_proven":False}, "location": role.doc.location(node),
            "runtime_verified": False, "manufactured_call_edge": False, **payload}
        record["relation_id"] = _digest(record)
        self.relations.append(record)
        return record

    def same(self, role: _Role, left: Any, right: Any) -> bool:
        left_root, left_keys = _member(role.doc, left)
        right_root, right_keys = _member(role.doc, right)
        if left_root is None or right_root is None or left_keys != right_keys:
            return False
        lexical = self.bindings[role.doc.source.path]
        return bool(lexical.same(left_root, right_root))

    def binding(self, role: _Role, node: Any) -> dict:
        root, keys = _member(role.doc, node)
        if root is None:
            return {"state": "unknown", "member_keys": keys}
        record = self.bindings[role.doc.source.path].resolve(root)
        return {**record, "member_keys": keys}

    def declaration(self, role: _Role, name: str) -> Any | None:
        matches = [node for node in _runtime(role.body) if node.type in {"variable_declarator", "let_declaration"}
            and role.doc.text(node.child_by_field_name("name") or node.child_by_field_name("pattern")) == name]
        return matches[0] if len(matches) == 1 else None

    def calls(self, role: _Role, spelling: str, *, nested: bool = False) -> list[Any]:
        nodes = walk(role.body) if nested else _runtime(role.body)
        return [node for node in nodes if node.type == "call_expression" and _callee(role, node) == spelling]

    def one_call(self, role: _Role, spelling: str, obligation: str, *, nested: bool = False) -> Any | None:
        calls = self.calls(role, spelling, nested=nested)
        if not self.require(len(calls) == 1, obligation, "device_call_not_unique", "one selected call site was not authenticated", role=role.name, spelling=spelling, count=len(calls)):
            return None
        return calls[0]

    def method(self, role: _Role, name: str, obligation: str) -> _Role | None:
        matches = [node for node in walk(role.body) if node.type == "method_definition" and role.doc.text(node.child_by_field_name("name")) == name]
        if not self.require(len(matches) == 1, obligation, "device_method_not_unique", "selected returned/dependency method is not unique", role=role.name, method=name, count=len(matches)):
            return None
        definition = role.doc.definition_for_ast(matches[0])
        if definition is None:
            self.gap(obligation, "device_method_owner_missing", "method has no authenticated lexical owner", role=role.name, method=name)
            return None
        return _Role(role.name+"."+name, role.doc, definition, matches[0], role.source_class)

    def parameter(self, role: _Role, index: int = 0) -> Any | None:
        parameters = role.syntax.child_by_field_name("parameters")
        items = [node for node in _children(parameters) if node.type not in {"type_annotation", "type_parameters"}]
        if index >= len(items):
            return None
        item = items[index]
        return item.child_by_field_name("pattern") or item.child_by_field_name("name") or (item if item.type == "identifier" else None)

    def returned(self, role: _Role, obligation: str) -> Any | None:
        returns = [node for node in _runtime(role.body) if node.type == "return_statement"]
        body_children = _children(role.body)
        direct = len(returns) == 1 and returns[0].parent is not None and returns[0].parent.id == role.body.id and body_children and body_children[-1].id == returns[0].id
        if not self.require(direct, obligation, "device_return_not_unique", "selected lexical body does not end with one unconditional direct return", role=role.name, count=len(returns)):
            return None
        children = _children(returns[0])
        return unwrap(children[0]) if len(children) == 1 else None

    def local_value(self, role: _Role, node: Any, obligation: str) -> Any | None:
        node = unwrap(node)
        if node is None or node.type not in {"identifier", "shorthand_property_identifier"}:
            return node
        identity = self.binding(role, node)
        if identity.get("state") != "unique" or identity.get("declaration_kind") not in {"const", "variable", "let", "variable_declaration"}:
            # Different frontend adapters encode declaration_kind differently;
            # authenticating its actual binder is decisive below.
            if identity.get("state") != "unique":
                self.gap(obligation, "device_value_binding_unknown", "operand has no unique lexical declaration", identity=identity)
                return None
        location = identity.get("declaration_location") or identity.get("binder_location") or {}
        candidates = [candidate for candidate in walk(role.doc.tree.root_node) if candidate.type == "variable_declarator"
            and candidate.start_byte <= location.get("start_byte", -1) <= candidate.end_byte
            and self.same(role, node, candidate.child_by_field_name("name"))]
        if len(candidates) != 1:
            self.gap(obligation, "device_value_initializer_unknown", "operand does not select one captured initializer", identity=identity)
            return None
        candidate = candidates[0]
        if candidate.start_byte >= node.start_byte:
            self.gap(obligation, "device_value_before_initialization", "operand initializer does not precede the selected read")
            return None
        declaration = candidate.parent
        if declaration is None or not role.doc.text(declaration).lstrip().startswith("const "):
            self.gap(obligation, "device_mutable_reaching_value", "selected alias is not an immutable lexical const")
            return None
        writes = self.bindings[role.doc.source.path].writes(identity)
        binding_writes = [write for write in writes if write.get("binding_reassignment") or write.get("kind") == "unknown_identity"]
        if binding_writes:
            self.gap(obligation, "device_alias_written", "selected const/alias has visible writes", writes=binding_writes)
            return None
        self.fact("immutable_initializer_binding", obligation, role, candidate, binding=identity)
        return unwrap(candidate.child_by_field_name("value"))

    def target(self, caller: _Role, call: Any, callee: _Role, obligation: str) -> bool:
        """Authenticate a CALLS edge or a separately typed literal-module import.

        Literal dynamic import produces a module-member binding relationship;
        it does not upgrade the captured graph's dynamic call edge.
        """
        function = unwrap(call.child_by_field_name("function")) if call is not None else None
        if function is None or function.type != "identifier":
            return self.require(False, obligation, "device_callee_identifier_required", "selected factory/function call must use a unique identifier binding")
        owner = caller.doc.definition_for_ast(next((ancestor for ancestor in _ancestors(call) if ancestor.type in _FUNCTIONS), caller.syntax))
        edge, edge_gaps = self.sources.call_binding(call, caller.doc, owner or caller.definition)
        expected = getattr(callee.definition, "graph_node_id", "")
        if edge is not None and expected and edge.target == expected:
            self.fact("captured_call_binding", obligation, caller, call, edge_id=edge.id,
                target_node_id=edge.target, target_location=callee.doc.location(callee.definition.node))
            return True
        lexical = self.bindings[caller.doc.source.path]
        binding = lexical.resolve(function)
        if binding.get("state") != "unique":
            return self.require(False, obligation, "device_import_binding_unknown", "callee has no unique captured lexical binding", binding=binding, graph_gaps=edge_gaps)
        import_nodes = [node for node in walk(caller.doc.tree.root_node) if node.type == "import_specifier"
            and lexical.same(function, node.child_by_field_name("alias") or node.child_by_field_name("name"))]
        if len(import_nodes) == 1:
            node = import_nodes[0]
            statement = next((item for item in _ancestors(node) if item.type == "import_statement"), None)
            module = _literal(caller.doc, statement.child_by_field_name("source")) if statement else None
            imported = caller.doc.text(node.child_by_field_name("name"))
            target_path = self.module_path(caller.doc.source.path, module)
            exported = callee.definition.node.parent is not None and callee.definition.node.parent.type == "export_statement"
            ok = target_path == callee.doc.source.path and imported == callee.definition.local_name and exported
            if ok:
                self.fact("literal_module_member_binding", obligation, caller, node,
                    binding=binding, import_module=module, imported_name=imported,
                    resolved_module_file=target_path, target_location=callee.doc.location(callee.definition.node),
                    relationship_kind="source_module_binding", graph_call_resolution_upgraded=False)
                return True
        # Promise.all literal imports plus object-destructuring declarations.
        for declaration in walk(caller.body):
            if declaration.type != "variable_declarator":
                continue
            name, value = declaration.child_by_field_name("name"), declaration.child_by_field_name("value")
            if name is None or name.type != "array_pattern" or value is None:
                continue
            patterns = _children(name)
            awaited = unwrap(value)
            if awaited.type != "await_expression":
                continue
            expressions = _children(awaited)
            promise_call = expressions[0] if len(expressions) == 1 else None
            if promise_call is None or _callee(caller, promise_call) != "Promise.all":
                continue
            promise_function = promise_call.child_by_field_name("function")
            promise_root, _ = _member(caller.doc, promise_function)
            promise_binding = lexical.resolve(promise_root) if promise_root is not None else {}
            if promise_binding.get("state") != "unknown" or "unresolved_lexical_binding" not in promise_binding.get("gaps", []):
                continue
            arguments = _arguments(promise_call)
            if len(arguments) != 1 or arguments[0].type != "array":
                continue
            imports = _children(arguments[0])
            if len(patterns) != len(imports) or any(item.type == "spread_element" for item in imports):
                continue
            # A named-child zip would misalign elided array pattern slots.
            if len([child for child in name.children if child.type == ","]) != len(patterns)-1:
                continue
            for pattern, imported_call in zip(patterns, imports):
                if pattern.type != "object_pattern" or imported_call.type != "call_expression" or _callee(caller, imported_call) != "import":
                    continue
                module_args = _arguments(imported_call)
                if len(module_args) != 1:
                    continue
                module = _literal(caller.doc, module_args[0])
                target_path = self.module_path(caller.doc.source.path, module)
                for binder in _children(pattern):
                    imported_name = caller.doc.text(binder.child_by_field_name("key") or binder)
                    actual_binder = binder.child_by_field_name("value") or binder
                    exported = callee.definition.node.parent is not None and callee.definition.node.parent.type == "export_statement"
                    if target_path == callee.doc.source.path and imported_name == callee.definition.local_name and exported and lexical.same(function, actual_binder):
                        self.fact("literal_dynamic_module_member_binding", obligation, caller, declaration,
                            binding=binding, import_module=module, imported_name=imported_name,
                            module_position=patterns.index(pattern), target_location=callee.doc.location(callee.definition.node),
                            relationship_kind="source_module_binding", graph_call_resolution_upgraded=False,
                            normal_import_completion_condition=True)
                        return True
        return self.require(False, obligation, "device_actual_target_unresolved", "role locator did not match the actual imported call binding", graph_gaps=edge_gaps,
            call_location=caller.doc.location(call), target_location=callee.doc.location(callee.definition.node))

    def module_path(self, caller_path: str, module: Any) -> str | None:
        if not isinstance(module, str):
            return None
        if module.startswith("."):
            components = list(PurePosixPath(caller_path).parent.parts)
            for component in module.split("/"):
                if component == ".":
                    continue
                if component == "..":
                    if not components:
                        return None
                    components.pop()
                else:
                    components.append(component)
            base = "/".join(components)
            candidates = [base, re.sub(r"\.(?:js|mjs)$", ".ts", base), re.sub(r"\.(?:js|mjs)$", ".tsx", base)]
            if not PurePosixPath(base).suffix:
                candidates.extend([base+".ts", base+"/index.ts"])
        else:
            mapping = self.snapshot.config.get("analysis", {}).get("module_aliases", {})
            candidates = []
            if isinstance(mapping, dict):
                for key, values in mapping.items():
                    if key == module:
                        candidates.extend(values if isinstance(values, list) else [values])
                    elif "*" in key:
                        before, after = key.split("*", 1)
                        if module.startswith(before) and module.endswith(after):
                            middle = module[len(before):len(module)-len(after) if after else None]
                            candidates.extend(value.replace("*", middle) for value in values if isinstance(value, str))
            normalized = []
            for candidate in candidates:
                if isinstance(candidate, str):
                    normalized.extend([candidate.removeprefix("./"), candidate.removeprefix("./")+".ts", candidate.removeprefix("./")+"/index.ts"])
            candidates = normalized
        available = {**self.sources.files, **self.snapshot.input_evidence}
        matches = sorted({candidate for candidate in candidates if candidate in available})
        return matches[0] if len(matches) == 1 else None

    def finish_obligation(self, obligation: str, start: int, **details):
        gaps = [item for item in self.gaps[start:] if item.get("obligation_id") == obligation]
        relations = [item["relation_id"] for item in self.relations if item["obligation_id"] == obligation]
        self.obligations.append({"id": obligation, "status": "supported" if not gaps else "partial" if relations else "unknown",
            "complete": not gaps, "evidence_relation_ids": relations, "analysis_gaps": gaps, "gaps": gaps, "necessary_gaps": gaps, **details})


def _ancestors(node: Any):
    while node is not None:
        yield node
        node = node.parent


def _producer(engine: _Engine):
    obligation, start = "D1", len(engine.gaps)
    role = engine.role("producer", obligation)
    if role is None:
        engine.finish_obligation(obligation, start)
        return
    kind = function_kind(role.doc, role.syntax)
    engine.require(kind.get("kind") == "ordinary_sync", obligation, "device_producer_completion_unclosed",
        "producer invocation is not an ordinary synchronous return-value construction", completion=kind)
    returned = engine.returned(role, obligation)
    fields, closed = _fields(role, returned)
    protocol = engine.rule["protocol"]
    envelope = closed and _literal(role.doc, fields.get("command")) == protocol["command"] and _literal(role.doc, fields.get("schemaVersion")) == protocol["schema_version"]
    engine.require(envelope, obligation, "device_envelope_constructor_incomplete", "producer return is not one closed versioned command envelope")
    payload, payload_closed = _fields(role, fields.get("payload"))
    spec, spec_closed = _fields(role, payload.get("spec"))
    engine.require(payload_closed and spec_closed, obligation, "device_spec_constructor_incomplete", "payload/spec contains unresolved spread, accessor, computed key, duplicate key or return")
    missing = spec_closed and protocol["wire_field"] not in spec
    engine.require(missing, obligation, "device_field_not_proven_absent", "required conditional wire field is not proven absent from the complete producer object")
    if returned is not None:
        engine.fact("closed_command_payload_construction", obligation, role, returned,
            command=_literal(role.doc, fields.get("command")), schema_version=_literal(role.doc, fields.get("schemaVersion")),
            envelope_keys=sorted(fields), payload_keys=sorted(payload), spec_keys=sorted(spec),
            wire_field=protocol["wire_field"], selected_field_presence="absent" if missing else "unknown",
            complete_literal_own_key_domain=bool(closed and payload_closed and spec_closed),
            nested_criterion_text_is_top_level_command=False)
    engine.finish_obligation(obligation, start, field_presence="absent" if missing else "unknown")


def _same_actual_parameter(engine: _Engine, role: _Role, call: Any, index: int, parameter_index: int, obligation: str):
    arguments = _arguments(call)
    parameter = engine.parameter(role, parameter_index)
    return engine.require(index < len(arguments) and parameter is not None and engine.same(role, arguments[index], parameter), obligation,
        "device_forwarding_parameter_mismatch", "actual forwarded argument is not the selected lexical parameter", role=role.name,
        call_location=role.doc.location(call) if call is not None else None)


def _actual_object(engine: _Engine, role: _Role, call: Any, obligation: str, index: int = 0):
    arguments = _arguments(call)
    fields, closed = _fields(role, arguments[index] if index < len(arguments) else None)
    engine.require(closed, obligation, "device_factory_argument_not_closed", "factory actual argument is not a closed data/method object", role=role.name)
    return fields


def _client_wiring(engine: _Engine):
    obligation, start = "D2", len(engine.gaps)
    roles = {name: engine.role(name, obligation) for name in ("producer", "port_factory", "view_model", "application", "application_route",
        "observer_factory", "cache_factory", "client_factory", "neutral_factory", "generated_transport", "http_factory")}
    if any(value is None for value in roles.values()):
        engine.finish_obligation(obligation, start)
        return
    for name in ("port_factory", "view_model", "application", "observer_factory", "cache_factory", "client_factory", "neutral_factory", "http_factory"):
        factory_kind = function_kind(roles[name].doc, roles[name].syntax)
        engine.require(factory_kind.get("kind") == "ordinary_sync", obligation,
            "device_factory_completion_unclosed", "actual injected factory does not expose an ordinary synchronous return value", role=name, completion=factory_kind)
    application, route, port, vm = (roles[key] for key in ("application", "application_route", "port_factory", "view_model"))
    raw = engine.declaration(application, "rawControlPlane")
    raw_value = unwrap(raw.child_by_field_name("value")) if raw is not None else None
    raw_rhs = raw_value.child_by_field_name("right") if raw_value is not None else None
    raw_lhs = raw_value.child_by_field_name("left") if raw_value is not None else None
    binary_operator = next((child.type for child in raw_value.children if not child.is_named and child.type == "??"), "") if raw_value is not None else ""
    root, keys = _member(application.doc, raw_lhs)
    engine.require(raw is not None and binary_operator == "??" and keys == ["controlPlane"] and engine.same(application, root, engine.parameter(application)), obligation,
        "device_default_client_selection_unknown", "production client nullish default and injected override were not derived from the actual application parameter")
    if raw_rhs is not None and raw_rhs.type == "call_expression":
        engine.target(application, raw_rhs, roles["client_factory"], obligation)
    else:
        engine.gap(obligation, "device_default_client_constructor_missing", "normal production default has no selected constructor")
    observed_call = engine.one_call(application, "observeControlPlaneClient", obligation)
    cache_call = engine.one_call(application, "createQueryCache", obligation)
    observed_fields = _actual_object(engine, application, observed_call, obligation)
    cache_fields = _actual_object(engine, application, cache_call, obligation)
    observed = engine.declaration(application, "observedControlPlane")
    cache = engine.declaration(application, "queryCache")
    control = engine.declaration(application, "controlPlane")
    observed_name = observed.child_by_field_name("name") if observed is not None else None
    cache_name = cache.child_by_field_name("name") if cache is not None else None
    raw_name = raw.child_by_field_name("name") if raw is not None else None
    engine.target(application, observed_call, roles["observer_factory"], obligation)
    engine.target(application, cache_call, roles["cache_factory"], obligation)
    engine.require(engine.same(application, observed_fields.get("client"), raw_name), obligation, "device_observer_source_mismatch", "observer actual client does not bind the normal raw client")
    cache_root, cache_keys = _member(application.doc, cache_fields.get("client"))
    engine.require(cache_keys == ["client"] and engine.same(application, cache_root, observed_name), obligation,
        "device_cache_source_mismatch", "cache actual client does not bind observer returned client property")
    control_value = control.child_by_field_name("value") if control is not None else None
    control_root, control_keys = _member(application.doc, control_value)
    engine.require(control_keys == ["client"] and engine.same(application, control_root, cache_name), obligation,
        "device_route_client_alias_mismatch", "route client alias is not the actual returned cache client")
    port_call = engine.one_call(route, "createControlPlaneClarificationPort", obligation)
    vm_call = engine.one_call(route, "createClarificationViewModel", obligation)
    engine.target(route, port_call, port, obligation)
    engine.target(route, vm_call, vm, obligation)
    port_fields = _actual_object(engine, route, port_call, obligation)
    vm_fields = _actual_object(engine, route, vm_call, obligation)
    engine.require(control is not None and engine.same(route, port_fields.get("client"), control.child_by_field_name("name")), obligation,
        "device_port_client_actual_unknown", "UI port actual client is not the production client declaration")
    engine.require(vm_fields.get("port") is not None and port_call is not None and vm_fields["port"].id == port_call.id, obligation,
        "device_vm_port_actual_unknown", "ViewModel actual port is not the selected factory return expression")
    vm_save_calls = engine.calls(vm, "options.port.save", nested=True)
    engine.require(len(vm_save_calls) == 1, obligation, "device_vm_save_binding_unknown", "ViewModel save does not have one actual options.port.save site")
    if vm_save_calls:
        call = vm_save_calls[0]
        root, keys = _member(vm.doc, call.child_by_field_name("function"))
        engine.require(keys == ["port", "save"] and engine.same(vm, root, engine.parameter(vm)), obligation,
            "device_vm_save_receiver_unknown", "save receiver is not the injected port parameter")
        engine.fact("viewmodel_injected_port_invocation", obligation, vm, call, receiver_binding=engine.binding(vm, root),
            injection_location=route.doc.location(port_call), relationship_kind="actual_argument_property_to_invocation")
    save = engine.method(port, "save", obligation)
    if save is not None:
        producer_call = engine.one_call(save, "clarificationUpdateCommand", obligation)
        command_call = engine.one_call(save, "options.client.command", obligation)
        engine.target(save, producer_call, roles["producer"], obligation)
        _same_actual_parameter(engine, save, producer_call, 0, 0, obligation)
        command_args = _arguments(command_call)
        value = engine.local_value(save, command_args[0], obligation) if command_args else None
        engine.require(value is not None and producer_call is not None and value.id == producer_call.id, obligation,
            "device_saved_command_identity_unknown", "client command operand is not the immutable actual producer return binding")
        root, keys = _member(save.doc, command_call.child_by_field_name("function") if command_call is not None else None)
        engine.require(keys == ["client", "command"] and engine.same(save, root, engine.parameter(port)), obligation,
            "device_port_client_receiver_unknown", "client command receiver does not capture the actual port options parameter")
        if command_call is not None:
            engine.fact("producer_result_to_injected_client", obligation, save, command_call,
                source_call_location=save.doc.location(producer_call), actual_client_injection=route.doc.location(port_call),
                relationship_kind="value_binding_and_receiver_property", command_value_binding=engine.binding(save, command_args[0]))
    # Both wrappers retain the actual command parameter at invocation, even if
    # their observation/cache work later rejects.  They do not manufacture a
    # new command or connect clients by method-name equality.
    for role_name, spelling in (("observer_factory", "options.client.command"), ("cache_factory", "sourceClient.command")):
        factory = roles[role_name]
        method = engine.method(factory, "command", obligation)
        if method is None:
            continue
        forwarded = engine.one_call(method, spelling, obligation)
        _same_actual_parameter(engine, method, forwarded, 0, 0, obligation)
        root, keys = _member(method.doc, forwarded.child_by_field_name("function") if forwarded is not None else None)
        if role_name == "observer_factory":
            ok = keys == ["client", "command"] and engine.same(method, root, engine.parameter(factory))
        else:
            source = engine.local_value(method, root, obligation)
            source_root, source_keys = _member(method.doc, source)
            ok = keys == ["command"] and source_keys == ["client"] and engine.same(method, source_root, engine.parameter(factory))
        engine.require(ok, obligation, "device_forwarder_receiver_unknown", "wrapper method does not use its actual injected client receiver", role=role_name)
        if forwarded is not None:
            engine.fact("injected_client_command_forwarding", obligation, method, forwarded,
                command_parameter_binding=engine.binding(method, engine.parameter(method)), factory_location=factory.doc.location(factory.syntax))
    # Community facade's injected generated transport is itself captured data.
    community = roles["client_factory"]
    neutral_call = engine.one_call(community, "createNeutralControlPlaneClient", obligation)
    engine.target(community, neutral_call, roles["neutral_factory"], obligation)
    community_args = _arguments(neutral_call)
    actual = community_args[0] if community_args else None
    parts = _children(actual)
    generated_pair = next((part for part in parts if part.type == "pair" and community.doc.text(part.child_by_field_name("key")) == "generated"), None)
    option_spread = next((part for part in parts if part.type == "spread_element"), None)
    spread_operand = _children(option_spread)[0] if option_spread is not None and len(_children(option_spread)) == 1 else None
    generated_value = generated_pair.child_by_field_name("value") if generated_pair is not None else None
    generated_binding = engine.binding(community, generated_value)
    expected_binder = roles["generated_transport"].definition.node.child_by_field_name("name")
    engine.require(actual is not None and actual.type == "object" and len(parts) == 2 and option_spread is parts[0] and generated_pair is parts[1]
        and engine.same(community, spread_operand, engine.parameter(community)) and engine.same(community, generated_value, expected_binder), obligation,
        "device_generated_transport_injection_unknown", "community constructor does not actually override generated transport after its options spread")
    if generated_pair is not None:
        engine.fact("generated_transport_actual_injection", obligation, community, generated_pair,
            transport_binding=generated_binding, target_location=roles["generated_transport"].doc.location(roles["generated_transport"].definition.node),
            ordinary_option_copy_model=True)
    neutral = roles["neutral_factory"]
    method = engine.method(neutral, "command", obligation)
    if method is not None:
        submits = engine.calls(method, "", nested=True)
        submits = [node for node in walk(method.body) if node.type == "call_expression" and _callee(method, node).endswith(".submitCommand")]
        engine.require(len(submits) == 1, obligation, "device_neutral_submit_unknown", "neutral client has no unique submitCommand forwarding expression")
        if submits:
            _same_actual_parameter(engine, method, submits[0], 0, 0, obligation)
            engine.fact("neutral_client_generated_submit", obligation, method, submits[0],
                selected_parameter_binding=engine.binding(method, engine.parameter(method)), generated_actual=community.doc.location(generated_pair))
    # Returned wrapper properties must be the actual declared methods.
    for name in ("port_factory", "observer_factory", "cache_factory", "neutral_factory"):
        factory = roles[name]
        returned = engine.returned(factory, obligation)
        if returned is not None and returned.type == "call_expression" and _callee(factory, returned) == "Object.freeze":
            args = _arguments(returned)
            returned = engine.local_value(factory, args[0], obligation) if len(args) == 1 else None
        elif returned is not None:
            returned = engine.local_value(factory, returned, obligation)
        fields, closed = _fields(factory, returned)
        engine.require(closed, obligation, "device_factory_return_record_unknown", "factory actual return is not a closed record with source-defined selected members", role=name)
        if name in {"port_factory", "neutral_factory"}:
            selected_name = "save" if name == "port_factory" else "command"
            selected_method = engine.method(factory, selected_name, obligation)
            engine.require(selected_method is not None and fields.get(selected_name) is not None and fields[selected_name].id == selected_method.syntax.id,
                obligation, "device_returned_method_identity_unknown", "selected method does not occupy the actual factory return property", role=name, property=selected_name)
        else:
            client_expression = engine.local_value(factory, fields.get("client"), obligation)
            if name == "observer_factory":
                client_fields, client_closed = _fields(factory, client_expression)
                method = engine.method(factory, "command", obligation)
                engine.require(client_closed and method is not None and client_fields.get("command") is not None and client_fields["command"].id == method.syntax.id,
                    obligation, "device_observer_returned_client_unknown", "observer returned client does not contain the actual forwarding command method")
            else:
                constructor = client_expression.child_by_field_name("constructor") if client_expression is not None else None
                args = _arguments(client_expression)
                source = engine.declaration(factory, "sourceClient")
                overrides = engine.declaration(factory, "overrides")
                override_fields, override_closed = _fields(factory, overrides.child_by_field_name("value") if overrides is not None else None)
                method = engine.method(factory, "command", obligation)
                handler_fields, handler_closed = _fields(factory, args[1] if len(args) == 2 else None)
                getter = handler_fields.get("get")
                getter_body = getter.child_by_field_name("body") if getter is not None else None
                getter_prefix = _children(getter_body)[0] if _children(getter_body) else None
                expected_get = "if(Reflect.has(overrides,property))returnReflect.get(overrides,property,overrides)"
                getter_actual = _text(factory, getter_prefix).rstrip(";") if getter_prefix is not None else ""
                native = engine.binding(factory, constructor)
                engine.require(client_expression is not None and client_expression.type == "new_expression" and factory.doc.text(constructor) == "Proxy"
                    and native.get("state") == "unknown" and len(args) == 2 and source is not None and engine.same(factory, args[0], source.child_by_field_name("name"))
                    and override_closed and method is not None and override_fields.get("command") is not None and override_fields["command"].id == method.syntax.id
                    and handler_closed and getter_actual == expected_get, obligation,
                    "device_cache_proxy_command_binding_unknown", "actual cache Proxy get handler does not select the own command override from its actual closed overrides record")
                if getter_prefix is not None:
                    engine.fact("native_proxy_own_override_member_selection", obligation, factory, getter_prefix,
                        selected_property="command", override_location=factory.doc.location(override_fields["command"]) if "command" in override_fields else None,
                        factory_returned_client_location=factory.doc.location(client_expression) if client_expression is not None else None,
                        source_client_binding=engine.binding(factory, args[0]) if args else None,
                        trusted_native_model="ordinary Proxy get with Reflect.has/get of its fresh own data-method record",
                        fallback_branch_not_selected_for_known_own_command=True)
        if returned is not None:
            engine.fact("factory_actual_return_members", obligation, factory, returned,
                factory_role=name, own_properties=sorted(fields), source_return_relationship_complete=closed)
    # The actual community generated transport contains the HTTP constructor
    # and a submit method whose source receiver is that constructor result.
    transport = roles["generated_transport"]
    http_method = engine.method(transport, "createHttpClient", obligation)
    if http_method is not None:
        constructor_call = engine.one_call(http_method, "createControlPlaneHttpClient", obligation)
        engine.target(http_method, constructor_call, roles["http_factory"], obligation)
        submit_method = engine.method(http_method, "submitCommand", obligation)
        transport_return = engine.returned(http_method, obligation)
        transport_fields, transport_closed = _fields(http_method, transport_return)
        engine.require(transport_closed and submit_method is not None and transport_fields.get("submitCommand") is not None and transport_fields["submitCommand"].id == submit_method.syntax.id,
            obligation, "device_transport_returned_submit_unknown", "actual generated transport return does not contain the selected submit method")
        if submit_method is not None:
            forward = engine.one_call(submit_method, "client.submitCommand", obligation)
            _same_actual_parameter(engine, submit_method, forward, 0, 0, obligation)
            function = forward.child_by_field_name("function") if forward is not None else None
            root, keys = _member(submit_method.doc, function)
            source_value = engine.local_value(submit_method, root, obligation)
            engine.require(keys == ["submitCommand"] and source_value is not None and constructor_call is not None and source_value.id == constructor_call.id,
                obligation, "device_transport_submit_receiver_unknown", "actual generated submit receiver does not bind the selected HTTP client constructor result")
            if forward is not None:
                engine.fact("actual_generated_transport_http_client_forwarding", obligation, submit_method, forward,
                    http_constructor_location=http_method.doc.location(constructor_call) if constructor_call is not None else None,
                    parameter_binding=engine.binding(submit_method, engine.parameter(submit_method)))
    # The neutral constructor's generated property is the actual parameter
    # injected above, and its httpClient helper calls that exact record member.
    neutral = roles["neutral_factory"]
    generated = engine.declaration(neutral, "generated")
    generated_value = generated.child_by_field_name("value") if generated is not None else None
    generated_root, generated_keys = _member(neutral.doc, generated_value)
    generated_calls = engine.calls(neutral, "generated.createHttpClient", nested=True)
    engine.require(generated_keys == ["generated"] and engine.same(neutral, generated_root, engine.parameter(neutral)) and len(generated_calls) == 1,
        obligation, "device_neutral_generated_actual_unknown", "neutral HTTP helper does not use the actual injected generated transport parameter member")
    if generated_calls:
        engine.fact("neutral_actual_generated_factory_member", obligation, neutral, generated_calls[0],
            injected_generated_location=community.doc.location(generated_pair) if generated_pair is not None else None,
            generated_parameter_binding=engine.binding(neutral, generated_root))
    engine.finish_obligation(obligation, start, scope="normal no-controlPlane-override production client and clarification save path",
        override_scope="injected controlPlane clients are excluded and explicitly retained as counterexamples")


def _protocol(engine: _Engine):
    obligation, start = "D3", len(engine.gaps)
    protocol = engine.rule["protocol"]
    rust, rust_class = engine.load(protocol["rust_file"], obligation)
    domain, domain_class = engine.load(protocol["rust_domain_file"], obligation)
    typescript, typescript_class = engine.load(protocol["typescript_file"], obligation)
    http = engine.role("http_factory", obligation)
    dispatcher = engine.role("server_dispatcher", obligation)
    family = engine.role("server_family", obligation)
    app = engine.role("server_application_dispatcher", obligation)
    delivery = engine.role("server_delivery_dispatcher", obligation)
    router = engine.role("server_router", obligation)
    http_command = engine.role("server_http_command", obligation)
    http_parser = engine.role("server_http_parser", obligation)
    if any(value is None for value in (rust, domain, typescript, http, dispatcher, family, app, delivery, router, http_command, http_parser)):
        engine.finish_obligation(obligation, start)
        return
    spec = _item(rust, protocol["spec_type"], {"struct_item"})
    command = _item(rust, protocol["command_type"], {"struct_item"})
    payload = _item(rust, protocol["payload_type"], {"struct_item"})
    discriminator = _item(rust, protocol["command_discriminator_type"], {"enum_item"})
    requests = _item(rust, protocol["request_type"], {"enum_item"})
    engine.require(all(item is not None for item in (spec, command, payload, discriminator, requests)), obligation,
        "device_protocol_declarations_missing", "protocol locators did not resolve unique captured generated Rust declarations")
    if not all(item is not None for item in (spec, command, payload, discriminator, requests)):
        engine.finish_obligation(obligation, start)
        return
    ts_spec = _typescript_type(typescript, protocol["spec_type"])
    ts_command = _typescript_type(typescript, protocol["command_type"])
    ts_payload = _typescript_type(typescript, protocol["payload_type"])
    ts_spec_fields, ts_command_fields, ts_payload_fields = (_typescript_fields(typescript, declaration) for declaration in (ts_spec, ts_command, ts_payload))
    ts_field = ts_spec_fields.get(protocol["wire_field"])
    engine.require(ts_field is not None and ts_field["optional"] and ts_field["type"] == "string"
        and ts_command_fields.get("payload", {}).get("type") == protocol["payload_type"]
        and ts_payload_fields.get("spec", {}).get("type") == protocol["spec_type"]
        and ts_command_fields.get("command", {}).get("type") == '"'+protocol["command"]+'"', obligation,
        "device_typescript_protocol_identity_unclosed", "captured generated TypeScript command/payload/spec path does not match the selected wire record and optional string field")
    if ts_field is not None:
        ts_role = _role_for_document("typescript_protocol_spec", typescript, typescript_class, ts_spec)
        engine.fact("generated_typescript_wire_record_path", obligation, ts_role, ts_field["syntax"],
            command_type=protocol["command_type"], payload_type=protocol["payload_type"], spec_type=protocol["spec_type"],
            wire_field=protocol["wire_field"], field_optional=ts_field["optional"], relationship_kind="protocol_type_declaration")
    spec_fields, command_fields, payload_fields = (_rust_fields(rust, item) for item in (spec, command, payload))
    version_type = command_fields.get("schema_version", {}).get("type", "")
    version_parts = version_type.split("::")
    crate_root = engine.snapshot.config.get("analysis", {}).get("rust_crates", {}).get(version_parts[0]) if len(version_parts) == 2 else None
    version_enum = _item(domain, protocol["schema_version_type"], {"enum_item"})
    version_variants = _rust_variants(domain, version_enum)
    version_closed = bool(crate_root and protocol["rust_domain_file"].startswith(crate_root+"/")
        and version_parts[-1] == protocol["schema_version_type"] and len(version_variants) == 1
        and version_variants[0]["name"] == protocol["schema_version_variant"] and version_variants[0]["wire_name"] == protocol["schema_version"])
    engine.require(version_closed, obligation, "device_schema_version_record_identity_unclosed", "API qualified schema-version type does not map to the actual generated singleton wire-version enum")
    version_attrs = [domain.text(attr) for attr in _attributes(version_enum)] if version_enum is not None else []
    derive_match = re.fullmatch(r"#\[derive\(([^\]]+)\)\]", version_attrs[0]) if len(version_attrs) == 1 else None
    version_derives = {name.strip() for name in derive_match.group(1).split(",")} if derive_match else set()
    safe_derives = {"Debug", "Clone", "PartialEq", "Eq", "Hash", "serde::Serialize", "serde::Deserialize"}
    version_helpers_closed = bool(version_enum is not None and version_enum.child_by_field_name("type_parameters") is None
        and {"serde::Serialize", "serde::Deserialize"} <= version_derives <= safe_derives
        and len(version_variants) == 1 and version_variants[0]["type"] is None
        and len(version_variants[0]["attributes"]) == 1)
    engine.require(version_helpers_closed, obligation, "device_schema_version_derive_unclosed", "version enum has unsupported conditional/helper/custom-deserializer or non-unit shape")
    domain_provider = None
    if crate_root:
        try:
            domain_provider = _declared_provider(engine.snapshot.input_evidence, crate_root, protocol["serde_profile"]["workspace_manifest"], protocol["rust_domain_file"])
        except ValueError as error:
            engine.gap(obligation, "device_schema_version_provider_unverified", str(error))
    else:
        engine.gap(obligation, "device_schema_version_crate_unknown", "version type's actual declared crate alias is unavailable")
    ts_version = _typescript_type(typescript, protocol["schema_version_type"])
    ts_version_value = ts_version.child_by_field_name("value") if ts_version is not None else None
    ts_version_text = typescript.text(ts_version_value)
    engine.require(ts_version_text == '"'+protocol["schema_version"]+'"', obligation,
        "device_typescript_version_unclosed", "generated TypeScript version does not equal the produced wire version")
    if version_enum is not None:
        version_role = _role_for_document("protocol_schema_version", domain, domain_class, version_enum)
        engine.fact("wire_schema_version_enum_identity", obligation, version_role, version_enum,
            qualified_api_field_type=version_type, api_schema_field_location=rust.location(command_fields["schema_version"]["syntax"]),
            wire_version=protocol["schema_version"], enum_variant=protocol["schema_version_variant"], provider=domain_provider,
            typescript_version_location=typescript.location(ts_version) if ts_version is not None else None,
            relationship_kind="protocol_record_version_mapping")
    selected = spec_fields.get(protocol["rust_field"])
    acceptable = selected is not None and selected["wire_name"] == protocol["wire_field"] and re.sub(r"\s+", "", selected["type"]) == "Option<String>"
    allowed = {f'#[serde(rename = "{protocol["wire_field"]}")]', '#[serde(default, skip_serializing_if = "Option::is_none")]'}
    acceptable = acceptable and {re.sub(r"\s+", "", text) for text in selected["attribute_text"]} == {re.sub(r"\s+", "", text) for text in allowed}
    engine.require(acceptable, obligation, "device_option_mapping_unclosed", "camel/snake mapping, Option<String> default and skip-none attributes are not exact source facts")
    profile = protocol["serde_profile"]
    declared_profiles = engine.snapshot.config.get("analysis", {}).get("rust_helper_profiles", [])
    engine.require(profile in declared_profiles, obligation, "device_serde_profile_not_enabled", "selected API crate serde profile is not enabled by captured policy")
    attrs = [rust.text(attr) for attr in _attributes(spec)]
    shadowed = {rust.text(node.child_by_field_name("name")) for node in rust.tree.root_node.named_children if node.type in {"mod_item", "struct_item", "enum_item", "type_item", "macro_definition"}}
    shadows = shadowed & {"serde", "Option", "String"}
    for node in rust.tree.root_node.named_children:
        if node.type == "use_declaration" and re.search(r"\b(?:serde|Option|String)\b", rust.text(node)):
            shadows.update({"serde", "Option", "String"})
    engine.require(not shadows, obligation, "device_protocol_builtin_shadow", "generated Option/String/serde names are not authentic supported standard providers", shadowed_names=sorted(shadows))
    helper = classify_helpers(attrs, profile_id=profile["id"], support_inputs=engine.snapshot.input_evidence,
        crate_root=profile["crate_root"], workspace_manifest=profile["workspace_manifest"],
        item_file=protocol["rust_file"], item_kind="struct", shadowed_names=shadows,
        bindings_complete=True, source_complete=not rust.tree.root_node.has_error,
        generic=spec.child_by_field_name("type_parameters") is not None,
        conditional=any(re.search(r"\bcfg(?:_attr)?\b", attr) for attr in attrs), macro_scope_unknown=False)
    engine.require(bool(helper.get("accepted")), obligation, "device_serde_provider_unverified", "serde derive/helper provider could not be authenticated", helper=helper)
    model = {"model_id": MODEL_ID, "source_class": "trusted-model", "version": VERSION,
        "serde_helper_version": RUST_HELPER_VERSION, "provider": helper, "schema_version_provider": domain_provider,
        "applicability": {"accepted": bool(helper.get("accepted") and acceptable and not shadows and version_closed and version_helpers_closed and domain_provider),
            "ordinary_plain_json_records": True, "native_json_binding": "checked at selected serializer below",
            "source_check": rust.location(spec)},
        "rules": ["absent plain-object own key is absent from native JSON object serialization",
            "authenticated serde rename maps the selected wire field to the selected Rust field",
            "default Option<String> maps an absent wire key to None",
            "skip_serializing_if Option::is_none omits None when payload is reserialized",
            "None.filter remains None; ok_or_else produces Err and ? exits before criterion use"],
        "macro_expansion_performed": False, "runtime_verified": False}
    model["model_record_id"] = _digest(model)
    engine.models.append(model)
    if selected is not None:
        role = _role_for_document("protocol_spec", rust, rust_class, spec)
        engine.fact("wire_record_field_mapping_and_default", obligation, role, selected["syntax"],
            wire_field=selected["wire_name"], rust_field=protocol["rust_field"], rust_type=selected["type"],
            source_attributes=selected["attribute_text"], absent_wire_value="None", model_record_id=model["model_record_id"],
            relationship_kind="protocol_record_mapping", graph_call_edge_created=False)
    expected_type_relations = ((command_fields, "payload", protocol["payload_type"]),
        (command_fields, "command", protocol["command_discriminator_type"]), (payload_fields, "spec", protocol["spec_type"]))
    engine.require(all(name in fields and fields[name]["type"] == expected and fields[name]["wire_name"] == name
        for fields, name, expected in expected_type_relations), obligation, "device_protocol_record_path_unclosed", "command.payload.spec path does not refer to the selected generated record declarations")
    discriminators = _rust_variants(rust, discriminator)
    engine.require(len(discriminators) == 1 and discriminators[0]["name"] == protocol["command_enum_variant"] and discriminators[0]["wire_name"] == protocol["command"], obligation,
        "device_command_discriminator_mismatch", "generated command discriminator does not select the producer wire command")
    variants = _rust_variants(rust, requests)
    selected_variants = [variant for variant in variants if variant["name"] == protocol["command_request_variant"] and variant["type"] == protocol["command_type"]]
    request_attrs = [rust.text(attr) for attr in _attributes(requests)]
    engine.require(len(selected_variants) == 1 and any(re.sub(r"\s+", "", attr) == "#[serde(untagged)]" for attr in request_attrs), obligation,
        "device_request_dispatch_variant_unclosed", "untagged generated request does not contain the selected typed command variant")
    # All candidate command variants must have an authenticated, distinct
    # singleton command discriminator; an earlier permissive variant would
    # invalidate selection of this Rust command.
    command_values = []
    for variant in variants:
        struct = _item(rust, variant["type"] or "", {"struct_item"})
        fields = _rust_fields(rust, struct)
        command_type = fields.get("command", {}).get("type")
        enum = _item(rust, command_type or "", {"enum_item"})
        names = _rust_variants(rust, enum)
        if len(names) != 1 or names[0]["wire_name"] is None:
            engine.gap(obligation, "device_untagged_candidate_unknown", "request variant does not have one source-authenticated command discriminator", variant=variant["name"])
        else:
            command_values.append(names[0]["wire_name"])
    engine.require(len(command_values) == len(variants) and len(set(command_values)) == len(command_values), obligation,
        "device_untagged_ambiguous_command", "generated request variants do not have distinct complete discriminators")
    schema_declarations = [node for node in walk(http.doc.tree.root_node) if node.type == "variable_declarator" and http.doc.text(node.child_by_field_name("name")) == "CONTROL_PLANE_RUNTIME_SCHEMAS"]
    schemas = None
    if len(schema_declarations) == 1:
        literal = schema_declarations[0].child_by_field_name("value")
        try:
            schemas = json.loads(http.doc.text(literal))
        except (json.JSONDecodeError, TypeError):
            pass
    spec_schema = schemas.get(protocol["spec_type"], {}) if isinstance(schemas, dict) else {}
    field_schema = spec_schema.get("properties", {}).get(protocol["wire_field"])
    engine.require(isinstance(field_schema, dict) and field_schema.get("type") == "string" and protocol["wire_field"] not in spec_schema.get("required", []), obligation,
        "device_wire_schema_default_unverified", "captured generated JSON schema does not permit the missing conditional string field")
    if schemas is not None:
        engine.fact("generated_wire_schema_optional_field", obligation, http, schema_declarations[0],
            schema_name=protocol["spec_type"], wire_field=protocol["wire_field"], optional=protocol["wire_field"] not in spec_schema.get("required", []),
            model_record_id=model["model_record_id"], captured_schema_count=len(schemas), all_schema_data_retained_by_source_pointer=True)
    submit = engine.method(http, "submitCommand", obligation)
    send_nodes = [node for node in walk(http.syntax) if node.type == "function_declaration" and http.doc.text(node.child_by_field_name("name")) == "send"]
    send = None
    if len(send_nodes) == 1:
        definition = http.doc.definition_for_ast(send_nodes[0])
        send = _Role("http_factory.send", http.doc, definition, send_nodes[0], http.source_class) if definition else None
    engine.require(submit is not None and send is not None, obligation, "device_http_send_binding_missing", "generated HTTP client command/send bodies are not uniquely captured")
    command_path = None
    if submit is not None and send is not None:
        send_call = engine.one_call(submit, "send", obligation)
        _same_actual_parameter(engine, submit, send_call, 1, 0, obligation)
        send_args = _arguments(send_call)
        path_value = engine.local_value(submit, send_args[0], obligation) if send_args else None
        command_path = _literal(submit.doc, path_value)
        serializer = engine.one_call(send, "JSON.stringify", obligation)
        _same_actual_parameter(engine, send, serializer, 0, 1, obligation)
        lexical = engine.bindings[send.doc.source.path]
        serializer_root = serializer.child_by_field_name("function").child_by_field_name("object") if serializer is not None else None
        serializer_binding = lexical.resolve(serializer_root) if serializer_root is not None else {}
        engine.require(serializer_binding.get("state") == "unknown" and "unresolved_lexical_binding" in serializer_binding.get("gaps", []), obligation,
            "device_json_native_binding_unverified", "JSON serializer may be shadowed by a captured local declaration", binding=serializer_binding)
        init = engine.declaration(send, "init")
        init_fields, init_closed = _fields(send, init.child_by_field_name("value") if init else None)
        engine.require(init_closed and _literal(send.doc, init_fields.get("method")) == "POST", obligation,
            "device_http_post_init_unknown", "actual generated HTTP init is not a closed POST object")
        body_root, body_keys = _member(send.doc, init_fields.get("body"))
        serialized_assignment = [node for node in walk(send.body) if node.type == "assignment_expression"
            and engine.same(send, node.child_by_field_name("left"), body_root)
            and _strip(node.child_by_field_name("right")) is not None and serializer is not None
            and _strip(node.child_by_field_name("right")).id == serializer.id]
        engine.require(not body_keys and len(serialized_assignment) == 1, obligation,
            "device_http_serialized_body_unknown", "actual POST body does not use the selected serializer result binding")
        fetch_call = engine.one_call(send, "fetchImplementation", obligation)
        fetch_args = _arguments(fetch_call)
        engine.require(len(fetch_args) == 2 and init is not None and engine.same(send, fetch_args[1], init.child_by_field_name("name")), obligation,
            "device_http_init_transport_unknown", "HTTP transport operand is not the actual selected init record")
        engine.fact("command_json_http_record_transport", obligation, send, serializer,
            command_path=command_path, method="POST", request_parameter_binding=engine.binding(send, engine.parameter(send, 1)),
            field_presence_from_producer="absent", serialized_presence="absent", model_record_id=model["model_record_id"],
            relationship_kind="message_record_transport", delivery_success_not_verified=True)
    routes = [node for node in walk(router.body) if node.type == "call_expression" and _callee(router, node).endswith(".route")]
    matching_routes = []
    for call in routes:
        args = _arguments(call)
        if len(args) == 2 and _literal(router.doc, args[0]) == command_path:
            posts = [child for child in walk(args[1]) if child.type == "call_expression" and _callee(router, child) == "post"]
            if len(posts) == 1 and len(_arguments(posts[0])) == 1 and router.doc.text(_arguments(posts[0])[0]) == http_command.definition.local_name:
                matching_routes.append(call)
    engine.require(len(matching_routes) == 1 and command_path is not None, obligation,
        "device_http_route_mapping_unknown", "actual server POST route does not select the source client command path and handler")
    parser_call = engine.one_call(http_command, "parse_json_body", obligation)
    api_call = engine.one_call(http_command, "state.api.command", obligation)
    api_args = _arguments(api_call)
    engine.require(len(api_args) == 2 and http_command.doc.text(api_args[1]) == "body", obligation,
        "device_server_body_dispatch_unknown", "server command dispatcher does not consume the parsed request body binding")
    parse_calls = engine.calls(http_parser, "serde_json::from_slice")
    engine.require(len(parse_calls) == 1, obligation, "device_server_json_decode_unknown", "server request parser does not use one captured serde_json decoder")
    version_constants = [node for node in http_parser.doc.tree.root_node.named_children if node.type == "const_item"
        and http_parser.doc.text(node.child_by_field_name("name")) == "SUPPORTED_SCHEMA_VERSION"]
    constant_value = version_constants[0].child_by_field_name("value") if len(version_constants) == 1 else None
    version_guards = [node for node in _runtime(http_parser.body) if node.type == "if_expression"
        and _text(http_parser, node.child_by_field_name("condition")) == 'value.get("schemaVersion").and_then(Value::as_str)!=Some(SUPPORTED_SCHEMA_VERSION)']
    engine.require(_literal(http_parser.doc, constant_value) == protocol["schema_version"] and len(version_guards) == 1
        and any(node.type == "return_expression" and _text(http_parser, node).startswith("returnErr(") for node in walk(version_guards[0].child_by_field_name("consequence"))), obligation,
        "device_server_protocol_version_guard_unclosed", "HTTP parser does not derive a rejecting guard for this captured supported version")
    if version_guards:
        engine.fact("http_wire_version_rejection_guard", obligation, http_parser, version_guards[0],
            supported_wire_version=protocol["schema_version"], supported_constant_location=http_parser.doc.location(version_constants[0]) if version_constants else None,
            before_typed_dispatch=True, actual_deployment_or_request_not_verified=True)
    if parser_call is not None and api_call is not None:
        engine.fact("server_json_body_to_dispatcher", obligation, http_command, api_call,
            parser_location=http_command.doc.location(parser_call), decoder_location=http_parser.doc.location(parse_calls[0]) if parse_calls else None,
            message_path=command_path, relationship_kind="message_record_decode_and_dispatch")
    typed = engine.declaration(dispatcher, "typed")
    typed_call = _strip(typed.child_by_field_name("value")) if typed is not None else None
    typed_type = dispatcher.doc.text(typed.child_by_field_name("type")) if typed is not None else ""
    engine.require(typed_call is not None and _callee(dispatcher, typed_call) == "decode" and typed_type == protocol["request_type"], obligation,
        "device_rust_typed_decoder_unknown", "generated dispatcher does not decode the source request into selected Rust request type")
    application_call = engine.one_call(dispatcher, "self.application.command", obligation)
    application_args = _arguments(application_call)
    engine.require(len(application_args) == 3 and typed is not None and dispatcher.doc.text(application_args[2]) == dispatcher.doc.text(typed.child_by_field_name("pattern")), obligation,
        "device_rust_dispatch_operand_unknown", "typed source request is not the actual dispatcher command operand")
    # These are source match arms, not fabricated cross-language CALLS.
    family_arms = [node for node in walk(family.body) if node.type == "match_arm"
        and re.search(r"\b"+re.escape(protocol["command_enum_variant"])+r"\b", family.doc.text(node.child_by_field_name("pattern")))
        and _text(family, node.child_by_field_name("value")) == "Self::Delivery"]
    app_arms = [node for node in walk(app.body) if node.type == "match_arm"
        and _text(app, node.child_by_field_name("pattern")) == "CommandFamily::Delivery"
        and "self.delivery_command(request)" == _text(app, node.child_by_field_name("value"))]
    delivery_arms = [node for node in walk(delivery.body) if node.type == "match_arm"
        and _text(delivery, node.child_by_field_name("pattern")) == protocol["request_type"]+"::"+protocol["command_request_variant"]+"(command)"
        and any(child.type == "call_expression" and _callee(delivery, child) == "state.control_plane.delivery_update_spec" for child in walk(node))]
    engine.require(len(family_arms) == len(app_arms) == len(delivery_arms) == 1, obligation,
        "device_backend_dispatch_arms_unclosed", "command discriminator/family/typed-request arms do not derive the selected delivery update route")
    for role, arms, kind in ((family, family_arms, "command_family_mapping"), (app, app_arms, "typed_application_family_dispatch"), (delivery, delivery_arms, "typed_command_update_dispatch")):
        if arms:
            engine.fact(kind, obligation, role, arms[0], command=protocol["command"],
                typed_request_variant=protocol["command_request_variant"], relationship_kind="typed_dispatch_relation")
    engine.finish_obligation(obligation, start, wire_field=protocol["wire_field"], rust_field=protocol["rust_field"], absent_wire_value="None",
        transport_model="ordinary successful JSON message along authenticated command endpoint; no network execution")


def _authority(engine: _Engine):
    obligation, start = "D4", len(engine.gaps)
    names = ("server_update", "server_map", "server_resolve", "server_take", "authority_installer",
        "authority_specification", "authority_decoder", "authority_device_target")
    roles = {name: engine.role(name, obligation) for name in names}
    if any(value is None for value in roles.values()):
        engine.finish_obligation(obligation, start)
        return
    update, mapper, resolve, take, installer, authority, decoder, device = (roles[key] for key in names)
    protocol = engine.rule["protocol"]
    mapped = engine.declaration(update, "mapped")
    map_call = _strip(mapped.child_by_field_name("value")) if mapped is not None else None
    map_args = _arguments(map_call)
    engine.require(map_call is not None and _callee(update, map_call) == "map_command" and len(map_args) == 7
        and _text(update, map_args[1]) == "CommandName::"+protocol["command_enum_variant"]
        and _text(update, map_args[3]) == "&command.payload", obligation,
        "device_authority_command_mapping_unknown", "delivery update does not map its actual typed command/payload to the authority envelope")
    mapper_serializers = engine.calls(mapper, "serde_json::to_value")
    engine.require(len(mapper_serializers) == 1 and len(_arguments(mapper_serializers[0])) == 1
        and _text(mapper, _arguments(mapper_serializers[0])[0]) == "payload", obligation,
        "device_authority_payload_reserialize_unknown", "map_command does not serialize its actual generic payload parameter")
    mapper_version_guards = [node for node in _runtime(mapper.body) if node.type == "if_expression"
        and _text(mapper, node.child_by_field_name("condition")) == "schema_version!=&SchemaVersion::"+protocol["schema_version_variant"]]
    engine.require(len(mapper_version_guards) == 1 and any(node.type == "return_expression" and _text(mapper, node).startswith("returnErr(")
        for node in walk(mapper_version_guards[0].child_by_field_name("consequence"))), obligation,
        "device_authority_version_guard_unclosed", "mapped command does not enforce the selected source version before payload transport")
    if mapper_version_guards:
        engine.fact("typed_authority_version_guard", obligation, mapper, mapper_version_guards[0],
            required_enum_variant=protocol["schema_version_variant"], wire_version=protocol["schema_version"], rejects_before_payload_mapping=True)
    resolve_call = engine.one_call(update, "self.resolve_specification_authority", obligation)
    resolve_args = _arguments(resolve_call)
    engine.require(len(resolve_args) == 2 and _text(update, resolve_args[0]) == "&mapped" and _text(update, resolve_args[1]) == "Some(&current)", obligation,
        "device_update_authority_actual_unknown", "update does not pass its mapped command and current delivery to the authority resolver")
    take_decl = engine.declaration(resolve, "port")
    take_call = _strip(take_decl.child_by_field_name("value")) if take_decl is not None else None
    specification_call = engine.one_call(resolve, "port.specification", obligation)
    specification_args = _arguments(specification_call)
    engine.require(take_call is not None and _callee(resolve, take_call) == "self.take_delivery_authority" and len(specification_args) == 1
        and _text(resolve, specification_args[0]) == "DeliveryAuthorityRequest{command,delivery}", obligation,
        "device_authority_receiver_source_unknown", "specification invocation does not use the actual taken installed authority and command request record")
    take_calls = engine.calls(take, "self.delivery_authority.take")
    engine.require(len(take_calls) == 1, obligation, "device_authority_take_field_unknown", "authority receiver does not originate from the installed authority field")
    authority_decl = engine.declaration(installer, "authority")
    authority_open = _strip(authority_decl.child_by_field_name("value")) if authority_decl is not None else None
    authority_type = authority.definition.symbol.split(".")[0]
    concrete_match = re.match(r"<([^ ]+) as [^>]+>", authority_type)
    concrete_name = concrete_match.group(1) if concrete_match else authority_type
    assignments = [node for node in _runtime(installer.body) if node.type == "assignment_expression"
        and _text(installer, node.child_by_field_name("left")) == "self.delivery_authority"]
    engine.require(authority_open is not None and _callee(installer, authority_open) == concrete_name+"::open" and len(assignments) == 1
        and _text(installer, assignments[0].child_by_field_name("right")) == "Some(Box::new(authority))", obligation,
        "device_authority_actual_installation_unknown", "installed authority is not the selected concrete constructor result boxed into the consumed field")
    if assignments:
        engine.fact("concrete_authority_port_installation", obligation, installer, assignments[0],
            concrete_type=concrete_name, constructor_location=installer.doc.location(authority_open) if authority_open is not None else None,
            field="delivery_authority", resolver_location=resolve.doc.location(specification_call) if specification_call is not None else None,
            relationship_kind="concrete_object_to_owned_trait_port_field")
    spec_decl = engine.declaration(authority, "spec")
    spec_value = spec_decl.child_by_field_name("value") if spec_decl is not None else None
    arms = [node for node in walk(spec_value) if node.type == "match_arm"] if spec_value is not None else []
    selected_arms = [arm for arm in arms if _text(authority, arm.child_by_field_name("pattern")) == "CommandName::"+protocol["command_enum_variant"]]
    if len(selected_arms) == 1:
        arm = selected_arms[0]
        payload_decls = [node for node in walk(arm) if node.type == "let_declaration" and authority.doc.text(node.child_by_field_name("pattern")) == "payload"]
        payload_decl = payload_decls[0] if len(payload_decls) == 1 else None
        payload_call = _strip(payload_decl.child_by_field_name("value")) if payload_decl is not None else None
        body = arm.child_by_field_name("value")
        values = _children(body)
        engine.require(payload_decl is not None and authority.doc.text(payload_decl.child_by_field_name("type")) == protocol["payload_type"]
            and payload_call is not None and _callee(authority, payload_call) == "decode_payload"
            and len(_arguments(payload_call)) == 1 and _text(authority, _arguments(payload_call)[0]) == "request.command()"
            and values and _text(authority, values[-1]) == "payload.spec", obligation,
            "device_authority_spec_operand_unclosed", "authority does not select the decoded update payload's actual spec field")
        engine.fact("typed_update_payload_to_authority_spec", obligation, authority, arm,
            command=protocol["command"], payload_type=protocol["payload_type"], spec_field="spec", relationship_kind="typed_record_projection")
    else:
        engine.gap(obligation, "device_authority_command_arm_missing", "authority has no unique selected update command match arm")
    decode_calls = engine.calls(decoder, "serde_json::from_value")
    canonical_calls = engine.calls(decoder, "serde_json::to_value")
    engine.require(len(decode_calls) == len(canonical_calls) == 1 and len(_arguments(decode_calls[0])) == 1
        and _text(decoder, _arguments(decode_calls[0])[0]) == "command.payload.clone()", obligation,
        "device_authority_decoder_unclosed", "authority decoder is not the actual command payload JSON decoder/canonicality check")
    device_decl = engine.declaration(authority, "device")
    device_call = _strip(device_decl.child_by_field_name("value")) if device_decl is not None else None
    engine.require(device_call is not None and _callee(authority, device_call) == "self.device_target" and len(_arguments(device_call)) == 1
        and _text(authority, _arguments(device_call)[0]) == "spec.source_product_session_id.as_ref()", obligation,
        "device_target_source_unclosed", "Device target condition does not originate from the source spec product-session field")
    conditionals = [node for node in _runtime(authority.body) if node.type == "if_expression"
        and _text(authority, node.child_by_field_name("condition")) == "letSome(device)=device"]
    engine.require(len(conditionals) == 1, obligation, "device_condition_region_unclosed", "authority Device branch is not a unique if-let Some of the actual target result")
    if conditionals:
        branch = conditionals[0].child_by_field_name("consequence")
        commands = [node for node in _runtime(branch) if node.type == "let_declaration" and authority.doc.text(node.child_by_field_name("pattern")) == "command"]
        command_decl = commands[0] if len(commands) == 1 else None
        command_value = command_decl.child_by_field_name("value") if command_decl is not None else None
        outer = _strip(command_value)
        filter_calls = [node for node in walk(command_value) if node.type == "call_expression" and _callee(authority, node).endswith(".filter")] if command_value is not None else []
        ok_calls = [node for node in walk(command_value) if node.type == "call_expression" and _callee(authority, node).endswith(".ok_or_else")] if command_value is not None else []
        filter_call = filter_calls[0] if len(filter_calls) == 1 else None
        filter_function = filter_call.child_by_field_name("function") if filter_call is not None else None
        filter_receiver = filter_function.child_by_field_name("value") if filter_function is not None else None
        predicate = _arguments(filter_call)
        predicate_text = _text(authority, predicate[0]) if len(predicate) == 1 else ""
        engine.require(command_decl is not None and command_value.type == "try_expression" and len(ok_calls) == 1
            and outer is not None and outer.id == ok_calls[0].id
            and _text(authority, filter_receiver) == "spec."+protocol["rust_field"]
            and predicate_text == "|command|!command.trim().is_empty()", obligation,
            "device_nonempty_option_guard_unclosed", "Device branch does not derive Option.filter(nonblank).ok_or_else(...)? from the selected spec field")
        if command_decl is not None:
            uses = [node for node in _runtime(authority.body) if node.type == "field_initializer" and authority.doc.text(node.child_by_field_name("field")) == "criterion_verification_methods"]
            engine.require(len(uses) == 1 and command_decl.end_byte < uses[0].start_byte, obligation,
                "device_guard_before_use_unknown", "conditional rejection does not precede criterion verification method construction")
            engine.fact("device_nonempty_option_rejection_guard", obligation, authority, command_decl,
                selected_rust_field=protocol["rust_field"], operand_state_from_wire_default="None",
                option_filter_rule="None remains None; present blank strings are removed",
                guarded_completion="Err propagated by ? before criterion verification methods", device_condition_location=authority.doc.location(conditionals[0]),
                criterion_use_location=authority.doc.location(uses[0]) if uses else None, relationship_kind="conditional_guard_completion",
                source_condition="resolved source-product-session Device target is Some and previous guards permit reaching this branch")
    if resolve_call is not None:
        engine.fact("update_mapped_command_to_authority", obligation, update, resolve_call,
            mapped_constructor_location=update.doc.location(map_call) if map_call is not None else None,
            target_resolver_location=resolve.doc.location(resolve.syntax), before_commit=any(node.type == "call_expression" and _callee(update, node).endswith(".commit_delivery_command") and node.start_byte > resolve_call.start_byte for node in walk(update.body)))
    engine.finish_obligation(obligation, start, conditional_outcome="missing selected field reaches Device Option None rejection before criterion use and commit")


def _refutations(engine: _Engine):
    obligation, start = "D5", len(engine.gaps)
    names = ("authority_specification", "authority_device_target", "chat_producer", "producer", "server_update", "server_dispatcher", "port_factory", "criterion_values")
    roles = {name: engine.role(name, obligation) for name in names}
    if any(value is None for value in roles.values()):
        engine.finish_obligation(obligation, start)
        return
    authority, device, chat, producer, update, dispatcher, port, criterion_values = (roles[name] for name in names)
    conditionals = [node for node in _runtime(authority.body) if node.type == "if_expression"
        and _text(authority, node.child_by_field_name("condition")) == "letSome(device)=device"]
    alternative = conditionals[0].child_by_field_name("alternative") if len(conditionals) == 1 else None
    selectors = [node for node in walk(alternative) if node.type == "call_expression" and _callee(authority, node) == "select_verification_command"] if alternative is not None else []
    engine.require(len(selectors) == 1, obligation, "device_nondevice_refutation_missing", "non-Device branch does not have the actual repository verification-command fallback")
    if selectors:
        record = engine.fact("nondevice_repository_command_fallback", obligation, authority, selectors[0],
            conditional_refutation="without a resolved Device target, missing top-level command is not this rejection", repository_fallback_can_itself_fail=True)
        engine.counterexamples.append({"kind": "non_device_repository", "status": "supported", "source_class": record["source_class"], "relation_id": record["relation_id"], "scope": "does not establish every non-Device save succeeds"})
    none_returns = [node for node in _runtime(device.body) if node.type == "return_expression" and _text(device, node).startswith("returnOk(None)")]
    some_tail = [node for node in _runtime(device.body) if node.type == "call_expression" and _callee(device, node) == "Some"]
    gate = engine.calls(device, "crate::device_session_gate::authorize_device_session")
    engine.require(len(none_returns) >= 2 and len(some_tail) >= 1 and len(gate) == 1, obligation,
        "device_activity_authorization_refutation_missing", "source-session/no-grant fallback and authorized Device target construction are not fully located")
    if gate:
        record = engine.fact("device_target_environment_and_authorization", obligation, device, gate[0],
            source_session_missing_returns_none=bool(none_returns), launch_grant_required=True, authorization_failure_prevents_device_target=True, target_activity_not_observed=True)
        engine.counterexamples.append({"kind": "device_target_not_active_or_not_authorized", "status": "supported", "source_class": record["source_class"], "relation_id": record["relation_id"]})
    chat_fields = [node for node in walk(chat.body) if node.type == "pair" and chat.doc.text(node.child_by_field_name("key")) == engine.rule["protocol"]["wire_field"]]
    engine.require(len(chat_fields) >= 1, obligation, "device_chat_explicit_command_refutation_missing", "independent Chat construction has no authenticated explicit selected command field")
    for node in chat_fields:
        record = engine.fact("chat_explicit_verification_command", obligation, chat, node,
            field=engine.rule["protocol"]["wire_field"], supplied_expression=chat.doc.text(node.child_by_field_name("value")),
            conditional_refutation="Chat's explicit field path is independent of the clarification spec constructor", nonblank_value_not_guaranteed=True)
        engine.counterexamples.append({"kind": "chat_explicit_command", "status": "supported", "source_class": record["source_class"], "relation_id": record["relation_id"]})
    returned = engine.returned(producer, obligation)
    fields, _ = _fields(producer, returned)
    payload, _ = _fields(producer, fields.get("payload"))
    spec, _ = _fields(producer, payload.get("spec"))
    criteria = spec.get("acceptanceCriteria")
    criterion_objects = [node for node in walk(criteria) if node.type == "object"] if criteria is not None else []
    criterion_keys = []
    for obj in criterion_objects:
        keys, closed = _fields(producer, obj)
        if closed:
            criterion_keys.append(sorted(keys))
    engine.require(criterion_keys == [["id", "required", "title"]], obligation,
        "device_criterion_field_refutation_unclosed", "nested criterion display/title data is not distinguished from a top-level executable command")
    if criteria is not None:
        record = engine.fact("criterion_text_not_top_level_command", obligation, producer, criteria,
            criterion_own_keys=criterion_keys, selected_top_level_field_absent=engine.rule["protocol"]["wire_field"] not in spec)
        engine.counterexamples.append({"kind": "criterion_display_is_not_wire_command", "status": "supported", "source_class": record["source_class"], "relation_id": record["relation_id"]})
    display_fields = [node for node in walk(criterion_values.body) if node.type == "pair"
        and criterion_values.doc.text(node.child_by_field_name("key")) == "verificationMethod"
        and _text(criterion_values, node.child_by_field_name("value")) == "criterion.verificationMethod"]
    engine.require(len(display_fields) == 1, obligation, "device_existing_criterion_display_unclosed", "existing criterion verification method display does not have one source-derived read")
    if display_fields:
        engine.fact("existing_criterion_verification_display", obligation, criterion_values, display_fields[0],
            nested_read_path="criterion.verificationMethod", distinct_from_top_level_wire_field=engine.rule["protocol"]["wire_field"],
            supplied_as_executable_command=False)
    authorization = engine.calls(dispatcher, "self.application.authorize_scope")
    actor_validation = engine.calls(dispatcher, "validate_actor")
    replay = engine.calls(update, "self.delivery_replay")
    engine.require(len(authorization) == len(actor_validation) == len(replay) == 1, obligation,
        "device_auth_replay_conditions_missing", "authorization/actor/replay branch limitations are not source-authenticated")
    save = engine.method(port, "save", obligation)
    confirmation = []
    if save is not None:
        confirmation = [node for node in _runtime(save.body) if node.type == "if_statement"
            and "response.outcome" in save.doc.text(node.child_by_field_name("condition")) and "response.command" in save.doc.text(node.child_by_field_name("condition"))]
    engine.require(len(confirmation) == 1, obligation, "device_command_confirmation_missing", "UI save lacks source-derived outcome and command confirmation limitations")
    for role, nodes, kind in ((dispatcher, authorization, "authorized_scope_required"), (update, replay, "existing_exact_receipt_replays_before_authority"), (save, confirmation, "completed_command_confirmation_required")):
        if role is not None and nodes:
            record = engine.fact(kind, obligation, role, nodes[0], is_condition_or_counterexample=True)
            engine.counterexamples.append({"kind": kind, "status": "supported", "source_class": record["source_class"], "relation_id": record["relation_id"]})
    engine.finish_obligation(obligation, start, all_requested_counterexamples_retained=True,
        outcome_scope="conditional clarification update rejection, never all specification edits or every delivery path")


def assess_device_flow(snapshot: GraphSnapshot, rule: dict, sources: SemanticSources | None = None) -> dict:
    validate_device_flow_rule(rule)
    engine = _Engine(snapshot, sources or SemanticSources(snapshot), rule)
    for analysis in (_producer, _client_wiring, _protocol, _authority, _refutations):
        try:
            analysis(engine)
        except (ValueError, TypeError, AttributeError, RuntimeError, RecursionError, KeyError, IndexError) as error:
            obligation = {"_producer": "D1", "_client_wiring": "D2", "_protocol": "D3", "_authority": "D4", "_refutations": "D5"}[analysis.__name__]
            engine.gap(obligation, "device_analyzer_boundary", "finite source extractor did not close this obligation", error_type=type(error).__name__, error=str(error)[:500])
            if not any(item["id"] == obligation for item in engine.obligations):
                engine.finish_obligation(obligation, 0)
    complete = len(engine.obligations) == 5 and all(item["complete"] and item["status"] == "supported" for item in engine.obligations) and not engine.gaps
    model_complete = bool(engine.models) and all(item["applicability"]["accepted"] for item in engine.models)
    complete = bool(complete and model_complete)
    return {"analyzer_version": VERSION, "policy_version": POLICY_VERSION, "snapshot_id": snapshot.id,
        "source_hash": snapshot.source_hash, "policy_hash": snapshot.policy_hash, "contract_hash": _digest(rule),
        "lexical_bindings_version": LEXICAL_VERSION, "proof_domain": "source-and-finite-trusted-protocol-model",
        "completion_summaries_version": COMPLETION_VERSION,
        "original_claim": "clarification update omits the conditional required verification command; an active Device authority rejects that update",
        "derived_judgment": "Under the explicitly retained normal production, JSON/Serde and active Device conditions, the closed UI command field omission reaches None and the nonblank authority guard rejects before criterion use/commit." if complete else "Only the supported obligations are established; the missing intermediate relationships are not environmental assumptions.",
        "assessment": "scoped_static_judgment_reproduced" if complete else "partial_obligations_supported" if engine.relations else "unknown_or_source_invalid",
        "complete_assessment": complete, "full_goal_supported": complete,
        "obligations": engine.obligations, "relations": engine.relations, "models": engine.models,
        "conditions": {"source_class": "policy-declared", "kind": "true_environment_and_model_conditions", "items": rule["applicability"]["conditions"], "provenance": rule["provenance"]},
        "refutations": engine.counterexamples, "analysis_gaps": engine.gaps, "necessary_gaps": engine.gaps,
        "summary": {"snapshot_id": snapshot.id, "source_hash": snapshot.source_hash, "policy_hash": snapshot.policy_hash,
            "contract_hash": _digest(rule), "obligation_count": 5, "supported": sum(item["status"] == "supported" for item in engine.obligations),
            "relation_count": len(engine.relations), "relation_counts": dict(Counter(item["kind"] for item in engine.relations)),
            "source_class_counts": dict(Counter(item["source_class"] for item in engine.relations)),
            "all_relations_retained": True, "sampled": False, "operation_count": engine.operations, "operation_limit": _LIMIT},
        "scope_boundaries": ["No target code, tests, build, generated module or macro is executed.",
            "Protocol/message/dependency records do not create or upgrade snapshot CALLS edges.",
            "A successful ordinary-model message and an active Device branch are conditional, not observed running facts.",
            "Role configuration does not establish actual injection or dependency identity."]}


def analyze_device_flows(snapshot: GraphSnapshot, rules: list[dict]) -> list[Finding]:
    sources, findings = SemanticSources(snapshot), []
    counts = Counter(rule.get("id") for rule in rules if isinstance(rule, dict) and isinstance(rule.get("id"), str)) if isinstance(rules, list) else Counter()
    if not isinstance(rules, list):
        rules = [{"id": "invalid-device-flows"}]
    for index, rule in enumerate(rules):
        try:
            validate_device_flow_rule(rule)
            if counts[rule["id"]] != 1:
                raise ValueError("duplicate device flow rule id")
            details = assess_device_flow(snapshot, rule, sources)
        except (ValueError, TypeError, AttributeError, RuntimeError, RecursionError, KeyError) as error:
            details = {"analyzer_version": VERSION, "policy_version": POLICY_VERSION, "snapshot_id": snapshot.id,
                "assessment": "unknown_or_source_invalid", "complete_assessment": False, "full_goal_supported": False,
                "obligations": [{"id": "D"+str(item), "status": "unknown", "complete": False} for item in range(1, 6)],
                "analysis_gaps": [{"code": "device_rule_invalid", "message": str(error), "source_class": "unresolved"}], "necessary_gaps": [{"code": "device_rule_invalid", "message": str(error)}]}
        rule_id = rule.get("id", f"invalid-device-rule-{index}") if isinstance(rule, dict) else f"invalid-device-rule-{index}"
        fingerprint = _digest({"version": VERSION, "rule_id": rule_id, "contract": rule})
        locations = [item["location"] for item in details.get("relations", [])]
        evidence = Evidence(id=_digest({"snapshot": snapshot.id, "fingerprint": fingerprint, "kind": "device-flow-assessment", "details": details})[:24],
            kind="static_device_protocol_flow", message="Complete necessary-obligation assessment over captured source and finite protocol models; no execution.",
            locations=locations, details=details)
        findings.append(Finding(id=_digest({"snapshot": snapshot.id, "fingerprint": fingerprint})[:24],
            type="conditional_protocol_field_omission", severity=rule.get("severity", "info") if isinstance(rule, dict) else "info",
            status="confirmed" if details.get("full_goal_supported") else "uncertain", title="Conditional command field to Device authority judgment",
            description=details.get("derived_judgment", "Necessary source/model relationships remain unresolved."),
            rule_id=rule_id, fingerprint=fingerprint, snapshot_id=snapshot.id, evidence=[evidence], metadata={"device_flow_assessment": details}))
    return findings
