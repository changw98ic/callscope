"""Data-only static contracts over captured source; no target code is executed.

This first implementation checks declaration initializer string members and
literal object field construction. It does not infer runtime values, business
equivalence, cross-language reachability, or transaction semantics.

Public interface: analyze_contracts(snapshot, rules) -> list[Finding].
Selectors always combine a captured file path with an exact lexical symbol.
Source-document paths in provenance are labels only and are never opened.
"""

from dataclasses import dataclass
import hashlib
import json
import re
from typing import Any

from .models import Evidence, Finding, GraphSnapshot, SourceFile
from .parsers import language_parser, parser_version


CONTRACT_ANALYZER_VERSION = "static-contracts-1"
CONTRACT_POLICY_VERSION = "static-contract-policy-v1"
_SOURCE_STATUSES = frozenset({"parsed", "complete", "ok", "analyzed"})
_FUNCTIONS = frozenset({
    "function_declaration", "generator_function_declaration",
    "function_expression", "generator_function", "arrow_function",
    "method_definition", "function_item", "closure_expression",
})
_DEFINITIONS = frozenset({
    "function_declaration", "generator_function_declaration",
    "method_definition", "function_item", "variable_declarator", "const_item",
    "static_item",
})
_CLASS_SCOPES = frozenset({"class_declaration", "class", "internal_module"})
_SEVERITIES = frozenset({"high", "medium", "low", "info"})
_TS_LANGUAGES = frozenset({"typescript", "javascript", "tsx", "jsx", "ts", "js"})
_ERASED_WRAPPERS = frozenset({
    "parenthesized_expression", "as_expression", "satisfies_expression",
    "non_null_expression",
})
_ALLOWED_REFERENCE_KEYS = frozenset({
    "file", "symbol", "node_type", "text", "enclosing_condition", "branch", "role",
})
_LAYOUT = re.compile(r'''("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|//[^\n]*|/\*[\s\S]*?\*/|\s+)''')


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, ensure_ascii=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")).hexdigest()


def _issue(code: str, message: str, file: str = "", line: int = 0) -> dict:
    return {"code": code, "message": message, "file": file, "line": line}


def _path(value: Any) -> bool:
    return (
        isinstance(value, str) and bool(value)
        and not value.startswith("/") and "\\" not in value and "\x00" not in value
        and all(part not in {"", ".", ".."} for part in value.split("/"))
    )


def _string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and "\x00" not in value


def _content_hash(content: str) -> str | None:
    try:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()
    except UnicodeEncodeError:
        return None


def _validate_selector(value: Any, site: str | None = None) -> None:
    keys = {"file", "symbol"} if site is None else {"file", "symbol", "site"}
    if site == "return":
        keys.add("object_path")
    if not isinstance(value, dict) or set(value) - keys:
        raise ValueError("源码选择器只能包含 file、symbol 和对应的静态 site/object_path。")
    if not _path(value.get("file")) or not _string(value.get("symbol")):
        raise ValueError("选择器需要项目内相对文件路径与非空词法 symbol。")
    if site is not None and value.get("site") != site:
        raise ValueError(f"此规则只支持 site={site}。")
    if "object_path" in value:
        parts = value["object_path"]
        if not isinstance(parts, list) or len(parts) > 32 or not all(_string(part) for part in parts):
            raise ValueError("object_path 必须是静态字段名数组。")


def _validate_reference(value: Any) -> None:
    if not isinstance(value, dict) or set(value) - _ALLOWED_REFERENCE_KEYS:
        raise ValueError("源码依据只接受固定 file/symbol/node_type/text/condition/branch/role。")
    _validate_selector({key: value.get(key) for key in ("file", "symbol")})
    if not _string(value.get("node_type")) or not _string(value.get("text")):
        raise ValueError("源码依据必须提供 AST node_type 与字面 text。")
    if value.get("branch") not in {None, "then", "else"}:
        raise ValueError("branch 仅支持 then 或 else。")
    if "enclosing_condition" in value and not _string(value["enclosing_condition"]):
        raise ValueError("enclosing_condition 必须是非空源码条件文本。")
    if "role" in value and value["role"] not in {"guard", "counterexample", "context"}:
        raise ValueError("源码依据 role 必须为 guard/counterexample/context。")


