# WWC-01 完整静态条件判断

日期：2026-10-13。此轮以原 [Astra WinWinCode 分析报告的 WWC-01](../astra-baseline/WINWINCODE_ANALYSIS.md) 为功能基准。既有 [七项义务](../astra-iteration4/GOAL_ACCEPTANCE.md) 作为实施索引保留，不增加浏览器、一般 JS 完整性或全 UI 验收要求，也不修改原五目标、三十义务和二十六项历史基准。目标源码只作为捕获数据读取；没有执行、导入、构建或测试 WinWinCode。

新增 [navigation_completion.py](/workspace/callscope/callscope/navigation_completion.py) 提供 `validate_navigation_completion_rule(rule)`、`analyze_navigation_completion(snapshot, rule)` 和正常批量入口 `analyze_navigation_completions(snapshot, rules)`。独立 [新规则](navigation-rule.json) 选择来源角色、需要的查询键和有版本的有限模型，不提供实际绑定、路径、返回结果或守卫结论。既有导航规则及报告保持原样。

| 义务 | 自动连接的必要证据 | 真实条件与边界 |
| --- | --- | --- |
| N1 | 选定 href receiver 的声明身份；真实 element helper 调用、实参/形参 tag 和 createElement 返回节点；anchor→append→同 formal root 的 DOM 构造链；实际 workRoot→看板→My Work→renderHome 安装；链上 hidden 写入；字面 seed | 源码公开 DOM 组合，未观察 CSS、浏览器绘制或用户点击 |
| N2 | 复用正常导航分析生成的 surfaceHash/scopeHash 实参、返回、URLSearchParams receiver 和 set/delete/serialize 事件 | 有版本的标准 URL 和 JS 模型；未知调用/写入不能编造负证 |
| N3 | possible/guaranteed 键域和封闭性；规则必需键与 actual possible 集合差异 | 四个 scope 键可以缺省，不推断必定存在 |
| N4 | 原正常 boot、strict undefined 分支、真实工厂、callback/formal/capture、返回 create 到 VM port 关系；actual VM result const→page actual model 字段；literal import namespace 模型；实际 form 构造/安装与 submit 注册 callback→同 model.submit；源码所见 model 写入和裸别名/逃逸审计 | DOM 事件在已挂载页面上触发；标准模型排除外部方法篡改，不保证某次事件发生 |
| N5 | 原真实 ambient hash→routeParameters→get→null→callback await 结果；返回 create body 唯一前置 await callback declaration、直接 abrupt throw guard、其全部 command 调用严格在 guard 后 | async body throw 是 Promise rejection；结论仅是该 create 的提交拒绝，不说所有 HTTP 或授权请求均未发生 |
| N6 | 实际 subroute selector 的 hash path projection→guard return；实际 performRender selector/result/branch/injection；实际 clientSurfaceFromHash 参数、冻结 source catalog、find 谓词和 first match→outer surface id guard | 导航及读取稳定、授权/生命周期允许挂载、表单前置条件满足是明确环境适用条件；未连接的代码段仍为 gap |
| N7 | 已有有效 delivery seed 的保留反证；nondefault seed 分支真实 alternate factory 及其返回 create；Chat 独立 createRequest 构造与自身 deliveryId 来源；手工有效 URL 的范围排除 | 不证明 fake/Chat 总成功；不泛化所有任务创建失败 |

每条新事实带 snapshot、source hash、原始 byte/span/hash、语义 parse 身份、输入关系和提取器版本。真实 source CALLS 与 literal import 装配模型分开保存，后者不创建或重写快照 CALLS 边。未知/来源失效、节点和事实预算都阻止完整判断。正常 API 只接受快照和规则，始终从保存源码重新生成关系，不能传预填的 prior source facts。

既有局部导航分析的 raw gaps 在 `navigation_source` 原样保留。`prior_local_gap_dispositions` 逐条说明新增源码关系已闭合的缺段、真实平台条件及不属于所选 null 拒绝判断的其他行为。未识别的旧 gap 仍进入必要未知；不会通过清空旧证据或统计折算宣布完整。

批量入口保存七条 `status`、`complete_assessment`、`full_goal_supported`、`conditions`、`refutations`、`necessary_gaps`、原 claim 和推导判断。只有七义务全部支持且必要 gaps 为空，才输出 `scoped_static_judgment_reproduced`。局部键缺失、多个 locator 命中或有限装配已完成不单独升级为完整。

注册模型 `dom-anchor-append-listener-1`、`js-hash-path-strip-1`、`ordinary-source-method-invocation-1` 是明确普通 DOM/JS 源码关系模型；模型实现身份、浏览器事件执行与部署均未运行验证。额外 source query 使用完整历史快照和相同真实源码，串行获取 source-query 锁，避免多个大快照加载同时占用内存。

本候选已通过正常保存源码查询，原报告 WWC-01 的七段索引均已支持，必要 gaps 为空：公开看板 seed 的 possible keys 只有四个 scope 键；默认 boot 选择真实生产端口；该端口实际 callback 从当前 URL 读取缺失的 delivery 并返回 null；真实 create 消费 await null，两个 command 调用都在 abrupt guard 之后。实际 form/VM 接线及 valid seed、fake alternate 和 Chat 独立构造反证一并保存。

[候选完整查询证据](NAVIGATION_PREFREEZE_OBSERVATIONS.json) 绑定历史 WWC snapshot `2b298f494c99d0f0040f7a8b856421813066caa21d7d6d26d36bb573d41626be`。模块 SHA-256 `ba6250f5eb52e1f43a44e28d2a0f5afd06fdceffcc0aa1c4ea37d567c1277d5e` 在查询前、后和此记录时一致。结果包含 11 个新 source facts、10,783 个完整枚举 AST 节点和旧 local gaps 的逐条 disposition。整套开发工具同时仍有其他模块变更，故 `query_core_bytes_stable=false`；这份候选证据不能当作整个最终版本的冻结证书。统一冻结后的正常扫描/注册入口由主代理完成。
