# Source-only review of value domains and actual property operations

Review date: 2026-10-12. This reviewer read the frozen iteration8 records, the corresponding 0.10.1 core source, and CodePatchBay source as data. No target or analyzer import/execution, target CLI/index, tests, builds, installs, or tool test suite was used. The root agent owns core changes. This reviewer writes only this new report.

The inspected core hashes match iteration8 `CORE_FREEZE.json`: `semantic_ir.py` is `b430f7ce224f7321fc6541bc11c378ac57f6572ad9d9333b955871a3823a4539`; `field_summaries.py` is `10f33804c3b77913aef29e12a0a00c24ea43ab61f7c09276ed053becb7d69443`. The frozen policy bytes hash is `134671b5cb1cc7f6acb3514e63eac6a1e7bd3d53d48b750d38d8d35b9b63faa0`; its published semantic policy hash is `920edf6ba07f0a43821cd940b211848556ace921d2d8c3e76f05face4dc73ef0`. Line references below describe this inspected source and may move during implementation.

## Saved endpoints and causes

| Frozen endpoint | Saved result | Source distinction that must survive |
| --- | --- | --- |
| engine `runJob` argument, `engine-runner.ts:157` | conditional source form preserved, selected closed, presence unknown, whole shape open | Copy observations capture the old top-level slot; shared child mutation and actual activation remain separate. |
| queue `resolveAgentsForEntry` argument, `hub-queue.ts:1580`, two branches | unknown, gap `field_get_value_origin_unknown` | A root own-data surface does not certify the `metadata` child, ordinary Set, or a later actual Get. |
| agent direct body return, `agent-config.ts:487` | unknown, gap `ir_captured_binding_write_possible` | Parameter-cell/referent identity can be retained independently from current selected-field contents and async fulfillment. |
| agent constructed body return, `agent-config.ts:489` | unknown, gap `ir_copy_surface_or_exclusions_not_certified` | A source spread plus two different explicit keys describes an ordered copy relationship, not an authenticated current source slot or Promise result. |

The queue first records unsupported `new Error` at line 1551 in global source facts, but that is the `then` branch of a throw. `execute` removes that branch from active continuations. It must not be described as automatically damaging the surviving sink branch.

The actual expanded `buildMeta(input)` at queue line 1554 has an avoidable default alternative: `not_undefined` accepts only a *fresh* tracked object. The supplied selected root is an external ObjectRef (`fresh=False`), so the helper joins `input` with `{}`. An actual Get on the joined receiver cannot use `ordinary_get`'s current `lookup_object` authorization. `_external_domain` also fails to recognize an authenticated external ObjectRef itself, although it recognizes symbolic children of that root. These distinct limitations create incomplete Get effects at `core/job/meta.ts:17` onward. A repair requires an explicit normal value/type/domain basis; a TS annotation alone cannot establish that a runtime formal is an object or a primitive.

In `enqueue`, the literal at line 1561 shallow-copies the root `input`; `metadata` is a shared child. Lines 1570–1573 use ordinary property assignment, not `CreateDataProperty` initialization. Under the unchanged policy, a symbolic child may have setters, accessors, Proxy behavior, or shared aliases. Removing earlier synthetic barriers does not by itself prove that these writes preserve another selected key. Repeated Gets of `normalizedInput.metadata` may also be affected by those operations. The source argument/formal mapping at line 1580 can remain useful even when the projected `maxRetries` source is unknown.

In `resolveAgentsForEntry`, saved facts identify unsupported dynamic import at line 474, unsupported array literal at line 477, unsupported helper loops at lines 441/457, and array destructuring at line 323. The blanket reflection transfer rewrites parent activation cells as well as heap contents. A dynamic import does not lexically capture the caller activation, and ordinary arrays have a new normal-result identity; these are useful domain refinements. Their values, module loading, iterators, getters, abrupt paths, and Promise completion must remain separately unknown.

## Concrete stale-slot Get loophole

`semantic_ir._damage` retains each materialized slot's old ValueRef and marks the FieldSlot `closed=False` with an effect barrier. `_project_version` returns that old value along with the damaged projection. However `ordinary_get` at inspected lines 301–306 only checks `selected.value.capture_unknown`; it does not require `selected.closed` or reject projection barriers. A damaged materialized slot commonly retains an unbarriered symbolic ValueRef with `capture_unknown=False`.

