# CallScope v0.5：对照 Astra 报告的第二轮能力迭代

两份独立源码报告已经完成，并冻结了 26 项观察。本轮把其中 10 项正向调用／路径观察的重现数从 v0.4 的 7 项推进到 9 项；新增两项依赖显式注册的 Rust helper 与标准接口模型。另增加两类可配置的静态合同检查，自动复核了终态初始化集合的缺项和一个返回对象的字段遗漏。仍不能把这些结果称为两库功能通过、90% 功能覆盖，或已经整体超越人工报告。

优先级保持为：正确且可用的有限静态结论、可扩展的证据与合同接口、最后才是性能。本轮没有执行、导入、构建或测试目标仓库，也没有触发目标项目的 CLI、验证 probe、沙箱或动态 trace。运行的是 CallScope 的正常静态扫描、数据导出与冻结基准核对；不宣称自动化测试套件通过。

## 独立报告与不变的比较对象

- [Astra CodePatchBay 完整源码分析](../astra-baseline/CODEPATCHBAY_ANALYSIS.md)：覆盖账本、主要执行链、三项具体结论、反证与未审范围。
- [Astra WinWinCode 完整源码分析](../astra-baseline/WINWINCODE_ANALYSIS.md)：主要前后端／Rust 链、两项具体接线缺口、条件与反证。
- [冻结基准](../astra-baseline/capability-baseline.json)：26 项观察、36 份原文件哈希，仍为 `final`；SHA256 `16b4b05c8818fa1eecf396132ebe2ea29a8f0068801165f0649da379d9041dd7`。
- [本轮 Astra 独立复核](INDEPENDENT_REVIEW.md)：审查实现和正式保存产物，独立判断结论边界。
- [机器能力账本](capability-ledger.json)及[两条合同的完整证据](static-contract-witnesses.json)。

“完整报告”指已经写清主要模块、生产链、证据和审查边界；它不是逐行审查所有第三方实现，更不是全业务验收。工具迭代没有修改人工原报告或缩减基准分母来提高数字。

## 正式两仓库结果

| 保存项 | CodePatchBay | WinWinCode |
| --- | --- | --- |
| 目标提交 | `4f2d2eca31d90b0122db1c1429dd365672db2393` | `da407e4f3df3719718b23bd8913b73fe3ff73857` |
| v0.5 快照 | `e55cd3d2d84ee473026bafa9169a7a3ccdab19d3e4815a5575f726aaa805af00` | `e372ed1670979aaf53f52df905844647892e02d9a418f0eba5311f2a6c3e6ab1` |
| 选入代码文件／解析成功 | 333 / 330 | 471 / 465 |
| 文件解析缺口 | 3 个不支持的 Shell 文件 | 6 个 Rust 语法解析失败文件 |
| 辅助输入捕获 | 0 | 4 / 4；不算作新增解析成功代码文件 |
| 图节点／记录边 | 11,085 / 60,571 | 32,407 / 171,983 |
| 已绑定内部静态调用 | 23,380 | 15,799 |
| 快照状态 | `partial` | `partial` |
| 冷扫描 | Python、TypeScript 重算并发布新快照 | Python、Rust、TypeScript 重算并发布新快照 |
| 热扫描 | 同 ID、`created=false`，两语言前端复用 | 同 ID、`created=false`，三语言前端复用；Python 为 0 文件 bundle |

两次扫描均完整重算检测器。CocoIndex 的维护粒度仍是语言 bundle，没有宣称逐文件语义增量或任意三跳内分析完备。Axon 图核心与官方 CocoIndex 1.0.25 继续参与实际运行，复用来源见[上游代码说明](../../docs/UPSTREAM_REUSE.md)。

同一正式工具源码身份为 `300f396835db0463d087ce5c830f55816233bb0e91b9220fe1ec01a2155273e0`，schema `2`、分析器 `static-multilang-5`、检测器 `call-rules-4-static-contracts`。冻结观察核对器版本 `frozen-static-baseline-1.2`，其自身源码哈希 `947a4c63a27a95de1231888a6c908ad129000334880237db85c31d1d5b7e3335` 与图的工具身份分别记录。正式扫描期间核心实现保持冻结。

直接产物：[CPB 扫描](codepatchbay-integration.json)、[WWC 扫描](winwincode-integration.json)、[CPB 精简图统计](codepatchbay-summary.json)、[WWC 精简图统计](winwincode-summary.json)、[CPB v0.5/v0.4 对照](codepatchbay-baseline-v5-and-v4.json)、[WWC v0.5/v0.4 对照](winwincode-baseline-v5-and-v4.json)。

## 冻结基准：进展与分母

| 观察类别 | 总数 | v0.3 | v0.4 | v0.5 |
| --- | --- | --- | --- | --- |
| 正向直接调用／静态路径 | 10 | 重现 5 | 重现 7 | 重现 9，其中新增 2 项有显式模型前提 |
| 必须保留未知的真实调用点 | 3 | 保留 3 | 保留 3 | 保留 3 |
| 高阶关系、合同与风险观察 | 13 | 不自动裁决 | 不自动裁决，其中 1 项来源缺失 | 不自动裁决；来源缺失已补捕获 |

v0.5 全部 26 项的状态为 **9 项 reproduced、4 项 unknown、13 项 evidence_only**。4 项 unknown 包含 3 项本来要求保留的未知，以及 1 项尚未重现的正向关系。没有 `source_changed`、`source_missing`、引用不匹配或端点缺失；36 份基准原文件哈希均有保存来源并匹配。

