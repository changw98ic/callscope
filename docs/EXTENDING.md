# 扩展指南

CallScope 的扩展目标是增加静态分析能力并保留证据一致性。扩展不得导入目标模块、执行目标代码、调用目标构建/测试工具、安装目标依赖或启动沙箱。工具自身的固定语法库与目标项目依赖分开管理。

当前接口是固定注册的工具模块边界，不是动态插件加载系统。v0.15 默认 `analysis.languages:["all"]`，展开为 38 个规范语言/格式 ID：保留 Python、TypeScript 家族与 Rust，新增语言结构提取直接复用固定 CodeGraph。Axon 提供确定图索引，CocoIndex 可选缓存语言前端；CodeGraph 候选不进入确定邻接。完整目录、Node.js 20–24 和元数据/模板边界见 [CODEGRAPH_REUSE.md](CODEGRAPH_REUSE.md)。配置只能是数据，不定义脚本或可执行回调。v0.14 scope2 冻结结果继续属于原版本，以下历史查询不升级为 v0.15 验收。

v0.13 历史正式依据为 [CPB 自动报告](../reports/astra-iteration11/codepatchbay-automatic-report.md)、[WWC 自动报告](../reports/astra-iteration11/winwincode-automatic-report.md)及各自 [CPB integration](../reports/astra-iteration11/codepatchbay-integration.json)、[WWC integration](../reports/astra-iteration11/winwincode-integration.json)。13+18 条所选链的保存状态均为 `scoped_source_relations_supported`；[正式账本](../reports/astra-iteration11/goal-ledger.json)保存五项 `scoped_static_judgment_reproduced`、complete/full 均 true、必要缺口为空，30项必要关系全部 supported、未闭关系为空。[判断证据](../reports/astra-iteration11/GOAL_JUDGMENT_EVIDENCE.json)包含704项真实引用。31条、五判断和30关系各有范围，均不作为全文覆盖率或全部功能通过数；资源写者仍保留 partial ownership assessment，wire/外部效果/一般状态空间仍有明确边界。

该版每库两次 `full` 静态扫描分别重算前端与检测，冷/热同 ID、创建标记 true/false；未使用这一结果声明增量缓存效果。源码 hash 与 v0.12 相同，解析330/333与465/471、快照 partial 保持。[原26项比较](../reports/astra-iteration11/ORIGINAL_BASELINE_COMPARISON.json)为10 reproduced/3 unknown/13 evidence_only、两库 changes=[]；36原引用的保存/现场 hash 和冻结 commit 匹配。[发布身份](../reports/astra-iteration11/PUBLICATION_IDENTITY.json) verified=true、共享组件一致、60份当前/存档核心一致。这些核对不扩成全部功能无回退、精度/性能结论或审批。

[正常 CLI 报告导出](../reports/astra-iteration11/CLI_REPORT_READBACK.json)已核对 WWC 导出与正式 Markdown 的字节/hash、保存数据逻辑/schema/身份一致，没有重扫。阅读该版结果可从 [CPB摘要](../reports/astra-iteration11/codepatchbay-analysis-summary.md)、[WWC摘要](../reports/astra-iteration11/winwincode-analysis-summary.md)与 [发布说明](../reports/astra-iteration11/REPORT.md)开始；扩展选题以 [原报告范围差距](../reports/astra-iteration11/REPORT_SCOPE_GAPS.md)和 [条目导航](../reports/astra-iteration11/REPORT_ALIGNMENT_RESULTS.json)对应的实际证据为依据，不能用目录盘点或关系数量替代。

## 共享协议

`callscope/models.py` 定义可序列化模型；`callscope/config.py` 校验配置。分析器、检测器、存储和客户端统一使用这些协议。

扩展需要遵守：

- 源码位置使用项目内相对 POSIX 路径，时间为 UTC ISO8601。
- 每个确定调用目标都要有解析依据；不确定目标保留原因与候选。
- 未支持或失败的部分生成诊断，不用空图假装成功。
- 发现与证据绑定分析快照，处置记录独立保存。
- 输入规范、分析器、检测器和模型变更进行版本管理；宿主解析器也属于分析输入。
- 兼容变更不能让同一个快照身份代表不同不可变事实。

## 添加语言或框架分析器

当前入口：

```python
def analyze_project(root: str | Path, config: dict | None = None,
                    *, frontend_runner=None) -> GraphSnapshot:
    ...
```

统一入口位于 `callscope/analysis.py`；`callscope/analyzer.py` 保留兼容入口及 Python 前端。`language_catalog.py` 统一规范 ID、别名、扩展名、特殊路径和能力层级，`all` 展开为整个目录；显式历史语言列表不自动扩展。JavaScript/TSX/JSX 归入原 TypeScript 调度，不能再注册重复扫描。未知后缀只盘点路径；已识别但未配置或无前端的输入保留 unsupported。

新增语言需同时明确 catalog 层级、配置/服务分派、捕获规则、组件身份及缓存初始化。复用 CodeGraph 时在 `codegraph_frontend.py` 转换已捕获文本、源码身份、位置、状态与候选，不能把上游 confidence 或唯一候选转为 resolved。YAML/Twig/XML/properties、模板和嵌入语言分别保留元数据/局部结构边界；注册和语法可加载不表示已完成真实项目验证。

`source_reader.py` 负责一次安全捕获，Python 消费 `captured_files`；TS/Rust 与 CodeGraph 桥接沿用以下返回协议，具体版本由各组件提供：

```python
ANALYZER_VERSION: str
PARSER_VERSION: str

def analyze_files(files: list[SourceFile], root: Path, config: dict) -> dict:
    # 返回 nodes / edges / files / diagnostics / stats
    ...
```

适配器不得重新读取或执行目标源码，不修改调用方的 `SourceFile` 对象；通过新的文件对象返回解析状态。最终身份由统一入口生成，语言前端不独立发布快照。

