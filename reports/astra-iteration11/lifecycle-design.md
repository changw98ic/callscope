# 浏览器延迟结果与生命周期的有限源码关系

基准是原 `WINWINCODE_ANALYSIS.md` 中浏览器组合、scope 与 lazy render 段落。本次直接增加静态分析能力，未让另一个模型重新裁定原报告。

实现为 `callscope/lifecycle_ownership_relations.py` 的 `browser_async_lifecycle`，版本 `captured-lifecycle-ownership-relations-1`。注册源码模型为 `browser-continuation-guard-source-v1`；规则仅包含 exact role/file/symbol locators、模型和范围声明，没有期待的 counter、guard、writer 或结论。

## 实际计算

- 用保存源码的哈希认证 CST 与 `LexicalBindings.resolve_identity` 的声明 token，对实际自增 counter、truthy invalidation、abort/close/dispose 调用分别建源事实。声明 token 不是对象身份或当时的值。
- 从 `counter += 1` / `counter++`、实际 `const local = counter` 和保存的已绑定内部 CALLS，计算局部代次 token 作为第几个实参传到哪个确切形参。不会按 `render` 名称拼调用边。
- 识别实际返回 `null` 与 record 的 provider、确切已绑定调用、result 的 `=== null` / `== null` 提前返回，关联正常继续前的上下文拒绝来源。该关系不独立证明身份或 scope 授权正确。
- 从 OR 条件、实际 abrupt consequence 和同一词法声明，识别关闭 token、代次不等与 signal.aborted 的返回守卫。只保留同一 callable 内先前块语句对后续写入的条件支配；不会从相邻源码或另一个分支推导支配。
- 对共享字段赋值和有明确 browser mutator 形式的调用，记录其先前 suspension 和当前有效 guard。RHS/参数内部的 await 也使先前 guard 失去新鲜性。嵌套 callback 没有继承父函数 guard；callback 的实际激活始终未证明。
- 对 closed 分支内对回调结果参数执行 close/dispose 后返回，单列消费补偿。close 调用不代表先前效果已经撤销。

## 有意保留的边界

`all_async_callbacks_guarded_proven`、`all_stale_results_rejected_proven`、`unique_browser_runtime_binding_proven`、`all_resources_released_proven` 均为 false。没有局部 guard 的 callback 不自动归为缺陷；导入页面可能有自己的关闭或结果消费合同。标准 AbortController/DOM 是显式源码模型，未启动浏览器、取消网络请求或验证外部 mount 的效果。

发展查询读取 iteration10 正式保存快照，带旧 snapshot/source/policy 与当前模块 SHA，并检查整个查询期间模块 bytes 稳定；它们不会修改或重新发布旧快照。正式结果由主进程统一冻结新工具和新策略后重新扫描产生。

## 实际保存源码查询

`lifecycle-source-query.json` 已在保存的 WWC 快照 `ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28` 完成。最终模块 SHA 为 `6ee0cf1d1434a17869e7f36e66b9c31649e6fb807fbcad18dabe36c8a326d74c`，查询全程 bytes 稳定；19 个 exact 角色和 graph binding 均可认证，984 个事实、30,852 次 AST 操作，未截断，`analysis_gaps=[]`。

实际计算有 25 个 generation 实参/形参关系、10 个 nullable context 拒绝关系、11 个标准 controller 构造与共享 slot 安装、37 个返回 guard，以及 1 个 settings closed 结果消费补偿。195 个 target/effect-frontier 记录具有同 callable 的有效局部 guard；25 个挂起后记录没有这种局部 guard；97 个初始同步 setup 单列。这些是源码关系计数，不是功能覆盖率、安全率或缺陷数量。

`renderSettings.mountUsagePanel`、onboarding 的延迟 connect、annotation transport 等 callback 保留其真实的局部边界；未将其父 render 的 guard 跨 callback 或 await 继承。settings consumer 的关闭补偿独立记录，不与“所有 callback 均拒绝旧结果”合并。opaque frontier 没有被解释为实际写入，缺少局部 guard 也没有被判为新缺陷。

源码相位按 CST 包含关系处理：`await f()` 的 `f()` 求值不受它自己返回后的 suspension 影响；包含 await 的外层赋值/调用必须等该 await 后正常继续。摘要在 `LIFECYCLE_OWNERSHIP_OBSERVATIONS.json`；其 JSON Pointer 对应原查询事实。三项新规则另通过当前真实 `validate_report_claim` 的数据 schema 验证，自身 Python AST 检查通过；未运行测试或合成夹具。
