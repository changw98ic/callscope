# 原完整报告与 v0.13 自动报告的范围对照草稿

本中途草稿已由 [最终范围差距](REPORT_SCOPE_GAPS.md) 替代。以下保留当时只读到 CPB 的过程状态，不作为最新结论。

**状态：只已读取闭合的 CPB v0.13 正式结果；WWC 正式结果尚未读取，本轮两库对照尚未完成。** 原两份完整 Astra 报告仍是比较依据；新增十三条查询是实现工作分组，不是新的功能覆盖分母。开发查询提供实现证据，不能替代新版本保存的 Finding、Evidence 和快照身份。正式数据完成后，应逐项核对再生成 `REPORT_SCOPE_GAPS.md`，不能把本草稿中的计划范围直接变成“全部支持”。

本次整理读取原报告、上一轮范围差距、当前 policy 元数据、已经保存的开发产物及闭合的 CPB 正式报告。正式 JSON 经 `_SavedJSON` 流式投影，巨大 source_facts 留在原文件，只保留真实数量和 Pointer。没有重新审查目标项目，没有调用分析器、读取数据库、运行目标或增加 Astra 审核流程。各文件 SHA256、准确 JSON Pointer 及已读取的正式身份见 [scope-pointer-map.json](scope-pointer-map.json)。

## 固定比较依据

- [CodePatchBay 原完整报告](../astra-baseline/CODEPATCHBAY_ANALYSIS.md)，目标提交 `4f2d2eca31d90b0122db1c1429dd365672db2393`。
- [WinWinCode 原完整报告](../astra-baseline/WINWINCODE_ANALYSIS.md)，目标提交 `da407e4f3df3719718b23bd8913b73fe3ff73857`。
- [v0.12 正式范围差距](../astra-iteration10/REPORT_SCOPE_GAPS.md)。其中五项具体条件判断已经有正式结果；v0.13 是否保留，须以本轮正式账本核对，不能由本草稿预填。
- [本轮策略扩展记录](POLICY_EXTENSION.json)。原十八条主要源码关系规则保留，CPB 增加七条、WWC 增加六条。此数量不代表十八或十三种功能，也不代表全文完成比例。

原报告中的“完整”包含阅读范围、主要域、关键链、证据、反证和未审范围；它没有宣称逐行、全状态机或运行正确。对照不能把原作者明确未审的范围额外扩大为本轮验收目标，也不能把目录盘点或局部关系提升成原文全部判断。

对照只分三类：**原已读明确命题仍待自动承接、已经承接的有限段落及相同限制、原本未审或更强命题的模型边界。** 第三类不进入第一类，不因模型保留 false 就制造新的未完成目标。原架构职责表本身也是有限源码解释，没有证明全项目唯一 owner、全部授权或所有写入均经某条权威路径。

## 十三条新增查询与旧缺口的对应

下表保留十三条模型的**开发查询**入口，方便追溯实现；CPB 七条的正式状态和 Pointer 另见下一节，WWC 六条仍待正式核对。表中的“承接关系”描述模型的有限范围，不预填未读取的正式结果。

