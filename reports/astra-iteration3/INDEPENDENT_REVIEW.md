# Astra 独立复核：第三轮静态能力迭代（v0.6）

结论：本轮可以作为有明确边界的静态能力增量交付。冻结的 10 项正向调用／路径观察现已全部重现，3 项应当保留的未知仍然保留；13 项高阶观察仍为 `evidence_only`。新增参数规则自动确认了两处来源形式与配置期望的关系，但没有证明完整运输链或运行值错误。原五项人工业务推导仍未被工具独立自动裁定，不能据本轮结果宣称整体达到或超越完整人工报告。

本审查只阅读 CallScope 实现、配置、目标源码和保存产物。没有运行、导入、构建或测试两个目标仓库，没有运行测试套件、浏览器或自行运行 CallScope。根代理正常运行受信分析工具进行纯静态扫描；这不等于执行目标程序，也不构成目标功能测试。

原始两库提交、[26 项基准](../astra-baseline/capability-baseline.json)和五项人工业务推导保持冻结。基准 SHA256 为 `16b4b05c8818fa1eecf396132ebe2ea29a8f0068801165f0649da379d9041dd7`。本轮的判断范围已在 [REVIEW_SCOPE.md](REVIEW_SCOPE.md)说明。

## 已完成的实现审查

### 参数来源能力

`value_analysis.py` 提供配置式 `call_argument_value` 检查：以文件、精确词法 owner、callee 表达式、参数下标和对象字段路径选择源码，比较有限 symbolic expression 与记录的局部声明来源。producer 与 consumer 分别抽取；两者存在同名字段不会生成跨进程流边或新的 CALLS 关系。

以下设计应当保留：

- 引用身份包含原文件哈希、声明位置、作用域与名称。`const` 别名展开保留该身份，不把不同作用域里的同名变量合并。
- 按对象属性顺序处理 spread：后置明确字段可以提供局部确定事实，后置未知 spread／computed key 则可能覆盖；重复属性、访问器、动态形状和未支持语法保守未知。
- 区分 `||`、`??`、`&&` 和条件表达式，记录调用与初始化源码而不求值。源码形式相同不证明运行值相等，形式不同也不证明运行值必然不同。
- `all_direct_calls` 不把嵌套函数、回调或嵌套类的方法／初始化混入外层调用事实。调用预算或形状不闭合不会静默变成成功；有界证据优先保留 mismatch，完整计数与截断状态独立保存。
- 配置期望中的名称也在实际调用位置做词法绑定。callee 的文本选择与保存调用图中的内部绑定是两个事实；动态导入或端口分派不因函数拼写相同而获得确定目标。
- 规则、模型和工具源码身份进入新快照与政策身份，finding 关联同一份原文与坐标；没有向旧快照补写新判断。

审查发现并由实现者修复了几处实质正确性问题：别名展开丢失绑定身份导致同名来源误配；for-in/of 绑定和无声明循环写入遗漏；命名 function/class expression 的自身名称未遮蔽外层绑定；转义标识符，特别是函数／catch 的解构 shorthand，可能绕过遮蔽检查；嵌套 class 内调用可能混入外层；传统前导零数字可能被解释成错误数值；callee 见证未完整核对唯一 owner、目标存在及解析状态。最终版本均采取精确身份或保守 unknown 修正，没有为当前仓库增加名称特例。

这仍是有限来源形式模型。它没有实现完整到达定义、堆别名、函数返回值求解、所有路径条件或跨进程字段传递。空 findings 只表示当前配置没有产生差异／未知记录，不是被分析功能运行通过。

### Rust 同一泛型 impl 的窄绑定

`rust-tree-sitter-1.7-generic-lexical` 新增 `rust-generic-same-impl-lexical-v1`，从调用者当前的精确固有 impl 中选择目标，而不是抹掉泛型参数后在全局同名表中挑方法。全局成员表仍用于拒绝竞争。

首批只支持同 impl 中直接原生 `self` 接收器，及更窄的 `Self::` 静态函数。源／目标独立的 method-level generic、where、impl Trait、参数属性、turbofish、typed self、字段接收器、重复上下文、cfg／opaque、可见未知宏、未知 trait/default／Deref 竞争及借用不匹配仍受限制。接收器声明有 derive 而缺少完整受限接口模型时，新泛型路径也拒绝放行。