def _validate_rule(rule: Any) -> None:
    if not isinstance(rule, dict):
        raise ValueError("每条静态合同必须是 JSON 对象。")
    # Reject callables, class instances, NaN, and any non-JSON rule values.
    json.dumps(rule, ensure_ascii=True, allow_nan=False)
    common = {"id", "type", "severity", "provenance", "applicability", "source_evidence"}
    kind = rule.get("type")
    special = (
        {"reference", "subject", "relation"} if kind == "literal_set_consistency"
        else {"subject", "required_fields", "evaluation"} if kind == "required_object_fields"
        else set()
    )
    if kind not in {"literal_set_consistency", "required_object_fields"}:
        raise ValueError("不支持的静态合同类型；首批仅包含集合初始化与对象字段。")
    if set(rule) - common - special or not _string(rule.get("id")):
        raise ValueError("规则有未知配置字段或缺少 id。")
    if rule.get("severity", "medium") not in _SEVERITIES:
        raise ValueError("severity 必须为 high/medium/low/info。")
    provenance = rule.get("provenance")
    if (
        not isinstance(provenance, dict)
        or set(provenance) - {"authority", "reviewer", "author_approved", "source_doc", "note"}
        or not _string(provenance.get("authority"))
        or not _string(provenance.get("source_doc"))
        or not isinstance(provenance.get("author_approved"), bool)
    ):
        raise ValueError("provenance 需要 authority、author_approved 和仅作标签的 source_doc。")
    applicability = rule.get("applicability")
    if (
        not isinstance(applicability, dict)
        or set(applicability) - {"kind", "conditions", "counterexamples", "guard"}
        or applicability.get("kind") not in {"unconditional", "conditional"}
    ):
        raise ValueError("applicability 必须明确 unconditional 或 conditional。")
    for field in ("conditions", "counterexamples"):
        values = applicability.get(field, [])
        if not isinstance(values, list) or not all(_string(item) for item in values):
            raise ValueError(f"applicability.{field} 必须是非空说明字符串数组。")
    if applicability["kind"] == "conditional" and not applicability.get("conditions"):
        raise ValueError("条件合同必须记录外部适用前提，不能省略为普遍必填。")
    if "guard" in applicability:
        _validate_reference(applicability["guard"])
    references = rule.get("source_evidence", [])
    if not isinstance(references, list) or len(references) > 64:
        raise ValueError("source_evidence 必须是最多 64 项的源码 AST 选择器。")
    for reference in references:
        _validate_reference(reference)
    if kind == "literal_set_consistency":
        _validate_selector(rule.get("reference"), "initializer")
        _validate_selector(rule.get("subject"), "initializer")
        if rule.get("relation") != "equal":
            raise ValueError("首批集合合同只支持声明初始化成员集合 equal。")
    else:
        _validate_selector(rule.get("subject"), "return")
        if rule.get("evaluation") != "all_direct_returns":
            raise ValueError("对象规则必须声明 all_direct_returns 的语法覆盖范围。")
        fields = rule.get("required_fields")
        if (
            not isinstance(fields, list) or not 1 <= len(fields) <= 64
            or not all(_string(field) for field in fields) or len(set(fields)) != len(fields)
        ):
            raise ValueError("required_fields 需要 1 至 64 个不同的静态字段名。")


def _walk(node: Any, skip_functions: bool = False):
    stack = [node]
    while stack:
        current = stack.pop()
        yield current
        if skip_functions and current != node and current.type in _FUNCTIONS:
            continue
        stack.extend(reversed(current.named_children))


def _unwrap(node: Any) -> Any:
    while node is not None and node.type in _ERASED_WRAPPERS:
        node = node.child_by_field_name("expression") or next(
            (child for child in node.named_children if child.type != "comment"), None,
        )
    return node


def _compact(text: str) -> str:
    # Literal selectors compare AST text, ignoring layout/comments outside strings.
    return _LAYOUT.sub(lambda match: match.group(0) if match.group(0).startswith(
        ('"', "'"),
    ) else "", text)


def _literal_string(raw: str) -> str | None:
    """Decode fixed JavaScript string escapes without evaluating expressions."""
    if len(raw) < 2 or raw[0] not in {'"', "'"} or raw[-1] != raw[0]:
        return None
    raw = raw[1:-1]
    output: list[str] = []
    index = 0
    escapes = {"b": "\b", "f": "\f", "n": "\n", "r": "\r", "t": "\t", "v": "\v"}
    while index < len(raw):
        char = raw[index]
        if char != "\\":
            output.append(char)
            index += 1
            continue
        index += 1
        if index >= len(raw):
            return None
        char = raw[index]
        index += 1
        if char in escapes:
            output.append(escapes[char])
        elif char == "0":
            if index < len(raw) and raw[index].isdigit():
                return None
            output.append("\0")
        elif char in {"\n", "\r"}:
            if char == "\r" and index < len(raw) and raw[index] == "\n":
                index += 1
        elif char in {"x", "u"}:
            length = 2 if char == "x" else 4
            if char == "u" and index < len(raw) and raw[index] == "{":
                end = raw.find("}", index + 1)
                if end < 0:
                    return None
                digits = raw[index + 1:end]
                index = end + 1
            else:
                digits = raw[index:index + length]
                index += length
                if len(digits) != length:
                    return None
            if not digits or not all(digit in "0123456789abcdefABCDEF" for digit in digits):
                return None
            codepoint = int(digits, 16)
            if codepoint > 0x10FFFF:
                return None
            output.append(chr(codepoint))
        elif char.isdigit():
            return None  # Legacy octal escapes are outside the first contract grammar.
        else:
            output.append(char)
    value = "".join(output)
    # Normalize JS UTF-16 surrogate pairs to the same Unicode string spelling.
    try:
        return value.encode("utf-16-le", "surrogatepass").decode("utf-16-le")
    except UnicodeDecodeError:
        return None


