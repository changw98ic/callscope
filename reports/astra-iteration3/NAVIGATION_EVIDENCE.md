# WWC 导航与闭包上下文：第三轮原始来源与实现范围

日期：2026-10-12。只读目录：/workspace/winwincode。

本稿是来源整理及下一项静态合同建议，不是已集成的检测器或运行报告。没有导入目标、执行目标、测试、构建或浏览器验证；没有修改核心、目标仓库或 UI。合同意图来自 Astra 独立观察，尚未获得目标项目作者审批。

## 1. 结论的正确粒度

可以从已读源码确认：看板入口给 URL 构造器的种子是无查询部分的字面路径；构造链只写四个 Scope 查询键；真实任务端口的注入闭包读另一个必需键 delivery，缺键返回 null，而真实 create 方法拒绝这个 null。

不能把它简化为“scopeSelection 没有 delivery 同名字段所以任务必失败”。实际发生了查询键 delivery → 局部值 deliveryId → 闭包返回的 context.deliveryId 的映射；这些名字并不相同。需要参数、返回值、闭包注入、读取和守卫的来源链。

同样不能说 scopeHash 丢掉了已有 delivery。scopeHash 保留输入 hash 中原有的实体查询参数；本样本缺口来自特定导航调用先新建了一个没有实体查询参数的种子。

## 2. 可定位的有限来源事实

| 编号 | 源码事实与定位 | 确定范围 |
| --- | --- | --- |
| N01 | mountHomeDashboardPage 在 [home-dashboard-page.ts:360](/workspace/winwincode/apps/client/src/home-dashboard-page.ts:360) 把 surfaceHash('/home/new-task', options.scopeSelection) 赋给 newTask.href；该调用的第一个实参是字符串字面量，无问号或查询种子。 | AST 调用实参与赋值事实。并未观测用户点击。 |
| N02 | 该函数在 [home-dashboard-page.ts:11](/workspace/winwincode/apps/client/src/home-dashboard-page.ts:11) 显式从 @winwincode/browser-core/scope-context 导入 surfaceHash；[home-dashboard-page.ts:368](/workspace/winwincode/apps/client/src/home-dashboard-page.ts:368) 将 newTask 放入实际 topActions。 | 模块导入与 DOM 组合来源。包解析及 DOM 导航语义需有模型依据，不能用全局同名匹配替代。 |
| N03 | [scope-context.ts:271](/workspace/winwincode/packages/browser-core/src/scope-context.ts:271) 的 surfaceHash 仅为 path 加 '#' 前缀，然后把该表达式及 selection 传给 scopeHash，并返回其结果。 | 参数绑定、模板构造和返回来源。 |
| N04 | [scope-context.ts:197](/workspace/winwincode/packages/browser-core/src/scope-context.ts:197) 的 scopeHash 从输入 hash 截取已有 query 初始化 URLSearchParams；[scope-context.ts:204](/workspace/winwincode/packages/browser-core/src/scope-context.ts:204) 仅循环 SCOPE_PARAMETER_NAMES，按 selection[name] 执行 delete 或 set，最后序列化。 | 有限查询键变换。在明确的标准 URLSearchParams API 模型中，输入已有键保留，新增键来自这个数组。 |
| N05 | [scope-context.ts:12](/workspace/winwincode/packages/browser-core/src/scope-context.ts:12) 的数组仅有 organizationId、workspaceId、projectId、repositoryId；scopeSelectionFromHash 的封闭对象也只构造四个字段：[scope-context.ts:184](/workspace/winwincode/packages/browser-core/src/scope-context.ts:184)。 | 声明数组及对象构造事实。不能据接口类型本身断言运行时对象没有其他属性；本例关键是 setter 循环的键来源。 |
| N06 | renderHome 把 scopeSelectionFromHash(browser.location.hash) 作为 mountMyWorkPage 的 scopeSelection：[application.ts:1259](/workspace/winwincode/apps/client/src/application.ts:1259)。mountMyWorkPage 再把该属性传给实际 mountHomeDashboardPage：[my-work-page.ts:137](/workspace/winwincode/apps/client/src/my-work-page.ts:137)。 | 对象实参属性传递。scopeSelectionFromHash 不携带实体查询键，因此调用路径也没有额外的 query 种子。 |
| N07 | application 在 [application.ts:277](/workspace/winwincode/apps/client/src/application.ts:277) 根据 options.taskSeed === undefined 选择真实 createControlPlaneTaskPort 或 fake factory。正常 [boot.ts:23](/workspace/winwincode/apps/client/src/boot.ts:23) 调用只构造 root/serverUrl 两个选项，没有 taskSeed。 | 源码组合条件。宿主若注入其他选项就不能套用“正常 boot”结论。 |
| N08 | 传入真实 factory 的对象在 [application.ts:285](/workspace/winwincode/apps/client/src/application.ts:285) 定义 async deliveryContext；它读取 routeParameters(browser.location.hash).get('delivery')，且 context === null 或 deliveryId === null 时返回 null。 | 显式回调构造、捕获 browser、查询读取与 null 分支。不是直接参数流：读取的是提交时的 ambient location.hash。 |
| N09 | [application.ts:175](/workspace/winwincode/apps/client/src/application.ts:175) 的 routeParameters 取当前 hash 中问号之后的部分，交给 URLSearchParams。没有 query 时输入为空字符串。 | 有限字符串切片与标准 API 模型。在该模型中，缺少键的 get 返回 null。 |
| N10 | [community-control-plane-client.ts:2791](/workspace/winwincode/apps/client/src/community-control-plane-client.ts:2791) 的真实 factory 返回 create 方法；该方法首先 await options.deliveryContext()，然后 context === null 时 throw。HTTP 创建命令在 [community-control-plane-client.ts:2813](/workspace/winwincode/apps/client/src/community-control-plane-client.ts:2813)，位于这个守卫之后。 | callback 属性调用、返回来源、null 守卫与语法先后关系。不能把“callback 存在”当成任意对象方法都解析成功。 |
| N11 | renderTaskEntry 把 taskPort 注入 TaskEntryViewModel：[application.ts:1319](/workspace/winwincode/apps/client/src/application.ts:1319)。表单有效时在 [task-entry-view-model.ts:311](/workspace/winwincode/apps/client/src/task-entry-view-model.ts:311) 构造五字段输入，随后 port.create(input)；输入没有交付创建或交付选择步骤。 | 真实端口注入及调用点。还必须满足设备、仓库、描述和模型选择等表单前置条件，才能到达此调用。 |
| N12 | homeSubRoute 将 /home/new-task 映射为 task-entry：[application.ts:1272](/workspace/winwincode/apps/client/src/application.ts:1272)；Home 分发确实调用 renderTaskEntry：[application.ts:1907](/workspace/winwincode/apps/client/src/application.ts:1907)。performRender 会关闭旧特性并重新挂载：[application.ts:1782](/workspace/winwincode/apps/client/src/application.ts:1782)。 | 路由分发与特性生命周期。导航、事件时序和全局状态稳定性仍是组合适用条件。 |

