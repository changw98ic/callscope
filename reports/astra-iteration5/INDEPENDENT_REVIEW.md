# Astra 独立复核：第五轮共享语义与字段来源

**结论：v0.8 可以作为范围明确的阶段成果交付；原五项完整静态判断仍为 0／5 完成。** 共享环境与 completion 已被真实消费者采用，旧导航／端口／保护区证据没有因迁移丢失；新增字段分析保存了有价值的局部来源，但三条合同的五个路径 assessment 全部未知，没有贯通 CPB 重试参数链。本轮没有新增完整目标的已支持义务。

源码审读发现的问题已修复或保守降级，正式产物发现的错误复制标注也已改版重扫；当前没有剩余的已知交付阻断。这不是一般语言完备性或所有实现正确性的保证。审查范围见 [REVIEW_SCOPE.md](REVIEW_SCOPE.md)。原 26 项基准、五项人工判断及完整目标合同保持冻结。

本审查只读实现、两库原文及保存产物，只修改本目录审查文档。没有执行 CallScope 模块、目标程序、目标导入、构建、测试套件或浏览器。实现者正常运行受信静态分析器的保存源观察会与正式发布结果分开核对。

## 正式结果与证据身份

本结论只对应整体工具哈希 `900090668e899bc07134e5d2c9b73f338f29a4302924247f8aa4e1850bb4a47e`、`finite-field-summaries-2` 和以下最终快照。两库源码哈希与 v0.7 相同；配置哈希随新增合同和共享模型身份分别记录，没有把旧快照补写成新事实。

| 项目 | CodePatchBay | WinWinCode |
| --- | --- | --- |
| 最终快照 | `fb9efe4704d83310958712a8b35089f06511d733258c63777e1d93af25bf89e8` | `24997ddb7ac245abb12a7da4387b77d1f605b50e6719e8b131322cfe4f164f31` |
| 捕获／解析成功 | 333／330 | 471／465 |
| 未解析边界 | 3 份 Shell 不支持 | 6 份 Rust 解析失败 |
| 节点／边 | 11,085／60,571 | 32,407／171,983 |
| 已绑定内部调用 | 23,380 | 16,293 |
| 原 13 项观察 | 4 reproduced、2 unknown、7 evidence_only | 6 reproduced、1 unknown、6 evidence_only |

两库状态均为 partial。冷扫描创建新快照，热扫描得到同一 ID、`created=false`；热扫描复用全部配置语言的 CocoIndex 前端结果，检测仍为 `global_detection=full`。这证明本次真实输入上的发布／复用结果，不能扩写成增删改名、故障恢复或任意缓存失效已操作验证。

已独立核对 [CPB 正式摘要](codepatchbay-summary.json)、[WWC 正式摘要](winwincode-summary.json)、两份 integration 与 baseline-v8-and-v7。原 26 项仍为 **10 reproduced、3 unknown、13 evidence_only**；36 个来源检查全部匹配，比较结果没有变化。CLI 动态 `mod.run`、注入的 `ctx.appendEvent`、泛型字段 `self.codex.ensure_thread` 均保留实际调用位置的未知证据。WorkRun 两条绑定仍带 serde／Eq 受信接口模型前提，Worker 同一泛型 impl 绑定仍声明实例化、bounds、参数类型和完整编译器命名空间未验证。

正式 [字段 assessment](field-assessments.json) 保留三条合同和全部五个路径：

| 合同 | 实际位置／路径 | 结果与可保留的局部事实 |
| --- | --- | --- |
| engine options | `engine-runner.ts:157`，1 个路径 | unknown。真实 `:137` rest 排除、实际 buildServices 形参映射与返回 11 个 own keys 可记录；helper 外层没有 maxRetries 的局部形状成立，前置效果仍未知。 |
| queue → agent input | `hub-queue.ts:1580`，2 个分支路径 | 均 unknown。同一调用的两条抽象路径没有当作两个不同调用点，输入规范化和实际 helper 关系保留。 |
| agent metadata return | `agent-config.ts:487/489`，2 个返回路径 | 均 unknown。body 返回形式与 Promise fulfilled 值、子对象 alias／opaque 效果分开。 |

