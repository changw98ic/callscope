# 原完整报告与 v0.13 正式自动报告的范围差距

本轮两库正式扫描和保存产物均已闭合。原五项具体条件判断保持自动承接；CPB 的十三条、WWC 的十八条条件源码关系均保存为 `scoped_source_relations_supported`，其中包含本轮十三条新增查询。原来的三个 WWC partial 也已解除错误的声明属性上下文限制。**这些是真实源关系状态，不是三十一种业务功能通过或全文覆盖率。**

原已读内容还存在两类明确距离：Device 架构文档具体绝对声明与真实部署来源的差异，尚未自动作对应比较；两库的有限架构职责说明仍主要保存为结构、写者和接口证据引用，尚未自动汇总成原职责表那样的具体分工解释。后文只将这些原文实际说过的有限命题列作差距，不把唯一 owner、全授权、全协议、完整状态机或物理效果追加为验收目标。

## 正式依据与定位

依据是 [CodePatchBay 原报告](../astra-baseline/CODEPATCHBAY_ANALYSIS.md)、[WinWinCode 原报告](../astra-baseline/WINWINCODE_ANALYSIS.md) 和 [v0.12 范围差距](../astra-iteration10/REPORT_SCOPE_GAPS.md)。本文件只比较已保存产物，没有重新审查目标代码、调用分析器、打开数据库或增加 Astra 把关。巨大 source_facts 留在正式 JSON；流式投影仅保存数量与原 Pointer。

| 项目 | 正式快照 | 正式报告 SHA256 |
| --- | --- | --- |
| codepatchbay | `7b58e73339e7ad28592c4a0bede1da0028935b30edd940419841971b354c2bfe` | `6fe5fe8a23ce386b3d5641ed6f8964d6bb5aa90f19b735ff03d0f2bf6b046fb0` |
| winwincode | `cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2` | `01b324f5d68c082a673d034dc6117e53e7fb05c7c252f06107a794e388249135` |

原正式文件：[CodePatchBay](codepatchbay-automatic-report.json)、[WinWinCode](winwincode-automatic-report.json)。下文 `C:/…` 与 `W:/…` 分别是两文件的 JSON Pointer；精确 Finding/Evidence ID、文件 SHA、范围、实际 gaps 和开发来源沿革见 [scope-pointer-map.json](scope-pointer-map.json)。

冻结工具身份为 `c4c127375f044133c328c1fd17782df277426bf64e4bed0be8779602088fafee`。两份 integration 均记录数据库关闭、WAL 为空；cold 创建新快照，warm 返回同一快照且 `created=false`。本轮采用全量前端/检测重算，不能当作与 v0.12 相同维护引擎的性能比较。

[账本身份核对](scope-ledger-identity.json) 将五个保存判断与正式快照、source/policy、冻结 tool 和 [goal-ledger.json](goal-ledger.json) 对齐。账本记录五项 `scoped_static_judgment_reproduced`、三十项必要关系 `supported`、无未闭合必要关系；这是原五项判断的实现跟踪，未替代两份完整报告。

原 [二十六项冻结观察对照](ORIGINAL_BASELINE_COMPARISON.json) 保留十项 reproduced、三项 unknown、十三项 evidence_only，未重定义旧分母；[PUBLICATION_IDENTITY.json](PUBLICATION_IDENTITY.json) 的 `verified=true`。该对照不等于全文或功能覆盖率。

## 一、原已读明确命题尚未同等自动承接

