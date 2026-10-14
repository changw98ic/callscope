"""Narrow, auditable syntax projections for a fixed Tree-sitter TS grammar.

The returned tree reads a *derived* byte buffer. Original source bytes remain
the authority for names, strings, evidence and coordinates. Every substitution
has the same width and preserves newlines, so the position map is identity.
No expression is evaluated and unsupported syntax stays a parse failure.
"""

from __future__ import annotations

from bisect import bisect_right
from dataclasses import dataclass, field
import hashlib
from typing import Any

PROJECTION_VERSION = "ts-syntax-projection-1"
_TYPE_MARKER = b"__cst_"
_PROPERTY_MARKER = b"_cs_prop"


def _walk(root: Any):
    pending = [root]
    while pending:
        node = pending.pop()
        yield node
        pending.extend(reversed(node.children))


def grammar_errors(tree: Any) -> list[dict[str, Any]]:
    errors = []
    for node in _walk(tree.root_node):
        if node.type == "ERROR" or node.is_missing:
            errors.append({"type": node.type, "missing": bool(node.is_missing),
                "start_byte": node.start_byte, "end_byte": node.end_byte,
                "line": node.start_point.row + 1, "column": node.start_point.column,
                "end_line": node.end_point.row + 1, "end_column": node.end_point.column})
    return errors


def _field(node: Any, name: str) -> Any:
    return node.child_by_field_name(name) if node is not None else None


def _contains(outer: Any, inner: Any) -> bool:
    return outer is not None and outer.start_byte <= inner.start_byte and inner.end_byte <= outer.end_byte


def _type_context(node: Any, data: bytes) -> dict[str, Any] | None:
    """Find positive type-context evidence, including one strict error recovery."""
    cursor = node.parent
    while cursor is not None:
        if cursor.type == "type_annotation" and data[cursor.start_byte:cursor.start_byte + 1] == b":":
            return {"kind": "type_annotation", "start_byte": cursor.start_byte, "end_byte": cursor.end_byte}
        if cursor.type == "type_alias_declaration" and _contains(_field(cursor, "value"), node):
            return {"kind": "type_alias", "start_byte": cursor.start_byte, "end_byte": cursor.end_byte}
        if cursor.type == "interface_declaration":
            return {"kind": "interface", "start_byte": cursor.start_byte, "end_byte": cursor.end_byte}
        if cursor.type == "ERROR" and cursor.parent is not None and cursor.parent.type == "variable_declarator":
            declaration = cursor.parent
            name, value = _field(declaration, "name"), _field(declaration, "value")
            prefix = data[cursor.start_byte:cursor.start_byte + 1]
            between_name = data[name.end_byte:cursor.start_byte] if name is not None else b"invalid"
            between_value = data[cursor.end_byte:value.start_byte] if value is not None else b"invalid"
            if (name is not None and name.type == "identifier" and value is not None and prefix == b":"
                    and not between_name.strip() and between_value.strip() == b"="
                    and name.end_byte <= cursor.start_byte < node.start_byte < cursor.end_byte <= value.start_byte):
                return {"kind": "recovered_declaration_annotation", "start_byte": cursor.start_byte,
                        "end_byte": cursor.end_byte, "name_start_byte": name.start_byte,
                        "initializer_start_byte": value.start_byte}
        if cursor.type in {"program", "statement_block", "arguments", "template_substitution"}:
            return None
        cursor = cursor.parent
    return None


class _Decline(ValueError):
    pass


