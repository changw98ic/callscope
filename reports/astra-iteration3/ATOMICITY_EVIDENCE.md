# CPB 同键去重：读查、权威写入与原子边界来源

本稿为第三轮静态能力实现提供源码材料，不是已运行的检测结果或新的目标缺陷确认。只读 `/workspace/codepatchbay` 生产源码；未导入、执行、测试、构建目标，也未调用仓库 CLI、Beads、索引或工具测试套件。未修改 v0.5 文档、核心或冻结 Astra 报告。

原观察为 [Astra CPB-03](../astra-baseline/CODEPATCHBAY_ANALYSIS.md) 与冻结基准的 `cpb.gap.active-key-dedupe-window`，定性仍为有具体前提的条件风险、`evidence_only`。本文没有生成或预填 A/B 并发交错，也不将人工原观察冒充模型自动发现。下文路径相对于目标仓库，行号为本轮原文定位。

## 1. 可以直接核对的源码事实

| 位置 / 符号 | 原文或局部事实 | 有限含义 |
| --- | --- | --- |
| `cli/commands/fix.ts:469`，`run` | `export async function run(args: string[], ctx: FixCtx = {})` | 分析对象是这一函数体，不是假定所有调用者都使用同一依赖。 |
| `fix.ts:426–450`，`resolveDeps` | `enqueue: o.enqueue ?? hubQueueMod.enqueue`；`loadQueue: o.loadQueue ?? hubQueueMod.loadQueue`（原文含类型cast） | 实际默认候选连接存在；ctx.deps 可覆盖，不能按方法名称固定全局唯一目标。 |
| `fix.ts:516–528` | 有 idempotencyKey 才 hash；`:520` `queue = await deps.loadQueue(hubRoot)`；`:525–527` 按 projectId 过滤；`:528` `selectIdempotentEntry(projectEntries, hashedKey)` | read / select 位于 enqueue 之前，且针对外层读到的 queue 值。 |
| `fix.ts:521–522`、`:524` | 读失败替换 `{entries: []}`；非数组也按空 entries | 这是源码fallback事实，不是所有读失败都会引发重复的证明。 |
| `fix.ts:529–541` | 有 existing.id 时返回/进入 follow，不执行后面的 enqueue | 正常新请求看到既有非终态同键项时可以复用；不能说所有同键提交都重复。 |
| `fix.ts:565–576` | `buildFixEnqueueInput(..., hashedKey, Date.now())`；`:576` `await deps.enqueue(hubRoot, enqueueInput)` | 执行写路径之前还有 registry / route / builder 等操作；同一词法 hubRoot 传给 read 和 enqueue。 |
| `fix.ts:202–234`，`buildFixEnqueueInput` | `:226` `metadata.queueDedupeKey = hashedDedupeKey`；`:228` projectId；`:231` description=problem | 关联键、项目与description的构造出处，不是一般字段流已自动证明。 |
| `core/contracts/idempotency.ts:10–16` | ACTIVE 为任意非终态，含 pending/scheduled/in_progress；同 key 复用同 taskId；终态允许新建 | 项目声明的去重意图来源。约束不是从 enqueue 这个名字猜出的。 |
| `idempotency.ts:58–73`、`:113–122` | terminal 初始化为 completed/failed/cancelled/canceled/archived；按 queueDedupeKey 相等且非 terminal 选第一个 | helper 实际谓词为非终态，不是仅 pending；该 queue 合同不与其它 job terminal 集合混为一谈。 |
| `server/services/hub/hub-queue.ts:1545–1547`，`entryKey` | lineage=`queueDedupeKey || originJobId || ''`；返回 ``projectId::description::lineage`` | writer 的复合键包括 description，外层 select 不比较 description。 |
| `hub-queue.ts:1595–1598`，`enqueue` | `return withQueueMutation(hubRoot, async (queue, authorityNowMs) => { ... queue.entries.find((e) => entryKey(e) === key && e.status === "pending"); if(existing) return existing; ... })` | 内层确实再次检查，检查口径限 pending 且复合键相等。不能误报“完全没有原子内检查”。 |
| `hub-queue.ts:1600–1620` | 创建新 id、status=pending、description及metadata，`:1619` `queue.entries.push(entry)` | check 与 insert 处于同一回调，回调内部这些步骤之间没有显式 await。 |
| `hub-queue.ts:1465–1466`，`loadQueue` | 直接 `return await loadLocalQueue(hubRoot)` | 所读默认 read helper 本身没有进入 withQueueMutation/withQueueLock。 |
| `hub-queue.ts:553–554`，`queuePath` | `path.join(path.resolve(hubRoot), "queue", "queue.json")` | read/save 使用同一个路径构造函数；物理文件身份仍需要部署/资源范围假设。 |

`enqueue` 在进入 mutation 之前会规范化 metadata / agent 配置。`server/services/agent/agent-config.ts:471–493` 的 `resolveAgentsForEntry` 无 agent 配置时返回原 metadata，另一分支以 `...metadata` 后追加 agent 字段；与 `hub-queue.ts:1580–1581` 的调用/赋值构成保存 queueDedupeKey 的源码反证。`core/job/meta.ts:15–23` 的 buildMeta 只提取执行边界字段，不能误以为该临时对象覆盖了全部 input.metadata。

