# Astra 独立审查：0.10.1 字段精度修复

日期：2026-10-12。审查对象为 iteration8 最终冻结源码与两库正式保存结果。

**本轮修复了已定位的 v9 局部字段精度退化。** 正式 engine 评估现在支持 `maxRetries` 在存在时的来源形式保留，`buildServices` 的完整外层 own-key 集合与该键缺失也已恢复。其余四条字段评估路径仍为 unknown；原五项完整判断仍为 **0/5**，30 项必要义务未削减或升格。可以交付这一有明确边界的精度修复，不能称为完整参数运输或预算消费判断已经完成。

本次独立源码／保存产物审查未发现遗留阻塞项。该结论只覆盖所审查的实现与证据，不是一般 JavaScript 语义完备性、运行行为或测试通过认证。

## 最终身份与对照条件

[CORE_FREEZE.json](CORE_FREEZE.json) 的 package 为 `0.10.1`，analyzer 为 `static-multilang-10`，detector 为 `call-rules-9-field-precision`，schema 为 `2`。独立读取实际 package 源文件集合，42 个文件全部匹配冻结 hash；按工具的公开算法直接处理这些字节，重新得到整体身份：

`7957dad01f30a20b36823058eb245d120074c9f6f11802bd41a55641d8d26e7e`

`field_summaries.py` 为 `10f33804c3b77913aef29e12a0a00c24ea43ab61f7c09276ed053becb7d69443`，`semantic_ir.py` 为 `b430f7ce224f7321fc6541bc11c378ac57f6572ad9d9333b955871a3823a4539`。源码、正式扫描和导出的字段证据使用同一工具身份。

| 仓库 | 最终快照 | 选入／解析／未解析文件 | 图节点／边 |
| --- | --- | --- | --- |
| CodePatchBay | `3a987ec8a0ced043379a0e75a6f5932c24982e807e1d252d9b0fc0033183f977` | 333／330／3 | 11,085／60,571 |
| WinWinCode | `9c791af9bf562d6f0f36e09ddeb1f21b4a3445b649064d21ec4d34d33c6abece` | 471／465／6 | 32,407／171,983 |

两库的 [integration](codepatchbay-integration.json)／[integration](winwincode-integration.json) 都记录了冷、暖扫描；暖扫描全部配置语言复用缓存、全项目检测重算，保持同一快照且 `created=false`。两库仍为 partial；未解析来源没有被当作项目缺陷或完整覆盖。WWC 的零文件 Python bundle 不构成该语言的生产源码覆盖。

两库目标 source hash 与 v9 相同，策略文件与冻结 v9 **逐字节相同**，policy hash 也相同。因此这是相同保存目标与相同声明模型下的实现精度修复，没有靠增加 copy／Get 用户前提换取正项。v8 与 v9 的策略此前有差异，不能把三版都称作同策略实验。对应对照见 [FIELD_VERSION_COMPARISON.json](FIELD_VERSION_COMPARISON.json)。

## 正式字段结论与来源链

[field-assessments.json](field-assessments.json) 与最终 summary 中的全部字段 finding 完全一致，保留原三合同、五条评估路径，finding 状态仍为 uncertain。

| 实际路径 | 最终字段结果 | 保留的限制 |
| --- | --- | --- |
| `engine-runner.ts:157` 的 `runJob` 实参 | `source_form_preserved_when_present`；selected shape/source form complete | presence unknown，whole argument shape 未封闭；分析止于 callee activation 之前 |
| `hub-queue.ts:1580` 的两个来源路径 | 两条 unknown | 共享 metadata、普通写入、callee/completion 等缺口仍在 |
| `agent-config.ts:487` 的直接返回 | unknown | 外部对象及前缀 effects 未闭合；body return 不等于 fulfilled 值 |
| `agent-config.ts:489` 的构造返回 | unknown | spread／共享引用和 async 同化边界仍在 |

engine 正项可追溯到真实 `opts` 声明，parameter index 为 0，字段路径为 `[maxRetries]`。`:137` 的 rest-copy observation 与 `:158` 的 ordered-spread observation 保留同一 selected value ID，来源 BindingKey 与 subject parameter 一致。它记录复制时的源版本，后续对原 `opts` 或共享 child 的损坏不会被错误地当作已复制顶层 slot 的重新赋值；反过来，浅复制也没有认证 child 内容不变。

`:155` 的实际 helper 摘要给出一条同步正常返回、无遗漏返回／fallthrough、outer whole shape closed、selected `maxRetries` absent。真实 `ports` 的 11 个固定 own data keys 不含该键，`:176 ...services` 因此不会覆盖已复制的 `maxRetries`。这个缺键证明依赖实际新 allocation、完整 initializer／capture／escape 顺序与正常返回关系；不是按函数名或手填键集合生成。

helper 同时保留 `normal_prefix_effects_unknown=true`、`invocation_or_completion_proven=false`。外层结论仍要求 normal prefix 与已有独立 copy／actual Get 模型：普通 `services.maxRetries` 还可能涉及 prototype／accessor，不能用 own-key absent 推导一般 Get 必定为 undefined；也不能从这条实参源式推导字段存在、数值、实际调用、Promise 履约、消息运输或预算归属。保存的 reaching value、runtime value、transport、full functionality 均未升级。