| 原文有限命题 | 当前正式保存内容 | 具体剩余距离 |
| --- | --- | --- |
| [WWC Device 文档口径差异](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:88) | `W:/functional_chains/5/pattern` 已保存 Server boundary、Worker/Device provider 构造和安装来源；`W:/functional_chains/1/pattern/unreviewed_scope` 明确保留文档一致性范围。 | 尚未自动定位并比较文档中“长期 Credential/Provider 唯属 Control Plane”的具体绝对表述与 Device 生产来源。需要的是原文这个局部说明差异，不是全架构文档规范或所有 credential 安全审计。 |
| [CPB 有限架构职责表](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:30) | `C:/architecture/meaning` 仍限定目录组成/已认证引用；`C:/architecture/captured_writer_references/0` 和 `C:/functional_chains/0/pattern/responsibility_interpretation` 提供 event/job/queue 写者与接口证据。 | 尚未自动汇总原表中的 CLI 提交/投影、orchestrator assignment/attempt、worker/bridge 消息/进程、engine 注入端口与 service 实现等具体分工解释。源链和写者已可下钻，不把这些来源缺少解释等同目标缺实现。 |
| [WWC 有限职责与身份表](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:30) | `W:/architecture/captured_writer_references/0`、`W:/functional_chains/1/pattern/responsibility_interpretation` 及 `W:/functional_chains/12/pattern` 提供具体 writer/interface 与身份字段。 | 已有所选身份分离来源，但报告尚未自动把它们汇总为原表中 Client 表现/协议、Control Plane/Delivery 产品状态、Worker 执行事实、adapter/Kernel 接线的有限职责说明。 |

以上两类差距是原文中的具体比较或报告解释。新写者模式的 `partial_captured_writers_and_consumers` 不是失败判据：只要有限来源足以支持原句，就可以承接原句；不要求证明 canonical 唯一所有者、全部写入者、全堆资源等价或全部授权。

## 二、已承接的有限段落与原报告相同的限制

### 原五项具体条件判断

| 原判断 | 正式位置 | 保存状态 |
| --- | --- | --- |
| CPB-01 | `C:/judgments/0`；finding `1978d3f48218391a36a82e8f`，evidence `3df40e7e4b2844a5dd6506ca` | `scoped_static_judgment_reproduced`；complete/full 均 true，必要 gaps 为空。 |
| CPB-02 | `C:/judgments/1`；finding `e465a1162af15e0336a0c410`，evidence `f493e9c9e901101b279f221c` | `scoped_static_judgment_reproduced`；complete/full 均 true，必要 gaps 为空。 |
| CPB-03 | `C:/judgments/2`；finding `d55451aeec7a362795d8447d`，evidence `1dddaf6898b23e4f45015e0d` | `scoped_static_judgment_reproduced`；complete/full 均 true，必要 gaps 为空。 |
| WWC-01 | `W:/judgments/0`；finding `8587a3dad0bef1ede9bfd666`，evidence `e8f805eaeedf86b71cf0237b` | `scoped_static_judgment_reproduced`；complete/full 均 true，必要 gaps 为空。 |
| WWC-02 | `W:/judgments/1`；finding `7e7dc738afda264f3b24a0d8`，evidence `9144dc2875788bfdba88323b` | `scoped_static_judgment_reproduced`；complete/full 均 true，必要 gaps 为空。 |

重试预算、终态分类、幂等交错、公开导航缺上下文和 Device 条件字段遗漏各自保留真实条件与反证；没有扩大成所有重试、恢复、双提交或创建入口均失败。完整条件以各 judgment 及其 adapter evidence 为准。

### 十三条新增查询对应的正式有限关系

下表状态直接来自保存 assessment，十三项均为 `scoped_source_relations_supported`。字段数量和条目数只帮助定位，不作为功能成熟度计量。

