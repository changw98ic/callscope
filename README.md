# CallScope · 静态调用结构完整性分析

公开源代码分发：项目原创代码使用 [MIT License](LICENSE)，上游与分析样本来源见[开源声明](OPEN_SOURCE_NOTICES.md)。本仓库保存源码、文档与报告；当前完整大 JSON 证据分段压缩存放，克隆后运行 `python scripts/restore_report_artifacts.py` 还原原路径和原始字节。数据库和缓存留在原工作区，完整保存范围见[发布说明](publication/README.md)。以下为原项目说明；增加发布入口前的 README 原文另存于 `publication/workspace-original/README.md`。

CallScope 只读项目源码，构建版本化调用图，并按有限合同分析字段、状态、导航、消息与协议、预算和查重保护关系。当前正式版本为 v0.14.0，增加具体职责解释、文档与部署来源对照，以及条件状态沿革和发布边界。两库正常纯静态冷/暖重算及自动报告均已保存；完成依据是原报告实际内容与证据的对应，不能按版本号关闭目标。当前状态见[目标记录](reports/astra-iteration12/CURRENT_GOAL.json)，原内容的正式逐项对应见[内容对照](reports/astra-iteration12-scope2/ORIGINAL_REPORT_COMPLETION.md)。

默认分析 Python，可选 TypeScript/TSX、JavaScript 家族与 Rust 静态前端。字段适配器使用公共不可变 IR；确定图索引复用 Axon，可选 CocoIndex 引擎持久缓存语言前端。提供 CLI、本地网页、HTTP、MCP 和冻结源码观察核对命令。

**系统不执行目标代码，不导入目标模块，不运行测试，不触发构建，不提供沙箱或动态 trace。** 路径存在只能说明静态调用图存在相应连接，不能保证实际执行顺序、分支覆盖、参数、输出、业务正确性或一般意义上的功能完整性。

实现以原始 [CodePatchBay 分析报告](reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md)和 [WinWinCode 分析报告](reports/astra-baseline/WINWINCODE_ANALYSIS.md)为基准，不设置重复 Astra 审批步骤。五项判断及三十项必要关系是实现追踪，不替代全文报告的主链、架构边界、反证与未审范围。v0.11 历史账本为0/5；v0.12 与 v0.13 正式保存的五项判断均为complete/full_goal_supported=true，三十项必要关系均supported。这是所选条件判断的完成数，不是目标功能通过率。报告入口与扩展规范见 [自动项目分析报告](docs/AUTOMATED_REPORTS.md)。

`goal_contracts` 自 v0.12 起固定注册状态、参数管线、导航、Device 协议和有限并发窗口分析。每项判断必须由保存源码生成全部必要关系，核对快照、合同与模型身份，并保留适用条件、反证和缺口。`report_claims` 独立抽取主要功能链的实际调用、参数、guard、正常源码顺序、失败分支及生产装配候选；局部链关系支持不等于完整判断支持。原报告文字只用作对照，不进入检测器充当自动证据。

生成可下钻的项目报告：

```sh
python -m callscope report --db .callscope/demo.sqlite3 --snapshot SNAPSHOT_ID --format markdown --output project-report.md
python -m callscope report --db .callscope/demo.sqlite3 --snapshot SNAPSHOT_ID --format json --output project-report.json
```

报告读取已保存的图、源码与发现，不重新扫描目标。它分列架构结构、完整条件判断、主要功能链、局部证据、条件与未审范围；HTTP `GET /api/v1/report` 和 MCP `get_project_report` 提供同一报告。配置条数、源码事实数、五项判断完成数和解析比例均不代表全文报告或项目功能覆盖率；当前报告明确保留 `whole_report_reproduction_claimed=false`。

## v0.14.0 正式结果

直接阅读 [CodePatchBay 自动报告](reports/astra-iteration12-scope2/codepatchbay-automatic-report.md)和 [WinWinCode 自动报告](reports/astra-iteration12-scope2/winwincode-automatic-report.md)。正常 CLI、HTTP 和 MCP 共用报告生成器 v3，正文展示实际字段、实参交接、guard、条件表、反证和源码位置，完整 JSON 保留全部原始证据与精确引用。

| 保存范围 | CodePatchBay | WinWinCode |
| --- | --- | --- |
| 完整条件判断 / 必要关系 | 3 项 / 18 项，全部支持 | 2 项 / 12 项，全部支持 |
| 所选源码关系 | 16 项限定支持 | 20 项限定支持 |
| 实际来源操作 | 15,223 项 | 10,023 项 |
| 完整解析 / 选入文件 | 330 / 333 | 465 / 471 |

新增正文承接 Task 的读取、记录投影、sanitize 与 render，FIXED→superseded→新 lineage 的实际来源，以及模式、dry-run 与许可条件下的发布边界。WinWinCode 增加冻结候选、角色、lease/fencing 与 evidence-source 的有限合同盘点，并将 JSON/Serde 的实际协议接缝接回职责说明。Device 文档比较分别保留 Control Plane 内部限定、凭据材料与期限未知、Worker 模型流和本地消费来源，不据此判定协议绕过。

原职责表、主要链路、文档三方面和具体判断分别在[原报告内容对照](reports/astra-iteration12-scope2/ORIGINAL_REPORT_COMPLETION.md)中对应实际正文与来源；[静态边界](reports/astra-iteration12-scope2/REPORT_SCOPE_GAPS.md)保留 source-only 未知和原明确未审范围。五项/30 关系、36 条选中关系、操作数量与解析比例均不是全项目功能覆盖率。`whole_report_reproduction_claimed=false` 和运行验证 false 继续保留，不声称全仓库无缺陷或复写原报告全部建议。

两库冷、暖轮均全量重算，同库快照一致且第二轮不重复创建。目标源码 hash 与 v0.13 相同，原 26 项冻结观察保持 10 reproduced / 3 unknown / 13 evidence_only、两库 `changes=[]`；36 份原引用身份与仓库提交匹配，65 份核心源码与冻结存档一致。完整身份、账本和输入 hash 见[发布报告](reports/astra-iteration12-scope2/REPORT.md)。

## v0.13.0 历史正式结果

先读 [CodePatchBay 静态分析简报](reports/astra-iteration11/codepatchbay-analysis-brief.md)和 [WinWinCode 静态分析简报](reports/astra-iteration11/winwincode-analysis-brief.md)。更多关系、source-only 边界及证据导航见 [CPB 源码摘要](reports/astra-iteration11/codepatchbay-analysis-summary.md)和 [WWC 源码摘要](reports/astra-iteration11/winwincode-analysis-summary.md)。本轮新增八种关系类型、十三个来源查询，正式报告直接展示条件、状态表、字段连接、guard 和原始证据指针。

简报从正式保存值选择必要关系、条件和有限表，不重新评判；其输入和显示字段见 [简报输入清单](reports/astra-iteration11/BRIEF_INPUTS.json)。这是本轮额外的阅读视图，CLI/HTTP/MCP 的报告接口保持原协议。

| 保存范围 | CodePatchBay | WinWinCode |
| --- | --- | --- |
| 完整条件判断 / 必要关系 | 3项 / 18项，全部支持 | 2项 / 12项，全部支持 |
| 所选源码关系 | 13项限定支持 | 18项限定支持 |
| 完整解析 / 选入文件 | 330 / 333 | 465 / 471 |
| 捕获辅助原文 | 2项 | 11项 |