三条规则的 selected-shape、source-form 完成位及 reaching-value／运输／完整功能证明均为 false；全部选定路径已列入 assessment。75／35／16 个 source facts 是证据条数，不能作为通过项。独立从目标原字节核对了新字段证据的 225 个去重源码区间、5 份文件，文件及区间哈希无不匹配。

迁移后的正式 WWC 导航 finding `164b2c45a7872f13450a9e68` 仍为 uncertain：82 个 trace、8 个节点、4 条实际边；四个 Scope 键仅 possible，guaranteed 为空，缺少 delivery。已有 delivery seed 的独立反例保留该键。相同上下文的查询来源、null 传播、直接 await 和 async create 的 Promise rejection 保留；未写成同步调用必然 throw。端口有 6 个 segment 记录，其中 5 段有限装配、route_activation 未知；23 个事实、end-to-end=false 和原 10 个导航 gap 均保留。另核对 6 份原文件的 162 个去重导航／端口区间，哈希全部匹配。

正式 CPB atomicity finding `a954aafc9b11a2901626fc97` 仍为 uncertain：15 个节点、12 条边及原 3 个必要 gap 保留。目录 owner lock 的有限 acquire→fresh read→callback→save→release 尝试，与两个只覆盖 acquire/release callback 的 process fence 分开；正常值转发和 catch/release 限制保留。外层非终态与内层 pending 谓词差异仍只是受信模型内的来源事实，实际 deps 装配、集合 heap 身份和外部锁协议未闭合，没有推导交错或证明运行中会重复。

总计 8 个配置式有限 finding，包括原 5 个及本轮 3 个字段 assessment；它们不是 8 个业务缺陷，也不替代原 26 项观察或五项完整目标。

[保存证据查询记录](saved-query-observations.json)包含 CPB 的四种与 WWC 的两种查询。已核对它们返回的 8 个有限 finding、rule／status 与上述最终 summary 一致，字段查询保留全部三项，来源读取绑定最终快照。此项只说明保存证据可正常查询，不代表浏览器交互或目标功能经过验证。

## 五项目标的独立验收

[目标账本](goal-ledger.json)保留原 5 项判断和 30 个必要义务，要求文本与冻结模板完全一致。已独立验证其 438 个递归证据引用的文件哈希、JSON pointer，以及关联 finding／rule／contract／snapshot 身份，未发现串版本或失效引用。账本明确是人工评审已保存自动证据，`automatic_obligation_solver_used=false`，没有伪装为自动业务裁决器。

| 完整判断 | 本轮实际支持 | 仍阻止完成的必要关系 |
| --- | --- | --- |
| CPB-01 重试参数与预算 | 原来源形式差异，加局部 rest／参数／helper 字段事实 | 五条字段路径仍未知；新旧队列、消息／记录身份、bridge 转交与有效预算消费者未闭合。 |
| CPB-02 superseded 终态分类 | 原初始化集合差异保持 | 状态生产和 job 身份、谓词／recover guard、权威终态保护及 terminal/recoverable 政策关系未闭合。 |
| CPB-03 同键去重 | 原有限保护区与谓词关系保持 | 实际 deps、物理／heap 资源对应、调度条件及自动交错推导未闭合。 |
| WWC-01 看板新任务上下文 | 原 URL 来源、null／拒绝链和有限端口装配保持 | 可见入口／route-event 激活、公开 VM 对象可变及其它 port／前缀效果仍有必要缺段。 |
| WWC-02 Device 规格字段 | 原封闭 spec 构造缺字段保持 | 生产 client 注入、命令／JSON／跨语言字段映射、真实 authority 和 Device guard 关系未闭合。 |

五项均为 partial；30 个义务仍是 **4 项在声明范围支持、19 项部分支持、7 项未知**，与 v0.7 的分类没有变化。CPB-01.P3/P4 增加了实际来源证据，但仍保持 partial。四项已支持的是 CPB-03.A4、WWC-01.N2/N3、WWC-02.D1，不能相加代替任何一个完整判断。

## 已完成的设计与接口审读

新字段规则以实际 owner／参数位置／field 和 sink 作为选择器，没有预填中间链、字段集合或消息运输结果。配置验证、分析组件身份、检测接入和服务约束计数已经接通；字段 finding 的最终类型约定为 `static_parameter_field_flow`，正式导出还需按实际产物复核。

