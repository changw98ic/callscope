# 正式 v9 的 IR 迁移结果

**IR 已实际接管字段分析，但本轮字段精度目标没有达成。** 三条字段合同的五个真实评估位置仍全部 unknown；services 的旧局部 own-shape / maxRetries 缺键摘要退为 unknown。没有把独立 IR 组件的 positive 观察代入正式 adapter。

[机器对照](/workspace/callscope/reports/astra-iteration6/IR_MIGRATION_COMPARISON.json) · [固定 v8 基线](/workspace/callscope/reports/astra-iteration6/ir-migration-baseline.json) · [迁移验收要求](/workspace/callscope/reports/astra-iteration6/IR_MIGRATION_ACCEPTANCE.md) · [Astra 独立复核](/workspace/callscope/reports/astra-iteration6/INDEPENDENT_REVIEW.md)

## 来源与实际变化

正式工具身份为 `35aedb73739399068219e6b9b46840c27441f5b1f74430031234ffb285c8b7fc`。CPB 快照 `bc3350f0…a4ff1de`、WWC 快照 `640931a5…55eae7` 的 source hash 与正式 v8 相同；政策和工具身份不同。

字段 adapter 使用不可变 IR 的 allocate、copy_own_slots、write_selected、invalidate_reachable 和 guard 判定；正式结果保存 ObjectVersion、copy-time 记录、捕获/别名、效果根和模型证据，属于实际接线。三条规则分别有 208、163、503 条来源事实，总计 874；这不是通过数或功能准确率。

模型变化单独记录：whole-copy 前提收紧；新增显式 `ecmascript-own-data-read-v1`；field policy 升为 v2。Get 的注册不会恢复已损坏槽或认证 symbolic child。没有同政策反事实重分析，不能把结果变化全部归因于 IR 精度。

## 五个正式位置

| 原位置/分支 | presence：v8 → v9 | source-form：v8 → v9 | v9 的直接边界 |
| --- | --- | --- | --- |
| engine-runner.ts:157，runJob 实参 | maybe → unknown | unknown → unknown | selected receiver/Get 关系未闭合；`field_actual_get_unregistered_or_receiver_unknown` |
| hub-queue.ts:1580，metadata 缺省支 | unknown → unknown | unknown → unknown | `field_actual_get_unknown`；外层替换与子引用不当作同一保留关系 |
| 同位置，metadata 已有支 | unknown → unknown | unknown → unknown | 同上；浅拷贝子引用与不明效果仍可见 |
| agent-config.ts:487，原 metadata return | unknown → unknown | unknown → unknown | `ir_captured_binding_write_possible`；另保留 async body/fulfilled 边界 |
| agent-config.ts:489，新对象 return | maybe → unknown | unknown → unknown | selected receiver/Get 未闭合；copy/捕获/async 边界仍在 |

五个 selected shape 都未闭合。对应效果总数从 8/13/10/11/13 变为 56/35/32/197/202；新版每处只展示 24 项样本并标记截断。IR 记录展开粒度不同，这些数量不是错误增长或精度提升的指标。

### services 的局部退化

同一实际 buildServices 调用、声明和 11 个字面外层键保留。v8 helper 摘要曾支持 maxRetries absent；v9 中 helper 的 selected presence 为 unknown、selected/whole shape 为 false。新版效果证据中有 roots/captures 未闭合及相应 widening；仅有已登记 guard 或 raw literal keys 不足以恢复判定。

这说明顶层 source form 事实仍可看，但正式 adapter 没有保住原局部缺键证明。下一步应沿 receiver/version/join 和 helper 返回的实际失效点修精度，并保留必要 alias/getter/completion 边界；本稿没有修改冻结核心。

## 其它必要关系与目标边界

导航与 atomicity 按具体来源、域、谓词、guard、反证和剩余缺口比较，关系保留。导航仍缺 delivery，已有 query 反例、特定 factory/callback 的 null→await→异步拒绝链和五段有限 port 装配保持；end-to-end=false、原 10 项 gap 保留。atomic 保护区、依赖装配、谓词和 lifecycle 保留，三个必要 unknown 及无交错证明的边界不变。

派生事件/context/abstract 身份的重命名有一致双射并核对引用，不当作语义退化；没有只比节点或事实数量。机器对照保留身份变化表与各关系检查。

新增两个局部预算 source-form 完成位为 true，但 numeric bound、实际预算消费、termination、全函数支配及全项目传递覆盖均未证明。它们不是完整 pipeline 参数消费结论。

[正式 v9 目标账本](/workspace/callscope/reports/astra-iteration6/goal-ledger.json)仍为 5 项判断、30 项必要义务，完整验收 false。字段 runtime-value、transport、full-functionality 均为 false。本次只读保存结果和冻结源码，未运行目标、分析器、测试、构建或浏览器。
