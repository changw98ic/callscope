# Astra 对照推进：v0.9 不可变字段 IR 与局部预算

版本：CallScope 0.9.0。日期：2026-10-12。

本轮已完成两个真实仓库的冷／热静态扫描。公共不可变IR已由字段适配器实际消费，新增两种局部预算源码模式；**字段精度目标仍未达成，五项完整判断仍未达成。** 三条字段合同的五个评估位置全部unknown，services helper的自有字段形状较v0.8退回unknown；两项预算只支持局部源码形状，不证明数值限额或真正执行消费。

验收仍采用原[五项判断／30义务合同](../astra-iteration4/GOAL_ACCEPTANCE.md)和本轮[逐义务账本](goal-ledger.json)。账本从冻结模板重新映射正式自动证据，分类方法为manual_review_of_saved_automatic_evidence、automatic_obligation_solver_used=false；不是通用自动业务判断求解器。原[26项观察](../astra-baseline/capability-baseline.json)及历史报告不改写。

## 本轮真正改变了什么

**字段判定改用公共不可变状态。** semantic_ir的allocation、当前ObjectVersion、copy-time ObservationRef、FieldSlot、shared referent、EffectRef和ModelGuard分开表达。字段适配器实际使用allocate／bind／lookup／copy／write／reachable-effect／join，移除了旧mutable value/frame、clone与全局epoch算法。复制固定当时的源own-slot状态，浅复制的child仍保留共享allocation，并在以后读取当前状态；未知捕获、alias、getter／proxy、computed与effects继续保留。

这完成了公共协议及真实接线，不等于改善目标字段结果。正式五个位置的source_form_relation、presence仍unknown，selected-shape／source-form完成位均false。三合同自动事实分别208／163／503，共874，粒度较旧版改变，不能把事实条数增长当精度或功能增长。engine的真实services helper摘要当前为presence unknown、selected／whole shape false；组件层11个keys及maxRetries absent观察不能代替适配器的最终关系。

copy模型的适用范围已明确为整个相关own-enumerable普通data表面；另行注册ecmascript-own-data-read-v1提供有限actual Get条件。旧copy-only配置仍可接受，却不认证Get。每次应用仍需匹配来源guard，不能从模型名称或boolean直接补已知值；模型／政策前提变化与实现精化分别阅读。字段精度未改善，需要继续收窄可达effects及helper／return适用摘要。

**预算新增真实局部来源关系。** 两条conditional合同仅选择subject及counter／limit词法声明，不预填比较、阈值、增量或消费者连接，author_approved=false：

| 合同 | 正式自动源码关系 | 仍未证明 |
| --- | --- | --- |
| cpb-phase-retry-local-budget | prepareRecovery的:396 `>=`，对应局部counter／limit声明与:530／575／619／663四个counter写入；嵌套guard的分支源码 | 数值域、guard激活及整个主体支配、更新与真实attempt完成、CLI参数归属／上游运输 |
| cpb-verification-infra-local-budget | :1004 `iteration <= maxRetries`、initializer／单步更新，limit经已保存CALLS连接helper原文；早退与异常来源另存 | helper数值求值、实际循环次数、body完成／termination、其它phase或job预算等价 |

两项source_form_complete=true仅限所选局部模式，两项finding仍uncertain。numeric_bound_proven、runtime_budget_consumption_proven、termination_proven和whole_function_domination_proven均false。FailureRouter的表预算／durable attempts及opaque supervisor仍是不同来源与反证；不能从搜索缺同名字段推断全程序未消费，也不知道目标作者希望CLI retries控制哪一种预算。

来源准备与自动结果分开：[预算来源稿](BUDGET_SOURCE_REVIEW.md)及[24项人工来源包](budget-source-observations.json)不计自动成果；[预算正式评估](budget-assessments.json)只引用本轮保存快照。[预算来源复核](BUDGET_FORMAL_REVIEW.json)核对3份保存原文的103个去重区间、声明及已有调用，不证明运行预算。[IR迁移要求](IR_MIGRATION_ACCEPTANCE.md)冻结验收边界，正式对照见[迁移比较](IR_MIGRATION_COMPARISON.json)及[迁移结果](IR_MIGRATION_RESULT.md)；组件／开发观察不用于补正式字段positive。

## 正式身份与原26项对照

