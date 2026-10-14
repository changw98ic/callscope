# CPB 字段传递来源准备：两个有限片段

日期：2026-10-12。性质：独立只读来源整理，尚不是 v0.8 正式扫描或字段分析结果。

本稿选取原源码，用固定 Tree-sitter 语法读取器保存字节 hash、词法 owner、AST 区间和对象成员顺序。[机器来源包](field-source-observations.json)包含 12 份源码、20 项人工选择观察、60 个去重 AST 锚点；所选文件原语法树均未报告解析错误。语法解析不证明类型、运行或功能正确。本稿没有导入、执行、测试、构建目标，也没有导入或运行 CallScope 字段分析器；`automatic_field_flow_results=0`。

[原目标合同](../astra-iteration4/GOAL_ACCEPTANCE.md)的五项判断及30项必要义务保持原样。下文只指出可能帮助 CPB-01 的 P3/P4 的来源；不把人工锚点升为自动满足，不修改旧账本或原26项分类。

## 1. 先纠正源码角色名称

实际 bridge 导出为 `bridges/engine-bridge.ts:18` 的 `runJobWithServices`，通过 `:11` 的导入别名 `runJobWithServerServices` 在 `:19` 转交 `opts`。所选文件没有名为 `runManagedJob` 的导出。

队列规范化是 `server/services/hub/hub-queue.ts:1550` 的 `enqueue` 内部 `normalizedInput` 构造和后续赋值；没有独立的 `normalizeQueueEntryInput` 函数。这些名称不能被策略角色当成已解析的实际调用目标。

机器包的每个锚点保存原文件 SHA256、原始字节区间、1基行号/0基 UTF-8 字节列和 AST 词法 owner。`manual_seed_label` 仅说明人工选择目的，不能替代声明或调用绑定身份。较长原节点摘录有显式截断标记和完整节点文本 hash；摘录不是完整目标分析。

## 2. bridge → engine opts/rest → services → runJob

| 实际位置 | 可直接核对的源码形式 | 后续自动分析仍需完成什么 |
| --- | --- | --- |
| `bridges/engine-bridge.ts:11/18/19` | 静态导入别名，形参 `opts`，`return runJobWithServerServices(opts)` | 导入/导出与实际 CALLS 身份、实参→形参、async 正常返回关系；上游动态 bridge 加载另列 |
| `server/services/engine-runner.ts:130–138` | 从同一 `opts` 声明取出五个键，余项绑定为 `jobOptions` | 普通可枚举自有数据属性模型、rest 排除、别名/可见写入和未知 getter/proxy；声明身份已知不等于字段值已知 |
| `:140–148` | `await mkdir`、broker/direct 路径解析、缺 `projectRuntimeRoot` 时 throw | 只描述正常前缀到达条件；未知调用效果、失败和返回值不应被当作无副作用或必然完成 |
| `:155` | `services = buildServices(cpbRoot, {hubRoot,env,dataRoot,workerBrokerClient})` | 从实际调用绑定取得 helper，分析参数、所有 return、封闭 own-data shape、alias/escape/effect 和正常完成 |
| `:157–180` | `runJob` 实参对象先 `...jobOptions`，后显式属性，再 `...services`，最后显式 `providerServices` | 按原对象成员顺序逐字段求来源；未知 spread 不等于空对象，独立字段覆盖和整对象封闭不可混淆 |
| `core/engine/run-job.ts:65–75` | `ctxInput` record guard、类型 cast、`runJobInner(ctx)` | cast/guard 不是重试预算消费者；setter 效果、最终读取/比较与预算归属仍未总结 |

rest 的实际排除键是 `cpbRoot`、`project`、`sourcePath`、`hubRoot`、`workerBrokerClient`；其中 `sourcePath` 和 `hubRoot` 分别绑定到 `explicitSourcePath`、`explicitHubRoot`。这些键及别名从原 AST pattern 读取，不根据希望保留的字段反向拼出模型。

`buildServices` 的 `ports` 字面对象在 `:85–119` 实际包含11个外层键：`createJob`、`startPhase`、`completePhase`、`completeJob`、`failJob`、`blockJob`、`appendEvent`、`prepareTask`、`getPool`、`getArtifactIndex`、`providerServices`。机器包先记录全部外层键和成员形式，没有预填某预算键应缺失。所选外层字面对象没有 spread、computed key 或 accessor；`:121` 直接 `return ports`。`satisfies RunJobPorts` 是类型语法。