CodeGraph worker 只接收相对路径和文本/哈希，不序列化真实目标根。新增项目清单须先通过安全捕获进入快照；虚拟文件系统之外的解析需求保留 unknown。使用 `ensure_runtime()` 初始化固定 Node 工具，不为这些新增语言调用 Python `language_parser()`。保存 `metadata.language` 为规范调度 ID，实际方言另存 `upstream_language`，避免跨语言统计和缓存串包。

推荐步骤：

1. 定义支持范围：语法版本、源码根、模块解析、函数/方法、导入别名和动态关系。
2. 消费统一读取器已捕获的 `SourceFile` 内容、哈希和状态，不二次采集工作区。
3. 构建 `Node`，处理重名及模块冲突；节点 ID 必须具备明确命名空间。
4. 构建 `Edge`，输出调用位置、表达式、目标、状态和解析原因。
5. 输出诊断和统计，计算包含全部分析输入的身份。
6. 让 UI、图算法和检测器能够理解新增实体与关系；未支持的特性继续展示未知。

`GraphSnapshot.parser_version` 保存工具源码、图/维护后端、各语言前端及实际语法库/宿主版本的规范组合，并进入快照身份与版本可比性；`stats.component_versions` 保存结构化明细。新分析器应记录实际解析工具/运行时版本，不能把不同解析器结果混在同一身份下；未知旧版本不应伪装成当前宿主版本。CocoIndex 模式必须记录 worker 实际版本，而不是仅记录父进程环境。

TypeScript/Rust 使用 `parsers.language_parser(kind)` 与 `parser_version(kind)`，从本工具 `.analysis-tools/python` 或 Python 安装目录加载语法包，不搜索目标目录。可选依赖在 `pyproject.toml` 的 `languages` extras 固定版本声明。全量模式缺依赖返回解析失败与诊断；CocoIndex worker 初始化/运行依赖失败使更新失败，不缓存成正常结果，也不能回退执行目标编译器。

TypeScript v0.4 的 `syntax_projection.parse_with_projection` 只为受支持的类型 import、类型属性和字面量 NUL 构造派生 CST。适配版本为 `ts-syntax-projection-1`，前端版本为 `typescript-tree-sitter-call-2-projection-1`。原 `SourceFile.content/hash` 不变；CST位置保持保存文本 UTF-8 字节及行列的恒等映射，原文件字节哈希另存。原 parser 错误、派生 errors、edit 证据、原/派生哈希必须保留在模块 `metadata.syntax_projection`，节点/边关联 projection 来源。扩展新的适配规则需有正向语法上下文与严格派生校验，不能全局正则删除 ERROR 或把运行时 import 改成类型声明；动态运行关系仍保留未知。完整范围见 [STATIC_SCOPE.md](STATIC_SCOPE.md)。

TS/Rust 节点使用语言、相对文件去扩展名及词法限定名组合，格式为 `ts:path#qualified`、`rust:path#qualified`；模块加 `module:` 前缀，Rust 方法采用 `Type.method`。`Node.metadata.language` 记录语言，不因跨文件同名合并节点。

v0.4 的 Rust 基础前端 `rust-tree-sitter-1.5-concrete-self` 仅增加非泛型具体 impl 内直接 self/Self 到唯一固有方法的解析；具体 trait impl 内调用固有目标也属于该范围。节点保存 `impl_type`、`impl_type_name`、`impl_type_id`、`impl_trait`、`impl_trait_implementation`、`impl_generic`、`impl_location` 等来源；trait 方法 ID 仍保留 `<Type as Trait>.method`。确定边保存 `receiver_type`、`receiver_type_name`、`receiver_type_declaration`、`receiver_impl_location`、适用时的 `receiver_binding_location`、`target_declaration`、`target_impl_location` 和 `binding_basis`。不能将字段接收者、generic/where、dyn/trait、Deref、配置/宏或多目标候选按名称提升为确定边。trait 默认成员、reference/blanket 成员、相关 trait 来源缺失/部分解析，以及 receiver 借用/所有权形状也进入保守分析；receiver 未知时可能降级全局绑定，不能为提高样本数字忽略这条防线。

静态工作区配置 `analysis.module_aliases` 将 TS 导入名映射到项目内源码入口，`analysis.rust_crates` 将 crate 导入名映射到 crate 根目录。映射不能含绝对路径或 `..`，纳入配置身份。它们不允许 shell、构建或动态加载逻辑。

统一源码读取器使用 POSIX 目录文件描述符读取、`dir_fd` 和不跟随符号链接接口。跨平台适配需要单独设计安全读取边界；首版未适配 Windows 原生环境，不能只因使用标准库便宣称可移植。

框架入口可从静态装饰器、注册表和配置声明中提取。不能启动框架来枚举路由，也不能依赖 import 触发注册。对于只有运行时才能获得的注册结果，保留未知边界。

多语言项目须定义跨语言关系的来源与命名空间。并列解析多种语言不能证明跨语言运行通信；只解析了一种语言时，不应将其他语言当成“没有调用”。统一入口保留 `by_language`、未支持文件、失败文件及 frontend 诊断，覆盖失败与调用关系失败分别报告。

v0.12 所用前端为 `rust-tree-sitter-1.7-generic-lexical`，当前 v0.14 继续使用 `rust-tree-sitter-1.8-crate-attribute-context`，继承 helper 模型。`analysis.rust_helper_profiles` 显式记录 `{id,crate_root,workspace_manifest}`，现有 profile 为 `serde-1.0.228-declared-helper-v1`；`analysis.rust_interface_models` 可独立注册 `rust-core-cmp-eq-interface-v1`，两者默认空。profile 使用 `analysis.support_inputs` 捕获的 Cargo 原文/锁文件精确身份、完整名称环境及配对属性；错哈希、版本/别名patch、遮蔽、未知宏、cfg/generic等保守拒绝。accepted只解除对应helper，生成正文仍unknown。receiver接口模型涵盖默认成员竞争，“无生成固有/Deref”是显式假设；标准库源码未捕获、项目工具链未验证。受影响边保留 `receiver_helper_model` / `receiver_standard_interface_models`，扩展不得隐去模型前提或执行Cargo求证。

