# 静态调用结构：约束语义与能力边界

## 判定的对象

CallScope 检查源码产生的调用关系及显式有限源码合同。声明提供“应满足什么”的依据；分析器提供当前源码可解析的事实。发现保留定位、合同来源、成立条件和未知，静态功能完整性不等于业务正确性保证。

没有明确约束时，系统可以描述图和图的变化，但不能可靠地推断缺少某项功能。存在同名函数也不意味着它已被正确注册或调用。

## v0.14 当前正式结果与有限静态范围

当前实现为 `static-multilang-14` / `call-rules-13-architecture-explanations`，快照 schema 2，scope2 的[核心与策略已冻结](../reports/astra-iteration12-scope2/CORE_FREEZE.json)。两库正常纯静态冷/热分析及正式报告已保存、数据库已关闭，快照范围仍 partial。原 26 观察比较与发布身份已核对；原已读有限源码报告内容已完成[正式读回](../reports/astra-iteration12-scope2/ORIGINAL_REPORT_COMPLETION.md)，complete=true、已知有限内容缺口为空，原未审范围和 source-only 效果未知保留。下文 v0.13 数字保持历史身份，不用于预填本轮结论。

v0.14 增加真实字段/条件链、职责解释与文档部署对照。条件式状态沿袭提取实际状态 guard、事件字面字段、形参绑定和后续 queue 同源字段；发布边界区分源码模式/布尔 opt-in、callee return guard 与 opaque effect。对象未知 spread/成员不被当作已知值，局部状态及嵌套分支不冒充入口配置或必经门。顺序关系不证明 callback 激活、持久化、实际授权或远端成功。

职责解释由保存 CST 中的记录/字段/绑定操作、已绑定实参交接、guard/return、协议字面字段及正常源码顺序生成，回指完整源位置和证据。业务标签与目录只导航；同 token 写者、partial ownership、source-only 和外部效果边界不因解释出现而被抹去。

文档比较从显式捕获的文档读取有限条款，保留段落/标题、否定、引述和部署限定，再与所选生产来源对照。Control Plane 内部唯一与 Device 本地路径分开；凭据材料/引用/长期性分开，长期性保持 unknown；Worker 本地消费不等于绕过 ExecutionPort 模型流协议，不据此宣布安全缺陷。

正常报告 v3 独立保存职责解释、文档比较、实际条件及反例。报告组件身份与快照分析身份分列；显示旧快照不能补记新发现。本轮是否支持各条有限关系，以 [v0.14 保存产物](../reports/astra-iteration12-scope2/)为准。配置数量、五项/30 义务、操作数、表格行数和解析率都不是功能覆盖率，不增加复审门或目标执行步骤。

正式结果可从 [CPB 摘要](../reports/astra-iteration12-scope2/codepatchbay-analysis-summary.md)和 [WWC 摘要](../reports/astra-iteration12-scope2/winwincode-analysis-summary.md)下钻：所选支持链为 16/20，子追踪判断为 3/2、必要关系为 18/12；职责操作为 15,223/10,023，共享引用检查失败均为 0。原 26 观察与发布身份的核对均保持原证据域，[原已读有限源码内容正式读回](../reports/astra-iteration12-scope2/ORIGINAL_REPORT_COMPLETION.md)已完成，不以这些计数替代，也不证明全程序或运行正确。

## v0.13 历史正式结果与有限静态关系

v0.13.0 的两库正式冷/热扫描与自动报告已保存，数据库已关闭。正式来源见 [CPB 报告](../reports/astra-iteration11/codepatchbay-automatic-report.md)、[WWC 报告](../reports/astra-iteration11/winwincode-automatic-report.md)及对应 [CPB 扫描记录](../reports/astra-iteration11/codepatchbay-integration.json)、[WWC 扫描记录](../reports/astra-iteration11/winwincode-integration.json)。该版 CPB 13 条、WWC 18 条报告关系均为 `scoped_source_relations_supported`；五项原判断均 `complete_assessment=true`、`full_goal_supported=true`、必要缺口为空。正式 [五判断/30 关系账本](../reports/astra-iteration11/goal-ledger.json)保存五项 `scoped_static_judgment_reproduced`、30 关系 supported、未闭关系为空；[证据引用](../reports/astra-iteration11/GOAL_JUDGMENT_EVIDENCE.json)关联 704 个真实来源引用。

两库冷/热轮各自保存相同 snapshot ID，`created` 分别为 true/false；源码 hash 与各自 v0.12 相同，解析范围仍为 CPB 330/333、WWC 465/471，两图仍 partial。[冻结身份](../reports/astra-iteration11/CORE_FREEZE.json)记录 `static-multilang-13`、`call-rules-12-report-relations` 和 60 份 Python 核心来源；版本身份、源码解析范围和条件判断支持性分开。

[原 26 观察比较](../reports/astra-iteration11/ORIGINAL_BASELINE_COMPARISON.json)保存 10 reproduced/3 unknown/13 evidence_only，两库相对 v0.12 的 changes=[]；36 份原引用的保存/现场 hash 与目标 commit 匹配。[发布身份](../reports/astra-iteration11/PUBLICATION_IDENTITY.json)为 verified=true，共享组件一致，60 份核心 live/archive 一致。这些核对维持原观察和产物身份，不产生全文覆盖率。

原两份完整分析报告仍是范围基准，不增加 Astra 复审或批准门。原五项/30 必要关系和该版配置的 31 个报告条目分别用于实现追踪与来源定位，均不是功能覆盖率，也不能推出已经达到或超过原全文。

该版在原有八种报告模式外增加八类有限来源关系，实际字段、guard、状态表和实参关系来自保存源码；规则只提供声明定位、模型和适用范围：

