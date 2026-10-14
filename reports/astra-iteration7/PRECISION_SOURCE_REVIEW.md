# Astra 独立源码复核：v9 字段精度退化

日期：2026-10-12。状态：开发阶段只读审查，**不是新版本正式验收**。本代理读取 v8/v9 冻结结果、v9 字段核心及真实目标源码；核心开始开发修改后，不把工作区中的新代码当作冻结 v9。本稿不编辑核心，不导入或执行目标、CallScope 分析器、工具测试、目标测试、构建、安装、目标 CLI、目标 code-index 或浏览器。

结论：真实 `buildServices` 的局部 own-key 缺失证明有保留价值；v9 丢失它至少有两个明确的表示／适配断点。修复应保住私有新对象的关系并继续分析真实 effects，不能用“已知返回字面键”清除前缀效果，也不能把普通属性读取或 Promise 履约等同于 own-slot 查询。

来源包：[PRECISION_SOURCE_REVIEW_EVIDENCE.json](PRECISION_SOURCE_REVIEW_EVIDENCE.json)。采集脚本只读 JSON 和源码字节：[collect_precision_review_evidence.py](collect_precision_review_evidence.py)。其中的 10 条 site 记录是同一五个位置的 v8/v9 两次保存结果，24 条事实是因果复核选样，均不是新增能力分母。

## 1. 旧局部结论在什么意义上有效

真实 [engine-runner.ts](/workspace/codepatchbay/server/services/engine-runner.ts:73) 中，`buildServices` 是同步普通函数。`:85–119` 的 `ports` 外层字面量只有固定数据属性，实际键为 `createJob`、`startPhase`、`completePhase`、`completeJob`、`failJob`、`blockJob`、`appendEvent`、`prepareTask`、`getPool`、`getArtifactIndex`、`providerServices`。没有外层 spread、computed key、accessor 或特殊 `__proto__` 设置，`:121` 紧接着返回该绑定。

在所有初始化正常完成且返回该对象的条件下，`ports` 是新建普通对象，上述固定定义给出完整的自有键集合，因此 **`maxRetries` 不是它的自有键**。该事实不要求这些端口的值已知，也不要求 `buildCreateJobPort`、broker getter/`.bind` 或 `prepareTaskForEnv` 纯净。它们可以改变可达外部对象或抛错，但不能仅因发生调用，就改变尚未暴露的 literal 临时父对象。

这里应从源码证明“父对象尚未暴露”，不能只靠 `const`：`ports` 在字面量完成前尚未初始化；该源码没有把它交给 initializer；已建立和存入对象的闭包不捕获 `ports`；绑定完成后至同步 return 没有另外调用或写入。键、initializer、capture、escape 和 return 覆盖都应由实际 AST／词法身份导出，不得从本报告或策略预填。对象中的未知值可能引用外部对象，**外部对象的反向指针不能因此被虚构为指向尚未暴露的父对象**。

据此，v8 保存的 `selected_field_presence=absent`／局部 whole shape 可以在这个真实函数的正常返回关系内成立。它不是以下结论：

- 一般 JavaScript 的 `services.maxRetries` 必定为 `undefined`。普通 `Get` 还可能沿 prototype 查到值或调用 getter；spread 的 own-key 枚举不沿 prototype 复制缺失键。
- 参数值是数字或预算被消费。`...services` 在该局部条件下不覆盖 `maxRetries`，不自动完成上游运输、实际消费者、比较和预算归属。
- `buildServices` 一定返回、外层正常前缀必然到达、`runJobWithServices` 的 Promise 必然履约。它们需独立的 completion／activation 关系。
- 对任意相似函数都可重建形状。computed key、spread、accessor、`__proto__`、反射、真实 escape、返回分支缺失或未建模控制流仍阻止这份负证。

v8 的最终 engine 字段端点也仍是 unknown；该局部缺键事实不能倒推出 v8 端到端已通过。

## 2. v9 的第一个断点：合流抹掉已知外部可达域

正式 v9 engine 事实的执行顺序可以直接对照机器包中的 JSON pointers：

