# CodePatchBay：Astra 独立静态分析 v1

分析对象：`/workspace/codepatchbay`，提交 `4f2d2eca31d90b0122db1c1429dd365672db2393`。本报告于 2026-10-12 固定第一版，作为 CallScope 后续能力迭代的独立依据。只读源码、项目声明和已有分析产物；没有执行目标入口、导入目标模块、安装目标依赖、调用 Beads/code-index、运行测试或构建。

## 判断

CodePatchBay 的主要交付链在源码上已经接通：CLI 任务进入队列，由带租约与 fencing 的编排器分配给受管理 worker，经服务适配器注入存储和 provider 端口，进入 checklist/DAG 引擎、阶段执行、完成门和交付收尾。关键边界不是单一同步调用栈：动态命令加载、持久 inbox、独立进程、对象端口和事件日志都是系统的一部分。仅凭当前 CallScope 的确定调用图会漏掉这些连接，不能据此判断“功能未实现”。

本轮得到三项值得维护者处理的具体结论：`pipeline --retries` 在受管理执行链上存在接线遗漏；`superseded` 在两个生产终态分类中不一致；`fix` 的同键幂等检查存在需要并发时序才能触发的窗口。前两项是可直接核对的代码事实，第三项是具有具体交错顺序的条件风险。它们都超出了“有没有调用边”的判断能力，不能伪装为现有图检测器已经自动发现的缺陷。

没有据此得出项目整体不具备交付能力，也没有证明运行正确。报告中的“完整”指覆盖账本、主要功能域、关键链路、证据、反证和未审范围完整，不表示逐行审完全部实现。

## 覆盖账本

| 区域 | 本轮阅读层次与代表来源 | 覆盖结论及限制 |
| --- | --- | --- |
| 产品与项目结构 | `README.md`、`AGENTS.md`、`package.json`；生产目录清单 | 确认本地/私有 coding-agent 交付运行时定位及稳定化目标；未执行发布门命令 |
| CLI 与产品入口 | `cli/cpb.ts`、`cli/commands/fix.ts`、`pipeline.ts`、`task.ts` | 重点检查分派、readiness、幂等、提交参数和结果展示；其他命令只作目录/职责盘点 |
| 编排与 worker | `server/orchestrator/hub-orchestrator.ts`、`scheduler.ts`、`worker-supervisor.ts`、`failure-router.ts`、`runtime/worker/managed-worker.ts`、`bridges/engine-bridge.ts` | 检查派发、任务身份、重试参数及进程/inbox 边界；未遍历全部异常恢复交错 |
| 引擎与阶段 | `server/services/engine-runner.ts`、`core/engine/run-job.ts`、`run-job-ports.ts`、DAG/完成门相关模块 | 深读组合入口、提前返回、基础设施注入和完成门；阶段子模块按主链检查，不宣称每种 workflow 已完整审核 |
| 证据与验证 | `core/workflow/probe-runner.ts`、`trusted-probe-policy.ts`、`evidence-probes.ts`、`checklist-decomposer.ts`、`core/engine/completion-gate.ts` | 检查可信命令来源、未支持方法、结构证据与语义结论边界 |
| Agent/provider | `core/agents/agent-runner.ts`、`core/engine/provider-handoff.ts`、`core/policy/child-env.ts`、`agent-sandbox.ts` | 检查端口、失败类型、环境与沙箱策略分支；外部 agent/ACP 实现未执行或验证 |
| 状态与持久化 | `event-store.ts`、`event-materializer.ts`、`job-store.ts`、`hub-queue.ts`、review/remediation 相关段落 | 重点复核终态集合、事件封口、索引投影与队列原子边界；存储故障恢复未实际演练 |
| Hub、安全和交付收尾 | `server/index.ts`、认证/worker broker/审计/finalizer 模块的来源整理与关键段落 | 确认存在分层认证、授权及审计路径；未完成所有 HTTP 路由、OIDC 算法、备份状态机和发布 provider 的逐分支安全审计 |
| 本地代码索引与辅助工具 | `core/indexing/local-code-index/` 目录、接口和已有解析缺口 | 仅结构盘点及语法缺口核对，未运行或完整复审其自有索引算法 |
| 排除/未审 | 测试、第三方依赖、构建产物、全部模板/技能 adapter 行为、所有支持平台和部署配置 | 不计入人工功能覆盖；没有使用未运行的测试作为通过证据 |

