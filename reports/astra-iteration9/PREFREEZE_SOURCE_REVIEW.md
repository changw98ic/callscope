# iteration9 字段来源的冻结前独立审查

本报告由 Astra 代理独立只读审查真实源码及 iteration8 保存结果后编写。它是开发建议，不是新版本正式验收。未执行、导入、构建、安装或测试 CodePatchBay；未运行目标 CLI、仓库命令或 CallScope 测试。仅使用文件读取和标准库 JSON／哈希检查；没有修改核心、旧报告、policy、基线或目标合同。

**结论：现有 copy/Get 条件不足以把剩余四个字段端点评估改成正项。可以新增有证据的局部关系，尤其是词法别名、分支、浅复制共享引用、实际写入位置、有序字面量的固定键不覆盖，以及 async 的 body-return 关系。它们必须与入口字段保留、字段当前内容和 fulfilled 值分别保存。**

## 读取身份与既有结果

原五目标／30 必要义务合同 [GOAL_ACCEPTANCE.md](../astra-iteration4/GOAL_ACCEPTANCE.md) 的 SHA256 为 `9b6f4fda6aa24f055e288690e76405779e36758f8ba986799f78f2f96aa8d118`。本轮没有改变这个分母或达成条件。

| 本次读取文件 | SHA256 |
| --- | --- |
| `server/services/hub/hub-queue.ts` | `0bd13766a2a2fcd271c2ead8166fbbd6f782fde32f63954ccced88a4cb2de02c` |
| `server/services/agent/agent-config.ts` | `83a2eef775f1ff274054ee16fa749e195ae5a475f42abf520b2434e7ed6af484` |
| `core/job/meta.ts` | `2e40a285e1ea4c28af9fb7d949e026a3edd74c2471e726ff702f1aa2a9ac0319` |
| `callscope/field_summaries.py` | `10f33804c3b77913aef29e12a0a00c24ea43ab61f7c09276ed053becb7d69443` |
| `callscope/semantic_ir.py` | `b430f7ce224f7321fc6541bc11c378ac57f6572ad9d9333b955871a3823a4539` |
| iteration8 `codepatchbay-policy.json` 原始文件字节 | `134671b5cb1cc7f6acb3514e63eac6a1e7bd3d53d48b750d38d8d35b9b63faa0` |

两份主要目标源码的哈希与 iteration8 `field-assessments.json` 中对应位置保存的 source hash 一致。表中 policy 文件字节哈希不等同于分析器规范化 policy hash。读取时 iteration8 冻结包版本为 `0.10.1`、publication series 为 `v10`。

iteration8 的三个 field 合同共保存五个分支评估：engine 一个 `source_form_preserved_when_present`，queue 两个 unknown，agent 两个 unknown。queue 的两个评估对应同一 `:1580` 调用位置的不同 `:1570` 分支，不能计成两个不同调用位置。具体保存障碍如下。

| 评估 | iteration8 结果／障碍 | 本审查裁定 |
| --- | --- | --- |
| queue `:1580`，`:1570` then 缺省支 | unknown；`field_get_value_origin_unknown` | 最终 `maxRetries` 来源继续 unknown；可保存缺省分支和新对象语法事实 |
| queue `:1580`，`:1570` else 已有支 | unknown；`field_get_value_origin_unknown` | 最终 `maxRetries` 来源继续 unknown；可保存浅复制共享子引用和实际 Get/Set 序列 |
| agent `:487` 直接 return | unknown；`ir_captured_binding_write_possible` | 可进一步闭合词法参数引用／body 直接返回关系；入口字段内容及 fulfilled 继续 unknown |
| agent `:489` 对象 return | unknown；`ir_copy_surface_or_exclusions_not_certified` | 可闭合有序成员及局部不覆盖关系；入口字段来源及 fulfilled 继续 unknown |

这些局部改进不自动改变原来的 `0/5` 完整目标、4 supported／20 partial／6 unknown 义务结论。

## queue：浅复制的父对象与共享 metadata 必须分开

[hub-queue.ts:1550](/workspace/codepatchbay/server/services/hub/hub-queue.ts:1550) 的相关次序是：