| 新增关系 | 实际计算范围 | 保留的边界 |
| --- | --- | --- |
| `conditional_gate_relations` | readiness 谓词与提前返回后的提交；completion checklist、mutating 条件和各豁免返回；access audit 的失败响应字段到 writer 实参 | 只解释所选普通记录、布尔与严格比较；外部判定、checklist 内部和真实响应效果不由此证明。缺值/null 与普通记录分区分开 |
| `rust_finite_state_selection` | WorkRun 的 effective-state 有限表、依赖量词、iterator 选择、活动排除与所选身份再次检查 | 不穷举整个领域状态机、所有 attempt 或 validator 条件；宏、Clone、集合行为依赖显式有限模型，不把未知调用补成 resolved |
| `event_index_projection` | serializer 结果到 append 实参、projection.state 到同一 index record/writer、事件重放到重建 writer | 正常语句顺序与 record 来源不是一次事务、物理持久化或全部恢复证明；doctor 分支保留源码条件 |
| `trusted_command_lineage` | stdout→JSON→policy parser→lookup→command 实参，以及同一 formal 的 executable/args→结构化执行来源 | 局部声明身份不证明 heap 稳定或全部非干扰；expectedEvidence 仍可参与独立的 oracle 保护路径；没有执行命令 |
| `unsupported_record_retention` | true 失败 marker→返回集合、排除所选 skip、ledger 返回→JSON→artifact content | 缺身份、checklist 匹配、hardGate first-wins、spread 覆盖、abort 和写入失败不能被消除；不是所有输入保留保证 |
| `message_identity_relations` | Chat 当前尝试的请求投影；Worker/adapter 的 job/lease/workspace/profile/session/turn 字段；outbox/ack 的有限 enum、codec、字面 SQL 参数位置 | 不因同名字段合并身份；projection agreement 不证明线上值相等、ack 真实、数据库提交或全部消息族闭合 |
| `browser_async_lifecycle` | generation token、null context 拒绝、abort/closed guard、挂起后的 guard 新鲜性和关闭结果的消费补偿 | 不把父 guard 跨 callback/await 继承；没有局部 guard 不自动定为缺陷；不证明所有旧结果均被拒绝或资源全释放 |
| `resource_writer_ownership` | 所选字段写者、相同捕获 token 的消费者、认证接口实参和拒绝 guard | 固定保持 `ownership_assessment=partial_captured_writers_and_consumers`；唯一事实所有者、规范权威、全部授权和持久资源等价均未证明 |

Rust 上下文还增加严格限于已知 crate root、值为明文十进制字符串的 `recursion_limit` / `type_length_limit` 内建属性模型，修复其被误当作未知属性宏的范围传播。新版正式结果中，原 provider 部署、Worker 入口和生产构造三个条目的有限声明/步骤来源已支持；v0.12 保存的三个 partial 保持原值。其它属性宏、cfg、泛型、未解析声明和 source-only 边界没有因此消失，也不证明实际生产组装已运行。具体模型见 [源码说明](../reports/astra-iteration11/RUST_SOURCE_CONTEXT_DESIGN.md)。

v0.13 项目报告 v2 新增 `source_relation_index` 和 `architecture.captured_writer_references`。它们只引用保存的 Finding/Evidence、pattern、source facts、scope 和 gaps；展示投影明确 `presentation_only=true`，保留 false/unknown、原 JSON Pointer 和截断标记。该版尚未自动汇总所选写者/消费者的具体职责，以及 Device/Credential 文档与实际部署的范围对照，见 [v0.13 范围差距](../reports/astra-iteration11/REPORT_SCOPE_GAPS.md)。v0.14 已实现的承接与正式状态见上文；不把部分所有权升级成唯一权威，也不扩大为全部权限、协议和原明确未审领域的验收目标。

该版正式发布采用 `full` 引擎，冷/热两轮均重算前端与检测；v0.12 使用 CocoIndex。引擎、模型及策略变化单独记录，不把两轮当作相同引擎的性能或纯精度对比。目标代码、测试、构建和 probe 均不执行；自己的静态扫描、保存查询和产物身份核对属于工具工作流。

[正常报告 CLI 读回](../reports/astra-iteration11/CLI_REPORT_READBACK.json)另确认 WWC 导出的 Markdown 与正式报告字节/hash 相同，数据库逻辑、schema 和身份保持，未重新扫描。它验证保存产物的读取与展示一致性，不证明目标运行功能。原报告到正式证据的导航见 [该版对齐](../reports/astra-iteration11/REPORT_ALIGNMENT_RESULTS.json)，不是全文评级。

## v0.12 已完成正式结果与历史范围

本轮以原两份完整分析报告为固定基准，报告文字不参与运行判定，也没有重复 Astra 审批步骤。`goal_contracts` 中五种固定适配器负责完整的所选静态判断；`report_claims` 负责其它主要功能链、guard、顺序、命令来源、失败与部署分流。五项/30义务账本是实现追踪，不替代全文报告的架构、主链、反证和未审范围。正式保存的五项判断complete/full_goal_supported均true，30项必要关系均supported；完整性结论限各项记录的源码/模型条件。

实际状态与证据指针见 [CodePatchBay摘要](../reports/astra-iteration10/codepatchbay-analysis-summary.md)和 [WinWinCode摘要](../reports/astra-iteration10/winwincode-analysis-summary.md)。CPB3判断/18关系、WWC2判断/12关系；18条所选链为15项scoped_source_relations_supported与3项partial_source_relations。WWC的provider部署、Worker入口和生产构造保留图绑定/生产条件缺段；18条captured-source-structure支持不抹去这些缺段，已支持链的外部/iterator/macro边界仍单列。

两库图范围均partial，解析330/333与465/471，捕获辅助输入2与11；这不是判断支持性或功能通过率。新policy、模型和辅助输入改变范围；v0.11局部字段unknown不会被v0.12具名记录/消息模型中的完整条件判断直接改写，原始证据轴分别保留。