@dataclass
class _Definition:
    symbol: str
    local_name: str
    node: Any
    value: Any
    callable: bool


class _Document:
    def __init__(self, source: SourceFile, kind: str):
        self.source = source
        self.data = source.content.encode("utf-8")
        self.lines = source.content.splitlines()
        self.kind = kind
        self.parser_version = parser_version(kind)
        self.tree = language_parser(kind).parse(self.data)
        self.definitions: dict[str, list[_Definition]] = {}
        for node in _walk(self.tree.root_node):
            if node.type not in _DEFINITIONS:
                continue
            name = node.child_by_field_name("name")
            if name is None or name.type not in {"identifier", "property_identifier", "type_identifier"}:
                continue
            local_name = self.text(name)
            scope = self._scope(node)
            symbol = ".".join([*scope, local_name])
            value = node.child_by_field_name("value")
            is_callable = node.type in _FUNCTIONS or (
                value is not None and _unwrap(value).type in _FUNCTIONS
            )
            definition = _Definition(symbol, local_name, node, value, is_callable)
            self.definitions.setdefault(symbol, []).append(definition)

    def text(self, node: Any) -> str:
        return self.data[node.start_byte:node.end_byte].decode("utf-8")

    def _scope(self, node: Any) -> list[str]:
        scopes = []
        parent = node.parent
        while parent is not None:
            if parent.type == "impl_item":
                scope = parent.child_by_field_name("type")
                if scope is not None:
                    scopes.append(self.text(scope))
            elif parent.type in _CLASS_SCOPES or parent.type in _FUNCTIONS:
                name = parent.child_by_field_name("name")
                if name is not None:
                    scopes.append(self.text(name))
                elif parent.type in _FUNCTIONS:
                    owner = parent.parent
                    name = owner.child_by_field_name("name") if owner is not None else None
                    if owner is not None and owner.type == "variable_declarator" and name is not None:
                        scopes.append(self.text(name))
                    else:
                        scopes.append(f"<anonymous@{parent.start_point.row + 1}:{parent.start_point.column + 1}>")
            parent = parent.parent
        return list(reversed(scopes))

    def location(self, node: Any) -> dict:
        excerpt = self.data[node.start_byte:node.end_byte]
        return {
            "file": self.source.path, "line": node.start_point.row + 1,
            "column": node.start_point.column + 1, "end_line": node.end_point.row + 1,
            "end_column": node.end_point.column + 1, "column_unit": "utf8_bytes",
            "source_hash": self.source.hash,
            "grammar": self.kind, "parser_version": self.parser_version,
            "span_hash": hashlib.sha256(excerpt).hexdigest(),
            "source_line": self.lines[node.start_point.row] if node.start_point.row < len(self.lines) else "",
            "source_excerpt": excerpt[:4096].decode("utf-8", "ignore"),
            "source_excerpt_truncated": len(excerpt) > 4096,
        }


