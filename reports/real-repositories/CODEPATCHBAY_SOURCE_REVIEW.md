# CodePatchBay 源码调用结构核对

本报告是 CallScope 对真实源码的工具能力评估，目标目录为 `/workspace/codepatchbay`。目标仓库保持只读，未执行 `cpb`、`code-index`、Beads、依赖安装、编译、测试、Node 模块或仓库脚本。读取的仓库 `AGENTS.md` 中要求先使用本地索引与 Beads 的流程，受本次用户“目标代码零执行”的明确要求限制，因此没有触发这些工具。

本文只记录源码中可核对的连接、真实声明的意图，以及当前静态模型无法证明的部分。附属策略中的十条规则都是**人工选定的工具核对基准**，不是仓库维护者批准的完整架构约束；规则发现不能直接称为 CodePatchBay 缺陷。

## 范围与模块身份

- 配置：`codepatchbay-policy.json`；`source_roots=["."]`，不仅扫描抽样文件。
- 分析语言为 TypeScript 与 Python。主生产区为 `cli/`、`core/`、`server/`、`runtime/`、`bridges/` 与 `shared/`；根扫描还保留 `scripts/`、`skills/hermes/adapter.py`、`skills/openclaw/adapter.py` 和其他未排除的受支持源码，只把它们当文本数据。
- 显式排除 Git/Beads/CallScope 状态、依赖、`third_party`、`vendor`、`generated`、构建输出、覆盖率、测试、`.test-tmp` 测试生成物与 fixtures。未声称排除区已分析。
- `tsconfig.node.json` 使用 NodeNext，已读配置未设置 `paths` 或 `baseUrl`；代表性生产连接全部使用相对 ESM 导入，因此 `module_aliases={}`，无需猜测包输出目录。
- `.js` 相对导入需要绑定到相邻 `.ts` 源文件，例如 `engine-runner.ts` 的 `../../core/engine/run-job.js`。这是一项前端解析能力核对，不运行 `tsc`。
- 节点标识使用 `ts:<相对路径去扩展名>#<词法限定名>`，例如 `ts:core/engine/run-job#runJob`。不同文件的同名 `run` 不得合并。
- Python adapter 使用现有 Python 静态前端；没有将两份已有支持能力的 Python 源码悄悄排除或当作不支持。Python 与 TypeScript 间通过进程/协议的连接仍不建模为确定调用边。
- 三份 Shell 脚本 `scripts/cutover-orchestrator.sh`、`scripts/install.sh`、`skills/claude-code/install.sh` 保留在输入范围，但当前不支持 Shell 语义构图；应以 `unsupported` 呈现，不执行或伪装成解析成功。
- `cpb` 无扩展名启动器和编译后的 `dist/` 不属于本轮可构图源码覆盖；不承诺源码扫描等同于实际发布产物。

入口模式选取 `cli/cpb.main`、`fix.run`、`task.run`、`startHubServer` 和 `runJobWithServices`，用于展示代表性闭包。这不是所有 worker、bridge、timer、事件处理器、脚本和外部调用入口的完整清单。从这些入口未确定可达的函数不能称为死代码。

## 手工读取到的主要链路

**CLI 分派是动态边界。** `cli/cpb.ts:154` 根据 `COMMANDS[cmd]` 计算绝对模块路径再 `import()`，在 `cli/cpb.ts:186` 调用 `mod.run(...)`。源码可看到命令表包含 `task: "task.js"`，但这不等于具有确定的 `main → task.run` 静态绑定。CallScope 应保留动态导入和属性调用缺口，不能靠全局同名 `run` 猜测目标。

**服务适配器到执行核心有明确静态连接。** `server/services/engine-runner.ts:2` 导入 `runJob`，`runJobWithServices` 在同文件 `:157` 调用它。核心包装在 `core/engine/run-job.ts:75` 调用本地 `runJobInner`；内部流程在 `:159` 调用 `freezeChecklistAndMaterializeDag`，在 `:177` 调用 `executeWorkflowDag`。因此至少存在 `runJobWithServices → runJob → runJobInner → executeWorkflowDag` 的显式静态结构路径。路径存在不证明前置分支一定通过、执行顺序满足要求或所有异常恢复正确。

**基础设施通过端口注入。** `core/engine/run-job.ts` 的开头明确写出基础设施由 `ctx` 注入，不从 `core/` 导入 `server/`；适配器 `engine-runner.ts` 构造 `createJob`、`appendEvent` 等端口。此意图是源码依赖方向约束，不能翻译成“核心在运行时绝不能调用服务实现”。`ctx.appendEvent(...)` 等属性调用的目标需要注入信息，第一版静态前端应报告未知，不能伪造连接，也不能称为功能断链。本配置不使用 `forbidden_path core → server` 替代这项意图。

