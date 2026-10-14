# 原五目标的完整静态判断：独立验收计划

> 职责调整记录：用户随后明确以两份完整原分析报告为benchmark，由root负责实现验证，Astra停止批准／gatekeeper工作。本文件保留为此前开发计划，不构成当前批准条件，也不增加原报告未要求的标准。当前工作对应见 [REPORT_ALIGNMENT_NOTES.md](REPORT_ALIGNMENT_NOTES.md)。

日期：2026-10-13。审查者：Astra 独立审查代理。此文件是新开发轮的验收与源码审查计划，不改写原合同或宣布新能力已完成。

**五项判断都可以作为纯静态、有限范围、显式模型下的完整判断来实现。原合同没有要求证明任意 JavaScript／Rust 程序、整个运行环境或某次运行必然成功。当前工作应继续闭合原 30 项必要义务，先完成 CPB-02，再持续其余目标；版本冻结和局部事实增长都不是停止条件。**

这里的“可以”是针对已读源码中有限的指定链路与条件，不是提前认定原五项 claim 必然全部成立。若完整自动证据反驳旧表述，应在新 assessment 中如实报告反证或所需收窄，保留原 claim，不能修改原合同、删去必要分支或伪造支持。

本代理只读目标原文、保存报告与分析器源码，写新审查文档；不执行／导入目标、目标 CLI、测试、构建或安装，也不运行 CallScope 测试。目标仓库 AGENTS 中的 index、bd 与测试命令没有执行，服从用户明确的更高优先级边界。

## 固定验收依据

| 文件 | SHA256 |
| --- | --- |
| [原 GOAL_ACCEPTANCE](../astra-iteration4/GOAL_ACCEPTANCE.md) | `9b6f4fda6aa24f055e288690e76405779e36758f8ba986799f78f2f96aa8d118` |
| [原 5-goal／30-obligation 模板](../astra-iteration4/goal-ledger.template.json) | `d33f48b4f0908458b587e3ad4a97d3b40eb46e3b7eb291d04d053155a5c6ad04` |
| [v11 目标账本](../astra-iteration9/goal-ledger.json) | `65b9f84fb9eba805b2ed16a8336c9f2e48b49169296c8a67ad6e840425abcb89` |
| [原 26 项观察](../astra-baseline/capability-baseline.json) | `16b4b05c8818fa1eecf396132ebe2ea29a8f0068801165f0649da379d9041dd7` |

v11 的 `0/5`、4 supported／20 partial／6 unknown 是开发起点。原 26 项的 10 reproduced／3 unknown／13 evidence_only 继续按旧协议保存；新的完整判断在独立目标账本中判定，不改旧 evidence_only 标签。

## 完整裁决与原 claim 支持的计数

原合同允许“完整静态条件判断已支持”和“原 claim 不成立或需收窄”两种实质结论。可以新增 `complete_assessment` 表达是否已经完成原问题的完整裁决，但必须保留 `full_goal_supported` 的原义，不把两者合并成一个绿色计数。

| 证据状态 | 最终 status | complete_assessment | full_goal_supported |
| --- | --- | --- | --- |
| 原全部必要义务自动闭合，原 claim 在原声明范围成立 | `scoped_static_judgment_reproduced` | true | true |
| 原全部必要义务自动闭合，完整证据推翻原 claim 或确立它需收窄 | `claim_refuted_or_narrowed` | true | false |
| 仅有局部反证，或收窄范围只是绕开未完成必要链 | `claim_refuted_or_narrowed`，并显式标局部 | false | false |
| 必要源码／绑定／模型／传输／guard 尚缺，或来源失效 | 原 partial／unknown 类状态 | false | false |

`complete_assessment=true` 必须同时满足：原五个 goal 和30个 required obligation 的 ID、文本、required 标志不变；该 goal 的每条必要义务都有完整的自动证据证书和明确支持／源码否定结果；必要模型适用检查通过；所有必要分支已纳入；没有影响该义务的未解 gap、坏身份、截断或失效；最终 claim 比较由这些关系推出。完整判断的人工审查可以核验这些事实，不能代替缺失的自动推导。

