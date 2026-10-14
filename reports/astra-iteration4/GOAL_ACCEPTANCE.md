# 实际目标验收合同：五项完整静态判断

版本：v1。日期：2026-10-12。制定时工具起点为 CallScope v0.6。

本合同在 v0.7 正式结果之前制定，评价标准独立于新增实现。它不修改 [Astra CPB v1](../astra-baseline/CODEPATCHBAY_ANALYSIS.md)、[WWC v1](../astra-baseline/WINWINCODE_ANALYSIS.md)、[原26项观察](../astra-baseline/capability-baseline.json)或其分母。本轮只阅读源码、保存报告及配置；没有导入、执行、测试、构建目标，没有浏览器或测试套件验证。

## 1. 验收目标与完整判断

目标是让工具在声明范围内自动产生、连接并保存支持完整代码判断的证据：入口和生产装配是什么，数据或状态怎样传递，何种条件下进入消费者，哪个守卫或权威写入决定结果，什么反证限制结论。只定位调用、字段、guard 或 lock 的多个角色不足以完成这项目标。

v0.6 重现了冻结的10条正向调用观察，并正确保留3条指定未知；这不是本合同的达标标准。三条配置式有限合同已复核初始化集合、对象键和两处参数来源形式，仍不能替代下文五项完整判断。当前五项都还有必要证据段没有自动闭合，不能宣布系统已达到用户要求的功能判断能力。

“完整”在这里限于指定入口、静态模型和明确不变量，不保证所有业务正确或某次运行必然成功。完整的有条件静态判断可以保留真实环境条件，例如用户沿该href导航且提交前URL没有被修改、并发请求同属一个队列。**不能把尚未实现的中间分析写成假设后算完成**，例如“假设所有字段都已传播”“假设配置的callback就是实际注入者”“假设这个函数包住了所有写入”。这些必须进入尚未解决的证据段。

## 2. 统一证据义务

每项判断需保存原claim、范围、条件和反证，随后逐子义务提供证据与最终assessment。下列来源分开表达，不折算成通用置信分：

| 来源类别 | 可以承载什么 | 不允许替代什么 |
| --- | --- | --- |
| `source-derived` | 从保存AST生成的声明身份、实参/返回/赋值、字段构造、分支、谓词、调用点及范围 | 运行值、动态目标、隐含通信或未分析路径 |
| `trusted-model` | 有版本和适用检查的URLSearchParams、普通对象/JSON、回调协议、资源保护语义等有限模型 | 未验证模型适用性、完整编译器或实际部署证明 |
| `policy-declared` | 明确的必需字段、不变量、资源/命令映射、适用环境条件及作者审批状态 | 中间源码关系、实际派发目标、预计算的路径/缺键/谓词差异/交错 |
| `unresolved` | 缺来源、解析/绑定不足、对象逃逸、未知返回、保护区失败、运输或条件未闭合 | 不得改名为普通条件或从分母移除后宣布完整 |

所有自动事实必须绑定快照、原文件hash、词法owner、声明/AST位置、提取器/模型版本及剩余边界；历史下钻读取保存原文。缺文件、坏hash、重复声明、parser缺口、超预算及截断都需可见。摘要须有总数、采样标记和完整证据指针；样本不能替代完整义务检查。

callee源码拼写、配置中的实现角色与实际绑定分别检查。`ctx.deps`覆盖、factory返回对象、callback属性、闭包捕获值和receiver身份不能按同名相连。消息、跨语言字段和持久记录使用独立关系及身份，不伪造普通CALLS。控制流至少保留分支、早退、guard效果及局部先后，不能从调用图的两条边证明支配或顺序。

每条必要子义务必须有已支持、已否定、尚未知或来源失效的结果，包含“形式匹配”等不产生Finding的结果。空findings、所有选择器均定位到源码、没有红色节点都不是完成记录。目标账本须独立于26项调用/来源基准和额外AST锚点；不把五项evidence_only改名或把局部事实增加为新的通过项。

