# 交付 Evidence：实际字段与条件盘点

本视图只复制正常报告保存的生产源码操作，`presentation_only=true`；没有增加判定。完整报告：`winwincode-delivery-evidence-contract-report.json`。
正常源码延续、调用成功、字段运行值、角色权限和 Runtime 真实性互相独立；此盘点不证明后四项。
完整操作、source hash、源码位置与 evidence 引用均保留在每个 JSON pointer。

## resolve_production_verdict · 源退出条件

来源：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:221`；`/architecture/responsibility_explanations/operations/24`。

- 条件：`!roles.insert(resolved.role)`。
- 退出形式：`Err_return`；`Err(error("durable verification repeats one current role"))`。
- 保存边界：`guard_truth_or_rejection_observed=false`；`return_is_error_or_business_rejection_proven=false`。

## resolve_production_verdict · 源退出条件

来源：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:231`；`/architecture/responsibility_explanations/operations/44`。

- 条件：`roles.len() != required_roles.len()         &amp;#124;&amp;#124; required_roles.iter().any(&amp;#124;role&amp;#124; !roles.contains(role))`。
- 退出形式：`Err_return`；`Err(error(             "durable verification does not contain every exact current role",         ))`。
- 保存边界：`guard_truth_or_rejection_observed=false`；`return_is_error_or_business_rejection_proven=false`。

## resolve_production_verdict · VerificationFacts

来源：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:241`；`/architecture/responsibility_explanations/operations/66`。

| 实际字段 | 捕获初始化来源 |
|---|---|
| required_roles | required_roles |
| sessions | sessions |

保存边界：`closed_captured_shape=true`，`runtime_field_presence_or_value_proven=false`。

## resolve_production_verdict · ResolveDeliveryEvidenceInput

来源：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:258`；`/architecture/responsibility_explanations/operations/81`。

| 实际字段 | 捕获初始化来源 |
|---|---|
| work_run_id | candidate.producer_work_run_id().clone() |
| session_binding_id | candidate.producer_session_binding_id().clone() |
| source | EvidenceSource::CandidateCommit |
| created_at_millis | produced_at_millis |

保存边界：`closed_captured_shape=true`，`runtime_field_presence_or_value_proven=false`。

## resolve_production_verdict · ProductionVerdictFacts

来源：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:270`；`/architecture/responsibility_explanations/operations/102`。

| 实际字段 | 捕获初始化来源 |
|---|---|
| candidate | candidate |
| verification | verification |
| evidence | evidence |
| produced_at_millis | produced_at_millis |

保存边界：`closed_captured_shape=true`，`runtime_field_presence_or_value_proven=false`。

## resolve_verification_runtime · ResolvedVerificationRuntime

来源：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:335`；`/architecture/responsibility_explanations/operations/165`。

