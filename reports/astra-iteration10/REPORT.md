# CallScope v0.12.0：原报告范围内的自动静态判断

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

正式报告有 18 个所选主要链条目；源码关系状态为 `{"partial_source_relations":3,"scoped_source_relations_supported":15}`。其中 `captured_source_structure_supported=true` 为 18 项，`scoped_source_supported=true` 为 15 项。结构抽取与包含实际装配/guard 的源码支持是不同字段；partial 条目保留具体缺段。

这些条目描述所选声明和正常分支的静态关系，均不自动证明完整运行功能。相同源 selector 的重叠在自动报告单列，不累计为额外能力；目录、依赖图、解析文件及 AST anchor 数量也不构成功能覆盖率。

`scoped_source_relations_supported` 也不表示全部 `analysis_gaps` 为空；以下既含 partial，也含已支持条目保留的 source-only 边界。表中只复制 gap code、角色和文件位置，完整记录保存在自动报告与输入清单。

| 保留边界的链 | 保存状态 | 保存分析缺段导航 |
| --- | --- | --- |
| cpb-report-trusted-probe-command-source | scoped_source_relations_supported | [{"code":"structured_command_intermediate_values_and_external_effects_not_fully_proven","source_only":true}] |
| cpb-report-unsupported-probe-evidence | scoped_source_relations_supported | [{"code":"structured_record_markers_do_not_prove_all_input_retention_or_persistence","source_only":true}] |
| wwc-report-device-provider-deployment | partial_source_relations | [{"code":"report_source_role_graph_binding_limited","location":{"file":"crates/winwincode-server/src/main.rs","line":340},"role":"boundary","source_body_available":true,"source_gap_codes":["graph_declaration_not_unique"]},{"code":"report_source_role_graph_binding_limited","location":{"file":"crates/winwincode-worker/src/main.rs","line":154},"role":"bootstrap","source_body_available":true,"source_gap_codes":["graph_declaration_not_unique"]},{"code":"deployment_candidate_chain_not_global_dispatch_or_credential_availability","source_only":true}] |
| wwc-report-worker-bootstrap-entries | partial_source_relations | [{"code":"report_source_role_graph_binding_limited","location":{"file":"crates/winwincode-worker/src/main.rs","line":34},"role":"entry","source_body_available":true,"source_gap_codes":["graph_declaration_not_unique"]},{"code":"report_source_role_graph_binding_limited","location":{"file":"crates/winwincode-worker/src/main.rs","line":97},"role":"remote","source_body_available":true,"source_gap_codes":["graph_declaration_not_unique"]},{"code":"report_source_role_graph_binding_limited","location":{"file":"crates/winwincode-worker/src/main.rs","line":118},"role":"managed","source_body_available":true,"source_gap_codes":["graph_declaration_not_unique"]}] |
| wwc-report-worker-production-construction | partial_source_relations | [{"code":"report_source_role_graph_binding_limited","location":{"file":"crates/winwincode-worker/src/main.rs","line":154},"role":"shared_loop","source_body_available":true,"source_gap_codes":["graph_declaration_not_unique"]},{"code":"report_source_role_graph_binding_limited","location":{"file":"crates/winwincode-worker/src/main.rs","line":315},"role":"adapter_factory","source_body_available":true,"source_gap_codes":["graph_declaration_not_unique"]}] |
| wwc-report-workrun-state-guards | scoped_source_relations_supported | [{"code":"iterator_selection_and_macro_runtime_semantics_not_fully_proven","source_only":true}] |

[全文范围对照](REPORT_ALIGNMENT_RESULTS.json) 保留原目录的 32 个章节、130 个段落/表格行/列表项。该数量是证据导航清单，未给每段文字、建议或业务职责重新评级。`whole_report_reproduction_claimed=false`；更广职责、安全、部署和原未审范围仍不能由五项判断或所选链替代。

## 正式来源与捕获范围

| 仓库 | 正式快照 | 状态 | 选入 / 解析 | 图节点 / 边 | 冷 / 暖创建 |
| --- | --- | --- | --- | --- | --- |
| codepatchbay | `7524afef4f9234ebef40eec1d74dbb91a3f56dc76f0191728c42d3bdd3cfb167` | partial | 333 / 330 | 11085 / 60571 | True / False |
| winwincode | `ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28` | partial | 471 / 465 | 32407 / 171983 | True / False |

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

- **codepatchbay**：policy 字节相同=`false`；变化 section=`["analysis","goal_contracts","report_claims"]`；捕获 source hash 与 v11 相同=`false`。inert 支持输入 2 项；原引用源文件 hash 与 target commit 由 publication identity 单独核对。
- **winwincode**：policy 字节相同=`false`；变化 section=`["analysis","goal_contracts","report_claims"]`；捕获 source hash 与 v11 相同=`false`。inert 支持输入 11 项；原引用源文件 hash 与 target commit 由 publication identity 单独核对。

输入捕获范围改变不等于目标代码发生修改。受信模型和环境条件不填补尚未建立的源连接；旧 field/IR 的 unknown 不因新局部 record 关系被升级。无运行、浏览器、网络、并发或业务验收证明。

## 原 26 条观察与交付身份

原冻结观察保留 26 条，总计比较 26 条，状态为 `{"ambiguous":0,"endpoint_missing":0,"evidence_only":13,"evidence_unavailable":0,"mismatch":0,"reproduced":10,"source_changed":0,"source_missing":0,"unknown":3}`；相对 v11 的保存变化记录为 0 项。evidence_only 和指定 unknown 仍遵循原 evaluator；观察重现数量不是完整功能判断数量。

包版本 `0.12.0`，analyzer `static-multilang-12`，detector `call-rules-11-whole-judgments`，schema `2`。冻结 tool source hash：`664f0723371e930791f7a69669cdf33e2bde4d85f9342cfd21ac3fcb9c97a44f`。

[CORE_FREEZE.json](CORE_FREEZE.json) 的 54 份核心 Python 源码 live/archive hash 一致，AST 可解析；此项只是身份/语法核对。正式身份产物记录原引用的 36 份文件 saved/live hash 一致，两库 target commit 一致；没有宣称工作区 clean。两库和共有组件的正式 publication identity 已验证；本报告没有再次执行检测器或读取数据库。

- [CodePatchBay 自动报告](codepatchbay-automatic-report.md)与[扫描记录](codepatchbay-integration.json)。
- [WinWinCode 自动报告](winwincode-automatic-report.md)与[扫描记录](winwincode-integration.json)。
- [CodePatchBay 简明分析](codepatchbay-analysis-summary.md)、[WinWinCode 简明分析](winwincode-analysis-summary.md)。
- [原五项结果账本](goal-ledger.json)、[原 26 条比较](ORIGINAL_BASELINE_COMPARISON.json)、[正式身份](PUBLICATION_IDENTITY.json)。
- [全文范围对照](REPORT_ALIGNMENT_RESULTS.json)、[本报告输入与核对记录](RELEASE_REPORT_INPUTS.json)。

[正常 report CLI 读回记录](CLI_REPORT_READBACK.json) 已确认保存的 CodePatchBay Markdown 字节一致；该查询没有重算检测器。本生成器只复制并核对记录，没有重跑 CLI。

[原全文与当前自动报告的具体差距](REPORT_SCOPE_GAPS.md) 分列原已读但尚无同等自动结论的段落、源码边界与原明确未审范围；其导航不增加新评分或审批。
