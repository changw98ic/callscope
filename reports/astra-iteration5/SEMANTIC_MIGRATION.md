# v0.8 导航与端口装配的共享语义迁移

本稿记录纯静态实现迁移和保存源观察，不是目标执行或测试结果。没有执行目标、导入目标、构建、浏览器或工具测试；原 26 项冻结基线没有改写。

## 实际迁移点

| 消费者 | 移除的重复判断 | 公共协议的实际消费 | 保留的消费者约束 |
| --- | --- | --- | --- |
| navigation_analysis | 内建名字、别名、可见写入/逃逸审计 | BuiltinEnvironment(document).audit(name, at, member) 的 supported 与完整 audit 证据 | 规则仍显式注册 URL/String/Object 语义模型；unsupported 不启用模型，保留 gap |
| port_wiring | 独立内建/global 审计 | 同一个 BuiltinEnvironment 协议，保留原 standard-name fact，并附审计来源/范围 | 普通数据对象缺字段、const 声明、receiver escape 与 freeze 字段约束仍由装配层核对 |
| navigation_analysis | 独立 ordinary/async/generator/await 检查 | function_kind 用于 helper、factory、callback、returned method；completion_relation 用于 callback 的真实 await | 同步 helper 才解释源返回值；异步 callback 同时要求直接 await 与有限正常消费关系，不把 returned Promise 当 fulfilled value |
| port_wiring | generator/own-yield/async 判断 | function_kind 用于所选 owner、工厂/VM 与返回方法；completion_relation 用于 Promise.all namespace 的 await 解构 | 未等待的 async 工厂不当对象；generator 不当普通 body；普通/async boot 参数身份可记录；普通 async create 保留 |

导航标准环境事件的 operation 与端口标准名称事实的 operation 保留；公共审计数据实际进入它们。没有保留一份私有全套内建审计算法，也没有仅导入 unused 组件。参数/返回来源、query domain、specific callback 注入、null guard、真实工厂 callsite 认证、旧动态 CALLS 和 route/event/public-object gaps 不由公共 supported 值覆盖。

navigation VERSION 为 `static-navigation-contracts-2-shared`；port VERSION 为 `finite-port-wiring-2-shared`。输入 policy schema 仍为 v1。共享函数种类将同步函数的 invocation result 标为任意值/抛出，不能仅因 sync 就假定返回非 Promise；消费者仍须检查实际源返回形状。

另修正导航诊断兼容性：旧代码借用的 static_contracts._issue 不接受部分诊断分支传入的 details；改用 SemanticSources 的相同基本字段、支持 details 的 _issue，避免 unknown 分支因格式适配失败退出。

按 root 额外授权，界面只新增 `static_parameter_field_flow` 中文标签“参数字段传递待核对”。已有 uncertain/颜色语义保留，没有运行浏览器。

## 已发布 v7 的迁移前来源

[NAVIGATION_MIGRATION_BASELINE.json](/workspace/callscope/reports/astra-iteration5/NAVIGATION_MIGRATION_BASELINE.json) 直接读取正式保存 v7 finding，snapshot 为 `10bcd33b59b4eb76f67eaabf825782cb3434d8a9c6909c106036a4c82db13b3e`。

当时有限必要条件链 source_fact_confirmed=true、缺失 query key 为 delivery；trace 82 项、8 个节点、4 条边、10 项缺口。端口五段有限装配闭合，23 条 source facts。finding 为 uncertain，整体功能未被证明。这些数字仅描述该来源报告的规模，不是测试数、通过率或成功指标分母。

## 第一轮公共协议开发观察

[NAVIGATION_SHARED_PROTOCOL_INITIAL_OBSERVATIONS.json](/workspace/callscope/reports/astra-iteration5/NAVIGATION_SHARED_PROTOCOL_INITIAL_OBSERVATIONS.json) 在同一保存 v7 源和图上重新运行工具的静态模型，记录 consumer 版本、观察前后工具源码哈希以及 published=false。此时共享 Environment 仍在收紧审计，不冒称正式/冻结扫描。

第一次观察使用 Environment 哈希 `88c556cd09864c782e986d3f21a34cd13416188798eb503ba59665dcb65208b2`，前后源码稳定，但公共审计增加了实际阻断：

- application.ts :193 的 `options.window ?? window` 主宿主别名，影响 String 与 URLSearchParams 模型。
- 同文件 :1107/:1132 的 primitive undefined 普通值返回；从保存源 AST 补查，两者的 parent 均为 `() => undefined`，grandparent 为 pair。

消费者遵守 supported=false，没有特殊放行，因此生产 query domain 仍闭合（四个 possible Scope 键、无 guaranteed 键），消费端 null 条件来源链暂未闭合，端口装配也保留 unknown。未闭合后模型展开更多不确定分支，trace 变为 120、gaps 变为 54，端口仅留下前置四条事实。这是审计范围/支持形状变化引发的来源差异，不能将数字增加解释成更多异常检出。

精确阻断已发公共 owner 与 Astra，随后由公共模块 owner 修正别名/primitive profile 并接受独立审查。修正依据通用 AST 和明确模型边界，没有在消费者为恢复旧计数覆盖 unknown，也没有增加项目路径/业务字段硬编码。

## 已被替代的环境依赖候选

