# CodePatchBay · 保存的自动分析摘要

此摘要只展示已保存正式报告的结果和证据导航；不重新分析、不新增评价，也不替代完整证据。
五项判断是实现追踪，不是全文报告或项目功能覆盖率。链标题只是规则 ID 的展示标签。

- 固定全文基准：[原分析报告](../astra-baseline/CODEPATCHBAY_ANALYSIS.md)；不设置重复 Astra 审批步骤。
- 完整自动报告：[Markdown](codepatchbay-automatic-report.md) / [JSON](codepatchbay-automatic-report.json)；[正式 integration](codepatchbay-integration.json)。
- 快照：`dd5d4e3cc349b57eb87d0f810a415560bfd5f6b1022a990a35190a44d0e50ebb`；状态：`partial`；报告版本：`captured-project-analysis-report-3`。
- 实现：`0.14.0` / `static-multilang-14` / `call-rules-13-architecture-explanations`。
- 源码身份：`4e07250709288887cd79ae51b5f23f0239e054bc1db40371f7e7d0609148791b`。
- 策略身份：`7dc3b17d71cc3bdd409886e636bc17268dd92ad191933b38258c83931a87e887`。
- 保存 JSON SHA256：`47d26d8b44c382cbaf80d84e0a063bfccafafd45fac137962fccdd2d28a37ad7`；integration SHA256：`14ec2da687fc96870a5b511d86bebc7ab5d262334e9f52fb3b2f3d65108f815c`。
- 保存比较范围：v13 and v14 both use full frontend/detector recomputation. New source/doc scope, models, policies and architecture explanations can change identity; no same-policy precision or performance comparison is claimed.

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
Finding=`b9d2fb17c08b2364997af404`；Evidence=`b681af29edc7822e7a2297a6`；保存 evidence 指针=`/evidence/0/details`（相对于该 Finding）。
完整 [/judgments/0](codepatchbay-automatic-report.json#/judgments/0)；条件 [/judgments/0/conditions](codepatchbay-automatic-report.json#/judgments/0/conditions)；反证 [/judgments/0/refutations](codepatchbay-automatic-report.json#/judgments/0/refutations)；缺口 [/judgments/0/necessary_gaps](codepatchbay-automatic-report.json#/judgments/0/necessary_gaps)。

### `CPB-02`

状态 `superseded` 在所选身份条件下的终态谓词结果为 `False`，权威终态集合成员关系为 `True`；消费者据此进入拒绝分支。恢复政策和权威写入保护分别保存。

derived_judgment：`{"authority_terminal_membership":true,"classification_differs":true,"kind":"conditional_terminal_classification_difference","recovery_is_required_or_authorized":false,"status":"superseded","terminal_state_can_be_illegally_mutated":false,"valid_identity_predicate_result":false}`
assessment=`scoped_static_judgment_reproduced`；complete=`true`；support=`true`。
必要义务（原状态）：`S1=supported, S2=supported, S3=supported, S4=supported, S5=supported`；必要缺口：`[]`。
Finding=`86509ebe4b1a74d001042251`；Evidence=`8b2a0ec1a0958f1288f56be1`；保存 evidence 指针=`/evidence/0/details`（相对于该 Finding）。
完整 [/judgments/1](codepatchbay-automatic-report.json#/judgments/1)；条件 [/judgments/1/conditions](codepatchbay-automatic-report.json#/judgments/1/conditions)；反证 [/judgments/1/refutations](codepatchbay-automatic-report.json#/judgments/1/refutations)；缺口 [/judgments/1/necessary_gaps](codepatchbay-automatic-report.json#/judgments/1/necessary_gaps)。

### `CPB-03`

预查与权威写入的去重口径不同；从实际保护区和状态转换生成的有限交错可产生重复非终态记录，同时保存可以复用的顺序和失败条件。

derived_judgment：`"Two same-project/key/description default submissions can both observe no row; the first protected insert can be guardedly scheduled before the second protected check; the pending-only inner check then inserts a second nonterminal row"`
assessment=`scoped_static_judgment_reproduced`；complete=`true`；support=`true`。
必要义务（原状态）：`A1=supported, A2=supported, A3=supported, A4=supported, A5=supported, A6=supported, A7=supported`；必要缺口：`[]`。
Finding=`dabb6bfcc8ed51ec9b68286b`；Evidence=`ea76985490c9ee433a943733`；保存 evidence 指针=`/evidence/0/details`（相对于该 Finding）。
完整 [/judgments/2](codepatchbay-automatic-report.json#/judgments/2)；条件 [/judgments/2/conditions](codepatchbay-automatic-report.json#/judgments/2/conditions)；反证 [/judgments/2/refutations](codepatchbay-automatic-report.json#/judgments/2/refutations)；缺口 [/judgments/2/necessary_gaps](codepatchbay-automatic-report.json#/judgments/2/necessary_gaps)。

## 所选主要源码链

显示每条保存规则的实际 assessment 和缺口；source-structure 支持与目标分派闭合分开。

### CodePatchBay 记录与资源写者 · `cpb-captured-record-resource-writers`

`resource_writer_ownership`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`13d443da928da60f312c04a3`；Evidence=`729def0a562d78db0dbecdca`。
源码/关系 [/functional_chains/0](codepatchbay-automatic-report.json#/functional_chains/0)；缺段 [/functional_chains/0/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/0/analysis_gaps)；模型 [/functional_chains/0/trusted_models](codepatchbay-automatic-report.json#/functional_chains/0/trusted_models)；policy [/functional_chains/0/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/0/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

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

### 事件提交与索引投影 · `cpb-event-index-projection`

`event_index_projection`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`record_projection_physical_commit_and_all_recovery_not_proven`；Finding=`62730b11397229db7b001ed9`；Evidence=`a0a575907cc48107377253eb`。
源码/关系 [/functional_chains/1](codepatchbay-automatic-report.json#/functional_chains/1)；缺段 [/functional_chains/1/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/1/analysis_gaps)；模型 [/functional_chains/1/trusted_models](codepatchbay-automatic-report.json#/functional_chains/1/trusted_models)；policy [/functional_chains/1/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/1/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

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

### 发布模式、权限与外写边界 · `cpb-finalizer-conditional-publication`

`conditional_publication_boundary`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`68ccc02ac3ab4a201dea8e9a`；Evidence=`9e70fd31cebc00879b453793`。
源码/关系 [/functional_chains/2](codepatchbay-automatic-report.json#/functional_chains/2)；缺段 [/functional_chains/2/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/2/analysis_gaps)；模型 [/functional_chains/2/trusted_models](codepatchbay-automatic-report.json#/functional_chains/2/trusted_models)；policy [/functional_chains/2/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/2/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

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

### 访问审计与响应字段 · `cpb-report-access-audit-response`

`conditional_gate_relations`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`a6809cb5f80cad425b325b5e`；Evidence=`82a569001adfe75deb59161c`。
源码/关系 [/functional_chains/3](codepatchbay-automatic-report.json#/functional_chains/3)；缺段 [/functional_chains/3/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/3/analysis_gaps)；模型 [/functional_chains/3/trusted_models](codepatchbay-automatic-report.json#/functional_chains/3/trusted_models)；policy [/functional_chains/3/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/3/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

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

### agent allowlist / env / sandbox 策略 · `cpb-report-agent-execution-policy`

`agent_execution_policy`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`d9034e67dd88277d6e056b0a`；Evidence=`cffc82566f20dfe6838bee71`。
源码/关系 [/functional_chains/4](codepatchbay-automatic-report.json#/functional_chains/4)；缺段 [/functional_chains/4/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/4/analysis_gaps)；模型 [/functional_chains/4/trusted_models](codepatchbay-automatic-report.json#/functional_chains/4/trusted_models)；policy [/functional_chains/4/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/4/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/4/pattern/scoped_source_supported](codepatchbay-automatic-report.json#/functional_chains/4/pattern/scoped_source_supported) |
| source_derived_conditions_and_counterexamples/allowed_agents_null_and_empty_denial_distinct | true | [/functional_chains/4/pattern/source_derived_conditions_and_counterexamples](codepatchbay-automatic-report.json#/functional_chains/4/pattern/source_derived_conditions_and_counterexamples) |
| source_derived_conditions_and_counterexamples/external_agent_audit_file_and_provider_capability_are_not_execution_evidence | true | [/functional_chains/4/pattern/source_derived_conditions_and_counterexamples](codepatchbay-automatic-report.json#/functional_chains/4/pattern/source_derived_conditions_and_counterexamples) |
| source_derived_conditions_and_counterexamples/native_none_off_custom_platform_policy_branches_retained | true | [/functional_chains/4/pattern/source_derived_conditions_and_counterexamples](codepatchbay-automatic-report.json#/functional_chains/4/pattern/source_derived_conditions_and_counterexamples) |
| source_derived_conditions_and_counterexamples/provider_credentials_explicit_allow_keys_and_postfilter_writes_retained | true | [/functional_chains/4/pattern/source_derived_conditions_and_counterexamples](codepatchbay-automatic-report.json#/functional_chains/4/pattern/source_derived_conditions_and_counterexamples) |
| admission_and_postexecution_review/supported | true | [/functional_chains/4/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/4/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/admission_fact_id | 6b0bc21d40a8def9175769da | [/functional_chains/4/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/4/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/result_binding_source/state | unique | [/functional_chains/4/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/4/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/result_binding_source/binder_location/file | core/agents/agent-runner.ts | [/functional_chains/4/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/4/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/result_binding_source/binder_location/line | 527 | [/functional_chains/4/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/4/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/result_binding_source/binder_location/column | 11 | [/functional_chains/4/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/4/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/result_binding_source/binder_location/end_line | 527 | [/functional_chains/4/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/4/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/result_binding_source/binder_location/start_byte | 18355 | [/functional_chains/4/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/4/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/result_binding_source/binder_location/end_byte | 18365 | [/functional_chains/4/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/4/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/result_binding_source/declaration_kind | const | [/functional_chains/4/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/4/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/result_binding_source/declaration_location/file | core/agents/agent-runner.ts | [/functional_chains/4/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/4/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/result_binding_source/declaration_location/line | 527 | [/functional_chains/4/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/4/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/result_binding_source/declaration_location/column | 11 | [/functional_chains/4/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/4/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/result_binding_source/declaration_location/end_line | 545 | [/functional_chains/4/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/4/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/result_binding_source/declaration_location/start_byte | 18355 | [/functional_chains/4/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/4/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/result_binding_source/declaration_location/end_byte | 19054 | [/functional_chains/4/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/4/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/result_binding_source/identity_complete | true | [/functional_chains/4/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/4/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/actual_callee_graph_node_id | null | [/functional_chains/4/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/4/pattern/admission_and_postexecution_review) |
| admission_and_postexecution_review/execute_binding/arguments/0/kind | identifier | [/functional_chains/4/pattern/admission_and_postexecution_review](codepatchbay-automatic-report.json#/functional_chains/4/pattern/admission_and_postexecution_review) |

完整关系 [/functional_chains/4/pattern](codepatchbay-automatic-report.json#/functional_chains/4/pattern)；原 source facts [/functional_chains/4/source_facts](codepatchbay-automatic-report.json#/functional_chains/4/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### 完成门条件与豁免 · `cpb-report-completion-gate-conditions`

`conditional_gate_relations`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`57b7965ae2fe48439796004c`；Evidence=`df28732a9d2ed46aa5fd72df`。
源码/关系 [/functional_chains/5](codepatchbay-automatic-report.json#/functional_chains/5)；缺段 [/functional_chains/5/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/5/analysis_gaps)；模型 [/functional_chains/5/trusted_models](codepatchbay-automatic-report.json#/functional_chains/5/trusted_models)；policy [/functional_chains/5/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/5/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

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

### finalizer → 结果写入 → reconcile · `cpb-report-conditional-delivery-result`

`conditional_delivery_result`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`6be872753a6f9135c0269bad`；Evidence=`b8219ea169ef44f8b2d4dc74`。
源码/关系 [/functional_chains/6](codepatchbay-automatic-report.json#/functional_chains/6)；缺段 [/functional_chains/6/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/6/analysis_gaps)；模型 [/functional_chains/6/trusted_models](codepatchbay-automatic-report.json#/functional_chains/6/trusted_models)；policy [/functional_chains/6/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/6/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| interpretation | The captured normal source chain separates execution, terminal delivery and queue projection; external I/O and provider outcomes remain conditional. | [/functional_chains/6/pattern/interpretation](codepatchbay-automatic-report.json#/functional_chains/6/pattern/interpretation) |
| scoped_source_supported | true | [/functional_chains/6/pattern/scoped_source_supported](codepatchbay-automatic-report.json#/functional_chains/6/pattern/scoped_source_supported) |
| source_delivery_result | deferred result publication subject to cleanup/retention/fence and created-or-equal-readback branches | [/functional_chains/6/pattern/source_delivery_result](codepatchbay-automatic-report.json#/functional_chains/6/pattern/source_delivery_result) |
| source_execution_result | original execution result or finalizer-failure construction, selected by extracted conditional formula | [/functional_chains/6/pattern/source_execution_result](codepatchbay-automatic-report.json#/functional_chains/6/pattern/source_execution_result) |
| source_projection_result | current attempt, finalizer contract, mode readback, journal and recovery conditions before queue projection | [/functional_chains/6/pattern/source_projection_result](codepatchbay-automatic-report.json#/functional_chains/6/pattern/source_projection_result) |
| all_function_paths_or_hidden_effects_proven | false | [/functional_chains/6/pattern/all_function_paths_or_hidden_effects_proven](codepatchbay-automatic-report.json#/functional_chains/6/pattern/all_function_paths_or_hidden_effects_proven) |
| all_recovery_complete_proven | false | [/functional_chains/6/pattern/all_recovery_complete_proven](codepatchbay-automatic-report.json#/functional_chains/6/pattern/all_recovery_complete_proven) |
| components/finalizer/supported | true | [/functional_chains/6/pattern/components](codepatchbay-automatic-report.json#/functional_chains/6/pattern/components) |
| components/finalizer/conditional_finalization/0/supported | true | [/functional_chains/6/pattern/components](codepatchbay-automatic-report.json#/functional_chains/6/pattern/components) |
| components/finalizer/conditional_finalization/0/fact/truth_table/shown_items/0/persisted_result_source | execution_result | [/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table](codepatchbay-automatic-report.json#/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table) |
| components/finalizer/conditional_finalization/0/fact/truth_table/shown_items/0/auto_finalize_enabled | false | [/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table](codepatchbay-automatic-report.json#/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table) |
| components/finalizer/conditional_finalization/0/fact/truth_table/shown_items/0/execution_success_status | false | [/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table](codepatchbay-automatic-report.json#/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table) |
| components/finalizer/conditional_finalization/0/fact/truth_table/shown_items/0/finalization_ok | true | [/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table](codepatchbay-automatic-report.json#/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table) |
| components/finalizer/conditional_finalization/0/fact/truth_table/shown_items/0/finalization_required | false | [/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table](codepatchbay-automatic-report.json#/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table) |
| components/finalizer/conditional_finalization/0/fact/truth_table/shown_items/0/finalizer_ok | false | [/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table](codepatchbay-automatic-report.json#/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table) |
| components/finalizer/conditional_finalization/0/fact/truth_table/shown_items/1/persisted_result_source | execution_result | [/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table](codepatchbay-automatic-report.json#/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table) |
| components/finalizer/conditional_finalization/0/fact/truth_table/shown_items/1/auto_finalize_enabled | false | [/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table](codepatchbay-automatic-report.json#/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table) |
| components/finalizer/conditional_finalization/0/fact/truth_table/shown_items/1/execution_success_status | false | [/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table](codepatchbay-automatic-report.json#/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table) |
| components/finalizer/conditional_finalization/0/fact/truth_table/shown_items/1/finalization_ok | true | [/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table](codepatchbay-automatic-report.json#/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table) |
| components/finalizer/conditional_finalization/0/fact/truth_table/shown_items/1/finalization_required | false | [/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table](codepatchbay-automatic-report.json#/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table) |
| components/finalizer/conditional_finalization/0/fact/truth_table/shown_items/1/finalizer_ok | true | [/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table](codepatchbay-automatic-report.json#/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table) |
| components/finalizer/conditional_finalization/0/fact/truth_table/shown_items/2/persisted_result_source | execution_result | [/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table](codepatchbay-automatic-report.json#/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table) |
| components/finalizer/conditional_finalization/0/fact/truth_table/shown_items/2/auto_finalize_enabled | false | [/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table](codepatchbay-automatic-report.json#/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table) |
| components/finalizer/conditional_finalization/0/fact/truth_table/shown_items/2/execution_success_status | true | [/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table](codepatchbay-automatic-report.json#/functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/truth_table) |

完整关系 [/functional_chains/6/pattern](codepatchbay-automatic-report.json#/functional_chains/6/pattern)；原 source facts [/functional_chains/6/source_facts](codepatchbay-automatic-report.json#/functional_chains/6/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### runJob 主链与前置阻断 · `cpb-report-engine-stage-chain`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`64cc21afc98bd5e621642d14`；Evidence=`d08604e4528faaf285470779`。
源码/关系 [/functional_chains/7](codepatchbay-automatic-report.json#/functional_chains/7)；缺段 [/functional_chains/7/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/7/analysis_gaps)；模型 [/functional_chains/7/trusted_models](codepatchbay-automatic-report.json#/functional_chains/7/trusted_models)；policy [/functional_chains/7/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/7/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/7/pattern/scoped_source_supported](codepatchbay-automatic-report.json#/functional_chains/7/pattern/scoped_source_supported) |
| sequences/entry/conditions/0/condition/kind | unary_expression | [/functional_chains/7/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/7/pattern/sequences) |
| sequences/entry/conditions/0/condition/location/file | core/engine/run-job.ts | [/functional_chains/7/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/7/pattern/sequences) |
| sequences/entry/conditions/0/condition/location/line | 66 | [/functional_chains/7/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/7/pattern/sequences) |
| sequences/entry/conditions/0/condition/location/column | 7 | [/functional_chains/7/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/7/pattern/sequences) |
| sequences/entry/conditions/0/condition/location/end_line | 66 | [/functional_chains/7/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/7/pattern/sequences) |
| sequences/entry/conditions/0/condition/location/start_byte | 2472 | [/functional_chains/7/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/7/pattern/sequences) |
| sequences/entry/conditions/0/condition/location/end_byte | 2491 | [/functional_chains/7/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/7/pattern/sequences) |
| sequences/entry/conditions/0/condition/operands/0/call_effects_or_result_proven | false | [/functional_chains/7/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/7/pattern/sequences) |
| sequences/entry/conditions/0/condition/operands/0/arguments/0/kind | 显示投影省略 | [/functional_chains/7/pattern/sequences/entry/conditions/0/condition/operands/0/arguments/0/kind](codepatchbay-automatic-report.json#/functional_chains/7/pattern/sequences/entry/conditions/0/condition/operands/0/arguments/0/kind) |
| sequences/entry/conditions/0/condition/operands/0/arguments/0/location | 显示投影省略 | [/functional_chains/7/pattern/sequences/entry/conditions/0/condition/operands/0/arguments/0/location](codepatchbay-automatic-report.json#/functional_chains/7/pattern/sequences/entry/conditions/0/condition/operands/0/arguments/0/location) |
| sequences/entry/conditions/0/condition/operands/0/arguments/0/name | 显示投影省略 | [/functional_chains/7/pattern/sequences/entry/conditions/0/condition/operands/0/arguments/0/name](codepatchbay-automatic-report.json#/functional_chains/7/pattern/sequences/entry/conditions/0/condition/operands/0/arguments/0/name) |
| sequences/entry/conditions/0/condition/operands/0/callee_expression/kind | identifier | [/functional_chains/7/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/7/pattern/sequences) |
| sequences/entry/conditions/0/condition/operands/0/callee_expression/location/file | core/engine/run-job.ts | [/functional_chains/7/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/7/pattern/sequences) |
| sequences/entry/conditions/0/condition/operands/0/callee_expression/location/line | 66 | [/functional_chains/7/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/7/pattern/sequences) |
| sequences/entry/conditions/0/condition/operands/0/callee_expression/location/column | 8 | [/functional_chains/7/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/7/pattern/sequences) |
| sequences/entry/conditions/0/condition/operands/0/callee_expression/location/end_line | 66 | [/functional_chains/7/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/7/pattern/sequences) |
| sequences/entry/conditions/0/condition/operands/0/callee_expression/location/start_byte | 2473 | [/functional_chains/7/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/7/pattern/sequences) |
| sequences/entry/conditions/0/condition/operands/0/callee_expression/location/end_byte | 2481 | [/functional_chains/7/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/7/pattern/sequences) |
| sequences/entry/conditions/0/condition/operands/0/callee_expression/name | isRecord | [/functional_chains/7/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/7/pattern/sequences) |
| sequences/entry/conditions/0/condition/operands/0/callee_source | isRecord | [/functional_chains/7/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/7/pattern/sequences) |
| sequences/entry/conditions/0/condition/operands/0/kind | call_expression | [/functional_chains/7/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/7/pattern/sequences) |
| sequences/entry/conditions/0/condition/operands/0/location/file | core/engine/run-job.ts | [/functional_chains/7/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/7/pattern/sequences) |
| sequences/entry/conditions/0/condition/operands/0/location/line | 66 | [/functional_chains/7/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/7/pattern/sequences) |

完整关系 [/functional_chains/7/pattern](codepatchbay-automatic-report.json#/functional_chains/7/pattern)；原 source facts [/functional_chains/7/source_facts](codepatchbay-automatic-report.json#/functional_chains/7/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### audit best-effort 分支 · `cpb-report-job-audit-best-effort`

`best_effort_finalization`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`7ba0e642e5f36b5bef03a2ea`；Evidence=`8ee578da5ec41492dbb9d755`。
源码/关系 [/functional_chains/8](codepatchbay-automatic-report.json#/functional_chains/8)；缺段 [/functional_chains/8/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/8/analysis_gaps)；模型 [/functional_chains/8/trusted_models](codepatchbay-automatic-report.json#/functional_chains/8/trusted_models)；policy [/functional_chains/8/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/8/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/8/pattern/scoped_source_supported](codepatchbay-automatic-report.json#/functional_chains/8/pattern/scoped_source_supported) |
| audit_subject_equivalence_to_other_systems_proven | false | [/functional_chains/8/pattern/audit_subject_equivalence_to_other_systems_proven](codepatchbay-automatic-report.json#/functional_chains/8/pattern/audit_subject_equivalence_to_other_systems_proven) |
| caught_scopes/0/call_ids/0 | 6968b0efeca2789e41208506 | [/functional_chains/8/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/8/pattern/caught_scopes) |
| caught_scopes/0/call_ids/1 | 516fbd5e3e838e5fe08990e7 | [/functional_chains/8/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/8/pattern/caught_scopes) |
| caught_scopes/0/catch_body_location/file | core/engine/run-job.ts | [/functional_chains/8/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/8/pattern/caught_scopes) |
| caught_scopes/0/catch_body_location/line | 91 | [/functional_chains/8/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/8/pattern/caught_scopes) |
| caught_scopes/0/catch_body_location/column | 19 | [/functional_chains/8/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/8/pattern/caught_scopes) |
| caught_scopes/0/catch_body_location/end_line | 106 | [/functional_chains/8/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/8/pattern/caught_scopes) |
| caught_scopes/0/catch_body_location/start_byte | 3562 | [/functional_chains/8/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/8/pattern/caught_scopes) |
| caught_scopes/0/catch_body_location/end_byte | 4118 | [/functional_chains/8/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/8/pattern/caught_scopes) |
| caught_scopes/0/catch_location/file | core/engine/run-job.ts | [/functional_chains/8/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/8/pattern/caught_scopes) |
| caught_scopes/0/catch_location/line | 91 | [/functional_chains/8/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/8/pattern/caught_scopes) |
| caught_scopes/0/catch_location/column | 5 | [/functional_chains/8/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/8/pattern/caught_scopes) |
| caught_scopes/0/catch_location/end_line | 106 | [/functional_chains/8/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/8/pattern/caught_scopes) |
| caught_scopes/0/catch_location/start_byte | 3548 | [/functional_chains/8/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/8/pattern/caught_scopes) |
| caught_scopes/0/catch_location/end_byte | 4118 | [/functional_chains/8/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/8/pattern/caught_scopes) |
| caught_scopes/0/failure_swallowed_by_empty_catch_source | false | [/functional_chains/8/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/8/pattern/caught_scopes) |
| caught_scopes/0/finally_present | false | [/functional_chains/8/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/8/pattern/caught_scopes) |
| caught_scopes/0/kind | caught_call_failure_scope | [/functional_chains/8/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/8/pattern/caught_scopes) |
| caught_scopes/0/location/file | core/engine/run-job.ts | [/functional_chains/8/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/8/pattern/caught_scopes) |
| caught_scopes/0/location/line | 74 | [/functional_chains/8/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/8/pattern/caught_scopes) |
| caught_scopes/0/location/column | 3 | [/functional_chains/8/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/8/pattern/caught_scopes) |
| caught_scopes/0/location/end_line | 106 | [/functional_chains/8/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/8/pattern/caught_scopes) |
| caught_scopes/0/location/start_byte | 2848 | [/functional_chains/8/pattern/caught_scopes](codepatchbay-automatic-report.json#/functional_chains/8/pattern/caught_scopes) |

完整关系 [/functional_chains/8/pattern](codepatchbay-automatic-report.json#/functional_chains/8/pattern)；原 source facts [/functional_chains/8/source_facts](codepatchbay-automatic-report.json#/functional_chains/8/source_facts)。原投影截取标志 `false`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### readiness 提交前保护 · `cpb-report-readiness-abrupt-guard`

`conditional_gate_relations`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`dbdf085022aed24e7f0f4607`；Evidence=`052f8833f6c10d2b78d7fba0`。
源码/关系 [/functional_chains/9](codepatchbay-automatic-report.json#/functional_chains/9)；缺段 [/functional_chains/9/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/9/analysis_gaps)；模型 [/functional_chains/9/trusted_models](codepatchbay-automatic-report.json#/functional_chains/9/trusted_models)；policy [/functional_chains/9/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/9/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

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

### trusted probe 命令来源 · `cpb-report-trusted-probe-command-source`

`structured_command_source`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`structured_command_intermediate_values_and_external_effects_not_fully_proven`；Finding=`65cd294919771816fe7c8dc6`；Evidence=`1e94fcfc31c8ae130e7eb25a`。
源码/关系 [/functional_chains/10](codepatchbay-automatic-report.json#/functional_chains/10)；缺段 [/functional_chains/10/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/10/analysis_gaps)；模型 [/functional_chains/10/trusted_models](codepatchbay-automatic-report.json#/functional_chains/10/trusted_models)；policy [/functional_chains/10/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/10/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/10/pattern/scoped_source_supported](codepatchbay-automatic-report.json#/functional_chains/10/pattern/scoped_source_supported) |
| argument_reference_transfers/shown_items/0/argument/kind | identifier | [/functional_chains/10/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/10/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/argument/location/file | core/workflow/probe-runner.ts | [/functional_chains/10/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/10/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/argument/location/line | 157 | [/functional_chains/10/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/10/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/argument/location/column | 36 | [/functional_chains/10/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/10/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/argument/location/end_line | 157 | [/functional_chains/10/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/10/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/argument/location/start_byte | 5785 | [/functional_chains/10/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/10/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/argument/location/end_byte | 5791 | [/functional_chains/10/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/10/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/argument/name | parsed | [/functional_chains/10/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/10/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/argument_value_field_or_activation_proven | false | [/functional_chains/10/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/10/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/formal/state | unique | [/functional_chains/10/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/10/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/formal/binder_location/file | core/workflow/trusted-probe-policy.ts | [/functional_chains/10/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/10/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/formal/binder_location/line | 34 | [/functional_chains/10/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/10/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/formal/binder_location/column | 41 | [/functional_chains/10/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/10/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/formal/binder_location/end_line | 34 | [/functional_chains/10/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/10/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/formal/binder_location/start_byte | 1306 | [/functional_chains/10/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/10/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/formal/binder_location/end_byte | 1311 | [/functional_chains/10/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/10/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/formal/declaration_kind | parameter | [/functional_chains/10/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/10/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/formal/declaration_location/file | core/workflow/trusted-probe-policy.ts | [/functional_chains/10/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/10/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/formal/declaration_location/line | 34 | [/functional_chains/10/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/10/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/formal/declaration_location/column | 40 | [/functional_chains/10/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/10/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/formal/declaration_location/end_line | 34 | [/functional_chains/10/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/10/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/formal/declaration_location/start_byte | 1305 | [/functional_chains/10/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/10/pattern/argument_reference_transfers) |
| argument_reference_transfers/shown_items/0/formal/declaration_location/end_byte | 1321 | [/functional_chains/10/pattern/argument_reference_transfers](codepatchbay-automatic-report.json#/functional_chains/10/pattern/argument_reference_transfers) |

完整关系 [/functional_chains/10/pattern](codepatchbay-automatic-report.json#/functional_chains/10/pattern)；原 source facts [/functional_chains/10/source_facts](codepatchbay-automatic-report.json#/functional_chains/10/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### unsupported probe 失败证据 · `cpb-report-unsupported-probe-evidence`

`unsupported_method_evidence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`structured_record_markers_do_not_prove_all_input_retention_or_persistence`；Finding=`b577b30117078aaecea00767`；Evidence=`07fadddb4f3766f3f08a6f14`。
源码/关系 [/functional_chains/11](codepatchbay-automatic-report.json#/functional_chains/11)；缺段 [/functional_chains/11/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/11/analysis_gaps)；模型 [/functional_chains/11/trusted_models](codepatchbay-automatic-report.json#/functional_chains/11/trusted_models)；policy [/functional_chains/11/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/11/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/11/pattern/scoped_source_supported](codepatchbay-automatic-report.json#/functional_chains/11/pattern/scoped_source_supported) |
| marker_consumption_guard_sources/shown_items/0/condition/kind | binary_expression | [/functional_chains/11/pattern/marker_consumption_guard_sources](codepatchbay-automatic-report.json#/functional_chains/11/pattern/marker_consumption_guard_sources) |
| marker_consumption_guard_sources/shown_items/0/condition/location/file | core/workflow/probe-runner.ts | [/functional_chains/11/pattern/marker_consumption_guard_sources](codepatchbay-automatic-report.json#/functional_chains/11/pattern/marker_consumption_guard_sources) |
| marker_consumption_guard_sources/shown_items/0/condition/location/line | 592 | [/functional_chains/11/pattern/marker_consumption_guard_sources](codepatchbay-automatic-report.json#/functional_chains/11/pattern/marker_consumption_guard_sources) |
| marker_consumption_guard_sources/shown_items/0/condition/location/column | 7 | [/functional_chains/11/pattern/marker_consumption_guard_sources](codepatchbay-automatic-report.json#/functional_chains/11/pattern/marker_consumption_guard_sources) |
| marker_consumption_guard_sources/shown_items/0/condition/location/end_line | 592 | [/functional_chains/11/pattern/marker_consumption_guard_sources](codepatchbay-automatic-report.json#/functional_chains/11/pattern/marker_consumption_guard_sources) |
| marker_consumption_guard_sources/shown_items/0/condition/location/start_byte | 20972 | [/functional_chains/11/pattern/marker_consumption_guard_sources](codepatchbay-automatic-report.json#/functional_chains/11/pattern/marker_consumption_guard_sources) |
| marker_consumption_guard_sources/shown_items/0/condition/location/end_byte | 21037 | [/functional_chains/11/pattern/marker_consumption_guard_sources](codepatchbay-automatic-report.json#/functional_chains/11/pattern/marker_consumption_guard_sources) |
| marker_consumption_guard_sources/shown_items/0/condition/operands/0/kind | unary_expression | [/functional_chains/11/pattern/marker_consumption_guard_sources](codepatchbay-automatic-report.json#/functional_chains/11/pattern/marker_consumption_guard_sources) |
| marker_consumption_guard_sources/shown_items/0/condition/operands/0/location/file | core/workflow/probe-runner.ts | [/functional_chains/11/pattern/marker_consumption_guard_sources](codepatchbay-automatic-report.json#/functional_chains/11/pattern/marker_consumption_guard_sources) |
| marker_consumption_guard_sources/shown_items/0/condition/operands/0/location/line | 592 | [/functional_chains/11/pattern/marker_consumption_guard_sources](codepatchbay-automatic-report.json#/functional_chains/11/pattern/marker_consumption_guard_sources) |
| marker_consumption_guard_sources/shown_items/0/condition/operands/0/location/column | 7 | [/functional_chains/11/pattern/marker_consumption_guard_sources](codepatchbay-automatic-report.json#/functional_chains/11/pattern/marker_consumption_guard_sources) |
| marker_consumption_guard_sources/shown_items/0/condition/operands/0/location/end_line | 592 | [/functional_chains/11/pattern/marker_consumption_guard_sources](codepatchbay-automatic-report.json#/functional_chains/11/pattern/marker_consumption_guard_sources) |
| marker_consumption_guard_sources/shown_items/0/condition/operands/0/location/start_byte | 20972 | [/functional_chains/11/pattern/marker_consumption_guard_sources](codepatchbay-automatic-report.json#/functional_chains/11/pattern/marker_consumption_guard_sources) |
| marker_consumption_guard_sources/shown_items/0/condition/operands/0/location/end_byte | 20992 | [/functional_chains/11/pattern/marker_consumption_guard_sources](codepatchbay-automatic-report.json#/functional_chains/11/pattern/marker_consumption_guard_sources) |
| marker_consumption_guard_sources/shown_items/0/condition/operands/0/operands/0/kind | identifier | [/functional_chains/11/pattern/marker_consumption_guard_sources](codepatchbay-automatic-report.json#/functional_chains/11/pattern/marker_consumption_guard_sources) |
| marker_consumption_guard_sources/shown_items/0/condition/operands/0/operands/0/location/file | core/workflow/probe-runner.ts | [/functional_chains/11/pattern/marker_consumption_guard_sources](codepatchbay-automatic-report.json#/functional_chains/11/pattern/marker_consumption_guard_sources) |
| marker_consumption_guard_sources/shown_items/0/condition/operands/0/operands/0/location/line | 592 | [/functional_chains/11/pattern/marker_consumption_guard_sources](codepatchbay-automatic-report.json#/functional_chains/11/pattern/marker_consumption_guard_sources) |
| marker_consumption_guard_sources/shown_items/0/condition/operands/0/operands/0/location/column | 8 | [/functional_chains/11/pattern/marker_consumption_guard_sources](codepatchbay-automatic-report.json#/functional_chains/11/pattern/marker_consumption_guard_sources) |
| marker_consumption_guard_sources/shown_items/0/condition/operands/0/operands/0/location/end_line | 592 | [/functional_chains/11/pattern/marker_consumption_guard_sources](codepatchbay-automatic-report.json#/functional_chains/11/pattern/marker_consumption_guard_sources) |
| marker_consumption_guard_sources/shown_items/0/condition/operands/0/operands/0/location/start_byte | 20973 | [/functional_chains/11/pattern/marker_consumption_guard_sources](codepatchbay-automatic-report.json#/functional_chains/11/pattern/marker_consumption_guard_sources) |
| marker_consumption_guard_sources/shown_items/0/condition/operands/0/operands/0/location/end_byte | 20992 | [/functional_chains/11/pattern/marker_consumption_guard_sources](codepatchbay-automatic-report.json#/functional_chains/11/pattern/marker_consumption_guard_sources) |
| marker_consumption_guard_sources/shown_items/0/condition/operands/0/operands/0/name | acceptanceChecklist | [/functional_chains/11/pattern/marker_consumption_guard_sources](codepatchbay-automatic-report.json#/functional_chains/11/pattern/marker_consumption_guard_sources) |
| marker_consumption_guard_sources/shown_items/0/condition/operands/0/operator | ! | [/functional_chains/11/pattern/marker_consumption_guard_sources](codepatchbay-automatic-report.json#/functional_chains/11/pattern/marker_consumption_guard_sources) |

完整关系 [/functional_chains/11/pattern](codepatchbay-automatic-report.json#/functional_chains/11/pattern)；原 source facts [/functional_chains/11/source_facts](codepatchbay-automatic-report.json#/functional_chains/11/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### FIXED 分支的替代事件与后续任务 · `cpb-review-fixed-state-lineage`

`conditional_state_lineage`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`4837c30b914f63f70f03ca34`；Evidence=`91922b21c002a4d21084a1d8`。
源码/关系 [/functional_chains/12](codepatchbay-automatic-report.json#/functional_chains/12)；缺段 [/functional_chains/12/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/12/analysis_gaps)；模型 [/functional_chains/12/trusted_models](codepatchbay-automatic-report.json#/functional_chains/12/trusted_models)；policy [/functional_chains/12/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/12/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

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

### cpb-task-read-projection · `cpb-task-read-projection`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`b9f0bd2b67503d6e15c41d4f`；Evidence=`dff8cf1bca15b50c8faf74e0`。
源码/关系 [/functional_chains/13](codepatchbay-automatic-report.json#/functional_chains/13)；缺段 [/functional_chains/13/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/13/analysis_gaps)；模型 [/functional_chains/13/trusted_models](codepatchbay-automatic-report.json#/functional_chains/13/trusted_models)；policy [/functional_chains/13/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/13/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/13/pattern/scoped_source_supported](codepatchbay-automatic-report.json#/functional_chains/13/pattern/scoped_source_supported) |
| sequences/linked_record_lookup/conditions/0/condition/kind | unary_expression | [/functional_chains/13/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/linked_record_lookup/conditions/0/condition/location/file | server/services/job/job-store.ts | [/functional_chains/13/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/linked_record_lookup/conditions/0/condition/location/line | 1375 | [/functional_chains/13/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/linked_record_lookup/conditions/0/condition/location/column | 7 | [/functional_chains/13/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/linked_record_lookup/conditions/0/condition/location/end_line | 1375 | [/functional_chains/13/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/linked_record_lookup/conditions/0/condition/location/start_byte | 46225 | [/functional_chains/13/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/linked_record_lookup/conditions/0/condition/location/end_byte | 46238 | [/functional_chains/13/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/linked_record_lookup/conditions/0/condition/operands/0/kind | identifier | [/functional_chains/13/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/linked_record_lookup/conditions/0/condition/operands/0/location/file | server/services/job/job-store.ts | [/functional_chains/13/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/linked_record_lookup/conditions/0/condition/operands/0/location/line | 1375 | [/functional_chains/13/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/linked_record_lookup/conditions/0/condition/operands/0/location/column | 8 | [/functional_chains/13/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/linked_record_lookup/conditions/0/condition/operands/0/location/end_line | 1375 | [/functional_chains/13/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/linked_record_lookup/conditions/0/condition/operands/0/location/start_byte | 46226 | [/functional_chains/13/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/linked_record_lookup/conditions/0/condition/operands/0/location/end_byte | 46238 | [/functional_chains/13/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/linked_record_lookup/conditions/0/condition/operands/0/name | queueEntryId | [/functional_chains/13/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/linked_record_lookup/conditions/0/condition/operator | ! | [/functional_chains/13/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/linked_record_lookup/conditions/0/condition/runtime_predicate_or_assignment_proven | false | [/functional_chains/13/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/linked_record_lookup/conditions/0/branches/0/abrupt_source_expressions/0/kind | return_statement | [/functional_chains/13/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/linked_record_lookup/conditions/0/branches/0/abrupt_source_expressions/0/location/file | server/services/job/job-store.ts | [/functional_chains/13/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/linked_record_lookup/conditions/0/branches/0/abrupt_source_expressions/0/location/line | 1375 | [/functional_chains/13/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/linked_record_lookup/conditions/0/branches/0/abrupt_source_expressions/0/location/column | 22 | [/functional_chains/13/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/linked_record_lookup/conditions/0/branches/0/abrupt_source_expressions/0/location/end_line | 1375 | [/functional_chains/13/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/linked_record_lookup/conditions/0/branches/0/abrupt_source_expressions/0/location/start_byte | 46240 | [/functional_chains/13/pattern/sequences](codepatchbay-automatic-report.json#/functional_chains/13/pattern/sequences) |

完整关系 [/functional_chains/13/pattern](codepatchbay-automatic-report.json#/functional_chains/13/pattern)；原 source facts [/functional_chains/13/source_facts](codepatchbay-automatic-report.json#/functional_chains/13/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### 可信命令的字段来源 · `cpb-trusted-command-lineage`

`trusted_command_lineage`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`record_command_source_dependencies_do_not_prove_full_heap_noninterference`；Finding=`57e29e3f2281f98bc96e7ca1`；Evidence=`26047964af40b26c149168d5`。
源码/关系 [/functional_chains/14](codepatchbay-automatic-report.json#/functional_chains/14)；缺段 [/functional_chains/14/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/14/analysis_gaps)；模型 [/functional_chains/14/trusted_models](codepatchbay-automatic-report.json#/functional_chains/14/trusted_models)；policy [/functional_chains/14/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/14/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

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

### 未支持方法的失败记录 · `cpb-unsupported-record-retention`

`unsupported_record_retention`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`record_true_marker_does_not_prove_all_input_or_artifact_retention`；Finding=`9d287929d532c5df6d777a3d`；Evidence=`dedc47b87853d5b80ef62667`。
源码/关系 [/functional_chains/15](codepatchbay-automatic-report.json#/functional_chains/15)；缺段 [/functional_chains/15/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/15/analysis_gaps)；模型 [/functional_chains/15/trusted_models](codepatchbay-automatic-report.json#/functional_chains/15/trusted_models)；policy [/functional_chains/15/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/15/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

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
| `cold` | `partial` | `true` | `dd5d4e3cc349b57eb87d0f810a415560bfd5f6b1022a990a35190a44d0e50ebb` |
| `warm` | `partial` | `false` | `dd5d4e3cc349b57eb87d0f810a415560bfd5f6b1022a990a35190a44d0e50ebb` |

这张表复制保存发布记录；partial 是图/解析范围状态，不能据此覆盖上方判断结论。完整记录见 [integration](codepatchbay-integration.json)。
