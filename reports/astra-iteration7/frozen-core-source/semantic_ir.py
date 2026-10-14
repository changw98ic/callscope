"""Finite immutable source-state IR, not a JavaScript evaluator.

Object values identify allocations.  Content versions and copy observations
are separate: an immutable IR record does not freeze the referenced heap.
All public records contain only scalars, tuples and other IR records.  ASTs,
caller frames, mutable containers and Python object identities are excluded.

Model guards link declared finite capabilities to captured source evidence.
The IR checks that linkage; it does not authenticate a running heap or prove
the language/model premises supplied by the source adapter.
"""

from __future__ import annotations

from dataclasses import dataclass, fields, replace
import hashlib
import json
from typing import Literal

VERSION = "finite-immutable-semantic-ir-2"
PROTOCOL_READY = True


class _Record:
    __slots__ = ()

    def __post_init__(self) -> None:
        for item in fields(self):
            _immutable(getattr(self, item.name))
        if type(self).__name__ in {"FieldSlot", "Projection"} and self.presence not in {"present", "absent", "unknown", "maybe"}:
            raise ValueError("Unknown IR field-presence domain")
        if type(self).__name__ == "Limits" and any(getattr(self, item.name) <= 0 for item in fields(self)):
            raise ValueError("IR limits must be positive")
        if type(self).__name__ == "State":
            if len({obj.alloc_id for obj in self.objects}) != len(self.objects) or len({key for key, _ref in self.bindings}) != len(self.bindings):
                raise ValueError("State allocations and binding cells must be unique")


def _immutable(value: object) -> None:
    if value is None or type(value) in {str, int, bool}:
        return
    if type(value) is tuple:
        for item in value:
            _immutable(item)
        return
    if isinstance(value, _Record):
        if (type(value).__module__ != __name__ or not type(value).__dataclass_params__.frozen
                or hasattr(value, "__dict__")):
            raise TypeError("IR nesting requires a frozen slotted IR record")
        for item in fields(value):
            _immutable(getattr(value, item.name))
        return
    raise TypeError("Semantic IR accepts only immutable scalar/tuple/IR records")


def _data(value: object) -> object:
    if isinstance(value, _Record):
        return {"record": type(value).__name__, **{item.name: _data(getattr(value, item.name)) for item in fields(value)}}
    if type(value) is tuple:
        return [_data(item) for item in value]
    _immutable(value)
    return value


