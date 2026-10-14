# 静态能力路线与独立观察

依据：[Astra CodePatchBay v1](../reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md)、[WinWinCode v1](../reports/astra-baseline/WINWINCODE_ANALYSIS.md) 和 [26 项冻结观察](../reports/astra-baseline/capability-baseline.json)。这些报告和基准保持冻结；后续工具结果另存，不改原观察来迁就实现。

本路线以支持范围内功能闭环和正确判断优先，可扩展性其次，性能最后。当前实现为 v0.14.0，scope2 的[核心与策略已冻结](../reports/astra-iteration12-scope2/CORE_FREEZE.json)，两库正常纯静态冷/热分析及正式报告已完成并关闭数据库。[原已读有限源码内容正式读回](../reports/astra-iteration12-scope2/ORIGINAL_REPORT_COMPLETION.md)已完成，complete=true、已知有限内容缺口为空；v0.13 正式结果保留在下方历史记录。固定范围仍是原两份完整分析报告中的有限内容，不设置重复 Astra 审批，也不把五项/30 义务追踪当成全文分母。

## v0.14 已实现内容与正式结果状态

本轮承接 [v0.13 范围差距](../reports/astra-iteration11/REPORT_SCOPE_GAPS.md)中的职责解释与文档部署对照，同时补原 CPB 事件/交付段落的条件式状态沿袭和发布边界。实现已进入固定分析和正常报告路径，不以新字段或规则数量宣布全文目标完成。

| 本轮能力 | 已实现的源码关系 | 正式状态与边界 |
| --- | --- | --- |
| 字段、状态与条件 | 真实 guard、事件字面字段、event/queue 的同源 job 字段、模式/布尔 opt-in 分区、选项到 callee return guard 的绑定 | 所选有限关系已保存在正式报告。局部状态、嵌套 catch、未知 spread/成员及提前返回分开；不证明必然入队、授权结果或远端成功 |
| 职责解释 | 实际记录/字段/绑定操作、已认证调用实参交接、拒绝 guard、return 与正常源码顺序，生成声明级说明、交接和通信边界 | 正式保存 CPB 15,223、WWC 10,023 个操作，共享引用检查失败均为 0。目录/业务标签只导航，partial ownership、opaque effect、回调激活与全部写者范围继续保留 |
| 文档部署对照 | 捕获文档的限定条款与所选生产装配、Device provider、凭据字节材料、Worker 本地消费和 transport 分支对照 | WWC 正式报告已保存文档比较。保留 Control Plane 内部范围，区分材料/引用/长期性，不把本地分支写成协议绕过或安全缺陷 |
| 正常报告 v3 | Markdown/JSON 展示实际解释、条件表、反证和 source-only 边界，ID/Pointer 回指完整证据；报告组件与快照分析身份分开 | 两库正式报告及摘要已保存，数据库已关闭。展示数量和条目导航不产生新判断，不改旧快照或原报告 |

当前身份为 `static-multilang-14` / `call-rules-13-architecture-explanations`、快照 schema 2。正常流程仍是只读捕获、前端分析、全量检测、原子发布，再从保存证据生成报告。冻结记录选择 `full` 引擎，冷/热两轮均重算，不把第二轮叫作前端缓存复用，也不发布未经核对的性能收益。

本轮正式结果来自 [v0.14 scope2 目录](../reports/astra-iteration12-scope2/)：CPB 保存三项条件判断/18 必要关系、16 条所选支持链，WWC 保存两项/12 必要关系、20 条所选支持链；[原 26 观察比较](../reports/astra-iteration12-scope2/ORIGINAL_BASELINE_COMPARISON.json)保持 10 reproduced/3 unknown/13 evidence_only、changes=[]，[发布身份](../reports/astra-iteration12-scope2/PUBLICATION_IDENTITY.json)verified=true，65 份核心与冻结身份一致。iteration12 首候选和开发查询不替代这些正式结果。原 14 行、十领域和文档三方面已由[正式原内容读回](../reports/astra-iteration12-scope2/ORIGINAL_REPORT_COMPLETION.md)按实际正文及来源承接，mode=formal、complete=true、remaining_known_original_source_content_gaps=[]；不由所选链/操作数量推定，也不追加唯一权威、全授权、全协议、任意 heap/并发或原明确未审领域作为新验收门。