Consequently the source transfer can forward stale provenance into a new literal:

```javascript
const o = { maxRetries: opts.maxRetries };
opaque(o);
return { maxRetries: o.maxRetries };
```

The opaque call may replace `o.maxRetries`. The old copy/Get premise still permits a plain data Get, but permits no restoration of its old source. The returned fresh slot can otherwise look closed because literal initialization creates a new slot from the unbarriered old value. This is a source-inspection counterexample, not an executed witness.

Require a closed, barrier-free projection before forwarding its captured source ValueRef. If the Get model is supported but the slot source is damaged, return a bounded unknown from the receiver's authenticated domain, keeping source/presence unknown. A getter-free read does not heal earlier slot damage. Inspect this even when materialized slot presence remains `present`.

## Generic useful relationships under the same policy

1. Separate possible referents from own-data shape. A source-bound external child domain can exclude unexposed caller-local allocations while retaining unknown child shape, type, contents, captured cells, and completion. Do not turn external-domain support into a lookup-field capability.
2. Preserve normal primitive results independently of operand effects. Arithmetic, bitwise, equality, relational, `typeof`, and `!` results are primitives on normal completion. For `+`, the content/type alternatives include string/number/bigint; conversion effects and throws still matter. Do not infer standard `Boolean`, `String`, `Object.keys`, or other host-call result behavior from a bare name or the existing copy policy.
3. Evaluate array elements in source order and record the new normal-result allocation and referent slots. Array holes are absent indices. Array spread performs iteration and can invoke arbitrary code; an array shape/type or own-data copy model is no iteration-purity premise. A reach-only array record can be useful without a complete own-key claim.
4. Treat dynamic import's argument evaluation/coercion and module-loading effects separately from lexical caller capture. Return/await domains stay external or rooted in actual evaluated values and exposed/captured state; namespace fields and Promise fulfillment remain unknown. This does not authorize reading a module export from raw text or replacing the authenticated graph call edge.
5. Retain actual argument-to-formal value identity separately from selected-field source. The current selected sink already has its authenticated graph edge, parameter index, and argument ValueRef. Reporting that relationship does not prove callee activation, current child contents, or completion.
6. Retain body return expression identity separately from field origin. Line 487 syntactically returns the current `metadata` binding; this can support a source relationship after proving that cell was not rebound. It does not preserve its initial selected field after heap effects, and async return still has `then` assimilation. Line 489 builds a fresh object from the ordered spread and `agents`/`agent` writes; source syntax identifies the copy operation and different explicit keys even when source-surface/source-slot closure is unavailable.
7. For unsupported loops/helpers, narrow the effect domain using authenticated runtime reads and real live captures, while keeping unsupported control and normal/abrupt completion explicit. A loop that cannot lexically reach a parent activation's parameter cell should not get that cell by reflection fallback. Actual object referents supplied as arguments, module cells, closures, iterators, getters, and exposed state remain roots. This is not permission to assume the loop body pure or skip its effects.

## Capture and reachability boundaries

`_runtime_nodes` only erases `type_annotation` and `type_arguments`. `semantic_environment` already knows more erased contexts, including `type_query`, `type_parameters`, interface/type-alias declarations, implements clauses, import types, and function types. A body expression such as `value as typeof outer` can otherwise make the erased `outer` reference appear as a live capture. Prefer a shared runtime-syntax traversal or transparent-wrapper traversal that visits only the runtime expression child. Continue visiting nested closures, default RHS expressions, computed keys, enum/class runtime initializers, and import expressions.

Captured cells must remain live, including future initialization and future rebind. Const cell identity cannot freeze its referent. Removing fake TS captures is justified; removing unresolved real local captures is not. `this`, `super`, `arguments`, meta-properties, dynamic scope, direct eval, and unsupported implicit capture behavior must retain their current unknown boundary unless independently modeled.

When refining reach domains, retain the conservative domain of *replacement* values after opaque damage. Existing materialized slot values are only historical reach information after damage; new unknown children may reach the mutator's actual roots, recorded captures, and exposed world. Do not use their old zero-referent or external domain as a proof of the current child contents. Keep missing slots/open copy layers, conditional allocations, branch/state/value correlation, and budget failures visible. A domain improvement must not reintroduce a reverse child-to-private-parent edge or remove a real alias edge.

