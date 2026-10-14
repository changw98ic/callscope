# Astra 对照推进：v0.8 共享语义与字段来源

版本：CallScope 0.8.0。日期：2026-10-12。

本轮已完成两个真实仓库的最终冷／热静态扫描、共享内建环境和完成态迁移，以及三条选定参数字段合同的评估。**五项完整判断仍未达成。** 新字段合同保留全部五个分支／终点评估，结果均为unknown；新增源码事实不能替代值传递、消息运输或有效预算判断。

验收仍采用原[五项判断合同](../astra-iteration4/GOAL_ACCEPTANCE.md)及本轮[逐30义务账本](goal-ledger.json)。账本从冻结模板重新映射正式自动证据，`manual_review_of_saved_automatic_evidence`、`automatic_obligation_solver_used=false`；不是通用业务判断求解器。

## 实际自动进展

**共享协议已用于真实消费者。** `BuiltinEnvironment.audit` 在保存且认证的文档内检查有限标准接口、词法遮蔽、可见写入、host alias、prototype及escape；结果只启用注册模型，不验证实际宿主。最终 `Object.assign` 登记只允许静态调用的源码出现，没有赋予pure、receiver／arguments效果已知或字段复制语义。

completion接口区分ordinary sync/async、generator/async_generator、direct-await、return-without-await和有限正常值关系。普通同步调用可返回任意值，包括thenable；async body返回表达式不等于Promise fulfilled值。body激活、所有完成路径、运行和资源寿命独立保留未知。导航、port和atomic模块已实际共享这些接口，仍保留各自必要效果／资源护栏；不新增resolved CALLS。

**CPB字段摘要新增了可定位的源事实。** 配置只给主体形参字段和调用实参／return终点；实际rest排除、对象成员和spread顺序、helper调用／形参以及body返回来自保存AST和认证调用边，未预填中间传播链。

| 选定有限段 | 正式来源事实 | 分支／终点评估 | 尚未证明 |
| --- | --- | --- | --- |
| engine `runJobWithServices.opts` → `runJob`实参 | 75；包括5个实际rest排除键、helper实参／形参、`buildServices`的11个own keys和局部返回形状 | 1 unknown | 选定字段的reaching来源、前缀effects、实际bridge转交及有效预算消费 |
| `enqueue.input.metadata` → `resolveAgentsForEntry`实参 | 35；包括新字面对象、按序spread、实际callee／形参和可见写入 | 2 unknown | 浅别名／嵌套写入后的字段来源，以及queue新旧分支与后续消息身份 |
| `resolveAgentsForEntry.metadata` → body返回字段 | 16；保留直接return和spread新对象return的不同来源 | 2 unknown | 未闭合helper／alias effects及async返回同化后的fulfilled值 |

五个assessment不是五条普通CALLS路径：enqueue的同一个调用点保留两个分支上下文。每条有效合同输出一个uncertain摘要Finding，正向、未知及缺口均保存；本轮没有positive字段路径，selected-shape/source-form完整位都为false。126个局部事实或三个Finding都不能折成两个完整P3/P4义务通过。

具体可查的新事实：`engine-runner.ts:137` 的真实 `...jobOptions` 排除 `cpbRoot/project/sourcePath/hubRoot/workerBrokerClient`，产生rest范围的新浅复制；`:141`及`:73`的普通对象解构只记录读取／绑定键，未标记为复制输入。`buildServices`字面ports的11个外层键由AST全量读取，局部所选`maxRetries`形状为absent；这不证明整个opts字段已保留到消费者，其helper摘要同时记录`normal_prefix_effects_unknown=true`。

**判定不足有具体证据。** 五个路径的distinct effect数为8／13／12／11／13，全部低于每site24项展示上限，没有截断；完整barriers先参与状态失效。容器／callback逃逸、嵌套heap写、未知调用／receiver、Promise／iterator和async同化等边界没有因字面键已知而被清除。`normal_returns`仅标记`body_return_expression_only=true`、`fulfilled_value_proven=false`。详见[字段评估](field-assessments.json)、[完整有限见证](finite-contract-witnesses.json)及[CPB汇总](codepatchbay-summary.json)。

原先的三条初始化／对象／参数合同，加上导航、保护和本轮三条字段合同，共8条配置式有限发现；其来源仍为独立审查，`author_approved=false`。这不是自动确诊8个业务bug，也不是五项完整判断的验收结果。

## 共享迁移与既有能力

正式WinWinCode导航仍保存82个来源事件、8个声明节点、4条认证调用边和10项gap；possible query keys仍为organizationId/projectId/repositoryId/workspaceId，guaranteed为空且封闭possible集合不含delivery。已有query保留反例、callback读键→null→direct-await→async拒绝关系保留。端口23个事实、5个有限装配段另加route_activation未知段，`assembly_complete=true`、`end_to_end_complete=false`；不认证DOM／route／event、公开VM可变性或其它port effects。

CPB保护／谓词摘要仍关联15个声明节点、12条认证调用边和3项必要gap。所选目录owner保护范围在显式协议模型内支持，process fence寿命独立；实际deps、collection heap／方法效果及物理资源／协议条件仍未闭合。状态patch不是已执行转换，`facade_to_authority_execution_chain_proved=false`、`interleaving_inferred=false`，没有并发交错裁决。

