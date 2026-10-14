# 原完整分析报告与正式自动报告的范围差距

截至 2026-10-13，正式自动报告已承接原报告的 CPB-01、CPB-02、CPB-03、WWC-01、WWC-02 五项具体条件判断。它们的实际记录均为 `scoped_static_judgment_reproduced`，`complete_assessment=true`、`full_goal_supported=true`，必要缺口为空。主要链路另有自动源码关系，仍不能把这些判断、源码链、目录盘点合并成“两份全文已经自动复现”。下面只解释保存产物承接了哪些原内容，以及还有哪些具体距离；不重新审查目标项目，不增加评分或验收分母。

## 依据与定位方式

| 标识 | 正式保存产物 | 快照 / 产物 SHA256 |
| --- | --- | --- |
| C | [CodePatchBay 自动报告](codepatchbay-automatic-report.json) | 快照 `7524afef4f9234ebef40eec1d74dbb91a3f56dc76f0191728c42d3bdd3cfb167`；JSON `6ff36204cda0ceb12fe15e8d1dc2e999ad71bc9d59d3d87faedb449816d58eb9` |
| W | [WinWinCode 自动报告](winwincode-automatic-report.json) | 快照 `ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28`；JSON `884202b5715f42c61a428479c18d91963b6452410a1f009855fd9a0ae130b8d7` |

原依据是 [CODEPATCHBAY_ANALYSIS.md](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md) 与 [WINWINCODE_ANALYSIS.md](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md)，其冻结 hash 见 [CORE_FREEZE.json](CORE_FREEZE.json) 的 `/benchmark_reports`。本文逐库流式读取正式 JSON；未读取数据库、调用分析器、执行目标、测试或构建。

`C:/…`、`W:/…` 是对应正式 JSON 的 JSON Pointer。`judgments` 与 `functional_chains` 条目保存实际 `finding_id`、`evidence_id`；`source_facts` 保存来源位置、原 hash、解析身份和具体关系。引用一个来源或目录只表示被捕获，不表示已生成对应功能结论。`policy_declarations` 中的条件和反证文字是配置范围；源码计算的事实、注册模型与配置声明仍分开。

## 原五项具体判断已经自动承接

| 原判断及行锚点 | 实际自动结论 | finding / evidence；正式指针 | 模型、条件及反证范围 |
| --- | --- | --- | --- |
| [CPB-01：重试参数接线](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:86) | 普通生产 pipeline 的提交字段经 metadata、持久记录和消息传递，但 worker 使用独立预算；queue、phase、verification-infrastructure 的权威预算分开。 | `c5702ff61b2fe477fb28b9dc` / `71f6cf7c7a31d0977b4c9a06`；`C:/judgments/0`，来源链见 `C:/judgments/0/obligations/2/evidence`；完整 source facts 在 `C:/judgments/0/adapter_judgments/0/evidence/0/details/source_facts`。 | 有限普通记录、正常 JSON/async/默认装配及受认证通道；旧记录复用、finalizer-only、提前返回、不透明消费者和失败通道单列。不是没有 retry 能力。 |
| [CPB-02：终态分类不一致](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:94) | 有效 job 身份和当前 `superseded` 状态下，消费者终态谓词为 false，权威集合成员关系为 true，所选消费者进入拒绝分支。 | `4b842226073458a0e78e4030` / `042e5b5d63099be326f960a9`；`C:/judgments/1`，状态来源与消费者见 `C:/judgments/1/obligations`、`C:/judgments/1/adapter_judgments/0/evidence/0/details/source`。 | 普通当前记录及稳定集合语义；缺身份、权威封口、允许事件和恢复政策分开。没有推出非法写入或必须开放 recovery。 |
| [CPB-03：幂等并发窗口](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:100) | 真实预查、保护区写入、guarded scheduled 更新生成有限交错；两次预查为空、第一项被调度后第二项可再次插入。 | `a6270e2d476c805d8c26eb60` / `78f93f2d73951286ebc21de9`；`C:/judgments/2`，交错及反证见 `C:/judgments/2/obligations/6/evidence`、`C:/judgments/2/refutations`；源扫描在 `C:/judgments/2/adapter_judgments/0/evidence/0/details/source`。 | 默认依赖、同逻辑 queue 身份、正常锁/发布及有限记录模型；同描述仍 pending、顺序 facade 复用、不同 description 与失败路径分别保留。没有声称并发已经实际发生。 |
| [WWC-01：看板导航丢 delivery](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:92) | 所选公开 href 缺值，经真实生产端口闭包传到 create，命令提交前被拒绝。 | `333b5dc5882abce976c0d9dc` / `1f75ceee5eab722beeb2d270`；`W:/judgments/0`，来源与拒绝链见 `W:/judgments/0/obligations`、`W:/judgments/0/adapter_judgments/0/evidence/0/details/source_facts`。 | 标准 DOM/URL 模型、当前 hash 为所选导航结果、挂载及表单 guard 允许提交；有效 delivery 链接、fake/taskSeed 与独立 Chat 入口保留。不是所有任务创建失败。 |
| [WWC-02：Device 条件必填字段遗漏](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:102) | 闭合 UI 命令遗漏字段，经生成协议、普通 JSON、Serde 到 `None`，活动 Device authority 的非空守卫在使用/提交前拒绝。 | `89fc6bad0b0557c4623dd65b` / `3a311ed2a8291589c7016d8c`；`W:/judgments/1`，协议与 authority 来源见 `W:/judgments/1/obligations`、`W:/judgments/1/adapter_judgments/0/evidence/0/details/relations`。 | 默认生产装配、正常通道、授权/版本/基线允许到达所选 guard；local、Chat 显式字段、非活动 Device、已存在 exact receipt replay 分开。不是所有规格编辑失败。 |