条件判断、所选关系、源操作数、有限表行数、解析比例和目录条目数均不是功能覆盖率。本轮完成的是原已读有限源码报告内容，依据为实际解释、条件、反证及来源对照；原未审领域、全程序功能、运行成功或超越全部原文内容均未据此证明。系统仍不执行目标、测试、构建或沙箱，不新增 Astra 复审。

## v0.13 历史正式范围与当时差距

该版沿 [v0.12 全文范围差距](../reports/astra-iteration10/REPORT_SCOPE_GAPS.md)补原报告已读段落的有限关系。正式 [CPB 报告](../reports/astra-iteration11/codepatchbay-automatic-report.md)和 [WWC 报告](../reports/astra-iteration11/winwincode-automatic-report.md)分别保存 13 条和 18 条 `scoped_source_relations_supported` 关系；[正式账本](../reports/astra-iteration11/goal-ledger.json)保存五项 `scoped_static_judgment_reproduced`、30 关系 supported、未闭关系为空，五项 complete/full 支持且必要缺口为空；[证据文件](../reports/astra-iteration11/GOAL_JUDGMENT_EVIDENCE.json)关联 704 个真实引用。既有规则、五项判断和 31 条来源条目均没有改成全文分母。新核心和策略见 [冻结身份](../reports/astra-iteration11/CORE_FREEZE.json)与 [策略扩展](../reports/astra-iteration11/POLICY_EXTENSION.json)。

| 已实现的有限扩展 | 实际承接与保留范围 |
| --- | --- |
| 条件门与响应字段 | readiness→提前返回→enqueue、completion checklist/mutating/豁免、access-audit→拒绝响应。关联真实 guard、返回对象与 writer 实参；不把 job best-effort audit 和 access audit 合并 |
| WorkRun 表与 Rust 来源上下文 | runnable/依赖/活动排除/选中身份再次检查；crate-root 内建编译限制属性的严格分类。原三个 partial 的有限来源在新版正式结果中支持，保留未解析宏、trait、泛型和实际部署条件 |
| 消息、codec 与记录投影 | Chat 请求尝试、Worker/adapter 独立身份、outbox/ack 参数位置，以及 event→index/rebuild、可信命令中间来源和失败 record 保留。保存实际声明/字段接缝，不以字段同名或调用邻接替代传递 |
| 浏览器生命周期 | generation/null context/abort/closed guard、挂起后新鲜性与关闭结果补偿。局部来源关系与所有 callback/资源安全分开 |
| 有限写者职责 | 捕获字段写者、同 token 消费者和拒绝 guard。状态保持 partial；堆别名、全部写者、规范权威与所有授权仍未闭合 |
| 报告展示 v2 | 保存关系索引、有限表、条件与边界、写者引用，均为 presentation-only；原 Finding/Evidence 与完整 pattern 不改写 |

正式 [CPB 扫描记录](../reports/astra-iteration11/codepatchbay-integration.json)和 [WWC 扫描记录](../reports/astra-iteration11/winwincode-integration.json)保存冷/热同 ID 与 created=true/false。两库 source hash 与各自 v0.12 相同，解析仍为 330/333 与 465/471。[原 26 观察比较](../reports/astra-iteration11/ORIGINAL_BASELINE_COMPARISON.json)保持 10 reproduced/3 unknown/13 evidence_only、两库 changes=[]，36 份保存/现场 hash 及目标 commit 匹配；[发布身份](../reports/astra-iteration11/PUBLICATION_IDENTITY.json)verified=true，共享组件和 60 份 live/archive 核心一致。正式发布采用 full 引擎、两轮均重算；与 v0.12 的 CocoIndex 维护方式不同，不能把引擎变化当纯精度提升或缓存性能对比。

