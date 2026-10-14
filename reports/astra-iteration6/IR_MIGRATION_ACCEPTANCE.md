# IR 迁移来源基线与验收要求

状态：**正式 v9 对照已完成，字段精度目标未达成**。下文保留扫描前制定的 v8 来源基线与验收要求；正式结果见 [IR_MIGRATION_RESULT.md](/workspace/callscope/reports/astra-iteration6/IR_MIGRATION_RESULT.md) 和 [IR_MIGRATION_COMPARISON.json](/workspace/callscope/reports/astra-iteration6/IR_MIGRATION_COMPARISON.json)。本稿只读保存结果和冻结源码，没有执行或导入目标，没有构建、测试套件或浏览器验证。机器基线为 [ir-migration-baseline.json](/workspace/callscope/reports/astra-iteration6/ir-migration-baseline.json)，因果注释是独立源码审阅，不是预填给新引擎的结果。

## 固定起点

| 来源 | 固定身份与含义 |
| --- | --- |
| CPB 正式 v8 | `fb9efe4704d83310958712a8b35089f06511d733258c63777e1d93af25bf89e8`；source `1d6936ac…20d7c5` |
| WWC 正式 v8 | `24997ddb7ac245abb12a7da4387b77d1f605b50e6719e8b131322cfe4f164f31`；此轮字段合同配置为 0，不能当字段能力已覆盖 |
| 字段内核 | `finite-field-summaries-2`，冻结源码 SHA `443edebc290a6a2fabc56c76d405f417af7c668ce17b22ce0201ab9fe5f3aec9` |
| 正式结果 | [field-assessments.json](/workspace/callscope/reports/astra-iteration5/field-assessments.json)：3 条 CPB 规则、5 个选定评估位置，全部 `unknown`；三条规则的 source-form、selected-shape 完成位均为 false |
| 独立完整目标 | [原验收合同](/workspace/callscope/reports/astra-iteration4/GOAL_ACCEPTANCE.md)及 [v8 目标账本](/workspace/callscope/reports/astra-iteration5/goal-ledger.json)：5 项判断、30 项必要义务，完整验收 false |

5 个字段位置与 5 项完整判断是不同的集合。基线保存了 4 份真正来自指定 v8 快照的原文身份、45 个实际 AST 区间和旧内核的关键源码片段；原文件及区间哈希全部匹配。人工 AST 选择只定位来源，实际关系仍以正式 source facts 为依据。旧报告、原 26 项观察和目标分母均没有改写。

## 五个位置为何仍为 unknown

| 实际位置与分支 | v8 的直接失效原因 | 可收窄的实现保守策略 | 必须继续分栏的源码边界 |
| --- | --- | --- | --- |
| [engine-runner.ts:157](/workspace/codepatchbay/server/services/engine-runner.ts:157)，正常前缀通过 runtime-root guard 后的 `runJob` 实参 | `field_container_or_callback_escape_unknown` 与 `field_temporary_shallow_value_epoch_unknown`；选定字段为 maybe，source/shape 未闭合 | :155/:178 的不明容器参数使所有 env 值失效；任意调用提升全局 epoch，连新建 rest 父对象和正在构造的实参也被污染 | :142/:143 的异步路径解析、broker 选择、env/providerServices 引用与 helper 效果未知；不能宣布正常前缀必到达、预算为数字或有效消费者已连接 |
| [hub-queue.ts:1580](/workspace/codepatchbay/server/services/hub/hub-queue.ts:1580)，`:1570` metadata 缺省分支 | `field_receiver_effect_unknown`；分支先执行 `normalizedInput.metadata = {}`，再子字段写入 | 一次已知外层属性替换及每次嵌套写都使全部 env 失效 | 缺省分支不是“保留既有 maxRetries”；空对象、truthiness 默认、ui-profile guard、原 input 调用效果仍需按分支处理 |
| 同一 `:1580`，`:1570` metadata 已有分支 | 同上；正式结果保留独立第二个评估 | 无关 normalized 外层槽也随全局失效一起丢失 | `...input` 是浅拷贝；metadata 可与 input.metadata 共用引用，`:1571–1573` 是共享子对象写。getter/proxy、未闭合 alias/effect 不能因引入 IR 而消失 |
| [agent-config.ts:487](/workspace/codepatchbay/server/services/agent/agent-config.ts:487)，直接 `return metadata` 分支 | 动态 import、array/opaque/container 效果污染 metadata；另有 `field_async_return_assimilation_unknown` | 前缀的无已知可达关系调用被全局扩大为该 receiver 的失效 | `metadataRecord` 与 metadata 是同一来源；`:481` 把 agents 子引用送入 merge。async body return 不等于 Promise fulfilled 值，thenable/继承 then 未解 |
| [agent-config.ts:489](/workspace/codepatchbay/server/services/agent/agent-config.ts:489)，新对象返回分支 | 前述失效，外加后方 `Object.keys(merged)` 的 epoch 使已展开的临时来源失效；仍有 async assimilation gap | 任意后续 initializer 调用污染此前复制的字段，不区分能否触及新对象/槽 | `...metadata` 后写 agents/agent 是新对象构造。copy 会访问其它枚举属性，其它 getter 也可能影响 selected field；merge/alias/fulfilled 返回仍未闭合 |

