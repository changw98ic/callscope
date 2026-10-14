# Astra 独立复核：第二轮静态能力迭代（v0.5）

结论：本轮可以作为有明确边界的静态能力增量交付。工具在冻结的 10 项正向调用／路径观察中重现 9 项，其中本轮新增的 2 项依赖显式注册的 Rust 可信接口模型；3 项必须保留的动态边界仍然正确保留。新增两类通用配置式规则复核了两项有限源码事实。工具仍不能独立产生或裁定完整人工报告中的全部业务判断，尚不能宣称整体超越该报告。

我阅读了实现、配置和正式保存的精简结果，并用标准库核对观察 ID、计数、quote 状态、模型标记及规则哈希。没有运行／导入／构建／测试两个目标仓库，没有运行测试套件或浏览器，也没有自行运行 CallScope。根代理完成了正常的静态冷／热扫描和发布；这些操作读取源码，未执行目标源码。本报告不把工具扫描完成称为项目功能测试通过。

冻结的 [v1 基准](../astra-baseline/capability-baseline.json)没有修改：`status=final`、26 项，SHA256 仍为 `16b4b05c8818fa1eecf396132ebe2ea29a8f0068801165f0649da379d9041dd7`。原始两份 Astra 项目报告的结论、条件与反证保持不变；[第一轮独立复核](../astra-iteration1/INDEPENDENT_REVIEW.md)记录 v0.3→v0.4 的进展。

| 保存身份与规模 | CodePatchBay | WinWinCode |
| --- | --- | --- |
| 目标 commit | `4f2d2eca31d90b0122db1c1429dd365672db2393` | `da407e4f3df3719718b23bd8913b73fe3ff73857` |
| v0.5 snapshot | `e55cd3d2d84ee473026bafa9169a7a3ccdab19d3e4815a5575f726aaa805af00` | `e372ed1670979aaf53f52df905844647892e02d9a418f0eba5311f2a6c3e6ab1` |
| 选入／解析成功／缺口文件 | 333 / 330 / 3 | 471 / 465 / 6 |
| 剩余文件缺口 | 3 个 Shell 文件不在语言能力内 | 6 个 Rust 解析失败文件 |
| 节点／边／resolved 边 | 11,085 / 60,571 / 23,380 | 32,407 / 171,983 / 15,799 |
| 辅助原文输入 | 0 | 4；不计作新增已解析实现文件 |
| 静态合同规则 | 1 | 1 |
| 快照完整性 | `partial` | `partial` |

两库冷扫描都重算其配置语言并发布新快照；热扫描复用对应语言 bundle，保持同一个 snapshot ID，`created=false`，仍全量重新执行检测。WWC 配置中的 Python 是 0 文件 bundle，不应表述成分析了 Python 生产代码。正式依据为 [CPB integration](codepatchbay-integration.json)、[WWC integration](winwincode-integration.json)及两份 `*-summary.json`。未加载巨型完整导出或数据库。

保存的工具源码指纹为 `300f396835db0463d087ce5c830f55816233bb0e91b9220fe1ec01a2155273e0`。分析器为 `static-multilang-5`，检测器为 `call-rules-4-static-contracts`，快照 schema 为 `2`；Rust 前端为 `rust-tree-sitter-1.6-helpers`，静态合同为 `static-contracts-1`。比较两边使用同一个基准核对器 `frozen-static-baseline-1.2`，其实现指纹为 `947a4c63a27a95de1231888a6c908ad129000334880237db85c31d1d5b7e3335`。

全体 26 项的观察 ID、顺序和冻结文档一致。CPB 19 份基准源身份匹配；WWC 17 份匹配，其中生成协议客户端是辅助原文。合计 35 份实现源码加 1 份辅助原文；已核对 quote 没有失败。以下计数没有剔除未知或高阶观察：

另外逐项核对了独立导出的 [能力台账](capability-ledger.json)和 [静态合同见证](static-contract-witnesses.json)：台账的 26 项状态、期望、源身份及汇总与原始比较产物完全一致，两条合同 finding 与对应保存快照摘要中的完整记录完全一致。

