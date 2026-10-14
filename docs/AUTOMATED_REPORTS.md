# 自动项目分析报告

## v0.14：具体职责与文档部署对照

当前版本已接入正常 `build_project_report` / CLI / HTTP / MCP 报告路径。两库正常 full 冷/暖分析和自动报告已保存：[CPB](../reports/astra-iteration12-scope2/codepatchbay-automatic-report.md)、[WWC](../reports/astra-iteration12-scope2/winwincode-automatic-report.md)。原报告有限内容按[正式内容对照](../reports/astra-iteration12-scope2/ORIGINAL_REPORT_COMPLETION.md)核到实际正文与来源；开发查询或字段存在不能代替正式证据。

CPB 保存3项原判断/18项必要关系、16条源码关系、15,223个实际来源操作；WWC保存2项原判断/12项必要关系、20条源码关系、10,023个实际来源操作。五项判断及30项必要关系全部支持，所选关系均为限定源码支持；图仍为partial、解析为330/333与465/471。各数量只说明保存范围，不是全仓库功能覆盖率。

原26项观察保持10 reproduced/3 unknown/13 evidence_only，两库changes=[]；36份原引用与仓库commit匹配，65份核心与冻结存档一致。见[正式发布身份](../reports/astra-iteration12-scope2/PUBLICATION_IDENTITY.json)。两库两次full重算同快照、第二次不重复创建；本轮扩展了模型与源选择，不作同策略精度或性能比较。

`architecture.responsibility_explanations` 从认证保存的 CST、词法 binding、真实参数绑定和所选声明生成操作及具体正文。目录和业务分组只作导航。所有操作、源码位置、来源引用、guard、普通调用与消息边界保留；记录构造不解释为物理提交，字段同名不解释为身份相同，返回不一概解释为业务拒绝。

`documentation_comparisons` 索引实际文档段落与所选部署源码的有限比较。新 `document_deployment_consistency` 规则额外要求数据定位 `documents: [{role, file}]`；每个路径必须在辅助原文捕获范围内，按 raw hash、decoded text hash、字节大小及 BOM 认证。文档事实不冒充 AST 或 CALLS；既有 `sources` 仍只指实际代码声明，旧规则无需添加文档字段。策略协议为 `static-report-claim-policy-v2-documents`。

`conditional_state_lineage` 和 `conditional_publication_boundary` 分别解释实际状态分支、事件/队列记录来源以及配置/许可条件下的发布接口。有限 Boolean/enum 分区来自实际表达式，不执行目标输入。外部回调、持久化、远端写入和恢复结果保留条件或未知。

报告生成器为 `captured-project-analysis-report-3`。`report_components` 保存当前生成器、职责解释器、操作抽取器、Markdown 视图与工具身份；`snapshot.component_versions` 保留原扫描身份。新版报告可以解释旧快照保存的源码，但不能升级旧 Finding 或混写成新的正式分析。默认 Markdown 显示发现、具体职责、实际条件和有限表；完整 JSON、原 pattern/source facts、反证与未知项均保留。

最终范围按[原全文有限命题合同](../reports/astra-iteration12/REPORT_COMPLETION_CONTRACT.md)读回，发现原已读子句遗漏后继续补实现。五个判断、31 条旧关系和版本发布不是停止条件。

实现目标以最初的 [CodePatchBay 分析报告](../reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md)和 [WinWinCode 分析报告](../reports/astra-baseline/WINWINCODE_ANALYSIS.md)为准。它们提供要解释的架构范围、主要链路、具体结论、成立条件、反证和未审范围；不会作为检测器输入直接生成答案。Astra 不承担后续每轮批准或重复审查的角色。

五项判断及三十项必要关系是既有实现追踪账本，不代表两份全文报告的全部内容。原二十六项图观察继续依照冻结协议比较，不能通过改标签制造能力提升。新的完整静态条件判断与旧图观察的历史类别分别保存。

## v0.13 历史版本状态

