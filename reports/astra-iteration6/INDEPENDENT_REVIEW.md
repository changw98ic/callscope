# Astra 独立审查：v0.9 不可变字段 IR 与局部预算证据

日期：2026-10-12。评审对象为本轮冻结实现及两库正式保存结果；核心和目标仓库均只读，原 26 项基准、五项人工判断和五目标／30 义务合同保持不变。

**本轮字段精度目标没有达成。** 不可变 IR 已实际接管字段分析，两个局部预算模式也有正式来源证据；但三个字段合同的五条评估路径仍全部 unknown，`buildServices` 的局部 own-shape／`maxRetries` 缺键摘要还比 v0.8 更保守。可以交付这一有明确边界的静态分析版本，不能宣称已经复现五项完整业务判断，也不能用 874 条字段事实或组件数量替代功能进展。

在本次只读审查范围内，已发现的错误确定性问题均已修正或降级未知，没有遗留阻止本次有限交付的确定缺陷。这个结论不是一般 JavaScript 语义完备性或分析器全面正确性的认证。

## 正式身份与扫描结果

独立核对 [CORE_FREEZE.json](CORE_FREEZE.json) 的 42 个 Python 源文件，全部与冻结 hash 一致。正式组件身份为 package `0.9.0`、analyzer `static-multilang-9`、detector `call-rules-8-field-ir-budgets`、schema `2`；整体工具 hash 为：

`35aedb73739399068219e6b9b46840c27441f5b1f74430031234ffb285c8b7fc`

| 仓库 | 正式快照 | 选入／解析／未解析文件 | 图节点／边 |
| --- | --- | --- | --- |
| CodePatchBay | `bc3350f010b470fb2bcf8e72e8e966bd432602ae07ec465666f797bb6a4ff1de` | 333／330／3 | 11,085／60,571 |
| WinWinCode | `640931a5622d449ab3aa8a141336e6b45818397c97cbcc35e4491645bc55eae7` | 471／465／6 | 32,407／171,983 |

两库均完成正式冷、暖扫描。暖扫描全部配置语言复用 CocoIndex 1.0.25 缓存，检测仍为全项目重算，发布同一 snapshot ID 且 `created=false`。WinWinCode 的 Python bundle 为零文件，不算 Python 生产源码覆盖。两库状态均为 `partial`；CPB 的三个未解析文件是选入的 Shell，WWC 是六个 Rust 文件，不能把这些覆盖缺口当作项目缺陷。

原项目源码 hash 与 v0.8 相同。字段策略升级为 v2，加入独立 Get 前提，整体工具身份也改变，因此这不是“同策略仅换 IR”的对照实验。正式来源见两库 [integration](codepatchbay-integration.json)／[integration](winwincode-integration.json)、[summary](codepatchbay-summary.json)／[summary](winwincode-summary.json)。

| 本轮核心组件 | 最终 SHA256 |
| --- | --- |
| `semantic_ir.py` | `1abb91c5a29f55d6988c2a568f2164132143a197cfa4e5e878bc6dffc065a999` |
| `field_summaries.py` | `e0f7c95cd6ec8e6f518dd006e48a7d5dd37b70e4484aac0cf60de80d98c8c744` |
| `field_analysis.py` | `974504fa066c3bf129a364e66b6a1cc2a33179ad1157142de3dfda95cc8f3317` |
| `budget_analysis.py` | `9d05d7045360cf25ea9960e5d9635e96abe3247ba9fa12a6045800105f251555` |

开发字段产物使用过 `2f72275…`，最终模块 cell 逃逸修正为 `e0f7c95…`；本报告采用最终正式重算结果，没有把旧开发观察冒充最终运行结果。

## 架构判断

这次迁移是真实接管。旧 `_Value`、`_Frame`、私有 clone／merge 和全局 epoch 判定已移除，AST adapter 通过公共 IR 的 allocation、binding、lookup、copy、write、effect、join 操作生成状态。不可变记录把以下概念分开：

- `ObjectRef` 标识 allocation，`ObjectVersion` 标识其当前状态，copy observation 保存复制时的源版本。
- 浅复制固定顶层 slot 的来源；slot 指向的 child 仍是共享 referent，后续读取不能冒充深复制。
- 声明身份与 activation cell 分开；闭包持有实际捕获 cell，逃逸和后续重绑继续传播。
- effect 只有在实参、捕获、外部和已逃逸根的边界有来源证明时才收窄；未知捕获、反射、模型或预算缺口仍扩大为 unknown。
- 模型证明保存在不可变 `State.guards`，来源、模型条件、策略声明和未知分别记录，不用伪造无效果调用保存证明。

