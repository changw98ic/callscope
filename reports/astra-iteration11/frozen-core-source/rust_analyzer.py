"""Rust source-body call extraction without Cargo, rustc, macros or execution.

The input is the orchestrator's already captured text. Only explicit lexical
bindings, non-generic concrete Self-to-inherent-method calls, and bounded
same-impl lexical self/Self calls in generic inherent impls are resolved.
Other method/trait dispatch, closures, conditional compilation, generated
definitions and unavailable module bodies stay visible as uncertainty.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field, replace
import hashlib
import posixpath
from pathlib import Path, PurePosixPath
import re
from typing import Any

from .models import Diagnostic, Edge, Node, SourceFile
from .parsers import language_parser, parser_version
from .rust_helpers import HELPER_MODEL_VERSION, classify_rust_item_helpers
from .rust_source_context import SOURCE_CONTEXT_VERSION, classify_crate_inner_attribute

ANALYZER_VERSION = "rust-tree-sitter-1.8-crate-attribute-context"
PARSER_VERSION = parser_version("rust")
_GENERIC_IMPL_MODEL = "rust-generic-same-impl-lexical-v1"
_EQ_INTERFACE_MODEL = "rust-core-cmp-eq-interface-v1"
_EQ_INTERFACE_MEMBERS = {"eq", "ne", "assert_receiver_is_total_eq"}

_STANDARD_ATTRIBUTES = {
    "cfg", "cfg_attr", "derive", "test", "must_use", "inline", "allow", "warn",
    "deny", "forbid", "doc", "cold", "repr", "non_exhaustive", "no_mangle",
    "link", "link_name", "export_name", "deprecated", "track_caller", "path",
    "automatically_derived", "ignore", "should_panic", "macro_use", "macro_export",
    "unsafe", "expect", "rustfmt::skip",
}
_PRELUDE_CONSTRUCTORS = {"Some", "None", "Ok", "Err"}
_PRELUDE_FUNCTIONS = {"drop"}


def _name(value: str) -> str:
    return value[2:] if value.startswith("r#") else value


def _text(node: Any, raw: bytes, maximum: int = 900) -> str:
    return raw[node.start_byte:node.end_byte].decode("utf-8", "replace")[:maximum] if node else ""


def _segments(node: Any, raw: bytes) -> list[str] | None:
    if node is None:
        return None
    if node.type in {"identifier", "type_identifier", "self", "crate", "super"}:
        return [_name(_text(node, raw))]
    if node.type in {"scoped_identifier", "scoped_type_identifier"}:
        prefix = node.child_by_field_name("path")
        suffix = node.child_by_field_name("name")
        left = _segments(prefix, raw) if prefix else []
        right = _segments(suffix, raw)
        if left is None or right is None:
            return None
        return (["::"] if prefix is None and _text(node, raw).startswith("::") else []) + left + right
    if node.type in {"generic_function", "generic_type"}:
        return _segments(node.child_by_field_name("function") or node.child_by_field_name("type"), raw)
    return None


def _pattern_names(node: Any, raw: bytes) -> set[str]:
    if node is None:
        return set()
    if node.type in {"scoped_identifier", "scoped_type_identifier", "type_identifier"}:
        return set()
    if node.type == "field_pattern":
        pattern = node.child_by_field_name("pattern")
        if pattern:
            return _pattern_names(pattern, raw)
        name = _text(node.child_by_field_name("name"), raw)
        return {_name(name)} if name and name != "_" else set()
    if node.type in {"identifier", "self"}:
        value = _name(_text(node, raw))
        return {value} if value != "_" else set()
    names: set[str] = set()
    for child in node.named_children:
        if node.child_by_field_name("type") == child:
            continue
        names.update(_pattern_names(child, raw))
    return names


def _attribute_name(text: str) -> str:
    match = re.match(r"#\s*!?\s*\[\s*([A-Za-z_][A-Za-z_0-9:]*)", text)
    return match.group(1) if match else "unknown"


def _cfg(attrs: list[str]) -> list[str]:
    return [value for value in attrs if _attribute_name(value) in {"cfg", "cfg_attr"}]


def _opaque(attrs: list[str]) -> bool:
    return any(_attribute_name(value) not in _STANDARD_ATTRIBUTES for value in attrs)


def _location(file: _File, syntax: Any) -> dict[str, Any]:
    return {"file": file.source.path, "line": syntax.start_point.row + 1,
        "column": syntax.start_point.column, "end_line": syntax.end_point.row + 1}


def _has_generic_type(node: Any) -> bool:
    pending = [node] if node is not None else []
    while pending:
        current = pending.pop()
        if current.type in {"generic_type", "type_arguments", "qualified_type"}:
            return True
        pending.extend(current.named_children)
    return False


def _plain_self_parameter(parameter: Any, raw: bytes) -> bool:
    if parameter.type != "self_parameter" or parameter.child_by_field_name("type") is not None:
        return False
    return bool(re.fullmatch(r"(?:&\s*(?:'[A-Za-z_][A-Za-z_0-9]*\s+)?(?:mut\s+)?|mut\s+)?self",
        _text(parameter, raw).strip()))


@dataclass
class _File:
    source: SourceFile
    raw: bytes
    tree: Any = None


@dataclass
class _Binding:
    kind: str
    target: str = ""
    path: list[str] = field(default_factory=list)
    modules: list[Any] = field(default_factory=list)
    start: int = 0
    conditional: bool = False
    scope: Any = None
    callable: bool = False
    value_position: int = 0
    location: dict[str, Any] = field(default_factory=dict)


@dataclass
class _Scope:
    kind: str
    file: _File
    owner: str
    qualpath: str
    parent: Any = None
    module: Any = None
    parent_module: Any = None
    unit: str = ""
    namespace: tuple[str, ...] = ()
    directory: str = ""
    known_unit: bool = False
    cfg: list[str] = field(default_factory=list)
    opaque: bool = False
    bindings: dict[str, list[_Binding]] = field(default_factory=dict)
    stars: list[list[str]] = field(default_factory=list)
    impl_scope: Any = None
    impl_type: list[str] = field(default_factory=list)
    impl_receiver_base: list[str] = field(default_factory=list)
    impl_target: str | None = None
    trait_impl: bool = False
    impl_type_text: str = ""
    impl_trait: str = ""
    impl_trait_path: list[str] = field(default_factory=list)
    impl_generic: bool = False
    impl_location: dict[str, Any] = field(default_factory=dict)
    impl_header: str = ""
    impl_end_byte: int = 0
    impl_resolution_reason: str = ""
    start: int = 0
    macro_bindings_unknown: bool = False
    macro_names: set[str] = field(default_factory=set)
    model_bindings_incomplete: bool = False
    inner_attributes: list[str] = field(default_factory=list)
    builtin_attribute_models: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _Call:
    node: Any
    scope: _Scope
    attrs: list[str] = field(default_factory=list)
    macro: bool = False
    closure_definition: str = ""


@dataclass
class _Ref:
    resolution: str
    kind: str = "unknown"
    target: str | None = None
    modules: list[_Scope] = field(default_factory=list)
    candidates: list[str] = field(default_factory=list)
    reason: str = ""
    external: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class _Index:
    def __init__(self, files: dict[str, _File], config: dict):
        self.files = files
        self.config = config
        self.nodes: dict[str, Node] = {}
        self.locations: dict[str, set[tuple[str, int, int]]] = {}
        self.contexts: dict[str, set[str]] = {}
        self.modules: dict[tuple[str, tuple[str, ...]], list[_Scope]] = {}
        self.roots: dict[str, _Scope] = {}
        self.crates: dict[str, list[_Scope]] = {}
        self.processed_files: set[str] = set()
        self.calls: list[_Call] = []
        self.impls: list[_Scope] = []
        self.associated: dict[tuple[str, str], list[str]] = {}
        self.inherent_methods: dict[tuple[str, str], list[str]] = {}
        self.trait_methods: dict[tuple[str, str], list[str]] = {}
        self.trait_declaration_members: dict[str, dict[str, list[str]]] = {}
        self.unmodeled_trait_members: dict[str, list[dict[str, Any]]] = {}
        self.unknown_trait_default_types: set[str] = set()
        self.unknown_trait_default_receivers: list[dict[str, Any]] = []
        self.deref_types: set[str] = set()
        self.method_names: dict[str, set[str]] = {}
        self.nodes_scopes: dict[str, _Scope] = {}
        self.function_scopes: dict[str, list[_Scope]] = {}
        self.callable_parameters: dict[str, set[int]] = {}
        self.diagnostics: list[Diagnostic] = []
        self.coverage_incomplete = False
        self.unmapped_files: list[str] = []
        self.module_gaps: list[dict[str, Any]] = []
        self.cfg_scopes = 0
        self.macro_definitions = 0
        self.exported_macro_names: dict[str, set[str]] = {}
        self.type_items: list[tuple[str, _Scope, _Binding, list[str], str]] = []
        self.modeled_trait_interfaces: dict[str, list[dict[str, Any]]] = {}
        self.build_complete = False

    def diagnostic(self, code: str, message: str, file: _File | None = None,
                   node: Any = None, level: str = "warning") -> None:
        self.diagnostics.append(Diagnostic(level, code, message,
            file.source.path if file else "", node.start_point.row + 1 if node else 0))

    def add_node(self, node: Node, syntax: Any, scope: _Scope) -> None:
        location = (node.file, syntax.start_byte if syntax else 0, syntax.end_byte if syntax else 0)
        context = scope.unit + "::" + "::".join(scope.namespace)
        self.contexts.setdefault(node.id, set()).add(context)
        prior = self.nodes.get(node.id)
        if prior is None:
            self.nodes[node.id] = node
            self.locations[node.id] = {location}
        elif location not in self.locations[node.id]:
            self.locations[node.id].add(location)
            definitions = prior.metadata.setdefault("definitions", [{
                "file": prior.file, "line": prior.line, "end_line": prior.end_line,
                "signature": prior.signature, "cfg_conditions": prior.metadata.get("cfg_conditions", []),
            }])
            definitions.append({"file": node.file, "line": node.line, "end_line": node.end_line,
                "signature": node.signature, "cfg_conditions": node.metadata.get("cfg_conditions", [])})
            prior.metadata["duplicate_definition"] = True
            self.diagnostic("rust_duplicate_definition", f"{node.id} 有多个源码声明；不能选择唯一实现。",
                scope.file, syntax)

    def child_scope(self, kind: str, scope: _Scope, owner: str | None = None,
                    qualpath: str | None = None, attrs: list[str] | None = None,
                    start: int = 0) -> _Scope:
        attrs = attrs or []
        return _Scope(kind, scope.file, owner or scope.owner,
            scope.qualpath if qualpath is None else qualpath, parent=scope,
            module=scope.module, unit=scope.unit, namespace=scope.namespace,
            directory=scope.directory, known_unit=scope.known_unit,
            cfg=list(dict.fromkeys([*scope.cfg, *_cfg(attrs)])),
            opaque=scope.opaque or _opaque(attrs), impl_scope=scope.impl_scope, start=start,
            builtin_attribute_models=list(scope.builtin_attribute_models))

    def bind(self, scope: _Scope, name: str, binding: _Binding) -> None:
        if name and name != "_":
            binding.scope = binding.scope or scope
            scope.bindings.setdefault(name, []).append(binding)

    def module_scope(self, file: _File, body: Any, unit: str,
                     namespace: tuple[str, ...], directory: str,
                     parent_module: _Scope | None = None,
                     attrs: list[str] | None = None, known: bool = True,
                     qualpath: str = "", inline: bool = False) -> _Scope:
        attrs = attrs or []
        key = (unit, namespace)
        for prior in self.modules.get(key, []):
            if prior.file.source.path == file.source.path and prior.start == body.start_byte:
                return prior
        module = file.source.module
        owner = f"{module}#{qualpath}" if inline else "module:" + module
        conditions = list(dict.fromkeys([*(parent_module.cfg if parent_module else []), *_cfg(attrs)]))
        scope = _Scope("module", file, owner, qualpath,
            parent_module=parent_module, unit=unit, namespace=namespace, directory=directory,
            known_unit=known, cfg=conditions,
            opaque=(parent_module.opaque if parent_module else False) or _opaque(attrs), start=body.start_byte,
            builtin_attribute_models=list(parent_module.builtin_attribute_models) if parent_module else [])
        scope.module = scope
        self.modules.setdefault(key, []).append(scope)
        if not namespace:
            self.roots[unit] = scope
        self.processed_files.add(file.source.path)
        self.add_node(Node(owner, namespace[-1] if namespace else module, owner, module,
            file.source.path, body.start_point.row + 1, max(1, body.end_point.row + 1), "module",
            metadata={"language": "rust", "source_status": file.source.status,
                "rust_namespace": "::".join(namespace), "crate_root": unit,
                "cfg_conditions": conditions, "conditional_definition": bool(conditions),
                "cfg_test": any(re.search(r"\bcfg\s*\(\s*test\s*\)", x) for x in conditions),
                "attribute_macros_unknown": scope.opaque}), body, scope)
        if conditions:
            self.cfg_scopes += 1
        self.sequence(body, scope)
        saved = self.nodes[owner].metadata
        saved["cfg_conditions"] = list(scope.cfg)
        saved["conditional_definition"] = bool(scope.cfg)
        saved["attribute_macros_unknown"] = scope.opaque
        saved["builtin_crate_attribute_models"] = list(scope.builtin_attribute_models)
        return scope

    def generic_parameters(self, syntax: Any, scope: _Scope) -> None:
        parameters = syntax.child_by_field_name("type_parameters")
        if parameters:
            for parameter in parameters.named_children:
                name = parameter.child_by_field_name("name")
                if name:
                    self.bind(scope, _name(_text(name, scope.file.raw)), _Binding("generic"))

    def sequence(self, node: Any, scope: _Scope) -> None:
        # Inner cfg/attribute macros govern the whole enclosing source body.
        for child in node.named_children:
            if child.type == "inner_attribute_item":
                text = _text(child, scope.file.raw, 600)
                scope.inner_attributes.append(text)
                scope.cfg = list(dict.fromkeys([*scope.cfg, *_cfg([text])]))
                builtin = classify_crate_inner_attribute(child, scope.file.raw,
                    is_known_crate_root=(scope.kind == "module" and scope.known_unit
                        and scope.parent is None and scope.parent_module is None
                        and not scope.namespace and scope.unit == scope.file.source.path))
                if builtin is not None:
                    scope.builtin_attribute_models.append({**builtin, "file": scope.file.source.path,
                        "source_sha256": scope.file.source.hash, "crate_root": scope.unit})
                else:
                    scope.opaque = scope.opaque or _opaque([text])
        pending: list[str] = []
        for child in node.named_children:
            if child.type == "inner_attribute_item":
                # Already applied to this enclosing scope in the pass above.
                # An inner attribute is never an outer attribute of the next
                # use/item/statement, regardless of intervening comments.
                continue
            if child.type == "attribute_item":
                pending.append(_text(child, scope.file.raw, 600))
                continue
            if child.type in {"line_comment", "block_comment"}:
                continue
            self.visit(child, scope, pending)
            pending = []

    def visit(self, syntax: Any, scope: _Scope, attrs: list[str] | None = None) -> None:
        attrs = attrs or []
        kind = syntax.type
        raw = scope.file.raw
        if kind in {"function_item", "function_signature_item"}:
            name = _name(_text(syntax.child_by_field_name("name"), raw))
            if not name:
                return
            qualpath = scope.qualpath + "." + name if scope.qualpath else name
            node_id = scope.file.source.module + "#" + qualpath
            body = syntax.child_by_field_name("body")
            parameters = syntax.child_by_field_name("parameters")
            value_parameters = [x for x in parameters.named_children
                if x.type in {"parameter", "self_parameter", "variadic_parameter"}] if parameters else []
            type_parameters = syntax.child_by_field_name("type_parameters")
            where_clause = next((x for x in syntax.named_children if x.type == "where_clause"), None)
            constraint_gaps = []
            if type_parameters is not None:
                constraint_gaps.append("method-level generic parameters")
            if where_clause is not None:
                constraint_gaps.append("method-level where clause")
            pending_parameters = list(parameters.named_children) if parameters else []
            while pending_parameters:
                parameter_node = pending_parameters.pop()
                if parameter_node.type in {"abstract_type", "attribute_item", "inner_attribute_item", "variadic_parameter"}:
                    constraint_gaps.append(parameter_node.type)
                pending_parameters.extend(parameter_node.named_children)
            self_parameter = bool(parameters and any(x.type == "self_parameter" for x in parameters.named_children))
            plain_receiver = next((x for x in parameters.named_children if _plain_self_parameter(x, raw)), None) if parameters else None
            method = scope.kind in {"impl", "trait"}
            conditions = list(dict.fromkeys([*scope.cfg, *_cfg(attrs)]))
            signature_end = body.start_byte if body else syntax.end_byte
            signature = raw[syntax.start_byte:signature_end].decode("utf-8", "replace").strip()[:900]
            metadata = {"language": "rust", "cfg_conditions": conditions,
                "conditional_definition": bool(conditions), "attributes": attrs,
                "attribute_macros_unknown": scope.opaque or _opaque(attrs),
                "builtin_crate_attribute_models": list(scope.builtin_attribute_models),
                "declaration_only": body is None,
                "static_method": method and not self_parameter,
                "trait_dispatch": scope.kind == "trait" or scope.trait_impl,
                "rust_namespace": "::".join(scope.namespace), "crate_root": scope.unit,
                "cfg_test": any(re.search(r"\bcfg\s*\(\s*test\s*\)", x) for x in conditions),
                "declaration_location": _location(scope.file, syntax),
                "plain_self_receiver": plain_receiver is not None,
                "self_parameter": _text(plain_receiver, raw).strip() if plain_receiver else "",
                "value_parameter_count": len(value_parameters),
                "method_type_parameters": _text(type_parameters, raw, type_parameters.end_byte - type_parameters.start_byte) if type_parameters else "",
                "method_where_clause": _text(where_clause, raw, where_clause.end_byte - where_clause.start_byte) if where_clause else "",
                "method_constraint_gaps": sorted(set(constraint_gaps)),
                "async": bool(re.search(r"\basync\s+fn\b", signature))}
            if scope.kind == "impl":
                metadata.update({"impl_type": scope.impl_type_text,
                    "impl_type_name": "::".join(scope.impl_type),
                    "impl_trait": scope.impl_trait,
                    "impl_trait_implementation": scope.trait_impl,
                    "impl_generic": scope.impl_generic,
                    "impl_location": scope.impl_location})
            self.add_node(Node(node_id, name, node_id, scope.file.source.module,
                scope.file.source.path, syntax.start_point.row + 1, syntax.end_point.row + 1,
                "method" if method else "function", signature, metadata=metadata), syntax, scope)
            self.bind(scope, name, _Binding("symbol", target=node_id,
                conditional=bool(conditions) or scope.opaque or _opaque(attrs)))
            if method:
                self.method_names.setdefault(name, set()).add(node_id)
                if scope.kind == "trait":
                    self.trait_declaration_members.setdefault(scope.owner, {}).setdefault(name, []).append(node_id)
            if body is not None:
                function_scope = self.child_scope("function", scope, node_id, qualpath, attrs,
                    start=syntax.start_byte)
                function_scope.impl_scope = scope if scope.kind == "impl" else scope.impl_scope
                self.function_scopes.setdefault(node_id, []).append(function_scope)
                self.generic_parameters(syntax, function_scope)
                callable_positions: set[int] = set()
                for i, parameter in enumerate(parameters.named_children if parameters else []):
                    pattern = parameter.child_by_field_name("pattern") or parameter
                    type_node = parameter.child_by_field_name("type")
                    callable_type = bool(re.search(r"\b(?:fn|Fn|FnMut|FnOnce)\b", _text(type_node, raw)))
                    if callable_type:
                        callable_positions.add(i)
                    for variable in _pattern_names(pattern, raw):
                        receiver = variable == "self" and parameter == plain_receiver and scope.kind == "impl"
                        self.bind(function_scope, variable, _Binding("self_receiver" if receiver else "variable",
                            callable=callable_type, start=parameter.start_byte,
                            location=_location(scope.file, parameter)))
                self.callable_parameters[node_id] = callable_positions
                self.sequence(body, function_scope)
            return
        if kind in {"struct_item", "enum_item", "trait_item", "type_item", "union_item"}:
            name = _name(_text(syntax.child_by_field_name("name"), raw))
            if not name:
                return
            qualpath = scope.qualpath + "." + name if scope.qualpath else name
            node_id = scope.file.source.module + "#" + qualpath
            conditions = list(dict.fromkeys([*scope.cfg, *_cfg(attrs)]))
            helper_body_gaps: list[str] = []
            if any(_attribute_name(attr) == "serde" for attr in attrs):
                pending_body = list(syntax.named_children)
                while pending_body:
                    child = pending_body.pop()
                    if child.type == "macro_invocation":
                        helper_body_gaps.append("unexpanded macro within type declaration")
                    elif child.type in {"attribute_item", "inner_attribute_item"}:
                        attribute = _text(child, raw, 600)
                        if _cfg([attribute]) or _opaque([attribute]):
                            helper_body_gaps.append(attribute)
                    pending_body.extend(child.named_children)
            self.add_node(Node(node_id, name, node_id, scope.file.source.module,
                scope.file.source.path, syntax.start_point.row + 1, syntax.end_point.row + 1,
                "trait" if kind == "trait_item" else "type", metadata={"language": "rust",
                    "type_kind": kind, "cfg_conditions": conditions,
                    "conditional_definition": bool(conditions), "attributes": attrs,
                    "attribute_macros_unknown": scope.opaque or _opaque(attrs),
                    "builtin_crate_attribute_models": list(scope.builtin_attribute_models),
                    "generic_definition": syntax.child_by_field_name("type_parameters") is not None,
                    "declaration_location": _location(scope.file, syntax),
                    "helper_nested_model_gaps": list(dict.fromkeys(helper_body_gaps)),
                    "type_alias_unknown": kind == "type_item"}), syntax, scope)
            binding = _Binding("type", target=node_id,
                conditional=bool(conditions) or scope.opaque or _opaque(attrs))
            self.bind(scope, name, binding)
            self.type_items.append((node_id, scope, binding, list(attrs), kind))
            body = syntax.child_by_field_name("body")
            if kind == "trait_item" and body:
                trait_scope = self.child_scope("trait", scope, node_id, qualpath, attrs)
                trait_scope.trait_impl = True
                self.generic_parameters(syntax, trait_scope)
                self.sequence(body, trait_scope)
            return
        if kind == "impl_item":
            type_node = syntax.child_by_field_name("type")
            trait = syntax.child_by_field_name("trait")
            type_path = _segments(type_node, raw)
            type_name = "::".join(type_path) if type_path else _text(type_node, raw, 180)
            label = f"<{type_name} as {_text(trait, raw, 180)}>" if trait else type_name
            qualpath = scope.qualpath + "." + label if scope.qualpath else label
            impl_scope = self.child_scope("impl", scope, qualpath=qualpath, attrs=attrs, start=syntax.start_byte)
            impl_scope.impl_type = type_path or []
            receiver_base = type_node
            while receiver_base is not None and receiver_base.type == "reference_type":
                receiver_base = receiver_base.child_by_field_name("type")
            impl_scope.impl_receiver_base = _segments(receiver_base, raw) or []
            impl_scope.trait_impl = trait is not None
            impl_scope.impl_type_text = _text(type_node, raw, 300)
            impl_scope.impl_trait = _text(trait, raw, 300)
            impl_scope.impl_trait_path = _segments(trait, raw) or []
            impl_scope.impl_generic = bool(syntax.child_by_field_name("type_parameters") is not None
                or _has_generic_type(type_node) or _has_generic_type(trait)
                or any(child.type == "where_clause" for child in syntax.named_children))
            impl_scope.impl_location = _location(scope.file, syntax)
            body = syntax.child_by_field_name("body")
            impl_scope.impl_header = raw[syntax.start_byte:body.start_byte if body else syntax.end_byte].decode("utf-8", "replace").strip()
            impl_scope.impl_end_byte = syntax.end_byte
            impl_scope.impl_scope = impl_scope
            self.generic_parameters(syntax, impl_scope)
            self.impls.append(impl_scope)
            if body:
                self.sequence(body, impl_scope)
            return
        if kind == "mod_item":
            self.module_item(syntax, scope, attrs)
            return
        if kind == "use_declaration":
            argument = syntax.child_by_field_name("argument")
            self.use_tree(argument, scope, [], bool(scope.cfg or _cfg(attrs) or scope.opaque or _opaque(attrs)))
            return
        if kind == "extern_crate_declaration":
            if any(_attribute_name(attr) == "macro_use" for attr in attrs):
                scope.model_bindings_incomplete = True
            match = re.search(r"extern\s+crate\s+([\w]+)(?:\s+as\s+([\w]+))?", _text(syntax, raw))
            if match:
                self.bind(scope, match.group(2) or match.group(1), _Binding("extern_crate", path=[match.group(1)],
                    conditional=bool(scope.cfg or _cfg(attrs)), start=syntax.start_byte))
            return
        if kind in {"closure_expression", "async_block", "gen_block"}:
            label = f"<{kind}@{syntax.start_point.row + 1}:{syntax.start_point.column + 1}>"
            qualpath = scope.qualpath + "." + label if scope.qualpath else label
            node_id = scope.file.source.module + "#" + qualpath
            self.add_node(Node(node_id, label, node_id, scope.file.source.module,
                scope.file.source.path, syntax.start_point.row + 1, syntax.end_point.row + 1,
                "closure", metadata={"language": "rust", "activation_unknown": True,
                    "cfg_conditions": [*scope.cfg, *_cfg(attrs)]}), syntax, scope)
            self.calls.append(_Call(syntax, scope, attrs, closure_definition=node_id))
            closure_scope = self.child_scope("closure", scope, node_id, qualpath, attrs, syntax.start_byte)
            params = syntax.child_by_field_name("parameters")
            for name in _pattern_names(params, raw):
                self.bind(closure_scope, name, _Binding("variable", callable=True))
            body = syntax.child_by_field_name("body")
            if body:
                self.visit(body, closure_scope)
            else:
                for child in syntax.named_children:
                    if child != params:
                        self.visit(child, closure_scope)
            return
        if kind == "macro_invocation":
            self.calls.append(_Call(syntax, scope, attrs, macro=True))
            expansion_scope = scope
            while expansion_scope.kind == "expression" and expansion_scope.parent:
                expansion_scope = expansion_scope.parent
            expansion_scope.macro_bindings_unknown = True
            return
        if kind == "macro_definition":
            self.macro_definitions += 1
            macro_name = _name(_text(syntax.child_by_field_name("name"), raw))
            if macro_name:
                scope.macro_names.add(macro_name)
                if any(_attribute_name(attr) == "macro_export" for attr in attrs):
                    self.exported_macro_names.setdefault(scope.unit, set()).add(macro_name)
            else:
                scope.model_bindings_incomplete = True
            self.coverage_incomplete = True
            self.diagnostic("rust_macro_definition", "宏定义未展开；可能生成的声明和调用不在显式源码图中。",
                scope.file, syntax, "info")
            return
        if kind == "call_expression":
            self.calls.append(_Call(syntax, scope, attrs))
        if kind == "let_declaration":
            value = syntax.child_by_field_name("value")
            if value:
                self.visit(value, scope, attrs)
            pattern = syntax.child_by_field_name("pattern")
            names = _pattern_names(pattern, raw)
            path = _segments(value, raw)
            simple = pattern is not None and pattern.type == "identifier" and len(names) == 1
            mutable = bool(re.search(r"\bmut\b", _text(syntax, raw)))
            type_node = syntax.child_by_field_name("type")
            for child in syntax.named_children:
                if child != value and child != pattern and child != type_node:
                    # In let-else, the alternative body executes before the
                    # new binding becomes available. Its calls must not vanish.
                    self.visit(child, scope, attrs)
            for name in names:
                self.bind(scope, name, _Binding("alias" if simple and path and not mutable else "variable",
                    path=path or [], start=syntax.end_byte,
                    value_position=value.start_byte if value else syntax.start_byte,
                    conditional=bool(scope.cfg or _cfg(attrs)), callable=bool(value and value.type == "closure_expression")))
            return
        if kind in {"const_item", "static_item"}:
            name = _name(_text(syntax.child_by_field_name("name"), raw))
            self.bind(scope, name, _Binding("variable"))
        if kind == "assignment_expression":
            left = syntax.child_by_field_name("left")
            if left and left.type == "identifier":
                self.bind(scope, _name(_text(left, raw)), _Binding("variable", start=syntax.end_byte))
        if kind in {"if_expression", "while_expression", "for_expression", "match_arm"}:
            scope = self.child_scope("block", scope, attrs=attrs, start=syntax.start_byte)
            if kind in {"for_expression", "match_arm"}:
                pattern = syntax.child_by_field_name("pattern")
                for name in _pattern_names(pattern, raw):
                    self.bind(scope, name, _Binding("variable"))
            attrs = []
        if kind == "let_condition":
            value = syntax.child_by_field_name("value")
            if value:
                self.visit(value, scope)
            for name in _pattern_names(syntax.child_by_field_name("pattern"), raw):
                self.bind(scope, name, _Binding("variable", start=syntax.end_byte))
            return
        if kind == "block":
            block = self.child_scope("block", scope, attrs=attrs, start=syntax.start_byte)
            self.sequence(syntax, block)
            return
        child_scope = self.child_scope("expression", scope, attrs=attrs, start=syntax.start_byte) if attrs else scope
        self.sequence(syntax, child_scope)

    def use_tree(self, node: Any, scope: _Scope, prefix: list[str], conditional: bool) -> None:
        if node is None:
            return
        raw = scope.file.raw
        if node.type == "scoped_use_list":
            path = _segments(node.child_by_field_name("path"), raw)
            group = node.child_by_field_name("list")
            if path is not None and group:
                self.use_tree(group, scope, prefix + path, conditional)
            return
        if node.type == "use_list":
            for child in node.named_children:
                self.use_tree(child, scope, prefix, conditional)
            return
        if node.type == "use_wildcard":
            parts = _segments(node.named_children[0], raw) if node.named_children else []
            scope.stars.append(prefix + (parts or []))
            self.coverage_incomplete = True
            self.diagnostic("rust_glob_import", "星号导入的导出集合未推断；相关未绑定调用保留未知。", scope.file, node)
            return
        if node.type == "use_as_clause":
            path = _segments(node.child_by_field_name("path"), raw)
            alias = _name(_text(node.child_by_field_name("alias"), raw))
        else:
            path = _segments(node, raw)
            alias = path[-1] if path else ""
        if path is None:
            scope.model_bindings_incomplete = True
            self.coverage_incomplete = True
            self.diagnostic("rust_use_unparsed", "use 路径不在支持的静态形式中。", scope.file, node)
            return
        complete = prefix + path
        if path == ["self"] and prefix:
            complete, alias = prefix, prefix[-1]
        self.bind(scope, alias, _Binding("import", path=complete, conditional=conditional, start=node.start_byte))

    def module_item(self, syntax: Any, scope: _Scope, attrs: list[str]) -> None:
        if any(_attribute_name(attr) == "macro_use" for attr in attrs):
            scope.model_bindings_incomplete = True
        name = _name(_text(syntax.child_by_field_name("name"), scope.file.raw))
        body = syntax.child_by_field_name("body")
        namespace = (*scope.module.namespace, name)
        qualpath = scope.module.qualpath + "." + name if scope.module.qualpath else name
        conditional = bool(scope.cfg or _cfg(attrs) or scope.opaque or _opaque(attrs))
        candidates: list[_Scope] = []
        if body:
            candidates.append(self.module_scope(scope.file, body, scope.unit, namespace,
                posixpath.join(scope.module.directory, name), scope.module, attrs,
                scope.known_unit, qualpath, inline=True))
        else:
            path_attributes = [a for a in attrs if _attribute_name(a) == "path"]
            uncertain_path = any(_attribute_name(a) == "cfg_attr" and "path" in a for a in attrs)
            targets: list[str] = []
            if path_attributes and not uncertain_path:
                match = re.search(r'\bpath\s*=\s*"([^"\\]+)"', path_attributes[0])
                if match:
                    base = scope.module.directory if scope.module.qualpath else posixpath.dirname(scope.file.source.path)
                    path = posixpath.normpath(posixpath.join(base, match.group(1)))
                    if not path.startswith("/") and path != ".." and not path.startswith("../"):
                        targets.append(path)
            elif not uncertain_path:
                targets = [posixpath.join(scope.module.directory, name + ".rs"),
                    posixpath.join(scope.module.directory, name, "mod.rs")]
            selected = [self.files[p] for p in targets if p in self.files and self.files[p].tree is not None]
            for file in selected:
                filename = PurePosixPath(file.source.path)
                directory = str(filename.parent) if filename.name in {"lib.rs", "main.rs", "mod.rs"} else str(filename.with_suffix(""))
                candidates.append(self.module_scope(file, file.tree.root_node, scope.unit, namespace,
                    directory, scope.module, attrs, scope.known_unit))
            if len(candidates) != 1:
                self.coverage_incomplete = True
                self.module_gaps.append({"file": scope.file.source.path, "line": syntax.start_point.row + 1,
                    "module": name, "candidate_files": targets, "available": [x.file.source.path for x in candidates]})
                message = "模块路径依赖未解析的属性" if uncertain_path or path_attributes and not targets else "模块没有唯一可用的捕获源码"
                self.diagnostic("rust_module_gap", f"{name}: {message}；不把它判断成实现缺失。", scope.file, syntax)
        self.bind(scope, name, _Binding("module", modules=candidates, conditional=conditional))

    def build(self) -> None:
        mappings = self.config.get("analysis", {}).get("rust_crates", {})
        for alias, directory in sorted(mappings.items()):
            if not isinstance(alias, str) or not isinstance(directory, str):
                self.coverage_incomplete = True
                self.diagnostic("rust_crate_config", "Rust crate 映射必须为导入名到相对目录。")
                continue
            normalized = posixpath.normpath(directory)
            if normalized.startswith("/") or normalized == ".." or normalized.startswith("../"):
                self.coverage_incomplete = True
                self.diagnostic("rust_crate_config", f"crate {alias} 的路径不在项目范围内。")
                continue
            roots = []
            for basename in ("lib.rs", "main.rs"):
                path = posixpath.normpath(posixpath.join(normalized, "src", basename))
                file = self.files.get(path)
                if file and file.tree is not None:
                    roots.append(self.module_scope(file, file.tree.root_node, path, (), posixpath.dirname(path)))
            if roots:
                self.crates.setdefault(alias.replace("-", "_"), []).append(roots[0])
            else:
                self.coverage_incomplete = True
                self.diagnostic("rust_crate_root_unavailable", f"crate {alias} 无可解析的 src/lib.rs 或 src/main.rs。")
        for path, file in sorted(self.files.items()):
            if file.tree is not None and path not in self.processed_files:
                self.unmapped_files.append(path)
                self.coverage_incomplete = True
                filename = PurePosixPath(path)
                directory = str(filename.parent) if filename.name in {"lib.rs", "main.rs", "mod.rs"} else str(filename.with_suffix(""))
                self.module_scope(file, file.tree.root_node, path, (), directory, known=False)
        if self.unmapped_files:
            self.diagnostic("rust_unmapped_crate_context", f"{len(self.unmapped_files)} 个文件未连接到已配置的 crate 模块树；仅支持文件内词法绑定。")
        for node_id, contexts in self.contexts.items():
            self.nodes[node_id].metadata["module_contexts"] = sorted(contexts)
            if len(contexts) > 1:
                self.nodes[node_id].metadata["multiple_module_contexts"] = True
                self.coverage_incomplete = True
        self.build_complete = True

    def model_environment(self, scope: _Scope) -> dict[str, Any]:
        """Closure facts for explicitly trusted data models, not compiler facts.

        Out-of-line modules have ``parent_module`` rather than lexical parents.
        Both chains matter: a crate's inner attributes and inherited macro
        namespace must not disappear at a captured module-file boundary.
        """
        scopes: list[_Scope] = []
        visited: set[int] = set()
        current: _Scope | None = scope
        while current is not None:
            if id(current) not in visited:
                scopes.append(current)
                visited.add(id(current))
            current = current.parent
        current = scope.module
        while current is not None:
            if id(current) not in visited:
                scopes.append(current)
                visited.add(id(current))
            current = current.parent_module
        root = self.roots.get(scope.unit)
        known_root = bool(root and scope.known_unit and root.known_unit and id(root) in visited)
        source_complete = known_root
        bindings_complete = known_root and self.build_complete
        macro_unknown = False
        prelude_enabled = known_root
        shadowed = set(self.exported_macro_names.get(scope.unit, set()))
        evidence: list[dict[str, Any]] = []
        reasons: list[str] = []
        if not self.build_complete:
            reasons.append("Rust index traversal did not complete; later bindings/duplicates may be missing")
        for item in scopes:
            node = self.nodes.get(item.owner)
            source_ok = item.file.source.status == "parsed"
            context_ok = not bool(node and any(node.metadata.get(key) for key in (
                "duplicate_definition", "multiple_module_contexts")))
            module_ok = item.kind != "module" or len(self.modules.get((item.unit, item.namespace), [])) == 1
            attributes_ok = not item.cfg and not item.opaque
            declarations_ok = not item.stars and not item.model_bindings_incomplete
            source_complete = source_complete and source_ok and context_ok and module_ok
            bindings_complete = bindings_complete and attributes_ok and declarations_ok and context_ok and module_ok
            macro_unknown = macro_unknown or item.macro_bindings_unknown or item.model_bindings_incomplete
            disabled = any(_attribute_name(attr) in {"no_implicit_prelude", "no_core", "no_std"}
                for attr in item.inner_attributes)
            prelude_enabled = prelude_enabled and not disabled and attributes_ok
            shadowed.update(item.bindings)
            shadowed.update(item.macro_names)
            if not (source_ok and context_ok and module_ok and attributes_ok and declarations_ok) or disabled:
                reasons.append(f"{item.file.source.path}:{item.kind}: source/namespace/attribute closure incomplete")
            evidence.append({"file": item.file.source.path, "hash": item.file.source.hash,
                "scope_kind": item.kind, "scope_owner": item.owner, "source_status": item.file.source.status,
                "known_crate_context": item.known_unit, "unique_module_context": context_ok and module_ok,
                "cfg_conditions": list(item.cfg), "attribute_macros_unknown": item.opaque,
                "inner_attributes": list(dict.fromkeys(item.inner_attributes)),
                "builtin_crate_attribute_models": list(item.builtin_attribute_models),
                "glob_imports": [list(path) for path in item.stars],
                "unexpanded_macro_bindings": item.macro_bindings_unknown,
                "macro_names": sorted(item.macro_names), "binding_capture_incomplete": item.model_bindings_incomplete})
        return {"source_complete": bool(source_complete), "bindings_complete": bool(bindings_complete),
            "index_traversal_complete": self.build_complete,
            "macro_scope_unknown": bool(macro_unknown), "prelude_enabled": bool(prelude_enabled),
            "shadowed_names": sorted(shadowed), "scope_evidence": evidence, "reasons": reasons}

    def apply_helper_models(self) -> None:
        """Classify after all use/mod/macro bindings and duplicate contexts exist."""
        analysis = self.config.get("analysis", {})
        profiles = analysis.get("rust_helper_profiles", [])
        support = analysis.get("_captured_support_inputs", {})
        for node_id, scope, binding, attributes, kind in self.type_items:
            if not any(_attribute_name(attr) == "serde" for attr in attributes):
                continue
            node = self.nodes[node_id]
            environment = self.model_environment(scope)
            crate_root = posixpath.dirname(posixpath.dirname(scope.unit))
            selected = [profile for profile in profiles if isinstance(profile, dict)
                and profile.get("crate_root") == crate_root]
            workspace_manifest = selected[0].get("workspace_manifest", "Cargo.toml") if len(selected) == 1 else "Cargo.toml"
            context_ok = not any(node.metadata.get(key) for key in (
                "duplicate_definition", "multiple_module_contexts"))
            result = classify_rust_item_helpers(attributes, profiles=profiles, support_inputs=support,
                crate_root=crate_root, workspace_manifest=workspace_manifest,
                item_file=node.file, item_kind=kind,
                shadowed_names=set(environment["shadowed_names"]),
                bindings_complete=environment["bindings_complete"] and context_ok,
                source_complete=environment["source_complete"] and context_ok,
                generic=bool(node.metadata.get("generic_definition")),
                conditional=bool(node.metadata.get("conditional_definition")),
                macro_scope_unknown=environment["macro_scope_unknown"] or bool(node.metadata.get("helper_nested_model_gaps")))
            result["namespace_evidence"] = environment
            node.metadata["derive_helper_model"] = result
            if not result.get("accepted"):
                continue
            accepted = set(result.get("helper_attribute_indices", []))
            if not accepted or any(type(index) is not int or not 0 <= index < len(attributes) for index in accepted):
                result.update(accepted=False, reasons=["helper model returned invalid attribute indices"])
                continue
            remaining = [attribute for index, attribute in enumerate(attributes) if index not in accepted]
            node.metadata["attribute_macros_unknown"] = scope.opaque or _opaque(remaining)
            binding.conditional = bool(node.metadata.get("conditional_definition")) or scope.opaque or _opaque(remaining)
            node.metadata["generated_members_unknown"] = True


class _Resolver:
    def __init__(self, index: _Index):
        self.index = index

    def uncertain(self, ref: _Ref, reason: str, resolution: str = "dynamic") -> _Ref:
        return _Ref(resolution, ref.kind, modules=ref.modules,
            candidates=sorted(set([*ref.candidates, *([ref.target] if ref.target else [])])),
            reason=reason, external=ref.external, metadata=dict(ref.metadata))

    def symbol(self, binding: _Binding, *, lexical_impl: _Scope | None = None) -> _Ref:
        node = self.index.nodes.get(binding.target)
        if node is None:
            return _Ref("unresolved", reason="声明目标没有被捕获")
        kind = "type" if binding.kind == "type" else "function"
        ref = _Ref("resolved", kind, target=node.id)
        if node.metadata.get("duplicate_definition") or node.metadata.get("multiple_module_contexts"):
            return self.uncertain(ref, "目标存在重名声明或多个 crate 上下文", "ambiguous")
        if node.metadata.get("conditional_definition") or binding.conditional:
            return self.uncertain(ref, "目标受 cfg/属性宏影响，未选择构建配置")
        if node.metadata.get("attribute_macros_unknown"):
            return self.uncertain(ref, "属性宏可能变换声明，未展开")
        same_impl = bool(lexical_impl is not None and binding.scope is lexical_impl
            and self.index.nodes_scopes.get(node.id) is lexical_impl and not lexical_impl.trait_impl)
        if node.metadata.get("impl_generic") and not same_impl:
            return self.uncertain(ref, "泛型/特化 impl 的具体参数与约束未匹配")
        if node.metadata.get("declaration_only") or node.metadata.get("trait_dispatch"):
            return self.uncertain(ref, "声明无实现体或涉及 trait 分派")
        if binding.scope.file.source.status != "parsed":
            return self.uncertain(ref, "目标文件存在语法解析失败")
        return ref

    def module_ref(self, scopes: list[_Scope]) -> _Ref:
        unique = {(scope.unit, scope.namespace, scope.file.source.path, scope.start): scope for scope in scopes}
        scopes = list(unique.values())
        if not scopes:
            return _Ref("unresolved", "module", reason="模块源码未捕获或路径未解析")
        if len(scopes) != 1:
            return _Ref("ambiguous", "module", modules=scopes, reason="模块映射存在多个候选")
        scope = scopes[0]
        return _Ref("dynamic" if scope.cfg or scope.opaque else "resolved", "module", modules=scopes,
            reason="模块受 cfg/属性宏影响" if scope.cfg or scope.opaque else "")

    def lookup(self, scope: _Scope, name: str, position: int) -> list[_Binding]:
        crossed_function = False
        current: _Scope | None = scope
        while current is not None:
            bindings = current.bindings.get(name, [])
            # Associated functions/constants do not enter bare-name lexical
            # lookup in an impl/trait body; Self::name is a separate path.
            if current.kind in {"impl", "trait"}:
                bindings = [x for x in bindings if x.kind == "generic"]
            variables = [x for x in bindings if x.kind in {"variable", "alias", "self_receiver"} and x.start <= position]
            if variables and not crossed_function:
                newest = max(x.start for x in variables)
                return [x for x in variables if x.start == newest]
            items = [x for x in bindings if x.kind not in {"variable", "alias", "self_receiver"}]
            if items:
                return items
            if current.kind == "function":
                crossed_function = True
            current = current.parent
        return []

    def binding(self, binding: _Binding, position: int, seen: set[tuple]) -> _Ref:
        if binding.kind in {"symbol", "type"}:
            return self.symbol(binding)
        if binding.kind in {"variable", "self_receiver"}:
            return _Ref("dynamic", reason="局部变量/参数/函数指针的运行时值未推断")
        if binding.kind == "generic":
            return _Ref("dynamic", "type", reason="泛型/trait 约束的具体类型未推断")
        if binding.kind == "extern_crate":
            name = binding.path[0]
            ref = self.module_ref(self.index.crates[name]) if name in self.index.crates else _Ref("external", "external", external=name)
            return self.uncertain(ref, "extern crate 绑定受cfg影响") if binding.conditional else ref
        if binding.kind == "module":
            ref = self.module_ref(binding.modules)
        else:
            key = (id(binding), tuple(binding.path))
            if key in seen or len(seen) > 96:
                return _Ref("ambiguous", reason="use/别名循环或解析预算不足")
            same_name = self.lookup(binding.scope, binding.path[0], position) if binding.path else []
            if binding.kind == "import" and len(binding.path) == 1 and len(same_name) == 1 and same_name[0] is binding:
                name = binding.path[0]
                ref = self.module_ref(self.index.crates[name]) if name in self.index.crates else _Ref("external", "external", external=name)
            else:
                ref = self.path(binding.path, binding.scope,
                    binding.value_position if binding.kind == "alias" else position, {*seen, key})
        return self.uncertain(ref, "绑定受 cfg/属性宏影响") if binding.conditional else ref

    def combine(self, refs: list[_Ref]) -> _Ref:
        if len(refs) == 1:
            return refs[0]
        if refs and all(r.kind == "module" for r in refs):
            combined = self.module_ref([m for ref in refs for m in ref.modules])
            if any(ref.resolution != "resolved" for ref in refs):
                return self.uncertain(combined, "模块名称存在条件性或不确定的多重绑定", "ambiguous")
            return combined
        candidates = sorted({t for r in refs for t in [*r.candidates, *([r.target] if r.target else [])]})
        return _Ref("ambiguous", candidates=candidates, reason="名称存在多个静态绑定，不能选择唯一目标")

    def named(self, name: str, scope: _Scope, position: int, seen: set[tuple]) -> _Ref:
        if name == "Self":
            ref = self.concrete_self_type(scope)
            ref.metadata["receiver_form"] = "Self::"
            return ref
        bindings = self.lookup(scope, name, position)
        if bindings:
            ref = self.combine([self.binding(x, position, seen) for x in bindings])
            current: _Scope | None = scope
            while current:
                if current.macro_bindings_unknown:
                    return self.uncertain(ref, "当前词法作用域含未展开宏，可能引入同名绑定")
                current = current.parent
            return ref
        if name in self.index.crates:
            return self.module_ref(self.index.crates[name])
        if name in _PRELUDE_CONSTRUCTORS or name in _PRELUDE_FUNCTIONS:
            return _Ref("external", "external", external=name, reason="Rust 标准 prelude 边界")
        current: _Scope | None = scope
        while current:
            if current.stars:
                return _Ref("unresolved", reason="星号导入的导出集合未推断")
            current = current.parent
        return _Ref("unresolved", reason="没有可确定的词法声明；不等同于已证明实现缺失")

    def concrete_self_type(self, scope: _Scope) -> _Ref:
        current: _Scope | None = scope
        while current is not None and current.kind != "function":
            if current.macro_bindings_unknown:
                return _Ref("dynamic", "type", reason="接收者作用域含未展开宏，绑定来源不完整")
            current = current.parent
        if current is None or current.parent is None or current.parent.kind != "impl":
            return _Ref("dynamic", "type", reason="Self 不在直接所属的具体 impl 方法中；不借用嵌套函数的外层类型")
        impl = current.parent
        source = self.index.nodes.get(current.owner)
        metadata = {"receiver_type_name": impl.impl_type_text,
            "receiver_impl_location": dict(impl.impl_location),
            "receiver_impl_trait": impl.impl_trait,
            "receiver_impl_is_trait": impl.trait_impl}
        candidates = [impl.impl_target] if impl.impl_target else []
        if source and (source.metadata.get("duplicate_definition") or source.metadata.get("multiple_module_contexts")):
            return _Ref("ambiguous", "type", candidates=candidates,
                reason="调用者具有重复声明或多个模块上下文", metadata=metadata)
        if impl.impl_generic:
            return _Ref("dynamic", "type", candidates=candidates,
                reason="泛型/特化/where impl 的具体接收者参数未匹配", metadata=metadata)
        if impl.cfg or impl.opaque or scope.cfg or scope.opaque or current.macro_bindings_unknown:
            return _Ref("dynamic", "type", candidates=candidates,
                reason="接收者源码受 cfg/属性宏或未展开宏影响", metadata=metadata)
        if impl.file.source.status != "parsed" or scope.file.source.status != "parsed":
            return _Ref("dynamic", "type", candidates=candidates,
                reason="接收者实现来源未完整解析", metadata=metadata)
        if impl.impl_target is None:
            return _Ref("dynamic", "type", reason=impl.impl_resolution_reason or "impl 接收者类型没有唯一捕获声明",
                metadata=metadata)
        declared_type = self.index.nodes[impl.impl_target]
        if declared_type.metadata.get("generic_definition") or declared_type.metadata.get("type_alias_unknown") or declared_type.kind == "trait":
            return _Ref("dynamic", "type", candidates=candidates,
                reason="泛型类型、类型别名或 trait 接收者不作具体方法绑定", metadata=metadata)
        if declared_type.metadata.get("duplicate_definition") or declared_type.metadata.get("multiple_module_contexts"):
            return _Ref("ambiguous", "type", candidates=candidates,
                reason="接收者类型具有重复声明或多个模块上下文", metadata=metadata)
        metadata.update({"receiver_type": declared_type.id,
            "receiver_type_declaration": dict(declared_type.metadata["declaration_location"]),
            "concrete_self": True})
        return _Ref("resolved", "type", target=declared_type.id, metadata=metadata)

    def generic_impl_member(self, name: str, scope: _Scope, position: int,
                            call_node: Any, *, instance: bool) -> _Ref | None:
        """A captured lexical relation, never generic Rust type inference.

        This route selects only a declaration in the caller's exact impl AST
        scope. Erased type identities are used solely to refuse competing
        declarations, not to choose a generic implementation. Macros outside
        visible ancestor scopes remain explicit residual boundaries.
        """
        source_scope: _Scope | None = scope
        while source_scope is not None and source_scope.kind != "function":
            if source_scope.kind == "closure":
                return None
            source_scope = source_scope.parent
        if source_scope is None or source_scope.parent is None or source_scope.parent.kind != "impl":
            return None
        impl = source_scope.parent
        if not impl.impl_generic:
            return None
        source = self.index.nodes.get(source_scope.owner)
        bindings = impl.bindings.get(name, [])
        candidates = sorted({binding.target for binding in bindings if binding.target})
        metadata: dict[str, Any] = {"generic_impl_binding": {
            "model_id": _GENERIC_IMPL_MODEL,
            "basis": "captured_same_inherent_impl_lexical_declaration_relation",
            "same_impl_identity": {"file": impl.file.source.path, "source_hash": impl.file.source.hash,
                "start_byte": impl.start, "end_byte": impl.impl_end_byte,
                "declaration_location": dict(impl.impl_location), "header": impl.impl_header},
            "receiver_form": "self." if instance else "Self::",
            "source_method": source_scope.owner,
            "source_declaration": dict(source.metadata.get("declaration_location", {})) if source else {},
            "generic_instantiation_verified": False, "bounds_not_verified": True,
            "argument_types_verified": False, "execution_verified": False,
            "compiler_namespace_complete": False, "macro_expansion_performed": False,
            "residual_boundaries": ["unexpanded macros outside visible ancestor scopes",
                "generated definitions, trait bodies and implicit calls are not closed",
                "argument values, generic instantiations and bounds are not verified"],
            "assumptions": ["the captured declarations retain their explicit lexical structure",
                "receiver lookup is restricted to an unambiguous direct same-impl declaration",
                "unmodeled compiler or macro namespaces may add further behavior"]}}

        def decline(reason: str, resolution: str = "dynamic") -> _Ref:
            return _Ref(resolution, candidates=candidates[:64], reason=reason, metadata=metadata)

        if impl.trait_impl:
            return decline("同 impl 泛型词法模型仅支持固有 impl，不推断 trait 分派")
        source_environment = self.index.model_environment(scope)
        metadata["generic_impl_binding"]["source_namespace_evidence"] = source_environment
        if not (source_environment["source_complete"] and source_environment["bindings_complete"]
                and not source_environment["macro_scope_unknown"]):
            return decline("同 impl 泛型词法来源受未捕获/重复模块、cfg、属性宏、可见宏或未建模绑定影响")
        if source is None or source.kind != "method" or self.index.nodes_scopes.get(source.id) is not impl:
            return decline("调用者不是该固有 impl 直接所属的唯一方法")
        if source.metadata.get("method_constraint_gaps"):
            return decline("调用者具有额外方法泛型/where/匿名类型或参数属性约束，未验证")
        if len(bindings) != 1 or bindings[0].kind != "symbol" or not bindings[0].target:
            return decline("同一个固有 impl 中没有唯一目标方法声明", "ambiguous" if len(bindings) > 1 else "dynamic")
        target = self.index.nodes.get(bindings[0].target)
        if target is None or target.kind != "method" or self.index.nodes_scopes.get(target.id) is not impl:
            return decline("目标声明没有唯一的同 impl 语法身份")
        metadata["generic_impl_binding"].update({"target_method": target.id,
            "target_declaration": dict(target.metadata.get("declaration_location", {})),
            "source_method_constraint_gaps": list(source.metadata.get("method_constraint_gaps", [])),
            "target_method_constraint_gaps": list(target.metadata.get("method_constraint_gaps", []))})
        if target.metadata.get("method_constraint_gaps"):
            return decline("目标具有独立方法泛型/where/匿名类型或参数属性约束，未验证")
        target_scopes = self.index.function_scopes.get(target.id, [])
        if len(target_scopes) != 1 or target_scopes[0].parent is not impl:
            return decline("目标实现体缺失或具有重复源码身份", "ambiguous" if len(target_scopes) > 1 else "dynamic")
        target_environment = self.index.model_environment(target_scopes[0])
        metadata["generic_impl_binding"]["target_namespace_evidence"] = target_environment
        if not (target_environment["source_complete"] and target_environment["bindings_complete"]
                and not target_environment["macro_scope_unknown"]):
            return decline("目标声明/可见实现作用域受 cfg、属性宏、可见宏或不完整绑定影响")
        if instance:
            receiver_bindings = self.lookup(scope, "self", position)
            if (len(receiver_bindings) != 1 or receiver_bindings[0].kind != "self_receiver"
                    or receiver_bindings[0].scope is not source_scope
                    or not source.metadata.get("plain_self_receiver")):
                return decline("接收者不是该方法直接声明的原生 self/&self/&mut self")
        elif not target.metadata.get("static_method"):
            return decline("泛型 Self:: 首版仅绑定同 impl 无 self 接收者的固有函数")
        function = call_node.child_by_field_name("function")
        if function is not None and function.type == "generic_function":
            return decline("显式调用类型参数未匹配；同 impl 模型不擦除 turbofish")
        arguments = call_node.child_by_field_name("arguments")
        argument_count = len([argument for argument in arguments.named_children
            if argument.type not in {"line_comment", "block_comment"}]) if arguments else 0
        expected_count = target.metadata.get("value_parameter_count", 0) - (1 if instance else 0)
        metadata["generic_impl_binding"]["explicit_argument_count"] = argument_count
        metadata["generic_impl_binding"]["target_explicit_parameter_count"] = expected_count
        if argument_count != expected_count:
            return decline("显式实参数量与目标参数声明不匹配；不证明可调用性")
        if impl.impl_target is None:
            return decline(impl.impl_resolution_reason or "impl 的接收者类型声明未唯一捕获")
        declared = self.index.nodes[impl.impl_target]
        declaration_ref = self.symbol(_Binding("type", target=declared.id, scope=impl.parent))
        if (declaration_ref.resolution != "resolved" or declared.kind == "trait"
                or declared.metadata.get("type_alias_unknown")):
            return decline("同 impl 的接收者类型声明受歧义/属性宏/别名影响")
        has_derives = any(_attribute_name(attribute) == "derive"
            for attribute in declared.metadata.get("attributes", []))
        helper_interface = declared.metadata.get("derive_helper_model", {}).get("receiver_interface_model", {})
        if has_derives and not helper_interface.get("complete_within_profile"):
            return decline("泛型接收者带未建模 derive；生成成员或 Deref 竞争不能排除")
        ref = _Ref("resolved", "type", target=declared.id, metadata={**metadata,
            "receiver_type": declared.id, "receiver_type_name": impl.impl_type_text,
            "receiver_type_declaration": dict(declared.metadata.get("declaration_location", {})),
            "receiver_impl_location": dict(impl.impl_location),
            "receiver_impl_trait": impl.impl_trait, "receiver_impl_is_trait": False,
            "receiver_form": "self." if instance else "Self::",
            "receiver_parameter": source.metadata.get("self_parameter", "")})
        result = self.inherent_member(ref, name, instance=instance, lexical_impl=impl)
        if result.resolution == "resolved":
            result.metadata["binding_basis"] = "rust.generic_same_impl_self_method" if instance else "rust.generic_same_impl_associated_function"
        return result

    def inherent_member(self, ref: _Ref, name: str, *, instance: bool = False,
                        lexical_impl: _Scope | None = None) -> _Ref:
        if ref.resolution != "resolved" or ref.target is None:
            return ref
        node = self.index.nodes[ref.target]
        same_impl = bool(lexical_impl is not None and lexical_impl.impl_target == ref.target
            and ref.metadata.get("generic_impl_binding", {}).get("model_id") == _GENERIC_IMPL_MODEL)
        if node.metadata.get("type_alias_unknown") or node.kind == "trait" or (node.metadata.get("generic_definition") and not same_impl):
            return self.uncertain(ref, "泛型类型/别名/trait 关联目标未推断")
        use_instance_members = instance or ref.metadata.get("concrete_self")
        registry = self.index.inherent_methods if use_instance_members else self.index.associated
        targets = sorted(set(registry.get((ref.target, name), [])))
        if same_impl:
            targets = sorted({binding.target for binding in lexical_impl.bindings.get(name, [])
                if binding.kind == "symbol" and binding.target})
            others = sorted(set(self.index.inherent_methods.get((ref.target, name), [])) - set(targets))
            if others:
                return _Ref("ambiguous", candidates=sorted(set(targets + others))[:64],
                    reason="其它捕获 impl 有同名固有声明；未比较泛型特化/约束或方法优先级", metadata=dict(ref.metadata))
        trait_targets = sorted(set(self.index.trait_methods.get((ref.target, name), [])))
        helper = node.metadata.get("derive_helper_model", {})
        if helper.get("accepted"):
            interface = helper.get("receiver_interface_model", {})
            ref.metadata["receiver_helper_model"] = {"receiver_type": node.id,
                "model_version": helper.get("model_version"), "profile_id": helper.get("profile_id"),
                "registration": helper.get("registration"), "providers": helper.get("providers", []),
                "namespace_evidence": helper.get("namespace_evidence", {}),
                "receiver_interface_model": interface,
                "generated_members_unknown": True, "macro_expansion_performed": False}
            if not interface.get("complete_within_profile") or name in interface.get("member_names", []):
                return _Ref("dynamic", candidates=targets[:64],
                    reason="derive 生成的接收者接口不完整或包含同名成员，不能排除生成 trait/默认方法竞争",
                    metadata=dict(ref.metadata))
        interfaces = self.index.modeled_trait_interfaces.get(ref.target, [])
        if interfaces:
            ref.metadata["receiver_standard_interface_models"] = interfaces
            if any(name in interface["member_names"] for interface in interfaces):
                return _Ref("dynamic", candidates=targets[:64],
                    reason="显式标准接口模型包含同名 trait/超 trait/默认成员，不选择其分派",
                    metadata=dict(ref.metadata))
        unmodeled_traits = self.index.unmodeled_trait_members.get(name, [])
        if unmodeled_traits:
            return _Ref("dynamic", candidates=targets[:64],
                reason="未解析的引用/泛型 trait 接收者存在同名成员，不能排除接收器调整后选择该实现",
                metadata={**ref.metadata, "unmodeled_trait_impl_count": len(unmodeled_traits),
                    "unmodeled_trait_impl_locations": unmodeled_traits[:8]})
        if ref.target in self.index.unknown_trait_default_types or self.index.unknown_trait_default_receivers:
            return _Ref("dynamic", candidates=targets[:64],
                reason="相关 trait 的声明/默认成员来源不完整，不能排除默认方法影响接收器选择",
                metadata={**ref.metadata, "trait_default_members_unknown": True,
                    "unmodeled_trait_receiver_count": len(self.index.unknown_trait_default_receivers)})
        if ref.target in self.index.deref_types:
            return _Ref("dynamic", candidates=targets[:64],
                reason="接收者存在 Deref 或无法排除的解引用调整实现，未分析方法调整与分派", metadata=dict(ref.metadata))
        if trait_targets:
            return _Ref("ambiguous" if targets else "dynamic", candidates=sorted(set(targets + trait_targets))[:64],
                reason="同一接收者类型存在 trait 同名成员；不选择 trait 或推断调整顺序", metadata=dict(ref.metadata))
        if not targets:
            return _Ref("dynamic", reason="该具体类型没有唯一捕获的固有方法；不按全局方法名猜测",
                metadata=dict(ref.metadata))
        target_refs = []
        for target in targets:
            target_scope = self.index.nodes_scopes[target]
            target_node = self.index.nodes[target]
            target_ref = self.symbol(_Binding("symbol", target=target, scope=target_scope),
                lexical_impl=lexical_impl if same_impl else None)
            if target_scope.cfg or target_scope.opaque or (target_scope.impl_generic and target_scope is not lexical_impl):
                target_ref = self.uncertain(target_ref, "目标 impl 的配置/宏/类型参数未确定")
            if instance and (target_node.metadata.get("static_method") or not target_node.metadata.get("plain_self_receiver")):
                target_ref = self.uncertain(target_ref, "目标不是支持的直接 self 接收者方法")
            if instance:
                source_receiver = str(ref.metadata.get("receiver_parameter", ""))
                target_receiver = str(target_node.metadata.get("self_parameter", ""))
                needs_mutable = target_receiver.startswith("&") and bool(re.search(r"\bmut\b", target_receiver))
                needs_owned = bool(target_receiver) and not target_receiver.startswith("&")
                if (needs_mutable and not re.search(r"\bmut\b", source_receiver)) or (
                    needs_owned and source_receiver.startswith("&")
                ):
                    target_ref = self.uncertain(target_ref, "接收者借用/所有权形式不匹配，不能排除调整后的其他方法")
            target_refs.append(target_ref)
        result = self.combine(target_refs)
        result.metadata.update(ref.metadata)
        if result.resolution == "resolved" and result.target:
            target = self.index.nodes[result.target]
            target_impl = self.index.nodes_scopes[result.target]
            result.metadata.update({"target_declaration": dict(target.metadata["declaration_location"]),
                "target_impl_location": dict(target_impl.impl_location),
                "binding_basis": "rust.explicit_self_associated_path" if ref.metadata.get("concrete_self")
                    else "rust.explicit_type_associated_function"})
        return result

    def self_method(self, expression: Any, scope: _Scope, position: int, call_node: Any) -> _Ref:
        receiver = expression.child_by_field_name("value")
        member = _name(_text(expression.child_by_field_name("field"), scope.file.raw))
        if receiver is None or receiver.type != "self":
            return _Ref("dynamic", candidates=sorted(self.index.method_names.get(member, set()))[:64],
                reason="字段/变量/表达式接收者、trait 和 Deref 分派未推断；同名仅为候选")
        bindings = self.lookup(scope, "self", position)
        if len(bindings) != 1 or bindings[0].kind != "self_receiver":
            return _Ref("dynamic", reason="self 参数不是直接 self/&self/&mut self，或其绑定来源不唯一")
        generic_ref = self.generic_impl_member(member, scope, position, call_node, instance=True)
        if generic_ref is not None:
            generic_ref.metadata["receiver_binding_location"] = dict(bindings[0].location)
            return generic_ref
        ref = self.concrete_self_type(scope)
        caller = self.index.nodes.get(bindings[0].scope.owner)
        ref.metadata.update({"receiver_form": "self.", "receiver_binding_location": dict(bindings[0].location),
            "receiver_parameter": caller.metadata.get("self_parameter", "") if caller else ""})
        result = self.inherent_member(ref, member, instance=True)
        if result.resolution == "resolved":
            result.metadata["binding_basis"] = "rust.concrete_self_in_trait_impl" if ref.metadata.get("receiver_impl_is_trait") else "rust.inherent_self_method"
        return result

    def member(self, ref: _Ref, name: str, position: int, seen: set[tuple]) -> _Ref:
        if ref.kind == "external":
            return _Ref("external", "external", external=ref.external + "::" + name, reason=ref.reason)
        if ref.kind == "module" and ref.modules:
            child_refs = []
            for module in ref.modules:
                bindings = module.bindings.get(name, [])
                if bindings:
                    child_refs.append(self.combine([self.binding(x, position, seen) for x in bindings]))
                else:
                    child_refs.append(_Ref("unresolved", reason="模块中没有可确定的显式导出或声明"))
            result = self.combine(child_refs)
            if ref.resolution != "resolved":
                return self.uncertain(result, ref.reason or "模块上下文不确定", ref.resolution)
            return result
        if ref.kind == "type" and ref.target:
            return self.inherent_member(ref, name)
        return _Ref(ref.resolution if ref.resolution != "resolved" else "dynamic", candidates=ref.candidates,
            reason=ref.reason or "限定路径不能解析为模块或具体类型", metadata=dict(ref.metadata))

    def path(self, parts: list[str], scope: _Scope, position: int, seen: set[tuple] | None = None) -> _Ref:
        seen = seen or set()
        if not parts:
            return _Ref("dynamic", reason="调用表达式不是支持的静态路径")
        module = scope.module
        first, remaining = parts[0], list(parts[1:])
        if first == "crate":
            if not module.known_unit:
                return _Ref("unresolved", reason="该文件没有已配置的 crate 根上下文")
            ref = self.module_ref([self.index.roots[module.unit]])
        elif first == "self":
            ref = self.module_ref([module])
        elif first == "super":
            current = module.parent_module
            while remaining and remaining[0] == "super":
                current = current.parent_module if current else None
                remaining.pop(0)
            ref = self.module_ref([current] if current else [])
        elif first == "::":
            if not remaining:
                return _Ref("unresolved", reason="空的绝对 Rust 路径")
            name = remaining.pop(0)
            ref = self.module_ref(self.index.crates[name]) if name in self.index.crates else _Ref("external", "external", external=name)
        else:
            ref = self.named(first, scope, position, seen)
            if ref.resolution == "unresolved" and remaining and not self.lookup(scope, first, position):
                ref = _Ref("external", "external", external=first,
                    reason="路径根不在配置的内部 crate/module 中；外部绑定未验证")
        for part in remaining:
            ref = self.member(ref, part, position, seen)
        return ref

    def eq_interface_model(self, impl: _Scope, receiver: str) -> dict[str, Any] | None:
        """Use an opted-in standard interface assumption, never an Eq whitelist.

        This models possible receiver member names, including PartialEq and
        Eq's hidden helper. It neither provides a captured trait body nor
        claims the project's unspecified toolchain implements this interface.
        """
        enabled = self.index.config.get("analysis", {}).get("rust_interface_models", [])
        if _EQ_INTERFACE_MODEL not in enabled or impl.impl_trait_path != ["Eq"]:
            return None
        if impl.impl_generic or impl.cfg or impl.opaque or impl.macro_bindings_unknown:
            return None
        if impl.parent is None or self.lookup(impl.parent, "Eq", impl.start) or "Eq" in self.index.crates:
            return None
        node = self.index.nodes[receiver]
        # A trusted Eq interface must not remove an unknown derive's ability
        # to add receiver members/Deref. Only the separate accepted helper
        # profile supplies that stronger, explicitly scoped interface premise.
        derives = any(_attribute_name(attr) == "derive" for attr in node.metadata.get("attributes", []))
        helper = node.metadata.get("derive_helper_model", {})
        if derives and not (helper.get("accepted") and helper.get("receiver_interface_model", {}).get("complete_within_profile")):
            return None
        environment = self.index.model_environment(impl.parent)
        if not (environment["source_complete"] and environment["bindings_complete"]
                and environment["prelude_enabled"] and not environment["macro_scope_unknown"]):
            return None
        if {"Eq", "core", "std"} & set(environment["shadowed_names"]):
            return None
        if any(name not in _EQ_INTERFACE_MEMBERS for name in impl.bindings):
            return None
        return {"id": _EQ_INTERFACE_MODEL, "trait": "core::cmp::Eq",
            "supertraits": ["core::cmp::PartialEq<Self>"], "member_names": sorted(_EQ_INTERFACE_MEMBERS),
            "basis": "explicit_versioned_trusted_standard_interface_assumption",
            "registration": "analysis.rust_interface_models",
            "source_references": ["https://doc.rust-lang.org/core/cmp/trait.Eq.html",
                "https://github.com/rust-lang/rust/blob/1.85.0/library/core/src/cmp.rs"],
            "standard_library_source_captured": False, "project_toolchain_verified": False,
            "complete_within_model": True, "trait_bodies_known": False,
            "namespace_evidence": environment, "impl_location": dict(impl.impl_location),
            "receiver_type": receiver,
            "assumptions": ["unshadowed implicit Rust prelude Eq uses the registered member-name interface",
                "the model is not tied to or verified against the project's actual standard-library version",
                "unmodeled trait implementations, macros and generated bodies remain unknown"]}

    def prepare_impls(self) -> None:
        for impl in self.index.impls:
            for bindings in impl.bindings.values():
                for binding in bindings:
                    if binding.target:
                        self.index.nodes_scopes[binding.target] = impl
            trait_members: dict[str, list[str]] = {}
            trait_complete = not impl.trait_impl
            trait_ref = _Ref("unresolved")
            if impl.trait_impl:
                trait_ref = self.path(impl.impl_trait_path, impl.parent, impl.start) if impl.impl_trait_path else trait_ref
                trait_ids = [*trait_ref.candidates, *([trait_ref.target] if trait_ref.target else [])]
                for trait_id in sorted(set(trait_ids)):
                    trait_node = self.index.nodes.get(trait_id)
                    if trait_node is None or trait_node.kind != "trait":
                        continue
                    for name, targets in self.index.trait_declaration_members.get(trait_id, {}).items():
                        trait_members.setdefault(name, []).extend(targets)
                    source = self.index.files.get(trait_node.file)
                    trait_complete = bool(trait_ref.resolution == "resolved" and trait_ref.target == trait_id
                        and source and source.source.status == "parsed"
                        and not any(trait_node.metadata.get(key) for key in (
                            "duplicate_definition", "multiple_module_contexts", "conditional_definition", "attribute_macros_unknown")))

            def record_unmodeled_trait_members() -> None:
                if impl.trait_impl:
                    names = set(trait_members)
                    names.update(name for name, bindings in impl.bindings.items()
                        if any(self.index.nodes.get(binding.target)
                            and self.index.nodes[binding.target].kind == "method" for binding in bindings))
                    for name in names:
                        self.index.unmodeled_trait_members.setdefault(name, []).append(dict(impl.impl_location))
                    if not trait_complete:
                        base_ref = self.path(impl.impl_receiver_base, impl.parent, impl.start) if impl.impl_receiver_base else _Ref("unresolved")
                        possible_types = set([*base_ref.candidates, *([base_ref.target] if base_ref.target else [])])
                        possible_types = {target for target in possible_types if target in self.index.nodes
                            and self.index.nodes[target].kind == "type"
                            and not self.index.nodes[target].metadata.get("type_alias_unknown")}
                        if possible_types:
                            self.index.unknown_trait_default_types.update(possible_types)
                        else:
                            self.index.unknown_trait_default_receivers.append(dict(impl.impl_location))
            if impl.trait_impl and impl.impl_generic:
                record_unmodeled_trait_members()
            if not impl.impl_type:
                if not impl.impl_generic:
                    record_unmodeled_trait_members()
                impl.impl_resolution_reason = "impl 类型不是受支持的显式路径"
                continue
            ref = self.path(impl.impl_type, impl.parent, impl.start)
            if ref.kind != "type" or ref.resolution != "resolved" or not ref.target:
                if not impl.impl_generic:
                    record_unmodeled_trait_members()
                impl.impl_resolution_reason = ref.reason or "impl 类型没有唯一已解析声明"
                continue
            impl.impl_target = ref.target
            if impl.trait_impl:
                if not trait_complete:
                    model = self.eq_interface_model(impl, ref.target)
                    if model is not None:
                        trait_complete = True
                        self.index.modeled_trait_interfaces.setdefault(ref.target, []).append(model)
                        self.index.nodes[ref.target].metadata.setdefault("standard_trait_interface_models", []).append(model)
                for name, targets in trait_members.items():
                    self.index.trait_methods.setdefault((ref.target, name), []).extend(targets)
                if not trait_complete:
                    self.index.unknown_trait_default_types.add(ref.target)
                names = {impl.impl_trait.rsplit("::", 1)[-1], trait_ref.external.rsplit("::", 1)[-1]}
                for target in [*trait_ref.candidates, *([trait_ref.target] if trait_ref.target else [])]:
                    if target in self.index.nodes:
                        names.add(self.index.nodes[target].name)
                if names & {"Deref", "DerefMut"} or (
                    trait_ref.resolution != "resolved" and any(name in impl.bindings for name in {"deref", "deref_mut"})
                ) or impl.opaque or impl.macro_bindings_unknown:
                    self.index.deref_types.add(ref.target)
            for name, bindings in impl.bindings.items():
                for binding in bindings:
                    node = self.index.nodes.get(binding.target)
                    if node is None or node.kind != "method":
                        continue
                    node.metadata["impl_type_id"] = ref.target
                    registry = self.index.trait_methods if impl.trait_impl else self.index.inherent_methods
                    registry.setdefault((ref.target, name), []).append(node.id)
                    if not impl.trait_impl and not impl.impl_generic and not impl.cfg and not impl.opaque and (
                        node.metadata.get("static_method") and not node.metadata.get("trait_dispatch")
                    ):
                        self.index.associated.setdefault((ref.target, name), []).append(node.id)

    def callable_arguments(self, call: _Call, target: str | None) -> list[str]:
        arguments = call.node.child_by_field_name("arguments")
        if not arguments:
            return []
        values = []
        expected = self.index.callable_parameters.get(target or "", set())
        for i, argument in enumerate(arguments.named_children):
            if i in expected or argument.type in {"closure_expression", "async_block"}:
                values.append(_text(argument, call.scope.file.raw, 160))
                continue
            parts = _segments(argument, call.scope.file.raw)
            if parts:
                ref = self.path(parts, call.scope, argument.start_byte)
                if ref.kind == "function" or any(binding.callable for binding in self.lookup(call.scope, parts[0], argument.start_byte)):
                    values.append(_text(argument, call.scope.file.raw, 160))
        return values

    def edges(self) -> list[Edge]:
        output: dict[str, Edge] = {}
        for call in self.index.calls:
            node, scope = call.node, call.scope
            expression_node = node.child_by_field_name("macro") if call.macro else node.child_by_field_name("function")
            while expression_node and expression_node.type == "generic_function":
                expression_node = expression_node.child_by_field_name("function")
            expression = _text(expression_node, scope.file.raw, 600) or _text(node, scope.file.raw, 160)
            metadata: dict[str, Any] = {"language": "rust", "cfg_conditions": list(dict.fromkeys([*scope.cfg, *_cfg(call.attrs)])),
                "crate_root": scope.unit, "rust_namespace": "::".join(scope.namespace),
                "source_body_only": True}
            if call.closure_definition:
                ref = _Ref("dynamic", candidates=[call.closure_definition], reason="闭包/Future 构造不证明调用或轮询其主体")
                metadata["closure_activation_unknown"] = True
            elif call.macro:
                ref = _Ref("dynamic", reason="宏未展开；生成的调用/声明与隐式行为未知")
                metadata["macro_unknown"] = True
                metadata["callbacks_unknown"] = True
            elif expression_node and expression_node.type == "field_expression":
                ref = self.self_method(expression_node, scope, node.start_byte, node)
            else:
                parts = _segments(expression_node, scope.file.raw)
                generic_ref = self.generic_impl_member(parts[1], scope, node.start_byte, node, instance=False) if parts and len(parts) == 2 and parts[0] == "Self" else None
                ref = generic_ref if generic_ref is not None else self.path(parts, scope, node.start_byte) if parts else _Ref("dynamic", reason="函数值/UFCS/表达式调用未静态绑定")
                if ref.resolution == "resolved" and ref.kind != "function":
                    if ref.kind == "type":
                        ref = _Ref("external", "external", external=expression, reason="类型/变体构造没有显式函数实现体")
                    else:
                        ref = self.uncertain(ref, "调用路径未绑定到函数实现体")
            metadata.update(ref.metadata)
            current: _Scope | None = scope
            inside_closure = False
            while current:
                inside_closure = inside_closure or current.kind == "closure"
                current = current.parent
            if inside_closure and ref.resolution == "resolved":
                ref = self.uncertain(ref, "闭包/Future 的执行和捕获绑定未验证")
                metadata["closure_activation_unknown"] = True
            if metadata["cfg_conditions"] and ref.resolution == "resolved":
                ref = self.uncertain(ref, "调用所在源码受cfg条件影响，未选择构建配置")
            if scope.opaque or _opaque(call.attrs):
                metadata["source_attribute_macros_unknown"] = True
                if ref.resolution == "resolved":
                    ref = self.uncertain(ref, "源码主体受未知属性宏影响，未展开宏后的调用不确定")
            if scope.file.source.status != "parsed":
                metadata["source_parse_partial"] = True
                if ref.resolution == "resolved":
                    ref = self.uncertain(ref, "调用所在文件存在语法解析失败")
            if self.index.nodes.get(scope.owner) and self.index.nodes[scope.owner].metadata.get("multiple_module_contexts"):
                ref = self.uncertain(ref, "同一源码所属多个 crate/module 上下文", "ambiguous")
            callbacks = self.callable_arguments(call, ref.target)
            if callbacks:
                metadata["callable_arguments"] = callbacks
                metadata["callbacks_unknown"] = True
            if ref.resolution == "external" and ref.external not in _PRELUDE_CONSTRUCTORS | _PRELUDE_FUNCTIONS:
                metadata["callbacks_unknown"] = True
            if ref.external:
                metadata["external_symbol"] = ref.external
            anchor = f"{scope.file.source.path}:{scope.owner}:{node.start_byte}:{node.end_byte}"
            edge_id = "rust-call:" + hashlib.sha256(anchor.encode("utf-8")).hexdigest()[:24]
            edge = Edge(edge_id, scope.owner, ref.target if ref.resolution == "resolved" else None,
                expression, scope.file.source.path, node.start_point.row + 1, node.start_point.column,
                ref.resolution, ref.candidates, ref.reason, metadata)
            prior = output.get(edge_id)
            if prior is None:
                output[edge_id] = edge
            elif (prior.target, prior.resolution) != (edge.target, edge.resolution):
                prior.candidates = sorted(set([*prior.candidates, *edge.candidates,
                    *([prior.target] if prior.target else []), *([edge.target] if edge.target else [])]))
                prior.target = None
                prior.resolution = "ambiguous"
                prior.reason = "同一调用位置在多个模块上下文中有不同绑定"
        for node in self.index.nodes.values():
            conditional = node.metadata.get("conditional_definition")
            opaque = node.metadata.get("attribute_macros_unknown")
            unsupported_declaration = node.metadata.get("declaration_only") or node.kind in {"trait", "type", "closure"}
            if not (conditional or opaque or unsupported_declaration):
                continue
            edge_id = "rust-boundary:" + hashlib.sha256(node.id.encode("utf-8")).hexdigest()[:24]
            output[edge_id] = Edge(edge_id, node.id, None, "<declaration boundary>", node.file,
                node.line, resolution="dynamic", reason=(
                    "该声明受cfg/属性宏影响，或其trait/类型/闭包执行关系未建模；不能据空出边确认路径不存在。"
                ), metadata={"language": "rust", "declaration_boundary": True,
                    "cfg_conditions": node.metadata.get("cfg_conditions", []),
                    "derive_helper_model_id": node.metadata.get("derive_helper_model", {}).get("profile_id"),
                    "generated_members_unknown": bool(node.metadata.get("generated_members_unknown")),
                    "source_body_only": True})
        return sorted(output.values(), key=lambda item: (item.file, item.line, item.column, item.id))


def analyze_files(files: list[SourceFile], root: Path, config: dict) -> dict:
    """Analyze captured Rust text; ``root`` is identity/context, never a read path."""
    states: dict[str, _File] = {}
    diagnostics: list[Diagnostic] = []
    try:
        parser = language_parser("rust")
        parser_error = None
    except (RuntimeError, ImportError, ValueError) as error:
        parser, parser_error = None, str(error)
    for original in sorted(files, key=lambda item: item.path):
        module = "rust:" + str(PurePosixPath(original.path).with_suffix(""))
        source = replace(original, language="rust", module=module)
        raw = source.content.encode("utf-8")
        state = _File(source, raw)
        states[source.path] = state
        if source.status != "captured":
            diagnostics.append(Diagnostic("warning", source.status, source.error or "源码捕获失败，未解析。", source.path))
            continue
        if parser is None:
            source.status, source.error = "parse_error", parser_error
            diagnostics.append(Diagnostic("warning", "rust_parser_unavailable", parser_error or "Rust 语法库不可用", source.path))
            continue
        try:
            state.tree = parser.parse(raw)
            source.status = "parse_error" if state.tree.root_node.has_error else "parsed"
            source.error = "Tree-sitter 检测到错误/缺失语法节点；仅提取可识别的局部结构。" if source.status == "parse_error" else None
            if source.error:
                pending = [state.tree.root_node]
                positions = []
                while pending and len(positions) < 12:
                    node = pending.pop()
                    if node.type == "ERROR" or node.is_missing:
                        positions.append(node.start_point.row + 1)
                    pending.extend(reversed(node.named_children))
                diagnostics.append(Diagnostic("warning", "rust_parse_error", source.error, source.path,
                    min(positions) if positions else 1))
        except (ValueError, RecursionError, RuntimeError) as error:
            source.status, source.error = "parse_error", str(error)
            state.tree = None
            diagnostics.append(Diagnostic("warning", "rust_parser_failure", str(error), source.path))
    index = _Index(states, config)
    index.diagnostics.extend(diagnostics)
    try:
        index.build()
    except RecursionError:
        index.coverage_incomplete = True
        index.diagnostic("rust_ast_depth_limit", "Rust AST 遍历超过递归预算；图只保留已提取的局部结构。")
    # Even unreadable files have module nodes: absence of parser output is not
    # an empty, successfully analyzed module.
    for path, state in sorted(states.items()):
        module_id = "module:" + state.source.module
        index.nodes.setdefault(module_id, Node(module_id, state.source.module, module_id,
            state.source.module, path, 1, max(1, len(state.source.content.splitlines())), "module",
            metadata={"language": "rust", "source_status": state.source.status}))
    resolver = _Resolver(index)
    index.apply_helper_models()
    resolver.prepare_impls()
    edges = resolver.edges()
    counts = Counter(edge.resolution for edge in edges)
    callback_boundaries = sum(bool(edge.metadata.get("callbacks_unknown")) for edge in edges)
    duplicate_symbols = sum(bool(node.metadata.get("duplicate_definition")) for node in index.nodes.values())
    cfg_nodes = sum(bool(node.metadata.get("conditional_definition")) for node in index.nodes.values())
    failed = sum(state.source.status != "parsed" for state in states.values())
    call_incomplete = any(counts[x] for x in ("dynamic", "ambiguous", "unresolved")) or bool(callback_boundaries or cfg_nodes or index.macro_definitions)
    coverage_incomplete = index.coverage_incomplete or bool(failed) or not states
    index.diagnostics.sort(key=lambda item: (item.file, item.line, item.code, item.message))
    return {
        "nodes": sorted(index.nodes.values(), key=lambda item: item.id), "edges": edges,
        "files": [state.source for _, state in sorted(states.items())],
        "diagnostics": index.diagnostics,
        "stats": {"language": "rust", "analyzer_version": ANALYZER_VERSION, "parser_version": PARSER_VERSION,
            "files_total": len(states), "files_parsed": len(states) - failed, "files_failed": failed,
            "nodes": len(index.nodes), "edges": len(edges), "resolved_calls": counts["resolved"],
            "external_calls": counts["external"], "dynamic_calls": counts["dynamic"],
            "ambiguous_calls": counts["ambiguous"], "unresolved_calls": counts["unresolved"],
            "external_callback_boundaries": callback_boundaries, "ambiguous_symbols": duplicate_symbols,
            "conditional_nodes": cfg_nodes, "macro_definitions_not_expanded": index.macro_definitions,
            "helper_model_version": HELPER_MODEL_VERSION,
            "helper_models_accepted": sum(bool(node.metadata.get("derive_helper_model", {}).get("accepted"))
                for node in index.nodes.values()),
            "standard_interface_models_applied": sum(len(models) for models in index.modeled_trait_interfaces.values()),
            "generic_same_impl_model": _GENERIC_IMPL_MODEL,
            "source_context_model": SOURCE_CONTEXT_VERSION,
            "builtin_crate_attribute_model_count": sum(len(node.metadata.get("builtin_crate_attribute_models", []))
                for node in index.nodes.values() if node.kind == "module"),
            "generic_same_impl_resolved_calls": sum(edge.resolution == "resolved"
                and bool(edge.metadata.get("generic_impl_binding")) for edge in edges),
            "unmapped_crate_files": index.unmapped_files, "module_gaps": index.module_gaps,
            "coverage_incomplete": coverage_incomplete, "call_resolution_incomplete": bool(call_incomplete),
            "incomplete": coverage_incomplete or bool(call_incomplete),
            "resolution_model": "Rust source-body lexical bindings; no compiler or target execution",
            "limitations": ["未运行Cargo/rustc/测试，未验证类型、可见性或依赖可用性",
                "具体Self及同一泛型固有impl内的直接self/Self词法声明可绑定；未验证泛型实例、参数类型或bounds",
                "泛型词法模型不封闭旁支宏生成的命名空间；字段/跨impl泛型/trait目标/显式包装self保留未知",
                "不展开宏或选择cfg配置；属性宏、Deref和闭包/Future激活保留未知",
                "显式helper/标准接口模型仅在捕获名称环境与注册假设内绑定；生成体和实际标准库/toolchain未验证",
                "不推断隐式Drop/Deref/运算符分派、回调或跨语言调用",
                "模块解析仅使用配置crate根与已捕获源码；不猜测Cargo自定义target"]},
    }
