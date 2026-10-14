# CodePatchBay：持久化、状态与权限边界来源整理

日期：2026-10-12。来源仓库：`/workspace/codepatchbay`。读取的 HEAD 为 `4f2d2eca31d90b0122db1c1429dd365672db2393`；以下位置指本轮读取的工作区源码。

这是交给 Astra 的来源稿，不是最终缺陷裁定，也不是执行验证报告。只进行了文件读取和源码搜索，没有导入、运行、构建或测试目标项目，没有修改目标或 CallScope 核心。仓库 AGENTS 要求的 `cpb code-index` 与 Beads 命令未执行，因为本轮明确禁止运行目标及改变目标状态。

## 观察范围

详细读取了下表函数及其相关片段；较大的合并文件没有逐行全部审阅。补充检索了生产 `cli/`、`core/`、`server/`、`runtime/`、`bridges/` 中的重试参数、终态及索引恢复调用点。未检查目标测试、安装依赖或部署配置的实际生效状态，未验证平台沙箱、外部 GitHub、磁盘故障与并发时序。

| 边界 | 关键模块及可定位符号 |
| --- | --- |
| CLI 入队 | `cli/commands/pipeline.ts:134 run`，`:36 parseCommonFlags`；`cli/commands/retry.ts:3 run` |
| 队列持久化 | `server/services/hub/hub-queue.ts:1550 enqueue`，`:1633 updateEntry`，`:1309 withQueueLock`，`:1453 withQueueMutation` |
| 调度与恢复 | `server/orchestrator/hub-orchestrator.ts:224` 启动恢复，`:319` 候选调度；`server/orchestrator/reconciler.ts:1183 recoverRuntime`，`:1704 _finalizeQueue` |
| Worker 与结果 | `runtime/worker/managed-worker.ts:1235 main`，`:1133 publishTerminalResultAfterWorktreeCleanup`，`:982 writeTerminalResultOnceVerified`，`:847 completeAssignmentStateFromResult` |
| 引擎依赖注入 | `bridges/engine-bridge.ts:18 runJobWithServices`；`server/services/engine-runner.ts:130 runJobWithServices`，`:73 buildServices` |
| 引擎执行与完成 | `core/engine/run-job.ts:65 runJob`；`core/engine/run-job-execute-dag.ts:1783 executeWorkflowDag`；`core/engine/completion-success.ts:169 handleCompletionSuccess` |
| Job 持久化 | `server/services/job/job-store.ts:508 createJob`，`:1129 completeJob`，`:315 updateJobsIndexEntry`，`:473 getJobAndUpdateIndex`，`:1359 getJob` |
| 事件与检查点 | `server/services/event/event-store.ts:1179 appendEvent`，`:1493 appendEventIfCursor`，`:1034 appendSerializedEventDurably`，`:1747 readJobProjection`，`:1805 checkpointJob` |
| 状态物化 | `server/services/event/event-materializer.ts:270 materializeJob`，`:381 advanceMaterializedJob`，`:792 TERMINAL_STATUSES` |
| 新任务恢复 | `server/services/job/job-store.ts:927 createRecoveryJob`，`:985 retryJob`，`:1425 recoverAsNewJob`，`:1473 retryAsNewJob` |
| 发布及仅发布恢复 | `runtime/worker/assignment-finalizer.ts:757 maybeFinalizeSuccessfulAssignment`，`:1184 finalizeAndWriteSuccessfulResult`，`:951 recoverAndWriteFinalizerOnlyResult`；`server/services/auto-finalizer.ts:1425 finalizeSuccessfulQueueEntry`，`:3135 recoverFinalizerOnly` |
| 发布持久意图 | `server/services/finalizer-journal.ts:669 readFinalizerJournal`，`:714 appendFinalizerJournal` |
| Hub 权限 | `server/index.ts:144 startHubServer`；`shared/hub-auth.ts:135 readServiceTokensFile`，`:360 authenticateHubRequest`，`:386 hubPrincipalHasScope`，`:392 hubPrincipalCanAccessProject` |
| OIDC 与内部 broker | `shared/hub-oidc.ts:618 openHubOidcProvider`；`server/services/hub/worker-state-broker.ts:111 handleWorkerStateBroker` |
| 独立只读流服务 | `server/services/stream/stream-server.ts:236 startStreamServer`，`:389` wiki 路由 |
| 维护与备份恢复 | `shared/hub-maintenance.ts:710 writeJsonDurableAtomic`，`:1488 assertHubWritable`；`server/services/hub/hub-backup.ts:3621 recoverInterruptedHubRestore`，`:3707 restoreHubBackup` |
| 显式状态修复 | `server/services/cleanup/cleanup.ts:1100` 索引重建；`server/services/hub/hub-registry.ts:2907 flushJobsIndexesDuringHubStop`；`server/services/runtime.ts:440` divergence 告警；`cli/commands/doctor.ts:312` 展示 |