共享环境协议区分源码 blocker、注册标准接口模型及外部宿主条件。共享 completion 区分普通调用值、Promise、iterator、直接 await、直接返回和正常结果的有限转发；它不认证调用激活、全路径完成、异常处理或资源寿命。

completion 候选冻结源码 SHA-256 为 `35dd3124f2bd6a33156d9e48a716172f11fff79ec90d1e0340166dc34510c77e`。已复核 finally／不支持默认 RHS／loop 等拒绝边界，唯一局部 await 赋值与 return 的有限来源，以及表达式箭头的精确隐式返回。两项审读问题已修正：返回嵌套 generator 不能使外层普通箭头被误判为 generator；同步函数的调用结果改称 arbitrary value，不排除返回 Promise。

nav、port、atomic 已实际迁移。薄 adapter 没有把共享成功结果升级为业务运行保证：异步 callback 和 Promise.all 仍需直接 await 及正常值关系；factory／VM 的未等待 async 返回、generator 返回体及公开可变对象边界继续保留。atomic 原独立资源／flag／谓词／release 门槛仍与共享层合取。

已独立核对一组固定候选的保存 v7 源观察：导航保留 82 事件、8 节点、4 边和原 10 个 gap；核对内容还包括实际四个 Scope possible keys、空 guaranteed 集合、已有 delivery 查询的反例、同 factory context 的 hash→query→params 来源及 callback null→直接 await→异步拒绝。端口 23 个事实、5 段有限装配及 end-to-end=false 保持。atomic 新旧 compact 除 finding ID 外完全一致，15 节点、12 边、3 个必要 gap 及不证明交错的边界保持。这是开发阶段保存源观察，未写回历史快照，也不代替正式 v0.8 结果。

该组环境候选为 `be115185a54c441170424565b2872ddef7abe0e406d8df5a1fa9b840030a03c8`，lexical 为 `c2820fd2d08be101bd8b51cc996fce69b0c2c2beffea94a1498b6b011fb75672`。随后真实字段来源观察发现三份文档使用 `Object.assign`，该已知标准成员尚未在共享接口登记，根代理授权窄增“允许出现”登记。已独立复核新环境哈希 `39e388c78584e176640109c869b3c3fe58819619e82bb29a570d9de1381d9566`：此修改不赋予 pure 或字段覆盖语义，requested semantic members 未扩大，API／prototype 作为实参仍逐项受原逃逸审计。31 处真实调用的保存源观察只证明标准接口出现登记，没有字段效果结果。atomic 与导航已按新依赖刷新，源码关系和必要 gap 均再次保持；导航最终开发观察哈希为 `7bec3b7f351e86da56099436cc260cd47d295b89ff25a2a581d8b9a49b652c4e`。旧候选与首次降级观察独立保存，没有冒充当前最终身份。

## 实现问题与闭环状态

1. **已修复 P1：宿主对象别名的可见写入可能漏审。** 初版只识别直接 `window`／`globalThis` 等根，别名经过 `??`、`||`、透明括号或宿主成员链后，后续显式 API 写入可能被误归入一般 opaque 宿主条件。修版以真实声明 ID 建立有限 may-host-alias 集合，跟踪其显式 API／computed／prototype 写和逃逸；未知存储拒绝。may-alias 不能认证实际 API receiver。保守过渡版曾使真实导航降级，保留在 INITIAL 观察中，没有删除护栏维持计数。
2. **已修复 P1：动态下标被当成静态属性名。** 初版 `_access` 将 subscript 中 identifier 的拼写作为键，可能遗漏 `globalThis[apiName]` 的动态写入，或把 `Object[freeze]()` 当成固定成员。修版只有静态点属性或已认证字符串字面下标可确定，其他下标保留未知。
3. **版本身份修正。** 已发布的 lexical 组件增加 rest binder 能力后不能继续沿用首次未发布时的版本理由；当前已递增为 `captured-lexical-bindings-2`。rest 只新增简单叶声明身份，不从中推导排除键或运行值。

字段内核首稿另有来源正确性问题，已经修复或保守降级：动态下标／undefined 遮蔽不能折叠为固定键或假值；rest 与 lazy call 实参保存当时状态，branch clone 不继续共享可变输入；嵌套参数成员写入不能仅落到临时读取值后丢失；复制来源的其它 getter、未闭合调用接触对象、默认 RHS 或不支持表达式的显式效果不能只记 gap 后继续宣布 sink shape 已闭合。构造时的 source form 可以保留为事实，使用点的完整性要另行降级。这些属于有限来源模型自身的正确性，不能以运行值尚未验证为由忽略。

