# Source relation design review

This file is a read-only design review of v0.10.1 source and saved iteration8 evidence. It is not an automatic witness, an implementation result, or a goal-acceptance report. No target code, CLI, build, install, or test was executed. Core, target repositories, and frozen reports were not edited.

## Why the current unknowns are correct

`field_summaries.py:748` computes `source_form_relation` from a closed selected projection and matching parameter provenance. `:757` then separates async body-return expressions from Promise fulfillment. Ordinary member assignments at `:641` retain an unmodeled Set effect; neither the Copy nor Get model licenses a setter-free Set. Consequently source syntax can be known while the selected heap projection remains unknown.

Saved iteration8 evidence contains:

- `cpb-astra-field-queue-agent-input`: one call AST site and two branch assessments at `hub-queue.ts:1580`. Both selected projections are unknown, with `field_get_value_origin_unknown`.
- `cpb-astra-field-agent-metadata-return`: two body returns at `agent-config.ts:487` and `:489`. The reference-return projection retains `ir_captured_binding_write_possible`; the copy-return projection retains `ir_copy_surface_or_exclusions_not_certified`. Both pre-completion and final source relations remain unknown.

The adapter already records literal parts and spread order, but the saved output does not provide a compact, typed, independently assessed relation connecting those parts, explicit Set targets, the actual argument position, and the selected source bindings.

## Keep two independent proof axes

Add an automatically generated `source_relations` result alongside the existing IR selected projection. Its proof domain is `captured_ast_and_lexical_binding`. The domain proves expression structure, declaration identity, direct control alternatives, direct program order conditional on normal arrival, and authenticated call argument/formal positions. It does not certify initial-to-current binding value identity, current object contents, successful Set, absent setter effects, runtime activation, or Promise fulfillment.

Do not change the semantics of `source_form_relation`, `pre_completion_source_form_relation`, `selected_field_shape_closed`, `selected_shape_complete`, `source_form_complete`, `reaching_value_origin_proven`, or `source_complete`. In particular, a complete source-syntax summary must not set any of those booleans to true.

Source syntax should not need a new runtime plainness policy assumption. Model-dependent copy preservation still uses the existing explicit Copy/Get guards and IR output. A relation may reference those guards without upgrading an unknown projection.

## Suggested typed records

The names below are proposed interfaces rather than claimed implemented types. Use frozen immutable records or equivalently strict validated JSON. IDs digest the complete record including source/snapshot/context identity.

```python
RelationKind = Literal[
    "lexical_alias_initializer",
    "ordered_object_construction",
    "conditional_member_set_attempt",
    "explicit_member_set_attempt",
    "normal_prefix_program_order",
    "actual_argument_formal_binding",
    "body_return_reaching_binding_reference",
    "body_return_ordered_copy_structure",
    "selected_key_direct_write_scan",
]

@dataclass(frozen=True)
class SourcePath:
    declaration_id: str
    binding_context: str
    member_keys: tuple[str, ...]
    evidence: EvidenceRef
    # Every key comes from the actual member AST; root resolution is unique.
    # This identifies source syntax, not a persistent receiver object.

@dataclass(frozen=True)
class SourceOperand:
    expression_id: str
    kind: str
    evidence: EvidenceRef
    source_path: SourcePath | None
    child_expression_ids: tuple[str, ...]
    # Finite discriminated kinds: binding_reference, static_member_access,
    # literal, object_construction, call, await, binary, conditional, unknown.

@dataclass(frozen=True)
class SourceRelation:
    relation_id: str
    kind: RelationKind
    status: Literal["proven_source_structure", "unknown_source_structure"]
    proof_domain: Literal["captured_ast_and_lexical_binding"]
    evidence: tuple[EvidenceRef, ...]
    operand_ids: tuple[str, ...]
    branch_guard_ids: tuple[str, ...]
    basis_relation_ids: tuple[str, ...]
    analysis_phase: str
    payload: object  # Strict discriminated immutable payload per kind.
    limitations: tuple[str, ...]
```