`rust-generic-same-impl-lexical-v1` 仅绑定同一泛型固有 impl AST 身份内的直接 `self.method()` 或 `Self::static_method()`；源/目标须唯一、完整捕获且无额外方法约束或相关成员竞争。字段接收者、trait/dyn 目标、其它 impl 候选不因此确定。边 `generic_impl_binding` 保存 impl 原文哈希/header/字节范围、源/目标声明、实参数量和剩余边界；泛型实例化、bounds、实参类型、执行、完整编译器命名空间和宏展开未验证。扩展不能将词法关系改称编译结果，也不能省略借用、Deref、默认 trait 和可见宏防线。

v0.13 的 `rust_source_context.classify_crate_inner_attribute` 只在配置确认的 crate 根、完整直接 `source_file` 内属性 CST、普通十进制字符串值同时成立时，识别 `recursion_limit`/`type_length_limit`。`rust-builtin-crate-limit-attribute-v1` 表示编译限制不改写声明名称；不是全局属性白名单。`inner_attribute_item` 只作用于其包围范围，不再附到下一条 use/item。属性原文、文件/hash/span、crate_root 与 `source_context_version` 保存在 `builtin_crate_attribute_models`；未知属性、外属性、`cfg_attr`、namespaced/复杂值和未知 crate 上下文继续保守。扩展不能因此宣称已展开宏、求值 cfg、验证编译或闭合任意 trait 目标。

## 扩展前端维护引擎

当前 `frontend_runner.run(root, policy, captured, implementation)` 返回 `{results, versions, maintenance}`。`results` 按语言保存既有前端模型，`versions` 保存实际执行组件身份，`maintenance` 保存后端身份。runner 不读取目标源码第二次，也不自行发布快照。

CocoIndex 通过固定 `python -I` worker 消费已捕获 JSON，调用 `analysis.execute_frontend` 注册的工具代码。新语言须同时接入注册表、版本函数、依赖初始化和语言模型校验；不能把项目配置转换为 CocoIndex 变换代码。

当前 memo 是语言整体。完整文件记录包含路径、内容/哈希、状态和模块信息；完整 policy 及工具源码/解析版本也在键中。新增、删除、重命名必须使语言绑定重算，不能仅按现存文件内容哈希缓存。`read_error` 不 memo；解析器运行故障是任务失败，源码语法覆盖不足才是可保留的部分结果。

父进程校验请求指纹、工具身份、引擎协议、语言和文件集合及证据内容。扩展不能跳过这些检查。服务运行期间工具源码变更需重启；运行计数放 publication/status，不能把热缓存状态写入不可变快照。

schema 2 的 `GraphSnapshot.input_evidence` 由 `input_capture.capture_support_inputs` 捕获显式相对路径，记录 `{path,hash,content,status,error,kind,text_hash,size_bytes}`。原字节hash与UTF-8文本hash分开，失败状态保留；完整记录进入快照及CocoIndex身份，捕获失败不memo。代码与辅助路径重叠而身份不一致应拒绝。辅助文本不构造parsed SourceFile/Node，不计代码覆盖；模型与查询均消费保存内容，不回读当前磁盘补历史。

进一步细化缓存需要明确跨文件导入、别名、重导出、条件声明及未知传播的失效协议。当前语言 memo 不证明逐文件语义增量已经实现，全局检测仍每轮全量。来源与边界见 [UPSTREAM_REUSE.md](UPSTREAM_REUSE.md)。

## 替换图索引

`callscope/axon_adapter.py` 把 CallScope 节点/确定边交给固定版本 Axon `KnowledgeGraph`，`GraphIndex.outgoing/incoming` 从其标签、关系及邻接索引取得。替换或扩展后端应保留节点/边身份、多调用位置、稳定排序和方向语义，且不让动态、候选、重复定义或缺失端点进入确定图。

图后端不负责决定调用是否确定，也不提供目标运行证明。运行时图对象不写入快照；随包上游代码、适配器和来源记录应保留许可证，并记录后端版本与工具源码身份。

## 添加检测器

当前入口：

```python
def detect(snapshot: GraphSnapshot) -> list[Finding]:
    ...
```

位于 `callscope/detectors.py`，图操作位于 `callscope/graph.py`。

每个新增检测器应先形成以下规格：

| 项目 | 应明确的内容 |
|---|---|
| 输入 | 使用哪些节点、调用边、配置或静态声明 |
| 假设 | 哪些语言语义、入口和解析状态成立时结果有效 |
| 规则语义 | 什么结构满足、违反或无法判断 |
| 未知传播 | 外部、动态、歧义及失败文件对结果有什么影响 |
| 证据 | 哪些规则、源码位置、边和路径支持发现 |
| 身份 | 发现 ID、跨快照 fingerprint 与引擎版本 |
| 预算 | 图规模、遍历限制与超限诊断 |

返回 `Finding` 时，严重度、状态和结构依据分别记录。路径证据包含真实的调用边与节点，不能由自然语言推断补出不存在的边。若存在证据缺口，返回不确定状态并说明限制。

检测器不得修改传入快照、源码或人工处置。输出顺序、指纹和证据应尽量确定，支持同一分析输入的幂等发布。不同检测器分数没有天然共同量纲，不增加未经定义的统一加权评分。

当前全量算法优先保证支持范围内的稳定结果。以后增加增量检测，需要按检测器定义依赖和失效范围；SCC、可达性等不能用通用三跳截断替代正确性分析。

