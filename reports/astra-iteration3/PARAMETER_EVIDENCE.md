# CPB 参数与来源分析证据合同

本稿只观察保存原文前的源码与原始 Tree-sitter AST，供 v0.6 的独立实现和复核使用。没有导入、执行、编译、构建或测试 CodePatchBay；也没有运行工具测试套件。这里的 AST 观察不是 `value_analysis` 的自动输出，更不是业务行为结论。

机器稿：[parameter-observations.json](parameter-observations.json)。新增 ID 使用 `iter3.cpb.parameter.*`，没有改写冻结的 26 项 `capability-baseline.json`。本组包含 **11 项观察、31 个 AST 锚点、8 个源码文件；自动值流分析结果为 0**。7 项为局部源码事实，4 项为需要额外分析的连接边界。全部文件的本次 AST 均无语法解析错误；这只说明解析成功。

## 观察方法与来源身份

仅通过安全读取器 `_secure_bytes` 捕获下表明确声明的文件。解析器为 `tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14`。锚点按 AST 节点类型、字段键、绑定名称、callee 结构及所属词法符号选取；每个选择器要求唯一匹配，未使用预填 quote 筛选。源码原文随后从实际 AST 的 byte 范围提取。

每个锚点保存原文件 SHA-256、节点类型、原始 byte 起止、原始行列、节点文本及其 UTF-8 文本哈希。byte 结束位置不包含在范围内；行从 1 开始，UTF-8 byte 列从 0 开始。8 个文件均无 UTF-8 BOM。匿名回调中的锚点记录最近的具名词法符号，但这不证明回调属于函数的直接执行路径；例如 `enqueue` 中队列回调还依赖 `withQueueMutation` 的执行合同。

| 文件 | 原始字节 SHA-256 | 字节数 |
|---|---|---:|
| `cli/commands/pipeline.ts` | `3df3f333ec4668352efde20049494c4a85bdf13049c808cd9f89f2d82f30b4ed` | 6985 |
| `runtime/worker/managed-worker.ts` | `75cdd41a20c71a7f0c7c500080ab7743417f932d35e4179a031b822831c633ca` | 93984 |
| `server/orchestrator/failure-router.ts` | `8abe3a09afcf48aa46b9380f9955e6c9e3e0411c1b02a29a9d2b4f1d721ea1a9` | 14963 |
| `server/services/hub/hub-queue.ts` | `0bd13766a2a2fcd271c2ead8166fbbd6f782fde32f63954ccced88a4cb2de02c` | 92403 |
| `server/orchestrator/hub-orchestrator.ts` | `41e248486eeae6f36b8f66b87df56a466bb1d4c5cb86d4c09066012e170f8454` | 27683 |
| `bridges/engine-bridge.ts` | `b0647dd081f10fc07fb84117c925763859bfbf74b5544413104d2d15cce31076` | 643 |
| `server/services/engine-runner.ts` | `952b6a43e9d2e5a2040eae1c7c8ec5c000d26a12f1c44d395041434db48bd864` | 8674 |
| `server/services/agent/agent-config.ts` | `83a2eef775f1ff274054ee16fa749e195ae5a475f42abf520b2434e7ed6af484` | 28903 |

## 实际参数链

