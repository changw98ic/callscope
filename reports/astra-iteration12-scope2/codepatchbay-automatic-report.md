# CodePatchBay — static source review：自动静态分析报告

快照：`dd5d4e3cc349b57eb87d0f810a415560bfd5f6b1022a990a35190a44d0e50ebb`；仅使用保存源码、图和静态分析证据，未执行目标、测试或构建。

## 主要发现

- **CPB-01**：提交选项与所读执行预算之间存在接线差异；参数构造、消息关系、消费者及不同重试预算分别得到源码证据，适用分支和不透明消费者保留。 完整判断=`true`；支持原有限判断=`true`；条件、反证和来源：`/judgments/0`。
- **CPB-02**：状态 `superseded` 在所选身份条件下的终态谓词结果为 `False`，权威终态集合成员关系为 `True`；消费者据此进入拒绝分支。恢复政策和权威写入保护分别保存。 完整判断=`true`；支持原有限判断=`true`；条件、反证和来源：`/judgments/1`。
- **CPB-03**：预查与权威写入的去重口径不同；从实际保护区和状态转换生成的有限交错可产生重复非终态记录，同时保存可以复用的顺序和失败条件。 完整判断=`true`；支持原有限判断=`true`；条件、反证和来源：`/judgments/2`。

原始完整 JSON 保留所有条件、反证、未知项、source facts 和保存发现身份。以下限制仅影响展示，不改变分析结果。

### CPB-01

保存发现：`b9d2fb17c08b2364997af404`；证据：`b681af29edc7822e7a2297a6`。

**推导**：`/judgments/0/derived_judgment`。

**适用条件**：`/judgments/0/conditions`。

**反证与范围**：`/judgments/0/refutations`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| all_required_modes_classified | true | /judgments/0/refutations/all_required_modes_classified |
| equal_request_value_possible | true | /judgments/0/refutations/equal_request_value_possible |
| normal_execution_or_route_activation_guaranteed | false | /judgments/0/refutations/normal_execution_or_route_activation_guaranteed |
| opaque_consumers/0/conditions | [] | /judgments/0/refutations/opaque_consumers/0/conditions |
| opaque_consumers/1/conditions | [] | /judgments/0/refutations/opaque_consumers/1/conditions |
| opaque_consumers/2/conditions | ["2c24606f30ddc0c477005ade49c8bd95:then"] | /judgments/0/refutations/opaque_consumers/2/conditions |
| opaque_consumers/3/conditions | ["7178391ef60ce9a693ef754f3c4520a5:then"] | /judgments/0/refutations/opaque_consumers/3/conditions |
| opaque_consumers/4/conditions | ["fc8d6610445843496f99748088ab8b3a:condition"] | /judgments/0/refutations/opaque_consumers/4/conditions |

**必要缺口**：`/judgments/0/necessary_gaps`。

| 必要关系 | 实际结果 |
| --- | --- |
| P1 | supported |
| P2 | supported |
| P3 | supported |
| P4 | supported |
| P5 | supported |
| P6 | supported |

### CPB-02

保存发现：`86509ebe4b1a74d001042251`；证据：`8b2a0ec1a0958f1288f56be1`。

**推导**：`/judgments/1/derived_judgment`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| status | superseded | /judgments/1/derived_judgment/status |
| authority_terminal_membership | true | /judgments/1/derived_judgment/authority_terminal_membership |
| classification_differs | true | /judgments/1/derived_judgment/classification_differs |
| kind | conditional_terminal_classification_difference | /judgments/1/derived_judgment/kind |
| recovery_is_required_or_authorized | false | /judgments/1/derived_judgment/recovery_is_required_or_authorized |
| terminal_state_can_be_illegally_mutated | false | /judgments/1/derived_judgment/terminal_state_can_be_illegally_mutated |
| valid_identity_predicate_result | false | /judgments/1/derived_judgment/valid_identity_predicate_result |

**适用条件**：`/judgments/1/conditions`。

**反证与范围**：`/judgments/1/refutations`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| authority_blocks_nonallowlisted_later_mutations/actual_later_durable_append_boundaries/0/durability_runtime_success_proven | false | /judgments/1/refutations/authority_blocks_nonallowlisted_later_mutations/actual_later_durable_append_boundaries/0/durability_runtime_success_proven |
| authority_blocks_nonallowlisted_later_mutations/allow_receiver/actual_use_instance_audit/supported | true | /judgments/1/refutations/authority_blocks_nonallowlisted_later_mutations/allow_receiver/actual_use_instance_audit/supported |
| authority_blocks_nonallowlisted_later_mutations/allow_receiver/provider_instance_audit/supported | true | /judgments/1/refutations/authority_blocks_nonallowlisted_later_mutations/allow_receiver/provider_instance_audit/supported |
| authority_blocks_nonallowlisted_later_mutations/allow_receiver/standard_environment_audit/supported | true | /judgments/1/refutations/authority_blocks_nonallowlisted_later_mutations/allow_receiver/standard_environment_audit/supported |
| authority_blocks_nonallowlisted_later_mutations/allow_receiver/standard_environment_audit/host_aliases/unsupported_container_storage_is_barrier | true | /judgments/1/refutations/authority_blocks_nonallowlisted_later_mutations/allow_receiver/standard_environment_audit/host_aliases/unsupported_container_storage_is_barrier |
| authority_blocks_nonallowlisted_later_mutations/allow_receiver/standard_environment_audit/lexical_absence/limitations | ["no captured local binding is not proof of a standard runtime value","global/member/alias effects and external mutation need separate effect guards"] | /judgments/1/refutations/authority_blocks_nonallowlisted_later_mutations/allow_receiver/standard_environment_audit/lexical_absence/limitations |
| authority_blocks_nonallowlisted_later_mutations/callback_forwarding/call_relation/function_kind/reason | null | /judgments/1/refutations/authority_blocks_nonallowlisted_later_mutations/callback_forwarding/call_relation/function_kind/reason |
| authority_blocks_nonallowlisted_later_mutations/callback_forwarding/callback_forwarding/0/call_relation/function_kind/reason | null | /judgments/1/refutations/authority_blocks_nonallowlisted_later_mutations/callback_forwarding/callback_forwarding/0/call_relation/function_kind/reason |

**必要缺口**：`/judgments/1/necessary_gaps`。

| 必要关系 | 实际结果 |
| --- | --- |
| S1 | supported |
| S2 | supported |
| S3 | supported |
| S4 | supported |
| S5 | supported |

### CPB-03

保存发现：`dabb6bfcc8ed51ec9b68286b`；证据：`ea76985490c9ee433a943733`。

**推导**：`/judgments/2/derived_judgment`。

**适用条件**：`/judgments/2/conditions`。

**反证与范围**：`/judgments/2/refutations`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| bounded_cases/0/duplicate_witness/resulting_rows/0/status | scheduled | /judgments/2/refutations/bounded_cases/0/duplicate_witness/resulting_rows/0/status |
| bounded_cases/0/duplicate_witness/resulting_rows/0/abstract_version | 1 | /judgments/2/refutations/bounded_cases/0/duplicate_witness/resulting_rows/0/abstract_version |
| bounded_cases/0/duplicate_witness/resulting_rows/0/request | 0 | /judgments/2/refutations/bounded_cases/0/duplicate_witness/resulting_rows/0/request |
| bounded_cases/0/duplicate_witness/resulting_rows/1/status | pending | /judgments/2/refutations/bounded_cases/0/duplicate_witness/resulting_rows/1/status |
| bounded_cases/0/duplicate_witness/resulting_rows/1/abstract_version | 0 | /judgments/2/refutations/bounded_cases/0/duplicate_witness/resulting_rows/1/abstract_version |
| bounded_cases/0/duplicate_witness/resulting_rows/1/request | 1 | /judgments/2/refutations/bounded_cases/0/duplicate_witness/resulting_rows/1/request |
| bounded_cases/0/duplicate_witness/steps/0/actor | request-0 | /judgments/2/refutations/bounded_cases/0/duplicate_witness/steps/0/actor |
| bounded_cases/0/duplicate_witness/steps/0/observed_rows | 0 | /judgments/2/refutations/bounded_cases/0/duplicate_witness/steps/0/observed_rows |

**必要缺口**：`/judgments/2/necessary_gaps`。

| 必要关系 | 实际结果 |
| --- | --- |
| A1 | supported |
| A2 | supported |
| A3 | supported |
| A4 | supported |
| A5 | supported |
| A6 | supported |
| A7 | supported |

## 具体职责与接口交接

以下正文由所选声明的实际记录字段、赋值、实参接口和提前退出条件生成。目录名只供导航；普通调用、消息字段、执行、交付和投影分别保留。

完整职责、所有操作和来源：`/architecture/responsibility_explanations`。

### `bridges/engine-bridge.ts::runJobWithServices`

将「opts」作为第 1 个实参交给已绑定接口「ts:server/services/engine-runner#runJobWithServices」，对应捕获形参「opts: LooseRecord」。该普通调用关系不替代进程或网络协议关系。 以「return runJobWithServerServices(opts);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`bridges/engine-bridge.ts:18`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/0`。

### `cli/commands/doctor.ts::checkRuntimeHealth`

构造捕获记录，字段按源码次序为「cpbRoot ← cpbRoot；executorRoot ← executorRoot」。不据构造形式推断物理持久化。 在调用形式「collectRuntimeHealth」中提供第 1 个实参「{ cpbRoot, executorRoot }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 包含赋值/更新「results.runtimeHealth = health」，捕获目标为「results.runtimeHealth」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「health」的初始化来源为「await collectRuntimeHealth({ cpbRoot, executorRoot })」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以字段投影形式「cpbRoot」关联路径「cpbRoot」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「4fb2e5ba687652f9093b732e」先于语句位置「1」的操作「1e027a34369b10733aed2b38」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`cli/commands/doctor.ts:306`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/1`。

### `cli/commands/fix.ts::resolveDeps`

构造捕获记录，字段按源码次序为「assertFixReadiness ← o.assertFixReadiness ?? readinessMod.assertFixReadiness；enqueue ← o.enqueue ?? (hubQueueMod.enqueue as unknown as FixDeps["enqueue"])；loadQueue ← o.loadQueue ?? (hubQueueMod.loadQueue as unknown as FixDeps["loadQueue"])；loadRegistry ← o.loadRegistry ?? (hubRegistryMod.loadRegistry as unknown as FixDeps["loadRegistry"])；resolveHubRoot ← o.resolveHubRoot ?? hubRegistryMod.resolveHubRoot；projectTaskView ← o.projectTaskView ?? taskViewMod.projectTaskView；resolveTaskRoute ← o.resolveTaskRoute ?? (autoRouteMod.resolveTaskRoute as unknown as FixDeps["resolveTaskRoute"])」。不据构造形式推断物理持久化。 在调用形式「Promise.all」中提供第 1 个实参「[\n    import("../../server/services/task/readiness.js"),\n    import("../../server/services/hub/hub-queue.js"),\n    import("../../server/services/hub/hub-registry.js"),\n    import("../../server/services/task/task-view.js"),\n    import("../../core/workflow/auto-route.js"),\n  ]」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「o」的初始化来源为「ctx.deps ?? {}」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return {\n    assertFixReadiness: o.assertFixReadiness ?? readinessMod.assertFixReadiness,\n    enqueue: o.enqueue ?? (hubQueueMod.enqueue as unknown as FixDeps["enqueue"]),\n    loadQueue: o.loadQueue ?? (hubQueueMod.loadQueue as unknown as FixDeps["loadQueue"]),\n    loadRegistry:\n      o.loadRegistry ?? (hubRegistryMod.loadRegistry as unknown as FixDeps[…［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「aec110ec9a30c1c9f80e68bd」先于语句位置「1」的操作「3f6e67f016a8f9f8e5b40130」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`cli/commands/fix.ts:426`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/2`。

### `cli/commands/fix.ts::isReadinessFailure`

以「return r.ok === false;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`cli/commands/fix.ts:465`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/3`。

### `cli/commands/fix.ts::run`

构造捕获记录，字段按源码次序为「task ← parsed.problem；workflow ← "standard"；planMode ← "auto"；triageMode ← null；workflowExplicit ← false；planModeExplicit ← false；actor ← "cli"」。不据构造形式推断物理持久化。 将「projectEntries」作为第 1 个实参交给已绑定接口「ts:core/contracts/idempotency#selectIdempotentEntry」，对应捕获形参「entries: readonly T[]」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「project」的初始化来源为「parsed.project」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「project」存在源更新「project = await autoDetectProject(deps.loadRegistry, hubRoot, path.resolve(process.cwd()))」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(parsed.help)」的捕获提前退出分支为「return：ExitCode.FixAccepted」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return ExitCode.FixAccepted;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「cpbRoot」关联路径「cpbRoot」；只描述捕获来源，不证明当时的字段值。 将「ctx」作为第 1 个实参交给已绑定接口「ts:cli/commands/fix#resolveDeps」，对应捕获形参「ctx: FixCtx」。该普通调用关系不替代进程或网络协议关系。

源码：`cli/commands/fix.ts:469`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/4`。

### `cli/commands/pipeline.ts::parseCommonFlags`

构造捕获记录，字段按源码次序为「positional ← positional；workflow ← workflow；planMode ← planMode；triageMode ← triageMode；workflowExplicit ← workflowExplicit；planModeExplicit ← planModeExplicit；retries ← retries；agent ← agent；model ← model；planAgent ← planAgent；executeAgent ← executeAgent；verifyAgent ← verifyAgent」；其余字段见完整操作。不据构造形式推断物理持久化。 在调用形式「positional.push」中提供第 1 个实参「arg」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「i」的初始化来源为「0」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「i」存在源更新「i++」；循环和分支条件见操作上下文，未推执行次数或最终数值。 以「return {\n    positional,\n    workflow,\n    planMode,\n    triageMode,\n    workflowExplicit,\n    planModeExplicit,\n    retries,\n    agent,\n    model,\n    planAgent,\n    executeAgent,\n    verifyAgent,\n    reviewAgent,\n    project,\n    planVariant,\n    executeVariant,\n    verifyVariant,\n    reviewVariant,\n    issueNumber,\n    issueUrl,\n    r…［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「positional」关联路径「positional」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「a412b5876d34e855806af70b」先于语句位置「1」的操作「0a5d381acaf518e44f54bdac」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`cli/commands/pipeline.ts:36`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/5`。

### `cli/commands/pipeline.ts::run`

构造捕获记录，字段按源码次序为「source ← "cli"；workflow ← route.workflow；planMode ← route.planMode；triageMode ← parsed.triageMode；routeDecision ← route.decision || undefined；actor ← "cli"；autoFinalize ← true；agent ← parsed.agent || undefined；model ← parsed.model || undefined；maxRetries ← parsed.retries；issueNumber ← parsed.issueNumber ? Number(parsed.issueNumber) : null；issueUrl ← parsed.issueUrl || null」；其余字段见完整操作。不据构造形式推断物理持久化。 将「args」作为第 1 个实参交给已绑定接口「ts:cli/commands/pipeline#parseCommonFlags」，对应捕获形参「args: string[]」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「parsed」的初始化来源为「parseCommonFlags(args)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「registered」存在源更新「registered = null」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(args.includes("--help") || args.includes("-h"))」的捕获提前退出分支为「return：0」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return 0;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「task」关联路径「task」；只描述捕获来源，不证明当时的字段值。

源码：`cli/commands/pipeline.ts:134`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/6`。

### `cli/commands/task.ts::renderTaskView`

将「view.state」作为第 1 个实参交给已绑定接口「ts:cli/commands/task#humanStateLine」，对应捕获形参「state: TaskStateValue」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「rawSummary」的初始化来源为「typeof view.summary === "string" ? view.summary.trim() : ""」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留同一块中的正常源码顺序：语句位置「0」的操作「f16404dee785d00e8185708e」先于语句位置「1」的操作「f65b18943f29608bf83ca875」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`cli/commands/task.ts:163`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/7`。

### `cli/commands/task.ts::autoResolveProject`

构造捕获的空记录「{}」；没有从空记录形式推断额外字段或持久效果。 在调用形式「resolveHubRoot」中提供第 1 个实参「cpbRoot」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「src」的初始化来源为「proj?.sourcePath ? path.resolve(String(proj.sourcePath)) : null」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(src &amp;&amp; (src === cwd || cwd.startsWith(src + path.sep)))」的捕获提前退出分支为「return：id」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return id;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「09b803171d53f2470091a403」先于语句位置「1」的操作「e0609d80e8fa52384917c5c0」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`cli/commands/task.ts:210`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/8`。

### `cli/commands/task.ts::run`

将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:cli/commands/task#autoResolveProject」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「i」的初始化来源为「0」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「i」存在源更新「i++」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(args.includes("--help") || args.includes("-h"))」的捕获提前退出分支为「return：0」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return 0;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「5bce1e489095b51834cb5bfd」先于语句位置「1」的操作「efbc8765c29ff4c96fd36708」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「view」作为第 1 个实参交给已绑定接口「ts:cli/commands/task#renderTaskView」，对应捕获形参「view: TaskView」。该普通调用关系不替代进程或网络协议关系。

源码：`cli/commands/task.ts:259`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/9`。

### `cli/cpb.ts::main`

构造捕获记录，字段按源码次序为「cpbRoot ← CPB_ROOT；executorRoot ← CPB_EXECUTOR_ROOT；command ← cmd」。不据构造形式推断物理持久化。 将「cmd」作为第 1 个实参交给已绑定接口「ts:cli/cpb#projectArgForCommand」，对应捕获形参「cmd: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「PROJECT_COMMANDS」的初始化来源为「new Set(["pipeline", "fix", "task", "status", "retry", "diff", "review", "inbox", "cancel", "redirect"])」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「cmd」存在源更新「cmd = "version"」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!project?.projectRuntimeRoot)」的捕获提前退出分支为「throw：new Error(`project runtime root required for project '${projectArg}'`)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return args.length === 0 ? undefined : 0;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「CPB_ROOT」关联路径「CPB_ROOT」；只描述捕获来源，不证明当时的字段值。

源码：`cli/cpb.ts:127`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/10`。

### `core/agents/agent-runner.ts::readOnlyMutationViolation`

构造捕获记录，字段按源码次序为「auditFile ← auditFile；phase ← phase；title ← typeof event.title === "string" ? event.title : undefined；status ← typeof event.status === "string" ? event.status : undefined；targetPath ← "&lt;provider-did-not-report-path&gt;"；allowedRoots ← allowedRoots」。不据构造形式推断物理持久化。 将「JSON.parse(line)」作为第 1 个实参交给已绑定接口「ts:shared/types#recordValue」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「eventSessionId」的初始化来源为「typeof event.sessionId === "string" ? event.sessionId : null」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「event」存在源更新「event = recordValue(JSON.parse(line))」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!isReadOnlyPhase(phase) || typeof auditFile !== "string" || !auditFile.trim())」的捕获提前退出分支为「return：null」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return null;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「auditFile」关联路径「auditFile」；只描述捕获来源，不证明当时的字段值。

源码：`core/agents/agent-runner.ts:206`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/11`。

### `core/agents/agent-runner.ts::readOnlyMutationViolation.&lt;loop@229:2&gt;.&lt;block@229:38&gt;.&lt;arrow@257:26&gt;`

将「targetPath」作为第 1 个实参交给已绑定接口「ts:core/agents/agent-runner#pathWithin」，对应捕获形参「candidate: string」。该普通调用关系不替代进程或网络协议关系。

源码：`core/agents/agent-runner.ts:257`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/12`。

### `core/agents/agent-runner.ts::allowedAgentsFromEnv`

在调用形式「JSON.parse」中提供第 1 个实参「value」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「parsed」的初始化来源为「JSON.parse(value)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(value === undefined || value === null)」的捕获提前退出分支为「return：null」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return null;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「a5d703605a2e0ffabf89cc04」先于语句位置「1」的操作「ef9d4fe0d18714aaee2ad0b5」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`core/agents/agent-runner.ts:332`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/13`。

### `core/agents/agent-runner.ts::allowedAgentsFromEnv.&lt;block@335:6&gt;.&lt;arrow@340:11&gt;`

以无显式实参的调用形式「entry.trim」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`core/agents/agent-runner.ts:340`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/14`。

### `core/agents/agent-runner.ts::poolWithExecute`

将「value」作为第 1 个实参交给已绑定接口「ts:core/agents/agent-runner#isErrorObject」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 条件「(!isErrorObject(value) || typeof value.execute !== "function")」的捕获提前退出分支为「return：null」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return null;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「60f27945383c5f7a5a871696」先于语句位置「1」的操作「5b9329fca11f147ba8dee643」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`core/agents/agent-runner.ts:347`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/15`。

### `core/agents/agent-runner.ts::phaseWriteAllowOverride`

具有捕获记录构造「{ ...recordValue(env) }」；该记录的可枚举字段为空或保留开放形状，未把展开来源补成确定字段。 将「env」作为第 1 个实参交给已绑定接口「ts:shared/types#recordValue」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「baseEnv.CPB_ACP_WRITE_ALLOW = writeAllow」，捕获目标为「baseEnv.CPB_ACP_WRITE_ALLOW」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「sandboxPolicy」的初始化来源为「"cpb-required"」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「sandboxPolicy」存在源更新「sandboxPolicy = getCapability(agentName)?.sandboxPolicy || "cpb-required"」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!isReadOnlyPhase(phase))」的捕获提前退出分支为「return：baseEnv」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return baseEnv;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`core/agents/agent-runner.ts:357`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/16`。

### `core/agents/agent-runner.ts::runAgent`

构造捕获记录，字段按源码次序为「phase ← phaseName；role ← roleName；bypass ← false；projectId ← project；jobId ← jobId；attemptId ← attemptId；conversationKey ← typeof conversationKey === "string" &amp;&amp; conversationKey ? conversationKey : undefined；variant ← variant；provider ← provider；model ← model；workspaceId ← typeof scopeRecord.workspaceId === "string" ? scopeRecord.workspaceId : undefined；cwd ← cwd」；其余字段见完整操作。不据构造形式推断物理持久化。 将「scope」作为第 1 个实参交给已绑定接口「ts:shared/types#recordValue」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「startedAt」的初始化来源为「Date.now()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!execPool)」的捕获提前退出分支为「throw：new TypeError("agent pool does not expose execute()")」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return {\n      ok: false,\n      kind: FailureKind.AGENT_UNAVAILABLE,\n      reason: `agent ${agentName || "unknown"} is outside allowed agent policy`,\n      retryable: false,\n      agent: agentName,\n      diagnostics: {\n        elapsedMs: Date.now() - startedAt,\n        agent: agentName,\n        role: roleName,\n        hardGate: true,\n        allow…［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「FailureKind.AGENT_UNAVAILABLE」关联路径「FailureKind.AGENT_UNAVAILABLE」；只描述捕获来源，不证明当时的字段值。 记录消息形状中的固定文本字段「kind」及捕获形式「FailureKind.AGENT_UNAVAILABLE」。单个文本字段不是跨语言调用或传输成功的证明。 将「{\n      auditFile: execRecord.acpAuditFile,\n      phase: phaseName,\n      cwd: typeof cwd === "string" ? cwd : process.cwd(),\n      env: executionEnv,\n      startedAt,\n      sessionId: execRecord.sessionId,\n    }」作为第 1 个实参交给已绑定接口「ts:core/agents/agent-runner#readOnlyMutationViolation」，对应捕获形参「{\n  auditFile,\n  phase,\n  cwd,\n  env,\n  startedAt,\n  sessionId,\n}: {\n  auditFile: unknown;\n  phase: string;\n  cwd: string;\n  env: LooseRecord;\n  startedAt: number;\n  sessionId: unknown;\n}」。该普通调用关系不替代进程或网络协议关系。

源码：`core/agents/agent-runner.ts:475`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/17`。

### `core/agents/agent-runner.ts::classifyError`

构造捕获记录，字段按源码次序为「untilTs ← untilTs；status ← errorRecord.status || null；providerKey ← errorRecord.providerKey || agent；nextEligibleAt ← errorRecord.nextEligibleAt || untilTs；source ← errorRecord.source || null；confidence ← errorRecord.confidence ?? null；stdout ← errorRecord.partialStdout || ""；stderr ← errorRecord.partialStderr || ""」。不据构造形式推断物理持久化。 将「err」作为第 1 个实参交给已绑定接口「ts:shared/types#recordValue」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「untilTs」的初始化来源为「errorRecord.untilTs || errorRecord.nextEligibleAt || parseResetTime(msg)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(hardConstraintKind)」的捕获提前退出分支为「return：{\n      ok: false,\n      kind: hardConstraintKind,\n      reason: msg,\n      retryable: true,\n      agent,\n      diagnostics: diagnostics({ stderrSnippet: snippet }),\n    }」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return {\n      ok: false,\n      kind: hardConstraintKind,\n      reason: msg,\n      retryable: true,\n      agent,\n      diagnostics: diagnostics({ stderrSnippet: snippet }),\n    };」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「hardConstraintKind」关联路径「hardConstraintKind」；只描述捕获来源，不证明当时的字段值。 记录消息形状中的固定文本字段「kind」及捕获形式「FailureKind.AGENT_RATE_LIMITED」。单个文本字段不是跨语言调用或传输成功的证明。 将「{ stderrSnippet: snippet }」作为第 1 个实参交给已绑定接口「ts:core/agents/agent-runner#classifyError.diagnostics」，对应捕获形参「extra = {}」。该普通调用关系不替代进程或网络协议关系。

源码：`core/agents/agent-runner.ts:600`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/18`。

### `core/agents/agent-runner.ts::classifyError.diagnostics`

构造捕获的空记录「{}」；没有从空记录形式推断额外字段或持久效果。 以字段投影形式「elapsedMs」关联路径「elapsedMs」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「extra」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。

源码：`core/agents/agent-runner.ts:606`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/19`。

### `core/artifacts/artifact-store.ts::writeArtifact`

构造捕获记录，字段按源码次序为「committed ← true as const；cleanupPending ← result.cleanupPending；commitWarnings ← result.commitWarnings；retryCleanup ← result.retryCleanup」。不据构造形式推断物理持久化。 将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:core/artifacts/artifact-store#prepareArtifactWrite」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「prepared」的初始化来源为「await prepareArtifactWrite(cpbRoot, input)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!isArtifactCommitOutcome(result))」的捕获提前退出分支为「return：result」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return result;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「result.cleanupPending」关联路径「result.cleanupPending」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「result.artifact」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。

源码：`core/artifacts/artifact-store.ts:434`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/20`。

### `core/contracts/idempotency.ts::isTerminalQueueStatus`

在调用形式「TERMINAL_SET.has」中提供第 1 个实参「status」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return typeof status === "string" &amp;&amp; TERMINAL_SET.has(status);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`core/contracts/idempotency.ts:72`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/21`。

### `core/contracts/idempotency.ts::selectIdempotentEntry`

将「entry?.status」作为第 1 个实参交给已绑定接口「ts:core/contracts/idempotency#isTerminalQueueStatus」，对应捕获形参「status: unknown」。该普通调用关系不替代进程或网络协议关系。 以「return entry;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「1」的操作「e277bec546d730cf14afae94」先于语句位置「2」的操作「69caab36ac5625bced2a157a」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`core/contracts/idempotency.ts:113`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/22`。

### `core/contracts/task-view-fields.ts::sanitizeTaskView`

构造捕获的空记录「{}」；没有从空记录形式推断额外字段或持久效果。 在调用形式「Object.entries」中提供第 1 个实参「raw」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「out」的初始化来源为「{}」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return out;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「213207ae180b3454583a5d40」先于语句位置「1」的操作「1f7d9f3350233041759e2f30」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`core/contracts/task-view-fields.ts:128`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/23`。

### `core/engine/completion-gate.ts::isMutatingJob`

捕获 binding「mode」的初始化来源为「job.planMode」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!job)」的捕获提前退出分支为「return：false」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return false」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「3093d6427fc131622fb8b94d」先于语句位置「1」的操作「465ec9d3a0b6100a3454ead5」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`core/engine/completion-gate.ts:107`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/24`。

### `core/engine/completion-gate.ts::evaluateCompletionGate`

构造捕获记录，字段按源码次序为「checklist ← checklist；verdict ← checklistVerdict；evidenceLedger ← evidenceLedger；executionMap ← executionMap；runtimeFailures ← runtimeFailures；attemptId ← attemptId；multiAttempt ← multiAttempt」。不据构造形式推断物理持久化。 将「{\n        ...details,\n        checklist: checklistResult,\n      }」作为第 4 个实参交给已绑定接口「ts:core/engine/completion-gate#gateResult」，对应捕获形参「details: CompletionGateDetails」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「checklistResult」的初始化来源为「evaluateChecklistCompletion({\n      checklist,\n      verdict: checklistVerdict,\n      evidenceLedger,\n      executionMap,\n      runtimeFailures,\n      attemptId,\n      multiAttempt,\n    })」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(checklistResult.outcome !== "complete")」的捕获提前退出分支为「return：gateResult(checklistResult.outcome || "checklist_invalid", checklistResult.reason || "checklist completion failed", ["checklist"], {\n        ...details,\n        checklist: checklistResult,\n      })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return gateResult(checklistResult.outcome || "checklist_invalid", checklistResult.reason || "checklist completion failed", ["checklist"], {\n        ...details,\n        checklist: checklistResult,\n      });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「checklist」关联路径「checklist」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「details」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。 将「job」作为第 1 个实参交给已绑定接口「ts:core/engine/completion-gate#isMutatingJob」，对应捕获形参「job: CompletionGateJob | null | undefined」。该普通调用关系不替代进程或网络协议关系。

源码：`core/engine/completion-gate.ts:140`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/25`。

### `core/engine/completion-gate.ts::evaluateCompletionGate.&lt;arrow@173:72&gt;`

在调用形式「Boolean」中提供第 1 个实参「phase」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`core/engine/completion-gate.ts:173`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/26`。

### `core/engine/completion-gate.ts::gateResult`

构造捕获记录，字段按源码次序为「outcome ← outcome；reason ← reason；missingGates ← missingGates；details ← details」。不据构造形式推断物理持久化。 以「return { outcome, reason, missingGates, details }」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「outcome」关联路径「outcome」；只描述捕获来源，不证明当时的字段值。

源码：`core/engine/completion-gate.ts:323`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/27`。

### `core/engine/phase-retry.ts::runPhaseRetryLoops`

构造捕获记录，字段按源码次序为「type ← "phase_agent_fallback_blocked"；jobId ← n.jobId；project ← n.project；phase ← n.phase；role ← n.role；fromAgent ← selectedAgentForPhase(ctx, activeState) || "unknown"；blockedAgent ← fallbackAgent；allowedAgents ← allowedAgents；reason ← `fallback agent ${fallbackAgent} is outside allowed agent policy`」。不据构造形式推断物理持久化。 将「result」作为第 1 个实参交给已绑定接口「ts:core/engine/phase-retry#runPhaseRetryLoops.prepareRecovery」，对应捕获形参「currentResult: PhaseResult」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「runPhase」的初始化来源为「deps.runPhase」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「phaseAgentFallback」存在源更新「phaseAgentFallback = {\n      applied: true,\n      count: 1,\n      fromAgent,\n      toAgent: fallbackAgent,\n      failureKind: retry.failureKind,\n      reason: retry.failureReason,\n    }」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!runPhase)」的捕获提前退出分支为「throw：new Error("runPhase dependency is required for phase retry loops")」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new Error("runPhase dependency is required for phase retry loops");」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「n.jobId」关联路径「n.jobId」；只描述捕获来源，不证明当时的字段值。 将「prepared.recovery」作为第 1 个实参交给已绑定接口「ts:core/engine/phase-retry#runPhaseRetryLoops.recoveryFields」，对应捕获形参「recovery: FailureRecoveryDecision」。该普通调用关系不替代进程或网络协议关系。

源码：`core/engine/phase-retry.ts:363`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/28`。

### `core/engine/phase-retry.ts::runPhaseRetryLoops.&lt;arrow@372:53&gt;`

将「env」作为第 1 个实参交给已绑定接口「ts:core/engine/phase-retry#configuredRetryBaseDelayMs」，对应捕获形参「env: NodeJS.ProcessEnv」。该普通调用关系不替代进程或网络协议关系。

源码：`core/engine/phase-retry.ts:372`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/29`。

### `core/engine/phase-retry.ts::runPhaseRetryLoops.&lt;arrow@374:27&gt;`

以无显式实参的调用形式「new Date().toISOString」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`core/engine/phase-retry.ts:374`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/30`。

### `core/engine/phase-retry.ts::runPhaseRetryLoops.prepareRecovery`

构造捕获记录，字段按源码次序为「type ← "retry_decision"；jobId ← n.jobId；project ← n.project；phase ← n.phase；role ← n.role；action ← "stop_retry_budget_exhausted"；retryClass ← retryClass；attempt ← attempt；retryCount ← phaseRetryCount；maxRetries ← phaseRetryTotalMax；reason ← `phase retry budget exhausted (${phaseRetryCount}/${phaseRetryTotalMax})`；ts ← now()」。不据构造形式推断物理持久化。 将「{\n      failure: currentResult.failure,\n      previousFingerprint,\n      previousStrategy,\n      preferredStrategy,\n      scope: "phase",\n    }」作为第 1 个实参交给已绑定接口「ts:core/contracts/failure-recovery#selectFailureRecovery」，对应捕获形参「{\n  failure,\n  previousFingerprint = null,\n  previousStrategy = null,\n  preferredStrategy = null,\n  scope = "queue",\n}: {\n  failure: unknown;\n  previousFingerprint?: string | null;\n  previousStrategy?: string | null;\n  preferredStrategy?: string | null;\n  scope?: RecoveryScope;\n}」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「recovery」的初始化来源为「selectFailureRecovery({\n      failure: currentResult.failure,\n      previousFingerprint,\n      previousStrategy,\n      preferredStrategy,\n      scope: "phase",\n    })」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「previousFingerprint」存在源更新「previousFingerprint = recovery.failureFingerprint」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(phaseRetryCount &gt;= phaseRetryTotalMax)」的捕获提前退出分支为「return：null」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return null;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「retryClass」关联路径「retryClass」；只描述捕获来源，不证明当时的字段值。

源码：`core/engine/phase-retry.ts:389`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/31`。

### `core/engine/phase-retry.ts::runPhaseRetryLoops.recoveryFields`

构造捕获记录，字段按源码次序为「failureClass ← recovery.failureClass；failureFingerprint ← recovery.failureFingerprint；retryStrategy ← recovery.retryStrategy；strategyChanged ← recovery.strategyChanged；forceFreshSession ← recovery.forceFreshSession；failureEvidence ← recovery.failureEvidence」。不据构造形式推断物理持久化。 以字段投影形式「recovery.failureClass」关联路径「recovery.failureClass」；只描述捕获来源，不证明当时的字段值。

源码：`core/engine/phase-retry.ts:454`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/32`。

### `core/engine/run-job-execute-dag.ts::runVerificationInfrastructureRetryLoop`

构造捕获记录，字段按源码次序为「type ← "verification_infrastructure_retry_started"；jobId ← session.jobId；project ← session.project；attemptId ← session.attemptId || null；iteration ← iteration；phase ← verificationOutcome.phase；failureFingerprint ← feedback.failureFingerprint；candidateId ← frozenCandidateId；candidateMutationAllowed ← false；ts ← ts()」。不据构造形式推断物理持久化。 将「initialFailure.result」作为第 1 个实参交给已绑定接口「ts:core/engine/solver-loop#verificationInfrastructureFailureFingerprint」，对应捕获形参「result: PhaseResult」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「session.phaseSourceContext = originalSourceContext」，捕获目标为「session.phaseSourceContext」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「originalSourceContext」的初始化来源为「session.phaseSourceContext」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「retryOutcome」存在源更新「retryOutcome = outcome」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!initialFailure.result)」的捕获提前退出分支为「return：finishDeferredVerificationFailure(session, initialFailure)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return finishDeferredVerificationFailure(session, initialFailure);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`core/engine/run-job-execute-dag.ts:990`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/33`。

### `core/engine/run-job.ts::runJob`

构造捕获记录，字段按源码次序为「cpbRoot ← ctx.cpbRoot；project ← ctx.project || "unknown"；jobId ← result?.jobId || ctx._jobId；attemptId ← ctx._attemptId || result?.jobId || ctx._jobId；appendEvent ← ctx.appendEvent；result ← result；sourceContext ← ctx.sourceContext ?? undefined」。不据构造形式推断物理持久化。 将「ctx」作为第 1 个实参交给已绑定接口「ts:core/engine/run-job#runJobInner」，对应捕获形参「ctx: RunJobContext」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「ctx」的初始化来源为「ctxInput as RunJobContext」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!isRecord(ctxInput))」的捕获提前退出分支为「throw：new TypeError("runJob context must be an object")」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new TypeError("runJob context must be an object");」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「ctx.cpbRoot」关联路径「ctx.cpbRoot」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「29391929d25bf3419c54c723」先于语句位置「1」的操作「33ea26fce7b195b7d75095b2」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`core/engine/run-job.ts:65`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/34`。

### `core/engine/run-job.ts::runJobInner`

构造捕获记录，字段按源码次序为「type ← "scheduler_decision_applied"；jobId ← jobId；project ← ctx.project；attemptId ← attemptId；queueEntryId ← sourceContext?.queueEntryId || null；mode ← typeof schedulerDecision.mode === "string" ? schedulerDecision.mode : undefined；rank ← schedulerDecision.rank ?? null；score ← schedulerDecision.score ?? null；reasons ← Array.isArray(schedulerDecision.reasons) ? schedulerDecision.reasons : []；retryStrategy ← schedulerDecision.retryStrategy || null；failureFingerprint ← schedulerDecision.failureFingerprint || null；failureClass ← schedulerDecision.failureClass || null」；其余字段见完整操作。不据构造形式推断物理持久化。 将「ctx」作为第 1 个实参交给已绑定接口「ts:core/engine/run-job-prepare#createJobAndHandleBlocked」，对应捕获形参「ctx: RunJobPrepareContext」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「ctx.jobId = jobId」，捕获目标为「ctx.jobId」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「created」的初始化来源为「await createJobAndHandleBlocked(ctx)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「phaseSourceContext」存在源更新「phaseSourceContext = assurance.phaseSourceContext」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(created.kind === "blocked")」的捕获提前退出分支为「return：created.result」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return created.result;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`core/engine/run-job.ts:109`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/35`。

### `core/phases/verify.ts::buildEvidenceLedger`

构造捕获记录，字段按源码次序为「schemaVersion ← 1；jobId ← jobId；project ← project；attemptId ← attemptId；ledgerId ← ledgerId；finalWorktree ← finalWorktree；evidence ← []」。不据构造形式推断物理持久化。 将「{ attemptId, finalWorktree }」作为第 3 个实参交给已绑定接口「ts:core/workflow/evidence-probes#validateEvidenceObservation」，对应捕获形参「{ attemptId, finalWorktree }: LooseRecord = {}」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「checklistItem」的初始化来源为「checklist.items.find((item) =&gt; item.id === probe.checklistId)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「index」存在源更新「index++」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!checklist)」的捕获提前退出分支为「return：{ schemaVersion: 1, jobId, project, attemptId, ledgerId, finalWorktree, evidence: [] }」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return { schemaVersion: 1, jobId, project, attemptId, ledgerId, finalWorktree, evidence: [] };」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「jobId」关联路径「jobId」；只描述捕获来源，不证明当时的字段值。

源码：`core/phases/verify.ts:1117`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/36`。

### `core/phases/verify.ts::runVerify`

构造捕获记录，字段按源码次序为「project ← project；jobId ← jobId；phase ← "verify"；role ← role；agent ← resolvedAgent.agent；prompt ← prompt；dataRoot ← dataRoot；signal ← ctx.signal as AbortSignal | undefined」。不据构造形式推断物理持久化。 将「{\n        acceptanceChecklist,\n        hardGateChecks,\n        attemptId,\n        finalWorktree: verificationEvidence.git,\n      }」作为第 1 个实参交给已绑定接口「ts:core/workflow/evidence-probes#buildEvidenceProbePlan」，对应捕获形参「{ acceptanceChecklist, hardGateChecks = [], attemptId }: LooseRecord」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「verifierCwd」的初始化来源为「cwd」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「acceptanceChecklist」存在源更新「acceptanceChecklist = ctx.sourceContext.acceptanceChecklist」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「((err as Error | undefined)?.name === "AbortError")」的捕获提前退出分支为「throw：err」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return phaseFailed({\n      phase: "verify",\n      failure: failure({\n        kind: FailureKind.VERIFICATION_FAILED,\n        phase: "verify",\n        reason,\n        retryable: false,\n        cause: {\n          planRequired: true,\n          plan: planEvidence,\n        },\n      }),\n      diagnostics: { planRequired: planEvidence },\n    });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「acceptanceChecklist」关联路径「acceptanceChecklist」；只描述捕获来源，不证明当时的字段值。 将「{\n      signal: ctx.signal as AbortSignal | undefined,\n      project,\n      jobId,\n      kind: "evidence-ledger",\n      content: JSON.stringify(evidenceLedger, null, 2),\n      dataRoot,\n      metadata: evidenceLedger,\n    }」作为第 2 个实参交给已绑定接口「ts:core/artifacts/artifact-store#writeArtifact」，对应捕获形参「input: ArtifactWriteInput」。该普通调用关系不替代进程或网络协议关系。

源码：`core/phases/verify.ts:1326`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/37`。

### `core/phases/verify.ts::runVerify.&lt;object@1620:38&gt;.operation`

构造捕获记录，字段按源码次序为「cwd ← verificationReplay.replayPath；base ← expectedCandidate?.baseSha || "HEAD"；env ← runtimeEnv」。不据构造形式推断物理持久化。 将「{\n      phase: "verify",\n      role,\n      ...resolvedAgent,\n      project,\n      jobId,\n      prompt,\n      cwd: verifierCwd,\n      pool,\n      timeoutMs: ctx.timeouts?.verify ?? 0,\n      scope: ctx.scope,\n      env: verifierEnv,\n      dataRoot,\n      onProgress: ctx.onProgress,\n      attemptId: ctx.attemptId,\n      conversationKey: verificat…［展示截断；完整操作保留］」作为第 1 个实参交给已绑定接口「ts:core/agents/agent-runner#runAgent」，对应捕获形参「{\n  phase,\n  role,\n  agent,\n  variant,\n  provider,\n  model,\n  project,\n  jobId,\n  prompt,\n  cwd,\n  pool,\n  timeoutMs = DEFAULT_TIMEOUT_MS,\n  scope,\n  env,\n  dataRoot = null,\n  onProgress = null,\n  conversationKey = null,\n  attemptId = null,\n  signal = null,\n}: LooseRecord」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「replayCandidate」的初始化来源为「await captureCandidateArtifact({\n            cwd: verificationReplay.replayPath,\n            base: expectedCandidate?.baseSha || "HEAD",\n            env: runtimeEnv,\n          })」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「replayCaptureError」存在源更新「replayCaptureError = err」；循环和分支条件见操作上下文，未推执行次数或最终数值。 以字段投影形式「role」关联路径「role」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「resolvedAgent」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「ee6d20d2eaed38fd5c446ef4」先于语句位置「1」的操作「f9224c1a9b2082bb9f8f348d」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`core/phases/verify.ts:1623`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/38`。

### `core/phases/verify.ts::runVerify.&lt;block@1833:27&gt;.&lt;block@1953:33&gt;.&lt;block@1954:10&gt;.&lt;object@1955:73&gt;.&lt;arrow@1959:56&gt;`

将「file」作为第 1 个实参交给已绑定接口「ts:core/phases/verify#stringValue」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。

源码：`core/phases/verify.ts:1959`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/39`。

### `core/phases/verify.ts::runVerify.&lt;block@1833:27&gt;.&lt;block@1953:33&gt;.&lt;block@1954:10&gt;.&lt;object@1955:73&gt;.&lt;arrow@1962:21&gt;`

在调用形式「Array.isArray」中提供第 1 个实参「item.allowedFiles」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`core/phases/verify.ts:1962`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/40`。

### `core/phases/verify.ts::runVerify.&lt;block@1833:27&gt;.&lt;block@1953:33&gt;.&lt;block@1954:10&gt;.&lt;object@1955:73&gt;.&lt;arrow@1963:17&gt;`

将「file」作为第 1 个实参交给已绑定接口「ts:core/phases/verify#stringValue」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。

源码：`core/phases/verify.ts:1963`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/41`。

### `core/phases/verify.ts::runVerify.&lt;block@1833:27&gt;.&lt;block@1953:33&gt;.&lt;block@1954:10&gt;.&lt;object@1955:73&gt;.&lt;arrow@1964:20&gt;`

将「file」作为第 1 个实参交给已绑定接口「ts:core/phases/verify#isRepositoryTestPath」，对应捕获形参「file: string」。该普通调用关系不替代进程或网络协议关系。

源码：`core/phases/verify.ts:1964`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/42`。

### `core/policy/agent-sandbox.ts::normalizedMode`

在调用形式「VALID_MODES.has」中提供第 1 个实参「requested」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「requested」的初始化来源为「String(\n    env.CPB_AGENT_SANDBOX ||\n    env.CPB_AGENT_SANDBOX_MODE ||\n    "required"\n  ).trim().toLowerCase()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!VALID_MODES.has(requested))」的捕获提前退出分支为「throw：new Error(`CPB_AGENT_SANDBOX_INVALID_MODE: ${JSON.stringify(requested)}`)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return "off";」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「75dc33bc965ce0aca7a7587e」先于语句位置「1」的操作「d93e71f0e96bdb406a0ff29c」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

条件「(env.CPB_AGENT_SANDBOX_INHERITED === "1")」的捕获提前退出分支为「return："off"」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。

源码：`core/policy/agent-sandbox.ts:90`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/43`。

### `core/policy/agent-sandbox.ts::withExecutableReadRoots`

构造捕获记录，字段按源码次序为「readRoots ← readRoots」。不据构造形式推断物理持久化。 将「command」作为第 1 个实参交给已绑定接口「ts:core/policy/agent-sandbox#executableReadRoots」，对应捕获形参「command: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「readRoots」的初始化来源为「uniqueRoots([\n    ...policy.readRoots,\n    ...executableReadRoots(command, env, cwd),\n    ...argumentReadRoots(args, cwd),\n  ])」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!policy.enabled || policy.provider === "custom")」的捕获提前退出分支为「return：policy」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return policy;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「readRoots」关联路径「readRoots」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「policy」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。

源码：`core/policy/agent-sandbox.ts:351`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/44`。

### `core/policy/agent-sandbox.ts::resolveAgentSandboxPolicy`

构造捕获记录，字段按源码次序为「mode ← mode；enabled ← true；provider ← "custom"；command ← customCommand；args ← parseEnvArgs(env.CPB_AGENT_SANDBOX_ARGS)；network ← network；subprocess ← subprocess；readRoots ← readRoots；writeRoots ← writeRoots」。不据构造形式推断物理持久化。 将「env」作为第 1 个实参交给已绑定接口「ts:core/policy/agent-sandbox#normalizedMode」，对应捕获形参「env: EnvRecord = {}」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「mode」的初始化来源为「normalizedMode(env)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(mode === "off")」的捕获提前退出分支为「return：{ mode, enabled: false, provider: null, network, subprocess, readRoots, writeRoots }」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return { mode, enabled: false, provider: null, network, subprocess, readRoots, writeRoots };」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「mode」关联路径「mode」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「bfb9d9c88ed1daba151b2bc3」先于语句位置「1」的操作「ee8fedc074e0e29351b45229」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`core/policy/agent-sandbox.ts:361`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/45`。

### `core/policy/agent-sandbox.ts::buildAgentSandboxLaunch`

构造捕获记录，字段按源码次序为「command ← command；args ← args；sandbox ← policy」。不据构造形式推断物理持久化。 将「command」作为第 2 个实参交给已绑定接口「ts:core/policy/agent-sandbox#withExecutableReadRoots」，对应捕获形参「command: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「env」的初始化来源为「options.env || {}」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(policy.mode === "required" || policy.mode === "strict")」的捕获提前退出分支为「throw：new Error(`CPB_AGENT_SANDBOX_REQUIRED: ${policy.reason || "agent sandbox is required but unavailable"}`)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new Error(`CPB_AGENT_SANDBOX_REQUIRED: ${policy.reason || "agent sandbox is required but unavailable"}`);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「command」关联路径「command」；只描述捕获来源，不证明当时的字段值。 记录消息形状中的固定文本字段「command」及捕获形式「policy.command」。单个文本字段不是跨语言调用或传输成功的证明。 将「options」作为第 2 个实参交给已绑定接口「ts:core/policy/agent-sandbox#resolveAgentSandboxPolicy」，对应捕获形参「{ cwd = process.cwd(), platform = process.platform, probe = defaultProbe }: SandboxOptions = {}」。该普通调用关系不替代进程或网络协议关系。

源码：`core/policy/agent-sandbox.ts:499`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/46`。

### `core/policy/child-env.ts::allowedProviderCredentialsForOptions`

将「providerEnv」作为第 1 个实参交给已绑定接口「ts:core/agents/provider-catalog#configuredProviderEnvironmentKeys」，对应捕获形参「env: Record&lt;string, string | undefined&gt; = process.env」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「explicit」的初始化来源为「providerKeysFromOptions(options)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(typeof options !== "string" &amp;&amp; options.includeProviderCredentials === false)」的捕获提前退出分支为「return：NO_PROVIDER_CREDENTIALS」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return NO_PROVIDER_CREDENTIALS;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「1」的操作「651efdc36775e7cb9602fa7c」先于语句位置「2」的操作「07869e1612a9678c6b22cf33」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`core/policy/child-env.ts:197`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/47`。

### `core/policy/child-env.ts::shouldCopyChildEnvEntry`

将「key」作为第 1 个实参交给已绑定接口「ts:core/policy/child-env#isAllowedChildEnvKey」，对应捕获形参「key: string」。该普通调用关系不替代进程或网络协议关系。 以「return isAcpPoolNumericEntry(key, value) || isAllowedChildEnvKey(key, options, providerEnv);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`core/policy/child-env.ts:241`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/48`。

### `core/policy/child-env.ts::isAllowedChildEnvKey`

将「options」作为第 1 个实参交给已绑定接口「ts:core/policy/child-env#allowedProviderCredentialsForOptions」，对应捕获形参「options: ChildEnvOptions = {}」。该普通调用关系不替代进程或网络协议关系。 条件「(allowedProviderCredentialsForOptions(options, providerEnv).has(key))」的捕获提前退出分支为「return：true」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return true;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「e7677f55e8412ef6dcef6d8b」先于语句位置「1」的操作「352d5c446527ef3b2b7b1124」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`core/policy/child-env.ts:250`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/49`。

### `core/policy/child-env.ts::_filterEnv`

构造捕获的空记录「{}」；没有从空记录形式推断额外字段或持久效果。 在调用形式「EXPLICIT_ONLY_CHILD_ENV.has」中提供第 1 个实参「k」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「env」的初始化来源为「{}」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return env;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「bba20381a29bea12202f550a」先于语句位置「1」的操作「5320a095be88e7cfaf37d9a9」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`core/policy/child-env.ts:266`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/50`。

### `core/policy/child-env.ts::buildChildEnv`

具有捕获记录构造「{ ...process.env, ...parentEnv, ...extra }」；该记录的可枚举字段为空或保留开放形状，未把展开来源补成确定字段。 将「parentEnv」作为第 1 个实参交给已绑定接口「ts:core/policy/child-env#_filterEnv」，对应捕获形参「parentEnv: EnvMap = {}」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「allowKeys」的初始化来源为「allowKeysFromOptions(options)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return _filterEnv(parentEnv, extra, (k, v) =&gt; allowKeys.has(k) || shouldCopyChildEnvEntry(k, v, options, providerEnv));」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留记录复制/展开来源「parentEnv」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「d264ddd2032ed13315634076」先于语句位置「1」的操作「46c40c3916b448f0e37c88cf」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`core/policy/child-env.ts:276`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/51`。

### `core/policy/child-env.ts::buildChildEnv.&lt;arrow@279:38&gt;`

将「k」作为第 1 个实参交给已绑定接口「ts:core/policy/child-env#shouldCopyChildEnvEntry」，对应捕获形参「key: string」。该普通调用关系不替代进程或网络协议关系。

源码：`core/policy/child-env.ts:279`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/52`。

### `core/workflow/evidence-probes.ts::validateEvidenceObservation`

将「entry.attemptId」作为第 1 个实参交给已绑定接口「ts:core/workflow/evidence-probes#text」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 条件「(!entry || typeof entry !== "object")」的捕获提前退出分支为「return：INVALID」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return INVALID;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「6dc8bd0aeca40c20b7f6af82」先于语句位置「1」的操作「fe03ea00b1d6b384ac3b1747」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`core/workflow/evidence-probes.ts:37`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/53`。

### `core/workflow/evidence-probes.ts::buildEvidenceProbePlan`

构造捕获记录，字段按源码次序为「checklistId ← checklistId；predicateId ← predicateId；probeId ← `probe-${checklistId}`；observation ← {\n        checklistId,\n        predicateId,\n        verificationMethod: item.verificationMethod || "static",\n        expectedEvidence: item.expectedEvidence…［展示截断；完整操作保留］；emitFailedClaim ← true」。不据构造形式推断物理持久化。 将「acceptanceChecklist」作为第 1 个实参交给已绑定接口「ts:shared/types#recordValue」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「existing.observation = observation」，捕获目标为「existing.observation」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「item」的初始化来源为「recordValue(itemValue)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return {\n    schemaVersion: 1,\n    attemptId,\n    probes,\n  };」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「checklistId」关联路径「checklistId」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「6ff00a50d991f899ba52d074」先于语句位置「1」的操作「2bdc554b12f305c794399cdf」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`core/workflow/evidence-probes.ts:297`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/54`。

### `core/workflow/probe-runner.ts::text`

以无显式实参的调用形式「value.trim」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。 以「return typeof value === "string" ? value.trim() : "";」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`core/workflow/probe-runner.ts:53`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/55`。

### `core/workflow/probe-runner.ts::posixify`

在调用形式「p.split("\\").join」中提供第 1 个实参「"/"」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return p.split("\\").join("/");」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`core/workflow/probe-runner.ts:86`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/56`。

### `core/workflow/probe-runner.ts::scopeMatches`

在调用形式「Array.isArray」中提供第 1 个实参「allowedFiles」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「count」的初始化来源为「0」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「count」存在源更新「count += 1」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!Array.isArray(allowedFiles) || allowedFiles.length === 0)」的捕获提前退出分支为「return：0」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return 0;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「af36a114cef6c3b33782cae6」先于语句位置「1」的操作「8acf7ff68c8ad02a2e75c402」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`core/workflow/probe-runner.ts:99`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/57`。

### `core/workflow/probe-runner.ts::scopeMatches.&lt;loop@102:2&gt;.&lt;block@102:32&gt;.&lt;arrow@103:21&gt;`

将「changedFile」作为第 1 个实参交给已绑定接口「ts:core/workflow/probe-runner#scopePathMatches」，对应捕获形参「changedFile: string」。该普通调用关系不替代进程或网络协议关系。 将「f」作为第 1 个实参交给已绑定接口「ts:core/workflow/probe-runner#text」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。

源码：`core/workflow/probe-runner.ts:103`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/58`。

### `core/workflow/probe-runner.ts::scopePathMatches`

将「changedFile」作为第 1 个实参交给已绑定接口「ts:core/workflow/probe-runner#posixify」，对应捕获形参「p: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「suffix」的初始化来源为「allowed.slice(3)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!allowed)」的捕获提前退出分支为「return：false」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return false;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「71f3746a023e3bfb90ec2d72」先于语句位置「1」的操作「296d7b9230141c9f6a2df57d」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`core/workflow/probe-runner.ts:108`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/59`。

### `core/workflow/probe-runner.ts::loadTrustedProbePolicy`

构造捕获记录，字段按源码次序为「cwd ← cwd；env ← env；maxBuffer ← 1024 * 1024」。不据构造形式推断物理持久化。 将「parsed」作为第 1 个实参交给已绑定接口「ts:core/workflow/trusted-probe-policy#parseTrustedProbePolicy」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「result」的初始化来源为「await execFileAsync("git", ["show", `HEAD:${TRUSTED_PROBE_POLICY_PATH}`], {\n      cwd,\n      env,\n      maxBuffer: 1024 * 1024,\n    })」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return parseTrustedProbePolicy(parsed);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「cwd」关联路径「cwd」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「f72ff9b375952bbe9761e659」先于语句位置「1」的操作「28222ca8e1a5722d99eca90b」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`core/workflow/probe-runner.ts:147`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/60`。

### `core/workflow/probe-runner.ts::renderProbeCommand`

在调用形式「[spec.executable, ...spec.args].map((part) =&gt; JSON.stringify(part)).join」中提供第 1 个实参「" "」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return [spec.executable, ...spec.args].map((part) =&gt; JSON.stringify(part)).join(" ");」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`core/workflow/probe-runner.ts:163`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/61`。

### `core/workflow/probe-runner.ts::renderProbeCommand.&lt;arrow@164:45&gt;`

在调用形式「JSON.stringify」中提供第 1 个实参「part」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`core/workflow/probe-runner.ts:164`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/62`。

### `core/workflow/probe-runner.ts::oracleProtectedPaths`

将「item.sourceRefs」作为第 1 个实参交给已绑定接口「ts:core/workflow/probe-runner#collectSourceRefPaths」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「paths」的初始化来源为「new Set&lt;string&gt;()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return [...paths].sort();」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「0d0d72172cb1f036194da681」先于语句位置「1」的操作「305e4a027974e17a4bfd8ac1」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`core/workflow/probe-runner.ts:215`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/63`。

### `core/workflow/probe-runner.ts::changedOracleFiles`

将「item」作为第 1 个实参交给已绑定接口「ts:core/workflow/probe-runner#oracleProtectedPaths」，对应捕获形参「item: LooseRecord」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「protectedPaths」的初始化来源为「oracleProtectedPaths(item, declaredCommand)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!requiresCleanOracleProvenance(item))」的捕获提前退出分支为「return：[]」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return [];」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「eb5bee00770946ad8906e6f3」先于语句位置「1」的操作「f8be79ecd1eba9f67a83a8eb」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`core/workflow/probe-runner.ts:233`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/64`。

### `core/workflow/probe-runner.ts::changedOracleFiles.&lt;arrow@238:12&gt;`

在调用形式「protectedPaths.some」中提供第 1 个实参「(scope) =&gt; scopePathMatches(file, scope)」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`core/workflow/probe-runner.ts:238`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/65`。

### `core/workflow/probe-runner.ts::changedOracleFiles.&lt;arrow@238:12&gt;.&lt;arrow@238:42&gt;`

将「file」作为第 1 个实参交给已绑定接口「ts:core/workflow/probe-runner#scopePathMatches」，对应捕获形参「changedFile: string」。该普通调用关系不替代进程或网络协议关系。

源码：`core/workflow/probe-runner.ts:238`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/66`。

### `core/workflow/probe-runner.ts::resolveDeclaredCommand`

将「item.predicateId」作为第 1 个实参交给已绑定接口「ts:core/workflow/probe-runner#text」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 以「return policy.get(text(item.predicateId)) || null;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`core/workflow/probe-runner.ts:435`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/67`。

### `core/workflow/probe-runner.ts::runDeclaredCommand`

构造捕获记录，字段按源码次序为「exitCode ← -1；stdoutSha256 ← ""；stderrSha256 ← ""；stdoutTail ← ""；stderrTail ← ""；note ← "command probe did not run"；retryCount ← 0；probeAttempts ← attempts」。不据构造形式推断物理持久化。 将「command」作为第 1 个实参交给已绑定接口「ts:core/workflow/probe-runner#runDeclaredCommandOnce」，对应捕获形参「command: TrustedProbeSpec」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「attempt」的初始化来源为「1」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「attempt」存在源更新「attempt += 1」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!last)」的捕获提前退出分支为「return：{\n      exitCode: -1,\n      stdoutSha256: "",\n      stderrSha256: "",\n      stdoutTail: "",\n      stderrTail: "",\n      note: "command probe did not run",\n      retryCount: 0,\n      probeAttempts: attempts,\n    }」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return {\n      exitCode: -1,\n      stdoutSha256: "",\n      stderrSha256: "",\n      stdoutTail: "",\n      stderrTail: "",\n      note: "command probe did not run",\n      retryCount: 0,\n      probeAttempts: attempts,\n    };」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「attempt」关联路径「attempt」；只描述捕获来源，不证明当时的字段值。

源码：`core/workflow/probe-runner.ts:444`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/68`。

### `core/workflow/probe-runner.ts::runDeclaredCommandOnce`

构造捕获记录，字段按源码次序为「exitCode ← -1；stdoutSha256 ← ""；stderrSha256 ← ""；stdoutTail ← ""；stderrTail ← ""；note ← reason；retryable ← false」。不据构造形式推断物理持久化。 将「e?.code」作为第 1 个实参交给已绑定接口「ts:core/workflow/probe-runner#text」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「e」的初始化来源为「isRecordLike(err) ? err : null」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(typeof e?.code === "number")」的捕获提前退出分支为「return：{\n        exitCode: e.code,\n        stdoutSha256: sha256Hex(stdout),\n        stderrSha256: sha256Hex(stderr),\n        stdoutTail: outputTail(stdout),\n        stderrTail: outputTail(stderr),\n        retryable: true,\n      }」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return {\n      exitCode: 0,\n      stdoutSha256: sha256Hex(result.stdout ?? ""),\n      stderrSha256: sha256Hex(result.stderr ?? ""),\n      stdoutTail: outputTail(result.stdout ?? ""),\n      stderrTail: outputTail(result.stderr ?? ""),\n      retryable: false,\n      // Note: digests are always emitted, even for empty output, so the\n      // observation …［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「cwd」关联路径「cwd」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「64ff28ad5278b8859d69374a」先于语句位置「1」的操作「2ae87c6ed63d834e1a37cfd4」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`core/workflow/probe-runner.ts:513`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/69`。

### `core/workflow/probe-runner.ts::runChecklistProbes`

构造捕获记录，字段按源码次序为「checklistId ← checklistId；predicateId ← predicateId；probeId ← probeId；observation ← {\n          checklistId,\n          predicateId,\n          probeId,\n          verificationMethod: "static",\n          queryId: `static-diff-scope:${checklis…［展示截断；完整操作保留］；emitFailedClaim ← true」。不据构造形式推断物理持久化。 将「cwd」作为第 1 个实参交给已绑定接口「ts:core/workflow/probe-runner#loadTrustedProbePolicy」，对应捕获形参「cwd: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「checklistId」的初始化来源为「text(item.id)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!acceptanceChecklist || !Array.isArray(acceptanceChecklist.items))」的捕获提前退出分支为「return：[]」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return [];」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「cwd」关联路径「cwd」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「(worktreeHead ? { worktreeHead } : {})」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。 将「cwd」作为第 2 个实参交给已绑定接口「ts:core/workflow/probe-runner#runDeclaredCommand」，对应捕获形参「cwd: string」。该普通调用关系不替代进程或网络协议关系。

源码：`core/workflow/probe-runner.ts:582`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/70`。

### `core/workflow/probe-runner.ts::runChecklistProbes.&lt;arrow@595:4&gt;`

将「item?.id」作为第 1 个实参交给已绑定接口「ts:core/workflow/probe-runner#text」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。

源码：`core/workflow/probe-runner.ts:595`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/71`。

### `core/workflow/probe-runner.ts::runChecklistProbes.&lt;loop@607:2&gt;.&lt;block@607:37&gt;.&lt;block@613:29&gt;.&lt;object@617:18&gt;.&lt;object@621:21&gt;.&lt;arrow@629:46&gt;`

在调用形式「allowedFiles.some」中提供第 1 个实参「(allowedFile) =&gt; scopePathMatches(f, allowedFile)」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`core/workflow/probe-runner.ts:629`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/72`。

### `core/workflow/probe-runner.ts::runChecklistProbes.&lt;loop@607:2&gt;.&lt;block@607:37&gt;.&lt;block@613:29&gt;.&lt;object@617:18&gt;.&lt;object@621:21&gt;.&lt;arrow@629:46&gt;.&lt;arrow@629:71&gt;`

将「f」作为第 1 个实参交给已绑定接口「ts:core/workflow/probe-runner#scopePathMatches」，对应捕获形参「changedFile: string」。该普通调用关系不替代进程或网络协议关系。

源码：`core/workflow/probe-runner.ts:629`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/73`。

### `core/workflow/trusted-probe-policy.ts::trustedProbeSpec`

构造捕获记录，字段按源码次序为「predicateId ← predicateId；executable ← executable；args ← args.map(String)」。不据构造形式推断物理持久化。 将「value」作为第 1 个实参交给已绑定接口「ts:core/contracts/types#isRecord」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「predicateId」的初始化来源为「text(value.predicateId)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!isRecord(value))」的捕获提前退出分支为「return：null」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return null;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「predicateId」关联路径「predicateId」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「1a7d2ec23389da5e9adf0863」先于语句位置「1」的操作「4b7e4a917c56c30b672beeb9」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`core/workflow/trusted-probe-policy.ts:17`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/74`。

### `core/workflow/trusted-probe-policy.ts::trustedProbeSpec.&lt;arrow@22:56&gt;`

在调用形式「arg.includes」中提供第 1 个实参「"\0"」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`core/workflow/trusted-probe-policy.ts:22`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/75`。

### `core/workflow/trusted-probe-policy.ts::trustedProbeSpec.&lt;arrow@27:44&gt;`

在调用形式「String」中提供第 1 个实参「arg」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`core/workflow/trusted-probe-policy.ts:27`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/76`。

### `core/workflow/trusted-probe-policy.ts::parseTrustedProbePolicy`

将「value」作为第 1 个实参交给已绑定接口「ts:core/contracts/types#isRecord」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「probes」的初始化来源为「value.probes as unknown[]」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!isRecord(value) || value.schemaVersion !== 1 || !Array.isArray(value.probes))」的捕获提前退出分支为「return：new Map()」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return new Map();」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「ad55d6998b15864bfee3b1b2」先于语句位置「1」的操作「0a8fadb1159aa6515dcde535」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`core/workflow/trusted-probe-policy.ts:34`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/77`。

### `core/workflow/trusted-probe-policy.ts::parseTrustedProbePolicy.&lt;arrow@37:52&gt;`

在调用形式「Boolean」中提供第 1 个实参「entry」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`core/workflow/trusted-probe-policy.ts:37`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/78`。

### `runtime/worker/assignment-finalizer.ts::failedJobResult`

构造捕获记录，字段按源码次序为「kind ← FINALIZER_FAILURE_KIND；phase ← "finalize"；reason ← reason；retryable ← finalizeResult?.retryable === true；cause ← {\n        finalizer: safeFinalizeResult,\n        executionResult: safeResult,\n        worktreePath: worktreeInfo?.path || null,\n        worktreeBranch: work…［展示截断；完整操作保留］」。不据构造形式推断物理持久化。 将「finalizeResult」作为第 1 个实参交给已绑定接口「ts:runtime/worker/assignment-finalizer#finalizerFailureReason」，对应捕获形参「finalizeResult: LooseRecord | null」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「status」的初始化来源为「finalizeResult?.status === "blocked" ? "blocked" : "failed"」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return {\n    ...safeResult,\n    status,\n    failure: {\n      kind: FINALIZER_FAILURE_KIND,\n      phase: "finalize",\n      reason,\n      retryable: finalizeResult?.retryable === true,\n      cause: {\n        finalizer: safeFinalizeResult,\n        executionResult: safeResult,\n        worktreePath: worktreeInfo?.path || null,\n        worktreeBranch: …［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「status」关联路径「status」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「safeResult」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「16b5353cfedc339cc3e36b89」先于语句位置「1」的操作「4226b2a9346d3fc43af0d859」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`runtime/worker/assignment-finalizer.ts:704`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/79`。

### `runtime/worker/assignment-finalizer.ts::finalizeAndWriteSuccessfulResult`

构造捕获记录，字段按源码次序为「cpbRoot ← cpbRoot；hubRoot ← hubRoot；dataRoot ← dataRoot；assignment ← assignment；attemptNum ← attemptNum；jobId ← jobId；result ← result；worktreeInfo ← worktreeInfo；log ← log；resolveTransport ← resolveTransport；resolveDataRoot ← resolveDataRoot；finalizeQueueEntry ← finalizeQueueEntry」；其余字段见完整操作。不据构造形式推断物理持久化。 将「result」作为第 1 个实参交给已绑定接口「ts:runtime/worker/assignment-finalizer#failedJobResult」，对应捕获形参「result: JobResult」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「structuredFinalizeResult」的初始化来源为「isRecord(finalizeResult) ? finalizeResult : {}」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(structuredFinalizeResult.code === "ASSIGNMENT_CANCELLED"\n    &amp;&amp; structuredFinalizeResult.committed === false\n    &amp;&amp; !isRecord(structuredFinalizeResult.remoteIntent)\n    &amp;&amp; !isRecord(structuredFinalizeResult.remoteWrites))」的捕获提前退出分支为「throw：Object.assign(\n      new Error(finalizerFailureReason(finalizeResult)),\n      finalizeResult,\n      { finalizeResult },\n    )」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw Object.assign(\n      new Error(finalizerFailureReason(finalizeResult)),\n      finalizeResult,\n      { finalizeResult },\n    );」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「cpbRoot」关联路径「cpbRoot」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「(assignment.orchestratorEpoch !== undefined ? { orchestratorEpoch: assignment.orchestratorEpoch } : {})」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。

源码：`runtime/worker/assignment-finalizer.ts:1184`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/80`。

### `runtime/worker/managed-worker.ts::completeAssignmentStateFromResult`

构造捕获记录，字段按源码次序为「result ← result；inboxAcked ← completion.inboxAcked；terminalSyncFailed ← false；mutationOwnershipLost ← false」。不据构造形式推断物理持久化。 将「err」作为第 1 个实参交给已绑定接口「ts:runtime/worker/managed-worker#redactedWorkerErrorMessage」，对应捕获形参「error: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「resultPath」的初始化来源为「path.join(attemptDir, "result.json")」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return {\n      result,\n      inboxAcked: completion.inboxAcked,\n      terminalSyncFailed: false,\n      mutationOwnershipLost: false,\n    };」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「workerId」关联路径「workerId」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「b5d98294d1a039600d138d9c」先于语句位置「1」的操作「c372a3a998ebf18c4787b71b」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`runtime/worker/managed-worker.ts:847`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/81`。

### `runtime/worker/managed-worker.ts::completeAssignmentStateFromResult.&lt;block@866:6&gt;.&lt;object@873:6&gt;.&lt;arrow@877:12&gt;`

在调用形式「workerStore.completeInboxClaim」中提供第 1 个实参「wid」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`runtime/worker/managed-worker.ts:877`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/82`。

### `runtime/worker/managed-worker.ts::writeTerminalResultOnceVerified`

构造捕获记录，字段按源码次序为「created ← true；idempotent ← false；value ← intended」。不据构造形式推断物理持久化。 将「{\n      maxBytes: TERMINAL_RESULT_MAX_BYTES,\n    }」作为第 2 个实参交给已绑定接口「ts:shared/primitives/durable-directory-lock#readBoundedRegularFileNoFollow」，对应捕获形参「{ maxBytes, hooks }: BoundedRegularFileReadOptions」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「intended」的初始化来源为「canonicalTerminalResult(value)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「existing」存在源更新「existing = canonicalTerminalResult(JSON.parse(await readBoundedRegularFileNoFollow(file, {\n      maxBytes: TERMINAL_RESULT_MAX_BYTES,\n    })))」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!path.isAbsolute(file) || path.resolve(file) !== file)」的捕获提前退出分支为「throw：Object.assign(new Error("terminal result path must be absolute and normalized"), {\n      code: "TERMINAL_RESULT_PATH_INVALID",\n    })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw Object.assign(new Error("terminal result path must be absolute and normalized"), {\n      code: "TERMINAL_RESULT_PATH_INVALID",\n    });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「intended」关联路径「intended」；只描述捕获来源，不证明当时的字段值。

源码：`runtime/worker/managed-worker.ts:982`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/83`。

### `runtime/worker/managed-worker.ts::publishTerminalResultAfterWorktreeCleanup`

构造捕获记录，字段按源码次序为「produced ← produced；cleanupProof ← cleanupProof；attemptResult ← publication.value；publication ← publication」。不据构造形式推断物理持久化。 将「{\n      file: captured.file,\n      value: captured.value,\n      writeResult,\n    }」作为第 1 个实参交给已绑定接口「ts:runtime/worker/managed-worker#writeTerminalResultOnceVerified」，对应捕获形参「{\n  file,\n  value,\n  writeResult = writeJsonOnce,\n}: {\n  file: string;\n  value: unknown;\n  writeResult?: (file: string, value: unknown) =&gt; Promise&lt;boolean&gt;;\n}」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「captured.value.cleanup = {\n      ...recordValue(captured.value.cleanup),\n      worktree: cleanupProof,\n    }」，捕获目标为「captured.value.cleanup」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「captured」的初始化来源为「deferred as DeferredTerminalResult」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「cleanupProof」存在源更新「cleanupProof = parseManagedWorktreeDispositionProof(await produceProof(), binding)」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!deferred)」的捕获提前退出分支为「throw：Object.assign(new Error("terminal result producer did not provide a result"), {\n      code: "TERMINAL_RESULT_MISSING",\n    })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw Object.assign(new Error("terminal result producer did not provide a result"), {\n      code: "TERMINAL_RESULT_MISSING",\n    });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`runtime/worker/managed-worker.ts:1133`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/84`。

### `runtime/worker/managed-worker.ts::publishTerminalResultAfterWorktreeCleanup.&lt;arrow@1147:39&gt;`

构造捕获记录，字段按源码次序为「file ← file；value ← canonicalTerminalResult(value)」。不据构造形式推断物理持久化。 将「value」作为第 1 个实参交给已绑定接口「ts:runtime/worker/managed-worker#canonicalTerminalResult」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 对捕获 binding「deferred」存在源更新「deferred = { file, value: canonicalTerminalResult(value) }」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(deferred)」的捕获提前退出分支为「throw：Object.assign(new Error("terminal result producer attempted more than one publication"), {\n        code: "TERMINAL_RESULT_MULTIPLE_PUBLICATIONS",\n      })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw Object.assign(new Error("terminal result producer attempted more than one publication"), {\n        code: "TERMINAL_RESULT_MULTIPLE_PUBLICATIONS",\n      });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「file」关联路径「file」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「2」的操作「4e8c938b9aed6a085d54d671」先于语句位置「3」的操作「1790777c533ba8af074ef4b2」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`runtime/worker/managed-worker.ts:1147`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/85`。

### `runtime/worker/managed-worker.ts::main`

构造捕获记录，字段按源码次序为「workerId ← workerId；pid ← process.pid；host ← os.hostname()；startedAt ← new Date().toISOString()；lastHeartbeatAt ← new Date().toISOString()；incarnationToken ← workerIncarnationToken；processIdentity ← workerProcessIdentity」。不据构造形式推断物理持久化。 将「"once"」作为第 1 个实参交给已绑定接口「ts:runtime/worker/managed-worker#main.shutdown」，对应捕获形参「signal: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「directAssignmentStore」的初始化来源为「new AssignmentStore(hubRoot)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「assignmentStore」存在源更新「assignmentStore = brokerClient」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!workerProcessIdentity)」的捕获提前退出分支为「throw：Object.assign(new Error("managed worker could not capture its exact process identity"), {\n      code: "PROCESS_IDENTITY_UNAVAILABLE",\n    })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw Object.assign(new Error("managed worker could not capture its exact process identity"), {\n      code: "PROCESS_IDENTITY_UNAVAILABLE",\n    });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「brokerUrl」关联路径「brokerUrl」；只描述捕获来源，不证明当时的字段值。 以无显式实参的调用形式「processInboxGuarded」调用已绑定接口「ts:runtime/worker/managed-worker#main.processInboxGuarded」；没有据调用存在断言激活、存储或网络效果。

源码：`runtime/worker/managed-worker.ts:1235`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/86`。

### `runtime/worker/managed-worker.ts::main.&lt;arrow@1334:37&gt;`

构造捕获记录，字段按源码次序为「lastHeartbeatAt ← new Date().toISOString()」。不据构造形式推断物理持久化。 在调用形式「workerStore.updateWorkerIf」中提供第 2 个实参「{ lastHeartbeatAt: new Date().toISOString() }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以字段投影形式「workerIncarnationToken」关联路径「workerIncarnationToken」；只描述捕获来源，不证明当时的字段值。

源码：`runtime/worker/managed-worker.ts:1334`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/87`。

### `runtime/worker/managed-worker.ts::main.stopWorkerAcpPool`

构造捕获记录，字段按源码次序为「cpbRoot ← cpbRoot；hubRoot ← hubRoot」。不据构造形式推断物理持久化。 将「{ cpbRoot, hubRoot }」作为第 1 个实参交给已绑定接口「ts:server/services/acp/acp-pool#stopManagedAcpPool」，对应捕获形参「{ cpbRoot, hubRoot, ...opts }: AcpPoolOptions = {}」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「stopped」的初始化来源为「await stopManagedAcpPool({ cpbRoot, hubRoot })」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以字段投影形式「cpbRoot」关联路径「cpbRoot」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「51f109dcabb5524ceb3d95d4」先于语句位置「1」的操作「c603735f25b7ff6d6eebaaa2」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`runtime/worker/managed-worker.ts:1351`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/88`。

### `runtime/worker/managed-worker.ts::main.releaseWorkerAcpAttempt`

构造捕获记录，字段按源码次序为「cpbRoot ← cpbRoot；hubRoot ← hubRoot；projectId ← projectId；jobId ← jobId」。不据构造形式推断物理持久化。 将「{ cpbRoot, hubRoot, projectId, jobId }」作为第 1 个实参交给已绑定接口「ts:server/services/acp/acp-pool#releaseManagedAcpJob」，对应捕获形参「{ cpbRoot, hubRoot, projectId, jobId, reason = "job_release", ...opts }: AcpPoolOptions &amp; {\n  projectId?: string;\n  jobId?: string;\n  reason?: string;\n} = {}」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「releasedJob」的初始化来源为「projectId &amp;&amp; jobId\n        ? await releaseManagedAcpJob({ cpbRoot, hubRoot, projectId, jobId })\n        : false」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!worktreePath &amp;&amp; (!projectId || !jobId))」的捕获提前退出分支为「return：true」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return true;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「cpbRoot」关联路径「cpbRoot」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「2ca4702f406c1d35ea3296be」先于语句位置「1」的操作「b7798c96f166bf1dc56c8873」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`runtime/worker/managed-worker.ts:1360`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/89`。

### `runtime/worker/managed-worker.ts::main.processInbox`

构造捕获记录，字段按源码次序为「workerId ← workerId；assignmentId ← assignmentId；attempt ← attemptNum；phase ← "starting"；activePhase ← null；activeJobId ← null；status ← "running"；executionBoundary ← executionBoundary；sourcePath ← assignment.sourcePath；pid ← process.pid；workerIncarnation ← workerIncarnationToken；processIdentity ← {\n          pid: workerProcessIdentity.pid,\n          startTimeTicks: workerProcessIdentity.birthId,\n          birthIdPrecision: workerProcessIdentity.birthI…［展示截断；完整操作保留］」；其余字段见完整操作。不据构造形式推断物理持久化。 将「{\n            assignmentId,\n            attempt: attemptNum,\n            attemptToken: assignment.attemptToken,\n            executionBoundary,\n            sourcePath: assignment.sourcePath,\n            worktreePath: worktreeInfo.path,\n            worktreeBranch: worktreeInfo.branch,\n            managedWorktree: durableManagedWorktree,\n            wo…［展示截断；完整操作保留］」作为第 2 个实参交给已绑定接口「ts:shared/fs-utils#writeJsonAtomic」，对应捕获形参「data: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「assignment」的初始化来源为「claim.assignment as AssignmentPayload」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「worktreeCleanupProof」存在源更新「worktreeCleanupProof = terminalPublication.cleanupProof as ManagedWorktreeCleanupProof | null」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(finalizerOnly &amp;&amp; !verifiedPriorFinalizerAttempt)」的捕获提前退出分支为「throw：Object.assign(new Error("finalizer recovery prior-attempt proof is not authoritative"), {\n          code: "FINALIZER_RECOVERY_PROOF_INVALID",\n        })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw Object.assign(new Error("finalizer recovery prior-attempt proof is not authoritative"), {\n          code: "FINALIZER_RECOVERY_PROOF_INVALID",\n        });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「assignment.entryId」关联路径「assignment.entryId」；只描述捕获来源，不证明当时的字段值。 将「{\n          worktreePath: worktreeInfo?.path,\n          projectId: assignment.projectId,\n          jobId,\n          jobLog,\n        }」作为第 1 个实参交给已绑定接口「ts:runtime/worker/managed-worker#main.releaseWorkerAcpAttempt」，对应捕获形参「{\n    worktreePath,\n    projectId,\n    jobId,\n    jobLog = log,\n  }: {\n    worktreePath: string | null | undefined;\n    projectId: string;\n    jobId: string;\n    jobLog?: ReturnType&lt;typeof createLogger&gt;;\n  }」。该普通调用关系不替代进程或网络协议关系。

源码：`runtime/worker/managed-worker.ts:1393`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/90`。

### `runtime/worker/managed-worker.ts::main.processInbox.&lt;loop@1396:4&gt;.&lt;block@1396:32&gt;.writeAssignmentHeartbeat`

构造捕获的空记录「{}」；没有从空记录形式推断额外字段或持久效果。 在调用形式「writeJsonAtomic」中提供第 1 个实参「heartbeatPath」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 包含赋值/更新「heartbeatState.progressUpdatedAt = progressUpdatedAt || now」，捕获目标为「heartbeatState.progressUpdatedAt」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「progressUpdatedAt」的初始化来源为「typeof patch.progressUpdatedAt === "string" ? patch.progressUpdatedAt : null」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「heartbeatState」存在源更新「heartbeatState = {\n          ...heartbeatState,\n          ...patch,\n          updatedAt: now,\n        }」；循环和分支条件见操作上下文，未推执行次数或最终数值。 以字段投影形式「now」关联路径「now」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「heartbeatState」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。

源码：`runtime/worker/managed-worker.ts:1527`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/91`。

### `runtime/worker/managed-worker.ts::main.processInbox.&lt;loop@1396:4&gt;.&lt;block@1396:32&gt;.&lt;arrow@1555:63&gt;`

对捕获 binding「resolveExecutionLeaseLoss」存在源更新「resolveExecutionLeaseLoss = resolve」；循环和分支条件见操作上下文，未推执行次数或最终数值。

源码：`runtime/worker/managed-worker.ts:1555`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/92`。

### `runtime/worker/managed-worker.ts::main.processInbox.&lt;loop@1396:4&gt;.&lt;block@1396:32&gt;.loseExecutionLease`

构造捕获记录，字段按源码次序为「kind ← FailureKind.RUNTIME_INTERRUPTED；reason ← reason；retryable ← true；cause ← { code: "WORKER_EXECUTION_LEASE_LOST" }」。不据构造形式推断物理持久化。 在调用形式「resolveExecutionLeaseLoss」中提供第 1 个实参「{\n          status: "failed",\n          jobId,\n          failure: {\n            kind: FailureKind.RUNTIME_INTERRUPTED,\n            reason,\n            retryable: true,\n            cause: { code: "WORKER_EXECUTION_LEASE_LOST" },\n          },\n        }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 对捕获 binding「executionLeaseLost」存在源更新「executionLeaseLost = Object.assign(new Error(reason), { code: "WORKER_EXECUTION_LEASE_LOST" })」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(executionLeaseLost)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「jobId」关联路径「jobId」；只描述捕获来源，不证明当时的字段值。 记录消息形状中的固定文本字段「kind」及捕获形式「FailureKind.RUNTIME_INTERRUPTED」。单个文本字段不是跨语言调用或传输成功的证明。

源码：`runtime/worker/managed-worker.ts:1561`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/93`。

### `runtime/worker/managed-worker.ts::main.processInbox.&lt;loop@1396:4&gt;.&lt;block@1396:32&gt;.assertExecutionLeaseHeld`

条件「(executionLeaseLost)」的捕获提前退出分支为「throw：executionLeaseLost」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw executionLeaseLost;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`runtime/worker/managed-worker.ts:1579`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/94`。

### `runtime/worker/managed-worker.ts::main.processInbox.&lt;loop@1396:4&gt;.&lt;block@1396:32&gt;.&lt;arrow@1583:40&gt;`

构造捕获记录，字段按源码次序为「errored ← true；elapsedSinceSuccessMs ← elapsedSinceSuccessMs；errorCode ← errorCode」。不据构造形式推断物理持久化。 将「{ renewed }」作为第 1 个实参交给已绑定接口「ts:runtime/worker/managed-worker#executionLeaseRenewalLost」，对应捕获形参「{\n  renewed,\n  errored = false,\n  elapsedSinceSuccessMs = 0,\n  errorCode = null,\n}: {\n  renewed?: boolean;\n  errored?: boolean;\n  elapsedSinceSuccessMs?: number;\n  errorCode?: string | null;\n}」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「elapsedSinceSuccessMs」的初始化来源为「Date.now() - lastInboxClaimRenewedAt」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「lastInboxClaimRenewedAt」存在源更新「lastInboxClaimRenewedAt = Date.now()」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(executionLeaseRenewalLost({ renewed }))」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「renewed」关联路径「renewed」；只描述捕获来源，不证明当时的字段值。

源码：`runtime/worker/managed-worker.ts:1583`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/95`。

### `runtime/worker/managed-worker.ts::main.processInbox.&lt;loop@1396:4&gt;.&lt;block@1396:32&gt;.&lt;arrow@1611:51&gt;`

对捕获 binding「resolveCancel」存在源更新「resolveCancel = resolve」；循环和分支条件见操作上下文，未推执行次数或最终数值。

源码：`runtime/worker/managed-worker.ts:1611`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/96`。

### `runtime/worker/managed-worker.ts::main.processInbox.&lt;loop@1396:4&gt;.&lt;block@1396:32&gt;.interruptedPhase`

以「return heartbeatState.activePhase || (heartbeatState.phase !== "cancelled" ? heartbeatState.phase : null);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`runtime/worker/managed-worker.ts:1618`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/97`。

### `runtime/worker/managed-worker.ts::main.processInbox.&lt;loop@1396:4&gt;.&lt;block@1396:32&gt;.buildCancelledResult`

构造捕获记录，字段按源码次序为「kind ← FailureKind.RUNTIME_INTERRUPTED；phase ← phase；reason ← `assignment cancelled: ${reason}`；retryable ← false；cause ← {\n              cancel: {\n                reason,\n                requestedAt: safeCancel.requestedAt || null,\n                requestedBy: safeCancel.reque…［展示截断；完整操作保留］」。不据构造形式推断物理持久化。 在调用形式「redactedWorkerRecord」中提供第 1 个实参「cancel」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「safeCancel」的初始化来源为「redactedWorkerRecord(cancel)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return {\n          status: "cancelled",\n          jobId: heartbeatState.activeJobId || jobId,\n          failure: {\n            kind: FailureKind.RUNTIME_INTERRUPTED,\n            phase,\n            reason: `assignment cancelled: ${reason}`,\n            retryable: false,\n            cause: {\n              cancel: {\n                reason,\n          …［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「FailureKind.RUNTIME_INTERRUPTED」关联路径「FailureKind.RUNTIME_INTERRUPTED」；只描述捕获来源，不证明当时的字段值。 记录消息形状中的固定文本字段「kind」及捕获形式「FailureKind.RUNTIME_INTERRUPTED」。单个文本字段不是跨语言调用或传输成功的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「5616e83411c758ae6743b140」先于语句位置「1」的操作「2f3d70f640aa2b3c69565aa3」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`runtime/worker/managed-worker.ts:1622`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/98`。

### `runtime/worker/managed-worker.ts::main.processInbox.&lt;loop@1396:4&gt;.&lt;block@1396:32&gt;.requestCancel`

构造捕获记录，字段按源码次序为「status ← "cancelling"；phase ← "cancelled"；activePhase ← null；progressKind ← "cancel_requested"；lastProgressType ← "cancel_requested"」。不据构造形式推断物理持久化。 在调用形式「writeAssignmentHeartbeat」中提供第 1 个实参「{\n          status: "cancelling",\n          phase: "cancelled",\n          activePhase: null,\n          progressKind: "cancel_requested",\n          lastProgressType: "cancel_requested",\n        }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「phase」的初始化来源为「interruptedPhase()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「cancelRequested」存在源更新「cancelRequested = cancel || { reason: "assignment cancelled" }」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(cancelRequested)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「d55329e7140f99e67d9588a2」先于语句位置「1」的操作「9c5617c23232828bfed85cc1」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`runtime/worker/managed-worker.ts:1644`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/99`。

### `runtime/worker/managed-worker.ts::main.processInbox.&lt;loop@1396:4&gt;.&lt;block@1396:32&gt;.pollCancel`

在调用形式「assignmentStore.readCancel」中提供第 1 个实参「assignmentId」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「cancel」的初始化来源为「await assignmentStore.readCancel(assignmentId, attemptNum)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留同一块中的正常源码顺序：语句位置「0」的操作「2fc8cf2ef9164138c6cd0674」先于语句位置「1」的操作「9b6cbc35b420d22230fc343d」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`runtime/worker/managed-worker.ts:1660`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/100`。

### `runtime/worker/managed-worker.ts::main.processInbox.&lt;loop@1396:4&gt;.&lt;block@1396:32&gt;.&lt;arrow@1665:38&gt;`

以无显式实参的调用形式「pollCancel」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`runtime/worker/managed-worker.ts:1665`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/101`。

### `runtime/worker/managed-worker.ts::main.processInbox.&lt;loop@1396:4&gt;.&lt;block@1396:32&gt;.&lt;block@1732:10&gt;.&lt;block@1796:15&gt;.&lt;object@1797:48&gt;.onProgress`

构造捕获记录，字段按源码次序为「phase ← event.phase || activePhase || "running"；activePhase ← activePhase；activeJobId ← event.jobId || jobId；progressKind ← eventType；lastProgressType ← eventType；progressUpdatedAt ← event.ts || new Date().toISOString()」。不据构造形式推断物理持久化。 在调用形式「writeAssignmentHeartbeat」中提供第 1 个实参「{\n                phase: event.phase || activePhase || "running",\n                activePhase,\n                activeJobId: event.jobId || jobId,\n                progressKind: eventType,\n                lastProgressType: eventType,\n                progressUpdatedAt: event.ts || new Date().toISOString(),\n              }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「eventType」的初始化来源为「event.type || "progress"」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以字段投影形式「activePhase」关联路径「activePhase」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「a8dd10166dba85d555af739c」先于语句位置「1」的操作「ec8662c69e3e054d22590c93」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`runtime/worker/managed-worker.ts:1817`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/102`。

### `runtime/worker/managed-worker.ts::main.processInbox.&lt;loop@1396:4&gt;.&lt;block@1396:32&gt;.&lt;block@1732:10&gt;.&lt;block@1796:15&gt;.&lt;arrow@1832:27&gt;`

将「err」作为第 1 个实参交给已绑定接口「ts:runtime/worker/managed-worker#redactedWorkerErrorMessage」，对应捕获形参「error: unknown」。该普通调用关系不替代进程或网络协议关系。

源码：`runtime/worker/managed-worker.ts:1832`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/103`。

### `runtime/worker/managed-worker.ts::main.processInbox.&lt;loop@1396:4&gt;.&lt;block@1396:32&gt;.&lt;block@1732:10&gt;.&lt;object@1858:84&gt;.produceResult`

构造捕获记录，字段按源码次序为「cpbRoot ← cpbRoot；hubRoot ← hubRoot；assignment ← assignment；attemptDir ← attemptDir；assignmentId ← assignmentId；attemptNum ← attemptNum；jobId ← jobId；result ← result；worktreeInfo ← null；log ← jobLog；recoverFinalizerOnly ← recoverFinalizerOnly as (options: LooseRecord) =&gt; Promise&lt;unknown&gt;；assertMutationLease ← assertFinalizerMutationLease」；其余字段见完整操作。不据构造形式推断物理持久化。 将「{\n              cpbRoot,\n              hubRoot,\n              assignment,\n              attemptDir,\n              assignmentId,\n              attemptNum,\n              jobId,\n              result,\n              worktreeInfo,\n              log: jobLog,\n              assertMutationLease: assertFinalizerMutationLease,\n              mutationFence: fi…［展示截断；完整操作保留］」作为第 1 个实参交给已绑定接口「ts:runtime/worker/assignment-finalizer#finalizeAndWriteSuccessfulResult」，对应捕获形参「{\n  cpbRoot,\n  hubRoot,\n  dataRoot,\n  assignment,\n  attemptDir,\n  assignmentId,\n  attemptNum,\n  jobId,\n  result,\n  worktreeInfo,\n  log = null,\n  resolveTransport = resolveGithubTransport,\n  resolveDataRoot = resolveProjectDataRoot,\n  finalizeQueueEntry = finalizeSuccessfulQueueEntry,\n  writeResult = writeJsonOnce,\n  assertMutationLease = null…［展示截断；完整操作保留］」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「recoverFinalizerOnly」的初始化来源为「runtimeServices.recoverFinalizerOnly」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(typeof recoverFinalizerOnly !== "function")」的捕获提前退出分支为「throw：Object.assign(new Error("finalizer-only recovery service is unavailable"), {\n                  code: "FINALIZER_RECOVERY_UNAVAILABLE",\n                })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw Object.assign(new Error("finalizer-only recovery service is unavailable"), {\n                  code: "FINALIZER_RECOVERY_UNAVAILABLE",\n                });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「cpbRoot」关联路径「cpbRoot」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「23781d0fea362fb6610e1c4b」先于语句位置「1」的操作「bf507f9bbc900d2f41e3f484」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`runtime/worker/managed-worker.ts:1859`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/104`。

### `runtime/worker/managed-worker.ts::main.processInbox.&lt;loop@1396:4&gt;.&lt;block@1396:32&gt;.&lt;block@1732:10&gt;.&lt;object@1858:84&gt;.&lt;arrow@1904:14&gt;`

构造捕获记录，字段按源码次序为「projectRuntimeRoot ← assignment.projectRuntimeRoot；sourcePath ← assignment.sourcePath；entryId ← assignment.entryId；managedWorktree ← worktreeInfo!」。不据构造形式推断物理持久化。 将「{\n                projectRuntimeRoot: assignment.projectRuntimeRoot,\n                sourcePath: assignment.sourcePath,\n                entryId: assignment.entryId,\n                managedWorktree: worktreeInfo!,\n              }」作为第 1 个实参交给已绑定接口「ts:runtime/worker/worktree-manager#cleanupManagedWorkerWorktree」，对应捕获形参「options: CleanupManagedWorkerWorktreeOptions」。该普通调用关系不替代进程或网络协议关系。 以字段投影形式「assignment.projectRuntimeRoot」关联路径「assignment.projectRuntimeRoot」；只描述捕获来源，不证明当时的字段值。

源码：`runtime/worker/managed-worker.ts:1904`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/105`。

### `runtime/worker/managed-worker.ts::main.processInbox.&lt;loop@1396:4&gt;.&lt;block@1396:32&gt;.&lt;block@1732:10&gt;.&lt;object@1858:84&gt;.&lt;arrow@1912:14&gt;`

构造捕获记录，字段按源码次序为「projectRuntimeRoot ← assignment.projectRuntimeRoot；sourcePath ← assignment.sourcePath；entryId ← assignment.entryId；managedWorktree ← worktreeInfo!」。不据构造形式推断物理持久化。 将「{\n                projectRuntimeRoot: assignment.projectRuntimeRoot,\n                sourcePath: assignment.sourcePath,\n                entryId: assignment.entryId,\n                managedWorktree: worktreeInfo!,\n              }」作为第 1 个实参交给已绑定接口「ts:runtime/worker/worktree-manager#verifyRetainedManagedWorkerWorktree」，对应捕获形参「{\n  projectRuntimeRoot,\n  sourcePath,\n  entryId,\n  managedWorktree,\n  slug = managedWorktreeSlug(projectRuntimeRoot),\n  runGit = defaultGitRunner,\n}: CleanupManagedWorkerWorktreeOptions」。该普通调用关系不替代进程或网络协议关系。 以字段投影形式「assignment.projectRuntimeRoot」关联路径「assignment.projectRuntimeRoot」；只描述捕获来源，不证明当时的字段值。

源码：`runtime/worker/managed-worker.ts:1912`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/106`。

### `runtime/worker/managed-worker.ts::main.processInbox.&lt;loop@1396:4&gt;.&lt;block@1396:32&gt;.&lt;block@1732:10&gt;.&lt;object@1858:84&gt;.beforePublish`

构造捕获记录，字段按源码次序为「operation ← "result.publish"；phase ← "before-write"；mode ← String(finalizeResult.mode || metadata.finalizeMode || metadata.finalizerMode || "dry-run")；project ← assignment.projectId；entryId ← assignment.entryId；jobId ← String(finalizeResult.jobId || jobId)；finalizationId ← typeof remoteIntent.finalizationId === "string"\n                ? remoteIntent.finalizationId\n                : typeof finalizeResult.finalizationId === "stri…［展示截断；完整操作保留］；generation ← Number.isSafeInteger(remoteIntent.generation)\n                ? Number(remoteIntent.generation)\n                : Number.isSafeInteger(finalizeResult.generati…［展示截断；完整操作保留］；repository ← String(\n                metadataCapability.repository\n                || sourceCapability.repository\n                || metadata.repo\n                || met…［展示截断；完整操作保留］；issueNumber ← typeof metadataCapability.issueNumber === "string"\n                || typeof metadataCapability.issueNumber === "number"\n                ? metadataCapability.…［展示截断；完整操作保留］；commit ← typeof finalizeResult.commit === "string" ? finalizeResult.commit : null；tree ← typeof finalizeResult.tree === "string" ? finalizeResult.tree : null」。不据构造形式推断物理持久化。 将「attemptResult.finalizeResult」作为第 1 个实参交给已绑定接口「ts:runtime/worker/managed-worker#recordValue」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「finalizeResult」的初始化来源为「recordValue(attemptResult.finalizeResult)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以字段投影形式「assignment.projectId」关联路径「assignment.projectId」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「3fcca1a9ef6b8e1247df1c2a」先于语句位置「1」的操作「14cfe9ae75f699462a3dbafb」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`runtime/worker/managed-worker.ts:1920`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/107`。

### `runtime/worker/managed-worker.ts::main.inboxJsonCount`

在调用形式「workerStore.hasInboxWork」中提供第 1 个实参「workerId」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return await workerStore.hasInboxWork(workerId) ? 1 : 0;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`runtime/worker/managed-worker.ts:2236`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/108`。

### `runtime/worker/managed-worker.ts::main.exitIdleWorkerIfRequested`

将「"idle"」作为第 1 个实参交给已绑定接口「ts:runtime/worker/managed-worker#main.shutdown」，对应捕获形参「signal: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「count」的初始化来源为「await inboxJsonCount()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「idleSince」存在源更新「idleSince ??= now」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!shouldExitWorkerOnIdle() || processing || exitingIdle)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「f0c52543ca9107f42dc528a7」先于语句位置「1」的操作「fc2be45a8ad903453405555f」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 以无显式实参的调用形式「inboxJsonCount」调用已绑定接口「ts:runtime/worker/managed-worker#main.inboxJsonCount」；没有据调用存在断言激活、存储或网络效果。

源码：`runtime/worker/managed-worker.ts:2240`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/109`。

### `runtime/worker/managed-worker.ts::main.processInboxGuarded`

以无显式实参的调用形式「processInbox」调用已绑定接口「ts:runtime/worker/managed-worker#main.processInbox」；没有据调用存在断言激活、存储或网络效果。 对捕获 binding「processing」存在源更新「processing = false」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(processing)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「87af4d031a79233e9f09aa87」先于语句位置「1」的操作「b4b19234abd2dc2a47f1ac5f」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 以无显式实参的调用形式「exitIdleWorkerIfRequested」调用已绑定接口「ts:runtime/worker/managed-worker#main.exitIdleWorkerIfRequested」；没有据调用存在断言激活、存储或网络效果。

源码：`runtime/worker/managed-worker.ts:2254`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/110`。

### `runtime/worker/managed-worker.ts::main.&lt;arrow@2281:20&gt;`

以无显式实参的调用形式「processInboxGuarded」调用已绑定接口「ts:runtime/worker/managed-worker#main.processInboxGuarded」；没有据调用存在断言激活、存储或网络效果。

源码：`runtime/worker/managed-worker.ts:2281`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/111`。

### `runtime/worker/managed-worker.ts::main.&lt;arrow@2286:22&gt;`

在调用形式「String」中提供第 1 个实参「err」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`runtime/worker/managed-worker.ts:2286`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/112`。

### `runtime/worker/managed-worker.ts::main.&lt;arrow@2292:35&gt;`

在调用形式「String」中提供第 1 个实参「err」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`runtime/worker/managed-worker.ts:2292`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/113`。

### `runtime/worker/managed-worker.ts::main.&lt;arrow@2297:26&gt;`

以无显式实参的调用形式「processInboxGuarded」调用已绑定接口「ts:runtime/worker/managed-worker#main.processInboxGuarded」；没有据调用存在断言激活、存储或网络效果。 保留同一块中的正常源码顺序：语句位置「0」的操作「e80878082de272465e901ac4」先于语句位置「1」的操作「dd8904ab6b6f88cb72d49b93」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 以无显式实参的调用形式「exitIdleWorkerIfRequested」调用已绑定接口「ts:runtime/worker/managed-worker#main.exitIdleWorkerIfRequested」；没有据调用存在断言激活、存储或网络效果。

源码：`runtime/worker/managed-worker.ts:2297`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/114`。

### `runtime/worker/managed-worker.ts::main.&lt;arrow@2305:18&gt;`

以无显式实参的调用形式「exitIdleWorkerIfRequested」调用已绑定接口「ts:runtime/worker/managed-worker#main.exitIdleWorkerIfRequested」；没有据调用存在断言激活、存储或网络效果。

源码：`runtime/worker/managed-worker.ts:2305`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/115`。

### `runtime/worker/managed-worker.ts::main.shutdown`

构造捕获记录，字段按源码次序为「status ← "exited"；exitSignal ← signal」。不据构造形式推断物理持久化。 以无显式实参的调用形式「stopWorkerAcpPool」调用已绑定接口「ts:runtime/worker/managed-worker#main.stopWorkerAcpPool」；没有据调用存在断言激活、存储或网络效果。 对捕获 binding「pollTimer」存在源更新「pollTimer = null」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(shuttingDown)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「signal」关联路径「signal」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「9c2af8126284f3b0e2e10746」先于语句位置「1」的操作「41a519c659d3bc5c81b27c5f」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`runtime/worker/managed-worker.ts:2313`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/116`。

### `runtime/worker/managed-worker.ts::main.&lt;arrow@2335:23&gt;`

将「"SIGINT"」作为第 1 个实参交给已绑定接口「ts:runtime/worker/managed-worker#main.shutdown」，对应捕获形参「signal: string」。该普通调用关系不替代进程或网络协议关系。

源码：`runtime/worker/managed-worker.ts:2335`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/117`。

### `runtime/worker/managed-worker.ts::main.&lt;arrow@2336:24&gt;`

将「"SIGTERM"」作为第 1 个实参交给已绑定接口「ts:runtime/worker/managed-worker#main.shutdown」，对应捕获形参「signal: string」。该普通调用关系不替代进程或网络协议关系。

源码：`runtime/worker/managed-worker.ts:2336`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/118`。

### `server/index.ts::sendJson`

构造捕获记录，字段按源码次序为「cache-control ← "no-store"；content-length ← Buffer.byteLength(body)；content-type ← "application/json; charset=utf-8"」。不据构造形式推断物理持久化。 在调用形式「JSON.stringify」中提供第 1 个实参「payload」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「body」的初始化来源为「`${JSON.stringify(payload)}\n`」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留记录复制/展开来源「headers」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「364dc9ff48283896545f82fd」先于语句位置「1」的操作「28157fc76fafe6d4ec24b267」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/index.ts:73`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/119`。

### `server/index.ts::startHubServer`

构造捕获记录，字段按源码次序为「server ← server；host ← host；hubRoot ← hubRoot；port ← address.port；url ← `http://${host}:${address.port}`；close ← () =&gt; {\n      if (!closing) {\n        closing = (async () =&gt; {\n          const errors: unknown[] = [];\n          await closeServer(server).catch((error) =&gt; …［展示截断；完整操作保留］」。不据构造形式推断物理持久化。 将「{\n    hubRoot,\n    maxBytes: options.accessAuditMaxBytes,\n  }」作为第 1 个实参交给已绑定接口「ts:server/services/audit/hub-access-audit#openHubAccessAudit」，对应捕获形参「options: AuditOptions」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「initialAuthConfig」的初始化来源为「authProvider.initial」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(allowAnonymousDev &amp;&amp; !isLoopbackHost(host))」的捕获提前退出分支为「throw：new Error("CPB_HUB_ALLOW_ANONYMOUS_DEV is restricted to loopback development binds")」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new Error("CPB_HUB_ALLOW_ANONYMOUS_DEV is restricted to loopback development binds");」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「hubRoot」关联路径「hubRoot」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「0626394915aae0d185046974」先于语句位置「1」的操作「6622b82deb9ee2ced4711328」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/index.ts:144`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/120`。

### `server/index.ts::startHubServer.&lt;arrow@195:30&gt;`

构造捕获记录，字段按源码次序为「requestId ← requestId；method ← request.method || "UNKNOWN"；path ← auditPath；statusCode ← response.statusCode；outcome ← auditOutcome(response.statusCode)；principalId ← principal?.id || null；principalSource ← principal?.source || null；remoteAddress ← request.socket.remoteAddress || null；requiredScope ← response.requiredScope || null；errorCode ← responseErrorCode(response.payload)；durationMs ← durationMs」。不据构造形式推断物理持久化。 将「{\n          cpbRoot,\n          hubRoot,\n          headers: request.headers,\n          body,\n          beforeMutation: async () =&gt; {\n            attributeWorkerRequest();\n            const durationMs = Number((process.hrtime.bigint() - startedAt) / 1_000_000n);\n            await accessAudit.append({\n              requestId,\n              method: req…［展示截断；完整操作保留］」作为第 1 个实参交给已绑定接口「ts:server/services/hub/worker-state-broker#handleWorkerStateBroker」，对应捕获形参「{\n  cpbRoot,\n  hubRoot,\n  headers,\n  body,\n  beforeMutation,\n}: {\n  cpbRoot: string;\n  hubRoot: string;\n  headers: IncomingHttpHeaders;\n  body: LooseRecord;\n  beforeMutation?: (context: { workerId: string; op: string }) =&gt; Promise&lt;void&gt;;\n}」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「body」的初始化来源为「await readWorkerBrokerBody(request)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「authenticationUnavailable」存在源更新「authenticationUnavailable = error」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(thrownErrorCode(error) !== "HUB_AUTH_CONFIGURATION_UNAVAILABLE")」的捕获提前退出分支为「throw：error」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw error;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「cpbRoot」关联路径「cpbRoot」；只描述捕获来源，不证明当时的字段值。 将「request」作为第 1 个实参交给已绑定接口「ts:server/services/hub/worker-state-broker#readWorkerBrokerBody」，对应捕获形参「request: AsyncIterable&lt;unknown&gt;」。该普通调用关系不替代进程或网络协议关系。

源码：`server/index.ts:195`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/121`。

### `server/index.ts::startHubServer.&lt;arrow@195:30&gt;.&lt;block@201:8&gt;.&lt;block@203:82&gt;.attributeWorkerRequest`

构造捕获记录，字段按源码次序为「id ← `worker:${auditWorkerId}`；scopes ← []；projects ← []；source ← "worker-broker"；expiresAt ← null」。不据构造形式推断物理持久化。 对捕获 binding「principal」存在源更新「principal = {\n            id: `worker:${auditWorkerId}`,\n            scopes: [],\n            projects: [],\n            source: "worker-broker",\n            expiresAt: null,\n          }」；循环和分支条件见操作上下文，未推执行次数或最终数值。 保留同一块中的正常源码顺序：语句位置「0」的操作「db1d9ddd0903e0329660d601」先于语句位置「1」的操作「8da5721b9742fbdb910fd4b5」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/index.ts:212`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/122`。

### `server/index.ts::startHubServer.&lt;arrow@195:30&gt;.&lt;block@201:8&gt;.&lt;block@203:82&gt;.&lt;object@222:53&gt;.beforeMutation`

构造捕获记录，字段按源码次序为「requestId ← requestId；method ← request.method || "UNKNOWN"；path ← auditPath；statusCode ← 202；outcome ← "mutation_intent"；principalId ← principal?.id || null；principalSource ← principal?.source || null；remoteAddress ← request.socket.remoteAddress || null；requiredScope ← null；errorCode ← null；durationMs ← durationMs」。不据构造形式推断物理持久化。 在调用形式「accessAudit.append」中提供第 1 个实参「{\n              requestId,\n              method: request.method || "UNKNOWN",\n              path: auditPath,\n              statusCode: 202,\n              outcome: "mutation_intent",\n              principalId: principal?.id || null,\n              principalSource: principal?.source || null,\n              remoteAddress: request.socket.remoteAddress || n…［展示截断；完整操作保留］」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「durationMs」的初始化来源为「Number((process.hrtime.bigint() - startedAt) / 1_000_000n)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以字段投影形式「requestId」关联路径「requestId」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「f89d930aaac0866f2c1d2e6a」先于语句位置「1」的操作「840f6dfb55cb689557101869」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/index.ts:227`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/123`。

### `server/index.ts::startHubServer.&lt;arrow@195:30&gt;.&lt;block@201:8&gt;.&lt;block@247:13&gt;.&lt;block@281:13&gt;.&lt;block@308:81&gt;.&lt;block@322:17&gt;.&lt;object@324:23&gt;.&lt;arrow@326:39&gt;`

将「principal!」作为第 1 个实参交给已绑定接口「ts:shared/hub-auth#hubPrincipalCanAccessProject」，对应捕获形参「principal: HubPrincipal」。该普通调用关系不替代进程或网络协议关系。

源码：`server/index.ts:326`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/124`。

### `server/index.ts::startHubServer.&lt;object@469:9&gt;.close`

以无显式实参的调用形式「(async () =&gt; {\n          const errors: unknown[] = [];\n          await closeServer(server).catch((error) =&gt; errors.push(error));\n          await accessAudit.close().catch((error) =&gt; errors.push(error));\n          await runtime.markDead().catch((error) =&gt; errors.push(error));\n          if (errors.length &gt; 0) throw new AggregateError(errors, "Hub shutdown…［展示截断；完整操作保留］」调用已绑定接口「ts:server/index#startHubServer.&lt;object@469:9&gt;.close.&lt;block@476:20&gt;.&lt;arrow@477:19&gt;」；没有据调用存在断言激活、存储或网络效果。 对捕获 binding「closing」存在源更新「closing = (async () =&gt; {\n          const errors: unknown[] = [];\n          await closeServer(server).catch((error) =&gt; errors.push(error));\n          await accessAudit.close().catch((error) =&gt; errors.push(error));\n          await runtime.markDead().catch((error) =&gt; errors.push(error));\n          if (errors.length &gt; 0) throw new AggregateError(errors, "Hu…［展示截断；完整操作保留］」；循环和分支条件见操作上下文，未推执行次数或最终数值。 以「return closing;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`server/index.ts:475`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/125`。

### `server/index.ts::startHubServer.&lt;object@469:9&gt;.close.&lt;block@476:20&gt;.&lt;arrow@477:19&gt;`

将「server」作为第 1 个实参交给已绑定接口「ts:server/index#closeServer」，对应捕获形参「server: Server」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「errors」的初始化来源为「[]」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(errors.length &gt; 0)」的捕获提前退出分支为「throw：new AggregateError(errors, "Hub shutdown did not complete cleanly")」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new AggregateError(errors, "Hub shutdown did not complete cleanly");」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「b25793556243e886f4f48aad」先于语句位置「1」的操作「94cbb2f60b8982fbb724e8d1」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/index.ts:477`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/126`。

### `server/index.ts::startHubServer.&lt;object@469:9&gt;.close.&lt;block@476:20&gt;.&lt;arrow@477:19&gt;.&lt;arrow@479:42&gt;`

在调用形式「errors.push」中提供第 1 个实参「error」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`server/index.ts:479`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/127`。

### `server/index.ts::startHubServer.&lt;object@469:9&gt;.close.&lt;block@476:20&gt;.&lt;arrow@477:19&gt;.&lt;arrow@480:42&gt;`

在调用形式「errors.push」中提供第 1 个实参「error」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`server/index.ts:480`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/128`。

### `server/index.ts::startHubServer.&lt;object@469:9&gt;.close.&lt;block@476:20&gt;.&lt;arrow@477:19&gt;.&lt;arrow@481:41&gt;`

在调用形式「errors.push」中提供第 1 个实参「error」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`server/index.ts:481`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/129`。

### `server/orchestrator/failure-router.ts::FailureRouter.route`

构造捕获记录，字段按源码次序为「action ← "retry_same_worker"；reason ← `verifier read-only mutation denied: ${failure.reason}`；retryable ← true；retryPhase ← "verify"」。不据构造形式推断物理持久化。 将「assignment」作为第 1 个实参交给已绑定接口「ts:shared/types#recordValue」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「routingLabel」的初始化来源为「typeof failureCause.routingLabel === "string" ? failureCause.routingLabel : ""」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「verificationRetryScope」存在源更新「verificationRetryScope = collectVerificationRetryScope(failure)」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(\n      failure.retryable === false &amp;&amp;\n      failure.kind !== FailureKind.PLAN_BOUNDED_HANDOFF_TIMEOUT &amp;&amp;\n      failure.kind !== FailureKind.PERMISSION_DENIED &amp;&amp;\n      failure.kind !== FailureKind.HUMAN_APPROVAL_REQUIRED &amp;&amp;\n      // Scope violations with a checklist routing label get bounded\n      // executor remediation turn; unlabelled violations sti…［展示截断；完整操作保留］」的捕获提前退出分支为「return：{\n        action: "mark_failed",\n        reason: `${failure.kind} is non-retryable: ${failure.reason}`,\n        retryable: false,\n        ...failureMetadata,\n      }」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return {\n        action: "mark_failed",\n        reason: `${failure.kind} is non-retryable: ${failure.reason}`,\n        retryable: false,\n        ...failureMetadata,\n      };」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「failure」关联路径「failure」；只描述捕获来源，不证明当时的字段值。 将「{\n          action: "retry_same_worker",\n          reason: failure.reason,\n          retryable: true,\n          retryPhase: routing.retryPhase,\n          ...(routing.requiresFixScope &amp;&amp; verificationRetryScope.length &gt; 0 ? { fixScope: verificationRetryScope } : {}),\n        }」作为第 1 个实参交给已绑定接口「ts:server/orchestrator/failure-router#FailureRouter.route.retryDecision」，对应捕获形参「decision: LooseRecord」。该普通调用关系不替代进程或网络协议关系。

源码：`server/orchestrator/failure-router.ts:103`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/130`。

### `server/orchestrator/failure-router.ts::FailureRouter.route.recoveryFor`

构造捕获记录，字段按源码次序为「failure ← failure；previousFingerprint ← normalizedPreviousFingerprint；previousStrategy ← previousStrategy；preferredStrategy ← preferredStrategy；scope ← "queue"」。不据构造形式推断物理持久化。 将「{\n      failure,\n      previousFingerprint: normalizedPreviousFingerprint,\n      previousStrategy,\n      preferredStrategy,\n      scope: "queue",\n    }」作为第 1 个实参交给已绑定接口「ts:core/contracts/failure-recovery#selectFailureRecovery」，对应捕获形参「{\n  failure,\n  previousFingerprint = null,\n  previousStrategy = null,\n  preferredStrategy = null,\n  scope = "queue",\n}: {\n  failure: unknown;\n  previousFingerprint?: string | null;\n  previousStrategy?: string | null;\n  preferredStrategy?: string | null;\n  scope?: RecoveryScope;\n}」。该普通调用关系不替代进程或网络协议关系。 以字段投影形式「preferredStrategy」关联路径「preferredStrategy」；只描述捕获来源，不证明当时的字段值。

源码：`server/orchestrator/failure-router.ts:126`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/131`。

### `server/orchestrator/failure-router.ts::FailureRouter.route.retryDecision`

构造捕获记录，字段按源码次序为「failureClass ← recovery.failureClass；failureFingerprint ← recovery.failureFingerprint；failureEvidence ← recovery.failureEvidence；retryStrategy ← recovery.retryStrategy；strategyChanged ← recovery.strategyChanged；forceFreshSession ← recovery.forceFreshSession」。不据构造形式推断物理持久化。 将「preferredStrategy || (typeof decision.retryStrategy === "string" ? decision.retryStrategy : null)」作为第 1 个实参交给已绑定接口「ts:server/orchestrator/failure-router#FailureRouter.route.recoveryFor」，对应捕获形参「preferredStrategy: string | null = null」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「recovery」的初始化来源为「recoveryFor(preferredStrategy || (typeof decision.retryStrategy === "string" ? decision.retryStrategy : null))」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(fingerprintRepeated &amp;&amp; !previousStrategy)」的捕获提前退出分支为「return：{\n          action: "mark_failed",\n          reason: `repeated unchanged failure ${initialRecovery.failureFingerprint} has no recorded prior strategy; blind retry denied`,\n          retryable: false,\n          ...failureMetadata,\n          retryStrategy: null,\n          strategyChanged: false,\n        }」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return {\n          action: "mark_failed",\n          reason: `repeated unchanged failure ${initialRecovery.failureFingerprint} has no recorded prior strategy; blind retry denied`,\n          retryable: false,\n          ...failureMetadata,\n          retryStrategy: null,\n          strategyChanged: false,\n        };」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「recovery.retryStrategy」关联路径「recovery.retryStrategy」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「decision」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。

源码：`server/orchestrator/failure-router.ts:141`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/132`。

### `server/orchestrator/hub-orchestrator.ts::HubOrchestrator.constructor`

构造捕获记录，字段按源码次序为「assignmentStore ← this.assignmentStore；workerStore ← this.workerStore；workerSupervisor ← this.workerSupervisor；leaderLock ← this.leaderLock；failureRouter ← failureRouter；hubRoot ← hubRoot；cpbRoot ← cpbRoot」。不据构造形式推断物理持久化。 将「{ env: process.env, fallbackRoot: cpbRoot }」作为第 1 个实参交给已绑定接口「ts:server/services/executor-root#resolveExecutorRoot」，对应捕获形参「{ env = process.env, fallbackRoot = process.cwd() }: LooseRecord = {}」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「this.hubRoot = hubRoot」，捕获目标为「this.hubRoot」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「readModeFn」的初始化来源为「async () =&gt; {\n      const { readHubConfig: rhc, readSchedulerConfig: rsc } = await import("../services/agent/agent-config.js");\n      return rsc(await rhc(hubRoot)).mode;\n    }」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以字段投影形式「cpbRoot」关联路径「cpbRoot」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「bf0fedabf5701d3dc1868c6c」先于语句位置「1」的操作「c3830c080739128386ca2625」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/hub-orchestrator.ts:153`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/133`。

### `server/orchestrator/hub-orchestrator.ts::HubOrchestrator.constructor.&lt;object@164:44&gt;.providerCapacityFn`

在调用形式「this._providerCapacity」中提供第 1 个实参「agentKey」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`server/orchestrator/hub-orchestrator.ts:169`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/134`。

### `server/orchestrator/hub-orchestrator.ts::HubOrchestrator.constructor.readModeFn`

在调用形式「rhc」中提供第 1 个实参「hubRoot」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return rsc(await rhc(hubRoot)).mode;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「f8993373f652d8a9218f2879」先于语句位置「1」的操作「65a3ed7a915d1c12f129b318」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/hub-orchestrator.ts:177`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/135`。

### `server/orchestrator/hub-orchestrator.ts::HubOrchestrator.tick`

构造捕获记录，字段按源码次序为「assignmentId ← assignment.assignmentId；entryId ← assignment.entryId；projectId ← assignment.projectId；projectRuntimeRoot ← assignment.projectRuntimeRoot；task ← assignment.task；sourcePath ← assignment.sourcePath；workflow ← assignment.workflow；planMode ← assignment.planMode；sourceContext ← assignment.sourceContext；metadata ← assignment.metadata || {}；attempt ← attempt.attempt；attemptToken ← attempt.attemptToken」；其余字段见完整操作。不据构造形式推断物理持久化。 将「this.hubRoot」作为第 1 个实参交给已绑定接口「ts:shared/hub-maintenance#assertHubWritable」，对应捕获形参「hubRoot: string」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「expectedWorker.incarnationToken = worker.incarnationToken」，捕获目标为「expectedWorker.incarnationToken」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「sLog」的初始化来源为「this.log.child({ traceId: candidate.id })」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「reservation」存在源更新「reservation = await updateEntry(this.hubRoot, candidate.id, {\n          status: "scheduled",\n          claimedBy: `orchestrator:${epoch}`,\n          claimedAt: new Date().toISOString(),\n          // Persist the exact smart-scheduler score/rank/evidence that led to\n          // dispatch. Keeping this only on the in-memory candidate made the\n          //…［展示截断；完整操作保留］」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!registeredProject?.projectRuntimeRoot)」的捕获提前退出分支为「throw：new Error(`project runtime root required for dispatch: ${candidate.projectId}`)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return { stopped: true, reason: "Hub maintenance became active" };」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`server/orchestrator/hub-orchestrator.ts:300`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/136`。

### `server/orchestrator/hub-orchestrator.ts::HubOrchestrator._providerCapacity`

构造捕获记录，字段按源码次序为「providerKey ← providerKey；active ← active；total ← total；available ← Math.max(0, total - active)」。不据构造形式推断物理持久化。 将「this.hubRoot」作为第 1 个实参交给已绑定接口「ts:server/services/infra#resolveHubConcurrencyLimits」，对应捕获形参「hubRoot: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「total」的初始化来源为「hubLimits.acpProviderMax」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return {\n      providerKey,\n      active,\n      total,\n      available: Math.max(0, total - active),\n    };」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「providerKey」关联路径「providerKey」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「56d20e602a6686e7afc4c4cc」先于语句位置「1」的操作「64e197ba4e656ef9a92162e5」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/hub-orchestrator.ts:516`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/137`。

### `server/orchestrator/hub-orchestrator.ts::HubOrchestrator._providerCapacity.&lt;arrow@522:34&gt;`

将「e」作为第 1 个实参交给已绑定接口「ts:server/orchestrator/hub-orchestrator#providerAgentForEntry」，对应捕获形参「entry: LooseRecord」。该普通调用关系不替代进程或网络协议关系。

源码：`server/orchestrator/hub-orchestrator.ts:522`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/138`。

### `server/orchestrator/reconciler.ts::persistedFinalizerSuccessContractValid`

构造捕获记录，字段按源码次序为「assignmentId ← assignment.assignmentId；entryId ← assignment.entryId；attemptToken ← attempt.attemptToken；orchestratorEpoch ← attempt.orchestratorEpoch；workerId ← attempt.workerId；workerIncarnation ← heartbeat.workerIncarnation；processIdentity ← {\n      pid: processIdentity.pid,\n      startTimeTicks: processIdentity.startTimeTicks,\n    }」。不据构造形式推断物理持久化。 将「assignment.metadata」作为第 1 个实参交给已绑定接口「ts:core/contracts/types#recordValue」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「audit」的初始化来源为「recordValue(finalizeResult.audit)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(metadata.autoFinalize !== true)」的捕获提前退出分支为「return：true」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return true;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「assignment.assignmentId」关联路径「assignment.assignmentId」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「(readOnlyRecovery ? {\n      claimPolicy: "durable-observation",\n      acceptedOwnerDigest: ownerProof.acceptedOwnerDigest,\n    } : {})」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。

源码：`server/orchestrator/reconciler.ts:489`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/139`。

### `server/orchestrator/reconciler.ts::persistedFinalizerGitReadbackValid`

构造捕获记录，字段按源码次序为「repositoryPath ← sourcePath；result ← finalizeResult；candidate ← candidate；expectedRef ← `refs/heads/${targetBranch}`」。不据构造形式推断物理持久化。 将「assignment.metadata」作为第 1 个实参交给已绑定接口「ts:core/contracts/types#recordValue」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「intent」的初始化来源为「recordValue(finalizeResult.remoteIntent)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(mode !== "local" &amp;&amp; mode !== "remote" &amp;&amp; mode !== "pr")」的捕获提前退出分支为「return：true」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return true;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「sourcePath」关联路径「sourcePath」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「05475d57fc4444a1d21626c2」先于语句位置「1」的操作「cf56338a0ba3e7f7def2c584」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/reconciler.ts:633`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/140`。

### `server/orchestrator/reconciler.ts::persistedFinalizerJournalValid`

构造捕获记录，字段按源码次序为「dataRoot ← requestedDataRoot」。不据构造形式推断物理持久化。 将「assignment.metadata」作为第 1 个实参交给已绑定接口「ts:core/contracts/types#recordValue」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「mode」的初始化来源为「expectedFinalizeMode(recordValue(assignment.metadata))」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(mode !== "remote" &amp;&amp; mode !== "pr")」的捕获提前退出分支为「return：true」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return true;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「hubRoot」关联路径「hubRoot」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「(requestedDataRoot ? { dataRoot: requestedDataRoot } : {})」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。

源码：`server/orchestrator/reconciler.ts:664`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/141`。

### `server/orchestrator/reconciler.ts::buildFinalizerOnlyRecoveryPlan`

构造捕获记录，字段按源码次序为「schema ← FINALIZER_HANDOFF_SCHEMA；kind ← "explicit-handoff"；previousClaimId ← priorAttemptProof.previousClaimId；evidenceId ← priorAttemptProof.evidenceId；observedAt ← priorAttemptProof.observedAt；evidence ← priorAttemptProof.evidence」。不据构造形式推断物理持久化。 将「result.finalization」作为第 1 个实参交给已绑定接口「ts:core/contracts/types#recordValue」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「allowMutation」的初始化来源为「safePartialContinuation」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!finalizerFailed || finalizeResult.ok === true || (mode !== "remote" &amp;&amp; mode !== "pr") || !jobId || !intentOriginJobId)」的捕获提前退出分支为「return：null」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return null;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「FINALIZER_HANDOFF_SCHEMA」关联路径「FINALIZER_HANDOFF_SCHEMA」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「(takeover ? {\n      previousClaimId: takeover.previousClaimId,\n      takeover,\n    } : {})」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。

源码：`server/orchestrator/reconciler.ts:899`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/142`。

### `server/orchestrator/reconciler.ts::Reconciler.constructor`

将「"reconciler"」作为第 1 个实参交给已绑定接口「ts:shared/logger#createLogger」，对应捕获形参「component: string」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「this.hubRoot = hubRoot」，捕获目标为「this.hubRoot」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「d397af49050fe3b33e0a1939」先于语句位置「1」的操作「980968decfeda174226627f9」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/reconciler.ts:1132`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/143`。

### `server/orchestrator/reconciler.ts::Reconciler.reconcileAssignments`

构造捕获记录，字段按源码次序为「assignmentId ← assignment.assignmentId；attempt ← attempt.attempt；orchestratorEpoch ← attempt.orchestratorEpoch；status ← "failed"；jobResult ← { status: "failed", failure: { kind: "worker_heartbeat_lost", reason: "assignment not accepted within TTL" } }；attemptToken ← attempt.attemptToken」。不据构造形式推断物理持久化。 在调用形式「this.log.child」中提供第 1 个实参「{ traceId: assignment.assignmentId }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 包含赋值/更新「progressDelay.cause.probe = probe」，捕获目标为「progressDelay.cause.probe」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「aLog」的初始化来源为「this.log.child({ traceId: assignment.assignmentId })」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以字段投影形式「assignment.assignmentId」关联路径「assignment.assignmentId」；只描述捕获来源，不证明当时的字段值。 记录消息形状中的固定文本字段「kind」及捕获形式「"worker_heartbeat_lost"」。单个文本字段不是跨语言调用或传输成功的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「4e5cd42176120cf55cd886a7」先于语句位置「1」的操作「d25d7c1a53c4c45105f71433」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/reconciler.ts:1222`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/144`。

### `server/orchestrator/reconciler.ts::Reconciler._compensateFinalization`

构造捕获记录，字段按源码次序为「allowCommittedFile ← Boolean(assignment.resultWrittenAt)」。不据构造形式推断物理持久化。 在调用形式「this._readAttemptResult」中提供第 3 个实参「{\n        allowCommittedFile: Boolean(assignment.resultWrittenAt),\n      }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「result」的初始化来源为「await this._readAttemptResult(assignment.assignmentId, attempt.attempt, {\n        allowCommittedFile: Boolean(assignment.resultWrittenAt),\n      })」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!attempt)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「1」的操作「e823cde13e6df1088f53b0b8」先于语句位置「3」的操作「83d92d0c43623a3a69573b28」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/reconciler.ts:1677`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/145`。

### `server/orchestrator/reconciler.ts::Reconciler._finalizeAssignment`

在调用形式「this._finalizeQueue」中提供第 1 个实参「assignment」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 保留同一块中的正常源码顺序：语句位置「0」的操作「39f1cac7c497fc480eee8719」先于语句位置「1」的操作「4e52f5067c6d5108c242fd0d」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/reconciler.ts:1699`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/146`。

### `server/orchestrator/reconciler.ts::Reconciler._finalizeQueue`

构造捕获记录，字段按源码次序为「action ← decision.action；reason ← decision.reason；retryable ← boolOrNull(decision.retryable)；retryAt ← new Date().toISOString()；untilTs ← decision.untilTs ?? null；failureClass ← retryContract.failureClass || null；failureFingerprint ← retryContract.failureFingerprint || null；retryStrategy ← retryContract.retryStrategy || null；strategyChanged ← retryContract.strategyChanged === true；forceFreshSession ← retryContract.forceFreshSession === true」。不据构造形式推断物理持久化。 将「assignment」作为第 1 个实参交给已绑定接口「ts:server/orchestrator/reconciler#persistedFinalizerSuccessContractValid」，对应捕获形参「assignment: ReconcilerRecord」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「reason」的初始化来源为「effectiveResult.jobResult?.failure?.reason\n        || effectiveResult.failure?.reason\n        || "assignment finalization blocked"」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以字段投影形式「persistedHeartbeat」关联路径「persistedHeartbeat」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「attempt」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。 记录消息形状中的固定文本字段「kind」及捕获形式「"finalizer_failed"」。单个文本字段不是跨语言调用或传输成功的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「f30f382bba1c9d8dc99fccde」先于语句位置「1」的操作「8c7fb6a0ca02ef9c378f9fa2」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「assignment」作为第 1 个实参交给已绑定接口「ts:server/orchestrator/reconciler#persistedFinalizerGitReadbackValid」，对应捕获形参「assignment: ReconcilerRecord」。该普通调用关系不替代进程或网络协议关系。

源码：`server/orchestrator/reconciler.ts:1704`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/147`。

### `server/orchestrator/reconciler.ts::Reconciler._readAttemptResult`

构造捕获记录，字段按源码次序为「maxBytes ← ATTEMPT_RESULT_MAX_BYTES」。不据构造形式推断物理持久化。 将「{ maxBytes: ATTEMPT_RESULT_MAX_BYTES }」作为第 2 个实参交给已绑定接口「ts:shared/primitives/durable-directory-lock#readBoundedRegularFileNoFollow」，对应捕获形参「{ maxBytes, hooks }: BoundedRegularFileReadOptions」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「attempt」的初始化来源为「await this.assignments.getActiveAttempt(assignmentId)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(Number(attempt?.attempt) !== attemptNum)」的捕获提前退出分支为「return：null」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return null;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「ATTEMPT_RESULT_MAX_BYTES」关联路径「ATTEMPT_RESULT_MAX_BYTES」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「8c2df64bc3fe9017831620e5」先于语句位置「1」的操作「f77208e3f19362b4e955fa01」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/reconciler.ts:2036`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/148`。

### `server/orchestrator/scheduler.ts::Scheduler.constructor`

将「maxActivePerProject」作为第 1 个实参交给已绑定接口「ts:server/services/infra#positiveInt」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「this.hubRoot = hubRoot」，捕获目标为「this.hubRoot」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「09cd6cbe883653cb3d3d8886」先于语句位置「1」的操作「2715ecf622f94ed89057fbd0」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/scheduler.ts:147`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/149`。

### `server/orchestrator/scheduler.ts::Scheduler._preparePendingPool`

构造捕获记录，字段按源码次序为「status ← "pending"；claimedBy ← null；claimedAt ← null」。不据构造形式推断物理持久化。 将「{\n      claimTimeoutMs: CLAIM_TIMEOUT_MS,\n      assignmentStore: this.assignments,\n    }」作为第 2 个实参交给已绑定接口「ts:server/services/hub/hub-queue#recoverStaleInProgressAsync」，对应捕获形参「opts: QueueRecoveryOptions」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「entry」的初始化来源为「allEntries.find((e) =&gt; e.id === id)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return await listQueue(this.hubRoot) as SchedulerEntry[];」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「CLAIM_TIMEOUT_MS」关联路径「CLAIM_TIMEOUT_MS」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「46e1f131a9333adf8d395bfe」先于语句位置「1」的操作「5a79ce915b4a7e1754a1a0a2」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/scheduler.ts:173`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/150`。

### `server/orchestrator/scheduler.ts::Scheduler._preparePendingPool.&lt;arrow@176:50&gt;`

构造捕获记录，字段按源码次序为「expectedStatus ← entry.status；expectedClaimedAt ← entry.claimedAt ?? null；expectedUpdatedAt ← entry.updatedAt ?? null」。不据构造形式推断物理持久化。 以字段投影形式「entry.status」关联路径「entry.status」；只描述捕获来源，不证明当时的字段值。

源码：`server/orchestrator/scheduler.ts:176`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/151`。

### `server/orchestrator/scheduler.ts::Scheduler._filterDagReady`

在调用形式「Set」中提供第 1 个实参「allEntries.filter(e =&gt; e.status === "completed").map(e =&gt; e.id)」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「completedIds」的初始化来源为「new Set(\n      allEntries.filter(e =&gt; e.status === "completed").map(e =&gt; e.id),\n    )」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return pending.filter(entry =&gt; {\n      const deps = entry.metadata?.dependsOn;\n      if (!deps || !Array.isArray(deps) || deps.length === 0) return true;\n      return deps.every(depId =&gt; completedIds.has(depId));\n    });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「6b6311afeb7304d978816a77」先于语句位置「1」的操作「fe3fd4c6e8727714289d0b7b」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/scheduler.ts:215`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/152`。

### `server/orchestrator/scheduler.ts::Scheduler._filterDagReady.&lt;arrow@219:26&gt;`

在调用形式「Array.isArray」中提供第 1 个实参「deps」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「deps」的初始化来源为「entry.metadata?.dependsOn」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!deps || !Array.isArray(deps) || deps.length === 0)」的捕获提前退出分支为「return：true」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return true;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「e10be0ebe467a3f2b6b77357」先于语句位置「1」的操作「ca475e60782235124a76ec69」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/scheduler.ts:219`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/153`。

### `server/orchestrator/scheduler.ts::Scheduler._filterDagReady.&lt;arrow@219:26&gt;.&lt;arrow@222:24&gt;`

在调用形式「completedIds.has」中提供第 1 个实参「depId」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`server/orchestrator/scheduler.ts:222`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/154`。

### `server/orchestrator/scheduler.ts::Scheduler._filterByProjectCapacity`

在调用形式「pending.filter」中提供第 1 个实参「e =&gt; {\n      if (isMutatingEntry(e)) {\n        const projectLimit = projectLimits.get(e.projectId) ?? hubLimits.maxActivePerProject;\n        if (projectLimit &gt; 0 &amp;&amp; (activeMutatingByProject[e.projectId] || 0) &gt;= projectLimit) {\n          return false;\n        }\n      }\n      return true;\n    }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return pending.filter(e =&gt; {\n      if (isMutatingEntry(e)) {\n        const projectLimit = projectLimits.get(e.projectId) ?? hubLimits.maxActivePerProject;\n        if (projectLimit &gt; 0 &amp;&amp; (activeMutatingByProject[e.projectId] || 0) &gt;= projectLimit) {\n          return false;\n        }\n      }\n      return true;\n    });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`server/orchestrator/scheduler.ts:236`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/155`。

### `server/orchestrator/scheduler.ts::Scheduler._filterByProjectCapacity.&lt;arrow@237:26&gt;`

将「e」作为第 1 个实参交给已绑定接口「ts:server/services/hub/hub-queue#isMutatingEntry」，对应捕获形参「entry: QueueEntryInput」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「projectLimit」的初始化来源为「projectLimits.get(e.projectId) ?? hubLimits.maxActivePerProject」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(projectLimit &gt; 0 &amp;&amp; (activeMutatingByProject[e.projectId] || 0) &gt;= projectLimit)」的捕获提前退出分支为「return：false」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return false;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「a3b083445b31e3f490e71ac2」先于语句位置「1」的操作「66873eb4340033b6eb62c058」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/scheduler.ts:237`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/156`。

### `server/orchestrator/scheduler.ts::Scheduler._reserveProjectCapacity`

构造捕获的空记录「{}」；没有从空记录形式推断额外字段或持久效果。 在调用形式「pending.filter」中提供第 1 个实参「(entry) =&gt; {\n      if (!isMutatingEntry(entry)) return true;\n      const projectLimit = projectLimits.get(entry.projectId) ?? hubLimits.maxActivePerProject;\n      if (projectLimit &lt;= 0) return true;\n      const projected = (activeMutatingByProject[entry.projectId] || 0)\n        + (reservedByProject[entry.projectId] || 0);\n      if (projected &gt;= project…［展示截断；完整操作保留］」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「reservedByProject」的初始化来源为「{}」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return pending.filter((entry) =&gt; {\n      if (!isMutatingEntry(entry)) return true;\n      const projectLimit = projectLimits.get(entry.projectId) ?? hubLimits.maxActivePerProject;\n      if (projectLimit &lt;= 0) return true;\n      const projected = (activeMutatingByProject[entry.projectId] || 0)\n        + (reservedByProject[entry.projectId] || 0);\n      if…［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「e34a6750320fb62f212cfc7e」先于语句位置「1」的操作「83894659e0f56dd7f5071b1a」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/scheduler.ts:249`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/157`。

### `server/orchestrator/scheduler.ts::Scheduler._reserveProjectCapacity.&lt;arrow@251:26&gt;`

将「entry」作为第 1 个实参交给已绑定接口「ts:server/services/hub/hub-queue#isMutatingEntry」，对应捕获形参「entry: QueueEntryInput」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「projectLimit」的初始化来源为「projectLimits.get(entry.projectId) ?? hubLimits.maxActivePerProject」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!isMutatingEntry(entry))」的捕获提前退出分支为「return：true」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return true;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「1f16d2e25a9b31fba6b24a82」先于语句位置「1」的操作「17f8fb2bf9742d7bbadc4d21」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/scheduler.ts:251`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/158`。

### `server/orchestrator/scheduler.ts::Scheduler._filterByRetryDecisionDue`

在调用形式「pending.filter」中提供第 1 个实参「(entry) =&gt; {\n      const untilMs = parseRetryUntilMs(entry.metadata?.retryDecision?.untilTs);\n      return untilMs === null || untilMs &lt;= now;\n    }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「now」的初始化来源为「Date.now()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return pending.filter((entry) =&gt; {\n      const untilMs = parseRetryUntilMs(entry.metadata?.retryDecision?.untilTs);\n      return untilMs === null || untilMs &lt;= now;\n    });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「16202fe9f6dc5b552f261704」先于语句位置「1」的操作「e7236ac9ac4a0822e08ac60c」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/scheduler.ts:263`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/159`。

### `server/orchestrator/scheduler.ts::Scheduler._filterByRetryDecisionDue.&lt;arrow@265:26&gt;`

将「entry.metadata?.retryDecision?.untilTs」作为第 1 个实参交给已绑定接口「ts:server/orchestrator/scheduler#parseRetryUntilMs」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「untilMs」的初始化来源为「parseRetryUntilMs(entry.metadata?.retryDecision?.untilTs)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return untilMs === null || untilMs &lt;= now;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「30aa67ee8cd53fb1b2f36af0」先于语句位置「1」的操作「778b1849648981d7f016432f」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/scheduler.ts:265`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/160`。

### `server/orchestrator/scheduler.ts::Scheduler.nextCandidates`

构造捕获记录，字段按源码次序为「activeMutatingByProject ← activeMutatingByProject；projectLimits ← projectLimits；hubLimits ← hubLimits；allEntries ← allEntries」。不据构造形式推断物理持久化。 将「{\n      maxActivePerProject: this.maxActivePerProject,\n    }」作为第 2 个实参交给已绑定接口「ts:server/services/infra#resolveHubConcurrencyLimits」，对应捕获形参「fallback: LooseRecord = {}」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「allEntries」的初始化来源为「await this._preparePendingPool()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「pending」存在源更新「pending = await this._smartRank(pending, { activeMutatingByProject, projectLimits, hubLimits, allEntries })」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(pending.length === 0)」的捕获提前退出分支为「return：[]」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return [];」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「this.maxActivePerProject」关联路径「this.maxActivePerProject」；只描述捕获来源，不证明当时的字段值。

源码：`server/orchestrator/scheduler.ts:285`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/161`。

### `server/orchestrator/scheduler.ts::Scheduler.nextCandidates.&lt;block@317:11&gt;.&lt;arrow@318:19&gt;`

将「a.priority」作为第 1 个实参交给已绑定接口「ts:server/services/hub/hub-queue#priorityScore」，对应捕获形参「priority: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「pa」的初始化来源为「priorityScore(a.priority)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(pa !== pb)」的捕获提前退出分支为「return：pa - pb」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return pa - pb;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「56af4d38750b9eabc279f582」先于语句位置「1」的操作「f19903a5c7d579b00d2dd4b9」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/scheduler.ts:318`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/162`。

### `server/orchestrator/scheduler.ts::Scheduler._applyProjectReadinessGate`

构造捕获记录，字段按源码次序为「available ← false；indexDirty ← true；indexStale ← false；worktreeDirty ← false；dirtyReasons ← ["missing_source_or_runtime_root"]」。不据构造形式推断物理持久化。 将「{\n          cpbRoot: this.cpbRoot || project.cpbRoot || project.metadata?.cpbRoot || project.sourcePath,\n          sourcePath: project.sourcePath,\n        }」作为第 1 个实参交给已绑定接口「ts:core/indexing/local-code-index/service#localCodeIndexStatus」，对应捕获形参「options: Readonly&lt;{ cpbRoot?: string; sourcePath: string }&gt;」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「entry.metadata = metadata」，捕获目标为「entry.metadata」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「project」的初始化来源为「await this.getProjectFn(this.hubRoot, entry.projectId)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「localCodeIndexStatusResult」存在源更新「localCodeIndexStatusResult = await localCodeIndexStatus({\n          cpbRoot: this.cpbRoot || project.cpbRoot || project.metadata?.cpbRoot || project.sourcePath,\n          sourcePath: project.sourcePath,\n        })」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!this.getProjectFn)」的捕获提前退出分支为「return：pending」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return pending;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`server/orchestrator/scheduler.ts:344`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/163`。

### `server/orchestrator/scheduler.ts::Scheduler._markLocalCodeIndexUnavailable`

构造捕获记录，字段按源码次序为「status ← "local_code_index_unavailable"；updatedAt ← nowIso()；metadata ← metadata」。不据构造形式推断物理持久化。 以无显式实参的调用形式「nowIso」调用已绑定接口「ts:server/orchestrator/scheduler#nowIso」；没有据调用存在断言激活、存储或网络效果。 包含赋值/更新「entry.metadata = metadata」，捕获目标为「entry.metadata」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「metadata」的初始化来源为「{ ...(entry.metadata || {}), ...metadataPatch }」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!updated)」的捕获提前退出分支为「return：false」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return false;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「metadata」关联路径「metadata」；只描述捕获来源，不证明当时的字段值。

源码：`server/orchestrator/scheduler.ts:493`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/164`。

### `server/orchestrator/scheduler.ts::Scheduler._applyProviderCapacityGate`

将「first」作为第 1 个实参交给已绑定接口「ts:server/orchestrator/scheduler#Scheduler._applyProviderCapacityGate.fits」，对应捕获形参「entry: SchedulerEntry」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「eligible」的初始化来源为「[]」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!first || !this.providerCapacityFn)」的捕获提前退出分支为「return：[]」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return [];」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「5a85c8d1306902baf106b815」先于语句位置「1」的操作「10f46ec2d39f672ef5eebac9」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/scheduler.ts:516`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/165`。

### `server/orchestrator/scheduler.ts::Scheduler._applyProviderCapacityGate.fits`

将「entry」作为第 1 个实参交给已绑定接口「ts:server/orchestrator/scheduler#providerAgentForEntry」，对应捕获形参「entry: SchedulerEntry」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「provider」的初始化来源为「providerAgentForEntry(entry)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!cap || typeof cap !== "object")」的捕获提前退出分支为「return：false」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return false;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「5931295ca319ac2c2b68e061」先于语句位置「1」的操作「9a0553b8d0d924fec58833ea」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/scheduler.ts:535`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/166`。

### `server/orchestrator/scheduler.ts::Scheduler._smartRank`

构造捕获的空记录「{}」；没有从空记录形式推断额外字段或持久效果。 在调用形式「readProviderQuotas」中提供第 1 个实参「this.hubRoot」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「now」的初始化来源为「Date.now()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「providerQuotas」存在源更新「providerQuotas = await readProviderQuotas(this.hubRoot)」；循环和分支条件见操作上下文，未推执行次数或最终数值。 以「return scored.map(({ entry, score, reasons }, index) =&gt; {\n      const retryEvidence = entry.metadata?.sourceContext?.retry || {};\n      entry.metadata = {\n        ...(entry.metadata || {}),\n        schedulerDecision: {\n          mode: "smart",\n          selectedAt,\n          rank: index + 1,\n          score,\n          reasons,\n          retryStrate…［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「b5796ed2e36811aee3426148」先于语句位置「1」的操作「cb8b3b893a20523920398fda」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/scheduler.ts:562`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/167`。

### `server/orchestrator/scheduler.ts::Scheduler._smartRank.&lt;arrow@580:31&gt;`

构造捕获记录，字段按源码次序为「entry ← entry；score ← score；reasons ← reasons」。不据构造形式推断物理持久化。 将「entry.priority」作为第 1 个实参交给已绑定接口「ts:server/services/hub/hub-queue#priorityScore」，对应捕获形参「priority: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「nextEligibleAt」的初始化来源为「parseRetryUntilMs(quota.nextEligibleAt)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「score」存在源更新「score += priorityWeight」；循环和分支条件见操作上下文，未推执行次数或最终数值。 以「return { entry, score, reasons };」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「entry」关联路径「entry」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「62ee1e6ab57d790be8de5da2」先于语句位置「1」的操作「2ddf789acff005272d5762f5」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/scheduler.ts:580`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/168`。

### `server/orchestrator/scheduler.ts::Scheduler._smartRank.&lt;arrow@669:16&gt;`

在调用形式「a.entry.createdAt.localeCompare」中提供第 1 个实参「b.entry.createdAt」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 条件「(b.score !== a.score)」的捕获提前退出分支为「return：b.score - a.score」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return b.score - a.score;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「ea77527db0c94bb376228eb1」先于语句位置「1」的操作「f8e8192f481b5ca35673af49」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/scheduler.ts:669`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/169`。

### `server/orchestrator/scheduler.ts::Scheduler._smartRank.&lt;arrow@675:22&gt;`

构造捕获记录，字段按源码次序为「mode ← "smart"；selectedAt ← selectedAt；rank ← index + 1；score ← score；reasons ← reasons；retryStrategy ← typeof retryEvidence.retryStrategy === "string" ? retryEvidence.retryStrategy : null；failureFingerprint ← typeof retryEvidence.failureFingerprint === "string" ? retryEvidence.failureFingerprint : null；failureClass ← typeof retryEvidence.failureClass === "string" ? retryEvidence.failureClass : null」。不据构造形式推断物理持久化。 包含赋值/更新「entry.metadata = {\n        ...(entry.metadata || {}),\n        schedulerDecision: {\n          mode: "smart",\n          selectedAt,\n          rank: index + 1,\n          score,\n          reasons,\n          retryStrategy: typeof retryEvidence.retryStrategy === "string" ? retryEvidence.retryStrategy : null,\n          failureFingerprint: typeof retryEvide…［展示截断；完整操作保留］」，捕获目标为「entry.metadata」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「retryEvidence」的初始化来源为「entry.metadata?.sourceContext?.retry || {}」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return entry;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「selectedAt」关联路径「selectedAt」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「(entry.metadata || {})」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「a1379fcfe80c5c3deb751054」先于语句位置「1」的操作「4cceef46a078e40afce90654」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/scheduler.ts:675`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/170`。

### `server/orchestrator/scheduler.ts::Scheduler.#resolveProjectLimits`

构造捕获记录，字段按源码次序为「maxActivePerProject ← maxActivePerProject；getProjectFn ← this.getProjectFn」。不据构造形式推断物理持久化。 将「{\n      maxActivePerProject,\n      getProjectFn: this.getProjectFn,\n    }」作为第 3 个实参交给已绑定接口「ts:server/services/infra#resolveProjectConcurrencyLimits」，对应捕获形参「{\n  maxActivePerProject = DEFAULT_MAX_ACTIVE_PER_PROJECT,\n  getProjectFn = null,\n}: ResolveProjectConcurrencyOptions = {}」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「projectIds」的初始化来源为「[...new Set(entries.map((entry) =&gt; entry.projectId).filter(Boolean))]」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return resolveProjectConcurrencyLimits(this.hubRoot, projectIds, {\n      maxActivePerProject,\n      getProjectFn: this.getProjectFn,\n    });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「maxActivePerProject」关联路径「maxActivePerProject」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「d48b0bb2f6f3face17c7186f」先于语句位置「1」的操作「59a271e554fa3ef0ecffffda」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/scheduler.ts:698`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/171`。

### `server/orchestrator/worker-supervisor.ts::WorkerSupervisor.constructor`

构造捕获记录，字段按源码次序为「env ← process.env；fallbackRoot ← this.cpbRoot」。不据构造形式推断物理持久化。 将「{\n      env: process.env,\n      fallbackRoot: this.cpbRoot,\n    }」作为第 1 个实参交给已绑定接口「ts:server/services/executor-root#resolveExecutorRoot」，对应捕获形参「{ env = process.env, fallbackRoot = process.cwd() }: LooseRecord = {}」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「this._processSystem = processSystem as ProcessTreeSystem | undefined」，捕获目标为「this._processSystem」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 以字段投影形式「this.cpbRoot」关联路径「this.cpbRoot」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「ac281356695b33236c653dab」先于语句位置「1」的操作「e0b03cdee8c61b67a8414ede」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/worker-supervisor.ts:36`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/172`。

### `server/orchestrator/worker-supervisor.ts::WorkerSupervisor.ensureWorkerFor`

在调用形式「this.startWorker」中提供第 1 个实参「assignment」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 条件「(worker &amp;&amp; worker.status === "ready")」的捕获提前退出分支为「return：worker」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return worker;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「69b818dd882e4b32cf193e6e」先于语句位置「1」的操作「44deb8f216f3ce6c30f5aa78」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/orchestrator/worker-supervisor.ts:51`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/173`。

### `server/orchestrator/worker-supervisor.ts::WorkerSupervisor.startWorker`

构造捕获记录，字段按源码次序为「projectId ← assignment.projectId；pid ← null；status ← "starting"；executorRoot ← executorRoot；restartCount ← restartCount；incarnationToken ← incarnationToken；brokerTokenHash ← brokerTokenHash」。不据构造形式推断物理持久化。 将「{ cpbRoot: this.cpbRoot, executorRoot }」作为第 2 个实参交给已绑定接口「ts:server/services/executor-root#executorEnv」，对应捕获形参「{ cpbRoot, executorRoot, extra }: LooseRecord = {}」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「executorRoot」的初始化来源为「this.executorRoot」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「worker」存在源更新「worker = persisted」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!Number.isInteger(childPid) || Number(childPid) &lt;= 0)」的捕获提前退出分支为「throw：Object.assign(new Error("spawned worker did not expose a valid pid"), { code: "WORKER_PID_UNAVAILABLE" })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw Object.assign(new Error("spawned worker did not expose a valid pid"), { code: "WORKER_PID_UNAVAILABLE" });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「assignment.projectId」关联路径「assignment.projectId」；只描述捕获来源，不证明当时的字段值。

源码：`server/orchestrator/worker-supervisor.ts:58`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/174`。

### `server/services/acp/acp-client.ts::childEnvWithoutControlPlaneAuditPath`

具有捕获记录构造「{ ...env }」；该记录的可枚举字段为空或保留开放形状，未把展开来源补成确定字段。 捕获 binding「childEnv」的初始化来源为「{ ...env }」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return childEnv;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留记录复制/展开来源「env」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「04aabe4d32ca2e6189a02444」先于语句位置「4」的操作「3061ac8117a66e6d086be1bf」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/acp/acp-client.ts:308`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/175`。

### `server/services/acp/acp-client.ts::AcpClient.start`

构造捕获记录，字段按源码次序为「codexSandboxMode ← this.agent === "codex" ? codexConfiguredSandboxModeForExecution(env) : null；effectiveSandboxMode ← this.agent === "codex" ? codexSandboxModeForExecution(env) : null；sandboxEnforcement ← this.agent === "codex" ? codexSandboxEnforcementForExecution(env) : "cpb-outer"；codexApprovalPolicy ← this.agent === "codex" ? "never" : null；outerSandboxMode ← launch.sandbox?.mode || null；outerSandboxProvider ← launch.sandbox?.provider || null；outerWorkspaceWritable ← outerWriteRoots.some((root) =&gt; pathIsWithin(this.cwd, root))；outerWriteRootCount ← outerWriteRoots.length」。不据构造形式推断物理持久化。 将「{\n      agent: this.agent,\n      allowKeys: [\n        "CPB_CAPSULE_CODEX_PATH",\n        "CPB_CAPSULE_CLAUDE_CODE_EXECUTABLE",\n        ...capsuleKeys,\n      ],\n    }」作为第 3 个实参交给已绑定接口「ts:core/policy/child-env#buildChildEnv」，对应捕获形参「options: ChildEnvOptions = {}」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「env.CODEX_CONFIG = codexPolicy.CODEX_CONFIG」，捕获目标为「env.CODEX_CONFIG」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「codexPolicy」的初始化来源为「codexAcpEnvPolicy(env)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「nativeCapsule」存在源更新「nativeCapsule = { env: native.env, targetEnv: native.targetEnv }」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(this.child &amp;&amp; this.initialized &amp;&amp; !this.isUsable())」的捕获提前退出分支为「throw：new Error("ACP agent transport is not reusable because stdin is closed")」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return this.initialized;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 将「{ env, cwd: this.cwd }」作为第 3 个实参交给已绑定接口「ts:core/policy/agent-sandbox#buildAgentSandboxLaunch」，对应捕获形参「options: BuildAgentSandboxOptions = {}」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/acp/acp-client.ts:1646`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/176`。

### `server/services/acp/acp-client.ts::AcpClient.start.&lt;object@1749:43&gt;.&lt;object@1758:23&gt;.&lt;arrow@1765:53&gt;`

将「this.cwd」作为第 1 个实参交给已绑定接口「ts:server/services/acp/acp-client#pathIsWithin」，对应捕获形参「candidatePath: string」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/acp/acp-client.ts:1765`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/177`。

### `server/services/acp/acp-client.ts::AcpClient.start.&lt;arrow@1795:28&gt;`

在调用形式「this.errorSink」中提供第 1 个实参「chunk」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 包含赋值/更新「this.stderrTail = `${this.stderrTail}${chunk.toString()}`.slice(-ACP_STDERR_TAIL_LIMIT)」，捕获目标为「this.stderrTail」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「665d484c4b5f20f66dec7caa」先于语句位置「1」的操作「884fc81a75a1677428d3767a」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/acp/acp-client.ts:1795`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/178`。

### `server/services/acp/acp-client.ts::AcpClient.start.&lt;arrow@1801:22&gt;`

在调用形式「this.rejectAll」中提供第 1 个实参「error」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 包含赋值/更新「this.childSpawnError = error」，捕获目标为「this.childSpawnError」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「27dd105880c2a177ce29e68d」先于语句位置「1」的操作「8bd02bd29226facfdd9a7d16」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/acp/acp-client.ts:1801`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/179`。

### `server/services/acp/acp-client.ts::AcpClient.start.&lt;arrow@1806:28&gt;`

在调用形式「this.rejectAll」中提供第 1 个实参「error」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`server/services/acp/acp-client.ts:1806`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/180`。

### `server/services/acp/acp-client.ts::AcpClient.start.&lt;arrow@1810:21&gt;`

在调用形式「this.rejectAll」中提供第 1 个实参「this.startupExitFailure()」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 包含赋值/更新「this.childExitCode = code」，捕获目标为「this.childExitCode」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「4376a9b398f9a1a4d60a0823」先于语句位置「1」的操作「8e8415f547019566c66d25b9」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/acp/acp-client.ts:1810`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/181`。

### `server/services/acp/acp-client.ts::AcpClient.start.&lt;arrow@1824:22&gt;`

包含赋值/更新「this.childExitCode = code」，捕获目标为「this.childExitCode」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「045ed83a3aba92e71b1e24d4」先于语句位置「1」的操作「6b0230c8b9daf16409d0b21d」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/acp/acp-client.ts:1824`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/182`。

### `server/services/acp/acp-client.ts::AcpClient.start.&lt;arrow@1839:18&gt;`

在调用形式「this.lineQueue.then」中提供第 1 个实参「() =&gt; this.handleLine(line)」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 包含赋值/更新「this.lineQueue = this.lineQueue.then(() =&gt; this.handleLine(line))」，捕获目标为「this.lineQueue」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「6051f097d31f9ccc1d6752a2」先于语句位置「1」的操作「a5ff5650f3d693e328af83e4」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/acp/acp-client.ts:1839`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/183`。

### `server/services/acp/acp-client.ts::AcpClient.start.&lt;arrow@1839:18&gt;.&lt;arrow@1841:43&gt;`

在调用形式「this.handleLine」中提供第 1 个实参「line」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`server/services/acp/acp-client.ts:1841`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/184`。

### `server/services/acp/acp-client.ts::AcpClient.createTerminal`

构造捕获记录，字段按源码次序为「child ← child；identity ← identity；teardown ← null；cwd ← terminalCwd；detached ← detached；output ← bufferedOutput；truncated ← bufferedTruncated；outputByteLimit ← outputByteLimit；exitStatus ← bufferedExitStatus；exitAudit ← null；waiters ← []」。不据构造形式推断物理持久化。 将「{ agent: this.agent }」作为第 3 个实参交给已绑定接口「ts:core/policy/child-env#buildChildEnv」，对应捕获形参「options: ChildEnvOptions = {}」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「this.nextTerminalId++」，捕获目标为「this.nextTerminalId」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「classification」的初始化来源为「permResult.classification || "deny"」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「terminal」存在源更新「terminal = {\n      child,\n      identity,\n      teardown: null,\n      cwd: terminalCwd,\n      detached,\n      output: bufferedOutput,\n      truncated: bufferedTruncated,\n      outputByteLimit,\n      exitStatus: bufferedExitStatus,\n      exitAudit: null,\n      waiters: [],\n    }」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(this.terminalPolicy === "deny")」的捕获提前退出分支为「throw：new Error("terminal access denied for this phase")」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new Error("terminal access denied for this phase");」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 将「{ env, cwd: terminalCwd }」作为第 3 个实参交给已绑定接口「ts:core/policy/agent-sandbox#buildAgentSandboxLaunch」，对应捕获形参「options: BuildAgentSandboxOptions = {}」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/acp/acp-client.ts:2760`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/185`。

### `server/services/acp/acp-client.ts::AcpClient.createTerminal.append`

在调用形式「Buffer.byteLength」中提供第 1 个实参「terminal.output」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 包含赋值/更新「terminal.output += text」，捕获目标为「terminal.output」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「text」的初始化来源为「chunk.toString("utf8")」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「bufferedOutput」存在源更新「bufferedOutput += text」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(terminal)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「50abdcb0caa3a82a67a9a47d」先于语句位置「1」的操作「a7c4b215ef5c86bd215d64c9」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/acp/acp-client.ts:2860`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/186`。

### `server/services/acp/acp-client.ts::AcpClient.createTerminal.recordTerminalExit`

构造捕获记录，字段按源码次序为「terminalId ← terminalId；cwd ← terminalCwd；exitCode ← exitCode；signal ← signal；outputTail ← String(redactSecrets(terminal.output) || "").slice(-ACP_TERMINAL_AUDIT_TAIL_LIMIT)；truncated ← terminal.truncated」。不据构造形式推断物理持久化。 将「terminal.output」作为第 1 个实参交给已绑定接口「ts:server/services/secret-policy#redactSecrets」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「terminal.exitStatus = status」，捕获目标为「terminal.exitStatus」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「status」的初始化来源为「{ exitCode, signal }」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「bufferedExitStatus」存在源更新「bufferedExitStatus = status」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!terminal)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`server/services/acp/acp-client.ts:2877`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/187`。

### `server/services/acp/acp-client.ts::AcpClient.createTerminal.recordTerminalExit.&lt;arrow@2891:36&gt;`

在调用形式「String」中提供第 1 个实参「error」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`server/services/acp/acp-client.ts:2891`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/188`。

### `server/services/acp/acp-client.ts::AcpClient.createTerminal.recordTerminalExit.&lt;arrow@2898:35&gt;`

在调用形式「resolve」中提供第 1 个实参「terminal!.exitStatus!」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 包含赋值/更新「terminal!.waiters = []」，捕获目标为「terminal.waiters」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「16560da7c335fb65bb2276b1」先于语句位置「1」的操作「d14fce11fbea9c1d88ec17f5」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/acp/acp-client.ts:2898`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/189`。

### `server/services/agent/agent-config.ts::resolveAgentsForEntry`

构造捕获记录，字段按源码次序为「agents ← Object.keys(merged).length &gt; 0 ? merged : undefined；agent ← metadataRecord.agent || undefined」。不据构造形式推断物理持久化。 将「hubRoot」作为第 1 个实参交给已绑定接口「ts:server/services/agent/agent-config#readHubConfig」，对应捕获形参「hubRoot: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「metadataRecord」的初始化来源为「metadata」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(Object.keys(merged).length === 0 &amp;&amp; !metadataRecord.agent)」的捕获提前退出分支为「return：metadata」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return metadata;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留记录复制/展开来源「metadata」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「72361022bd4cc6ae3c6b4167」先于语句位置「1」的操作「b9a5fedba5a0f91cb161c710」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/agent/agent-config.ts:471`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/190`。

### `server/services/audit/hub-access-audit.ts::openHubAccessAudit`

构造捕获记录，字段按源码次序为「recursive ← true；mode ← 0o700」。不据构造形式推断物理持久化。 将「options.maxBytes」作为第 1 个实参交给已绑定接口「ts:server/services/audit/hub-access-audit#normalizeMaxBytes」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「maxBytes」的初始化来源为「normalizeMaxBytes(options.maxBytes)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!directoryInfo.isDirectory() || directoryInfo.isSymbolicLink())」的捕获提前退出分支为「throw：new Error(`Hub access-audit directory must be a real directory: ${paths.directory}`)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new Error(`Hub access-audit directory must be a real directory: ${paths.directory}`);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「options.hubRoot」关联路径「options.hubRoot」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「af1abf4c24e23a5d53af44c4」先于语句位置「1」的操作「4eefbbee35a335394bdae027」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/audit/hub-access-audit.ts:530`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/191`。

### `server/services/audit/hub-access-audit.ts::openHubAccessAudit.&lt;object@554:9&gt;.append`

在调用形式「queue.then」中提供第 1 个实参「async () =&gt; {\n        if (closed) throw new Error("Hub access-audit writer is closed");\n        if (fatal) throw fatal;\n        const record = createRecord(input, state);\n        validateAuditRecord(record, state.lastSequence + 1, state.lastHash);\n        try {\n          await appendRecordLine(state, record);\n          return record;\n        } catch …［展示截断；完整操作保留］」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「operation」的初始化来源为「queue.then(async () =&gt; {\n        if (closed) throw new Error("Hub access-audit writer is closed");\n        if (fatal) throw fatal;\n        const record = createRecord(input, state);\n        validateAuditRecord(record, state.lastSequence + 1, state.lastHash);\n        try {\n          await appendRecordLine(state, record);\n          return record;\n     …［展示截断；完整操作保留］」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「queue」存在源更新「queue = operation.then(() =&gt; undefined, () =&gt; undefined)」；循环和分支条件见操作上下文，未推执行次数或最终数值。 以「return operation;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「0c223799d638bd914de66ce6」先于语句位置「1」的操作「4370fb920452bcb672d304b9」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/audit/hub-access-audit.ts:556`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/192`。

### `server/services/audit/hub-access-audit.ts::openHubAccessAudit.&lt;object@554:9&gt;.append.&lt;arrow@557:35&gt;`

将「input」作为第 1 个实参交给已绑定接口「ts:server/services/audit/hub-access-audit#createRecord」，对应捕获形参「input: HubAccessAuditInput」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「record」的初始化来源为「createRecord(input, state)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「fatal」存在源更新「fatal = error」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(closed)」的捕获提前退出分支为「throw：new Error("Hub access-audit writer is closed")」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new Error("Hub access-audit writer is closed");」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「a9e822e6fbda349184948df5」先于语句位置「1」的操作「e66517689afc7b01ceedb661」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/audit/hub-access-audit.ts:557`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/193`。

### `server/services/audit/hub-access-audit.ts::openHubAccessAudit.&lt;object@554:9&gt;.status`

构造捕获记录，字段按源码次序为「filePath ← state.filePath；recordCount ← state.recordCount；lastSequence ← state.lastSequence；lastHash ← state.lastHash；sizeBytes ← state.sizeBytes；maxBytes ← state.maxBytes；healthy ← fatal === null」。不据构造形式推断物理持久化。 以「return {\n        filePath: state.filePath,\n        recordCount: state.recordCount,\n        lastSequence: state.lastSequence,\n        lastHash: state.lastHash,\n        sizeBytes: state.sizeBytes,\n        maxBytes: state.maxBytes,\n        healthy: fatal === null,\n      };」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「state.filePath」关联路径「state.filePath」；只描述捕获来源，不证明当时的字段值。

源码：`server/services/audit/hub-access-audit.ts:573`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/194`。

### `server/services/audit/hub-access-audit.ts::openHubAccessAudit.&lt;object@554:9&gt;.close`

对捕获 binding「closed」存在源更新「closed = true」；循环和分支条件见操作上下文，未推执行次数或最终数值。

源码：`server/services/audit/hub-access-audit.ts:584`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/195`。

### `server/services/auto-finalizer.ts::runGit`

构造捕获记录，字段按源码次序为「code ← "GIT_COMMAND_FAILED"；stdout ← result.stdout；stderr ← result.stderr；committed ← null」。不据构造形式推断物理持久化。 将「err」作为第 1 个实参交给已绑定接口「ts:server/services/auto-finalizer#commandErrorDetails」，对应捕获形参「err: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「details」的初始化来源为「commandErrorDetails(err)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(explicitFailure)」的捕获提前退出分支为「throw：Object.assign(new Error(String(result.stderr || `git ${args[0] || "command"} failed`)), {\n        code: "GIT_COMMAND_FAILED",\n        stdout: result.stdout,\n        stderr: result.stderr,\n        committed: null,\n      })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw Object.assign(new Error(String(result.stderr || `git ${args[0] || "command"} failed`)), {\n        code: "GIT_COMMAND_FAILED",\n        stdout: result.stdout,\n        stderr: result.stderr,\n        committed: null,\n      });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「cwd」关联路径「cwd」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「(env ? { env } : {})」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。

源码：`server/services/auto-finalizer.ts:332`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/196`。

### `server/services/auto-finalizer.ts::runGit.&lt;block@337:6&gt;.&lt;arrow@344:56&gt;`

在调用形式「Object.prototype.hasOwnProperty.call」中提供第 1 个实参「result」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「status」的初始化来源为「result[field]」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!Object.prototype.hasOwnProperty.call(result, field))」的捕获提前退出分支为「return：false」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return false;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「abe550b223627c455d1d71a4」先于语句位置「1」的操作「39424693d7ec9297f11e3d21」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/auto-finalizer.ts:344`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/197`。

### `server/services/auto-finalizer.ts::finalizeAsReviewBundle`

构造捕获记录，字段按源码次序为「ok ← true；status ← "review_bundle"；mode ← "review_bundle"；jobId ← jobId；bundlePath ← bundlePath；bundleSha256 ← bundleSha256；bundleBytes ← bundleBytes；committed ← true；eventRecorded ← true；audit ← {\n        eventType: "review_bundle_created",\n        jobId: stableJobId,\n        project: stableProject,\n        bundlePath,\n      }；changedFiles ← evidence.changedFiles；verdict ← verdict.verdict || null」。不据构造形式推断物理持久化。 将「{\n        type: "review_bundle_created",\n        jobId: stableJobId,\n        project: stableProject,\n        bundlePath,\n        bundleSha256,\n        bundleBytes,\n        changedFiles: evidence.changedFiles,\n        verdict: verdict.verdict || null,\n        ts: new Date().toISOString(),\n      }」作为第 4 个实参交给已绑定接口「ts:server/services/event/event-store#appendEvent」，对应捕获形参「event: EventRecord」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「details」的初始化来源为「finalizerRecord(err)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「bundleSha256」存在源更新「bundleSha256 = createHash("sha256").update(serialized, "utf8").digest("hex")」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!recorded)」的捕获提前退出分支为「throw：new Error("review_bundle_created event was not persisted")」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return blocked("MUTATION_LEASE_REQUIRED", {\n      mode: "review_bundle",\n      jobId: stableJobId || jobId || null,\n      committed: false,\n      eventRecorded: false,\n      retryable: false,\n    });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「stableJobId」关联路径「stableJobId」；只描述捕获来源，不证明当时的字段值。 将「bundlePath」作为第 1 个实参交给已绑定接口「ts:shared/hub-maintenance#writeJsonDurableAtomic」，对应捕获形参「filePath: string」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/auto-finalizer.ts:1273`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/198`。

### `server/services/auto-finalizer.ts::finalizeAsReviewBundle.assertReviewBundleMutationLease`

构造捕获记录，字段按源码次序为「operation ← "review_bundle.publish"；phase ← "before-write"；mode ← "review_bundle"；project ← stableProject；entryId ← stableEntryId；originJobId ← stableJobId；jobId ← stableJobId；finalizationId ← null；generation ← null；repository ← null；issueNumber ← null；commit ← null」；其余字段见完整操作。不据构造形式推断物理持久化。 在调用形式「assertMutationLease」中提供第 1 个实参「{\n      operation: "review_bundle.publish",\n      phase: "before-write",\n      mode: "review_bundle",\n      project: stableProject,\n      entryId: stableEntryId,\n      originJobId: stableJobId,\n      jobId: stableJobId,\n      finalizationId: null,\n      generation: null,\n      repository: null,\n      issueNumber: null,\n      commit: null,\n      …［展示截断；完整操作保留］」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「allowed」的初始化来源为「await assertMutationLease({\n      operation: "review_bundle.publish",\n      phase: "before-write",\n      mode: "review_bundle",\n      project: stableProject,\n      entryId: stableEntryId,\n      originJobId: stableJobId,\n      jobId: stableJobId,\n      finalizationId: null,\n      generation: null,\n      repository: null,\n      issueNumber: null,\n …［展示截断；完整操作保留］」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(allowed === false)」的捕获提前退出分支为「throw：Object.assign(new Error("review bundle mutation lease was rejected"), {\n        code: "MUTATION_LEASE_LOST",\n        committed: false,\n        retryable: true,\n      })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw Object.assign(new Error("review bundle mutation lease was rejected"), {\n        code: "MUTATION_LEASE_LOST",\n        committed: false,\n        retryable: true,\n      });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「target」关联路径「target」；只描述捕获来源，不证明当时的字段值。

源码：`server/services/auto-finalizer.ts:1305`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/199`。

### `server/services/auto-finalizer.ts::finalizeSuccessfulQueueEntry`

构造捕获记录，字段按源码次序为「job ← prJob；verdict ← prVerdict.verdict；branchPushed ← false；dryRun ← dryRun；allowLive ← liveAllowed；createPullRequest ← createPullRequest；runCommand ← runCommand；pushToken ← pushToken；agents ← agents；routingContext ← buildRoutingContext(entry, job, routeGuard)；verdictDetail ← prVerdictDetail || evidenceVerdictDetail；completionGate ← prVerdict.completionGate || null」。不据构造形式推断物理持久化。 将「{\n          ...prOptions,\n          dryRun: true,\n          allowLive: false,\n          createPullRequest: undefined,\n        }」作为第 1 个实参交给已绑定接口「ts:server/services/github/github-issues#openDraftPullRequest」，对应捕获形参「{\n  job,\n  verdict,\n  branchPushed = false,\n  dryRun = true,\n  allowLive = false,\n  createPullRequest,\n  runCommand,\n  pushToken = null,\n  agents = {},\n  routingContext = null,\n  artifacts = {},\n  tests = [],\n  audit = {},\n  verdictDetail = null,\n  completionGate = null,\n  remoteCapability = null,\n  remoteAuthorityValidator = null,\n  remote…［展示截断；完整操作保留］」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「finalizationId」的初始化来源为「journalSnapshot.record!.finalizationId」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「pushed」存在源更新「pushed = pushVerification.committed」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(preview.status !== "dry-run" || !prPlan.repo || !prPlan.head || !prPlan.base\n          || typeof prPlan.title !== "string" || !prPlan.title || prPlan.title.length &gt; 256\n          || typeof prPlan.body !== "string" || prPlan.body.length &gt; 65_536\n          || prPlan.body.includes("\u0000") || prPlan.draft !== true)」的捕获提前退出分支为「throw：Object.assign(new Error("PR recovery plan could not be frozen before finalization"), {\n            code: "PR_CREATE_PLAN_MISSING",\n            committed: false,\n          })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return recordAndReturn(skipped("JOB_NOT_COMPLETED", { jobId }));」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「jobId」关联路径「jobId」；只描述捕获来源，不证明当时的字段值。 将「{\n        worktree: canonicalWorktreePath,\n        repository: remoteCapability.repository,\n        commit,\n        expectedTree: auditedTree,\n        expectedRemoteHead: sourceHead,\n        targetBranch: sourceBranch,\n        token: pushToken,\n        runCommand,\n        authorize: () =&gt; remoteAuthorityValidator(pushAuthorityRequest),\n        veri…［展示截断；完整操作保留］」作为第 1 个实参交给已绑定接口「ts:server/services/github/github-issues#pushGithubCommitWithControlledTransport」，对应捕获形参「{\n  worktree,\n  repository,\n  commit,\n  expectedTree,\n  expectedRemoteHead,\n  targetBranch,\n  token = null,\n  env = process.env,\n  runCommand = execFileAsync,\n  authorize = null,\n  verify = null,\n  beforeAttempt = null,\n  afterCommitted = null,\n}: {\n  worktree: string;\n  repository: string;\n  commit: string;\n  expectedTree: string;\n  expec…［展示截断；完整操作保留］」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/auto-finalizer.ts:1425`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/200`。

### `server/services/auto-finalizer.ts::finalizeSuccessfulQueueEntry.recordAndReturn`

构造捕获记录，字段按源码次序为「jobId ← jobId；mode ← mode；committed ← result.committed ?? null；pushed ← result.pushed ?? null；closed ← result.closed ?? null；prUrl ← result.prUrl ?? null；prNumber ← result.prNumber ?? null；remoteWrites ← result.remoteWrites ?? null；remoteIntent ← result.remoteIntent ?? null；principal ← result.principal ?? null；commit ← result.commit ?? null；tree ← result.tree ?? null」；其余字段见完整操作。不据构造形式推断物理持久化。 将「{\n          jobId,\n          mode,\n          committed: result.committed ?? null,\n          pushed: result.pushed ?? null,\n          closed: result.closed ?? null,\n          prUrl: result.prUrl ?? null,\n          prNumber: result.prNumber ?? null,\n          remoteWrites: result.remoteWrites ?? null,\n          remoteIntent: result.remoteIntent ?? nul…［展示截断；完整操作保留］」作为第 2 个实参交给已绑定接口「ts:server/services/auto-finalizer#blocked」，对应捕获形参「details: FinalizerRecord = {}」。该普通调用关系不替代进程或网络协议关系。 条件「(cpbRoot &amp;&amp; projectId &amp;&amp; jobId &amp;&amp; jobId !== "unknown")」的捕获提前退出分支为「return：blocked("FINALIZER_AUDIT_RECORD_FAILED", {\n          jobId,\n          mode,\n          committed: result.committed ?? null,\n          pushed: result.pushed ?? null,\n          closed: result.closed ?? null,\n          prUrl: result.prUrl ?? null,\n          prNumber: result.prNumber ?? null,\n          remoteWrites: result.remoteWrites ?? null,\n         …［展示截断；完整操作保留］」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return blocked("FINALIZER_AUDIT_RECORD_FAILED", {\n          jobId,\n          mode,\n          committed: result.committed ?? null,\n          pushed: result.pushed ?? null,\n          closed: result.closed ?? null,\n          prUrl: result.prUrl ?? null,\n          prNumber: result.prNumber ?? null,\n          remoteWrites: result.remoteWrites ?? null,\n  …［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「result」关联路径「result」；只描述捕获来源，不证明当时的字段值。

源码：`server/services/auto-finalizer.ts:1454`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/201`。

### `server/services/auto-finalizer.ts::finalizeSuccessfulQueueEntry.&lt;arrow@1646:6&gt;`

构造捕获记录，字段按源码次序为「runCommand ← runCommand as GithubRemoteRunCommand；principal ← transportPrincipal || undefined」。不据构造形式推断物理持久化。 将「{\n              runCommand: runCommand as GithubRemoteRunCommand,\n              principal: transportPrincipal || undefined,\n            }」作为第 2 个实参交给已绑定接口「ts:server/services/github/github-remote-capability#assertGithubRemoteWriteAuthorized」，对应捕获形参「{\n    runCommand = execFileAsync as GithubRemoteRunCommand,\n    principal: rawPrincipal = null,\n  }: { runCommand?: GithubRemoteRunCommand; principal?: GithubTransportPrincipal | LooseRecord | null } = {}」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「pushRemote」的初始化来源为「mode === "pr" &amp;&amp; pushToken\n            ? `https://github.com/${remoteCapability.repository}.git`\n            : mode === "pr" ? "origin" : remote」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!transportPrincipal || !observedPrincipal\n          || finalizerJournalDigest(observedPrincipal) !== finalizerJournalDigest(transportPrincipal))」的捕获提前退出分支为「throw：Object.assign(new Error("GitHub authority principal does not match the bound transport"), {\n            code: "GITHUB_TRANSPORT_PRINCIPAL_MISMATCH",\n            committed: false,\n          })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw Object.assign(new Error("GitHub authority principal does not match the bound transport"), {\n            code: "GITHUB_TRANSPORT_PRINCIPAL_MISMATCH",\n            committed: false,\n          });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「runCommand as GithubRemoteRunCommand」关联路径「runCommand」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「0a1c8a2c15cb01e6e7a61db3」先于语句位置「1」的操作「d54be2d75336d84c8fc57801」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/auto-finalizer.ts:1646`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/202`。

### `server/services/auto-finalizer.ts::finalizeSuccessfulQueueEntry.&lt;arrow@1676:6&gt;`

构造捕获记录，字段按源码次序为「operation ← trustedRequest.operation；committed ← null；reason ← "GitHub verifier principal does not match the bound transport"」。不据构造形式推断物理持久化。 将「{\n              runCommand: runCommand as GithubRemoteRunCommand,\n              principal: transportPrincipal || undefined,\n            }」作为第 2 个实参交给已绑定接口「ts:server/services/github/github-remote-capability#verifyGithubRemoteWriteCommitted」，对应捕获形参「{\n    runCommand = execFileAsync as GithubRemoteRunCommand,\n    principal: rawPrincipal = null,\n  }: { runCommand?: GithubRemoteRunCommand; principal?: GithubTransportPrincipal | LooseRecord | null } = {}」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「trustedRequest」的初始化来源为「immutableRemoteAuthorityRequest(request)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!transportPrincipal || !observedPrincipal\n          || finalizerJournalDigest(observedPrincipal) !== finalizerJournalDigest(transportPrincipal))」的捕获提前退出分支为「return：{\n            operation: trustedRequest.operation,\n            committed: null,\n            reason: "GitHub verifier principal does not match the bound transport",\n          }」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return {\n            operation: trustedRequest.operation,\n            committed: null,\n            reason: "GitHub verifier principal does not match the bound transport",\n          };」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「runCommand as GithubRemoteRunCommand」关联路径「runCommand」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「80db040df23a4fae35bffa7e」先于语句位置「1」的操作「59ff576cb4e2dbd23a5bafec」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/auto-finalizer.ts:1676`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/203`。

### `server/services/auto-finalizer.ts::finalizeSuccessfulQueueEntry.assertLiveMutationLease`

构造捕获记录，字段按源码次序为「operation ← operation；phase ← "before-write"；mode ← mode；project ← projectId；entryId ← stableEntryId；originJobId ← jobId；jobId ← jobId；finalizationId ← intent?.finalizationId || null；generation ← intent?.generation || null；repository ← remoteCapability?.repository || null；issueNumber ← remoteCapability?.issueNumber || null；commit ← commitIdentity」；其余字段见完整操作。不据构造形式推断物理持久化。 在调用形式「assertMutationLease」中提供第 1 个实参「{\n      operation,\n      phase: "before-write",\n      mode,\n      project: projectId,\n      entryId: stableEntryId,\n      originJobId: jobId,\n      jobId,\n      finalizationId: intent?.finalizationId || null,\n      generation: intent?.generation || null,\n      repository: remoteCapability?.repository || null,\n      issueNumber: remoteCapability?.i…［展示截断；完整操作保留］」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「allowed」的初始化来源为「await assertMutationLease({\n      operation,\n      phase: "before-write",\n      mode,\n      project: projectId,\n      entryId: stableEntryId,\n      originJobId: jobId,\n      jobId,\n      finalizationId: intent?.finalizationId || null,\n      generation: intent?.generation || null,\n      repository: remoteCapability?.repository || null,\n      issueN…［展示截断；完整操作保留］」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(allowed === false)」的捕获提前退出分支为「throw：Object.assign(new Error("finalizer mutation lease was rejected"), {\n        code: "MUTATION_LEASE_LOST",\n        committed: false,\n        retryable: true,\n      })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「operation」关联路径「operation」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「bdb7de523460e9b2de3b34e2」先于语句位置「1」的操作「2a43c0e9aca02a45646efa99」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

条件「(!liveMutationMode || !assertMutationLease)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。

源码：`server/services/auto-finalizer.ts:1959`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/204`。

### `server/services/auto-finalizer.ts::finalizeSuccessfulQueueEntry.initializeLiveJournal`

构造捕获记录，字段按源码次序为「project ← projectId；entryId ← stableEntryId；originJobId ← jobId；mode ← mode as "remote" | "pr"；repository ← remoteCapability.repository；issueNumber ← remoteCapability.issueNumber；capabilityDigest ← finalizerCapabilityDigest(remoteCapability)；principal ← transportPrincipal；source ← { branch: sourceBranch, head: sourceHead.toLowerCase() }；commit ← commitIdentity.toLowerCase()；tree ← auditedTree.toLowerCase()；preRemoteHead ← preRemoteHead?.toLowerCase() || null」；其余字段见完整操作。不据构造形式推断物理持久化。 将「commitIdentity」作为第 2 个实参交给已绑定接口「ts:server/services/auto-finalizer#finalizeSuccessfulQueueEntry.assertLiveMutationLease」，对应捕获形参「commitIdentity: string | null」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「initial」的初始化来源为「{\n        schema: FINALIZER_MUTATION_RECEIPT_SCHEMA,\n        finalizationId,\n        generation: 1,\n        project: projectId,\n        entryId: stableEntryId,\n        originJobId: jobId,\n        mode: mode as "remote" | "pr",\n        stage: "claimed",\n        repository: remoteCapability.repository,\n        issueNumber: remoteCapability.issueNumbe…［展示截断；完整操作保留］」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「journalSnapshot」存在源更新「journalSnapshot = snapshot」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(snapshot.invalidReason)」的捕获提前退出分支为「throw：Object.assign(new Error(snapshot.invalidReason), {\n      code: "FINALIZER_JOURNAL_INVALID",\n      committed: null,\n    })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return null;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「targetBranch」关联路径「targetBranch」；只描述捕获来源，不证明当时的字段值。

源码：`server/services/auto-finalizer.ts:1990`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/205`。

### `server/services/auto-finalizer.ts::finalizeSuccessfulQueueEntry.advanceLiveJournal`

构造捕获记录，字段按源码次序为「dataRoot ← dataRoot；expected ← journalSnapshot；assertMutationLease ← assertMutationLease；leaseContext ← { mode, jobId }」。不据构造形式推断物理持久化。 将「{\n      dataRoot,\n      expected: journalSnapshot,\n      assertMutationLease,\n      leaseContext: { mode, jobId },\n    }」作为第 5 个实参交给已绑定接口「ts:server/services/finalizer-journal#appendFinalizerJournal」，对应捕获形参「{\n    dataRoot,\n    expected,\n    assertMutationLease,\n    leaseContext = {},\n  }: {\n    dataRoot?: string;\n    expected: FinalizerJournalSnapshot;\n    assertMutationLease: AssertJournalMutationLease;\n    leaseContext?: LooseRecord;\n  }」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「next」的初始化来源为「nextJournalRecord(journalSnapshot, stage, {\n      receipts: receiptUpdates,\n    })」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「journalSnapshot」存在源更新「journalSnapshot = observed」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!journalSnapshot || !cpbRoot || !projectId || !stableEntryId || !dataRoot || !assertMutationLease)」的捕获提前退出分支为「throw：Object.assign(new Error("finalizer journal is unavailable"), {\n        code: "FINALIZER_JOURNAL_REQUIRED",\n        committed: null,\n      })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw Object.assign(new Error("finalizer journal is unavailable"), {\n        code: "FINALIZER_JOURNAL_REQUIRED",\n        committed: null,\n      });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「receiptUpdates」关联路径「receiptUpdates」；只描述捕获来源，不证明当时的字段值。

源码：`server/services/auto-finalizer.ts:2164`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/206`。

### `server/services/auto-finalizer.ts::finalizeSuccessfulQueueEntry.&lt;block@2195:43&gt;.&lt;object@2319:29&gt;.&lt;arrow@2323:44&gt;`

构造捕获记录，字段按源码次序为「committed ← null」。不据构造形式推断物理持久化。 将「{ branchPushIntent }」作为第 2 个实参交给已绑定接口「ts:server/services/auto-finalizer#finalizeSuccessfulQueueEntry.advanceLiveJournal」，对应捕获形参「receiptUpdates: FinalizerRecord = {}」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「branchPushIntent.pullRequestPlan = finalizerRecord(journalSnapshot.record.receipts.prPlan)」，捕获目标为「branchPushIntent.pullRequestPlan」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「branchPushIntent」的初始化来源为「finalizerRecord(redactSecrets(request))」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(journalSnapshot?.record?.stage !== "claimed")」的捕获提前退出分支为「throw：Object.assign(new Error("PR branch push intent is already ambiguous"), { committed: null })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw Object.assign(new Error("PR branch push intent is already ambiguous"), { committed: null });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「branchPushIntent」关联路径「branchPushIntent」；只描述捕获来源，不证明当时的字段值。 将「worktreeHead」作为第 2 个实参交给已绑定接口「ts:server/services/auto-finalizer#finalizeSuccessfulQueueEntry.assertLiveMutationLease」，对应捕获形参「commitIdentity: string | null」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/auto-finalizer.ts:2323`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/207`。

### `server/services/auto-finalizer.ts::finalizeSuccessfulQueueEntry.&lt;block@2195:43&gt;.&lt;object@2319:29&gt;.&lt;arrow@2344:43&gt;`

构造捕获记录，字段按源码次序为「repository ← journalSnapshot?.record?.repository；issueNumber ← journalSnapshot?.record?.issueNumber；commit ← journalSnapshot?.record?.commit；headBranch ← createIntent.headBranch；baseBranch ← createIntent.baseBranch；title ← createIntent.title；body ← createIntent.body；draft ← createIntent.draft；authorLogin ← createIntent.authorLogin；authorId ← createIntent.authorId；prUrl ← prUrl；prNumber ← prNumber」；其余字段见完整操作。不据构造形式推断物理持久化。 将「{\n              branchPush: operationReceipt("pull_request.push", {\n                repository: journalSnapshot?.record?.repository,\n                issueNumber: journalSnapshot?.record?.issueNumber,\n                commit: journalSnapshot?.record?.commit,\n                tree: journalSnapshot?.record?.tree,\n                targetBranch: journalSnapsho…［展示截断；完整操作保留］」作为第 2 个实参交给已绑定接口「ts:server/services/auto-finalizer#finalizeSuccessfulQueueEntry.advanceLiveJournal」，对应捕获形参「receiptUpdates: FinalizerRecord = {}」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「prUrl」的初始化来源为「typeof details.prUrl === "string" ? details.prUrl : ""」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(operation === "pull_request.push")」的捕获提前退出分支为「throw：Object.assign(error instanceof Error ? error : new Error(String(error)), {\n              committed: true,\n              attempted: true,\n              operation: "pull_request.push",\n            })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw Object.assign(error instanceof Error ? error : new Error(String(error)), {\n              committed: true,\n              attempted: true,\n              operation: "pull_request.push",\n            });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「journalSnapshot?.record?.repository」关联路径「journalSnapshot.record.repository」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「8c5f1a78444ffd51ec76cebe」先于语句位置「1」的操作「9f88dd7f30457f0bf3d3d388」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/auto-finalizer.ts:2344`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/208`。

### `server/services/auto-finalizer.ts::finalizeSuccessfulQueueEntry.&lt;block@2644:35&gt;.&lt;object@2651:6&gt;.beforeUpdateRef`

将「worktreeHead」作为第 2 个实参交给已绑定接口「ts:server/services/auto-finalizer#finalizeSuccessfulQueueEntry.assertLiveMutationLease」，对应捕获形参「commitIdentity: string | null」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/auto-finalizer.ts:2654`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/209`。

### `server/services/auto-finalizer.ts::finalizeSuccessfulQueueEntry.&lt;block@2715:25&gt;.&lt;block@2739:8&gt;.&lt;object@2749:71&gt;.authorize`

在调用形式「remoteAuthorityValidator」中提供第 1 个实参「pushAuthorityRequest」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`server/services/auto-finalizer.ts:2758`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/210`。

### `server/services/auto-finalizer.ts::finalizeSuccessfulQueueEntry.&lt;block@2715:25&gt;.&lt;block@2739:8&gt;.&lt;object@2749:71&gt;.verify`

在调用形式「remoteCommitVerifier」中提供第 1 个实参「pushAuthorityRequest」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`server/services/auto-finalizer.ts:2759`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/211`。

### `server/services/auto-finalizer.ts::finalizeSuccessfulQueueEntry.&lt;block@2715:25&gt;.&lt;block@2739:8&gt;.&lt;object@2749:71&gt;.beforeAttempt`

构造捕获记录，字段按源码次序为「committed ← null；attempted ← false」。不据构造形式推断物理持久化。 将「commit」作为第 2 个实参交给已绑定接口「ts:server/services/auto-finalizer#finalizeSuccessfulQueueEntry.assertLiveMutationLease」，对应捕获形参「commitIdentity: string | null」。该普通调用关系不替代进程或网络协议关系。 对捕获 binding「operationAttempted」存在源更新「operationAttempted = true」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(journalSnapshot?.record?.stage !== "claimed")」的捕获提前退出分支为「throw：Object.assign(new Error("repository push intent is already ambiguous"), {\n              committed: null,\n              attempted: false,\n            })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw Object.assign(new Error("repository push intent is already ambiguous"), {\n              committed: null,\n              attempted: false,\n            });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「1」的操作「8f829c137f5f208a0b54aa96」先于语句位置「2」的操作「0e0464ed597cbc1cd8a85dd5」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「"repository.push.intent"」作为第 1 个实参交给已绑定接口「ts:server/services/auto-finalizer#finalizeSuccessfulQueueEntry.advanceLiveJournal」，对应捕获形参「stage: FinalizerJournalStage」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/auto-finalizer.ts:2760`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/212`。

### `server/services/auto-finalizer.ts::finalizeSuccessfulQueueEntry.&lt;block@2715:25&gt;.&lt;block@2739:8&gt;.&lt;object@2749:71&gt;.afterCommitted`

构造捕获记录，字段按源码次序为「repository ← journalSnapshot?.record?.repository；issueNumber ← journalSnapshot?.record?.issueNumber；commit ← journalSnapshot?.record?.commit；tree ← journalSnapshot?.record?.tree；targetBranch ← journalSnapshot?.record?.targetBranch；preRemoteHead ← journalSnapshot?.record?.preRemoteHead；verification ← redactFinalizerRemoteValue(verification, [pushToken])」。不据构造形式推断物理持久化。 将「{\n              push: operationReceipt("repository.push", {\n                repository: journalSnapshot?.record?.repository,\n                issueNumber: journalSnapshot?.record?.issueNumber,\n                commit: journalSnapshot?.record?.commit,\n                tree: journalSnapshot?.record?.tree,\n                targetBranch: journalSnapshot?.recor…［展示截断；完整操作保留］」作为第 2 个实参交给已绑定接口「ts:server/services/auto-finalizer#finalizeSuccessfulQueueEntry.advanceLiveJournal」，对应捕获形参「receiptUpdates: FinalizerRecord = {}」。该普通调用关系不替代进程或网络协议关系。 以「throw Object.assign(error instanceof Error ? error : new Error(String(error)), {\n              committed: true,\n              attempted: true,\n              operation: "repository.push",\n            });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「journalSnapshot?.record?.repository」关联路径「journalSnapshot.record.repository」；只描述捕获来源，不证明当时的字段值。

源码：`server/services/auto-finalizer.ts:2771`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/213`。

### `server/services/engine-runner.ts::buildServices`

构造捕获记录，字段按源码次序为「createJob ← buildCreateJobPort(broker, runtimeDataRoot)；startPhase ← broker ? broker.startPhase.bind(broker) : withJobOptions(startPhase)；completePhase ← broker ? broker.completePhase.bind(broker) : withJobOptions(completePhase)；completeJob ← broker\n      ? broker.completeJob.bind(broker)\n      : runtimeDataRoot\n      ? (root: string, project: string, jobId: string, opts: LooseRecord = {}) =&gt; comp…［展示截断；完整操作保留］；failJob ← broker ? broker.failJob.bind(broker) : withJobOptions(failJob)；blockJob ← broker ? broker.blockJob.bind(broker) : withJobOptions(blockJob)；appendEvent ← broker\n      ? broker.appendEvent.bind(broker)\n      : runtimeDataRoot\n      ? (root: string, project: string, jobId: string, event: EventRecord, opts: Loose…［展示截断；完整操作保留］；prepareTask ← prepareTaskForEnv(runtimeEnv)；getPool ← () =&gt; getManagedAcpPool({ cpbRoot, hubRoot, env: runtimeEnv })；getArtifactIndex ← broker\n      ? broker.getArtifactIndex.bind(broker)\n      : (root: string, project: string, jobId: string, opts: LooseRecord = {}) =&gt;\n        buildArtifactIn…［展示截断；完整操作保留］；providerServices ← {\n      assertProviderAvailable,\n      getProviderAdapter,\n      delegateMarkProviderUnavailable,\n      delegateEnqueueProviderUsage,\n      readAgentRoutin…［展示截断；完整操作保留］」。不据构造形式推断物理持久化。 将「env」作为第 1 个实参交给已绑定接口「ts:server/services/engine-runner#envRecord」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「runtimeEnv」的初始化来源为「envRecord(env)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return ports;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「assertProviderAvailable」关联路径「assertProviderAvailable」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「808dd0d7be3473d6299b8b0a」先于语句位置「1」的操作「958f24942cb52cdb326269a5」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/engine-runner.ts:73`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/214`。

### `server/services/engine-runner.ts::buildServices.withJobOptions.&lt;arrow@83:6&gt;`

构造捕获的空记录「{}」；没有从空记录形式推断额外字段或持久效果。 在调用形式「fn」中提供第 4 个实参「{ ...opts, dataRoot: runtimeDataRoot }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以字段投影形式「runtimeDataRoot」关联路径「runtimeDataRoot」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「opts」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。

源码：`server/services/engine-runner.ts:83`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/215`。

### `server/services/engine-runner.ts::buildServices.ports.&lt;arrow@92:8&gt;`

构造捕获的空记录「{}」；没有从空记录形式推断额外字段或持久效果。 将「{ ...opts, dataRoot: runtimeDataRoot }」作为第 4 个实参交给已绑定接口「ts:server/services/job/job-store#completeJob」，对应捕获形参「{ ts = nowIso(), dataRoot }: RuntimePathOptions &amp; { ts?: string } = {}」。该普通调用关系不替代进程或网络协议关系。 以字段投影形式「runtimeDataRoot」关联路径「runtimeDataRoot」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「opts」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。

源码：`server/services/engine-runner.ts:92`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/216`。

### `server/services/engine-runner.ts::buildServices.ports.&lt;arrow@99:8&gt;`

构造捕获的空记录「{}」；没有从空记录形式推断额外字段或持久效果。 将「{ ...opts, dataRoot: runtimeDataRoot }」作为第 5 个实参交给已绑定接口「ts:server/services/event/event-store#appendEvent」，对应捕获形参「opts: EventStoreOptions = {}」。该普通调用关系不替代进程或网络协议关系。 条件「(typeof jobId !== "string" || !/^[A-Za-z0-9][A-Za-z0-9-]*$/.test(jobId))」的捕获提前退出分支为「throw：new Error(`invalid jobId for appendEvent: ${JSON.stringify(jobId)}`)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new Error(`invalid jobId for appendEvent: ${JSON.stringify(jobId)}`);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「runtimeDataRoot」关联路径「runtimeDataRoot」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「opts」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「1ce120666e92043065af261c」先于语句位置「1」的操作「128b226e49894db787c6fb50」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/engine-runner.ts:99`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/217`。

### `server/services/engine-runner.ts::buildServices.ports.getPool`

构造捕获记录，字段按源码次序为「cpbRoot ← cpbRoot；hubRoot ← hubRoot；env ← runtimeEnv」。不据构造形式推断物理持久化。 将「{ cpbRoot, hubRoot, env: runtimeEnv }」作为第 1 个实参交给已绑定接口「ts:server/services/acp/acp-pool#getManagedAcpPool」，对应捕获形参「{ cpbRoot, hubRoot, ...opts }: AcpPoolOptions = {}」。该普通调用关系不替代进程或网络协议关系。 以字段投影形式「cpbRoot」关联路径「cpbRoot」；只描述捕获来源，不证明当时的字段值。

源码：`server/services/engine-runner.ts:107`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/218`。

### `server/services/engine-runner.ts::buildServices.ports.&lt;arrow@110:8&gt;`

构造捕获的空记录「{}」；没有从空记录形式推断额外字段或持久效果。 将「{ ...opts, dataRoot: runtimeDataRoot }」作为第 4 个实参交给已绑定接口「ts:server/services/job/job-projection#buildArtifactIndex」，对应捕获形参「{ events, dataRoot, wikiDir, restrictToWiki = false }: ArtifactIndexOptions = {}」。该普通调用关系不替代进程或网络协议关系。 以字段投影形式「runtimeDataRoot」关联路径「runtimeDataRoot」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「opts」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。

源码：`server/services/engine-runner.ts:110`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/219`。

### `server/services/engine-runner.ts::runJobWithServices`

构造捕获记录，字段按源码次序为「hubRoot ← hubRoot；env ← env；dataRoot ← projectRuntimeRoot；workerBrokerClient ← broker」。不据构造形式推断物理持久化。 将「{\n    ...jobOptions,\n    cpbRoot,\n    project,\n    hubRoot,\n    dataRoot: projectRuntimeRoot,\n    env,\n    sourcePath,\n    routing: opts.routing || null,\n    agentAvailability: opts.agentAvailability || null,\n    agentHealth: opts.agentHealth || null,\n    teamPolicy: opts.teamPolicy || null,\n    // Inject the existing process registry so verify h…［展示截断；完整操作保留］」作为第 1 个实参交给已绑定接口「ts:core/engine/run-job#runJob」，对应捕获形参「ctxInput: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「broker」的初始化来源为「workerBrokerClient instanceof WorkerBrokerClient ? workerBrokerClient : null」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!projectRuntimeRoot)」的捕获提前退出分支为「throw：new Error(`project runtime root required for project '${project}'`)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new Error(`project runtime root required for project '${project}'`);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「projectRuntimeRoot」关联路径「projectRuntimeRoot」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「envRecord(jobOptions.env || process.env)」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。 将「{ hubRoot, env, dataRoot: projectRuntimeRoot, workerBrokerClient: broker }」作为第 2 个实参交给已绑定接口「ts:server/services/engine-runner#buildServices」，对应捕获形参「{\n  hubRoot = null,\n  env = process.env,\n  dataRoot = null,\n  workerBrokerClient = null,\n}: LooseRecord = {}」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/engine-runner.ts:130`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/220`。

### `server/services/engine-runner.ts::runJobWithServices.&lt;object@157:16&gt;.&lt;object@173:26&gt;.registerChild`

构造捕获记录，字段按源码次序为「dataRoot ← projectRuntimeRoot」。不据构造形式推断物理持久化。 将「{ dataRoot: projectRuntimeRoot }」作为第 4 个实参交给已绑定接口「ts:server/services/infra#addChildPid」，对应捕获形参「options: AddChildPidOptions = {}」。该普通调用关系不替代进程或网络协议关系。 以字段投影形式「projectRuntimeRoot」关联路径「projectRuntimeRoot」；只描述捕获来源，不证明当时的字段值。

源码：`server/services/engine-runner.ts:174`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/221`。

### `server/services/event/event-materializer.ts::materializeJob`

构造捕获记录，字段按源码次序为「jobId ← null；project ← null；task ← null；status ← null；phase ← null；attempt ← null；workflow ← null；planMode ← null；planDecision ← null；executor ← null；artifacts ← {}；completedPhases ← []」；其余字段见完整操作。不据构造形式推断物理持久化。 将「state」作为第 1 个实参交给已绑定接口「ts:server/services/event/event-materializer#_syncDagResume」，对应捕获形参「state: MaterializedJobState」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「state.jobId = event.jobId」，捕获目标为「state.jobId」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「isPostTerminal」的初始化来源为「ctx.terminal」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return state;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「ee8ed85b15bd34da1742689f」先于语句位置「1」的操作「bd32c08a7c69c0dec663d398」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/event/event-materializer.ts:270`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/222`。

### `server/services/event/event-materializer.ts::advanceMaterializedJob`

构造捕获记录，字段按源码次序为「terminal ← TERMINAL_STATUSES.has(state.status)」。不据构造形式推断物理持久化。 将「state」作为第 1 个实参交给已绑定接口「ts:server/services/event/event-materializer#_syncDagResume」，对应捕获形参「state: MaterializedJobState」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「state.jobId = event.jobId」，捕获目标为「state.jobId」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「isPostTerminal」的初始化来源为「ctx.terminal」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(isPostTerminal &amp;&amp; !POST_TERMINAL_ALLOWED.has(event.type))」的捕获提前退出分支为「return：state」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return state;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「b76c7622ccfa784aa0dd31bb」先于语句位置「1」的操作「4787559206b5e28e25315892」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/event/event-materializer.ts:381`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/223`。

### `server/services/event/event-materializer.ts::EVENT_HANDLERS.job_superseded`

包含赋值/更新「state.status = "superseded"」，捕获目标为「state.status」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「8bcc709f70e2d8e6e04e3117」先于语句位置「1」的操作「c6c5e6bab42b83eb630d2aa0」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/event/event-materializer.ts:633`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/224`。

### `server/services/event/event-store.ts::serializeEvent`

在调用形式「Array.isArray」中提供第 1 个实参「event」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 对捕获 binding「serialized」存在源更新「serialized = JSON.stringify(event)」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(event === null || typeof event !== "object" || Array.isArray(event))」的捕获提前退出分支为「throw：new Error("invalid event: expected a non-null object")」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new Error("invalid event: expected a non-null object");」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「9a051d46a122c8d92fc7b5ce」先于语句位置「4」的操作「b1d0e2c11d79994f7e3e31a7」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/event/event-store.ts:273`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/225`。

### `server/services/event/event-store.ts::appendSerializedEventDurably`

构造捕获记录，字段按源码次序为「bytesWritten ← bytesWritten；fileSynced ← fileSynced；created ← created；parentSynced ← parentSynced；expectedBytes ← payload.byteLength」。不据构造形式推断物理持久化。 将「filePath」作为第 1 个实参交给已绑定接口「ts:server/services/event/event-store#eventPathGeneration」，对应捕获形参「filePath: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「maxWriteBytes」的初始化来源为「eventLockTestHooks().maxAppendWriteBytes」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「bytesWritten」存在源更新「bytesWritten += write.bytesWritten」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!expected &amp;&amp; errnoCode(error) === "EEXIST")」的捕获提前退出分支为「throw：eventFileSuccessor(filePath, "append")」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw eventFileSuccessor(filePath, "append");」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「filePath」关联路径「filePath」；只描述捕获来源，不证明当时的字段值。

源码：`server/services/event/event-store.ts:1034`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/226`。

### `server/services/event/event-store.ts::appendEvent`

构造捕获记录，字段按源码次序为「cpbRoot ← cpbRoot；project ← project；jobId ← jobId；file ← file；dataRoot ← opts.dataRoot ?? null；event ← written」。不据构造形式推断物理持久化。 将「tracedEvent」作为第 1 个实参交给已绑定接口「ts:server/services/event/event-store#serializeEvent」，对应捕获形参「event: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「boundEvent」的初始化来源为「bindEventStreamIdentity(event, project, jobId)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return written;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「project」关联路径「project」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「32a9a22a7eb2c8adbabbe1d7」先于语句位置「1」的操作「7119a6a6a14145eaa9fbdc84」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/event/event-store.ts:1179`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/227`。

### `server/services/event/event-store.ts::appendEvent.&lt;arrow@1188:44&gt;`

将「existing」作为第 1 个实参交给已绑定接口「ts:server/services/event/event-materializer#materializeJob」，对应捕获形参「events: EventRecord[]」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「artifact」的初始化来源为「tracedEvent.artifact」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(TERMINAL_STATUSES.has(state.status) &amp;&amp; !POST_TERMINAL_ALLOWED.has(eventType))」的捕获提前退出分支为「return：null」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return null;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「6bd51bf8cf3f7bafea03a29a」先于语句位置「1」的操作「89e08bf7363716a062f869fa」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/event/event-store#readEvents」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。 将「tracedEvent.artifact」作为第 1 个实参交给已绑定接口「ts:server/services/event/event-store#appendEvent.&lt;arrow@1188:44&gt;.writeBlocked」，对应捕获形参「artifactName: unknown」。该普通调用关系不替代进程或网络协议关系。 将「redacted」作为第 1 个实参交给已绑定接口「ts:server/services/event/event-store#serializeEvent」，对应捕获形参「event: unknown」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/event/event-store.ts:1188`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/228`。

### `server/services/event/event-store.ts::appendEvent.&lt;arrow@1188:44&gt;.writeBlocked`

构造捕获记录，字段按源码次序为「project ← project；jobId ← jobId」。不据构造形式推断物理持久化。 将「tracedBlocked」作为第 1 个实参交给已绑定接口「ts:server/services/event/event-store#serializeEvent」，对应捕获形参「event: unknown」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「blocked.jobId = tracedEvent.jobId ?? jobId」，捕获目标为「blocked.jobId」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「blocked」的初始化来源为「makeSecretBlockedEvent(artifactName, reason)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return tracedBlocked;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「project」关联路径「project」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「c174475cd52c277f05c020d2」先于语句位置「1」的操作「9e72f88347861ce86ccdc0fe」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「file」作为第 1 个实参交给已绑定接口「ts:server/services/event/event-store#appendSerializedEventDurably」，对应捕获形参「filePath: string」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/event/event-store.ts:1200`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/229`。

### `server/services/event/event-store.ts::appendEvent.&lt;arrow@1188:44&gt;.&lt;block@1221:38&gt;.&lt;arrow@1229:31&gt;`

将「typeof value === "string" ? value : JSON.stringify(value)」作为第 1 个实参交给已绑定接口「ts:server/services/secret-policy#isSecretContent」，对应捕获形参「content: unknown」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/event/event-store.ts:1229`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/230`。

### `server/services/event/event-store.ts::readEvents`

将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/event/event-store#eventFileFor」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「file」的初始化来源为「eventFileFor(cpbRoot, project, jobId, opts)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return result ?? [];」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「d10c82c0d127bf70f8edc493」先于语句位置「1」的操作「084dbc544ef61512cc4325c7」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/event/event-store.ts:1561`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/231`。

### `server/services/event/event-store.ts::readJobProjection`

构造捕获记录，字段按源码次序为「checkpointEventCount ← checkpointEventCount；eventCount ← events.length」。不据构造形式推断物理持久化。 将「events」作为第 1 个实参交给已绑定接口「ts:server/services/event/event-materializer#materializeJob」，对应捕获形参「events: EventRecord[]」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「checkpoint」的初始化来源为「await readCheckpointRecord(cpbRoot, project, jobId, opts)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「replayed」存在源更新「replayed = advanceMaterializedJob(replayed, event)」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!sameCheckpointState(replayed, fullyMaterialized))」的捕获提前退出分支为「throw：checkpointReplayError(\n      checkpoint,\n      `checkpoint suffix replay diverged from a full event replay: ${checkpoint.filePath}`,\n      "CHECKPOINT_REPLAY_MISMATCH",\n      { checkpointEventCount, eventCount: events.length },\n    )」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return {\n      ...cursor,\n      checkpointEventCount: null,\n      state: materializeJob(events),\n    };」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「checkpointEventCount」关联路径「checkpointEventCount」；只描述捕获来源，不证明当时的字段值。 将「replayed」作为第 1 个实参交给已绑定接口「ts:server/services/event/event-materializer#advanceMaterializedJob」，对应捕获形参「current: MaterializedJobState」。该普通调用关系不替代进程或网络协议关系。

条件「(!checkpoint)」的捕获提前退出分支为「return：{\n      ...cursor,\n      checkpointEventCount: null,\n      state: materializeJob(events),\n    }」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。

源码：`server/services/event/event-store.ts:1747`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/232`。

### `server/services/event/event-store.ts::withLockedJobProjection`

将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/event/event-store#eventFileFor」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「file」的初始化来源为「eventFileFor(cpbRoot, project, jobId, opts)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return withEventLock(file, async () =&gt; (\n    operation(await readJobProjection(cpbRoot, project, jobId, opts))\n  ));」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「fb823badf0f532a1eb3f2836」先于语句位置「1」的操作「c1c9144c62d94c87334510d0」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/event/event-store.ts:1785`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/233`。

### `server/services/event/event-store.ts::withLockedJobProjection.&lt;arrow@1793:29&gt;`

将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/event/event-store#readJobProjection」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/event/event-store.ts:1793`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/234`。

### `server/services/executor-root.ts::resolveExecutorRoot`

将「env」作为第 1 个实参交给已绑定接口「ts:shared/types#recordValue」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「envRecord」的初始化来源为「recordValue(env)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return path.resolve(stringValue(envRecord.CPB_EXECUTOR_ROOT) || stringValue(fallbackRoot));」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「dea4d4487c07ce43bd806ce1」先于语句位置「1」的操作「430c43b998e4db52377e83f2」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/executor-root.ts:53`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/235`。

### `server/services/executor-root.ts::executorEnv`

构造捕获记录，字段按源码次序为「CPB_ROOT ← path.resolve(stringValue(cpbRoot) || stringValue(envRecord.CPB_ROOT) || process.cwd())；CPB_EXECUTOR_ROOT ← path.resolve(stringValue(executorRoot) || stringValue(envRecord.CPB_EXECUTOR_ROOT) || stringValue(cpbRoot) || process.cwd())」。不据构造形式推断物理持久化。 将「env」作为第 1 个实参交给已绑定接口「ts:shared/types#recordValue」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「envRecord」的初始化来源为「recordValue(env)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return buildChildEnv(stringEnv(envRecord), {\n    CPB_ROOT: path.resolve(stringValue(cpbRoot) || stringValue(envRecord.CPB_ROOT) || process.cwd()),\n    CPB_EXECUTOR_ROOT: path.resolve(stringValue(executorRoot) || stringValue(envRecord.CPB_EXECUTOR_ROOT) || stringValue(cpbRoot) || process.cwd()),\n    ...stringEnv(extra),\n  });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留记录复制/展开来源「stringEnv(extra)」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「a0ecfa40236e3b7c49c45ac1」先于语句位置「1」的操作「5de3f6a803593548f5ae2c58」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「{\n    CPB_ROOT: path.resolve(stringValue(cpbRoot) || stringValue(envRecord.CPB_ROOT) || process.cwd()),\n    CPB_EXECUTOR_ROOT: path.resolve(stringValue(executorRoot) || stringValue(envRecord.CPB_EXECUTOR_ROOT) || stringValue(cpbRoot) || process.cwd()),\n    ...stringEnv(extra),\n  }」作为第 2 个实参交给已绑定接口「ts:core/policy/child-env#buildChildEnv」，对应捕获形参「extra: EnvMap = {}」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/executor-root.ts:58`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/236`。

### `server/services/github/github-issues.ts::runGit`

构造捕获记录，字段按源码次序为「cwd ← cwd；maxBuffer ← 1024 * 1024」。不据构造形式推断物理持久化。 将「await runCommand("git", args, opts)」作为第 1 个实参交给已绑定接口「ts:server/services/github/github-issues#assertCommandSucceeded」，对应捕获形参「value: GitHubCommandResult | string」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「opts.env = env」，捕获目标为「opts.env」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「opts」的初始化来源为「{ cwd, maxBuffer: 1024 * 1024 }」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return assertCommandSucceeded(await runCommand("git", args, opts), `git ${args[0] || "command"}`) as GitHubRecord;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「cwd」关联路径「cwd」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「00dbf081ac06e542eb0c294e」先于语句位置「1」的操作「52ce9e6dda1bdde991963ac2」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/github/github-issues.ts:993`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/237`。

### `server/services/github/github-issues.ts::pushGithubCommitWithControlledTransport`

构造捕获记录，字段按源码次序为「committed ← false；attempted ← false」。不据构造形式推断物理持久化。 将「{ committedOnSuccess: (verification) =&gt; verification.committed }」作为第 4 个实参交给已绑定接口「ts:server/services/github/github-issues#withGithubTemporaryWorkspace」，对应捕获形参「{\n    committedOnSuccess = () =&gt; true,\n  }: {\n    committedOnSuccess?: (result: T) =&gt; boolean | null;\n  } = {}」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「record.attempted = pushAttempted」，捕获目标为「record.attempted」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「record」的初始化来源为「recordValue(error)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!worktree)」的捕获提前退出分支为「throw：Object.assign(new Error("controlled GitHub push requires a worktree"), { committed: false, attempted: false })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw Object.assign(new Error("controlled GitHub push requires a worktree"), { committed: false, attempted: false });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「819c5720602e1be1dec01cdf」先于语句位置「1」的操作「8c41812e4ac84194c3bdaf5e」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/github/github-issues.ts:1175`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/238`。

### `server/services/github/github-issues.ts::pushGithubCommitWithControlledTransport.&lt;block@1222:6&gt;.&lt;arrow@1226:6&gt;`

构造捕获记录，字段按源码次序为「operation ← "repository.push"；committed ← null；reason ← "controlled GitHub push has no remote post-condition verifier"」。不据构造形式推断物理持久化。 将「{\n          runCommand,\n          env: gitEnv,\n        }」作为第 3 个实参交给已绑定接口「ts:server/services/github/github-issues#runGit」，对应捕获形参「{ runCommand = execFileAsync, env }: GitHubRecord &amp; { runCommand?: RunCommand; env?: NodeJS.ProcessEnv } = {}」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「pushEnv.CPB_GIT_ASKPASS_TOKEN = token」，捕获目标为「pushEnv.CPB_GIT_ASKPASS_TOKEN」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「gitEnv」的初始化来源为「githubTrustedGitEnv(env, workspace.rootPath)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「transportError」存在源更新「transportError = error」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(sourceHead !== commit.toLowerCase())」的捕获提前退出分支为「throw：Object.assign(new Error("worktree HEAD changed before controlled GitHub push"), {\n            committed: false,\n            attempted: false,\n          })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw Object.assign(new Error("worktree HEAD changed before controlled GitHub push"), {\n            committed: false,\n            attempted: false,\n          });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`server/services/github/github-issues.ts:1226`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/239`。

### `server/services/github/github-issues.ts::openDraftPullRequest`

构造捕获记录，字段按源码次序为「status ← "pr.opened"；jobStatus ← "passed"；request ← request；response ← response；prUrl ← discoveredUrl；prNumber ← discoveredNumber；committed ← true；branchPreparation ← branchPreparation；verification ← safeDiscovery；transportWarning ← transportWarning；remoteWrites ← {\n          pullRequestCreate: {\n            attempted: true,\n            committed: true,\n            verification: safeDiscovery,\n            transportWa…［展示截断；完整操作保留］」。不据构造形式推断物理持久化。 将「{\n      ...boundCreateRequest,\n      pullRequestNumber: prNumber,\n    }」作为第 1 个实参交给已绑定接口「ts:server/services/github/github-issues#detachedRemoteAuthorityRequest」，对应捕获形参「request: GithubRemoteAuthorityRequest」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「errorRecord」的初始化来源为「recordValue(error)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「branchPreparation」存在源更新「branchPreparation = await preparePullRequestBranchWithGit(request, normalizedJob, {\n      runCommand,\n      token: pushToken,\n      remoteCapability,\n      remoteAuthorityValidator,\n      remoteCommitVerifier,\n      beforeRemoteMutation: beforeRemoteMutation\n        ? (operation, authorityRequest) =&gt; beforeRemoteMutation(operation, {\n            ...a…［展示截断；完整操作保留］」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(response.ok === false)」的捕获提前退出分支为「throw：Object.assign(new Error("pull request transport returned ok=false"), {\n        code: "GITHUB_PR_CREATE_TRANSPORT_REJECTED",\n        committed: null,\n        response: safeResponse,\n      })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return {\n      status: "skipped",\n      reason: "draft PR creation requires a PASS verdict",\n      jobStatus: stringValue(normalizedJob.status, "unknown"),\n    };」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「artifacts」关联路径「artifacts」；只描述捕获来源，不证明当时的字段值。

源码：`server/services/github/github-issues.ts:1529`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/240`。

### `server/services/github/github-issues.ts::openDraftPullRequest.&lt;block@1600:21&gt;.&lt;object@1601:86&gt;.&lt;arrow@1608:10&gt;`

构造捕获记录，字段按源码次序为「repo ← request.repo；head ← request.head；base ← request.base；title ← request.title；body ← request.body；draft ← request.draft」。不据构造形式推断物理持久化。 在调用形式「beforeRemoteMutation」中提供第 2 个实参「{\n            ...authorityRequest,\n            pullRequestPlan: {\n              repo: request.repo,\n              head: request.head,\n              base: request.base,\n              title: request.title,\n              body: request.body,\n              draft: request.draft,\n            },\n          }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以字段投影形式「request.repo」关联路径「request.repo」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「authorityRequest」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。

源码：`server/services/github/github-issues.ts:1608`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/241`。

### `server/services/github/github-issues.ts::openDraftPullRequest.&lt;block@1654:6&gt;.&lt;arrow@1670:8&gt;`

在调用形式「createPullRequest」中提供第 1 个实参「req」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`server/services/github/github-issues.ts:1670`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/242`。

### `server/services/github/github-issues.ts::openDraftPullRequest.&lt;block@1654:6&gt;.&lt;arrow@1671:8&gt;`

构造捕获记录，字段按源码次序为「runCommand ← runCommand」。不据构造形式推断物理持久化。 将「{ runCommand }」作为第 2 个实参交给已绑定接口「ts:server/services/github/github-issues#createPullRequestWithGh」，对应捕获形参「{ runCommand = execFileAsync }: GitHubRecord &amp; { runCommand?: RunCommand } = {}」。该普通调用关系不替代进程或网络协议关系。 以字段投影形式「runCommand」关联路径「runCommand」；只描述捕获来源，不证明当时的字段值。

源码：`server/services/github/github-issues.ts:1671`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/243`。

### `server/services/hub/hub-queue.ts::isQueueEntry`

将「value」作为第 1 个实参交给已绑定接口「ts:server/services/hub/hub-queue#isRecord」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 以「return isRecord(value);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`server/services/hub/hub-queue.ts:352`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/244`。

### `server/services/hub/hub-queue.ts::toQueueEntries`

在调用形式「Array.isArray」中提供第 1 个实参「value」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return Array.isArray(value) ? value.filter(isQueueEntry) : [];」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`server/services/hub/hub-queue.ts:356`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/245`。

### `server/services/hub/hub-queue.ts::queuePath`

在调用形式「path.resolve」中提供第 1 个实参「hubRoot」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return path.join(path.resolve(hubRoot), "queue", "queue.json");」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`server/services/hub/hub-queue.ts:553`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/246`。

### `server/services/hub/hub-queue.ts::normalizeQueue`

构造捕获记录，字段按源码次序为「version ← typeof obj.version === "number" ? obj.version : QUEUE_VERSION；entries ← toQueueEntries(obj.entries)」。不据构造形式推断物理持久化。 将「obj.entries」作为第 1 个实参交给已绑定接口「ts:server/services/hub/hub-queue#toQueueEntries」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「obj」的初始化来源为「raw as LooseRecord」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!raw || typeof raw !== "object" || Array.isArray(raw))」的捕获提前退出分支为「return：defaultQueue()」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return defaultQueue();」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「780d5db98fd428c729e6fb98」先于语句位置「1」的操作「a31d18b8b82a863f6b10faa1」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/hub/hub-queue.ts:561`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/247`。

### `server/services/hub/hub-queue.ts::withQueueProcessFence`

构造捕获记录，字段按源码次序为「waitMs ← QUEUE_LOCK_TTL_MS」。不据构造形式推断物理持久化。 将「lockDir」作为第 1 个实参交给已绑定接口「ts:shared/primitives/durable-directory-lock#withDirectoryProcessFence」，对应捕获形参「lockPath: string」。该普通调用关系不替代进程或网络协议关系。 以「return withDirectoryProcessFence(lockDir, callback, { waitMs: QUEUE_LOCK_TTL_MS });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「QUEUE_LOCK_TTL_MS」关联路径「QUEUE_LOCK_TTL_MS」；只描述捕获来源，不证明当时的字段值。

源码：`server/services/hub/hub-queue.ts:980`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/248`。

### `server/services/hub/hub-queue.ts::withQueueLock`

构造捕获记录，字段按源码次序为「format ← QUEUE_LOCK_OWNER_FORMAT；ownerToken ← randomUUID()；lockPath ← lockDir；ownerPid ← process.pid；host ← os.hostname()；acquiredAt ← nowIso()；processIdentity ← processIdentity」。不据构造形式推断物理持久化。 将「hubRoot」作为第 1 个实参交给已绑定接口「ts:server/services/hub/hub-queue#queuePath」，对应捕获形参「hubRoot: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「attempt」的初始化来源为「0」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「primaryError」存在源更新「primaryError = err」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!processIdentity)」的捕获提前退出分支为「throw：queueLockError(`queue lock process identity unavailable: ${lockDir}`, "HUB_QUEUE_LOCK_IDENTITY_UNAVAILABLE")」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw queueLockError(`queue lock process identity unavailable: ${lockDir}`, "HUB_QUEUE_LOCK_IDENTITY_UNAVAILABLE");」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「QUEUE_LOCK_OWNER_FORMAT」关联路径「QUEUE_LOCK_OWNER_FORMAT」；只描述捕获来源，不证明当时的字段值。 将「hubRoot」作为第 1 个实参交给已绑定接口「ts:server/services/hub/hub-queue#loadLocalQueue」，对应捕获形参「hubRoot: string」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/hub/hub-queue.ts:1309`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/249`。

### `server/services/hub/hub-queue.ts::withQueueLock.&lt;loop@1330:2&gt;.&lt;block@1330:53&gt;.&lt;arrow@1331:56&gt;`

构造捕获记录，字段按源码次序为「owner ← partialOwnerSnapshot?.owner || null；ownerSnapshot ← partialOwnerSnapshot?.raw || null；lockGeneration ← pathGeneration(createdInfo)；kind ← "incomplete"」。不据构造形式推断物理持久化。 将「{\n              owner: partialOwnerSnapshot?.owner || null,\n              ownerSnapshot: partialOwnerSnapshot?.raw || null,\n              lockGeneration: pathGeneration(createdInfo),\n              kind: "incomplete",\n            }」作为第 2 个实参交给已绑定接口「ts:server/services/hub/hub-queue#quarantineQueueLock」，对应捕获形参「candidate: QueueLockCandidate」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「partialOwnerSnapshot」的初始化来源为「null」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「partialOwnerSnapshot」存在源更新「partialOwnerSnapshot = await readQueueLockOwnerSnapshot(ownerFile)」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(errnoCode(err) === "HUB_QUEUE_LOCK_OWNER_COMMITTED_AMBIGUOUS")」的捕获提前退出分支为「throw：err」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw err;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「err」关联路径「err」；只描述捕获来源，不证明当时的字段值。

源码：`server/services/hub/hub-queue.ts:1331`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/250`。

### `server/services/hub/hub-queue.ts::withQueueLock.&lt;block@1402:6&gt;.&lt;arrow@1403:58&gt;`

将「lockDir」作为第 1 个实参交给已绑定接口「ts:server/services/hub/hub-queue#releaseQueueLockExact」，对应捕获形参「lockDir: string」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/hub/hub-queue.ts:1403`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/251`。

### `server/services/hub/hub-queue.ts::loadLocalQueue`

构造捕获记录，字段按源码次序为「maxBytes ← QUEUE_MAX_BYTES」。不据构造形式推断物理持久化。 将「hubRoot」作为第 1 个实参交给已绑定接口「ts:server/services/hub/hub-queue#queuePath」，对应捕获形参「hubRoot: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「raw」的初始化来源为「await readBoundedRegularFileNoFollow(queuePath(hubRoot), { maxBytes: QUEUE_MAX_BYTES })」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(String(errnoCode(err)).startsWith("BOUNDED_FILE_"))」的捕获提前退出分支为「throw：Object.assign(new Error(`unsafe local queue file: ${queuePath(hubRoot)}`, { cause: err }), {\n        code: errnoCode(err) === "BOUNDED_FILE_TOO_LARGE" ? "HUB_QUEUE_TOO_LARGE" : "HUB_QUEUE_UNSAFE",\n      })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return defaultQueue();」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「QUEUE_MAX_BYTES」关联路径「QUEUE_MAX_BYTES」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「ddfdb7cfc92b33c1f900a13e」先于语句位置「1」的操作「4ff1df254db77e27e242b21d」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「JSON.parse(raw)」作为第 1 个实参交给已绑定接口「ts:server/services/hub/hub-queue#normalizeQueue」，对应捕获形参「raw: unknown」。该普通调用关系不替代进程或网络协议关系。

条件「(errnoCode(err) === "ENOENT")」的捕获提前退出分支为「return：defaultQueue()」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。

源码：`server/services/hub/hub-queue.ts:1424`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/252`。

### `server/services/hub/hub-queue.ts::serializeQueue`

构造捕获记录，字段按源码次序为「version ← QUEUE_VERSION；entries ← queue.entries」。不据构造形式推断物理持久化。 在调用形式「JSON.stringify」中提供第 1 个实参「{ version: QUEUE_VERSION, entries: queue.entries }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「serialized」的初始化来源为「JSON.stringify({ version: QUEUE_VERSION, entries: queue.entries })」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(Buffer.byteLength(serialized, "utf8") &gt; QUEUE_MAX_BYTES)」的捕获提前退出分支为「throw：Object.assign(new Error(`queue exceeds ${QUEUE_MAX_BYTES} bytes`), { code: "HUB_QUEUE_TOO_LARGE" })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw Object.assign(new Error(`queue exceeds ${QUEUE_MAX_BYTES} bytes`), { code: "HUB_QUEUE_TOO_LARGE" });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「queue.entries」关联路径「queue.entries」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「14617ad853d2bf0ead9ef7db」先于语句位置「1」的操作「6f013455b2dd93b6e3f0355b」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/hub/hub-queue.ts:1439`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/253`。

### `server/services/hub/hub-queue.ts::saveLocalQueue`

构造捕获记录，字段按源码次序为「version ← QUEUE_VERSION；entries ← queue.entries」。不据构造形式推断物理持久化。 将「hubRoot」作为第 1 个实参交给已绑定接口「ts:server/services/hub/hub-queue#queuePath」，对应捕获形参「hubRoot: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「normalized」的初始化来源为「{ version: QUEUE_VERSION, entries: queue.entries }」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return normalized;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「queue.entries」关联路径「queue.entries」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「1836da9f9c95ff697d1971af」先于语句位置「1」的操作「ae04a00e59d43891d3bfd530」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「queuePath(hubRoot)」作为第 1 个实参交给已绑定接口「ts:server/services/hub/hub-queue#writeAtomic」，对应捕获形参「filePath: string」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/hub/hub-queue.ts:1447`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/254`。

### `server/services/hub/hub-queue.ts::withQueueMutation`

将「hubRoot」作为第 1 个实参交给已绑定接口「ts:server/services/hub/hub-queue#withQueueLock」，对应捕获形参「hubRoot: string」。该普通调用关系不替代进程或网络协议关系。 以「return await withQueueLock(hubRoot, (queue) =&gt; callback(queue, Date.now()));」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「fad46d14a9f40e1bee39133a」先于语句位置「1」的操作「ba2314a31cebe5858b970a88」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/hub/hub-queue.ts:1454`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/255`。

### `server/services/hub/hub-queue.ts::withQueueMutation.&lt;arrow@1462:38&gt;`

在调用形式「callback」中提供第 1 个实参「queue」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`server/services/hub/hub-queue.ts:1462`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/256`。

### `server/services/hub/hub-queue.ts::loadQueue`

将「hubRoot」作为第 1 个实参交给已绑定接口「ts:server/services/hub/hub-queue#loadLocalQueue」，对应捕获形参「hubRoot: string」。该普通调用关系不替代进程或网络协议关系。 以「return await loadLocalQueue(hubRoot);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`server/services/hub/hub-queue.ts:1465`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/257`。

### `server/services/hub/hub-queue.ts::writeAtomic`

构造捕获记录，字段按源码次序为「code ← "HUB_QUEUE_WRITE_COMMITTED_AMBIGUOUS"；committed ← true；committedPath ← filePath；recoveryPaths ← { canonical: filePath }」。不据构造形式推断物理持久化。 将「filePath」作为第 1 个实参交给已绑定接口「ts:server/services/hub/hub-queue#generationFor」，对应捕获形参「filePath: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「cleanupErrors」的初始化来源为「[]」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「existingGeneration」存在源更新「existingGeneration = await generationFor(filePath)」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(errnoCode(statError) !== "ENOENT")」的捕获提前退出分支为「throw：statError」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw statError;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「filePath」关联路径「filePath」；只描述捕获来源，不证明当时的字段值。

源码：`server/services/hub/hub-queue.ts:1469`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/258`。

### `server/services/hub/hub-queue.ts::entryKey`

捕获 binding「lineage」的初始化来源为「entry.metadata?.queueDedupeKey || entry.metadata?.originJobId || ""」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return `${entry.projectId}::${entry.description}::${lineage}`;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「64465b516c6801b57e5f7ca2」先于语句位置「1」的操作「2350f8456691e1d3d415d23c」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/hub/hub-queue.ts:1545`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/259`。

### `server/services/hub/hub-queue.ts::enqueue`

构造捕获记录，字段按源码次序为「sourcePath ← stringOrNull(rawMeta.sourcePath)；sessionId ← stringOrNull(rawMeta.sessionId)；workerId ← stringOrNull(rawMeta.workerId)；cwd ← stringOrNull(rawMeta.cwd)」。不据构造形式推断物理持久化。 将「hubRoot」作为第 1 个实参交给已绑定接口「ts:server/services/agent/agent-config#resolveAgentsForEntry」，对应捕获形参「hubRoot: string」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「meta.sourcePath = project.sourcePath」，捕获目标为「meta.sourcePath」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「projectId」的初始化来源为「input.projectId」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!input.projectId)」的捕获提前退出分支为「throw：new Error("projectId is required")」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new Error("projectId is required");」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「projectId」关联路径「projectId」；只描述捕获来源，不证明当时的字段值。 将「hubRoot」作为第 1 个实参交给已绑定接口「ts:server/services/hub/hub-queue#withQueueMutation」，对应捕获形参「hubRoot: string」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/hub/hub-queue.ts:1550`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/260`。

### `server/services/hub/hub-queue.ts::enqueue.&lt;arrow@1595:36&gt;`

构造捕获记录，字段按源码次序为「id ← generateId()；projectId ← projectId；sourcePath ← meta.sourcePath；sessionId ← meta.sessionId；workerId ← meta.workerId；cwd ← meta.cwd；executionBoundary ← REQUIRED_EXECUTION_BOUNDARY；type ← normalizedInput.type || "candidate"；status ← "pending"；priority ← normalizedInput.priority || "P2"；description ← normalizedInput.description || ""；metadata ← normalizedInput.metadata || {}」；其余字段见完整操作。不据构造形式推断物理持久化。 将「normalizedInput」作为第 1 个实参交给已绑定接口「ts:server/services/hub/hub-queue#entryKey」，对应捕获形参「entry: QueueEntryInput」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「key」的初始化来源为「entryKey(normalizedInput)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(existing)」的捕获提前退出分支为「return：existing」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return existing;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「projectId」关联路径「projectId」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「06c8d4921787cae04cef8d9d」先于语句位置「1」的操作「0d32f9e0694ed3c1314ff172」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/hub/hub-queue.ts:1595`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/261`。

### `server/services/hub/hub-queue.ts::enqueue.&lt;arrow@1595:36&gt;.&lt;arrow@1597:40&gt;`

将「e」作为第 1 个实参交给已绑定接口「ts:server/services/hub/hub-queue#entryKey」，对应捕获形参「entry: QueueEntryInput」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/hub/hub-queue.ts:1597`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/262`。

### `server/services/hub/hub-queue.ts::updateEntry`

将「hubRoot」作为第 1 个实参交给已绑定接口「ts:server/services/hub/hub-queue#withQueueMutation」，对应捕获形参「hubRoot: string」。该普通调用关系不替代进程或网络协议关系。 以「return withQueueMutation(hubRoot, async (queue, authorityNowMs) =&gt; {\n    const entry = queue.entries.find((e) =&gt; e.id === entryId);\n    if (!entry) return null;\n\n    const expectedStatuses = Array.isArray(guard.expectedStatus)\n      ? guard.expectedStatus\n      : guard.expectedStatus === undefined\n        ? null\n        : [guard.expectedStatus];\n   …［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`server/services/hub/hub-queue.ts:1633`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/263`。

### `server/services/hub/hub-queue.ts::updateEntry.&lt;arrow@1640:36&gt;`

具有捕获记录构造「{ ...entry.metadata, ...patch.metadata }」；该记录的可枚举字段为空或保留开放形状，未把展开来源补成确定字段。 将「entry」作为第 1 个实参交给已绑定接口「ts:server/services/hub/hub-queue#clearClaim」，对应捕获形参「entry: QueueEntryInput」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「entry.status = patch.status」，捕获目标为「entry.status」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「entry」的初始化来源为「queue.entries.find((e) =&gt; e.id === entryId)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!entry)」的捕获提前退出分支为「return：null」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return null;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留记录复制/展开来源「entry.metadata」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。

源码：`server/services/hub/hub-queue.ts:1640`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/264`。

### `server/services/hub/hub-queue.ts::listQueue`

将「hubRoot」作为第 1 个实参交给已绑定接口「ts:server/services/hub/hub-queue#loadQueue」，对应捕获形参「hubRoot: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「queue」的初始化来源为「await loadQueue(hubRoot)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return queue.entries.filter((e) =&gt; {\n    if (status &amp;&amp; e.status !== status) return false;\n    if (projectId &amp;&amp; e.projectId !== projectId) return false;\n    return true;\n  });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「cc9aa472fcac9044861fc4d9」先于语句位置「1」的操作「196546be974d4be7b5868865」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/hub/hub-queue.ts:1673`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/265`。

### `server/services/hub/hub-queue.ts::listQueue.&lt;arrow@1675:30&gt;`

条件「(status &amp;&amp; e.status !== status)」的捕获提前退出分支为「return：false」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return false;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「edb56fffea8707496d5678ee」先于语句位置「1」的操作「4a18eb95664b786e0304bb95」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/hub/hub-queue.ts:1675`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/266`。

### `server/services/hub/worker-state-broker.ts::readWorkerBrokerBody`

将「parsed」作为第 1 个实参交给已绑定接口「ts:core/contracts/types#isRecord」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「value」的初始化来源为「Buffer.isBuffer(chunk) ? chunk : Buffer.from(String(chunk))」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「size」存在源更新「size += value.length」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(size &gt; MAX_BROKER_BODY_BYTES)」的捕获提前退出分支为「throw：brokerError("HUB_WORKER_BROKER_REQUEST_TOO_LARGE", "worker broker request is too large", 413)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw brokerError("HUB_WORKER_BROKER_REQUEST_TOO_LARGE", "worker broker request is too large", 413);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「67ca467ac3c059f1095515c9」先于语句位置「1」的操作「70e6c38ad81d41278a8600ff」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/hub/worker-state-broker.ts:92`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/267`。

### `server/services/hub/worker-state-broker.ts::handleWorkerStateBroker`

构造捕获记录，字段按源码次序为「assignment ← assignment；active ← active；project ← project；projectId ← projectId；dataRoot ← dataRoot；jobId ← expectedJobId」。不据构造形式推断物理持久化。 将「{\n        ...pick(input, [\n          "ts", "executor", "indexSnapshot", "indexFreshness", "planCache",\n          "routingCategory", "routing", "agentAvailability", "teamPolicy",\n        ]),\n        project: scope.projectId,\n        jobId: scope.jobId,\n        task: typeof scope.assignment.task === "string" ? scope.assignment.task : "",\n        workfl…［展示截断；完整操作保留］」作为第 2 个实参交给已绑定接口「ts:server/services/job/job-store#createJob」，对应捕获形参「{\n    project,\n    task,\n    workflow = "standard",\n    planMode = null,\n    ts = nowIso(),\n    jobId: providedJobId,\n    executor = null,\n    dataRoot,\n    sourceContext,\n    queueEntryId = null,\n    indexSnapshot = null,\n    indexFreshness = null,\n    planCache = null,\n    routingCategory = null,\n    routing = null,\n    agentAvailability = …［展示截断；完整操作保留］」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「activeAssignmentId」的初始化来源为「typeof worker.currentAssignmentId === "string" ? worker.currentAssignmentId : ""」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「assignmentActive」存在源更新「assignmentActive = assignmentId ? await assignments.getActiveAttempt(assignmentId) : null」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!token || !workerId || !incarnationToken || !op)」的捕获提前退出分支为「throw：brokerError("HUB_WORKER_BROKER_AUTHENTICATION_REQUIRED", "valid worker broker credentials are required", 401)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw brokerError("HUB_WORKER_BROKER_AUTHENTICATION_REQUIRED", "valid worker broker credentials are required", 401);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「assignment」关联路径「assignment」；只描述捕获来源，不证明当时的字段值。 将「{\n        ...event,\n        jobId: scope.jobId,\n        project: scope.projectId,\n      }」作为第 4 个实参交给已绑定接口「ts:server/services/event/event-store#appendEvent」，对应捕获形参「event: EventRecord」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/hub/worker-state-broker.ts:111`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/268`。

### `server/services/hub/worker-state-broker.ts::handleWorkerStateBroker.scopedJob`

将「"HUB_WORKER_BROKER_OPERATION_DENIED"」作为第 1 个实参交给已绑定接口「ts:server/services/hub/worker-state-broker#brokerError」，对应捕获形参「code: string」。该普通调用关系不替代进程或网络协议关系。 条件「(!jobScope)」的捕获提前退出分支为「throw：brokerError("HUB_WORKER_BROKER_OPERATION_DENIED", "job scope is required", 403)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw brokerError("HUB_WORKER_BROKER_OPERATION_DENIED", "job scope is required", 403);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「6b6d9ff9184c939e9267a6ae」先于语句位置「1」的操作「d50eb887b83a9329924ec659」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/hub/worker-state-broker.ts:189`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/269`。

### `server/services/job/job-store.ts::writeJobsIndex`

将「index」作为第 2 个实参交给已绑定接口「ts:shared/hub-maintenance#writeJsonDurableAtomic」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「target」的初始化来源为「indexFilePath(cpbRoot, opts)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留同一块中的正常源码顺序：语句位置「0」的操作「b6e1a5228e5d898af73a2ad3」先于语句位置「1」的操作「dff0a16ec0cfd22128382add」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/job/job-store.ts:310`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/270`。

### `server/services/job/job-store.ts::updateJobsIndexEntry`

将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/job/job-store#enqueueWrite」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。 以「return enqueueWrite(cpbRoot, opts, async () =&gt; {\n    const afterProjectionRead = jobsIndexLockTestHooks().afterProjectionRead;\n    if (afterProjectionRead) {\n      const observed = await readJobProjection(cpbRoot, project, jobId, opts);\n      await afterProjectionRead({\n        project,\n        jobId,\n        eventCount: observed.eventCount,\n        …［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`server/services/job/job-store.ts:315`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/271`。

### `server/services/job/job-store.ts::updateJobsIndexEntry.&lt;arrow@316:37&gt;`

构造捕获记录，字段按源码次序为「project ← project；jobId ← jobId；eventCount ← observed.eventCount；state ← observed.eventCount &gt; 0 ? observed.state : state」。不据构造形式推断物理持久化。 将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/event/event-store#readJobProjection」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「observed」的初始化来源为「await readJobProjection(cpbRoot, project, jobId, opts)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return withLockedJobProjection(cpbRoot, project, jobId, opts, async (projection) =&gt; {\n      const authoritativeState = projection.eventCount &gt; 0 ? projection.state : state;\n      const index = await readJobsIndex(cpbRoot, opts) || {\n        _meta: { version: INDEX_VERSION, updatedAt: null, jobCount: 0 },\n        jobs: {},\n      } satisfies JobsIndex;\n\…［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「project」关联路径「project」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「3add03de8ea18e9d6bd983b2」先于语句位置「1」的操作「ff1a2eaa6a2340bdf5f6b1be」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/event/event-store#withLockedJobProjection」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/job/job-store.ts:316`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/272`。

### `server/services/job/job-store.ts::updateJobsIndexEntry.&lt;arrow@316:37&gt;.&lt;arrow@331:66&gt;`

构造捕获记录，字段按源码次序为「version ← INDEX_VERSION；updatedAt ← null；jobCount ← 0」。不据构造形式推断物理持久化。 将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/job/job-store#writeJobsIndex」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「index._meta.updatedAt = new Date().toISOString()」，捕获目标为「index._meta.updatedAt」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「authoritativeState」的初始化来源为「projection.eventCount &gt; 0 ? projection.state : state」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return authoritativeState as JobState;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「INDEX_VERSION」关联路径「INDEX_VERSION」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「da9c83a9f780009e7f00cf5c」先于语句位置「1」的操作「20e40beccea9873269d12664」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/job/job-store.ts:331`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/273`。

### `server/services/job/job-store.ts::rebuildJobsIndexLocked`

构造捕获记录，字段按源码次序为「version ← INDEX_VERSION；updatedAt ← new Date().toISOString()；jobCount ← Object.keys(jobs).length」。不据构造形式推断物理持久化。 将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/event/event-store#readEvents」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「events」的初始化来源为「await readEvents(cpbRoot, project, jobId, opts)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return index;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「INDEX_VERSION」关联路径「INDEX_VERSION」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「3cd611d6243b8a16e69e2643」先于语句位置「1」的操作「43283d7bfc510dc7885b8280」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「events」作为第 1 个实参交给已绑定接口「ts:server/services/event/event-materializer#materializeJob」，对应捕获形参「events: EventRecord[]」。该普通调用关系不替代进程或网络协议关系。 将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/job/job-store#writeJobsIndex」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/job/job-store.ts:348`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/274`。

### `server/services/job/job-store.ts::rebuildJobsIndex`

将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/job/job-store#enqueueWrite」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。 以「return enqueueWrite(cpbRoot, opts, () =&gt; rebuildJobsIndexLocked(cpbRoot, opts));」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`server/services/job/job-store.ts:374`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/275`。

### `server/services/job/job-store.ts::rebuildJobsIndex.&lt;arrow@375:37&gt;`

将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/job/job-store#rebuildJobsIndexLocked」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/job/job-store.ts:375`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/276`。

### `server/services/job/job-store.ts::listJobsFromIndex`

将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/job/job-store#enqueueWrite」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。 以「return enqueueWrite(cpbRoot, opts, async () =&gt; {\n    let index = await readJobsIndex(cpbRoot, opts);\n    if (!index) {\n      index = await rebuildJobsIndexLocked(cpbRoot, opts);\n    } else {\n      index = await mergeMissingEventStreams(cpbRoot, index, opts);\n    }\n\n    return Object.values(index.jobs)\n      .filter((job) =&gt; job.createdAt &amp;&amp; job.proj…［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`server/services/job/job-store.ts:411`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/277`。

### `server/services/job/job-store.ts::listJobsFromIndex.&lt;arrow@412:37&gt;`

将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/job/job-store#rebuildJobsIndexLocked」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「index」的初始化来源为「await readJobsIndex(cpbRoot, opts)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「index」存在源更新「index = await rebuildJobsIndexLocked(cpbRoot, opts)」；循环和分支条件见操作上下文，未推执行次数或最终数值。 以「return Object.values(index.jobs)\n      .filter((job) =&gt; job.createdAt &amp;&amp; job.project &amp;&amp; job.jobId)\n      .sort((a, b) =&gt; (b.updatedAt ?? "").localeCompare(a.updatedAt ?? ""));」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「2eb24becaea86567302151d9」先于语句位置「2」的操作「fdb11fb1a1008be8e2cb19e4」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/job/job-store.ts:412`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/278`。

### `server/services/job/job-store.ts::listJobsFromIndex.&lt;arrow@412:37&gt;.&lt;arrow@422:12&gt;`

在调用形式「(b.updatedAt ?? "").localeCompare」中提供第 1 个实参「a.updatedAt ?? ""」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`server/services/job/job-store.ts:422`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/279`。

### `server/services/job/job-store.ts::retryUpdate`

在调用形式「process.stderr.write」中提供第 1 个实参「`${ts} [error] [job-store] index update failed after ${maxRetries} retries: ${err.message}\n`」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「i」的初始化来源为「0」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「i」存在源更新「i++」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(i === maxRetries - 1)」的捕获提前退出分支为「throw：err」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw err;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「6f8a0111b4b52a296f3abc51」先于语句位置「1」的操作「f81e65eb63b9a5ad5c2d02eb」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/job/job-store.ts:432`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/280`。

### `server/services/job/job-store.ts::retryUpdate.&lt;loop@433:2&gt;.&lt;block@433:39&gt;.&lt;catch@436:6&gt;.&lt;block@441:13&gt;.&lt;arrow@442:26&gt;`

在调用形式「setTimeout」中提供第 1 个实参「r」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`server/services/job/job-store.ts:442`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/281`。

### `server/services/job/job-store.ts::getJobAndUpdateIndex`

将「async () =&gt; {\n    const state = await getJob(cpbRoot, project, jobId, { dataRoot });\n    return updateJobsIndexEntry(cpbRoot, project, jobId, state, { dataRoot });\n  }」作为第 1 个实参交给已绑定接口「ts:server/services/job/job-store#retryUpdate」，对应捕获形参「fn: () =&gt; Promise&lt;T&gt;」。该普通调用关系不替代进程或网络协议关系。 以「return retryUpdate(async () =&gt; {\n    const state = await getJob(cpbRoot, project, jobId, { dataRoot });\n    return updateJobsIndexEntry(cpbRoot, project, jobId, state, { dataRoot });\n  });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`server/services/job/job-store.ts:473`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/282`。

### `server/services/job/job-store.ts::getJobAndUpdateIndex.&lt;arrow@474:21&gt;`

构造捕获记录，字段按源码次序为「dataRoot ← dataRoot」。不据构造形式推断物理持久化。 将「{ dataRoot }」作为第 4 个实参交给已绑定接口「ts:server/services/job/job-store#getJob」，对应捕获形参「{ dataRoot }: RuntimePathOptions = {}」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「state」的初始化来源为「await getJob(cpbRoot, project, jobId, { dataRoot })」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return updateJobsIndexEntry(cpbRoot, project, jobId, state, { dataRoot });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「dataRoot」关联路径「dataRoot」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「a91d34d69e2ca663930ab324」先于语句位置「1」的操作「b6037fcf6ed40292c1de4812」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「{ dataRoot }」作为第 5 个实参交给已绑定接口「ts:server/services/job/job-store#updateJobsIndexEntry」，对应捕获形参「opts: IndexOpts = {}」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/job/job-store.ts:474`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/283`。

### `server/services/job/job-store.ts::createJob`

构造捕获记录，字段按源码次序为「type ← "agent_routing_decision"；jobId ← jobId；project ← project；role ← "executor"；category ← executorSelection.category；workflow ← selectedWorkflow；preferredAgent ← executorSelection.preferredAgent；selectedAgent ← executorSelection.selectedAgent；fallbackAgent ← executorSelection.fallbackAgent；fallbackAllowed ← executorSelection.fallbackAllowed；fallbackApplied ← executorSelection.fallbackApplied；reason ← executorSelection.reason」；其余字段见完整操作。不据构造形式推断物理持久化。 将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/event/event-store#appendEvent」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「event.executorSelection = executorSelection」，捕获目标为「event.executorSelection」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「selectedWorkflow」的初始化来源为「workflow」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「selectedWorkflow」存在源更新「selectedWorkflow = routingSelection.workflow || selectedWorkflow」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!valid)」的捕获提前退出分支为「throw：new Error(`invalid team policy: ${errors.join("; ")}`)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new Error(`invalid team policy: ${errors.join("; ")}`);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/job/job-store#getJob」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/job/job-store.ts:508`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/284`。

### `server/services/job/job-store.ts::getJob`

构造捕获记录，字段按源码次序为「dataRoot ← dataRoot」。不据构造形式推断物理持久化。 将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/event/event-store#readJobProjection」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「opts」的初始化来源为「{ dataRoot }」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return (await readJobProjection(cpbRoot, project, jobId, opts)).state as JobState;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「dataRoot」关联路径「dataRoot」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「e002598d78a510102a4d8fc6」先于语句位置「1」的操作「c37f620a70e2ad785bf1bdf7」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/job/job-store.ts:1359`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/285`。

### `server/services/job/job-store.ts::getJobByQueueEntryId`

构造捕获记录，字段按源码次序为「project ← project；dataRoot ← dataRoot」。不据构造形式推断物理持久化。 将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/job/job-store#listJobs」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「jobs」的初始化来源为「await listJobs(cpbRoot, { project, dataRoot })」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!queueEntryId)」的捕获提前退出分支为「return：null」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return null;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「project」关联路径「project」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「56fdf44f79482d532d2c8e0a」先于语句位置「1」的操作「0c852330cff6629f0142d3cc」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/job/job-store.ts:1374`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/286`。

### `server/services/job/job-store.ts::isTerminal`

在调用形式「TERMINAL_STATUSES.has」中提供第 1 个实参「job.status || ""」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return !job?.jobId || TERMINAL_STATUSES.has(job.status || "");」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`server/services/job/job-store.ts:1407`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/287`。

### `server/services/job/job-store.ts::isRecoverable`

将「job」作为第 1 个实参交给已绑定接口「ts:server/services/job/job-store#isTerminal」，对应捕获形参「job: TerminalStatusProbe | null | undefined」。该普通调用关系不替代进程或网络协议关系。 条件「(!isTerminal(job))」的捕获提前退出分支为「return：false」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return false;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「5be12077b39a6a93ed32014e」先于语句位置「1」的操作「6c7df61e93c473d92139a345」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/job/job-store.ts:1411`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/288`。

### `server/services/job/job-store.ts::recoverAsNewJob`

构造捕获记录，字段按源码次序为「mode ← useCurrentExecutor ? "use-current" : "preserve-parent"；override ← !!useCurrentExecutor；parentRoot ← parentExecutorRef.root；selectedRoot ← selectedExecutorRef.root；parentReleaseId ← parentExecutorRef.releaseId；selectedReleaseId ← selectedExecutorRef.releaseId」。不据构造形式推断物理持久化。 将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/job/job-store#getJob」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「dataRoot」的初始化来源为「runtimeOpts.dataRoot」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!original?.jobId)」的捕获提前退出分支为「throw：new Error(`job not found: ${jobId}`)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new Error(`job not found: ${jobId}`);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「parentExecutorRef.root」关联路径「parentExecutorRef.root」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「1」的操作「130b35066e9a2441f3c5088c」先于语句位置「2」的操作「78f3ae71737c34c62b3bdbd8」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「original」作为第 1 个实参交给已绑定接口「ts:server/services/job/job-store#isTerminal」，对应捕获形参「job: TerminalStatusProbe | null | undefined」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/job/job-store.ts:1425`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/289`。

### `server/services/review/review-dispatch.ts::withHeldWorkflowLockRelease`

构造捕获记录，字段按源码次序为「cause ← primaryError」。不据构造形式推断物理持久化。 将「lockDir」作为第 1 个实参交给已绑定接口「ts:server/services/review/review-dispatch#releaseHeldWorkflowLock」，对应捕获形参「lockDir: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「primaryError」的初始化来源为「null」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「primaryError」存在源更新「primaryError = error」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!releaseError)」的捕获提前退出分支为「throw：primaryError」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw primaryError;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「primaryError」关联路径「primaryError」；只描述捕获来源，不证明当时的字段值。

源码：`server/services/review/review-dispatch.ts:4282`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/290`。

### `server/services/review/review-dispatch.ts::recordRemediationEvent`

将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/event/event-store#appendEvent」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「state」的初始化来源为「materializeJobRem(await readEventsRem(cpbRoot, project, jobId, options))」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留同一块中的正常源码顺序：语句位置「0」的操作「e4d5dee398b29b2006b6468f」先于语句位置「1」的操作「4cd25856ab190e6b1bf09ea3」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/event/event-store#readEvents」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。 将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/job/job-store#updateJobsIndexEntry」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。 将「await readEventsRem(cpbRoot, project, jobId, options)」作为第 1 个实参交给已绑定接口「ts:server/services/event/event-materializer#materializeJob」，对应捕获形参「events: EventRecord[]」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/review/review-dispatch.ts:4339`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/291`。

### `server/services/review/review-dispatch.ts::completeRemediation`

将「lockDir」作为第 1 个实参交给已绑定接口「ts:server/services/review/review-dispatch#withHeldWorkflowLockRelease」，对应捕获形参「lockDir: string」。该普通调用关系不替代进程或网络协议关系。 条件「(!lockDir)」的捕获提前退出分支为「throw：workflowLockError(\n      `Remediation for ${project}/${jobId} requires its exact lock lease`,\n      "REVIEW_WORKFLOW_LOCK_OWNERSHIP_UNAVAILABLE",\n      explicitDataRoot\n        ? path.join(path.resolve(explicitDataRoot), "remediation-locks", project, `${jobId}.lock`)\n        : `project-runtime-root/remediation-locks/${project}/${jobId}.lock`,\n    )」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw workflowLockError(\n      `Remediation for ${project}/${jobId} requires its exact lock lease`,\n      "REVIEW_WORKFLOW_LOCK_OWNERSHIP_UNAVAILABLE",\n      explicitDataRoot\n        ? path.join(path.resolve(explicitDataRoot), "remediation-locks", project, `${jobId}.lock`)\n        : `project-runtime-root/remediation-locks/${project}/${jobId}.lock`,\n   …［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`server/services/review/review-dispatch.ts:4398`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/292`。

### `server/services/review/review-dispatch.ts::completeRemediation.&lt;arrow@4408:61&gt;`

构造捕获记录，字段按源码次序为「type ← "external_remediation_failed"；jobId ← jobId；project ← project；artifact ← remediationArtifact；file ← remediationFile；error ← error || "unknown error"；ts ← new Date().toISOString()」。不据构造形式推断物理持久化。 将「{ project, jobId, remediationArtifact, remediationStatus, executorRoot, dataRoot }」作为第 2 个实参交给已绑定接口「ts:server/services/review/review-dispatch#createRemediationLineageTask」，对应捕获形参「{ project, jobId, remediationArtifact, remediationStatus, executorRoot, dataRoot }: LineageTaskOptions」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「dataRoot」的初始化来源为「await resolveRemediationDataRoot(cpbRoot, project, {\n      hubRoot,\n      dataRoot: explicitDataRoot,\n      lockDir,\n    })」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「remediationContent」存在源更新「remediationContent = await readFileRem(remediationFile, "utf8")」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!remediationStatus)」的捕获提前退出分支为「throw：new Error("invalid remediation status")」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「hubRoot」关联路径「hubRoot」；只描述捕获来源，不证明当时的字段值。 将「{\n        type: "external_remediation_failed",\n        jobId,\n        project,\n        artifact: remediationArtifact,\n        file: remediationFile,\n        error: error || "unknown error",\n        ts: new Date().toISOString(),\n      }」作为第 4 个实参交给已绑定接口「ts:server/services/review/review-dispatch#recordRemediationEvent」，对应捕获形参「event: LooseRecord」。该普通调用关系不替代进程或网络协议关系。

条件「(status === "failed")」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。

源码：`server/services/review/review-dispatch.ts:4408`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/293`。

### `server/services/review/review-dispatch.ts::parseRemediationStatus`

在调用形式「content.split」中提供第 1 个实参「/\r?\n/」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「firstLine」的初始化来源为「content.split(/\r?\n/)[0] || ""」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(status === "FIXED" || status === "NOOP" || status === "BLOCKED")」的捕获提前退出分支为「return：status」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return status;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「a8ef3555e5148908a6325de4」先于语句位置「1」的操作「31a611f5276b797c11c4ca59」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/review/review-dispatch.ts:4477`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/294`。

### `server/services/review/review-dispatch.ts::markJobSuperseded`

构造捕获记录，字段按源码次序为「type ← "job_superseded"；jobId ← jobId；project ← project；reason ← "external_remediation_fixed"；ts ← new Date().toISOString()」。不据构造形式推断物理持久化。 将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/event/event-store#readEvents」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「state.status = "superseded"」，捕获目标为「state.status」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「state」的初始化来源为「materializeJobRem(await readEventsRem(cpbRoot, project, jobId, options))」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以字段投影形式「jobId」关联路径「jobId」；只描述捕获来源，不证明当时的字段值。 记录消息形状中的固定文本字段「type」及捕获形式「"job_superseded"」。单个文本字段不是跨语言调用或传输成功的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「2d1d4cef82106f7b2f2c6a7f」先于语句位置「1」的操作「958b32e43f424532447f9fe8」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/job/job-store#updateJobsIndexEntry」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/review/review-dispatch.ts:4485`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/295`。

### `server/services/review/review-dispatch.ts::createRemediationLineageTask`

构造捕获记录，字段按源码次序为「projectId ← project；sourcePath ← sourcePath；sessionId ← origin?.sessionId || null；workerId ← origin?.workerId || null；cwd ← origin?.cwd || sourcePath；executionBoundary ← origin?.executionBoundary || "worktree"；type ← origin?.type || "pipeline"；priority ← origin?.priority || "P2"；description ← job.task；metadata ← {\n      ...(origin?.metadata || {}),\n      originJobId: jobId,\n      originQueueEntryId: origin?.id || null,\n      remediationArtifact,\n      remediationSt…［展示截断；完整操作保留］」。不据构造形式推断物理持久化。 将「cpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/event/event-store#readEvents」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「metaFile」的初始化来源为「path.join(dataRoot, "wiki", "project.json")」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「sourcePath」存在源更新「sourcePath = meta.sourcePath || ""」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!dataRoot)」的捕获提前退出分支为「throw：new Error("dataRoot is required for remediation lineage")」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new Error("dataRoot is required for remediation lineage");」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「dataRoot」关联路径「dataRoot」；只描述捕获来源，不证明当时的字段值。 将「{ projectId: project }」作为第 2 个实参交给已绑定接口「ts:server/services/hub/hub-queue#listQueue」，对应捕获形参「{ status, projectId }: QueueEntryInput = {}」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/review/review-dispatch.ts:4500`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/296`。

### `server/services/review/review-dispatch.ts::createRemediationLineageTask.&lt;block@4509:6&gt;.&lt;arrow@4513:6&gt;`

捕获 binding「candidate」的初始化来源为「j as LooseRecord」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return candidate &amp;&amp; candidate.task === job.task &amp;&amp; candidate.status === "completed" &amp;&amp; candidate.project === project;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「a302827c6bcc197c6f4751b3」先于语句位置「1」的操作「53f98e67ba0526f8cd94529d」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/review/review-dispatch.ts:4513`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/297`。

### `server/services/runtime.ts::countJobsIndexDivergenceForRoot`

构造捕获的空记录「{}」；没有从空记录形式推断额外字段或持久效果。 将「events」作为第 1 个实参交给已绑定接口「ts:server/services/event/event-materializer#materializeJob」，对应捕获形参「events: EventRecord[]」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「key」的初始化来源为「`${project}/${jobId}`」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「index」存在源更新「index = null」；循环和分支条件见操作上下文，未推执行次数或最终数值。 以「return 0;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「2」的操作「5e2b846b322874428c90b776」先于语句位置「3」的操作「941516aebbbe085a0bdbda40」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/runtime.ts:216`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/298`。

### `server/services/runtime.ts::classifyJobsIndexDivergence`

将「reconcileEvidence」作为第 1 个实参交给已绑定接口「ts:shared/types#recordValue」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「historyEntries」的初始化来源为「Array.isArray(history)\n    ? history.filter((entry): entry is LooseRecord =&gt; entry !== null &amp;&amp; typeof entry === "object" &amp;&amp; !Array.isArray(entry))\n    : []」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(count &lt;= 0)」的捕获提前退出分支为「return："ok"」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return "ok";」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「32af3bb366c6551a5501fce7」先于语句位置「1」的操作「21826962bebf8344e222080d」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/runtime.ts:312`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/299`。

### `server/services/runtime.ts::classifyJobsIndexDivergence.&lt;arrow@314:21&gt;`

在调用形式「Array.isArray」中提供第 1 个实参「entry」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`server/services/runtime.ts:314`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/300`。

### `server/services/runtime.ts::classifyJobsIndexDivergence.&lt;arrow@317:31&gt;`

在调用形式「Array.isArray」中提供第 1 个实参「entry」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`server/services/runtime.ts:317`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/301`。

### `server/services/runtime.ts::collectRuntimeHealth`

构造捕获记录，字段按源码次序为「ok ← blockers.length === 0；sourceVersion ← sourceVersion；activeReleaseVersion ← activeReleaseVersion || null；launcherReleaseVersion ← launcherReleaseVersion || null；initialized ← Boolean(initialized)；hubOrchestratorStatus ← hubOrchestratorStatus；queueBlockingCounts ← queueBlockingCounts；staleJobs ← staleJobList.length；jobsIndexDivergence ← {\n      count: Number(divergenceCount) || 0,\n      severity: jobsIndexSeverity,\n    }；blockers ← blockers；warnings ← warnings」。不据构造形式推断物理持久化。 将「{\n    history,\n    reconcileEvidence,\n  }」作为第 2 个实参交给已绑定接口「ts:server/services/runtime#classifyJobsIndexDivergence」，对应捕获形参「{ history = [], reconcileEvidence = null }: LooseRecord = {}」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「resolvedCpbRoot」的初始化来源为「path.resolve(cpbRoot)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return {\n    ok: blockers.length === 0,\n    sourceVersion,\n    activeReleaseVersion: activeReleaseVersion || null,\n    launcherReleaseVersion: launcherReleaseVersion || null,\n    initialized: Boolean(initialized),\n    hubOrchestratorStatus,\n    queueBlockingCounts,\n    staleJobs: staleJobList.length,\n    jobsIndexDivergence: {\n      count: Number(d…［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「history」关联路径「history」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「741fcf22df902c85983a8c03」先于语句位置「1」的操作「c81ea302a434eb5b4f8e1f00」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`server/services/runtime.ts:328`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/302`。

### `server/services/runtime.ts::collectRuntimeHealth.&lt;arrow@339:59&gt;`

构造捕获记录，字段按源码次序为「initialized ← false；version ← null」。不据构造形式推断物理持久化。

源码：`server/services/runtime.ts:339`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/303`。

### `server/services/runtime.ts::collectRuntimeHealth.&lt;arrow@351:40&gt;`

将「resolvedCpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/runtime#readPackageVersion」，对应捕获形参「root: string」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/runtime.ts:351`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/304`。

### `server/services/runtime.ts::collectRuntimeHealth.&lt;arrow@353:49&gt;`

将「resolvedExecutorRoot」作为第 1 个实参交给已绑定接口「ts:server/services/runtime#readLauncherReleaseVersion」，对应捕获形参「executorRoot: string」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/runtime.ts:353`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/305`。

### `server/services/runtime.ts::collectRuntimeHealth.&lt;arrow@355:48&gt;`

将「hubRoot」作为第 1 个实参交给已绑定接口「ts:server/orchestrator/leader-lock#readLeaderStatus」，对应捕获形参「hubRoot: string」。该普通调用关系不替代进程或网络协议关系。 以「return (await readLeaderStatus(hubRoot)).status || null;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`server/services/runtime.ts:355`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/306`。

### `server/services/runtime.ts::collectRuntimeHealth.&lt;arrow@362:39&gt;`

将「hubRoot」作为第 1 个实参交给已绑定接口「ts:server/services/hub/hub-queue#loadQueue」，对应捕获形参「hubRoot: string」。该普通调用关系不替代进程或网络协议关系。 以「return (await loadQueue(hubRoot)).entries || [];」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`server/services/runtime.ts:362`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/307`。

### `server/services/runtime.ts::collectRuntimeHealth.&lt;arrow@369:51&gt;`

将「resolvedCpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/runtime#countJobsIndexDivergence」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/runtime.ts:369`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/308`。

### `server/services/runtime.ts::collectRuntimeHealth.&lt;arrow@370:36&gt;`

将「resolvedCpbRoot」作为第 1 个实参交给已绑定接口「ts:server/services/runtime#findStaleJobs」，对应捕获形参「cpbRoot: string」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/runtime.ts:370`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/309`。

### `server/services/task/task-view.ts::projectTaskView`

构造捕获记录，字段按源码次序为「schemaVersion ← TASK_VIEW_SCHEMA_VERSION；taskId ← taskId；state ← projected.state；summary ← summary；progress ← progress；checks ← checks；changedFiles ← changedFiles；nextAction ← nextAction；createdAt ← createdAt；updatedAt ← updatedAt」。不据构造形式推断物理持久化。 将「{\n      dataRoot: opts.dataRoot,\n    }」作为第 4 个实参交给已绑定接口「ts:server/services/job/job-store#getJobByQueueEntryId」，对应捕获形参「{ dataRoot }: RuntimePathOptions = {}」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「entries」的初始化来源为「(queue as LooseRecord)?.entries」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「job」存在源更新「job = null」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(typeof taskId !== "string" || !taskId)」的捕获提前退出分支为「return：null」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return null;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「opts.dataRoot」关联路径「opts.dataRoot」；只描述捕获来源，不证明当时的字段值。 将「hubRoot」作为第 1 个实参交给已绑定接口「ts:server/services/hub/hub-queue#loadQueue」，对应捕获形参「hubRoot: string」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/task/task-view.ts:615`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/310`。

### `server/services/task/task-view.ts::projectTaskView.&lt;arrow@628:21&gt;`

将「e」作为第 1 个实参交给已绑定接口「ts:core/contracts/types#isRecord」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/task/task-view.ts:628`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/311`。

### `server/services/task/task-view.ts::projectTaskView.&lt;arrow@636:19&gt;`

将「e.id」作为第 1 个实参交给已绑定接口「ts:server/services/task/task-view#stringValue」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。

源码：`server/services/task/task-view.ts:636`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/312`。

### `shared/fs-utils.ts::jsonContent`

在调用形式「JSON.stringify」中提供第 1 个实参「data」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return typeof data === "string" ? data : `${JSON.stringify(data, null, 2)}\n`;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`shared/fs-utils.ts:91`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/313`。

### `shared/fs-utils.ts::tempPathFor`

在调用形式「path.dirname」中提供第 1 个实参「filePath」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return path.join(path.dirname(filePath), `.${path.basename(filePath)}.tmp-${randomUUID()}`);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`shared/fs-utils.ts:95`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/314`。

### `shared/fs-utils.ts::writeJsonAtomic`

构造捕获记录，字段按源码次序为「committed ← null；renameCommitted ← null」。不据构造形式推断物理持久化。 将「data」作为第 1 个实参交给已绑定接口「ts:shared/fs-utils#jsonContent」，对应捕获形参「data: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「content」的初始化来源为「jsonContent(data)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「renameCommitted」存在源更新「renameCommitted = sourceGeneration === null\n          &amp;&amp; destinationGeneration !== null\n          &amp;&amp; temporaryGeneration !== null\n          &amp;&amp; sameFileGenerationAcrossRename(temporaryGeneration, destinationGeneration)」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(closeErrors.length &gt; 0)」的捕获提前退出分支为「throw：closeErrors[0]」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw closeErrors[0];」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「14cdfd19833bb99def12311c」先于语句位置「1」的操作「59baac3c7fb580574ed849d5」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「filePath」作为第 1 个实参交给已绑定接口「ts:shared/fs-utils#tempPathFor」，对应捕获形参「filePath: string」。该普通调用关系不替代进程或网络协议关系。

源码：`shared/fs-utils.ts:325`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/315`。

### `shared/hub-maintenance.ts::writeJsonDurableAtomic`

构造捕获记录，字段按源码次序为「code ← publicationRace\n            ? "DURABLE_JSON_COMMITTED_PUBLICATION_RACE"\n            : "DURABLE_JSON_COMMITTED_DURABILITY_AMBIGUOUS"；primaryError ← primaryError；cleanupErrors ← cleanupErrors；committed ← true；filePath ← filePath；committedPath ← filePath；successorPreserved ← publicationRace；recoveryPaths ← publicationRace ? { filePath, parent } : [filePath, parent]」。不据构造形式推断物理持久化。 将「filePath」作为第 1 个实参交给已绑定接口「ts:shared/hub-maintenance#isolateFailedTemp」，对应捕获形参「filePath: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「tempInfo」的初始化来源为「await handle.stat()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「primaryError」存在源更新「primaryError = error」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(typeof constants.O_NOFOLLOW !== "number" || constants.O_NOFOLLOW === 0)」的捕获提前退出分支为「throw：Object.assign(new Error(`no-follow temp publication is unavailable: ${tempPath}`), {\n      code: "DURABLE_JSON_TEMP_UNSAFE",\n      committed: false,\n    })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw Object.assign(new Error(`no-follow temp publication is unavailable: ${tempPath}`), {\n      code: "DURABLE_JSON_TEMP_UNSAFE",\n      committed: false,\n    });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「filePath」关联路径「filePath」；只描述捕获来源，不证明当时的字段值。

源码：`shared/hub-maintenance.ts:710`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/316`。

### `shared/hub-maintenance.ts::writeJsonDurableAtomic.&lt;block@833:20&gt;.&lt;arrow@872:46&gt;`

将「error」作为第 1 个实参交给已绑定接口「ts:shared/hub-maintenance#errnoCode」，对应捕获形参「error: unknown」。该普通调用关系不替代进程或网络协议关系。

源码：`shared/hub-maintenance.ts:872`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/317`。

### `shared/orchestrator/assignment-store.ts::normalizeJsonValue`

构造捕获记录，字段按源码次序为「cause ← cause」。不据构造形式推断物理持久化。 在调用形式「Object.assign」中提供第 2 个实参「{\n      code: "HUB_ASSIGNMENT_JSON_INVALID",\n    }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「normalized」的初始化来源为「JSON.parse(serialized) as unknown」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「cloned」存在源更新「cloned = structuredClone(value)」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(serialized === undefined)」的捕获提前退出分支为「throw：Object.assign(new TypeError(`${label} must serialize to JSON`), {\n      code: "HUB_ASSIGNMENT_JSON_INVALID",\n    })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw Object.assign(new TypeError(`${label} must serialize to JSON`), {\n      code: "HUB_ASSIGNMENT_JSON_INVALID",\n    });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「cause」关联路径「cause」；只描述捕获来源，不证明当时的字段值。

源码：`shared/orchestrator/assignment-store.ts:362`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/318`。

### `shared/orchestrator/assignment-store.ts::AssignmentStore.constructor`

在调用形式「path.resolve」中提供第 1 个实参「hubRoot」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 包含赋值/更新「this.hubRoot = path.resolve(hubRoot)」，捕获目标为「this.hubRoot」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「24147eaeb350f2dadb46c770」先于语句位置「1」的操作「1fbb91876e79cd48459e5812」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`shared/orchestrator/assignment-store.ts:481`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/319`。

### `shared/orchestrator/assignment-store.ts::AssignmentStore.getOrCreateAssignmentForEntry`

在调用形式「String」中提供第 1 个实参「entryId」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「entryIdText」的初始化来源为「String(entryId)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return this._withAssignmentLock(id, async () =&gt; {\n      // Preserve existing assignment on retry/reroute — don't reset attempt history\n      const existing = await this._readStateFile(id);\n      if (existing) {\n        const updated = {\n          ...existing,\n          // Update mutable fields (may change on reroute)\n          workflow: workflow || ex…［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「3ea31b6659d698ccf4290648」先于语句位置「1」的操作「5908acaf25bd97fd4b1140d3」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`shared/orchestrator/assignment-store.ts:495`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/320`。

### `shared/orchestrator/assignment-store.ts::AssignmentStore.getOrCreateAssignmentForEntry.&lt;arrow@499:40&gt;`

构造捕获记录，字段按源码次序为「assignmentId ← id；entryId ← entryIdText；projectId ← projectId；projectRuntimeRoot ← projectRuntimeRoot；task ← task；sourcePath ← sourcePath；workflow ← workflow || "standard"；planMode ← planMode || "full"；sourceContext ← recordValue(sourceContext)；metadata ← recordValue(metadata)；status ← "scheduled"；createdAt ← new Date().toISOString()」；其余字段见完整操作。不据构造形式推断物理持久化。 将「{ ...assignment, attempts: 0 }」作为第 2 个实参交给已绑定接口「ts:shared/fs-utils#writeJsonAtomic」，对应捕获形参「data: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「updated」的初始化来源为「{\n          ...existing,\n          // Update mutable fields (may change on reroute)\n          workflow: workflow || existing.workflow,\n          planMode: planMode || existing.planMode,\n          sourceContext: { ...recordValue(existing.sourceContext), ...recordValue(sourceContext) },\n          task: task || existing.task,\n          sourcePath: source…［展示截断；完整操作保留］」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(existing)」的捕获提前退出分支为「return：updated」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return updated;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「id」关联路径「id」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「existing」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。 将「existing.sourceContext」作为第 1 个实参交给已绑定接口「ts:shared/types#recordValue」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。

源码：`shared/orchestrator/assignment-store.ts:499`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/321`。

### `shared/orchestrator/assignment-store.ts::AssignmentStore.createAttempt`

在调用形式「this._withAssignmentLock」中提供第 1 个实参「assignmentId」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return this._withAssignmentLock(assignmentId, async () =&gt; {\n      const state = await this._readStateFile(assignmentId);\n      if (!state) throw new Error(`assignment not found: ${assignmentId}`);\n      const previousAttempts = typeof state.attempts === "number" ? state.attempts : 0;\n      const attemptNum = previousAttempts + 1;\n      const attemptDir …［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`shared/orchestrator/assignment-store.ts:553`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/322`。

### `shared/orchestrator/assignment-store.ts::AssignmentStore.createAttempt.&lt;arrow@554:50&gt;`

构造捕获记录，字段按源码次序为「assignmentId ← assignmentId；attempt ← attemptNum；entryId ← String(state.entryId || "")；projectId ← String(state.projectId || "")；workerId ← normalizedWorkerId；status ← "assigned"；orchestratorEpoch ← typeof orchestratorEpoch === "number" ? orchestratorEpoch : undefined；attemptToken ← attemptToken；createdAt ← new Date().toISOString()」。不据构造形式推断物理持久化。 将「attempt」作为第 2 个实参交给已绑定接口「ts:shared/fs-utils#writeJsonAtomic」，对应捕获形参「data: unknown」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「state.attempts = attemptNum」，捕获目标为「state.attempts」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「state」的初始化来源为「await this._readStateFile(assignmentId)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!state)」的捕获提前退出分支为「throw：new Error(`assignment not found: ${assignmentId}`)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new Error(`assignment not found: ${assignmentId}`);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「assignmentId」关联路径「assignmentId」；只描述捕获来源，不证明当时的字段值。

源码：`shared/orchestrator/assignment-store.ts:554`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/323`。

### `shared/orchestrator/assignment-store.ts::AssignmentStore._readStateFile`

将「state」作为第 1 个实参交给已绑定接口「ts:shared/types#recordValue」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「state」的初始化来源为「await this._readLocalJsonObject(\n      path.join(this.baseDir, assignmentId, "state.json"),\n      "assignment state",\n    )」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return state ? recordValue(state) as AssignmentRecord : null;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「9ca6da4551b843e3c1368e5f」先于语句位置「1」的操作「21d50186b4a93ee4831bb97d」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`shared/orchestrator/assignment-store.ts:730`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/324`。

### `shared/orchestrator/assignment-store.ts::AssignmentStore.getAssignment`

在调用形式「this._readState」中提供第 1 个实参「assignmentId」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return this._readState(assignmentId);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`shared/orchestrator/assignment-store.ts:1299`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/325`。

### `shared/orchestrator/assignment-store.ts::AssignmentStore.listAssignments`

在调用形式「readdir」中提供第 1 个实参「this.baseDir」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「state」的初始化来源为「await this._readState(dir)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return entries;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「9d45589c095e4165adcaa1f3」先于语句位置「1」的操作「ddbf03fa19ee77d70de10b9d」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`shared/orchestrator/assignment-store.ts:1333`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/326`。

### `shared/orchestrator/assignment-store.ts::AssignmentStore._writeState`

将「state」作为第 2 个实参交给已绑定接口「ts:shared/fs-utils#writeJsonAtomic」，对应捕获形参「data: unknown」。该普通调用关系不替代进程或网络协议关系。

源码：`shared/orchestrator/assignment-store.ts:1354`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/327`。

### `shared/orchestrator/assignment-store.ts::AssignmentStore._withAssignmentLock`

构造捕获记录，字段按源码次序为「schemaVersion ← ASSIGNMENT_OWNER_SCHEMA_VERSION；assignmentId ← assignmentId；ownerToken ← ownerToken；pid ← process.pid；host ← os.hostname()；acquiredAt ← new Date().toISOString()；processIdentity ← processIdentity」。不据构造形式推断物理持久化。 将「{\n        schemaVersion: ASSIGNMENT_OWNER_SCHEMA_VERSION,\n        assignmentId,\n        ownerToken,\n        pid: process.pid,\n        host: os.hostname(),\n        acquiredAt: new Date().toISOString(),\n        processIdentity,\n      }」作为第 2 个实参交给已绑定接口「ts:shared/hub-maintenance#writeJsonDurableAtomic」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「attempt」的初始化来源为「0」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「primaryError」存在源更新「primaryError = error」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!processIdentity)」的捕获提前退出分支为「throw：assignmentLockConflict(`assignment lock process identity unavailable: ${assignmentId}`)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw assignmentLockConflict(`assignment lock process identity unavailable: ${assignmentId}`);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「options.signal」关联路径「options.signal」；只描述捕获来源，不证明当时的字段值。

源码：`shared/orchestrator/assignment-store.ts:1426`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/328`。

### `shared/orchestrator/assignment-store.ts::AssignmentStore._withAssignmentLock.&lt;loop@1452:4&gt;.&lt;block@1452:75&gt;.&lt;arrow@1454:58&gt;`

构造捕获记录，字段按源码次序为「schemaVersion ← ASSIGNMENT_OWNER_SCHEMA_VERSION；ownerToken ← ownerToken；pid ← process.pid；host ← os.hostname()；acquiredAt ← new Date().toISOString()；processIdentity ← processIdentity」。不据构造形式推断物理持久化。 将「{ syncParentDirectory: syncAssignmentDirectory }」作为第 3 个实参交给已绑定接口「ts:shared/hub-maintenance#writeJsonDurableAtomic」，对应捕获形参「options: WriteJsonDurableAtomicOptions = {}」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「cleanupError」的初始化来源为「null」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「cleanupError」存在源更新「cleanupError = error」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(errorCode(error) !== "EEXIST")」的捕获提前退出分支为「throw：error」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw error;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「lockDir」关联路径「lockDir」；只描述捕获来源，不证明当时的字段值。

源码：`shared/orchestrator/assignment-store.ts:1454`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/329`。

### `shared/orchestrator/worker-broker-client.ts::brokerResult`

将「`worker broker ${op} success response must declare ok=true`」作为第 1 个实参交给已绑定接口「ts:shared/orchestrator/worker-broker-client#contractError」，对应捕获形参「message: string」。该普通调用关系不替代进程或网络协议关系。 条件「(payload.ok !== true)」的捕获提前退出分支为「throw：contractError(`worker broker ${op} success response must declare ok=true`)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw contractError(`worker broker ${op} success response must declare ok=true`);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「1」的操作「886dafb2763e9c1a09fa28cc」先于语句位置「2」的操作「85d364048d5fccc5c2df42ac」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`shared/orchestrator/worker-broker-client.ts:24`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/330`。

### `shared/orchestrator/worker-broker-client.ts::recordResult`

将「value」作为第 1 个实参交给已绑定接口「ts:shared/types#isRecord」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 条件「(!isRecord(value))」的捕获提前退出分支为「throw：contractError(`worker broker ${op} result must be an object`)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw contractError(`worker broker ${op} result must be an object`);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「34f3ff9ad9baaf0b1a4e08a6」先于语句位置「1」的操作「9841167364f681ff1747da9f」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`shared/orchestrator/worker-broker-client.ts:34`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/331`。

### `shared/orchestrator/worker-broker-client.ts::inboxClaimsResult`

将「`worker broker ${op} result must be an array`」作为第 1 个实参交给已绑定接口「ts:shared/orchestrator/worker-broker-client#contractError」，对应捕获形参「message: string」。该普通调用关系不替代进程或网络协议关系。 条件「(!Array.isArray(value))」的捕获提前退出分支为「throw：contractError(`worker broker ${op} result must be an array`)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw contractError(`worker broker ${op} result must be an array`);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「0612f2d2693b3ff2e01e4bba」先于语句位置「1」的操作「92b5e188b079d3f0285d6df5」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`shared/orchestrator/worker-broker-client.ts:81`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/332`。

### `shared/orchestrator/worker-broker-client.ts::inboxClaimsResult.&lt;arrow@83:19&gt;`

将「claim.assignment」作为第 1 个实参交给已绑定接口「ts:shared/types#isRecord」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「claim」的初始化来源为「recordResult(candidate, `${op}[${index}]`)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(typeof claim.assignmentId !== "string" || !claim.assignmentId\n      || typeof claim.claimToken !== "string" || !claim.claimToken\n      || !isRecord(claim.assignment))」的捕获提前退出分支为「throw：contractError(`worker broker ${op}[${index}] requires assignmentId, claimToken, and assignment`)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw contractError(`worker broker ${op}[${index}] requires assignmentId, claimToken, and assignment`);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「6eac92bb9ba0ee97adce3b5a」先于语句位置「1」的操作「18e7cd53b0fb38476c7da963」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「candidate」作为第 1 个实参交给已绑定接口「ts:shared/orchestrator/worker-broker-client#recordResult」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。

源码：`shared/orchestrator/worker-broker-client.ts:83`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/333`。

### `shared/orchestrator/worker-broker-client.ts::WorkerBrokerClient.constructor`

将「endpoint.hostname」作为第 1 个实参交给已绑定接口「ts:shared/network#isLoopbackHost」，对应捕获形参「host: string」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「endpoint.pathname = "/internal/worker-state"」，捕获目标为「endpoint.pathname」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「endpoint」的初始化来源为「new URL(credentials.url)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(endpoint.protocol !== "https:" &amp;&amp; !(endpoint.protocol === "http:" &amp;&amp; isLoopbackHost(endpoint.hostname)))」的捕获提前退出分支为「throw：new Error("worker broker URL must use HTTPS or loopback HTTP")」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new Error("worker broker URL must use HTTPS or loopback HTTP");」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「9729d3e02774f7dcd58fbd74」先于语句位置「1」的操作「0c915ad4427fa2c0a33b8a71」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`shared/orchestrator/worker-broker-client.ts:109`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/334`。

### `shared/orchestrator/worker-broker-client.ts::WorkerBrokerClient.#call`

构造捕获记录，字段按源码次序为「method ← "POST"；headers ← {\n        authorization: `Bearer ${this.#token}`,\n        "content-type": "application/json",\n      }；body ← JSON.stringify({\n        workerId: this.#workerId,\n        incarnationToken: this.#incarnationToken,\n        op,\n        args,\n      })；signal ← AbortSignal.timeout(15_000)」。不据构造形式推断物理持久化。 将「payloadValue」作为第 1 个实参交给已绑定接口「ts:shared/types#isRecord」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「response」的初始化来源为「await this.#fetch(this.#url, {\n      method: "POST",\n      headers: {\n        authorization: `Bearer ${this.#token}`,\n        "content-type": "application/json",\n      },\n      body: JSON.stringify({\n        workerId: this.#workerId,\n        incarnationToken: this.#incarnationToken,\n        op,\n        args,\n      }),\n      signal: AbortSignal.ti…［展示截断；完整操作保留］」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!response.ok)」的捕获提前退出分支为「throw：Object.assign(new Error(String(payload.message || "worker broker request failed")), {\n        code: typeof payload.code === "string" ? payload.code : "HUB_WORKER_BROKER_UNAVAILABLE",\n        statusCode: response.status,\n      })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw Object.assign(new Error(String(payload.message || "worker broker request failed")), {\n        code: typeof payload.code === "string" ? payload.code : "HUB_WORKER_BROKER_UNAVAILABLE",\n        statusCode: response.status,\n      });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「op」关联路径「op」；只描述捕获来源，不证明当时的字段值。 记录消息形状中的固定文本字段「method」及捕获形式「"POST"」。单个文本字段不是跨语言调用或传输成功的证明。 将「payload」作为第 1 个实参交给已绑定接口「ts:shared/orchestrator/worker-broker-client#brokerResult」，对应捕获形参「payload: LooseRecord」。该普通调用关系不替代进程或网络协议关系。

源码：`shared/orchestrator/worker-broker-client.ts:125`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/335`。

### `shared/orchestrator/worker-broker-client.ts::WorkerBrokerClient.#call.&lt;arrow@140:62&gt;`

构造捕获的空记录「{}」；没有从空记录形式推断额外字段或持久效果。

源码：`shared/orchestrator/worker-broker-client.ts:140`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/336`。

### `shared/orchestrator/worker-broker-client.ts::WorkerBrokerClient.claimInboxEntries`

在调用形式「this.#call」中提供第 1 个实参「"inbox.claim"」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return this.#call("inbox.claim").then((value) =&gt; inboxClaimsResult(value, "inbox.claim"));」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`shared/orchestrator/worker-broker-client.ts:154`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/337`。

### `shared/orchestrator/worker-broker-client.ts::WorkerBrokerClient.claimInboxEntries.&lt;arrow@154:107&gt;`

将「value」作为第 1 个实参交给已绑定接口「ts:shared/orchestrator/worker-broker-client#inboxClaimsResult」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。

源码：`shared/orchestrator/worker-broker-client.ts:154`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/338`。

### `shared/orchestrator/worker-store.ts::receiptClone`

在调用形式「structuredClone」中提供第 1 个实参「value」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return value === undefined ? value : structuredClone(value);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`shared/orchestrator/worker-store.ts:574`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/339`。

### `shared/orchestrator/worker-store.ts::normalizeJsonRecord`

构造捕获记录，字段按源码次序为「cause ← cause」。不据构造形式推断物理持久化。 在调用形式「structuredClone」中提供第 1 个实参「value」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「normalized」的初始化来源为「JSON.parse(serialized) as unknown」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「cloned」存在源更新「cloned = structuredClone(value)」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(serialized === undefined)」的捕获提前退出分支为「throw：Object.assign(new TypeError(`${label} must serialize to JSON`), {\n      code: "HUB_WORKER_INBOX_PAYLOAD_INVALID",\n    })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw Object.assign(new TypeError(`${label} must serialize to JSON`), {\n      code: "HUB_WORKER_INBOX_PAYLOAD_INVALID",\n    });」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「cause」关联路径「cause」；只描述捕获来源，不证明当时的字段值。

源码：`shared/orchestrator/worker-store.ts:578`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/340`。

### `shared/orchestrator/worker-store.ts::readLocalWorkerJsonAuthority`

构造捕获记录，字段按源码次序为「record ← parsed as LooseRecord；generation ← after」。不据构造形式推断物理持久化。 将「filePath」作为第 1 个实参交给已绑定接口「ts:shared/primitives/durable-directory-lock#readBoundedRegularFileNoFollow」，对应捕获形参「filePath: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「before」的初始化来源为「await observeWorkerPathGeneration(filePath, "file")」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「raw」存在源更新「raw = await readBoundedRegularFileNoFollow(filePath, { maxBytes })」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!parsed || typeof parsed !== "object" || Array.isArray(parsed))」的捕获提前退出分支为「throw：Object.assign(new Error(`${label} is not a JSON object: ${filePath}`), { code: invalidCode })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return null;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「maxBytes」关联路径「maxBytes」；只描述捕获来源，不证明当时的字段值。

条件「(!before)」的捕获提前退出分支为「return：null」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。

源码：`shared/orchestrator/worker-store.ts:711`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/341`。

### `shared/orchestrator/worker-store.ts::readLocalWorkerJsonObject`

将「filePath」作为第 1 个实参交给已绑定接口「ts:shared/orchestrator/worker-store#readLocalWorkerJsonAuthority」，对应捕获形参「filePath: string」。该普通调用关系不替代进程或网络协议关系。 以「return (await readLocalWorkerJsonAuthority(filePath, label, invalidCode, maxBytes))?.record ?? null;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`shared/orchestrator/worker-store.ts:753`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/342`。

### `shared/orchestrator/worker-store.ts::inboxReceipt`

构造捕获记录，字段按源码次序为「path ← input.path」。不据构造形式推断物理持久化。 将「input.previousRecord」作为第 1 个实参交给已绑定接口「ts:shared/orchestrator/worker-store#receiptClone」，对应捕获形参「value: T」。该普通调用关系不替代进程或网络协议关系。 以「return deepFreezeReceipt({\n    workerId: input.workerId,\n    assignmentId: input.assignmentId,\n    attempt: input.attempt,\n    attemptToken: input.attemptToken,\n    backend: input.backend,\n    ref: input.ref,\n    ...(input.path ? { path: input.path } : {}),\n    previousRecord: receiptClone(input.previousRecord),\n    committedRecord: receiptClone(inp…［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「input.workerId」关联路径「input.workerId」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「(input.path ? { path: input.path } : {})」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。

源码：`shared/orchestrator/worker-store.ts:762`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/343`。

### `shared/orchestrator/worker-store.ts::WorkerStore.constructor`

在调用形式「path.resolve」中提供第 1 个实参「hubRoot」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 包含赋值/更新「this.hubRoot = path.resolve(hubRoot)」，捕获目标为「this.hubRoot」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「a8fb8399c0ebeb70e83e36ec」先于语句位置「1」的操作「a18d215e06f742d615097374」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`shared/orchestrator/worker-store.ts:783`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/344`。

### `shared/orchestrator/worker-store.ts::WorkerStore._readLocalInboxJson`

将「filePath」作为第 1 个实参交给已绑定接口「ts:shared/orchestrator/worker-store#readLocalWorkerJsonObject」，对应捕获形参「filePath: string」。该普通调用关系不替代进程或网络协议关系。 以「return readLocalWorkerJsonObject(filePath, label, "HUB_WORKER_INBOX_PAYLOAD_INVALID");」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`shared/orchestrator/worker-store.ts:1410`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/345`。

### `shared/orchestrator/worker-store.ts::WorkerStore.writeInboxWithReceipt`

将「assignment」作为第 1 个实参交给已绑定接口「ts:shared/orchestrator/worker-store#normalizeJsonRecord」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「committedPayload」的初始化来源为「normalizeJsonRecord(assignment, "worker inbox payload")」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(!assignmentId)」的捕获提前退出分支为「throw：new Error("assignmentId is required for worker inbox")」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new Error("assignmentId is required for worker inbox");」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「e6b5d51407e93d4dcbbf2702」先于语句位置「1」的操作「28e62ac182c7c549a1b4dc9f」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`shared/orchestrator/worker-store.ts:1698`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/346`。

### `shared/orchestrator/worker-store.ts::WorkerStore.writeInboxWithReceipt.&lt;arrow@1703:60&gt;`

构造捕获记录，字段按源码次序为「workerId ← workerId；assignmentId ← assignmentId；attempt ← attempt；attemptToken ← attemptToken；backend ← "local"；ref ← filePath；path ← filePath；previousRecord ← previousRecord；committedRecord ← committedPayload；writeFence ← {\n          backend: "local",\n          ownerToken: String(committedOwner.ownerToken),\n          previousOwner,\n          committedOwner,\n          payload…［展示截断；完整操作保留］」。不据构造形式推断物理持久化。 将「stagingPath」作为第 1 个实参交给已绑定接口「ts:shared/fs-utils#writeJsonAtomic」，对应捕获形参「filePath: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「reportsCommitted」的初始化来源为「Boolean(originalError &amp;&amp; typeof originalError === "object"\n          &amp;&amp; "committed" in originalError &amp;&amp; originalError.committed === true)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「stagingGeneration」存在源更新「stagingGeneration = await observeWorkerPathGeneration(stagingPath, "file")」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!Number.isInteger(attempt) || attempt &lt; 1 || !attemptToken)」的捕获提前退出分支为「throw：new Error("attempt and attemptToken are required for worker inbox")」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new Error("attempt and attemptToken are required for worker inbox");」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「workerId」关联路径「workerId」；只描述捕获来源，不证明当时的字段值。 将「{\n        workerId,\n        assignmentId,\n        attempt,\n        attemptToken,\n        ownerToken: crypto.randomUUID(),\n        writtenAt: new Date().toISOString(),\n      }」作为第 1 个实参交给已绑定接口「ts:shared/orchestrator/worker-store#normalizeJsonRecord」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。

源码：`shared/orchestrator/worker-store.ts:1703`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/347`。

### `shared/orchestrator/worker-store.ts::WorkerStore.writeInbox`

在调用形式「this.writeInboxWithReceipt」中提供第 1 个实参「workerId」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return (await this.writeInboxWithReceipt(workerId, assignment)).committedRecord;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`shared/orchestrator/worker-store.ts:1932`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/348`。

### `shared/orchestrator/worker-store.ts::WorkerStore.claimInboxEntries`

构造捕获记录，字段按源码次序为「recursive ← true」。不据构造形式推断物理持久化。 将「dir」作为第 1 个实参交给已绑定接口「ts:shared/orchestrator/worker-store#readWorkerDirectoryNamesPinned」，对应捕获形参「directory: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「assignmentId」的初始化来源为「file.slice(0, -5)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return claims;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「b0979249b48e1a80186f9484」先于语句位置「1」的操作「53069f47a7498abbe47546dd」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`shared/orchestrator/worker-store.ts:1960`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/349`。

### `shared/orchestrator/worker-store.ts::WorkerStore.claimInboxEntries.&lt;loop@1967:4&gt;.&lt;arrow@1967:36&gt;`

在调用形式「name.endsWith」中提供第 1 个实参「".json"」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`shared/orchestrator/worker-store.ts:1967`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/350`。

### `shared/orchestrator/worker-store.ts::WorkerStore.claimInboxEntries.&lt;loop@1967:4&gt;.&lt;block@1967:71&gt;.&lt;arrow@1969:75&gt;`

构造捕获记录，字段按源码次序为「assignmentId ← assignmentId；assignment ← assignment as LooseRecord；claimToken ← claimed」。不据构造形式推断物理持久化。 将「dir」作为第 1 个实参交给已绑定接口「ts:shared/orchestrator/worker-store#syncWorkerDirectory」，对应捕获形参「directory: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「code」的初始化来源为「errorCode(error)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(errorCode(error) !== "ENOENT")」的捕获提前退出分支为「throw：new AggregateError(\n                [error, rollbackError],\n                `worker inbox claim rollback failed: ${assignmentId}`,\n              )」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return null;」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「assignmentId」关联路径「assignmentId」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「710ecc321799c7545c9ffe15」先于语句位置「1」的操作「158c83f82a17ee66675c7030」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

条件「(errorCode(error) === "ENOENT")」的捕获提前退出分支为「return：null」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。

源码：`shared/orchestrator/worker-store.ts:1969`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/351`。

### `shared/types.ts::isRecord`

在调用形式「Array.isArray」中提供第 1 个实参「value」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return value !== null &amp;&amp; typeof value === "object" &amp;&amp; !Array.isArray(value);」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`shared/types.ts:213`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/352`。

### `shared/types.ts::recordValue`

构造捕获的空记录「{}」；没有从空记录形式推断额外字段或持久效果。 将「value」作为第 1 个实参交给已绑定接口「ts:shared/types#isRecord」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 以「return isRecord(value) ? value : {};」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`shared/types.ts:217`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/353`。

**实际装配与消息接缝**（源模型与运行效果分开）：

- 所选默认装配的源模型列出动态命令 import 的候选路径「captured_path:cli/commands/pipeline.ts」。其他捕获路径分支为「symbolic_path:cli/commands/init.js；symbolic_path:cli/commands/hub.js；symbolic_path:cli/commands/pipeline.js；symbolic_path:cli/commands/fix.js；symbolic_path:cli/commands/task.js；symbolic_path:cli/commands/status.js；symbolic_path:cli/commands/list.js；symbolic_path:cli/commands/jobs.js；symbolic_path:cli/commands/retry.js；symbolic_path:cli/commands/diff.js；symbolic_path:cli/commands/review.js；symbolic_path:cli/commands/inbox.js；symbolic_path:cli/commands/setup.js；symbolic_path:cli/commands/agents.js；symbolic_path:cli/commands/github.js；symbolic_path:cli/commands/doctor.js；symbolic_path:cli/commands/stream.js；symbolic_path:cli/commands/cancel-redirect.js；symbolic_path:cli/commands/cancel-redirect.js；symbolic_path:cli/commands/version.js；symbolic_path:cli/commands/code-index.js；captured_path:cli/commands/init.js；captured_path:cli/commands/hub.js；captured_path:cli/commands/fix.js；captured_path:cli/commands/task.js；captured_path:cli/commands/status.js；captured_path:cli/commands/list.js；captured_path:cli/commands/jobs.js；captured_path:cli/commands/retry.js；captured_path:cli/commands/diff.js；captured_path:cli/commands/review.js；captured_path:cli/commands/inbox.js；captured_path:cli/commands/setup.js；captured_path:cli/commands/agents.js；captured_path:cli/commands/github.js；captured_path:cli/commands/doctor.js；captured_path:cli/commands/stream.js；captured_path:cli/commands/cancel-redirect.js；captured_path:cli/commands/cancel-redirect.js；captured_path:cli/commands/version.js；captured_path:cli/commands/code-index.js」；这是有限路径与实际形参关系，不把所有候选当必然普通调用。 原分析关系：`/judgments/0/obligations/1/evidence/production_assembly/cli/calls/0`；完整条件与来源：`/architecture/responsibility_explanations/computed_source_contract_seams/0`。
- 捕获的标准 Node spawn 导入通过实际 argv 源关系选择 worker 路径「symbolic_path:runtime/worker/managed-worker.js」；进程接线独立于普通函数 CALLS，未据此宣称进程已经启动或 worker 已执行。 原分析关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_process_starts/0`；完整条件与来源：`/architecture/responsibility_explanations/computed_source_contract_seams/1`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.claimInboxEntries；WorkerStore.claimInboxEntries」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原分析关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/0`；完整条件与来源：`/architecture/responsibility_explanations/computed_source_contract_seams/2`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.completeInboxClaim；WorkerStore.completeInboxClaim」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原分析关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/1`；完整条件与来源：`/architecture/responsibility_explanations/computed_source_contract_seams/3`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.completeInboxClaim；WorkerStore.completeInboxClaim」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原分析关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/2`；完整条件与来源：`/architecture/responsibility_explanations/computed_source_contract_seams/4`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.completeInboxClaim；WorkerStore.completeInboxClaim」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原分析关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/3`；完整条件与来源：`/architecture/responsibility_explanations/computed_source_contract_seams/5`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.completeInboxClaim；WorkerStore.completeInboxClaim」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原分析关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/4`；完整条件与来源：`/architecture/responsibility_explanations/computed_source_contract_seams/6`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.completeInboxClaim；WorkerStore.completeInboxClaim」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原分析关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/5`；完整条件与来源：`/architecture/responsibility_explanations/computed_source_contract_seams/7`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.assertActiveAttemptIdentity；AssignmentStore.assertActiveAttemptIdentity」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原分析关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/6`；完整条件与来源：`/architecture/responsibility_explanations/computed_source_contract_seams/8`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.completeInboxClaim；WorkerStore.completeInboxClaim」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原分析关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/7`；完整条件与来源：`/architecture/responsibility_explanations/computed_source_contract_seams/9`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.updateWorkerIf；WorkerStore.updateWorkerIf」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原分析关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/8`；完整条件与来源：`/architecture/responsibility_explanations/computed_source_contract_seams/10`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.updateWorkerIf；WorkerStore.updateWorkerIf」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原分析关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/9`；完整条件与来源：`/architecture/responsibility_explanations/computed_source_contract_seams/11`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.completeInboxClaim；WorkerStore.completeInboxClaim」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原分析关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/10`；完整条件与来源：`/architecture/responsibility_explanations/computed_source_contract_seams/12`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.markRunning；AssignmentStore.markRunning」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原分析关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/11`；完整条件与来源：`/architecture/responsibility_explanations/computed_source_contract_seams/13`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.assertActiveAttemptIdentity；AssignmentStore.assertActiveAttemptIdentity」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原分析关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/12`；完整条件与来源：`/architecture/responsibility_explanations/computed_source_contract_seams/14`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.completeInboxClaim；WorkerStore.completeInboxClaim」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原分析关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/13`；完整条件与来源：`/architecture/responsibility_explanations/computed_source_contract_seams/15`。
- 同一捕获 receiver 调用在所记录的构造/注入分支中列出目标/候选「WorkerBrokerClient.updateWorkerIf；WorkerStore.updateWorkerIf」；保留 direct/broker 条件，不将任意上下文端口全局绑定为一个实现。 原分析关系：`/judgments/0/obligations/1/evidence/production_assembly/worker_direct_broker_variants/14`；完整条件与来源：`/architecture/responsibility_explanations/computed_source_contract_seams/16`。
- 已有条件源码模型记录「受保护 queue 的 JSON 记录交接」的源操作与条件；实际部件关系为「callback=true；codec=true；lifecycle=true；path=true」，捕获参与声明为「ts:server/services/hub/hub-queue#loadLocalQueue；ts:server/services/hub/hub-queue#saveLocalQueue；ts:server/services/hub/hub-queue#withQueueMutation；ts:server/services/hub/hub-queue#withQueueMutation.&lt;arrow@1462:38&gt;」。持久消息和协议关系保持独立，执行、交付与队列投影没有合并成一个成功。 原分析关系：`/judgments/0/obligations/2/evidence/channels/queue`；完整条件与来源：`/architecture/responsibility_explanations/computed_source_contract_seams/17`。
- 已有条件源码模型记录「inbox 文件记录的提交、领取与消费」的源操作与条件；实际部件关系为「reader=true；record_identity=true；writer=true」，捕获参与声明为「module:ts:shared/fs-utils；ts:shared/fs-utils#currentHooks；ts:shared/fs-utils#jsonContent；ts:shared/fs-utils#writeJsonAtomic；ts:shared/orchestrator/worker-store#WorkerStore._readLocalInboxJson；ts:shared/orchestrator/worker-store#WorkerStore._withLocalInboxLock；ts:shared/orchestrator/worker-store#WorkerStore.claimInboxEntries；ts:shared/orchestrator/worker-store#WorkerStore.claimInboxEntries.&lt;loop@1967:4&gt;.&lt;arrow@1967:36&gt;；ts:shared/orchestrator/worker-store#WorkerStore.claimInboxEntries.&lt;loop@1967:4&gt;.&lt;block@1967:71&gt;.&lt;arrow@1969:75&gt;；ts:shared/orchestrator/worker-store#WorkerStore.constructor；ts:shared/orchestrator/worker-store#WorkerStore.writeInboxWithReceipt；ts:shared/orchestrator/worker-store#WorkerStore.writeInboxWithReceipt.&lt;arrow@1703:60&gt;」。记录/响应字段为「assignmentId；attempt；attemptToken；backend；committedRecord；path；previousRecord；ref；workerId；writeFence」。持久消息和协议关系保持独立，执行、交付与队列投影没有合并成一个成功。 原分析关系：`/judgments/0/obligations/2/evidence/channels/inbox`；完整条件与来源：`/architecture/responsibility_explanations/computed_source_contract_seams/18`。
- 已有条件源码模型记录「认证 broker 的 JSON 请求、分派与响应」的源操作与条件；实际部件关系为「claims_validation=true；credentials=true；dispatch=true；operation=true；request=true；response=true」，捕获参与声明为「ts:server/index#sendJson；ts:server/index#startHubServer.&lt;arrow@195:30&gt;；ts:server/services/hub/worker-state-broker#handleWorkerStateBroker；ts:server/services/hub/worker-state-broker#readWorkerBrokerBody；ts:shared/orchestrator/worker-broker-client#WorkerBrokerClient.#call；ts:shared/orchestrator/worker-broker-client#WorkerBrokerClient.claimInboxEntries；ts:shared/orchestrator/worker-broker-client#WorkerBrokerClient.claimInboxEntries.&lt;arrow@154:107&gt;；ts:shared/orchestrator/worker-broker-client#WorkerBrokerClient.constructor；ts:shared/orchestrator/worker-broker-client#brokerResult；ts:shared/orchestrator/worker-broker-client#inboxClaimsResult；ts:shared/orchestrator/worker-broker-client#inboxClaimsResult.&lt;arrow@83:19&gt;；ts:shared/orchestrator/worker-broker-client#recordResult」。记录/响应字段为「beforeMutation；body；cpbRoot；headers；hubRoot」。持久消息和协议关系保持独立，执行、交付与队列投影没有合并成一个成功。 原分析关系：`/judgments/0/obligations/2/evidence/channels/broker`；完整条件与来源：`/architecture/responsibility_explanations/computed_source_contract_seams/19`。
- 已有条件源码模型记录「持久 assignment/attempt 记录到消费者的交接」的源操作与条件；实际部件关系为「consumer=true；reader=true；writer=true」，捕获参与声明为「module:ts:shared/fs-utils；ts:server/orchestrator/reconciler#Reconciler._compensateFinalization；ts:server/orchestrator/reconciler#Reconciler._finalizeAssignment；ts:server/orchestrator/reconciler#Reconciler._finalizeQueue；ts:server/orchestrator/reconciler#Reconciler.reconcileAssignments；ts:shared/fs-utils#currentHooks；ts:shared/fs-utils#jsonContent；ts:shared/fs-utils#writeJsonAtomic；ts:shared/orchestrator/assignment-store#AssignmentStore._readLocalJsonObject；ts:shared/orchestrator/assignment-store#AssignmentStore._readState；ts:shared/orchestrator/assignment-store#AssignmentStore._readStateFile；ts:shared/orchestrator/assignment-store#AssignmentStore._writeState」。持久消息和协议关系保持独立，执行、交付与队列投影没有合并成一个成功。 原分析关系：`/judgments/0/obligations/2/evidence/channels/counter_transport`；完整条件与来源：`/architecture/responsibility_explanations/computed_source_contract_seams/20`。
- 源码实际模式字面量为 ["dry-run", "local", "pr", "remote"]，声明的 plan 字段为 ["closeIssue", "commit", "merge", "pullRequest", "pullRequestPreview", "push"]。有限表组合这些模式与源码中的布尔 opt-in，并保留字段 unknown；plan 不是已发生的写入。PR 调用的真实选项绑定到 callee 形参后，源码中早于条件 transport 且成立时 return 的条件包括 ["(!allowLive)", "(!isPass(verdict))", "(!remoteCapability || !remoteAuthorityValidator || !remoteCommitVerifier)", "(dryRun)"]。另有实际 review-bundle 分支在所选模式/权限 guard 之前调用其他接口，不能把后续 guard 推广为整个函数无本地 IO 的保证。远端命令接口的实际 Git 首参数为 ["push"]；注入 callback、授权结果、命令执行及远端后置条件保持未知。 原分析关系：`/functional_chains/2/pattern`；完整条件与来源：`/architecture/responsibility_explanations/computed_source_contract_seams/21`。
- 所选回调到达实际条件 (remediationStatus === "FIXED") 且前序 await 正常完成时，源码先调用 supersession 接口，再调用 lineage 接口；前一接口向已绑定事件写者传递的字面字段为 [{"type":"job_superseded","reason":"external_remediation_fixed"}]。后续 queue 入参中与该事件共享同一词法输入的字段为 [{"event_field":"jobId","queue_field":"/metadata/originJobId","input":"jobId"},{"event_field":"jobId","queue_field":"/metadata/sourceContext/remediation/previousJobId","input":"jobId"},{"event_field":"jobId","queue_field":"/metadata/sourceContext/retry/previousJobId","input":"jobId"},{"event_field":"project","queue_field":"/projectId","input":"project"}]；lineage helper 内的提前返回、抛出及外部操作失败仍可阻止实际入队。 原分析关系：`/functional_chains/12/pattern`；完整条件与来源：`/architecture/responsibility_explanations/computed_source_contract_seams/22`。

**显式来源交接**（列实际样例，所有关系保留）：

- 「cli/commands/doctor.ts::checkRuntimeHealth」中的实际记录 literal 语法位置直接构成「cli/commands/doctor.ts::checkRuntimeHealth」的调用实参；没有把记录构造解释为持久提交。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/0`。
- 「cli/commands/doctor.ts::checkRuntimeHealth」的捕获记录与「cli/commands/doctor.ts::checkRuntimeHealth」中的字段投影存在显式源关系；当前值和全部覆盖路径另保留。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/1`。
- 「cli/commands/doctor.ts::checkRuntimeHealth」的捕获记录与「cli/commands/doctor.ts::checkRuntimeHealth」中的字段投影存在显式源关系；当前值和全部覆盖路径另保留。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/2`。
- 「cli/commands/fix.ts::resolveDeps」的捕获来源被「cli/commands/fix.ts::resolveDeps」的显式 return 消费；未据此证明调用方激活或运行结果。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/3`。
- 「cli/commands/fix.ts::run」的捕获来源被「cli/commands/fix.ts::run」的显式 return 消费；未据此证明调用方激活或运行结果。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/4`。
- 「cli/commands/fix.ts::run」的捕获来源被「cli/commands/fix.ts::run」的显式 return 消费；未据此证明调用方激活或运行结果。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/5`。
- 「cli/commands/fix.ts::run」的捕获来源被「cli/commands/fix.ts::run」的显式 return 消费；未据此证明调用方激活或运行结果。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/6`。
- 「cli/commands/fix.ts::run」中的实际记录 literal 语法位置直接构成「cli/commands/fix.ts::run」的调用实参；没有把记录构造解释为持久提交。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/7`。

**接口复用**（列实际样例，所有关系保留）：

- 所选的 2 个确切声明通过已绑定调用复用「ts:core/agents/agent-runner#isErrorObject」；复用本身不构成职责混乱或唯一资源所有权的判断。 完整引用：`/architecture/responsibility_explanations/authenticated_interface_reuse/0`。
- 所选的 3 个确切声明通过已绑定调用复用「ts:core/agents/agent-runner#isReadOnlyPhase」；复用本身不构成职责混乱或唯一资源所有权的判断。 完整引用：`/architecture/responsibility_explanations/authenticated_interface_reuse/1`。
- 所选的 3 个确切声明通过已绑定调用复用「ts:core/contracts/failure-recovery#selectFailureRecovery」；复用本身不构成职责混乱或唯一资源所有权的判断。 完整引用：`/architecture/responsibility_explanations/authenticated_interface_reuse/2`。
- 所选的 9 个确切声明通过已绑定调用复用「ts:core/contracts/types#isRecord」；复用本身不构成职责混乱或唯一资源所有权的判断。 完整引用：`/architecture/responsibility_explanations/authenticated_interface_reuse/3`。
- 所选的 12 个确切声明通过已绑定调用复用「ts:core/contracts/types#recordValue」；复用本身不构成职责混乱或唯一资源所有权的判断。 完整引用：`/architecture/responsibility_explanations/authenticated_interface_reuse/4`。
- 所选的 2 个确切声明通过已绑定调用复用「ts:core/engine/candidate-artifact#captureCandidateArtifact」；复用本身不构成职责混乱或唯一资源所有权的判断。 完整引用：`/architecture/responsibility_explanations/authenticated_interface_reuse/5`。
- 所选的 2 个确切声明通过已绑定调用复用「ts:core/engine/candidate-artifact#verifyCandidateArtifactIdentity」；复用本身不构成职责混乱或唯一资源所有权的判断。 完整引用：`/architecture/responsibility_explanations/authenticated_interface_reuse/6`。
- 所选的 2 个确切声明通过已绑定调用复用「ts:core/engine/phase-retry#appendRuntimeEvent」；复用本身不构成职责混乱或唯一资源所有权的判断。 完整引用：`/architecture/responsibility_explanations/authenticated_interface_reuse/7`。

## 主要功能链、条件与反证

源码顺序只描述同一次调用正常到达的关系；异步完成、消息传输、远端响应和物理持久化均以实际证据范围为准。

### `cpb-captured-record-resource-writers`

分析类型：`resource_writer_ownership`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/0`；保存发现：`13d443da928da60f312c04a3`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| ownership_assessment | partial_captured_writers_and_consumers | /functional_chains/0/pattern/ownership_assessment |
| all_mutations_authorized_proven | false | /functional_chains/0/pattern/all_mutations_authorized_proven |
| all_storage_resources_bound_proven | false | /functional_chains/0/pattern/all_storage_resources_bound_proven |
| call_record_and_effect_frontiers/0/activation_and_physical_effect_proven | false | /functional_chains/0/pattern/call_record_and_effect_frontiers/0/activation_and_physical_effect_proven |
| call_record_and_effect_frontiers/1/activation_and_physical_effect_proven | false | /functional_chains/0/pattern/call_record_and_effect_frontiers/1/activation_and_physical_effect_proven |
| call_record_and_effect_frontiers/1/arguments/1/construction/fields/jobId/value/kind | shorthand_property_identifier | /functional_chains/0/pattern/call_record_and_effect_frontiers/1/arguments/1/construction/fields/jobId/value/kind |
| call_record_and_effect_frontiers/1/arguments/1/construction/fields/jobId/value/name | jobId | /functional_chains/0/pattern/call_record_and_effect_frontiers/1/arguments/1/construction/fields/jobId/value/name |
| call_record_and_effect_frontiers/1/arguments/1/construction/fields/project/value/kind | shorthand_property_identifier | /functional_chains/0/pattern/call_record_and_effect_frontiers/1/arguments/1/construction/fields/project/value/kind |
| call_record_and_effect_frontiers/1/arguments/1/construction/fields/project/value/name | project | /functional_chains/0/pattern/call_record_and_effect_frontiers/1/arguments/1/construction/fields/project/value/name |
| call_record_and_effect_frontiers/1/arguments/1/construction/parts/0/value/kind | shorthand_property_identifier | /functional_chains/0/pattern/call_record_and_effect_frontiers/1/arguments/1/construction/parts/0/value/kind |
| call_record_and_effect_frontiers/1/arguments/1/construction/parts/0/value/name | project | /functional_chains/0/pattern/call_record_and_effect_frontiers/1/arguments/1/construction/parts/0/value/name |
| call_record_and_effect_frontiers/1/arguments/1/construction/parts/1/value/kind | shorthand_property_identifier | /functional_chains/0/pattern/call_record_and_effect_frontiers/1/arguments/1/construction/parts/1/value/kind |
| call_record_and_effect_frontiers/1/arguments/1/construction/parts/1/value/name | jobId | /functional_chains/0/pattern/call_record_and_effect_frontiers/1/arguments/1/construction/parts/1/value/name |
| call_record_and_effect_frontiers/1/arguments/1/construction/runtime_object_or_presence_proven | false | /functional_chains/0/pattern/call_record_and_effect_frontiers/1/arguments/1/construction/runtime_object_or_presence_proven |
| call_record_and_effect_frontiers/2/activation_and_physical_effect_proven | false | /functional_chains/0/pattern/call_record_and_effect_frontiers/2/activation_and_physical_effect_proven |
| call_record_and_effect_frontiers/3/activation_and_physical_effect_proven | false | /functional_chains/0/pattern/call_record_and_effect_frontiers/3/activation_and_physical_effect_proven |
| call_record_and_effect_frontiers/4/activation_and_physical_effect_proven | false | /functional_chains/0/pattern/call_record_and_effect_frontiers/4/activation_and_physical_effect_proven |
| call_record_and_effect_frontiers/5/activation_and_physical_effect_proven | false | /functional_chains/0/pattern/call_record_and_effect_frontiers/5/activation_and_physical_effect_proven |

所有事实及源位置：`/functional_chains/0/source_facts`；配置声明单列于 `/functional_chains/0/policy_declarations`，不作为自动证据。

### `cpb-event-index-projection`

分析类型：`event_index_projection`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/1`；保存发现：`62730b11397229db7b001ed9`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| relation_witnesses/append_calls_selected_durable_writer | true | /functional_chains/1/pattern/relation_witnesses/append_calls_selected_durable_writer |
| relation_witnesses/event_append_precedes_index_refresh_on_normal_reaching | true | /functional_chains/1/pattern/relation_witnesses/event_append_precedes_index_refresh_on_normal_reaching |
| relation_witnesses/event_serializer_result_is_actual_durable_writer_argument | true | /functional_chains/1/pattern/relation_witnesses/event_serializer_result_is_actual_durable_writer_argument |
| relation_witnesses/index_rebuild_calls_same_index_writer | true | /functional_chains/1/pattern/relation_witnesses/index_rebuild_calls_same_index_writer |
| relation_witnesses/index_refresh_calls_selected_updater | true | /functional_chains/1/pattern/relation_witnesses/index_refresh_calls_selected_updater |
| relation_witnesses/index_update_calls_selected_index_writer | true | /functional_chains/1/pattern/relation_witnesses/index_update_calls_selected_index_writer |
| relation_witnesses/locked_projection_supplies_literal_update_callback | true | /functional_chains/1/pattern/relation_witnesses/locked_projection_supplies_literal_update_callback |
| relation_witnesses/projection_callback_state_is_written_to_same_index_record | true | /functional_chains/1/pattern/relation_witnesses/projection_callback_state_is_written_to_same_index_record |
| relation_witnesses/projection_returns_explicit_state_field | true | /functional_chains/1/pattern/relation_witnesses/projection_returns_explicit_state_field |
| relation_witnesses/read_events_materialized_state_flows_to_rebuilt_index_writer | true | /functional_chains/1/pattern/relation_witnesses/read_events_materialized_state_flows_to_rebuilt_index_writer |
| relation_witnesses/retry_has_captured_catch | true | /functional_chains/1/pattern/relation_witnesses/retry_has_captured_catch |
| record_fields/classification | [] | /functional_chains/1/pattern/record_fields/classification |
| record_fields/append/0/branch_context | [] | /functional_chains/1/pattern/record_fields/append/0/branch_context |
| record_fields/append/0/callback_activation_proven | false | /functional_chains/1/pattern/record_fields/append/0/callback_activation_proven |
| record_fields/append/0/fields/0/value/kind | shorthand_property_identifier | /functional_chains/1/pattern/record_fields/append/0/fields/0/value/kind |
| record_fields/append/0/fields/0/value/reference_dependencies_only | true | /functional_chains/1/pattern/record_fields/append/0/fields/0/value/reference_dependencies_only |
| record_fields/append/0/fields/0/value/reference_path/binding_id | c010df4f4b224bf61cbd86a6b8c984bf7fd4397b39f8af1d88968f4a53c25140 | /functional_chains/1/pattern/record_fields/append/0/fields/0/value/reference_path/binding_id |
| record_fields/append/0/fields/0/value/reference_path/members | [] | /functional_chains/1/pattern/record_fields/append/0/fields/0/value/reference_path/members |

**保留的分析缺口**：

- `record_projection_physical_commit_and_all_recovery_not_proven`；完整位置与原因见 `/functional_chains/1/analysis_gaps`。

所有事实及源位置：`/functional_chains/1/source_facts`；配置声明单列于 `/functional_chains/1/policy_declarations`，不作为自动证据。

### `cpb-finalizer-conditional-publication`

分析类型：`conditional_publication_boundary`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/2`；保存发现：`68ccc02ac3ab4a201dea8e9a`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| statement | 源码实际模式字面量为 ["dry-run", "local", "pr", "remote"]，声明的 plan 字段为 ["closeIssue", "commit", "merge", "pullRequest", "pullRequestPreview", "push"]。有限表组合这些模式与源码中的布尔 opt-in，并保留字段 unknown；plan 不是已发生的写入。PR 调用的真实选项绑定到 callee 形参后，源码中早于条件 transport 且成立时 return 的条件包括 ["(!allowLive)", "(!isPass(verdict))", "(!remot…［展示截断；完整值见引用］ | /functional_chains/2/pattern/statement |
| interpretation | 区分的是实际枚举/opt-in 条件、PR 提前返回和源码发布接口；配置允许与真实外写成功是不同证据。可空通用 callback 的默认值与所选 caller 提供的字段另列，未推广为全项目必然授权。 | /functional_chains/2/pattern/interpretation |
| relation_witnesses/0/conditions/0/branch | then | /functional_chains/2/pattern/relation_witnesses/0/conditions/0/branch |
| relation_witnesses/0/conditions/0/condition/kind | binary_expression | /functional_chains/2/pattern/relation_witnesses/0/conditions/0/condition/kind |
| relation_witnesses/0/conditions/0/condition/operands/0/kind | binary_expression | /functional_chains/2/pattern/relation_witnesses/0/conditions/0/condition/operands/0/kind |
| relation_witnesses/0/conditions/0/condition/operands/0/operator | === | /functional_chains/2/pattern/relation_witnesses/0/conditions/0/condition/operands/0/operator |
| relation_witnesses/0/conditions/0/condition/operands/0/runtime_predicate_or_assignment_proven | false | /functional_chains/2/pattern/relation_witnesses/0/conditions/0/condition/operands/0/runtime_predicate_or_assignment_proven |
| relation_witnesses/0/conditions/0/condition/operands/1/kind | binary_expression | /functional_chains/2/pattern/relation_witnesses/0/conditions/0/condition/operands/1/kind |
| relation_witnesses/0/conditions/0/condition/operands/1/operator | === | /functional_chains/2/pattern/relation_witnesses/0/conditions/0/condition/operands/1/operator |
| relation_witnesses/0/conditions/0/condition/operands/1/runtime_predicate_or_assignment_proven | false | /functional_chains/2/pattern/relation_witnesses/0/conditions/0/condition/operands/1/runtime_predicate_or_assignment_proven |
| relation_witnesses/0/conditions/0/condition/operator | \|\| | /functional_chains/2/pattern/relation_witnesses/0/conditions/0/condition/operator |
| relation_witnesses/0/conditions/0/condition/runtime_predicate_or_assignment_proven | false | /functional_chains/2/pattern/relation_witnesses/0/conditions/0/condition/runtime_predicate_or_assignment_proven |
| relation_witnesses/0/conditions/0/condition_truth_proven | false | /functional_chains/2/pattern/relation_witnesses/0/conditions/0/condition_truth_proven |
| relation_witnesses/0/conditions/0/kind | if | /functional_chains/2/pattern/relation_witnesses/0/conditions/0/kind |
| relation_witnesses/0/conditions/1/branch | then | /functional_chains/2/pattern/relation_witnesses/0/conditions/1/branch |
| relation_witnesses/0/conditions/1/condition/kind | unary_expression | /functional_chains/2/pattern/relation_witnesses/0/conditions/1/condition/kind |
| relation_witnesses/0/conditions/1/condition/operands/0/kind | identifier | /functional_chains/2/pattern/relation_witnesses/0/conditions/1/condition/operands/0/kind |
| relation_witnesses/0/conditions/1/condition/operands/0/name | dryRun | /functional_chains/2/pattern/relation_witnesses/0/conditions/1/condition/operands/0/name |

**有限源码分区 rows**；`/functional_chains/2/pattern/finite_mode_permission_relation/rows`，展示 20/20 行；展示截断=true。

| prefix_guard_values_complete | selected_prefix_guard_blocks | boolean_input_cells | mode_cell | plan_is_not_actual_remote_effect | source_plan_fields | 完整行引用 |
| --- | --- | --- | --- | --- | --- | --- |
| true | null | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":false,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":false} | dry-run | true | {"closeIssue":false,"commit":false,"merge":false,"pullRequest":false,"pullRequestPreview":true,"push":false} | /functional_chains/2/pattern/finite_mode_permission_relation/rows/0 |
| true | null | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":false,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":true} | dry-run | true | {"closeIssue":false,"commit":false,"merge":false,"pullRequest":false,"pullRequestPreview":true,"push":false} | /functional_chains/2/pattern/finite_mode_permission_relation/rows/1 |
| true | null | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":true,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":false} | dry-run | true | {"closeIssue":false,"commit":false,"merge":false,"pullRequest":false,"pullRequestPreview":true,"push":false} | /functional_chains/2/pattern/finite_mode_permission_relation/rows/2 |
| true | null | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":true,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":true} | dry-run | true | {"closeIssue":false,"commit":false,"merge":false,"pullRequest":false,"pullRequestPreview":true,"push":false} | /functional_chains/2/pattern/finite_mode_permission_relation/rows/3 |
| true | ad8f8a73a416c456f70ca619 | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":false,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":false} | local | true | {"closeIssue":false,"commit":{"unknown":true,"source_expression":{"kind":"binary","left":{"kind":"not","operand":{"kind":"binary","left":{"kind":"input","name":"mode"},"operator":"===","right":{"kind":"literal","value":"dry-run"}}},"operator":"&amp;&amp;","right":{"kind":"binary","left":{"key":"length","kin…［展示截断；完整值见引用］ | /functional_chains/2/pattern/finite_mode_permission_relation/rows/4 |
| true | null | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":false,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":true} | local | true | {"closeIssue":false,"commit":{"unknown":true,"source_expression":{"kind":"binary","left":{"kind":"not","operand":{"kind":"binary","left":{"kind":"input","name":"mode"},"operator":"===","right":{"kind":"literal","value":"dry-run"}}},"operator":"&amp;&amp;","right":{"kind":"binary","left":{"key":"length","kin…［展示截断；完整值见引用］ | /functional_chains/2/pattern/finite_mode_permission_relation/rows/5 |
| true | null | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":true,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":false} | local | true | {"closeIssue":false,"commit":{"unknown":true,"source_expression":{"kind":"binary","left":{"kind":"not","operand":{"kind":"binary","left":{"kind":"input","name":"mode"},"operator":"===","right":{"kind":"literal","value":"dry-run"}}},"operator":"&amp;&amp;","right":{"kind":"binary","left":{"key":"length","kin…［展示截断；完整值见引用］ | /functional_chains/2/pattern/finite_mode_permission_relation/rows/6 |
| true | null | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":true,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":true} | local | true | {"closeIssue":false,"commit":{"unknown":true,"source_expression":{"kind":"binary","left":{"kind":"not","operand":{"kind":"binary","left":{"kind":"input","name":"mode"},"operator":"===","right":{"kind":"literal","value":"dry-run"}}},"operator":"&amp;&amp;","right":{"kind":"binary","left":{"key":"length","kin…［展示截断；完整值见引用］ | /functional_chains/2/pattern/finite_mode_permission_relation/rows/7 |
| true | ad8f8a73a416c456f70ca619 | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":false,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":false} | pr | true | {"closeIssue":false,"commit":{"unknown":true,"source_expression":{"kind":"binary","left":{"kind":"not","operand":{"kind":"binary","left":{"kind":"input","name":"mode"},"operator":"===","right":{"kind":"literal","value":"dry-run"}}},"operator":"&amp;&amp;","right":{"kind":"binary","left":{"key":"length","kin…［展示截断；完整值见引用］ | /functional_chains/2/pattern/finite_mode_permission_relation/rows/8 |
| true | null | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":false,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":true} | pr | true | {"closeIssue":false,"commit":{"unknown":true,"source_expression":{"kind":"binary","left":{"kind":"not","operand":{"kind":"binary","left":{"kind":"input","name":"mode"},"operator":"===","right":{"kind":"literal","value":"dry-run"}}},"operator":"&amp;&amp;","right":{"kind":"binary","left":{"key":"length","kin…［展示截断；完整值见引用］ | /functional_chains/2/pattern/finite_mode_permission_relation/rows/9 |
| true | null | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":true,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":false} | pr | true | {"closeIssue":false,"commit":{"unknown":true,"source_expression":{"kind":"binary","left":{"kind":"not","operand":{"kind":"binary","left":{"kind":"input","name":"mode"},"operator":"===","right":{"kind":"literal","value":"dry-run"}}},"operator":"&amp;&amp;","right":{"kind":"binary","left":{"key":"length","kin…［展示截断；完整值见引用］ | /functional_chains/2/pattern/finite_mode_permission_relation/rows/10 |
| true | null | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":true,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":true} | pr | true | {"closeIssue":false,"commit":{"unknown":true,"source_expression":{"kind":"binary","left":{"kind":"not","operand":{"kind":"binary","left":{"kind":"input","name":"mode"},"operator":"===","right":{"kind":"literal","value":"dry-run"}}},"operator":"&amp;&amp;","right":{"kind":"binary","left":{"key":"length","kin…［展示截断；完整值见引用］ | /functional_chains/2/pattern/finite_mode_permission_relation/rows/11 |
| true | ad8f8a73a416c456f70ca619 | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":false,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":false} | remote | true | {"closeIssue":true,"commit":{"unknown":true,"source_expression":{"kind":"binary","left":{"kind":"not","operand":{"kind":"binary","left":{"kind":"input","name":"mode"},"operator":"===","right":{"kind":"literal","value":"dry-run"}}},"operator":"&amp;&amp;","right":{"kind":"binary","left":{"key":"length","kind…［展示截断；完整值见引用］ | /functional_chains/2/pattern/finite_mode_permission_relation/rows/12 |
| true | null | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":false,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":true} | remote | true | {"closeIssue":true,"commit":{"unknown":true,"source_expression":{"kind":"binary","left":{"kind":"not","operand":{"kind":"binary","left":{"kind":"input","name":"mode"},"operator":"===","right":{"kind":"literal","value":"dry-run"}}},"operator":"&amp;&amp;","right":{"kind":"binary","left":{"key":"length","kind…［展示截断；完整值见引用］ | /functional_chains/2/pattern/finite_mode_permission_relation/rows/13 |
| true | null | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":true,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":false} | remote | true | {"closeIssue":true,"commit":{"unknown":true,"source_expression":{"kind":"binary","left":{"kind":"not","operand":{"kind":"binary","left":{"kind":"input","name":"mode"},"operator":"===","right":{"kind":"literal","value":"dry-run"}}},"operator":"&amp;&amp;","right":{"kind":"binary","left":{"key":"length","kind…［展示截断；完整值见引用］ | /functional_chains/2/pattern/finite_mode_permission_relation/rows/14 |
| true | null | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":true,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":true} | remote | true | {"closeIssue":true,"commit":{"unknown":true,"source_expression":{"kind":"binary","left":{"kind":"not","operand":{"kind":"binary","left":{"kind":"input","name":"mode"},"operator":"===","right":{"kind":"literal","value":"dry-run"}}},"operator":"&amp;&amp;","right":{"kind":"binary","left":{"key":"length","kind…［展示截断；完整值见引用］ | /functional_chains/2/pattern/finite_mode_permission_relation/rows/15 |
| true | 377044156c3863e47858bbfc | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":false,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":false} | &lt;other-than-source-mode-literals&gt; | true | {"closeIssue":false,"commit":{"unknown":true,"source_expression":{"kind":"binary","left":{"kind":"not","operand":{"kind":"binary","left":{"kind":"input","name":"mode"},"operator":"===","right":{"kind":"literal","value":"dry-run"}}},"operator":"&amp;&amp;","right":{"kind":"binary","left":{"key":"length","kin…［展示截断；完整值见引用］ | /functional_chains/2/pattern/finite_mode_permission_relation/rows/16 |
| true | 377044156c3863e47858bbfc | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":false,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":true} | &lt;other-than-source-mode-literals&gt; | true | {"closeIssue":false,"commit":{"unknown":true,"source_expression":{"kind":"binary","left":{"kind":"not","operand":{"kind":"binary","left":{"kind":"input","name":"mode"},"operator":"===","right":{"kind":"literal","value":"dry-run"}}},"operator":"&amp;&amp;","right":{"kind":"binary","left":{"key":"length","kin…［展示截断；完整值见引用］ | /functional_chains/2/pattern/finite_mode_permission_relation/rows/17 |
| true | 377044156c3863e47858bbfc | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":true,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":false} | &lt;other-than-source-mode-literals&gt; | true | {"closeIssue":false,"commit":{"unknown":true,"source_expression":{"kind":"binary","left":{"kind":"not","operand":{"kind":"binary","left":{"kind":"input","name":"mode"},"operator":"===","right":{"kind":"literal","value":"dry-run"}}},"operator":"&amp;&amp;","right":{"kind":"binary","left":{"key":"length","kin…［展示截断；完整值见引用］ | /functional_chains/2/pattern/finite_mode_permission_relation/rows/18 |
| true | 377044156c3863e47858bbfc | {"a28644eb7b1c391771c8ecb5cff41049b6b8b12cf7f64a3c8d5388223e555305":true,"c7def2c4b0aeb1c66f726a3ebdbbcd7dfbddde841240e28d1befe58be39627c7":true} | &lt;other-than-source-mode-literals&gt; | true | {"closeIssue":false,"commit":{"unknown":true,"source_expression":{"kind":"binary","left":{"kind":"not","operand":{"kind":"binary","left":{"kind":"input","name":"mode"},"operator":"===","right":{"kind":"literal","value":"dry-run"}}},"operator":"&amp;&amp;","right":{"kind":"binary","left":{"key":"length","kin…［展示截断；完整值见引用］ | /functional_chains/2/pattern/finite_mode_permission_relation/rows/19 |

所有事实及源位置：`/functional_chains/2/source_facts`；配置声明单列于 `/functional_chains/2/policy_declarations`，不作为自动证据。

### `cpb-report-access-audit-response`

分析类型：`conditional_gate_relations`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/3`；保存发现：`a6809cb5f80cad425b325b5e`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| all_project_functionality_proven | false | /functional_chains/3/pattern/all_project_functionality_proven |
| groups/access_audit/necessary_gaps | [] | /functional_chains/3/pattern/groups/access_audit/necessary_gaps |
| groups/access_audit/all_http_security_or_business_mutations_proven | false | /functional_chains/3/pattern/groups/access_audit/all_http_security_or_business_mutations_proven |
| groups/access_audit/response_replacement_relations/0/conditions | ["the captured registered request callback is invoked and reaches the awaited audit call","the selected opener, callback and response writer declarations are active","the audit await rejects or throws and catch logging completes normally","normal plain response object properties; no getters, Proxy o…［展示截断；完整值见引用］ | /functional_chains/3/pattern/groups/access_audit/response_replacement_relations/0/conditions |
| groups/access_audit/response_replacement_relations/0/actual_http_response_delivery_proven | false | /functional_chains/3/pattern/groups/access_audit/response_replacement_relations/0/actual_http_response_delivery_proven |
| groups/access_audit/response_replacement_relations/0/actual_response_writer_call/callee_source | sendJson | /functional_chains/3/pattern/groups/access_audit/response_replacement_relations/0/actual_response_writer_call/callee_source |
| groups/access_audit/response_replacement_relations/0/actual_response_writer_call/arguments/1/current_referent_value_proven | false | /functional_chains/3/pattern/groups/access_audit/response_replacement_relations/0/actual_response_writer_call/arguments/1/current_referent_value_proven |
| groups/access_audit/response_replacement_relations/0/actual_response_writer_call/arguments/2/current_referent_value_proven | false | /functional_chains/3/pattern/groups/access_audit/response_replacement_relations/0/actual_response_writer_call/arguments/2/current_referent_value_proven |
| groups/access_audit/response_replacement_relations/0/actual_response_writer_call/arguments/3/current_referent_value_proven | false | /functional_chains/3/pattern/groups/access_audit/response_replacement_relations/0/actual_response_writer_call/arguments/3/current_referent_value_proven |
| groups/access_audit/response_replacement_relations/0/actual_response_writer_call/call_runtime_success_proven | false | /functional_chains/3/pattern/groups/access_audit/response_replacement_relations/0/actual_response_writer_call/call_runtime_success_proven |
| groups/access_audit/response_replacement_relations/0/actual_response_writer_call/callee_activation_proven | false | /functional_chains/3/pattern/groups/access_audit/response_replacement_relations/0/actual_response_writer_call/callee_activation_proven |
| groups/access_audit/response_replacement_relations/0/audit_arguments/0/construction/runtime_object_or_presence_proven | false | /functional_chains/3/pattern/groups/access_audit/response_replacement_relations/0/audit_arguments/0/construction/runtime_object_or_presence_proven |
| groups/access_audit/response_replacement_relations/0/audit_write_durability_proven | false | /functional_chains/3/pattern/groups/access_audit/response_replacement_relations/0/audit_write_durability_proven |
| groups/access_audit/response_replacement_relations/0/business_mutation_rollback_proven | false | /functional_chains/3/pattern/groups/access_audit/response_replacement_relations/0/business_mutation_rollback_proven |
| groups/access_audit/response_replacement_relations/0/callback_activation_proven | false | /functional_chains/3/pattern/groups/access_audit/response_replacement_relations/0/callback_activation_proven |
| groups/access_audit/response_replacement_relations/0/conditional_gate_version | captured-conditional-gate-relations-1 | /functional_chains/3/pattern/groups/access_audit/response_replacement_relations/0/conditional_gate_version |
| groups/access_audit/response_replacement_relations/0/failure_response/fields/statusCode/value | 503 | /functional_chains/3/pattern/groups/access_audit/response_replacement_relations/0/failure_response/fields/statusCode/value |
| groups/access_audit/response_replacement_relations/0/response_field_arguments/1/current_referent_value_proven | false | /functional_chains/3/pattern/groups/access_audit/response_replacement_relations/0/response_field_arguments/1/current_referent_value_proven |

所有事实及源位置：`/functional_chains/3/source_facts`；配置声明单列于 `/functional_chains/3/policy_declarations`，不作为自动证据。

### `cpb-report-agent-execution-policy`

分析类型：`agent_execution_policy`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/4`；保存发现：`d9034e67dd88277d6e056b0a`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| admission_and_postexecution_review/supported | true | /functional_chains/4/pattern/admission_and_postexecution_review/supported |
| admission_and_postexecution_review/execute_binding/callee_source | execPool.execute | /functional_chains/4/pattern/admission_and_postexecution_review/execute_binding/callee_source |
| admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/attemptId/value/kind | shorthand_property_identifier | /functional_chains/4/pattern/admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/attemptId/value/kind |
| admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/attemptId/value/name | attemptId | /functional_chains/4/pattern/admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/attemptId/value/name |
| admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/bypass/value/literal | false | /functional_chains/4/pattern/admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/bypass/value/literal |
| admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/bypass/value/kind | false | /functional_chains/4/pattern/admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/bypass/value/kind |
| admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/conversationKey/value/kind | ternary_expression | /functional_chains/4/pattern/admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/conversationKey/value/kind |
| admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/conversationKey/value/runtime_value_proven | false | /functional_chains/4/pattern/admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/conversationKey/value/runtime_value_proven |
| admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/conversationKey/value/source | typeof conversationKey === "string" &amp;&amp; conversationKey ? conversationKey : undefined | /functional_chains/4/pattern/admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/conversationKey/value/source |
| admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/conversationKey/value/source_truncated | false | /functional_chains/4/pattern/admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/conversationKey/value/source_truncated |
| admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/cwd/value/kind | shorthand_property_identifier | /functional_chains/4/pattern/admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/cwd/value/kind |
| admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/cwd/value/name | cwd | /functional_chains/4/pattern/admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/cwd/value/name |
| admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/dataRoot/value/kind | shorthand_property_identifier | /functional_chains/4/pattern/admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/dataRoot/value/kind |
| admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/dataRoot/value/name | dataRoot | /functional_chains/4/pattern/admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/dataRoot/value/name |
| admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/env/value/kind | identifier | /functional_chains/4/pattern/admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/env/value/kind |
| admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/env/value/name | executionEnv | /functional_chains/4/pattern/admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/env/value/name |
| admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/jobId/value/kind | shorthand_property_identifier | /functional_chains/4/pattern/admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/jobId/value/kind |
| admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/jobId/value/name | jobId | /functional_chains/4/pattern/admission_and_postexecution_review/execute_binding/arguments/4/construction/fields/jobId/value/name |

所有事实及源位置：`/functional_chains/4/source_facts`；配置声明单列于 `/functional_chains/4/policy_declarations`，不作为自动证据。

### `cpb-report-completion-gate-conditions`

分析类型：`conditional_gate_relations`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/5`；保存发现：`57b7965ae2fe48439796004c`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| all_project_functionality_proven | false | /functional_chains/5/pattern/all_project_functionality_proven |
| groups/completion/statement | Return records, local condition dependencies and source order are computed separately. Path conditions retain prior short circuits; local conditions describe the current gate only. No target inputs were executed. | /functional_chains/5/pattern/groups/completion/statement |
| groups/completion/necessary_gaps | [] | /functional_chains/5/pattern/groups/completion/necessary_gaps |
| groups/completion/checklist_internal_checks_proven | false | /functional_chains/5/pattern/groups/completion/checklist_internal_checks_proven |
| groups/completion/condition_consumers/0/condition_source/kind | identifier | /functional_chains/5/pattern/groups/completion/condition_consumers/0/condition_source/kind |
| groups/completion/condition_consumers/0/condition_source/name | checklist | /functional_chains/5/pattern/groups/completion/condition_consumers/0/condition_source/name |
| groups/completion/condition_consumers/0/branch_runtime_selected | false | /functional_chains/5/pattern/groups/completion/condition_consumers/0/branch_runtime_selected |
| groups/completion/condition_consumers/0/condition_abstract_form/kind | input | /functional_chains/5/pattern/groups/completion/condition_consumers/0/condition_abstract_form/kind |
| groups/completion/condition_consumers/0/condition_abstract_form/name | checklist | /functional_chains/5/pattern/groups/completion/condition_consumers/0/condition_abstract_form/name |
| groups/completion/condition_consumers/0/condition_variants/0/kind | input | /functional_chains/5/pattern/groups/completion/condition_consumers/0/condition_variants/0/kind |
| groups/completion/condition_consumers/0/condition_variants/0/name | checklist | /functional_chains/5/pattern/groups/completion/condition_consumers/0/condition_variants/0/name |
| groups/completion/condition_consumers/0/conditional_gate_version | captured-conditional-gate-relations-1 | /functional_chains/5/pattern/groups/completion/condition_consumers/0/conditional_gate_version |
| groups/completion/condition_consumers/0/kind | completion_gate_condition_consumes_result | /functional_chains/5/pattern/groups/completion/condition_consumers/0/kind |
| groups/completion/condition_consumers/0/local_predicate_roles | [] | /functional_chains/5/pattern/groups/completion/condition_consumers/0/local_predicate_roles |
| groups/completion/condition_consumers/0/normal_source_order_index | 0 | /functional_chains/5/pattern/groups/completion/condition_consumers/0/normal_source_order_index |
| groups/completion/condition_consumers/0/opaque_result_fields | [] | /functional_chains/5/pattern/groups/completion/condition_consumers/0/opaque_result_fields |
| groups/completion/condition_consumers/1/condition_source/kind | binary_expression | /functional_chains/5/pattern/groups/completion/condition_consumers/1/condition_source/kind |
| groups/completion/condition_consumers/1/condition_source/operands/0/current_referent_value_proven | false | /functional_chains/5/pattern/groups/completion/condition_consumers/1/condition_source/operands/0/current_referent_value_proven |

**有限源码分区 absent_input_partitions**；`/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/absent_input_partitions`，展示 2/2 行；展示截断=false。

| boolean_result | input_cell | unknown | 完整行引用 |
| --- | --- | --- | --- |
| false | missing | false | /functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/absent_input_partitions/0 |
| false | null | false | /functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/absent_input_partitions/1 |

**有限源码分区 record_partitions**；`/functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions`，展示 9/9 行；展示截断=false。

| boolean_result | property_cells | unknown | 完整行引用 |
| --- | --- | --- | --- |
| false | {"planMode":"none","workflow":"docs"} | false | /functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/0 |
| false | {"planMode":"none","workflow":"readonly"} | false | /functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/1 |
| false | {"planMode":"none","workflow":"&lt;other-than-captured-literals&gt;"} | false | /functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/2 |
| false | {"planMode":"parent","workflow":"docs"} | false | /functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/3 |
| false | {"planMode":"parent","workflow":"readonly"} | false | /functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/4 |
| false | {"planMode":"parent","workflow":"&lt;other-than-captured-literals&gt;"} | false | /functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/5 |
| false | {"planMode":"&lt;other-than-captured-literals&gt;","workflow":"docs"} | false | /functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/6 |
| false | {"planMode":"&lt;other-than-captured-literals&gt;","workflow":"readonly"} | false | /functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/7 |
| true | {"planMode":"&lt;other-than-captured-literals&gt;","workflow":"&lt;other-than-captured-literals&gt;"} | false | /functional_chains/5/pattern/groups/completion/mutating_finite_enum_partition/record_partitions/8 |

所有事实及源位置：`/functional_chains/5/source_facts`；配置声明单列于 `/functional_chains/5/policy_declarations`，不作为自动证据。

### `cpb-report-conditional-delivery-result`

分析类型：`conditional_delivery_result`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/6`；保存发现：`6be872753a6f9135c0269bad`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| interpretation | The captured normal source chain separates execution, terminal delivery and queue projection; external I/O and provider outcomes remain conditional. | /functional_chains/6/pattern/interpretation |
| all_function_paths_or_hidden_effects_proven | false | /functional_chains/6/pattern/all_function_paths_or_hidden_effects_proven |
| all_recovery_complete_proven | false | /functional_chains/6/pattern/all_recovery_complete_proven |
| components/finalizer/supported | true | /functional_chains/6/pattern/components/finalizer/supported |
| components/finalizer/conditional_finalization/0/supported | true | /functional_chains/6/pattern/components/finalizer/conditional_finalization/0/supported |
| components/finalizer/conditional_finalization/0/fact/actual_execution_or_finalizer_success_proven | false | /functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/actual_execution_or_finalizer_success_proven |
| components/finalizer/conditional_finalization/0/fact/execution_status_path/0 | 4650e60de88b55260c2b9a13c5aaa313a7ebebe37a7d59d17e2c10f65b77f754 | /functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/execution_status_path/0 |
| components/finalizer/conditional_finalization/0/fact/execution_status_path/1 | ["status"] | /functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/execution_status_path/1 |
| components/finalizer/conditional_finalization/0/fact/execution_success_literal | completed | /functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/execution_success_literal |
| components/finalizer/conditional_finalization/0/fact/finalizer_ok_path/0 | 7f9440dc927642e5d70a52081d3a2d94d47dc65bf291550849e9a3a2137f6e1a | /functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/finalizer_ok_path/0 |
| components/finalizer/conditional_finalization/0/fact/finalizer_ok_path/1 | ["ok"] | /functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/finalizer_ok_path/1 |
| components/finalizer/conditional_finalization/0/fact/kind | delivery_execution_success_requires_conditional_finalization | /functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/kind |
| components/finalizer/conditional_finalization/0/fact/metadata_enable_path/0 | 5c0c7be8e18e8c5cf81f007821034233cf5505d132e89d1e283d4cec2dbc6e3f | /functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/metadata_enable_path/0 |
| components/finalizer/conditional_finalization/0/fact/metadata_enable_path/1 | ["metadata","autoFinalize"] | /functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/metadata_enable_path/1 |
| components/finalizer/conditional_finalization/0/fact/ok_expression/kind | binary_expression | /functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/ok_expression/kind |
| components/finalizer/conditional_finalization/0/fact/ok_expression/operands/0/kind | unary_expression | /functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/ok_expression/operands/0/kind |
| components/finalizer/conditional_finalization/0/fact/ok_expression/operands/0/operator | ! | /functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/ok_expression/operands/0/operator |
| components/finalizer/conditional_finalization/0/fact/ok_expression/operands/0/runtime_predicate_or_assignment_proven | false | /functional_chains/6/pattern/components/finalizer/conditional_finalization/0/fact/ok_expression/operands/0/runtime_predicate_or_assignment_proven |

所有事实及源位置：`/functional_chains/6/source_facts`；配置声明单列于 `/functional_chains/6/policy_declarations`，不作为自动证据。

### `cpb-report-engine-stage-chain`

分析类型：`guarded_call_sequence`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/7`；保存发现：`64cc21afc98bd5e621642d14`。

**entry 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `isRecord → TypeError`；`core/engine/run-job.ts:66`。
- `setJobId`；`core/engine/run-job.ts:72`。
- `setCurrentPhase`；`core/engine/run-job.ts:73`。
- `runJobInner → finalizeAuditTrail → handleRunJobPanic`；`core/engine/run-job.ts:74`。

**stages 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `buildRunJobEnv`；`core/engine/run-job.ts:116`。
- `attachPreDagTimeouts`；`core/engine/run-job.ts:117`。
- `createJobAndHandleBlocked`；`core/engine/run-job.ts:120`。
- `recordValue`；`core/engine/run-job.ts:125`。
- `Object.keys → ctx.appendEvent → Array.isArray → new Date().toISOString → Date`；`core/engine/run-job.ts:126`。
- `prepareTaskAndRiskMap`；`core/engine/run-job.ts:145`。
- `runHighAssurancePlanning`；`core/engine/run-job.ts:152`。
- `freezeChecklistAndMaterializeDag`；`core/engine/run-job.ts:159`。
- `recordValue → import → cleanupSessionCache`；`core/engine/run-job.ts:168`。
- `executeWorkflowDag`；`core/engine/run-job.ts:177`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| scoped_source_supported | true | /functional_chains/7/pattern/scoped_source_supported |
| sequences/entry/conditions/0/branch_context | [] | /functional_chains/7/pattern/sequences/entry/conditions/0/branch_context |
| sequences/entry/conditions/0/branches/0/abrupt_source_expressions/0/kind | throw_statement | /functional_chains/7/pattern/sequences/entry/conditions/0/branches/0/abrupt_source_expressions/0/kind |
| sequences/entry/conditions/0/branches/0/abrupt_source_expressions/0/runtime_completion_proven | false | /functional_chains/7/pattern/sequences/entry/conditions/0/branches/0/abrupt_source_expressions/0/runtime_completion_proven |
| sequences/entry/conditions/0/branches/0/branch | then | /functional_chains/7/pattern/sequences/entry/conditions/0/branches/0/branch |
| sequences/entry/conditions/0/branches/0/branch_all_paths_abrupt_proven | true | /functional_chains/7/pattern/sequences/entry/conditions/0/branches/0/branch_all_paths_abrupt_proven |
| sequences/entry/conditions/0/branches/0/call_ids | ["1924eba8c503978b0e775159"] | /functional_chains/7/pattern/sequences/entry/conditions/0/branches/0/call_ids |
| sequences/entry/conditions/0/condition/kind | unary_expression | /functional_chains/7/pattern/sequences/entry/conditions/0/condition/kind |
| sequences/entry/conditions/0/condition/operands/0/callee_source | isRecord | /functional_chains/7/pattern/sequences/entry/conditions/0/condition/operands/0/callee_source |
| sequences/entry/conditions/0/condition/operands/0/call_effects_or_result_proven | false | /functional_chains/7/pattern/sequences/entry/conditions/0/condition/operands/0/call_effects_or_result_proven |
| sequences/entry/conditions/0/condition/operands/0/callee_expression/kind | identifier | /functional_chains/7/pattern/sequences/entry/conditions/0/condition/operands/0/callee_expression/kind |
| sequences/entry/conditions/0/condition/operands/0/callee_expression/name | isRecord | /functional_chains/7/pattern/sequences/entry/conditions/0/condition/operands/0/callee_expression/name |
| sequences/entry/conditions/0/condition/operands/0/kind | call_expression | /functional_chains/7/pattern/sequences/entry/conditions/0/condition/operands/0/kind |
| sequences/entry/conditions/0/condition/operator | ! | /functional_chains/7/pattern/sequences/entry/conditions/0/condition/operator |
| sequences/entry/conditions/0/condition/runtime_predicate_or_assignment_proven | false | /functional_chains/7/pattern/sequences/entry/conditions/0/condition/runtime_predicate_or_assignment_proven |
| sequences/entry/conditions/0/kind | source_guard_and_abrupt_branch | /functional_chains/7/pattern/sequences/entry/conditions/0/kind |
| sequences/entry/conditions/0/role | entry | /functional_chains/7/pattern/sequences/entry/conditions/0/role |
| sequences/entry/conditions/0/runtime_predicate_proven | false | /functional_chains/7/pattern/sequences/entry/conditions/0/runtime_predicate_proven |

所有事实及源位置：`/functional_chains/7/source_facts`；配置声明单列于 `/functional_chains/7/policy_declarations`，不作为自动证据。

### `cpb-report-job-audit-best-effort`

分析类型：`best_effort_finalization`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/8`；保存发现：`7ba0e642e5f36b5bef03a2ea`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| audit_subject_equivalence_to_other_systems_proven | false | /functional_chains/8/pattern/audit_subject_equivalence_to_other_systems_proven |
| caught_scopes/0/runtime_failure_or_finalization_success_proven | false | /functional_chains/8/pattern/caught_scopes/0/runtime_failure_or_finalization_success_proven |
| caught_scopes/1/runtime_failure_or_finalization_success_proven | false | /functional_chains/8/pattern/caught_scopes/1/runtime_failure_or_finalization_success_proven |
| caught_scopes/2/enclosing_branch_context/0/activation_proven | false | /functional_chains/8/pattern/caught_scopes/2/enclosing_branch_context/0/activation_proven |
| caught_scopes/2/runtime_failure_or_finalization_success_proven | false | /functional_chains/8/pattern/caught_scopes/2/runtime_failure_or_finalization_success_proven |
| scoped_source_supported | true | /functional_chains/8/pattern/scoped_source_supported |

所有事实及源位置：`/functional_chains/8/source_facts`；配置声明单列于 `/functional_chains/8/policy_declarations`，不作为自动证据。

### `cpb-report-readiness-abrupt-guard`

分析类型：`conditional_gate_relations`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/9`；保存发现：`dbdf085022aed24e7f0f4607`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| all_project_functionality_proven | false | /functional_chains/9/pattern/all_project_functionality_proven |
| groups/readiness/necessary_gaps | [] | /functional_chains/9/pattern/groups/readiness/necessary_gaps |
| groups/readiness/predicate_finite_partition/absent_input_partitions/0/boolean_result | null | /functional_chains/9/pattern/groups/readiness/predicate_finite_partition/absent_input_partitions/0/boolean_result |
| groups/readiness/predicate_finite_partition/absent_input_partitions/0/unknown | true | /functional_chains/9/pattern/groups/readiness/predicate_finite_partition/absent_input_partitions/0/unknown |
| groups/readiness/predicate_finite_partition/absent_input_partitions/1/boolean_result | null | /functional_chains/9/pattern/groups/readiness/predicate_finite_partition/absent_input_partitions/1/boolean_result |
| groups/readiness/predicate_finite_partition/absent_input_partitions/1/unknown | true | /functional_chains/9/pattern/groups/readiness/predicate_finite_partition/absent_input_partitions/1/unknown |
| groups/readiness/predicate_finite_partition/record_partitions/0/boolean_result | true | /functional_chains/9/pattern/groups/readiness/predicate_finite_partition/record_partitions/0/boolean_result |
| groups/readiness/predicate_finite_partition/record_partitions/0/unknown | false | /functional_chains/9/pattern/groups/readiness/predicate_finite_partition/record_partitions/0/unknown |
| groups/readiness/predicate_finite_partition/record_partitions/1/boolean_result | false | /functional_chains/9/pattern/groups/readiness/predicate_finite_partition/record_partitions/1/boolean_result |
| groups/readiness/predicate_finite_partition/record_partitions/1/unknown | false | /functional_chains/9/pattern/groups/readiness/predicate_finite_partition/record_partitions/1/unknown |
| groups/readiness/readiness_implementation_success_or_external_state_proven | false | /functional_chains/9/pattern/groups/readiness/readiness_implementation_success_or_external_state_proven |
| groups/readiness/relations/0/conditions | ["the selected entry and predicate declarations are active","the initializer and opaque calls before the return complete normally","the predicate reads the same stable ordinary result record; no getters, Proxy or external mutation"] | /functional_chains/9/pattern/groups/readiness/relations/0/conditions |
| groups/readiness/relations/0/actual_predicate_call/callee_source | isReadinessFailure | /functional_chains/9/pattern/groups/readiness/relations/0/actual_predicate_call/callee_source |
| groups/readiness/relations/0/actual_predicate_call/branch_context/0/condition/callee_source | isReadinessFailure | /functional_chains/9/pattern/groups/readiness/relations/0/actual_predicate_call/branch_context/0/condition/callee_source |
| groups/readiness/relations/0/actual_predicate_call/branch_context/0/condition/call_effects_or_result_proven | false | /functional_chains/9/pattern/groups/readiness/relations/0/actual_predicate_call/branch_context/0/condition/call_effects_or_result_proven |
| groups/readiness/relations/0/actual_predicate_call/branch_context/0/condition/kind | call_expression | /functional_chains/9/pattern/groups/readiness/relations/0/actual_predicate_call/branch_context/0/condition/kind |
| groups/readiness/relations/0/actual_predicate_call/branch_context/0/condition_truth_proven | false | /functional_chains/9/pattern/groups/readiness/relations/0/actual_predicate_call/branch_context/0/condition_truth_proven |
| groups/readiness/relations/0/actual_predicate_call/call_runtime_success_proven | false | /functional_chains/9/pattern/groups/readiness/relations/0/actual_predicate_call/call_runtime_success_proven |

**有限源码分区 absent_input_partitions**；`/functional_chains/9/pattern/groups/readiness/predicate_finite_partition/absent_input_partitions`，展示 2/2 行；展示截断=false。

| boolean_result | input_cell | unknown | 完整行引用 |
| --- | --- | --- | --- |
| null | missing | true | /functional_chains/9/pattern/groups/readiness/predicate_finite_partition/absent_input_partitions/0 |
| null | null | true | /functional_chains/9/pattern/groups/readiness/predicate_finite_partition/absent_input_partitions/1 |

**有限源码分区 record_partitions**；`/functional_chains/9/pattern/groups/readiness/predicate_finite_partition/record_partitions`，展示 2/2 行；展示截断=false。

| boolean_result | property_cells | unknown | 完整行引用 |
| --- | --- | --- | --- |
| true | {"ok":false} | false | /functional_chains/9/pattern/groups/readiness/predicate_finite_partition/record_partitions/0 |
| false | {"ok":"&lt;other-than-captured-literals&gt;"} | false | /functional_chains/9/pattern/groups/readiness/predicate_finite_partition/record_partitions/1 |

所有事实及源位置：`/functional_chains/9/source_facts`；配置声明单列于 `/functional_chains/9/policy_declarations`，不作为自动证据。

### `cpb-report-trusted-probe-command-source`

分析类型：`structured_command_source`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/10`；保存发现：`65cd294919771816fe7c8dc6`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| argument_reference_transfers/0/argument_value_field_or_activation_proven | false | /functional_chains/10/pattern/argument_reference_transfers/0/argument_value_field_or_activation_proven |
| argument_reference_transfers/1/argument/current_referent_value_proven | false | /functional_chains/10/pattern/argument_reference_transfers/1/argument/current_referent_value_proven |
| argument_reference_transfers/1/argument_value_field_or_activation_proven | false | /functional_chains/10/pattern/argument_reference_transfers/1/argument_value_field_or_activation_proven |
| argument_reference_transfers/2/argument/current_referent_value_proven | false | /functional_chains/10/pattern/argument_reference_transfers/2/argument/current_referent_value_proven |
| argument_reference_transfers/2/argument_value_field_or_activation_proven | false | /functional_chains/10/pattern/argument_reference_transfers/2/argument_value_field_or_activation_proven |
| argument_reference_transfers/3/argument/current_referent_value_proven | false | /functional_chains/10/pattern/argument_reference_transfers/3/argument/current_referent_value_proven |
| argument_reference_transfers/3/argument_value_field_or_activation_proven | false | /functional_chains/10/pattern/argument_reference_transfers/3/argument_value_field_or_activation_proven |
| argument_reference_transfers/4/argument_value_field_or_activation_proven | false | /functional_chains/10/pattern/argument_reference_transfers/4/argument_value_field_or_activation_proven |
| argument_reference_transfers/5/argument_value_field_or_activation_proven | false | /functional_chains/10/pattern/argument_reference_transfers/5/argument_value_field_or_activation_proven |
| argument_reference_transfers/6/argument_value_field_or_activation_proven | false | /functional_chains/10/pattern/argument_reference_transfers/6/argument_value_field_or_activation_proven |
| argument_reference_transfers/7/argument/current_referent_value_proven | false | /functional_chains/10/pattern/argument_reference_transfers/7/argument/current_referent_value_proven |
| argument_reference_transfers/7/argument_value_field_or_activation_proven | false | /functional_chains/10/pattern/argument_reference_transfers/7/argument_value_field_or_activation_proven |
| argument_reference_transfers/8/argument/current_referent_value_proven | false | /functional_chains/10/pattern/argument_reference_transfers/8/argument/current_referent_value_proven |
| argument_reference_transfers/8/argument_value_field_or_activation_proven | false | /functional_chains/10/pattern/argument_reference_transfers/8/argument_value_field_or_activation_proven |
| argument_reference_transfers/9/argument_value_field_or_activation_proven | false | /functional_chains/10/pattern/argument_reference_transfers/9/argument_value_field_or_activation_proven |
| argument_reference_transfers/10/argument_value_field_or_activation_proven | false | /functional_chains/10/pattern/argument_reference_transfers/10/argument_value_field_or_activation_proven |
| argument_reference_transfers/11/argument_value_field_or_activation_proven | false | /functional_chains/10/pattern/argument_reference_transfers/11/argument_value_field_or_activation_proven |
| captured_role_call_path_to_executor | true | /functional_chains/10/pattern/captured_role_call_path_to_executor |

**保留的分析缺口**：

- `structured_command_intermediate_values_and_external_effects_not_fully_proven`；完整位置与原因见 `/functional_chains/10/analysis_gaps`。

所有事实及源位置：`/functional_chains/10/source_facts`；配置声明单列于 `/functional_chains/10/policy_declarations`，不作为自动证据。

### `cpb-report-unsupported-probe-evidence`

分析类型：`unsupported_method_evidence`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/11`；保存发现：`b577b30117078aaecea00767`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| connected_true_marker_assignments/0/assignment_success_proven | false | /functional_chains/11/pattern/connected_true_marker_assignments/0/assignment_success_proven |
| connected_true_marker_assignments/0/branch_context/0/activation_proven | false | /functional_chains/11/pattern/connected_true_marker_assignments/0/branch_context/0/activation_proven |
| connected_true_marker_assignments/0/branch_context/1/condition/kind | identifier | /functional_chains/11/pattern/connected_true_marker_assignments/0/branch_context/1/condition/kind |
| connected_true_marker_assignments/0/branch_context/1/condition/name | existing | /functional_chains/11/pattern/connected_true_marker_assignments/0/branch_context/1/condition/name |
| connected_true_marker_assignments/0/branch_context/1/condition_truth_proven | false | /functional_chains/11/pattern/connected_true_marker_assignments/0/branch_context/1/condition_truth_proven |
| connected_true_marker_assignments/0/branch_context/2/condition/kind | binary_expression | /functional_chains/11/pattern/connected_true_marker_assignments/0/branch_context/2/condition/kind |
| connected_true_marker_assignments/0/branch_context/2/condition/operands/0/current_referent_value_proven | false | /functional_chains/11/pattern/connected_true_marker_assignments/0/branch_context/2/condition/operands/0/current_referent_value_proven |
| connected_true_marker_assignments/0/branch_context/2/condition/operands/0/kind | member_expression | /functional_chains/11/pattern/connected_true_marker_assignments/0/branch_context/2/condition/operands/0/kind |
| connected_true_marker_assignments/0/branch_context/2/condition/operands/0/member | emitFailedClaim | /functional_chains/11/pattern/connected_true_marker_assignments/0/branch_context/2/condition/operands/0/member |
| connected_true_marker_assignments/0/branch_context/2/condition/operands/0/member_location/column | 17 | /functional_chains/11/pattern/connected_true_marker_assignments/0/branch_context/2/condition/operands/0/member_location/column |
| connected_true_marker_assignments/0/branch_context/2/condition/operands/0/member_location/column_base | 1 | /functional_chains/11/pattern/connected_true_marker_assignments/0/branch_context/2/condition/operands/0/member_location/column_base |
| connected_true_marker_assignments/0/branch_context/2/condition/operands/0/member_location/column_unit | utf8_bytes | /functional_chains/11/pattern/connected_true_marker_assignments/0/branch_context/2/condition/operands/0/member_location/column_unit |
| connected_true_marker_assignments/0/branch_context/2/condition/operands/0/member_location/coordinate_space | captured_text_utf8 | /functional_chains/11/pattern/connected_true_marker_assignments/0/branch_context/2/condition/operands/0/member_location/coordinate_space |
| connected_true_marker_assignments/0/branch_context/2/condition/operands/0/member_location/end_byte | 15015 | /functional_chains/11/pattern/connected_true_marker_assignments/0/branch_context/2/condition/operands/0/member_location/end_byte |
| connected_true_marker_assignments/0/branch_context/2/condition/operands/0/member_location/end_column | 32 | /functional_chains/11/pattern/connected_true_marker_assignments/0/branch_context/2/condition/operands/0/member_location/end_column |
| connected_true_marker_assignments/0/branch_context/2/condition/operands/0/member_location/end_line | 351 | /functional_chains/11/pattern/connected_true_marker_assignments/0/branch_context/2/condition/operands/0/member_location/end_line |
| connected_true_marker_assignments/0/branch_context/2/condition/operands/0/member_location/file | core/workflow/evidence-probes.ts | /functional_chains/11/pattern/connected_true_marker_assignments/0/branch_context/2/condition/operands/0/member_location/file |
| connected_true_marker_assignments/0/branch_context/2/condition/operands/0/member_location/grammar | typescript | /functional_chains/11/pattern/connected_true_marker_assignments/0/branch_context/2/condition/operands/0/member_location/grammar |

**保留的分析缺口**：

- `structured_record_markers_do_not_prove_all_input_retention_or_persistence`；完整位置与原因见 `/functional_chains/11/analysis_gaps`。

所有事实及源位置：`/functional_chains/11/source_facts`；配置声明单列于 `/functional_chains/11/policy_declarations`，不作为自动证据。

### `cpb-review-fixed-state-lineage`

分析类型：`conditional_state_lineage`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/12`；保存发现：`4837c30b914f63f70f03ca34`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| statement | 所选回调到达实际条件 (remediationStatus === "FIXED") 且前序 await 正常完成时，源码先调用 supersession 接口，再调用 lineage 接口；前一接口向已绑定事件写者传递的字面字段为 [{"type":"job_superseded","reason":"external_remediation_fixed"}]。后续 queue 入参中与该事件共享同一词法输入的字段为 [{"event_field":"jobId","queue_field":"/metadata/originJobId","input":"jobId"},{"event_f…［展示截断；完整值见引用］ | /functional_chains/12/pattern/statement |
| interpretation | 这里闭合的是实际状态条件、事件字面字段及旧任务到后续任务的字段来源；并未证明回调必然激活、事件持久化成功、每次创建新任务或覆盖全部恢复路径。 | /functional_chains/12/pattern/interpretation |
| relation_witnesses/0/all_lineage_creation_proven | false | /functional_chains/12/pattern/relation_witnesses/0/all_lineage_creation_proven |
| relation_witnesses/0/event_durability_proven | false | /functional_chains/12/pattern/relation_witnesses/0/event_durability_proven |
| relation_witnesses/0/event_literal_fields/0/reason/value | external_remediation_fixed | /functional_chains/12/pattern/relation_witnesses/0/event_literal_fields/0/reason/value |
| relation_witnesses/0/event_literal_fields/0/reason/kind | literal | /functional_chains/12/pattern/relation_witnesses/0/event_literal_fields/0/reason/kind |
| relation_witnesses/0/event_literal_fields/0/type/value | job_superseded | /functional_chains/12/pattern/relation_witnesses/0/event_literal_fields/0/type/value |
| relation_witnesses/0/event_literal_fields/0/type/kind | literal | /functional_chains/12/pattern/relation_witnesses/0/event_literal_fields/0/type/kind |
| relation_witnesses/0/shared_source_field_origins/0/captured_origin_declaration_id | 5240bea3213ba205e41fb21cdc9ef4b42e535849569cc13888b9ea9c5e286c8c | /functional_chains/12/pattern/relation_witnesses/0/shared_source_field_origins/0/captured_origin_declaration_id |
| relation_witnesses/0/shared_source_field_origins/0/event_field | jobId | /functional_chains/12/pattern/relation_witnesses/0/shared_source_field_origins/0/event_field |
| relation_witnesses/0/shared_source_field_origins/0/heap_or_runtime_identity_proven | false | /functional_chains/12/pattern/relation_witnesses/0/shared_source_field_origins/0/heap_or_runtime_identity_proven |
| relation_witnesses/0/shared_source_field_origins/0/queue_field_path | /metadata/originJobId | /functional_chains/12/pattern/relation_witnesses/0/shared_source_field_origins/0/queue_field_path |
| relation_witnesses/0/shared_source_field_origins/0/source_origin/kind | input | /functional_chains/12/pattern/relation_witnesses/0/shared_source_field_origins/0/source_origin/kind |
| relation_witnesses/0/shared_source_field_origins/0/source_origin/name | jobId | /functional_chains/12/pattern/relation_witnesses/0/shared_source_field_origins/0/source_origin/name |
| relation_witnesses/0/shared_source_field_origins/1/captured_origin_declaration_id | 5240bea3213ba205e41fb21cdc9ef4b42e535849569cc13888b9ea9c5e286c8c | /functional_chains/12/pattern/relation_witnesses/0/shared_source_field_origins/1/captured_origin_declaration_id |
| relation_witnesses/0/shared_source_field_origins/1/event_field | jobId | /functional_chains/12/pattern/relation_witnesses/0/shared_source_field_origins/1/event_field |
| relation_witnesses/0/shared_source_field_origins/1/heap_or_runtime_identity_proven | false | /functional_chains/12/pattern/relation_witnesses/0/shared_source_field_origins/1/heap_or_runtime_identity_proven |
| relation_witnesses/0/shared_source_field_origins/1/queue_field_path | /metadata/sourceContext/remediation/previousJobId | /functional_chains/12/pattern/relation_witnesses/0/shared_source_field_origins/1/queue_field_path |

所有事实及源位置：`/functional_chains/12/source_facts`；配置声明单列于 `/functional_chains/12/policy_declarations`，不作为自动证据。

### `cpb-task-read-projection`

分析类型：`guarded_call_sequence`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/13`；保存发现：`b9f0bd2b67503d6e15c41d4f`。

**linked_record_lookup 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `listJobs`；`server/services/job/job-store.ts:1376`。
- `jobs.find`；`server/services/job/job-store.ts:1377`。

**project_selection 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `import → resolveHubRoot → loadRegistry → path.resolve → process.cwd → Object.entries → String → cwd.startsWith`；`cli/commands/task.ts:212`。
- `readFile → path.join → process.cwd → JSON.parse → pkg.name.replace(/[^a-zA-Z0-9-]/g, "-").replace → pkg.name.replace`；`cli/commands/task.ts:231`。
- `path     .basename(process.cwd())     .replace(/[^a-zA-Z0-9-]/g, "-")     .replace → path     .basename(process.cwd())     .replace → path     .basename → process.cwd`；`cli/commands/task.ts:243`。

**queue_interface 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `loadLocalQueue`；`server/services/hub/hub-queue.ts:1466`。

**queue_read 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `readBoundedRegularFileNoFollow → queuePath → normalizeQueue → JSON.parse → errnoCode → defaultQueue → String(errnoCode(err)).startsWith → String → Object.assign → Error`；`server/services/hub/hub-queue.ts:1425`。

**record_filter 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `Object.entries → FORBIDDEN_SET.has`；`core/contracts/task-view-fields.ts:132`。

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
- 后续步骤保留在 `/functional_chains/13/pattern/sequences/task_projection`。

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

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| scoped_source_supported | true | /functional_chains/13/pattern/scoped_source_supported |
| sequences/linked_record_lookup/conditions/0/branch_context | [] | /functional_chains/13/pattern/sequences/linked_record_lookup/conditions/0/branch_context |
| sequences/linked_record_lookup/conditions/0/branches/0/abrupt_source_expressions/0/kind | return_statement | /functional_chains/13/pattern/sequences/linked_record_lookup/conditions/0/branches/0/abrupt_source_expressions/0/kind |
| sequences/linked_record_lookup/conditions/0/branches/0/abrupt_source_expressions/0/runtime_completion_proven | false | /functional_chains/13/pattern/sequences/linked_record_lookup/conditions/0/branches/0/abrupt_source_expressions/0/runtime_completion_proven |
| sequences/linked_record_lookup/conditions/0/branches/0/branch | then | /functional_chains/13/pattern/sequences/linked_record_lookup/conditions/0/branches/0/branch |
| sequences/linked_record_lookup/conditions/0/branches/0/branch_all_paths_abrupt_proven | true | /functional_chains/13/pattern/sequences/linked_record_lookup/conditions/0/branches/0/branch_all_paths_abrupt_proven |
| sequences/linked_record_lookup/conditions/0/branches/0/call_ids | [] | /functional_chains/13/pattern/sequences/linked_record_lookup/conditions/0/branches/0/call_ids |
| sequences/linked_record_lookup/conditions/0/condition/kind | unary_expression | /functional_chains/13/pattern/sequences/linked_record_lookup/conditions/0/condition/kind |
| sequences/linked_record_lookup/conditions/0/condition/operands/0/kind | identifier | /functional_chains/13/pattern/sequences/linked_record_lookup/conditions/0/condition/operands/0/kind |
| sequences/linked_record_lookup/conditions/0/condition/operands/0/name | queueEntryId | /functional_chains/13/pattern/sequences/linked_record_lookup/conditions/0/condition/operands/0/name |
| sequences/linked_record_lookup/conditions/0/condition/operator | ! | /functional_chains/13/pattern/sequences/linked_record_lookup/conditions/0/condition/operator |
| sequences/linked_record_lookup/conditions/0/condition/runtime_predicate_or_assignment_proven | false | /functional_chains/13/pattern/sequences/linked_record_lookup/conditions/0/condition/runtime_predicate_or_assignment_proven |
| sequences/linked_record_lookup/conditions/0/kind | source_guard_and_abrupt_branch | /functional_chains/13/pattern/sequences/linked_record_lookup/conditions/0/kind |
| sequences/linked_record_lookup/conditions/0/role | linked_record_lookup | /functional_chains/13/pattern/sequences/linked_record_lookup/conditions/0/role |
| sequences/linked_record_lookup/conditions/0/runtime_predicate_proven | false | /functional_chains/13/pattern/sequences/linked_record_lookup/conditions/0/runtime_predicate_proven |
| sequences/linked_record_lookup/future_or_callback_activation_proven | false | /functional_chains/13/pattern/sequences/linked_record_lookup/future_or_callback_activation_proven |
| sequences/linked_record_lookup/guards/0/activation_or_termination_proven | false | /functional_chains/13/pattern/sequences/linked_record_lookup/guards/0/activation_or_termination_proven |
| sequences/linked_record_lookup/guards/0/predicate_truth_proven | false | /functional_chains/13/pattern/sequences/linked_record_lookup/guards/0/predicate_truth_proven |

所有事实及源位置：`/functional_chains/13/source_facts`；配置声明单列于 `/functional_chains/13/policy_declarations`，不作为自动证据。

### `cpb-trusted-command-lineage`

分析类型：`trusted_command_lineage`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/14`；保存发现：`57e29e3f2281f98bc96e7ca1`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| relation_witnesses/all_selected_direct_role_call_transfers | true | /functional_chains/14/pattern/relation_witnesses/all_selected_direct_role_call_transfers |
| relation_witnesses/execfile_stdout_json_decode_is_actual_policy_parser_input | true | /functional_chains/14/pattern/relation_witnesses/execfile_stdout_json_decode_is_actual_policy_parser_input |
| relation_witnesses/executor_reads_executable_and_args_from_same_command_formal | true | /functional_chains/14/pattern/relation_witnesses/executor_reads_executable_and_args_from_same_command_formal |
| relation_witnesses/loaded_policy_lookup_result_is_actual_command_runner_input | true | /functional_chains/14/pattern/relation_witnesses/loaded_policy_lookup_result_is_actual_command_runner_input |
| relation_witnesses/parsed_policy_spec_has_explicit_command_fields | true | /functional_chains/14/pattern/relation_witnesses/parsed_policy_spec_has_explicit_command_fields |
| relation_witnesses/policy_parser_references_spec_parser_callback | true | /functional_chains/14/pattern/relation_witnesses/policy_parser_references_spec_parser_callback |
| relation_witnesses/selected_call_arguments_have_local_initializer_dependencies | true | /functional_chains/14/pattern/relation_witnesses/selected_call_arguments_have_local_initializer_dependencies |
| record_fields/command_runner/0/branch_context/0/activation_proven | false | /functional_chains/14/pattern/record_fields/command_runner/0/branch_context/0/activation_proven |
| record_fields/command_runner/0/branch_context/0/kind | for_statement | /functional_chains/14/pattern/record_fields/command_runner/0/branch_context/0/kind |
| record_fields/command_runner/0/callback_activation_proven | false | /functional_chains/14/pattern/record_fields/command_runner/0/callback_activation_proven |
| record_fields/command_runner/0/fields/0/value/kind | shorthand_property_identifier | /functional_chains/14/pattern/record_fields/command_runner/0/fields/0/value/kind |
| record_fields/command_runner/0/fields/0/value/reference_dependencies_only | true | /functional_chains/14/pattern/record_fields/command_runner/0/fields/0/value/reference_dependencies_only |
| record_fields/command_runner/0/fields/0/value/reference_path/binding_id | cf042e1aaa1ab37ef1ab61c79ad62de085d80794e8278d169b8e2c01fe5b6697 | /functional_chains/14/pattern/record_fields/command_runner/0/fields/0/value/reference_path/binding_id |
| record_fields/command_runner/0/fields/0/value/reference_path/members | [] | /functional_chains/14/pattern/record_fields/command_runner/0/fields/0/value/reference_path/members |
| record_fields/command_runner/0/fields/0/value/references/0/binding_path | null | /functional_chains/14/pattern/record_fields/command_runner/0/fields/0/value/references/0/binding_path |
| record_fields/command_runner/0/fields/0/value/references/0/declaration_kind | let | /functional_chains/14/pattern/record_fields/command_runner/0/fields/0/value/references/0/declaration_kind |
| record_fields/command_runner/0/fields/0/value/references/0/identity_complete | true | /functional_chains/14/pattern/record_fields/command_runner/0/fields/0/value/references/0/identity_complete |
| record_fields/command_runner/0/fields/0/value/references/0/name | attempt | /functional_chains/14/pattern/record_fields/command_runner/0/fields/0/value/references/0/name |

**保留的分析缺口**：

- `record_command_source_dependencies_do_not_prove_full_heap_noninterference`；完整位置与原因见 `/functional_chains/14/analysis_gaps`。

所有事实及源位置：`/functional_chains/14/source_facts`；配置声明单列于 `/functional_chains/14/policy_declarations`，不作为自动证据。

### `cpb-unsupported-record-retention`

分析类型：`unsupported_record_retention`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/15`；保存发现：`9d287929d532c5df6d777a3d`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| relation_witnesses/failure_records_append_to_returned_runner_collection | true | /functional_chains/15/pattern/relation_witnesses/failure_records_append_to_returned_runner_collection |
| relation_witnesses/ledger_claims_append_to_returned_evidence_collection | true | /functional_chains/15/pattern/relation_witnesses/ledger_claims_append_to_returned_evidence_collection |
| relation_witnesses/plan_initializes_and_propagates_true_marker | true | /functional_chains/15/pattern/relation_witnesses/plan_initializes_and_propagates_true_marker |
| relation_witnesses/runner_emits_explicit_true_failure_record | true | /functional_chains/15/pattern/relation_witnesses/runner_emits_explicit_true_failure_record |
| relation_witnesses/true_marker_excludes_selected_invalid_record_skip | true | /functional_chains/15/pattern/relation_witnesses/true_marker_excludes_selected_invalid_record_skip |
| relation_witnesses/verification_calls_runner_plan_ledger | true | /functional_chains/15/pattern/relation_witnesses/verification_calls_runner_plan_ledger |
| relation_witnesses/verification_passes_actual_ledger_result_json_to_artifact_writer | true | /functional_chains/15/pattern/relation_witnesses/verification_passes_actual_ledger_result_json_to_artifact_writer |
| record_fields/artifact_writer/0/branch_context | [] | /functional_chains/15/pattern/record_fields/artifact_writer/0/branch_context |
| record_fields/artifact_writer/0/callback_activation_proven | false | /functional_chains/15/pattern/record_fields/artifact_writer/0/callback_activation_proven |
| record_fields/artifact_writer/0/fields/0/value/kind | true | /functional_chains/15/pattern/record_fields/artifact_writer/0/fields/0/value/kind |
| record_fields/artifact_writer/0/fields/0/value/reference_dependencies_only | true | /functional_chains/15/pattern/record_fields/artifact_writer/0/fields/0/value/reference_dependencies_only |
| record_fields/artifact_writer/0/fields/0/value/reference_path | null | /functional_chains/15/pattern/record_fields/artifact_writer/0/fields/0/value/reference_path |
| record_fields/artifact_writer/0/fields/0/value/references | [] | /functional_chains/15/pattern/record_fields/artifact_writer/0/fields/0/value/references |
| record_fields/artifact_writer/0/fields/0/value/runtime_value_or_heap_identity_proven | false | /functional_chains/15/pattern/record_fields/artifact_writer/0/fields/0/value/runtime_value_or_heap_identity_proven |
| record_fields/artifact_writer/0/fields/0/value/source | true | /functional_chains/15/pattern/record_fields/artifact_writer/0/fields/0/value/source |
| record_fields/artifact_writer/0/fields/0/value/source_truncated | false | /functional_chains/15/pattern/record_fields/artifact_writer/0/fields/0/value/source_truncated |
| record_fields/artifact_writer/0/fields/0/index | 1 | /functional_chains/15/pattern/record_fields/artifact_writer/0/fields/0/index |
| record_fields/artifact_writer/0/fields/0/key | committed | /functional_chains/15/pattern/record_fields/artifact_writer/0/fields/0/key |

**保留的分析缺口**：

- `record_true_marker_does_not_prove_all_input_or_artifact_retention`；完整位置与原因见 `/functional_chains/15/analysis_gaps`。

所有事实及源位置：`/functional_chains/15/source_facts`；配置声明单列于 `/functional_chains/15/policy_declarations`，不作为自动证据。

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

