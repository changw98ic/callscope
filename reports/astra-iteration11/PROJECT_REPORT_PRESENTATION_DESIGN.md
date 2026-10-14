# 保存源码关系的报告展示 v2

修改仅在 `callscope/project_report.py`，其 `VERSION` 为 `captured-project-analysis-report-2`。公共调用保持 `build_project_report(snapshot, findings)` 和 `render_markdown(report)`，CLI/HTTP/MCP 不需要新增参数。

## 新的报告字段

- `source_relation_index.entries[]`：每条已保存 `static_report_claim` 的规则、分析类型、Finding/Evidence ID、原 assessment/pattern/source_facts/source_scope/analysis_gaps 的准确 JSON Pointer，以及原保存 Evidence 内部的 pointer。它是导航索引，不新增判断。
- `source_relation_index.entries[].presentation`：从该真实 pattern 生成的通用、有界 `presentation_only=true` 展示投影。包含按 pattern 字段组织的 sections、实际 rows/finite partitions 真值表、每一节/每一行的完整数据 pointer、明确的展示 truncation 和限额。
- `architecture.captured_writer_references[]`：仅在真实 pattern 已有 `captured_resource_writer_groups` 时生成。保留已有写者组、writer/consumer/rejection guard 及责任文字的 refs、已有选中写者符号，并原样复制 `ownership_assessment` 为 `source_assessment`。当前 `partial_captured_writers_and_consumers` 不会升级为完整所有权。

原 `functional_chains[].pattern`、`source_facts`、assessment 和 Evidence 都保持原值，没有为展示剪掉真实证据。没有读取原分析报告来补写结果，没有调用检测器重新评级，也不按目录名推断职责、唯一事实所有者或授权。

## Markdown 呈现

原有 source sequence 之外，按真实 pattern 通用展示必要关系、来源连接、guard、条件、反证与 false 边界，不再只显示 source fact 类型数量。有限状态 `rows`、`record_partitions`、`absent_input_partitions`、`*_table_rows` 自动表格化，保留实际 false/null/unknown 和每行原 JSON Pointer。表内未显示/原行缺项单独标识，不伪装为计算出的 null。

对新八类关系没有期望结果表或规则 ID 特例：Rust 状态、条件门、事件投影、可信命令来源、未支持 record 保留、消息身份、浏览器异步及资源写者都复用同一保存数据投影。其他旧关系也可按相同结构展示。大型 source fact 的摘要附向原 `source_facts` 的 refs，不复制完整重复源码、parse identity 或解析元数据。JSON 和 Markdown 均明确标识这是展示；原始完整字段仍可以下钻。

每节最多 224 个展示节点、深度 8、列表通常 6 项、字符串 240 字符；真值表最多显示 64 行/12 列，最多收集 24 张表。触及限额保留 `truncated=true` 与完整 pointer。表格只显示一次，其在 section 中的重复出现改成展示表与完整数据 refs。此截断不成为新分析缺口，不使原 partial 变为 supported。源码关系数量及展示行数不是功能覆盖率。

架构部分另列真实捕获的写者/消费者引用，保留原 partial 所有权范围。报告 `whole_report_reproduction_claimed=false`、运行未验证边界保持原样。

## 当前验证范围

通过自身 Python AST 语法核对。另对已经保存的真实 `workrun-source-query.json` 进行了正常的纯展示转换，见 [展示 JSON](PROJECT_REPORT_PRESENTATION_DEVELOPMENT_QUERY.json) 与 [展示 Markdown](PROJECT_REPORT_PRESENTATION_DEVELOPMENT_QUERY.md)。主状态表的八行和反证表的六/两行全部显示，已有全状态机/运行调度等 false 边界可见。

这份展示预览没有构造 Finding 或新快照，没有重新运行分析，不是正式 v13 发布结果，也不冒充从新正式 Findings 生成的完整报告。正式报告仍由 root 在冻结后调用现有扫描/保存 Findings 路径生成。未执行目标代码、测试、构建、安装或测试夹具。
