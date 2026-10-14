# Astra 独立复核：第四轮静态语义链

**结论：v0.7 的有限静态语义能力可以交付，五项完整判断目标仍未完成。** 已完成实现源码、正式双仓产物及目标账本的独立复核，未发现本轮剩余阻断问题。本轮进展是实际来源／guard／保护区间推导，原调用基准没有增长。

## 审查边界

本审查只读 CallScope 实现、两库源码及已保存 JSON 证据，修改的只有本人报告。未执行 CallScope 模块、目标程序、目标导入、构建、测试套件或浏览器。其它代理正常使用受信解析器读取保存源码的观察，是工具输出证据，不是目标执行或功能测试。

原 26 项基准 SHA-256 仍为 `16b4b05c8818fa1eecf396132ebe2ea29a8f0068801165f0649da379d9041dd7`。五项人工业务判断保持冻结；新能力另按 [GOAL_ACCEPTANCE](GOAL_ACCEPTANCE.md) 的 30 项必要义务衡量。原基准 10 个正向关系重现不能代替这些义务。

## 已确认的实现进展

- 共享来源层认证保存原文、原哈希、派生 CST、声明和原调用边；新语义关系不改写历史 CALLS。BOM 的保存文本坐标与原字节偏移分开记录。
- 共享词法层区分声明身份、值稳定性及运行时值。未知身份不能因拼写相同被连接；空写入列表不排除任意别名或外部 effect。
- 端口装配已从实际源码推导启动字面对象、真实 factory 分支、同一端口声明注入、VM 参数字段捕获和返回方法内的使用。有限动态 import 装配单列模型，旧调用边仍动态。

[PORT_WIRING_OBSERVATIONS.json](PORT_WIRING_OBSERVATIONS.json) 是对 v0.6 已保存快照的开发观察，末轮模块哈希为 `7e7291643aa873a697b7ea9d123fb274732badeb617754f73d7619ad6a9efc45`。我核对了其 23 个来源事实、5 个有限装配段和 6 个残余 gap；`assembly_complete=true` 的范围没有扩大到路由或事件触发，`end_to_end_complete=false`。生成器返回 iterator、未等待的 async 工厂返回 Promise 均不能被当成端口对象；普通 async `create` 的 body throw 表示 Promise 拒绝。这不是正式 v0.7 完整扫描结果。

两项共享层已完成末轮源码复核：`semantic_sources.py` 为 `dab9108e47787b451665563bc08aab62e906eb0e02d3f77c2f70182bf00f5381`，`lexical_bindings.py` 为 `5e8d787afd041afc6b30452b7d33fb1f6e2692f182f8dcbd14d36c05ab2ac081`。前者按完整调用跨度与原表达式区分同起点的嵌套调用，后者仅从默认形参模式左侧提取声明，不把默认表达式当成新声明。

导航模块末轮哈希为 `84fef8803a8cd378f572faa29683dbadfa39e7bc4967751efc3eb098b105f3e1`，与 [开发观察](NAVIGATION_DEVELOPMENT_OBSERVATIONS.json) 的 `tool_sources` 一致。独立核对到 82 条有限来源事件、8 个实际图节点和 4 条原图边；所选链接的 guaranteed keys 为空，possible keys 为四个 Scope 键，实际消费键 `delivery` 不在其中。同一 factory context 的 hash→raw query→URLSearchParams 投影与 null 返回、async 拒绝关系已连接。真实反证入口的 `delivery` 属于 guaranteed keys，证明 helper 保留已有 query。结果仍有 10 个 gap，`full_functionality_proven=false`；这些数字只描述未发布的开发观察。

## 冻结前已修正的关键问题

本轮已报告的关键问题均已修复或保守降为未知，当前未见阻止正式扫描的剩余 P1。以下结论来自源码复核，拒绝边界没有通过合成用例或测试套件验证：

1. 短路表达式及 ternary 分支对 query receiver 的真实静态效果；跨 helper／closure 的未建模对象不能被重建成另一个确定对象。
2. 缺键→null→throw 要由 guard 真值、对应上下文及返回覆盖共同推出；不能以几个事件都出现代替逻辑蕴含。factory 形参的直接和嵌套逃逸不能省略。
3. 回调函数值与同根成员调用严格区分；取得结果、异步 completion、失败 guard、读写和释放位置都需要实际 AST 关系。
4. 简单形参声明身份不因其它默认解构而丢失，但参数默认 RHS 的写入不能被 body 范围过滤。
5. 去重 guard 的正负极性、实际循环 binder、完整字段集合和标准 Set 来源必须明确；展示采样不能参与语义判定。
6. 导航来源须逐段保持 hash、原始 query 和 URLSearchParams 三种表示；常量 query 或一般控制依赖不能冒充当前导航的查询投影。`slice(indexOf('?') + 1)` 只有在分隔符存在时才是查询尾部。
7. 集合初始化必须引用实际裸数组值，不能用同根成员路径代替；锁释放还须检查中间退出和 `finally`，不以源码顺序证明可到达。

