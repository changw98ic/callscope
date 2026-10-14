# Astra 对照推进：v0.7 静态语义关系

版本：CallScope 0.7.0。日期：2026-10-12。

本轮已完成两个真实仓库的正式冷／热静态扫描，新增可追溯的导航查询消费链和查重保护范围分析。五项完整判断仍有必要关系未闭合，尚未达到原定完整目标。具体验收采用[五项合同](GOAL_ACCEPTANCE.md)和[目标账本](goal-ledger.json)，不以调用样本、AST锚点或Finding数量代替。

## 本轮自动生成了什么

**WinWinCode 导航。** 看板 `newTask.href` 的真实实参，经唯一 `surfaceHash → scopeHash` 绑定、形参、字符串与 URLSearchParams 模型生成查询键摘要：可能键为 organizationId、workspaceId、projectId、repositoryId，必有键为空；封闭摘要不含 delivery。键来自保存 AST 的冻结数组与实际 set/delete 分支，不由配置填写。

分析继续追到生产 factory 实参中的 deliveryContext、当前导航 hash 的查询投影、实际 `get('delivery')`、缺键返回 null、OR guard 为真、回调正常返回 null，以及端口 create 中真正的 await 和空上下文拒绝。lookup 的 receiver、ambient 来源和 factory context 必须一致；常量空查询不能接到导航来源上。create 为 async 方法，此处对应拒绝的 Promise，不称为同步调用已抛出。

正式发现 `e889ad8ba3543e2359bed2a9` 保存82个来源事件、8个真实声明节点、4条认证调用边。有限端口装配同时生成23条事实，闭合正常 boot、生产 factory 分支、同一 taskPort 注入、VM 的 options.port 捕获及返回 submit 方法内的 create 使用。显式动态 import 的装配是独立版本模型，旧 CALLS 仍为动态。

真实 `homeDecisionHash` 调用提供了已有 delivery query 的反证：同一 builder 正确保留该键；四个 scope 键仍只是可能存在。缺键结论只涉及所选入口和声明的正常前缀、导航／hash稳定条件。正常路由 dispatch、事件接线、未知前缀返回及效果、其它端口方法、公开 VM 对象可变性等10项gap保留。`source_condition_chain_confirmed=true`，`full_functionality_proven=false`，Finding仍为`uncertain`。

**CodePatchBay 查重。** 工具从 facade 的预查、选择、早退和写入点，authority 的 find／复用／push，以及 wrapper 和目录 owner 锁的源码，生成有限保护关系：取得结果与唯一 true 返回、初始 false／唯一 true 写入、失败即终止的 guard、回调完成链、fresh read → await callback → 条件 save → release attempt。process fence 的范围限于取得和释放回调；目录 owner 模型覆盖中间队列操作。保护协议正确性和物理资源身份不是运行证明。

从同步、正极性的 for-of 选择谓词及认证 Set 初始化，得到外层非五个终态的选择域；内层 source conjunction 只接受 pending。终态成员 completed、failed、cancelled、canceled、archived，以及 pending 都由 AST 提取。key 结构也由源式提取：权威 key 多读取 description 与 metadata.originJobId。此为字段结构差异，`semantic_key_equality_proof=false`，不能把它升级为一般运行键不等。

正式发现 `480f1137cb02e8b96438b1b1` 包含15个声明节点、12条已认证调用边、两处真实状态 patch 见证及反证。`authority_region_state=source_backed_protocol_model`；所选 facade 检查位于所选 authority callback 外，这不证明没有其它外层保护。默认动态依赖装配、entries 堆对象身份／getter／方法效果及外部协议条件仍是三个明确gap。未计算并发交错，`facade_to_authority_execution_chain_proved=false`、`bounded_interleaving=false`，不能宣布完整竞态或任意双提交必然重复。

## 证据与扩展边界

新增五个模块：共享 [semantic_sources](../../callscope/semantic_sources.py)、[lexical_bindings](../../callscope/lexical_bindings.py)，以及 [navigation_analysis](../../callscope/navigation_analysis.py)、[port_wiring](../../callscope/port_wiring.py)、[atomicity_analysis](../../callscope/atomicity_analysis.py)。共享层认证原文、hash、语法投影、声明身份和完整调用 byte span；嵌套调用同起点不再被误判为两条候选。

声明唯一、值稳定、运行值与资源身份分别表达。默认解构只识别绑定左侧，默认值和潜在写入另计；generator、未 await 的 async 返回和普通对象返回不混用。标准模型核对可见遮蔽、alias／computed write／escape；未知效果不能生成封闭缺失负证。模型版本和整体工具源码身份进入正式快照。