完整自动报告见 [CPB](../reports/astra-iteration10/codepatchbay-automatic-report.md)和 [WWC](../reports/astra-iteration10/winwincode-automatic-report.md)。原26项冻结观察保持10 reproduced/3 unknown/13 evidence_only，与v0.11 changes=[]，36份保存/现场原文身份matched；[发布身份](../reports/astra-iteration10/PUBLICATION_IDENTITY.json)verified=true，54份核心与存档一致。原观察、五项/30义务及全文范围分列，不合计成覆盖率。

本轮发布说明见 [v0.12正式报告](../reports/astra-iteration10/REPORT.md)。正式实现追踪见 [五判断/30义务账本](../reports/astra-iteration10/goal-ledger.json)及 [保存判断证据](../reports/astra-iteration10/GOAL_JUDGMENT_EVIDENCE.json)；[全文条目导航](../reports/astra-iteration10/REPORT_ALIGNMENT_RESULTS.json)仅关联原条目和证据，不生成全文评分。 原主链尚未闭合的内容及原明确未审范围见 [范围差距](../reports/astra-iteration10/REPORT_SCOPE_GAPS.md)。

| 完整判断适配器 | 有限模型的实际范围 |
| --- | --- |
| `status` | 捕获的普通状态记录、实际生产/投影/分类和恢复guard；terminal与recoverable的策略分开 |
| `pipeline` | 所选参数记录、JSON消息通道、生产装配及有效预算消费者；记录/通道身份独立于普通CALLS，旧记录、覆盖、提前退出和opaque消费者分别保留 |
| `navigation` | 所选可见入口、query域、真实port/callback与缺键拒绝链；受实际路由、平台和正常回调模型条件限制 |
| `device` | 所选UI/请求/JSON/Serde/dispatcher及Device条件必填guard；非Device/Chat反证独立，不以optional类型免除分支要求 |
| `atomicity` | 源码推导的两个同项目/键/描述默认提交与一个受保护scheduler转换的有限交错；是条件式存在性窗口，不是所有写者或一般并发证明 |

模型适用性由实际源码/声明认证和明确条件共同记录。标准JSON、普通record、锁/callback或生产装配模型不证明真实部署、物理资源、任意heap和语言全部语义。有限交错必须由源中的检查、保护范围、写入和转交关系生成，不接受预填时间线作为发现；顺序复用、pending重复保护、rollback和发布前失败等反证仍保留。

完整判断注册器检查每个必要ID、实际来源/策略/合同身份、预算和适用性证书；全部必需关系支持且无必要缺口才可为 `scoped_static_judgment_reproduced`。完整反证可为 `claim_refuted_or_narrowed`，不完整分析继续缺口状态。包装Finding始终 `uncertain`，`complete_assessment` 与 `full_goal_supported` 分开，不推导目标运行成功。

报告链的源码事实、可信模型、policy和未解析部分分栏；选定语句的顺序不自动成为一般支配关系，嵌套async块/闭包的正文不证明Future或callback已激活。源码同类方法候选可帮助定位，真实 `actual_callee` 未绑定时仍为空。命令来源和 `shell:false` 仅在对应结构化执行模型中解释；allowlist/env/sandbox 分支源码不证明实际隔离或全秘密过滤。

自动项目报告从保存快照/发现产生架构、完整判断、主要链、局部证据、重叠源选择与未审范围。它保留 `whole_report_reproduction_claimed=false`；解析文件数、条目数、关系数和完成的五项判断均不是全项目功能覆盖率。接口与规则协议见 [API](API.md)，完整用途见 [自动项目报告](AUTOMATED_REPORTS.md)。

## 词法声明身份与值稳定性

`LexicalBindings.resolve_identity` 是 `captured-declaration-identity-only-1`：只认证捕获的声明身份，记录 `write_and_effect_review_performed=false`。唯一声明也强制 `stable=false`，模型为 `captured_declaration_identity_only`，`heap_state_verified=false`，理由为 `write_and_effect_review_not_requested`。它可用于参数/实参或source token身份比较，不能充当无写入、readonly、别名堆不变或值稳定证明。

需要可见写入与效果检查时使用原 `resolve` 及对应模型/IR分析。其结果仍不能越过实际效果、共享referent、getter/proxy或预算缺口。缓存了身份不意味着缓存了稳定性；新identity入口未改变原字段来源判断。

## 四类调用规则

配置格式为：

```json
{
  "id": "rule-unique-id",
  "kind": "required_path",
  "from": "app.api.submit_order",
  "to": "app.domain.validate_order",
  "severity": "high",
  "description": "维护者给定的静态调用结构约束"
}
```

`id` 在一个配置内必须唯一，端点使用限定符号名或 glob，`severity` 为 `high`、`medium`、`low` 或 `info`。

| `kind` | 检查含义 | 路径存在时不能推出的结论 |
|---|---|---|
| `required_call` | 必须存在一条确定的直接调用边 | 调用每次都会发生、执行次数符合要求 |
| `required_path` | 必须存在由确定调用关系组成的路径 | 路径可在运行时成立、某调用先于另一调用 |
| `forbidden_call` | 不得出现声明禁止的确定直接调用边 | 所有未解析目标都安全 |
| `forbidden_path` | 不得出现声明禁止的确定调用路径 | 没有已解析路径就绝对不会运行到目标 |

必需规则的量词是：每个匹配 `from` 的源，至少连接到一个匹配 `to` 的目标。它不是要求所有源与所有目标逐对连接。禁止规则则是任何匹配连接出现就形成违规证据。因此需要“连接到每个指定实现”时，应分别写精确目标规则。

规则中的路径必须至少包含一条调用边。`from` 与 `to` 匹配同一符号时，只有实际自调用或调用环满足路径规则，不能靠零长度路径满足必需调用。

