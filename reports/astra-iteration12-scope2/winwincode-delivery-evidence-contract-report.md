# WinWinCode / 项目源码静态调用核对：自动静态分析报告

快照：`cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2`；仅使用保存源码、图和静态分析证据，未执行目标、测试或构建。

## 主要发现

此快照没有配置完整条件判断；不从结构规模推断功能正确。

原始完整 JSON 保留所有条件、反证、未知项、source facts 和保存发现身份。以下限制仅影响展示，不改变分析结果。

## 具体职责与接口交接

以下正文由所选声明的实际记录字段、赋值、实参接口和提前退出条件生成。目录名只供导航；普通调用、消息字段、执行、交付和投影分别保留。

完整职责、所有操作和来源：`/architecture/responsibility_explanations`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::resolve_production_verdict`

构造捕获记录，字段按源码次序为「work_run_id ← candidate.producer_work_run_id().clone()；session_binding_id ← candidate.producer_session_binding_id().clone()；source ← EvidenceSource::CandidateCommit；created_at_millis ← produced_at_millis」。不据构造形式推断物理持久化。 将「ResolveDeliveryEvidenceInput {\n            work_run_id: candidate.producer_work_run_id().clone(),\n            session_binding_id: candidate.producer_session_binding_id().clone(),\n            source: EvidenceSource::CandidateCommit,\n            created_at_millis: produced_at_millis,\n        }」作为第 3 个实参交给已绑定接口「rust:crates/winwincode-delivery/src/domain/evidence#resolve_delivery_evidence」，对应捕获形参「input: ResolveDeliveryEvidenceInput&lt;'_&gt;」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「resolved」的初始化来源为「resolve_verification_runtime(delivery, &amp;candidate, &amp;runtime)?」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「produced_at_millis」存在源更新「produced_at_millis = produced_at_millis.max(resolved.finished_at_millis)」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「!roles.insert(resolved.role)」的捕获提前退出分支为「Err_return：Err(error("durable verification repeats one current role"))」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(error("durable verification repeats one current role"))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「required_roles」关联路径「required_roles」；只描述捕获来源，不证明当时的字段值。 将「delivery」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-delivery/src/domain/candidate/verdict_authority#resolve_verification_runtime」，对应捕获形参「delivery: &amp;Delivery」。该普通调用关系不替代进程或网络协议关系。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:206`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/0`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@212:18&gt;`

在调用形式「resolution_error」中提供第 1 个实参「&amp;error_value」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:212`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/1`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@229:38&gt;`

在调用形式「roles.contains」中提供第 1 个实参「role」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:229`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/2`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@235:26&gt;`

在调用形式「role_order」中提供第 1 个实参「session.role」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:235`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/3`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@236:22&gt;`

在调用形式「left.evidence().id.0.cmp」中提供第 1 个实参「&amp;right.evidence().id.0」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:236`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/4`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@237:23&gt;`

以无显式实参的调用形式「left.evidence」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:237`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/5`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@246:14&gt;`

在调用形式「resolution_error」中提供第 1 个实参「&amp;error_value」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:246`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/6`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@249:21&gt;`

在调用形式「error」中提供第 1 个实参「"verdict production time exceeds the durable range"」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:249`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/7`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@265:14&gt;`

在调用形式「error」中提供第 1 个实参「error_value.to_string()」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:265`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/8`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@267:22&gt;`

在调用形式「left.evidence().id.0.cmp」中提供第 1 个实参「&amp;right.evidence().id.0」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:267`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/9`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@268:23&gt;`

以无显式实参的调用形式「left.evidence」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:268`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/10`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::resolve_verification_runtime`

构造捕获记录，字段按源码次序为「role ← role；work_run_id ← binding.work_run_id.clone()；session_binding_id ← binding.id.clone()；workspace_mode ← VerificationWorkspaceMode::CandidateReadOnly；permission_profile ← VerificationPermissionProfile::CandidateReadOnlyRestricted；pre_candidate_snapshot ← Some(snapshot.clone())；post_candidate_snapshot ← Some(snapshot)；accepted_job_outcome ← Some(terminal)；codex_turn_completed ← true；mutation_records ← Vec::new()；findings ← findings」。不据构造形式推断物理持久化。 将「&amp;terminal」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-delivery/src/domain/evidence#checkout_attestation_from_snapshot」，对应捕获形参「terminal: &amp;AcceptedVerificationJobOutcomeFact」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「role」的初始化来源为「runtime.role」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以字段投影形式「role」关联路径「role」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「59c30ebc1a8dfe8b31401c29」先于语句位置「1」的操作「57a1c3a30762395ddf1113ce」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「delivery」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-delivery/src/domain/candidate/verdict_authority#resolve_findings」，对应捕获形参「delivery: &amp;Delivery」。该普通调用关系不替代进程或网络协议关系。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:285`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/11`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@295:14&gt;`

在调用形式「resolution_error」中提供第 1 个实参「&amp;error_value」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:295`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/12`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@301:15&gt;`

以无显式实参的调用形式「verified_terminal.execution_job_id」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:301`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/13`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@306:21&gt;`