策略只提供来源角色、固定模型、合同意图和条件，不提供预计算键集、终态集合、保护区域或交错。源码事实、可信模型、策略声明、未解决的分析段和反证分开保存。独立 callback、import、保护和词法声明关系保留在证据中，不伪造普通 resolved CALLS；热力图关联的是实际声明节点。

原有三个有限合同也保留：CPB 初始化集合缺 superseded、pipeline parsed.retries 与 worker 新对象 maxRetries:3 的来源形式差异、WWC spec 返回对象缺 verificationCommand。五条配置式发现是有限评审结果，不是五项完整缺陷已被自动裁定。

## 正式静态扫描与原基准

| 指标 | CodePatchBay | WinWinCode |
| --- | --- | --- |
| commit | `4f2d2eca31d90b0122db1c1429dd365672db2393` | `da407e4f3df3719718b23bd8913b73fe3ff73857` |
| v0.7 snapshot | `4866cb471f54673322145c50750546b90077746e9fd83c3f58221aeafe92962a` | `10bcd33b59b4eb76f67eaabf825782cb3434d8a9c6909c106036a4c82db13b3e` |
| 状态 | partial | partial |
| 解析文件／纳入源文件 | 330 / 333 | 465 / 471 |
| 节点 | 11,085 | 32,407 |
| 调用边 | 60,571 | 171,983 |
| resolved调用 | 23,380 | 16,293 |
| 显式辅助输入 | 0 | 4 |
| 冻结正向观察重现 | 4 / 4 | 6 / 6 |
| 指定unknown保留 | 2 / 2 | 1 / 1 |
| 配置式有限发现 | 3 | 2 |

解析覆盖约99.1%／98.7%，仅指明确纳入范围的文件能够解析；这不是功能覆盖率、检出率或一般调用解析率。排除测试、构建、生成实现等范围继续保留。原26项结果为10 reproduced、3 unknown、13 evidence_only，其余状态为零；36个冻结源hash及quote均匹配，与v0.6比较没有观察分类变化。Rust同impl generic、显式serde／Eq模型、字段动态调用未知均未修改。

两个仓库 cold 都创建新快照，warm 复用全部已启用语言、得到同ID且created=false；官方 CocoIndex 1.0.25 的缓存粒度仍是完整语言 bundle，检测始终全量。没有宣称逐文件语义增量或已经满足性能指标。

统一工具身份为 `d0b2f76e6f8c398758e0d3ba2b8f0d583876de636062b758ac94e216afcbe49c`。分析器 `static-multilang-7`，检测器 `call-rules-6-semantic-relations`，GraphSnapshot schema仍为2；基准核对器仍为`frozen-static-baseline-1.3`。冻结基准SHA256仍为 `16b4b05c8818fa1eecf396132ebe2ea29a8f0068801165f0649da379d9041dd7`。各新模块冻结身份见 [CORE_FREEZE](CORE_FREEZE.json)。

正式产物：[CPB扫描](codepatchbay-integration.json)、[WWC扫描](winwincode-integration.json)、[CPB汇总](codepatchbay-summary.json)、[WWC汇总](winwincode-summary.json)、[CPB v0.7／v0.6](codepatchbay-baseline-v7-and-v6.json)、[WWC v0.7／v0.6](winwincode-baseline-v7-and-v6.json)、[能力账本](capability-ledger.json)、[五条完整有限见证](finite-contract-witnesses.json)、[独立复核](INDEPENDENT_REVIEW.md)。开发观察明确使用旧v0.6保存源，不代替上述正式v0.7发布。

## 完整目标与后续方向

[目标账本](goal-ledger.json)保留五个原判断及30项必要义务。新增导航来源、guard和装配关系，以及查重保护／谓词关系，补上了此前需要人工连接的部分；完整参数运输和预算消费、终态生产与恢复保护、默认装配与并发交错、实际路由／事件接线、跨语言 spec 协议和Device guard仍需继续闭合。

可扩展性优先抽取版本化的内建环境／效果审计与有限 completion／value 摘要协议。本轮共享源码和词法层已有实际作用，三个检测器仍重复维护部分标准语义护栏；不能每新增来源选择器就再复制一份判断逻辑。随后按实际未闭合关系推进字段、路由和消息模型。功能正确性优先，其次可扩展性，性能最后。

## 交付核对

正常[保存查询](saved-query-observations.json)读取新发现、当前能力目录和保存源码；界面仅新增两种发现的中文类型标签，未进行浏览器验证。工具Python和界面JavaScript做静态语法核对，报告与文档做本地引用核对，身份及范围见[交付记录](verification-summary.json)。两个目标的只读状态见[仓库记录](target-state-observations.json)。

全程没有执行、导入、测试或构建目标，没有沙箱、工具测试套件、浏览器或安装包验证。冷／热扫描与来源核对均为纯静态工具正常操作。
