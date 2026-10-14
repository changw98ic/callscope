# Copy 边界与字段 IR 实现只读复审

日期：2026-10-12。范围：当前新增 `CopyBoundaryObservation`、`CopyRetentionWitness`、三个 copy 操作，`ordinary_get` 修复，object literal／capture／arguments 相关适配，以及新局部结果与旧字段验收的连接处。只读取源码与历史保存产物，不导入或执行分析器／目标，不运行目标 CLI、tests、build、install 或工具测试。核心、目标及旧报告均未由本审查者修改。

**在本报告对应的修补后源码中，没有发现遗留阻塞项。** 最初读到的“destination 受 damage 但未 escape 时仍支持 retention”缺口已反馈并在后续源码中修复。结论是所审查的局部条件关系可以与旧字段 unknown 并存；不是一般 JavaScript 语义完备性、运行正确性或最终正式扫描认证。

本次最终读到的源码 SHA256：

| 文件 | SHA256 |
| --- | --- |
| `callscope/semantic_ir.py` | `b1a604fbe80e5d0d192fef6d9ba59ffa7412e87be13a78e6ed761ee2e837bb61` |
| `callscope/field_summaries.py` | `464da566fa7343258776dc0b49cd7e6b1264fb7e49d10bdef5cee3409de97f62` |
| `callscope/field_analysis.py` | `9d9423b275801cf2ad1e122c66a4a2e8ae789439171d106c9d2760fce21de5f5` |

这些是审查时开发源码身份，不冒充最终冻结核心或正式快照身份。根代理负责后续冻结、正式静态工具运行及与 iteration8 的 engine／services 保持性比较。

## 条件 copy 关系的实际实现

`observe_copy_boundary` 保存真实 source ValueRef 及 value ID，即使该 value 为 unknown；有记录的 source ObjectVersion 时保留其当前抽象 snapshot，否则显式为空。目标记录包含实际 allocation/version 和 construction guard。该操作只查询已存在状态，不更新源对象、FieldSlot、CopyLayer 或 Projection，也不从 damaged source snapshot 修复入口 provenance。

其支持性需要已有 `own_data_copy` capability 在实际 copy EvidenceRef 上通过 `_supported`，目标为 fresh、未逃逸、非 external-aliasable、非 conditional allocation，且目标真实 evidence 支持 `private_literal_construction`。同目标的显式 source allocation/root alias、预算不完整、未知 key 和已证明缺失的 selected slot 都不能产生支持结果。

支持的命题仅是：**在本次真实 copy 正常完成，且当前 source 存在所选 enumerable own data slot 的条件下，destination 获得这个 copy-time value/reference。** source 当前 slot 的存在、最初形参值、源旧字段内容、嵌套 referent 内容及 runtime completion 不由这一命题证明。`source_presence` 只来自原有 closed 且无 projection barrier 的查询；不闭合时仍为 unknown。

新增 `copy_with_boundary_observation` 将 observe 和真实 `copy_own_slots` 串在同一调用中，不带 exclusions，保存 `actual_copy_evidence` 和立即 copy 后的 `destination_after_copy`。它检查 copy 支持标志、状态预算、checkpoint 存在及 allocation 身份。这样，一个裸 boundary 记录不能直接获得 literal endpoint retention。

未知 copy source 可以使旧 `copy_own_slots` 的抽象 shape 继续损伤。局部 theorem 支持不消除这个损伤，也不关闭原 selected field 的来源判断；它表达的是当前 copy 操作的相对关系。旧 copy-time ObservationRef／source snapshot 仍用于原有已闭合来源，不被新的记录替代。

## 已反馈并修复的 destination damage 缺口

第一次审阅的 `retain_copy_to_literal_end` 只检查 fresh、escape、external alias、conditional allocation 及 construction guard 相等。公共 `invalidate_reachable(..., escape_roots=False)` 能 damage 目标而保留 fresh/construction，因此错误地获得 retention 支持。仅比较新增 barrier 集合还会遗漏同 reason 的重复 damage；仅比较新增 EffectRef ID 集合则会受 canonical effect 去重影响。