模型证明的是捕获源码中的同 impl 声明关系。证据必须保留 impl 原文、原文件哈希和位置，以及 `generic_instantiation_verified=false`、`bounds_not_verified=true`、`argument_types_verified=false`、`compiler_namespace_complete=false`、`macro_expansion_performed=false`、`execution_verified=false`。其它分支的宏仍保留动态边；本模型不能伪装成 Rust 编译器完成了宏展开或全局实例化。

`baseline.py` 1.3 在 bounded witness 中保存这些前提及完整原 edge 指针，不复制整个命名空间树，也不改变原 26 项判定标准。模型摘要包含 edge resolution，拒绝边携带模型说明不能被误读为接受绑定。原 serde／Eq 可信模型的摘要继续保留。

完成源码复核时的文件身份为：

| 文件 | SHA256 |
| --- | --- |
| `value_analysis.py` | `3963bc48baf8fb8a3f05afd292f50bb6ab1d67e48aef716c3ff7cf3a27efab07` |
| `rust_analyzer.py` | `331cd7994a1eecdf0f794f6035f13226b5fd5333249baee5def5e79b33b23411` |
| `baseline.py` | `db09661e194ca132aed2bf6f4405d3d33ef9ad4157cf690a03f84fb4fe72b905` |

## 三项高阶观察的边界

CPB retries 的自动化目标限于两处源码：pipeline 提交对象的 `metadata.maxRetries: parsed.retries`，与 managed worker 新调用参数对象的 `maxRetries: 3`。后者是独立构造，不是已经证明对同一个对象的覆盖。中间 queue、assignment、inbox、动态 bridge 和 opts spread 的完整传递仍需单独模型；输入恰好为 3、pending 项复用、其它阶段／队列重试预算等反证必须保留。因此原业务断接观察继续为 `evidence_only`，额外 finding 应为 conditional／uncertain。

[PARAMETER_EVIDENCE.md](PARAMETER_EVIDENCE.md)和 [parameter-observations.json](parameter-observations.json)整理了 11 项补充来源、31 个 AST 锚点、8 个文件，作为后续传递分析的材料。它们不是新增到冻结基准里的自动通过项，也不是 11 项已确认缺陷。

WWC 导航尚未自动化组合裁定。[NAVIGATION_EVIDENCE.md](NAVIGATION_EVIDENCE.md)纠正了一个重要泛化：`scopeHash` 会保留 seed hash 原有 query；当前候选来自指定导航传入不含 query 的 `/home/new-task`，而 helper 只加入四个 Scope key。生产闭包读取当前 URL、默认真实 task port、提交前 URL 未补入 delivery 等仍是组合条件。有效 delivery URL、fake 端口和 Chat 新建链是反证；本轮没有生成 URL／闭包装配的端到端证明。

CPB 并发窗口仍是有前提的人工推导。[ATOMICITY_EVIDENCE.md](ATOMICITY_EVIDENCE.md)确认 writer 内部存在再次检查和目录 owner lock，不能报告成“没有锁／没有原子内检查”。外层按同 key 非终态复用，内层按含 description 的复合键且仅 pending 复用；这是不同范围和谓词。短期 process fence 分别保护目录锁取得／释放，跨越 fresh read、callback 和 save 的是目录 owner lock；看到 await 不证明提前解锁。没有同资源身份、生产依赖装配、保护区语义及调度可达性模型，就不能自动宣称某个并发交错已经成立。

## 正式产物复核

我独立读取了两库 `integration`、`summary`、`baseline-v6-and-v5`、[能力台账](capability-ledger.json)、[三条有限合同见证](finite-contract-witnesses.json)与 [Worker 完整边元数据](worker-generic-binding-witness.json)，用标准库核对保存数据及原文身份，没有加载巨型数据库或全图导出。

| 保存项 | CodePatchBay | WinWinCode |
| --- | --- | --- |
| 目标 commit | `4f2d2eca31d90b0122db1c1429dd365672db2393` | `da407e4f3df3719718b23bd8913b73fe3ff73857` |
| v0.6 snapshot | `3952ccb24bb530f5acf7096329ab085043c8e8bf8ee25f77e0ed623cb3be3ec5` | `66019560ade80433538040084e66645953cdf9825b71760b9f8ff0abcd777200` |
| 选入／解析成功／缺口文件 | 333 / 330 / 3 | 471 / 465 / 6 |
| 节点／边／resolved 边 | 11,085 / 60,571 / 23,380 | 32,407 / 171,983 / 16,293 |
| 辅助原文输入 | 0 | 4；不计作新增已解析实现文件 |
| 静态合同／参数合同 | 1 / 1 | 1 / 0 |
| 快照完整性 | `partial` | `partial` |