v0.13 当时的剩余优先项来自原全文两类内容：把捕获写者/消费者组织为职责解释；将文档中 Device/Credential 声明与实际部署分支做来源对照，区分适用范围。该版尚未自动汇总，见 [v0.13 范围差距](../reports/astra-iteration11/REPORT_SCOPE_GAPS.md)。这两类已由 v0.14 实现继续承接，正式结果状态见上文；不扩成唯一权威、全部权限、全协议、任意 heap/并发和原明确未审领域的新验收目标。

[报告 CLI 正常读回](../reports/astra-iteration11/CLI_REPORT_READBACK.json)确认 WWC 导出与正式 Markdown 字节/hash 一致、数据库逻辑/schema/身份保持且未重扫；[全文条目导航](../reports/astra-iteration11/REPORT_ALIGNMENT_RESULTS.json)只关联真实保存证据，不重新评级原报告。

五项/30 必要关系、31 条配置、有限状态表行数、facts 数和解析率均不是功能覆盖率。该版不能宣称已自动复现或超过原两份全文报告，也不添加目标执行、测试、构建、沙箱或 Astra 复审门。

## v0.12 历史正式能力与扩展依据

正式 [CodePatchBay摘要](../reports/astra-iteration10/codepatchbay-analysis-summary.md)和 [WinWinCode摘要](../reports/astra-iteration10/winwincode-analysis-summary.md)保存五判断全部complete/full支持、30义务全部supported：CPB3项/18义务，WWC2项/12义务。源码链CPB6支持；WWC9支持与3partial，三项为provider部署、Worker入口和生产构造，18条链均保存结构支持但不全称分派闭合。条件、反证、已有支持链的外部/iterator/macro gap与完整JSON指针全部保留。

解析330/333与465/471、辅助输入2与11、两图均partial；这与完整条件判断状态分开。新增policy、模型和辅助原文的范围变化独立记录，不能将五项完成率或15条链关系支持计成全文覆盖率。

完整自动报告见 [CPB](../reports/astra-iteration10/codepatchbay-automatic-report.md)和 [WWC](../reports/astra-iteration10/winwincode-automatic-report.md)。原26项冻结观察保持10 reproduced/3 unknown/13 evidence_only，与v0.11 changes=[]，36份保存/现场原文身份matched；[发布身份](../reports/astra-iteration10/PUBLICATION_IDENTITY.json)verified=true，54份核心与存档一致。原观察、五项/30义务及全文范围分列，不合计成覆盖率。

该版发布说明见 [v0.12正式报告](../reports/astra-iteration10/REPORT.md)。正式实现追踪见 [五判断/30义务账本](../reports/astra-iteration10/goal-ledger.json)及 [保存判断证据](../reports/astra-iteration10/GOAL_JUDGMENT_EVIDENCE.json)；[全文条目导航](../reports/astra-iteration10/REPORT_ALIGNMENT_RESULTS.json)仅关联原条目和证据，不生成全文评分。 原主链尚未闭合的内容及原明确未审范围见 [范围差距](../reports/astra-iteration10/REPORT_SCOPE_GAPS.md)。

固定注册层接入status、pipeline、navigation、device和atomicity五种完整条件判断；逐项认证真实源关系、必要义务、模型适用性、来源身份和预算。源码链层另用八类通用模式生成主链、前置guard、正常顺序、命令来源、失败分支、结果持久化/reconcile、agent执行策略和worker/provider分流。标准模型、policy和源码事实分开，局部支持不代替完整判断。

自动项目报告从保存证据生成架构结构、捕获声明、完整判断、主要链、反证和缺口；重叠源选择独立呈现。CLI/HTTP/MCP共用报告，不读取原报告文字充当结果。机制见 [自动项目报告](AUTOMATED_REPORTS.md)，全文对齐范围见 [原报告对齐说明](../reports/astra-iteration10/REPORT_ALIGNMENT_NOTES.md)及 [条目目录](../reports/astra-iteration10/REPORT_ALIGNMENT_CATALOG.json)。该版报告保留whole_report_reproduction_claimed=false。

后续先按全文条目的未闭合功能域补真实证据和反证，再扩独立样本、框架与语言范围；通用heap/effects、全部动态分派与任意并发不因有限模型而完成。source selector、必要关系、标准语义和运行适用性必须分清；新增模型不能把必要未知作为可忽略条件。模型/策略变化与实现精化分别比较。

