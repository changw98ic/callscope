# WinWinCode 前端与控制面：只读源码来源整理

日期：2026-10-12。目标目录：/workspace/winwincode。读取时 HEAD：da407e4f3df3719718b23bd8913b73fe3ff73857。

这份材料供 Astra 独立审查使用，记录实际源码接线、职责与条件性缺口。只读取源码和 Git HEAD；没有导入或执行目标模块，没有构建、测试、浏览器验证，也没有修改目标仓库。源码链存在仅说明相关入口和依赖已经接上，不证明条件可执行、外部设备可用或功能结果正确。

## 1. 组合根与工作区边界

| 层次 | 源码入口与职责 | 来源 |
| --- | --- | --- |
| 浏览器发布入口 | public/index.html 先加载 runtime-config.js，再加载 assets/client.js，挂载点为 data-winwincode-client-root。构建脚本把 src/boot.ts 作为浏览器 bundle 入口；本次只读了脚本。 | [index.html:10](/workspace/winwincode/apps/client/public/index.html:10)、[build.mjs:151](/workspace/winwincode/apps/client/scripts/build.mjs:151) |
| 部署配置与启动 | readWinWinCodeClientRuntimeConfig 从全局配置读取 serverUrl，交给 parseControlPlaneServerUrl；boot 再调用 mountWinWinCodeClient。启动错误进入可见错误文案。正常启动不提供 taskSeed。 | [runtime-config.ts:12](/workspace/winwincode/apps/client/src/runtime-config.ts:12)、[boot.ts:20](/workspace/winwincode/apps/client/src/boot.ts:20) |
| 浏览器组合根 | mountWinWinCodeClient 负责外壳、认证、连接监控、查询缓存、Clients/Repositories/Occupancy/Candidates/WorkerSession 端口，以及按路由动态挂载特性。 | [application.ts:190](/workspace/winwincode/apps/client/src/application.ts:190) |
| 共享查询与范围 | application 直接使用 @winwincode/browser-core/query-cache 和 scope-context。query-cache 统一查询复用及命令、事件、授权变更的失效；scope-context 负责 URL 范围解析、授权匹配和链接生成。 | [application.ts:57](/workspace/winwincode/apps/client/src/application.ts:57)、[query-cache.ts:576](/workspace/winwincode/packages/browser-core/src/query-cache.ts:576)、[scope-context.ts:217](/workspace/winwincode/packages/browser-core/src/scope-context.ts:217) |
| 产品 TS API 适配器 | community-control-plane-client 接入公共 @winwincode/control-plane-client，同时注入本产品生成的 HTTP/WebSocket transport；还提供设备目录、占用、候选、任务、预览等产品端口。 | [community-control-plane-client.ts:3](/workspace/winwincode/apps/client/src/community-control-plane-client.ts:3)、[community-control-plane-client.ts:361](/workspace/winwincode/apps/client/src/community-control-plane-client.ts:361) |
| 公共 TS facade | packages/control-plane-client 的 createControlPlaneClient 处理 Server URL、认证会话、命令、查询及订阅。生成契约通过注入接入，页面无需直接操纵 transport。 | [index.ts:851](/workspace/winwincode/packages/control-plane-client/src/index.ts:851) |
| Rust 发布组合根 | main 组合 ControlPlane、SqliteStorage、DurableEventHub、ProductSessionExecutionApplication、RepositoryRuntimeScheduler、远端 Worker/Client exchange 与 GeneratedContractDispatcher，随后启动一个 Server。 | [main.rs:280](/workspace/winwincode/crates/winwincode-server/src/main.rs:280)、[main.rs:359](/workspace/winwincode/crates/winwincode-server/src/main.rs:359)、[main.rs:472](/workspace/winwincode/crates/winwincode-server/src/main.rs:472) |
| Rust HTTP 与契约分发 | server 的 router 接收公开 API；GeneratedContractDispatcher 验证 actor、授权范围及生成契约，再按 CommandFamily/QueryFamily 分发给 StandaloneControlPlaneApplication。 | [server.rs:419](/workspace/winwincode/crates/winwincode-server/src/server.rs:419)、[dispatcher.rs:203](/workspace/winwincode/crates/winwincode-server/src/dispatcher.rs:203)、[application.rs:1237](/workspace/winwincode/crates/winwincode-server/src/application.rs:1237) |

