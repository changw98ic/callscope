"""Finite source-expression contracts for captured TS/JS call arguments.

Nothing here opens a target file, imports a target module, executes an
expression, or follows a transport by its field name. Expected expressions
are explicit policy data. Actual expressions and lexical initializer origins
come from the captured AST. A matched callee spelling is not a CALLS proof.
"""

from __future__ import annotations

import math
from typing import Any

from .models import Evidence, Finding, GraphSnapshot
from .static_contracts import (
    _Sources, _Document, _Definition, _FUNCTIONS, _CLASS_SCOPES,
    _walk, _unwrap, _literal_string, _digest, _issue, _path, _string,
    _validate_reference, _source_reference, _branch_conditions,
)

VERSION = "static-value-contracts-1"
POLICY_VERSION = "static-value-policy-v1"
_SEVERITIES = {"high", "medium", "low", "info"}
_SCOPES = {"program", "statement_block", "switch_body", "for_statement",
    "for_in_statement", "catch_clause", *_FUNCTIONS, *_CLASS_SCOPES}
_SYMBOLIC_KINDS = {"literal", "reference", "member", "call", "conditional"}
_CALL_LIMIT = 512
_FACT_SAMPLE_LIMIT = 64
_ORIGIN_DEPTH = 4


def _json_data(value: Any, depth: int = 0, budget: list[int] | None = None) -> None:
    """Reject Python objects/callables even when json would coerce their keys."""
    budget = budget if budget is not None else [4096]
    budget[0] -= 1
    if depth > 32 or budget[0] < 0:
        raise ValueError("值合同超出静态数据大小/嵌套范围。")
    if value is None or type(value) in {str, bool, int}:
        return
    if type(value) is float and math.isfinite(value):
        return
    if type(value) is list:
        for item in value:
            _json_data(item, depth + 1, budget)
        return
    if type(value) is dict and all(type(key) is str for key in value):
        for item in value.values():
            _json_data(item, depth + 1, budget)
        return
    raise ValueError("值合同只能包含有限 JSON 数据，不能含可执行对象。")


def _expression_policy(value: Any, depth: int = 0) -> None:
    if not isinstance(value, dict) or depth > 16 or not isinstance(value.get("kind"), str) or value.get("kind") not in _SYMBOLIC_KINDS:
        raise ValueError("expected 必须是受支持的有限 symbolic expression。")
    kind = value["kind"]
    keys = {
        "literal": {"kind", "value"}, "reference": {"kind", "name"},
        "member": {"kind", "object", "property"},
        "call": {"kind", "callee", "arguments"},
        "conditional": {"kind", "operator", "condition", "then", "else"},
    }[kind]
    if set(value) != keys:
        raise ValueError(f"{kind} 表达式字段不完整或包含未知键。")
    if kind == "literal":
        literal = value["value"]
        if literal is not None and type(literal) not in {str, bool, int, float}:
            raise ValueError("literal 仅支持 JSON primitive。")
        if type(literal) in {int, float} and (abs(literal) > 2**53 - 1 or (type(literal) is float and not math.isfinite(literal))):
            raise ValueError("literal 数字必须处于有限、精确的 JS Number 范围。")
    elif kind == "reference":
        if not _string(value["name"]) or not value["name"].isidentifier() or "\\" in value["name"]:
            raise ValueError("reference 需要未转义的词法名称。")
    elif kind == "member":
        if not _string(value["property"]):
            raise ValueError("member.property 必须为静态字段名。")
        _expression_policy(value["object"], depth + 1)
    elif kind == "call":
        _expression_policy(value["callee"], depth + 1)
        if not isinstance(value["arguments"], list) or len(value["arguments"]) > 32:
            raise ValueError("call.arguments 必须是有限表达式列表。")
        for argument in value["arguments"]:
            _expression_policy(argument, depth + 1)
    else:
        if not isinstance(value["operator"], str) or value["operator"] not in {"?:", "||", "??", "&&"}:
            raise ValueError("conditional.operator 仅支持 ?: / || / ?? / &&，默认语义不得混同。")
        for key in ("condition", "then", "else"):
            _expression_policy(value[key], depth + 1)


def _selector_policy(selector: Any) -> None:
    if not isinstance(selector, dict) or set(selector) != {"file", "symbol", "callee", "argument_index", "object_path"}:
        raise ValueError("调用选择器必须包含 file/symbol/callee/argument_index/object_path。")
    if not _path(selector["file"]) or not _string(selector["symbol"]):
        raise ValueError("选择器需要项目内文件路径与精确词法 symbol。")
    callee = selector["callee"]
    if not _string(callee) or any(not part.isidentifier() or "\\" in part for part in callee.split(".")):
        raise ValueError("callee 仅支持未转义 identifier/member 路径，不能包含调用或动态下标。")
    if type(selector["argument_index"]) is not int or not 0 <= selector["argument_index"] <= 32:
        raise ValueError("argument_index 必须是 0 至 32 的静态位置。")
    path = selector["object_path"]
    if not isinstance(path, list) or not 1 <= len(path) <= 32 or not all(_string(part) for part in path):
        raise ValueError("object_path 必须包含最终字段，且是 1 至 32 项静态名称。")


