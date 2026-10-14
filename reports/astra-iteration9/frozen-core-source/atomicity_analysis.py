"""Finite protection-region and deduplication facts over captured TS/JS AST.

Policies select source roles and declare conditional protocol semantics. They
cannot supply predicates, regions or an interleaving. Callback/resource mapping,
guards, source order and predicate syntax are extracted independently. Nothing
opens a target file, evaluates its expressions or certifies a locking protocol.
"""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any

from .models import Evidence, Finding, GraphSnapshot
from .completion_summaries import VERSION as COMPLETION_VERSION, completion_relation, function_kind
from .semantic_environment import VERSION as ENVIRONMENT_VERSION, BuiltinEnvironment

VERSION = "static-atomicity-contracts-2-shared"
POLICY_VERSION = "static-atomicity-policy-v1"
_FUNCTIONS = {"function_declaration", "generator_function_declaration", "method_definition",
              "function_expression", "generator_function", "arrow_function"}
_WRAPPERS = {"parenthesized_expression", "as_expression", "satisfies_expression", "non_null_expression"}
_COMMENTS = {"comment", "line_comment", "block_comment"}
_SAMPLE = 8
_CALL_LIMIT = 128


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True,
        separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()


def _data(value: Any, depth: int = 0, budget: list[int] | None = None) -> None:
    budget = [8192] if budget is None else budget
    budget[0] -= 1
    if depth > 32 or budget[0] < 0:
        raise ValueError("原子边界合同超出 JSON 大小或嵌套范围。")
    if value is None or type(value) in {bool, int}:
        return
    if type(value) is str and len(value) <= 16384 and "\x00" not in value:
        return
    if type(value) is float and math.isfinite(value):
        return
    if type(value) is list:
        for item in value:
            _data(item, depth + 1, budget)
        return
    if type(value) is dict and all(type(key) is str for key in value):
        for key, item in value.items():
            _data(key, depth + 1, budget)
            _data(item, depth + 1, budget)
        return
    raise ValueError("原子边界合同仅接受有限 JSON 数据。")


def _string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and "\x00" not in value


def _path(value: Any) -> bool:
    return (_string(value) and not value.startswith("/") and "\\" not in value
        and all(part not in {"", ".", ".."} for part in value.split("/")))


def _keys(value: Any, required: set[str], optional: set[str] = frozenset()) -> None:
    if not isinstance(value, dict) or not required <= set(value) or set(value) - required - optional:
        raise ValueError("原子边界合同字段不完整或包含未支持字段。")


def _selector(value: Any) -> None:
    _keys(value, {"file", "symbol"})
    if not _path(value["file"]) or not _string(value["symbol"]):
        raise ValueError("源码选择器需要项目内相对路径与精确词法 symbol。")


def _name(value: Any) -> None:
    if not _string(value) or any(not part.isidentifier() or "\\" in part for part in value.split(".")):
        raise ValueError("callee/binding 只能是未转义词法名称或 member 路径。")


def _index(value: Any) -> None:
    if type(value) is not int or not 0 <= value <= 32:
        raise ValueError("参数位置必须为 0 至 32 的整数。")


def _strings(value: Any, required: bool = False) -> None:
    if (not isinstance(value, list) or len(value) > 64
            or not all(_string(item) for item in value) or (required and not value)):
        raise ValueError("合同条件/反证必须为有界字符串列表。")


def validate_atomicity_rule(rule: Any) -> None:
    """Strict data-only schema; selectors are candidates, never region facts."""
    _data(rule)
    _keys(rule, {"id", "type", "facade", "authority", "predicate_sources", "protection", "resource", "provenance", "applicability"},
          {"severity", "dependency_assembly", "transition"})
    if not _string(rule["id"]) or rule["type"] != "protected_deduplication":
        raise ValueError("首版原子合同需要 id 与 type=protected_deduplication。")
    if rule.get("severity", "medium") not in {"high", "medium", "low", "info"}:
        raise ValueError("原子合同 severity 无效。")
    facade = rule["facade"]
    _keys(facade, {"owner", "read", "select", "write"})
    _selector(facade["owner"])
    for role in ("read", "write"):
        call = facade[role]
        _keys(call, {"callee", "resource_argument_index"}, {"implementation"} if role == "read" else set())
        _name(call["callee"])
        _index(call["resource_argument_index"])
        if "implementation" in call:
            _selector(call["implementation"])
    _keys(facade["select"], {"callee", "implementation"})
    _name(facade["select"]["callee"])
    _selector(facade["select"]["implementation"])
    _selector(rule["authority"])
    if rule.get("dependency_assembly") is not None:
        _selector(rule["dependency_assembly"])
    predicates = rule["predicate_sources"]
    _keys(predicates, {"terminal_predicate", "terminal_values", "key"})
    for value in predicates.values():
        _selector(value)
    model = rule["protection"]
    _keys(model, {"id", "version", "kind", "wrappers", "lifecycle"})
    if not _string(model["id"]) or not _string(model["version"]) or model["kind"] != "directory_owner_lock":
        raise ValueError("保护模型需要有版本的 directory_owner_lock 声明。")
    wrappers = model["wrappers"]
    if not isinstance(wrappers, list) or not 1 <= len(wrappers) <= 8:
        raise ValueError("保护模型需要 1 至 8 个源码 wrapper 候选。")
    seen = set()
    for wrapper in wrappers:
        _keys(wrapper, {"owner", "callee", "callback_parameter_index", "callback_argument_index", "resource_parameter_index", "resource_argument_index"})
        _selector(wrapper["owner"])
        _name(wrapper["callee"])
        for key in ("callback_parameter_index", "callback_argument_index", "resource_parameter_index", "resource_argument_index"):
            _index(wrapper[key])
        identity = (wrapper["owner"]["file"], wrapper["owner"]["symbol"])
        if identity in seen or wrapper["callback_parameter_index"] == wrapper["resource_parameter_index"]:
            raise ValueError("wrapper 身份重复或 callback/resource 参数槽相同。")
        seen.add(identity)
    life = model["lifecycle"]
    _keys(life, {"owner", "callback_parameter_index", "resource_parameter_index", "acquire", "fresh_read", "persist", "release", "acquired_binding", "process_fence"})
    _selector(life["owner"])
    for key in ("callback_parameter_index", "resource_parameter_index"):
        _index(life[key])
    if life["callback_parameter_index"] == life["resource_parameter_index"]:
        raise ValueError("lifecycle callback/resource 参数槽相同。")
    _name(life["acquired_binding"])
    if "." in life["acquired_binding"]:
        raise ValueError("acquired_binding 必须为一个局部绑定名称。")
    for role in ("acquire", "fresh_read", "persist", "release"):
        call = life[role]
        _keys(call, {"callee", "resource_argument_index"}, {"resource_binding"} if role == "acquire" else set())
        _name(call["callee"])
        _index(call["resource_argument_index"])
    if not _string(life["acquire"].get("resource_binding")) or not life["acquire"]["resource_binding"].isidentifier():
        raise ValueError("acquire 必须选择实际局部 resource_binding，不能手填区域结果。")
    fence = life["process_fence"]
    _keys(fence, {"callee", "implementation", "callback_argument_index"})
    _name(fence["callee"])
    _selector(fence["implementation"])
    _index(fence["callback_argument_index"])
    if rule.get("transition") is not None:
        transition = rule["transition"]
        _keys(transition, {"owner", "callee", "patch_argument_index", "guard_argument_index"})
        _selector(transition["owner"])
        _name(transition["callee"])
        _index(transition["patch_argument_index"])
        _index(transition["guard_argument_index"])
    resource = rule["resource"]
    _keys(resource, {"id", "authority", "conditions"})
    if not _string(resource["id"]) or resource["authority"] not in {"source_declared", "policy_declared"}:
        raise ValueError("资源映射需要声明来源 authority，不能伪装成物理身份证明。")
    _strings(resource["conditions"], required=True)
    provenance = rule["provenance"]
    _keys(provenance, {"authority", "author_approved", "source_doc"}, {"reviewer", "note"})
    if (not _string(provenance["authority"]) or not _string(provenance["source_doc"])
            or type(provenance["author_approved"]) is not bool):
        raise ValueError("provenance 需要 authority/author_approved/source_doc；文档路径仅作标签。")
    applicability = rule["applicability"]
    _keys(applicability, {"kind", "conditions"}, {"counterexamples"})
    if applicability["kind"] != "conditional":
        raise ValueError("原子区域协议首版仅支持保留明确条件的 conditional 合同。")
    _strings(applicability["conditions"], required=True)
    _strings(applicability.get("counterexamples", []))


def _walk(node: Any, skip_functions: bool = False):
    stack = [node] if node is not None else []
    while stack:
        current = stack.pop()
        yield current
        if skip_functions and current != node and current.type in _FUNCTIONS:
            continue
        stack.extend(reversed(current.named_children))


def _unwrap(node: Any) -> Any:
    while node is not None and node.type in _WRAPPERS | {"await_expression"}:
        node = node.child_by_field_name("expression") or next((child for child in node.named_children if child.type not in _COMMENTS), None)
    return node


def _children(node: Any) -> list[Any]:
    return [child for child in node.named_children if child.type not in _COMMENTS] if node is not None else []


def _ancestors(node: Any):
    while node is not None:
        yield node
        node = node.parent


def _inside(outer: Any, inner: Any) -> bool:
    return outer is not None and inner is not None and outer.start_byte <= inner.start_byte and inner.end_byte <= outer.end_byte


def _path_of(document: Any, node: Any) -> list[str] | None:
    node = _unwrap(node)
    if node is None:
        return None
    if node.type in {"identifier", "shorthand_property_identifier", "this"}:
        value = document.text(node)
        return [value] if "\\" not in value else None
    if node.type == "member_expression":
        prefix = _path_of(document, node.child_by_field_name("object"))
        prop = node.child_by_field_name("property")
        if prefix is not None and prop is not None and prop.type in {"property_identifier", "identifier"}:
            value = document.text(prop)
            return [*prefix, value] if "\\" not in value else None
    return None


def _args(call: Any) -> list[Any]:
    return _children(call.child_by_field_name("arguments"))


def _argument(call: Any, index: int) -> Any:
    arguments = _args(call)
    if index >= len(arguments) or any(node.type == "spread_element" for node in arguments[:index + 1]):
        return None
    return arguments[index]


def _function(document: Any, definition: Any) -> Any:
    value = definition.node if definition.node.type in _FUNCTIONS else _unwrap(definition.value)
    return value if _ordinary(document, value) else None


def _ordinary(document: Any, function: Any) -> bool:
    return function_kind(document, function)["ordinary"]


def _synchronous(document: Any, function: Any) -> bool:
    return function_kind(document, function)["kind"] == "ordinary_sync"


def _parameters(function: Any) -> list[Any]:
    params = function.child_by_field_name("parameters")
    return _children(params) if params is not None else [function.child_by_field_name("parameter")] if function.child_by_field_name("parameter") is not None else []


def _param(document: Any, function: Any, index: int) -> str | None:
    parameters = _parameters(function)
    if index >= len(parameters):
        return None
    parameter = parameters[index]
    pattern = parameter.child_by_field_name("pattern") or parameter
    return document.text(pattern) if pattern.type == "identifier" else None