这改善了扩展基础，却不自动带来有用精度。v0.8 的问题一部分来自可变状态／全局失效，另一部分来自真实的 alias、getter、opaque 调用、Promise 同化及运输缺口。换成不可变数据结构只能让这些关系更清楚，不能替代分析。

源码审查曾发现并已修正的重点包括：跨 activation 误取同声明绑定、把嵌套函数视为空捕获、遗漏尚未初始化的未来 cell、未知写入不登记 RHS 逃逸、模块 cell 仍沿旧 primitive 剪枝、成员 callee getter 与实参求值顺序错误、fallthrough 仍保完整位，以及用 copy 条件代替普通 Get／Set。最终实现对未支持的普通 Set 保持效果未知，没有为了得到正向结果加入全局 pure 假设。

## 字段结果：能力目标未完成

正式 [field-assessments.json](field-assessments.json) 保留全部五条路径，没有从分母删除 unknown。

| 合同 | 实际评估位置 | 正式结果 | 已保存 source facts |
| --- | --- | --- | --- |
| engine options | `engine-runner.ts:157`，向 `runJob` 构造参数 | 1 条 unknown | 208 |
| queue agent input | `hub-queue.ts:1580`，两个来源路径 | 2 条 unknown | 163 |
| agent metadata return | `agent-config.ts:487/489`，两个返回来源 | 2 条 unknown | 503 |

全部五条的 selected-field shape、source-form 完整位均未闭合，presence 与来源关系仍未知；运行值、运输和完整功能也没有被升级。每条仅显示最多 24 个 effect 样本，同时保留 distinct 总数和截断标记，不能把样本数当作完整效果数。

实际 engine 路径仍在 Get 的 receiver／version／合流来源处失去精度；helper 结果的未知又限制后续字段摘要。完整 adapter 中，services own-shape／`maxRetries` absent 也退为 unknown。组件观察确实能列出十一服务键、区分源对象变化与私有 rest 父对象，但那份观察没有解释完整 initializer、捕获、async 前缀和最终实参，不能补足正式结果。

本轮多出一个重要适用条件：`ecmascript-own-data-read-v1` 与 own-enumerable copy 模型独立注册。每个 Get 需要实际 receiver/version/key 的证据；字段存在时为普通 own data，缺失时不经 prototype、accessor 或 Proxy 产生效果。copy 则要求整个相关可枚举自有表面满足普通 data 条件，而非只有所选字段。两者都不递归认证 child，也不证明字段存在或数值稳定。这些是显式可信模型前提，不是从目标运行中验证出的事实；更强前提不能被记成 IR 精度收益。

## 预算结果：新增两种局部来源关系

正式 [budget-assessments.json](budget-assessments.json) 的两条发现均为 `uncertain`。

| 合同 | 自动来源支持 | 仍未证明 |
| --- | --- | --- |
| phase retry | `phase-retry.ts:396` 的 `>=`，实际嵌套 `prepareRecovery`，以及 `:530/575/619/663` 四次同声明计数写入 | 嵌套激活、数值、全路径支配、上游参数与预算归属；limit 外层调用仍有绑定缺口 |
| verification infrastructure | `run-job-execute-dag.ts:1004` 的 `<=`、初始化与一步更新，以及实际绑定的 limit helper 来源 | 实际迭代次数、终止、异常完成、所选限额与 CLI 参数等价 |

`source_form_complete=true` 仅表示所选有限局部模式的源码关系闭合。numeric bound、runtime consumption、termination、whole-function domination 和 whole-project-unconsumed 等位均为 false。四处 `+= 1` 不是四次实际尝试；带 `return` 的真分支也不能忽略前置 await 的异常／未完成。两条结果可以支持 CPB-01.P5 的局部评审，不足以自动复现原“重试选项未接入受管理执行预算”判断。

## 原能力保持与完整目标

原 [26 项账本](capability-ledger.json) 为 **10 reproduced、3 unknown、13 evidence_only**，对 v0.8 零状态变化；36 个来源检查全部匹配。三个刻意保留的动态边界没有被改成确定调用。它们与新配置式事实、五个字段路径、五项业务判断是不同分母。