`SourceOperand` should retain the operator token for binary/default expressions (`||`, `??`, `&&` are distinct), the argument index for calls, and static data-member keys plus ordered spread/property parts for objects. An unsupported/computed operand is explicit unknown. Exact evidence should use saved original AST locations and parse/source identities, not a later text or name search.

Every relation should carry `analysis_phase` from a small enum: `initializer_expression`, `ordinary_set_attempt`, `call_argument_before_callee_activation`, or `body_return_expression_before_promise_assimilation`. The strict payload determines what has actually been proved; generic prose and booleans must not redefine the relation.

Useful payloads:

| Kind | Payload and exact meaning |
| --- | --- |
| lexical_alias_initializer | destination declaration identity, source operand ID, initialization location; the destination receives the source's value at that initialization if it completes normally. Const protects the binding cell, not the referent or a separately mutable source cell. |
| ordered_object_construction | construction expression ID, ordered parts `(spread operand / explicit static data property)`, explicit-key coverage; proves a new literal and its source parts, without asserting whole shape or copied slot contents. |
| conditional_member_set_attempt | condition operand, consequent/alternative event IDs, target SourcePath, RHS expression ID, assignment operator; proves the selected branch contains a Set attempt. An omitted alternative contains no direct Set attempt from this statement. |
| explicit_member_set_attempt | target SourcePath, RHS expression ID, assignment operator; proves source evaluation attempts Set after evaluating receiver and RHS. Successful mutation and setter/Proxy effects remain unknown. |
| normal_prefix_program_order | predecessor/successor event IDs, owning statement-block evidence, control-path guards, order `before_if_both_reached_normally`; do not obtain cross-branch order from byte offsets alone. |
| actual_argument_formal_binding | authenticated edge ID, argument expression ID/index, actual target definition/formal evidence/index; proves the selected syntactic argument maps to the selected formal position, without proving activation or argument property contents. |
| body_return_reaching_binding_reference | return evidence, operand SourcePath with empty member path, binding-read phase; identifies the *current reaching lexical binding read*, not the entry parameter's original value. |
| body_return_ordered_copy_structure | return evidence, object-construction relation ID, current reaching spread operands, subsequent explicit keys; proves copy construction form, separately from model-dependent current-source copy preservation and async fulfillment. |
| selected_key_direct_write_scan | finite scope evidence, receiver SourcePath, selected suffix, complete scan flag, exact matching/static/dynamic/update/delete event IDs, verdict; proves only the explicitly specified source-target scan. |

The negative scan must name its scope precisely: selected outer function's direct source prefix up to the chosen sink, excluding nested function/class bodies and all unexpanded callee bodies. `no_explicit_static_target_match` is a safe narrow verdict only when that scoped enumeration is complete. If a dynamic target can match, report it and use `unknown_selected_target_match` for any stronger direct-write exclusion. Never label this `own_key_untouched`, `no_mutation`, `selected_field_absent`, or `preserved`.

## What the two real functions can safely expose

For `enqueue`, the source-only relation chain can extract:

1. The `normalizedInput` literal starts with `...input`, then writes `projectId`, `sourcePath`, `sessionId`, `workerId`, `cwd`, and `executionBoundary`. Its explicit properties do not name `metadata`.
2. `if (!normalizedInput.metadata) normalizedInput.metadata = {}` is a conditional root-member Set attempt. The truthy continuation has no replacement attempt from this statement. Neither branch alone proves the current metadata referent equals the originally copied child.
3. The source then attempts Set at `metadata.acpProfile`, `metadata.uiLane`, and `metadata.uiLaneReason`, in that order. Their actual RHS forms are respectively `old || "headless"`, `Boolean(old)`, and `old || ""`. A named `Boolean` call must retain its actual binding/environment identity; its name is not a builtin-semantics proof.
4. The UI-profile guard has an explicit throw branch. The sink's normal continuation follows its non-throw branch; this is not proof that an arbitrary request reaches the sink.
5. The actual `normalizedInput.metadata` argument occupies position 3 at the authenticated `resolveAgentsForEntry` call, mapping to its actual metadata formal.
6. In this prefix there is no direct explicit static assignment target `normalizedInput.metadata.maxRetries`. The three other field Sets, prior helper calls, property accesses, and source-object aliases may affect it indirectly. The fact also does not establish that an own `maxRetries` slot exists.