v0.5 `static_contracts.analyze_contracts(snapshot, rules) -> list[Finding]`（`static-contracts-1`）追加到全量检测，规则通过config校验后一起原子发布。只支持 `literal_set_consistency`（两个initializer的封闭字符串成员equal）和 `required_object_fields`（all_direct_returns的封闭对象键）。选择器为file+精确词法symbol+site，字段对象另用object_path；合同必有provenance和applicability。source_doc仅标签不打开。spread、别名、计算键、未知构造和不完整返回保持uncertain；条件合同即使source_fact_confirmed也始终uncertain，不推断跨语言分支。发现保存contract_hash、source_fact、guard/反证、未知及模型范围，不扩展为业务故障证明。

v0.6 `value_analysis.analyze_value_contracts(snapshot, rules) -> list[Finding]`（`static-value-contracts-1` / `static-value-policy-v1`）消费保存源码，由全量 detect 追加结果并一起发布。顶层 `value_contracts` 只接受数据规则，当前 type 为 `call_argument_value`。subject 精确指定 file/symbol/callee/argument_index/object_path，evaluation 为 all_direct_calls；expected 是 literal/reference/member/call/conditional 的有限树。直接函数主体排除嵌套函数，嵌套类中的匹配调用保留作用域缺口；名称必须按调用位置的声明身份判读，有限 const 初始化来源不构成运行值或堆分析。后置未知 spread、动态键、可变/歧义/转义绑定和超出预算均不能作封闭负证。

可选 producer 需独立 subject/expected 及 `transport:{kind:external_contract,conditions:[...]}`，且 applicability 必须 conditional。它只并列两个源码事实，不推断端到端传递、入口/分支执行或运行值等价。Finding.type 为 `static_value_call_argument_value`，Evidence.kind 为 `static_value_analysis`，保存比较、词法来源、callee 绑定依据、位置/哈希及未证明范围。只返回差异或未知；空列表不是所有合同满足的账本。增加其它值模型必须另定义语义和版本，不能把字段同名当数据流或把 callee 拼写当 CALLS。

v0.7新增两条模块入口，仍在全量detect中与快照一起原子发布：

```python
navigation_analysis.validate_navigation_rule(rule) -> None
navigation_analysis.analyze_navigation_contracts(snapshot, rules) -> list[Finding]
atomicity_analysis.validate_atomicity_rule(rule) -> None
atomicity_analysis.analyze_atomicity_contracts(snapshot, rules) -> list[Finding]
port_wiring.analyze_port_wiring(snapshot, navigation_rule) -> dict
```

顶层navigation_contracts接受navigation_query_context：producer为assignment/call来源，consumer选择factory调用实参callback及returned_method，显式注册URL/字符串/Object.freeze三个固定模型和ambient条件，可选wiring选择boot/injection/use。AST生成possible/guaranteed query keys、参数/返回、具体callback、null/throw/await链；不可把配置中的必需键或结果直接当实际keys。port_wiring保存五有限装配段，route_activation仍独立；literal Promise.all import模型不改原动态CALLS。模型中的抽象求值只解释有限AST操作，不执行目标函数。

atomicity_contracts接受protected_deduplication：配置facade、authority、predicate_sources、protection wrapper/lifecycle及resource，可选dependency_assembly/transition。版本保护模型提供语义条件，实际callback/resource转发、acquire guard、fresh read/callback/save/release尝试、查重谓词、key字段及patch从源式提取。unknown wrapper不得当无保护，候选deps不得当实际绑定，同member-path不得当集合heap；不接受预填交错，interleaving_inferred=false。

新检测器共用semantic_sources.SemanticSources(snapshot)的load/select/call_binding及SemanticDocument的原文/位置接口；semantic-snapshot-sources-1核对原hash、UTF-8文本、BOM偏移、projection身份及完整call span。lexical_bindings.LexicalBindings(document)提供resolve(identifier_node)、declaration_for(identity)、writes(identity)，当前版本captured-lexical-bindings-3；简单rest叶声明身份不等于rest值或排除集合已知。声明唯一、局部origin稳定、运行值和资源/heap身份必须分开。缓存的AST/索引仅用于该保存快照，不重读工作区；support原文不伪造实现节点。拓展不得绕过遮蔽、alias/computed write、escape、generator、async completion及语法缺口。

v0.8共享接口为：

```python
BuiltinEnvironment(document).audit(name, at, member=None) -> dict
function_kind(document, function) -> dict
completion_relation(document, call, function,
                    consumption="return_or_await", *, lexical=None) -> dict
summarize_field(snapshot, selector, *, parameter_index, field_path,
                sink, models) -> dict
collect_site_relations(sources, document, definition, lexical, site, *,
                       subject_parameter, sink, field_path,
                       branch_conditions) -> dict
field_analysis.validate_field_rule(rule) -> None
field_analysis.analyze_field_contracts(snapshot, rules) -> list[Finding]
```

前两个模块分别为 `semantic_environment`（captured-builtin-environment-1）和 `completion_summaries`（captured-completion-summaries-1）。内建审计只对认证保存文档及固定profile成立，输出scope/lexical_absence、source/model/policy、visible barriers、host_aliases和opaque_effects；supported只允许消费已注册模型，不认证实际宿主、对象值、callee纯净或调用激活。Object、Promise、Set、URLSearchParams、String、encodeURIComponent和undefined的有限接口按实际使用审计，未登记成员或未知效果不得自定义为安全。

最终Env仅窄注册静态`Object.assign(...)`调用的源码出现；这不是赋予它pure、receiver/arguments效果已知或字段复制语义。字段kernel的复制解释及适用检查独立进行。可见API/prototype/alias/computed写、eval与escape仍可阻止环境模型；不能由appearance审计消除这些缺口。

completion把ordinary sync/async与generator分开，普通sync返回可为任意值或throw（也可能thenable）；direct-await、returned-without-await和正常值关系分别保存。`normal_value_relation_closed`仅在所选正常履约/return到达条件内成立；try/catch条件保留，finally、未知默认RHS及特殊控制可拒绝封闭。body激活、全部完成、运行与资源生命周期不由normal摘要证明。

