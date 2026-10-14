# Astra 独立复核：第一轮静态能力迭代（v0.4）

结论：本轮在有限且可追溯的范围内取得了真实进展，可以交付为静态分析能力增量。冻结的 10 项正向调用／路径观察由 v0.3 重现 5 项增加到 7 项；3 项要求保留未知的动态边界全部仍在原调用位置保持未知。两库没有因此被证明功能通过，也没有自动检出此前人工推导的 5 项业务缺口。

本复核由独立审查代理完成：阅读实现源码、冻结基准、精简扫描与核对产物，并用标准库核对 JSON 观察 ID、源码证据状态和计数。我没有执行／导入／构建／测试目标仓库，也没有运行工具测试套件、浏览器或自行重跑分析器。根代理运行的是 CallScope 的正常静态扫描与缓存维护，读取的目标源码没有被当作程序执行。此区别不应被写成“未运行任何程序”，也不应写成“测试已通过”。

冻结基准仍为 [capability-baseline.json](../astra-baseline/capability-baseline.json)，`status=final`、26 项、SHA256 `16b4b05c8818fa1eecf396132ebe2ea29a8f0068801165f0649da379d9041dd7`。两份完整源码报告未按本轮工具结果改写业务判断。这里记录新增能力及其限制，不覆盖后续 v0.5 的声明模型或合同检测。

| 保存身份 | CodePatchBay | WinWinCode |
| --- | --- | --- |
| 目标 commit | `4f2d2eca31d90b0122db1c1429dd365672db2393` | `da407e4f3df3719718b23bd8913b73fe3ff73857` |
| v0.4 snapshot | `ed28aa79a44fd5d4941fb3bd62f603f54460ed5306beb3b676ce7b1cd8205a40` | `d966bf9036469ae288a29176db9fb89ba97050e0ae61b745d2412d51ac96f5f8` |
| 选入／解析成功／缺口文件 | 333 / 330 / 3 | 471 / 465 / 6 |
| 剩余文件缺口 | 3 个不支持的 Shell 文件 | 6 个 Rust 解析失败文件 |
| 节点／边／resolved 边 | 11,085 / 60,571 / 23,380 | 32,407 / 171,983 / 15,784 |
| 快照完整性状态 | `partial` | `partial` |
| 冷扫描 | Python、TypeScript 重算；新快照发布 | Python、Rust、TypeScript 重算；新快照发布 |
| 热扫描 | 两语言复用，同 ID，`created=false` | 三配置语言复用，同 ID，`created=false`；Python 是 0 文件 bundle |

保存的工具源码指纹为 `5f267f6d0a36c24f468d15a1ffb96117bf2af32a4a8c6617c432ef3a59e3ea52`；分析器 `static-multilang-4`，检测器 `call-rules-3-axon`，schema `1`。基准核对器是 `frozen-static-baseline-1.1`，自身实现指纹 `25f3c887097ef867a5ad9ae0f3c60af8a73c2748744f0e90211db69f72206999`，与保存图的工具身份分开记录。

依据为 [CPB integration](codepatchbay-integration.json)、[WWC integration](winwincode-integration.json)、两份 `*-summary.json` 和两份 `*-baseline-v4-and-v3.json`。未加载巨大完整导出或数据库。本次冷／热结果能证明这两个固定输入的正常扫描、发布和缓存复用，不能替代增删改名、崩溃恢复、并发修改源码、打包安装或浏览器验证。

9 个原有 TS/JS 解析缺口全部恢复：CPB 328 个 TS/JS 文件全部解析成功，WWC 120 个全部解析成功。已读实现仅在有语法依据的类型 import、类型属性及 literal NUL 区间生成派生 CST 文本；原始内容与哈希保留，UTF-8 字节宽度及换行位置保持不变。原始错误、派生区间、派生哈希和适配版本单列保存。派生文本不被执行，也不成为业务 literal 值的来源。未识别错误仍保留缺口，不能依据这 9 个文件外推所有 TS/TSX 语法组合均支持。

Rust 的确定绑定范围是非泛型具体 Self 到唯一固有方法，保留 trait 默认方法、引用接收器、Deref／别名、借用形式、宏、cfg、重复声明与不完整来源的保守边界。WWC 的 resolved 总数从 v0.3 的 16,357 降为 15,784；这一变化包含更严格边界带来的降级，不能宣传为总绑定率增长。resolved 边占比也不是召回率或功能覆盖率。

新增的两项正向证据为：

| 观察 | 原始调用位置 | 保存的确定目标与边 |
| --- | --- | --- |
| `wwc.client.diagnostic-scope-call` | `apps/client/src/application.ts:359:23`，`resolveScopeContext` | `packages/browser-core/src/scope-context.ts#resolveScopeContext`；`8504a40e391f017281b97963` |
| `wwc.codex.submit-turn-persist-call` | `crates/winwincode-codex/src/adapter.rs:3558:8`，`self.persist_run` | 同文件 `ProductionCodexAdapter.persist_run`；`rust-call:909b1ee6f81aa6c96bcea53f` |

前者的调用者先前因整个 application 文件的类型语法缺口不可用；本轮恢复解析后绑定到原导入。后者的调用者词法身份仍是 `<ProductionCodexAdapter as CodexCoreAdapter>.submit_turn`，接收器 Self 是具体类型；核对器只作有依据的 trait impl selector 投影，没有按全局方法名猜目标。两项 source/target 都唯一，调用位置落在冻结 quote 内，原文件 SHA256 与基准一致。不能据 `persist_run` 这条边推出持久化成功、之后 Kernel 必然执行或整个提交事务完成。

