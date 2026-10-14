# TypeScript 静态分析能力准备草案

本草案只做源码与固定语法库核对，等待 Astra 全面报告驱动实施。没有修改 CallScope 核心代码或两个目标仓库，没有执行、导入、构建或测试目标。解析操作只运行受信 Tree-sitter 读取源码文本；文中的派生片段仅用于观察语法形状，不作为修复正确性的证明。

核对基线：`reports/upstream-reuse/codepatchbay-summary.json` 和 `winwincode-summary.json` 的 `problem_files`。读取时，以下 9 个 TS/JS 文件的原始字节 SHA256 均与摘要一致。实际库为 `tree-sitter 0.25.2`、`tree-sitter-typescript 0.23.2`、CPython 3.12.14。

## 1. 失败机制与源码证据

对每个文件的相同原始 bytes 分别使用 `language_typescript` 与 `language_tsx`：两种语法的 ERROR/MISSING 数量、位置和上下文相同。因此本批 inline import 类型失败不是误选 TSX。

| 仓库 / 文件 | 原始位置 | 机制 / 语法节点 |
| --- | --- | --- |
| CPB `core/indexing/local-code-index/gc.ts` | 225、378、390、441、453、495 | `let entries: import("node:fs").Dirent[]` 等：库在 `lexical_declaration` 插入 `MISSING ";"`，把数组类型后缀拆到另一个表达式。 |
| CPB `shared/primitives/process-tree.ts` | 952 | `let child: (import("node:child_process").ChildProcess & { detached?: boolean }) \| null = null`：`variable_declarator` 中 ERROR。 |
| CPB `core/indexing/local-code-index/rules/types.ts` | 30 | `PatternCaptureGroups = Readonly<{ abstract?: string; ... }>`：type-only `object_type` 把合法属性名 `abstract` 当修饰符，形成 ERROR。 |
| WWC `apps/client/src/application.ts` | 966 | `let project: import('./chat-page.js').ChatPageOptions['project']`：库在变量声明插入 `MISSING ";"`。这是前端组合根，不能用其他文件成功比例淡化此覆盖缺口。 |
| WWC `apps/client/src/candidate-run-preview-control-plane.ts` | 325、333 | `Promise<readonly import(...).PreviewLogSegmentFacts[]>` 的 `type_arguments` ERROR；变量同类数组类型插入 `MISSING ";"`。 |
| WWC `apps/client/src/community-control-plane-client.ts` | 2935、2946 | 接口属性 `readonly import('./generated/contracts.js').DeliveryEvidenceProjection[]`：`type_annotation` ERROR。 |
| WWC `apps/client/src/home-recent-visits.ts` | 135 | 模板 `${stored.scope}<U+0000>${stored.deliveryId}` 含真实 `00` 字节，`template_string` ERROR。 |
| WWC `apps/client/src/readiness-view-model.ts` | 473、482，连带 576 | 模板及 `.join('<U+0000>')` 含真实 NUL，词法错误导致后续括号/表达式结构错误恢复。576 行不是独立的业务错误证据。 |
| WWC `schema/winwincode-export/v1/validate.js` | 288 | 模板 `${project.sourceOrganizationId}<U+0000>${project.slug}` 中真实 NUL，`template_string` ERROR；换 TSX 没有改善。 |

这里的 `<U+0000>` 是报告中的可见表示；目标文件实际含单字节 `00`，不是字符序列 `\\0` 或 `\\u0000`。CPB 摘要中的 Shell `unsupported` 和 WWC 的 Rust `parse_error` 属于其他前端范围，本草案没有把它们当 TS 语法问题处理。

局部语法观察：将 import 类型的 `import('...')` 区间变为派生的 type identifier 后，数组 / indexed access / readonly 泛型结构均被库正确识别；type-only `"abstract"?: string` 可解析；字符串 / 模板的文本转义 `\u0000` 可解析。这只证明替代语法形状可接受，尚未证明可靠识别原始区间或完整的运行语法等价。

## 2. 修复方案及正确性约束

优先选择可审计的语法前端修复：升级 / 修补并固定上游 grammar，或单独安装受信 TypeScript parser，使用纯语法 AST API（如 `createSourceFile` 与 parse diagnostics），不创建执行入口、compiler program、emitter 或目标依赖加载。后者属于源码解析，需要有自己的固定依赖路径与进程环境，避免目标目录、NODE_OPTIONS / loader hook 影响工具模块加载；也要明确 UTF-16 offsets 到原始 UTF-8 bytes 的位置映射。

如采用严格的派生解析适配，需要同时满足：

1. 原始 `SourceFile.content/hash`、证据与源码快照不变；绝不能把改写文本保存成目标源码或静默替换 evidence。派生 parse input 的 hash、原始 error 列表、规则版本、适配区间、可逆位置映射独立保存，并进入解析器 / 分析器身份。
2. import 类型只能在证据充分的类型上下文适配。依据合法声明的 colon / return type / type-only property / type alias 结构及有界 lexer 验证，不依赖一条全局 regex，也不把 ERROR 覆盖范围自动判为 type-only。`import()`、`await import()` 的运行表达式、模板插值和 import specifier 保持原样。
3. `import('...')` 的派生占位符只存在于类型语法，保留原始类型引用来源；不得进入运行值绑定、调用边或 API 可用性判断。合成名字不得与实际符号混用。若做等宽替换，需验证每个字节区间；否则必须使用完整的 offset map，函数、闭包、调用位置全部映射回原始源码。
4. `abstract?` 仅能在确认 type-only 对象成员的位置识别为属性名；运行对象、类的 abstract modifier、计算属性和其他关键字歧义不能套用此规则。
5. NUL 需要有字符串 lexer 范围的支持，区分普通字符串、模板原始文本、`${...}` 插值、转义、注释、regex 和 tagged template。优先修补 lexer；若为派生解析转义，原始 literal 内容和 raw/cooked 区别仍必须保留，不能把派生字符串解释成实际业务值，也不能全文件 `replace(b'\x00', ...)`。
6. 原始字节、源位置与调用语法 tokens 的保留必须可核对。仅适配一个缺口后仍有任何未识别 ERROR/MISSING，则继续 partial / coverage gap；不能简单忽略 `has_error`。适配成功状态也要公开 `raw_parser_error` / `adapted_parse` provenance，避免呈现为库直接支持了原始文本。