`field_summaries`（finite-field-summaries-5-ir）与field_analysis（static-field-contracts-4-ir/static-field-policy-v2）接受parameter_field_flow/all_direct_sites。subject=file/symbol/parameter_index/field_path；sink=call_argument(callee/argument_index/field_path)或return(field_path)。必须注册ecmascript-own-enumerable-field-copy-v1，可另注册ecmascript-own-data-read-v1；copy-only可用但Get保持未认证。whole-copy前提覆盖整个相关own-enumerable普通data表面，Get应用另有来源guard，不递归认证child；模型boolean没有匹配proof/capability时降unknown。helper仍须SemanticSources.call_binding认证，配置角色不补实际关系。

普通对象解构只记录`object_destructure_keys`、actual_extracted_keys/has_rest和copy_scope=none_at_pattern_level；不能称为复制整个输入。仅实际rest子绑定产生`object_rest_copy`，保存actual_excluded_keys、rest_binding_id/location以及新对象/浅复制/rest_binding_only范围。该区分属于来源协议，不提升字段判定能力。

字段摘要保留全部assessments/source_facts/normal_returns/abrupt_or_exception_boundaries/analysis_gaps，presence、source form、所选/whole shape、运行值与transport独立。每site保存ir_selected_value、copy_steps/ObservationRef及真实effects的roots/affected/protected/guard/reachability关系；实际Get事实记录key、receiver allocation/version和read-model guard。body返回表达式不证明async fulfilled值；effects按全部distinct barriers判定，24项展示样本与总数/截断/完整指针分别保存。v0.10.1正式engine正常前缀site来源形式保留，selected/source-form true但presence unknown/whole argument shape false；services helper十一键/closed/absent恢复，另四site unknown。见 [第八轮报告](../reports/astra-iteration8/REPORT.md)与 [字段评估](../reports/astra-iteration8/field-assessments.json)。

当前公共semantic_ir（finite-immutable-semantic-ir-3）由字段AST适配器实际消费：allocation、当前ObjectVersion、copy-time ObservationRef、FieldSlot、shared referent、EffectRef和ModelGuard分离；allocate/bind/lookup/copy/write/reachable-effect/join返回不可变状态。复制固定源own-slot观察时点，共享child仍按allocation读取当前状态；未知捕获、alias、getter/proxy及未闭合effects保留barriers。旧mutable value/frame、clone与全局epoch判定已移除，但这不证明实际字段链闭合。

公共记录为frozen/slotted的EvidenceRef、BindingKey、BindingDomain、ValueRef、ObjectRef、ObjectVersion、FieldSlot、ObservationRef、CopyBoundaryObservation、CopyRetentionWitness、State、EffectRef和ModelGuard，只含有限immutable数据，不隐藏AST或mutable Frame，不以Python对象id构造语义身份。公开操作包括allocate、finish_construction、bind、lookup_binding/lookup_object/lookup_field、copy_own_slots、observe_copy_boundary、copy_with_boundary_observation、retain_copy_to_literal_end、write_selected、invalidate_reachable、join_values/join_states、register_guard/supports_guard及to_data。保存原hash/span与模型guard身份；copy观察与live读取不能互换。

EvidenceRef所有内容字段参与evidence_id；添加guard或变更kind必须使用evidence(...)重建。v0.10.1修正模块live cell写后未知域的内部构造，新的工具身份重新产生正式结果，[旧候选](../reports/astra-iteration7/SUPERSEDED_CANDIDATE.md)保持原样。记录的内容标识、snapshot/hash/span与模型guard必须一起维护。

BindingDomain(binding,guard,evidence)认证模块live cell的外部词法域；State.external_binding_domains与immutable_bindings分开。const的不可重绑须有真实声明/初始化证据，不冻结它引用的对象。ObjectVersion.construction_guard只保护未暴露普通字面对象的构造阶段，finish_construction在物化及普通bind/暴露前结束；实际到达root、alias/escape、反射、不完整状态或预算失败不得被保护。join只保留所有分支相同guard，conditional allocation清除保护；copy仍固定每个spread的实际时点。

字段effects必须保留真实callee值、receiver、实参、live capture cells及已暴露域。原始值content未知和对象reachability未知分别表达，TS擦除类型子树不参加运行capture，真实闭包仍扫描。扩大支持时必须保留实际Get/copy模型guard与shared child可变性，不能把opaque调用改为pure或按函数名设置特例。

v0.11 将源码结构关系放在独立的 `field_relations.collect_site_relations(...)`，版本为 `captured-field-source-relations-1`。输入须为 `SemanticSources` 认证的保存文档、真实 declaration/site、唯一 subject parameter 身份及本 site 的 branch guards；输出 actual argument/formal、const alias、当前返回引用、顺序构造、Set 尝试和范围限定的显式写入扫描。关系身份绑定版本、source context、snapshot/hash/span 与 branch context。`proven_source_structure` 只认证所声明的源码关系；不能反向修改 IR projection，也不能从别名声明证明 referent 不变。未支持控制或预算使负扫枚举不完整时，负证必须降为 unknown。

`CopyBoundaryObservation` 与 `CopyRetentionWitness` 是另一个条件证明域：前者记录实际 copy 的当前 ValueRef、source/目标 allocation/version、模型及构造 guard，后者记录复制后 checkpoint、完整后缀出处及匿名 literal 终点。adapter 必须使用实际 copy 操作挂回 checkpoint，不能只用手工 boundary observation 宣称保留。IR 检查全部 retained effects、所选 slot、surface 与后续操作；不以 effect ID 差集跳过重复损伤。明确后置同键写、未知 spread/computed/accessor/prototype、escape/alias、损伤及预算缺口均阻止见证。存在性和 entry-origin 未闭合仍保持未知，观察不参与 slot 修复；只将直接匿名 literal operand 的见证挂到该终点，不能重用到之后的别名端点。