def validate_value_rule(rule: Any) -> None:
    """Validate JSON-only policy; does not read provenance document paths."""
    _json_data(rule)
    if not isinstance(rule, dict):
        raise ValueError("值合同必须是 JSON 对象。")
    keys = {"id", "type", "severity", "subject", "expected", "evaluation",
        "provenance", "applicability", "source_evidence", "producer", "transport"}
    if set(rule) - keys or not _string(rule.get("id")) or rule.get("type") != "call_argument_value":
        raise ValueError("值合同需要唯一 id、type=call_argument_value，且不能含未知配置字段。")
    if not isinstance(rule.get("severity", "medium"), str) or rule.get("severity", "medium") not in _SEVERITIES or rule.get("evaluation") != "all_direct_calls":
        raise ValueError("severity 无效或缺少 evaluation=all_direct_calls。")
    _selector_policy(rule.get("subject"))
    _expression_policy(rule.get("expected"))
    provenance = rule.get("provenance")
    if (not isinstance(provenance, dict) or set(provenance) - {
            "authority", "reviewer", "author_approved", "source_doc", "note"}
        or not _string(provenance.get("authority")) or not _string(provenance.get("source_doc"))
        or type(provenance.get("author_approved")) is not bool):
        raise ValueError("provenance 需要 authority/author_approved/source_doc；文档路径仅作标签。")
    applicability = rule.get("applicability")
    if (not isinstance(applicability, dict) or set(applicability) - {"kind", "conditions", "counterexamples", "guard"}
            or not isinstance(applicability.get("kind"), str) or applicability.get("kind") not in {"unconditional", "conditional"}):
        raise ValueError("applicability 必须声明 unconditional 或 conditional。")
    for key in ("conditions", "counterexamples"):
        values = applicability.get(key, [])
        if not isinstance(values, list) or not all(_string(item) for item in values):
            raise ValueError(f"applicability.{key} 必须是说明字符串列表。")
    if applicability["kind"] == "conditional" and not applicability.get("conditions"):
        raise ValueError("条件合同必须保留外部前提。")
    if applicability.get("guard") is not None:
        _validate_reference(applicability["guard"])
    refs = rule.get("source_evidence", [])
    if not isinstance(refs, list) or len(refs) > 64:
        raise ValueError("source_evidence 最多包含 64 个 AST 依据选择器。")
    for ref in refs:
        _validate_reference(ref)
    producer, transport = rule.get("producer"), rule.get("transport")
    if producer is not None:
        if not isinstance(producer, dict) or set(producer) != {"subject", "expected"}:
            raise ValueError("producer 需要独立 subject 与 expected，不能从消费者字段名推断。")
        _selector_policy(producer["subject"])
        _expression_policy(producer["expected"])
        if (applicability["kind"] != "conditional" or not isinstance(transport, dict)
            or set(transport) != {"kind", "conditions"} or transport.get("kind") != "external_contract"
            or not isinstance(transport.get("conditions"), list) or not transport["conditions"]
            or not all(_string(item) for item in transport["conditions"])):
            raise ValueError("producer 比较必须声明 conditional 与 external_contract transport 前提。")
    elif transport is not None:
        raise ValueError("transport 必须与显式 producer 一起配置。")


def _key(node: Any) -> tuple:
    return (node.type, node.start_byte, node.end_byte)


def _ancestors(node: Any) -> list[Any]:
    values = []
    while node is not None:
        values.append(node)
        node = node.parent
    return values


def _binding_scope(node: Any, var: bool = False) -> Any:
    current = node.parent
    kinds = {"program", *_FUNCTIONS} if var else _SCOPES
    while current is not None and current.type not in kinds:
        current = current.parent
    return current


def _bound_names(node: Any, document: _Document) -> set[str]:
    if node is None:
        return set()
    if node.type in {"identifier", "shorthand_property_identifier_pattern"}:
        text = document.text(node)
        return {text} if "\\" not in text else set()
    if node.type in {"type_annotation", "type_identifier", "property_identifier", "member_expression"}:
        return set()
    pattern = node.child_by_field_name("pattern")
    if pattern is not None:
        return _bound_names(pattern, document)
    if node.type in {"pair_pattern", "assignment_pattern", "object_assignment_pattern"}:
        value = node.child_by_field_name("value") if node.type == "pair_pattern" else node.child_by_field_name("left")
        return _bound_names(value, document)
    values: set[str] = set()
    for child in node.named_children:
        values.update(_bound_names(child, document))
    return values


def _member_path(node: Any, document: _Document) -> list[str] | None:
    node = _unwrap(node)
    if node is None:
        return None
    if node.type in {"identifier", "shorthand_property_identifier", "this"}:
        text = document.text(node)
        return [text] if "\\" not in text else None
    if node.type == "member_expression" and not any(child.type == "optional_chain" for child in node.children):
        prefix = _member_path(node.child_by_field_name("object"), document)
        prop = node.child_by_field_name("property")
        if prefix is not None and prop is not None and prop.type in {"property_identifier", "identifier"} and "\\" not in document.text(prop):
            return [*prefix, document.text(prop)]
    return None


def _unknown(document: _Document, node: Any, reason: str, syntax: dict | None = None) -> dict:
    result = {"kind": "unknown", "complete": False, "reason": reason}
    if node is not None:
        result["location"] = document.location(node)
        result["node_type"] = node.type
    if syntax is not None:
        result["syntax"] = syntax
    return result