## 2. 锁和持久化的真实范围

`withQueueMutation` 位于 `hub-queue.ts:1454–1463`，将回调转交给 `withQueueLock(hubRoot, (queue) => callback(queue, Date.now()))`。这不是 SQL 事务；是该仓库自有的文件队列 mutation 协议。

`withQueueLock` 的完整生命周期在 `hub-queue.ts:1309–1422`：

1. `:1311–1313` 从 queuePath 构造 `.lock` 目录及 owner 文件；`:1314–1326` 获取精确进程身份与 owner token。
2. `:1331–1387` 在 process fence 中尝试目录锁取得、owner 写入/恢复；无法取得就失败，不继续回调。
3. `:1392` 在已取得目录锁后重新 `loadLocalQueue`；`:1393` 记录 before；`:1394` `await callback(queue)`；`:1395–1396` 记录 after，改变才 `saveLocalQueue`。
4. `:1403` 再进入 process fence 调用 `releaseQueueLockExact`；`:1410–1421` 处理 mutation / release 错误并返回。

因此，**queue 内层的 fresh read → callback中的find/push → save，处于同一目录 owner lock 生命周期**。CLI 的 `loadQueue` / `selectIdempotentEntry` 不在该源码区域；writer 的回调虽受保护，保护也不会向外扩展到整个 `fix.run`。

不要把过程中的两种锁混淆：`hub-queue.ts:980–981` 的 `withQueueProcessFence` 调用 shared `withDirectoryProcessFence`；`core/runtime/durable-directory-lock.ts:2` 仅重导出 `shared/primitives/durable-directory-lock.ts`。后者 `:843–868` 规范化路径并调用 withProcessFence；`:809–840` 取得 fence、调用 operation、释放。queue 的 process fence **分别**用于 acquire / release 目录锁，不直接包围 `:1394` 的业务 callback。`withDurableDirectoryLock` 在 hub-queue 中另用于 inbox，不应被当作 enqueue 的保护函数。

持久化源码为 `hub-queue.ts:1447–1451` 的 saveLocalQueue → writeAtomic。writeAtomic `:1469–1527` 使用临时文件、sync、generation 校验、`:1503` rename 与目录sync；rename后 durability不明会保留 committed 标记。这些是写入/恢复机制的证据，不是完整锁算法或崩溃一致性已经验证。本稿没有逐分支审计所有 owner 恢复、进程探测及文件系统行为。

## 3. 改变内层过滤结果的生产写路径

`server/orchestrator/scheduler.ts:285–341` 的 nextCandidates 读取 pending pool 并按 DAG/readiness/capacity 等条件筛选。候选可能为空或被阻止；不能把存在状态写入代码解释为每项任务必然马上调度。

具体 pending → scheduled 写入位于 `server/orchestrator/hub-orchestrator.ts:342–353`：

```typescript
reservation = await updateEntry(this.hubRoot, candidate.id, {
  status: "scheduled",
  // claimedBy / claimedAt / metadata
}, {
  expectedStatus: "pending",
  expectedUpdatedAt: /* candidate revision timestamp */,
});
```

该调用前 `:334` 校验 leader lock；更新失败 `:354–356` 跳过候选。`hub-queue.ts:1633–1671` 的 updateEntry 同样使用 withQueueMutation，在 callback 中读取 entry、验证 expectedStatus/claimedAt/updatedAt，`:1659` 写 status，`:1667` 更新时间。它不会在 QueueState 外偷偷修改磁盘数据。

后续 dispatch 的另一写入 `hub-orchestrator.ts:442–449` 保持 scheduled并更换claim；失败路径 `:476–497` 在条件成立时可回到pending。`scheduler.ts:173–208` 的 stale recovery 也通过 guarded updateEntry，并重新读取 pool。这些是并发风险的反证/条件边界：状态转换不是无条件，成功调度和回滚需要分别建模。

leader lock 管理 orchestrator 的领导身份；源码没有显示它也被默认 fix facade 的 read-select-enqueue 整体持有。不能凭“有 leader lock”推导同键facade串行。

## 4. 适合通用 AST 抽取的材料

以下都是有范围的语法事实，可由通用提取器产生位置、源哈希和未知，而不硬编码 CPB 路径或预制并发trace：

| 抽取事实 | 本例来源 | 不能顺带推导 |
| --- | --- | --- |
| 函数内源码次序、分支和早退 | load/select/enqueue、existing.id return | 跨函数真实执行顺序、并发调度、每次都到达写入 |
| 调用点与参数词法来源 | 同一hubRoot标识符；builder的hashedKey参数 | 物理目录别名、ctx注入的实际目标、值从未被改写 |
| 回调嵌套范围与转发 | enqueue→withQueueMutation callback；mutation→withQueueLock callback | callback本身就是锁/数据库事务，或所有同资源写者都受保护 |
| 读、predicate、early reuse、insert | fresh load、find中status==pending、push | 谓词等价于产品意图、运行时Array方法未被替换 |
| key函数的字段构造 | projectId、description、lineage fallback | 任意输入归一化、hash碰撞或业务key语义 |
| 保护区域的取得/释放出处 | acquired guard、callback/save、releaseExact | 锁协议实际安全、崩溃、所有权变化或FS效果 |
| 字面状态更新与guard | updateEntry patch scheduled、expectedStatus pending | 更新实际成功、是否发生在另一个请求的两个操作之间 |
| 异常/回滚反证 | read catch空值；reservation null；scheduled→pending | 所有失败均可恢复或一定会造成重复 |