N01 与 N03/N04/N05 在有限标准 API 模型下可给出这个来源事实：

    seed 的已知 query keys：{}
    构造链可能新增的 keys：
      {organizationId, workspaceId, projectId, repositoryId}
    required key：delivery
    在上述闭合构造模型中，delivery 不在输出可能键集合中。

Scope 值可能为 null，delete 分支意味着这四个键不一定全部出现；因此只能把它们记为 possible keys，不能误标为 guaranteed present。未知 Scope 值不会通过标准 URLSearchParams.set 注入另一个查询键，因为该 API 对值进行编码。若分析器不知道 receiver 的绑定或 API 行为，这一点就必须降为 unknown。

## 3. 参数、返回与 closure 来源图应如何表达

下面是源码关系示意，不是工具已经提取出的端到端 resolved 执行图：

    literal '/home/new-task'
      → call argument #0 of imported surfaceHash
      → parameter path
      → prefixed hash expression
      → call argument #0 of scopeHash
      → URLSearchParams seed + finite-key mutation summary
      → serialized return
      → assignment newTask.href

    normal boot option object
      → taskSeed-undefined factory branch
      → object argument's deliveryContext method
      → injected options.deliveryContext callback
      → returned taskPort.create method
      → callback invocation and null guard

    assumed navigation effect / unchanged destination hash
      → captured browser.location.hash read
      → routeParameters result
      → get('delivery')
      → local deliveryId
      → null return or context.deliveryId construction

第一组大多是参数/返回/赋值的静态来源；第二组涉及工厂返回对象与回调注入；第三组包含 ambient 状态和宿主平台边界。不能因为图上存在箭头，就把第三组自动升级成参数值从 href 精确流进了某次 callback。

建议的通用来源节点：literal、call_argument、formal_parameter、return_expression、object_property、injected_callback、captured_read、query_key_lookup、null_guard。身份应至少包含 captured file hash、词法 owner、AST site/property path、原始 span；匿名对象方法不应仅取全局同名 create 或 deliveryContext。

建议的边：ARG_BINDS、RETURNS_VALUE、ASSIGNS_TO、PASSES_PROPERTY、BINDS_CALLBACK、CAPTURES_VALUE、LOOKS_UP_KEY、GUARDS_NULL。每条边分别记录 AST-proven / modeled-assumption / unknown，不把参数边、平台导航边、闭包执行时序合成一个笼统 resolved 标记。

