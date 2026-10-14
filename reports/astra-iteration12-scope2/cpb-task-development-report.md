# CodePatchBay — static source review：自动静态分析报告

快照：`7b58e73339e7ad28592c4a0bede1da0028935b30edd940419841971b354c2bfe`；仅使用保存源码、图和静态分析证据，未执行目标、测试或构建。

## 主要发现

此快照没有配置完整条件判断；不从结构规模推断功能正确。

原始完整 JSON 保留所有条件、反证、未知项、source facts 和保存发现身份。以下限制仅影响展示，不改变分析结果。

## 具体职责与接口交接

以下正文由所选声明的实际记录字段、赋值、实参接口和提前退出条件生成。目录名只供导航；普通调用、消息字段、执行、交付和投影分别保留。

完整职责、所有操作和来源：`/architecture/responsibility_explanations`。

### `cli/commands/task.ts::renderTaskView`

将「view.state」作为第 1 个实参交给已绑定接口「ts:cli/commands/task#humanStateLine」，对应捕获形参「state: TaskStateValue」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「rawSummary」的初始化来源为「typeof view.summary === "string" ? view.summary.trim() : ""」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留同一块中的正常源码顺序：语句位置「0」的操作「3b1091123dd08243bc950563」先于语句位置「1」的操作「840e2ba8ba36b12238a5425c」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`cli/commands/task.ts:163`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/0`。

### `cli/commands/task.ts::autoResolveProject`

构造捕获的空记录「{}」；没有从空记录形式推断额外字段或持久效果。 在调用形式「resolveHubRoot」中提供第 1 个实参「cpbRoot」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「src」的初始化来源为「proj?.sourcePath ? path.resolve(String(proj.sourcePath)) : null」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(src &amp;&amp; (src === cwd || cwd.startsWith(src + path.sep)))」的捕获提前退出分支为「return：id」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return id;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「2c7af75fc38e2d943ef152ab」先于语句位置「1」的操作「9aecad713e8d1c06de1b5a20」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`cli/commands/task.ts:210`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/1`。

### `cli/commands/task.ts::run`

将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:cli/commands/task#autoResolveProject」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「i」的初始化来源为「0」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「i」存在源更新「i++」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(args.includes("--help") || args.includes("-h"))」的捕获提前退出分支为「return：0」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return 0;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「bf1988c13bbab19235518e7f」先于语句位置「1」的操作「1843e3fd0764e64496af4196」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「view」作为第 1 个实参交给已绑定接口「ts:cli/commands/task#renderTaskView」，对应捕获形参「view: TaskView」。该普通调用关系不替代进程或网络协议关系。

源码：`cli/commands/task.ts:259`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/2`。

### `core/contracts/task-view-fields.ts::sanitizeTaskView`

构造捕获的空记录「{}」；没有从空记录形式推断额外字段或持久效果。 在调用形式「Object.entries」中提供第 1 个实参「raw」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「out」的初始化来源为「{}」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return out;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「8584c6a14db44eeb1e6ca79b」先于语句位置「1」的操作「7e61fbfe4a0b79a138d67af1」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`core/contracts/task-view-fields.ts:128`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/3`。

### `server/services/hub/hub-queue.ts::loadLocalQueue`

构造捕获记录，字段按源码次序为「maxBytes ← QUEUE_MAX_BYTES」。不据构造形式推断物理持久化。 将「{ maxBytes: QUEUE_MAX_BYTES }」作为第 2 个实参交给已绑定接口「ts:shared/primitives/durable-directory-lock#readBoundedRegularFileNoFollow」，对应捕获形参「{ maxBytes, hooks }: BoundedRegularFileReadOptions」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「raw」的初始化来源为「await readBoundedRegularFileNoFollow(queuePath(hubRoot), { maxBytes: QUEUE_MAX_BYTES })」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(String(errnoCode(err)).startsWith("BOUNDED_FILE_"))」的捕获提前退出分支为「throw：Object.assign(new Error(`unsafe local queue file: ${queuePath(hubRoot)}`, { cause: err }), {\n        code: errnoCode(err) === "BOUNDED_FILE_TOO_LARGE" ? "HUB_QUEUE_TOO_LARGE" : "HUB_QUEUE_UNSAFE",\n      })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return defaultQueue();」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「QUEUE_MAX_BYTES」关联路径「QUEUE_MAX_BYTES」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「9067fbf7677b304c45459528」先于语句位置「1」的操作「b1892da4993ec9120808f60f」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

条件「(errnoCode(err) === "ENOENT")」的捕获提前退出分支为「return：defaultQueue()」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。

源码：`server/services/hub/hub-queue.ts:1424`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/4`。