class _Reader:
    """A lexical origin record, never reaching-values or heap interpretation."""

    def __init__(self, document: _Document, function: Any, call: Any):
        self.document, self.function, self.call = document, function, call
        self.visible = {_key(node) for node in _ancestors(call)}
        self.all_nodes = list(_walk(document.tree.root_node))
        self.binding_cache: dict[tuple[str, int], dict] = {}

    def binding(self, name: str, at: Any) -> dict:
        cache_key = (name, at.start_byte)
        if cache_key in self.binding_cache:
            return self.binding_cache[cache_key]
        if any(node.type == "with_statement" for node in _ancestors(at)):
            return {"known": False, "name": name, "reason": "with_dynamic_scope"}
        ancestors = {_key(node): index for index, node in enumerate(_ancestors(at))}
        candidates: list[tuple[int, dict]] = []
        for node in self.all_nodes:
            if node.type == "variable_declarator":
                pattern = node.child_by_field_name("name")
                if name not in _bound_names(pattern, self.document):
                    continue
                declaration = node.parent
                var = declaration is not None and declaration.type == "variable_declaration"
                scope = _binding_scope(node, var)
                if scope is None or _key(scope) not in ancestors:
                    continue
                keyword = next((child.type for child in declaration.children if child.type in {"const", "let", "var"}), "")
                candidates.append((ancestors[_key(scope)], {"kind": "const" if keyword == "const" else "mutable",
                    "node": node, "initializer": node.child_by_field_name("value"), "scope": scope,
                    "destructured": pattern is not None and pattern.type != "identifier", "name": name}))
            elif node.type in {"function_declaration", "generator_function_declaration", "class_declaration", "enum_declaration", "internal_module", "import_alias"}:
                ident = node.child_by_field_name("name")
                scope = _binding_scope(node)
                if ident is not None and self.document.text(ident) == name and scope is not None and _key(scope) in ancestors:
                    candidates.append((ancestors[_key(scope)], {"kind": "opaque_declaration" if node.type in {
                        "enum_declaration", "internal_module", "import_alias"} else "declaration", "node": node,
                        "initializer": None, "scope": scope, "name": name}))
            elif node.type in {"import_specifier", "namespace_import", "import_clause"}:
                alias = node.child_by_field_name("alias") or node.child_by_field_name("name")
                if node.type == "import_clause":
                    identifiers = [child for child in node.named_children if child.type == "identifier"]
                    alias = identifiers[0] if len(identifiers) == 1 else None
                if alias is not None and self.document.text(alias) == name:
                    scope = self.document.tree.root_node
                    candidates.append((ancestors.get(_key(scope), 10000), {"kind": "import",
                        "node": node, "initializer": None, "scope": scope, "name": name}))
            elif node.type == "for_in_statement":
                left = node.child_by_field_name("left")
                keyword = next((child.type for child in node.children if child.type in {"let", "const", "var"}), "")
                if keyword and left is not None and left.type not in {"lexical_declaration", "variable_declaration"} and name in _bound_names(left, self.document):
                    scope = _binding_scope(node, True) if keyword == "var" else node
                    if scope is not None and _key(scope) in ancestors:
                        candidates.append((ancestors[_key(scope)], {"kind": "loop_binding", "node": left,
                            "initializer": node.child_by_field_name("right"), "scope": scope, "name": name}))
        for owner in _ancestors(at):
            if owner.type in {"function_expression", "generator_function", "class", "class_expression"}:
                ident = owner.child_by_field_name("name")
                if ident is not None and self.document.text(ident) == name:
                    candidates.append((ancestors[_key(owner)], {"kind": "expression_self_name", "node": ident,
                        "initializer": None, "scope": owner, "name": name}))
            if owner.type not in _FUNCTIONS and owner.type != "catch_clause":
                continue
            params = owner.child_by_field_name("parameters") or owner.child_by_field_name("parameter")
            if params is not None and name in _bound_names(params, self.document):
                candidates.append((ancestors[_key(owner)], {"kind": "parameter", "node": params,
                    "initializer": None, "scope": owner, "name": name}))
        if not candidates:
            result = {"known": False, "name": name, "reason": "unresolved_lexical_binding"}
        else:
            nearest = min(rank for rank, _ in candidates)
            bindings = [binding for rank, binding in candidates if rank == nearest]
            # A var/lexical redeclaration cannot be silently resolved by source order.
            unique = {_key(binding["node"]): binding for binding in bindings}
            if len(unique) != 1:
                result = {"known": False, "name": name, "reason": "duplicate_or_shadow_binding", "binding_count": len(unique)}
            else:
                result = next(iter(unique.values()))
                result["known"] = True
                node = result["node"]
                if result["kind"] in {"const", "mutable"} and node.start_byte >= at.start_byte:
                    result.update(known=False, reason="binding_not_initialized_before_use")
                if result["kind"] in {"mutable", "loop_binding", "opaque_declaration"}:
                    result.update(known=False, reason="mutable_binding_reaching_value_not_modeled")
                aliases = {name}
                for _ in range(_ORIGIN_DEPTH):
                    added = set()
                    for alias_node in self.all_nodes:
                        if alias_node.type != "variable_declarator":
                            continue
                        ident = alias_node.child_by_field_name("name")
                        origin = _unwrap(alias_node.child_by_field_name("value"))
                        scope = _binding_scope(alias_node)
                        if (ident is not None and ident.type == "identifier" and origin is not None
                            and origin.type == "identifier" and self.document.text(origin) in aliases
                            and scope is not None and any(_key(ancestor) == _key(result["scope"]) for ancestor in _ancestors(scope))):
                            added.add(self.document.text(ident))
                    if added <= aliases:
                        break
                    aliases.update(added)
                writes = []
                for mutation in self.all_nodes:
                    if mutation.type not in {"assignment_expression", "augmented_assignment_expression", "update_expression", "for_in_statement"}:
                        continue
                    if mutation.type == "for_in_statement" and any(child.type in {"const", "let", "var", "lexical_declaration", "variable_declaration"} for child in mutation.children):
                        continue
                    left = mutation.child_by_field_name("left") or mutation.child_by_field_name("argument")
                    names = _bound_names(left, self.document) if left is not None and left.type != "member_expression" else set()
                    path = _member_path(left, self.document)
                    if not aliases.intersection(names) and not (path and path[0] in aliases):
                        continue
                    owner = _binding_scope(mutation)
                    # Include nested closures which can write a visible captured name;
                    # do not assert they execute, only refuse a negative proof.
                    if owner is not None and any(_key(ancestor) == _key(result["scope"]) for ancestor in _ancestors(owner)):
                        writes.append(self.document.location(mutation))
                if writes:
                    result.update(known=False, reason="visible_binding_or_member_write",
                        write_count=len(writes), write_locations=writes[:8], possible_aliases=sorted(aliases))
        escaped = []
        for node in self.all_nodes:
            patterns = []
            scope = _binding_scope(node)
            mutation = False
            if node.type == "variable_declarator":
                patterns = [node.child_by_field_name("name")]
                scope = _binding_scope(node, node.parent is not None and node.parent.type == "variable_declaration")
            elif node.type in {"assignment_expression", "augmented_assignment_expression", "for_in_statement"}:
                patterns = [node.child_by_field_name("left")]
                keyword = next((child.type for child in node.children if child.type in {"var", "const", "let"}), "")
                mutation = node.type != "for_in_statement" or not keyword
                if node.type == "for_in_statement" and keyword:
                    scope = _binding_scope(node, True) if keyword == "var" else node
            elif node.type == "update_expression":
                patterns = [node.child_by_field_name("argument")]
                mutation = True
            elif node.type in {"function_declaration", "generator_function_declaration", "class_declaration",
                    "enum_declaration", "internal_module", "import_alias"}:
                patterns = [node.child_by_field_name("name")]
            elif node.type in {"function_expression", "generator_function", "class", "class_expression"}:
                patterns = [node.child_by_field_name("name")]
                scope = node
            elif node.type in {"import_specifier", "namespace_import"}:
                patterns = [node.child_by_field_name("alias") or node.child_by_field_name("name")]
                scope = self.document.tree.root_node
            elif node.type == "import_clause":
                patterns = [child for child in node.named_children if child.type == "identifier"]
                scope = self.document.tree.root_node
            visible_scope = scope is not None and _key(scope) in ancestors
            if mutation and scope is not None:
                binding_scope = result.get("scope")
                if binding_scope is not None:
                    visible_scope = visible_scope or any(_key(ancestor) == _key(binding_scope) for ancestor in _ancestors(scope))
            for pattern in patterns:
                if pattern is not None and visible_scope and any(
                        child.type in {"identifier", "shorthand_property_identifier_pattern"} and "\\" in self.document.text(child)
                        for child in _walk(pattern)):
                    escaped.append(self.document.location(pattern))
        for owner in _ancestors(at):
            params = owner.child_by_field_name("parameters") or owner.child_by_field_name("parameter")
            if owner.type in _FUNCTIONS | {"catch_clause"} and params is not None and any(
                    child.type in {"identifier", "shorthand_property_identifier_pattern"} and "\\" in self.document.text(child) for child in _walk(params)):
                escaped.append(self.document.location(params))
        if escaped:
            result.update(known=False, reason="escaped_binding_or_write_not_decoded", escaped_binding_locations=escaped[:8])
        self.binding_cache[cache_key] = result
        return result

    def _binding_record(self, binding: dict) -> dict:
        public = {key: value for key, value in binding.items() if key not in {"node", "initializer", "scope"}}
        if binding.get("node") is not None:
            public["location"] = self.document.location(binding["node"])
            public["binding_id"] = _digest({"file": self.document.source.path, "source_hash": self.document.source.hash,
                "declaration": _key(binding["node"]), "scope": _key(binding["scope"]), "name": binding.get("name")})
        return public

    def read(self, value: Any, depth: int = 0, seen: frozenset[tuple] = frozenset()) -> dict:
        original, value = value, _unwrap(value)
        if value is None or depth > 20:
            return _unknown(self.document, original, "expression_or_origin_budget")
        location = self.document.location(original)
        kind, text = value.type, self.document.text(value)
        literal: Any = None
        literal_ok = kind in {"null", "true", "false", "number", "string"}
        if kind == "true":
            literal = True
        elif kind == "false":
            literal = False
        elif kind == "string":
            literal = _literal_string(text)
            literal_ok = literal is not None
        elif kind == "number":
            try:
                cleaned = text.replace("_", "")
                if len(cleaned) > 1 and cleaned[0] == "0" and cleaned[1].isdigit():
                    return _unknown(self.document, original, "legacy_leading_zero_number")
                literal = int(cleaned, 0) if cleaned.lower().startswith(("0x", "0b", "0o")) else float(cleaned) if "." in cleaned or "e" in cleaned.lower() else int(cleaned, 10)
                literal_ok = math.isfinite(literal) and abs(literal) <= 2**53 - 1 and not cleaned.endswith("n")
            except (ValueError, OverflowError):
                literal_ok = False
        if literal_ok:
            if type(literal) is float and literal.is_integer():
                literal = int(literal)
            return {"kind": "literal", "value": literal, "complete": True, "location": location, "runtime_value_known": False}
        if kind == "unary_expression":
            argument = value.child_by_field_name("argument")
            operator = value.child_by_field_name("operator")
            if operator is not None and self.document.text(operator) in {"+", "-"}:
                inner = self.read(argument, depth + 1, seen)
                if inner["kind"] == "literal" and type(inner.get("value")) in {int, float}:
                    number = inner["value"] * (-1 if self.document.text(operator) == "-" else 1)
                    if number == 0 and self.document.text(operator) == "-":
                        return _unknown(self.document, original, "negative_zero_not_modeled")
                    return {"kind": "literal", "value": number, "complete": True, "location": location, "runtime_value_known": False}
        if kind in {"identifier", "shorthand_property_identifier"}:
            if "\\" in text:
                return _unknown(self.document, original, "escaped_identifier")
            binding = self.binding(text, value)
            syntax = {"kind": "reference", "name": text}
            if not binding.get("known"):
                result = _unknown(self.document, original, binding.get("reason", "unknown_binding"), syntax)
                result["binding"] = self._binding_record(binding)
                return result
            result = {**syntax, "complete": True, "location": location,
                "binding": self._binding_record(binding), "runtime_value_known": False}
            initializer = binding.get("initializer")
            if initializer is not None:
                anchor = _key(binding["node"])
                origin = {"location": self.document.location(initializer),
                    "interpretation": "captured lexical initializer only; return value, aliases and heap state are not evaluated"}
                if depth < _ORIGIN_DEPTH and anchor not in seen and not binding.get("destructured"):
                    origin["expression"] = self.read(initializer, depth + 1, seen | {anchor})
                else:
                    origin["expression"] = _unknown(self.document, initializer, "destructured_or_origin_budget")
                result["origin"] = origin
            return result
        if kind == "member_expression":
            object_node, property_node = value.child_by_field_name("object"), value.child_by_field_name("property")
            if property_node is None or property_node.type not in {"identifier", "property_identifier"} or any(child.type == "optional_chain" for child in value.children) or "\\" in self.document.text(property_node):
                return _unknown(self.document, original, "dynamic_optional_or_escaped_member")
            obj = self.read(object_node, depth + 1, seen)
            return {"kind": "member", "object": obj, "property": self.document.text(property_node),
                "complete": bool(obj.get("complete")), "location": location, "runtime_value_known": False}
        if kind == "await_expression":
            operand = next((child for child in value.named_children if child.type != "comment"), None)
            result = self.read(operand, depth + 1, seen)
            return {**result, "location": location, "awaited": True, "runtime_value_known": False}
        if kind == "call_expression":
            callee = self.read(value.child_by_field_name("function"), depth + 1, seen)
            arguments_node = value.child_by_field_name("arguments")
            nodes = [child for child in arguments_node.named_children if child.type != "comment"] if arguments_node else []
            if len(nodes) > 32 or any(child.type == "spread_element" for child in nodes) or any(child.type == "optional_chain" for child in value.children):
                return _unknown(self.document, original, "call_argument_spread_optional_or_budget")
            arguments = [self.read(child, depth + 1, seen) for child in nodes]
            return {"kind": "call", "callee": callee, "arguments": arguments,
                "complete": bool(callee.get("complete")) and all(argument.get("complete") for argument in arguments),
                "location": location, "return_value_known": False, "runtime_value_known": False}
        if kind == "ternary_expression":
            condition = self.read(value.child_by_field_name("condition"), depth + 1, seen)
            consequent = self.read(value.child_by_field_name("consequence"), depth + 1, seen)
            alternative = self.read(value.child_by_field_name("alternative"), depth + 1, seen)
            return {"kind": "conditional", "operator": "?:", "condition": condition,
                "then": consequent, "else": alternative, "location": location,
                "complete": all(item.get("complete") for item in (condition, consequent, alternative)),
                "branch_reachability_known": False}
        if kind == "binary_expression":
            operator = value.child_by_field_name("operator")
            spelling = self.document.text(operator) if operator is not None else ""
            if spelling in {"||", "??", "&&"}:
                left = self.read(value.child_by_field_name("left"), depth + 1, seen)
                right = self.read(value.child_by_field_name("right"), depth + 1, seen)
                return {"kind": "conditional", "operator": spelling, "condition": left,
                    "then": right if spelling == "&&" else left, "else": left if spelling == "&&" else right,
                    "complete": bool(left.get("complete") and right.get("complete")), "location": location,
                    "default_semantics": "nullish" if spelling == "??" else "truthiness",
                    "branch_reachability_known": False}
        return _unknown(self.document, original, "unsupported_expression_form")