**公开 task 展示复用结果文案与字段清理。** `task.renderTaskView` 在 `cli/commands/task.ts:172` 调用本地 `humanResultLine`；`fix.followTask` 在 `cli/commands/fix.ts:352` 调用静态导入的同一 helper。`projectTaskView` 在 `server/services/task/task-view.ts:708` 调用 `sanitizeTaskView`。后者位于 `core/contracts/task-view-fields.ts:128`，源码明确采用浅层黑名单清理。这些调用结构可以核对，但工具不检查返回文案、字段值或嵌套数据是否符合业务约束。

**Hub 的认证请求处理依赖回调。** `server/index.ts` 的 `startHubServer` 构造原生 HTTP server 并传入异步请求 handler；其内部调用认证、权限与审计服务。外部 `createServer(...)` 注册 handler 的关系属于回调边界。本轮将该入口纳入图，但不要求现有显式调用图证明“每个请求都认证”或“审计一定完成”。

## 十个核对项与预期

| 规则 ID | 源 → 目标 | 规则性质与源码见证 | 正确的工具结果 |
|---|---|---|---|
| `cpb-observed-cli-project-argument` | `cli/cpb#main → cli/cpb#projectArgForCommand` | 实见直接调用，`cli/cpb.ts:167` | 确定直接边；不要求每次命令都执行 |
| `cpb-observed-task-result-rendering` | `cli/commands/task#renderTaskView → ...#humanResultLine` | 实见直接调用，`task.ts:172` | 确定直接边 |
| `cpb-observed-fix-shared-result-renderer` | `cli/commands/fix#followTask → cli/commands/task#humanResultLine` | 静态导入与调用，`fix.ts:61`、`:352` | 确定跨文件边 |
| `cpb-observed-server-engine-delegation` | `server/services/engine-runner#runJobWithServices → core/engine/run-job#runJob` | 静态导入与调用，`engine-runner.ts:2`、`:157` | 确定跨层边 |
| `cpb-observed-runjob-crash-wrapper` | `core/engine/run-job#runJob → ...#runJobInner` | 实见直接调用，`run-job.ts:75` | 确定直接边 |
| `cpb-observed-checklist-materialization` | `core/engine/run-job#runJobInner → core/engine/run-job-checklist-dag#freezeChecklistAndMaterializeDag` | 静态导入与调用，`run-job.ts:159` | 确定跨文件边 |
| `cpb-observed-runjob-to-dag-path` | `core/engine/run-job#runJob → core/engine/run-job-execute-dag#executeWorkflowDag` | 经 `runJobInner`，`run-job.ts:75`、`:177` | 确定正长度路径 |
| `cpb-observed-task-view-sanitization` | `server/services/task/task-view#projectTaskView → core/contracts/task-view-fields#sanitizeTaskView` | 实见清理调用，`task-view.ts:53`、`:708` | 确定跨文件边；不保证输出安全 |
| `cpb-capability-dynamic-command-boundary` | `cli/cpb#main → cli/commands/task#run` | 动态加载与 `mod.run`，`cpb.ts:154`、`:186` | 两端点存在，`mod.run` 保留真实解析缺口，没有伪造确定路径；单有 `uncertain` 状态不足以通过核对 |
| `cpb-observed-pure-result-helper-no-engine-call` | `cli/commands/task#humanResultLine → core/engine/run-job#runJob` | 手工读到的不存在直接边，`task.ts:141–152` | 不报告确定禁止连接；若全局覆盖缺口导致 `uncertain`，单列工具范围限制，不能推广为整条 task 链无副作用 |

前八条是“源码里有这个连接”的能力基准，第九条是保守性的能力边界，第十条是有真实端点的负向结构基准。它们不是检出率、误报率或整个仓库功能完整性的基准集合。两个端点不存在、存在解析失败或被重复定义时，都必须单独呈现分析缺口，不能把缺少发现算作核对通过。全局 `unsupported` 也可能使已读局部规则保守未知，因此需要分别看源码见证、局部调用解析和全局覆盖状态。

## 声明意图与本工具不能推出的结论