def _param_node(function: Any, index: int) -> Any:
    parameters = _parameters(function)
    if index >= len(parameters):
        return None
    return parameters[index].child_by_field_name("pattern") or parameters[index]


def _root_identifier(node: Any) -> Any:
    node = _unwrap(node)
    while node is not None and node.type == "member_expression":
        node = _unwrap(node.child_by_field_name("object"))
    return node if node is not None and node.type in {"identifier", "shorthand_property_identifier"} else None


def _direct_predecessor(document: Any, event: Any, target: Any, block: Any) -> bool:
    """Source-structure dominance: an unconditional direct event precedes target."""
    if block is None or block.type != "statement_block":
        return False
    statements = _children(block)
    event_statement = next((node for node in statements if _inside(node, event)), None)
    target_statement = next((node for node in statements if _inside(node, target)), None)
    if event_statement is None or target_statement is None or event_statement.start_byte >= target_statement.start_byte:
        return False
    if event_statement.type == "expression_statement":
        values = _children(event_statement)
        expression = _unwrap(values[0]) if len(values) == 1 else None
        return bool(expression == event or (expression is not None and expression.type == "assignment_expression"
            and _unwrap(expression.child_by_field_name("right")) == event))
    if event_statement.type == "lexical_declaration":
        declarators = [child for child in event_statement.named_children if child.type == "variable_declarator"]
        return len(declarators) == 1 and _unwrap(declarators[0].child_by_field_name("value")) == event
    return False


def _direct_call_statement(statement: Any, call: Any) -> bool:
    if statement is None or call is None:
        return False
    if statement.type == "expression_statement":
        values = _children(statement)
        return len(values) == 1 and _unwrap(values[0]) == call
    if statement.type in {"lexical_declaration", "variable_declaration"}:
        declarators = _children(statement)
        return (len(declarators) == 1 and declarators[0].type == "variable_declarator"
            and declarators[0].child_by_field_name("name") is not None
            and declarators[0].child_by_field_name("name").type == "identifier"
            and _unwrap(declarators[0].child_by_field_name("value")) == call)
    return False


def _effect_free_declaration(statement: Any) -> bool:
    """Only plain local declarations with primitive literals can bridge regions."""
    if statement is None or statement.type not in {"lexical_declaration", "variable_declaration"}:
        return False
    declarators = _children(statement)
    return bool(declarators) and all(node.type == "variable_declarator"
        and node.child_by_field_name("name") is not None
        and node.child_by_field_name("name").type == "identifier"
        and (node.child_by_field_name("value") is None
            or node.child_by_field_name("value").type in {"null", "true", "false", "number", "string"})
        for node in declarators)


def _calls(document: Any, body: Any, name: str | None = None, *, nested: bool = False) -> list[Any]:
    calls = [node for node in _walk(body, skip_functions=not nested) if node.type == "call_expression"
        and (name is None or _path_of(document, node.child_by_field_name("function")) == name.split("."))]
    return calls


def _variable(document: Any, body: Any, name: str) -> list[Any]:
    return [node for node in _walk(body, skip_functions=True) if node.type == "variable_declarator"
        and _path_of(document, node.child_by_field_name("name")) == [name]]


def _writes(document: Any, body: Any, name: str) -> list[Any]:
    values = []
    for node in _walk(body):
        if node.type not in {"assignment_expression", "augmented_assignment_expression", "update_expression"}:
            continue
        left = node.child_by_field_name("left") or node.child_by_field_name("argument")
        path = _path_of(document, left)
        if path and path[0] == name:
            values.append(node)
    return values


def _literal(document: Any, node: Any) -> Any:
    node = _unwrap(node)
    if node is None:
        return None
    if node.type in {"true", "false"}:
        return node.type == "true"
    if node.type == "string":
        # Trusted decoder handles syntax data; never evaluates a JS expression.
        from .static_contracts import _literal_string
        return _literal_string(document.text(node))
    return None


def _op(document: Any, node: Any) -> str:
    operator = node.child_by_field_name("operator")
    return document.text(operator) if operator is not None else ""


def _conjuncts(document: Any, node: Any) -> list[Any]:
    node = _unwrap(node)
    if node is not None and node.type == "binary_expression" and _op(document, node) == "&&":
        return [*_conjuncts(document, node.child_by_field_name("left")), *_conjuncts(document, node.child_by_field_name("right"))]
    return [node] if node is not None else []


def _bound_call(call: Any) -> Any:
    for node in _ancestors(call.parent):
        if node.type == "variable_declarator":
            return node
        if node.type in _FUNCTIONS:
            return None
    return None


def _conditions(document: Any, node: Any, boundary: Any) -> list[dict]:
    values = []
    for parent in _ancestors(node.parent):
        if parent == boundary:
            break
        if parent.type == "if_statement":
            condition = parent.child_by_field_name("condition")
            consequence = parent.child_by_field_name("consequence")
            alternative = parent.child_by_field_name("alternative")
            if condition is not None:
                branch = "then" if _inside(consequence, node) else "else" if _inside(alternative, node) else "condition"
                values.append({"expression": document.text(condition)[:2000], "branch": branch,
                               "location": document.location(condition)})
        if len(values) >= _SAMPLE:
            break
    return values


def _terminal(statement: Any) -> bool:
    statement = _unwrap(statement)
    if statement is None:
        return False
    if statement.type in {"throw_statement", "return_statement", "continue_statement", "break_statement"}:
        return True
    children = _children(statement)
    return statement.type == "statement_block" and bool(children) and children[-1].type in {"throw_statement", "return_statement", "continue_statement", "break_statement"}


class _Analysis:
    def __init__(self, snapshot: GraphSnapshot, sources: Any):
        self.snapshot, self.sources = snapshot, sources
        self.issues: list[dict] = []
        self.documents: dict[str, Any] = {}
        self.nodes = {node.id: node for node in snapshot.nodes}
        node_counts: dict[str, int] = {}
        for node in snapshot.nodes:
            node_counts[node.id] = node_counts.get(node.id, 0) + 1
        self.duplicate_nodes = {key for key, count in node_counts.items() if count > 1}
        self.node_ids: set[str] = set()
        self.edge_ids: set[str] = set()
        self.lexical_readers: dict[str, Any] = {}
        self.completion_relations: dict[tuple, dict] = {}
        self.builtin_environments: dict[str, Any] = {}
        self.sites: dict[tuple, list[Any]] = {}
        for edge in snapshot.edges:
            self.sites.setdefault((edge.file, edge.line, edge.column, edge.source), []).append(edge)

    def lexical(self, document: Any) -> Any:
        if document.source.path not in self.lexical_readers:
            from .lexical_bindings import LexicalBindings
            self.lexical_readers[document.source.path] = LexicalBindings(document)
        return self.lexical_readers[document.source.path]

    def completion(self, document: Any, call: Any, function: Any = None,
                   consumption: str = "return_or_await") -> dict:
        if function is None and call is not None:
            function = next((node for node in _ancestors(call.parent) if node.type in _FUNCTIONS), None)
        key = (document.source.path, getattr(call, "id", None), getattr(function, "id", None), consumption)
        if key not in self.completion_relations:
            self.completion_relations[key] = completion_relation(document, call, function, consumption,
                lexical=self.lexical(document))
        return self.completion_relations[key]

    def directly_awaited(self, document: Any, call: Any) -> bool:
        return bool(self.completion(document, call, consumption="await").get("direct_await"))

    def environment(self, document: Any) -> Any:
        if document.source.path not in self.builtin_environments:
            self.builtin_environments[document.source.path] = BuiltinEnvironment(document)
        return self.builtin_environments[document.source.path]

    def identity(self, document: Any, node: Any) -> dict:
        root = _root_identifier(node)
        if root is None:
            return {"state": "unknown", "identity_complete": False, "reason": "expression_is_not_an_identifier_binding"}
        return self.lexical(document).resolve(root)

    def same(self, document: Any, first: Any, second: Any) -> bool:
        left, right = _root_identifier(first), _root_identifier(second)
        return bool(left is not None and right is not None and self.lexical(document).same(left, right))

    def exact(self, document: Any, first: Any, second: Any) -> bool:
        left, right = _unwrap(first), _unwrap(second)
        return bool(left is not None and right is not None and left.type == right.type == "identifier"
            and self.lexical(document).same(left, right))

    def writes(self, document: Any, body: Any, identifier: Any, *, members: bool = False) -> tuple[list[Any], bool]:
        identity = self.identity(document, identifier)
        if identity.get("state") != "unique" or not identity.get("identity_complete"):
            return [], False
        values, complete = [], True
        reader = self.lexical(document)
        if identity.get("declaration_kind") == "parameter":
            declaration = reader.declaration_for(identity)
            function = next((node for node in _ancestors(declaration) if node.type in _FUNCTIONS), None)
            if function is not None:
                body = function  # Defaults can reassign another formal before its body.
        for record in reader.writes(identity):
            location = record.get("source_location", {})
            if body is not None and not (body.start_byte <= location.get("start_byte", -1) < body.end_byte):
                continue
            if record.get("possible_effect") and (members or not record.get("member_write") or not record.get("mutation_target_complete")):
                complete = False
            if record.get("identity_match_known") and (members or record.get("binding_reassignment")):
                mutation = reader.mutation_for(record)
                if mutation is None:
                    complete = False
                else:
                    values.append(mutation)
        unique = {(node.type, node.start_byte, node.end_byte): node for node in values}
        return list(unique.values()), complete

    def stable(self, document: Any, body: Any, identifier: Any) -> bool:
        writes, complete = self.writes(document, body, identifier)
        return complete and not writes

    def source_callee(self, document: Any, call: Any, expected: dict | None = None) -> tuple[dict, Any, Any]:
        """Existing CALLS first; narrow same-file declaration relation second."""
        owner_id = document.call_owner(call)
        owners = document.definition_nodes.get(owner_id, [])
        owner = owners[0] if len(owners) == 1 else None
        edge, issues = self.sources.call_binding(call, document, owner.node) if owner is not None else (None, [])
        record = {"state": "unknown", "location": self.ref(document, call), "binding_issues": issues[:_SAMPLE],
            "existing_calls_unchanged": True, "runtime_activation_verified": False}
        if edge is not None:
            target = self.nodes.get(edge.target)
            if target is not None:
                target_doc, definition, problems = self.sources.definition_for_node(target)
                if target_doc is not None and definition is not None and not problems:
                    if expected is None or (target.file == expected["file"] and definition.symbol == expected["symbol"]):
                        self.documents[target_doc.source.path] = target_doc
                        self.node_ids.add(target.id)
                        self.edge_ids.add(edge.id)
                        usable = _function(target_doc, definition) is not None
                        record.update(state="snapshot_resolved" if usable else "generator_or_callable_body_unknown", edge_id=edge.id, target=edge.target,
                            declaration=self.ref(target_doc, definition.node))
                        return record, target_doc, _function(target_doc, definition)
        original = self.sites.get((document.source.path, call.start_point.row + 1, call.start_point.column, owner_id), [])
        if len(original) != 1:
            return record, None, None
        original_edge = original[0]
        record["original_snapshot_edge"] = {"id": original_edge.id, "resolution": original_edge.resolution,
            "target": original_edge.target, "reason": original_edge.reason,
            "closure_activation_unknown": bool(original_edge.metadata.get("closure_activation_unknown"))}
        # Do not bypass any other unknown, duplicate, import or dispatch gap.
        gaps = ("incomplete_source", "source_parse_partial", "source_ambiguous", "source_attribute_macros_unknown", "cfg_conditions")
        function_name = _unwrap(call.child_by_field_name("function"))
        if (original_edge.resolution != "resolved" or not original_edge.metadata.get("closure_activation_unknown")
                or any(original_edge.metadata.get(key) for key in gaps)
                or function_name is None or function_name.type != "identifier"):
            return record, None, None
        info = self.identity(document, function_name)
        declaration = self.lexical(document).declaration_for(info)
        if (info.get("state") != "unique" or not info.get("identity_complete") or declaration is None
                or declaration.type != "function_declaration" or not _ordinary(document, declaration)
                or not self.stable(document, document.tree.root_node, function_name)):
            return record, None, None
        definition = document.definition_for_ast(declaration)
        target = self.nodes.get(original_edge.target)
        target_doc, target_definition, problems = self.sources.definition_for_node(target) if target is not None else (None, None, [])
        if definition is None or target_doc is not document or target_definition is not definition or problems or original_edge.target in self.duplicate_nodes:
            return record, None, None
        if expected is not None and (document.source.path != expected["file"] or definition.symbol != expected["symbol"]):
            return record, None, None
        version = self.snapshot.stats.get("component_versions", {}).get("typescript", {}).get("analyzer")
        span_id = _digest([version, owner_id, document.source.path, call.start_byte, call.end_byte, "call"])[:24] if version else None
        if original_edge.id != span_id or original_edge.expression != document.text(function_name)[:600]:
            return record, None, None
        record.update(state="source_lexical_declaration_relation", declaration=self.ref(document, declaration),
            declaration_identity=info, interpretation="Independent same-file declaration relation; CALLS/activation are not promoted")
        return record, document, declaration

    def issue(self, code: str, message: str, document: Any = None, node: Any = None) -> None:
        item = {"code": code, "message": message}
        if document is not None:
            item["file"] = document.source.path
        if document is not None and node is not None:
            item["location"] = document.location(node)
        self.issues.append(item)

    def select(self, selector: dict, *, callable: bool = True) -> tuple[Any, Any, Any]:
        document, definition, issues = self.sources.select(selector)
        self.issues.extend(issues)
        if document is None or definition is None:
            return document, definition, None
        self.documents[document.source.path] = document
        graph_id = getattr(definition, "graph_node_id", "")
        graph_node = self.nodes.get(graph_id)
        if graph_node is not None and graph_id not in self.duplicate_nodes:
            graph_document, graph_definition, graph_issues = self.sources.definition_for_node(graph_node)
            if graph_document is document and graph_definition is definition and not graph_issues:
                self.node_ids.add(graph_id)
        if document.kind not in {"typescript", "tsx"}:
            self.issue("atomicity_language_unsupported", "原子边界首版仅支持捕获的 TS/JS AST。", document)
            return document, definition, None
        function = _function(document, definition)
        if callable and function is None:
            self.issue("atomicity_owner_not_callable", "所选 symbol 不是唯一函数主体。", document, definition.node)
        return document, definition, function

    def ref(self, document: Any, node: Any) -> dict:
        value = document.location(node)
        value.update(node_type=node.type, byte_start=node.start_byte, byte_end=node.end_byte,
            byte_coordinate_space="captured_utf8_text", byte_end_exclusive=True)
        return value

    def call(self, document: Any, call: Any, owner: dict, target: dict | None = None) -> dict:
        edge, issues = self.sources.call_binding(call, document, owner)
        record = {"location": self.ref(document, call), "callee_syntax": document.text(call.child_by_field_name("function"))[:1000],
            "arguments": [{"syntax": document.text(arg)[:1000], "location": self.ref(document, arg)} for arg in _args(call)[:_SAMPLE]],
            "awaited": self.directly_awaited(document, call), "binding_state": "unknown", "graph_edge_id": edge.id if edge is not None else None,
            "binding_issues": issues[:_SAMPLE], "binding_issue_count": len(issues), "source_runtime_dispatch_verified": False}
        if edge is not None:
            self.edge_ids.add(edge.id)
            node = self.nodes.get(edge.target)
            if node is not None:
                lexical = node.qualname[len(node.module) + 1:] if node.qualname.startswith(node.module + "#") else node.qualname
                target_matches = target is None or (node.file == target["file"] and lexical == target["symbol"])
                record.update(binding_state="snapshot_resolved" if target_matches else "different_snapshot_target",
                    graph_target=edge.target, graph_target_file=node.file, graph_target_symbol=lexical,
                    selected_target_matches=target_matches)
        return record

    def unique_call(self, document: Any, body: Any, callee: str, *, nested: bool = False) -> Any:
        calls = _calls(document, body, callee, nested=nested)
        if len(calls) != 1:
            self.issue("atomicity_callsite_not_unique", f"callee {callee} 在所选范围匹配 {len(calls)} 个调用。", document, body)
            return None
        return calls[0]