各项实际 `conditions`、`refutations` 和 `necessary_gaps` 都保存在上述 judgment 内。这是原具体静态判断的承接范围，不是运行通过或全项目功能覆盖率。

## 原主要链路目前承接到哪里

### CodePatchBay

| 原报告具体内容 | 自动来源与实际状态 | 已建模的关系 | 仍保留的范围 / 未形成的同等结论 |
| --- | --- | --- | --- |
| [命令、队列、worker、bridge、服务组合](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:44) | `C:/judgments/0/obligations/1/evidence`、`/judgments/0/obligations/2/evidence`；完整 CPB-01 内的生产装配与记录/消息链。 | 默认 CLI pipeline 装配、候选/assignment/inbox/worker 的字段来源、bridge 与预算消费者；消息关系未伪造成 CALLS。 | 不等于每个 CLI handler、任意 executorRoot 或所有 ctx 注入都唯一绑定；fix readiness 的提交前早退顺序未成为独立自动结论，见后表。 |
| [引擎准备、规划、冻结、DAG 与早退](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:58) | `C:/functional_chains/2`：`scoped_source_relations_supported`；早退来源如 `/functional_chains/2/source_facts/46`。 | `runJob`/`runJobInner` 的实际步骤、返回 guard、结果绑定、正常源码顺序。 | 前序正常完成及所选分支到达是条件；没有证明所有 workflow、全部阶段子模块或 completion gate 的每个豁免分支。 |
| [job audit best-effort](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:64) | `C:/functional_chains/3`：`scoped_source_relations_supported`；`/functional_chains/3/source_facts/9`。 | 正常/panic 相关作用域中，同一认证目标的捕获调用及 empty catch。 | `pattern/audit_subject_equivalence_to_other_systems_proven=false`；未由它生成 Hub access audit fail-closed 的另一份完整合同。 |
| [Agent、环境与沙箱策略](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:66) | `C:/functional_chains/0`：`scoped_source_relations_supported`；allowlist 拒绝来源 `/functional_chains/0/source_facts/278`。 | allowlist→注入 pool、执行后 readonly 审查、失败分类、环境过滤→sandbox wrapper→ACP spawn 的实际来源与条件。 | 唯一外部 pool、所有 secret 拒绝、实际隔离仍为 false；native/off/custom、平台及显式 credential 分支保留，不升级为运行安全保证。 |
| [可信 probe 命令来源](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:68) | `C:/functional_chains/4`：`scoped_source_relations_supported`；policy read `C:/functional_chains/4/source_facts/80`、lookup `C:/functional_chains/4/source_facts/83`。 | 捕获 HEAD policy、predicate lookup、源实参/形参关系及结构化 execFile 参数形式。 | `/analysis_gaps/0` 保留中间值/外部效果缺口；`pattern/expected_evidence_noninterference_proven=false`。不能把所选参数源码形式扩大为所有值路径的非干扰判断。 |
| [未支持 probe 的失败记录](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:70) | `C:/functional_chains/5`：`scoped_source_relations_supported`。 | 固定方法集合、条件失败 record、marker 设置与消费 guard 的来源。 | `/analysis_gaps/0`、`pattern/silent_drop_for_all_inputs_excluded=false`；尚未闭合所有输入的 record 保留与持久化。自动事实没有执行任何 probe。 |
| [执行结果、finalizer、持久结果与 reconciler](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:82) | `C:/functional_chains/1`：`scoped_source_relations_supported`；`C:/functional_chains/1/source_facts/483` 的条件收尾与 `C:/functional_chains/1/source_facts/485` 的实际 callback 安装。 | autoFinalize/执行成功的条件关系、失败结果替换、writer 的新建/已存在校验、attempt/finalizer/journal 与队列投影的来源条件。 | `pattern/remote_success_proven`、`exactly_once_proven`、`all_recovery_complete_proven` 均 false。原报告本身也未承诺远端成功或全部恢复正确。 |