应用组合根将 rawControlPlane 包装为连接监控，再包装为 queryCache.client，供普通特性使用：[application.ts:205](/workspace/winwincode/apps/client/src/application.ts:205)。登录、设备目录、候选与设备启动端口保留 rawControlPlane 或 browserTransport 接线，不应把这些端口没有经过同一缓存 wrapper 解释为“没有服务接入”：见 [application.ts:221](/workspace/winwincode/apps/client/src/application.ts:221)、[application.ts:234](/workspace/winwincode/apps/client/src/application.ts:234)、[application.ts:241](/workspace/winwincode/apps/client/src/application.ts:241)、[application.ts:250](/workspace/winwincode/apps/client/src/application.ts:250)。

公共 package 的 exports 指向发布 dist，人工源码整理按 package 内源码定位。这里只确认源码依赖与 API 边界，没有验证已构建包或安装后的发布产物。

## 2. Route / Client / Scope 生命周期

1. clientSurfaceFromHash 选择 Chat、Home、Projects、Extensions、Device、Settings 或 Onboarding；默认 Chat，子路径沿所属顶层 surface 识别：[client-surface.ts:26](/workspace/winwincode/apps/client/src/client-surface.ts:26)、[client-surface.ts:87](/workspace/winwincode/apps/client/src/client-surface.ts:87)。
2. performRender 每次增加 renderGeneration，abort 旧 featureController、close 旧 activeFeature，清空旧作用域和页面 slot，再为当前 URL 解析授权范围：[application.ts:1782](/workspace/winwincode/apps/client/src/application.ts:1782)。
3. resolveScopeContext 只依据当前 AuthSession.authorizedScopes 和 URL；空选择仅在一个兼容范围时自动选中，越权、无兼容范围或多个候选分别返回 denied / empty / selection-required：[scope-context.ts:217](/workspace/winwincode/packages/browser-core/src/scope-context.ts:217)。
4. authenticatedRouteContext 要求已登录且选中 RepositoryScope，否则输出不可用状态，不构造业务端口：[application.ts:892](/workspace/winwincode/apps/client/src/application.ts:892)。
5. Home 子路由为 new-task、run / task-run、preview、clarify、review 和默认看板；run 需要有效 task 与 delivery 锚点：[application.ts:1272](/workspace/winwincode/apps/client/src/application.ts:1272)、[application.ts:1285](/workspace/winwincode/apps/client/src/application.ts:1285)。分发入口见 [application.ts:1907](/workspace/winwincode/apps/client/src/application.ts:1907)。
6. hashchange、认证恢复/失效、窗口错误、online/offline 驱动外壳更新；路由异步结果检查 generation 与 aborted。application.close 解除监听、停止历史刷新、关闭 feature、readiness、认证及各共享模型：[application.ts:1981](/workspace/winwincode/apps/client/src/application.ts:1981)、[application.ts:2023](/workspace/winwincode/apps/client/src/application.ts:2023)、[application.ts:2078](/workspace/winwincode/apps/client/src/application.ts:2078)。

这是一套单一外壳与独立特性生命周期的组合。Community 在源码中明确只承载一个本地 Owner 及单一仓库场景，不应以缺少多组织管理路由判定功能遗漏：[application.ts:3](/workspace/winwincode/apps/client/src/application.ts:3)、[application.ts:1831](/workspace/winwincode/apps/client/src/application.ts:1831)。

## 3. Chat → ProductSession → Device Worker