def _canonical(expression: dict) -> dict | None:
    if not expression.get("complete", True) or expression.get("kind") not in _SYMBOLIC_KINDS:
        return None
    kind = expression["kind"]
    if kind in {"literal", "reference"}:
        value = expression["value" if kind == "literal" else "name"]
        if kind == "literal" and type(value) is float and value.is_integer():
            value = int(value)
        result = {"kind": kind, "value" if kind == "literal" else "name": value}
        if kind == "reference" and expression.get("binding", {}).get("binding_id"):
            result["binding_id"] = expression["binding"]["binding_id"]
        return result
    keys = {"member": ("object",), "call": ("callee",), "conditional": ("condition", "then", "else")}[kind]
    result = {"kind": kind}
    for key in keys:
        value = _canonical(expression[key])
        if value is None:
            return None
        result[key] = value
    if kind == "member":
        result["property"] = expression["property"]
    elif kind == "conditional":
        result["operator"] = expression["operator"]
    else:
        result["arguments"] = [_canonical(argument) for argument in expression["arguments"]]
        if any(value is None for value in result["arguments"]):
            return None
    return result


def _source_forms(expression: dict, depth: int = 0) -> list[dict]:
    """Include an unmodified const alias's recorded source, without evaluation.

    This is a source-origin equivalence only. Calls are not substituted as
    runtime equivalents, and unknown/conditional origins do not prove that a
    reference evaluates to a different value.
    """
    direct = _canonical(expression)
    if direct is None or depth > _ORIGIN_DEPTH:
        return []
    forms = [direct]
    if expression["kind"] == "reference":
        binding, origin = expression.get("binding", {}), expression.get("origin", {}).get("expression", {})
        if binding.get("kind") == "const" and binding.get("known") and origin.get("kind") in {"reference", "member", "literal"}:
            forms.extend(_source_forms(origin, depth + 1))
    elif expression["kind"] == "member":
        for obj in _source_forms(expression["object"], depth + 1):
            forms.append({"kind": "member", "object": obj, "property": expression["property"]})
    unique = {_digest(form): form for form in forms}
    return list(unique.values())