| 原报告与上一轮缺段 | 新查询 ID / 开发入口 | 承接的有限关系 | 模型边界；不新增验收项 |
| --- | --- | --- | --- |
| [CPB fix readiness 提交前早退](../astra-baseline/CODEPATCHBAY_ANALYSIS.md:48) | `cpb-report-readiness-abrupt-guard`；[gates-source-query.json](gates-source-query.json) `/results/0` | 实际 readiness 结果声明、失败谓词、同块提前 return/throw 与后续 enqueue 的正常到达。 | readiness 外部环境的真实可用性；null/缺值不强行解释为普通结果记录。 |
| [CPB completion 条件门与豁免](../astra-baseline/CODEPATCHBAY_ANALYSIS.md:72) | `cpb-report-completion-gate-conditions`；[gates-source-query.json](gates-source-query.json) `/results/1` | checklist 返回字段的消费者、mutating 谓词有限单元、逐门当前条件和完整返回路径条件。 | 不能把 verify 豁免推广成 checklist/adversarial 的全面豁免；外部 verdict 内容和 checklist 内部全部判定未由该模型证明。 |
| [CPB Hub access audit 与 job audit 分属不同对象](../astra-baseline/CODEPATCHBAY_ANALYSIS.md:64) | `cpb-report-access-audit-response`；[gates-source-query.json](gates-source-query.json) `/results/2` | audit opener、实际 await、catch 的同一 response 字段及 response writer 实参。 | callback 实际激活、持久成功、网络发送和已发生业务修改的回滚；不与 job best-effort 合并。 |
| [CPB 事件提交、索引投影与重建](../astra-baseline/CODEPATCHBAY_ANALYSIS.md:76) | `cpb-event-index-projection`；[records-event_index_projection.json](records-event_index_projection.json) `/pattern` | serializer→append、projection callback.state→index 记录→writer、readEvents→materializer→rebuild writer。 | 独立源码调用边界不等于一次事务或物理提交；全部崩溃恢复和 doctor 完成仍未证明。 |
| [CPB trusted command 精确来源](../astra-baseline/CODEPATCHBAY_ANALYSIS.md:68) | `cpb-trusted-command-lineage`；[records-trusted_command_lineage.json](records-trusted_command_lineage.json) `/pattern` | stdout→JSON→policy parser→lookup→command；同一 formal 的 executable/args 与 shell=false。 | 不宣称全 heap/分支非干扰；expectedEvidence 仍可参与独立保护路径和 provenance 分支。 |
| [CPB unsupported evidence 保留路径](../astra-baseline/CODEPATCHBAY_ANALYSIS.md:70) | `cpb-unsupported-record-retention`；[records-unsupported_record_retention.json](records-unsupported_record_retention.json) `/pattern` | true marker、返回集合、ledger skip 条件和 artifact content 来源；first-wins、spread 等反证来源。 | 缺身份/checklist、hardGate 先入、覆盖、abort/异常和写入失败；不是所有输入均保留。 |
| [CPB 职责和事实所有权](../astra-baseline/CODEPATCHBAY_ANALYSIS.md:30) | `cpb-captured-record-resource-writers`；[ownership-codepatchbay-source-query.json](ownership-codepatchbay-source-query.json) `/analyses/0` | 所选字段写者、普通构造、接口交接、同 token 引用与拒绝来源。 | 局部 binding/记录赋值不等于持久事实权威；canonical authority、唯一 owner、全部资源和权限仍未证明。 |
| [WWC WorkRun runnable/dependency/active](../astra-baseline/WINWINCODE_ANALYSIS.md:60) | `wwc-report-workrun-finite-selection`；[workrun-source-query.json](workrun-source-query.json) `/pattern` | 源 iterator/enum 的有限状态表、依赖量词、活动集合投影、所选 ID 回送 start_item 及 validation 前提。 | 标准迭代器/宏/Clone 模型、选中 helper 来源条件；完整领域状态机、所有 enum/attempt、并发和调度仍未证明。 |
| [WWC Chat 保留请求身份](../astra-baseline/WINWINCODE_ANALYSIS.md:54) | `wwc-report-chat-retained-request-identities`；[messages-source-query.json](messages-source-query.json) `/results/0` | 当前 attempt 的 create/items/start 请求来源、delivery 字段、requestId 比较及赋值条件。 | 阶段 requestId 彼此独立；网络、后端提交、任意自动重试和全部 Chat 命令成功不由该结构保证。 |
| [WWC Worker/adapter/Kernel 身份分离](../astra-baseline/WINWINCODE_ANALYSIS.md:42) | `wwc-report-worker-adapter-record-identities`；[messages-source-query.json](messages-source-query.json) `/results/1` | typed dispatch binder、job/lease/workspace/profile、canonical thread/Kernel session 与所选 submit/persist/exact reconcile 字段。 | 所选记录投影不等于每条线上消息值相同；泛型 Codex 仍是上下文接口，不推导唯一运行实现或全部租约/故障收尾。 |
| [WWC durable outbox/ack](../astra-baseline/WINWINCODE_ANALYSIS.md:78) | `wwc-report-outbox-ack-correlation-fields`；[messages-source-query.json](messages-source-query.json) `/results/2` | 所选 Family 的有序关联字段域、frame 编码/metadata/SQL 参数以及 ack target→DELETE 参数。 | 字段域一致不是外部 payload/ack 真实；全部 Family、间接 Outcome tuple、sequence→ack_sequence、物理持久和 exactly-once 仍未证明。 |
| [WWC scope 与 lazy render generation/abort](../astra-baseline/WINWINCODE_ANALYSIS.md:48) | `wwc-browser-continuation-lifecycle`；[lifecycle-source-query.json](lifecycle-source-query.json) `/analyses/0` | generation 形实参、nullable context 返回、abort/closed/代次 guard、悬挂后的局部写回条件与所选关闭补偿。 | 局部 scope null 拒绝不是完整授权合同；父 guard 不跨 callback/await 自动继承；全旧结果拒绝、DOM/网络效果及全部资源释放未证明。 |
| [WWC 职责和事实所有权](../astra-baseline/WINWINCODE_ANALYSIS.md:30) | `wwc-captured-record-resource-writers`；[ownership-winwincode-source-query.json](ownership-winwincode-source-query.json) `/analyses/0` | 所选 state/record 的写者、消费者、接口和拒绝来源。 | whole-repository ownership、canonical authority、跨过程资源等价和全部授权仍未证明；不是按目录名补责任。 |