Rust语言、显式serde／Eq及同impl泛型词法模型没有扩大；既有词法／可信模型前提仍随边与基准见证保存，不解释为编译、宏展开或实际工具链验证。

## 最终正式扫描与冻结基准

| 指标 | CodePatchBay | WinWinCode |
| --- | --- | --- |
| 最终snapshot | `fb9efe4704d83310958712a8b35089f06511d733258c63777e1d93af25bf89e8` | `24997ddb7ac245abb12a7da4387b77d1f605b50e6719e8b131322cfe4f164f31` |
| 状态 | partial | partial |
| 完整解析／纳入文件 | 330 / 333 | 465 / 471 |
| 节点 | 11,085 | 32,407 |
| 调用边 | 60,571 | 171,983 |
| resolved调用 | 23,380 | 16,293 |
| 辅助输入 | 0 | 4 |
| 冻结正向观察重现 | 4 / 4 | 6 / 6 |
| 指定unknown保留 | 2 / 2 | 1 / 1 |
| 配置式有限发现 | 6 | 2 |

原26项仍为10 reproduced、3 unknown、13 evidence_only；36份冻结来源hash与quote均matched，与v0.7比较`changes=[]`。这些是有限人工观察核对，不是功能覆盖率或完整判断通过率。三个Shell未支持文件及六个Rust解析缺口保留；原测试、生成实现等排除范围不隐藏。

最终两库cold均发布新快照，warm复用全部启用语言的前端memo，得到同ID且`created=false`；官方CocoIndex 1.0.25仍以语言整体为粒度，检测每轮full。没有逐文件语义增量、增量检测或性能达标声明。

本轮最终工具身份为 `900090668e899bc07134e5d2c9b73f338f29a4302924247f8aa4e1850bb4a47e`，分析器`static-multilang-8`、检测器`call-rules-7-field-summaries`、schema 2。最终字段摘要为`finite-field-summaries-2`，wrapper为`static-field-contracts-1`；源码身份见[CORE_FREEZE](CORE_FREEZE.json)。

首次正式产物将普通解构误标为新对象复制，已窄修并升字段摘要版本2。旧`a59d…`身份及`46213…/8ceb…`快照保留在[SUPERSEDED_SCANS](SUPERSEDED_SCANS.json)及数据库历史，最终正文／账本只采用重扫后的身份，不改写旧证据。独立审查见[Astra报告](INDEPENDENT_REVIEW.md)。

正式产物：[CPB扫描](codepatchbay-integration.json)、[WWC扫描](winwincode-integration.json)、[CPB汇总](codepatchbay-summary.json)、[WWC汇总](winwincode-summary.json)、[CPB基准比较](codepatchbay-baseline-v8-and-v7.json)、[WWC基准比较](winwincode-baseline-v8-and-v7.json)、[能力账本](capability-ledger.json)、[字段评估](field-assessments.json)及[有限见证](finite-contract-witnesses.json)。[现场来源稿](FIELD_SOURCE_REVIEW.md)和开发观察不算上述自动成果。

## 完整目标仍缺什么

[本轮目标账本](goal-ledger.json)保留五个原claim及30必要义务，并重新绑定最终snapshot、合同／模型、来源hash和实际JSON指针。分类为4个限定子义务支持、19个partial、7个unknown；完整五项均partial，与上一轮完成类别相同。分类是人工评审自动证据的范围映射，不是30项自动义务求解。

| 完整判断 | 本轮具体进展 | 仍缺的必要闭合段 |
| --- | --- | --- |
| CPB重试参数 | P3/P4新增真实局部构造、rest、helper／形参和body-return事实；五字段路径仍未知 | new/existing队列、scheduler／assignment／JSON／inbox／broker对应身份，bridge生产装配与转交、有效预算guard／计数／阶段及完整反证 |
| CPB终态分类 | 既有初始化集合差保留 | 状态生产／投影、具体job与terminal谓词、recover guard、event-store保护及terminal/recoverable政策 |
| CPB同键窗口 | 共享环境／completion迁移保留所选region与谓词关系 | 实际deps、物理资源／collection heap／全写者、guard状态可达及模型推导交错 |
| WWC导航 | 共享迁移保留query/callback/五有限装配段 | 可见DOM入口、route／event到提交的实际关系、opaque前缀／其它port effects、公开VM对象和ambient接缝 |
| WWC Device字段 | 既有封闭对象缺键及guard出处保留 | 真实UI／client装配、command／协议版本／camel-snake运输、Rust dispatcher／authority及Device非空guard与反证 |

下一阶段先稳定不可变抽象状态／对象版本和窄IR公共协议，统一copy时点、alias、按序写入、branch／effect join；这些架构债务尚未实现。随后选一条必要义务闭环，推进记录／消息身份或真正预算读取，避免每个detector复制一套语言语义。功能正确性优先，其次可扩展性，性能最后。

## 交付边界

本轮没有导入／执行／测试／构建目标，没有工具测试套件、浏览器或安装包验证。冷／热扫描与[六类型保存查询](saved-query-observations.json)属于受信静态工具正常使用，不构成目标功能测试通过。源码身份／引用核对和只读仓库状态由交付记录分别说明；不把这些检查当作五项业务判断已完成。
