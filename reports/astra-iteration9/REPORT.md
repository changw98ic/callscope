# CallScope v0.11.0：字段连接关系与当前复制时点证明

日期：2026-10-13（Asia/Shanghai）。优先级：功能判断的正确性、可扩展性、性能。

本轮增加了自动生成的字段连接证据，以及一条可核对的局部复制证明。正式结果保留 v0.10.1 的 engine 来源结论，没有把 queue／agent 的四条 unknown 改成完整来源判断。原五项完整目标仍为 **0/5**；30 项必要义务仍为 **4 项限定支持、20 项 partial、6 项 unknown**。

系统只读取源码和保存的图／证据，不执行目标程序、测试、构建、安装或沙箱。验证方式是受信工具的正常静态扫描、保存源码查询、独立源码／产物审查和语法／链接核对。

## 新增的实际能力

`source_relations` 从已认证的 AST、词法声明和 CALLS 边自动生成以下关系：

- 所选实参对应的真实形参位置。
- 直接词法别名初始化，以及 body return 对当前绑定的读取。
- 对象构造中的 spread 与固定属性定义顺序。
- 普通 Set 尝试的目标、分支所属和有条件的源码先后顺序。
- 在明确源码前缀范围内扫描所选字段的显式写入。动态目标、未支持的控制／写入区域或预算不足使排除结论保持 unknown。

因此，queue 不再只有一个终点 unknown：证据可展示 `normalizedInput` 的构造、`metadata` 的条件替换、三个子属性写入，以及第四实参到 agent 形参的连接。Set 是否成功、setter／Proxy 的副作用和所选字段当前内容仍单独未知。

`local_copy_retention` 使用新的不可变 IR 记录 `CopyBoundaryObservation` 和 `CopyRetentionWitness`。它将观察绑定到实际 copy、复制后的目的快照、完整后缀定义和目的对象效果记录，不恢复受损的入口字段来源。

在 `agent-config.ts:489`，若 `maxRetries` 是该次合法复制中的可枚举自有数据字段，且构造正常完成，那么复制时的值／引用在新字面量终点保留：后续两个固定键 `agents`、`agent` 不覆盖它。这一证明起于当前复制时点；不证明字段存在、此前入口值未变、共享对象内容、Promise fulfilled 值或后续运输。

## 同条件的正式结果

两库目标 source hash 和 policy hash 均与 final v10 相同；策略文件与 v9／v10 逐字节相同，没有新增递归 child plainness、普通 Set 或 Promise 模型前提。

| 所选位置／路径 | 原来源判断 | 新增证据 |
| --- | --- | --- |
| engine `runJob` 实参 `:157` | `source_form_preserved_when_present`；selected/source-form complete | 实参与真实形参的结构关系；helper 的十一自有键及 `maxRetries` 缺键保留 |
| queue `:1580` 的两个分支 | 两条 unknown | 分支内 Set 尝试、构造及实参连接，分别保存 |
| agent 直接返回 `:487` | unknown | 当前词法绑定的 body-return 关系 |
| agent 构造返回 `:489` | unknown | 有序构造及条件性的当前 copy-time 保留证明 |

全部字段 finding 仍为 uncertain。engine 的 presence 仍 unknown，整个实参 shape 仍 open，结论止于 callee activation 之前。五条评估来自三个合同；queue 两条对应一个源码调用位置的不同分支。新生成的 41 条结构关系及一条局部 copy 支持描述输出范围，不是功能覆盖率或新的验收分母。

| 仓库 | 新快照 | 选入／解析／未解析 | 节点／边 |
| --- | --- | --- | --- |
| CodePatchBay | `731ae3b53582e86de4c9c786c224fc99aa45154099b7738ce8652be0f5a3f336` | 333／330／3 | 11,085／60,571 |
| WinWinCode | `2b298f494c99d0f0040f7a8b856421813066caa21d7d6d26d36bb573d41626be` | 471／465／6 | 32,407／171,983 |