| 仓库真实声明 | 来源 | 本轮可核对部分 | 本轮不可保证部分 |
|---|---|---|---|
| CLI 命令位于 `cli/commands/`，core 为工作流契约与引擎，server 为编排服务 | `AGENTS.md` 的结构说明 | 文件身份、部分明确导入与显式调用 | 动态命令加载完整性及运行时分派 |
| core 基础设施通过 `ctx` 注入，无 server 导入 | `core/engine/run-job.ts:6–8` | 直接源码依赖说明与适配器调用 | 注入端口运行时目标、禁止所有 core→server 行为 |
| task 为只读 facade，不引入新状态机 | `cli/commands/task.ts` 开头与 `run` 注释 | 已读文案 helper 没有 engine 直接调用 | 整个传递调用链无写入、无外部行为 |
| fix.follow 与 task 共用结果文案 | `cli/commands/task.ts:133–139`、`cli/commands/fix.ts:347–353` | helper 共享调用结构 | 输出内容在所有输入下符合产品语义 |
| TaskView 返回前经过字段边界清理 | `server/services/task/task-view.ts:610–613`、`:704–709` | `sanitizeTaskView` 调用存在 | 每个字段值、嵌套信息或其他消费者都符合要求 |

调用链不能单独验证 strict flow order、readiness 失败不写 queue、异常恢复、字段映射、外部认证回调或真实业务行为。源码有相应注释与契约类型不代表 CallScope 已证明这些承诺。

## 最终静态扫描结果

扫描已保存并完成导出，快照 ID 为 `e91c3726e1238304414eab681edbd8045246e0c11b4e5e7244125910754aa7d7`，状态为 `partial`。本节依据 [codepatchbay-summary.json](codepatchbay-summary.json) 与 [codepatchbay-rule-witnesses.json](codepatchbay-rule-witnesses.json) 逐项核对，二者绑定相同的快照、源码哈希和策略哈希。完整原始报告在 [codepatchbay-snapshot.json](codepatchbay-snapshot.json)；它很大，阅读结果时优先使用精简证据文件。

本轮分析器为 `static-multilang-2`，检测器为 `call-rules-2`，快照 schema 为 `1`。捕获的解析组件版本包括 Tree-sitter `0.25.2`、TypeScript grammar `0.23.2` 与 CPython `3.12.14`，完整组件身份记录在上述 JSON 中。目标执行与目标测试标志均为 `false`。

| 源码类别 | 捕获文件 | 解析成功 | 覆盖缺口 |
|---|---:|---:|---|
| TypeScript / JavaScript / TSX | 328 | 325 | 3 份 `parse_error` |
| Python adapters | 2 | 2 | 0 |
| Shell | 3 | 0 | 3 份 `unsupported` |
| 合计 | 333 | 327 | 6 份未完成语义解析 |

首次输入清单 `input-inventory.json` 的 334 份文件曾包含 `.test-tmp` 生成的 JavaScript；最终策略显式排除了该目录，并启用两份 Python adapters 的已有前端。最终计数以保存快照的 333 份文件为准。文件解析成功只表示当前前端接受了语法，不表示调用全部解析或功能得到证明。

图中共有 **10,999 个节点、60,146 条调用边**。内部确定调用 `resolved` 为 23,099 条，已识别外部调用 `external` 为 18,285 条，`dynamic` 为 18,179 条，`ambiguous` 为 428 条，`unresolved` 为 155 条。18,762 条后三类调用保持未知；11,808 个已识别外部回调边界是外部边上的额外不确定性标记，不能再与边总数相加。两种完整性标志 `coverage_incomplete` 与 `call_resolution_incomplete` 都为 `true`。

### 十项源码基准的实际核对

十项基准的源、目标节点均存在。前八项全部重现了人工读取到的确定连接，不能仅因“没有缺失发现”算通过；下表列出保存快照中的具体边 ID 和调用位置，完整节点与源码行文本可在见证文件中读取。