CPB 缺口仍为 3 个不支持的 Shell 文件；WWC 仍有 6 个 Rust 解析失败文件。解析成功也不表示所有调用可确定。两库正式冷扫描发布新快照，热扫描复用语言 bundle，同 ID 且 `created=false`；冷热保存的不可变 stats 完全一致，检测仍为全量重算。WWC 的 Python 是 0 文件 bundle，不应算成 Python 生产覆盖。

两库保存的工具指纹均为 `79d3ec0c1eadc16578d7fc7c52a381ea80ea89dd6ff427d602ca5d0a49c6391e`，分析器为 `static-multilang-6`，检测器为 `call-rules-5-values`，schema 为 `2`。参数组件为 `static-value-contracts-1`／`static-value-policy-v1`；Rust 与基准核对器的版本和文件身份符合前述复核版本。CocoIndex 1.0.25 与 Axon 后端身份保持；缓存复用是固定输入下工具正常维护的证据，不是项目功能通过的证据。

### 冻结基准与新增绑定

全部 26 项 ID、顺序和期望未变。36 份基准文件的当前只读原字节 SHA256、冻结源身份和保存的 source checks 均匹配；其中 35 份为代码文件，1 份生成协议客户端是辅助原文。85 个原 quote 位置均匹配，没有 source_changed、source_missing 或 quote 失败被排除。台账的逐项状态、源检查与汇总符合完整比较产物。

| 状态 | CPB v0.5→v0.6 | WWC v0.5→v0.6 | v0.6 合计 |
| --- | --- | --- | --- |
| reproduced | 4→4 | 5→6 | 10 |
| unknown | 2→2 | 2→1 | 3 |
| evidence_only | 7→7 | 6→6 | 13 |
| 总数 | 13→13 | 13→13 | 26 |

10 项正向见证均有正确端点、非空 resolved 边序列；其中 CPB 的 service→DAG 路径为连续 3 条边，其余是指定原调用位置的直接边。这是针对性源码观察的重现率，不能转换成全项目功能覆盖率、缺陷召回率或一般语言准确率。两库另有各 10 项旧图规则观察，它们使用不同分母，不并入这 26 项。

唯一状态变化为 `wwc.worker.control-to-dispatch-call`。保存的边 `rust-call:14eb734d0b2507bebd041dd4` 在 `crates/winwincode-worker/src/lib.rs:764:16` 将 `WorkerMain.accept_control` 绑定到 `WorkerMain.accept_dispatch`。其原文件 SHA256 为 `13b6fa9a2a0b697ba48c350ccfd1fa856d70e392d8a1e6239aeb132e45b145d6`；同一个 impl 位于第 399–4152 行，原始 byte 范围 `[16018,169215)` 与 header 完全匹配。源声明第 743 行，目标声明第 2634 行，显式实参数与目标显式参数都为 2。

我核对了完整 edge metadata 与 compact witness 一致：源／目标的可见词法环境没有已记录的局部缺口，同 impl 身份和六项未验证前提均存在。这里的局部环境完整不能覆盖 `compiler_namespace_complete=false`，也不能消除其它作用域未展开宏的残余边界。WWC 本轮 resolved 总数增加 494；我精确复核了这条冻结新增见证和相关守门实现，没有逐条背书其余 493 条。

三条 intentional unknown 都在实际 caller 与原调用位置保留 `target=null`、`resolution=dynamic` 和非空原因：`cli/cpb.ts:186 mod.run`、`core/engine/run-job.ts:127 ctx.appendEvent`、`worker/src/lib.rs:2744` 起的 `self.codex.ensure_thread`。泛型字段没有借同 impl 规则变成确定目标。

