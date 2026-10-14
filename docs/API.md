# CLI 与 HTTP API

所有操作围绕纯静态分析快照。当前正式版本 v0.14：schema 2、分析器 `static-multilang-14`、检测器 `call-rules-13-architecture-explanations`。两库正常冷/暖重算及报告已保存于 [scope2](../reports/astra-iteration12-scope2/CORE_FREEZE.json)；下方旧版结果保留其原身份。扫描只读目标源码，不执行目标、测试或构建。

新增项目报告入口从保存证据生成架构结构、完整条件判断、主要功能链、反证和未审范围。基准是原两份分析报告，没有重复 Astra 审批步骤；见 [自动项目分析报告](AUTOMATED_REPORTS.md)。

v0.14 的正常报告增加 `architecture.responsibility_explanations`、`documentation_comparisons` 与 `report_components`，调用方式不变。职责正文及源操作有共享位置/证据索引，不按目录名或方法名分配所有权；普通调用与消息边界分开。当前生成器身份与原快照分析身份分别保存，旧快照不会因重新生成报告而升级发现。

`capabilities.source_relations` 增加 `conditional_state_lineage`、`conditional_publication_boundary`；`document_comparisons=[document_deployment_consistency]`、`architecture_explanations=authenticated_captured_operations_and_handoffs` 表示已安装能力，并不表示当前仓库已经支持或配置。报告规则协议 `static-report-claim-policy-v2-documents` 兼容原规则；仅文档比较规则必须额外声明数据定位 `documents: [{role, file}]`，其余规则仍拒绝该字段。辅助文档须已捕获并按字节/text hash 与坐标认证，文档不产生伪造 AST 或 CALLS。

## v0.14 正式保存结果

| 仓库 | 正常自动报告 | 扫描身份与重复发布记录 | 所选源码关系 |
| --- | --- | --- | --- |
| CodePatchBay | [Markdown](../reports/astra-iteration12-scope2/codepatchbay-automatic-report.md) / [JSON](../reports/astra-iteration12-scope2/codepatchbay-automatic-report.json) | [integration](../reports/astra-iteration12-scope2/codepatchbay-integration.json)，快照 `dd5d4e3c…0e50ebb` | 16 条限定支持 |
| WinWinCode | [Markdown](../reports/astra-iteration12-scope2/winwincode-automatic-report.md) / [JSON](../reports/astra-iteration12-scope2/winwincode-automatic-report.json) | [integration](../reports/astra-iteration12-scope2/winwincode-integration.json)，快照 `cc327a39…463d372` | 20 条限定支持 |

五项原判断均 complete/full 支持，30 项必要关系 supported；共享位置、证据与操作引用检查均无失效引用。原报告有限内容的实际正文、模型条件、文档三方面与未审边界见[正式内容对照](../reports/astra-iteration12-scope2/ORIGINAL_REPORT_COMPLETION.md)。这些状态、关系数和解析比例均不是项目功能通过率。

两库图快照仍为 `partial`，解析为 330/333、465/471；同库两次 full 重算得到同一快照，第二次 `created=false`。原26观察及源码引用身份见[原观察比较](../reports/astra-iteration12-scope2/ORIGINAL_BASELINE_COMPARISON.json)与[发布身份](../reports/astra-iteration12-scope2/PUBLICATION_IDENTITY.json)。报告读取已保存内容，不通过重新生成升级旧快照的发现。

## v0.13 历史正式保存结果

| 仓库 | 正式自动报告 | 扫描身份与重复发布记录 | 所选源码链 |
| --- | --- | --- | --- |
| CodePatchBay | [Markdown](../reports/astra-iteration11/codepatchbay-automatic-report.md) / [JSON](../reports/astra-iteration11/codepatchbay-automatic-report.json) | [integration](../reports/astra-iteration11/codepatchbay-integration.json)，快照 `7b58e733…54c2bfe` | 13 条 |
| WinWinCode | [Markdown](../reports/astra-iteration11/winwincode-automatic-report.md) / [JSON](../reports/astra-iteration11/winwincode-automatic-report.json) | [integration](../reports/astra-iteration11/winwincode-integration.json)，快照 `cb8df704…74f4da2` | 18 条 |

31 条的保存状态均为 `scoped_source_relations_supported`；它们包含原链与本轮有限关系，不是31个功能通过或全文覆盖率。WWC 原三条生产入口/装配相关 partial 的 crate 属性绑定误判已修正，generic receiver、source-only 模型和外部效果边界仍保留。[正式判断账本](../reports/astra-iteration11/goal-ledger.json)保存五项 `scoped_static_judgment_reproduced`，`complete_assessment`、`full_goal_supported` 均 true、必要缺口为空；30项必要关系全部 supported、未闭关系为空。[判断证据](../reports/astra-iteration11/GOAL_JUDGMENT_EVIDENCE.json)保存704项真实引用。五/30是实现追踪，不是原全文验收分母。

两库冷/热轮分别保持同一快照 ID，`created=true/false`；本轮使用 `full` 引擎，两轮均重算静态前端并全量检测，未声称缓存复用。完整解析分别330/333与465/471，快照仍为 `partial`；源码 hash 与 v0.12 相同，策略、工具及引擎身份已变化，不能当成同引擎精度或性能对照。

[原26项比较](../reports/astra-iteration11/ORIGINAL_BASELINE_COMPARISON.json)保存10 reproduced/3 unknown/13 evidence_only，两库 `changes=[]`；36份原引用的保存/现场 hash 均匹配，commit 与冻结版本一致。[发布身份](../reports/astra-iteration11/PUBLICATION_IDENTITY.json)的 `verified=true`，共享组件一致，60份核心当前/存档 hash 一致。这是身份和原观察关系核对，不是全部功能无回退的证明，也不是模型批准步骤。

[正常 CLI 报告导出记录](../reports/astra-iteration11/CLI_REPORT_READBACK.json)确认 WWC 的 `report` 导出与正式 Markdown 字节/hash 一致，保存数据的逻辑内容、schema 与身份保持；未重扫目标。易读入口见 [CPB摘要](../reports/astra-iteration11/codepatchbay-analysis-summary.md)、[WWC摘要](../reports/astra-iteration11/winwincode-analysis-summary.md)及 [本轮发布说明](../reports/astra-iteration11/REPORT.md)；[范围差距](../reports/astra-iteration11/REPORT_SCOPE_GAPS.md)与 [原报告条目导航](../reports/astra-iteration11/REPORT_ALIGNMENT_RESULTS.json)继续区分实际承接范围和未审边界。

