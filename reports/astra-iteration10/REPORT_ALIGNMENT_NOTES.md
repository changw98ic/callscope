# 两份原始分析报告与 CallScope 的能力对应

日期：2026-10-13。本文以固定的 [CodePatchBay 分析](../astra-baseline/CODEPATCHBAY_ANALYSIS.md) 和 [WinWinCode 分析](../astra-baseline/WINWINCODE_ANALYSIS.md) 为完整 benchmark，整理原判断、范围、反证、现有自动证据和具体能力差距。五个业务目标／30条义务是此前的实现台账，不取代这两份报告。本文不批准版本，不增加验收门槛，也不将人工读完报告计为系统自动达到。

两份报告都包含架构职责、主要功能链、具体缺口、保护和反证、覆盖及未审范围。新建的五个模块主要对应五项具体缺口；即使这五项均能自动输出，trusted probe、交付收尾、Auth 工厂、WorkRun 状态约束、Kernel 顺序和 Device provider 部署分流等报告判断仍有独立的能力差距。

## 固定来源与当前证据

| 原报告 | 原始字节 SHA256 | 本次目录化内容 |
| --- | --- | --- |
| CODEPATCHBAY_ANALYSIS.md | `863f5dfe52ced7129a0bda499afa4a89b30d2db9396c654a5120204cfe422900` | 16个标题段、63个原文段落／表格行／列表项 |
| WINWINCODE_ANALYSIS.md | `b3f8b1def361595e2bd3540a6bca5381ef4ad2a71d4f3c49535bf3f24f212950` | 16个标题段、67个原文段落／表格行／列表项 |

[REPORT_ALIGNMENT_CATALOG.json](REPORT_ALIGNMENT_CATALOG.json) 保存每个标题段与原文条目的 file、原文 hash、byte span、行位置、span hash、完整原句及范围上下文；另保存原26项机器观察的 claim、条件、反证、v11证据指针，以及原基线36个目标来源文件的固定／本次读取 hash。段落和表格行只是检索单位，包含标题表头、背景和未审声明，**不是新增的功能目标或通过率分母**。

当前正式自动证据取自 [v11能力账本](../astra-iteration9/capability-ledger.json)、两库 [CPB基线结果](../astra-iteration9/codepatchbay-baseline-v11-and-v10.json)、[WWC基线结果](../astra-iteration9/winwincode-baseline-v11-and-v10.json)、[字段结果](../astra-iteration9/field-assessments.json) 和保存 summary。v11复现的是10项确定调用／路径，保留3项预期未知；13项业务／架构观察仍按原协议为 evidence_only。后续有限分析已产生额外字段、导航和保护关系，这些关系与旧基线类别分别说明。

下文的“开发模块”只指出正在实现的对应能力。它不是正式自动结果，也不表示我对实现作批准。表中的源码位置沿用原报告；详细当前结果由正常分析产物提供。

## CodePatchBay：原报告判断对应