| 结果 | CPB v0.4→v0.5 | WWC v0.4→v0.5 | v0.5 合计 |
| --- | --- | --- | --- |
| reproduced | 4→4 | 3→5 | 9 |
| unknown | 2→2 | 4→2 | 4 |
| evidence_only | 7→7 | 5→6 | 13 |
| source_missing | 0→0 | 1→0 | 0 |
| 总数 | 13→13 | 13→13 | 26 |

4 项 unknown 中有 3 项本来就要求保留未知，另一项是尚未支持的正向观察 `WorkerMain.accept_control→accept_dispatch`。10 项正向观察的重现历程为 v0.3 的 5 项、v0.4 的 7 项、v0.5 的 9 项；这是一组冻结的针对性观察，不是统计估计的项目功能覆盖率、缺陷召回率或一般 Rust／TS 准确率。

本轮完整比较仅有 3 项状态变化，见 [CPB 基准比较](codepatchbay-baseline-v5-and-v4.json)和 [WWC 基准比较](winwincode-baseline-v5-and-v4.json)：

| 冻结观察 | v0.4→v0.5 | 精确新增证据 |
| --- | --- | --- |
| `wwc.delivery.start-next-to-item` | unknown→reproduced | `workrun.rs:411:8 self.start_item`，边 `rust-call:a3066171453c3baeae01fee0` |
| `wwc.delivery.start-item-validation` | unknown→reproduced | `workrun.rs:419:8 self.validate`，边 `rust-call:fa068277a98006959937f3af` |
| `wwc.protocol.client-to-rust-dispatch` | source_missing→evidence_only | 保存了 generated control-plane-client 原文、SHA256 与原始 quote；没有生成跨语言确定调用边 |

两个 WorkRun 绑定使用同一原文件 SHA256 `4fd4fefee2ed35883f686928b87e711e9584934cf9360ecc85fd683b406b0b2b`，调用者、目标与调用位置符合冻结观察。其 compact witness 明确保留以下前提，不能省略后只称“源码已经完全证明”：

- `serde-1.0.228-declared-helper-v1`：在显式配置、捕获的 manifest／lock 和完整名称环境下，把配对的窄 `serde` 属性识别为 helper。
- `serde-1.0.228-receiver-interfaces-v1`：模型只封闭受支持 derives 对原接收器的成员名竞争接口，包括相关默认成员；不生成宏函数体。原接收器不新增固有方法／Deref 是该显式可信模型的假设。
- `rust-core-cmp-eq-interface-v1`：标准 Eq 接口的显式假设，保留 `eq`、`ne` 和 hidden 默认成员的竞争边界；实际标准库源码未捕获，项目工具链未验证。

已检查实现不会仅按字符串 `serde`／`Eq` 直接放行：别名 patch、另指 workspace、哈希不一致、名字遮蔽、星导入、未知宏、cfg、重复上下文、遍历中断及泛型／Deref 限制都有相应保守处理。宏展开、生成体与其它生成项仍保持未知；类型声明边界没有被删掉。来源模型、命名空间证据及原快照／edge 指针保存在证据中。正式统计只显示 WWC 本轮新增 15 条 resolved 边；我精确核对了其中这 2 条冻结基准见证，没有据此逐条背书其余 13 条，也不把边数增长当成功指标。

三条必须未知的边仍在原位置、`target=null`、`resolution=dynamic`，且存在对应真实 caller：`cli/cpb.ts:186 mod.run`、`core/engine/run-job.ts:127 ctx.appendEvent`、`worker/src/lib.rs:2744` 开始的 `self.codex.ensure_thread`。这排除了通过丢弃 caller 或把坏 resolved 边冒充未知来满足基准的做法。泛型 Worker 的正向固有调用尚未重现，不能因此声称业务实现缺失。

两条新静态合同的 `contract_hash` 与保存的配置逐字规范化重算一致；finding、evidence 的 snapshot、source、policy 身份均相符，证据文件哈希与原人工基准相符。规则都明确来源于独立审查，`author_approved=false`，没有冒充仓库维护者已批准的业务规范。