| 原已读段落 | 新条目与正式 Pointer | 本轮具体承接 | 原文同样保留的范围 |
| --- | --- | --- | --- |
| [codepatchbay:48](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:48) | `cpb-report-readiness-abrupt-guard`；`C:/functional_chains/8` | readiness return/throw→enqueue 正常到达条件 | readiness 外部环境是否可用 |
| [codepatchbay:72](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:72) | `cpb-report-completion-gate-conditions`；`C:/functional_chains/4` | checklist 字段消费、逐门条件、mutating 等价单元及各返回路径 | checklist 内部全部判定与外部 verdict 真实性 |
| [codepatchbay:64](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:64) | `cpb-report-access-audit-response`；`C:/functional_chains/2` | access audit await/catch→同 response 字段→writer 实参 | callback 实际激活、审计持久成功、网络响应和业务回滚 |
| [codepatchbay:76](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:76) | `cpb-event-index-projection`；`C:/functional_chains/1` | serializer→append、projection→index writer、readEvents→materializer→rebuild | 物理持久、一体事务、全部恢复与 doctor 成功 |
| [codepatchbay:68](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:68) | `cpb-trusted-command-lineage`；`C:/functional_chains/11` | stdout→JSON→policy parser→resolver→executable/args→shell=false | 全 heap/分支非干扰；expectedEvidence 的其他保护路径作用 |
| [codepatchbay:70](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:70) | `cpb-unsupported-record-retention`；`C:/functional_chains/12` | failure marker→返回集合→ledger→artifact content；first-wins/覆盖来源 | 所有输入记录均保留、abort/异常和写入效果 |
| [codepatchbay:30](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:30) | `cpb-captured-record-resource-writers`；`C:/functional_chains/0` | 所选写者、构造、接口交接、拒绝 guard 与同 token 引用 | canonical authority、唯一 owner、全部资源/写入者和完整授权 |
| [winwincode:60](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:60) | `wwc-report-workrun-finite-selection`；`W:/functional_chains/16` | 有限 iterator/enum/depends-on 关系、active 集合与 selected ID recheck | 完整领域状态机、全 enum/attempt、调度与并发 |
| [winwincode:54](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:54) | `wwc-report-chat-retained-request-identities`；`W:/functional_chains/4` | 当前 attempt 的 create/items/start 请求与 delivery 字段来源 | 网络/后端成功、任意自动重试和全部 Chat 命令 |
| [winwincode:42](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:42) | `wwc-report-worker-adapter-record-identities`；`W:/functional_chains/12` | dispatch/lease/job/workspace/thread/session/turn 的所选记录投影与消费者 | 跨全部 wire 的同一实际值、所有租约、泛型唯一实现与故障收尾 |
| [winwincode:78](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:78) | `wwc-report-outbox-ack-correlation-fields`；`W:/functional_chains/9` | 所选 Family 关联字段域、有序 tuple、编码/SQL 插入与删除参数来源 | 全部 Family、sequence→ack_sequence、外部 ack、持久效果和 exactly-once |
| [winwincode:48](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:48) | `wwc-browser-continuation-lifecycle`；`W:/functional_chains/0` | generation 形实参、nullable context、abort/closed/代次 guard 与悬挂后局部写回来源 | 完整 auth/scope 规范、全部 callback 旧结果拒绝、DOM/网络效果与资源释放 |
| [winwincode:30](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:30) | `wwc-captured-record-resource-writers`；`W:/functional_chains/1` | 所选 state/record 赋值、接口交接、消费者与拒绝来源 | 唯一事实权威、跨过程资源等价、全部写者和权限合同 |

readiness 的普通记录分区与 null/缺值 unknown 分开；completion 的当前门依赖与完整前序路径条件分开，不把 readonly/docs/parent 的 verify 豁免扩大为所有门豁免。access audit 的失败 response 与 job 尾部 best-effort audit 是不同对象。上述区别是原报告有限解释的承接，不要求实际执行外部检查或网络响应。

WorkRun 的有限状态表和依赖/活动选择已与所选 ID recheck 相连；这足以承接原文的所选检查，不要求完整领域状态机。Chat 的阶段请求身份保持独立；Worker/adapter 的 job/lease/workspace/thread/session 来源分开；outbox 的字段域一致关系不假定两条线上消息值相同。浏览器 guard 按具体 callback、正常继续和 suspension 边界保存，缺少局部 guard 没有自动归为新缺陷。

### 旧主要链与三个 partial 的实际变化

原六条 CPB 和十二条 WWC 主要源码规则均仍存在。CPB 的 engine 前置阻断、agent/env/sandbox、finalizer→持久结果→reconcile、job audit、trusted probe 和失败记录来源保持；WWC 的 Chat、typed dispatch、adapter/Kernel、三个不同 Kernel API 和 intent→persist→exact reconcile 保持。

