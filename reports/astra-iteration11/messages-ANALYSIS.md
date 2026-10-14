# 消息身份的实际静态分析结果（开发查询）

本结果来自 v12 保存快照 `ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28`，使用新增消息关系模块，尚不是 v13 正式扫描。查询前后模块 SHA 相同：`6f6da497d4554ea8acb6c162330d5b84bd59fd05a5e2ed89266f9c6ef3d74b4b`；`query_core_bytes_stable=true`。

| 所选条目 | 源关系支持 | 源事实数 | 分析缺口 | 保存 JSON 指针 |
| --- | --- | --- | --- | --- |
| wwc-report-chat-retained-request-identities | True | 90 | 0 | `/results/0` |
| wwc-report-worker-adapter-record-identities | True | 353 | 0 | `/results/1` |
| wwc-report-outbox-ack-correlation-fields | True | 120 | 0 | `/results/2` |

这些条目是原报告具体段落的有限源关系，不是三个新缺陷、全仓库功能覆盖率或全文完成比例。原两份完整报告仍是范围对照依据。

Chat 已从捕获赋值关联 `attempt`、`currentAttempt` 和 deliveryId：三个发包实参来自同一当前尝试记录的 create/items/start 字段；后续 Delivery 投影和 WorkItem builder 的实际绑定被分别保存。不同阶段 requestId 保持独立，后续响应的 requestId 比较及各次赋值条件也保存。结论是所选请求保留结构存在，不能保证后端成功或任意自动重试成功。

Worker 已关联 typed JobDispatch arm 的真实 binder、from_dispatch 的局部结果和 start_dispatch 实参；CodexRunKey 的 job/attempt/fencing/digest 投影同根，ThreadStart 的 Job/lease 同根，workspace/revision/worker session 来自同一 prepared 记录。adapter 所选 StoredRun 与 binding 分别保留 canonical thread 和 Kernel session。execution_profile 被传给选定配置消费者；StoredRun.submission_id 的分支 tuple、persist 的同一 run-key 和 exact reconcile 的实参分开保存。泛型 Codex receiver 仍是上下文接口，没有被提升成全类唯一目标。

Outbox 已抽取七组 request/response correlation 字段域一致关系：ModelOpen→首个 ModelChunk/特定 ModelAck、Action request→receipt、Approval request→decision、Input request→response、Register→result、Heartbeat→ack。每组保留实际 Family、arm 条件及有序字段。它们不假设两条线上消息的值相等。另已关联消息编码的 frame 局部绑定、metadata 输入、INSERT 的字段/字节列参数，以及 response-target 返回 tuple 到 DELETE 参数的实际 binder 身份。

仍未承诺所有消息 Family、Outcome helper 的间接 tuple、sequence→ack_sequence 值关系、外部 ack 真实性、物理持久成功、完整故障恢复或 exactly-once。Option.map 回调只提供带来源的延迟字段投影，不当成已经执行。SQL 只读字面量与 params token tree，没有执行数据库。

[完整保存查询](messages-source-query.json)、[规则定位](messages-rules.json)、[设计与模型范围](messages-DESIGN.md)、[源位置校对](messages-SOURCE_CHECKS.json)。源位置校对对 6 个实际目标源码文件、2635 个去重位置核对源 hash 与 span hash，全部匹配。

未执行或导入目标代码，未测试、构建、安装或创建夹具。
