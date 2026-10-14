# Astra 独立审查协议：第六轮不可变字段 IR 与局部预算证据

状态：设计与实现前审查。本文不预报 v0.9 的字段结果或完整目标达成。目标仍为纯静态分析；不执行、导入、构建或测试目标，不运行工具测试套件。审查只读核心／目标／保存产物，只修改本轮审查文档。

对照是 [v0.8 独立审查](../astra-iteration5/INDEPENDENT_REVIEW.md)及正式快照：CPB `fb9efe4704d83310958712a8b35089f06511d733258c63777e1d93af25bf89e8`，WWC `24997ddb7ac245abb12a7da4387b77d1f605b50e6719e8b131322cfe4f164f31`。原 26 项、五项人工判断和[五目标／30 义务合同](../astra-iteration4/GOAL_ACCEPTANCE.md)不修改。

## 1. 五个 unknown 的原因不能混为一类

从 v0.8 `field_summaries.py` 和正式 CPB 字段 evidence 可以分出三层原因。

| 层次 | 源码／产物依据 | 本轮应如何处理 |
| --- | --- | --- |
| 故意宽泛的效果失效 | `invalidate` 给整个 env 加 gap；每次 call 增加全局 epoch；任意已知 member write 也使所有 aggregate 失效 | 换成有依据的可达对象／字段影响范围，不能只是删除 gap。 |
| 可变抽象状态的实现负担 | `_Value` 同时保存来源、对象、当前值和可变 gap；clone／merge／临时参数 epoch 要协同维护复制时点与别名 | 以不可变值与独立 store 版本明确这些身份，替代旧算法，不能增加一个未使用的 IR 外壳。 |
| 真实未闭合语义 | queue 的 metadata 是浅层共享 referent；agent helper 把子对象传出、动态导入并有 async 返回同化；预算与消息运输未闭合 | 继续未知，除非有新增、可定位的来源与模型证据；IR 重构本身不消除这些缺口。 |

engine 的最终 `runJob` 实参在 `engine-runner.ts:157` 被 `buildServices`／`normalizeProviderServices` 等调用产生的广泛 barrier 和临时 epoch 降级。`jobOptions` 则早在 `:137` 作为新的 rest 对象创建。需要研究的是这些调用能否到达该**新父对象的顶层槽位**，而不是宣称调用无副作用。

queue 的 `:1580` 两个分支路径有实际 `normalizedInput.metadata` 及子字段写入；agent 的 `:487/489` 两条 body 返回还跨 Promise 边界。不能以 engine 的私有新对象隔离结论顺带认证它们。v0.8 的保守结果本身没有把未知误称缺陷；问题是精度有限以及维护这种状态语义的成本。

## 2. IR 的身份协议

最小数据层应区分以下概念，名称可由实现者选择，含义不可合并：

| 概念 | 含义 | 不允许的替代 |
| --- | --- | --- |
| Declaration／Binding ID | 捕获源码中的词法声明与使用关系 | 不证明对象身份、值稳定或与另一变量不 alias。 |
| Value／Origin ref | literal、引用、参数投影或某次读取／复制的来源观察 | 不代表目标对象永久不可变；相同文本不代表相同读取时点。 |
| Allocation ID | 在有限上下文里创建的新对象，或明确标为外部／未知的对象族 | 不以 Python `id()`、遍历顺序碰巧相同或不同变量名证明 heap 不相交。 |
| Object version | 某个 State 中该 allocation 的不可变属性状态 | 不同 branch 不能只靠自增计数生成碰撞的版本；相同 allocation 的写入须更新版本。 |
| State | 声明环境、allocation→当前版本、逃逸／外部可达集合、控制及效果信息 | 分支不能共享可变 dict/list/gaps。 |
| Copy observation | 实际 copy 节点、源对象／版本、复制面、目标 allocation／版本和当时值来源 | 不能把浅复制子对象冻结成 copy 时的深层版本。 |

建议协议形态是 `env: BindingID → ValueRef` 与 `store: AllocationID → ObjectVersion`。槽位里的对象引用指向 allocation；后续嵌套读取从**当前 State** 查这个 referent 的版本。复制时槽位捕获的 primitive／reference 来源可以不变，而同一 referent 的内部状态随后变化。这两件事必须能同时表达。

