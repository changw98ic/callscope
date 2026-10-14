# v0.7 导航上下文合同：真实来源与静态生成验证规格

日期：2026-10-12。目标：`/workspace/winwincode`，只读。

本稿提供导航检测负责人的实际 AST 源式、有限抽象语义、组合条件和反证。它不证明用户执行过该路径或整个功能失败。没有运行目标、导入目标、测试、构建或浏览器；没有修改 CallScope 核心、目标、UI 或原 26 项冻结基线。下一项合同的意图来自 Astra 独立观察，`author_approved=false`。

## 1. 本轮新增独立机读来源

- [navigation-observed-anchors.json](/workspace/callscope/reports/astra-iteration4/navigation-observed-anchors.json)：59 个选择器获得真实 AST 节点，涵盖生产点、helper、注入 callback、真实消费端、正常 boot、表单/路由接线、fake 和 Chat。这个数字表示来源采集覆盖，不能当功能检出率或正确率。
- [collect_navigation_anchors.py](/workspace/callscope/reports/astra-iteration4/collect_navigation_anchors.py)：可复查的来源采集脚本，仅读取八个目标源文件及 browser-core 的 JSON manifest。选择器指定已评审源码位置；观察到的字面量、参数、字段、条件、分支、对象方法、quotes 和 hash 都由实际 AST/原始字节生成。没有预填 helper keys、required key、query 抽象结果或 null trace。
- [NAVIGATION_EVIDENCE.md](/workspace/callscope/reports/astra-iteration3/NAVIGATION_EVIDENCE.md)：上一轮完整人工来源说明，保持原文件不变。

机读来源中的 `snapshot_id=null`：这是独立 live source 采集，不冒充正式快照。正式 finding 必须读取同一个 snapshot.files，并与自身 snapshot/policy/model/analyzer 身份绑定。原 26 项 baseline 只记录读取哈希，没有改写。采集脚本只提供来源锚点，不是新生产检测器，也不是测试程序。

八个原源码文件保持与上一轮来源稿相同的 SHA-256。application.ts 与 community-control-plane-client.ts 的 raw grammar 有 inline import type 支持缺口；调用既有 `parse_with_projection` 后均 `mode=adapted`、最终 AST 无语法错误，其余六个文件为 original。全部 quote/hash/span 以原始源码为准。不能把 raw 错误说成 v0.5/v0.6 正式快照丢文件。

## 2. 真实生产点及 builder 的源式

### 字面导航 seed

[home-dashboard-page.ts:360](/workspace/winwincode/apps/client/src/home-dashboard-page.ts:360)：

```typescript
newTask.href = surfaceHash('/home/new-task', options.scopeSelection)
```

机读锚点 `producer.dashboard-href` 是 assignment_expression：left 的成员路径为 `newTask.href`，right 为 call_expression。第 0 实参是无转义字符串字面量；其值含路由路径，没有 query seed。不能从 ScopeRouteSelection 类型的字段清单代替这个值来源结论。

[home-dashboard-page.ts:11](/workspace/winwincode/apps/client/src/home-dashboard-page.ts:11) 的 import_statement 指定 `@winwincode/browser-core/scope-context`。browser-core manifest 的 `./scope-context` 导出映射到 dist JS；将它映射为 workspace TS 源码仍要由正式解析器的唯一模块解析模型确认，不能按全局同名 surfaceHash 连接。

### 参数、模板和直接返回

[scope-context.ts:271](/workspace/winwincode/packages/browser-core/src/scope-context.ts:271)：

```typescript
export function surfaceHash(path: string, selection: ScopeRouteSelection): string {
  return scopeHash(`#${path}`, selection)
}
```

需由唯一 helper binding 将 actual arg #0 绑定到 formal `path`，再从模板的静态 `#` 前缀及 `${path}` 得出下一个 actual arg；另一个参数只影响 Scope 值。随后绑定到同文件唯一函数 scopeHash 的 formal `hash`。不能在 policy 中预填这条 helper chain 或直接写输出 `#/home/new-task` 充当解析结果。

