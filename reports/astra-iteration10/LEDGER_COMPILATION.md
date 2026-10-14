# 保存目标结果的实施索引

`compile_goal_ledger.py` 只整理未来 v12 两库 SQLite 中真实的 `static_goal_judgment`，不重新分析目标代码、不运行目标、构建或测试，也不新增评级或 Astra 审批。两份原全文报告仍是功能基准；原五目标和三十关系作为实施追踪保留。

默认输入为本目录的 `codepatchbay-v12.sqlite3`、`winwincode-v12.sqlite3` 与 `CORE_FREEZE.json`。默认输出为新的 `goal-ledger.json` 和完整原结果存档 `GOAL_JUDGMENT_EVIDENCE.json`。可用 `--codepatchbay-db`、`--winwincode-db`、对应 `--*-snapshot`、`--freeze`、`--output` 与 `--evidence-output` 覆写；已有输出一律保留。

正式扫描后，从 CallScope 根目录运行：

```bash
.analysis-tools/runtime/bin/python reports/astra-iteration10/compile_goal_ledger.py
```

脚本自行获取既有 source-query 文件锁，串行读取两库；SQLite 使用只读连接和同一读事务。利用 JSON 数据接口读取捕获配置、源文件和原图身份，不创建缩小的分析快照、不导入分析器或目标模块。

核对覆盖：

- 原合同、模板、26 条历史基准及两份全文报告的固定 SHA-256，原五目标/三十义务 ID、必要属性和 claim 定义。
- goal→仓库→实际 adapter 映射，以及真实捕获策略中的 inner/outer rule 身份。
- SQLite 表与 snapshot JSON 的身份一致；source/scope/support-input aggregate、policy、parser/component 版本和 snapshot ID 的原算法；tool 与冻结清单相同。
- `CORE_FREEZE.json` 的 `benchmark_reports` 与两份原报告固定 SHA 一致，`policy_files` 的两个实际输入文件字节 SHA 一致；保存的完整 normalized policy 必须与对应冻结输入一致。冻结 loader 会排序 `support_inputs` 和 `rust_helper_profiles` 两个数据列表，脚本复用这两项明确的排序规则并保留对应冻结模块 SHA；其他字段仍作完整一致性核对。可覆写 freeze 路径时，其 policy 文件从该 freeze 所在目录读取。
- 原 registered finding fingerprint/ID、evidence ID 的内容公式；嵌套 adapter 结果 ID、上下文及重复内容一致；引用 node/edge 属于捕获图。
- 所有携带原文件 SHA 的源码出处，其保存文字 hash、byte/span hash、UTF-8 line/column/BOM 映射与 parse snapshot 来源。`SourceAnchor` 原记录只提供 SHA 和 byte coordinates 时核对这些已有字段，单独统计未提供原 span hash 的 anchor；不填造或要求原记录没有声明的 span hash。
- 新证据存档 hash，以及每条 ledger JSON pointer 的原 finding/evidence/contract/snapshot/tool/policy/source 身份和目标内容 hash。

所有 assessment、必要未知、模型适用性、条件、反证及完整 adapter 结果均来自保存产物。源位置数量、selector 命中或引用条数都不会被解释为达标。脚本不重新判断哪个模型支持哪个业务结论；完整原结果保留在 `registered_judgment`，义务自身原记录保留在 `recorded_result`。状态计数只是既有自动结果的分组。

源码、模型、政策引用保留各 adapter 的原摘要容器和义务自身容器；表达式中恰好名为 `source` 或 `model` 的普通字段不会被重新标成证据类别。两份新产物均完成身份和 JSON pointer 校验后才开始写出；已有文件或越出本 iteration 的输出路径在读取 DB 前即拒绝。

在最终 DB 尚未存在时，只核对脚本语法与命令接口，不制造示例结果，也不从历史开发候选构造正式账本。
