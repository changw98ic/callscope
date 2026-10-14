# CodePatchBay · 保存的自动分析摘要

此摘要只展示已保存正式报告的结果和证据导航；不重新分析、不新增评价，也不替代完整证据。
五项判断是实现追踪，不是全文报告或项目功能覆盖率。链标题只是规则 ID 的展示标签。

- 固定全文基准：[原分析报告](../astra-baseline/CODEPATCHBAY_ANALYSIS.md)；不设置重复 Astra 审批步骤。
- 完整自动报告：[Markdown](codepatchbay-automatic-report.md) / [JSON](codepatchbay-automatic-report.json)；[正式 integration](codepatchbay-integration.json)。
- 快照：`7b58e73339e7ad28592c4a0bede1da0028935b30edd940419841971b354c2bfe`；状态：`partial`；报告版本：`captured-project-analysis-report-2`。
- 实现：`0.13.0` / `static-multilang-13` / `call-rules-12-report-relations`。
- 源码身份：`4e07250709288887cd79ae51b5f23f0239e054bc1db40371f7e7d0609148791b`。
- 策略身份：`0fff976c5bcee4485b553448ac80df4298b47a8c4656aaab6062324d4e9bbdfc`。
- 保存 JSON SHA256：`6fe5fe8a23ce386b3d5641ed6f8964d6bb5aa90f19b735ff03d0f2bf6b046fb0`；integration SHA256：`d81223a18f733d2fd238c22f21dee13f9db8f2739ef7e9c8e0ce18c486a1a6ea`。
- 保存比较范围：v12 used CocoIndex; v13 cold and warm scans both recompute every static frontend and detector. Not a same-engine precision/performance comparison.

## 保存范围与结构盘点