def _expectation_origins(reader: _Reader, expected: dict, call: Any) -> tuple[list[dict], bool]:
    names: set[str] = set()
    pending = [expected]
    while pending:
        expression = pending.pop()
        if expression["kind"] == "reference":
            names.add(expression["name"])
        elif expression["kind"] == "member":
            pending.append(expression["object"])
        elif expression["kind"] == "call":
            pending.extend([expression["callee"], *expression["arguments"]])
        elif expression["kind"] == "conditional":
            pending.extend(expression[key] for key in ("condition", "then", "else"))
    bindings = []
    for name in sorted(names):
        binding = reader.binding(name, call)
        public = reader._binding_record(binding)
        initializer = binding.get("initializer")
        if initializer is not None:
            public["origin"] = {"location": reader.document.location(initializer),
                "expression": reader.read(initializer),
                "interpretation": "captured lexical initializer, not a return-value or heap-state evaluation"}
        bindings.append(public)
    return bindings, all(binding.get("known") for binding in bindings)


def _expected_expression(expected: dict, bindings: list[dict]) -> dict:
    """Resolve policy names at the callsite, retaining declaration identities."""
    by_name = {binding["name"]: binding for binding in bindings}
    kind = expected["kind"]
    result = {**expected, "complete": True}
    if kind == "reference":
        binding = by_name.get(expected["name"], {})
        result.update(binding=binding, complete=bool(binding.get("known")))
        if binding.get("origin"):
            result["origin"] = binding["origin"]
    elif kind == "member":
        result["object"] = _expected_expression(expected["object"], bindings)
        result["complete"] = result["object"]["complete"]
    elif kind == "call":
        result["callee"] = _expected_expression(expected["callee"], bindings)
        result["arguments"] = [_expected_expression(argument, bindings) for argument in expected["arguments"]]
        result["complete"] = result["callee"]["complete"] and all(argument["complete"] for argument in result["arguments"])
    elif kind == "conditional":
        for key in ("condition", "then", "else"):
            result[key] = _expected_expression(expected[key], bindings)
        result["complete"] = all(result[key]["complete"] for key in ("condition", "then", "else"))
    return result


