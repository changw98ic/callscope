# Axon / CocoIndex 上游代码复用

本文对应 CallScope v0.14.0；Axon/CocoIndex 的复用起于 v0.3，固定来源与许可保持。Axon 图核心进入路径查询和检测器的确定邻接索引；CocoIndex 官方库可选维护语言前端结果的持久 memo。项目源码仍只作为已捕获的文本数据，不导入目标模块、不执行目标代码、不运行测试或构建。

当前 scope2 的[核心与策略已冻结](../reports/astra-iteration12-scope2/CORE_FREEZE.json)，两库正常纯静态冷/热分析及正式报告已保存、数据库已关闭。正式轮次使用 `full` 引擎，两轮均重算且各库同 ID、created=true/false；不把历史 CocoIndex 缓存记录当成本轮缓存收益或功能验收。

## 实际复用位置

| 上游 | 固定身份 | 本地代码 | 进入实际流程的职责 |
|---|---|---|---|
| Axon | 提交 `2b386fb38a468201ab2ec825ddea5ebf4c33f513`，上游版本 `1.0.1` | `callscope/_vendor/axon/model.py`、`graph.py`；适配器 `axon_adapter.py` | 节点标签、关系类型、有向邻接索引；`GraphIndex` 的确定内部调用邻接由此生成 |
| CocoIndex | 官方包 `cocoindex==1.0.25` | `cocoindex_runner.py`、`cocoindex_worker.py` 使用官方发行库 | `@coco.fn(memo=True)`、`Environment`、`App.update_blocking` 持久复用语言前端结果 |