callback的“资源保护”语义不能单靠 AST 名称自动猜测。提取器可以发现回调属于哪个函数/调用参数、相关 acquire/release 位置；把它解释为一个可信 critical region 必须有版本化协议或明确声明，且保留未审锁实现条件。

## 5. 必须由显式合同提供的关系

如果下一轮增加通用原子边界合同，至少需要明确以下前提，并分别记录“源码抽取”“合同声明”“仍未知”的来源：

- **权威资源**：默认facade的loadQueue、enqueue和scheduler.updateEntry读写同一个逻辑queue；同一hubRoot词法参数及queuePath出处提供证据，不证明运行时物理资源一致。
- **依赖装配**：规则针对resolveDeps默认分支、没有ctx.deps覆盖的路径；不能将整个FixDeps接口全局写成唯一实现。
- **保护区域语义**：withQueueMutation/withQueueLock将fresh read、callback和save归入同一个资源范围；process fence与长期目录锁分别声明，不能因为函数名含lock就认证任意回调原子。
- **产品匹配谓词**：同projectId + hashed queueDedupeKey + 非终态复用同id，来源为idempotency.ts合同。将enqueue当作facade最后的去重权威点是要明确说明的合同关系；其它enqueue调用者可有自己的用途。
- **状态及键口径**：非terminal与pending不是同一个集合；description不是facade选择器的条件。预查谓词、权威回调谓词、scheduler状态写入必须作为不同出处关联，不能只靠同名字段判等。
- **其他写者假设**：评估限定所读入口、同资源、有效锁协议、没有额外外层串行化或其它数据库唯一约束；未声明这些不能证明系统一般并发行为。

契约出处必须可下钻。它可以声明检查义务、资源映射与保护函数模型；不得在配置里手工填写“A先读/B后写”的交错，然后把这些输入重新输出称为工具推导。

## 6. 可报告的结论和仍未知的条件

当前源码支持有限差异结论：默认facade的项目/同hash/非终态选择先于独立enqueue调用；writer内部确实有受保护的再次检查，但只复用pending且键含description；另有生产guarded mutation可把pending变成scheduled。**读查与权威检查口径/作用域不同**，不是“没有锁”，也不是“存在锁所以没有竞态”。

要进一步认定产生重复，仍需同资源并发请求、足够相同key、预查没有看到既有项、权威读时状态/description使内层不匹配、后续插入/持久化成功、没有外层统一约束等前提。源码里有相关操作，并不证明某次运行满足全部条件。本稿不提供运行复现、不自动裁决交错可达性、不声明一般线程/进程原子性。

反证必须保存：新请求已看见scheduled/in_progress同键项时外层会复用；同description且队列权威读取仍pending时内层会复用；leader、容量、expectedUpdatedAt等会阻止部分调度；dispatch失败可能返回pending；队列锁、写入或恢复错误可阻止commit。不能从条件风险宣传“任何双提交必然重复”。

## 7. 原文件身份

前四项与冻结Astra观察引用的原文件SHA256一致；其余为本稿补读来源的原始字节身份。目标提交仅沿用原Astra报告上下文，不以此替代字节核对。读取后未执行目标或改变文件。

| 相对路径 | SHA256 |
| --- | --- |
| cli/commands/fix.ts | 5275c7d3cb7633c48ff4fca005207a78a6783527b445d25ac36e330cb3a9e083 |
| core/contracts/idempotency.ts | 8ab99736798fa50dbc981b5c99bf21d29199b89bb67ecf61e03f486164765dd4 |
| server/services/hub/hub-queue.ts | 0bd13766a2a2fcd271c2ead8166fbbd6f782fde32f63954ccced88a4cb2de02c |
| server/orchestrator/hub-orchestrator.ts | 41e248486eeae6f36b8f66b87df56a466bb1d4c5cb86d4c09066012e170f8454 |
| server/orchestrator/scheduler.ts | 69d275bae38a3a614d4d1b412542a8b2eb2b83f0f7b2bd694807cec529d55c00 |
| server/services/agent/agent-config.ts | 83a2eef775f1ff274054ee16fa749e195ae5a475f42abf520b2434e7ed6af484 |
| core/job/meta.ts | 2e40a285e1ea4c28af9fb7d949e026a3edd74c2471e726ff702f1aa2a9ac0319 |
| core/runtime/durable-directory-lock.ts | 9b434101cacec190524cd43f8313506082abc1bc065f161be78b57b6e00b257d |
| shared/primitives/durable-directory-lock.ts | 505dfb1c6c373911fbbedfadf273d982ccf459abacb643c6310c5ef46d8e510c |