def _facade(context: _Analysis, rule: dict) -> dict:
    policy = rule["facade"]
    document, definition, function = context.select(policy["owner"])
    result = {"owner": policy["owner"], "state": "unknown", "runtime_order_proof": False}
    if function is None:
        return result
    body = function.child_by_field_name("body")
    calls = {role: context.unique_call(document, body, policy[role]["callee"]) for role in ("read", "select", "write")}
    result["calls"] = {role: context.call(document, call, policy["owner"],
        policy[role].get("implementation") if role != "write" else rule["authority"])
        for role, call in calls.items() if call is not None}
    if any(call is None for call in calls.values()):
        return result
    read, select, write = (calls[role] for role in ("read", "select", "write"))
    resource_read = _argument(read, policy["read"]["resource_argument_index"])
    resource_write = _argument(write, policy["write"]["resource_argument_index"])
    read_path, write_path = _path_of(document, resource_read), _path_of(document, resource_write)
    # Same spelling is qualified as a lexical candidate, never physical identity.
    same_resource = bool(read_path and len(read_path) == 1 and read_path == write_path
        and context.same(document, resource_read, resource_write) and context.stable(document, body, resource_read))
    select_binding = _bound_call(select)
    select_name = document.text(select_binding.child_by_field_name("name")) if select_binding is not None else None
    early_reuse = []
    if select_name:
        for node in _walk(body, skip_functions=True):
            if node.type != "if_statement" or not select.end_byte < node.start_byte < write.start_byte:
                continue
            condition = node.child_by_field_name("condition")
            positive_terms = _conjuncts(document, condition)
            returns = [candidate for candidate in _walk(node.child_by_field_name("consequence"), skip_functions=True)
                       if candidate.type == "return_statement"]
            if any(_path_of(document, term) == [select_name] and context.same(document, term, select_binding.child_by_field_name("name")) for term in positive_terms) and returns:
                early_reuse.append({"guard": context.ref(document, condition),
                    "return_locations": [context.ref(document, value) for value in returns[:_SAMPLE]],
                    "all_guard_paths_return": _terminal(node.child_by_field_name("consequence"))})
    read_fallback = []
    for parent in _ancestors(read):
        if parent == function:
            break
        if parent.type == "try_statement":
            handler = parent.child_by_field_name("handler")
            if handler is not None:
                read_fallback.append({"handler": context.ref(document, handler),
                    "assignment_samples": [context.ref(document, node) for node in _walk(handler, skip_functions=True)
                        if node.type == "assignment_expression"][:_SAMPLE]})
    project_filters = []
    preselection_structure_complete = True
    for call in _calls(document, body):
        parts = _path_of(document, call.child_by_field_name("function")) or []
        if not parts or parts[-1] != "filter" or not read.start_byte < call.start_byte < select.start_byte:
            continue
        callback = _unwrap(_argument(call, 0))
        filter_binding = _bound_call(call)
        filter_binder = filter_binding.child_by_field_name("name") if filter_binding is not None else None
        if (filter_binder is None or not context.exact(document, _argument(select, 0), filter_binder)
                or not context.stable(document, body, filter_binder)):
            continue
        if not _synchronous(document, callback):
            preselection_structure_complete = False
            continue
        parameter = _param(document, callback, 0)
        comparisons = []
        for node in _walk(callback.child_by_field_name("body"), skip_functions=True):
            if node.type == "binary_expression" and _op(document, node) in {"===", "=="}:
                for side in ("left", "right"):
                    path = _path_of(document, node.child_by_field_name(side))
                    if (path and parameter and path[0] == parameter and len(path) > 1
                            and context.same(document, node.child_by_field_name(side), _param_node(callback, 0))):
                        comparisons.append({"field_path": path[1:], "location": context.ref(document, node),
                            "filter_feeds_select_argument": True})
        project_filters.extend(comparisons)
    result.update(state="source_confirmed", syntax_order="read_select_write" if read.start_byte < select.start_byte < write.start_byte else "different_or_unclosed",
        resource={"read_expression": document.text(resource_read)[:1000] if resource_read is not None else None,
            "write_expression": document.text(resource_write)[:1000] if resource_write is not None else None,
            "same_stable_lexical_candidate": same_resource,
            "read_binding_identity": context.identity(document, resource_read),
            "write_binding_identity": context.identity(document, resource_write), "physical_identity_verified": False},
        call_conditions={role: _conditions(document, call, function) for role, call in calls.items()},
        existing_guard_early_exit=early_reuse[:_SAMPLE], read_catch_fallback=read_fallback[:_SAMPLE],
        preselection_field_comparisons=project_filters[:_SAMPLE], preselection_comparison_count=len(project_filters),
        preselection_comparisons_truncated=len(project_filters) > _SAMPLE,
        preselection_field_paths=sorted({tuple(record["field_path"]) for record in project_filters}) if len(project_filters) <= _CALL_LIMIT else [],
        preselection_structure_complete=preselection_structure_complete and len(project_filters) <= _CALL_LIMIT)
    return result


def _assembly(context: _Analysis, rule: dict) -> dict:
    selector = rule.get("dependency_assembly")
    result = {"state": "policy_declared", "runtime_selection_verified": False, "defaults": []}
    if selector is None:
        return result
    document, _, function = context.select(selector)
    if function is None:
        return result
    keys = {rule["facade"][role]["callee"].split(".")[-1]: role for role in ("read", "write")}
    for node in _walk(function.child_by_field_name("body"), skip_functions=True):
        if node.type != "pair":
            continue
        key = document.text(node.child_by_field_name("key"))
        value = _unwrap(node.child_by_field_name("value"))
        if key not in keys or value is None or value.type != "binary_expression" or _op(document, value) != "??":
            continue
        left, right = value.child_by_field_name("left"), value.child_by_field_name("right")
        result["defaults"].append({"role": keys[key], "field": key, "operator": "??",
            "override_expression": document.text(left)[:1000], "default_expression": document.text(right)[:1000],
            "location": context.ref(document, node), "runtime_override_possible": True})
    result.update(source_owner=selector, source_backed_default_candidates=bool(result["defaults"]),
        interpretation="Default assembly expressions are source facts; their policy-selected implementation/runtime branch is not a CALLS binding")
    return result


