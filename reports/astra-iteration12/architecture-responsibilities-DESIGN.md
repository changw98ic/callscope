# 由真实操作生成有限架构职责解释

本轮基准仍是原两份完整分析报告。新增代码 `callscope/architecture_responsibilities.py`，接口为 `build_responsibility_explanations(snapshot, report) -> dict`。主报告将完整返回值置于 `architecture.responsibility_explanations`。

本模块不读取基准文档，不从目录名、方法相似或规则用途判断职责。`responsibility_operations.py` 负责已保存源码的哈希/CST/声明/调用认证与操作提取，本模块消费其实际结果。既有 Finding/Evidence 可以提供选中范围及来源导航；它们不会替代新操作的真实源位置证明。

## 正文由什么生成

| 实际输入 | 生成的有限解释 |
| --- | --- |
| record construction 的真实字段与表达式 | 该确切声明构造哪些记录字段，字段具体来自何表达式。开放 shape、覆盖与当前值未知保留。 |
| field write、binding initializer/update | 哪个捕获字段或词法 binding 被初始化/更新，更新原式及循环/分支上下文。局部 count 不能冒充持久事实写者。 |
| 已认证 call/argument/formal | 实际实参位置与确切接口/形参；未绑定 call 保留源形式，不指定唯一实现。无显式实参调用单列。 |
| 显式字段投影、复制与 return | 该记录如何组织输入或提供结果来源；不把同名变量或源码邻接连成数据流。 |
| 条件分支内的 return/throw/Err | 条件及实际提前退出内容；普通 return 可能是成功、复用或拒绝，不猜业务含义。 |
| 确切 binder/AST 包含/已绑定形参关系 | 有证据的构造到实参、参数到字段、return 来源交接。normal source order 单列，不新增因果/事务连接。 |

每个 exact declaration 有具体 `summary`、实际 `statements`、`derived_work_roles` 和所有操作引用。工作角色由操作类型生成，例如构造记录、字段更新、实参接口消费、条件退出；不是按函数名称贴业务责任。

## 进程、持久消息与普通调用分开

`computed_source_contract_seams` 复用既有完整 goal 中真正计算出的 `production_assembly` 和 `channels`：有限动态 import 路径、标准 Node spawn 导入与 argv、direct/broker receiver 分支，以及 queue/inbox/broker/assignment attempt 的条件交接。每条仍指向原 `judgments/.../obligations/.../evidence/...`、原 Finding/Evidence、实际源位置与注册模型条件。

它也消费 `finite-conditional-event-lineage-publication-source-v1` 已生成的状态/发布关系，但仅在 `scoped_source_supported` 和 `source_statement_relation_closed` 都为真且确有关系 witness 时。正文是该模型依据真实 guard、事件字面字段、共享源字段、选项和接口计算的 `statement`，下钻指向原 pattern、source facts 和 witness。较早 review-bundle 分支、可空通用 callback、正常 await 完成条件及远端后置条件未知仍保存在同一原关系中。

WWC 原已读有限协议句还有一条实际模型接缝：原 `static-device-spec-protocol-flow-1` adapter 的支持 obligation 已保存 generated TypeScript 字段、Serde rename/default、JSON 请求记录、Server 同路径解码和 typed dispatch。解释器只在该 adapter 与报告/快照身份一致、`captured-device-json-serde-dispatch-v1` 模型版本和 accepted 证书有效、实际 obligation supported/complete 且无 gap、六类关系各唯一并列在该 obligation 的 relation IDs、模型 record/path/type/field 来源一致时生成 `finite_generated_json_serde_message_source_relation`。所有 Finding/Evidence、model、obligation 和 relation 指针由实际 enumerate 得出，不固定数组号，也不把两个相似接口名字连起来。相关 generated 原始支持仍是 `support-input-derived`，不升级为实现。成功消息/普通 JSON/Serde 条件原样保留，网络成功和新增 CALLS 均为 false；并不声称所有 HTTP query/WS 都经过这次 codec 分析。

这不是从 `spawn`、`writeInbox` 或某个 HTTP 方法的名称猜效果。消息/codec/进程接线不新增普通 CALLS；执行结果、交付收尾、持久消息与队列投影不合并为一个成功。所选 shared 接口复用只在多个确切声明实际调用同一已绑定 callee 时产生，未因广泛复用推断“上帝对象”。

## 来源下钻与共享索引

完整操作只保留一份。`source_location_index` 保留原哈希、span 与解析坐标；`evidence_reference_index` 保留 Finding/Evidence/fact/原 JSON Pointer。操作使用薄 location/evidence ref；正文和关系用相对 `/operations/{index}` 的指针，再定位到操作的来源与共享索引。`operation_pointer_scope` 和 `source_index_pointer_scope` 明示相对本职责对象，而非顶层报告。

`navigation` 的原章节/区域标签只便于检索，不是职责断言或覆盖分母。找不到相应实际操作就没有该正文；不会按标签补造缺失子句。

## 展示范围与分析边界

每个声明最多展示 24 个具体操作句，至少保留实际出现的每种操作，全文操作及关系均可下钻。`presentation_truncated` 单列展示省略；分析器预算、来源缺口、未知调用和未闭合字段不被删除。根报告另显示 guard 与完整正文引用。

实际 WWC 读回曾发现首个普通调用可能只是 `to_owned` 或 `Err`，掩盖同一声明中的已绑定接口。当前选句按真实目标绑定、目标是否也有选中声明、跨文件形参、真实记录/参数关系及不同字段/条件增加结构多样性；不使用接口的业务拼写、目录或原报告角色评分。摘要至多列 8 个实际句，可包含第二个不同的已绑定选中接口。源码展示仍按源位置排列；选句优先级不新增调用、因果、授权或重要性判断。

当前接口不宣称唯一事实所有者、全部授权、所有路由、任意堆别名、真实存储/远端成功或完整恢复。目标是原已读有限职责、字段/记录及接口关系的具体说明，不引入全项目安全验收。

发展查询使用旧 v13 保存源码和明确的新数据选择/工具版本；附各模块 SHA 及稳定性，不冒充正式 v14 结果。全部查询串行使用 common flock，不运行目标、测试、构建或合成夹具。最终是否已承接每个原有限子句，将按真实发展/正式报告的具体正文及证据核对，不以操作数量或新版本号判定。
