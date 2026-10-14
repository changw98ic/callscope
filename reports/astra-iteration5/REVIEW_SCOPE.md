# Astra 独立复核范围：第五轮共享语义与有限字段来源

本轮要把已经在真实源码上成立的有限语义提炼成可复用协议，并增加实际字段来源关系。共享代码数量、调用绑定数量或新 finding 数量都不是用户完整目标的替代指标。必须同时检查推导是否正确、现有证据是否退化，以及新增关系是否减少原五项判断的必要缺口。

目标源码仍为 CodePatchBay `4f2d2eca31d90b0122db1c1429dd365672db2393` 与 WinWinCode `da407e4f3df3719718b23bd8913b73fe3ff73857`。两库只读；不执行、导入、构建或测试目标，不运行测试套件。本审查只读核心、源码和保存产物，只修改本目录审查文档。根代理和实现者可以正常运行受信静态分析器读取保存源码，不能把这种分析操作称为目标运行验证。

## 1. 不变的对照与证据身份

[原 26 项基准](../astra-baseline/capability-baseline.json)、五项人工判断和[完整目标合同](../astra-iteration4/GOAL_ACCEPTANCE.md)保持冻结。v0.7 的实际对照如下：

| 对照 | 冻结事实 | 本轮必须保留的含义 |
| --- | --- | --- |
| 原 26 项 | 10 reproduced、3 unknown、13 evidence_only | 正向关系与必须未知分别核对；evidence_only 不因新增分析被删除，也不禁止新目标账本另行获得有限支持。 |
| WWC 导航 | 82 个 trace 事件、8 个实际节点、4 条已保存调用边；10 个 gap | 同一 callback 上下文的 hash→query→URLSearchParams→缺键→null→异步拒绝关系；已有 delivery 的 seed 是反证。 |
| WWC 端口装配 | 5 个有限装配段、23 个源码事实、6 个剩余 gap | 真实 boot/factory/port/VM 绑定成立不等于 route/event 激活、公开可变对象或其它方法效果已闭合。 |
| CPB 去重 | 15 个节点、12 条调用边；3 个必要 gap | 目录 owner lock 的有限保护区与两个独立 process fence 分开；集合身份、依赖装配和外部协议仍有限。未推导并发交错。 |
| 五项目标、30 项义务 | 全部五个完整判断仍 partial；仅 4 个子义务在声明范围获得支持 | 子义务的人工映射不是自动业务判断器；新结论须逐义务解释，而非使用上述计数计算“完整度”。 |

数量相同不能证明迁移正确；数量改变也不必然是退化。最终审查比较的是实际来源、绑定、条件、反证和 gap。每项变化要有源码或模型依据。

v0.7 工具源码身份为 `d0b2f76e6f8c398758e0d3ba2b8f0d583876de636062b758ac94e216afcbe49c`，详见 [CORE_FREEZE.json](../astra-iteration4/CORE_FREEZE.json)。正式本轮扫描应在全部核心冻结后以新版本发布；不能向旧快照补写新模型 finding。

## 2. 共享 API 的证据下限

共享模块应返回可组合的证据，而非一个含义模糊的 `safe=true`。至少区分：

- **源码关系**：实际声明、读取、调用、赋值、返回、位置和源哈希。
- **受信模型**：显式注册的接口／协议 ID、版本和适用边界。
- **政策要求**：待检查的 field、入口和业务义务。选择器不能替代绑定或预填结论。
- **未知与条件**：未闭合效果、运行环境、控制路径、预算或语言覆盖。

证据要能追溯到当前 snapshot、捕获文件及哈希、实际 UTF-8 原位置、parser／projection 身份、声明或调用身份。模型结果的 audit scope 与 completeness 要明确；旧快照源码、辅助输入和当前工具实现的身份不能混用。预算到达、不支持语法或来源错误须产生 unknown，不能以空列表伪装审计成功。先基于完整检查作决定，再对展示证据采样。

