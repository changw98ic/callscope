# 所选消息与记录身份关系

实现入口为 `callscope/message_identity_relations.py:analyze_pattern(analysis)`。输入是 report-chain 引擎已经认证的保存源码角色，不读基准报告正文，不读目标工作树，不导入或执行目标代码。原 WinWinCode 报告用于选择要建模的源码范围，不提供答案、字段路径或成功状态。

`messages-rules.json` 将范围拆成三个独立条目：Chat 保留请求、Worker/adapter 记录、outbox/ack 关联。每条规则只有源角色定位、模型注册和描述性适用范围。真实字段、赋值、复制、调用实参、enum arm、SQL 参数位置均从捕获 CST 计算。

## 通用基础

- TypeScript 使用现有词法绑定器的 declaration identity，不把当前 heap 值稳定性混入身份。
- Rust 处理捕获的普通参数、顺序 shadow、局部 tuple binder、enum arm binder 和显式 closure 参数。没有宏展开或任意 trait 分派推断。
- 字段路径由已认证根声明加静态字段组成。借用和所选 `clone`/`to_owned` 记录为普通生成数据的条件复制模型，不等于任意 trait 实现都保值。
- 对象和 Rust struct 字段逐项保存来源；未知 spread、重复 key、动态 key 保留开放形状。不会因字段同名而合并根声明。
- 已存在的唯一 CALLS 绑定可建立实参来源。图未绑定时，只允许有限同模块普通函数声明关系，并记录其未展开宏和未激活边界；不会修补 CALLS。
- `params!` 仅按捕获 token tree 的顶层参数位置读取。SQL 只解释选定字面量、列与 `?N` 对应关系，不展开宏、连接数据库或执行语句。

模型为 `finite-captured-record-message-identities-v1`；SQL 条目额外要求 `captured-literal-sql-positional-bindings-v1`。两者都以所选正常源码关系为证据域，不是运行保证。

## Chat 条目

计算初始 `attempt` 记录赋值、`currentAttempt` 的实际 declaration alias，以及从 `createRequest.payload.deliveryId` 提取的局部字段。三个 `client.command` 实参须来自同一个当前尝试根的 `createRequest`、`itemsRequest`、`startRequest`。后续 Delivery 字段投影须使用前述局部绑定。

WorkItem builder 须有实际认证调用关系，其输出字段按输入投影保存。后续请求赋值的分支条件以及 requestId 比较均保存具体源码。请求身份彼此独立；共同 delivery 字段没有被合并为相同 requestId。保留的是条件请求重用结构，不能据此保证网络、后端提交、自动重试或所有 Chat 命令成功。

## Worker/adapter 条目

typed `JobDispatchMessage` 的 arm binder 和消费者实参使用同一捕获 binder。`accept_dispatch` 中 `from_dispatch(dispatch)` 的实际结果局部绑定与后续 `start_dispatch(dispatch, run_key, ...)` 实参单列联接。

`CodexRunKey` 记录的四个字段须来自同一个 dispatch 根的 job/lease 投影；`CodexThreadStart` 的 job 和 lease 须同根，workspace/workspace revision/worker session 须来自同一 prepared 根。adapter 的实际记录保留 Job、lease authority、canonical thread、Kernel session 等不同字段来源；没有把这些身份折叠为一个 `session_id`。

profile 条目仅关联传入 Job 的 `execution_profile` 与选定配置消费者；不承诺所有 provider/model/permission 设置。`session_for_thread` 的 `Option.map` closure 来源单列，不提升为已执行回调。submission intent 写入、persist 调用、exact reconcile 调用的正常源码顺序保存，但不声称做过崩溃一致性验证。

泛型 `self.codex.ensure_thread` 保持上下文接口关系。单个生产候选不被写成整个泛型类唯一的运行实现，且没有推断全部工作区、租约或故障收尾路径。

## Outbox/ack 条目

从实际 enum arms 提取 request 和 response 的 Family、同一 correlation helper 以及有序字段 tuple。只对 binder 闭合、相同 Family、有序字段投影一致的条目给出 projection agreement。这个关系不假设两条线上消息的字段值相等；字段值是否命中仍由生成 correlation key 和 SQL 消费者决定。

额外关联 message→Serde encode→frame 局部绑定→metadata(message, frame)→SQL 的 delivery/family/correlation/frame 列参数，并关联 response-target 返回 tuple→DELETE 的 Family/key 位置及 acknowledgement-required 条件。物理事务成功、外部 ack 真实性、所有消息 Family、sequence 到 ack_sequence 的值关系、Outcome helper 的间接 tuple 展开均不由本条目保证。

## 核对方法

`query_message_sources.py` 在公共文件锁内逐条查询 v12 已保存快照，输出 `messages-source-query.json` 和 `messages-query.log`。它记录 snapshot/source/policy 身份及查询时模块 SHA256；明确标记 development query、未保存新规则、不是 v13 正式结果。之后由 root 统一冻结新工具和策略并正式扫描。本工作没有测试、构建、安装、目标 CLI、沙箱或夹具。