def _property(document: _Document, obj: Any, name: str) -> tuple[Any, dict]:
    """Respect source order; a later spread can overwrite an earlier key."""
    obj = _unwrap(obj)
    if obj is None or obj.type != "object":
        return None, {"state": "unknown", "shape_closed": False, "field_closed": False,
            "reason": "argument_or_nested_path_is_not_literal_object"}
    selected, selected_index, occurrences = None, -1, 0
    barriers: list[dict] = []
    accessor = False
    for index, child in enumerate(obj.named_children):
        if child.type == "comment":
            continue
        key, value = None, None
        if child.type == "pair":
            key_node = child.child_by_field_name("key")
            value = child.child_by_field_name("value")
            if key_node is not None and key_node.type in {"property_identifier", "identifier"} and "\\" not in document.text(key_node):
                key = document.text(key_node)
            elif key_node is not None and key_node.type == "string" and "\\" not in document.text(key_node):
                key = _literal_string(document.text(key_node))
        elif child.type == "shorthand_property_identifier" and "\\" not in document.text(child):
            key, value = document.text(child), child
        elif child.type == "method_definition":
            key_node = child.child_by_field_name("name")
            if key_node is not None and key_node.type in {"property_identifier", "identifier"} and "\\" not in document.text(key_node):
                key = document.text(key_node)
                if key == name:
                    accessor = True
        if key is None or key == "__proto__":
            barriers.append({"index": index, "node_type": child.type, "location": document.location(child)})
        if key == name:
            occurrences += 1
            selected, selected_index = value, index
    record = {"field": name, "object_location": document.location(obj),
        "shape_closed": not barriers, "field_closed": False,
        "explicit_occurrences": occurrences, "barrier_count": len(barriers),
        "barrier_samples": barriers[:8], "barriers_truncated": len(barriers) > 8}
    if occurrences > 1:
        record.update(state="unknown", reason="duplicate_explicit_property")
    elif accessor:
        record.update(state="unknown", reason="getter_setter_or_method_value")
    elif selected is not None and not any(barrier["index"] > selected_index for barrier in barriers):
        record.update(state="present", field_closed=True, location=document.location(selected),
            interpretation="selected explicit field follows any earlier unknown keys/spreads; whole object need not be closed")
    elif selected is not None:
        record.update(state="unknown", reason="later_spread_computed_or_prototype_may_override")
    elif barriers:
        record.update(state="unknown", reason="unknown_keys_may_supply_missing_field")
    else:
        record.update(state="missing", field_closed=True)
    return selected if record["state"] == "present" else None, record


def _function(definition: _Definition) -> Any:
    if definition.node.type in _FUNCTIONS:
        return definition.node
    value = _unwrap(definition.value)
    return value if value is not None and value.type in _FUNCTIONS else None


def _direct_body_nodes(body: Any, document: _Document, callee: list[str]) -> tuple[list[Any], list[dict]]:
    nodes, gaps = [], []
    pending = [body]
    while pending:
        node = pending.pop()
        if node.type in _FUNCTIONS:
            # The expression body can itself be a returned inner function.
            # Such a root must be fenced just like a nested callback.
            continue
        if node.type in _CLASS_SCOPES | {"class_expression"}:
            if any(child.type == "call_expression"
                and _member_path(child.child_by_field_name("function"), document) == callee for child in _walk(node)):
                gaps.append(_issue("value_nested_class_scope", "同名调用出现在嵌套类初始化/继承/成员语法中，首版不把它归为外层直接调用。",
                    document.source.path, node.start_point.row + 1))
            continue
        nodes.append(node)
        pending.extend(reversed(node.named_children))
    return nodes, gaps


def _callee_evidence(snapshot: GraphSnapshot, document: _Document, call: Any, selector: dict, reader: _Reader) -> dict:
    function = call.child_by_field_name("function")
    paths = _member_path(function, document) or []
    binding = reader.binding(paths[0], function) if paths and function is not None else {"known": False, "reason": "dynamic_callee"}
    owners = [node for node in snapshot.nodes if node.file == selector["file"]
        and (node.qualname == selector["symbol"] or node.id.endswith("#" + selector["symbol"]))]
    matches = [edge for edge in snapshot.edges if edge.file == selector["file"]
        and edge.source in {node.id for node in owners}
        and edge.line == call.start_point.row + 1 and edge.column == call.start_point.column]
    target_nodes = [node for node in snapshot.nodes if len(matches) == 1 and node.id == matches[0].target]
    def endpoint_complete(node: Any) -> bool:
        files = [source for source in snapshot.files if source.path == node.file]
        return (len(files) == 1 and files[0].status in {"parsed", "complete", "ok", "analyzed"}
            and not any(node.metadata.get(key) for key in (
                "duplicate_definition", "multiple_module_contexts", "conditional_definition",
                "attribute_macros_unknown", "declaration_only")))
    resolved = (len(owners) == 1 and endpoint_complete(owners[0]) and len(matches) == 1
        and matches[0].resolution == "resolved" and len(target_nodes) == 1 and endpoint_complete(target_nodes[0]))
    return {"selector": selector["callee"], "syntax_matched": True,
        "syntax_location": document.location(function), "lexical_binding": reader._binding_record(binding),
        "graph_edge_ids": [edge.id for edge in matches], "graph_target": matches[0].target if resolved else None,
        "internal_binding_confirmed_by_snapshot": bool(resolved),
        "resolution": "resolved" if resolved else "unknown",
        "interpretation": "callee spelling selects source syntax; it does not establish actual runtime dispatch or transport"}


