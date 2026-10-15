"""Finite static port assembly from authenticated snapshot source.

This module does not import a target, execute an event, create CALLS edges or
infer arbitrary factory values. A data-only locator selects a boot call, an
injection call and a returned consumer method. All keys, guards, declarations
and branch results are derived from the selected CST and lexical identities.
Unsupported aliases, writes, escape or shape retain an explicit gap.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import posixpath
from pathlib import PurePosixPath
from typing import Any

from .models import GraphSnapshot
from .semantic_sources import SEMANTIC_SOURCE_VERSION, SemanticSources, unwrap, walk
from .semantic_environment import BuiltinEnvironment, VERSION as ENVIRONMENT_VERSION
from .completion_summaries import function_kind, completion_relation, VERSION as COMPLETION_VERSION
from .static_contracts import _literal_string


VERSION = "finite-port-wiring-2-shared"
LITERAL_IMPORT_MODEL = "literal-promise-all-destructuring-assembly-1"
OBJECT_MODEL = "ordinary-static-object-and-freeze-assembly-1"
BRANCH_MODEL = "closed-object-undefined-ternary-assembly-1"
ALIAS_MODEL = "unique-const-property-port-capture-1"
_FUNCTIONS = frozenset({"function_declaration", "generator_function_declaration",
    "function_expression", "generator_function", "arrow_function", "method_definition"})
_NODE_GAPS = frozenset({"duplicate_definition", "multiple_module_contexts",
    "conditional_definition", "attribute_macros_unknown", "declaration_only",
    "binding_uncertain", "module_identity_collision"})
_EXTENSIONS = (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".mts", ".cts", ".xsjs", ".xsjslib")
_OBJECT_PROTOTYPE_KEYS = frozenset({"constructor", "toString", "toLocaleString", "valueOf",
    "hasOwnProperty", "isPrototypeOf", "propertyIsEnumerable", "__proto__", "__defineGetter__",
    "__defineSetter__", "__lookupGetter__", "__lookupSetter__"})


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True,
        separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()


def _field(node: Any, name: str) -> Any:
    return node.child_by_field_name(name) if node is not None else None


def _children(node: Any) -> list[Any]:
    return [child for child in node.named_children if child.type != "comment"] if node is not None else []


def _function(definition: Any) -> Any:
    return unwrap(definition.value) if definition.value is not None else definition.node


def _arguments(call: Any) -> list[Any]:
    return _children(_field(call, "arguments"))


def _const(declaration: Any) -> bool:
    parent = declaration.parent if declaration is not None else None
    return parent is not None and parent.type == "lexical_declaration" and any(
        child.type == "const" for child in parent.children)


def _name(document: Any, node: Any) -> str | None:
    if node is None:
        return None
    raw = document.text(node)
    if node.type in {"identifier", "property_identifier", "shorthand_property_identifier",
                     "shorthand_property_identifier_pattern"}:
        return raw if raw and "\\" not in raw else None
    return _literal_string(raw) if node.type == "string" else None


def _member(document: Any, node: Any) -> tuple[Any, str | None]:
    node = unwrap(node)
    if node is None or node.type not in {"member_expression", "subscript_expression"}:
        return None, None
    key = _field(node, "property") if node.type == "member_expression" else _field(node, "index")
    if node.type == "subscript_expression" and (key is None or key.type != "string"):
        return _field(node, "object"), None
    return unwrap(_field(node, "object")), _name(document, key)


def _path(value: Any) -> bool:
    return isinstance(value, str) and bool(value) and not value.startswith("/") and "\\" not in value and "\x00" not in value and all(
        part not in {"", ".", ".."} for part in value.split("/"))


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and "\x00" not in value


def _index(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= 32


def _validate(rule: Any) -> None:
    if not isinstance(rule, dict):
        raise ValueError("导航合同必须是数据对象。")
    json.dumps(rule, allow_nan=False)
    wiring = rule.get("wiring")
    if not isinstance(wiring, dict) or set(wiring) != {"boot", "injection", "use"}:
        raise ValueError("wiring 仅接受 boot、injection、use 三段来源选择器。")
    schemas = {
        "boot": {"file", "callee", "argument_index"},
        "injection": {"file", "symbol", "callee", "argument_index", "property"},
        "use": {"file", "symbol", "parameter_index", "property", "returned_method", "method"},
    }
    for stage, keys in schemas.items():
        selector = wiring.get(stage)
        if not isinstance(selector, dict) or set(selector) != keys or not _path(selector.get("file")):
            raise ValueError(f"wiring.{stage} 有未知字段或没有规范项目内 file。")
        for key in keys - {"file", "argument_index", "parameter_index"}:
            if not _text(selector.get(key)):
                raise ValueError(f"wiring.{stage}.{key} 必须是非空静态来源名称。")
        for key in keys & {"argument_index", "parameter_index"}:
            if not _index(selector.get(key)):
                raise ValueError(f"wiring.{stage}.{key} 必须是有限参数位次。")
    consumer = rule.get("consumer")
    if not isinstance(consumer, dict) or not _path(consumer.get("file")) or not all(
        _text(consumer.get(key)) for key in ("symbol", "factory_callee", "returned_method")):
        raise ValueError("导航 consumer 需要 exact file/symbol/factory_callee/returned_method。")


class _Context:
    def __init__(self, snapshot: GraphSnapshot, rule: dict):
        self.snapshot, self.rule = snapshot, rule
        self.sources = SemanticSources(snapshot)
        self.lexical: dict[str, Any] = {}
        self.environments: dict[str, BuiltinEnvironment] = {}
        self.facts: list[dict] = []
        self.models: list[dict] = []
        self.gaps: list[dict] = []
        self.segments: dict[str, dict] = {}
        self.consumer_factory: dict | None = None

    def bindings(self, document: Any) -> Any:
        from .lexical_bindings import LexicalBindings
        if document.source.path not in self.lexical:
            self.lexical[document.source.path] = LexicalBindings(document)
        return self.lexical[document.source.path]

    def environment(self, document: Any) -> BuiltinEnvironment:
        if document.source.path not in self.environments:
            self.environments[document.source.path] = BuiltinEnvironment(document)
        return self.environments[document.source.path]

    def gap(self, stage: str, code: str, message: str, document: Any = None,
            node: Any = None, necessary: bool = True, **details: Any) -> dict:
        location = document.location(node) if document is not None and node is not None else None
        value = {"segment": stage, "code": code, "message": message,
            "necessary_for_assembly": necessary, "location": location, **details}
        value["id"] = "port-gap:" + _digest(value)[:24]
        if not any(item["id"] == value["id"] for item in self.gaps):
            self.gaps.append(value)
        return value

    def problems(self, stage: str, problems: list[dict]) -> None:
        for problem in problems:
            self.gap(stage, "semantic_" + problem.get("code", "unknown"), problem.get("message", "源码不完整。"),
                source_problem=deepcopy(problem))

    def fact(self, operation: str, document: Any, nodes: list[Any], observed: dict,
             inputs: list[str] | None = None) -> str:
        value = {"operation": operation, "owner": document.source.path,
            "locations": [document.location(node) for node in nodes if node is not None],
            "inputs": list(inputs or []), "observed": observed,
            "snapshot_id": self.snapshot.id, "semantic_source_version": SEMANTIC_SOURCE_VERSION}
        value["id"] = "port-fact:" + _digest(value)[:24]
        if not any(item["id"] == value["id"] for item in self.facts):
            self.facts.append(value)
        return value["id"]

    def model(self, model: str, operation: str, facts: list[str], **observed: Any) -> str:
        value = {"model": model, "operation": operation, "input_fact_ids": facts,
            "observed": observed, "target_executed": False,
            "runtime_environment_verified": False}
        value["id"] = "port-model:" + _digest(value)[:24]
        if not any(item["id"] == value["id"] for item in self.models):
            self.models.append(value)
        return value["id"]

    def segment(self, stage: str, state: str, fact_ids: list[str], **observed: Any) -> None:
        self.segments[stage] = {"state": state, "fact_ids": fact_ids, "observed": observed,
            "gap_ids": [item["id"] for item in self.gaps if item["segment"] == stage]}

    def record(self, stage: str, document: Any, identifier: Any) -> dict | None:
        if identifier is None or identifier.type not in {"identifier", "shorthand_property_identifier"} or _name(document, identifier) is None:
            self.gap(stage, "identifier_shape_unknown", "声明/捕获只支持未转义的简单值标识符。", document, identifier)
            return None
        record = self.bindings(document).resolve(identifier)
        if record.get("state") != "unique" or not record.get("identity_complete"):
            self.gap(stage, "lexical_identity_unknown", "词法声明身份没有唯一闭合；不按同名匹配。", document, identifier,
                lexical_result=deepcopy(record))
            return None
        if self.bindings(document).writes(record):
            self.gap(stage, "binding_written", "该声明有赋值/更新来源，不将捕获值视为稳定。", document, identifier,
                writes=deepcopy(self.bindings(document).writes(record)))
            return None
        return record

    def same(self, document: Any, first: dict, second: dict) -> bool:
        return bool(self.bindings(document).same(first, second))


def _definition(ctx: _Context, stage: str, selector: dict) -> tuple[Any, Any]:
    document, definition, problems = ctx.sources.select({"file": selector["file"], "symbol": selector["symbol"]})
    if definition is None:
        ctx.problems(stage, problems)
        return document, None
    function = _function(definition)
    if not definition.callable or function is None or function.type not in _FUNCTIONS:
        ctx.gap(stage, "owner_not_function", "选择器不是唯一具体函数/方法实现。", document, definition.node)
        return document, None
    kind = function_kind(document, function)
    if kind.get("kind") not in {"ordinary_sync", "ordinary_async"}:
        ctx.gap(stage, "generator_body_activation_not_modeled", "共享调用种类没有普通 body 装配模型；生成器迭代激活或未知种类均保留缺口。", document, function,
            function_kind=kind)
        return document, None
    graph_nodes = ctx.sources.nodes.get(getattr(definition, "graph_node_id", ""), [])
    if len(graph_nodes) != 1:
        ctx.gap(stage, "selected_owner_graph_not_unique", "装配 owner 不是唯一捕获图声明；CST quote 不替代 graph 身份。", document, function)
        return document, None
    authenticated_document, authenticated_definition, graph_problems = ctx.sources.definition_for_node(graph_nodes[0])
    if authenticated_document is not document or authenticated_definition is not definition or graph_problems:
        ctx.problems(stage, graph_problems)
        ctx.gap(stage, "selected_owner_graph_gap", "装配 owner 有图声明 gap/重绑定，不绕过为独立装配来源。", document, function)
        return document, None
    return document, definition


def _calls(document: Any, definition: Any, callee: str) -> list[Any]:
    root = _field(_function(definition), "body") if definition is not None else document.tree.root_node
    return [node for node in walk(root, skip_functions=True) if node.type == "call_expression"
        and document.text(_field(node, "function")) == callee]


def _parameter(ctx: _Context, stage: str, document: Any, definition: Any, index: int) -> tuple[Any, dict | None]:
    function = _function(definition)
    parameters = _children(_field(function, "parameters"))
    if len(parameters) <= index:
        ctx.gap(stage, "formal_parameter_missing", "实际函数没有配置位次的形参。", document, function, parameter_index=index)
        return None, None
    parameter = parameters[index]
    identifier = _field(parameter, "pattern") or _field(parameter, "name") if parameter.type in {"required_parameter", "optional_parameter"} else parameter
    if parameter.type == "optional_parameter" or _field(parameter, "value") is not None:
        ctx.gap(stage, "formal_parameter_default_unknown", "默认或可选形参的装配语义未建模。", document, parameter)
        return None, None
    return identifier, ctx.record(stage, document, identifier)


def _properties(ctx: _Context, stage: str, document: Any, obj: Any, data_only: bool = False) -> dict | None:
    obj = unwrap(obj)
    if obj is None or obj.type != "object":
        ctx.gap(stage, "object_not_literal", "装配实参/返回值不是封闭字面对象。", document, obj)
        return None
    members = {}
    for node in _children(obj):
        if node.type == "pair":
            key = _name(document, _field(node, "key"))
            value = _field(node, "value")
            member_kind = "data"
        elif node.type == "shorthand_property_identifier":
            key, value, member_kind = _name(document, node), node, "data"
        elif node.type == "method_definition" and not data_only:
            key, value = _name(document, _field(node, "name")), node
            member_kind = "getter" if any(child.type == "get" for child in node.children) else (
                "setter" if any(child.type == "set" for child in node.children) else "method")
        else:
            ctx.gap(stage, "object_property_shape_unknown", "spread、computed、访问器实参或未知字段形状不能构成封闭装配对象。", document, node)
            return None
        if key is None or key == "__proto__" or key in members:
            ctx.gap(stage, "object_key_not_unique", "对象键转义/计算、特殊原型键或重复声明，拒绝字段身份负证。", document, node)
            return None
        members[key] = {"node": node, "value": value, "kind": member_kind}
    return members


def _global_name_safe(ctx: _Context, stage: str, document: Any, at: Any, name: str, member: str) -> bool:
    audit = ctx.environment(document).audit(name, at, member or None)
    if audit.get("supported") is not True:
        ctx.gap(stage, "builtin_environment_not_closed", "公共内建环境审计未闭合所需标准模型。", document, at,
            global_name=name, environment_audit=audit)
        return False
    ctx.fact("standard_name_local_absence_and_visible_mutation_audit", document, [at], {
        "standard_name": name, "standard_member": member,
        "local_declaration_absent": audit.get("lexical_absence", {}).get("local_declaration_absent"),
        "semantic_environment_version": ENVIRONMENT_VERSION, "environment_audit": audit,
        "visible_mutation_and_alias_audit_scope": audit.get("source", {}).get("audit_scope"),
        "runtime_builtin_verified": False, "standard_environment_is_model_assumption": True})
    return True


def _builtin(ctx: _Context, stage: str, document: Any, identifier: Any, member: str) -> bool:
    if identifier is None or identifier.type != "identifier" or _name(document, identifier) is None:
        ctx.gap(stage, "builtin_receiver_unknown", "内建模型 receiver 不是简单未转义标识符。", document, identifier)
        return False
    return _global_name_safe(ctx, stage, document, identifier, document.text(identifier), member)


def _returned(ctx: _Context, stage: str, document: Any, definition: Any, property_name: str) -> tuple[Any, dict | None, bool]:
    function = _function(definition)
    kind = function_kind(document, function)
    if kind.get("kind") not in {"ordinary_sync", "ordinary_async"}:
        ctx.gap(stage, "generator_return_is_iterator", "生成器/异步生成器调用返回 iterator，不能把其 body 中 return 对象作为调用返回值。", document, function,
            function_kind=kind)
        return None, None, False
    if kind.get("kind") == "ordinary_async":
        ctx.gap(stage, "async_factory_return_is_promise", "该工厂/VM 的调用未在装配模型中 await，async return 是 Promise，不是直接端口对象。", document, function)
        return None, None, False
    body = _field(function, "body")
    returns = [node for node in walk(body, skip_functions=True) if node.type == "return_statement"]
    if len(returns) != 1:
        ctx.gap(stage, "direct_return_not_unique", "工厂的语法层直接 return 非唯一，不能选择嵌套状态投影代替。", document, _function(definition), count=len(returns))
        return None, None, False
    if returns[0].parent != body or not _children(body) or _children(body)[-1] != returns[0]:
        ctx.gap(stage, "direct_return_control_flow_unknown", "唯一 return 不是外层 body 的末尾直接返回，隐式落空/条件返回未建模。", document, returns[0])
        return None, None, False
    expression = unwrap(next(iter(_children(returns[0])), None))
    frozen = False
    if expression is not None and expression.type == "call_expression":
        receiver, member = _member(document, _field(expression, "function"))
        args = _arguments(expression)
        if document.text(receiver) != "Object" or member != "freeze" or len(args) != 1 or not _builtin(
                ctx, stage, document, receiver, member):
            ctx.gap(stage, "return_wrapper_unknown", "返回 wrapper 不是已核对的普通 Object.freeze。", document, expression)
            return None, None, False
        expression, frozen = unwrap(args[0]), True
    members = _properties(ctx, stage, document, expression)
    if members is None or property_name not in members or members[property_name]["kind"] != "method":
        if members is not None:
            ctx.gap(stage, "returned_method_unknown", "返回对象中没有唯一静态普通方法。", document, expression, property=property_name)
        return None, None, frozen
    method = members[property_name]["value"]
    method_kind = function_kind(document, method)
    if method_kind.get("kind") not in {"ordinary_sync", "ordinary_async"}:
        ctx.gap(stage, "returned_generator_method_body_not_activated", "选定返回方法是生成器/异步生成器，普通调用不会直接进入其 body，不闭合 port 使用。", document, method,
            function_kind=method_kind)
        return None, None, frozen
    fact = ctx.fact("direct_returned_object_method", document, [returns[0], expression, method], {
        "owner_symbol": definition.symbol, "returned_property": property_name, "frozen_wrapper": frozen,
        "factory_function_kind": kind, "returned_method_function_kind": method_kind,
        "static_members": [{"key": key, "kind": item["kind"]} for key, item in members.items()],
        "nested_function_returns_excluded": True})
    ctx.model(OBJECT_MODEL, "literal_return_method_identity", [fact], frozen_wrapper=frozen,
        public_object_mutability="ordinary_public_object" if not frozen else "fixed_standard_freeze_model")
    return method, {"fact_id": fact, "members": members}, frozen


def _stored_call(ctx: _Context, document: Any, call: Any, owner: Any = None) -> tuple[Any, list[dict]]:
    if owner is not None:
        return ctx.sources.call_binding(call, document, owner)
    source_id = document.call_owner(call)
    source_nodes = ctx.sources.nodes.get(source_id, [])
    if len(source_nodes) != 1 or source_nodes[0].kind != "module" or source_nodes[0].file != document.source.path or any(
            source_nodes[0].metadata.get(key) for key in _NODE_GAPS):
        return None, [{"code": "module_call_owner_unknown", "message": "启动调用不属于唯一捕获模块。"}]
    edges = [edge for edge in ctx.sources.edges.get((document.source.path, call.start_point.row + 1,
        call.start_point.column), []) if edge.source == source_id]
    if len(edges) != 1:
        return None, [{"code": "module_call_edge_not_unique", "message": "启动调用位置没有唯一同 owner 快照边。"}]
    edge = edges[0]
    version = ctx.snapshot.stats.get("component_versions", {}).get("typescript", {}).get("analyzer")
    if not version or edge.id != _digest([version, source_id, document.source.path,
            call.start_byte, call.end_byte, "call"])[:24] or edge.expression != document.text(_field(call, "function"))[:600]:
        return None, [{"code": "module_call_identity_mismatch", "message": "启动调用边与原始 byte span/模型身份不一致。"}]
    if edge.resolution != "resolved" or not edge.target or edge.metadata.get("cfg_conditions") or any(
            edge.metadata.get(key) for key in ("incomplete_source", "source_parse_partial", "source_ambiguous",
                "source_attribute_macros_unknown", "closure_activation_unknown")):
        return None, [{"code": "module_call_binding_unknown", "message": "启动 callee 尚非唯一内部 resolved CALLS。",
            "edge_id": edge.id, "resolution": edge.resolution}]
    targets = ctx.sources.nodes.get(edge.target, [])
    if len(targets) != 1:
        return None, [{"code": "module_call_target_unknown", "message": "启动目标图声明不是唯一。"}]
    _, _, problems = ctx.sources.definition_for_node(targets[0])
    return (None, problems) if problems else (edge, [])


def _relative_source(ctx: _Context, stage: str, origin: Any, specifier: str, at: Any) -> Any:
    if not specifier.startswith(".") or "\\" in specifier or "\x00" in specifier:
        ctx.gap(stage, "literal_import_source_unsupported", "独立装配模型只支持规范相对 literal import。", origin, at)
        return None
    base = posixpath.normpath(posixpath.join(posixpath.dirname(origin.source.path), specifier))
    if base.startswith("/") or base == ".." or base.startswith("../"):
        ctx.gap(stage, "literal_import_out_of_capture", "literal import 逃逸快照项目范围。", origin, at)
        return None
    suffix = PurePosixPath(base).suffix
    paths = [base]
    if suffix == ".js":
        paths += [base[:-3] + extension for extension in (".ts", ".tsx", ".jsx")]
    elif suffix == ".mjs":
        paths += [base[:-4] + ".mts"]
    elif suffix == ".cjs":
        paths += [base[:-4] + ".cts"]
    elif not suffix:
        paths += [base + extension for extension in _EXTENSIONS]
        paths += [base + "/index" + extension for extension in _EXTENSIONS]
    elif suffix not in _EXTENSIONS:
        ctx.gap(stage, "literal_import_not_source", "literal import 不是已支持实现源码后缀。", origin, at)
        return None
    matches = [path for path in sorted(set(paths)) if ctx.sources.files.get(path)]
    if len(matches) != 1 or len(ctx.sources.files[matches[0]]) != 1:
        ctx.gap(stage, "literal_import_source_not_unique", "literal import 的捕获源码映射不唯一，不猜加载器优先级。", origin, at, candidates=matches)
        return None
    document, problems = ctx.sources.load(matches[0])
    if document is None:
        ctx.problems(stage, problems)
    return document


def _holes(node: Any) -> bool:
    previous = "["
    for child in node.children:
        if child.type == "comment":
            continue
        if child.type == "," and previous in {"[", ","}:
            return True
        previous = child.type
    return False


def _dynamic_import_boundary(ctx: _Context, document: Any, call: Any, owner: Any) -> Any:
    owner_id = getattr(owner, "graph_node_id", "")
    edges = [edge for edge in ctx.sources.edges.get((document.source.path, call.start_point.row + 1,
        call.start_point.column), []) if edge.source == owner_id]
    version = ctx.snapshot.stats.get("component_versions", {}).get("typescript", {}).get("analyzer")
    if len(edges) != 1 or not version or document.call_owner(call) != owner_id:
        ctx.gap("injection", "import_boundary_site_not_unique", "独立装配模型要求唯一已捕获、同 owner 的动态调用位置。", document, call)
        return None
    edge = edges[0]
    if edge.id != _digest([version, owner_id, document.source.path, call.start_byte, call.end_byte, "call"])[:24] or edge.expression != document.text(
            _field(call, "function"))[:600]:
        ctx.gap("injection", "import_boundary_identity_mismatch", "动态调用边的原 byte span/表达式/版本身份不一致。", document, call)
        return None
    if edge.resolution not in {"dynamic", "unresolved"} or edge.target or edge.metadata.get("cfg_conditions") or any(
            edge.metadata.get(key) for key in ("incomplete_source", "source_parse_partial", "source_ambiguous",
                "source_attribute_macros_unknown", "closure_activation_unknown")):
        ctx.gap("injection", "import_boundary_not_eligible", "原调用不是可支持的动态 import 边界，来源歧义/部分分析不能由模型补成。", document, call,
            edge_id=edge.id, resolution=edge.resolution)
        return None
    return edge


def _literal_import_target(ctx: _Context, stage: str, document: Any, call: Any,
                           expected_document: Any, expected_definition: Any,
                           caller_definition: Any) -> tuple[Any, dict | None]:
    callee = unwrap(_field(call, "function"))
    record = ctx.record(stage, document, callee)
    if record is None:
        return None, None
    declaration = ctx.bindings(document).declaration_for(record)
    if declaration is None or declaration.type != "variable_declarator" or not _const(declaration):
        ctx.gap(stage, "literal_import_binding_shape_unknown", "动态装配 callee 不是唯一 const 解构声明。", document, callee)
        return None, None
    pattern = _field(declaration, "name")
    value = unwrap(_field(declaration, "value"))
    if pattern is None or pattern.type != "array_pattern" or _holes(pattern) or value is None or value.type != "await_expression":
        ctx.gap(stage, "literal_import_pattern_unknown", "仅支持无缺项数组/静态对象解构与 await Promise.all。", document, declaration)
        return None, None
    promise_call = unwrap(next(iter(_children(value)), None))
    receiver, member = _member(document, _field(promise_call, "function"))
    args = _arguments(promise_call) if promise_call is not None and promise_call.type == "call_expression" else []
    if document.text(receiver) != "Promise" or member != "all" or len(args) != 1 or not _builtin(
            ctx, stage, document, receiver, member):
        ctx.gap(stage, "literal_import_await_model_unknown", "await initializer 不是已核对的 Promise.all 字面数组。", document, value)
        return None, None
    fulfillment = completion_relation(document, promise_call, _function(caller_definition), "await",
        lexical=ctx.bindings(document))
    if not fulfillment.get("direct_await") or not fulfillment.get("normal_value_relation_closed"):
        ctx.gap(stage, "literal_import_await_completion_unknown", "公共完成关系未闭合 Promise.all 的正常 await 结果，不能绑定 namespace 解构值。", document, promise_call,
            completion_relation=fulfillment)
        return None, None
    array = unwrap(args[0])
    patterns, imports = _children(pattern), _children(array)
    if array is None or array.type != "array" or _holes(array) or len(patterns) != len(imports):
        ctx.gap(stage, "literal_import_arity_unknown", "Promise.all import 数组与解构位次无法精确配对。", document, declaration)
        return None, None
    matched = []
    for index, part in enumerate(patterns):
        if part.type != "object_pattern":
            ctx.gap(stage, "literal_import_destructure_unknown", "Promise.all 解构仅支持静态 object pattern。", document, part)
            return None, None
        for item in _children(part):
            if item.type == "shorthand_property_identifier_pattern":
                imported, local = _name(document, item), item
            elif item.type == "pair_pattern":
                imported, local = _name(document, _field(item, "key")), _field(item, "value")
            else:
                ctx.gap(stage, "literal_import_member_pattern_unknown", "解构 default/rest/computed 不按名字猜导出来源。", document, item)
                return None, None
            if imported is None or local is None or local.type not in {"identifier", "shorthand_property_identifier_pattern"}:
                ctx.gap(stage, "literal_import_member_identity_unknown", "解构导出名或本地 binder 不闭合。", document, item)
                return None, None
            candidate = ctx.bindings(document).resolve(local)
            if ctx.same(document, record, candidate):
                matched.append((index, imported, local))
    if len(matched) != 1:
        ctx.gap(stage, "literal_import_binding_not_unique", "callee 声明不能唯一对应实际 import 解构 binder。", document, callee)
        return None, None
    target_index, imported, binder = matched[0]
    target_document = None
    import_sites = []
    for index, expression in enumerate(imports):
        expression = unwrap(expression)
        import_args = _arguments(expression) if expression is not None and expression.type == "call_expression" else []
        if expression is None or expression.type != "call_expression" or _field(expression, "function") is None or _field(
                expression, "function").type != "import" or len(import_args) != 1:
            ctx.gap(stage, "literal_import_array_entry_unknown", "Promise.all 每个成员必须是单实参 literal import。", document, expression)
            return None, None
        specifier = _name(document, import_args[0])
        if specifier is None or import_args[0].type != "string":
            ctx.gap(stage, "literal_import_specifier_unknown", "import 源不是静态字符串。", document, expression)
            return None, None
        loaded = _relative_source(ctx, stage, document, specifier, expression)
        if loaded is None:
            return None, None
        import_sites.append({"index": index, "specifier": specifier, "source_file": loaded.source.path,
            "source_hash": loaded.source.hash, "location": document.location(expression)})
        if index == target_index:
            target_document = loaded
    if target_document is not expected_document:
        ctx.gap(stage, "literal_import_target_mismatch", "实际 literal import 来源不是配置 use 实现源码。", document, call)
        return None, None
    module_scope = target_document._collector_scopes.get(target_document.tree.root_node.id)
    exports = module_scope.module.exports.get(imported, []) if module_scope is not None else []
    if len(exports) != 1 or exports[0].kind != "local":
        ctx.gap(stage, "literal_import_export_unknown", "捕获模块没有唯一 direct local 运行时导出对应 use 声明。", target_document, expected_definition.node)
        return None, None
    definitions = target_document.definitions.get(exports[0].name, [])
    if module_scope.module.commonjs or len(definitions) != 1 or not definitions[0].callable:
        ctx.gap(stage, "literal_import_export_identity_unknown", "导出/source declaration 身份不唯一或存在未建模 CommonJS。", target_document, expected_definition.node)
        return None, None
    actual_definition = definitions[0]
    actual_nodes = ctx.sources.nodes.get(getattr(actual_definition, "graph_node_id", ""), [])
    if len(actual_nodes) != 1:
        ctx.gap(stage, "literal_import_provider_graph_unknown", "实际 local export 没有唯一完整捕获图声明。", target_document, actual_definition.node)
        return None, None
    provider_document, provider_definition, provider_problems = ctx.sources.definition_for_node(actual_nodes[0])
    if provider_document is not target_document or provider_definition is not actual_definition or provider_problems:
        ctx.problems(stage, provider_problems)
        ctx.gap(stage, "literal_import_provider_graph_gap", "实际 local export 有图声明 gap/重绑定，不能绕过旧 CALLS unknown。", target_document, actual_definition.node)
        return None, None
    export_binder = _field(actual_definition.node, "name")
    export_record = ctx.record(stage, target_document, export_binder)
    if export_record is None or actual_definition is not expected_definition:
        ctx.gap(stage, "literal_import_provider_identity_mismatch", "实际导出词法声明不稳定或与 use 选择器不相同。", target_document, actual_definition.node)
        return None, None
    fact = ctx.fact("literal_import_destructuring_callee", document, [declaration, binder, call], {
        "binding_id": record.get("declaration_id", record.get("binding_id")),
        "destructure_index": target_index, "imported_member": imported,
        "imports": import_sites, "target_file": target_document.source.path,
        "target_graph_node_id": getattr(actual_definition, "graph_node_id", ""),
        "provider_declaration_id": export_record.get("declaration_id", export_record.get("binding_id")),
        "await_completion_relation": fulfillment,
        "snapshot_calls_edge_created": False})
    ctx.model(LITERAL_IMPORT_MODEL, "await_namespace_positional_export_binding", [fact],
        source_mapping="unique_captured_relative_source", snapshot_calls_edge_created=False,
        completion_summaries_version=COMPLETION_VERSION,
        import_execution_or_loader_verified=False)
    return actual_definition, {"kind": "independent_assembly_model", "fact_id": fact}


def _binding_uses(ctx: _Context, document: Any, record: dict) -> list[Any]:
    result = []
    for node in walk(document.tree.root_node):
        if node.type not in {"identifier", "shorthand_property_identifier"} or document.text(node) != record.get("name"):
            continue
        candidate = ctx.bindings(document).resolve(node)
        if ctx.same(document, record, candidate):
            result.append(node)
    return result


def _escape_audit(ctx: _Context, stage: str, document: Any, record: dict,
                  allowed: set[int], property_guard: str | None = None,
                  known_data_keys: set[str] | None = None, frozen_fields: bool = False) -> bool:
    declaration = ctx.bindings(document).declaration_for(record)
    binder = record.get("binder_location", {})
    okay = True
    for node in _binding_uses(ctx, document, record):
        if node.id in allowed or (binder.get("start_byte") == node.start_byte and binder.get("end_byte") == node.end_byte):
            continue
        parent = node.parent
        if declaration is not None and _field(declaration, "name") == node:
            continue
        if parent is not None and parent.type in {"required_parameter", "optional_parameter"} and (_field(parent, "pattern") == node or _field(parent, "name") == node):
            continue
        if parent is not None and parent.type in {"member_expression", "subscript_expression"} and _field(parent, "object") == node:
            _, key = _member(document, parent)
            if key is None:
                ctx.gap(stage, "captured_dynamic_property_effect_unknown", "捕获对象含动态属性读取/调用，getter或字段 effect 未闭合。", document, parent)
                okay = False
                continue
            if known_data_keys is not None and key not in known_data_keys and key in _OBJECT_PROTOTYPE_KEYS:
                ctx.gap(stage, "captured_inherited_member_effect_unknown", "捕获对象读取普通原型成员，不能当 own data 字段或未知 effect 已排除。", document, parent)
                okay = False
                continue
            mutation = parent.parent
            while mutation is not None and mutation.type in {"parenthesized_expression", "as_expression",
                    "satisfies_expression", "non_null_expression", "type_assertion"}:
                mutation = mutation.parent
            if mutation is not None and mutation.type in {"assignment_expression", "augmented_assignment_expression", "update_expression", "unary_expression"} and (
                    _field(mutation, "left") == parent or _field(mutation, "argument") == parent):
                if property_guard is None or key is None or key == property_guard:
                    ctx.gap(stage, "captured_property_written", "同一捕获对象的所需字段有写入/delete，不能保持装配值。", document, mutation)
                    okay = False
            elif mutation is not None and mutation.type == "call_expression" and unwrap(_field(mutation, "function")) == parent:
                if frozen_fields:
                    fact = ctx.fact("frozen_port_other_receiver_call", document, [mutation], {
                        "declaration_id": record.get("declaration_id", record.get("binding_id")),
                        "method": key, "only_own_method_field_identity_preserved": True,
                        "callee_effects_analyzed": False})
                    ctx.model(OBJECT_MODEL, "fixed_freeze_preserves_own_method_field", [fact])
                    ctx.gap(stage, "other_port_method_effects_unknown", "其他端口方法 effect 未分析；固定 freeze 模型只保留方法字段身份。",
                        document, mutation, necessary=False, necessary_for_end_to_end=True)
                elif known_data_keys is not None and key not in known_data_keys and key not in _OBJECT_PROTOTYPE_KEYS:
                    fact = ctx.fact("closed_data_object_absent_member_call", document, [mutation], {
                        "declaration_id": record.get("declaration_id", record.get("binding_id")),
                        "member": key, "literal_data_keys": sorted(known_data_keys),
                        "member_absent_in_ordinary_data_model": True,
                        "normal_return_scope_only": True})
                    ctx.model(OBJECT_MODEL, "absent_data_member_has_no_receiver_callback", [fact],
                        ordinary_prototype_model_required=True)
                else:
                    ctx.gap(stage, "captured_receiver_call_effect_unknown", "捕获对象的成员调用可能改写 guard/port 字段，局部无赋值不证明无 effect。", document, mutation)
                    okay = False
            elif known_data_keys is None and not frozen_fields:
                ctx.gap(stage, "captured_member_getter_unknown", "未闭合对象形状的成员读取可能有 getter effect。", document, parent)
                okay = False
            continue
        ctx.gap(stage, "captured_binding_escape_unknown", "捕获对象/端口被赋给未分析别名、传出或作为值使用；不假定其保持原字段。", document, node)
        okay = False
    return okay


def _abrupt(node: Any) -> str | None:
    if node is None:
        return None
    if node.type in {"return_statement", "throw_statement"}:
        return "return" if node.type == "return_statement" else "throw"
    if node.type == "statement_block":
        children = _children(node)
        return _abrupt(children[-1]) if children else None
    return None


def _guard_summaries(ctx: _Context, document: Any, method: Any, call: Any) -> tuple[list[dict], bool]:
    body = _field(method, "body")
    statement = call
    while statement.parent is not None and statement.parent != body:
        if statement.parent.type in _FUNCTIONS:
            break
        statement = statement.parent
    if statement.parent != body:
        ctx.gap("use", "use_control_flow_unknown", "port 调用不位于已支持方法 body 的顶层语句，不推控制支配。", document, call)
        return [], False
    statements = _children(body)
    before = [item for item in statements if item.end_byte <= statement.start_byte]
    result = []
    complete = True
    for item in before:
        if item.type == "if_statement":
            condition = _field(item, "condition")
            consequence, alternative = _field(item, "consequence"), _field(item, "alternative")
            refs = []
            for identifier in walk(condition):
                if identifier.type == "identifier":
                    record = ctx.bindings(document).resolve(identifier)
                    refs.append({"location": document.location(identifier), "state": record.get("state"),
                        "declaration_id": record.get("declaration_id", record.get("binding_id"))})
            fact = ctx.fact("preceding_submit_guard", document, [item, condition], {
                "condition": document.text(condition), "consequence_completion": _abrupt(consequence),
                "alternative_completion": _abrupt(alternative), "condition_bindings": refs,
                "order": "preceding_top_level_statement", "condition_truth_evaluated": False})
            result.append({"fact_id": fact, "condition": document.text(condition),
                "consequence_completion": _abrupt(consequence), "condition_evaluation": "not_performed"})
        elif item.type not in {"lexical_declaration", "variable_declaration", "expression_statement", "empty_statement"}:
            ctx.gap("use", "submit_prior_control_flow_unmodeled", "port 调用之前含未支持控制结构，前置条件摘要不完整。", document, item)
            complete = False
    return result, complete


def _analyze(ctx: _Context) -> None:
    rule, wiring = ctx.rule, ctx.rule["wiring"]
    consumer = rule["consumer"]
    owner_document, owner = _definition(ctx, "port_selection", consumer)
    use_document, use_owner = _definition(ctx, "view_model", wiring["use"])
    injection_document, injection_owner = _definition(ctx, "injection", wiring["injection"])
    if any(item is None for item in (owner, use_owner, injection_owner)):
        return
    factory_calls = _calls(owner_document, owner, consumer["factory_callee"])
    if len(factory_calls) != 1:
        ctx.gap("port_selection", "consumer_factory_call_not_unique", "consumer owner 内 factory 实际调用不唯一。", owner_document, _function(owner), count=len(factory_calls))
        return
    factory_call = factory_calls[0]
    factory_edge, problems = _stored_call(ctx, owner_document, factory_call, owner)
    if factory_edge is None:
        ctx.problems("port_selection", problems)
        return
    factory_node = ctx.sources.nodes[factory_edge.target][0]
    factory_document, factory_definition, problems = ctx.sources.definition_for_node(factory_node)
    if factory_definition is None:
        ctx.problems("port_selection", problems)
        return
    factory_fact = ctx.fact("navigation_consumer_factory_identity", owner_document, [factory_call], {
        "snapshot_edge_id": factory_edge.id, "source_graph_node_id": factory_edge.source,
        "target_graph_node_id": factory_edge.target, "callee_expression": factory_edge.expression})
    ctx.consumer_factory = {"fact_id": factory_fact, "edge_id": factory_edge.id,
        "source_graph_node_id": factory_edge.source, "target_graph_node_id": factory_edge.target,
        "location": owner_document.location(factory_call)}
    factory_method, factory_return, port_frozen = _returned(ctx, "port_selection", factory_document,
        factory_definition, consumer["returned_method"])
    if factory_method is None:
        return

    boot_document, problems = ctx.sources.load(wiring["boot"]["file"])
    if boot_document is None:
        ctx.problems("boot", problems)
        return
    boot_calls = _calls(boot_document, None, wiring["boot"]["callee"])
    if len(boot_calls) != 1:
        ctx.gap("boot", "boot_call_not_unique", "boot 模块内启动调用不唯一。", boot_document, boot_document.tree.root_node, count=len(boot_calls))
        return
    boot_call = boot_calls[0]
    boot_edge, problems = _stored_call(ctx, boot_document, boot_call)
    if boot_edge is None or boot_edge.target != getattr(owner, "graph_node_id", ""):
        ctx.problems("boot", problems)
        if boot_edge is not None:
            ctx.gap("boot", "boot_target_mismatch", "真实启动 CALLS 目标不是 navigation.consumer owner。", boot_document, boot_call,
                target_graph_node_id=boot_edge.target)
        return
    boot_index = wiring["boot"]["argument_index"]
    boot_args = _arguments(boot_call)
    if len(boot_args) <= boot_index or any(arg.type == "spread_element" for arg in boot_args):
        ctx.gap("boot", "boot_argument_unknown", "boot 实参位次不存在或 spread 改变参数绑定。", boot_document, boot_call)
        return
    boot_object = unwrap(boot_args[boot_index])
    boot_members = _properties(ctx, "boot", boot_document, boot_object, data_only=True)
    owner_parameter, owner_parameter_record = _parameter(ctx, "boot", owner_document, owner, boot_index)
    if boot_members is None or owner_parameter_record is None:
        return
    boot_fact = ctx.fact("boot_literal_to_consumer_parameter", boot_document, [boot_call, boot_object], {
        "snapshot_edge_id": boot_edge.id, "target_graph_node_id": boot_edge.target,
        "argument_index": boot_index, "literal_data_keys": sorted(boot_members),
        "formal_parameter_location": owner_document.location(owner_parameter),
        "formal_parameter_declaration_id": owner_parameter_record.get("declaration_id", owner_parameter_record.get("binding_id")),
        "values_executed": False})
    ctx.segment("boot", "confirmed_static", [boot_fact])

    port_declaration = factory_call.parent
    while port_declaration is not None and port_declaration.type != "variable_declarator":
        if port_declaration.type in _FUNCTIONS:
            break
        port_declaration = port_declaration.parent
    if port_declaration is None or port_declaration.type != "variable_declarator" or not _const(port_declaration):
        ctx.gap("port_selection", "factory_port_declaration_unknown", "实际 factory call 不在唯一 const 端口声明初始化中。", owner_document, factory_call)
        return
    port_identifier = _field(port_declaration, "name")
    port_record = ctx.record("port_selection", owner_document, port_identifier)
    branch = unwrap(_field(port_declaration, "value"))
    if port_record is None or branch is None or branch.type != "ternary_expression":
        ctx.gap("port_selection", "factory_port_branch_unknown", "首版只建模 const 端口声明的直接 ternary 初始化。", owner_document, port_declaration)
        return
    selected_branch = next((key for key in ("consequence", "alternative") if unwrap(_field(branch, key)) == factory_call), None)
    condition = unwrap(_field(branch, "condition"))
    operator = owner_document.text(_field(condition, "operator"))
    if selected_branch is None or condition is None or condition.type != "binary_expression" or operator not in {"===", "!=="}:
        ctx.gap("port_selection", "factory_port_guard_unknown", "真实 factory 必须为直接 ternary 分支，guard 为已支持的严格 undefined 比较。", owner_document, branch)
        return
    left, right = unwrap(_field(condition, "left")), unwrap(_field(condition, "right"))
    parameter_use, property_name = _member(owner_document, left)
    undefined = right
    if parameter_use is None:
        parameter_use, property_name = _member(owner_document, right)
        undefined = left
    parameter_record = ctx.record("port_selection", owner_document, parameter_use)
    if parameter_record is None or not ctx.same(owner_document, owner_parameter_record, parameter_record) or property_name is None or undefined is None or undefined.type != "undefined":
        ctx.gap("port_selection", "factory_guard_parameter_mismatch", "guard 不是 boot actual 绑定的同一个 formal 对象与 literal undefined 比较。", owner_document, condition)
        return
    if not _global_name_safe(ctx, "port_selection", owner_document, undefined, "undefined", "") or not _global_name_safe(
            ctx, "port_selection", owner_document, condition, "Object", "prototype") or not _global_name_safe(
            ctx, "boot", boot_document, boot_object, "Object", "prototype"):
        return
    if not _escape_audit(ctx, "port_selection", owner_document, owner_parameter_record, set(), property_guard=property_name,
            known_data_keys=set(boot_members)):
        return
    present = property_name in boot_members
    if not present and property_name in _OBJECT_PROTOTYPE_KEYS:
        ctx.gap("port_selection", "guard_property_inherited_in_standard_model", "guard 字段可能来自普通 Object 原型，不能从无 own key 推 undefined。", owner_document, condition,
            property=property_name)
        return
    undefined_value = not present
    if present:
        value = unwrap(boot_members[property_name]["value"])
        if value is not None and value.type == "undefined":
            if not _global_name_safe(ctx, "boot", boot_document, value, "undefined", ""):
                return
            undefined_value = True
        elif value is not None and value.type in {"null", "string", "number", "true", "false", "array", "object"}:
            undefined_value = False
        else:
            ctx.gap("port_selection", "boot_guard_value_unknown", "boot 对 guard 字段的实际值不是已支持字面值。", boot_document, boot_members[property_name]["node"])
            return
    truth = undefined_value if operator == "===" else not undefined_value
    actual_branch = "consequence" if truth else "alternative"
    matches = actual_branch == selected_branch
    branch_fact = ctx.fact("boot_undefined_guard_selects_port_branch", owner_document, [port_declaration, condition, factory_call], {
        "port_declaration_id": port_record.get("declaration_id", port_record.get("binding_id")),
        "parameter_declaration_id": parameter_record.get("declaration_id", parameter_record.get("binding_id")),
        "guard_property_derived": property_name, "operator": operator,
        "boot_literal_property_present": present, "boot_property_is_undefined_in_model": undefined_value,
        "guard_truth_in_model": truth, "selected_branch": actual_branch,
        "requested_factory_branch": selected_branch, "factory_selected_for_this_boot": matches}, [boot_fact, factory_fact])
    ctx.model(BRANCH_MODEL, "ordinary_object_key_and_strict_undefined_guard", [boot_fact, branch_fact],
        property=property_name, selected_branch=actual_branch,
        prototype_or_host_modification_excluded_by_standard_model=True, runtime_execution_verified=False)
    if not matches:
        ctx.gap("port_selection", "requested_factory_not_selected_for_boot", "此 boot 实参模型选择另一端口分支，不能将主 consumer 接到实际装配。", owner_document, branch)
        ctx.segment("port_selection", "different_branch", [factory_fact, branch_fact])
        return
    ctx.segment("port_selection", "modeled", [factory_fact, factory_return["fact_id"], branch_fact],
        port_object_frozen=port_frozen)

    injection_calls = _calls(injection_document, injection_owner, wiring["injection"]["callee"])
    if len(injection_calls) != 1:
        ctx.gap("injection", "injection_call_not_unique", "注入 owner 内实际 callee 调用不唯一。", injection_document, _function(injection_owner), count=len(injection_calls))
        return
    injection_call = injection_calls[0]
    injection_edge, binding_problems = _stored_call(ctx, injection_document, injection_call, injection_owner)
    import_fact = None
    if injection_edge is not None:
        if injection_edge.target != getattr(use_owner, "graph_node_id", ""):
            ctx.gap("injection", "injection_target_mismatch", "注入 CALLS 目标不是配置 use 实现。", injection_document, injection_call)
            return
        injection_kind = "snapshot_calls_binding"
    else:
        boundary_edge = _dynamic_import_boundary(ctx, injection_document, injection_call, injection_owner)
        if boundary_edge is None:
            ctx.problems("injection", binding_problems)
            return
        modeled, import_fact = _literal_import_target(ctx, "injection", injection_document, injection_call, use_document, use_owner,
            injection_owner)
        if modeled is None:
            ctx.problems("injection", binding_problems)
            return
        injection_kind = "independent_assembly_model"
        ctx.gap("injection", "snapshot_injection_call_not_resolved", "原 CALLS 仍未解析；独立 literal import 装配模型只提供来源对应，不改写 CALLS。",
            injection_document, injection_call, necessary=False, original_binding_problems=binding_problems,
            original_snapshot_edge_id=boundary_edge.id, original_resolution=boundary_edge.resolution)
    injection_index = wiring["injection"]["argument_index"]
    injection_args = _arguments(injection_call)
    if len(injection_args) <= injection_index or any(arg.type == "spread_element" for arg in injection_args):
        ctx.gap("injection", "injection_argument_unknown", "注入实参位次不闭合。", injection_document, injection_call)
        return
    injection_object = unwrap(injection_args[injection_index])
    injection_members = _properties(ctx, "injection", injection_document, injection_object, data_only=True)
    property_name = wiring["injection"]["property"]
    if injection_members is None or property_name not in injection_members:
        if injection_members is not None:
            ctx.gap("injection", "injection_property_missing", "实际封闭注入对象没有配置 port 字段。", injection_document, injection_object)
        return
    injected_identifier = unwrap(injection_members[property_name]["value"])
    injected_record = ctx.record("injection", injection_document, injected_identifier)
    if injection_document is not owner_document or injected_record is None or not ctx.same(owner_document, port_record, injected_record):
        ctx.gap("injection", "injection_port_identity_mismatch", "注入值不是同一词法声明捕获的生产端口；不按拼写串联。", injection_document, injected_identifier)
        return
    if not _escape_audit(ctx, "injection", owner_document, port_record, {injected_identifier.id}, frozen_fields=port_frozen):
        return
    if injection_index != wiring["use"]["parameter_index"] or property_name != wiring["use"]["property"]:
        ctx.gap("injection", "injection_formal_mapping_mismatch", "实参位次/字段与 use formal 定位不能建立同一映射。", injection_document, injection_call)
        return
    use_parameter, use_parameter_record = _parameter(ctx, "view_model", use_document, use_owner, injection_index)
    if use_parameter_record is None:
        return
    injection_fact = ctx.fact("captured_port_actual_to_formal_object", injection_document,
        [injection_call, injection_object, injected_identifier], {
        "binding_kind": injection_kind, "snapshot_edge_id": injection_edge.id if injection_edge is not None else None,
        "port_declaration_id": injected_record.get("declaration_id", injected_record.get("binding_id")),
        "argument_index": injection_index, "property": property_name,
        "formal_parameter_location": use_document.location(use_parameter),
        "formal_parameter_declaration_id": use_parameter_record.get("declaration_id", use_parameter_record.get("binding_id")),
        "target_graph_node_id": getattr(use_owner, "graph_node_id", "")}, [branch_fact, *([import_fact["fact_id"]] if import_fact else [])])
    ctx.segment("injection", "modeled" if import_fact else "confirmed_static", [injection_fact])

    aliases = []
    for declaration in walk(_field(_function(use_owner), "body"), skip_functions=True):
        if declaration.type != "variable_declarator" or not _const(declaration):
            continue
        receiver, key = _member(use_document, _field(declaration, "value"))
        if key != wiring["use"]["property"] or receiver is None or receiver.type != "identifier":
            continue
        candidate = ctx.bindings(use_document).resolve(receiver)
        if ctx.same(use_document, use_parameter_record, candidate):
            aliases.append(declaration)
    if len(aliases) != 1:
        ctx.gap("view_model", "formal_port_alias_not_unique", "VM formal 字段没有唯一直接 const alias。", use_document, _function(use_owner), count=len(aliases))
        return
    alias_declaration = aliases[0]
    alias_identifier = _field(alias_declaration, "name")
    alias_record = ctx.record("view_model", use_document, alias_identifier)
    if alias_record is None or not _escape_audit(ctx, "view_model", use_document, use_parameter_record, set(), property_guard=wiring["use"]["property"],
            known_data_keys=set(injection_members)):
        return
    alias_fact = ctx.fact("formal_port_property_to_const_alias", use_document,
        [use_parameter, alias_declaration], {
        "formal_declaration_id": use_parameter_record.get("declaration_id", use_parameter_record.get("binding_id")),
        "property": wiring["use"]["property"],
        "alias_declaration_id": alias_record.get("declaration_id", alias_record.get("binding_id")),
        "immutable_declaration_kind": "const"}, [injection_fact])
    ctx.model(ALIAS_MODEL, "unique_const_property_alias", [injection_fact, alias_fact])
    returned_method, returned_info, vm_frozen = _returned(ctx, "view_model", use_document, use_owner,
        wiring["use"]["returned_method"])
    if returned_method is None:
        return
    ctx.segment("view_model", "modeled", [alias_fact, returned_info["fact_id"]], public_object_frozen=vm_frozen)
    if not vm_frozen:
        ctx.gap("view_model", "public_returned_object_not_frozen", "VM 实际返回普通公开对象，未证明未来调用方不会替换其方法；并未观察到运行时替换。",
            use_document, returned_method, necessary=False, source_condition="plain_returned_object")
    method_name = wiring["use"]["method"]
    port_calls = []
    for call in walk(_field(returned_method, "body"), skip_functions=True):
        if call.type != "call_expression":
            continue
        receiver, key = _member(use_document, _field(call, "function"))
        if key != method_name or receiver is None or receiver.type != "identifier":
            continue
        candidate = ctx.bindings(use_document).resolve(receiver)
        if ctx.same(use_document, alias_record, candidate):
            port_calls.append((call, receiver, candidate))
    if len(port_calls) != 1 or method_name != consumer["returned_method"]:
        ctx.gap("use", "port_use_not_unique", "返回 VM 方法没有唯一同 const alias 的指定 port 调用，或消费字段不同。", use_document, returned_method, count=len(port_calls))
        return
    port_call, port_receiver, use_record = port_calls[0]
    if not _escape_audit(ctx, "use", use_document, alias_record, {port_receiver.id}, frozen_fields=port_frozen):
        return
    guards, guards_complete = _guard_summaries(ctx, use_document, returned_method, port_call)
    if not port_frozen:
        ctx.gap("use", "port_method_value_mutable", "生产端口返回对象未在受信 freeze 模型中固定方法字段，实际方法值仍可能变化。", factory_document, factory_method)
    use_fact = ctx.fact("returned_method_captures_injected_port_use", use_document,
        [returned_method, port_call, port_receiver], {
        "returned_method": wiring["use"]["returned_method"], "port_method": method_name,
        "alias_declaration_id": use_record.get("declaration_id", use_record.get("binding_id")),
        "port_factory_method_location": factory_document.location(factory_method),
        "port_factory_method_field_fixed_by_model": port_frozen,
        "preceding_guards": guards, "preceding_guard_summary_complete": guards_complete,
        "snapshot_calls_edge_created": False, "event_execution_verified": False},
        [alias_fact, returned_info["fact_id"], factory_return["fact_id"]])
    ctx.model(ALIAS_MODEL, "captured_port_method_use_identity", [use_fact], snapshot_calls_edge_created=False)
    ctx.segment("use", "modeled" if guards_complete and port_frozen else "partial", [use_fact],
        valid_submit_preconditions="source_guards_only_not_evaluated")


def analyze_port_wiring(snapshot: GraphSnapshot, navigation_rule: dict) -> dict:
    """Return finite boot/port/use facts from captured source, never a run verdict."""
    if not isinstance(navigation_rule, dict) or "wiring" not in navigation_rule:
        return {"version": VERSION, "snapshot_id": snapshot.id, "status": "not_configured",
            "source_fact_confirmed": False, "assembly_complete": False, "end_to_end_complete": False,
            "complete_scope": "finite_static_port_assembly", "source_facts": [],
            "model_applications": [], "policy_declared": {}, "unresolved": [], "segments": {}}
    ctx = _Context(snapshot, navigation_rule)
    try:
        _validate(navigation_rule)
        _analyze(ctx)
    except (ValueError, TypeError, AttributeError, ImportError, RuntimeError, RecursionError, OverflowError) as error:
        ctx.gap("analysis", "port_wiring_analysis_unknown", "装配解析不能闭合，保留诊断。",
            exception_kind=type(error).__name__, error=str(error)[:300])
    for stage in ("boot", "port_selection", "injection", "view_model", "use"):
        if stage not in ctx.segments:
            ctx.segment(stage, "unknown", [])
    ctx.gap("route_activation", "route_dispatch_not_analyzed", "尚未分析路由匹配/dispatch 到该 VM 的完整接线；不从 locator 推断到达。",
        necessary=False, necessary_for_end_to_end=True)
    ctx.gap("route_activation", "event_activation_unknown", "没有执行或静态闭合用户事件、有效提交及读取时全局状态稳定性。",
        necessary=False, necessary_for_end_to_end=True)
    ctx.segment("route_activation", "unknown", [], execution_verified=False)
    for stage, value in ctx.segments.items():
        value["gap_ids"] = [item["id"] for item in ctx.gaps if item["segment"] == stage]
    assembly = all(ctx.segments[stage]["state"] in {"confirmed_static", "modeled"} for stage in
        ("boot", "port_selection", "injection", "view_model", "use")) and not any(
        gap["necessary_for_assembly"] for gap in ctx.gaps)
    return {"version": VERSION, "semantic_source_version": SEMANTIC_SOURCE_VERSION,
        "semantic_environment_version": ENVIRONMENT_VERSION, "completion_summaries_version": COMPLETION_VERSION,
        "snapshot_id": snapshot.id, "status": "finite_assembly_confirmed" if assembly else "partial",
        "source_fact_confirmed": assembly, "assembly_complete": assembly, "end_to_end_complete": False,
        "complete_scope": "finite_boot_literal_port_branch_injection_const_capture_and_method_use",
        "consumer_factory": ctx.consumer_factory,
        "source_facts": ctx.facts, "model_applications": ctx.models,
        "policy_declared": {"wiring": deepcopy(navigation_rule.get("wiring")),
            "provenance": deepcopy(navigation_rule.get("provenance", {})),
            "applicability": deepcopy(navigation_rule.get("applicability", {})),
            "source_doc_paths_are_labels_only": True},
        "unresolved": ctx.gaps, "segments": ctx.segments,
        "target_executed": False, "target_tests_run": False, "target_build_run": False,
        "snapshot_calls_edges_created": False}
