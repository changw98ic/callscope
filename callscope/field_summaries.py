"""Selected-field AST adapter over the shared immutable semantic state IR.

The adapter selects saved syntax, authenticates bindings and supplies explicit
language-model premises. Allocation, shallow copying, alias effects and branch
joins are performed by semantic_ir, never by adapter-owned mutable values.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from . import semantic_ir as ir
from .models import GraphSnapshot
from .semantic_sources import SemanticSources, VERSION as SOURCE_VERSION, unwrap, walk
from .lexical_bindings import LexicalBindings, VERSION as LEXICAL_VERSION
from .completion_summaries import function_kind, completion_relation, VERSION as COMPLETION_VERSION
from .semantic_environment import BuiltinEnvironment, VERSION as ENVIRONMENT_VERSION
from .field_relations import collect_site_relations, VERSION as RELATIONS_VERSION
from .static_contracts import _digest, _issue, _literal_string

VERSION = "finite-field-summaries-5-ir"
MODEL_ID = "ecmascript-own-enumerable-field-copy-v1"
READ_MODEL_ID = "ecmascript-own-data-read-v1"
_FUNCTIONS = {"function_declaration", "generator_function_declaration", "function_expression", "generator_function", "arrow_function", "method_definition"}
_CLASSES = {"class", "class_declaration", "class_expression"}
_TYPE_ONLY_NODES = {"type_annotation", "type_alias_declaration", "interface_declaration", "type_query",
    "type_arguments", "type_parameters", "implements_clause", "import_type", "function_type"}
_LIMIT, _DEPTH, _BRANCHES, _FACT_LIMIT = 4096, 8, 32, 1024


def _children(node: Any) -> list[Any]:
    return [child for child in node.named_children if child.type not in {"comment", "type_annotation", "type_arguments"}] if node is not None else []


def _field(node: Any, name: str) -> Any:
    return node.child_by_field_name(name) if node is not None else None


def _function(definition: Any) -> Any:
    node = unwrap(definition.value) if definition is not None and definition.value is not None else definition.node if definition is not None else None
    return node if node is not None and node.type in _FUNCTIONS else None


def _direct(node: Any):
    pending = [node] if node is not None else []
    while pending:
        current = pending.pop()
        yield current
        if current != node and current.type in _FUNCTIONS | _CLASSES:
            continue
        pending.extend(reversed(_children(current)))


def _runtime_nodes(node: Any):
    """Visit nested runtime syntax while erasing TS annotation subtrees."""
    pending = [node] if node is not None else []
    while pending:
        current = pending.pop()
        if current.type in _TYPE_ONLY_NODES or current.type.endswith("_type"):
            continue
        yield current
        if current.type in {"as_expression", "satisfies_expression", "type_assertion", "non_null_expression"}:
            operand = unwrap(current)
            if operand is not None and operand.id != current.id:
                pending.append(operand)
                continue
        pending.extend(reversed(_children(current)))


def _name(document: Any, node: Any) -> str | None:
    if node is None:
        return None
    text = document.text(node)
    if node.type in {"identifier", "property_identifier", "shorthand_property_identifier", "shorthand_property_identifier_pattern"}:
        return text if text and "\\" not in text else None
    if node.type == "string":
        name = _literal_string(text)
        return name if name is not None and not any(0xD800 <= ord(char) <= 0xDFFF for char in name) else None
    return None


def _key(document: Any, node: Any) -> str | None:
    child = _field(node, "property") if node.type == "member_expression" else unwrap(_field(node, "index"))
    return _name(document, child) if child is not None and (node.type == "member_expression" or child.type == "string") else None


def _path(document: Any, node: Any) -> list[str] | None:
    node = unwrap(node)
    if node is None:
        return None
    if node.type == "identifier":
        name = _name(document, node)
        return [name] if name is not None else None
    if node.type in {"member_expression", "subscript_expression"}:
        root, key = _path(document, _field(node, "object")), _key(document, node)
        return [*root, key] if root is not None and key is not None else None
    return None


@dataclass(frozen=True)
class _Context:
    """AST handle keys are adapter data; no source handle is stored in IR."""
    context_id: str
    handle_id: str
    conditions: tuple[str, ...] = ()
    captures: tuple[ir.BindingKey, ...] = ()


@dataclass(frozen=True)
class _Returned:
    context: _Context
    state: ir.State
    node: Any
    value: ir.ValueRef


class FieldSummaryBuilder:
    def __init__(self, snapshot: GraphSnapshot, models: list[str]):
        self.snapshot, self.models = snapshot, models
        self.sources = SemanticSources(snapshot)
        self.handles: dict[str, tuple[Any, Any, Any]] = {}
        self.binders: dict[str, LexicalBindings] = {}
        self.environments: dict[str, BuiltinEnvironment] = {}
        self.facts: dict[str, dict] = {}
        self.diagnostics: dict[str, dict] = {}
        self.guards: dict[str, dict] = {}
        self.assessments: list[dict] = []
        self.normal_returns: list[dict] = []
        self.abrupt: list[dict] = []
        self.sink: dict = {}
        self.source_binding: ir.BindingKey | None = None
        self.source_path: tuple[str, ...] = ()
        self.operations = 0
        self.incomplete = False
        self.stack: list[str] = []
        self.site_nodes: tuple[Any, ...] = ()
        self.root_handle = ""
        self.active_contexts: list[_Context] = []
        self.model_guards: dict[str, ir.ModelGuard] = {}
        self.return_fallthrough = False
        self.local_copy_witnesses: dict[str,list[dict]] = {}
        self.subject_identity: dict = {}

    def context(self, document: Any, definition: Any, context_id: str, *, captures: tuple[ir.BindingKey, ...] = ()) -> _Context:
        handle_id = _digest((document.source.path, definition.graph_node_id, definition.symbol))[:24]
        self.handles[handle_id] = (document, definition, _function(definition))
        return _Context(context_id, handle_id, captures=captures)

    def parts(self, context: _Context) -> tuple[Any, Any, Any]:
        return self.handles[context.handle_id]

    def evidence(self, context: _Context, node: Any, kind: str = "source", *, proof: ir.ModelGuard | None = None) -> ir.EvidenceRef:
        document, _, _ = self.parts(context)
        guard_ids = (*context.conditions, *((self.model_guards[context.context_id].guard_id,) if context.context_id in self.model_guards else ()), *((proof.guard_id,) if proof else ()))
        return ir.evidence(document.source.path, document.source.hash, node.start_byte if node is not None else 0,
            node.end_byte if node is not None else 0, MODEL_ID, guard_ids=guard_ids,
            snapshot_id=self.snapshot.id, context_id=context.context_id, kind=kind)

    def lexical(self, document: Any) -> LexicalBindings:
        if document.source.path not in self.binders:
            self.binders[document.source.path] = LexicalBindings(document)
        return self.binders[document.source.path]

    def diagnostic(self, code: str, message: str, context: _Context | None = None, node: Any = None, **details: Any) -> str:
        document = self.parts(context)[0] if context is not None else None
        result = _issue(code, message, document.source.path if document is not None else "", node.start_point.row + 1 if node is not None else 0)
        if document is not None and node is not None:
            result["location"] = document.location(node)
        result.update(details)
        identifier = _digest(result)[:24]
        self.diagnostics[identifier] = result
        return identifier

    def fact(self, operation: str, context: _Context, node: Any, **details: Any) -> None:
        if len(self.facts) >= _FACT_LIMIT:
            self.incomplete = True
            self.diagnostic("field_fact_budget", "来源事实预算耗尽；不声明完整源式。")
            return
        document, definition, _ = self.parts(context)
        result = {"operation": operation, "location": document.location(node), "owner": definition.symbol,
            "graph_node_id": document.call_owner(node), "call_context": context.context_id, **details}
        result["id"] = _digest(result)[:24]
        self.facts[result["id"]] = result

    def tick(self) -> bool:
        self.operations += 1
        if self.operations > _LIMIT:
            self.incomplete = True
            self.diagnostic("field_analysis_budget", "有限 adapter 预算耗尽，后续来源必须 unknown。")
            return False
        return True

    def unknown(self, context: _Context, node: Any, reason: str, *, external: bool = True, capture_unknown: bool = False) -> ir.ValueRef:
        self.diagnostic(reason, "有限源码形式或效果未闭合。", context, node)
        return ir.value("unknown", self.evidence(context, node), external_alias=external,
            capture_unknown=capture_unknown, barriers=(reason,))

    def bounded_external(self, context: _Context, state: ir.State, node: Any, reason: str, *, roots: tuple[ir.ValueRef, ...] = (), basis: str) -> tuple[ir.State, ir.ValueRef]:
        """Unknown contents, with a source-certified external referent domain."""
        source = self.evidence(context,node,"external_domain_source")
        proof = ir.guard((source,),MODEL_ID,capabilities=("external_value_domain",),supported=True,
            assumptions=(basis,"value contents/type/completion remain unknown; possible referents are evaluated roots and the external/escaped domain, not unexposed future local allocations"))
        state = ir.register_guard(state,proof)
        at = self.evidence(context,node,"external_domain_value",proof=proof)
        pending, seen, aliases, captures = list(roots), set(), set(), set()
        while pending:
            root = pending.pop()
            if root.value_id in seen:
                continue
            seen.add(root.value_id)
            if root.object_ref is not None:
                aliases.add(root.object_ref)
            aliases.update(root.alias_roots)
            captures.update(root.captured_bindings)
            pending.extend(root.alternatives)
        value = ir.value("unknown",at,external_alias=True,alias_roots=tuple(sorted(aliases,key=lambda ref:ref.alloc_id)),
            captured_bindings=tuple(sorted(captures,key=lambda key:(key.declaration_id,key.context_id))),barriers=(reason,))
        self.fact("bounded_external_value_domain",context,node,model_guard=ir.to_data(proof),value_id=value.value_id,
            actual_root_value_ids=[root.value_id for root in roots],content_or_referent_stability_proven=False)
        return state,value

    def audit(self, context: _Context, node: Any) -> bool:
        document, _, _ = self.parts(context)
        if document.source.path not in self.environments:
            self.environments[document.source.path] = BuiltinEnvironment(document)
        result = self.environments[document.source.path].audit("Object", node)
        self.fact("own_data_copy_environment", context, node, audit=result, field_model=MODEL_ID,
            runtime_source_plainness_verified=False,
            copy_source_surface_condition="entire source ordinary own-enumerable data surface, no Proxy or other getter enumeration effects; child referents not certified")
        supported = bool(result.get("supported") and MODEL_ID in self.models)
        if context.context_id not in self.model_guards:
            source_ref = self.evidence(context, node, "model_source_environment")
            proof = ir.guard((source_ref,), MODEL_ID, capabilities=("own_data_shape", "own_data_copy", "own_data_write"),
                supported=supported, assumptions=("entire current copy source is an ordinary own-enumerable data surface, without Proxy or other getter enumeration effects",
                    "this model does not certify child referents or runtime standard APIs"))
            self.model_guards[context.context_id] = proof
            self.fact("registered_own_data_model_guard", context, node, model_guard=ir.to_data(proof), environment_audit=result)
        return supported

    def key_for(self, context: _Context, node: Any, state: ir.State, *, declaring: bool = False) -> tuple[ir.BindingKey | None, dict]:
        document, _, function = self.parts(context)
        identity = self.lexical(document).resolve(node)
        if identity.get("state") != "unique":
            return None, identity
        key = ir.BindingKey(identity["declaration_id"], context.context_id)
        if declaring:
            return key, identity
        declaration = self.lexical(document).declaration_for(identity)
        parent = declaration.parent if declaration is not None else None
        while parent is not None and parent.type not in _FUNCTIONS:
            parent = parent.parent
        if parent is not None and function is not None and parent.id == function.id:
            return key, identity
        captures = {candidate for candidate in context.captures if candidate.declaration_id == key.declaration_id}
        if len(captures) == 1:
            return next(iter(captures)), identity
        if parent is not None:
            owners = [candidate for candidate in self.active_contexts if self.parts(candidate)[0] is document
                and self.parts(candidate)[2] is not None and self.parts(candidate)[2].id == parent.id]
            if len(owners) == 1:
                return ir.BindingKey(key.declaration_id, owners[0].context_id), identity
            return None, {**identity, "state": "unknown", "reason": "outer_activation_not_unique"}
        return ir.BindingKey(key.declaration_id, "module:" + document.source.hash), identity

    def projection(self, context: _Context, state: ir.State, value: ir.ValueRef, path: tuple[str, ...], at: Any) -> ir.Projection:
        if not path:
            obj = ir.lookup_object(state, value)
            return ir.Projection("present", value, not value.barriers and value.kind != "unknown",
                bool(obj and obj.closed_shape and not obj.barriers))
        observations: tuple[ir.ObservationRef, ...] = ()
        barriers: tuple[str, ...] = ()
        closed = True
        result = ir.Projection("unknown", value, False, False)
        for index, key in enumerate(path):
            if not self.tick():
                return ir.Projection("unknown", self.unknown(context, at, "field_read_budget"), False, False)
            # Each additional external own-data surface is an explicit model
            # condition, never an inference from the parent parameter type.
            # The certified root ObjectVersion already records its surface
            # guard. A symbolic child receives no recursive plainness premise.
            result = ir.lookup_field(state, value, key, self.evidence(context, at), external_own_data=False)
            observations += result.observations
            barriers += result.barriers
            closed = closed and result.closed
            value = result.value
            if result.presence == "absent":
                break
        return ir.Projection(result.presence, result.value, closed, result.whole_closed,
            observations, tuple(sorted(set(barriers))))

    def ordinary_get(self, context: _Context, state: ir.State, receiver: ir.ValueRef, key: str, at: Any) -> tuple[ir.State, ir.ValueRef]:
        """Own-slot queries and JavaScript Get have independent premises."""
        obj = ir.lookup_object(state, receiver)
        selected = self.projection(context, state, receiver, (key,), at)
        document, _, _ = self.parts(context)
        source_ref = ir.evidence(document.source.path, document.source.hash, at.start_byte, at.end_byte, READ_MODEL_ID,
            guard_ids=context.conditions, snapshot_id=self.snapshot.id, context_id=context.context_id, kind="actual_get")
        supported = bool(READ_MODEL_ID in self.models and obj is not None and obj.model_supported)
        proof = ir.guard((source_ref,), READ_MODEL_ID, capabilities=("ordinary_own_data_get",), supported=supported,
            assumptions=("at this actual Get, an existing selected own property is ordinary data (enumerability is not required)",
                "if the own property is missing this Get returns undefined without prototype, accessor or Proxy effects",
                "this read premise does not certify any child referent surface, presence, type or runtime value"))
        self.fact("registered_actual_get_model", context, at, key=key, model_guard=ir.to_data(proof),
            receiver_allocation=obj.alloc_id if obj else None, receiver_version=obj.version_id if obj else None,
            own_presence=selected.presence, own_slot_source_closed=selected.closed,
            non_recursive_child_model=True, runtime_get_verified=False)
        state=ir.register_guard(state,proof)
        read_at=ir.evidence(document.source.path,document.source.hash,at.start_byte,at.end_byte,READ_MODEL_ID,
            guard_ids=(*context.conditions,proof.guard_id),snapshot_id=self.snapshot.id,context_id=context.context_id,kind="actual_get_application")
        if ir.supports_guard(proof,read_at,"ordinary_own_data_get"):
            if selected.presence == "absent" and selected.closed and not selected.barriers and not selected.value.barriers:
                return state, ir.value("literal", read_at, literal_kind="undefined", source_text="undefined")
            if not selected.closed or selected.barriers or selected.value.barriers or selected.value.capture_unknown:
                # The Get premise excludes getter invocation; it does not
                # restore a previously damaged slot's source or presence.
                return self.bounded_external(context,state,at,"field_get_value_origin_unknown",roots=(receiver,),
                    basis="registered actual ordinary own-data Get; this unknown slot value is reachable from its authenticated receiver")
            return state, selected.value
        external_domain = ir.external_domain_supported(state, receiver)
        state = self.effect(context,state,at,(receiver,),complete=external_domain,reason="field_actual_get_unregistered_or_receiver_unknown")
        if external_domain:
            return self.bounded_external(context,state,at,"field_external_getter_value_unknown",roots=(receiver,),
                basis="source-certified external receiver domain; getter/value effects remain unknown and may reach that receiver/exposed roots but not unexposed caller-local allocations")
        return state,self.unknown(context,at,"field_actual_get_unknown",capture_unknown=True)

    def effect(self, context: _Context, state: ir.State, node: Any, roots: tuple[ir.ValueRef, ...], *,
               complete: bool, reflection: bool = False, reason: str = "opaque_call_effects_unknown", captured: tuple[ir.BindingKey, ...] = ()) -> ir.State:
        visible = tuple(ref for key, ref in state.bindings if key.context_id == context.context_id)
        proof = ir.guard((self.evidence(context, node, "effect_scope_source"),), MODEL_ID,
            capabilities=("effect_roots", "lexical_capture_domain"), supported=not reflection,
            assumptions=("effect roots include evaluated arguments, receiver, lexical capture cells and previously escaped/external allocations",
                "authenticated lexical activation does not acquire unescaped caller-local allocations merely through unknown child contents"))
        result = ir.invalidate_reachable(state, roots, self.evidence(context, node, "effect", proof=proof), reason=reason,
            roots_complete=complete, captures_complete=complete, visible_roots=visible,
            captured_bindings=captured, reflection=reflection, model_guard=proof)
        previous = {item.effect_id for item in state.effects}
        self.fact("registered_effect_scope_guard", context, node, model_guard=ir.to_data(proof),
            roots_complete=complete, visible_binding_context=context.context_id, reflection=reflection, reason=reason,
            actual_roots=[{"value_id":ref.value_id,"kind":ref.kind,"domain_complete":ir.external_domain_supported(state,ref),
                "capture_unknown":ref.capture_unknown,"captured_bindings":ir.to_data(ref).get("captured_bindings",[])} for ref in roots],
            effect_ids=[item.effect_id for item in result.effects if item.effect_id not in previous])
        return result

    def truth(self, state: ir.State, value: ir.ValueRef) -> bool | None:
        if value.barriers:
            return None
        if value.kind == "literal":
            if value.literal_kind in {"false", "null", "undefined"}:
                return False
            if value.literal_kind == "true":
                return True
        obj = ir.lookup_object(state, value)
        if obj is not None and obj.fresh:
            return True
        return None

    def not_undefined(self, state: ir.State, value: ir.ValueRef) -> bool:
        return not value.barriers and (value.kind == "literal" and value.literal_kind != "undefined"
            or value.kind == "object" and bool(ir.lookup_object(state, value) and ir.lookup_object(state, value).fresh))

    def guard(self, context: _Context, node: Any, branch: str) -> _Context:
        document, _, _ = self.parts(context)
        record = {"branch": branch, "location": document.location(node), "text": document.text(node), "truth_proven": False}
        identifier = _digest(record)[:24]
        self.guards[identifier] = record
        return _Context(context.context_id, context.handle_id, (*context.conditions, identifier), context.captures)

    def bind_pattern(self, context: _Context, state: ir.State, pattern: Any, value: ir.ValueRef, *, provided: bool = False) -> ir.State:
        pattern = unwrap(pattern)
        if pattern is None:
            return self.effect(context, state, pattern, (), complete=False, reflection=True, reason="field_binding_pattern_missing")
        document, _, _ = self.parts(context)
        if pattern.type in {"required_parameter", "optional_parameter"}:
            default = _field(pattern, "value")
            binder = _field(pattern, "pattern") or _field(pattern, "name")
            if default is not None and not provided and not self.not_undefined(state, value):
                before = state
                after, fallback = self.eval(context, state, default)
                state = ir.join_states((before, after), self.evidence(context, default))
                value = ir.join_values((value, fallback), self.evidence(context, default))
                self.fact("conditional_parameter_default", context, pattern, default_location=document.location(default), provided_value_proven=False)
            return self.bind_pattern(context, state, binder, value, provided=provided)
        if pattern.type in {"identifier", "shorthand_property_identifier_pattern"}:
            key, identity = self.key_for(context, pattern, state, declaring=True)
            if key is None:
                self.diagnostic("field_binding_identity_unknown", "声明不唯一，不能按裸名称绑定。", context, pattern, identity=identity)
                return self.effect(context, state, pattern, (), complete=False, reflection=True, reason="field_binding_identity_unknown")
            immutable = ir.guard((self.evidence(context,pattern,"immutable_lexical_declaration"),),MODEL_ID,
                capabilities=("immutable_lexical_cell",),supported=identity.get("declaration_kind")=="const",
                assumptions=("source-authenticated const declaration's initialized lexical binding cannot be reassigned by ordinary code",
                    "referenced objects and captured cells remain mutable; this premise does not freeze the referent"))
            state = ir.bind(state, key, value, self.evidence(context, pattern,proof=immutable),immutable_guard=immutable)
            self.fact("lexical_value_binding", context, pattern, declaration_id=key.declaration_id,
                binding_context=key.context_id, value_id=value.value_id, value_kind=value.kind,
                immutable_cell_model_guard=ir.to_data(immutable))
            return state
        if pattern.type == "object_pattern":
            keys = []
            keys_closed = True
            children = _children(pattern)
            for child in children:
                if child.type == "rest_pattern":
                    continue
                key_node = _field(child, "key") if child.type == "pair_pattern" else _field(child, "left") if child.type == "object_assignment_pattern" else child
                name = _name(document, key_node)
                if name is None:
                    keys_closed = False
                else:
                    keys.append(name)
            self.fact("object_destructure_keys", context, pattern, actual_extracted_keys=keys, keys_closed=keys_closed,
                has_rest=any(child.type == "rest_pattern" for child in children), copy_scope="none_at_pattern_level")
            for child in children:
                if child.type == "rest_pattern":
                    supported = self.audit(context, child)
                    state, rest = ir.copy_own_slots(state, value, self.evidence(context, child, "rest_copy"), context_id=context.context_id,
                        excluded_keys=tuple(keys), exclusions_closed=keys_closed, model_supported=supported,
                        model_guard=self.model_guards.get(context.context_id))
                    binder = next(iter(_children(child)), None)
                    state = self.bind_pattern(context, state, binder, rest)
                    key, _ = self.key_for(context, binder, state)
                    self.fact("object_rest_copy", context, child, actual_excluded_keys=keys, exclusions_closed=keys_closed,
                        rest_binding_id=key.declaration_id if key else None, input_value_id=value.value_id, output_value_id=rest.value_id,
                        copy_scope="rest_binding_only", source_copy_is_new_object=True, source_copy_is_shallow=True,
                        copy_model_supported=supported, ir_object=ir.to_data(ir.lookup_object(state, rest)) if ir.lookup_object(state, rest) else None)
                elif child.type in {"pair_pattern", "object_assignment_pattern", "shorthand_property_identifier_pattern"}:
                    name_node = _field(child, "key") if child.type == "pair_pattern" else _field(child, "left") if child.type == "object_assignment_pattern" else child
                    name = _name(document, name_node)
                    if name is not None:
                        state, selected = self.ordinary_get(context,state,value,name,child)
                    else:
                        state = self.effect(context,state,child,(),complete=False,reflection=True,reason="field_computed_destructure")
                        selected = self.unknown(context,child,"field_computed_destructure")
                    binder = _field(child, "value") if child.type == "pair_pattern" else _field(child, "left") if child.type == "object_assignment_pattern" else child
                    if child.type == "object_assignment_pattern" and not self.not_undefined(state, selected):
                        after, fallback = self.eval(context, state, _field(child, "right"))
                        state = ir.join_states((state, after), self.evidence(context, child))
                        selected = ir.join_values((selected, fallback), self.evidence(context, child))
                    state = self.bind_pattern(context, state, binder, selected)
                else:
                    state = self.effect(context, state, child, (), complete=False, reflection=True, reason="field_destructure_unsupported")
            return state
        if pattern.type in {"assignment_pattern", "object_assignment_pattern"}:
            if not self.not_undefined(state, value):
                after, fallback = self.eval(context, state, _field(pattern, "right"))
                state = ir.join_states((state, after), self.evidence(context, pattern))
                value = ir.join_values((value, fallback), self.evidence(context, pattern))
            return self.bind_pattern(context, state, _field(pattern, "left"), value)
        return self.effect(context, state, pattern, (), complete=False, reflection=True, reason="field_binding_pattern_unsupported")

    def callable(self, context: _Context, state: ir.State, node: Any) -> tuple[ir.State, ir.ValueRef]:
        document, _, _ = self.parts(context)
        captured, incomplete = set(), False
        for child in _runtime_nodes(node):
            if child.type in {"this","super","meta_property","with_statement"} or child.type=="identifier" and document.text(child)=="arguments" and self.lexical(document).unbound("arguments",child).get("unbound"):
                incomplete = True
                self.diagnostic("field_implicit_callable_capture_unknown","未建模的隐式词法捕获保留未知。",context,child)
            if child.type not in {"identifier", "shorthand_property_identifier"}:
                continue
            # Exclude declarations owned by the callable before resolving a
            # capture activation. Its future parameters/locals do not belong
            # to the creator's current activation and are not free captures.
            identity = self.lexical(document).resolve(child)
            declaration = identity.get("declaration_span", {})
            if node.start_byte <= declaration.get("start_byte", -1) < node.end_byte:
                continue
            if identity.get("declaration_kind") == "import":
                continue
            key, identity = self.key_for(context, child, state)
            if key is None:
                incomplete = incomplete or not self.lexical(document).unbound(document.text(child), child).get("unbound")
                continue
            # Capture a lexical cell, including one initialized later. The
            # shared IR reads the cell's current value at the opaque use.
            captured.add(key)
            if key.context_id.startswith("module:") and not any(cell == key for cell, _ in state.bindings):
                # A genuine module free cell is retained as a live cell, not
                # omitted or confused with a missing caller-local activation.
                # It can reach the exposed world; its contents stay unknown.
                state, current = self.bounded_external(context,state,child,"field_module_capture_value_unknown",
                    basis="source-authenticated module declaration cell outside this function activation; its unknown current value cannot reach unexposed caller-local allocations")
                declaration = self.lexical(document).declaration_for(identity)
                owner = ir.guard((self.evidence(context,declaration,"module_cell_declaration_owner"),),MODEL_ID,
                    capabilities=("external_lexical_cell_domain",),supported=identity.get("state")=="unique",
                    assumptions=("actual unique lexical declaration has no function owner; its live cell belongs to the captured module outside the current activation",
                        "unknown replacement values may reach evaluated roots and the exposed world; declaration identity does not establish value contents or purity"))
                state = ir.bind(state,key,current,self.evidence(context,declaration,"module_capture_cell",proof=owner),external_guard=owner)
                self.fact("authenticated_module_capture_cell_seed",context,child,binding_key=ir.to_data(key),
                    declaration_id=identity["declaration_id"],declaration_location=identity["declaration_location"],
                    seeded_value_id=current.value_id,unique_lexical_identity=True,only_if_absent=True,
                    cell_owner_guard=ir.to_data(owner),
                    cell_is_outside_current_function_activation=True,live_cell_and_future_rebind_retained=True)
        ref = ir.value("callable", self.evidence(context, node), captured_bindings=tuple(sorted(captured, key=lambda key:(key.declaration_id,key.context_id))),
            capture_unknown=incomplete)
        self.fact("actual_callable_capture_cells",context,node,value_id=ref.value_id,capture_unknown=incomplete,
            captured_bindings=ir.to_data(ref)["captured_bindings"],callee_internal_declarations_excluded=True)
        return state,ref

    def eval(self, context: _Context, state: ir.State, node: Any, *, expand: bool = False) -> tuple[ir.State, ir.ValueRef]:
        node = unwrap(node)
        if node is None or not self.tick():
            return state, self.unknown(context, node, "field_expression_missing_or_budget")
        document, _, _ = self.parts(context)
        kind = node.type
        evidence = self.evidence(context, node)
        if kind in {"string", "number", "true", "false", "null"}:
            text = document.text(node)
            if kind == "number" and len(text) > 1 and text[0] == "0" and text[1].isdigit():
                return state, self.unknown(context, node, "field_legacy_number_unknown")
            return state, ir.value("literal", evidence, literal_kind=kind, source_text=text,
                provenance=(ir.ProvenanceRef("literal_source_expression", evidence),))
        if kind == "undefined":
            if document.source.path not in self.environments:
                self.environments[document.source.path] = BuiltinEnvironment(document)
            audited = self.environments[document.source.path].audit("undefined", node)
            self.fact("undefined_environment_guard", context, node, audit=audited)
            return state, ir.value("literal", evidence, literal_kind="undefined", source_text="undefined") if audited.get("supported") else self.unknown(context, node, "field_undefined_identity_unknown")
        if kind in {"identifier", "shorthand_property_identifier"}:
            key, identity = self.key_for(context, node, state)
            if key is not None and any(candidate == key for candidate, _ in state.bindings):
                return state, ir.lookup_binding(state, key, evidence)
            if document.text(node)=="arguments" and self.lexical(document).unbound("arguments",node).get("unbound"):
                state=self.effect(context,state,node,(),complete=False,reflection=True,reason="field_implicit_arguments_unmodeled")
                return state,self.unknown(context,node,"field_implicit_arguments_unmodeled",capture_unknown=True)
            if identity.get("state") == "unique" and identity.get("declaration_kind") in {"function", "import"}:
                declaration = self.lexical(document).declaration_for(identity)
                if identity.get("declaration_kind") == "function" and declaration is not None and declaration.type in _FUNCTIONS:
                    return self.callable(context, state, declaration)
                return state, ir.value("callable", evidence, external_alias=True)
            if identity.get("state") == "unique" and identity.get("value", {}).get("stable"):
                initializer = unwrap(self.lexical(document).initializer_for(identity))
                if initializer is not None and initializer.type in {"string", "number", "true", "false", "null"}:
                    return self.eval(context, state, initializer)
            if key is not None and key.context_id.startswith("module:") or self.lexical(document).unbound(document.text(node),node).get("unbound"):
                return self.bounded_external(context,state,node,"field_external_lexical_value_unknown",
                    basis="authenticated module binding or lexical absence; the binding is outside this function activation, not a captured local cell")
            return state, self.unknown(context, node, "field_reference_value_unknown",capture_unknown=True)
        if kind in _FUNCTIONS:
            return self.callable(context, state, node)
        if kind in {"member_expression", "subscript_expression"}:
            state, receiver = self.eval(context, state, _field(node, "object"))
            key = _key(document, node)
            if key is None:
                state = self.effect(context, state, node, (receiver,), complete=False, reflection=True, reason="field_dynamic_member_effect_unknown")
                return state, self.unknown(context, node, "field_dynamic_member_unknown")
            return self.ordinary_get(context,state,receiver,key,node)
        if kind == "object":
            supported = self.audit(context, node)
            supported = supported and all(child.type == "spread_element" or child.type in {"pair","shorthand_property_identifier","method_definition"}
                and _name(document,_field(child,"key") if child.type=="pair" else _field(child,"name") if child.type=="method_definition" else child) not in {None,"__proto__"}
                and not (child.type=="method_definition" and any(item.type in {"get","set"} for item in child.children)) for child in _children(node))
            construction = ir.guard((self.evidence(context, node, "literal_construction_source"),), MODEL_ID,
                capabilities=("private_literal_construction",), supported=supported,
                assumptions=("this ordinary static data literal's new destination is an unnamed temporary during property evaluation, before the initializer binding is assigned",
                    "property expressions and registered shallow spreads do not receive that destination; children have no implicit reverse parent edge",
                    "protection ends before binding/return/argument exposure and does not exempt actual reachable roots, reflection, unsupported members or exhausted analysis"))
            evidence = self.evidence(context, node, "literal_allocation", proof=construction)
            state, result = ir.allocate(state, evidence, context_id=context.context_id, model_supported=supported,
                model_guard=self.model_guards.get(context.context_id), construction_guard=construction)
            keys, parts, boundaries = [], [], []
            members = _children(node)
            for member_index,child in enumerate(members):
                if child.type == "spread_element":
                    state, source = self.eval(context, state, next(iter(_children(child)), None), expand=True)
                    state, result, boundary = ir.copy_with_boundary_observation(state,source,result,self.sink.get("field_path",[""])[0],
                        self.evidence(context,child,"ordered_spread"),context_id=context.context_id,model_supported=supported,
                        model_guard=self.model_guards.get(context.context_id))
                    boundaries.append((member_index,child,boundary))
                    parts.append({"kind":"spread","source_value_id":source.value_id,"location":document.location(child)})
                    self.fact("ordered_object_spread", context, child, source_value_id=source.value_id, destination_value_id=result.value_id,
                        new_object_construction=True, not_same_object_overwrite=True)
                elif child.type in {"pair", "shorthand_property_identifier", "method_definition"}:
                    key_node = _field(child,"key") if child.type=="pair" else _field(child,"name") if child.type=="method_definition" else child
                    key = _name(document,key_node)
                    accessor = child.type == "method_definition" and any(item.type in {"get","set"} for item in child.children)
                    if key is None or key == "__proto__" or accessor:
                        state = self.effect(context,state,child,(result,),complete=False,reflection=True,reason="field_computed_proto_accessor_unknown")
                        state = ir.write_selected(state,result,None,self.unknown(context,child,"field_object_member_unknown"),self.evidence(context,child),model_supported=False)
                        parts.append({"kind":"unknown_member","location":document.location(child)})
                        continue
                    value_node = _field(child,"value") if child.type=="pair" else child
                    state, value = self.eval(context,state,value_node,expand=bool(key == self.sink.get("field_path",[""])[0]))
                    state = ir.write_selected(state,result,key,value,self.evidence(context,child,"literal_suffix_definition"),model_supported=supported,
                        model_guard=self.model_guards.get(context.context_id))
                    keys.append(key)
                    parts.append({"kind":"property","name":key,"location":document.location(child),"accessor":False})
                else:
                    state = self.effect(context,state,child,(result,),complete=False,reflection=True,reason="field_object_member_unknown")
            copy_witnesses = []
            for member_index,spread,boundary in boundaries:
                later = members[member_index+1:]
                later_keys = tuple(_name(document,_field(item,"key") if item.type=="pair" else _field(item,"name") if item.type=="method_definition" else item)
                    for item in later)
                suffix_complete = all(item.type in {"pair","shorthand_property_identifier","method_definition"}
                    and key not in {None,"__proto__"} and not (item.type=="method_definition" and any(token.type in {"get","set"} for token in item.children))
                    for item,key in zip(later,later_keys))
                suffix_refs = tuple(self.evidence(context,item,"literal_suffix_definition") for item in later)
                suffix_guard = ir.guard((self.evidence(context,node,"literal_suffix_source"),*suffix_refs),MODEL_ID,
                    capabilities=("ordered_data_definition_suffix",),supported=suffix_complete,
                    assumptions=("the complete recorded suffix of this actual object literal consists only of fixed data definitions with the recorded canonical keys",
                        "there is no later spread, computed key, accessor or prototype definition; value evaluation effects remain independently checked against the destination"))
                witness = ir.retain_copy_to_literal_end(state,boundary,self.evidence(context,node,"literal_copy_endpoint",proof=suffix_guard),
                    later_definition_keys=tuple(key for key in later_keys if key is not None),suffix_evidence=suffix_refs,
                    suffix_complete=suffix_complete,suffix_guard=suffix_guard)
                copy_witnesses.append({"spread_location":document.location(spread),"literal_location":document.location(node),
                    "selected_path_scope":"top-level own-enumerable slot only; nested referent contents remain unknown",
                    "analysis_phase":"literal expression before exposure and promise assimilation",
                    "antecedents":["this actual registered whole-surface copy completes normally", "selected current own-enumerable data slot exists at this copy"],
                    "conclusion":"that copy-time value/reference is retained at this literal endpoint" if witness.supported else "unknown",
                    "initial_parameter_origin_proven":False,"presence_proven":False,"runtime_value_verified":False,
                    "fulfilled_value_proven":False,"transport_proven":False,"witness":ir.to_data(witness)})
                self.fact("current_copy_boundary_retention",context,spread,witness=ir.to_data(witness),literal_location=document.location(node),
                    original_entry_origin_restored=False,source_projection_repaired=False)
            self.local_copy_witnesses[result.value_id] = copy_witnesses
            state = ir.finish_construction(state,result,self.evidence(context,node,"literal_materialization"))
            self.fact("new_literal_object_shape",context,node,actual_literal_keys=keys,parts=parts,
                allocation=ir.to_data(result.object_ref) if result.object_ref else None,
                construction_model_guard=ir.to_data(construction),construction_private_domain_released=True,
                whole_object_shape_closed=bool(ir.lookup_object(state,result) and ir.lookup_object(state,result).closed_shape),
                selected_field_closure_is_separate=True)
            return state,result
        if kind == "call_expression":
            return self.call(context,state,node,expand=expand)
        if kind == "await_expression":
            expression = unwrap(next(iter(_children(node)),None))
            state,value = self.eval(context,state,expression,expand=False)
            domain = ir.external_domain_supported(state,value)
            state = self.effect(context,state,node,(value,),complete=domain,reason="field_await_thenable_boundary")
            self.diagnostic("field_promise_or_iterator_boundary","未将await/thenable fulfillment当普通对象。",context,node)
            if domain:
                return self.bounded_external(context,state,node,"field_await_fulfilled_value_unknown",roots=(value,),
                    basis="already certified external operand domain; fulfillment/thenable contents and completion remain unknown, possible referents stay in that operand/capture/escaped domain")
            return state,self.unknown(context,node,"field_await_value_unknown",capture_unknown=True)
        if kind == "ternary_expression":
            state,condition = self.eval(context,state,_field(node,"condition"))
            truth = self.truth(state,condition)
            branches = [truth] if truth is not None else [True,False]
            results = [self.eval(self.guard(context,_field(node,"condition"),"then" if branch else "else"),state,
                _field(node,"consequence" if branch else "alternative"),expand=expand) for branch in branches]
            return ir.join_states(tuple(item[0] for item in results),evidence),ir.join_values(tuple(item[1] for item in results),evidence)
        if kind == "binary_expression":
            state,left = self.eval(context,state,_field(node,"left"))
            operator = document.text(_field(node,"operator"))
            if operator in {"||","&&","??"}:
                truth = self.truth(state,left)
                take = (truth is False) if operator=="||" and truth is not None else (truth is True) if operator=="&&" and truth is not None else (left.literal_kind in {"null","undefined"}) if operator=="??" and left.kind=="literal" and not left.barriers else None
                if take is False:
                    return state,left
                after,right = self.eval(self.guard(context,node,"rhs"),state,_field(node,"right"),expand=expand)
                return (after,right) if take is True else (ir.join_states((state,after),evidence),ir.join_values((left,right),evidence))
            state,right = self.eval(context,state,_field(node,"right"))
            if operator not in {"===", "!=="}:
                state=self.effect(context,state,node,(left,right),complete=True,reason="field_binary_conversion_effect_unknown")
            # These normal results are primitives, even when their content is
            # unknown. This does not confer a value on either input operand.
            if operator in {"===", "!==", "==", "!=", "<", ">", "<=", ">=", "instanceof", "in"}:
                return state,ir.value("scalar",evidence,literal_kind="boolean_unknown")
            return state,self.unknown(context,node,"field_binary_result_unknown")
        if kind == "unary_expression" and document.text(_field(node,"operator")) in {"typeof","!"}:
            state,value = self.eval(context,state,_field(node,"argument"))
            truth = self.truth(state,value)
            if document.text(_field(node,"operator"))=="!" and truth is not None:
                return state,ir.value("literal",evidence,literal_kind="false" if truth else "true")
            return state,ir.value("scalar",evidence,literal_kind="string_unknown" if document.text(_field(node,"operator"))=="typeof" else "boolean_unknown")
        if kind == "assignment_expression":
            lhs = unwrap(_field(node,"left"))
            receiver = None
            if lhs is not None and lhs.type in {"member_expression","subscript_expression"}:
                state,receiver = self.eval(context,state,_field(lhs,"object"))
                if _key(document,lhs) is None:
                    state = self.effect(context,state,lhs,(receiver,),complete=False,reflection=True,reason="field_write_computed_target_unknown")
            state,value = self.eval(context,state,_field(node,"right"),expand=expand)
            if lhs is not None and lhs.type=="identifier":
                key,_=self.key_for(context,lhs,state)
                if key is None:
                    state=self.effect(context,state,node,(value,),complete=False,reflection=True,reason="field_assignment_cell_unknown")
                elif key in state.immutable_bindings:
                    state=self.effect(context,state,node,(value,),complete=False,reflection=True,reason="field_const_assignment_completion_unknown")
                    self.diagnostic("field_const_assignment_completion_unknown","const写入不当作正常绑定更新。",context,node)
                    value=self.unknown(context,node,"field_const_assignment_completion_unknown",capture_unknown=True)
                else:
                    state=ir.bind(state,key,value,self.evidence(context,lhs))
                    if key.context_id.startswith("module:"):
                        state=self.effect(context,state,node,(value,),complete=True,reason="field_module_binding_escape",captured=(key,))
            elif receiver is not None:
                # Ordinary [[Set]] can invoke a setter/Proxy. Copy/Get models
                # authorize neither Set nor its possible side effects.
                state=self.effect(context,state,node,(receiver,value),complete=False,reason="field_ordinary_set_unmodeled")
            else:
                state = self.effect(context,state,node,(value,),complete=False,reflection=True,reason="field_write_target_unknown")
            return state,value
        # Unsupported syntax is an effect barrier, never skipped children.
        state = self.effect(context,state,node,(),complete=False,reflection=True,reason="field_expression_effect_unsupported")
        return state,self.unknown(context,node,"field_expression_unsupported",capture_unknown=True)

    def module_function(self, function: Any) -> bool:
        parent = function.parent
        while parent is not None:
            if parent.type in _FUNCTIONS | _CLASSES:
                return False
            parent = parent.parent
        return True

    def call(self, context: _Context, state: ir.State, node: Any, *, expand: bool) -> tuple[ir.State,ir.ValueRef]:
        document,definition,function = self.parts(context)
        callee_node = unwrap(_field(node,"function"))
        receiver = None
        if callee_node is not None and callee_node.type in {"member_expression","subscript_expression"}:
            state,receiver = self.eval(context,state,_field(callee_node,"object"))
            member_key = _key(document,callee_node)
            if member_key is None:
                state = self.effect(context,state,callee_node,(receiver,),complete=False,reflection=True,reason="field_dynamic_callee_unknown")
                callee = self.unknown(context,callee_node,"field_dynamic_callee_unknown",capture_unknown=True)
            else:
                state,callee = self.ordinary_get(context,state,receiver,member_key,callee_node)
        else:
            state,callee = self.eval(context,state,callee_node)
        argument_nodes = _children(_field(node,"arguments"))
        arguments = []
        for argument in argument_nodes:
            state,value = self.eval(context,state,argument,expand=expand)
            arguments.append(value)
        if context.handle_id == self.root_handle and self.sink.get("kind")=="call_argument" and _path(document,callee_node)==self.sink["callee"].split("."):
            self.observe(context,state,node,argument_nodes,tuple(arguments))
        edge,issues = self.sources.call_binding(node,document,definition)
        for issue in issues:
            self.diagnostic(issue.get("code","call_binding_unknown"),issue.get("message","callee binding未知"),context,node)
        target_doc,target_def,target_fn = None,None,None
        if edge is not None:
            nodes = self.sources.nodes.get(edge.target,[])
            if len(nodes)==1:
                target_doc,target_def,issues = self.sources.definition_for_node(nodes[0])
                target_fn = _function(target_def)
        captured = callee.captured_bindings
        target_module = target_fn is not None and self.module_function(target_fn)
        complete = bool(target_module or callee.kind=="callable" and not callee.capture_unknown
            or ir.external_domain_supported(state, callee))
        # The function value is itself an effect root: an opaque function may
        # reach its own aliases/captured cells even without a member receiver.
        roots = (callee,*tuple(arguments),*((receiver,) if receiver is not None else ()))
        # Imported/module-level functions cannot lexically capture caller-local
        # fresh allocations; this is a scope proof, never a purity assertion.
        if target_module:
            self.fact("authenticated_module_callee_capture_boundary",context,node,edge_id=edge.id,target_graph_node_id=edge.target,
                caller_local_capture_possible=False,actual_arguments_and_escaped_domain_still_effect_roots=True)
        if expand and edge is not None and target_fn is not None and len(self.stack)<_DEPTH and edge.target not in self.stack and not any(item.type=="spread_element" for item in argument_nodes):
            kind = function_kind(target_doc,target_fn)
            params = _children(_field(target_fn,"parameters"))
            simple = all(item.type in {"required_parameter","optional_parameter","identifier","object_pattern"} for item in params)
            if kind.get("ordinary") and not kind.get("async") and not callee.capture_unknown and simple and len(arguments)<=len(params):
                child_id = _digest((context.context_id,edge.id,tuple(value.value_id for value in arguments),self.models))[:24]
                child = self.context(target_doc,target_def,child_id,captures=callee.captured_bindings)
                self.audit(child,target_fn)
                self.active_contexts.append(child)
                for index,parameter in enumerate(params):
                    value = arguments[index] if index<len(arguments) else ir.value("literal",self.evidence(child,parameter),literal_kind="undefined")
                    state = self.bind_pattern(child,state,parameter,value)
                    self.fact("actual_call_argument_formal_mapping",context,node,edge_id=edge.id,target_graph_node_id=edge.target,
                        parameter_index=index,argument_value_id=value.value_id,formal_location=target_doc.location(parameter),callee_context=child_id)
                self.stack.append(edge.target)
                returned,active = self.execute(child,state,_field(target_fn,"body"),root=False)
                self.stack.pop()
                self.active_contexts.pop()
                if returned and not active:
                    state = ir.join_states(tuple(item.state for item in returned),self.evidence(context,node,"normal_return_join"))
                    value = ir.join_values(tuple(item.value for item in returned),self.evidence(context,node,"normal_return_join"))
                    projection = self.projection(context,state,value,tuple(self.sink.get("field_path",())),node)
                    self.fact("actual_helper_selected_return_summary",context,node,edge_id=edge.id,target_graph_node_id=edge.target,
                        selected_field_path=self.sink.get("field_path",[]),normal_return_count=len(returned),incomplete_or_fallthrough=False,
                        selected_field_presence=projection.presence,selected_field_shape_closed=projection.closed,whole_object_shape_closed=projection.whole_closed,
                        normal_prefix_effects_unknown=bool(state.effects),invocation_or_completion_proven=False)
                    return state,value
            self.diagnostic("field_helper_completion_or_parameters_unknown","async/generator/default-rest/未闭合helper不解释为普通返回对象。",context,node)
        elif expand and edge is not None and (len(self.stack)>=_DEPTH or edge.target in self.stack):
            self.incomplete=True
            self.diagnostic("field_helper_recursion_budget","递归/深度未闭合；不把截断当缺字段。",context,node)
        if callee_node is not None and callee_node.type=="identifier" and document.text(callee_node)=="eval" and self.lexical(document).unbound("eval",callee_node).get("unbound"):
            state=self.effect(context,state,node,roots,complete=False,reflection=True,reason="field_direct_eval_unmodeled")
            return state,self.unknown(context,node,"field_direct_eval_value_unknown",capture_unknown=True)
        state = self.effect(context,state,node,roots,complete=complete,reason="field_opaque_call_effects_unknown",captured=captured)
        if complete:
            return self.bounded_external(context,state,node,"field_opaque_call_result_unknown",roots=roots,
                basis="authenticated module-level target or actual complete lexical callable captures; evaluated arguments and exposed/captured domain bound possible returned referents")
        return state,self.unknown(context,node,"field_opaque_call_result_unknown",capture_unknown=True)

    def effects(self,state:ir.State)->dict:
        records = [ir.to_data(effect) for effect in state.effects]
        return {"effect_barriers":records[:24],"effect_barrier_count":len(records),"effect_barriers_truncated":len(records)>24,
            "effect_barrier_sample_limit":24,"effect_evidence_snapshot_id":self.snapshot.id,
            "full_effect_evidence_source":"shared immutable IR distinct effects over authenticated source contexts"}

    def assessment(self,context:_Context,state:ir.State,node:Any,projection:ir.Projection,*,edge_id:str|None=None,formal:dict|None=None,
        operand:ir.ValueRef|None=None,operand_node:Any=None)->dict:
        document,definition,function = self.parts(context)
        refs = projection.value.provenance
        origins = [{"kind":ref.kind,"binding_id":ref.binding.declaration_id if ref.binding else None,
            "binding_context":ref.binding.context_id if ref.binding else None,"parameter_index":ref.parameter_index,
            "field_path":list(ref.field_path),"evidence":ir.to_data(ref.evidence),"presence_or_runtime_value_proven":False} for ref in refs]
        matching = [ref for ref in refs if ref.binding==self.source_binding and ref.field_path==self.source_path]
        relation = "selected_field_absent" if projection.closed and projection.presence=="absent" else "source_form_preserved_when_present" if projection.closed and not projection.value.barriers and refs and len(matching)==len(refs) else "unknown"
        completion = function_kind(document,function)
        pre_completion = relation
        if node.type=="return_statement" and completion.get("async"):
            relation="unknown"
            self.diagnostic("field_async_return_assimilation_unknown","body返回源式不是Promise fulfilled值。",context,node)
        copies = []
        expression = unwrap(operand_node)
        if operand is not None and expression is not None and expression.type=="object":
            copies = [item for item in self.local_copy_witnesses.get(operand.value_id,[])
                if item["literal_location"]["start_byte"]==expression.start_byte and item["literal_location"]["end_byte"]==expression.end_byte]
        branch_conditions = [self.guards[key] for key in context.conditions if key in self.guards]
        source_relations = collect_site_relations(self.sources,document,definition,self.lexical(document),node,
            subject_parameter=self.subject_identity,sink=self.sink,field_path=list(self.source_path),
            branch_conditions=branch_conditions)
        return {"site_location":document.location(node),"call_context":context.context_id,
            "branch_conditions":branch_conditions,
            "field_presence":projection.presence,"selected_field_shape_closed":projection.closed,
            "whole_object_shape_closed":projection.whole_closed,"field_sources":origins,"source_form_relation":relation,
            "pre_completion_source_form_relation":pre_completion,"copy_steps":[ir.to_data(item) for item in projection.observations],
            "ir_selected_value":ir.to_data(projection.value),"edge_id":edge_id,"formal":formal,"completion":completion,
            "analysis_phase":"body return expression before promise assimilation" if node.type=="return_statement" else "call argument before callee activation",
            "local_copy_retention":copies,
            "local_copy_retention_supported":any(item["witness"]["supported"] for item in copies),
            "source_relations":source_relations,
            **self.effects(state),"reaching_value_origin_proven":False,"opaque_effects_or_exceptions_excluded":False,
            "runtime_value_verified":False,"conditions":["selected site reached on normal prefix","entire copy-source own-enumerable data surfaces obey registered conditional model; no recursive child plainness assumed",
                *(["each separately guarded actual Get resolves an own data property or getter-free missing read; it does not certify child surfaces"] if READ_MODEL_ID in self.models else [])],
            "gaps":list(projection.barriers)}

    def observe(self,context:_Context,state:ir.State,call:Any,argument_nodes:list[Any],arguments:tuple[ir.ValueRef,...])->None:
        document,definition,_ = self.parts(context)
        edge,issues = self.sources.call_binding(call,document,definition)
        index=self.sink["argument_index"]
        formal=None
        if edge is not None and index<len(arguments) and not any(node.type=="spread_element" for node in argument_nodes[:index+1]):
            projection = self.projection(context,state,arguments[index],tuple(self.sink["field_path"]),argument_nodes[index])
            nodes=self.sources.nodes.get(edge.target,[])
            target_doc,target_def,_=self.sources.definition_for_node(nodes[0]) if len(nodes)==1 else (None,None,[])
            target_fn=_function(target_def)
            params=_children(_field(target_fn,"parameters"))
            if target_doc is not None and index<len(params):
                formal={"target_graph_node_id":edge.target,"parameter_index":index,"location":target_doc.location(params[index]),
                    "callee_function_kind":function_kind(target_doc,target_fn),"argument_value_id":arguments[index].value_id}
        else:
            projection=ir.Projection("unknown",self.unknown(context,call,"field_selected_argument_or_binding_unknown"),False,False)
        if formal is None:
            projection=ir.Projection(projection.presence,projection.value,False,projection.whole_closed,projection.observations,(*projection.barriers,"field_selected_formal_unknown"))
        self.assessments.append(self.assessment(context,state,call,projection,edge_id=edge.id if edge else None,formal=formal,
            operand=arguments[index] if index<len(arguments) else None,operand_node=argument_nodes[index] if index<len(argument_nodes) else None))

    def execute(self,context:_Context,state:ir.State,statement:Any,*,root:bool)->tuple[list[_Returned],list[tuple[_Context,ir.State]]]:
        if statement is None:
            return [],[(context,state)]
        if not self.tick():
            return [],[(context,self.effect(context,state,statement,(),complete=False,reflection=True,reason="field_execution_budget"))]
        document,_,function=self.parts(context)
        kind=statement.type
        if kind=="statement_block":
            returned=[]
            active=[(context,state)]
            for child in _children(statement):
                if child.type in _FUNCTIONS:
                    continue
                next_active=[]
                for current,current_state in active:
                    result,remaining=self.execute(current,current_state,child,root=root)
                    returned.extend(result);next_active.extend(remaining)
                active=next_active
                if len(active)>_BRANCHES:
                    self.incomplete=True
                    state=ir.join_states(tuple(item[1] for item in active),self.evidence(context,child,"branch_budget"))
                    state=self.effect(context,state,child,(),complete=False,reflection=True,reason="field_branch_budget")
                    active=[(context,state)]
                if not active or root and self.sink.get("kind")=="call_argument" and self.all_accounted():
                    break
            return returned,active
        if kind in {"lexical_declaration","variable_declaration"}:
            for declaration in _children(statement):
                if declaration.type=="variable_declarator":
                    state,value=self.eval(context,state,_field(declaration,"value"),expand=True)
                    state=self.bind_pattern(context,state,_field(declaration,"name"),value)
            return [],[(context,state)]
        if kind=="expression_statement":
            state,_=self.eval(context,state,next(iter(_children(statement)),None))
            return [],[(context,state)]
        if kind=="return_statement":
            state,value=self.eval(context,state,next(iter(_children(statement)),None),expand=True)
            self.normal_returns.append({"location":document.location(statement),"graph_node_id":document.call_owner(statement),
                "context":context.context_id,"value_id":value.value_id,"function_kind":function_kind(document,function),
                "body_return_expression_only":True,"fulfilled_value_proven":False,**self.effects(state)})
            if root and self.sink.get("kind")=="return":
                projection=self.projection(context,state,value,tuple(self.sink["field_path"]),statement)
                self.assessments.append(self.assessment(context,state,statement,projection,operand=value,operand_node=next(iter(_children(statement)),None)))
            return [_Returned(context,state,statement,value)],[]
        if kind=="throw_statement":
            state,_=self.eval(context,state,next(iter(_children(statement)),None))
            self.abrupt.append({"location":document.location(statement),"kind":"explicit_body_throw","conditions":[self.guards[key] for key in context.conditions if key in self.guards]})
            return [],[]
        if kind=="if_statement":
            state,value=self.eval(context,state,_field(statement,"condition"))
            truth=self.truth(state,value)
            results=[];active=[]
            for branch in ([truth] if truth is not None else [True,False]):
                selected=self.guard(context,_field(statement,"condition"),"then" if branch else "else")
                result,remaining=self.execute(selected,state,_field(statement,"consequence" if branch else "alternative"),root=root)
                results.extend(result);active.extend(remaining)
            return results,active
        if kind=="else_clause":
            return self.execute(context,state,next(iter(_children(statement)),None),root=root)
        state=self.effect(context,state,statement,(),complete=False,reflection=True,reason="field_control_effect_unsupported")
        return [],[(context,state)]

    def all_accounted(self)->bool:
        seen={(item["site_location"]["start_byte"],item["site_location"]["end_byte"]) for item in self.assessments}
        return bool(self.site_nodes and all((node.start_byte,node.end_byte) in seen for node in self.site_nodes))

    def summarize(self,selector:dict,*,parameter_index:int,field_path:list[str],sink:dict)->dict:
        self.sink=sink
        result={"version":VERSION,"snapshot_id":self.snapshot.id,"source_hash":self.snapshot.source_hash,"selector":selector,
            "parameter_index":parameter_index,"field_path":field_path,"sink":sink,
            "models":[{"id":MODEL_ID,"authority":"explicit conditional trusted language/data model","semantics":"entire source own-enumerable ordinary data copy surface; shallow referent identity retained",
                "runtime_objects_getters_proxies_verified":False,"source_reference":"https://tc39.es/ecma262/#sec-copydataproperties"}],
            "source_assumptions":["selected parameter supplied on the provided-value branch","each modeled copy source has an entire ordinary own-enumerable data surface, without Proxy or other getter enumeration effects; child referents are not certified"],
            "assessments":[],"source_facts":[],"normal_returns":[],"abrupt_or_exception_boundaries":[],"analysis_gaps":[],
            "source_complete":False,"all_selected_sites_accounted":False,"runtime_value_verified":False,"transport_proven":False,"full_functionality_proven":False,
            "component_versions":{"semantic_sources":SOURCE_VERSION,"lexical_bindings":LEXICAL_VERSION,"builtin_environment":ENVIRONMENT_VERSION,"completion_summaries":COMPLETION_VERSION,"semantic_ir":ir.VERSION,"field_relations":RELATIONS_VERSION}}
        if READ_MODEL_ID in self.models:
            result["models"].append({"id":READ_MODEL_ID,"authority":"separately registered conditional actual-Get model",
                "semantics":"existing data-source ObjectVersion only: selected key resolves own data if present; a missing own key yields undefined without prototype/accessor/Proxy effects",
                "runtime_read_verified":False,"recursive_child_plainness_inferred":False})
            result["source_assumptions"].append("each recorded actual Get additionally satisfies its separate nonrecursive own-data/getter-free-missing-read premise")
        document,definition,issues=self.sources.select(selector)
        function=_function(definition)
        for issue in issues:
            self.diagnostics[_digest(issue)[:24]]=issue
        if not ir.PROTOCOL_READY:
            self.diagnostic("field_ir_protocol_not_ready","IR仍为开发协议，不发布源式闭合结果。")
        elif document is None or function is None or document.kind not in {"typescript","tsx"} or self.models not in ([MODEL_ID],[MODEL_ID,READ_MODEL_ID]):
            self.diagnostic("field_subject_source_or_model_unknown","主体或固定模型未认证。")
        else:
            kind=function_kind(document,function)
            parameters=_children(_field(function,"parameters"))
            context_id=_digest((self.snapshot.id,definition.graph_node_id,parameter_index,field_path,sink,self.models))[:24]
            context=self.context(document,definition,context_id)
            self.root_handle=context.handle_id
            if not kind.get("ordinary") or parameter_index>=len(parameters):
                self.diagnostic("field_subject_parameter_or_kind_unknown","所选形参缺失/generator不能补完整来源。",context,function)
            else:
                selected=parameters[parameter_index]
                binder=_field(selected,"pattern") or _field(selected,"name") or selected
                identity=self.lexical(document).resolve(binder)
                if identity.get("state")!="unique" or binder.type!="identifier":
                    self.diagnostic("field_subject_parameter_identity_unknown","主体selected形参不是唯一简单声明。",context,selected)
                else:
                    self.source_binding=ir.BindingKey(identity["declaration_id"],context_id)
                    self.subject_identity=identity
                    self.source_path=tuple(field_path)
                    self.active_contexts.append(context)
                    result.update(subject_parameter=identity,subject_function_kind=kind,subject_graph_node_id=definition.graph_node_id)
                    state=ir.initial_state()
                    supported=self.audit(context,function)
                    for index,parameter in enumerate(parameters):
                        parameter_binder=_field(parameter,"pattern") or _field(parameter,"name") or parameter
                        parameter_identity=self.lexical(document).resolve(parameter_binder) if parameter_binder.type=="identifier" else {"state":"unknown"}
                        binding=ir.BindingKey(parameter_identity.get("declaration_id","unknown:"+str(index)),context_id)
                        origin=ir.ProvenanceRef("parameter_field_reference",self.evidence(context,parameter),binding,index,())
                        state,value=ir.allocate(state,self.evidence(context,parameter),context_id=context_id,closed_shape=False,fresh=False,
                            external_aliasable=True,origin=origin,model_supported=supported,allocation_tag="parameter:"+str(index),
                            model_guard=self.model_guards.get(context.context_id))
                        state=self.bind_pattern(context,state,parameter,value,provided=index==parameter_index)
                    self.site_nodes=tuple(node for node in _direct(_field(function,"body")) if node.type=="call_expression" and _path(document,_field(node,"function"))==sink.get("callee","").split(".")) if sink["kind"]=="call_argument" else tuple(node for node in _direct(_field(function,"body")) if node.type=="return_statement")
                    returned,active=self.execute(context,state,_field(function,"body"),root=True)
                    self.active_contexts.pop()
                    self.incomplete = self.incomplete or any(item.state.incomplete for item in returned) or any(item[1].incomplete for item in active)
                    result["selected_site_count"]=len(self.site_nodes)
                    result["all_selected_sites_accounted"]=self.all_accounted()
                    if not result["all_selected_sites_accounted"]:
                        self.diagnostic("field_selected_sites_unaccounted","所有选定源码call/return必须被独立评估；空/遗漏不作通过。",context,function)
                    if active and sink["kind"]=="return":
                        self.return_fallthrough=True
                        self.diagnostic("field_return_fallthrough_unknown","存在非返回路径，不能称完整normal返回集合。",context,function)
        result.update(assessments=self.assessments,source_facts=list(self.facts.values()),normal_returns=self.normal_returns,
            abrupt_or_exception_boundaries=self.abrupt,analysis_gaps=[*self.diagnostics.values(),_issue("field_runtime_and_transport_unknown","源式摘要不认证运行值、整个pipeline/消息/跨进程或目标激活。")],
            summary_budget={"operations":self.operations,"limit":_LIMIT,"incomplete":self.incomplete},
            captured_sources=[{"file":path,"hash":doc.source.hash,"parse_id":doc.parse_id} for path,(doc,_) in sorted(self.sources.cache.items()) if doc is not None])
        result["selected_shape_complete"]=bool(result["all_selected_sites_accounted"] and not self.return_fallthrough and not self.incomplete and self.assessments and all(item["selected_field_shape_closed"] for item in self.assessments))
        result["source_form_complete"]=bool(result["selected_shape_complete"] and all(item["source_form_relation"]!="unknown" for item in self.assessments))
        result["source_complete"]=result["source_form_complete"]
        return result


def summarize_field(snapshot:GraphSnapshot,selector:dict,*,parameter_index:int,field_path:list[str],sink:dict,models:list[str])->dict:
    return FieldSummaryBuilder(snapshot,models).summarize(selector,parameter_index=parameter_index,field_path=field_path,sink=sink)
