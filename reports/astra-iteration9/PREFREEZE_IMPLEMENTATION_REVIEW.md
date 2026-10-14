# v11 冻结前实现的独立审查

本报告是 Astra 对开发源码及随后冻结身份的独立只读审查，不替代冻结后正式两库产物验收。未执行或导入目标代码、目标 CLI、构建或安装；未运行目标或 CallScope 测试。核对方式为源码阅读、标准库 `ast.parse`、文件哈希和保存 JSON 的只读分析。核心文件由根代理／实现代理修改；本审查只写本报告及独立产物审查脚本。

**当前结论：本次源码审查没有剩余 blocker。目的对象 effect 漏检与循环目标负向完整性问题均已修补并复读；普通 Get 的 stale-slot 护栏保留。engine 回退已定位为默认参数 RHS 被误当声明名，修补后稳定查询恢复原有 when-present 正项。current-copy 轴的设计边界合理，局部 copy 正项不能替代原字段端点或完整目标。正式两库产物与全部内容 ID 的验收仍由后续独立产物审查完成。**

最终复读并用 `ast.parse` 检查可读取性的源码身份如下，均与 `CORE_FREEZE.json` 对应条目一致。冻结的 43 个 Python 文件聚合身份为 `38933589ba90c08a8769fafa720e9c7258d29f17303c37dfadbdf491c579de7c`。

| 文件 | SHA256 |
| --- | --- |
| `callscope/field_summaries.py` | `8ecda3c6be660b4d911b22b0c5dd1f586ecdd748bb31930071e8ad4a4f52d7d8` |
| `callscope/semantic_ir.py` | `8b220fb90d07656289e175cc0aa3d92bec5f7d0daa357322e825f71039320c56` |
| `callscope/field_relations.py` | `6bb036b06cc05e8728cc858b012a650ca496d21026e7288bf2349c00f6ffe98c` |
| `callscope/lexical_bindings.py` | `896b1ed014c1b4172d5b482a4d953d674088b07eab936c06de4da809cd4f75f4` |

语法可读取不代表测试通过、真实扫描成功或语义正确。原 policy、基线、目标源码及五目标／30 义务合同未由本代理修改。

## current-copy 轴的实际实现边界

`CopyBoundaryObservation` 与 `CopyRetentionWitness` 是 frozen／slotted IR records，经 `_Record` 递归不可变检查。它们分别保存 source ValueRef／可用 source snapshot、复制前目的 snapshot、模型与构造 guard，以及 literal 后缀终点。新增 `copy_with_boundary_observation` 把观察绑定到真实 `copy_own_slots` 调用、actual-copy EvidenceRef 和直接复制后的 destination checkpoint。

这是必要的独立轴：源当前内容可能未知，旧 `copy_own_slots` 仍可保存 `ir_copy_surface_or_exclusions_not_certified`，而新关系只在既有 whole-source own-enumerable copy 条件内证明该次当前 slot 的复制和后续保留。它不建立新 FieldSlot，不重建旧参数 provenance，不认证 child，不授予普通 Set 能力。已知 absent 的 source slot 不发布 vacuous positive。未知 presence 的正项仍携带“所选当前自有可枚举字段存在”与“实际复制正常完成”的前提。

adapter 在实际 literal 的每个 spread 位置创建观察；源值在该次表达式求值后捕获。suffix 来自该 literal 的后续 AST 成员，要求都是规范化静态键的数据定义，不接受后续 spread、computed key、accessor 或特殊 `__proto__`。`later_definition_keys` 与所选键的相交会阻止保留关系。新的数据定义沿用 literal 构造路径，普通 assignment 仍走未建模 Set 的 effect 路径。

保留检查发生于 `finish_construction` 之前；同时检查 fresh、escape、external-alias、conditional-allocation 和相同 construction guard。输出明确标记 `literal expression before exposure and promise assimilation`，并保留 `initial_parameter_origin_proven=false`、`presence_proven=false`、`fulfilled_value_proven=false`、`transport_proven=false`。assessment 仅为实际所选 literal operand 附加该观察，原来的 source-form 判定与 async 强制 unknown 路径没有从新 local-copy 布尔位取得权限。

这些限制支持 agent `:490` 的局部命题：在当次合法复制中若复制了 `maxRetries`，后续 `agents`／`agent` 的固定定义不覆盖那个 slot。它仍不证明前缀调用／await 未改变 metadata，也不证明返回 Promise 的最终值。

