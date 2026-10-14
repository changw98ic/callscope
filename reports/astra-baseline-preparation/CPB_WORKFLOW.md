# CodePatchBay 工作流源码来源稿

供 Astra 独立审查使用。来源为只读的 `/workspace/codepatchbay` 生产源码；未执行目标命令、依赖安装、构建或测试。本稿整理源码连接、条件、契约与反证，不把人工阅读结论冒充 CallScope 已自动检测的发现。

已有 v3 快照为 `4376321a4081901f9a62e74b6a9a1cbedfacf1a2f2d68278ac2bbdf6ce3d8db2`，分析器 `static-multilang-3`，检测器 `call-rules-3-axon`。扫描范围 333 份文件、327 份解析成功，状态 `partial`；详见 [扫描说明](../upstream-reuse/UPSTREAM_REUSE_SCAN.md) 与 [精简结果](../upstream-reuse/codepatchbay-summary.json)。本稿不是整个仓库功能完整性的证明。

## 工作流入口与实际流转

| 阶段 | 符号与来源 | 源码可支持的静态结论 | 当前调用图的边界 |
|---|---|---|---|
| CLI 分派 | [cli/cpb.main](/workspace/codepatchbay/cli/cpb.ts:127)，动态加载 `:154`，`mod.run` 在 `:186` | `COMMANDS` 选择命令模块，然后调用该模块的 `run` | 计算路径的动态 import、命名空间属性调用未绑定为确定命令目标 |
| 用户修复提交 | [fix.run](/workspace/codepatchbay/cli/commands/fix.ts:469) | 空问题/缺项目返回；readiness `:505` 失败在 `:508` 返回；活动同键任务 `:528` 被复用；最后在 `:576` 入队 | `deps.assertFixReadiness`、`deps.enqueue` 等依赖来自动态导入/注入，不是直接本地调用边 |
| 提交依赖 | [fix.resolveDeps](/workspace/codepatchbay/cli/commands/fix.ts:426) | `:434` 并行 import readiness/queue/registry/task-view/auto-route；`ctx.deps` 可以覆盖默认实现 | 只知道词法对象属性不足以证明运行时实现或必然执行顺序 |
| 持久入队 | [hub-queue.enqueue](/workspace/codepatchbay/server/services/hub/hub-queue.ts:1550) | 标准化 project/sourcePath/ACP 配置；`withQueueMutation` 在 `:1595` 包住当前队列的查重与添加；队列入口创建为 pending | 这是文件/状态协议，跨进程的生产者与消费者不通过函数调用直接相连 |
| 候选调度 | [Scheduler.nextCandidates](/workspace/codepatchbay/server/orchestrator/scheduler.ts:285) | 待重试时间、队列 dependsOn、项目 readiness、项目并发、provider 容量过滤；按 smart 或优先级/时间排序，再保留容量 | `this` 方法、注入 providerCapacityFn 等尚未确定绑定；queue dependsOn 不等于 core 内部 DAG |
| 分配与预约 | [HubOrchestrator.tick 主体](/workspace/codepatchbay/server/orchestrator/hub-orchestrator.ts:315) | 先 reconcile，再 nextCandidates；`updateEntry :342` 按 pending+updatedAt 预约；创建 assignment/attempt 后先预约 worker，再 `writeInbox :417` | 领导租约、CAS、持久 inbox 和跨组件状态不是单条 CALLS 的功能证明 |
| worker 启动 | [WorkerSupervisor.ensureWorkerFor](/workspace/codepatchbay/server/orchestrator/worker-supervisor.ts:51)，[startWorker](/workspace/codepatchbay/server/orchestrator/worker-supervisor.ts:58) | 可复用 ready/starting worker；新 worker 先登记 incarnation/能力凭据，再 `:89` spawn managed-worker.js | 目标进程入口未作为确定本地调用边；源码的 spawn 不是本次执行了进程 |
| inbox 消费 | [managed-worker.processInbox](/workspace/codepatchbay/runtime/worker/managed-worker.ts:1393) | `:1394` claimInboxEntries；校验 attempt/token/runtimeRoot 等；普通执行在 `:1797` 调 engine bridge | 扁平 assignment JSON、租约和回调字段需要协议/绑定建模 |
| runtime bridge | [engine-bridge.runJobWithServices](/workspace/codepatchbay/bridges/engine-bridge.ts:17) | 直接转调用 server-owned `runJobWithServerServices`；runtime 不自行实现服务注入 | worker 在 `managed-worker.ts:1349` 动态导入 bridge，不能因此要求图提供完整 worker→server 静态路径 |
| 服务与核心 | [engine-runner.runJobWithServices](/workspace/codepatchbay/server/services/engine-runner.ts:130)，调用 `runJob :157` | 解析项目 source/runtimeRoot，缺 runtimeRoot 抛错；构造环境、服务端口、进度与子进程注册钩子，再调用核心 | broker 与本地持久化是不同端口分支；路径存在不能证明参数值/有效性 |

