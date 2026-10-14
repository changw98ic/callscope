"""Read captured semantic source evidence without repository I/O or execution.

Trees are a view of saved source text, not a new call graph. TypeScript uses
the same narrowly authenticated syntax projection as its captured frontend;
all text, literals and spans still come from the original UTF-8 buffer.
Only an existing, unique, valid snapshot CALLS edge can identify a callee.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import hashlib
import json
from pathlib import PurePosixPath
from typing import Any

from .models import Edge, GraphSnapshot, Node, SourceFile
from .parsers import language_parser, parser_version
from .syntax_projection import PROJECTION_VERSION, grammar_errors, parse_with_projection

VERSION = SEMANTIC_SOURCE_VERSION = "semantic-snapshot-sources-1"
_TS_LANGUAGES = {"typescript", "javascript", "tsx", "jsx", "ts", "js"}
_FUNCTIONS = {"function_declaration", "generator_function_declaration",
    "function_expression", "generator_function", "arrow_function",
    "method_definition", "function_item", "closure_expression"}
_DEFINITIONS = {"function_declaration", "generator_function_declaration",
    "method_definition", "function_item", "variable_declarator", "const_item", "static_item"}
_NODE_GAPS = {"duplicate_definition", "multiple_module_contexts", "conditional_definition",
    "attribute_macros_unknown", "declaration_only", "binding_uncertain", "module_identity_collision"}


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True,
        separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()


def _issue(code: str, message: str, file: str = "", line: int = 0, **details: Any) -> dict:
    return {"code": code, "message": message, "file": file, "line": line, **details}


def _path(value: Any) -> bool:
    return isinstance(value, str) and bool(value) and not value.startswith("/") and "\\" not in value and "\x00" not in value and all(
        part not in {"", ".", ".."} for part in value.split("/"))


def walk(node: Any, skip_functions: bool = False):
    """Compatibility adapter for the existing data-only CST walker."""
    from .static_contracts import _walk
    return _walk(node, skip_functions)


def unwrap(node: Any) -> Any:
    from .static_contracts import _unwrap
    result = _unwrap(node)
    if result is not None and result.type == "type_assertion":
        from .typescript_analyzer import _unwrap as _ts_unwrap
        return _ts_unwrap(result)
    return result


def _authenticated_text(source: SourceFile) -> tuple[dict | None, list[dict]]:
    if not isinstance(source.content, str):
        return None, [_issue("source_content_invalid", "快照没有文本源码。", source.path)]
    try:
        data = source.content.encode("utf-8")
    except UnicodeEncodeError:
        return None, [_issue("source_encoding_invalid", "保存文本不能编码为 UTF-8。", source.path)]
    text_hash = hashlib.sha256(data).hexdigest()
    if source.hash == text_hash:
        return {"original_text_utf8_sha256": text_hash, "source_file_sha256": source.hash,
            "source_encoding": "utf-8", "original_file_byte_offset": 0}, []
    # The trusted reader decodes UTF-8-sig, but keeps the original byte hash.
    # Accept a BOM only when reconstructing that exact byte stream proves it.
    if source.hash == hashlib.sha256(b"\xef\xbb\xbf" + data).hexdigest():
        return {"original_text_utf8_sha256": text_hash, "source_file_sha256": source.hash,
            "source_encoding": "utf-8-sig", "original_file_byte_offset": 3}, []
    return None, [_issue("source_hash_mismatch", "保存文本与原文件哈希不匹配，拒绝作为语义源码依据。", source.path)]


class SemanticDocument:
    """Compatibility view of _Document with authenticated derived parsing.

    The frontend collector is reused only for lexical CST owner identities.
    It has a separate temporary index and never resolves imports, writes to
    the snapshot, or creates new CALLS facts. This private compatibility
    dependency should eventually become a shared public CST record layer.
    """

    def __init__(self, source: SourceFile, kind: str, snapshot: GraphSnapshot,
                 authentication: dict, saved_projection: dict | None):
        self.source, self.kind = replace(source), kind
        self.data = source.content.encode("utf-8")
        self.lines = source.content.split("\n")
        self.parser_version = parser_version(kind)
        self.snapshot_id = snapshot.id
        self.original_file_byte_offset = authentication["original_file_byte_offset"]
        parser = language_parser(kind)
        if kind in {"typescript", "tsx"}:
            self.tree, projection = parse_with_projection(self.data, parser, kind)
        else:
            self.tree = parser.parse(self.data)
            projection = None
        self.parse_provenance: dict[str, Any] = {
            "semantic_source_version": VERSION, "semantic_parser_version": self.parser_version,
            "grammar": kind, "text_authentication": dict(authentication),
            "snapshot_identity": {"snapshot_id": snapshot.id, "source_hash": snapshot.source_hash,
                "analyzer_version": snapshot.analyzer_version, "detector_version": snapshot.detector_version,
                "parser_version": snapshot.parser_version,
                "frontend_version": deepcopy(snapshot.stats.get("component_versions", {}).get(
                    "rust" if kind == "rust" else "typescript", {}))},
            "syntax_projection": projection,
            "saved_syntax_projection": deepcopy(saved_projection),
            "literal_authority": "original_saved_source_text_only",
            "position_map": "identity_utf8_bytes_and_line_columns",
            "coordinate_space": "captured_text_utf8", "raw_prefix_bytes": self.original_file_byte_offset,
            "original_file_byte_map": "captured_byte_offset_plus_raw_prefix_bytes",
            "column_base": 1, "snapshot_graph_edge_column_base": 0,
        }
        self.definitions: dict[str, list[Any]] = {}
        self.definition_nodes: dict[str, list[Any]] = {}
        self._ast_definitions: dict[int, list[Any]] = {}
        self._collector_scopes: dict[int, Any] = {}
        self._function_ids: dict[int, str] = {}
        self.module = ("rust:" if kind == "rust" else "ts:") + str(PurePosixPath(source.path).with_suffix(""))
        self.parse_id = _digest(self.parse_provenance)

    def text(self, node: Any) -> str:
        if node is None:
            return ""
        return self.data[node.start_byte:node.end_byte].decode("utf-8")

    def contains(self, node: Any) -> bool:
        if node is None or not (0 <= node.start_byte <= node.end_byte <= len(self.data)):
            return False
        root = node
        while root.parent is not None:
            root = root.parent
        return root.id == self.tree.root_node.id

    def location(self, node: Any) -> dict:
        if not self.contains(node):
            raise ValueError("CST 节点不属于此已认证源码文档")
        excerpt = self.data[node.start_byte:node.end_byte]
        projection = self.parse_provenance.get("syntax_projection") or {}
        return {"file": self.source.path, "line": node.start_point.row + 1,
            "column": node.start_point.column + 1, "end_line": node.end_point.row + 1,
            "end_column": node.end_point.column + 1, "column_unit": "utf8_bytes", "column_base": 1,
            "coordinate_space": "captured_text_utf8", "raw_prefix_bytes": self.original_file_byte_offset,
            "start_byte": node.start_byte, "end_byte": node.end_byte,
            "original_file_start_byte": node.start_byte + self.original_file_byte_offset,
            "original_file_end_byte": node.end_byte + self.original_file_byte_offset,
            "source_hash": self.source.hash, "grammar": self.kind, "parser_version": self.parser_version,
            "span_hash": hashlib.sha256(excerpt).hexdigest(),
            "source_line": self.lines[node.start_point.row] if node.start_point.row < len(self.lines) else "",
            "source_excerpt": excerpt[:4096].decode("utf-8", "ignore"),
            "source_excerpt_truncated": len(excerpt) > 4096,
            "semantic_parse_id": self.parse_id,
            "parse_identity": {"semantic_source_version": VERSION,
                "semantic_parser_version": self.parser_version, "snapshot_id": self.snapshot_id,
                "original_text_utf8_sha256": hashlib.sha256(self.data).hexdigest(),
                "projection_version": projection.get("version"), "projection_mode": projection.get("mode", "original"),
                "derived_text_utf8_sha256": projection.get("derived_text_utf8_sha256"),
                "coordinate_space": "captured_text_utf8", "raw_prefix_bytes": self.original_file_byte_offset,
                "literal_authority": "original_saved_source_text_only",
                "position_map": "identity_utf8_bytes_and_line_columns"}}

    def _scope(self, node: Any) -> list[str]:
        if self.kind != "rust" and node.id in self._collector_scopes:
            qualified = self._collector_scopes[node.id].qualname
            return qualified.split(".") if qualified else []
        scopes: list[str] = []
        parent = node.parent
        while parent is not None:
            if self.kind == "rust" and parent.type == "impl_item":
                from .rust_analyzer import _segments
                declared_type = parent.child_by_field_name("type")
                parts = _segments(declared_type, self.data)
                type_name = "::".join(parts) if parts else self.text(declared_type)
                trait = parent.child_by_field_name("trait")
                scopes.append(f"<{type_name} as {self.text(trait)}>" if trait else type_name)
            elif parent.type in {"mod_item", "trait_item"}:
                name = parent.child_by_field_name("name")
                if name is not None:
                    scopes.append(self.text(name).removeprefix("r#"))
            elif parent.type in _FUNCTIONS:
                if parent.id in self._function_ids:
                    return self._function_ids[parent.id].split("#", 1)[1].split(".") + list(reversed(scopes))
                name = parent.child_by_field_name("name")
                scopes.append(self.text(name).removeprefix("r#") if name is not None else
                    f"<{parent.type}@{parent.start_point.row + 1}:{parent.start_point.column + 1}>")
            parent = parent.parent
        return list(reversed(scopes))

    def index_definitions(self, config: dict) -> None:
        from .static_contracts import _Definition
        if self.kind != "rust":
            from . import typescript_analyzer as frontend
            module = frontend._Module(replace(self.source, module=self.module), self.data,
                tree=self.tree, projection=self.parse_provenance.get("syntax_projection") or {})
            temporary = frontend._Index(config)
            temporary.modules[self.source.path] = [module]
            module.scope = frontend._Scope("module", module, "module:" + self.module, "")
            frontend._Collector(temporary, module).visit(self.tree.root_node)
            self._collector_scopes = temporary.scopes
            self._function_ids = {key: value for key, value in temporary.function_nodes.items()
                if value in temporary.nodes and temporary.nodes[value].kind in {"function", "method"}}
            self.parse_provenance["lexical_selector_model"] = frontend.ANALYZER_VERSION
        else:
            from .rust_analyzer import ANALYZER_VERSION
            self.parse_provenance["lexical_selector_model"] = ANALYZER_VERSION
        seen: set[tuple[str, int, int]] = set()
        for node in walk(self.tree.root_node):
            if node.type not in _DEFINITIONS and node.id not in self._function_ids:
                continue
            value = node.child_by_field_name("value")
            function = unwrap(value) if value is not None else node
            function_id = self._function_ids.get(function.id)
            if self.kind == "rust":
                name = node.child_by_field_name("name")
                if name is None or name.type not in {"identifier", "type_identifier"}:
                    continue
                local_name = self.text(name).removeprefix("r#")
                symbol = ".".join([*self._scope(node), local_name])
                if node.type == "function_item":
                    function_id = self.module + "#" + symbol
                    self._function_ids[node.id] = function_id
            elif function_id:
                symbol = function_id.split("#", 1)[1]
                local_name = symbol.rsplit(".", 1)[-1]
                # A named expression assigned to a variable has one callable
                # identity. Keep the declaration wrapper for compatibility.
                key = (symbol, function.start_byte, function.end_byte)
                if key in seen:
                    continue
                seen.add(key)
            else:
                name = node.child_by_field_name("name")
                if name is None or name.type != "identifier" or node.id not in self._collector_scopes:
                    continue
                local_name = self.text(name)
                symbol = ".".join([*self._scope(node), local_name])
            is_callable = bool(function_id) or node.type in _FUNCTIONS
            definition = _Definition(symbol, local_name, node, value, is_callable)
            definition.graph_node_id = function_id or ""
            self.definitions.setdefault(symbol, []).append(definition)
            if function_id:
                self.definition_nodes.setdefault(function_id, []).append(definition)
            for syntax in (node, function):
                self._ast_definitions.setdefault(syntax.id, []).append(definition)
        self.parse_id = _digest(self.parse_provenance)

    def definition_for_ast(self, node: Any) -> Any | None:
        if not self.contains(node):
            return None
        definitions = self._ast_definitions.get(node.id, [])
        unique = {id(definition): definition for definition in definitions}
        return next(iter(unique.values())) if len(unique) == 1 else None

    def call_owner(self, call: Any) -> str | None:
        if not self.contains(call):
            return None
        if self.kind != "rust":
            scope = self._collector_scopes.get(call.id)
            return scope.owner if scope else None
        parent = call.parent
        while parent is not None:
            if parent.type in {"closure_expression", "async_block", "gen_block"}:
                return None
            if parent.type == "function_item":
                return self._function_ids.get(parent.id)
            parent = parent.parent
        return "module:" + self.module


class SemanticSources:
    def __init__(self, snapshot: GraphSnapshot):
        self.snapshot = snapshot
        self.files: dict[str, list[SourceFile]] = {}
        self.nodes: dict[str, list[Node]] = {}
        self.edges: dict[tuple[str, int, int], list[Edge]] = {}
        for source in snapshot.files:
            self.files.setdefault(source.path, []).append(source)
        for node in snapshot.nodes:
            self.nodes.setdefault(node.id, []).append(node)
        for edge in snapshot.edges:
            self.edges.setdefault((edge.file, edge.line, edge.column), []).append(edge)
        self.cache: dict[str, tuple[SemanticDocument | None, list[dict]]] = {}

    def _saved_projection(self, source: SourceFile) -> tuple[dict | None, list[dict]]:
        candidates = [node for node in self.snapshot.nodes if node.file == source.path and node.kind == "module"
            and isinstance(node.metadata.get("syntax_projection"), dict)]
        if len(candidates) > 1:
            return None, [_issue("projection_not_unique", "快照有多个派生解析身份，不能认证。", source.path)]
        return (candidates[0].metadata["syntax_projection"] if candidates else None), []

    def load(self, path: str) -> tuple[SemanticDocument | None, list[dict]]:
        if not _path(path):
            return None, [_issue("source_path_invalid", "源码路径必须为项目内规范相对路径。")]
        if path in self.cache:
            return self.cache[path]
        files = self.files.get(path, [])
        if len(files) != 1:
            code = "support_input_only" if not files and path in self.snapshot.input_evidence else "source_not_unique"
            result = (None, [_issue(code, f"已解析实现源码匹配 {len(files)} 项；辅助输入不充当实现。", path)])
        elif files[0].status != "parsed":
            source = files[0]
            result = (None, [_issue("source_not_parsed", f"历史快照源码状态 {source.status}：{source.error or '不完整'}；新 parser 不能补成旧事实。", path)])
        else:
            source = files[0]
            authentication, problems = _authenticated_text(source)
            saved, saved_problems = self._saved_projection(source)
            problems.extend(saved_problems)
            language = source.language.lower()
            kind = "rust" if language == "rust" else ("tsx" if PurePosixPath(path).suffix in {".tsx", ".jsx"} else "typescript") if language in _TS_LANGUAGES else ""
            if not kind:
                problems.append(_issue("unsupported_semantic_language", "语义 CST 仅支持保存的 TS/JS/TSX 与 Rust。", path))
            document = None
            if not problems:
                try:
                    document = SemanticDocument(source, kind, self.snapshot, authentication, saved)
                    projection = document.parse_provenance.get("syntax_projection") or {}
                    if document.tree.root_node.has_error:
                        problems.append(_issue("semantic_parse_error", "未识别语法仍不完整，不作封闭语义推论。", path,
                            raw_errors=projection.get("raw_errors", grammar_errors(document.tree)),
                            derived_errors=projection.get("derived_errors", []), parse_provenance=document.parse_provenance))
                    elif projection.get("raw_parser_has_error"):
                        keys = ("version", "mode", "accepted", "source_file_sha256", "original_text_utf8_sha256", "derived_text_utf8_sha256", "edits")
                        actual = {**projection, "source_file_sha256": source.hash}
                        if (projection.get("mode") != "adapted" or not projection.get("accepted")
                                or not saved or any(saved.get(key) != actual.get(key) for key in keys)):
                            problems.append(_issue("projection_not_authenticated", "派生 CST 必须与历史快照已接受的投影及原文身份一致。", path,
                                semantic_projection=projection, saved_projection=saved))
                    if not problems:
                        document.index_definitions(self.snapshot.config)
                except (ImportError, ValueError, RuntimeError, RecursionError, OverflowError, TypeError, AttributeError) as error:
                    problems.append(_issue("semantic_parser_failure", f"可信 CST 适配失败：{type(error).__name__}: {str(error)[:300]}", path))
            result = (None if problems else document, problems)
        self.cache[path] = result
        return result

    def select(self, selector: dict) -> tuple[SemanticDocument | None, Any | None, list[dict]]:
        if not isinstance(selector, dict) or not _path(selector.get("file")) or not isinstance(selector.get("symbol"), str):
            return None, None, [_issue("selector_invalid", "选择器需要 exact file 与 lexical symbol。")]
        document, problems = self.load(selector["file"])
        if document is None:
            return None, None, problems
        definitions = document.definitions.get(selector["symbol"], [])
        if len(definitions) != 1:
            return document, None, [_issue("symbol_not_unique", f"词法符号 {selector['symbol']} 精确匹配 {len(definitions)} 个定义。", selector["file"])]
        return document, definitions[0], []

    def definition_for_node(self, node: Node) -> tuple[SemanticDocument | None, Any | None, list[dict]]:
        stored = self.nodes.get(node.id, [])
        if len(stored) != 1 or stored[0] is not node or node.kind not in {"function", "method"} or any(node.metadata.get(key) for key in _NODE_GAPS):
            return None, None, [_issue("graph_declaration_not_unique", "图声明不是唯一、完整的捕获函数/方法。", node.file, node.line)]
        document, problems = self.load(node.file)
        if document is None:
            return None, None, problems
        definitions = document.definition_nodes.get(node.id, [])
        if len(definitions) != 1:
            return document, None, [_issue("graph_symbol_not_unique", "图节点没有唯一 exact lexical CST 声明。", node.file, node.line, node_id=node.id)]
        definition = definitions[0]
        function = unwrap(definition.value) if definition.value is not None else definition.node
        if (not definition.callable or function.start_point.row + 1 != node.line
                or function.end_point.row + 1 != node.end_line):
            return document, None, [_issue("graph_declaration_span_mismatch", "图声明区间与原源码 CST 函数身份不一致。", node.file, node.line, node_id=node.id)]
        return document, definition, []

    def call_binding(self, call: Any, document: SemanticDocument, owner: Any) -> tuple[Edge | None, list[dict]]:
        loaded, problems = self.load(document.source.path)
        if loaded is not document or not document.contains(call) or call.type not in {"call_expression", "new_expression"}:
            return None, problems or [_issue("call_site_invalid", "调用 CST/文档不是此快照的已认证调用位置。", document.source.path)]
        if isinstance(owner, dict):
            selected_document, definition, problems = self.select(owner)
            if selected_document is not document or definition is None:
                return None, problems or [_issue("call_owner_invalid", "调用者选择器属于其它文档。", document.source.path)]
        elif hasattr(owner, "symbol") and hasattr(owner, "node"):
            definition = document.definition_for_ast(owner.node)
            if definition is not owner:
                return None, [_issue("call_owner_invalid", "调用者定义不属于此已认证文档。", document.source.path)]
        else:
            definition = document.definition_for_ast(owner)
            if definition is None:
                return None, [_issue("call_owner_invalid", "AST 调用者没有唯一的已认证词法定义。", document.source.path)]
        owner_id = getattr(definition, "graph_node_id", "")
        owner_nodes = self.nodes.get(owner_id, [])
        if len(owner_nodes) != 1 or document.call_owner(call) != owner_id:
            return None, [_issue("call_owner_mismatch", "调用点不属于唯一 exact lexical 图调用者；不按同名匹配。", document.source.path, call.start_point.row + 1)]
        _, _, owner_problems = self.definition_for_node(owner_nodes[0])
        if owner_problems:
            return None, owner_problems
        function = call.child_by_field_name("function") or call.child_by_field_name("constructor")
        if document.kind == "rust":
            while function is not None and function.type == "generic_function":
                function = function.child_by_field_name("function")
            anchor = f"{document.source.path}:{owner_id}:{call.start_byte}:{call.end_byte}"
            expected_id = "rust-call:" + hashlib.sha256(anchor.encode("utf-8")).hexdigest()[:24]
        else:
            frontend = self.snapshot.stats.get("component_versions", {}).get("typescript", {})
            version = frontend.get("analyzer")
            if not version:
                return None, [_issue("snapshot_call_identity_missing", "历史快照缺少 TS call-id 模型版本，不能认证 byte span。", document.source.path, call.start_point.row + 1)]
            expected_id = _digest([version, owner_id, document.source.path, call.start_byte, call.end_byte,
                "new" if call.type == "new_expression" else "call"])[:24]
        sites = self.edges.get((document.source.path, call.start_point.row + 1, call.start_point.column), [])
        # Nested calls may share their start point. The saved call-id model
        # binds the complete byte extent, so disambiguate before uniqueness.
        edges = [edge for edge in sites if edge.source == owner_id and edge.id == expected_id
            and edge.expression == document.text(function)[:600]]
        if len(edges) != 1:
            return None, [_issue("call_edge_not_unique", f"原完整调用区间匹配 {len(edges)} 条同 owner 快照边。", document.source.path, call.start_point.row + 1,
                expected_edge_id=expected_id, start_byte=call.start_byte, end_byte=call.end_byte)]
        edge = edges[0]
        if edge.resolution != "resolved" or not edge.target or edge.metadata.get("cfg_conditions") or any(edge.metadata.get(key) for key in (
                "incomplete_source", "source_parse_partial", "source_ambiguous", "source_attribute_macros_unknown", "closure_activation_unknown")):
            return None, [_issue("call_binding_unknown", "快照没有有效确定的内部 callee；候选、动态或部分来源不提升。", edge.file, edge.line,
                edge_id=edge.id, resolution=edge.resolution, candidates=list(edge.candidates), reason=edge.reason)]
        targets = self.nodes.get(edge.target, [])
        if len(targets) != 1:
            return None, [_issue("call_target_not_unique", "边目标没有唯一快照节点。", edge.file, edge.line)]
        _, _, target_problems = self.definition_for_node(targets[0])
        if target_problems:
            return None, target_problems
        return edge, []
