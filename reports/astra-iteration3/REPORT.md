# CallScope v0.6：参数来源与词法绑定的第三轮迭代

本轮已完成两库正式冷／热静态扫描与全部冻结基准核对。10 项正向调用／路径首次全部重现，3 个指定未知保持；另自动复核了一项参数来源形式差异。两库仍为 partial，13 项高阶人工观察仍不自动裁决，不能将 10/10 写成功能覆盖率或项目功能通过。

新增能力是通用的调用参数来源形式合同，以及同一个泛型 Rust 固有 impl 内的有限直接自身绑定。优先级仍为功能正确和可扩展性，性能最后；不执行、导入、测试或构建目标，不提供沙箱或动态行为证明。

## 参数来源形式与显式条件

`value_contracts` 是独立的顶层数据配置。`call_argument_value` 使用文件、精确词法函数、调用表达式、参数下标和对象路径选择源码，抽取有限 symbolic expression 与唯一声明身份。支持字面量、引用、成员、调用形式及条件／逻辑表达式，区分 `||` 与 `??`。const 初始化来源不等于求出运行值。

[CPB 配置](codepatchbay-policy.json)分别选择 `run` 的 enqueue 第二实参 `metadata.maxRetries` 和 `main.processInbox` 的 runJobWithServices 第一实参 `maxRetries`。中间 queue、assignment、inbox 运输为单独的 `external_contract`；producer 存在时规则必须是 conditional。真实字段表达式与期望来源形式不同时仍保留动态 callee、传输与运行值等价性未知，不把它们连成普通 CALLS。

原来的两类初始化集合和返回对象字段合同保持，并与新合同在同一快照原子发布。字段同名、没有红色节点或空 findings 都不能用作整个项目功能通过的证据。

## 泛型同 impl 模型

Rust `rust-tree-sitter-1.7-generic-lexical` 只在同一个完整、唯一的固有 impl 内定位直接 self／Self 目标。字段分派、trait 目标、额外方法约束、Deref、cfg、未知宏与声明竞争继续保守。`generic_impl_binding` 保留同 impl 原文身份、参数形状、模型与未验证前提；不证明泛型实参、bounds、参数类型、编译器命名空间或执行成功。

基准核对器 1.3 保存这些有界前提并指向完整边证据，既有 serde helper／Eq 模型摘要保持。GraphSnapshot schema 仍为 2；原 [26 项基准](../astra-baseline/capability-baseline.json)和五项人工推导未改。

## 独立源码复查的纠正

- [参数证据](PARAMETER_EVIDENCE.md)：worker 的常量 3 是另一个对象的构造，不是已经证明对上游对象覆盖；queue 会规范化 metadata，也可能复用既有 pending entry，端到端来源仍需单独证明。
- [导航证据](NAVIGATION_EVIDENCE.md)：scopeHash 保留已有 query，问题来自这个新路由种子没有 delivery。已有 delivery URL、fake 端口及 Chat 创建是反证；不能泛化成所有创建失败。
- [原子边界证据](ATOMICITY_EVIDENCE.md)：process fence 和目录 owner lock 的持有范围不同。权威写路径确实有锁内再次查重，但谓词与外层选择不同；本轮未实现并发交错推导。

这三份新来源稿是人工独立观察，不能计入检测器自动结果。[参数机器观察](parameter-observations.json)的 11 项观察／31 个 AST 锚点也不是自动值流覆盖率。

## 正式结果与交付核对

| 保存项 | CodePatchBay | WinWinCode |
| --- | --- | --- |
| 提交 | `4f2d2eca31d90b0122db1c1429dd365672db2393` | `da407e4f3df3719718b23bd8913b73fe3ff73857` |
| v0.6 快照 | `3952ccb24bb530f5acf7096329ab085043c8e8bf8ee25f77e0ed623cb3be3ec5` | `66019560ade80433538040084e66645953cdf9825b71760b9f8ff0abcd777200` |
| 选入／完整解析／缺口代码文件 | 333 / 330 / 3 | 471 / 465 / 6 |
| 节点／记录边／确定内部调用 | 11,085 / 60,571 / 23,380 | 32,407 / 171,983 / 16,293 |
| 辅助原文 | 0 | 4 / 4；不计为新增已解析代码 |
| 图规则／旧静态合同／新值合同 | 10 / 1 / 1 | 10 / 1 / 0 |
| 冷／热结果 | 冷发布，热复用两语言，同 ID、`created=false` | 冷发布，热复用三配置语言，同 ID、`created=false`；Python 为 0 文件 bundle |

所有扫描使用实际官方 CocoIndex 1.0.25 语言 bundle memo 和 Axon 图核心，每轮全量重算检测。冷热稳定是上述固定输入的正常维护观察，不是逐文件语义增量、并发捕获或性能验收。剩余代码解析缺口仍为 CPB 3 个 Shell、WWC 6 个 Rust 文件。

