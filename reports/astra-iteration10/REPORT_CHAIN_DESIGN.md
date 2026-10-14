# 原分析报告主链的自动源码关系

日期：2026-10-13。实现模块：`callscope/report_chain_analysis.py`。本模块补两份原 Astra 报告中五项具体异常以外的主链、守卫和反证；不读取报告文字作为检测依据，也不要求再次由 Astra 审核或批准输出。

## 输入和输出

`validate_report_claim(rule)` 校验数据；`analyze_report_claims(snapshot, rules)` 返回独立 `static_report_claim` Finding，证据类型为 `static_report_chain_analysis`。report claims 不加入原五目标／30义务分母，也不以事实数量或报告段落数计算功能覆盖率。

规则固定键为 `id`、`type`、`severity`、`sources`、`models`、`provenance`、`applicability`。每个 source 只有 `{role,file,symbol}`，唯一选择保存源码中的真实声明。配置不能提供调用步骤、guard、属性结果、先后关系或正确结论；`provenance.source_doc` 只作来源标签，不打开文件。实际角色调用、参数、结果 binder、分支和构造均由已认证 AST／CALLS 生成。

声明和调用的文件、snapshot、source hash、字节区间、span hash、parser／投影身份保存。内部 callee 必须通过 `SemanticSources.call_binding`；外部、动态、部分或未绑定调用只保存原 call-site 及原因，不能靠名称替换成确定边。参数实参／形参映射绑定真实被调用声明及参数位置；spread 映射未知单独记录。

完整解析、唯一 AST 定义和原图 exact span 一致，但 macro/条件/namespace binding 不闭合的角色，可保留 source-only body。角色 graph binding limits 另记，overall claim 保持 partial；不因原调用图绑定不足而删掉真实部署反证，也不修复 resolved CALLS。

## 有限模式

| 模式 | 自动生成的关系 | 结论边界 |
| --- | --- | --- |
| `guarded_call_sequence` | 同一主体的直接 statement steps、真实调用／实参、call-result binder 与 guard 的来源联系、简单 abrupt 分支和正常到达排除、赋值尝试及相邻 statement 次序；async/gen body 的 source-only 子区域另列 | 源码顺序以两 statement 正常到达为条件；deferred body 另有激活前提但不证明激活；不把并列实参或嵌套调用排成执行顺序，不证明所有路径、异步完成、持久化或注入端口成功 |
| `best_effort_finalization` | 真实 try/catch 范围、空 catch/no finally、正常与外层 catch 里的同一个认证 callee | 只证明所选异常处理结构；不同审计对象不能合并，捕获失败不证明收尾成功 |
| `structured_command_source` | execFile 的真实 import 或 const promisify 来源、loader 实际参数及模板／导入常量、resolver 查询源式、真实角色调用和实参／形参、executor 的同形参字段和完整字面 shell:false | 注册 Node 源合同而不调用 Node/Git/probe；未证明中间 heap 值稳定、策略内容真实性或全函数 expectedEvidence 非干扰 |
| `unsupported_method_evidence` | 实际 const 字符串集合、同 binder 的 if 集合调用、结构记录 marker 字段／payload／guard／emission，以及 plan 同 marker 的条件赋值 | marker 值来自显式定义源式，未知 spread 或 heap 不变性不补；不以任意 bool 支持该模式，不证明所有输入都留痕、记录已持久化或外部 hardGate observation 已获得 |
| `state_guard_sequence` | 两函数最初调用的相同认证内部 callee、显式选择表达式、正常 continuation／Result `?`、closure/macro 的实际源谓词 | 可报告重复 validate 和活动状态源式；macro 不展开、iterator 不执行，不证明每种持久状态或运行尝试 |
| `deployment_provider_split` | 单独 boundary 结果、生产 bootstrap 构造源式、installation 赋值、provider 的真实调用和参数 | worker 与 server 来源分开，unsupported 不自动推导能力缺失；组合候选不提升 generic 全局 dispatch，不证明 secret 或 provider 配置可用 |
| `conditional_delivery_result` | 固定委托 `report_delivery_analysis.analyze_pattern(analysis)`，由自动源证据生成交付结果、持久终态与调和段 | helper 自己保留具体缺口；不把 core completed 当 published，不推导所有故障恢复 |
| `agent_execution_policy` | 固定委托 `report_agent_policy_analysis.analyze_pattern(analysis)`，生成 agent allowlist、pool 调用和环境／sandbox 条件策略 | 源码策略不等于运行隔离保证，native/off/custom 和 required/strict 反证分别保存 |

