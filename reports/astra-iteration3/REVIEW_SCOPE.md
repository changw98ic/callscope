# Astra 独立复核范围：第三轮静态能力迭代

本轮目标是让 CallScope 对参数来源、默认与覆盖、导航上下文及操作边界给出可复核的有限事实。优先级是功能正确和可扩展性；不以 resolved 边数或发现数增长作为目标。两个目标仓库保持只读，不运行、导入、构建或测试目标，不运行测试套件。

源码基线保持 CodePatchBay `4f2d2eca31d90b0122db1c1429dd365672db2393` 与 WinWinCode `da407e4f3df3719718b23bd8913b73fe3ff73857`。[原 26 项基准](../astra-baseline/capability-baseline.json)及五项人工业务推导继续冻结。新增自动事实另列；不得把原 `evidence_only` 改成自动发现的完整业务缺陷。

本文件记录实现前的独立判断与验收边界。最后应以本轮保存的实现身份、配置、快照和见证填写 `INDEPENDENT_REVIEW.md`，不能把以下设计要求当成已经实现或通过。

## 1. 三个观察的可自动事实

| 观察 | 可先自动核对的有限事实 | 不能由这些事实直接推出 |
| --- | --- | --- |
| CPB pipeline retries | 提交对象 `metadata.maxRetries` 的表达式为 `parsed.retries`；指定 worker 调用参数的 `maxRetries` 是字面量 `3`；解析器对输入使用 `parseInt(...) || 3`。 | 参数已经完整传递至 worker 后被覆盖；所有重试决策都不消费输入；任意用户输入都会改变失败行为。 |
| WWC 新任务导航 | 指定链接以不含 query 的 `/home/new-task` 构造新 hash；范围 helper 只写四个 Scope key；生产闭包从当前 hash 读 `delivery`，空值分支返回 null；真实 task port 对 null 抛错。 | 所有新任务入口失效；用户提交时 URL 必定未修改；fake/Chat 路径同样失败；已有任意调用路径即证明整条生产链的条件同时满足。 |
| CPB 幂等窗口 | facade 的查找先于 enqueue；该查找按同 key、非终态选择；enqueue 回调在队列锁内只匹配 `pending` 和 `entryKey`；scheduler 可把 pending 改成 scheduled；写入 key 还含 description。 | 运行中已发生重复；所有双提交都会重复；看到 await 就证明释放了锁；单个源码锁名足以证明跨进程互斥及全部权威写入约束。 |

这三项不应采用相同的“已检出缺陷”标记。局部 AST 事实可以确定；跨位置传递、生产装配、并发时序与业务义务分别保留为合同、模型或未知。

## 2. CPB：参数来源与显式常量

### 源码链与反证

- [pipeline.ts](/workspace/codepatchbay/cli/commands/pipeline.ts:36)：`parseCommonFlags` 初始化 `retries = 3`；`--retries` 分支采用 `parseInt(args[++i], 10) || 3`；返回对象保留 `retries`。`run` 用 `const parsed = parseCommonFlags(args)`，向 enqueue 的第二个参数写入 `metadata.maxRetries: parsed.retries`（第 205 行）。
- [hub-queue.ts](/workspace/codepatchbay/server/services/hub/hub-queue.ts:1549)：enqueue 不是无条件透明传递；它构造 `normalizedInput`，调用 `resolveAgentsForEntry`，再把返回的 metadata 写入 entry。要声称字段已经跨过此边界，必须分析该返回对象/所有覆盖或引用明确的传递模型，不能跳过它。
- [hub-orchestrator.ts](/workspace/codepatchbay/server/orchestrator/hub-orchestrator.ts:363)：创建 assignment 时使用 `metadata: candidate.metadata || {}`。这只是局部传递表达式；queue、assignment 持久化与 inbox/worker 之间不是普通函数参数链。
- [managed-worker.ts](/workspace/codepatchbay/runtime/worker/managed-worker.ts:1428)：局部 `metadata = assignment.metadata || {}`；正常执行分支在 `runJobWithServices({...})` 中指定 `maxRetries: 3`（第 1809 行），旁边的 agent 等字段才读取 metadata。finalizer-only 分支不执行该调用。
- [engine-runner.ts](/workspace/codepatchbay/server/services/engine-runner.ts:130)：从 opts 解构剩余 jobOptions，再通过 `...jobOptions`、显式字段和 `...services` 构造 runJob 参数。分析若继续向下，必须按 spread 顺序核对最终字段，不能看见第一处 spread 就宣布来源保留。
- [failure-router.ts](/workspace/codepatchbay/server/orchestrator/failure-router.ts:102)：另一个预算为 `MAX_RETRIES[failureKind] ?? 0`，使用 durable assignment attempts；它和 pipeline 参数、阶段重试、DAG 节点重试不是可以仅凭变量同名合并的概念。