def _wrappers(context: _Analysis, rule: dict) -> tuple[list[dict], bool]:
    models = rule["protection"]["wrappers"]
    facts, complete = [], True
    for index, model in enumerate(models):
        document, _, function = context.select(model["owner"])
        next_selector = models[index + 1]["owner"] if index + 1 < len(models) else rule["protection"]["lifecycle"]["owner"]
        record = {"owner": model["owner"], "configured_next_candidate": next_selector, "state": "unknown"}
        if function is None:
            facts.append(record)
            complete = False
            continue
        body = function.child_by_field_name("body")
        call = context.unique_call(document, body, model["callee"])
        callback_name = _param(document, function, model["callback_parameter_index"])
        resource_name = _param(document, function, model["resource_parameter_index"])
        if call is None or not callback_name or not resource_name:
            facts.append(record)
            complete = False
            continue
        callback_arg = _unwrap(_argument(call, model["callback_argument_index"]))
        resource_arg = _argument(call, model["resource_argument_index"])
        resource_parameter = _param_node(function, model["resource_parameter_index"])
        callback_parameter = _param_node(function, model["callback_parameter_index"])
        resource_forwarded = bool(_path_of(document, resource_arg) == [resource_name]
            and context.same(document, resource_arg, resource_parameter) and context.stable(document, body, resource_parameter))
        forwarding_calls = []
        callback_mapping = None
        callback_relation = None
        if _ordinary(document, callback_arg):
            callback_body = callback_arg.child_by_field_name("body")
            forwarding_calls = _calls(document, callback_body, callback_name)
            if len(forwarding_calls) == 1:
                first_parameter = _param(document, callback_arg, 0)
                first_parameter_node = _param_node(callback_arg, 0)
                first_argument = _argument(forwarding_calls[0], 0)
                callback_relation = context.completion(document, forwarding_calls[0], callback_arg)
                callback_mapping = bool(first_parameter and _path_of(document, first_argument) == [first_parameter]
                    and context.same(document, first_argument, first_parameter_node)
                    and context.same(document, forwarding_calls[0].child_by_field_name("function"), callback_parameter)
                    and context.stable(document, body, callback_parameter)
                    and context.stable(document, callback_body, first_parameter_node)
                    and callback_relation["normal_value_relation_closed"])
        elif _path_of(document, callback_arg) == [callback_name]:
            callback_mapping = bool(context.same(document, callback_arg, callback_parameter)
                and context.stable(document, body, callback_parameter))
        binding = context.call(document, call, model["owner"], next_selector)
        delegate_relation = context.completion(document, call, function)
        completion_forwarded = delegate_relation["normal_value_relation_closed"]
        verified = bool(resource_forwarded and callback_mapping and completion_forwarded and binding["binding_state"] == "snapshot_resolved")
        record.update(state="source_confirmed" if verified else "unknown", call=binding,
            resource_parameter=resource_name, resource_forwarded=bool(resource_forwarded),
            callback_parameter=callback_name, callback_forwarded=callback_mapping,
            delegate_completion_forwarded=completion_forwarded,
            delegate_normal_completion_relation=delegate_relation,
            callback_normal_completion_relation=callback_relation,
            resource_binding_identity=context.identity(document, resource_parameter),
            callback_binding_identity=context.identity(document, callback_parameter),
            callback_argument_location=context.ref(document, callback_arg) if callback_arg is not None else None,
            forwarded_invocations=[context.ref(document, node) for node in forwarding_calls[:_SAMPLE]])
        if not verified:
            context.issue("atomicity_wrapper_mapping_unknown", "wrapper 的唯一实际绑定或 callback/resource 形参实参映射未闭合。", document, call)
            complete = False
        facts.append(record)
    return facts, complete


def _returned_result(context: _Analysis, document: Any, function: Any, call: Any) -> tuple[bool, dict]:
    relation = context.completion(document, call, function, consumption="return_result")
    return relation["normal_value_relation_closed"], relation


def _fence_result_chain(context: _Analysis, document: Any, function: Any, callback_index: int,
                        depth: int = 0, visited: frozenset = frozenset()) -> tuple[bool, list[dict]]:
    """Follow actual source bindings and callback argument slots, at most 4 hops."""
    identity = (document.source.path, function.start_byte, function.end_byte, callback_index)
    if depth >= 4 or identity in visited:
        return False, [{"reason": "fence_forward_budget_or_cycle"}]
    parameter = _param_node(function, callback_index)
    body = function.child_by_field_name("body")
    if parameter is None or parameter.type != "identifier" or not context.stable(document, body, parameter):
        return False, [{"reason": "fence_callback_identity_or_write_unknown"}]
    invocation = [call for call in _calls(document, body)
        if _unwrap(call.child_by_field_name("function")) is not None
        and _unwrap(call.child_by_field_name("function")).type == "identifier"
        and context.same(document, call.child_by_field_name("function"), parameter)]
    if len(invocation) == 1:
        complete, result = _returned_result(context, document, function, invocation[0])
        return bool(complete and context.directly_awaited(document, invocation[0])), [{"owner": context.ref(document, function),
            "callback_parameter_identity": context.identity(document, parameter), "invocation": context.ref(document, invocation[0]),
            "completion_awaited": context.directly_awaited(document, invocation[0]), "return_relation": result,
            "runtime_invocation_proof": False}]
    delegations = []
    for call in _calls(document, body):
        for index, argument in enumerate(_args(call)):
            if argument.type == "identifier" and context.same(document, argument, parameter):
                delegations.append((call, index))
    if len(delegations) != 1:
        return False, [{"reason": "fence_callback_delegate_not_unique", "delegate_count": len(delegations)}]
    call, argument_index = delegations[0]
    returned, return_relation = _returned_result(context, document, function, call)
    binding, target_doc, target_function = context.source_callee(document, call)
    record = {"owner": context.ref(document, function), "callback_parameter_identity": context.identity(document, parameter),
        "delegation": binding, "callback_argument_index": argument_index, "return_relation": return_relation}
    if not returned or target_function is None:
        return False, [record]
    complete, rest = _fence_result_chain(context, target_doc, target_function, argument_index, depth + 1, visited | {identity})
    return complete, [record, *rest]


