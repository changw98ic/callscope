# v0.13 正式发布与原始基准对照 helper

这些脚本只负责冻结身份、调用可信 CallScope 静态扫描和核对保存产物。原两份完整分析报告仍为目标依据；没有 Astra 复审或批准环节。当前阶段仅准备 helper，未执行冻结、正式扫描或数据库对照。

## 输出与固定身份

- 版本必须同时为 `0.13.0` / `static-multilang-13` / `call-rules-12-report-relations` / schema `2`。
- 新数据库为 `codepatchbay-v13.sqlite3`、`winwincode-v13.sqlite3`。
- 前轮仅从 `astra-iteration10` 读取 v12 的冻结 JSON、policy 和 `*-baseline-v12-and-v11.json/current`，不加载前轮数据库。
- 冻结递归收录当前 `callscope/**/*.py` 的实际集合、源 bytes、hash 和数量；没有 54 或 60 的硬编码数量。额外包含交付 pyproject hash/副本、原报告 hash、新 policy 原始及规范化 hash、前轮 freeze hash。
- 原 26 个观察项、36 个原始源码 hash、五项目标、30 条义务及原 ledger template 的 bytes/分母保持原样。

## 准备的接口

以下命令都从 `/workspace/callscope` 调用可信工具解释器，并设置 `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/workspace/callscope`。只有 root 明确宣布核心和新 policy 已就绪后，才运行第一项。

```bash
.analysis-tools/runtime/bin/python reports/astra-iteration11/freeze_core.py
.analysis-tools/runtime/bin/python reports/astra-iteration11/scan_repository.py codepatchbay
.analysis-tools/runtime/bin/python reports/astra-iteration11/scan_repository.py winwincode
.analysis-tools/runtime/bin/python reports/astra-iteration11/compare_original_baseline.py
```

1. `freeze_core.py` 先核对旧冻结跟踪合同、原两份报告 hash、新版本和新 policy 可验证性，再做全部实际 Python 源码 AST 语法检查、稳定读取/归档和身份记录。拒绝覆盖现有 freeze/archive。
2. `scan_repository.py REPOSITORY` 内部持有 `.analysis-tools/goal-source-query.lock`。**不要再套同一把 shell flock**。串行完成 cold 和 warm；两次都用 `engine="full"` 重新计算全部前端和全局检测，没有新 LMDB/CocoIndex 缓存目录。检查 cold 确实新建、warm 同 snapshot id 且未新建，再生成自动 JSON/Markdown、configured findings 和 integration。
3. `*-integration.json` 最后才写入，并明确 `database_closed=true` 与 `database_wal_empty_or_absent=true`。其他需要完整快照的 helper 应等待 root 确认两库完成，再打开只读保存数据库。
4. `compare_original_baseline.py` 内部使用同一锁，一次只载入一个正式完整快照。拒绝非空 WAL、不同工具/归档/版本/policy、原观察 ID 或原引用文件集合变化。读取目标的操作限于 Git commit 元数据及原 36 份源码 raw bytes；Git 禁用 hooksPath 和 fsmonitor。原 frozen-static-baseline-1.3 evaluator 与源码 hash 不变。

新输出包含 `*-baseline-v13-and-v12.json`、`*-baseline-source-checks.json`、`PUBLICATION_IDENTITY.json`、`ORIGINAL_BASELINE_COMPARISON.json`，文件名不冒充前轮结果。脚本拒绝覆盖现存本轮正式产物；若中途失败，应保留失败现场，由 root 明确标识后续重试，不能悄悄覆盖。

## 引擎、空间与解释范围

前轮 v12 使用 CocoIndex；本轮为了避免重复 LMDB 缓存，在有限剩余空间下选择 full。工具原本的 CocoIndex 功能不作修改。正式摘要、freeze 和 baseline scope 均记录此变化：本轮 cold/warm 是完整纯静态重新计算的身份重复性检查，**不是同引擎精度或性能对比**。不把没有缓存复用描述成增量命中。

保留未解析、动态、宏/trait/cfg、外部副作用及未建模段落，原观察复现数量不是功能覆盖率。没有执行/导入目标代码、目标测试、构建、安装、沙箱或测试夹具。helper 自身验证仅为 Python AST 语法检查和实际已有小型 JSON 的字段读取。
