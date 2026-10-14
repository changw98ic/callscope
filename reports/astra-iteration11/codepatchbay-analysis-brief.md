# CodePatchBay · 代码层静态分析简报

只重排已保存正式报告的实际值；没有重新分析或新增评价。章节标题仅供导航，不是结论来源。
快照 `7b58e73339e7ad28592c4a0bede1da0028935b30edd940419841971b354c2bfe`；[完整报告](codepatchbay-automatic-report.json)。
保存关系状态：`{"scoped_source_relations_supported":13}`。两库 31 条有限源码关系的支持状态不是功能覆盖率；未知、条件和反证仍按原证据保留。

## 原具体问题

- **CPB-01**：提交选项与所读执行预算之间存在接线差异；参数构造、消息关系、消费者及不同重试预算分别得到源码证据，适用分支和不透明消费者保留。 完整判断=`true`；支持=`true`；[条件、反证与证据](codepatchbay-automatic-report.json#/judgments/0)。
- **CPB-02**：状态 `superseded` 在所选身份条件下的终态谓词结果为 `False`，权威终态集合成员关系为 `True`；消费者据此进入拒绝分支。恢复政策和权威写入保护分别保存。 完整判断=`true`；支持=`true`；[条件、反证与证据](codepatchbay-automatic-report.json#/judgments/1)。
- **CPB-03**：预查与权威写入的去重口径不同；从实际保护区和状态转换生成的有限交错可产生重复非终态记录，同时保存可以复用的顺序和失败条件。 完整判断=`true`；支持=`true`；[条件、反证与证据](codepatchbay-automatic-report.json#/judgments/2)。

## 主要有限源码关系

每项最多列两条实际关系和一条边界；大字段、源码位置、hash 与事实 ID 留在原 JSON Pointer。表格仅复制保存的有限输入分区，未执行这些输入。

### CodePatchBay 记录与资源写者

- 实际关系 `ownership_assessment`：`partial_captured_writers_and_consumers`；[保存值](codepatchbay-automatic-report.json#/functional_chains/0/pattern/ownership_assessment)。
- 实际条件/接线 `responsibility_interpretation`：`Selected captured functions write the recorded lexical fields and pass the recorded arguments; directory names assign no responsibility.`；[保存值](codepatchbay-automatic-report.json#/functional_chains/0/pattern/responsibility_interpretation)。
- 保留边界 `all_mutations_authorized_proven`：`false`；[保存值](codepatchbay-automatic-report.json#/functional_chains/0/pattern/all_mutations_authorized_proven)。

### 事件提交与索引投影

- 实际关系 `relation_witnesses`：`{"append_calls_selected_durable_writer":true,"event_append_precedes_index_refresh_on_normal_reaching":true,"event_serializer_result_is_actual_durable_writer_argument":true,"index_rebuild_calls_same_index_writer":true}`；另 7 项见原值；[保存值](codepatchbay-automatic-report.json#/functional_chains/1/pattern/relation_witnesses)。
- 实际条件/接线 `normal_append_then_refresh_orders/0/conditions`：`["the same captured invocation reaches both statements normally","earlier awaited calls complete normally and intervening guards allow continuation"]`；[保存值](codepatchbay-automatic-report.json#/functional_chains/1/pattern/normal_append_then_refresh_orders/0/conditions)。
- 保留边界 `record_boundary/all_crash_recovery_interleavings_proven`：`false`；[保存值](codepatchbay-automatic-report.json#/functional_chains/1/pattern/record_boundary/all_crash_recovery_interleavings_proven)。

### 访问审计与响应字段

- 实际关系 `groups/access_audit/response_replacement_relations/0/conditions`：`["the captured registered request callback is invoked and reaches the awaited audit call","the selected opener, callback and response writer declarations are active","the audit await rejects or throws and catch logging completes normally","normal plain response object properties; no getters, Proxy or external mutation","intervening header operations and the response writer complete normally"]`；[保存值](codepatchbay-automatic-report.json#/functional_chains/2/pattern/groups/access_audit/response_replacement_relations/0/conditions)。
- 实际条件/接线 `groups/access_audit/response_replacement_relations/0/actual_response_writer_call/callee_source`：`sendJson`；[保存值](codepatchbay-automatic-report.json#/functional_chains/2/pattern/groups/access_audit/response_replacement_relations/0/actual_response_writer_call/callee_source)。
- 保留边界 `groups/access_audit/all_http_security_or_business_mutations_proven`：`false`；[保存值](codepatchbay-automatic-report.json#/functional_chains/2/pattern/groups/access_audit/all_http_security_or_business_mutations_proven)。

### agent allowlist / env / sandbox 策略

- 实际关系 `child_environment_filter/conditional_copy_attempts/0/guard/callee_source`：`predicate`；[保存值](codepatchbay-automatic-report.json#/functional_chains/3/pattern/child_environment_filter/conditional_copy_attempts/0/guard/callee_source)。
- 实际条件/接线 `admission_and_postexecution_review/execute_binding/callee_source`：`execPool.execute`；[保存值](codepatchbay-automatic-report.json#/functional_chains/3/pattern/admission_and_postexecution_review/execute_binding/callee_source)。
- 保留边界 `all_secrets_denied_proven`：`false`；[保存值](codepatchbay-automatic-report.json#/functional_chains/3/pattern/all_secrets_denied_proven)。

### 完成门条件与豁免

- 实际关系 `groups/completion/condition_consumers/0/condition_abstract_form`：`{"name":"checklist"}`；[保存值](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/condition_consumers/0/condition_abstract_form)。
- 实际条件/接线 `groups/completion/condition_consumers/0/condition_source`：`{"name":"checklist"}`；[保存值](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/condition_consumers/0/condition_source)。
- 保留边界 `groups/completion/checklist_internal_checks_proven`：`false`；[保存值](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/checklist_internal_checks_proven)。

保存的 `absent_input_partitions`：[完整表](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/absent_input_partitions)；2/2 行。

| boolean_result | input_cell | unknown |
| --- | --- | --- |
| false | missing | false |
| false | null | false |

保存的 `record_partitions`：[完整表](codepatchbay-automatic-report.json#/functional_chains/4/pattern/groups/completion/mutating_finite_enum_partition/record_partitions)；9/9 行。

| boolean_result | property_cells | unknown |
| --- | --- | --- |
| false | {"planMode":"none","workflow":"docs"} | false |
| false | {"planMode":"none","workflow":"readonly"} | false |
| false | {"planMode":"none","workflow":"&lt;other-than-captured-literals&gt;"} | false |
| false | {"planMode":"parent","workflow":"docs"} | false |
| false | {"planMode":"parent","workflow":"readonly"} | false |
| false | {"planMode":"parent","workflow":"&lt;other-than-captured-literals&gt;"} | false |
| false | {"planMode":"&lt;other-than-captured-literals&gt;","workflow":"docs"} | false |
| false | {"planMode":"&lt;other-than-captured-literals&gt;","workflow":"readonly"} | false |
| true | {"planMode":"&lt;other-than-captured-literals&gt;","workflow":"&lt;other-than-captured-literals&gt;"} | false |

### finalizer → 结果写入 → reconcile

- 实际关系 `components/finalizer/conditional_finalization/0/supported`：`true`；[保存值](codepatchbay-automatic-report.json#/functional_chains/5/pattern/components/finalizer/conditional_finalization/0/supported)。
- 实际条件/接线 `interpretation`：`The captured normal source chain separates execution, terminal delivery and queue projection; external I/O and provider outcomes remain conditional.`；[保存值](codepatchbay-automatic-report.json#/functional_chains/5/pattern/interpretation)。
- 保留边界 `all_recovery_complete_proven`：`false`；[保存值](codepatchbay-automatic-report.json#/functional_chains/5/pattern/all_recovery_complete_proven)。

### runJob 主链与前置阻断

- 实际关系 `sequences/entry/conditions/0/condition/operands/0/callee_source`：`isRecord`；[保存值](codepatchbay-automatic-report.json#/functional_chains/6/pattern/sequences/entry/conditions/0/condition/operands/0/callee_source)。
- 实际条件/接线 `sequences/entry/orders/0/conditions`：`["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"]`；[保存值](codepatchbay-automatic-report.json#/functional_chains/6/pattern/sequences/entry/orders/0/conditions)。
- 保留边界 `sequences/entry/future_or_callback_activation_proven`：`false`；[保存值](codepatchbay-automatic-report.json#/functional_chains/6/pattern/sequences/entry/future_or_callback_activation_proven)。

### audit best-effort 分支

- 保留边界 `audit_subject_equivalence_to_other_systems_proven`：`false`；[保存值](codepatchbay-automatic-report.json#/functional_chains/7/pattern/audit_subject_equivalence_to_other_systems_proven)。

### readiness 提交前保护

- 实际关系 `groups/readiness/relations/0/true_branch_always_abrupt`：`true`；[保存值](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups/readiness/relations/0/true_branch_always_abrupt)。
- 实际条件/接线 `groups/readiness/relations/0/conditions`：`["the selected entry and predicate declarations are active","the initializer and opaque calls before the return complete normally","the predicate reads the same stable ordinary result record; no getters, Proxy or external mutation"]`；[保存值](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups/readiness/relations/0/conditions)。
- 保留边界 `groups/readiness/readiness_implementation_success_or_external_state_proven`：`false`；[保存值](codepatchbay-automatic-report.json#/functional_chains/8/pattern/groups/readiness/readiness_implementation_success_or_external_state_proven)。

### trusted probe 命令来源

- 实际关系 `executions/0/same_parameter_field_source`：`true`；[保存值](codepatchbay-automatic-report.json#/functional_chains/9/pattern/executions/0/same_parameter_field_source)。
- 实际条件/接线 `lookups/0/arguments/0/callee_source`：`text`；[保存值](codepatchbay-automatic-report.json#/functional_chains/9/pattern/lookups/0/arguments/0/callee_source)。
- 保留边界 `expected_evidence_noninterference_proven`：`false`；[保存值](codepatchbay-automatic-report.json#/functional_chains/9/pattern/expected_evidence_noninterference_proven)。

### unsupported probe 失败证据

- 实际关系 `marker_consumption_guard_sources/0/condition/operands/1/operands/0/callee_source`：`Array.isArray`；[保存值](codepatchbay-automatic-report.json#/functional_chains/10/pattern/marker_consumption_guard_sources/0/condition/operands/1/operands/0/callee_source)。
- 实际条件/接线 `marker_assignment_attempts/1/branch_context/2/condition/callee_source`：`text`；[保存值](codepatchbay-automatic-report.json#/functional_chains/10/pattern/marker_assignment_attempts/1/branch_context/2/condition/callee_source)。
- 保留边界 `marker_field_business_meaning_inferred`：`false`；[保存值](codepatchbay-automatic-report.json#/functional_chains/10/pattern/marker_field_business_meaning_inferred)。

### 可信命令的字段来源

- 实际关系 `relation_witnesses`：`{"all_selected_direct_role_call_transfers":true,"execfile_stdout_json_decode_is_actual_policy_parser_input":true,"executor_reads_executable_and_args_from_same_command_formal":true,"loaded_policy_lookup_result_is_actual_command_runner_input":true}`；另 3 项见原值；[保存值](codepatchbay-automatic-report.json#/functional_chains/11/pattern/relation_witnesses)。
- 实际条件/接线 `loader_codec_joins/0/conditions`：`["registered ordinary Node execFile/promisify and JSON.parse source models"]`；[保存值](codepatchbay-automatic-report.json#/functional_chains/11/pattern/loader_codec_joins/0/conditions)。
- 保留边界 `command_boundary/expected_evidence_as_executable_source_proven`：`false`；[保存值](codepatchbay-automatic-report.json#/functional_chains/11/pattern/command_boundary/expected_evidence_as_executable_source_proven)。

### 未支持方法的失败记录

- 实际关系 `relation_witnesses`：`{"failure_records_append_to_returned_runner_collection":true,"ledger_claims_append_to_returned_evidence_collection":true,"plan_initializes_and_propagates_true_marker":true,"runner_emits_explicit_true_failure_record":true}`；另 3 项见原值；[保存值](codepatchbay-automatic-report.json#/functional_chains/12/pattern/relation_witnesses)。
- 实际条件/接线 `explicit_key_precedence_counter_sources/0/conditions`：`["ordinary Set membership and the captured iteration body are reached"]`；[保存值](codepatchbay-automatic-report.json#/functional_chains/12/pattern/explicit_key_precedence_counter_sources/0/conditions)。
- 保留边界 `retention_boundary/all_input_retention_or_artifact_durability_proven`：`false`；[保存值](codepatchbay-automatic-report.json#/functional_chains/12/pattern/retention_boundary/all_input_retention_or_artifact_durability_proven)。

## 阅读边界

- 全文自动复现声明：`false`；运行功能验证：`false`。
- 写者来源的 partial assessment 不等于唯一事实所有者、规范权威或所有授权完整。
- 这份简报只选有意义保存值；省略的字段、完整条件、反证和必要缺口仍在各条完整 pattern、source facts 与原判断中。
- `unknown` / `false` 不被摘要改成通过；所选源码关系不证明 IO、远端响应、实际调度或全路径运行成功。
- 未执行目标代码、测试或构建；原始证据、已有 summary 和发布报告未修改。