## 已确认的源码连接

### 1. CLI → 队列 → assignment → worker → 引擎

1. `pipeline.run` 根据 `parseCommonFlags` 得到任务和参数，通过运行时路径动态导入 `enqueue`，再写队列：`cli/commands/pipeline.ts:183`、`:189`。动态 import 不等于没有连接。
2. `hub-queue.enqueue:1550` 强制 `REQUIRED_EXECUTION_BOUNDARY`，解析项目和 agent 元数据；`:1593` 起在 `withQueueMutation` 内检查已有 pending 去重键并创建条目。队列去重检查位于队列锁内，与下面 Job 创建候选不同。
3. `hub-orchestrator.ts:342` 用 expectedStatus/expectedUpdatedAt 预留队列；`:364` `getOrCreateAssignmentForEntry` 保存任务、项目运行根和完整 metadata；`:381` `createAttempt` 记录 worker 与 epoch；之后发布 inbox。各阶段仍检查 leader，并保留失败元数据：`:335`、`:438`、`:461`。
4. `managed-worker.main` 在 `:1797` 调用桥接的 `runJobWithServices`，传入 jobId、project、worktree sourcePath、AbortSignal 和 workerBrokerClient。
5. `engine-bridge.runJobWithServices:18` → `engine-runner.runJobWithServices:130` → `runJob:157`。`buildServices:73` 明确把 job/event 能力装配为本地函数或 broker 的绑定方法；所以 `ctx.createJob`、`ctx.appendEvent` 等间接调用应在报告中保留注入证据，不应以自动图缺少唯一目标判定为未接线。
6. `runJob` 依次创建任务、准备风险/计划、冻结 checklist/DAG，再调用执行器：`core/engine/run-job.ts:121`、`:144`、`:160`。`handleCompletionSuccess:181` 调 `completeJob` 后才返回 completed。

这些连接是静态源码可见的装配关系；没有证明 provider、网络和实际 subprocess 成功执行。

### 2. 事件日志 → 检查点 → Job 索引

- `createJob:624`、`completeJob:1136` 先追加事件；后续 `getJobAndUpdateIndex:473` 读取 `getJob` 的权威物化状态，再更新索引。
- `appendEvent:1179` 绑定 project/job 身份并校验序列化；`:1189` 获得事件锁；`:1194` 根据物化终态过滤非允许的后续业务事件；`:1237` 追加经过秘密处理的序列化内容。
- `appendSerializedEventDurably:1034` 中有 file sync (`:1123`) 和 parent sync (`:1138`)，并检查文件/目录权限身份与写后状态。不能把这等同于跨文件事务或绝对不可篡改。
- `readEvents:1561` 与 `readEventsReadOnly:1567` 均调用只读解析器，当前代码没有在普通读取中自动恢复事件文件。
- `readJobProjection:1747` 对 checkpoint 校验 eventCount、事件前缀摘要和该前缀的物化状态（`:1713` 起）；重放 suffix 后还与完整物化结果比较（`:1769`）。不匹配会抛明确错误，而不是偷偷使用失配 checkpoint。
- `updateJobsIndexEntry:315` 采用索引锁 → 事件锁顺序，再重新读取权威 projection，在持有事件锁时写索引（`:327`–`:342`）。这保护索引更新不发布调用者传来的旧状态；没有把先前事件追加与索引更新合成跨文件原子事务。
- `writeJsonDurableAtomic:710` 使用独占 no-follow 临时文件、file sync、rename、parent sync 和 rename 前后身份核对；已 rename 但后续失败会携带 committed/ambiguity 等信息。

