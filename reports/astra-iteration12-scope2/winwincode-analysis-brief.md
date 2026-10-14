# WinWinCode · 代码层静态分析简报

只重排已保存正式报告的实际值；没有重新分析或新增评价。章节标题仅供导航，不是结论来源。
快照 `cc327a390837a897be93cdd4bdd4d9ad652c47f70f0b0dbfbbf89a52b463d372`；[完整报告](winwincode-automatic-report.json)。
保存关系状态：`{"scoped_source_relations_supported":20}`。所选有限源码关系的支持状态不是功能覆盖率；未知、条件和反证仍按原证据保留。

## 原具体问题

- **WWC-01**：所选公开导航未提供消费者必需的查询上下文；经真实生产装配与缺值传播，创建在提交命令前被拒绝。有效上下文和替代创建入口是反证。 完整判断=`true`；支持=`true`；[条件、反证与证据](winwincode-automatic-report.json#/judgments/0)。
- **WWC-02**：所选提交对象遗漏条件分支必填字段；经过生成协议、普通 JSON 与 Serde 映射后，权威非空守卫在使用或提交前拒绝。其它分支和显式字段来源是反证。 完整判断=`true`；支持=`true`；[条件、反证与证据](winwincode-automatic-report.json#/judgments/1)。

## 主要有限源码关系

每项最多列两条实际关系和一条边界；大字段、源码位置、hash 与事实 ID 留在原 JSON Pointer。表格仅复制保存的有限输入分区，未执行这些输入。

### 渲染代次与异步回写条件

- 实际关系 `scope_conditions`：`["selected captured callables and nested callbacks are invoked and their recorded branches are reached normally","generation tokens compare captured lexical declarations, without asserting current counter values","standard AbortController/DOM behavior is an explicit source model, not observed browser behavior","a parent guard is never inherited across a nested callback or an intervening suspension"]`；[保存值](winwincode-automatic-report.json#/functional_chains/0/pattern/scope_conditions)。
- 实际条件/接线 `closed_result_disposal_consumers/0/close_before_normal_return`：`true`；[保存值](winwincode-automatic-report.json#/functional_chains/0/pattern/closed_result_disposal_consumers/0/close_before_normal_return)。
- 保留边界 `all_async_callbacks_guarded_proven`：`false`；[保存值](winwincode-automatic-report.json#/functional_chains/0/pattern/all_async_callbacks_guarded_proven)。

### WinWinCode 记录与资源写者

- 实际关系 `ownership_assessment`：`partial_captured_writers_and_consumers`；[保存值](winwincode-automatic-report.json#/functional_chains/1/pattern/ownership_assessment)。
- 实际条件/接线 `responsibility_interpretation`：`Selected captured functions write the recorded lexical fields and pass the recorded arguments; directory names assign no responsibility.`；[保存值](winwincode-automatic-report.json#/functional_chains/1/pattern/responsibility_interpretation)。
- 保留边界 `all_mutations_authorized_proven`：`false`；[保存值](winwincode-automatic-report.json#/functional_chains/1/pattern/all_mutations_authorized_proven)。

### wwc-delivery-evidence-frozen-contract-slice

- 实际关系 `sequences/canonical_evidence/orders/0/conditions`：`["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"]`；[保存值](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences/canonical_evidence/orders/0/conditions)。
- 实际条件/接线 `sequences/checkout_guard/conditions/0/condition/operands/0/callee_source`：`checkout_identity`；[保存值](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences/checkout_guard/conditions/0/condition/operands/0/callee_source)。
- 保留边界 `sequences/canonical_evidence/future_or_callback_activation_proven`：`false`；[保存值](winwincode-automatic-report.json#/functional_chains/2/pattern/sequences/canonical_evidence/future_or_callback_activation_proven)。

### Provider 文档与部署范围比较

- 实际关系 `relation_witnesses`：`{"device_message_body_connects_local_store_to_model_callback_source":true,"local_execute_contains_selected_invoke_source":true,"local_factory_reads_endpoint_and_constructs_provider_candidate":true,"local_resolver_passes_captured_byte_material_to_secret_constructor":true}`；另 7 项见原值；[保存值](winwincode-automatic-report.json#/functional_chains/3/pattern/relation_witnesses)。
- 实际条件/接线 `conditions`：`["captured selected production methods and deferred callbacks are activated and reached normally in the selected Device composition","ordinary Rust lexical shadowing, Option/Result callback source contracts and plain captured records apply","literal SQL describes selected columns under ordinary rusqlite source contracts; no query is executed","selected provider implementation is a contextual source candidate; ordinary trait dispatch is not globally repaired"]`；[保存值](winwincode-automatic-report.json#/functional_chains/3/pattern/conditions)。
- 保留边界 `whole_report_reproduction_claimed`：`false`；[保存值](winwincode-automatic-report.json#/functional_chains/3/pattern/whole_report_reproduction_claimed)。

### Adapter durable / exact turn

- 实际关系 `sequences/adapter_submit/conditions/1/condition/operands/1/callee_source`：`run.record.format_repair.is_some`；[保存值](winwincode-automatic-report.json#/functional_chains/4/pattern/sequences/adapter_submit/conditions/1/condition/operands/1/callee_source)。
- 保留边界 `sequences/adapter_submit/conditions/0/runtime_predicate_proven`：`false`；[保存值](winwincode-automatic-report.json#/functional_chains/4/pattern/sequences/adapter_submit/conditions/0/runtime_predicate_proven)。

### Chat 请求与 WorkItem / WorkRun

- 保留边界 `sequences/builder/conditions/0/runtime_predicate_proven`：`false`；[保存值](winwincode-automatic-report.json#/functional_chains/5/pattern/sequences/builder/conditions/0/runtime_predicate_proven)。

### Chat 请求身份与字段保留

- 实际关系 `components/chat_request_identity/supported`：`true`；[保存值](winwincode-automatic-report.json#/functional_chains/6/pattern/components/chat_request_identity/supported)。
- 实际条件/接线 `components/chat_request_identity/builder_call_relations/0/supported`：`true`；[保存值](winwincode-automatic-report.json#/functional_chains/6/pattern/components/chat_request_identity/builder_call_relations/0/supported)。
- 保留边界 `runtime_transport_or_physical_effect_proven`：`false`；[保存值](winwincode-automatic-report.json#/functional_chains/6/pattern/runtime_transport_or_physical_effect_proven)。

### Device provider 部署分流

- 实际关系 `boundary_results/0/expression/callee_source`：`Err`；[保存值](winwincode-automatic-report.json#/functional_chains/7/pattern/boundary_results/0/expression/callee_source)。
- 实际条件/接线 `installation_assignments/0/right/callee_source`：`Some`；[保存值](winwincode-automatic-report.json#/functional_chains/7/pattern/installation_assignments/0/right/callee_source)。
- 保留边界 `deployments_or_provider_implementations_equivalent`：`false`；[保存值](winwincode-automatic-report.json#/functional_chains/7/pattern/deployments_or_provider_implementations_equivalent)。

### Kernel create_session 接口

- 实际关系 `nested_source_regions/0/conditions`：`["this deferred captured body is activated and the recorded statements are reached normally"]`；[保存值](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions/0/conditions)。
- 实际条件/接线 `nested_source_regions/0/sequence/orders/0/conditions`：`["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"]`；[保存值](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions/0/sequence/orders/0/conditions)。
- 保留边界 `nested_source_regions/0/body_activation_proven`：`false`；[保存值](winwincode-automatic-report.json#/functional_chains/8/pattern/nested_source_regions/0/body_activation_proven)。

### Kernel reconcile_turn_exact 接口

- 实际关系 `nested_source_regions/0/conditions`：`["this deferred captured body is activated and the recorded statements are reached normally"]`；[保存值](winwincode-automatic-report.json#/functional_chains/9/pattern/nested_source_regions/0/conditions)。
- 实际条件/接线 `sequences/kernel_reconcile/conditions/0/condition/operands/0/callee_source`：`turn_id.trim().is_empty`；[保存值](winwincode-automatic-report.json#/functional_chains/9/pattern/sequences/kernel_reconcile/conditions/0/condition/operands/0/callee_source)。
- 保留边界 `nested_source_regions/0/body_activation_proven`：`false`；[保存值](winwincode-automatic-report.json#/functional_chains/9/pattern/nested_source_regions/0/body_activation_proven)。

### Kernel submit_turn 接口

- 实际关系 `nested_source_regions/0/conditions`：`["this deferred captured body is activated and the recorded statements are reached normally"]`；[保存值](winwincode-automatic-report.json#/functional_chains/10/pattern/nested_source_regions/0/conditions)。
- 实际条件/接线 `sequences/kernel_submit/conditions/0/condition/callee_expression/object/callee_source`：`text.trim`；[保存值](winwincode-automatic-report.json#/functional_chains/10/pattern/sequences/kernel_submit/conditions/0/condition/callee_expression/object/callee_source)。
- 保留边界 `nested_source_regions/0/body_activation_proven`：`false`；[保存值](winwincode-automatic-report.json#/functional_chains/10/pattern/nested_source_regions/0/body_activation_proven)。

### 发件记录与确认关联字段

- 实际关系 `components/outbox_ack_correlation/projection_agreements/0/ordered_field_paths`：`[["model_exchange_id"],["lease"],["worker_session_id"],["session_identity"]]`；[保存值](winwincode-automatic-report.json#/functional_chains/11/pattern/components/outbox_ack_correlation/projection_agreements/0/ordered_field_paths)。
- 实际条件/接线 `components/outbox_ack_correlation/projection_agreements/1/ordered_field_paths`：`[["model_exchange_id"],["lease"],["worker_session_id"],["session_identity"]]`；[保存值](winwincode-automatic-report.json#/functional_chains/11/pattern/components/outbox_ack_correlation/projection_agreements/1/ordered_field_paths)。
- 保留边界 `runtime_transport_or_physical_effect_proven`：`false`；[保存值](winwincode-automatic-report.json#/functional_chains/11/pattern/runtime_transport_or_physical_effect_proven)。

### ProductionAdapter → Kernel 构造

- 实际关系 `sequences/adapter_open/orders/0/conditions`：`["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"]`；[保存值](winwincode-automatic-report.json#/functional_chains/12/pattern/sequences/adapter_open/orders/0/conditions)。
- 实际条件/接线 `sequences/adapter_open/orders/1/conditions`：`["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"]`；[保存值](winwincode-automatic-report.json#/functional_chains/12/pattern/sequences/adapter_open/orders/1/conditions)。
- 保留边界 `sequences/adapter_open/future_or_callback_activation_proven`：`false`；[保存值](winwincode-automatic-report.json#/functional_chains/12/pattern/sequences/adapter_open/future_or_callback_activation_proven)。

### intent → persist → exact reconcile

- 实际关系 `sequences/submission/conditions/1/condition/operands/1/callee_source`：`run.record.format_repair.is_some`；[保存值](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences/submission/conditions/1/condition/operands/1/callee_source)。
- 保留边界 `sequences/submission/conditions/0/runtime_predicate_proven`：`false`；[保存值](winwincode-automatic-report.json#/functional_chains/13/pattern/sequences/submission/conditions/0/runtime_predicate_proven)。

### Worker 与 Adapter 的消息身份

- 实际关系 `components/worker_adapter_identity/components/adapter_ensure_thread/supported`：`true`；[保存值](winwincode-automatic-report.json#/functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/supported)。
- 实际条件/接线 `components/worker_adapter_identity/supported`：`true`；[保存值](winwincode-automatic-report.json#/functional_chains/14/pattern/components/worker_adapter_identity/supported)。
- 保留边界 `runtime_transport_or_physical_effect_proven`：`false`；[保存值](winwincode-automatic-report.json#/functional_chains/14/pattern/runtime_transport_or_physical_effect_proven)。

### Worker 入口分支

- 实际关系 `sequences/entry/orders/0/conditions`：`["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"]`；[保存值](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences/entry/orders/0/conditions)。
- 实际条件/接线 `sequences/managed/orders/0/conditions`：`["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"]`；[保存值](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences/managed/orders/0/conditions)。
- 保留边界 `sequences/entry/future_or_callback_activation_proven`：`false`；[保存值](winwincode-automatic-report.json#/functional_chains/15/pattern/sequences/entry/future_or_callback_activation_proven)。

### 生产 Worker 构造

- 实际关系 `sequences/adapter_factory/orders/0/conditions`：`["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"]`；[保存值](winwincode-automatic-report.json#/functional_chains/16/pattern/sequences/adapter_factory/orders/0/conditions)。
- 实际条件/接线 `sequences/adapter_factory/orders/1/conditions`：`["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"]`；[保存值](winwincode-automatic-report.json#/functional_chains/16/pattern/sequences/adapter_factory/orders/1/conditions)。
- 保留边界 `sequences/adapter_factory/future_or_callback_activation_proven`：`false`；[保存值](winwincode-automatic-report.json#/functional_chains/16/pattern/sequences/adapter_factory/future_or_callback_activation_proven)。

### Worker typed dispatch

- 实际关系 `sequences/control/conditions/0/condition/operand/callee_expression/object/callee_source`：`self                     .workspaces                     .is_observation_model_exchange`；[保存值](winwincode-automatic-report.json#/functional_chains/17/pattern/sequences/control/conditions/0/condition/operand/callee_expression/object/callee_source)。
- 实际条件/接线 `sequences/control/conditions/0/condition/operand/callee_source`：`self                     .workspaces                     .is_observation_model_exchange(&amp;chunk.model_exchange_id)                     .map_err`；[保存值](winwincode-automatic-report.json#/functional_chains/17/pattern/sequences/control/conditions/0/condition/operand/callee_source)。
- 保留边界 `sequences/control/conditions/0/runtime_predicate_proven`：`false`；[保存值](winwincode-automatic-report.json#/functional_chains/17/pattern/sequences/control/conditions/0/runtime_predicate_proven)。

### WorkRun 可运行状态与依赖条件

- 实际关系 `persisted_selection_recheck_relation/checks`：`{"active_collection_passed_to_selector_and_selected_id_rechecked":true,"aggregate_validation_collect_select_recheck_source_order":true,"both_selected_entries_have_fallible_validation_prefix":true,"runnable_predicate_in_both_find_conjunctions":true}`；另 5 项见原值；[保存值](winwincode-automatic-report.json#/functional_chains/18/pattern/persisted_selection_recheck_relation/checks)。
- 实际条件/接线 `source_model_conditions`：`["selected normal source bodies are reached and their fallible prefixes return Ok","captured plain matches! uses the standard Rust macro, not an external macro override","captured Vec/slice iterator, HashSet membership, field equality and Clone obey their standard source contracts","the recorded unique same-module helper source declarations are the invoked helpers; historical unresolved graph calls remain unchanged"]`；[保存值](winwincode-automatic-report.json#/functional_chains/18/pattern/source_model_conditions)。
- 保留边界 `all_active_states_or_attempts_proven`：`false`；[保存值](winwincode-automatic-report.json#/functional_chains/18/pattern/all_active_states_or_attempts_proven)。

保存的 `rows`：[完整表](winwincode-automatic-report.json#/functional_chains/18/pattern/finite_effective_state_relation/rows)；8/8 行。

| effective_state | input_state | runnable | source_quantifiers |
| --- | --- | --- | --- |
| WorkItemState::Done | WorkItemState::Done | false | {"source_quantifier_1":false} |
| WorkItemState::Done | WorkItemState::Done | false | {"source_quantifier_1":true} |
| WorkItemState::Ready | WorkItemState::Ready | true | {"source_quantifier_1":false} |
| WorkItemState::WaitingDependency | WorkItemState::Ready | false | {"source_quantifier_1":true} |
| WorkItemState::Ready | WorkItemState::WaitingDependency | true | {"source_quantifier_1":false} |
| WorkItemState::WaitingDependency | WorkItemState::WaitingDependency | false | {"source_quantifier_1":true} |
| &lt;other value of this state enum&gt; | &lt;other value of this state enum&gt; | false | {"source_quantifier_1":false} |
| &lt;other value of this state enum&gt; | &lt;other value of this state enum&gt; | false | {"source_quantifier_1":true} |

### WorkRun 校验与重复 guard

- 实际关系 `sequences/selection/orders/0/conditions`：`["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"]`；[保存值](winwincode-automatic-report.json#/functional_chains/19/pattern/sequences/selection/orders/0/conditions)。
- 实际条件/接线 `selection_predicate_sources/1/expression/operands/0/operands/1/callee_source`：`work_item_is_runnable`；[保存值](winwincode-automatic-report.json#/functional_chains/19/pattern/selection_predicate_sources/1/expression/operands/0/operands/1/callee_source)。
- 保留边界 `all_active_states_or_attempts_proven`：`false`；[保存值](winwincode-automatic-report.json#/functional_chains/19/pattern/all_active_states_or_attempts_proven)。

## 阅读边界

- 全文自动复现声明：`false`；运行功能验证：`false`。
- 写者来源的 partial assessment 不等于唯一事实所有者、规范权威或所有授权完整。
- 这份简报只选有意义保存值；省略的字段、完整条件、反证和必要缺口仍在各条完整 pattern、source facts 与原判断中。
- `unknown` / `false` 不被摘要改成通过；所选源码关系不证明 IO、远端响应、实际调度或全路径运行成功。
- 未执行目标代码、测试或构建；原始证据、已有 summary 和发布报告未修改。