各条 purpose、conditions 或配置反证不充当源码事实。正式更新时应同时引用真实 `/pattern`、`/source_facts`、`/source_scope`、`/analysis_gaps` 与 assessment；不能只抄 `scoped_source_supported` 一个布尔值。

## 已闭合的 CPB 正式映射

CPB integration 记录 `database_closed=true`、WAL 为空；cold 创建新快照，warm 返回同一个快照且未创建新快照。以下仅表示 CPB 已保存的正式结果，不表示 WWC 已完成。

- 快照：`7b58e73339e7ad28592c4a0bede1da0028935b30edd940419841971b354c2bfe`。
- 原正式文件：[codepatchbay-automatic-report.json](codepatchbay-automatic-report.json)，SHA256 `6fe5fe8a23ce386b3d5641ed6f8964d6bb5aa90f19b735ff03d0f2bf6b046fb0`。
- 冻结 tool：`c4c127375f044133c328c1fd17782df277426bf64e4bed0be8779602088fafee`；与报告 `/snapshot/component_versions/tool/source_hash` 一致。
- 流式投影：[scope-codepatchbay-formal-observations.json](scope-codepatchbay-formal-observations.json)。完整 source_facts 未复制；原数组位置、Finding/Evidence ID 和 gaps 存在映射中。

CPB 的原三项具体判断在 `/judgments/0`、`/judgments/1`、`/judgments/2` 分别保留 `scoped_static_judgment_reproduced`、`complete_assessment=true`、`full_goal_supported=true`、`necessary_gaps=[]`。十三条主要源码关系的保存状态均为 `scoped_source_relations_supported`，这不是十三种业务功能通过。

| 新增 CPB 条目 | 正式 Pointer | source facts | 正式 analysis_gaps 与解释 |
| --- | --- | ---: | --- |
| readiness | `/functional_chains/8` | 38 | `[]`；提交前失败提前返回的有限关系。 |
| completion gate | `/functional_chains/4` | 78 | `[]`；当前门与前序路径条件分开；外部证据真实性仍属原报告相同边界。 |
| access audit | `/functional_chains/2` | 61 | `[]`；同 response 及 writer 实参来源，和 job audit 分开。 |
| event/index projection | `/functional_chains/1` | 971 | `record_projection_physical_commit_and_all_recovery_not_proven`；`source_only=true` 且 `necessary_to_scoped_source_relations=false`。 |
| trusted command lineage | `/functional_chains/11` | 466 | `record_command_source_dependencies_do_not_prove_full_heap_noninterference`；同样是非必要 source-only 边界。 |
| unsupported record retention | `/functional_chains/12` | 1610 | `record_true_marker_does_not_prove_all_input_or_artifact_retention`；同样是非必要 source-only 边界。 |
| captured resource writers | `/functional_chains/0` | 299 | `[]`；`ownership_assessment=partial_captured_writers_and_consumers`，实际 writer/interface 引用支持。 |