这里的“不明效果”不是已经发生修改的运行证据。“可收窄”也不表示调用纯净；须由 IR 的实际可达关系、观察时间和 heap 身份支持收窄，不能简单删除这些 gap。

## 首个 engine 路径允许恢复什么

[engine-runner.ts:131](/workspace/codepatchbay/server/services/engine-runner.ts:131) 的普通解构本身不是 copy；`:137` 的 rest 才创建新对象。正式事实已提取五个排除键：cpbRoot、project、sourcePath、hubRoot、workerBrokerClient；maxRetries 不在其中。新 rest 的自有槽须指向 **copy 时** 的来源，不能在后续使用点重新读取已经可能变化的 live opts。

`:158` 先展开 jobOptions，`:176` 后展开 services。实际 `buildServices` 调用有正式 CALLS/实参形参证据，helper 在 `:85–119` 构造 11 个固定外层键，`:121` 返回 ports。v8 已保存 helper 对 maxRetries 的局部 absent 摘要和 `later_spread_selected_field_absent`；未知字段值没有抹掉此局部缺键事实。新的 IR 仍须从真正 AST、返回覆盖与别名/逃逸检查产生这份负证，不能从配置或报告预填 11 个键。

若 mkdir、路径 helper 或子字段 opaque 调用没有可达新 rest/最终实参父对象的写入、捕获或逃逸关系，不能只凭全局 epoch 判其 own-slot 来源失效。它们仍可能抛错、改变子引用内容或影响外部对象；`:178` 的后续 initializer 也必须检查真正可达效果，不能一律视作纯调用。

首轮可支持的改善是：**在显式普通 own-enumerable data 模型与正常到达条件下，所选 maxRetries 槽由 copy-time 参数来源传入最终新实参**。它不证明当前 opts.maxRetries 相等、referent 内容稳定、参数存在或为数字，也不证明 runJob 激活、有效预算决策、消息运输或完整 CPB-01。

## v9 的显式 Get 模型变化

本轮 root 另行登记 `ecmascript-own-data-read-v1`，字段 policy 升为 v2，三条字段政策注册 copy 与 read 两个模型。**read 是新增的显式模型，不是 copy 已经隐含认证的读取。** 正式产物到盘后，以其中保存的版本和政策身份为准；v8 机器基线不补入这个新前提。

有限 Get 只用于有真实 ObjectVersion/guard 的 root 或 fresh-data 对象。own data 属性存在时可以非 enumerable；是否可以复制仍由 copy 模型另外决定。缺键按显式无 prototype/accessor/Proxy 读取前提得到 undefined，不推广到一般 JavaScript 对象。presence 必须从源形状和相应 guard 推导，symbolic child 不因父对象有模型就被认证为普通对象。

