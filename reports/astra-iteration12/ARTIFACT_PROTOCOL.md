# v0.14 保存产物协议

当前实现为 `0.14.0 / static-multilang-14 / call-rules-13-architecture-explanations / schema 2`；数据库名称为 `*-v14.sqlite3`，前一正式轮次为 `astra-iteration11/v13`。65 份真实核心源码已保存于 [CORE_FREEZE.json](CORE_FREEZE.json) 及冻结存档，tool source hash 为 `a198491ce936c91ce7a1c848789cf9fb27c5fc720b90ae81725c2ddf65f779dc`。正式结果是否完成以各 integration、发布身份及原报告有限命题的实际读回为准；冻结或开始扫描不表示目标完成。

原两份完整报告仍是功能基准；原五项/三十关系与 26 条观察、36 个原引用源码身份保持原合同。原目录 `REPORT_ALIGNMENT_CATALOG.json` 与 v0.13 逐字节相同，只是 32 章节/130 条的证据导航，不构成功能百分比或新的验收分母。没有新增 Astra 复审或审批。

## 执行入口

以下入口按实际前置条件顺序使用。可信 Python 为 `.analysis-tools/runtime/bin/python`，工作目录 `/workspace/callscope`，环境使用 `PYTHONDONTWRITEBYTECODE=1`、`PYTHONPATH=/workspace/callscope`。

| 阶段 | 入口 | 先决条件 |
| --- | --- | --- |
| 固定真实源码身份 | `freeze_core.py --run` | 根代理已完成模块、策略、版本和空间准备；尚无本轮 archive/freeze |
| 正常纯静态发布 | `scan_repository.py codepatchbay`，随后 `scan_repository.py winwincode` | 本轮 freeze 已完成；使用 full 冷/暖扫描，不创建新 CocoIndex cache |
| 原观察对比 | `compare_original_baseline.py --formal-artifacts-closed` | 两库 integration 明确 DB 已关闭、WAL 空 |
| 原五项实现账本 | `compile_goal_ledger.py --formal-artifacts-closed` | 两库 DB 同上；保留 coordinate-only anchor 认证与 policy 排序修正 |
| 正常工具 CLI 读回 | `readback_report_cli.py --run` | 两库正式发布已关闭；实际读取 WinWinCode 保存快照 |
| 原目录导航 | `build_report_alignment.py --formal-artifacts-closed` | 正式 report/findings/policy、原五项账本已保存 |
| 证据导航摘要 | `render_report_summaries.py --formal-artifacts-closed` | 两库正式 report/integration 已保存 |
| 易读分析简报 | `render_analysis_briefs.py --formal-artifacts-closed` | 同上；`--preview` 也要求正式输入已关闭 |
| 发布结果记录 | `build_release_report.py --formal-artifacts-closed` | 对比、身份、CLI、scope、两摘要、正式 MD 及账本/导航均已完成 |

扫描、原观察对比、账本和 CLI helper **各自内部持有唯一共同 flock**：`.analysis-tools/goal-source-query.lock`。不要再套外部 flock。JSON-only 展示工具不打开 DB。所有正式输出均拒绝覆盖；失败现场、旧 v0.13 产物、原报告和基准不得修改。

## 已延续的身份与展示边界

- `publication_identity.py` 认证未来本轮 freeze、live/archive、policy 和原报告；readback 从真实 freeze 的内容 hash 核对 live/archive，不沿用旧 v0.13 的硬编码 tool hash。
- 账本保留 support_inputs、rust_helper_profiles 的真实规范化排序；coordinate-only source anchor 不伪造历史 span hash。
- 异构 ordinary Evidence 的 `source_facts` object 与 report Evidence array 通过显式投影形状处理区分；真正 report 的状态、合同、数量和身份仍严格匹配。巨大树留在原文件，未保留的完整子树不声称已计算 canonical target hash。
- source-only gaps、partial ownership、unknown/false 和原条件继续按实际 JSON 保留。标题只是导航；有限表格和具体语义值由真实保存关系投影展示，显示省略不成为分析结论。
- CLI 记录实际仓库与导出 hash、逻辑行/Schema/身份和物理文件指纹。普通 Store 初始化连接不是只读；物理字节可能变化，只有实际指纹能决定该标志。
- 发布报告把 scope、两摘要、正式 Markdown、CLI 记录与读回文件绑定到最终输入 hash，再核对输入稳定性。版本发布不是功能完成的替代判据。

## 正常报告接口与引用核查

`source_relation_index.entries[].presentation` 保留 sections/tables/full refs。正常生成器 v3 增加 `architecture.responsibility_explanations`、`documentation_comparisons` 和 `report_components`；实际声明正文、操作、共享位置/证据引用和 D3 消息接缝分别保存，不从标题或方法名猜事实。

新规则类型为 `document_deployment_consistency`、`conditional_state_lineage`、`conditional_publication_boundary`。文档规则额外使用数据定位 `documents: [{role, file}]`，协议 `static-report-claim-policy-v2-documents`；原规则无需该字段。文档按照字节/text hash、大小和 BOM 认证，不产生伪 AST 或 CALLS。

`scan_repository.py` 在两轮正常扫描后，对本工具分析存储做 WAL checkpoint，再调用真实 `build_project_report` / `render_markdown`。报告写出前由 `report_shared_references.py` 校验实际内存中的共享索引、操作 ID 与 scoped pointers；成功或失败均写独立 `<repo>-report-shared-reference-check.json`，失败保留现场，不填写通过。该结构核查不将引用存在当作模型或运行证明。

原两库旧 scope 的额外完整 API 开发读回已取消，进度不明的部分保留记录；最终 API 行为由本轮正式正常报告和 CLI 读回覆盖，不再重复提取旧范围。原文有限命题由 `readback_report_completion.py` 读取实际正式产物核对，导航及数量不替代具体命题。

未执行目标、测试、构建、安装或夹具；旧 conditional gate 核心模块未改。