### 真实 URLSearchParams receiver

[scope-context.ts:201](/workspace/winwincode/packages/browser-core/src/scope-context.ts:201)：

```typescript
const queryIndex = hash.indexOf('?')
const path = queryIndex < 0 ? hash : hash.slice(0, queryIndex)
const parameters = new URLSearchParams(queryIndex < 0 ? '' : hash.slice(queryIndex + 1))
for (const name of SCOPE_PARAMETER_NAMES) {
  const value = selection[name]
  if (value === null) parameters.delete(name)
  else parameters.set(name, value)
}
const query = parameters.toString()
return query.length === 0 ? path : `${path}?${query}`
```

实际 loop 的 AST 类型是 `for_in_statement`，字段 `kind=const`、`left=name`、`operator=of`、`right=SCOPE_PARAMETER_NAMES`。不能把 for-in 的另一种 `in` 语义也当成元素遍历。

`parameters` 是此词法函数内唯一 const variable_declarator 的 new_expression receiver。set/delete/toString 必须全部绑定到这个局部值；只看到同名调用文本不足以证明同一 receiver，也不足以排除别的写入、逃逸或 reassign。

`SCOPE_PARAMETER_NAMES` 在 [scope-context.ts:12](/workspace/winwincode/packages/browser-core/src/scope-context.ts:12) 的实际初始化是 `Object.freeze([...四个字符串...] as const)`。机读 JSON 的 literal_value 来自 array children；policy 不可预填预期四键来代替数组 AST。`as const` 是类型包装，不能当运行时变换。

## 3. 有限 query-key 抽象域及不应误判的反证

至少区分 `possible_keys`、`guaranteed_keys`、`unknown_keys` 和 receiver 的 closed 状态。键的“存在”不等于值有效、非空、已授权或后端实体存在。结论仅讨论正常返回的构造值，不保证 helper 总会返回。

本条 literal seed 在固定字符串/URLSearchParams 模型中先构造空 query；实际循环的每个 Scope 值未知，既可能为 null 触发 delete，也可能非 null 触发 set。分支 join 应取 possible 的并集、guaranteed 的交集：

```text
seed possible = {}
seed guaranteed = {}
loop possible = {organizationId, workspaceId, projectId, repositoryId}
loop guaranteed = {}
unknown_keys = false，仅当本地 mutation/receiver/模型都闭合
```

不能写“返回 URL 含四个 Scope 键”；本例只证明它们可能出现。在 closed 模型内，delivery 不在 possible，才可形成缺失键的来源事实。若存在未知 mutation、动态键或 receiver 绑定不明，不能忽略它们后仍给出缺失负证。

### 必须保留已有 input query

scopeHash 在 :203 用 `hash.slice(queryIndex + 1)` 初始化已有参数，它并不删除 Scope 集合之外的实体键。某个已带 delivery 的 seed，在同一个算法里必须保留这个键，不能让检测器总重建空 query。

本轮还有实际调用反证，而非虚构运行输入：[home-dashboard-page.ts:226](/workspace/winwincode/apps/client/src/home-dashboard-page.ts:226) 的 homeDecisionHash 在 attention 且 deliveryId 非 null 分支调用：