五项原问题分别是：pipeline 重试选项与受管理执行预算接线差异、`superseded` 终态分类不一致、同键提交的有限并发窗口、看板新建导航缺少 delivery 上下文、Device 更新命令遗漏条件必填的 `verificationCommand`。结论均保留各自的触发条件、反证和拒绝位置。

新增关系承接 readiness 提交前早退、completion 条件门、access-audit 响应、事件到索引及重建、可信命令来源、失败 record 保留、WorkRun 状态与依赖选择、消息/提交身份、outbox/ack 字段及浏览器生命周期。资源写者和消费者另有来源索引，所有权评估保持 `partial_captured_writers_and_consumers`。这些是实际源码关系，不是十三个新缺陷；31 条来源查询不构成功能覆盖率。

Rust 前端修正了 crate 内置编译限制属性的误分类。上一版三个 WWC 来源条目的错误 opaque 绑定已解除；任意宏、活动 cfg、泛型/trait 分派、provider 凭据及外部效果的原有边界仍分别保留。两图快照仍为 partial，不将解析范围状态与具体判断混为一谈。

两库 source hash 与 v0.12 相同；五项原问题仍在限定模型内成立。原 26 项观察保持 10 reproduced / 3 unknown / 13 evidence_only，两库 `changes=[]`；36 份原引用源码 saved/live hash 和两仓库 commit 均匹配。60 份核心源码与冻结存档一致，[发布身份](reports/astra-iteration11/PUBLICATION_IDENTITY.json)为 `verified=true`。这些核对不代表全文报告完成率。

冷、暖两轮均使用 full 引擎重算全部前端和检测，各仓库两轮事实一致、同快照且第二轮 `created=false`。本轮未复用前端缓存；与 v0.12 的 CocoIndex 维护方式不同，不作同引擎精度或性能比较。工具原有 CocoIndex 功能保留。

报告生成器 v2 新增 `source_relation_index` 和有界 `presentation_only` 展示；有限表与实际条件可下钻到完整 pattern、source facts、Finding/Evidence。源码关系支持仍与必要缺口、source-only 边界和原明确未审范围分列。原报告中的职责说明、Device 文档与部署口径比较尚未全部形成同等自动解释，`whole_report_reproduction_claimed=false`。

本轮 [正式报告](reports/astra-iteration11/REPORT.md)、[全文范围差距](reports/astra-iteration11/REPORT_SCOPE_GAPS.md)、[五判断/30关系账本](reports/astra-iteration11/goal-ledger.json)、[原观察比较](reports/astra-iteration11/ORIGINAL_BASELINE_COMPARISON.json)与[条目导航](reports/astra-iteration11/REPORT_ALIGNMENT_RESULTS.json)分别保存。

- CodePatchBay：[完整自动报告](reports/astra-iteration11/codepatchbay-automatic-report.md)、[完整 JSON 证据](reports/astra-iteration11/codepatchbay-automatic-report.json)、[正式扫描记录](reports/astra-iteration11/codepatchbay-integration.json)
- WinWinCode：[完整自动报告](reports/astra-iteration11/winwincode-automatic-report.md)、[完整 JSON 证据](reports/astra-iteration11/winwincode-automatic-report.json)、[正式扫描记录](reports/astra-iteration11/winwincode-integration.json)

## v0.12.0 历史正式结果

先读 [CodePatchBay 易读摘要](reports/astra-iteration10/codepatchbay-analysis-summary.md)和 [WinWinCode 易读摘要](reports/astra-iteration10/winwincode-analysis-summary.md)，再按 Finding/Evidence ID 与 JSON Pointer 下钻完整证据。

| 保存范围 | CodePatchBay | WinWinCode |
| --- | --- | --- |
| 完整条件判断 / 必要关系 | 3项 / 18项，全部支持 | 2项 / 12项，全部支持 |
| 所选主要源码链 | 6项源码关系支持 | 9项源码关系支持，3项partial |
| 完整解析 / 选入文件 | 330 / 333 | 465 / 471 |
| 捕获辅助原文 | 2项 | 11项 |

五项判断分别处理参数与预算接线、superseded终态分类、有限同键窗口、导航缺少上下文、Device条件字段遗漏；保存结论含实际适用条件及反证。两库图快照仍为partial，这是解析/图范围状态，不覆盖五项判断的模型内完成结论。冷/热轮保存同一快照，热轮不重复发布。

18条链均保存源码结构支持；其中WWC的provider部署、Worker入口与生产构造三项仍为partial_source_relations，图绑定/生产分派或凭据条件没有被候选源码补齐。已支持的trusted probe、unsupported marker与WorkRun链也保留外部效果、全输入保持、iterator/macro边界，不将supported写成无缺口。逐项state与gaps见摘要。

本轮新增模型、policy与辅助原文；与v0.11的比较包含分析范围变化，不是同policy的纯精度比较。完整报告明确whole_report_reproduction_claimed=false；五项/30关系与原26项冻结观察采用不同分母，均不能代表全文报告覆盖率。

原26项冻结观察正式保持10 reproduced/3 unknown/13 evidence_only，与v0.11 changes=[]；36份引用原文的保存/现场哈希全部matched，两库目标commit保持。54份核心源码与冻结存档一致，[保存身份核对](reports/astra-iteration10/PUBLICATION_IDENTITY.json)为verified=true。原观察对照见 [CPB](reports/astra-iteration10/codepatchbay-baseline-v12-and-v11.json)和 [WWC](reports/astra-iteration10/winwincode-baseline-v12-and-v11.json)，这些身份/观察计数不替代五判断或全文覆盖。

本轮发布说明见 [v0.12正式报告](reports/astra-iteration10/REPORT.md)。正式实现追踪见 [五判断/30义务账本](reports/astra-iteration10/goal-ledger.json)与 [保存判断证据及指针](reports/astra-iteration10/GOAL_JUDGMENT_EVIDENCE.json)；全文条目导航见 [REPORT_ALIGNMENT_RESULTS](reports/astra-iteration10/REPORT_ALIGNMENT_RESULTS.json)。条目/引用数量用于定位，不生成全文评分。 与原全文报告的具体距离及后续有限静态能力见 [范围差距](reports/astra-iteration10/REPORT_SCOPE_GAPS.md)。

- CodePatchBay：[完整自动报告](reports/astra-iteration10/codepatchbay-automatic-report.md)、[完整JSON证据](reports/astra-iteration10/codepatchbay-automatic-report.json)、[正式扫描记录](reports/astra-iteration10/codepatchbay-integration.json)
- WinWinCode：[完整自动报告](reports/astra-iteration10/winwincode-automatic-report.md)、[完整JSON证据](reports/astra-iteration10/winwincode-automatic-report.json)、[正式扫描记录](reports/astra-iteration10/winwincode-integration.json)

## 快速使用

需要 Python 3.11 或更新版本，以及支持 `dir_fd`、文件描述符目录扫描和禁止跟随符号链接接口的 Linux/POSIX 环境。首版未适配 Windows 原生环境。Python 全量模式在仓库根目录直接运行，无需安装额外 Python 包；Axon 的纯 Python 图核心已随工具保存：

```sh
python -m callscope scan examples/order_service --engine full --json
python -m callscope serve examples/order_service --engine full --port 8787 --watch
```

打开 `http://127.0.0.1:8787`。`serve` 启动时先尝试一次静态扫描，然后提供发现列表、调用图、源码证据、路径查询、版本比较、规则配置和人工处置。初始扫描失败时，界面仍可查看状态与修改配置。`--watch` 周期性全量捕获源码；全量模式每次重算前端，CocoIndex 模式可复用未变语言的前端缓存，检测始终全量重算。相同分析输入去重，不会执行应用。

