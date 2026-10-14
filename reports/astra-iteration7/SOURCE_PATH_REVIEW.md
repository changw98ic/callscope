# Source-only field-path review

This review reads target TypeScript and published v9/v8 JSON as data. It does not execute or import either target, run any target or CallScope CLI, build or install anything, run test suites, or create synthetic inputs. It does not modify target sources, analyzer sources, or frozen prior artifacts. The observations below are semantic review arguments, not newly computed analyzer findings or runtime checks.

## Source identity and frozen result

The current source bytes match the source hashes carried by the published v9 locations:

| Source | SHA256 |
| --- | --- |
| `server/services/engine-runner.ts` | `952b6a43e9d2e5a2040eae1c7c8ec5c000d26a12f1c44d395041434db48bd864` |
| `server/services/hub/hub-queue.ts` | `0bd13766a2a2fcd271c2ead8166fbbd6f782fde32f63954ccced88a4cb2de02c` |
| `server/services/agent/agent-config.ts` | `83a2eef775f1ff274054ee16fa749e195ae5a475f42abf520b2434e7ed6af484` |

`reports/astra-iteration6/IR_MIGRATION_COMPARISON.json` at `/services_own_shape_comparison` records the regression at the same actual `buildServices` call at engine-runner line 155, edge `fde7f8eaa64a8b1209e61834`: v8 had selected presence `absent`, selected shape closed, and whole object shape closed; v9 has `unknown` and both shape bits false. Both retain the same eleven literal keys. The v9 literal fact is `7916505bc6962773a86aa558`. This is evidence of the published regression; neither the old positive result nor isolated IR observations substitute for a corrected full-adapter result.

The frozen `field-assessments.json` keeps all five evaluated paths: engine one, queue two branch sources, and agent two returns. All remain unknown. Its separate invocation/completion, runtime, transport, and full functionality limits remain applicable after any local precision repair.

## `buildServices`: valid conditional own-shape argument

Read the complete ordinary synchronous function at engine-runner lines 73–122, including initializer evaluation and closure bodies, rather than treating a list of literal keys as sufficient proof.

At line 85 a new ordinary object literal is allocated. Lines 86–118 use eleven distinct static property names, without spread, computed names, accessor declarations, deletion, or a `__proto__` setter definition. On normal completion of the initializer, those definitions create these own enumerable data slots in source order:

`createJob`, `startPhase`, `completePhase`, `completeJob`, `failJob`, `blockJob`, `appendEvent`, `prepareTask`, `getPool`, `getArtifactIndex`, `providerServices`.

The initializer can call helpers and access broker members. Those operations can throw, have effects on their evaluated roots, or produce unknown member values. The new `ports` object is not supplied as a receiver or argument to any of them, stored in an external object, or referenced by any created closure. Its binding is initialized only after the initializer completes. The only remaining statement returns that binding at line 121. Conditional on this normal return, the returned object therefore has exactly those eleven own slots, with no own `maxRetries` slot. The proof depends on allocation identity, evaluation order, lexical captures, and lack of exposure, not text-search absence.

The relevant actual captures are:

| Expression | Caller-local captures relevant to exposure |
| --- | --- |
| `withJobOptions` and its returned arrow, lines 82–83 | `runtimeDataRoot`; the returned arrow also uses its own activation's `fn` |
| local completeJob / appendEvent / getArtifactIndex arrows, lines 92, 99–104, 110–111 | `runtimeDataRoot`; imported/module functions are outside this activation |
| `getPool` arrow, line 107 | `cpbRoot`, `hubRoot`, `runtimeEnv` |
| arrows returned by `buildCreateJobPort`, lines 55–69 | that helper activation's `broker`, `runtimeDataRoot`, and module-level functions |
| fake callback returned by `prepareTaskForEnv`, lines 31–44 | no `ports` reference |

Broker `.bind` paths receive broker and broker members. A broker getter, custom member `.bind`, or other opaque result can affect broker or external objects and alter returned function behavior. It does not acquire the unexposed `ports` allocation through the shown call roots. The nested `providerServices` literal also has five fixed own keys at normal creation; its member values and later use remain separate.

This own-shape argument does **not** prove:

- that any initializer call completes or that `buildServices` is ever reached;
- which branch or function each service member selects, that a member is callable, or any service invocation result;
- that a later `ports.maxRetries` Get yields undefined: the object inherits a prototype, and inherited data/accessor behavior requires its own model;
- that the object cannot later be mutated after return and exposure;
- that arbitrary unknown captures may be ignored. A real closure edge, including a future lexical cell, still exposes the referenced allocation when that closure escapes.