普通 Get 必须同时检查 projection、slot/value 的 closed/barriers/capture 状态，不能将损伤前 provenance 洗入新的封闭对象；缺键 undefined 也不能绕过这一检查。擦除 TS 类型仅跳过类型子树和透明 wrapper 的类型部分，实际 operand/default/closure/computed 子树仍扫描。`captured-lexical-bindings-3` 的 absence 必须区分 binder 与默认 RHS 引用，未知隐式 arguments 或捕获域不得被 helper 直接 AST 执行绕过。

v0.11 正式三字段合同/五site共41条源码结构关系；agent-config.ts:489新增唯一当前copy到literal终点支持，source-form仍unknown。engine原条件来源形式保留、services helper十一键/缺键保持，queue/agent其余入口字段未知未被局部见证修复。见 [第九轮报告](../reports/astra-iteration9/REPORT.md)、[v0.11字段](../reports/astra-iteration9/field-assessments.json)及 [独立关系](../reports/astra-iteration9/field-relations.json)。

先区分当前源码连接、copy-time 局部保留和完整入口来源；再闭合 queue/agent 的 actual Get/copy surface、setter/共享 child、捕获 cell 及 helper/return/Promise 边界，随后扩大消息/预算消费者。不要让各 detector 另复制一套语言解释，也不能把未知调用当 pure。有限接口不等于一般 heap、全控制、跨文档 effects 或完整 DFG。

预算扩展接口：

```python
budget_analysis.validate_budget_rule(rule) -> None
budget_analysis.analyze_budget_contracts(snapshot, rules) -> list[Finding]
```

v0.9引入的顶层budget_contracts仍仅支持bounded_for_loop与counter_exhaustion_guard，evaluation=all_lexical_sites；subject={file,symbol}，counter/limit各为{kind:local_binding,name}，只定位唯一声明，不能填阈值、比较、更新或消费结论。必须注册captured-local-budget-source-v1并保留provenance和conditional条件。来源/比较/增量/helper原文由保存AST与实际CALLS提取，相关而不支持的候选保留unknown；嵌套函数激活另列。source_form_complete只限局部语法关系，数值域、实际次数、termination、全部支配与上游预算归属均未证明。版本为static-local-budget-contracts-1/static-local-budget-policy-v1，Finding.type=static_local_budget、Evidence.kind=static_budget_analysis。每条有效规则保存来源与未知摘要，status始终uncertain；正常形状支持与numeric/runtime/termination/domination分栏。v0.11 历史策略见 [CPB](../reports/astra-iteration9/codepatchbay-policy.json)，该版正式结果见 [保存汇总](../reports/astra-iteration9/codepatchbay-summary.json)，[v0.9预算评估](../reports/astra-iteration6/budget-assessments.json)保持历史身份。

## 扩展完整判断与报告源码关系

v0.12 新增的 `goal_contracts` 和 `report_claims` 均为数据协议。完整判断由 `goal_registry.py` 固定注册 `status`、`pipeline`、`navigation`、`device`、`atomicity`，核对实际适配器证据、必要义务、缺口、预算及来源/策略/合同身份；不能由配置布尔值或义务计数授予完整状态。五判断/30 义务是实现账本，原两份完整分析报告才是报告范围基准，没有重复 Astra 复审或批准环节。

源码关系统一由 `report_chain_analysis.analyze_report_claims(snapshot, rules) -> list[Finding]` 进入全量检测。每条 `report_claims` 精确包含 `id`、`type`、`severity`、`sources`、`models`、`provenance`、`applicability`；来源为 1..32 个唯一 `{role,file,symbol}`，只能定位声明。`document_deployment_consistency` 另须 `documents`，包含 1..4 个唯一 `{role,file}`，只选择已显式捕获的文档。原八类链、v0.13 的八种类型与 v0.14 的三个新增类型并存：

| 类型 | 固定实现模块 | 必需扩展模型 |
| --- | --- | --- |
| `rust_finite_state_selection` | `rust_state_relations.py` | `rust-finite-iterator-enum-source-v1` |
| `conditional_gate_relations` | `conditional_gate_relations.py` | `finite-js-plain-record-gate-conditions-v1` |
| `event_index_projection` | `record_projection_relations.py` | `finite-record-codec-projection-source-v1` |
| `trusted_command_lineage` | `record_projection_relations.py` | `finite-record-codec-projection-source-v1` |
| `unsupported_record_retention` | `record_projection_relations.py` | `finite-record-codec-projection-source-v1` |
| `message_identity_relations` | `message_identity_relations.py` | `finite-captured-record-message-identities-v1` |
| `browser_async_lifecycle` | `lifecycle_ownership_relations.py` | `browser-continuation-guard-source-v1` |
| `resource_writer_ownership` | `lifecycle_ownership_relations.py` | `captured-resource-writer-source-v1` |
| `conditional_state_lineage` | `state_lineage_relations.py` | `finite-conditional-event-lineage-publication-source-v1` |
| `conditional_publication_boundary` | `state_lineage_relations.py` | `finite-conditional-event-lineage-publication-source-v1` |
| `document_deployment_consistency` | `documentation_relations.py` | `captured-document-deployment-qualified-source-v1` |

所有类型仍注册 `captured-normal-statement-control-v1`。消息身份关系可额外声明 `captured-literal-sql-positional-bindings-v1`；它只解释捕获的字面 SQL 与参数 token 位置。固定 `_EXTENSIONS`/`_OPTIONAL_EXTENSION_MODELS` 白名单控制加载和校验，配置不能提供任意 import 路径。当前版本为 `captured-report-source-chains-3-architecture`，策略协议为 `static-report-claim-policy-v2-documents`；`relation_component_versions()` 将固定模块的实际版本纳入快照组件身份。旧保存结果保留其原版本，不能只改版本标签升级。

模块入口形状为：