`pyproject.toml` 同样声明了安装后的 `callscope` 命令及 `share/callscope/web` 网页资源。源码运行从仓库 `web/` 读取页面，安装后回退到 Python 环境的资源目录。打包使用 setuptools；本轮没有进行打包或安装验证。

TypeScript/Rust 前端使用固定版本的可选 Tree-sitter 工具依赖，可安装本工具的 extras：

```sh
python -m pip install '.[languages]'
```

也可以使用本次工作区已准备的 `.analysis-tools/python` 工具库目录。安装的是 CallScope 分析依赖，不安装目标项目依赖，不调用目标编译器。依赖声明为 `tree-sitter==0.25.2`、`tree-sitter-typescript==0.23.2`、`tree-sitter-rust==0.24.0`。全量模式缺少语法库时保留解析失败/部分分析；CocoIndex 模式的工具解析器初始化失败会使本轮更新失败并保留旧快照，不会缓存成成功空图。

## Axon 与 CocoIndex 接入

`scan`、`serve` 和 `mcp` 支持 `--engine auto|full|cocoindex`，默认 `auto`：

| 引擎 | 行为 |
|---|---|
| `auto` | 发现工具目录或当前 Python 安装中固定版本的 CocoIndex 依赖时选用它，否则使用 `full` |
| `full` | 不使用前端持久缓存，每次全量解析与检测 |
| `cocoindex` | 使用 CocoIndex `1.0.25` 的持久 memo，按语言整体复用或重算前端结果；依赖缺失时报告错误 |

可在 CallScope 的工具环境安装完整可选依赖：

```sh
python -m pip install '.[languages,maintenance]'
python -m callscope serve examples/order_service --engine cocoindex --port 8787 --watch
```

本工作区已准备隔离工具环境 `.analysis-tools/runtime`，可由宿主 CallScope 启动其固定 Python；实际安装依赖记录在 [requirements-maintenance.lock](requirements-maintenance.lock)。CocoIndex worker 使用 `python -I`，仅接收已捕获源码的 JSON 数据，执行固定注册的 CallScope 前端，不导入或执行目标代码。

缓存粒度是语言整体：同一语言内文件新增、删除、改名或内容变化后，重新解析并绑定该语言全部选入文件；完整配置、工具源码身份和 worker 实际解析组件版本也参与缓存键。其他语言可复用缓存，但全局规则、可达性及调用环检测每轮重新计算。`read_error` 所在语言不写入 memo；解析器运行失败或协议/证据身份不一致时本轮不发布新快照。`auto` 选中 CocoIndex 后的运行失败不会静默切换为另一引擎。维护计数位于 `publication.maintenance` 和服务状态，不进入不可变快照统计。

Axon 接入随所有引擎启用：`GraphIndex` 使用其节点、关系及有向邻接索引，供路径查询和检测器访问确定内部调用。调用绑定、未知传播及规则判断由 CallScope 负责。来源、固定版本与实际改动见 [上游代码复用说明](docs/UPSTREAM_REUSE.md) 和 [第三方声明](THIRD_PARTY_NOTICES.md)。

扫描将快照和发现保存到当前工作目录下的 `.callscope/callscope.sqlite3`。CLI 的 `--db PATH` 可以指定同一份数据库；不同工作目录下运行时要明确指定路径。

```sh
python -m callscope scan examples/order_service --db .callscope/demo.sqlite3 --json
python -m callscope path app.api.submit_order app.storage.write_order --db .callscope/demo.sqlite3
python -m callscope anomalies --db .callscope/demo.sqlite3 --json
```

`path` 默认使用数据库最新快照，返回一条确定调用关系组成的路径及分析完整性信息。它不是执行轨迹，也不枚举所有调用路径。

手动修改目标目录的源码后再次扫描，会形成新的分析快照。相同项目、源码、配置、分析器、检测器、模式、工具源码及后端/解析组件身份的重复扫描不会发布重复快照。`parser_version` 保存这些组件身份的规范组合，`stats.component_versions` 提供结构化信息；不同维护引擎或版本属于不同分析输入，缓存命中次数不改变快照身份。`scan --json` 返回 `{snapshot, findings, publication}`，快照 ID 位于 `snapshot.id`。使用两个分析快照 ID 比较：

```sh
python -m callscope diff OLD_SNAPSHOT_ID NEW_SNAPSHOT_ID --db .callscope/demo.sqlite3
python -m callscope path app.api.submit_order app.domain.validate_order --snapshot NEW_SNAPSHOT_ID --db .callscope/demo.sqlite3
```

以上快照 ID 为占位符，要替换成实际 ID。静态版本比较展示符号、调用关系和发现变化，不声称行为差分。不同项目之间的比较也不代表同一项目的历史演化。

## 检查范围

| 能力 | 结论边界 |
|---|---|
| `required_call` | 声明的必需直接调用是否存在 |
| `required_path` | 声明的必需静态调用路径是否存在 |
| `forbidden_call` | 是否存在声明禁止的直接调用 |
| `forbidden_path` | 是否存在声明禁止的静态调用路径 |
| 调用环识别 | 存在递归或相互调用结构；不判断是否无法终止 |
| 指定入口的连接分析 | 与声明入口未连接的函数标为疑似不可达，不认定死代码 |
| 未解析调用展示 | 显示动态、外部、歧义及其他未解析关系；不把未知当作缺失 |
| 快照、源码及规则证据 | 所有发现绑定分析版本，历史下钻读取当时保存的源码 |
| 人工处置 | 记录接受风险、误报标记或计划修复，保留原始发现 |
| `literal_set_consistency` | 比较指定声明的封闭字符串初始化集合；不证明运行时集合或终态语义 |
| `required_object_fields` | 检查指定函数直接返回的封闭字面对象是否构造指定键；条件合同始终保持 `uncertain` |
| `call_argument_value` | 比较 TS/JS 直接调用参数字段的有限表达式和词法来源形式；不计算运行值或跨进程传输 |
| `navigation_query_context` | 推导所选导航的有限query keys、具体callback注入、读键/null/拒绝链；真实路由/事件仍可能未知 |
| `protected_deduplication` | 提取所选callback保护范围、外内查重谓词和状态patch来源差；不推导并发交错 |
| `parameter_field_flow` | 按实际调用绑定和有限对象模型摘要所选形参字段到调用实参或正常return的来源形式；逐site保存正向或unknown，仍不证明运行值、消息运输或完整字段流 |
| `goal_contracts` | 固定适配器生成完整的所选静态条件判断；必要关系、模型适用性与预算均须闭合，不保证运行成功 |
| `report_claims` | 从定位的源码抽取主链、guard、正常语句顺序、命令来源、失败分支与生产装配关系；不将候选分派升级为确定调用 |
| `rust_finite_state_selection` | 从所选 Rust iterator/enum/`matches!` 计算有限状态与依赖筛选、活动集合及选中项来源；不穷举领域状态机 |
| `conditional_gate_relations` | 连接实际返回记录、条件分支、提前返回、门的适用条件和响应字段；外部检查结果仍为不透明输入 |
| `event_index_projection` / `trusted_command_lineage` / `unsupported_record_retention` | 追踪所选记录、codec、投影、命令参数和证据内容来源；保留覆盖、first-wins、异常与物理写入边界 |
| `message_identity_relations` | 连接实际声明、typed arm、请求/提交字段及有限 SQL 位置；字段域一致不等于线上值相同或 exactly-once |
| `browser_async_lifecycle` | 关联 generation/context/controller 与局部继续执行和写回 guard；不把父 guard 自动继承给回调 |
| `resource_writer_ownership` | 展示所选字段的实际写者、消费者和拒绝条件；保留 partial，不推断唯一事实所有者或全部授权 |
| 项目报告 | 汇总保存证据及明确的未审范围；重叠源码选择单列，不相加成覆盖率 |