原26项的`expected=evidence_only`只冻结那份图级观察的类别，不意味着五项判断永远不能自动完成。新的目标账本可以在必要子义务全部闭合、可信模型及真实环境条件清楚时记录`scoped_static_judgment_reproduced`；原26项仍按原协议保留历史分类。这是独立完整判断的达成，不是给旧evidence_only换标签，也不能由调用样本增长代替。

最终assessment只允许：

- **完整静态条件判断已支持**：必要源码关系和受信模型适用检查都闭合，自动推导与原claim在其真实条件内一致，反证和剩余运行条件完整保存。仍不是运行故障或业务验收证明。
- **原claim不成立或需收窄**：自动证据反驳一段，明确新的范围和反证；不得为了重现旧文字丢掉真实保护或保留关系。
- **仅支持局部义务**：局部源码事实成立，但完整来源、绑定、guard、运输、状态或保护关系尚缺；列出具体缺段。
- **未知/来源失效**：必要来源、解析、身份或模型不满足，不能作负证。已成立的局部正事实可以保留。

## 3. v0.6实际差距账本

| 完整判断 | v0.6自动可用 | 尚缺的必要闭合段 | 本合同起点assessment |
| --- | --- | --- | --- |
| CPB-01：pipeline重试选项与受管理预算 | producer `parsed.retries`匹配、consumer新对象`maxRetries:3`形式差异；conditional/uncertain保留 | 正常队列新建/复用分支，metadata规范化与持久/消息运输，动态端口，engine有效消费者及预算归属/条件 | 仅支持两处局部来源形式 |
| CPB-02：superseded跨层终态分类 | 两个封闭初始化字符串集合差异，缺superseded的有限事实 | 状态赋值/投影→具体job身份→isTerminal谓词→recover guard；event-store终态保护反证；terminal与recoverable政策区分 | 仅支持初始化集合义务 |
| CPB-03：同键去重读查与权威写入 | 调用、源码及人工保护范围整理；没有自动region/谓词/交错裁决 | 默认deps真实来源，资源身份，callback保护生命周期，外内谓词关系，scheduler受guard状态转换；条件交错推导 | 必要关系仍需人工，未完成自动判断 |
| WWC-01：看板导航与生产task port上下文 | 调用和保存原文；人工URL/闭包来源稿 | seed→helper参数/返回→possible query keys→href，boot/factory/callback/port注入，ambient读取、null传播和throw guard | 必要关系仍需人工，未完成自动判断 |
| WWC-02：Device更新spec条件必填字段 | 封闭返回对象缺verificationCommand；源码事实确认且Device适用仍uncertain | UI真实client装配、update_spec命令/协议映射、Rust反序列化和authority分派，Device条件及非空guard，local/Chat反证 | 仅支持对象构造义务 |

正式起点见 [v0.6 REPORT](../astra-iteration3/REPORT.md)、[能力账本](../astra-iteration3/capability-ledger.json)和 [有限合同见证](../astra-iteration3/finite-contract-witnesses.json)。没有字段流、导航或并发完整能力的结果不能用10/10调用重现抵消。

## 4. 五项判断的独立验收义务

### CPB-01：重试选项到有效预算

原判断范围为正常pipeline提交进入受管理执行链；不是“没有任何retry能力”。首先应明确用户选项控制queue attempt、pipeline、phase还是DAG/node预算；不同预算不得因都叫maxRetries而合并。该意图来源与审批状态必须保存。

