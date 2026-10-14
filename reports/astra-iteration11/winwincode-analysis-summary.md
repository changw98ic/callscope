# WinWinCode · 保存的自动分析摘要

此摘要只展示已保存正式报告的结果和证据导航；不重新分析、不新增评价，也不替代完整证据。
五项判断是实现追踪，不是全文报告或项目功能覆盖率。链标题只是规则 ID 的展示标签。

- 固定全文基准：[原分析报告](../astra-baseline/WINWINCODE_ANALYSIS.md)；不设置重复 Astra 审批步骤。
- 完整自动报告：[Markdown](winwincode-automatic-report.md) / [JSON](winwincode-automatic-report.json)；[正式 integration](winwincode-integration.json)。
- 快照：`cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2`；状态：`partial`；报告版本：`captured-project-analysis-report-2`。
- 实现：`0.13.0` / `static-multilang-13` / `call-rules-12-report-relations`。
- 源码身份：`eb8e7cae7c2cd2b0503495033cc9a2a98c6e16b3d54b5a2f95dbdca24d118ab2`。
- 策略身份：`c085aff2d4adffa22410a5ce818a1f3ec431665a595de0c4f2d575326c982aaa`。
- 保存 JSON SHA256：`01b324f5d68c082a673d034dc6117e53e7fb05c7c252f06107a794e388249135`；integration SHA256：`03464185c752a28dc8faffa54f9bb261fe78923d88f80037245d71f3a40562e9`。
- 保存比较范围：v12 used CocoIndex; v13 cold and warm scans both recompute every static frontend and detector. Not a same-engine precision/performance comparison.

## 保存范围与结构盘点