v0.11 在字段评估中分开保存两类关系。`source_relations` 展示实际参数/形参连接、词法别名、当前返回引用、对象构造次序和显式字段写入尝试；它帮助定位链路走到哪里、在哪个操作后开始未知。`local_copy_retention` 另检查当前 spread 复制的所选自有字段，在字段存在、普通自有数据复制正常完成的条件下，能否保留到尚未暴露的字面对象构造终点。这个局部结论不恢复最初入口值，也不证明字段存在、共享子对象不变、Promise 履约或消息运输。

当前不提供类型检查、编译校验、参数运行值证明、一般控制流/支配证明、完整数据流/污点分析、一般字段传递或原子性证明、业务需求评审、测试接入或执行验证。有限局部顺序与guard摘要不替代这些能力。它也不能从没有声明的项目意图中推断“应该还实现什么”。静态功能完整性分析不等于业务正确性保证。

“未检出”“未完成”“不支持”和“无法解析”不是同一种状态。已解析节点采用中性显示，未知关系单独展示，不能把没有红色节点解释为功能已经正确。首版完整性仅针对支持范围内的显式调用模型，普通外部调用作为终点；外部回调、隐式特殊方法等运行关系不包含在完整性承诺内。

多语言并列展示不意味着跨语言调用已解析。TypeScript 接口/对象分派、JSX 隐式渲染、动态回调，Rust 字段接收者、一般泛型/trait 分派、宏展开和活动 `cfg` 条件均可能保留未知。统计按 `stats.by_language` 查看；TypeScript 项包含选入的 JS/JSX/MJS/CJS/MTS/CTS 文件。快照为 `partial` 时，应同时查看文件状态、诊断与未解析调用。

v0.4 对固定 TypeScript 语法库提供有限派生语法适配：有明确类型上下文的 qualified import 类型、类型对象内的 `abstract?:` 属性，以及已确认字符串/模板原文区域中的 NUL。保存的源码和原文件哈希保持不变；派生文本等宽并保留换行，记录改写范围、原/派生哈希和位置映射。未识别语法、代码区域 NUL、模板插值代码及运行时动态 import 不因此成为确定关系。源码证据仍来自原文，详细边界见 [静态分析范围](docs/STATIC_SCOPE.md)。

Rust 保留非泛型具体 `impl` 内直接 `self` / `Self::` 到唯一固有方法的有限绑定；具体 trait 实现中的 `self` 也可连接同类型的固有目标。v0.6 另支持同一个泛型固有 `impl` AST 身份内的直接 `self.method()` / `Self::static_method()` 词法绑定，保存 `generic_impl_binding` 及剩余前提；不验证泛型实例、bounds、实参类型、编译器命名空间或宏展开。trait 默认成员、Deref、额外方法约束和借用歧义仍可阻止绑定；字段接收者、dyn/trait 目标和其它泛型关系仍保留未知，不因生产装配有候选就推断唯一实现。

v0.13 修正 Rust crate 内属性的作用域：只在已配置 crate 根和完整普通属性语法下，将 `recursion_limit` / `type_length_limit` 识别为不改写声明的内置编译限制。原文、位置和模型前提保留；未知属性、活动 `cfg`、宏展开与 trait 分派不因此得到证明。

## 项目配置

v0.5 可显式注册 `serde-1.0.228-declared-helper-v1` 和独立 `rust-core-cmp-eq-interface-v1` 模型，默认不启用。模型依据捕获的 Cargo 声明、锁文件、名称环境与受限接口假设，仅解除对应 helper 的不透明性；不执行 Cargo、不加载目标依赖、不展开宏、不证明实际工具链。生成正文和其它未知边界保留，受影响边保存模型前提。实际配置见 [本轮 WWC policy](reports/astra-iteration2/winwincode-policy.json)。

在目标源码目录添加 `.callscope.json`。最小示例：

```json
{
  "schema_version": 1,
  "project": { "name": "my-project" },
  "analysis": {
    "languages": ["python"],
    "source_roots": ["."],
    "exclude": [".git/**", ".venv/**", "__pycache__/**", ".callscope/**"],
    "max_file_bytes": 1048576
  },
  "layers": {
    "API": ["app.api.*"],
    "DOMAIN": ["app.domain.*"],
    "STORAGE": ["app.storage.*"]
  },
  "entrypoints": ["app.api.submit_order"],
  "rules": [
    {
      "id": "submit-validation-connected",
      "kind": "required_path",
      "from": "app.api.submit_order",
      "to": "app.domain.validate_order",
      "severity": "high",
      "description": "提交入口必须在静态调用图中连接到校验函数"
    },
    {
      "id": "no-api-storage-call",
      "kind": "forbidden_call",
      "from": "app.api.*",
      "to": "app.storage.*",
      "severity": "high",
      "description": "API 不得直接调用存储层"
    }
  ]
}
```

`layers` 为符号提供层级标签；标签本身不会自动产生禁止规则。`entrypoints` 声明入口，不能把未声明的公共函数直接认定为死代码。端点可使用节点 ID 或限定名的 glob。必需规则要求每个匹配源至少连接一个匹配目标，禁止规则禁止任何匹配连接；要求多个目标分别存在时，应分别写规则。

扫描配置可以通过 `--config PATH` 显式指定。网页提供“保存配置”与“保存并扫描”：前者只保存并提示重新扫描，后者保存后再发起静态扫描。旧快照保留旧规则对应的发现。源码分析本身保持只读。

完整规则语义和不确定性边界见 [静态分析与约束说明](docs/STATIC_SCOPE.md)。

多语言项目显式设置 `analysis.languages`，并给工作区包及 crate 提供静态入口映射。例如将下面字段合入项目配置：

```json
{
  "analysis": {
    "languages": ["python", "typescript", "rust"],
    "source_roots": ["."],
    "module_aliases": { "@project/shared": "packages/shared/src/index.ts" },
    "rust_crates": { "project_core": "crates/core" }
  }
}
```

`module_aliases` 的键为 TypeScript 导入名，值为项目内源码入口；`rust_crates` 的键为规范 crate 导入名，值为项目内 crate 根目录。它们是用户提供的静态映射，不能代替构建产物或类型解析。未配置时默认为 Python 分析；扫描范围中的其他源码会显式标记未支持/未分析。

Python 节点使用 `module.qualname`；TS 节点使用 `ts:相对文件去扩展名#词法限定名`；Rust 使用 `rust:相对文件去扩展名#限定名`，方法限定名形如 `Type.method`。规则应使用扫描结果里的真实 ID，不将跨文件同名函数合并。

`analysis.support_inputs` 可显式列出项目内相对路径的 Cargo 或协议原文，保存为快照 `input_evidence`，不算新增已解析实现文件，也不生成调用节点。原字节哈希、UTF-8 文本哈希、内容和状态参与快照/CocoIndex 身份；读取失败不缓存，同路径代码/辅助原文不一致则拒绝发布。历史下钻只读保存文本。`static_contracts` 和 `value_contracts` 是与四类调用 `rules` 分开的顶层数据配置，必须记录来源、`author_approved`、适用条件及反证；独立审查来源不能冒称维护者已批准。支持范围和配置字段见 [静态约束说明](docs/STATIC_SCOPE.md)。

