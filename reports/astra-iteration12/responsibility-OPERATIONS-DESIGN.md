# 有限职责操作 API 与证据域

实现为 `callscope/responsibility_operations.py`，入口 `extract_responsibility_operations(snapshot, report) -> dict`。`snapshot_identity` 的三个精确键是 `snapshot_id`、`source_hash`、`policy_hash`，须与输入报告一致。原报告只是范围基准，不是运行时输入或答案；源码只来自 `SemanticSources` 已认证的保存文本。

当前提取形状针对这两个库中的 JavaScript/TypeScript 与 Rust CST，非所有语言或所有表达式的语义模型。显式 return/throw 和条件出口属于本轮形状；不能据此声称已枚举全部 Rust 隐式 tail return、异常路径、宏展开、动态对象语义或任意语言的全部副作用。其他语言或新 CST 形状应通过独立源适配扩展，不能借用函数命名填充操作。

来源选择使用报告 `functional_chains[].source_scope.selected_definitions`，并读取原判断对应的保存 policy 中 `{file,symbol}` 定位器。选择上下文的 Finding/Evidence 及 JSON Pointer 标记为 `reference_role=selection_context`、`old_finding_proves_new_operation=false`。新操作的实际证据来自其源码 hash/span/CST/词法声明及已有调用绑定；不能借用旧 goal 的通过状态认证新操作。已有 source fact 的位置再次核对原文件 hash 和 span hash，匹配才作为独立来源引用。

操作固定为十一类：

| operation_kind | 限定的实际来源 |
| --- | --- |
| record_construction | 对象或 Rust struct 的实际字段构造与固定/开放形状 |
| record_field_projection | 字段初始化值引用的实际词法根与成员路径 |
| record_copy_projection | 捕获的 spread/base-copy 表达式；不保证当前复制面或保留 |
| binding_initializer | 普通真实局部声明的初始化值；不从变量名猜业务含义 |
| binding_update | 同一捕获局部 binder 的赋值、增量或更新尝试；不证明次数/终止 |
| field_write | 显式字段赋值/更新尝试；不把 opaque 方法当成已知写存储 |
| call_argument_transfer | 实际 callee/receiver/实参位置；唯一已绑定内部目标才保存形参来源 |
| protocol_literal_field | command/query/schema/tag 等实际字段的字面量或枚举源码；不证明 wire |
| guard_rejection | 条件分支里的显式 return/throw/Err-return 源码；不把所有 return 当成业务错误 |
| return_transfer | 捕获的返回/抛出表达式；不保证 async 履约 |
| normal_source_order | 同一捕获 block 的语句位置先后；不是值流或因果边 |

每条操作包括 `id`、`operation_kind`、`actual_owner`、`source_locations`、`source_evidence_refs`、`operands`、`subject`、`guards`、`source_order`、`relationships`、`limitations`。`actual_owner` 使用真实最近 callable 的 file/symbol/graph ID/span；嵌套 closure 单列，未认证图声明保持 source-only。源正文只保存短片段并标记截断；不复制旧 source_facts、AST 树或大块 function body。完整来源由原 Finding/Evidence/JSON Pointer 和 source span/hash 下钻。重复位置集中于 `source_location_index`，完整旧来源上下文集中于 `evidence_reference_index`；操作保留可展示的薄 anchor 与相对索引 Pointer，职责解释对象原样保留这两个池。

通用 operand 含 `source_text`、`node_kind`、`location`、`source_path`、`binding`、`member_path`；不可认证词法根时 binding/path 为 null。`record_fields` 的元素含 `name`、`source_text`、`source_path`、`binding`、`location`、`closed`。call 另含 `callee`、`receiver`、`argument_index`、`argument`、`target_parameter`；无实参调用保留 index=null，不虚构输入。

callee 的 `binding_state` 只取 `authenticated_internal_call`、`captured_call_site_unknown`、`captured_source_only`。只有第一类同时拥有真实 `authenticated_call_edge_id` 和 target ID；其余只显示捕获接口源码及真实未知原因。模型不新造 CALLS、跨语言连接、数据库效果、全局唯一 owner 或授权结论。

显式 relationships 使用 `from_operation_id`、`to_operation_id`、`kind`、`binding_state`、`conditions`。直接字面记录实参由同一 AST span 相连；局部构造与后续实参由同一 declaration ID 关联，但明确未排除覆盖和 heap effects；字段初始化和返回亦保存其真实来源。`authenticated_argument_parameter_projection` 只在已有认证 CALLS、确切普通形参 binder 和所选 callee 内真实引用三者都成立时关联，不证明激活、当前 heap 值或运输。`normal_source_before` 只表示顺序，不补值来源或消息运输。

职责解释由 `architecture_responsibilities.py` 消费以上实际操作生成。目录、函数命名和原报告角色标签只用于导航，不参与“谁负责什么”的事实判断。发展查询使用 v13 保存快照，common flock 串行加载；记录模块字节身份和稳定性，不把发展查询当成后续正式扫描结果。本工作不执行/导入目标，不测试、构建、安装或使用夹具。

可选 `supplemental_selectors` 只供开发查询把新 data-only 定位器关联到旧保存源码，默认空。其来源明确标记 `development_selection_context`、定位 artifact hash/pointer 和 `not_saved_snapshot_policy`，没有借用旧 Finding 的证明地位。正式构建从本轮已保存 policy/report 范围选择。非 CST 的文档事实（captured-document-text）单列计数，不尝试当成代码 CST 或记为代码位置认证失败。
