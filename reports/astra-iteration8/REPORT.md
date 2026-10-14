# Astra 对照推进：v0.10.1 字段精度修复

版本：CallScope 0.10.1。日期：2026-10-12。

**v0.9的services helper自有字段形状退化已在正式v0.10.1结果中修复；engine的真实runJob实参新增一个有条件的来源形式保留结果。** 三条字段合同共五个评估位置，其中一个为source_form_preserved_when_present，另四个仍unknown。五项原始完整判断仍全部partial，完整目标为0/5。

验收继续采用原[五项判断／30必要义务合同](../astra-iteration4/GOAL_ACCEPTANCE.md)及本轮[目标账本](goal-ledger.json)。全部原定义、条件、反证、次序、required及评审类别保留；账本是manual_review_of_saved_automatic_evidence、automatic_obligation_solver_used=false，不是自动业务义务求解器。原[26项冻结观察](../astra-baseline/capability-baseline.json)和早期报告没有改写。

[v0.10.0第七轮候选](../astra-iteration7/SUPERSEDED_CANDIDATE.md)在最终源码审查中发现内部EvidenceRef内容标识构造缺陷，未作为最终交付。v0.10.1将模块cell写后未知域的guard/kind变更改用规范evidence(...)构造器重算标识，保存新冻结核心并重新进行正式扫描。候选已导出的EvidenceRef复算没有发现碰撞；这是内部构造协议修正，没有以新实现覆盖旧快照。

## 正式修复及其边界

在保存的真实`server/services/engine-runner.ts:155` helper调用中，buildServices正常body-return摘要恢复maxRetries absent、selected shape closed和whole shape closed。其`:85`外层字面对象由实际有序IR状态得到封闭shape及十一自有键：createJob、startPhase、completePhase、completeJob、failJob、blockJob、appendEvent、prepareTask、getPool、getArtifactIndex、providerServices。它没有maxRetries；这不是从原文键名事后补出的封闭结论。

真实`:157` runJob实参在`call argument before callee activation`阶段为source_form_preserved_when_present，selected_shape_complete/source_form_complete均true，来源指向主体形参0的maxRetries。它依赖正常前缀到达及原有普通own-enumerable copy／独立actual Get模型；**field_presence仍unknown，whole argument shape仍false**。这个结果说明所选源码段在字段存在时保留其来源形式，不证明字段实际存在、最初值稳定、runJob激活、运行预算、Promise履约或完整消息运输。Finding仍uncertain，reaching_value_origin_proven、transport_proven、full_functionality_proven保持false。

| 所选正式位置 | v0.9 | v0.10.1 | 保留的限制 |
| --- | --- | --- | --- |
| engine runJob实参`:157` | unknown，selected/source-form false | source_form_preserved_when_present，selected/source-form true | normal-prefix及copy/Get模型；presence unknown、whole argument open |
| queue→agent实参`:1580`的两个分支 | 两个unknown | 两个unknown | actual Get来源仍未闭合 |
| agent return`:487`／`:489` | 两个unknown | 两个unknown | captured cell／copy surface及Promise完成边界仍缺 |
| services helper`:155`的局部返回 | presence/selected/whole unknown | absent、selected/whole closed | 正常body-return源码对象；不认证激活、运行对象或预算消费 |

正式字段来源事实为engine 247、queue 172、agent 590，共1009；这些事实和五个site不是精度、召回率、项目覆盖率或完整goal义务分母。依据为[字段评估](field-assessments.json)与[保存汇总](codepatchbay-summary.json)。

## 实现为何不再丢失这一关系

公共IR仍是字段AST适配器实际消费的不可变状态，没有退回mutable frame、clone或全局epoch。v2新增有来源guard的构造寿命：未暴露普通字面对象parent只免于fallback全heap扩大，真实root、alias、escape、反射、不完整状态或预算耗尽继续产生damage；物化及bind／return／argument暴露前结束保护。join只保留各分支一致的guard，conditional allocation不能获得该保护。

source认证的initialized const cell不可重绑与其对象referent可变分别表达；类型化BindingDomain保存模块live cell的外部词法域，opaque重绑不凭空获得未暴露caller对象。实际callee值、receiver、实参、捕获cell及已暴露域仍参与effects。原始值join的content未知不扩大对象域，TS擦除类型子树不产生运行capture，真实闭包仍读取。ordered spread仍在原时点保存copy ObservationRef，共享child身份、可变性、Get模型及完成边界保留。