## 审查中发现的实现问题与修补状态

### 目的对象 effect 不能仅靠 escape 状态检测——已读到修补

初版 `retain_copy_to_literal_end` 只检查目的对象的 fresh／escape 状态和 construction guard。公共 `invalidate_reachable(..., escape_roots=False)` 可以调用 `_damage` 改坏目的对象，却不清除 construction guard 或 fresh；因此初版公共协议可能在真正 mutation 后仍给 positive。该问题已先行反馈根代理。

最终冻结版本补入了 actual-copy checkpoint，并拒绝 state 中任何 `affected_allocations` 包含目的对象的 EffectRef。检查全部已保存 effects 而不只取 ID 差集，可防止 canonical effect 去重隐藏重复 mutation。另比较复制后与终点的 barriers／copy layers／base shape、所选 FieldSlot，并拒绝不属于已认证 suffix 源码位置的新 destination operation evidence。这个修补在源码层关闭了上述 `escape_roots=False` 漏洞；它允许 unknown copy 自身造成的抽象来源障碍继续存在，但不允许后来真正的目的对象效果被忽略。

初版还有一个防御检查的证据种类差异：actual literal write 的 EvidenceRef 与 `literal_suffix_definition` 的 EvidenceRef `kind` 不同，故 exact-record membership 不能识别同一位置。最终 adapter 的普通 literal data write 与 suffix refs 均使用 `literal_suffix_definition`，该差异已消除；`later_definition_keys`、checkpoint selected-slot 比较与 occurrence 比较也独立阻止同键覆盖。

### 源码扫描漏掉循环赋值目标——已修补并复核

初版 `field_relations._Collector.prefix` 会记录 `for_in_statement` 等 unsupported control regions，但 negative-scan 的 `complete = not self.incomplete and not unmatched` 不消费这些 regions。`_WRITES` 只包含 assignment、augmented assignment 和 update；例如源码 `for (metadata.maxRetries of values) {}` 的迭代目标不是这些节点。初版可能保存 `scoped_enumeration_complete=true` 和 `no_explicit_static_target_match`，尽管该位置明确写入所选成员。

这是新 source-only 输出自身的准确性问题，不能靠 `no_indirect_mutation_proven=false` 消除。最终 `field_relations.py:504` 的 `complete` 增加 `not self.prefix_controls`，同时保存 `unmodeled_control_or_write_regions`。未明确见到同键写入且存在未建模 control 时，verdict/status 降为 unknown；`direct_prefix_write_coverage_complete` 单独消费该完整位。后续预算截断仍会降级并重算记录 ID。该修补关闭了负向完整性漏洞。未执行上述示例或测试。

## 普通 Get 修复

当前 `ordinary_get` 在转发 selected ValueRef 前要求 `selected.closed`，同时排除 Projection barriers、ValueRef barriers 和 `capture_unknown`。absent→undefined 分支同样检查 closed 和两层 barriers。

这纠正了旧版的一处实际协议漏洞：IR 失效会把 FieldSlot 标记为不闭合并加 barrier，但保留旧 ValueRef 供审查；旧 Get 仅检查该旧 ValueRef 的 `capture_unknown`，可能误把它重新当成当前读取值。新分支返回有界但来源未知的值，不恢复先前 slot 来源。这是正确的保守修补，不应为保持旧数字而取消。

正常的 when-present 来源不要求 presence=present；存在性仍可未知。修补也不应把先前不可逆地损坏的源当前版本与独立 copy-time snapshot 混淆：若实际被读取的是未损坏的复制快照，应保留它自己的 closed/value 证据，不能用来源对象后来的 damage 反向损坏历史捕获。

## 内容 ID、证据与来源关系输出

两个新 typed record 的 factory 先用空主 ID 构造完整 immutable 内容，再 `_digest` 并填 ID；wrapper 在添加 actual-copy checkpoint 时先清空旧 observation ID 后重算，避免改内容复用旧 ID。嵌套 source／destination snapshots 和 guards 都进入 canonical 内容。正式复核仍需对保存结果逐记录重新计算 ID，并核对同 ID 不对应不同内容。