| 原报告的实际判断／出处 | 原范围及反证 | 当前自动证据与对应模块 | 尚未自动聚合的原报告链段 |
| --- | --- | --- | --- |
| “主要交付链在源码上已经接通”；CLI→队列→编排器→worker→服务→checklist/DAG→完成门→收尾。`判断`及`主要功能链路` | 指已读主要生产结构；包括动态模块、持久消息、独立进程和对象端口，不是运行成功。 | 图能给若干直接路径；`pipeline_flow`覆盖队列／执行子链；`status_analysis`覆盖状态子链。 | 将进程、inbox、对象端口和最终交付关系连成带范围的架构主链报告；当前不能仅凭一条 runJob→DAG 路径输出整链结论。 |
| CLI、orchestrator、worker/bridge、engine、workflow、services、shared 各自职责。`架构职责和所有权` | 职责／修改耦合判断；shared广泛使用不等于“上帝对象”；core不import server不等于不能使用注入端口。 | 模块／导入／调用及来源查询可支撑结构盘点。 | 责任、端口实现、权威存储与副作用边界尚无统一自动架构摘要；五模块也不是全架构分类器。 |
| “main…动态加载…调用 mod.run”；命令表与 CPB_EXECUTOR_ROOT 影响目标。`命令到任务` | 环境可覆盖executorRoot；候选不等于每个handler必然调用。 | `cpb.cli.dynamic-command-boundary`保持正确unknown；保存动态调用位置。 | 从命令表、path构造、import与export生成有条件候选，并将环境覆盖与未知原因一起报告；`pipeline_flow`只涉及所选命令链。 |
| fix主顺序为项目→readiness→同键查询→route/metadata→enqueue；readiness失败先返回。`fix.ts:505–508` | 只说明失败分支挡住本次提交；不说明注入依赖行为或后续执行成功。 | 旧观察 `cpb.fix.readiness-before-enqueue`为evidence_only；`atomicity_completion`处理同一facade的幂等链。 | 自动将实际readiness结果、失败return与后续enqueue顺序表达为保护事实；幂等选择的早退不能代替这一条readiness判断。 |
| pipeline把task、workflow、plan mode、agent及retries交给队列。`命令到任务` | 参数被接受、metadata构造与最终消费是三件事。 | `value_analysis`有参数形式；`field_relations`有实参／形参、alias、构造顺序；`pipeline_flow`继续连接。 | 参数解析返回值与具体入队构造、后续记录／消息和消费者之间的关联。 |
| tick调和assignment→候选→预约→assignment/attempt→worker→inbox；supervisor启动managed-worker，worker领取后经bridge执行。`hub-orchestrator.ts:315–450`、`managed-worker.ts:1393,1797` | 结构链存在，不宣称租约、消息持久性、重放及所有崩溃交错均正确。 | 原 `cpb.dispatch.queue-inbox-process-chain`为evidence_only；`pipeline_flow`是对应开发模块。 | queue/assignment/inbox的记录身份、worker启动参数和领取结果、bridge调用接线；输出独立消息／进程关系，不用伪造CALLS。 |
| buildServices组合broker或本地createJob、appendEvent、终态、pool、artifact、provider端口。`engine-runner.ts:85–121,130–180` | runJob接受不同ctx；不能把所有ctx.method全局绑定唯一server实现。 | service→runJob直接边已复现；engine字段展开关系已有条件支持；ctx.appendEvent全局unknown保留。 | 对实际返回端口的条件成员、实现来源和使用上下文做组合报告；`maxRetries`局部保留不等于所有端口均已接线。 |
| runJob→runJobInner；创建、准备、规划、冻结checklist/DAG、执行DAG有明确顺序及blocked/failed早退。`run-job.ts:75,121–177` | 高保障规划先于scope冻结；存在结构路径不表示每次必经。 | service→runJob、冻结checklist直接调用和service→DAG路径均已复现。 | 将返回discriminant、对应早退及后续步骤顺序聚合；已有直接边没有自动表达整段条件控制。 |
| crash barrier交给handleRunJobPanic；正常/panic都尝试finalizeAuditTrail且捕获其失败。`服务组合到checklist/DAG` | job尾部best-effort与Hub access audit fail-closed是不同合同。 | 当前可以检索调用和源码；五个业务模块未专门输出该判断。 | try/catch/finally、正常／panic路径及错误捕获结果；并保留审计对象不同，避免报告虚假矛盾。 |
| runAgent先检查允许agent，经pool执行，检查只读阶段变更并分类失败。`agent-runner.ts:475–589` | pool是注入端口；仅名字不能确定唯一实现。 | 图保存调用／动态边；`pipeline_flow`的agent配置传递不是本段完整执行判断。 | allowlist结果→pool实际执行→readonly违规→失败分类的条件链，以及生产pool组合候选。 |
| 子进程环境过滤与required/strict沙箱失败分支存在。`阶段执行和可信验证` | native/off/custom和平台能力改变边界；存在检查不等于隔离效果已运行验收。 | 来源可定位；五模块不覆盖该策略结果。 | 配置分支、环境构造、沙箱required/strict失败处理的自动摘要；范围仍只是源码策略。 |
| 可信probe只从HEAD策略取得predicateId对应executable/args，execFile使用shell:false；expectedEvidence不作命令。`probe-runner.ts:147–160,435–438,527–534` | 原报告没有执行probe；策略加载不是业务验收成立。 | `cpb.probe.trusted-policy-call`的直接加载调用已复现。 | HEAD读取→策略解析→predicateId选择→command参数→execFile选项的值来源链；当前直接call见证不能单独复现“可信命令来源”。 |
| static probe只给范围变更证据；缺可信策略及event/manual/absence等未支持方法会记录失败。`probe-runner.ts:613–637,707–726` | 不称需求语义已验证，不把未实现方法解释为静默放行；额外hardGate observation是边界。 | 有源码／调用查询；没有对应完整自动报告项。 | method分支→结构观察／emitFailedClaim→证据记录；将自动采集与额外外部observation分开。 |
| completion-gate先checklist，再按mutating检查verify/adversarial；readonly/docs/parent有豁免。`阶段执行和可信验证` | 门的存在与外部执行结果真实可靠分开。 | 可以定位直接调用与分支；五模块没有输出整组工作流条件。 | 工作流分类→所需gate→拒绝/豁免结果，保留每种分支。 |
| 事件流是权威来源；event-store在锁内重建状态并封终态业务变更；索引是后续投影。`event-store.ts:1188–1197` | 事件持久化与索引失败不是同一提交边界；存在重建/doctor/调和，不推永久丢失。 | `status_analysis`对应终态封口部分；旧atomicity分析对应queue锁而非事件所有权全链。 | event持久化→index update与各自失败分支、修复来源的自动关联；不能将队列保护事实套到事件/索引上。 |
| remediation FIXED记录job_superseded并创建lineage task；finalizer有独立journal，外部GitHub与dry-run分开。`review-dispatch.ts:4468–4470` | 是否发布取决配置／授权，API存在不表示发生发布。 | `status_analysis`连接superseded状态含义；来源查询能定位review调用。 | FIXED控制→superseded事件→lineage新task，以及finalizer journal/remote action/dry-run的条件连接。 |
| “核心job的completed还不是assignment或远端发布最终成功”；autoFinalize可把结果变failed，之后worker持久／读回、reconciler收敛。`assignment-finalizer.ts:1236–1242` | autoFinalize关闭、外部发布条件、工作区清理和journal范围均保留。 | `cpb.finalization.completed-is-not-published`仍evidence_only；五模块没有完整收尾判断。 | result.status＋autoFinalize＋finalizeResult→persistedJobResult/status→终态写读→attempt/finalizer/journal调和。这是独立于重试字段的主要功能链。 |
| CPB-01：“pipeline --retries…接线遗漏”。`具体缺口` | 已读受管理生产链；phase/DAG/infra预算不同；请求可能本就为3；零值是否允许属于产品合同。 | 参数形式、worker常量3、局部预算均有自动事实；`pipeline_flow`对应全链。 | 报告所指请求参数到所读有效worker／FailureRouter预算的连接与不连接来源；不能把局部常量或未绑定消费者直接改写成全程序无retry。 |
| CPB-02：“superseded…两个生产终态分类不一致”，isTerminal false导致recover非终态拒绝。`具体缺口` | 有效jobId且当前superseded；event-store封口作反证；允许recovery是另一个政策。 | 字符串Set初始化差异已自动保存；`status_analysis`扩展生产状态、实际谓词和消费者效果。 | 从当前集合差异进一步生成报告中的具体谓词结果、recover拒绝和封口反证；不扩大为全状态历史不可变或必须开放恢复。 |
| CPB-03：“同键幂等检查…并发窗口”；同key不同description另有口径差异。`具体缺口` | A/B都预查无项→A入队→A变scheduled→B入队；顺序调用复用active、同描述仍pending时底层去重。 | `atomicity_analysis`有外内谓词与保护region；`atomicity_completion`处理实际转移和条件交错。 | 从源码操作生成原报告的条件交错与两个反证，给出“可以发生”的有限风险而非所有双提交必重复。 |