`value_contracts` 当前只支持 `call_argument_value`：选择文件、精确词法函数、callee 源码拼写、参数位置和对象字段路径，比较 literal/reference/member/call/conditional 形式及有限 const 初始化来源。`all_direct_calls` 排除嵌套函数和回调主体。配置 producer 时必须另列 `external_contract` 传输前提并保持 conditional；同名字段不是传输证据，callee 拼写也不是目标绑定证明。形式差异、未知和运行值证明分别记录；没有 finding 不代表参数或功能通过。

v0.7 的顶层 `navigation_contracts` / `atomicity_contracts` 同样只接受数据选择器、版本模型、来源和条件，均为 conditional。前者选择真实producer/factory/callback，可选wiring选择boot、injection及use；键集、参数/返回、guard和装配事实由保存AST生成。后者选择facade、authority、wrapper/lifecycle、资源和谓词来源；保护区域和差异不得预填。配置例见 [WWC](reports/astra-iteration4/winwincode-policy.json) / [CPB](reports/astra-iteration4/codepatchbay-policy.json)。模型假设、策略声明和未闭合分析分别保留，原CALLS不因独立装配模型而改为resolved。

顶层 `field_contracts` 支持 `parameter_field_flow`，只配置主体/形参字段及 `call_argument` 或 `return` 终点；`all_direct_sites` 保留全部所选评估，不预填中间传播。当前摘要为 finite-field-summaries-5-ir、wrapper/策略为 static-field-contracts-4-ir/static-field-policy-v2，公共IR为finite-immutable-semantic-ir-3。必须显式注册 ecmascript-own-enumerable-field-copy-v1；可独立追加 ecmascript-own-data-read-v1，copy-only不认证Get。sink.callee仅定位源码，helper/形参从保存CALLS认证；字段presence、复制时来源、shared referent、正常完成与运行值分开。见 [静态范围](docs/STATIC_SCOPE.md)及 [当前CPB策略](reports/astra-iteration9/codepatchbay-policy.json)。

导航、端口、保护与字段模块共用保存源码/词法身份、BuiltinEnvironment.audit和有限completion摘要；字段另消费公共不可变semantic_ir。v0.11 正式结果保留 services helper 十一键/缺键和 engine 的 conditional 来源关系，另四个入口字段评估仍 unknown；agent 的实际返回 literal 新增当前 copy 的条件终点见证。normal-prefix、copy/Get 模型和字段存在条件没有变成运行证明，见 [第九轮报告](reports/astra-iteration9/REPORT.md)。

v0.9顶层budget_contracts仅支持bounded_for_loop与counter_exhaustion_guard，evaluation=all_lexical_sites；subject={file,symbol}，counter/limit各为{kind:local_binding,name}，只定位唯一声明，不能填阈值、比较、更新或消费结论。必须注册captured-local-budget-source-v1并保留provenance和conditional条件。来源/比较/增量/helper原文由保存AST与实际CALLS提取，相关而不支持的候选保留unknown；嵌套函数激活另列。source_form_complete只限局部语法关系，数值域、实际次数、termination、全部支配与上游预算归属均未证明。 真实配置见 [CPB policy](reports/astra-iteration6/codepatchbay-policy.json)，来源准备不是自动结果。

## 人工处置与 AI 工具接入

处置记录独立保存，不降低原始严重度，也不抹除发现：

```sh
python -m callscope decide FINDING_ID --snapshot SNAPSHOT_ID --action fix_planned --reason "已登记调用连接修复" --db .callscope/demo.sqlite3
```

通过 stdio 启动 MCP 服务：

```sh
python -m callscope mcp examples/order_service --db .callscope/demo.sqlite3
```

工具接入用于让 AI 获取结构、发现和证据，提供 `scan_project`、`query_graph`、`get_anomalies`、`get_evidence`、`find_call_path`、`list_versions`、`compare_snapshots`。MCP 启动不自动扫描，先调用 `scan_project` 或使用已保存的项目快照。系统不自动修复代码，不提供 `trigger_verify`，也不允许通过工具执行目标项目。

## 独立观察与能力核对

Astra 的两份独立报告已冻结为 v1：[CodePatchBay](reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md)、[WinWinCode](reports/astra-baseline/WINWINCODE_ANALYSIS.md)。配套 [机器基准](reports/astra-baseline/capability-baseline.json) 包含两个仓库各 13 项、共 26 项人工观察，引用 36 份原文件；其中 9 项直接调用、1 项路径、3 项要求保留未知、13 项仅有证据。[基准协议](reports/astra-baseline/BASELINE_CONTRACT.md) 说明每项的成立条件、反证和能力边界。

对已有快照进行核对，不重新读取当前目标源码：

```sh
python -m callscope baseline reports/astra-baseline/capability-baseline.json --db DB --snapshot SNAPSHOT_ID --repo-id winwincode --output baseline-result.json
python -m callscope baseline reports/astra-baseline/capability-baseline.json --db NEW_DB --snapshot NEW_SNAPSHOT_ID --compare-db OLD_DB --compare-snapshot OLD_SNAPSHOT_ID --repo-id winwincode
```

数据库路径与快照 ID 要替换成真实值；省略 `--snapshot` 使用数据库最新快照，省略 `--repo-id` 按项目根匹配仓库。`--compare-db` 可读取另一数据库的旧快照，省略旧 ID 时选该库最新快照；同库比较只需 `--compare-snapshot`。比较要求两个快照来自同一项目。结果核对原文件哈希、引用与调用位置，分别记录确定关系、未知、来源变化和仅有证据的观察；对照不重新发布或改写快照、冻结基准。这个 CLI 始终输出 JSON，未新增 HTTP 或 MCP 基准接口。

两份报告合计提出五项人工分析结论，涉及参数传递、终态定义、幂等并发窗口、导航上下文和条件必填字段。它们在机器基准中仍是 `evidence_only`：**人工发现五项不等于 CallScope 自动检出五项，也不等于目标功能完整性通过。** 对照样本数不是功能覆盖率；只有调用路径无法裁决这些条件、字段与原子性问题。后续能力依赖与边界见 [能力路线图](docs/CAPABILITY_ROADMAP.md)。

基准核对器只允许辅助原文补齐 `evidence_only` 来源；不会把它变成 parsed SourceFile、真实 caller 或确定调用。v0.6 的核对器版本为 `frozen-static-baseline-1.3`，见证 `binding_models` 增加同 impl 泛型词法模型的有界摘要，保留模型版本、未验证前提与完整 edge 指针；依赖模型的 `reproduced` 不能表述为泛型编译、实际宏展开或项目工具链验证。

## 数据与部署边界

首版定位为本地单用户工具。网页默认仅监听 `127.0.0.1`，未实现企业级认证、租户隔离和加密存储，不应直接暴露到公网。

SQLite 快照保存扫描范围内的源码内容，数据库应按源码仓库的敏感程度保管。排除规则决定扫描范围；后续排除文件不会自动从已有快照删除它。配置写入和人工处置是管理操作，分析器没有修改源码能力。

CocoIndex 持久缓存同样含源码及分析结果，路径为快照数据库绝对路径后加 `.cocoindex`，需按同样标准保管。服务启动后若 CallScope 工具源码改变，必须重启服务再扫描；旧快照保持可读。

## 设计与扩展