层级标签只是展示和匹配信息。定义 `API`、`DOMAIN`、`STORAGE` 不会隐式禁止所有跨层调用；需要对应的 `forbidden_call` 或 `forbidden_path` 规则。多个层同时匹配时保留候选并标记层归属未知，不擅自选择第一个标签。

Python 端点形如 `app.api.submit_order`；TS 端点形如 `ts:apps/client/src/page#mountPage.render`；Rust 端点形如 `rust:crates/core/src/lib#Type.method`。后两者保留文件身份，避免跨文件同名误绑定。工作区包和 crate 的静态映射来自 `analysis.module_aliases` 与 `analysis.rust_crates`，不能把它们理解成编译器已经验证的依赖环境。

v0.5另有顶层static_contracts数据规则：literal_set_consistency比较reference/subject的file+精确symbol+initializer封闭字符串成员（relation=equal）；required_object_fields检查subject函数all_direct_returns中object_path所选字面对象的required_fields。规则必须保存provenance（authority/author_approved/source_doc）和applicability（kind/conditions/counterexamples，可选guard），实际例子见 [CPB](../reports/astra-iteration2/codepatchbay-policy.json) 与 [WWC](../reports/astra-iteration2/winwincode-policy.json)。本轮来源是独立审查，author_approved=false；source_doc是标签，不读取文件执行规则。

集合别名/展开/未知构造器、对象spread/计算键/未知返回、嵌套函数及不完整结构不作封闭负证。检查只描述初始化/字段构造，不能证明运行时值、字段非空、一般传递、所有终态等价或消费者一定到达。conditional合同即使source_fact_confirmed也始终uncertain；守卫与else反证只保存出处，不证明producer进入跨语言Device分支。2条有限事实复核不等于自动确诊2个业务bug。

v0.6 的独立顶层 `value_contracts` 目前只支持 TS/JS 的 `type=call_argument_value`，用 `subject:{file,symbol,callee,argument_index,object_path}` 指定精确词法函数、callee 源码拼写、参数位置和字段路径。`evaluation=all_direct_calls` 只检查该函数直接主体的匹配调用，排除嵌套函数、回调及别名 callee 替代命中；嵌套类内匹配调用保留作用域缺口，不算外层直接调用。实际配置见 [参数来源合同](../reports/astra-iteration3/codepatchbay-policy.json)。

`expected` 是有限表达式树：literal（JSON primitive）、reference（词法名称）、member（object/property）、call（callee/arguments）、conditional（operator/condition/then/else）。conditional 区分 `?:`、`||`、`??`、`&&`，不求值或判断分支是否执行。名称按调用位置的声明身份核对，有限 const 别名可保留初始化来源；可变、重声明、遮蔽不明、转义名称、循环绑定、with、初始化前使用或可见写入等保留未知，不计算函数返回、别名堆状态或实参运行值。

对象路径要求所选字段可由字面 AST 确认；整个对象不必封闭，但后置未知 spread/计算键可能覆盖字段时不能确认。重复显式键、访问器、未知嵌套对象或参数 spread 保留未知；字段完全缺失的负证需要路径处没有未知键来源。callee 匹配是源码选择器，确定内部调用还需独立查看快照边绑定，不能仅凭拼写推断目标或加载的动态实现。

合同可另列 `producer:{subject,expected}`，必须搭配 `transport:{kind:external_contract,conditions:[...]}` 且 applicability=conditional；来源、作者批准状态、适用条件及反证同样必须保留。producer 与 consumer 仅为两个独立 AST 事实，不从同名字段证明队列、消息、进程或跨语言运输。comparison 的 matches/mismatch/unknown 是来源形式结论；形式不同不证明运行值不同，source_form_difference_confirmed 不证明业务错误，conditional 仍为 uncertain。只输出差异或未知，空 findings 不表示完整合同或功能通过。

v0.7新增两个顶层数据数组，均为conditional且须保留provenance/applicability。`navigation_contracts`的navigation_query_context选择producer assignment/call和具体factory实参callback/returned_method，显式注册url-search-params-v1、js-string-url-slicing-v1、object-freeze-inert-v1及ambient hash条件；可选wiring选择boot/injection/use。`atomicity_contracts`的protected_deduplication选择facade/authority、predicate_sources、保护wrapper/lifecycle和资源条件，可选deps/transition来源。实际配置见 [WWC](../reports/astra-iteration4/winwincode-policy.json) / [CPB](../reports/astra-iteration4/codepatchbay-policy.json)。配置只选择角色和模型，不提供实际keys、谓词结果、保护region或预计算交错，author_approved=false不能当维护者政策审批。

导航模型从保存AST推导实参/形参、有限return/字符串和URLSearchParams receiver，记录possible/guaranteed keys及keyset_closed。只有封闭possible集合排除了required key才能作缺键来源事实；set/delete的条件join不把可能键变成必有键，既有query仍保留。动态key、未知mutation/escape、名称遮蔽、opaque返回和预算缺口保留unknown。实际callback按factory context和实参属性关联，读键/null guard、direct-await正常fulfillment及create拒绝分别保存；async throw为rejected Promise，未证明事件激活或处理结果。

有限port_wiring可以对应正常boot、factory分支、同一port注入、VM options.port捕获和返回方法的使用；literal Promise.all import来源是独立模型，不改原动态CALLS。当前五段有限assembly支持仍有route_activation未知、其它方法effects及公开VM普通对象可变性缺口。assembly_complete不等于end_to_end_complete或功能通过；href assignment也不单独认证可见DOM入口。

原子模型提取源码次序、early reuse、callback/resource词法转发、取得guard与fresh read/callback/save/release尝试，分别记录process fence和目录owner锁生命周期。有限Set和字符串status谓词、key字段结构、状态patch/guard来自实际AST。selected callback受保护不能说明整个facade串行；外部检查位置不能说明没有其它保护。find/push同路径不证明集合heap/方法效果，实际deps与物理资源仍可未知，状态patch不证明已执行转换。interleaving_inference=false，不求解交错、不证明锁/文件系统或一般并发正确性。

