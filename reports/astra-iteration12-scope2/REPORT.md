# CallScope v0.14.0：原报告范围内的自动静态判断

本轮以原 [CodePatchBay](../astra-baseline/CODEPATCHBAY_ANALYSIS.md) 和 [WinWinCode](../astra-baseline/WINWINCODE_ANALYSIS.md) 分析报告为功能基准。具体判断、主要链的源码关系、项目结构盘点和全文范围对照分别保存；没有新增重复 Astra 审批。

原报告实际已读的有限内容已逐项对照到本轮正常自动报告的具体正文与来源，见 [原报告内容对照](ORIGINAL_REPORT_COMPLETION.md)及[正式引用记录](ORIGINAL_REPORT_COMPLETION.json)。范围包含职责表、主要链、文档部署比较及原反证；未审领域与更强运行命题继续保留。

既有追踪另含 5 项原判断、30 项关系：5 项完整裁决，5 项完整支持原 claim。这是所选条件判断的结果，不是全项目功能覆盖率或缺陷通过率。

目标未导入、执行、测试、构建或安装；工具测试套件未运行。结果来自受信工具的正常静态冷/暖扫描和保存产物。

## 配置判断的保存结果

| 仓库 | 原判断 | 保存评估 | 完整裁决 | 支持原 claim | 必要关系状态 |
| --- | --- | --- | --- | --- | --- |
| codepatchbay | CPB-01 | scoped_static_judgment_reproduced | True | True | {"supported":6} |
| codepatchbay | CPB-02 | scoped_static_judgment_reproduced | True | True | {"supported":5} |
| codepatchbay | CPB-03 | scoped_static_judgment_reproduced | True | True | {"supported":7} |
| winwincode | WWC-01 | scoped_static_judgment_reproduced | True | True | {"supported":7} |
| winwincode | WWC-02 | scoped_static_judgment_reproduced | True | True | {"supported":5} |

以下结论逐字复制正式报告的 `derived_judgment` 字段；条件、反证、policy 不变量与模型适用范围保存在两库自动报告和 [goal-ledger.json](goal-ledger.json)。账本复制正式保存状态，没有重新评分。

- **CPB-01**：On the checked normal pipeline record/message path, the submitted retries field is transported as metadata but the managed worker constructs an independent selected literal. Actual queue, phase and infrastructure decisions use their distinct local authorities. Existing records, finalizer-only, early returns, opaque consumers and unsuccessful/not-run operations bound this finding; retry capability is present.
- **CPB-02**：{"authority_terminal_membership":true,"classification_differs":true,"kind":"conditional_terminal_classification_difference","recovery_is_required_or_authorized":false,"status":"superseded","terminal_state_can_be_illegally_mutated":false,"valid_identity_predicate_result":false}
- **CPB-03**：Two same-project/key/description default submissions can both observe no row; the first protected insert can be guardedly scheduled before the second protected check; the pending-only inner check then inserts a second nonterminal row
- **WWC-01**：The selected source-derived absent-query path reaches the actual production port callback and rejects its create before command calls, under the retained platform/form conditions.
- **WWC-02**：Under the explicitly retained normal production, JSON/Serde and active Device conditions, the closed UI command field omission reaches None and the nonblank authority guard rejects before criterion use/commit.

## 具体职责、接口与文档对照

正常 CLI / HTTP / MCP 报告已接入生成器 v3 的具体职责正文。正文来自所选声明的实际字段、实参、绑定接口、guard 和来源模型；目录标签、同名方法和操作数量均不充当行为证据。完整操作、共享位置/上下文索引与原 Findings 分别保留。

### codepatchbay

保存评估 `{"all_operations_authorized_proven":false,"explanation_generated_from_actual_operations":true,"functional_coverage_percentage_computed":false,"method_names_used_to_infer_responsibility":false,"reference_report_text_used_as_evidence":false,"runtime_or_physical_effects_verified":false,"source_directories_used_to_assign_responsibility":false,"state":"finite_source_responsibility_explanations_available","unique_fact_owner_proven":false,"whole_report_reproduced":false,"whole_repository_ownership_proven":false}`；操作抽取预算 `{"incomplete":false,"limits":{"operations":16384,"relationships":32768,"selected_declarations":512,"source_references_per_operation":96,"source_text_characters":384,"visited_nodes":262144},"operations":15223,"relationships":9911,"visited_nodes":66909}`。

实际解释缺口 `[]`；正文来源缺口 `[]`。缺口按原值保留，不以已有正文覆盖。