## 实现修复的有效边界

源码审查确认，修复通过公共 IR 的来源、allocation、binding、effect 和 join 关系表达：

- 外部可达域在所有 join alternatives 都有依据时保留，primitive 的零对象引用与其内容／completion 分开；callee 本身仍加入 effect roots。
- 未暴露字面量的 construction guard 只排除 wildcard fallback 对匿名父对象的虚构反向可达；真实 alias／visible root、reflection、budget 和 incomplete 仍损坏相应对象。unknown spread 仍可直接破坏目标形状；finish 不恢复旧 slot，join、escape、reuse 和 bind 均遵守 lifetime 边界。
- capture 收集先排除目标函数内部声明与 import，再解析真正 free cells；跳过 TS 注解但继续遍历真实嵌套函数。未建模的隐式捕获保持 unknown，未来初始化的 captured cell 没有按当前 primitive 值剪枝。
- const guard 只保留已初始化不可重绑 cell 的身份，referent 对象和 captured cells 仍参与 mutation／escape。模块 owner 通过真实声明证据的 `BindingDomain` 注册，不能仅凭 `module:` 前缀获得权限；可变 cell 的替换仍 unknown，并保留受影响根、live cells 与未来 rebind。

开发因果追审见 [PRECISION_SOURCE_REVIEW.md](../astra-iteration7/PRECISION_SOURCE_REVIEW.md)。这些来源约束改善了有用精度，同时保留公共协议；它们不构成对所有 alias／effect／completion 情形的完备证明。

## 证据 ID 修补与独立机器核验

iteration7 的首次 0.10.0 候选随后被替代：模块 cell replacement 曾修改 EvidenceRef 的 guards/kind，却复用旧 ID。独立检查当时实际导出的记录没有发现内容碰撞，因此没有据此宣称 engine 正项已被证伪；问题是内部公共记录构造违反内容身份约定。0.10.1 已改为通过 `evidence(...)` 重建记录，并重新冻结、扫描和发表。旧 42 份源码已归档并匹配旧冻结记录，历史产物不冒充当前结果。

[INDEPENDENT_REVIEW_EVIDENCE.json](INDEPENDENT_REVIEW_EVIDENCE.json) 保存最终只读核验：18 个实际源文件的 1,167 个去重位置／EvidenceRef 均匹配原文件字节，其中 842 个带 span hash；1,055 个去重 typed EvidenceRef 全属对应正式快照，按完整构造公式重算 ID 全部一致、guards 规范化、ID 对应多内容的碰撞数为 0。字段导出、正式工具身份、策略字节、复制来源链与输入稳定性也全部匹配。这些数量描述核验范围，不是能力覆盖率。

## 旧关系与原目标合同

独立比较原始 navigation／atomicity 完整 finding，保持列表顺序、所有非身份字段和身份引用双射；只有已验证的发布版本字段改变。navigation 的 `abstract-N` 按实际 `_Engine` 实例分域：主 producer/consumer 与每个 counterexample 各有独立计数器，域内引用仍必须一对一保持。该区分来自源码构造，未删除语义字段。最终 [INDEPENDENT_RELATION_REVIEW.json](INDEPENDENT_RELATION_REVIEW.json) 没有遗留语义差异。

atomic 的保护区／内外谓词、真实二次查重与三项必要缺口保持；没有新增交错推导。navigation 的 query 域、已有 query 反证、callback／port 局部装配及十项缺口保持，`end_to_end_complete=false`。原 26 项账本仍是 **10 reproduced、3 unknown、13 evidence_only**，没有状态或预期变化。

[goal-ledger.json](goal-ledger.json) 的五项 claim 与 30 项必要义务定义、条件、反证和 required 标记均与原模板一致。独立解析 618 条递归引用、105 个去重 artifact/JSON pointer，artifact hash、snapshot、finding、rule 与 contract hash 全部匹配；见 [INDEPENDENT_GOAL_REVIEW.json](INDEPENDENT_GOAL_REVIEW.json)。原验收合同 SHA256 仍为 `9b6f4fda6aa24f055e288690e76405779e36758f8ba986799f78f2f96aa8d118`。

最终仍为 **0/5 完整目标**；30 项义务是 **4 项在声明范围内支持、20 项 partial、6 项 unknown**。engine 的局部进展进入 CPB-01.P4 的证据与说明，P4 仍 partial；queue／agent、scheduler／assignment／JSON／inbox／broker 运输、有效消费者和预算关联未被改写成普通环境假设。账本仍是人工评审自动保存证据的映射，`automatic_obligation_solver_used=false`。

本代理只读取核心源码、目标原文和保存 JSON，并运行只处理这些数据的独立采集器；没有导入或执行目标或分析器，没有运行工具／目标测试、构建、安装、目标 CLI/index 或浏览器。正式冷暖扫描由主代理运行受信静态工具完成。本次应交付的是可追溯的局部精度修复；下一步仍应优先连接原目标中的参数运输、实际消费者、guard 与预算归属，而非增加事实数或优先优化性能。