### WinWinCode

| 原报告具体内容 | 自动来源与实际状态 | 已建模的关系 | 仍保留的范围 / 未形成的同等结论 |
| --- | --- | --- | --- |
| [浏览器生产入口、task port 与所选命令协议](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:46) | `W:/judgments/0`、`/judgments/1`；生成来源捕获见 `/coverage/support_inputs/3`、`/4`、`/6`、`/9`。 | 两项具体判断所需的真实端口、URL/字段、普通 JSON/Serde、命令分派及条件拒绝链。 | 生成合同的捕获不是全部生成文件一致性判断；没有推出全部 auth/render lifecycle、HTTP/WS 或 ExecutionPort 协议已经闭合。 |
| [Chat 的 Delivery、WorkItem、WorkRun 请求](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:54) | `W:/functional_chains/1`：`scoped_source_relations_supported`。 | 所选 create 来源的请求步骤、guard、结果绑定和正常顺序；作为独立入口反证保留。 | 不等于每个跨请求身份/重试字段都得到语义关联，也不等于 Chat 实际创建成功。 |
| [WorkRun 校验与状态选择](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:60) | `W:/functional_chains/11`：`scoped_source_relations_supported`；谓词来源 `W:/functional_chains/11/source_facts/35`。 | start_next/start_item 的同一首个认证校验、正常顺序、选择谓词源码。 | `/analysis_gaps/0` 保留 iterator/macro 语义；`pattern/all_active_states_or_attempts_proven=false`。有限 runnable/dependency/active 状态条件尚未全面计算。 |
| [Worker 两入口与生产组装](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:62) | `W:/functional_chains/8`、`/functional_chains/9` 均 `partial_source_relations`。 | 源码 body、调用、生产构造实参与正常顺序均已保存。 | graph role binding 的 attribute-macro 限制仍在 `/analysis_gaps`；源码 body 可读取没有被当成绑定已闭合，也没有按方法名猜泛型唯一实现。 |
| [typed dispatch 与 checkout/adapter 边界](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:64) | `W:/functional_chains/10`：`scoped_source_relations_supported`；guard 来源 `W:/functional_chains/10/source_facts/95`。 | accept_control/accept_dispatch/start_dispatch 的步骤、guard、正常顺序及调用来源。 | 不是 lease、job/workspace/profile、adapter/session/turn 的全链字段身份关联；generic 端口仍不能在全类上绑定唯一生产实现。 |
| [Production adapter 与嵌入式 Kernel](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:70) | `W:/functional_chains/6`：`scoped_source_relations_supported`。 | adapter open 与 Kernel constructor 中的实际构造/调用顺序、错误继续条件及 source guard。 | 所选生产接线不是全部 helper、vendored 工具或沙箱审查；不从源码顺序推出资源恢复成功。 |
| [submission intent→persist→exact reconcile](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:74) | `W:/functional_chains/0`、`/functional_chains/7` 均 `scoped_source_relations_supported`。 | 同一 submit_turn 的状态赋值、persist/reconcile 来源和正常顺序。 | 两条规则选中同一来源，不累计为额外功能覆盖；不是全 WAL/outbox/ack 身份与恢复状态机判断。重叠见 `/overlapping_source_selections`。 |
| [Kernel 三个不同接口](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:76) | `W:/functional_chains/3`、`/4`、`/5` 均 `scoped_source_relations_supported`。 | create_session、submit_turn、reconcile_turn_exact 分开保存；async 子区域有明确来源与条件，如 `/functional_chains/3/source_facts/24`。 | 延迟 body 的激活、future 完成及所有 session/turn 状态效果未由源码步骤证明；接口没有按相近名称合并。 |
| [Device provider 部署分流](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:84) | `W:/functional_chains/2`：`partial_source_relations`；boundary 源结果 `W:/functional_chains/2/source_facts/72`。 | Server unsupported body、worker/provider 构造来源及安装赋值均已保存，可反驳“一个 unsupported 就代表全项目无模型连接”的过度推断。 | `/analysis_gaps` 保留 macro binding、部署候选/credential 范围；没有自动比较架构文档长期 Credential 所有权与 Device 实现，见后表。 |

