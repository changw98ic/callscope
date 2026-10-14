# CallScope v0.11.0 独立实现与正式产物审查

日期：2026-10-13（Asia/Shanghai）。审查者：Astra 独立审查代理。

**结论：本次所审范围内没有剩余 blocker。冻结实现与正式保存产物一致；原 engine 的 when-present 来源正项、queue／agent 的四条 unknown 均保留。新增 agent 构造返回处的一条条件性 copy-time 保留关系有效地独立记录，没有升级入口来源、存在性、Promise fulfilled、运行值或运输结论。原五项完整目标仍为 0/5，30 项必要义务仍为 4 项限定支持、20 项 partial、6 项 unknown。**

本代理没有修改核心、目标源码、旧冻结报告、policy、基线或验收合同；没有执行或导入目标代码、目标 CLI、测试、构建或安装，也没有运行 CallScope 测试。预冻结阶段阅读实现与原始目标文本、用标准库解析 Python 源码及 JSON。正式阶段只读取根代理已完成的正常静态扫描产物，用标准库独立重算身份、逐字段比较和解析证据指针，没有导入或重新执行分析器。

## 冻结身份与同条件比较

包版本为 `0.11.0`；schema 为 `2`；analyzer 为 `static-multilang-11`；detector 为 `call-rules-10-field-relations`。IR 为 `finite-immutable-semantic-ir-3`，字段摘要为 `finite-field-summaries-5-ir`，字段 wrapper 为 `static-field-contracts-4-ir`，词法组件为 `captured-lexical-bindings-3`，源码关系为 `captured-field-source-relations-1`。field policy 仍为 v2。

独立按路径、NUL 分隔和原始文件字节重算 43 个 Python 文件，聚合身份为：

`38933589ba90c08a8769fafa720e9c7258d29f17303c37dfadbdf491c579de7c`

实际文件集合、每文件 SHA256、聚合值及 `frozen-core-source` 归档全部匹配 [CORE_FREEZE.json](CORE_FREEZE.json)。读取期间核心与被审产物字节稳定。相对 final v10，变化限定在八个核心文件：包／发布身份、字段 adapter／wrapper／IR、新源码关系模块及共享词法 binder 精度修补；navigation、atomicity、budget 实现文件未变。

| 仓库 | 正式快照 | 选入／解析／未解析 | 节点／边 |
| --- | --- | --- | --- |
| CodePatchBay | `731ae3b53582e86de4c9c786c224fc99aa45154099b7738ce8652be0f5a3f336` | 333／330／3 | 11,085／60,571 |
| WinWinCode | `2b298f494c99d0f0040f7a8b856421813066caa21d7d6d26d36bb573d41626be` | 471／465／6 | 32,407／171,983 |

两库 source hash、policy hash 和策略文件字节与 iteration8 final v10 一致。两库 cold／warm 都保存为上述相同快照，cold `created=true`、warm `created=false`，两次保存的 tool identity 均匹配冻结；状态仍为 partial。原 26 项观察的 ID、状态与预期保持，合计 10 reproduced、3 unknown、13 evidence_only，其他状态为零。这不是完整目标覆盖率。

## 原五条字段评估与新增轴

| 所选位置／路径 | 原 endpoint 来源轴 | 新局部复制轴 | 源码关系数 |
| --- | --- | --- | --- |
| engine `runJob` 实参 `:157` | `source_form_preserved_when_present` | false | 2 |
| queue `resolveAgentsForEntry` 实参 `:1580`，第一分支 | unknown | false | 16 |
| queue 同一实参，第二分支 | unknown | false | 16 |
| agent body return `:487` | unknown | false | 3 |
| agent 构造 return `:489`，spread `:490` | unknown | true | 4 |

五条评估来自三个合同；queue 是同一源码调用点的两个路径评估。所有字段 finding 仍为 uncertain。41 条源码关系和一条所选局部复制支持只说明新增输出范围，不是新的目标分母。

engine 的所选 ValueRef provenance 对应真实 subject 参数声明、参数位置及 `maxRetries` 路径。rest／spread 的 ObservationRef 保持同一所选 ValueRef，helper `buildServices :155` 的返回对象仍具有闭合 own shape 与所选键 absent 证据。endpoint 的 selected/source-form complete 保留，presence 仍 unknown，whole shape 仍 open；reaching-value、runtime、transport、full-functionality 均未声称成立。