第二次字段源码复核还发现：copy-time 快照与 live 对象保留同一逻辑 ID 时，按该 ID memo clone 会重新合并不同时间的状态；逐个复制实参会丢失同次调用别名；浅层 branch signature 会忽略嵌套变化；动态下标表达式、delete、模板或 callee 求值中的已见效果，以及容器／callback 参数逃逸仍可能漏审。最终候选按内存状态而非逻辑来源 ID 复制，保留同次实参别名，并把嵌套状态、效果与分支合流纳入判定。不支持效果使来源失效；不再将未知 callee 或 class 初始化视作无效果。wrapper 的 selected-shape 与 source-form 完成位已分开。

末轮还修复了两处构造过程的时间状态漏洞：后续 initializer／实参的效果必须影响尚未放入环境的先前临时值；分支比较也要包含这个状态。最终 `state` 比较加入 epoch flag，读取受影响 aggregate 的非 absent 子值会克隆并附真实 value gap，`origins` 遇 gap 只能产生未知来源。连续 `.child.key` 单段读取不能绕过这一降级。外层静态 own-key 的 presence／absence 与子值来源分开，所以不会因未知值抹掉已经证明的局部缺键。async body 的返回表达式与 Promise fulfilled 值亦分列。

另从实际开发产物发现并修复证据放大问题：哈希 `84f9457b…920fd114` 的字段内核只处理 engine 规则的 405 次操作、74 个 source facts 和一个选定 site，却输出 8,450 个 effect barriers；单 finding 的紧凑 JSON 约 41 MB，三规则开发产物约 67 MB。分支合流反复拼接共同 prefix 是重复证据来源，不是新分析覆盖。最终按稳定来源／上下文身份去重，完整 distinct 状态先参与判定，再按 24 项上限展示。实际最终开发产物为 2,060,447 字节，五个路径的 distinct effect 数分别为 8／13／12／11／13，均未截断。这修复的是证据可靠性和实际功能可用性，不能算成业务能力通过。

以上边界缺陷及修复结论来自源码推导，没有构造或执行边界用例。首轮冻结字段内核 SHA-256 为 `a170c39809d68888fc48e29430db83d5d16a397b31e36b8519c8e6ba4c41e29a`，wrapper 为 `99b2903b6530bb7c8558bd38b5812ca1606c28fe874764b89cce9a0f9ba6fb25`。该候选开发观察 SHA-256 为 `67c8b65091b7e015928f5ac10957a87f7985f71e3478711b1e8e33441c11ce11`；其六组件身份在当时独立核对一致。它只分析保存的 v7 源码，不是最终 v8 发布结果。

首轮正式 CPB 产物审查又定位并修复一个确定的事实标注错误：普通 `object_pattern` 无论有无 rest 都被写成 `source_copy_is_new_object=true`。实际 `engine-runner.ts:141` 与 `buildServices` 的参数解构没有创建 rest 副本。五个路径判定仍是 unknown，但这种错误不能作为新增来源事实交付。最终普通 pattern 只记录 `object_destructure_keys`，`copy_scope=none_at_pattern_level`；仅 `:137` 真实 rest 子节点记录浅复制、输入／输出、绑定身份和模型适用。已经发布过的字段内核递增为 `finite-field-summaries-2`，旧快照保留，不补写其证据。其余 source-fact 类别已经补读，未见第二处相同标注错误。

最终字段内核 SHA-256 为 `443edebc290a6a2fabc56c76d405f417af7c668ce17b22ce0201ab9fe5f3aec9`；最终开发观察 [FIELD_DEVELOPMENT_OBSERVATIONS.json](FIELD_DEVELOPMENT_OBSERVATIONS.json) 为 2,067,888 字节，SHA-256 为 `f42d38f0b8ad677f6f3b1d852cc6f8c756409cdc5da6f4b2610181f0f742946b`。独立核对六组件身份一致，三规则 source facts 分别为 75／35／16，五个路径仍全部未知。多出的事实来自把普通解构和实际 rest 复制分开，不是多完成一项业务判断。

