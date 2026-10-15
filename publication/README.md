# 公开源代码分发

本目录的初始导出清单记录 CallScope v0.14.0 从持续分析工作区导出的内容。后续源码继续迭代，初始清单不作为当前工作树的源码身份。Git 保存产品源码、网页、使用/架构文档、示例、可读报告、冻结源码和相应元数据。原工作区约31GB，数据库、WAL、缓存、工具虚拟环境及部分历史巨量原始数据不进入源代码仓库，原文件仍留在本地。

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

初次公开 README 增加了本节入口；当时原文保存在 `workspace-original/`，以便对照既有文档哈希。初次发布的65份产品核心 Python 源码和 `pyproject.toml` 保持当时正式冻结版本的字节身份；此声明仅适用于初始发布提交 `47ffb6c74103f3d8109c30ee09e6dc1ea405d42a`。

## v0.15 CodeGraph 前端接入

当前源码复用固定提交的 CodeGraph 全语言提取器、语法资源和调用候选策略。来源、逐文件身份、依赖条款及保守能力范围见 [CodeGraph 说明](../docs/CODEGRAPH_REUSE.md)。原 v0.14 冻结报告及发布清单继续保留原字节，不用新增语言登记替代历史验收。新增扫描数据库和工具缓存仍不进入 Git；本轮可读报告、验证范围及压缩证据另存于 `reports/codegraph-integration-v15/`。