1. `:1551` 检查 `input.projectId`；正常前缀不经过该 throw。
2. `:1554` 调用 `buildMeta(input)`，`:1556` 至 `:1559` 调用 `stringOrNull`。
3. `:1561` 创建 `normalizedInput`，先 `...input`，后固定定义 `projectId`、`sourcePath`、`sessionId`、`workerId`、`cwd`、`executionBoundary`。这些固定定义均不是 `metadata`。
4. `:1570` 在 `!normalizedInput.metadata` 分支尝试把整个 `metadata` 属性写成新的 `{}`。
5. `:1571` 至 `:1573` 写入子属性 `acpProfile`、`uiLane`、`uiLaneReason`。`:1572` 还调用 `Boolean`。
6. `:1574` 可能 throw；`:1579` 可能调用 `process.cwd()`。
7. `:1580` 的第四实参是 `normalizedInput.metadata`，对应 `resolveAgentsForEntry` 的 parameter index 3。

`buildMeta` 的实际声明在 [core/job/meta.ts:15](/workspace/codepatchbay/core/job/meta.ts:15)：它读取 `input.projectId/sourcePath/sessionId/workerId/cwd`，按 `||` 选择返回字段，返回新字面量；没有直接 metadata 写入。`stringOrNull` 在 [hub-queue.ts:371](/workspace/codepatchbay/server/services/hub/hub-queue.ts:371)，只有 `typeof` 检查和返回。以通用、有预算的 helper 摘要解释这些源码，可减少前缀不必要的 opaque barrier；默认形参、实际 Get、调用目标和每个 return 仍须认证。仅记录 helper 名或源码中没有 assignment 不足以证明它的读取无副作用。

### 已有支

若 `metadata` 在 `...input` 的实际复制时被复制，复制得到的是同一浅层值／引用。它没有复制 metadata 对象自身的字段表面。后面 `:1570` 的 else 表示该次 `Get` 的值为 truthy，不证明它一定是普通对象，也不证明 `maxRetries` 存在。

即使 `acpProfile`、`uiLane`、`uiLaneReason` 都与 `maxRetries` 字符串不同，普通 `[[Set]]` 仍可能调用自身或继承的 setter／Proxy trap，在同一 metadata 上修改 `maxRetries`。对 child 的实际 Get 也可能有 effects。外层 input 的 own-data copy 条件和外层 Get 条件没有递归认证这个 child。

这里存在有价值的**引用身份精度**：在这个 else 分支，若分析认证了实际浅复制、normalizedInput 的自有 metadata slot 未替换且新父对象没有逃逸，则它仍保存复制时的 metadata 引用。外部 child 的 setter 不能仅凭“可能有任意内容”获得随后新建、未暴露的父对象反向引用。这个判定可保存 copy-time observation、父 allocation、child 外部域、后续 effect roots 和分支条件。但是 child 的内容仍可能被修改；不能把父 slot 的引用身份变成 `metadata.maxRetries` 的稳定性。

当前 `field_summaries.py:642` 至 `:644` 对所有普通 Set 都做 `complete=False` 的 effect，因而会失去本来可证明的局部父对象／cell 精度。通用改进可以在 receiver 与 RHS 的来源域、真实捕获及 prototype 可执行代码的可达域已经认证时，收窄该 effect 的根。**根域收窄不允许把 Set 认定成无副作用，也不能调用 literal 的 `write_selected` 冒充普通赋值。** 对未知 receiver、真实捕获、逃逸、反射或预算不足，原来的保守行为仍适用。

### 缺省支

`:1570` 的 then 条件是 falsy；它不是严格的 absent 检查。`undefined`、`null`、`false`、`0`、`NaN`、空字符串等都可能进入。不能把它记为“原 maxRetries 缺失已证实”，也不能把新 `{}` 当作原 metadata 的来源保留。

`{}` 的字面量在建立时没有 `maxRetries` 自有键，这是初始化时的局部事实。后续赋值未闭合，故不能把这个 absent 延长到 `:1580`：

- 若 `normalizedInput` 已有可写的自有 metadata 数据属性，对它的普通写入有更窄的语义；若属性未被复制，给缺失 metadata 赋值可能碰到继承 setter。现有模型不证明这个分支中的两者一定是哪一种。
- 即使确实安装了新的 `{}`，该对象继承的 `acpProfile` setter 也可在 `:1571` 被调用并创建 `this.maxRetries`。一个只有 setter、没有 getter 的继承属性可以让前面的读取返回 `undefined`，所以 getter-free 的 missing-read 条件没有排除这种情形。
- `Boolean` 与 `process.cwd` 的源码名称不证明运行时实现纯净；实际来源审计和效果域仍要保存。

