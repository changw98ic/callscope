# WinWinCode · 保存的自动分析摘要

此摘要只展示已保存正式报告的结果和证据导航；不重新分析、不新增评价，也不替代完整证据。
五项判断是实现追踪，不是全文报告或项目功能覆盖率。链标题只是规则 ID 的展示标签。

- 固定全文基准：[原分析报告](../astra-baseline/WINWINCODE_ANALYSIS.md)；不设置重复 Astra 审批步骤。
- 完整自动报告：[Markdown](winwincode-automatic-report.md) / [JSON](winwincode-automatic-report.json)；[正式 integration](winwincode-integration.json)。
- 快照：`ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28`；状态：`partial`；报告版本：`captured-project-analysis-report-1`。
- 实现：`0.12.0` / `static-multilang-12` / `call-rules-11-whole-judgments`。
- 源码身份：`eb8e7cae7c2cd2b0503495033cc9a2a98c6e16b3d54b5a2f95dbdca24d118ab2`。
- 策略身份：`b1e290e7b61da9b404129887b1c41a4f86dcd5e25d7c851fb69822eda9ec4ac8`。
- 保存 JSON SHA256：`884202b5715f42c61a428479c18d91963b6452410a1f009855fd9a0ae130b8d7`；integration SHA256：`aa490b55676d6a3b184e32a99bf431ce3cc1b55e9ed53b07448e2ad3df9421ce`。
- 保存比较范围：New source models and inert support inputs; not a same-policy precision experiment.

## 保存范围与结构盘点

