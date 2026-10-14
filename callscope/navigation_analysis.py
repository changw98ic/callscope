"""Captured-source navigation/query contracts, never browser execution.

Policy selects source entrances and a factory/callback context. Query keys,
argument/parameter mappings, returns and null guards are inferred from the
saved CST and authenticated snapshot bindings. Platform navigation and event
timing remain external assumptions; UI port usage is not inferred here.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import parse_qsl

from .models import Evidence, Finding, GraphSnapshot
from .semantic_sources import SemanticSources, VERSION as SOURCE_VERSION, _issue
from .lexical_bindings import LexicalBindings, VERSION as LEXICAL_VERSION
from .semantic_environment import BuiltinEnvironment, VERSION as ENVIRONMENT_VERSION
from .completion_summaries import function_kind, completion_relation, VERSION as COMPLETION_VERSION
from .static_contracts import _digest, _path, _string, _walk, _unwrap, _literal_string, _FUNCTIONS, _CLASS_SCOPES
from .value_analysis import _json_data, _Reader, _bound_names, _binding_scope, _key, _member_path

VERSION = "static-navigation-contracts-2-shared"
POLICY_VERSION = "static-navigation-policy-v1"
_MODELS = {"url-search-params-v1", "js-string-url-slicing-v1", "object-freeze-inert-v1"}
_MAX_CALL_DEPTH = 12
_MAX_LOOP_KEYS = 64
_MAX_TRACE = 256


def _entrance(value: Any) -> None:
    if not isinstance(value, dict) or not _path(value.get("file")) or not _string(value.get("symbol")):
        raise ValueError("导航入口需要项目内 file 和精确 lexical symbol。")
    if value.get("site") == "assignment":
        if set(value) != {"file", "symbol", "site", "target"} or not isinstance(value["target"], list) or not 2 <= len(value["target"]) <= 16 or not all(_string(part) for part in value["target"]):
            raise ValueError("assignment 入口需要静态 target 路径，不能配置输出键。")
    elif value.get("site") == "call":
        if set(value) != {"file", "symbol", "site", "callee"} or not _string(value["callee"]) or any(not part.isidentifier() for part in value["callee"].split(".")):
            raise ValueError("call 入口需要唯一静态 callee 路径。")
    else:
        raise ValueError("导航入口 site 仅支持 assignment 或 call。")


def validate_navigation_rule(rule: Any) -> None:
    _json_data(rule)
    if not isinstance(rule, dict) or set(rule) - {"id", "type", "severity", "producer", "consumer", "models", "ambient", "provenance", "applicability", "counterexample_producers", "wiring"}:
        raise ValueError("导航合同只能包含固定静态选择器、模型和外部条件。")
    if not _string(rule.get("id")) or rule.get("type") != "navigation_query_context":
        raise ValueError("导航合同需要 id/type=navigation_query_context。")
    if not isinstance(rule.get("severity", "medium"), str) or rule.get("severity", "medium") not in {"high", "medium", "low", "info"}:
        raise ValueError("导航 severity 无效。")
    _entrance(rule.get("producer"))
    counterexamples = rule.get("counterexample_producers", [])
    if not isinstance(counterexamples, list) or len(counterexamples) > 8:
        raise ValueError("counterexample_producers 最多选择 8 个真实源码入口。")
    for selector in counterexamples:
        _entrance(selector)
    consumer = rule.get("consumer")
    if not isinstance(consumer, dict) or set(consumer) != {"file", "symbol", "factory_callee", "argument_index", "callback_property", "returned_method"}:
        raise ValueError("consumer 需要 file/symbol/factory_callee/argument_index/callback_property/returned_method。")
    if not _path(consumer["file"]) or not all(_string(consumer[key]) for key in ("symbol", "factory_callee", "callback_property", "returned_method")):
        raise ValueError("consumer 选择器不完整。")
    if any(not part.isidentifier() for part in consumer["factory_callee"].split(".")) or type(consumer["argument_index"]) is not int or not 0 <= consumer["argument_index"] <= 16:
        raise ValueError("factory_callee/argument_index 无效。")
    models = rule.get("models")
    if not isinstance(models, list) or any(not isinstance(model, str) for model in models) or set(models) != _MODELS or len(models) != len(_MODELS):
        raise ValueError("必须显式注册三个固定版本的 URLSearchParams、字符串和 Object.freeze 标准模型。")
    ambient = rule.get("ambient")
    if not isinstance(ambient, dict) or set(ambient) != {"kind", "read_path", "conditions"} or ambient.get("kind") != "navigation_hash_stability":
        raise ValueError("ambient 仅支持明确的 navigation_hash_stability 外部假设。")
    if not isinstance(ambient["read_path"], list) or not 2 <= len(ambient["read_path"]) <= 16 or not all(_string(part) for part in ambient["read_path"]):
        raise ValueError("ambient.read_path 必须选实际捕获读取路径。")
    if not isinstance(ambient["conditions"], list) or not ambient["conditions"] or not all(_string(item) for item in ambient["conditions"]):
        raise ValueError("ambient 必须保留导航效果和读取稳定性条件。")
    provenance = rule.get("provenance")
    if not isinstance(provenance, dict) or set(provenance) - {"authority", "reviewer", "author_approved", "source_doc", "note"} or not _string(provenance.get("authority")) or not _string(provenance.get("source_doc")) or type(provenance.get("author_approved")) is not bool:
        raise ValueError("provenance 需要来源标签和作者是否审批；不会读取 source_doc。")
    applicability = rule.get("applicability")
    if not isinstance(applicability, dict) or set(applicability) - {"kind", "conditions", "counterexamples"} or applicability.get("kind") != "conditional":
        raise ValueError("首版导航合同必须为 conditional，不认证完整功能失败。")
    for key in ("conditions", "counterexamples"):
        values = applicability.get(key, [])
        if not isinstance(values, list) or not all(_string(item) for item in values):
            raise ValueError("applicability 条件/反证必须是说明字符串。")
    if not applicability.get("conditions"):
        raise ValueError("导航组合合同不得省略适用条件。")
    wiring = rule.get("wiring")
    if wiring is not None:
        if not isinstance(wiring, dict) or set(wiring) != {"boot", "injection", "use"}:
            raise ValueError("wiring 仅接受 boot/injection/use 来源角色。")
        schemas = {"boot": {"file", "callee", "argument_index"},
            "injection": {"file", "symbol", "callee", "argument_index", "property"},
            "use": {"file", "symbol", "parameter_index", "property", "returned_method", "method"}}
        for role, keys in schemas.items():
            selector = wiring[role]
            if not isinstance(selector, dict) or set(selector) != keys or not _path(selector.get("file")):
                raise ValueError("wiring 角色只能配置固定来源选择器，不能含结果或绑定链。")
            for key in keys - {"file", "argument_index", "parameter_index"}:
                if not _string(selector[key]):
                    raise ValueError("wiring 名称选择器无效。")
            for key in keys & {"argument_index", "parameter_index"}:
                if type(selector[key]) is not int or not 0 <= selector[key] <= 16:
                    raise ValueError("wiring 参数位置无效。")


@dataclass
class _Domain:
    guaranteed: set[str] = field(default_factory=set)
    possible: set[str] = field(default_factory=set)
    closed: bool = True
    gaps: list[str] = field(default_factory=list)

    def public(self) -> dict:
        return {"guaranteed_keys": sorted(self.guaranteed), "possible_keys": sorted(self.possible),
            "keyset_closed": self.closed, "unknown_keys": not self.closed, "unknown_reasons": sorted(set(self.gaps)),
            "invariant": "guaranteed subset actual subset possible only when keyset_closed"}

    def uncertain(self, reason: str) -> None:
        self.closed = False
        self.guaranteed.clear()
        self.gaps.append(reason)

    def join(self, other: _Domain) -> _Domain:
        return _Domain(self.guaranteed & other.guaranteed, self.possible | other.possible,
            self.closed and other.closed, [*self.gaps, *other.gaps])


@dataclass
class _Value:
    kind: str
    uid: str
    data: Any = None
    parts: list[Any] = field(default_factory=list)
    domain: _Domain | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    def public(self) -> dict:
        result = {"kind": self.kind, "source_value_id": self.uid}
        if self.kind in {"literal", "number", "boolean", "null"}:
            result["value"] = self.data
        if self.domain is not None:
            result["query_domain"] = self.domain.public()
        if self.kind == "string":
            result["segments"] = [{"kind": "literal", "text": part} if isinstance(part, str)
                else {"kind": part.kind, "source_value_id": part.uid} for part in self.parts]
            result["exact_text"] = "".join(self.parts) if not self.extra.get("summarized_hash") and all(isinstance(part, str) for part in self.parts) else None
        if self.extra.get("query_projection"):
            result["query_projection"] = deepcopy(self.extra["query_projection"])
        result["runtime_execution_proven"] = False
        return result


@dataclass
class _Frame:
    document: Any
    definition: Any
    function: Any
    env: dict[str, _Value] = field(default_factory=dict)
    ambient: _Value | None = None
    ambient_path: list[str] = field(default_factory=list)
    callbacks: dict[tuple[str, str], Any] = field(default_factory=dict)
    mode: str = "helper"
    context_id: str = ""
    queryless_projection: dict | None = None

    def fork(self) -> _Frame:
        return _Frame(self.document, self.definition, self.function, deepcopy(self.env),
            deepcopy(self.ambient), list(self.ambient_path), dict(self.callbacks), self.mode,
            self.context_id, deepcopy(self.queryless_projection))


def _function(definition: Any) -> Any:
    value = _unwrap(definition.value) if definition.value is not None else definition.node
    return value if value is not None and value.type in _FUNCTIONS else None


def _direct(node: Any):
    pending = [node]
    while pending:
        current = pending.pop()
        if current != node and current.type in _FUNCTIONS | _CLASS_SCOPES | {"class_expression"}:
            continue
        yield current
        pending.extend(reversed(current.named_children))


def _conditions(document: Any, node: Any, boundary: Any) -> list[dict]:
    result = []
    child, parent = node, node.parent
    while parent is not None and parent != boundary:
        if parent.type in {"if_statement", "ternary_expression"}:
            condition = parent.child_by_field_name("condition")
            then, otherwise = parent.child_by_field_name("consequence"), parent.child_by_field_name("alternative")
            branch = "then" if then is not None and then.start_byte <= child.start_byte < then.end_byte else "else" if otherwise is not None and otherwise.start_byte <= child.start_byte < otherwise.end_byte else "condition"
            if condition is not None:
                result.append({"branch": branch, "condition": document.text(condition), "location": document.location(condition)})
        child, parent = parent, parent.parent
    return result


def _simple_parameter(parameter: Any) -> Any:
    if parameter is None or parameter.type in {"optional_parameter", "rest_pattern", "assignment_pattern"} or parameter.child_by_field_name("value") is not None:
        return None
    if any(child.type in {"?", "...", "="} for child in parameter.children):
        return None
    pattern = parameter.child_by_field_name("pattern") or parameter.child_by_field_name("name") or parameter
    return pattern if pattern.type == "identifier" else None


class _Engine:
    def __init__(self, snapshot: GraphSnapshot, sources: SemanticSources, rule: dict):
        self.snapshot, self.sources, self.rule = snapshot, sources, rule
        self.trace: list[dict] = []
        self.gaps: list[dict] = []
        self.lookups: list[dict] = []
        self.stack: list[str] = []
        self.counter = 0
        self._reader_cache: dict[tuple, _Reader] = {}
        self._builtin_cache: dict[tuple, bool] = {}
        self._lexical_cache: dict[str, LexicalBindings] = {}
        self._environment_cache: dict[str, BuiltinEnvironment] = {}

    def lexical(self, document: Any) -> LexicalBindings:
        if document.source.path not in self._lexical_cache:
            self._lexical_cache[document.source.path] = LexicalBindings(document)
        return self._lexical_cache[document.source.path]

    def environment(self, document: Any) -> BuiltinEnvironment:
        if document.source.path not in self._environment_cache:
            self._environment_cache[document.source.path] = BuiltinEnvironment(document)
        return self._environment_cache[document.source.path]

    def value(self, kind: str, data: Any = None, **kwargs: Any) -> _Value:
        self.counter += 1
        return _Value(kind, f"abstract-{self.counter}", data, **kwargs)

    def unknown(self, reason: str, frame: _Frame | None = None, node: Any = None, gap: bool = False) -> _Value:
        if gap:
            self.gaps.append(_issue(reason, "有限导航来源模型未闭合。", frame.document.source.path if frame else "",
                node.start_point.row + 1 if node is not None else 0))
        return self.value("unknown", extra={"reason": reason})

    def event(self, operation: str, frame: _Frame, node: Any, **details: Any) -> None:
        if len(self.trace) >= _MAX_TRACE:
            if not any(gap["code"] == "navigation_trace_budget" for gap in self.gaps):
                self.gaps.append(_issue("navigation_trace_budget", "来源事件超过展示范围，不能宣称完整来源链。"))
            return
        location = frame.document.location(node)
        self.trace.append({"id": _digest({"op": operation, "location": location, "details": details})[:24],
            "operation": operation, "owner": frame.definition.symbol,
            "ast_owner_id": frame.document.call_owner(node), "location": location, **details})

    def reader(self, frame: _Frame) -> _Reader:
        cache_key = (frame.document.source.path, frame.function.start_byte, frame.function.end_byte)
        if cache_key not in self._reader_cache:
            self._reader_cache[cache_key] = _Reader(frame.document, frame.function, frame.function)
        return self._reader_cache[cache_key]

    def binding(self, frame: _Frame, name: str, at: Any) -> tuple[dict, str]:
        binding = self.reader(frame).binding(name, at)
        public = self.reader(frame)._binding_record(binding)
        return binding, public.get("binding_id", "")

    def bind(self, frame: _Frame, declaration: Any, name: str, value: _Value, scope: Any = None) -> None:
        scope = scope or _binding_scope(declaration)
        key = _digest({"file": frame.document.source.path, "source_hash": frame.document.source.hash,
            "declaration": _key(declaration), "scope": _key(scope), "name": name})
        frame.env[key] = value

    def builtin(self, frame: _Frame, name: str, at: Any, member: str | None = None) -> bool:
        cache_key = (frame.document.source.path, name, member, at.start_byte)
        if cache_key in self._builtin_cache:
            return self._builtin_cache[cache_key]
        audit = self.environment(frame.document).audit(name, at, member)
        valid = audit.get("supported") is True
        self._builtin_cache[cache_key] = valid
        if not valid:
            self.gaps.append(_issue("navigation_standard_binding_unknown", f"{name} 有遮蔽/显式写入或不完整名称环境，拒绝标准模型。",
                frame.document.source.path, at.start_point.row + 1, environment_audit=audit))
        else:
            self.event("captured_standard_api_environment", frame, at, name=name,
                member=member, lexical_absence=audit.get("lexical_absence"), environment_audit=audit,
                semantic_environment_version=ENVIRONMENT_VERSION, lexical_model_version=LEXICAL_VERSION,
                visible_api_audit_scope=audit.get("source", {}).get("audit_scope"), opaque_host_effects_proven=False,
                runtime_builtin_verified=False, standard_implementation_assumed=True)
        return valid

    def lookup(self, frame: _Frame, node: Any) -> _Value:
        name = frame.document.text(node)
        binding, key = self.binding(frame, name, node)
        if key in frame.env and binding.get("reason") not in {"visible_binding_or_member_write", "escaped_binding_or_write_not_decoded"}:
            return frame.env[key]
        if binding.get("known") and binding.get("kind") == "const" and not binding.get("destructured") and binding.get("initializer") is not None:
            scope = binding.get("scope")
            ancestor = scope
            while ancestor is not None and ancestor.type not in _FUNCTIONS:
                ancestor = ancestor.parent
            if ancestor is not None and ancestor != frame.function:
                # Re-evaluating a closure's outer initializer would create a
                # different abstract heap object. The first model only uses
                # captured immutable literal strings/arrays across scopes.
                initializer = _unwrap(binding["initializer"])
                if initializer is None or any(child.type in {"identifier", "new_expression", "member_expression", "subscript_expression"}
                        for child in _walk(initializer)):
                    self.invalidate(frame, "outer_heap_capture_not_modeled")
                    return self.unknown("outer_heap_capture_not_modeled", frame, node, True)
            anchor = f"initializer:{key}"
            if anchor in self.stack:
                return self.unknown("navigation_initializer_cycle", frame, node, True)
            self.stack.append(anchor)
            value = self.eval(frame, binding["initializer"])
            self.stack.pop()
            frame.env[key] = value
            self.event("lexical_const_origin", frame, binding["node"], binding_id=key, value=value.public())
            return value
        return self.unknown("unknown_parameter_or_lexical_value")

    def join(self, left: _Value, right: _Value) -> _Value:
        if left.kind == right.kind and left.kind in {"null", "number", "boolean", "literal"} and left.data == right.data:
            return left
        if left.kind == right.kind == "params":
            return self.projection_join(self.value("params", domain=left.domain.join(right.domain), extra={**left.extra, "joined": True}), left, right)
        if left.kind == right.kind == "serialized":
            return self.projection_join(self.value("serialized", domain=left.domain.join(right.domain)), left, right)
        if left.kind == right.kind == "string":
            domain = self.hash_domain(left).join(self.hash_domain(right))
            exact = left.parts == right.parts
            return self.projection_join(self.value("string", parts=left.parts if exact else [], domain=domain,
                extra={"summarized_hash": not exact or left.extra.get("summarized_hash") or right.extra.get("summarized_hash"),
                    "raw_domain": self.query_domain(left, True).join(self.query_domain(right, True)),
                    "has_query": self.has_query(left) if self.has_query(left) == self.has_query(right) else None}), left, right)
        return self.unknown("branch_values_not_equal")

    def projection_join(self, result: _Value, left: _Value, right: _Value) -> _Value:
        a, b = left.extra.get("query_projection", {}), right.extra.get("query_projection", {})
        guaranteed = set(a.get("guaranteed_contexts", [])) & set(b.get("guaranteed_contexts", []))
        possible = set(a.get("possible_contexts", [])) | set(b.get("possible_contexts", []))
        same_view = bool(a.get("view") and a.get("view") == b.get("view"))
        if not same_view:
            guaranteed.clear()
        if guaranteed or possible:
            result.extra["query_projection"] = {"guaranteed_contexts": sorted(guaranteed), "possible_contexts": sorted(possible),
                "relation": "branch_join_of_query_key_preserving_projections", "inputs": [left.uid, right.uid],
                "view": a.get("view") if same_view else "unknown",
                "input_relations": sorted({value.get("relation", "") for value in (a, b) if value})}
        else:
            result.extra.pop("query_projection", None)
        return result

    def projected(self, result: _Value, source: _Value, relation: str, location: dict | None = None) -> _Value:
        projection = source.extra.get("query_projection")
        transformations = {"data_query_tail_of_bound_hash": ("hash", "raw_query"),
            "url_search_params_string_seed_preserves_query_keys": ("raw_query", "params"),
            "query_serialization_preserves_key_presence": ("params", "raw_query")}
        expected, produced = transformations.get(relation, (None, None))
        if projection and expected is not None and projection.get("view") == expected:
            result.extra["query_projection"] = {"guaranteed_contexts": list(projection.get("guaranteed_contexts", [])),
                "possible_contexts": list(projection.get("possible_contexts", [])), "relation": relation,
                "input_value_id": source.uid, "input_relation": projection.get("relation"),
                "view": produced,
                "source_location": location, "original_query_keys_preserved": True}
        return result

    def merge_frames(self, frame: _Frame, branches: list[_Frame]) -> None:
        aliases: dict[tuple[str, ...], _Value] = {}
        for key in set().union(*(set(branch.env) for branch in branches)):
            values = [branch.env.get(key, self.unknown("branch_binding_missing")) for branch in branches]
            alias_key = tuple(value.uid for value in values)
            current = aliases.get(alias_key)
            if current is None:
                current = values[0]
                for value in values[1:]:
                    current = self.join(current, value)
                aliases[alias_key] = current
            frame.env[key] = current

    def query_domain(self, value: _Value, raw: bool = False) -> _Domain:
        if value.kind in {"params", "serialized"}:
            return deepcopy(value.domain)
        if value.kind != "string":
            return _Domain(closed=False, gaps=["unknown_query_seed"])
        if value.extra.get("summarized_hash"):
            domain = value.extra.get("raw_domain") if raw else value.domain
            return deepcopy(domain) if domain is not None else _Domain(closed=False, gaps=["summary_context_conversion_unknown"])
        if raw and value.extra.get("query_text") and value.domain is not None and not value.extra.get("summarized_hash"):
            return deepcopy(value.domain)
        if all(isinstance(part, str) for part in value.parts):
            text = "".join(value.parts)
            if not raw:
                text = text.split("?", 1)[1] if "?" in text else ""
            elif text.startswith("?"):
                text = text[1:]
            keys = {key for key, _ in parse_qsl(text, keep_blank_values=True, errors="replace", separator="&")}
            return _Domain(set(keys), set(keys))
        # Encoded pieces cannot introduce query delimiters. They are supported
        # only in a value position, not as unknown key names or separators.
        parts = list(value.parts)
        if not raw:
            found = False
            tail = []
            for part in parts:
                if found:
                    tail.append(part)
                elif isinstance(part, str) and "?" in part:
                    found = True
                    tail.append(part.split("?", 1)[1])
                elif not isinstance(part, str) and not (part.kind == "encoded" or part.kind == "string" and self.has_query(part) is False):
                    return _Domain(closed=False, gaps=["unknown_template_query_delimiter"])
            if not found:
                return _Domain()
            parts = [part for part in tail if not isinstance(part, str) or part]
        if len(parts) == 1 and isinstance(parts[0], _Value) and parts[0].kind == "serialized":
            return deepcopy(parts[0].domain)
        keys, key, in_value = set(), "", False
        for part in parts:
            if isinstance(part, _Value):
                if part.kind != "encoded" or not in_value:
                    return _Domain(closed=False, gaps=["unknown_template_key_or_query_tail"])
                continue
            for character in part:
                if character == "&":
                    if key or in_value:
                        keys.add(parse_qsl(key + "=x", keep_blank_values=True, separator="&")[0][0])
                    key, in_value = "", False
                elif character == "=" and not in_value:
                    in_value = True
                elif not in_value:
                    key += character
        if key or in_value:
            pairs = parse_qsl(key + "=x", keep_blank_values=True, separator="&")
            if not pairs:
                return _Domain(closed=False, gaps=["query_key_decode_unknown"])
            keys.add(pairs[0][0])
        return _Domain(set(keys), set(keys))

    def hash_domain(self, value: _Value) -> _Domain:
        return self.query_domain(value)

    def has_query(self, value: _Value) -> bool | None:
        if value.kind != "string":
            return None
        if value.extra.get("summarized_hash"):
            return value.extra.get("has_query")
        for part in value.parts:
            if isinstance(part, str) and "?" in part:
                return True
            if isinstance(part, _Value) and part.kind not in {"encoded"}:
                if part.kind != "string" or self.has_query(part) is not False:
                    return None
        return False

    def truth(self, value: _Value) -> bool | None:
        if "logical_truth" in value.extra:
            return value.extra["logical_truth"]
        if value.kind == "boolean":
            return value.data
        if value.kind == "null":
            return False
        if value.kind in {"literal", "number"}:
            return bool(value.data)
        if value.kind == "string" and not value.extra.get("summarized_hash") and all(isinstance(part, str) for part in value.parts):
            return bool("".join(value.parts))
        return None

    def dependencies(self, *values: _Value) -> list[str]:
        return sorted({item for value in values for item in value.extra.get("lookup_dependencies", [])})

    def _string(self, text: str) -> _Value:
        if any(0xD800 <= ord(character) <= 0xDFFF for character in text):
            return self.unknown("lone_surrogate_string_not_modeled")
        return self.value("string", parts=[text])

    def _bool(self, truth: bool | None, *sources: _Value) -> _Value:
        return self.value("boolean", truth, extra={"lookup_dependencies": self.dependencies(*sources)})

    def refine(self, frame: _Frame, condition: Any, assume: bool) -> None:
        condition = _unwrap(condition)
        if condition is None or condition.type != "binary_expression":
            return
        left_node, right_node = condition.child_by_field_name("left"), condition.child_by_field_name("right")
        operator = frame.document.text(condition.child_by_field_name("operator"))
        # Refinement is not a second execution of the condition. Only the
        # supported pure local index/length reads are inspected here.
        if operator not in {"<", "==", "==="} or left_node is None or right_node is None or left_node.type not in {"identifier", "member_expression"} or right_node.type != "number":
            return
        left = self.eval(frame, left_node)
        right = self.eval(frame, right_node)
        if left.kind == "query_index" and left.extra.get("offset", 0) == 0 and right.kind == "number" and right.data == 0 and operator == "<":
            uid = left.extra["input_uid"]
            if assume and left.extra.get("query_projection"):
                frame.queryless_projection = {**deepcopy(left.extra["query_projection"]),
                    "relation": "control_queryless_empty", "input_value_id": uid,
                    "view": "raw_query",
                    "condition_location": frame.document.location(condition), "condition_assumed": True,
                    "original_query_keys_preserved": True, "data_dependency": False, "control_dependency": True}
            for value in frame.env.values():
                if value.uid == uid and value.kind == "string":
                    if self.has_query(value) is not None:
                        continue
                    domain = self.hash_domain(value)
                    value.extra["has_query"] = not assume
                    value.extra["summarized_hash"] = True
                    value.domain = _Domain() if assume else domain
        elif left.kind == "query_length" and right.kind == "number" and right.data == 0 and operator in {"==", "==="} and assume:
            uid = left.extra["input_uid"]
            for value in frame.env.values():
                if value.uid == uid and value.kind == "serialized":
                    value.domain = _Domain()

    def _slice(self, value: _Value, args: list[_Value]) -> _Value:
        if value.kind != "string" or not 1 <= len(args) <= 2:
            return self.unknown("unsupported_string_slice")
        if all(isinstance(part, str) for part in value.parts) and not value.extra.get("summarized_hash") and all(argument.kind == "number" for argument in args):
            # String indices are UTF-16 code units, not Python codepoints.
            units = "".join(value.parts).encode("utf-16-le", "surrogatepass")
            length = len(units) // 2
            start = int(args[0].data)
            end = int(args[1].data) if len(args) == 2 else length
            start = min(length, max(0, start if start >= 0 else length + start))
            end = min(length, max(0, end if end >= 0 else length + end))
            return self._string(units[start * 2:max(start, end) * 2].decode("utf-16-le", "surrogatepass"))
        marker = args[0] if args[0].kind == "query_index" else args[1] if len(args) == 2 and args[1].kind == "query_index" else None
        if marker is None or marker.extra.get("input_uid") != value.uid:
            return self.unknown("slice_index_source_not_bound")
        if len(args) == 2 and args[0].kind == "number" and args[0].data == 0 and marker.extra.get("offset", 0) == 0:
            if not value.extra.get("summarized_hash"):
                before = []
                for part in value.parts:
                    if isinstance(part, str) and "?" in part:
                        before.append(part.split("?", 1)[0])
                        return self.value("string", parts=before)
                    before.append(part)
            return self.value("string", domain=_Domain(), extra={"summarized_hash": True, "has_query": False,
                "raw_domain": _Domain(closed=False, gaps=["unknown_path_as_raw_query"])})
        if len(args) == 1 and marker.extra.get("offset", 0) == 1:
            exists = self.has_query(value)
            if exists is False:
                # indexOf returns -1, therefore +1 is zero. This is the
                # whole hash string, not a raw query projection.
                return deepcopy(value)
            if exists is not True:
                return self.unknown("query_tail_separator_presence_unproven")
            if not value.extra.get("summarized_hash"):
                after, found = [], False
                for part in value.parts:
                    if found:
                        after.append(part)
                    elif isinstance(part, str) and "?" in part:
                        found = True
                        after.append(part.split("?", 1)[1])
                if found:
                    return self.projected(self.value("string", parts=after, domain=self.hash_domain(value), extra={"query_text": True}), value, "data_query_tail_of_bound_hash")
            return self.projected(self.value("string", domain=_Domain(closed=False, gaps=["query_tail_as_hash_unknown"]),
                extra={"summarized_hash": True, "has_query": None, "raw_domain": self.hash_domain(value), "query_text": True}), value, "data_query_tail_of_bound_hash")
        return self.unknown("unsupported_slice_shape")

    def eval(self, frame: _Frame, original: Any) -> _Value:
        node = _unwrap(original)
        if node is None:
            return self.unknown("missing_expression")
        document, kind = frame.document, node.type
        if kind == "string":
            text = _literal_string(document.text(node))
            if text is None:
                return self.unknown("unmodeled_string_literal", frame, node, True)
            if any(0xD800 <= ord(character) <= 0xDFFF for character in text):
                return self.unknown("lone_surrogate_string_not_modeled", frame, node, True)
            value = self._string(text)
            if text == "" and frame.queryless_projection:
                value.extra["query_projection"] = {**deepcopy(frame.queryless_projection), "empty_literal_location": document.location(node)}
            self.event("literal_seed", frame, node, text=text, value=value.public())
            return value
        if kind in {"null", "true", "false"}:
            return self.value("null") if kind == "null" else self._bool(kind == "true")
        if kind == "number":
            try:
                text = document.text(node)
                number = int(text, 10)
                if len(text) > 1 and text.startswith("0") or abs(number) > 2**53 - 1:
                    raise ValueError("unsupported numeric shape")
                return self.value("number", number)
            except (ValueError, OverflowError):
                return self.unknown("unsupported_numeric_literal")
        if kind == "identifier":
            return self.lookup(frame, node)
        if kind == "template_string":
            parts = []
            for child in node.named_children:
                if child.type == "string_fragment":
                    parts.append(document.text(child))
                elif child.type == "template_substitution":
                    expression = next((item for item in child.named_children if item.type != "comment"), None)
                    value = self.eval(frame, expression)
                    if value.kind == "string" and not value.extra.get("summarized_hash"):
                        parts.extend(value.parts)
                    elif value.kind in {"serialized", "encoded"} or value.kind == "string" and self.has_query(value) is False:
                        parts.append(value)
                    else:
                        return self.unknown("unknown_template_delimiter", frame, child, True)
                else:
                    return self.unknown("unmodeled_template_escape", frame, child, True)
            value = self.value("string", parts=parts)
            self.event("template_construction", frame, node, segments=value.public()["segments"])
            return value
        if kind == "array":
            values = []
            for child in node.named_children:
                if child.type == "comment":
                    continue
                value = self.eval(frame, child)
                if value.kind != "string" or not all(isinstance(part, str) for part in value.parts):
                    return self.unknown("array_key_not_literal", frame, child, True)
                values.append("".join(value.parts))
            # Sparse arrays and spreads are not a closed literal key list.
            previous = "["
            for child in node.children:
                if child.type == "comment":
                    continue
                if child.type == "," and previous in {"[", ","}:
                    return self.unknown("sparse_key_array", frame, node, True)
                previous = child.type
            return self.value("array", values, extra={"frozen": False, "declaration_location": document.location(node)})
        if kind == "member_expression":
            path = _member_path(node, document)
            if frame.ambient is not None and path == frame.ambient_path:
                binding, key = self.binding(frame, path[0], node.child_by_field_name("object") or node)
                if not key or binding.get("reason") in {"duplicate_or_shadow_binding", "with_dynamic_scope", "escaped_binding_or_write_not_decoded"}:
                    return self.unknown("ambient_capture_binding_unknown", frame, node, True)
                value = deepcopy(frame.ambient)
                value.uid = self.value(value.kind).uid
                value.extra["query_projection"] = {"guaranteed_contexts": [frame.context_id], "possible_contexts": [frame.context_id],
                    "relation": "ambient_hash_query_identity", "view": "hash", "source_location": document.location(node),
                    "ambient_read_binding_id": key, "navigation_input_value_id": frame.ambient.uid,
                    "original_query_keys_preserved": True, "external_navigation_assumption": True}
                self.event("ambient_hash_read", frame, node, binding_id=key,
                    relation="external_navigation_and_read_stability_assumption", query_domain=self.hash_domain(value).public(),
                    factory_context_id=frame.context_id, navigation_input_value_id=frame.ambient.uid, value=value.public())
                return value
            object_node, prop = node.child_by_field_name("object"), node.child_by_field_name("property")
            obj = self.eval(frame, object_node)
            name = document.text(prop)
            if name == "length" and obj.kind == "serialized":
                return self.value("query_length", extra={"input_uid": obj.uid, "domain": deepcopy(obj.domain)})
            return self.unknown("unknown_member_value")
        if kind == "subscript_expression":
            # The value of selection[name] can be null or non-null. The finite
            # query key comes from the loop binding, not this untrusted value.
            return self.unknown("unknown_indexed_value")
        if kind == "await_expression":
            return self.eval(frame, next((child for child in node.named_children if child.type != "comment"), None))
        if kind == "ternary_expression":
            condition = node.child_by_field_name("condition")
            truth = self.truth(self.eval(frame, condition))
            branches = [truth] if truth is not None else [True, False]
            results, forks = [], []
            for branch in branches:
                fork = frame.fork()
                self.refine(fork, condition, branch)
                results.append(self.eval(fork, node.child_by_field_name("consequence" if branch else "alternative")))
                forks.append(fork)
            self.merge_frames(frame, forks)
            value = results[0]
            for result in results[1:]:
                value = self.join(value, result)
            self.event("conditional_value_join", frame, node, condition_location=document.location(condition),
                condition_truth=truth, input_value_ids=[result.uid for result in results], result=value.public())
            return value
        if kind == "binary_expression":
            left_node, right_node = node.child_by_field_name("left"), node.child_by_field_name("right")
            op = document.text(node.child_by_field_name("operator"))
            left = self.eval(frame, left_node)
            if op in {"||", "&&"}:
                a = self.truth(left)
                skips = a is True if op == "||" else a is False
                evaluates = a is False if op == "||" else a is True
                if skips:
                    return left
                if evaluates:
                    right = self.eval(frame, right_node)
                    right.extra["lookup_dependencies"] = self.dependencies(left, right)
                    return right
                right_frame = frame.fork()
                right = self.eval(right_frame, right_node)
                self.merge_frames(frame, [frame.fork(), right_frame])
                b = self.truth(right)
                truth = True if op == "||" and b is True else False if op == "&&" and b is False else None
                value = self.join(left, right)
                value.extra.update(logical_truth=truth, lookup_dependencies=self.dependencies(left, right))
                return value
            right = self.eval(frame, right_node)
            if op == "+" and left.kind == "query_index" and right.kind == "number":
                return self.value("query_index", extra={**left.extra, "offset": left.extra.get("offset", 0) + right.data})
            if op == "+" and left.kind == right.kind == "number":
                number = left.data + right.data
                return self.value("number", number) if abs(number) <= 2**53 - 1 else self.unknown("numeric_addition_not_safe_integer")
            if op in {"==", "===", "!=", "!=="}:
                truth = None
                if left.kind == right.kind == "null":
                    truth = True
                elif left.kind == "null" or right.kind == "null":
                    other = right if left.kind == "null" else left
                    if other.kind in {"string", "number", "boolean", "literal", "nonnull", "params"}:
                        truth = False
                elif left.kind == right.kind and left.kind in {"number", "boolean", "literal"} and left.data is not None and right.data is not None:
                    truth = left.data == right.data
                elif left.kind == "query_length" and right.kind == "number" and right.data == 0:
                    domain = left.extra["domain"]
                    truth = False if domain.guaranteed else True if domain.closed and not domain.possible else None
                if op in {"!=", "!=="} and truth is not None:
                    truth = not truth
                value = self._bool(truth, left, right)
                value.extra["factory_callback_contexts"] = sorted({context for operand in (left, right)
                    for context in operand.extra.get("factory_callback_contexts", [])})
                return value
            if op == "<" and right.kind == "number" and right.data == 0 and left.kind == "query_index":
                if left.extra.get("offset", 0) != 0:
                    return self.unknown("offset_separator_index_comparison_not_modeled")
                exists = left.extra.get("has_query")
                return self._bool(None if exists is None else not exists, left)
            if op == "<" and left.kind == right.kind == "number":
                return self._bool(left.data < right.data, left, right)
            return self.unknown("unsupported_binary_expression")
        if kind in {"call_expression", "new_expression"}:
            return self.call(frame, node)
        self.invalidate(frame, "unsupported_expression_possible_effect")
        return self.unknown("unsupported_navigation_expression", frame, node, True)

    def call(self, frame: _Frame, node: Any) -> _Value:
        document = frame.document
        function = node.child_by_field_name("function") or node.child_by_field_name("constructor")
        path = _member_path(function, document)
        arguments_node = node.child_by_field_name("arguments")
        argument_nodes = [child for child in arguments_node.named_children if child.type != "comment"] if arguments_node else []
        if any(child.type == "spread_element" for child in argument_nodes) or any(child.type == "optional_chain" for child in node.children):
            self.invalidate(frame, "spread_or_optional_call")
            return self.unknown("spread_or_optional_call", frame, node, True)
        arguments = [self.eval(frame, argument) for argument in argument_nodes]
        if node.type == "new_expression" and path == ["URLSearchParams"]:
            if len(arguments) != 1 or not self.builtin(frame, "URLSearchParams", function):
                return self.unknown("url_constructor_identity_or_arity_unknown", frame, node, True)
            domain = self.query_domain(arguments[0], raw=True)
            value = self.projected(self.value("params", domain=domain, extra={"constructor_location": document.location(node),
                "constructor_seed_value_id": arguments[0].uid, "model": "url-search-params-v1"}), arguments[0],
                "url_search_params_string_seed_preserves_query_keys", document.location(argument_nodes[0]))
            self.event("url_search_params_seed", frame, node, argument_location=document.location(argument_nodes[0]),
                input_value_id=arguments[0].uid, receiver_id=value.uid, key_domain=domain.public(),
                query_projection=value.extra.get("query_projection"), model="url-search-params-v1")
            return value
        if path == ["Object", "freeze"]:
            if len(arguments) != 1 or not self.builtin(frame, "Object", function, "freeze"):
                return self.unknown("freeze_identity_or_arity_unknown", frame, node, True)
            value = arguments[0]
            if value.kind == "array":
                value.extra["frozen"] = True
                self.event("frozen_literal_key_array", frame, node, keys=list(value.data),
                    array_location=value.extra["declaration_location"], model="object-freeze-inert-v1")
                return value
            return self.unknown("freeze_argument_not_modeled", frame, node, True)
        if path == ["encodeURIComponent"]:
            if len(arguments) != 1 or not self.builtin(frame, "encodeURIComponent", function):
                return self.unknown("encoding_identity_or_arity_unknown", frame, node, True)
            value = self.value("encoded", extra={"location": document.location(node)})
            self.event("encoded_template_component", frame, node, model="js-string-url-slicing-v1", delimiter_injection_excluded_under_model=True)
            return value
        if function is not None and function.type == "member_expression":
            receiver_node = function.child_by_field_name("object")
            receiver = self.eval(frame, receiver_node)
            member = document.text(function.child_by_field_name("property"))
            if receiver.kind == "params":
                if member in {"set", "delete", "get"} and len(arguments) in ({2} if member == "set" else {1}):
                    key = arguments[0]
                    literal_key = "".join(key.parts) if key.kind == "string" and not key.extra.get("summarized_hash") and all(isinstance(part, str) for part in key.parts) else None
                    if literal_key is None:
                        receiver.domain.uncertain("dynamic_query_key")
                        return self.unknown("dynamic_query_key", frame, node, True)
                    if member == "set":
                        receiver.domain.guaranteed.add(literal_key)
                        receiver.domain.possible.add(literal_key)
                    elif member == "delete":
                        receiver.domain.guaranteed.discard(literal_key)
                        receiver.domain.possible.discard(literal_key)
                    else:
                        lookup_id = _digest({"file": document.source.path, "hash": document.source.hash, "site": _key(node),
                            "factory_context_id": frame.context_id, "receiver_id": receiver.uid,
                            "seed_value_id": receiver.extra.get("constructor_seed_value_id")})[:24]
                        value = self.value("null" if receiver.domain.closed and literal_key not in receiver.domain.possible else "nonnull" if literal_key in receiver.domain.guaranteed else "unknown",
                            extra={"lookup_dependencies": [lookup_id]})
                        lookup = {"id": lookup_id, "key": literal_key, "location": document.location(node),
                            "receiver_id": receiver.uid, "constructor_location": receiver.extra.get("constructor_location"),
                            "constructor_seed_value_id": receiver.extra.get("constructor_seed_value_id"),
                            "query_projection": deepcopy(receiver.extra.get("query_projection")), "factory_context_id": frame.context_id,
                            "query_domain": receiver.domain.public(), "get_result": value.kind,
                            "model": "url-search-params-v1", "normal_return_only": True}
                        self.lookups.append(lookup)
                        self.event("query_key_lookup", frame, node, **lookup)
                        return value
                    if receiver.extra.get("query_projection"):
                        receiver.extra["query_projection"]["guaranteed_contexts"] = []
                        receiver.extra["query_projection"]["relation"] = "query_mutation_projection_not_certified"
                        receiver.extra["query_projection"]["original_query_keys_preserved"] = False
                    self.event("query_key_mutation", frame, node, method=member, key=literal_key,
                        receiver_id=receiver.uid, key_argument_location=document.location(argument_nodes[0]),
                        key_domain=receiver.domain.public(), model="url-search-params-v1")
                    return self.unknown("void_query_mutation_result")
                if member == "toString" and not arguments:
                    self.event("query_serialization", frame, node, receiver_id=receiver.uid, key_domain=receiver.domain.public(), model="url-search-params-v1")
                    return self.projected(self.value("serialized", domain=deepcopy(receiver.domain)), receiver,
                        "query_serialization_preserves_key_presence", document.location(node))
                receiver.domain.uncertain("unsupported_query_operation_or_arity")
                return self.unknown("unsupported_query_operation_or_arity", frame, node, True)
            if receiver.kind == "string" and member in {"indexOf", "slice"}:
                if not self.builtin(frame, "String", function, member):
                    return self.unknown("string_standard_interface_unknown", frame, node, True)
                if member == "indexOf" and len(arguments) == 1 and arguments[0].kind == "string" and arguments[0].parts == ["?"]:
                    self.event("query_separator_index", frame, node, receiver_id=receiver.uid, model="js-string-url-slicing-v1")
                    return self.value("query_index", extra={"input_uid": receiver.uid, "offset": 0,
                        "has_query": self.has_query(receiver), "query_projection": deepcopy(receiver.extra.get("query_projection"))
                            if receiver.extra.get("query_projection", {}).get("view") == "hash" else None})
                if member == "slice":
                    value = self._slice(receiver, arguments)
                    if value.kind == "unknown":
                        self.gaps.append(_issue("navigation_string_slice_unknown", "字符串索引与源串身份未闭合。", document.source.path, node.start_point.row + 1))
                    self.event("string_slice", frame, node, receiver_id=receiver.uid, result=value.public(), model="js-string-url-slicing-v1")
                    return value
            if receiver.kind == "factory_options":
                callback = frame.callbacks.get((receiver.extra["parameter_binding_id"], member))
                if callback is not None and not arguments:
                    callback_kind = function_kind(callback["document"], callback["function"])
                    is_async = callback_kind.get("kind") == "ordinary_async"
                    consumption = completion_relation(document, node, frame.function, "await",
                        lexical=self.lexical(document)) if is_async else None
                    if callback_kind.get("kind") not in {"ordinary_sync", "ordinary_async"} or is_async and not (
                            consumption.get("direct_await") and consumption.get("normal_value_relation_closed")):
                        self.gaps.append(_issue("injected_callback_async_or_generator_consumption_unknown",
                            "共享调用种类/完成关系未闭合实际 callback 的正常结果消费。",
                            document.source.path, node.start_point.row + 1,
                            callback_function_kind=callback_kind, completion_relation=consumption))
                        return self.unknown("injected_callback_async_or_generator_consumption_unknown", frame, node)
                    self.event("invokes_injected_callback", frame, node,
                        factory_context_id=receiver.extra["factory_context_id"], callback_graph_node_id=callback["definition"].graph_node_id,
                        callback_location=callback["document"].location(callback["function"]),
                        async_callback=is_async, result_consumption="direct_await_normal_fulfillment" if is_async else "ordinary_synchronous_call",
                        callback_function_kind=callback_kind, completion_relation=consumption,
                        completion_summaries_version=COMPLETION_VERSION,
                        relation="specific_argument_property_to_captured_parameter; not global CALLS")
                    callback_frame = _Frame(callback["document"], callback["definition"], callback["function"],
                        ambient=frame.ambient, ambient_path=frame.ambient_path, mode="callback", context_id=frame.context_id)
                    returns, continues = self.execute(callback_frame, callback["function"].child_by_field_name("body"))
                    value = self.return_value(returns, continues)
                    value.extra["factory_callback_contexts"] = [receiver.extra["factory_context_id"]]
                    self.event("injected_callback_normal_result", frame, node,
                        factory_context_id=receiver.extra["factory_context_id"],
                        callback_graph_node_id=callback["definition"].graph_node_id,
                        all_normal_returns_null=bool(returns and not continues and all(item.kind == "null" for item in returns)),
                        normal_return_coverage_complete=not continues, result=value.public())
                    return value
        edge, problems = self.sources.call_binding(node, document, frame.definition)
        if edge is None:
            self.gaps.extend(problems)
            self.invalidate(frame, "unknown_call_possible_query_effect")
            for argument in arguments:
                if argument.kind == "params":
                    argument.domain.uncertain("unknown_call_query_escape")
            return self.unknown("callee_or_helper_body_unknown", frame, node, True)
        if any(argument.kind == "params" for argument in arguments):
            for argument in arguments:
                if argument.kind == "params":
                    argument.domain.uncertain("cross_helper_query_heap_not_modeled")
            self.invalidate(frame, "cross_helper_query_heap_not_modeled")
            return self.unknown("cross_helper_query_heap_not_modeled", frame, node, True)
        # String summaries are supported across helpers, heap side effects
        # and captured query objects are not. A live parent receiver cannot
        # remain closed after an arbitrary helper invocation.
        self.invalidate(frame, "helper_possible_captured_query_effect")
        targets = self.sources.nodes.get(edge.target, [])
        target_document, definition, problems = self.sources.definition_for_node(targets[0])
        if target_document is None or definition is None:
            self.gaps.extend(problems)
            return self.unknown("helper_declaration_unknown")
        function_body = _function(definition)
        helper_kind = function_kind(target_document, function_body)
        if helper_kind.get("kind") != "ordinary_sync" or len(self.stack) >= _MAX_CALL_DEPTH or edge.target in self.stack:
            return self.unknown("helper_call_scope_or_recursion_unknown", frame, node, True)
        # General object semantics and arbitrary effectful helper bodies are
        # deliberately not treated as transparent URL transformers.
        if any(child.type == "object" for child in _direct(function_body.child_by_field_name("body"))):
            self.invalidate(frame, "opaque_helper_possible_query_effect")
            return self.unknown("helper_object_or_effect_semantics_not_modeled", frame, node, True)
        child = _Frame(target_document, definition, function_body, context_id=frame.context_id)
        parameters = function_body.child_by_field_name("parameters")
        params = [part for part in parameters.named_children if part.type != "comment"] if parameters is not None else []
        if len(params) != len(arguments):
            return self.unknown("helper_argument_parameter_arity_unknown", frame, node, True)
        for index, (parameter, value) in enumerate(zip(params, arguments)):
            pattern = _simple_parameter(parameter)
            if pattern is None:
                return self.unknown("helper_parameter_pattern_unknown", frame, node, True)
            name = target_document.text(pattern)
            self.bind(child, parameters, name, value, function_body)
            self.event("argument_binds_parameter", frame, node, edge_id=edge.id, target_node_id=edge.target,
                argument_index=index, argument_location=document.location(argument_nodes[index]),
                formal_parameter_location=target_document.location(parameter), parameter_name=name,
                target_declaration=target_document.location(function_body), value=value.public())
        self.stack.append(edge.target)
        helper_gap_start = len(self.gaps)
        returns, continues = self.execute(child, function_body.child_by_field_name("body"))
        self.stack.pop()
        value = self.return_value(returns, continues)
        if len(self.gaps) > helper_gap_start and value.kind in {"params", "serialized", "string"}:
            # An opaque prefix could alter a captured receiver or standard
            # interface before allocation/use. Do not return a false closed
            # URL summary merely because the final expression is recognized.
            if value.domain is not None:
                value.domain.uncertain("helper_effect_prefix_not_closed")
            else:
                value = self.unknown("helper_effect_prefix_not_closed", frame, node, True)
        self.event("helper_normal_return", child, function_body, caller_call_location=document.location(node),
            result=value.public(), normal_return_only=True, helper_function_kind=helper_kind,
            completion_summaries_version=COMPLETION_VERSION)
        return value

    def invalidate(self, frame: _Frame, reason: str) -> None:
        for value in frame.env.values():
            if value.kind == "params":
                value.domain.uncertain(reason)
                if value.extra.get("query_projection"):
                    value.extra["query_projection"]["guaranteed_contexts"] = []
                    value.extra["query_projection"]["relation"] = "opaque_effect_projection_not_certified"
            elif value.kind == "factory_options":
                value.kind = "unknown"
                value.extra["reason"] = reason

    def return_value(self, returns: list[_Value], continues: bool) -> _Value:
        if not returns or continues:
            return self.unknown("function_return_coverage_unknown")
        value = returns[0]
        for other in returns[1:]:
            value = self.join(value, other)
        return value

    def execute(self, frame: _Frame, node: Any) -> tuple[list[_Value], bool]:
        if node is None:
            return [], True
        kind, document = node.type, frame.document
        if kind == "statement_block":
            returns = []
            for child in node.named_children:
                if child.type == "comment" or child.type in _FUNCTIONS:
                    continue
                current, continues = self.execute(frame, child)
                returns.extend(current)
                if not continues:
                    return returns, False
            return returns, True
        if kind in {"lexical_declaration", "variable_declaration"}:
            keyword = next((child.type for child in node.children if child.type in {"const", "let", "var"}), "")
            for declaration in node.named_children:
                if declaration.type != "variable_declarator":
                    continue
                pattern = declaration.child_by_field_name("name")
                if keyword != "const" or pattern is None or pattern.type != "identifier":
                    self.invalidate(frame, "mutable_or_destructured_declaration")
                    self.gaps.append(_issue("navigation_declaration_unknown", "可变/解构声明不在有限 helper 模型内。", document.source.path, node.start_point.row + 1))
                    continue
                value = self.eval(frame, declaration.child_by_field_name("value"))
                self.bind(frame, declaration, document.text(pattern), value)
                self.event("local_value_binding", frame, declaration, name=document.text(pattern), value=value.public())
            return [], True
        if kind == "expression_statement":
            expression = next((child for child in node.named_children if child.type != "comment"), None)
            if expression is not None and expression.type == "call_expression":
                self.eval(frame, expression)
            else:
                self.invalidate(frame, "unsupported_expression_effect")
                self.gaps.append(_issue("navigation_effect_unknown", "未知表达式效果可能改变 receiver/来源，不能省略。", document.source.path, node.start_point.row + 1))
            return [], True
        if kind == "if_statement":
            condition = node.child_by_field_name("condition")
            condition_value = self.eval(frame, condition)
            truth = self.truth(condition_value)
            active, returns = [], []
            for branch in [truth] if truth is not None else [True, False]:
                fork = frame.fork()
                self.refine(fork, condition, branch)
                body = node.child_by_field_name("consequence" if branch else "alternative")
                values, continues = self.execute(fork, body)
                action = "return_null" if values and not continues and all(value.kind == "null" for value in values) else "throw" if values and not continues and all(value.kind == "throw" for value in values) else None
                self.event("branch_guard", frame, condition, branch=branch, condition_truth=truth,
                    condition_text=document.text(condition), lookup_dependencies=self.dependencies(condition_value),
                    condition_value_id=condition_value.uid, action=action,
                    factory_callback_contexts=condition_value.extra.get("factory_callback_contexts", []),
                    branch_result_ids=[value.uid for value in values], branch_result_kinds=[value.kind for value in values],
                    branch_continues=continues, consequent_coverage_complete=not continues)
                returns.extend(values)
                if continues:
                    active.append(fork)
            if active:
                self.merge_frames(frame, active)
            return returns, bool(active)
        if kind == "else_clause":
            child = next((child for child in node.named_children if child.type != "comment"), None)
            return self.execute(frame, child)
        if kind == "for_in_statement":
            left, right, body = node.child_by_field_name("left"), node.child_by_field_name("right"), node.child_by_field_name("body")
            keyword = document.text(node.child_by_field_name("kind"))
            operator = document.text(node.child_by_field_name("operator"))
            iterable = self.eval(frame, right)
            if keyword != "const" or operator != "of" or left is None or left.type != "identifier" or iterable.kind != "array" or not iterable.extra.get("frozen") or len(iterable.data) > _MAX_LOOP_KEYS:
                self.invalidate(frame, "unsupported_or_mutable_key_loop")
                return [self.unknown("unsupported_or_mutable_key_loop", frame, node, True)], True
            self.event("finite_key_loop", frame, node, keys=list(iterable.data), key_source_location=document.location(right),
                literal_array_location=iterable.extra["declaration_location"], operator=operator)
            returns = []
            for key in iterable.data:
                self.bind(frame, left, document.text(left), self._string(key), node)
                values, continues = self.execute(frame, body)
                returns.extend(values)
                if not continues:
                    return returns, False
            return returns, True
        if kind == "return_statement":
            expression = next((child for child in node.named_children if child.type != "comment"), None)
            value = self.eval(frame, expression)
            self.event("return_expression", frame, node, expression_location=document.location(expression) if expression is not None else None, value=value.public(), normal_return_only=True)
            return [value], False
        if kind == "throw_statement":
            self.event("throw_guard_action", frame, node, normal_return_only=False)
            return [self.value("throw", extra={"location": document.location(node)})], False
        self.invalidate(frame, "unsupported_control_or_effect")
        self.gaps.append(_issue("navigation_control_unknown", "未支持的控制流/效果不能视为空操作。", document.source.path, node.start_point.row + 1))
        return [self.unknown("unsupported_control_or_effect")], True


def _definition_identity(document: Any, definition: Any) -> dict:
    function = _function(definition)
    return {"symbol": definition.symbol, "graph_node_id": getattr(definition, "graph_node_id", ""),
        "location": document.location(function or definition.node)}


def _producer(engine: _Engine, selector: dict) -> tuple[dict, _Value]:
    document, definition, problems = engine.sources.select(selector)
    engine.gaps.extend(problems)
    result = {"selector": selector, "source_complete": False, "query_domain": _Domain(closed=False, gaps=["producer_unresolved"]).public()}
    if document is None or definition is None or document.kind not in {"typescript", "tsx"} or _function(definition) is None:
        return result, engine.unknown("producer_source_unknown")
    function = _function(definition)
    body = function.child_by_field_name("body")
    matches = []
    for node in _direct(body):
        if selector["site"] == "assignment" and node.type == "assignment_expression" and _member_path(node.child_by_field_name("left"), document) == selector["target"]:
            matches.append((node, node.child_by_field_name("right")))
        elif selector["site"] == "call" and node.type == "call_expression" and _member_path(node.child_by_field_name("function"), document) == selector["callee"].split("."):
            matches.append((node, node))
    if len(matches) != 1:
        engine.gaps.append(_issue("navigation_producer_site_not_unique", f"生产入口匹配 {len(matches)} 个 AST；不选取某个通过项。",
            selector["file"]))
        return result, engine.unknown("producer_site_not_unique")
    site, expression = matches[0]
    frame = _Frame(document, definition, function)
    value = engine.eval(frame, expression)
    domain = engine.hash_domain(value)
    result.update(source_complete=value.kind == "string" and domain.closed,
        declaration=_definition_identity(document, definition), site_location=document.location(site),
        expression_location=document.location(expression), branch_conditions=_conditions(document, site, function),
        abstract_value=value.public(), query_domain=domain.public(),
        scope="RHS value on normal return of the selected expression; not observed DOM navigation",
        assignment_target_receiver_not_executed=True)
    engine.event("selected_navigation_source", frame, site, selector=selector, query_domain=domain.public())
    return result, value


def _object_member(document: Any, obj: Any, name: str) -> tuple[Any, list[dict]]:
    obj = _unwrap(obj)
    if obj is None or obj.type != "object":
        return None, [_issue("navigation_object_not_literal", "工厂实参/返回对象不是封闭字面对象，不能把别名当注入。", document.source.path)]
    matches, problems = [], []
    for member in obj.named_children:
        if member.type == "comment":
            continue
        if member.type in {"pair", "method_definition"}:
            key = member.child_by_field_name("key") or member.child_by_field_name("name")
            if key is None or key.type not in {"identifier", "property_identifier"} or "\\" in document.text(key):
                problems.append(_issue("navigation_object_dynamic_key", "动态/转义字段禁止闭合 callback/method 来源。", document.source.path, member.start_point.row + 1))
                continue
            if document.text(key) == name:
                value = member if member.type == "method_definition" else _unwrap(member.child_by_field_name("value"))
                if member.type == "method_definition" and any(child.type in {"get", "set"} for child in member.children):
                    problems.append(_issue("navigation_object_accessor", "访问器不作为普通 callback 注入。", document.source.path, member.start_point.row + 1))
                else:
                    matches.append(value)
        elif member.type == "shorthand_property_identifier":
            if "\\" in document.text(member):
                problems.append(_issue("navigation_object_escaped_shorthand", "转义 shorthand 可能覆盖 callback 字段，拒绝封闭映射。", document.source.path, member.start_point.row + 1))
            elif document.text(member) == name:
                problems.append(_issue("navigation_callback_alias_unknown", "callback shorthand 的运行绑定未推断。", document.source.path, member.start_point.row + 1))
        else:
            problems.append(_issue("navigation_object_spread_or_unknown", "展开/未知对象成员不能静默忽略为封闭映射。", document.source.path, member.start_point.row + 1))
    if problems or len(matches) != 1:
        return None, [*problems, _issue("navigation_object_member_not_unique", f"字段 {name} 匹配 {len(matches)} 项且需无未知覆盖。", document.source.path)]
    return matches[0], []


def _returned_method(engine: _Engine, frame: _Frame, property_name: str) -> tuple[Any, list[dict]]:
    document = frame.document
    returns = [node for node in _direct(frame.function.child_by_field_name("body")) if node.type == "return_statement"]
    if len(returns) != 1:
        return None, [_issue("navigation_factory_return_not_unique", "工厂返回来源不唯一，首版不合并任意对象/早退为同一方法。", document.source.path)]
    expression = _unwrap(next((child for child in returns[0].named_children if child.type != "comment"), None))
    if expression is not None and expression.type == "call_expression":
        function = expression.child_by_field_name("function")
        args_node = expression.child_by_field_name("arguments")
        args = [node for node in args_node.named_children if node.type != "comment"] if args_node else []
        if _member_path(function, document) != ["Object", "freeze"] or len(args) != 1 or not engine.builtin(frame, "Object", function, "freeze"):
            return None, [_issue("navigation_factory_return_wrapper_unknown", "返回 wrapper 未认证为固定 Object.freeze 模型。", document.source.path)]
        engine.event("factory_return_frozen_object", frame, expression, model="object-freeze-inert-v1", normal_return_only=True)
        expression = _unwrap(args[0])
    method, problems = _object_member(document, expression, property_name)
    if method is not None and method.type not in _FUNCTIONS:
        return None, [*problems, _issue("navigation_returned_method_not_callable", "返回字段不是实际函数/方法声明。", document.source.path)]
    return method, problems


def _consumer(engine: _Engine, rule: dict, navigation: _Value) -> dict:
    selector = rule["consumer"]
    document, owner, problems = engine.sources.select(selector)
    engine.gaps.extend(problems)
    result = {"selector": selector, "source_complete": False, "query_lookups": [], "required_query_keys": [],
        "null_return_guards": [], "factory_null_throw_guards": [], "callback_relation_closed": False}
    if document is None or owner is None or _function(owner) is None:
        return result
    function = _function(owner)
    calls = [node for node in _direct(function.child_by_field_name("body")) if node.type == "call_expression"
        and _member_path(node.child_by_field_name("function"), document) == selector["factory_callee"].split(".")]
    if len(calls) != 1:
        engine.gaps.append(_issue("navigation_factory_call_not_unique", f"工厂调用匹配 {len(calls)} 项，不能按同名全局绑定。", selector["file"]))
        return result
    call = calls[0]
    edge, problems = engine.sources.call_binding(call, document, owner)
    engine.gaps.extend(problems)
    if edge is None:
        return result
    target = engine.sources.nodes[edge.target][0]
    factory_document, factory, problems = engine.sources.definition_for_node(target)
    engine.gaps.extend(problems)
    if factory_document is None or factory is None:
        return result
    arguments_node = call.child_by_field_name("arguments")
    args = [node for node in arguments_node.named_children if node.type != "comment"] if arguments_node else []
    index = selector["argument_index"]
    if index >= len(args) or any(node.type == "spread_element" for node in args[:index + 1]):
        engine.gaps.append(_issue("navigation_factory_argument_unknown", "工厂实参位置缺失或含展开。", selector["file"]))
        return result
    callback_function, problems = _object_member(document, args[index], selector["callback_property"])
    engine.gaps.extend(problems)
    callback = document.definition_for_ast(callback_function) if callback_function is not None else None
    if callback is None or callback_function.type not in _FUNCTIONS:
        engine.gaps.append(_issue("navigation_callback_source_unknown", "实参 callback 没有唯一原始 AST 函数身份。", selector["file"]))
        return result
    callback_parameters = callback_function.child_by_field_name("parameters")
    if callback_parameters is None or any(child.type != "comment" for child in callback_parameters.named_children):
        engine.gaps.append(_issue("navigation_callback_parameters_unknown", "零实参注入 callback 的默认/rest/声明参数效果未建模。", selector["file"]))
        return result
    callback_nodes = engine.sources.nodes.get(callback.graph_node_id, [])
    if len(callback_nodes) != 1:
        engine.gaps.append(_issue("navigation_callback_graph_identity_unknown", "callback 图声明不唯一。", selector["file"]))
        return result
    _, _, problems = engine.sources.definition_for_node(callback_nodes[0])
    engine.gaps.extend(problems)
    if problems:
        return result
    factory_function = _function(factory)
    factory_kind = function_kind(factory_document, factory_function)
    if factory_kind.get("kind") != "ordinary_sync":
        engine.gaps.append(_issue("navigation_factory_async_or_generator_unknown", "工厂异步/生成器返回不是同步对象，首版不打开 Promise/iterator。",
            factory_document.source.path, function_kind=factory_kind))
        return result
    parameters = factory_function.child_by_field_name("parameters")
    params = [node for node in parameters.named_children if node.type != "comment"] if parameters else []
    if index >= len(params):
        engine.gaps.append(_issue("navigation_factory_formal_missing", "工厂对应形参未找到。", factory_document.source.path))
        return result
    parameter = params[index]
    pattern = _simple_parameter(parameter)
    if pattern is None or any(_simple_parameter(item) is None for item in params):
        engine.gaps.append(_issue("navigation_factory_parameter_pattern", "工厂形参不是唯一简单绑定。", factory_document.source.path))
        return result
    factory_frame = _Frame(factory_document, factory, factory_function)
    # Only an unescaped fresh argument whose formal has no direct use/effect
    # before its returned closures can be contextually injected. Closure
    # uses are interpreted at the selected method, not run at factory time.
    factory_parameter_identity = engine.lexical(factory_document).resolve(pattern)
    factory_formal_uses = []
    for node in _direct(factory_function.child_by_field_name("body")):
        if node.type != "identifier" or factory_document.text(node) != factory_document.text(pattern):
            continue
        identity = engine.lexical(factory_document).resolve(node)
        if identity.get("state") != "unique" or identity.get("declaration_id") == factory_parameter_identity.get("declaration_id"):
            factory_formal_uses.append(factory_document.location(node))
    writes = engine.lexical(factory_document).writes(factory_parameter_identity)
    if factory_parameter_identity.get("state") != "unique" or factory_formal_uses or writes:
        engine.gaps.append(_issue("navigation_factory_formal_effect_unknown", "工厂形参存在未支持直接使用、写入/别名逃逸或身份缺口，不能注入 callback。",
            factory_document.source.path, parameter.start_point.row + 1,
            formal_identity=factory_parameter_identity, direct_uses=factory_formal_uses[:12], write_count=len(writes), writes=writes[:12]))
        return result
    method, problems = _returned_method(engine, factory_frame, selector["returned_method"])
    engine.gaps.extend(problems)
    method_definition = factory_document.definition_for_ast(method) if method is not None else None
    if method_definition is None:
        return result
    method_kind = function_kind(factory_document, method)
    if method_kind.get("kind") not in {"ordinary_sync", "ordinary_async"}:
        engine.gaps.append(_issue("navigation_returned_generator_unknown", "返回 generator 方法是 iterator 边界，不解释其 body 为直接调用结果。",
            factory_document.source.path, function_kind=method_kind))
        return result
    returned_object = method.parent
    if returned_object is not None and returned_object.type == "pair":
        returned_object = returned_object.parent
    captured_formal_gaps = []
    for node in _walk(factory_function.child_by_field_name("body")):
        if node.type != "identifier":
            continue
        name = factory_document.text(node)
        if "\\" in name:
            captured_formal_gaps.append({"reason": "escaped_reference_not_decoded", "location": factory_document.location(node)})
            continue
        if name != factory_document.text(pattern):
            continue
        identity = engine.lexical(factory_document).resolve(node)
        if identity.get("state") == "unique" and identity.get("declaration_id") != factory_parameter_identity.get("declaration_id"):
            continue
        ancestor, top_capture = node.parent, None
        while ancestor is not None and ancestor != factory_function:
            if ancestor.type in _FUNCTIONS:
                owner_parent = ancestor.parent
                if owner_parent is not None and owner_parent.type == "pair":
                    owner_parent = owner_parent.parent
                if owner_parent == returned_object:
                    top_capture = ancestor
            ancestor = ancestor.parent
        member_read = node.parent is not None and node.parent.type in {"member_expression", "subscript_expression"} and node.parent.child_by_field_name("object") == node
        if identity.get("state") != "unique" or top_capture is None or not member_read:
            captured_formal_gaps.append({"reason": "unmodeled_factory_capture_or_escape", "location": factory_document.location(node), "identity": identity})
    if captured_formal_gaps:
        engine.gaps.append(_issue("navigation_factory_capture_escape_unknown",
            "只有最终返回方法内已界定的形参 member 捕获可注入；其他嵌套捕获/整对象逃逸/转义引用未闭合。",
            factory_document.source.path, capture_gap_count=len(captured_formal_gaps), capture_gap_samples=captured_formal_gaps[:12]))
        return result
    method_parameters = method.child_by_field_name("parameters")
    if method_parameters is None or any(_simple_parameter(item) is None for item in method_parameters.named_children if item.type != "comment"):
        engine.gaps.append(_issue("navigation_method_parameter_effect_unknown", "返回方法默认/rest/解构参数效果未建模。", factory_document.source.path))
        return result
    method_nodes = engine.sources.nodes.get(method_definition.graph_node_id, [])
    if len(method_nodes) != 1:
        engine.gaps.append(_issue("navigation_returned_method_graph_unknown", "返回方法没有唯一捕获图身份。", factory_document.source.path))
        return result
    _, _, problems = engine.sources.definition_for_node(method_nodes[0])
    engine.gaps.extend(problems)
    if problems:
        return result
    parameter_name = factory_document.text(pattern)
    binding_id = _digest({"file": factory_document.source.path, "source_hash": factory_document.source.hash,
        "declaration": _key(parameters), "scope": _key(factory_function), "name": parameter_name})
    context_id = _digest({"factory_edge": edge.id, "argument": document.location(args[index]),
        "callback": document.location(callback_function), "formal": factory_document.location(parameter)})[:24]
    frame = _Frame(factory_document, method_definition, method, ambient=navigation,
        ambient_path=rule["ambient"]["read_path"], mode="consumer", context_id=context_id)
    frame.env[binding_id] = engine.value("factory_options", extra={"parameter_binding_id": binding_id, "factory_context_id": context_id})
    frame.callbacks[(binding_id, selector["callback_property"])] = {"document": document,
        "definition": callback, "function": callback_function}
    engine.event("factory_callback_argument_mapping", _Frame(document, owner, function), call,
        edge_id=edge.id, factory_context_id=context_id, argument_index=index,
        argument_location=document.location(args[index]), callback_property=selector["callback_property"],
        callback_declaration=_definition_identity(document, callback),
        factory_declaration=_definition_identity(factory_document, factory),
        formal_parameter_location=factory_document.location(parameter), formal_binding_id=binding_id,
        returned_method=_definition_identity(factory_document, method_definition),
        relation="context-specific property/formal/capture mapping; not a callback CALLS edge")
    trace_start, lookup_start = len(engine.trace), len(engine.lookups)
    returns, continues = engine.execute(frame, method.child_by_field_name("body"))
    events = engine.trace[trace_start:]
    lookups = engine.lookups[lookup_start:]
    callback_guards = [event for event in events if event["operation"] == "branch_guard"
        and event["owner"] == callback.symbol and event.get("action") == "return_null" and event.get("lookup_dependencies")
        and event.get("branch") is True and event.get("condition_truth") is True
        and event.get("consequent_coverage_complete")]
    required_ids = {item for event in callback_guards for item in event["lookup_dependencies"]}
    required = [lookup for lookup in lookups if lookup["id"] in required_ids
        and context_id in (lookup.get("query_projection") or {}).get("guaranteed_contexts", [])]
    detached_required = [lookup for lookup in lookups if lookup["id"] in required_ids and lookup not in required]
    if detached_required:
        engine.gaps.append(_issue("navigation_lookup_ambient_origin_unproven", "空值守卫查询 receiver 未证明来自当前 ambient 导航的键投影，不能嫁接生产者。",
            document.source.path, lookup_count=len(detached_required), lookups=detached_required))
    null_throws = [event for event in events if event["operation"] == "branch_guard"
        and event["owner"] == method_definition.symbol and event.get("action") == "throw"
        and event.get("branch") is True and event.get("condition_truth") is True
        and context_id in event.get("factory_callback_contexts", [])]
    invocations = [event for event in events if event["operation"] == "invokes_injected_callback" and event.get("factory_context_id") == context_id]
    callback_results = [event for event in events if event["operation"] == "injected_callback_normal_result"
        and event.get("factory_context_id") == context_id]
    returns_throw = bool(returns and not continues and all(value.kind == "throw" for value in returns))
    result.update(source_complete=bool(required and callback_guards and null_throws and invocations and callback_results
            and all(event.get("all_normal_returns_null") for event in callback_results) and returns_throw),
        caller=_definition_identity(document, owner), factory_call_location=document.location(call),
        factory_call_edge_id=edge.id, factory_branch_conditions=_conditions(document, call, function),
        factory_call_source_node_id=edge.source, factory_call_target_node_id=edge.target,
        factory_declaration=_definition_identity(factory_document, factory),
        callback_declaration=_definition_identity(document, callback),
        formal_parameter_location=factory_document.location(parameter), formal_binding_id=binding_id,
        returned_method=_definition_identity(factory_document, method_definition), factory_context_id=context_id,
        query_lookups=lookups, required_query_keys=sorted({lookup["key"] for lookup in required}),
        null_return_guards=callback_guards, factory_null_throw_guards=null_throws,
        callback_invocations=invocations, callback_results=callback_results, callback_relation_closed=bool(invocations),
        factory_parameter_identity=factory_parameter_identity, factory_parameter_effect_review="no captured direct use or writes before returned closures",
        all_consumer_returns_throw=returns_throw,
        factory_function_kind=factory_kind, returned_method_function_kind=method_kind,
        returned_method_async=method_kind.get("kind") == "ordinary_async",
        rejection_semantics="async method body throw becomes rejected Promise; caller activation/handling not proved" if method_kind.get("body_throw_effect") == "promise_rejection" else "ordinary method body throw",
        selected_read_and_guard_on_normal_prefix=True,
        factory_method_result=engine.return_value(returns, continues).public(),
        interpretation="query absence implies the captured null/throw guards only when execution reaches them under the ambient assumption")
    return result


def _standard_models() -> list[dict]:
    return [
        {"id": "url-search-params-v1", "authority": "explicit trusted standard interface assumption",
            "semantics": "string constructor strips one initial question mark; UTF-8 form decoding, plus to space, ampersand delimiter; duplicate keys retain presence; empty value differs from null; set encodes values; get missing returns null",
            "source_reference": "https://url.spec.whatwg.org/#urlsearchparams", "actual_host_implementation_verified": False},
        {"id": "js-string-url-slicing-v1", "authority": "explicit trusted standard interface assumption",
            "semantics": "UTF-16 string slice/indexOf question-mark, finite prefix/template, encodeURIComponent delimiter exclusion; unsupported shapes unknown",
            "source_reference": "https://tc39.es/ecma262/", "actual_host_implementation_verified": False},
        {"id": "object-freeze-inert-v1", "authority": "explicit trusted standard interface assumption",
            "semantics": "returns same fresh literal object/array; shallow freeze; not runtime implementation or constructor identity proof",
            "source_reference": "https://tc39.es/ecma262/#sec-object.freeze", "actual_host_implementation_verified": False},
    ]


def _finding(snapshot: GraphSnapshot, rule: dict, details: dict) -> Finding:
    fingerprint = _digest({"version": VERSION, "policy_schema": POLICY_VERSION, "rule": rule, "project_id": snapshot.project_id})
    trace = details.get("source_trace", [])
    locations = [event["location"] for event in trace if event.get("location")]
    node_ids = sorted({event["ast_owner_id"] for event in trace if event.get("ast_owner_id") in {
        node.id for node in snapshot.nodes if node.kind in {"function", "method"}}})
    edge_ids = sorted({event["edge_id"] for event in trace if event.get("edge_id") in {edge.id for edge in snapshot.edges}})
    confirmed = bool(details.get("source_fact_confirmed"))
    title = "导航查询上下文条件链待复核" if confirmed else "导航查询上下文来源链未闭合"
    description = "URL 键域、参数/返回和 callback 注入/null 守卫来自保存源码；导航效果、触发时序及未闭合装配仍为未知。"
    evidence = Evidence(_digest({"snapshot": snapshot.id, "fingerprint": fingerprint, "details": details})[:24],
        "static_navigation_analysis", description, locations=locations, node_ids=node_ids, edge_ids=edge_ids, details=details)
    return Finding(id=_digest({"snapshot": snapshot.id, "fingerprint": fingerprint})[:24],
        type="static_navigation_query_context", severity=rule.get("severity", "medium"), status="uncertain",
        title=title, description=description, node_ids=node_ids, edge_ids=edge_ids, evidence=[evidence],
        rule_id=rule.get("id", "invalid-navigation-rule"), fingerprint=fingerprint, snapshot_id=snapshot.id,
        metadata={"navigation_analyzer_version": VERSION, "navigation_policy_version": POLICY_VERSION,
            "source_fact_confirmed": confirmed, "source_condition_chain_confirmed": confirmed,
            "full_functionality_proven": False, "runtime_proof": False,
            "missing_query_keys": details.get("missing_query_keys", []),
            "provenance": rule.get("provenance", {}), "applicability": rule.get("applicability", {})})


def analyze_navigation_contracts(snapshot: GraphSnapshot, rules: list[dict]) -> list[Finding]:
    if not isinstance(rules, list):
        return [_finding(snapshot, {"id": "invalid-navigation-rules", "severity": "info"},
            {"analysis_gaps": [_issue("navigation_rules_invalid", "导航合同必须是规则列表。")]})]
    sources, findings = SemanticSources(snapshot), []
    counts: dict[str, int] = {}
    for rule in rules:
        if isinstance(rule, dict) and isinstance(rule.get("id"), str):
            counts[rule["id"]] = counts.get(rule["id"], 0) + 1
    for index, rule in enumerate(rules):
        try:
            validate_navigation_rule(rule)
            if counts[rule["id"]] != 1:
                raise ValueError("navigation id 重复，不允许后规则覆盖。")
        except (ValueError, TypeError, OverflowError, RecursionError) as error:
            findings.append(_finding(snapshot, {"id": f"invalid-navigation-rule-{index}", "severity": "info"},
                {"analysis_gaps": [_issue("navigation_rule_invalid", str(error))]}))
            continue
        engine = _Engine(snapshot, sources, rule)
        producer, value = _producer(engine, rule["producer"])
        consumer = _consumer(engine, rule, value)
        counterexamples = []
        for selector in rule.get("counterexample_producers", []):
            counter_engine = _Engine(snapshot, sources, rule)
            counter, _ = _producer(counter_engine, selector)
            counter["source_trace"] = counter_engine.trace
            counter["source_trace_complete"] = not any(gap.get("code") == "navigation_trace_budget" for gap in counter_engine.gaps)
            counter["analysis_gaps"] = counter_engine.gaps
            counterexamples.append(counter)
        domain = producer["query_domain"]
        missing = sorted(set(consumer["required_query_keys"]) - set(domain["possible_keys"])) if domain["keyset_closed"] else []
        gaps = [*engine.gaps,
            _issue("navigation_effect_not_observed", "href 到当前 hash 的平台效果不是观察到的执行事实。"),
            _issue("ambient_hash_read_timing_unknown", "实际读取前 URL 是否被改写尚未证明。"),
            _issue("ui_route_dispatch_not_followed", "目的路由选择和消费者触发尚未自动闭合。")]
        port_wiring = {"source_facts": [], "unresolved": [_issue("port_wiring_not_selected", "正常 boot/真实 factory 分支及 taskPort→VM→submit 使用未自动闭合。")]}
        if rule.get("wiring") is not None:
            try:
                from .port_wiring import analyze_port_wiring
                port_wiring = analyze_port_wiring(snapshot, rule)
            except (ImportError, ValueError, TypeError, RuntimeError, RecursionError, AttributeError) as error:
                port_wiring = {"source_facts": [], "unresolved": [_issue("port_wiring_unavailable", f"装配模型尚未闭合：{type(error).__name__}: {str(error)[:200]}")]}
            wiring_factory = port_wiring.get("consumer_factory") or {}
            expected_location = consumer.get("factory_call_location") or {}
            wired_location = wiring_factory.get("location") or {}
            location_keys = ("file", "source_hash", "start_byte", "end_byte", "span_hash", "semantic_parse_id")
            same_factory = bool(consumer.get("factory_call_edge_id") and wiring_factory.get("edge_id") == consumer.get("factory_call_edge_id")
                and wiring_factory.get("source_graph_node_id") == consumer.get("factory_call_source_node_id")
                and wiring_factory.get("target_graph_node_id") == consumer.get("factory_call_target_node_id")
                and all(key in expected_location and expected_location[key] == wired_location.get(key) for key in location_keys))
            port_wiring["navigation_context_identity_matched"] = same_factory
            if not same_factory:
                port_wiring["assembly_complete"] = False
                port_wiring["source_fact_confirmed"] = False
                port_wiring.setdefault("unresolved", []).append(_issue("port_wiring_consumer_context_unmatched",
                    "装配工厂与 callback 条件链的原始调用身份未精确对应，不能合成为同一上下文。"))
        gaps.extend(port_wiring.get("unresolved", []))
        trace_complete = not any(gap.get("code") == "navigation_trace_budget" for gap in engine.gaps)
        confirmed = bool(missing and producer["source_complete"] and consumer["source_complete"] and trace_complete)
        details = {"analyzer_version": VERSION, "policy_version": POLICY_VERSION, "semantic_source_version": SOURCE_VERSION,
            "semantic_environment_version": ENVIRONMENT_VERSION, "completion_summaries_version": COMPLETION_VERSION,
            "snapshot_id": snapshot.id, "source_hash": snapshot.source_hash, "policy_hash": snapshot.policy_hash,
            "contract_hash": _digest(rule), "producer": producer, "consumer": consumer,
            "counterexample_producers": counterexamples, "source_trace": engine.trace, "source_trace_complete": trace_complete,
            "standard_models": _standard_models(),
            "ambient_assumptions": rule["ambient"], "applicability": rule["applicability"], "provenance": rule["provenance"],
            "analysis_gaps": gaps, "port_wiring": port_wiring, "missing_query_keys": missing,
            "source_fact_confirmed": confirmed, "full_functionality_proven": False, "runtime_proof": False,
            "analysis_scope": "source-derived finite normal-return summaries and contextual callback/null guards; no runtime/transport proof",
            "semantic_assumptions": {"standard_environment_stable": "explicit trusted API premise, not verified runtime implementation",
                "opaque_prefix": "claims condition on reaching selected reads and guards via normal prefix; no guarantee of helper return or callback activation",
                "query_projection": "guaranteed context requires supported data query-tail or controlled empty query of the same hash identity in every joined branch"},
            "captured_source_files": [{"file": path, "source_hash": document.source.hash, "parse_id": document.parse_id}
                for path, (document, _) in sorted(sources.cache.items()) if document is not None]}
        findings.append(_finding(snapshot, rule, details))
    return findings