前六类在主模块实现，后两类由固定白名单 helper 模块实现。helper 共享已认证的 roles、calls、source expression、fact/gap、有限 nodes 和 sequence 接口；不存在从策略导入任意 Python、动态插件或目标模块的接口。

## 证据域

`source_facts` 是自动提取的 source-derived 记录；`trusted_models` 单独声明正常 statement 控制、Node structured execFile 和生产构造源模型；`policy_declarations` 保存来源和适用条件；`analysis_gaps` 保存 unresolved。每个域不能替另一个域补结论。

`scoped_source_relations_supported` 表示所选有限源关系足够，不表示原报告全部重现。Finding 始终 uncertain；`runtime_verified`、`full_functionality_proven`、`whole_report_reproduced` 和 `original_five_goal_acceptance_computed` 均 false。解析、调用身份、控制范围、marker consumer、field stability 或预算缺口都可使具体模式 partial/unknown。

Rust 只为可见的简单 parameter/let pattern 保存 captured binder identity，拒绝未解码 pattern 和多候选；不是编译器命名空间或宏展开结果。成员、状态和 Result guard 原式保留，不从相同拼写直接证明同一运行对象。

## 当前来源选择

[report-claims-rule.json](report-claims-rule.json) 当前按仓库保存18条规则：CPB六条，WWC十二条。初始七条对应 CPB runJob/stages、job audit、trusted probe command、unsupported probe evidence；WWC WorkRun、adapter intent/persist/exact reconcile、Device worker/provider 部署。另接入交付结果和 agent execution 策略，以及九条 WWC remote/managed bootstrap、typed dispatch、生产 adapter open、三个独立 Kernel API 和 Chat 请求链。选择器只定位来源，rows 顺序不决定执行链次序。

交付结果 helper 的13个来源包括真实 `main.processInbox`、finalizer 结果、终态 write/readback、attempt/finalizer/git/journal/recovery 调和；agent helper 的18个来源包括 allowlist/pool、readonly/failure、child-env predicates、sandbox policy/launch 和 ACP 实际 env 投影。它们是分析实现，不是新批准步骤。其余原报告范围仍需分别实现和记录 gaps：全面职责所有权、所有 CLI/HTTP 入口、所有路由/事件协议、外部发布、全写者和全部恢复交错等。覆盖账本必须将“可定位来源”“自动有限链支持”“未审范围”分开。

开发观察来自旧正式 snapshot 的正常源码查询，只用于实现核对；新正式证据由冻结后的普通扫描／报告生成入口产生。完整 snapshot 查询统一获取 `.analysis-tools/goal-source-query.lock`，避免并行反序列化导致内存耗尽。目标代码、probe、测试、构建、发布和应用均不执行。

## 正常保存源码查询核对

完整18条规则已经通过普通分析入口读取两库 v0.11 保存 snapshot；目标目录未执行或导入，三份分析模块的查询前后字节一致。CPB六条均支持所选源码关系，WWC九条支持、三条保留 partial；全部18条都有足够 captured source structure，未超过分析预算。三条 partial 是原 main 声明的 macro/namespace binding 限制，真实 provider/worker 构造源码仍保存，不报实现缺失。

实际自动证据包括 runJob 五个正常到达早退排除及六个结果 binder→guard 联系、audit 同 target 两个空 catch、HEAD 模板和导入策略常量、execFile 同形参字段及 shell:false、unsupported method 实际字符串集合→条件→marker消费、WorkRun 重复 first callee 与活动选择源式、delivery 四段结果关系和 agent/env/sandbox/ACP 六类策略关系。Kernel 的三个 API 分别保存一个 deferred body 内的顺序区域，future 激活／履约仍未证明；Chat 选择实际内部构造与公开 create，而不是仅提取外层工厂。

开发输出位于 `/tmp/codepatchbay-report-chain-observations.json` 和 `/tmp/winwincode-report-chain-observations.json`，明确 `published=false`；它们不是最终新版本证据。2541个 source-fact 记录含不同规则的重叠来源，既不是独立功能数，也不是覆盖率。正式冻结和扫描另行生成新分析身份、Finding 和报告。