```python
VERSION: str

def analyze_pattern(analysis) -> dict:
    # 消费已认证的 analysis.roles / sources / snapshot。
    # 用 analysis.fact(...) 保存实际源事实，analysis.gap(...) 保存缺口。
    # 返回 pattern；其中 scoped_source_supported 来自必要关系的实际评估。
    ...
```

这是工具内固定适配器接口，不是配置脚本。扩展应拆成可独立判断的有限 slice，先定义实际 binder、记录/字段来源、消费者、guard 和适用模型，再生成判断。角色齐全或 AST 存在本身不够。已认证根声明与静态成员路径只能提供所选源投影；同名字段、邻近调用、复制语法或多个 session 名称不自动具有同一运行身份。

条件模块可解释有限布尔/enum 分区、短路、提前 return 与条件返回记录；Rust 选择模块可计算有限 iterator/enum 消费者。这些是对源码有限语言的解释，不执行目标表达式，不穷举完整领域状态机。消息模块区分 ordinary record/borrow/clone、enum arm binder、独立请求与有序 correlation 字段域；记录模块区分事件来源、codec、投影及重建调用。opaque call、动态键、未支持分支、值覆盖、wire 和持久化效果必须按各自证据域保留边界。

状态沿袭模型要求真实状态 guard、同分支调用及 await 顺序、事件到 writer 的实际绑定和 queue 同源字段。发布模型只解释实际枚举与布尔输入的有限切片；局部 capability、嵌套 catch 或别的分支不能混成入口布尔选项/必经门。对象成员与选项补丁按源码顺序处理，后置未知 spread/计算键使已有字段未知，不识别成员不能忽略后继续保留已知。未知 transport 可以作为带源码的 opaque frontier，不得补造 CALLS、回调激活或远端成功。

文档模型从保存 `input_evidence` 认证原文/hash/span，再用有限条款语法读取段落、标题、引述、否定和部署限定。代码一侧仍须认证所选声明、真实 binder/参数、guard 和接口来源；关键字共现、引用路径或原报告措辞不能代替这些关系。比较须分别保留 Control Plane 内部范围、凭据材料与引用/长期性、Worker 消费与模型流协议。没有实际证据时保持 unknown，不把本地 route、字节容器或调用接口推成协议绕过、密钥泄露或所有部署结论。

浏览器模块不能把父级 guard 继承到暂停后或嵌套 callback；generation、abort、closed 与写回/处置消费者要有实际词法来源。资源模块只聚合所选写者与同 token 引用，`ownership_assessment=partial_captured_writers_and_consumers`、`unique_fact_owner_proven=false` 仍须保留，不能按目录名或 setter 名称推断唯一事实 authority。泛型端口候选和跨消息关系单列，不生成虚构 CALLS。

外层仍输出 `static_report_claim` / `static_report_chain_analysis`，包装状态 `uncertain`。`scoped_source_relations_supported`、`partial_source_relations`、`unknown` 取决于源认证、图声明绑定、实际 pattern 与预算；展示逻辑不能把状态改成通过。开发查询应记录保存快照、当前模块 hash 和变化情况，并明确不是新版本正式结果；冻结后的核心/策略不在同一轮内静默修改。

## 扩展项目报告呈现

`project_report.py` 的当前报告版本为 `captured-project-analysis-report-3`。生成器消费已保存的快照和 Findings，可从保存源码生成独立版本化的操作与解释，不读取当前目标文件或原报告正文补事实，不重跑检测器来改写保存发现。CLI `report`、HTTP `/api/v1/report` 和 MCP `get_project_report` 共用该入口。

`source_relation_index.entries` 通过 `finding_id`、`evidence_id`、`saved_evidence_pointer` 和 JSON Pointer 引用原 `functional_chains` 的 assessment/pattern/source_facts/source_scope/analysis_gaps。`presentation` 使用 `captured-relation-presentation-2`，优先显示实际 statement/interpretation、条件、有限表及反证；截断必须保留总量、`truncated` 与 `full_value_ref`/`full_table_ref`/`full_row_ref`。`architecture.captured_writer_references` 同样只引用已有 writer groups 与 assessment。

`responsibility_operations.extract_responsibility_operations(snapshot, report)` 和 `architecture_responsibilities.build_responsibility_explanations(snapshot, report)` 使用固定版本的有限操作模型。实际记录构造、字段/绑定操作、已认证调用实参交接、拒绝 guard、return、协议字面字段与正常源码顺序分别保留。职责说明消费这些真实 operands、条件和显式关系；目录/规则/业务标签只导航，不从方法名推断行为。没有支撑操作的解释保持缺口，不用既有事实数量填职责。

`architecture.responsibility_explanations` 中的 operations、源位置与证据引用经索引保存，ID/Pointer 必须在声明的索引范围内闭合，摘要不能把 pool/ID 当作已知语义。`documentation_comparisons` 回指完整条款与来源。重复 source fact 可通过同一分析内 `source_fact_id` 引用，完整记录只存一次；保留原来源身份及明确查找范围，不制造图边。`report_components` 单独记录生成器、操作/解释器、展示与工具身份，不能覆盖保存快照的分析身份。

呈现扩展不得按字段名猜成功、丢弃 false/unknown，或把展示省略当作证据缺口；完整 pattern 和事实保持不变。`presentation_only=true` 明确这层不生成新评级。新格式重新显示旧快照时，旧分析身份与结果不变，不能给旧快照补记新分析器关系。接口字段详见 [API.md](API.md)。

v0.14 scope2 两库正常静态分析、正式报告及共享引用校验已完成，当前结果见 [scope2 目录](../reports/astra-iteration12-scope2/)；原已读有限源码报告内容已由[正式读回](../reports/astra-iteration12-scope2/ORIGINAL_REPORT_COMPLETION.md)确认 complete=true、已知有限内容缺口为空，条件与原未审范围保留。这里的扩展协议不提供全文覆盖率，也不增加 Astra 审批、目标执行或测试步骤。

