# v0.13 正式产物辅助入口

这组工具只准备和编译保存产物，不新增审查、不新增评分。原两份完整报告仍是功能基准；五项判断/三十项关系只是冻结实现账本，26 项观察保持原合同。`REPORT_ALIGNMENT_CATALOG.json` 从 iteration10 逐字节复制，32 个章节/130 个条目只作导航。

四个脚本已在发布者明确通知两库数据库及必要输入关闭后顺序执行成功，正式账本、目录对照、两份摘要和发布报告均已保存。以下是重现入口说明；当前成功产物拒绝覆盖，不应直接再次运行。全部正式入口要求 `--formal-artifacts-closed`，该标记只表示输入已完成，不是新的模型审查或人工审批。

执行环境为可信工具 Python，以下命令在 `/workspace/callscope` 中执行：

```bash
env PYTHONDONTWRITEBYTECODE=1 .analysis-tools/runtime/bin/python reports/astra-iteration11/compile_goal_ledger.py --formal-artifacts-closed
env PYTHONDONTWRITEBYTECODE=1 .analysis-tools/runtime/bin/python reports/astra-iteration11/build_report_alignment.py --formal-artifacts-closed
env PYTHONDONTWRITEBYTECODE=1 .analysis-tools/runtime/bin/python reports/astra-iteration11/render_report_summaries.py --formal-artifacts-closed
env PYTHONDONTWRITEBYTECODE=1 .analysis-tools/runtime/bin/python reports/astra-iteration11/build_release_report.py --formal-artifacts-closed
```

1. `compile_goal_ledger.py` 等两库 scan、保存 Finding 和数据库关闭后，读取默认 `codepatchbay-v13.sqlite3`、`winwincode-v13.sqlite3` 与本轮 `CORE_FREEZE.json`。内部唯一 common flock，**不要再套外部 flock**。拒绝非空 WAL，保留 v12 对 coordinate-only source anchor 的认证及 support_inputs/rust_helper_profiles 排序修正；输出 `goal-ledger.json`、`GOAL_JUDGMENT_EVIDENCE.json`，已有文件拒绝覆盖。
2. `build_report_alignment.py` 等 ledger、两库 automatic report/configured findings 和正式 policy 保存后执行。它从实际 policy 获取 rule ID/role/type 并与实际保存 finding 的 contract hash/ID 对照；目录映射只导航，不产生结论。使用 `_SavedJSON` 流式选择小字段和保存关系索引，完整 pattern/source facts 保留原 artifact SHA、JSON Pointer 和真实元素数量。未保留的巨大子树不声称已重新算出其完整 canonical target hash；只有完整保留的小字段才附目标 canonical hash。输出 `REPORT_ALIGNMENT_RESULTS.json`。
3. `render_report_summaries.py` 仅需两库 report/integration 均保存并关闭，可在 ledger 之后或独立渲染。按正式 report v2 的 `source_relation_index` 展示真实关系投影、有限表格、条件/字段与原指针，保留 false/unknown 和显示省略；不只打印状态。每链显示预算为三表、每表十二行、二十四字段，完整保留本轮 WorkRun 八行、completion 九个普通 enum 单元及两个缺值单元；更多表/字段返回原关系指针。十三条新增规则均有简短中文导航标题，标签不构成结论。输出两库 `*-analysis-summary.md`，已有摘要拒绝覆盖。
4. `build_release_report.py` 等上述结果、最终 scope、正常 CLI 读回、原 26 项比较和正式身份文件均完成后，生成 `REPORT.md`、`RELEASE_REPORT_INPUTS.json`。前一版本比较口径为 iteration10/v0.12；本轮要求 freeze 为 v0.13。报告复制保存状态及具体门/WorkRun/消息/投影等关系，显示截取不是分析缺口。scope、两摘要、正式 Markdown 与 CLI 导出文件的实际 hash 均纳入输入清单和末次稳定性核对。

本轮执行日志为 `goal-ledger-build.log`、`report-alignment-build.log`、`report-summaries-build.log`、`release-report-build.log`。账本复制五项判断、三十项关系；目录保留 32 章节/130 条及 320 个引用；两摘要为 624/798 行；发布报告为 611 行。两轮 alignment 失败日志保留在 `report-alignment-build.failure1.log`、`report-alignment-build.failure2.log`：普通旧 Evidence 的 `source_facts` 是 object，不能按 report Evidence 的 array 投影。修正只涉及 artifact parser，遇到异构字段保留形状不符标记；实际 report 字段的数量、状态、合同和身份仍严格核对，未修改核心或已成功结果。

正常 CLI 读回的实际仓库为 WinWinCode。其普通 Store 初始化使用非只读连接，数据库物理字节发生变化；保存的逻辑行、Schema 与身份指纹保持一致，导出 Markdown 与正式文件逐字节相同，末尾 WAL 为空/不存在。发布报告按这份实际协议校验，没有将正常初始化表述成零物理效果，也没有重新运行 CLI。

两份只读 JSON 展示工具不打开分析 DB；只有 ledger 工具按上面说明读取已关闭 DB。全部工具不读取目标工作区、不运行目标、测试、构建或夹具。新源码/版本/策略/扫描/对比由 root 和相应负责人处理，这些入口不修改它们，也不修改旧轮次产物。