之前 CallScope v0.3 选入 333 份文件、完整解析 327 份，图含 10,999 节点和 60,146 条边。23,099 条是已绑定内部调用，约占所有记录边 38.4%；这个比例不是内部调用召回率，分母还含外部和动态边，分子也不代表功能正确率。3 份 TypeScript 语法失败、3 份 Shell 不支持与排除范围均保留。人工阅读范围与工具选入范围不是同一个指标。

## 架构职责和所有权

| 层 | 实际职责 | 关键边界 |
| --- | --- | --- |
| `cli/` | 命令选择、参数解释、任务提交和面向用户的投影 | 动态 import 选 handler；`task` 主要读取，不等于其所有传递依赖均无副作用 |
| `server/orchestrator/` | 队列候选、assignment/attempt、worker 生命周期及失败路由 | 队列和 worker 状态更新的原子条件、leader fencing 与任务身份 |
| `runtime/worker/`、`bridges/` | 工作区、inbox、执行进程以及从 worker 到引擎的适配 | 进程和持久消息边界，不应压成虚假的普通函数调用 |
| `core/engine/` | 任务准备、checklist 冻结、DAG、阶段和完成门 | 从 `ctx` 获取端口；禁止源码反向依赖 server 与允许调用注入的 server 实现是两回事 |
| `core/workflow/` | checklist、probe、证据格式和可判定条件 | 结构范围证据不能直接证明业务验收条件成立 |
| `server/services/` | job/event/queue、ACP/provider、GitHub、审计与 finalizer 实现 | 存储、外部副作用及恢复的权威操作需要在本层维持约束 |
| `shared/` | 文件、进程、身份、网络、锁与公共类型 | 广泛复用不意味着“上帝对象”；应按职责和修改耦合判断 |

## 主要功能链路

### 1. 命令到任务

`cli/cpb.ts` 的命令表选择文件，`main` 在第 154 行动态加载并在第 186 行调用 `mod.run`。`CPB_EXECUTOR_ROOT` 可由环境覆盖，命令表也不是一套已证明封闭的运行时模块集合。因此可以提取声明候选与命令 key，但不能把所有候选 handler 都当作必然直接调用。

`fix.run` 的主顺序是解析项目 → `assertFixReadiness` → 同键查询 → 组装 route/metadata → `enqueue`。`fix.ts:505–508` 的 readiness 失败分支在提交前返回，说明这里确实有保护分支；调用图单有 readiness 和 enqueue 两条边，不能证明这个顺序约束。

`pipeline` 同样把任务、workflow、plan mode、agent 配置及重试参数交给队列。命令参数被接受、传入 metadata 与最后被执行策略消费必须分开检查，`--retries` 的问题正发生在这一层间契约。

### 2. 队列到受管理执行

`HubOrchestrator.tick` 先调和 assignment，再取得候选、以条件更新预约队列、创建 assignment/attempt、选择 worker，并写 inbox（`hub-orchestrator.ts:315–450`）。worker supervisor 启动独立 managed-worker；worker 领取 inbox，在工作区和任务身份确定后，经动态 bridge 调用服务适配器（`managed-worker.ts:1349`、`:1393`、`:1797`；`bridges/engine-bridge.ts:17–18`）。

这是一条可由源码和协议串联的端到端结构链，但中间包括持久消息和进程启动。不能因函数可达性搜索停在 `spawn`、`writeInbox` 或 `import()` 就报“执行入口没接上”；也不能在图里跳过它们，假装任务身份、租约和提交时序已经得到证明。

### 3. 服务组合到 checklist/DAG

`runJobWithServices`（`engine-runner.ts:130`）调用 `buildServices`，再在第 157 行调用 `runJob`。端口有 broker 与本地存储两类分支：`createJob`、`appendEvent`、phase/job 终态写入、pool、artifact index、provider services 均由这里组装。`runJob(ctxInput: unknown)` 仍允许不同调用者提供上下文，故不能把引擎中的每个 `ctx.method()` 全局绑定到唯一实现。

`runJob → runJobInner`（`run-job.ts:75`）内的顺序清楚：创建/阻塞检查 `:121` → task/risk 准备 `:146` →高保障规划 `:152` →冻结 checklist 与构建 DAG `:159` →执行 DAG `:177`。前置步骤可返回 blocked/failed；高保障规划在范围冻结之前。仅保留无条件结构路径不足以表达这些保护分支。

外层 crash barrier 将未处理异常交给 `handleRunJobPanic`。`finalizeAuditTrail` 在正常和 panic 路径均尝试执行，但失败被捕获。这是 job 尾部的 best-effort 收尾，不能和 Hub 访问审计必须成功后响应的另一份合同混为一谈。