源码否定不能与无法证明混同。未知动态目标、未建模运输或只知道有 opaque consumer，不是原 claim 错误的证据。若真实源码证明某个所需连接不存在，应有其封闭范围的负证和对后续义务的逻辑影响，不能假装后续成功链已经分析完成。不能通过改 required=false、删除义务或新增未经原合同允许的 N/A 从分母移除它。

报道必须分开写：“完整裁决 x/5，其中支持 y、反驳／需收窄 z；原 claim 完整支持 y/5；必要义务已闭合 n/30，支持、否定、partial、unknown／失效的分布”。其中 x=y+z 只计完整裁决，不能称为原目标支持率。局部 narrowed 不进入 x；原 26 项观察另报，不能与以上计数相加。

## 必要条件与不应新增的障碍

完整验收只要求：必要源码关系被自动连接；所用有限模型已登记并通过其适用性检查；guard／分支／正常与异常完成正确；原反证及真实环境条件保存；所有原 required obligation 都有实质判定。不能要求“所有运行条件都被证明发生”，否则原合同允许的条件性判断永远无法完成。

可声明的有限模型包括标准 ECMAScript 字符串／布尔短路、原生 Set／Array／Promise、普通数据记录／JSON／structuredClone、标准 DOM 导航、所选协议的 JSON／serde 映射、特定 callback 和目录锁协议。模型需版本、适用对象、作用位置及真实限制；相关局部 shadow、已捕获 mutation、替代 callee、未知 alias／spread 或不受保护的写入必须进入检查，不能被一句“标准环境”覆盖。

不必证明整个世界永远没有修改 `Object.prototype` 或 `Promise`。原生接口和正常数据域可以是明确的 `trusted-model` 前提；已有源码中的相反证据不能忽略。JSON.parse 的数据域、实际 literal 的新对象、实际 primitive null 返回等可以建立更窄的适用证据，不宜一律扩大成“任意对象都 plain”。

以下条件不是受信模型：假设中间字段都传播了；假设配置中两个角色就是实际调用者和 callee；假设 callback 确由该实例注入；假设两个同名文件路径是同资源；假设所有 guard／写入都在锁内；假设消息响应就是对应请求；假设未支持 checkpoint 分支与已支持分支相同。它们均需源码关系或独立协议身份。

`author_approved=false` 保留作者审批状态，不能仅凭它否定自动源码事实。尤其 CPB-02 的“两个分类不同且具体 guard 拒绝”不依赖维护者批准修复策略；“应该允许 superseded recovery”则是不同的产品判断，不能擅自推导。

未知应按与 claim 的关系分类：必要关系未知会阻止完整；不在所选正常分支的失败条件、真实环境时序、未声称的运行安全与协议部署可以继续作为边界。不能为了得到绿色而把第一类移入第二类，也不能把第二类无限加入原验收义务。

## CPB-02：最小完整闭合

待支持的具体判断是：在同一合法 job 的当前投影状态为 `superseded`、所选读取与调用正常到达的条件下，materializer 的终态分类包含该值，job-store 的 `isTerminal` 对有 jobId 的该状态返回 false，`recoverAsNewJob` 的相应 guard 在创建 recovery job 之前拒绝。event-store 的所选普通 append 路径仍会拒绝不在 allowlist 的后终态事件；terminal 与 recoverable 的策略不能合并。

“当前投影状态为 superseded”是被分类的业务状态条件，不是允许假设中间传播。分析仍须证明实际 projection return 的 `state`、getJob 返回与 original 参数是同一来源，并证明 `job_superseded` 是该状态的真实生产路径。无需证明所有历史事件最终都保持 superseded。