这些是通用源码域和状态关系，不按仓库、字段、helper名称或行号设置特例。历史开发来源审查见[精度复核](../astra-iteration7/PRECISION_SOURCE_REVIEW.md)、[IR复核](../astra-iteration7/IR_PRECISION_REVIEW.md)及[来源路径复核](../astra-iteration7/SOURCE_PATH_REVIEW.md)；开发JSON和人工来源锚点没有用于补正式positive；最终独立核对见[第八轮Astra复核](INDEPENDENT_REVIEW.md)。

## 同源码和同策略比较

[v8／v9／v10比较](FIELD_VERSION_COMPARISON.json)认证两库目标source_hash在三版相同，v9／v10的policy字节及policy_hash也相同。因此本轮选定关系改善来自实现修复，没有通过删site、收窄所选段、预填helper键或修改模型条件取得positive。v8仍保留作历史比较；v8／v9策略曾增加预算及CPB独立Get模型，不能把这两版当作相同前提来归因。

最终工具源码身份为7957dad01f30a20b36823058eb245d120074c9f6f11802bd41a55641d8d26e7e，schema 2、分析器static-multilang-10、检测器call-rules-9-field-precision。公共IR为finite-immutable-semantic-ir-2，字段摘要finite-field-summaries-4-ir，wrapper／策略static-field-contracts-3-ir／static-field-policy-v2。预算及导航／原子模块版本保持，身份见[CORE_FREEZE](CORE_FREEZE.json)。

| 正式扫描指标 | CodePatchBay | WinWinCode |
| --- | --- | --- |
| snapshot | 3a987ec8a0ced043379a0e75a6f5932c24982e807e1d252d9b0fc0033183f977 | 9c791af9bf562d6f0f36e09ddeb1f21b4a3445b649064d21ec4d34d33c6abece |
| 完整解析／选入文件 | 330／333 | 465／471 |
| 节点／边 | 11,085／60,571 | 32,407／171,983 |
| 确定绑定调用 | 23,380 | 16,293 |
| 辅助原文 | 0 | 4 |
| 覆盖状态 | partial | partial |
| 配置式有限发现 | 8 | 2 |

两库cold发布新快照；warm复用全部请求语言memo，保持相同ID且created=false，检测每轮full。原26项保持10 reproduced、3 unknown、13 evidence_only，36份来源hash／quote均matched，v10／v9分类changes=[]。三份Shell未支持文件与六份Rust解析缺口继续保留。官方CocoIndex仍按语言整体缓存，没有逐文件语义增量或增量检测声明。

正式依据：[CPB扫描](codepatchbay-integration.json)、[WWC扫描](winwincode-integration.json)、[CPB汇总](codepatchbay-summary.json)、[WWC汇总](winwincode-summary.json)、[CPB v10／v9对照](codepatchbay-baseline-v10-and-v9.json)、[WWC对照](winwincode-baseline-v10-and-v9.json)、[原26项账本](capability-ledger.json)及[有限见证](finite-contract-witnesses.json)。

## 原完整目标及下一步

本轮局部改善对应原义务CPB-01.P4的rest／spread／services返回键证据。P4要求的实际bridge装配、参数转交、完整字段关系和有效预算消费仍未闭合，所以P4保持partial；不能用一个site positive提升整个必要义务或goal。其它四个字段site unknown，P3的normalization／new-existing／scheduler／assignment／JSON／inbox／broker记录运输仍缺。

[目标账本](goal-ledger.json)保留全部五goal／30义务及v0.9评审类别：4限定子义务支持、20partial、6unknown，五goal全部partial、full_goal_acceptance=false。618条递归引用／105个去重JSON pointer绑定正式summary的SHA、snapshot、finding、rule和contract；十个旧索引源码事实按operation／owner／target及保存file/hash/span重新映射并核对，没有只替换旧snapshot ID。

两项既有局部预算仍source_form_complete=true且Finding uncertain；数值域、真实激活／消费、termination、全函数支配和上游预算归属仍未证明。CPB终态仍缺状态生产／job投影／消费guard及event-store反证；同键窗口仍缺实际deps、集合heap／物理资源／全写者及模型推导交错；WWC导航仍缺可见DOM、route／event激活及ambient接缝；Device字段仍缺真实client／协议／跨语言dispatcher及条件guard。10条有限发现不是10个业务bug。

下一步先闭合queue／agent四个unknown site的实际Get、copy surface、captured cell和helper／return／Promise关系，再连接消息／记录身份、bridge装配与具体预算归属。完整目标按原必要关系验收：功能正确与闭环优先，可扩展性其次，性能最后。

## 操作边界

本轮没有执行、导入、测试或构建目标，也没有工具测试套件、浏览器或包安装验证。冷／热扫描及[七类型保存查询](saved-query-observations.json)是受信工具正常静态使用，只读取源码和正式保存快照；这些操作不代表目标功能测试通过或业务正确保证。