def _digest(value: object) -> str:
    return hashlib.sha256(json.dumps(_data(value), sort_keys=True, ensure_ascii=True,
        separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class EvidenceRef(_Record):
    evidence_id: str
    file: str
    source_hash: str
    start_byte: int
    end_byte: int
    model_id: str
    guard_ids: tuple[str, ...] = ()
    snapshot_id: str = ""
    context_id: str = ""
    kind: str = "source"


@dataclass(frozen=True, slots=True)
class ModelGuard(_Record):
    guard_id: str
    model_id: str
    evidence: tuple[EvidenceRef, ...]
    capabilities: tuple[str, ...]
    supported: bool = False
    assumptions: tuple[str, ...] = ()
    runtime_verified: bool = False


@dataclass(frozen=True, slots=True)
class BindingKey(_Record):
    declaration_id: str
    context_id: str = ""


@dataclass(frozen=True, slots=True)
class BindingDomain(_Record):
    binding: BindingKey
    guard: ModelGuard
    evidence: EvidenceRef


@dataclass(frozen=True, slots=True)
class ObjectRef(_Record):
    alloc_id: str


@dataclass(frozen=True, slots=True)
class ProvenanceRef(_Record):
    kind: str
    evidence: EvidenceRef
    binding: BindingKey | None = None
    parameter_index: int | None = None
    field_path: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ValueRef(_Record):
    value_id: str
    kind: str
    evidence: tuple[EvidenceRef, ...] = ()
    object_ref: ObjectRef | None = None
    provenance: tuple[ProvenanceRef, ...] = ()
    literal_kind: str = ""
    source_text: str = ""
    alternatives: tuple[ValueRef, ...] = ()
    alias_roots: tuple[ObjectRef, ...] = ()
    external_alias: bool = False
    capture_unknown: bool = False
    captured_bindings: tuple[BindingKey, ...] = ()
    barriers: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ObservationRef(_Record):
    observation_id: str
    evidence: EvidenceRef
    alloc_id: str
    version_id: str
    key: str
    captured_value_id: str
    presence: str


@dataclass(frozen=True, slots=True)
class FieldSlot(_Record):
    key: str
    presence: Literal["present", "absent", "unknown", "maybe"]
    value: ValueRef
    closed: bool
    observations: tuple[ObservationRef, ...] = ()
    evidence: tuple[EvidenceRef, ...] = ()
    barriers: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class CopyLayer(_Record):
    source_snapshot: ObjectVersion
    evidence: EvidenceRef
    excluded_keys: tuple[str, ...] = ()
    exclusions_closed: bool = True


@dataclass(frozen=True, slots=True)
class ObjectVersion(_Record):
    alloc_id: str
    version_id: str
    slots: tuple[FieldSlot, ...]
    closed_shape: bool
    model_supported: bool
    fresh: bool
    escaped: bool
    external_aliasable: bool
    origin: ProvenanceRef | None = None
    evidence: tuple[EvidenceRef, ...] = ()
    barriers: tuple[str, ...] = ()
    conditional_allocation: bool = False
    base_closed_shape: bool = True
    copy_layers: tuple[CopyLayer, ...] = ()
    guards: tuple[ModelGuard, ...] = ()
    construction_guard: ModelGuard | None = None


@dataclass(frozen=True, slots=True)
class EffectRef(_Record):
    effect_id: str
    evidence: EvidenceRef
    reason: str
    root_allocations: tuple[str, ...]
    affected_allocations: tuple[str, ...]
    protected_fresh_allocations: tuple[str, ...]
    roots_complete: bool
    captures_complete: bool
    include_escaped: bool
    reflection: bool
    budget_exceeded: bool = False
    runtime_effect_verified: bool = False
    visible_scope_restricted: bool = False
    visible_root_allocations: tuple[str, ...] = ()
    guard: ModelGuard | None = None
    reachability_edges: tuple[tuple[str, str, str], ...] = ()


@dataclass(frozen=True, slots=True)
class Limits(_Record):
    max_objects: int = 1024
    max_slots: int = 4096
    max_steps: int = 4096
    max_reachable: int = 4096
    max_alternatives: int = 32
    max_copy_depth: int = 16


@dataclass(frozen=True, slots=True)
class State(_Record):
    bindings: tuple[tuple[BindingKey, ValueRef], ...] = ()
    objects: tuple[ObjectVersion, ...] = ()
    effects: tuple[EffectRef, ...] = ()
    escaped_bindings: tuple[BindingKey, ...] = ()
    unknown_captures_escaped: bool = False
    barriers: tuple[str, ...] = ()
    steps: int = 0
    limits: Limits = Limits()
    incomplete: bool = False
    guards: tuple[ModelGuard, ...] = ()
    immutable_bindings: tuple[BindingKey, ...] = ()
    external_binding_domains: tuple[BindingDomain, ...] = ()


@dataclass(frozen=True, slots=True)
class Projection(_Record):
    presence: Literal["present", "absent", "unknown", "maybe"]
    value: ValueRef
    closed: bool
    whole_closed: bool
    observations: tuple[ObservationRef, ...] = ()
    barriers: tuple[str, ...] = ()


def evidence(file: str, source_hash: str, start_byte: int, end_byte: int,
    model_id: str, *, guard_ids: tuple[str, ...] = (), snapshot_id: str = "",
    context_id: str = "", kind: str = "source") -> EvidenceRef:
    identity = (VERSION, file, source_hash, start_byte, end_byte, model_id,
        tuple(sorted(set(guard_ids))), snapshot_id, context_id, kind)
    return EvidenceRef(_digest(identity), file, source_hash, start_byte, end_byte,
        model_id, identity[6], snapshot_id, context_id, kind)


def value(kind: str, evidence_ref: EvidenceRef, *, object_ref: ObjectRef | None = None,
    provenance: tuple[ProvenanceRef, ...] = (), literal_kind: str = "", source_text: str = "",
    alternatives: tuple[ValueRef, ...] = (), alias_roots: tuple[ObjectRef, ...] = (),
    external_alias: bool = False, capture_unknown: bool = False,
    captured_bindings: tuple[BindingKey, ...] = (), barriers: tuple[str, ...] = ()) -> ValueRef:
    record = ValueRef("", kind, (evidence_ref,), object_ref, provenance, literal_kind,
        source_text, alternatives, alias_roots, external_alias, capture_unknown,
        captured_bindings, tuple(sorted(set(barriers))))
    return ValueRef(_digest(record), *tuple(getattr(record, item.name) for item in fields(record))[1:])


def initial_state(*, limits: Limits = Limits()) -> State:
    return State(limits=limits)


def guard(evidence_refs: tuple[EvidenceRef, ...], model_id: str, *, capabilities: tuple[str, ...],
    supported: bool = False, assumptions: tuple[str, ...] = ()) -> ModelGuard:
    record = ModelGuard("", model_id, evidence_refs, tuple(sorted(set(capabilities))), supported, assumptions)
    return replace(record, guard_id=_digest(record))


def register_guard(state: State, proof: ModelGuard) -> State:
    """Store a declared source-model proof without inventing an effect."""
    return replace(_step(state), guards=_unique((*state.guards, proof)))


def _supported(proof: ModelGuard | None, at: EvidenceRef, capability: str) -> bool:
    return bool(proof and proof.supported and proof.model_id == at.model_id
        and proof.guard_id in at.guard_ids and capability in proof.capabilities
        and proof.evidence and proof.assumptions
        and all(item.model_id == proof.model_id and len(item.source_hash) == 64
            and all(char in "0123456789abcdef" for char in item.source_hash)
            and 0 <= item.start_byte <= item.end_byte and item.file
            and (not at.snapshot_id or item.snapshot_id == at.snapshot_id) for item in proof.evidence))


def supports_guard(proof: ModelGuard | None, at: EvidenceRef, capability: str) -> bool:
    """Check source/model linkage, not runtime truth or language semantics."""
    return _supported(proof, at, capability)


def _key(binding: BindingKey | str) -> BindingKey:
    return binding if isinstance(binding, BindingKey) else BindingKey(binding)


def _unique(records: tuple) -> tuple:
    return tuple(record for _identity, record in sorted({_digest(record): record for record in records}.items()))


def _budget(state: State, reason: str) -> State:
    return replace(state, incomplete=True, barriers=tuple(sorted({*state.barriers, reason})))


def _step(state: State) -> State:
    advanced = replace(state, steps=state.steps + 1)
    return _budget(advanced, "ir_step_budget_exceeded") if state.incomplete or advanced.steps > state.limits.max_steps else advanced


def _unknown(at: EvidenceRef, reason: str) -> ValueRef:
    return value("unknown", at, capture_unknown=True, barriers=(reason,))


def _object_version(record: ObjectVersion) -> ObjectVersion:
    return replace(record, version_id=_digest(replace(record, version_id="")))


def _put(state: State, record: ObjectVersion) -> State:
    objects = {item.alloc_id: item for item in state.objects}
    objects[record.alloc_id] = _object_version(record)
    result = replace(state, objects=tuple(objects[key] for key in sorted(objects)))
    if len(result.objects) > state.limits.max_objects or sum(len(item.slots) for item in result.objects) > state.limits.max_slots:
        return _budget(result, "ir_object_or_slot_budget_exceeded")
    return result


def _observation(at: EvidenceRef, obj: ObjectVersion, key: str, ref: ValueRef, presence: str) -> ObservationRef:
    record = ObservationRef("", at, obj.alloc_id, obj.version_id, key, ref.value_id, presence)
    return replace(record, observation_id=_digest(record))


def _failure(at: EvidenceRef, reason: str) -> Projection:
    return Projection("unknown", _unknown(at, reason), False, False, barriers=(reason,))


def _overlay(previous: Projection, copied: Projection, at: EvidenceRef, limit: int) -> Projection:
    if copied.presence == "absent" and copied.closed:
        return replace(previous, observations=_unique((*previous.observations, *copied.observations)))
    if copied.presence == "present":
        return copied
    if previous.presence == "absent" and previous.closed:
        return copied
    refs = tuple(item.value for item in (previous, copied) if item.presence != "absent")
    return Projection("present" if previous.presence == "present" else "maybe",
        join_values(refs, at, max_alternatives=limit), previous.closed and copied.closed,
        previous.whole_closed and copied.whole_closed,
        _unique((*previous.observations, *copied.observations)),
        tuple(sorted({*previous.barriers, *copied.barriers})))


def _project_version(state: State, obj: ObjectVersion, key: str, at: EvidenceRef, depth: int = 0) -> Projection:
    if depth > state.limits.max_copy_depth:
        return _failure(at, "ir_copy_projection_depth_exceeded")
    if obj.conditional_allocation:
        return _failure(at, "ir_conditional_allocation_not_refined")
    whole = obj.closed_shape and obj.model_supported and not obj.barriers
    slot = next((slot for slot in obj.slots if slot.key == key), None)
    if slot is not None:
        return Projection(slot.presence, slot.value, slot.closed and not slot.barriers, whole,
            slot.observations, slot.barriers)
    if obj.barriers or not obj.model_supported:
        return _failure(at, obj.barriers[0] if obj.barriers else "ir_own_data_model_not_certified")
    if obj.origin is not None:
        origin = replace(obj.origin, field_path=(*obj.origin.field_path, key))
        ref = value("symbolic", at, provenance=(origin,), alias_roots=(ObjectRef(obj.alloc_id),), external_alias=True)
        selected = Projection("unknown", ref, True, False)
    elif obj.base_closed_shape:
        selected = Projection("absent", value("absent", at), True, whole)
    else:
        selected = _failure(at, "ir_open_own_shape_without_origin")
    for layer in obj.copy_layers:
        if not layer.exclusions_closed:
            selected = _failure(at, "ir_copy_exclusions_unknown")
            continue
        if key in layer.excluded_keys:
            continue
        copied = _project_version(state, layer.source_snapshot, key, layer.evidence, depth + 1)
        captured = _observation(layer.evidence, layer.source_snapshot, key, copied.value, copied.presence)
        copied = replace(copied, observations=_unique((*copied.observations, captured)), whole_closed=False)
        selected = _overlay(selected, copied, layer.evidence, state.limits.max_alternatives)
    return replace(selected, whole_closed=whole)


def _copy_depth(obj: ObjectVersion, limit: int) -> int:
    pending, greatest = [(obj, 0)], 0
    seen: set[tuple[str, str]] = set()
    while pending:
        item, depth = pending.pop()
        if (item.alloc_id, item.version_id) in seen:
            continue
        seen.add((item.alloc_id, item.version_id))
        greatest = max(greatest, depth)
        if depth > limit:
            return depth
        pending.extend((layer.source_snapshot, depth + 1) for layer in item.copy_layers)
    return greatest


def allocate(state: State, evidence_ref: EvidenceRef, *, context_id: str,
    slots: tuple[FieldSlot, ...] = (), closed_shape: bool = True, fresh: bool = True,
    external_aliasable: bool = False, origin: ProvenanceRef | None = None,
    model_supported: bool = False, allocation_tag: str = "literal",
    model_guard: ModelGuard | None = None,
    construction_guard: ModelGuard | None = None) -> tuple[State, ValueRef]:
    _immutable(slots)
    state = _step(state)
    if state.incomplete:
        return state, _unknown(evidence_ref, "ir_allocation_budget_exceeded")
    alloc_id = _digest((VERSION, "allocation", evidence_ref, context_id, allocation_tag))
    old = next((item for item in state.objects if item.alloc_id == alloc_id), None)
    if old is not None:
        reused = replace(old, fresh=False, escaped=True, closed_shape=False, model_supported=False,
            construction_guard=None,
            slots=tuple(replace(slot, closed=False,
                barriers=tuple(sorted({*slot.barriers, "ir_allocation_context_reused"}))) for slot in old.slots),
            barriers=tuple(sorted({*old.barriers, "ir_allocation_context_reused"})))
        return _put(state, reused), value("object", evidence_ref, object_ref=ObjectRef(alloc_id),
            barriers=("ir_allocation_context_reused",))
    certified = model_supported and _supported(model_guard, evidence_ref, "own_data_shape")
    keys = [slot.key for slot in slots]
    duplicates = len(keys) != len(set(keys))
    reasons = ("ir_duplicate_slot_not_ordered",) if duplicates else ()
    if not certified:
        reasons = (*reasons, "ir_own_data_model_not_certified")
    unique_slots = {slot.key: slot for slot in slots}
    checked_slots = tuple(replace(unique_slots[key], closed=False,
        barriers=tuple(sorted({*unique_slots[key].barriers, *reasons}))) if reasons else unique_slots[key] for key in sorted(unique_slots))
    private = bool(certified and fresh and not external_aliasable
        and _supported(construction_guard, evidence_ref, "private_literal_construction"))
    obj = ObjectVersion(alloc_id, "", checked_slots, closed_shape and not duplicates,
        certified, fresh and certified and not external_aliasable, not fresh or external_aliasable or not certified,
        external_aliasable or not fresh or not certified, origin, (evidence_ref,), reasons,
        base_closed_shape=closed_shape, guards=(model_guard,) if model_guard else (),
        construction_guard=construction_guard if private else None)
    new_state = _put(state, obj)
    ref = value("object", evidence_ref, object_ref=ObjectRef(alloc_id))
    return (new_state, _unknown(evidence_ref, "ir_allocation_budget_exceeded")) if new_state.incomplete else (new_state, ref)


def finish_construction(state: State, ref: ValueRef, evidence_ref: EvidenceRef) -> State:
    """Release the allocation-specific temporary domain before exposure/bind.

    The source adapter certifies the literal lifetime, not its runtime success.
    Existing shape damage is retained; finishing cannot restore lost slots.
    """
    state = _step(state)
    if ref.kind == "join":
        for child in ref.alternatives:
            state = finish_construction(state,child,evidence_ref)
        return state
    obj = lookup_object(state, ref)
    return _put(state, replace(obj, construction_guard=None,
        evidence=_unique((*obj.evidence, evidence_ref)))) if obj is not None else state


def _private_constructions(state: State, reached: set[str]) -> set[str]:
    return {obj.alloc_id for obj in state.objects if obj.alloc_id not in reached
        and obj.fresh and not obj.escaped and not obj.external_aliasable
        and not obj.conditional_allocation
        and obj.construction_guard is not None
        and any(_supported(obj.construction_guard, at, "private_literal_construction") for at in obj.evidence)}


def bind(state: State, binding_id: BindingKey | str, ref: ValueRef, evidence_ref: EvidenceRef, *,
         immutable_guard: ModelGuard | None = None,
         external_guard: ModelGuard | None = None) -> State:
    state = _step(state)
    obj = lookup_object(state, ref)
    if ref.kind == "join" or obj is not None and obj.construction_guard is not None:
        state = finish_construction(state, ref, evidence_ref)
    key = _key(binding_id)
    entries = dict(state.bindings)
    entries[key] = ref
    result = replace(state, bindings=tuple(sorted(entries.items(), key=lambda item: (item[0].declaration_id, item[0].context_id))))
    if _supported(immutable_guard, evidence_ref, "immutable_lexical_cell"):
        result = replace(result, immutable_bindings=tuple(sorted({*result.immutable_bindings,key},
            key=lambda cell:(cell.declaration_id,cell.context_id))), guards=_unique((*result.guards,immutable_guard)))
    if _supported(external_guard,evidence_ref,"external_lexical_cell_domain"):
        domains = {item.binding:item for item in result.external_binding_domains}
        domains[key] = BindingDomain(key,external_guard,evidence_ref)
        result = replace(result,external_binding_domains=tuple(domains[key] for key in sorted(domains,
            key=lambda cell:(cell.declaration_id,cell.context_id))),guards=_unique((*result.guards,external_guard)))
    if key in state.escaped_bindings or state.unknown_captures_escaped:
        ids, _edges, wide, exceeded, cells = _reachable(result, (ref,), include_escaped=False)
        if wide or exceeded:
            private = _private_constructions(result, ids) if not exceeded and not result.incomplete else set()
            ids = {obj.alloc_id for obj in result.objects} - private
        result = _escape(result, ids)
        result = replace(result, escaped_bindings=tuple(sorted({*result.escaped_bindings, *cells},
            key=lambda cell: (cell.declaration_id, cell.context_id))),
            unknown_captures_escaped=result.unknown_captures_escaped or wide)
        if exceeded:
            result = _budget(result, "ir_reachability_budget_exceeded")
    return result


def lookup_binding(state: State, binding_id: BindingKey | str, evidence_ref: EvidenceRef) -> ValueRef:
    if state.incomplete:
        return _unknown(evidence_ref, "ir_state_budget_incomplete")
    return next((ref for key, ref in state.bindings if key == _key(binding_id)), _unknown(evidence_ref, "ir_binding_not_available"))


def lookup_object(state: State, ref: ValueRef | ObjectRef) -> ObjectVersion | None:
    obj = ref if isinstance(ref, ObjectRef) else ref.object_ref
    return next((item for item in state.objects if obj is not None and item.alloc_id == obj.alloc_id), None)


def lookup_field(state: State, ref: ValueRef | ObjectRef, key: str, evidence_ref: EvidenceRef, *,
    external_own_data: bool = False) -> Projection:
    if state.incomplete:
        return _failure(evidence_ref, "ir_state_budget_incomplete")
    if not isinstance(key, str) or key == "__proto__":
        return _failure(evidence_ref, "ir_dynamic_or_prototype_key")
    if isinstance(ref, ValueRef) and ref.barriers:
        return _failure(evidence_ref, ref.barriers[0])
    if isinstance(ref, ValueRef) and ref.kind == "join":
        if len(ref.alternatives) > state.limits.max_alternatives:
            return _failure(evidence_ref, "ir_alternative_budget_exceeded")
        return _join_projections(tuple(lookup_field(state, child, key, evidence_ref,
            external_own_data=external_own_data) for child in ref.alternatives), evidence_ref, state.limits.max_alternatives)
    obj = lookup_object(state, ref)
    if obj is not None:
        return _project_version(state, obj, key, evidence_ref)
    # The published finite protocol has no child-surface guard parameter.
    # A boolean/condition ID cannot add a recursive plainness capability.
    if external_own_data:
        return _failure(evidence_ref, "ir_recursive_external_own_data_model_unavailable")
    return _failure(evidence_ref, "ir_referent_own_data_not_certified")


def copy_own_slots(state: State, source: ValueRef, evidence_ref: EvidenceRef, *, context_id: str,
    excluded_keys: tuple[str, ...] = (), exclusions_closed: bool = True,
    destination: ValueRef | None = None, model_supported: bool = False,
    model_guard: ModelGuard | None = None) -> tuple[State, ValueRef]:
    state = _step(state)
    certified = model_supported and _supported(model_guard, evidence_ref, "own_data_copy")
    if destination is None:
        state, destination = allocate(state, evidence_ref, context_id=context_id,
            model_supported=model_supported, model_guard=model_guard, allocation_tag="shallow_copy")
    target = lookup_object(state, destination)
    source_snapshot = lookup_object(state, source)
    if target is None or state.incomplete:
        return _budget(state, "ir_copy_destination_or_budget_unknown"), _unknown(evidence_ref, "ir_copy_destination_or_budget_unknown")
    if source.kind == "join":
        if not source.alternatives or len(source.alternatives) > state.limits.max_alternatives:
            return _budget(state, "ir_alternative_budget_exceeded"), _unknown(evidence_ref, "ir_alternative_budget_exceeded")
        branches = tuple(copy_own_slots(state, child, evidence_ref, context_id=context_id,
            excluded_keys=excluded_keys, exclusions_closed=exclusions_closed, destination=destination,
            model_supported=model_supported, model_guard=model_guard) for child in source.alternatives)
        if not branches or len(branches) > state.limits.max_alternatives:
            return _budget(state, "ir_alternative_budget_exceeded"), _unknown(evidence_ref, "ir_alternative_budget_exceeded")
        return join_states(tuple(item[0] for item in branches), evidence_ref), join_values(tuple(item[1] for item in branches), evidence_ref)
    source_safe = bool(source_snapshot and source_snapshot.model_supported and not source_snapshot.barriers
        and all(slot.closed and not slot.barriers for slot in source_snapshot.slots)
        and not source_snapshot.conditional_allocation and not source.barriers)
    if not certified or not source_safe or not exclusions_closed:
        reason = "ir_copy_surface_or_exclusions_not_certified"
        damaged = replace(target, closed_shape=False, base_closed_shape=False,
            slots=tuple(replace(slot, closed=False, barriers=tuple(sorted({*slot.barriers, reason}))) for slot in target.slots),
            barriers=tuple(sorted({*target.barriers, reason})), evidence=_unique((*target.evidence, evidence_ref)))
        return _put(state, damaged), destination
    if _copy_depth(source_snapshot, state.limits.max_copy_depth) >= state.limits.max_copy_depth:
        return _budget(state, "ir_copy_projection_depth_exceeded"), _unknown(evidence_ref, "ir_copy_projection_depth_exceeded")
    old_slots = {slot.key: slot for slot in target.slots}
    keys = sorted({*old_slots, *(slot.key for slot in source_snapshot.slots), *excluded_keys})
    for key in keys:
        if key in excluded_keys:
            if destination.object_ref.alloc_id == target.alloc_id and not target.slots and not target.copy_layers:
                old_slots[key] = FieldSlot(key, "absent", value("absent", evidence_ref), True, evidence=(evidence_ref,))
            continue
        copied = _project_version(state, source_snapshot, key, evidence_ref)
        observation = _observation(evidence_ref, source_snapshot, key, copied.value, copied.presence)
        copied = replace(copied, observations=_unique((*copied.observations, observation)))
        previous = _project_version(state, target, key, evidence_ref)
        selected = _overlay(previous, copied, evidence_ref, state.limits.max_alternatives)
        old_slots[key] = FieldSlot(key, selected.presence, selected.value, selected.closed,
            selected.observations, (evidence_ref,), selected.barriers)
    layers = target.copy_layers
    if not source_snapshot.closed_shape:
        layers = (*layers, CopyLayer(source_snapshot, evidence_ref, tuple(sorted(set(excluded_keys))), True))
    copied_target = replace(target, slots=tuple(old_slots[key] for key in sorted(old_slots)), copy_layers=layers,
        closed_shape=target.closed_shape and source_snapshot.closed_shape, model_supported=target.model_supported and certified,
        evidence=_unique((*target.evidence, evidence_ref)), guards=_unique((*target.guards, model_guard)))
    return _put(state, copied_target), destination


def write_selected(state: State, receiver: ValueRef, key: str | None, ref: ValueRef,
    evidence_ref: EvidenceRef, *, model_supported: bool = False,
    model_guard: ModelGuard | None = None) -> State:
    state = _step(state)
    target = lookup_object(state, receiver)
    certified = model_supported and _supported(model_guard, evidence_ref, "own_data_write")
    if target is None or key is None or key == "__proto__" or not certified or receiver.barriers:
        return invalidate_reachable(state, (receiver, ref), evidence_ref, reason="ir_write_target_or_model_unknown",
            model_guard=model_guard, roots_complete=True, captures_complete=True,
            include_escaped=True, escape_roots=True, reflection=key is None or key == "__proto__")
    slots = {slot.key: slot for slot in target.slots}
    slots[key] = FieldSlot(key, "present", ref, True, evidence=(evidence_ref,))
    updated = replace(target, slots=tuple(slots[key] for key in sorted(slots)),
        evidence=_unique((*target.evidence, evidence_ref)), guards=_unique((*target.guards, model_guard)))
    state = _put(state, updated)
    if target.external_aliasable:
        state = _damage(state, {item.alloc_id for item in state.objects if item.alloc_id != target.alloc_id
            and (item.external_aliasable or item.escaped)}, evidence_ref, "ir_external_alias_write_possible")
    if target.escaped or target.external_aliasable:
        ids, _edges, wide, exceeded, cells = _reachable(state, (ref,), include_escaped=False)
        if wide or exceeded:
            private = _private_constructions(state, ids) if not exceeded and not state.incomplete else set()
            ids = {obj.alloc_id for obj in state.objects} - private
        state = _escape(state, ids)
        state = replace(state, escaped_bindings=tuple(sorted({*state.escaped_bindings, *cells},
            key=lambda key: (key.declaration_id, key.context_id))),
            unknown_captures_escaped=state.unknown_captures_escaped or wide)
        if exceeded:
            state = _budget(state, "ir_reachability_budget_exceeded")
    return state


def invalidate_reachable(state: State, roots: tuple[ValueRef, ...], evidence_ref: EvidenceRef, *,
    reason: str, roots_complete: bool = False, captures_complete: bool = False,
    include_escaped: bool = True, escape_roots: bool = True,
    captured_roots: tuple[ValueRef, ...] = (), captured_bindings: tuple[BindingKey, ...] = (),
    reflection: bool = False, visible_roots: tuple[ValueRef, ...] | None = None,
    model_guard: ModelGuard | None = None) -> State:
    state = _step(state)
    roots_certified = roots_complete and _supported(model_guard, evidence_ref, "effect_roots")
    captures_certified = captures_complete and _supported(model_guard, evidence_ref, "lexical_capture_domain")
    scope_certified = visible_roots is not None and _supported(model_guard, evidence_ref, "lexical_capture_domain")
    cells = tuple(ref for binding, ref in state.bindings if binding in captured_bindings)
    all_roots = (*roots, *captured_roots, *cells)
    ids, edges, wide, exceeded, cells = _reachable(state, all_roots, include_escaped=include_escaped, proof=model_guard)
    visible_ids: set[str] = set()
    if scope_certified and (not roots_certified or not captures_certified):
        visible_ids, visible_edges, visible_wide, visible_exceeded, visible_cells = _reachable(state, visible_roots, include_escaped=False, proof=model_guard)
        edges.update(visible_edges)
        cells.update(visible_cells)
        wide = wide or visible_wide
        exceeded = exceeded or visible_exceeded
    private = _private_constructions(state, ids | visible_ids) if not reflection and not exceeded and not state.incomplete else set()
    if reflection or wide or exceeded or state.incomplete:
        ids = {obj.alloc_id for obj in state.objects} - private
    elif not roots_certified or not captures_certified:
        ids.update(visible_ids if scope_certified else {obj.alloc_id for obj in state.objects} - private)
    protected = {obj.alloc_id for obj in state.objects if obj.fresh and not obj.escaped and obj.alloc_id not in ids}
    if not roots_certified and not scope_certified or exceeded or wide or reflection or state.incomplete:
        protected = private
    reason_codes = reason if not exceeded else "ir_reachability_budget_exceeded"
    result = _damage(state, ids, evidence_ref, reason_codes)
    cells.update(captured_bindings)
    if reflection or wide or exceeded or state.incomplete:
        cells.update(key for key, _ref in state.bindings)
    elif not roots_certified or not captures_certified:
        if scope_certified:
            visible_values = {ref.value_id for ref in visible_roots}
            cells.update(key for key, ref in state.bindings if ref.value_id in visible_values)
        else:
            cells.update(key for key, _ref in state.bindings)
    if cells:
        bindings = []
        written = cells - set(result.immutable_bindings)
        domains = {item.binding:item for item in result.external_binding_domains
            if _supported(item.guard,item.evidence,"external_lexical_cell_domain")}
        for key, ref in result.bindings:
            if key not in written:
                bindings.append((key,ref))
                continue
            if key in domains and scope_certified and not reflection and not exceeded and not state.incomplete:
                # A live module cell may change. Its replacement may refer
                # to actual effect roots/cells or the exposed world, without
                # acquiring an unexposed caller-local temporary by fiat.
                domain = guard((domains[key].evidence,evidence_ref),evidence_ref.model_id,capabilities=("external_value_domain",),supported=True,
                    assumptions=("source-authenticated module cell outside the caller activation may be rebound by this opaque effect",
                        "replacement referents/captures are within affected/exposed allocations and recorded live cells; private construction destinations are not implicit reverse edges"))
                result = register_guard(result,domain)
                at = replace(evidence_ref,guard_ids=(*evidence_ref.guard_ids,domain.guard_id),kind="module_cell_effect_domain")
                replacement = value("unknown",at,external_alias=True,alias_roots=tuple(ObjectRef(alloc) for alloc in sorted(ids)),
                    captured_bindings=tuple(sorted(cells - {key},key=lambda cell:(cell.declaration_id,cell.context_id))),
                    barriers=("ir_captured_binding_write_possible",))
            else:
                replacement = _unknown(evidence_ref,"ir_captured_binding_write_possible")
            bindings.append((key,replacement))
        result = replace(result,bindings=tuple(bindings))
        edges.update(("", f"binding:{key.declaration_id}:{key.context_id}", "possible_captured_binding_write") for key in written)
    if escape_roots:
        result = _escape(result, ids)
        result = replace(result, escaped_bindings=tuple(sorted({*result.escaped_bindings, *cells},
            key=lambda item: (item.declaration_id, item.context_id))),
            unknown_captures_escaped=result.unknown_captures_escaped or wide)
    entry = EffectRef("", evidence_ref, reason_codes, tuple(sorted({root.alloc_id for ref in roots for root in ref.alias_roots}
        | {ref.object_ref.alloc_id for ref in all_roots if ref.object_ref is not None})), tuple(sorted(ids)),
        tuple(sorted(protected)), roots_certified, captures_certified, include_escaped, reflection,
        exceeded, visible_scope_restricted=scope_certified, visible_root_allocations=tuple(sorted(visible_ids)),
        guard=model_guard, reachability_edges=tuple(sorted(edges)))
    entry = replace(entry, effect_id=_digest(entry))
    result = replace(result, effects=_unique((*result.effects, entry)))
    return _budget(result, "ir_reachability_budget_exceeded") if exceeded else result


def _external_domain(state: State, ref: ValueRef, proof: ModelGuard | None) -> bool:
    # Primitives have no possible object referents.  This is a reach-domain
    # fact, not a claim about their content or normal/abrupt completion.
    if not ref.barriers and not ref.capture_unknown and (
            ref.kind == "literal" and ref.literal_kind in {"string", "number", "true", "false", "null", "undefined"}
            or ref.kind == "scalar" and ref.literal_kind in {"boolean_unknown", "string_unknown"}):
        return True
    # A source branch join does not introduce new referents.  Preserve the
    # certified reach domain only when *every* alternative has it; contents,
    # selected slots and branch truth remain independent and unknown.
    if ref.kind == "join":
        return bool(ref.alternatives and not ref.barriers and not ref.capture_unknown
            and all(_external_domain(state, child, proof) for child in ref.alternatives))
    if not ref.external_alias or ref.capture_unknown:
        return False
    proofs = tuple(candidate for candidate in (proof, *state.guards, *(effect.guard for effect in state.effects)) if candidate is not None)
    if any(_supported(candidate, at, "external_value_domain") for candidate in proofs for at in ref.evidence):
        return True
    # A source parameter projection originates outside this activation.
    # Its unknown child may alias that root or any exposed external object,
    # but cannot reach a later private allocation without a captured edge.
    for root in ref.alias_roots:
        obj = lookup_object(state, root)
        if obj is None or obj.origin is None or not obj.external_aliasable:
            continue
        if not any(_supported(candidate, at, "own_data_shape") for candidate in obj.guards for at in obj.evidence):
            continue
        if ref.provenance and all(origin.binding == obj.origin.binding and origin.parameter_index == obj.origin.parameter_index
                and origin.field_path[:len(obj.origin.field_path)] == obj.origin.field_path for origin in ref.provenance):
            return True
    return False


def external_domain_supported(state: State, ref: ValueRef) -> bool:
    """A guarded possible external reach domain, not contents or plainness."""
    return _external_domain(state, ref, None)


def _reachable(state: State, refs: tuple[ValueRef, ...], *, include_escaped: bool,
    proof: ModelGuard | None = None) -> tuple[set[str], set[tuple[str, str, str]], bool, bool, set[BindingKey]]:
    objects = {obj.alloc_id: obj for obj in state.objects}
    external = {obj.alloc_id for obj in state.objects if obj.external_aliasable or obj.escaped or not obj.fresh}
    pending_values = [(ref, "", "explicit_root") for ref in refs]
    cells: set[BindingKey] = set(state.escaped_bindings) if include_escaped else set()
    pending_values.extend((ref, "", "escaped_binding_cell") for key, ref in state.bindings if key in cells)
    pending_objects = [(key, "", "escaped_or_external_world") for key in external] if include_escaped else []
    reached: set[str] = set()
    seen_values: set[str] = set()
    edges: set[tuple[str, str, str]] = set()
    wide, operations = False, 0
    while pending_values or pending_objects:
        operations += 1
        if operations > state.limits.max_reachable:
            return set(objects), edges, True, True, {key for key, _ref in state.bindings}
        if pending_values:
            ref, parent, relation = pending_values.pop()
            if ref.value_id in seen_values:
                continue
            seen_values.add(ref.value_id)
            if ref.object_ref is not None:
                pending_objects.append((ref.object_ref.alloc_id, parent, relation))
            pending_objects.extend((root.alloc_id, parent, "possible_referent_root_alias") for root in ref.alias_roots)
            if ref.external_alias:
                pending_objects.extend((key, parent, "possible_external_alias") for key in external)
            if (ref.kind in {"unknown", "call_result", "symbolic"} and not _external_domain(state, ref, proof)) or ref.capture_unknown or (ref.kind == "callable" and not any(at.guard_ids for at in ref.evidence)):
                wide = True
            for cell in ref.captured_bindings:
                cells.add(cell)
                edges.add((parent, f"binding:{cell.declaration_id}:{cell.context_id}", "captured_binding_cell"))
                current = next((item for key, item in state.bindings if key == cell), None)
                if current is None:
                    wide = True
                else:
                    pending_values.append((current, parent, "captured_binding_cell"))
            pending_values.extend((child, parent, "value_alternative") for child in ref.alternatives)
            continue
        alloc_id, parent, relation = pending_objects.pop()
        edges.add((parent, alloc_id, relation))
        if alloc_id in reached:
            continue
        if alloc_id not in objects:
            wide = True
            continue
        reached.add(alloc_id)
        obj = objects[alloc_id]
        if obj.external_aliasable or not obj.fresh:
            pending_objects.extend((other, alloc_id, "possible_external_object_alias") for other in external)
        pending_values.extend((slot.value, alloc_id, "own_slot_referent") for slot in obj.slots if slot.presence != "absent")
        # Open copied surfaces can contain an external child which aliases
        # its old root. This is not a reverse edge to the new copy parent.
        if obj.origin is not None or obj.copy_layers:
            pending_objects.extend((other, alloc_id, "open_surface_possible_child_alias") for other in external)
    return reached, edges, wide, False, cells


def _escape(state: State, ids: set[str]) -> State:
    result = state
    for obj in state.objects:
        if obj.alloc_id in ids and not obj.escaped:
            result = _put(result, replace(obj, escaped=True, construction_guard=None))
    return result


def _damage(state: State, ids: set[str], at: EvidenceRef, reason: str) -> State:
    result = state
    for obj in state.objects:
        if obj.alloc_id not in ids:
            continue
        slots = tuple(replace(slot, closed=False, barriers=tuple(sorted({*slot.barriers, reason}))) for slot in obj.slots)
        damaged = replace(obj, slots=slots, closed_shape=False, base_closed_shape=False,
            barriers=tuple(sorted({*obj.barriers, reason})), evidence=_unique((*obj.evidence, at)))
        result = _put(result, damaged)
    return result


def join_values(refs: tuple[ValueRef, ...], evidence_ref: EvidenceRef, *, max_alternatives: int = 32) -> ValueRef:
    pending, combined = list(refs), {}
    while pending:
        ref = pending.pop()
        if ref.kind == "join" and not ref.barriers:
            pending.extend(ref.alternatives)
        else:
            combined[ref.value_id] = ref
        if len(combined) + len(pending) > max_alternatives * max_alternatives:
            return _unknown(evidence_ref, "ir_alternative_budget_exceeded")
    alternatives = tuple(combined[key] for key in sorted(combined))
    if not alternatives or len(alternatives) > max_alternatives:
        return _unknown(evidence_ref, "ir_alternative_budget_exceeded" if alternatives else "ir_join_without_values")
    if len(alternatives) == 1:
        return alternatives[0]
    return value("join", evidence_ref, alternatives=alternatives)


def _join_projections(projections: tuple[Projection, ...], at: EvidenceRef, limit: int) -> Projection:
    if not projections:
        return _failure(at, "ir_join_without_projection")
    presences = {item.presence for item in projections}
    if len(presences) == 1:
        presence = projections[0].presence
    elif presences == {"unknown"}:
        presence = "unknown"
    else:
        presence = "maybe"
    refs = tuple(item.value for item in projections if item.presence != "absent")
    joined = join_values(refs, at, max_alternatives=limit) if refs else value("absent", at)
    return Projection(presence, joined, all(item.closed for item in projections), all(item.whole_closed for item in projections),
        _unique(tuple(observation for item in projections for observation in item.observations)),
        tuple(sorted({reason for item in projections for reason in item.barriers})))


def join_states(states: tuple[State, ...], evidence_ref: EvidenceRef) -> State:
    if not states:
        return _budget(initial_state(), "ir_join_without_states")
    if len(states) > min(item.limits.max_alternatives for item in states):
        return _budget(states[0], "ir_alternative_budget_exceeded")
    states = tuple(item for _identity, item in sorted({_digest(item): item for item in states}.items()))
    limits = Limits(*(min(getattr(item.limits, name.name) for item in states) for name in fields(Limits)))
    bindings = []
    for key in sorted({key for item in states for key, _ref in item.bindings}, key=lambda key: (key.declaration_id, key.context_id)):
        refs = tuple(next((ref for cell, ref in item.bindings if cell == key), _unknown(evidence_ref, "ir_branch_binding_missing")) for item in states)
        bindings.append((key, join_values(refs, evidence_ref, max_alternatives=limits.max_alternatives)))
    result = State(bindings=tuple(bindings), effects=_unique(tuple(effect for item in states for effect in item.effects)),
        escaped_bindings=tuple(sorted({key for item in states for key in item.escaped_bindings}, key=lambda key: (key.declaration_id, key.context_id))),
        unknown_captures_escaped=any(item.unknown_captures_escaped for item in states),
        barriers=tuple(sorted({reason for item in states for reason in item.barriers})),
        steps=max(item.steps for item in states) + 1, limits=limits, incomplete=any(item.incomplete for item in states),
        guards=_unique(tuple(proof for item in states for proof in item.guards)),
        immutable_bindings=tuple(sorted(set.intersection(*(set(item.immutable_bindings) for item in states)),
            key=lambda cell:(cell.declaration_id,cell.context_id))),
        external_binding_domains=tuple(sorted(set.intersection(*(set(item.external_binding_domains) for item in states)),
            key=lambda item:(item.binding.declaration_id,item.binding.context_id))))
    for alloc_id in sorted({obj.alloc_id for item in states for obj in item.objects}):
        versions = tuple(next((obj for obj in item.objects if obj.alloc_id == alloc_id), None) for item in states)
        available = tuple(obj for obj in versions if obj is not None)
        if len(available) != len(states):
            merged = replace(available[0], conditional_allocation=True, closed_shape=False,
                construction_guard=None,
                barriers=tuple(sorted({reason for obj in available for reason in obj.barriers} | {"ir_branch_allocation_missing"})))
        elif len({obj.version_id for obj in available}) == 1:
            merged = available[0]
        else:
            slots = []
            for key in sorted({slot.key for obj in available for slot in obj.slots}):
                selected = _join_projections(tuple(_project_version(item, obj, key, evidence_ref) for item, obj in zip(states, available)),
                    evidence_ref, limits.max_alternatives)
                slots.append(FieldSlot(key, selected.presence, selected.value, selected.closed, selected.observations,
                    (evidence_ref,), selected.barriers))
            # A varying open surface cannot be collapsed to one branch's
            # latent copy layer. Materialized selected slots survive; other
            # keys stay unknown until a branch-specific state is selected.
            stable_open = all(obj.copy_layers == available[0].copy_layers and obj.origin == available[0].origin for obj in available)
            closed = all(obj.closed_shape for obj in available)
            merged = replace(available[0], slots=tuple(slots), closed_shape=closed,
                construction_guard=available[0].construction_guard if all(obj.construction_guard == available[0].construction_guard for obj in available) else None,
                fresh=all(obj.fresh for obj in available), escaped=any(obj.escaped for obj in available),
                external_aliasable=any(obj.external_aliasable for obj in available),
                model_supported=all(obj.model_supported for obj in available),
                origin=available[0].origin if stable_open else None,
                copy_layers=available[0].copy_layers if stable_open else (),
                base_closed_shape=all(obj.base_closed_shape for obj in available) if stable_open else closed,
                evidence=_unique(tuple(at for obj in available for at in obj.evidence)),
                guards=_unique(tuple(proof for obj in available for proof in obj.guards)),
                barriers=tuple(sorted({reason for obj in available for reason in obj.barriers}
                    | ({"ir_branch_open_surface_not_materialized"} if not stable_open and not closed else set()))),
                conditional_allocation=any(obj.conditional_allocation for obj in available))
        result = _put(result, merged)
    return _budget(result, "ir_step_budget_exceeded") if result.steps > result.limits.max_steps else result


def to_data(record: _Record) -> dict:
    return _data(record)
