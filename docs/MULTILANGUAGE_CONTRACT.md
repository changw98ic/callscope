# 真实仓库静态评估：多语言共享协议

本轮目标是只读分析 WinWinCode 与 CodePatchBay 的真实源码，不执行目标模块、脚本、构建或测试。不修改这两个仓库。报告、约束配置和数据库放在 CallScope 的 `reports/real-repositories/`。

语言前端使用已捕获的源码文本与固定的 Tree-sitter 语法库，不启动 TypeScript 编译器、Rust 编译器或目标框架。

## 前端 API

`callscope/typescript_analyzer.py` 和 `callscope/rust_analyzer.py` 各提供：

```python
ANALYZER_VERSION: str
PARSER_VERSION: str
def analyze_files(files: list[SourceFile], root: Path, config: dict) -> dict:
    ...
```

返回 `{"nodes": list[Node], "edges": list[Edge], "files": list[SourceFile], "diagnostics": list[Diagnostic], "stats": dict}`。不返回最终快照 ID，由统一编排器生成。输入文件已按配置选择并安全读取；前端不要重新读取或执行目标。更新 SourceFile 的解析状态但不要修改调用方对象，返回新的对象。

使用 `from .parsers import language_parser, parser_version`；`language_parser("typescript"|"tsx"|"rust")` 返回新的 Tree-sitter Parser；`parser_version(kind)` 返回语法库、Tree-sitter 和宿主版本。库位于 `.analysis-tools/python`（或通过声明的可选依赖安装）。

TypeScript 节点 ID/qualname：`ts:<源码相对路径去除最后扩展名>#<词法限定名>`，模块节点 `module:ts:<同一路径>`。Rust 对应 `rust:<同一路径>#<词法限定名>`、`module:rust:<同一路径>`。路径保留 POSIX `/`；全局声明不省略文件身份，防止跨文件同名错误合并。Node.module 为无 `module:` 前缀的模块 ID。metadata.language 保留语言。

边使用既有 Edge；resolution 为 resolved / external / dynamic / ambiguous / unresolved。只有有静态绑定依据的内部显式调用可以 resolved；候选不得作为确定边。闭包参数、trait/interface/virtual 分派、属性覆盖、宏展开、回调、动态导入、跨语言调用和不受支持的注册机制保留未知。外部边界如可能回调，metadata.callbacks_unknown 为 true。重复定义用 metadata.duplicate_definition 与 definitions 记录，相关调用不能确定。

前端必须给出诊断和失败文件，不把无法解析的输入伪装成空成功图。所有位置从保存的文件得出，行号为 1-based。确定的函数声明/词法函数别名、相对导入、明确重导出应尽量解析；对象方法、构造函数及类型推断宁可保守。

配置 `analysis.module_aliases` 是 TypeScript 模块名到项目内源码入口的显式映射（相对文件/目录；禁止绝对路径/..）。Rust `analysis.rust_crates` 是 crate 导入名到项目内 crate 根目录的显式映射。这些映射纳入 policy_hash；不能猜测 package 构建结果。

## 根代理负责

根代理修改 models/config/service/analyzer 的分派及版本、新增 analysis.py/source_reader.py/parsers.py，负责依赖声明、安装工具语法库、静态扫描、数据库、服务启动、最终集成。保持 Python 原功能。

## 子代理职责

- static_analyzer：仅 owns typescript_analyzer.py。
- snapshot_storage：仅 owns rust_analyzer.py。
- graph_detection：只读 CodePatchBay，owns reports/real-repositories/codepatchbay-policy.json 和 CODEPATCHBAY_SOURCE_REVIEW.md；选取有明确源码依据的入口、正/反约束并记录意图来源，不把自己设定的规则当仓库缺陷。
- documentation_examples：只读 WinWinCode，owns winwincode-policy.json 和 WINWINCODE_SOURCE_REVIEW.md；同上，并给出模块别名/crate 映射。
- exploration_ui：owns web/，静态复查真实大图/多语言数据下的状态和显示，必要时修正，不运行浏览器测试。
- astra_architecture_review：独立只读各实现与代表性源码，owns REAL_REPOSITORIES_REVIEW.md；审查错误确定性、覆盖遗漏、证据一致性，缺陷通知 owner；不执行目标。

reports 文件是本工具的评估产物，不是目标仓库的任务追踪。两个仓库保持原提交，不安装其依赖、不触发其 code-index 命令、Beads、脚本或其他项目执行入口。
