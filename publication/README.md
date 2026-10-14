# 公开源代码分发

本目录记录 CallScope v0.14.0 从持续分析工作区导出的内容。Git 保存产品源码、网页、使用/架构文档、示例、可读报告、冻结源码和相应元数据。原工作区约31GB，数据库、WAL、缓存、工具虚拟环境及部分历史巨量原始数据不进入源代码仓库，原文件仍留在本地。

当前 `reports/astra-iteration12-scope2/` 的大 JSON 证据按原始字节分段压缩保存；较大的历史 JSON 元数据也采用同一形式。每段压缩前最多64MiB，文件低于 GitHub 单文件限制。[归档清单](COMPRESSED_REPORT_ARTIFACTS.json)保存原路径、原始 SHA256/大小、顺序和每段压缩 SHA256。

克隆后，在仓库根目录还原当前完整 JSON：

```sh
python scripts/restore_report_artifacts.py
```

还原所有随本仓库归档的历史 JSON：

```sh
python scripts/restore_report_artifacts.py --all
```

只验证归档字节、不写出解压文件：

```sh
python scripts/restore_report_artifacts.py --all --verify-only
```

脚本只处理数据，不导入或运行目标项目。它核对每段和完整文件哈希，拒绝覆盖不同内容的文件。原路径还原后，报告中的原始 JSON Pointer 可用于下钻；这些体积较大的 JSON 的 Markdown 链接需要先还原。当前还原数据是完整报告和发现证据，不是 SQLite 运行数据库。

[导出清单](SOURCE_EXPORT_MANIFEST.json)分别列出原字节复制、压缩保存和留在本地的文件。留在本地的历史大文件没有被声称已上传。历史源程序、辅助脚本和身份记录保留其当时路径与机器信息，不将它们改写为新结果；当前可读结论见 [正式报告](../reports/astra-iteration12-scope2/REPORT.md)与[原内容对照](../reports/astra-iteration12-scope2/ORIGINAL_REPORT_COMPLETION.md)。

公开 README 增加了本节入口；原文保存在 `workspace-original/`，以便对照既有文档哈希。65份产品核心 Python 源码和 `pyproject.toml` 均保持正式冻结版本的字节身份。
