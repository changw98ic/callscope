# CodeGraph 全语言静态前端复用

CallScope v0.15.0 将 CodeGraph 的语言提取器、固定 WASM 语法及部分公开解析策略接入正常静态扫描。默认配置为 `analysis.languages: ["all"]`；已有配置显式选择的语言保持其选择。全量语言注册不表示这些语言已在真实项目逐一验证，也不将原 TypeScript/Rust 有限合同自动移植到新增语言。

## 固定来源与实际代码

| 项目 | 保存内容 |
| --- | --- |
| 上游 | [colbymchenry/codegraph](https://github.com/colbymchenry/codegraph)，声明版本 1.6.2 |
| 固定提交 | `8f1f842b5b828175992d2ce2cdf673b955b2cce9` |
| 原样来源文件 | `callscope/_vendor/codegraph/upstream/`，来源清单共 323 个文件，逐项保存 SHA256 |
| 语法资源 | 31 份压缩 WASM，32 个语言映射；JavaScript 与 JSX 共用同一份语法 |
| 工具运行时 | 外部 Node.js 20–24；随包 web-tree-sitter 0.25.10、jsonc-parser 3.3.1、picomatch 4.0.3，以及固定语法资源 |
| CallScope 桥接 | `codegraph_frontend.py`、`_vendor/codegraph/worker.ts`、`resolution-bridge.ts` 与已保存 `worker.cjs` |
| 身份与许可 | [`UPSTREAM.json`](../callscope/_vendor/codegraph/UPSTREAM.json)、[`ARTIFACTS.json`](../callscope/_vendor/codegraph/ARTIFACTS.json)、[第三方声明](../THIRD_PARTY_NOTICES.md) |

这是真实源码复用：worker 调用上游 `extractFromSource` 和语言提取器，并通过捕获输入上下文调用部分公开的导入、名称与接收者匹配策略。不是仅使用 CodeGraph 生成一份参考报告，也没有在 CallScope 中重写 35 个语言前端。

Python、TypeScript 家族和 Rust 保留原 CallScope 前端。Node 工具执行的是随包保存的分析代码，不执行被分析项目。原生 CodeGraph kernel 被关闭；不运行 Cargo、目标编译器、目标 npm 脚本或目标包加载器。`esbuild` 只属于生成工具桥接产物的工具链，不是扫描时的目标构建步骤。

## 38 个规范前端 ID

`language_catalog.py` 是配置、源码识别与服务能力目录的共同来源。38 个 ID 包含语言及文件格式，不等于 38 套完整语义分析器。

| 调度层 | 规范 ID |
| --- | --- |
| 保留的 CallScope 前端 | `python`, `typescript`, `rust` |
| CodeGraph 语言结构提取 | `arkts`, `go`, `java`, `c`, `cpp`, `csharp`, `php`, `ruby`, `swift`, `kotlin`, `dart`, `pascal`, `scala`, `lua`, `luau`, `objc`, `r`, `solidity`, `nix`, `cfml`, `cfscript`, `cfquery`, `cobol`, `vbnet`, `erlang`, `terraform` |
| 模板与组件结构提取 | `razor`, `svelte`, `vue`, `astro`, `liquid` |
| 文件或元数据层 | `yaml`, `twig`, `xml`, `properties` |

上游类型表有 42 个值：排除 `unknown` 后，将 `javascript`、`tsx`、`jsx` 合并到既有 `typescript` 调度，因此得到 38 个规范 ID。`cfquery` 为 CFML 中的嵌入 SQL 语法，没有独立文件扩展名；不据此声称一般 SQL 项目支持。

上游 78 个扩展名全部进入识别表，另保留原有 `.pyi` 与 `.sh` 的识别。后两者继续为无实现前端的输入，不能因 `all` 变成解析成功。TypeScript 调度包含 JS/JSX、MJS/CJS、MTS/CTS、XSJS/XSJSLIB；不为 JavaScript 或 TSX 再启动一次重复扫描。

路径特判包括 Play `conf/routes`/`.routes`、Erlang `.app`/`.app.src`、具有主题标记的 Shopify `templates/` 与 `sections/` JSON。普通 JSON 不作为代码。未知扩展名进入独立文件路径盘点，不进入源码解析成功分母；符号链接仍不跟随。

`.h` 与 `.inc` 在语言分组前，再由固定上游 `detectLanguage` 根据捕获文本校正为 C/C++/Objective-C 或 PHP/Pascal。校正记录进入快照，显式语言配置按校正后的语言决定是否分析；内容识别失败会留下诊断并标记覆盖不完整。仅选择原三类前端时不增加 Node 依赖。

## 配置与工具依赖

不提供 `.callscope.json` 或省略语言选择时，使用全部规范前端：

```json
{"schema_version": 1, "analysis": {"languages": ["all"]}}
```

也可显式缩小范围：

```json
{"schema_version": 1, "analysis": {"languages": ["dart", "yaml"]}}
```

`all` 必须单独使用。保守别名如 `javascript`、`tsx`、`jsx` 统一为 `typescript`，`c++` 为 `cpp`、`c#` 为 `csharp`、`objective-c` 为 `objc`、`vb.net` 为 `vbnet`、`hcl` 为 `terraform`。同一前端通过多个别名重复选择会被拒绝。既有显式 `python/typescript/rust` 配置不会因为默认值变化而扩展。

新增 CodeGraph 语言需要工具环境中的 Node.js 20–24。语法与 worker 已随 CallScope 保存，不在扫描时下载语法或安装目标依赖。TypeScript/Rust 原前端仍需 `languages` extras 中固定的 Python Tree-sitter 库；仅 Python 的显式全量配置仍不需要这些额外依赖。CocoIndex 为可选维护引擎，缓存单位仍为整个规范语言。

## 捕获、身份与调用关系

统一读取器先通过禁止跟随符号链接的文件描述符捕获源码。CodeGraph worker 只收到相对路径、已捕获文本及字节/文本哈希；真实目标根路径不传给 Node。固定名称的项目清单同样作为数据捕获并纳入快照，不能由上游解析策略临时读取工作区。

worker 使用虚拟根和捕获文件系统进行候选解析。请求指纹、返回文件集合、源码哈希、固定提交和协议均需匹配。工具身份还包含全部 vendored 资源；语法加载校验压缩内容及解压内容的 SHA256。Node 启动时清除 `NODE_OPTIONS`、`NODE_PATH`，目标配置不能注入工具启动代码。

组件版本记录 Node 的精确版本，并参与快照身份和 CocoIndex 缓存键；更换 Node 版本不能直接沿用旧运行时的缓存证据。

v0.15 的 `parser_version` 使用 `components-sha256:<完整组件映射 SHA256>`；完整映射仍保存于 `stats.component_versions`。该值是身份摘要，不是语法版本名称，也不让不同组件得到相同身份。图接口新增 `files` 分类记录，但不包含源码内容；UI 读取实际 `language/status`，不自行按后缀重猜特殊路径。

每个节点的 `metadata.language` 保留规范调度 ID，`upstream_language` 另记上游识别的具体方言。源码位置回到保存文本；UTF-16 列转换为 UTF-8 字节列。重复声明身份、语法缺口及缺失所有者有独立标记或诊断。

**所有新增 CodeGraph 调用关系均为 candidate-only。** 有候选时保存 `ambiguous`，无候选时保存未知关系；`target` 不因唯一候选或较高 confidence 被写成确定目标。上游 confidence 是候选排序依据，不是实测正确率。非调用关系与结构关系另存节点元数据，不进入 Axon 的确定 `CALLS` 邻接。因此，候选丰富可以帮助定位，尚不能直接补齐需要确定路径的合同。

当前复用不包含 CodeGraph 的完整框架发现、全局合成、数据库延迟解析和全部私有策略，也不把原 TS/Rust 字段 IR、有限交错、职责解释或文档合同自动应用于所有新语言。具体边界保存在每次前端结果的 `boundaries` 中。

## 状态、覆盖与验证口径

能力目录分别记录 `registered`、运行时可用性和当前项目验证状态；静态注册本身不把 `available` 或项目验证改成 true。运行时语法可以加载，也不等于已在该语言真实项目上完成扫描。

普通语法前端保留 `parsed` 与 `parse_error`；语法有缺口时可保存部分符号及候选，但仍须标记不完整。YAML/Twig/properties 为文件或配置元数据层；XML 仅有限定的 MyBatis 结构提取，普通 XML 不具有通用语义验证能力。组件模板、正则提取与嵌入脚本范围需要保守记录，不能将有文件节点或有提取结果解释为整个模板语法完整。状态统计应分列元数据及局部结构输入，不能把它们混入完整语法覆盖率。

项目报告中的文件选择数、语法解析数、节点数与候选数均不是功能完整性覆盖率。功能与条件判断仍需要实际支持的合同和来源证据；未配置、未建模或没有静态证据的领域保持未知。这里不预填新项目扫描覆盖数字，也不声称未实际扫描语言已经验证。

## 历史结果与许可

v0.14 的 CodePatchBay/WinWinCode [冻结 scope2 结果](../reports/astra-iteration12-scope2/REPORT.md)继续属于原版本、原工具身份、原策略与原文件选择；五项判断、30 项必要关系及原报告有限内容完成状态不因新增语言而改写。新增 38-ID 目录不是对这些旧报告重新验收，也不构成新的 Astra 审批门。

CodeGraph 源码为 MIT，保留 Copyright (c) 2026 Colby Mchenry 和原 LICENSE。web-tree-sitter、jsonc-parser、picomatch 为 MIT；tree-sitter-wasms 发行包声明为 Unlicense，单项 grammar 的来源许可仍分别有效，特别 Terraform/HCL 与 Erlang grammar 的 Apache-2.0。COBOL、VB.NET 等来源说明保留在上游 grammar 文档目录；不能把这些资源统一重标为 CallScope 的 MIT。完整条款位置和版本见[第三方声明](../THIRD_PARTY_NOTICES.md)。

31 份资源逐项对应的版权与许可全文、获取来源和精确 revision 缺口见 [grammar-license-sources.json](../callscope/_vendor/codegraph/grammar-license-sources.json)。资源字节由固定 CodeGraph 提交及 SHA256 锁定；这不等于已验证每份 WASM 的源码重建过程。

## 重新生成工具桥接产物

仓库已包含运行所需的 `worker.cjs` 与语法，无须在扫描前构建。维护者修改桥接源码后，可以在独立工具依赖目录安装 `tool-dependencies.lock.json` 根节点声明的五项固定依赖，再运行：

```sh
node scripts/build_codegraph_bridge.mjs /absolute/path/to/tool-dependencies
```

脚本只打包 CallScope 自己的分析桥接，同时重算 `ARTIFACTS.json`。`scripts/vendor_codegraph.py` 可从固定上游 checkout 与同一工具依赖目录重新复制来源文件和压缩语法；单项 grammar 版权声明须继续保留。两个脚本均不构建被分析项目，不运行测试。