核心中“不从 core 导入 server”的声明位于 [run-job.ts 开头](/workspace/codepatchbay/core/engine/run-job.ts:6)，描述源码依赖方向。它不禁止运行时经过注入端口调用 server-owned 能力，不能改写成 `forbidden_path core → server`。

## 核心执行、依赖和条件返回

[runJob](/workspace/codepatchbay/core/engine/run-job.ts:65) 校验 context 为 object，调用 `runJobInner :75`，外层在成功/失败/blocked 返回和 panic 后都尝试 audit finalization。`isRecord` 不能验证所有服务成员，源码在此明确保留动态边界。audit 是 best effort，不能宣称每次日志必然持久成功。

`runJobInner` 的源码顺序为：

1. 构造环境、合并阶段超时。
2. `createJobAndHandleBlocked :121`；blocked 即返回。
3. `prepareTaskAndRiskMap :146`；blocked 即返回。
4. `runHighAssurancePlanning :152`；除 ok/skipped 外返回结果。
5. `freezeChecklistAndMaterializeDag :159`；blocked/failed 即返回。
6. 可选 `forceFreshSession` 清理，然后 `executeWorkflowDag :177`。

这些直接调用及相邻 return 可以支持局部控制流论断；当前 CALLS 图自身不编码分支谓词与语句先后，也不能仅因五条路径均存在证明 fail-closed。

[freezeChecklistAndMaterializeDag](/workspace/codepatchbay/core/engine/run-job-checklist-dag.ts:131) 将来源 checklist/要求分类、规划结果和风险图输入冻结与覆盖校验。可定位连接包括 `validateAcceptanceChecklist :229`、`validateChecklistSourceCoverage :243`、`buildWorkflowDag :356`、`validateChecklistDagCoverage :378`、`dagSequentialExecutionPlan :391`、resume context `:392`，以及 `validateDynamicAgentPlan :483`。动态计划失败在 `:497` 阻断、`:515` 返回。`CPB_CHECKLIST_DECOMPOSE`、预先存在 checklist、已 aborted signal 与独立验证要求会影响分支，不能用默认路径替代所有配置。

[executeWorkflowDag](/workspace/codepatchbay/core/engine/run-job-execute-dag.ts:1783) 使用 completed/executed 集合调度，而不是按“任意可达”执行节点：

- [stableReadyNodes :1219](/workspace/codepatchbay/core/engine/run-job-execute-dag.ts:1219) 只接受所有 dependsOn 已完成的节点。
- [pickExecutionBatch :1235](/workspace/codepatchbay/core/engine/run-job-execute-dag.ts:1235) 遵守容量/冲突集合；[isParallelNodeCandidate :1189](/workspace/codepatchbay/core/engine/run-job-execute-dag.ts:1189) 仅允许受支持的 read-only review，custom/side-effecting/resume 节点排除。其他阶段仍顺序执行。
- `:1901` 无 ready nodes 时，`:1917` 失败任务并返回，避免依赖缺口只表现为无限等待。
- 并发 wave 在 `:1928` 运行隔离 session，缓冲副作用；顺序分支在 `:2036` 调 `runDagNode`。
- 终态失败取消未执行节点；deferred verification 在 `:2058` 进入修复路径；所有节点完成后 `:2066` 调 completion repair/gate。

单节点可见主链为 `runDagNode :695 → runDagNodeAttempt :582 → preflightAndRunPhase :308 → runPhase :333`，并含 provider fallback 与 phase retries。收尾在 [finalizeDagNodeOutcome :492](/workspace/codepatchbay/core/engine/run-job-execute-dag.ts:492) 先 scope guard `:508`，再 `finalizePhaseResult :531`，最后按 passed/deferred verification/failed 分支落地。scope guard 的 return 先于后续成功收尾，不能因 graph path 包含 success 节点就判断越过 guard。

## 失败、恢复与结果发布