原子模块末轮源码哈希为 `899f6fdb7fab0e67576cf4543e404dc76a4d4eb8604b55a6aae21be2234254c6`。其释放模型限于已识别的外层直接控制区域：错误保存目标必须是 try 之前已初始化的可写局部变量，mutation try 无 finally，中间只允许无效果声明，release fence 是下一释放 try 的直接首句。集合模型则要求同步谓词、真实 for-of 项、稳定且经受信 freeze 的数组裸值，以及未逃逸的 Set 成员用法。它们不认证操作系统锁、任意回调效果、所有写者或可达并发交错。

[原子开发观察](ATOMICITY_DEVELOPMENT_OBSERVATIONS.json) 与该哈希一致：15 个实际图节点、12 条原图边；目录保护 region、fresh read／callback／save 映射及释放尝试是有条件的来源模型。两个 process fence 只包围取得和释放回调。外层非终态集合与内层 `pending` 等式、额外 `description`／`originJobId` 字段均来自源码。默认依赖装配、集合 heap 身份、协议运行前提三类缺口保留，未推导交错。

另外对开发稿做了原字节身份核对：导航证据递归覆盖 6 份源文件、146 个去重 span；原子证据覆盖 5 份源文件、105 个 span。文件 SHA-256 和跨度 SHA-256 均与目标原文件一致，未发现串文件或坐标偏移。这是 JSON／原文一致性核对，不是程序测试，也不替代正式新快照核验。

## 尚不能宣布完成的目标

当前完整导航路径仍缺路由 dispatch／用户事件等必要接线；有限端口装配不会使这些义务自动通过。原子分析首版也不计算并发交错，不证明默认动态依赖的实际选取、所有写者或部署物理资源身份。完整 `--retries` 运输与消费、跨语言规格协议映射、终态与可恢复政策的其它义务仍按独立账本保留。

可扩展性方面，新共享来源和声明身份协议有实际价值；nav、port、atomic 对标准内建的可见遮蔽／写入／逃逸仍有重复实现。应在后续提取版本化环境审计接口，避免相同正确性修复在多个分析器中漂移。本轮不为该重构扩大冻结范围。

同时应将有限表达式、guard、正常返回和 completion 摘要逐步复用，域分析只增加 URL、集合或锁协议的明确语义。当前模块可以解释支持的具体形状；它们还不是通用路径敏感字段流或并发求解器。新增一种形状必须带上来源、模型适用范围及拒绝条件，不能只靠扩大选择器覆盖率。

## 正式产物核验

[CORE_FREEZE.json](CORE_FREEZE.json) 的工具源码身份为 `d0b2f76e6f8c398758e0d3ba2b8f0d583876de636062b758ac94e216afcbe49c`；五个新增组件的冻结哈希与上述独立复核一致。正式版本为 `static-multilang-7`／`call-rules-6-semantic-relations`，schema 仍为 2。

| 项目 | CodePatchBay | WinWinCode |
| --- | --- | --- |
| 正式快照 | `4866cb471f54673322145c50750546b90077746e9fd83c3f58221aeafe92962a` | `10bcd33b59b4eb76f67eaabf825782cb3434d8a9c6909c106036a4c82db13b3e` |
| 选入／已解析文件 | 333／330 | 471／465 |
| 图节点／边 | 11,085／60,571 | 32,407／171,983 |
| resolved 调用 | 23,380 | 16,293 |
| 原 13 项基准 | 4 reproduced、2 unknown、7 evidence_only | 6 reproduced、1 unknown、6 evidence_only |
| 全部发现条目 | 40,555 | 139,686 |

这些发现条目包含结构和覆盖诊断，不是项目缺陷数。CodePatchBay 的 3 个未解析项是未支持的 Shell 文件；WinWinCode 有 6 个 Rust `parse_error`，不能把解析器失败当成项目编译错误。两仓均保持 `partial`，选入范围之外也没有覆盖承诺。

[CPB integration](codepatchbay-integration.json) 与 [WWC integration](winwincode-integration.json) 均记录 cold 新建、warm 不重复发布，前后同一个 snapshot ID，CocoIndex 热复用对应语言前端而全局检测仍为 `full`。这是正常静态工具运行的保存证据，不是测试套件结果；也不证明所有增删改名或故障恢复情形。

