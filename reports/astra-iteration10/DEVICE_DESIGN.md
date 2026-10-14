# WWC-02：条件必填字段的完整静态判断

实现入口为 `callscope/device_flow.py`，API 为 `validate_device_flow_rule`、`assess_device_flow`、`analyze_device_flows`。配置见 [device-rule.json](device-rule.json)。配置提供精确角色和协议声明定位器、版本化模型选择以及真实环境条件，不提供传播结论、预计算的缺键、派发关系或 guard 结果。

基准保持 [Astra 原始 WWC 报告](../astra-baseline/WINWINCODE_ANALYSIS.md) 中 WWC-02 的条件范围：clarification update 的完整 spec 没有顶层 verificationCommand，已活动 Device 的非空 guard 因而拒绝；非 Device 仓库回退和 Chat 显式字段是反证。五项义务是实现索引，不替代该报告。

| 义务 | 自动检查 |
| --- | --- |
| D1 | 唯一正常返回、完整 envelope/payload/spec own keys、命令与版本、无未知 spread/accessor/computed key、所选顶层字段缺失 |
| D2 | application 默认 client 的实参、observer/cache 包装、cache 原生 Proxy 实际 own override、动态字面模块绑定、真实 port/VM 属性注入与调用、const 命令返回 binding、实际返回方法、neutral/generated/HTTP 包装实参 |
| D3 | 保存的 TS/generated schema 与 Rust record 路径、唯一命令 discriminator、untagged 候选的不同 discriminator、camelCase/snake_case rename、Option 默认/skip-none、实际 JSON/POST/body/server handler/decoder/family/request 派发 |
| D4 | typed update → serde envelope payload → installed/taken authority receiver → command match/decode/spec、Device target 来自 source session、非空 Option guard、拒绝先于 criterion 使用与 commit |
| D5 | 非 Device 回退、source/grant/授权条件、Chat 显式字段、已有 criterion verificationMethod 与提交对象不同层、已有 receipt replay、scope/actor 授权和 command confirmation |

源码关系保存快照、文件 hash、AST/owner 区间、span hash、模型版本和内容寻址 relation id。实现文件使用已认证 SemanticSources；此前排除的 generated 原文通过独立辅助输入读取和 hash/CST 认证。辅助输入从不制造图函数、CALLS 或将 dynamic call 升级为 resolved。字面 `Promise.all(import(...))` 产生独立 module-member binding，并检查普通 Promise 词法、完整无空洞数组对应及真实 export。

协议模型 `captured-device-json-serde-dispatch-v1` 只处理正常生产的普通 JSON 数据和所选、受提供者认证的 serde 属性。API crate Cargo manifest、workspace Cargo、Cargo.lock 与生成声明都要真实保存；未捕获或不匹配时输出必要 gap。模型说明 JSON 缺键、rename、Option None、skip-none 和 `filter/ok_or_else/?` 的有限规则，未执行反序列化、宏展开、网络或目标代码。

完整位依赖 D1–D5 的全部必要关系、模型适用性和零必要 gap；缺中间 binding、字段、receiver 或 guard 不能写成环境条件。真实条件包括正常无 client override 路径、请求成功到达、前置权限/版本/已有 delivery/revision/source-session/baseline 检查允许继续、不是旧 receipt replay、Device target 已活动。结果不是所有规格编辑的运行保证。

开发查询使用 v0.11 保存图和新捕获辅助原文的独立 unpublished 派生上下文；保存 base_graph_snapshot_id、派生 context id/source hash/policy hash，明确图未重建。它不覆盖 v0.11 历史身份，最终结果须使用新策略的正常全图静态扫描。未运行任一目标、测试、构建或安装。

最后一次开发查询读取9项实际捕获辅助输入，D1–D5全部为supported，必要与分析gap均为空，81条完整自动关系保存在 [device-development-query.json](device-development-query.json)。其中74条来自实现原文、7条来自辅助原文。该数量不是测试覆盖率，也不是额外验收分母。API/domain的serde提供者、TS/Rust/wire版本与字段关系均自动核对；模型没有执行反序列化或宏展开。这里的完整位是原WWC-02的有条件代码判断，新策略的正式扫描与全报告接入由主代理完成。