- [修订后的架构设计 v1.1](docs/ARCHITECTURE_V1_1.md)
- [静态分析范围、规则语义和边界](docs/STATIC_SCOPE.md)
- [分析器、检测器和存储扩展指南](docs/EXTENDING.md)
- [Axon / CocoIndex 上游代码复用](docs/UPSTREAM_REUSE.md)
- [第三方声明及许可证依据](THIRD_PARTY_NOTICES.md)
- [首版历史实现审查](docs/INDEPENDENT_REVIEW.md)
- [CLI 与 HTTP API](docs/API.md)
- [源码示例说明](examples/order_service/README.md)
- [Python 基线共享协议](docs/IMPLEMENTATION_CONTRACT.md)
- [多语言实现协议](docs/MULTILANGUAGE_CONTRACT.md)
- [冻结观察与后续能力路线](docs/CAPABILITY_ROADMAP.md)
- [CodePatchBay 原分析报告 v1](reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md)
- [WinWinCode 原分析报告 v1](reports/astra-baseline/WINWINCODE_ANALYSIS.md)
- [26 项冻结观察与比较协议](reports/astra-baseline/BASELINE_CONTRACT.md)
- [WinWinCode 真实源码核对](reports/real-repositories/WINWINCODE_SOURCE_REVIEW.md)
- [CodePatchBay 真实源码核对](reports/real-repositories/CODEPATCHBAY_SOURCE_REVIEW.md)
- [Astra 两个真实仓库的独立审查](reports/real-repositories/REAL_REPOSITORIES_REVIEW.md)

这一组实现审查与旧扫描资料仅保留历史记录，不构成当前审批步骤；两份原分析报告是固定对照基准。

两个真实仓库报告保存的是 v0.2.0 的历史快照与统计，未因 v0.3.0 接入替换为新结果。它们不能作为新版引擎已经重扫或完成验收的证明。

v0.3 已另行完成两库的首次计算与缓存复用扫描，第二轮均保留相同快照 ID 且没有重复发布。各 10 项原有静态调用观察的结构、源码证据和未知状态均保持一致：

- [本轮上游接入与真实源码扫描](reports/upstream-reuse/UPSTREAM_REUSE_SCAN.md)
- [Astra 上游接入独立审查](reports/upstream-reuse/INDEPENDENT_REVIEW.md)
- [CodePatchBay 首次/重复扫描](reports/upstream-reuse/codepatchbay-integration.json)、[静态证据对比](reports/upstream-reuse/codepatchbay-witness-comparison.json)
- [WinWinCode 首次/重复扫描](reports/upstream-reuse/winwincode-integration.json)、[静态证据对比](reports/upstream-reuse/winwincode-witness-comparison.json)

新版依然保留两个项目的解析缺口，不能将缓存复用或这些源码观察解释为目标功能通过。

v0.4 的首轮结果另存于 `reports/astra-iteration1/`，两库均进行了正常静态扫描及缓存复用，重复扫描保持相同快照 ID、`created=false`：

| 仓库 | 完整解析 / 选入文件 | 已绑定调用 / 记录边 | 冻结正向关系重现 | 剩余文件缺口 |
| --- | --- | --- | --- | --- |
| CodePatchBay | 330 / 333 | 23,380 / 60,571 | 4 / 4 | 3 份 Shell 未支持 |
| WinWinCode | 465 / 471 | 15,784 / 171,983 | 3 / 6 | 6 份 Rust 未完整解析 |

TypeScript 原有 3 + 6 份解析缺口通过有限派生语法恢复，原错误与改写证据仍保存。确定关系样本合计从 v0.3 的 5/10 变为 7/10；三个 `unknown_required` 都在原调用位置保持未知。13 项仅证据观察中 12 项来源已核对，1 项为生成客户端来源未选入的 `source_missing`，没有从分母删除。WinWinCode 总绑定数从 16,357 降至 15,784，反映 trait 默认成员等边界收紧，不能说所有指标都提升。两库快照仍为 `partial`，以上均不是调用召回率、功能覆盖率或目标测试结果。

- CodePatchBay：[扫描/复用记录](reports/astra-iteration1/codepatchbay-integration.json)、[汇总](reports/astra-iteration1/codepatchbay-summary.json)、[原规则见证](reports/astra-iteration1/codepatchbay-rule-witnesses.json)、[v0.4 / v0.3 基准对照](reports/astra-iteration1/codepatchbay-baseline-v4-and-v3.json)
- WinWinCode：[扫描/复用记录](reports/astra-iteration1/winwincode-integration.json)、[汇总](reports/astra-iteration1/winwincode-summary.json)、[原规则见证](reports/astra-iteration1/winwincode-rule-witnesses.json)、[v0.4 / v0.3 基准对照](reports/astra-iteration1/winwincode-baseline-v4-and-v3.json)
- [TypeScript 派生语法来源复核](reports/astra-iteration1/TS_PROJECTION_REVIEW.md)

v0.5 的正式结果保存于 `reports/astra-iteration2/`，保留所有历史产物：CPB 330/333 份完整解析、23,380 条已绑定调用；WWC 465/471 份完整解析、15,799 条已绑定调用及 4/4 份辅助原文捕获。两库仍为 `partial`，冷/热扫描同 ID，热扫描不重复发布且每轮全量检测。冻结正向关系历程为 **5→7→9/10**，新增两项 WorkRun 关系依赖 serde helper 与 Eq 接口模型；3/3 指定未知保持，全部 26 项为 9 `reproduced`、4 `unknown`、13 `evidence_only`。辅助协议原文消除了来源缺失，没有证明跨语言调用。

两条配置式合同自动复核了 CPB 初始化集合缺 `superseded`（`open`）及 WWC 封闭对象未构造 `verificationCommand`（源码事实确定，Device 条件仍 `uncertain`）。这不是自动确诊两个业务 bug；重试预算、URL 上下文与并发幂等三项人工结论仍未自动覆盖。

- [第二轮正式报告](reports/astra-iteration2/REPORT.md)、[Astra 独立复核](reports/astra-iteration2/INDEPENDENT_REVIEW.md)
- [26 项能力账本](reports/astra-iteration2/capability-ledger.json)、[有限合同见证](reports/astra-iteration2/static-contract-witnesses.json)、[保存快照查询记录](reports/astra-iteration2/saved-query-observations.json)
- CodePatchBay：[扫描记录](reports/astra-iteration2/codepatchbay-integration.json)、[汇总](reports/astra-iteration2/codepatchbay-summary.json)、[v0.5/v0.4 对照](reports/astra-iteration2/codepatchbay-baseline-v5-and-v4.json)
- WinWinCode：[扫描记录](reports/astra-iteration2/winwincode-integration.json)、[汇总](reports/astra-iteration2/winwincode-summary.json)、[v0.5/v0.4 对照](reports/astra-iteration2/winwincode-baseline-v5-and-v4.json)

v0.6 增加有限调用参数来源合同及同 impl 泛型词法绑定，保持 schema 2 和原 26 项观察。三个独立来源稿区分可抽取事实与尚未实现的完整分析：[参数来源](reports/astra-iteration3/PARAMETER_EVIDENCE.md)、[导航上下文](reports/astra-iteration3/NAVIGATION_EVIDENCE.md)、[原子边界](reports/astra-iteration3/ATOMICITY_EVIDENCE.md)。worker 的 `maxRetries: 3` 是独立对象构造；`scopeHash` 会保留已有查询，缺键涉及无查询的字面路由种子；process fence 与队列目录锁有不同寿命。这些纠正不等于自动完成端到端字段流、URL 上下文或并发证明。参数稿的 11 项源码观察独立于冻结基准，不能混入自动检出计数。