## v0.5 至 v0.11 历史结果与当时路线

v0.11 将字段源码结构与当前copy终点见证作为独立轴；它们不修复入口来源，也不把局部复制当成完整字段链。以下统计、缺段及优先级表保存当时证据，不作为v0.12正式结果。

截至v0.5的历史确定关系历程为5→7→9/10；该轮新增2项WorkRun依赖显式serde helper与Eq接口模型，不是宏展开/实际工具链证明。3/3指定未知保持，全部26项为9 reproduced、4 unknown、13 evidence_only；辅助协议原文仅补来源，未生成跨语言调用。CPB330/333解析、23380绑定；WWC465/471解析、15799绑定、4辅助捕获，均partial。正式依据见 [REPORT](../reports/astra-iteration2/REPORT.md) 与 [Astra复核](../reports/astra-iteration2/INDEPENDENT_REVIEW.md)，冻结报告不变。

v0.6的正式正向观察为10/10，历程5→7→9→10；新增Worker同泛型impl关系依赖捕获作用域及有限约束，实例化/bounds/实参类型/完整编译器命名空间/宏展开未验证。3/3指定未知保留，26项为10 reproduced、3 unknown、13 evidence_only。CPB330/333解析、23380绑定；WWC465/471解析、16293绑定、4辅助捕获；两库partial、冷热同ID且热轮不重复发布，检测每轮全量。本轮额外3条配置式合同发现保留之前2条，并新增参数来源形式uncertain，不代表3个业务bug或功能覆盖。依据见 [第三轮REPORT](../reports/astra-iteration3/REPORT.md)、[Astra复核](../reports/astra-iteration3/INDEPENDENT_REVIEW.md)、[完整账本](../reports/astra-iteration3/capability-ledger.json)和 [合同见证](../reports/astra-iteration3/finite-contract-witnesses.json)。

v0.7正式两库图/解析/绑定统计与v0.6相同，均partial；冷热同ID、热轮不重复发布、检测全量。原26项仍10/3/13，36份冻结来源匹配。导航新增82来源关系/8声明/4调用，有限port装配23事实及五段支持、10gap保留；原子15声明/12调用及3gap。共5配置式有限发现，未裁定五业务bug。依据见 [第四轮REPORT](../reports/astra-iteration4/REPORT.md)、[Astra复核](../reports/astra-iteration4/INDEPENDENT_REVIEW.md)与 [五有限见证](../reports/astra-iteration4/finite-contract-witnesses.json)。

v0.8最终CPB330/333解析、23,380绑定；WWC465/471解析、16,293绑定和4辅助输入，两库仍partial、最终冷/热同ID且热不重复发布，检测full。原26项保持10/3/13、36来源匹配且changes为空。三字段合同五分支/终点评估全unknown，事实75/35/16；8条有限发现不是8个bug，完整义务类别仍4限定支持/19partial/7unknown。依据见 [第五轮REPORT](../reports/astra-iteration5/REPORT.md)、[字段评估](../reports/astra-iteration5/field-assessments.json)及 [保存查询](../reports/astra-iteration5/saved-query-observations.json)。

v0.9最终双库冷/热扫描已完成：CPB330/333解析、23,380绑定；WWC465/471解析、16,293绑定及4辅助输入，两库仍partial，热轮同ID且created=false，检测full。原26项仍10 reproduced/3 unknown/13 evidence_only，36来源匹配、changes=[]。新IR字段三合同五位置全unknown，事实208/163/503；services helper own-shape退unknown，组件11键/absent观察不能补正式结果。两预算源码模式source_form_complete=true，numeric/runtime/termination/domination仍false；共10条有限发现不是10个bug。五目标仍partial，30义务为4限定支持/20partial/6unknown，仅P5新增局部预算来源partial。 见 [第六轮REPORT](../reports/astra-iteration6/REPORT.md)、[字段](../reports/astra-iteration6/field-assessments.json)、[预算](../reports/astra-iteration6/budget-assessments.json)与 [保存查询](../reports/astra-iteration6/saved-query-observations.json)。