| 规则 ID | 最终见证与结果 |
|---|---|
| `cpb-observed-cli-project-argument` | `83d1e4de49e6c03482ef5a94`，`cli/cpb.ts:167`；确定直接边 |
| `cpb-observed-task-result-rendering` | `3f05e38de9bb5c3a48fddaf9`，`cli/commands/task.ts:172`；确定直接边 |
| `cpb-observed-fix-shared-result-renderer` | `5cdd4d800d16e1b90a9a0d64`，`cli/commands/fix.ts:352`；`.js` 导入成功绑定到 `.ts` helper |
| `cpb-observed-server-engine-delegation` | `4df4ad4b942785c1dd1e80df`，`server/services/engine-runner.ts:157`；确定跨文件边 |
| `cpb-observed-runjob-crash-wrapper` | `8a62b9a8fbd15a264d220870`，`core/engine/run-job.ts:75`；确定直接边 |
| `cpb-observed-checklist-materialization` | `a8b37a8e02050a05938fed5a`，`core/engine/run-job.ts:159`；确定跨文件边 |
| `cpb-observed-runjob-to-dag-path` | `8a62b9a8fbd15a264d220870` + `7aee7dad0a2229111bb0a128`，`run-job.ts:75`、`:177`；`runJob → runJobInner → executeWorkflowDag` 两跳确定路径 |
| `cpb-observed-task-view-sanitization` | `341c5bccfbdf59626f83cf08`，`server/services/task/task-view.ts:708`；确定跨文件边 |
| `cpb-capability-dynamic-command-boundary` | 两端点存在，未伪造 `main → task.run` 确定路径；规则为 `uncertain`。`80eae50cb1e0a4537c489901` 保留 `cli/cpb.ts:154` 的动态 `import(path.join(...COMMANDS[cmd]))`，`d931c96f87c720652cb5d5b2` 保留 `:186` 的 `mod.run`；这不是单靠全局覆盖缺口得到的未知 |
| `cpb-observed-pure-result-helper-no-engine-call` | 两端点存在，无 `humanResultLine → runJob` 确定直接边，helper 也无未知出边；规则仍为 `uncertain`，证据包含 7 项全局覆盖缺口。符合未报告确定违规的保守边界，但不能算成已完成的全局否定证明 |

**8/8 只描述本次选定的正向源码连接重现情况**；它不是检出率，也不证明所有调用提取正确。第九项说明动态分派边界被保留，第十项暴露全局解析缺口会使局部负向检查保守未知。该样本不能用于宣称“10/10 功能通过”或“仓库缺陷检出率 100%”。

### 前端缺口与发现含义

三份 TypeScript 前端解析失败文件为：

- `core/indexing/local-code-index/gc.ts`：诊断行 225、378、390、441、453、495，包含 inline import 类型的语法能力缺口。
- `core/indexing/local-code-index/rules/types.ts`：诊断行 30，当前 grammar 无法处理该处声明语法。
- `shared/primitives/process-tree.ts`：诊断行 952，包含 inline import 类型的语法能力缺口。

这些是当前静态前端拒绝/未覆盖的语法，未经编译或执行不能称为目标源码错误。三份 Shell 文件保持 `unsupported`。此外，`scripts/workflows/local-code-index-v2.js` 与同名 `.ts` 共享去扩展名后的模块身份，诊断保留了模块与定义歧义；工具没有把这一重名消解成确定本地目标。

总计 40,388 条发现按性质分为：

| 发现类型 | 数量 | 可作出的结论 |
|---|---:|---|
| 未知调用 | 18,762 | 调用解析缺口，不能断言遗漏实现 |
| 外部回调边界 | 11,808 | 路径可能经外部实现重入，需要保留模型边界 |
| 疑似不可达 | 9,763 | 未从五个选定入口确定到达；入口与图均不完整，不能称为死代码 |
| 递归结构 | 51 | 静态自调用关系，不能判断不终止 |
| 多节点调用环 | 2 | 静态结构环，不能直接判断递归错误 |
| 人工基准规则的未知结果 | 2 | CLI 动态路径与 helper 负向边检查均未确认违规 |

**本轮没有从这些基准发现确认 CodePatchBay 的真实功能缺陷。** 这表示没有获得足以支持该结论的证据，不表示项目不存在问题。大量未知与入口提示是分析覆盖信息；若把它们全部涂成故障热力图，会重现原架构想消除的噪音。界面需要把规则违规、确定结构事实与分析缺口分别解释。

### 工具可用性结论

首轮真实扫描暴露了证据重复膨胀：每条疑似不可达发现反复附带完整入口闭包缺口，导致扫描无法完成。检测器 `call-rules-2` 将每条发现的缺口展示限制为 8 条，同时保留原缺口数量、截断标记与完整快照出处；未知判断仍基于完整证据。采用该修正的本轮扫描已成功保存与导出。

路径与子图查询也可能重复返回巨大的缺口集合，现将交互响应的 `gaps` 限制为 20 条，保留 `gap_count`、`gaps_truncated`、`gap_sample_limit`、`gap_snapshot_id` 与完整事实来源。该修正只限制展示，不改变搜索范围、检测事实或当前快照版本。大快照的全量加载与深层子图节点/边规模仍是后续可用性边界，本轮没有给出性能验收结论。

本次实际完成的是：完整配置范围的源码捕获、支持语言的静态构图、可追溯的确定连接、显式未知以及规则相对结果。当前实现适合作为部分架构连接的检查与证据浏览工具；若产品承诺是“仅凭调用链保证代码功能完整性”，本轮证据不支持这一承诺。要进一步减少未知，下一步应优先补充静态语法支持、明确的回调/注入绑定或架构契约，再扩大前端覆盖，仍保持目标代码零执行。