## v0.13 源码关系接口

v0.13 继续使用 `report_claims` 的原数据协议，没有新增可执行配置、目标验证端点或动态插件入口。原八类源码链保留，新增以下八种 `report_claims.type`；类型数量不表示发现数量或功能覆盖率。

| `report_claims.type` | 实际关系范围 | 额外必需模型 |
| --- | --- | --- |
| `rust_finite_state_selection` | 有限 iterator、enum/`matches!`、runnable/依赖和活动尝试选择条件 | `rust-finite-iterator-enum-source-v1` |
| `conditional_gate_relations` | 返回记录、前置拒绝、readiness/completion 条件及独立 access-audit 拒绝来源 | `finite-js-plain-record-gate-conditions-v1` |
| `event_index_projection` | 所选事件记录、codec、提交调用与索引投影/replay 来源 | `finite-record-codec-projection-source-v1` |
| `trusted_command_lineage` | 所选可信命令、参数中间绑定、固定记录与消费者来源 | `finite-record-codec-projection-source-v1` |
| `unsupported_record_retention` | 所选 unsupported 输入、失败记录、集合修改和后续消费者 | `finite-record-codec-projection-source-v1` |
| `message_identity_relations` | 词法声明、记录字段/复制、typed arm、请求/提交身份及 correlation 字段域 | `finite-captured-record-message-identities-v1` |
| `browser_async_lifecycle` | generation/abort/closed 来源、暂停后的局部 guard、结果处置及上下文消费者 | `browser-continuation-guard-source-v1` |
| `resource_writer_ownership` | 所选资源的捕获写者、同 token 引用、拒绝 guard 与 opaque frontier | `captured-resource-writer-source-v1` |

每条仍须注册 `captured-normal-statement-control-v1`，且只能携带该类型允许的模型。`message_identity_relations` 可额外注册 `captured-literal-sql-positional-bindings-v1`，用于字面 SQL 与 `params!` 捕获参数位置的有限关系，不执行 SQL。选择器只指定声明；不能配置预期字段流、分支真值或成功结论。

`GET /api/v1/status` 的 `capabilities.source_relations` 列出这八种已安装能力。它是能力目录，不表明当前项目已配置或满足它们。配置条数仍由 `report_claims_count` 表示；没有新增顶层合同数组。`stats.component_versions.report_claims` 保存报告链分析器 `captured-report-source-chains-2-relations`、原策略协议 `static-report-claim-policy-v1` 与 `relation_modules` 的实际版本。

发现继续通过 `/api/v1/anomalies` 与详情接口读取，`Finding.type=static_report_claim`、`Evidence.kind=static_report_chain_analysis`、包装状态 `uncertain`。实际结果查看 `pattern`、`assessment`、`source_facts`、`source_scope`、`trusted_models` 与 `analysis_gaps`。有限源码关系支持不证明回调/Future 已激活、跨消息值相等、事务提交成功、唯一事实所有权或全部功能可通过。必要缺口与明确留在模型外的边界需分别阅读，不能把源码片段存在当成身份或条件已经闭合。

Rust 前端升为 `rust-tree-sitter-1.8-crate-attribute-context`。已配置 crate 根上的完整内属性 `#![recursion_limit = "十进制值"]` 与 `type_length_limit` 使用有限 `rust-builtin-crate-limit-attribute-v1` 来源模型，保留原文/hash/span；它们属于编译限制，不再被当成改写所有声明的属性宏。其它属性、`cfg`、宏展开、trait/generic 和未知 crate 上下文的保守边界保留。此修正没有执行 Cargo 或证明编译成功。

## v0.12 正式保存结果

从 [CodePatchBay摘要](../reports/astra-iteration10/codepatchbay-analysis-summary.md)和 [WinWinCode摘要](../reports/astra-iteration10/winwincode-analysis-summary.md)可下钻完整自动报告和JSON证据。五个static_goal_judgment均complete_assessment=true/full_goal_supported=true，三十必要义务均supported；包装Finding.status仍uncertain，运行验证仍false。CPB为3判断/18义务/6源码链，WWC为2判断/12义务/12源码链。

源码链的真实state为CPB6项scoped_source_relations_supported、WWC9项同状态与3项partial_source_relations；后者是provider部署、Worker入口和生产构造。18项captured_source_structure_supported均true，已支持链仍可带显式模型/外部边界gaps。全部状态及条件按保存指针读取，不能用链数量替代完整判断或全文报告覆盖率。两库完整解析分别330/333、465/471，快照均partial；辅助输入分别2与11。

完整自动报告见 [CPB](../reports/astra-iteration10/codepatchbay-automatic-report.md)和 [WWC](../reports/astra-iteration10/winwincode-automatic-report.md)。原26项冻结观察保持10 reproduced/3 unknown/13 evidence_only，与v0.11 changes=[]，36份保存/现场原文身份matched；[发布身份](../reports/astra-iteration10/PUBLICATION_IDENTITY.json)verified=true，54份核心与存档一致。原观察、五项/30义务及全文范围分列，不合计成覆盖率。

v0.12 发布说明见 [v0.12正式报告](../reports/astra-iteration10/REPORT.md)。该版正式实现追踪见 [五判断/30义务账本](../reports/astra-iteration10/goal-ledger.json)及 [保存判断证据](../reports/astra-iteration10/GOAL_JUDGMENT_EVIDENCE.json)；[全文条目导航](../reports/astra-iteration10/REPORT_ALIGNMENT_RESULTS.json)仅关联原条目和证据，不生成全文评分。该版原主链尚未闭合的内容及原明确未审范围见 [范围差距](../reports/astra-iteration10/REPORT_SCOPE_GAPS.md)。

## v0.12 配置与证据协议

新增顶层数组 `goal_contracts` 和 `report_claims`，各最多 256 条。它们是严格校验的数据合同，不能指定 Python 模块、可执行插件或目标执行入口。规则 ID 跨所有约束数组唯一；`goal_id` 在完整判断数组内唯一。

`goal_contracts` 的外层字段如下，内部 `contract` 按固定适配器分别校验，内部 ID 必须与外层一致：

```json
{
  "id": "unique-rule-id",
  "goal_id": "unique-goal-id",
  "analyzer": "status",
  "contract": { "id": "unique-rule-id" }
}
```

上例只展示外层形状，缺少内部必需字段，不能直接用作扫描配置。`analyzer` 白名单为 `status`、`pipeline`、`navigation`、`device`、`atomicity`。完整配置应声明源选择器、有限模型、适用条件及判断范围；不得预填中间关系、guard、流程步骤或结论。v0.12 的实际规则随该版正式 policy 保存，新版规则使用各自保存的 policy 身份。