| 原义务 | 最小自动证据与源码位置（CodePatchBay） | 完整所需的精确结论 |
| --- | --- | --- |
| S1 状态生产 | `event-materializer.ts:270–378` 的新 state／ctx、event loop、`:373` 的 `EVENT_HANDLERS[event.type]?.(state,event,ctx)`；`:420` 的实际 table；`:633–636` 的 handler 参数、`state.status="superseded"`、`ctx.terminal=true`。增量入口 `:381–396` 的 clone、gate、同一 dispatch。事件 jobId／project 在 `:365–366`、`:386–387` 写入同一 state。 | 由事件类型分派到真实 handler，在同一 state allocation 上写入所选状态及 terminal 标记；不能仅匹配字符串或同名方法。源码中的后续 helper／handler effects 不得被空白 purity 假设消除。 |
| S2 定义与谓词 | materializer `:792` 与 job-store `:430` 的实际 Set 初始化；export/import 与 `.has` receiver 声明身份；job-store `:1407–1408` 的 `!job?.jobId || TERMINAL_STATUSES.has(job.status || "")`。 | 对 truthy 合法 jobId＋status superseded 求得 materializer true／job-store false；对无 jobId 求得 isTerminal 的早真，缺失 status 的默认另列。需要实际 receiver 和输入路径，不是两集合文本差。 |
| S3 消费 guard | job-store imports `:7–15`、`getJob :1359–1361`；event-store `readJobProjection :1747–1782`；recover `:1433–1443` 的 runtimeOpts、getJob、original、missing-job 早退及 `!isTerminal(original)`；`:1463` 的 recovery 创建在 guard 后。 | 同一 cpbRoot／project／jobId／runtimeOpts 路径的 projection.state 经 await/return 进入 original；有 jobId 的 superseded 走“not terminal”错误，创建不可达；缺 jobId 先走“not found”，不是误认其可恢复。 |
| S4 权威保护 | event-store `:14–20` 真实导入 materializer Sets；`appendEvent :1179–1243` 的 stream identity binding、eventFile、withEventLock callback、same-job readEvents→materializeJob；`:1194–1196` 的 `terminal && !allowlist` 早 return；`:1237` append 与外层 written 返回。 | 在所选普通 append 路径，当前状态 superseded＋事件类型不在 allowlist 时，callback 返回 null，常规 append 不可达。保留 allowlist 分支、无 existing 事件分支、锁/读取失败及其它 journal API，不推广为任何业务状态永不能变化。 |
| S5 政策与结论 | `isRecoverable :1411–1414` 独立先调用 isTerminal、排除 completed、检查 failed/blocked/cancelled；recover 本身的实际两个 guard；原 claim／范围／反证一并引用。 | 报告 terminal 分类差异与实际 consumer 影响，明确“修正 terminal 集合并不等于承诺开放 recovery”；不要求不同用途的所有集合全等。作者审批标志不被改成 true。 |

S1 的真实生产调用还可保存 `review-dispatch.ts:4468–4470` FIXED→markJobSuperseded、`:4485–4492` 构造含 jobId/project 的事件、`:4339–4343` 真正 appendEvent 别名调用作为额外入口证据。原义务的最小核心是事件入口／dispatch／state 身份；不要把必须证明全部 remediation 或远端发布发生额外加入 S1。

### projection 分支的必要精度

`readJobProjection` 无 checkpoint 分支返回 `state: materializeJob(events)`（`:1756–1761`）；有 checkpoint 分支 clone checkpoint.state，逐事件 advance，最后返回 `state: replayed`（`:1764–1782`）。两正常 return 的字段来源必须保存；不能只提取一个匹配的 return 就标整个 getJob 来源闭合。

最小 CPB-02 结论不要求两个分支的整个对象被证明相等：可以分别记录所返回状态的来源，以当前合法 projection.status 为分类输入。若实现进一步借 `sameCheckpointState` 恢复“replayed 与 full materialization 完全相同”的事实，应注意 `event-store.ts:362–367` 实际比较 SHA256(serializeEvent(state))，不是对象相等。此时需要显式内容完整性模型；没有使用该推理时，不新增抗碰撞证明义务。