## WinWinCode：原报告判断对应

| 原报告的实际判断／出处 | 原范围及反证 | 当前自动证据与对应模块 | 尚未自动聚合的原报告链段 |
| --- | --- | --- | --- |
| “已有真实的纵向产品结构”：Browser→生成合同/Server→Control Plane/Delivery→ExecutionPort/Worker→ProductionCodexAdapter→Kernel。`判断` | 链条存在与每个公开入口完成任务分开；不宣称运行正确。 | Rust/TS图及来源查询提供部分结构；`device_flow`补selected command协议链。 | 整个纵向链的协议、组合、身份和条件摘要；Device spec子链不能替代Worker/Kernel执行链。 |
| Client只组织请求，产品写入经canonical command；各domain、Worker、Kernel、Device职责和身份分开。`架构与职责` | ProductSession/WorkerSession/CodexThread/WorkRun不能合成一个session_id；大模块不自动等于职责混乱。 | 模块、定义、调用和schema来源可查。 | 所有权与各身份字段间的关系尚未统一输出；五模块不等于全领域架构报告。 |
| boot没有taskSeed；application按runtime/auth/scope组合真实端口，lazy挂载受generation/abort限制。`boot.ts:23`、`浏览器启动` | 源码生产组合，不是浏览器行为或全部UI可用性验收。 | v11 `port_wiring`已输出normal boot→task factory→VM port装配；`navigation_completion`关联本入口。 | auth、其它页面和runtime变体的通用装配／过期结果保护仍未形成全application摘要。原导航结论不要求增加所有UI隐含root的通用证明。 |
| diagnosticScope→resolveScopeContext→scopeSelectionFromHash的来源确定。`application.ts:359` | session=null可提前返回；结构边不表示总执行。 | diagnosticScope命名调用已reproduced，scope helper可查询。 | 若报告进一步解释scope结果，仍需读取返回与分支；单个确定call的原观察已可复现。 |
| application inline import/U+0000等曾导致工具漏入口，不能归因项目缺实现。`浏览器启动` | 保留原字节／定位和真实解析失败。 | 现有TS派生解析映射已恢复相关文件；正式WWC 471选入、465完整解析，剩余缺口保留。 | 这一历史覆盖问题与修复范围可直接进入报告；不能用解析率代替下述产品链结论。 |
| typed facade／生成合同通过HTTP/WS command/query/event进入Rust dispatcher。`浏览器启动、范围和协议` | endpoint相同不证明payload、授权或全部处理成功；协议不是跨语言CALLS。 | support input捕获生成合同；原协议观察仍evidence_only；`device_flow`扩展delivery.update_spec的具体HTTP/serde/dispatcher路径。 | 将command子链推广为报告中的query、event、WS、requestId/scope/revision关联；当前selected command结果不能宣称覆盖全部协议。 |
| auth工厂返回对象被赋authSession并调用restore。`机器基准对应浏览器组合` | 对象内部client.restore仍依赖注入client，不能直接折叠唯一后端。 | `wwc.client.auth-factory-composition`为evidence_only；现有port_wiring可复用方法，但当前配置针对task。 | createAuthSessionViewModel实际return→authSession→restore→client组合。 |
| Chat有DeliveryCreate、spec、后续WorkItem/WorkRun及重试request身份。`chat-delivery-creator.ts:235–309` | 是看板缺口反证，不证明Chat每次成功。 | 导航记录Chat范围排除，device模块提取verificationCommand反证。 | 完整Chat创建／后续命令顺序、返回ID与重试身份保持；仅保留一个Chat字段反证尚不能复现整条Chat链。 |
| specification authority区分create/update并检查scope/repository/Device baseline/verification command，后续aggregate推进。`delivery_production_adapters.rs:583–654` | optional schema不取消Device条件必填；不说每输入都进入Device。 | `device_flow`对应该报告段和WWC-02。 | 实际命令到authority、字段映射和条件拒绝正在该模块中连接；完整领域aggregate状态机超出该字段模块，原报告也未穷举。 |
| WorkRun.start_next先validate并从持久runs/items求候选，再start_item；start_item再次validate，排依赖未满足与active尝试。`workrun.rs:391–418` | 无候选或验证失败可早退；固有Self不同于任意trait。 | start_next→start_item、start_item→validate两条固定Self调用已reproduced。 | persistent state→候选→依赖／Leased/Running/CandidateReady拒绝的状态和guard摘要；直接call不包含全部状态判断。 |
| remote与managed-session入口共同构造WorkerMain，安装RemoteWorkerPort、ProductionCodexAdapter和workspace runtime。`worker/main.rs` | 配置、短期凭据与lease身份和Server产品状态分开；未运行恢复。 | 原泛型边界有生产main反证来源，仍保持unknown；五模块未建Worker装配判断。 | 两个入口→共同run_worker→具体构造实参／类型→WorkerMain receiver的条件组合。 |
| accept_control按typed message分派；JobDispatch先durable replay，再accept_dispatch；检查workspace/profile/容量、checkout后调用Codex端口。`worker/lib.rs:743–766,2744–2754` | 不同消息或replay选择其它路径；失败拒绝收尾，不宣称所有故障点回收完整。 | accept_control→accept_dispatch已reproduced；generic ensure_thread保留unknown。 | typed variant、replay、实际dispatch guard、checkout及拒绝／收尾顺序；按生产上下文给adapter候选。 |
| `self.codex.ensure_thread`依赖泛型，production main可提供具体候选，但不能全局唯一。`调度消息到Worker` | 不混入测试实现；未知不等于实现缺失。 | `wwc.worker.generic-codex-boundary`保持原预期unknown。 | 有来源的生产构造候选与generic未知并列，而不是消除unknown；该差距不是方法名字匹配。 |
| ProductionCodexAdapter.open建立目录、helper、store/outbox和bridges，然后Kernel::new。`adapter.rs:412–459` | 实际源码接线，不是README推断；未复审所有vendored Kernel或沙箱。 | 定义／调用／源码可查询；五模块不输出此生产open链。 | 构造参数、helper/store准备与Kernel成员的组合关系和早失败条件。 |
| submit_turn核对stage prompt/digest，写SubmissionIntent，persist_run后才exact reconcile。`adapter.rs:3558–3574` | settled、cfg故障点可提前返回；未演练崩溃一致性。 | persist_run固有调用已reproduced；`wwc.codex.intent-before-kernel`仍evidence_only。 | 状态写入→同run_key持久化→settled／cfg返回→Kernel exact调用的顺序与分支。 |
| Kernel.create_session创建线程；submit_turn校验后start/steer；reconcile_turn_exact查durable history，接口不能合并。`kernel/src/lib.rs:1220,1333,1369` | 只是所读Kernel API入口，不是全部内核／工具实现审核。 | 可保存独立定义／调用；五模块不处理该生命周期。 | thread/session/turn参数对应及三个入口的独立行为摘要。 |
| 候选、冻结提交、WorkRun/lease/fencing、角色和evidence source进入合同；adapter有outbox/ack。`证据、候选与外部交付` | 不证明外部日志、bytes、签名和provider结果真实。 | 来源／schema可读；已有局部Rust调用不能替代身份关联。 | 有版本的身份／证据字段映射、活动revision检查和outbox/ack状态关系的自动报告。 |
| Publication/audit/export/connector各有操作键、receipt、持久化职责。`证据、候选与外部交付` | 原报告未逐一审全部副作用adapter，不声称exactly-once、完全防泄漏或全connector完整。 | 目录、manifest、定义可列；当前没有该整类行为分析。 | 先输出模块和未审范围，已有报告并没有要求自动证明所有外部副作用。 |
| Server DeviceModelBoundary unsupported不等于缺模型；Worker安装Device provider并有配置/secret/adapter路径。`Provider的部署分流` | 仅安装／来源确认，不读取真实凭据或证明全部provider可用。 | `wwc.device.production-provider-composition`仍evidence_only。`device_flow`处理spec字段，不是此provider组合。 | Server边界结果与worker.with_device_providers→DeviceModels→provider adapter的实际替代路径自动关联。 |
| docs长期Credential/Provider归Control Plane的绝对说法与当前Device路径存在口径差异。`Provider的部署分流` | 建议按local/Device写清所有权；Provider位置和唯一Kernel不同；不推全部secret安全结论。 | 文档和实现来源可保存；五模块无文档／部署对照。 | 将文档断言和生产部署来源放在同一报告项，表述为限定文档差异，不生成额外安全缺陷。 |
| WWC-01：可见看板新任务seed无delivery，生产callback从当前URL读并返回null，create拒绝；表单不补delivery且显示unavailable/保留草稿。`具体产品接线缺口` | 默认生产port、沿所选看板入口、URL无delivery；manual URL、taskSeed/fake和Chat反证；不用my-work隐藏区证明入口。 | v11导航已有键域／helper返回／callback和端口装配；`navigation_completion`聚合原条件拒绝。 | 将已有局部关系输出为原报告的条件发现，并保留表单输入／失败结果和三个反证。无需将其扩写为一般DOM/CSS或所有UI根安装分析。 |
| WWC-02：clarification完整spec缺verificationCommand，真实client提交；Device authority要求非空字段并拒绝。`具体产品接线缺口` | sourceProductSessionId为Device；local仓库fallback与Chat显式字段反证；criterion展示文本不等于顶层命令，拒绝不等于已存spec被清空。 | 正式规则已有完整构造缺键事实；`device_flow`扩展实际client、传输、字段和Rust条件。 | 将实际命令、字段缺省／映射和条件Err连成报告判断，并保留Device范围、local/Chat反证与授权建议。 |