v0.10.1两库目标源码及policy字节/hash与v0.9相同，图/解析统计、冻结观察10/3/13、36来源匹配和冷/热一致性保持。局部P4证据改善没有改变原30义务类别：4限定支持/20partial/6unknown。实际结果见 [第八轮报告](../reports/astra-iteration8/REPORT.md)、[正式字段](../reports/astra-iteration8/field-assessments.json)及 [版本比较](../reports/astra-iteration8/FIELD_VERSION_COMPARISON.json)。site数量不是功能覆盖率。

v0.11 正式五个字段site保存41条独立源码结构关系和一个条件式当前copy终点支持，位置为agent-config.ts:489。engine原来源形式及helper十一键/maxRetries absent保持，queue/agent四入口字段结果仍unknown；实际字段前提和新关系分别记录，没有将body-return提升为fulfilled或消息运输。原26项仍10 reproduced/3 unknown/13 evidence_only，与v10分类changes=[]。两库冷/热同ID、热轮不重复发布、语言memo复用且检测full，36来源全部匹配；原五完整目标0/5、30义务4限定支持/20partial/6unknown保持。见 [第九轮报告](../reports/astra-iteration9/REPORT.md)、[当前字段](../reports/astra-iteration9/field-assessments.json)及 [独立结构与复制关系](../reports/astra-iteration9/field-relations.json)。

v0.11 当时的五项实现追踪采用原 [判断合同](../reports/astra-iteration4/GOAL_ACCEPTANCE.md)及 [该轮30义务账本](../reports/astra-iteration9/goal-ledger.json)，不是10/10调用验收，更不是全文报告分母。五claim当时仍partial，必要缺段如下：

| 原完整判断 | v0.11 自动局部支持 | v0.11 尚未闭合 |
| --- | --- | --- |
| CPB retries | 两处独立参数形式、engine正常前缀conditional字段来源保留、services helper封闭shape/缺键及两局部预算模式；另四field位置unknown | normalize入口来源、setter/共享child和Promise边界闭合、new-existing/scheduler/assignment/JSON/inbox/broker对应运输、bridge装配与转交、有效预算消费及条件 |
| CPB superseded | 初始化成员差 | 状态生产/投影、job身份、terminal谓词、recover guard及event-store保护反证 |
| CPB同键窗口 | selected保护生命周期及外内symbolic谓词/键字段差 | 实际deps、物理资源/集合heap、全写者、guard状态可达及模型推导交错 |
| WWC导航 | query domain、具体callback null/direct-await拒绝链、五有限装配段 | 可见DOM入口、正常route/event激活、opaque前缀/其它port effects、VM plain对象与ambient接缝 |
| WWC Device字段 | 封闭spec对象缺字段及consumer guard出处 | UI/client实际装配、消息/协议版本和camel-snake映射、Rust dispatcher/authority、Device非空guard和反证 |