[自动报告正文](codepatchbay-automatic-report.md)；[全部具体职责与来源](codepatchbay-automatic-report.json#/architecture/responsibility_explanations)。

- 所选默认装配的源模型列出动态命令 import 的候选路径「captured_path:cli/commands/pipeline.ts」。其他捕获路径分支为「symbolic_path:cli/commands/init.js；symbolic_path:cli/commands/hub.js；symbolic_path:cli/commands/pipeline.js；symbolic_path:cli/commands/fix.js；symbolic_path:cli/commands/task.js；symbolic_path:cli/commands/status.js；symbolic_path:cli/commands/list.js；symbolic_path:cli/commands/jobs.js；symbolic_path:cli/commands/retry.js；symbolic_path:cli/commands/diff.js；symbolic_path:cli/commands/review.js；symbolic_path:cli/commands/inbox.js；symbolic_path:cli/commands/setup.js；symbolic_path:cli/commands/agents.js；symbolic_path:cli/commands/github.js；symbolic_path:cli/commands/doctor.js；symbolic_path:cli/commands/stream.js；symbolic_path:cli/commands/cancel-redirect.js；symbolic_path:cli/commands/cancel-redirect.js；symbolic_path:cli/commands/version.js；symbolic_path:cli/commands/code-index.js；captured_path:cli/commands/init.js；captured_path:cli/commands/hub.js；captured_path:cli/commands/fix.js；captured_path:cli/commands/task.js；captured_path:cli/commands/status.js；captured_path:cli/commands/list.js；captured_path:cli/commands/jobs.js；captured_path:cli/commands/retry.js；captured_path:cli/commands/diff.js；captured_path:cli/commands/review.js；captured_path:cli/commands/inbox.js；captured_path:cli/commands/setup.js；captured_path:cli/commands/agents.js；captured_path:cli/commands/github.js；captured_path:cli/commands/doctor.js；captured_path:cli/commands/stream.js；captured_path:cli/commands/cancel-redirect.js；captured_path:cli/commands/cancel-redirect.js；captured_path:cli/commands/version.js；captured_path:cli/commands/code-index.js」；这是有限路径与实际形参关系，不把所有候选当必然普通调用。 原关系：`/judgments/0/obligations/1/evidence/production_assembly/cli/calls/0`。
- 捕获的标准 Node spawn 导入通过实际 argv 源关系选择 worker 路径「symbolic_path:runtime/worker/managed-worker.js」；进程接线独立于普通函数 CALLS，未据此宣称进程已经启动或 worker 已执行。 原关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_process_starts/0`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.claimInboxEntries；WorkerStore.claimInboxEntries」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/0`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.completeInboxClaim；WorkerStore.completeInboxClaim」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/1`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.completeInboxClaim；WorkerStore.completeInboxClaim」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/2`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.completeInboxClaim；WorkerStore.completeInboxClaim」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/3`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.completeInboxClaim；WorkerStore.completeInboxClaim」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/4`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.completeInboxClaim；WorkerStore.completeInboxClaim」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/5`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.assertActiveAttemptIdentity；AssignmentStore.assertActiveAttemptIdentity」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/6`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.completeInboxClaim；WorkerStore.completeInboxClaim」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/7`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.updateWorkerIf；WorkerStore.updateWorkerIf」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/8`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.updateWorkerIf；WorkerStore.updateWorkerIf」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/9`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.completeInboxClaim；WorkerStore.completeInboxClaim」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/10`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.markRunning；AssignmentStore.markRunning」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/11`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.assertActiveAttemptIdentity；AssignmentStore.assertActiveAttemptIdentity」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/12`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.completeInboxClaim；WorkerStore.completeInboxClaim」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/13`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.updateWorkerIf；WorkerStore.updateWorkerIf」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/14`。
- 已有条件源码模型记录「受保护 queue 的 JSON 记录交接」的源操作与条件；实际部件关系为「callback=true；codec=true；lifecycle=true；path=true」，捕获参与声明为「ts:server/services/hub/hub-queue#loadLocalQueue；ts:server/services/hub/hub-queue#saveLocalQueue；ts:server/services/hub/hub-queue#withQueueMutation；ts:server/services/hub/hub-queue#withQueueMutation.<arrow@1462:38>」。持久消息和协议关系保持独立，执行、交付与队列投影没有合并成一个成功。 原关系：`/judgments/0/obligations/2/evidence/channels/queue`。
- 已有条件源码模型记录「inbox 文件记录的提交、领取与消费」的源操作与条件；实际部件关系为「reader=true；record_identity=true；writer=true」，捕获参与声明为「module:ts:shared/fs-utils；ts:shared/fs-utils#currentHooks；ts:shared/fs-utils#jsonContent；ts:shared/fs-utils#writeJsonAtomic；ts:shared/orchestrator/worker-store#WorkerStore._readLocalInboxJson；ts:shared/orchestrator/worker-store#WorkerStore._withLocalInboxLock；ts:shared/orchestrator/worker-store#WorkerStore.claimInboxEntries；ts:shared/orchestrator/worker-store#WorkerStore.claimInboxEntries.<loop@1967:4>.<arrow@1967:36>；ts:shared/orchestrator/worker-store#WorkerStore.claimInboxEntries.<loop@1967:4>.<block@1967:71>.<arrow@1969:75>；ts:shared/orchestrator/worker-store#WorkerStore.constructor；ts:shared/orchestrator/worker-store#WorkerStore.writeInboxWithReceipt；ts:shared/orchestrator/worker-store#WorkerStore.writeInboxWithReceipt.<arrow@1703:60>」。记录/响应字段为「assignmentId；attempt；attemptToken；backend；committedRecord；path；previousRecord；ref；workerId；writeFence」。持久消息和协议关系保持独立，执行、交付与队列投影没有合并成一个成功。 原关系：`/judgments/0/obligations/2/evidence/channels/inbox`。
- 已有条件源码模型记录「认证 broker 的 JSON 请求、分派与响应」的源操作与条件；实际部件关系为「claims_validation=true；credentials=true；dispatch=true；operation=true；request=true；response=true」，捕获参与声明为「ts:server/index#sendJson；ts:server/index#startHubServer.<arrow@195:30>；ts:server/services/hub/worker-state-broker#handleWorkerStateBroker；ts:server/services/hub/worker-state-broker#readWorkerBrokerBody；ts:shared/orchestrator/worker-broker-client#WorkerBrokerClient.#call；ts:shared/orchestrator/worker-broker-client#WorkerBrokerClient.claimInboxEntries；ts:shared/orchestrator/worker-broker-client#WorkerBrokerClient.claimInboxEntries.<arrow@154:107>；ts:shared/orchestrator/worker-broker-client#WorkerBrokerClient.constructor；ts:shared/orchestrator/worker-broker-client#brokerResult；ts:shared/orchestrator/worker-broker-client#inboxClaimsResult；ts:shared/orchestrator/worker-broker-client#inboxClaimsResult.<arrow@83:19>；ts:shared/orchestrator/worker-broker-client#recordResult」。记录/响应字段为「beforeMutation；body；cpbRoot；headers；hubRoot」。持久消息和协议关系保持独立，执行、交付与队列投影没有合并成一个成功。 原关系：`/judgments/0/obligations/2/evidence/channels/broker`。
- 已有条件源码模型记录「持久 assignment/attempt 记录到消费者的交接」的源操作与条件；实际部件关系为「consumer=true；reader=true；writer=true」，捕获参与声明为「module:ts:shared/fs-utils；ts:server/orchestrator/reconciler#Reconciler._compensateFinalization；ts:server/orchestrator/reconciler#Reconciler._finalizeAssignment；ts:server/orchestrator/reconciler#Reconciler._finalizeQueue；ts:server/orchestrator/reconciler#Reconciler.reconcileAssignments；ts:shared/fs-utils#currentHooks；ts:shared/fs-utils#jsonContent；ts:shared/fs-utils#writeJsonAtomic；ts:shared/orchestrator/assignment-store#AssignmentStore._readLocalJsonObject；ts:shared/orchestrator/assignment-store#AssignmentStore._readState；ts:shared/orchestrator/assignment-store#AssignmentStore._readStateFile；ts:shared/orchestrator/assignment-store#AssignmentStore._writeState」。持久消息和协议关系保持独立，执行、交付与队列投影没有合并成一个成功。 原关系：`/judgments/0/obligations/2/evidence/channels/counter_transport`。
- 源码实际模式字面量为 ["dry-run", "local", "pr", "remote"]，声明的 plan 字段为 ["closeIssue", "commit", "merge", "pullRequest", "pullRequestPreview", "push"]。有限表组合这些模式与源码中的布尔 opt-in，并保留字段 unknown；plan 不是已发生的写入。PR 调用的真实选项绑定到 callee 形参后，源码中早于条件 transport 且成立时 return 的条件包括 ["(!allowLive)", "(!isPass(verdict))", "(!remoteCapability || !remoteAuthorityValidator || !remoteCommitVerifier)", "(dryRun)"]。另有实际 review-bundle 分支在所选模式/权限 guard 之前调用其他接口，不能把后续 guard 推广为整个函数无本地 IO 的保证。远端命令接口的实际 Git 首参数为 ["push"]；注入 callback、授权结果、命令执行及远端后置条件保持未知。 原关系：`/functional_chains/2/pattern`。
- 所选回调到达实际条件 (remediationStatus === "FIXED") 且前序 await 正常完成时，源码先调用 supersession 接口，再调用 lineage 接口；前一接口向已绑定事件写者传递的字面字段为 [{"type":"job_superseded","reason":"external_remediation_fixed"}]。后续 queue 入参中与该事件共享同一词法输入的字段为 [{"event_field":"jobId","queue_field":"/metadata/originJobId","input":"jobId"},{"event_field":"jobId","queue_field":"/metadata/sourceContext/remediation/previousJobId","input":"jobId"},{"event_field":"jobId","queue_field":"/metadata/sourceContext/retry/previousJobId","input":"jobId"},{"event_field":"project","queue_field":"/projectId","input":"project"}]；lineage helper 内的提前返回、抛出及外部操作失败仍可阻止实际入队。 原关系：`/functional_chains/12/pattern`。

### winwincode

保存评估 `{"all_operations_authorized_proven":false,"explanation_generated_from_actual_operations":true,"functional_coverage_percentage_computed":false,"method_names_used_to_infer_responsibility":false,"reference_report_text_used_as_evidence":false,"runtime_or_physical_effects_verified":false,"source_directories_used_to_assign_responsibility":false,"state":"finite_source_responsibility_explanations_available","unique_fact_owner_proven":false,"whole_report_reproduced":false,"whole_repository_ownership_proven":false}`；操作抽取预算 `{"incomplete":false,"limits":{"operations":16384,"relationships":32768,"selected_declarations":512,"source_references_per_operation":96,"source_text_characters":384,"visited_nodes":262144},"operations":10023,"relationships":6004,"visited_nodes":50811}`。

实际解释缺口 `[{"code":"responsibility_selected_declaration_unavailable","file":"apps/client/src/generated/control-plane-client.ts","source_gaps":[{"code":"support_input_only","file":"apps/client/src/generated/control-plane-client.ts","line":0,"message":"已解析实现源码匹配 0 项；辅助输入不充当实现。"}],"symbol":"createControlPlaneHttpClient"}]`；正文来源缺口 `[]`。缺口按原值保留，不以已有正文覆盖。

[自动报告正文](winwincode-automatic-report.md)；[全部具体职责与来源](winwincode-automatic-report.json#/architecture/responsibility_explanations)。

- 所选命令「delivery.update_spec」的生成 TypeScript 记录按「DeliveryUpdateSpecCommand → payload:DeliveryUpdateSpecPayload → spec:DeliverySpecInput」组织字段「verificationCommand」（optional=true）。已认证 Serde 模型将它映射到 Rust 字段「verification_command:Option<String>」，缺失值为「None」，源属性为「#[serde(default, skip_serializing_if = "Option::is_none")]；#[serde(rename = "verificationCommand")]」。在原普通 JSON/已认证 Serde 及成功消息模型条件下，实际「POST /api/v1/commands」序列化记录与 Server 的同一路径解码/dispatcher 记录相接，typed variant 为「DeliveryUpdateSpecCommand」。这是所选协议字段与消息关系，不把 HTTP 已发生、所有 query/WS codec 或跨语言普通调用当成已证明。 原关系：`/judgments/1/adapter_judgments/0/evidence/0/details`。

所选文档描述 Control Plane 内部唯一模型路由及 Worker 仅经模型流；所选 Device 源码另有本地 provider 选择、字节 material 容器与调用来源，表述需要说明部署范围。

- 文档明确限定Control Plane内部唯一；所选Device源码另有本地provider装配、消费及凭据字节操作来源，宜补充部署分支说明，不能把内部唯一扩成全项目唯一。 保存状态：`selected_document_wording_requires_device_deployment_qualification`。
- 文档谈长期Credential；所选代码来源为Vec<u8>/ResolvedSecret字节容器，字节材料与凭据引用须区分，也无法据此确定凭据长期性或公开Delivery密钥泄露。 保存状态：`material_source_distinguished_lifetime_unknown`。
- Worker源码在本地消费者返回Ok(true)时提前返回；正常未消费分支走transport，错误可提前传播。仍使用ExecutionPort消息，不能由本地provider路径推断绕过模型流协议。 保存状态：`local_source_route_does_not_prove_stream_protocol_bypass`。

原文、限定范围、来源事实及必要未知：`/functional_chains/3/pattern`。


旧 pending/assignment、finalizer、不同重试预算、opaque supervisor、导航与提交环境、Device/Chat/local 分支及失败操作仍各自限制结论。

## 主要链、结构与全文范围

正式报告有 36 个所选主要链条目；源码关系状态为 `{"scoped_source_relations_supported":36}`。其中 `captured_source_structure_supported=true` 为 36 项，`scoped_source_supported=true` 为 36 项。结构抽取与包含实际装配/guard 的源码支持是不同字段；partial 条目保留具体缺段。

这些条目描述所选声明和正常分支的静态关系，均不自动证明完整运行功能。相同源 selector 的重叠在自动报告单列，不累计为额外能力；目录、依赖图、解析文件及 AST anchor 数量也不构成功能覆盖率。

## 本轮保存的具体条件与字段关系

以下只复制正式报告的关系投影，包含实际门条件、状态枚举、记录字段与必要未知；不是根据规则名生成新结论。完整表达式、source facts 与反证以相应 JSON Pointer 为准。

### `cpb-captured-record-resource-writers`

保存状态 `scoped_source_relations_supported`；保存缺口 `[]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/0/pattern/scoped_source_supported](codepatchbay-automatic-report.json#/functional_chains/0/pattern/scoped_source_supported) |
| relation_component_version | captured-lifecycle-ownership-relations-1 | [/functional_chains/0/pattern/relation_component_version](codepatchbay-automatic-report.json#/functional_chains/0/pattern/relation_component_version) |
| responsibility_interpretation | Selected captured functions write the recorded lexical fields and pass the recorded arguments; directory names assign no responsibility. | [/functional_chains/0/pattern/responsibility_interpretation](codepatchbay-automatic-report.json#/functional_chains/0/pattern/responsibility_interpretation) |
| source_rejection_guard_fact_ids/shown_items/0 | 0a83225f1f97849f999b1fab | [/functional_chains/0/pattern/source_rejection_guard_fact_ids](codepatchbay-automatic-report.json#/functional_chains/0/pattern/source_rejection_guard_fact_ids) |
| source_rejection_guard_fact_ids/shown_items/1 | 390e9f81225c29699239d6d0 | [/functional_chains/0/pattern/source_rejection_guard_fact_ids](codepatchbay-automatic-report.json#/functional_chains/0/pattern/source_rejection_guard_fact_ids) |
| source_rejection_guard_fact_ids/shown_items/2 | 009946731b8fe01af5c797db | [/functional_chains/0/pattern/source_rejection_guard_fact_ids](codepatchbay-automatic-report.json#/functional_chains/0/pattern/source_rejection_guard_fact_ids) |
| source_rejection_guard_fact_ids/shown_items/3 | 3a244e9f76a5ee5bdb2dc242 | [/functional_chains/0/pattern/source_rejection_guard_fact_ids](codepatchbay-automatic-report.json#/functional_chains/0/pattern/source_rejection_guard_fact_ids) |
| source_rejection_guard_fact_ids/shown_items/4 | a43ae706fec70f2e63c2082b | [/functional_chains/0/pattern/source_rejection_guard_fact_ids](codepatchbay-automatic-report.json#/functional_chains/0/pattern/source_rejection_guard_fact_ids) |
| source_rejection_guard_fact_ids/shown_items/5 | e6fd9fed5f97272f98519c01 | [/functional_chains/0/pattern/source_rejection_guard_fact_ids](codepatchbay-automatic-report.json#/functional_chains/0/pattern/source_rejection_guard_fact_ids) |
| source_rejection_guard_fact_ids/shown_count | 6 | [/functional_chains/0/pattern/source_rejection_guard_fact_ids](codepatchbay-automatic-report.json#/functional_chains/0/pattern/source_rejection_guard_fact_ids) |
| source_rejection_guard_fact_ids/total_count | 16 | [/functional_chains/0/pattern/source_rejection_guard_fact_ids](codepatchbay-automatic-report.json#/functional_chains/0/pattern/source_rejection_guard_fact_ids) |
| source_rejection_guard_fact_ids/truncated | true | [/functional_chains/0/pattern/source_rejection_guard_fact_ids](codepatchbay-automatic-report.json#/functional_chains/0/pattern/source_rejection_guard_fact_ids) |
| all_mutations_authorized_proven | false | [/functional_chains/0/pattern/all_mutations_authorized_proven](codepatchbay-automatic-report.json#/functional_chains/0/pattern/all_mutations_authorized_proven) |
| all_storage_resources_bound_proven | false | [/functional_chains/0/pattern/all_storage_resources_bound_proven](codepatchbay-automatic-report.json#/functional_chains/0/pattern/all_storage_resources_bound_proven) |
| call_record_and_effect_frontiers/shown_items/0/activation_and_physical_effect_proven | false | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/kind | identifier | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/location/file | server/services/event/event-store.ts | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/location/line | 1180 | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/location/column | 46 | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/location/end_line | 1180 | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/location/start_byte | 39869 | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/location/end_byte | 39874 | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/name | event | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/1/kind | identifier | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |

完整关系 [/functional_chains/0/pattern](codepatchbay-automatic-report.json#/functional_chains/0/pattern)；原 source facts [/functional_chains/0/source_facts](codepatchbay-automatic-report.json#/functional_chains/0/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### `cpb-event-index-projection`

保存状态 `scoped_source_relations_supported`；保存缺口 `[{"code":"record_projection_physical_commit_and_all_recovery_not_proven","source_only":true}]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| relation_witnesses/event_serializer_result_is_actual_durable_writer_argument | true | [/functional_chains/1/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/1/pattern/relation_witnesses) |
| relation_witnesses/append_calls_selected_durable_writer | true | [/functional_chains/1/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/1/pattern/relation_witnesses) |
| relation_witnesses/event_append_precedes_index_refresh_on_normal_reaching | true | [/functional_chains/1/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/1/pattern/relation_witnesses) |
| relation_witnesses/index_rebuild_calls_same_index_writer | true | [/functional_chains/1/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/1/pattern/relation_witnesses) |
| relation_witnesses/index_refresh_calls_selected_updater | true | [/functional_chains/1/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/1/pattern/relation_witnesses) |
| relation_witnesses/index_update_calls_selected_index_writer | true | [/functional_chains/1/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/1/pattern/relation_witnesses) |
| relation_witnesses/locked_projection_supplies_literal_update_callback | true | [/functional_chains/1/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/1/pattern/relation_witnesses) |
| relation_witnesses/projection_callback_state_is_written_to_same_index_record | true | [/functional_chains/1/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/1/pattern/relation_witnesses) |
| relation_witnesses/projection_returns_explicit_state_field | true | [/functional_chains/1/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/1/pattern/relation_witnesses) |
| relation_witnesses/read_events_materialized_state_flows_to_rebuilt_index_writer | true | [/functional_chains/1/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/1/pattern/relation_witnesses) |
| relation_witnesses/retry_has_captured_catch | true | [/functional_chains/1/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/1/pattern/relation_witnesses) |
| scoped_source_supported | true | [/functional_chains/1/pattern/scoped_source_supported](codepatchbay-automatic-report.json#/functional_chains/1/pattern/scoped_source_supported) |
| guards/append/shown_items/0/condition/kind | binary_expression | [/functional_chains/1/pattern/guards/append](codepatchbay-automatic-report.json#/functional_chains/1/pattern/guards/append) |
| guards/append/shown_items/0/condition/location/file | server/services/event/event-store.ts | [/functional_chains/1/pattern/guards/append](codepatchbay-automatic-report.json#/functional_chains/1/pattern/guards/append) |
| guards/append/shown_items/0/condition/location/line | 1191 | [/functional_chains/1/pattern/guards/append](codepatchbay-automatic-report.json#/functional_chains/1/pattern/guards/append) |
| guards/append/shown_items/0/condition/location/column | 9 | [/functional_chains/1/pattern/guards/append](codepatchbay-automatic-report.json#/functional_chains/1/pattern/guards/append) |
| guards/append/shown_items/0/condition/location/end_line | 1191 | [/functional_chains/1/pattern/guards/append](codepatchbay-automatic-report.json#/functional_chains/1/pattern/guards/append) |
| guards/append/shown_items/0/condition/location/start_byte | 40398 | [/functional_chains/1/pattern/guards/append](codepatchbay-automatic-report.json#/functional_chains/1/pattern/guards/append) |
| guards/append/shown_items/0/condition/location/end_byte | 40417 | [/functional_chains/1/pattern/guards/append](codepatchbay-automatic-report.json#/functional_chains/1/pattern/guards/append) |
| guards/append/shown_items/0/condition/reference_dependencies_only | true | [/functional_chains/1/pattern/guards/append](codepatchbay-automatic-report.json#/functional_chains/1/pattern/guards/append) |
| guards/append/shown_items/0/condition/reference_path | null | [/functional_chains/1/pattern/guards/append](codepatchbay-automatic-report.json#/functional_chains/1/pattern/guards/append) |
| guards/append/shown_items/0/condition/references/0/state | unique | [/functional_chains/1/pattern/guards/append](codepatchbay-automatic-report.json#/functional_chains/1/pattern/guards/append) |
| guards/append/shown_items/0/condition/references/0/binder_location/file | server/services/event/event-store.ts | [/functional_chains/1/pattern/guards/append](codepatchbay-automatic-report.json#/functional_chains/1/pattern/guards/append) |
| guards/append/shown_items/0/condition/references/0/binder_location/line | 1190 | [/functional_chains/1/pattern/guards/append](codepatchbay-automatic-report.json#/functional_chains/1/pattern/guards/append) |

完整关系 [/functional_chains/1/pattern](codepatchbay-automatic-report.json#/functional_chains/1/pattern)；原 source facts [/functional_chains/1/source_facts](codepatchbay-automatic-report.json#/functional_chains/1/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### `cpb-finalizer-conditional-publication`

保存状态 `scoped_source_relations_supported`；保存缺口 `[]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

`rows`；完整 [/functional_chains/2/pattern/finite_mode_permission_relation/rows](codepatchbay-automatic-report.json#/functional_chains/2/pattern/finite_mode_permission_relation/rows)；保存总行数 `20`。

| prefix_guard_values_complete | selected_prefix_guard_blocks | boolean_input_cells | mode_cell | plan_is_not_actual_remote_effect | source_plan_fields | 完整行 |
| --- | --- | --- | --- | --- | --- | --- |
| true | null | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":false,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":false} | dry-run | true | {"closeIssue":false,"commit":false,"merge":false,"pullRequest":false,"pullRequestPreview":true,"push":false} | [/functional_chains/2/pattern/finite_mode_permission_relation/rows/0](codepatchbay-automatic-report.json#/functional_chains/2/pattern/finite_mode_permission_relation/rows/0) |
| true | null | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":false,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":true} | dry-run | true | {"closeIssue":false,"commit":false,"merge":false,"pullRequest":false,"pullRequestPreview":true,"push":false} | [/functional_chains/2/pattern/finite_mode_permission_relation/rows/1](codepatchbay-automatic-report.json#/functional_chains/2/pattern/finite_mode_permission_relation/rows/1) |
| true | null | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":true,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":false} | dry-run | true | {"closeIssue":false,"commit":false,"merge":false,"pullRequest":false,"pullRequestPreview":true,"push":false} | [/functional_chains/2/pattern/finite_mode_permission_relation/rows/2](codepatchbay-automatic-report.json#/functional_chains/2/pattern/finite_mode_permission_relation/rows/2) |
| true | null | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":true,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":true} | dry-run | true | {"closeIssue":false,"commit":false,"merge":false,"pullRequest":false,"pullRequestPreview":true,"push":false} | [/functional_chains/2/pattern/finite_mode_permission_relation/rows/3](codepatchbay-automatic-report.json#/functional_chains/2/pattern/finite_mode_permission_relation/rows/3) |
| true | ad8f8a73a416c456f70ca619 | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":false,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":false} | local | true | {"closeIssue":false,"commit":{"unknown":true,"source_expression":{"kind":"binary","left":{"kind":"not","operand":{"kind":"binary","left":{"kind":"input","name":"mode"},"operator":"===","right":{"kind":"literal","value":"dry-run"}}},"operator":"&amp;&amp;","right":{"kind":"binary","left":{"key":"length","kind":"get","object":{"actual_target_role":null,"arguments":[{"actual_target_role":{"omitted_for_presentation":true,"full_value_ref":"/functional_chains/2/pattern/finite_mode_permission_relation/rows/4/source_plan_fields/commit/source_expression/right/left/object/arguments/0/actual_target_role"},"argum…（显示省略） | [/functional_chains/2/pattern/finite_mode_permission_relation/rows/4](codepatchbay-automatic-report.json#/functional_chains/2/pattern/finite_mode_permission_relation/rows/4) |
| true | null | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":false,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":true} | local | true | {"closeIssue":false,"commit":{"unknown":true,"source_expression":{"kind":"binary","left":{"kind":"not","operand":{"kind":"binary","left":{"kind":"input","name":"mode"},"operator":"===","right":{"kind":"literal","value":"dry-run"}}},"operator":"&amp;&amp;","right":{"kind":"binary","left":{"key":"length","kind":"get","object":{"actual_target_role":null,"arguments":[{"actual_target_role":{"omitted_for_presentation":true,"full_value_ref":"/functional_chains/2/pattern/finite_mode_permission_relation/rows/5/source_plan_fields/commit/source_expression/right/left/object/arguments/0/actual_target_role"},"argum…（显示省略） | [/functional_chains/2/pattern/finite_mode_permission_relation/rows/5](codepatchbay-automatic-report.json#/functional_chains/2/pattern/finite_mode_permission_relation/rows/5) |
| true | null | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":true,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":false} | local | true | {"closeIssue":false,"commit":{"unknown":true,"source_expression":{"kind":"binary","left":{"kind":"not","operand":{"kind":"binary","left":{"kind":"input","name":"mode"},"operator":"===","right":{"kind":"literal","value":"dry-run"}}},"operator":"&amp;&amp;","right":{"kind":"binary","left":{"key":"length","kind":"get","object":{"actual_target_role":null,"arguments":[{"actual_target_role":{"omitted_for_presentation":true,"full_value_ref":"/functional_chains/2/pattern/finite_mode_permission_relation/rows/6/source_plan_fields/commit/source_expression/right/left/object/arguments/0/actual_target_role"},"argum…（显示省略） | [/functional_chains/2/pattern/finite_mode_permission_relation/rows/6](codepatchbay-automatic-report.json#/functional_chains/2/pattern/finite_mode_permission_relation/rows/6) |
| true | null | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":true,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":true} | local | true | {"closeIssue":false,"commit":{"unknown":true,"source_expression":{"kind":"binary","left":{"kind":"not","operand":{"kind":"binary","left":{"kind":"input","name":"mode"},"operator":"===","right":{"kind":"literal","value":"dry-run"}}},"operator":"&amp;&amp;","right":{"kind":"binary","left":{"key":"length","kind":"get","object":{"actual_target_role":null,"arguments":[{"actual_target_role":{"omitted_for_presentation":true,"full_value_ref":"/functional_chains/2/pattern/finite_mode_permission_relation/rows/7/source_plan_fields/commit/source_expression/right/left/object/arguments/0/actual_target_role"},"argum…（显示省略） | [/functional_chains/2/pattern/finite_mode_permission_relation/rows/7](codepatchbay-automatic-report.json#/functional_chains/2/pattern/finite_mode_permission_relation/rows/7) |
| true | ad8f8a73a416c456f70ca619 | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":false,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":false} | pr | true | {"closeIssue":false,"commit":{"unknown":true,"source_expression":{"kind":"binary","left":{"kind":"not","operand":{"kind":"binary","left":{"kind":"input","name":"mode"},"operator":"===","right":{"kind":"literal","value":"dry-run"}}},"operator":"&amp;&amp;","right":{"kind":"binary","left":{"key":"length","kind":"get","object":{"actual_target_role":null,"arguments":[{"actual_target_role":{"omitted_for_presentation":true,"full_value_ref":"/functional_chains/2/pattern/finite_mode_permission_relation/rows/8/source_plan_fields/commit/source_expression/right/left/object/arguments/0/actual_target_role"},"argum…（显示省略） | [/functional_chains/2/pattern/finite_mode_permission_relation/rows/8](codepatchbay-automatic-report.json#/functional_chains/2/pattern/finite_mode_permission_relation/rows/8) |
| true | null | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":false,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":true} | pr | true | {"closeIssue":false,"commit":{"unknown":true,"source_expression":{"kind":"binary","left":{"kind":"not","operand":{"kind":"binary","left":{"kind":"input","name":"mode"},"operator":"===","right":{"kind":"literal","value":"dry-run"}}},"operator":"&amp;&amp;","right":{"kind":"binary","left":{"key":"length","kind":"get","object":{"actual_target_role":null,"arguments":[{"actual_target_role":{"omitted_for_presentation":true,"full_value_ref":"/functional_chains/2/pattern/finite_mode_permission_relation/rows/9/source_plan_fields/commit/source_expression/right/left/object/arguments/0/actual_target_role"},"argum…（显示省略） | [/functional_chains/2/pattern/finite_mode_permission_relation/rows/9](codepatchbay-automatic-report.json#/functional_chains/2/pattern/finite_mode_permission_relation/rows/9) |
| true | null | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":true,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":false} | pr | true | {"closeIssue":false,"commit":{"unknown":true,"source_expression":{"kind":"binary","left":{"kind":"not","operand":{"kind":"binary","left":{"kind":"input","name":"mode"},"operator":"===","right":{"kind":"literal","value":"dry-run"}}},"operator":"&amp;&amp;","right":{"kind":"binary","left":{"key":"length","kind":"get","object":{"actual_target_role":null,"arguments":[{"actual_target_role":{"omitted_for_presentation":true,"full_value_ref":"/functional_chains/2/pattern/finite_mode_permission_relation/rows/10/source_plan_fields/commit/source_expression/right/left/object/arguments/0/actual_target_role"},"argu…（显示省略） | [/functional_chains/2/pattern/finite_mode_permission_relation/rows/10](codepatchbay-automatic-report.json#/functional_chains/2/pattern/finite_mode_permission_relation/rows/10) |
| true | null | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":true,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":true} | pr | true | {"closeIssue":false,"commit":{"unknown":true,"source_expression":{"kind":"binary","left":{"kind":"not","operand":{"kind":"binary","left":{"kind":"input","name":"mode"},"operator":"===","right":{"kind":"literal","value":"dry-run"}}},"operator":"&amp;&amp;","right":{"kind":"binary","left":{"key":"length","kind":"get","object":{"actual_target_role":null,"arguments":[{"actual_target_role":{"omitted_for_presentation":true,"full_value_ref":"/functional_chains/2/pattern/finite_mode_permission_relation/rows/11/source_plan_fields/commit/source_expression/right/left/object/arguments/0/actual_target_role"},"argu…（显示省略） | [/functional_chains/2/pattern/finite_mode_permission_relation/rows/11](codepatchbay-automatic-report.json#/functional_chains/2/pattern/finite_mode_permission_relation/rows/11) |
表格为显示子集；省略项和原条件见完整表指针，不作为分析缺口。

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| statement/text | 源码实际模式字面量为 ["dry-run", "local", "pr", "remote"]，声明的 plan 字段为 ["closeIssue", "commit", "merge", "pullRequest", "pullRequestPreview", "push"]。有限表组合这些模式与源码中的布尔 opt-in，并保留字段 unknown；plan 不是已发生的写入。PR 调用的真实选项绑定到 callee 形参后，源码中早于条件 transport 且成立时  | [/functional_chains/2/pattern/statement](codepatchbay-automatic-report.json#/functional_chains/2/pattern/statement) |
| statement/truncated | true | [/functional_chains/2/pattern/statement](codepatchbay-automatic-report.json#/functional_chains/2/pattern/statement) |
| statement/original_characters | 517 | [/functional_chains/2/pattern/statement](codepatchbay-automatic-report.json#/functional_chains/2/pattern/statement) |
| interpretation | 区分的是实际枚举/opt-in 条件、PR 提前返回和源码发布接口；配置允许与真实外写成功是不同证据。可空通用 callback 的默认值与所选 caller 提供的字段另列，未推广为全项目必然授权。 | [/functional_chains/2/pattern/interpretation](codepatchbay-automatic-report.json#/functional_chains/2/pattern/interpretation) |
| relation_witnesses/0/conditions/0/condition/kind | binary_expression | [/functional_chains/2/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/2/pattern/relation_witnesses) |
| relation_witnesses/0/conditions/0/condition/location/file | server/services/auto-finalizer.ts | [/functional_chains/2/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/2/pattern/relation_witnesses) |
| relation_witnesses/0/conditions/0/condition/location/line | 2195 | [/functional_chains/2/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/2/pattern/relation_witnesses) |
| relation_witnesses/0/conditions/0/condition/location/column | 7 | [/functional_chains/2/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/2/pattern/relation_witnesses) |
| relation_witnesses/0/conditions/0/condition/location/end_line | 2195 | [/functional_chains/2/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/2/pattern/relation_witnesses) |
| relation_witnesses/0/conditions/0/condition/location/start_byte | 79710 | [/functional_chains/2/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/2/pattern/relation_witnesses) |
| relation_witnesses/0/conditions/0/condition/location/end_byte | 79745 | [/functional_chains/2/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/2/pattern/relation_witnesses) |
| relation_witnesses/0/conditions/0/condition/operands/0/kind | binary_expression | [/functional_chains/2/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/2/pattern/relation_witnesses) |
| relation_witnesses/0/conditions/0/condition/operands/0/location/file | server/services/auto-finalizer.ts | [/functional_chains/2/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/2/pattern/relation_witnesses) |
| relation_witnesses/0/conditions/0/condition/operands/0/location/line | 2195 | [/functional_chains/2/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/2/pattern/relation_witnesses) |
| relation_witnesses/0/conditions/0/condition/operands/0/location/column | 7 | [/functional_chains/2/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/2/pattern/relation_witnesses) |
| relation_witnesses/0/conditions/0/condition/operands/0/location/end_line | 2195 | [/functional_chains/2/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/2/pattern/relation_witnesses) |
| relation_witnesses/0/conditions/0/condition/operands/0/location/start_byte | 79710 | [/functional_chains/2/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/2/pattern/relation_witnesses) |
| relation_witnesses/0/conditions/0/condition/operands/0/location/end_byte | 79723 | [/functional_chains/2/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/2/pattern/relation_witnesses) |
| relation_witnesses/0/conditions/0/condition/operands/0/operands/0/kind | 显示投影省略 | [/functional_chains/2/pattern/relation_witnesses/0/conditions/0/condition/operands/0/operands/0/kind](codepatchbay-automatic-report.json#/functional_chains/2/pattern/relation_witnesses/0/conditions/0/condition/operands/0/operands/0/kind) |
| relation_witnesses/0/conditions/0/condition/operands/0/operands/0/location | 显示投影省略 | [/functional_chains/2/pattern/relation_witnesses/0/conditions/0/condition/operands/0/operands/0/location](codepatchbay-automatic-report.json#/functional_chains/2/pattern/relation_witnesses/0/conditions/0/condition/operands/0/operands/0/location) |
| relation_witnesses/0/conditions/0/condition/operands/0/operands/0/name | 显示投影省略 | [/functional_chains/2/pattern/relation_witnesses/0/conditions/0/condition/operands/0/operands/0/name](codepatchbay-automatic-report.json#/functional_chains/2/pattern/relation_witnesses/0/conditions/0/condition/operands/0/operands/0/name) |
| relation_witnesses/0/conditions/0/condition/operands/0/operands/1/kind | 显示投影省略 | [/functional_chains/2/pattern/relation_witnesses/0/conditions/0/condition/operands/0/operands/1/kind](codepatchbay-automatic-report.json#/functional_chains/2/pattern/relation_witnesses/0/conditions/0/condition/operands/0/operands/1/kind) |
| relation_witnesses/0/conditions/0/condition/operands/0/operands/1/literal | 显示投影省略 | [/functional_chains/2/pattern/relation_witnesses/0/conditions/0/condition/operands/0/operands/1/literal](codepatchbay-automatic-report.json#/functional_chains/2/pattern/relation_witnesses/0/conditions/0/condition/operands/0/operands/1/literal) |
| relation_witnesses/0/conditions/0/condition/operands/0/operands/1/location | 显示投影省略 | [/functional_chains/2/pattern/relation_witnesses/0/conditions/0/condition/operands/0/operands/1/location](codepatchbay-automatic-report.json#/functional_chains/2/pattern/relation_witnesses/0/conditions/0/condition/operands/0/operands/1/location) |

完整关系 [/functional_chains/2/pattern](codepatchbay-automatic-report.json#/functional_chains/2/pattern)；原 source facts [/functional_chains/2/source_facts](codepatchbay-automatic-report.json#/functional_chains/2/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### `cpb-report-access-audit-response`

保存状态 `scoped_source_relations_supported`；保存缺口 `[]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/3/pattern/scoped_source_supported](codepatchbay-automatic-report.json#/functional_chains/3/pattern/scoped_source_supported) |
| source_return_conditions_computed | true | [/functional_chains/3/pattern/source_return_conditions_computed](codepatchbay-automatic-report.json#/functional_chains/3/pattern/source_return_conditions_computed) |
| all_project_functionality_proven | false | [/functional_chains/3/pattern/all_project_functionality_proven](codepatchbay-automatic-report.json#/functional_chains/3/pattern/all_project_functionality_proven) |
| budgets/summary_path_limit | 256 | [/functional_chains/3/pattern/budgets](codepatchbay-automatic-report.json#/functional_chains/3/pattern/budgets) |
| budgets/truncated | false | [/functional_chains/3/pattern/budgets](codepatchbay-automatic-report.json#/functional_chains/3/pattern/budgets) |
| groups/access_audit/scoped_source_supported | true | [/functional_chains/3/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/3/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/conditions/0 | the captured registered request callback is invoked and reaches the awaited audit call | [/functional_chains/3/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/3/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/conditions/1 | the selected opener, callback and response writer declarations are active | [/functional_chains/3/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/3/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/conditions/2 | the audit await rejects or throws and catch logging completes normally | [/functional_chains/3/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/3/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/conditions/3 | normal plain response object properties; no getters, Proxy or external mutation | [/functional_chains/3/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/3/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/conditions/4 | intervening header operations and the response writer complete normally | [/functional_chains/3/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/3/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/conditional_gate_version | captured-conditional-gate-relations-1 | [/functional_chains/3/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/3/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/opener_result_declaration_id | 19efdab5e3e1669abe3d093426107c50a993a391f86e0560d98a150e00cd26dc | [/functional_chains/3/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/3/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/actual_awaited_method | append | [/functional_chains/3/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/3/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/actual_http_response_delivery_proven | false | [/functional_chains/3/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/3/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/actual_response_writer_call/result_binding_source | null | [/functional_chains/3/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/3/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/actual_response_writer_call/actual_callee_graph_node_id | ts:server/index#sendJson | [/functional_chains/3/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/3/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/actual_response_writer_call/arguments/0/kind | identifier | [/functional_chains/3/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/3/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/actual_response_writer_call/arguments/0/location/file | server/index.ts | [/functional_chains/3/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/3/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/actual_response_writer_call/arguments/0/location/line | 444 | [/functional_chains/3/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/3/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/actual_response_writer_call/arguments/0/location/column | 14 | [/functional_chains/3/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/3/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/actual_response_writer_call/arguments/0/location/end_line | 444 | [/functional_chains/3/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/3/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/actual_response_writer_call/arguments/0/location/start_byte | 16557 | [/functional_chains/3/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/3/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/actual_response_writer_call/arguments/0/location/end_byte | 16562 | [/functional_chains/3/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/3/pattern/groups) |

完整关系 [/functional_chains/3/pattern](codepatchbay-automatic-report.json#/functional_chains/3/pattern)；原 source facts [/functional_chains/3/source_facts](codepatchbay-automatic-report.json#/functional_chains/3/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### `cpb-report-completion-gate-conditions`

保存状态 `scoped_source_relations_supported`；保存缺口 `[]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

`absent_input_partitions`；完整 [/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/absent_input_partitions](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/absent_input_partitions)；保存总行数 `2`。

| boolean_result | input_cell | unknown | 完整行 |
| --- | --- | --- | --- |
| false | missing | false | [/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/absent_input_partitions/0](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/absent_input_partitions/0) |
| false | null | false | [/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/absent_input_partitions/1](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/absent_input_partitions/1) |

`record_partitions`；完整 [/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions)；保存总行数 `9`。

| boolean_result | property_cells | unknown | 完整行 |
| --- | --- | --- | --- |
| false | {"planMode":"none","workflow":"docs"} | false | [/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/0](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/0) |
| false | {"planMode":"none","workflow":"readonly"} | false | [/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/1](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/1) |
| false | {"planMode":"none","workflow":"&lt;other-than-captured-literals&gt;"} | false | [/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/2](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/2) |
| false | {"planMode":"parent","workflow":"docs"} | false | [/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/3](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/3) |
| false | {"planMode":"parent","workflow":"readonly"} | false | [/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/4](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/4) |
| false | {"planMode":"parent","workflow":"&lt;other-than-captured-literals&gt;"} | false | [/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/5](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/5) |
| false | {"planMode":"&lt;other-than-captured-literals&gt;","workflow":"docs"} | false | [/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/6](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/6) |
| false | {"planMode":"&lt;other-than-captured-literals&gt;","workflow":"readonly"} | false | [/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/7](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/7) |
| true | {"planMode":"&lt;other-than-captured-literals&gt;","workflow":"&lt;other-than-captured-literals&gt;"} | false | [/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/8](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/8) |

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/5/pattern/scoped_source_supported](codepatchbay-automatic-report.json#/functional_chains/5/pattern/scoped_source_supported) |
| source_return_conditions_computed | true | [/functional_chains/5/pattern/source_return_conditions_computed](codepatchbay-automatic-report.json#/functional_chains/5/pattern/source_return_conditions_computed) |
| all_project_functionality_proven | false | [/functional_chains/5/pattern/all_project_functionality_proven](codepatchbay-automatic-report.json#/functional_chains/5/pattern/all_project_functionality_proven) |
| budgets/summary_path_limit | 256 | [/functional_chains/5/pattern/budgets](codepatchbay-automatic-report.json#/functional_chains/5/pattern/budgets) |
| budgets/truncated | false | [/functional_chains/5/pattern/budgets](codepatchbay-automatic-report.json#/functional_chains/5/pattern/budgets) |
| groups/completion/statement | Return records, local condition dependencies and source order are computed separately. Path conditions retain prior short circuits; local conditions describe the current gate only. No target inputs were executed. | [/functional_chains/5/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups) |
| groups/completion/scoped_source_supported | true | [/functional_chains/5/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups) |
| groups/completion/condition_consumers/shown_items/0/condition_abstract_form/kind | input | [/functional_chains/5/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/condition_abstract_form/name | checklist | [/functional_chains/5/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/condition_source/kind | identifier | [/functional_chains/5/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/condition_source/location/file | core/engine/completion-gate.ts | [/functional_chains/5/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/condition_source/location/line | 182 | [/functional_chains/5/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/condition_source/location/column | 7 | [/functional_chains/5/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/condition_source/location/end_line | 182 | [/functional_chains/5/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/condition_source/location/start_byte | 6306 | [/functional_chains/5/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/condition_source/location/end_byte | 6315 | [/functional_chains/5/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/condition_source/name | checklist | [/functional_chains/5/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/condition_variants/0/kind | input | [/functional_chains/5/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/condition_variants/0/name | checklist | [/functional_chains/5/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/conditional_gate_version | captured-conditional-gate-relations-1 | [/functional_chains/5/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/affected_return_fact_ids/0 | c7672db417aa9a3e0a4efab9 | [/functional_chains/5/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/branch_runtime_selected | false | [/functional_chains/5/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/kind | completion_gate_condition_consumes_result | [/functional_chains/5/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/location/file | core/engine/completion-gate.ts | [/functional_chains/5/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/5/pattern/groups/completion/condition_consumers) |

完整关系 [/functional_chains/5/pattern](codepatchbay-automatic-report.json#/functional_chains/5/pattern)；原 source facts [/functional_chains/5/source_facts](codepatchbay-automatic-report.json#/functional_chains/5/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### `cpb-report-readiness-abrupt-guard`

保存状态 `scoped_source_relations_supported`；保存缺口 `[]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

`absent_input_partitions`；完整 [/functional_chains/9/pattern/groups/readiness/predicate_finite_partition/absent_input_partitions](codepatchbay-automatic-report.json#/functional_chains/9/pattern/groups/readiness/predicate_finite_partition/absent_input_partitions)；保存总行数 `2`。

| boolean_result | input_cell | unknown | 完整行 |
| --- | --- | --- | --- |
| null | missing | true | [/functional_chains/9/pattern/groups/readiness/predicate_finite_partition/absent_input_partitions/0](codepatchbay-automatic-report.json#/functional_chains/9/pattern/groups/readiness/predicate_finite_partition/absent_input_partitions/0) |
| null | null | true | [/functional_chains/9/pattern/groups/readiness/predicate_finite_partition/absent_input_partitions/1](codepatchbay-automatic-report.json#/functional_chains/9/pattern/groups/readiness/predicate_finite_partition/absent_input_partitions/1) |

`record_partitions`；完整 [/functional_chains/9/pattern/groups/readiness/predicate_finite_partition/record_partitions](codepatchbay-automatic-report.json#/functional_chains/9/pattern/groups/readiness/predicate_finite_partition/record_partitions)；保存总行数 `2`。

| boolean_result | property_cells | unknown | 完整行 |
| --- | --- | --- | --- |
| true | {"ok":false} | false | [/functional_chains/9/pattern/groups/readiness/predicate_finite_partition/record_partitions/0](codepatchbay-automatic-report.json#/functional_chains/9/pattern/groups/readiness/predicate_finite_partition/record_partitions/0) |
| false | {"ok":"&lt;other-than-captured-literals&gt;"} | false | [/functional_chains/9/pattern/groups/readiness/predicate_finite_partition/record_partitions/1](codepatchbay-automatic-report.json#/functional_chains/9/pattern/groups/readiness/predicate_finite_partition/record_partitions/1) |

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/9/pattern/scoped_source_supported](codepatchbay-automatic-report.json#/functional_chains/9/pattern/scoped_source_supported) |
| source_return_conditions_computed | true | [/functional_chains/9/pattern/source_return_conditions_computed](codepatchbay-automatic-report.json#/functional_chains/9/pattern/source_return_conditions_computed) |
| all_project_functionality_proven | false | [/functional_chains/9/pattern/all_project_functionality_proven](codepatchbay-automatic-report.json#/functional_chains/9/pattern/all_project_functionality_proven) |
| budgets/summary_path_limit | 256 | [/functional_chains/9/pattern/budgets](codepatchbay-automatic-report.json#/functional_chains/9/pattern/budgets) |
| budgets/truncated | false | [/functional_chains/9/pattern/budgets](codepatchbay-automatic-report.json#/functional_chains/9/pattern/budgets) |
| groups/readiness/scoped_source_supported | true | [/functional_chains/9/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/9/pattern/groups) |
| groups/readiness/relations/0/conditions/0 | the selected entry and predicate declarations are active | [/functional_chains/9/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/9/pattern/groups) |
| groups/readiness/relations/0/conditions/1 | the initializer and opaque calls before the return complete normally | [/functional_chains/9/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/9/pattern/groups) |
| groups/readiness/relations/0/conditions/2 | the predicate reads the same stable ordinary result record; no getters, Proxy or external mutation | [/functional_chains/9/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/9/pattern/groups) |
| groups/readiness/relations/0/conditional_gate_version | captured-conditional-gate-relations-1 | [/functional_chains/9/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/9/pattern/groups) |
| groups/readiness/relations/0/actual_predicate_call/result_binding_source | null | [/functional_chains/9/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/9/pattern/groups) |
| groups/readiness/relations/0/actual_predicate_call/actual_callee_graph_node_id | ts:cli/commands/fix#isReadinessFailure | [/functional_chains/9/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/9/pattern/groups) |
| groups/readiness/relations/0/actual_predicate_call/arguments/0/kind | identifier | [/functional_chains/9/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/9/pattern/groups) |
| groups/readiness/relations/0/actual_predicate_call/arguments/0/location/file | cli/commands/fix.ts | [/functional_chains/9/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/9/pattern/groups) |
| groups/readiness/relations/0/actual_predicate_call/arguments/0/location/line | 506 | [/functional_chains/9/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/9/pattern/groups) |
| groups/readiness/relations/0/actual_predicate_call/arguments/0/location/column | 26 | [/functional_chains/9/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/9/pattern/groups) |
| groups/readiness/relations/0/actual_predicate_call/arguments/0/location/end_line | 506 | [/functional_chains/9/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/9/pattern/groups) |
| groups/readiness/relations/0/actual_predicate_call/arguments/0/location/start_byte | 21205 | [/functional_chains/9/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/9/pattern/groups) |
| groups/readiness/relations/0/actual_predicate_call/arguments/0/location/end_byte | 21214 | [/functional_chains/9/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/9/pattern/groups) |
| groups/readiness/relations/0/actual_predicate_call/arguments/0/name | readiness | [/functional_chains/9/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/9/pattern/groups) |
| groups/readiness/relations/0/actual_predicate_call/authenticated_call_edge_id | 04397b66192f668821507c8c | [/functional_chains/9/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/9/pattern/groups) |
| groups/readiness/relations/0/actual_predicate_call/binding_state | authenticated_internal_call | [/functional_chains/9/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/9/pattern/groups) |
| groups/readiness/relations/0/actual_predicate_call/branch_context/0/condition/call_effects_or_result_proven | false | [/functional_chains/9/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/9/pattern/groups) |
| groups/readiness/relations/0/actual_predicate_call/branch_context/0/condition/arguments/0 | 显示投影省略 | [/functional_chains/9/pattern/groups/readiness/relations/0/actual_predicate_call/branch_context/0/condition/arguments/0](codepatchbay-automatic-report.json#/functional_chains/9/pattern/groups/readiness/relations/0/actual_predicate_call/branch_context/0/condition/arguments/0) |

完整关系 [/functional_chains/9/pattern](codepatchbay-automatic-report.json#/functional_chains/9/pattern)；原 source facts [/functional_chains/9/source_facts](codepatchbay-automatic-report.json#/functional_chains/9/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### `cpb-review-fixed-state-lineage`

保存状态 `scoped_source_relations_supported`；保存缺口 `[]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| statement/text | 所选回调到达实际条件 (remediationStatus === "FIXED") 且前序 await 正常完成时，源码先调用 supersession 接口，再调用 lineage 接口；前一接口向已绑定事件写者传递的字面字段为 [{"type":"job_superseded","reason":"external_remediation_fixed"}]。后续 queue 入参中与该事件共享同一词法输入的字段为 [{"event_field":"jobId","que | [/functional_chains/12/pattern/statement](codepatchbay-automatic-report.json#/functional_chains/12/pattern/statement) |
| statement/truncated | true | [/functional_chains/12/pattern/statement](codepatchbay-automatic-report.json#/functional_chains/12/pattern/statement) |
| statement/original_characters | 609 | [/functional_chains/12/pattern/statement](codepatchbay-automatic-report.json#/functional_chains/12/pattern/statement) |
| interpretation | 这里闭合的是实际状态条件、事件字面字段及旧任务到后续任务的字段来源；并未证明回调必然激活、事件持久化成功、每次创建新任务或覆盖全部恢复路径。 | [/functional_chains/12/pattern/interpretation](codepatchbay-automatic-report.json#/functional_chains/12/pattern/interpretation) |
| relation_witnesses/0/all_lineage_creation_proven | false | [/functional_chains/12/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/12/pattern/relation_witnesses) |
| relation_witnesses/0/event_durability_proven | false | [/functional_chains/12/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/12/pattern/relation_witnesses) |
| relation_witnesses/0/event_literal_fields/0/reason/kind | literal | [/functional_chains/12/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/12/pattern/relation_witnesses) |
| relation_witnesses/0/event_literal_fields/0/reason/value | external_remediation_fixed | [/functional_chains/12/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/12/pattern/relation_witnesses) |
| relation_witnesses/0/event_literal_fields/0/type/kind | literal | [/functional_chains/12/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/12/pattern/relation_witnesses) |
| relation_witnesses/0/event_literal_fields/0/type/value | job_superseded | [/functional_chains/12/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/12/pattern/relation_witnesses) |
| relation_witnesses/0/shared_source_field_origins/0/captured_origin_declaration_id | 5240bea3213ba205e41fb21cdc9ef4b42e535849569cc13888b9ea9c5e286c8c | [/functional_chains/12/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/12/pattern/relation_witnesses) |
| relation_witnesses/0/shared_source_field_origins/0/event_field | jobId | [/functional_chains/12/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/12/pattern/relation_witnesses) |
| relation_witnesses/0/shared_source_field_origins/0/heap_or_runtime_identity_proven | false | [/functional_chains/12/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/12/pattern/relation_witnesses) |
| relation_witnesses/0/shared_source_field_origins/0/queue_field_path | /metadata/originJobId | [/functional_chains/12/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/12/pattern/relation_witnesses) |
| relation_witnesses/0/shared_source_field_origins/0/source_origin/kind | input | [/functional_chains/12/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/12/pattern/relation_witnesses) |
| relation_witnesses/0/shared_source_field_origins/0/source_origin/name | jobId | [/functional_chains/12/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/12/pattern/relation_witnesses) |
| relation_witnesses/0/shared_source_field_origins/1/captured_origin_declaration_id | 5240bea3213ba205e41fb21cdc9ef4b42e535849569cc13888b9ea9c5e286c8c | [/functional_chains/12/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/12/pattern/relation_witnesses) |
| relation_witnesses/0/shared_source_field_origins/1/event_field | jobId | [/functional_chains/12/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/12/pattern/relation_witnesses) |
| relation_witnesses/0/shared_source_field_origins/1/heap_or_runtime_identity_proven | false | [/functional_chains/12/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/12/pattern/relation_witnesses) |
| relation_witnesses/0/shared_source_field_origins/1/queue_field_path | /metadata/sourceContext/remediation/previousJobId | [/functional_chains/12/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/12/pattern/relation_witnesses) |
| relation_witnesses/0/shared_source_field_origins/1/source_origin/kind | input | [/functional_chains/12/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/12/pattern/relation_witnesses) |
| relation_witnesses/0/shared_source_field_origins/1/source_origin/name | jobId | [/functional_chains/12/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/12/pattern/relation_witnesses) |
| relation_witnesses/0/shared_source_field_origins/2/captured_origin_declaration_id | 5240bea3213ba205e41fb21cdc9ef4b42e535849569cc13888b9ea9c5e286c8c | [/functional_chains/12/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/12/pattern/relation_witnesses) |
| relation_witnesses/0/shared_source_field_origins/2/event_field | jobId | [/functional_chains/12/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/12/pattern/relation_witnesses) |

完整关系 [/functional_chains/12/pattern](codepatchbay-automatic-report.json#/functional_chains/12/pattern)；原 source facts [/functional_chains/12/source_facts](codepatchbay-automatic-report.json#/functional_chains/12/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### `cpb-trusted-command-lineage`

保存状态 `scoped_source_relations_supported`；保存缺口 `[{"code":"record_command_source_dependencies_do_not_prove_full_heap_noninterference","source_only":true}]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| relation_witnesses/loaded_policy_lookup_result_is_actual_command_runner_input | true | [/functional_chains/14/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/14/pattern/relation_witnesses) |
| relation_witnesses/all_selected_direct_role_call_transfers | true | [/functional_chains/14/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/14/pattern/relation_witnesses) |
| relation_witnesses/execfile_stdout_json_decode_is_actual_policy_parser_input | true | [/functional_chains/14/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/14/pattern/relation_witnesses) |
| relation_witnesses/executor_reads_executable_and_args_from_same_command_formal | true | [/functional_chains/14/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/14/pattern/relation_witnesses) |
| relation_witnesses/parsed_policy_spec_has_explicit_command_fields | true | [/functional_chains/14/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/14/pattern/relation_witnesses) |
| relation_witnesses/policy_parser_references_spec_parser_callback | true | [/functional_chains/14/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/14/pattern/relation_witnesses) |
| relation_witnesses/selected_call_arguments_have_local_initializer_dependencies | true | [/functional_chains/14/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/14/pattern/relation_witnesses) |
| scoped_source_supported | true | [/functional_chains/14/pattern/scoped_source_supported](codepatchbay-automatic-report.json#/functional_chains/14/pattern/scoped_source_supported) |
| command_boundary/command_argument_origin_is_source_record_dependency | true | [/functional_chains/14/pattern/command_boundary](codepatchbay-automatic-report.json#/functional_chains/14/pattern/command_boundary) |
| command_boundary/command_executed | false | [/functional_chains/14/pattern/command_boundary](codepatchbay-automatic-report.json#/functional_chains/14/pattern/command_boundary) |
| command_boundary/expected_evidence_as_executable_source_proven | false | [/functional_chains/14/pattern/command_boundary](codepatchbay-automatic-report.json#/functional_chains/14/pattern/command_boundary) |
| command_boundary/expected_evidence_never_influences_any_branch_proven | false | [/functional_chains/14/pattern/command_boundary](codepatchbay-automatic-report.json#/functional_chains/14/pattern/command_boundary) |
| command_boundary/opaque_effects_or_mutated_heap_excluded | false | [/functional_chains/14/pattern/command_boundary](codepatchbay-automatic-report.json#/functional_chains/14/pattern/command_boundary) |
| command_boundary/trusted_head_authenticity_runtime_verified | false | [/functional_chains/14/pattern/command_boundary](codepatchbay-automatic-report.json#/functional_chains/14/pattern/command_boundary) |
| guards/command_runner/0/condition/kind | binary_expression | [/functional_chains/14/pattern/guards](codepatchbay-automatic-report.json#/functional_chains/14/pattern/guards) |
| guards/command_runner/0/condition/location/file | core/workflow/probe-runner.ts | [/functional_chains/14/pattern/guards](codepatchbay-automatic-report.json#/functional_chains/14/pattern/guards) |
| guards/command_runner/0/condition/location/line | 481 | [/functional_chains/14/pattern/guards](codepatchbay-automatic-report.json#/functional_chains/14/pattern/guards) |
| guards/command_runner/0/condition/location/column | 9 | [/functional_chains/14/pattern/guards](codepatchbay-automatic-report.json#/functional_chains/14/pattern/guards) |
| guards/command_runner/0/condition/location/end_line | 481 | [/functional_chains/14/pattern/guards](codepatchbay-automatic-report.json#/functional_chains/14/pattern/guards) |
| guards/command_runner/0/condition/location/start_byte | 17010 | [/functional_chains/14/pattern/guards](codepatchbay-automatic-report.json#/functional_chains/14/pattern/guards) |
| guards/command_runner/0/condition/location/end_byte | 17087 | [/functional_chains/14/pattern/guards](codepatchbay-automatic-report.json#/functional_chains/14/pattern/guards) |
| guards/command_runner/0/condition/reference_dependencies_only | true | [/functional_chains/14/pattern/guards](codepatchbay-automatic-report.json#/functional_chains/14/pattern/guards) |
| guards/command_runner/0/condition/reference_path | null | [/functional_chains/14/pattern/guards](codepatchbay-automatic-report.json#/functional_chains/14/pattern/guards) |
| guards/command_runner/0/condition/references/0/state | unique | [/functional_chains/14/pattern/guards](codepatchbay-automatic-report.json#/functional_chains/14/pattern/guards) |

完整关系 [/functional_chains/14/pattern](codepatchbay-automatic-report.json#/functional_chains/14/pattern)；原 source facts [/functional_chains/14/source_facts](codepatchbay-automatic-report.json#/functional_chains/14/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### `cpb-unsupported-record-retention`

保存状态 `scoped_source_relations_supported`；保存缺口 `[{"code":"record_true_marker_does_not_prove_all_input_or_artifact_retention","source_only":true}]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| relation_witnesses/verification_passes_actual_ledger_result_json_to_artifact_writer | true | [/functional_chains/15/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/15/pattern/relation_witnesses) |
| relation_witnesses/failure_records_append_to_returned_runner_collection | true | [/functional_chains/15/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/15/pattern/relation_witnesses) |
| relation_witnesses/ledger_claims_append_to_returned_evidence_collection | true | [/functional_chains/15/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/15/pattern/relation_witnesses) |
| relation_witnesses/plan_initializes_and_propagates_true_marker | true | [/functional_chains/15/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/15/pattern/relation_witnesses) |
| relation_witnesses/runner_emits_explicit_true_failure_record | true | [/functional_chains/15/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/15/pattern/relation_witnesses) |
| relation_witnesses/true_marker_excludes_selected_invalid_record_skip | true | [/functional_chains/15/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/15/pattern/relation_witnesses) |
| relation_witnesses/verification_calls_runner_plan_ledger | true | [/functional_chains/15/pattern/relation_witnesses](codepatchbay-automatic-report.json#/functional_chains/15/pattern/relation_witnesses) |
| scoped_source_supported | true | [/functional_chains/15/pattern/scoped_source_supported](codepatchbay-automatic-report.json#/functional_chains/15/pattern/scoped_source_supported) |
| explicit_key_precedence_counter_sources/0/conditions/0 | ordinary Set membership and the captured iteration body are reached | [/functional_chains/15/pattern/explicit_key_precedence_counter_sources](codepatchbay-automatic-report.json#/functional_chains/15/pattern/explicit_key_precedence_counter_sources) |
| explicit_key_precedence_counter_sources/0/later_matching_input_skipped_on_this_guard | true | [/functional_chains/15/pattern/explicit_key_precedence_counter_sources](codepatchbay-automatic-report.json#/functional_chains/15/pattern/explicit_key_precedence_counter_sources) |
| explicit_key_precedence_counter_sources/0/record_relations_version | captured-record-projection-relations-1 | [/functional_chains/15/pattern/explicit_key_precedence_counter_sources](codepatchbay-automatic-report.json#/functional_chains/15/pattern/explicit_key_precedence_counter_sources) |
| explicit_key_precedence_counter_sources/0/all_input_record_preservation_proven | false | [/functional_chains/15/pattern/explicit_key_precedence_counter_sources](codepatchbay-automatic-report.json#/functional_chains/15/pattern/explicit_key_precedence_counter_sources) |
| explicit_key_precedence_counter_sources/0/following_add_call_fact_ids/0 | 6dacaa1e2808492cc63088e1 | [/functional_chains/15/pattern/explicit_key_precedence_counter_sources](codepatchbay-automatic-report.json#/functional_chains/15/pattern/explicit_key_precedence_counter_sources) |
| explicit_key_precedence_counter_sources/0/kind | record_seen_explicit_key_skips_later_input_source | [/functional_chains/15/pattern/explicit_key_precedence_counter_sources](codepatchbay-automatic-report.json#/functional_chains/15/pattern/explicit_key_precedence_counter_sources) |
| explicit_key_precedence_counter_sources/0/location/file | core/workflow/evidence-probes.ts | [/functional_chains/15/pattern/explicit_key_precedence_counter_sources](codepatchbay-automatic-report.json#/functional_chains/15/pattern/explicit_key_precedence_counter_sources) |
| explicit_key_precedence_counter_sources/0/location/line | 339 | [/functional_chains/15/pattern/explicit_key_precedence_counter_sources](codepatchbay-automatic-report.json#/functional_chains/15/pattern/explicit_key_precedence_counter_sources) |
| explicit_key_precedence_counter_sources/0/location/column | 5 | [/functional_chains/15/pattern/explicit_key_precedence_counter_sources](codepatchbay-automatic-report.json#/functional_chains/15/pattern/explicit_key_precedence_counter_sources) |
| explicit_key_precedence_counter_sources/0/location/end_line | 339 | [/functional_chains/15/pattern/explicit_key_precedence_counter_sources](codepatchbay-automatic-report.json#/functional_chains/15/pattern/explicit_key_precedence_counter_sources) |
| explicit_key_precedence_counter_sources/0/location/start_byte | 14319 | [/functional_chains/15/pattern/explicit_key_precedence_counter_sources](codepatchbay-automatic-report.json#/functional_chains/15/pattern/explicit_key_precedence_counter_sources) |
| explicit_key_precedence_counter_sources/0/location/end_byte | 14375 | [/functional_chains/15/pattern/explicit_key_precedence_counter_sources](codepatchbay-automatic-report.json#/functional_chains/15/pattern/explicit_key_precedence_counter_sources) |
| explicit_key_precedence_counter_sources/0/membership_source/kind | call_expression | [/functional_chains/15/pattern/explicit_key_precedence_counter_sources](codepatchbay-automatic-report.json#/functional_chains/15/pattern/explicit_key_precedence_counter_sources) |
| explicit_key_precedence_counter_sources/0/membership_source/location/file | core/workflow/evidence-probes.ts | [/functional_chains/15/pattern/explicit_key_precedence_counter_sources](codepatchbay-automatic-report.json#/functional_chains/15/pattern/explicit_key_precedence_counter_sources) |
| explicit_key_precedence_counter_sources/0/membership_source/location/line | 339 | [/functional_chains/15/pattern/explicit_key_precedence_counter_sources](codepatchbay-automatic-report.json#/functional_chains/15/pattern/explicit_key_precedence_counter_sources) |
| explicit_key_precedence_counter_sources/0/membership_source/location/column | 9 | [/functional_chains/15/pattern/explicit_key_precedence_counter_sources](codepatchbay-automatic-report.json#/functional_chains/15/pattern/explicit_key_precedence_counter_sources) |

完整关系 [/functional_chains/15/pattern](codepatchbay-automatic-report.json#/functional_chains/15/pattern)；原 source facts [/functional_chains/15/source_facts](codepatchbay-automatic-report.json#/functional_chains/15/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### `wwc-browser-continuation-lifecycle`

保存状态 `scoped_source_relations_supported`；保存缺口 `[]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/0/pattern/scoped_source_supported](winwincode-automatic-report.json#/functional_chains/0/pattern/scoped_source_supported) |
| all_async_callbacks_guarded_proven | false | [/functional_chains/0/pattern/all_async_callbacks_guarded_proven](winwincode-automatic-report.json#/functional_chains/0/pattern/all_async_callbacks_guarded_proven) |
| all_stale_results_rejected_proven | false | [/functional_chains/0/pattern/all_stale_results_rejected_proven](winwincode-automatic-report.json#/functional_chains/0/pattern/all_stale_results_rejected_proven) |
| closed_result_disposal_consumers/0/condition_token/root_declaration_id | 0d7629777cc8b0e6de78212203160b2123bba2cddb98c7a70186375e29b1e657 | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/condition_token/root_declaration_location/file | apps/client/src/settings-page.ts | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/condition_token/root_declaration_location/line | 483 | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/condition_token/root_declaration_location/column | 7 | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/condition_token/root_declaration_location/end_line | 483 | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/condition_token/root_declaration_location/start_byte | 17405 | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/condition_token/root_declaration_location/end_byte | 17419 | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/condition_token/root_identity/state | unique | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/condition_token/root_identity/limitations/0 | identity denotes a captured lexical declaration, not an object/resource or alias identity | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/condition_token/root_identity/limitations/1 | no reaching values, target activation, hidden calls or external heap mutation are proved | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/condition_token/root_identity/limitations/2 | write records include captured syntax and possible effects, not executed writes | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/condition_token/root_identity/binder_location/file | apps/client/src/settings-page.ts | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/condition_token/root_identity/binder_location/line | 483 | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/condition_token/root_identity/binder_location/column | 7 | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/condition_token/root_identity/binder_location/end_line | 483 | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/condition_token/root_identity/binder_location/start_byte | 17405 | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/condition_token/root_identity/binder_location/end_byte | 17411 | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/condition_token/root_identity/binder_span/end_byte | 17411 | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/condition_token/root_identity/binder_span/node_type | identifier | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/condition_token/root_identity/binder_span/start_byte | 17405 | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/condition_token/root_identity/binding_id | 0d7629777cc8b0e6de78212203160b2123bba2cddb98c7a70186375e29b1e657 | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |

完整关系 [/functional_chains/0/pattern](winwincode-automatic-report.json#/functional_chains/0/pattern)；原 source facts [/functional_chains/0/source_facts](winwincode-automatic-report.json#/functional_chains/0/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### `wwc-captured-record-resource-writers`

保存状态 `scoped_source_relations_supported`；保存缺口 `[]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/1/pattern/scoped_source_supported](winwincode-automatic-report.json#/functional_chains/1/pattern/scoped_source_supported) |
| relation_component_version | captured-lifecycle-ownership-relations-1 | [/functional_chains/1/pattern/relation_component_version](winwincode-automatic-report.json#/functional_chains/1/pattern/relation_component_version) |
| responsibility_interpretation | Selected captured functions write the recorded lexical fields and pass the recorded arguments; directory names assign no responsibility. | [/functional_chains/1/pattern/responsibility_interpretation](winwincode-automatic-report.json#/functional_chains/1/pattern/responsibility_interpretation) |
| source_rejection_guard_fact_ids/0 | 6ee85ca49c479b9a2e9e6b2d | [/functional_chains/1/pattern/source_rejection_guard_fact_ids](winwincode-automatic-report.json#/functional_chains/1/pattern/source_rejection_guard_fact_ids) |
| all_mutations_authorized_proven | false | [/functional_chains/1/pattern/all_mutations_authorized_proven](winwincode-automatic-report.json#/functional_chains/1/pattern/all_mutations_authorized_proven) |
| all_storage_resources_bound_proven | false | [/functional_chains/1/pattern/all_storage_resources_bound_proven](winwincode-automatic-report.json#/functional_chains/1/pattern/all_storage_resources_bound_proven) |
| call_record_and_effect_frontiers/shown_items/0/activation_and_physical_effect_proven | false | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/kind | identifier | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/location/file | apps/client/src/application.ts | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/location/line | 195 | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/location/column | 45 | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/location/end_line | 195 | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/location/start_byte | 6970 | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/location/end_byte | 6977 | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/name | browser | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/1/kind | identifier | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/1/location/file | apps/client/src/application.ts | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/1/location/line | 195 | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/1/location/column | 54 | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/1/location/end_line | 195 | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/1/location/start_byte | 6979 | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/1/location/end_byte | 6987 | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/1/name | document | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/authenticated_call_edge_id | e3f0645515e3b509073e48cf | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |

完整关系 [/functional_chains/1/pattern](winwincode-automatic-report.json#/functional_chains/1/pattern)；原 source facts [/functional_chains/1/source_facts](winwincode-automatic-report.json#/functional_chains/1/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### `wwc-document-device-provider-deployment-scope`

保存状态 `scoped_source_relations_supported`；保存缺口 `[]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| comparison/statement | 所选文档描述 Control Plane 内部唯一模型路由及 Worker 仅经模型流；所选 Device 源码另有本地 provider 选择、字节 material 容器与调用来源，表述需要说明部署范围。 | [/functional_chains/3/pattern/comparison](winwincode-automatic-report.json#/functional_chains/3/pattern/comparison) |
| comparison/actual_deployment_or_network_execution_verified | false | [/functional_chains/3/pattern/comparison](winwincode-automatic-report.json#/functional_chains/3/pattern/comparison) |
| comparison/classification | selected_document_wording_requires_device_deployment_qualification | [/functional_chains/3/pattern/comparison](winwincode-automatic-report.json#/functional_chains/3/pattern/comparison) |
| comparison/document_control_plane_internal_scope_preserved | true | [/functional_chains/3/pattern/comparison](winwincode-automatic-report.json#/functional_chains/3/pattern/comparison) |
| comparison/global_project_exclusivity_inferred_from_document | false | [/functional_chains/3/pattern/comparison](winwincode-automatic-report.json#/functional_chains/3/pattern/comparison) |
| comparison/long_term_credential_exclusivity_refuted | unknown | [/functional_chains/3/pattern/comparison](winwincode-automatic-report.json#/functional_chains/3/pattern/comparison) |
| comparison/public_delivery_or_contract_secret_leak_proven | false | [/functional_chains/3/pattern/comparison](winwincode-automatic-report.json#/functional_chains/3/pattern/comparison) |
| comparison/raw_secret_reference_equated_with_material | false | [/functional_chains/3/pattern/comparison](winwincode-automatic-report.json#/functional_chains/3/pattern/comparison) |
| comparison/secret_material_lifetime | unknown | [/functional_chains/3/pattern/comparison](winwincode-automatic-report.json#/functional_chains/3/pattern/comparison) |
| comparison/security_defect_declared | false | [/functional_chains/3/pattern/comparison](winwincode-automatic-report.json#/functional_chains/3/pattern/comparison) |
| comparison/worker_execution_port_protocol_bypass_proven | false | [/functional_chains/3/pattern/comparison](winwincode-automatic-report.json#/functional_chains/3/pattern/comparison) |
| relation_witnesses/server_boundary_retains_unsupported_result_source | true | [/functional_chains/3/pattern/relation_witnesses](winwincode-automatic-report.json#/functional_chains/3/pattern/relation_witnesses) |
| relation_witnesses/worker_local_consumer_guard_precedes_transport_fallback_source | true | [/functional_chains/3/pattern/relation_witnesses](winwincode-automatic-report.json#/functional_chains/3/pattern/relation_witnesses) |
| relation_witnesses/device_message_body_connects_local_store_to_model_callback_source | true | [/functional_chains/3/pattern/relation_witnesses](winwincode-automatic-report.json#/functional_chains/3/pattern/relation_witnesses) |
| relation_witnesses/local_execute_contains_selected_invoke_source | true | [/functional_chains/3/pattern/relation_witnesses](winwincode-automatic-report.json#/functional_chains/3/pattern/relation_witnesses) |
| relation_witnesses/local_factory_reads_endpoint_and_constructs_provider_candidate | true | [/functional_chains/3/pattern/relation_witnesses](winwincode-automatic-report.json#/functional_chains/3/pattern/relation_witnesses) |
| relation_witnesses/local_resolver_passes_captured_byte_material_to_secret_constructor | true | [/functional_chains/3/pattern/relation_witnesses](winwincode-automatic-report.json#/functional_chains/3/pattern/relation_witnesses) |
| relation_witnesses/production_bootstrap_contains_selected_provider_installation_candidate | true | [/functional_chains/3/pattern/relation_witnesses](winwincode-automatic-report.json#/functional_chains/3/pattern/relation_witnesses) |
| relation_witnesses/resolved_config_and_secret_reach_same_local_provider_source | true | [/functional_chains/3/pattern/relation_witnesses](winwincode-automatic-report.json#/functional_chains/3/pattern/relation_witnesses) |
| relation_witnesses/secret_container_constructs_owned_byte_material_source | true | [/functional_chains/3/pattern/relation_witnesses](winwincode-automatic-report.json#/functional_chains/3/pattern/relation_witnesses) |
| relation_witnesses/selected_provider_method_exposes_secret_operand_source | true | [/functional_chains/3/pattern/relation_witnesses](winwincode-automatic-report.json#/functional_chains/3/pattern/relation_witnesses) |
| relation_witnesses/worker_installs_captured_local_model_field | true | [/functional_chains/3/pattern/relation_witnesses](winwincode-automatic-report.json#/functional_chains/3/pattern/relation_witnesses) |
| conditions/0 | captured selected production methods and deferred callbacks are activated and reached normally in the selected Device composition | [/functional_chains/3/pattern/conditions](winwincode-automatic-report.json#/functional_chains/3/pattern/conditions) |
| conditions/1 | ordinary Rust lexical shadowing, Option/Result callback source contracts and plain captured records apply | [/functional_chains/3/pattern/conditions](winwincode-automatic-report.json#/functional_chains/3/pattern/conditions) |

完整关系 [/functional_chains/3/pattern](winwincode-automatic-report.json#/functional_chains/3/pattern)；原 source facts [/functional_chains/3/source_facts](winwincode-automatic-report.json#/functional_chains/3/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### `wwc-report-chat-retained-request-identities`

保存状态 `scoped_source_relations_supported`；保存缺口 `[]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/6/pattern/scoped_source_supported](winwincode-automatic-report.json#/functional_chains/6/pattern/scoped_source_supported) |
| relation_fact_ids/shown_items/0 | 0e025b9a5dfa98cd414b940d | [/functional_chains/6/pattern/relation_fact_ids](winwincode-automatic-report.json#/functional_chains/6/pattern/relation_fact_ids) |
| relation_fact_ids/shown_items/1 | 4f8322f697b728ed8643fa4c | [/functional_chains/6/pattern/relation_fact_ids](winwincode-automatic-report.json#/functional_chains/6/pattern/relation_fact_ids) |
| relation_fact_ids/shown_items/2 | 019343d27b68264b4131894c | [/functional_chains/6/pattern/relation_fact_ids](winwincode-automatic-report.json#/functional_chains/6/pattern/relation_fact_ids) |
| relation_fact_ids/shown_items/3 | 8380dc1c5e28aef173759cfc | [/functional_chains/6/pattern/relation_fact_ids](winwincode-automatic-report.json#/functional_chains/6/pattern/relation_fact_ids) |
| relation_fact_ids/shown_items/4 | 06692a0244fbfb36780f1061 | [/functional_chains/6/pattern/relation_fact_ids](winwincode-automatic-report.json#/functional_chains/6/pattern/relation_fact_ids) |
| relation_fact_ids/shown_items/5 | 72ddfc095f0aabde8ecf4736 | [/functional_chains/6/pattern/relation_fact_ids](winwincode-automatic-report.json#/functional_chains/6/pattern/relation_fact_ids) |
| relation_fact_ids/shown_count | 6 | [/functional_chains/6/pattern/relation_fact_ids](winwincode-automatic-report.json#/functional_chains/6/pattern/relation_fact_ids) |
| relation_fact_ids/total_count | 39 | [/functional_chains/6/pattern/relation_fact_ids](winwincode-automatic-report.json#/functional_chains/6/pattern/relation_fact_ids) |
| relation_fact_ids/truncated | true | [/functional_chains/6/pattern/relation_fact_ids](winwincode-automatic-report.json#/functional_chains/6/pattern/relation_fact_ids) |
| budget/incomplete | false | [/functional_chains/6/pattern/budget](winwincode-automatic-report.json#/functional_chains/6/pattern/budget) |
| budget/limit | 65536 | [/functional_chains/6/pattern/budget](winwincode-automatic-report.json#/functional_chains/6/pattern/budget) |
| budget/operations | 901 | [/functional_chains/6/pattern/budget](winwincode-automatic-report.json#/functional_chains/6/pattern/budget) |
| components/chat_request_identity/supported | true | [/functional_chains/6/pattern/components](winwincode-automatic-report.json#/functional_chains/6/pattern/components) |
| components/chat_request_identity/builder_call_relations/0/supported | true | [/functional_chains/6/pattern/components](winwincode-automatic-report.json#/functional_chains/6/pattern/components) |
| components/chat_request_identity/builder_call_relations/0/kind | existing_authenticated_call | [/functional_chains/6/pattern/components](winwincode-automatic-report.json#/functional_chains/6/pattern/components) |
| components/chat_request_identity/builder_call_relations/0/target_role | chat_items_builder | [/functional_chains/6/pattern/components](winwincode-automatic-report.json#/functional_chains/6/pattern/components) |
| components/chat_request_identity/all_chat_commands_covered | false | [/functional_chains/6/pattern/components](winwincode-automatic-report.json#/functional_chains/6/pattern/components) |
| components/chat_request_identity/builder_field_projections/shown_items/0/creates_calls_edge | false | [/functional_chains/6/pattern/components/chat_request_identity/builder_field_projections](winwincode-automatic-report.json#/functional_chains/6/pattern/components/chat_request_identity/builder_field_projections) |
| components/chat_request_identity/builder_field_projections/shown_items/0/extractor_version | captured-message-identity-relations-1 | [/functional_chains/6/pattern/components/chat_request_identity/builder_field_projections](winwincode-automatic-report.json#/functional_chains/6/pattern/components/chat_request_identity/builder_field_projections) |
| components/chat_request_identity/builder_field_projections/shown_items/0/field | actor | [/functional_chains/6/pattern/components/chat_request_identity/builder_field_projections](winwincode-automatic-report.json#/functional_chains/6/pattern/components/chat_request_identity/builder_field_projections) |
| components/chat_request_identity/builder_field_projections/shown_items/0/kind | message_builder_field_projection | [/functional_chains/6/pattern/components/chat_request_identity/builder_field_projections](winwincode-automatic-report.json#/functional_chains/6/pattern/components/chat_request_identity/builder_field_projections) |
| components/chat_request_identity/builder_field_projections/shown_items/0/location/file | apps/client/src/community-control-plane-client.ts | [/functional_chains/6/pattern/components/chat_request_identity/builder_field_projections](winwincode-automatic-report.json#/functional_chains/6/pattern/components/chat_request_identity/builder_field_projections) |
| components/chat_request_identity/builder_field_projections/shown_items/0/location/line | 424 | [/functional_chains/6/pattern/components/chat_request_identity/builder_field_projections](winwincode-automatic-report.json#/functional_chains/6/pattern/components/chat_request_identity/builder_field_projections) |

完整关系 [/functional_chains/6/pattern](winwincode-automatic-report.json#/functional_chains/6/pattern)；原 source facts [/functional_chains/6/source_facts](winwincode-automatic-report.json#/functional_chains/6/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### `wwc-report-outbox-ack-correlation-fields`

保存状态 `scoped_source_relations_supported`；保存缺口 `[]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/11/pattern/scoped_source_supported](winwincode-automatic-report.json#/functional_chains/11/pattern/scoped_source_supported) |
| relation_fact_ids/shown_items/0 | c115be0dd2f6450150079751 | [/functional_chains/11/pattern/relation_fact_ids](winwincode-automatic-report.json#/functional_chains/11/pattern/relation_fact_ids) |
| relation_fact_ids/shown_items/1 | 888b099cdb80e643657b0a04 | [/functional_chains/11/pattern/relation_fact_ids](winwincode-automatic-report.json#/functional_chains/11/pattern/relation_fact_ids) |
| relation_fact_ids/shown_items/2 | 6804597ee017d8b903b722c0 | [/functional_chains/11/pattern/relation_fact_ids](winwincode-automatic-report.json#/functional_chains/11/pattern/relation_fact_ids) |
| relation_fact_ids/shown_items/3 | b58376d52b1d57f508362a84 | [/functional_chains/11/pattern/relation_fact_ids](winwincode-automatic-report.json#/functional_chains/11/pattern/relation_fact_ids) |
| relation_fact_ids/shown_items/4 | ceecfe449e4cabaeee74ee02 | [/functional_chains/11/pattern/relation_fact_ids](winwincode-automatic-report.json#/functional_chains/11/pattern/relation_fact_ids) |
| relation_fact_ids/shown_items/5 | 13a0b4f23dd230ea5d32d74d | [/functional_chains/11/pattern/relation_fact_ids](winwincode-automatic-report.json#/functional_chains/11/pattern/relation_fact_ids) |
| relation_fact_ids/shown_count | 6 | [/functional_chains/11/pattern/relation_fact_ids](winwincode-automatic-report.json#/functional_chains/11/pattern/relation_fact_ids) |
| relation_fact_ids/total_count | 29 | [/functional_chains/11/pattern/relation_fact_ids](winwincode-automatic-report.json#/functional_chains/11/pattern/relation_fact_ids) |
| relation_fact_ids/truncated | true | [/functional_chains/11/pattern/relation_fact_ids](winwincode-automatic-report.json#/functional_chains/11/pattern/relation_fact_ids) |
| budget/incomplete | false | [/functional_chains/11/pattern/budget](winwincode-automatic-report.json#/functional_chains/11/pattern/budget) |
| budget/limit | 65536 | [/functional_chains/11/pattern/budget](winwincode-automatic-report.json#/functional_chains/11/pattern/budget) |
| budget/operations | 2145 | [/functional_chains/11/pattern/budget](winwincode-automatic-report.json#/functional_chains/11/pattern/budget) |
| components/outbox_ack_correlation/supported | true | [/functional_chains/11/pattern/components](winwincode-automatic-report.json#/functional_chains/11/pattern/components) |
| components/outbox_ack_correlation/correlation_codec_sources/0/arguments/0/kind | identifier | [/functional_chains/11/pattern/components](winwincode-automatic-report.json#/functional_chains/11/pattern/components) |
| components/outbox_ack_correlation/correlation_codec_sources/0/arguments/0/location/file | crates/winwincode-codex/src/outbox.rs | [/functional_chains/11/pattern/components](winwincode-automatic-report.json#/functional_chains/11/pattern/components) |
| components/outbox_ack_correlation/correlation_codec_sources/0/arguments/0/location/line | 738 | [/functional_chains/11/pattern/components](winwincode-automatic-report.json#/functional_chains/11/pattern/components) |
| components/outbox_ack_correlation/correlation_codec_sources/0/arguments/0/location/column | 36 | [/functional_chains/11/pattern/components](winwincode-automatic-report.json#/functional_chains/11/pattern/components) |
| components/outbox_ack_correlation/correlation_codec_sources/0/arguments/0/location/end_line | 738 | [/functional_chains/11/pattern/components](winwincode-automatic-report.json#/functional_chains/11/pattern/components) |
| components/outbox_ack_correlation/correlation_codec_sources/0/arguments/0/location/start_byte | 30300 | [/functional_chains/11/pattern/components](winwincode-automatic-report.json#/functional_chains/11/pattern/components) |
| components/outbox_ack_correlation/correlation_codec_sources/0/arguments/0/location/end_byte | 30305 | [/functional_chains/11/pattern/components](winwincode-automatic-report.json#/functional_chains/11/pattern/components) |
| components/outbox_ack_correlation/correlation_codec_sources/0/arguments/0/name | value | [/functional_chains/11/pattern/components](winwincode-automatic-report.json#/functional_chains/11/pattern/components) |
| components/outbox_ack_correlation/correlation_codec_sources/0/callee_source | serde_json::to_vec | [/functional_chains/11/pattern/components](winwincode-automatic-report.json#/functional_chains/11/pattern/components) |
| components/outbox_ack_correlation/correlation_codec_sources/0/codec_runtime_or_digest_collision_proven | false | [/functional_chains/11/pattern/components](winwincode-automatic-report.json#/functional_chains/11/pattern/components) |

完整关系 [/functional_chains/11/pattern](winwincode-automatic-report.json#/functional_chains/11/pattern)；原 source facts [/functional_chains/11/source_facts](winwincode-automatic-report.json#/functional_chains/11/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### `wwc-report-worker-adapter-record-identities`

保存状态 `scoped_source_relations_supported`；保存缺口 `[]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/14/pattern/scoped_source_supported](winwincode-automatic-report.json#/functional_chains/14/pattern/scoped_source_supported) |
| relation_fact_ids/shown_items/0 | 9b2ee07136826ba3aa4a47b3 | [/functional_chains/14/pattern/relation_fact_ids](winwincode-automatic-report.json#/functional_chains/14/pattern/relation_fact_ids) |
| relation_fact_ids/shown_items/1 | 567d98cde9f06e78baf528a1 | [/functional_chains/14/pattern/relation_fact_ids](winwincode-automatic-report.json#/functional_chains/14/pattern/relation_fact_ids) |
| relation_fact_ids/shown_items/2 | 2dd47e138b7ea4f68739c9ac | [/functional_chains/14/pattern/relation_fact_ids](winwincode-automatic-report.json#/functional_chains/14/pattern/relation_fact_ids) |
| relation_fact_ids/shown_items/3 | 3f8709c9352be7417dd19429 | [/functional_chains/14/pattern/relation_fact_ids](winwincode-automatic-report.json#/functional_chains/14/pattern/relation_fact_ids) |
| relation_fact_ids/shown_items/4 | 49eccd259000f6fb18a8c56a | [/functional_chains/14/pattern/relation_fact_ids](winwincode-automatic-report.json#/functional_chains/14/pattern/relation_fact_ids) |
| relation_fact_ids/shown_items/5 | 3e69d04416d9e737728cc99a | [/functional_chains/14/pattern/relation_fact_ids](winwincode-automatic-report.json#/functional_chains/14/pattern/relation_fact_ids) |
| relation_fact_ids/shown_count | 6 | [/functional_chains/14/pattern/relation_fact_ids](winwincode-automatic-report.json#/functional_chains/14/pattern/relation_fact_ids) |
| relation_fact_ids/total_count | 86 | [/functional_chains/14/pattern/relation_fact_ids](winwincode-automatic-report.json#/functional_chains/14/pattern/relation_fact_ids) |
| relation_fact_ids/truncated | true | [/functional_chains/14/pattern/relation_fact_ids](winwincode-automatic-report.json#/functional_chains/14/pattern/relation_fact_ids) |
| budget/incomplete | false | [/functional_chains/14/pattern/budget](winwincode-automatic-report.json#/functional_chains/14/pattern/budget) |
| budget/limit | 65536 | [/functional_chains/14/pattern/budget](winwincode-automatic-report.json#/functional_chains/14/pattern/budget) |
| budget/operations | 3619 | [/functional_chains/14/pattern/budget](winwincode-automatic-report.json#/functional_chains/14/pattern/budget) |
| components/worker_adapter_identity/supported | true | [/functional_chains/14/pattern/components](winwincode-automatic-report.json#/functional_chains/14/pattern/components) |
| components/worker_adapter_identity/authority_and_result_values_proven | false | [/functional_chains/14/pattern/components](winwincode-automatic-report.json#/functional_chains/14/pattern/components) |
| components/worker_adapter_identity/all_profile_settings_fully_traced | false | [/functional_chains/14/pattern/components](winwincode-automatic-report.json#/functional_chains/14/pattern/components) |
| components/worker_adapter_identity/all_worker_messages_covered | false | [/functional_chains/14/pattern/components](winwincode-automatic-report.json#/functional_chains/14/pattern/components) |
| components/worker_adapter_identity/components/adapter_ensure_thread/supported | true | [/functional_chains/14/pattern/components](winwincode-automatic-report.json#/functional_chains/14/pattern/components) |
| components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/shown_items/0/creates_calls_edge | false | [/functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections](winwincode-automatic-report.json#/functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections) |
| components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/shown_items/0/extractor_version | captured-message-identity-relations-1 | [/functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections](winwincode-automatic-report.json#/functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections) |
| components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/shown_items/0/field | lease | [/functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections](winwincode-automatic-report.json#/functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections) |
| components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/shown_items/0/kind | message_record_field_projection | [/functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections](winwincode-automatic-report.json#/functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections) |
| components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/shown_items/0/location/file | crates/winwincode-codex/src/adapter.rs | [/functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections](winwincode-automatic-report.json#/functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections) |
| components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/shown_items/0/location/line | 3378 | [/functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections](winwincode-automatic-report.json#/functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections) |

完整关系 [/functional_chains/14/pattern](winwincode-automatic-report.json#/functional_chains/14/pattern)；原 source facts [/functional_chains/14/source_facts](winwincode-automatic-report.json#/functional_chains/14/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### `wwc-report-workrun-finite-selection`

保存状态 `scoped_source_relations_supported`；保存缺口 `[]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

`rows`；完整 [/functional_chains/18/pattern/finite_effective_state_relation/rows](winwincode-automatic-report.json#/functional_chains/18/pattern/finite_effective_state_relation/rows)；保存总行数 `8`。

| effective_state | input_state | runnable | source_quantifiers | 完整行 |
| --- | --- | --- | --- | --- |
| WorkItemState::Done | WorkItemState::Done | false | {"source_quantifier_1":false} | [/functional_chains/18/pattern/finite_effective_state_relation/rows/0](winwincode-automatic-report.json#/functional_chains/18/pattern/finite_effective_state_relation/rows/0) |
| WorkItemState::Done | WorkItemState::Done | false | {"source_quantifier_1":true} | [/functional_chains/18/pattern/finite_effective_state_relation/rows/1](winwincode-automatic-report.json#/functional_chains/18/pattern/finite_effective_state_relation/rows/1) |
| WorkItemState::Ready | WorkItemState::Ready | true | {"source_quantifier_1":false} | [/functional_chains/18/pattern/finite_effective_state_relation/rows/2](winwincode-automatic-report.json#/functional_chains/18/pattern/finite_effective_state_relation/rows/2) |
| WorkItemState::WaitingDependency | WorkItemState::Ready | false | {"source_quantifier_1":true} | [/functional_chains/18/pattern/finite_effective_state_relation/rows/3](winwincode-automatic-report.json#/functional_chains/18/pattern/finite_effective_state_relation/rows/3) |
| WorkItemState::Ready | WorkItemState::WaitingDependency | true | {"source_quantifier_1":false} | [/functional_chains/18/pattern/finite_effective_state_relation/rows/4](winwincode-automatic-report.json#/functional_chains/18/pattern/finite_effective_state_relation/rows/4) |
| WorkItemState::WaitingDependency | WorkItemState::WaitingDependency | false | {"source_quantifier_1":true} | [/functional_chains/18/pattern/finite_effective_state_relation/rows/5](winwincode-automatic-report.json#/functional_chains/18/pattern/finite_effective_state_relation/rows/5) |
| &lt;other value of this state enum&gt; | &lt;other value of this state enum&gt; | false | {"source_quantifier_1":false} | [/functional_chains/18/pattern/finite_effective_state_relation/rows/6](winwincode-automatic-report.json#/functional_chains/18/pattern/finite_effective_state_relation/rows/6) |
| &lt;other value of this state enum&gt; | &lt;other value of this state enum&gt; | false | {"source_quantifier_1":true} | [/functional_chains/18/pattern/finite_effective_state_relation/rows/7](winwincode-automatic-report.json#/functional_chains/18/pattern/finite_effective_state_relation/rows/7) |

`non_runnable_table_rows`；完整 [/functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows](winwincode-automatic-report.json#/functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows)；保存总行数 `6`。

| effective_state | input_state | runnable | source_quantifiers | 完整行 |
| --- | --- | --- | --- | --- |
| WorkItemState::Done | WorkItemState::Done | false | {"source_quantifier_1":false} | [/functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows/0](winwincode-automatic-report.json#/functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows/0) |
| WorkItemState::Done | WorkItemState::Done | false | {"source_quantifier_1":true} | [/functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows/1](winwincode-automatic-report.json#/functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows/1) |
| WorkItemState::WaitingDependency | WorkItemState::Ready | false | {"source_quantifier_1":true} | [/functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows/2](winwincode-automatic-report.json#/functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows/2) |
| WorkItemState::WaitingDependency | WorkItemState::WaitingDependency | false | {"source_quantifier_1":true} | [/functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows/3](winwincode-automatic-report.json#/functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows/3) |
| &lt;other value of this state enum&gt; | &lt;other value of this state enum&gt; | false | {"source_quantifier_1":false} | [/functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows/4](winwincode-automatic-report.json#/functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows/4) |
| &lt;other value of this state enum&gt; | &lt;other value of this state enum&gt; | false | {"source_quantifier_1":true} | [/functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows/5](winwincode-automatic-report.json#/functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows/5) |

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/18/pattern/scoped_source_supported](winwincode-automatic-report.json#/functional_chains/18/pattern/scoped_source_supported) |
| dependency_blocker_relation/supported | true | [/functional_chains/18/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/18/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/empty_dependency_collection_result | false | [/functional_chains/18/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/18/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/actual_dependencies_or_reachability_evaluated | false | [/functional_chains/18/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/18/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/candidate_collection/kind | name | [/functional_chains/18/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/18/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/candidate_collection/name | items | [/functional_chains/18/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/18/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/candidate_collection/span/0 | 23876 | [/functional_chains/18/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/18/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/candidate_collection/span/1 | 23881 | [/functional_chains/18/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/18/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/dependency_collection/field | depends_on | [/functional_chains/18/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/18/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/dependency_collection/kind | field | [/functional_chains/18/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/18/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/dependency_collection/span/0 | 23825 | [/functional_chains/18/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/18/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/dependency_collection/span/1 | 23840 | [/functional_chains/18/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/18/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/dependency_collection/value/kind | name | [/functional_chains/18/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/18/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/dependency_collection/value/name | item | [/functional_chains/18/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/18/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/dependency_collection/value/span/0 | 23825 | [/functional_chains/18/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/18/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/dependency_collection/value/span/1 | 23829 | [/functional_chains/18/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/18/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/finite_state_component | captured-rust-finite-state-relations-1 | [/functional_chains/18/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/18/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/identity_comparison/candidate_key/0 | candidate | [/functional_chains/18/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/18/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/identity_comparison/candidate_key/1 | id | [/functional_chains/18/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/18/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/identity_comparison/dependency_value/0 | dependency | [/functional_chains/18/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/18/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/kind | rust_finite_dependency_blocker_relation | [/functional_chains/18/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/18/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/location/file | crates/winwincode-delivery/src/application/workrun.rs | [/functional_chains/18/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/18/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/location/line | 648 | [/functional_chains/18/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/18/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/location/column | 10 | [/functional_chains/18/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/18/pattern/dependency_blocker_relation) |

完整关系 [/functional_chains/18/pattern](winwincode-automatic-report.json#/functional_chains/18/pattern)；原 source facts [/functional_chains/18/source_facts](winwincode-automatic-report.json#/functional_chains/18/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

`scoped_source_relations_supported` 也不表示全部 `analysis_gaps` 为空；以下既含 partial，也含已支持条目保留的 source-only 边界。表中只复制 gap code、角色和文件位置，完整记录保存在自动报告与输入清单。

| 保留边界的链 | 保存状态 | 保存分析缺段导航 |
| --- | --- | --- |
| cpb-event-index-projection | scoped_source_relations_supported | [{"code":"record_projection_physical_commit_and_all_recovery_not_proven","source_only":true}] |
| cpb-report-trusted-probe-command-source | scoped_source_relations_supported | [{"code":"structured_command_intermediate_values_and_external_effects_not_fully_proven","source_only":true}] |
| cpb-report-unsupported-probe-evidence | scoped_source_relations_supported | [{"code":"structured_record_markers_do_not_prove_all_input_retention_or_persistence","source_only":true}] |
| cpb-trusted-command-lineage | scoped_source_relations_supported | [{"code":"record_command_source_dependencies_do_not_prove_full_heap_noninterference","source_only":true}] |
| cpb-unsupported-record-retention | scoped_source_relations_supported | [{"code":"record_true_marker_does_not_prove_all_input_or_artifact_retention","source_only":true}] |
| wwc-report-device-provider-deployment | scoped_source_relations_supported | [{"code":"deployment_candidate_chain_not_global_dispatch_or_credential_availability","source_only":true}] |
| wwc-report-workrun-state-guards | scoped_source_relations_supported | [{"code":"iterator_selection_and_macro_runtime_semantics_not_fully_proven","source_only":true}] |

[全文范围对照](REPORT_ALIGNMENT_RESULTS.json) 保留原目录的 32 个章节、130 个段落/表格行/列表项。该数量是证据导航清单，未给每段文字、建议或业务职责重新评级。`whole_report_reproduction_claimed=false`；更广职责、安全、部署和原未审范围仍不能由五项判断或所选链替代。

## 正式来源与捕获范围

| 仓库 | 正式快照 | 状态 | 选入 / 解析 | 图节点 / 边 | 冷 / 暖创建 |
| --- | --- | --- | --- | --- | --- |
| codepatchbay | `dd5d4e3cc349b57eb87d0f810a415560bfd5f6b1022a990a35190a44d0e50ebb` | partial | 333 / 330 | 11085 / 60571 | True / False |
| winwincode | `cc327a390837a897be93cdd4bdd4d9ad652c47f70f0b0dbfbbf89a52b463d372` | partial | 471 / 465 | 32407 / 171939 | True / False |

两库冷、暖扫描各自保持同一不可变 snapshot，暖扫描 `created=false`。缓存情况由 integration 中的 maintenance 记录保存；不能据此宣称每文件增量依赖分析。源码捕获/解析状态仍与功能判断分开。

## 模型、policy 与 input scope 的变化

下列 model ID 从保存判断的显式模型记录复制，既不是运行验证，也不是新增能力计数。模型的实际源码适用关系、条件和 policy 条目以原 evidence 为准；主要链自己的 `trusted_models` 与 `policy_declarations` 另存于自动报告。

| 配置判断 | 保存的显式模型 |
| --- | --- |
| CPB-01 | ["normal-async-callback-transfer-v1","normal-authenticated-json-broker-channel-v1","normal-durable-record-channel-v1","ordinary-record-tree-flow-v1","source-derived-module-assembly-v1","standard-json-record-codec-v1"] |
| CPB-02 | ["ordinary-record-status-predicate-normal-projection-v1"] |
| CPB-03 | ["atomic-file-normal-publish-v1","directory-owner-lock-normal-operation-v1","ecmascript-literal-module-import-v1","ecmascript-plain-json-record-array-v1","ecmascript-source-closed-instance-v1","finite-queue-interleaving-v1","node-logical-path-identity-v1","node-source-hash-key-v1"] |
| WWC-01 | ["dom-anchor-append-listener-1","js-hash-path-strip-1","literal-promise-all-destructuring-assembly-1","ordinary-source-method-invocation-1","ordinary-static-object-and-freeze-assembly-1"] |
| WWC-02 | ["captured-device-json-serde-dispatch-v1"] |

policy 和 inert 支持输入的实际变化如下，本轮不作同条件精度或缺陷率比较。

- **codepatchbay**：policy 字节相同=`false`；变化 section=`["report_claims"]`；捕获 source hash 与 v13 相同=`true`。inert 支持输入 2 项；原引用源文件 hash 与 target commit 由 publication identity 单独核对。
- **winwincode**：policy 字节相同=`false`；变化 section=`["report_claims"]`；捕获 source hash 与 v13 相同=`true`。inert 支持输入 11 项；原引用源文件 hash 与 target commit 由 publication identity 单独核对。

输入捕获范围改变不等于目标代码发生修改。受信模型和环境条件不填补尚未建立的源连接；旧 field/IR 的 unknown 不因新局部 record 关系被升级。无运行、浏览器、网络、并发或业务验收证明。

## 原 26 条观察与交付身份

原冻结观察保留 26 条，总计比较 26 条，状态为 `{"ambiguous":0,"endpoint_missing":0,"evidence_only":13,"evidence_unavailable":0,"mismatch":0,"reproduced":10,"source_changed":0,"source_missing":0,"unknown":3}`；相对 v13 的保存变化记录为 0 项。evidence_only 和指定 unknown 仍遵循原 evaluator；观察重现数量不是完整功能判断数量。

包版本 `0.14.0`，analyzer `static-multilang-14`，detector `call-rules-13-architecture-explanations`，schema `2`。冻结 tool source hash：`a198491ce936c91ce7a1c848789cf9fb27c5fc720b90ae81725c2ddf65f779dc`。

[CORE_FREEZE.json](CORE_FREEZE.json) 的 65 份核心 Python 源码 live/archive hash 一致，AST 可解析；此项只是身份/语法核对。正式身份产物记录原引用的 36 份文件 saved/live hash 一致，两库 target commit 一致；没有宣称工作区 clean。两库和共有组件的正式 publication identity 已验证；本报告没有再次执行检测器或读取数据库。

- [CodePatchBay 自动报告](codepatchbay-automatic-report.md)与[扫描记录](codepatchbay-integration.json)。
- [WinWinCode 自动报告](winwincode-automatic-report.md)与[扫描记录](winwincode-integration.json)。
- [CodePatchBay 简明分析](codepatchbay-analysis-summary.md)、[WinWinCode 简明分析](winwincode-analysis-summary.md)。
- [原五项结果账本](goal-ledger.json)、[原 26 条比较](ORIGINAL_BASELINE_COMPARISON.json)、[正式身份](PUBLICATION_IDENTITY.json)。
- [全文范围对照](REPORT_ALIGNMENT_RESULTS.json)、[本报告输入与核对记录](RELEASE_REPORT_INPUTS.json)。

[正常 report CLI 读回记录](CLI_REPORT_READBACK.json) 确认 WinWinCode 的 [导出 Markdown](winwincode-cli-report-readback.md) 与[正式 Markdown](winwincode-automatic-report.md) 字节一致，属于保存快照 `cc327a390837a897be93cdd4bdd4d9ad652c47f70f0b0dbfbbf89a52b463d372`。该 CLI 没有重扫或重算检测器；普通 Store 初始化已记录，其连接不是只读连接，前后逻辑行/Schema/身份指纹保持一致。数据库物理字节相同=`false`，不把初始化视为无物理效果。本生成器只核对保存记录及 Markdown hash，没有重跑 CLI 或打开数据库。

[原报告范围与静态边界](REPORT_SCOPE_GAPS.md) 区分已完成的原有限内容、保留的 source-only 边界及原明确未审范围；其导航不增加新评分或审批。