合法 job 身份的来源可由 `eventFileFor :708–720` 的路径参数、`readEvents :1561–1564`、`parseEventJsonl :1267–1283` 的 JSON 解析与 persisted identity guard 关联。不能把任意手工传入的异构事件集合默认为该 stream。外部文件读取成功、正常 JSON 和所选数据根一致可以是环境／协议条件；实际参数与路径组成仍由源码得出。

### 两个必须自动保留的反例

第一，POST_TERMINAL_ALLOWED 不是“只读事件集合”。`event-materializer.ts:200` 包含 `approval_required`、`job_approved`、`approval_timed_out`；`:638–656` 的 handlers 实际会改 status。不能把“曾有 job_superseded”直接传播为所有后续读取永远 superseded，也不能将 S4 描述为不可突破的全局终态封印。

第二，isTerminal(null／无 jobId) 的返回是 true；但 recover 在调用它之前检查 original.jobId 并抛 not found。truth table 与 consumer 路径必须同时保存，不能用单一谓词返回值伪造 recovery 行为。

### 最小通用实现能力

所需能力不是为 CPB-02 写死一句判断，而是：真实词法／导入身份；有限字符串集合与 `.has`；普通数据记录的字段读写／投影／clone；有界 dispatch-table 选择及参数绑定；normal return／await 返回连接；布尔短路与 if throw/return 的控制效果；callback 参数转发与普通 append 的局部顺序；按关系 ID 组合的五个 obligation witness。

业务 token `superseded`、`status`、`jobId` 与源码角色可以来自声明的合同；handler 名、Set 实际成员、参数索引、return operand、guard 方向、append 前后关系、反例与最终 true/false 不应来自政策预填。未支持的结构要留下 gap 阻止相应 complete，不能靠“若干 selector 均找到”计算完成。

## 其余四目标的最小完整工作