class _Sources:
    def __init__(self, snapshot: GraphSnapshot):
        self.snapshot = snapshot
        self.files: dict[str, list[SourceFile]] = {}
        for source in snapshot.files:
            self.files.setdefault(source.path, []).append(source)
        self.cache: dict[str, tuple[_Document | None, list[dict]]] = {}

    def load(self, path: str) -> tuple[_Document | None, list[dict]]:
        if path in self.cache:
            return self.cache[path]
        files = self.files.get(path, [])
        if len(files) != 1:
            result = (None, [_issue("source_not_unique", f"快照中此文件匹配 {len(files)} 项，无法唯一定位。", path)])
        else:
            source = files[0]
            if source.status not in _SOURCE_STATUSES:
                result = (None, [_issue("source_not_parsed", f"快照文件状态 {source.status}：{source.error or '未完成静态解析'}", path)])
            elif not isinstance(source.content, str):
                result = (None, [_issue("source_content_invalid", "快照没有可解析的文本源码。", path)])
            elif _content_hash(source.content) is None or _content_hash(source.content) != source.hash:
                result = (None, [_issue("source_hash_mismatch", "保存文本编码或文件哈希不一致，拒绝作为静态合同依据。", path)])
            else:
                language = str(source.language).lower()
                kind = "tsx" if path.endswith((".tsx", ".jsx")) else "typescript" if language in _TS_LANGUAGES else "rust" if language == "rust" else ""
                if not kind:
                    result = (None, [_issue("unsupported_contract_language", "首批合同 AST 前端仅支持 TypeScript/JavaScript 与 Rust 来源。", path)])
                else:
                    try:
                        document = _Document(source, kind)
                        if document.tree.root_node.has_error:
                            errors = [node for node in _walk(document.tree.root_node) if node.is_error or node.is_missing]
                            locations = [document.location(node) for node in errors[:20]]
                            problem = _issue("contract_parse_error", "AST 存在语法错误；不作封闭集合或对象的负向证明。", path)
                            problem.update(error_count=len(errors), error_samples=locations, samples_truncated=len(errors) > 20)
                            result = (None, [problem])
                        else:
                            result = (document, [])
                    except Exception as exc:
                        result = (None, [_issue("contract_parser_unavailable", f"固定语法解析失败：{type(exc).__name__}: {str(exc)[:300]}", path)])
        self.cache[path] = result
        return result

    def select(self, selector: dict) -> tuple[_Document | None, _Definition | None, list[dict]]:
        document, problems = self.load(selector["file"])
        if document is None:
            return None, None, problems
        definitions = document.definitions.get(selector["symbol"], [])
        if len(definitions) != 1:
            return document, None, [_issue(
                "symbol_not_unique",
                f"词法符号 {selector['symbol']} 匹配 {len(definitions)} 个定义，不能选取某个同名定义代替。",
                selector["file"],
            )]
        return document, definitions[0], []


def _branch_conditions(document: _Document, node: Any, boundary: Any) -> list[dict]:
    conditions = []
    parent = node.parent
    while parent is not None and parent != boundary:
        if parent.type in {"if_statement", "if_expression"}:
            condition = parent.child_by_field_name("condition")
            consequence = parent.child_by_field_name("consequence")
            alternative = parent.child_by_field_name("alternative")
            branch = (
                "then" if consequence is not None and consequence.start_byte <= node.start_byte < consequence.end_byte
                else "else" if alternative is not None and alternative.start_byte <= node.start_byte < alternative.end_byte
                else "condition"
            )
            if condition is not None:
                conditions.append({"text": document.text(condition), "branch": branch, "location": document.location(condition)})
        parent = parent.parent
    return conditions


def _source_reference(sources: _Sources, selector: dict) -> tuple[dict | None, list[dict]]:
    document, definition, problems = sources.select(selector)
    if document is None or definition is None:
        return None, problems
    candidates = [
        node for node in _walk(definition.node, skip_functions=True)
        if node.type == selector["node_type"] and _compact(document.text(node)) == _compact(selector["text"])
    ]
    if "enclosing_condition" in selector or "branch" in selector:
        expected = _compact(selector.get("enclosing_condition", ""))
        candidates = [
            node for node in candidates if any(
                (not expected or _compact(condition["text"]) == expected)
                and (not selector.get("branch") or condition["branch"] == selector["branch"])
                for condition in _branch_conditions(document, node, definition.node)
            )
        ]
    if len(candidates) != 1:
        return None, [_issue("source_reference_not_unique", f"此 AST 源码依据匹配 {len(candidates)} 项，守卫/反证尚未唯一定位。", selector["file"])]
    node = candidates[0]
    return {
        "role": selector.get("role", "context"), "symbol": definition.symbol,
        "node_type": node.type, "location": document.location(node),
        "enclosing_conditions": _branch_conditions(document, node, definition.node),
        "interpretation": "此处仅确认保存源码中存在该语法与条件，不证明生产者会进入这个分支。",
    }, []