| 子义务 | 需由分析生成的证据 | 不闭合时的结论 |
| --- | --- | --- |
| P1 参数来源 | `parseCommonFlags`的初始化、flag写入、truthiness默认、返回binding→run.parsed→enqueue.metadata.maxRetries，逐声明身份关联 | 不能仅用同名retries说明返回值来源；未建模分支/返回为unknown |
| P2 正常装配 | CLI默认enqueue、queue/scheduler/assignment、worker direct/broker和动态bridge的实际来源；覆盖或注入另列 | 配置写了一个实现路径不等于绑定；动态目标不足不算完整 |
| P3 中间字段 | 规范化return/merge、new/existing queue分支、candidate/assignment、inbox写读/JSON、worker.metadata逐段关系 | 字段同名或type cast不是保留证明；复用旧记录不能当本次输入 |
| P4 消费选择 | worker新参数对象、finalizer-only等分支，bridge转交、rest/spread顺序、service返回键、最终预算读/比较 | 常量3是独立构造；无同对象身份和顺序不能标覆盖 |
| P5 预算决策 | 具体决策guard、默认/局部预算、实际尝试计数及适用阶段；opaque消费者单列 | 不得从局部MAX_RETRIES推导全程序从未读metadata |
| P6 结论与反证 | 请求值可能也是3；旧pending复用；finalizer-only；不同重试预算；opaque supervisor；未发生调用等 | 形式差异仅局部义务，未闭合传输/预算不算完整接线断接证明 |

验收要求是自动关联上述关系并说明明确预算合同是否满足，不要求求出某次运行的数字。支持范围外的反射、代理、动态模块或路径必须保留unknown；不能用所有调用存在替代参数语义。

### CPB-02：状态生产、终态谓词与保护反证

| 子义务 | 需由分析生成的证据 | 必須保留的限制 |
| --- | --- | --- |
| S1 状态生产 | event-materializer `job_superseded`将state.status设为superseded的AST、事件入口与对象身份 | 字符串出现不是生产状态写入 |
| S2 定义与谓词 | materializer/job-store两个terminal集合及各`.has`实际接收者；isTerminal中的jobId缺失早真、status默认 | 只比较集合不证明具体job判读；有jobId的superseded与缺jobId要分开 |
| S3 消费guard | `recoverAsNewJob`读original及`!isTerminal(original)`拒绝的来源/guard；所用status来自对应job投影 | 看见recover调用不等于guard效果已推导 |
| S4 权威保护 | event-store使用含superseded集合拒绝后续业务变更，保留实际POST_TERMINAL_ALLOWED分支 | 不能推导“终态可非法改写” |
| S5 政策和结论 | terminal分类差异与是否允许recoverable分别说明，跨层比较有明确合同 | 不同用途集合不得强制全等；不由终态分类自动开放恢复 |

完整结果应给出所选合法job身份条件下谓词差异及其具体消费者效果，再限制业务影响；初始化集合的一个缺项不单独完成这条判断。

### CPB-03：预查、权威资源与保护范围

| 子义务 | 需由分析生成的证据 | 不允许的替代 |
| --- | --- | --- |
| A1 实际deps | resolveDeps默认load/enqueue来源、ctx.deps覆盖条件及run调用关联 | role-config列了两个文件不算默认装配证明 |
| A2 预查谓词 | 同project、hashed queueDedupeKey、非terminal选择、existing.id早退及发生于enqueue之前的局部顺序 | 不用callee名字或quote命中推断谓词 |
| A3 资源关联 | facade的hubRoot实参→实际load/save queuePath，writer及scheduler同逻辑资源的来源与可信范围 | 同名root变量不证明物理同资源 |
| A4 保护region | wrapper转发的callback身份、目录owner lock acquire→fresh read→callback→save→release及错误/退出；process fence独立范围 | wrapper抽取失败必须unknown，不能当“callback不受保护”；不能以lock存在证明整个facade串行 |
| A5 内层谓词/写入 | writer pending+含description复合key的find、existing return、push/commit出处和保护归属 | 内层确实查重；不能报告“无锁/无二次检查” |
| A6 状态竞争来源 | scheduler实际binding、pending→scheduled的guarded update及容量/leader/版本/失败回滚前提 | 状态patch存在不证明该任务成功改变或与请求交错 |
| A7 条件风险推导 | 外内口径与region差异先独立报告；若报告可产生重复的交错，须从抽取状态/操作及显式保护语义求得，保留可达条件和未知 | 不接受配置预填A/B步骤；未实现交错只能局部region/谓词结果，不能称完整竞态发现 |

产品不变量来自idempotency合同：同project+同key的任意非terminal任务复用，终态允许新建。权威点/锁协议/物理资源模型必须独立声明并检查源码适用性。目录锁、文件原子rename及崩溃恢复的真实运行行为不在本轮证明范围，不能把SQLite快照原子发布误用为目标队列原子性。