def _lifecycle(context: _Analysis, rule: dict) -> tuple[dict, bool]:
    model = rule["protection"]["lifecycle"]
    document, _, function = context.select(model["owner"])
    result = {"owner": model["owner"], "state": "unknown", "lock_protocol_correctness_verified": False,
        "release_success_verified": False, "process_fence_encloses_mutation_callback": None}
    if function is None:
        return result, False
    body = function.child_by_field_name("body")
    callback_name = _param(document, function, model["callback_parameter_index"])
    resource_name = _param(document, function, model["resource_parameter_index"])
    callback_parameter = _param_node(function, model["callback_parameter_index"])
    resource_parameter = _param_node(function, model["resource_parameter_index"])
    resource_lock = model["acquire"]["resource_binding"]
    lock_declarations = _variable(document, body, resource_lock)
    lock_binder = lock_declarations[0].child_by_field_name("name") if len(lock_declarations) == 1 else None
    lock_identity_stable = bool(lock_binder is not None and context.stable(document, body, lock_binder))
    read = context.unique_call(document, body, model["fresh_read"]["callee"])
    persist = context.unique_call(document, body, model["persist"]["callee"])
    release = context.unique_call(document, body, model["release"]["callee"], nested=True)
    callback = context.unique_call(document, body, callback_name) if callback_name else None
    acquires = [node for node in _calls(document, body, model["acquire"]["callee"], nested=True)
        if _path_of(document, _argument(node, model["acquire"]["resource_argument_index"])) == [resource_lock]
        and context.same(document, _argument(node, model["acquire"]["resource_argument_index"]), lock_binder)]
    acquire = acquires[0] if len(acquires) == 1 else None
    if len(acquires) != 1:
        context.issue("atomicity_acquire_not_unique", "选定目录绑定没有唯一 acquire 调用；其它 mkdir 不充当取得证据。", document, body)
    if any(node is None for node in (read, persist, release, callback, acquire)) or not resource_name or not callback_name:
        return result, False
    role_bindings = {role: context.source_callee(document, node)[0] for role, node in (("fresh_read", read), ("persist", persist), ("release", release))}
    callee_bindings_closed = all(record["state"] in {"snapshot_resolved", "source_lexical_declaration_relation"} for record in role_bindings.values())
    acquire_identity = context.identity(document, acquire.child_by_field_name("function"))
    imported = acquire_identity.get("import") or {}
    primitive_known = bool(acquire_identity.get("state") == "unique" and acquire_identity.get("identity_complete")
        and _unwrap(acquire.child_by_field_name("function")).type == "identifier"
        and imported.get("module") in {"node:fs/promises", "fs/promises"}
        and imported.get("imported_name") == "mkdir" and len(_args(acquire)) == 1
        and context.stable(document, document.tree.root_node, acquire.child_by_field_name("function")))
    result["role_callee_bindings"] = role_bindings
    result["acquire_primitive"] = {"state": "source_imported_trusted_primitive" if primitive_known else "unknown",
        "binding_identity": acquire_identity, "model": "node.fs-promises.mkdir.directory-exclusion-v1" if primitive_known else None,
        "primitive_provider_runtime_verified": False, "model_semantics": "successful nonrecursive mkdir excludes competing directory creation; OS/FS correctness is conditional"}
    result["events"] = {role: {"location": context.ref(document, node), "callee_syntax": document.text(node.child_by_field_name("function")),
        "awaited": context.directly_awaited(document, node), "conditions": _conditions(document, node, function)}
        for role, node in (("acquire", acquire), ("fresh_read", read), ("callback", callback), ("persist", persist), ("release_attempt", release))}
    result["lock_resource_declaration"] = context.ref(document, lock_declarations[0]) if len(lock_declarations) == 1 else None
    result["lock_resource_identity_stable"] = lock_identity_stable
    queue_binding = _bound_call(read)
    queue_name = document.text(queue_binding.child_by_field_name("name")) if queue_binding is not None and queue_binding.child_by_field_name("name").type == "identifier" else None
    queue_binder = queue_binding.child_by_field_name("name") if queue_name else None
    queue_resource_mapping = bool(queue_name and _path_of(document, _argument(callback, 0)) == [queue_name]
        and context.same(document, callback.child_by_field_name("function"), callback_parameter)
        and context.exact(document, _argument(callback, 0), queue_binder)
        and context.exact(document, _argument(read, model["fresh_read"]["resource_argument_index"]), resource_parameter)
        and context.exact(document, _argument(persist, model["persist"]["resource_argument_index"]), resource_parameter)
        and any(context.exact(document, argument, queue_binder) for argument in _args(persist))
        and context.stable(document, body, resource_parameter) and context.stable(document, body, queue_binder)
        and context.stable(document, body, callback_parameter))
    result["fresh_queue_callback_save_mapping"] = queue_resource_mapping
    same_try = next((node for node in _ancestors(read) if node.type == "try_statement"), None)
    try_body = same_try.child_by_field_name("body") if same_try is not None else None
    direct_try = bool(same_try is not None and same_try.parent == body)
    ordered_region = bool(direct_try and _inside(try_body, callback) and _inside(try_body, persist)
        and read.start_byte < callback.start_byte < persist.start_byte < release.start_byte
        and context.directly_awaited(document, read) and context.directly_awaited(document, callback) and context.directly_awaited(document, persist)
        and _direct_predecessor(document, read, callback, try_body))
    # Early exits/releases in the selected mutation body make the modeled
    # lifetime unknown. Normal exceptions are retained by its catch below.
    premature_exits = [node for node in _walk(try_body, skip_functions=True)
        if node.type in {"return_statement", "break_statement", "continue_statement"}]
    result.update(ordered_fresh_read_callback_save_release_attempt=ordered_region,
        mutation_body_premature_exit_count=len(premature_exits),
        mutation_body_premature_exit_samples=[context.ref(document, node) for node in premature_exits[:_SAMPLE]])
    flag = model["acquired_binding"]
    declarations = _variable(document, body, flag)
    flag_binder = declarations[0].child_by_field_name("name") if len(declarations) == 1 else None
    writes, flag_identity_complete = context.writes(document, body, flag_binder)
    flag_false = len(declarations) == 1 and _literal(document, declarations[0].child_by_field_name("value")) is False and declarations[0].parent.parent == body
    flag_write = writes[0] if len(writes) == 1 else None
    flag_true = bool(flag_write is not None and flag_write.type == "assignment_expression"
        and _literal(document, flag_write.child_by_field_name("right")) is True)
    success_if = next((node for node in _ancestors(flag_write) if node.type == "if_statement"), None) if flag_write is not None else None
    success_path = _path_of(document, success_if.child_by_field_name("condition")) if success_if is not None else None
    fenced_declarations = _variable(document, body, success_path[0]) if success_path and len(success_path) == 1 else []
    fenced_binder = fenced_declarations[0].child_by_field_name("name") if len(fenced_declarations) == 1 else None
    fenced_call = _unwrap(fenced_declarations[0].child_by_field_name("value")) if len(fenced_declarations) == 1 else None
    fenced_matches = bool(fenced_call is not None and fenced_call.type == "call_expression"
        and _path_of(document, fenced_call.child_by_field_name("function")) == model["process_fence"]["callee"].split(".")
        and context.directly_awaited(document, fenced_call) and context.stable(document, body, fenced_binder)
        and context.same(document, success_if.child_by_field_name("condition"), fenced_binder)
        and context.exact(document, _argument(fenced_call, 0), lock_binder))
    fenced_binding, fence_document, fence_function = context.source_callee(document, fenced_call, model["process_fence"]["implementation"]) if fenced_matches else ({"state": "unknown"}, None, None)
    fence_forwarded, fence_forwarding = _fence_result_chain(context, fence_document, fence_function, model["process_fence"]["callback_argument_index"]) if fence_function is not None else (False, [])
    acquisition_callback = _unwrap(_argument(fenced_call, model["process_fence"]["callback_argument_index"])) if fenced_matches else None
    acquisition_body = acquisition_callback.child_by_field_name("body") if _ordinary(document, acquisition_callback) else None
    true_returns = [node for node in _walk(acquisition_body, skip_functions=True) if node.type == "return_statement"
        and _children(node) and _literal(document, _children(node)[0]) is True]
    acquisition_try = next((node for node in _ancestors(acquire) if node.type == "try_statement"), None)
    acquisition_try_body = acquisition_try.child_by_field_name("body") if acquisition_try is not None else None
    all_acquisition_returns = [node for node in _walk(acquisition_body, skip_functions=True) if node.type == "return_statement"]
    boolean_returns_only = bool(all_acquisition_returns and all(len(_children(node)) == 1 and _children(node)[0].type in {"true", "false"} for node in all_acquisition_returns))
    acquired_return_relation = bool(acquisition_body is not None and _inside(acquisition_body, acquire)
        and len(true_returns) == 1 and _inside(acquisition_try_body, true_returns[0])
        and _direct_predecessor(document, acquire, true_returns[0], acquisition_try_body)
        and context.directly_awaited(document, acquire) and boolean_returns_only)
    guards = []
    for node in _children(body):
        if node.type != "if_statement" or not node.end_byte < read.start_byte:
            continue
        condition = _unwrap(node.child_by_field_name("condition"))
        if (condition is not None and condition.type == "unary_expression" and _op(document, condition) == "!"
                and context.exact(document, condition.child_by_field_name("argument"), flag_binder)
                and _terminal(node.child_by_field_name("consequence"))):
            guards.append(node)
    guard = guards[0] if len(guards) == 1 else None
    success_consequence = success_if.child_by_field_name("consequence") if success_if is not None else None
    write_direct = bool(flag_write is not None and flag_write.parent is not None and flag_write.parent.type == "expression_statement"
        and (flag_write.parent.parent == success_consequence or flag_write.parent == success_consequence))
    guard_relation = bool(flag_false and flag_true and flag_identity_complete and write_direct
        and fenced_matches and fence_forwarded and acquired_return_relation and guard is not None and flag_write.end_byte < guard.start_byte
        and same_try is not None and guard.end_byte < same_try.start_byte)
    release_same_identity = context.exact(document, _argument(release, model["release"]["resource_argument_index"]), lock_binder)
    handler = same_try.child_by_field_name("handler") if same_try is not None else None
    handler_exits = [node for node in _walk(handler, skip_functions=True) if node.type in {"return_statement", "throw_statement", "break_statement", "continue_statement"}]
    fence_calls = _calls(document, body, model["process_fence"]["callee"])
    release_fence = next((node for node in fence_calls if _inside(node, release)), None)
    release_try = next((node for node in _ancestors(release_fence) if node.type == "try_statement"), None)
    body_statements = _children(body)
    mutation_index = body_statements.index(same_try) if same_try in body_statements else -1
    release_index = body_statements.index(release_try) if release_try in body_statements else -1
    intermediate_statements = body_statements[mutation_index + 1:release_index] if release_index > mutation_index >= 0 else []
    release_statements = _children(release_try.child_by_field_name("body")) if release_try is not None else []
    handler_parameter = handler.child_by_field_name("parameter") if handler is not None else None
    handler_statements = _children(handler.child_by_field_name("body")) if handler is not None else []
    handler_simple_assignments = bool(handler_statements)
    for statement in handler_statements:
        values = _children(statement) if statement.type == "expression_statement" else []
        assignment = values[0] if len(values) == 1 and values[0].type == "assignment_expression" else None
        left = _unwrap(assignment.child_by_field_name("left")) if assignment is not None else None
        right = _unwrap(assignment.child_by_field_name("right")) if assignment is not None else None
        identity = context.identity(document, left)
        error_declaration = context.lexical(document).declaration_for(identity)
        error_initialized_before_region = bool(error_declaration is not None
            and error_declaration.type == "variable_declarator" and identity.get("declaration_kind") in {"let", "var"}
            and error_declaration.child_by_field_name("value") is not None
            and error_declaration.parent is not None and error_declaration.parent.parent == body
            and same_try is not None and error_declaration.end_byte < same_try.start_byte
            and _effect_free_declaration(error_declaration.parent))
        handler_simple_assignments = bool(handler_simple_assignments and assignment is not None
            and any(child.type == "=" for child in assignment.children) and left is not None and left.type == "identifier"
            and identity.get("state") == "unique" and identity.get("identity_complete")
            and error_initialized_before_region and context.exact(document, right, handler_parameter))
    catch_then_release = bool(handler is not None and not handler_exits and handler_simple_assignments
        and same_try.child_by_field_name("finalizer") is None and release_index > mutation_index >= 0
        and release_try.parent == body and all(_effect_free_declaration(node) for node in intermediate_statements)
        and release_statements and _direct_call_statement(release_statements[0], release_fence))
    fence_encloses_callback = any(_inside(node, callback) for node in fence_calls)
    release_arrow = _unwrap(_argument(release_fence, model["process_fence"]["callback_argument_index"])) if release_fence is not None else None
    release_context_complete = bool(release_fence is not None and context.exact(document, _argument(release_fence, 0), lock_binder)
        and _ordinary(document, release_arrow) and context.completion(document, release, release_arrow)["normal_value_relation_closed"]
        and context.directly_awaited(document, release_fence) and context.source_callee(document, release_fence, model["process_fence"]["implementation"])[0]["state"] in {"snapshot_resolved", "source_lexical_declaration_relation"})
    fence_counts_closed = len(fence_calls) == 2 and fenced_call in fence_calls and release_context_complete
    result.update(acquisition_guard={"initial_false": flag_false, "single_true_write": flag_true,
            "write_count": len(writes), "flag_declaration": context.ref(document, declarations[0]) if len(declarations) == 1 else None,
            "success_if": context.ref(document, success_if) if success_if is not None else None,
            "fenced_call": context.ref(document, fenced_call) if fenced_matches else None,
            "fenced_binding": fenced_binding, "callback_result_forwarding_closed": fence_forwarded,
            "callback_result_forwarding": fence_forwarding,
            "flag_binding_identity": context.identity(document, flag_binder),
            "acquire_before_unique_true_return": acquired_return_relation,
            "true_return": context.ref(document, true_returns[0]) if len(true_returns) == 1 else None,
            "failure_guard": context.ref(document, guard) if guard is not None else None,
            "guard_relation_closed": guard_relation},
        release_same_lock_binding=release_same_identity, mutation_catch_defers_error_then_release_attempt=catch_then_release,
        release_reachability_model={"state": "source_closed_direct_regions" if catch_then_release else "unknown",
            "mutation_finalizer_absent": bool(same_try is not None and same_try.child_by_field_name("finalizer") is None),
            "catch_plain_error_assignments_only": handler_simple_assignments,
            "intermediate_statement_count": len(intermediate_statements),
            "release_first_direct_statement": bool(release_statements and _direct_call_statement(release_statements[0], release_fence)),
            "release_region": context.ref(document, release_try) if release_try is not None else None,
            "release_success_verified": False},
        process_fence_call_count=len(fence_calls), process_fence_encloses_mutation_callback=fence_encloses_callback,
        process_fence_scope="acquisition and release callbacks only" if fence_counts_closed and not fence_encloses_callback else "unknown",
        process_fence_locations=[context.ref(document, node) for node in fence_calls[:_SAMPLE]])
    if fence_document is not None and fence_function is not None:
        result["process_fence_implementation"] = {"location": context.ref(fence_document, fence_function),
            "parameter_names": [_param(fence_document, fence_function, index) for index in range(min(len(_parameters(fence_function)), _SAMPLE))],
            "direct_calls": [context.ref(fence_document, node) for node in _calls(fence_document, fence_function.child_by_field_name("body"))[:_SAMPLE]],
            "correctness_verified": False}
    complete = bool(lock_identity_stable and queue_resource_mapping and ordered_region and not premature_exits
        and guard_relation and release_same_identity and catch_then_release and fence_counts_closed and not fence_encloses_callback
        and primitive_known and callee_bindings_closed)
    result["state"] = "source_backed_protocol_model" if complete else "unknown"
    if not complete:
        context.issue("atomicity_lifecycle_unknown", "取得guard、callback/resource映射、释放次序或源码控制区域未在有限模型内闭合。", document, function)
    return result, complete