def _constructor_unknown(document: _Document, definition: _Definition) -> list[dict]:
    """Conservatively fence local bindings and visible constructor replacement."""
    problems = []
    ancestors = set()
    parent = definition.node
    while parent is not None:
        ancestors.add((parent.type, parent.start_byte, parent.end_byte))
        parent = parent.parent
    for node in _walk(document.tree.root_node):
        if (node.type in _DEFINITIONS - {"method_definition"}) or node.type in _CLASS_SCOPES or node.type == "enum_declaration":
            name = node.child_by_field_name("name")
            binds_set = name is not None and (
                document.text(name) == "Set" or "\\" in document.text(name) or any(
                    child.type in {"identifier", "shorthand_property_identifier_pattern"}
                    and (document.text(child) == "Set" or "\\" in document.text(child)) for child in _walk(name)
                )
            )
            if binds_set:
                scope = node.parent
                # var bindings are function-scoped even inside a child block.
                scope_types = {"program", *_FUNCTIONS}
                if scope is None or scope.type != "variable_declaration":
                    scope_types.add("statement_block")
                while scope is not None and scope.type not in scope_types:
                    scope = scope.parent
                if scope is not None and (scope.type, scope.start_byte, scope.end_byte) in ancestors:
                    problems.append(_issue("set_constructor_binding", "可见声明可能绑定 Set 或包含未解析转义标识符，不确定是内建构造器。", document.source.path, node.start_point.row + 1))
        elif node.type in {"import_specifier", "namespace_import", "import_clause"}:
            alias = node.child_by_field_name("alias") or node.child_by_field_name("name")
            if alias is not None and (document.text(alias) == "Set" or "\\" in document.text(alias)):
                problems.append(_issue("set_constructor_binding", "Set 来自模块绑定，首批规则不展开构造器实现。", document.source.path, node.start_point.row + 1))
            elif node.type in {"namespace_import", "import_clause"} and any(
                child.type == "identifier" and (document.text(child) == "Set" or "\\" in document.text(child)) for child in node.named_children
            ):
                problems.append(_issue("set_constructor_binding", "存在默认/命名空间 Set 导入，无法保证内建构造器。", document.source.path, node.start_point.row + 1))
        elif node.type in {"assignment_expression", "augmented_assignment_expression"}:
            left = node.child_by_field_name("left")
            if left is not None and (
                _compact(document.text(left)) in {"Set", "globalThis.Set", "window.Set"}
                or any(child.type in {"identifier", "property_identifier"} and "\\" in document.text(child) for child in _walk(left))
            ):
                problems.append(_issue("set_constructor_assignment", "保存源码中存在 Set 构造器赋值；不据初始化文本断言完整构造器行为。", document.source.path, node.start_point.row + 1))
    # Parameters can shadow Set without a declaration node.
    parent = definition.node.parent
    while parent is not None:
        if parent.type in _FUNCTIONS or parent.type == "catch_clause":
            parameters = parent.child_by_field_name("parameters") or parent.child_by_field_name("parameter")
            if parameters is not None and any(
                node.type in {"identifier", "shorthand_property_identifier_pattern"} and document.text(node) == "Set"
                or node.type in {"identifier", "shorthand_property_identifier_pattern"} and "\\" in document.text(node)
                for node in _walk(parameters)
            ):
                problems.append(_issue("set_constructor_parameter", "外层参数可能绑定 Set，构造器来源未知。", document.source.path, parent.start_point.row + 1))
        parent = parent.parent
    return problems


def _initializer_members(sources: _Sources, selector: dict) -> tuple[dict | None, list[dict]]:
    document, definition, problems = sources.select(selector)
    if document is None or definition is None:
        return None, problems
    if document.kind not in {"typescript", "tsx"}:
        return None, [_issue("unsupported_initializer_language", "首批封闭字符串成员初始化仅支持 TS/JS 数组和 Set 语法。", selector["file"])]
    value = _unwrap(definition.value)
    if value is None:
        return None, [_issue("initializer_missing", "符号没有可读的声明初始化表达式。", selector["file"])]
    container = "array_literal"
    if value.type == "new_expression":
        constructor = value.child_by_field_name("constructor")
        arguments = value.child_by_field_name("arguments")
        arguments = [node for node in arguments.named_children if node.type != "comment"] if arguments is not None else []
        if constructor is None or document.text(constructor) != "Set" or len(arguments) != 1:
            return None, [_issue("initializer_constructor_unknown", "只识别单参数、无未知构造器的 Set 语法初始化。", selector["file"], value.start_point.row + 1)]
        problems.extend(_constructor_unknown(document, definition))
        value = _unwrap(arguments[0])
        container = "set_constructor_syntax"
    if value is None or value.type != "array":
        return None, [*problems, _issue("initializer_not_literal_array", "初始化使用别名、调用或其他动态表达式，成员集合不封闭。", selector["file"])]
    values = []
    for node in value.named_children:
        if node.type == "comment":
            continue
        literal = _literal_string(document.text(node)) if node.type == "string" else None
        if literal is None:
            problems.append(_issue("initializer_dynamic_member", "数组存在非字符串字面元素、模板表达式或展开，不能忽略为完整集合。", selector["file"], node.start_point.row + 1))
        else:
            values.append(literal)
    # Sparse arrays have unnamed commas without an intervening element.
    previous = "["
    for child in value.children:
        if child.type == "comment":
            continue
        if child.type == "," and previous in {"[", ","}:
            problems.append(_issue("initializer_sparse_array", "稀疏数组包含隐式 undefined，不是封闭字符串成员集合。", selector["file"], child.start_point.row + 1))
        previous = child.type
    return {
        "file": selector["file"], "symbol": definition.symbol, "container": container,
        "members": sorted(set(values)), "literal_element_count": len(values),
        "closed": not problems, "location": document.location(definition.node),
        "interpretation": "仅表示声明初始化语法中的字符串成员，不证明运行时 Set/数组不被修改或全局构造器不被替换。",
    }, problems