首批自动结果应表述为：“在指定源码调用位置，写入的字段表达式是常量 3，与配置要求的 `metadata.maxRetries` 来源形式不同；给定 pipeline→managed worker 传递合同后，这是一项待复核的参数接线差异。”如果尚未自动证明中间传递，finding 保持 conditional/uncertain，不写成端到端数据流已证明断开。

这里的“默认”和“覆盖”必须分开：`parseInt(...) || 3` 是 falsy 回退；`x ?? 3` 是 nullish 回退；worker 的 `maxRetries: 3` 是直接常量赋值，不是读取上游失败后的默认。源表达式不同也不证明本次运行值不同；例如提交值恰好是 3。零是否是合法预算仍由产品合同决定。

### 可验收输出

1. 精确给出 producer 与 subject 的文件、词法 owner、调用点、参数下标、对象路径、原始 quote/hash、原始坐标及各自 symbolic AST。
2. 区分 `literal`、绑定到具体声明的 `identifier`、静态 `member`、`call`、`||`、`??`、条件表达式和 unsupported。局部 lexical origin 是表达式来源，不能冒充求得运行值。
3. producer 与 subject 各自成功定位才算两项事实成立。callee 作为源码表达式选择器时明确不意味着实际动态导入目标已绑定。
4. 明示 transport 的外部前提和反证；没有模型的 queue/assignment/IPC 段不得补成普通 CALLS 边。
5. 字段/调用未找到、源文件 partial、选择歧义、复杂对象形状分别保留 unknown；“找不到字段引用”不等于“输入从未使用”。

## 3. WWC：导航上下文的局部事实与组合条件

### 源码来源

- [home-dashboard-page.ts](/workspace/winwincode/apps/client/src/home-dashboard-page.ts:359)：可见的新任务锚点调用 `surfaceHash('/home/new-task', options.scopeSelection)`，随后加入 topActions。不是以隐藏的 my-work start 区作为唯一可触达证据。
- [scope-context.ts](/workspace/winwincode/packages/browser-core/src/scope-context.ts:271)：`surfaceHash(path, selection)` 用 `scopeHash(\`#${path}\`, selection)` 重新构造。对该已知 path，初始 query 为空。
- 同文件第 197–212 行：`scopeHash` 从传入 hash 创建 `URLSearchParams`，只迭代第 12 行的四项 `SCOPE_PARAMETER_NAMES`。它本身会保留原 hash 的其它 query key，所以不能全局声称“scopeHash 删除 delivery”；缺口取决于 surfaceHash 收到的本次无 query 路径。
- [application.ts](/workspace/winwincode/apps/client/src/application.ts:277)：`options.taskSeed === undefined` 选择生产端口；`deliveryContext` 从当前 `browser.location.hash` 取 delivery，context 或 delivery 为 null 即返回 null。第 1319 行将同一个 taskPort 交给 task entry model。
- [community-control-plane-client.ts](/workspace/winwincode/apps/client/src/community-control-plane-client.ts:2791)：production task port 的 `create` 等待 `options.deliveryContext()`，为 null 时先抛错，再谈后续 command。
- [task-entry-view-model.ts](/workspace/winwincode/apps/client/src/task-entry-view-model.ts:311)：构造输入仅有 device/client、repository binding、base branch、description、model route，交给 `port.create`。
- [boot.ts](/workspace/winwincode/apps/client/src/boot.ts:23)：默认启动只传 root/serverUrl，没有 taskSeed。ChatDeliveryCreator 是另外一条真实创建链；手工带 delivery 的 URL 和 fake 端口也是必须保留的反证。

### 模型要求与本轮合理范围

“新 URL 没有某 key”是负证，需要封闭的 query 来源与写入 key 集合；不能仅因表单对象不含 delivery 就证明 URL 缺失。若实现 URL/URLSearchParams 语义，需要显式的版本化标准接口模型，并核对名字遮蔽、别名、构造参数、set/append/delete、动态 key 和所有返回分支；不允许按方法文本名猜浏览器原生对象。