WorkRun 第 411、419 行的两条边及 ProductionCodexAdapter 第 3558 行的 `persist_run` 见证保留。WorkRun 的 helper 与标准接口摘要和 v0.5 完全一致：仍依赖显式注册的 `serde-1.0.228-declared-helper-v1`、`serde-1.0.228-receiver-interfaces-v1`、`rust-core-cmp-eq-interface-v1`；没有捕获实际宏展开或验证项目标准库／工具链。新增泛型能力没有抹掉这些旧前提。

### 三条有限合同事实

三条 compact finding 与各自保存快照 summary 的完整记录逐对象一致。规则规范化哈希、finding／evidence 的 snapshot、source、policy 身份均一致；额外独立核对了 42 个不重复原文 span 的 SHA256 与 quote。合同证据的列为从 1 开始的 UTF-8 byte 列，调用图 Edge.column 为从 0 开始，核对时分别使用对应约定。

| 合同事实 | 正式结果 | 能证明的范围 |
| --- | --- | --- |
| CPB 两个终态初始化集合 | `open`；少 `superseded`，没有额外项或形状未知 | 指定声明初始化字符串成员不一致；不认证完整状态机。 |
| WWC clarification 返回对象字段 | `uncertain`；唯一直接 return 的 `payload.spec` 封闭且缺 `verificationCommand` | 返回对象构造缺该字段；Device 适用性仍是外部条件，Rust else 反证保留。 |
| CPB pipeline／worker 参数来源形式 | `uncertain`；producer matches，subject mismatch | 两处指定字段的原源码形式与各自配置比较；完整运输、运行值和业务结果未证明。 |

新增 finding 为 `27afb5ced428b324cdbb8709`，规则哈希为 `d1f5515ac3c8aed55cd7d28b68267e1a692e910bbd033baa4bc0edac0c2de516`。两侧都只有 1 个匹配的直接调用：producer 在 `pipeline.ts:189`，第二实参的 `metadata.maxRetries` 在第 205 行为 `parsed.retries`；subject 在 `managed-worker.ts:1797`，第一实参的 `maxRetries` 在第 1809 行为字面量 `3`。producer 的实际／期望引用有同一 `parsed` 声明身份；subject 期望的 `metadata` 唯一声明位于第 1428 行。

参数证据没有把初始化来源冒充完整值流：`parsed` 的 origin 是 `parseCommonFlags(args)` 调用且 `return_value_known=false`；`metadata` 的 origin 记录 `assignment.metadata || {}`，其中更深层来源仍不完整。第 70 行 `parseInt(...) || 3` 作为单独 AST context 保存，没有执行 parseInt 或推导所有用户输入的预算。两个 callee 的内部动态绑定均未确认，`callee_target_not_inferred`、`value_transport_not_inferred`、`value_equivalence_not_inferred` 三项未知都存在；`runtime_proof=false`、`transport_proof=false`。

既有集合 finding 为 `b8d514b3c229433de24b94b1`，合同哈希仍为 `3cbceb399081fb2060a9b636c454eb592983770f06b7e66336624910b5a4b941`；字段 finding 为 `ad536ba51ec6800f11e480da`，合同哈希仍为 `8543f89585c9e89e5ad118ea3eda9e008c1d92dda16d75c2e48509844228cc67`。字段 finding 继续保留 `external_applicability_not_inferred`。三项规则均标记独立审查来源及 `author_approved=false`，没有冒充维护者已批准的规范。

这 3 条是人工配置合同后自动复核的有限源码事实，与原 26 项并列。原五项业务推导的主状态都仍是 `evidence_only`；参数事实的进展也不能被写成“第三个完整业务故障已自动确认”。导航上下文组合和并发交错尚未成为本轮检测器能力。

## 交付判断与下一步

截至当前实现和保存产物，本轮已确认的 P0／P1 实现问题全部闭环，没有剩余已知交付阻断。未运行的范围包括目标行为、目标或工具测试套件、浏览器、安装包、增删改名失效、故障恢复、并发捕获和完整 Rust／TS 语义；本结论不为这些范围提供保证。

值得继续的是通用的声明身份、字段形状、源码条件和模型前提协议。下一步优先补有来源和反例的函数参数／返回对象摘要，再扩展 queue／assignment／消息的显式传递关系；之后才组合 URL key 与闭包注入、保护区域与资源身份。不要通过更宽松的 resolved 规则或更多图分数替代这些功能。当前工具已经覆盖冻结报告中的全部正向调用样本，但离完整人工业务分析仍有清楚、可追踪的能力差距。