以上是静态语言层面的未排除情况，不是声称该仓库运行时已出现这些对象，也没有执行合成反例。

### queue 最少需要的额外能力

若后续要关闭这两个最终字段端点，需要新增并明确版本化、逐实际位置应用的条件或来源证明：metadata child 的相应数据表面／Get 条件；普通 Set 的 receiver、descriptor／prototype、成功写入和无额外效果条件；必要的运行时 builtin 条件或源内函数效果摘要。existing-own-writable-data 和 absent-key-create 两类 Set 不能共用一个未经限定的许可。

新模型应限定到真实 receiver version 和属性路径；不能因参数 TS 类型、`const`、已有 parent copy guard、或命中某个文件／字段名而授予。它也不能借默认分支的新对象回填已有分支的证据。若新 policy 引入这些条件，应作为条件增强单独发布和比较，不能计为与 iteration8 同条件的精度提升。

## agent：alias／body return 可前进，入口值与 Promise 仍断开

[agent-config.ts:471](/workspace/codepatchbay/server/services/agent/agent-config.ts:471) 的第四形参是 `metadata`；`:472` 的 `const metadataRecord = metadata` 是直接词法别名。`:473` 至 `:479` 包括三类异步前缀：`readHubConfig`、动态 import／`getProject`、`readProjectConfigFromRoots`。`:481` 至 `:485` 调用 `mergeAgentConfig`，其中 `metadataRecord.agents || null` 是共享 child 值。

`metadata` 是外部传入值。源码没有对它执行赋值，也没有在本函数中创建可将其参数 cell 暴露给外界的闭包。可以认证直接 alias、参数 binding identity 和 body 内无重新赋值／无局部捕获暴露的事实。外部调用或 import 不会仅凭发生调用就获得调用方尚未暴露的词法 cell。当前保存的 `ir_captured_binding_write_possible` 因而包含可精化的 cell 层损失。

这与对象内容不同：参数 referent 可能已有外部别名；await 期间的其它工作、被调用函数以及 `metadataRecord.agents` 的未知别名都可能触达它。`metadata.agents` 甚至可能指向 metadata 自身，不能凭 child 属性名推断它与父对象不相交。TS 类型没有禁止这样的结构。即使恢复 metadata cell 的引用身份，也不能删除其 ObjectVersion 的 effects 或恢复入口 `maxRetries` 来源。

### `:487 return metadata`

在 `Object.keys(merged).length === 0 && !metadataRecord.agent` 的 then 分支，返回表达式直接读取同一 metadata 参数绑定。这是有来源的 **body-return 引用关系**；该分支条件来自真实 AST，真假尚未证明。

可进一步证明的是：在这个 body return 发生时，表达式值是该局部参数绑定当前持有的值；若无重新绑定／cell 暴露的源码证明完整，还可把引用身份连回参数接收值。不可由此证明参数对象的字段从函数入口到此未变，也不可把它作为 async fulfilled 值的身份。

### `:489 return { ...metadata, agents, agent }`

`:490` 先复制 metadata 的可枚举自有字段；`:491` 再定义 `agents`；`:492` 再定义 `agent`。静态键集合 `{agents, agent}` 与所选键 `maxRetries` 不相交。这里的固定字面量定义采用新目的对象的数据属性构造语义，不是对外部 metadata 的普通 Set。

由实际 AST、有序成员和新 literal 目的对象的未暴露性，可以支持一个局部关系：**若 `maxRetries` 在该次合法 shallow copy 中被复制，它在这个 body 返回对象的 slot 中保留该次捕获的值／引用；随后的两个固定定义不覆盖它。** 该关系的起点是 `:490` 的当前 copy-time snapshot，而不是函数入口的 metadata 字段值。

`:491` 的 `Object.keys(merged)`、比较及 `:492` 的 metadata Get 可以有未知完成或外部 effects；按本源码，它们没有接收到正在构造的匿名目的对象。未知 child referent 没有隐式反向 parent edge。因此在所有成员求值正常完成且没有真实 escape 的条件下，它们不因此覆盖该临时目的对象的自有 slot。这一隔离不证明共享 child 当前内容不变，也不证明整个返回对象 own shape 封闭；spread 的键集仍可能 open。