局部 getter `routeParameters(...).get('delivery')`、null return、消费者 null throw 可以作为分别带 guard 的结构证据。把它们组合为用户失败仍有条件：使用默认生产组合、实际进入指定导航、提交前没有补写 delivery、表单通过其它前置校验。单有源码文本出现和读取顺序不足以证明调用、闭包身份与可达性。

本轮如果只提供通用参数/字段 AST，它可以核对 literal route、query key、组合参数和 guard 定位；产品结论继续 evidence_only。不要为“把第三个候选自动化”添加仓库名分支或硬编码 `delivery` 专用判定。

## 4. CPB：幂等前置读与权威写入边界

### 源码事实

- [idempotency.ts](/workspace/codepatchbay/core/contracts/idempotency.ts:5)：项目明示同 key 的任意非终态任务应复用；`selectIdempotentEntry` 按 metadata.queueDedupeKey 相等、状态非终态选择。这是本例真正的仓库合同来源，优先于分析者自行发明的规范。
- [fix.ts](/workspace/codepatchbay/cli/commands/fix.ts:513)：同 key 查找经 `deps.loadQueue` 和 `selectIdempotentEntry` 完成；存在活动项则提前返回。未命中后还有 await loadRegistry、route/input 构造，再调用 `deps.enqueue`。deps 允许注入，因此模型必须区分默认生产实现与任意传入实现。
- [hub-queue.ts](/workspace/codepatchbay/server/services/hub/hub-queue.ts:1545)：`entryKey` 使用 project、description、lineage；lineage 首选 queueDedupeKey。锁内的 enqueue 回调第 1595–1619 行只复用相同 entryKey 且 status=pending 的 entry，否则 push 新 entry。
- 同文件第 1454–1463 行：`withQueueMutation` 经 `withQueueLock` 调 callback。第 1392–1403 行位于取得锁成功之后，顺序为 loadLocalQueue→await callback→必要时 saveLocalQueue→release；单独的 `loadQueue` 仅调用 loadLocalQueue。不能把这个 `await callback` 错判为提前释放锁。
- [hub-orchestrator.ts](/workspace/codepatchbay/server/orchestrator/hub-orchestrator.ts:342)：调度预约以 expectedStatus=pending 的条件更新把 entry 改成 scheduled。

这里还有两种不同寿命的保护：process fence 分别包围目录 owner lock 的取得/释放；跨越 fresh read、业务 callback 与 save 的是后者。不能把 process fence 的短回调误当整个 enqueue 的事务区域。更完整的源码账本见 [ATOMICITY_EVIDENCE.md](ATOMICITY_EVIDENCE.md)。

### 自动结果的边界

可提取“读/查/写操作分别位于哪一个词法回调/封装区域”及 guard 表达式、关键字段、声明顺序。但如果未分析封装实现，`withQueueMutation` 只是函数名，不自动意味着事务。可信 operation model 必须关联真实实现、锁身份和范围、callback 下标、提交/释放位置及失败路径；模型不证明文件系统/跨进程锁的运行效果。

人工交错仍为 A/B 都前置未命中→A enqueue→scheduler 把 A 改 scheduled→B enqueue。要自动推出窗口，需要同一 project/key 的身份等价、两个流程都可到达写入、没有更外层统一锁/唯一约束、scheduled 转换可夹在两次写入之间等条件。不能以“read-check 在函数上方、write 在下方”直接当作并发漏洞。

反证必须保留：顺序请求会复用；相同 description/key 且第一项仍 pending 时锁内也去重；任意不同业务请求并不要求复用；生产外层若存在未分析的串行化或唯一性保障，结论需重新评估。本轮如未实现身份和原子边界组合，只记录来源证据与能力差距，不以人工挑选的一个 AST 模式冒充完整自动并发检测。

## 5. 通用来源分析的正确性门槛