v0.13.0 的两库正式自动报告已经保存：[CPB](../reports/astra-iteration11/codepatchbay-automatic-report.md)、[WWC](../reports/astra-iteration11/winwincode-automatic-report.md)。CPB 13 条、WWC 18 条报告关系均为 `scoped_source_relations_supported`，五项原判断均 complete/full 支持且必要缺口为空。[正式账本](../reports/astra-iteration11/goal-ledger.json)保存五项 `scoped_static_judgment_reproduced`、30 必要关系 supported、未闭关系为空；[证据引用文件](../reports/astra-iteration11/GOAL_JUDGMENT_EVIDENCE.json)关联 704 个真实引用。31 条关系、五项/30 关系与解析比例都不是功能覆盖率。

正式 [CPB 扫描记录](../reports/astra-iteration11/codepatchbay-integration.json)和 [WWC 扫描记录](../reports/astra-iteration11/winwincode-integration.json)记录各库冷/热同 ID、created=true/false；源码 hash 与各自 v0.12 相同，解析仍为 330/333 和 465/471。工具与策略身份见 [v0.13 冻结记录](../reports/astra-iteration11/CORE_FREEZE.json)。开发查询继续作为开发来源保存，不替代正式 Finding/Evidence 或改写旧版报告。

[原观察比较](../reports/astra-iteration11/ORIGINAL_BASELINE_COMPARISON.json)保持 10 reproduced/3 unknown/13 evidence_only，两库 changes=[]；36 份原引用的保存/现场 hash 与目标 commit 匹配。[发布身份](../reports/astra-iteration11/PUBLICATION_IDENTITY.json)verified=true，60 份核心 live/archive 及共享组件一致。该身份核对没有把原 26 观察重新定义成全文判断。

新增有限模型覆盖 readiness/completion/access-audit 条件门、WorkRun 状态/依赖选择表、消息字段与 outbox/ack 参数关系、事件索引投影与重建、可信命令中间来源、失败 record 保留、浏览器异步 guard 和捕获写者。结论仍限所选源码、模型和正常到达条件，没有声称达到或超过原全文。

## 使用

本轮保存产物另有 [CodePatchBay 简报](../reports/astra-iteration12-scope2/codepatchbay-analysis-brief.md)和 [WinWinCode 简报](../reports/astra-iteration12-scope2/winwincode-analysis-brief.md)，优先展示实际必要关系、有限表和所选边界。它们由独立的发布显示工具读取正式报告生成，没有重跑分析或修改原报告；[输入清单](../reports/astra-iteration12-scope2/BRIEF_INPUTS.json)记录来源及显示选择。具体职责与文档对照在正常自动报告正文中；source-only 边界及原明确未审范围见 [范围说明](../reports/astra-iteration12-scope2/REPORT_SCOPE_GAPS.md)。这个额外阅读视图不新增 CLI/API 格式。

在保存了分析快照的数据库上生成报告：

```bash
python -m callscope report --db /path/to/project.sqlite3 --format markdown --output /path/to/report.md
python -m callscope report --db /path/to/project.sqlite3 --snapshot SNAPSHOT_ID --format json --output /path/to/report.json
```

报告命令只读取保存图、源码和发现，不运行目标代码、测试、构建或外部验证。HTTP 提供 `GET /api/v1/report?snapshot_id=SNAPSHOT_ID`；MCP 提供 `get_project_report`，参数为可选 `snapshot_id`。历史报告使用指定快照的保存内容，不以当前工作区替代历史证据。

## 报告内容

`judgments` 保存配置的完整条件判断，包括必要关系、推导、真实适用条件、反证、剩余缺口及原发现证据指针。只有必要关系全部闭合、模型适用性成立、来源身份一致且没有截断，才能记录完整判断。局部缺口不能改写为环境假设。

`functional_chains` 保存主要功能链的有限源码关系：实际声明和调用、正常源码顺序、结果与守卫的连接、提前返回、构造和注入候选。按模式另记录可信命令来源、审计收尾、状态保护、部署分流、交付收尾和 agent 执行策略。所选源码关系成立不表示所有函数路径到达或外部副作用成功。