engine 的新 local-copy 汇总为 false 是预期结果：较早 spread 后存在后续 spread；末次 `services` spread 的所选键已知 absent，不发布 vacuous 的局部正项。

queue 的普通 Set、child 表面与跨前缀修改缺口仍保留；agent 两个 async return 的入口来源和 fulfilled 关系仍未知。新增 source-only 关系记录了构造、词法 alias 初始化、分支、Set 尝试、条件性源码顺序和实参／形参位置，但不把同一源码路径当成稳定 receiver，也不把“没有显式同键写入”当成没有间接效果。

## 新局部复制记录的独立核验

所选正项的 `CopyRetentionWitness` 为：

`17a41c5ccc74ca88886d4a95277667b7671b6f79c026f7aad0c783d8f69ebe26`

该记录对应 `agent-config.ts:490` 的实际 `...metadata`，终点为 `:489–493` 的整个对象字面量。它的前提是当次注册的 whole-surface copy 正常完成，且所选当前 own-enumerable data slot 存在。结论只是该次复制的浅值／引用在匿名新对象的字面量终点保留；后缀两个固定键 `agents`、`agent` 与 `maxRetries` 不相交。

独立检查覆盖以下连接：实际 spread 的 source ValueRef ID；已知时的 source allocation／version，未知时保留空身份；复制前目标版本；真实 copy EvidenceRef；复制后 checkpoint；与 source-fact 相同的 literal allocation；后缀固定键、位置及定义证据；同一 private-construction guard；终点 selected slot、barriers、copy layers 与 base shape；新增目标操作只能来自已认证后缀。

内容 ID 的重算包括完整嵌套内容、快照和 guards，没有先删语义字段再比较。正式字段产物中两个新 record 各出现 33 次，各有 30 个不同内容 ID；另核对 914 个 ModelGuard、79 个 ObjectVersion 与 201 个已保存 EffectRef 的内容 ID。全部一致，无同 ID 对应不同内容。全部 41 个 source-relation、3 个 copy-plan 及五个 source-context ID 重算一致；关系引用均可解析。`field-relations.json` 的五条导出与正式 summary 逐字段相同，汇总数也相同。

在所选正项后缀，独立核对了四个真实 effect-scope guard 及其来源、actual roots 和 effect IDs。没有把 opaque value evaluation 当成纯表达式；private construction 的边界用于保护尚未暴露且不可达的新父对象，不认证被复制 child 的内部内容。

**效果证据的审查边界：**正式 assessment 的 EffectRef 列表是最多 24 条的样本，agent 构造分支保存的总数是 199。本代理没有把样本误称为全量效果重放。完整 implementation 的 `retain_copy_to_literal_end` 已逐行复读：它检查 state 中所有保留 EffectRef 是否影响目的 allocation，且不使用可能因 canonical 去重漏掉重复效果的 ID 差集。产物审查另核对实际后缀 guards、checkpoint 与终点表面，以及已导出样本。内容哈希证明保存身份一致，不替代条件模型本身的前提。

## 预冻结问题的处置

详见 [PREFREEZE_IMPLEMENTATION_REVIEW.md](PREFREEZE_IMPLEMENTATION_REVIEW.md) 与 [PREFREEZE_SOURCE_REVIEW.md](PREFREEZE_SOURCE_REVIEW.md)。发现并复核关闭的问题包括：

1. 初版保留关系仅靠 fresh／escape／construction guard 不能识别 `escape_roots=False` 的目的对象损伤。最终版增加 actual-copy checkpoint、全量 state effects 检查、表面／selected-slot 比较及目标操作范围约束。
2. 初版 direct-write negative scan 没有消费 unsupported control regions，可能漏掉 `for (obj.key of values)` 的目标写入。最终完整位包含 `not prefix_controls`；未知控制／目标或预算截断降级负证并重算 ID。
3. 旧普通 Get 可能从不闭合 FieldSlot 中转发保留作审查用途的旧 ValueRef。最终要求 slot/projection closed、两层 barriers 为空且 capture 不未知；absent→undefined 也保留同类护栏。
4. 严格 helper capture gate 暴露了默认参数 RHS 假 binder 问题。`env = process.env` 的 RHS `process` 曾被误当可能声明，导致 engine 开发结果退化。最终共享词法层用 `_binders` 枚举支持模式的真实声明 token；unsupported 模式继续保守 fallback。它不证明全局运行值，也没有撤回 Get 或 capture 护栏。冻结身份下稳定保存源码查询与本轮正式扫描都恢复了合法 engine 正项。

