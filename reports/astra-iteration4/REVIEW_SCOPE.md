# Astra 独立复核范围：第四轮静态语义链能力

本轮的必要进展是从若干独立字段事实走向可追溯的来源、守卫和保护范围关系。不能只增加调用样本、把人工填写的角色串起来，或将尚未实现的分析放入“假设”后宣布完整业务结论成立。

目标源码仍为 CodePatchBay `4f2d2eca31d90b0122db1c1429dd365672db2393` 和 WinWinCode `da407e4f3df3719718b23bd8913b73fe3ff73857`。两库只读，不执行、导入、构建、测试目标，不运行测试套件。允许根代理使用受信分析器读取源码并生成静态产物；本审查只读实现、配置、原文及保存结果，不修改核心。

[原 26 项基准](../astra-baseline/capability-baseline.json)及五项人工判断冻结。v0.6 的 10 项正向重现、3 项必须未知、13 项仅证据及额外三条有限事实是对照基线，不是本轮完整目标已达成的依据。最终以独立的 v0.7 快照、模型身份和证据填写 `INDEPENDENT_REVIEW.md`。

## 1. 统一证据协议

每条推导要区分四种来源，不能仅用一个 confidence 或 uncertain 标记混合：

| 来源 | 本轮允许的含义 | 不能替代的内容 |
| --- | --- | --- |
| `source_derived` | 依据保存原文、AST 和声明身份自动抽取或推导，带原位置、规则步骤和前提。 | 执行见证、编译器检查、分支必然发生。 |
| `trusted_model` | 显式注册、版本化的标准接口或保护协议语义，如 URLSearchParams 或目录 owner lock。 | 实际工具链、浏览器／文件系统行为已验证。 |
| `policy_declared` | 人声明业务义务、资源角色、候选实现或环境适用条件。 | 源码已经证明被注入的实现、所有路径使用该资源。 |
| `unresolved` | 绑定、来源、分支或语义不在当前有限模型中闭合。 | 确定不存在、已覆盖，或通过添加假设绕过分析缺口。 |

合法的条件结论可以保留“默认生产装配、用户从此入口提交、期间 URL 未改变”等明确环境条件；不能以“假设所有未分析中间步骤均正确连接”冒充完整自动静态分析。派生事实、外部条件、反证和未解决义务要能分别查询。某个子链缺口不应抹掉其它已确认事实，也不能被该事实掩盖。

规则配置可选择入口、消费者、候选保护协议和业务义务；不能预填要发现的 URL key 集合、完整返回链、集合差、保护区结论或 A/B 并发交错。配置提供候选拓扑时，报告应称“配置候选经 AST 核对”，不能称工具独立发现了全部架构意图。

## 2. 共享 `semantic_sources` 的门槛

共享层应提供安全、稳定的源选择和原图绑定证据，不成为绕开前端未知的第二个不透明分析器。

1. 只消费当前不可变 snapshot 中捕获的实现源码。辅助原文可以支持来源说明，不能伪造 parsed SourceFile、Node、caller 或实现调用边。
2. 保留原字节／解码文本身份、snapshot 前端／parser 身份、本次语义 parser／collector 身份和派生 CST provenance。只允许受信、受限、等宽并保持原位置的语法投影；不能忽略未知 ERROR 或用新解析成功改写旧快照事实。
3. 字符串、属性和 quote 从原 buffer 读取，不从替换过的 CST token 文本推业务值。BOM 等解码差异必须有可核对字节哈希依据。
4. 选择器使用文件、精确词法 symbol 和声明位置；重复、遮蔽、失效、解析失败分别未知。callee 名字或配置指定实现不能代替已有唯一静态绑定。
5. 复用纯 CST collector 时只建临时索引，不修改 snapshot 的 files、status、metadata、节点或边；collector 身份与当前图 owner 不一致时拒绝拼接。
6. 图边核对包括精确 owner、实际调用位置、两端存在与来源解析状态、重复／cfg／opaque 限制。语义证据明确 `column_base` 和 UTF-8 单位，避免旧合同的 1-based 列与图边的 0-based 列串用。
7. 递归、摘要缓存、预算和失败路径必须显式未知。上下文摘要身份至少区分源文件／函数、抽象实参和模型版本，不能把某一次 literal seed 的结论缓存成 helper 的全局语义。

首版复用旧检测器或前端的私有纯 AST 结构可作为兼容适配，但需要记录依赖；lazy import 只延迟循环依赖，不能替代长期公共数据协议。没有必要为解耦而在本轮复制另一套作用域规则。

## 3. WWC 导航：需要自动推导的链

真实材料见 [上一轮导航账本](../astra-iteration3/NAVIGATION_EVIDENCE.md)。目标不是单独查到字符串 `delivery`，而是以下关系各有来源并可组合：