| 目标／原义务 | 仍需自动闭合的内容 | 可接受的显式边界与不能省略的反证 |
| --- | --- | --- |
| CPB-01 P1–P2 | flags 初始化、`parseInt(...) || 3`、返回 binding→parsed→metadata.maxRetries；默认 enqueue 的动态 ESM 路径来源；queue／scheduler／assignment／worker direct/broker 的真实生产装配。已读 `pipeline.ts:69–70,183–205`。 | 可声明使用所选正常生产 executorRoot 和标准 ESM，但必须从真实 root/path/export 得到目标；不能把配置角色当实际 binding。零被默认不自动成为新缺陷。 |
| CPB-01 P3–P4 | normalization、new/existing queue、candidate／assignment、消息身份／JSON、worker.metadata；非 finalizer-only 新对象 maxRetries=3→bridge→engine→所选读取。`hub-queue.ts:1595–1620` 的复用/新建分开；`managed-worker.ts:1784–1809` 是分支及新对象，不是原 metadata 上的覆盖。 | 普通数据／JSON／Promise／协议可以是受信模型，但字段关系、分支与消息对应必须推导。请求值本来为3、复用旧pending、finalizer-only均保存。 |
| CPB-01 P5–P6 | 对每种声称相关预算记录 owner、实际计数、默认、guard 和使用路径。`failure-router.ts:103–113,265–277` 的 attempts/MAX_RETRIES 与 supervisor；其它 phase、DAG/node、verification infra 各自独立。 | FailureRouter 的早 return 可能绕过一般预算 guard；opaque supervisor 不能成为“全程序从未消费 metadata”的负证。可完整给出明确预算合同在限定路径的符合／不符合判断；不能只用局部常量3宣称整个 pipeline 无 retry。 |
| CPB-03 A1–A3 | `fix.resolveDeps :426–451` 中 ctx.deps 覆盖/default import→run 的实际 deps；`:520–540` 同project、hash key、非terminal选择和早退；hubRoot→queuePath／真实 load-save 资源连接。 | 默认无覆盖、两请求同逻辑queue可作为真实范围；不能假设资源接线。原 `idempotency.ts:6–16` 的同key全部非terminal不变量继续单独标policy/source来源。 |
| CPB-03 A4–A6 | 已有 callback lock region 保留；writer `hub-queue.ts:1595–1620` pending＋复合key查重／复用／push／commit；`hub-orchestrator.ts:333–356` 实际 updateEntry、scheduled patch、pending/version guard、leader/capacity/rollback来源。 | 目录锁／原子文件语义可声明，不必证明文件系统在这次运行成功；实际 callback 与操作范围不可跳过。不能报告无锁或无二次查重。 |
| CPB-03 A7 | 从提取的操作、谓词、read/write集、保护区、状态转换构造有限调度，自动找出满足guard的交错及两commit后的不变量反例。 | 用户报告中的A/B步骤不能直接作为“求得”的见证。预查已见active、writer仍pending同key、scheduler被guard阻止、rollback和commit失败等反例保留。存在性条件风险不需证明所有双提交都重复。 |
| WWC-01 N1–N3 | `home-dashboard-page.ts:359–370,636` 的实际 a 元素、href、append到layout；import到surfaceHash／scopeHash；已有有限URL查询键域继续使用。 | 不需证明像素可见性或浏览器运行成功；要有真实DOM组合并排除所选节点被代码明确隐藏。已有query保留、四scope键仅possible而非guaranteed，仍不能改写。 |
| WWC-01 N4–N5 | normal boot无taskSeed→`application.ts:277–310`真实factory分支／deliveryContext闭包属性；返回create方法→taskPort→VM；ambient hash→get(delivery)→null返回→`community-control-plane-client.ts:2791–2793` await后throw→HTTP不可达。`task-entry-view-model.ts:284–333` 的表单gate与port.create应连接。 | 原生 Promise 对primitive null传播可以明确建模，无需证明任意对象thenable安全。普通实例/闭包稳定的受信边界需明确；源码中的替代注入或写入不能忽略。 |
| WWC-01 N6–N7 | 从实际anchor选择与路由handler到本次form/VM的源码连接；导航到ambient hash是独立环境边；提交前hash未变及表单满足作为真实条件；fake/有效delivery seed/Chat反证连接。 | href→browser.location.hash的真实导航时序不必静态证明发生，但未实现boot/callback/return或事件绑定不能伪装成这项环境条件。结论止于所选正常入口、HTTP之前的条件拒绝。 |
| WWC-02 D1–D2 | `clarificationUpdateCommand :190–221` 完整spec缺键；`:240–244` 命令值→options.client.command；`application.ts:1421–1456`动态import、真实port/VM/client装配；表单submit→model.submit。 | 显示criterion.verificationMethod不是顶层字段。作者实际生产client wrappers必须逐段或经可验证通用转发摘要连接，不能按`.command`同名拼接。 |
| WWC-02 D3 | 所选 command/version/envelope/payload identity、JSON缺省、generated TypeScript/Rust schema字段映射、serde deserialize、dispatcher family/command arm→实际authority。 | 标准JSON/serde可作为版本化协议模型；需实际schema/rename/default证据。跨语言使用协议关系，不伪造CALLS。不能仅保存generated原文而声称已解释其语义。 |
| WWC-02 D4–D5 | `delivery_production_adapters.rs:583–647`真实LocalDeliveryAuthority，create/update的payload.spec，scope/repository校验、Device分支、baseline guard、Option.filter(trim非空).ok_or_else?的提前Err；非Device fallback、Chat显式字段与授权/确认条件。 | “当前Device有效、请求通过更早权限与revision guard”可作为真实条件，不需证明每次UI都选Device；actual dispatcher/authority binding不能假设。无Device的`:638–641` fallback不受同一缺键结论影响。 |

对五项均不新增“全程序无任何未知”的验收条件；要求的是每条原必要链完整，scope 外的不确定性准确列示。CPB-01 与 CPB-03 工作量较大，有限协议与状态域可共享，但不能把新状态模块的成功当作其它目标的完成。

## 对实现代理的可执行审查要求