def _side(sources: _Sources, snapshot: GraphSnapshot, selector: dict, expected: dict) -> tuple[dict, list[dict]]:
    document, definition, problems = sources.select(selector)
    result = {"selector": selector, "expected": expected, "calls": [], "call_count": 0,
        "comparison": "unknown", "source_fact_confirmed": False}
    if document is None or definition is None:
        return result, problems
    if document.kind not in {"typescript", "tsx"}:
        return result, [*problems, _issue("value_language_unsupported", "值来源首版只支持捕获的 TS/JS AST。", selector["file"])]
    function = _function(definition)
    if function is None:
        return result, [*problems, _issue("value_subject_not_callable", "词法 symbol 未绑定到唯一函数主体。", selector["file"])]
    body = function.child_by_field_name("body")
    if body is None:
        return result, [*problems, _issue("value_body_missing", "所选函数没有捕获主体。", selector["file"])]
    nodes, scope_gaps = _direct_body_nodes(body, document, selector["callee"].split("."))
    problems.extend(scope_gaps)
    calls = [node for node in nodes if node.type == "call_expression"
        and _member_path(node.child_by_field_name("function"), document) == selector["callee"].split(".")]
    result.update(symbol=definition.symbol, location=document.location(function), call_count=len(calls),
        evaluation="all syntax direct calls, excluding nested function and callback bodies",
        nested_function_bodies_excluded=True, nested_class_scopes_not_inferred=True,
        scope_complete=not scope_gaps)
    if not calls:
        return result, [*problems, _issue("value_callsite_missing", "直接函数主体没有匹配的 callee AST；不把别名/嵌套函数调用替代为命中。", selector["file"])]
    if len(calls) > _CALL_LIMIT:
        return result, [*problems, _issue("value_callsite_budget", f"匹配 {len(calls)} 个调用，超出 {_CALL_LIMIT} 范围，不能确认 all_direct_calls。", selector["file"])]
    comparisons, facts = [], []
    for call in calls:
        reader = _Reader(document, function, call)
        callee = _callee_evidence(snapshot, document, call, selector, reader)
        arguments_node = call.child_by_field_name("arguments")
        arguments = [node for node in arguments_node.named_children if node.type != "comment"] if arguments_node is not None else []
        argument_index = selector["argument_index"]
        fact = {"call_location": document.location(call), "callee": callee,
            "enclosing_conditions": _branch_conditions(document, call, function),
            "object_path": selector["object_path"], "path_facts": [], "comparison": "unknown"}
        expected_bindings, expected_bound = _expectation_origins(reader, expected, call)
        fact["expected_lexical_bindings"] = expected_bindings
        fact["expected_binding_complete"] = expected_bound
        expected_expression = _expected_expression(expected, expected_bindings)
        fact["expected_source_origin_forms"] = _source_forms(expected_expression)
        if not expected_bound:
            problems.append(_issue("value_expected_binding_unknown", "配置期待的词法名称未唯一、稳定绑定；不能据不同名字确认来源合同差异。", selector["file"], call.start_point.row + 1))
        if argument_index >= len(arguments) or any(node.type == "spread_element" for node in arguments[:argument_index + 1]):
            fact["actual"] = _unknown(document, call, "argument_missing_or_spread_position_unknown")
            problems.append(_issue("value_argument_unknown", "调用参数位置缺失或被展开参数影响。", selector["file"], call.start_point.row + 1))
        else:
            value, missing, unknown = arguments[argument_index], False, False
            fact["argument_location"] = document.location(value)
            for name in selector["object_path"]:
                value, shape = _property(document, value, name)
                fact["path_facts"].append(shape)
                if shape["state"] == "missing":
                    missing = True
                    break
                if shape["state"] == "unknown":
                    unknown = True
                    break
            if missing:
                fact["actual"] = {"kind": "unknown", "reason": "closed_literal_object_field_missing", "complete": False}
                fact["comparison"] = "mismatch" if expected_bound else "unknown"
                fact["source_fact_confirmed"] = True
            elif unknown:
                fact["actual"] = _unknown(document, arguments[argument_index], "object_path_not_closed")
                problems.append(_issue("value_object_unknown", "对象字段被别名、展开、动态键、访问器或重复属性影响，不能作封闭负证。", selector["file"], call.start_point.row + 1))
            else:
                fact["actual"] = reader.read(value)
                actual = _canonical(fact["actual"])
                if actual is None:
                    problems.append(_issue("value_expression_unknown", "字段表达式/词法绑定未在有限模型中闭合。", selector["file"], value.start_point.row + 1))
                else:
                    forms = _source_forms(fact["actual"])
                    fact["source_origin_forms"] = forms
                    if not expected_bound:
                        fact["comparison"] = "unknown"
                    else:
                        fact["comparison"] = "matches" if {_digest(form) for form in fact["expected_source_origin_forms"]}.intersection(
                            _digest(form) for form in forms) else "mismatch"
                    fact["comparison_semantics"] = "captured expression/origin form, not runtime value equality"
                    fact["source_fact_confirmed"] = True
        comparisons.append(fact["comparison"])
        facts.append(fact)
    samples = sorted(facts, key=lambda fact: {"mismatch": 0, "unknown": 1, "matches": 2}[fact["comparison"]])
    result.update(calls=samples[:_FACT_SAMPLE_LIMIT], calls_truncated=len(facts) > _FACT_SAMPLE_LIMIT,
        call_sample_limit=_FACT_SAMPLE_LIMIT, comparison=("mismatch" if "mismatch" in comparisons
            else "unknown" if "unknown" in comparisons else "matches"),
        all_direct_calls_closed="unknown" not in comparisons and not scope_gaps,
        source_fact_confirmed=any(fact.get("source_fact_confirmed") for fact in facts),
        mismatch_count=comparisons.count("mismatch"), unknown_count=comparisons.count("unknown"),
        matches_count=comparisons.count("matches"),
        call_sample_order="mismatch_then_unknown_then_matches",
        callee_binding_complete=all(fact["callee"]["internal_binding_confirmed_by_snapshot"] for fact in facts))
    if scope_gaps and result["comparison"] == "matches":
        result["comparison"] = "unknown"
    return result, problems