正式工具身份 `79d3ec0c1eadc16578d7fc7c52a381ea80ea89dd6ff427d602ca5d0a49c6391e`，分析器 `static-multilang-6`、检测器 `call-rules-5-values`、schema `2`；基准核对器 `frozen-static-baseline-1.3`，自身源码 SHA256 `db09661e194ca132aed2bf6f4405d3d33ef9ad4157cf690a03f84fb4fe72b905`。原冻结基准 SHA256 仍为 `16b4b05c8818fa1eecf396132ebe2ea29a8f0068801165f0649da379d9041dd7`。

全部 26 项保持：**10 reproduced、3 unknown、13 evidence_only**。正向观察历程为 **5 → 7 → 9 → 10**。本轮唯一状态变化是 `wwc.worker.control-to-dispatch-call`：`WorkerMain.accept_control` 在 `worker/src/lib.rs:764:16` 的 `self.accept_dispatch` 连接同一 impl 的固有目标，边 `rust-call:14eb734d0b2507bebd041dd4`。见[完整边模型见证](worker-generic-binding-witness.json)；它没有验证泛型实例、bounds、参数类型、编译器命名空间或展开宏。WWC resolved 增加 494 条，不等于 494 个功能补齐；精确冻结样本及独立复核的范围另行记录。

三条 intentional unknown 仍必须在原调用位置保留：CPB 的 `mod.run`、`ctx.appendEvent`，WWC 的 `self.codex.ensure_thread`。既有 WorkRun 两条 serde／Eq 模型关系及 Production.persist_run 关系不能因新增 generic 通路失去其原前提。

参数 finding `27afb5ced428b324cdbb8709` 为 `uncertain`：producer 在 `pipeline.ts:189` 的 enqueue 第二个实参（下标 1）中写入 `metadata.maxRetries: parsed.retries`（字段位于第 205 行），来源形式匹配；consumer 在 `managed-worker.ts:1797` 的第一个实参（下标 0）中写入 `maxRetries: 3`（字段位于第 1809 行），与配置的 `metadata.maxRetries` 来源形式不同。记录了 parsed 的初始化调用和 metadata 的 `assignment.metadata || {}` 来源；声明身份包含文件哈希与 AST scope/span。`callee_target_not_inferred`、`value_transport_not_inferred`、`value_equivalence_not_inferred` 均保留，`runtime_proof=false`、`transport_proof=false`。这是一项有限合同复核，未自动证明参数穿过所有中间步骤后被覆盖或所有重试失效。

本轮共保存 **3 条配置式有限发现**：原 CPB 初始化集合缺项 `open`、原 WWC Device 对象字段合同 `uncertain`、新增 CPB 参数来源形式 `uncertain`。它们与 26 项主基准并列，不能偷偷加入 reproduced 分子，也不能称为自动确诊三个完整业务故障。图规则的另外两个 10 项账本仍为图关系核对，不能代表这些合同或全项目功能覆盖。

正式产物：[CPB 扫描](codepatchbay-integration.json)、[WWC 扫描](winwincode-integration.json)、[CPB 汇总](codepatchbay-summary.json)、[WWC 汇总](winwincode-summary.json)、[CPB v0.6/v0.5 比较](codepatchbay-baseline-v6-and-v5.json)、[WWC v0.6/v0.5 比较](winwincode-baseline-v6-and-v5.json)、[机器账本](capability-ledger.json)、[三条有限发现证据](finite-contract-witnesses.json)、[Astra 独立复核](INDEPENDENT_REVIEW.md)。

## 修复与剩余能力

Astra 的源码复核发现并推动修复了 const alias 比较丢失声明身份、命名函数表达式及转义声明遮蔽、loop／with 环境、嵌套类字段调用混入外层 direct call 等问题。没有用当前 CPB 样本碰巧正确替代这些通用边界的修正。显式重复字段、访问器、晚出现的 spread／计算键、未知表达式和绑定、超出分析预算的部分都保留未知；展示采样不替代完整判读。

下一步要缩小的仍是对象／端口组合候选、参数和 URL 的真正生产者—消费者传递、协议消息身份以及锁／事务边界。NAVIGATION_EVIDENCE 与 ATOMICITY_EVIDENCE 给出更准确的下一步来源，尚未实现 URL query-key 抽象域、callback 注入图或并发交错求解。本轮有进展，仍未整体达到五项完整人工推导的自动分析能力。

31 份工具 Python 源码和界面 JavaScript做了静态语法核对；正式扫描及[正常保存查询](saved-query-observations.json)读取源码与保存数据，确认新发现可以通过原有查询接口读取，status 提供值合同能力与独立配置计数。两个目标工作区保持清洁，见[只读仓库状态](target-state-observations.json)；工具身份、版本及引用检查见[交付核对](verification-summary.json)。未运行目标代码／测试／构建、工具测试套件、浏览器或安装包验证。没有把冷热扫描叫作项目测试通过。

Astra 的[最终独立复核](INDEPENDENT_REVIEW.md)确认全部 26 项身份／期望未变，36 份原文件哈希、85 处基准引用及 42 处合同片段匹配，完整 Worker 模型见证与有界摘要一致。结论为可在明确静态模型边界内交付，无剩余已知 P0/P1 阻断；这不背书全部新增 494 条绑定或语言／程序语义完备性。