选入 `471` 文件，完整解析 `465`；文件状态 `{"parse_error":6,"parsed":465}`。
调用图保存 `32407` 节点、`171939` 边；确定调用 `16396`。这些是结构统计。
外部 `24597` / 动态 `129442` / 歧义 `62` / 未解析 `1442`；外部回调边界 `8559`。
捕获辅助原文 `11`；源根 `["."]`。完整范围见 [/coverage](winwincode-automatic-report.json#/coverage)。

下表仅展示文件数最多的 12 个保存目录条目；目录名不是推断出的运行职责。

| 保存目录 | 文件 / 解析 | 语言文件数 |
| --- | --- | --- |
| `apps/client` | 95 / 95 | `{"typescript":95}` |
| `crates/winwincode-control-plane` | 94 / 94 | `{"rust":94}` |
| `crates/winwincode-storage` | 34 / 33 | `{"rust":34}` |
| `crates/winwincode-execution-port` | 26 / 25 | `{"rust":26}` |
| `crates/winwincode-delivery` | 25 / 25 | `{"rust":25}` |
| `crates/winwincode-server` | 23 / 22 | `{"rust":23}` |
| `crates/winwincode-worker` | 21 / 18 | `{"rust":21}` |
| `crates/winwincode-device-client` | 20 / 20 | `{"rust":20}` |
| `crates/winwincode-codex` | 16 / 16 | `{"rust":16}` |
| `crates/winwincode-client-port` | 12 / 12 | `{"rust":12}` |
| `crates/winwincode-cli` | 11 / 11 | `{"rust":11}` |
| `crates/winwincode-provider` | 11 / 11 | `{"rust":11}` |

全部目录 `45`，保存的确定跨目录依赖条目 `43`；来源见 [/architecture](winwincode-automatic-report.json#/architecture)。
依赖样本仅来自已确定图连接，不证明动态可达、执行顺序或职责正确性。

## 捕获的项目声明

manifest、脚本名称、依赖及文档标题都是捕获声明；没有执行脚本或验证依赖实际可用。

| 保存 manifest | 格式 | 保存名称 / 版本 |
| --- | --- | --- |
| `Cargo.toml` | `toml` | `{"name":null,"version":null}` |
| `crates/winwincode-api/Cargo.toml` | `toml` | `{"name":"winwincode-api","version":{"workspace":true}}` |
| `crates/winwincode-delivery/Cargo.toml` | `toml` | `{"name":"winwincode-delivery","version":{"workspace":true}}` |
| `crates/winwincode-domain/Cargo.toml` | `toml` | `{"name":"winwincode-domain","version":{"workspace":true}}` |

声明文档 `2`，声明缺口 `[]`；详见 [/project_declarations](winwincode-automatic-report.json#/project_declarations)。

## 已保存的完整条件判断

以下 summary、derived_judgment、完整性/支持性和义务状态直接复制；成立条件与反证保留原 JSON 指针。

### `WWC-01`

所选公开导航未提供消费者必需的查询上下文；经真实生产装配与缺值传播，创建在提交命令前被拒绝。有效上下文和替代创建入口是反证。

derived_judgment：`"The selected source-derived absent-query path reaches the actual production port callback and rejects its create before command calls, under the retained platform/form conditions."`
assessment=`scoped_static_judgment_reproduced`；complete=`true`；support=`true`。
必要义务（原状态）：`N1=supported, N2=supported, N3=supported, N4=supported, N5=supported, N6=supported, N7=supported`；必要缺口：`[]`。
Finding=`8587a3dad0bef1ede9bfd666`；Evidence=`e8f805eaeedf86b71cf0237b`；保存 evidence 指针=`/evidence/0/details`（相对于该 Finding）。
完整 [/judgments/0](winwincode-automatic-report.json#/judgments/0)；条件 [/judgments/0/conditions](winwincode-automatic-report.json#/judgments/0/conditions)；反证 [/judgments/0/refutations](winwincode-automatic-report.json#/judgments/0/refutations)；缺口 [/judgments/0/necessary_gaps](winwincode-automatic-report.json#/judgments/0/necessary_gaps)。

### `WWC-02`

所选提交对象遗漏条件分支必填字段；经过生成协议、普通 JSON 与 Serde 映射后，权威非空守卫在使用或提交前拒绝。其它分支和显式字段来源是反证。

derived_judgment：`"Under the explicitly retained normal production, JSON/Serde and active Device conditions, the closed UI command field omission reaches None and the nonblank authority guard rejects before criterion use/commit."`
assessment=`scoped_static_judgment_reproduced`；complete=`true`；support=`true`。
必要义务（原状态）：`D1=supported, D2=supported, D3=supported, D4=supported, D5=supported`；必要缺口：`[]`。
Finding=`7e7dc738afda264f3b24a0d8`；Evidence=`9144dc2875788bfdba88323b`；保存 evidence 指针=`/evidence/0/details`（相对于该 Finding）。
完整 [/judgments/1](winwincode-automatic-report.json#/judgments/1)；条件 [/judgments/1/conditions](winwincode-automatic-report.json#/judgments/1/conditions)；反证 [/judgments/1/refutations](winwincode-automatic-report.json#/judgments/1/refutations)；缺口 [/judgments/1/necessary_gaps](winwincode-automatic-report.json#/judgments/1/necessary_gaps)。

## 所选主要源码链

显示每条保存规则的实际 assessment 和缺口；source-structure 支持与目标分派闭合分开。

### 渲染代次与异步回写条件 · `wwc-browser-continuation-lifecycle`

`browser_async_lifecycle`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`87c75b2e07643b48cd81f1d8`；Evidence=`7f72aef766f31b9517847707`。
源码/关系 [/functional_chains/0](winwincode-automatic-report.json#/functional_chains/0)；缺段 [/functional_chains/0/analysis_gaps](winwincode-automatic-report.json#/functional_chains/0/analysis_gaps)；模型 [/functional_chains/0/trusted_models](winwincode-automatic-report.json#/functional_chains/0/trusted_models)；policy [/functional_chains/0/policy_declarations](winwincode-automatic-report.json#/functional_chains/0/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| all_async_callbacks_guarded_proven | false | [/functional_chains/0/pattern/all_async_callbacks_guarded_proven](winwincode-automatic-report.json#/functional_chains/0/pattern/all_async_callbacks_guarded_proven) |
| all_resources_released_proven | false | [/functional_chains/0/pattern/all_resources_released_proven](winwincode-automatic-report.json#/functional_chains/0/pattern/all_resources_released_proven) |
| all_stale_results_rejected_proven | false | [/functional_chains/0/pattern/all_stale_results_rejected_proven](winwincode-automatic-report.json#/functional_chains/0/pattern/all_stale_results_rejected_proven) |
| closed_result_disposal_consumers/0/close_before_normal_return | true | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/disposed_effects_reverted_proven | false | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/id | c112dca676b65c597bd625be | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/kind | lifecycle_truthy_result_disposal_consumer | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/origin | source-derived | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/promise_fulfillment_and_callback_activation_proven | false | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/relation_component | captured-lifecycle-ownership-relations-1 | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/selected_role | settingsShell | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/source_model | browser-continuation-guard-source-v1 | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/abrupt_location/file | apps/client/src/settings-page.ts | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/abrupt_location/line | 758 | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/abrupt_location/column | 9 | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/abrupt_location/end_line | 758 | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/abrupt_location/start_byte | 29541 | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/abrupt_location/end_byte | 29547 | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/condition_token/root_declaration_id | 0d7629777cc8b0e6de78212203160b2123bba2cddb98c7a70186375e29b1e657 | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/condition_token/root_name | closed | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/condition_token/runtime_resource_identity_proven | false | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/condition_token/root_declaration_location/file | apps/client/src/settings-page.ts | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/condition_token/root_declaration_location/line | 483 | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |
| closed_result_disposal_consumers/0/condition_token/root_declaration_location/column | 7 | [/functional_chains/0/pattern/closed_result_disposal_consumers](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers) |

完整关系 [/functional_chains/0/pattern](winwincode-automatic-report.json#/functional_chains/0/pattern)；原 source facts [/functional_chains/0/source_facts](winwincode-automatic-report.json#/functional_chains/0/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### WinWinCode 记录与资源写者 · `wwc-captured-record-resource-writers`

`resource_writer_ownership`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`503cd6d9621e80a371620dea`；Evidence=`270c257e5b3bbfbff83b79b9`。
源码/关系 [/functional_chains/1](winwincode-automatic-report.json#/functional_chains/1)；缺段 [/functional_chains/1/analysis_gaps](winwincode-automatic-report.json#/functional_chains/1/analysis_gaps)；模型 [/functional_chains/1/trusted_models](winwincode-automatic-report.json#/functional_chains/1/trusted_models)；policy [/functional_chains/1/policy_declarations](winwincode-automatic-report.json#/functional_chains/1/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| all_mutations_authorized_proven | false | [/functional_chains/1/pattern/all_mutations_authorized_proven](winwincode-automatic-report.json#/functional_chains/1/pattern/all_mutations_authorized_proven) |
| all_storage_resources_bound_proven | false | [/functional_chains/1/pattern/all_storage_resources_bound_proven](winwincode-automatic-report.json#/functional_chains/1/pattern/all_storage_resources_bound_proven) |
| call_record_and_effect_frontiers/shown_items/0/activation_and_physical_effect_proven | false | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/authenticated_call_edge_id | e3f0645515e3b509073e48cf | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/authenticated_callee_graph_node_id | ts:apps/client/src/preferences#mountPreferences | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/captured_callee_source | mountPreferences | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/captured_receiver_token | null | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/role | browserShell | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/source_call_fact_id | d87fe1e538142cf765f00c18 | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/kind | identifier | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/name | browser | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/location/file | apps/client/src/application.ts | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/location/line | 195 | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/location/column | 45 | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/location/end_line | 195 | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/location/start_byte | 6970 | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/location/end_byte | 6977 | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/reference/declaration_id | a630274c69c7be85924cdb035d7ad3c07851a1779230f75602892a9483d4b653 | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/reference/declaration_kind | const | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/reference/identity_complete | true | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/reference/parameter_index | null | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/reference/state | unique | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/reference/binder_location/file | apps/client/src/application.ts | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |
| call_record_and_effect_frontiers/shown_items/0/arguments/0/reference/binder_location/line | 193 | [/functional_chains/1/pattern/call_record_and_effect_frontiers](winwincode-automatic-report.json#/functional_chains/1/pattern/call_record_and_effect_frontiers) |

完整关系 [/functional_chains/1/pattern](winwincode-automatic-report.json#/functional_chains/1/pattern)；原 source facts [/functional_chains/1/source_facts](winwincode-automatic-report.json#/functional_chains/1/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### Adapter durable / exact turn · `wwc-report-adapter-durable-exact-turn`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`247af23afa4ac8334a582bfa`；Evidence=`b647b91896ea10fd29a58bcf`。
源码/关系 [/functional_chains/2](winwincode-automatic-report.json#/functional_chains/2)；缺段 [/functional_chains/2/analysis_gaps](winwincode-automatic-report.json#/functional_chains/2/analysis_gaps)；模型 [/functional_chains/2/trusted_models](winwincode-automatic-report.json#/functional_chains/2/trusted_models)；policy [/functional_chains/2/policy_declarations](winwincode-automatic-report.json#/functional_chains/2/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/2/pattern/scoped_source_supported](winwincode-automatic-report.json#/functional_chains/2/pattern/scoped_source_supported) |
| sequences/adapter_submit/all_function_paths_or_effects_accounted | false | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/adapter_submit/future_or_callback_activation_proven | false | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/adapter_submit/region_kind | function_item | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/adapter_submit/role | adapter_submit | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/adapter_submit/assignment_attempts/0/id | 90d41e3430ab64ef75530f85 | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/adapter_submit/assignment_attempts/0/kind | ordered_source_assignment_attempt | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/adapter_submit/assignment_attempts/0/origin | source-derived | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/adapter_submit/assignment_attempts/0/role | adapter_submit | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/adapter_submit/assignment_attempts/0/write_runtime_success_proven | false | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/adapter_submit/assignment_attempts/0/branch_context/0/activation_proven | false | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/adapter_submit/assignment_attempts/0/branch_context/0/kind | match_arm | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/adapter_submit/assignment_attempts/0/branch_context/0/location/file | crates/winwincode-codex/src/adapter.rs | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/adapter_submit/assignment_attempts/0/branch_context/0/location/line | 3539 | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/adapter_submit/assignment_attempts/0/branch_context/0/location/column | 17 | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/adapter_submit/assignment_attempts/0/branch_context/0/location/end_line | 3539 | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/adapter_submit/assignment_attempts/0/branch_context/0/location/start_byte | 138925 | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/adapter_submit/assignment_attempts/0/branch_context/0/location/end_byte | 138988 | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/adapter_submit/assignment_attempts/0/left/current_referent_value_proven | false | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/adapter_submit/assignment_attempts/0/left/kind | field_expression | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/adapter_submit/assignment_attempts/0/left/member | submission_digest | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/adapter_submit/assignment_attempts/0/left/location/file | crates/winwincode-codex/src/adapter.rs | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/adapter_submit/assignment_attempts/0/left/location/line | 3539 | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/adapter_submit/assignment_attempts/0/left/location/column | 25 | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |

完整关系 [/functional_chains/2/pattern](winwincode-automatic-report.json#/functional_chains/2/pattern)；原 source facts [/functional_chains/2/source_facts](winwincode-automatic-report.json#/functional_chains/2/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### Chat 请求与 WorkItem / WorkRun · `wwc-report-chat-delivery-workrun-requests`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`79ca6cc3908f5919d3b7d573`；Evidence=`19318bbcec3b472c92535c6f`。
源码/关系 [/functional_chains/3](winwincode-automatic-report.json#/functional_chains/3)；缺段 [/functional_chains/3/analysis_gaps](winwincode-automatic-report.json#/functional_chains/3/analysis_gaps)；模型 [/functional_chains/3/trusted_models](winwincode-automatic-report.json#/functional_chains/3/trusted_models)；policy [/functional_chains/3/policy_declarations](winwincode-automatic-report.json#/functional_chains/3/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/3/pattern/scoped_source_supported](winwincode-automatic-report.json#/functional_chains/3/pattern/scoped_source_supported) |
| sequences/builder/all_function_paths_or_effects_accounted | false | [/functional_chains/3/pattern/sequences](winwincode-automatic-report.json#/functional_chains/3/pattern/sequences) |
| sequences/builder/future_or_callback_activation_proven | false | [/functional_chains/3/pattern/sequences](winwincode-automatic-report.json#/functional_chains/3/pattern/sequences) |
| sequences/builder/region_kind | function_declaration | [/functional_chains/3/pattern/sequences](winwincode-automatic-report.json#/functional_chains/3/pattern/sequences) |
| sequences/builder/role | builder | [/functional_chains/3/pattern/sequences](winwincode-automatic-report.json#/functional_chains/3/pattern/sequences) |
| sequences/builder/assignment_attempts/shown_items/0/id | 712074bcce14b56c9ed1a503 | [/functional_chains/3/pattern/sequences/builder/assignment_attempts](winwincode-automatic-report.json#/functional_chains/3/pattern/sequences/builder/assignment_attempts) |
| sequences/builder/assignment_attempts/shown_items/0/kind | ordered_source_assignment_attempt | [/functional_chains/3/pattern/sequences/builder/assignment_attempts](winwincode-automatic-report.json#/functional_chains/3/pattern/sequences/builder/assignment_attempts) |
| sequences/builder/assignment_attempts/shown_items/0/origin | source-derived | [/functional_chains/3/pattern/sequences/builder/assignment_attempts](winwincode-automatic-report.json#/functional_chains/3/pattern/sequences/builder/assignment_attempts) |
| sequences/builder/assignment_attempts/shown_items/0/role | builder | [/functional_chains/3/pattern/sequences/builder/assignment_attempts](winwincode-automatic-report.json#/functional_chains/3/pattern/sequences/builder/assignment_attempts) |
| sequences/builder/assignment_attempts/shown_items/0/write_runtime_success_proven | false | [/functional_chains/3/pattern/sequences/builder/assignment_attempts](winwincode-automatic-report.json#/functional_chains/3/pattern/sequences/builder/assignment_attempts) |
| sequences/builder/assignment_attempts/shown_items/0/branch_context/0/branch | then | [/functional_chains/3/pattern/sequences/builder/assignment_attempts](winwincode-automatic-report.json#/functional_chains/3/pattern/sequences/builder/assignment_attempts) |
| sequences/builder/assignment_attempts/shown_items/0/branch_context/0/condition_truth_proven | false | [/functional_chains/3/pattern/sequences/builder/assignment_attempts](winwincode-automatic-report.json#/functional_chains/3/pattern/sequences/builder/assignment_attempts) |
| sequences/builder/assignment_attempts/shown_items/0/branch_context/0/kind | if | [/functional_chains/3/pattern/sequences/builder/assignment_attempts](winwincode-automatic-report.json#/functional_chains/3/pattern/sequences/builder/assignment_attempts) |
| sequences/builder/assignment_attempts/shown_items/0/branch_context/0/condition/kind | binary_expression | [/functional_chains/3/pattern/sequences/builder/assignment_attempts](winwincode-automatic-report.json#/functional_chains/3/pattern/sequences/builder/assignment_attempts) |
| sequences/builder/assignment_attempts/shown_items/0/branch_context/0/condition/operator | === | [/functional_chains/3/pattern/sequences/builder/assignment_attempts](winwincode-automatic-report.json#/functional_chains/3/pattern/sequences/builder/assignment_attempts) |
| sequences/builder/assignment_attempts/shown_items/0/branch_context/0/condition/runtime_predicate_or_assignment_proven | false | [/functional_chains/3/pattern/sequences/builder/assignment_attempts](winwincode-automatic-report.json#/functional_chains/3/pattern/sequences/builder/assignment_attempts) |
| sequences/builder/assignment_attempts/shown_items/0/branch_context/0/condition/location/file | apps/client/src/chat-delivery-creator.ts | [/functional_chains/3/pattern/sequences/builder/assignment_attempts](winwincode-automatic-report.json#/functional_chains/3/pattern/sequences/builder/assignment_attempts) |
| sequences/builder/assignment_attempts/shown_items/0/branch_context/0/condition/location/line | 226 | [/functional_chains/3/pattern/sequences/builder/assignment_attempts](winwincode-automatic-report.json#/functional_chains/3/pattern/sequences/builder/assignment_attempts) |
| sequences/builder/assignment_attempts/shown_items/0/branch_context/0/condition/location/column | 9 | [/functional_chains/3/pattern/sequences/builder/assignment_attempts](winwincode-automatic-report.json#/functional_chains/3/pattern/sequences/builder/assignment_attempts) |
| sequences/builder/assignment_attempts/shown_items/0/branch_context/0/condition/location/end_line | 226 | [/functional_chains/3/pattern/sequences/builder/assignment_attempts](winwincode-automatic-report.json#/functional_chains/3/pattern/sequences/builder/assignment_attempts) |
| sequences/builder/assignment_attempts/shown_items/0/branch_context/0/condition/location/start_byte | 7690 | [/functional_chains/3/pattern/sequences/builder/assignment_attempts](winwincode-automatic-report.json#/functional_chains/3/pattern/sequences/builder/assignment_attempts) |
| sequences/builder/assignment_attempts/shown_items/0/branch_context/0/condition/location/end_byte | 7706 | [/functional_chains/3/pattern/sequences/builder/assignment_attempts](winwincode-automatic-report.json#/functional_chains/3/pattern/sequences/builder/assignment_attempts) |
| sequences/builder/assignment_attempts/shown_items/0/branch_context/0/condition/operands/0/kind | 显示投影省略 | [/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/branch_context/0/condition/operands/0/kind](winwincode-automatic-report.json#/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/branch_context/0/condition/operands/0/kind) |
| sequences/builder/assignment_attempts/shown_items/0/branch_context/0/condition/operands/0/name | 显示投影省略 | [/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/branch_context/0/condition/operands/0/name](winwincode-automatic-report.json#/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/branch_context/0/condition/operands/0/name) |

完整关系 [/functional_chains/3/pattern](winwincode-automatic-report.json#/functional_chains/3/pattern)；原 source facts [/functional_chains/3/source_facts](winwincode-automatic-report.json#/functional_chains/3/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### Chat 请求身份与字段保留 · `wwc-report-chat-retained-request-identities`

`message_identity_relations`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`38c824f8b536a9f7d17dc8ad`；Evidence=`688bfd252f4e08f62d95fbf5`。
源码/关系 [/functional_chains/4](winwincode-automatic-report.json#/functional_chains/4)；缺段 [/functional_chains/4/analysis_gaps](winwincode-automatic-report.json#/functional_chains/4/analysis_gaps)；模型 [/functional_chains/4/trusted_models](winwincode-automatic-report.json#/functional_chains/4/trusted_models)；policy [/functional_chains/4/policy_declarations](winwincode-automatic-report.json#/functional_chains/4/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| budget/incomplete | false | [/functional_chains/4/pattern/budget](winwincode-automatic-report.json#/functional_chains/4/pattern/budget) |
| budget/limit | 65536 | [/functional_chains/4/pattern/budget](winwincode-automatic-report.json#/functional_chains/4/pattern/budget) |
| budget/operations | 901 | [/functional_chains/4/pattern/budget](winwincode-automatic-report.json#/functional_chains/4/pattern/budget) |
| components/chat_request_identity/all_chat_commands_covered | false | [/functional_chains/4/pattern/components](winwincode-automatic-report.json#/functional_chains/4/pattern/components) |
| components/chat_request_identity/runtime_retry_or_transport_proven | false | [/functional_chains/4/pattern/components](winwincode-automatic-report.json#/functional_chains/4/pattern/components) |
| components/chat_request_identity/scope | one captured Chat create body and its selected fixed-record builder; requests are separate identities linked through the retained delivery field | [/functional_chains/4/pattern/components](winwincode-automatic-report.json#/functional_chains/4/pattern/components) |
| components/chat_request_identity/supported | true | [/functional_chains/4/pattern/components](winwincode-automatic-report.json#/functional_chains/4/pattern/components) |
| components/chat_request_identity/builder_call_relations/0/edge_id | 56319ab867fb03c8cb21decd | [/functional_chains/4/pattern/components](winwincode-automatic-report.json#/functional_chains/4/pattern/components) |
| components/chat_request_identity/builder_call_relations/0/fact_id | 7e6c19c10b0bf1c4555c769a | [/functional_chains/4/pattern/components](winwincode-automatic-report.json#/functional_chains/4/pattern/components) |
| components/chat_request_identity/builder_call_relations/0/kind | existing_authenticated_call | [/functional_chains/4/pattern/components](winwincode-automatic-report.json#/functional_chains/4/pattern/components) |
| components/chat_request_identity/builder_call_relations/0/supported | true | [/functional_chains/4/pattern/components](winwincode-automatic-report.json#/functional_chains/4/pattern/components) |
| components/chat_request_identity/builder_call_relations/0/target_role | chat_items_builder | [/functional_chains/4/pattern/components](winwincode-automatic-report.json#/functional_chains/4/pattern/components) |
| components/chat_request_identity/builder_field_projections/shown_items/0/creates_calls_edge | false | [/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections](winwincode-automatic-report.json#/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections) |
| components/chat_request_identity/builder_field_projections/shown_items/0/extractor_version | captured-message-identity-relations-1 | [/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections](winwincode-automatic-report.json#/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections) |
| components/chat_request_identity/builder_field_projections/shown_items/0/field | actor | [/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections](winwincode-automatic-report.json#/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections) |
| components/chat_request_identity/builder_field_projections/shown_items/0/id | 68d6295081115e6378f1aa73 | [/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections](winwincode-automatic-report.json#/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections) |
| components/chat_request_identity/builder_field_projections/shown_items/0/kind | message_builder_field_projection | [/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections](winwincode-automatic-report.json#/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections) |
| components/chat_request_identity/builder_field_projections/shown_items/0/origin | source-derived | [/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections](winwincode-automatic-report.json#/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections) |
| components/chat_request_identity/builder_field_projections/shown_items/0/target_code_executed | false | [/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections](winwincode-automatic-report.json#/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections) |
| components/chat_request_identity/builder_field_projections/shown_items/0/location/file | apps/client/src/community-control-plane-client.ts | [/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections](winwincode-automatic-report.json#/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections) |
| components/chat_request_identity/builder_field_projections/shown_items/0/location/line | 424 | [/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections](winwincode-automatic-report.json#/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections) |
| components/chat_request_identity/builder_field_projections/shown_items/0/location/column | 12 | [/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections](winwincode-automatic-report.json#/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections) |
| components/chat_request_identity/builder_field_projections/shown_items/0/location/end_line | 424 | [/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections](winwincode-automatic-report.json#/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections) |
| components/chat_request_identity/builder_field_projections/shown_items/0/location/start_byte | 16586 | [/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections](winwincode-automatic-report.json#/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections) |

完整关系 [/functional_chains/4/pattern](winwincode-automatic-report.json#/functional_chains/4/pattern)；原 source facts [/functional_chains/4/source_facts](winwincode-automatic-report.json#/functional_chains/4/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### Device provider 部署分流 · `wwc-report-device-provider-deployment`

`deployment_provider_split`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`deployment_candidate_chain_not_global_dispatch_or_credential_availability`；Finding=`760fc36cee29db794d4056c6`；Evidence=`e86cf700fe852d931a5420bb`。
源码/关系 [/functional_chains/5](winwincode-automatic-report.json#/functional_chains/5)；缺段 [/functional_chains/5/analysis_gaps](winwincode-automatic-report.json#/functional_chains/5/analysis_gaps)；模型 [/functional_chains/5/trusted_models](winwincode-automatic-report.json#/functional_chains/5/trusted_models)；policy [/functional_chains/5/policy_declarations](winwincode-automatic-report.json#/functional_chains/5/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| boundary_results/0/id | ab2cfada79b8758a58eac49d | [/functional_chains/5/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/5/pattern/boundary_results) |
| boundary_results/0/kind | boundary_result_source | [/functional_chains/5/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/5/pattern/boundary_results) |
| boundary_results/0/origin | source-derived | [/functional_chains/5/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/5/pattern/boundary_results) |
| boundary_results/0/runtime_result_proven | false | [/functional_chains/5/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/5/pattern/boundary_results) |
| boundary_results/0/expression/call_effects_or_result_proven | false | [/functional_chains/5/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/5/pattern/boundary_results) |
| boundary_results/0/expression/callee_source | Err | [/functional_chains/5/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/5/pattern/boundary_results) |
| boundary_results/0/expression/kind | call_expression | [/functional_chains/5/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/5/pattern/boundary_results) |
| boundary_results/0/expression/arguments/0/kind | scoped_identifier | [/functional_chains/5/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/5/pattern/boundary_results) |
| boundary_results/0/expression/arguments/0/source | winwincode_control_plane::DurableExecutionPortError::UnsupportedMessage | [/functional_chains/5/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/5/pattern/boundary_results) |
| boundary_results/0/expression/arguments/0/children/0/kind | scoped_identifier | [/functional_chains/5/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/5/pattern/boundary_results) |
| boundary_results/0/expression/arguments/0/children/0/source | winwincode_control_plane::DurableExecutionPortError | [/functional_chains/5/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/5/pattern/boundary_results) |
| boundary_results/0/expression/arguments/0/children/0/children/0/kind | 显示投影省略 | [/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/children/0/children/0/kind](winwincode-automatic-report.json#/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/children/0/children/0/kind) |
| boundary_results/0/expression/arguments/0/children/0/children/0/name | 显示投影省略 | [/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/children/0/children/0/name](winwincode-automatic-report.json#/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/children/0/children/0/name) |
| boundary_results/0/expression/arguments/0/children/0/children/0/location | 显示投影省略 | [/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/children/0/children/0/location](winwincode-automatic-report.json#/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/children/0/children/0/location) |
| boundary_results/0/expression/arguments/0/children/0/children/0/reference | 显示投影省略 | [/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/children/0/children/0/reference](winwincode-automatic-report.json#/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/children/0/children/0/reference) |
| boundary_results/0/expression/arguments/0/children/0/children/1/kind | 显示投影省略 | [/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/children/0/children/1/kind](winwincode-automatic-report.json#/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/children/0/children/1/kind) |
| boundary_results/0/expression/arguments/0/children/0/children/1/name | 显示投影省略 | [/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/children/0/children/1/name](winwincode-automatic-report.json#/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/children/0/children/1/name) |
| boundary_results/0/expression/arguments/0/children/0/children/1/location | 显示投影省略 | [/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/children/0/children/1/location](winwincode-automatic-report.json#/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/children/0/children/1/location) |
| boundary_results/0/expression/arguments/0/children/0/children/1/reference | 显示投影省略 | [/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/children/0/children/1/reference](winwincode-automatic-report.json#/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/children/0/children/1/reference) |
| boundary_results/0/expression/arguments/0/children/0/location/file | crates/winwincode-server/src/main.rs | [/functional_chains/5/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/5/pattern/boundary_results) |
| boundary_results/0/expression/arguments/0/children/0/location/line | 346 | [/functional_chains/5/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/5/pattern/boundary_results) |
| boundary_results/0/expression/arguments/0/children/0/location/column | 13 | [/functional_chains/5/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/5/pattern/boundary_results) |
| boundary_results/0/expression/arguments/0/children/0/location/end_line | 346 | [/functional_chains/5/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/5/pattern/boundary_results) |
| boundary_results/0/expression/arguments/0/children/0/location/start_byte | 13431 | [/functional_chains/5/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/5/pattern/boundary_results) |

完整关系 [/functional_chains/5/pattern](winwincode-automatic-report.json#/functional_chains/5/pattern)；原 source facts [/functional_chains/5/source_facts](winwincode-automatic-report.json#/functional_chains/5/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### Kernel create_session 接口 · `wwc-report-kernel-create-session-interface`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`9e6f9a052635cfe39709cfcb`；Evidence=`b5c22276425869081b036a8e`。
源码/关系 [/functional_chains/6](winwincode-automatic-report.json#/functional_chains/6)；缺段 [/functional_chains/6/analysis_gaps](winwincode-automatic-report.json#/functional_chains/6/analysis_gaps)；模型 [/functional_chains/6/trusted_models](winwincode-automatic-report.json#/functional_chains/6/trusted_models)；policy [/functional_chains/6/policy_declarations](winwincode-automatic-report.json#/functional_chains/6/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| nested_source_regions/0/body_activation_proven | false | [/functional_chains/6/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/6/pattern/nested_source_regions) |
| nested_source_regions/0/future_fulfillment_proven | false | [/functional_chains/6/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/6/pattern/nested_source_regions) |
| nested_source_regions/0/id | 94663e096f62c84dfd5647eb | [/functional_chains/6/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/6/pattern/nested_source_regions) |
| nested_source_regions/0/kind | deferred_source_region_sequence | [/functional_chains/6/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/6/pattern/nested_source_regions) |
| nested_source_regions/0/nested_calls_promoted_to_resolved | false | [/functional_chains/6/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/6/pattern/nested_source_regions) |
| nested_source_regions/0/origin | source-derived | [/functional_chains/6/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/6/pattern/nested_source_regions) |
| nested_source_regions/0/role | kernel_create | [/functional_chains/6/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/6/pattern/nested_source_regions) |
| nested_source_regions/0/conditions/0 | this deferred captured body is activated and the recorded statements are reached normally | [/functional_chains/6/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/6/pattern/nested_source_regions) |
| nested_source_regions/0/location/file | crates/kernel/src/lib.rs | [/functional_chains/6/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/6/pattern/nested_source_regions) |
| nested_source_regions/0/location/line | 1221 | [/functional_chains/6/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/6/pattern/nested_source_regions) |
| nested_source_regions/0/location/column | 21 | [/functional_chains/6/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/6/pattern/nested_source_regions) |
| nested_source_regions/0/location/end_line | 1230 | [/functional_chains/6/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/6/pattern/nested_source_regions) |
| nested_source_regions/0/location/start_byte | 44514 | [/functional_chains/6/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/6/pattern/nested_source_regions) |
| nested_source_regions/0/location/end_byte | 44981 | [/functional_chains/6/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/6/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/all_function_paths_or_effects_accounted | false | [/functional_chains/6/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/6/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/future_or_callback_activation_proven | false | [/functional_chains/6/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/6/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/region_kind | async_block | [/functional_chains/6/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/6/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/role | kernel_create | [/functional_chains/6/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/6/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/orders/0/after_step_id | e5bc9708256c5d88bd42401d | [/functional_chains/6/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/6/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/orders/0/all_paths_reach_next_proven | false | [/functional_chains/6/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/6/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/orders/0/before_step_id | 320a72e058dd618cc4cf5fe7 | [/functional_chains/6/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/6/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/orders/0/id | 83d107da963e01963366fab5 | [/functional_chains/6/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/6/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/orders/0/kind | conditional_direct_statement_order | [/functional_chains/6/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/6/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/orders/0/model_id | captured-normal-statement-control-v1 | [/functional_chains/6/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/6/pattern/nested_source_regions) |

完整关系 [/functional_chains/6/pattern](winwincode-automatic-report.json#/functional_chains/6/pattern)；原 source facts [/functional_chains/6/source_facts](winwincode-automatic-report.json#/functional_chains/6/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### Kernel reconcile_turn_exact 接口 · `wwc-report-kernel-reconcile-exact-interface`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`557da6f8cb10a7baed663d3b`；Evidence=`15fa9079162b552d1f0ad5d1`。
源码/关系 [/functional_chains/7](winwincode-automatic-report.json#/functional_chains/7)；缺段 [/functional_chains/7/analysis_gaps](winwincode-automatic-report.json#/functional_chains/7/analysis_gaps)；模型 [/functional_chains/7/trusted_models](winwincode-automatic-report.json#/functional_chains/7/trusted_models)；policy [/functional_chains/7/policy_declarations](winwincode-automatic-report.json#/functional_chains/7/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| nested_source_regions/0/body_activation_proven | false | [/functional_chains/7/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/7/pattern/nested_source_regions) |
| nested_source_regions/0/future_fulfillment_proven | false | [/functional_chains/7/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/7/pattern/nested_source_regions) |
| nested_source_regions/0/id | 4b5bfecc921378671ac24ec6 | [/functional_chains/7/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/7/pattern/nested_source_regions) |
| nested_source_regions/0/kind | deferred_source_region_sequence | [/functional_chains/7/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/7/pattern/nested_source_regions) |
| nested_source_regions/0/nested_calls_promoted_to_resolved | false | [/functional_chains/7/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/7/pattern/nested_source_regions) |
| nested_source_regions/0/origin | source-derived | [/functional_chains/7/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/7/pattern/nested_source_regions) |
| nested_source_regions/0/role | kernel_reconcile | [/functional_chains/7/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/7/pattern/nested_source_regions) |
| nested_source_regions/0/conditions/0 | this deferred captured body is activated and the recorded statements are reached normally | [/functional_chains/7/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/7/pattern/nested_source_regions) |
| nested_source_regions/0/location/file | crates/kernel/src/lib.rs | [/functional_chains/7/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/7/pattern/nested_source_regions) |
| nested_source_regions/0/location/line | 1376 | [/functional_chains/7/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/7/pattern/nested_source_regions) |
| nested_source_regions/0/location/column | 21 | [/functional_chains/7/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/7/pattern/nested_source_regions) |
| nested_source_regions/0/location/end_line | 1432 | [/functional_chains/7/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/7/pattern/nested_source_regions) |
| nested_source_regions/0/location/start_byte | 50583 | [/functional_chains/7/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/7/pattern/nested_source_regions) |
| nested_source_regions/0/location/end_byte | 53102 | [/functional_chains/7/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/7/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/all_function_paths_or_effects_accounted | false | [/functional_chains/7/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/7/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/future_or_callback_activation_proven | false | [/functional_chains/7/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/7/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/region_kind | async_block | [/functional_chains/7/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/7/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/role | kernel_reconcile | [/functional_chains/7/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/7/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/id | 8b85ee660787e07af8da6fe8 | [/functional_chains/7/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/7/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/kind | source_guard_and_abrupt_branch | [/functional_chains/7/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/7/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/origin | source-derived | [/functional_chains/7/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/7/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/role | kernel_reconcile | [/functional_chains/7/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/7/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/runtime_predicate_proven | false | [/functional_chains/7/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/7/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/branches/0/branch | then | [/functional_chains/7/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/7/pattern/nested_source_regions) |

完整关系 [/functional_chains/7/pattern](winwincode-automatic-report.json#/functional_chains/7/pattern)；原 source facts [/functional_chains/7/source_facts](winwincode-automatic-report.json#/functional_chains/7/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### Kernel submit_turn 接口 · `wwc-report-kernel-submit-turn-interface`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`42977c03f1c8a2a9e2521666`；Evidence=`0bd42c038dd5d829bbc1821f`。
源码/关系 [/functional_chains/8](winwincode-automatic-report.json#/functional_chains/8)；缺段 [/functional_chains/8/analysis_gaps](winwincode-automatic-report.json#/functional_chains/8/analysis_gaps)；模型 [/functional_chains/8/trusted_models](winwincode-automatic-report.json#/functional_chains/8/trusted_models)；policy [/functional_chains/8/policy_declarations](winwincode-automatic-report.json#/functional_chains/8/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| nested_source_regions/0/body_activation_proven | false | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/future_fulfillment_proven | false | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/id | d9b2044f73f4aae62ce5e783 | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/kind | deferred_source_region_sequence | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/nested_calls_promoted_to_resolved | false | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/origin | source-derived | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/role | kernel_submit | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/conditions/0 | this deferred captured body is activated and the recorded statements are reached normally | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/location/file | crates/kernel/src/lib.rs | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/location/line | 1339 | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/location/column | 21 | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/location/end_line | 1356 | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/location/start_byte | 49122 | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/location/end_byte | 49859 | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/all_function_paths_or_effects_accounted | false | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/future_or_callback_activation_proven | false | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/region_kind | async_block | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/role | kernel_submit | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/id | b7789aa6094243ca51cbe06a | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/kind | source_guard_and_abrupt_branch | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/origin | source-derived | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/role | kernel_submit | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/runtime_predicate_proven | false | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/branches/0/branch | then | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |

完整关系 [/functional_chains/8/pattern](winwincode-automatic-report.json#/functional_chains/8/pattern)；原 source facts [/functional_chains/8/source_facts](winwincode-automatic-report.json#/functional_chains/8/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### 发件记录与确认关联字段 · `wwc-report-outbox-ack-correlation-fields`

`message_identity_relations`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`4414f1cf6af7cc88a1e0a80f`；Evidence=`616c459960b976504475b608`。
源码/关系 [/functional_chains/9](winwincode-automatic-report.json#/functional_chains/9)；缺段 [/functional_chains/9/analysis_gaps](winwincode-automatic-report.json#/functional_chains/9/analysis_gaps)；模型 [/functional_chains/9/trusted_models](winwincode-automatic-report.json#/functional_chains/9/trusted_models)；policy [/functional_chains/9/policy_declarations](winwincode-automatic-report.json#/functional_chains/9/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| budget/incomplete | false | [/functional_chains/9/pattern/budget](winwincode-automatic-report.json#/functional_chains/9/pattern/budget) |
| budget/limit | 65536 | [/functional_chains/9/pattern/budget](winwincode-automatic-report.json#/functional_chains/9/pattern/budget) |
| budget/operations | 2145 | [/functional_chains/9/pattern/budget](winwincode-automatic-report.json#/functional_chains/9/pattern/budget) |
| components/outbox_ack_correlation/all_message_families_covered | false | [/functional_chains/9/pattern/components](winwincode-automatic-report.json#/functional_chains/9/pattern/components) |
| components/outbox_ack_correlation/external_ack_truth_or_exactly_once_proven | false | [/functional_chains/9/pattern/components](winwincode-automatic-report.json#/functional_chains/9/pattern/components) |
| components/outbox_ack_correlation/outcome_helper_tuple_expanded | false | [/functional_chains/9/pattern/components](winwincode-automatic-report.json#/functional_chains/9/pattern/components) |
| components/outbox_ack_correlation/physical_store_commit_proven | false | [/functional_chains/9/pattern/components](winwincode-automatic-report.json#/functional_chains/9/pattern/components) |
| components/outbox_ack_correlation/scope | only closed enum-arm direct tuple correlations and literal outbox insert/delete source seams | [/functional_chains/9/pattern/components](winwincode-automatic-report.json#/functional_chains/9/pattern/components) |
| components/outbox_ack_correlation/sequence_to_ack_sequence_rename_value_proven | false | [/functional_chains/9/pattern/components](winwincode-automatic-report.json#/functional_chains/9/pattern/components) |
| components/outbox_ack_correlation/supported | true | [/functional_chains/9/pattern/components](winwincode-automatic-report.json#/functional_chains/9/pattern/components) |
| components/outbox_ack_correlation/ack_gate_sources/0/caller_supplied_domain_validation_independently_proven | false | [/functional_chains/9/pattern/components](winwincode-automatic-report.json#/functional_chains/9/pattern/components) |
| components/outbox_ack_correlation/ack_gate_sources/0/creates_calls_edge | false | [/functional_chains/9/pattern/components](winwincode-automatic-report.json#/functional_chains/9/pattern/components) |
| components/outbox_ack_correlation/ack_gate_sources/0/extractor_version | captured-message-identity-relations-1 | [/functional_chains/9/pattern/components](winwincode-automatic-report.json#/functional_chains/9/pattern/components) |
| components/outbox_ack_correlation/ack_gate_sources/0/id | ae22eebeb82fe8d73e31d47c | [/functional_chains/9/pattern/components](winwincode-automatic-report.json#/functional_chains/9/pattern/components) |
| components/outbox_ack_correlation/ack_gate_sources/0/kind | message_ack_authority_source_guard | [/functional_chains/9/pattern/components](winwincode-automatic-report.json#/functional_chains/9/pattern/components) |
| components/outbox_ack_correlation/ack_gate_sources/0/origin | source-derived | [/functional_chains/9/pattern/components](winwincode-automatic-report.json#/functional_chains/9/pattern/components) |
| components/outbox_ack_correlation/ack_gate_sources/0/target_code_executed | false | [/functional_chains/9/pattern/components](winwincode-automatic-report.json#/functional_chains/9/pattern/components) |
| components/outbox_ack_correlation/ack_gate_sources/0/arguments/0/kind | identifier | [/functional_chains/9/pattern/components](winwincode-automatic-report.json#/functional_chains/9/pattern/components) |
| components/outbox_ack_correlation/ack_gate_sources/0/arguments/0/name | acknowledgement | [/functional_chains/9/pattern/components](winwincode-automatic-report.json#/functional_chains/9/pattern/components) |
| components/outbox_ack_correlation/ack_gate_sources/0/arguments/0/location/file | crates/winwincode-codex/src/outbox.rs | [/functional_chains/9/pattern/components](winwincode-automatic-report.json#/functional_chains/9/pattern/components) |
| components/outbox_ack_correlation/ack_gate_sources/0/arguments/0/location/line | 269 | [/functional_chains/9/pattern/components](winwincode-automatic-report.json#/functional_chains/9/pattern/components) |
| components/outbox_ack_correlation/ack_gate_sources/0/arguments/0/location/column | 31 | [/functional_chains/9/pattern/components](winwincode-automatic-report.json#/functional_chains/9/pattern/components) |
| components/outbox_ack_correlation/ack_gate_sources/0/arguments/0/location/end_line | 269 | [/functional_chains/9/pattern/components](winwincode-automatic-report.json#/functional_chains/9/pattern/components) |
| components/outbox_ack_correlation/ack_gate_sources/0/arguments/0/location/start_byte | 11817 | [/functional_chains/9/pattern/components](winwincode-automatic-report.json#/functional_chains/9/pattern/components) |

完整关系 [/functional_chains/9/pattern](winwincode-automatic-report.json#/functional_chains/9/pattern)；原 source facts [/functional_chains/9/source_facts](winwincode-automatic-report.json#/functional_chains/9/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### ProductionAdapter → Kernel 构造 · `wwc-report-production-adapter-embedded-kernel`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`c901566eaf1f168ef369c481`；Evidence=`00c779145d1bc95117d02554`。
源码/关系 [/functional_chains/10](winwincode-automatic-report.json#/functional_chains/10)；缺段 [/functional_chains/10/analysis_gaps](winwincode-automatic-report.json#/functional_chains/10/analysis_gaps)；模型 [/functional_chains/10/trusted_models](winwincode-automatic-report.json#/functional_chains/10/trusted_models)；policy [/functional_chains/10/policy_declarations](winwincode-automatic-report.json#/functional_chains/10/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/10/pattern/scoped_source_supported](winwincode-automatic-report.json#/functional_chains/10/pattern/scoped_source_supported) |
| sequences/adapter_open/all_function_paths_or_effects_accounted | false | [/functional_chains/10/pattern/sequences](winwincode-automatic-report.json#/functional_chains/10/pattern/sequences) |
| sequences/adapter_open/future_or_callback_activation_proven | false | [/functional_chains/10/pattern/sequences](winwincode-automatic-report.json#/functional_chains/10/pattern/sequences) |
| sequences/adapter_open/region_kind | function_item | [/functional_chains/10/pattern/sequences](winwincode-automatic-report.json#/functional_chains/10/pattern/sequences) |
| sequences/adapter_open/role | adapter_open | [/functional_chains/10/pattern/sequences](winwincode-automatic-report.json#/functional_chains/10/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/id | 744db531952c791c40e55a60 | [/functional_chains/10/pattern/sequences](winwincode-automatic-report.json#/functional_chains/10/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/kind | ordered_source_assignment_attempt | [/functional_chains/10/pattern/sequences](winwincode-automatic-report.json#/functional_chains/10/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/origin | source-derived | [/functional_chains/10/pattern/sequences](winwincode-automatic-report.json#/functional_chains/10/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/role | adapter_open | [/functional_chains/10/pattern/sequences](winwincode-automatic-report.json#/functional_chains/10/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/write_runtime_success_proven | false | [/functional_chains/10/pattern/sequences](winwincode-automatic-report.json#/functional_chains/10/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/current_referent_value_proven | false | [/functional_chains/10/pattern/sequences](winwincode-automatic-report.json#/functional_chains/10/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/kind | field_expression | [/functional_chains/10/pattern/sequences](winwincode-automatic-report.json#/functional_chains/10/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/member | helper_executable | [/functional_chains/10/pattern/sequences](winwincode-automatic-report.json#/functional_chains/10/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/location/file | crates/winwincode-codex/src/adapter.rs | [/functional_chains/10/pattern/sequences](winwincode-automatic-report.json#/functional_chains/10/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/location/line | 420 | [/functional_chains/10/pattern/sequences](winwincode-automatic-report.json#/functional_chains/10/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/location/column | 9 | [/functional_chains/10/pattern/sequences](winwincode-automatic-report.json#/functional_chains/10/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/location/end_line | 420 | [/functional_chains/10/pattern/sequences](winwincode-automatic-report.json#/functional_chains/10/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/location/start_byte | 17565 | [/functional_chains/10/pattern/sequences](winwincode-automatic-report.json#/functional_chains/10/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/location/end_byte | 17589 | [/functional_chains/10/pattern/sequences](winwincode-automatic-report.json#/functional_chains/10/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/member_location/file | crates/winwincode-codex/src/adapter.rs | [/functional_chains/10/pattern/sequences](winwincode-automatic-report.json#/functional_chains/10/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/member_location/line | 420 | [/functional_chains/10/pattern/sequences](winwincode-automatic-report.json#/functional_chains/10/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/member_location/column | 16 | [/functional_chains/10/pattern/sequences](winwincode-automatic-report.json#/functional_chains/10/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/member_location/end_line | 420 | [/functional_chains/10/pattern/sequences](winwincode-automatic-report.json#/functional_chains/10/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/member_location/start_byte | 17572 | [/functional_chains/10/pattern/sequences](winwincode-automatic-report.json#/functional_chains/10/pattern/sequences) |

完整关系 [/functional_chains/10/pattern](winwincode-automatic-report.json#/functional_chains/10/pattern)；原 source facts [/functional_chains/10/source_facts](winwincode-automatic-report.json#/functional_chains/10/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### intent → persist → exact reconcile · `wwc-report-submission-intent-kernel-order`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`e1a2d1a98046bb6e76d3c181`；Evidence=`bb269bde2edbbed274bea4e3`。
源码/关系 [/functional_chains/11](winwincode-automatic-report.json#/functional_chains/11)；缺段 [/functional_chains/11/analysis_gaps](winwincode-automatic-report.json#/functional_chains/11/analysis_gaps)；模型 [/functional_chains/11/trusted_models](winwincode-automatic-report.json#/functional_chains/11/trusted_models)；policy [/functional_chains/11/policy_declarations](winwincode-automatic-report.json#/functional_chains/11/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/11/pattern/scoped_source_supported](winwincode-automatic-report.json#/functional_chains/11/pattern/scoped_source_supported) |
| sequences/submission/all_function_paths_or_effects_accounted | false | [/functional_chains/11/pattern/sequences](winwincode-automatic-report.json#/functional_chains/11/pattern/sequences) |
| sequences/submission/future_or_callback_activation_proven | false | [/functional_chains/11/pattern/sequences](winwincode-automatic-report.json#/functional_chains/11/pattern/sequences) |
| sequences/submission/region_kind | function_item | [/functional_chains/11/pattern/sequences](winwincode-automatic-report.json#/functional_chains/11/pattern/sequences) |
| sequences/submission/role | submission | [/functional_chains/11/pattern/sequences](winwincode-automatic-report.json#/functional_chains/11/pattern/sequences) |
| sequences/submission/assignment_attempts/0/id | a4a2cb197e3bf7b8ed776cfe | [/functional_chains/11/pattern/sequences](winwincode-automatic-report.json#/functional_chains/11/pattern/sequences) |
| sequences/submission/assignment_attempts/0/kind | ordered_source_assignment_attempt | [/functional_chains/11/pattern/sequences](winwincode-automatic-report.json#/functional_chains/11/pattern/sequences) |
| sequences/submission/assignment_attempts/0/origin | source-derived | [/functional_chains/11/pattern/sequences](winwincode-automatic-report.json#/functional_chains/11/pattern/sequences) |
| sequences/submission/assignment_attempts/0/role | submission | [/functional_chains/11/pattern/sequences](winwincode-automatic-report.json#/functional_chains/11/pattern/sequences) |
| sequences/submission/assignment_attempts/0/write_runtime_success_proven | false | [/functional_chains/11/pattern/sequences](winwincode-automatic-report.json#/functional_chains/11/pattern/sequences) |
| sequences/submission/assignment_attempts/0/branch_context/0/activation_proven | false | [/functional_chains/11/pattern/sequences](winwincode-automatic-report.json#/functional_chains/11/pattern/sequences) |
| sequences/submission/assignment_attempts/0/branch_context/0/kind | match_arm | [/functional_chains/11/pattern/sequences](winwincode-automatic-report.json#/functional_chains/11/pattern/sequences) |
| sequences/submission/assignment_attempts/0/branch_context/0/location/file | crates/winwincode-codex/src/adapter.rs | [/functional_chains/11/pattern/sequences](winwincode-automatic-report.json#/functional_chains/11/pattern/sequences) |
| sequences/submission/assignment_attempts/0/branch_context/0/location/line | 3539 | [/functional_chains/11/pattern/sequences](winwincode-automatic-report.json#/functional_chains/11/pattern/sequences) |
| sequences/submission/assignment_attempts/0/branch_context/0/location/column | 17 | [/functional_chains/11/pattern/sequences](winwincode-automatic-report.json#/functional_chains/11/pattern/sequences) |
| sequences/submission/assignment_attempts/0/branch_context/0/location/end_line | 3539 | [/functional_chains/11/pattern/sequences](winwincode-automatic-report.json#/functional_chains/11/pattern/sequences) |
| sequences/submission/assignment_attempts/0/branch_context/0/location/start_byte | 138925 | [/functional_chains/11/pattern/sequences](winwincode-automatic-report.json#/functional_chains/11/pattern/sequences) |
| sequences/submission/assignment_attempts/0/branch_context/0/location/end_byte | 138988 | [/functional_chains/11/pattern/sequences](winwincode-automatic-report.json#/functional_chains/11/pattern/sequences) |
| sequences/submission/assignment_attempts/0/left/current_referent_value_proven | false | [/functional_chains/11/pattern/sequences](winwincode-automatic-report.json#/functional_chains/11/pattern/sequences) |
| sequences/submission/assignment_attempts/0/left/kind | field_expression | [/functional_chains/11/pattern/sequences](winwincode-automatic-report.json#/functional_chains/11/pattern/sequences) |
| sequences/submission/assignment_attempts/0/left/member | submission_digest | [/functional_chains/11/pattern/sequences](winwincode-automatic-report.json#/functional_chains/11/pattern/sequences) |
| sequences/submission/assignment_attempts/0/left/location/file | crates/winwincode-codex/src/adapter.rs | [/functional_chains/11/pattern/sequences](winwincode-automatic-report.json#/functional_chains/11/pattern/sequences) |
| sequences/submission/assignment_attempts/0/left/location/line | 3539 | [/functional_chains/11/pattern/sequences](winwincode-automatic-report.json#/functional_chains/11/pattern/sequences) |
| sequences/submission/assignment_attempts/0/left/location/column | 25 | [/functional_chains/11/pattern/sequences](winwincode-automatic-report.json#/functional_chains/11/pattern/sequences) |

完整关系 [/functional_chains/11/pattern](winwincode-automatic-report.json#/functional_chains/11/pattern)；原 source facts [/functional_chains/11/source_facts](winwincode-automatic-report.json#/functional_chains/11/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### Worker 与 Adapter 的消息身份 · `wwc-report-worker-adapter-record-identities`

`message_identity_relations`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`476c604a9cc207b991b654d1`；Evidence=`1f2c773a6c7d0ed56f559e71`。
源码/关系 [/functional_chains/12](winwincode-automatic-report.json#/functional_chains/12)；缺段 [/functional_chains/12/analysis_gaps](winwincode-automatic-report.json#/functional_chains/12/analysis_gaps)；模型 [/functional_chains/12/trusted_models](winwincode-automatic-report.json#/functional_chains/12/trusted_models)；policy [/functional_chains/12/policy_declarations](winwincode-automatic-report.json#/functional_chains/12/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| budget/incomplete | false | [/functional_chains/12/pattern/budget](winwincode-automatic-report.json#/functional_chains/12/pattern/budget) |
| budget/limit | 65536 | [/functional_chains/12/pattern/budget](winwincode-automatic-report.json#/functional_chains/12/pattern/budget) |
| budget/operations | 3619 | [/functional_chains/12/pattern/budget](winwincode-automatic-report.json#/functional_chains/12/pattern/budget) |
| components/worker_adapter_identity/all_profile_settings_fully_traced | false | [/functional_chains/12/pattern/components](winwincode-automatic-report.json#/functional_chains/12/pattern/components) |
| components/worker_adapter_identity/all_worker_messages_covered | false | [/functional_chains/12/pattern/components](winwincode-automatic-report.json#/functional_chains/12/pattern/components) |
| components/worker_adapter_identity/authority_and_result_values_proven | false | [/functional_chains/12/pattern/components](winwincode-automatic-report.json#/functional_chains/12/pattern/components) |
| components/worker_adapter_identity/execution_profile_projection_to_selected_consumer_only | true | [/functional_chains/12/pattern/components](winwincode-automatic-report.json#/functional_chains/12/pattern/components) |
| components/worker_adapter_identity/generic_codex_receiver_globally_bound | false | [/functional_chains/12/pattern/components](winwincode-automatic-report.json#/functional_chains/12/pattern/components) |
| components/worker_adapter_identity/kernel_session_equals_product_or_worker_session | false | [/functional_chains/12/pattern/components](winwincode-automatic-report.json#/functional_chains/12/pattern/components) |
| components/worker_adapter_identity/scope | captured typed JobDispatch arm, explicit borrowed start record, selected adapter run and Kernel session/turn interfaces | [/functional_chains/12/pattern/components](winwincode-automatic-report.json#/functional_chains/12/pattern/components) |
| components/worker_adapter_identity/supported | true | [/functional_chains/12/pattern/components](winwincode-automatic-report.json#/functional_chains/12/pattern/components) |
| components/worker_adapter_identity/components/adapter_ensure_thread/supported | true | [/functional_chains/12/pattern/components](winwincode-automatic-report.json#/functional_chains/12/pattern/components) |
| components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/shown_items/0/creates_calls_edge | false | [/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections](winwincode-automatic-report.json#/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections) |
| components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/shown_items/0/extractor_version | captured-message-identity-relations-1 | [/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections](winwincode-automatic-report.json#/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections) |
| components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/shown_items/0/field | lease | [/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections](winwincode-automatic-report.json#/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections) |
| components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/shown_items/0/id | f2284014deea7a05deb92f5f | [/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections](winwincode-automatic-report.json#/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections) |
| components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/shown_items/0/kind | message_record_field_projection | [/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections](winwincode-automatic-report.json#/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections) |
| components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/shown_items/0/ordinary_generated_record_clone_model_required | true | [/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections](winwincode-automatic-report.json#/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections) |
| components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/shown_items/0/origin | source-derived | [/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections](winwincode-automatic-report.json#/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections) |
| components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/shown_items/0/record_type_source | ModelLeaseAuthority | [/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections](winwincode-automatic-report.json#/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections) |
| components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/shown_items/0/role | adapter_ensure_thread | [/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections](winwincode-automatic-report.json#/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections) |
| components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/shown_items/0/target_code_executed | false | [/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections](winwincode-automatic-report.json#/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections) |
| components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/shown_items/0/location/file | crates/winwincode-codex/src/adapter.rs | [/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections](winwincode-automatic-report.json#/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections) |
| components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/shown_items/0/location/line | 3378 | [/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections](winwincode-automatic-report.json#/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections) |

完整关系 [/functional_chains/12/pattern](winwincode-automatic-report.json#/functional_chains/12/pattern)；原 source facts [/functional_chains/12/source_facts](winwincode-automatic-report.json#/functional_chains/12/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### Worker 入口分支 · `wwc-report-worker-bootstrap-entries`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`04ee83bf9ca6e6b33b2656d6`；Evidence=`9df4cf4113207a99c88623ae`。
源码/关系 [/functional_chains/13](winwincode-automatic-report.json#/functional_chains/13)；缺段 [/functional_chains/13/analysis_gaps](winwincode-automatic-report.json#/functional_chains/13/analysis_gaps)；模型 [/functional_chains/13/trusted_models](winwincode-automatic-report.json#/functional_chains/13/trusted_models)；policy [/functional_chains/13/policy_declarations](winwincode-automatic-report.json#/functional_chains/13/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/13/pattern/scoped_source_supported](winwincode-automatic-report.json#/functional_chains/13/pattern/scoped_source_supported) |
| sequences/entry/all_function_paths_or_effects_accounted | false | [/functional_chains/13/pattern/sequences](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/entry/future_or_callback_activation_proven | false | [/functional_chains/13/pattern/sequences](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/entry/region_kind | function_item | [/functional_chains/13/pattern/sequences](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/entry/role | entry | [/functional_chains/13/pattern/sequences](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/entry/orders/0/after_step_id | f855d8faeed6db98f32e895e | [/functional_chains/13/pattern/sequences](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/entry/orders/0/all_paths_reach_next_proven | false | [/functional_chains/13/pattern/sequences](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/entry/orders/0/before_step_id | 84db448869e8ab3a3b5ebc7a | [/functional_chains/13/pattern/sequences](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/entry/orders/0/id | 265b4b63d5cc2b515a588ae5 | [/functional_chains/13/pattern/sequences](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/entry/orders/0/kind | conditional_direct_statement_order | [/functional_chains/13/pattern/sequences](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/entry/orders/0/model_id | captured-normal-statement-control-v1 | [/functional_chains/13/pattern/sequences](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/entry/orders/0/origin | source-derived | [/functional_chains/13/pattern/sequences](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/entry/orders/0/role | entry | [/functional_chains/13/pattern/sequences](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/entry/orders/0/conditions/0 | both direct statements normally reached in the same invocation | [/functional_chains/13/pattern/sequences](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/entry/orders/0/conditions/1 | preceding asynchronous operations complete normally; no claim of completion or whole-program dominance | [/functional_chains/13/pattern/sequences](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/entry/orders/0/location/file | crates/winwincode-worker/src/main.rs | [/functional_chains/13/pattern/sequences](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/entry/orders/0/location/line | 36 | [/functional_chains/13/pattern/sequences](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/entry/orders/0/location/column | 5 | [/functional_chains/13/pattern/sequences](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/entry/orders/0/location/end_line | 49 | [/functional_chains/13/pattern/sequences](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/entry/orders/0/location/start_byte | 1408 | [/functional_chains/13/pattern/sequences](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/entry/orders/0/location/end_byte | 1968 | [/functional_chains/13/pattern/sequences](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/entry/source_region_location/file | crates/winwincode-worker/src/main.rs | [/functional_chains/13/pattern/sequences](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/entry/source_region_location/line | 34 | [/functional_chains/13/pattern/sequences](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences) |
| sequences/entry/source_region_location/column | 1 | [/functional_chains/13/pattern/sequences](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences) |

完整关系 [/functional_chains/13/pattern](winwincode-automatic-report.json#/functional_chains/13/pattern)；原 source facts [/functional_chains/13/source_facts](winwincode-automatic-report.json#/functional_chains/13/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### 生产 Worker 构造 · `wwc-report-worker-production-construction`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`ffa5234d6efa3458bf87eb4d`；Evidence=`3f0ada51f2258a0c6ef4e8d8`。
源码/关系 [/functional_chains/14](winwincode-automatic-report.json#/functional_chains/14)；缺段 [/functional_chains/14/analysis_gaps](winwincode-automatic-report.json#/functional_chains/14/analysis_gaps)；模型 [/functional_chains/14/trusted_models](winwincode-automatic-report.json#/functional_chains/14/trusted_models)；policy [/functional_chains/14/policy_declarations](winwincode-automatic-report.json#/functional_chains/14/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/14/pattern/scoped_source_supported](winwincode-automatic-report.json#/functional_chains/14/pattern/scoped_source_supported) |
| sequences/adapter_factory/all_function_paths_or_effects_accounted | false | [/functional_chains/14/pattern/sequences](winwincode-automatic-report.json#/functional_chains/14/pattern/sequences) |
| sequences/adapter_factory/future_or_callback_activation_proven | false | [/functional_chains/14/pattern/sequences](winwincode-automatic-report.json#/functional_chains/14/pattern/sequences) |
| sequences/adapter_factory/region_kind | function_item | [/functional_chains/14/pattern/sequences](winwincode-automatic-report.json#/functional_chains/14/pattern/sequences) |
| sequences/adapter_factory/role | adapter_factory | [/functional_chains/14/pattern/sequences](winwincode-automatic-report.json#/functional_chains/14/pattern/sequences) |
| sequences/adapter_factory/orders/shown_items/0/after_step_id | 8c1ecd3ca350be13b4ee01bc | [/functional_chains/14/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/14/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/all_paths_reach_next_proven | false | [/functional_chains/14/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/14/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/before_step_id | d9d40a2fc0db59cda153ef67 | [/functional_chains/14/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/14/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/id | 88d16950f471d8b99dc2a9de | [/functional_chains/14/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/14/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/kind | conditional_direct_statement_order | [/functional_chains/14/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/14/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/model_id | captured-normal-statement-control-v1 | [/functional_chains/14/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/14/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/origin | source-derived | [/functional_chains/14/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/14/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/role | adapter_factory | [/functional_chains/14/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/14/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/conditions/0 | both direct statements normally reached in the same invocation | [/functional_chains/14/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/14/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/conditions/1 | preceding asynchronous operations complete normally; no claim of completion or whole-program dominance | [/functional_chains/14/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/14/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/location/file | crates/winwincode-worker/src/main.rs | [/functional_chains/14/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/14/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/location/line | 326 | [/functional_chains/14/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/14/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/location/column | 5 | [/functional_chains/14/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/14/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/location/end_line | 326 | [/functional_chains/14/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/14/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/location/start_byte | 13491 | [/functional_chains/14/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/14/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/location/end_byte | 13571 | [/functional_chains/14/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/14/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/1/after_step_id | 79770f8af7282f716af88112 | [/functional_chains/14/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/14/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/1/all_paths_reach_next_proven | false | [/functional_chains/14/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/14/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/1/before_step_id | 8c1ecd3ca350be13b4ee01bc | [/functional_chains/14/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/14/pattern/sequences/adapter_factory/orders) |

完整关系 [/functional_chains/14/pattern](winwincode-automatic-report.json#/functional_chains/14/pattern)；原 source facts [/functional_chains/14/source_facts](winwincode-automatic-report.json#/functional_chains/14/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### Worker typed dispatch · `wwc-report-worker-typed-dispatch`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`9c163d82a20d8ba9656b1e41`；Evidence=`fe08b74d4164f6e85a7e1847`。
源码/关系 [/functional_chains/15](winwincode-automatic-report.json#/functional_chains/15)；缺段 [/functional_chains/15/analysis_gaps](winwincode-automatic-report.json#/functional_chains/15/analysis_gaps)；模型 [/functional_chains/15/trusted_models](winwincode-automatic-report.json#/functional_chains/15/trusted_models)；policy [/functional_chains/15/policy_declarations](winwincode-automatic-report.json#/functional_chains/15/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/15/pattern/scoped_source_supported](winwincode-automatic-report.json#/functional_chains/15/pattern/scoped_source_supported) |
| sequences/control/all_function_paths_or_effects_accounted | false | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/control/future_or_callback_activation_proven | false | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/control/region_kind | function_item | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/control/role | control | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/control/conditions/0/id | 2928b890106a9da4612f7a8b | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/control/conditions/0/kind | source_guard_and_abrupt_branch | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/control/conditions/0/origin | source-derived | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/control/conditions/0/role | control | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/control/conditions/0/runtime_predicate_proven | false | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/control/conditions/0/branch_context/0/activation_proven | false | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/control/conditions/0/branch_context/0/kind | match_arm | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/control/conditions/0/branch_context/0/location/file | crates/winwincode-worker/src/lib.rs | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/control/conditions/0/branch_context/0/location/line | 771 | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/control/conditions/0/branch_context/0/location/column | 13 | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/control/conditions/0/branch_context/0/location/end_line | 827 | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/control/conditions/0/branch_context/0/location/start_byte | 30873 | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/control/conditions/0/branch_context/0/location/end_byte | 33570 | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/control/conditions/0/branches/0/branch | then | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/control/conditions/0/branches/0/branch_all_paths_abrupt_proven | true | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/control/conditions/0/branches/0/abrupt_source_expressions/0/kind | return_expression | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/control/conditions/0/branches/0/abrupt_source_expressions/0/runtime_completion_proven | false | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/control/conditions/0/branches/0/abrupt_source_expressions/0/location/file | crates/winwincode-worker/src/lib.rs | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/control/conditions/0/branches/0/abrupt_source_expressions/0/location/line | 777 | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |

完整关系 [/functional_chains/15/pattern](winwincode-automatic-report.json#/functional_chains/15/pattern)；原 source facts [/functional_chains/15/source_facts](winwincode-automatic-report.json#/functional_chains/15/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### WorkRun 可运行状态与依赖条件 · `wwc-report-workrun-finite-selection`

`rust_finite_state_selection`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`ca3bbdf71c845333fe640b2e`；Evidence=`ddcf0a91c7456da988fdbe75`。
源码/关系 [/functional_chains/16](winwincode-automatic-report.json#/functional_chains/16)；缺段 [/functional_chains/16/analysis_gaps](winwincode-automatic-report.json#/functional_chains/16/analysis_gaps)；模型 [/functional_chains/16/trusted_models](winwincode-automatic-report.json#/functional_chains/16/trusted_models)；policy [/functional_chains/16/policy_declarations](winwincode-automatic-report.json#/functional_chains/16/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

`rows`；完整 [/functional_chains/16/pattern/finite_effective_state_relation/rows](winwincode-automatic-report.json#/functional_chains/16/pattern/finite_effective_state_relation/rows)；保存总行数 `8`。

| effective_state | input_state | runnable | source_quantifiers | 完整行 |
| --- | --- | --- | --- | --- |
| WorkItemState::Done | WorkItemState::Done | false | {"source_quantifier_1":false} | [/functional_chains/16/pattern/finite_effective_state_relation/rows/0](winwincode-automatic-report.json#/functional_chains/16/pattern/finite_effective_state_relation/rows/0) |
| WorkItemState::Done | WorkItemState::Done | false | {"source_quantifier_1":true} | [/functional_chains/16/pattern/finite_effective_state_relation/rows/1](winwincode-automatic-report.json#/functional_chains/16/pattern/finite_effective_state_relation/rows/1) |
| WorkItemState::Ready | WorkItemState::Ready | true | {"source_quantifier_1":false} | [/functional_chains/16/pattern/finite_effective_state_relation/rows/2](winwincode-automatic-report.json#/functional_chains/16/pattern/finite_effective_state_relation/rows/2) |
| WorkItemState::WaitingDependency | WorkItemState::Ready | false | {"source_quantifier_1":true} | [/functional_chains/16/pattern/finite_effective_state_relation/rows/3](winwincode-automatic-report.json#/functional_chains/16/pattern/finite_effective_state_relation/rows/3) |
| WorkItemState::Ready | WorkItemState::WaitingDependency | true | {"source_quantifier_1":false} | [/functional_chains/16/pattern/finite_effective_state_relation/rows/4](winwincode-automatic-report.json#/functional_chains/16/pattern/finite_effective_state_relation/rows/4) |
| WorkItemState::WaitingDependency | WorkItemState::WaitingDependency | false | {"source_quantifier_1":true} | [/functional_chains/16/pattern/finite_effective_state_relation/rows/5](winwincode-automatic-report.json#/functional_chains/16/pattern/finite_effective_state_relation/rows/5) |
| <other value of this state enum> | <other value of this state enum> | false | {"source_quantifier_1":false} | [/functional_chains/16/pattern/finite_effective_state_relation/rows/6](winwincode-automatic-report.json#/functional_chains/16/pattern/finite_effective_state_relation/rows/6) |
| <other value of this state enum> | <other value of this state enum> | false | {"source_quantifier_1":true} | [/functional_chains/16/pattern/finite_effective_state_relation/rows/7](winwincode-automatic-report.json#/functional_chains/16/pattern/finite_effective_state_relation/rows/7) |

`non_runnable_table_rows`；完整 [/functional_chains/16/pattern/finite_source_countercases/non_runnable_table_rows](winwincode-automatic-report.json#/functional_chains/16/pattern/finite_source_countercases/non_runnable_table_rows)；保存总行数 `6`。

| effective_state | input_state | runnable | source_quantifiers | 完整行 |
| --- | --- | --- | --- | --- |
| WorkItemState::Done | WorkItemState::Done | false | {"source_quantifier_1":false} | [/functional_chains/16/pattern/finite_source_countercases/non_runnable_table_rows/0](winwincode-automatic-report.json#/functional_chains/16/pattern/finite_source_countercases/non_runnable_table_rows/0) |
| WorkItemState::Done | WorkItemState::Done | false | {"source_quantifier_1":true} | [/functional_chains/16/pattern/finite_source_countercases/non_runnable_table_rows/1](winwincode-automatic-report.json#/functional_chains/16/pattern/finite_source_countercases/non_runnable_table_rows/1) |
| WorkItemState::WaitingDependency | WorkItemState::Ready | false | {"source_quantifier_1":true} | [/functional_chains/16/pattern/finite_source_countercases/non_runnable_table_rows/2](winwincode-automatic-report.json#/functional_chains/16/pattern/finite_source_countercases/non_runnable_table_rows/2) |
| WorkItemState::WaitingDependency | WorkItemState::WaitingDependency | false | {"source_quantifier_1":true} | [/functional_chains/16/pattern/finite_source_countercases/non_runnable_table_rows/3](winwincode-automatic-report.json#/functional_chains/16/pattern/finite_source_countercases/non_runnable_table_rows/3) |
| <other value of this state enum> | <other value of this state enum> | false | {"source_quantifier_1":false} | [/functional_chains/16/pattern/finite_source_countercases/non_runnable_table_rows/4](winwincode-automatic-report.json#/functional_chains/16/pattern/finite_source_countercases/non_runnable_table_rows/4) |
| <other value of this state enum> | <other value of this state enum> | false | {"source_quantifier_1":true} | [/functional_chains/16/pattern/finite_source_countercases/non_runnable_table_rows/5](winwincode-automatic-report.json#/functional_chains/16/pattern/finite_source_countercases/non_runnable_table_rows/5) |

`runnable_table_rows`；完整 [/functional_chains/16/pattern/finite_source_countercases/runnable_table_rows](winwincode-automatic-report.json#/functional_chains/16/pattern/finite_source_countercases/runnable_table_rows)；保存总行数 `2`。

| effective_state | input_state | runnable | source_quantifiers | 完整行 |
| --- | --- | --- | --- | --- |
| WorkItemState::Ready | WorkItemState::Ready | true | {"source_quantifier_1":false} | [/functional_chains/16/pattern/finite_source_countercases/runnable_table_rows/0](winwincode-automatic-report.json#/functional_chains/16/pattern/finite_source_countercases/runnable_table_rows/0) |
| WorkItemState::Ready | WorkItemState::WaitingDependency | true | {"source_quantifier_1":false} | [/functional_chains/16/pattern/finite_source_countercases/runnable_table_rows/1](winwincode-automatic-report.json#/functional_chains/16/pattern/finite_source_countercases/runnable_table_rows/1) |

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| all_active_states_or_attempts_proven | false | [/functional_chains/16/pattern/all_active_states_or_attempts_proven](winwincode-automatic-report.json#/functional_chains/16/pattern/all_active_states_or_attempts_proven) |
| boundaries/0 | source-mentioned enum alternatives and a symbolic complement are interpreted; no complete enum declaration or arbitrary macro expansion is inferred | [/functional_chains/16/pattern/boundaries](winwincode-automatic-report.json#/functional_chains/16/pattern/boundaries) |
| boundaries/1 | quantifiers describe current captured predicates; concrete item records, dependency truth and actual active runs are unknown | [/functional_chains/16/pattern/boundaries](winwincode-automatic-report.json#/functional_chains/16/pattern/boundaries) |
| boundaries/2 | selection does not prove persistence, scheduling fairness, concurrency isolation, all state transitions or every attempt identity | [/functional_chains/16/pattern/boundaries](winwincode-automatic-report.json#/functional_chains/16/pattern/boundaries) |
| dependency_blocker_relation/supported | true | [/functional_chains/16/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/16/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/actual_dependencies_or_reachability_evaluated | false | [/functional_chains/16/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/16/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/empty_dependency_collection_result | false | [/functional_chains/16/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/16/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/finite_state_component | captured-rust-finite-state-relations-1 | [/functional_chains/16/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/16/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/id | 45b1c2a354c3b89a85844a5c | [/functional_chains/16/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/16/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/kind | rust_finite_dependency_blocker_relation | [/functional_chains/16/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/16/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/origin | source-derived | [/functional_chains/16/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/16/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/quantifier | exists dependency for which no equal-identity candidate has the captured required state | [/functional_chains/16/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/16/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/role | effective_state | [/functional_chains/16/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/16/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/candidate_collection/kind | name | [/functional_chains/16/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/16/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/candidate_collection/name | items | [/functional_chains/16/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/16/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/candidate_collection/span/0 | 23876 | [/functional_chains/16/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/16/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/candidate_collection/span/1 | 23881 | [/functional_chains/16/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/16/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/dependency_collection/field | depends_on | [/functional_chains/16/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/16/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/dependency_collection/kind | field | [/functional_chains/16/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/16/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/dependency_collection/span/0 | 23825 | [/functional_chains/16/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/16/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/dependency_collection/span/1 | 23840 | [/functional_chains/16/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/16/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/dependency_collection/value/kind | name | [/functional_chains/16/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/16/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/dependency_collection/value/name | item | [/functional_chains/16/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/16/pattern/dependency_blocker_relation) |
| dependency_blocker_relation/relations/0/dependency_collection/value/span/0 | 23825 | [/functional_chains/16/pattern/dependency_blocker_relation](winwincode-automatic-report.json#/functional_chains/16/pattern/dependency_blocker_relation) |

完整关系 [/functional_chains/16/pattern](winwincode-automatic-report.json#/functional_chains/16/pattern)；原 source facts [/functional_chains/16/source_facts](winwincode-automatic-report.json#/functional_chains/16/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### WorkRun 校验与重复 guard · `wwc-report-workrun-state-guards`

`state_guard_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`iterator_selection_and_macro_runtime_semantics_not_fully_proven`；Finding=`0ff85dbba15ccb39ada4a775`；Evidence=`df35191414060797f247176d`。
源码/关系 [/functional_chains/17](winwincode-automatic-report.json#/functional_chains/17)；缺段 [/functional_chains/17/analysis_gaps](winwincode-automatic-report.json#/functional_chains/17/analysis_gaps)；模型 [/functional_chains/17/trusted_models](winwincode-automatic-report.json#/functional_chains/17/trusted_models)；policy [/functional_chains/17/policy_declarations](winwincode-automatic-report.json#/functional_chains/17/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| all_active_states_or_attempts_proven | false | [/functional_chains/17/pattern/all_active_states_or_attempts_proven](winwincode-automatic-report.json#/functional_chains/17/pattern/all_active_states_or_attempts_proven) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/0/call_fact_id | 855b44866e7a3bb46e68f8fc | [/functional_chains/17/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/17/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/0/role | selection | [/functional_chains/17/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/17/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/0/location/file | crates/winwincode-delivery/src/application/workrun.rs | [/functional_chains/17/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/17/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/0/location/line | 392 | [/functional_chains/17/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/17/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/0/location/column | 9 | [/functional_chains/17/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/17/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/0/location/end_line | 392 | [/functional_chains/17/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/17/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/0/location/start_byte | 14655 | [/functional_chains/17/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/17/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/0/location/end_byte | 14670 | [/functional_chains/17/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/17/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/1/call_fact_id | 00566343142225ed3672799c | [/functional_chains/17/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/17/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/1/role | start | [/functional_chains/17/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/17/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/1/location/file | crates/winwincode-delivery/src/application/workrun.rs | [/functional_chains/17/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/17/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/1/location/line | 419 | [/functional_chains/17/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/17/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/1/location/column | 9 | [/functional_chains/17/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/17/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/1/location/end_line | 419 | [/functional_chains/17/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/17/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/1/location/start_byte | 15641 | [/functional_chains/17/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/17/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/1/location/end_byte | 15656 | [/functional_chains/17/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/17/pattern/repeated_first_callee) |
| scoped_source_supported | true | [/functional_chains/17/pattern/scoped_source_supported](winwincode-automatic-report.json#/functional_chains/17/pattern/scoped_source_supported) |
| selection_predicate_sources/shown_items/0/callback_activation_proven | false | [/functional_chains/17/pattern/selection_predicate_sources](winwincode-automatic-report.json#/functional_chains/17/pattern/selection_predicate_sources) |
| selection_predicate_sources/shown_items/0/id | 994002f9fe93f897c9751421 | [/functional_chains/17/pattern/selection_predicate_sources](winwincode-automatic-report.json#/functional_chains/17/pattern/selection_predicate_sources) |
| selection_predicate_sources/shown_items/0/kind | state_selection_predicate_source | [/functional_chains/17/pattern/selection_predicate_sources](winwincode-automatic-report.json#/functional_chains/17/pattern/selection_predicate_sources) |
| selection_predicate_sources/shown_items/0/macro_expansion_or_iterator_effects_proven | false | [/functional_chains/17/pattern/selection_predicate_sources](winwincode-automatic-report.json#/functional_chains/17/pattern/selection_predicate_sources) |
| selection_predicate_sources/shown_items/0/nested_predicate_callable | true | [/functional_chains/17/pattern/selection_predicate_sources](winwincode-automatic-report.json#/functional_chains/17/pattern/selection_predicate_sources) |
| selection_predicate_sources/shown_items/0/origin | source-derived | [/functional_chains/17/pattern/selection_predicate_sources](winwincode-automatic-report.json#/functional_chains/17/pattern/selection_predicate_sources) |

完整关系 [/functional_chains/17/pattern](winwincode-automatic-report.json#/functional_chains/17/pattern)；原 source facts [/functional_chains/17/source_facts](winwincode-automatic-report.json#/functional_chains/17/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

## 未解析与未审边界

- 全文复现声明：`false`；未建模功能域不视为已覆盖：`true`。
- 局部配置评估 `2` 条；重复源选择 `1` 组，见 [/overlapping_source_selections](winwincode-automatic-report.json#/overlapping_source_selections)，不合计为新增覆盖。
- 保存诊断 `165`；文件缺口见 [/coverage/unparsed_files](winwincode-automatic-report.json#/coverage/unparsed_files)，诊断见 [/diagnostics](winwincode-automatic-report.json#/diagnostics)。
- 源码排除规则：`[".git",".beads",".agents",".codex",".callscope",".analysis-tools",".venv","venv","__pycache__","node_modules","target","dist","build","coverage","third_party","upstream","vendor","generated","tests","test","__tests__","examples","scripts","crates/winwincode-test-assets","**/*.test.ts","**/*.test.tsx","**/*.spec.ts","**/*.spec.tsx","**/*.generated.ts","**/generated.rs","**/*_tests.rs","**/test_support.rs","**/build.rs"]`。
- 标准模型、正常到达和生产装配条件只按各项保存范围成立；未知字段/分派、特殊语言语义及任意并发不被摘要补齐。
- 嵌套 async/callback 的源码正文不是执行轨迹；候选方法不是已验证 runtime provider。
- 保存 target_executed=`false` / target_tests_run=`false` / target_build_run=`false` / runtime_functionality_verified=`false`。
- 上方 `#/...` 为 JSON Pointer 导航；查看器若不支持该 fragment，请在原 JSON 按指针定位。指针与 Finding/Evidence 身份应一起阅读。

## 正式保存轮次

| 轮次 | 保存状态 | 新建快照 | 相同快照 ID |
| --- | --- | --- |
| `cold` | `partial` | `true` | `cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2` |
| `warm` | `partial` | `false` | `cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2` |

这张表复制保存发布记录；partial 是图/解析范围状态，不能据此覆盖上方判断结论。完整记录见 [integration](winwincode-integration.json)。