状态版本可以按规范化内容定址。任何影响判定的域都必须进入版本或被不可变 State 引用：presence、描述符／可枚举性、属性值、动态键范围、unknown 部分、可达性、条件和效果。证据展示样本不能参与或截断语义判定。

## 3. rest／spread 的准确边界

1. 普通解构只是读取／绑定字段；只有实际 rest 子节点创建新浅复制对象。延续 v0.8 最后修正，不能再次把普通 `object_pattern` 标为 copy。
2. copy 按目标语言实际求值顺序读取源面；后方 spread／显式属性对同名槽位的覆盖必须按序表达。未知 spread 不能当空对象；后方明确 data property 可以重新建立自己的槽位来源，但不使整对象自动闭合。
3. 输入模型应覆盖**本次 copy 源的整个相关可枚举自有数据属性表面**。只声明 maxRetries 为 data 属性不能排除其它 getter／Proxy 在遍历中的效果。该前提不递归保证所有 child 也是普通对象。
4. fresh allocation 与输入外部对象不同，但它复制的任意 child 可能与输入根、另一个字段或另一个参数 alias。`input.env` 与 `input.maxRetries` 不能因路径不同就判不相交。
5. copy 捕获的是某个值／引用观察。随后修改原输入的顶层属性，不应倒写目标 copy 的已捕获槽位；随后修改共享 child，却必须影响从任一父对象做的 child 深层读取。
6. 新对象的 own-key 形状、所选字段 presence、槽位来源、referent 状态和正常完成分别表达。属性初始化值未知不必抹掉整个字面对象静态 key set；但未知 getter、computed key 或可见效果不得被 shape 成功掩盖。

实现审查中追加了一个必要区分：普通解构／成员 `Get` 不等于 own-enumerable copy。即使复制面全为 data property，显式读取仍可能访问非枚举 getter 或原型属性。根代理已授权独立的 `ecmascript-own-data-read-v1` 与 field policy v2；每次实际 Get 保存 key、receiver/version、guard 和条件。该有限模型只覆盖已有根／新 data 对象，不递归认证 symbolic child；缺失时无 prototype/accessor/Proxy 效果是显式额外前提。普通 `Set` 不因此被认证，未支持的属性赋值可降级未知。

本轮 engine 可争取的有限正结论是：在注册普通 copy 表面模型、实际应用的 Get 模型和正常到达的范围内，若输入有该字段，则 `jobOptions` 的顶层槽位捕获相应的值／引用，最终 `runJob` 实参槽位来源于这个 copy observation。它不证明最初 `opts.maxRetries` 的运行值至今未变、值必定是数字，或所指对象内容未变。正式对照须分别列出新增 Get 前提、whole-copy 前提严化和 IR 精度变化，不能把更强环境条件独自造成的结果升级算成 IR 改善。

## 4. selective effect 的必要证明

替代全 env invalidation 的依据应是可达性，不能换成全局 pure 假设。

- 对 opaque call 至少考虑实际 receiver、实参、可调用值的闭包捕获、已逃逸对象和外部世界可达对象。传出函数可能传出其捕获的 fresh 对象或可变 binding cell，不能只看实参是否是 object literal。
- 未知输入对象和其成员要允许回指、环及跨字段 alias。外部可达部分可能被调用或 await 期间的重入改变。普通属性读取也可能跨 getter／Proxy／转换边界，除非适用模型确实覆盖。
- **未暴露的新父对象**可以不被不相关 opaque call 改写，但要有出处说明它尚未作为 receiver／实参／闭包捕获／成员／返回值逃逸。外部 child 无法凭空反向到达后来创建的新父对象；一旦实际写入形成反向边，这个隔离结论就不再成立。
- effect 应支持已知字段写、未知键写、referent 内容失效、binding 重赋值和逃逸等不同变化；未知 target／alias／可达性预算不能被当作空 effect set。未知范围应显式扩大或阻止相关结论。
- 不支持的 class 初始化、computed callee／index、`new`、update、delete、模板插值、默认 RHS、`eval`／`with`、closure 激活等仍必须记其效果边界。实现能力不足不能归入“标准宿主稳定”后静默跳过。
- 标准接口“允许出现”不提供效果摘要。特别是现有 `Object.assign` 登记不是 pure 或 copy 语义证明；如本轮要解释它，须另有实际 receiver／参数及属性操作模型。

效果证据需要保存来源节点、实际影响根、通过哪些关系传播、未影响 fresh 对象的依据、未知 closure／外部范围和模型条件。仅减少 gap 数量不构成精度改进的证明。

