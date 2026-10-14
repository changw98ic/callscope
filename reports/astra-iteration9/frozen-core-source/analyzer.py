"""Read-only Python call extraction.

This module never imports a target module and never runs a target interpreter,
test, build, hook, or sandbox. ``resolved`` means a binding in the supported
static model, not a proof that a call executes or returns the expected value.
Runtime dispatch, callbacks and incomplete source coverage remain explicit.
"""

from __future__ import annotations

import ast
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
import fnmatch
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import sys
import tokenize
from typing import Any

from .config import load_config, validate_config
from .models import (
    ANALYZER_VERSION, DETECTOR_VERSION, PARSER_VERSION, SCHEMA_VERSION, Diagnostic, Edge,
    GraphSnapshot, Node, SourceFile, project_id_for,
)


# Dependency/generated directories are never traversed, even when a custom
# exclusion list replaces the configuration defaults.
_IGNORED_DIRS = {
    ".git", ".hg", ".svn", ".venv", "venv", "env", "__pycache__",
    "node_modules", ".callscope", "build", "dist", ".tox", ".nox",
    ".mypy_cache", ".pytest_cache", ".ruff_cache", "site-packages",
    "__pypackages__", ".eggs",
}
_BUILTIN_CALLABLES = {
    "abs", "aiter", "all", "anext", "any", "ascii", "bin", "bool",
    "breakpoint", "bytearray", "bytes", "callable", "chr", "classmethod",
    "compile", "complex", "delattr", "dict", "dir", "divmod", "enumerate",
    "eval", "exec", "filter", "float", "format", "frozenset", "getattr",
    "globals", "hasattr", "hash", "help", "hex", "id", "input", "int",
    "isinstance", "issubclass", "iter", "len", "list", "locals", "map",
    "max", "memoryview", "min", "next", "object", "oct", "open", "ord",
    "pow", "print", "property", "range", "repr", "reversed", "round",
    "set", "setattr", "slice", "sorted", "staticmethod", "str", "sum",
    "super", "tuple", "type", "vars", "zip", "__import__",
    # Exception constructors are ordinary external builtin callables.
    "BaseException", "Exception", "ArithmeticError", "AssertionError",
    "AttributeError", "EOFError", "ImportError", "ModuleNotFoundError",
    "IndexError", "KeyError", "LookupError", "MemoryError", "NameError",
    "NotImplementedError", "OSError", "OverflowError", "RecursionError",
    "ReferenceError", "RuntimeError", "StopAsyncIteration", "StopIteration",
    "SyntaxError", "SystemError", "TypeError", "UnboundLocalError",
    "UnicodeError", "ValueError", "ZeroDivisionError", "Warning",
    "UserWarning", "DeprecationWarning", "RuntimeWarning", "SystemExit",
    "KeyboardInterrupt", "GeneratorExit", "TimeoutError", "FileNotFoundError",
    "PermissionError", "ConnectionError", "NotADirectoryError",
    "IsADirectoryError", "BrokenPipeError",
}
_REFLECTIVE_BUILTINS = {"exec", "eval", "__import__", "getattr", "setattr", "globals", "locals", "vars", "super"}
_STDLIB_MODULES = set(getattr(sys, "stdlib_module_names", ())) | {"builtins", "sys", "os", "typing"}