The public callable check in `_reachable` currently treats any nonempty EvidenceRef guard list as enough to avoid one callable-wide fallback. A branch condition or copy guard is not itself a callable capture capability. A future protocol refinement should authenticate the exact capture-domain capability instead of relying on nonempty guard IDs. This is protocol hardening advice; the demonstrated stale-slot Get issue above is the concrete source-transfer defect.

## Preservation requirements

Keep the engine conditional source-form result and the `buildServices` normal outer own-key absence from actual ordered IR state. A Get damage repair should not degrade a genuinely closed copied slot merely because its old source object was later mutated; ObservationRef identifies copy time and source version. Conversely, a fresh new slot must not inherit a damaged old source ValueRef as current provenance.

No refinement described here supplies recursive child plainness, general getter/setter absence, immutable prototypes, standard runtime hosts, automatic normal completion, Promise fulfillment, metadata transport, runtime values, or full functionality. The queue/agent four original unknown endpoints can remain unknown while richer partial relationships and more faithful effect domains become formally reportable. Goal and necessary-obligation definitions must remain unchanged.

## Follow-up: typed relative copy-boundary observation

An actual registered `CopyDataProperties` operation can support a narrower theorem even when its source ValueRef or its saved heap version has unknown contents:

> If the current source has the selected own enumerable data property at this actual copy boundary, the registered whole-surface copy premise holds, and this copy completes normally, the destination receives exactly that property's copy-time value/reference.

This antecedent is deliberately about the **current copy-time slot**, not the source's initial field, a damaged old slot, or its initial parameter provenance. The source may be an unknown ValueRef. A missing or nonenumerable selected source property does not satisfy the antecedent. Normal prefix, field presence, normal completion, and runtime values are not established by the theorem.

A separate immutable `CopyBoundaryObservation` can record:

- A content-derived observation ID, actual copy EvidenceRef, selected key/exclusions, and the existing supported `own_data_copy` ModelGuard.
- The actual source ValueRef/value ID, even if unknown, and its recorded ObjectVersion when available. A damaged recorded ObjectVersion is an abstract saved source state, not a proof of the current selected source slot.
- The destination ObjectRef, recorded before/after ObjectVersions, and its active private literal-construction guard.
- An explicit conditional-current-slot relation, capability support/status/gaps, and fixed false runtime/source-entry/field-presence/completion claims.

A pure IR observation operation can create this record without calling `lookup_field` to recover old provenance and without mutating FieldSlot, CopyLayer, Projection, or source ObjectVersion. It must use the canonical content-ID constructor; later changes to evidence, guards, snapshots, status, or gaps require a newly derived ID. Source/destination snapshots may be absent only with that absence recorded; a destination lacking the required ordinary fresh/private-construction evidence cannot receive an endpoint-retention proof.

Keep boundary recording separate from a second typed `survives_to_endpoint` witness. The witness needs the actual ordered suffix operations and terminal evidence. Internal literal data writes with static keys different from the selected key preserve the top-level copied reference. A later spread whose selected overwrite/absence is unknown, same-key write, computed/prototype/accessor member, destination-affecting effect, escape, or incomplete/budget step blocks the retained relation. Copy exclusions must be closed and must not include the selected key. A mutable shared child's contents can change without rewriting the copied top-level slot, so child mutation alone does not falsify value/reference transfer.

Releasing construction privacy at the literal's normal endpoint does not retroactively falsify the relation established there. It also provides no protection against later effects after the value is exposed. An observation with only boundary support must not be reported as a retained endpoint theorem.

For `agent-config.ts:489`, the recorded actual source is the value read from `metadata` at the spread, and the two explicit suffix keys are `agents` and `agent`. A supported endpoint witness would describe a current copy-time relationship under the already registered actual-copy surface premise, despite earlier source-content uncertainty. It must leave the original `maxRetries` field-origin result, async fulfilled-value result, reaching-origin, transport, and full-functionality claims unknown/false. This relation belongs in a separate typed observation/result domain, not in the old `source_form_preserved_when_present` category.

An actual spread's independently registered whole-source surface premise applies to that copy operation. It does not recursively grant a plain-data model to earlier or later Gets of the same child, or to any other child referent. The boundary observation therefore cannot authorize `ordinary_get`, ordinary Set, prototype assumptions, iterator behavior, or Promise assimilation.