### 前端接线

- renderChat 读取 session/client/repositoryBinding 参数；已有 ProductSession 的 deviceContext 优先决定设备与仓库绑定。若指定项目，使用 clientDirectory 查实际设备和仓库，缺项则显示不可用：[application.ts:940](/workspace/winwincode/apps/client/src/application.ts:940)。
- 随后动态加载 ChatViewModel、ChatPage、ChatDeliveryCreator 和交付列表模型，并以当前 actor / RepositoryScope 组合：[application.ts:985](/workspace/winwincode/apps/client/src/application.ts:985)。
- ChatViewModel.createSession 检查当前模型路由可用，发送 session.create，校验返回会话 ID，保存 pendingDeviceSession，重新读取快照：[chat-view-model.ts:1480](/workspace/winwincode/apps/client/src/chat-view-model.ts:1480)。
- submitMessage 在 chat.submit 之前调用注入的 launchDeviceSession。应用注入的实现先 claim occupancy，再 workerSessions.launch；后者连接 /api/v1/sessions。发送命令附带 ProductSession revision 与 attachments：[chat-view-model.ts:1426](/workspace/winwincode/apps/client/src/chat-view-model.ts:1426)、[application.ts:1003](/workspace/winwincode/apps/client/src/application.ts:1003)、[community-control-plane-client.ts:2692](/workspace/winwincode/apps/client/src/community-control-plane-client.ts:2692)。
- querySnapshot 汇集会话、消息、运行投影、交互和审批；subscribeRealtime 接续事件；输入回应、审批与取消分别有命令路径：[chat-view-model.ts:728](/workspace/winwincode/apps/client/src/chat-view-model.ts:728)、[chat-view-model.ts:1332](/workspace/winwincode/apps/client/src/chat-view-model.ts:1332)、[chat-view-model.ts:1553](/workspace/winwincode/apps/client/src/chat-view-model.ts:1553)、[chat-view-model.ts:1591](/workspace/winwincode/apps/client/src/chat-view-model.ts:1591)、[chat-view-model.ts:1641](/workspace/winwincode/apps/client/src/chat-view-model.ts:1641)。
- mountChatPage 启动模型和交付列表，创建订阅与刷新计时器；close 完整关闭模型、creator、列表、监听与渲染器：[chat-page.ts:1231](/workspace/winwincode/apps/client/src/chat-page.ts:1231)、[chat-page.ts:1248](/workspace/winwincode/apps/client/src/chat-page.ts:1248)。

### Rust 接收与后续生命周期

HTTP command → GeneratedContractDispatcher → CommandFamily.Session → StandaloneControlPlaneApplication.session_command → ProductSessionApiService.create / submit_chat / cancel。InputRespond 和 ApprovalDecide 分流到 interaction_command：

- [dispatcher.rs:31](/workspace/winwincode/crates/winwincode-server/src/dispatcher.rs:31)
- [application.rs:1239](/workspace/winwincode/crates/winwincode-server/src/application.rs:1239)
- [application.rs:385](/workspace/winwincode/crates/winwincode-server/src/application.rs:385)
- [product_session_api.rs:87](/workspace/winwincode/crates/winwincode-control-plane/src/product_session_api.rs:87)
- [product_session_api.rs:124](/workspace/winwincode/crates/winwincode-control-plane/src/product_session_api.rs:124)

chat.submit 的 Server 路径要求 Device session gate 与设备模型路由可用；没有设备锚点可返回 DEVICE_SESSION_REQUIRED。服务层 prepare ExecutionJob、校验 revision、更新 ProductSession 与消息，之后 Server dispatch_turn_to_device_worker，并 publish_pending 到 DurableEventHub：[application.rs:399](/workspace/winwincode/crates/winwincode-server/src/application.rs:399)、[product_session_chat.rs:583](/workspace/winwincode/crates/winwincode-control-plane/src/product_session_chat.rs:583)、[application.rs:472](/workspace/winwincode/crates/winwincode-server/src/application.rs:472)。

