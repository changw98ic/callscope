# CPB 预算消费者与不同预算：只读来源准备

日期：2026-10-12。状态：源码准备，尚不是v0.9正式分析结果。

本稿只读取目标原文并使用固定Tree-sitter语法库保存原始字节SHA256、AST区间、词法owner和声明／调用出处。[机器来源包](budget-source-observations.json)包含13份原源码、24项人工选择观察、89个去重AST锚点；所选原语法树均未报告parse error。没有导入、执行、测试或构建目标，没有导入CallScope核心或运行预算检测器，`automatic_budget_analysis_results=0`。语法可解析不证明预算语义、函数执行或功能正确。

原[五项判断／30义务合同](../astra-iteration4/GOAL_ACCEPTANCE.md)保持冻结。本稿为CPB-01.P5提供真实消费者及反证来源；不按`rg`缺少`maxRetries`判定全程序没有消费，也不知道CLI `--retries`应控制哪一个预算。规则／意图未经目标维护者批准，`author_approved=false`；不能强迫不同预算共享一个值。

## 1. 可交给分析器的实际选择器

| 预算类别 | 文件／实际词法符号 | counter与limit | guard／循环来源 |
| --- | --- | --- | --- |
| queue assignment attempt | `server/orchestrator/failure-router.ts#FailureRouter.route` | `attemptCount`来自`assignmentRecord.attempts`；`maxRetries`来自`MAX_RETRIES[failureKind] ?? 0` | `:265`的`attemptCount > maxRetries`，该分支返回`mark_failed` |
| phase总重试计数 | `core/engine/phase-retry.ts#runPhaseRetryLoops` | `phaseRetryCount=0`；`phaseRetryTotalMax=Math.max(0,deps.phaseRetryTotalMax ?? configuredPhaseRetryTotalMax(env))` | guard在嵌套async箭头`runPhaseRetryLoops.prepareRecovery:396`，为`phaseRetryCount >= phaseRetryTotalMax`；四个外层增量另列 |
| verification infrastructure retry | `core/engine/run-job-execute-dag.ts#runVerificationInfrastructureRetryLoop` | `iteration`与局部`maxRetries` | `:1004`的`for (let iteration=1; iteration <= maxRetries; iteration += 1)` |

预算准备策略仅选实际owner和counter／limit名称，不预填阈值、比较符、递增、消费者连接或完整判断。当前[CPB policy](codepatchbay-policy.json)只新增`cpb-phase-retry-local-budget`和`cpb-verification-infra-local-budget`两个局部模式；其subject、名称与原AST一致，均声明conditional且作者审批为false。queue跨记录计数与scope复杂，不被这两个规则自动包含。

机器包中的名称是原AST词法owner；原始字节区间和hash用于定位。它们不是CallScope已认证的CALLS／binding，不代表目标类型检查或实际部署身份。

## 2. queue：真实attempt guard及实际递增候选

`FailureRouter.route:105–112`先将assignment经`recordValue`投影为`assignmentRecord`；`:111`读取`typeof assignmentRecord.attempts === 'number' ? assignmentRecord.attempts : 0`。`:112`按failure kind查本文件的`MAX_RETRIES`，缺项默认0。`typeof number`本身不证明有限、非负整数；不能把来源语法换成已验证的运行计数。

`MAX_RETRIES:7–18`的全部10项由机器包读取：runtime_interrupted=2、timeout=1、`FailureKind.PLAN_BOUNDED_HANDOFF_TIMEOUT`=2、agent_contract_invalid=1、`FailureKind.PERMISSION_DENIED`=1、worker_crashed=2、worker_heartbeat_lost=2、assignment_progress_stale=2、agent_rate_limited=0、verification_failed=2。两个computed成员保留原语法；其静态候选来源是`core/contracts/failure.ts:1`的`FailureKind`声明与`:8/17`等原成员，不在准备器中求值导入模块。Object.freeze／key映射的模型适用性应由正式分析认证。

`:265–273`当`attemptCount > maxRetries`返回`action:'mark_failed'`、`retryable:false`；reason还显示`maxRetries+1`。真实store在首次attempt由0加1，因此“额外retry数”和“已启动attempt序号”不能直接当同一种计数；是否符合项目意图仍需独立合同。

**该guard不覆盖整个route。** 原函数在其之前有7个直接return，位于`:183/193/207/228/238/247/255`，包括非retryable停止、rate-limit等待和checklist routing的`retryDecision(...)`。源码顺序表明这些分支可在到达guard前返回；不能宣称所有retry动作被此guard支配，也不能据此报业务bug。其它phase或策略预算可能负责这些分支，未经批准的“统一预算”不能作判错依据。

实际attempt增量有两种构造：