据此可提出一个**需要适用检查的局部分析任务**：在普通 own-data 对象模型及封闭返回/别名/可见效果/正常完成检查成立时，`services` 的外层键不会覆盖不在该键集合中的 `jobOptions` 字段。不能仅凭 `const ports` 或没有直接写 `ports` 就宣称返回对象永不改变。属性初始化调用、broker `.bind`、闭包效果、抛错和可注入依赖须分别建模；普通对象语义与未来 opaque 端口调用的实际执行也不同。

`createJobInput` 在 `:47–52` 另行排除 `executor`、展开 `rest`、写 `dataRoot`，供 createJob 端口使用。这是另一个对象构造，不能拿它替代 `runJob` 最终参数或有效预算读取。

## 3. enqueue normalization → agent helper → new/existing queue

| 实际位置 | 可直接核对的源码形式 | 后续自动分析仍需完成什么 |
| --- | --- | --- |
| `hub-queue.ts:1554–1569` | `rawMeta`/`meta` 是单独边界字段投影；`normalizedInput` 以 `...input` 起始，再覆盖几个边界键 | 不把独立投影中没有预算键误报为 metadata 丢失；浅拷贝与 metadata 引用别名须分开 |
| `:1570–1575` | 缺 metadata 时新建 `{}`；写 `acpProfile/uiLane/uiLaneReason`；UI profile guard 可 throw | 整 metadata 替换、metadata 子字段写入、truthiness 默认、早退及原对象别名效果分别记录 |
| `:1580–1581` | 第4个实参为 `normalizedInput.metadata`；await `resolveAgentsForEntry`，随后整体赋 `resolvedMeta as QueueMetadata` | 精确 callee/实参→形参/返回和正常 completion；cast 不复制或验证字段 |
| `agent-config.ts:471–492` | `metadataRecord = metadata`；一支 `return metadata`，另一支 `{...metadata, agents:..., agent:...}` | 保留两支对象身份与条件，再逐字段 join；前缀调用、子对象 alias/effect 和 helper 返回摘要不能省略 |
| `hub-queue.ts:1595–1621` | callback 中查 pending existing，命中直接返回；新 entry 的 metadata 读 `normalizedInput.metadata || {}`，push 后返回 | callback 实际激活、record 身份与持久结果；existing 不是本次请求 metadata 的无条件来源 |
| `:1454–1463` | `withQueueMutation` 先 await 可写检查，再 await `withQueueLock`，callback 被转交 | 转交语法与 actual activation、锁生命周期、保存成功及返回关系分别验收；不据此证明端到端运输或无竞态 |

在普通可枚举 own-data 模型下，`normalizedInput` 的浅对象展开可能让其 `metadata` 与 `input.metadata` 指向同一值；后续子字段写入可能影响调用方 metadata。`:1581` 的整属性替换与这些子字段写入不同。不能把全部操作说成一次深复制。

`resolveAgentsForEntry` 的正常返回存在保留依据：`:487` 直接返回传入 metadata；`:489–493` 先展开 metadata，再显式设置 `agents`、`agent`。这两支没有在返回字面语法中显式覆盖 `maxRetries`。但方法前缀读取 hub/project 配置、动态导入、调用 `mergeAgentConfig(..., metadataRecord.agents || null)` 等；对 aliased 子对象的跨 helper 效果、getters、异常和闭合条件必须独立分析。不能仅凭两个 return 形状证明实际全路径保留。

新 entry 与既有 pending entry 的分支必须保留。`:1597–1598` 可能返回较早记录；本次 producer 的 metadata 并非该支无条件来源。`:1600–1617` 新 entry 的 metadata 有局部来源表达式，却仍未证明 callback、commit、scheduler、assignment、inbox 和 worker 组成同一条消息/记录链。

## 4. 消费者与不同预算的反证

`cli/commands/pipeline.ts:189–225` 构造 enqueue 参数，metadata 的 `maxRetries` 源码形式为 `parsed.retries`（`:205`）。其动态导入路径依赖 `executorRoot`；本稿不重新证明 flags 的解析/返回或生产模块绑定。

`runtime/worker/managed-worker.ts:1784–1836` 在非 `finalizerOnly` 分支另建 `runJobWithServices` 参数对象，`:1809` 写 `maxRetries:3`。这是**独立的新对象构造**，不是已证明对上游 metadata 同一个对象进行覆盖。请求值也可能是3；cancel/lease/前置失败、finalizer-only 和动态 bridge 装配均是必要限制。

这些预算不能按字段名合并：