本轮新增重现：

| 观察 | 原始调用点 | 确定目标 | 前提 |
| --- | --- | --- | --- |
| `wwc.delivery.start-next-to-item` | `application/workrun.rs:411`，`self.start_item` | `WorkRunAggregate.start_item` | 已捕获 Cargo 声明／锁文件、注册 serde helper profile 与 Eq 接口模型 |
| `wwc.delivery.start-item-validation` | `application/workrun.rs:419`，`self.validate` | `WorkRunAggregate.validate` | 同上；不证明验证器覆盖所有领域不变量 |

模型只在限定声明、名称绑定、成员冲突与 receiver 范围成立时解除对应 helper 属性的不透明性。没有实际展开宏，没有读取目标工具链的标准库源码，也没有验证实际 Cargo 依赖解析。生成方法正文、未知宏、cfg、泛型、Deref、未知 trait 及对象字段分派仍保留未知；模型身份和这些假设随调用边与基准见证保存。

仍未重现的正向观察是 `WorkerMain.accept_control` 到 `accept_dispatch`，受泛型容器边界限制。真实 `self.codex.ensure_thread` 仍保持未知，不能因读到一个生产实例就把公开泛型定义的所有调用提升为唯一绑定。

生成客户端协议原文现在作为辅助输入存入快照，故 `wwc.protocol.client-to-rust-dispatch` 从 `source_missing` 变为 `evidence_only`。这只补齐可审计的原文来源，没有生成跨语言 CALLS 或证明协议字段传递完整。

## 自动合同复核与人工结论的关系

两个检测器是通用 AST 选择器与数据合同，目标路径和规则放在[CPB 配置](codepatchbay-policy.json)、[WWC 配置](winwincode-policy.json)。实现没有硬编码两个仓库名称、状态值或业务参数。合同记录审查来源、`author_approved=false`、政策哈希、适用条件和反证；工具不会把审查者的合同说成仓库维护者已经批准的产品规范。

| Astra 原观察 | 本轮自动复核 | 尚不能推出 |
| --- | --- | --- |
| CPB `superseded` 终态分类不一致 | 两个封闭字符串初始化集合分别含 5 与 4 项，job-store 缺 `superseded`，状态 `open` | 所有运行时 Set 恒定、非法状态写入发生、recovery 策略必须开放 |
| WWC Device 编辑遗漏 `verificationCommand` | `clarificationUpdateCommand` 的封闭 `payload.spec` 返回对象含 10 个字段，没有所需键；保存 Device then guard 和 non-Device else 反证，状态 `uncertain` | producer 一定进入跨语言 Device 分支、所有编辑失败、字段存在即非空或校验通过 |
| CPB `pipeline --retries` 参数接线 | 仍为人工报告证据 | 跨函数、队列、worker 的字段消费与默认覆盖已经自动追踪 |
| WWC 新任务导航缺 delivery 上下文 | 仍为人工报告证据 | URL 来源、页面注入闭包和条件拒绝链已经自动关联 |
| CPB 同键去重的并发窗口 | 仍为人工条件风险 | 锁／事务范围、权威约束与交错已被自动证明或运行复现 |

条件合同即使字段遗漏这一源码事实确定，也继续输出 `uncertain`。别名、对象 spread、计算键、未知构造器、嵌套函数返回和不完整集合不会被当作封闭对象的否定证明。这轮是 **2 条配置式有限源码事实自动复核**，不是自动确诊五项人工业务推导中的两项，更不是一般数据流分析已完成。

## 证据维护与后续能力顺序

辅助文件通过显式相对路径、禁止符号链接的只读捕获进入 `input_evidence`，保存原字节哈希、文本哈希、大小及状态，并参与输入／缓存身份。历史源码查询读取保存内容，不回到当前磁盘解释旧结果。代码与辅助输入重叠而内容不一致时拒绝发布；辅助输入捕获失败时保留缺口并绕过前端 memo，避免把暂时读失败缓存为成功。

下一步能力依赖仍由[能力路线](../../docs/CAPABILITY_ROADMAP.md)约束：先补可追溯的对象工厂、端口注入与协议关系，再扩展字段来源、默认覆盖及 URL 保留，随后分析支配关系、事务边界和具体并发交错。每类关系需要独立类型、证据和未知，不能都伪装成普通调用边；新增真实独立样本也需保留原始分母。

本轮用正式冷／热扫描、不可变发布、正常查询和独立源码／产物复核验证了上述固定输入的交付行为。[保存查询记录](saved-query-observations.json)确认两种合同发现可通过查询返回，生成协议源码返回内容与保存文本哈希一致。30 份工具 Python 源码通过 AST 语法核对；新发现类型补了中文界面标签，JavaScript 通过语法核对，条件发现仍显示待确认。两目标仓库 Git 工作区保持清洁，见[只读仓库状态记录](target-state-observations.json)。

没有运行工具测试套件、浏览器或安装包验证；增删改名、崩溃恢复、并发修改捕获和更广语言组合也没有在本轮额外验证。当前服务进程的界面没有被宣称已经刷新到本轮版本。性能没有作为本轮成功标准。文档、版本与工具身份核对见[交付核对记录](verification-summary.json)。