`field_relations` 在输入处验证 saved document、lexical document、真实 definition、site owner 和 subject 参数声明。它输出的 path 是带声明身份的语法路径；没有把路径相同当成稳定 receiver。const initializer 的 alias 仅代表初始化依赖，不声明入口参数值或当前两变量相等。ordinary member writes 始终标记 attempt；顺序关系限定为同一 block 中“双方正常到达时在前”；return 关系停留在 body-return 源表达式层。

source-relation IDs 包含来源位置、snapshot／parse／context、分支、payload 和状态；末尾若预算耗尽导致负扫描降级，代码会重新计算该 scan 的 ID。新的 AST 关系没有回写公共 IR，也没有给原 source-form、presence、runtime、transport 或 fulfilled 升级。上述循环目标遗漏说明 source-only 负证也必须有完整范围证明，不能只看输出级别不同就放宽准确性要求。

## engine 回退的原因、修补与稳定保存观察

早期开发查询 `PREFREEZE_FIELD_OBSERVATIONS.json` 中 engine 为 unknown。独立对照 iteration8 与该开发 JSON，两者在真实 `buildServices :73` 上具有相同旧 callable ValueRef，且 `capture_unknown=true`。iteration8 仍展开 helper；新代码加入 `not callee.capture_unknown` 后停止展开，helper `:155` 的 closed own-shape 证据随之缺失。回退的边界是严格 capture gate；没有发现新 Get 检查把合法闭合复制 slot 错误拒绝的证据。

进一步定位到 `LexicalBindings.unbound` 的 fallback 对已支持参数模式遍历整个子树，把 `env = process.env` 右侧的 `process` 误当潜在 binder。最终 `lexical_bindings.py:263` 改用已有 `_binders` 枚举真实声明 token：required/optional 参数只取 pattern/name，assignment pattern 只取 left；不支持的模式仍抛 `_UnsupportedPattern` 并回退旧保守 walk。已有 binding、shadow 与 eval 检查未放宽；default RHS 自身仍参与别处的读写/effect 分析。该修补只改善“捕获源码中无此局部声明”的证明，不认证全局 `process` 的运行时值。lexical 版本由 2 更新到 3，严格 helper capture gate 保留。runtime-only traversal 的 type wrapper 解包和 type subtree 排除也已复读。

旧保存结果中不闭合的 actual Gets 包括 `opts.jobId/routing/agentAvailability/agentHealth/teamPolicy`；它们读的是已被 effects 损坏的外部 opts。`jobOptions.env` 的自身 slot 读取具有独立闭合复制来源，另一个同文本 `.env` 是 `process.env`。修补没有取消 damage 检查，也没有把前者的旧值复活。

新 `PREFREEZE_ENGINE_OBSERVATIONS.json` 的 SHA256 为 `8592c1ef94baaadf70a62c9d33f5720501ed2f982acac4b020c114a566585897`。其中 query 前后 tool identity 均为上述冻结 `389335…`，`query_core_bytes_stable=true`；来源是 iteration8 已捕获快照，非本轮正式重扫产物。保存结果中 `buildServices :73` 的 `capture_unknown=false`，`:155` helper 返回 `maxRetries` absent、selected/whole shape closed，`incomplete_or_fallthrough=false`。engine assessment 为 `source_form_preserved_when_present`，`source_complete=true`，field presence 仍 unknown，whole shape 仍 false，runtime／transport／full-functionality 均 false。新 local-copy 汇总为 false：末次 `services` spread 的 selected key 已知 absent，不把 vacuous 条件计为进步。

## 冻结前仍需完成的事项

上述源码 blocker 均已关闭，预冻结审查可进入正式产物阶段。已保存的早期开发结果中，两个新 typed record 共 66 次出现／60 个独立内容 ID，逐条重算无不匹配；41 个 source-relation 与 3 个 copy-plan ID 重算一致，所选新轴的 173 个来源 span 与 58 个 typed EvidenceRef 位置匹配真实目标字节。这些是开发证据检查数量，不是最终冻结验收或覆盖率。正式两库扫描仍须重新核对原五个 field 分支评估、helper ownshape／absence、既有 navigation／atomicity／budget 关系，以及新增局部轴的 actual-copy、effect、guard、内容 ID 与来源证据。标准库源码检查不替代这些正式扫描。

本报告不会把局部 positive 数量当作覆盖率，也没有修改原五目标／30 必要义务的 `0/5` 完整结论。