| 位置 | 真实源码关系 | 尚未闭合 |
| --- | --- | --- |
| `AssignmentStore.createAttempt:553–587` | `previousAttempts`从读取state取值或0；`:558`加1；`:579`写`state.attempts=attemptNum`，`:584`await `_writeState`；代码位于`_withAssignmentLock`的async callback中 | callback激活、store receiver、对应assignment／attempt身份、持久化成功和route读回 |
| `AssignmentStore.enqueueWithReceipt:590–698` | existing state取previousAttempts或0；`:634`加1；`:649`在新state构造`attempts:attemptNum`；committed state随后写入并返回receipt | new/existing记录、JSON规范化、commit／restore、当前实际运行入口；这是新对象构造，不是上一行的同对象字段写 |

`getAssignment:1299`经`_readState`读取，`listAssignments:1333`遍历并返回state；`_writeState:1354`写本store目录下的`state.json`。`Reconciler.reconcileAssignments:1224`调用`this.assignments.listAssignments()`，`_finalizeQueue:1801`将assignment／attempt／conditional effectiveResult交给`this.failureRouter.route`。这些是生产读取／使用候选；路径相同拼写不认证同一物理记录、当前版本、class receiver或实际调用。

`HubOrchestrator`构造器`:181`创建FailureRouter并注入Reconciler，`:381`调用store的createAttempt。配置／constructor候选、动态store对象与真正分派要分开。`FailureRouter.resetBudget`为无操作方法，注释说明预算取自assignment.attempts；不产生显式counter清零事实。

**opaque反证不删除。** route`:277`将完整assignment／attempt／result传给可注入supervisor；候选`AcpSupervisor.diagnoseFailure:230`又构造prompt、调用pool.execute及saveDecision。准备器不执行pool／LLM／provider，不证明其所有消费，也不因局部MAX_RETRIES存在就宣布metadata不可能被其它路径读取。

## 3. phase：嵌套总额guard、四个增量及子预算

`runPhaseRetryLoops:364–378`取得env，分别构造transient、feedback、quality三个子预算和总额，初始化局部`phaseRetryCount=0`。总额默认链为：

`retryEnv(n)` → `n.env ?? process.env`；`configuredPhaseRetryTotalMax(env):121` → `numericEnv(env,'CPB_PHASE_RETRY_TOTAL_MAX',FALLBACK_PHASE_RETRY_TOTAL_MAX)`；fallback常量为3。

`numericEnv:98–103`对undefined／空字符串返回fallback，否则用Number并以Number.isFinite决定返回或fallback。此源码没有integer检查。deps提供值时可绕过该helper，总额外层只有Math.max(0,...)；不自动证明deps值有效、环境标准接口未被替换或实际执行得到哪一个数字。

`prepareRecovery:389–450`是捕获外层counter／limit的async箭头。`:396`到达耗尽条件时先await appendRuntimeEvent，保存`stop_retry_budget_exhausted/retryCount/maxRetries`，随后return null；event append也可能抛错。该helper还有“不改变失败策略”的停止条件。正式分析需连接真实闭包声明、调用点、await返回及`!prepared`控制，而不是按同名counter把guard接到所有增量。

| 分支 | prepareRecovery来源 | counter递增 | 后续实际源码调用 |
| --- | --- | --- | --- |
| agent fallback | `:487`，未prepared则return result | `:530` | abort检查后`:532`调用注入的runPhase |
| quality interception | `:547`，未prepared则break | `:575` | abort检查后`:577`runPhase |
| transient failure | `:590`，未prepared则break | `:619`，在delay之后 | abort检查后`:621`runPhase |
| contract feedback | `:629`，未prepared则break | `:663` | abort检查后`:665`runPhase |

这些增量在runPhase之前，不能直接解释为“已完成一次执行”。append／progress／delay／abort／注入callee的失败或未完成是必要限制；中途return也可能跳过最终diagnostics。`:670–681`仅当count大于0时将其写进result.diagnostics，不是动态trace。

各个for循环还受自己的phaseRetryMax、phaseQualityRepairMax、phaseFeedbackRetryMax、isPhasePassed、failure kind和允许actor条件控制；总counter还包括不属于for循环的fallback一次。总预算与各子预算不应按类似名字或数字3自动合并。

真实调用候选`run-job-execute-dag.ts#applyPhaseRetryLoops:437`传入ctx、phase state以及`{runPhase:runPhase}`，phase env来自`ctx.env`；这是局部生产装配来源，不证明CLI metadata.maxRetries控制总额或当前phase确实运行。

## 4. verification infrastructure：有限for及严格numeric helper来源

`runVerificationRepairLoop:849–855`只在recoverable infrastructure failure分支选择`runVerificationInfrastructureRetryLoop`；其它repair路径使用不同预算。选中函数`:996`还在没有initial result时提前finish。

`:998`的局部maxRetries由静态导入`solver-loop.ts#verificationInfrastructureRetryLimit:366`取得，实参为`session.ctx.env ?? process.env`。helper原文为Number(env.CPB_VERIFICATION_INFRA_RETRY_MAX ?? 2)，非integer或负数返回2，否则Math.min(value,10)。这是可供固定Number／Math模型消费的来源语法；本稿没有执行helper或认证实际内建／env对象。