因此“前端发送了消息”与“设备完成了一轮执行”是不同事实。这里确认的是命令、设备启动和持久化/事件路径已接线，未证明设备实际收到或模型产生正确输出。

## 4. Delivery / WorkRun / Candidate / Preview 生命周期

### 从 Chat 草稿创建交付

Chat conversion 表单显式调用注入的 deliveryCreator.create，包含 sourceProductSessionId、baseRevision、验收条件与 verificationCommand：[chat-page.ts:1182](/workspace/winwincode/apps/client/src/chat-page.ts:1182)。

ChatDeliveryCreator 的链路为：

    DeliveryCreate → queryWorkRunAggregate → workitems.create → workrun.start
                   → created 状态 → onCreated → 页面刷新交付列表

具体来源：[chat-delivery-creator.ts:167](/workspace/winwincode/apps/client/src/chat-delivery-creator.ts:167)、[chat-delivery-creator.ts:235](/workspace/winwincode/apps/client/src/chat-delivery-creator.ts:235)、[chat-delivery-creator.ts:286](/workspace/winwincode/apps/client/src/chat-delivery-creator.ts:286)、[chat-delivery-creator.ts:299](/workspace/winwincode/apps/client/src/chat-delivery-creator.ts:299)、[chat-page.ts:1232](/workspace/winwincode/apps/client/src/chat-page.ts:1232)。creator 保存请求和提交阶段，草稿改变后不能静默替换此前 attempt；这里只确认有这些状态与校验，不作网络重试通过保证。

Rust 将上述命令归为 Delivery family；delivery_command 依次转交 ControlPlane.delivery_create / work_items_create / workrun_start 等服务，工作运行提交后接 dispatch_work_run_to_device_worker 并发布事件：[dispatcher.rs:37](/workspace/winwincode/crates/winwincode-server/src/dispatcher.rs:37)、[application.rs:635](/workspace/winwincode/crates/winwincode-server/src/application.rs:635)、[delivery_application.rs:533](/workspace/winwincode/crates/winwincode-control-plane/src/delivery_application.rs:533)、[delivery_application.rs:683](/workspace/winwincode/crates/winwincode-control-plane/src/delivery_application.rs:683)。

### 任务运行与候选身份

正常 boot 下 taskPort 是 createControlPlaneTaskPort；只有显式 taskSeed 才选择 fake task store 与 fixtureRunIdentity：[application.ts:277](/workspace/winwincode/apps/client/src/application.ts:277)。因此源码出现 Fake 名称不能单独作为生产使用假结果的证据。

真实任务端口依赖一个已有 deliveryContext，创建 WorkItem，启动 WorkRun，启动所选 Device WorkerSession，再查询 canonical aggregate 验证 run 与设备绑定，最后返回 task anchor：[community-control-plane-client.ts:2775](/workspace/winwincode/apps/client/src/community-control-plane-client.ts:2775)。

renderTaskRun 从 URL task/delivery 构建 anchor，依赖真实 runIdentityPort。该 port 先读取 DeliveryDetail，再以相同 readCursor 读 WorkRunAggregate，选取当前候选 producer 的运行及设备绑定，核对设备候选 commit / repositoryBinding；不存在必要事实时直接报错，而不是凭 URL 任意生成候选：[application.ts:1352](/workspace/winwincode/apps/client/src/application.ts:1352)、[community-control-plane-client.ts:3003](/workspace/winwincode/apps/client/src/community-control-plane-client.ts:3003)。

### Frozen candidate 预览