- `server/orchestrator/failure-router.ts:111–112/265` 使用 assignment attempt count 与 `MAX_RETRIES[failureKind]` 比较；`:277` 还把整个 assignment 交给 opaque supervisor。不能从局部常量表推出全程序没有 metadata 消费者。
- `core/engine/phase-retry.ts:369` 的 `phaseRetryTotalMax` 来自 deps 或环境配置，是 phase total budget。
- `core/engine/run-job-execute-dag.ts:998` 的局部 `maxRetries` 来自 `verificationInfrastructureRetryLimit`，是 verification infrastructure budget。
- `core/engine/run-job-ports.ts:83` 的 optional `maxRetries` 类型属性仅是声明，不证明读取、验证或有效值。

上述只作为真实消费者/不同预算/opaque 反证的来源准备，不是完整消费者审计。

## 5. 对冻结义务的贡献与仍缺段

| 原必要义务 | 两段未来分析可减少的缺段 | 仍不能跳过的必要分析 |
| --- | --- | --- |
| P3 中间字段 | enqueue 的局部 normalization/metadata replacement、helper 形参/return 的两支字段来源、new/existing 入口边界 | candidate、scheduler、assignment、持久记录/JSON、inbox、broker/direct、worker 的对应身份与传递；existing 分支不得冒充本次提交 |
| P4 消费选择 | worker 新对象的独立来源；engine rest 排除/顺序 spread；实际 helper 返回 ports 的 own-data shape | bridge 的实际上游装配/实参绑定、受条件控制的激活/正常 completion、最终预算读取/guard及适用阶段 |
| P1/P2/P5/P6 | 可提供相关入口、别名和反证锚点 | 不是参数解析返回、完整生产装配、有效预算决策或完整结论与反证的自动闭合 |

现场源码支持研究的是**若干局部字段保留关系**；不能因为重建对象就预设 pipeline 参数被破坏，也不能因为几段保留成立就宣布参数端到端已连接。完整判断仍按原合同逐必要关系验收。

正式字段分析至少需要：保存源码声明身份；按实际 call binding 求形参/返回；区分固定键、rest、按序 spread、别名与写入；为 helper 生成所有正常 return 的 own-data shape；把正常值关系、body activation、全部 completion、资源生命周期分别表达；来源缺失、opaque effect、失败和未建模运输保持可见 unknown。策略只能声明起点/终点/字段与业务不变量，不能预填中间 flow 结果。

## 6. 原源码身份

下表来自机器来源包的原始字节捕获；逐文件读取稳定，不承诺整个工作区是原子快照。正式扫描须重新绑定其保存来源及工具/模型身份。本稿不改两个目标库。

| 相对文件 | 原始字节 SHA256 |
| --- | --- |
| bridges/engine-bridge.ts | `b0647dd081f10fc07fb84117c925763859bfbf74b5544413104d2d15cce31076` |
| server/services/engine-runner.ts | `952b6a43e9d2e5a2040eae1c7c8ec5c000d26a12f1c44d395041434db48bd864` |
| server/services/hub/hub-queue.ts | `0bd13766a2a2fcd271c2ead8166fbbd6f782fde32f63954ccced88a4cb2de02c` |
| server/services/agent/agent-config.ts | `83a2eef775f1ff274054ee16fa749e195ae5a475f42abf520b2434e7ed6af484` |
| core/job/meta.ts | `2e40a285e1ea4c28af9fb7d949e026a3edd74c2471e726ff702f1aa2a9ac0319` |
| core/engine/run-job.ts | `ae4a6baf16e3ca09c360f14ff52c084b83fc99a7206280fe4f7092d3b720a3cf` |
| core/engine/run-job-ports.ts | `6e10fe21adafe7446a87e146e680e41c7133229be1fe932f3b35a8ec414129a1` |
| runtime/worker/managed-worker.ts | `75cdd41a20c71a7f0c7c500080ab7743417f932d35e4179a031b822831c633ca` |
| cli/commands/pipeline.ts | `3df3f333ec4668352efde20049494c4a85bdf13049c808cd9f89f2d82f30b4ed` |
| server/orchestrator/failure-router.ts | `8abe3a09afcf48aa46b9380f9955e6c9e3e0411c1b02a29a9d2b4f1d721ea1a9` |
| core/engine/phase-retry.ts | `9a5b5b06fb5e120f3708e3999e90a14e8bdf05334828e930a7f92eaa18d7083c` |
| core/engine/run-job-execute-dag.ts | `5fb852088e425a0e3bf1f1bd2db5b3682fe61f031f01b213fc9a0d08b908bd14` |