class _LiteralScanner:
    """Scan quote/template raw regions, with CST evidence for slash tokens.

    Unknown slash classification or unterminated literals abort projection,
    rather than guessing regex/division or swallowing interpolation code.
    """
    def __init__(self, data: bytes, tree: Any):
        self.data = data
        self.regions: list[tuple[int, int, str]] = []
        self.nuls: list[tuple[int, str]] = []
        self.regex = {node.start_byte: node.end_byte for node in _walk(tree.root_node)
                      if node.type == "regex" and not node.has_error}
        self.slashes = {node.start_byte: node.end_byte for node in _walk(tree.root_node)
                        if node.type in {"/", "/="} and not node.is_missing}
        self._code(0, False, 0)
        self.regions.sort()
        self.starts = [start for start, _, _ in self.regions]

    def _region(self, start: int, end: int, kind: str) -> None:
        if end > start:
            self.regions.append((start, end, kind))

    def is_code(self, offset: int) -> bool:
        index = bisect_right(self.starts, offset) - 1
        return index < 0 or self.regions[index][1] <= offset

    def _quoted(self, start: int) -> int:
        data, quote, position = self.data, self.data[start], start + 1
        while position < len(data):
            byte = data[position]
            if byte == quote:
                self._region(start, position + 1, "quoted_literal")
                return position + 1
            if byte in {10, 13}:
                raise _Decline("未闭合 quoted literal，拒绝猜测后续语法范围")
            if byte == 0:
                self.nuls.append((position, "quoted_literal"))
            if byte == 92:
                if position + 1 >= len(data):
                    break
                if data[position + 1] == 0:
                    self.nuls.append((position + 1, "quoted_literal"))
                position += 2
                if data[position - 1] == 13 and position < len(data) and data[position] == 10:
                    position += 1
            else:
                position += 1
        raise _Decline("未闭合 quoted literal，拒绝语法适配")

    def _template(self, start: int, depth: int) -> int:
        if depth > 64:
            raise _Decline("模板嵌套超过静态 lexer 范围")
        data, position, segment = self.data, start + 1, start
        while position < len(data):
            byte = data[position]
            if byte == 96:
                self._region(segment, position + 1, "template_raw")
                return position + 1
            if byte == 0:
                self.nuls.append((position, "template_raw"))
            if byte == 92:
                if position + 1 < len(data) and data[position + 1] == 0:
                    self.nuls.append((position + 1, "template_raw"))
                position += 2
                continue
            if byte == 36 and data[position:position + 2] == b"${":
                self._region(segment, position + 2, "template_raw")
                position = self._code(position + 2, True, depth + 1)
                segment = position - 1
                continue
            position += 1
        raise _Decline("未闭合 template literal，拒绝语法适配")

    def _code(self, position: int, interpolation: bool, depth: int) -> int:
        data, braces = self.data, 0
        while position < len(data):
            byte = data[position]
            if byte in {34, 39}:
                position = self._quoted(position)
            elif byte == 96:
                position = self._template(position, depth + 1)
            elif data[position:position + 2] == b"//":
                end = data.find(b"\n", position + 2)
                end = len(data) if end < 0 else end
                self._region(position, end, "comment")
                position = end
            elif data[position:position + 2] == b"/*":
                end = data.find(b"*/", position + 2)
                if end < 0:
                    raise _Decline("未闭合 comment，拒绝猜测后续 literal 范围")
                self._region(position, end + 2, "comment")
                position = end + 2
            elif byte == 47:
                if position in self.regex:
                    end = self.regex[position]
                    if b"\x00" in data[position:end]:
                        raise _Decline("regex 内的 NUL 不在本次适配范围")
                    self._region(position, end, "regex")
                    position = end
                elif position in self.slashes:
                    position = self.slashes[position]
                else:
                    raise _Decline(f"无法由源码CST确认 slash 是regex还是division（byte {position}）")
            elif byte == 123:
                braces += 1
                position += 1
            elif byte == 125:
                if interpolation and braces == 0:
                    return position + 1
                braces -= 1
                position += 1
            else:
                position += 1
        if interpolation:
            raise _Decline("未闭合 template interpolation，拒绝语法适配")
        return position


@dataclass
class _Edit:
    start: int
    end: int
    rule: str
    replacement: bytes
    evidence: dict[str, Any] = field(default_factory=dict)


def _candidate_edits(data: bytes, tree: Any, scanner: _LiteralScanner, grammar: str) -> list[_Edit]:
    edits: list[_Edit] = []
    for node in _walk(tree.root_node):
        if node.type == "call_expression":
            function, arguments = _field(node, "function"), _field(node, "arguments")
            if function is None or function.type != "import" or arguments is None or node.has_error:
                continue
            children = [child for child in arguments.named_children if child.type != "comment"]
            if len(children) != 1 or children[0].type != "string" or _field(node, "type_arguments") is not None:
                continue
            if not scanner.is_code(node.start_byte) or data[function.start_byte:function.end_byte] != b"import":
                continue
            context = _type_context(node, data)
            if context is None:
                continue
            if node.parent is None or node.parent.type != "member_expression" or _field(node.parent, "object") != node:
                continue  # the first version supports qualified import types only
            if _field(node.parent, "optional_chain") is not None:
                continue
            original = data[node.start_byte:node.end_byte]
            if not original.startswith(b"import(") and not original.startswith(b"import ("):
                continue
            replacement = bytearray(10 if byte == 10 else 13 if byte == 13 else 32 for byte in original)
            replacement[:len(_TYPE_MARKER)] = _TYPE_MARKER
            edits.append(_Edit(node.start_byte, node.end_byte, "qualified_import_type", bytes(replacement), context))
        elif node.type == "ERROR" and node.parent is not None and node.parent.type == "object_type":
            original = data[node.start_byte:node.end_byte]
            if not original.startswith(b"abstract") or original[8:].strip() != b"?:" or not scanner.is_code(node.start_byte):
                continue
            context = _type_context(node, data)
            if context is not None:
                edits.append(_Edit(node.start_byte, node.start_byte + 8, "type_only_abstract_property", _PROPERTY_MARKER, context))
    if grammar == "typescript":  # JSX text needs its own lexer, not this code lexer
        for position, kind in scanner.nuls:
            edits.append(_Edit(position, position + 1, "literal_nul_cst_surrogate", b"~",
                {"kind": kind, "literal_value_authority": "original_utf8_source",
                 "derived_literal_must_not_be_evaluated": True}))
    return sorted(edits, key=lambda edit: (edit.start, edit.end, edit.rule))