以上主要链的实际 `assessment/full_functionality_proven` 与 `whole_report_reproduced` 均 false；其中源码关系支持不等于整段原文的全部语义被计算。配置反证文字仍可在各条目 `policy_declarations` 中看到，不能替代实际 source facts。

## 原报告已有内容中，仍未形成相应自动结论的具体部分

下面列的是原报告与当前产物的有限距离；“尚无相应结论”指正式报告没有提供该结论，不是断言目标代码缺功能。

| 原内容及行锚点 | 当前实际承接范围 / 正式指针 | 剩余有限静态关系 |
| --- | --- | --- |
| [CPB fix readiness 失败先返回、再允许 enqueue](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:48) | CPB-03 已计算同键 facade/authority；`C:/judgments/2`。主要顺序条目选的是 runJob，来源选择见 `C:/functional_chains/2/source_scope`；没有独立 readiness→提前返回→enqueue 结论。 | 将实际 readiness 返回值、失败 branch、提前 return 与后续提交的正常到达关系连起来。 |
| [CPB completion gate 的 checklist、mutating verdict 与 readonly/docs/parent 豁免](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:72) | runJob 的调用/前置 guard 已抽取：`C:/functional_chains/2/pattern/sequences`；当前该条目的 selected_definitions 没有 completion-gate body。 | 计算所选 workflow 条件、各门的真实消费者与豁免分支；不能用“调用到完成门”代替它们。 |
| [CPB 事件提交、索引投影、重建/doctor 的不同边界](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:76) | CPB-02 已计算当前状态分类和权威封口范围：`C:/judgments/1`；交付结果到 queue projection 已单列：`C:/functional_chains/1`。 | 尚无事件内容→索引投影→失败/重建来源的独立自动结论。限于该持久化/投影段落，不要求全部崩溃恢复演练。 |
| [CPB Hub access audit 与 job audit 是不同对象](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:64) | job 的 caught-call 来源成立，但 `C:/functional_chains/3/pattern/audit_subject_equivalence_to_other_systems_proven` 为 false。 | 自动呈现 access-audit 写入与响应拒绝的主体/guard，和 job best-effort 分开比较；不扩大成全 HTTP 安全审计。 |
| [CPB trusted command 与 unsupported evidence 的精确来源](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:68) | `C:/functional_chains/4/analysis_gaps/0`、`/functional_chains/5/analysis_gaps/0` 是实际 source-only 缺口。 | 对已选 codec/参数与失败 record 补中间值保留、覆盖、consumer 及写入来源；保留 hardGate observation 反证。不要求执行命令。 |
| [WWC auth/scope、lazy render generation/abort 防旧结果回写](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:48) | 看板/clarification 两项条件链已闭合：`W:/judgments`；其挂载/guard 条件保留，并没有独立 auth/render lifecycle 判断。 | 围绕已读 render/install 入口，关联 generation、abort、旧 callback 返回和写回 guard。不是全 UI 浏览器验收。 |
| [WWC WorkRun runnable/dependency 与活动尝试过滤](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:60) | `W:/functional_chains/11/pattern/selection_predicate_sources` 有源码；`/pattern/all_active_states_or_attempts_proven=false`。 | 将有限 iterator/enum/`matches!` 条件及实际被选 item 与 start_item guard 连起来；不是穷举完整领域状态机。 |
| [WWC Worker、adapter、Kernel 的消息与身份分离](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:42) | typed dispatch、adapter 与 Kernel 段分别支持：`W:/functional_chains/10`、`/6`、`/0`、`/3`、`/4`、`/5`；生产构造仍 partial：`/8`、`/9`。 | 先关闭捕获声明的有限 macro/receiver 适用范围，再关联所选消息的 job/lease/workspace/profile/session/turn 字段与候选装配；不把源码段邻接当作同一身份已经传递。 |
| [WWC candidate、evidence source、durable outbox/ack](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:78) | 当前自动条目是所选 WorkRun guard 和 adapter submit 顺序：`W:/functional_chains/11`、`/0`；没有全消息字段关联或独立 outbox/ack 合同。 | 对原已读候选/证据身份及 receipt/ack 段建立有限字段与顺序关系；不宣称外部 bytes、签名、日志真实。 |
| [WWC Device 实现与文档 Credential 所有权口径](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:88) | 代码分流是 partial 来源关系：`W:/functional_chains/2`；文档只捕获 headings，`W:/project_declarations/documentation/1/product_statements_independently_proven` 为 false。 | 尚无文档声明与代码部署分支的自动一致性结论。可把明确的所有权声明与 local/Device 来源对应，不把文档文本当代码事实。 |
| [两库职责和事实所有权解释](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:30)、[WWC 所有权](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:30) | `C:/architecture/meaning`、`W:/architecture/meaning` 明确仅目录组成与已绑定引用；project declarations 也不证明产品描述。 | 当前架构部分主要是结构盘点，不是原报告“谁拥有哪个事实、哪些操作被授权”的完整自动解释。应从实际 state/record 写者、接口和条件建模职责，而不是按目录名贴责任。 |