实现时尤其不能用“当前 copy 条件成立”恢复此前被 effects 损坏的入口 provenance。可对当前 source snapshot 建立新的 observation，记录其捕获值未知，再证明 destination 没有后续同键覆盖；入口值到当前 snapshot 的关系仍是独立 unknown。把新 observation 冒写成旧参数字段来源，会把普通“从当前对象复制”错误升级成“原请求字段已保留”。

### Promise 边界

两个 return 都在 async 函数内。Promise resolution 会读取返回值的 `then`；自有或继承的 callable then、getter／Proxy、同化过程及抛错都可能改变最终结果或完成方式。新 literal 自有键没有 `then` 也不能排除继承的 `then`，何况这里还有 open spread。

existing actual-Get 模型仅针对认证的实际源码 Get，不包含由 Promise resolution 隐式执行的 `Get(result, "then")`。不能把普通 Get 的注册状态借给这个新语义位置。若要支持 fulfilled 身份，必须引入单独的 Promise-resolution／then 护栏及证据；body-return 的正向局部关系仍应单独保存，`fulfilled_value_proven=false` 继续保留。

## 建议的通用算法与输出协议

第一优先是新增独立可审查的局部关系，并保留五个现有端点评估和 final flags。通用关系应从保存 AST、词法声明身份和公共 IR 得到，不从 policy、报告文本、字符串匹配或仓库特判获得。

1. **词法值与对象版本分层。** 用 BindingKey／声明位置证明直接 alias、实际赋值、重绑定和捕获暴露；用 ObjectRef／ObjectVersion 记录字段与 heap effects。未知对象 mutation 不应自动变成参数 cell 重绑定，cell 引用稳定也不应清除对象 mutation。
2. **分支与替换顺序显式化。** 每条关系携带实际 branch guard 和顺序位置；queue `:1570` 的整个属性替换与 `:1571` 至 `:1573` 的子属性 Set 分开。join 只保留全部参与分支都支持的公共关系；缺分支和预算不足不得视为已闭合。
3. **复制时观察单独建模。** observation 绑定 source allocation/version、所选键、捕获 ValueRef、copy 操作证据及 branch。来源内容未知仍可保存“此次 copy 捕获了未知值”及后续 identity 关系；不得回填旧版本来源。parent 与 child 的 source surface guard 分开。
4. **有序写入的局部不覆盖。** 按 actual literal member 顺序检查后续静态键、spread、computed key、accessor、特殊 `__proto__` 及真实 escape。只对已认证的新 ordinary literal 的数据定义使用 `own_data_write`；普通 assignment 必须走 Set 路径。未知 spread、可能同键、反射或分析截断保持 unknown。
5. **完成阶段分开。** 关系应声明 `call_argument_before_activation`、`body_return_before_promise_resolution` 或具体 copy 阶段。async 的 body relation 不能改变 final `source_form_relation` 或 fulfilled flags；未知 normal prefix 仍需保留。
6. **逐关系证据与状态。** 保存支持类型（source 或 conditional model）、source hash/span、BindingKey／allocation/version、guard、所选字段、依赖 relation ID、完整性及独立 gaps。模型条件必须可追到注册 ID；自然语言说明或裸布尔值不构成公共 IR 的能力证书。

有限 AST 关系可以作为 source facts 交付；只有 adapter 实际消费公共 IR 证明并满足对应关系的所有前提时，才应标记其语义闭合。事实数量增长不改变目标分母。若仅新增关系输出，也要让报告说明具体关系的起点、终点和限制，不能用一个合计数字掩盖四个最终 unknown。

可随后考虑 effect-domain 精化：对合法普通 Set 的未知效果，区分“写语义未知”与“无法确定其词法捕获范围”；对 authenticated helper 的默认形参与动态 import，保留来源域但不授予纯净性。此类修改需要通用作用域、escape、alias 和 prototype 论证，不能只因当前 fixture 得到更好数字就通过。

## 冻结后独立复核要求

本报告没有批准尚未提供的新核心或正式结果。后续应在新冻结身份下用两库真实源码的正常静态扫描保存结果，并核对：

- 目标源码、旧 policy、基线和五目标／30 义务合同是否保持既有身份；若新模型条件变化，应分开列出。
- engine 原有 when-present 正项、helper 的局部 ownshape／absence，以及现有 navigation／atomicity／budget 关系是否保留。
- queue 两分支和 agent 两 body return 是否全部独立列出；局部 alias/no-overwrite 不得替代最终字段来源。
- 新关系是否使用实际 receiver/version、真实 BindingKey、branch 和每个 effect／write；存在未知来源时不能通过空集合、删诊断或新 seed 得到正项。
- 字面量 CreateDataProperty 与普通 Set、parent 与 child、copy-time value 与当前 referent、body 与 fulfilled 是否分别记录。
- 超预算、缺支、未解析、截断、动态 member、真实 capture／escape 和未知 Promise 同化是否继续阻止相应完整位。