完整判断的 Finding.type 为 `static_goal_judgment`，Evidence.kind 为 `static_whole_judgment`，Finding.status 保持 `uncertain`。完整性另读 `assessment`、`complete_assessment`、`full_goal_supported`、必要义务与缺口。只有全部必需 ID 被真实适配器证据逐项支持或反证、来源/策略/合同身份一致、模型适用性闭合、必要缺口为空且预算完整时，注册层才接受完整评估。全部支持时为 `scoped_static_judgment_reproduced`；完整反证或范围收窄为 `claim_refuted_or_narrowed`；缺段保持 partial/unknown。配置布尔值、义务数量和来源锚点不能代替这些条件，`runtime_value_verified` 仍为 false。

`report_claims` 的字段为 `id`、`type`、`severity`、`sources`、`models`、`provenance`、`applicability`。`sources` 含 1 到 32 个 `{role,file,symbol}`，role 唯一，只负责定位；实际 callee、参数、guard 和顺序从 AST 与保存 CALLS 生成。`applicability` 必须声明条件；`provenance.source_doc` 仅为来源标签，检测器不读取原报告文字作为证据。

| `report_claims.type` | 所选源码关系 |
| --- | --- |
| `guarded_call_sequence` | 真实调用、正常语句顺序与前置阻断分支 |
| `best_effort_finalization` | 异常处理、最终化和失败容忍分支 |
| `structured_command_source` | 命令/参数来源及结构化执行接口模型 |
| `unsupported_method_evidence` | 不支持方法的集合、guard 与失败分支 |
| `state_guard_sequence` | 状态校验、写入及重复保护关系 |
| `deployment_provider_split` | 捕获的生产构造、provider 选择及未支持分支 |
| `conditional_delivery_result` | finalizer、结果写入/readback、reconcile 与投影条件 |
| `agent_execution_policy` | allowlist、child env 过滤及 sandbox 分支策略 |

Finding.type 为 `static_report_claim`，Evidence.kind 为 `static_report_chain_analysis`，status 为 `uncertain`。实际源码事实、`trusted_models`、`policy_declarations` 与 `analysis_gaps` 分开；`scoped_source_relations_supported` 只说明所选源码关系在声明模型中支持。嵌套 async/callback 源码区可提供内部调用和顺序事实，不证明 Future、回调或外部 provider 已实际激活。生产同类方法候选可以保留源码接缝，不能把 `actual_callee=null` 改成运行目标已解析。

服务状态包含 `capabilities.goal_contracts` 五适配器目录、`report_claims=captured_source_chains`，并保留一般 `interleaving_inference=false`；新 `finite_source_interleavings=registered_two_request_one_scheduler_model` 仅表示有限来源交错模型。`stats.goal_contracts_count` 和 `report_claims_count` 只计配置；`stats.component_versions` 保存注册器、各适配器、报告链及策略版本。`constraints_count` 为九个数组之和：`rules`、`static_contracts`、`value_contracts`、`navigation_contracts`、`atomicity_contracts`、`field_contracts`、`budget_contracts`、`goal_contracts`、`report_claims`。

完整判断与报告链沿用 `/anomalies`、`/anomalies/{id}` 与保存源码接口；没有单独的 goal 执行或目标验证接口。五判断/三十必要义务是实现追踪，不能充当全文报告分母。

## 自动项目报告

CLI `report` 默认生成 Markdown，也可用 `--format json`；未指定 `--snapshot` 时读取最新保存快照。HTTP 完整路径为 `GET /api/v1/report?snapshot_id=...`，MCP 为 `get_project_report`。三者使用保存快照和发现生成同一报告，不读取当前工作区补充历史证据，不调用 LLM。

| JSON 字段 | 内容与边界 |
| --- | --- |
| `version` / `snapshot` | 报告版本及快照、源码/策略哈希、状态和组件身份 |
| `coverage` | 选入/解析文件、未解析原因及辅助原文身份；不是功能覆盖率 |
| `architecture` / `project_declarations` | 目录结构、确定跨目录依赖样本及捕获的 manifest 声明；不推断运行频率或职责正确性 |
| `judgments` | 固定完整判断、条件、反证、必要义务、缺口及保存证据指针 |
| `functional_chains` | 主要源码链、实际源事实、可信模型、policy 与范围缺口 |
| `source_relation_index` | v2 报告的展示索引；引用每条链的状态、pattern、原事实与缺口，不新增分析结论 |
| `overlapping_source_selections` | 多条规则重叠选择的源码；不合计成新增功能 |
| `configured_local_assessments` / `graph_observation_counts` | 局部合同与图观察，和完整判断分列 |
| `report_scope` / `diagnostics` | 未建模范围与解析/分析诊断；`whole_report_reproduction_claimed=false` |

顶层 `target_executed`、`target_tests_run`、`target_build_run`、`runtime_functionality_verified` 均为 false。各模型的真实适用范围记录在判断条件、`trusted_models` 与分析范围中；源码链支持、模型内完整判断和全部项目功能通过是不同结论。

当前报告版本为 `captured-project-analysis-report-2`，CLI/HTTP/MCP 的报告入口和参数保持不变。`source_relation_index.entries` 保存 `rule_id`、`claim_type`、`finding_id`、`evidence_id`、`saved_evidence_pointer`，以及指向完整链的 `assessment_ref`、`pattern_ref`、`source_facts_ref`、`source_scope_ref`、`analysis_gaps_ref`。引用均为该报告的 JSON Pointer；完整证据仍在原 `functional_chains` 中。

每个索引条目的 `presentation` 使用 `captured-relation-presentation-1`，含 `sections`、`tables`、`limits`、`truncated` 与 `full_pattern_ref`。表格保留行数、实际值及 `full_table_ref`/`full_row_ref`；压缩省略通过 `full_value_ref` 返回原记录。`presentation_only=true` 表示展示投影，不重新评级；显示截断不修改原证据，也不能当成分析完整或失败。`architecture.captured_writer_references` 只引用保存的 writer groups、assessment 和证据位置，不按目录名生成职责或认定唯一授权写者。

报告生成器版本与快照分析版本分开：用当前生成器读取旧快照，只能重新呈现旧快照已保存的证据，不能为旧结果补记新关系。原两份完整报告是范围基准，五判断/30 必要义务只作实现账本，报告索引、源码事实数和表格行数均不充当全文覆盖率。