对旧 atomic／navigation 的完整保存 JSON 做了逐字段比较：除了 snapshot、parse、版本、策略和派生事件身份，实际来源位置、谓词、域、guard、反证及缺口不变；重命名事件／context 的关系保持一致，而非仅比较数量。

- atomic 保留 15 个节点、12 条边、所选保护 region 和谓词来源，以及依赖装配、collection heap、外部保护协议三项必要缺口；仍没有交错推导。
- navigation 保留 82 个事件、8 个节点、4 条边、缺失 `delivery` 的 query 来源及已有 query 反证；port 的 23 条事实和五段有限装配保持，仍有十项缺口，`end_to_end_complete=false`。

独立核对新 [goal-ledger.json](goal-ledger.json) 的 611 条递归引用、104 个去重 JSON pointer：artifact hash、snapshot、finding、rule 和 contract hash 全部匹配。账本是人工评审正式自动证据的映射，`automatic_obligation_solver_used=false`。结论为：

- **0/5 完整目标达成**，五项均只获局部支持。
- 30 项必要义务中，4 项在声明范围内支持，20 项 partial，6 项 unknown。
- 只有预算决策 P5 从 unknown 增为 partial；P3／P4 没有因 IR 或事实数上升而被升格。

CPB 参数运输、终态生产与消费、实际 deps／heap／交错，WWC route／event／可变对象与跨语言命令运输，仍是必要分析缺口，不能改写成普通环境假设来宣告完成。

## 独立核验范围与交付优先级

本代理只读审查核心源码、目标源码和保存 JSON。针对本轮三个字段与两个预算发现，独立核对了 8 个实际文件的 756 个去重来源位置，其中 531 个带区间 hash；原文件 hash、区间范围和这些区间 hash 均匹配。832 个去重 typed EvidenceRef 没有串入旧快照。原基准及验收合同 hash 未改变。

交付记录也已核对：[verification-summary.json](verification-summary.json) 的最终工具身份与两份正式扫描一致，package／pyproject 均为 0.9.0，记录了 42 份 Python 源码语法读取、JavaScript 语法检查及无缺失的文档链接检查；具体文档／链接总数以该最终记录为准。[目标状态记录](target-state-observations.json) 中两个原始 commit 未变、工作区清洁。[七类型保存查询](saved-query-observations.json) 绑定上述最终快照；[预算正式来源复核](BUDGET_FORMAL_REVIEW.json) 的 3 文件／103 个去重区间及 4 条既有 helper CALLS 身份与正式结果一致。

最终 [IR 迁移对照](IR_MIGRATION_COMPARISON.json) 与[迁移结果说明](IR_MIGRATION_RESULT.md)也已核对：五处原始来源／分支匹配，仍是五条 unknown，services 缺键摘要退化；导航和 atomicity 的来源关系保留。机器对照 SHA256 为 `cdb528bc45b4f39923340eb7a0ca1726cd396693a36dd9c7a6e31fd175af130a`，输入 hash 全部匹配。派生 ID 引用标记修正后没有残余语义差异，该修正只涉及报告，不涉及核心或重新扫描。

两库正式静态扫描是受信工具的正常运行，不是目标功能测试。本代理未执行或导入目标，未构建目标、运行工具／目标测试套件或浏览器；本报告也不认证部署、语言编译、实际对象形态或运行结果。没有进行同一策略下的 IR 对照实验，也没有证明所选之外的任意 alias／effect 情况正确。

下一步优先顺序应当是：

1. **先修有实际证据的字段精度损失。** 沿 engine 的 receiver／version／join 与 helper 返回关系定位第一个失去证据的位置，恢复可证明的顶层 rest 来源及 services own-key 摘要；保留 getter、alias、completion 的必要未知，不能再靠增加全局假设换取 positive。
2. **然后连接同一原目标的必要关系。** 从已保存的字段与局部预算来源继续核对参数、实际消费者、guard 与计数归属。若运输／装配未闭合，就继续保留完整判断未达成。
3. **维持公共协议和版本审计。** 新分析应复用已实现的 IR、词法身份、效果与完成态接口。不要继续用新增组件、规则数或 source-fact 数量作为功能完成度；本轮也没有证据支持优先投入性能优化。

因此，本轮可交付的是可追溯的语义基础重构、保留的旧有限关系和两项新增局部预算证据。用户要求的完整自动分析目标仍未完成。