def _object_properties(document: _Document, node: Any) -> tuple[dict[str, Any], list[dict]]:
    node = _unwrap(node)
    if node is None or node.type != "object":
        return {}, [_issue("return_object_unknown", "返回值或嵌套路径是别名、调用、条件表达式等非字面对象。", document.source.path)]
    properties = {}
    problems = []
    for member in node.named_children:
        if member.type == "comment":
            continue
        if member.type == "pair":
            key = member.child_by_field_name("key")
            value = member.child_by_field_name("value")
            name = (
                document.text(key) if key is not None and key.type in {"property_identifier", "identifier"} and "\\" not in document.text(key)
                else _literal_string(document.text(key)) if key is not None and key.type == "string"
                else None
            )
        elif member.type == "shorthand_property_identifier":
            # A shorthand has a fixed key. Its value remains opaque; it cannot
            # satisfy a deeper object_path without a literal object definition.
            name, value = (None if "\\" in document.text(member) else document.text(member)), member
        else:
            name, value = None, None
        if name is None or name == "__proto__":
            problems.append(_issue("object_dynamic_shape", "对象含展开、computed/转义标识符 key、getter/method 或特殊原型构造，字段形状未封闭。", document.source.path, member.start_point.row + 1))
        elif name in properties:
            problems.append(_issue("object_duplicate_key", f"对象重复构造字段 {name}，不能选择某个定义作封闭形状证明。", document.source.path, member.start_point.row + 1))
        else:
            properties[name] = value
    return properties, problems


def _terminates(node: Any, depth: int = 0) -> bool:
    if node is None or depth > 64:
        return False
    if node.type in {"return_statement", "throw_statement"}:
        return True
    if node.type in {"statement_block", "block"}:
        return any(_terminates(child, depth + 1) for child in node.named_children if child.type != "comment")
    if node.type == "if_statement":
        consequence = node.child_by_field_name("consequence")
        alternative = node.child_by_field_name("alternative")
        return _terminates(consequence, depth + 1) and _terminates(alternative, depth + 1)
    # Loops, switch, try/finally and other complex flow retain unknown coverage.
    return False


def _return_shapes(sources: _Sources, selector: dict) -> tuple[list[dict], list[dict]]:
    document, definition, problems = sources.select(selector)
    if document is None or definition is None:
        return [], problems
    if document.kind not in {"typescript", "tsx"} or not definition.callable:
        return [], [_issue("return_scope_unsupported", "首批对象字段规则需要唯一 TS/JS 函数、方法或函数绑定。", selector["file"])]
    callable_node = _unwrap(definition.value) if definition.node.type == "variable_declarator" else definition.node
    body = callable_node.child_by_field_name("body")
    if body is None:
        return [], [_issue("function_body_missing", "函数只有声明或未捕获实现，不能空集合判定字段满足。", selector["file"])]
    returns = [node for node in _walk(body, skip_functions=True) if node.type == "return_statement"]
    if callable_node.type == "arrow_function" and body.type != "statement_block":
        returns = [body]
    elif not _terminates(body):
        problems.append(_issue("implicit_return_unknown", "不能排除正常执行隐式 fallthrough 或复杂控制流；不声称覆盖所有运行返回。", selector["file"], body.start_point.row + 1))
    if not returns:
        problems.append(_issue("no_direct_returns", "词法函数没有直接返回对象；零返回、仅 throw 或隐式返回不能判通过。", selector["file"], callable_node.start_point.row + 1))
    shapes = []
    for returned in returns:
        value = next((node for node in returned.named_children if node.type != "comment"), None) if returned.type == "return_statement" else returned
        value = _unwrap(value)
        local_problems = []
        for field in selector.get("object_path", []):
            properties, current = _object_properties(document, value)
            local_problems.extend(current)
            if current:
                value = None
                break
            if field not in properties:
                local_problems.append(_issue("object_path_missing", f"返回字面对象未构造选定嵌套路径字段 {field}，无法取得目标对象形状。", selector["file"], returned.start_point.row + 1))
                value = None
                break
            value = _unwrap(properties[field])
        if value is not None:
            properties, current = _object_properties(document, value)
            local_problems.extend(current)
        else:
            properties = {}
            if not local_problems:
                local_problems.append(_issue("return_value_missing", "直接 return 没有可读字面值。", selector["file"], returned.start_point.row + 1))
        problems.extend(local_problems)
        shapes.append({
            "file": selector["file"], "symbol": definition.symbol,
            "object_path": selector.get("object_path", []),
            "fields": sorted(properties), "closed": not local_problems,
            "location": document.location(value if value is not None else returned),
            "return_location": document.location(returned),
            "enclosing_conditions": _branch_conditions(document, returned, callable_node),
            "interpretation": "仅检查对象源码构造字段名；字段值非空、类型与完整消费者校验不在此规则的证明范围。",
        })
    return shapes, problems