def _authority(context: _Analysis, rule: dict) -> dict:
    document, _, function = context.select(rule["authority"])
    result = {"owner": rule["authority"], "state": "unknown"}
    if function is None:
        return result
    first = rule["protection"]["wrappers"][0]
    wrapper_name = first["owner"]["symbol"].split(".")[-1]
    call = context.unique_call(document, function.child_by_field_name("body"), wrapper_name)
    if call is None:
        return result
    callback = _unwrap(_argument(call, first["callback_parameter_index"]))
    resource_index = rule["facade"]["write"]["resource_argument_index"]
    resource_name = _param(document, function, resource_index)
    resource_parameter = _param_node(function, resource_index)
    resource_forwarded = bool(resource_name and _path_of(document, _argument(call, first["resource_parameter_index"])) == [resource_name]
        and context.same(document, _argument(call, first["resource_parameter_index"]), resource_parameter)
        and context.stable(document, function.child_by_field_name("body"), resource_parameter))
    result.update(wrapper_call=context.call(document, call, rule["authority"], first["owner"]),
        resource_forwarded=resource_forwarded, callback_is_inline=bool(callback is not None and callback.type in _FUNCTIONS),
        callback_completion_usable=_ordinary(document, callback))
    if not _ordinary(document, callback):
        return result
    body = callback.child_by_field_name("body")
    queue_parameter = _param(document, callback, 0)
    queue_binder = _param_node(callback, 0)
    find_calls = [node for node in _calls(document, body) if (_path_of(document, node.child_by_field_name("function")) or []) == [queue_parameter, "entries", "find"]
        and context.same(document, node.child_by_field_name("function"), queue_binder)]
    push_calls = [node for node in _calls(document, body) if (_path_of(document, node.child_by_field_name("function")) or []) == [queue_parameter, "entries", "push"]
        and context.same(document, node.child_by_field_name("function"), queue_binder)]
    result.update(callback_location=context.ref(document, callback), queue_parameter=queue_parameter,
        find_count=len(find_calls), insertion_count=len(push_calls),
        direct_await_count=sum(node.type == "await_expression" for node in _walk(body, skip_functions=True)))
    if len(find_calls) != 1 or len(push_calls) != 1:
        context.issue("atomicity_check_insert_unknown", "authority callback 不含唯一同一 entries 的 find/push。", document, callback)
        return result
    find, push = find_calls[0], push_calls[0]
    predicate = _unwrap(_argument(find, 0))
    existing_binding = _bound_call(find)
    existing_name = document.text(existing_binding.child_by_field_name("name")) if existing_binding is not None else None
    existing_binder = existing_binding.child_by_field_name("name") if existing_binding is not None else None
    early = []
    for node in _walk(body, skip_functions=True):
        if node.type == "if_statement" and find.end_byte < node.start_byte < push.start_byte:
            consequence = node.child_by_field_name("consequence")
            statements = _children(consequence) if consequence is not None and consequence.type == "statement_block" else [consequence]
            returned = statements[0] if len(statements) == 1 else None
            values = _children(returned) if returned is not None and returned.type == "return_statement" else []
            if (node.parent == body and context.exact(document, node.child_by_field_name("condition"), existing_binder)
                    and len(values) == 1 and context.exact(document, values[0], existing_binder)
                    and existing_binding is not None and existing_binding.parent.parent == body
                    and push.parent is not None and push.parent.type == "expression_statement" and push.parent.parent == body):
                early.append(context.ref(document, node))
    comparisons = []
    predicate_parameter = _param(document, predicate, 0) if _synchronous(document, predicate) else None
    predicate_binder = _param_node(predicate, 0) if predicate_parameter else None
    predicate_body = predicate.child_by_field_name("body") if predicate_parameter else None
    predicate_expression = predicate_body
    if predicate_body is not None and predicate_body.type == "statement_block":
        statements = _children(predicate_body)
        values = _children(statements[0]) if len(statements) == 1 and statements[0].type == "return_statement" else []
        predicate_expression = values[0] if len(values) == 1 else None
    terms = _conjuncts(document, predicate_expression)
    predicate_shape_closed = len(terms) == 2 and all(term.type == "binary_expression" and _op(document, term) == "===" for term in terms)
    for node in terms if predicate_shape_closed else []:
        if node.type != "binary_expression" or _op(document, node) not in {"===", "=="}:
            continue
        for side, other in (("left", "right"), ("right", "left")):
            path = _path_of(document, node.child_by_field_name(side))
            literal = _literal(document, node.child_by_field_name(other))
            if (path and path[0] == predicate_parameter and isinstance(literal, str)
                    and context.same(document, node.child_by_field_name(side), predicate_binder)):
                comparisons.append({"field_path": path[1:], "operator": _op(document, node), "literal": literal,
                    "location": context.ref(document, node)})
    key_name = rule["predicate_sources"]["key"]["symbol"].split(".")[-1]
    key_calls = _calls(document, predicate_body, key_name)
    key_binding = context.source_callee(document, key_calls[0], rule["predicate_sources"]["key"])[0] if len(key_calls) == 1 else {"state": "unknown"}
    key_equality_terms = [term for term in terms if term.type == "binary_expression" and any(_unwrap(term.child_by_field_name(side)) in key_calls for side in ("left", "right"))]
    status_gates = [value for value in comparisons if value["field_path"] == ["status"]]
    model_closed = bool(predicate_shape_closed and len(status_gates) == 1 and len(key_equality_terms) == 1
        and len(key_calls) == 1 and context.exact(document, _argument(key_calls[0], 0), predicate_binder)
        and key_binding["state"] in {"snapshot_resolved", "source_lexical_declaration_relation"})
    result.update(state="source_confirmed", find_location=context.ref(document, find), insertion_location=context.ref(document, push),
        check_before_insert=find.start_byte < push.start_byte, early_existing_reuse=early[:_SAMPLE],
        literal_predicate_comparisons=comparisons[:_SAMPLE], literal_predicate_comparison_count=len(comparisons),
        literal_predicate_comparisons_truncated=len(comparisons) > _SAMPLE,
        predicate_model={"state": "source_closed_conjunction" if model_closed else "unknown",
            "direct_conjunction_term_count": len(terms), "status_equality_literals": [value["literal"] for value in status_gates],
            "key_call_binding": key_binding},
        key_call_locations=[context.ref(document, node) for node in key_calls[:_SAMPLE]],
        predicate_location=context.ref(document, predicate) if predicate is not None else None,
        find_push_same_member_path=bool(queue_parameter), collection_identity_state="unknown",
        collection_identity_verified=False, queue_formal_stable=context.stable(document, callback, queue_binder),
        collection_runtime_methods_verified=False)
    context.issue("atomicity_collection_heap_identity_unresolved", "find/push 共享来源成员路径；未证明 entries 对象身份、getter/别名或任意方法效果。", document, callback)
    return result


def _continue_only(statement: Any) -> bool:
    values = _children(statement) if statement is not None and statement.type == "statement_block" else [statement]
    return len(values) == 1 and values[0] is not None and values[0].type == "continue_statement"


def _return_fields(context: _Analysis, document: Any, function: Any, expression: Any,
                   parameter: Any, depth: int = 0, seen: frozenset = frozenset()) -> tuple[list[dict], bool]:
    if expression is None or depth > 4:
        return [], False
    fields, complete = [], True
    for node in _walk(expression, skip_functions=True):
        path = _path_of(document, node)
        if node.type == "member_expression" and path and len(path) > 1 and context.same(document, node, parameter):
            parent = node.parent
            if parent is not None and parent.type == "member_expression" and parent.child_by_field_name("object") == node:
                continue
            fields.append({"field_path": path[1:], "location": context.ref(document, node)})
        elif node.type == "identifier" and not context.same(document, node, parameter):
            parent = node.parent
            if parent is not None and (parent.type == "member_expression" or parent.type == "call_expression"):
                continue
            info = context.identity(document, node)
            declaration = context.lexical(document).declaration_for(info)
            if declaration is None or declaration.type != "variable_declarator":
                complete = False
                continue
            identity = info.get("declaration_id")
            if identity in seen or not context.stable(document, function.child_by_field_name("body"), node):
                complete = False
                continue
            values, closed = _return_fields(context, document, function, declaration.child_by_field_name("value"), parameter, depth + 1, seen | {identity})
            fields.extend(values)
            complete = complete and closed
        if len(fields) > 128:
            return fields[:128], False
    unique = {(tuple(value["field_path"]), value["location"]["byte_start"]): value for value in fields}
    return list(unique.values()), complete


def _private_set_usage(context: _Analysis, document: Any, receiver: Any) -> dict:
    identity = context.identity(document, receiver)
    declaration = context.lexical(document).declaration_for(identity)
    barriers = []
    if declaration is None or any(node.type == "export_statement" for node in _ancestors(declaration)):
        barriers.append({"kind": "set_declaration_exported_or_unknown"})
    name = document.text(_root_identifier(receiver))
    binder = declaration.child_by_field_name("name") if declaration is not None else None
    for node in _walk(document.tree.root_node):
        if node.type not in {"identifier", "shorthand_property_identifier"} or document.text(node) != name or node == binder:
            continue
        info = context.identity(document, node)
        if info.get("state") != "unique":
            barriers.append({"kind": "set_reference_binding_unknown", "location": context.ref(document, node)})
        elif context.same(document, node, receiver):
            parent = node.parent
            member = parent if parent is not None and parent.type == "member_expression" and parent.child_by_field_name("object") == node else None
            call = member.parent if member is not None else None
            if (member is None or document.text(member.child_by_field_name("property")) != "has"
                    or call is None or call.type != "call_expression" or call.child_by_field_name("function") != member):
                barriers.append({"kind": "set_mutation_alias_escape_or_other_use", "location": context.ref(document, node)})
    return {"captured_private_has_only_usage_closed": not barriers, "barrier_count": len(barriers),
        "barrier_samples": barriers[:_SAMPLE], "barriers_truncated": len(barriers) > _SAMPLE,
        "external_or_runtime_mutation_proof": False}


def _ambient_builtin_candidate(context: _Analysis, document: Any, identifier: Any, member: str | None = None) -> tuple[bool, dict]:
    name = document.text(identifier) if identifier is not None else ""
    audit = context.environment(document).audit(name, identifier, member)
    return bool(audit.get("supported") and audit.get("state") == "supported_in_registered_model"), audit