### 4. 阶段执行和可信验证

`runAgent` 先检查允许的 agent，再通过注入的 pool 执行，检查只读阶段的变更违规并分类失败（`agent-runner.ts:475–589`）。`pool.execute` 的唯一实现不是仅凭方法名可以得出的结论。子进程环境过滤、required/strict 沙箱失败分支确实存在；配置为 native/off/custom 与平台能力改变边界，源码有检查不等于实际隔离效果已验收。

`probe-runner.ts:147–160` 只从 `HEAD:.cpb/verification-probes.json` 读取可信 probe；`:435–438` 按 predicateId 选择结构化 executable/args；`:527–534` 使用 `execFile` 且 `shell: false`。模型的 `expectedEvidence` 文本不被用作命令。这里描述的是目标系统的源码行为，本审查没有调用任何 probe。

`static` probe 统计允许范围内的文件变化（`:613–637`），能证明“声明范围有改动”，不能证明需求语义。command/test 没有可信策略时保留失败证据；event/manual/absence 等方法在 `:707–726` 明确保留未实现 probe 的失败记录。不能把这解释成静默放行，也不能宣传这类自动验证已齐备。证据计划能接收额外 hardGate observation，是未支持自动采集方法的反证边界。

`completion-gate.ts` 先检查 checklist，再按 mutating 工作流检查 verify/adversarial verdict 等门；readonly/docs/parent 等分支有豁免语义。能核对门的存在和支配分支，不能单凭“调用了 completion gate”证明每个外部执行结果真实可靠。

### 5. 事件、投影和交付

事件流是 job 状态的重要来源，`event-store.ts:1188–1197` 在事件锁内重建状态并对终态业务变更封口。索引是投影，事件持久化和后续索引更新失败不是同一个提交边界；重建/doctor/调和路径存在，不能因暂时分歧直接宣称事件丢失或永久损坏。

review/remediation 的 FIXED 分支会记录 `job_superseded` 并创建新的 lineage task（`review-dispatch.ts:4468–4470`），这解释了为何原 job 的终态分类必须统一。finalizer 又有独立 journal 和恢复路径；外部 GitHub 写入与本地 dry-run 的区别应保留为配置/授权条件，不能按“有 GitHub API 调用”自动判断发生了发布。

核心 job 的 `completed` 还不是 assignment 或远端发布的最终成功。`runtime/worker/assignment-finalizer.ts:1236–1242` 按 `autoFinalize` 决定是否要求收尾成功，失败会转换持久结果；managed-worker 还有工作区清理和终态写入/读回，reconciler 才继续校验 attempt、finalizer 与 journal 并收敛队列。应把执行、交付与投影分别建模，不能只沿 `completeJob` 调用把整条链标绿。

## 具体缺口与反证

### CPB-01：`pipeline --retries` 未连接到受管理执行预算

**定性：已确认的参数接线遗漏，范围限定于已读生产队列链。** 帮助文本 `pipeline.ts:149` 承诺最大 pipeline retries；参数在 `:69–70` 解析、`:205` 写成 `metadata.maxRetries`。但 worker 在 `managed-worker.ts:1809` 固定传 `maxRetries: 3`；队列失败路由在 `failure-router.ts:112` 从 `MAX_RETRIES[failureKind]` 取预算，并在 `:265` 比较 attempts。所读生产链没有消费提交的 `metadata.maxRetries`。

这不是缺少 retry 能力，而是用户选项与实际预算没有建立对应关系。phase retry、DAG node retry、基础设施重试是不同预算；不能把它们存在当作该参数已生效的反证。`job-store.retryJob` 接受自己的 maxRetries 也不说明 pipeline metadata 已进入它。另有 `parseInt(...) || 3` 把零值回退默认的事实，但零是否允许须由产品合同明确，不能擅自把它计作第二个缺陷。

建议维护者先明确该选项控制哪一种尝试预算，在权威重试决策处消费并展示最终生效值；否则删去/拒绝无效选项，避免表面可配置。机器基准列为 `evidence_only`，需要跨函数属性传递和覆盖来源分析。

### CPB-02：`superseded` 的生产终态分类不一致

**定性：确定的跨层状态定义不一致；业务影响需按调用者细化。** materializer 第 633–636 行把 `job_superseded` 设为 terminal，第 792 行集合含 `superseded`；job-store 第 430 行集合缺少它，`isTerminal`（第 1407–1408 行）因此会对已有 superseded job 返回 false，`recoverAsNewJob` 在第 1441 行按“非终态”拒绝。