## 冻结观察与能力账本

基准是独立源码观察数据，不是目标项目的规范规则。格式见 [BASELINE_CONTRACT.md](../reports/astra-baseline/BASELINE_CONTRACT.md)；新增工具能力的核对结果另存，不更新其中冻结的 `tool_support` 起点描述。

当前 Python 模块接口位于 `callscope/baseline.py`：

```python
load_baseline(path: str | Path) -> dict[str, Any]
evaluate_baseline(snapshot: GraphSnapshot, baseline: dict[str, Any],
                  repo_id: str | None = None) -> dict[str, Any]
```

loader 只接受 `final` 的 v1 数据文件，最大 8 MiB，并校验字段、枚举、路径、源码哈希、观察身份与引用范围；它不打开目标路径。evaluator 再校验输入，用保存快照做哈希/引用/调用位置匹配；省略 repo_id 时只按保存的项目根文字匹配，不探测当前工作区。

扩展核对器必须先校验保存源码与原文件哈希、quote和位置，再判读符号及调用。确定直接调用须匹配原调用位置；正长度路径须提供逐边见证；当前解析范围不足时不能用缺边证明不存在调用。unknown_required要求保留该调用位置的未知关系和原因，evidence_only保持“现模型尚不能裁决”，不与目标失败合并。

`status=unknown` 与 `expectation_satisfied` 是两个维度。指定未知观察须保留原调用点的 dynamic/unresolved/ambiguous、target为空且有实际reason，才满足预期；dangling resolved或无明确原因不算满足。证据存在而不能裁决的观察为 evidence_only，满足值为 null。全基准分母、选中仓库全部分母及其它仓库剩余观察分别保存。`confirmed_reproduction_count` 只计 reproduced；unknown-preserved 数量另列，不能合并成确定调用解析率。满足一项观察不是对其中每个 required_capabilities 的独立认证。

核对器的 `evaluator_version`、`evaluator_source_hash` 与实际 import-loaded 实现来源独立记录，不能从当前工具环境覆盖旧快照的分析身份。正向边要求源/目标对应文件完整解析；无关文件覆盖不足不抹去已有正向事实，负向检查仍需要其模型完整性依据。

结果保留完整观察列表，包括源变化、范围排除、证据不可用、端点缺失/歧义和关系不匹配。统计描述人工样本的静态重现与能力缺口，不发布功能覆盖率；人工报告中的五项结论仍需字段/状态/原子边界能力，不能由调用绑定升级自动转成工具发现。

后续边界见 [CAPABILITY_ROADMAP.md](CAPABILITY_ROADMAP.md)。有限表达式、query/callback和保护区域不等于一般字段流、真实路由事件、消息/跨语言或并发交错。[五项合同](../reports/astra-iteration4/GOAL_ACCEPTANCE.md)与 [v0.11 的30义务账本](../reports/astra-iteration9/goal-ledger.json)保留当时0/5、4限定支持/20partial/6unknown的历史状态。v0.12 已另存 [完整判断账本](../reports/astra-iteration10/goal-ledger.json)，不能覆盖旧记录；这些账本均不充当原两份完整报告的验收分母，也不能以角色定位或空 findings 达标。

当前核对器 `frozen-static-baseline-1.3` 继承 input_evidence 仅供 evidence_only 的 hash/quote 验证，不满足正向调用或 unknown_required 的 caller 条件。代码/辅助来源身份冲突或坏 support 返回 evidence_unavailable。见证 binding_models 摘要保存边中的 helper/接口模型及 generic_impl_model，保留原文身份、未验证前提并指向完整 metadata；依赖模型的 reproduced 不等于泛型编译、实际宏或工具链验证。冻结报告仍不修改，v0.5 历史结果见 [第二轮报告](../reports/astra-iteration2/REPORT.md)。

## 替换存储后端

当前后端为 `callscope/store.py` 中的 `Store`：

```python
Store(path: str | Path)
publish(snapshot, findings) -> bool
latest(project_id=None) -> GraphSnapshot | None
get_snapshot(snapshot_id) -> GraphSnapshot | None
list_snapshots(project_id=None) -> list[dict]
get_findings(snapshot_id) -> list[Finding]
record_decision(snapshot_id, finding_id, action, reason,
                actor="local", expires_at=None) -> dict
list_decisions(snapshot_id=None, finding_id=None) -> list[dict]
```

SQLite 后端通过锁和事务支持 HTTP 线程调用，将快照、发现与项目最新指针一起提交。重复身份只能对应相同不可变内容；冲突必须拒绝。快照和处置记录通过正常应用连接追加，不开放改写旧记录。

替换图数据库、对象存储或组合后端时，必须保持：

1. 图、发现和证据同版本发布；不能暴露半套新数据。
2. 旧任务不会在协调缺失时覆盖当前结果；分布式实现需要额外的发布顺序协议。
3. 查询源码来自指定快照，不从当前工作目录临时读取。
4. 处置始终引用存在的快照及发现，不修改检测事实。
5. 客户端接口继续通过服务访问，不绑定底层数据库的查询方言。

多存储之间的发布必须另行设计协调和失败恢复，单库事务无法直接推广为分布式事务。当前数据库哈希链只能帮助检查本地记录一致性，不提供数据库管理员无法篡改的保证。

## 新增查询或客户端

CLI、HTTP 和 MCP 应复用相同服务与 `snapshot_id`，不复制独立检测逻辑。查询需要明确方向、范围及返回预算。自然语言解释如果以后加入，不能直接执行无限制图查询，也不能生成静态证据没有支持的新判断。

源码下钻只访问快照中已保存的路径。客户端不能通过任意绝对路径、shell 字符串或可执行配置请求目标执行。

扩展文档必须明确实际支持范围及未知状态。本轮不运行任何测试，也没有发布准确率或性能结论；以后增加能力仍需遵守用户对目标代码零执行的边界。