## 原报告的覆盖与边界也属于输出内容

原报告的覆盖表不会因为某模块能解析而自动变成“已完整分析”。可以自动报告选入／排除文件、语言解析状态、源码与support input身份、应用了哪些分析器、哪些报告项尚无结果；人工报告的“重点深读”“接口盘点”“未逐分支审计”应保留为benchmark的阅读范围，而非系统已经完成的工作。

原报告明确不支持的推断应继续留在报告中：递归／调用环不等于不终止；动态端口／trait未知不等于没有实现；全局覆盖不全导致的否定未知不是负证；不同对象的audit合同不能拼成矛盾；Device unsupported要结合设备侧处理来源；一个创建入口不能代表更新、取消、恢复等其它功能。这些是结论范围，不是为了把unknown转绿而新增的项目缺陷。

未审的全部测试、第三方实现、所有部署／平台、全部HTTP/WS路由、全部安全与崩溃交错仍按原文保留。本文没有要求实现这些超出原报告的证明，也没有要求目标执行、一般JavaScript realm不变或所有隐含UI装配链。

## 按原报告优先级安排复用能力

| 原优先级 | 已有基础／当前工作 | 能直接覆盖的下一批原报告内容 |
| --- | --- | --- |
| P1 语法、定位、固定调用与基准 | v11已恢复相关TS语法和明确Rust Self样本；原3项预期unknown保留。 | 直接纳入报告的来源／覆盖层，并显示剩余解析缺口及候选。无需重复用更大图替代结果。 |
| P1 CPB组合候选与消息关系；WWC明确Self与基准 | `pipeline_flow`的生产队列链，现有port/lexical/source能力。 | CPB命令表候选、queue→inbox→worker；WWC Worker生产装配候选，与原generic未知并存。 |
| P2 五项具体业务判断 | 继续当前pipeline/status/atomicity/navigation/device模块。 | 先完成已经在做的五项原报告发现；它们生成的assembly、field、protocol、guard/order、state事实可复用于主链。 |
| P2 保护和顺序 | generic guard/order关系可复用当前条件返回、状态写入和区域抽取。 | fix readiness先返回；runJob准备／规划／冻结／DAG早退；completion-gate豁免；submit intent→persist→exact reconcile；autoFinalize→persisted result。 |
| P2 工厂、协议和身份 | 复用port_wiring/device中的返回对象、注入、命令及字段映射。 | authSession.restore、Chat后续命令身份、WorkRun active/dependency guard、Device provider安装及部署分流；不要把selected spec命令当全部HTTP/WS协议。 |
| P2 可信命令／证据和收尾 | 字段来源与分支结果摘要，不需执行probe或provider。 | HEAD策略→predicateId→execFile参数；未支持probe失败记录；job与access audit区别；事件→索引、finalizer journal与reconciler。 |
| P3 统计、性能、展示 | 当前快照与缓存事实保持可追溯。 | 在上述报告内容基础上改善检索／变化对比；性能和条目数不作为功能完成替代。 |

