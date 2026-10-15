# Third-party notices / 第三方声明

CallScope v0.15.0 直接使用以下上游组件；Axon/CocoIndex 接入始于 v0.3，CodeGraph 接入始于 v0.15。本文记录来源、版本、改动与许可证依据，不替代各组件完整许可证。CallScope 分发配置保留各 vendored 组件的许可证、来源元数据及本声明；CocoIndex 作为可选工具依赖安装，其官方发行包保留自己的许可证及依赖声明。

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

### CodeGraph 与随包 WASM/runtime

- 项目：[colbymchenry/codegraph](https://github.com/colbymchenry/codegraph)，声明版本 `1.6.2`。
- 固定提交：`8f1f842b5b828175992d2ce2cdf673b955b2cce9`。
- 原许可：MIT，Copyright (c) 2026 Colby Mchenry；完整原文保留于 [`upstream/LICENSE`](callscope/_vendor/codegraph/upstream/LICENSE)。
- 原样复用来源文件共 323 个，清单与 SHA256 位于 [`UPSTREAM.json`](callscope/_vendor/codegraph/UPSTREAM.json)。上游文件未改写；CallScope 独立提供固定文本协议、候选关系桥接及 Python 适配器，`worker.cjs` 为保存的工具桥接产物。
- 语法分发为 31 份压缩 WASM、32 个语言映射。压缩及解压 SHA256 单独保存；不能因 CodeGraph 的 MIT 许可推定每份 grammar 同为 MIT。
- Terraform/HCL grammar 为 Apache-2.0，完整条款保留于 [`tree-sitter-terraform-LICENSE`](callscope/_vendor/codegraph/dependency-notices/tree-sitter-terraform-LICENSE)；Erlang grammar 同为 Apache-2.0，条款保留于 [`tree-sitter-erlang-LICENSE`](callscope/_vendor/codegraph/dependency-notices/tree-sitter-erlang-LICENSE)。它们不被重新许可为 CallScope 的 MIT。
- 随包工具运行依赖 `web-tree-sitter==0.25.10`、`jsonc-parser==3.3.1`、`picomatch==4.0.3` 为 MIT，其条款与发行元数据分别保留于 [`dependency-notices/`](callscope/_vendor/codegraph/dependency-notices/)。`tree-sitter-wasms==0.1.13` 提供部分固定语法，其发行包声明为 Unlicense，完整条款和 package.json 独立保留；该包许可不能代替每份 grammar 的来源许可。
- COBOL、VB.NET 等语法的上游来源和补丁说明继续保留于 [`upstream/docs/grammars/`](callscope/_vendor/codegraph/upstream/docs/grammars/)，单项语法许可须结合其来源及随包条款阅读。
- 外部 Node.js 20–24 不随 CallScope 分发；Node 项目及其依赖许可按实际安装的发行包保留。`esbuild==0.21.5` 只用于生成工具 bundle，不是目标项目依赖或扫描时构建步骤。
- [`ARTIFACTS.json`](callscope/_vendor/codegraph/ARTIFACTS.json) 记录保存的分发文件身份；具体提取与候选边界见 [CodeGraph 复用说明](docs/CODEGRAPH_REUSE.md)。语言已注册或语法可加载均不表示该语言已在真实项目完成验证。
- 31 份语法资源的逐项许可、版权全文及来源记录见 [`grammar-license-sources.json`](callscope/_vendor/codegraph/grammar-license-sources.json)。部分上游资源未锁定精确语法构建 revision；清单保留这一来源边界，不声称全部二进制均已从源码重建核验。

### 原 TypeScript/Rust 与 CocoIndex 可选依赖

TypeScript/Rust 工具依赖在 `pyproject.toml` 的 `languages` extras 声明：Tree-sitter 0.25.2、TypeScript grammar 0.23.2、Rust grammar 0.24.0。CocoIndex 位于 `maintenance` extras。`requirements-maintenance.lock` 记录本次隔离工具环境的实际依赖版本，不含目标项目依赖，也不声明已锁定 wheel 哈希或完成供应链验收。

这些依赖各自的官方发行包保留其许可证。工具不安装被分析目标的依赖，不执行其代码或测试；静态分析产物可能包含为证据保存的目标原文，仍受该目标原许可约束。上游组件的其他能力不扩大 CallScope 的纯静态产品边界。

