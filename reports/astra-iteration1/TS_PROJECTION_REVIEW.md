# TS 派生语法适配：首轮局部源码观察

这是受信静态解析器的正常操作记录，不是测试通过、运行正确或项目功能完整声明。未导入 / 执行 / 构建 / 测试两个目标，未运行工具测试套件；本记录仅分析前一快照列出的 9 个失败 TS/JS 文件，不是两库全量正式扫描。

实现已冻结，等待根代理统一 fingerprint 后复扫：

- `callscope/typescript_analyzer.py`：`typescript-tree-sitter-call-2-projection-1`。
- `callscope/syntax_projection.py`：`ts-syntax-projection-1`，也纳入 `PARSER_VERSION`。
- 固定库：Tree-sitter 0.25.2、tree-sitter-typescript 0.23.2；没有网络下载新解析器。

## 原失败文件的局部解析状态

输入来源为 `reports/upstream-reuse/*-summary.json` 的 TS/JS `problem_files`。读取的原始文件 SHA256 与前一摘要相同；返回 SourceFile 的 content/hash 逐项保持，不修改仓库。

| 仓库 / 文件 | 前一状态 | 当前局部状态 | 有证据的投影区间 |
| --- | --- | --- | --- |
| CPB `core/indexing/local-code-index/gc.ts` | parse_error | parsed / adapted | 6 个 qualified import type 头 |
| CPB `core/indexing/local-code-index/rules/types.ts` | parse_error | parsed / adapted | 1 个 type-only `abstract?` 属性名 |
| CPB `shared/primitives/process-tree.ts` | parse_error | parsed / adapted | 4 个 qualified import type 头 |
| WWC `apps/client/src/application.ts` | parse_error | parsed / adapted | 2 个 qualified import type 头 |
| WWC `apps/client/src/candidate-run-preview-control-plane.ts` | parse_error | parsed / adapted | 3 个 qualified import type 头 |
| WWC `apps/client/src/community-control-plane-client.ts` | parse_error | parsed / adapted | 22 个 qualified import type 头 |
| WWC `apps/client/src/home-recent-visits.ts` | parse_error | parsed / adapted | 1 个 literal raw NUL |
| WWC `apps/client/src/readiness-view-model.ts` | parse_error | parsed / adapted | 2 个 literal raw NUL |
| WWC `schema/winwincode-export/v1/validate.js` | parse_error | parsed / adapted | 1 个 literal raw NUL |

总计 37 个类型 import 头、1 个类型属性名、4 个 literal NUL，共 42 个等宽区间。失败文件中的其他已证实 type-only import 头也会投影，故区间数不等于原始 ERROR 数。9 个派生 CST 均无 ERROR/MISSING，并通过投影后语法上下文校验；局部图中没有 `__cst_` / `_cs_prop` 合成值节点。

## 原始坐标抽查

行号 1-based，列是 0-based UTF-8 byte column，与 Edge 约定一致。以下调用表达式在原始保存内容的该位置逐字节匹配：

| 源文件 | 调用者 / 表达式 | 行:列 |
| --- | --- | --- |
| WWC `application.ts` | `mountWinWinCodeClient.diagnosticScope` / `resolveScopeContext` | 359:23 |
| WWC `application.ts` | `mountWinWinCodeClient.performRender` / `resolveScopeContext` | 1816:23 |
| CPB `gc.ts` | `enumerateWorktreeKeys` / `readdir` | 227:20 |
| CPB `gc.ts` | `scanStoredObjects` / `readdir` | 380:28、392:28 |
| WWC `readiness-view-model.ts` | `createReadinessViewModel.run` / `publish` | 508:6、519:4、528:6 |

最后三项位于原始 NUL 缺口之后；未移动调用位置。局部输入没有引入所有被导入文件，故不使用其跨文件调用分数或总边数评价仓库能力；完整基准匹配由根代理统一复扫产生。

## 临时语法文本观察

只把内存文本作为 SourceFile 输入，没有执行文本：

- 同一函数同时含运行时 `await import('./runtime.js')` 和类型 `import('./types.js').T[]`：类型缺口恢复，运行 `import` 与 `loaded.run` 两个动态调用保留。
- 类型 import 缺口旁有 `const broken = ;`：仍 parse_error，provenance 为 partial_projection，不进入 Collector。
- NUL 位于普通 code 或模板 `${...}` 的 code：仍 parse_error，没有全局替换。
- 模板插值中一个完整 quoted literal 含 NUL：仅该 quoted literal 区间适配，原来的 `g(...)` 调用仍保留为 unresolved。

这些有限观察用于审查适配边界，不声称穷尽 TS / TSX 的全部词法组合。

## 证据与保守边界

`module.data` 始终为原 SourceFile.content 的 UTF-8 编码；派生解析只用于 CST 结构。所有区间等宽且 LF/CR 位置相同，因此 runtime 节点位置映射为恒等。原文件 byte hash `source_file_sha256` 与捕获文本 UTF-8 hash `original_text_utf8_sha256` 分开保存，避免 BOM / 解码差异被混同。

模块 `metadata.syntax_projection` 保存 raw errors、mode / applied / accepted、派生 hash、规则 / 区间 / 原始与派生文本和 hex / 上下文依据 / identity map。节点与调用边以 `source_parse_mode`、`syntax_projection_version`、`source_projection_node` 链回模块。diagnostic 为 `ts_syntax_projection` 或 `ts_projection_partial`；统计另列 raw_parse_error_files、syntax_projected_files、规则区间数与 partial 数。

类型 import 仅处理有类型上下文的 qualified literal import 头，包含一个严格的声明 colon ERROR 恢复形式，投影后再确认只处于类型语法。运行导入、合成值绑定与业务值推断不从占位符生成。`abstract?` 只适配 type-only object_type 中的该窄形式。

literal NUL 采用单字节 CST surrogate `00 → 7e`，不是把实际源码中的 NUL 改成业务字符 `~`。原始 literal 仍是唯一语义 / 证据来源，派生 literal 不执行、不用于业务值判断；lexer 必须确认 quoted / template raw 范围，派生 CST 再确认 literal 归属。未知 slash、未闭合 literal / comment / interpolation、regex NUL、JSX text 与未知错误继续保留缺口。

Astra 已独立阅读实现及接入，当前未发现确定阻断；这是源码审查结论，不是运行验证或所有语言组合的完整证明。