| 指标 | CodePatchBay | WinWinCode |
| --- | --- | --- |
| 最终snapshot | bc3350f010b470fb2bcf8e72e8e966bd432602ae07ec465666f797bb6a4ff1de | 640931a5622d449ab3aa8a141336e6b45818397c97cbcc35e4491645bc55eae7 |
| 完整解析／选入文件 | 330／333 | 465／471 |
| 节点／边 | 11,085／60,571 | 32,407／171,983 |
| 确定绑定调用 | 23,380 | 16,293 |
| 辅助原文 | 0 | 4 |
| 快照覆盖状态 | partial | partial |
| 配置式有限发现 | 8 | 2 |

最终工具源码身份为35aedb73739399068219e6b9b46840c27441f5b1f74430031234ffb285c8b7fc，分析器static-multilang-9、检测器call-rules-8-field-ir-budgets、schema 2。字段摘要finite-field-summaries-3-ir，wrapper／策略static-field-contracts-2-ir／static-field-policy-v2，公共IR finite-immutable-semantic-ir-1；局部预算static-local-budget-contracts-1／static-local-budget-policy-v1。身份见[CORE_FREEZE](CORE_FREEZE.json)。

原26项保持10 reproduced、3 unknown、13 evidence_only；36份来源hash／quote均matched，与v0.8的分类changes=[]。10条配置式有限发现不是10个bug，局部模式与原26项和30义务是不同集合。三份Shell未支持文件与六份Rust解析缺口保留，两库仍partial。

两库cold发布新快照；warm复用全部请求语言memo，得到相同ID且created=false。官方CocoIndex仍为语言整体缓存，检测每轮full。没有逐文件语义增量、增量检测、准确率或性能达标声明。

正式依据：[CPB扫描](codepatchbay-integration.json)、[WWC扫描](winwincode-integration.json)、[CPB汇总](codepatchbay-summary.json)、[WWC汇总](winwincode-summary.json)、[CPB v9／v8比较](codepatchbay-baseline-v9-and-v8.json)、[WWC比较](winwincode-baseline-v9-and-v8.json)、[能力账本](capability-ledger.json)、[字段评估](field-assessments.json)、[预算评估](budget-assessments.json)及[有限合同见证](finite-contract-witnesses.json)。独立范围见[Astra报告](INDEPENDENT_REVIEW.md)。

## 原完整目标没有缩小分母

新账本保留全部五claim和30必要义务，实际611条递归引用／104个去重JSON pointer均绑定本轮summary的SHA、snapshot、finding、rule和contract身份。账本分类是人工评审范围映射：4个限定子义务支持、20个partial、6个unknown；五项完整判断全部partial，完整验收false。唯一类别变化为CPB-01.P5从unknown增加预算局部源码partial，不是完整预算决策通过。

| 完整判断 | 本轮局部进展 | 仍缺的必要闭合段 |
| --- | --- | --- |
| CPB重试参数 | 公共IR真实接线与更多局部字段／effects出处；P5新增两预算模式源码 | 字段五路径仍unknown，new/existing、scheduler／assignment／JSON／inbox／broker身份、bridge装配与转交、预算归属／激活／guard和opaque反证 |
| CPB终态分类 | 保存既有初始化成员差 | 状态生产／具体job投影、terminal消费谓词、recover guard、event-store保护与状态政策 |
| CPB同键窗口 | 所选保护region与谓词差保留 | 真实deps、物理资源／collection heap／全写者、guard状态可达和模型推导交错 |
| WWC导航 | 原query/callback及有限port关系保留 | 可见DOM、route／event到提交、公开VM／其它effects和ambient接缝 |
| WWC Device字段 | 封闭对象缺键与guard出处保留 | 实际UI／client、command／协议版本／camel-snake运输、Rust dispatcher／authority、Device非空guard与反证 |

下一步先使IR适配器的真实字段段获得可解释的有限源式闭合，完善copy观察、reachable effects、helper／return摘要及独立Get模型；再连接消息／记录身份与具体预算归属。完整目标始终按必要关系验收，不能通过增加模块、事实、配置角色或调用样本变成达标。功能正确与闭环优先，可扩展性其次，性能最后。

## 操作边界

本轮没有执行／导入／测试／构建目标，没有工具测试套件或浏览器。冷／热扫描与[七类型保存查询](saved-query-observations.json)属于受信工具正常静态应用；查询只读取最终保存快照，配置数为CPB18／WWC12，不是满足数。源码／引用／语法检查见[交付检查记录](verification-summary.json)，目标只读状态见[仓库状态记录](target-state-observations.json)；这些不能当目标功能测试通过或业务正确保证。