## 4. 反证与适用前提

### 已含有效 delivery 的 URL

scopeHash 的 [scope-context.ts:203](/workspace/winwincode/packages/browser-core/src/scope-context.ts:203) 用输入已有 query 初始化 parameters；只改四个 Scope 键，所以已有 delivery 会被保留。读入有效 delivery 的路径可绕过“缺键导致 null”的那个条件。

这不是“有效 URL 就保证任务成功”：认证、交付存在、required criterion、设备与后端结果等仍有独立前置条件，参见 [application.ts:286](/workspace/winwincode/apps/client/src/application.ts:286)、[application.ts:296](/workspace/winwincode/apps/client/src/application.ts:296)。反证只限定本条缺失键观察的范围。

### taskSeed 与 fake task port

[application.ts:307](/workspace/winwincode/apps/client/src/application.ts:307) 的替代分支创建 createControlPlaneTaskFake。其 create 在 [community-control-plane-client.ts:2883](/workspace/winwincode/apps/client/src/community-control-plane-client.ts:2883) 直接根据 input 构造/保存 anchor，不调用真实 deliveryContext，因此不能拿 fake 的创建成功作为真实端口已满足交付前置条件的证明。

也不能说 fake 让整个 UI 工作流完成：onStarted 在 [application.ts:1332](/workspace/winwincode/apps/client/src/application.ts:1332) 只在当前 URL 已有 delivery 时才将它写入下一跳；任务运行路由仍要求 task/delivery 两个锚点。这里没有运行任何 fixture。

### Chat 创建是另一条真实来源链

Chat 路由显式注入 ChatDeliveryCreator：[application.ts:1023](/workspace/winwincode/apps/client/src/application.ts:1023)。creator 在 [chat-delivery-creator.ts:227](/workspace/winwincode/apps/client/src/chat-delivery-creator.ts:227) 取得新 deliveryId，构造 DeliveryCreate 请求；之后分别构造 workitems.create 与 workrun.start 的 payload，明确传入该 deliveryId：[chat-delivery-creator.ts:286](/workspace/winwincode/apps/client/src/chat-delivery-creator.ts:286)、[chat-delivery-creator.ts:302](/workspace/winwincode/apps/client/src/chat-delivery-creator.ts:302)。

这是单独的值来源和端口链，不能用看板入口的缺口推断系统没有任何创建任务能力；也不能用这条链存在反推看板入口已带正确 context。

### 必须保留的组合条件

- 通过当前看板 href 导航到该目的路由，而不是手工或其他入口携带实体参数。
- 使用 normal boot 选择的真实 task port，不使用 taskSeed/fake 或其他宿主注入。
- 到达表单提交调用，且 callback 读取前 destination hash 没有被其他代码/用户改写。
- 标准 DOM 导航、URLSearchParams 与相关内建行为处于显式静态模型内；没有证明所有运行时替换都被排除。
- 路由、工厂及 callback 的模块绑定和词法来源已唯一确认；动态 import、对象替换或逃逸未闭合时保留 unknown。

## 5. 可落地的下一项静态合同

建议新增 **navigation_query_context**，先做“已配置导航构造链没有提供已配置消费者必需查询键”的合同核对。目标是有限来源与前置条件配对，不是通用浏览器执行、全程序污点分析或功能成功预测。

第一批可实现范围：

1. AST 定位一个 href/hash 赋值的生产点，提取字面 seed 与唯一函数 binding；按调用实参位置绑定 helper 形参，跟踪直接 return、不可变局部值与有限模板前后缀。
2. 为固定受信 URLSearchParams API 定义有限抽象域：已知初始键、possible keys、guaranteed keys、unknown mutations。只有没有未知写入/逃逸时，才能用“required key 不在 possible keys”形成缺失键的负向来源事实。
3. 从 AST 本身核对 helper 的 seed 参数、字面键来源、set/delete receiver 及序列化 return。条件分支做集合 join；动态 key、外部 builder、对象 getter、spread、重复属性、构造器绑定未知、未知函数返回或 mutable alias 全部禁止缺失键负证。
4. 单独定位工厂实参对象的 callback property 与返回对象方法，建立 options.property 的注入来源，提取 callback 的 query-key read、null propagation 和调用者 throw guard。属性路径需匹配真实注入对象，不按同名方法相连。
5. href 到 browser.location.hash 的关系与“提交时仍是该 hash”保留为独立平台/时序假设。缺失来源事实可确认，应用于整个任务链的 finding 第一批仍为 conditional / uncertain。