A useful display is “source structure proved; selected current field relation unknown,” with the two metadata branch alternatives, the three ordered Set attempts, the actual argument/formal link, and preserved barriers. The current unknown selected assessments are not a reason to hide these independent proved relations.

For `resolveAgentsForEntry`:

1. `const metadataRecord = metadata` is an authenticated alias initializer. It stores the current metadata value at that point; metadataRecord's immutable cell does not freeze its referent and does not freeze the mutable metadata parameter cell.
2. The first return operand is a uniquely resolved read of the current reaching `metadata` parameter binding on the guard's then branch.
3. The second return constructs a new literal with ordered parts `...metadata`, then `agents`, then `agent`, on the guard's else continuation. The explicit final keys do not name `maxRetries`; this is source construction form, not proof of the current source's copy surface or selected slot.
4. Both facts belong to body-return expression evaluation before async Promise assimilation. The overall async call and caller `await` keep their separate unknown completion/thenable facts. Do not connect the body-return source operand directly to the caller's `resolvedMeta` runtime value.

## Integration in formal outputs

Generate these relations in core from `SemanticSources` and `LexicalBindings`; never prefill target symbol/key/sequence knowledge in policies or a report collector. The existing parameter/field/sink locators select the query. Generic operations derive intermediate declarations, keys, guards, object parts, returns, and call positions from saved source.

Attach per-site relation IDs and independently computed relation coverage to the ordinary field assessments. Keep a single summary-level operand/relation table to avoid multiplying the same source fact across branch contexts. Relation IDs must include applicable branch guards. Reuse the existing guard mechanism where possible; do not treat its `truth_proven: false` as an established runtime truth.

Suggested additional output:

```json
{
  "source_relation_summary": {
    "version": "captured-field-source-relations-1",
    "proof_domain": "captured_ast_and_lexical_binding",
    "operands": [],
    "relations": [],
    "coverage": {
      "selected_site_count": 0,
      "accounted_selected_site_count": 0,
      "direct_prefix_scan_complete": false,
      "budget_exhausted": false
    },
    "selected_heap_projection_upgraded": false,
    "runtime_value_verified": false,
    "promise_fulfillment_proven": false
  }
}
```

The zeros/empty arrays above are schema placeholders, not observed target results. Coverage should be computed over actual selected sites, including each branch context and each direct return. Unsupported syntax, parser/source/binding failures, budgets, omitted prefixes, and unaccounted selected sites block relevant coverage claims. Independent positive source facts can survive an unrelated IR heap barrier; complete negative source scans need complete scoped enumeration.

`field_analysis._finding` should include relation graph/edge IDs and counts in formal evidence and metadata while retaining its uncertain finding status and existing selected-field closure counts. Count relations by kind/status separately from source-form relation counts. Compact report generation should expose source-relation kind/status, phase, branch guards, critical operand targets, and the current IR unknown alongside it.

In the goal ledger, add artifact/hash/JSON-pointer witnesses for these automatically saved relations under `CPB-01.P3` (normalization/intermediate fields), with actual argument/formal relation as narrowly relevant to assembly as well. Use `source-derived` provenance for the AST/binding facts, `trusted-model` only for actual Copy/Get or control-model premises, `policy-declared` for the unchanged rule locators/contract, and `unresolved` for effect/current-value/async/transport gaps. The new facts support a local portion of P3; scheduler, new/existing selection, assignment, JSON/inbox/direct-broker transport, and complete field origin remain unclosed.

Keep five goals / thirty required obligations, the original rule policies, and frozen observation denominators unchanged. No source relation count, display improvement, or schema completeness can make the full goal/obligation complete. This design note must remain outside the automatic witness inventory.