renderCandidateRunPreview 要求有效 delivery/task；重新读取 canonical identity，要求 candidate 和 fileContext，组合 frozen-candidate、commit、tree、run、attempt 与配置事实后挂载页面：[application.ts:1468](/workspace/winwincode/apps/client/src/application.ts:1468)、[application.ts:1520](/workspace/winwincode/apps/client/src/application.ts:1520)、[candidate-run-preview-control-plane.ts:69](/workspace/winwincode/apps/client/src/candidate-run-preview-control-plane.ts:69)。

预览端口的主要边界：

| 作用 | TS 路径 | Rust 接口 |
| --- | --- | --- |
| 授权/撤销预览 | createControlPlaneCandidatePreviewPort.authorizePreview / revokePreview | POST /api/v1/previews、DELETE /api/v1/previews/{access_id} |
| 冻结文件列表、内容、diff | candidate.files.list / candidate.file.content.get / candidate.diff.get，携带 readCursor、candidateRef、candidateTreeId、diffSha256 | queries → Delivery family → strongflow_query |
| 受管应用 start/stop/restart/query | managedAppRequest 校验 occupancy lease、fencing token 和 canonical config；浏览器发送运行身份，完整执行配置由 Server 解析 | POST /api/v1/clients/{client_id}/managed-app |
| 页面批注 | annotationFacts 再读当前 candidate、contract、attention、evidence；CollaborationPageAnnotationSubmit 绑定候选、运行与规范 revision | command → Collaboration family |

来源：[candidate-run-preview-control-plane.ts:507](/workspace/winwincode/apps/client/src/candidate-run-preview-control-plane.ts:507)、[candidate-run-preview-control-plane.ts:553](/workspace/winwincode/apps/client/src/candidate-run-preview-control-plane.ts:553)、[candidate-run-preview-control-plane.ts:636](/workspace/winwincode/apps/client/src/candidate-run-preview-control-plane.ts:636)、[candidate-run-preview-control-plane.ts:443](/workspace/winwincode/apps/client/src/candidate-run-preview-control-plane.ts:443)、[candidate-run-preview-control-plane.ts:737](/workspace/winwincode/apps/client/src/candidate-run-preview-control-plane.ts:737)、[server.rs:450](/workspace/winwincode/crates/winwincode-server/src/server.rs:450)、[server.rs:538](/workspace/winwincode/crates/winwincode-server/src/server.rs:538)、[application.rs:1085](/workspace/winwincode/crates/winwincode-server/src/application.rs:1085)、[application.ts:1598](/workspace/winwincode/apps/client/src/application.ts:1598)、[application.ts:1667](/workspace/winwincode/apps/client/src/application.ts:1667)。

CandidatePreviewViewModel.start 只加载/校验身份；authorizePreview 才授权来源和读取文件；startRun/stopRun/restartRun 是分别触发的操作。不能把 start 或 ready 状态等同于已启动受管应用或验收通过：[candidate-run-preview-view-model.ts:677](/workspace/winwincode/apps/client/src/candidate-run-preview-view-model.ts:677)、[candidate-run-preview-view-model.ts:710](/workspace/winwincode/apps/client/src/candidate-run-preview-view-model.ts:710)、[candidate-run-preview-view-model.ts:810](/workspace/winwincode/apps/client/src/candidate-run-preview-view-model.ts:810)。

### 审核、应用与需求编辑

renderReview 注入 StrongFlowReviewViewModel、annotations，以及 clientCandidates/directory/claim 的候选操作端口：[application.ts:1731](/workspace/winwincode/apps/client/src/application.ts:1731)。review 模型读取 Delivery、候选、WorkRun、Runtime、Evidence 和 artifact；acceptDelivery 要求当前 candidate commit 与通过的 verdict 绑定一致，再提交 DeliveryResolveAttention：[strongflow-review-view-model.ts:1048](/workspace/winwincode/apps/client/src/strongflow-review-view-model.ts:1048)。