## CLI

从仓库根目录使用 `python -m callscope`。默认数据库为当前工作目录下 `.callscope/callscope.sqlite3`，多个命令应使用相同 `--db` 路径。

| 命令 | 主要参数 |
|---|---|
| `scan ROOT` | `--config PATH`、`--db PATH`、`--engine auto\|full\|cocoindex`、`--json`、`--output PATH` |
| `serve ROOT` | `--config PATH`、`--db PATH`、`--engine auto\|full\|cocoindex`、`--host 127.0.0.1`、`--port 8787`、`--watch`、`--interval 2` |
| `path FROM TO` | `--snapshot ID`、`--db PATH` |
| `diff OLD NEW` | `--db PATH`；两个参数是已经保存的快照 ID |
| `versions` | `--db PATH`、`--project-id ID` |
| `anomalies` | `--snapshot ID`、`--db PATH`、`--severity LEVEL`、`--type TYPE`、`--json` |
| `report` | `--snapshot ID`、`--db PATH`、`--format json\|markdown`、`--output PATH` |
| `baseline BASELINE_FILE` | `--snapshot ID`、`--repo-id ID`、`--compare-snapshot OLD`、`--compare-db OLD_DB`、`--db PATH`、`--output JSON`；输出 JSON |
| `decide FINDING_ID` | `--snapshot ID`、`--action ACTION`、`--reason TEXT`、`--expires-at ISO8601`、`--db PATH` |
| `mcp ROOT` | `--config PATH`、`--db PATH`、`--engine auto\|full\|cocoindex`；stdio 服务 |

`scan` 持久化快照及发现；`--json` 输出 `{snapshot, findings, publication}`，`--output` 将完整报告写到指定文件。快照包含 `analyzer_version`、`detector_version`、`schema_version` 和 `parser_version`；后者保存工具源码、图/维护后端及实际语言解析组件身份的规范组合，同样参与身份计算。`stats.component_versions` 为结构化明细。维护运行计数位于 `publication.maintenance`，不进入不可变 `stats`。`path`、`anomalies` 未指定快照时使用数据库最新快照。切换数据库或项目后，应显式指定快照，避免把其他项目的结果当作当前项目。

引擎参数默认 `auto`：工具目录或当前 Python 安装中存在固定 CocoIndex 依赖时选用它，否则使用 `full`。`full` 每轮重算前端；`cocoindex` 使用 CocoIndex `1.0.25` 持久复用语言整体结果，依赖缺失时失败。选定 CocoIndex 后的运行失败不静默切换为 `full`。所有引擎使用 Axon 确定调用图索引，检测始终全量。缓存粒度及输入身份见 [上游复用说明](UPSTREAM_REUSE.md)。

默认只请求 Python；项目配置 `analysis.languages` 可设为 `["python", "typescript", "rust"]`。TypeScript 项包含 JS/JSX/MJS/CJS/MTS/CTS 输入。`analysis.module_aliases` 提供 TS 包入口映射，`analysis.rust_crates` 提供 crate 根映射。CLI 不调用目标的编译器、包管理器或任务脚本。

`decide` 的行动为 `accept_risk`、`false_positive`、`fix_planned`，不是执行修复或验证。`serve` 先尝试一次静态扫描，初始失败时仍提供状态及配置界面；`--watch` 按 `interval` 周期全量捕获源码，再按所选引擎计算，相同分析输入去重。`interval` 至少为 0.5 秒，不是更新延迟或增量分析的性能保证。服务启动后工具源码变化要求重启再扫描。

CLI 不因结构发现返回失败码，不充当门禁；返回 0 表示工具命令完成，不表示目标功能通过。命令或操作错误返回 2，中断返回 130。数据库列表、发现和差异仍需结合完整性状态理解。

## 冻结源码观察核对

v0.4 的 `baseline` 从数据库读取快照，与数据文件中的原始观察核对，不扫描当前目标目录，也不导入或执行目标。默认使用最新快照，建议用 `--snapshot` 固定身份；未提供 `--repo-id` 时按保存的项目根匹配基准仓库。

```sh
python -m callscope baseline reports/astra-baseline/capability-baseline.json --db DB --snapshot SNAPSHOT_ID --repo-id codepatchbay --output comparison.json
```

替换 `DB`、`SNAPSHOT_ID` 为真实值。普通调用返回 `{current}`；提供 `--compare-snapshot OLD` 或 `--compare-db OLD_DB` 后返回 `{current, previous, changes, interpretation}`。`--compare-db` 读取独立数据库，省略 `--compare-snapshot` 时取其最新快照；未提供旧库则从 `--db` 读取指定旧快照。比较限同项目，`changes` 保存每项状态或 `expectation_satisfied` 的变化，包含前后满足值，不仅展示改善。`--output` 原子写入独立报告，不发布新快照，不改冻结观察或历史快照。

核对包含原文件哈希、原文引用及同一调用位置；`unknown_required` 与 `evidence_only` 保留为独立观察类别。原文变化、文件不在选入范围、端点未解析、关系不匹配与能力未支持需要分别阅读，不能把所有非确定项都排除后宣称覆盖完整。具体基准格式见 [BASELINE_CONTRACT.md](../reports/astra-baseline/BASELINE_CONTRACT.md)。HTTP 与 MCP 仍使用下述原接口，未新增基准入口。

`current` / `previous` 内的主要字段如下：

| 字段 | 含义 |
| --- | --- |
| `baseline_total`、`expected_counts` | 冻结基准全部观察及其预期类别计数；Astra v1 共 26 项 |
| `selected_total`、`selected_expected_counts` | 所选仓库全部观察及预期类别，不排除未知或仅证据；本基准每库 13 项 |
| `remaining_repository_observations` | 基准中其它仓库的观察数量；不在无关快照上判失败 |
| `counts`、`by_expected_outcome` | 所选观察全部状态及按预期类别细分 |
| `confirmed_reproduction_count` | 仅 `reproduced` 的有限静态关系数 |
| `intentional_unknown_preserved_count` | `unknown_required` 且同一调用位置确实保留未知的数量 |
| `expectation_satisfied_count` | 确定关系重现与正确保留未知的合计；不是功能通过数 |
| `source_checks`、`observations` | 原文件核对及每项定位、端点、见证、原因、条件与反证 |

结果另保存 `evaluator_version`、`evaluator_source_hash` 及实际加载实现的来源信息，与 `snapshot` 内分析组件身份分开。对同一个旧快照使用新的核对器应产生新独立报告，不能替旧快照补写当前工具版本。