```typescript
scopeHash(`#/home/review?delivery=${encodeURIComponent(card.deliveryId)}`, scopeSelection)
```

机读锚点 `counterexample.actual-delivery-query-seed` 含这个模板实参和 enclosing ternary。它证明源码确有带实体 query 的 seed。delivery 值及消费者有效性仍有独立前提；不能据此宣称该路由功能成功，也不能将不同 review 路由当成 new-task 正向功能对照。

URLSearchParams.set 在受信标准模型内会编码值，未知值文本不能通过 `&delivery=...` 新增另一个查询键。但这必须来自已声明模型及 receiver binding，不能用目标调用执行得到，也不能在内建 binding 未确认时强用该模型。

## 4. 消费端是注入对象方法与返回对象方法

### 实际 callback 注入位置

[application.ts:277](/workspace/winwincode/apps/client/src/application.ts:277) 的 taskPort variable_declarator 有一个 ternary initializer：

```typescript
options.taskSeed === undefined
  ? createControlPlaneTaskPort({
      /* 其他端口选项 */
      async deliveryContext() {
        const context = authenticatedRouteContext()
        const deliveryId = routeParameters(browser.location.hash).get('delivery') as DeliveryId | null
        if (context === null || deliveryId === null) return null
        /* 读取 aggregate 和 criterion */
        if (criterion === undefined) return null
        return { deliveryId, expectedRevision: /* ... */, contractRevision: /* ... */, criterionId: /* ... */ }
      },
    })
  : createControlPlaneTaskFake({ /* ... */ })
