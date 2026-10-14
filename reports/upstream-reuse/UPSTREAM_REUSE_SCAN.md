# CallScope v0.3：上游代码接入与真实源码扫描

Axon 图核心和官方 CocoIndex 引擎已进入实际调用路径。Axon 用于确定调用邻接、路径查询和检测；CocoIndex 1.0.25 用于固定静态语言前端的持久 memo。接入说明见 [UPSTREAM_REUSE](../../docs/UPSTREAM_REUSE.md)，独立审查见 [INDEPENDENT_REVIEW](INDEPENDENT_REVIEW.md)。

## 已观察的普通工具使用

每个仓库以相同静态 policy 连续扫描两轮。第一轮解析并发布，第二轮复用前端缓存，全项目检测仍重新计算。两轮的快照 ID 一致，第二轮 `created=false`，没有重复发布。维护计数保存于操作记录，不写入同 ID 的不可变图事实。

| 仓库 | 选入 / 完整解析 / 未完整解析文件 | 节点 / 边 | 人工正向源码关系重现 | 第二轮复用语言 |
|---|---|---|---|---|
| codepatchbay | 333 / 327 / 6 | 10,999 / 60,146 | 8 | python, typescript |
| winwincode | 471 / 459 / 12 | 31,941 / 170,176 | 9 | python, rust, typescript |

WinWinCode 的 Python bundle 是 0 文件；有实际源码的复用为 TypeScript 与 Rust。CodePatchBay 的 6 份未完整分析文件包含 3 个 TypeScript 语法缺口和 3 个不支持的 Shell 文件。WinWinCode 保留 12 个解析缺口，包含关键组合入口 application.ts。两份快照都为 `partial`；接入基础库没有自动补齐这些语言能力。

## 覆盖率口径与当前发现

下面的数字来自本目录保存的 v0.3 summary，而非目标测试或执行覆盖率。

| 指标 | CodePatchBay | WinWinCode |
|---|---:|---:|
| 选入文件完整解析率 | 327 / 333 = 98.20% | 459 / 471 = 97.45% |
| 已提取调用绑定到项目内确定目标的比例 | 23,099 / 60,146 = 38.40% | 16,357 / 170,176 = 9.61% |
| 识别为外部调用的数量 | 18,285 | 24,269 |
| dynamic / ambiguous / unresolved 调用总数 | 18,762 | 129,550 |
| 调用环结构 / 直接递归结构 | 2 / 51 | 4 / 9 |
| 预先选择的 10 项源码关系观察 | 8 项确定连接，2 项未知 | 9 项确定连接，1 项未知 |

文件率的分母是 policy 选入范围，排除了测试目录、工具状态和部分生成内容，不是仓库全部文件。调用率的分母是分析器已经提取的调用点，包括外部、动态调用及 Rust 宏等表达式；没有全项目调用点真值，所以该指标不是调用检出率。外部调用没有展开实现，不能当作项目内完整链路。所选 10 项是小规模源码观察，不是随机样本，也不是功能覆盖率或准确率基准。

已确认的正向结构包括 CodePatchBay 的 `runJob → runJobInner → executeWorkflowDag` 和 WinWinCode 的 Rust CLI `main → default_state_root`。CodePatchBay 的 CLI 动态 import / `mod.run` 路由仍未知；WinWinCode 的 `application.ts` 含当前语法库未完整支持的 inline import type，导致关键入口关系不能确认。WinWinCode 的 Rust 已提取调用仅 7.88% 绑定到项目内确定目标，实例方法、trait、宏、闭包及运行时机制是主要能力缺口。

调用环和递归仅是确定静态结构，不等于不终止或功能缺陷。源码复核例子：CodePatchBay 的 `listJobs ↔ listJobsAcrossRuntimeRoots` 按 `dataRoot` 分支；WinWinCode 的 `freeze_source ↔ resolve_current_candidate_with_source` 在进入前序状态时检查 revision 严格下降。因此不能把这些发现数量报成 bug 数量。现有产物尚没有经复核确认的功能缺失或调用漏接结论；全项目代码功能完整性覆盖率也无法据此给出。

读取保存的 v0.3 图，再核对 v0.2 已保存的 10 项人工源码关系观察：两库均 10/10 的端点、路径、边、源码引文和未知状态相同；source_hash 与 policy_hash 也相同。正向关系分别重现 8 项与 9 项。其余关系保留不确定，未作为缺陷或功能通过结论。源码观察并非仓库作者批准的功能需求。

本轮只执行 CallScope 自身的解析、静态查询和证据导出，没有运行任何测试套件，没有执行、导入或构建目标代码，没有安装目标依赖。两个目标仓库 Git 工作区仍干净。浏览器、安装包构建、文件增删改名后的实际更新和失败恢复路径未运行验证；后两类失效机制已由独立源码审查核对。

## 保存产物

- [CodePatchBay 冷/热扫描记录](codepatchbay-integration.json)、[精简分析结果](codepatchbay-summary.json)、[静态调用证据](codepatchbay-rule-witnesses.json)、[与旧证据对比](codepatchbay-witness-comparison.json)。
- [WinWinCode 冷/热扫描记录](winwincode-integration.json)、[精简分析结果](winwincode-summary.json)、[静态调用证据](winwincode-rule-witnesses.json)、[与旧证据对比](winwincode-witness-comparison.json)。
- 两库 v3 SQLite 快照及 CocoIndex 持久缓存位于本目录；历史 v2 产物保留在 real-repositories/，没有改写。

## 可替换与扩展边界

缓存目前按语言整体失效，语言内增删改名或内容变化会重新解析和绑定该语言全部文件。有效配置、工具源码、实际 worker 的语言前端、Python/语法组件及 CocoIndex 版本进入计算身份。每轮仍捕获完整文件集合，检测每轮全量。可以显式用 `--engine full` 关闭 memo；所有引擎仍使用 Axon 图核心。

当前语言前端彼此独立，跨语言运行关系保持未知。未来加入 FFI、生成代码或共享类型推断时，必须扩展依赖输入，不能继续假设语言间互不影响。没有采用三跳失效边界，没有复制上游的模糊调用判断来制造确定证据。