def _validate_edit(edit: _Edit, tree: Any, original: bytes) -> bool:
    node = tree.root_node.descendant_for_byte_range(edit.start, edit.start + 1)
    if edit.rule == "qualified_import_type":
        return (node.type in {"identifier", "type_identifier"} and node.start_byte == edit.start
                and node.end_byte == edit.start + len(_TYPE_MARKER) and _type_context(node, original) is not None)
    if edit.rule == "type_only_abstract_property":
        return (node.type == "property_identifier" and node.start_byte == edit.start and node.end_byte == edit.end
                and node.parent is not None and node.parent.type == "property_signature"
                and _type_context(node, original) is not None)
    if edit.rule == "literal_nul_cst_surrogate":
        while node is not None:
            if node.type in {"string", "template_string"}:
                return True
            if node.type in {"template_substitution", "program", "regex"}:
                return False
            node = node.parent
    return False


def parse_with_projection(data: bytes, parser: Any, grammar: str) -> tuple[Any, dict[str, Any]]:
    """Return a tree and explicit provenance; never change the caller's data."""
    raw_tree = parser.parse(data)
    raw_errors = grammar_errors(raw_tree) if raw_tree.root_node.has_error else []
    provenance: dict[str, Any] = {"version": PROJECTION_VERSION, "mode": "original", "applied": False,
        "original_text_utf8_sha256": hashlib.sha256(data).hexdigest(),
        "raw_parser_has_error": bool(raw_tree.root_node.has_error), "raw_errors": raw_errors,
        "position_map": "identity_utf8_bytes_and_line_columns", "edits": []}
    if not raw_errors:
        return raw_tree, provenance
    try:
        scanner = _LiteralScanner(data, raw_tree)
        edits = _candidate_edits(data, raw_tree, scanner, grammar)
    except (_Decline, RecursionError) as error:
        provenance["declined_reason"] = str(error)
        return raw_tree, provenance
    if not edits:
        provenance["declined_reason"] = "没有同时具备lexer范围与类型/字面量证据的受支持适配区间"
        return raw_tree, provenance
    derived = bytearray(data)
    end = -1
    for edit in edits:
        before = data[edit.start:edit.end]
        if edit.start < end or len(before) != len(edit.replacement):
            provenance["declined_reason"] = "适配区间重叠或不等宽，拒绝改变源码位置"
            return raw_tree, provenance
        if [i for i, byte in enumerate(before) if byte in {10, 13}] != [i for i, byte in enumerate(edit.replacement) if byte in {10, 13}]:
            provenance["declined_reason"] = "适配改变换行位置，拒绝改变源码坐标"
            return raw_tree, provenance
        derived[edit.start:edit.end] = edit.replacement
        end = edit.end
        line = data.count(b"\n", 0, edit.start) + 1
        last_newline = data.rfind(b"\n", 0, edit.start)
        provenance["edits"].append({"rule": edit.rule, "start_byte": edit.start, "end_byte": edit.end,
            "line": line, "column": edit.start - last_newline - 1,
            "original_utf8": before.decode("utf-8", "replace"), "original_hex": before.hex(),
            "derived_utf8": edit.replacement.decode("ascii"), "derived_hex": edit.replacement.hex(),
            "evidence": edit.evidence})
    parse_data = bytes(derived)
    tree = parser.parse(parse_data)
    provenance["derived_text_utf8_sha256"] = hashlib.sha256(parse_data).hexdigest()
    provenance["derived_errors"] = grammar_errors(tree) if tree.root_node.has_error else []
    if tree.root_node.has_error:
        provenance.update(mode="partial_projection", applied=True, accepted=False)
        return tree, provenance
    if not all(_validate_edit(edit, tree, data) for edit in edits):
        provenance.update(mode="rejected_projection", accepted=False,
                          declined_reason="派生CST未证明占位符仅处于类型/字面量语法，保留原始解析失败")
        return raw_tree, provenance
    provenance.update(mode="adapted", applied=True, accepted=True,
        runtime_literal_authority="original_source_only", runtime_value_bindings_synthesized=False)
    return tree, provenance