### 3. 引擎完成 → 发布 → 结果 → 队列收敛

- `maybeFinalizeSuccessfulAssignment:757` 要求 autoFinalize 且 engine result completed；`:795` 起检查 sourcePath/worktree 与 candidate-base 绑定。
- `finalizeSuccessfulQueueEntry:1425` 先要求 job completed（`:1480`）；live 模式需明确 allowLive（`:1510`）及 mutation lease/fence（`:1578`）。远程流程另核对 capability、transport principal、候选及 Git 读回。并非引擎返回 completed 就无条件 push。
- PR 远程写入前先持久化 intent：`auto-finalizer.ts:2324`–`:2344` 的 `beforeRemoteMutation` 调 `advanceLiveJournal`，再核验 lease。`appendFinalizerJournal:714` 校验身份/允许状态转移/lease，并在 `:788` 调 `appendEventIfCursor`。日志持久化 uses cursor CAS，而非无条件覆盖。
- `publishTerminalResultAfterWorktreeCleanup:1133` 暂存 produced result；验证 managed worktree 的 cleanup/retention proof（`:1172`），再调用 `writeTerminalResultOnceVerified:1203`，两次执行 `beforePublish` fence。
- `completeAssignmentStateFromResult:847` 从持久 `result.json` 读取，再 `completeAttemptAndAckInbox:869`。失败返回 terminalSyncFailed，不把未同步状态宣称完成。
- `Reconciler._finalizeQueue:1704` 检查持久 finalizer success contract、bundle 文件、Git readback 和 journal（`:1713`），不满足时把结果当 finalizer_failed；`:1748` 可安排 finalizer-only recovery。该层与 engine job completed 是不同阶段，不能仅因状态不同就断言不一致。

### 4. 恢复路径

- Job 恢复创建新 Job，并附 recovery_created/lineage：`createRecoveryJob:954`、`:966`、`:980`。原终态任务的普通业务事件仍受封印。
- finalizer-only：worker `:1859` 分支 → `recoverAndWriteFinalizerOnlyResult:951` → `recoverFinalizerOnly:3135`。恢复先核对 journal 项目/entry/originJob/repository/issue/capability/principal（`:3199`），复核 durable capsule，再根据远程 readback 决定后续动作；若允许写，`:3273` 与 `:3301` 仍要求 lease 和 journal CAS。未执行这些路径，不能宣称远程幂等已验证。
- Hub 启动 `server/index.ts:181` 先 `recoverInterruptedHubRestore`，再恢复 stale maintenance、`assertHubWritable`；orchestrator `:224` 完成 runtime/queue reconciliation 后才 markReady。
- `assertHubWritable:1488` 对存在 restore journal 或 active maintenance 拒绝写入；`recoverInterruptedHubRestore:3621` 在 maintenance 内读取权威 journal、处理恢复和锁释放的 committed ambiguity。备份/恢复路径会重新验证 archive 和目录 generation；没有实际模拟中断。

## 权限与隔离边界