在调用形式「error」中提供第 1 个实参「"verification terminal SessionBinding is missing"」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:306`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/14`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@320:14&gt;`

在调用形式「resolution_error」中提供第 1 个实参「&amp;error_value」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:320`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/15`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::resolve_findings`

构造捕获记录，字段按源码次序为「finding_ref ← finding.finding_id；criterion_id ← AcceptanceCriterionId::new(criterion_id)\n                .map_err(|error_value| resolution_error(&amp;error_value))?；conclusion ← conclusion；result_sequence ← ExecutionSequence(\n                i64::try_from(result.event.sequence)\n                    .map_err(|_| error("verification result sequence exceeds the durab…［展示截断；完整操作保留］；source_refs ← source_refs；source_sequences ← source_sequences；explanation ← finding.explanation」。不据构造形式推断物理持久化。 将「"verification result repeats one criterion"」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-delivery/src/domain/candidate/verdict_authority#error」，对应捕获形参「message: impl Into&lt;String&gt;」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「criterion_id」的初始化来源为「finding\n            .criterion_id\n            .ok_or_else(|| error("verification finding has no current criterion"))?」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「!criterion_ids.insert(criterion_id.clone())」的捕获提前退出分支为「Err_return：Err(error("verification result repeats one criterion"))」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(error("verification result repeats one criterion"))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「session_binding_id.clone()」关联路径「session_binding_id」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「49929b6cf8f4aa1288daf23d」先于语句位置「1」的操作「9a7e5fd81f07468d1089cc96」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:559`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/16`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@577:25&gt;`

在调用形式「error」中提供第 1 个实参「"verification finding has no current criterion"」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:577`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/17`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@621:33&gt;`

在调用形式「error」中提供第 1 个实参「"Evidence time exceeds the durable range"」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:621`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/18`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@638:26&gt;`

在调用形式「error」中提供第 1 个实参「error_value.to_string()」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:638`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/19`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@644:30&gt;`

在调用形式「error」中提供第 1 个实参「"Evidence source sequence exceeds the durable range"」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:644`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/20`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@650:26&gt;`

在调用形式「resolution_error」中提供第 1 个实参「&amp;error_value」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:650`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/21`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@654:30&gt;`

在调用形式「error」中提供第 1 个实参「"verification result sequence exceeds the durable range"」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:654`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/22`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::exact_source_event`

将「"verification finding Evidence source identity is ambiguous"」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-delivery/src/domain/candidate/verdict_authority#error」，对应捕获形参「message: impl Into&lt;String&gt;」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「matching」的初始化来源为「events\n        .iter()\n        .filter(|event| event.event.event_id == *event_id)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「matching.next().is_some()」的捕获提前退出分支为「Err_return：Err(error(\n            "verification finding Evidence source identity is ambiguous",\n        ))」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(error(\n            "verification finding Evidence source identity is ambiguous",\n        ))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「5064e4ac570e9a19e41ee7ab」先于语句位置「1」的操作「b3350b8696f493e4f3a4c0de」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:664`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/23`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@673:21&gt;`

在调用形式「error」中提供第 1 个实参「"verification finding Evidence source is missing"」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:673`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/24`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::required_roles`

在调用形式「Ok」中提供第 1 个实参「roles」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「roles」的初始化来源为「[\n        VerificationRole::Reviewer,\n        VerificationRole::Verifier,\n        VerificationRole::AdversarialVerifier,\n    ]\n    .into_iter()\n    .filter(|role| roles.contains(role))\n    .collect::&lt;Vec&lt;_&gt;&gt;()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「!matches!(\n        roles.as_slice(),\n        [VerificationRole::Reviewer, VerificationRole::Verifier]\n            | [\n                VerificationRole::Reviewer,\n                VerificationRole::Verifier,\n                VerificationRole::AdversarialVerifier\n            ]\n    )」的捕获提前退出分支为「Err_return：Err(error(\n            "durable verification does not contain the canonical verification roles",\n        ))」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(error(\n            "durable verification does not contain the canonical verification roles",\n        ))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「466b7e86f4ee9c37b25277a5」先于语句位置「2」的操作「6fc8b2e2d4ff3a3e02d031a4」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:759`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/25`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@768:13&gt;`

在调用形式「roles.contains」中提供第 1 个实参「role」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:768`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/26`。

### `crates/winwincode-delivery/src/domain/evidence.rs::checkout_attestation_from_snapshot`

构造捕获记录，字段按源码次序为「product_session_id ← terminal.product_session_id().clone()；execution_job_id ← terminal.execution_job_id().clone()；work_run_id ← terminal.work_run_id().clone()；role_id ← terminal.role_id().into()；attempt ← terminal.attempt()；lease_id ← terminal.lease_id().clone()；fencing_token ← terminal.fencing_token().clone()；worker_id ← terminal.worker_id().clone()；worker_instance_id ← terminal.worker_instance_id().clone()；worker_session_id ← terminal.worker_session_id().clone()；codex_thread_id ← terminal.codex_thread_id().clone()；repository ← snapshot.repository().clone()」；其余字段见完整操作。不据构造形式推断物理持久化。 以无显式实参的调用形式「terminal.product_session_id」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-delivery/src/domain/evidence.rs:131`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/27`。

### `crates/winwincode-delivery/src/domain/evidence.rs::accepted_runtime_source`

构造捕获记录，字段按源码次序为「source_event_id ← source_event_id；evidence_type ← evidence_type；product_session_id ← terminal.product_session_id().clone()；execution_job_id ← terminal.execution_job_id().clone()；worker_session_id ← terminal.worker_session_id().clone()；codex_thread_id ← terminal.codex_thread_id().clone()；work_run_id ← terminal.work_run_id().clone()；role_id ← terminal.role_id().into()；attempt ← terminal.attempt()；lease_id ← terminal.lease_id().clone()；fencing_token ← terminal.fencing_token().clone()；worker_id ← terminal.worker_id().clone()」；其余字段见完整操作。不据构造形式推断物理持久化。 以无显式实参的调用形式「terminal.product_session_id().clone」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。 以字段投影形式「source_event_id」关联路径「source_event_id」；只描述捕获来源，不证明当时的字段值。

源码：`crates/winwincode-delivery/src/domain/evidence.rs:154`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/28`。

### `crates/winwincode-delivery/src/domain/evidence.rs::resolve_delivery_evidence`

构造捕获记录，字段按源码次序为「schema_version ← super::DELIVERY_SCHEMA_VERSION；id ← evidence_id；delivery_id ← delivery.id().clone()；delivery_spec_id ← delivery.snapshot().spec.id.clone()；delivery_spec_revision ← delivery.snapshot().spec.revision；work_run_id ← work_run.id.clone()；session_binding_id ← binding.id.clone()；candidate_ref ← candidate.candidate_ref().into()；evidence_type ← source.evidence_type；source_ref ← source.source_ref；created_at_millis ← input.created_at_millis」。不据构造形式推断物理持久化。 将「candidate」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-delivery/src/domain/evidence#resolve_runtime_source」，对应捕获形参「candidate: &amp;FrozenDeliveryCandidate」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「source」的初始化来源为「match &amp;input.source {\n        EvidenceSource::Runtime {\n            evidence_type,\n            source_event_id,\n            accepted_sources,\n            terminal,\n            checkout,\n        } =&gt; resolve_runtime_source(\n            candidate,\n            work_run,\n            binding,\n            *evidence_type,\n            source_event_id,\n …［展示截断；完整操作保留］」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以字段投影形式「input.created_at_millis」关联路径「input.created_at_millis」；只描述捕获来源，不证明当时的字段值。 记录消息形状中的固定文本字段「schema_version」及捕获形式「super::DELIVERY_SCHEMA_VERSION」。单个文本字段不是跨语言调用或传输成功的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「b259dc50ba537b3d124cb595」先于语句位置「1」的操作「a5883af26683f427f06912a1」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「candidate」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-delivery/src/domain/evidence#resolve_direct_candidate_source」，对应捕获形参「candidate: &amp;FrozenDeliveryCandidate」。该普通调用关系不替代进程或网络协议关系。

源码：`crates/winwincode-delivery/src/domain/evidence.rs:417`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/29`。

### `crates/winwincode-delivery/src/domain/evidence.rs::&lt;closure_expression@422:66&gt;`

在调用形式「resolution_error」中提供第 1 个实参「EvidenceResolutionErrorCode::CandidateStale」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/evidence.rs:422`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/30`。

### `crates/winwincode-delivery/src/domain/evidence.rs::&lt;closure_expression@482:45&gt;`

在调用形式「resolution_error」中提供第 1 个实参「EvidenceResolutionErrorCode::InvalidEvidence」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/evidence.rs:482`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/31`。

### `crates/winwincode-delivery/src/domain/evidence.rs::resolve_direct_candidate_source`

构造捕获记录，字段按源码次序为「evidence_type ← EvidenceRefType::Commit；source_ref ← format!("git_commit:{}", candidate.candidate_commit_id())；outcome ← VerifiedEvidenceOutcome::Observed；identity ← VerifiedEvidenceSourceIdentity::CandidateCommit {\n                candidate_ref: candidate.candidate_ref().into(),\n                candidate_commit_id: candid…［展示截断；完整操作保留］」。不据构造形式推断物理持久化。 将「candidate」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-delivery/src/domain/evidence#assert_direct_candidate_producer」，对应捕获形参「candidate: &amp;FrozenDeliveryCandidate」。该普通调用关系不替代进程或网络协议关系。 保留同一块中的正常源码顺序：语句位置「0」的操作「6792750ddcff53647ee2774a」先于语句位置「1」的操作「509045a7a6f0921481e700eb」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-delivery/src/domain/evidence.rs:531`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/32`。

### `crates/winwincode-delivery/src/domain/evidence.rs::resolve_runtime_source`

构造捕获记录，字段按源码次序为「execution ← expected_identity；source_sequence ← fact.source_sequence；terminal_last_event_sequence ← accepted_terminal_sequence(terminal)；candidate_ref ← fact.candidate_ref.clone()；checkout_commit_id ← checkout.checkout_commit_id.clone()；checkout_tree_id ← checkout.checkout_tree_id.clone()；command_digest ← fact.command_digest.clone()」。不据构造形式推断物理持久化。 在调用形式「portable_identifier」中提供第 1 个实参「&amp;source_event_id.0」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「expected_identity」的初始化来源为「validate_runtime_terminal(\n        candidate,\n        work_run,\n        binding,\n        terminal,\n        evidence_created_at_millis,\n    )?」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「evidence_type == EvidenceRefType::PullRequest」的捕获提前退出分支为「Err_return：Err(resolution_error(\n            EvidenceResolutionErrorCode::InvalidEvidence,\n            "runtime evidence type is unsupported",\n        ))」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(resolution_error(\n            EvidenceResolutionErrorCode::InvalidEvidence,\n            "runtime evidence type is unsupported",\n        ))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「evidence_type」关联路径「evidence_type」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「1」的操作「26bb8ebe9ee300ad92361c0e」先于语句位置「2」的操作「c8c5ae7e6ae8f03305d294f9」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-delivery/src/domain/evidence.rs:743`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/33`。

### `crates/winwincode-delivery/src/domain/evidence.rs::&lt;closure_expression@760:79&gt;`

在调用形式「resolution_error」中提供第 1 个实参「EvidenceResolutionErrorCode::InvalidEvidence」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/evidence.rs:760`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/34`。

### `crates/winwincode-delivery/src/domain/evidence.rs::&lt;closure_expression@817:83&gt;`

在调用形式「resolution_error」中提供第 1 个实参「EvidenceResolutionErrorCode::InvalidEvidence」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/evidence.rs:817`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/35`。

### `crates/winwincode-delivery/src/domain/evidence.rs::validate_runtime_terminal`

构造捕获记录，字段按源码次序为「product_session_id ← terminal.product_session_id().clone()；execution_job_id ← terminal.execution_job_id().clone()；work_run_id ← terminal.work_run_id().clone()；role_id ← terminal.role_id().into()；attempt ← terminal.attempt()；lease_id ← terminal.lease_id().clone()；fencing_token ← terminal.fencing_token().clone()；worker_id ← terminal.worker_id().clone()；worker_instance_id ← terminal.worker_instance_id().clone()；worker_session_id ← terminal.worker_session_id().clone()；codex_thread_id ← terminal.codex_thread_id().clone()」。不据构造形式推断物理持久化。 将「terminal」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-delivery/src/domain/evidence#accepted_terminal_sequence」，对应捕获形参「terminal: &amp;AcceptedVerificationJobOutcomeFact」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「worker_session_id」的初始化来源为「binding\n        .worker_session_id\n        .as_ref()\n        .expect("complete binding")」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「terminal.product_session_id() != &amp;binding.product_session_id\n        || terminal.execution_job_id() != &amp;binding.execution_job_id\n        || terminal.worker_session_id() != worker_session_id\n        || terminal.codex_thread_id() != codex_thread_id\n        || terminal.work_run_id() != &amp;work_run.id\n        || terminal.attempt() != u64::try_from(work_run.at…［展示截断；完整操作保留］」的捕获提前退出分支为「Err_return：Err(resolution_error(\n            EvidenceResolutionErrorCode::SessionMismatch,\n            "runtime terminal result belongs to another product, job, worker, thread, stage, or role",\n        ))」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(resolution_error(\n            EvidenceResolutionErrorCode::SessionMismatch,\n            "runtime terminal result belongs to another product, job, worker, thread, stage, or role",\n        ))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「4c12038815b86c3136227061」先于语句位置「1」的操作「eef066a8db55d8545c0ffd4d」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-delivery/src/domain/evidence.rs:841`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/36`。

### `crates/winwincode-delivery/src/domain/evidence.rs::validate_checkout_attestation`

将「checkout」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-delivery/src/domain/evidence#checkout_identity」，对应捕获形参「fact: &amp;ValidatedCheckoutAttestationFact」。该普通调用关系不替代进程或网络协议关系。 条件「checkout_identity(checkout) != *expected_identity」的捕获提前退出分支为「Err_return：Err(resolution_error(\n            EvidenceResolutionErrorCode::SessionMismatch,\n            "checkout attestation belongs to another fenced execution",\n        ))」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(resolution_error(\n            EvidenceResolutionErrorCode::SessionMismatch,\n            "checkout attestation belongs to another fenced execution",\n        ))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「fa23335772cc33b215144001」先于语句位置「1」的操作「7692e3ea259b344cfb3d2d8e」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-delivery/src/domain/evidence.rs:898`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/37`。

### `crates/winwincode-delivery/src/domain/evidence.rs::runtime_source_identity`

构造捕获记录，字段按源码次序为「product_session_id ← fact.product_session_id.clone()；execution_job_id ← fact.execution_job_id.clone()；work_run_id ← fact.work_run_id.clone()；role_id ← fact.role_id.clone()；attempt ← fact.attempt；lease_id ← fact.lease_id.clone()；fencing_token ← fact.fencing_token.clone()；worker_id ← fact.worker_id.clone()；worker_instance_id ← fact.worker_instance_id.clone()；worker_session_id ← fact.worker_session_id.clone()；codex_thread_id ← fact.codex_thread_id.clone()」。不据构造形式推断物理持久化。 以无显式实参的调用形式「fact.product_session_id.clone」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。 以字段投影形式「fact.product_session_id.clone()」关联路径「fact.product_session_id」；只描述捕获来源，不证明当时的字段值。

源码：`crates/winwincode-delivery/src/domain/evidence.rs:921`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/38`。

**显式来源交接**（列实际样例，所有关系保留）：

- 「crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::resolve_production_verdict」的捕获来源被「crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::resolve_production_verdict」的显式 return 消费；未据此证明调用方激活或运行结果。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/0`。
- 「crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::resolve_production_verdict」的捕获来源被「crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::resolve_production_verdict」的显式 return 消费；未据此证明调用方激活或运行结果。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/1`。
- 「crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::resolve_production_verdict」的捕获记录与「crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::resolve_production_verdict」中的字段投影存在显式源关系；当前值和全部覆盖路径另保留。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/2`。
- 「crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::resolve_production_verdict」的捕获记录与「crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::resolve_production_verdict」中的字段投影存在显式源关系；当前值和全部覆盖路径另保留。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/3`。
- 「crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::resolve_production_verdict」中的实际记录 literal 语法位置直接构成「crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::resolve_production_verdict」的调用实参；没有把记录构造解释为持久提交。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/4`。
- 「crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::resolve_production_verdict」的捕获记录与「crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::resolve_production_verdict」中的字段投影存在显式源关系；当前值和全部覆盖路径另保留。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/5`。
- 「crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::resolve_production_verdict」中的实际记录 literal 语法位置直接构成「crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::resolve_production_verdict」的调用实参；没有把记录构造解释为持久提交。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/6`。
- 「crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::resolve_production_verdict」的捕获记录与「crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::resolve_production_verdict」中的字段投影存在显式源关系；当前值和全部覆盖路径另保留。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/7`。

**接口复用**（列实际样例，所有关系保留）：

- 所选的 3 个确切声明通过已绑定调用复用「rust:crates/winwincode-delivery/src/domain/candidate/verdict_authority#error」；复用本身不构成职责混乱或唯一资源所有权的判断。 完整引用：`/architecture/responsibility_explanations/authenticated_interface_reuse/0`。
- 所选的 3 个确切声明通过已绑定调用复用「rust:crates/winwincode-delivery/src/domain/evidence#resolution_error」；复用本身不构成职责混乱或唯一资源所有权的判断。 完整引用：`/architecture/responsibility_explanations/authenticated_interface_reuse/1`。

## 主要功能链、条件与反证

源码顺序只描述同一次调用正常到达的关系；异步完成、消息传输、远端响应和物理持久化均以实际证据范围为准。

### `wwc-delivery-evidence-frozen-contract-slice`

分析类型：`guarded_call_sequence`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/0`；保存发现：`7221871f53add43c022a5cea`。

**verdict_root 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `assert_frozen_candidate_current(delivery, &amp;candidate)         .map_err → assert_frozen_candidate_current`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:211`。
- `Vec::with_capacity → verification.len`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:213`。
- `Vec::new`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:214`。
- `HashSet::with_capacity → verification.len`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:215`。
- `candidate.producer_finished_at_millis`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:216`。
- `resolve_verification_runtime → roles.insert → Err → error → produced_at_millis.max → sessions.push → evidence.extend`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:218`。
- `required_roles`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:227`。
- `roles.len → required_roles.len → required_roles.iter().any → required_roles.iter → Err → error`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:228`。
- `sessions.sort_by_key`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:235`。
- `evidence.sort_by`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:236`。
- `evidence.dedup_by`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:237`。
- `validate_independent_verification(         delivery,         &amp;candidate,         &amp;VerificationFacts {             required_roles,             sessions,         },     )     .map_err → validate_independent_verification`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:238`。
- 后续步骤保留在 `/functional_chains/0/pattern/sequences/verdict_root`。

**verification_runtime 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `if runtime.read_only_candidate_source {         validated_git_snapshot_from_candidate(delivery, candidate, &amp;runtime.terminal)     } else {         validated_git_snapshot_from_source(delivery, &amp;runtime.source, &amp;runtime.terminal)     }     .map_err → validated_git_snapshot_from_candidate → validated_g…［展示截断；完整值见引用］`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:290`。
- `delivery         .snapshot()         .session_bindings         .iter()         .find(|binding| {             binding.execution_job_id == *verified_terminal.execution_job_id()                 &amp;&amp; binding.work_run_id == *verified_terminal.work_run_id()                 &amp;&amp; binding.attempt == verified_ter…［展示截断；完整值见引用］`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:297`。
- `if runtime.read_only_candidate_source {         AcceptedVerificationJobOutcomeFact::from_verified_read_only_outcome(             &amp;verified_terminal,             &amp;snapshot,             role.as_str(),         )     } else {         AcceptedVerificationJobOutcomeFact::from_verified_outcome(            …［展示截断；完整值见引用］`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:307`。
- `validated_runtime_events`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:321`。
- `validate_policy_attestation`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:322`。
- `structured_result`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:323`。
- `checkout_attestation_from_snapshot`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:324`。
- `resolve_findings`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:325`。
- `Ok → binding.work_run_id.clone → binding.id.clone → Some → snapshot.clone → Vec::new → verified_terminal.finished_at_millis`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:335`。

**role_requirements 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `[         VerificationRole::Reviewer,         VerificationRole::Verifier,         VerificationRole::AdversarialVerifier,     ]     .into_iter()     .filter(|role| roles.contains(role))     .collect::&lt;Vec&lt;_&gt;&gt; → [         VerificationRole::Reviewer,         VerificationRole::Verifier,         Verifica…［展示截断；完整值见引用］`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:762`。
- `Err → error`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:770`。
- `Ok`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:783`。

**finding_sources 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `Vec::with_capacity → result.payload.findings.len`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:571`。
- `BTreeMap::new`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:572`。
- `HashSet::with_capacity → result.payload.findings.len`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:573`。
- `finding             .criterion_id             .ok_or_else → criterion_ids.insert → criterion_id.clone → Err → error → finding.evidence_sources.is_empty → Vec::with_capacity → finding.evidence_sources.len → exact_source_event → runtime_outcome → source.event_id.0.clone → evidence_type_order → evidenc…［展示截断；完整值见引用］`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:574`。
- `Ok → evidence_by_source.into_values().collect → evidence_by_source.into_values`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:661`。

**source_event_lookup 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `events         .iter()         .filter → events         .iter`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:668`。
- `matching         .next()         .ok_or_else → matching         .next`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:671`。
- `matching.next().is_some → matching.next → Err → error`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:674`。
- `Ok`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:679`。

**canonical_evidence 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `assert_frozen_candidate_current(delivery, candidate).map_err → assert_frozen_candidate_current`；`crates/winwincode-delivery/src/domain/evidence.rs:422`。
- `evidence_work_run_and_binding`；`crates/winwincode-delivery/src/domain/evidence.rs:428`。
- `resolve_runtime_source → resolve_direct_candidate_source`；`crates/winwincode-delivery/src/domain/evidence.rs:430`。
- `deterministic_evidence_id → delivery.id → delivery.snapshot → candidate.candidate_ref`；`crates/winwincode-delivery/src/domain/evidence.rs:458`。
- `delivery.id().clone → delivery.id → delivery.snapshot().spec.id.clone → delivery.snapshot → work_run.id.clone → binding.id.clone → candidate.candidate_ref().into → candidate.candidate_ref`；`crates/winwincode-delivery/src/domain/evidence.rs:469`。
- `validate(&amp;evidence, "evidence").map_err → validate`；`crates/winwincode-delivery/src/domain/evidence.rs:482`。
- `Ok`；`crates/winwincode-delivery/src/domain/evidence.rs:489`。

**direct_candidate_source 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `assert_direct_candidate_producer`；`crates/winwincode-delivery/src/domain/evidence.rs:539`。
- `Ok → candidate.candidate_ref().into → candidate.candidate_ref → candidate.candidate_commit_id().into → candidate.candidate_commit_id → candidate.diff_sha256().into → candidate.diff_sha256 → resolve_direct_candidate_file → Err → resolution_error`；`crates/winwincode-delivery/src/domain/evidence.rs:546`。

**runtime_source 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `Err → resolution_error`；`crates/winwincode-delivery/src/domain/evidence.rs:754`。
- `portable_identifier(&amp;source_event_id.0, "evidence.sourceEventId").map_err → portable_identifier`；`crates/winwincode-delivery/src/domain/evidence.rs:760`。
- `validate_runtime_terminal`；`crates/winwincode-delivery/src/domain/evidence.rs:766`。
- `validate_checkout_attestation`；`crates/winwincode-delivery/src/domain/evidence.rs:773`。
- `accepted_sources         .iter()         .filter(|fact| fact.source_event_id == *source_event_id)         .collect → accepted_sources         .iter()         .filter → accepted_sources         .iter`；`crates/winwincode-delivery/src/domain/evidence.rs:774`。
- `matches.is_empty → Err → resolution_error`；`crates/winwincode-delivery/src/domain/evidence.rs:778`。
- `matches.len → Err → resolution_error`；`crates/winwincode-delivery/src/domain/evidence.rs:784`。
- `runtime_source_identity → Err → resolution_error`；`crates/winwincode-delivery/src/domain/evidence.rs:791`。
- `Err → resolution_error`；`crates/winwincode-delivery/src/domain/evidence.rs:797`。
- `candidate.candidate_ref → Err → resolution_error`；`crates/winwincode-delivery/src/domain/evidence.rs:803`。
- `validate_runtime_source_position`；`crates/winwincode-delivery/src/domain/evidence.rs:809`。
- `bounded_text(&amp;source_ref, "evidence.sourceRef", MAX_REFERENCE_LENGTH).map_err → bounded_text`；`crates/winwincode-delivery/src/domain/evidence.rs:817`。
- 后续步骤保留在 `/functional_chains/0/pattern/sequences/runtime_source`。

**runtime_terminal 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `binding         .worker_session_id         .as_ref()         .expect → binding         .worker_session_id         .as_ref`；`crates/winwincode-delivery/src/domain/evidence.rs:848`。
- `binding.codex_thread_id.as_ref().expect → binding.codex_thread_id.as_ref`；`crates/winwincode-delivery/src/domain/evidence.rs:852`。
- `terminal.product_session_id → terminal.execution_job_id → terminal.worker_session_id → terminal.codex_thread_id → terminal.work_run_id → terminal.attempt → u64::try_from(work_run.attempt).unwrap_or → u64::try_from → Err → resolution_error`；`crates/winwincode-delivery/src/domain/evidence.rs:853`。
- `terminal.terminal_candidate_tree_id → candidate.candidate_tree_id → Err → resolution_error`；`crates/winwincode-delivery/src/domain/evidence.rs:865`。
- `accepted_terminal_sequence`；`crates/winwincode-delivery/src/domain/evidence.rs:871`。
- `terminal.finished_at_millis → Err → resolution_error`；`crates/winwincode-delivery/src/domain/evidence.rs:872`。
- `Ok → terminal.product_session_id().clone → terminal.product_session_id → terminal.execution_job_id().clone → terminal.execution_job_id → terminal.work_run_id().clone → terminal.work_run_id → terminal.role_id().into → terminal.role_id → terminal.attempt → terminal.lease_id().clone → terminal.lease_id…［展示截断；完整值见引用］`；`crates/winwincode-delivery/src/domain/evidence.rs:883`。

**checkout_guard 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `checkout_identity → Err → resolution_error`；`crates/winwincode-delivery/src/domain/evidence.rs:903`。
- `candidate.repository → candidate.candidate_commit_id → candidate.candidate_tree_id → Err → resolution_error`；`crates/winwincode-delivery/src/domain/evidence.rs:909`。
- `Ok`；`crates/winwincode-delivery/src/domain/evidence.rs:918`。

**runtime_identity 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `fact.product_session_id.clone → fact.execution_job_id.clone → fact.work_run_id.clone → fact.role_id.clone → fact.lease_id.clone → fact.fencing_token.clone → fact.worker_id.clone → fact.worker_instance_id.clone → fact.worker_session_id.clone → fact.codex_thread_id.clone`；`crates/winwincode-delivery/src/domain/evidence.rs:922`。

**checkout_capture 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `terminal.product_session_id().clone → terminal.product_session_id → terminal.execution_job_id().clone → terminal.execution_job_id → terminal.work_run_id().clone → terminal.work_run_id → terminal.role_id().into → terminal.role_id → terminal.attempt → terminal.lease_id().clone → terminal.lease_id → te…［展示截断；完整值见引用］`；`crates/winwincode-delivery/src/domain/evidence.rs:135`。

**runtime_capture 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `terminal.product_session_id().clone → terminal.product_session_id → terminal.execution_job_id().clone → terminal.execution_job_id → terminal.worker_session_id().clone → terminal.worker_session_id → terminal.codex_thread_id().clone → terminal.codex_thread_id → terminal.work_run_id().clone → terminal.…［展示截断；完整值见引用］`；`crates/winwincode-delivery/src/domain/evidence.rs:164`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| scoped_source_supported | true | /functional_chains/0/pattern/scoped_source_supported |
| sequences/canonical_evidence/conditions | [] | /functional_chains/0/pattern/sequences/canonical_evidence/conditions |
| sequences/canonical_evidence/future_or_callback_activation_proven | false | /functional_chains/0/pattern/sequences/canonical_evidence/future_or_callback_activation_proven |
| sequences/canonical_evidence/orders/0/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/0/pattern/sequences/canonical_evidence/orders/0/conditions |
| sequences/canonical_evidence/orders/0/all_paths_reach_next_proven | false | /functional_chains/0/pattern/sequences/canonical_evidence/orders/0/all_paths_reach_next_proven |
| sequences/canonical_evidence/orders/1/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/0/pattern/sequences/canonical_evidence/orders/1/conditions |
| sequences/canonical_evidence/orders/1/all_paths_reach_next_proven | false | /functional_chains/0/pattern/sequences/canonical_evidence/orders/1/all_paths_reach_next_proven |
| sequences/canonical_evidence/orders/2/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/0/pattern/sequences/canonical_evidence/orders/2/conditions |
| sequences/canonical_evidence/orders/2/all_paths_reach_next_proven | false | /functional_chains/0/pattern/sequences/canonical_evidence/orders/2/all_paths_reach_next_proven |
| sequences/canonical_evidence/orders/3/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/0/pattern/sequences/canonical_evidence/orders/3/conditions |
| sequences/canonical_evidence/orders/3/all_paths_reach_next_proven | false | /functional_chains/0/pattern/sequences/canonical_evidence/orders/3/all_paths_reach_next_proven |
| sequences/canonical_evidence/orders/4/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/0/pattern/sequences/canonical_evidence/orders/4/conditions |
| sequences/canonical_evidence/orders/4/all_paths_reach_next_proven | false | /functional_chains/0/pattern/sequences/canonical_evidence/orders/4/all_paths_reach_next_proven |
| sequences/canonical_evidence/orders/5/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/0/pattern/sequences/canonical_evidence/orders/5/conditions |
| sequences/canonical_evidence/orders/5/all_paths_reach_next_proven | false | /functional_chains/0/pattern/sequences/canonical_evidence/orders/5/all_paths_reach_next_proven |
| sequences/canonical_evidence/steps/0/conditional_normal_reaching_only | true | /functional_chains/0/pattern/sequences/canonical_evidence/steps/0/conditional_normal_reaching_only |
| sequences/canonical_evidence/steps/1/conditional_normal_reaching_only | true | /functional_chains/0/pattern/sequences/canonical_evidence/steps/1/conditional_normal_reaching_only |
| sequences/canonical_evidence/steps/2/conditional_normal_reaching_only | true | /functional_chains/0/pattern/sequences/canonical_evidence/steps/2/conditional_normal_reaching_only |

所有事实及源位置：`/functional_chains/0/source_facts`；配置声明单列于 `/functional_chains/0/policy_declarations`，不作为自动证据。

## 捕获范围与未审边界

选入 471 份源码，解析 465 份。这是源码捕获与语法解析范围，不能换算成功能完整率。

| 区域 | 文件 | 已解析 |
| --- | --- | --- |
| apps/client | 95 | 95 |
| crates/helper | 1 | 1 |
| crates/kernel | 2 | 2 |
| crates/winwincode-api | 1 | 1 |
| crates/winwincode-audit | 5 | 5 |
| crates/winwincode-cli | 11 | 11 |
| crates/winwincode-client-port | 12 | 12 |
| crates/winwincode-codex | 16 | 16 |
| crates/winwincode-connector-github | 1 | 1 |
| crates/winwincode-connector-jira | 1 | 1 |
| crates/winwincode-connector-linear | 1 | 1 |
| crates/winwincode-connector-slack | 1 | 1 |
| crates/winwincode-connector-teams | 1 | 1 |
| crates/winwincode-connector-webhook | 1 | 1 |
| crates/winwincode-control-plane | 94 | 94 |
| crates/winwincode-data-export | 1 | 1 |
| crates/winwincode-delivery | 25 | 25 |
| crates/winwincode-device-client | 20 | 20 |
| crates/winwincode-domain | 5 | 5 |
| crates/winwincode-evidence-export | 6 | 6 |
| crates/winwincode-execution-port | 26 | 25 |
| crates/winwincode-fusion | 4 | 4 |
| crates/winwincode-integration-core | 5 | 5 |
| crates/winwincode-integration-sqlite | 2 | 2 |
| crates/winwincode-local | 1 | 1 |
| crates/winwincode-observability-core | 1 | 1 |
| crates/winwincode-observability-sqlite | 1 | 1 |
| crates/winwincode-provider | 11 | 11 |
| crates/winwincode-publication | 7 | 7 |
| crates/winwincode-repository-context | 5 | 5 |
| crates/winwincode-s3-artifact-adapter | 1 | 1 |
| crates/winwincode-server | 23 | 22 |
| crates/winwincode-session | 4 | 4 |
| crates/winwincode-storage | 34 | 33 |
| crates/winwincode-worker | 21 | 18 |
| deploy | 1 | 1 |
| docs/engineering-runtime | 1 | 1 |
| jev-runtime-spec/js | 1 | 1 |
| packages/browser-core | 2 | 2 |
| packages/browser-ui | 7 | 7 |
| packages/contracts | 6 | 6 |
| packages/control-plane-client | 1 | 1 |
| packages/strongflow | 2 | 2 |
| schema/winwincode-export | 3 | 3 |
| winwincode-bd-tracks/js | 1 | 1 |

项目声明与依赖：`/project_declarations`；已绑定跨目录图引用：`/architecture/dependencies`。声明存在、路径可达和依赖计数均不证明业务行为通过。

- `crates/winwincode-execution-port/src/diagnostic_parser.rs`：parse_error；Tree-sitter 检测到错误/缺失语法节点；仅提取可识别的局部结构。。
- `crates/winwincode-server/src/worker_session_credentials.rs`：parse_error；Tree-sitter 检测到错误/缺失语法节点；仅提取可识别的局部结构。。
- `crates/winwincode-storage/src/provider_exchange.rs`：parse_error；Tree-sitter 检测到错误/缺失语法节点；仅提取可识别的局部结构。。
- `crates/winwincode-worker/src/managed_session.rs`：parse_error；Tree-sitter 检测到错误/缺失语法节点；仅提取可识别的局部结构。。
- `crates/winwincode-worker/src/probe_evidence.rs`：parse_error；Tree-sitter 检测到错误/缺失语法节点；仅提取可识别的局部结构。。
- `crates/winwincode-worker/src/probe_scheduler.rs`：parse_error；Tree-sitter 检测到错误/缺失语法节点；仅提取可识别的局部结构。。

配置排除：`[".git",".beads",".agents",".codex",".callscope",".analysis-tools",".venv","venv","__pycache__","node_modules","target","dist","build","coverage","third_party","upstream","vendor","generated","tests","test","__tests__","examples","scripts","crates/winwincode-test-assets","**/*.test.ts","**/*.test.ts…［展示截断；完整值见引用］`。

所选局部分析：`/configured_local_assessments`；完整诊断：`/diagnostics`。未建模域保持未审，不保证全仓库无缺陷、所有权或授权完整，也不将未知标为通过。

报告生成组件：`/report_components`；原快照分析组件：`/snapshot/component_versions`。两者分别保存，历史发现不会因生成新版报告而升级。