新增语义层semantic_sources/lexical_bindings只消费保存快照：核对原hash、文本/BOM、projection、完整call span和唯一声明，记录位置与parse身份。词法唯一、origin稳定、运行值、对象/资源身份分别表达；generator/未await async、default/写入、alias/escape和标准内建遮蔽均不能悄悄闭合。模型及policy声明、source-derived事实和unresolved分析分列，不按统一分数或红色节点替代判断。

## 共享语义与选定参数字段

`BuiltinEnvironment.audit` 仅审计当前保存且认证的文档，检查固定标准接口的词法遮蔽、显式/计算写入、host alias、prototype、eval/with、escape和预算。`supported_in_registered_model` 只启用注册语义模型，实际宿主和外部 effects 没有被认证；host alias 按声明身份追踪可见行为，不推断其实际对象值。标准模型、source事实、policy和unresolved barriers分栏保存。

共享completion层区分普通sync/async与generator/async_generator，普通sync调用也可能返回thenable。直接await、return-without-await和正常值关系不同。`normal_value_relation_closed`保留所选调用正常履约及return到达的控制前提；try/catch不隐藏，finally、未知默认RHS或特殊控制可拒绝封闭。body激活、全部完成、运行和资源生命周期不由该摘要证明，不能把返回Promise当成已经完成body或持锁至settlement。

顶层field_contracts支持TS/JS parameter_field_flow/all_direct_sites。subject为file/symbol/parameter_index/field_path，sink为call_argument或return，静态字段路径1..8键。必须注册ecmascript-own-enumerable-field-copy-v1并保留来源/审批和conditional，可独立追加ecmascript-own-data-read-v1。copy前提覆盖整个相关普通自有可枚举表面；Get的缺省undefined/不触发prototype/accessor/Proxy也需独立guard，不递归认证child。不能预填中间传播，例见 [当前CPB策略](../reports/astra-iteration9/codepatchbay-policy.json)。

有限摘要按保存AST读取声明/别名、同对象赋值、普通own-data rest及顺序spread、实际helper实参/形参与正常return。`sink.callee`仅是源码选择器，未通过SemanticSources.call_binding认证的动态/同名callee保持unknown；不按配置角色猜helper。选定字段来源封闭、整对象shape封闭、字段presence和运行值是不同结果。普通参数字段在提供值/普通自有数据属性条件下描述来源，不由已知声明推断已知值；新对象复制不等于同对象覆盖。

普通解构只读取/绑定源键，object_destructure_keys的pattern层copy_scope=none_at_pattern_level；实际rest才记录object_rest_copy与排除键/rest_binding_only浅复制。这一区分在当前finite-field-summaries-5-ir中保留，不把普通参数列表或赋值称为复制整个输入。

unknown后置spread/键、alias/escape/effect、未知prefix、unsupported控制、未await Promise/iterator、fallthrough及预算边界保持unknown，不将未知当空对象。每条有效合同都输出status uncertain的字段摘要Finding，逐site保存正向或unknown，另保留body返回表达式、abrupt边界、analysis_gaps及完整来源/组件身份。async的thenable/继承then同化未求解时不把body返回表达式当fulfilled值；effect样本截断不影响完整barriers判定。`selected_shape_complete`与`source_form_complete`不证明运行字段存在、最初参数值一直未变、消息运输或全部功能；多个规则不能相加成端到端字段链。

[独立字段来源稿](../reports/astra-iteration5/FIELD_SOURCE_REVIEW.md)只准备现场源码和原hash/AST：实际bridge是runJobWithServices，队列normalization为enqueue局部代码。buildServices的全部ports键须由源式读取后检查封闭own-data/effects，不能预填某预算键的缺失。queue helper两return/new-existing和metadata浅别名分别保留。稿中20项人工观察/60AST锚点不算自动field结果。v0.8最终正式字段评估保留3合同/5分支终点、全部unknown和75/35/16事实；所选字段shape/source-form完整位为false。依据见 [REPORT](../reports/astra-iteration5/REPORT.md)和 [保存查询](../reports/astra-iteration5/saved-query-observations.json)。

## 不可变状态与局部预算

当前公共semantic_ir（finite-immutable-semantic-ir-3）由字段AST适配器实际消费：allocation、当前ObjectVersion、copy-time ObservationRef、FieldSlot、shared referent、EffectRef和ModelGuard分离；allocate/bind/lookup/copy/write/reachable-effect/join返回不可变状态。复制固定源own-slot观察时点，共享child仍按allocation读取当前状态；未知捕获、alias、getter/proxy及未闭合effects保留barriers。旧mutable value/frame、clone与全局epoch判定已移除，但这不证明实际字段链闭合。

v0.10.1区分字面对象构造期间未暴露的parent、initialized const cell及有类型化BindingDomain的模块live cell。构造保护只限制fallback全heap扩大，真实root/alias/escape、反射或预算缺口照常生效，物化及bind/return/argument暴露前结束保护。const cell不可重绑不表示referent不变；callee、receiver、实参和实际捕获cell仍参与effects。原始值content未知不产生对象referent，TS类型语法不构成运行capture；复制观察、共享child及正常到达条件没有被省略。

v0.11 的 `source_relations` 是保存 AST 和词法身份的独立结构轴：实际参数/形参连接、const 别名、当前 body-return 引用、顺序对象构造及显式字段写入尝试可直接下钻。写入扫描限定所选函数源码前缀；无匹配只表示该范围的显式静态目标没有出现，动态键、不支持控制和嵌套 callable/class 均另记缺口，不推导无间接修改或所有路径到达。它不升级 IR selected projection、入口字段来源、运行值或 Promise 履约。

