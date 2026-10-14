"""Static TS/TSX/JS calls from captured text; target programs are never loaded.

Only explicit calls with a unique lexical/ES-module binding are resolved.
Object dispatch, callbacks, JSX lifecycle, constructors, CommonJS/dynamic
loading and ambient declarations keep an observable uncertainty boundary.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field, replace
import fnmatch
import hashlib
import json
from pathlib import Path, PurePosixPath
import posixpath
from typing import Any

from .models import Diagnostic, Edge, Node, SourceFile
from .parsers import language_parser, parser_version
from .syntax_projection import PROJECTION_VERSION, parse_with_projection

ANALYZER_VERSION = "typescript-tree-sitter-call-2-projection-1"
PARSER_VERSION = parser_version("typescript") + ";" + parser_version("tsx") + ";" + PROJECTION_VERSION

_EXTENSIONS = (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".mts", ".cts")
_FUNCTIONS = {"function_declaration", "generator_function_declaration", "function_expression", "generator_function", "arrow_function"}
_TYPE_ONLY = {
    "type_annotation", "type_alias_declaration", "interface_declaration", "type_parameters",
    "type_arguments", "function_signature", "method_signature", "abstract_method_signature",
    "implements_clause", "ambient_declaration", "function_type", "constructor_type",
    "type_query", "import_type", "type_predicate", "asserts_annotation",
}
_INTRINSICS = {
    "Boolean", "String", "Number", "BigInt", "Symbol", "parseInt", "parseFloat", "isNaN",
    "isFinite", "decodeURI", "decodeURIComponent", "encodeURI", "encodeURIComponent",
    "Error", "TypeError", "RangeError", "ReferenceError", "SyntaxError", "URIError",
    "EvalError", "AggregateError", "Object", "Array", "Map", "Set", "WeakMap", "WeakSet",
    "Date", "RegExp", "Promise", "ArrayBuffer", "DataView", "Uint8Array", "Int8Array",
    "Uint16Array", "Int16Array", "Uint32Array", "Int32Array", "Float32Array", "Float64Array",
    "JSON", "Math", "Reflect", "Atomics", "Intl", "console",
}
_HOST_GLOBALS = {"fetch", "setTimeout", "clearTimeout", "setInterval", "clearInterval", "setImmediate",
                 "clearImmediate", "queueMicrotask", "URL", "URLSearchParams", "TextEncoder", "TextDecoder",
                 "AbortController", "AbortSignal", "Buffer", "process", "performance", "structuredClone"}
_INTRINSIC_OBJECTS = {"JSON", "Math", "Reflect", "Atomics", "Intl", "console"}
_UNWRAP = {"parenthesized_expression", "as_expression", "satisfies_expression", "type_assertion", "non_null_expression"}


def _hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode()).hexdigest()[:24]


def _field(node: Any, name: str) -> Any:
    return node.child_by_field_name(name) if node is not None else None


def _tokens(node: Any) -> set[str]:
    return {child.type for child in node.children if not child.is_named}


def _unwrap(node: Any) -> Any:
    while node is not None and node.type in _UNWRAP:
        expression = _field(node, "expression")
        if expression is None:
            children = [child for child in node.named_children if child.type not in {"type_annotation", "type_arguments"} and not child.type.endswith("_type")]
            expression = (children[-1] if node.type == "type_assertion" else children[0]) if children else None
        if expression is None:
            break
        node = expression
    return node


@dataclass
class _Module:
    file: SourceFile
    data: bytes
    tree: Any = None
    scope: _Scope | None = None
    exports: dict[str, list[_Export]] = field(default_factory=dict)
    stars: list[str] = field(default_factory=list)
    commonjs: bool = False
    projection: dict[str, Any] = field(default_factory=dict)

    @property
    def name(self) -> str:
        return self.file.module

    def text(self, node: Any, limit: int = 600) -> str:
        return self.data[node.start_byte:node.end_byte].decode("utf-8", "replace")[:limit] if node is not None else ""


@dataclass
class _Binding:
    kind: str
    position: int = 0
    target: str = ""
    expression: Any = None
    specifier: str = ""
    member: str = ""
    hoisted: bool = False
    conditional: bool = False
    reason: str = ""
    origin: _Scope | None = None


@dataclass
class _Scope:
    kind: str
    module: _Module
    owner: str
    qualname: str
    parent: _Scope | None = None
    bindings: dict[str, list[_Binding]] = field(default_factory=dict)
    types: set[str] = field(default_factory=set)
    class_id: str = ""


@dataclass
class _Export:
    kind: str
    name: str = ""
    specifier: str = ""
    member: str = ""
    expression: Any = None
    scope: _Scope | None = None


@dataclass
class _Ref:
    resolution: str
    kind: str = "unknown"
    target: str | None = None
    module: _Module | None = None
    candidates: list[str] = field(default_factory=list)
    reason: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class _Site:
    node: Any
    function: Any
    scope: _Scope
    kind: str = "call"


class _Index:
    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.nodes: dict[str, Node] = {}
        self.modules: dict[str, list[_Module]] = {}
        self.scopes: dict[int, _Scope] = {}
        self.function_nodes: dict[int, str] = {}
        self.sites: list[_Site] = []
        self.writes: list[tuple[str, Any, _Scope]] = []
        self.attribute_writes: list[tuple[str, _Scope, Any]] = []
        self.global_writes: set[str] = set()
        self.symbol_origins: dict[str, list[tuple[_Scope, str]]] = {}
        self.source_unknowns: dict[str, _Ref] = {}
        self.object_members: dict[str, dict[str, list[str]]] = {}
        self.signatures: list[tuple[Any, _Scope, bool]] = []
        self.diagnostics: list[Diagnostic] = []
        self.coverage_incomplete = False

    def add(self, node: Node) -> None:
        sources = self.modules.get(node.file, [])
        if any(source.projection.get("mode") == "adapted" for source in sources):
            node.metadata["source_parse_mode"] = "adapted"
            node.metadata["syntax_projection_version"] = PROJECTION_VERSION
            node.metadata["source_projection_node"] = "module:" + node.module
        module_node = self.nodes.get("module:" + node.module)
        if node.kind != "module" and module_node is not None and module_node.metadata.get("duplicate_definition"):
            node.metadata["module_identity_collision"] = True
        old = self.nodes.get(node.id)
        if old is None:
            self.nodes[node.id] = node
            return
        old.metadata.setdefault("definitions", [{"file": old.file, "line": old.line, "end_line": old.end_line,
                                                   "kind": old.kind, "signature": old.signature}]).append(
            {"file": node.file, "line": node.line, "end_line": node.end_line, "kind": node.kind, "signature": node.signature})
        old.metadata["duplicate_definition"] = True
        self.diagnostics.append(Diagnostic("warning", "ts_duplicate_definition", f"同一词法符号 {node.id} 有多个定义，保留歧义。", node.file, node.line))

    def identifier(self, module: _Module, qualified: str) -> str:
        return module.name + "#" + qualified


def _bound_names(node: Any) -> list[str]:
    if node is None:
        return []
    if node.type in {"identifier", "shorthand_property_identifier_pattern"}:
        return [node.text.decode("utf-8", "replace")]
    if node.type in {"pair_pattern", "pair"}:
        return _bound_names(_field(node, "value"))
    if node.type in {"assignment_pattern", "object_assignment_pattern"}:
        return _bound_names(_field(node, "left") or next(iter(node.named_children), None))
    if node.type in {"required_parameter", "optional_parameter"}:
        return _bound_names(_field(node, "pattern") or _field(node, "name"))
    if node.type in {"object_pattern", "array_pattern", "rest_pattern", "formal_parameters"}:
        return [name for child in node.named_children for name in _bound_names(child)]
    return []


class _Collector:
    def __init__(self, index: _Index, module: _Module):
        self.index = index
        self.module = module
        assert module.scope is not None
        self.scope = module.scope
        self.conditional = 0

    def _qualify(self, name: str) -> str:
        return self.scope.qualname + "." + name if self.scope.qualname else name

    def _bind(self, name: str, binding: _Binding, *, var: bool = False) -> None:
        origin = self.scope
        destination = origin
        if var:
            while destination.kind not in {"function", "module"} and destination.parent is not None:
                destination = destination.parent
        binding.origin = binding.origin or origin
        binding.conditional = binding.conditional or self.conditional > 0
        destination.bindings.setdefault(name, []).append(binding)
        if binding.target and binding.kind in {"callable", "class"}:
            self.index.symbol_origins.setdefault(binding.target, []).append((destination, name))

    def _export(self, name: str, export: _Export) -> None:
        if self.scope.kind != "module":
            return  # namespace exports do not become file-level ES exports
        self.module.exports.setdefault(name, []).append(export)

    def _declaration_names(self, declaration: Any) -> list[str]:
        if declaration is None:
            return []
        if declaration.type in {"lexical_declaration", "variable_declaration"}:
            return [name for child in declaration.named_children if child.type == "variable_declarator"
                    for name in _bound_names(_field(child, "name"))]
        name = _field(declaration, "name")
        return [self.module.text(name)] if name is not None else []

    def visit(self, node: Any, *, body: bool = False) -> None:
        if node is None:
            return
        self.index.scopes[node.id] = self.scope
        kind = node.type
        if kind in _TYPE_ONLY or kind.endswith("_type"):
            name = _field(node, "name")
            if name is not None:
                self.scope.types.add(self.module.text(name))
            if kind == "function_signature":
                self.index.signatures.append((node, self.scope, False))
            elif kind == "ambient_declaration":
                for child in node.named_children:
                    if child.type == "function_signature":
                        self.index.signatures.append((child, self.scope, True))
                        name = _field(child, "name")
                        if name is not None:
                            self._bind(self.module.text(name), _Binding("unknown", child.start_byte, hoisted=True,
                                reason="ambient 函数只声明运行时名称，没有捕获实现"))
                    elif child.type in {"lexical_declaration", "variable_declaration", "class_declaration", "enum_declaration", "internal_module"}:
                        for name in self._declaration_names(child):
                            self._bind(name, _Binding("unknown", child.start_byte, hoisted=True,
                                reason="ambient 值只声明运行时名称，没有捕获实现"))
                    name = _field(child, "name")
                    if name is not None:
                        self.scope.types.add(self.module.text(name))
            return
        if kind == "import_statement":
            self._import(node)
            return
        if kind == "export_statement":
            self._export_statement(node)
            return
        if kind in _FUNCTIONS:
            self._function(node)
            return
        if kind in {"class_declaration", "class", "class_expression"}:
            self._class(node)
            return
        if kind == "method_definition":
            self._function(node, method=True)
            return
        if kind == "variable_declarator":
            self._variable(node)
            return
        if kind == "enum_declaration":
            name = _field(node, "name")
            if name is not None:
                self._bind(self.module.text(name), _Binding("unknown", node.end_byte, reason="enum 运行时对象属性未推断"))
            for child in node.named_children:
                self.visit(child)
            return
        if kind in {"assignment_expression", "augmented_assignment_expression"}:
            left, right = _field(node, "left"), _field(node, "right")
            if left is not None:
                for name in _bound_names(_unwrap(left)):
                    self.index.writes.append((name, node, self.scope))
                if left.type in {"member_expression", "subscript_expression"}:
                    prop = _field(left, "property") or _field(left, "index")
                    name = self.module.text(prop) if prop is not None and prop.type in {"property_identifier", "identifier"} else "*"
                    self.index.attribute_writes.append((name, self.scope, left))
                    if self.module.text(_field(left, "object")) in {"module", "exports"}:
                        self.module.commonjs = True
            self.visit(left)
            self.visit(right)
            return
        if kind == "update_expression":
            argument = _field(node, "argument") or next(iter(node.named_children), None)
            if argument is not None and argument.type == "identifier":
                self.index.writes.append((self.module.text(argument), node, self.scope))
            elif argument is not None and argument.type in {"member_expression", "subscript_expression"}:
                self.index.attribute_writes.append(("*", self.scope, argument))
        if kind == "call_expression":
            self.index.sites.append(_Site(node, _field(node, "function"), self.scope))
        elif kind == "new_expression":
            self.index.sites.append(_Site(node, _field(node, "constructor"), self.scope, "new"))
        elif kind.startswith("jsx_") and kind in {"jsx_element", "jsx_self_closing_element", "jsx_fragment"}:
            opening = _field(node, "open_tag") or next((child for child in node.named_children if child.type == "jsx_opening_element"), node)
            self.index.sites.append(_Site(node, _field(opening, "name"), self.scope, "jsx"))
        if kind == "statement_block" and not body:
            previous = self.scope
            label = f"<block@{node.start_point.row + 1}:{node.start_point.column}>"
            self.scope = _Scope("block", self.module, previous.owner, self._qualify(label), previous, class_id=previous.class_id)
            for child in node.named_children:
                self.visit(child)
            self.scope = previous
            return
        if kind == "catch_clause":
            previous = self.scope
            label = f"<catch@{node.start_point.row + 1}:{node.start_point.column}>"
            self.scope = _Scope("block", self.module, previous.owner, self._qualify(label), previous, class_id=previous.class_id)
            parameter = _field(node, "parameter")
            for name in _bound_names(parameter):
                self._bind(name, _Binding("unknown", node.start_byte, reason="catch 参数的运行时值未知"))
            for child in node.named_children:
                self.visit(child, body=child == _field(node, "body"))
            self.scope = previous
            return
        if kind in {"for_statement", "for_in_statement"}:
            previous = self.scope
            label = f"<loop@{node.start_point.row + 1}:{node.start_point.column}>"
            self.scope = _Scope("block", self.module, previous.owner, self._qualify(label), previous, class_id=previous.class_id)
            left = _field(node, "left")
            if left is not None:
                declaration_tokens = _tokens(node) & {"var", "let", "const"}
                for name in _bound_names(left):
                    if declaration_tokens:
                        self._bind(name, _Binding("unknown", node.start_byte, reason="循环变量运行时类型未知"), var="var" in declaration_tokens)
                    else:
                        self.index.writes.append((name, node, self.scope))
            self.conditional += 1
            for child in node.named_children:
                self.visit(child)
            self.conditional -= 1
            self.scope = previous
            return
        if kind == "object":
            self._object(node)
            return
        if kind in {"internal_module", "module"}:
            self._namespace(node)
            return
        conditional = kind in {"if_statement", "while_statement", "do_statement", "switch_case", "switch_default"}
        if conditional:
            self.conditional += 1
        for child in node.named_children:
            self.visit(child)
        if conditional:
            self.conditional -= 1

    def _import(self, node: Any) -> None:
        specifier = _string(_field(node, "source"), self.module)
        clause = next((child for child in node.named_children if child.type == "import_clause"), None)
        type_only = "type" in _tokens(node)
        if clause is None:
            return  # side-effect imports do not invent a function CALLS edge
        for child in clause.named_children:
            if child.type == "identifier":
                name = self.module.text(child)
                if type_only:
                    self.scope.types.add(name)
                else:
                    self._bind(name, _Binding("import_member", node.start_byte, specifier=specifier, member="default", hoisted=True))
            elif child.type == "namespace_import":
                identifier = next((item for item in child.named_children if item.type == "identifier"), None)
                name = self.module.text(identifier)
                if type_only:
                    self.scope.types.add(name)
                elif name:
                    self._bind(name, _Binding("import_namespace", node.start_byte, specifier=specifier, hoisted=True))
            elif child.type == "named_imports":
                for item in child.named_children:
                    imported = _field(item, "name")
                    local = _field(item, "alias") or imported
                    name = self.module.text(local)
                    if type_only or "type" in _tokens(item):
                        self.scope.types.add(name)
                    elif name:
                        self._bind(name, _Binding("import_member", node.start_byte, specifier=specifier,
                            member=self.module.text(imported), hoisted=True))
        if not specifier:
            self.index.diagnostics.append(Diagnostic("warning", "ts_import_source", "导入源字符串未能静态读取。", self.module.file.path, node.start_point.row + 1))

    def _export_statement(self, node: Any) -> None:
        tokens = _tokens(node)
        declaration = _field(node, "declaration")
        value = _field(node, "value")
        specifier = _string(_field(node, "source"), self.module)
        default = "default" in tokens
        type_only = "type" in tokens
        if declaration is not None:
            self.visit(declaration)
            names = self._declaration_names(declaration)
            if default:
                if names:
                    self._export("default", _Export("local", names[0], scope=self.scope))
                else:
                    self._export("default", _Export("expression", expression=declaration, scope=self.scope))
            elif not type_only:
                for name in names:
                    self._export(name, _Export("local", name, scope=self.scope))
            return
        if default and value is not None:
            expression = _unwrap(value)
            if expression is not None and expression.type in _FUNCTIONS:
                self._function(expression, assigned="<default>")
            elif expression is not None and expression.type in {"class", "class_expression"}:
                self._class(expression, assigned="<default>")
            else:
                self.visit(value)
            self._export("default", _Export("expression", expression=value, scope=self.scope))
            return
        clause = next((child for child in node.named_children if child.type == "export_clause"), None)
        namespace = next((child for child in node.named_children if child.type == "namespace_export"), None)
        if namespace is not None and specifier:
            name = self.module.text(next(iter(namespace.named_children), None))
            if name and not type_only:
                self._export(name, _Export("namespace", specifier=specifier, scope=self.scope))
        elif clause is not None:
            for item in clause.named_children:
                if type_only or "type" in _tokens(item):
                    continue
                local = self.module.text(_field(item, "name"))
                exported = self.module.text(_field(item, "alias")) or local
                if exported:
                    self._export(exported, _Export("reexport" if specifier else "local", local,
                        specifier, local, scope=self.scope))
        elif specifier and "*" in tokens and not type_only and self.scope.kind == "module":
            self.module.stars.append(specifier)
        else:
            for child in node.named_children:
                self.visit(child)

    def _function(self, node: Any, assigned: str = "", method: bool = False) -> str:
        parent = self.scope
        declared = self.module.text(_field(node, "name"))
        generated = f"<arrow@{node.start_point.row + 1}:{node.start_point.column}>" if node.type == "arrow_function" else f"<function@{node.start_point.row + 1}:{node.start_point.column}>"
        name = assigned or declared or generated
        if method and _field(node, "name") is not None and _field(node, "name").type == "computed_property_name":
            self.visit(_field(node, "name"))
            name = f"<computed-method@{node.start_point.row + 1}:{node.start_point.column}>"
        qualified = self._qualify(name)
        node_id = self.index.identifier(self.module, qualified)
        parameters = _field(node, "parameters") or _field(node, "parameter")
        body = _field(node, "body")
        metadata = {"language": "typescript", "syntax_kind": node.type, "async": "async" in _tokens(node),
                    "static": "static" in _tokens(node), "lexical_scope": parent.qualname,
                    "dispatch": "object_method" if method else "lexical", "declaration_only": body is None}
        self.index.add(Node(node_id, name, node_id, self.module.name, self.module.file.path,
            node.start_point.row + 1, node.end_point.row + 1, "method" if method else "function",
            (name + self.module.text(parameters) + self.module.text(_field(node, "return_type")))[:800], metadata=metadata))
        self.index.function_nodes[node.id] = node_id
        declaration = node.type in {"function_declaration", "generator_function_declaration"}
        if declaration and declared:
            self._bind(declared, _Binding("callable", node.start_byte, target=node_id, hoisted=True))
        if method and parent.kind == "class":
            self.index.object_members.setdefault(parent.owner, {}).setdefault(declared or name, []).append(node_id)
        function_scope = _Scope("function", self.module, node_id, qualified, parent, class_id=parent.class_id)
        if not declaration and declared and not method:
            function_scope.bindings[declared] = [_Binding("callable", node.start_byte, target=node_id, hoisted=True, origin=function_scope)]
        for parameter in _bound_names(parameters):
            function_scope.bindings[parameter] = [_Binding("unknown", node.start_byte, reason="参数/闭包回调运行时绑定未知", origin=function_scope)]
        self.scope = function_scope
        old_conditional, self.conditional = self.conditional, 0
        self.visit(parameters)
        self.visit(body, body=True)
        self.conditional = old_conditional
        self.scope = parent
        return node_id

    def _variable(self, node: Any) -> None:
        name_node, value = _field(node, "name"), _field(node, "value")
        names = _bound_names(name_node)
        direct = name_node is not None and name_node.type == "identifier"
        expression = _unwrap(value)
        parent_type = node.parent.type if node.parent is not None else ""
        var = parent_type == "variable_declaration"
        if direct and expression is not None and expression.type in _FUNCTIONS:
            target = self._function(expression, assigned=names[0])
            self._bind(names[0], _Binding("callable", node.end_byte, target=target), var=var)
        elif direct and expression is not None and expression.type in {"class", "class_expression"}:
            target = self._class(expression, assigned=names[0])
            self._bind(names[0], _Binding("class", node.end_byte, target=target), var=var)
        else:
            if direct and expression is not None and expression.type == "object":
                self._object(expression, assigned=names[0])
            else:
                self.visit(value)
            for name in names:
                self._bind(name, _Binding("alias" if direct and value is not None else "unknown", node.end_byte,
                    expression=value if direct else None, reason="解构/未初始化变量值未推断"), var=var)
        # Defaults/computed keys in destructuring are executable expressions.
        self.visit(name_node)

    def _class(self, node: Any, assigned: str = "") -> str:
        parent = self.scope
        declared = self.module.text(_field(node, "name"))
        name = assigned or declared or f"<class@{node.start_point.row + 1}:{node.start_point.column}>"
        qualified = self._qualify(name)
        node_id = self.index.identifier(self.module, qualified)
        self.index.add(Node(node_id, name, node_id, self.module.name, self.module.file.path,
            node.start_point.row + 1, node.end_point.row + 1, "class",
            metadata={"language": "typescript", "constructor_dispatch_expanded": False}))
        self.index.function_nodes[node.id] = node_id
        if node.type == "class_declaration" and declared:
            self._bind(declared, _Binding("class", node.end_byte, target=node_id))
        body = _field(node, "body")
        for child in node.named_children:
            if child != body and child != _field(node, "name"):
                self.visit(child)
        class_scope = _Scope("class", self.module, node_id, qualified, parent, class_id=node_id)
        if declared:
            class_scope.bindings[declared] = [_Binding("class", node.start_byte, target=node_id, hoisted=True, origin=class_scope)]
        self.scope = class_scope
        if body is not None:
            for child in body.named_children:
                if child.type == "method_definition":
                    self._function(child, method=True)
                elif child.type in {"public_field_definition", "field_definition"}:
                    value = _field(child, "value")
                    name_node = _field(child, "name")
                    field_name = self.module.text(name_node) or f"<field@{child.start_point.row + 1}>"
                    if name_node is not None and name_node.type == "computed_property_name":
                        self.scope = parent
                        self.visit(name_node)
                        self.scope = class_scope
                    expression = _unwrap(value)
                    if expression is not None and expression.type in _FUNCTIONS:
                        target = self._function(expression, assigned=field_name, method=True)
                        self.index.object_members.setdefault(node_id, {}).setdefault(field_name, []).append(target)
                    elif "static" in _tokens(child):
                        self.scope = parent
                        self.visit(value)
                        self.scope = class_scope
                    elif value is not None:
                        initializer_id = self.index.identifier(self.module, qualified + ".<field:" + field_name + ">")
                        self.index.add(Node(initializer_id, field_name, initializer_id, self.module.name,
                            self.module.file.path, child.start_point.row + 1, child.end_point.row + 1, "function",
                            metadata={"language": "typescript", "implicit": "instance_field_initializer"}))
                        self.scope = _Scope("function", self.module, initializer_id, qualified + ".<field:" + field_name + ">", class_scope, class_id=node_id)
                        self.visit(value)
                        self.scope = class_scope
                elif child.type == "class_static_block":
                    self.scope = parent
                    self.visit(child)
                    self.scope = class_scope
                else:
                    self.visit(child)
        self.scope = parent
        return node_id

    def _object(self, node: Any, assigned: str = "") -> None:
        parent = self.scope
        label = assigned or f"<object@{node.start_point.row + 1}:{node.start_point.column}>"
        qualified = self._qualify(label)
        object_key = self.index.identifier(self.module, qualified)
        self.index.function_nodes[node.id] = object_key
        self.scope = _Scope("object", self.module, parent.owner, qualified, parent, class_id=parent.class_id)
        for child in node.named_children:
            if child.type == "method_definition":
                target = self._function(child, method=True)
                self.index.object_members.setdefault(object_key, {}).setdefault(self.module.text(_field(child, "name")), []).append(target)
            elif child.type == "pair":
                key, value = _field(child, "key"), _field(child, "value")
                expression = _unwrap(value)
                if expression is not None and expression.type in _FUNCTIONS:
                    name = self.module.text(key) or f"<property@{child.start_point.row + 1}>"
                    target = self._function(expression, assigned=name, method=True)
                    self.index.object_members.setdefault(object_key, {}).setdefault(name, []).append(target)
                else:
                    self.visit(child)
            else:
                self.visit(child)
        self.scope = parent

    def _namespace(self, node: Any) -> None:
        name_node, body = _field(node, "name"), _field(node, "body")
        name = self.module.text(name_node)
        if not name or body is None:
            return
        parent = self.scope
        qualified = self._qualify(name)
        key = self.index.identifier(self.module, qualified)
        self.index.add(Node(key, name, key, self.module.name, self.module.file.path,
            node.start_point.row + 1, node.end_point.row + 1, "namespace", metadata={"language": "typescript", "dispatch_expanded": False}))
        self._bind(name, _Binding("object", node.start_byte, target=key))
        self.scope = _Scope("namespace", self.module, parent.owner, qualified, parent, class_id=parent.class_id)
        self.visit(body, body=True)
        self.scope = parent


def _string(node: Any, module: _Module) -> str:
    if node is None or node.type not in {"string", "string_fragment"}:
        return ""
    raw = module.text(node, 4096)
    if node.type == "string_fragment":
        return raw
    if len(raw) < 2:
        return ""
    # Normal relative/package specifiers have no escapes. Escaped module names
    # keep an unknown boundary rather than running a JS evaluator.
    return raw[1:-1] if raw[0] in {"'", '"'} and raw[-1] == raw[0] and "\\" not in raw[1:-1] else ""


class _Resolver:
    def __init__(self, index: _Index):
        self.index = index
        self.attribute_names = {name for name, _, _ in index.attribute_writes}

    @staticmethod
    def unknown(reason: str, resolution: str = "dynamic", candidates: list[str] | None = None) -> _Ref:
        return _Ref(resolution, candidates=sorted(set(candidates or [])), reason=reason)

    def combine(self, refs: list[_Ref], reason: str, *, force: bool = False) -> _Ref:
        if len(refs) == 1 and not force:
            return refs[0]
        identities = {(ref.resolution, ref.kind, ref.target, ref.module.file.path if ref.module else "", ref.metadata.get("external_symbol", "")) for ref in refs}
        if refs and len(identities) == 1 and not force and all(ref.resolution in {"resolved", "external"} for ref in refs):
            return refs[0]
        candidates = [candidate for ref in refs for candidate in [*ref.candidates, *([ref.target] if ref.target else [])]]
        return self.unknown(reason, "ambiguous" if len(set(candidates)) > 1 or (force and candidates) else "dynamic", candidates)

    def _symbol(self, target: str) -> _Ref:
        node = self.index.nodes.get(target)
        if node is None:
            return self.unknown("没有对应的实现声明", "unresolved")
        if node.metadata.get("duplicate_definition"):
            return self.unknown("重复定义不能选择唯一实现", "ambiguous", [target])
        if node.metadata.get("module_identity_collision"):
            return self.unknown("不同源码文件共享模块身份，不能确认唯一实现", "ambiguous", [target])
        if node.metadata.get("declaration_only"):
            return self.unknown("声明没有运行时实现体", "unresolved", [target])
        return _Ref("resolved", "class" if node.kind == "class" else "callable", target,
                    reason="唯一词法实现声明", metadata={"binding_model": "lexical_declaration"})

    def module(self, specifier: str, origin: _Module) -> _Ref:
        if not specifier:
            return self.unknown("模块源字符串无法静态读取")
        candidate_base: str | None = None
        if specifier.startswith("."):
            candidate_base = posixpath.normpath(posixpath.join(posixpath.dirname(origin.file.path), specifier))
        else:
            aliases = self.index.config.get("analysis", {}).get("module_aliases", {})
            matches: list[tuple[int, str]] = []
            for alias, destination in aliases.items():
                if not isinstance(alias, str) or not isinstance(destination, str):
                    continue
                if "*" in alias and alias.count("*") == 1:
                    before, after = alias.split("*")
                    if specifier.startswith(before) and specifier.endswith(after):
                        middle = specifier[len(before):len(specifier) - len(after) if after else None]
                        matches.append((len(alias), destination.replace("*", middle)))
                elif specifier == alias:
                    matches.append((len(alias), destination))
                elif specifier.startswith(alias + "/") and PurePosixPath(destination).suffix not in _EXTENSIONS:
                    matches.append((len(alias), destination.rstrip("/") + specifier[len(alias):]))
            if matches:
                best = max(score for score, _ in matches)
                destinations = sorted({value for score, value in matches if score == best})
                if len(destinations) != 1:
                    return self.unknown("模块别名匹配多个目标", "ambiguous")
                candidate_base = posixpath.normpath(destinations[0])
        if candidate_base is None:
            if specifier.startswith("/") or ":\\" in specifier:
                return self.unknown("绝对文件导入不在捕获项目范围内", "unresolved")
            return _Ref("external", "namespace", reason="外部模块声明；不验证安装与 API 实现",
                metadata={"external_symbol": specifier, "external_kind": "node_builtin" if specifier.startswith("node:") else "declared_external",
                          "availability_verified": False, "callbacks_unknown": True})
        if candidate_base == ".." or candidate_base.startswith("../") or candidate_base.startswith("/"):
            return self.unknown("模块路径逃逸项目捕获范围", "unresolved")
        suffix = PurePosixPath(candidate_base).suffix
        paths = [candidate_base]
        if suffix == ".js":
            paths += [candidate_base[:-3] + ext for ext in (".ts", ".tsx", ".jsx")]
        elif suffix == ".mjs":
            paths += [candidate_base[:-4] + ".mts"]
        elif suffix == ".cjs":
            paths += [candidate_base[:-4] + ".cts"]
        elif not suffix:
            paths += [candidate_base + ext for ext in _EXTENSIONS]
            paths += [candidate_base + "/index" + ext for ext in _EXTENSIONS]
        elif suffix not in _EXTENSIONS:
            return self.unknown("资源/原生模块导入不属于本次调用实现分析")
        modules = [module for path in sorted(set(paths)) for module in self.index.modules.get(path, [])]
        if len(modules) > 1:
            return self.unknown("源码入口有多个候选；未假定编译器/加载器优先级", "ambiguous", ["module:" + module.name for module in modules])
        if not modules:
            return self.unknown("项目内导入没有捕获到对应源码入口（缺失或范围未覆盖）", "unresolved")
        module = modules[0]
        if module.file.status != "parsed":
            return self.unknown(f"导入源码未成功解析 ({module.file.status})", "unresolved", ["module:" + module.name])
        return _Ref("resolved", "namespace", module=module, reason="捕获源码中的静态 ES 模块入口",
                    metadata={"import_specifier": specifier, "imported_file": module.file.path})

    def exported(self, module_ref: _Ref, name: str, seen: set[tuple[str, str]]) -> _Ref:
        if module_ref.resolution == "external":
            metadata = {**module_ref.metadata, "external_symbol": str(module_ref.metadata.get("external_symbol", "")) + "." + name}
            return _Ref("external", "callable", reason="外部导出声明；未扫描外部实现", metadata=metadata)
        if module_ref.resolution != "resolved" or module_ref.module is None:
            return module_ref
        module = module_ref.module
        key = (module.file.path, "export:" + name)
        if key in seen or len(seen) > 150:
            return self.unknown("重导出存在循环或解析预算耗尽")
        seen = seen | {key}
        exports = module.exports.get(name, [])
        if exports:
            refs: list[_Ref] = []
            for export in exports:
                if export.kind == "local":
                    assert export.scope is not None
                    refs.append(self.name(export.name, export.scope, seen))
                elif export.kind == "expression":
                    assert export.scope is not None
                    refs.append(self.expression(export.expression, export.scope, seen))
                elif export.kind == "namespace":
                    refs.append(self.module(export.specifier, module))
                elif export.kind == "reexport":
                    refs.append(self.exported(self.module(export.specifier, module), export.member, seen))
            result = self.combine(refs, "导出名对应多个定义", force=len(exports) > 1)
            result.metadata = {**result.metadata, "exported_name": name, "exported_file": module.file.path}
            return result
        if name != "default" and module.stars:
            refs = [self.exported(self.module(specifier, module), name, seen) for specifier in module.stars]
            present = [ref for ref in refs if not (ref.resolution == "unresolved" and ref.metadata.get("export_missing"))]
            if present:
                return self.combine(present, "多个 export* 来源存在歧义或未知")
        if module.commonjs:
            return self.unknown("CommonJS 导出/ES互操作未静态展开")
        result = self.unknown(f"捕获模块没有运行时导出 {name}", "unresolved")
        result.metadata["export_missing"] = True
        return result

    def binding(self, binding: _Binding, scope: _Scope, seen: set[tuple[str, str]]) -> _Ref:
        origin = binding.origin or scope
        if binding.kind in {"callable", "class"}:
            return self._symbol(binding.target)
        if binding.kind == "object":
            return _Ref("resolved", "object", target=binding.target, reason="词法对象声明；属性分派保持未知")
        if binding.kind == "import_namespace":
            return self.module(binding.specifier, origin.module)
        if binding.kind == "import_member":
            return self.exported(self.module(binding.specifier, origin.module), binding.member, seen)
        if binding.kind == "alias" and binding.expression is not None:
            result = self.expression(binding.expression, origin, seen)
            result.metadata = {**result.metadata, "alias_model": "unique_lexical_binding"}
            return result
        return self.unknown(binding.reason or "运行时值未推断")

    def scope_binding(self, scope: _Scope, name: str, seen: set[tuple[str, str]]) -> _Ref | None:
        bindings = scope.bindings.get(name, [])
        if not bindings:
            return None
        key = (scope.module.file.path, f"scope:{id(scope)}:{name}")
        if key in seen or len(seen) > 150:
            return self.unknown("词法别名解析循环或预算耗尽")
        refs = [self.binding(binding, scope, seen | {key}) for binding in bindings]
        return self.combine(refs, "名称有重复声明、重赋值或条件初始化",
                            force=len(bindings) > 1 or any(binding.conditional for binding in bindings))

    def name(self, name: str, scope: _Scope, seen: set[tuple[str, str]], position: int | None = None) -> _Ref:
        cursor: _Scope | None = scope
        types_seen = False
        while cursor is not None:
            if cursor.kind not in {"class", "object"}:
                ref = self.scope_binding(cursor, name, seen)
                if ref is not None:
                    bindings = cursor.bindings[name]
                    if position is not None and cursor.owner == scope.owner and all(not item.hoisted and item.position > position for item in bindings):
                        return self.unknown("词法变量/类在当前执行作用域中尚未初始化（TDZ/顺序未知）", "unresolved", ref.candidates or ([ref.target] if ref.target else []))
                    return ref
                types_seen = types_seen or name in cursor.types
            cursor = cursor.parent
        if name in self.index.global_writes:
            return self.unknown("项目中对未绑定全局名称有写入，不能假定默认全局值")
        if name in {"require", "eval", "Function"}:
            return self.unknown("动态模块加载/代码生成边界不展开")
        if name in _INTRINSICS or name in _HOST_GLOBALS:
            return _Ref("external", "namespace" if name in _INTRINSIC_OBJECTS else "callable",
                reason="JS内建/宿主全局声明；未验证目标运行环境",
                metadata={"external_symbol": name, "external_kind": "js_builtin" if name in _INTRINSICS else "host_global",
                          "availability_verified": False, "callbacks_unknown": name in _HOST_GLOBALS})
        return self.unknown("只有类型声明，无法建立运行时调用实现" if types_seen else f"名称 {name} 没有可解析的值声明", "unresolved")

    def member(self, base: _Ref, name: str, seen: set[tuple[str, str]]) -> _Ref:
        if base.resolution == "external":
            metadata = {**base.metadata, "external_symbol": str(base.metadata.get("external_symbol", "")) + "." + name,
                        "availability_verified": False, "callbacks_unknown": True}
            return _Ref("external", "callable", reason="外部/宿主对象属性，实现未捕获", metadata=metadata)
        if base.resolution == "resolved" and base.kind == "namespace" and base.module is not None:
            if name in self.attribute_names or "*" in self.attribute_names:
                return self.unknown("项目中存在同名属性写入，不能确认模块属性未覆盖")
            return self.exported(base, name, seen)
        candidates: list[str] = []
        if base.target:
            candidates += self.index.object_members.get(base.target, {}).get(name, [])
        return self.unknown("对象/this/类方法分派不推断为确定调用", candidates=candidates or base.candidates)

    def expression(self, node: Any, scope: _Scope, seen: set[tuple[str, str]] | None = None) -> _Ref:
        seen = seen or set()
        node = _unwrap(node)
        if node is None:
            return self.unknown("调用目标语法无法提取")
        if node.type in {"identifier", "type_identifier", "shorthand_property_identifier"}:
            return self.name(scope.module.text(node), scope, seen, node.start_byte)
        if node.type in _FUNCTIONS:
            target = self.index.function_nodes.get(node.id)
            return self._symbol(target) if target else self.unknown("函数表达式未提取")
        if node.type in {"class", "class_expression"}:
            target = self.index.function_nodes.get(node.id)
            return self._symbol(target) if target else self.unknown("类表达式未提取")
        if node.type == "member_expression":
            prop = _field(node, "property")
            return self.member(self.expression(_field(node, "object"), scope, seen), scope.module.text(prop), seen)
        if node.type == "subscript_expression":
            index = _field(node, "index")
            if index is not None and index.type == "string":
                return self.member(self.expression(_field(node, "object"), scope, seen), _string(index, scope.module), seen)
            return self.unknown("计算属性/数组下标分派未推断")
        if node.type == "this":
            return _Ref("resolved", "object", target=scope.class_id or None, reason="this 仅保留词法类候选，不推断实例类型")
        if node.type == "object":
            return _Ref("resolved", "object", target=self.index.function_nodes.get(node.id), reason="对象字面量；属性可变，保留未知")
        if node.type == "ternary_expression":
            return self.combine([self.expression(_field(node, name), scope, seen) for name in ("consequence", "alternative")],
                                "条件表达式有多个潜在目标", force=True)
        if node.type in {"number", "string", "true", "false", "null", "undefined", "array", "regex"}:
            return _Ref("resolved", "value", reason="值表达式未解析为可调用实现")
        if node.type in {"call_expression", "new_expression", "await_expression"}:
            return self.unknown("工厂/构造/异步返回值未做运行时类型推断")
        if node.type == "import":
            return self.unknown("动态 import 的加载与返回命名空间未展开")
        return self.unknown(f"{node.type} 动态调用目标未推断")

    def prepare(self) -> None:
        # JS assignment writes affect the nearest existing lexical binding, even
        # when the write occurs in a nested closure before collection sees it.
        for name, node, origin in self.index.writes:
            scope: _Scope | None = origin
            while scope is not None:
                if scope.kind not in {"class", "object"} and name in scope.bindings:
                    scope.bindings[name].append(_Binding("unknown", node.start_byte,
                        reason="该词法名称在项目中被重赋值/更新", origin=origin))
                    break
                scope = scope.parent
            else:
                self.index.global_writes.add(name)
        for node, scope, ambient in self.index.signatures:
            name = scope.module.text(_field(node, "name"))
            if not name:
                continue
            implementation = scope.bindings.get(name, [])
            if implementation and not ambient:
                for binding in implementation:
                    if binding.target in self.index.nodes:
                        self.index.nodes[binding.target].metadata.setdefault("overload_signatures", []).append(
                            {"line": node.start_point.row + 1, "signature": scope.module.text(node)})
                continue
            target = self.index.identifier(scope.module, scope.qualname + "." + name if scope.qualname else name)
            self.index.add(Node(target, name, target, scope.module.name, scope.module.file.path,
                node.start_point.row + 1, node.end_point.row + 1, "declaration", scope.module.text(node),
                metadata={"language": "typescript", "declaration_only": True, "ambient": ambient}))
            scope.types.add(name)
            if not implementation:
                scope.bindings[name] = [_Binding("callable", node.start_byte, target=target, hoisted=True, origin=scope)]
        for node_id, origins in self.index.symbol_origins.items():
            refs = [self.scope_binding(scope, name, set()) for scope, name in origins]
            refs = [ref for ref in refs if ref is not None]
            if refs and any(ref.resolution != "resolved" or ref.target != node_id for ref in refs):
                self.index.source_unknowns[node_id] = self.combine(refs, "源符号的最终词法绑定有重赋值/歧义", force=True)
                self.index.nodes[node_id].metadata["binding_uncertain"] = True

    def _callbacks(self, site: _Site) -> list[str]:
        arguments = _field(site.node, "arguments")
        if arguments is None:
            return []
        candidates: set[str] = set()
        pending = list(arguments.named_children)
        while pending:
            argument = pending.pop()
            if argument.type in {"array", "object", "pair", "spread_element"}:
                pending.extend(argument.named_children)
                continue
            try:
                ref = self.expression(argument, site.scope)
            except RecursionError:
                continue
            if ref.kind in {"callable", "class"} and ref.target:
                candidates.add(ref.target)
            candidates.update(ref.candidates)
        return sorted(candidate for candidate in candidates if candidate in self.index.nodes)

    def edges(self) -> list[Edge]:
        edges: list[Edge] = []
        duplicate_nodes = [node for node in self.index.nodes.values() if node.metadata.get("duplicate_definition")]
        for site in self.index.sites:
            try:
                ref = self.expression(site.function, site.scope)
            except RecursionError:
                ref = self.unknown("词法解析递归预算耗尽")
            if site.kind == "jsx" or (site.kind == "new" and ref.resolution != "external"):
                ref = self.unknown("JSX渲染/事件生命周期未静态展开" if site.kind == "jsx" else "构造器/实例分派未静态展开",
                                   candidates=ref.candidates or ([ref.target] if ref.target else []))
            if ref.resolution == "resolved" and ref.kind != "callable":
                ref = self.unknown("调用目标未解析为唯一函数实现", candidates=ref.candidates or ([ref.target] if ref.target else []))
            callbacks = self._callbacks(site)
            metadata = {"language": "typescript", "syntax_kind": site.node.type, "static_only": True,
                        "execution_order_verified": False, "call_kind": site.kind, **ref.metadata}
            if site.scope.module.projection.get("mode") == "adapted":
                metadata.update(source_parse_mode="adapted", syntax_projection_version=PROJECTION_VERSION,
                                source_projection_node="module:" + site.scope.module.name)
            if callbacks:
                metadata["callable_arguments"] = callbacks
                if ref.resolution == "external":
                    metadata["callbacks_unknown"] = True
            if site.kind == "jsx":
                metadata["implicit"] = "jsx_lifecycle"
                if site.function is not None:
                    metadata["component_expression"] = site.scope.module.text(site.function)
            ambiguous_sources = [node for node in duplicate_nodes if node.id == site.scope.owner or site.scope.owner.startswith(node.id + ".")
                                 or (node.kind == "module" and node.module == site.scope.module.name)]
            source_gap = self.index.source_unknowns.get(site.scope.owner)
            if ambiguous_sources or source_gap is not None:
                original = ref.target
                ref = self.unknown("源实现存在重复定义/重赋值，不能合并为确定调用", "ambiguous",
                                   [*ref.candidates, *([original] if original else [])])
                metadata["source_ambiguous"] = True
                metadata["source_definitions"] = [node.metadata.get("definitions", []) for node in ambiguous_sources]
            line, column = site.node.start_point.row + 1, site.node.start_point.column
            edges.append(Edge(_hash([ANALYZER_VERSION, site.scope.owner, site.scope.module.file.path,
                                     site.node.start_byte, site.node.end_byte, site.kind]), site.scope.owner,
                ref.target if ref.resolution == "resolved" else None,
                site.scope.module.text(site.function) or ("<JSX lifecycle>" if site.kind == "jsx" else "<unknown call>"),
                site.scope.module.file.path, line, column, ref.resolution, sorted(set(ref.candidates)), ref.reason, metadata))
        for node_id, ref in sorted(self.index.source_unknowns.items()):
            node = self.index.nodes[node_id]
            edges.append(Edge(_hash([node_id, "source_binding_boundary"]), node_id, None, "<source binding>",
                node.file, node.line, resolution="dynamic", candidates=ref.candidates, reason="源声明与最终词法绑定的关系不确定",
                metadata={"language": "typescript", "implicit": "source_binding_boundary", "source_ambiguous": True}))
        for node in sorted(self.index.nodes.values(), key=lambda item: item.id):
            if node.kind in {"class", "declaration"}:
                edges.append(Edge(_hash([node.id, "implementation_boundary"]), node.id, None,
                    "<constructor/implementation boundary>", node.file, node.line, resolution="dynamic",
                    candidates=sorted(self.index.object_members.get(node.id, {}).get("constructor", [])),
                    reason="类初始化/构造分派未展开" if node.kind == "class" else "仅声明，运行时实现未捕获",
                    metadata={"language": "typescript", "implicit": "constructor_dispatch" if node.kind == "class" else "ambient_implementation"}))
        return sorted(edges, key=lambda edge: (edge.file, edge.line, edge.column, edge.id))


def _apply_policy(index: _Index) -> None:
    for node in index.nodes.values():
        layers = [name for name, patterns in index.config.get("layers", {}).items()
                  if any(fnmatch.fnmatchcase(value, pattern) for pattern in patterns
                         for value in (node.id, node.qualname, node.module, node.file))]
        if len(layers) == 1:
            node.layer = layers[0]
        elif layers:
            node.metadata["candidate_layers"] = sorted(layers)
        if any(fnmatch.fnmatchcase(value, pattern) for pattern in index.config.get("entrypoints", [])
               for value in (node.id, node.qualname)):
            node.metadata["entrypoint"] = True


def analyze_files(files: list[SourceFile], root: Path, config: dict[str, Any]) -> dict[str, Any]:
    """Analyze only supplied text, returning copies and deterministic facts."""
    del root  # Authority is the caller's captured SourceFile list, never disk.
    index = _Index(config)
    outputs: list[SourceFile] = []
    states: list[_Module] = []
    parser_cache: dict[str, Any] = {}
    for source in sorted(files, key=lambda item: item.path):
        module_name = "ts:" + source.path.rsplit(".", 1)[0]
        captured = replace(source, module=module_name)
        data = captured.content.encode("utf-8")
        module = _Module(captured, data)
        states.append(module)
        index.modules.setdefault(captured.path, []).append(module)
        if source.status == "captured":
            grammar = "tsx" if PurePosixPath(source.path).suffix in {".tsx", ".jsx"} else "typescript"
            try:
                if grammar not in parser_cache:
                    parser_cache[grammar] = language_parser(grammar)
                parser = parser_cache[grammar]
                module.tree, module.projection = parse_with_projection(data, parser, grammar)
                module.projection["source_file_sha256"] = captured.hash
                if module.projection.get("applied"):
                    kinds = sorted({edit["rule"] for edit in module.projection.get("edits", [])})
                    accepted = module.projection.get("mode") == "adapted"
                    index.diagnostics.append(Diagnostic("info" if accepted else "warning",
                        "ts_syntax_projection" if accepted else "ts_projection_partial",
                        f"原始语法库存在缺口；派生解析{'成功' if accepted else '仍不完整'}，规则 {', '.join(kinds)}。原始源码/哈希与UTF8坐标不变；适配证据见模块metadata。",
                        captured.path, min((edit["line"] for edit in module.projection.get("edits", [])), default=1)))
                if module.tree.root_node.has_error:
                    errors: list[Any] = []
                    pending = [module.tree.root_node]
                    while pending and len(errors) < 12:
                        node = pending.pop()
                        if node.type == "ERROR" or node.is_missing:
                            errors.append(node)
                        elif node.has_error:
                            pending.extend(reversed(node.children))
                    locations = sorted({node.start_point.row + 1 for node in errors})
                    captured = replace(captured, status="parse_error", error="Tree-sitter 语法错误/不支持语法，行：" + ", ".join(map(str, locations)))
                    for node in errors:
                        index.diagnostics.append(Diagnostic("warning", "ts_parse_error", f"语法节点 {node.type}{' (missing)' if node.is_missing else ''} 未解析；保留文件覆盖缺口。",
                            captured.path, node.start_point.row + 1))
                elif captured.path.endswith((".d.ts", ".d.mts", ".d.cts")):
                    captured = replace(captured, status="declaration_only", error="类型声明文件不作为运行时实现。")
                    index.diagnostics.append(Diagnostic("info", "ts_declaration_file", captured.error or "", captured.path))
                else:
                    captured = replace(captured, status="parsed", error=None)
            except (RuntimeError, ValueError, OverflowError, RecursionError) as error:
                captured = replace(captured, status="parse_error", error=str(error))
                index.diagnostics.append(Diagnostic("warning", "ts_parser_failure", str(error), captured.path))
        module.file = captured
        outputs.append(captured)
        module_id = "module:" + module_name
        module_metadata = {"language": "typescript", "source_status": captured.status}
        if module.projection.get("raw_parser_has_error"):
            module_metadata["syntax_projection"] = module.projection
        index.add(Node(module_id, source.path, module_id, module_name, source.path, 1,
            max(1, len(source.content.splitlines())), "module", metadata=module_metadata))
        module.scope = _Scope("module", module, module_id, "")
        if captured.status != "parsed":
            index.coverage_incomplete = True
    collided = [node for node in index.nodes.values() if node.kind == "module" and node.metadata.get("duplicate_definition")]
    if collided:
        index.coverage_incomplete = True
        for node in collided:
            node.metadata["module_identity_collision"] = True
            index.diagnostics.append(Diagnostic("warning", "ts_module_identity_collision",
                "不同扩展名/重复输入共享模块身份，相关节点与调用保持歧义。", node.file, 1))
    for module in states:
        if module.file.status == "parsed" and module.tree is not None:
            try:
                _Collector(index, module).visit(module.tree.root_node)
            except RecursionError:
                index.coverage_incomplete = True
                module.file = replace(module.file, status="parse_error", error="CST遍历超过递归预算；只提取部分结构。")
                index.nodes["module:" + module.name].metadata["source_status"] = "parse_error"
                outputs = [module.file if source.path == module.file.path else source for source in outputs]
                index.diagnostics.append(Diagnostic("warning", "ts_traversal_limit", module.file.error or "", module.file.path))
    resolver = _Resolver(index)
    resolver.prepare()
    edges = resolver.edges()
    _apply_policy(index)
    counts = Counter(edge.resolution for edge in edges)
    callback_boundaries = sum(edge.resolution == "external" and bool(edge.metadata.get("callbacks_unknown") or edge.metadata.get("callable_arguments")) for edge in edges)
    ambiguous_symbols = sum(bool(node.metadata.get("duplicate_definition")) for node in index.nodes.values())
    call_incomplete = bool(callback_boundaries or ambiguous_symbols or any(counts[key] for key in ("dynamic", "unresolved", "ambiguous")))
    diagnostics = sorted(index.diagnostics, key=lambda item: (item.file, item.line, item.code, item.message))
    projection_rules = Counter(edit["rule"] for module in states if module.projection.get("mode") == "adapted"
                               for edit in module.projection.get("edits", []))
    stats = {"language": "typescript", "analyzer_version": ANALYZER_VERSION, "parser_version": PARSER_VERSION,
        "syntax_projection_version": PROJECTION_VERSION,
        "syntax_projected_files": sum(module.projection.get("mode") == "adapted" for module in states),
        "syntax_projection_edits_by_rule": dict(sorted(projection_rules.items())),
        "raw_parse_error_files": sum(bool(module.projection.get("raw_parser_has_error")) for module in states),
        "syntax_projection_partial_files": sum(module.projection.get("mode") in {"partial_projection", "rejected_projection"} for module in states),
        "files_total": len(outputs), "files_parsed": sum(source.status == "parsed" for source in outputs),
        "files_failed": sum(source.status != "parsed" for source in outputs), "nodes": len(index.nodes), "edges": len(edges),
        "resolved_calls": counts["resolved"], "external_calls": counts["external"], "dynamic_calls": counts["dynamic"],
        "ambiguous_calls": counts["ambiguous"], "unresolved_calls": counts["unresolved"],
        "external_callback_boundaries": callback_boundaries, "ambiguous_symbols": ambiguous_symbols,
        "coverage_incomplete": index.coverage_incomplete, "call_resolution_incomplete": call_incomplete,
        "incomplete": index.coverage_incomplete or call_incomplete,
        "limitations": ["仅捕获源码中的显式词法/ES模块调用；不执行目标", "类型/接口不证明对象运行时目标",
            "对象方法、构造、回调、JSX生命周期、动态import/CommonJS保持未知", "不证明分支、顺序、返回值、加载成功或业务结果"]}
    return {"nodes": sorted(index.nodes.values(), key=lambda item: item.id), "edges": edges,
            "files": outputs, "diagnostics": diagnostics, "stats": stats}