| 新观察 ID 后缀 | 局部原始 AST 位置 | 关系与能支持的结论 | 不能省略的反证或前提 |
|---|---|---|---|
| `flag-to-returned-binding` | `pipeline.ts:42`、`:70`、`:111`，`parseCommonFlags` | `DERIVES_BINDING`：局部 `retries` 初始为 3，`--retries` 分支写 `parseInt(args[++i], 10) || 3`，返回对象使用该绑定。 | 未给定或执行 argv；0/NaN 走 truthiness 回退，负数未被此表达式排除。这不是读取运行值的证明。 |
| `enqueue-metadata-field` | `pipeline.ts:158`、`:205`，`run` | `CONSTRUCTS_FIELD`：`enqueue` 第二参数的 `metadata.maxRetries` 构造为 `parsed.retries`；字段 pair 的 byte 范围是 `[6205,6231)`。 | `parsed` 的初始化来自函数调用；函数返回摘要和动态导入的 enqueue 身份仍须建立。请求本身也可能是 3。 |
| `queue-metadata-reconstruction` | `hub-queue.ts:1561–1569`、`:1580–1581`、`:1612`；`agent-config.ts:472`、`:487`、`:489–493` | `BOUNDARY_UNKNOWN`：先展开 `input`，再把整个 `normalizedInput.metadata` 赋为 await 返回，随后新 entry 的 metadata 读取这个字段。 | 反证非常具体：所选 `resolveAgentsForEntry` 一支直接返回 `metadata`，另一支返回 `{...metadata, agents:…, agent:…}`，没有显式 `maxRetries` 写入。普通自有可枚举字段存在保留依据；不能只因“重建”就报告丢失。自动连接仍需返回、别名、修改及 callee 摘要。 |
| `queue-existing-entry-reuse` | `hub-queue.ts:1597–1598`、`:1612`，`enqueue` 的队列回调 | `CONDITIONAL_RETURN`：同 key 的 pending entry 存在时，先返回 `existing`，不构造本次新 entry。 | 对应输入 metadata 是否进入返回值取决于该分支；新建分支有显式 metadata 构造。不能把两支合成无条件同一来源。 |
| `assignment-metadata-construction` | `hub-orchestrator.ts:373`，`HubOrchestrator.tick` | `CONSTRUCTS_FIELD`：assignment 构造调用提供 `metadata: candidate.metadata || {}`。 | 实例方法调用和持久化返回需要独立解析；这里只证明调用实参中的字段表达式。 |
| `inbox-to-worker-payload-boundary` | `hub-orchestrator.ts:427`；`managed-worker.ts:1394`、`:1397`、`:1428` | `MESSAGE_BOUNDARY`：写 inbox 时提供 assignment metadata；worker 从 claim.assignment 获得 assignment，再读 `assignment.metadata || {}`。 | 名称相同、`as AssignmentPayload` 或同名 schema 都不证明队列、存储、broker、序列化及 ownership/generation 对应。必须明确连接合同；本稿保持 unknown。 |
| `worker-literal-job-options` | `managed-worker.ts:1797` 调用、`:1809` 字段，`main.processInbox` | `CONSTRUCTS_FIELD`：传入 `runJobWithServices` 的第 0 参数是对象字面量，其中 `maxRetries` 为数值字面量 3，pair byte 范围 `[72609,72622)`。 | 非 finalizer-only 分支才有此调用；该对象没有从 metadata 展开的旧字段，因此不是已经证明的“同对象覆盖”。即使请求值也是 3，构造仍是字面量 3。 |
| `bridge-options-forward` | `engine-bridge.ts:19`，`runJobWithServices` | `FORWARDS_PARAMETER`：完整 `opts` 参数作为唯一实参传给导入别名 `runJobWithServerServices`。 | 单跳参数表达式转交不证明下游消费或某次实际调用。导入绑定依据与关系证据应并列保存。 |
| `service-rest-and-spread-order` | `engine-runner.ts:131–138`、`:157–180`；`buildServices` 的 ports 初始化和 `:121` 返回 | `BOUNDARY_UNKNOWN`：`opts` 的 object rest 成为 `jobOptions`，核心 runJob 实参先展开 jobOptions，后展开 services。 | `buildServices` 的 ports 字面量没有显式 maxRetries，且返回 ports，是重要反证。但要排除后续覆盖仍需闭合返回形状、别名和修改摘要。单看 spread 次序不能宣布丢失或贯通。 |
| `router-budget-local-origin` | `failure-router.ts` 的 `MAX_RETRIES` 初始化、`:111–112`、`:265`，`FailureRouter.route` | `DERIVES_BINDING`：局部预算来自 `MAX_RETRIES[failureKind] ?? 0`；另一个操作数来自 `assignmentRecord.attempts`；比较为 `attemptCount > maxRetries`。 | 这是局部预算的来源；部分分支先返回，不能声称每个失败均到达比较，也不能推导 whole-program 从不使用 metadata。 |
| `opaque-supervisor-counterevidence` | `failure-router.ts:277`，`FailureRouter.route` | `BOUNDARY_UNKNOWN`：满足 supervisor eligibility 时，整个 assignment 传入 `diagnoseFailure({ assignment, attempt, result })`。 | 该实例消费者及其返回尚未闭合；它是“所有 metadata 都没消费者”之类全程序负结论的实际反证边界。 |

这条链足以支持两类独立结论：CLI 源码字段构造，以及 worker 源码字段构造。只有显式来源合同要求 worker 使用请求字段、且有关传递和适用条件已说明时，才可将表达式差异报告为合同候选。`parsed.retries` 与字面量 `3` 的语法不同，不等于任意一次运行值不同。队列失败预算与引擎内部重试预算也需要分别标识，不能因为都叫 maxRetries 就合并。

## 有界 Evidence.details 合同建议

现有 `Evidence` 的 `kind`、`locations`、`node_ids`、`edge_ids` 和 `details` 足够，无需升级 `GraphSnapshot`。这些关系保存为独立证据，不生成伪 `CALLS` 边。当前 v0.6 的 `kind="static_value_analysis"` 可继续承载；下一步增加关系记录时可在 `details.relations` 内使用以下固定结构，而不改变已有字段：