IR v3 的 `CopyBoundaryObservation` / `CopyRetentionWitness` 则提供局部条件结论：在实际 spread 时点，当前 copy-source 的所选普通自有可枚举 data 字段如果存在且复制正常完成，完整的后置固定键不覆盖它，尚未暴露的目标仍受构造 guard 保护且 checkpoint / effects 未显示损伤，copy-time 值或引用可保留到匿名 literal 终点。存在性、最初入口来源和 shared child 内容仍未知；见证不修复 FieldSlot/projection，不延伸到之后的别名/堆端点、callee 激活、async fulfilled 值或运输。已知缺键的 copy 不能用这个条件结论充当新增有效保留。

普通 Get 不再转发带 damage/barriers 的旧 slot provenance，缺键 undefined 同样需要封闭、无损伤读取。运行捕获排除被擦除 TS 类型子树，保留真正 RHS/闭包/默认值与隐式 arguments；absence 只扫描真实 binder，默认 RHS 引用不被误标为声明。未知效果仍可能损伤对象，不把 setter 或共享 metadata 子对象当无害。

v0.10.1正式三字段合同中，engine的真实runJob实参位置在normal-prefix及copy/Get模型下为source_form_preserved_when_present，selected-shape/source-form完整位true；presence仍unknown、whole argument shape仍false。services helper的十一自有键/封闭shape/maxRetries absent已由真实AST适配器恢复；queue/agent四位置仍unknown。source-form、presence、referent当前内容、body-return/fulfilled与完整reaching分别保存，局部来源保留不证明数值预算、激活或运输。v9/v10目标源码及policy字节/hash相同，见 [正式字段比较](../reports/astra-iteration8/FIELD_VERSION_COMPARISON.json)。

v0.11 正式结果保留该 engine 来源形式关系与 helper 十一键/缺键，queue/agent 四入口字段位置仍 unknown。41 条源码结构关系和 agent-config.ts:489 唯一的当前 copy 终点支持独立计数：后者只保留复制时的顶层 maxRetries 值/引用到匿名 literal 终点，没有证明入口 metadata 未变、presence 或 async fulfilled。见 [当前字段](../reports/astra-iteration9/field-assessments.json)、[结构与复制关系](../reports/astra-iteration9/field-relations.json)及 [版本比较](../reports/astra-iteration9/FIELD_VERSION_COMPARISON.json)。

v0.9顶层budget_contracts仅支持bounded_for_loop与counter_exhaustion_guard，evaluation=all_lexical_sites；subject={file,symbol}，counter/limit各为{kind:local_binding,name}，只定位唯一声明，不能填阈值、比较、更新或消费结论。必须注册captured-local-budget-source-v1并保留provenance和conditional条件。来源/比较/增量/helper原文由保存AST与实际CALLS提取，相关而不支持的候选保留unknown；嵌套函数激活另列。source_form_complete只限局部语法关系，数值域、实际次数、termination、全部支配与上游预算归属均未证明。

两种现有预算源码模式仍source_form_complete=true，finding uncertain；phase guard在嵌套async箭头中，四counter写不能当四次完成attempt，infra有限for header不能证明激活或termination。limit helper正常化原文不等于运行求值，提前return、注入callee和opaque范围保留。FailureRouter assignment attempt、phase/solver/completion/infra可以是不同预算；没有批准CLI意图时不要求统一，也不以rg缺同名字段作全程序未消费负证。当前结果见 [保存汇总](../reports/astra-iteration9/codepatchbay-summary.json)；历史 [预算来源准备](../reports/astra-iteration6/BUDGET_SOURCE_REVIEW.md)和 [v0.9预算](../reports/astra-iteration6/budget-assessments.json)保留。来源包24人工观察/89AST锚点独立计数，不当作自动预算结果。

## 存在、缺失与未知

确定边来自支持范围内能够绑定的调用目标。动态参数回调、反射、复杂对象方法、歧义导入及外部符号等关系可能保留为未解析或候选关系。

必需路径没有找到时，必须同时审阅相关未知关系。如果未知调用或未分析文件可能隐藏连接，结论应表达证据不足，不能直接定为确定缺失。配置端点没有匹配到节点时，也可能是拼写错误、源码改名、扫描范围或解析问题。

发现状态中的 `open` 表示当前证据支持的规则违反或结构发现，`uncertain` 表示不确定。它们都不是最终人工裁决。图的完整性声明只覆盖当前语言、源码范围和解析能力，不代表运行时完整图。

首版采用“显式调用模型”：只遍历当前快照中确定绑定到内部符号的显式调用。普通外部调用作为终点，外部库回调、框架运行时注册行为、运算符触发的特殊方法及其他隐式调用不属于完整性承诺。即使查询标记模型内完整，也不能据此断言目标语言的全部运行关系均已覆盖。

如果分析器从外部调用元数据中明确识别到回调边界，缺失路径可因该边界标为不确定；系统不推断外部实现实际会调用哪个内部函数。

路径查询 `status` 为 `found`、`not_found` 或 `unknown`。`found` 带确定静态路径；`not_found` 只表示支持的显式调用模型内未找到连接；`unknown` 表示端点歧义或分析缺口可能影响结论。结果的完整性说明必须与状态一起阅读。

未知关系不能用于伪造确定路径。候选目标可以帮助下钻，但没有足够解析依据时，不能选择一个“看起来正确”的候选来消除发现。

禁止规则中，一条确定的禁止调用就是结构证据；没有找到禁止调用不能证明所有动态关系都符合规则。已确认的真实调用仍然可用，其他未知关系不会抹除它。

## 路径与调用环

查询通常返回一条最短的确定路径。查询同一节点到自身可以返回零边路径，但会明确提示这不是递归证据；调用规则仍采用正长度路径。查询避免枚举指数数量的所有路径，也不宣称可替代执行观察。函数节点内的顺序、分支条件和参数不在普通调用图中完整表达。