当前共享层可以复用已经审过的词法身份和纯 AST 帮助器。复制另一套不一致的作用域规则，或者仅把旧私有布尔函数改成公共名称，都不能解决可扩展性问题。消费者应实际调用新协议，同时保留其独有的来源与控制条件。

## 3. builtin-environment／effect 审计

`BuiltinEnvironment.audit` 成功只表示：在已说明的捕获范围内，没有发现会破坏这个**显式注册模型**的本地来源事实。它不能证明运行时 provider、对象、全局值或副作用已验证。

1. `unbound` 只说明已捕获词法作用域没有本地绑定，不能推出实际 `Object`、`String`、`Set`、`URLSearchParams` 就是标准实现。
2. 明确的 API／prototype 写入、computed 写入、delete、实际 API 值别名与逃逸、转义 binding、`eval`、`with` 和参数默认 RHS 不能被归入一般宿主假设后忽略。
3. 裸 `Window` 作为普通 opaque transport 的实参，不单独证明某个标准 API 被改写；可在显式固定标准宿主模型下继续。但这不等于该 opaque 调用没有效果。把 API 本身或其 prototype 传出与把宿主根对象传出需要不同证据。
4. 唯一声明身份不等于稳定值；可变绑定即使 identity 已知，重赋值或成员写入仍可能使模型失效。不同 alias 的相同文本不能合并，不同声明也不能仅凭不同 ID 证明对象不同。
5. 审计失败原因、实际 blockers 和外部假设分列。消费者可有更严格的 heap、callback、default 或 completion 前提，不能因公共审计通过而省掉。
6. 缓存至少区分文档／模型／作用域／实际使用位置与相关配置；一次调用的局部未遮蔽不能复用成整个文档的所有位置都安全。

迁移应核对旧 nav、port、atomic 的差异。统一收紧或放宽必须有明确模型理由和剩余风险，不能采用最宽松实现后只核对真实样本计数。

## 4. finite completion 摘要

允许的第一层是**源码正常履约关系**：某个实际调用若在限定路径正常履约，返回的值沿唯一声明／赋值／return 传回。这与“调用会发生”“所有路径结束”“异常被正确处理”“资源保持到 Promise settlement”不同。

`function_kind` 至少区分 ordinary sync、ordinary async、generator、async generator。普通同步函数可能返回任意值，包括 Promise；异步函数与 generator 分别有 Promise／iterator 的调用边界。generator 普通调用不激活其函数体；未 await 的 async factory 不能当成直接返回对象。普通 async `create` 中的 throw 对调用者体现为 Promise rejection，不能误写成同步调用立即抛出。

`completion_relation` 应分别表达 direct await、direct return value、return Promise、await assignment 后返回唯一值等受限形式。要求实际调用位置、owner、声明身份和正常值来源成立；只看到 `await`／`return` 祖先或文本顺序不够。

- `return operation()` 与 `await operation()` 在 catch、finally 和资源寿命上不同；后者也不保证整个外层函数正常结束。
- finally 可以替换返回、抛异常或改来源值，不能忽略。try/catch 可以保留有限正常履约关系，但异常／前置 abrupt 路径及其条件要明确，不能宣布全路径 completion。
- `value = await operation(); return value` 必须核对唯一实际写入及同一声明；`operation.member()` 不等于调用回调参数 `operation`，`return value.child` 也不等于返回 `value`。
- 形参默认表达式、嵌套函数、条件调用、提前 return／throw、generator yield、对象或 getter 效果不能被声明顺序掩盖。
- `completion_guaranteed=false`、异常路径未知和执行激活未知应与有限值关系并存，不能用一个 `closed` 字段覆盖全部问题。

CPB 原 fence 的 `value = await operation` 位于 try/catch，再返回 value。公共层可以记录该正常履约关系；atomic 消费者仍需另行认证其有限 catch/release 区域、资源与 callback 转发。公共层不应为适配这个样本而将任意 try/catch 当作已知安全，也不应一概拒绝 try 从而抹掉已有有限事实。