### `server/services/hub/hub-queue.ts::loadQueue`

将「hubRoot」作为第 1 个实参交给已绑定接口「ts:server/services/hub/hub-queue#loadLocalQueue」，对应捕获形参「hubRoot: string」。该普通调用关系不替代进程或网络协议关系。 以「return await loadLocalQueue(hubRoot);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`server/services/hub/hub-queue.ts:1465`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/5`。

### `server/services/job/job-store.ts::getJobByQueueEntryId`

构造捕获记录，字段按源码次序为「project ← project；dataRoot ← dataRoot」。不据构造形式推断物理持久化。 将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/job/job-store#listJobs」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「jobs」的初始化来源为「await listJobs(cpbRoot, { project, dataRoot })」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!queueEntryId)」的捕获提前退出分支为「return：null」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return null;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「project」关联路径「project」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「ebb91b53f9f16439c4552898」先于语句位置「1」的操作「bd3356f574187c444d7a5a1c」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/job/job-store.ts:1374`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/6`。

### `server/services/task/task-view.ts::projectTaskView`

构造捕获记录，字段按源码次序为「schemaVersion ← TASK_VIEW_SCHEMA_VERSION；taskId ← taskId；state ← projected.state；summary ← summary；progress ← progress；checks ← checks；changedFiles ← changedFiles；nextAction ← nextAction；createdAt ← createdAt；updatedAt ← updatedAt」。不据构造形式推断物理持久化。 将「{\n      dataRoot: opts.dataRoot,\n    }」作为第 4 个实参交给已绑定接口「ts:server/services/job/job-store#getJobByQueueEntryId」，对应捕获形参「{ dataRoot }: RuntimePathOptions = {}」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「entries」的初始化来源为「(queue as LooseRecord)?.entries」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「job」存在源更新「job = null」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(typeof taskId !== "string" || !taskId)」的捕获提前退出分支为「return：null」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return null;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「opts.dataRoot」关联路径「opts.dataRoot」；只描述捕获来源，不证明当时的字段值。 将「hubRoot」作为第 1 个实参交给已绑定接口「ts:server/services/hub/hub-queue#loadQueue」，对应捕获形参「hubRoot: string」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/task/task-view.ts:615`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/7`。

### `server/services/task/task-view.ts::projectTaskView.&lt;arrow@628:21&gt;`

将「e」作为第 1 个实参交给已绑定接口「ts:core/contracts/types#isRecord」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/task/task-view.ts:628`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/8`。

### `server/services/task/task-view.ts::projectTaskView.&lt;arrow@636:19&gt;`

将「e.id」作为第 1 个实参交给已绑定接口「ts:server/services/task/task-view#stringValue」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/task/task-view.ts:636`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/9`。

**显式来源交接**（列实际样例，所有关系保留）：