| 领域 | 必须满足的边界 |
| --- | --- |
| 选择范围 | 文件+精确词法 symbol+callee 表达式+参数下标+对象路径；重复声明/多个调用按 all_direct_calls 全部列出，不能只选择吻合的一项。 |
| 调用作用域 | 除非单独选择嵌套 owner，不把回调、对象方法、嵌套函数的调用算进外层 direct calls；缺 caller 不算检查通过。 |
| 属性构造 | 按对象属性顺序处理。末尾显式字段可以覆盖前置 spread；后置未知 spread/动态 computed 可能覆盖。任何省略必须有封闭形状依据。 |
| 属性名称 | 转义 identifier/string key 不能未经解码就报缺字段；computed、重复、getter/setter、__proto__ 或未支持语法应保守未知。 |
| 绑定与来源 | 区分作用域内同名绑定、参数、catch、块级遮蔽、var 提升、destructuring、重赋值与 TDZ。`const obj` 不等于对象深层不可变；逃逸/别名写入不能被忽略。 |
| 表达式语义 | 表达式结构相同不是运行值相等；不同不是必定不同。`||` 与 `??` 的回退集合不同；副作用 call 不求值，类型擦除不得吞运行表达式。 |
| 条件 | AST guard 的存在、分支位置与操作顺序分开保存；不把不可达分支算运行见证，不从语法父节点直接宣布业务条件满足。 |
| 失败与未知 | parse_error、source_missing、hash_changed、复杂 expression、别名/多目标、未知 transport 均可见；未知不当 absence，不从分母删去。 |
| 输出 | source_fact / lexical_origin / contract_assumptions / counterevidence / unknown 分离，结论按实际能力命名；条件未推断时 finding 保持 uncertain。 |

规则、来源模型及工具实现版本必须进入不可变快照/政策身份；证据保存原始文本/hash/坐标和完整原快照指针。辅助输入不变成已解析实现文件；历史发现不得以当前模型隐式重新判定。新增类别应可用于别的仓库，配置中不允许按项目名执行特例代码。

## 6. Rust：同一个泛型固有 impl 的窄路径

本轮唯一拟解除的泛型限制是：调用者和目标是同一个显式固有 impl 的源码成员，接收器直接是词法 `self`；或更窄的 `Self::` 同 impl 静态函数。它不需要先知道 Port/Codex 的运行实参，但只证明该源码声明关系，不证明所有泛型约束可满足或程序可编译。

正向材料为 [WorkerMain](/workspace/winwincode/crates/winwincode-worker/src/lib.rs:399) 同一个 `impl<Port, Codex> WorkerMain<Port, Codex> where ...` 内的 `accept_control→accept_dispatch`。两侧原生 receiver 均为 `&mut self`。原位置 `self.codex.ensure_thread` 是泛型字段端口，必须继续 unknown。

审核要求：

1. 建立独立的同 impl 词法成员路径，不移除既有泛型全局 guard，不按擦除参数后的 WorkerMain 名称在全局 registry 选方法。
2. 调用者最近 function 直接属于该 impl；嵌套 fn 不借用外层 Self。原生 receiver 必须唯一，typed self/alias/字段/任意表达式不借道。
3. 目标为该 impl 内唯一固有成员；同名其它 impl/trait、未知 default、Deref、宏、cfg、重复声明、多模块上下文、部分解析、receiver 所有权/借用竞争继续保守处理。首批拒绝源/目标独立 method-level 泛型或 where 条件。
4. `Self::` 首批仅同 impl static 函数，避免将任意显式 receiver 参数误认为当前 self。保留既有 helper/interface 可信模型的竞争检查与来源标签。
5. 证据记录源/目标位置、同一个 impl 身份、原泛型参数与 where 文本、receiver 形式，明确 generic instantiation/bounds 未验证。不要伪装成类型检查器完成了实例化。

可验收的改善是正向 Worker 观察有原调用点的唯一受限静态边，同时三条 intentional unknown 不变，已有 WorkRun/Production 见证不丢失或降级成无来源确定性。若窄规则无法满足这些守门条件，保留 unknown 比凑齐 10/10 更正确。

## 7. 本轮正式结果的独立核对清单

- 原基准 SHA256 与全部 26 项 ID/顺序不变；source_changed、unknown、evidence_only 等仍列在全分母中。
- 调用改善使用保存快照的原文件 hash、调用位置、源/目标身份及逐边模型前提；不得以其它同名调用代替。
- 新参数事实和任何导航/原子边界证据另表记录规则来源、假设、反证、未知、状态；不将它们并入旧 reproduced 计数。
- 所有修改有新分析器/检测器/模型版本及工具源码指纹，正式冷/热扫描同输入保持同 snapshot 身份；Coco 计数不是能力通过证据。
- 两个仓库保持原 commit 和只读；本审查仅阅读源码及保存产物。若由根代理正常运行静态扫描，明确它与目标执行/测试的区别。

在完整结果到达前，本文件只支持设计推进，不宣称本轮功能已完成。当前独立优先级是先把参数/字段的有限模型做正确，再考虑导航与事务组合；不要用宽泛“数据流已支持”覆盖尚未建模的边界。