def _digest(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _text(node: ast.AST | None, limit: int = 600) -> str:
    if node is None:
        return ""
    try:
        return ast.unparse(node)[:limit]
    except (ValueError, RecursionError):
        return node.__class__.__name__


@dataclass
class _Binding:
    kind: str
    line: int = 0
    target: str = ""
    expr: ast.AST | None = None
    module: str = ""
    member: str = ""
    level: int = 0
    conditional: bool = False
    reason: str = ""
    scope: _Scope | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class _Scope:
    kind: str
    module: _Module
    owner: str
    qualpath: str
    parent: _Scope | None = None
    bindings: dict[str, list[_Binding]] = field(default_factory=dict)
    globals: set[str] = field(default_factory=set)
    nonlocals: set[str] = field(default_factory=set)
    star_imports: list[str] = field(default_factory=list)
    class_id: str = ""
    call_owner: str = ""


@dataclass
class _Module:
    name: str
    source: SourceFile
    tree: ast.Module | None
    package: str
    is_package: bool
    aliases: list[str]
    importable_aliases: list[str] = field(default_factory=list)
    scope: _Scope | None = None
    future_annotations: bool = False


@dataclass
class _Ref:
    resolution: str
    kind: str = "unknown"
    target: str | None = None
    module: str = ""
    external_symbol: str = ""
    candidates: list[str] = field(default_factory=list)
    reason: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class _CallSite:
    func: ast.AST
    anchor: ast.AST
    scope: _Scope
    implicit: str = ""


class _Index:
    def __init__(self, config: dict[str, Any], diagnostics: list[Diagnostic]):
        self.config = config
        self.diagnostics = diagnostics
        self.nodes: dict[str, Node] = {}
        self.modules: dict[str, list[_Module]] = {}
        self.module_states: list[_Module] = []
        self.namespaces: set[str] = set()
        self.expr_scopes: dict[int, _Scope] = {}
        self.lambda_ids: dict[int, str] = {}
        self.classes: dict[str, list[_Scope]] = {}
        self.class_defs: dict[str, list[ast.ClassDef]] = {}
        self.class_bases: dict[str, list[str]] = {}
        self.uncertain_bases: set[str] = set()
        self.calls: list[_CallSite] = []
        self.coverage_incomplete = False
        self.constructed_classes: set[str] = set()
        self.attribute_writes: list[tuple[ast.Attribute, _Scope]] = []
        self.attribute_invalidations: set[tuple[str, str]] = set()
        self.unknown_attribute_writes: set[str] = set()
        self.nonlocal_writes: list[tuple[str, _Binding, _Scope]] = []
        self.symbol_decorators: dict[str, list[tuple[list[ast.expr], _Scope]]] = {}
        self.method_parameters: dict[str, list[tuple[_Scope, str]]] = {}

    def add_node(self, node: Node) -> None:
        prior = self.nodes.get(node.id)
        if prior is None:
            self.nodes[node.id] = node
            return
        locations = prior.metadata.setdefault("definitions", [{
            "file": prior.file, "line": prior.line, "end_line": prior.end_line,
            "kind": prior.kind, "signature": prior.signature,
        }])
        locations.append({"file": node.file, "line": node.line, "end_line": node.end_line,
                          "kind": node.kind, "signature": node.signature})
        prior.metadata["duplicate_definition"] = True
        self.diagnostics.append(Diagnostic("warning", "duplicate_definition",
            f"符号 {node.id} 有多个声明；调用目标保留歧义。", node.file, node.line))

    def register_module(self, module: _Module) -> None:
        self.module_states.append(module)
        for alias in module.aliases:
            self.modules.setdefault(alias, []).append(module)
            parts = alias.split(".")
            if alias in module.importable_aliases:
                self.namespaces.update(".".join(parts[:i]) for i in range(1, len(parts)))
        module_id = "module:" + module.name
        self.add_node(Node(module_id, module.name, module_id, module.name,
            module.source.path, 1, max(1, len(module.source.content.splitlines())), "module",
            metadata={"source_status": module.source.status, "import_aliases": module.aliases,
                      "is_package": module.is_package}))
        module.scope = _Scope("module", module, module_id, "")

    def finalize_module_registry(self) -> None:
        for name, modules in sorted(self.modules.items()):
            if len(modules) > 1:
                self.coverage_incomplete = True
                files = sorted(module.source.path for module in modules)
                self.diagnostics.append(Diagnostic("warning", "module_collision",
                    f"导入名 {name} 对应多个源码文件，不能确定导入目标：{', '.join(files)}"))
        for namespace in sorted(self.namespaces - set(self.modules)):
            module_id = "module:" + namespace
            self.nodes.setdefault(module_id, Node(module_id, namespace, module_id,
                namespace, "", 0, 0, "module", metadata={"namespace_package": True}))


def _directives(body: list[ast.stmt]) -> tuple[set[str], set[str]]:
    globals_: set[str] = set()
    nonlocals: set[str] = set()
    pending: list[ast.AST] = list(body)
    while pending:
        node = pending.pop()
        if isinstance(node, ast.Global):
            globals_.update(node.names)
        elif isinstance(node, ast.Nonlocal):
            nonlocals.update(node.names)
        elif not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
            pending.extend(ast.iter_child_nodes(node))
    return globals_, nonlocals


class _Collector(ast.NodeVisitor):
    """Collect declarations and every binding before resolving any call."""

    def __init__(self, index: _Index, module: _Module):
        self.index = index
        self.module = module
        assert module.scope is not None
        self.scope = module.scope
        self.conditional = 0

    def visit(self, node: ast.AST) -> Any:
        self.index.expr_scopes[id(node)] = self.scope
        return super().visit(node)

    def _module_scope(self) -> _Scope:
        assert self.module.scope is not None
        return self.module.scope

    def _bind(self, name: str, binding: _Binding) -> None:
        scope = self.scope
        if name in scope.globals:
            scope = self._module_scope()
            if self.scope is not scope:
                binding = _Binding("unknown", binding.line, reason="global 名称在函数执行时被修改",
                                   conditional=True, scope=self.scope)
        elif name in scope.nonlocals:
            binding = _Binding("unknown", binding.line, reason="nonlocal 名称在运行时被修改",
                               conditional=True, scope=self.scope)
            # The enclosing declaration may appear later in its body. Resolve
            # the write after collection rather than losing that invalidation.
            self.index.nonlocal_writes.append((name, binding, self.scope))
            return
        binding.scope = binding.scope or self.scope
        binding.conditional = binding.conditional or self.conditional > 0
        scope.bindings.setdefault(name, []).append(binding)

    def _target(self, target: ast.AST, value: ast.AST | None = None, reason: str = "运行时赋值") -> None:
        self.index.expr_scopes[id(target)] = self.scope
        if isinstance(target, ast.Name):
            self._bind(target.id, _Binding("assignment" if value is not None else "unknown",
                getattr(target, "lineno", 0), expr=value, reason=reason, scope=self.scope))
        elif isinstance(target, (ast.Tuple, ast.List)):
            for child in target.elts:
                self._target(child, reason="解构赋值的目标类型未推断")
        elif isinstance(target, ast.Starred):
            self._target(target.value, reason="可变长度解构赋值")
        else:
            # Attribute/subscript stores can execute receiver and index calls.
            if isinstance(target, ast.Attribute):
                self.index.attribute_writes.append((target, self.scope))
            self.visit(target)

    def visit_Call(self, node: ast.Call) -> None:
        self.index.calls.append(_CallSite(node.func, node, self.scope))
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            bound = alias.asname or alias.name.split(".")[0]
            self._bind(bound, _Binding("module_import", node.lineno,
                module=alias.name if alias.asname else alias.name.split(".")[0],
                metadata={"loaded_module": alias.name}))

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module == "__future__":
            return
        for alias in node.names:
            if alias.name == "*":
                self.scope.star_imports.append("." * node.level + (node.module or ""))
                self.index.diagnostics.append(Diagnostic("warning", "star_import",
                    "星号导入的运行时导出集合未推断，不能据此确认缺失名称。", self.module.source.path, node.lineno))
            else:
                self._bind(alias.asname or alias.name, _Binding("member_import", node.lineno,
                    module=node.module or "", member=alias.name, level=node.level))

    def _function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        parent = self.scope
        qualpath = f"{parent.qualpath}.{node.name}" if parent.qualpath else node.name
        node_id = f"{self.module.name}.{qualpath}"
        decorators = [_text(item) for item in node.decorator_list]
        recognized = {"staticmethod", "classmethod", "builtins.staticmethod", "builtins.classmethod"}
        transformed = any(item not in recognized for item in decorators)
        method = parent.kind == "class"
        metadata: dict[str, Any] = {"async": isinstance(node, ast.AsyncFunctionDef),
            "decorators": decorators, "decorated_binding": transformed,
            "conditional_definition": self.conditional > 0}
        if method:
            metadata["class_id"] = parent.owner
        signature = f"{node.name}({_text(node.args)})"
        if node.returns is not None:
            signature += " -> " + _text(node.returns)
        self.index.add_node(Node(node_id, node.name, node_id, self.module.name,
            self.module.source.path, node.lineno, getattr(node, "end_lineno", node.lineno),
            "method" if method else "function", signature[:900], metadata=metadata))
        self.index.symbol_decorators.setdefault(node_id, []).append((node.decorator_list, parent))
        self._bind(node.name, _Binding("symbol", node.lineno, target=node_id,
            metadata={"decorated": transformed}))
        for decorator in node.decorator_list:
            self.visit(decorator)
            self.index.calls.append(_CallSite(decorator, decorator, parent, "decorator_application"))
        for default in [*node.args.defaults, *[item for item in node.args.kw_defaults if item is not None]]:
            self.visit(default)
        if not self.module.future_annotations:
            for arg in [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs]:
                if arg.annotation is not None:
                    self.visit(arg.annotation)
            for arg in (node.args.vararg, node.args.kwarg):
                if arg is not None and arg.annotation is not None:
                    self.visit(arg.annotation)
            if node.returns is not None:
                self.visit(node.returns)
        globals_, nonlocals = _directives(node.body)
        function_scope = _Scope("function", self.module, node_id, qualpath, parent,
                                globals=globals_, nonlocals=nonlocals,
                                class_id=parent.owner if method else parent.class_id)
        parameters = [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs]
        if node.args.vararg:
            parameters.append(node.args.vararg)
        if node.args.kwarg:
            parameters.append(node.args.kwarg)
        for parameter in parameters:
            function_scope.bindings[parameter.arg] = [_Binding("parameter", parameter.lineno,
                reason="参数/回调的运行时值未推断", scope=function_scope)]
        positional = [*node.args.posonlyargs, *node.args.args]
        if method and positional and not any(item.endswith("staticmethod") for item in decorators):
            is_cls = any(item.endswith("classmethod") for item in decorators)
            function_scope.bindings[positional[0].arg] = [_Binding("receiver", node.lineno,
                target=parent.owner, scope=function_scope,
                metadata={"receiver": "class_parameter" if is_cls else "instance_parameter"})]
        if method and positional:
            self.index.method_parameters.setdefault(node_id, []).append((function_scope, positional[0].arg))
        if method:
            function_scope.bindings["__class__"] = [_Binding("class_reference", node.lineno,
                target=parent.owner, scope=function_scope)]
        old_conditional = self.conditional
        self.scope, self.conditional = function_scope, 0
        for statement in node.body:
            self.visit(statement)
        self.scope, self.conditional = parent, old_conditional

    visit_FunctionDef = _function
    visit_AsyncFunctionDef = _function

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        parent = self.scope
        qualpath = f"{parent.qualpath}.{node.name}" if parent.qualpath else node.name
        node_id = f"{self.module.name}.{qualpath}"
        decorators = [_text(item) for item in node.decorator_list]
        self.index.add_node(Node(node_id, node.name, node_id, self.module.name,
            self.module.source.path, node.lineno, getattr(node, "end_lineno", node.lineno),
            "class", metadata={"decorators": decorators, "decorated_binding": bool(decorators),
                "bases": [_text(item) for item in node.bases], "metaclass": any(k.arg == "metaclass" for k in node.keywords),
                "constructor_dispatch_expanded": False, "conditional_definition": self.conditional > 0}))
        self.index.symbol_decorators.setdefault(node_id, []).append((node.decorator_list, parent))
        self._bind(node.name, _Binding("symbol", node.lineno, target=node_id,
                                      metadata={"decorated": bool(decorators)}))
        for decorator in node.decorator_list:
            self.visit(decorator)
            self.index.calls.append(_CallSite(decorator, decorator, parent, "decorator_application"))
        for expression in [*node.bases, *[keyword.value for keyword in node.keywords]]:
            self.visit(expression)
        # The class suite executes at declaration time in the surrounding
        # execution context. It is not the body of a later C() constructor call.
        class_scope = _Scope("class", self.module, node_id, qualpath, parent, class_id=node_id,
                             call_owner=parent.call_owner or parent.owner)
        class_scope.globals, class_scope.nonlocals = _directives(node.body)
        self.index.classes.setdefault(node_id, []).append(class_scope)
        self.index.class_defs.setdefault(node_id, []).append(node)
        self.scope = class_scope
        for statement in node.body:
            self.visit(statement)
        self.scope = parent

    def visit_Lambda(self, node: ast.Lambda) -> None:
        parent = self.scope
        name = f"<lambda@{node.lineno}:{node.col_offset}>"
        qualpath = f"{parent.qualpath}.{name}" if parent.qualpath else name
        node_id = f"{self.module.name}.{qualpath}"
        self.index.lambda_ids[id(node)] = node_id
        self.index.add_node(Node(node_id, name, node_id, self.module.name, self.module.source.path,
            node.lineno, getattr(node, "end_lineno", node.lineno), "function", "lambda " + _text(node.args),
            metadata={"lambda": True}))
        for default in [*node.args.defaults, *[item for item in node.args.kw_defaults if item is not None]]:
            self.visit(default)
        scope = _Scope("function", self.module, node_id, qualpath, parent, class_id=parent.class_id)
        args = [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs]
        args += [item for item in (node.args.vararg, node.args.kwarg) if item is not None]
        for arg in args:
            scope.bindings[arg.arg] = [_Binding("parameter", node.lineno, reason="lambda 参数的运行时值未推断", scope=scope)]
        self.scope = scope
        self.visit(node.body)
        self.scope = parent

    def visit_Assign(self, node: ast.Assign) -> None:
        self.visit(node.value)
        for target in node.targets:
            self._target(target, node.value)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if node.value is not None:
            self.visit(node.value)
            self._target(node.target, node.value)
        else:
            self._target(node.target, reason="仅类型声明，不证明存在运行时值")
        if self.scope.kind in {"module", "class"} and not self.module.future_annotations:
            self.visit(node.annotation)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        self.visit(node.value)
        self._target(node.target, reason="增量赋值改变运行时绑定")

    def visit_NamedExpr(self, node: ast.NamedExpr) -> None:
        self.visit(node.value)
        parent = self.scope
        while self.scope.kind == "comprehension" and self.scope.parent is not None:
            self.scope = self.scope.parent
        self._target(node.target, node.value, "赋值表达式")
        self.scope = parent

    def visit_Delete(self, node: ast.Delete) -> None:
        for target in node.targets:
            self._target(target, reason="名称可能被删除")

    def _conditional_block(self, statements: list[ast.stmt]) -> None:
        self.conditional += 1
        for statement in statements:
            self.visit(statement)
        self.conditional -= 1

    def visit_If(self, node: ast.If) -> None:
        self.visit(node.test)
        self._conditional_block(node.body)
        self._conditional_block(node.orelse)

    def visit_While(self, node: ast.While) -> None:
        self.visit(node.test)
        self._conditional_block(node.body)
        self._conditional_block(node.orelse)

    def visit_For(self, node: ast.For | ast.AsyncFor) -> None:
        self.visit(node.iter)
        self._target(node.target, reason="循环变量的运行时值未推断")
        self._conditional_block(node.body)
        self._conditional_block(node.orelse)

    visit_AsyncFor = visit_For

    def visit_With(self, node: ast.With | ast.AsyncWith) -> None:
        for item in node.items:
            self.visit(item.context_expr)
            if item.optional_vars is not None:
                self._target(item.optional_vars, reason="上下文管理器返回值未推断")
        self._conditional_block(node.body)

    visit_AsyncWith = visit_With

    def visit_Try(self, node: ast.Try) -> None:
        self._conditional_block(node.body)
        for handler in node.handlers:
            if handler.type is not None:
                self.visit(handler.type)
            if handler.name:
                self._bind(handler.name, _Binding("unknown", handler.lineno,
                    reason="异常处理变量在运行时绑定和删除", conditional=True))
            self._conditional_block(handler.body)
        self._conditional_block(node.orelse)
        self._conditional_block(node.finalbody)

    visit_TryStar = visit_Try

    def visit_Match(self, node: ast.Match) -> None:
        self.visit(node.subject)
        for case in node.cases:
            self.conditional += 1
            for pattern in ast.walk(case.pattern):
                name = getattr(pattern, "name", None)
                if isinstance(name, str):
                    self._bind(name, _Binding("unknown", getattr(pattern, "lineno", node.lineno), reason="模式匹配绑定未推断"))
                rest = getattr(pattern, "rest", None)
                if isinstance(rest, str):
                    self._bind(rest, _Binding("unknown", getattr(pattern, "lineno", node.lineno), reason="模式匹配映射绑定未推断"))
            self.visit(case.pattern)
            if case.guard is not None:
                self.visit(case.guard)
            for statement in case.body:
                self.visit(statement)
            self.conditional -= 1

    def _comprehension(self, node: ast.AST) -> None:
        parent = self.scope
        generators = getattr(node, "generators", [])
        if generators:
            self.visit(generators[0].iter)
        self.scope = _Scope("comprehension", self.module, parent.owner, parent.qualpath, parent,
                            class_id=parent.class_id, call_owner=parent.call_owner)
        for i, generator in enumerate(generators):
            if i:
                self.visit(generator.iter)
            self._target(generator.target, reason="推导式变量的运行时值未推断")
            for expression in generator.ifs:
                self.visit(expression)
        for name in ("elt", "key", "value"):
            expression = getattr(node, name, None)
            if expression is not None:
                self.visit(expression)
        self.scope = parent

    visit_ListComp = _comprehension
    visit_SetComp = _comprehension
    visit_DictComp = _comprehension
    visit_GeneratorExp = _comprehension


class _Resolver:
    def __init__(self, index: _Index):
        self.index = index

    @staticmethod
    def _unknown(reason: str, resolution: str = "dynamic", candidates: list[str] | None = None) -> _Ref:
        return _Ref(resolution, candidates=sorted(set(candidates or [])), reason=reason)

    def _module_ref(self, name: str, *, required_local: bool = False) -> _Ref:
        modules = self.index.modules.get(name, [])
        if len(modules) > 1:
            return self._unknown(f"导入名 {name} 对应多个源码文件", "ambiguous",
                ["module:" + module.name for module in modules])
        if modules:
            module = modules[0]
            if name not in module.importable_aliases:
                return self._unknown(f"源码路径不是标准 Python 导入路径：{module.source.path}", "unresolved")
            if module.source.status != "parsed":
                return self._unknown(f"本地模块 {name} 未成功解析 ({module.source.status})", "unresolved")
            return _Ref("resolved", "module", "module:" + module.name, name,
                reason="本地模块导入", metadata={"canonical_module": module.name})
        if name in self.index.namespaces:
            return _Ref("resolved", "module", "module:" + name, name, reason="本地 namespace 包")
        first = name.split(".")[0]
        local_top = first in self.index.modules or first in self.index.namespaces
        if required_local or local_top:
            return self._unknown(f"本地导入目标 {name} 不在已解析源码中", "unresolved")
        classification = "stdlib" if first in _STDLIB_MODULES else "declared_external"
        return _Ref("external", "module", module=name, external_symbol=name,
            reason="外部导入声明；不验证依赖安装或外部 API 存在性",
            metadata={"external_kind": classification, "availability_verified": False})

    def _absolute_import(self, binding: _Binding, scope: _Scope) -> str | None:
        if not binding.level:
            return binding.module
        package = scope.module.package
        parts = package.split(".") if package else []
        ascend = binding.level - 1
        if not parts or ascend >= len(parts):
            return None
        prefix = ".".join(parts[:len(parts) - ascend])
        return prefix + ("." + binding.module if binding.module else "")

    def _combine(self, refs: list[_Ref], reason: str, *, force: bool = False) -> _Ref:
        if len(refs) == 1 and not force:
            return refs[0]
        identities = {(ref.resolution, ref.kind, ref.target, ref.module, ref.external_symbol) for ref in refs}
        if len(identities) == 1 and not force and all(ref.resolution in {"resolved", "external"} for ref in refs):
            ref = refs[0]
            loaded_modules = sorted({loaded for item in refs for loaded in [
                *item.metadata.get("loaded_modules", []), *([item.metadata["loaded_module"]] if item.metadata.get("loaded_module") else [])]})
            if loaded_modules:
                ref.metadata = {**ref.metadata, "loaded_modules": loaded_modules}
            return ref
        candidates = sorted({candidate for ref in refs for candidate in [*ref.candidates, *([ref.target] if ref.target else [])]})
        resolution = "ambiguous" if len(candidates) > 1 or (force and candidates) else "dynamic"
        return self._unknown(reason, resolution, candidates)

    def _symbol(self, target: str, decorated: bool = False) -> _Ref:
        node = self.index.nodes.get(target)
        if node is None:
            return self._unknown("声明目标未建立节点", "unresolved")
        if node.metadata.get("duplicate_definition"):
            return self._unknown("同一限定名有多个定义，不能确定绑定", "ambiguous", [target])
        if decorated or node.metadata.get("decorated_binding"):
            return self._unknown("装饰器可能替换原始声明的绑定", "dynamic", [target])
        return _Ref("resolved", "class" if node.kind == "class" else "callable", target,
                    reason="静态声明绑定", metadata={"binding_model": "lexical_declaration"})

    def _binding(self, binding: _Binding, scope: _Scope, seen: set[tuple[int, str]]) -> _Ref:
        origin = binding.scope or scope
        if binding.kind == "symbol":
            # Decorator identity is verified against final lexical bindings in
            # prepare_decorators; its textual spelling is never sufficient.
            return self._symbol(binding.target)
        if binding.kind == "module_import":
            ref = self._module_ref(binding.module)
            ref.metadata = {**ref.metadata, "loaded_module": binding.metadata.get("loaded_module", binding.module)}
            return ref
        if binding.kind == "member_import":
            absolute = self._absolute_import(binding, origin)
            if absolute is None:
                return self._unknown("相对导入超出配置的包根", "unresolved")
            module = self._module_ref(absolute, required_local=bool(binding.level))
            return self._member(module, binding.member, origin, seen, importing=True)
        if binding.kind in {"receiver", "class_reference"}:
            return _Ref("resolved", "class" if binding.kind == "class_reference" or binding.metadata.get("receiver") == "class_parameter" else "instance",
                binding.target, reason="声明方法的基础 self/cls 绑定", metadata=dict(binding.metadata))
        if binding.kind == "assignment" and binding.expr is not None:
            # Assignments are not executed; only simple aliases and simple local
            # construction carry a useful static receiver type.
            ref = self.expression(binding.expr, origin, seen)
            ref.metadata = {**ref.metadata, "assignment_inference": "single_static_binding"}
            return ref
        return self._unknown(binding.reason or "名称的运行时值未推断")

    def _scope_binding(self, scope: _Scope, name: str, seen: set[tuple[int, str]]) -> _Ref | None:
        bindings = scope.bindings.get(name)
        if not bindings:
            return None
        key = (id(scope), name)
        if key in seen:
            return self._unknown("别名/重导出解析存在循环", "dynamic")
        refs = [self._binding(binding, scope, seen | {key}) for binding in bindings]
        invalidated = scope.kind in {"class", "module"} and (
            (scope.owner if scope.kind == "class" else scope.module.name, name) in self.index.attribute_invalidations
            or name in self.index.unknown_attribute_writes)
        conditional = any(binding.conditional for binding in bindings)
        # Repeated imports of exactly the same target do not invent ambiguity;
        # redefinitions and reassignments always retain it.
        repeated_imports = all(binding.kind in {"module_import", "member_import"} for binding in bindings)
        force = conditional or invalidated or bool(scope.star_imports) or (len(bindings) > 1 and not repeated_imports)
        reason = ("显式属性写入可能覆盖声明" if invalidated else
                  "星号导入可能覆盖已有声明" if scope.star_imports else "名称存在条件绑定、重定义或赋值覆盖")
        return self._combine(refs, reason, force=force)

    def name(self, name: str, scope: _Scope, seen: set[tuple[int, str]], line: int = 0) -> _Ref:
        direct = scope.bindings.get(name, [])
        if line and direct and name not in scope.globals and name not in scope.nonlocals:
            if all(binding.line > line for binding in direct):
                return self._unknown("同一词法作用域中，该名称的调用/引用早于声明或赋值", "unresolved",
                    [binding.target for binding in direct if binding.target])
        if name in scope.globals:
            assert scope.module.scope is not None
            module_scope = scope.module.scope
            ref = self._scope_binding(module_scope, name, seen)
            if ref is not None:
                return ref
            scope = module_scope
        elif name in scope.nonlocals:
            scope = scope.parent or scope
            while scope.kind == "class" and scope.parent is not None:
                scope = scope.parent
        cursor: _Scope | None = scope
        skip_classes = scope.kind in {"function", "comprehension"}
        while cursor is not None:
            if not (skip_classes and cursor.kind == "class"):
                ref = self._scope_binding(cursor, name, seen)
                if ref is not None:
                    return ref
                if cursor.star_imports:
                    return self._unknown("星号导入可能提供或覆盖此名称")
            if cursor.kind in {"function", "comprehension"}:
                skip_classes = True
            cursor = cursor.parent
        if name in _BUILTIN_CALLABLES:
            return _Ref("external", "callable", external_symbol="builtins." + name,
                reason="Python builtin 名称", metadata={"external_kind": "builtin", "availability_verified": True})
        if name in {"None", "True", "False", "NotImplemented", "Ellipsis"}:
            return _Ref("resolved", "value", reason="已知非调用值")
        return self._unknown(f"名称 {name} 没有可解析的词法声明", "unresolved")

    def _class_member(self, class_id: str, name: str, seen: set[tuple[int, str]], visited: set[str]) -> _Ref:
        if class_id in visited:
            return self._unknown("继承解析循环")
        scopes = self.index.classes.get(class_id, [])
        if len(scopes) != 1:
            return self._unknown("类声明有歧义", "ambiguous", [class_id])
        scope = scopes[0]
        direct = self._scope_binding(scope, name, seen)
        if direct is not None:
            return direct
        bases = self.index.class_bases.get(class_id, [])
        refs = [self._class_member(base, name, seen, visited | {class_id}) for base in bases]
        useful = [ref for ref in refs if ref.resolution in {"resolved", "external", "ambiguous"}]
        if class_id in self.index.uncertain_bases:
            return self._unknown("继承/元类分派未完整解析", candidates=[ref.target for ref in useful if ref.target])
        if len(bases) > 1:
            return self._combine(refs, "多重继承的 MRO 分派未推断", force=True)
        if useful:
            return useful[0]
        return self._unknown(f"类 {class_id} 未声明属性 {name}；运行时实例属性未推断")

    def _has_custom_dispatch(self, class_id: str, visited: set[str] | None = None) -> bool:
        visited = visited or set()
        if class_id in visited:
            return True
        node = self.index.nodes.get(class_id)
        scopes = self.index.classes.get(class_id, [])
        if node is None or len(scopes) != 1 or class_id in self.index.uncertain_bases:
            return True
        if node.metadata.get("decorated_binding") or node.metadata.get("metaclass"):
            return True
        if any((class_id, name) in self.index.attribute_invalidations or name in self.index.unknown_attribute_writes
               for name in ("__getattribute__", "__getattr__")):
            return True
        if any("__getattribute__" in scope.bindings or "__getattr__" in scope.bindings for scope in scopes):
            return True
        return any(self._has_custom_dispatch(base, visited | {class_id})
                   for base in self.index.class_bases.get(class_id, []))

    def _subclass_overrides(self, class_id: str, name: str) -> tuple[list[str], bool]:
        found: set[str] = set()
        unknown_override = False
        frontier = [class_id]
        visited = {class_id}
        while frontier:
            parent = frontier.pop()
            for child, bases in self.index.class_bases.items():
                if parent in bases and child not in visited:
                    visited.add(child)
                    frontier.append(child)
                    if self._has_custom_dispatch(child):
                        unknown_override = True
                    if (child, name) in self.index.attribute_invalidations or name in self.index.unknown_attribute_writes:
                        unknown_override = True
                    for scope in self.index.classes.get(child, []):
                        if name in scope.bindings:
                            override = self._scope_binding(scope, name, set())
                            if override is not None:
                                if override.target:
                                    found.add(override.target)
                                found.update(override.candidates)
                                if override.resolution != "resolved" or override.kind not in {"callable", "class"} or not override.target:
                                    unknown_override = True
                            else:
                                unknown_override = True
        return sorted(found), unknown_override

    def _member(self, base: _Ref, name: str, scope: _Scope, seen: set[tuple[int, str]], *, importing: bool = False) -> _Ref:
        if base.resolution == "external":
            symbol = base.external_symbol or base.module
            metadata = {**base.metadata, "availability_verified": False}
            if symbol == "builtins" and name in _BUILTIN_CALLABLES:
                metadata.update({"external_kind": "builtin", "availability_verified": True})
            return _Ref("external", "module" if importing else "callable",
                module=symbol + "." + name if importing else "", external_symbol=symbol + "." + name,
                reason="外部导入/属性声明；外部实现未扫描", metadata=metadata)
        if base.resolution != "resolved":
            return self._unknown(base.reason, base.resolution, base.candidates)
        if base.kind == "module":
            modules = self.index.modules.get(base.module, [])
            canonical = modules[0].name if len(modules) == 1 else base.module
            if (canonical, name) in self.index.attribute_invalidations or name in self.index.unknown_attribute_writes:
                return self._unknown("显式属性写入可能覆盖模块属性", candidates=[canonical + "." + name]
                    if canonical + "." + name in self.index.nodes else [])
            if len(modules) == 1:
                module = modules[0]
                if module.scope is not None:
                    ref = self._scope_binding(module.scope, name, seen)
                    if ref is not None:
                        return ref
                    if module.scope.star_imports:
                        return self._unknown("本地模块使用星号重导出，属性集合未确定")
                    if "__getattr__" in module.scope.bindings:
                        return self._unknown("本地模块的 __getattr__ 可能动态提供属性")
            child = base.module + "." + name
            loaded = str(base.metadata.get("loaded_module", ""))
            loaded_modules = [loaded, *base.metadata.get("loaded_modules", [])]
            explicitly_loaded = any(item == child or item.startswith(child + ".") for item in loaded_modules)
            if importing or explicitly_loaded:
                ref = self._module_ref(child, required_local=True)
                if ref.resolution == "resolved":
                    ref.metadata = {**ref.metadata, "loaded_module": loaded or child, "loaded_modules": loaded_modules or [child]}
                return ref
            return self._unknown(f"本地模块 {base.module} 没有已声明/已加载的属性 {name}", "unresolved")
        if base.kind in {"class", "instance"} and base.target:
            ref = self._class_member(base.target, name, seen, set())
            if (base.target, name) in self.index.attribute_invalidations or name in self.index.unknown_attribute_writes:
                return self._unknown("显式实例/类属性写入可能覆盖调用目标", candidates=[ref.target] if ref.target else ref.candidates)
            if self._has_custom_dispatch(base.target):
                return self._unknown("类/基类具有未解析属性分派、装饰器或元类", candidates=[ref.target] if ref.target else ref.candidates)
            if base.metadata.get("receiver") in {"instance_parameter", "class_parameter"}:
                overrides, unknown_override = self._subclass_overrides(base.target, name)
                if overrides or unknown_override:
                    return self._unknown("self/cls 的已知子类存在覆盖/动态分派，不能选择唯一目标", "ambiguous" if overrides else "dynamic",
                        [*overrides, *([ref.target] if ref.target else ref.candidates)])
            ref.metadata = {**ref.metadata, "receiver_model": base.metadata.get("receiver", "static_class_or_simple_instance")}
            return ref
        return self._unknown("对象属性/返回值的运行时类型未推断", candidates=base.candidates)

    def _simple_constructor(self, class_id: str, seen: set[str] | None = None) -> bool:
        seen = seen or set()
        if class_id in seen:
            return False
        node = self.index.nodes.get(class_id)
        scopes = self.index.classes.get(class_id, [])
        if node is None or len(scopes) != 1 or node.metadata.get("duplicate_definition"):
            return False
        if node.metadata.get("decorated_binding") or node.metadata.get("metaclass") or class_id in self.index.uncertain_bases:
            return False
        if any((class_id, name) in self.index.attribute_invalidations or name in self.index.unknown_attribute_writes
               for name in ("__new__", "__init__", "__class__", "__call__")):
            return False
        if "__new__" in scopes[0].bindings:
            return False
        return all(self._simple_constructor(base, seen | {class_id}) for base in self.index.class_bases.get(class_id, []))

    def expression(self, node: ast.AST, scope: _Scope, seen: set[tuple[int, str]] | None = None) -> _Ref:
        seen = seen or set()
        if len(seen) > 120:
            return self._unknown("静态别名解析深度预算耗尽")
        if isinstance(node, ast.Name):
            return self.name(node.id, scope, seen, getattr(node, "lineno", 0))
        if isinstance(node, ast.Attribute):
            return self._member(self.expression(node.value, scope, seen), node.attr, scope, seen)
        if isinstance(node, ast.Lambda):
            target = self.index.lambda_ids.get(id(node))
            return self._symbol(target) if target else self._unknown("lambda 未建立声明")
        if isinstance(node, ast.Call):
            callee = self.expression(node.func, scope, seen)
            if callee.resolution == "resolved" and callee.kind == "class" and callee.target:
                if self._simple_constructor(callee.target):
                    return _Ref("resolved", "instance", callee.target, reason="简单本地构造器的基础实例绑定",
                        metadata={"receiver": "simple_constructor", "constructor_execution_verified": False})
                return self._unknown("构造返回类型受 __new__/继承/元类影响，未推断", candidates=[callee.target])
            if callee.resolution == "external" and callee.external_symbol:
                return self._unknown("外部调用返回值的类型未推断")
            return self._unknown("函数/工厂调用返回值的类型未推断", candidates=callee.candidates)
        if isinstance(node, ast.IfExp):
            return self._combine([self.expression(node.body, scope, seen), self.expression(node.orelse, scope, seen)],
                                 "条件表达式具有多个潜在目标", force=True)
        if isinstance(node, ast.Constant):
            return _Ref("resolved", "value", reason="字面量不是已知调用目标")
        if isinstance(node, ast.NamedExpr):
            return self.expression(node.value, scope, seen)
        return self._unknown(f"{node.__class__.__name__} 动态调用目标未推断")

    def prepare_bases(self) -> None:
        for class_id, definitions in sorted(self.index.class_defs.items()):
            if len(definitions) != 1:
                self.index.uncertain_bases.add(class_id)
                continue
            definition = definitions[0]
            scope = self.index.expr_scopes[id(definition)]
            bases: list[str] = []
            for expression in definition.bases:
                try:
                    ref = self.expression(expression, scope)
                except RecursionError:
                    ref = self._unknown("继承符号解析超过递归预算")
                if ref.resolution == "resolved" and ref.kind == "class" and ref.target:
                    bases.append(ref.target)
                elif not (ref.resolution == "external" and ref.external_symbol == "builtins.object"):
                    self.index.uncertain_bases.add(class_id)
            if len(bases) > 1:
                self.index.uncertain_bases.add(class_id)
            self.index.class_bases[class_id] = bases

    def prepare_decorators(self) -> None:
        for node_id, definitions in self.index.symbol_decorators.items():
            node = self.index.nodes[node_id]
            if not any(decorators for decorators, _ in definitions):
                continue
            recognized: set[str] = set()
            all_recognized = node.kind != "class" and len(definitions) == 1 and len(definitions[0][0]) == 1
            for decorators, scope in definitions:
                for expression in decorators:
                    try:
                        ref = self.expression(expression, scope)
                    except RecursionError:
                        ref = self._unknown("装饰器身份解析超过递归预算")
                    if ref.resolution == "external" and ref.external_symbol in {"builtins.staticmethod", "builtins.classmethod"}:
                        recognized.add(ref.external_symbol)
                    else:
                        all_recognized = False
            node.metadata["decorated_binding"] = not all_recognized
            node.metadata["verified_builtin_decorators"] = sorted(recognized) if all_recognized else []
            for scope, first_parameter in self.index.method_parameters.get(node_id, []):
                # Replace only the initial parameter/receiver declaration. Later
                # assignments are independent writes and must remain visible.
                subsequent = scope.bindings.get(first_parameter, [])[1:]
                if all_recognized and "builtins.staticmethod" in recognized:
                    scope.bindings[first_parameter] = [_Binding("parameter", node.line,
                        reason="staticmethod 参数的运行时值未推断", scope=scope), *subsequent]
                elif all_recognized and "builtins.classmethod" in recognized:
                    scope.bindings[first_parameter] = [_Binding("receiver", node.line,
                        target=scope.class_id, scope=scope, metadata={"receiver": "class_parameter"}), *subsequent]
                elif not all_recognized:
                    # An arbitrary decorator can alter binding and method
                    # descriptor semantics, so don't invent a self/cls type.
                    scope.bindings[first_parameter] = [_Binding("parameter", node.line,
                        reason="未解析装饰器可能改变方法接收器绑定", scope=scope), *subsequent]

    def prepare_nonlocal_writes(self) -> None:
        for name, binding, origin in self.index.nonlocal_writes:
            enclosing = origin.parent
            while enclosing is not None:
                if enclosing.kind == "function" and name in enclosing.bindings:
                    enclosing.bindings[name].append(binding)
                    break
                enclosing = enclosing.parent
            else:
                origin.bindings.setdefault(name, []).append(binding)

    def prepare_attribute_writes(self) -> None:
        invalidations: set[tuple[str, str]] = set()
        unknown_names: set[str] = set()
        for target, scope in self.index.attribute_writes:
            try:
                receiver = self.expression(target.value, scope)
            except RecursionError:
                receiver = self._unknown("属性接收器解析深度预算耗尽")
            if receiver.resolution == "resolved" and receiver.kind in {"class", "instance"} and receiver.target:
                invalidations.add((receiver.target, target.attr))
            elif receiver.resolution == "resolved" and receiver.kind == "module":
                canonical = receiver.metadata.get("canonical_module", receiver.module)
                invalidations.add((str(canonical), target.attr))
            else:
                # The receiver may be any local class/module. Conservatively
                # invalidate this attribute name instead of guessing its type.
                unknown_names.add(target.attr)
        self.index.attribute_invalidations.update(invalidations)
        self.index.unknown_attribute_writes.update(unknown_names)

    def _callback_metadata(self, site: _CallSite, ref: _Ref) -> dict[str, Any]:
        if not isinstance(site.anchor, ast.Call) or site.implicit:
            return {}
        call = site.anchor
        candidates: set[str] = set()
        for argument in [*call.args, *[keyword.value for keyword in call.keywords]]:
            # Container-held callbacks are visible too; arbitrary factory return
            # values and receiver protocols are deliberately not inferred.
            pending = [argument]
            while pending:
                expression = pending.pop()
                if isinstance(expression, (ast.Tuple, ast.List, ast.Set)):
                    pending.extend(expression.elts)
                    continue
                if isinstance(expression, ast.Dict):
                    pending.extend(value for value in expression.values)
                    continue
                try:
                    argument_ref = self.expression(expression, site.scope)
                except RecursionError:
                    continue
                if argument_ref.resolution == "resolved" and argument_ref.kind in {"callable", "class"} and argument_ref.target:
                    candidates.add(argument_ref.target)
                candidates.update(candidate for candidate in argument_ref.candidates
                                  if candidate in self.index.nodes and self.index.nodes[candidate].kind != "module")
        metadata: dict[str, Any] = {}
        if candidates:
            metadata["callable_arguments"] = sorted(candidates)
        if ref.resolution == "external":
            # Installation/dependency code is outside this scan. It may invoke
            # local callbacks or framework registrations even without an explicit
            # function argument, so absence of a path cannot cross this boundary.
            if ref.metadata.get("external_kind") != "builtin":
                metadata["callbacks_unknown"] = True
                metadata["callback_boundary_reason"] = "外部实现未扫描，是否重新进入本地代码未知"
            else:
                higher_order = {"builtins.map", "builtins.filter", "builtins.sorted", "builtins.min", "builtins.max", "builtins.iter"}
                if candidates or ref.external_symbol in higher_order:
                    callback_inputs = list(call.args[:1]) if ref.external_symbol in {"builtins.map", "builtins.filter"} else []
                    callback_inputs += [keyword.value for keyword in call.keywords if keyword.arg == "key"]
                    if ref.external_symbol == "builtins.iter" and len(call.args) > 1:
                        callback_inputs += list(call.args[:1])
                    metadata["callbacks_unknown"] = bool(candidates or any(not isinstance(value, ast.Constant) for value in callback_inputs))
                    if metadata["callbacks_unknown"]:
                        metadata["callback_boundary_reason"] = "builtin 高阶调用的回调执行未展开"
        return metadata

    def edges(self) -> list[Edge]:
        edges: list[Edge] = []
        duplicate_owners = [node for node in self.index.nodes.values() if node.metadata.get("duplicate_definition")]
        decorated_owners = [node for node in self.index.nodes.values() if node.metadata.get("decorated_binding")]
        for site in self.index.calls:
            source_owner = site.scope.call_owner or site.scope.owner
            try:
                ref = self.expression(site.func, site.scope)
            except RecursionError:
                ref = self._unknown("静态表达式解析深度预算耗尽")
            if ref.resolution == "resolved" and ref.kind not in {"callable", "class"}:
                ref = self._unknown("目标是已知模块/普通值，未解析为 callable", "unresolved",
                                    [ref.target] if ref.target else ref.candidates)
            if ref.resolution == "external" and ref.external_symbol in {"builtins." + name for name in _REFLECTIVE_BUILTINS}:
                ref = self._unknown("反射/动态绑定操作的调用结构无法静态展开")
            line, column = getattr(site.anchor, "lineno", 0), getattr(site.anchor, "col_offset", 0)
            expression = _text(site.func)
            identity = [source_owner, site.scope.module.source.path, line, column,
                        getattr(site.anchor, "end_lineno", line), getattr(site.anchor, "end_col_offset", column), site.implicit]
            metadata = {**ref.metadata, "callee_kind": ref.kind,
                        "external_symbol": ref.external_symbol or None,
                        "static_only": True, "execution_order_verified": False,
                        "lexical_scope": site.scope.owner}
            metadata.update(self._callback_metadata(site, ref))
            ambiguous_owners = [node for node in duplicate_owners
                if (node.id == source_owner or source_owner.startswith(node.id + ".")
                 or (node.kind == "module" and node.module == site.scope.module.name))]
            decorated_ancestors = [node for node in decorated_owners if node.id == source_owner or source_owner.startswith(node.id + ".")]
            if ambiguous_owners or decorated_ancestors:
                if ref.target:
                    ref.candidates = sorted(set([*ref.candidates, ref.target]))
                ref.target = None
                ref.resolution = "ambiguous" if ambiguous_owners else "dynamic"
                ref.reason = "源符号/祖先存在多个实现，无法确认所属调用" if ambiguous_owners else "源符号的装饰器绑定未解析，原始函数体不等于最终可调用对象"
                metadata["source_ambiguous"] = True
                metadata["source_definitions"] = [
                    {"node_id": owner.id, "definitions": owner.metadata.get("definitions", [])}
                    for owner in ambiguous_owners]
                if decorated_ancestors:
                    metadata["source_decorated_ancestors"] = [node.id for node in decorated_ancestors]
            if site.implicit:
                metadata["implicit"] = site.implicit
            if ref.kind == "class" and ref.resolution == "resolved" and ref.target:
                self.index.constructed_classes.add(ref.target)
                metadata["constructor_dispatch_expanded"] = False
            if metadata.get("receiver_model") or ref.kind == "class":
                metadata["assumptions"] = ["无运行时 monkey patch/对象重绑", "按当前可见类声明解析，执行未经验证"]
            edges.append(Edge(_digest(identity)[:24], source_owner,
                ref.target if ref.resolution == "resolved" else None, expression,
                site.scope.module.source.path, line, column, ref.resolution,
                sorted(set(ref.candidates)), ref.reason, metadata))
        # Binding the class object does not prove how __call__/__new__/__init__
        # execute. Retain a reachable gap instead of inventing initializer edges.
        # A class may also be selected directly as a configured entrypoint, even
        # if no explicit constructor call appears in the scanned sources.
        for class_id in sorted(node.id for node in self.index.nodes.values() if node.kind == "class"):
            node = self.index.nodes[class_id]
            candidates = [class_id + "." + name for name in ("__new__", "__init__")
                          if class_id + "." + name in self.index.nodes]
            edges.append(Edge(_digest([class_id, "constructor_dispatch"])[:24], class_id, None,
                "<constructor dispatch>", node.file, node.line, resolution="dynamic",
                candidates=candidates, reason="仅绑定到类对象；初始化和构造分派未展开",
                metadata={"implicit": "constructor_dispatch", "static_only": True}))
        return sorted(edges, key=lambda edge: (edge.file, edge.line, edge.column, edge.id))


def _excluded(relative: str, patterns: list[str], *, directory: bool = False) -> bool:
    parts = relative.split("/")
    if directory and parts[-1] in _IGNORED_DIRS:
        return True
    for raw in patterns:
        pattern = raw.replace("\\", "/").rstrip("/")
        if "/" not in pattern and any(fnmatch.fnmatchcase(part, pattern) for part in parts):
            return True
        prefixes = ["/".join(parts[:i]) for i in range(1, len(parts) + 1)]
        if any(fnmatch.fnmatchcase(prefix, pattern) or fnmatch.fnmatchcase(prefix + "/", pattern) for prefix in prefixes):
            return True
        if pattern.startswith("**/") and fnmatch.fnmatchcase(relative, pattern[3:]):
            return True
    return False


def _source_roots(root: Path, configured: list[str]) -> list[Path]:
    roots: list[Path] = []
    for name in configured:
        lexical = Path(name)
        if lexical.is_absolute() or ".." in lexical.parts:
            raise ValueError("source_roots 必须位于项目根内")
        source = root / lexical
        cursor = root
        for component in lexical.parts:
            if component == ".":
                continue
            cursor /= component
            if cursor.is_symlink():
                raise ValueError(f"source_roots 不能包含符号链接：{name}")
        resolved = source.resolve()
        if not resolved.is_relative_to(root):
            raise ValueError(f"source_roots 逃逸项目根：{name}")
        if not resolved.is_dir():
            raise ValueError(f"source_roots 不存在或不是目录：{name}")
        if resolved not in roots:
            roots.append(resolved)
    return sorted(roots, key=lambda path: (len(path.parts), str(path)))


def _secure_bytes(root: Path, relative: str, maximum: int) -> tuple[bytes | None, str, int]:
    """Open every component without following a link, then stream its hash."""
    directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    file_flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    opened: list[int] = []
    try:
        directory_fd = os.open(root, directory_flags)
        opened.append(directory_fd)
        parts = relative.split("/")
        for component in parts[:-1]:
            directory_fd = os.open(component, directory_flags, dir_fd=directory_fd)
            opened.append(directory_fd)
        file_fd = os.open(parts[-1], file_flags, dir_fd=directory_fd)
        opened.append(file_fd)
        before = os.fstat(file_fd)
        if not stat.S_ISREG(before.st_mode):
            raise OSError("源码目标不是普通文件")
        digest = hashlib.sha256()
        chunks: list[bytes] = []
        size = 0
        while True:
            chunk = os.read(file_fd, 65536)
            if not chunk:
                break
            digest.update(chunk)
            size += len(chunk)
            if size <= maximum:
                chunks.append(chunk)
            else:
                chunks.clear()
        after = os.fstat(file_fd)
        if (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (after.st_size, after.st_mtime_ns, after.st_ctime_ns):
            raise OSError("读取期间源码发生变化；请重新扫描")
        return b"".join(chunks) if size <= maximum else None, digest.hexdigest(), size
    finally:
        for descriptor in reversed(opened):
            os.close(descriptor)


def _open_directory(root: Path, relative: str) -> int:
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    current = os.open(root, flags)
    try:
        for component in Path(relative).parts:
            if component == ".":
                continue
            child = os.open(component, flags, dir_fd=current)
            os.close(current)
            current = child
        return current
    except BaseException:
        os.close(current)
        raise


def _module_name(path: Path, source_root: Path, package_root: bool) -> str:
    relative = path.relative_to(source_root)
    parts = list(relative.with_suffix("").parts)
    if parts[-1] == "__init__":
        parts.pop()
    if package_root:
        parts.insert(0, source_root.name)
    return ".".join(parts) or "__root__"


def _importable_path(path: Path, source_root: Path, package_root: bool) -> bool:
    parts = list(path.relative_to(source_root).with_suffix("").parts)
    if parts[-1] == "__init__":
        parts.pop()
    if package_root:
        parts.insert(0, source_root.name)
    return bool(parts) and all(part.isidentifier() for part in parts)


def _scan(root: Path, config: dict[str, Any], diagnostics: list[Diagnostic]) -> tuple[list[_Module], bool, dict[str, Any]]:
    source_roots = _source_roots(root, config["analysis"]["source_roots"])
    patterns = config["analysis"]["exclude"]
    maximum = config["analysis"]["max_file_bytes"]
    candidates: dict[str, set[Path]] = {}
    omitted_links: set[str] = set()
    scan_errors: list[str] = []
    excluded_paths: set[str] = set()
    stubs: set[str] = set()
    package_roots: dict[Path, bool] = {}
    for source in source_roots:
        source_relative = source.relative_to(root).as_posix()
        if source_relative != "." and _excluded(source_relative, patterns, directory=True):
            diagnostics.append(Diagnostic("warning", "excluded_source_root", f"源码根 {source_relative} 被排除规则跳过。"))
            scan_errors.append(source_relative)
            continue
        # fd-relative traversal prevents a directory swapped for a symlink from
        # causing even the scanner to enumerate paths outside the project root.
        try:
            source_fd = _open_directory(root, source_relative)
        except OSError as error:
            scan_errors.append(source_relative)
            diagnostics.append(Diagnostic("warning", "scan_error", f"无法打开源码根：{error}", source_relative))
            continue
        try:
            try:
                init_status = os.stat("__init__.py", dir_fd=source_fd, follow_symlinks=False)
                package_roots[source] = stat.S_ISREG(init_status.st_mode)
            except FileNotFoundError:
                package_roots[source] = False
            pending: list[tuple[int, str]] = [(source_fd, source_relative)]
            source_fd = -1  # pending now owns the descriptor
            flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
            try:
                while pending:
                    directory_fd, directory_relative = pending.pop()
                    try:
                        with os.scandir(directory_fd) as iterator:
                            entries = sorted(iterator, key=lambda entry: entry.name)
                        for entry in entries:
                            relative = entry.name if directory_relative == "." else directory_relative + "/" + entry.name
                            suffix = Path(entry.name).suffix
                            try:
                                if entry.name in _IGNORED_DIRS:
                                    excluded_paths.add(relative)
                                    continue
                                if entry.is_symlink():
                                    if suffix in {".py", ".pyi"} or not _excluded(relative, patterns):
                                        omitted_links.add(relative)
                                    continue
                                is_directory = entry.is_dir(follow_symlinks=False)
                                if _excluded(relative, patterns, directory=is_directory):
                                    if is_directory or suffix in {".py", ".pyi"}:
                                        excluded_paths.add(relative)
                                    continue
                                if is_directory:
                                    child = os.open(entry.name, flags, dir_fd=directory_fd)
                                    pending.append((child, relative))
                                elif suffix == ".pyi":
                                    stubs.add(relative)
                                elif suffix == ".py":
                                    candidates.setdefault(relative, set()).add(source)
                            except OSError as error:
                                scan_errors.append(relative)
                                diagnostics.append(Diagnostic("warning", "scan_error", f"无法读取源码条目：{error}", relative))
                    except OSError as error:
                        scan_errors.append(directory_relative)
                        diagnostics.append(Diagnostic("warning", "scan_error", f"无法枚举源码目录：{error}", directory_relative))
                    finally:
                        os.close(directory_fd)
            finally:
                for descriptor, _ in pending:
                    os.close(descriptor)
        except OSError as error:
            scan_errors.append(source_relative)
            diagnostics.append(Diagnostic("warning", "scan_error", f"无法检查源码根：{error}", source_relative))
        finally:
            if source_fd >= 0:
                os.close(source_fd)
    for relative in sorted(omitted_links):
        diagnostics.append(Diagnostic("warning", "symlink_skipped", "不读取符号链接源码或目录；该区域未分析。", relative))
    for relative in sorted(stubs):
        diagnostics.append(Diagnostic("info", "stub_not_implementation", ".pyi 仅为类型声明，本版不把它当作运行时实现。", relative))
    modules: list[_Module] = []
    failed = False
    for relative, applicable in sorted(candidates.items()):
        path = root / relative
        # A file visible through several import roots has one canonical identity,
        # but all import spellings are retained for name resolution.
        canonical = max(applicable, key=lambda item: (len(item.parts), str(item)))
        aliases = sorted({_module_name(path, source, package_roots[source]) for source in applicable})
        importable_aliases = sorted({_module_name(path, source, package_roots[source]) for source in applicable
                                    if _importable_path(path, source, package_roots[source])})
        name = _module_name(path, canonical, package_roots[canonical])
        source = SourceFile(relative, "", "", "read_error", module=name)
        tree: ast.Module | None = None
        error_line = 0
        try:
            raw, source.hash, size = _secure_bytes(root, relative, maximum)
            if raw is None:
                source.status = "too_large"
                source.error = f"文件 {size} 字节，超过静态解析上限 {maximum}；内容未解析。"
            else:
                encoding, _ = tokenize.detect_encoding(io.BytesIO(raw).readline)
                source.content = raw.decode(encoding)
                try:
                    tree = ast.parse(source.content, filename=relative, type_comments=True)
                    source.status = "parsed"
                except (SyntaxError, ValueError, RecursionError) as error:
                    source.status = "syntax_error"
                    source.error = str(error)
                    error_line = getattr(error, "lineno", 0) or 0
        except (UnicodeError, LookupError, SyntaxError) as error:
            source.status = "encoding_error"
            source.error = str(error)
        except OSError as error:
            source.error = str(error)
        if source.status != "parsed":
            failed = True
            diagnostics.append(Diagnostic("warning", source.status, source.error or "源码未解析", relative,
                error_line))
        if name not in importable_aliases:
            diagnostics.append(Diagnostic("warning", "nonimportable_module_name",
                f"模块名 {name} 不是标准 Python 导入名；脚本内调用仍可分析。", relative))
        is_package = path.name == "__init__.py"
        package = name if is_package else name.rpartition(".")[0]
        module = _Module(name, source, tree, package, is_package, aliases, importable_aliases)
        if tree:
            module.future_annotations = any(isinstance(statement, ast.ImportFrom) and statement.module == "__future__"
                and any(alias.name == "annotations" for alias in statement.names) for statement in tree.body)
        modules.append(module)
    stats = {"source_roots": [source.relative_to(root).as_posix() for source in source_roots],
             "excluded_paths": sorted(excluded_paths), "symlinks_skipped": sorted(omitted_links),
             "stubs_not_analyzed": sorted(stubs), "scan_errors": sorted(set(scan_errors))}
    # Intentional exclusions define the scope. Unreadable inputs, symlinks and
    # stub-only implementation declarations are explicit coverage gaps.
    return modules, failed or bool(omitted_links or scan_errors or stubs), stats


def _captured_modules(root: Path, config: dict[str, Any], files: list[SourceFile], diagnostics: list[Diagnostic]):
    """Parse exactly the immutable Python input set, without rereading files."""
    roots = [root / Path(relative) for relative in config["analysis"]["source_roots"]]
    paths = {source.path for source in files}
    package_roots = {source_root: (source_root.relative_to(root) / "__init__.py").as_posix() in paths for source_root in roots}
    modules = []
    incomplete = False
    for captured in sorted(files, key=lambda source: source.path):
        path = root / captured.path
        applicable = [source_root for source_root in roots if path.is_relative_to(source_root)]
        if not applicable:
            incomplete = True
            diagnostics.append(Diagnostic("warning", "source_root_mismatch", "捕获的源码不在声明根目录中", captured.path))
            continue
        canonical = max(applicable, key=lambda source_root: (len(source_root.parts), str(source_root)))
        aliases = sorted({_module_name(path, source_root, package_roots[source_root]) for source_root in applicable})
        importable = sorted({_module_name(path, source_root, package_roots[source_root]) for source_root in applicable
                             if _importable_path(path, source_root, package_roots[source_root])})
        name = _module_name(path, canonical, package_roots[canonical])
        source = replace(captured, module=name)
        tree = None
        if source.status == "captured":
            try:
                tree = ast.parse(source.content, filename=source.path, type_comments=True)
                source = replace(source, status="parsed", error=None)
            except (SyntaxError, ValueError, RecursionError) as exc:
                source = replace(source, status="syntax_error", error=str(exc))
                diagnostics.append(Diagnostic("warning", "syntax_error", str(exc), source.path, getattr(exc, "lineno", 0) or 0))
        if source.status != "parsed":
            incomplete = True
        if name not in importable:
            diagnostics.append(Diagnostic("warning", "nonimportable_module_name", f"模块名 {name} 不是标准 Python 导入名", source.path))
        is_package = path.name == "__init__.py"
        module = _Module(name, source, tree, name if is_package else name.rpartition(".")[0], is_package, aliases, importable)
        if tree:
            module.future_annotations = any(isinstance(statement, ast.ImportFrom) and statement.module == "__future__"
                                           and any(alias.name == "annotations" for alias in statement.names) for statement in tree.body)
        modules.append(module)
    return modules, incomplete, {"source_roots": config["analysis"]["source_roots"], "excluded_paths": [],
                                  "symlinks_skipped": [], "scan_errors": [], "stubs_not_analyzed": []}


def _apply_policy(index: _Index) -> None:
    for node in index.nodes.values():
        matched = [name for name, patterns in index.config["layers"].items()
                   if any(fnmatch.fnmatchcase(value, pattern) for pattern in patterns
                          for value in (node.id, node.qualname, node.module))]
        if len(matched) == 1:
            node.layer = matched[0]
        elif matched:
            node.metadata["candidate_layers"] = sorted(matched)
            index.diagnostics.append(Diagnostic("warning", "layer_ambiguous",
                f"节点 {node.id} 同时匹配多个层：{', '.join(sorted(matched))}", node.file, node.line))
        if any(fnmatch.fnmatchcase(value, pattern) for pattern in index.config["entrypoints"]
               for value in (node.id, node.qualname)):
            node.metadata["entrypoint"] = True


def analyze_python_project(root: str | Path, config: dict[str, Any] | None = None, *, captured_files: list[SourceFile] | None = None) -> GraphSnapshot:
    """Return an immutable-evidence snapshot without executing any target code.

    Configuration/source-root errors raise ``ValueError``. Individual unreadable,
    oversized or invalid Python files produce a partial snapshot with coverage
    diagnostics, rather than disappearing from the analysis.
    """
    lexical_root = Path(root).expanduser().absolute()
    if lexical_root.is_symlink():
        raise ValueError("项目根不能是符号链接")
    project_root = lexical_root.resolve()
    if not project_root.is_dir():
        raise ValueError(f"项目根不存在或不是目录：{project_root}")
    policy = deepcopy(load_config(project_root) if config is None else validate_config(config))
    diagnostics: list[Diagnostic] = []
    modules, coverage_incomplete, scan_stats = (_scan(project_root, policy, diagnostics) if captured_files is None
                                              else _captured_modules(project_root, policy, captured_files, diagnostics))
    index = _Index(policy, diagnostics)
    index.coverage_incomplete = coverage_incomplete
    for module in modules:
        index.register_module(module)
    index.finalize_module_registry()
    for module in modules:
        if module.tree is not None:
            try:
                _Collector(index, module).visit(module.tree)
            except RecursionError:
                index.coverage_incomplete = True
                diagnostics.append(Diagnostic("warning", "ast_depth_limit",
                    "AST 遍历超过递归预算；该文件仅部分提取。", module.source.path))
    resolver = _Resolver(index)
    resolver.prepare_nonlocal_writes()
    resolver.prepare_decorators()
    resolver.prepare_bases()
    resolver.prepare_attribute_writes()
    edges = resolver.edges()
    _apply_policy(index)
    files = sorted((module.source for module in modules), key=lambda source: source.path)
    counts = Counter(edge.resolution for edge in edges)
    ambiguous_symbols = sum(bool(node.metadata.get("duplicate_definition")) for node in index.nodes.values())
    callback_boundaries = sum(edge.resolution == "external" and bool(edge.metadata.get("callbacks_unknown") or edge.metadata.get("callable_arguments")) for edge in edges)
    call_incomplete = any(counts[value] for value in ("dynamic", "ambiguous", "unresolved")) or bool(callback_boundaries or ambiguous_symbols)
    incomplete = index.coverage_incomplete or call_incomplete
    if not files:
        incomplete = index.coverage_incomplete = True
        diagnostics.append(Diagnostic("warning", "no_python_sources", "扫描范围中没有 Python 实现文件，不能认为项目已完整分析。"))
    nodes = sorted(index.nodes.values(), key=lambda node: node.id)
    diagnostics.sort(key=lambda item: (item.file, item.line, item.code, item.message))
    source_hash = _digest({"files": [(source.path, source.hash, source.status, source.module, source.error) for source in files],
        "coverage": scan_stats, "collisions": [item.message for item in diagnostics if item.code == "module_collision"]})
    policy_hash = _digest(policy)
    project_id = project_id_for(project_root)
    snapshot_id = _digest({"project_id": project_id, "source_hash": source_hash, "policy_hash": policy_hash,
        "schema_version": SCHEMA_VERSION, "analyzer_version": ANALYZER_VERSION,
        "detector_version": DETECTOR_VERSION, "parser_version": PARSER_VERSION})
    stats = {**scan_stats, "files_total": len(files), "files_parsed": sum(source.status == "parsed" for source in files),
        "files_failed": sum(source.status != "parsed" for source in files), "nodes": len(nodes), "edges": len(edges),
        "resolved_calls": counts["resolved"], "external_calls": counts["external"],
        "dynamic_calls": counts["dynamic"], "ambiguous_calls": counts["ambiguous"], "unresolved_calls": counts["unresolved"],
        "external_callback_boundaries": callback_boundaries, "parser_version": PARSER_VERSION,
        "ambiguous_symbols": ambiguous_symbols,
        "attribute_invalidations": sorted([list(item) for item in index.attribute_invalidations]),
        "unknown_attribute_writes": sorted(index.unknown_attribute_writes),
        "coverage_incomplete": index.coverage_incomplete, "call_resolution_incomplete": call_incomplete,
        "incomplete": incomplete, "resolution_model": "static lexical binding; no runtime execution",
        "limitations": ["不证明分支可执行、调用顺序、返回值或业务结果", "不执行代码/测试/构建，不验证外部依赖可用性",
            "回调、反射、工厂返回值、对象字段及复杂继承保留未知", "静态绑定不涵盖任意 monkey patch 和运行时模块替换",
            "构造器内部调用保持未知，不推断初始化路径"]}
    return GraphSnapshot(snapshot_id, project_id, policy["project"].get("name") or project_root.name,
        str(project_root), datetime.now(timezone.utc).isoformat(), source_hash, ANALYZER_VERSION,
        policy_hash, "partial" if incomplete else "complete", nodes, edges, files, diagnostics, stats, policy)


def analyze_project(root: str | Path, config: dict[str, Any] | None = None, *, frontend_runner=None) -> GraphSnapshot:
    """Stable public entry point with explicit language dispatch and coverage."""
    from .analysis import analyze_project as dispatch
    return dispatch(root, config, frontend_runner=frontend_runner)