| 优先级与依赖 | 能力 | 原始样本 | 有限结论与所需证据 |
| --- | --- | --- | --- |
| 已有限实现 v0.5 | 声明初始化字符串集合equal、直接返回字面对象必需键 | CPB终态初始化差异；WWC spec字段构造 | 明确配置与来源；spread/别名/未知结构保留未知，conditional永远uncertain。不是全部状态/字段语义或2个业务bug确诊。 |
| 已有限实现 v0.6 | 调用参数的表达式和const词法来源形式；同一泛型固有impl内直接self/Self关系 | CPB独立worker预算构造；WorkerMain同impl方法 | 实际新增1条参数形式uncertain，producer parsed.retries匹配、consumer literal3形式不同；callee/transport/value_equivalence仍未知。Rust指定词法关系重现；均不证明运行值、运输或泛型编译。 |
| 已有限实现 v0.7 | 共享原文/词法身份、有限query/callback/装配、selected保护/谓词摘要 | WWC导航；CPB权威去重 | 源码、模型、policy和gaps分开；不伪造CALLS、实际deps或交错，不把有限assembly当端到端。 |
| 已有限实现 v0.8 | 共享builtin环境、有限completion和selected parameter field摘要 | 两个CPB opts/rest/services与metadata helper片段；导航/port/原子共享迁移 | 三合同五路径全unknown，事实75/35/16保存；局部rest/own keys/actual helper来源增加，完整P3/P4仍partial。不认证实际宿主、全部completion/激活/资源寿命、运行值或消息运输；源码准备不是分析结果。 |
| 已有限实现 v0.9 | 公共不可变IR及字段适配器迁移；两局部预算源码模式 | engine rest/queue metadata/helper returns；phase与infra预算 | allocation/版本/copy观察/child/effect/guard分开，旧mutable frame/epoch已移除；真实五字段全unknown，预算仅局部源码true。协议接线不是精度或完整判断通过。 |
| 已有限实现 v0.10.1 | 构造寿命、const/live cell域、callee/capture effects与真实字段精度修复 | services ownshape及runJob实参 | 正式helper十一键/封闭shape/maxRetries absent恢复；normal-prefix下来源形式保留，field presence仍unknown/whole argument shape false。与v9同源码/策略；不是激活、数值预算或运输证明。 |
| 已有限实现 v0.11 | 独立字段 source-relations 与当前 copy 的匿名 literal 终点见证；Get 和 lexical absence 精度防线 | queue normalization / shared metadata；agent 当前返回引用及 spread 后固定键 | 保存实际参数/形参、alias、body-return、ordered Set 尝试及范围负扫；copy-time 自有字段存在且正常复制、固定后缀不覆盖、构造与 effects 检查成立时保留到终点。不得升级 entry-origin、presence、shared child、async fulfilled 或运输。 |
| P0，先于扩大消息与预算 | 闭合剩余IR字段来源与helper/return/effect摘要 | queue metadata与agent两个return、opaque helper/shared child/Promise | 四site继续unknown；按实际Get来源、copy surface、captured cell及completion边界逐段闭合，未知捕获/全局/alias仍保守。通用跨文档effect、全heap与完整值链仍未实现。 |
| P1，先于完整字段链 | 条件化对象工厂、端口注入与组合摘要 | CPB buildServices/ctx；WWC auth/task port 与 WorkerMain | 保存实际组合点、返回对象成员、receiver 类型、分支候选与剩余未知；调用者可重新注入时不全局猜唯一实现。有限field helper摘要不等于全部生产装配已解析。 |
| P1，先于跨语言字段分析 | 协议、持久消息与进程关系 | queue→assignment→inbox→worker→bridge；client→Rust dispatcher | 独立关系记录 schema/version、command、channel、sender/receiver、request/job/scope 身份、条件和源码；禁止虚构跨进程普通调用边。 |
| P2，基于上述组合及协议 | 一般字段来源、覆盖、默认与消费者 | pipeline `--retries`；delivery URL；`verificationCommand` | 跟踪构造、映射、spread、重建、默认覆盖、具体消费者及条件必填 guard。有限表达式比较不替代此能力；只有证明对象身份和顺序后才标覆盖。字段同名、optional类型或一条调用路径不证明传递完整。 |
| P2，基于状态赋值与消费 | 枚举集合和跨层谓词一致性 | CPB `superseded`、completed 与 published | 关联状态赋值、集合成员、消费者条件与层级；terminal、recoverable、published 是不同概念，不自动合并业务策略。 |
| P2，基于控制流和权威写入 | 支配关系、持久顺序与原子边界 | readiness→enqueue；intent→persist→Kernel；same-key 去重 | 标注 early return、支配条件、事务/锁范围、原子约束与 receipt/outbox 关系。需要明确资源身份和锁合同；未来交错须由模型计算并保留前提，不能预填场景冒充发现。当前不证明一般并发正确性。 |
| P3，在语义稳定后 | 扩大语言/框架范围、性能和展示 | 冻结样本的持续追踪及新增独立样本 | 输入身份、范围和未知不能因优化变化；图更大或更快不是功能成熟度证明。 |

新增关系必须绑定分析快照、原始源码哈希与位置、工具组件版本、成立条件、来源和不确定性。确定调用、组合候选、协议关系、字段流、状态事实分别表达；现有图索引的确定邻接不能替代后四类分析。