v0.6 正式两库冷/热静态扫描结果如下；两库仍为 `partial`，冷/热快照同 ID、热轮 `created=false`，检测每轮全量计算：

| 仓库 | 完整解析 / 选入文件 | 节点 | 已绑定调用 / 记录边 | 冻结正向观察重现 | 辅助原文 |
| --- | --- | --- | --- | --- | --- |
| CodePatchBay | 330 / 333 | 11,085 | 23,380 / 60,571 | 4 / 4 | 0 |
| WinWinCode | 465 / 471 | 32,407 | 16,293 / 171,983 | 6 / 6 | 4 / 4 |

冻结正向观察历程为 **5→7→9→10/10**，新 Worker 关系来自同泛型 impl 的有限词法模型，未验证泛型实例、bounds、类型、编译器命名空间或宏展开。3/3 指定未知仍保留，全部26项为10 `reproduced`、3 `unknown`、13 `evidence_only`；这是样本重现数，不是功能覆盖率。

本轮共3条配置式有限合同发现：保留之前2条，并新增参数来源形式 `uncertain`。producer 的 `parsed.retries` 匹配合同，consumer 的字面量 `3` 形式不同；callee、transport 和 value equivalence 仍未知。不自动确诊3个业务bug，不证明端到端断接，URL key 传递与并发交错仍未自动化。独立参数稿的11项观察/31个AST锚点不计为自动字段流成果。

- [第三轮正式报告](reports/astra-iteration3/REPORT.md)、[Astra 独立复核](reports/astra-iteration3/INDEPENDENT_REVIEW.md)
- [26 项能力账本](reports/astra-iteration3/capability-ledger.json)、[有限合同见证](reports/astra-iteration3/finite-contract-witnesses.json)、[Worker 同 impl 词法见证](reports/astra-iteration3/worker-generic-binding-witness.json)
- CodePatchBay：[扫描记录](reports/astra-iteration3/codepatchbay-integration.json)、[汇总](reports/astra-iteration3/codepatchbay-summary.json)、[v0.6/v0.5 对照](reports/astra-iteration3/codepatchbay-baseline-v6-and-v5.json)
- WinWinCode：[扫描记录](reports/astra-iteration3/winwincode-integration.json)、[汇总](reports/astra-iteration3/winwincode-summary.json)、[v0.6/v0.5 对照](reports/astra-iteration3/winwincode-baseline-v6-and-v5.json)

v0.7 正式结果保存在 `reports/astra-iteration4/`：CPB 330/333解析、23,380绑定；WWC 465/471解析、16,293绑定及4份辅助捕获。图大小与v0.6相同；两库仍partial，官方CocoIndex冷/热同ID，热轮不重复发布，检测每轮全量。原26项仍为10 reproduced、3 unknown、13 evidence_only，36份冻结源身份和引用均匹配。

新增导航发现保存82条来源关系、8个声明节点、4条认证调用边；有限端口装配有23条事实，5段source/model支持，路由激活段未知。缺delivery经具体callback正常返回null和direct await触发async create的拒绝Promise；10项gap保留，不能宣布完整UI任务失败。原子发现保存15个声明节点、12条认证调用边以及保护范围/谓词差；3项gap保留，实际deps、集合heap、全写者和并发交错未闭合。共5条配置式有限发现，均来自独立审查且`author_approved=false`，不是自动裁定5个业务bug。

上述v0.7局部关系没有闭合完整参数运输/预算消费、状态生产与恢复保护、实际装配及交错、DOM/路由事件和跨语言Device guard。v0.9已实现公共不可变IR并接入字段适配器；下一步需改善真实字段效果/return摘要，再连接记录/消息和预算归属；性能最后。

- [第四轮正式报告](reports/astra-iteration4/REPORT.md)、[Astra独立复核](reports/astra-iteration4/INDEPENDENT_REVIEW.md)
- [完整目标合同](reports/astra-iteration4/GOAL_ACCEPTANCE.md)、[30义务实际账本](reports/astra-iteration4/goal-ledger.json)、[原26项账本](reports/astra-iteration4/capability-ledger.json)
- [五条有限证据](reports/astra-iteration4/finite-contract-witnesses.json)、[正常保存查询](reports/astra-iteration4/saved-query-observations.json)
- CodePatchBay：[冷/热扫描](reports/astra-iteration4/codepatchbay-integration.json)、[汇总](reports/astra-iteration4/codepatchbay-summary.json)、[v0.7/v0.6对照](reports/astra-iteration4/codepatchbay-baseline-v7-and-v6.json)
- WinWinCode：[冷/热扫描](reports/astra-iteration4/winwincode-integration.json)、[汇总](reports/astra-iteration4/winwincode-summary.json)、[v0.7/v0.6对照](reports/astra-iteration4/winwincode-baseline-v7-and-v6.json)

v0.8最终结果保存在 `reports/astra-iteration5/`：CPB330/333解析、23,380绑定；WWC465/471解析、16,293绑定和4份辅助输入，图统计保持不变，两库仍partial。最终冷/热同ID、热轮不发布重复快照，语言memo复用而检测full；原26项仍10 reproduced/3 unknown/13 evidence_only，36份来源匹配且与v0.7无分类变化。

新增三字段合同共五个分支/终点评估，全部unknown，源码事实分别75/35/16；所选字段shape和source-form完整位均false。真实rest排除、11个服务own keys和实际callee/形参是局部进展，不等于字段保留、消息运输或有效预算已证明。共8条配置式有限发现不代表8个bug。完整账本仍为五goal全部partial，30义务中4限定支持/19partial/7unknown，不因新来源事实提高完整判断通过数。

- [第五轮正式报告](reports/astra-iteration5/REPORT.md)、[Astra独立复核](reports/astra-iteration5/INDEPENDENT_REVIEW.md)、[v0.8目标账本](reports/astra-iteration5/goal-ledger.json)
- [字段逐路径评估](reports/astra-iteration5/field-assessments.json)、[8条有限见证](reports/astra-iteration5/finite-contract-witnesses.json)、[冻结26项账本](reports/astra-iteration5/capability-ledger.json)、[正常保存查询](reports/astra-iteration5/saved-query-observations.json)
- CodePatchBay：[最终冷/热扫描](reports/astra-iteration5/codepatchbay-integration.json)、[汇总](reports/astra-iteration5/codepatchbay-summary.json)、[v0.8/v0.7对照](reports/astra-iteration5/codepatchbay-baseline-v8-and-v7.json)
- WinWinCode：[最终冷/热扫描](reports/astra-iteration5/winwincode-integration.json)、[汇总](reports/astra-iteration5/winwincode-summary.json)、[v0.8/v0.7对照](reports/astra-iteration5/winwincode-baseline-v8-and-v7.json)

普通对象解构误标为新复制的首次结果已记录 [superseded](reports/astra-iteration5/SUPERSEDED_SCANS.json)，旧快照保留；上述最终结果只使用工具身份`90009066…`及finite-field-summaries-2，不改写旧证据。

本轮交付不运行任何测试套件，不执行示例应用。运行 CallScope 扫描源码属于工具自身的正常使用，目标代码仍仅作为文本读取；这些操作不能称为目标功能测试通过。本轮未运行浏览器或安装包验证，没有发布未经测量的检出率、误报率或性能承诺。

