# CodePatchBay 条件门开发查询

这次普通静态查询读取冻结 v0.12 快照 `7524afef4f9234ebef40eec1d74dbb91a3f56dc76f0191728c42d3bdd3cfb167` 的保存源码，未回写旧快照。新规则不是旧策略的一部分，因此以下是开发证据，正式 v0.13 scan 完成后才能作为新版本的保存 finding。

模块 SHA256：`97b96c16508390115e189ee5c3ee42ad0c282fd118143b21da864bb62905fbd4`。查询前后字节一致。完整产物 `gates-source-query.json` SHA256 为 `a8066ea9d863626e1a22db711170f84ab23aed2e1c9dc0b78a21a2350b9f7307`。

| 独立规则 | 条件源码关系 | 必要缺口 | source facts | 可信 AST 操作数 |
| --- | --- | --- | ---: | ---: |
| `cpb-report-readiness-abrupt-guard` | 支持 | 空 | 38 | 1112 |
| `cpb-report-completion-gate-conditions` | 支持 | 空 | 78（70 个不同内容身份） | 720 |
| `cpb-report-access-audit-response` | 支持 | 空 | 61 | 2544 |

## readiness 的提交前保护

`/results/0/pattern/groups/readiness` 保存实际谓词 `r.ok === false`、实参的词法声明、初始化调用和提前 return。true 分支阻断同一正常语句块内的后续调用，包含 `deps.enqueue` 的原行 576；不是只发现 readiness 与 enqueue 两个名字。

有限普通记录单元中，`ok=false` 对应谓词 true，其它严格不等于 false 的字段值对应 false。null/缺值访问不属于普通结果记录模型，仍为 unknown，未假定会返回 false。没有证明 readiness 实现检查的外部工具、端口或项目配置实际上可用。

## completion 条件与豁免

`/results/1/pattern/groups/completion` 从 mutating 谓词的实际源码生成九个普通记录等价单元和缺值/null 两个单元。`planMode=none/parent`、`workflow=docs/readonly` 返回 false；其它枚举单元返回 true，缺值/null 通过源码提前返回 false。enum 文本来自源码，不来自规则配置。

evaluator 的九个返回位置生成十九条条件路径，均通过真实调用边及形实参映射接到返回对象字段。四个当前 guard 直接依赖 `isMutatingJob` 的结果；checklist 和 adversarial 当前条件单列，完整路径仍保留前序门已允许正常继续的条件。由此不会把 readonly/docs/parent 的 verify 豁免扩大成 checklist 或 adversarial 的全面豁免。

checklist 先被判定；其 evaluator 的返回字段 `outcome` 被本地消费者读取，非 complete 时将其结果或源码默认失败值构造成返回记录。这里没有解释 checklist 内部全部证据判定，没有验证外部 verdict 真假或任何目标检查执行结果。

## access-audit 与响应字段

`/results/2/pattern/groups/access_audit` 认证 audit opener 的结果身份，并关联原行 415 的实际 await append、catch 和同一个 response。catch 直接赋值含 `statusCode=503`、`payload.code=HUB_ACCESS_AUDIT_UNAVAILABLE` 的普通记录；原行 444 的实际 `sendJson` 使用这个 response 的字段。

`response_value_relations` 进一步把 `response.statusCode` 接到 `sendJson` 第二个参数，再接到 `reply.writeHead` 第一个实参。这是具体值/字段的条件来源关系，超出了相邻调用顺序。

注册的请求 callback 是否被调用、catch 中日志和后续 header 操作能否正常完成、审计持久化、实际网络响应、先前业务修改的回滚均不由本摘要证明。对象是 Hub access audit，不与 job 尾部被 catch 的 best-effort audit 合并成同一合同。

规则见 `gates-rules.json`，模型和接口见 `gates-design.md`。未执行、导入、构建、安装目标，未运行测试或夹具。