每项 `status` 与 `expectation_satisfied` 分开阅读：

| 状态 | 语义 |
| --- | --- |
| `reproduced` | 确定关系按原调用位置或冻结逐边路径重现，`expectation_satisfied=true` |
| `unknown` | 源节点、解析或绑定不足；指定未知观察须在原调用点保留 dynamic/unresolved/ambiguous、无确定 target 且有明确 reason，才满足预期，仍不升级为确定边 |
| `ambiguous` | 端点或引用区间指向多个调用，不能任选一个满足观察 |
| `endpoint_missing` | 文件分析状态完整但所需端点未匹配；不是目标缺少功能的判断 |
| `mismatch` | 原位置的目标/关系与观察不一致，或完整解析后未捕获该调用；不是自动判目标缺陷 |
| `source_changed` | 保存的原文件哈希不同于冻结基准，优先阻止套用旧观察 |
| `source_missing` | 原文件未进入该快照；与源码变化区别呈现 |
| `evidence_unavailable` | 原字节哈希、源码文本或指定范围的 quote 无法核对 |
| `evidence_only` | 来源与 quote 已核对，但图模型不能裁决该观察，`expectation_satisfied=null` |

核对顺序为原文件变化 → 文件缺失 → 证据不可用 → 仅证据或关系判读。调用点匹配结合原 quote、行范围、UTF-8 字节列与 expression；正向边要求对应两端文件完整解析，无关文件的 gap 不否定已确认正向边。正向路径只使用这些已核对调用位置对应的边，不通过无关替代路径满足观察。否定直接调用须同时检查显式模型覆盖和未知，缺边不独立构成否定证明。每项保留 `reason_code`、`evaluation_reason`、`source_checks`、`locations`、`endpoint_status` 与 `witness`，不跳过源缺口项。`required_capabilities` / `missing_capabilities` 为观察需求与剩余缺口说明，满足一项观察不是逐项能力认证。

核对器 `frozen-static-baseline-1.3` 仅允许schema 2的input_evidence为evidence_only补原文/quote，状态可由source_missing变为evidence_only；不生成caller或跨语言确定调用。代码/support同路径身份冲突或辅助hash/text_hash无效为evidence_unavailable。witness.binding_models含helper/接口模型摘要及generic_impl_model、前提与snapshot/edge完整metadata指针；同impl词法模型不证明泛型实例化、bounds、实参类型、完整编译器命名空间、宏展开、生成体或目标工具链。

## HTTP

启动 `serve` 后，页面与 API 同源。所有业务接口以 `/api/v1` 开头。

| 方法 | 路径 | 用途 |
|---|---|---|
| GET | `/status` | 当前项目及分析服务状态 |
| GET | `/report?snapshot_id=...` | 从保存图和发现生成项目报告 JSON |
| GET | `/versions` | 快照列表 |
| GET | `/graph?snapshot_id=...` | 指定版本的节点、调用边、诊断和统计 |
| GET | `/anomalies?snapshot_id=...&severity=...&type=...&q=...` | 发现筛选 |
| GET | `/anomalies/{id}?snapshot_id=...` | 单项发现与静态证据 |
| GET | `/evidence/source?snapshot_id=...&file=...&line=...` | 保存于指定快照的源码 |
| GET | `/config` | 当前配置及路径 |
| GET | `/decisions` | 人工处置记录 |
| POST | `/scan` | 对服务启动时固定的项目目录重新分析 |
| POST | `/config` | 校验、保存配置，返回需要重新扫描的标记 |
| POST | `/graph/subgraph` | 获取局部图 |
| POST | `/query/path` | 查询确定调用路径 |
| POST | `/diff` | 两个已保存快照的结构差异 |
| POST | `/decisions` | 追加人工处置 |
| GET | `/audit` | 检查本地处置记录哈希链一致性；不是不可篡改证明 |

`/graph` 返回结构为 `{snapshot, nodes, edges, diagnostics, stats}`，不在图接口内联完整源码；`/anomalies` 为 `{snapshot_id, items}`；`/versions` 为 `{items}`；`/config` 为 `{config, config_path}`。

`GET /status` 新增 `capabilities.static_contracts=[literal_set_consistency,required_object_fields]` 和 `support_input_capture=true`。合同finding类型为 `static_contract_literal_set_consistency` / `static_contract_required_object_fields`，仍从anomalies接口读取。metadata包含contract_hash、provenance、applicability、source_fact_confirmed与runtime_proof=false；evidence.details包含source_fact、源hash/位置、guard及反证、unknown。conditional适用性始终uncertain，不能用source_fact_confirmed替代条件证明。

值合同能力为 `capabilities.value_contracts=[call_argument_value]`；`stats.value_contracts_count`只计值合同条数，`stats.component_versions.value_contracts`记录分析器/策略版本。finding类型为static_value_call_argument_value，Evidence.kind为static_value_analysis，使用原anomalies/source接口；不新增参数执行或运输验证API。constraints_count按上文九个配置数组总数计算。

值合同 metadata 包含 comparison、producer_comparison、source_fact_confirmed、source_form_difference_confirmed、contract_hash、provenance、applicability，以及 runtime_proof=false/transport_proof=false。evidence.details.source_fact 分别保存 subject/producer；每侧含调用总数、matches/mismatch/unknown 计数、源码表达式/词法绑定和 callee 快照边依据。每侧 calls 最多64项，优先展示mismatch、unknown、matches，另保留 calls_truncated/call_sample_limit；最多分析512个匹配调用，超出时保留unknown。样本截断不将未展示调用当作通过。comparison 描述来源形式，Finding.status 描述结论边界；conditional或未证明前提保持uncertain，形式差异不证明运行值错误，空 findings 不是全部合同通过证据。

capabilities保留navigation_contracts=[navigation_query_context]、atomicity_contracts=[protected_deduplication]、port_wiring=[boot,factory_branch,injection,returned_method_use]和interleaving_inference=false；field_contracts=[parameter_field_flow]，semantic_environment=captured_scope_conditional_model，completion_summaries=finite_normal_completion_relations。v0.9新增budget_contracts=[bounded_for_loop,counter_exhaustion_guard]、semantic_ir=finite_immutable_field_state。能力是目录，不认证端到端、字段运输或竞态。constraints_count另含v0.12的goal_contracts/report_claims，共九数组；各count仅计配置。stats.component_versions按启用记录模块版本；字段含field_summaries/semantic_ir/field_relations，预算含budget_contracts及共享来源组件。