反证是底层 event-store 使用含 `superseded` 的集合封住业务变更，不能由上层判断遗漏宣称终态已被非法改写。被替代 job 是否应该允许 recovery 是另一个产品决策；修正终态分类不意味着必须开放恢复。建议统一 terminal 定义，再单列 recoverable 策略。能力需要枚举集合、状态赋值和跨层谓词一致性分析，不能靠调用环或可达性解决。

### CPB-03：同键幂等检查与权威写入之间存在并发窗口

**定性：有明确源码前提的并发风险，未做运行复现。** `core/contracts/idempotency.ts:6–16` 要求同键的任意非终态任务复用。`fix.ts:520/528` 在 enqueue 之前读取并选择；真正事务内的 `hub-queue.ts:1595–1598` 只按包含 description 的 entryKey 找 `pending`。

一个允许的交错是：A、B 都读到无任务 → A enqueue → scheduler 将 A 改为 scheduled → B enqueue；B 的事务内查询不再匹配 A，可以创建新任务。锁保护单次写入，没有把前置判定纳入同一约束。即使尚未调度，显式同 key 但 description 不同也受两个判定口径差异影响。

反证：顺序调用时 facade 会复用 scheduled/in_progress；同描述且第一项仍 pending 时底层会去重。因此不是“所有双提交都会重复”。建议在 queue 权威事务中按 project + hashed key + 全非终态统一约束，返回既有 ID；前置查询只作体验优化。能力需要原子边界和交错建模，当前纯调用图只能保存待复核证据。

## 不成立的缺陷推断

- 代码中有递归或调用环，不等于无终止；此前识别的静态环没有提供错误基例/状态进展证据，本轮不把它们升级为 bug。
- broker、pool、ctx、回调和动态 import 未绑定，不等于实际缺少实现；组合点和消息协议提供了反证。
- global coverage 不完整导致 helper 的否定检查未知，不等于 helper 调用了 engine。
- job audit best-effort 与 Hub access audit fail-closed 是不同对象，不能拼成“审计合同自相矛盾”。
- verification probe 自身会执行目标项目的检查命令，是 CodePatchBay 的产品职责；本次分析没有触发它，不应将源码中出现执行 API 当作违反本次审查边界。

## CallScope 能力差距与建议顺序

| 优先级 | 能力 | 本仓库的可验收材料 | 不能越过的边界 |
| --- | --- | --- | --- |
| P1 | 语法覆盖、定位和基准核对 | inline import 类型、保留字属性、原源码/hash/派生解析映射；正向直接边必须定位调用点 | 不忽略未识别 ERROR，不改写原始证据 |
| P1 | 条件化组合与候选来源 | 命令表、固定字符串动态 import、buildServices 显式对象成员 | 环境覆盖、broker 分支、可注入 ctx 保留 residual unknown；不建立所有候选的确定边 |
| P1 | 跨进程/消息关系 | queue→assignment→inbox→worker→bridge | 单列关系类型、身份与条件，不冒充函数 CALLS |
| P2 | 字段来源与消费者 | `--retries`→metadata→worker/router | 字段名字相同不是已经传播，需识别覆盖、默认和分支 |
| P2 | 状态合同一致性 | 两个 TERMINAL_STATUSES 与事件状态赋值 | terminal 和 recoverable 不可合并 |
| P2 | 顺序/事务边界 | readiness 失败提前返回、同键读查与队列写事务 | 调用链不能证明互斥或原子性，结论保持范围说明 |
| P3 | 更广统计、性能和图展示 | 在上述真实材料上积累可追溯观察 | 不用巨大图或低延迟掩盖能力缺口 |

首版能力提升的验收应是：复现冻结基准中的确定源码关系；未知保留具体调用点、候选和原因；对上述三个业务候选诚实输出尚不能自动裁决的能力缺口。更远的目标是让静态证据覆盖参数、状态和事务约束，而不是把 unknown 调成绿色。

机器材料见 [capability-baseline.json](capability-baseline.json)；比较协议见 [BASELINE_CONTRACT.md](BASELINE_CONTRACT.md)。本报告没有运行验证、功能通过率、漏洞利用或全项目无缺陷结论。

来源整理附录：[工作流来源](../astra-baseline-preparation/CPB_WORKFLOW.md)、[存储与安全来源](../astra-baseline-preparation/CPB_STORAGE_SECURITY.md)、[TypeScript 语法与绑定边界](../astra-baseline-preparation/TS_GAPS.md)。附录中的额外待复核线索不自动成为本报告的确认结论。冻结机器基准含本仓库 13 项观察及所引原文件哈希。