1. **公开 Hub：** `startHubServer:150` 限制 anonymous-dev 只能 loopback，默认要求认证；`:165` 打开 service-token provider，另支持 OIDC。service-token 文件须绝对路径、非 symlink/真实文件、打开前后 fingerprint 相同，POSIX group/other 不可读（`hub-auth.ts:135`–`:165`）；bearer 以 SHA-256 digest/constant-time 比较并检查 expiry（`:360`）。`/api/projects` 同时检查 hub:read 和每个项目授权（`server/index.ts:307`–`:326`）。
2. **OIDC：** `hub-oidc.ts:805` 验证 claims、允许算法/key 和签名；`:818` 核对配置身份没变化；`:821` 做 group → scopes/projects 映射。签名有效不直接获得任意项目权限。
3. **内部 broker：** `/internal/worker-state` 在公开 Hub bearer 分支前被处理，但有独立认证。`handleWorkerStateBroker:124`–`:142` 验证 broker token digest、incarnation、worker 状态；`:163`–`:186` 绑定 currentAssignment、attemptToken、worker project、注册 runtimeRoot 与预期 jobId。不应误报为绕过认证。
4. **审计层有区别：** broker mutation 会在 switch 前 await `beforeMutation`（`worker-state-broker.ts:192`），Hub 在 `server/index.ts:230` 先落 mutation_intent；最终访问审计 `:415` 失败使 HTTP 响应 503。`runJob.ts:76`、`:93` 的 `finalizeAuditTrail` 则是 Job 运行尾部 best-effort。它们不在同一层，不能据此认定相互矛盾；finalizer 自己的审计失败又会返回 `FINALIZER_AUDIT_RECORD_FAILED`（`auto-finalizer.ts:1453`）。
5. **独立 stream：** `stream-server.ts:236`–`:287` 使用单独 bearer token 与 loopback-only anonymous opt-in，并检查 CORS origin。该 token 是服务范围共享读权限，`projects` 是订阅过滤，不是 Hub OIDC 的 project scope。没有 evidence 可把它说成多租户隔离。
6. **Worktree：** 只观察了 worker 的 create-time binding、cleanup proof、publication fence 与 finalizer candidate binding。agent OS sandbox 和 tool-deny 实现由 Astra 另行检查；本稿不证明这些部署策略已经生效。

## 交给 Astra 独立裁定的候选

### CPB-S1：CLI 重试预算没有接入当前 managed 执行预算

- **可见契约：** `pipeline.parseCommonFlags` 读取 `--retries`（`:69`），帮助文本称 Max pipeline retries（`:149`），入队 metadata 保存 `maxRetries: parsed.retries`（`:205`）。
- **断点证据：** orchestrator 把完整 metadata 放 assignment（`:373`），但 `managed-worker.ts:1809` 传固定 `maxRetries: 3`；`FailureRouter.route` 在 `failure-router.ts:112` 从按 failureKind 的 `MAX_RETRIES` 取预算，`:265` 与 assignment.attempts 比较。生产代码检索未发现 `metadata.maxRetries` 或 `ctx.maxRetries` 被该路径消费；phase retry 用 env/deps（`phase-retry.ts:369`），DAG 节点预算用 `node.maxRetries`（`core/workflow/dag-executor.ts:445`）。
- **反证与范围：** 独立 `job-store.retryJob:1029` 会消费其自己的 maxRetries 参数，但本轮未发现它接到 pipeline→managed-worker 主链。自动重试功能本身并非缺失；候选是公开参数与实际预算控制没有连接。没有运行任何不同参数任务。
- **机器定位：** `pipeline.parseCommonFlags`、`pipeline.run`、`managed-worker.main`、`FailureRouter.route`、`job-store.retryJob`。

### CPB-S2：superseded 的终态分类在层间不同

- **真实来源：** `review-dispatch.completeRemediation:4470` 的 FIXED 分支调用 `markJobSuperseded:4485`；`:4487` 写 job_superseded，`event-materializer.ts:633` 设 status=superseded。
- **不一致证据：** `event-materializer.TERMINAL_STATUSES:792` 包含 superseded；`job-store.ts:430` 的私有集合只有 completed/failed/blocked/cancelled。`job-store.isTerminal:1407` 对具有 jobId 的 superseded 返回 false，`requireNotTerminal:461` 同样未拒绝这个状态；`recoverAsNewJob:1441` 据此报 not terminal。
- **反证与限制：** `appendEvent:1194` 使用前者，仍拦截 superseded 的非允许业务事件；review-session/cleanup 也识别 superseded。不构成已证明的历史数据改写。当前 CLI retry 通过新队列，不直接调用 recoverAsNewJob；本轮未找到后者的当前主链调用者，也不能假定 superseded 必须允许恢复。适合裁定为跨层状态契约分歧，而非“CLI 恢复已坏”。
- **机器定位：** `completeRemediation`、`markJobSuperseded`、`materializeJob`/`job_superseded handler`、`isTerminal`、`requireNotTerminal`、`recoverAsNewJob`。

