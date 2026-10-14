# CodePatchBay · 保存的自动分析摘要

此摘要只展示已保存正式报告的结果和证据导航；不重新分析、不新增评价，也不替代完整证据。
五项判断是实现追踪，不是全文报告或项目功能覆盖率。链标题只是规则 ID 的展示标签。

- 固定全文基准：[原分析报告](../astra-baseline/CODEPATCHBAY_ANALYSIS.md)；不设置重复 Astra 审批步骤。
- 完整自动报告：[Markdown](codepatchbay-automatic-report.md) / [JSON](codepatchbay-automatic-report.json)；[正式 integration](codepatchbay-integration.json)。
- 快照：`7524afef4f9234ebef40eec1d74dbb91a3f56dc76f0191728c42d3bdd3cfb167`；状态：`partial`；报告版本：`captured-project-analysis-report-1`。
- 实现：`0.12.0` / `static-multilang-12` / `call-rules-11-whole-judgments`。
- 源码身份：`4e07250709288887cd79ae51b5f23f0239e054bc1db40371f7e7d0609148791b`。
- 策略身份：`c11c67291de2eb257c6b6195cae16f92333abe2f9ca323881403c954cd737714`。
- 保存 JSON SHA256：`6ff36204cda0ceb12fe15e8d1dc2e999ad71bc9d59d3d87faedb449816d58eb9`；integration SHA256：`5f349e2731d32346ea5dd3a248671ceaec5f2a04708caf190bb56050ce032217`。
- 保存比较范围：New source models and inert support inputs; not a same-policy precision experiment.

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
Finding=`c5702ff61b2fe477fb28b9dc`；Evidence=`71f6cf7c7a31d0977b4c9a06`；保存 evidence 指针=`/evidence/0/details`（相对于该 Finding）。
完整 [/judgments/0](codepatchbay-automatic-report.json#/judgments/0)；条件 [/judgments/0/conditions](codepatchbay-automatic-report.json#/judgments/0/conditions)；反证 [/judgments/0/refutations](codepatchbay-automatic-report.json#/judgments/0/refutations)；缺口 [/judgments/0/necessary_gaps](codepatchbay-automatic-report.json#/judgments/0/necessary_gaps)。

### `CPB-02`

状态 `superseded` 在所选身份条件下的终态谓词结果为 `False`，权威终态集合成员关系为 `True`；消费者据此进入拒绝分支。恢复政策和权威写入保护分别保存。

derived_judgment：`{"authority_terminal_membership":true,"classification_differs":true,"kind":"conditional_terminal_classification_difference","recovery_is_required_or_authorized":false,"status":"superseded","terminal_state_can_be_illegally_mutated":false,"valid_identity_predicate_result":false}`
assessment=`scoped_static_judgment_reproduced`；complete=`true`；support=`true`。
必要义务（原状态）：`S1=supported, S2=supported, S3=supported, S4=supported, S5=supported`；必要缺口：`[]`。
Finding=`4b842226073458a0e78e4030`；Evidence=`042e5b5d63099be326f960a9`；保存 evidence 指针=`/evidence/0/details`（相对于该 Finding）。
完整 [/judgments/1](codepatchbay-automatic-report.json#/judgments/1)；条件 [/judgments/1/conditions](codepatchbay-automatic-report.json#/judgments/1/conditions)；反证 [/judgments/1/refutations](codepatchbay-automatic-report.json#/judgments/1/refutations)；缺口 [/judgments/1/necessary_gaps](codepatchbay-automatic-report.json#/judgments/1/necessary_gaps)。

### `CPB-03`

预查与权威写入的去重口径不同；从实际保护区和状态转换生成的有限交错可产生重复非终态记录，同时保存可以复用的顺序和失败条件。

derived_judgment：`"Two same-project/key/description default submissions can both observe no row; the first protected insert can be guardedly scheduled before the second protected check; the pending-only inner check then inserts a second nonterminal row"`
assessment=`scoped_static_judgment_reproduced`；complete=`true`；support=`true`。
必要义务（原状态）：`A1=supported, A2=supported, A3=supported, A4=supported, A5=supported, A6=supported, A7=supported`；必要缺口：`[]`。
Finding=`a6270e2d476c805d8c26eb60`；Evidence=`78f93f2d73951286ebc21de9`；保存 evidence 指针=`/evidence/0/details`（相对于该 Finding）。
完整 [/judgments/2](codepatchbay-automatic-report.json#/judgments/2)；条件 [/judgments/2/conditions](codepatchbay-automatic-report.json#/judgments/2/conditions)；反证 [/judgments/2/refutations](codepatchbay-automatic-report.json#/judgments/2/refutations)；缺口 [/judgments/2/necessary_gaps](codepatchbay-automatic-report.json#/judgments/2/necessary_gaps)。

## 所选主要源码链

显示每条保存规则的实际 assessment 和缺口；source-structure 支持与目标分派闭合分开。

### agent allowlist / env / sandbox 策略 · `cpb-report-agent-execution-policy`

`agent_execution_policy`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`b58297963754231cc9ac5d97`；Evidence=`d07d8e902cb2715e8db77901`。
源码/关系 [/functional_chains/0](codepatchbay-automatic-report.json#/functional_chains/0)；缺段 [/functional_chains/0/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/0/analysis_gaps)；模型 [/functional_chains/0/trusted_models](codepatchbay-automatic-report.json#/functional_chains/0/trusted_models)；policy [/functional_chains/0/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/0/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

### finalizer → 结果写入 → reconcile · `cpb-report-conditional-delivery-result`

`conditional_delivery_result`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`b42e6e3c72ff9fca487df6a5`；Evidence=`5b31563bcc5fe588caca8969`。
源码/关系 [/functional_chains/1](codepatchbay-automatic-report.json#/functional_chains/1)；缺段 [/functional_chains/1/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/1/analysis_gaps)；模型 [/functional_chains/1/trusted_models](codepatchbay-automatic-report.json#/functional_chains/1/trusted_models)；policy [/functional_chains/1/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/1/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

### runJob 主链与前置阻断 · `cpb-report-engine-stage-chain`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`a5f66e48c73762d3fe92d558`；Evidence=`a8377019831698f83b53ea70`。
源码/关系 [/functional_chains/2](codepatchbay-automatic-report.json#/functional_chains/2)；缺段 [/functional_chains/2/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/2/analysis_gaps)；模型 [/functional_chains/2/trusted_models](codepatchbay-automatic-report.json#/functional_chains/2/trusted_models)；policy [/functional_chains/2/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/2/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

### audit best-effort 分支 · `cpb-report-job-audit-best-effort`

`best_effort_finalization`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`e2a338b6d888b78c028f0f07`；Evidence=`c52e46cfc1ab72f22322f302`。
源码/关系 [/functional_chains/3](codepatchbay-automatic-report.json#/functional_chains/3)；缺段 [/functional_chains/3/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/3/analysis_gaps)；模型 [/functional_chains/3/trusted_models](codepatchbay-automatic-report.json#/functional_chains/3/trusted_models)；policy [/functional_chains/3/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/3/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

### trusted probe 命令来源 · `cpb-report-trusted-probe-command-source`

`structured_command_source`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`structured_command_intermediate_values_and_external_effects_not_fully_proven`；Finding=`2fd6c4cf74d19d9b3ceed0b2`；Evidence=`af7b9396eac4030b8880e980`。
源码/关系 [/functional_chains/4](codepatchbay-automatic-report.json#/functional_chains/4)；缺段 [/functional_chains/4/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/4/analysis_gaps)；模型 [/functional_chains/4/trusted_models](codepatchbay-automatic-report.json#/functional_chains/4/trusted_models)；policy [/functional_chains/4/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/4/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

### unsupported probe 失败证据 · `cpb-report-unsupported-probe-evidence`

`unsupported_method_evidence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`structured_record_markers_do_not_prove_all_input_retention_or_persistence`；Finding=`346b54291f475e2948de3ce0`；Evidence=`4d65f8a475e5f5893d16a0d6`。
源码/关系 [/functional_chains/5](codepatchbay-automatic-report.json#/functional_chains/5)；缺段 [/functional_chains/5/analysis_gaps](codepatchbay-automatic-report.json#/functional_chains/5/analysis_gaps)；模型 [/functional_chains/5/trusted_models](codepatchbay-automatic-report.json#/functional_chains/5/trusted_models)；policy [/functional_chains/5/policy_declarations](codepatchbay-automatic-report.json#/functional_chains/5/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

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
| `cold` | `partial` | `true` | `7524afef4f9234ebef40eec1d74dbb91a3f56dc76f0191728c42d3bdd3cfb167` |
| `warm` | `partial` | `false` | `7524afef4f9234ebef40eec1d74dbb91a3f56dc76f0191728c42d3bdd3cfb167` |

这张表复制保存发布记录；partial 是图/解析范围状态，不能据此覆盖上方判断结论。完整记录见 [integration](codepatchbay-integration.json)。