曾使用 Environment `be115185a54c441170424565b2872ddef7abe0e406d8df5a1fa9b840030a03c8` 的观察保存在 [NAVIGATION_SHARED_PROTOCOL_ENV_BE115_SUPERSEDED.json](/workspace/callscope/reports/astra-iteration5/NAVIGATION_SHARED_PROTOCOL_ENV_BE115_SUPERSEDED.json)，artifact SHA-256 为 `69b1a9c8d5ed8f46e6a78c4135925194de5895c507cffe37670184be3b25fc8a`；其当时对照另存 `NAVIGATION_MIGRATION_COMPARISON_ENV_BE115_SUPERSEDED.json`。它保留必要来源关系，但依赖身份已经被替代，不能作为最新固定组件观察。

root 为真实字段消费者三文件要求公共登记允许 `Object.assign` 的静态接口出现；Astra 同意窄扩并复核新 Environment 哈希 `39e388c78584e176640109c869b3c3fe58819619e82bb29a570d9de1381d9566`。登记不证明 purity、参数效果或字段复制；API/prototype 目标参数、显式写入、别名、eval/computed/逃逸屏障仍保留。导航和端口自己的源码未修改。环境 VERSION 仍为未发布阶段的 `captured-builtin-environment-1`，精确身份由以下 SHA 区分。

## 最新同源观察与冻结

[NAVIGATION_SHARED_PROTOCOL_OBSERVATIONS.json](/workspace/callscope/reports/astra-iteration5/NAVIGATION_SHARED_PROTOCOL_OBSERVATIONS.json) 用新固定 Environment `39e388…` 与其它固定公共依赖重新分析同一真实保存 v7 源和图；它仍为开发对照观察，`published=false`，不是新正式快照。观察前后六个组件源码哈希一致，两个消费者保持原冻结源码。正式新扫描由 root 后续生成。

[NAVIGATION_MIGRATION_COMPARISON.json](/workspace/callscope/reports/astra-iteration5/NAVIGATION_MIGRATION_COMPARISON.json) 比对原始快照身份、源码哈希、policy、节点/边身份、具体工厂 callsite 与 callback、null/throw guard、反例 query domain，以及带原始位置的 trace/port fact 关系；还单列被替代 be115 观察与最新依赖观察的来源关系对照。实际必要来源关系保留：

- 看板 literal 新建路由的 query domain 封闭，Scope 四键仅为 possible，guaranteed 为空；消费端要求 delivery，该生产表达式没有 delivery。
- 真实既有 query 的 `homeDecisionHash` 反例仍保证 delivery；没有把所有导航或 scopeHash 一律判为丢字段。
- 特定注入 callback 与真实工厂 context 身份相同；lookup→null return→直接 await 正常结果消费→async create 的拒绝 Promise 分支均保留。公共 completion 同时记录 `direct_await=true` 与 `normal_value_relation_closed=true`，但执行激活、全路径完成、runtime_verified 均为 false。
- 五段有限端口装配闭合：boot、production 端口选择、实际 injection、VM 对象、submit 的实际端口使用；`navigation_context_identity_matched=true`，`end_to_end_complete=false`。
- 10 项原缺口的代码与顺序保留，包括 route/event、hash 读取时序、公开 VM 可变、其它 describe 方法 effect、原 snapshot dynamic CALLS，以及未建模的对象/前缀效果。finding 仍为 uncertain。

最终观察实际仍有 82 项 trace、8 个节点、4 条边、23 条 port source facts；这些数量没有成为判断依据。源码关系逐项对照保留，公共 audit、函数 kind 与 await-completion 元数据替换了原重复实现。公共 Environment 的认证范围为单个 `authenticated_document`，可见别名/修改审计与固定宿主前提、跨文档/opaque effects 分栏；supported 不意味着运行时 provider 已认证。第一版未闭合记录另存，不用最终结果覆盖它。

Astra 对固定源码和最终观察独立末读后允许两消费者冻结。没有目标执行、测试、构建或浏览器验证；本轮消费者仅做 AST 语法核对，界面标签仅做 `node --check`。

| 冻结组件 | VERSION | SHA-256 |
| --- | --- | --- |
| navigation_analysis.py | static-navigation-contracts-2-shared | 5e4b23130ce301c23937f504b71a39a54ebcb064d84a0f5c4ed77928201e70be |
| port_wiring.py | finite-port-wiring-2-shared | 388d9968a7511106b379545bbea86cb69a60e9d38c2354905f940e250fb75a47 |
| semantic_environment.py | captured-builtin-environment-1 | 39e388c78584e176640109c869b3c3fe58819619e82bb29a570d9de1381d9566 |
| completion_summaries.py | captured-completion-summaries-1 | 35dd3124f2bd6a33156d9e48a716172f11fff79ec90d1e0340166dc34510c77e |
| lexical_bindings.py | captured-lexical-bindings-2 | c2820fd2d08be101bd8b51cc996fce69b0c2c2beffea94a1498b6b011fb75672 |
| semantic_sources.py | semantic-snapshot-sources-1 | dab9108e47787b451665563bc08aab62e906eb0e02d3f77c2f70182bf00f5381 |

最新观察 artifact SHA-256：`7bec3b7f351e86da56099436cc260cd47d295b89ff25a2a581d8b9a49b652c4e`。
