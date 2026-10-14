# WorkRun 有限选择关系

本轮补原报告 `WINWINCODE_ANALYSIS.md:60` 的有限缺段：由保存的 Rust 源码自动计算 runnable、依赖谓词、活动 run 排除和被选身份的再次检查。它扩展纯静态分析，不执行目标程序、测试、构建或生成夹具。

实现为 `callscope/rust_state_relations.py`，导出 `VERSION`、`MODEL`、`REQUIRED_ROLES` 和 `analyze_pattern(analysis)`。调用者先按普通 report claim 装载已认证的 `SemanticSources` 声明；该函数把事实写入 `analysis.source_facts`、必要缺口写入 `analysis.gaps`，返回含 `scoped_source_supported` 的 pattern。规则候选为 `workrun-rule.json`，其 source roles 只定位六个声明，不声明状态集合、路径、预期谓词、真值表或成功结论。

## 可复用部分

1. 解析已认证 Rust CST 的字段、引用、解引用、比较、合取、非、有限 if、局部 let、普通 record、clone 和 iterator 链。未知语法保留，关键关系遇到未知不闭合。
2. 从 `matches!` 的原始 token tree 只接受简单字段主体和 `Enum::Variant | ...` 常量备选。不展开宏，不接受任意模式、guard 或动态模式。标准 macro 解释是显式模型条件。
3. 机器抽取 `iter/filter/map/collect/find/any` 的 receiver、闭包参数和谓词；集合与字段值来自保存源码。
4. 将 effective-state 的有限表达式解释成“源状态 × 源量词布尔值”的表，自动连到 runnable 的实际比较常量。没有读取规则中的目标集合。增加“同 enum 其余值”的符号补集，避免仅枚举出现的常量后冒充完整 enum。
5. 将 dependency 的外层 `any`、内层 `!any`、身份相等及所需状态连起来；表中的量词 byte span 必须与该关系一致。
6. 比较 aggregate filter 和 exact-item exclusion 的状态常量、元素字段、持久 run receiver 和 item key。校验 runnable 的两个实参对应各 find 的真实元素和集合。
7. 从真实 let、struct field、contains receiver、返回 record 中的 clone 和所选结果 key 追踪 `start_next → start_item`。只接受本有限模式支持的 validation→collect→select→recheck 顺序；保留两处 `validate()?` 的正常继续前提。

所有 source facts 都有保存快照、原文 hash、解析身份、UTF-8 byte span 和 span hash；没有新增或修补历史 CALLS。

## 本项目源条件及反证

实际查询写入 `workrun-source-query.json`；它是以 v0.12 保存快照为来源的新模块开发查询，明确 `new_rule_not_saved_in_snapshot=true`。不得当成 v0.13 正式扫描、计入正式新版本成果或把旧快照身份改写成新工具身份。正式冻结与重扫由主代理完成。

源码中的标准有限关系是：存在未满足的直接依赖会影响 Ready / WaitingDependency 的 effective state；缺少阻塞依赖时 WaitingDependency 可派生为 Ready；其他源状态不因此变成 Ready。依赖为空时外层 any 为 false，实际依赖记录与结果仍未知。

所选 aggregate/start-item 活动排除的常量集合与 validate 内部的唯一性谓词是不同层次的源条件。模块额外保存 validator 的 enum 备选来源，不能把某个较小集合判为遗漏或把所有名为 active 的概念合成一个集合。

具体而言，validate 对 CandidateReady 另有 `candidate_items` 条件，对 Leased/Running 另有 `active_items` 条件。当前自动 validator 辅助提取器只抽取有限 `matches!` 备选，未穷举 validator 的直接 `==` 条件，因此不能把其输出当成 validator 的全条件列表；完整 validator 语义仍未声明已证明。

## 明确边界

`all_active_states_or_attempts_proven=false`、`whole_domain_state_machine_closed=false`、`runtime_schedule_or_termination_proven=false`。有限状态表和 find guard 的源条件可以闭合，不表示整个领域状态机、全部 attempt 身份、并发隔离、调度公平或持久化效果已经证明。

标准 slice/Vec iterator、HashSet membership、Clone、enum equality 和 `matches!` 是已声明的有限源模型。闭包里的本模块 free helper 仅按所选同模块唯一声明连接源关系，条件要求该声明就是被调用函数；不会把原图的 unknown/dynamic 边提升为 resolved。外部宏替换、任意 trait 分派和任意集合实现不在范围内。

只有关键关系支持且必要缺口为空时 `scoped_source_supported=true`。部分来源可用时保留 facts 和精确缺口，不能用规则中的描述性反证替代机器计算。

## 已完成的实际开发查询

`workrun-source-query.json` 记录以 v0.12 已保存快照 `ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28` 为来源的查询。模块 SHA256 为 `e40f4e5f2ec918b5d908d882d0db92cdd96c25738cb0aeb325c27ae3caff3dfb`，查询期间模块字节稳定；保存结果 SHA256 为 `4e2467ee1bbe54d45b083dd074a1fed8ea6de42755858c54a049d563329f785c`。

该次结果：117 条 source facts；普通关系遍历 1,731 次，有限表达式解析 196 次；两项预算均完整；8 行有限状态/量词表；10 个选择、字段、身份、正常顺序检查均支持；依赖量词 span 关联支持；`scoped_source_supported=true`，`analysis_gaps=[]`。源码规则的数据验证和两个新增 Python 文件的 AST 语法核对通过。没有运行目标代码、测试、构建或夹具。

这些数目仅描述本次新模型的实际提取，不是功能覆盖率。正式 v0.13 的冻结、快照和报告身份须由正式扫描单独记录。