1. `source_facts/16` 保存 `:137` rest 的新 allocation：fresh=true、escaped=false、没有 barriers。被排除的五个键来自实际 pattern。
2. `:142`／`:143` 两个路径 helper 的 call 和 await 结果各保存 `bounded_external_value_domain`，并保留完成态／内容未知。effect 样本还显示此时新 rest allocation 仍在 protected 集合。
3. ternary 经 `join_values` 产生 `kind=join`。冻结 v9 `semantic_ir.py` 的 `_external_domain` 从 `external_alias` 开始检查，没有递归处理 alternatives；join wrapper 本身没有这项来源属性。真实支上的证明因此没有进入 subsequent read 的判定。
4. `source_facts/36–43` 对 `:141` 三个解构 Get 显示 receiver allocation=null、Get guard unsupported、effect roots_complete=false。缺少 root ObjectVersion 足以让读取值／own-shape 未知，却**不应另外抹掉已经独立认证的外部可达域**。
5. `ordinary_get` 将 domain=false 交给 `effect`，`invalidate_reachable` 扩张到当前 visible roots，再把可见 binding cells 改成 `ir_captured_binding_write_possible`。这包含私有 `jobOptions`。随后 escaped cells／unknown captures 的保守传播污染后续对象和 helper；`:149` 的 `opts.jobId` 和 `:151` 的 `jobOptions.env` 连根 receiver 都已丢失。

建议：对有界 alternatives 逐支证明外部可达域，并保留 union 的真实 alias／capture 根。所有可能分支都须获得证明；任一无证明、预算超限或反射分支仍 unknown。primitive／null 的 normal Get／throw 语义须单列，不把“没有对象引用”写成“读取必定成功”。这种精化只证明效果不能凭空接触尚未暴露的 caller-local allocation，不认证 receiver own-data 表面、读取结果、无副作用或正常完成。

同时注意 `bounded_external` 原先只收集直接 root.object_ref／alias_roots。提升 join 时不能只修布尔判定而丢掉嵌在 alternatives 中的真实 alias 和 capture roots。可在公共 IR 中建立通用的有界域／根遍历接口，复用现有 EvidenceRef 和 reachability；不要在 adapter 中另建不受审计的别名系统。

## 3. 第二个断点：callee 的域证明未用于调用效果边界

冻结 v9 `FieldSummaryBuilder.call` 的 `complete` 只接受已认证 module target，或者 `kind=callable` 且 capture 完整。`Object.assign` 和 broker 成员取得的值即使已有 `bounded_external_value_domain`，仍是 `kind=unknown`，因此调用又按 captures 不完整处理。

正式 `:126` 的证据显示，`Object` 与成员 Get 有外部域记录，随后 `Object.assign(record, recordValue(value))` 的 scope fact 却 roots_complete=false。这会扩张到 `envRecord` 可见绑定，并通过已经逃逸的域传播至调用者。`buildServices` 的 broker Get／`.bind` 和 `withJobOptions` 分支进一步放大失效；最终 `source_facts/175` 保留 11 个字面键但 whole shape=false，`/177` 的 helper `maxRetries` 判定变为 unknown。

建议：只在真实 callee 值有来源域证据时，允许证明它不能额外词法捕获当前未暴露的 caller-local cell；callee 本身、receiver、实际 arguments、已知 captured cells、external／escaped roots 仍全部参与效果可达性。不能仅设置 complete=true 而漏掉 callee 的引用／闭包根。实际目标绑定、返回值和 throw 仍可未知，不能把该域证明转成 pure、标准 API 身份或成功 invocation。

调用效果、对象形状、slot 内容、binding 可写性需要分别记录。未知外部内容不是任意局部变量赋值；真实 escaped closure/cell 则必须继续使后续重绑定和对象可达域失效。以后初始化的新对象也不能因旧的全局 `unknown_captures_escaped` 位自动永久失去所有精度，除非来源证据确实覆盖其 cell／allocation。

## 4. helper 前缀与其它四个端点的必要限制

`buildServices` 的参数 destructuring/defaults、`envRecord`、`instanceof`、broker 属性取得／调用都发生在 return 前。修复必须保留它们对可达参数、外部域和共享子对象的影响；initializer 的先后顺序也不能改成“所有键先建立后无条件忽略 effects”。可分别保留 fresh parent 的键事实和 child 值未知。

[agent-config.ts:471](/workspace/codepatchbay/server/services/agent/agent-config.ts:471) 的 `metadata` 是传入外部对象，前缀调用／await、动态 import、`metadataRecord.agents` 与 `mergeAgentConfig` 的别名效果尚未闭合。直接 `return metadata` 和 `{...metadata, agents, agent}` 是不同关系，必须独立评估。即使 body return 的字段源式恢复，async Promise resolution 会读取 `then` 并可能同化 thenable；own-key 缺失不排除 inherited `then`。不得用同步 fresh ownshape 的恢复直接设置 fulfilled=true。