反证必须自动定位或明确缺口：预查已见scheduled/in_progress会复用；writer见同复合key且pending会复用；scheduler可能被guard/容量阻止；dispatch可能回滚pending；lock/write失败阻止commit。完整条件风险不表示任意双提交必然重复。

### WWC-01：导航键与真实callback的拒绝链

| 子义务 | 需由分析生成的证据 | 不闭合时的限制 |
| --- | --- | --- |
| N1 可见生产点 | 看板newTask.href赋值和实际组合；字面seed `/home/new-task`；import绑定到surfaceHash | 不用隐藏按钮或字符串搜索证明公开入口 |
| N2 参数/返回链 | surfaceHash→scopeHash的实参/形参、前缀和return；URLSearchParams receiver来源及有限set/delete keys | helper配置不是参数/返回证明；未知mutation/逃逸不能作缺键负证 |
| N3 查询抽象 | seed keys、possible/guaranteed keys、分支join和序列化结果；required delivery不在possible集合 | 四个scope值可缺省，不能说四键必定存在；scopeHash保留已有query |
| N4 正常装配 | normal boot无taskSeed→真实factory分支，deliveryContext实参属性→options callback调用，返回create方法→taskPort/VM注入 | 不按全局同名deliveryContext/create连接；fake分支单列 |
| N5 消费guard | callback读当前browser.location.hash→routeParameters→get(delivery)→deliveryId null→callback返回null→真实create throw，HTTP提交在guard之后 | 每段要有来源及局部控制条件；只定位两个null守卫不足以证明传播 |
| N6 环境接缝 | href导航到ambient hash、提交时仍为该hash、表单前置条件、标准DOM/URL API模型 | 导航时序是显式环境条件，不伪造精确参数流；未完成binding/return分析不归类为环境条件 |
| N7 反证与结论 | 已有有效delivery seed被保留；手工URL；taskSeed/fake；Chat独立创建；条件适用范围 | 缺键链只支持所选默认入口的有条件拒绝，不泛化所有创建失败 |

完整判断可以输出“在明确导航/提交环境条件下，该构造未提供必需query key，经真实callback的null传播在HTTP前拒绝”。只有source seed/key缺失或callback属性定位属于局部义务；缺少装配、null传播、guard或模块身份时仍未达成完整判断。

### WWC-02：TypeScript payload到Device条件guard

| 子义务 | 需由分析生成的证据 | 不允许的跳跃 |
| --- | --- | --- |
| D1 生产构造 | clarificationUpdateCommand的完整返回对象及spec字段，verificationCommand缺失、未知spread/return排除 | 字段optional不能替代对象内容分析 |
| D2 真实提交 | ViewModel保存调用→实际client→application生产注入，返回命令身份与spec路径 | 配置指向client角色不等于对象注入已解析 |
| D3 协议身份 | delivery.update_spec命令、版本、verificationCommand↔verification_command字段映射、JSON缺省行为、Rust真实反序列化/dispatcher | 仅捕获generated协议原文不生成调用；跨语言同名不构成运输 |
| D4 authority与guard | LocalDeliveryAuthority处理create/update的来源，Device目标条件，Option/空白非空检查及拒绝在使用前的guard | 找到后端guard不能假设该UI输入一定进入Device分支 |
| D5 分支与反证 | 非Device仓库回退、Chat显式字段、已有criterion展示不是顶层verificationCommand、授权/命令确认条件 | 不泛化所有规格编辑失败，不从UI文本猜可执行命令 |

完整判断需说明缺省/字段映射在所选协议模型内怎样到达条件拒绝。Device是否活动可保留真实条件，但前端→协议→authority的未实现中间关系不得当成“假设已连接”。v0.6的对象缺键事实仍是必要而不充分的一段。

## 5. CPB中间field-flow：补读来源与最小通用规范

