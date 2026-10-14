# CPB-01 参数、记录与预算的有限源码分析

本实现读取保存的 `GraphSnapshot`，不读取基准报告来生成结果，也不导入或执行目标。合同文件 [pipeline-rule.json](pipeline-rule.json) 只提供原判断、入口/参数/字段/预算的来源定位、版本模型及意图；不提供中间边、预计算路径、字段值或裁决。原 CPB-01 的 P1–P6 全部保留。

`callscope.pipeline_flow` 提供 `validate_pipeline_flow_rule`、`analyze_pipeline_flow(snapshot, rule)` 和 `analyze_pipeline_flows(snapshot, rules)`。JSON/文件及 broker 接缝由独立 `pipeline_channels` helper 提供；调用者共享同一个 source analysis 和 snapshot，避免重复加载大快照。普通完整查询持有 `.analysis-tools/goal-source-query.lock`。

## 关系域

所有源码观察保存 snapshot、文件 hash、词法 owner、AST byte span 和 parser 版本。`SourceAnchor`、`RecordIdentity` 与 `FlowLink` 分开表示表达式来源、记录身份和运输；消息、进程及动态模块关系不会创建 `CALLS` 边。

局部 copy 观察表示“copy 时当前自有可枚举数据槽，经实际有序 literal 后缀复制到新记录”。它不会恢复旧 semantic IR 的 entry provenance、闭合形状、未知 child referent 或旧 heap projection。field/Get 的旧未知仍保留。返回参数、record fallback、数组元素、JSON codec 和消息接缝各有自己的适用检查；未知 suffix spread、计算键、可见写入和实际可达 opaque consumer 不会被字符串同名替代。

## 实际来源连接

- 参数连接沿声明身份建立初始化、flag 写入、truthy fallback、返回字段、实际 parser 调用与 enqueue 参数。
- 装配连接读取真实有限 command table、dynamic import 实参、默认 executorRoot 的来源和实际 context literal；环境 root 覆盖另列。constructor 注入、`this.field` 赋值、direct/broker 条件赋值及实际 worker spawn argv 是独立关系。
- metadata 连接保存 normalization 的实际正常 return、ordered copy/merge、新 queue entry 与 existing return、scheduler 中每次字段重建、candidate/assignment/inbox 实参和 JSON 记录。current source 与本次 producer 身份分开；复用旧 pending 不归入新记录身份。
- worker 新参数对象的独立 literal，经固定 bridge 导入和实际 wrapper return，进入 engine 的 rest/spread/service 有序构造。finalizer-only 跳过该调用；其它字段的转交不被泛化为“所有 metadata 被忽略”。
- 每个 budget 单独定位声明身份、初始化、比较、counter 更新和 return。嵌套预算 helper 使用同一 lexical counter/limit ID，并保留实际同声明 helper 调用。queue attempt、phase 和 verification infrastructure 不因字段同名而合并。

## 受信模型和边界

模型注册为 `ordinary-record-tree-flow-v1`、`standard-json-record-codec-v1`、`normal-async-callback-transfer-v1`、`source-derived-module-assembly-v1`、`normal-durable-record-channel-v1` 与 `normal-authenticated-json-broker-channel-v1`。适用范围是实际 literal/decoded 普通数据记录、标准源码装配、正常成功 callback/JSON/持久记录及受认证 broker envelope。每条接线仍必须从真实 AST 建立；模型不能填补缺少的 helper、receiver、codec operand、operation 或消息 key。

标准 JSON 保留其真实值转换：非有限数变为 null，undefined/function/symbol 字段可能省略，bigint/cycle 等可能拒绝。参数接受和数值语义是不同判断；`parseInt(...) || 3` 的零回退不会自动变成另一项产品缺陷。成功静态路径不保证文件系统、网络、credential、lease、调度或某次调用成功。注入 fetch/provider/receiver、外部 executorRoot 和 opaque supervisor 独立保存，不据此声称全程序从未读取 metadata。

## 裁决和身份

输出保存原 claim、derived judgment、conditions、refutations、模型和来源。P1–P6 各有 `status`、`gaps`/`necessary_gaps`、实际证据及结论；全局必要缺段和 source budget 可见。完整裁决要求所有必要源码和模型适用关系闭合；局部反例或换窄范围不能替代缺段。`complete_assessment` 与 `full_goal_supported` 分开，原判断需要收窄时保留明确的 claim/refutation。

结果 header 使用实际 snapshot/source/policy hash 和完整 rule digest。Finding 的 Evidence ID 在完整 details 形成后计算。报告不会把 fact 数量、selector 数量或缺少红色节点当作完整性证明。

## 保存源码查询结果

完整 v11 保存快照 `731ae3b53582e86de4c9c786c224fc99aa45154099b7738ce8652be0f5a3f336` 的普通查询已退出 0。P1–P6 全部 `supported`；`complete_assessment` 和 `full_goal_supported` 均为 true，裁决是 `scoped_static_judgment_reproduced`。各义务以及全局必要/分析缺段均为空，表达式操作 12,575/50,000，函数 92/256，没有截断或预算耗尽。

自动结果保留相等值可能性、旧 pending/current assignment 身份、finalizer-only、direct/broker、独立预算、guard 前 early return 和 opaque supervisor；不声称所有 retry action 由一个 guard 支配或全程序没有读取 metadata。参数保存与其所选预算控制之间的接线判断属于上述实际正常记录/运输范围。

完整来源证据在 `PIPELINE_OBSERVATION.json`；简明状态、规则 digest 与当前实现文件 hash 在 [PIPELINE_QUERY_COMPLETION.json](PIPELINE_QUERY_COMPLETION.json)。独立 channel 查询在 `PIPELINE_CHANNEL_OBSERVATION.json`，queue/inbox/broker/counter 的实际源 gate 全部支持。查询脚本 [observe_pipeline_sources.py](observe_pipeline_sources.py) 使用完整保存源、真实 CALLS metadata 和共享锁；它没有预裁剪 snapshot。

当前文件 hash 在主查询后核对，当前规则的 contract digest 与结果相符；统一冻结与 fresh cold/warm scan 会独立记录实际加载的 tool identity。本文件不把查询后的文件 hash 冒充进程启动时的加载证明。目标没有运行、测试或构建。
