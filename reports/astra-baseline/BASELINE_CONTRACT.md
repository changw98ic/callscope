# Astra 静态能力基准格式 v1

本目录用于冻结独立源码观察，不替目标仓库新增规范。报告与机器基准绑定仓库提交；比较工具能力时不得改写原观察来适应新工具结果。

`capability-baseline.json` 顶层字段为 `schema_version: 1`、`baseline_id`、`status`、`repositories`、`observations`。`status` 在报告完成前为 `draft`，完成后为 `final`。新增观察兼容现有格式，观察语义变化需变更 ID 或基准版本。

`repositories` 每项包含 `id`、`root`、`commit` 和 `source_files`。后者为 `{仓库相对路径: 原文件 SHA256}`，覆盖该仓库所有观察引用的位置和端点文件。哈希针对未经改写的原始字节；比较时应核对保存快照的源码哈希，不能仅凭 commit 元数据或相似 quote 套用旧观察。文件不在选入范围与文件内容已经变化应分别呈现。

每项观察字段固定如下：

| 字段 | 含义 |
| --- | --- |
| `id` | 稳定、全局唯一字符串 |
| `repo`, `commit` | 仓库 ID 和本次源码提交 |
| `category` | `source_fact`、`repository_contract`、`gap_candidate`、`analysis_boundary` |
| `claim` | 有限且可检查的源码陈述，不写“功能通过” |
| `source`, `target` | 端点选择器或 null；选择器为 `{path, symbol, language}`，路径相对仓库根，symbol 为文件内词法限定名称，例如 `mountWinWinCodeClient.diagnosticScope` |
| `expected_static_outcome` | 下述五个枚举之一 |
| `locations` | `{path, line, end_line, role, quote}` 数组，1-based；role 为 `call_site`、`definition`、`binding`、`guard`、`contract`、`counterevidence` 之一；quote 必须能在原源码对应范围找到 |
| `reason` | 从源码到有限结论的理由 |
| `certainty` | `source_confirmed`、`conditional_risk`、`unresolved`；不表示运行证明 |
| `conditions`, `counterevidence` | 字符串数组，保留成立前提与反证 |
| `priority` | 工具能力补齐优先级 `P1`、`P2`、`P3`，不是目标仓库缺陷严重度 |
| `tool_support` | `{version, state, required_capabilities, explanation, snapshot_id}`；state 为 `supported`、`partial`、`unsupported`、`not_evaluated`，snapshot_id 可为 null |

`expected_static_outcome` 语义：

- `confirmed_static_call`：需要同一调用位置的明确内部静态绑定及源码证据，单有任意路径或没有规则发现不足以满足。
- `confirmed_static_path`：需要正长度显式静态路径与逐边见证；不要求此路径运行、条件可满足或按时间顺序发生。
- `no_direct_call_in_explicit_model`：限定调用者实现与指定目标的直接调用检查；解析/绑定不足时必须报告未知，不能用缺边当否定证明。
- `unknown_required`：当前源码与合同本身不足以给出唯一确定内部目标。应保留对应调用位置及未知理由；不存在源节点或仅有其他文件覆盖缺口不算满足。
- `evidence_only`：架构所有权、注册/传输/进程关系、顺序/状态/条件判断及缺口候选，现有调用图不可直接裁决。工具应保存观察为能力缺口/待复核，不映射为已通过、已失败或目标缺陷。

路径缺失、端点歧义、工具语法失败、跨版本不可比须分别呈现。不得把 `unknown_required` 和 `evidence_only` 排除后宣称整个项目能力已覆盖。`tool_support` 是 v0.3 的起点描述，后续评估结果应另存，不能覆盖冻结基准。

本目录不运行目标代码、测试、构建、仓库 CLI 或索引命令。源文件和生成合同可只读作为证据，第三方实现另列未审范围。

第一版已冻结为 `final`，两个仓库各 13 项观察，总计 26 项，引用 36 份原文件。数量是人工观察样本数，不是功能覆盖率或缺陷数。复杂业务候选均保留为 `evidence_only`，调用解析能力提升不能自动将它们改为已裁决。