- 「cli/commands/task.ts::run」的实际已绑定调用实参与确切形参声明对应，该形参由「cli/commands/task.ts::renderTaskView」的捕获字段/实参/return 来源引用；保留调用激活、当前字段值和隐藏效果边界。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/0`。
- 「cli/commands/task.ts::run」的实际已绑定调用实参与确切形参声明对应，该形参由「cli/commands/task.ts::renderTaskView」的捕获字段/实参/return 来源引用；保留调用激活、当前字段值和隐藏效果边界。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/1`。
- 「cli/commands/task.ts::run」的实际已绑定调用实参与确切形参声明对应，该形参由「cli/commands/task.ts::renderTaskView」的捕获字段/实参/return 来源引用；保留调用激活、当前字段值和隐藏效果边界。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/2`。
- 「cli/commands/task.ts::run」的实际已绑定调用实参与确切形参声明对应，该形参由「cli/commands/task.ts::autoResolveProject」的捕获字段/实参/return 来源引用；保留调用激活、当前字段值和隐藏效果边界。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/3`。
- 「cli/commands/task.ts::autoResolveProject」的捕获来源被「cli/commands/task.ts::autoResolveProject」的显式 return 消费；未据此证明调用方激活或运行结果。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/4`。
- 「cli/commands/task.ts::autoResolveProject」的捕获来源被「cli/commands/task.ts::autoResolveProject」的显式 return 消费；未据此证明调用方激活或运行结果。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/5`。
- 「cli/commands/task.ts::run」的捕获来源被「cli/commands/task.ts::run」的显式 return 消费；未据此证明调用方激活或运行结果。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/6`。
- 「cli/commands/task.ts::run」的捕获来源被「cli/commands/task.ts::run」的显式 return 消费；未据此证明调用方激活或运行结果。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/7`。

**接口复用**（列实际样例，所有关系保留）：

- 所选的 2 个确切声明通过已绑定调用复用「ts:core/contracts/types#isRecord」；复用本身不构成职责混乱或唯一资源所有权的判断。 完整引用：`/architecture/responsibility_explanations/authenticated_interface_reuse/0`。
- 所选的 2 个确切声明通过已绑定调用复用「ts:server/services/task/task-view#stringValue」；复用本身不构成职责混乱或唯一资源所有权的判断。 完整引用：`/architecture/responsibility_explanations/authenticated_interface_reuse/1`。

## 主要功能链、条件与反证

源码顺序只描述同一次调用正常到达的关系；异步完成、消息传输、远端响应和物理持久化均以实际证据范围为准。

### `cpb-task-read-projection`