本节是只读来源助手整理，**不是v0.7已实现或自动字段流结果**。路径相对于 `/workspace/codepatchbay`，行号是本次源码定位；既有8份参数来源身份见 [PARAMETER_EVIDENCE](../astra-iteration3/PARAMETER_EVIDENCE.md)，新增来源hash在下节。当前没有为这些段添加新的自动通过项。

| 段 | 本次直接核对的来源 | 真正支持的局部事实与尚未知 |
| --- | --- | --- |
| normalization | `hub-queue.ts:1561`先展开input，`:1580–1581`调用resolveAgentsForEntry并整体赋metadata；`agent-config.ts:487/489`原样return或`{...metadata,agents,agent}` | 普通可枚举自有maxRetries有保留依据，不能仅因重建称丢失；callee/return/别名及可见修改要独立摘要 |
| queue分支 | `hub-queue.ts:1597–1598`复用existing，`:1612`新entry读normalizedInput.metadata | 复用的metadata不是必定来自本次producer；不能把两支合成单一来源 |
| scheduler | `scheduler.ts:285–341`候选筛选；`:460–488`readiness分支展开entry.metadata、写nextMetadata再回传entry | 此分支没有显式maxRetries覆盖；其它gate/ranking/回调和持久读取未全部闭合，不能从一个spread宣称所有candidate保留 |
| assignment实参 | `hub-orchestrator.ts:364–374`调用this.assignmentStore，metadata=candidate.metadata||{} | 成员callee需由constructor/receiver装配证明；truthiness默认与所选candidate身份保留 |
| assignment返回 | `shared/orchestrator/assignment-store.ts:495–549`existing分支`:512`以existing→incoming metadata展开；new分支`:537`recordValue(metadata) | 既有记录与incoming覆盖顺序明确，new保留record值；`shared/types.ts:217`不符合record时返回{}。锁内callback和JSON写入语义另外建模 |
| inbox生产 | `hub-orchestrator.ts:417–431`flattened payload包含assignment.metadata||{}及assignment/entry/attempt身份 | 元数据与消息身份显式构造；不证明某次发送/接收实际成功或仅有一个写者 |
| inbox规范化 | `worker-store.ts:1932`writeInbox→`:1698`writeInboxWithReceipt；`:578–600`structuredClone→JSON.stringify→JSON.parse；`:1732`写committedPayload | 普通JSON数值/字段保留需受信JSON模型；undefined、非有限值、getter/自定义原型和异常不能无条件保留。receipt/owner/generation不等于一般值流证明 |
| inbox读取 | `worker-store.ts:1960–2017`按worker目录claim，`:1975`rename到processing、`:2002/2004`读取后返回claim.assignment；异常`:2010`malformed标记 | path/assignment/claim/attempt关联和异常分支需保存；不能把读过同名assignment当源消息对应 |
| direct/broker装配 | `managed-worker.ts:1263–1285`env选择broker或两个direct stores；`worker-broker-client.ts:154`inbox.claim、`:125–148`JSON envelope；server worker-state-broker`:217`派发；client`:81–90`结果校验 | broker/direct都是实际候选。HTTP端点、operation、响应result、worker/incarnation/assignment/attempt以及可注入fetch需独立关系；未证明生产绑定时unknown |
| worker字段 | `managed-worker.ts:1394/1397/1428`claim.assignment.metadata||{}；`:1784–1809`非finalizer-only新调用对象写maxRetries:3 | 此处确为新对象；与输入值相等仍可能。attempt/lease等早退及finalizer-only不能删掉 |
| bridge/engine | `bridges/engine-bridge.ts:18–19`转交opts；`engine-runner.ts:131–138`rest为jobOptions，`:157–180`先展开jobOptions后services；buildServices`:85–121`字面ports无maxRetries；`core/engine/run-job.ts:65–75`ctxInput guard/cast后交runJobInner | opts转交、rest排除键和spread顺序可抽取；services返回/alias/mutation要闭合，类型cast不验证有效预算。核心consumer及opaque调用还未全分析 |
| 另一个预算 | `failure-router.ts:112/265`MAX_RETRIES[kind]与attempt比较；`:277`整个assignment进入supervisor | 局部预算独立于pipeline metadata，supervisor是实际opaque反证；不从搜索缺字段推出全程序没有消费者 |