随后读到的修补采用保守方案：

- 检查整段 State.effects；任何 `affected_allocations` 包含 destination 的记录都阻断 retention，不依赖 ID 集合差集。
- 必须有真实 copy 的 after-copy checkpoint 和 actual copy EvidenceRef。
- 端点与 checkpoint 的 barrier、copy layer、base closed shape，以及整个 selected FieldSlot 必须不变。
- 新增 destination evidence 必须对应完整 fixed-definition suffix 的认证 file、source hash、snapshot、context、model 与完整 byte span。
- same-key suffix 明确阻断；later spread、computed key、accessor、prototype syntax、missing definition evidence、budget/incomplete、逃逸、条件 allocation 或丢失 construction identity 都不能获得 endpoint witness。

检查所有已记录 destination effects 会保守拒绝一部分理论上能由后续 copy 覆盖的 prefix damage。这是精度限制，不是接受 damaged endpoint 的漏洞。copy 自身仅因 source 抽象表面未知产生的直接 shape damage 没有 EffectRef；after-copy checkpoint 保留该 damage，后续检查不把它自动当成真实 suffix mutation。

suffix 写入的 EvidenceRef kind 可以是 `source`，suffix 认证记录 kind 为 `literal_suffix_definition`；因此按完整来源 tuple 匹配比要求 record 相等合适。复读确认 tuple 已含 `model_id`，不只依赖行号或 byte span。

## Guard 与内容身份

surface、construction、suffix 分别使用其实际 capability，证据链包含来源 hash、snapshot/context 和 guard ID。suffix guard 由实际完整 literal suffix AST 的 canonical static keys 生成，不从字段合同说明预填 suffix 或键集合。value initializer 的 effects 仍独立接受 destination 检查。

`CopyBoundaryObservation` 和 `CopyRetentionWitness` 都是 frozen/slotted IR records，嵌套仅为 immutable scalar／tuple／IR records。构造 observation 时使用空 observation ID 对完整 record `_digest`；wrapper 添加 actual-copy/checkpoint 内容时先将 ID 清空，然后重算。witness 同样以空 witness ID 对完整内容重算。此次源码中没有看到改动 guard/kind/checkpoint 却保留旧 ID 的路径。

这些检查认证工具内部的来源与模型关系；ModelGuard 仍是静态声明前提，不认证目标运行堆或执行成功。审查结论覆盖规范操作的实际 adapter 调用路径，不声称手工伪造任意 State／IR record 可以作为受信来源证据。

## Get、object、capture 与 arguments

`ordinary_get` 现在要求返回源 ValueRef 的 projection 为 closed，projection/value 都无 barrier，且没有 capture unknown。已闭合 absent 分支也检查 projection 和 value barrier。损伤的 materialized slot 即使仍持有旧的 unbarriered ValueRef，也进入 bounded unknown 路径，不再凭 getter-free Get 复原旧来源。这覆盖前一报告中的 `opaque(o); return { maxRetries: o.maxRetries }` 源码反例。

object literal 在真实有序 spread 操作中记录 boundary；suffix 来自同一 literal 的实际成员次序。endpoint witness 在 `finish_construction` 之前建立，随后释放 construction lifetime；typed witness 仍明确其 scope 为 literal expression before exposure and Promise assimilation。局部记录只绑定直接观察到的 literal operand 及其 exact span，不作为任意别名日后当前值的证明。

`_runtime_nodes` 新增 TS-only contexts，并对 as/satisfies/type-assertion/non-null wrappers 只进入 runtime operand。它继续遍历真实 nested runtime syntax。callable 仍保留真实 live capture cells、future initialization／rebind，以及 this/super/meta-property/arguments/dynamic-scope 的 unknown 边界。helper expansion 新增 `not callee.capture_unknown` 检查，因此未知隐式 arguments／receiver 捕获不能被普通 helper 返回解释绕过。普通 Set 和未支持语法／control 仍保留效果边界，没有从 copy/Get 模型取得 Set 或子对象 plainness 权限。

## 旧字段域没有被局部支持提升