分析类型：`guarded_call_sequence`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/0`；保存发现：`a8de27ed8b905f79159044bc`。

**task_entry 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `args.includes → printHelp`；`cli/commands/task.ts:263`。
- `arg.startsWith → arg.slice → positional.push`；`cli/commands/task.ts:273`。
- `console.error`；`cli/commands/task.ts:287`。
- `process.cwd`；`cli/commands/task.ts:292`。
- `autoResolveProject`；`cli/commands/task.ts:294`。
- `import`；`cli/commands/task.ts:299`。
- `projectTaskView`；`cli/commands/task.ts:300`。
- `console.error`；`cli/commands/task.ts:302`。
- `renderTaskView`；`cli/commands/task.ts:309`。

**project_selection 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `import → resolveHubRoot → loadRegistry → path.resolve → process.cwd → Object.entries → String → cwd.startsWith`；`cli/commands/task.ts:212`。
- `readFile → path.join → process.cwd → JSON.parse → pkg.name.replace(/[^a-zA-Z0-9-]/g, "-").replace → pkg.name.replace`；`cli/commands/task.ts:231`。
- `path     .basename(process.cwd())     .replace(/[^a-zA-Z0-9-]/g, "-")     .replace → path     .basename(process.cwd())     .replace → path     .basename → process.cwd`；`cli/commands/task.ts:243`。

**task_render 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `view.summary.trim`；`cli/commands/task.ts:164`。
- `humanStateLine`；`cli/commands/task.ts:166`。
- `view.progress.label.trim`；`cli/commands/task.ts:167`。
- `humanNextStep`；`cli/commands/task.ts:171`。
- `humanResultLine`；`cli/commands/task.ts:172`。
- `lines.push`；`cli/commands/task.ts:175`。
- `lines.push`；`cli/commands/task.ts:176`。
- `lines.push`；`cli/commands/task.ts:177`。
- `lines.push`；`cli/commands/task.ts:178`。
- `lines.push`；`cli/commands/task.ts:179`。
- `lines.push`；`cli/commands/task.ts:180`。
- `console.log → lines.join`；`cli/commands/task.ts:181`。

**task_projection 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `resolveHubRoot`；`server/services/task/task-view.ts:624`。
- `loadQueue`；`server/services/task/task-view.ts:625`。
- `Array.isArray → entries.filter`；`server/services/task/task-view.ts:627`。
- `entryList.find`；`server/services/task/task-view.ts:635`。
- `getJobByQueueEntryId → isRecord`；`server/services/task/task-view.ts:643`。
- `deriveStateFromJob → deriveStateFromQueueEntry`；`server/services/task/task-view.ts:658`。
- `extractGateEvidence`；`server/services/task/task-view.ts:666`。
- `finalizerReceiptPresent`；`server/services/task/task-view.ts:667`。
- `publicationProven`；`server/services/task/task-view.ts:668`。
- `buildSummary`；`server/services/task/task-view.ts:680`。
- `buildProgress`；`server/services/task/task-view.ts:681`。
- `buildChecks`；`server/services/task/task-view.ts:682`。
- 后续步骤保留在 `/functional_chains/0/pattern/sequences/task_projection`。

**queue_interface 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `loadLocalQueue`；`server/services/hub/hub-queue.ts:1466`。

**queue_read 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `readBoundedRegularFileNoFollow → queuePath → normalizeQueue → JSON.parse → errnoCode → defaultQueue → String(errnoCode(err)).startsWith → String → Object.assign → Error`；`server/services/hub/hub-queue.ts:1425`。

**linked_record_lookup 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `listJobs`；`server/services/job/job-store.ts:1376`。
- `jobs.find`；`server/services/job/job-store.ts:1377`。

**record_filter 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `Object.entries → FORBIDDEN_SET.has`；`core/contracts/task-view-fields.ts:132`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| scoped_source_supported | true | /functional_chains/0/pattern/scoped_source_supported |
| sequences/linked_record_lookup/conditions/0/branch_context | [] | /functional_chains/0/pattern/sequences/linked_record_lookup/conditions/0/branch_context |
| sequences/linked_record_lookup/conditions/0/branches/0/abrupt_source_expressions/0/kind | return_statement | /functional_chains/0/pattern/sequences/linked_record_lookup/conditions/0/branches/0/abrupt_source_expressions/0/kind |
| sequences/linked_record_lookup/conditions/0/branches/0/abrupt_source_expressions/0/runtime_completion_proven | false | /functional_chains/0/pattern/sequences/linked_record_lookup/conditions/0/branches/0/abrupt_source_expressions/0/runtime_completion_proven |
| sequences/linked_record_lookup/conditions/0/branches/0/branch | then | /functional_chains/0/pattern/sequences/linked_record_lookup/conditions/0/branches/0/branch |
| sequences/linked_record_lookup/conditions/0/branches/0/branch_all_paths_abrupt_proven | true | /functional_chains/0/pattern/sequences/linked_record_lookup/conditions/0/branches/0/branch_all_paths_abrupt_proven |
| sequences/linked_record_lookup/conditions/0/branches/0/call_ids | [] | /functional_chains/0/pattern/sequences/linked_record_lookup/conditions/0/branches/0/call_ids |
| sequences/linked_record_lookup/conditions/0/condition/kind | unary_expression | /functional_chains/0/pattern/sequences/linked_record_lookup/conditions/0/condition/kind |
| sequences/linked_record_lookup/conditions/0/condition/operands/0/kind | identifier | /functional_chains/0/pattern/sequences/linked_record_lookup/conditions/0/condition/operands/0/kind |
| sequences/linked_record_lookup/conditions/0/condition/operands/0/name | queueEntryId | /functional_chains/0/pattern/sequences/linked_record_lookup/conditions/0/condition/operands/0/name |
| sequences/linked_record_lookup/conditions/0/condition/operator | ! | /functional_chains/0/pattern/sequences/linked_record_lookup/conditions/0/condition/operator |
| sequences/linked_record_lookup/conditions/0/condition/runtime_predicate_or_assignment_proven | false | /functional_chains/0/pattern/sequences/linked_record_lookup/conditions/0/condition/runtime_predicate_or_assignment_proven |
| sequences/linked_record_lookup/conditions/0/kind | source_guard_and_abrupt_branch | /functional_chains/0/pattern/sequences/linked_record_lookup/conditions/0/kind |
| sequences/linked_record_lookup/conditions/0/role | linked_record_lookup | /functional_chains/0/pattern/sequences/linked_record_lookup/conditions/0/role |
| sequences/linked_record_lookup/conditions/0/runtime_predicate_proven | false | /functional_chains/0/pattern/sequences/linked_record_lookup/conditions/0/runtime_predicate_proven |
| sequences/linked_record_lookup/future_or_callback_activation_proven | false | /functional_chains/0/pattern/sequences/linked_record_lookup/future_or_callback_activation_proven |
| sequences/linked_record_lookup/guards/0/activation_or_termination_proven | false | /functional_chains/0/pattern/sequences/linked_record_lookup/guards/0/activation_or_termination_proven |
| sequences/linked_record_lookup/guards/0/predicate_truth_proven | false | /functional_chains/0/pattern/sequences/linked_record_lookup/guards/0/predicate_truth_proven |

所有事实及源位置：`/functional_chains/0/source_facts`；配置声明单列于 `/functional_chains/0/policy_declarations`，不作为自动证据。

## 捕获范围与未审边界

选入 333 份源码，解析 330 份。这是源码捕获与语法解析范围，不能换算成功能完整率。

| 区域 | 文件 | 已解析 |
| --- | --- | --- |
| bridges | 4 | 4 |
| cli | 1 | 1 |
| cli/commands | 21 | 21 |
| core | 1 | 1 |
| core/acp | 1 | 1 |
| core/agents | 13 | 13 |
| core/artifacts | 4 | 4 |
| core/assurance | 1 | 1 |
| core/auth | 2 | 2 |
| core/contracts | 13 | 13 |
| core/engine | 43 | 43 |
| core/evaluation | 1 | 1 |
| core/evolve | 1 | 1 |
| core/handoff | 1 | 1 |
| core/indexing | 26 | 26 |
| core/job | 1 | 1 |
| core/phases | 8 | 8 |
| core/policy | 7 | 7 |
| core/runtime | 4 | 4 |
| core/setup | 6 | 6 |
| core/triage | 2 | 2 |
| core/workflow | 17 | 17 |
| runtime/evolve | 1 | 1 |
| runtime/git | 1 | 1 |
| runtime/worker | 3 | 3 |
| scripts | 40 | 38 |
| scripts/release-gate | 3 | 3 |
| scripts/workflows | 2 | 2 |
| server | 1 | 1 |
| server/orchestrator | 7 | 7 |
| server/services | 74 | 74 |
| shared | 9 | 9 |
| shared/orchestrator | 6 | 6 |
| shared/primitives | 3 | 3 |
| shared/types | 1 | 1 |
| skills/claude-code | 2 | 1 |
| skills/hermes | 1 | 1 |
| skills/openclaw | 1 | 1 |

项目声明与依赖：`/project_declarations`；已绑定跨目录图引用：`/architecture/dependencies`。声明存在、路径可达和依赖计数均不证明业务行为通过。

- `scripts/cutover-orchestrator.sh`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `scripts/install.sh`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `skills/claude-code/install.sh`：unsupported；此源码语言不在当前分析能力或配置范围中。

配置排除：`[".git",".beads",".callscope",".test-tmp","node_modules","third_party","vendor","generated","dist","dist-tests","build","coverage","tests","__tests__","fixtures","**/*.test.ts","**/*.spec.ts","**/*.test.tsx","**/*.spec.tsx"]`。

所选局部分析：`/configured_local_assessments`；完整诊断：`/diagnostics`。未建模域保持未审，不保证全仓库无缺陷、所有权或授权完整，也不将未知标为通过。

报告生成组件：`/report_components`；原快照分析组件：`/snapshot/component_versions`。两者分别保存，历史发现不会因生成新版报告而升级。