完整 26 项账本如下。`unknown（保留）` 表示该项本来要求在真实调用位置保留未知且已满足；普通 `unknown` 表示正向关系仍未重现。`evidence_only` 不算自动分析通过。

| 冻结观察 ID | v0.3 | v0.4 |
| --- | --- | --- |
| `cpb.engine.checklist-materialization-call` | reproduced | reproduced |
| `cpb.engine.service-to-run-call` | reproduced | reproduced |
| `cpb.engine.service-to-dag-path` | reproduced | reproduced |
| `cpb.probe.trusted-policy-call` | reproduced | reproduced |
| `cpb.cli.dynamic-command-boundary` | unknown（保留） | unknown（保留） |
| `cpb.engine.injected-append-boundary` | unknown（保留） | unknown（保留） |
| `cpb.engine.production-port-composition` | evidence_only | evidence_only |
| `cpb.fix.readiness-before-enqueue` | evidence_only | evidence_only |
| `cpb.dispatch.queue-inbox-process-chain` | evidence_only | evidence_only |
| `cpb.finalization.completed-is-not-published` | evidence_only | evidence_only |
| `cpb.gap.pipeline-retry-budget-disconnected` | evidence_only | evidence_only |
| `cpb.gap.superseded-terminal-disagreement` | evidence_only | evidence_only |
| `cpb.gap.active-key-dedupe-window` | evidence_only | evidence_only |
| `wwc.client.diagnostic-scope-call` | unknown | reproduced |
| `wwc.scope.surface-hash-call` | reproduced | reproduced |
| `wwc.delivery.start-next-to-item` | unknown | unknown |
| `wwc.delivery.start-item-validation` | unknown | unknown |
| `wwc.codex.submit-turn-persist-call` | unknown | reproduced |
| `wwc.worker.control-to-dispatch-call` | unknown | unknown |
| `wwc.worker.generic-codex-boundary` | unknown（保留） | unknown（保留） |
| `wwc.client.auth-factory-composition` | evidence_only | evidence_only |
| `wwc.protocol.client-to-rust-dispatch` | source_missing | source_missing |
| `wwc.codex.intent-before-kernel` | evidence_only | evidence_only |
| `wwc.device.production-provider-composition` | evidence_only | evidence_only |
| `wwc.gap.dashboard-new-task-context` | evidence_only | evidence_only |
| `wwc.gap.device-clarification-verification` | evidence_only | evidence_only |

汇总为 7 项 reproduced、6 项 unknown（其中 3 项是正确保留的未知）、12 项 evidence_only、1 项 source_missing，总数仍为 26。CPB 19 份基准源文件哈希匹配；WWC 16 份匹配，1 份 generated control-plane-client 源码未进入当时的保存快照。该 source_missing 仍占分母，没有以人工读过当前文件来替代保存证据。所有已核对 quote 无不匹配；缺失文件观察的 quote 未被标作匹配。

三条必须保留的未知均有真实调用者和原调用位置：`cli/cpb.ts:186 mod.run`、`core/engine/run-job.ts:127 ctx.appendEvent`、`worker/src/lib.rs:2744` 开始的 `self.codex.ensure_thread`。后者虽保留同名候选，仍无唯一 target；生产组合实例不是公开泛型定义所有上下文的唯一证明。两个 WorkRun 自身调用仍受 serde helper 的 opaque 边界影响；WorkerMain 的具体固有调用仍受泛型容器范围限制。它们是已知能力缺口，不能算仓库缺实现。

源码复核期间要求修复的确定性问题已经闭环：

- 基准核对器原先可能把损坏的 resolved／悬空目标边视为“正确未知”。现在仅真实调用位置的 dynamic/unresolved/ambiguous、空 target、明确原因可满足 intentional unknown；坏契约不能通过。缺 caller、哈希变化、来源缺失和 evidence_only 都保留原状态。
- Rust 引用／泛型 trait receiver、Deref 别名和接收器借用形式曾有遗漏的冲突来源。现保守降级，不选择猜测的 trait 目标。
- Rust trait 默认成员原先未完整进入冲突集合。现读取已捕获 trait 声明；来源不完整时关联到具体 receiver 或保留全局未知边界。正式仓库结果中 ProductionCodex 仍有足够上下文完成新增绑定，未沿用早期孤立文件分析的结论。

这些修复增加了静态结论的可信边界；源码审查和有限保存产物并不是一般语言语义完备性的证明。未运行目标验证，因此报告中的源码事实、条件风险和业务结果推断仍需严格分开。

下一轮应优先处理可表达、可核验的静态事实：把终态初始化集合差异和特定 producer 的字段构造做成通用配置式规则；合同来源、Device 适用条件和消费者反证必须随证据保存。即使工具复核了 `superseded` 缺项或 `verificationCommand` 缺字段，也不能把整项人工业务推导自动改成已证实运行故障。并发幂等窗口、端到端事务顺序、动态端口装配和跨进程协议仍需要独立能力，不能靠增加调用边替代。

本轮交付无剩余已确认的 P0/P1 阻断项。后续 v0.5 的 support inputs、可信 Rust helper／标准接口模型及静态合同检测必须获得新的输入、政策和工具身份；本结论不提前认可尚未完成的 v0.5 集成。