例如，图中同时有 `submit → validate` 与 `submit → persist`，并不能判断校验是否发生在保存之前，是否只有错误分支才校验，或保存了什么数据。

SCC 或自调用说明存在循环结构。递归可能有终止条件，互相调用可能是合理协议。调用环不能自动等价为不终止或业务错误；若项目禁止这种结构，应由显式规则或人工意图支持判断。

## 源码覆盖与故障

分析器可能因语法错误、读取权限、文件大小、语言或解析能力无法完成部分分析。诊断、文件状态和快照状态应保留这些原因，不能将相关区域显示为已验证。

默认配置只请求 Python；显式配置可以请求 TypeScript/JS-family 与 Rust。语言前端消费同一批安全捕获的源码文本，不重新读取不同工作区版本。缺少 Tree-sitter 工具依赖、语法库失败或不支持的源码仍需保留诊断。安装工具语法库不意味着安装或执行目标项目。

`stats.by_language` 统计各请求语言的选入文件、完整解析文件、未完整解析文件及调用解析状态。TypeScript 项包含其 JS/JSX/MJS/CJS/MTS/CTS 输入；未请求或未支持的语言另在 `unsupported_files` 说明。语法成功与调用绑定完整是两个维度，任一覆盖或解析缺口都可能使快照为 `partial`。

TypeScript 接口、复杂接收者方法、回调及 JSX 运行机制，Rust 一般泛型/trait/复杂实例分派、宏展开和实际活动 `cfg`，以及跨语言通信，均不能因目标名字相同而绑定到某个唯一实现。条件声明和测试模块标记不代表该代码在生产构建中活动。

### Rust 具体 Self 的有限绑定

当前 `rust-tree-sitter-1.7-generic-lexical` 继承v0.4的有限Self机制：在唯一、完整解析的非泛型具体impl中解析直接self.method()/Self::method；须排除目标和成员冲突。具体trait impl体可调用固有目标，不等于一般trait分派已解决。

一般接收者或目标的泛型/where、类型别名、cfg、未知属性宏、重复定义、多个模块上下文、解析失败、Deref/DerefMut 或同名 trait 成员均可使关系继续未知。`self.field.method()`、其他变量/表达式接收者、显式包装的 self 和 dyn/trait 目标不靠全局方法名字确定绑定；闭包/Future 的激活仍不证明。普通 trait 目标保持未知。

未 override 的 trait 默认成员也进入冲突分析。trait 声明缺失或部分解析时，对已知 receiver type 保留默认成员未知；receiver 本身无法确定时保守降级相关全局方法绑定。别名 Deref、reference/blanket trait 成员及借用/所有权形状不匹配不猜测方法调整顺序，这些限制也影响 `Type::static` 路径。因此语言机制存在不保证真实仓库里某个 Self 调用已经变成确定；应查看该快照的实际 reason 和见证。

确定边保存 receiver 类型、类型/impl/参数声明位置、目标声明与 impl 位置及 `binding_basis`。trait 实现节点保留 `<Type as Trait>.method` 的实现身份，基准可以用文件内 Type.method 选择器寻找该实现，多个候选时仍歧义；不把不同 trait 实现合并为一个符号。

显式analysis.rust_helper_profiles中的serde-1.0.228-declared-helper-v1使用捕获Cargo声明/精确锁checksum和完整名字环境，移除配对helper属性的opaque；analysis.rust_interface_models中的rust-core-cmp-eq-interface-v1独立注册，默认均不启用。受限receiver接口包括Deserialize默认deserialize_in_place、Eq的eq/ne/assert_receiver_is_total_eq冲突；无生成固有/Deref属于可信模型假设。名称遮蔽、别名patch、错hash、cfg/generic及其它未知宏等拒绝适用。未实际展开宏、未捕获实际标准库、未验证项目工具链，生成正文仍unknown。受影响边和基准binding_models保留模型前提，不省略后宣传纯源码或运行证明。

v0.6 的 `rust-generic-same-impl-lexical-v1` 是另一有限关系：源/目标在同一个泛型固有 impl 的确切 AST 身份内，且调用为直接 `self.method()` 或 `Self::static_method()`。唯一捕获声明、完整可见作用域、成员竞争、接收者形状及实参数量均须满足模型；额外方法泛型/where/impl Trait/参数属性、turbofish、cfg/opaque/可见宏，以及不明 trait/default/Deref/derive 竞争会拒绝。它不跨 impl 猜目标，不绑定 `self.codex.ensure_thread` 这类字段接收者。

`Edge.metadata.generic_impl_binding` 保存 model_id、impl 文件/原文hash/header/字节范围、源/目标声明和参数计数。泛型实例化、bounds、实参类型、执行、完整编译器命名空间和宏展开未验证，剩余边界不得省略。基准1.3仅摘要这些保存字段，不把同impl词法连接解释为泛型编译或功能证明。

### TypeScript 派生语法与原始证据

v0.4 的 `ts-syntax-projection-1` 仅适配固定语法库的有限缺口，不是完整 TypeScript 语法或类型检查器：

| 可适配情况 | 必须具备的证据 | 不包含的情况 |
| --- | --- | --- |
| qualified import 类型头，如 `import('./page.js').PageOptions` | CST 与源码确认处于类型注解、类型别名或 interface 上下文 | 运行时 import、未知表达式、所有可能的 import 类型变体 |
| 类型对象内 `abstract?:` 属性 | 类型上下文、原始错误区间及派生 property signature 对应 | 任意保留字全局替换、运行时对象重写 |
| 字面量原文中的实际 NUL | 静态扫描确认 quoted literal 或 template raw 区域，并由派生 CST 再确认 | 普通代码、模板插值代码、regex 内 NUL；JSX 字面量不使用此代码 lexer 适配 |