原报告提出的“HTTP/WS 名称、scope、expectedRevision、requestId 才是连接证据”已有 WWC-02 所选命令的实质承接（`W:/judgments/1/obligations`），尚不是通用全部协议判断；原文 [WWC:52](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:52) 与 `W:/report_scope` 共同界定这一范围。

## 源码捕获与局部未知不能代替上述结论

| 产物事实 | 正式定位 | 应保留的解释 |
| --- | --- | --- |
| CPB 选入 333 份、解析 330 份；三份 Shell unsupported。WWC 选入 471 份、解析 465 份；六份 Rust parse_error。 | `C:/coverage`、`W:/coverage`，具体文件见两者 `/coverage/unparsed_files`。 | 这是源码/语法范围；原文 [CPB:28](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:28)、[WWC:28](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:28) 已明确解析率与边比例不是功能覆盖。 |
| 老局部 contract、value、budget、field/navigation 条目仍可为 uncertain。 | `C:/configured_local_assessments`、`W:/configured_local_assessments`。 | 原局部分析口径与新完整判断不同，不能把其标签删除或解释成新完整判断退化；实际完整推导在 `/judgments`。 |
| 三个 WWC 主要条目保留 graph binding partial，body 来源依然存在。 | `W:/functional_chains/2/analysis_gaps`、`/8/analysis_gaps`、`/9/analysis_gaps`。 | attribute-macro / graph declaration 限制是分析能力边界，不是目标没有 Device provider、Worker 入口或 adapter。 |
| 结构 graph observations 与已绑定目录依赖单列。 | `C:/graph_observation_counts`、`W:/graph_observation_counts`、两者 `/architecture`。 | 递归/环不等于不终止，动态/trait 未知不等于缺实现；原 [CPB:108](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:108)、[WWC:112](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:112) 的否定边界继续成立。 |