## 5. 分支、求值时点与 completion

不可变 IR 必须真正替代 v0.8 `_clone`／`state`／`merge`／可变 `gaps` 的判定职责。AST adapter 可以保留文档／CST句柄表，但语义 State 不应藏有可变 Frame／AST／任意 Python 对象。

分支从同一不可变输入状态分出，合流按字段及版本表达所有可能结果。absence 与 unknown 不相同；presence 的保证取各可达分支共同部分，possible 来源需保留全部分支。别名不能在逐个复制实参时丢失；同一对象的不同历史版本也不能按 allocation ID 被重新合并成一个快照。

左到右求值需要保留：callee／receiver、实参顺序，对象键和值、spread、短路和条件分支。前方已求值的 primitive 值不会被后方调用改掉；前方对象 reference 指向的 referent 则可能变化。尚未放入 env 的临时构造同样需要记录。这正是 v0.8 epoch 曾保护的义务，不能随旧字段删除而遗漏。

异常、正常前缀、函数体 return、Promise fulfilled 值、generator 激活和资源寿命继续独立。局部字段摘要可以停在调用实参求值完成、callee 激活之前，不必因此证明被调用者正常完成。对返回值或跨 await 的摘要，必须按共享 completion 限定；一般同步调用也可能返回 thenable。普通 async helper 的 body 返回不能直接作为 fulfilled 对象。

## 6. 证据与版本要求

每个可组合事实至少保留 snapshot／原文件 hash／原 UTF-8 位置／声明或调用身份、IR／提取器／模型版本和必要条件。四类来源分列：source-derived、trusted-model、policy-declared、unresolved。策略只选择起终点、关注字段或不变量，不能预填中间对象版本、可达性、保留结论或预算关系。

IR 不可变是分析器内部性质，不是目标程序运行性质。不能只加一个总 `uncertain` 便容忍错误的子事实；相反局部已证形状也不应被统一未知分数抹去。

历史 v0.8 快照不补写；新 IR 和字段组件身份须进入 tool／detector／snapshot 及 CocoIndex 失效键。旧 26 项、五目标／30 义务的原要求和分母保持不变。新目标账本只在实际必要关系闭合时升级，不按组件数、代码量或 source-fact 数升级。

## 7. 预算 guard／counter 的范围

本轮可以添加局部 source-backed 的计数读取、阈值来源、比较运算、分支动作及限制。必须从真实声明身份和 AST 派生，不能因字段都叫 maxRetries 就连接不同预算。

至少分开 failure-kind 阈值表、assignment attempts、phase retry 与 verification/DAG 预算。读取的 key、`||`／`??`／默认分支、数值转换、实际 guard 极性和 guard 后动作要逐项保留。不闭合 helper 或动态目标仍未知；不要求求出一次运行的具体数值。

局部发现某个阈值和 counter 没有使用 metadata，不等于全程序从未消费该参数；搜索不到字段引用不是负证。opaque supervisor、不同阶段、终态／跳过分支、请求值也可能为默认值等反证仍需列明。此类局部证据最多先为 CPB-01.P5 提供部分支持，不能自动完成整个重试接线判断。

## 8. 本轮验收门槛

1. 公共 IR 实际接管字段 State／copy／write／effect／join，旧可变语义不在 adapter 里另存一套；选择器、来源、模型及未知可追溯。
2. 用最终保存源码比较原五个路径。任何 unknown→更强结果都逐条解释是哪个必要关系新增闭合，保留 model／normal-prefix／referent／运输边界。engine 未闭合也应如实交付，不强求 positive。
3. 同时核对实际反证与原拒绝义务，尤其其它 copy 源 getter、浅层共享 child、closure 逃逸、后方实参效果、branch 合流、默认 RHS 和 thenable。只做源码／已保存真实来源分析，不运行合成测试。
4. 原导航／端口／atomic 有限结论和 gap 不因新公共模块被静默改变；原26仍完整比较，五目标／30义务另表。
5. 全部核心冻结后正常双仓冷／热扫描、保存来源查询与正式证据审查。代码仍需适当语法核对；不把这些静态操作称为目标功能测试通过。

最终结论另写本轮 `INDEPENDENT_REVIEW.md`。本协议提供证据下限，不要求本轮完成一般 heap 分析、完整 JavaScript、全仓消息运输、自动并发交错或任意业务正确性证明。