新发现仍从anomalies接口读取：

| Finding.type / Evidence.kind | 主要保存证据与边界 |
| --- | --- |
| static_navigation_query_context / static_navigation_analysis | details含producer.query_domain、consumer、source_trace、standard_models、ambient_assumptions、analysis_gaps、port_wiring及snapshot/source/policy/contract身份；guaranteed/possible/keyset_closed分别阅读，source_fact_confirmed或source_condition_chain_confirmed不代表full_functionality_proven（固定false）。 |
| static_atomicity_protected_deduplication / static_atomicity_analysis | details.source_facts含facade/dependency_assembly/wrapper_forwarding/lifecycle/authority/predicates/transition/comparison；protocol_model、resource_mapping、counterevidence及unknown_count/samples/truncated分开。region支持不等于实际deps、集合heap、锁正确性或交错证明。 |
| static_parameter_field_flow / static_field_analysis | details保存所有site评估、IR对象/版本/复制/effect关系、源事实、body return/abrupt/gaps及model/contract/snapshot身份；uncertain摘要不合成字段运输证明。 |
| static_local_budget / static_budget_analysis | details保存局部比较、counter/limit声明和origin、更新/分支/helper、source_form_complete、候选及gap计数。数值、runtime consumption、termination、domination与whole-project unconsumed检查独立为false；不是预算通过判定。 |

导航consumer保存具体factory_context、callback参数来源、query_lookups、null_return_guards、callback_results和factory_null_throw_guards。direct-await仅解释正常fulfillment；returned_method_async为真时body throw对应rejected Promise，不是已发生同步异常。port_wiring含source_facts、model_applications、segments和unresolved；assembly_complete与end_to_end_complete分别表达，v0.7正式结果中五段有限装配支持而route_activation未知。literal import装配模型保留原动态CALLS，不创建确定边。

原子metadata明确assembly_state、authority_region_state、facade_to_authority_execution_chain_proved、bounded_interleaving和interleaving_inferred。当前装配可为policy_declared、保护为source_backed_protocol_model，整链和交错为false。find_push_same_member_path不表示collection_identity_verified；状态patch出处不表示转换已成功。wrapper/lifecycle未知不能解释为无保护。unknown样本有界，结论与计数不以样本替代完整缺口。

字段配置接受parameter_field_flow/all_direct_sites：subject={file,symbol,parameter_index,field_path}，sink为call_argument（callee/argument_index/field_path）或return（field_path）。注册ecmascript-own-enumerable-field-copy-v1，可另注册ecmascript-own-data-read-v1，保持conditional。sink.callee仅locator，实际目标需保存call span和确定边认证；未知callee、Get guard、effects、Promise/iterator或预算不足继续unknown。当前版本finite-field-summaries-5-ir/static-field-contracts-4-ir/static-field-policy-v2，公共IR为finite-immutable-semantic-ir-3，没有新增HTTP/MCP端点。

字段metadata保存assessment_counts/assessment_count、selected_field_shape_complete/source_form_complete及reaching_value_origin_proven=false、transport_proven=false、full_functionality_proven=false。details逐site保存site_location、edge_id、formal、conditions/branch_conditions、field_presence、selected_field_shape_closed、whole_object_shape_closed、field_sources、source_form_relation、copy_steps和completion。source_form_relation区分source_form_preserved_when_present/selected_field_absent/source_form_changed/unknown；条件式来源保留不证明字段实际存在或最初值稳定。summary.selected_shape_complete/source_form_complete/all_selected_sites_accounted不证明运行值或功能。

v0.11 每个 assessment 另含 `source_relations`、`local_copy_retention` 和 `local_copy_retention_supported`；details/metadata 保存 `source_relation_counts` 及 `local_copy_retention_supported_site_count`。这些计数描述独立证据轴，不修改旧的 `source_form_relation` 或完整目标状态。

`source_relations` 的版本为 `captured-field-source-relations-1`，`proof_domain=captured_ast_and_lexical_binding`。它保存实际参数/形参绑定、词法别名、当前 body-return 引用、顺序构造、显式 Set 尝试及选定源码前缀的写入扫描；记录所选 operand、source context、branch conditions、copy plans、coverage 和 analysis gaps。`no_explicit_static_target_match` 只表示已枚举范围中没有匹配的显式静态写入，`no_indirect_mutation_proven=false`；动态键、未支持控制、嵌套 callable/class 和不完整枚举按范围保留，不能读成无副作用或所有路径字段保留。

`local_copy_retention` 保存实际 spread 和匿名对象终点位置、成立条件及类型化 `CopyBoundaryObservation` / `CopyRetentionWitness`。当前 copy-source 的自有可枚举 data 字段若存在，且注册复制正常完成、后置固定键与所选键不重合、对象仍处于未暴露构造阶段并未被可达 effects 损伤，可支持 `conclusion="that copy-time value/reference is retained at this literal endpoint"`。checkpoint、完整 effect 检查和所有后置定义出处参与判断；未知 spread、计算键、accessor、prototype、escape、预算不足及未认证操作保留 gaps。`initial_parameter_origin_proven`、`presence_proven`、`runtime_value_verified`、`fulfilled_value_proven`、`transport_proven` 均保持 false；嵌套路径只证明顶层 slot 的引用保留，不证明 child 当前内容。

normal_returns只记录body_return_expression_only=true、fulfilled_value_proven=false；async返回表达式不能直接当Promise fulfilled值，继承then/thenable同化未求解。effect_barriers按真实ID去重，每site最多展示24项，保留effect_barrier_count/effect_barriers_truncated/effect_barrier_sample_limit/effect_evidence_snapshot_id；判定仍使用全部distinct barriers，不能从样本少或source shape封闭忽略effects。捕获来源、共享组件版本及summary_budget使不足可追溯。

source_facts中普通object_destructure_keys不创建copy；仅实际rest产生object_rest_copy及排除/绑定/浅复制范围。当前site保存ir_selected_value、copy_steps的ObservationRef与allocation/version、effect_barriers的roots/affected/protected及guard/reachability出处。actual Get事实另保存receiver/key/version与read-model guard。对象当前状态、copy观察、shared child、presence/source form/normal completion分别表达，IR数据不是运行对象认证。

IR v2增加有来源guard的construction_guard、不可重绑的initialized const cell及类型化BindingDomain。未暴露字面对象只在构造期间免受fallback全heap扩大，真实root/alias/escape仍有效，物化及bind/return/argument暴露前结束该寿命。模块live cell的替换域与cell引用对象的可变性分别保存；callee、receiver、实参和捕获cell仍进入effects。未知原始值的content不等于未知对象可达性，TS类型语法不产生运行capture。