旧 trusted command 与 unsupported record 条目分别在 `/functional_chains/9/analysis_gaps`、`/functional_chains/10/analysis_gaps` 保留旧 source-only 说明；新条目补具体中间关系，没有删除这些旧限制。事件与索引仍区分源码提交调用边界和物理效果；这些限制与原报告一致，不改列为新的剩余目标。

## 三个旧 partial 的声明上下文修复：另列，不算新增十三条

[Rust 上下文开发材料](RUST_SOURCE_CONTEXT_DESIGN.md) 记录 crate 内建编译限制属性曾被误归为未知属性宏。已有 [开发查询](RUST_REPORT_CLAIMS_DEVELOPMENT_QUERY.json) 分别保存 `wwc-report-worker-bootstrap-entries`、`wwc-report-worker-production-construction`、`wwc-report-device-provider-deployment` 的新来源关系。这三条仍使用原规则，不构成新的产品发现或新增功能分母。

本轮正式状态尚未读取。正式检查应区分：源码声明身份/既有步骤是否解除错误 opaque；任意宏/trait 目标分派是否仍未知；Device 部署候选是否被错误扩大为 provider 凭据可用。修复前后的原始输入/解析状态和必要限制都要保留，不能为了来源条目变绿而把 WorkerMain::new 等动态调用补为确定 CALLS。

## 第一类：原已读明确命题的有限承接待核

本节只列原报告实际表达过的有限命题。CPB 已读取，WWC 尚待正式结果；最终只把正式产物中确实没有的对应结论列为剩余差距。

| 原已读明确命题 | 本轮对应材料及需要核对的内容 | 不应追加的更强要求 |
| --- | --- | --- |
| [WWC Device 文档绝对口径与真实部署差异](../astra-baseline/WINWINCODE_ANALYSIS.md:88)：长期 Credential/Provider 唯属 Control Plane 的文档表述，与实际 Device 生产来源有说明口径差异。 | Device 部署来源有原规则及本轮上下文修复；目前新增模型没有文档声明比较器。最终应检查是否自动呈现具体文档语句、对应 Device 来源及两者口径区别。只有文档 heading 或代码分流来源不能替代这一明确比较。 | 不要求完整规范语言、所有架构文档一致性或全部 credential 路径安全审计。 |
| [CPB 有限架构职责解释](../astra-baseline/CODEPATCHBAY_ANALYSIS.md:30)：CLI 提交与投影、orchestrator 的 assignment/attempt、worker/bridge 的消息和进程边界、引擎的注入端口及 service 的具体实现分工。 | CPB 正式 `/architecture/meaning` 仍限定目录组成与已认证引用；新增 `/functional_chains/0/pattern/responsibility_interpretation` 表达所选 callable 写字段/传参数，`/architecture/captured_writer_references/0` 提供实际 event/job/queue 写者引用。来源证据更丰富，但尚未生成原职责表中上述跨层具体解释。这里缺的是有限报告解释，不是全局所有权证明。 | 不要求证明整个仓库唯一事实 owner、全部写者集合、全堆资源等价或所有修改都已授权。 |
| [WWC 有限职责与身份解释](../astra-baseline/WINWINCODE_ANALYSIS.md:30)：Client 表现与协议、Control Plane/Delivery 产品状态、Worker 执行事实、adapter/Kernel 接线，以及几类身份不能混成同一个 session。 | 既有主链、新消息字段来源与资源写者条目需要合并查看；正式报告若已展示这些有限分工和身份区别，就应记为承接，不能因 ownership 的强边界仍为 false 再判未完成。 | 不要求 canonical authority 的形式证明、全系统授权或全部消息协议闭合。 |

## 第二类：新增模型承接的有限段落及原报告相同的限制