| 机制 | 关键来源 | 支持的结构事实与反证 |
|---|---|---|
| 阶段扩展 | [run-phase.loadAdapter](/workspace/codepatchbay/core/engine/run-phase.ts:177)、[resolvePhaseAdapterExport](/workspace/codepatchbay/core/engine/run-phase.ts:105)、[runPhase](/workspace/codepatchbay/core/engine/run-phase.ts:201) | 动态加载 `../phases/${validatedPhase}.js`，校验具名 callable，再 `Reflect.apply`；返回结果经 `validatePhaseResult` 校验。当前静态图不能绑定所有 adapter，但源码并非缺少 dispatch |
| DAG 失败 | [handleDagNodeFailure](/workspace/codepatchbay/core/engine/dag-node-failure.ts:91) | `:112` 失败事件、`:126` failJob、进度与结构化失败返回；appendEvent/failJob 为注入端口，不能凭边保证 I/O 成功 |
| 验证修复/基础设施重试 | [repairLoop :843](/workspace/codepatchbay/core/engine/run-job-execute-dag.ts:843)、[infraRetryLoop :990](/workspace/codepatchbay/core/engine/run-job-execute-dag.ts:990) | 双向调用 `:850/:1084` 受 recoverable 分类的相反分支限制；有 maxRepairs/maxRetries。已读到调用环不等于无限递归 |
| 完成门 | [runCompletionRepairLoop](/workspace/codepatchbay/core/engine/run-job-execute-dag.ts:1663)、[runCompletionGate](/workspace/codepatchbay/core/engine/completion-gate-runner.ts:152) | 初次 gate `:1668`、有限 repair、最终不可再 defer 的 gate `:1772`。runner 的 candidate identity/replay/scope/checklist/evidence 参与 evaluate，失败与成功返回分开 |
| 核心完成 | [handleCompletionSuccess](/workspace/codepatchbay/core/engine/completion-success.ts:169) | `:181` completeJob 后报告 job_completed 并返回 completed；此时还不等于远端发布或整个 assignment 已成功 |
| assignment finalization | [maybeFinalizeSuccessfulAssignment](/workspace/codepatchbay/runtime/worker/assignment-finalizer.ts:757)、[finalizeAndWriteSuccessfulResult](/workspace/codepatchbay/runtime/worker/assignment-finalizer.ts:1184) | autoFinalize 且 core completed 才执行；sourcePath/worktree/candidate/lease 等不足则失败。`:1236` 把必要 finalization 未成功的结果转换失败，不直接发布原 core completed |
| 终态落盘 | [publishTerminalResultAfterWorktreeCleanup](/workspace/codepatchbay/runtime/worker/managed-worker.ts:1133)、[writeTerminalResultOnceVerified](/workspace/codepatchbay/runtime/worker/managed-worker.ts:982) | 先暂存 produceResult，再验证成功/取消任务的 worktree cleanup/retention 证明，最后 `:1203` 写终态；已有文件必须等于预期值才能幂等接受。worktree 处置失败不能与新 completed 共存 |
| assignment 状态同步 | [completeAssignmentStateFromResult](/workspace/codepatchbay/runtime/worker/managed-worker.ts:847)，调用 `:1969` | 从 result.json 读回，交 completeAttemptAndAckInbox，保留 inboxAcked/terminalSyncFailed/mutationOwnershipLost；不能凭核心 completed 忽略此层同步 |
| queue 收敛 | [Reconciler.reconcileAssignments](/workspace/codepatchbay/server/orchestrator/reconciler.ts:1222)、[_finalizeQueue](/workspace/codepatchbay/server/orchestrator/reconciler.ts:1704) | running 时读取 result `:1311`；验证 attempt/finalizer contract、Git/journal readback；无效 completed 转 blocked/failed；成功更新 queue completed `:1773` |
| 自动恢复 | [FailureRouter](/workspace/codepatchbay/server/orchestrator/failure-router.ts:74)、[_finalizeQueue :1802](/workspace/codepatchbay/server/orchestrator/reconciler.ts:1802) | 持久 attempt budget、失败 fingerprint/策略变化、rate-limit 等分类；可重试/重启/换 agent/reroute/阻断，并把sourceContext带回pending。不是简单无条件“失败重跑” |
| finalizer-only 恢复 | [buildFinalizerOnlyRecoveryPlan](/workspace/codepatchbay/server/orchestrator/reconciler.ts:899)、[managed-worker :1784](/workspace/codepatchbay/runtime/worker/managed-worker.ts:1784) | 远端/pr失败需既有attempt/owner/观察证据且有代数与次数限制；只恢复finalizer，跳过核心任务执行。unknown mutation truth可要求只读核对，不能直接重放远端写入 |
| 人工 retry 入口 | [cli/retry.run](/workspace/codepatchbay/cli/commands/retry.ts:3) | 通过动态导入 enqueue 提交 cli_retry，metadata 含 retryJobId/agent/fresh；已读 worker/HUB 主链尚未证明这三个字段全部进入旧 job 恢复路径，不能直接画成 retryJob 调用 |
| job 恢复原语 | [job-store.retryJob](/workspace/codepatchbay/server/services/job/job-store.ts:985)、fresh recovery `:955` | 检查旧任务状态/force/预算/phase，再用原task/workflow和恢复context创建新job；这与自动assignment重试、CLI cli_retry是否接通须分开审查 |