def _node_ids(snapshot: GraphSnapshot, locations: list[dict], symbols: list[str]) -> list[str]:
    files = {location["file"] for location in locations}
    result = []
    for node in snapshot.nodes:
        if node.file not in files:
            continue
        if any(node.qualname == symbol or node.id.endswith("#" + symbol) for symbol in symbols):
            result.append(node.id)
    return sorted(set(result))


def _finding(snapshot: GraphSnapshot, rule: dict, fact: dict, problems: list[dict], refs: list[dict]) -> Finding:
    conditional = rule.get("applicability", {}).get("kind") == "conditional"
    kind = rule.get("type", "rule_configuration")
    rule_id = rule.get("id", "invalid-contract-rule")
    provenance = rule.get("provenance", {})
    applicability = rule.get("applicability", {})
    fingerprint = _digest({
        "analyzer": CONTRACT_ANALYZER_VERSION, "rule_id": rule_id, "type": kind,
        "contract": rule, "project_id": snapshot.project_id,
    })
    locations = [
        value["location"] for value in (
            [fact.get("reference"), fact.get("subject")]
            + fact.get("returns", []) + refs
        ) if isinstance(value, dict) and isinstance(value.get("location"), dict)
    ]
    symbols = [
        value["symbol"] for value in [fact.get("reference"), fact.get("subject"), *fact.get("returns", []), *refs]
        if isinstance(value, dict) and isinstance(value.get("symbol"), str)
    ]
    node_ids = _node_ids(snapshot, locations, symbols)
    source_hashes = {source.path: source.hash for source in snapshot.files if source.path in {location["file"] for location in locations}}
    selected_paths = {
        selector["file"] for selector in [
            rule.get("reference"), rule.get("subject"),
            rule.get("applicability", {}).get("guard"), *rule.get("source_evidence", []),
        ] if isinstance(selector, dict) and isinstance(selector.get("file"), str)
    }
    source_inputs = [
        {"file": source.path, "source_hash": source.hash, "status": source.status,
         "language": source.language, "error": source.error}
        for source in snapshot.files if source.path in selected_paths
    ]
    unknown = list(problems)
    if conditional:
        unknown.append(_issue(
            "external_applicability_not_inferred",
            "合同适用条件属于显式外部假设；守卫存在不证明生产者一定进入该跨语言分支。",
            rule.get("subject", {}).get("file", ""),
        ))
    details = {
        "analyzer_version": CONTRACT_ANALYZER_VERSION, "snapshot_id": snapshot.id,
        "source_hash": snapshot.source_hash, "source_file_hashes": source_hashes,
        "captured_source_inputs": source_inputs,
        "snapshot_parser_version": snapshot.parser_version,
        "policy_hash": snapshot.policy_hash, "contract_hash": _digest(rule),
        "source_fact": fact,
        "contract_assumptions": applicability,
        "provenance": provenance,
        "guard_and_counterexample_sources": refs, "unknown": unknown,
        "analysis_scope": {
            "literal_sets": "declaration_initializer_closed_string_members",
            "objects": "all_syntax_direct_returns_excluding_nested_functions",
            "runtime_proof": False, "cross_language_branch_reachability": "not_inferred",
            "source_doc_is_label_only": True,
        },
    }
    if kind == "literal_set_consistency":
        title = "声明初始化字符串成员集合合同不一致" if fact.get("mismatch") else "集合初始化合同无法完整确认"
        description = "比较的是配置指定的两个声明初始化成员集合；不证明运行时集合恒定或业务终态等价。"
    elif kind == "required_object_fields":
        title = "返回字面对象未构造配置字段" if fact.get("missing") else "返回对象字段合同无法完整确认"
        description = "只确认保存源码的对象字段构造。"
        if conditional:
            description += " 必填条件由显式合同与守卫出处提供；生产者是否进入外部消费者分支尚未推导。"
    else:
        title, description = "静态合同配置无法应用", "规则校验失败，不能把缺少分析结果解释为满足合同。"
    if problems:
        description += " 解析、定位或形状覆盖存在未知，请查看证据。"
    evidence = Evidence(
        id=_digest({"snapshot": snapshot.id, "fingerprint": fingerprint, "details": details})[:24],
        kind="static_contract_analysis", message=description,
        locations=locations, node_ids=node_ids, details=details,
    )
    return Finding(
        id=_digest({"snapshot": snapshot.id, "fingerprint": fingerprint})[:24],
        type="static_contract_" + kind, severity=rule.get("severity", "medium"),
        status="uncertain" if conditional or problems else "open",
        title=title, description=description, node_ids=node_ids,
        evidence=[evidence], rule_id=rule_id, fingerprint=fingerprint,
        snapshot_id=snapshot.id,
        metadata={
            "contract_analyzer_version": CONTRACT_ANALYZER_VERSION,
            "contract_hash": _digest(rule), "provenance": provenance,
            "applicability": applicability,
            "source_fact_confirmed": bool(fact.get("mismatch") or fact.get("missing")),
            "runtime_proof": False,
        },
    )