v0.13 的有限条件门、WorkRun 表、消息字段、record/codec/投影和生命周期关系也保存在这里。普通调用边、callback 来源接缝、跨消息字段关系和 SQL 位置分别表达；没有因为源码相邻、字段同名或方法同名便补出 CALLS、相同运行对象或事务成功。

`architecture` 保存目录组成和实际绑定的跨目录图引用。v0.13 的 `captured_writer_references` 额外引用实际保存的字段写者组、消费者和拒绝 guard，保留原 `ownership_assessment`；当前为 `partial_captured_writers_and_consumers`。它不从函数或目录名猜职责，不推断唯一事实所有者、规范权威、全部授权或持久资源等价。v0.13 正式结果中的具体职责解释，以及文档 Device/Credential 声明与实际部署差异尚未自动汇总；捕获 README/架构文档不代表规范对照已完成。更强的全权威、全权限、全协议证明与原未审范围不因此变成新验收目标，具体见 [本轮范围差距](../reports/astra-iteration11/REPORT_SCOPE_GAPS.md)。

`coverage` 保存选择范围、解析状态、失败文件和辅助原文身份。生成协议、Cargo manifest 等辅助输入是独立的惰性原文，不产生伪造函数或跨进程 `CALLS`。解析比例与已绑定边比例均不是功能覆盖率。

`configured_local_assessments` 保留局部合同结果，`graph_observation_counts` 保留结构观察。它们与完整判断分别呈现。所有结论继续保留必要未知，不自动阻断开发流程。

## v0.13 报告 v2 的展示与证据下钻

v0.13 保存时生成器为 `captured-project-analysis-report-2`，CLI/HTTP/MCP 的使用方式保持一致。`source_relation_index.entries` 为每条保存关系列出 Finding/Evidence ID、原 assessment/pattern/source_facts/source_scope/analysis_gaps 的 JSON Pointer 和保存 Evidence 指针。它是导航索引，不是第二个判定器。

每条 entry 的 `presentation` 是 `presentation_only=true` 的有界投影：按真实 pattern 展示必要关系、字段连接、guard、条件、反证和有限真值表。已有 false/null/unknown 保留；原行缺项单独标识，不伪装成计算结果。大型源码事实以准确 pointer 关联，完整 `functional_chains[].pattern`、source facts 和原 Evidence 均保留。

展示每节最多 224 个节点、深度 8、普通列表 6 项、字符串 240 字符；表格最多 64 行/12 列，最多收集 24 张表。达到限额时记录截断与完整引用，展示省略不会变成分析支持，也不会把 partial 变为 supported。[展示设计](../reports/astra-iteration11/PROJECT_REPORT_PRESENTATION_DESIGN.md)说明了投影与原始数据的对应方式。

写者引用同样只展示已有证据。`whole_report_reproduction_claimed=false`、`runtime_functionality_verified=false` 和各 pattern 的未证明边界继续保留；表格行数和关系索引条目数不能用来声称报告覆盖率。

[正式 CLI 读回记录](../reports/astra-iteration11/CLI_REPORT_READBACK.json)确认正常 `report` 命令导出的 WWC Markdown 与正式报告字节/hash 一致；保存数据库的逻辑、schema 和身份相同，没有重扫或执行目标。原报告条目到真实保存证据的对应见 [本轮对齐导航](../reports/astra-iteration11/REPORT_ALIGNMENT_RESULTS.json)，该导航不新增判定或全文评分。

## 扩展与身份

`goal_contracts` 通过固定注册的分析器解释数据定位器；`report_claims` 提供所选声明和版本化有限模型。策略不能提供中间字段流、guard、交错步骤或正确结果，不能导入任意目标程序或 Python 插件。

源码事实、受信模型、策略声明和未解析关系分别保存。报告结论可下钻到原快照的文件 hash、AST 范围、声明身份、调用点和证据 ID。工具、策略、解析组件或辅助捕获范围改变后产生新快照，原始报告和历史快照保持不变。

当前实现使用纯静态模型。运行结果、所有并发路径、全部 HTTP 入口、外部 provider 的真实性及全仓库无缺陷均不由这些报告保证；原人工报告也没有作这些保证。