十三条映射表分别对应原文实际读过的 readiness、completion、access audit、事件/索引、可信命令、失败记录、WorkRun、Chat、所选 Worker/adapter、outbox/ack、浏览器生命周期与职责来源。正式状态应依据真实保存条目填写；若相应有限源关系支持，应直接承认该段的承接，而不是因为未证明更强命题继续称它未完成。

- 原报告对事件、audit、finalizer、outbox 描述的是源码中的边界、顺序、记录和恢复来源，未声称做过物理提交或故障演练。自动结果保留同一限制与原文相符，不构成新的差距。
- 原报告对 WorkRun 描述的是所选 runnable/dependency/active 检查，并未穷举完整领域状态机。有限 iterator/enum 关系可承接这段话；全状态机、所有 attempt 或调度性质为 false 不自动否定该段承接。
- 原报告对 typed dispatch、Chat、adapter 与协议的结论也有具体来源和范围。原 WWC-02 的指定命令链以及新增消息字段来源应按实际段落核对；不能追加“全部 HTTP/WS/ExecutionPort 都证明”作为支持条件。
- 原报告的架构职责是有限解释。`ownership_assessment=partial_captured_writers_and_consumers` 表示新模型没有全局所有权证明；如果实际 writer/interface 来源已经支持原句中的具体分工，原句可以被承接，不必消除所有 ownership false 标志。

`scoped_source_relations_supported`、partial ownership 和模型边界可以同时成立。该状态不是新的缺陷结论，也不能换算为整份报告或全项目功能覆盖率。

## 第三类：原作者明确未审与更强命题边界；不列入本轮剩余验收目标

CPB 原报告仍未逐分支审核所有 CLI、workflow、HTTP/OIDC、备份/发布 provider、本地代码索引算法、外部 adapter、平台部署或全部异常恢复交错；见 [覆盖账本](../astra-baseline/CODEPATCHBAY_ANALYSIS.md:16)。WWC 原报告仍未穷举所有 HTTP/WS、领域状态机/并发、credential 路径、vendored Kernel、所有 publication/audit/export/connector 副作用和平台/迁移；见 [覆盖账本](../astra-baseline/WINWINCODE_ANALYSIS.md:16) 与 [外部交付边界](../astra-baseline/WINWINCODE_ANALYSIS.md:82)。

完整跨边界协议、全部入口/分支生命周期、唯一 canonical owner、所有写入授权、物理持久/发布成功、外部 ack 真实和全故障恢复，也不因为本轮模型保留 false 就变成原报告已完成、本轮必须补齐的目标。它们作为解释边界保留，不作为“永远未完成”的理由。无需增加目标执行、测试、构建或新的 Astra 审核。

测试、第三方、生成文件、语法未解析或配置排除范围仍按正式 `/coverage` 和 `/report_scope` 记录。解析文件比例、确定边比例、source facts 数、查询数、章节数和展示表行数均不作为功能完整率。此前局部 contract 的 uncertain 也不能通过删除标签来冒充能力进展。

## 正式数据完成后的更新方法

1. 只读取已完成写入的两库 `*-automatic-report.json`、integration、goal ledger、冻结身份及原基准对照产物；不打开数据库、不运行分析器。先核对冻结工具/策略/报告身份。
2. 根据 `scope-pointer-map.json` 的 rule_id 在正式 `functional_chains` 或 `source_relation_index.entries` 定位；保存实际数组 Pointer、Finding/Evidence ID、report SHA 和 snapshot。禁止直接沿用上一轮数组序号，未找到的条目明确列缺失。
3. 原样记录真实 assessment、必要 gaps、source-only 边界、partial ownership 及所有相关 false 字段；按上述三类区分原文有限差距与更强命题边界，不能以 false 自动生成新的验收缺口。十八条保留规则和十三条新增规则分别比较；两个同源规则不累计为额外功能覆盖。
4. 本轮是否保留五项具体判断，以正式 goal ledger 和各 judgment 身份为准。把“具体判断保留”“所选源关系支持”“原全文尚未承接”分别陈述，不互相替代。
5. 用正式 Pointer 替换本草稿的待核状态，再生成最终范围差距。只有实际数据允许时才写条目状态和真实计数；始终不填功能覆盖百分比，不增加 Astra 复审或批准环节。