Axon 来源为 [harshkedia177/axon](https://github.com/harshkedia177/axon)。仅两个图核心文件随 CallScope 保存，改动为 `graph.py` 的模型导入改为包内相对路径，以及两个文件的末尾空白格式。`UPSTREAM.json` 保存来源、改动和本地文件哈希，`pyproject.upstream.toml` 保存上游许可与作者声明。

`GraphIndex` 先按 CallScope 的解析规则选择确定内部调用，再交给 `AxonCallGraph`。动态目标、外部边界、候选关系、重复定义和缺失端点不能进入确定邻接。适配层从上游图的索引取得相邻关系，并保持原始 CallScope 节点/边身份与排序；运行时图对象不写入快照。符号解析、路径语义、未知传播和规则判定仍属于 CallScope。未接入 Axon 的其他解析器、死代码推断、LLM、CLI 或 watcher。

CocoIndex 来源为 [cocoindex-io/cocoindex](https://github.com/cocoindex-io/cocoindex)，发行 tag `v1.0.25` 指向提交 `17c84f1a0f9bc5b0b4e1d8ebabb28bde79c4afa3`。使用官方 binary wheel 和 Python API，没有为本轮构建其 Rust 核心。安装于工具环境，目标项目不安装依赖。CallScope 未配置 CocoIndex 的 LLM、嵌入、网络数据连接器或目标执行入口。

v0.14 的条件式状态沿袭/发布边界、有限职责解释和文档部署对照由 CallScope 的固定分析模块完成。它们复用保存源码、词法身份、现有调用绑定及显式有限模型，未接入更多 Axon 源码分析器，也未把 CocoIndex 变成跨文件语义失效或异常检测引擎。实际字段/条件、操作交接、文档限定与 unknown 是分析证据；上游图索引或缓存命中不替它们授予结论。

## 引擎选择与工具进程

`scan`、`serve`、`mcp` 接受 `--engine auto|full|cocoindex`。默认 `auto`：找到本工具 `.analysis-tools/runtime/bin/python`，或当前 Python 安装目录中的 CocoIndex 1.0.25 时使用 CocoIndex；否则使用全量前端。显式 `full` 禁用前端缓存；显式 `cocoindex` 缺少工具依赖时失败。选定 CocoIndex 后若运行失败，不静默降级到全量引擎。

可从 CallScope 根目录安装工具依赖：

```sh
python -m pip install '.[languages,maintenance]'
python -m callscope scan examples/order_service --engine cocoindex --json
python -m callscope serve examples/order_service --engine cocoindex --watch
```

本工作区已有 `.analysis-tools/runtime` 隔离工具环境，实际依赖版本记录于 [requirements-maintenance.lock](../requirements-maintenance.lock)。这些命令属于工具安装或纯静态分析，不运行被分析项目。`full` 的 Python 分析不需安装额外包，Axon 图核心随工具提供。

父进程全量安全捕获源码，通过 stdin JSON 交给固定 worker，worker 用 `python -I` 启动。隔离模式限制 Python 导入搜索路径；worker 显式加载本工具包，消费已捕获文本，运行固定注册的静态前端。项目配置是数据，不能定义变换代码或可执行插件。

父进程校验请求指纹、工具身份、引擎协议、语言集合、返回文件集合、内容及哈希；worker 在缓存查找前初始化需要的语法解析器。主进程与 worker 实际 Python/前端/语法库版本分别参与相应输入身份，不能用主进程版本冒充 worker 版本。

## 当前缓存粒度

每个请求语言的全部选入 `SourceFile` 组成一个 bundle。CocoIndex memo 参数包括语言、项目根、完整文件记录、完整分析配置以及工具/解析组件身份。

- 同一语言内文件增删、改名或内容变化，重算该语言整个 bundle，重新处理其跨文件绑定。
- 未变语言可复用其 bundle；完整配置、工具源码或实际组件版本变化也使缓存键变化。
- 缓存身份包含文件路径、内容/哈希、读取状态、模块信息，不能只按 commit 或文件 mtime 判断。
- `read_error` 所在语言直接计算但不写入 memo，避免永久缓存一次读取失败。
- 源码语法失败可作为绑定输入的部分静态结果保留；解析器初始化/运行失败属于任务失败，不缓存成正常分析证据。
- 每轮重新组装完整快照、处理失败源码影响，再全量运行规则、可达性及调用环检测。

这是一种语言整体的计算复用。周期监听仍全量捕获源码，没有实现逐文件 AST 语义缓存、受影响子图检测或固定三跳传播。缓存命中不能说明目标功能通过，本文不发布性能收益或结果等价性验收结论。

CocoIndex 缓存路径为快照数据库绝对路径后加 `.cocoindex`，与发布快照的 SQLite 分开。缓存包含源码及派生结果，按源码敏感程度保管；缓存失效或任务失败不会改写已有快照。

## 身份、发布与扩展

`analysis_inputs.tool_identity()` 对 CallScope 包内全部 Python 源文件计算内容身份，包含随包 Axon 文件；同时记录 Axon 固定提交和适配器版本。`stats.component_versions.tool` 保存该身份，`maintenance` 保存后端版本/协议/粒度，语言项保存实际执行前端的版本。规范组合进入 `parser_version` 及快照 ID。不同引擎的身份可以不同，不能把跨引擎快照自动当成同一输入。

`recomputed_languages`、`reused_languages`、`uncached_languages` 等运行计数仅在 `publication.maintenance` 和服务状态中，不写入不可变 `stats`，所以冷缓存和热缓存不会因计数差异破坏同一快照的幂等发布。

服务运行期间工具源码变化会拒绝新的扫描，需要重启服务后再分析；分析期间身份变化或 worker 失败不发布新快照。快照、发现和最新指针仍由 CallScope 的 SQLite 事务原子发布，CocoIndex 缓存没有代替快照证据仓库。

新增前端应接入固定注册表、组件版本和源码身份，并定义其语言内跨文件绑定边界。进一步细化缓存前，需设计新增/删除/重命名、导入重绑定及未知传播的失效协议；当前语言 memo 不构成通用的增量检测证明。

## 许可证与历史记录

Axon 上游声明 MIT，固定提交没有独立 LICENSE 文件。本工具保存标准 MIT 条款和上游作者署名，并明确该文件不是上游 LICENSE 的复制品。CocoIndex 为 Apache-2.0，完整条款及官方 wheel 自带依赖声明分别保留。详细依据见 [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md)。

`reports/real-repositories/` 中两个真实仓库的 v0.2.0 快照、数值和独立审查是历史产物，不因后续接入改写。新版引擎的正常源码扫描也不能称为目标代码测试通过。本轮不执行目标、测试或构建。


v0.3 接入时完成的首次计算与再次缓存复用见历史 [接入扫描记录](../reports/upstream-reuse/UPSTREAM_REUSE_SCAN.md) 和 [当时独立审查](../reports/upstream-reuse/INDEPENDENT_REVIEW.md)。各 10 项历史源码观察的结构、源码引文和未知状态保持一致，只覆盖所选观察，不是目标功能验收，也不构成当前重复审查门。v0.14 正式结果已另存 [scope2 目录](../reports/astra-iteration12-scope2/)，与这份历史记录分开。