In particular, own-slot absence used by object spread differs from an ordinary property read. Spread copies own enumerable slots and does not consult an inherited `maxRetries` slot. Literal property creation likewise does not invoke an inherited setter for these names.

## Engine rest and ordered final argument

At engine-runner lines 131–138, rest creates a private shallow copy excluding only `cpbRoot`, `project`, `sourcePath`, `hubRoot`, and `workerBrokerClient`. The selected key `maxRetries` is not excluded. Under the existing explicit whole-surface ordinary enumerable own-data copy condition, its copied slot can retain parameter-field provenance at that copy's source version; key presence remains a separate unknown unless established.

The source `opts` is used again after awaits. Its own slots and exposed children can change. That does not by itself change the fresh `jobOptions` parent's already-copied top-level slot. Its `env`, `providerServices`, or selected value can still be shared references; shallow copy does not freeze or certify those referents.

The helpers receive values taken from the rest object, not the rest parent. The final `processHooks.registerChild` callback captures `cpbRoot`, `jobId`, and `projectRuntimeRoot`, without a reference to `jobOptions`, `services`, or the final argument literal. At lines 157–180 the final argument first spreads `jobOptions`, then defines explicit different keys, then spreads `services`, and finally sets `providerServices`. Once the helper own-key absence is established, the services spread does not overwrite `maxRetries`. The final normalizer receives `jobOptions.providerServices`; it can affect that shared referent or a selected child alias, but does not obtain either private parent merely because those parents contain references to it.

This supports restoration of a local copied-slot origin relation at the call argument, conditional on normal reach and the registered copy/Get surface premises. It does not prove field presence, selected child contents, initial input value stability, `runJob` body behavior, awaited-prefix completion, fulfillment identity, or end-to-end retry consumption. The final argument should be assessed before `runJob` activation; callee effects must not be applied retroactively to that observation.

## Queue and agent paths have additional necessary limits

`enqueue` at hub-queue lines 1561–1569 shallow-copies `input`. Its metadata child is initially shared. At line 1570 the falsy branch instead replaces that slot with a fresh empty object. Lines 1571–1573 then write `acpProfile`, `uiLane`, and `uiLaneReason` on the child before the selected call at line 1580. These are different source branches and must remain in the denominator. A copied metadata reference is not proof that its child surface is ordinary data; ordinary Set, setters/proxies, primitive behavior, inherited effects, and alias writes need their own handling. The copy/Get condition alone cannot certify those writes or preserve the child's `maxRetries` value through them. Conversely, on a proven ordinary fresh fallback child with supported different-key writes, the selected absent key can remain locally absent.

`resolveAgentsForEntry` at agent-config lines 471–494 aliases `metadata` as `metadataRecord` and awaits several operations before merging configuration. At line 487 it returns the same metadata object on one branch: identity is a local body-return relation, but its current own slots can have changed through shared references or effects. At line 489 it creates a new object by spreading the current metadata and replacing only `agents` and `agent`. Under the registered full-surface copy condition, that construction preserves the selected `maxRetries` slot's copy-time origin rather than establishing its initial entry value. Neither branch proves fulfillment identity: async return performs Promise/thenable assimilation, which can read a `then` property or inherit one. A source-form relation before assimilation must not be relabeled as a proved awaited value.

## High-value preservation requirements

1. Keep own-key shape and slot provenance independent from opaque slot values and function behavior. A fresh private literal can have a complete own-key set even if its service values are unknown.
2. Preserve allocation and version identity through actual helper return mappings and joins. Unknown earlier effects do not retroactively alter a later private allocation; unknown external children do not create a reverse reachability edge to a private parent that contains them.
3. Carry copy-time selected-slot observations through later source-root changes, while retaining child alias roots, captures, escape, and mutable contents. Do not turn shallow copying into a deep-copy claim.
4. Account for the actual closure capture domain, including future cells, and the receiver/arguments of each opaque operation. A module callee cannot lexically capture caller-local cells, but actual callbacks, escaped cells, and reflection still require widening.
5. Keep ordinary Get, Set, CopyDataProperties, and literal own-data creation as distinct semantic obligations. A missing own key is enough to exclude a spread overwrite; it is not enough to certify a getter-free read.
6. Record normal reach, body return, call argument observation, and async fulfillment separately. Restoration of the eleven-key service summary should not force the queue/agent paths or all five contracts to positive.

No new stronger user/environment model is required to justify the private eleven-key literal argument. If the adapter cannot express the necessary allocation/capture boundary using authenticated AST and the existing IR evidence, the formal result should retain that precise implementation gap rather than making a source-only argument look machine-proved.