设备候选 branch/apply/discard 是独立 API，具有 online、holder lease、仓库授权及候选状态检查；apply 经设备下行命令等待真实 settlement，不是浏览器本地改状态：[community-control-plane-client.ts:2048](/workspace/winwincode/apps/client/src/community-control-plane-client.ts:2048)、[server.rs:522](/workspace/winwincode/crates/winwincode-server/src/server.rs:522)、[client_candidates.rs:287](/workspace/winwincode/crates/winwincode-server/src/client_candidates.rs:287)、[client_candidates.rs:304](/workspace/winwincode/crates/winwincode-server/src/client_candidates.rs:304)、[client_candidates.rs:490](/workspace/winwincode/crates/winwincode-server/src/client_candidates.rs:490)。

renderDecisionClarification 组合真实 createControlPlaneClarificationPort，load 读取 delivery.get，save 发送 delivery.update_spec，并携带 expectedRevision：[application.ts:1421](/workspace/winwincode/apps/client/src/application.ts:1421)、[decision-clarification-view-model.ts:190](/workspace/winwincode/apps/client/src/decision-clarification-view-model.ts:190)、[decision-clarification-view-model.ts:242](/workspace/winwincode/apps/client/src/decision-clarification-view-model.ts:242)。

## 5. Readiness 的实际职责与边界

ReadinessViewModel 为已授权 RepositoryScope 并行读取：

- ModelRouteAvailabilityList；
- CredentialReferenceList；
- WorkerList；
- SessionList 与 DeliveryList。

它计算模型可用、凭据引用存在/可用、Server/Worker 报告、enabled worker capacity，以及已有对话/交付等准备信号。不是代码或交付结果验证：[readiness-view-model.ts:336](/workspace/winwincode/apps/client/src/readiness-view-model.ts:336)。scope 改变会取消旧消费者；结果按 generation 防止串范围，显式 refresh 清相关查询缓存；close 取消请求并停止监听：[readiness-view-model.ts:485](/workspace/winwincode/apps/client/src/readiness-view-model.ts:485)、[readiness-view-model.ts:547](/workspace/winwincode/apps/client/src/readiness-view-model.ts:547)。

应用根确实构造 model 与 mountReadinessPage，并在 render 时 updateContext：[application.ts:741](/workspace/winwincode/apps/client/src/application.ts:741)、[application.ts:1858](/workspace/winwincode/apps/client/src/application.ts:1858)。但当前 Community 外壳明确将 readinessRoot 始终隐藏，源码注释说明不再把内联清单放在内容上方：[application.ts:1854](/workspace/winwincode/apps/client/src/application.ts:1854)。Onboarding 是设备连接页面，[onboarding-page.ts:36](/workspace/winwincode/apps/client/src/onboarding-page.ts:36)。

因此，应分别记录“readiness 后台模型已接线”和“该清单在此外壳内不显示”。仅凭页面模块存在或模型 ready，不能声称用户已看到独立清单；也不能忽视明确的设计注释，把隐藏区块直接列为断链。readiness 模块还经 client index 导出供 host 使用：[index.ts:23](/workspace/winwincode/apps/client/src/index.ts:23)。

## 6. TS 与 Rust 之间如何连接

跨语言连接的依据是端点、schema、命令/查询名、请求字段与分发枚举，不是语言内 CALLS 边：

    TS feature / view-model
      → community-control-plane-client + public facade + generated transport
      → HTTP commands/queries 或 WebSocket events
      → Rust router / authorize / GeneratedContractDispatcher
      → CommandFamily / QueryFamily
      → StandaloneControlPlaneApplication
      → ControlPlane / ProductSession / ClientSessions / Candidate 服务