外层`:1004`for的initializer／condition／increment均有单独AST锚点：`let iteration=1`、`iteration <= maxRetries`、`iteration += 1`。它是初次失败之后的重试loop，不能把iteration1当整个job第一次执行。内部还遍历retryNodes，并可能：terminal早退、candidate drift停止、成功返回null、non-recoverable失败转向`runVerificationRepairLoop`。runDagNode／appendEvent和恢复前缀并不因有限header而证明激活、完成、全部iteration发生或资源正确。

`:1116`exhausted事件和`:1131`failure cause都写`retryAttempts:maxRetries`；该来源是limit，不是已经观测到的实际iteration次数。退出分支、抛错和初始失败条件不能隐藏。

`solverRepairLimit`和`completionGateRepairLimit`读取另外的CPB_SOLVER_REPAIR_MAX／CPB_COMPLETION_GATE_REPAIR_MAX，各有默认及上限；与verification infrastructure不同。queue attempt、phase total、solver repair、completion gate和基础设施预算可以合法承担不同职责，需明确意图才能检查彼此关系。

## 5. 对P5能提供什么，仍缺什么

这些原文提供真实的预算读取、局部比较、数值helper源码、counter写／增量、不同budget及opaque消费者反证，可以支持未来两个有限局部模式的实现与证据审阅。它们不证明P5已经自动满足，更不完成P3／P4的运输与消费链。

完整P5仍需：自动认证helper／receiver／闭包来源，连接guard与计数作用域、早退／phase条件及真正消费者，区分count与实际attempt／iteration，保存正常／异常和opaque范围，并明确CLI选项应控制哪个预算。未经目标作者批准的意图只能作policy声明，不能预填执行结果或要求所有budget相等。

`pipeline.ts:205`的metadata.maxRetries来源形式为parsed.retries，`managed-worker.ts:1809`另一个新参数对象写3；请求也可能是3。它们是两处独立源码形式，未证明同对象覆盖、记录／消息运输或与上述局部预算的语义关联。不能从搜索没有更多同名读取推导全程序未消费。

本轮七份现行文档与旧目标账本不修改。正式v0.9报告／新账本须从最终保存事实重新绑定原5项／30义务，并将人工准备与自动结果分开。功能闭环及来源正确性优先，可扩展性其次，性能最后；不增加目标执行／测试／构建。

## 6. 原始源码身份

逐文件读取稳定，不提供全工作区原子快照。正式新扫描应重新绑定保存文本／hash及分析组件身份；不能用本准备稿替代正式快照。

| 相对文件 | 原始字节SHA256 |
| --- | --- |
| server/orchestrator/failure-router.ts | `8abe3a09afcf48aa46b9380f9955e6c9e3e0411c1b02a29a9d2b4f1d721ea1a9` |
| shared/orchestrator/assignment-store.ts | `eb703d0845fd8aee1a97beddcb3c9f0502c7e6d912ec058a8e5110d08999ac48` |
| core/engine/phase-retry.ts | `9a5b5b06fb5e120f3708e3999e90a14e8bdf05334828e930a7f92eaa18d7083c` |
| core/engine/run-job-execute-dag.ts | `5fb852088e425a0e3bf1f1bd2db5b3682fe61f031f01b213fc9a0d08b908bd14` |
| core/engine/solver-loop.ts | `183d1b34f3b90d0ed935033b5e686d2e5d43f74e44741178b376496ddf1f9960` |
| core/contracts/failure.ts | `6e63812a626139813e108915c3fdcd2041a3160d6bd63e8c6c0dd00d4d442b5b` |
| shared/types.ts | `d44aac646eaa445967f33ad8690be01cc360abfd6b6f38e515a0f843ba8ef64e` |
| core/contracts/types.ts | `ee66ca21501d2056692f2a3cc70358d77dc536014fb09a25bc7a118f9b4140bf` |
| server/orchestrator/reconciler.ts | `ea876d11e67ec111c5a588cdf1cec90e31ba5339a3a0d109f2c616c81cb661c9` |
| server/orchestrator/hub-orchestrator.ts | `41e248486eeae6f36b8f66b87df56a466bb1d4c5cb86d4c09066012e170f8454` |
| server/orchestrator/acp-supervisor.ts | `5fa7fefb8a376e0d87a9f1dbebf079db7f11f0db84f418df29cd5cbcb6e6b3ba` |
| cli/commands/pipeline.ts | `3df3f333ec4668352efde20049494c4a85bdf13049c808cd9f89f2d82f30b4ed` |
| runtime/worker/managed-worker.ts | `75cdd41a20c71a7f0c7c500080ab7743417f932d35e4179a031b822831c633ca` |
