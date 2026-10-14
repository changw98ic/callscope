# 原 WWC 报告主要功能链的源码扩展

[wwc-additional-report-claims.json](wwc-additional-report-claims.json) 只声明9条 `guarded_call_sequence` 的文件、精确声明身份、有限模型和边界；没有配置步骤顺序、调用目标、谓词值、请求字段或预计算结论。主实现复用 `report_chain_analysis.py`，从保存源码自动生成调用实参、binding、guard、写入尝试、Result `?` 和条件性的顶层语句顺序。

覆盖原 [WINWINCODE_ANALYSIS.md](../astra-baseline/WINWINCODE_ANALYSIS.md) 主要静态功能链2、3、4：Chat实际请求构造与公开 create 方法、remote/managed入口、共享 Worker 构造、typed control/dispatch/start、Production adapter 打开 embedded Kernel、adapter 持久 intent 后的精确 turn reconcile，以及 Kernel create_session、普通 submit_turn、reconcile_turn_exact 三个不同接口。

Worker 泛型 `self.codex` 调用保持其原图绑定状态；生产 constructor 的源码实参不是全局唯一 implementation CALLS 证明。失败、重放、scope/profile/capacity、checkout及资源收尾分支分别留在证据中；未证明所有资源在所有故障点回收，也未做崩溃一致性演练。

三个 Kernel API 的正常源码都把 async block 传给 `Self::guard`。接口原文和 block 中的 start_thread、start_or_steer_turn、inspect_durable_turn 是可保存的源码事实；当前只分析顶层语句顺序时，外层只有一个statement，不能借增加配置角色伪造已闭合的 future 激活或运行顺序。该限制属于分析器能力；不能解释为 Kernel 未实现。可由主实现单列真实 async-block 结构与内部条件顺序，同时保留 future polling、opaque adapter 和 wrapper 边界。

worker main 的原图声明带 `attribute_macros_unknown`。新 reader 保留完整已认证 AST body 和明确的 graph-binding gap；不因此丢掉入口和 constructor 原文，也不把 CALLS 升级为确定绑定。宏展开和真实启动均未执行。

所有 locator 使用正常保存源码查询认证，结果见 [wwc-additional-report-claims-query.json](wwc-additional-report-claims-query.json)。该文件是新分析器对 v0.11 保存源码的未发布查询，不覆盖历史报告或策略。正式新策略扫描由主代理完成；此次仅新增配置与说明，没有改目标或已有 core，也没有执行目标、测试、构建或安装。

最后一次查询9条声明定位规则、17个源码角色均精确认证，selector gap为零；保留880条完整自动事实。Chat定位到内部真实请求构造 `createChatDeliveryCreator.create` 和公开返回方法 `createChatDeliveryCreator.<object@321:9>.create`，包含133条请求/实参/条件/顺序事实，避免用外层factory的6条普通构造事实替代真实请求链。Typed dispatch、adapter打开Kernel、adapter持久化/精确turn和Chat的条件源码结构为supported；两条worker入口/构造行保留图绑定gap，三个Kernel wrapper API保留只有一个外层statement的能力边界。原报告的generic/Codex和future activation限制没有删除或升级。