1. 看板新任务链接的实际赋值使用 literal `/home/new-task`；沿唯一保存绑定进入 `surfaceHash`，将实参与形参映射到 `scopeHash`。
2. 自动解释已支持的字符串切片、条件、template、URLSearchParams 构造与循环更新，从实际 `SCOPE_PARAMETER_NAMES` 声明获取写入键。键集合不得在 policy 中提供。
3. 根据原 return 表达式推导此输入输出 URL 的 query key 状态。helper 的摘要仍保留任意 seed 原有 query，不能泛化为“scopeHash 删除 delivery”。
4. 将输出导航值与生产 callback 读取的 `browser.location.hash` 关联时，明确浏览器导航生效、当前 URL 稳定及默认生产入口等环境条件；这不是已发生的 DOM／浏览器事件。
5. 在 callback 中定位 `routeParameters(...).get('delivery')`、赋给具体 `deliveryId` 声明，并计算缺键对应 null、足以满足 `context === null || deliveryId === null`，导出该分支 `return null`。不必也不能宣称 context 已知。
6. 精确关联 application 的 factory 实参对象中 `async deliveryContext`，与 factory 形参 `options`、返回对象 `create` 方法捕获该形参及 `options.deliveryContext()` 调用。此特定调用上下文的关系不能全局改写所有 factory 使用者的 CALLS。
7. 由同一个 callback 返回值赋给 consumer 的 `context` 声明，推导 `context === null` 的 throw 分支；如果声称该 `create` 是返回端口的方法，`Object.freeze` 的返回保持语义也需显式可信接口模型。

### Query 抽象域的正确性

在封闭域内应维持 `guaranteed_keys ⊆ actual_keys ⊆ possible_keys`。只有 possible 集合封闭时，某键不在 possible 才能证明缺失；unknown seed、动态 set/delete、对象逃逸、未支持方法或返回分支不能静默省略。

- 分支合流对 guaranteed 取交、possible 取并；未知条件保留两侧，常量条件要有有限解释依据。
- 摘要字符串和精确空字符串必须是不同状态；分支合流不能以空的片段列表表示未知内容，再在 query 初始化或真值判断中误当空值。hash 与原始 query 文本的域转换也要保留来源语义。
- 动态 delete 可能移除任意 guaranteed key；动态 set 可能引入任意 key。循环的静态键域必须来自真实绑定，未知迭代不能按空循环处理。
- 固定 `set(k, value)` 提供该键的存在，但值、重复项、percent decoding、空值与 fragment 语义受显式模型范围限制。URLSearchParams.get 对存在的空值返回空字符串，不是 null。
- 内置模型核对可见名字遮蔽、别名和写入；不能凭 `URLSearchParams`／`Object.freeze`／`get` 拼写认证任意用户对象。标准接口本身未被运行替换是模型假设，不冒充实际观察。
- 此真实入口的 selection 值不全已知时，四个 Scope key 可能存在，不必全部必然存在。仍可在键域封闭时证明 delivery 不会由这些更新凭空增加。

反证必须保留：seed URL 已带 delivery 时 scopeHash 保留它；默认生产组合以外有 fake 端口；Chat 先创建 delivery 是另一条有效链；URL 在 callback 前变化或其它前置校验阻止提交时，完整用户后果不同。未知不能被这些反证抹成成功，反证也不能被主结论省略。

## 4. CPB 去重：保护范围与谓词差

真实材料见 [上一轮原子边界账本](../astra-iteration3/ATOMICITY_EVIDENCE.md)。本轮要比“外层有 read、内层有 push”更进一步，但不需要假装实现并发调度器。

### 可自动核对的义务

- 定位 facade 中 read、select、早退、write 的实际源码与 guard；关联同一资源实参的声明身份。默认 dependency assembly 与可注入 override 分开；配置填写实现 selector 仍不等于动态 deps 已被源码唯一绑定。
- 验证 writer 到 mutation wrapper、再到 lock wrapper 的实际调用、参数／callback 转发和声明身份。配置中的 wrapper 列表不能直接充当已验证调用链。
- 从 writer callback 提取 fresh queue 上的 find predicate、复用早退和 insert；从外层 selector 提取同 key／非终态条件。terminal 初始化成员、pending 比较、包含 description 的 key 构造都来自 AST。
- 根据有限布尔／集合摘要计算可支持的谓词差。文本不同不等于逻辑不同；若 helper、转换或字段来源未闭合，应记录结构事实及未知，不能直接宣称状态集合包含或排除关系。
- 从真实 transition 调用提取状态 patch 与 expected guard，并与差异状态关联；状态写入存在不代表调度一定成功或可插入某个交错。

### 保护区域模型

