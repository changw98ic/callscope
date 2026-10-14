# CPB-03：源码生成的条件并发判断

目标是复现原 [Astra CodePatchBay 报告](../astra-baseline/CODEPATCHBAY_ANALYSIS.md) 的 CPB-03 完整判断：同 project、同 hashed key 的非终态任务应复用；facade 的预查与 authority 的 pending-only 复合键检查有不同口径，锁保护单次写入，允许一个有条件的重复交错。保留顺序复用、仍 pending 的内层复用、调度 guard 和失败回滚反证。没有执行目标代码、测试或构建。

实现文件为 `callscope/atomicity_completion.py`，本轮新规则为 [atomicity-rule.json](atomicity-rule.json)。旧 `atomicity_contracts` 规则及历史合同不修改。新规则只选择实际源码、注册八个有版本的有限模型和产品不变量；不提供谓词、路径、状态转换或 A/B 步骤。

## API

```python
validate_atomicity_completion_rule(rule)
complete_atomicity(snapshot, rule) -> dict
analyze_atomicity_completions(snapshot, rules) -> list[Finding]
```

`complete_atomicity` 重新读取认证的保存 AST，不接受外部 `prior_facts` 作为证明。每条 source relation、模型应用及 operation 有版本、快照、源 hash、实际位置和内容标识。`Finding` 输出全部 A1..A7、`necessary_gaps`、条件、反证和自动生成的交错；只有全部必要关系支持且模型应用完整，才输出 `complete_assessment/full_goal_supported=true`。

## 来源链

- 默认装配从真实 `Promise.all([import(...)])` 的稠密数组和声明身份，关联 `hubQueueMod`、return 对象的 `??` 默认、`ctx.deps` 覆盖和 `run` 的 factory 结果 receiver。普通 CALLS 不提升动态关系。holes/spreads、非唯一声明、条件 return/fallthrough 不作为支持。
- facade 的同项目过滤、hashed key 写入、非 terminal selector、existing.id 早退和 read-before-enqueue 来自实际语法及词法身份。实际 Node crypto 源式链与运行 provider 条件分开保存。
- 请求 builder 的 metadata 构造和选中 key 写入，关联到真实 enqueue 输入、normalizedInput 的 spread/固定覆盖以及 agent helper 的两个实际返回；字段在有限普通 JSON 数据模型内保留，不把 type cast、同名或配置路径当传播。
- 相同 root 的 load、authority、scheduler、fresh read、save 由实参/形参、constructor capture 和实际 `queuePath` 调用连接。`path.join(path.resolve(root), ...)` 是逻辑资源模型；物理路径别名、挂载和锁运行正确性仍是明确条件。
- queue save 的 entries → JSON.stringify → actual content → file handle.writeFile → 同一 temp rename 到 formal path 单独关联。只有正常 publish 是模型 commit；发布后 durability/release 错误可能已经提交，不能一概当回滚。
- 复用既有 region extractor 的 callback/resource 转发、acquire guard、fresh read、callback、save、错误收集、release 尝试和正常 return。process fence 只保护取得和释放，不把整个 facade 变成串行。
- 内层 find、pending 谓词、实际 key 函数、existing return、entry literal 和 push/commit 都有来源。新 entry 的 key 字段与 incoming 逐字段关联；明确保留“有锁且有二次检查”。
- scheduler 用真实 constructor-created receiver 和字面 dynamic import 绑定实际 updateEntry。有限 collection origin 分析经过 initializer、赋值、class helper return、filter/sort/slice、loop append 以及 map/destructure，证明返回候选来自真实队列项。guard 提取认证实际反向拒绝极性、expectedStatus 构造、id/status/version 对象身份和写前次序。

## 自动交错

源码提取器生成 `facade_active_precheck`、`protected_find_or_insert`、`scheduler_candidate_selection`、`guarded_status_update` 和条件 rollback 操作。BFS 在最多 4096 个抽象状态内搜索两个提交和一轮 scheduler 的可能先后，不执行目标代码。A/B 步骤来自 source-derived operation ID，不由 policy 预填。

同描述且 scheduler 可运行时，可找到两次预查均无项、首项受保护写入、候选被匹配 status/version 的 guard 改为 scheduled、第二次 pending-only 检查再插入的轨迹。关闭 scheduler 后，同描述 pending 项复用是独立反证。不同描述的情况先在实际 key 函数的有限 string/data 域内生成相同 project/hash、不同描述的渲染区别，然后用相同 operation 系统搜索；不假定任意复合 tuple 都是单射。

读、锁、写入、容量/leader/version guard、dispatch 失败与条件回滚均限制该风险；不声称某次请求实际并发、全部写者已覆盖、锁正确性已认证或业务运行通过。运行条件和尚未实现的中间关系严格分列：后者会进入 `necessary_gaps`，不会改名为条件。

## 开发核对

[ATOMICITY_DEVELOPMENT_OBSERVATIONS.json](ATOMICITY_DEVELOPMENT_OBSERVATIONS.json) 是当前工具对 v0.11 保存源码的正常静态查询，不是目标运行或测试套件。它是开发观察；正式重扫、版本身份与公开结果由根代理统一发布。源码匹配错误修复后继续查询到完整判断；未闭合结果不得作为完成交付。