def _predicates(context: _Analysis, rule: dict) -> dict:
    selectors = rule["predicate_sources"]
    result = {"state": "unknown", "runtime_predicate_equivalence_proof": False}
    outer_doc, _, outer_function = context.select(rule["facade"]["select"]["implementation"])
    term_doc, _, term_function = context.select(selectors["terminal_predicate"])
    values_doc, values_definition, _ = context.select(selectors["terminal_values"], callable=False)
    key_doc, _, key_function = context.select(selectors["key"])
    if any(value is None for value in (outer_function, term_function, values_definition, key_function)):
        return result
    if not all(_synchronous(document, function) for document, function in ((outer_doc, outer_function), (term_doc, term_function), (key_doc, key_function))):
        context.issue("atomicity_async_predicate_unknown", "布尔域/选择器/key 的有限模型只接受同步普通函数。")
        return result
    value = _unwrap(values_definition.value)
    freezer_model_closed = True
    array_freeze_closed = False
    if value is not None and value.type == "call_expression" and _path_of(values_doc, value.child_by_field_name("function")) == ["Object", "freeze"]:
        freezer_receiver = value.child_by_field_name("function").child_by_field_name("object")
        freezer_model_closed, freezer_guard = _ambient_builtin_candidate(context, values_doc, freezer_receiver, "freeze")
        result["array_freezer_model"] = {"model_id": "js-standard-object-freeze-v1", "object_guard": freezer_guard,
            "state": "trusted_ambient_standard_model" if freezer_model_closed else "unknown", "runtime_provider_verified": False}
        array_freeze_closed = freezer_model_closed and len(_args(value)) == 1
        value = _unwrap(_argument(value, 0)) if len(_args(value)) == 1 else None
    values = [_literal(values_doc, node) for node in _children(value)] if value is not None and value.type == "array" else []
    finite_values = bool(values) and all(isinstance(item, str) for item in values) and len(values) <= 64 and freezer_model_closed
    values_binder = values_definition.node.child_by_field_name("name")
    values_stable = bool(values_binder is not None and values_binder.type == "identifier"
        and context.stable(values_doc, values_doc.tree.root_node, values_binder))
    result["terminal_initializer"] = {"state": "source_confirmed" if finite_values else "unknown",
        "members": sorted(set(values)) if finite_values else [],
        "location": context.ref(values_doc, values_definition.node), "runtime_set_mutation_closed": False,
        "captured_array_freeze_model_closed": array_freeze_closed, "values_binding_stable": values_stable}
    terminal_name = selectors["terminal_predicate"]["symbol"].split(".")[-1]
    outer_statements = _children(outer_function.child_by_field_name("body"))
    loop = outer_statements[0] if len(outer_statements) == 2 and outer_statements[0].type == "for_in_statement" else None
    loop_body = loop.child_by_field_name("body") if loop is not None else None
    loop_statements = _children(loop_body)
    loop_operator = _op(outer_doc, loop) if loop is not None else None
    shape = (loop_operator == "of" and not any(child.type == "await" for child in loop.children)
        and len(loop_statements) == 3 and [node.type for node in loop_statements] == ["if_statement", "if_statement", "return_statement"]
        and context.exact(outer_doc, loop.child_by_field_name("right"), _param_node(outer_function, 0))) if loop is not None else False
    returned_entry = _unwrap(_children(loop_statements[2])[0]) if shape and len(_children(loop_statements[2])) == 1 else None
    returned_is_loop_item = bool(loop is not None and context.exact(outer_doc, returned_entry, loop.child_by_field_name("left")))
    key_guard = _unwrap(loop_statements[0].child_by_field_name("condition")) if shape else None
    terminal_call = _unwrap(loop_statements[1].child_by_field_name("condition")) if shape else None
    outer_fields = []
    key_guard_closed = False
    if key_guard is not None and key_guard.type == "binary_expression" and _op(outer_doc, key_guard) == "!==":
        for side, other in (("left", "right"), ("right", "left")):
            path = _path_of(outer_doc, key_guard.child_by_field_name(side))
            if (path and len(path) > 1 and context.same(outer_doc, key_guard.child_by_field_name(side), returned_entry)
                    and context.exact(outer_doc, key_guard.child_by_field_name(other), _param_node(outer_function, 1))):
                outer_fields.append({"field_path": path[1:], "location": context.ref(outer_doc, key_guard)})
                key_guard_closed = True
    terminal_call_shape = bool(terminal_call is not None and terminal_call.type == "call_expression"
        and _path_of(outer_doc, terminal_call.child_by_field_name("function")) == terminal_name.split(".")
        and len(_args(terminal_call)) == 1 and returned_entry is not None
        and _path_of(outer_doc, _argument(terminal_call, 0)) == [outer_doc.text(returned_entry), "status"]
        and context.same(outer_doc, _argument(terminal_call, 0), returned_entry))
    terminal_binding = context.source_callee(outer_doc, terminal_call, selectors["terminal_predicate"])[0] if terminal_call_shape else {"state": "unknown"}
    outer_closed = bool(shape and key_guard_closed and terminal_call_shape and returned_is_loop_item
        and _continue_only(loop_statements[0].child_by_field_name("consequence"))
        and _continue_only(loop_statements[1].child_by_field_name("consequence"))
        and loop_statements[0].child_by_field_name("alternative") is None and loop_statements[1].child_by_field_name("alternative") is None
        and terminal_binding["state"] in {"snapshot_resolved", "source_lexical_declaration_relation"})
    rejection = [{"call": context.ref(outer_doc, terminal_call), "skip_guard": context.ref(outer_doc, loop_statements[1]),
        "polarity": "positive_terminal_call_skips", "return_entry": context.ref(outer_doc, loop_statements[2]),
        "binding": terminal_binding}] if outer_closed else []
    key_body = key_function.child_by_field_name("body")
    key_parameter = _param(key_doc, key_function, 0)
    key_returns = [node for node in _walk(key_body, skip_functions=True) if node.type == "return_statement"]
    key_expression = _children(key_returns[0])[0] if len(key_returns) == 1 and len(_children(key_returns[0])) == 1 else None
    key_fields, key_origins_closed = _return_fields(context, key_doc, key_function, key_expression, _param_node(key_function, 0))
    term_body = term_function.child_by_field_name("body")
    term_statements = _children(term_body)
    term_expression = _children(term_statements[0])[0] if len(term_statements) == 1 and term_statements[0].type == "return_statement" and len(_children(term_statements[0])) == 1 else None
    term_parts = _conjuncts(term_doc, term_expression)
    has_calls = [part for part in term_parts if part.type == "call_expression" and (_path_of(term_doc, part.child_by_field_name("function")) or [])[-1:] == ["has"]]
    type_guards = []
    for part in term_parts:
        if part.type == "binary_expression" and _op(term_doc, part) == "===":
            left, right = _unwrap(part.child_by_field_name("left")), _unwrap(part.child_by_field_name("right"))
            if (left is not None and left.type == "unary_expression" and _op(term_doc, left) == "typeof"
                    and context.exact(term_doc, left.child_by_field_name("argument"), _param_node(term_function, 0))
                    and _literal(term_doc, right) == "string"):
                type_guards.append(part)
    set_relation = None
    if len(term_parts) == 2 and len(has_calls) == 1 and len(type_guards) == 1 and len(_args(has_calls[0])) == 1 and context.exact(term_doc, _argument(has_calls[0], 0), _param_node(term_function, 0)):
        receiver = (_path_of(term_doc, has_calls[0].child_by_field_name("function")) or [])[:-1]
        receiver_node = has_calls[0].child_by_field_name("function").child_by_field_name("object")
        receiver_info = context.identity(term_doc, receiver_node)
        declaration = context.lexical(term_doc).declaration_for(receiver_info)
        if len(receiver) == 1 and declaration is not None and declaration.type == "variable_declarator" and context.stable(term_doc, term_doc.tree.root_node, receiver_node):
            usage = _private_set_usage(context, term_doc, receiver_node)
            initializer = _unwrap(declaration.child_by_field_name("value"))
            if initializer is not None and initializer.type == "new_expression":
                constructor = initializer.child_by_field_name("constructor")
                constructor_name = term_doc.text(constructor) if constructor is not None else None
                constructor_info = context.identity(term_doc, constructor)
                arguments = _args(initializer)
                references_values = bool(len(arguments) == 1 and term_doc is values_doc
                    and context.exact(term_doc, arguments[0], values_binder))
                ambient_standard_candidate, constructor_guard = _ambient_builtin_candidate(context, term_doc, constructor)
                if (constructor_name == "Set" and references_values and array_freeze_closed and values_stable
                        and ambient_standard_candidate and usage["captured_private_has_only_usage_closed"]):
                    set_relation = {"initialization": context.ref(term_doc, declaration), "receiver_binding_identity": receiver_info,
                        "membership_call": context.ref(term_doc, has_calls[0]),
                        "constructor_binding": constructor_info, "constructor_guard": constructor_guard, "trusted_model_id": "js-standard-set-initializer-membership-v1",
                        "captured_usage_review": usage,
                        "assumptions": ["ambient global Set implements standard JavaScript Set", "no unmodeled mutation changes the captured initializer membership"],
                        "provider_or_runtime_membership_verified": False,
                        "interpretation": "source-backed standard Set initializer model with explicit unresolved ambient/runtime premises"}
    complete = bool(finite_values and outer_closed and set_relation is not None)
    result.update(state="source_backed_standard_set_model" if complete else "unknown", outer_terminal_rejection=rejection[:_SAMPLE],
        outer_control_pattern_closed=outer_closed, outer_loop_operator=loop_operator,
        terminal_set_initialization_relation=set_relation,
        outer_key_comparison_fields=outer_fields[:_SAMPLE], outer_key_field_paths=[value["field_path"] for value in outer_fields],
        authority_key_source={"parameter": key_parameter, "field_reads": key_fields[:32], "field_read_count": len(key_fields),
            "field_reads_truncated": len(key_fields) > 32,
            "field_paths": sorted({tuple(value["field_path"]) for value in key_fields}),
            "origin_model_closed": key_origins_closed,
            "return_locations": [context.ref(key_doc, node) for node in key_returns[:_SAMPLE]],
            "key_value_equivalence_proof": False})
    if not complete:
        context.issue("atomicity_predicate_model_unknown", "terminal初始化/成员调用/排除分支关联未闭合，只保留结构事实。")
    return result


def _transition(context: _Analysis, rule: dict) -> dict:
    policy = rule.get("transition")
    result = {"state": "not_requested", "runtime_transition_success_proof": False, "transitions": [], "status_patch_facts": []}
    if policy is None:
        return result
    document, _, function = context.select(policy["owner"])
    result["state"] = "unknown"
    if function is None:
        return result
    calls = _calls(document, function.child_by_field_name("body"), policy["callee"])
    if len(calls) > _CALL_LIMIT:
        context.issue("atomicity_transition_budget", "状态更新调用超出有限提取预算。", document, function)
        return result
    for call in calls:
        records = []
        for role, index in (("patch", policy["patch_argument_index"]), ("guard", policy["guard_argument_index"])):
            obj = _unwrap(_argument(call, index))
            fields = {}
            closed = obj is not None and obj.type == "object"
            for child in _children(obj) if closed else []:
                if child.type != "pair":
                    closed = False
                    continue
                key_node, value_node = child.child_by_field_name("key"), child.child_by_field_name("value")
                key = document.text(key_node) if key_node is not None and key_node.type in {"property_identifier", "identifier"} else None
                literal = _literal(document, value_node)
                if key and isinstance(literal, str):
                    if key in fields:
                        closed = False
                    fields[key] = {"literal": literal, "location": context.ref(document, child)}
                elif key is None:
                    closed = False
            records.append({"role": role, "explicit_string_fields": fields, "whole_shape_closed": closed})
        binding, _, _ = context.source_callee(document, call)
        call_fact = {"location": context.ref(document, call), "fields": records,
            "conditions": _conditions(document, call, function), "dispatch_binding": binding,
            "dispatch_verified": False, "interpretation": "captured patch/guard arguments; mutation execution not inferred"}
        result["transitions"].append(call_fact)
        patch, guard = records
        status = patch["explicit_string_fields"].get("status")
        expected_status = guard["explicit_string_fields"].get("expectedStatus")
        if status is not None and patch["whole_shape_closed"]:
            result["status_patch_facts"].append({"status": status["literal"], "location": status["location"],
                "call_location": call_fact["location"],
                "expected_status": expected_status["literal"] if expected_status is not None and guard["whole_shape_closed"] else None,
                "expected_status_location": expected_status["location"] if expected_status is not None and guard["whole_shape_closed"] else None,
                "transition_execution_verified": False})
    result.update(state="source_confirmed" if result["transitions"] else "unknown",
        transition_count=len(result["transitions"]), transitions=result["transitions"][:_SAMPLE],
        transitions_truncated=len(result["transitions"]) > _SAMPLE)
    return result