最终整体工具身份为 `900090668e899bc07134e5d2c9b73f338f29a4302924247f8aa4e1850bb4a47e`。已逐文件读取并核对 [CORE_FREEZE.json](CORE_FREEZE.json) 的 40 个 Python 包源码哈希，没有未登记或变动文件。包版本为 0.8.0，分析器 `static-multilang-8`、检测器 `call-rules-7-field-summaries`、schema 2。首轮 `a59d…` 身份和两库旧快照记录在 [SUPERSEDED_SCANS.json](SUPERSEDED_SCANS.json)，旧数据库快照保留，最终报告不得混用这些被取代的结果。

## 本轮字段结论的必要范围

独立补读真实 CPB 源码确认：`jobOptions` 是 rest 构造，`services` 来自另一个返回对象，最终调用又构造新对象。`maxRetries: 3` 不能直接称为覆盖原 metadata 对象。`buildServices` 的封闭 own-key shape 可以与各字段初始化值、异常和前置效果分别分析；不能因任意值未知就抹掉 shape，也不能据 shape 闭合宣布所有效果已知。

`resolveAgentsForEntry` 有直接返回 metadata 和展开后返回两种形状。普通字段的源码形式可分别记录；其子字段被传给未闭合消费者时，复杂 alias 或外部效果仍会阻止实际 reaching origin 闭合。三条配置规则不能合并冒充 queue／scheduler／assignment／inbox／worker 的完整运输链。

最终开发观察的三条规则保留了全部五个路径 assessment，来源关系全部为 `unknown`，selected-shape 与 source-form 完成位均为 false。可以单独展示真实 rest 排除、实际调用实参到形参和 helper 的局部返回字段摘要，不能称为三段字段链已经贯通。这一结果比忽略已见效果后给出假阳性更可信，但尚未减少原业务判断的主要运输与消费缺口。

上述来源范围已经在正式双仓扫描、原 26 项比较、导航／端口／保护区迁移、新字段 assessment 和五目标／30 义务账本中核验；最终未知没有被开发阶段的局部正事实覆盖。

## 架构判断

共享环境和 completion 已被真实消费者使用，减少了重复守门，并保留来源、模型与运行条件的分界，这是本轮有价值的架构进展。但字段内核又建立了可变抽象对象、复制时点、别名、分支和效果合流机制；本轮多项审读缺陷集中在这层状态语义。后续扩展消息、状态或预算分析之前，应把不可变抽象状态／对象版本、copy 与 alias、effect join 的协议稳定下来，避免每类业务合同另写一个小解释器。

三条字段规则最多增加 CPB-01.P3/P4 的部分来源证据。没有闭合 queue 新旧分支、scheduler／assignment／inbox 对应身份、实际 bridge 激活和有效预算消费者，就仍不能完成该业务判断。共享重构和来源样本增加也不能抵消其他四项完整目标的必要缺段。

后续工作的优先级应当是：

1. **先固定状态语义，再扩关系种类。** 把声明身份、对象身份、对象版本和读取时点分开；对象复制与引用别名分别建模；分支合流要覆盖全部影响判定的状态。效果摘要要说明可能改变哪些对象／字段，不能长期在“所有效果都忽略”和“任何调用都污染所有字段”之间选择。可以先在字段内核收敛这份窄协议，不要求立即重写已经可用的导航分析。
2. **选一项完整义务闭环，而非继续增加局部样本。** 接近闭合的导航关系仍要补实际 route/event 到 VM 提交的关联、公开可变返回对象和前置 opaque 效果的必要边界；若继续 CPB 重试判断，则要明确选择 P3 的记录／消息身份或 P4/P5 的真正预算读取，不能把三段字段规则直接拼成完整链。
3. **让证据类型约束结论。** 构造事实、存在条件、own-key 形状、来源形式、正常履约值、实际 heap 身份和业务不变量应有不同字段与组合条件。此次普通解构标成复制说明，即使最终 finding 是 uncertain，内部事实也需要逐类检查；一个总的 uncertain 不能掩盖错误事实。

这些是后续功能正确与可扩展性工作的建议，尚未实现。拒绝分支的一般语言完备性、增删改名／崩溃恢复、浏览器交互和安装包构建没有在本审查中操作验证；也不声称两库的所有源码路径或所有运行行为已经覆盖。