literal suffix 的实际 write EvidenceRef 与后缀枚举现在均使用 `literal_suffix_definition`，初版证据 kind 不一致的问题也已消除。早期未冻结开发 JSON 仅用于查因，不作为正式结果或实现身份依据。

## 既有关系与原目标合同

对保存的完整 atomicity／navigation finding 做递归逐字段比较，保留所有字典字段、列表顺序、非身份值与引用。只允许可认证的发布版本字段，以及明确登记的 `captured-lexical-bindings-2 → 3` 版本字段；不删除字段、不忽略 truth/status、不作字符串归一化。

CodePatchBay atomicity 有 38 个身份双射，WinWinCode navigation 有 280 个；均为零语义差异。词法版本字段分别登记 19 处和 63 处，全部与各自 summary 的组件版本一致；导航的 `abstract-N` 按实际独立 engine 实例分别建双射，避免不同 counterexample 的局部编号被误合并。

目标账本独立解析了 648 条引用、111 个不同 artifact/pointer，逐条核对文件 hash、指针内容 hash、snapshot／finding／rule／contract 身份；全部通过。另核对实际目标 ID 集合与原模板一致，确有五个目标、30 个必要义务，全部 goal `full_goal_supported=false`。原 claim、required 标志、义务要求与前版状态保持；验收合同和模板 hash 匹配。账本仍是对保存自动证据的人工义务判断，`automatic_obligation_solver_used=false`。

## 可复核产物与限制

一般来源核验覆盖 18 个真实源文件、1,329 个不同位置／来源记录，其中 919 个含独立 span hash；1,472 个不同 typed EvidenceRef 的内容 ID、snapshot 与 canonical guard 列表全部匹配，无 ID 碰撞。两库 formal summary、field 导出、baseline 与 integration 均在收集时保持字节稳定。这些数量是核验规模，不是精度或功能覆盖率。

| 独立产物 | SHA256 |
| --- | --- |
| [INDEPENDENT_REVIEW_EVIDENCE.json](INDEPENDENT_REVIEW_EVIDENCE.json) | `a8add2130b4e310a18b7fdc8ab9adc055b92700b92c2f6af5a643a0295013ca1` |
| [INDEPENDENT_COPY_RELATION_REVIEW.json](INDEPENDENT_COPY_RELATION_REVIEW.json) | `731a3f5e26fc4d8394ce1392281c34910e30de560bff65975cb8d393589700a8` |
| [INDEPENDENT_RELATION_REVIEW.json](INDEPENDENT_RELATION_REVIEW.json) | `b3a5022843c31ba0793df51f79fcf2f1cb18b02488d43fdeda5cd66378a1c8a9` |
| [INDEPENDENT_GOAL_REVIEW.json](INDEPENDENT_GOAL_REVIEW.json) | `d3c35fddd688de0aee84c4d71d30c662e9103f4a08bf6c94213c1323b8fc83b0` |

复核脚本为 [collect_independent_review.py](collect_independent_review.py)、[audit_independent_copy_relations.py](audit_independent_copy_relations.py)、[compare_independent_relations.py](compare_independent_relations.py) 和已阅读后由本代理亲自运行的 [collect_independent_goal_review.py](collect_independent_goal_review.py)。其操作限于标准库及保存数据／原始字节。

本审查不声称执行测试或验证运行时语义，不声称 partial 扫描已解析所有目标文件，也不以新增局部关系解决普通 Set、共享 child、跨函数运输、Promise 同化或完整业务目标的缺口。已阅读本轮 [REPORT.md](REPORT.md)；其中核心结论与本次独立核对一致，未修改该报告。