建议规则最小数据结构（提案，尚非已发布 schema）：

    id, type = navigation_query_context
    provenance:
      authority = independent_review
      reviewer = Astra
      author_approved = false
      source_doc = 来源标签，绝不作为读取/执行入口
    producer:
      file + owner_symbol
      site = assignment
      target_property_path = [newTask, href]
      call_binding = 受信导入/唯一函数定位
      seed_argument = 0
    required_query_keys = [delivery]
    builders:
      surfaceHash 的 argument/parameter/return 来源定位
      scopeHash 的 URLSearchParams receiver 与 finite-key mutation 来源定位
      SCOPE_PARAMETER_NAMES 的字面数组 AST 定位
    consumer:
      factory file + owner_symbol
      callback_argument_index = 0
      callback_property = deliveryContext
      returned_method_property = create
      captured_read = browser.location.hash
      query_key_read = get(delivery)
      null propagation 与 caller null-guard 的 AST 来源
    applicability:
      kind = conditional
      conditions + counterexamples + 原始源码出处

builder 描述只能选择工具支持的受信抽象操作；不能允许 Python/JavaScript 代码、可执行插件、任意正则替代 AST 或配置自行声明“已证明闭合”。closure selector 应允许在唯一 lexical owner 内定位“某个 factory 调用实参对象的某属性方法”，避免 current static_contracts 仅有 file + 裸方法名时的歧义。

输出应至少区分：

- **source_fact：**seed、helper 形参/return、四个 possible query keys、required key、closed/unknown、读键/null 分支与工厂 callback 注入节点，逐项绑定原文件 hash/span。
- **contract_assumptions：**normal boot、目的路由与消费者的对应、导航 effect、读取时 URL 稳定性，以及作者尚未审批的合同意图。
- **counterexamples：**已有实体 query 被 scopeHash 保留、fake factory、Chat 新 ID 创建路径。
- **unknown：**未闭合 binding、未知 query mutation、对象逃逸/重赋值、复杂 return/control flow、无法确认的 callback 注入、平台边与时序。

只提取生产点字面路径、或仅看到消费者 get('delivery')，都不足以宣称运行失败。可确认的初期标题是“导航查询上下文合同待核对”；描述明确“构造链未提供配置键，真实 callback 的 null guard 有源码出处，适用前提未全部自动闭合”。

## 6. 解析能力与快照身份边界

本次额外用固定受信的原始 Tree-sitter TypeScript grammar 只做文本/CST 来源采集。六个相关小文件 raw grammar 无错误；application.ts 与 community-control-plane-client.ts 的 raw grammar 存在 inline import type 等语法支持缺口。

**这只说明本次 raw 采集步骤的能力边界，不是 v0.5 正式快照缺文件或目标编译失败。** Astra 已确认 v0.4 起的可信、版本化派生 CST 恢复了这些语法；后续实现应复用该既有解析通道与原始源码位置映射，不能绕过不明错误宣称闭包 binding 已解析，也不能退回 raw grammar 失败来误报正式覆盖。

目前本稿中 application / community 的来源链由原始文本人工复核补充，不冒称已由新增 navigation 检测器自动闭合。正式 finding 应来自被分析 snapshot.files，规则/抽象模型版本纳入 policy 与工具身份；不能拿本次 live 读取哈希冒充某个正式快照 ID。

## 7. 原始文件 SHA-256

以下哈希直接来自本次读取的原始字节，未改写或执行源码：

| 文件 | SHA-256 |
| --- | --- |
| apps/client/src/home-dashboard-page.ts | e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f |
| packages/browser-core/src/scope-context.ts | 333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d |
| apps/client/src/application.ts | fa99231ab15cabe394bbfaac6d7baa59313c4da44c47e5f39101d617c95aa520 |
| apps/client/src/community-control-plane-client.ts | 023a8016a6c29ab24d0d6b24fb23715d257d7e311542333d37aa9bff951e7718 |
| apps/client/src/task-entry-view-model.ts | f9cd92310022579719d608c6465c26a7b328ba27d63d0cbe0baf44d6319c5f18 |
| apps/client/src/chat-delivery-creator.ts | 7598a2537abf9474a7bbbac4a858584f6075dbe33100b4b18da41930e5aa42e8 |
| apps/client/src/my-work-page.ts | 64a44385a0b2f93fd8e1241627817b08445c57aa5833df9f8ae47cce1f174a15 |
| apps/client/src/boot.ts | eef5a73fb2a7c16027f0e54f1be59111ec5fa72edaadbed5ce6c25ae50e80e9a |

本轮交付为来源稿和实施范围建议。未新增原型，未修改已冻结检测器，也未宣称该导航合同已经支持正式扫描。