IR v3 增加当前 copy 边界和构造终点见证；它们独立于 `FieldSlot` / projection，不清除 entry-origin barriers 或将未知 presence 改为 present。普通 Get 遇到受损 slot/value 时返回有真实 receiver roots 的未知，不能把旧来源读回新字面对象后当作封闭。`captured-lexical-bindings-3` 的 absence 扫描只把真正 binder 当声明，默认参数 RHS 中的引用不构成同名声明；实际运行子树、默认值、闭包与隐式 `arguments` 捕获仍保留 effects。

EvidenceRef的guard_ids/kind及其它内容字段变更须经规范evidence(...)构造器重算evidence_id。v0.10.1修复模块cell写后未知域的内部构造协议；[v0.10.0候选](../reports/astra-iteration7/SUPERSEDED_CANDIDATE.md)保留，新结果绑定新的工具和快照身份。

v0.10.1正式engine site的source_form_relation为source_form_preserved_when_present、selected shape/source-form为true；field_presence仍unknown、whole shape为false，分析阶段为call argument before callee activation。services helper的正式正常return摘要为maxRetries absent且selected/whole shape closed。queue/agent另四site仍unknown，Finding均uncertain；这些site计数不是目标覆盖。见 [字段评估](../reports/astra-iteration8/field-assessments.json)及 [第八轮报告](../reports/astra-iteration8/REPORT.md)。

v0.11 正式五个 site 保持上述来源形式边界，另保存 41 条 source-relations；agent-config.ts:489 的 direct literal return 是唯一 `local_copy_retention_supported=true` 的 site。该当前复制终点关系没有改变 async `source_form_relation=unknown`、presence、入口 origin 或 transport；关系和见证数都不是完整目标通过率，该历史版本的五目标为0/5、30义务为4限定支持/20partial/6unknown。见 [v0.11字段](../reports/astra-iteration9/field-assessments.json)、[独立关系](../reports/astra-iteration9/field-relations.json)及 [第九轮报告](../reports/astra-iteration9/REPORT.md)。

v0.9顶层budget_contracts仅支持bounded_for_loop与counter_exhaustion_guard，evaluation=all_lexical_sites；subject={file,symbol}，counter/limit各为{kind:local_binding,name}，只定位唯一声明，不能填阈值、比较、更新或消费结论。必须注册captured-local-budget-source-v1并保留provenance和conditional条件。来源/比较/增量/helper原文由保存AST与实际CALLS提取，相关而不支持的候选保留unknown；嵌套函数激活另列。source_form_complete只限局部语法关系，数值域、实际次数、termination、全部支配与上游预算归属均未证明。 stats.budget_contracts_count只计配置，组件为static-local-budget-contracts-1/static-local-budget-policy-v1。assessments中的source_form_state=source_backed_local_pattern与source_form_complete是限定源码结果；limit/helper原文未被求值，guard_or_loop_activation_proven/runtime_limit_value_proven等不得转为true。未支持的相关guard/header保留unknown且不删除分母。

共享BuiltinEnvironment.audit的supported表示当前认证文档内固定profile可启用，保存source/scope_identity/lexical_absence、model/policy、unresolved/host_aliases/opaque_effects；runtime_builtin_verified为false。completion摘要保存function kind、direct-await/returned-without-await、normal_value_relation_closed及控制条件；completion_guaranteed/body_activation_proved/runtime_verified不因此变真，资源生命周期未证明。组件版本为captured-builtin-environment-1/captured-completion-summaries-1，导航/port/原子共享迁移未增加resolved CALLS。

新语义位置保留snapshot_id、source_hash、semantic_parse_id、parse_identity、captured_text_utf8坐标、原文件byte偏移和span_hash；按column_base/column_unit读取列，不混用旧证据坐标。历史来源只读保存原文，新合同配置仍为数据，provenance作者审批与模型未验证条件可查。实际例见 [第四轮有限见证](../reports/astra-iteration4/finite-contract-witnesses.json)。

完整scan JSON的snapshot.input_evidence保存辅助原文；graph接口仍不内联它。`/evidence/source`使用原有file/snapshot_id参数读取已保存辅助内容，返回kind=support_input、text_hash、hash、status及error；旧快照缺记录时拒绝，不回读工作区。统计support_inputs_count/support_inputs_incomplete与代码files_parsed分开。分析支持`analysis.support_inputs`和显式Rust模型配置，所有身份进入扫描及缓存输入；不新增执行API或网络依赖。

模型绑定的边metadata保留receiver_helper_model、receiver_standard_interface_models。serde helper模型与Eq接口默认不启用；实际模型/标准库/工具链假设随基准见证保存，不解释为Cargo或宏展开完成。v0.6另有generic_impl_binding，模型为rust-generic-same-impl-lexical-v1，仅对同一固有impl的直接self/静态Self关系适用。

多语言统计在 `stats.by_language`，每个请求语言包含 `files_total`、`files_parsed`、`files_failed`、`nodes`、`edges` 及各调用解析状态数量。`files_failed` 表示没有完整解析，不只语法错误；未请求语言在 `unsupported_files` 单独报告。`coverage_incomplete` 与 `call_resolution_incomplete` 分别说明文件范围与调用解析缺口，快照可为 `partial`。能力列表不等于当前项目各语言已完整分析。

TypeScript 的有限派生语法信息位于模块节点 `metadata.syntax_projection`，含 `mode`、`applied`、`accepted`、`source_file_sha256`、`original_text_utf8_sha256`、`derived_text_utf8_sha256`、`raw_errors`、`derived_errors`、`edits` 与 `position_map`。未使用或被拒绝时部分字段可省略。每项 edit 保存 rule、原/派生范围和内容、证据；适配节点/边的 `source_parse_mode`、`syntax_projection_version`、`source_projection_node` 关联该模块。诊断 `ts_syntax_projection` / `ts_projection_partial` 及语言统计 `syntax_projected_files`、`raw_parse_error_files` 保留原解析器缺口。适配后的 `parsed` 表示限定语法范围可解析，不能解释为类型或功能通过；源码接口始终返回原文。