在实现前需要按 Astra 报告确定优先次序；在上述证据闭环形成之前维持现有 parse_error 状态是正确的。

## 3. CPB CLI 的有限候选分派

源码链：`cli/cpb.ts:89–111` 的 `COMMANDS` 对象，154 行 `cmd in COMMANDS ? await import(path.join(CPB_EXECUTOR_ROOT, "cli", "commands", COMMANDS[cmd])) : null`，180 行导出 callable guard，186 行 `mod.run(...)`。

对象有 21 个显式 key、20 个唯一命令文件；`cancel` / `redirect` 都对应 `cancel-redirect.js`。可以从这些字面值与保存的 `.ts` 源码、明确 `run` 导出构造 20 个项目内候选，而不是全局搜索所有名为 `run` 的函数。没有位于此对象内的 `cli/commands/migrate.ts#run` 不能被自动加进候选。

不能把这个对象当穷尽运行目标：19 行 `CPB_EXECUTOR_ROOT` 可由环境覆盖；`const` 不冻结对象；154 行 `in` 还允许原型链成员，未等价于 own-property 白名单；动态 import 的加载与导出可用性尚未验证。默认路径的源码目录只是条件化模型依据，不能替代实际部署路径证明。

建议保留一条 `resolution=dynamic, target=null` 的分派边，增加可审计 metadata：`dispatch_kind`、key→candidate 对应、字面对象 / 计算 import / 调用 site 的来源、root 表达式与环境覆盖、guards、`candidates_exhaustive=false`、`residual_unknown=true`。原有 required-path 仍 uncertain，但下钻可以显示 `cmd == 'task'` 的候选路径。不能将 20 条 may-call 加入 resolved adjacency，也不能用候选满足确定约束。

后续只有在词法值、对象写入 / alias / escape、限定 root、own-property guard 与全部被捕获的导出均有证据时，才能声明候选集合在明确模型下穷尽；多候选本身仍不等于每个候选都会执行。外部覆盖或不支持的计算保留 residual unknown。

## 4. 有限对象字面量与工厂返回摘要

真实源码样本：

- WWC `auth-view-model.ts:63` 的 `createAuthSessionViewModel` 正常返回显式对象，包含 `restore/logout/subscribe/close` 等方法；`application.ts:220` 绑定 `authSession`，394 / 712 / 2058 行调用 `restore`，2030 行 `subscribe`，2111 行 `close`。对象中有 `get state`，读取 getter 必须与方法调用分开。`client.restore/logout` 仍是传入端口，不能因返回对象已知而猜测 client 实现。
- WWC `editable-draft.ts:101` 构建 `controller` 字面对象，276 行正常返回同一局部 binding；`strongflow-review-annotations.ts:79` 返回方法集合，但 `togglePin` 通过 `this.isPinned/unpin/pin` 调用，必须保留接收者绑定与方法提取 / bind / call 的差别。
- CPB `engine-runner.ts:73` 的 `buildServices` 返回局部 `ports`；其中 broker 分支、环境配置、`.bind`、`withJobOptions`、`buildCreateJobPort`、参数注入都存在。首次能力应按字段保留候选与未知，而不是把 `RunJobPorts` 类型声明当实现。
- CPB `github-adapter.ts:67` 的 `createGithubAdapter` 返回 `validateGitPlatformAdapter(adapter)`；`core/contracts/git-platform.ts:30–44` 在检查后正常返回原始参数，且本函数没有把对象替换为另一个返回值。这允许一个源码证明的正常返回 alias 摘要，但不证明检查不抛错。`resolveGitPlatform` 的 cache / `registerAdapter` 会引入其他对象，不能继续按名称把所有返回值唯一绑定到 GitHub adapter。

建议先实现 allocation / return / field 的保守摘要：每个被解析的字面对象拥有 source allocation identity；字段包含 callable candidates、unknown remainder、getter / spread / computed / overwrite 标记；跨文件工厂需先唯一解析 callee，再分析所有正常 return（排除嵌套闭包的 return）。命名 `create*` / `build*` 只用于发现审查对象，不参与目标确定。

最初输出候选即可增加解释力。若进一步产生 resolved，需要能证明特定调用 site 的唯一接收者与 own method 绑定，包含词法遮蔽、变量重赋值、属性写入 / delete / defineProperty / prototype 改写、对象 alias、未知 escape、调用前控制流合流等失效条件；条件不够就降为 unknown。方法或对象 `readonly` 类型并不证明运行时不可改写，`Object.freeze` 也不能只靠文本匹配识别。

向函数参数传播对象必须保留 call-site/context 证据，不能把所有 caller 的对象合成一个唯一实现；进入未知 callback / 外部函数 / 动态注册后保留缺口。`bind/call/apply`、getter、Proxy、缓存返回、继承、Promise 与未知工厂不在首版唯一目标支持范围。整个过程是静态摘要与数据流，不调用工厂、不模拟业务执行。