## v0.9 正式结果

v0.9最终双库冷/热扫描已完成：CPB330/333解析、23,380绑定；WWC465/471解析、16,293绑定及4辅助输入，两库仍partial，热轮同ID且created=false，检测full。原26项仍10 reproduced/3 unknown/13 evidence_only，36来源匹配、changes=[]。新IR字段三合同五位置全unknown，事实208/163/503；services helper own-shape退unknown，组件11键/absent观察不能补正式结果。两预算源码模式source_form_complete=true，numeric/runtime/termination/domination仍false；共10条有限发现不是10个bug。五目标仍partial，30义务为4限定支持/20partial/6unknown，仅P5新增局部预算来源partial。

两项预算只核对phase局部guard/四counter写及infra for/单步更新/helper出处，不认证CLI retries应控制哪个预算，也不按搜索缺同名字段判全程序未消费。事实数量和调用重现不是完整功能通过率。

- [第六轮报告](reports/astra-iteration6/REPORT.md)、[Astra复核](reports/astra-iteration6/INDEPENDENT_REVIEW.md)、[五目标／30义务账本](reports/astra-iteration6/goal-ledger.json)
- [字段评估](reports/astra-iteration6/field-assessments.json)、[预算评估](reports/astra-iteration6/budget-assessments.json)、[预算来源复核](reports/astra-iteration6/BUDGET_FORMAL_REVIEW.json)、[能力账本](reports/astra-iteration6/capability-ledger.json)、[有限见证](reports/astra-iteration6/finite-contract-witnesses.json)、[保存查询](reports/astra-iteration6/saved-query-observations.json)
- [正式IR迁移比较](reports/astra-iteration6/IR_MIGRATION_COMPARISON.json)、[迁移结果与边界](reports/astra-iteration6/IR_MIGRATION_RESULT.md)
- CodePatchBay：[冷/热扫描](reports/astra-iteration6/codepatchbay-integration.json)、[汇总](reports/astra-iteration6/codepatchbay-summary.json)、[v9/v8对照](reports/astra-iteration6/codepatchbay-baseline-v9-and-v8.json)
- WinWinCode：[冷/热扫描](reports/astra-iteration6/winwincode-integration.json)、[汇总](reports/astra-iteration6/winwincode-summary.json)、[v9/v8对照](reports/astra-iteration6/winwincode-baseline-v9-and-v8.json)

本轮未执行/导入/测试/构建目标，没有工具测试套件、浏览器或包安装验证。扫描和保存查询是正常静态工具使用，不是目标功能测试通过。

## v0.10.1 正式结果

v0.10.0的[第七轮候选](reports/astra-iteration7/SUPERSEDED_CANDIDATE.md)因内部EvidenceRef构造未重算内容标识而被替代；已导出引用复算未发现碰撞。v0.10.1修正规范构造后使用新工具身份和新快照，候选文件保留。

v0.10.1修复v0.9的字段精度退化：正式AST/IR摘要恢复services helper的十一自有键、封闭shape和maxRetries缺键。在`engine-runner.ts:157`的真实runJob实参位置，正常前缀及原copy/Get模型条件内支持`source_form_preserved_when_present`，selected-shape/source-form完整位为true；字段presence仍unknown，整个实参shape仍open，不证明激活、运行值、预算或运输。queue/agent另四位置继续unknown。

v9/v10两库目标源码、policy字节和policy hash相同，这一局部变化来自实现修复。两库冷/热扫描同ID，热轮created=false、请求语言memo全部复用，检测仍full；解析/图统计和原26项10 reproduced/3 unknown/13 evidence_only保持，36来源匹配、分类changes=[]。五完整goal仍0/5，30义务仍4限定支持/20partial/6unknown；P4的局部证据改善没有闭合整个必要义务。以上位置和事实计数不是功能覆盖率。

- [第八轮报告](reports/astra-iteration8/REPORT.md)、[五目标／30义务账本](reports/astra-iteration8/goal-ledger.json)
- [正式字段评估](reports/astra-iteration8/field-assessments.json)、[v8/v9/v10来源与字段比较](reports/astra-iteration8/FIELD_VERSION_COMPARISON.json)、[原26项账本](reports/astra-iteration8/capability-ledger.json)
- CodePatchBay：[冷/热扫描](reports/astra-iteration8/codepatchbay-integration.json)、[汇总](reports/astra-iteration8/codepatchbay-summary.json)、[v10/v9对照](reports/astra-iteration8/codepatchbay-baseline-v10-and-v9.json)
- WinWinCode：[冷/热扫描](reports/astra-iteration8/winwincode-integration.json)、[汇总](reports/astra-iteration8/winwincode-summary.json)、[v10/v9对照](reports/astra-iteration8/winwincode-baseline-v10-and-v9.json)

## v0.11.0 正式结果

两库的新静态快照保留原图和解析范围：CPB 330/333 份完整解析、11,085 节点、60,571 边；WWC 465/471 份完整解析、32,407 节点、171,983 边，两库仍为 partial。目标源码及策略保持，与新工具实现身份分别记录。

两库冷/热扫描保存相同快照 ID，热轮 created=false、全部请求语言 memo 复用，检测仍全量；这是语言整体前端缓存，不是逐文件语义增量。原26项冻结观察仍为10 reproduced/3 unknown/13 evidence_only，36项来源全部匹配，与v10分类 changes=[]。

三字段合同的五个所选评估共保存 41 条独立 source-structure 关系：engine 2 条、queue 两分支各 16 条、agent 两 return 各 3/4 条。它们显示实际形参连接、词法别名、写入尝试与返回构造，不是 41 个缺陷，也不是功能覆盖率。旧 engine 来源形式保留及 services helper 十一键/maxRetries absent 保持；queue/agent 四个入口字段结果仍 unknown。

`agent-config.ts:489` 的返回对象新增唯一的 `local_copy_retention_supported`：实际 `...metadata` 处的 maxRetries 自有可枚举 data slot 如果存在、普通复制正常完成，其 copy-time 值或引用在后置 `agents` / `agent` 固定键之后仍保留到匿名 literal 终点。它不证明入口 metadata 未变、字段存在、共享 child 内容、async fulfilled 值或后续运输，旧 source-form 结果继续 unknown。原五个完整目标仍为0/5，30必要义务仍为4限定支持/20partial/6unknown；账本是对正式自动证据的人工评审映射，新的局部见证不替代完整义务验收。

- [第九轮报告](reports/astra-iteration9/REPORT.md)、[Astra 独立复核](reports/astra-iteration9/INDEPENDENT_REVIEW.md)、[五目标／30义务账本](reports/astra-iteration9/goal-ledger.json)
- [正式字段评估](reports/astra-iteration9/field-assessments.json)、[独立结构与复制关系](reports/astra-iteration9/field-relations.json)、[v11/v10 字段比较](reports/astra-iteration9/FIELD_VERSION_COMPARISON.json)、[正常保存查询](reports/astra-iteration9/saved-query-observations.json)
- CodePatchBay：[扫描记录](reports/astra-iteration9/codepatchbay-integration.json)、[汇总](reports/astra-iteration9/codepatchbay-summary.json)、[v11/v10 对照](reports/astra-iteration9/codepatchbay-baseline-v11-and-v10.json)
- WinWinCode：[扫描记录](reports/astra-iteration9/winwincode-integration.json)、[汇总](reports/astra-iteration9/winwincode-summary.json)、[v11/v10 对照](reports/astra-iteration9/winwincode-baseline-v11-and-v10.json)