选入 `471` 文件，完整解析 `465`；文件状态 `{"parse_error":6,"parsed":465}`。
调用图保存 `32407` 节点、`171983` 边；确定调用 `16293`。这些是结构统计。
外部 `24597` / 动态 `129600` / 歧义 `62` / 未解析 `1431`；外部回调边界 `8559`。
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
Finding=`333b5dc5882abce976c0d9dc`；Evidence=`1f75ceee5eab722beeb2d270`；保存 evidence 指针=`/evidence/0/details`（相对于该 Finding）。
完整 [/judgments/0](winwincode-automatic-report.json#/judgments/0)；条件 [/judgments/0/conditions](winwincode-automatic-report.json#/judgments/0/conditions)；反证 [/judgments/0/refutations](winwincode-automatic-report.json#/judgments/0/refutations)；缺口 [/judgments/0/necessary_gaps](winwincode-automatic-report.json#/judgments/0/necessary_gaps)。

### `WWC-02`

所选提交对象遗漏条件分支必填字段；经过生成协议、普通 JSON 与 Serde 映射后，权威非空守卫在使用或提交前拒绝。其它分支和显式字段来源是反证。

derived_judgment：`"Under the explicitly retained normal production, JSON/Serde and active Device conditions, the closed UI command field omission reaches None and the nonblank authority guard rejects before criterion use/commit."`
assessment=`scoped_static_judgment_reproduced`；complete=`true`；support=`true`。
必要义务（原状态）：`D1=supported, D2=supported, D3=supported, D4=supported, D5=supported`；必要缺口：`[]`。
Finding=`89fc6bad0b0557c4623dd65b`；Evidence=`3a311ed2a8291589c7016d8c`；保存 evidence 指针=`/evidence/0/details`（相对于该 Finding）。
完整 [/judgments/1](winwincode-automatic-report.json#/judgments/1)；条件 [/judgments/1/conditions](winwincode-automatic-report.json#/judgments/1/conditions)；反证 [/judgments/1/refutations](winwincode-automatic-report.json#/judgments/1/refutations)；缺口 [/judgments/1/necessary_gaps](winwincode-automatic-report.json#/judgments/1/necessary_gaps)。

## 所选主要源码链

显示每条保存规则的实际 assessment 和缺口；source-structure 支持与目标分派闭合分开。

### Adapter durable / exact turn · `wwc-report-adapter-durable-exact-turn`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`a69caa6dc6cf3b4f882a90e0`；Evidence=`7bdcbe863990b55a37f4e094`。
源码/关系 [/functional_chains/0](winwincode-automatic-report.json#/functional_chains/0)；缺段 [/functional_chains/0/analysis_gaps](winwincode-automatic-report.json#/functional_chains/0/analysis_gaps)；模型 [/functional_chains/0/trusted_models](winwincode-automatic-report.json#/functional_chains/0/trusted_models)；policy [/functional_chains/0/policy_declarations](winwincode-automatic-report.json#/functional_chains/0/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

### Chat 请求与 WorkItem / WorkRun · `wwc-report-chat-delivery-workrun-requests`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`5286c33493869864db5cae8a`；Evidence=`4becc4c2c83ad6d40f0abb96`。
源码/关系 [/functional_chains/1](winwincode-automatic-report.json#/functional_chains/1)；缺段 [/functional_chains/1/analysis_gaps](winwincode-automatic-report.json#/functional_chains/1/analysis_gaps)；模型 [/functional_chains/1/trusted_models](winwincode-automatic-report.json#/functional_chains/1/trusted_models)；policy [/functional_chains/1/policy_declarations](winwincode-automatic-report.json#/functional_chains/1/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

### Device provider 部署分流 · `wwc-report-device-provider-deployment`

`deployment_provider_split`；state=`partial_source_relations`；scoped_source_supported=`false`；captured_source_structure_supported=`true`。
保存缺口：`report_source_role_graph_binding_limited`, `report_source_role_graph_binding_limited`, `deployment_candidate_chain_not_global_dispatch_or_credential_availability`；Finding=`6326ace38185675d203f5809`；Evidence=`09b8a912de95ed026ccc5725`。
源码/关系 [/functional_chains/2](winwincode-automatic-report.json#/functional_chains/2)；缺段 [/functional_chains/2/analysis_gaps](winwincode-automatic-report.json#/functional_chains/2/analysis_gaps)；模型 [/functional_chains/2/trusted_models](winwincode-automatic-report.json#/functional_chains/2/trusted_models)；policy [/functional_chains/2/policy_declarations](winwincode-automatic-report.json#/functional_chains/2/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

### Kernel create_session 接口 · `wwc-report-kernel-create-session-interface`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`2476c0ba1c86c52e734c626b`；Evidence=`a8e64f975a826512eb66659e`。
源码/关系 [/functional_chains/3](winwincode-automatic-report.json#/functional_chains/3)；缺段 [/functional_chains/3/analysis_gaps](winwincode-automatic-report.json#/functional_chains/3/analysis_gaps)；模型 [/functional_chains/3/trusted_models](winwincode-automatic-report.json#/functional_chains/3/trusted_models)；policy [/functional_chains/3/policy_declarations](winwincode-automatic-report.json#/functional_chains/3/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

### Kernel reconcile_turn_exact 接口 · `wwc-report-kernel-reconcile-exact-interface`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`eb4241aadc167972eb15203c`；Evidence=`e5f427d3e22c0abe60aab073`。
源码/关系 [/functional_chains/4](winwincode-automatic-report.json#/functional_chains/4)；缺段 [/functional_chains/4/analysis_gaps](winwincode-automatic-report.json#/functional_chains/4/analysis_gaps)；模型 [/functional_chains/4/trusted_models](winwincode-automatic-report.json#/functional_chains/4/trusted_models)；policy [/functional_chains/4/policy_declarations](winwincode-automatic-report.json#/functional_chains/4/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

### Kernel submit_turn 接口 · `wwc-report-kernel-submit-turn-interface`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`c4c6a41c714f4ac6670821b9`；Evidence=`1743f4e539c0d17068c2785a`。
源码/关系 [/functional_chains/5](winwincode-automatic-report.json#/functional_chains/5)；缺段 [/functional_chains/5/analysis_gaps](winwincode-automatic-report.json#/functional_chains/5/analysis_gaps)；模型 [/functional_chains/5/trusted_models](winwincode-automatic-report.json#/functional_chains/5/trusted_models)；policy [/functional_chains/5/policy_declarations](winwincode-automatic-report.json#/functional_chains/5/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

### ProductionAdapter → Kernel 构造 · `wwc-report-production-adapter-embedded-kernel`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`bd05f66a1f61c19a19ca9800`；Evidence=`ff7fe3d0f3133e2b4c683fb5`。
源码/关系 [/functional_chains/6](winwincode-automatic-report.json#/functional_chains/6)；缺段 [/functional_chains/6/analysis_gaps](winwincode-automatic-report.json#/functional_chains/6/analysis_gaps)；模型 [/functional_chains/6/trusted_models](winwincode-automatic-report.json#/functional_chains/6/trusted_models)；policy [/functional_chains/6/policy_declarations](winwincode-automatic-report.json#/functional_chains/6/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

### intent → persist → exact reconcile · `wwc-report-submission-intent-kernel-order`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`a6f2eb12778d309024deb758`；Evidence=`792d494a7d4547952c04d4ab`。
源码/关系 [/functional_chains/7](winwincode-automatic-report.json#/functional_chains/7)；缺段 [/functional_chains/7/analysis_gaps](winwincode-automatic-report.json#/functional_chains/7/analysis_gaps)；模型 [/functional_chains/7/trusted_models](winwincode-automatic-report.json#/functional_chains/7/trusted_models)；policy [/functional_chains/7/policy_declarations](winwincode-automatic-report.json#/functional_chains/7/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

### Worker 入口分支 · `wwc-report-worker-bootstrap-entries`

`guarded_call_sequence`；state=`partial_source_relations`；scoped_source_supported=`false`；captured_source_structure_supported=`true`。
保存缺口：`report_source_role_graph_binding_limited`, `report_source_role_graph_binding_limited`, `report_source_role_graph_binding_limited`；Finding=`d234bfcfd8c964ba2d0ec7bd`；Evidence=`32cfa45a045584054f5b9a10`。
源码/关系 [/functional_chains/8](winwincode-automatic-report.json#/functional_chains/8)；缺段 [/functional_chains/8/analysis_gaps](winwincode-automatic-report.json#/functional_chains/8/analysis_gaps)；模型 [/functional_chains/8/trusted_models](winwincode-automatic-report.json#/functional_chains/8/trusted_models)；policy [/functional_chains/8/policy_declarations](winwincode-automatic-report.json#/functional_chains/8/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

### 生产 Worker 构造 · `wwc-report-worker-production-construction`

`guarded_call_sequence`；state=`partial_source_relations`；scoped_source_supported=`false`；captured_source_structure_supported=`true`。
保存缺口：`report_source_role_graph_binding_limited`, `report_source_role_graph_binding_limited`；Finding=`f566fd359f7b0d297f9b6d40`；Evidence=`a143612edb49ee3dbb90ff42`。
源码/关系 [/functional_chains/9](winwincode-automatic-report.json#/functional_chains/9)；缺段 [/functional_chains/9/analysis_gaps](winwincode-automatic-report.json#/functional_chains/9/analysis_gaps)；模型 [/functional_chains/9/trusted_models](winwincode-automatic-report.json#/functional_chains/9/trusted_models)；policy [/functional_chains/9/policy_declarations](winwincode-automatic-report.json#/functional_chains/9/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

### Worker typed dispatch · `wwc-report-worker-typed-dispatch`

`guarded_call_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`[]`；Finding=`0a29aee5f115a4f749fffe8a`；Evidence=`5666ac49d3b01d2f3f7d103f`。
源码/关系 [/functional_chains/10](winwincode-automatic-report.json#/functional_chains/10)；缺段 [/functional_chains/10/analysis_gaps](winwincode-automatic-report.json#/functional_chains/10/analysis_gaps)；模型 [/functional_chains/10/trusted_models](winwincode-automatic-report.json#/functional_chains/10/trusted_models)；policy [/functional_chains/10/policy_declarations](winwincode-automatic-report.json#/functional_chains/10/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

### WorkRun 校验与重复 guard · `wwc-report-workrun-state-guards`

`state_guard_sequence`；state=`scoped_source_relations_supported`；scoped_source_supported=`true`；captured_source_structure_supported=`true`。
保存缺口：`iterator_selection_and_macro_runtime_semantics_not_fully_proven`；Finding=`cf8f7d136865ae065a81d04f`；Evidence=`fba2a1501b574cd345f61de9`。
源码/关系 [/functional_chains/11](winwincode-automatic-report.json#/functional_chains/11)；缺段 [/functional_chains/11/analysis_gaps](winwincode-automatic-report.json#/functional_chains/11/analysis_gaps)；模型 [/functional_chains/11/trusted_models](winwincode-automatic-report.json#/functional_chains/11/trusted_models)；policy [/functional_chains/11/policy_declarations](winwincode-automatic-report.json#/functional_chains/11/policy_declarations)；evidence 指针=`/evidence/0/details`（相对于该 Finding）。

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
| `cold` | `partial` | `true` | `ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28` |
| `warm` | `partial` | `false` | `ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28` |

这张表复制保存发布记录；partial 是图/解析范围状态，不能据此覆盖上方判断结论。完整记录见 [integration](winwincode-integration.json)。