目录 owner lock 的生命周期跨越 fresh read、`await callback`、save 和 release。process fence 只分别围绕取得／释放目录锁，其短回调不是整个 mutation 区域。`await` 不等于释放保护。

版本化协议可以声明 acquire 返回值与持有状态、release 与资源之间的语义；AST 必须核对该 guard 位于 callback 之前、失败路径不继续、资源与 callback 转发一致、正常及异常路径的释放位置。若 guard 不支配目标、提前 release、资源被重新赋值、多个不明释放或 alias 不闭合，则派生 `protected_region` 必须未知。不能把这些分析失败移到 applicability 后仍宣布保护关系已证。

异步完成链也是保护关系的一部分：wrapper 仅调用 callback 却丢弃它的 Promise，不能视为外层 await 等待了全部写入。必须核对 callback 的直接返回或 await，以及取得包装器最终返回值确实源于取得回调。只比较调用文本位置不足以证明这些关系。

外层 read-select 与内层 writer 的区域差、谓词差可成为自动静态条件风险的组成证据。跨函数资源身份、默认依赖实现、锁协议假设、其它写者／外层统一约束及调度可达性要分别显示；不能用全仓 rg 没找到就排除额外保障。

首版明确 `interleaving_inferred=false`，不预填 A/B 时间线。反证包括顺序同 key 复用、同 description 且仍 pending 的锁内复用、leader／CAS／容量 guard 阻止转换、失败回滚或持久化失败。结果不能称为“无锁”“已发生重复”或“任何两个同键请求必然重复”。

## 5. 本轮验收与优先级

交付前必须核对：

1. 原 26 项和五项人工判断未改；新语义链另表列出子义务、来源类型、模型、反证、缺口与整体闭合状态。
2. 至少产生实际跨函数／callback 的关系推导，或诚实说明具体哪一段仍未知。定位全部配置角色不算完整链通过。
3. 原始位置、文件哈希、parser／projection、工具／检测器／模型／政策和快照身份一致；失败结果与预算缺口不被缓存成成功或写回旧版本。
4. 正式两个真实仓库的结果采用冻结核心的新进程和新快照，未知及不相关语言缺口继续可见。冷热复用与完整目标接受度使用不同分母。
5. 不运行目标或测试套件；本次未操作验证的故障、变更失效、浏览器和运行行为在最终报告列明。

功能正确首先取决于推导链不造假，其次是共享摘要／模型协议能用于其它源码。性能不作为本轮扩围理由；摘要预算可限制输出，但不得截断后宣称完整。若某一链无法闭合，明确剩余义务比把所有 finding 改称 conditional 更接近用户真正目标。

## 6. 实现审读补充门槛

声明身份和对象根身份不能互换。`operation.member()` 的根可以与形参 `operation` 相同，但这不是调用该形参函数；`return existing.child` 也不是返回 `existing`。回调转发、返回值、复用 guard 和循环元素需要逐项核对完整 AST 形状及实际 binder，再使用声明身份连接。

形参默认表达式属于函数进入前的源码效果。第三个默认解构参数不能使前两个简单形参的声明身份整体丢失，但默认 RHS 对这些形参的写入也不能因处于 body 之外而被稳定性检查过滤。声明身份成立不等于实际实参值仍保留。

导航抽象解释必须保留短路与分支效果：`||` / `&&` 不能提前执行被短路的右侧，ternary 的未知分支必须合并 receiver 状态。首版可以拒绝跨 helper／closure 传递 URLSearchParams 对象，不能重算外层 initializer 创建另一个对象后继续作确定缺键判断。

guard 事件出现不等于逻辑蕴含。确认缺键→null→throw 时，至少需要对应 lookup 和 factory 上下文身份、该 guard 的已推导真值、所选分支的实际返回覆盖，以及 callback／consumer 的正常返回覆盖。factory formal 的直接或嵌套逃逸、转义名字和默认参数未闭合时应停止此映射，而不是假定 callback 未变。

同样，consumer 中任何常量 query 的缺键都不能与 producer 的缺键自动拼接。需要传播受限 query 投影关系：真实 ambient 输入、同输入的 query-tail 切片／无 query 空分支、constructor seed、receiver 和当前 callback 上下文。普通控制依赖、相同键域或同一个 helper 调用位置不足以替代这个值来源关系；同位置的不同调用上下文也不能共用一个未限定的 lookup 身份。

开发阶段保存源观察与正式扫描必须分开。`PORT_WIRING_OBSERVATIONS.json` 等可以证明当前分析器对某份既有快照输出了这些有限事实，不能代替新版本完整快照发布、冷热复用、冻结基准比较和最终目标账本。拒绝分支仅读实现而未操作验证的，应明确如此报告。