## 5. 通用有限字段摘要

首版可追踪被选择 field 的 presence 与来源，不必先构造完整对象模型。两者应分别表达，例如 presence 为 present／absent／maybe／unknown，origin 为实际表达式、实参字段、别名或未知；整个对象的 shape 是否 closed 是第三个问题。

### 必要规则

1. 未知形参对象的 field 不能默认为 present。可以表达“若输入包含此字段，则输出由它保留”的条件关系，而不是给该字段编造值。
2. object literal、const alias、rest 排除与顺序 spread 要以实际声明和完整 AST 为依据。spread/rest 的 own-enumerable data 语义、getter、Proxy、prototype 和副作用限制属于版本化模型；未知对象不自动满足普通 data object 前提。
3. 后方未知 spread 或 computed key 可能覆盖前方字段，应使该字段来源／presence 按语义降级。后方明确 data property 可以重新建立该字段的局部来源，但不能使整个对象闭合。
4. rest 排除键必须来自实际解构；字符串、转义、默认和 computed 属性不支持时明确未知。object rest 与参数 rest 不能混为同一规则。
5. 跨函数需要实际绑定、参数位置、formal binder、默认／rest 语义、return 分支与有限 completion。调用名字、policy 选中的 owner、同名 field 或两个文件里的相似对象结构不能作为运输证据。
6. 多个返回分支需要合流；普通返回、throw、fallthrough、Promise、generator 和未闭合效果不能默默过滤。源对象被写、别名逃逸、getter／opaque callee 可能改变字段时应保留 barrier。
7. 新语义关系放在证据中，不伪造 CALLS 边。选择器可指定起点、终点和关注字段，不能预填整条 chain、完整 key set 或 transport 成功。

### CPB 的真实验收方向

第一段关注 `runJobWithServices` 输入 opts，解构 rest `jobOptions`，服务构造与最终 `runJob` 实参的顺序 spread。`buildServices` 的返回若要作为“不会覆盖 maxRetries”的负证，需要真实封闭的 own-data shape 及返回／效果范围，不能只因 `rg` 未见字段名便宣布不存在。

另一段关注 queue normalization 与 `resolveAgentsForEntry` 的 metadata 保留或改写。应同时保留分支、复用、未知来源和返回形式，不能跳过 scheduler／assignment／inbox／broker 的未分析关系，将 CLI 值强接到 worker。

worker 中 `maxRetries: 3` 是另一次 opts 对象构造；除非实际 heap identity 与写入关系已证明，不应称为“覆盖同一 metadata 对象”。字段来源摘要可以减少相关子义务缺口，但不能独自证明实际预算被 engine 消费、全部运输断开或 CLI 功能失败。

## 6. 交付前核对

1. 共享模块被三个实际消费者调用，版本、tool source hash、政策与快照身份完整；没有将旧快照事实变更成当前语义结果。
2. v0.7 导航 query 来源、实际 null／Promise rejection、反证和必要 gap 保留；端口 generator／async factory、plain public object 与 event 边界保留。
3. atomic 的正常结果转发、同步谓词／for-of／Set 来源、catch/release 无 finally 约束及集合身份缺口保留；不能把两个 process fence 误当整个 mutation 的保护范围。
4. 新字段关系逐段携带实际来源／模型／条件，能定位停止原因；没有以 configuration 填充未闭合连接。
5. 正式双库冷／热静态扫描使用统一冻结核心。核对原 26 项、全部模型前提、五目标／30 义务与新的有限字段证据，分母分列。
6. 正式产物与开发阶段保存源观察分开。未操作验证的拒绝分支、故障恢复、源码变动、浏览器和运行行为在最终报告说明。

当前这份文件定义审查范围，不预先确认实现或正式结果通过。最终结论写入本目录 `INDEPENDENT_REVIEW.md`。