| 实际字段 | 捕获初始化来源 |
|---|---|
| role | role |
| session | VerificationSessionFacts {             role,             work_run_id: binding.work_run_id.clone(),             session_binding_id: binding.id.clone(),             workspace_mode: VerificationWorkspaceMode::CandidateReadOnly,             permission_profile: VerificationPermissionProfile::CandidateReadOnlyRestricted,             pre_candidate_snapshot: Some(snapshot.clone()),         |
| evidence | evidence |
| finished_at_millis | verified_terminal.finished_at_millis() |

保存边界：`closed_captured_shape=true`，`runtime_field_presence_or_value_proven=false`。

## resolve_verification_runtime · VerificationSessionFacts

来源：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:337`；`/architecture/responsibility_explanations/operations/167`。

| 实际字段 | 捕获初始化来源 |
|---|---|
| role | role |
| work_run_id | binding.work_run_id.clone() |
| session_binding_id | binding.id.clone() |
| workspace_mode | VerificationWorkspaceMode::CandidateReadOnly |
| permission_profile | VerificationPermissionProfile::CandidateReadOnlyRestricted |
| pre_candidate_snapshot | Some(snapshot.clone()) |
| post_candidate_snapshot | Some(snapshot) |
| accepted_job_outcome | Some(terminal) |
| codex_turn_completed | true |
| mutation_records | Vec::new() |
| findings | findings |

保存边界：`closed_captured_shape=true`，`runtime_field_presence_or_value_proven=false`。

## resolve_findings · 源退出条件

来源：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:579`；`/architecture/responsibility_explanations/operations/197`。

- 条件：`!criterion_ids.insert(criterion_id.clone())`。
- 退出形式：`Err_return`；`Err(error("verification result repeats one criterion"))`。
- 保存边界：`guard_truth_or_rejection_observed=false`；`return_is_error_or_business_rejection_proven=false`。

## resolve_findings · 源退出条件

来源：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:585`；`/architecture/responsibility_explanations/operations/203`。

- 条件：`StructuredVerdict::Inconclusive &amp;#124; StructuredVerdict::InfraError`。
- 退出形式：`Err_return`；`Err(error(                     "a successful verification terminal must report pass or fail findings",                 ))`。
- 保存边界：`guard_truth_or_rejection_observed=false`；`return_is_error_or_business_rejection_proven=false`。

## resolve_findings · 源退出条件

来源：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:591`；`/architecture/responsibility_explanations/operations/209`。

- 条件：`finding.evidence_sources.is_empty()`。
- 退出形式：`Err_return`；`Err(error("verification finding has no direct Evidence source"))`。
- 保存边界：`guard_truth_or_rejection_observed=false`；`return_is_error_or_business_rejection_proven=false`。

## resolve_findings · 源退出条件

来源：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:598`；`/architecture/responsibility_explanations/operations/224`。

- 条件：`source_event.sequence &gt;= result.event.sequence`。
- 退出形式：`Err_return`；`Err(error(                     "verification finding Evidence must precede its structured result",                 ))`。
- 保存边界：`guard_truth_or_rejection_observed=false`；`return_is_error_or_business_rejection_proven=false`。

## resolve_findings · ResolveDeliveryEvidenceInput

来源：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:625`；`/architecture/responsibility_explanations/operations/259`。

| 实际字段 | 捕获初始化来源 |
|---|---|
| work_run_id | terminal.work_run_id().clone() |
| session_binding_id | session_binding_id.clone() |
| source | EvidenceSource::Runtime {                             evidence_type: source.evidence_type,                             source_event_id: source.event_id.clone(),                             accepted_sources: std::slice::from_ref(&amp;accepted),                             terminal,                             checkout,                         } |
| created_at_millis | created_at_millis |

保存边界：`closed_captured_shape=true`，`runtime_field_presence_or_value_proven=false`。

## resolve_findings · EvidenceSource::Runtime

来源：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:628`；`/architecture/responsibility_explanations/operations/264`。

| 实际字段 | 捕获初始化来源 |
|---|---|
| evidence_type | source.evidence_type |
| source_event_id | source.event_id.clone() |
| accepted_sources | std::slice::from_ref(&amp;accepted) |
| terminal | terminal |
| checkout | checkout |

保存边界：`closed_captured_shape=true`，`runtime_field_presence_or_value_proven=false`。

## resolve_findings · VerificationFindingFact

来源：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:647`；`/architecture/responsibility_explanations/operations/286`。

| 实际字段 | 捕获初始化来源 |
|---|---|
| finding_ref | finding.finding_id |
| criterion_id | AcceptanceCriterionId::new(criterion_id)                 .map_err(&amp;#124;error_value&amp;#124; resolution_error(&amp;error_value))? |
| conclusion | conclusion |
| result_sequence | ExecutionSequence(                 i64::try_from(result.event.sequence)                     .map_err(&amp;#124;_&amp;#124; error("verification result sequence exceeds the durable range"))?,             ) |
| source_refs | source_refs |
| source_sequences | source_sequences |
| explanation | finding.explanation |

保存边界：`closed_captured_shape=true`，`runtime_field_presence_or_value_proven=false`。

## exact_source_event · 源退出条件

来源：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:675`；`/architecture/responsibility_explanations/operations/312`。

- 条件：`matching.next().is_some()`。
- 退出形式：`Err_return`；`Err(error(             "verification finding Evidence source identity is ambiguous",         ))`。
- 保存边界：`guard_truth_or_rejection_observed=false`；`return_is_error_or_business_rejection_proven=false`。

## required_roles · 源退出条件

来源：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:779`；`/architecture/responsibility_explanations/operations/323`。

- 条件：`!matches!(         roles.as_slice(),         [VerificationRole::Reviewer, VerificationRole::Verifier]             &amp;#124; [                 VerificationRole::Reviewer,                 VerificationRole::Verifier,                 VerificationRole::AdversarialVerifier             ]     )`。
- 退出形式：`Err_return`；`Err(error(             "durable verification does not contain the canonical verification roles",         ))`。
- 保存边界：`guard_truth_or_rejection_observed=false`；`return_is_error_or_business_rejection_proven=false`。

## checkout_attestation_from_snapshot · ValidatedCheckoutAttestationFact

来源：`crates/winwincode-delivery/src/domain/evidence.rs:135`；`/architecture/responsibility_explanations/operations/329`。

| 实际字段 | 捕获初始化来源 |
|---|---|
| product_session_id | terminal.product_session_id().clone() |
| execution_job_id | terminal.execution_job_id().clone() |
| work_run_id | terminal.work_run_id().clone() |
| role_id | terminal.role_id().into() |
| attempt | terminal.attempt() |
| lease_id | terminal.lease_id().clone() |
| fencing_token | terminal.fencing_token().clone() |
| worker_id | terminal.worker_id().clone() |
| worker_instance_id | terminal.worker_instance_id().clone() |
| worker_session_id | terminal.worker_session_id().clone() |
| codex_thread_id | terminal.codex_thread_id().clone() |
| repository | snapshot.repository().clone() |
| checkout_commit_id | snapshot.candidate_commit_id().into() |
| checkout_tree_id | snapshot.candidate_tree_id().into() |

保存边界：`closed_captured_shape=true`，`runtime_field_presence_or_value_proven=false`。

## accepted_runtime_source · AcceptedRuntimeSourceFact

来源：`crates/winwincode-delivery/src/domain/evidence.rs:164`；`/architecture/responsibility_explanations/operations/357`。

| 实际字段 | 捕获初始化来源 |
|---|---|
| source_event_id | source_event_id |
| evidence_type | evidence_type |
| product_session_id | terminal.product_session_id().clone() |
| execution_job_id | terminal.execution_job_id().clone() |
| worker_session_id | terminal.worker_session_id().clone() |
| codex_thread_id | terminal.codex_thread_id().clone() |
| work_run_id | terminal.work_run_id().clone() |
| role_id | terminal.role_id().into() |
| attempt | terminal.attempt() |
| lease_id | terminal.lease_id().clone() |
| fencing_token | terminal.fencing_token().clone() |
| worker_id | terminal.worker_id().clone() |
| worker_instance_id | terminal.worker_instance_id().clone() |
| source_sequence | source_sequence |
| candidate_ref | candidate.candidate_ref().into() |
| occurred_at_millis | occurred_at_millis |
| outcome | outcome |
| command_digest | command_digest |

保存边界：`closed_captured_shape=true`，`runtime_field_presence_or_value_proven=false`。

## resolve_delivery_evidence · EvidenceIdentity

来源：`crates/winwincode-delivery/src/domain/evidence.rs:458`；`/architecture/responsibility_explanations/operations/416`。

| 实际字段 | 捕获初始化来源 |
|---|---|
| delivery_id | delivery.id() |
| delivery_spec_id | &amp;delivery.snapshot().spec.id |
| delivery_spec_revision | delivery.snapshot().spec.revision |
| candidate_ref | candidate.candidate_ref() |
| work_run_id | &amp;work_run.id |
| session_binding_id | &amp;binding.id |
| evidence_type | source.evidence_type |
| source_ref | &amp;source.source_ref |
| source_identity | &amp;source.identity |

保存边界：`closed_captured_shape=true`，`runtime_field_presence_or_value_proven=false`。

## resolve_delivery_evidence · EvidenceRef

来源：`crates/winwincode-delivery/src/domain/evidence.rs:469`；`/architecture/responsibility_explanations/operations/428`。

| 实际字段 | 捕获初始化来源 |
|---|---|
| schema_version | super::DELIVERY_SCHEMA_VERSION |
| id | evidence_id |
| delivery_id | delivery.id().clone() |
| delivery_spec_id | delivery.snapshot().spec.id.clone() |
| delivery_spec_revision | delivery.snapshot().spec.revision |
| work_run_id | work_run.id.clone() |
| session_binding_id | binding.id.clone() |
| candidate_ref | candidate.candidate_ref().into() |
| evidence_type | source.evidence_type |
| source_ref | source.source_ref |
| created_at_millis | input.created_at_millis |

保存边界：`closed_captured_shape=true`，`runtime_field_presence_or_value_proven=false`。

## resolve_delivery_evidence · ResolvedDeliveryEvidence

来源：`crates/winwincode-delivery/src/domain/evidence.rs:489`；`/architecture/responsibility_explanations/operations/453`。

| 实际字段 | 捕获初始化来源 |
|---|---|
| evidence | evidence |
| outcome | source.outcome |
| source_identity | source.identity |

保存边界：`closed_captured_shape=true`，`runtime_field_presence_or_value_proven=false`。

## resolve_direct_candidate_source · ResolvedEvidenceSource

来源：`crates/winwincode-delivery/src/domain/evidence.rs:547`；`/architecture/responsibility_explanations/operations/464`。

| 实际字段 | 捕获初始化来源 |
|---|---|
| evidence_type | EvidenceRefType::Commit |
| source_ref | format!("git_commit:{}", candidate.candidate_commit_id()) |
| outcome | VerifiedEvidenceOutcome::Observed |
| identity | VerifiedEvidenceSourceIdentity::CandidateCommit {                 candidate_ref: candidate.candidate_ref().into(),                 candidate_commit_id: candidate.candidate_commit_id().into(),             } |

保存边界：`closed_captured_shape=true`，`runtime_field_presence_or_value_proven=false`。

## resolve_direct_candidate_source · VerifiedEvidenceSourceIdentity::CandidateCommit

来源：`crates/winwincode-delivery/src/domain/evidence.rs:551`；`/architecture/responsibility_explanations/operations/465`。

| 实际字段 | 捕获初始化来源 |
|---|---|
| candidate_ref | candidate.candidate_ref().into() |
| candidate_commit_id | candidate.candidate_commit_id().into() |

保存边界：`closed_captured_shape=true`，`runtime_field_presence_or_value_proven=false`。

## resolve_direct_candidate_source · ResolvedEvidenceSource

来源：`crates/winwincode-delivery/src/domain/evidence.rs:556`；`/architecture/responsibility_explanations/operations/471`。

| 实际字段 | 捕获初始化来源 |
|---|---|
| evidence_type | EvidenceRefType::Diff |
| source_ref | format!("git_diff:sha256:{}", candidate.diff_sha256()) |
| outcome | VerifiedEvidenceOutcome::Observed |
| identity | VerifiedEvidenceSourceIdentity::CandidateDiff {                 candidate_ref: candidate.candidate_ref().into(),                 diff_sha256: candidate.diff_sha256().into(),             } |

保存边界：`closed_captured_shape=true`，`runtime_field_presence_or_value_proven=false`。

## resolve_direct_candidate_source · VerifiedEvidenceSourceIdentity::CandidateDiff

来源：`crates/winwincode-delivery/src/domain/evidence.rs:560`；`/architecture/responsibility_explanations/operations/472`。

| 实际字段 | 捕获初始化来源 |
|---|---|
| candidate_ref | candidate.candidate_ref().into() |
| diff_sha256 | candidate.diff_sha256().into() |

保存边界：`closed_captured_shape=true`，`runtime_field_presence_or_value_proven=false`。

## resolve_runtime_source · 源退出条件

来源：`crates/winwincode-delivery/src/domain/evidence.rs:755`；`/architecture/responsibility_explanations/operations/482`。

- 条件：`evidence_type == EvidenceRefType::PullRequest`。
- 退出形式：`Err_return`；`Err(resolution_error(             EvidenceResolutionErrorCode::InvalidEvidence,             "runtime evidence type is unsupported",         ))`。
- 保存边界：`guard_truth_or_rejection_observed=false`；`return_is_error_or_business_rejection_proven=false`。

## resolve_runtime_source · 源退出条件

来源：`crates/winwincode-delivery/src/domain/evidence.rs:779`；`/architecture/responsibility_explanations/operations/510`。

- 条件：`matches.is_empty()`。
- 退出形式：`Err_return`；`Err(resolution_error(             EvidenceResolutionErrorCode::SourceMissing,             "accepted runtime evidence source position is missing",         ))`。
- 保存边界：`guard_truth_or_rejection_observed=false`；`return_is_error_or_business_rejection_proven=false`。

## resolve_runtime_source · 源退出条件

来源：`crates/winwincode-delivery/src/domain/evidence.rs:785`；`/architecture/responsibility_explanations/operations/517`。

- 条件：`matches.len() != 1`。
- 退出形式：`Err_return`；`Err(resolution_error(             EvidenceResolutionErrorCode::SourceAmbiguous,             "accepted runtime evidence source position occurs more than once",         ))`。
- 保存边界：`guard_truth_or_rejection_observed=false`；`return_is_error_or_business_rejection_proven=false`。

## resolve_runtime_source · 源退出条件

来源：`crates/winwincode-delivery/src/domain/evidence.rs:792`；`/architecture/responsibility_explanations/operations/526`。

- 条件：`runtime_source_identity(fact) != expected_identity`。
- 退出形式：`Err_return`；`Err(resolution_error(             EvidenceResolutionErrorCode::SessionMismatch,             "runtime source belongs to another product, job, worker, thread, stage, or role",         ))`。
- 保存边界：`guard_truth_or_rejection_observed=false`；`return_is_error_or_business_rejection_proven=false`。

## resolve_runtime_source · 源退出条件

来源：`crates/winwincode-delivery/src/domain/evidence.rs:798`；`/architecture/responsibility_explanations/operations/531`。

- 条件：`fact.evidence_type != evidence_type`。
- 退出形式：`Err_return`；`Err(resolution_error(             EvidenceResolutionErrorCode::TypeMismatch,             "runtime source type does not match the requested Evidence type",         ))`。
- 保存边界：`guard_truth_or_rejection_observed=false`；`return_is_error_or_business_rejection_proven=false`。

## resolve_runtime_source · 源退出条件

来源：`crates/winwincode-delivery/src/domain/evidence.rs:804`；`/architecture/responsibility_explanations/operations/538`。

- 条件：`fact.candidate_ref != candidate.candidate_ref()`。
- 退出形式：`Err_return`；`Err(resolution_error(             EvidenceResolutionErrorCode::CandidateMismatch,             "runtime source belongs to another frozen candidate",         ))`。
- 保存边界：`guard_truth_or_rejection_observed=false`；`return_is_error_or_business_rejection_proven=false`。

## resolve_runtime_source · ResolvedEvidenceSource

来源：`crates/winwincode-delivery/src/domain/evidence.rs:823`；`/architecture/responsibility_explanations/operations/560`。

| 实际字段 | 捕获初始化来源 |
|---|---|
| evidence_type | evidence_type |
| source_ref | source_ref |
| outcome | fact.outcome |
| identity | VerifiedEvidenceSourceIdentity::Runtime(Box::new(             VerifiedRuntimeEvidenceSourceIdentity {                 execution: expected_identity,                 source_sequence: fact.source_sequence,                 terminal_last_event_sequence: accepted_terminal_sequence(terminal),                 candidate_ref: fact.candidate_ref.clone(),                 checkout_commit_id: ch |

保存边界：`closed_captured_shape=true`，`runtime_field_presence_or_value_proven=false`。

## resolve_runtime_source · VerifiedRuntimeEvidenceSourceIdentity

来源：`crates/winwincode-delivery/src/domain/evidence.rs:828`；`/architecture/responsibility_explanations/operations/566`。

| 实际字段 | 捕获初始化来源 |
|---|---|
| execution | expected_identity |
| source_sequence | fact.source_sequence |
| terminal_last_event_sequence | accepted_terminal_sequence(terminal) |
| candidate_ref | fact.candidate_ref.clone() |
| checkout_commit_id | checkout.checkout_commit_id.clone() |
| checkout_tree_id | checkout.checkout_tree_id.clone() |
| command_digest | fact.command_digest.clone() |

保存边界：`closed_captured_shape=true`，`runtime_field_presence_or_value_proven=false`。

## validate_runtime_terminal · 源退出条件

来源：`crates/winwincode-delivery/src/domain/evidence.rs:860`；`/architecture/responsibility_explanations/operations/594`。

- 条件：`terminal.product_session_id() != &amp;binding.product_session_id         &amp;#124;&amp;#124; terminal.execution_job_id() != &amp;binding.execution_job_id         &amp;#124;&amp;#124; terminal.worker_session_id() != worker_session_id         &amp;#124;&amp;#124; terminal.codex_thread_id() != codex_thread_id         &amp;#124;&amp;#124; terminal.work_run_id() != &amp;work_run.id         &amp;#124;&amp;#124; terminal.attempt() != u64::try_from(work_run.attempt).unwrap_or(0)`。
- 退出形式：`Err_return`；`Err(resolution_error(             EvidenceResolutionErrorCode::SessionMismatch,             "runtime terminal result belongs to another product, job, worker, thread, stage, or role",         ))`。
- 保存边界：`guard_truth_or_rejection_observed=false`；`return_is_error_or_business_rejection_proven=false`。

## validate_runtime_terminal · 源退出条件

来源：`crates/winwincode-delivery/src/domain/evidence.rs:866`；`/architecture/responsibility_explanations/operations/602`。

- 条件：`terminal.terminal_candidate_tree_id() != candidate.candidate_tree_id()`。
- 退出形式：`Err_return`；`Err(resolution_error(             EvidenceResolutionErrorCode::CandidateMismatch,             "runtime terminal result belongs to another candidate tree",         ))`。
- 保存边界：`guard_truth_or_rejection_observed=false`；`return_is_error_or_business_rejection_proven=false`。

## validate_runtime_terminal · 源退出条件

来源：`crates/winwincode-delivery/src/domain/evidence.rs:878`；`/architecture/responsibility_explanations/operations/614`。

- 条件：`terminal_sequence == 0         &amp;#124;&amp;#124; terminal_sequence &gt; MAX_SAFE_INTEGER         &amp;#124;&amp;#124; terminal.finished_at_millis() &gt; MAX_SAFE_INTEGER         &amp;#124;&amp;#124; terminal.finished_at_millis() &lt; binding.bound_at_millis         &amp;#124;&amp;#124; evidence_created_at_millis &lt; terminal.finished_at_millis()`。
- 退出形式：`Err_return`；`Err(resolution_error(             EvidenceResolutionErrorCode::SourceTimeMismatch,             "runtime terminal result must close this WorkRun before Evidence is created",         ))`。
- 保存边界：`guard_truth_or_rejection_observed=false`；`return_is_error_or_business_rejection_proven=false`。

## validate_runtime_terminal · FencedExecutionIdentity

来源：`crates/winwincode-delivery/src/domain/evidence.rs:883`；`/architecture/responsibility_explanations/operations/621`。

| 实际字段 | 捕获初始化来源 |
|---|---|
| product_session_id | terminal.product_session_id().clone() |
| execution_job_id | terminal.execution_job_id().clone() |
| work_run_id | terminal.work_run_id().clone() |
| role_id | terminal.role_id().into() |
| attempt | terminal.attempt() |
| lease_id | terminal.lease_id().clone() |
| fencing_token | terminal.fencing_token().clone() |
| worker_id | terminal.worker_id().clone() |
| worker_instance_id | terminal.worker_instance_id().clone() |
| worker_session_id | terminal.worker_session_id().clone() |
| codex_thread_id | terminal.codex_thread_id().clone() |

保存边界：`closed_captured_shape=true`，`runtime_field_presence_or_value_proven=false`。

## validate_checkout_attestation · 源退出条件

来源：`crates/winwincode-delivery/src/domain/evidence.rs:904`；`/architecture/responsibility_explanations/operations/644`。

- 条件：`checkout_identity(checkout) != *expected_identity`。
- 退出形式：`Err_return`；`Err(resolution_error(             EvidenceResolutionErrorCode::SessionMismatch,             "checkout attestation belongs to another fenced execution",         ))`。
- 保存边界：`guard_truth_or_rejection_observed=false`；`return_is_error_or_business_rejection_proven=false`。

## validate_checkout_attestation · 源退出条件

来源：`crates/winwincode-delivery/src/domain/evidence.rs:913`；`/architecture/responsibility_explanations/operations/653`。

- 条件：`checkout.repository != *candidate.repository()         &amp;#124;&amp;#124; checkout.checkout_commit_id != candidate.candidate_commit_id()         &amp;#124;&amp;#124; checkout.checkout_tree_id != candidate.candidate_tree_id()`。
- 退出形式：`Err_return`；`Err(resolution_error(             EvidenceResolutionErrorCode::CandidateMismatch,             "runtime source did not execute from the frozen candidate checkout",         ))`。
- 保存边界：`guard_truth_or_rejection_observed=false`；`return_is_error_or_business_rejection_proven=false`。

## runtime_source_identity · FencedExecutionIdentity

来源：`crates/winwincode-delivery/src/domain/evidence.rs:922`；`/architecture/responsibility_explanations/operations/660`。

| 实际字段 | 捕获初始化来源 |
|---|---|
| product_session_id | fact.product_session_id.clone() |
| execution_job_id | fact.execution_job_id.clone() |
| work_run_id | fact.work_run_id.clone() |
| role_id | fact.role_id.clone() |
| attempt | fact.attempt |
| lease_id | fact.lease_id.clone() |
| fencing_token | fact.fencing_token.clone() |
| worker_id | fact.worker_id.clone() |
| worker_instance_id | fact.worker_instance_id.clone() |
| worker_session_id | fact.worker_session_id.clone() |
| codex_thread_id | fact.codex_thread_id.clone() |

保存边界：`closed_captured_shape=true`，`runtime_field_presence_or_value_proven=false`。