通用最小规范先支持以下关系，各自有源码身份、certainty、条件和barriers：

1. **局部字段构造/读取**：对象字面键、shorthand、静态member path；所选字段封闭与整个对象封闭分开。spread顺序、重复键、getter、prototype/动态键和未知来源必须阻止不当负证。
2. **实参/形参和返回摘要**：按精确绑定、参数位置、destructuring/rest及各return分支连接；唯一声明身份、alias/mutable/capture/escape和可见写入分别记录。闭包回调由实际注入点关联，不按名字连接。
3. **字段映射、merge、默认**：记录构造新对象、普通对象展开及覆盖优先级；区分`||`/`??`，对条件return做分支join。只有证明同对象身份和写入顺序后才能产生OVERWRITES_FIELD；worker两个对象不得使用该标签。
4. **记录和消息身份**：JSON模型必须有版本/适用检查，明确写入和读取资源、record/assignment/attempt/channel及command身份。跨文件/进程关系不是CALLS；路径或配置role只能作种子，实际source和decoder/dispatcher仍要抽取。
5. **消费者与适用条件**：把字段源连接到实际读取/guard/预算决策，保存早退、不同预算及未知消费者；不能承诺所有路径或一般运行值。闭合失败返回可定位unknown，不把未知对象当空对象。

规则可提供起点、终点、必需字段、业务不变量和受信模型；中间表达式、flow边、实际callee、merge/guard结果必须由分析生成。若第一批只提供局部关系摘要，就按局部能力验收，不因这些摘要连成示意图称为完整字段流。正向保留关系和负向缺失证明采用不同覆盖要求，未知路径不能使“无消费”负证成立。

## 6. 补读原文件身份

以下为本轮静态读取的原始字节SHA256，不是新的测试或自动核对结果。位置/文本应在正式新快照中重新核对；改变来源时不能沿用此处判断。

| 相对文件 | SHA256 |
| --- | --- |
| shared/orchestrator/assignment-store.ts | eb703d0845fd8aee1a97beddcb3c9f0502c7e6d912ec058a8e5110d08999ac48 |
| shared/orchestrator/worker-store.ts | 68ae1ada845a93248f491e2daa9c101b9fa3da56b823abd63c5afd6315b1f7de |
| shared/orchestrator/worker-broker-client.ts | 49c9d30632f8742cf597840c6cfb5e31f1581d7150c658d6835a68836e0e2a0b |
| shared/types.ts | d44aac646eaa445967f33ad8690be01cc360abfd6b6f38e515a0f843ba8ef64e |
| server/services/hub/worker-state-broker.ts | 4a9870790e90b8657b1ae7aac21f4acabfe8ae203388a115191b0e698c522ad2 |
| server/orchestrator/scheduler.ts | 69d275bae38a3a614d4d1b412542a8b2eb2b83f0f7b2bd694807cec529d55c00 |
| core/engine/run-job.ts | ae4a6baf16e3ca09c360f14ff52c084b83fc99a7206280fe4f7092d3b720a3cf |

## 7. v0.7交付评价方式

正式结果应另存目标账本，每项至少保留claim/条件/反证、上述子义务、自动source/model/policy来源、缺口、完整证据指针和assessment。账本逐项列全五项，不用新增样本提高百分比，不把人工整理稿算作分析器结果，不改原26项或五项冻结报告。

导航query keys/callback与CPB保护region/谓词若得到有限实现，应按本合同实际自动闭合到哪一段报告；其余段仍缺就保留“仅支持局部义务”。完整条件链与一个缺键事实、保护摘要与可达交错推导分别验收。任何failed/unknown wrapper、实际deps或guard缺口都继续阻止完整结论，不能当成反证排除。

后续扩展仍以正确证据和功能闭环优先，可扩展性其次，性能最后。不增加目标执行、测试、构建、沙箱或浏览器验证，也不以这种限制为由隐藏静态能力缺口。