## 原作者明确未审的范围：单列，不变成新验收目标

| 项目 | 原明确未审 / 只盘点内容及行锚点 | 当前产物位置与范围 |
| --- | --- | --- |
| CPB | [其他 CLI 命令、全部异常恢复交错、每种 workflow](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:18)；[全部 HTTP/OIDC/备份/发布 provider 逐分支安全、本地索引完整算法、测试/第三方/模板技能 adapter/所有平台部署](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:24)。 | `C:/coverage/excluded`、`/architecture`、`/report_scope`；所选 agent/delivery 原始模型限制另见 `/functional_chains/0/pattern`、`/1/pattern`。存在目录或源码不代表这些领域已经被自动审核，也不要求把原未审领域新增为本轮达标项。 |
| WWC | [全部 HTTP/WS 路由、完整领域状态机/并发、全部 vendored Kernel/工具/沙箱、所有 credential 路径及外部 adapter 副作用](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:20)；[测试、构建执行、所有生成文件一致性、第三方、全部平台和迁移](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:26)；[publication/audit/export/connector 未逐一行为审计](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:82)。 | `W:/coverage/excluded`、`/coverage/support_inputs`、`/architecture`、`/report_scope`。所选生成合同作为 support input 被捕获用于 WWC-02，不等于验证全部生成结果。原明确未审范围不会因五项判断完成而视为已覆盖。 |

两正式报告的 `/report_scope/whole_report_reproduction_claimed=false`，`/runtime_functionality_verified=false`。这与原报告的“未运行验证、完整不代表逐行审完”一致；不是新增执行或测试要求。

## 最有价值的剩余有限静态能力

1. **Rust 条件装配与有限 iterator/enum 关系。** 先针对已读 Worker/provider 来源的 macro/receiver 适用范围以及 WorkRun 的候选/活动 guard，补当前明确的 partial 和 source-only 段；对应原 [WWC:60](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:60)、[WWC:62](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:62)、[WWC:84](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:84)，正式 `W:/functional_chains/11`、`/8`、`/9`、`/2`。任意 trait 分派仍保留候选和未知。
2. **可复用的字段/消息/身份传递。** 将已完成 pipeline、navigation、Device 的来源追踪抽为通用有限模型，延伸到原已读的 Chat request identity、Worker/adapter/session/turn、outbox/ack；对应原 [WWC:54](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:54)、[WWC:78](/workspace/callscope/reports/astra-baseline/WINWINCODE_ANALYSIS.md:78)，正式 `W:/functional_chains/1`、`/10`、`/0` 及两库 `/judgments`。跨 wire 继续单列协议关系，不能补虚假 CALLS。
3. **条件门、顺序与投影的有限摘要。** 用已有 normal-reaching、字段和保护区能力承接 fix readiness、completion gate 豁免、event→index、access audit 响应段；对应原 [CPB:48](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:48)、[CPB:72](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:72)、[CPB:76](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:76)，正式 `C:/judgments/1`、`/2`、`/functional_chains/2`、`/3`。目标是原段落的源码关系，不是全程序并发或运行恢复证明。
4. **所选中间值与证据 record 的保留。** 对 trusted probe/unsupported evidence 的实际 source-only gaps 复用 codec、alias、覆盖与持久 record 来源能力；对应原 [CPB:68](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:68)、[CPB:70](/workspace/callscope/reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md:70)，正式 `C:/functional_chains/4/analysis_gaps`、`/5/analysis_gaps`。不执行 probe，不把调用 API 的存在当作命令值与证据内容已经验证。

这些优先项直接来自原已读段落与正式保存缺口。性能、图规模、章节数、事实数没有被用作功能成熟度指标；原未审安全、所有平台和所有外部副作用也没有被添加为本轮新的目标。