两个 [CPB 基准比较](codepatchbay-baseline-v7-and-v6.json)／[WWC 基准比较](winwincode-baseline-v7-and-v6.json) 合计仍为 **10 reproduced、3 unknown、13 evidence_only**，相对 v0.6 无状态变化；36 份来源检查均 matched。原有 `mod.run`、`ctx.appendEvent`、`self.codex.ensure_thread` 未知项仍对应实际调用位置的 dynamic 边；WorkRun 的 serde／Eq 前提、Worker 同泛型 impl 的未验证参数／bounds／命名空间前提仍在见证中。没有以缺 caller 或源码变化满足 unknown，也没有移除 evidence_only 提高分母内比例。

[有限合同见证](finite-contract-witnesses.json) 有 5 个配置式结果：旧初始化集合、参数来源形式、Device 对象字段各 1 个，加本轮导航和原子保护各 1 个；其中 1 个 open、4 个 uncertain。这五项不是五个完整业务判断的验收结果。旧终态集合相等规则本身仍是独立评审配置的合同，不能冒充维护者已审批的业务规范。

本轮正式导航发现 `e889ad8ba3543e2359bed2a9` 和原子发现 `480f1137cb02e8b96438b1b1` 均为 uncertain。各自所有嵌套 snapshot 引用、来源／政策哈希与正式快照一致，没有混入 v0.6 的开发身份。正式见证的 11 份原文、251 个去重跨度再次与目标原字节匹配；来源链、模型前提、反证与开发稿一致。导航依然 `full_functionality_proven=false`，原子依然 `interleaving_inferred=false`。

## 五项完整判断的独立判读

按 [GOAL_ACCEPTANCE](GOAL_ACCEPTANCE.md) 的 5 项判断、30 项必要义务审查正式结果，目前五项均只能支持局部义务，尚无一项达到完整静态条件判断的验收范围。以下是评审对自动证据的范围判读，不是新增业务测试或工具自行求得的全项目完成率。

| 完整判断 | 当前自动证据实际增加／保留什么 | 仍阻止完整判断的必要缺段 |
| --- | --- | --- |
| CPB-01 重试预算接线 | producer `parsed.retries` 与 worker 新参数对象的 `maxRetries:3` 来源形式 | 参数解析返回、默认装配、normalize／复用／assignment／inbox／broker 字段运输、有效预算消费者与阶段归属未全闭合；新对象不是已证明的同对象覆盖 |
| CPB-02 superseded 分类 | 两个封闭初始化集合的成员差 | 状态生产与具体 job 投影、实际终态谓词和 recover guard、权威事件保护反证、terminal 与 recoverable 政策未串成完整自动关系 |
| CPB-03 活动键去重窗口 | 实际预查／写入结构、目录保护区间、进程 fence 范围、有限谓词及 key 字段结构差 | 默认动态 deps、队列集合 heap／物理资源身份、状态转换执行前提和可达交错未闭合；不能认定完整竞态已检出 |
| WWC-01 看板创建上下文 | 查询构造、同源 ambient 投影、null 传播、async 拒绝及五段有限端口装配；已有 delivery 的反证 | href receiver／可见入口、实际路由 dispatch 和事件接线仍未全自动认证，公开 VM 及其它端口效果保留缺口；环境条件不能代替这些未实现关系 |
| WWC-02 Device 编辑规格 | 封闭 spec 返回对象缺字段，Device guard 来源与本地分支反证位置 | 真实 UI／client 装配、命令对象运输、TS→JSON→Rust 字段／缺省映射、authority 和 Device 条件消费未全闭合 |

已逐项复核 [goal-ledger.json](goal-ledger.json)：5 项完整判断全部为 partial；30 项必要义务中，只有 A4（有限保护区间）、N2（参数／返回链）、N3（查询抽象）、D1（对象生产构造）在声明范围内支持，另 19 项部分支持、7 项未知。这是 4 个限定子义务，不能写成“完成 4 项业务判断”。

账本明确使用 `manual_review_of_saved_automatic_evidence`，`automatic_obligation_solver_used=false`。本次独立核对其 246 个递归证据引用、63 个去重 JSON pointer，引用的正式 artifact SHA-256 和指针均匹配；合同与冻结基准身份也一致。开发观察、人工源码锚点没有作为正式自动结果替代这些证据。

原 26 项的 `evidence_only` 分类保持历史身份，不表示这些目标永远不能被静态支持；后续只有闭合实际必要关系，才可在独立目标账本中升级完整判断。下一轮应沿账本缺段推进，并复用版本化来源、内建环境、有限值及 completion 摘要；不靠增加调用样本或重新定义分母达标。

## 本次复核的实际限制

本轮复核对象是新增实现、冻结回归项和正式选定证据，未重新逐行审查两个仓库全部源码。没有运行边界用例、测试套件、目标程序、浏览器或安装包；源码审读不等于证明所有拒绝分支无缺陷。冷／热发布成功不能外推到所有增删改名、并发扫描或故障恢复场景。标准宿主、Rust 显式接口和目录锁协议模型的运行真实性未验证，所有对应前提及未解析／排除范围继续保留。