## 最小 report generator 结构建议

生成器可以只消费保存快照及分析器输出，按以下数据层组织，不需要重新执行目标，也不需要我批准版本：

1. **benchmark目录**：两份原报告hash、章节／statement位置、原claim、原范围、反证、优先级。本文catalog仅承担这一层。原26基线和5/30台账保留其原有身份，作为可连接的子索引。
2. **自动事实输入**：snapshot/source/policy/tool身份，以及实际由分析器生成的call、候选、assembly、field、protocol、guard/order、state、region/interleaving事实。原报告引用、仅源码片段和分析器推导分别记录来源类型。
3. **报告项**：每项保存 `category`、`benchmark_refs`、`source_refs`、`automatic_evidence_refs`、`scope`、`counterevidence`、`current_conclusion`、`remaining_segments`。某条原句只有人工文字或源码引用时，显示“尚无对应自动判断”；不能把benchmark文字直接填成计算结果。
4. **四类展示**：`findings`呈现具体条件缺口；`architecture_and_chains`呈现已连接结构及权威边界；`coverage_and_unreviewed`呈现来源范围和未分析区；`boundaries`呈现反证、部署条件与不能得出的结论。它们各自反映进展，不用一个5/5或fact count代替整个报告。
5. **变化输出**：同一报告项对比前后结论／范围／证据来源和未连接段。已有源码保护使结论收窄时直接说明；动态未知保留候选和原因。显示的是系统实际生成了什么，不是人工目录被填满多少。

一个初始条目可以是：原 `cpb.finalization.completed-is-not-published`，benchmark给出原句与autoFinalize范围；当前只有旧源码引用则列具体未自动连接段。等guard/order分析生成 `autoFinalize && result.completed → finalizationRequired`、`!ok → failedJobResult` 和实际持久写入关系，再由这些事实生成新结论。这个方式同时适用于五项发现之外的主链，避免后续迭代再次只汇报“0/5与更多局部fact”。