共享环境只认可有限注册模型和保存文档审计；Object.assign appearance不认证pure、receiver/argument effects或复制。公共不可变 IR 已有真实字段消费者；v0.11 把源码结构、当前复制终点与入口字段来源分开，普通 Get 不将受损旧 slot 来源洗为正向。下一步闭合 queue/agent 的 setter/共享 child、可达效果及 helper/return/Promise 边界，再连接消息、记录身份和所选有效预算归属。模型/策略前提变化与实现精化分列，不以事实或模块数量替代完整义务。

字段与状态检查保留初始化集合、封闭对象键、参数来源形式、selected字段与局部预算数据合同。当前来源为独立观察、author_approved=false，不冒称维护者已批准。value producer/consumer并列不证明运输；field逐site保留presence/shape/copy/effects/return未知；budget只抽局部声明/比较/增量，不求值或证明termination/激活。完整DFG、一般heap、跨进程运输和预算归属未实现，空findings不代表通过。

v0.8来源准备见 [FIELD_SOURCE_REVIEW](../reports/astra-iteration5/FIELD_SOURCE_REVIEW.md)和 [field-source-observations](../reports/astra-iteration5/field-source-observations.json)，不算自动成果。最终来源事实补充P3的局部normalization/helper-return和P4的engine rest/services，但五路径仍unknown；P3还缺字段reaching、scheduler/assignment/JSON/inbox/broker记录运输和new-existing关联，P4还缺bridge真实装配/参数转交与有效预算消费者，未升级整条义务或完整claim。其它参数源/装配/预算及反证仍按原五项/30义务验收。

原26中的五项人工判断仍按历史协议evidence_only，不因额外合同事实加入call reproduced。新目标账本可以在必要义务全部闭合且可信模型/真实环境条件清楚时独立标记scoped_static_judgment_reproduced，旧eOnly不锁死目标。v0.11五目标当时尚未闭合；局部支持、条件风险、policy声明、未实现分析和运行故障分别表达，不能把缺分析伪装成“假设成立”。

第三轮来源依据为 [参数](../reports/astra-iteration3/PARAMETER_EVIDENCE.md)、[导航](../reports/astra-iteration3/NAVIGATION_EVIDENCE.md)、[原子边界](../reports/astra-iteration3/ATOMICITY_EVIDENCE.md)。worker的常量3是独立构造，不是已证明同对象上的覆盖；scopeHash会保留已有查询，缺键涉及字面路由种子和环境读取条件；process fence与目录锁范围/寿命不同，存在lock不证明无竞态。参数稿11项观察独立于冻结26项，人工AST锚点、模型前提和自动结果分别计数，不把源码准备稿当自动分析报告。

后续能力核对必须保留全部 26 项观察：9 项直接调用、1 项路径、3 项要求保留未知、13 项仅有证据。先验证原文件哈希和引用，再核对同一调用位置或逐边路径。原文件变更、范围排除、解析失败、端点歧义、未知保持和关系不匹配分别呈现。新增独立样本可以扩展基准；既有观察语义改变需变更观察身份或基准版本。

整个路线不新增目标执行、测试、构建、动态 trace 或沙箱能力，也不从正常静态扫描推导运行通过、业务验收或全功能完整性。

v0.9预算来源准备见 [BUDGET_SOURCE_REVIEW](../reports/astra-iteration6/BUDGET_SOURCE_REVIEW.md)与 [机器来源包](../reports/astra-iteration6/budget-source-observations.json)，该轮来源身份核对见 [BUDGET_FORMAL_REVIEW](../reports/astra-iteration6/BUDGET_FORMAL_REVIEW.json)；IR验收见 [IR_MIGRATION_ACCEPTANCE](../reports/astra-iteration6/IR_MIGRATION_ACCEPTANCE.md)及 [IR_MIGRATION_COMPARISON](../reports/astra-iteration6/IR_MIGRATION_COMPARISON.json)。[v0.10.0候选](../reports/astra-iteration7/SUPERSEDED_CANDIDATE.md)因内部EvidenceRef构造协议修正被替代，v0.10.1重新冻结与扫描；手工来源、组件观察、正式自动关系和完整目标评审保持分栏。
