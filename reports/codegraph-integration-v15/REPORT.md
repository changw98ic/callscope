# CodeGraph 全语言接入与真实源码静态验证

CallScope v0.15.0 已把 CodeGraph 的全部语言提取源码、固定语法资源及公开的候选解析策略接入正常扫描流程。保留原来的三个前端，新增 35 个语言/格式 ID，共 38 个规范 ID。此次完成的是语言接入与有边界的结构分析；没有据此宣称全项目功能完整性已经解决。

固定上游为 [colbymchenry/codegraph](https://github.com/colbymchenry/codegraph) 的 `8f1f842b5b828175992d2ce2cdf673b955b2cce9`。323 个来源文件逐字节匹配，78 个扩展名映射全部接入；31 份压缩 WASM 对应 32 个语法变体，全部完成加载检查。来源、资源身份与各自版权条款一并保存，见 [复用说明](../../docs/CODEGRAPH_REUSE.md)。加载检查不表示每种语言已用真实项目验证。

## 正常产品流程中的变化

- 默认 `analysis.languages=["all"]`；已有配置显式选择的语言保持其选择。Python、TypeScript/JavaScript 家族、Rust 沿用原前端。
- 读取器先安全捕获源码，再将相对路径、文本及哈希交给固定分析 worker。目标根目录不传给 Node；解析策略只访问捕获输入，不加载目标模块或依赖。
- 在分语言构图之前，复用上游内容识别校正 `.h` 和 `.inc` 的实际语言。本样本两个 Windows C++ 头文件由 C 分组改为 C++。识别失败会保留诊断与覆盖缺口。
- 新增节点、结构、导入、类型及调用候选进入持久快照。所有 CodeGraph 调用关系保持不确定，唯一候选或较高 confidence 均不升级为确定调用。上游 confidence 是排序依据，不是正确率。
- 普通报告、HTTP/MCP 共用报告生成器，展示逐语言状态、候选与未绑定站点，以及完整边 ID、源码位置和目标候选。网页可按新语言过滤、下钻；图接口同时返回不含文本的文件分类。
- `parsed`、`captured_metadata`、`structural_extracted`、`parse_error` 分列。未知扩展名进入路径盘点，避免主体语言再次静默遗漏。组件完整版本保存在快照中，重复证据使用其 SHA256 身份。

## n0vel：相同固定提交的前后比较

目标为 [changw98ic/n0vel](https://github.com/changw98ic/n0vel)，提交 `f846a62ecdd03158dbd5bff34e1afb7b816d10f9`。没有修改目标源码、执行或导入目标模块，没有运行测试、构建或安装目标依赖。`test/` 文件只作为源码捕获和解析。

| 项目 | v0.14 历史基线 | v0.15 正式扫描 |
| --- | ---: | ---: |
| Git 跟踪文件 | 1,075 | 同一固定提交 |
| 已识别文件 | 29 | 927；另有 148 个未识别路径明确列出 |
| 完整语法解析 | 6 | 881 |
| Dart 文件进入捕获 | 0 / 891 | 891 / 891 |
| Dart 完整语法解析 | 0 / 891 | 864 / 891，约 97.0% |
| `lib/` Dart 完整语法解析 | 0 / 536 | 513 / 536，约 95.7% |
| 图节点 | 44 | 19,126 |
| 保存的调用类引用 | 282 | 94,851 |
| 确定调用 | 102 | 102；全部来自原前端 |
| 自动确认的主体功能缺陷 | 0 | 0 |

**这些比例是文件语法解析覆盖，不是功能覆盖率。** Dart 仍有 27 个语法不完整文件，其中 `lib/` 23 个、`test/` 3 个、`tool/` 1 个；保留其局部结构，不将其计入完整解析。解析缺口、未绑定调用和不支持的输入使快照保持 `partial`。

| 实际观察到的语言/格式 | 选入 | parsed | parse_error | 其他状态 |
| --- | ---: | ---: | ---: | --- |
| Dart | 891 | 864 | 27 | — |
| C | 5 | 2 | 3 | — |
| C++ | 10 | 5 | 5 | — |
| Swift | 4 | 4 | 0 | — |
| Python | 5 | 5 | 0 | — |
| TypeScript/JavaScript 家族 | 1 | 1 | 0 | — |
| YAML | 7 | 0 | 0 | 7 captured_metadata |
| Shell | 4 | 0 | 0 | 4 unsupported |

Dart 保存 18,943 个节点与 94,335 个调用类引用位置，39,466 个位置有目标候选，54,869 个未能绑定；“调用类引用”还包括实例化和函数引用，具体类型保存在边上。全部为候选或未知关系，未形成确定调用路径证明。非调用关系保存在节点元数据中，不能用其数量充当已确认调用数。

本轮 94,691 条自动发现全部为 `uncertain`：94,646 条 `unresolved_call` 与 45 条 `external_callback_boundary`。它们披露分析边界，不是 94,691 个功能缺陷。未配置 Dart 功能合同；此前人工报告的三项候选风险没有被本次检测器自动重现，原事实、条件和反证继续见 [v0.14 评估](../n0vel-evaluation-20261015/REPORT.md)。功能覆盖率、缺陷检出率和误报率均未知。

正式全量快照：`7165ea038f8a8783b2f1a0c8f0075d9cd84e784ebde6a9f84c10e850076b7dea`。完整状态及逐文件哈希见 [snapshot-summary.json](snapshot-summary.json) 和 [captured-source-index.json](captured-source-index.json)。

## 旧前端兼容性

对 codepatchbay、winwincode 按原策略捕获一次真实源码，旧冻结前端和新前端分别读取相同文本。801 个文件、43,492 个节点、232,510 条边的完整记录与 metadata、文件状态、diagnostics、native stats 逐记录哈希一致；不是仅比较数量。原有 Rust 六个解析缺口保留。

详见 [兼容性说明](NATIVE_FRONTEND_COMPATIBILITY.md) 与 [完整比较记录](NATIVE_FRONTEND_COMPATIBILITY.json)。这没有重跑旧合同、goal 或全文报告，不能替代原报告级目标的重新验收，也没有验证实际样本未出现的 `.pyw`、`.xsjs` 输入。

## 尚未验证的范围

38 个规范 ID 包含语言、模板和元数据格式。本轮合并 n0vel 的源码扫描与两库原前端比较，实际观察到八个 ID，其中 YAML 仅为元数据层；其余 30 个尚未用真实项目扫描。它们的源码已接入，对应 WASM 若存在已检查加载，但不声称已在真实项目验证。

逐项状态见 [LANGUAGE_VALIDATION.json](LANGUAGE_VALIDATION.json)。新语言尚未接入原 TS/Rust 的字段 IR、异常清理、条件判断及有限交错模型。框架发现、跨语言调用、动态分派和私有上游解析路径的边界仍保留。下一步功能分析需要在这些源码事实之上继续建立公共语义关系，不能把本轮语言接入写成完成了通用功能完整性判断。

## 保存与复查

[CORE_IDENTITY.json](CORE_IDENTITY.json) 保存正式工具身份与源码哈希；[runtime-capabilities.json](runtime-capabilities.json) 保存语法加载结果；[source-registry-inspection.json](source-registry-inspection.json) 保存上游源码与扩展映射核对。

正常 CLI 生成的项目报告见 [n0vel-report.md](n0vel-report.md) 和 [n0vel-report.json](n0vel-report.json)。完整 scan 导出按原始字节压缩保存为 [n0vel-scan.json.gz](n0vel-scan.json.gz)，没有从正常导出中删减已保存的源码、节点、边或发现；原始大小与 SHA256 见 [SCAN_ARCHIVE.json](SCAN_ARCHIVE.json)。在本目录恢复：

```sh
gzip -dc n0vel-scan.json.gz > n0vel-scan.json
```

数据库和 CocoIndex 缓存留在 `/tmp/callscope-codegraph-build/formal-v15/`，不进入 Git。命令、重复发布与缓存观察另见 [COMMAND_RECORD.json](COMMAND_RECORD.json) 和 [EVALUATION.json](EVALUATION.json)。正式六项命令均成功。初轮辅助脚本的换行转义错误及修正记录另存 INITIAL_COMMAND_RECORD.json；其后补齐 Node 精确版本身份并重新执行了正式流程。目标与原冻结报告未被改写。

正式验证结果：全量重复发布 `created=false`；默认 CocoIndex 冷扫描创建独立身份的快照，暖扫描 `created=false`、38 个语言缓存项复用（含空语言结果，七个前端具有本样本输入）。两种引擎的源码、节点、边、诊断、配置、辅助输入及发现语义指纹相同。完整对照见 [FULL_AUTO_GRAPH_COMPARISON.json](FULL_AUTO_GRAPH_COMPARISON.json)。
