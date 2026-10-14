# CallScope v0.13.0：原报告范围内的自动静态判断

本轮以原 [CodePatchBay](../astra-baseline/CODEPATCHBAY_ANALYSIS.md) 和 [WinWinCode](../astra-baseline/WINWINCODE_ANALYSIS.md) 分析报告为功能基准。具体判断、主要链的源码关系、项目结构盘点和全文范围对照分别保存；没有新增重复 Astra 审批。

正式保存结果包含 5 项原判断、30 项关系：5 项完整裁决，5 项完整支持原 claim。这是本题样本的实际结果，不是全项目功能覆盖率或缺陷通过率。

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

旧 pending/assignment、finalizer、不同重试预算、opaque supervisor、导航与提交环境、Device/Chat/local 分支及失败操作仍各自限制结论。

## 主要链、结构与全文范围

正式报告有 31 个所选主要链条目；源码关系状态为 `{"scoped_source_relations_supported":31}`。其中 `captured_source_structure_supported=true` 为 31 项，`scoped_source_supported=true` 为 31 项。结构抽取与包含实际装配/guard 的源码支持是不同字段；partial 条目保留具体缺段。

这些条目描述所选声明和正常分支的静态关系，均不自动证明完整运行功能。相同源 selector 的重叠在自动报告单列，不累计为额外能力；目录、依赖图、解析文件及 AST anchor 数量也不构成功能覆盖率。

## 本轮保存的具体条件与字段关系

以下只复制正式报告 v2 的关系投影，包含实际门条件、状态枚举、记录字段与必要未知；不是根据规则名生成新结论。完整表达式、source facts 与反证以相应 JSON Pointer 为准。

### `cpb-captured-record-resource-writers`

保存状态 `scoped_source_relations_supported`；保存缺口 `[]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

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

### `cpb-event-index-projection`

保存状态 `scoped_source_relations_supported`；保存缺口 `[{"code":"record_projection_physical_commit_and_all_recovery_not_proven","source_only":true}]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

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

### `cpb-report-access-audit-response`

保存状态 `scoped_source_relations_supported`；保存缺口 `[]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

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

### `cpb-report-completion-gate-conditions`

保存状态 `scoped_source_relations_supported`；保存缺口 `[]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

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

### `cpb-report-readiness-abrupt-guard`

保存状态 `scoped_source_relations_supported`；保存缺口 `[]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

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

### `cpb-trusted-command-lineage`

保存状态 `scoped_source_relations_supported`；保存缺口 `[{"code":"record_command_source_dependencies_do_not_prove_full_heap_noninterference","source_only":true}]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

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

### `cpb-unsupported-record-retention`

保存状态 `scoped_source_relations_supported`；保存缺口 `[{"code":"record_true_marker_does_not_prove_all_input_or_artifact_retention","source_only":true}]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

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

### `wwc-browser-continuation-lifecycle`

保存状态 `scoped_source_relations_supported`；保存缺口 `[]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

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

### `wwc-captured-record-resource-writers`

保存状态 `scoped_source_relations_supported`；保存缺口 `[]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

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

### `wwc-report-chat-retained-request-identities`

保存状态 `scoped_source_relations_supported`；保存缺口 `[]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

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

### `wwc-report-outbox-ack-correlation-fields`

保存状态 `scoped_source_relations_supported`；保存缺口 `[]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

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

### `wwc-report-worker-adapter-record-identities`

保存状态 `scoped_source_relations_supported`；保存缺口 `[]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

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

### `wwc-report-workrun-finite-selection`

保存状态 `scoped_source_relations_supported`；保存缺口 `[]`。

保存的具体关系（仅展示投影，不增加分析或评分；每链至多 2 表、每表 12 行及 24 个字段）：

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
| codepatchbay | `7b58e73339e7ad28592c4a0bede1da0028935b30edd940419841971b354c2bfe` | partial | 333 / 330 | 11085 / 60571 | True / False |
| winwincode | `cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2` | partial | 471 / 465 | 32407 / 171939 | True / False |

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

- **codepatchbay**：policy 字节相同=`false`；变化 section=`["report_claims"]`；捕获 source hash 与 v12 相同=`true`。inert 支持输入 2 项；原引用源文件 hash 与 target commit 由 publication identity 单独核对。
- **winwincode**：policy 字节相同=`false`；变化 section=`["report_claims"]`；捕获 source hash 与 v12 相同=`true`。inert 支持输入 11 项；原引用源文件 hash 与 target commit 由 publication identity 单独核对。

输入捕获范围改变不等于目标代码发生修改。受信模型和环境条件不填补尚未建立的源连接；旧 field/IR 的 unknown 不因新局部 record 关系被升级。无运行、浏览器、网络、并发或业务验收证明。

## 原 26 条观察与交付身份

原冻结观察保留 26 条，总计比较 26 条，状态为 `{"ambiguous":0,"endpoint_missing":0,"evidence_only":13,"evidence_unavailable":0,"mismatch":0,"reproduced":10,"source_changed":0,"source_missing":0,"unknown":3}`；相对 v12 的保存变化记录为 0 项。evidence_only 和指定 unknown 仍遵循原 evaluator；观察重现数量不是完整功能判断数量。

包版本 `0.13.0`，analyzer `static-multilang-13`，detector `call-rules-12-report-relations`，schema `2`。冻结 tool source hash：`c4c127375f044133c328c1fd17782df277426bf64e4bed0be8779602088fafee`。

[CORE_FREEZE.json](CORE_FREEZE.json) 的 60 份核心 Python 源码 live/archive hash 一致，AST 可解析；此项只是身份/语法核对。正式身份产物记录原引用的 36 份文件 saved/live hash 一致，两库 target commit 一致；没有宣称工作区 clean。两库和共有组件的正式 publication identity 已验证；本报告没有再次执行检测器或读取数据库。

- [CodePatchBay 自动报告](codepatchbay-automatic-report.md)与[扫描记录](codepatchbay-integration.json)。
- [WinWinCode 自动报告](winwincode-automatic-report.md)与[扫描记录](winwincode-integration.json)。
- [CodePatchBay 简明分析](codepatchbay-analysis-summary.md)、[WinWinCode 简明分析](winwincode-analysis-summary.md)。
- [原五项结果账本](goal-ledger.json)、[原 26 条比较](ORIGINAL_BASELINE_COMPARISON.json)、[正式身份](PUBLICATION_IDENTITY.json)。
- [全文范围对照](REPORT_ALIGNMENT_RESULTS.json)、[本报告输入与核对记录](RELEASE_REPORT_INPUTS.json)。

[正常 report CLI 读回记录](CLI_REPORT_READBACK.json) 确认 WinWinCode 的 [导出 Markdown](winwincode-cli-report-readback.md) 与[正式 Markdown](winwincode-automatic-report.md) 字节一致，属于保存快照 `cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2`。该 CLI 没有重扫或重算检测器；普通 Store 初始化已记录，其连接不是只读连接，前后逻辑行/Schema/身份指纹保持一致。数据库物理字节相同=`false`，不把初始化视为无物理效果。本生成器只核对保存记录及 Markdown hash，没有重跑 CLI 或打开数据库。

[原全文与当前自动报告的具体差距](REPORT_SCOPE_GAPS.md) 分列原已读但尚无同等自动结论的段落、源码边界与原明确未审范围；其导航不增加新评分或审批。