`assessment.source_form_relation` 仍仅由原 Projection 的 closure、barrier、provenance 和所选 source binding/path 推导。async body return 仍把最终 relation 置为 unknown；pre-completion relation 与新局部 copy witness 分别保存。局部记录固定保留 initial parameter origin、presence、runtime value、fulfilled value、transport 等 false 标志，并明确 top-level copy-time slot scope。

`selected_shape_complete` 和 `source_form_complete` 的原计算没有使用 `local_copy_retention_supported` 或 source-structure relationship counts。`field_analysis` 只分别统计这些新记录；Finding 状态仍 uncertain，reaching-value-origin、transport、full-functionality 仍 false。因此“本次当前 slot 在 literal 内被保留”不会自动升级成“入口字段 source form 已闭合”或完整参数运输。

本审查没有运行新正式扫描，故没有独立声称 engine 的旧 positive 或 services 的旧 absent 已在最终保存产物中保持。源码连接仍保留原 copy-time snapshot／ObservationRef 路径，Get 修复仅阻断损伤 projection 的旧来源回流；正式保持性与五 goal／必要义务的最终结果需使用根代理保存的新静态产物核对。

## 后续正常来源查询：engine helper 捕获回退

根代理随后授权用现有 LexicalBindings／runtime traversal 进行小文件正常静态来源查询，追查新增 `not callee.capture_unknown` helper gate 导致的 engine 回退。本节使用已安装的 tree-sitter 解析一个实际源文件，并调用受信工具的 lexical/runtime 来源接口；没有运行目标、测试或整个 analyzer scan，也没有多次加载大型快照。前文的源码只读实施复审与本节的受信静态查询分别记录。

实际 `server/services/engine-runner.ts` SHA256 仍为 `952b6a43e9d2e5a2040eae1c7c8ec5c000d26a12f1c44d395041434db48bd864`，与旧保存 source 一致。解析无 error；`buildServices` function span 为 bytes 2978–5364。逐个查询当前 `_runtime_nodes` 返回的 runtime identifiers，并应用 callable 的 internal-declaration／import 排除规则，发现唯一 unknown capture 触发节点：

| 节点 | 实际来源 | Lexical identity | unbound 查询 |
| --- | --- | --- | --- |
| `process`，identifier，parent member_expression | 第 75 行 `env = process.env`，bytes 3046–3053 | `unresolved_lexical_binding` | `unbound=false`，`possible_unmodeled_binder` |

unbound 的 possible binding 位置指向整个 `buildServices` formal_parameters，bytes 3000–3127。`LexicalBindings.unbound` 的兜底扫描当前对 `walk(pattern)` 中任意同文本 node 都保留可能 binder，因此把参数默认值 RHS 中的 `process` **读取**当成了声明名。`satisfies RunJobPorts`、literal property keys 和 nested arrows 不是此次查询的触发点；匹配触发数量为一。

反馈根代理的通用修复方向是：对已支持的 pattern 使用 `_binders` 枚举实际 binder；参数默认值 RHS 不属于 binder。对不支持 pattern 仍保留未知声明边界，并按语法区分可识别的 RHS／type-only 子树。不能按 `process` 或 helper 名字加白名单，也不应仅为恢复旧数字而解除 `not callee.capture_unknown` gate。确认 `process` 无此处本地声明，只建立 lexical absence；仍不认证标准宿主值、process.env、callee purity 或运行时 effects。

根代理随后将版本更新为 `captured-lexical-bindings-3`：支持 pattern 使用已有 `_binders`，`_UnsupportedPattern` 仍保留原 walk 的保守 fallback。只读复审确认该修改没有源码名称特例，没有绕过 direct-eval／重复／未知 binding 边界，且仅在当前 visible scope 检查声明 token。读到的 `lexical_bindings.py` SHA256 为 `896b1ed014c1b4172d5b482a4d953d674088b07eab936c06de4da809cd4f75f4`。该源码修复可接受；此审查者未重复根代理已启动的 engine-only 正常工具查询，保存 endpoint 保持性仍由新查询结果证明。