def analyze_contracts(snapshot: GraphSnapshot, rules: list[dict[str, Any]]) -> list[Finding]:
    """Analyze only captured SourceFile content with fixed trusted grammars.

    Returns mismatches and explicit uncertain diagnostics, never a functional
    pass result. Conditional contracts always remain status='uncertain'.
    """
    if not isinstance(rules, list):
        return [_finding(snapshot, {"id": "invalid-contract-document", "type": "rule_configuration", "severity": "info"}, {}, [
            _issue("contract_rules_invalid", "analyze_contracts 的 rules 参数必须是规则数组。"),
        ], [])]
    sources = _Sources(snapshot)
    findings = []
    id_counts: dict[str, int] = {}
    for rule in rules:
        if isinstance(rule, dict) and isinstance(rule.get("id"), str):
            id_counts[rule["id"]] = id_counts.get(rule["id"], 0) + 1
    for index, rule in enumerate(rules):
        try:
            _validate_rule(rule)
            if id_counts[rule["id"]] != 1:
                raise ValueError("规则 id 重复；不能用后一个配置覆盖前一个。")
        except (ValueError, TypeError, OverflowError, RecursionError) as exc:
            invalid = {"id": f"invalid-contract-rule-{index}", "type": "rule_configuration", "severity": "info"}
            findings.append(_finding(snapshot, invalid, {"configuration_index": index}, [
                _issue("contract_rule_invalid", str(exc)),
            ], []))
            continue
        refs, problems = [], []
        references = list(rule.get("source_evidence", []))
        if rule["applicability"].get("guard"):
            references.insert(0, {**rule["applicability"]["guard"], "role": "guard"})
        for selector in references:
            reference, current = _source_reference(sources, selector)
            problems.extend(current)
            if reference is not None:
                refs.append(reference)
        if rule["type"] == "literal_set_consistency":
            reference, current = _initializer_members(sources, rule["reference"])
            problems.extend(current)
            subject, current = _initializer_members(sources, rule["subject"])
            problems.extend(current)
            closed = reference is not None and subject is not None and reference["closed"] and subject["closed"]
            expected, observed = (reference["members"] if reference else None), (subject["members"] if subject else None)
            mismatch = closed and expected != observed
            fact = {
                "reference": reference, "subject": subject, "expected": expected,
                "observed": observed, "mismatch": bool(mismatch),
                "missing_members": sorted(set(expected or []) - set(observed or [])) if closed else None,
                "additional_members": sorted(set(observed or []) - set(expected or [])) if closed else None,
                "interpretation": "初始化语法成员相等合同，不是运行时集合或业务状态机证明。",
            }
            if mismatch or problems:
                findings.append(_finding(snapshot, rule, fact, problems, refs))
        else:
            shapes, current = _return_shapes(sources, rule["subject"])
            problems.extend(current)
            required = rule["required_fields"]
            missing = []
            for shape in shapes:
                shape["missing_fields"] = sorted(set(required) - set(shape["fields"])) if shape["closed"] else None
                if shape["missing_fields"]:
                    missing.append({"location": shape["return_location"], "fields": shape["missing_fields"]})
            fact = {
                "expected": {"object_path": rule["subject"].get("object_path", []), "required_fields": required},
                "observed": [{"fields": shape["fields"], "closed": shape["closed"]} for shape in shapes],
                "returns": shapes, "direct_return_count": len(shapes), "missing": missing,
                "interpretation": "全体语法层直接返回对象的字段名构造；不等同于已执行路径或非空字段值。",
            }
            if missing or problems:
                findings.append(_finding(snapshot, rule, fact, problems, refs))
    return findings
