# Third-party notices / 第三方声明

CallScope v0.3.0 直接使用以下上游组件。本文记录来源、版本、改动与许可证依据，不替代各组件完整许可证。CallScope 分发配置保留 Axon 许可证、来源元数据及本声明；CocoIndex 作为可选工具依赖安装，其官方发行包保留自己的许可证及依赖声明。

## Axon graph core

- 项目：https://github.com/harshkedia177/axon
- 上游分发名：`axoniq`；声明版本：`1.0.1`。
- 固定提交：`2b386fb38a468201ab2ec825ddea5ebf4c33f513`。
- 作者署名：`harshkedia177`，来自该提交的 `pyproject.toml`。
- 许可证：MIT；依据是上游 `pyproject.toml` 明确的 `license = "MIT"` 声明。
- 复用文件：上游 `src/axon/core/graph/model.py` 与 `src/axon/core/graph/graph.py`，保存于 `callscope/_vendor/axon/`。
- 改动：`graph.py` 将模型的绝对 import 改为包内相对 import；两个文件末尾增加空白行。除命名空间导入适配及末尾空白格式外，未改变上游图核心代码。CallScope 适配层独立位于 `callscope/axon_adapter.py`。

固定提交未提供独立 LICENSE 文件。本工具的 `callscope/_vendor/axon/LICENSE.txt` 保存标准 MIT 条款，并按上游元数据保留作者署名；它不是上游 LICENSE 文件的复制品。原始许可声明保存在 `pyproject.upstream.toml`，文件路径、改动说明与本地 SHA256 保存在 `UPSTREAM.json`。不得将生成的标准条款说明成从上游取得的原始文件。

Copyright (c) harshkedia177. Axon graph core is distributed under the MIT License; the full terms accompany the vendored files.

## CocoIndex

- 项目：https://github.com/cocoindex-io/cocoindex
- 官方包：`cocoindex==1.0.25`；本工作区安装官方 binary wheel。
- 署名：CocoIndex contributors；官方包元数据作者为 CocoIndex。
- 许可证：Apache-2.0，来自官方发行元数据。
- 完整 Apache 2.0 条款保存在 `callscope/third_party/COCOINDEX_LICENSE.txt`。
- CallScope 使用官方库的 `fn`、`Environment` 与 `App` 维护语言前端的持久 memo，未修改 CocoIndex 发行代码。

本工作区官方 wheel 的 `cocoindex-1.0.25.dist-info/licenses/THIRD_PARTY_NOTICES.html` 保存其自身依赖声明，`sboms/cocoindex_py.cyclonedx.json` 保存发行包 SBOM。本文不是这些官方文件的替代品；再分发该 wheel 或整个工具环境时，应一并保留它们及相关组件许可证。

## Optional parser and runtime dependencies

TypeScript/Rust 工具依赖在 `pyproject.toml` 的 `languages` extras 声明：Tree-sitter 0.25.2、TypeScript grammar 0.23.2、Rust grammar 0.24.0。CocoIndex 位于 `maintenance` extras。`requirements-maintenance.lock` 记录本次隔离工具环境的实际依赖版本，不含目标项目依赖，也不声明已锁定 wheel 哈希或完成供应链验收。

这些依赖各自的官方发行包保留其许可证。本工具没有复制目标仓库的依赖、运行代码或测试；上游组件的其他能力也不扩大 CallScope 的纯静态产品边界。

