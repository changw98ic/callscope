# CPB-01：持久记录及 broker 来源接缝

实现为 `callscope/pipeline_channels.py`，由 `pipeline_flow` 的真实保存源码分析上下文调用 `analyze_pipeline_channels(analysis)`。本模块不执行目标、不运行测试或构建、不生成普通 CALLS 边。规则只提供来源选择器和有限模型；实际 codec 操作数、record 身份、路径、receiver、return projection、guard 和消息 envelope 从认证 AST 提取。

输出单列 `queue`、`inbox`、`broker`、`counter_transport`、`source_relations`、`models` 和必要 `gaps`。全部必要接缝支持且缺口为空才支持完整 channels；函数角色均存在不能代替来源关系。source anchor 带快照、原 hash、词法 owner、范围和 parser identity。

队列接缝连接实际 `withQueueMutation` 的 callback 形参、`withQueueLock` 的新读/执行/保存/释放区域、调用者同一 root 到 `queuePath`，以及 read bytes → JSON.parse 和 queue.entries → JSON.stringify → writeAtomic 操作数。目录锁及正常文件可见性为声明模型，实际时序、物理别名、失败发布与所有写者不在其运行证明范围。

inbox 接缝连接实际 assignment 参数 → structuredClone → JSON.stringify → JSON.parse → committedPayload；写入 staging 的实际 data 参数继续进入 `writeJsonAtomic` 的 jsonContent、file handle.writeFile、同 temp rename。`currentHooks` 的默认 Node 文件 provider 和可覆盖 branch 分开表达。staging 发布到 assignmentId.json 后，receipt 的 committedRecord clone/freeze、claim 的 processing rename、pinned JSON read、返回 assignment 与 claims append 都保留独立来源。malformed、missing、attempt/attemptToken 冲突、generation 变化、补偿、锁及 durability 错误不会被算成普通新记录传递。

broker 接缝连接 client 的实际 inbox.claim literal、私有 call 的 JSON `{workerId, incarnationToken, op, args}`、server body decode、op switch、source-created WorkerStore 的 claim 方法，以及 pre-dispatch credential rejection。HTTP success 的 handler result → `{ok:true,result}` → sendJson → client response.json → brokerResult.result → inboxClaimsResult 的同 claim return 分别保存。正常 HTTP/JSON provider 和有效 credentials 是明确运行条件；请求名与跨 wire 关系不会伪装成 CALLS。

counter 接缝连接 `createAttempt` 的 `_readStateFile(assignmentId)`、previousAttempts + 1、同 state.attempts 写入和 `_writeState`，再连接真实 state.json 数据读写。生产 reconciliation 使用 `listAssignments`，其实际读出的 state append 到列表并进入 Reconciler loop；经 `_finalizeAssignment`／`_compensateFinalization` → `_finalizeQueue` 的 assignment 实参，进入 failureRouter.route。独立 `getAssignment` API 不能代替该生产链。已有 attempts、queue attempt、phase 和 verification infrastructure 预算分开，不因同名字段合并。

普通 JSON 保留限定有限、普通、无自定义 provider 的数据记录及有限 scalar 域。缺字段、undefined、非有限数、custom clone/JSON/fetch、credential 拒绝和失败分支不是无条件保留证明。功能报告说明当前/新建/复用的来源及适用条件；事实数不是运行或业务覆盖率。

claims 返回关系要求实际 callback 返回的记录经 `_withLocalInboxLock` 的 `result = await callback()` 与同 result return，传到调用者的 `claim`，再进入 exact `claims.push(claim)` 和同一 fresh array return；同函数中存在任意 push 不构成此关系。锁释放/回调失败的 throw guard 单列，不把 callback 的正常完成提升为无条件成功。

client 返回来源要求 `response` 为 actual fetch 绑定、`response.json()` 为该 response receiver、decoded payload 通过实际 `isRecord` 成功分支进入 `brokerResult(payload, op)` 并被 return；`inboxClaimsResult` 要求实际 result formal 的 map 被 return，mapper 的 candidate 通过来源认证的 `recordResult` 同参数 return。解码失败、非对象 envelope 与 contract rejection 是独立错误分支。

2026-10-13 的普通保存源码查询已写入 `PIPELINE_CHANNEL_OBSERVATION.json`，查询脚本为 `observe_pipeline_channels.py`，日志为 `pipeline-channel-query.log`。实际快照为 `731ae3b53582e86de4c9c786c224fc99aa45154099b7738ce8652be0f5a3f336`；完整快照及 metadata 保留。queue、inbox、broker、counter_transport 四部分及其所有必要细分来源关系均支持，必要 gaps 与主分析上下文 gaps 均为空，保留 9 组源关系与 3 个具体模型应用。

该结果对应 `pipeline_channels.py` SHA256 `32df938a2b82ec32bd57bb6d8638e2e54658d031d74019507e9fc8014f89bfa4`。它确认本 helper 负责的持久化和消息来源接缝；CPB-01 主裁决仍需主分析器的字段 mutation、旧记录复用与 source modes 结果，不由这个局部来源查询替代。目标执行、测试、构建及运行传输验证均未发生。