| 原 WWC partial | 正式位置与状态 | 仍保留的同等边界 |
| --- | --- | --- |
| `wwc-report-worker-bootstrap-entries` | `W:/functional_chains/13`；`scoped_source_relations_supported`。 | 声明属性上下文修复不等于任意 trait/宏分派、运行启动或 provider 凭据可用。 |
| `wwc-report-worker-production-construction` | `W:/functional_chains/14`；`scoped_source_relations_supported`。 | 声明属性上下文修复不等于任意 trait/宏分派、运行启动或 provider 凭据可用。 |
| `wwc-report-device-provider-deployment` | `W:/functional_chains/5`；`scoped_source_relations_supported`。 | 声明属性上下文修复不等于任意 trait/宏分派、运行启动或 provider 凭据可用。 |

这些条目按原规则读取当前正式快照，解除的是 crate 内建编译限制属性被误当成未知宏导致的声明绑定障碍；不是把候选或同名方法强行补成唯一 CALLS。Device 部署仍保留 source-only credential/全分派边界。

WWC 的 `wwc-report-adapter-durable-exact-turn` 与 `wwc-report-submission-intent-kernel-order` 选择同一 submit_turn 来源，正式 `/overlapping_source_selections` 已标明重叠；不能把两个条目累计成额外功能。

### 正式 source-only gaps 原样保留

以下 gaps 不会被 scoped 状态掩盖。它们描述源模型或原文同样未提供的效果保证；不能直接变成原报告新增未完成项。

| 正式位置 | 保存的 gap code | 保存边界标记 |
| --- | --- | --- |
| `C:/functional_chains/1/analysis_gaps/0` | `record_projection_physical_commit_and_all_recovery_not_proven` | source_only=true；necessary_to_scoped_source_relations=false |
| `C:/functional_chains/9/analysis_gaps/0` | `structured_command_intermediate_values_and_external_effects_not_fully_proven` | source_only=true |
| `C:/functional_chains/10/analysis_gaps/0` | `structured_record_markers_do_not_prove_all_input_retention_or_persistence` | source_only=true |
| `C:/functional_chains/11/analysis_gaps/0` | `record_command_source_dependencies_do_not_prove_full_heap_noninterference` | source_only=true；necessary_to_scoped_source_relations=false |
| `C:/functional_chains/12/analysis_gaps/0` | `record_true_marker_does_not_prove_all_input_or_artifact_retention` | source_only=true；necessary_to_scoped_source_relations=false |
| `W:/functional_chains/5/analysis_gaps/0` | `deployment_candidate_chain_not_global_dispatch_or_credential_availability` | source_only=true |
| `W:/functional_chains/17/analysis_gaps/0` | `iterator_selection_and_macro_runtime_semantics_not_fully_proven` | source_only=true |

### 源码范围与原冻结观察

CPB 选入 333 份、完整解析 330 份，三份 Shell unsupported；WWC 选入 471 份、完整解析 465 份，六份 Rust parse_error。路径与原因见两正式报告的 `/coverage/unparsed_files`。这是语法捕获范围，不是功能完整率。生成合同的所选 support inputs、测试/第三方和配置排除范围按正式 `/coverage` 保留。

旧局部 contract 的 uncertain 和图中的 dynamic/ambiguous/unresolved 继续保留；它们的口径不等于完整 judgment，也不等于目标缺少实现。循环/递归本身没有被升级为不终止缺陷。

## 三、原本未审及更强命题边界；不作为本轮剩余目标

原 CPB 未逐分支审核所有 CLI/workflow、HTTP/OIDC、备份/发布 provider、全部异常恢复、本地代码索引算法和所有平台/adapter；原 WWC 未穷举所有 HTTP/WS、领域状态机/并发、credential 路径、vendored Kernel、全部 publication/audit/export/connector 副作用、平台/迁移。依据是两原报告的覆盖账本及 WWC 外部交付边界。

因此，完整协议、所有入口/分支生命周期、全授权、唯一 canonical owner、所有物理提交/外部 ack/发布/隔离效果、全故障恢复不是原报告已经完成而本轮必须补齐的命题。正式模型的相关 false 值应保留，但不能把它们列作新的验收缺口，更不能为了消除它们要求运行目标或测试。

两正式 `/report_scope/whole_report_reproduction_claimed=false`，`/runtime_functionality_verified=false`。前者与第一节的具体报告差距分开解释，后者与原报告未运行验证的范围一致。本轮未执行、导入、测试或构建目标，也没有新增测试套件或 Astra 批准步骤。