[hub-queue.ts:1550](/workspace/codepatchbay/server/services/hub/hub-queue.ts:1550) 的 metadata 缺省支和已有支仍不同。外层 `normalizedInput` 是浅复制；已有 metadata 是共享子引用，其普通 Set／getter／Proxy 效果不由 copy/Get 模型认证。新建空 metadata 不能称为保留既有值，后续整属性替换不能与子属性写入合并。callback activation、旧 pending 复用、新 entry、commit 和消息／记录身份也仍需独立分析。

## 5. 新版本正式复核的要求

修复验证应使用两库真实保存源码的正常静态扫描，保存新的工具／政策／快照身份，并与冻结 v8/v9 的同一五个实际位置和分支比较。若政策或模型前提变化，应单独说明，不把增强前提计为精度改进。开发观察不能代替冻结后的正式结果；本代理尚未进行新版本正式裁决。

至少应检查：私有 rest 的 copy-time 来源是否保留；真实 `buildServices` 全正常返回的 own-key/absence 是否恢复；真正暴露的对象、共享 child、捕获 cell 和未建模 Get/Set 是否仍失效；每次正向结论有实际 receiver/version/branch/effect 证据；async body 与 fulfilled 值仍分开；未解析、超预算、漏分支和截断不被当作已关闭。

原 [五目标／30 必要义务合同](../astra-iteration4/GOAL_ACCEPTANCE.md) 的 SHA256 仍为 `9b6f4fda6aa24f055e288690e76405779e36758f8ba986799f78f2f96aa8d118`。v9 正式结果仍是 0/5 完整目标。即使 engine 单个字段端点恢复，也只改善 CPB-01 P3/P4 中的有限来源段；不降低合同、不删除 unknown、不把事实数、组件数或模型数当覆盖率。最终仍须对原 30 项义务和旧 navigation／atomicity 的具体关系逐项复核。

## 6. 开发修改的独立追审

本节追加审查期间已经出现的开发代码，尚未冻结或正式验收。`LITERAL_LIFETIME_DEVELOPMENT.json` 中工具身份 `c878aa10…b67e2ecfc4` 的保存观察恢复了 helper 的 local absent／whole shape，engine 端点仍 unknown；本代理只读取该产物，没有执行它的采集器或分析器。这支持继续定位，而不是提前宣布修复完整完成。

**临时 literal 域保护原则成立。** 新增 allocation 专属 `private_literal_construction` 能保留未暴露目的对象，前提是只从 actual AST 建立证据，且只免除 wildcard fallback：真实 reach／alias／visible root、反射、预算耗尽和不完整状态不能被免除；结束构造必须在绑定、return 或实参暴露前释放能力，不能恢复已经损坏的 slot。child 不继承 parent 的保护。含 spread 的 literal 也可以拥有匿名目的对象，但 unknown spread 必须继续直接损坏目标形状，临时隔离能力不构成 copy 负证。

公共 `join_states` 还应要求所有参与版本具有相同有效 construction guard 和同一未结束 lifetime；缺支、某支已 finish 或 guard 不一致时清除。不能通过 `replace(available[0], ...)` 自动保留首支的临时能力。这是通用 IR 的合流条件，不能只凭当前示例没有触发就省略。

**新增 callee root 暴露了 capture collector 的顺序问题。** 冻结 v9 的 `callable` 在查看 `declaration_span` 是否位于被分析函数内部之前，先调用当前 caller context 的 `key_for`。目标模块函数自己的形参／局部声明属于目标 activation，当前 caller 无对应 active context，于是 `key_for` 可先返回 None；collector 随即设置 capture_unknown，根本没有走到“内部声明不属于捕获”的排除分支。callee 加入 effects 的 roots 后，`_reachable` 即使面对 module scope complete=true，也会因这个误报 capture_unknown 再次 wide。

建议先从 lexical.resolve 的真实声明身份排除函数子树内部的声明／参数和 import，再仅对真正 free variables 求当前 capture cell。不要通过删除 callee root 或无条件忽略 capture_unknown 规避。