def _compare(facade: dict, authority: dict, predicates: dict, lifecycle_complete: bool,
             wrappers_complete: bool, transition: dict, assembly: dict) -> dict:
    wrapper = authority.get("wrapper_call", {})
    protected = bool(lifecycle_complete and wrappers_complete and authority.get("resource_forwarded")
        and wrapper.get("binding_state") == "snapshot_resolved" and authority.get("callback_completion_usable"))
    outside = None
    if protected and facade.get("state") == "source_confirmed" and facade.get("syntax_order") == "read_select_write":
        outside = facade["owner"] != authority["owner"]
    status_literals = authority.get("predicate_model", {}).get("status_equality_literals", [])
    excluded = predicates.get("terminal_initializer", {}).get("members", [])
    domain = {"state": "unknown", "semantic_equivalence_proof": False}
    if (predicates.get("state") == "source_backed_standard_set_model" and authority.get("predicate_model", {}).get("state") == "source_closed_conjunction"
            and len(status_literals) == 1):
        domain.update(state="source_backed_symbolic_difference", outer={"kind": "not_terminal_initializer_members", "excluded_members": excluded},
            inner={"kind": "literal_equality", "member": status_literals[0]},
            trusted_model=predicates.get("terminal_set_initialization_relation"), domain_scope="string status values",
            interpretation="Symbolic domains in the closed captured predicate/standard-Set model; not runtime Set membership or state reachability proof")
        witnesses = []
        for record in transition.get("status_patch_facts", []):
            if record["status"] not in excluded and record["status"] != status_literals[0]:
                witnesses.append(record)
        domain.update(source_patch_difference_witnesses=witnesses[:_SAMPLE],
            source_patch_difference_witness_count=len(witnesses), source_patch_difference_witnesses_truncated=len(witnesses) > _SAMPLE)
    outer_keys = {tuple(value) for value in predicates.get("outer_key_field_paths", [])}
    outer_keys.update(tuple(value) for value in facade.get("preselection_field_paths", []))
    inner_keys = {tuple(value) for value in predicates.get("authority_key_source", {}).get("field_paths", [])}
    key_difference = sorted(inner_keys - outer_keys)
    return {"authority_region_state": "source_backed_protocol_model" if protected else "unknown",
        "facade_check_outside_selected_authority_callback": outside,
        "outside_is_not_proof_of_no_outer_protection": True,
        "relation_scope": "selected facade/authority source regions under declared default assembly and protocol; not a proved whole execution chain",
        "assembly_state": assembly.get("state", "unknown"), "facade_to_authority_execution_chain_proved": False,
        "status_domain": domain,
        "key_structure": {"outer_comparison_field_paths": [list(value) for value in sorted(outer_keys)],
            "authority_key_field_paths": [list(value) for value in sorted(inner_keys)],
            "authority_extra_source_field_reads": [list(value) for value in key_difference],
            "structure_differs": bool(key_difference) if predicates.get("authority_key_source", {}).get("origin_model_closed")
                and predicates.get("outer_control_pattern_closed") and facade.get("preselection_structure_complete") else None,
            "semantic_key_equality_proof": False},
        "bounded_interleaving": False, "interleaving_inferred": False,
        "runtime_duplicate_proof": False, "all_writers_scope_closed": False}


def _finding(snapshot: GraphSnapshot, rule: dict, facts: dict, issues: list[dict], documents: dict[str, Any],
             node_ids: set[str] | None = None, edge_ids: set[str] | None = None) -> Finding:
    fingerprint = _digest({"project": snapshot.project_id, "version": VERSION, "policy_version": POLICY_VERSION, "rule": rule})
    comparison = facts.get("comparison", {})
    source_fact = comparison.get("facade_check_outside_selected_authority_callback") is True
    details = {"schema": "callscope.atomicity-evidence.v1", "analyzer_version": VERSION,
        "policy_version": POLICY_VERSION, "snapshot_id": snapshot.id, "source_hash": snapshot.source_hash,
        "shared_model_versions": {"completion": COMPLETION_VERSION, "builtin_environment": ENVIRONMENT_VERSION},
        "policy_hash": snapshot.policy_hash, "contract_hash": _digest(rule), "source_facts": facts,
        "protocol_model": rule.get("protection"), "resource_mapping": rule.get("resource"),
        "provenance": rule.get("provenance"), "applicability": rule.get("applicability"),
        "unknown_count": len(issues), "unknown_samples": issues[:64], "unknown_truncated": len(issues) > 64,
        "captured_source_inputs": [{"file": path, "source_hash": doc.source.hash, "status": doc.source.status,
            "parser_version": doc.parser_version, "parse_provenance": getattr(doc, "parse_provenance", {})}
            for path, doc in sorted(documents.items())],
        "analysis_scope": {"source_only": True, "protocol_semantics_conditional": True,
            "bounded_interleaving": False, "interleaving_inferred": False, "runtime_duplicate_proof": False,
            "target_code_executed": False, "lock_correctness_verified": False, "all_writer_or_outer_serialization_proof": False,
            "source_doc_is_label_only": True},
        "counterevidence": {"facade_existing_guard_early_exit": facts.get("facade", {}).get("existing_guard_early_exit", []),
            "authority_locked_existing_entry_reuse": facts.get("authority", {}).get("early_existing_reuse", []),
            "facade_read_catch_fallback": facts.get("facade", {}).get("read_catch_fallback", []),
            "dependency_override": facts.get("dependency_assembly", {})}}
    locations = [doc.location(doc.tree.root_node) for doc in documents.values()]
    description = "从捕获 AST 提取检查次序、callback/resource映射、取得guard、锁内读写及谓词出处；结果依赖显式资源/协议条件。未推导并发交错或运行重复。"
    evidence = Evidence(id=_digest({"snapshot": snapshot.id, "fingerprint": fingerprint, "details": details})[:24],
        kind="static_atomicity_analysis", message=description, locations=locations, node_ids=sorted(node_ids or []),
        edge_ids=sorted(edge_ids or []), details=details)
    return Finding(id=_digest({"snapshot": snapshot.id, "fingerprint": fingerprint})[:24],
        type="static_atomicity_protected_deduplication", severity=rule.get("severity", "medium"), status="uncertain",
        title="查重检查区域与权威谓词口径待复核" if source_fact else "查重保护模型无法完整确认",
        description=description, evidence=[evidence], rule_id=rule.get("id", "invalid-atomicity-rule"),
        node_ids=sorted(node_ids or []), edge_ids=sorted(edge_ids or []),
        fingerprint=fingerprint, snapshot_id=snapshot.id,
        metadata={"atomicity_analyzer_version": VERSION, "atomicity_policy_version": POLICY_VERSION,
            "shared_model_versions": {"completion": COMPLETION_VERSION, "builtin_environment": ENVIRONMENT_VERSION},
            "contract_hash": _digest(rule), "provenance": rule.get("provenance", {}),
            "applicability": rule.get("applicability", {}), "source_fact_confirmed": source_fact,
            "authority_region_state": comparison.get("authority_region_state", "unknown"),
            "relation_scope": comparison.get("relation_scope"), "assembly_state": comparison.get("assembly_state"),
            "facade_to_authority_execution_chain_proved": False,
            "bounded_interleaving": False, "interleaving_inferred": False, "runtime_proof": False})


def analyze_atomicity_contracts(snapshot: GraphSnapshot, rules: list[dict]) -> list[Finding]:
    """Return conditional source evidence; no result is a runtime atomicity pass."""
    if not isinstance(snapshot, GraphSnapshot):
        raise ValueError("atomicity analysis requires a captured GraphSnapshot")
    if not isinstance(rules, list) or len(rules) > 256:
        return [_finding(snapshot, {"id": "invalid-atomicity-rules", "severity": "info"}, {},
            [{"code": "atomicity_rules_invalid", "message": "原子合同需要最多256项JSON列表。"}], {})]
    from .semantic_sources import SemanticSources
    sources = SemanticSources(snapshot)
    ids = [rule.get("id") for rule in rules if isinstance(rule, dict)]
    findings = []
    for index, rule in enumerate(rules):
        try:
            validate_atomicity_rule(rule)
            if ids.count(rule["id"]) != 1:
                raise ValueError("原子合同 id 重复，不能覆盖前一条。")
        except (ValueError, TypeError, RecursionError, OverflowError) as exc:
            findings.append(_finding(snapshot, {"id": f"invalid-atomicity-rule-{index}", "severity": "info"}, {},
                [{"code": "atomicity_rule_invalid", "message": str(exc)[:1000]}], {}))
            continue
        context = _Analysis(snapshot, sources)
        facade = _facade(context, rule)
        assembly = _assembly(context, rule)
        if (assembly.get("state") == "policy_declared" or any(call.get("binding_state") != "snapshot_resolved"
                for role, call in facade.get("calls", {}).items() if role in {"read", "write"})):
            context.issue("atomicity_dependency_assembly_unresolved", "装配默认候选或 deps 动态实际目标未闭合；所选源码区域差异不证明 facade 到该 authority 的整条执行链。")
        wrapper_facts, wrappers_complete = _wrappers(context, rule)
        lifecycle, lifecycle_complete = _lifecycle(context, rule)
        authority = _authority(context, rule)
        predicates = _predicates(context, rule)
        transition = _transition(context, rule)
        comparison = _compare(facade, authority, predicates, lifecycle_complete, wrappers_complete, transition, assembly)
        context.issue("atomicity_external_protocol_conditions", "资源物理身份、目录锁正确性、外层串行/唯一性、部署依赖和实际调度未证明；保留条件。")
        facts = {"facade": facade, "dependency_assembly": assembly, "wrapper_forwarding": wrapper_facts,
            "lifecycle": lifecycle, "authority": authority, "predicates": predicates,
            "transition": transition, "comparison": comparison}
        findings.append(_finding(snapshot, rule, facts, context.issues, context.documents, context.node_ids, context.edge_ids))
    return findings
