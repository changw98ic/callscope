# n0vel：现有 CallScope v0.14.0 的真实源码评估

本次验证现有工具能否分析一个新项目。结论：**扫描和报告命令正常完成，但当前工具不具备评估 n0vel 主体功能链的能力。** 项目主体使用 Dart；891 个 Dart 文件没有进入源码捕获，`lib/` 的 536 个实现文件语法解析覆盖为 **0/536**。不能把附属脚本的扫描完成写成项目分析通过。

目标：[changw98ic/n0vel](https://github.com/changw98ic/n0vel)，`master` 提交 `f846a62ecdd03158dbd5bff34e1afb7b816d10f9`。只读克隆位于 `/tmp/callscope-n0vel-evaluation/target`。当前工作区磁盘空间不足以容纳此仓库，所以克隆与临时运行结果使用空间充足的 `/tmp`；本目录另行保存报告、证据、文件哈希清单和已关闭的扫描数据库。

工具保持已发布 v0.14.0 原样，65 个 Python 核心文件与冻结记录一致，工具源码身份为 `a198491ce936c91ce7a1c848789cf9fb27c5fc720b90ae81725c2ddf65f779dc`。本次未增加 Dart 适配器、专用判断合同或检测器，没有将人工审查结论回填为自动发现。

## 实际执行与自动结果

启用现有全部三种语言 Python、TypeScript（含 JS）、Rust，源码根为整个仓库，其余使用默认配置。完成两次 `full` 静态扫描以及正常 CLI 的 JSON/Markdown 报告导出。命令与返回码见 [COMMAND_RECORD.json](COMMAND_RECORD.json)，配置见 [scan-config.json](scan-config.json)。

| 项目 | 保存结果 |
| --- | --- |
| Git 跟踪文件 | 1,075 |
| Dart 源文件 | 891；343,554 物理行 |
| `lib/` Dart 实现 | 536；197,559 物理行；捕获/解析均为 0 |
| `test/` Dart 源码 | 318；仅盘点，未运行 |
| `tool/`、`scripts/` Dart | 36、1；均未捕获 |
| 工具实际选入 | 29 个已登记扩展名文件 |
| 实际解析 | 6：5 个 Python、1 个 JS；全部是附属脚本 |
| 已登记但不支持 | 23：C、C++、Swift、Shell |
| 自动调用图 | 44 节点、282 条调用；102 resolved、103 external、77 dynamic |
| 自动发现 | 122 条，全部 uncertain：77 unresolved_call、45 external_callback_boundary |
| 自动确认的功能缺陷 | 0；没有证据证明目标无缺陷 |
| 完整条件判断、功能链合同 | 均未配置，自动报告未形成主体功能判断 |
| 功能覆盖率、检出率、误报率 | 均未知；不从文件或发现计数推导 |

正常自动报告见 [baseline-report.md](baseline-report.md) 和 [baseline-report.json](baseline-report.json)。完整扫描见 [baseline-scan.json](baseline-scan.json)。这些原始结果保持原样，不能把本报告补充的 Dart 文件清单误认为现有产品已自动输出该清单。

快照 `3b37d1364b982bf3ddde3ff89db3b3d426a8b40b25dae818d9070b68cf8ace7c`；两次全量扫描的完整保存快照与 findings 一致，第二次 `created=false`。这只验证静态结果可重复和重复发布去重，不是目标代码运行验证，也不是缓存性能结果。

## 本次明确暴露的 CallScope 缺口

1. **主体语言缺失。** `callscope/config.py:53` 仅允许三种现有语言，没有 Dart 前端，无法构建 Flutter 主体的调用、字段和异常控制流关系。
2. **源码范围静默遗漏。** `callscope/source_reader.py:12` 的 `EXTENSIONS` 未登记 `.dart`，第 62–64 行仅把已知后缀加入 candidates。因此 891 个 Dart 文件既未捕获，也没有进入 unsupported 清单。`project_report.py:380` 的范围统计基于已捕获文件，只会展示 29/6，遗漏项目主体这个事实没有被产品直接披露。
3. **版本身份同样受范围限制。** `analysis.py:216` 的 source hash 基于已捕获源码和 scope。未被捕获的 Dart 内容变化不会进入该源码内容身份；不能宣称本次快照代表全部 n0vel 实现。这里依据当前代码结构作判断，没有修改目标制造试验。

本次快照已标为 partial，现有自动报告也明确拒绝功能完整率推断，所以没有观察到产品直接宣告“全仓库通过”。实际问题是主体文件没有进入盘点，少量附属脚本不能弥补这个盲区。

## 单独的人工源码审查

以下由独立只读审查提出，主代理核对了对应调用、字段、状态和异常路径。**三项均不是 CallScope 自动检测成果，也未运行复现。** 证据按目标固定提交、完整文件 SHA256、行号和原文摘录保存在 [MANUAL_SOURCE_REFERENCES.json](MANUAL_SOURCE_REFERENCES.json)，结构化判断见 [MANUAL_REVIEW.json](MANUAL_REVIEW.json)。没有穷举全项目。

### NV-MANUAL-01：启动保存失败后，运行占用没有清理

从 idle/completed 等非 running、非 blocked 状态开始同场景生成，初始快照持久保存抛错时，可得到以下异常路径：

`WorkbenchOrchestrator.prepareAiGeneration` → `runCurrentScene` → `_beginRun` → `_setSnapshot` → `_persistSnapshot` → `StoryGenerationRunStorage.save`。

- `story_generation_run_store.dart:319` 先取得运行 token；第 876–880 行立即设置占用。异常捕获直到第 408 行才开始。
- 第 350 行先等待初始 `_setSnapshot`。`story_generation_run_snapshot_persistence.dart:82` 先等待保存，第 87 行才更新内存 snapshot。保存失败时，旧状态保留。
- 随后同场景重试被 `story_generation_run_store.dart:294` 的占用判断直接返回；取消又被第 627–644 行对 running/blocked 的判断拒绝，不能清理 token。
- 上层 Workbench 的 finally 只清理自身 `_isGeneratingAi`，没有清理 run-store token。

**静态条件推导：**初始保存失败可能造成当前 store 实例的同场景生成停滞，即使保存服务稍后恢复，直接重试仍可能被旧 token 阻止。建议把 token 获取后的准备与保存纳入统一异常清理，并使清理核对所属 token，避免误清其他运行。

**反证与边界：**初次保存成功后 snapshot 已为 running，取消通常可清理。启动另一场景、项目生命周期重置、重建 store 或重开应用可以恢复，不能描述为永久锁死或已动态复现。

### NV-MANUAL-02：改稿请求进入生成，但没有进入 feedback lease 消费

`AuthorFeedbackStore.activeRevisionRequestsForScene` 第 57–67 行选出 revisionRequested 请求；run-store 第 322–336 行将其传入生成材料，scene-brief 第 22–33 行实际传入 note 文本。

候选采纳时，`story_generation_run_store.dart:725` 创建的 `GenerationCommitRequest` 没有传 `feedbackLeases`；该字段在 `generation_ledger_models.dart:487` 默认为空。`generation_commit_coordinator.dart:684` 因空 lease 直接返回空文档，第 1435 行跳过保存。在 `lib` 范围的词法搜索只找到 `claimFeedbackLeases` 和 `markRevisionRequestsInProgress` 的定义，没有调用引用。

**确定源码事实：**这条生成→采纳路径没有通过现有 lease 机制把已纳入生成的反馈请求消费为 accepted，仍处于 revisionRequested 的请求下次还会被选择。

**条件风险：**只有要求“采纳候选即自动消费对应请求”时，这才构成功能闭环缺口；代码自身不足以确定这一产品合同。`AuthorFeedbackStore.accept/resolve` 第 199–204 行存在独立手动处理路径，不能把未传字段直接定性为无条件业务错误。建议明确合同；如需自动消费，应传递反馈身份和版本/lease，而不只传 note 文本。

### NV-MANUAL-03：已提交后的展示保存失败，被提示为采纳未完成

`generation_commit_coordinator.dart:185` 已 COMMIT，随后返回成功；run-store 第 748 行还会等待另一次 `_setSnapshot`。若这次展示状态保存抛错，上层 `workbench_orchestrator.dart:389` 进入一般失败提示“候选采纳未完成”。run-store 第 758 行开始的 outbox 调度在该 await 之后，本次不会到达。

**静态条件推导：**持久提交事实与用户看到的失败提示可能不一致，并跳过本次派生索引调度。建议在提交回执已成功后单独处理投影保存失败，保留“已提交、展示/索引待恢复”的明确状态。

**反证与边界：**作者事务和 outbox 行已经持久提交，不代表部分事务提交或正文丢失；第 81–89 行的同 key 回执重试能返回既有结果，outbox 本身可重试。不声称索引永久丢失。

### 已查到的保护，不能省略

候选 finalizer 有非空正文、review、质量与精确文本证据检查；质量有限模型要求 overall ≥95、关键维度 ≥90。采纳 coordinator 使用同连接 BEGIN IMMEDIATE、资料和草稿 CAS、幂等回执，把正文、版本、批准写入、回执、run 状态和 outbox 纳入事务。没有据此发现正常路径绕过质量门，也不能仅凭类或函数存在就证明所有异常路径完整。

## 这次评估对项目目标的意义

两库原报告范围的阶段成果不能证明跨语言、跨项目通用性。本次新样本直接证明：现有 v0.14.0 无法用于 n0vel 主体的功能完整性判断。主要差距是语言接入、范围披露和语义关系分析，性能不影响这个结论。

后续优先顺序应为：先让项目源码盘点明确披露不支持的主体语言与未捕获文件；再接入 Dart 的导入、part、符号和方法/回调关系；随后让公共分析层处理异常退出的占用清理、提交与投影边界、字段到消费者的关系。不得把上述三条人工结论写成检测器预设答案。若后续针对本样本开发，n0vel 只能作为冻结回归样本，新的泛化判断还需其他未用于规则设计的源码。

## 保存和约束

[EVALUATION.json](EVALUATION.json) 保存身份与统计；[SOURCE_INVENTORY.json](SOURCE_INVENTORY.json) 保存所有 Git 跟踪文件的路径、字节大小和哈希；`baseline.sqlite3` 是 CLI 正常发布后已关闭的本地数据库，不用于公开分发。

本轮仅增加本报告目录下的分析产物。没有修改 n0vel 或 CallScope 核心，没有代码简化。未执行/导入目标模块，未运行目标或工具测试套件，未构建或安装目标依赖。自动扫描退出码为 0 只说明工具命令完成；**n0vel 主体分析能力评估为不支持，不是目标功能通过。**