两库均为 partial。图／解析／调用分类保持；原 26 项冻结观察保持 **10 reproduced、3 unknown、13 evidence_only**，36 项来源核对全部匹配。10 个配置的有限合同 finding 不是 10 个业务缺陷，也不能合计证明完整功能。

两库冷、暖扫描保持各自同一快照；暖扫描 `created=false`，全部请求语言复用官方 CocoIndex 1.0.25 缓存，全项目检测仍重算。这里的缓存单位是语言前端 bundle，不是每文件增量依赖图。

## 修补与防退化

独立复核发现并促成三处正确性修补：

1. 普通 Get 必须检查所选槽的 closed 状态及 projection／value barriers；getter-free 模型不能把损伤槽中保存的旧 ValueRef 恢复成当前来源。
2. 局部 copy 的终点证明检查真实复制后的快照，以及所有保存效果中是否有目的 allocation。未逃逸但已损伤的对象不能保留正项；后续未认证目的操作、同键覆盖、未知 spread／成员和预算不足都会阻断。
3. 未建模循环目标／控制区域不能支持“未见显式所选字段写入”的排除结论。

严格 helper capture 检查一度使 engine 开发观察退化。追查发现共享词法层把参数默认值 `env = process.env` 中的 RHS `process` 误当成可能声明。通用修补用已有模式解码器枚举真实 binder；未支持模式保持保守，没有按项目、函数或字段名放行。新版稳定源码查询及正式扫描恢复旧 engine 正项，未撤销 Get 损伤护栏。

开发观察不是正式见证；最终依据是本轮冻结身份生成的两库保存产物。未冻结的首次全字段观察仅用于查因，不证明查询时加载的实现等于之后测量的字节身份。

## 版本与证据

包版本 `0.11.0`，schema `2`，analyzer `static-multilang-11`，detector `call-rules-10-field-relations`。字段摘要 `finite-field-summaries-5-ir`，wrapper `static-field-contracts-4-ir`，IR `finite-immutable-semantic-ir-3`，词法层 `captured-lexical-bindings-3`，结构关系 `captured-field-source-relations-1`；field policy 仍为 v2。

工具身份：`38933589ba90c08a8769fafa720e9c7258d29f17303c37dfadbdf491c579de7c`。43 份核心源码按 [CORE_FREEZE.json](CORE_FREEZE.json) 的哈希归档在 [frozen-core-source](frozen-core-source)。本轮新增关系不改变旧 API 端点或完整目标定义。

交付核对完成：43 份 Python 核心源码可解析，工具 JS 语法检查通过；18 份 Markdown 的 328 个本地链接无缺失。七类正常查询返回 10 个有限 finding，21 次保存源码响应均绑定相应正式快照。两个目标仓库的原 commit 保持且工作区干净；未做浏览器、安装或任何测试验证。

- [正式字段评估](field-assessments.json)、[分开的结构／局部复制轴](field-relations.json)、[v10／v11 对比](FIELD_VERSION_COMPARISON.json)。
- [能力账本](capability-ledger.json)、[原五目标账本](goal-ledger.json)、[本轮目标进展](GOAL_PROGRESS.md)、[原验收合同](../astra-iteration4/GOAL_ACCEPTANCE.md)。
- [Astra 独立审查](INDEPENDENT_REVIEW.md)、[独立证据核验](INDEPENDENT_REVIEW_EVIDENCE.json)、[新复制／结构关系核验](INDEPENDENT_COPY_RELATION_REVIEW.json)、[旧关系比较](INDEPENDENT_RELATION_REVIEW.json)、[目标指针核验](INDEPENDENT_GOAL_REVIEW.json)。
- [CodePatchBay 扫描记录](codepatchbay-integration.json)、[WinWinCode 扫描记录](winwincode-integration.json)、[正常保存查询](saved-query-observations.json)、[交付核对](verification-summary.json)。

尚需解决的是完整参数运输、实际消费者与预算归属、跨语言事件连接、保护范围与并发交错的必要关系。普通 Set 和 async 同化的缺口继续明确保存，源码语法关系不会替它们授予运行语义。