新增模型适用前提、whole-copy 前提收紧和 IR 的不可变 allocation/slot/effect 精化须分别列出。一个 unknown 变强可能依赖三者共同成立；本轮没有做同政策反事实分析，不能宣称它仅来自 IR 精度提高。

## 迁移验收表

以下要求由实现源码和真实保存源的结果对照验收，不建立测试套件、伪造 fixture 或目标执行结果。新快照 ID/组件版本可变化；跨快照对齐原文件 hash、AST 区间、词法声明和实际调用点，不能强行追相同事件数或 gap 数。

| ID | 必须看到的实际 IR 接线与来源证据 | 不可接受的通过方式 |
| --- | --- | --- |
| IR-01 接线 | 字段 selector/formal/return 判定真正读取 IR 的 allocation、slot、copy、effect 与条件节点；结果引用所用 IR 身份 | 旁边生成 IR，继续由旧递归模型独立产出判定；只新增 unused component |
| IR-02 身份 | snapshot、原 hash/span、词法声明、真实 CALLS 和模型版本；解析、坏 hash、重复声明、超预算仍有诊断 | 依靠路径、callee 拼写或政策角色补中间绑定 |
| IR-03 观察时间 | rest/literal 父 allocation 分离；copy-time slot 与源对象后续状态分离；同次调用真实 alias 保留 | 按同一个 source ID 合并不同时间对象；深复制浅拷贝子引用；把 live read 当复制值 |
| IR-04 效果范围 | opaque 调用的可能参数、receiver、capture、global/escape 可达集与被影响槽明确；无可达 fresh parent 不全局污染 | 假定 opaque 调用纯净，或忽略真正未知 global/captured reachability |
| IR-05 负证 | services 实际声明/返回的固定 own-key shape 独立支持 maxRetries absent；字段 presence、source form、whole shape、字段值分开 | “const 就不会变”“其它字段值未知所以该键也必存在/必缺”或手填中间 keys |
| IR-06 copy/heap | shared child、slot replacement、alias 写入、getter/proxy/computed/转义键/__proto__ 的适用与未知检查 | 只检查 selected key 的 getter；把动态 subscript identifier 当固定字段 |
| IR-07 时间求值 | receiver/callee 先于实参、initializer/实参按源码顺序；后方可达效果影响先前尚未入 env 的 temporary | 删除 epoch 护栏，却没有等价的可达时间关系；连续 `.child.key` 绕过失效 |
| IR-08 效果语法 | default RHS 在 body 前求值；class/static/new/update/delete/template/computed/callee 未建模效果仍保守保留 | 把未支持表达式当无效果，先评估 sink 再补一条无约束 gap |
| IR-09 分支 | `||`/`??`/`&&` 只排除有限模型已证明不进入的分支；条件未知则保留各可能支并 join 深 heap、effect/temporal flag 和 alias 状态 | 冒称一般路径可行性已求解；只按浅签名合并；固定 unknown 谓词为单支；遗漏另一正常 return |
| IR-10 完成关系 | sync arbitrary value、generator activation、direct await、async body return、fulfilled 值分栏；thenable/继承 then 保留 | 有 await 或 ordinary_async 就宣布 fulfilled 对象、全路径完成或资源寿命已证明 |
| IR-11 覆盖/出处 | 逐原 selected site 对照 AST/source facts；全部正常返回和剩余缺口、采样总数/完整指针明确，四类出处分开 | 删除 unknown 路径降分母；手工来源包当自动结果；把采样当全部证据 |
| IR-12 完整目标 | 局部 positive assessment 只贡献对应必要义务；runtime_value、transport、full_functionality 和原 5/30 账本各自验收 | 一个字段源式改善或“无红色 finding”就算完整功能通过 |