```json
{
  "relation_schema": "callscope.value-relations.v1",
  "analyzer_version": "<actual implementation version>",
  "policy_hash": "<explicit policy identity>",
  "snapshot_id": "<captured snapshot>",
  "relation_count": 1,
  "relations": [{
    "type": "CONSTRUCTS_FIELD",
    "certainty": "exact_expression_relation",
    "scope": {"file": "cli/commands/pipeline.ts", "source_hash": "<raw SHA>", "symbol": "run"},
    "from": {"kind": "expression", "root": "parsed", "field_path": ["retries"]},
    "to": {"kind": "call_argument_field", "callee_syntax": "enqueue", "argument_index": 1, "field_path": ["metadata", "maxRetries"]},
    "ast_refs": [{"file": "cli/commands/pipeline.ts", "source_hash": "<raw SHA>", "node_type": "pair", "byte_start": 6205, "byte_end": 6231, "byte_coordinate_space": "original_source_bytes", "node_text_sha256": "<actual node hash>"}],
    "conditions": [],
    "barriers": [],
    "runtime_value_proof": false,
    "transport_proof": false
  }],
  "relations_truncated": false
}
```

支持的关系应各有独立义务：`CONSTRUCTS_FIELD`、`DERIVES_BINDING`、`READS_FIELD`、`PASSES_ARGUMENT`、`FORWARDS_PARAMETER`、`CONDITIONAL_RETURN`、`MESSAGE_BOUNDARY`、`BOUNDARY_UNKNOWN`。只有证明同一对象身份及先后写入时才允许 `OVERWRITES_FIELD`；当前 worker 两字段不能用这个标签。

建议每条关系最多 8 个 AST refs、8 个 barrier 样本、32 段静态 field path；文字和表达式设独立上限；每个证据只留有限关系样本并保留总数、截断标记和完整证据引用。unknown 至少包含 barrier 类型与实际位置，区分动态 callee、object spread、alias/mutation、transport、条件 join、解析失败及不支持语法。不将全项目 gaps 复制到每条关系。

`callee_syntax` 只是实际 AST callee 的选择依据；是否绑定内部目标另存 `graph_edge_ids` 和实际 resolution。对象字段的“封闭”是字段层级属性：晚于未知 spread 的显式键可能已确定，但整个对象仍不封闭。成员访问的表达式来源与对象运行值应分开。`||` 与 `??` 必须保留不同默认语义；`as`、`satisfies` 等擦除包装不得当成运行验证。

## 保存、版本与计数边界

运行期分析仅消费 `snapshot.files` 的捕获内容与身份；不得重新读当前 target 文件。协议等 `input_evidence` 仍仅提供原文证据，不能假装 parsed code、caller 或值流节点。AST 坐标必须注明捕获文本和原字节的关系，BOM 情况不能让位置悄悄错位。坏哈希、重复或冲突来源、parse error 必须输出明确 unknown/invalid，不能被空对象或空列表掩盖。

value analyzer/policy 的实际版本进入 component identity；配置合同与 source hash 同时进入新快照身份。新增关系只在一次新的不可变发布中保存。历史 v3/v4/v5 没有值流事实，应保持原样并可读取；对历史捕获源码进行新版本的只读评估时，结果同时标明旧 snapshot ID、新 evaluator/implementation identity，不能覆写历史发现。

报告必须分开计数：冻结基准仍是 26 项；本组仍是新增 11 项源码观察。每条显式 value contract 需要区分已闭合表达式匹配、不匹配、未知，以及外部适用条件/transport 是否未闭合。多个 AST 锚点、多个 relations 或 quote 命中都不直接增加“功能检出数”。本次观察没有自动 value analysis 结果，不能宣布 11 项自动通过或代码层功能完整。

## v0.6 实现保存链的只读复核

在本稿提交时已静态查看 `value_analysis._side/_finding/analyze_value_contracts`、`static_contracts._Sources/_Document`、`analysis.analyze_project`、`detectors.detect`、`service.scan` 和 `Store.publish/get_findings`，没有发现已确认的保存或历史身份阻断。`_Sources` 从快照的唯一 parsed 来源及保存内容哈希载入 AST，不读取当前项目文件；实际字段 AST、词法来源、条件、callee 是否绑定、合同出处及运输未知分别保存在证据中。实际版本同时进入 component identity，配置合同进入 policy hash。发布时快照和发现同事务保存；同 ID 的不同事实拒绝覆盖；历史查询直接读取原 JSON，不自动重新裁决旧发现。新增能力不改变历史空 `input_evidence`。

边界仍需如实显示：当前来源加载器要求捕获文本 UTF-8 哈希等于保存 hash；若原字节带 BOM 而捕获文本已移除 BOM，会给 `source_hash_mismatch`，不会伪装成已分析。上述 8 个观察文件均无 BOM，因此不影响本组来源。本次只完成源码观察及保存链审查，没有运行完整扫描或自动值流评估，也没有用工具测试套件验证行为。

`collect_source_review.py` 的 `rule_observation_counts` 只遍历 `snapshot.config["rules"]`，表示图规则分母。静态合同、值来源合同和本组源码观察必须分别计数。`analyze_value_contracts` 返回不匹配或未知发现，表达式匹配时可以不产生 Finding；因此没有 Finding 不等于拿到了每个合同完整通过的审计记录，更不等于目标功能或运行正确。