CPB-02 `status_analysis.py`：提供按 S1–S5 分开的 witness 与 precise truth/guard outcomes；每个 supported 位必须能追到关系 ID、source span、真实 binding 和已登记模型。单独展示 checkpoint 分支与allowlist反例。反事实源码若换Set receiver、删jobId guard、反转if、改dispatch目标或把append移到早退之前，应由结构/关系检查失配而降级；无需执行这些反事实或运行测试。

CPB-01 `pipeline_flow.py`：先保存端到端两类身份——值/记录来源与queue/assignment/inbox/attempt消息身份；再对当前有效消费者和独立预算推导。禁止将 `metadata.maxRetries` 的沿途文本命中当作传输证明。新/existing、direct/broker、finalizer/execute和opaque supervisor的表必须完整。

WWC-01 代理：保留 v11 已闭合键域，补真实可见节点组合、路由事件、boot→factory→VM、async null→guard；不要为所有对象的可变性无限后退到unknown，也不要因“正常环境”忽略已捕获的替代实例。

WWC-02 `device_flow.py`：分别提交生产注入、客户端wrapper转发、协议mapping、具体Rust authority和条件Err五类关系。每段以实际AST实参/返回/属性/分派为依据，不能将一组源码片段都存在等同跨语言链成立。辅助协议原文的捕获身份与解释器能力分别记录。

CPB-03 代理／root：在既有region/predicate基础上加入default deps、具体资源和可执行的有限状态转换规则，再计算交错。配置可声明不变量和锁语义，不能输入答案步骤。保留原inner pending查重作为反证，不能弱化它来得到风险。

统一输出应提供：旧goal/obligation ID；声明范围与模型；自动关系及source snapshot/hash/owner/span；各分支的normal/abrupt outcome；完整计数/截断位；每个必要gap及其关联义务；组合算法实际得到的结论；原反证与policy审批状态。`complete` 不能等于选择器数量满足、字段名集合满足或硬编码五个true。

## 持续验收顺序

先独立读 CPB-02 实现与它的正常保存源码查询，核对上述最小链和反例；满足 S1–S5 后生成原目标的第一项完整自动判断并复核真实两库产物。保留其余四项未完成状态，但继续实现，不把该阶段发布当任务终点。

随后按可复用能力推进导航与Device协议闭合，再完成完整队列参数/预算链及状态交错；并行代理可以提前工作。每次只更新新一轮能力/目标产物，原合同、旧报告和26项历史基线不变。最后对原5/30逐项复核所有必要关系；若有源反证，则明确裁决，不用“下一版本再做”替代用户要求的持续完成。

本文件尚未将任何 v11 partial/unknown 升级。升级依据必须是新实现的自动事实与独立验收，不是本计划中人工已读到的源码。

## 本次 CPB-02 原始来源身份

| 目标文件（相对 CodePatchBay） | SHA256 |
| --- | --- |
| `server/services/event/event-materializer.ts` | `b996cee994fe63b138a41e3805319d73de5ff21ff902090993324739ee69c993` |
| `server/services/event/event-store.ts` | `9323053b0a49589604dc8b568a4448feb53d68f8d8cf1411c56dca8ef01da750` |
| `server/services/job/job-store.ts` | `1b18f79636c4c4078eda53a7df8fa92236357b4afef41bc9372b7d2034e707d7` |
| `server/services/review/review-dispatch.ts` | `24405468ce46d08b50b14f541511a0f85f99f9e06c8b61cd6cbeef2c395adba9` |
| `core/workflow/dag-executor.ts` | `2a7f96ab1714ccc51a5e4edd64a2c37079f3d00aa580d7b55e6a2e14b3e9255b` |

其它四目标的表中位置同样来自本次实际读取，涉及 pipeline/fix/hub-queue/hub-orchestrator/failure-router/managed-worker/idempotency，以及 home-dashboard/application/task-entry/community-client/clarification/Device authority；这些阅读只用于设计独立检查，不代替新自动证据。
