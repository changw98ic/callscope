# 记录来源、索引投影与失败证据的有限静态关系

本轮直接承接原 CPB 报告第 68、70、76 行和 v0.12 明确保留的缺口。实现为 `callscope/record_projection_relations.py`，入口 `analyze_pattern(analysis, kind=None)`；接收报告引擎已认证的保存源码 roles，不读取原报告作为事实，不访问或导入目标工作区，不生成新的 CALLS。

接口版本 `captured-record-projection-relations-1`，模型 `finite-record-codec-projection-source-v1`。规则仅配置 file/symbol/role 定位与适用条件，`records-rules.json` 分别选择 event_index_projection、trusted_command_lineage、unsupported_record_retention 三种固定实现；20、10、6 个角色均低于每条 32 角色限制。

## 计算的内容

- 通用层根据 CST 生成按顺序排列的 record 字段、spread 覆盖风险、局部声明身份、initializer 依赖、赋值尝试、guard、return/throw/continue 和真实认证调用。
- 函数调用之间仅在现有快照 CALLS 唯一认证时关联实参/形参。字面量 callback 通过实际实参与 callee 相应 formal 的调用关联；该来源接缝明确 `synthesized_call_edge=false`，不证明 callback 被激活。
- 局部身份使用 `resolve_identity`，只比较相同捕获声明；该 API 不等于 reaching value 分析，因此每条 initializer 依赖保留 `value_preservation_proven=false`。任何 alias、未知 heap effect、外部端口成功均不通过同名猜测补齐。
- 同一 block 内分离语句之间的顺序只适用于正常到达两句的同一次调用；不把 AST 顺序当作事务、提交或所有路径支配。
- 固定 finite marker 模型只计算 `other && !marker` 在 marker=true 时为 false，不能消除匹配 checklist、输入校验、早退、abort、覆盖和异常等其他条件。

## 三类必要来源关系

`event_index_projection` 要求真实正常 append→独立 index refresh 顺序，serializer 结果绑定作为 durable append 的实际参数，projection callback 的 `.state`/fallback 来源赋给同一 index.jobs 记录再传给 index writer，以及 readEvents→materializeJob→重建 jobs→index record→同一 writer。另保留 retry catch/throw、divergence count、classification 和 doctor 源码 guards。它支持“事件与索引属于不同源码提交调用边界、存在重建来源”，不证明物理持久化、一次事务、崩溃恢复完备或分歧意味着事件丢失。

`trusted_command_lineage` 要求源 `execFile` stdout→JSON.parse→policy parser，实际 parser callback、policy spec 的显式 executable/args 字段、loaded policy→resolver→command runner 的相同声明依赖，以及 executor 从同一 formal 读取 executable/args 并采用 shell=false。`expectedEvidence` 仍可能参与 protected path/provenance 等独立策略分支；本模型不宣称所有路径上的完整非干扰或命令已经执行。

`unsupported_record_retention` 要求 runner 的 emitFailedClaim=true 记录 push 到返回数组，plan 初始化/升级保留 true marker，指定 ledger skip 对 true marker 为 false，claim push 到返回 evidence 集合，以及实际 ledger 调用结果 JSON.stringify 后作为 writeArtifact 的 content。真实 counterexamples：缺 id/predicate、缺 checklist item、hardGate 先入且按 checklistId first-wins、observation spread 对先前字段的覆盖、abort/异常及写入失败。它承接原报告“存在失败记录路径”，没有推广成所有输入都保留或每条 artifact 都提交成功。

## 开发查询与身份

`records-query.py` 是可信 CallScope 正常静态来源查询。它在统一 flock 下只读打开关闭后的 v0.12 CPB 数据库，使用保存源码与当前模块生成三份 development JSON；输出明确 `formal_publication=false`，记录旧 snapshot/source hash 和当前 adapter SHA。它不回写旧数据库、报告或 policy，不执行任何目标命令、测试、构建或夹具。正式新版应由 root 统一冻结后重新扫描绑定新版 tool/policy/snapshot 身份，不能把开发查询标成 v0.13 正式结果。
