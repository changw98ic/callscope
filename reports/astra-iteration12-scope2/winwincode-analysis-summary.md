# WinWinCode · 保存的自动分析摘要

此摘要只展示已保存正式报告的结果和证据导航；不重新分析、不新增评价，也不替代完整证据。
五项判断是实现追踪，不是全文报告或项目功能覆盖率。链标题只是规则 ID 的展示标签。

- 固定全文基准：[原分析报告](../astra-baseline/WINWINCODE_ANALYSIS.md)；不设置重复 Astra 审批步骤。
- 完整自动报告：[Markdown](winwincode-automatic-report.md) / [JSON](winwincode-automatic-report.json)；[正式 integration](winwincode-integration.json)。
- 快照：`cc327a390837a897be93cdd4bdd4d9ad652c47f70f0b0dbfbbf89a52b463d372`；状态：`partial`；报告版本：`captured-project-analysis-report-3`。
- 实现：`0.14.0` / `static-multilang-14` / `call-rules-13-architecture-explanations`。
- 源码身份：`eb8e7cae7c2cd2b0503495033cc9a2a98c6e16b3d54b5a2f95dbdca24d118ab2`。
- 策略身份：`47aa40e4904639bec88bb3d5b74cd7ebb69954bab81a3ff93dda81b959603499`。
- 保存 JSON SHA256：`65312658d7c9adc0cfbb8feb98af35b13791c03ba0466d6c3f3e149c74751cb1`；integration SHA256：`df8ea8684b5de5b142fa129bef9587153c126082cb13d83c62150af8fa89a6f8`。
- 保存比较范围：v13 and v14 both use full frontend/detector recomputation. New source/doc scope, models, policies and architecture explanations can change identity; no same-policy precision or performance comparison is claimed.

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
Finding=`27ca18396beeb47bea36a628`；Evidence=`b53ade9dca10d93c45a94cc1`；保存 evidence 指针=`/evidence/0/details`（相对于该 Finding）。
完整 [/judgments/0](winwincode-automatic-report.json#/judgments/0)；条件 [/judgments/0/conditions](winwincode-automatic-report.json#/judgments/0/conditions)；反证 [/judgments/0/refutations](winwincode-automatic-report.json#/judgments/0/refutations)；缺口 [/judgments/0/necessary_gaps](winwincode-automatic-report.json#/judgments/0/necessary_gaps)。

### `WWC-02`

所选提交对象遗漏条件分支必填字段；经过生成协议、普通 JSON 与 Serde 映射后，权威非空守卫在使用或提交前拒绝。其它分支和显式字段来源是反证。

derived_judgment：`"Under the explicitly retained normal production, JSON/Serde and active Device conditions, the closed UI command field omission reaches None and the nonblank authority guard rejects before criterion use/commit."`
assessment=`scoped_static_judgment_reproduced`；complete=`true`；support=`true`。
必要义务（原状态）：`D1=supported, D2=supported, D3=supported, D4=supported, D5=supported`；必要缺口：`[]`。
Finding=`547f718f81cb530068c86aef`；Evidence=`d7a8c3f23d4c857eb2c19799`；保存 evidence 指针=`/evidence/0/details`（相对于该 Finding）。
完整 [/judgments/1](winwincode-automatic-report.json#/judgments/1)；条件 [/judgments/1/conditions](winwincode-automatic-report.json#/judgments/1/conditions)；反证 [/judgments/1/refutations](winwincode-automatic-report.json#/judgments/1/refutations)；缺口 [/judgments/1/necessary_gaps](winwincode-automatic-report.json#/judgments/1/necessary_gaps)。

## 所选主要源码链

显示每条保存规则的实际 assessment 和缺口；source-structure 支持与目标分派闭合分开。

### 渲染代次与异步回写条件 · `wwc-browser-continuation-lifecycle`

`browser_async_lifecycle`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`cba5af4fec0e40bdd4f77d2f`；Evidence=`db64c471a53658ecf6591799`。
源码/关系 [/functional_chains/0](winwincode-automatic-report.json#/functional_chains/0)；缺段 [/functional_chains/0/analysis_gaps](winwincode-automatic-report.json#/functional_chains/0/analysis_gaps)；模型 [/functional_chains/0/trusted_models](winwincode-automatic-report.json#/functional_chains/0/trusted_models)；policy [/functional_chains/0/policy_declarations](winwincode-automatic-report.json#/functional_chains/0/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

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

### WinWinCode 记录与资源写者 · `wwc-captured-record-resource-writers`

`resource_writer_ownership`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`dd33866bcd25385a8792a37d`；Evidence=`b5f822ca48f27831106b96db`。
源码/关系 [/functional_chains/1](winwincode-automatic-report.json#/functional_chains/1)；缺段 [/functional_chains/1/analysis_gaps](winwincode-automatic-report.json#/functional_chains/1/analysis_gaps)；模型 [/functional_chains/1/trusted_models](winwincode-automatic-report.json#/functional_chains/1/trusted_models)；policy [/functional_chains/1/policy_declarations](winwincode-automatic-report.json#/functional_chains/1/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

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

### wwc-delivery-evidence-frozen-contract-slice · `wwc-delivery-evidence-frozen-contract-slice`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`12d0ebaf619479cb00cfc62b`；Evidence=`7bbe89b3f3de8e36ecf6769a`。
源码/关系 [/functional_chains/2](winwincode-automatic-report.json#/functional_chains/2)；缺段 [/functional_chains/2/analysis_gaps](winwincode-automatic-report.json#/functional_chains/2/analysis_gaps)；模型 [/functional_chains/2/trusted_models](winwincode-automatic-report.json#/functional_chains/2/trusted_models)；policy [/functional_chains/2/policy_declarations](winwincode-automatic-report.json#/functional_chains/2/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/2/pattern/scoped_source_supported](winwincode-automatic-report.json#/functional_chains/2/pattern/scoped_source_supported) |
| sequences/checkout_guard/conditions/0/condition/kind | binary_expression | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/checkout_guard/conditions/0/condition/location/file | crates/winwincode-delivery/src/domain/evidence.rs | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/checkout_guard/conditions/0/condition/location/line | 903 | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/checkout_guard/conditions/0/condition/location/column | 8 | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/checkout_guard/conditions/0/condition/location/end_line | 903 | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/checkout_guard/conditions/0/condition/location/start_byte | 32298 | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/checkout_guard/conditions/0/condition/location/end_byte | 32347 | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/checkout_guard/conditions/0/condition/operands/0/call_effects_or_result_proven | false | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/checkout_guard/conditions/0/condition/operands/0/arguments/0/kind | 显示投影省略 | [/functional_chains/2/pattern/sequences/checkout_guard/conditions/0/condition/operands/0/arguments/0/kind](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences/checkout_guard/conditions/0/condition/operands/0/arguments/0/kind) |
| sequences/checkout_guard/conditions/0/condition/operands/0/arguments/0/location | 显示投影省略 | [/functional_chains/2/pattern/sequences/checkout_guard/conditions/0/condition/operands/0/arguments/0/location](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences/checkout_guard/conditions/0/condition/operands/0/arguments/0/location) |
| sequences/checkout_guard/conditions/0/condition/operands/0/arguments/0/name | 显示投影省略 | [/functional_chains/2/pattern/sequences/checkout_guard/conditions/0/condition/operands/0/arguments/0/name](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences/checkout_guard/conditions/0/condition/operands/0/arguments/0/name) |
| sequences/checkout_guard/conditions/0/condition/operands/0/callee_expression/kind | identifier | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/checkout_guard/conditions/0/condition/operands/0/callee_expression/location/file | crates/winwincode-delivery/src/domain/evidence.rs | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/checkout_guard/conditions/0/condition/operands/0/callee_expression/location/line | 903 | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/checkout_guard/conditions/0/condition/operands/0/callee_expression/location/column | 8 | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/checkout_guard/conditions/0/condition/operands/0/callee_expression/location/end_line | 903 | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/checkout_guard/conditions/0/condition/operands/0/callee_expression/location/start_byte | 32298 | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/checkout_guard/conditions/0/condition/operands/0/callee_expression/location/end_byte | 32315 | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/checkout_guard/conditions/0/condition/operands/0/callee_expression/name | checkout_identity | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/checkout_guard/conditions/0/condition/operands/0/callee_source | checkout_identity | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/checkout_guard/conditions/0/condition/operands/0/kind | call_expression | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/checkout_guard/conditions/0/condition/operands/0/location/file | crates/winwincode-delivery/src/domain/evidence.rs | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |
| sequences/checkout_guard/conditions/0/condition/operands/0/location/line | 903 | [/functional_chains/2/pattern/sequences](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences) |

完整关系 [/functional_chains/2/pattern](winwincode-automatic-report.json#/functional_chains/2/pattern)；原 source facts [/functional_chains/2/source_facts](winwincode-automatic-report.json#/functional_chains/2/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### Provider 文档与部署范围比较 · `wwc-document-device-provider-deployment-scope`

`document_deployment_consistency`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`1014da044f38227217dcb6b9`；Evidence=`9fd9277990396cd65116dfd6`。
源码/关系 [/functional_chains/3](winwincode-automatic-report.json#/functional_chains/3)；缺段 [/functional_chains/3/analysis_gaps](winwincode-automatic-report.json#/functional_chains/3/analysis_gaps)；模型 [/functional_chains/3/trusted_models](winwincode-automatic-report.json#/functional_chains/3/trusted_models)；policy [/functional_chains/3/policy_declarations](winwincode-automatic-report.json#/functional_chains/3/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

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

### Adapter durable / exact turn · `wwc-report-adapter-durable-exact-turn`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`884dfadd2ea90efdd48367ed`；Evidence=`73b06b779a5f39046a5dbf74`。
源码/关系 [/functional_chains/4](winwincode-automatic-report.json#/functional_chains/4)；缺段 [/functional_chains/4/analysis_gaps](winwincode-automatic-report.json#/functional_chains/4/analysis_gaps)；模型 [/functional_chains/4/trusted_models](winwincode-automatic-report.json#/functional_chains/4/trusted_models)；policy [/functional_chains/4/policy_declarations](winwincode-automatic-report.json#/functional_chains/4/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/4/pattern/scoped_source_supported](winwincode-automatic-report.json#/functional_chains/4/pattern/scoped_source_supported) |
| sequences/adapter_submit/conditions/shown_items/0/condition/kind | binary_expression | [/functional_chains/4/pattern/sequences/adapter_submit/conditions](winwincode-automatic-report.json#/functional_chains/4/pattern/sequences/adapter_submit/conditions) |
| sequences/adapter_submit/conditions/shown_items/0/condition/location/file | crates/winwincode-codex/src/adapter.rs | [/functional_chains/4/pattern/sequences/adapter_submit/conditions](winwincode-automatic-report.json#/functional_chains/4/pattern/sequences/adapter_submit/conditions) |
| sequences/adapter_submit/conditions/shown_items/0/condition/location/line | 3526 | [/functional_chains/4/pattern/sequences/adapter_submit/conditions](winwincode-automatic-report.json#/functional_chains/4/pattern/sequences/adapter_submit/conditions) |
| sequences/adapter_submit/conditions/shown_items/0/condition/location/column | 12 | [/functional_chains/4/pattern/sequences/adapter_submit/conditions](winwincode-automatic-report.json#/functional_chains/4/pattern/sequences/adapter_submit/conditions) |
| sequences/adapter_submit/conditions/shown_items/0/condition/location/end_line | 3526 | [/functional_chains/4/pattern/sequences/adapter_submit/conditions](winwincode-automatic-report.json#/functional_chains/4/pattern/sequences/adapter_submit/conditions) |
| sequences/adapter_submit/conditions/shown_items/0/condition/location/start_byte | 138292 | [/functional_chains/4/pattern/sequences/adapter_submit/conditions](winwincode-automatic-report.json#/functional_chains/4/pattern/sequences/adapter_submit/conditions) |
| sequences/adapter_submit/conditions/shown_items/0/condition/location/end_byte | 138313 | [/functional_chains/4/pattern/sequences/adapter_submit/conditions](winwincode-automatic-report.json#/functional_chains/4/pattern/sequences/adapter_submit/conditions) |
| sequences/adapter_submit/conditions/shown_items/0/condition/operands/0/kind | identifier | [/functional_chains/4/pattern/sequences/adapter_submit/conditions](winwincode-automatic-report.json#/functional_chains/4/pattern/sequences/adapter_submit/conditions) |
| sequences/adapter_submit/conditions/shown_items/0/condition/operands/0/location/file | crates/winwincode-codex/src/adapter.rs | [/functional_chains/4/pattern/sequences/adapter_submit/conditions](winwincode-automatic-report.json#/functional_chains/4/pattern/sequences/adapter_submit/conditions) |
| sequences/adapter_submit/conditions/shown_items/0/condition/operands/0/location/line | 3526 | [/functional_chains/4/pattern/sequences/adapter_submit/conditions](winwincode-automatic-report.json#/functional_chains/4/pattern/sequences/adapter_submit/conditions) |
| sequences/adapter_submit/conditions/shown_items/0/condition/operands/0/location/column | 12 | [/functional_chains/4/pattern/sequences/adapter_submit/conditions](winwincode-automatic-report.json#/functional_chains/4/pattern/sequences/adapter_submit/conditions) |
| sequences/adapter_submit/conditions/shown_items/0/condition/operands/0/location/end_line | 3526 | [/functional_chains/4/pattern/sequences/adapter_submit/conditions](winwincode-automatic-report.json#/functional_chains/4/pattern/sequences/adapter_submit/conditions) |
| sequences/adapter_submit/conditions/shown_items/0/condition/operands/0/location/start_byte | 138292 | [/functional_chains/4/pattern/sequences/adapter_submit/conditions](winwincode-automatic-report.json#/functional_chains/4/pattern/sequences/adapter_submit/conditions) |
| sequences/adapter_submit/conditions/shown_items/0/condition/operands/0/location/end_byte | 138296 | [/functional_chains/4/pattern/sequences/adapter_submit/conditions](winwincode-automatic-report.json#/functional_chains/4/pattern/sequences/adapter_submit/conditions) |
| sequences/adapter_submit/conditions/shown_items/0/condition/operands/0/name | goal | [/functional_chains/4/pattern/sequences/adapter_submit/conditions](winwincode-automatic-report.json#/functional_chains/4/pattern/sequences/adapter_submit/conditions) |
| sequences/adapter_submit/conditions/shown_items/0/condition/operands/1/kind | identifier | [/functional_chains/4/pattern/sequences/adapter_submit/conditions](winwincode-automatic-report.json#/functional_chains/4/pattern/sequences/adapter_submit/conditions) |
| sequences/adapter_submit/conditions/shown_items/0/condition/operands/1/location/file | crates/winwincode-codex/src/adapter.rs | [/functional_chains/4/pattern/sequences/adapter_submit/conditions](winwincode-automatic-report.json#/functional_chains/4/pattern/sequences/adapter_submit/conditions) |
| sequences/adapter_submit/conditions/shown_items/0/condition/operands/1/location/line | 3526 | [/functional_chains/4/pattern/sequences/adapter_submit/conditions](winwincode-automatic-report.json#/functional_chains/4/pattern/sequences/adapter_submit/conditions) |
| sequences/adapter_submit/conditions/shown_items/0/condition/operands/1/location/column | 20 | [/functional_chains/4/pattern/sequences/adapter_submit/conditions](winwincode-automatic-report.json#/functional_chains/4/pattern/sequences/adapter_submit/conditions) |
| sequences/adapter_submit/conditions/shown_items/0/condition/operands/1/location/end_line | 3526 | [/functional_chains/4/pattern/sequences/adapter_submit/conditions](winwincode-automatic-report.json#/functional_chains/4/pattern/sequences/adapter_submit/conditions) |
| sequences/adapter_submit/conditions/shown_items/0/condition/operands/1/location/start_byte | 138300 | [/functional_chains/4/pattern/sequences/adapter_submit/conditions](winwincode-automatic-report.json#/functional_chains/4/pattern/sequences/adapter_submit/conditions) |
| sequences/adapter_submit/conditions/shown_items/0/condition/operands/1/location/end_byte | 138313 | [/functional_chains/4/pattern/sequences/adapter_submit/conditions](winwincode-automatic-report.json#/functional_chains/4/pattern/sequences/adapter_submit/conditions) |
| sequences/adapter_submit/conditions/shown_items/0/condition/operands/1/name | expected_goal | [/functional_chains/4/pattern/sequences/adapter_submit/conditions](winwincode-automatic-report.json#/functional_chains/4/pattern/sequences/adapter_submit/conditions) |

完整关系 [/functional_chains/4/pattern](winwincode-automatic-report.json#/functional_chains/4/pattern)；原 source facts [/functional_chains/4/source_facts](winwincode-automatic-report.json#/functional_chains/4/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### Chat 请求与 WorkItem / WorkRun · `wwc-report-chat-delivery-workrun-requests`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`16e57e77d5f8cc51ac46006c`；Evidence=`c48ec6276cd990a04b1ae929`。
源码/关系 [/functional_chains/5](winwincode-automatic-report.json#/functional_chains/5)；缺段 [/functional_chains/5/analysis_gaps](winwincode-automatic-report.json#/functional_chains/5/analysis_gaps)；模型 [/functional_chains/5/trusted_models](winwincode-automatic-report.json#/functional_chains/5/trusted_models)；policy [/functional_chains/5/policy_declarations](winwincode-automatic-report.json#/functional_chains/5/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/5/pattern/scoped_source_supported](winwincode-automatic-report.json#/functional_chains/5/pattern/scoped_source_supported) |
| sequences/builder/conditions/shown_items/0/condition/kind | identifier | [/functional_chains/5/pattern/sequences/builder/conditions](winwincode-automatic-report.json#/functional_chains/5/pattern/sequences/builder/conditions) |
| sequences/builder/conditions/shown_items/0/condition/location/file | apps/client/src/chat-delivery-creator.ts | [/functional_chains/5/pattern/sequences/builder/conditions](winwincode-automatic-report.json#/functional_chains/5/pattern/sequences/builder/conditions) |
| sequences/builder/conditions/shown_items/0/condition/location/line | 168 | [/functional_chains/5/pattern/sequences/builder/conditions](winwincode-automatic-report.json#/functional_chains/5/pattern/sequences/builder/conditions) |
| sequences/builder/conditions/shown_items/0/condition/location/column | 9 | [/functional_chains/5/pattern/sequences/builder/conditions](winwincode-automatic-report.json#/functional_chains/5/pattern/sequences/builder/conditions) |
| sequences/builder/conditions/shown_items/0/condition/location/end_line | 168 | [/functional_chains/5/pattern/sequences/builder/conditions](winwincode-automatic-report.json#/functional_chains/5/pattern/sequences/builder/conditions) |
| sequences/builder/conditions/shown_items/0/condition/location/start_byte | 5580 | [/functional_chains/5/pattern/sequences/builder/conditions](winwincode-automatic-report.json#/functional_chains/5/pattern/sequences/builder/conditions) |
| sequences/builder/conditions/shown_items/0/condition/location/end_byte | 5586 | [/functional_chains/5/pattern/sequences/builder/conditions](winwincode-automatic-report.json#/functional_chains/5/pattern/sequences/builder/conditions) |
| sequences/builder/conditions/shown_items/0/condition/name | closed | [/functional_chains/5/pattern/sequences/builder/conditions](winwincode-automatic-report.json#/functional_chains/5/pattern/sequences/builder/conditions) |
| sequences/builder/conditions/shown_items/0/branches/0/abrupt_source_expressions/0/kind | throw_statement | [/functional_chains/5/pattern/sequences/builder/conditions](winwincode-automatic-report.json#/functional_chains/5/pattern/sequences/builder/conditions) |
| sequences/builder/conditions/shown_items/0/branches/0/abrupt_source_expressions/0/location/file | apps/client/src/chat-delivery-creator.ts | [/functional_chains/5/pattern/sequences/builder/conditions](winwincode-automatic-report.json#/functional_chains/5/pattern/sequences/builder/conditions) |
| sequences/builder/conditions/shown_items/0/branches/0/abrupt_source_expressions/0/location/line | 168 | [/functional_chains/5/pattern/sequences/builder/conditions](winwincode-automatic-report.json#/functional_chains/5/pattern/sequences/builder/conditions) |
| sequences/builder/conditions/shown_items/0/branches/0/abrupt_source_expressions/0/location/column | 17 | [/functional_chains/5/pattern/sequences/builder/conditions](winwincode-automatic-report.json#/functional_chains/5/pattern/sequences/builder/conditions) |
| sequences/builder/conditions/shown_items/0/branches/0/abrupt_source_expressions/0/location/end_line | 171 | [/functional_chains/5/pattern/sequences/builder/conditions](winwincode-automatic-report.json#/functional_chains/5/pattern/sequences/builder/conditions) |
| sequences/builder/conditions/shown_items/0/branches/0/abrupt_source_expressions/0/location/start_byte | 5588 | [/functional_chains/5/pattern/sequences/builder/conditions](winwincode-automatic-report.json#/functional_chains/5/pattern/sequences/builder/conditions) |
| sequences/builder/conditions/shown_items/0/branches/0/abrupt_source_expressions/0/location/end_byte | 5699 | [/functional_chains/5/pattern/sequences/builder/conditions](winwincode-automatic-report.json#/functional_chains/5/pattern/sequences/builder/conditions) |
| sequences/builder/conditions/shown_items/0/branches/0/abrupt_source_expressions/0/returned_expression/call_effects_or_result_proven | 显示投影省略 | [/functional_chains/5/pattern/sequences/builder/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/call_effects_or_result_proven](winwincode-automatic-report.json#/functional_chains/5/pattern/sequences/builder/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/call_effects_or_result_proven) |
| sequences/builder/conditions/shown_items/0/branches/0/abrupt_source_expressions/0/returned_expression/arguments | 显示投影省略 | [/functional_chains/5/pattern/sequences/builder/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/arguments](winwincode-automatic-report.json#/functional_chains/5/pattern/sequences/builder/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/arguments) |
| sequences/builder/conditions/shown_items/0/branches/0/abrupt_source_expressions/0/returned_expression/callee_expression | 显示投影省略 | [/functional_chains/5/pattern/sequences/builder/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/callee_expression](winwincode-automatic-report.json#/functional_chains/5/pattern/sequences/builder/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/callee_expression) |
| sequences/builder/conditions/shown_items/0/branches/0/abrupt_source_expressions/0/returned_expression/callee_source | 显示投影省略 | [/functional_chains/5/pattern/sequences/builder/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/callee_source](winwincode-automatic-report.json#/functional_chains/5/pattern/sequences/builder/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/callee_source) |
| sequences/builder/conditions/shown_items/0/branches/0/abrupt_source_expressions/0/returned_expression/kind | 显示投影省略 | [/functional_chains/5/pattern/sequences/builder/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/kind](winwincode-automatic-report.json#/functional_chains/5/pattern/sequences/builder/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/kind) |
| sequences/builder/conditions/shown_items/0/branches/0/abrupt_source_expressions/0/returned_expression/location | 显示投影省略 | [/functional_chains/5/pattern/sequences/builder/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/location](winwincode-automatic-report.json#/functional_chains/5/pattern/sequences/builder/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/location) |
| sequences/builder/conditions/shown_items/0/branches/0/abrupt_source_expressions/0/runtime_completion_proven | false | [/functional_chains/5/pattern/sequences/builder/conditions](winwincode-automatic-report.json#/functional_chains/5/pattern/sequences/builder/conditions) |
| sequences/builder/conditions/shown_items/0/branches/0/branch | then | [/functional_chains/5/pattern/sequences/builder/conditions](winwincode-automatic-report.json#/functional_chains/5/pattern/sequences/builder/conditions) |

完整关系 [/functional_chains/5/pattern](winwincode-automatic-report.json#/functional_chains/5/pattern)；原 source facts [/functional_chains/5/source_facts](winwincode-automatic-report.json#/functional_chains/5/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### Chat 请求身份与字段保留 · `wwc-report-chat-retained-request-identities`

`message_identity_relations`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`be660f8d000a53b2df3bfe28`；Evidence=`1c69fd05b8f3d7ef73ad9961`。
源码/关系 [/functional_chains/6](winwincode-automatic-report.json#/functional_chains/6)；缺段 [/functional_chains/6/analysis_gaps](winwincode-automatic-report.json#/functional_chains/6/analysis_gaps)；模型 [/functional_chains/6/trusted_models](winwincode-automatic-report.json#/functional_chains/6/trusted_models)；policy [/functional_chains/6/policy_declarations](winwincode-automatic-report.json#/functional_chains/6/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

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

### Device provider 部署分流 · `wwc-report-device-provider-deployment`

`deployment_provider_split`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`deployment_candidate_chain_not_global_dispatch_or_credential_availability`；Finding=`f0600517dc7e144b07df96ba`；Evidence=`520679e01079d6ae62a8efaf`。
源码/关系 [/functional_chains/7](winwincode-automatic-report.json#/functional_chains/7)；缺段 [/functional_chains/7/analysis_gaps](winwincode-automatic-report.json#/functional_chains/7/analysis_gaps)；模型 [/functional_chains/7/trusted_models](winwincode-automatic-report.json#/functional_chains/7/trusted_models)；policy [/functional_chains/7/policy_declarations](winwincode-automatic-report.json#/functional_chains/7/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/7/pattern/scoped_source_supported](winwincode-automatic-report.json#/functional_chains/7/pattern/scoped_source_supported) |
| boundary_results/0/runtime_result_proven | false | [/functional_chains/7/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/7/pattern/boundary_results) |
| boundary_results/0/expression/call_effects_or_result_proven | false | [/functional_chains/7/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/7/pattern/boundary_results) |
| boundary_results/0/expression/arguments/0/children/0/children/0/kind | 显示投影省略 | [/functional_chains/7/pattern/boundary_results/0/expression/arguments/0/children/0/children/0/kind](winwincode-automatic-report.json#/functional_chains/7/pattern/boundary_results/0/expression/arguments/0/children/0/children/0/kind) |
| boundary_results/0/expression/arguments/0/children/0/children/0/location | 显示投影省略 | [/functional_chains/7/pattern/boundary_results/0/expression/arguments/0/children/0/children/0/location](winwincode-automatic-report.json#/functional_chains/7/pattern/boundary_results/0/expression/arguments/0/children/0/children/0/location) |
| boundary_results/0/expression/arguments/0/children/0/children/0/name | 显示投影省略 | [/functional_chains/7/pattern/boundary_results/0/expression/arguments/0/children/0/children/0/name](winwincode-automatic-report.json#/functional_chains/7/pattern/boundary_results/0/expression/arguments/0/children/0/children/0/name) |
| boundary_results/0/expression/arguments/0/children/0/children/1/kind | 显示投影省略 | [/functional_chains/7/pattern/boundary_results/0/expression/arguments/0/children/0/children/1/kind](winwincode-automatic-report.json#/functional_chains/7/pattern/boundary_results/0/expression/arguments/0/children/0/children/1/kind) |
| boundary_results/0/expression/arguments/0/children/0/children/1/location | 显示投影省略 | [/functional_chains/7/pattern/boundary_results/0/expression/arguments/0/children/0/children/1/location](winwincode-automatic-report.json#/functional_chains/7/pattern/boundary_results/0/expression/arguments/0/children/0/children/1/location) |
| boundary_results/0/expression/arguments/0/children/0/children/1/name | 显示投影省略 | [/functional_chains/7/pattern/boundary_results/0/expression/arguments/0/children/0/children/1/name](winwincode-automatic-report.json#/functional_chains/7/pattern/boundary_results/0/expression/arguments/0/children/0/children/1/name) |
| boundary_results/0/expression/arguments/0/children/0/kind | scoped_identifier | [/functional_chains/7/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/7/pattern/boundary_results) |
| boundary_results/0/expression/arguments/0/children/0/location/file | crates/winwincode-server/src/main.rs | [/functional_chains/7/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/7/pattern/boundary_results) |
| boundary_results/0/expression/arguments/0/children/0/location/line | 346 | [/functional_chains/7/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/7/pattern/boundary_results) |
| boundary_results/0/expression/arguments/0/children/0/location/column | 13 | [/functional_chains/7/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/7/pattern/boundary_results) |
| boundary_results/0/expression/arguments/0/children/0/location/end_line | 346 | [/functional_chains/7/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/7/pattern/boundary_results) |
| boundary_results/0/expression/arguments/0/children/0/location/start_byte | 13431 | [/functional_chains/7/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/7/pattern/boundary_results) |
| boundary_results/0/expression/arguments/0/children/0/location/end_byte | 13482 | [/functional_chains/7/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/7/pattern/boundary_results) |
| boundary_results/0/expression/arguments/0/children/0/source | winwincode_control_plane::DurableExecutionPortError | [/functional_chains/7/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/7/pattern/boundary_results) |
| boundary_results/0/expression/arguments/0/children/1/kind | identifier | [/functional_chains/7/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/7/pattern/boundary_results) |
| boundary_results/0/expression/arguments/0/children/1/location/file | crates/winwincode-server/src/main.rs | [/functional_chains/7/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/7/pattern/boundary_results) |
| boundary_results/0/expression/arguments/0/children/1/location/line | 346 | [/functional_chains/7/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/7/pattern/boundary_results) |
| boundary_results/0/expression/arguments/0/children/1/location/column | 66 | [/functional_chains/7/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/7/pattern/boundary_results) |
| boundary_results/0/expression/arguments/0/children/1/location/end_line | 346 | [/functional_chains/7/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/7/pattern/boundary_results) |
| boundary_results/0/expression/arguments/0/children/1/location/start_byte | 13484 | [/functional_chains/7/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/7/pattern/boundary_results) |
| boundary_results/0/expression/arguments/0/children/1/location/end_byte | 13502 | [/functional_chains/7/pattern/boundary_results](winwincode-automatic-report.json#/functional_chains/7/pattern/boundary_results) |

完整关系 [/functional_chains/7/pattern](winwincode-automatic-report.json#/functional_chains/7/pattern)；原 source facts [/functional_chains/7/source_facts](winwincode-automatic-report.json#/functional_chains/7/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### Kernel create_session 接口 · `wwc-report-kernel-create-session-interface`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`196dfa3ccb808a6ae8466128`；Evidence=`51d1aa9f761bf2b9fdb04582`。
源码/关系 [/functional_chains/8](winwincode-automatic-report.json#/functional_chains/8)；缺段 [/functional_chains/8/analysis_gaps](winwincode-automatic-report.json#/functional_chains/8/analysis_gaps)；模型 [/functional_chains/8/trusted_models](winwincode-automatic-report.json#/functional_chains/8/trusted_models)；policy [/functional_chains/8/policy_declarations](winwincode-automatic-report.json#/functional_chains/8/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/8/pattern/scoped_source_supported](winwincode-automatic-report.json#/functional_chains/8/pattern/scoped_source_supported) |
| nested_source_regions/0/conditions/0 | this deferred captured body is activated and the recorded statements are reached normally | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/body_activation_proven | false | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/future_fulfillment_proven | false | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/kind | deferred_source_region_sequence | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/location/file | crates/kernel/src/lib.rs | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/location/line | 1221 | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/location/column | 21 | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/location/end_line | 1230 | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/location/start_byte | 44514 | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/location/end_byte | 44981 | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/nested_calls_promoted_to_resolved | false | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/origin | source-derived | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/role | kernel_create | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/all_function_paths_or_effects_accounted | false | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/future_or_callback_activation_proven | false | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/orders/0/conditions/0 | both direct statements normally reached in the same invocation | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/orders/0/conditions/1 | preceding asynchronous operations complete normally; no claim of completion or whole-program dominance | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/orders/0/after_step_id | ad8a2fdb5ec2f51512b2ce92 | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/orders/0/all_paths_reach_next_proven | false | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/orders/0/before_step_id | 09ee72949d81e965f8b901a0 | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/orders/0/kind | conditional_direct_statement_order | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/orders/0/location/file | crates/kernel/src/lib.rs | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/orders/0/location/line | 1223 | [/functional_chains/8/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions) |

完整关系 [/functional_chains/8/pattern](winwincode-automatic-report.json#/functional_chains/8/pattern)；原 source facts [/functional_chains/8/source_facts](winwincode-automatic-report.json#/functional_chains/8/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### Kernel reconcile_turn_exact 接口 · `wwc-report-kernel-reconcile-exact-interface`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`913a6055ce2aac727cf43afc`；Evidence=`edbcd21274048cef1e842d4d`。
源码/关系 [/functional_chains/9](winwincode-automatic-report.json#/functional_chains/9)；缺段 [/functional_chains/9/analysis_gaps](winwincode-automatic-report.json#/functional_chains/9/analysis_gaps)；模型 [/functional_chains/9/trusted_models](winwincode-automatic-report.json#/functional_chains/9/trusted_models)；policy [/functional_chains/9/policy_declarations](winwincode-automatic-report.json#/functional_chains/9/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/9/pattern/scoped_source_supported](winwincode-automatic-report.json#/functional_chains/9/pattern/scoped_source_supported) |
| nested_source_regions/0/conditions/0 | this deferred captured body is activated and the recorded statements are reached normally | [/functional_chains/9/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/9/pattern/nested_source_regions) |
| nested_source_regions/0/body_activation_proven | false | [/functional_chains/9/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/9/pattern/nested_source_regions) |
| nested_source_regions/0/future_fulfillment_proven | false | [/functional_chains/9/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/9/pattern/nested_source_regions) |
| nested_source_regions/0/kind | deferred_source_region_sequence | [/functional_chains/9/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/9/pattern/nested_source_regions) |
| nested_source_regions/0/location/file | crates/kernel/src/lib.rs | [/functional_chains/9/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/9/pattern/nested_source_regions) |
| nested_source_regions/0/location/line | 1376 | [/functional_chains/9/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/9/pattern/nested_source_regions) |
| nested_source_regions/0/location/column | 21 | [/functional_chains/9/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/9/pattern/nested_source_regions) |
| nested_source_regions/0/location/end_line | 1432 | [/functional_chains/9/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/9/pattern/nested_source_regions) |
| nested_source_regions/0/location/start_byte | 50583 | [/functional_chains/9/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/9/pattern/nested_source_regions) |
| nested_source_regions/0/location/end_byte | 53102 | [/functional_chains/9/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/9/pattern/nested_source_regions) |
| nested_source_regions/0/nested_calls_promoted_to_resolved | false | [/functional_chains/9/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/9/pattern/nested_source_regions) |
| nested_source_regions/0/origin | source-derived | [/functional_chains/9/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/9/pattern/nested_source_regions) |
| nested_source_regions/0/role | kernel_reconcile | [/functional_chains/9/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/9/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/condition/kind | binary_expression | [/functional_chains/9/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/9/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/condition/location/file | crates/kernel/src/lib.rs | [/functional_chains/9/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/9/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/condition/location/line | 1377 | [/functional_chains/9/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/9/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/condition/location/column | 16 | [/functional_chains/9/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/9/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/condition/location/end_line | 1377 | [/functional_chains/9/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/9/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/condition/location/start_byte | 50606 | [/functional_chains/9/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/9/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/condition/location/end_byte | 50657 | [/functional_chains/9/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/9/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/condition/operands/0/call_effects_or_result_proven | false | [/functional_chains/9/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/9/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/condition/operands/0/callee_expression/current_referent_value_proven | 显示投影省略 | [/functional_chains/9/pattern/nested_source_regions/0/sequence/conditions/0/condition/operands/0/callee_expression/current_referent_value_proven](winwincode-automatic-report.json#/functional_chains/9/pattern/nested_source_regions/0/sequence/conditions/0/condition/operands/0/callee_expression/current_referent_value_proven) |
| nested_source_regions/0/sequence/conditions/0/condition/operands/0/callee_expression/kind | 显示投影省略 | [/functional_chains/9/pattern/nested_source_regions/0/sequence/conditions/0/condition/operands/0/callee_expression/kind](winwincode-automatic-report.json#/functional_chains/9/pattern/nested_source_regions/0/sequence/conditions/0/condition/operands/0/callee_expression/kind) |

完整关系 [/functional_chains/9/pattern](winwincode-automatic-report.json#/functional_chains/9/pattern)；原 source facts [/functional_chains/9/source_facts](winwincode-automatic-report.json#/functional_chains/9/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### Kernel submit_turn 接口 · `wwc-report-kernel-submit-turn-interface`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`cb2d5f3a570ce0c9da78a1af`；Evidence=`fd521c4e48b793a0dd12ab4e`。
源码/关系 [/functional_chains/10](winwincode-automatic-report.json#/functional_chains/10)；缺段 [/functional_chains/10/analysis_gaps](winwincode-automatic-report.json#/functional_chains/10/analysis_gaps)；模型 [/functional_chains/10/trusted_models](winwincode-automatic-report.json#/functional_chains/10/trusted_models)；policy [/functional_chains/10/policy_declarations](winwincode-automatic-report.json#/functional_chains/10/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/10/pattern/scoped_source_supported](winwincode-automatic-report.json#/functional_chains/10/pattern/scoped_source_supported) |
| nested_source_regions/0/conditions/0 | this deferred captured body is activated and the recorded statements are reached normally | [/functional_chains/10/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/10/pattern/nested_source_regions) |
| nested_source_regions/0/body_activation_proven | false | [/functional_chains/10/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/10/pattern/nested_source_regions) |
| nested_source_regions/0/future_fulfillment_proven | false | [/functional_chains/10/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/10/pattern/nested_source_regions) |
| nested_source_regions/0/kind | deferred_source_region_sequence | [/functional_chains/10/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/10/pattern/nested_source_regions) |
| nested_source_regions/0/location/file | crates/kernel/src/lib.rs | [/functional_chains/10/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/10/pattern/nested_source_regions) |
| nested_source_regions/0/location/line | 1339 | [/functional_chains/10/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/10/pattern/nested_source_regions) |
| nested_source_regions/0/location/column | 21 | [/functional_chains/10/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/10/pattern/nested_source_regions) |
| nested_source_regions/0/location/end_line | 1356 | [/functional_chains/10/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/10/pattern/nested_source_regions) |
| nested_source_regions/0/location/start_byte | 49122 | [/functional_chains/10/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/10/pattern/nested_source_regions) |
| nested_source_regions/0/location/end_byte | 49859 | [/functional_chains/10/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/10/pattern/nested_source_regions) |
| nested_source_regions/0/nested_calls_promoted_to_resolved | false | [/functional_chains/10/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/10/pattern/nested_source_regions) |
| nested_source_regions/0/origin | source-derived | [/functional_chains/10/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/10/pattern/nested_source_regions) |
| nested_source_regions/0/role | kernel_submit | [/functional_chains/10/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/10/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/condition/call_effects_or_result_proven | false | [/functional_chains/10/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/10/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/condition/callee_expression/current_referent_value_proven | false | [/functional_chains/10/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/10/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/condition/callee_expression/kind | field_expression | [/functional_chains/10/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/10/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/condition/callee_expression/location/file | crates/kernel/src/lib.rs | [/functional_chains/10/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/10/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/condition/callee_expression/location/line | 1340 | [/functional_chains/10/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/10/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/condition/callee_expression/location/column | 16 | [/functional_chains/10/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/10/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/condition/callee_expression/location/end_line | 1340 | [/functional_chains/10/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/10/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/condition/callee_expression/location/start_byte | 49145 | [/functional_chains/10/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/10/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/condition/callee_expression/location/end_byte | 49165 | [/functional_chains/10/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/10/pattern/nested_source_regions) |
| nested_source_regions/0/sequence/conditions/0/condition/callee_expression/member | is_empty | [/functional_chains/10/pattern/nested_source_regions](winwincode-automatic-report.json#/functional_chains/10/pattern/nested_source_regions) |

完整关系 [/functional_chains/10/pattern](winwincode-automatic-report.json#/functional_chains/10/pattern)；原 source facts [/functional_chains/10/source_facts](winwincode-automatic-report.json#/functional_chains/10/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### 发件记录与确认关联字段 · `wwc-report-outbox-ack-correlation-fields`

`message_identity_relations`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`f2a949272f560b9d0dfb5e46`；Evidence=`9de38e3ca5cc1932733bca8e`。
源码/关系 [/functional_chains/11](winwincode-automatic-report.json#/functional_chains/11)；缺段 [/functional_chains/11/analysis_gaps](winwincode-automatic-report.json#/functional_chains/11/analysis_gaps)；模型 [/functional_chains/11/trusted_models](winwincode-automatic-report.json#/functional_chains/11/trusted_models)；policy [/functional_chains/11/policy_declarations](winwincode-automatic-report.json#/functional_chains/11/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

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

### ProductionAdapter → Kernel 构造 · `wwc-report-production-adapter-embedded-kernel`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`3ad1a2c3498a4a08ddb2bcaf`；Evidence=`318a09eca70749d291d1af8e`。
源码/关系 [/functional_chains/12](winwincode-automatic-report.json#/functional_chains/12)；缺段 [/functional_chains/12/analysis_gaps](winwincode-automatic-report.json#/functional_chains/12/analysis_gaps)；模型 [/functional_chains/12/trusted_models](winwincode-automatic-report.json#/functional_chains/12/trusted_models)；policy [/functional_chains/12/policy_declarations](winwincode-automatic-report.json#/functional_chains/12/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/12/pattern/scoped_source_supported](winwincode-automatic-report.json#/functional_chains/12/pattern/scoped_source_supported) |
| sequences/adapter_open/all_function_paths_or_effects_accounted | false | [/functional_chains/12/pattern/sequences](winwincode-automatic-report.json#/functional_chains/12/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/kind | ordered_source_assignment_attempt | [/functional_chains/12/pattern/sequences](winwincode-automatic-report.json#/functional_chains/12/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/current_referent_value_proven | false | [/functional_chains/12/pattern/sequences](winwincode-automatic-report.json#/functional_chains/12/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/kind | field_expression | [/functional_chains/12/pattern/sequences](winwincode-automatic-report.json#/functional_chains/12/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/location/file | crates/winwincode-codex/src/adapter.rs | [/functional_chains/12/pattern/sequences](winwincode-automatic-report.json#/functional_chains/12/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/location/line | 420 | [/functional_chains/12/pattern/sequences](winwincode-automatic-report.json#/functional_chains/12/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/location/column | 9 | [/functional_chains/12/pattern/sequences](winwincode-automatic-report.json#/functional_chains/12/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/location/end_line | 420 | [/functional_chains/12/pattern/sequences](winwincode-automatic-report.json#/functional_chains/12/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/location/start_byte | 17565 | [/functional_chains/12/pattern/sequences](winwincode-automatic-report.json#/functional_chains/12/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/location/end_byte | 17589 | [/functional_chains/12/pattern/sequences](winwincode-automatic-report.json#/functional_chains/12/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/member | helper_executable | [/functional_chains/12/pattern/sequences](winwincode-automatic-report.json#/functional_chains/12/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/member_location/file | crates/winwincode-codex/src/adapter.rs | [/functional_chains/12/pattern/sequences](winwincode-automatic-report.json#/functional_chains/12/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/member_location/line | 420 | [/functional_chains/12/pattern/sequences](winwincode-automatic-report.json#/functional_chains/12/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/member_location/column | 16 | [/functional_chains/12/pattern/sequences](winwincode-automatic-report.json#/functional_chains/12/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/member_location/end_line | 420 | [/functional_chains/12/pattern/sequences](winwincode-automatic-report.json#/functional_chains/12/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/member_location/start_byte | 17572 | [/functional_chains/12/pattern/sequences](winwincode-automatic-report.json#/functional_chains/12/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/member_location/end_byte | 17589 | [/functional_chains/12/pattern/sequences](winwincode-automatic-report.json#/functional_chains/12/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/object/kind | identifier | [/functional_chains/12/pattern/sequences](winwincode-automatic-report.json#/functional_chains/12/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/object/location/file | crates/winwincode-codex/src/adapter.rs | [/functional_chains/12/pattern/sequences](winwincode-automatic-report.json#/functional_chains/12/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/object/location/line | 420 | [/functional_chains/12/pattern/sequences](winwincode-automatic-report.json#/functional_chains/12/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/object/location/column | 9 | [/functional_chains/12/pattern/sequences](winwincode-automatic-report.json#/functional_chains/12/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/object/location/end_line | 420 | [/functional_chains/12/pattern/sequences](winwincode-automatic-report.json#/functional_chains/12/pattern/sequences) |
| sequences/adapter_open/assignment_attempts/0/left/object/location/start_byte | 17565 | [/functional_chains/12/pattern/sequences](winwincode-automatic-report.json#/functional_chains/12/pattern/sequences) |

完整关系 [/functional_chains/12/pattern](winwincode-automatic-report.json#/functional_chains/12/pattern)；原 source facts [/functional_chains/12/source_facts](winwincode-automatic-report.json#/functional_chains/12/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### intent → persist → exact reconcile · `wwc-report-submission-intent-kernel-order`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`719c7a3c938f4606d84cb1c9`；Evidence=`59329e33767ab815dc68d984`。
源码/关系 [/functional_chains/13](winwincode-automatic-report.json#/functional_chains/13)；缺段 [/functional_chains/13/analysis_gaps](winwincode-automatic-report.json#/functional_chains/13/analysis_gaps)；模型 [/functional_chains/13/trusted_models](winwincode-automatic-report.json#/functional_chains/13/trusted_models)；policy [/functional_chains/13/policy_declarations](winwincode-automatic-report.json#/functional_chains/13/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/13/pattern/scoped_source_supported](winwincode-automatic-report.json#/functional_chains/13/pattern/scoped_source_supported) |
| sequences/submission/conditions/shown_items/0/condition/kind | binary_expression | [/functional_chains/13/pattern/sequences/submission/conditions](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences/submission/conditions) |
| sequences/submission/conditions/shown_items/0/condition/location/file | crates/winwincode-codex/src/adapter.rs | [/functional_chains/13/pattern/sequences/submission/conditions](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences/submission/conditions) |
| sequences/submission/conditions/shown_items/0/condition/location/line | 3526 | [/functional_chains/13/pattern/sequences/submission/conditions](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences/submission/conditions) |
| sequences/submission/conditions/shown_items/0/condition/location/column | 12 | [/functional_chains/13/pattern/sequences/submission/conditions](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences/submission/conditions) |
| sequences/submission/conditions/shown_items/0/condition/location/end_line | 3526 | [/functional_chains/13/pattern/sequences/submission/conditions](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences/submission/conditions) |
| sequences/submission/conditions/shown_items/0/condition/location/start_byte | 138292 | [/functional_chains/13/pattern/sequences/submission/conditions](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences/submission/conditions) |
| sequences/submission/conditions/shown_items/0/condition/location/end_byte | 138313 | [/functional_chains/13/pattern/sequences/submission/conditions](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences/submission/conditions) |
| sequences/submission/conditions/shown_items/0/condition/operands/0/kind | identifier | [/functional_chains/13/pattern/sequences/submission/conditions](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences/submission/conditions) |
| sequences/submission/conditions/shown_items/0/condition/operands/0/location/file | crates/winwincode-codex/src/adapter.rs | [/functional_chains/13/pattern/sequences/submission/conditions](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences/submission/conditions) |
| sequences/submission/conditions/shown_items/0/condition/operands/0/location/line | 3526 | [/functional_chains/13/pattern/sequences/submission/conditions](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences/submission/conditions) |
| sequences/submission/conditions/shown_items/0/condition/operands/0/location/column | 12 | [/functional_chains/13/pattern/sequences/submission/conditions](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences/submission/conditions) |
| sequences/submission/conditions/shown_items/0/condition/operands/0/location/end_line | 3526 | [/functional_chains/13/pattern/sequences/submission/conditions](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences/submission/conditions) |
| sequences/submission/conditions/shown_items/0/condition/operands/0/location/start_byte | 138292 | [/functional_chains/13/pattern/sequences/submission/conditions](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences/submission/conditions) |
| sequences/submission/conditions/shown_items/0/condition/operands/0/location/end_byte | 138296 | [/functional_chains/13/pattern/sequences/submission/conditions](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences/submission/conditions) |
| sequences/submission/conditions/shown_items/0/condition/operands/0/name | goal | [/functional_chains/13/pattern/sequences/submission/conditions](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences/submission/conditions) |
| sequences/submission/conditions/shown_items/0/condition/operands/1/kind | identifier | [/functional_chains/13/pattern/sequences/submission/conditions](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences/submission/conditions) |
| sequences/submission/conditions/shown_items/0/condition/operands/1/location/file | crates/winwincode-codex/src/adapter.rs | [/functional_chains/13/pattern/sequences/submission/conditions](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences/submission/conditions) |
| sequences/submission/conditions/shown_items/0/condition/operands/1/location/line | 3526 | [/functional_chains/13/pattern/sequences/submission/conditions](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences/submission/conditions) |
| sequences/submission/conditions/shown_items/0/condition/operands/1/location/column | 20 | [/functional_chains/13/pattern/sequences/submission/conditions](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences/submission/conditions) |
| sequences/submission/conditions/shown_items/0/condition/operands/1/location/end_line | 3526 | [/functional_chains/13/pattern/sequences/submission/conditions](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences/submission/conditions) |
| sequences/submission/conditions/shown_items/0/condition/operands/1/location/start_byte | 138300 | [/functional_chains/13/pattern/sequences/submission/conditions](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences/submission/conditions) |
| sequences/submission/conditions/shown_items/0/condition/operands/1/location/end_byte | 138313 | [/functional_chains/13/pattern/sequences/submission/conditions](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences/submission/conditions) |
| sequences/submission/conditions/shown_items/0/condition/operands/1/name | expected_goal | [/functional_chains/13/pattern/sequences/submission/conditions](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences/submission/conditions) |

完整关系 [/functional_chains/13/pattern](winwincode-automatic-report.json#/functional_chains/13/pattern)；原 source facts [/functional_chains/13/source_facts](winwincode-automatic-report.json#/functional_chains/13/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### Worker 与 Adapter 的消息身份 · `wwc-report-worker-adapter-record-identities`

`message_identity_relations`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`54aa478e9d99f2659cc0022c`；Evidence=`846408d1484e9960f40875fd`。
源码/关系 [/functional_chains/14](winwincode-automatic-report.json#/functional_chains/14)；缺段 [/functional_chains/14/analysis_gaps](winwincode-automatic-report.json#/functional_chains/14/analysis_gaps)；模型 [/functional_chains/14/trusted_models](winwincode-automatic-report.json#/functional_chains/14/trusted_models)；policy [/functional_chains/14/policy_declarations](winwincode-automatic-report.json#/functional_chains/14/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

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

### Worker 入口分支 · `wwc-report-worker-bootstrap-entries`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`31ff1b2904390c31587a11f1`；Evidence=`1fbfeecdfb62eaf4a930ac30`。
源码/关系 [/functional_chains/15](winwincode-automatic-report.json#/functional_chains/15)；缺段 [/functional_chains/15/analysis_gaps](winwincode-automatic-report.json#/functional_chains/15/analysis_gaps)；模型 [/functional_chains/15/trusted_models](winwincode-automatic-report.json#/functional_chains/15/trusted_models)；policy [/functional_chains/15/policy_declarations](winwincode-automatic-report.json#/functional_chains/15/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/15/pattern/scoped_source_supported](winwincode-automatic-report.json#/functional_chains/15/pattern/scoped_source_supported) |
| sequences/entry/all_function_paths_or_effects_accounted | false | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/entry/future_or_callback_activation_proven | false | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/entry/orders/0/conditions/0 | both direct statements normally reached in the same invocation | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/entry/orders/0/conditions/1 | preceding asynchronous operations complete normally; no claim of completion or whole-program dominance | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/entry/orders/0/after_step_id | 49fcf927344caeb053bbf92c | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/entry/orders/0/all_paths_reach_next_proven | false | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/entry/orders/0/before_step_id | cfe66950facbd010367d60b2 | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/entry/orders/0/kind | conditional_direct_statement_order | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/entry/orders/0/location/file | crates/winwincode-worker/src/main.rs | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/entry/orders/0/location/line | 36 | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/entry/orders/0/location/column | 5 | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/entry/orders/0/location/end_line | 49 | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/entry/orders/0/location/start_byte | 1408 | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/entry/orders/0/location/end_byte | 1968 | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/entry/orders/0/model_id | captured-normal-statement-control-v1 | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/entry/orders/0/origin | source-derived | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/entry/orders/0/role | entry | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/entry/region_kind | function_item | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/entry/role | entry | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/entry/source_region_location/file | crates/winwincode-worker/src/main.rs | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/entry/source_region_location/line | 34 | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/entry/source_region_location/column | 1 | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |
| sequences/entry/source_region_location/end_line | 50 | [/functional_chains/15/pattern/sequences](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences) |

完整关系 [/functional_chains/15/pattern](winwincode-automatic-report.json#/functional_chains/15/pattern)；原 source facts [/functional_chains/15/source_facts](winwincode-automatic-report.json#/functional_chains/15/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### 生产 Worker 构造 · `wwc-report-worker-production-construction`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`592af9e5752f7a582d46b025`；Evidence=`5794bcb9410b1863c784f02f`。
源码/关系 [/functional_chains/16](winwincode-automatic-report.json#/functional_chains/16)；缺段 [/functional_chains/16/analysis_gaps](winwincode-automatic-report.json#/functional_chains/16/analysis_gaps)；模型 [/functional_chains/16/trusted_models](winwincode-automatic-report.json#/functional_chains/16/trusted_models)；policy [/functional_chains/16/policy_declarations](winwincode-automatic-report.json#/functional_chains/16/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/16/pattern/scoped_source_supported](winwincode-automatic-report.json#/functional_chains/16/pattern/scoped_source_supported) |
| sequences/adapter_factory/all_function_paths_or_effects_accounted | false | [/functional_chains/16/pattern/sequences](winwincode-automatic-report.json#/functional_chains/16/pattern/sequences) |
| sequences/adapter_factory/future_or_callback_activation_proven | false | [/functional_chains/16/pattern/sequences](winwincode-automatic-report.json#/functional_chains/16/pattern/sequences) |
| sequences/adapter_factory/orders/shown_items/0/conditions/0 | both direct statements normally reached in the same invocation | [/functional_chains/16/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/16/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/conditions/1 | preceding asynchronous operations complete normally; no claim of completion or whole-program dominance | [/functional_chains/16/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/16/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/after_step_id | d34ee7a9c9c23378653afb9e | [/functional_chains/16/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/16/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/all_paths_reach_next_proven | false | [/functional_chains/16/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/16/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/before_step_id | 45cd76b9e885d45633d6ef89 | [/functional_chains/16/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/16/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/kind | conditional_direct_statement_order | [/functional_chains/16/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/16/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/location/file | crates/winwincode-worker/src/main.rs | [/functional_chains/16/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/16/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/location/line | 326 | [/functional_chains/16/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/16/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/location/column | 5 | [/functional_chains/16/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/16/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/location/end_line | 326 | [/functional_chains/16/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/16/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/location/start_byte | 13491 | [/functional_chains/16/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/16/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/location/end_byte | 13571 | [/functional_chains/16/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/16/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/model_id | captured-normal-statement-control-v1 | [/functional_chains/16/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/16/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/origin | source-derived | [/functional_chains/16/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/16/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/0/role | adapter_factory | [/functional_chains/16/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/16/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/1/conditions/0 | both direct statements normally reached in the same invocation | [/functional_chains/16/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/16/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/1/conditions/1 | preceding asynchronous operations complete normally; no claim of completion or whole-program dominance | [/functional_chains/16/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/16/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/1/after_step_id | 378f7da1c3d8ddc552184713 | [/functional_chains/16/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/16/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/1/all_paths_reach_next_proven | false | [/functional_chains/16/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/16/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/1/before_step_id | d34ee7a9c9c23378653afb9e | [/functional_chains/16/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/16/pattern/sequences/adapter_factory/orders) |
| sequences/adapter_factory/orders/shown_items/1/kind | conditional_direct_statement_order | [/functional_chains/16/pattern/sequences/adapter_factory/orders](winwincode-automatic-report.json#/functional_chains/16/pattern/sequences/adapter_factory/orders) |

完整关系 [/functional_chains/16/pattern](winwincode-automatic-report.json#/functional_chains/16/pattern)；原 source facts [/functional_chains/16/source_facts](winwincode-automatic-report.json#/functional_chains/16/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### Worker typed dispatch · `wwc-report-worker-typed-dispatch`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`1fc26eccb25a192cdd8c7408`；Evidence=`8f1bdd62de2f8b0581cc84a2`。
源码/关系 [/functional_chains/17](winwincode-automatic-report.json#/functional_chains/17)；缺段 [/functional_chains/17/analysis_gaps](winwincode-automatic-report.json#/functional_chains/17/analysis_gaps)；模型 [/functional_chains/17/trusted_models](winwincode-automatic-report.json#/functional_chains/17/trusted_models)；policy [/functional_chains/17/policy_declarations](winwincode-automatic-report.json#/functional_chains/17/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/17/pattern/scoped_source_supported](winwincode-automatic-report.json#/functional_chains/17/pattern/scoped_source_supported) |
| sequences/control/conditions/0/condition/kind | try_expression | [/functional_chains/17/pattern/sequences](winwincode-automatic-report.json#/functional_chains/17/pattern/sequences) |
| sequences/control/conditions/0/condition/location/file | crates/winwincode-worker/src/lib.rs | [/functional_chains/17/pattern/sequences](winwincode-automatic-report.json#/functional_chains/17/pattern/sequences) |
| sequences/control/conditions/0/condition/location/line | 772 | [/functional_chains/17/pattern/sequences](winwincode-automatic-report.json#/functional_chains/17/pattern/sequences) |
| sequences/control/conditions/0/condition/location/column | 20 | [/functional_chains/17/pattern/sequences](winwincode-automatic-report.json#/functional_chains/17/pattern/sequences) |
| sequences/control/conditions/0/condition/location/end_line | 775 | [/functional_chains/17/pattern/sequences](winwincode-automatic-report.json#/functional_chains/17/pattern/sequences) |
| sequences/control/conditions/0/condition/location/start_byte | 30944 | [/functional_chains/17/pattern/sequences](winwincode-automatic-report.json#/functional_chains/17/pattern/sequences) |
| sequences/control/conditions/0/condition/location/end_byte | 31110 | [/functional_chains/17/pattern/sequences](winwincode-automatic-report.json#/functional_chains/17/pattern/sequences) |
| sequences/control/conditions/0/condition/operand/call_effects_or_result_proven | false | [/functional_chains/17/pattern/sequences](winwincode-automatic-report.json#/functional_chains/17/pattern/sequences) |
| sequences/control/conditions/0/condition/operand/arguments/0/kind | closure_expression | [/functional_chains/17/pattern/sequences](winwincode-automatic-report.json#/functional_chains/17/pattern/sequences) |
| sequences/control/conditions/0/condition/operand/arguments/0/location/file | crates/winwincode-worker/src/lib.rs | [/functional_chains/17/pattern/sequences](winwincode-automatic-report.json#/functional_chains/17/pattern/sequences) |
| sequences/control/conditions/0/condition/operand/arguments/0/location/line | 775 | [/functional_chains/17/pattern/sequences](winwincode-automatic-report.json#/functional_chains/17/pattern/sequences) |
| sequences/control/conditions/0/condition/operand/arguments/0/location/column | 30 | [/functional_chains/17/pattern/sequences](winwincode-automatic-report.json#/functional_chains/17/pattern/sequences) |
| sequences/control/conditions/0/condition/operand/arguments/0/location/end_line | 775 | [/functional_chains/17/pattern/sequences](winwincode-automatic-report.json#/functional_chains/17/pattern/sequences) |
| sequences/control/conditions/0/condition/operand/arguments/0/location/start_byte | 31087 | [/functional_chains/17/pattern/sequences](winwincode-automatic-report.json#/functional_chains/17/pattern/sequences) |
| sequences/control/conditions/0/condition/operand/arguments/0/location/end_byte | 31108 | [/functional_chains/17/pattern/sequences](winwincode-automatic-report.json#/functional_chains/17/pattern/sequences) |
| sequences/control/conditions/0/condition/operand/arguments/0/runtime_value_proven | false | [/functional_chains/17/pattern/sequences](winwincode-automatic-report.json#/functional_chains/17/pattern/sequences) |
| sequences/control/conditions/0/condition/operand/arguments/0/source | &#124;_&#124; workspace_error() | [/functional_chains/17/pattern/sequences](winwincode-automatic-report.json#/functional_chains/17/pattern/sequences) |
| sequences/control/conditions/0/condition/operand/arguments/0/source_truncated | false | [/functional_chains/17/pattern/sequences](winwincode-automatic-report.json#/functional_chains/17/pattern/sequences) |
| sequences/control/conditions/0/condition/operand/callee_expression/current_referent_value_proven | false | [/functional_chains/17/pattern/sequences](winwincode-automatic-report.json#/functional_chains/17/pattern/sequences) |
| sequences/control/conditions/0/condition/operand/callee_expression/kind | field_expression | [/functional_chains/17/pattern/sequences](winwincode-automatic-report.json#/functional_chains/17/pattern/sequences) |
| sequences/control/conditions/0/condition/operand/callee_expression/location/file | crates/winwincode-worker/src/lib.rs | [/functional_chains/17/pattern/sequences](winwincode-automatic-report.json#/functional_chains/17/pattern/sequences) |
| sequences/control/conditions/0/condition/operand/callee_expression/location/line | 772 | [/functional_chains/17/pattern/sequences](winwincode-automatic-report.json#/functional_chains/17/pattern/sequences) |
| sequences/control/conditions/0/condition/operand/callee_expression/location/column | 20 | [/functional_chains/17/pattern/sequences](winwincode-automatic-report.json#/functional_chains/17/pattern/sequences) |

完整关系 [/functional_chains/17/pattern](winwincode-automatic-report.json#/functional_chains/17/pattern)；原 source facts [/functional_chains/17/source_facts](winwincode-automatic-report.json#/functional_chains/17/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

### WorkRun 可运行状态与依赖条件 · `wwc-report-workrun-finite-selection`

`rust_finite_state_selection`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`409a9e2d1a7a8b93c1cd532b`；Evidence=`e8cc08b5caa05bbb67bb6610`。
源码/关系 [/functional_chains/18](winwincode-automatic-report.json#/functional_chains/18)；缺段 [/functional_chains/18/analysis_gaps](winwincode-automatic-report.json#/functional_chains/18/analysis_gaps)；模型 [/functional_chains/18/trusted_models](winwincode-automatic-report.json#/functional_chains/18/trusted_models)；policy [/functional_chains/18/policy_declarations](winwincode-automatic-report.json#/functional_chains/18/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

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

`runnable_table_rows`；完整 [/functional_chains/18/pattern/finite_source_countercases/runnable_table_rows](winwincode-automatic-report.json#/functional_chains/18/pattern/finite_source_countercases/runnable_table_rows)；保存总行数 `2`。

| effective_state | input_state | runnable | source_quantifiers | 完整行 |
| --- | --- | --- | --- | --- |
| WorkItemState::Ready | WorkItemState::Ready | true | {"source_quantifier_1":false} | [/functional_chains/18/pattern/finite_source_countercases/runnable_table_rows/0](winwincode-automatic-report.json#/functional_chains/18/pattern/finite_source_countercases/runnable_table_rows/0) |
| WorkItemState::Ready | WorkItemState::WaitingDependency | true | {"source_quantifier_1":false} | [/functional_chains/18/pattern/finite_source_countercases/runnable_table_rows/1](winwincode-automatic-report.json#/functional_chains/18/pattern/finite_source_countercases/runnable_table_rows/1) |

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

### WorkRun 校验与重复 guard · `wwc-report-workrun-state-guards`

`state_guard_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`iterator_selection_and_macro_runtime_semantics_not_fully_proven`；Finding=`db018b5abf4fca55e9128fa0`；Evidence=`e7a534c5885572a4f7dd2ec5`。
源码/关系 [/functional_chains/19](winwincode-automatic-report.json#/functional_chains/19)；缺段 [/functional_chains/19/analysis_gaps](winwincode-automatic-report.json#/functional_chains/19/analysis_gaps)；模型 [/functional_chains/19/trusted_models](winwincode-automatic-report.json#/functional_chains/19/trusted_models)；policy [/functional_chains/19/policy_declarations](winwincode-automatic-report.json#/functional_chains/19/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 3 表、每表 12 行及 24 个字段）：

| 保存关系字段 | 保存值 | 原值位置 |
| --- | --- | --- |
| scoped_source_supported | true | [/functional_chains/19/pattern/scoped_source_supported](winwincode-automatic-report.json#/functional_chains/19/pattern/scoped_source_supported) |
| all_active_states_or_attempts_proven | false | [/functional_chains/19/pattern/all_active_states_or_attempts_proven](winwincode-automatic-report.json#/functional_chains/19/pattern/all_active_states_or_attempts_proven) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/0/location/file | crates/winwincode-delivery/src/application/workrun.rs | [/functional_chains/19/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/19/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/0/location/line | 392 | [/functional_chains/19/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/19/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/0/location/column | 9 | [/functional_chains/19/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/19/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/0/location/end_line | 392 | [/functional_chains/19/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/19/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/0/location/start_byte | 14655 | [/functional_chains/19/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/19/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/0/location/end_byte | 14670 | [/functional_chains/19/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/19/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/0/role | selection | [/functional_chains/19/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/19/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/1/location/file | crates/winwincode-delivery/src/application/workrun.rs | [/functional_chains/19/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/19/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/1/location/line | 419 | [/functional_chains/19/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/19/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/1/location/column | 9 | [/functional_chains/19/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/19/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/1/location/end_line | 419 | [/functional_chains/19/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/19/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/1/location/start_byte | 15641 | [/functional_chains/19/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/19/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/1/location/end_byte | 15656 | [/functional_chains/19/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/19/pattern/repeated_first_callee) |
| repeated_first_callee/rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate/1/role | start | [/functional_chains/19/pattern/repeated_first_callee](winwincode-automatic-report.json#/functional_chains/19/pattern/repeated_first_callee) |
| selection_predicate_sources/shown_items/0/callback_activation_proven | false | [/functional_chains/19/pattern/selection_predicate_sources](winwincode-automatic-report.json#/functional_chains/19/pattern/selection_predicate_sources) |
| selection_predicate_sources/shown_items/0/expression/kind | macro_invocation | [/functional_chains/19/pattern/selection_predicate_sources](winwincode-automatic-report.json#/functional_chains/19/pattern/selection_predicate_sources) |
| selection_predicate_sources/shown_items/0/expression/location/file | crates/winwincode-delivery/src/application/workrun.rs | [/functional_chains/19/pattern/selection_predicate_sources](winwincode-automatic-report.json#/functional_chains/19/pattern/selection_predicate_sources) |
| selection_predicate_sources/shown_items/0/expression/location/line | 397 | [/functional_chains/19/pattern/selection_predicate_sources](winwincode-automatic-report.json#/functional_chains/19/pattern/selection_predicate_sources) |
| selection_predicate_sources/shown_items/0/expression/location/column | 17 | [/functional_chains/19/pattern/selection_predicate_sources](winwincode-automatic-report.json#/functional_chains/19/pattern/selection_predicate_sources) |
| selection_predicate_sources/shown_items/0/expression/location/end_line | 400 | [/functional_chains/19/pattern/selection_predicate_sources](winwincode-automatic-report.json#/functional_chains/19/pattern/selection_predicate_sources) |
| selection_predicate_sources/shown_items/0/expression/location/start_byte | 14781 | [/functional_chains/19/pattern/selection_predicate_sources](winwincode-automatic-report.json#/functional_chains/19/pattern/selection_predicate_sources) |
| selection_predicate_sources/shown_items/0/expression/location/end_byte | 14935 | [/functional_chains/19/pattern/selection_predicate_sources](winwincode-automatic-report.json#/functional_chains/19/pattern/selection_predicate_sources) |

完整关系 [/functional_chains/19/pattern](winwincode-automatic-report.json#/functional_chains/19/pattern)；原 source facts [/functional_chains/19/source_facts](winwincode-automatic-report.json#/functional_chains/19/source_facts)。原投影截取标志 `true`；本摘要预算截取标志 `true`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。

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
| `cold` | `partial` | `true` | `cc327a390837a897be93cdd4bdd4d9ad652c47f70f0b0dbfbbf89a52b463d372` |
| `warm` | `partial` | `false` | `cc327a390837a897be93cdd4bdd4d9ad652c47f70f0b0dbfbbf89a52b463d372` |

这张表复制保存发布记录；partial 是图/解析范围状态，不能据此覆盖上方判断结论。完整记录见 [integration](winwincode-integration.json)。