选入 `333` 文件，完整解析 `330`；文件状态 `{"parsed":330,"unsupported":3}`。
调用图保存 `11085` 节点、`60571` 边；确定调用 `23380`。这些是结构统计。
外部 `18429` / 动态 `18326` / 歧义 `429` / 未解析 `7`；外部回调边界 `11896`。
捕获辅助原文 `2`；源根 `["."]`。完整范围见 [/coverage](codepatchbay-automatic-report.json#/coverage)。

下表仅展示文件数最多的 12 个保存目录条目；目录名不是推断出的运行职责。

| 保存目录 | 文件 / 解析 | 语言文件数 |
| --- | --- | --- |
| `server/services` | 74 / 74 | `{"typescript":74}` |
| `core/engine` | 43 / 43 | `{"typescript":43}` |
| `scripts` | 40 / 38 | `{"shell":2,"typescript":38}` |
| `core/indexing` | 26 / 26 | `{"typescript":26}` |
| `cli/commands` | 21 / 21 | `{"typescript":21}` |
| `core/workflow` | 17 / 17 | `{"typescript":17}` |
| `core/agents` | 13 / 13 | `{"typescript":13}` |
| `core/contracts` | 13 / 13 | `{"typescript":13}` |
| `shared` | 9 / 9 | `{"typescript":9}` |
| `core/phases` | 8 / 8 | `{"typescript":8}` |
| `core/policy` | 7 / 7 | `{"typescript":7}` |
| `server/orchestrator` | 7 / 7 | `{"typescript":7}` |

全部目录 `38`，保存的确定跨目录依赖条目 `119`；来源见 [/architecture](codepatchbay-automatic-report.json#/architecture)。
依赖样本仅来自已确定图连接，不证明动态可达、执行顺序或职责正确性。

## 捕获的项目声明

manifest、脚本名称、依赖及文档标题都是捕获声明；没有执行脚本或验证依赖实际可用。

| 保存 manifest | 格式 | 保存名称 / 版本 |
| --- | --- | --- |
| `package.json` | `json` | `{"name":"codepatchbay","version":"0.5.0"}` |

声明文档 `1`，声明缺口 `[]`；详见 [/project_declarations](codepatchbay-automatic-report.json#/project_declarations)。

## 已保存的完整条件判断

以下 summary、derived_judgment、完整性/支持性和义务状态直接复制；成立条件与反证保留原 JSON 指针。

### `CPB-01`

提交选项与所读执行预算之间存在接线差异；参数构造、消息关系、消费者及不同重试预算分别得到源码证据，适用分支和不透明消费者保留。

derived_judgment：`"On the checked normal pipeline record/message path, the submitted retries field is transported as metadata but the managed worker constructs an independent selected literal. Actual queue, phase and infrastructure decisions use their distinct local authorities. Existing records, finalizer-only, early returns, opaque consumers and unsuccessful/not-run operations bound this finding; retry capability is present."`
assessment=`scoped_static_judgment_reproduced`；complete=`true`；support=`true`。
必要义务（原状态）：`P1=supported, P2=supported, P3=supported, P4=supported, P5=supported, P6=supported`；必要缺口：`[]`。
Finding=`1978d3f48218391a36a82e8f`；Evidence=`3df40e7e4b2844a5dd6506ca`；保存 evidence 指针=`/evidence/0/details`（相对于该 Finding）。
完整 [/judgments/0](codepatchbay-automatic-report.json#/judgments/0)；条件 [/judgments/0/conditions](codepatchbay-automatic-report.json#/judgments/0/conditions)；反证 [/judgments/0/refutations](codepatchbay-automatic-report.json#/judgments/0/refutations)；缺口 [/judgments/0/necessary_gaps](codepatchbay-automatic-report.json#/judgments/0/necessary_gaps)。

### `CPB-02`

状态 `superseded` 在所选身份条件下的终态谓词结果为 `False`，权威终态集合成员关系为 `True`；消费者据此进入拒绝分支。恢复政策和权威写入保护分别保存。

derived_judgment：`{"authority_terminal_membership":true,"classification_differs":true,"kind":"conditional_terminal_classification_difference","recovery_is_required_or_authorized":false,"status":"superseded","terminal_state_can_be_illegally_mutated":false,"valid_identity_predicate_result":false}`
assessment=`scoped_static_judgment_reproduced`；complete=`true`；support=`true`。
必要义务（原状态）：`S1=supported, S2=supported, S3=supported, S4=supported, S5=supported`；必要缺口：`[]`。
Finding=`e465a1162af15e0336a0c410`；Evidence=`f493e9c9e901101b279f221c`；保存 evidence 指针=`/evidence/0/details`（相对于该 Finding）。
完整 [/judgments/1](codepatchbay-automatic-report.json#/judgments/1)；条件 [/judgments/1/conditions](codepatchbay-automatic-report.json#/judgments/1/conditions)；反证 [/judgments/1/refutations](codepatchbay-automatic-report.json#/judgments/1/refutations)；缺口 [/judgments/1/necessary_gaps](codepatchbay-automatic-report.json#/judgments/1/necessary_gaps)。

### `CPB-03`

预查与权威写入的去重口径不同；从实际保护区和状态转换生成的有限交错可产生重复非终态记录，同时保存可以复用的顺序和失败条件。

derived_judgment：`"Two same-project/key/description default submissions can both observe no row; the first protected insert can be guardedly scheduled before the second protected check; the pending-only inner check then inserts a second nonterminal row"`
assessment=`scoped_static_judgment_reproduced`；complete=`true`；support=`true`。
必要义务（原状态）：`A1=supported, A2=supported, A3=supported, A4=supported, A5=supported, A6=supported, A7=supported`；必要缺口：`[]`。
Finding=`d55451aeec7a362795d8447d`；Evidence=`1dddaf6898b23e4f45015e0d`；保存 evidence 指针=`/evidence/0/details`（相对于该 Finding）。
完整 [/judgments/2](codepatchbay-automatic-report.json#/judgments/2)；条件 [/judgments/2/conditions](codepatchbay-automatic-report.json#/judgments/2/conditions)；反证 [/judgments/2/refutations](codepatchbay-automatic-report.json#/judgments/2/refutations)；缺口 [/judgments/2/necessary_gaps](codepatchbay-automatic-report.json#/judgments/2/necessary_gaps)。

## 所选主要源码链

显示每条保存规则的实际 assessment 和缺口；source-structure 支持与目标分派闭合分开。

### CodePatchBay 记录与资源写者 · `cpb-captured-record-resource-writers`

`resource_writer_ownership`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`7bd04b9dbd2d227e7d857618`；Evidence=`e9237f1a033181ebef41f71b`。
源码/关系 [/functional_chains/0](codepatchbay-automatic-report.json#/functional_chains/0)；缺段 [/functional_chains/0/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/0/analysis_gaps)；模型 [/functional_chains/0/trusted_models](codepatchbay-automatic-report.json#/functional_chains/0/trusted_models)；policy [/functional_chains/0/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/0/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| all_mutations_authorized_proven | false | [/functional_chains/0/pattern/all_mutations_authorized_proven](codepatchbay-automatic-report.json#/functional_chains/0/pattern/all_mutations_authorized_proven) |
| all_storage_resources_bound_proven | false | [/functional_chains/0/pattern/all_storage_resources_bound_proven](codepatchbay-automatic-report.json#/functional_chains/0/pattern/all_storage_resources_bound_proven) |
| call_record_and_effect_frontiers/shown_items/0/activation_and_physical_effect_proven | false | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/authenticated_call_edge_id | 7f3ae304194de7380672e7e7 | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/authenticated_callee_graph_node_id | ts:server/services/event/event-store#bindEventStreamIdentity | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/captured_callee_source | bindEventStreamIdentity | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/captured_receiver_token | null | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/role | eventCommit | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/source_call_fact_id | 36d22b0b81c02e12c31d2b44 | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/kind | identifier | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/name | event | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/location/file | server/services/event/event-store.ts | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/location/line | 1180 | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/location/column | 46 | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/location/end_line | 1180 | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/location/start_byte | 39869 | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/location/end_byte | 39874 | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/reference/declaration_id | 15a5eb8af471c36757e2ea9b1c5771c4a7b221e10a9b97a4ca02a5ad83cab200 | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/reference/declaration_kind | parameter | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/reference/identity_complete | true | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/reference/parameter_index | 3 | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/reference/state | unique | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/reference/binder_location/file | server/services/event/event-store.ts | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/reference/binder_location/line | 1179 | [/functional_chains/0/pattern/call_record_and_effect_frontiers](codepatchbay-automatic-report.json#/functional_chains/0/pattern/call_record_and_effect_frontiers) |

完整关系 [/functional_chains/0/pattern](codepatchbay-automatic-report.json#/functional_chains/0/pattern)；原 source facts [/functional_chains/0/source_facts](codepatchbay-automatic-report.json#/functional_chains/0/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### 事件提交与索引投影 · `cpb-event-index-projection`

`event_index_projection`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`record_projection_physical_commit_and_all_recovery_not_proven`；Finding=`0dee9a93542ad5f26ac7d58e`；Evidence=`73c1b6849a90fa7c4ef14ec3`。
源码/关系 [/functional_chains/1](codepatchbay-automatic-report.json#/functional_chains/1)；缺段 [/functional_chains/1/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/1/analysis_gaps)；模型 [/functional_chains/1/trusted_models](codepatchbay-automatic-report.json#/functional_chains/1/trusted_models)；policy [/functional_chains/1/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/1/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| all_selected_roles_bound | true | [/functional_chains/1/pattern/all_selected_roles_bound](codepatchbay-automatic-report.json#/functional_chains/1/pattern/all_selected_roles_bound) |
| assignment_attempts/append/0/assignment_success_proven | false | [/functional_chains/1/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/1/pattern/assignment_attempts) |
| assignment_attempts/append/0/callback_activation_proven | false | [/functional_chains/1/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/1/pattern/assignment_attempts) |
| assignment_attempts/append/0/id | b3baebe2291949d9ff519156 | [/functional_chains/1/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/1/pattern/assignment_attempts) |
| assignment_attempts/append/0/kind | record_assignment_source_attempt | [/functional_chains/1/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/1/pattern/assignment_attempts) |
| assignment_attempts/append/0/origin | source-derived | [/functional_chains/1/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/1/pattern/assignment_attempts) |
| assignment_attempts/append/0/record_relations_version | captured-record-projection-relations-1 | [/functional_chains/1/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/1/pattern/assignment_attempts) |
| assignment_attempts/append/0/role | append | [/functional_chains/1/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/1/pattern/assignment_attempts) |
| assignment_attempts/append/0/left/kind | member_expression | [/functional_chains/1/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/1/pattern/assignment_attempts) |
| assignment_attempts/append/0/left/reference_dependencies_only | true | [/functional_chains/1/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/1/pattern/assignment_attempts) |
| assignment_attempts/append/0/left/runtime_value_or_heap_identity_proven | false | [/functional_chains/1/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/1/pattern/assignment_attempts) |
| assignment_attempts/append/0/left/source | blocked.jobId | [/functional_chains/1/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/1/pattern/assignment_attempts) |
| assignment_attempts/append/0/left/source_truncated | false | [/functional_chains/1/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/1/pattern/assignment_attempts) |
| assignment_attempts/append/0/left/location/file | server/services/event/event-store.ts | [/functional_chains/1/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/1/pattern/assignment_attempts) |
| assignment_attempts/append/0/left/location/line | 1202 | [/functional_chains/1/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/1/pattern/assignment_attempts) |
| assignment_attempts/append/0/left/location/column | 7 | [/functional_chains/1/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/1/pattern/assignment_attempts) |
| assignment_attempts/append/0/left/location/end_line | 1202 | [/functional_chains/1/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/1/pattern/assignment_attempts) |
| assignment_attempts/append/0/left/location/start_byte | 40950 | [/functional_chains/1/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/1/pattern/assignment_attempts) |
| assignment_attempts/append/0/left/location/end_byte | 40963 | [/functional_chains/1/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/1/pattern/assignment_attempts) |
| assignment_attempts/append/0/left/reference_path/binding_id | 0dd91f58d1c285e80c670cbcc0470bf4560bb22d05055859fce78fd6ffdb6490 | [/functional_chains/1/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/1/pattern/assignment_attempts) |
| assignment_attempts/append/0/left/reference_path/binding/binding_path | null | [/functional_chains/1/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/1/pattern/assignment_attempts) |
| assignment_attempts/append/0/left/reference_path/binding/declaration_id | 0dd91f58d1c285e80c670cbcc0470bf4560bb22d05055859fce78fd6ffdb6490 | [/functional_chains/1/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/1/pattern/assignment_attempts) |
| assignment_attempts/append/0/left/reference_path/binding/declaration_kind | const | [/functional_chains/1/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/1/pattern/assignment_attempts) |
| assignment_attempts/append/0/left/reference_path/binding/identity_complete | true | [/functional_chains/1/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/1/pattern/assignment_attempts) |

完整关系 [/functional_chains/1/pattern](codepatchbay-automatic-report.json#/functional_chains/1/pattern)；原 source facts [/functional_chains/1/source_facts](codepatchbay-automatic-report.json#/functional_chains/1/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### 访问审计与响应字段 · `cpb-report-access-audit-response`

`conditional_gate_relations`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`002f93ee7108409cdc730fbb`；Evidence=`7853f91ff429ca3c208067f5`。
源码/关系 [/functional_chains/2](codepatchbay-automatic-report.json#/functional_chains/2)；缺段 [/functional_chains/2/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/2/analysis_gaps)；模型 [/functional_chains/2/trusted_models](codepatchbay-automatic-report.json#/functional_chains/2/trusted_models)；policy [/functional_chains/2/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/2/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| all_project_functionality_proven | false | [/functional_chains/2/pattern/all_project_functionality_proven](codepatchbay-automatic-report.json#/functional_chains/2/pattern/all_project_functionality_proven) |
| budgets/summary_path_limit | 256 | [/functional_chains/2/pattern/budgets](codepatchbay-automatic-report.json#/functional_chains/2/pattern/budgets) |
| budgets/truncated | false | [/functional_chains/2/pattern/budgets](codepatchbay-automatic-report.json#/functional_chains/2/pattern/budgets) |
| groups/access_audit/all_http_security_or_business_mutations_proven | false | [/functional_chains/2/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/2/pattern/groups) |
| groups/access_audit/job_audit_subject_equivalence_claimed | false | [/functional_chains/2/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/2/pattern/groups) |
| groups/access_audit/scoped_source_supported | true | [/functional_chains/2/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/2/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/actual_awaited_method | append | [/functional_chains/2/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/2/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/actual_http_response_delivery_proven | false | [/functional_chains/2/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/2/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/audit_write_durability_proven | false | [/functional_chains/2/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/2/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/business_mutation_rollback_proven | false | [/functional_chains/2/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/2/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/callback_activation_proven | false | [/functional_chains/2/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/2/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/catch_return_or_throw_before_response | false | [/functional_chains/2/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/2/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/conditional_gate_version | captured-conditional-gate-relations-1 | [/functional_chains/2/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/2/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/id | f8b0d82ab1fe46ff51cb3f24 | [/functional_chains/2/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/2/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/kind | awaited_access_audit_response_replacement | [/functional_chains/2/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/2/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/opener_call_fact_id | ec1135a5dac8613854252f66 | [/functional_chains/2/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/2/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/opener_result_declaration_id | 19efdab5e3e1669abe3d093426107c50a993a391f86e0560d98a150e00cd26dc | [/functional_chains/2/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/2/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/origin | source-derived | [/functional_chains/2/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/2/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/response_binding_declaration_id | 8dbb856a98a7669f0b001c352a3925dcb500b2aa24c4383cea203691c0a4852c | [/functional_chains/2/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/2/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/actual_response_writer_call/actual_callee_graph_node_id | ts:server/index#sendJson | [/functional_chains/2/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/2/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/actual_response_writer_call/authenticated_call_edge_id | 061961006a25235706f2e22c | [/functional_chains/2/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/2/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/actual_response_writer_call/binding_state | authenticated_internal_call | [/functional_chains/2/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/2/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/actual_response_writer_call/call_is_entire_binding_initializer | false | [/functional_chains/2/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/2/pattern/groups) |
| groups/access_audit/response_replacement_relations/0/actual_response_writer_call/call_runtime_success_proven | false | [/functional_chains/2/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/2/pattern/groups) |

完整关系 [/functional_chains/2/pattern](codepatchbay-automatic-report.json#/functional_chains/2/pattern)；原 source facts [/functional_chains/2/source_facts](codepatchbay-automatic-report.json#/functional_chains/2/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### agent allowlist / env / sandbox 策略 · `cpb-report-agent-execution-policy`

`agent_execution_policy`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`3a1cca07e75c0430c7aadaba`；Evidence=`7429cb490aca94b2f1159cb1`。
源码/关系 [/functional_chains/3](codepatchbay-automatic-report.json#/functional_chains/3)；缺段 [/functional_chains/3/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/3/analysis_gaps)；模型 [/functional_chains/3/trusted_models](codepatchbay-automatic-report.json#/functional_chains/3/trusted_models)；policy [/functional_chains/3/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/3/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| admission_and_postexecution_review/admission_fact_id | 3b7d25a81d0d4625f858d6fe | [/functional_chains/3/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/3/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/readonly_audit_activation_or_success_proven | false | [/functional_chains/3/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/3/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/supported | true | [/functional_chains/3/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/3/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/unique_pool_implementation_proven | false | [/functional_chains/3/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/3/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/actual_callee_graph_node_id | null | [/functional_chains/3/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/3/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/authenticated_call_edge_id | null | [/functional_chains/3/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/3/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/binding_state | external_or_unknown_call | [/functional_chains/3/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/3/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/call_is_entire_binding_initializer | true | [/functional_chains/3/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/3/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/call_runtime_success_proven | false | [/functional_chains/3/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/3/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/callee_activation_proven | false | [/functional_chains/3/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/3/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/callee_source | execPool.execute | [/functional_chains/3/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/3/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/captured_resolution | dynamic | [/functional_chains/3/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/3/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/captured_site_edge_id | dc452cc1b770dc3d20a64eab | [/functional_chains/3/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/3/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/id | 5696f3a8a76bcc3f0c265a23 | [/functional_chains/3/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/3/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/kind | captured_call_step | [/functional_chains/3/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/3/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/origin | source-derived | [/functional_chains/3/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/3/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/owner_graph_node_id | ts:core/agents/agent-runner#runAgent | [/functional_chains/3/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/3/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/role | runner | [/functional_chains/3/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/3/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/arguments/0/kind | identifier | [/functional_chains/3/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/3/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/arguments/0/name | agentName | [/functional_chains/3/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/3/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/arguments/0/location/file | core/agents/agent-runner.ts | [/functional_chains/3/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/3/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/arguments/0/location/line | 527 | [/functional_chains/3/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/3/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/arguments/0/location/column | 47 | [/functional_chains/3/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/3/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/arguments/0/location/end_line | 527 | [/functional_chains/3/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/3/pattern/admission_and_postexecution_review) |

完整关系 [/functional_chains/3/pattern](codepatchbay-automatic-report.json#/functional_chains/3/pattern)；原 source facts [/functional_chains/3/source_facts](codepatchbay-automatic-report.json#/functional_chains/3/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### 完成门条件与豁免 · `cpb-report-completion-gate-conditions`

`conditional_gate_relations`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`40663191c9c065dec61571d5`；Evidence=`1688042aea3b1caa613c4f85`。
源码/关系 [/functional_chains/4](codepatchbay-automatic-report.json#/functional_chains/4)；缺段 [/functional_chains/4/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/4/analysis_gaps)；模型 [/functional_chains/4/trusted_models](codepatchbay-automatic-report.json#/functional_chains/4/trusted_models)；policy [/functional_chains/4/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/4/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

`absent_input_partitions`；完整 [/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/absent_input_partitions](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/absent_input_partitions)；保存总行数 `2`。

| boolean_result | input_cell | unknown | 完整行 |
| --- | --- | --- | --- |
| false | missing | false | [/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/absent_input_partitions/0](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/absent_input_partitions/0) |
| false | null | false | [/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/absent_input_partitions/1](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/absent_input_partitions/1) |

`record_partitions`；完整 [/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/record_partitions](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/record_partitions)；保存总行数 `9`。

| boolean_result | property_cells | unknown | 完整行 |
| --- | --- | --- | --- |
| false | {"planMode":"none","workflow":"docs"} | false | [/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/0](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/0) |
| false | {"planMode":"none","workflow":"readonly"} | false | [/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/1](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/1) |
| false | {"planMode":"none","workflow":"<other-than-captured-literals>"} | false | [/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/2](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/2) |
| false | {"planMode":"parent","workflow":"docs"} | false | [/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/3](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/3) |
| false | {"planMode":"parent","workflow":"readonly"} | false | [/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/4](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/4) |
| false | {"planMode":"parent","workflow":"<other-than-captured-literals>"} | false | [/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/5](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/5) |
| false | {"planMode":"<other-than-captured-literals>","workflow":"docs"} | false | [/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/6](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/6) |
| false | {"planMode":"<other-than-captured-literals>","workflow":"readonly"} | false | [/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/7](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/7) |
| true | {"planMode":"<other-than-captured-literals>","workflow":"<other-than-captured-literals>"} | false | [/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/8](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/8) |

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| all_project_functionality_proven | false | [/functional_chains/4/pattern/all_project_functionality_proven](codepatchbay-automatic-report.json#/functional_chains/4/pattern/all_project_functionality_proven) |
| budgets/summary_path_limit | 256 | [/functional_chains/4/pattern/budgets](codepatchbay-automatic-report.json#/functional_chains/4/pattern/budgets) |
| budgets/truncated | false | [/functional_chains/4/pattern/budgets](codepatchbay-automatic-report.json#/functional_chains/4/pattern/budgets) |
| groups/completion/checklist_internal_checks_proven | false | [/functional_chains/4/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups) |
| groups/completion/external_verdict_or_evidence_truth_proven | false | [/functional_chains/4/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups) |
| groups/completion/scoped_source_supported | true | [/functional_chains/4/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups) |
| groups/completion/statement | Return records, local condition dependencies and source order are computed separately. Path conditions retain prior short circuits; local conditions describe the current gate only. No target inputs were executed. | [/functional_chains/4/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups) |
| groups/completion/condition_consumers/shown_items/0/branch_runtime_selected | false | [/functional_chains/4/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/conditional_gate_version | captured-conditional-gate-relations-1 | [/functional_chains/4/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/id | 6e11199e5c634d80b19cb378 | [/functional_chains/4/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/kind | completion_gate_condition_consumes_result | [/functional_chains/4/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/normal_source_order_index | 0 | [/functional_chains/4/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/origin | source-derived | [/functional_chains/4/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/affected_return_fact_ids/0 | c91a05236d12fc8e698afa06 | [/functional_chains/4/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/condition_abstract_form/declaration_id | 952fdb817337e3c4eac25e633da13ada829ba8def945ddd950292d94f531f5d5 | [/functional_chains/4/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/condition_abstract_form/kind | input | [/functional_chains/4/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/condition_abstract_form/name | checklist | [/functional_chains/4/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/condition_source/kind | identifier | [/functional_chains/4/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/condition_source/name | checklist | [/functional_chains/4/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/condition_source/location/file | core/engine/completion-gate.ts | [/functional_chains/4/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/condition_source/location/line | 182 | [/functional_chains/4/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/condition_source/location/column | 7 | [/functional_chains/4/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/condition_source/location/end_line | 182 | [/functional_chains/4/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/condition_consumers) |
| groups/completion/condition_consumers/shown_items/0/condition_source/location/start_byte | 6306 | [/functional_chains/4/pattern/groups/completion/condition_consumers](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/condition_consumers) |

完整关系 [/functional_chains/4/pattern](codepatchbay-automatic-report.json#/functional_chains/4/pattern)；原 source facts [/functional_chains/4/source_facts](codepatchbay-automatic-report.json#/functional_chains/4/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### finalizer → 结果写入 → reconcile · `cpb-report-conditional-delivery-result`

`conditional_delivery_result`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`01d82b550a91c8053252ab43`；Evidence=`132197875ea8f2a4cff27887`。
源码/关系 [/functional_chains/5](codepatchbay-automatic-report.json#/functional_chains/5)；缺段 [/functional_chains/5/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/5/analysis_gaps)；模型 [/functional_chains/5/trusted_models](codepatchbay-automatic-report.json#/functional_chains/5/trusted_models)；policy [/functional_chains/5/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/5/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| all_function_paths_or_hidden_effects_proven | false | [/functional_chains/5/pattern/all_function_paths_or_hidden_effects_proven](codepatchbay-automatic-report.json#/functional_chains/5/pattern/all_function_paths_or_hidden_effects_proven) |
| all_recovery_complete_proven | false | [/functional_chains/5/pattern/all_recovery_complete_proven](codepatchbay-automatic-report.json#/functional_chains/5/pattern/all_recovery_complete_proven) |
| components/finalizer/remote_finalization_success_proven | false | [/functional_chains/5/pattern/components](codepatchbay-automatic-report.json#/functional_chains/5/pattern/components) |
| components/finalizer/supported | true | [/functional_chains/5/pattern/components](codepatchbay-automatic-report.json#/functional_chains/5/pattern/components) |
| components/finalizer/conditional_finalization/0/supported | true | [/functional_chains/5/pattern/components](codepatchbay-automatic-report.json#/functional_chains/5/pattern/components) |
| components/finalizer/conditional_finalization/0/fact/actual_execution_or_finalizer_success_proven | false | [/functional_chains/5/pattern/components](codepatchbay-automatic-report.json#/functional_chains/5/pattern/components) |
| components/finalizer/conditional_finalization/0/fact/execution_success_literal | completed | [/functional_chains/5/pattern/components](codepatchbay-automatic-report.json#/functional_chains/5/pattern/components) |
| components/finalizer/conditional_finalization/0/fact/failure_call_fact_id | cadb7d6b05a88749c034d2e8 | [/functional_chains/5/pattern/components](codepatchbay-automatic-report.json#/functional_chains/5/pattern/components) |
| components/finalizer/conditional_finalization/0/fact/id | baf245b12a76346b76739727 | [/functional_chains/5/pattern/components](codepatchbay-automatic-report.json#/functional_chains/5/pattern/components) |
| components/finalizer/conditional_finalization/0/fact/kind | delivery_execution_success_requires_conditional_finalization | [/functional_chains/5/pattern/components](codepatchbay-automatic-report.json#/functional_chains/5/pattern/components) |
| components/finalizer/conditional_finalization/0/fact/origin | source-derived | [/functional_chains/5/pattern/components](codepatchbay-automatic-report.json#/functional_chains/5/pattern/components) |
| components/finalizer/conditional_finalization/0/fact/execution_status_path/0 | 4650e60de88b55260c2b9a13c5aaa313a7ebebe37a7d59d17e2c10f65b77f754 | [/functional_chains/5/pattern/components](codepatchbay-automatic-report.json#/functional_chains/5/pattern/components) |
| components/finalizer/conditional_finalization/0/fact/execution_status_path/1/0 | status | [/functional_chains/5/pattern/components](codepatchbay-automatic-report.json#/functional_chains/5/pattern/components) |
| components/finalizer/conditional_finalization/0/fact/finalizer_ok_path/0 | 7f9440dc927642e5d70a52081d3a2d94d47dc65bf291550849e9a3a2137f6e1a | [/functional_chains/5/pattern/components](codepatchbay-automatic-report.json#/functional_chains/5/pattern/components) |
| components/finalizer/conditional_finalization/0/fact/finalizer_ok_path/1/0 | ok | [/functional_chains/5/pattern/components](codepatchbay-automatic-report.json#/functional_chains/5/pattern/components) |
| components/finalizer/conditional_finalization/0/fact/location/file | runtime/worker/assignment-finalizer.ts | [/functional_chains/5/pattern/components](codepatchbay-automatic-report.json#/functional_chains/5/pattern/components) |
| components/finalizer/conditional_finalization/0/fact/location/line | 1236 | [/functional_chains/5/pattern/components](codepatchbay-automatic-report.json#/functional_chains/5/pattern/components) |
| components/finalizer/conditional_finalization/0/fact/location/column | 9 | [/functional_chains/5/pattern/components](codepatchbay-automatic-report.json#/functional_chains/5/pattern/components) |
| components/finalizer/conditional_finalization/0/fact/location/end_line | 1236 | [/functional_chains/5/pattern/components](codepatchbay-automatic-report.json#/functional_chains/5/pattern/components) |
| components/finalizer/conditional_finalization/0/fact/location/start_byte | 44544 | [/functional_chains/5/pattern/components](codepatchbay-automatic-report.json#/functional_chains/5/pattern/components) |
| components/finalizer/conditional_finalization/0/fact/location/end_byte | 44644 | [/functional_chains/5/pattern/components](codepatchbay-automatic-report.json#/functional_chains/5/pattern/components) |
| components/finalizer/conditional_finalization/0/fact/metadata_enable_path/0 | 5c0c7be8e18e8c5cf81f007821034233cf5505d132e89d1e283d4cec2dbc6e3f | [/functional_chains/5/pattern/components](codepatchbay-automatic-report.json#/functional_chains/5/pattern/components) |
| components/finalizer/conditional_finalization/0/fact/metadata_enable_path/1/0 | metadata | [/functional_chains/5/pattern/components](codepatchbay-automatic-report.json#/functional_chains/5/pattern/components) |
| components/finalizer/conditional_finalization/0/fact/metadata_enable_path/1/1 | autoFinalize | [/functional_chains/5/pattern/components](codepatchbay-automatic-report.json#/functional_chains/5/pattern/components) |

完整关系 [/functional_chains/5/pattern](codepatchbay-automatic-report.json#/functional_chains/5/pattern)；原 source facts [/functional_chains/5/source_facts](codepatchbay-automatic-report.json#/functional_chains/5/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### runJob 主链与前置阻断 · `cpb-report-engine-stage-chain`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`90ad7907624fb1774bd0cd51`；Evidence=`5498f400cf6844ba653fad65`。
源码/关系 [/functional_chains/6](codepatchbay-automatic-report.json#/functional_chains/6)；缺段 [/functional_chains/6/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/6/analysis_gaps)；模型 [/functional_chains/6/trusted_models](codepatchbay-automatic-report.json#/functional_chains/6/trusted_models)；policy [/functional_chains/6/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/6/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/6/pattern/scoped_source_supported](codepatchbay-automatic-report.json#/functional_chains/6/pattern/scoped_source_supported) |
| sequences/entry/all_function_paths_or_effects_accounted | false | [/functional_chains/6/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/6/pattern/sequences) |
| sequences/entry/future_or_callback_activation_proven | false | [/functional_chains/6/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/6/pattern/sequences) |
| sequences/entry/region_kind | function_declaration | [/functional_chains/6/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/6/pattern/sequences) |
| sequences/entry/role | entry | [/functional_chains/6/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/6/pattern/sequences) |
| sequences/entry/conditions/0/id | c3305764e5780bce6d7e4aad | [/functional_chains/6/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/6/pattern/sequences) |
| sequences/entry/conditions/0/kind | source_guard_and_abrupt_branch | [/functional_chains/6/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/6/pattern/sequences) |
| sequences/entry/conditions/0/origin | source-derived | [/functional_chains/6/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/6/pattern/sequences) |
| sequences/entry/conditions/0/role | entry | [/functional_chains/6/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/6/pattern/sequences) |
| sequences/entry/conditions/0/runtime_predicate_proven | false | [/functional_chains/6/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/6/pattern/sequences) |
| sequences/entry/conditions/0/branches/0/branch | then | [/functional_chains/6/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/6/pattern/sequences) |
| sequences/entry/conditions/0/branches/0/branch_all_paths_abrupt_proven | true | [/functional_chains/6/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/6/pattern/sequences) |
| sequences/entry/conditions/0/branches/0/abrupt_source_expressions/0/kind | throw_statement | [/functional_chains/6/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/6/pattern/sequences) |
| sequences/entry/conditions/0/branches/0/abrupt_source_expressions/0/runtime_completion_proven | false | [/functional_chains/6/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/6/pattern/sequences) |
| sequences/entry/conditions/0/branches/0/abrupt_source_expressions/0/location/file | core/engine/run-job.ts | [/functional_chains/6/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/6/pattern/sequences) |
| sequences/entry/conditions/0/branches/0/abrupt_source_expressions/0/location/line | 67 | [/functional_chains/6/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/6/pattern/sequences) |
| sequences/entry/conditions/0/branches/0/abrupt_source_expressions/0/location/column | 5 | [/functional_chains/6/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/6/pattern/sequences) |
| sequences/entry/conditions/0/branches/0/abrupt_source_expressions/0/location/end_line | 67 | [/functional_chains/6/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/6/pattern/sequences) |
| sequences/entry/conditions/0/branches/0/abrupt_source_expressions/0/location/start_byte | 2499 | [/functional_chains/6/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/6/pattern/sequences) |
| sequences/entry/conditions/0/branches/0/abrupt_source_expressions/0/location/end_byte | 2555 | [/functional_chains/6/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/6/pattern/sequences) |
| sequences/entry/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/call_effects_or_result_proven | 显示投影省略 | [/functional_chains/6/pattern/sequences/entry/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/call_effects_or_result_proven](codepatchbay-automatic-report.json#/functional_chains/6/pattern/sequences/entry/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/call_effects_or_result_proven) |
| sequences/entry/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/callee_source | 显示投影省略 | [/functional_chains/6/pattern/sequences/entry/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/callee_source](codepatchbay-automatic-report.json#/functional_chains/6/pattern/sequences/entry/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/callee_source) |
| sequences/entry/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/kind | 显示投影省略 | [/functional_chains/6/pattern/sequences/entry/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/kind](codepatchbay-automatic-report.json#/functional_chains/6/pattern/sequences/entry/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/kind) |
| sequences/entry/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/arguments | 显示投影省略 | [/functional_chains/6/pattern/sequences/entry/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/arguments](codepatchbay-automatic-report.json#/functional_chains/6/pattern/sequences/entry/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/arguments) |

完整关系 [/functional_chains/6/pattern](codepatchbay-automatic-report.json#/functional_chains/6/pattern)；原 source facts [/functional_chains/6/source_facts](codepatchbay-automatic-report.json#/functional_chains/6/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### audit best-effort 分支 · `cpb-report-job-audit-best-effort`

`best_effort_finalization`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`f0a3a53f129704f4f0875984`；Evidence=`b6d087ff6bf850a7823de709`。
源码/关系 [/functional_chains/7](codepatchbay-automatic-report.json#/functional_chains/7)；缺段 [/functional_chains/7/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/7/analysis_gaps)；模型 [/functional_chains/7/trusted_models](codepatchbay-automatic-report.json#/functional_chains/7/trusted_models)；policy [/functional_chains/7/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/7/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| audit_subject_equivalence_to_other_systems_proven | false | [/functional_chains/7/pattern/audit_subject_equivalence_to_other_systems_proven](codepatchbay-automatic-report.json#/functional_chains/7/pattern/audit_subject_equivalence_to_other_systems_proven) |
| caught_scopes/0/failure_swallowed_by_empty_catch_source | false | [/functional_chains/7/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/7/pattern/caught_scopes) |
| caught_scopes/0/finally_present | false | [/functional_chains/7/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/7/pattern/caught_scopes) |
| caught_scopes/0/id | 987d372c852ec7311a8dae7d | [/functional_chains/7/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/7/pattern/caught_scopes) |
| caught_scopes/0/kind | caught_call_failure_scope | [/functional_chains/7/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/7/pattern/caught_scopes) |
| caught_scopes/0/origin | source-derived | [/functional_chains/7/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/7/pattern/caught_scopes) |
| caught_scopes/0/role | entry | [/functional_chains/7/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/7/pattern/caught_scopes) |
| caught_scopes/0/runtime_failure_or_finalization_success_proven | false | [/functional_chains/7/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/7/pattern/caught_scopes) |
| caught_scopes/0/call_ids/0 | 0f3f1ef04fec926fb029977b | [/functional_chains/7/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/7/pattern/caught_scopes) |
| caught_scopes/0/call_ids/1 | fb0b5e6412e4a79a0807b3fd | [/functional_chains/7/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/7/pattern/caught_scopes) |
| caught_scopes/0/catch_body_location/file | core/engine/run-job.ts | [/functional_chains/7/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/7/pattern/caught_scopes) |
| caught_scopes/0/catch_body_location/line | 91 | [/functional_chains/7/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/7/pattern/caught_scopes) |
| caught_scopes/0/catch_body_location/column | 19 | [/functional_chains/7/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/7/pattern/caught_scopes) |
| caught_scopes/0/catch_body_location/end_line | 106 | [/functional_chains/7/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/7/pattern/caught_scopes) |
| caught_scopes/0/catch_body_location/start_byte | 3562 | [/functional_chains/7/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/7/pattern/caught_scopes) |
| caught_scopes/0/catch_body_location/end_byte | 4118 | [/functional_chains/7/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/7/pattern/caught_scopes) |
| caught_scopes/0/catch_location/file | core/engine/run-job.ts | [/functional_chains/7/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/7/pattern/caught_scopes) |
| caught_scopes/0/catch_location/line | 91 | [/functional_chains/7/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/7/pattern/caught_scopes) |
| caught_scopes/0/catch_location/column | 5 | [/functional_chains/7/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/7/pattern/caught_scopes) |
| caught_scopes/0/catch_location/end_line | 106 | [/functional_chains/7/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/7/pattern/caught_scopes) |
| caught_scopes/0/catch_location/start_byte | 3548 | [/functional_chains/7/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/7/pattern/caught_scopes) |
| caught_scopes/0/catch_location/end_byte | 4118 | [/functional_chains/7/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/7/pattern/caught_scopes) |
| caught_scopes/0/location/file | core/engine/run-job.ts | [/functional_chains/7/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/7/pattern/caught_scopes) |
| caught_scopes/0/location/line | 74 | [/functional_chains/7/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/7/pattern/caught_scopes) |

完整关系 [/functional_chains/7/pattern](codepatchbay-automatic-report.json#/functional_chains/7/pattern)；原 source facts [/functional_chains/7/source_facts](codepatchbay-automatic-report.json#/functional_chains/7/source_facts)。原投影截取标志 `false`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### readiness 提交前保护 · `cpb-report-readiness-abrupt-guard`

`conditional_gate_relations`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`c89bbef360a88ca00ec4fe96`；Evidence=`156760e090c5b5d73b7bcb91`。
源码/关系 [/functional_chains/8](codepatchbay-automatic-report.json#/functional_chains/8)；缺段 [/functional_chains/8/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/8/analysis_gaps)；模型 [/functional_chains/8/trusted_models](codepatchbay-automatic-report.json#/functional_chains/8/trusted_models)；policy [/functional_chains/8/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/8/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

`absent_input_partitions`；完整 [/functional_chains/8/pattern/groups/readiness/predicate_finite_partition/absent_input_partitions](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups/readiness/predicate_finite_partition/absent_input_partitions)；保存总行数 `2`。

| boolean_result | input_cell | unknown | 完整行 |
| --- | --- | --- | --- |
| null | missing | true | [/functional_chains/8/pattern/groups/readiness/predicate_finite_partition/absent_input_partitions/0](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups/readiness/predicate_finite_partition/absent_input_partitions/0) |
| null | null | true | [/functional_chains/8/pattern/groups/readiness/predicate_finite_partition/absent_input_partitions/1](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups/readiness/predicate_finite_partition/absent_input_partitions/1) |

`record_partitions`；完整 [/functional_chains/8/pattern/groups/readiness/predicate_finite_partition/record_partitions](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups/readiness/predicate_finite_partition/record_partitions)；保存总行数 `2`。

| boolean_result | property_cells | unknown | 完整行 |
| --- | --- | --- | --- |
| true | {"ok":false} | false | [/functional_chains/8/pattern/groups/readiness/predicate_finite_partition/record_partitions/0](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups/readiness/predicate_finite_partition/record_partitions/0) |
| false | {"ok":"<other-than-captured-literals>"} | false | [/functional_chains/8/pattern/groups/readiness/predicate_finite_partition/record_partitions/1](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups/readiness/predicate_finite_partition/record_partitions/1) |

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| all_project_functionality_proven | false | [/functional_chains/8/pattern/all_project_functionality_proven](codepatchbay-automatic-report.json#/functional_chains/8/pattern/all_project_functionality_proven) |
| budgets/summary_path_limit | 256 | [/functional_chains/8/pattern/budgets](codepatchbay-automatic-report.json#/functional_chains/8/pattern/budgets) |
| budgets/truncated | false | [/functional_chains/8/pattern/budgets](codepatchbay-automatic-report.json#/functional_chains/8/pattern/budgets) |
| groups/readiness/readiness_implementation_success_or_external_state_proven | false | [/functional_chains/8/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups) |
| groups/readiness/scoped_source_supported | true | [/functional_chains/8/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups) |
| groups/readiness/predicate_finite_partition/complete | false | [/functional_chains/8/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups) |
| groups/readiness/predicate_finite_partition/ordinary_record_no_getters_or_proxy_required | true | [/functional_chains/8/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups) |
| groups/readiness/predicate_finite_partition/ordinary_record_partition_complete | true | [/functional_chains/8/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups) |
| groups/readiness/predicate_finite_partition/other_cell_semantics | all other stable plain property values indistinguishable to captured strict comparisons | [/functional_chains/8/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups) |
| groups/readiness/predicate_finite_partition/record_cell_count | 2 | [/functional_chains/8/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups) |
| groups/readiness/predicate_finite_partition/runtime_inputs_exercised | false | [/functional_chains/8/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups) |
| groups/readiness/predicate_finite_partition/absent_input_partitions/presentation_table_ref | /source_relation_index/entries/8/presentation/tables/0 | [/functional_chains/8/pattern/groups/readiness/predicate_finite_partition/absent_input_partitions](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups/readiness/predicate_finite_partition/absent_input_partitions) |
| groups/readiness/predicate_finite_partition/absent_input_partitions/total_rows | 2 | [/functional_chains/8/pattern/groups/readiness/predicate_finite_partition/absent_input_partitions](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups/readiness/predicate_finite_partition/absent_input_partitions) |
| groups/readiness/predicate_finite_partition/absent_input_partitions/presentation_only | true | [/functional_chains/8/pattern/groups/readiness/predicate_finite_partition/absent_input_partitions](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups/readiness/predicate_finite_partition/absent_input_partitions) |
| groups/readiness/predicate_finite_partition/dimensions_derived_from_source_literals/ok/0 | false | [/functional_chains/8/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups) |
| groups/readiness/predicate_finite_partition/record_partitions/presentation_table_ref | /source_relation_index/entries/8/presentation/tables/1 | [/functional_chains/8/pattern/groups/readiness/predicate_finite_partition/record_partitions](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups/readiness/predicate_finite_partition/record_partitions) |
| groups/readiness/predicate_finite_partition/record_partitions/total_rows | 2 | [/functional_chains/8/pattern/groups/readiness/predicate_finite_partition/record_partitions](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups/readiness/predicate_finite_partition/record_partitions) |
| groups/readiness/predicate_finite_partition/record_partitions/presentation_only | true | [/functional_chains/8/pattern/groups/readiness/predicate_finite_partition/record_partitions](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups/readiness/predicate_finite_partition/record_partitions) |
| groups/readiness/relations/0/argument_binding_declaration_id | 54a1db8291cfa7b07e6d4ffa75e79ae07f814393334f0e4119c48015eb9cbf44 | [/functional_chains/8/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups) |
| groups/readiness/relations/0/conditional_gate_version | captured-conditional-gate-relations-1 | [/functional_chains/8/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups) |
| groups/readiness/relations/0/id | 22e69cfc9e54bd2fb6dd86c1 | [/functional_chains/8/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups) |
| groups/readiness/relations/0/kind | source_predicate_abrupt_guard_dominates_later_calls | [/functional_chains/8/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups) |
| groups/readiness/relations/0/origin | source-derived | [/functional_chains/8/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups) |
| groups/readiness/relations/0/role | readiness_entry | [/functional_chains/8/pattern/groups](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups) |

完整关系 [/functional_chains/8/pattern](codepatchbay-automatic-report.json#/functional_chains/8/pattern)；原 source facts [/functional_chains/8/source_facts](codepatchbay-automatic-report.json#/functional_chains/8/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### trusted probe 命令来源 · `cpb-report-trusted-probe-command-source`

`structured_command_source`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`structured_command_intermediate_values_and_external_effects_not_fully_proven`；Finding=`0b90c4a9dc357b7ba61dc581`；Evidence=`5321cf2099aea7aac3ad6a73`。
源码/关系 [/functional_chains/9](codepatchbay-automatic-report.json#/functional_chains/9)；缺段 [/functional_chains/9/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/9/analysis_gaps)；模型 [/functional_chains/9/trusted_models](codepatchbay-automatic-report.json#/functional_chains/9/trusted_models)；policy [/functional_chains/9/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/9/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| argument_reference_transfers/shown_items/0/argument_index | 0 | [/functional_chains/9/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/9/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/argument_value_field_or_activation_proven | false | [/functional_chains/9/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/9/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/from_role | loader | [/functional_chains/9/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/9/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/id | 608b8381774df532a4d3bf63 | [/functional_chains/9/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/9/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/kind | authenticated_role_argument_formal_source | [/functional_chains/9/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/9/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/origin | source-derived | [/functional_chains/9/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/9/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/role_call_fact_id | a475067997300eec519eeb0b | [/functional_chains/9/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/9/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/to_role | parser | [/functional_chains/9/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/9/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/argument/kind | identifier | [/functional_chains/9/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/9/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/argument/name | parsed | [/functional_chains/9/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/9/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/argument/location/file | core/workflow/probe-runner.ts | [/functional_chains/9/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/9/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/argument/location/line | 157 | [/functional_chains/9/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/9/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/argument/location/column | 36 | [/functional_chains/9/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/9/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/argument/location/end_line | 157 | [/functional_chains/9/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/9/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/argument/location/start_byte | 5785 | [/functional_chains/9/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/9/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/argument/location/end_byte | 5791 | [/functional_chains/9/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/9/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/argument/reference/declaration_id | 0c1f3849b05094747b7e1c5443e2a6f12337c1bc586043e7fe0ad1e6f2a3a5ad | [/functional_chains/9/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/9/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/argument/reference/declaration_kind | const | [/functional_chains/9/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/9/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/argument/reference/identity_complete | true | [/functional_chains/9/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/9/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/argument/reference/parameter_index | null | [/functional_chains/9/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/9/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/argument/reference/state | unique | [/functional_chains/9/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/9/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/argument/reference/binder_location/file | core/workflow/probe-runner.ts | [/functional_chains/9/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/9/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/argument/reference/binder_location/line | 156 | [/functional_chains/9/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/9/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/argument/reference/binder_location/column | 11 | [/functional_chains/9/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/9/pattern/argument_reference_transfers) |

完整关系 [/functional_chains/9/pattern](codepatchbay-automatic-report.json#/functional_chains/9/pattern)；原 source facts [/functional_chains/9/source_facts](codepatchbay-automatic-report.json#/functional_chains/9/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### unsupported probe 失败证据 · `cpb-report-unsupported-probe-evidence`

`unsupported_method_evidence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`structured_record_markers_do_not_prove_all_input_retention_or_persistence`；Finding=`93fe0ba9ad2e4a82c808c4c1`；Evidence=`3fe49942dd056088d91924e3`。
源码/关系 [/functional_chains/10](codepatchbay-automatic-report.json#/functional_chains/10)；缺段 [/functional_chains/10/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/10/analysis_gaps)；模型 [/functional_chains/10/trusted_models](codepatchbay-automatic-report.json#/functional_chains/10/trusted_models)；policy [/functional_chains/10/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/10/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| connected_true_marker_assignments/0/assignment_success_proven | false | [/functional_chains/10/pattern/connected_true_marker_assignments](codepatchbay-automatic-report.json#/functional_chains/10/pattern/connected_true_marker_assignments) |
| connected_true_marker_assignments/0/id | 3380a611842df69565f37762 | [/functional_chains/10/pattern/connected_true_marker_assignments](codepatchbay-automatic-report.json#/functional_chains/10/pattern/connected_true_marker_assignments) |
| connected_true_marker_assignments/0/kind | record_marker_assignment_attempt | [/functional_chains/10/pattern/connected_true_marker_assignments](codepatchbay-automatic-report.json#/functional_chains/10/pattern/connected_true_marker_assignments) |
| connected_true_marker_assignments/0/origin | source-derived | [/functional_chains/10/pattern/connected_true_marker_assignments](codepatchbay-automatic-report.json#/functional_chains/10/pattern/connected_true_marker_assignments) |
| connected_true_marker_assignments/0/role | plan | [/functional_chains/10/pattern/connected_true_marker_assignments](codepatchbay-automatic-report.json#/functional_chains/10/pattern/connected_true_marker_assignments) |
| connected_true_marker_assignments/0/branch_context/0/activation_proven | false | [/functional_chains/10/pattern/connected_true_marker_assignments](codepatchbay-automatic-report.json#/functional_chains/10/pattern/connected_true_marker_assignments) |
| connected_true_marker_assignments/0/branch_context/0/kind | for_in_statement | [/functional_chains/10/pattern/connected_true_marker_assignments](codepatchbay-automatic-report.json#/functional_chains/10/pattern/connected_true_marker_assignments) |
| connected_true_marker_assignments/0/branch_context/0/location/file | core/workflow/evidence-probes.ts | [/functional_chains/10/pattern/connected_true_marker_assignments](codepatchbay-automatic-report.json#/functional_chains/10/pattern/connected_true_marker_assignments) |
| connected_true_marker_assignments/0/branch_context/0/location/line | 333 | [/functional_chains/10/pattern/connected_true_marker_assignments](codepatchbay-automatic-report.json#/functional_chains/10/pattern/connected_true_marker_assignments) |
| connected_true_marker_assignments/0/branch_context/0/location/column | 3 | [/functional_chains/10/pattern/connected_true_marker_assignments](codepatchbay-automatic-report.json#/functional_chains/10/pattern/connected_true_marker_assignments) |
| connected_true_marker_assignments/0/branch_context/0/location/end_line | 366 | [/functional_chains/10/pattern/connected_true_marker_assignments](codepatchbay-automatic-report.json#/functional_chains/10/pattern/connected_true_marker_assignments) |
| connected_true_marker_assignments/0/branch_context/0/location/start_byte | 14030 | [/functional_chains/10/pattern/connected_true_marker_assignments](codepatchbay-automatic-report.json#/functional_chains/10/pattern/connected_true_marker_assignments) |
| connected_true_marker_assignments/0/branch_context/0/location/end_byte | 15461 | [/functional_chains/10/pattern/connected_true_marker_assignments](codepatchbay-automatic-report.json#/functional_chains/10/pattern/connected_true_marker_assignments) |
| connected_true_marker_assignments/0/branch_context/1/branch | then | [/functional_chains/10/pattern/connected_true_marker_assignments](codepatchbay-automatic-report.json#/functional_chains/10/pattern/connected_true_marker_assignments) |
| connected_true_marker_assignments/0/branch_context/1/condition_truth_proven | false | [/functional_chains/10/pattern/connected_true_marker_assignments](codepatchbay-automatic-report.json#/functional_chains/10/pattern/connected_true_marker_assignments) |
| connected_true_marker_assignments/0/branch_context/1/kind | if | [/functional_chains/10/pattern/connected_true_marker_assignments](codepatchbay-automatic-report.json#/functional_chains/10/pattern/connected_true_marker_assignments) |
| connected_true_marker_assignments/0/branch_context/1/condition/kind | identifier | [/functional_chains/10/pattern/connected_true_marker_assignments](codepatchbay-automatic-report.json#/functional_chains/10/pattern/connected_true_marker_assignments) |
| connected_true_marker_assignments/0/branch_context/1/condition/name | existing | [/functional_chains/10/pattern/connected_true_marker_assignments](codepatchbay-automatic-report.json#/functional_chains/10/pattern/connected_true_marker_assignments) |
| connected_true_marker_assignments/0/branch_context/1/condition/location/file | core/workflow/evidence-probes.ts | [/functional_chains/10/pattern/connected_true_marker_assignments](codepatchbay-automatic-report.json#/functional_chains/10/pattern/connected_true_marker_assignments) |
| connected_true_marker_assignments/0/branch_context/1/condition/location/line | 343 | [/functional_chains/10/pattern/connected_true_marker_assignments](codepatchbay-automatic-report.json#/functional_chains/10/pattern/connected_true_marker_assignments) |
| connected_true_marker_assignments/0/branch_context/1/condition/location/column | 9 | [/functional_chains/10/pattern/connected_true_marker_assignments](codepatchbay-automatic-report.json#/functional_chains/10/pattern/connected_true_marker_assignments) |
| connected_true_marker_assignments/0/branch_context/1/condition/location/end_line | 343 | [/functional_chains/10/pattern/connected_true_marker_assignments](codepatchbay-automatic-report.json#/functional_chains/10/pattern/connected_true_marker_assignments) |
| connected_true_marker_assignments/0/branch_context/1/condition/location/start_byte | 14490 | [/functional_chains/10/pattern/connected_true_marker_assignments](codepatchbay-automatic-report.json#/functional_chains/10/pattern/connected_true_marker_assignments) |
| connected_true_marker_assignments/0/branch_context/1/condition/location/end_byte | 14498 | [/functional_chains/10/pattern/connected_true_marker_assignments](codepatchbay-automatic-report.json#/functional_chains/10/pattern/connected_true_marker_assignments) |

完整关系 [/functional_chains/10/pattern](codepatchbay-automatic-report.json#/functional_chains/10/pattern)；原 source facts [/functional_chains/10/source_facts](codepatchbay-automatic-report.json#/functional_chains/10/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### 可信命令的字段来源 · `cpb-trusted-command-lineage`

`trusted_command_lineage`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`record_command_source_dependencies_do_not_prove_full_heap_noninterference`；Finding=`973b27bb1ecd1ee83c76eff7`；Evidence=`eb563cd58379ed6bc55f7f8a`。
源码/关系 [/functional_chains/11](codepatchbay-automatic-report.json#/functional_chains/11)；缺段 [/functional_chains/11/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/11/analysis_gaps)；模型 [/functional_chains/11/trusted_models](codepatchbay-automatic-report.json#/functional_chains/11/trusted_models)；policy [/functional_chains/11/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/11/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| all_selected_roles_bound | true | [/functional_chains/11/pattern/all_selected_roles_bound](codepatchbay-automatic-report.json#/functional_chains/11/pattern/all_selected_roles_bound) |
| assignment_attempts/command_runner/0/assignment_success_proven | false | [/functional_chains/11/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/11/pattern/assignment_attempts) |
| assignment_attempts/command_runner/0/callback_activation_proven | false | [/functional_chains/11/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/11/pattern/assignment_attempts) |
| assignment_attempts/command_runner/0/id | 024f34a548c7c81ef2db2b42 | [/functional_chains/11/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/11/pattern/assignment_attempts) |
| assignment_attempts/command_runner/0/kind | record_assignment_source_attempt | [/functional_chains/11/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/11/pattern/assignment_attempts) |
| assignment_attempts/command_runner/0/origin | source-derived | [/functional_chains/11/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/11/pattern/assignment_attempts) |
| assignment_attempts/command_runner/0/record_relations_version | captured-record-projection-relations-1 | [/functional_chains/11/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/11/pattern/assignment_attempts) |
| assignment_attempts/command_runner/0/role | command_runner | [/functional_chains/11/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/11/pattern/assignment_attempts) |
| assignment_attempts/command_runner/0/branch_context/0/activation_proven | false | [/functional_chains/11/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/11/pattern/assignment_attempts) |
| assignment_attempts/command_runner/0/branch_context/0/kind | for_statement | [/functional_chains/11/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/11/pattern/assignment_attempts) |
| assignment_attempts/command_runner/0/branch_context/0/location/file | core/workflow/probe-runner.ts | [/functional_chains/11/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/11/pattern/assignment_attempts) |
| assignment_attempts/command_runner/0/branch_context/0/location/line | 469 | [/functional_chains/11/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/11/pattern/assignment_attempts) |
| assignment_attempts/command_runner/0/branch_context/0/location/column | 3 | [/functional_chains/11/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/11/pattern/assignment_attempts) |
| assignment_attempts/command_runner/0/branch_context/0/location/end_line | 482 | [/functional_chains/11/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/11/pattern/assignment_attempts) |
| assignment_attempts/command_runner/0/branch_context/0/location/start_byte | 16526 | [/functional_chains/11/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/11/pattern/assignment_attempts) |
| assignment_attempts/command_runner/0/branch_context/0/location/end_byte | 17099 | [/functional_chains/11/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/11/pattern/assignment_attempts) |
| assignment_attempts/command_runner/0/left/kind | identifier | [/functional_chains/11/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/11/pattern/assignment_attempts) |
| assignment_attempts/command_runner/0/left/reference_dependencies_only | true | [/functional_chains/11/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/11/pattern/assignment_attempts) |
| assignment_attempts/command_runner/0/left/runtime_value_or_heap_identity_proven | false | [/functional_chains/11/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/11/pattern/assignment_attempts) |
| assignment_attempts/command_runner/0/left/source | attempt | [/functional_chains/11/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/11/pattern/assignment_attempts) |
| assignment_attempts/command_runner/0/left/source_truncated | false | [/functional_chains/11/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/11/pattern/assignment_attempts) |
| assignment_attempts/command_runner/0/left/location/file | core/workflow/probe-runner.ts | [/functional_chains/11/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/11/pattern/assignment_attempts) |
| assignment_attempts/command_runner/0/left/location/line | 469 | [/functional_chains/11/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/11/pattern/assignment_attempts) |
| assignment_attempts/command_runner/0/left/location/column | 67 | [/functional_chains/11/pattern/assignment_attempts](codepatchbay-automatic-report.json#/functional_chains/11/pattern/assignment_attempts) |

完整关系 [/functional_chains/11/pattern](codepatchbay-automatic-report.json#/functional_chains/11/pattern)；原 source facts [/functional_chains/11/source_facts](codepatchbay-automatic-report.json#/functional_chains/11/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### 未支持方法的失败记录 · `cpb-unsupported-record-retention`

`unsupported_record_retention`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`record_true_marker_does_not_prove_all_input_or_artifact_retention`；Finding=`6ab0ba74018e509d3efb265e`；Evidence=`125d0901bf7a8a5ab0762b91`。
源码/关系 [/functional_chains/12](codepatchbay-automatic-report.json#/functional_chains/12)；缺段 [/functional_chains/12/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/12/analysis_gaps)；模型 [/functional_chains/12/trusted_models](codepatchbay-automatic-report.json#/functional_chains/12/trusted_models)；policy [/functional_chains/12/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/12/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| all_selected_roles_bound | true | [/functional_chains/12/pattern/all_selected_roles_bound](codepatchbay-automatic-report.json#/functional_chains/12/pattern/all_selected_roles_bound) |
| assignment_attempts/plan/shown_items/0/assignment_success_proven | false | [/functional_chains/12/pattern/assignment_attempts/plan](codepatchbay-automatic-report.json#/functional_chains/12/pattern/assignment_attempts/plan) |
| assignment_attempts/plan/shown_items/0/callback_activation_proven | false | [/functional_chains/12/pattern/assignment_attempts/plan](codepatchbay-automatic-report.json#/functional_chains/12/pattern/assignment_attempts/plan) |
| assignment_attempts/plan/shown_items/0/id | 4404f7afb430d3b7bbc7080f | [/functional_chains/12/pattern/assignment_attempts/plan](codepatchbay-automatic-report.json#/functional_chains/12/pattern/assignment_attempts/plan) |
| assignment_attempts/plan/shown_items/0/kind | record_assignment_source_attempt | [/functional_chains/12/pattern/assignment_attempts/plan](codepatchbay-automatic-report.json#/functional_chains/12/pattern/assignment_attempts/plan) |
| assignment_attempts/plan/shown_items/0/origin | source-derived | [/functional_chains/12/pattern/assignment_attempts/plan](codepatchbay-automatic-report.json#/functional_chains/12/pattern/assignment_attempts/plan) |
| assignment_attempts/plan/shown_items/0/record_relations_version | captured-record-projection-relations-1 | [/functional_chains/12/pattern/assignment_attempts/plan](codepatchbay-automatic-report.json#/functional_chains/12/pattern/assignment_attempts/plan) |
| assignment_attempts/plan/shown_items/0/role | plan | [/functional_chains/12/pattern/assignment_attempts/plan](codepatchbay-automatic-report.json#/functional_chains/12/pattern/assignment_attempts/plan) |
| assignment_attempts/plan/shown_items/0/branch_context/0/activation_proven | false | [/functional_chains/12/pattern/assignment_attempts/plan](codepatchbay-automatic-report.json#/functional_chains/12/pattern/assignment_attempts/plan) |
| assignment_attempts/plan/shown_items/0/branch_context/0/kind | for_in_statement | [/functional_chains/12/pattern/assignment_attempts/plan](codepatchbay-automatic-report.json#/functional_chains/12/pattern/assignment_attempts/plan) |
| assignment_attempts/plan/shown_items/0/branch_context/0/location/file | core/workflow/evidence-probes.ts | [/functional_chains/12/pattern/assignment_attempts/plan](codepatchbay-automatic-report.json#/functional_chains/12/pattern/assignment_attempts/plan) |
| assignment_attempts/plan/shown_items/0/branch_context/0/location/line | 333 | [/functional_chains/12/pattern/assignment_attempts/plan](codepatchbay-automatic-report.json#/functional_chains/12/pattern/assignment_attempts/plan) |
| assignment_attempts/plan/shown_items/0/branch_context/0/location/column | 3 | [/functional_chains/12/pattern/assignment_attempts/plan](codepatchbay-automatic-report.json#/functional_chains/12/pattern/assignment_attempts/plan) |
| assignment_attempts/plan/shown_items/0/branch_context/0/location/end_line | 366 | [/functional_chains/12/pattern/assignment_attempts/plan](codepatchbay-automatic-report.json#/functional_chains/12/pattern/assignment_attempts/plan) |
| assignment_attempts/plan/shown_items/0/branch_context/0/location/start_byte | 14030 | [/functional_chains/12/pattern/assignment_attempts/plan](codepatchbay-automatic-report.json#/functional_chains/12/pattern/assignment_attempts/plan) |
| assignment_attempts/plan/shown_items/0/branch_context/0/location/end_byte | 15461 | [/functional_chains/12/pattern/assignment_attempts/plan](codepatchbay-automatic-report.json#/functional_chains/12/pattern/assignment_attempts/plan) |
| assignment_attempts/plan/shown_items/0/branch_context/1/branch | then | [/functional_chains/12/pattern/assignment_attempts/plan](codepatchbay-automatic-report.json#/functional_chains/12/pattern/assignment_attempts/plan) |
| assignment_attempts/plan/shown_items/0/branch_context/1/condition_truth_proven | false | [/functional_chains/12/pattern/assignment_attempts/plan](codepatchbay-automatic-report.json#/functional_chains/12/pattern/assignment_attempts/plan) |
| assignment_attempts/plan/shown_items/0/branch_context/1/kind | if | [/functional_chains/12/pattern/assignment_attempts/plan](codepatchbay-automatic-report.json#/functional_chains/12/pattern/assignment_attempts/plan) |
| assignment_attempts/plan/shown_items/0/branch_context/1/condition/kind | identifier | [/functional_chains/12/pattern/assignment_attempts/plan](codepatchbay-automatic-report.json#/functional_chains/12/pattern/assignment_attempts/plan) |
| assignment_attempts/plan/shown_items/0/branch_context/1/condition/name | existing | [/functional_chains/12/pattern/assignment_attempts/plan](codepatchbay-automatic-report.json#/functional_chains/12/pattern/assignment_attempts/plan) |
| assignment_attempts/plan/shown_items/0/branch_context/1/condition/location/file | core/workflow/evidence-probes.ts | [/functional_chains/12/pattern/assignment_attempts/plan](codepatchbay-automatic-report.json#/functional_chains/12/pattern/assignment_attempts/plan) |
| assignment_attempts/plan/shown_items/0/branch_context/1/condition/location/line | 343 | [/functional_chains/12/pattern/assignment_attempts/plan](codepatchbay-automatic-report.json#/functional_chains/12/pattern/assignment_attempts/plan) |
| assignment_attempts/plan/shown_items/0/branch_context/1/condition/location/column | 9 | [/functional_chains/12/pattern/assignment_attempts/plan](codepatchbay-automatic-report.json#/functional_chains/12/pattern/assignment_attempts/plan) |

完整关系 [/functional_chains/12/pattern](codepatchbay-automatic-report.json#/functional_chains/12/pattern)；原 source facts [/functional_chains/12/source_facts](codepatchbay-automatic-report.json#/functional_chains/12/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

## 未解析与未审边界

- 全文复现声明：`false`；未建模功能域不视为已覆盖：`true`。
- 局部配置评估 `10` 条；重复源选择 `0` 组，见 [/overlapping_source_selections](codepatchbay-automatic-report.json#/overlapping_source_selections)，不合计为新增覆盖。
- 保存诊断 `6`；文件缺口见 [/coverage/unparsed_files](codepatchbay-automatic-report.json#/coverage/unparsed_files)，诊断见 [/diagnostics](codepatchbay-automatic-report.json#/diagnostics)。
- 源码排除规则：`[".git",".beads",".callscope",".test-tmp","node_modules","third_party","vendor","generated","dist","dist-tests","build","coverage","tests","__tests__","fixtures","**/*.test.ts","**/*.spec.ts","**/*.test.tsx","**/*.spec.tsx"]`。
- 标准模型、正常到达和生产装配条件只按各项保存范围成立；未知字段/分派、特殊语言语义及任意并发不被摘要补齐。
- 嵌套 async/callback 的源码正文不是执行轨迹；候选方法不是已验证 runtime provider。
- 保存 target_executed=`false` / target_tests_run=`false` / target_build_run=`false` / runtime_functionality_verified=`false`。
- 上方 `#/...` 为 JSON Pointer 导航；查看器若不支持该 fragment，请在原 JSON 按指针定位。指针与 Finding/Evidence 身份应一起阅读。

## 正式保存轮次

| 轮次 | 保存状态 | 新建快照 | 相同快照 ID |
| --- | --- | --- |
| `cold` | `partial` | `true` | `7b58e73339e7ad28592c4a0bede1da0028935b30edd940419841971b354c2bfe` |
| `warm` | `partial` | `false` | `7b58e73339e7ad28592c4a0bede1da0028935b30edd940419841971b354c2bfe` |

这张表复制保存发布记录；partial 是图/解析范围状态，不能据此覆盖上方判断结论。完整记录见 [integration](codepatchbay-integration.json)。