真正自由的 module cell 则必须保留：若其内容尚未进入 state，可以从已认证模块词法身份建立外部域证据，同时保留 live cell edge 和未来 rebind／escape。不能按名称或当前 primitive 值剪掉该 cell；否则会重新引入模块状态后续赋值、晚初始化捕获和真实对象逃逸的旧漏洞。

## 7. 模块自由 cell 修复的冻结前复核

本节所读开发版本的 `field_summaries.py` SHA256 为 `a3730b7c2684817d36cc92dcfb7b9df7b03c994a2943b9ee8facbfd3d77afbb9`，`semantic_ir.py` 为 `95896a0352877ef768dfbb84b15e1b19cb926b76140335eeb43729d4761f66f3`；它们不是本轮最终冻结身份。

模块缺失 cell 的处理在其声明范围内合理：`key_for` 先要求 unique 的真实词法声明，沿声明祖先确认没有函数 activation owner，才取得模块 BindingKey；`callable` 只为尚未进入 state 的该 cell 创建有来源的外部域未知值，保留 live captured_bindings。后续读取与显式赋值仍使用相同声明身份，模块赋值的 escape 逻辑没有被删除。已有 state 值没有被重新 seed 覆盖，未来初始化／重绑定也没有按当前 primitive 值剪枝。该模型不证明模块内容、标准 API、纯净性或运行成功。

`bounded_external` 现已递归收集 alternatives 的 alias roots 和 captured cells，补上原直接根收集的缺口；构造 guard 的合流只保留全部一致的 lifetime，缺 allocation 支、escape 和 allocation reuse 均清除。建议通用 `finish_construction`／defensive bind 同样覆盖 join alternative 值；当前 AST adapter 在 literal 返回前已经显式 finish，故该项是公共 IR 协议一致性要求。

保存证据还应直接关联模块 seed 的 declaration_id／location、BindingKey、seed value_id、only-if-absent 和 future-rebind 保留状态。仅有 `module:` 字符串和自然语言 basis 不应成为未来消费者的独立证明。

新增的冻结前检查项如下，均为只读源码推导，没有执行合成反例：

- **隐式捕获须保守。** 捕获收集器只处理 identifier／shorthand，箭头中的 `this`、`arguments`、`super`、`new.target` 不一定形成显式声明身份。尤其返回的箭头可通过外层 arguments 访问实际对象；把它当成无捕获 callable 后执行 opaque effect 可能漏掉该对象。没有对应隐式 capture 模型时应标 capture_unknown 并保存来源。进一步核对确认 direct eval／with 已由现有 LexicalBindings 的 scope 护栏保守处理，不需要重复建立一套 eval 模型。
- **TypeScript 擦除子树不应污染运行捕获。** `MODULE_CELL_DEVELOPMENT.json` 的 engine 事实已恢复 `:151 jobOptions.env` 的私有 receiver／slot 来源，但 `buildServices` 和 `:82 withJobOptions` 仍 capture_unknown=true。真实 `fn: (...args: unknown[]) => unknown` 的 `args` 只是函数类型形参；全量 `walk(node)` 会把这个名字送入 runtime capture 判定。应跳过 type_annotation／type_arguments 等擦除子树，同时继续遍历真实嵌套函数体，不能按 `args` 或文件名特判。
- **后续精度边界需要分开。** opaque effects 当前对 captured cell 一概写成通用未知；对真正可变或尚未初始化的 cell 仍应保守。若恢复已初始化 const cell 的读取身份，必须使用实际 declaration-kind／初始化和写入证据；不能因 lexical cell 不可重绑而认证它引用的对象内容不可变。此项尚未声明为正式新结果。

开发产物 `MODULE_CELL_DEVELOPMENT.json`（工具身份 `04f7b417…207d67b6`）仍保留全部五个 unknown 端点，helper local absent 恢复。它没有修改 0/5 完整目标结论，也不能替代冻结后两库正式扫描。

## 8. 冻结前最终源码结论

本代理完成后续修补的只读复核，**未发现阻止冻结后正式扫描的源码问题**。这不是测试通过或 v10 正式验收。最后读取的 `field_summaries.py` SHA256 为 `10f33804c3b77913aef29e12a0a00c24ea43ab61f7c09276ed053becb7d69443`，`semantic_ir.py` 为 `c8fdf5ae9a0693708b43055411d6f58fcdd191ba5096ea2a7a8b53bb9294044a`。复核机器包：[PREFREEZE_PRECISION_SOURCE_REVIEW_EVIDENCE.json](PREFREEZE_PRECISION_SOURCE_REVIEW_EVIDENCE.json)；其采集器只读取保存 JSON 和源码字节，没有导入分析器。