复核只使用源码阅读和正常保存扫描／查询，不运行目标或工具测试。原完整目标仍需按原合同验收；本报告本身不构成任何完整功能达成证据。

## 后续设计复核：独立的 current-copy 语义轴

根代理提出在公共 IR 中增加 `LocalCopyBoundaryObservation`，单独输出 `local_current_copy_supported`，而不改变原字段端点的 `source_form_relation`。**这个方向有用，且在下列限定内 sound。** 这是设计复核；尚未读到该新类型的最终实现或正式扫描结果。

被证明的命题应完整表述为：在这个实际 spread 正常执行、当前源表面满足既有 whole-source own-enumerable copy 条件时，若所选自有可枚举键在该次复制中被复制，那么新 literal 目的对象的该 slot 保存此次捕获的浅层值／引用；其后被完整审查的固定数据属性定义不覆盖它，直到该 literal 正常构造完毕、尚未暴露或发生 Promise resolution 的边界。

这个命题不要求此前入口字段内容已知。源 ValueRef 由于前缀 effects 而 unknown 时，允许 source allocation/version 为空，但必须以实际 source expression 的保存位置、branch/context 和求值 ValueRef 标识这一次观察。这里记录的是表达式在该次复制中求值得到的值，不是之后再次执行同一表达式的值。不得根据这个 observation 新建带旧参数 provenance 的普通源 ObjectVersion，不得解除已有 barrier，亦不得把它作为已闭合的 FieldSlot 提供给既有入口来源检查器。

必要护栏如下：

- copy 模型授权必须来自已注册的既有 `own_data_copy` guard，并与实际 spread 的 EvidenceRef 绑定；不是因为出现 `...` 就无条件认证运行时普通数据表面。
- destination 必须是实际新建、尚未命名／暴露的 ordinary literal allocation；记录复制时的 destination version，以及覆盖整个相关后缀求值区间的有效 construction proof。不能使用过期、已 finish、已 escape、复用或不完整的 guard。
- selected key 必须是这个浅复制表面的单个规范化静态键。这个 observation 不授予嵌套 child 的表面、Get 或 Set 能力。
- 后缀计划须覆盖所有后续成员，记录其真实位置和规范化键。首版可只允许固定数据定义且全部键与 selected key 不同；后续 spread、computed key、accessor、特殊 `__proto__`、未知 AST、缺支、反射或预算不足应阻止正向 status。
- 后缀 initializer 的未知外部 effects 仍保存。private-construction 证明只用于说明它们无法获得该匿名 destination；真实 effect root／alias／capture 包含 destination 时必须失效。不能删除 effects 来取得局部正项。
- 此次观察内容、field presence、入口来源、共享 referent 当前内容和 async fulfilled 身份保持独立。when-present 和正常构造条件必须随 positive status 一起输出；原终点 unknown 和 `fulfilled_value_proven=false` 不变。

对 agent `:489` 的真实源码，`:490` 的 spread 后只有 `agents`、`agent` 两个固定数据定义，符合该计划的候选形态。prefix 可以改变 metadata 对象和它的字段，仍不妨碍证明“复制当前值之后没有在新对象上覆写同键”；两者有不同时间起点。新 relation ID 应涵盖实际复制证据、源求值身份、目标 allocation/version、所选键、分支及所用 proof／后缀计划，不能将自然语言计划或裸 `supported=true` 当作可复用 IR 权限。

同时复核了根代理在修改中的 `ordinary_get`：新增 `not selected.closed or selected.barriers` 检查，能阻止把已失效 slot 中仍保留的旧 ValueRef 直接当作当前读取值。建议完整护栏也检查 `selected.value.barriers`，并让 absent→undefined 的分支满足相同的无障碍前提。实际 Get 模型排除 getter effects，不负责恢复旧来源或存在性；失败分支应返回当前来源未知且保留可达域的值。这里不要求字段 presence 必须为 present，因为已有模型允许 when-present 的有限关系，但不得借此制造字段存在证明。