TS 生成 transport 的端点为 /api/v1/commands、/api/v1/queries、/api/v1/events：[generated/control-plane-client.ts:5](/workspace/winwincode/apps/client/src/generated/control-plane-client.ts:5)。community adapter 注入 transport，并给 HTTP 请求设置 credentials=include：[community-control-plane-client.ts:301](/workspace/winwincode/apps/client/src/community-control-plane-client.ts:301)。Rust 对应注册同名 route，并在 command/query handler 内 authorize 后调用 state.api.command/query：[server.rs:433](/workspace/winwincode/crates/winwincode-server/src/server.rs:433)、[server.rs:2337](/workspace/winwincode/crates/winwincode-server/src/server.rs:2337)、[server.rs:2360](/workspace/winwincode/crates/winwincode-server/src/server.rs:2360)。

生产 main 在 run_remote_composition 构造 GeneratedContractDispatcher，同时提供 Some(exchange) 和 Some(client_exchange) 给 Server：[main.rs:396](/workspace/winwincode/crates/winwincode-server/src/main.rs:396)、[main.rs:417](/workspace/winwincode/crates/winwincode-server/src/main.rs:417)。因此目录、占用、候选、设备启动在这个组合根中有真实接入。Server 的替代启动方式若没有 client_exchange，会缺少相应 application；preview_public_url 未配置也可使预览 application 不可用，这是配置边界，不是默认所有端点已就绪的保证：[server.rs:255](/workspace/winwincode/crates/winwincode-server/src/server.rs:255)、[server.rs:308](/workspace/winwincode/crates/winwincode-server/src/server.rs:308)。

工具当前 application.ts 的 inline import type 解析 gap 不影响人工来源阅读。比如 [application.ts:272](/workspace/winwincode/apps/client/src/application.ts:272)、[application.ts:956](/workspace/winwincode/apps/client/src/application.ts:956)、[application.ts:966](/workspace/winwincode/apps/client/src/application.ts:966) 中的 import(...).Type 是类型位置；图里缺少该文件或调用边不能直接解释成生产没有这些功能。这里的协议连接来自逐项源码对照，没有把它伪装成工具已经提取出的确定跨语言 CALLS 边。

## 7. 两处供独立复核的条件性接线缺口

### WWC-FE-01：看板“新任务”入口没有 Delivery context

**确定的源码条件链：**

1. 当前可见看板的 newTask.href 为 surfaceHash('/home/new-task', scopeSelection)，只带范围字段，没有 delivery：[home-dashboard-page.ts:359](/workspace/winwincode/apps/client/src/home-dashboard-page.ts:359)。隐藏的 my-work start entry 也如此：[my-work-page.ts:119](/workspace/winwincode/apps/client/src/my-work-page.ts:119)。后者是旁证，可见入口以前者为主。
2. normal boot 不注入 taskSeed，application 默认使用真实 taskPort：[boot.ts:23](/workspace/winwincode/apps/client/src/boot.ts:23)、[application.ts:277](/workspace/winwincode/apps/client/src/application.ts:277)。
3. 真实 taskPort.deliveryContext 仅从当前 URL 取 delivery；没有值即返回 null：[application.ts:285](/workspace/winwincode/apps/client/src/application.ts:285)。
4. TaskEntry 提交只构造 clientId、repositoryBindingId、baseBranch、description、modelRouteId，然后调用 port.create；该输入不提供交付选择或交付创建：[task-entry-view-model.ts:311](/workspace/winwincode/apps/client/src/task-entry-view-model.ts:311)。
5. 真实 TaskPort.create 先读取 deliveryContext，null 时在发送任何创建命令前直接抛出“创建任务项前请选择交付。”：[community-control-plane-client.ts:2791](/workspace/winwincode/apps/client/src/community-control-plane-client.ts:2791)。

**候选结论：**在正常 boot、由可见看板入口进入且用户未手工补入 delivery 参数的条件下，这条“新任务”链会在创建 WorkItem 前被拒绝。需要交付创建步骤、选择已有交付步骤或携带已有 delivery 的入口之一，才能满足真实端口前置条件。这里确认的是代码条件矛盾，没有运行用户交互。