第 6–7 节的问题已有具体修补：runtime capture 遍历跳过 TS 注解子树且仍进入真实嵌套函数体；隐式 `this`／`arguments`／`super`／meta-property 保持 capture_unknown；join alternatives 的构造保护会结束，bind 有防御性 finish，escape／reuse／缺支清除临时能力。const 的 guard 来自实际声明，仅禁止 opaque effect 虚构该已初始化 cell 的重绑定；引用对象和 captured cells 仍参加 damage／escape，显式非法 const assignment 不更新成新正常值。缺失的局部 captured cell 未被降成无捕获值。

模块 owner 的公共协议也已收紧：新增 `BindingDomain(binding, guard, evidence)`，只在携带有效 `external_lexical_cell_domain` 的 bind 注册；adapter 的 guard 绑定真实 unique 模块声明位置，seed 另存声明身份／BindingKey／value_id。`invalidate_reachable` 的有界替换读取该类型化 membership，而不再把 `module:` 字符串当权限。替换值仍 unknown，其 alias 域包含受影响／暴露 allocation，capture 域包含记录的 live cells，旧形状不会恢复；反射、预算和不完整状态继续 unbounded。合流只保留每支都存在的相同 owner 记录。

`RUNTIME_CAPTURE_DEVELOPMENT.json` 的工具身份为 `80a5d491499451d1391f531e61a6f7cc6d5f4a58d51317c19e0082eedf172bbd`，文件 SHA256 为 `f7708e135fdedafd129842dff2d9fcac2072797d092989d339b599d50b29fcfd`。其中 engine 正项的具体依据可追溯：同一 `opts` BindingKey、parameter 0、`[maxRetries]` 来源，经 `:137` rest 的 copy-time snapshot 到 `:158` spread，两个 ObservationRef 使用同一 captured_value_id；`:176 ...services` 的 outer own-key 缺失不覆盖该值，后续固定键也不是 maxRetries。保存的条件仍要求 normal prefix 和各自有版本的 copy／Get 模型。

因此该开发结果只支持 **call argument before callee activation 的 `source_form_preserved_when_present`**。presence 仍 unknown，whole object 仍不封闭；reaching value、opaque effects／exceptions 排除、实际运行、transport 和完整功能均未升级。helper 的正常返回 ownshape／absence 恢复而 `normal_prefix_effects_unknown=true`、`invocation_or_completion_proven=false` 仍在。其余四个字段端点仍 unknown，async return 没有改成 fulfilled 身份，原五目标／30 义务仍完整保留。

机器包独立核对的 42 个去重来源位置／EvidenceRef 的文件字节和可用 span hash 全部匹配；这是审查证据定位数量，不能作为能力覆盖率。该开发 query 早于最后的 typed owner／seed 证据／构造协议修补，故仍须等待最终冻结身份的两库正式保存结果；不得把它的 tool hash 当作正式 v10。

## 9. 首次 v10 冻结后的证据 ID 补充审查

根代理在最终交付核验中发现，模块 cell effect replacement 用 `replace(evidence_ref, guard_ids=..., kind=...)` 改写 EvidenceRef 内容却复用原 `evidence_id`。该 ID 的公开构造公式包含 guards 和 kind；即使 `_supported`／`_unique` 当前读取完整记录，此写法仍违反公共 IR 的内容身份约定。本代理同意应改用 `evidence(...)` 构造新记录，再冻结和正式重发；第 8 节源码通过结论不能当作对这一新问题的最终批准。

独立检查首次冻结 `dc5abc91…` 的 CPB 正式快照 `38ac19d2…` 已导出的所有 typed EvidenceRef，按原公式逐条重算，实际发现 **0 个 ID 内容不匹配、0 个 ID 对应多记录碰撞**，记录在 [EVIDENCE_ID_REVIEW_INITIAL.json](EVIDENCE_ID_REVIEW_INITIAL.json)。因此目前证据是内部构造协议的源码缺陷，不能写成已经观察到正式保存 JSON 的碰撞或已经证伪 engine 正项。最终审查将对修正后的冻结身份重做正式数据核对，并加入完整 ID 重算、guard 规范化和 ID→记录唯一性检查。