### 对外结果查询

[projectTaskView](/workspace/codepatchbay/server/services/task/task-view.ts:615) 读取 durable queue，`:636` 必须同时匹配 taskId 与 projectId；linked job 在 `:643` 读取，失败退回 queue-only。`:664` 起区分 gate verified 与 delivery receipt/publication，不能把 succeeded、verified、deliveryReady 合并。`:708` 调 sanitizeTaskView 后返回。

[task.run](/workspace/codepatchbay/cli/commands/task.ts:259) 动态导入同一投影、调用后 renderTaskView；[fix.followTask](/workspace/codepatchbay/cli/commands/fix.ts:295) 轮询同一投影，支持超时/中断并共用 humanResultLine `:352`。这是结果观察链，不是另一个执行状态机。只读查询不能因此证明其所有传递依赖均无副作用。

## 独立审查候选：幂等读查与权威写入之间的窗口

**待 Astra 独立复核，未执行重现，不属于当前 CallScope 自动检出结论。**

真实声明在 [core/contracts/idempotency.ts 开头](/workspace/codepatchbay/core/contracts/idempotency.ts:5)：same-key 的任意非终态 entry 必须复用，scheduled/in_progress 明确属于活动任务。`selectIdempotentEntry` 只比较 hashed key 与非终态状态。

支持证据：

1. [fix.ts:520](/workspace/codepatchbay/cli/commands/fix.ts:520) 读队列、`:528` 选已有任务；之后另有 registry/route/agent 等等待，最后 `:576` enqueue。
2. [hub-queue.ts:1454](/workspace/codepatchbay/server/services/hub/hub-queue.ts:1454) withQueueMutation 经同一权威 queue lock 执行 callback，但其内部的 [enqueue 查重 :1597](/workspace/codepatchbay/server/services/hub/hub-queue.ts:1597) 仅接受 `status === "pending"`。
3. [entryKey :1545](/workspace/codepatchbay/server/services/hub/hub-queue.ts:1545) 用 projectId、description、key/lineage 拼接，范围也比 same-key 契约更窄。
4. [HubOrchestrator :342](/workspace/codepatchbay/server/orchestrator/hub-orchestrator.ts:342) 会把 pending 改为 scheduled；此状态合法地与另一个 CLI 提交并发。

允许的静态交错：A、B 都读到无同键任务 → A入队 → scheduler将A改scheduled → B进入enqueue权威操作 → `pending` 查重不匹配A → 创建第二entry。另一个不同description但相同显式key的并发提交也不满足 entryKey 比较。

反证与适用限制：顺序 fix 提交的前置 select 会复用 scheduled/in_progress；同描述、同key且第一项仍 pending 时 enqueue 自身会去重；queue lock 能避免两个写者同时损坏队列。因此此候选不是“完全没有幂等”或“缺少锁”，而是声明的活动同键约束没有在权威新增操作中完整复核。Astra需独立判断是否确认、严重度与所需修正，不能引用本稿当运行实验结果。

## 结论边界与扩展点

- 已读入口、持久队列、跨进程 worker、核心 DAG、失败落地、completion、finalizer、终态同步和对外投影都有具体实现来源；没有把 graph 不可达直接写成遗漏功能。
- `ctx.deps`、RunJobPorts、broker、本地 runtimeRoot、providerServices、phase adapter 动态加载、parallel review、副作用缓冲、retry/finalizer-only 是需要保留的扩展点。固定默认实现/默认环境的路径不能代表全部配置。
- 源码中的分支、类型转换、值约束、lease/CAS 和持久协议都超出当前显式 CALLS 可达性的证明能力；可提供新的静态绑定/契约分析输入，但当前不能声称已自动覆盖。
- 待复核的幂等窗口与 CLI retry 字段流转是源码审查线索，不是为了“查出东西”而把正常递归或分析缺口升级成缺陷。