新增 Get 边界另核：read 模型有显式注册、版本、真实 receiver/ObjectVersion 和适用 guard；own 非 enumerable 的读取与 enumerable 的复制分开；缺键不预填 presence，symbolic child 不继承父前提。这是 v9 新模型的接受义务，旧 v8 机器基线仍保留原 12 项要求和旧模型身份。

旧 P1 护栏的来源是 [v8 独立复核](/workspace/callscope/reports/astra-iteration5/INDEPENDENT_REVIEW.md:78)和基线中的冻结内核片段。不是每个边界都在这五个真实位置被触发；没有捏造对应输入来声称验证过它们。新增 IR 未实现的边界必须继续 unknown，已经实现的精化须提供实际源证据。

## 本稿的评估边界

在正式 v9 到盘前，本稿只确立基线与验收义务，未预填 IR 结果。原 v8 的 runtime_value_verified、transport_proven、full_goal_acceptance 均为 false；首个 engine 局部源式改善不会自动改变这些值。queue callback/new-existing、scheduler、持久记录/JSON、inbox/direct-broker、worker 装配和有效预算消费者仍按原合同分别闭合，不改写成环境假设。正式 v9 已完成实际对照：五个字段位置仍全部 unknown，services 局部 own-shape/缺键摘要退为 unknown；上述完整目标边界未被升级。

root 正在为本轮政策补充 whole-copy 前提，旧 field locator 保持。正式 v9 对照须分别记录 policy/model 条件变化与实现的 allocation/slot/effect 精化；不能把仅有更强前提造成的结果变化当作 IR 精度提升。后续 `IR_MIGRATION_COMPARISON.json` 将逐五个实际位置比较 source、presence、referent、completion 和 effects，并保持导航/atomicity 的关键必要关系对照；当前没有预填新的通过结果。

本稿不修改 core、目标、UI、原正式结果或 Astra 最终报告。独立来源审阅与真正自动字段判定的界线保留在机器基线的 provenance 中。

## 正式 comparison 的字段准备

以下字段约定在正式 v9 summary/快照到盘前制定，现已按真正保存结果填入 comparison，没有伪造新结果或改写旧机器基线。

| 字段组 | 保存内容 |
| --- | --- |
| `input_identities` / `comparability` | v8/v9 快照、原文/政策/hash、组件版本和冻结来源；相同 locator 与 source 的核对；政策和模型不同处单列 |
| `policy_model_delta` | 两版 models/source_assumptions/适用条件；whole-copy 收紧、read 新登记与 field policy v2；模型登记与实际 receiver guard 分开 |
| `sites[].source_anchor` | selector、字段路径、sink、原文件 hash/span、词法声明及该位置分支。queue 同一 callsite 的两支和 agent 两个 return 分别对齐 |
| `sites[].before` / `after` | presence、source_form/pre_completion relation、selected/whole shape、field_sources、formal/edge、branch conditions、剩余 gaps；保留分析阶段 |
| `sites[].referent` / `completion` | copy-time 槽来源与 current input/referent 内容分开；IR ValueRef/ObjectVersion 引用及 barrier；body expression、Promise fulfilled、activation/runtime 各自记录 |
| `sites[].effects` / `precision_basis` | 前后真实效果证据、调用/receiver/capture/alias 的可达范围、复制与写入时间、受保护的新 allocation/slot、实际 IR decision 来源；没有此理由不能仅凭 gap 减少判精化 |
| `sites[].change_attribution` | `ir_reachable_slot_refinement`、`whole_copy_assumption_refinement`、`explicit_read_model_added` 分栏；只列真实参与证据，不假定可独立归因 |
| `cross_consumer_relations` | 导航 query/反例/context/null/await/rejection/port 与 atomic 资源、绑定、谓词、保护生命周期、反证/unknown 的实际 source 关系，不只比计数 |
| `goal_boundary` / `verification_scope` | 字段局部改善对原必要义务的范围；原 5/30 账本、runtime、transport、full_functionality 独立；本次只读保存源对照，无目标或测试执行 |