def _finding(snapshot: GraphSnapshot, rule: dict, fact: dict, problems: list[dict], refs: list[dict]) -> Finding:
    conditional = rule.get("applicability", {}).get("kind") == "conditional"
    subject, producer = fact.get("subject", {}), fact.get("producer")
    callee_unknown = not subject.get("callee_binding_complete") or (producer is not None and not producer.get("callee_binding_complete"))
    unknown = list(problems)
    if callee_unknown:
        unknown.append(_issue("callee_target_not_inferred", "命中 callee 源码表达式不证明其动态导入/运行分派目标。"))
    if conditional or producer is not None:
        unknown.append(_issue("value_transport_not_inferred", "适用条件、入口可达性和 producer→consumer 运输仅为外部合同，没有按同名字段推导。"))
    if subject.get("comparison") == "mismatch" or (producer is not None and producer.get("comparison") == "mismatch"):
        unknown.append(_issue("value_equivalence_not_inferred", "来源形式不同不证明运行值不同；输入、等价表达式、别名堆变化或分支执行尚未计算。"))
    fingerprint = _digest({"project_id": snapshot.project_id, "version": VERSION,
        "policy_version": POLICY_VERSION, "rule": rule})
    locations = []
    for side in [subject, producer]:
        if not isinstance(side, dict):
            continue
        if side.get("location"):
            locations.append(side["location"])
        for call in side.get("calls", []):
            locations.append(call["call_location"])
            if call.get("actual", {}).get("location"):
                locations.append(call["actual"]["location"])
    locations.extend(ref["location"] for ref in refs if ref.get("location"))
    paths = {location["file"] for location in locations}
    symbols = {side.get("symbol") for side in (subject, producer) if isinstance(side, dict)}
    node_ids = sorted({node.id for node in snapshot.nodes if node.file in paths and (
        node.qualname in symbols or any(symbol and node.id.endswith("#" + symbol) for symbol in symbols))})
    mismatch = subject.get("comparison") == "mismatch" or (producer is not None and producer.get("comparison") == "mismatch")
    title = "调用参数来源形式待复核" if mismatch else "调用参数来源合同无法完整确认"
    description = "比较保存源码中的调用参数表达式与配置来源；词法初始化记录不计算函数返回、运行值或别名堆状态。"
    if producer is not None:
        description += " 生产者与消费者是两个独立 AST 事实，跨边界传递尚未证明。"
    details = {"analyzer_version": VERSION, "policy_version": POLICY_VERSION, "snapshot_id": snapshot.id,
        "source_hash": snapshot.source_hash, "policy_hash": snapshot.policy_hash, "contract_hash": _digest(rule),
        "snapshot_parser_version": snapshot.parser_version, "source_fact": fact,
        "provenance": rule.get("provenance", {}), "applicability": rule.get("applicability", {}),
        "transport": rule.get("transport"), "guard_and_counterexample_sources": refs, "unknown": unknown,
        "captured_source_inputs": [{"file": source.path, "source_hash": source.hash, "status": source.status}
            for source in snapshot.files if source.path in paths],
        "analysis_scope": {"language": "TS/JS", "value_model": "finite captured expression and lexical initializer syntax",
            "call_coverage": "all direct syntax calls excluding nested functions",
            "runtime_value_proof": False, "cross_process_transport_proof": False,
            "branch_reachability_proof": False, "target_code_executed": False,
            "source_doc_is_label_only": True}}
    evidence = Evidence(_digest({"snapshot": snapshot.id, "fingerprint": fingerprint, "details": details})[:24],
        "static_value_analysis", description, locations=locations, node_ids=node_ids, details=details)
    return Finding(id=_digest({"snapshot": snapshot.id, "fingerprint": fingerprint})[:24],
        type="static_value_call_argument_value", severity=rule.get("severity", "medium"),
        status="uncertain" if conditional or unknown else "open", title=title, description=description,
        node_ids=node_ids, evidence=[evidence], rule_id=rule.get("id", "invalid-value-rule"),
        fingerprint=fingerprint, snapshot_id=snapshot.id,
        metadata={"value_analyzer_version": VERSION, "value_policy_version": POLICY_VERSION,
            "contract_hash": _digest(rule), "provenance": rule.get("provenance", {}),
            "applicability": rule.get("applicability", {}), "comparison": subject.get("comparison", "unknown"),
            "producer_comparison": producer.get("comparison") if producer is not None else None,
            "source_fact_confirmed": bool(mismatch and (subject.get("source_fact_confirmed") or producer is not None and producer.get("source_fact_confirmed"))),
            "source_form_difference_confirmed": bool(mismatch and (subject.get("source_fact_confirmed") or producer is not None and producer.get("source_fact_confirmed"))),
            "runtime_proof": False, "transport_proof": False})


def analyze_value_contracts(snapshot: GraphSnapshot, rules: list[dict]) -> list[Finding]:
    """Return static mismatches/unknowns; empty output is not a runtime pass."""
    if not isinstance(rules, list):
        return [_finding(snapshot, {"id": "invalid-value-rules", "severity": "info"}, {},
            [_issue("value_rules_invalid", "值合同必须是规则列表。")], [])]
    sources, findings = _Sources(snapshot), []
    counts: dict[str, int] = {}
    for rule in rules:
        if isinstance(rule, dict) and isinstance(rule.get("id"), str):
            counts[rule["id"]] = counts.get(rule["id"], 0) + 1
    for index, rule in enumerate(rules):
        try:
            validate_value_rule(rule)
            if counts.get(rule["id"]) != 1:
                raise ValueError("值合同 id 重复，不能覆盖前一条规则。")
        except (ValueError, TypeError, OverflowError, RecursionError) as exc:
            findings.append(_finding(snapshot, {"id": f"invalid-value-rule-{index}", "severity": "info"}, {},
                [_issue("value_rule_invalid", str(exc))], []))
            continue
        refs, problems = [], []
        selectors = list(rule.get("source_evidence", []))
        if rule["applicability"].get("guard"):
            selectors.insert(0, {**rule["applicability"]["guard"], "role": "guard"})
        for selector in selectors:
            reference, current = _source_reference(sources, selector)
            problems.extend(current)
            if reference is not None:
                refs.append(reference)
        subject, current = _side(sources, snapshot, rule["subject"], rule["expected"])
        problems.extend(current)
        fact = {"subject": subject, "producer": None, "transport_inferred": False,
            "interpretation": "explicit policy source-expression comparison; not end-to-end value or business proof"}
        if rule.get("producer") is not None:
            producer, current = _side(sources, snapshot, rule["producer"]["subject"], rule["producer"]["expected"])
            fact["producer"] = producer
            problems.extend(current)
        producer_comparison = fact["producer"].get("comparison") if fact["producer"] else "matches"
        if problems or subject["comparison"] != "matches" or producer_comparison != "matches":
            findings.append(_finding(snapshot, rule, fact, problems, refs))
    return findings