派生解析缓冲区以等宽替换并保留 CR/LF 位置；位置的恒等映射针对保存文本的 UTF-8 表示。原 `SourceFile.content`、原文件哈希及源码下钻不改写；原文件字节哈希与该文本 UTF-8 哈希分别记录，不能混淆 BOM/编码差异。字符串值、名称和证据均从原文读取，不求值派生字面量。

模块节点的 `metadata.syntax_projection` 保存改写范围、原/派生文本及哈希、原始/派生 parser errors、采用或拒绝状态和位置映射。适配后的节点/边通过 `source_projection_node`、`source_parse_mode` 和 `syntax_projection_version` 关联来源。原 parser 的错误仍有诊断和统计，不因适配而从账本消失。剩余未知语法、重叠/不等宽改写、范围不能确认或派生 CST 校验失败继续保留解析失败/部分分析；不能吞掉 ERROR 后宣称语义完整。

`entrypoints` 是项目声明的入口集合，系统可将与这些入口没有确定连接的函数标为疑似不可达，但保持不确定状态，不直接推出死代码。公共接口、框架入口和动态插件可能没有普通调用者。

依赖源代码不在扫描范围内时，外部调用不能靠 API 名称知识库认定存在或不存在。首版不安装依赖、不查询运行环境、不调用类型检查器；目标仓库根目录下的源码范围决定可见实现。

analysis.support_inputs只读取显式项目内相对路径的Cargo/协议原文，存schema 2的input_evidence，字节hash、UTF8文本hash、内容、状态进入输入/cache身份。失败不memo，同路径代码/辅助身份冲突拒绝发布。辅助原文不成为实现节点或新增代码解析成功；旧快照没有记录就不能用当前FS补。基准1.3仍只准它核对evidence_only，不能补正向caller、unknown调用或跨语言CALLS。

## 版本及人工处置

所有源码证据绑定快照。查看旧发现时读取旧快照保存的源码，不能拿当前工作区文件作为旧证据。符号重命名可能展示为删除与新增，系统不自动判断它是否为同一历史实体。

当前快照是扫描读到的文本集合，不是工作区的原子快照，也不自动绑定 Git commit。扫描过程中同时编辑源码可能改变采集输入；需要固定版本判断时，应先稳定源码范围。

差异报告中的发现消失或 `resolved` 只表示新快照未再报告，不代表已经修复。规则、源码范围、分析器、检测器、模式或语言组件版本变化均可能改变结果，必须同时阅读比较兼容性信息。`parser_version` 保存各前端、Tree-sitter/语法库及宿主版本的规范组合，`stats.component_versions` 提供结构化明细；不同组件版本属于不同分析输入。跨项目比较也不能当成同一项目的历史轨迹。

人工处置支持：

- `accept_risk`：接受已知结构风险或项目例外，保留原因和范围。
- `false_positive`：记录维护者认为证据或规则适用有误。
- `fix_planned`：记录修复计划。

处置不改变原始发现的严重度，不删除原始证据，不使未经重新分析的代码变成“已修复”。有效期记录也不证明结构在到期前保持不变。

## 冻结观察与工具能力

`baseline` 命令只对照保存快照和独立观察数据，核对原文件哈希、源码引用及调用位置，不读取当前目标目录。原文件变化、文件未选入、端点缺失/歧义、关系不匹配、具体调用点未知与仅有证据的观察分别呈现；它不是测试、规则门禁或人工结论自动化。

Astra v1 的 26 项包括 9 项直接调用、1 项路径、3 项 `unknown_required` 与 13 项 `evidence_only`。`unknown_required` 要求原调用位置保留 dynamic/unresolved/ambiguous、没有确定 target 且有明确原因；源节点缺失、dangling resolved或其他文件有诊断不算满足。`evidence_only` 涉及组合、协议、字段、状态或原子条件，当前图不能裁决。五项人工分析结论属于后者；记录其证据不等于工具自动发现五项问题。协议和反证见 [BASELINE_CONTRACT.md](../reports/astra-baseline/BASELINE_CONTRACT.md)。

独立来源稿不改上述26项。[参数稿](../reports/astra-iteration3/PARAMETER_EVIDENCE.md)中的worker常量3是独立构造；[导航稿](../reports/astra-iteration3/NAVIGATION_EVIDENCE.md)纠正scopeHash保留已有query；[原子稿](../reports/astra-iteration3/ATOMICITY_EVIDENCE.md)区分两种锁寿命。v0.7已自动生成有限query/callback链及selected保护/谓词摘要，完整参数运输、真实路由/事件、实际deps/集合heap/物理资源、权威不变量和交错仍未闭合，来源整理不算自动成果。

v0.11 历史实现追踪采用原 [五项判断合同](../reports/astra-iteration4/GOAL_ACCEPTANCE.md)和 [该轮30义务账本](../reports/astra-iteration9/goal-ledger.json)。当时10有限Finding不是10个业务bug，五claim仍partial、完整0/5；账本为人工映射正式证据，类别为4限定支持/20partial/6unknown。该历史类别不锁定v0.12固定注册器的结果，也不构成全文报告分母；缺分析仍不能假设成立。

## 系统明确不提供的能力

不运行单元、集成或 E2E 测试，不执行目标函数，不导入目标模块，不启动应用，不触发构建，不提供沙箱、运行 trace 或执行差分。没有用于这些目的的 API 或 MCP 工具。

不证明业务正确性、类型安全、数据流正确性、异常处理完整性、运行可达性、一般终止性、所有依赖 API 有效性或全代码功能正确性。LLM 没有参与当前检测结论；如果以后增加解释，解释仍需与静态事实区分。

代码由 AI 编写还是人工编写不改变这些判定标准。系统分析结构及其依据，不推断作者来源。