| 配置式静态事实 | 已确认的自动结果 | 保留的边界 |
| --- | --- | --- |
| CPB：两个 `TERMINAL_STATUSES` 初始化字符串集合相等 | `event-materializer.ts:792` 为 5 项；`job-store.ts:430` 为 4 项，少 `superseded`。结果 `open`，无形状未知。 | 只比较配置指定的声明初始化成员；不证明运行时集合不变、全部终态语义等价或所有恢复分支都错误。 |
| WWC：`clarificationUpdateCommand` 返回对象 `payload.spec` 构造 `verificationCommand` | 唯一直接 return 的 spec 字面对象在 `:204–219` 形状封闭，缺该字段；消费者 Device then 分支在 Rust `:616–617` 读取该字段，else 分支 `:641` 另选命令。结果仍是 `uncertain`。 | `external_applicability_not_inferred` 明确保留。源码没有自动证明 producer 到 Device 分支的可达性、授权前置条件、字段非空或完整消费校验。 |

CPB finding 为 `55dd550622cb4430b071851c`，合同哈希 `3cbceb399081fb2060a9b636c454eb592983770f06b7e66336624910b5a4b941`。WWC finding 为 `7414a8a037043a2794e749fe`，合同哈希 `8543f89585c9e89e5ad118ea3eda9e008c1d92dda16d75c2e48509844228cc67`。完整原文片段、grammar 版本、坐标及 span 哈希已随 finding 保存。

这两条规则是人工选择合同后，由工具自动复核有限源码事实；它们没有自主发现业务意图。人工报告中的 CPB 终态差异与 WWC Device 编辑问题仍为主基准的 `evidence_only`。不能把额外静态事实条目偷偷并入 26 项的 reproduced 计数，更不能据此称为“已自动确认两个运行故障”。其它 3 项人工缺口——CLI 重试预算断接、并发幂等窗口、看板新任务缺少 delivery 上下文——仍未被本轮工具自动裁定。

辅助输入的集成具备可审计的身份边界：只读取明确声明的相对路径，安全描述符读取后保存原始字节哈希、解码文本哈希、原文及失败状态；不调用 Cargo、不加载目标依赖。完整捕获值进入快照与 CocoIndex 输入身份；读取失败不记作可复用成功。代码与辅助输入若同路径而内容／哈希冲突，发布会被拒绝。基准核对器只允许 `evidence_only` 使用辅助原文；它不会伪造 parsed SourceFile、Node、caller 或确定调用。WWC 协议观察从 source_missing 变为 evidence_only 正是这一边界的实际表现。

源码审查发现并已修复的问题包括：转义标识符字段可能形成错误“缺字段”负证；Set 构造器的可见解构、catch、var 提升绑定遗漏；helper provider 对别名 package patch 和 workspace 的来源假设过强；Eq 被过度简化为空方法集合；模型前提在 compact witness 中丢失。当前保存产物与修正后的实现一致，未见本轮剩余已确认的 P0/P1 阻断项。此结论限定于已审实现和这些保存证据，不是语言完备性证明。

可扩展方向值得保留：事实模型、条件、合同来源、原文证据和不可变身份分开；规则使用通用 AST 选择器而非仓库名分支；未知不会因提升指标被改成确定。下一步的功能优先级仍应放在有源码见证的对象／端口候选、条件字段传递和事务边界，而不是继续堆叠图分数。若要进一步接近完整报告，应让工具生成可追踪的生产者—消费者与锁／提交边界解释，再分别复核反例；单纯增加 resolved 边不能替代这些能力。

本轮没有验证浏览器交互、wheel 安装、增删改名失效、故障恢复、并发源码修改或目标运行行为。冷／热正式扫描证明了当前固定输入下扫描、检测、发布与缓存复用的可用性。原始基准、v0.3／v0.4 产物和本轮 v0.5 产物分别保留，未覆盖历史结果。