**反证与边界：**带有效 delivery 的手工深链接并不受这一缺口影响；ChatDeliveryCreator 已有 DeliveryCreate → workitems.create → workrun.start 的另一条真实链。显式 taskSeed 还可选择 fake port，所以仅验证 fixture 成功可能避开生产条件。不能由此推断“系统没有任何任务创建能力”。

### WWC-FE-02：Device 交付需求编辑遗漏 verificationCommand

**确定的源码条件链：**

1. renderDecisionClarification 使用真实 createControlPlaneClarificationPort：[application.ts:1439](/workspace/winwincode/apps/client/src/application.ts:1439)。
2. clarificationUpdateCommand 重建完整 spec，保留 sourceProductSessionId/baseRevision/验收条件等，但没有 verificationCommand；save 将它发送为 delivery.update_spec：[decision-clarification-view-model.ts:190](/workspace/winwincode/apps/client/src/decision-clarification-view-model.ts:190)、[decision-clarification-view-model.ts:242](/workspace/winwincode/apps/client/src/decision-clarification-view-model.ts:242)。现有 criterion.verificationMethod 虽在读取时进入草稿，也没有被转成这个顶层字段：[decision-clarification-view-model.ts:155](/workspace/winwincode/apps/client/src/decision-clarification-view-model.ts:155)。
3. Rust DeliveryUpdateSpec 仍走 specification authority：[delivery_application.rs:582](/workspace/winwincode/crates/winwincode-control-plane/src/delivery_application.rs:582)。
4. 生产 specification adapter 对 DeliveryCreate 和 DeliveryUpdateSpec 都取本次 payload.spec：[delivery_production_adapters.rs:584](/workspace/winwincode/crates/winwincode-control-plane/src/delivery_production_adapters.rs:584)。
5. device_target 从 source ProductSession 的 WorkerLaunchGrant 定位 Device；若设备目标存在且基准等其他前置条件满足，该分支必须得到非空 spec.verification_command，否则返回“Device delivery requires a confirmed verification command”：[delivery_production_adapters.rs:252](/workspace/winwincode/crates/winwincode-control-plane/src/delivery_production_adapters.rs:252)、[delivery_production_adapters.rs:609](/workspace/winwincode/crates/winwincode-control-plane/src/delivery_production_adapters.rs:609)。

**候选结论：**对于仍满足 Device 来源条件的交付，当前需求编辑路径构造出的请求缺少后端所需字段，不能通过该 specification 分支。创建曾成功并不能证明编辑链完整；需要保留或明确编辑原已确认的方法，或由可信后端在允许的更新语义下保留它。这里没有执行任何验证命令，verificationCommand 仅作为已存在协议字段被读取。

**反证与边界：**ChatDeliveryCreator 创建请求在 [chat-delivery-creator.ts:246](/workspace/winwincode/apps/client/src/chat-delivery-creator.ts:246) 明确传该字段；device_target=null 的本地非 Device 分支会通过仓库上下文 select_verification_command，不依赖该字段：[delivery_production_adapters.rs:637](/workspace/winwincode/crates/winwincode-control-plane/src/delivery_production_adapters.rs:637)。不能扩大成“所有交付编辑都失败”，也不能误称已创建的验证方法已被成功清空；源码首先表现为更新请求被拒。

## 8. 交给 Astra 的判断边界

已确认源码存在浏览器组合根、共享 TS facade、生成 transport、Rust 分发、ProductSession 与 Delivery/WorkRun 服务，以及设备候选与预览的真实 API 接线。主要生命周期有明确 actor/scope、revision、readCursor、候选 identity 和 close/generation 结构。

两处候选都属于源码可识别的入口/参数前置条件不匹配，无需通过执行目标来定位。最终报告应保留它们的具体条件、反证和独立复核状态；不把静态链路存在、准备状态 ready 或没有规则违规升级为全功能完整性保证。设备握手、模型输出、网络部署、实际发布 bundle、候选运行与业务结果均未在本次只读来源整理中验证。