### CPB-S3：Job 创建的相同身份/队列键检查与事件提交不在同一原子边界

- **源码证据：** `createJob:582` 起对 providedJobId 执行 `getJob` 的存在检查，`:592` 起对 queueEntryId 执行 `getJobByQueueEntryId` 查询，最后 `:624` 才调用 appendEvent。这个检查与提交没有共同包住的 per-key lock/CAS。
- **可推导时序：** 两个并发调用都可先看到同 providedJobId 不存在，然后依次获得事件锁；`appendEvent:1189` 只核验终态，未拒绝已有 running stream 的第二个 job_created，因此普通 read-check-append 没有实现原子唯一性。不同随机 jobId 携同 queueEntryId 并发进入时，两者也可在索引更新前均看不到该队列键，写入不同事件流。
- **反证与限制：** 队列 `enqueue` 自己的 pending 去重检查在队列锁内，不能与这个问题混为一谈。managed 主链另有 assignment/attempt fencing 和 worker broker scope，它们降低正常路径出现并发的机会；没有运行并发请求，也没有证明真实仓库发生过重复创建。`createJob` 对既有 providedJobId 的顺序调用明确拒绝，不应把本候选叫“顺序幂等缺失”。
- **机器定位：** `createJob`、`getJobByQueueEntryId`、`appendEvent`、`updateJobsIndexEntry`。

## 条件关注与反证，不作为已确认缺陷

### 事件已提交、索引更新失败后列表可保留旧记录

`completeJob:1136` 的终态日志提交早于 `getJobAndUpdateIndex:1160`；索引失败重试后仍抛错（`retryUpdate:432`）。`listJobsFromIndex:411` 对已有索引只调 `mergeMissingEventStreams`；该函数在 `:392` 对已存在的 key 直接跳过，不主动刷新已有旧值，而 `getJob:1359` 直接重放 projection。因此在这类故障前提下，列表和详情可能暂时不同。

反证：`cleanup.ts:1100` 明确重建权威索引；`hub-registry.ts:2907` 停 Hub 刷索引；`runtime.ts:440`/`doctor.ts:312` 显示 divergence。不能报告“永远不能修复”或“整个 job state 没有权威来源”。当前 `jobs reconcile/cleanup/gc` CLI 已明确移除（`cli/commands/jobs.ts:4`），不建议援引旧命令作为现有恢复入口。

### stream wiki 读取只做词法路径约束

`stream-server.ts:400`–`:406` 使用 path.resolve + wikiBase 前缀检查，随后 fs.readFile。该函数未见 realpath/no-follow 校验。如果 wiki 树中存在指向外部的 symlink，Node 文件读取会沿 symlink 到外部；因此词法边界不等于实际文件边界。

反证与前提：有效 bearer 仍然必要；本轮未发现真实 symlink、远程写入它的能力或凭据不足用户可以访问此服务。不能称为已利用漏洞或已证明多租户越权。Astra 可结合 wiki 写入权限及系统安全契约决定是否纳入最终范围。

## 对工具评估的直接含义

上述三个主候选需要参数/状态/原子边界信息。仅有函数 CALLS 的存在性无法证明 `--retries` 值实际进入预算、两个终态集合相等或 read-check-append 原子性。依赖注入和动态 import 还会导致自动调用图未知边；手工发现连接后，应把 unknown 与已确认断点分开。

可以用明确调用关系作为基准：`engine-bridge.runJobWithServices → engine-runner.runJobWithServices → core.runJob`，`job-store.completeJob → appendEvent`，`appendFinalizerJournal → appendEventIfCursor`，`startHubServer → recoverInterruptedHubRestore`。这些关系不是运行成功或功能完整性的证明。缺口候选还需要把参数来源、状态枚举及提交边界作为证据，避免只靠完整路径/缺失路径二选一给结论。