Rust 的有限具体 Self 绑定可从边 `metadata.receiver_type`、`receiver_type_declaration`、`receiver_impl_location`、`receiver_binding_location`、`target_declaration`、`target_impl_location` 和 `binding_basis` 下钻；字段按关系适用范围出现。节点保留 impl 类型/trait/泛型及声明位置，不把具体 trait impl 内的固有目标绑定解释成所有 trait 分派可解析。泛型同 impl 模型在 generic_impl_binding 中保存 same_impl_identity（file/source_hash/字节范围/header/声明）、源/目标方法、参数计数及未验证标记；frontend_stats.rust 中 generic_same_impl_model/generic_same_impl_resolved_calls 是有限模型统计。其它泛型关系、字段接收者和 dyn/trait 等仍可未知；trait 默认成员来源不完整时还可见 `trait_default_members_unknown`、`unmodeled_trait_receiver_count` 及具体 reason。范围见 [STATIC_SCOPE.md](STATIC_SCOPE.md)。

`GET /status` 的 `capabilities` 还包含 `maintenance_engine`、`incremental_computation`、`incremental_granularity`、`global_detection` 与 `graph_backend`。CocoIndex 模式的计算复用粒度为 `language`，全局检测仍为 `full`；这些字段不表示逐文件语义增量。成功维护的运行信息位于 `analysis.maintenance`，包含引擎版本及重算、复用和不缓存语言列表。失败时应先阅读 `analysis.state` 和 `last_error`，不能将保留的上次维护信息当成本轮成功结果。HTTP 不允许在请求中临时改引擎，引擎由服务启动参数固定。

请求体使用 JSON：

```json
{
  "snapshot_id": "SNAPSHOT_ID",
  "from": "app.api.submit_order",
  "to": "app.storage.write_order"
}
```

以上用于 `POST /query/path`。其他写入或查询结构如下：

| 路径 | 请求对象 |
|---|---|
| `/scan` | 无需项目路径参数；目标由服务启动参数固定 |
| `/config` | `{ "config": { ... } }` |
| `/graph/subgraph` | `{ "snapshot_id": "...", "node_id": "...", "depth": 2, "direction": "both" }` |
| `/diff` | `{ "from_snapshot": "...", "to_snapshot": "..." }` |
| `/decisions` | `{ "snapshot_id": "...", "finding_id": "...", "action": "fix_planned", "reason": "...", "expires_at": "..." }` |

`expires_at` 可省略；提供时使用包含时区的未来 ISO8601 时间。处置保存原始发现，不能通过处置重写证据。配置保存成功不等于新分析完成，客户端应再发起 `POST /scan`；旧快照保留旧配置对应的发现。

源码接口只接受指定快照已保存的相对文件路径，不开放任意服务器文件读取。路径查询的结果是静态关系，必须结合解析状态阅读。

路径状态为 `found`、`not_found` 或 `unknown`，其中完整性仅针对显式静态调用模型。差异结果中的 `resolved` 表示新版本没有再报告该发现，不能直接解释为已修复；`comparison` 提供项目、规则、引擎/模式及语言解析组件等可比性信息，`same_parser_version` 明确指出解析组件身份是否一致。

路径查询与局部图响应的 `gaps` 最多展示 20 项解析缺口，并返回 `gap_count`、`gaps_truncated`、`gap_sample_limit: 20` 和 `gap_snapshot_id`。`full_gap_evidence` 为 `snapshot_edges_diagnostics_and_source_statuses`，完整依据仍在该快照的调用边、诊断与源码状态中。`status`、`complete` 和搜索结论使用完整缺口集合，采样不会截断路径搜索。局部图原有的 `truncated` 仍表示展示深度导致的图范围截断，与 `gaps_truncated` 分开阅读。

## MCP

MCP 通过 stdio 的按行 JSON-RPC 接入 AI 编码助手，stdout 仅输出协议消息。服务启动不自动扫描；先调用 `scan_project` 或查询已有项目快照。

| 工具 | 参数及行为 |
|---|---|
| `scan_project` | 无参数，对启动时固定的项目根目录全量捕获源码，按服务固定引擎计算前端，检测全量 |
| `query_graph` | 可选 `snapshot_id`；提供 `node_id` 时按 `depth`、`direction` 查询局部图，否则返回全图 |
| `get_anomalies` | 可选 `snapshot_id`、`severity`、`type`、`q`，读取发现 |
| `get_project_report` | 可选 `snapshot_id`，读取项目报告，分别呈现完整判断、功能链、局部证据与未审范围 |
| `get_evidence` | 可选 `snapshot_id`；提供 `finding_id` 时返回发现与证据，否则必须提供 `file`，可选 `line`，读取快照源码 |
| `find_call_path` | 必填 `from`、`to`，可选 `snapshot_id`，返回一条确定路径或未知/未找到状态 |
| `list_versions` | 无参数，列出服务当前项目的快照 |
| `compare_snapshots` | 必填 `from_snapshot`、`to_snapshot`，比较当前项目两个已保存快照 |

局部图 `depth` 为 0 到 8，`direction` 为 `both`、`in` 或 `out`。这些展示限制不截断检测器的路径判断。MCP 不提供任意 Cypher 或 shell，不允许更换项目根目录。

没有 `trigger_verify`、执行代码、测试、构建或沙箱工具，也没有通过 MCP 自动修复目标源码的操作。

## 部署边界

首版没有企业认证或跨租户授权，HTTP 服务仅接受 `127.0.0.1` 或 `localhost`，并校验请求 Host 与同源写入。它是本机工具，不提供公网部署能力。

本轮没有运行任何测试套件、目标程序或 E2E 流程。正常启动 CallScope 或进行只读静态扫描不等于执行被分析项目，也不构成目标功能测试通过。接口文档描述实现协议，不构成业务正确性或性能验收声明。

v0.11 正式 [保存查询](../reports/astra-iteration9/saved-query-observations.json)读取两库最终快照，七种有限类型经原接口返回10个有限Finding、21次保存源码响应；响应都绑定正式快照。field普通查询返回3合同/5site及1个当前copy终点支持，engine正常前缀conditional来源形式保留、另四入口field结果unknown，两预算模式仅源码支持。配置数CPB18/WWC12和返回数都不是满足数或功能覆盖率。该历史轮次的五项实现追踪见 [GOAL_ACCEPTANCE](../reports/astra-iteration4/GOAL_ACCEPTANCE.md)、[v0.11 goal-ledger](../reports/astra-iteration9/goal-ledger.json)与 [REPORT](../reports/astra-iteration9/REPORT.md)。账本为人工评审映射正式证据，五claim partial、完整0/5，4限定支持/20partial/6unknown；没有通用自动义务solver或新增goal HTTP/MCP入口。原26项仍10/3/13。
