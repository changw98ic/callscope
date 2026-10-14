# 可重建前端 memo 的归档与恢复

本次只回收计划列出的 23 个 `*.sqlite3.cocoindex` 目录。它们各有 `mdb/data.mdb`、`mdb/lock.mdb`，属于 CocoIndex 语言前端 memo；旁边的正式 `.sqlite3` 是独立的 GraphSnapshot/Finding Store，未删除或改写。四个报告 helper 的 `__pycache__` 保留。

- [计划](CACHE_RECLAIM_PLAN.json)：保留原目录、allocated/logical bytes、可重建依据、历史元数据引用；原字节未改。
- [执行结果](CACHE_RECLAIM_RESULT.json)：23 项已回收，0 跳过、0 错误；42 个正式 SQLite/WAL/SHM 的身份元数据前后相同。
- [归档清单](CACHE_RECLAIM_ARCHIVE_MANIFEST.json)：46 个成员的原路径、bytes、SHA256 和源文件身份。
- [gzip 归档](rebuildable-memo-archive.tar.gz)：362,319,209 bytes；SHA256 `cd8f6dddff926706d6d7033cdfcfeeb372fb5f5be4ab97a8f8a08157f9252435`。

归档直接采用 gzip level 1 流式写入，没有创建未压缩 tar。46 个成员全部流式读回核对原 bytes/SHA，并消费 gzip 尾部校验；验证成功后，再逐目录重查源身份、内容 SHA、可见 FD/maps/cwd、固定 Python CocoIndex worker 生命周期和 LMDB kernel locks，才移除原目录。不可读的基础服务进程元数据被明确记录；没有把它们伪装为全部可观测。两次零删除预检结果也保留。

完成时可用空间为 5,721,591,808 bytes，约 5.33 GiB；这是当时实际值，后续正式扫描会继续使用磁盘。

## 何时需要恢复

读取旧正式数据库、JSON、证据、ledger 和报告不需要这些 memo。v0.13 和本轮计划的 full 引擎扫描也不依赖旧 memo。将来重新运行旧 CocoIndex 扫描时，可以从保存输入重新计算；只有希望保留旧 memo 加速状态时才需要恢复。历史记录中的 cold/warm 与 reused-language 观察没有改写。

## 恢复方法

先结束使用这些旧 memo 路径的 CocoIndex worker。恢复脚本默认只验证归档；显式 `--restore` 才写回原 cache 目录。从 `/workspace/callscope` 运行：

```bash
PYTHONDONTWRITEBYTECODE=1 .analysis-tools/runtime/bin/python reports/astra-iteration12/restore_rebuildable_memo.py
PYTHONDONTWRITEBYTECODE=1 .analysis-tools/runtime/bin/python reports/astra-iteration12/restore_rebuildable_memo.py --restore
```

恢复脚本先核对归档 SHA、成员路径/集合与每文件 SHA。写回时先写到本轮报告目录中的独立 staging，全部成员核对通过后逐目录放回；任何已有同名 cache 目录都会被拒绝，不与新 memo 合并或覆盖。恢复内容仅限清单中的 `.sqlite3.cocoindex/mdb/` 文件，不打开正式数据库、不导入 CocoIndex，也不执行目标代码。

此脚本本次只作 Python AST 语法核对，没有实际恢复；实际归档验证已由回收工具完成。正式 SQLite、冻结源码、原报告、JSON、policy、ledger 与目标库均保留。