```

callback 的 AST 是 **method_definition**，不是 `deliveryContext: () => ...` pair。其 enclosing call AST 明确为真实 factory 第 0 实参对象；return-null、success-return 和其他 criterion-null 分支都在该方法的词法范围内。嵌套 `.find(candidate => ...)` 的函数不得混入 callback 的 direct-return 集合。

需要从实际 `get` 字面实参推导 required key，并沿 receiver 追到 routeParameters 的返回。不能要求 query 键 `delivery` 与局部名 `deliveryId` 或 context 字段同名；实际来源就是这三种不同的身份。

[application.ts:175](/workspace/winwincode/apps/client/src/application.ts:175) 的 routeParameters 是局部唯一命名函数，直接返回 `new URLSearchParams(query < 0 ? '' : hash.slice(query + 1))`。其 query 实例与 builder 的 parameters 是两个不同 receiver，不能合并为同一对象；以相同 hash 的显式平台/时序假设联系二者。

### 真正返回给调用方的端口方法

[community-control-plane-client.ts:2775](/workspace/winwincode/apps/client/src/community-control-plane-client.ts:2775) 的 factory formal 参数是 `options`。直接 factory return 在 :2790：

```typescript
return Object.freeze({
  async create(input: ControlPlaneTaskCreateInput): Promise<ControlPlaneTaskAnchor> {
    const context = await options.deliveryContext()
    if (context === null) throw new Error('创建任务项前请选择交付。')
    /* 其他前置条件和命令构造 */
    const response = await options.client.command(command)
    /* ... */
  },
  describe(taskId: string) { /* ... */ },
})
```

正式分析必须检查 factory 的直接 return → 受信 Object.freeze 的第 0 实参 object → 唯一 create method_definition，而不是搜文件里任意名为 create 的函数。对象形状若有 spread、computed、重复属性、getter、非受信 wrapper 或复杂别名，则 callback/method 注入关系不能闭合。

create 内调用的是捕获 factory formal `options` 的 `deliveryContext` 属性；必须把它绑定到实际注入的对象方法。`:2792` 的 local `context` initializer 是 await_expression → call，`:2793` 的 guard 是 if_statement → throw_statement。`:2813` 的 command 在其后，不能仅以“guard quote存在”推出必经/支配关系。

## 5. 完整条件链需要由数据生成的证据

| 步骤 | 最低需要的生成数据 | 源码出处或能力边界 |
| --- | --- | --- |
| Seed 来源 | assignment RHS actual arg 的字面值、AST span/hash、唯一 import binding | dashboard :360；import :11 |
| 参数传递 | actual-to-formal mapping、surfaceHash template parts、直接 return、scopeHash formal binding | scope-context :271–272、:197 |
| Query 构造 | indexOf/slice 条件、实际 constructor seed、receiver ID、循环字面 array、set/delete 条件、serialize return | scope-context :201–210 |
| Query 结论 | 由初始/分支/循环抽象操作计算的 possible、guaranteed、unknown 与模型版本 | 不能从 policy 复制键集或闭合标记 |
| Callback 注入 | factory callee 解析、actual 对象属性方法 AST、参数位次、formal options、return object create 属性 | application :277–309；community :2775、:2790 |
| Key 读取 | captured hash read、routeParameters 参数/return来源、get literal key、被赋值 lexical variable ID | application :175–177、:287 |
| 空值传播 | 缺键 → get 返回 null 的标准 API 依据；deliveryId === null → OR条件为true → direct return null 的 branch trace | application :288；其他 null 分支另外列出 |
| Consumer 拒绝 | callback call → await local context → context === null → abrupt throw，及 command 之前的语句关系 | community :2792–2793、:2813 |
| Port 分支选择 | taskSeed guard 的 AST，normal boot closed options literal 不带 taskSeed，与 fake 分支来源分开 | application :277、:307；boot :23 |
| UI 入口接线 | route match、实际 dispatch、model 的 port 实参、options.port 局部绑定、submit 的调用点与前置 guards | application :1275、:1911、:1319；task-entry-view-model :89、:271–321 |
| 平台与时间边 | href 导航会对应 destination hash，提交 callback 读取时 hash 没有改动；这些是独立假设 | 不能生成 AST-proven/普通 CALLS resolved 边 |

完整条件链的生成应该是一组逐步 trace，至少含 `input_fact_ids`、`output_fact`、`operation/model_version`、`source_sites`、`confidence/unknown`。例如把 missing key 变成 null、把 OR 中一项为 true 变成 return-null，必须列出绑定变量和源条件；固定返回一段解释文本或匹配 guard quote 不算生成这些数据。

形式上的条件结果可写为：“在所列导航/hash 稳定性与真实端口适用条件成立时，该闭合 query 构造模型不能提供 callback 查询的键；已有来源显示它会沿空值分支返回 null，并被真实 create 拒绝。”第一版 finding 保持 **conditional / uncertain**，不得改成已确定全功能失败。

## 6. 正常 boot、表单与反例都需要单独身份

### 正常 boot

[boot.ts:23](/workspace/winwincode/apps/client/src/boot.ts:23) 的调用实参是封闭字面对象 `{root, serverUrl: config.serverUrl}`。它不显式构造 taskSeed。在固定普通对象属性模型下对应真实分支；不能把所有宿主调用都推成同一选择，不能忽略 options.window、controlPlane 等注入可能改变环境。

[application.ts:193](/workspace/winwincode/apps/client/src/application.ts:193) 的 browser 来源是 `options.window ?? window`。这是被 callback 捕获的 ambient 状态，不是从 navigation 函数的 formal 参数自动传入。

### 表单门槛

[task-entry-view-model.ts:89](/workspace/winwincode/apps/client/src/task-entry-view-model.ts:89) 绑定 `const port=options.port`。submit 在 :271 起先检查 closed/status、设备、仓库、baseBranch、description、model route，再调用 :321 的 port.create。机读 `consumer.form-submit-direct-guards` 给出这些 guard 的真实 AST。

配置上下文缺口不能覆盖这些门槛，更不能说用户点击新任务就已经执行了 create。normal boot、真实端口、达到合法提交、目的 hash 未被改写是组合条件。

### fake 端口

fake factory 在 [community-control-plane-client.ts:2873](/workspace/winwincode/apps/client/src/community-control-plane-client.ts:2873)；其返回 create 方法直接构造 anchor，不调用真实 deliveryContext。机读锚点包含该方法内的全部直接 call sites，不能用全文 rg 缺引用作为“没有调用”的证据。

fake 可绕过这一真实端口前置条件，但不证明整个 UI 生命周期成功。onStarted 在 [application.ts:1332](/workspace/winwincode/apps/client/src/application.ts:1332) 仅从已有 URL 读取并复制 delivery；缺键时也不会自动创造交付锚点。不能拿 fake 的结构返回视为真实生产路径已闭合。

### Chat 创建

[application.ts:1023](/workspace/winwincode/apps/client/src/application.ts:1023) 注入 createChatDeliveryCreator。其内部 create 从 :227 的 nextDeliveryId 获取值，:230 的 createRequest.payload 携带该值，:291 的 workItemsCreateCommand 与 :305 的 startRequest.payload 再携带 deliveryId。机读 anchors 覆盖这组实际对象/参数来源，区分 :262 从已存 request 读取的另一个 local declaration。

这是独立真实路径，不能把导航合同提升为全系统缺创建能力。反之，Chat 链存在也不能为看板生产点补上它没有传入的 query seed。

## 7. 内建绑定、receiver 与 unknown 护栏

本轮机读文件级保守清单中，scope/application/community 对 URLSearchParams、Object 未观察到 runtime 同名 binding 或显式写入。这个清单可以供审查定位；它不是完整词法解析器，也不排除 host、其他模块或 prototype 改写。

正式规则至少核对：

1. 正式 snapshot 文件 parse/projection 接受且 source hash 一致；partial、ambiguous binding 或无法映射原 span 则 unknown。
2. URLSearchParams / Object 的 local/import/destructuring/catch/hoisted var/参数等 binding；相关位置被 shadow 就拒绝内建模型。转义 identifier 不做错误的“未匹配即无shadow”。
3. const receiver 的实际定义、所有读写、传入外部调用/对象属性/闭包的逃逸；动态 mutation、alias、重新赋值或未知方法不允许闭合 query 缺失负证。
4. array initializer 及 iteration 绑定；spread/nonliteral/动态数组修改不应忽略。Object.freeze 的语法形状不等于运行时永不改变或所有依赖都可信。
5. helper 的语法层直接 return 范围，排除 nested function；零匹配、复杂返回、多条返回中一条 unknown 等都不能空集通过。
6. callback 的精确对象方法身份、factory actual/formal 绑定、returned method 属性路径；不能以裸方法名 deliveryContext/create 连接不同对象。
7. query read、null-test、branch action 与 local variable 的身份；不能只搜同一文本或只摘 quote。
8. 标准 API、字符串操作、await/普通对象包装模型都使用固定受信、版本化代码。policy data-only，仅选择源码入口与审查前提，不允许执行片段、dynamic plugins 或配置预填分析结论。

无法证明 host 全局身份不被替换，是明确的标准环境模型假设；不能把它写成 AST 证明。对于尚未建模的 mutation/escape 应单独 unknown，不把“运行环境通常标准”作为忽略本地 AST 反证的理由。

## 8. 导航 owner 产物的只读复核清单

产物可静态审读时，优先核对以下数据生成边界，而不运行任何测试或目标：

- 函数、method、array、query key、null trace 的来源是否读取 SemanticSources 中同快照的 AST，而不是从规则中塞入字符串或对特定文件/函数写项目 if。
- 是否在同算法里处理 input query 与空 seed，按实际 null/set/delete 分支生成 possible/guaranteed；是否把未解出的 query键忽略成 empty。
- 真实 factory callee 是否跟随 import/source binding；第 0 实参 callback property 与返回 Object.freeze(create) 是否来自实际 object AST。
- callback 中 get literal、local-null propagation、consumer await与throw 是否各有 trace，且 trace 引用真正 lexical variable/receiver/span身份。
- rule 配置是否只含入口 locator、受信 model IDs、provenance、conditional 前提；不得接受 arbitrary source quote/expected keys/expected verdict 来替代发现。
- 正式 evidence 是否区分 `source_facts`、`model_applications`、`contract_assumptions`、`counterexamples`、`unknown`；finding 是否保留 uncertain 与作者未审批标记。
- 模型/检测器/配置版本是否进正式 policy/hash/component version；原 26 baseline 不因新增观测或新模型被重写。

本稿完成时尚未读取导航 owner 的新实现或正式 finding。因此这里是实际来源与审读规格，不宣称 owner 已满足全部条目；待文件可审读后再追加独立阅读结论。UI 标签也应等待正式 finding type 确定后再做简短中文映射，不提前宣称能力已发布。

## 9. 有限端口装配实现与冻结来源

随后获 root 授权，新增唯一核心模块 [port_wiring.py](/workspace/callscope/callscope/port_wiring.py)，API 为 `analyze_port_wiring(snapshot, navigation_rule) -> dict`。没有修改导航 owner 的 navigation_analysis.py；没有改目标或原 26 项基线。正式 rule 的 wiring 仅选择 boot/injection/use 来源入口，不能预填 taskSeed、分支结论或字段结果。

实现使用 SemanticSources 及共享 LexicalBindings：实际 boot CALLS、consumer factory CALLS 的 column-0/byte-ID/版本/目标声明均认证；参数、const 捕获和 alias 使用 declaration identity，而不是裸名字。未解析的 VM factory 调用只允许有版本的 `literal-promise-all-destructuring-assembly-1` 模型，同时核真实 import 位次、唯一捕获路径、实际导出声明、graph gap 和无重绑定；原 CALLS 仍保持动态边，未新增或改写。

源码纠正：createTaskEntryViewModel 在 :206 返回普通对象，selected submit 在 :271；nested project() 的 Object.freeze 不能当其 wrapper。真正的 port factory 返回 Object.freeze(create) 在 community :2790。实现分别记录冻结字段模型及公开 VM 未冻结条件。

Astra 独立只读复核的四处 P1 已修复：undefined 并非不可遮蔽常量，使用共享 unbound 守门；实际导出 provider 要核完整 graph 与稳定声明；内建 computed/alias/原型写入、with/eval/转义不能继续套标准模型；捕获对象 receiver call 的未知 effect 不能由“局部无赋值”排除。选定 owner 和动态旧边身份也另外收紧；没有为了检查这些规则构造目标样例或运行测试。

[PORT_WIRING_OBSERVATIONS.json](/workspace/callscope/reports/astra-iteration4/PORT_WIRING_OBSERVATIONS.json) 是对既有正式 v6 快照 `66019560ade80433538040084e66645953cdf9825b71760b9f8ff0abcd777200` 的只读语义来源采集，不是新正式 v0.7 scan。它生成 23 条事实，五段结果为 boot confirmed_static，port_selection/injection/view_model/use modeled：

- boot 实际字段只有 root/serverUrl，自动解析同一 formal 的 taskSeed/严格 undefined guard，选中真实 factory 分支。
- 同一 taskPort declaration ID 从 :277 捕获到 :1322 的 port 注入字段。
- Promise.all 数组第 0 实际 namespace 解构到 createTaskEntryViewModel 导出，再绑定 formal options 的 port 字段到 :89 的 const port。
- plain returned submit 的 :321 调用捕获同一 const port；六个实际前置 guard 分别保存，未计算用户输入是否满足。

`source_fact_confirmed=true` / `assembly_complete=true` **只指有限装配范围**。`end_to_end_complete=false`；残余保留原动态 injection CALLS、两个 describe 未分析 effect、公开 VM 可变性、route dispatch 未分析以及事件/合法提交/hash 稳定性未闭合。未知副作用不被当成已执行改写，普通 VM 未冻结也不被当成观察到运行替换。

末轮又按 Astra 要求补入 iterator/Promise 护栏：generator/async-generator 或本函数直接 yield 不按普通调用进入 body；工厂/VM 的未等待 async 返回不当作直接对象；普通/async boot 的参数身份和普通 async create 方法仍可记录。异步方法的源码拒绝分支不表示观察到同步抛出。

模块完成此窄修后重新冻结：`VERSION=finite-port-wiring-1`，SHA-256 为 `7e7291643aa873a697b7ea9d123fb274732badeb617754f73d7619ad6a9efc45`。保存观察由同一 v6 源实际重新生成，仍为 23 条事实与五个有限装配段，其模块哈希与最终护栏版本匹配。正式新扫描及完整导航 owner 合成结果由 root 后续生成；本来源稿不冒称它们已经完成。
