# WinWinCode / 项目源码静态调用核对：自动静态分析报告

快照：`cc327a390837a897be93cdd4bdd4d9ad652c47f70f0b0dbfbbf89a52b463d372`；仅使用保存源码、图和静态分析证据，未执行目标、测试或构建。

## 主要发现

- **WWC-01**：所选公开导航未提供消费者必需的查询上下文；经真实生产装配与缺值传播，创建在提交命令前被拒绝。有效上下文和替代创建入口是反证。 完整判断=`true`；支持原有限判断=`true`；条件、反证和来源：`/judgments/0`。
- **WWC-02**：所选提交对象遗漏条件分支必填字段；经过生成协议、普通 JSON 与 Serde 映射后，权威非空守卫在使用或提交前拒绝。其它分支和显式字段来源是反证。 完整判断=`true`；支持原有限判断=`true`；条件、反证和来源：`/judgments/1`。

原始完整 JSON 保留所有条件、反证、未知项、source facts 和保存发现身份。以下限制仅影响展示，不改变分析结果。

### WWC-01

保存发现：`27ca18396beeb47bea36a628`；证据：`b53ade9dca10d93c45a94cc1`。

**推导**：`/judgments/0/derived_judgment`。

**适用条件**：`/judgments/0/conditions`。

**反证与范围**：`/judgments/0/refutations`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| supported | true | /judgments/0/refutations/supported |
| independent_chat_source/supported | true | /judgments/0/refutations/independent_chat_source/supported |
| independent_chat_source/actual_chat_success_proven | false | /judgments/0/refutations/independent_chat_source/actual_chat_success_proven |
| scope_exclusion_is_not_independent_chat_success_proof | true | /judgments/0/refutations/scope_exclusion_is_not_independent_chat_success_proof |
| source_derived/0/producer/abstract_value/exact_text | null | /judgments/0/refutations/source_derived/0/producer/abstract_value/exact_text |
| source_derived/0/producer/abstract_value/kind | string | /judgments/0/refutations/source_derived/0/producer/abstract_value/kind |
| source_derived/0/producer/abstract_value/runtime_execution_proven | false | /judgments/0/refutations/source_derived/0/producer/abstract_value/runtime_execution_proven |
| source_derived/0/producer/abstract_value/segments/0/kind | literal | /judgments/0/refutations/source_derived/0/producer/abstract_value/segments/0/kind |

**必要缺口**：`/judgments/0/necessary_gaps`。

| 必要关系 | 实际结果 |
| --- | --- |
| N1 | supported |
| N2 | supported |
| N3 | supported |
| N4 | supported |
| N5 | supported |
| N6 | supported |
| N7 | supported |

### WWC-02

保存发现：`547f718f81cb530068c86aef`；证据：`d7a8c3f23d4c857eb2c19799`。

**推导**：`/judgments/1/derived_judgment`。

**适用条件**：`/judgments/1/conditions`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| kind | true_environment_and_model_conditions | /judgments/1/conditions/kind |
| provenance/author_approved | false | /judgments/1/conditions/provenance/author_approved |
| provenance/authority | Astra original WWC-02 source report, conditional code judgment | /judgments/1/conditions/provenance/authority |
| provenance/source_doc | reports/astra-baseline/WINWINCODE_ANALYSIS.md#wwc-02 | /judgments/1/conditions/provenance/source_doc |
| source_class | policy-declared | /judgments/1/conditions/source_class |

**反证与范围**：`/judgments/1/refutations`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| /0/status | supported | /judgments/1/refutations/0/status |
| /1/status | supported | /judgments/1/refutations/1/status |
| /2/status | supported | /judgments/1/refutations/2/status |
| /3/status | supported | /judgments/1/refutations/3/status |
| /4/status | supported | /judgments/1/refutations/4/status |
| /5/status | supported | /judgments/1/refutations/5/status |
| /6/status | supported | /judgments/1/refutations/6/status |
| /7/status | supported | /judgments/1/refutations/7/status |

**必要缺口**：`/judgments/1/necessary_gaps`。

| 必要关系 | 实际结果 |
| --- | --- |
| D1 | supported |
| D2 | supported |
| D3 | supported |
| D4 | supported |
| D5 | supported |

## 文档与实际部署来源

所选文档描述 Control Plane 内部唯一模型路由及 Worker 仅经模型流；所选 Device 源码另有本地 provider 选择、字节 material 容器与调用来源，表述需要说明部署范围。

源码关系评估：`scoped_source_relations_supported`；完整对照：`/functional_chains/3/pattern`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| statement | 所选文档描述 Control Plane 内部唯一模型路由及 Worker 仅经模型流；所选 Device 源码另有本地 provider 选择、字节 material 容器与调用来源，表述需要说明部署范围。 | /functional_chains/3/pattern/comparison/statement |
| classification | selected_document_wording_requires_device_deployment_qualification | /functional_chains/3/pattern/comparison/classification |
| actual_deployment_or_network_execution_verified | false | /functional_chains/3/pattern/comparison/actual_deployment_or_network_execution_verified |
| document_control_plane_internal_scope_preserved | true | /functional_chains/3/pattern/comparison/document_control_plane_internal_scope_preserved |
| global_project_exclusivity_inferred_from_document | false | /functional_chains/3/pattern/comparison/global_project_exclusivity_inferred_from_document |
| long_term_credential_exclusivity_refuted | unknown | /functional_chains/3/pattern/comparison/long_term_credential_exclusivity_refuted |
| public_delivery_or_contract_secret_leak_proven | false | /functional_chains/3/pattern/comparison/public_delivery_or_contract_secret_leak_proven |
| raw_secret_reference_equated_with_material | false | /functional_chains/3/pattern/comparison/raw_secret_reference_equated_with_material |
| secret_material_lifetime | unknown | /functional_chains/3/pattern/comparison/secret_material_lifetime |
| security_defect_declared | false | /functional_chains/3/pattern/comparison/security_defect_declared |
| worker_execution_port_protocol_bypass_proven | false | /functional_chains/3/pattern/comparison/worker_execution_port_protocol_bypass_proven |

- 文档明确限定Control Plane内部唯一；所选Device源码另有本地provider装配、消费及凭据字节操作来源，宜补充部署分支说明，不能把内部唯一扩成全项目唯一。 结果=`selected_document_wording_requires_device_deployment_qualification`；原文与来源事实：`/functional_chains/3/pattern/documentation_comparisons/0`。

- 文档谈长期Credential；所选代码来源为Vec&lt;u8&gt;/ResolvedSecret字节容器，字节材料与凭据引用须区分，也无法据此确定凭据长期性或公开Delivery密钥泄露。 结果=`material_source_distinguished_lifetime_unknown`；原文与来源事实：`/functional_chains/3/pattern/documentation_comparisons/1`。

- Worker源码在本地消费者返回Ok(true)时提前返回；正常未消费分支走transport，错误可提前传播。仍使用ExecutionPort消息，不能由本地provider路径推断绕过模型流协议。 结果=`local_source_route_does_not_prove_stream_protocol_bypass`；原文与来源事实：`/functional_chains/3/pattern/documentation_comparisons/2`。

## 具体职责与接口交接

以下正文由所选声明的实际记录字段、赋值、实参接口和提前退出条件生成。目录名只供导航；普通调用、消息字段、执行、交付和投影分别保留。

完整职责、所有操作和来源：`/architecture/responsibility_explanations`。

### `apps/client/src/application.ts::mountWinWinCodeClient`

构造捕获记录，字段按源码次序为「chat ← '&lt;path d="M11 4H5a1 1 0 0 0-1 1v13a1 1 0 0 0 1 1h13a1 1 0 0 0 1-1v-6"/&gt;&lt;path d="M17.5 3.5a2.1 2.1 0 0 1 3 3L12 15l-4 1 1-4Z"/&gt;'；home ← '&lt;rect x="4" y="4" width="7" height="7"/&gt;&lt;rect x="13" y="4" width="7" height="7"/&gt;&lt;rect x="4" y="13" width="7" height="7"/&gt;&lt;rect x="13" y="13" width="7" height=…［展示截断；完整操作保留］；projects ← '&lt;path d="M3 6h6l2 2h10v11H3z"/&gt;'；extensions ← '&lt;path d="M10 4h4v3a2 2 0 1 0 4 0h3v4h-3a2 2 0 1 0 0 4h3v4h-4v-3a2 2 0 1 0-4 0v3H6v-4H4v-4h3a2 2 0 1 0 0-4H4V4h6z"/&gt;'；device ← '&lt;rect x="3" y="4" width="18" height="12"/&gt;&lt;path d="M9 20h6M12 16v4"/&gt;'；settings ← '&lt;circle cx="12" cy="12" r="3"/&gt;&lt;path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M18.4 5.6l-2.1 2.1M7.7 16.3l-2.1 2.1"/&gt;'」。不据构造形式推断物理持久化。 将「{\n    serverUrl: options.serverUrl,\n    transport: browserTransport,\n    onAccessFailure(error) {\n      accessFailureSession?.authenticationRequired(error)\n    },\n  }」作为第 1 个实参交给已绑定接口「ts:apps/client/src/community-control-plane-client#createControlPlaneClient」，对应捕获形参「options: ControlPlaneClientOptions」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「text.textContent = surface.label」，捕获目标为「text.textContent」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「document」的初始化来源为「options.root.ownerDocument」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「accessFailureSession」存在源更新「accessFailureSession = authSession」；循环和分支条件见操作上下文，未推执行次数或最终数值。 以「return {\n    controlPlane,\n    authSession,\n    connection,\n    surfaces: CLIENT_SURFACES,\n    get activeSurface() {\n      return activeSurface\n    },\n    navigate(surfaceId) {\n      if (closed) throw new Error('WinWinCode Client is closed.')\n      const surface = CLIENT_SURFACES.find(candidate =&gt; candidate.id === surfaceId)\n      if (surface === …［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「now」关联路径「now」；只描述捕获来源，不证明当时的字段值。 将「{\n    client: rawControlPlane,\n    monitor: connection,\n    online: browserIsOnline,\n    onAuthorizationRevoked() { onRouteAuthorizationRevoked?.() },\n  }」作为第 1 个实参交给已绑定接口「ts:apps/client/src/core/connection-state#observeControlPlaneClient」，对应捕获形参「options: ObserveControlPlaneClientOptions」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:190`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/0`。

### `apps/client/src/application.ts::mountWinWinCodeClient.&lt;arrow@196:30&gt;`

以无显式实参的调用形式「Date」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/application.ts:196`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/1`。

### `apps/client/src/application.ts::mountWinWinCodeClient.browserIsOnline`

在调用形式「Reflect.get」中提供第 1 个实参「browser」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「navigatorValue」的初始化来源为「Reflect.get(browser, 'navigator') as Navigator | undefined」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return navigatorValue?.onLine !== false」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「b035747116438c86c32be8a2」先于语句位置「1」的操作「9d6c89cd6c8858ba3ad3f825」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:198`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/2`。

### `apps/client/src/application.ts::mountWinWinCodeClient.&lt;object@205:75&gt;.onAccessFailure`

在调用形式「accessFailureSession?.authenticationRequired」中提供第 1 个实参「error」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`apps/client/src/application.ts:208`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/3`。

### `apps/client/src/application.ts::mountWinWinCodeClient.&lt;object@212:57&gt;.onAuthorizationRevoked`

以无显式实参的调用形式「onRouteAuthorizationRevoked」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/application.ts:216`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/4`。

### `apps/client/src/application.ts::mountWinWinCodeClient.recordHomeVisit`

将「hash」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/scope-context#scopeSelectionFromHash」，对应捕获形参「hash: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「path」的初始化来源为「hash.slice(0, hash.indexOf('?') &lt; 0 ? hash.length : hash.indexOf('?'))」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(path !== '#/home/task-run')」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「008c84ecac1b7987f8fb9540」先于语句位置「1」的操作「886e6702b061a20740a1b33d」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:269`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/5`。

### `apps/client/src/application.ts::mountWinWinCodeClient.&lt;object@278:33&gt;.actor`

以无显式实参的调用形式「authenticatedRouteContext」调用已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.authenticatedRouteContext」；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/application.ts:280`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/6`。

### `apps/client/src/application.ts::mountWinWinCodeClient.&lt;object@278:33&gt;.scope`

以无显式实参的调用形式「authenticatedRouteContext」调用已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.authenticatedRouteContext」；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/application.ts:281`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/7`。

### `apps/client/src/application.ts::mountWinWinCodeClient.&lt;object@278:33&gt;.nextRequestId`

将「browser.crypto」作为第 2 个实参交给已绑定接口「ts:apps/client/src/application#contractId」，对应捕获形参「crypto: Crypto」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:282`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/8`。

### `apps/client/src/application.ts::mountWinWinCodeClient.&lt;object@278:33&gt;.nextWorkItemId`

将「browser.crypto」作为第 2 个实参交给已绑定接口「ts:apps/client/src/application#contractId」，对应捕获形参「crypto: Crypto」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:283`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/9`。

### `apps/client/src/application.ts::mountWinWinCodeClient.&lt;object@278:33&gt;.deliveryContext`

构造捕获记录，字段按源码次序为「actor ← context.actor；scope ← context.scope；requestId ← contractId('req', browser.crypto) as RequestId；workItemId ← null；deliveryId ← deliveryId」。不据构造形式推断物理持久化。 以无显式实参的调用形式「authenticatedRouteContext」调用已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.authenticatedRouteContext」；没有据调用存在断言激活、存储或网络效果。 捕获 binding「context」的初始化来源为「authenticatedRouteContext()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(context === null || deliveryId === null)」的捕获提前退出分支为「return：null」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return null」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「context.actor」关联路径「context.actor」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「de632488c67900a639e9371c」先于语句位置「1」的操作「75854785f12440f0a9fea486」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:285`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/10`。

### `apps/client/src/application.ts::mountWinWinCodeClient.&lt;object@307:33&gt;.nextTaskId`

将「browser.crypto」作为第 2 个实参交给已绑定接口「ts:apps/client/src/application#contractId」，对应捕获形参「crypto: Crypto」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:308`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/11`。

### `apps/client/src/application.ts::mountWinWinCodeClient.selectionIdentity`

在调用形式「[\n      selection.organizationId ?? '',\n      selection.workspaceId ?? '',\n      selection.projectId ?? '',\n      selection.repositoryId ?? '',\n    ].join」中提供第 1 个实参「'\u0000'」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return [\n      selection.organizationId ?? '',\n      selection.workspaceId ?? '',\n      selection.projectId ?? '',\n      selection.repositoryId ?? '',\n    ].join('\u0000')」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`apps/client/src/application.ts:347`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/12`。

### `apps/client/src/application.ts::mountWinWinCodeClient.diagnosticScope`

将「session.authorizedScopes」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/scope-context#resolveScopeContext」，对应捕获形参「scopes: readonly Scope[]」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「session」的初始化来源为「authSession.state.session」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「lastKnownDiagnosticScope」存在源更新「lastKnownDiagnosticScope = scope」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(session === null)」的捕获提前退出分支为「return：lastKnownDiagnosticScope」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return lastKnownDiagnosticScope」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「0ce228c6380c8fca046071f9」先于语句位置「1」的操作「b94ee007243e8e8381d5b3b0」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:356`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/13`。

### `apps/client/src/application.ts::mountWinWinCodeClient.diagnosticText`

构造捕获记录，字段按源码次序为「connection ← state；failure ← failure；scope ← diagnosticScope()；surface ← activeSurface.id；generatedAt ← now()」。不据构造形式推断物理持久化。 以无显式实参的调用形式「diagnosticScope」调用已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.diagnosticScope」；没有据调用存在断言激活、存储或网络效果。 以「return createSafeDiagnostic({\n      connection: state,\n      failure,\n      scope: diagnosticScope(),\n      surface: activeSurface.id,\n      generatedAt: now(),\n    })」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「state」关联路径「state」；只描述捕获来源，不证明当时的字段值。

源码：`apps/client/src/application.ts:369`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/14`。

### `apps/client/src/application.ts::mountWinWinCodeClient.copyDiagnostic`

在调用形式「options.copyText」中提供第 1 个实参「value」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「clipboard」的初始化来源为「navigatorValue?.clipboard」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(options.copyText !== undefined)」的捕获提前退出分支为「return：options.copyText(value)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return options.copyText(value)」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「287587e7e049b3d0c12fcf52」先于语句位置「1」的操作「c2f42191125c81cc339a417c」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:382`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/15`。

### `apps/client/src/application.ts::mountWinWinCodeClient.recoverConnection`

以无显式实参的调用形式「returnToSafeEntry」调用已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.returnToSafeEntry」；没有据调用存在断言激活、存储或网络效果。 捕获 binding「status」的初始化来源为「connection.state.status」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(status === 'authentication-required')」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「dea12f29356d6b5964cd6b4c」先于语句位置「1」的操作「fc5e55cafeeb2163e7397950」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 以无显式实参的调用形式「render」调用已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.render」；没有据调用存在断言激活、存储或网络效果。 以无显式实参的调用形式「browserIsOnline」调用已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.browserIsOnline」；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/application.ts:390`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/16`。

### `apps/client/src/application.ts::mountWinWinCodeClient.retryFailedRoute`

以无显式实参的调用形式「render」调用已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.render」；没有据调用存在断言激活、存储或网络效果。 对捕获 binding「currentFailure」存在源更新「currentFailure = null」；循环和分支条件见操作上下文，未推执行次数或最终数值。 保留同一块中的正常源码顺序：语句位置「0」的操作「ff6fa0713eb1b0481d6f081a」先于语句位置「1」的操作「76e488bf93493b366edeb43a」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:414`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/17`。

### `apps/client/src/application.ts::mountWinWinCodeClient.returnToSafeEntry`

将「surfaceHash('/chat', scopeSelectionFromHash(browser.location.hash))」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.replaceHash」，对应捕获形参「hash: string」。该普通调用关系不替代进程或网络协议关系。 对捕获 binding「currentFailure」存在源更新「currentFailure = null」；循环和分支条件见操作上下文，未推执行次数或最终数值。 保留同一块中的正常源码顺序：语句位置「0」的操作「a9a21c8021b8ca1d74503ee3」先于语句位置「1」的操作「2f97f76ef8216a990b1fe19a」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 以无显式实参的调用形式「render」调用已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.render」；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/application.ts:420`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/18`。

### `apps/client/src/application.ts::mountWinWinCodeClient.updateReliabilityViews`

构造捕获记录，字段按源码次序为「failure ← currentFailure；diagnostic ← diagnosticText(state)；onRetry ← retryFailedRoute；onSafeEntry ← returnToSafeEntry；onCopy ← copyDiagnostic」。不据构造形式推断物理持久化。 将「state」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.diagnosticText」，对应捕获形参「state: ConnectionSnapshot = connection.state」。该普通调用关系不替代进程或网络协议关系。 以字段投影形式「state」关联路径「state」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「2f680f7439aff61ef5496ce1」先于语句位置「1」的操作「b8644048294b54d9a9f3b7b8」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:447`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/19`。

### `apps/client/src/application.ts::mountWinWinCodeClient.applyFailureStatus`

在调用形式「connection.authenticationRequired」中提供第 1 个实参「failure.code」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`apps/client/src/application.ts:463`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/20`。

### `apps/client/src/application.ts::mountWinWinCodeClient.showRouteFailure`

将「currentFailure」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.applyFailureStatus」，对应捕获形参「failure: ClientFailure」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「slot.hidden = true」，捕获目标为「slot.hidden」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「failure」的初始化来源为「classifyClientFailure(\n      error,\n      fallbackCode,\n      browserIsOnline(),\n    )」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「currentFailure」存在源更新「currentFailure = failure」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「9d312f52a07d688ff55d72ce」先于语句位置「1」的操作「565b3244ec0901c4597ed1ce」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「connection.state」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.updateReliabilityViews」，对应捕获形参「state: ConnectionSnapshot」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:479`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/21`。

### `apps/client/src/application.ts::mountWinWinCodeClient.clearRouteFailure`

将「connection.state」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.updateReliabilityViews」，对应捕获形参「state: ConnectionSnapshot」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「slot.hidden = false」，捕获目标为「slot.hidden」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 对捕获 binding「currentFailure」存在源更新「currentFailure = null」；循环和分支条件见操作上下文，未推执行次数或最终数值。 保留同一块中的正常源码顺序：语句位置「0」的操作「f1f47788a3692402e8c81c8b」先于语句位置「1」的操作「a18c2438074c781b43c719b0」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:493`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/22`。

### `apps/client/src/application.ts::mountWinWinCodeClient.&lt;arrow@513:37&gt;`

以无显式实参的调用形式「event.preventDefault」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。 保留同一块中的正常源码顺序：语句位置「0」的操作「ccec009032476b5ef680d3c6」先于语句位置「1」的操作「52f6bbb7246eb8c71dae92d9」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:513`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/23`。

### `apps/client/src/application.ts::mountWinWinCodeClient.&lt;loop@528:2&gt;.&lt;block@528:41&gt;.&lt;arrow@540:35&gt;`

在调用形式「link.getAttribute」中提供第 1 个实参「'aria-disabled'」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 条件「(link.getAttribute('aria-disabled') !== 'true')」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「87350fee035cccac8341cb1e」先于语句位置「1」的操作「2715a9d8038f27912548de0c」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:540`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/24`。

### `apps/client/src/application.ts::mountWinWinCodeClient.&lt;arrow@560:45&gt;`

在调用形式「String」中提供第 1 个实参「expanded」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「expanded」的初始化来源为「header.classList.toggle('wwc-header-expanded')」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留同一块中的正常源码顺序：语句位置「0」的操作「3eb6d5b025c42cb3f3ca28be」先于语句位置「1」的操作「b35ca7c60f877988a8a1629f」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:560`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/25`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderRecentChats`

构造捕获记录，字段按源码次序为「sessions ← historySessions；loading ← historyLoading；error ← historyError；currentId ← routeParameters(browser.location.hash).get('session')；href ← session =&gt; {\n        const params = new URLSearchParams({ session: session.id })\n        if (session.deviceContext !== undefined) {\n          params.set('cli…［展示截断；完整操作保留］；refresh ← () =&gt; { void refreshRecentChats(true) }」。不据构造形式推断物理持久化。 将「browser.location.hash」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#routeParameters」，对应捕获形参「hash: string」。该普通调用关系不替代进程或网络协议关系。 以字段投影形式「historySessions」关联路径「historySessions」；只描述捕获来源，不证明当时的字段值。

源码：`apps/client/src/application.ts:570`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/26`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderRecentChats.&lt;object@571:26&gt;.href`

构造捕获记录，字段按源码次序为「session ← session.id」。不据构造形式推断物理持久化。 将「browser.location.hash」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/scope-context#scopeSelectionFromHash」，对应捕获形参「hash: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「params」的初始化来源为「new URLSearchParams({ session: session.id })」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return surfaceHash(`/chat?${params}`, scopeSelectionFromHash(browser.location.hash))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「session.id」关联路径「session.id」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「baead6ce0fa535a61397c6b5」先于语句位置「1」的操作「9722eafb6e3228077a0ecb2b」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:574`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/27`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderRecentChats.&lt;object@571:26&gt;.refresh`

将「true」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.refreshRecentChats」，对应捕获形参「force = false」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:582`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/28`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderRecentChats.&lt;object@571:26&gt;.update`

构造捕获记录，字段按源码次序为「productSessionId ← session.id；title ← title；archived ← archived」。不据构造形式推断物理持久化。 将「true」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.refreshRecentChats」，对应捕获形参「force = false」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「context」的初始化来源为「authenticatedRouteContext()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(context === null)」的捕获提前退出分支为「throw：new Error('请先登录')」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new Error('请先登录')」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「CommandName.SessionUpdate」关联路径「CommandName.SessionUpdate」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「context」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。 以无显式实参的调用形式「authenticatedRouteContext」调用已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.authenticatedRouteContext」；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/application.ts:583`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/29`。

### `apps/client/src/application.ts::mountWinWinCodeClient.refreshRecentChats`

构造捕获记录，字段按源码次序为「schemaVersion ← 'winwincode/v1'；actor ← session.actor；scope ← scope；requestId ← contractId('req', browser.crypto) as RequestId；query ← QueryName.SessionList；parameters ← { states: [] }；page ← { cursor, limit: 200 }」。不据构造形式推断物理持久化。 以无显式实参的调用形式「renderRecentChats」调用已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.renderRecentChats」；没有据调用存在断言激活、存储或网络效果。 包含赋值/更新「recentChatsRoot.hidden = true」，捕获目标为「recentChatsRoot.hidden」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「session」的初始化来源为「authSession.state.session」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「historySessions」存在源更新「historySessions = rows」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(response.query !== QueryName.SessionList)」的捕获提前退出分支为「throw：new Error('对话读取失败')」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

条件「(session === null || scope === null)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。

源码：`apps/client/src/application.ts:596`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/30`。

### `apps/client/src/application.ts::mountWinWinCodeClient.&lt;arrow@630:43&gt;`

将「true」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.refreshRecentChats」，对应捕获形参「force = false」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:630`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/31`。

### `apps/client/src/application.ts::mountWinWinCodeClient.&lt;object@658:52&gt;.now`

在调用形式「Date.parse」中提供第 1 个实参「now()」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`apps/client/src/application.ts:662`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/32`。

### `apps/client/src/application.ts::mountWinWinCodeClient.&lt;object@658:52&gt;.onDeviceSelect`

在调用形式「repositoriesModel.showDevice」中提供第 1 个实参「clientId」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`apps/client/src/application.ts:663`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/33`。

### `apps/client/src/application.ts::mountWinWinCodeClient.updateClientsVisibility`

在调用形式「clientsPage.setVisible」中提供第 1 个实参「visible」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「visible」的初始化来源为「status === 'signed-in'」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「clientsVisible」存在源更新「clientsVisible = visible」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(clientsVisible === visible)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「11403ce281a1f83cae3a7278」先于语句位置「1」的操作「ebea753f0c22f43f43026ae3」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:679`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/34`。

### `apps/client/src/application.ts::mountWinWinCodeClient.updateLoginVisibility`

将「status」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.updateClientsVisibility」，对应捕获形参「status: AuthSessionViewModel['state']['status']」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「status」的初始化来源为「authSession.state.status」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「loginVisible」存在源更新「loginVisible = visible」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(loginVisible === visible)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「515a88a6ad14fa691cd4805d」先于语句位置「1」的操作「0bd4ec672c91994d7dbb38d7」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:692`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/35`。

### `apps/client/src/application.ts::mountWinWinCodeClient.&lt;arrow@710:53&gt;`

以无显式实参的调用形式「authSession.restore」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/application.ts:710`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/36`。

### `apps/client/src/application.ts::mountWinWinCodeClient.readinessFixTarget`

构造捕获记录，字段按源码次序为「href ← surfaceHash('/settings', selection)；label ← '打开设置'」。不据构造形式推断物理持久化。 将「browser.location.hash」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/scope-context#scopeSelectionFromHash」，对应捕获形参「hash: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「resolution」的初始化来源为「currentScopeResolution」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(item.id === 'model-route' || item.id === 'credential-reference')」的捕获提前退出分支为「return：{ href: surfaceHash('/settings', selection), label: '打开设置' }」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return { href: surfaceHash('/settings', selection), label: '打开设置' }」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「a5acc656f1a3835393822072」先于语句位置「1」的操作「d88bf3bafb37cfdfd0556b82」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:716`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/37`。

### `apps/client/src/application.ts::mountWinWinCodeClient.&lt;object@741:45&gt;.nextRequestId`

将「browser.crypto」作为第 2 个实参交给已绑定接口「ts:apps/client/src/application#contractId」，对应捕获形参「crypto: Crypto」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:745`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/38`。

### `apps/client/src/application.ts::mountWinWinCodeClient.updateNavigation`

将「authSession.state」作为第 1 个实参交给已绑定接口「ts:apps/client/src/navigation-capability#projectionForSession」，对应捕获形参「state: Pick&lt;AuthSessionViewModelState, 'status' | 'session'&gt;」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「link.dataset.capability = entry.capability」，捕获目标为「link.dataset.capability」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「link」的初始化来源为「links.get(entry.surface.id)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「text」存在源更新「text = link.lastElementChild as HTMLElement | null ?? link」；循环和分支条件见操作上下文，未推执行次数或最终数值。 以「return projection」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「4fb352855b0343e43e127fde」先于语句位置「1」的操作「a3d23a3b11c7765770bf1830」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:753`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/39`。

### `apps/client/src/application.ts::mountWinWinCodeClient.routeDenied`

将「browser.location.hash」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/scope-context#scopeSelectionFromHash」，对应捕获形参「hash: string」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「denied.dataset.capability = capability.capability」，捕获目标为「denied.dataset.capability」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「denied」的初始化来源为「element(document, 'div', 'wwc-surface-route-denied')」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留同一块中的正常源码顺序：语句位置「0」的操作「6e2ade09bfeaddaedddda1c4」先于语句位置「1」的操作「a11d8d8e87f9e6148f8b5411」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:800`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/40`。

### `apps/client/src/application.ts::mountWinWinCodeClient.&lt;arrow@813:32&gt;`

构造捕获记录，字段按源码次序为「capability ← 'disabled'；reason ← 'capability-denied'」。不据构造形式推断物理持久化。 将「{\n      ...current,\n      capability: 'disabled',\n      reason: 'capability-denied',\n    }」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.routeDenied」，对应捕获形参「capability: SurfaceCapability」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「scopeNotice.textContent = '此范围的授权已被撤销。请返回安全入口并恢复访问。'」，捕获目标为「scopeNotice.textContent」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「link」的初始化来源为「links.get(activeSurface.id)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「revokedScopeIdentity」存在源更新「revokedScopeIdentity = selectionIdentity(currentScopeResolution.selection)」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 将「currentScopeResolution.selection」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.selectionIdentity」，对应捕获形参「selection: ScopeRouteSelection」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:813`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/41`。

### `apps/client/src/application.ts::mountWinWinCodeClient.closeAttentionMonitor`

以无显式实参的调用形式「attentionMonitor?.close」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。 对捕获 binding「attentionMonitor」存在源更新「attentionMonitor = null」；循环和分支条件见操作上下文，未推执行次数或最终数值。 保留同一块中的正常源码顺序：语句位置「0」的操作「bda446355e4248d35e5d41e6」先于语句位置「1」的操作「4a5ddabb15f9528400e63ee8」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:844`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/42`。

### `apps/client/src/application.ts::mountWinWinCodeClient.ensureAttentionMonitor`

构造捕获记录，字段按源码次序为「organizationId ← scope.organizationId；workspaceId ← scope.workspaceId；projectId ← scope.projectId；repositoryId ← scope.repositoryId」。不据构造形式推断物理持久化。 将「{\n      organizationId: scope.organizationId,\n      workspaceId: scope.workspaceId,\n      projectId: scope.projectId,\n      repositoryId: scope.repositoryId,\n    }」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.selectionIdentity」，对应捕获形参「selection: ScopeRouteSelection」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「identity」的初始化来源为「selectionIdentity({\n      organizationId: scope.organizationId,\n      workspaceId: scope.workspaceId,\n      projectId: scope.projectId,\n      repositoryId: scope.repositoryId,\n    })」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「attentionMonitor」存在源更新「attentionMonitor = monitor」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(attentionMonitor !== null &amp;&amp; attentionMonitorScope === identity)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「scope.organizationId」关联路径「scope.organizationId」；只描述捕获来源，不证明当时的字段值。 以无显式实参的调用形式「closeAttentionMonitor」调用已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.closeAttentionMonitor」；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/application.ts:855`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/43`。

### `apps/client/src/application.ts::mountWinWinCodeClient.ensureAttentionMonitor.&lt;object@872:69&gt;.nextRequestId`

将「browser.crypto」作为第 2 个实参交给已绑定接口「ts:apps/client/src/application#contractId」，对应捕获形参「crypto: Crypto」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:876`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/44`。

### `apps/client/src/application.ts::mountWinWinCodeClient.ensureAttentionMonitor.&lt;object@872:69&gt;.onOpenTarget`

以无显式实参的调用形式「render」调用已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.render」；没有据调用存在断言激活、存储或网络效果。 包含赋值/更新「browser.location.hash = hash」，捕获目标为「browser.location.hash」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 条件「(closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「07e52007bb1f758b2c72a135」先于语句位置「1」的操作「452f21c7fee8bf8969232999」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:880`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/45`。

### `apps/client/src/application.ts::mountWinWinCodeClient.ensureAttentionMonitor.&lt;arrow@886:22&gt;`

以无显式实参的调用形式「updateNavigation」调用已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.updateNavigation」；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/application.ts:886`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/46`。

### `apps/client/src/application.ts::mountWinWinCodeClient.authenticatedRouteContext`

构造捕获记录，字段按源码次序为「actor ← session.actor；scope ← scope」。不据构造形式推断物理持久化。 将「document」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#element」，对应捕获形参「document: Document」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「unavailable.textContent = authSession.state.status === 'restoring'\n        ? '正在恢复登录状态…'\n        : resolution?.status === 'denied'\n          ? 'URL 中的仓库范围未获授权，请选择其他范围。'\n          : resolution?.status === 'selection-required'\n            ? '选择一个已授权的仓库范围以打开工作区。'\n            : authSession.state.status === 'signed-in' &amp;&amp; session !== null\n              ? '…［展示截断；完整操作保留］」，捕获目标为「unavailable.textContent」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「session」的初始化来源为「authSession.state.session」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(authSession.state.status !== 'signed-in' || session === null || scope === null)」的捕获提前退出分支为「return：null」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return null」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「session.actor」关联路径「session.actor」；只描述捕获来源，不证明当时的字段值。

源码：`apps/client/src/application.ts:892`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/47`。

### `apps/client/src/application.ts::mountWinWinCodeClient.routeLoading`

将「document」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#element」，对应捕获形参「document: Document」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「loading.textContent = message」，捕获目标为「loading.textContent」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「loading」的初始化来源为「element(document, 'p', 'wwc-feature-route-loading')」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留同一块中的正常源码顺序：语句位置「0」的操作「d95f8ac3d66e72f3e11ceec6」先于语句位置「1」的操作「2912a46dac64ac16233a76cf」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:922`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/48`。

### `apps/client/src/application.ts::mountWinWinCodeClient.routeUnavailable`

将「document」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#element」，对应捕获形参「document: Document」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「unavailable.textContent = message」，捕获目标为「unavailable.textContent」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「unavailable」的初始化来源为「element(document, 'p', 'wwc-feature-route-unavailable')」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留同一块中的正常源码顺序：语句位置「0」的操作「234e78b8fbaf92d3cf6182ed」先于语句位置「1」的操作「ea63927d2e1919ab4e832378」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:929`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/49`。

### `apps/client/src/application.ts::mountWinWinCodeClient.replaceHash`

在调用形式「browser.history.replaceState」中提供第 1 个实参「null」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`apps/client/src/application.ts:936`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/50`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderChat`

构造捕获记录，字段按源码次序为「schemaVersion ← 'winwincode/v1'；requestId ← contractId('req', browser.crypto) as RequestId；actor ← context.actor；scope ← context.scope；query ← QueryName.SessionGet；parameters ← { productSessionId }；page ← { cursor: null, limit: 1 }」。不据构造形式推断物理持久化。 将「error」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.showRouteFailure」，对应捕获形参「error: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「chatPage」的初始化来源为「activeFeature」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「selectedClientId」存在源更新「selectedClientId = session.result.deviceContext.clientId」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(context === null)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「context.actor」关联路径「context.actor」；只描述捕获来源，不证明当时的字段值。 将「'正在加载新对话…'」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.routeLoading」，对应捕获形参「message: string」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:940`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/51`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderChat.&lt;block@946:8&gt;.&lt;object@997:40&gt;.launchDeviceSession`

构造捕获记录，字段按源码次序为「clientId ← input.clientId；repositoryBindingId ← input.repositoryBindingId；productSession ← { id: input.productSessionId, scope: context.scope }」。不据构造形式推断物理持久化。 在调用形式「clientOccupancy.claim」中提供第 1 个实参「{ clientId: input.clientId }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以字段投影形式「input.clientId」关联路径「input.clientId」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「9a330a9e09f3cc8b79173ade」先于语句位置「1」的操作「210191f2ea632340a8bae1f5」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:1003`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/52`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderChat.&lt;block@946:8&gt;.&lt;object@997:40&gt;.nextSubscriptionId`

将「browser.crypto」作为第 2 个实参交给已绑定接口「ts:apps/client/src/application#contractId」，对应捕获形参「crypto: Crypto」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1008`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/53`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderChat.&lt;block@946:8&gt;.&lt;object@997:40&gt;.nextRequestId`

将「browser.crypto」作为第 2 个实参交给已绑定接口「ts:apps/client/src/application#contractId」，对应捕获形参「crypto: Crypto」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1012`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/54`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderChat.&lt;block@946:8&gt;.&lt;object@997:40&gt;.onActiveSessionChange`

将「`#/chat?${parameters.toString()}`」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.replaceHash」，对应捕获形参「hash: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「parameters」的初始化来源为「routeParameters(browser.location.hash)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(closed || generation !== renderGeneration || controller.signal.aborted)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「83af67b90173726188bf5e22」先于语句位置「1」的操作「4c281a399e4b1e060fc76141」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:1013`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/55`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderChat.&lt;block@946:8&gt;.&lt;object@1023:56&gt;.nextDeliveryId`

将「browser.crypto」作为第 2 个实参交给已绑定接口「ts:apps/client/src/application#contractId」，对应捕获形参「crypto: Crypto」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1027`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/56`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderChat.&lt;block@946:8&gt;.&lt;object@1023:56&gt;.nextRequestId`

将「browser.crypto」作为第 2 个实参交给已绑定接口「ts:apps/client/src/application#contractId」，对应捕获形参「crypto: Crypto」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1028`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/57`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderChat.&lt;block@946:8&gt;.&lt;object@1033:36&gt;.listDeviceRepositories`

构造捕获记录，字段按源码次序为「clientId ← clientId」。不据构造形式推断物理持久化。 在调用形式「clientDirectory.listRepositories」中提供第 1 个实参「{ clientId }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以字段投影形式「clientId」关联路径「clientId」；只描述捕获来源，不证明当时的字段值。

源码：`apps/client/src/application.ts:1036`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/58`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderChat.&lt;block@946:8&gt;.&lt;object@1033:36&gt;.onProjectChange`

将「`#/chat?${parameters.toString()}`」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.replaceHash」，对应捕获形参「hash: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「parameters」的初始化来源为「routeParameters(browser.location.hash)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留同一块中的正常源码顺序：语句位置「0」的操作「f4c4fd3ff761a1e86d00ac27」先于语句位置「1」的操作「1bcefbea9362fba93a34991f」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:1038`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/59`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderChat.&lt;block@946:8&gt;.&lt;object@1033:36&gt;.&lt;object@1045:52&gt;.nextRequestId`

将「browser.crypto」作为第 2 个实参交给已绑定接口「ts:apps/client/src/application#contractId」，对应捕获形参「crypto: Crypto」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1047`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/60`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderChat.&lt;block@946:8&gt;.&lt;object@1033:36&gt;.nextProductSessionId`

将「browser.crypto」作为第 2 个实参交给已绑定接口「ts:apps/client/src/application#contractId」，对应捕获形参「crypto: Crypto」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1055`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/61`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderChat.&lt;block@946:8&gt;.&lt;arrow@1061:53&gt;`

将「true」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.refreshRecentChats」，对应捕获形参「force = false」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「session」的初始化来源为「state.session」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「lastHistoryRevision」存在源更新「lastHistoryRevision = identity」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(session === null)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「b5ffa62de81e98aa289c22c3」先于语句位置「1」的操作「7db4911c675d3537b5322766」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 以无显式实参的调用形式「renderRecentChats」调用已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.renderRecentChats」；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/application.ts:1061`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/62`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderChat.&lt;block@946:8&gt;.&lt;object@1072:22&gt;.close`

以无显式实参的调用形式「unsubscribeRecentChats」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。 保留同一块中的正常源码顺序：语句位置「0」的操作「58c3c1af2395fc2409a2b750」先于语句位置「1」的操作「f80153e1ee0c8c7a73234c72」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:1073`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/63`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderProjects`

构造捕获记录，字段按源码次序为「root ← slot；clientDirectory ← clientDirectory；registration ← createControlPlaneRepositoryRegistration({ serverUrl: controlPlane.serverUrl, transport: browserTransport })；managedAppTemplate ← createControlPlaneManagedAppTemplatePort({ serverUrl: controlPlane.serverUrl, transport: browserTransport })；newChatHref ← (clientId, repository) =&gt; scopeHash(`#/chat?${new URLSearchParams({\n          client: clientId,\n          repositoryBinding: repository.repositoryBindingId,\n…［展示截断；完整操作保留］；deviceHref ← '#/device'；requestOptions ← () =&gt; undefined」。不据构造形式推断物理持久化。 将「error」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.showRouteFailure」，对应捕获形参「error: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「context」的初始化来源为「authenticatedRouteContext()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「featureController」存在源更新「featureController = controller」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(context === null)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「slot」关联路径「slot」；只描述捕获来源，不证明当时的字段值。 将「'正在加载项目…'」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.routeLoading」，对应捕获形参「message: string」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1086`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/64`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderProjects.&lt;block@1092:8&gt;.&lt;object@1097:41&gt;.newChatHref`

构造捕获记录，字段按源码次序为「client ← clientId；repositoryBinding ← repository.repositoryBindingId」。不据构造形式推断物理持久化。 将「browser.location.hash」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/scope-context#scopeSelectionFromHash」，对应捕获形参「hash: string」。该普通调用关系不替代进程或网络协议关系。 以字段投影形式「clientId」关联路径「clientId」；只描述捕获来源，不证明当时的字段值。

源码：`apps/client/src/application.ts:1102`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/65`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderDevice`

构造捕获记录，字段按源码次序为「root ← slot；clientDirectory ← clientDirectory；homeHref ← '#/onboarding'；projectsHref ← '#/projects'；requestOptions ← () =&gt; undefined」。不据构造形式推断物理持久化。 将「error」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.showRouteFailure」，对应捕获形参「error: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「context」的初始化来源为「authenticatedRouteContext()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「featureController」存在源更新「featureController = controller」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(context === null)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「slot」关联路径「slot」；只描述捕获来源，不证明当时的字段值。 将「'正在加载执行设备…'」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.routeLoading」，对应捕获形参「message: string」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1116`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/66`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderExtensions`

构造捕获记录，字段按源码次序为「root ← slot；serverUrl ← controlPlane.serverUrl；fetch ← browserTransport.fetch」。不据构造形式推断物理持久化。 将「error」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.showRouteFailure」，对应捕获形参「error: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「controller」的初始化来源为「new AbortController()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「featureController」存在源更新「featureController = controller」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(authenticatedRouteContext() === null)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「slot」关联路径「slot」；只描述捕获来源，不证明当时的字段值。 将「'正在加载扩展…'」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.routeLoading」，对应捕获形参「message: string」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1141`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/67`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderSettings`

构造捕获记录，字段按源码次序为「root ← slot；serverUrl ← controlPlane.serverUrl；fetch ← browserTransport.fetch；model ← model；readOnly ← activeRouteReadOnly；mountUsagePanel ← async usageRoot =&gt; {\n          const [{ createUsageHealthViewModel }, { mountUsageHealthSummary }] = await Promise.all([\n            import('./usage-health-vi…［展示截断；完整操作保留］」。不据构造形式推断物理持久化。 将「error」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.showRouteFailure」，对应捕获形参「error: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「context」的初始化来源为「authenticatedRouteContext()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「featureController」存在源更新「featureController = controller」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(context === null)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「controlPlane」关联路径「controlPlane」；只描述捕获来源，不证明当时的字段值。 将「'正在加载设置…'」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.routeLoading」，对应捕获形参「message: string」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1158`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/68`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderSettings.&lt;block@1164:8&gt;.&lt;object@1170:44&gt;.nextRequestId`

将「browser.crypto」作为第 2 个实参交给已绑定接口「ts:apps/client/src/application#contractId」，对应捕获形参「crypto: Crypto」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1178`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/69`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderSettings.&lt;block@1164:8&gt;.&lt;object@1180:37&gt;.mountUsagePanel`

构造捕获记录，字段按源码次序为「client ← controlPlane；actor ← context.actor；scope ← context.scope；nextRequestId ← () =&gt; contractId('req', browser.crypto) as RequestId」。不据构造形式推断物理持久化。 在调用形式「createUsageHealthViewModel」中提供第 1 个实参「{\n            client: controlPlane,\n            actor: context.actor,\n            scope: context.scope,\n            nextRequestId: () =&gt; contractId('req', browser.crypto) as RequestId,\n          }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「healthModel」的初始化来源为「createUsageHealthViewModel({\n            client: controlPlane,\n            actor: context.actor,\n            scope: context.scope,\n            nextRequestId: () =&gt; contractId('req', browser.crypto) as RequestId,\n          })」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return {\n            close() {\n              healthSummary.close()\n              healthModel.close()\n            },\n          }」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「controlPlane」关联路径「controlPlane」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「ec18a2d6babcb7f86883287b」先于语句位置「1」的操作「e0ebf919760e5d4481661dc1」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:1189`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/70`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderSettings.&lt;block@1164:8&gt;.&lt;object@1180:37&gt;.mountUsagePanel.&lt;object@1194:57&gt;.nextRequestId`

将「browser.crypto」作为第 2 个实参交给已绑定接口「ts:apps/client/src/application#contractId」，对应捕获形参「crypto: Crypto」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1198`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/71`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderSettings.&lt;block@1164:8&gt;.&lt;object@1180:37&gt;.mountUsagePanel.&lt;object@1205:17&gt;.close`

以无显式实参的调用形式「healthSummary.close」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。 保留同一块中的正常源码顺序：语句位置「0」的操作「e5bfefd8abba40609cb8742d」先于语句位置「1」的操作「0cc253eae929a568eceb5655」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:1206`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/72`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderSettings.&lt;block@1164:8&gt;.&lt;object@1213:22&gt;.close`

以无显式实参的调用形式「page.close」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。 保留同一块中的正常源码顺序：语句位置「0」的操作「9a6fd3a012b9bc5f7d70b0cd」先于语句位置「1」的操作「74f02070ad88694f5d6dcc5c」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:1214`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/73`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderHome`

构造捕获记录，字段按源码次序为「client ← controlPlane；actor ← context.actor；scope ← context.scope；subscriptionId ← contractId(\n          'sub',\n          browser.crypto,\n        ) as ControlPlaneWebSocketSubscriptionId；nextRequestId ← () =&gt; contractId('req', browser.crypto) as RequestId；visits ← homeVisits；clients ← clientsModel」。不据构造形式推断物理持久化。 将「error」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.showRouteFailure」，对应捕获形参「error: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「context」的初始化来源为「authenticatedRouteContext()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「featureController」存在源更新「featureController = controller」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(context === null)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「controlPlane」关联路径「controlPlane」；只描述捕获来源，不证明当时的字段值。 将「'正在加载任务看板…'」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.routeLoading」，对应捕获形参「message: string」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1231`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/74`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderHome.&lt;block@1237:8&gt;.&lt;object@1243:42&gt;.nextRequestId`

将「browser.crypto」作为第 2 个实参交给已绑定接口「ts:apps/client/src/application#contractId」，对应捕获形参「crypto: Crypto」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1251`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/75`。

### `apps/client/src/application.ts::mountWinWinCodeClient.homeSubRoute`

在调用形式「browser.location.hash.replace(/^#/u, '').replace」中提供第 1 个实参「/\?.*$/u」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「path」的初始化来源为「browser.location.hash.replace(/^#/u, '').replace(/\?.*$/u, '')」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(path === '/home/new-task')」的捕获提前退出分支为「return：'task-entry'」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return 'task-entry'」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「4f7a796452a810370aefc874」先于语句位置「1」的操作「fd2d29b703f390c10a6b8e80」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:1272`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/76`。

### `apps/client/src/application.ts::mountWinWinCodeClient.taskRunRouteAnchor`

构造捕获记录，字段按源码次序为「taskId ← taskId as WorkItemId；deliveryId ← deliveryId as DeliveryId」。不据构造形式推断物理持久化。 将「browser.location.hash」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#routeParameters」，对应捕获形参「hash: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「parameters」的初始化来源为「routeParameters(browser.location.hash)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(\n      taskId === null || !matchesCanonicalSchema('WorkItemId', taskId)\n      || deliveryId === null || !matchesCanonicalSchema('DeliveryId', deliveryId)\n    )」的捕获提前退出分支为「return：null」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return null」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「taskId as WorkItemId」关联路径「taskId」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「4077664db6f2402dc83d789b」先于语句位置「1」的操作「eeedfcb90579c95604d93766」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:1285`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/77`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderTaskEntry`

构造捕获记录，字段按源码次序为「clients ← clientsModel；repositories ← repositoriesModel；port ← taskPort」。不据构造形式推断物理持久化。 将「error」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.showRouteFailure」，对应捕获形参「error: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「context」的初始化来源为「authenticatedRouteContext()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「featureController」存在源更新「featureController = controller」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(context === null)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「clientsModel」关联路径「clientsModel」；只描述捕获来源，不证明当时的字段值。 将「'正在加载新任务表单…'」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.routeLoading」，对应捕获形参「message: string」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1307`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/78`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderTaskEntry.&lt;block@1313:8&gt;.&lt;object@1324:41&gt;.onStarted`

构造捕获记录，字段按源码次序为「task ← anchor.taskId」。不据构造形式推断物理持久化。 将「scopeHash(\n            `#/home/run?${parameters.toString()}`,\n            scopeSelectionFromHash(browser.location.hash),\n          )」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.replaceHash」，对应捕获形参「hash: string」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「parameters」的初始化来源为「new URLSearchParams({\n            task: anchor.taskId,\n          })」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(closed || generation !== renderGeneration || controller.signal.aborted)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「anchor.taskId」关联路径「anchor.taskId」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「bf5b1484263ca0ea7751fba2」先于语句位置「1」的操作「f228b1b7a056509467b2e7a9」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 以无显式实参的调用形式「render」调用已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.render」；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/application.ts:1327`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/79`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderTaskRun`

构造捕获记录，字段按源码次序为「taskId ← anchorFacts.taskId；clientId ← ''；repositoryBindingId ← ''；baseBranch ← ''；description ← ''；modelRouteId ← ''」。不据构造形式推断物理持久化。 将「error」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.showRouteFailure」，对应捕获形参「error: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「context」的初始化来源为「authenticatedRouteContext()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「featureController」存在源更新「featureController = controller」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(context === null)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「anchorFacts.taskId」关联路径「anchorFacts.taskId」；只描述捕获来源，不证明当时的字段值。 将「'任务链接不完整。请从任务看板发起新任务，或在对话中委托任务。'」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.routeUnavailable」，对应捕获形参「message: string」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1352`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/80`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderTaskRun.&lt;block@1363:8&gt;.&lt;object@1378:43&gt;.&lt;object@1383:74&gt;.nextRequestId`

将「browser.crypto」作为第 2 个实参交给已绑定接口「ts:apps/client/src/application#contractId」，对应捕获形参「crypto: Crypto」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1389`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/81`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderTaskRun.&lt;block@1363:8&gt;.&lt;object@1378:43&gt;.candidatePreviewHref`

构造捕获记录，字段按源码次序为「delivery ← anchorFacts.deliveryId；task ← anchorFacts.taskId」。不据构造形式推断物理持久化。 将「browser.location.hash」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/scope-context#scopeSelectionFromHash」，对应捕获形参「hash: string」。该普通调用关系不替代进程或网络协议关系。 以字段投影形式「anchorFacts.deliveryId」关联路径「anchorFacts.deliveryId」；只描述捕获来源，不证明当时的字段值。

源码：`apps/client/src/application.ts:1391`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/82`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderDecisionClarification`

构造捕获记录，字段按源码次序为「client ← controlPlane；actor ← context.actor；scope ← context.scope；deliveryId ← deliveryId as DeliveryId；nextRequestId ← () =&gt; contractId('req', browser.crypto) as RequestId」。不据构造形式推断物理持久化。 将「error」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.showRouteFailure」，对应捕获形参「error: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「context」的初始化来源为「authenticatedRouteContext()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「featureController」存在源更新「featureController = controller」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(context === null)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「controlPlane」关联路径「controlPlane」；只描述捕获来源，不证明当时的字段值。 将「'需求编辑链接缺少有效的交付标识。请从任务页面重新打开。'」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.routeUnavailable」，对应捕获形参「message: string」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1421`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/83`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderDecisionClarification.&lt;block@1432:8&gt;.&lt;object@1439:49&gt;.&lt;object@1440:50&gt;.nextRequestId`

将「browser.crypto」作为第 2 个实参交给已绑定接口「ts:apps/client/src/application#contractId」，对应捕获形参「crypto: Crypto」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1445`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/84`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderDecisionClarification.&lt;block@1432:8&gt;.&lt;object@1439:49&gt;.nextRequestId`

将「browser.crypto」作为第 2 个实参交给已绑定接口「ts:apps/client/src/application#contractId」，对应捕获形参「crypto: Crypto」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1447`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/85`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderDecisionClarification.&lt;block@1432:8&gt;.&lt;object@1439:49&gt;.nextCriterionId`

将「browser.crypto」作为第 2 个实参交给已绑定接口「ts:apps/client/src/application#contractId」，对应捕获形参「crypto: Crypto」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1448`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/86`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderCandidateRunPreview`

构造捕获记录，字段按源码次序为「mode ← 'frozen-candidate' as const；clientId ← projection.clientId；sourceId ← previewRun.executionJobId；workRunId ← previewRun.id；repositoryBindingId ← projection.repositoryBindingId；taskId ← projection.taskId；attempt ← previewRun.attempt；candidateCommit ← projection.candidate.candidateCommitId；candidateTreeId ← projection.candidate.candidateTreeId；runConfigVersion ← projection.managedAppRunConfig?.schemaVersion ?? null」。不据构造形式推断物理持久化。 将「error」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.showRouteFailure」，对应捕获形参「error: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「routeContext」的初始化来源为「context」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「featureController」存在源更新「featureController = controller」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(context === null)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「taskId as WorkItemId」关联路径「taskId」；只描述捕获来源，不证明当时的字段值。 将「'预览链接只接受交付和任务锚点，请从运行中的任务重新打开。'」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.routeUnavailable」，对应捕获形参「message: string」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1468`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/87`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderCandidateRunPreview.&lt;block@1498:8&gt;.&lt;object@1520:61&gt;.nextRequestId`

将「browser.crypto」作为第 2 个实参交给已绑定接口「ts:apps/client/src/application#contractId」，对应捕获形参「crypto: Crypto」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1526`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/88`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderCandidateRunPreview.&lt;block@1498:8&gt;.&lt;object@1552:52&gt;.&lt;object@1553:53&gt;.runIdentityProjection`

在调用形式「identityPort.read」中提供第 1 个实参「anchor」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`apps/client/src/application.ts:1561`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/89`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderCandidateRunPreview.&lt;block@1498:8&gt;.&lt;object@1552:52&gt;.&lt;object@1553:53&gt;.occupancyStatus`

构造捕获记录，字段按源码次序为「clientId ← clientId」。不据构造形式推断物理持久化。 在调用形式「clientOccupancy.getStatus」中提供第 1 个实参「{ clientId }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以字段投影形式「clientId」关联路径「clientId」；只描述捕获来源，不证明当时的字段值。

源码：`apps/client/src/application.ts:1562`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/90`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderCandidateRunPreview.&lt;block@1498:8&gt;.&lt;object@1552:52&gt;.&lt;object@1553:53&gt;.nextRequestId`

将「browser.crypto」作为第 2 个实参交给已绑定接口「ts:apps/client/src/application#contractId」，对应捕获形参「crypto: Crypto」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1566`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/91`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderCandidateRunPreview.&lt;block@1498:8&gt;.&lt;object@1552:52&gt;.nextRequestId`

将「browser.crypto」作为第 2 个实参交给已绑定接口「ts:apps/client/src/application#contractId」，对应捕获形参「crypto: Crypto」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1568`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/92`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderCandidateRunPreview.&lt;block@1498:8&gt;.persistedAnnotation`

构造捕获记录，字段按源码次序为「id ← item.id；body ← item.body；candidateRef ← item.candidate.candidateRef；workRunId ← item.candidate.workRunId；target ← {\n            pagePath: item.target.pagePath,\n            viewport: item.target.viewport,\n            element: targetElement === null ? null : {\n           …［展示截断；完整操作保留］；updatedAt ← new Date(item.updatedAt).toISOString()」。不据构造形式推断物理持久化。 在调用形式「Date」中提供第 1 个实参「item.updatedAt」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「targetElement」的初始化来源为「item.target.element ?? null」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return {\n          id: item.id,\n          body: item.body,\n          candidateRef: item.candidate.candidateRef,\n          workRunId: item.candidate.workRunId,\n          target: {\n            pagePath: item.target.pagePath,\n            viewport: item.target.viewport,\n            element: targetElement === null ? null : {\n              tagName: target…［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「item.id」关联路径「item.id」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「fc51a5c0ceeac5d2aed54a3f」先于语句位置「1」的操作「389a4b921351bcf464b58185」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:1571`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/93`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderCandidateRunPreview.&lt;block@1498:8&gt;.annotationFacts`

构造捕获记录，字段按源码次序为「current ← current；contract ← contract；candidate ← candidate；attention ← attention；evidence ← evidence；candidateDigest ← candidateDigest」。不据构造形式推断物理持久化。 将「{\n          actor: routeContext.actor,\n          scope: routeContext.scope,\n          deliveryId: deliveryId as DeliveryId,\n          requestId: contractId('req', browser.crypto) as RequestId,\n        }」作为第 2 个实参交给已绑定接口「ts:apps/client/src/community-control-plane-client#queryDeliveryDetail」，对应捕获形参「input: Pick&lt;WorkRunAggregateQueryInput, 'actor' | 'scope' | 'requestId' | 'deliveryId'&gt;」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「contract」的初始化来源为「current.contract」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(current.deliveryId !== deliveryId || current.candidate === null || current.contract === null)」的捕获提前退出分支为「throw：new Error('当前候选身份已变化，请刷新预览后重试。')」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new Error('当前候选身份已变化，请刷新预览后重试。')」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「routeContext.actor」关联路径「routeContext.actor」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「abf79bb3809e848dcee5a1ac」先于语句位置「2」的操作「0c0d2ad9d15c486fa6d9613b」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:1598`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/94`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderCandidateRunPreview.&lt;block@1498:8&gt;.annotationTransport.list`

构造捕获记录，字段按源码次序为「schemaVersion ← 'winwincode/v1'；actor ← routeContext.actor；scope ← routeContext.scope；requestId ← contractId('req', browser.crypto) as RequestId；query ← QueryName.CollaborationPageAnnotationList；parameters ← { deliveryId: input.deliveryId as DeliveryId }；page ← { cursor, limit: 200 }」。不据构造形式推断物理持久化。 将「browser.crypto」作为第 2 个实参交给已绑定接口「ts:apps/client/src/application#contractId」，对应捕获形参「crypto: Crypto」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「items」的初始化来源为「[]」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「cursor」存在源更新「cursor = response.page.nextCursor」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(response.query !== QueryName.CollaborationPageAnnotationList)」的捕获提前退出分支为「throw：new Error('页面批注读取失败。')」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new Error('页面批注读取失败。')」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「routeContext.actor」关联路径「routeContext.actor」；只描述捕获来源，不证明当时的字段值。

源码：`apps/client/src/application.ts:1620`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/95`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderCandidateRunPreview.&lt;block@1498:8&gt;.annotationTransport.submit`

构造捕获记录，字段按源码次序为「deliveryId ← deliveryId as DeliveryId；deliverySpecId ← contract.id；deliverySpecRevision ← Number(contract.revision)；candidateRef ← candidate.candidateRef；candidateDigest ← candidateDigest；candidateTreeId ← candidate.candidateTreeId；diffSha256 ← candidate.diffSha256；workRunId ← current.workRun.id；attempt ← current.workRun.attempt；sessionBindingId ← evidence?.sessionBindingId ?? current.workRun.workerSessionId」。不据构造形式推断物理持久化。 将「completed.result.annotation」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.renderCandidateRunPreview.&lt;block@1498:8&gt;.persistedAnnotation」，对应捕获形参「item: CollaborationPageAnnotationProjection」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「draft」的初始化来源为「input.draft」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(response.command !== CommandName.CollaborationPageAnnotationSubmit\n            || !('result' in response))」的捕获提前退出分支为「throw：new Error('页面批注提交失败。')」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new Error('页面批注提交失败。')」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「draft.pagePath」关联路径「draft.pagePath」；只描述捕获来源，不证明当时的字段值。 记录消息形状中的固定文本字段「schemaVersion」及捕获形式「'winwincode/v1'」。单个文本字段不是跨语言调用或传输成功的证明。 以无显式实参的调用形式「annotationFacts」调用已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.renderCandidateRunPreview.&lt;block@1498:8&gt;.annotationFacts」；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/application.ts:1644`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/96`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderCandidateRunPreview.&lt;block@1498:8&gt;.&lt;object@1722:22&gt;.close`

以无显式实参的调用形式「page.close」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。 保留同一块中的正常源码顺序：语句位置「0」的操作「9243ce1d23e010e9f7a0d65f」先于语句位置「1」的操作「bc266e18c5b67c4e02b8a606」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:1722`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/97`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderReview`

构造捕获记录，字段按源码次序为「client ← controlPlane；actor ← context.actor；scope ← context.scope；deliveryId ← deliveryId；nextRequestId ← () =&gt; contractId('req', browser.crypto) as RequestId」。不据构造形式推断物理持久化。 将「error」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.showRouteFailure」，对应捕获形参「error: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「context」的初始化来源为「authenticatedRouteContext()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「featureController」存在源更新「featureController = controller」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(context === null)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「controlPlane」关联路径「controlPlane」；只描述捕获来源，不证明当时的字段值。 将「'审核链接缺少有效的交付标识。请从任务看板或对话中打开审核。'」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.routeUnavailable」，对应捕获形参「message: string」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1731`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/98`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderReview.&lt;block@1742:8&gt;.&lt;object@1751:52&gt;.nextRequestId`

将「browser.crypto」作为第 2 个实参交给已绑定接口「ts:apps/client/src/application#contractId」，对应捕获形参「crypto: Crypto」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1756`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/99`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderReview.&lt;block@1742:8&gt;.&lt;object@1758:47&gt;.&lt;object@1762:26&gt;.claim`

构造捕获记录，字段按源码次序为「clientId ← clientId」。不据构造形式推断物理持久化。 在调用形式「clientOccupancy.claim」中提供第 1 个实参「{ clientId }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以字段投影形式「clientId」关联路径「clientId」；只描述捕获来源，不证明当时的字段值。

源码：`apps/client/src/application.ts:1763`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/100`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderReview.&lt;block@1742:8&gt;.&lt;object@1758:47&gt;.onDownload`

构造捕获记录，字段按源码次序为「type ← mediaType」。不据构造形式推断物理持久化。 将「document」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#element」，对应捕获形参「document: Document」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「anchor.href = url」，捕获目标为「anchor.href」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「url」的初始化来源为「URL.createObjectURL(new Blob([Uint8Array.from(bytes)], { type: mediaType }))」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以字段投影形式「mediaType」关联路径「mediaType」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「557a02b6dd66de860e21b212」先于语句位置「1」的操作「e971b8daee9e6a882a2b9ab0」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:1765`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/101`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderReview.&lt;block@1742:8&gt;.&lt;object@1774:22&gt;.close`

以无显式实参的调用形式「page.close」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。 保留同一块中的正常源码顺序：语句位置「0」的操作「05c840700a01e8dc993c58fa」先于语句位置「1」的操作「f50caf4ec00366e52545db38」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:1774`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/102`。

### `apps/client/src/application.ts::mountWinWinCodeClient.performRender`

构造捕获记录，字段按源码次序为「status ← 'denied'；reason ← 'not-authorized'；selection ← resolved.selection；options ← resolved.options」。不据构造形式推断物理持久化。 将「resolved.selection」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.selectionIdentity」，对应捕获形参「selection: ScopeRouteSelection」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「main.dataset.surface = activeSurface.id」，捕获目标为「main.dataset.surface」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「generation」的初始化来源为「renderGeneration」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「currentScopeResolution」存在源更新「currentScopeResolution = resolution」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(routeAccessDenied)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 将「browser.location.hash」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.recordHomeVisit」，对应捕获形参「hash: string」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/application.ts:1782`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/103`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderOnboarding`

构造捕获记录，字段按源码次序为「root ← slot；connect ← async (clientId, connectionCode) =&gt; {\n          await clientDirectory.addClient({\n            clientId,\n            connectionCode,\n          })\n          …［展示截断；完整操作保留］；onSignOut ← () =&gt; { void authSession.logout() }」。不据构造形式推断物理持久化。 将「error」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.showRouteFailure」，对应捕获形参「error: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「page」的初始化来源为「null」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「activeFeature」存在源更新「activeFeature = page」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(closed || generation !== renderGeneration)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「slot」关联路径「slot」；只描述捕获来源，不证明当时的字段值。

源码：`apps/client/src/application.ts:1940`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/104`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderOnboarding.&lt;block@1946:8&gt;.&lt;object@1947:33&gt;.connect`

构造捕获记录，字段按源码次序为「organizationId ← currentScopeResolution?.status === 'selected'\n              &amp;&amp; currentScopeResolution.scope.kind === 'repository'\n              ? currentScopeResolution.scope…［展示截断；完整操作保留］；workspaceId ← currentScopeResolution?.status === 'selected'\n              &amp;&amp; currentScopeResolution.scope.kind === 'repository'\n              ? currentScopeResolution.scope…［展示截断；完整操作保留］；projectId ← currentScopeResolution?.status === 'selected'\n              &amp;&amp; currentScopeResolution.scope.kind === 'repository'\n                ? currentScopeResolution.sco…［展示截断；完整操作保留］；repositoryId ← currentScopeResolution?.status === 'selected'\n              &amp;&amp; currentScopeResolution.scope.kind === 'repository'\n              ? currentScopeResolution.scope…［展示截断；完整操作保留］」。不据构造形式推断物理持久化。 在调用形式「clientDirectory.addClient」中提供第 1 个实参「{\n            clientId,\n            connectionCode,\n          }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 包含赋值/更新「browser.location.hash = `#/device?${new URLSearchParams({\n            organizationId: currentScopeResolution?.status === 'selected'\n              &amp;&amp; currentScopeResolution.scope.kind === 'repository'\n              ? currentScopeResolution.scope.organizationId\n              : '',\n            workspaceId: currentScopeResolution?.status === 'selected'\n   …［展示截断；完整操作保留］」，捕获目标为「browser.location.hash」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 以字段投影形式「clientId」关联路径「clientId」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「27ab9a2be23ccf994893dcb8」先于语句位置「1」的操作「7cd620643ecaa7e2910243b6」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:1949`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/105`。

### `apps/client/src/application.ts::mountWinWinCodeClient.renderOnboarding.&lt;block@1946:8&gt;.&lt;object@1947:33&gt;.onSignOut`

以无显式实参的调用形式「authSession.logout」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/application.ts:1973`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/106`。

### `apps/client/src/application.ts::mountWinWinCodeClient.launchRoute`

在调用形式「operation.catch」中提供第 1 个实参「error =&gt; {\n      if (closed || generation !== renderGeneration) return\n      showRouteFailure(error, fallbackCode)\n    }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`apps/client/src/application.ts:1981`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/107`。

### `apps/client/src/application.ts::mountWinWinCodeClient.launchRoute.&lt;arrow@1986:25&gt;`

将「error」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.showRouteFailure」，对应捕获形参「error: unknown」。该普通调用关系不替代进程或网络协议关系。 条件「(closed || generation !== renderGeneration)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「05aeec2c1d868cdef1f984fe」先于语句位置「1」的操作「e6366926376e87108aa57e57」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:1986`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/108`。

### `apps/client/src/application.ts::mountWinWinCodeClient.render`

将「error」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.showRouteFailure」，对应捕获形参「error: unknown」。该普通调用关系不替代进程或网络协议关系。 以无显式实参的调用形式「performRender」调用已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.performRender」；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/application.ts:1992`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/109`。

### `apps/client/src/application.ts::mountWinWinCodeClient.onHashChange`

以无显式实参的调用形式「render」调用已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.render」；没有据调用存在断言激活、存储或网络效果。 保留同一块中的正常源码顺序：语句位置「0」的操作「b53b264e42afebbb6019ef19」先于语句位置「1」的操作「d165c08b43f6ca55e0141a62」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:2000`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/110`。

### `apps/client/src/application.ts::mountWinWinCodeClient.onOffline`

以无显式实参的调用形式「connection.offline」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/application.ts:2008`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/111`。

### `apps/client/src/application.ts::mountWinWinCodeClient.onFocus`

在调用形式「attentionMonitor?.refresh().catch」中提供第 1 个实参「() =&gt; {}」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`apps/client/src/application.ts:2010`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/112`。

### `apps/client/src/application.ts::mountWinWinCodeClient.onOnline`

在调用形式「queryCache.clear」中提供第 1 个实参「'reconnect'」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 保留同一块中的正常源码顺序：语句位置「0」的操作「ff5b6a02ec643b5341fb52f4」先于语句位置「1」的操作「d6109f2109e9a9893f8c52a9」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:2011`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/113`。

### `apps/client/src/application.ts::mountWinWinCodeClient.onWindowError`

将「event.error」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.showRouteFailure」，对应捕获形参「error: unknown」。该普通调用关系不替代进程或网络协议关系。 保留同一块中的正常源码顺序：语句位置「0」的操作「fba68b4dad549661198f3639」先于语句位置「1」的操作「f923816948b08a151a7e8146」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:2015`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/114`。

### `apps/client/src/application.ts::mountWinWinCodeClient.onUnhandledRejection`

将「event.reason」作为第 1 个实参交给已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.showRouteFailure」，对应捕获形参「error: unknown」。该普通调用关系不替代进程或网络协议关系。 保留同一块中的正常源码顺序：语句位置「0」的操作「294e226eaef751b8232dea7b」先于语句位置「1」的操作「725f95fa4ebce20fc72321f5」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:2019`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/115`。

### `apps/client/src/application.ts::mountWinWinCodeClient.&lt;arrow@2030:55&gt;`

以无显式实参的调用形式「updateLoginVisibility」调用已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.updateLoginVisibility」；没有据调用存在断言激活、存储或网络效果。 保留同一块中的正常源码顺序：语句位置「0」的操作「a795f21ce659d31302ca8104」先于语句位置「1」的操作「df4fb8ec255443672c11fe34」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 以无显式实参的调用形式「browserIsOnline」调用已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.browserIsOnline」；没有据调用存在断言激活、存储或网络效果。 以无显式实参的调用形式「diagnosticScope」调用已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.diagnosticScope」；没有据调用存在断言激活、存储或网络效果。 以无显式实参的调用形式「updateNavigation」调用已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.updateNavigation」；没有据调用存在断言激活、存储或网络效果。 以无显式实参的调用形式「render」调用已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.render」；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/application.ts:2030`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/116`。

### `apps/client/src/application.ts::mountWinWinCodeClient.&lt;object@2060:9&gt;.activeSurface`

以「return activeSurface」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`apps/client/src/application.ts:2065`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/117`。

### `apps/client/src/application.ts::mountWinWinCodeClient.&lt;object@2060:9&gt;.navigate`

以无显式实参的调用形式「render」调用已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.render」；没有据调用存在断言激活、存储或网络效果。 包含赋值/更新「browser.location.hash = surfaceHash(\n        surface.path,\n        scopeSelectionFromHash(browser.location.hash),\n      )」，捕获目标为「browser.location.hash」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「surface」的初始化来源为「CLIENT_SURFACES.find(candidate =&gt; candidate.id === surfaceId)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(closed)」的捕获提前退出分支为「throw：new Error('WinWinCode Client is closed.')」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new Error('WinWinCode Client is closed.')」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「5010be6d2bbdae1f8b94c083」先于语句位置「1」的操作「1009fbaa0ad6ddeac61d533f」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:2068`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/118`。

### `apps/client/src/application.ts::mountWinWinCodeClient.&lt;object@2060:9&gt;.close`

以无显式实参的调用形式「closeAttentionMonitor」调用已绑定接口「ts:apps/client/src/application#mountWinWinCodeClient.closeAttentionMonitor」；没有据调用存在断言激活、存储或网络效果。 对捕获 binding「closed」存在源更新「closed = true」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「8126943de8ec4eaeff801a0d」先于语句位置「1」的操作「9b135e1e4763bf9ac80bd335」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/application.ts:2078`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/119`。

### `apps/client/src/chat-delivery-creator.ts::createChatDeliveryCreator`

构造捕获记录，字段按源码次序为「status ← 'idle'；error ← null」。不据构造形式推断物理持久化。 在调用形式「Object.freeze」中提供第 1 个实参「{ status: 'idle', error: null }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「listeners」的初始化来源为「new Set&lt;(state: ChatDeliveryCreatorState) =&gt; void&gt;()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return {\n    get state() {\n      return currentState\n    },\n    subscribe(listener) {\n      listeners.add(listener)\n      listener(currentState)\n      return () =&gt; { listeners.delete(listener) }\n    },\n    async create(input) {\n      await create(input)\n    },\n    reset() {\n      if (closed || currentState.status !== 'created') return\n      att…［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「c8a145097c477d297cf6d7e2」先于语句位置「1」的操作「1a4d5db23397ab3fcaecdb1e」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/chat-delivery-creator.ts:123`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/120`。

### `apps/client/src/chat-delivery-creator.ts::createChatDeliveryCreator.publish`

构造捕获记录，字段按源码次序为「deliveryId ← attempt.created.deliveryId」。不据构造形式推断物理持久化。 在调用形式「Object.freeze」中提供第 1 个实参「{ status, error,\n      ...(attempt?.created === null || attempt === null ? {} : { deliveryId: attempt.created.deliveryId }),\n    }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 对捕获 binding「currentState」存在源更新「currentState = Object.freeze({ status, error,\n      ...(attempt?.created === null || attempt === null ? {} : { deliveryId: attempt.created.deliveryId }),\n    })」；循环和分支条件见操作上下文，未推执行次数或最终数值。 以字段投影形式「status」关联路径「status」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「(attempt?.created === null || attempt === null ? {} : { deliveryId: attempt.created.deliveryId })」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「8e8c711e9f9e306820c0bc1c」先于语句位置「1」的操作「6012711c6445aaec9f662bc1」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/chat-delivery-creator.ts:138`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/121`。

### `apps/client/src/chat-delivery-creator.ts::createChatDeliveryCreator.invalid`

将「'error'」作为第 1 个实参交给已绑定接口「ts:apps/client/src/chat-delivery-creator#createChatDeliveryCreator.publish」，对应捕获形参「status: ChatDeliveryCreatorState['status']」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/chat-delivery-creator.ts:145`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/122`。

### `apps/client/src/chat-delivery-creator.ts::createChatDeliveryCreator.completedDelivery`

将「response」作为第 1 个实参交给已绑定接口「ts:apps/client/src/chat-delivery-creator#expectCompletedCommand」，对应捕获形参「response: CommandAcceptedResponse | CommandCompletedResponse」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「completed」的初始化来源为「expectCompletedCommand(response, command, requestId)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(\n      !createdDeliveryMatchesScope(completed.result, deliveryId, options.scope)\n      || completed.result.revision !== completed.currentRevision\n    )」的捕获提前退出分支为「throw：clientFailure(\n      'STRONGFLOW_CREATE_RESPONSE_MISMATCH',\n      '交付命令返回了其他仓库修订版。',\n    )」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return null」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「2034b4afbe8fc9c6c7650b2c」先于语句位置「1」的操作「57db8297ac1d553b895b8016」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

条件「(completed === null)」的捕获提前退出分支为「return：null」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。

源码：`apps/client/src/chat-delivery-creator.ts:149`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/123`。

### `apps/client/src/chat-delivery-creator.ts::createChatDeliveryCreator.create`

构造捕获记录，字段按源码次序为「title ← title；goal ← goal；baseRevision ← baseRevision；deliveryScope ← deliveryScope；outOfScope ← outOfScope；constraints ← constraints；sourceProductSessionId ← input.sourceProductSessionId；acceptanceCriteria ← acceptanceCriteria；verificationCommand ← input.verificationCommand?.trim() ?? ''」。不据构造形式推断物理持久化。 将「{\n          actor: options.actor, scope: options.scope, requestId: options.nextRequestId(), deliveryId,\n          expectedRevision: currentAttempt.created.revision,\n          contractRevision: aggregate.contract.revision,\n          items: [{ id: deliveryId.replace(/^dlv_/u, 'wit_') as WorkItemId,\n            title, goal, criterionIds: aggregate.contract…［展示截断；完整操作保留］」作为第 1 个实参交给已绑定接口「ts:apps/client/src/community-control-plane-client#workItemsCreateCommand」，对应捕获形参「input: WorkItemsCreateInput」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「currentAttempt.created = created」，捕获目标为「currentAttempt.created」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「currentAttempt」的初始化来源为「attempt」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「active」存在源更新「active = controller」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(closed)」的捕获提前退出分支为「throw：clientFailure(\n      'STRONGFLOW_CREATE_VIEW_MODEL_CLOSED',\n      '交付创建视图已关闭。',\n    )」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw clientFailure(\n      'STRONGFLOW_CREATE_VIEW_MODEL_CLOSED',\n      '交付创建视图已关闭。',\n    )」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 将「createResponse」作为第 1 个实参交给已绑定接口「ts:apps/client/src/chat-delivery-creator#createChatDeliveryCreator.completedDelivery」，对应捕获形参「response: CommandAcceptedResponse | CommandCompletedResponse」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/chat-delivery-creator.ts:167`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/124`。

### `apps/client/src/chat-delivery-creator.ts::createChatDeliveryCreator.create.&lt;arrow@178:54&gt;`

以无显式实参的调用形式「value.trim」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/chat-delivery-creator.ts:178`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/125`。

### `apps/client/src/chat-delivery-creator.ts::createChatDeliveryCreator.create.&lt;arrow@179:56&gt;`

以无显式实参的调用形式「value.trim」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/chat-delivery-creator.ts:179`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/126`。

### `apps/client/src/chat-delivery-creator.ts::createChatDeliveryCreator.create.&lt;arrow@180:58&gt;`

以无显式实参的调用形式「value.trim」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/chat-delivery-creator.ts:180`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/127`。

### `apps/client/src/chat-delivery-creator.ts::createChatDeliveryCreator.create.&lt;arrow@182:11&gt;`

以无显式实参的调用形式「value.trim」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/chat-delivery-creator.ts:182`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/128`。

### `apps/client/src/chat-delivery-creator.ts::createChatDeliveryCreator.create.&lt;block@226:26&gt;.&lt;object@228:16&gt;.&lt;object@230:23&gt;.&lt;object@237:19&gt;.&lt;object@239:18&gt;.&lt;arrow@240:57&gt;`

构造捕获记录，字段按源码次序为「id ← `criterion:${String(index + 1)}`；required ← true；title ← criterion」。不据构造形式推断物理持久化。 在调用形式「String」中提供第 1 个实参「index + 1」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以字段投影形式「criterion」关联路径「criterion」；只描述捕获来源，不证明当时的字段值。

源码：`apps/client/src/chat-delivery-creator.ts:240`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/129`。

### `apps/client/src/chat-delivery-creator.ts::createChatDeliveryCreator.&lt;object@321:9&gt;.state`

以「return currentState」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`apps/client/src/chat-delivery-creator.ts:322`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/130`。

### `apps/client/src/chat-delivery-creator.ts::createChatDeliveryCreator.&lt;object@321:9&gt;.subscribe`

在调用形式「listeners.add」中提供第 1 个实参「listener」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return () =&gt; { listeners.delete(listener) }」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「4b1b548c2e75243e1cb8627f」先于语句位置「1」的操作「bbbb0b9af47d3a841d91a53c」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/chat-delivery-creator.ts:325`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/131`。

### `apps/client/src/chat-delivery-creator.ts::createChatDeliveryCreator.&lt;object@321:9&gt;.subscribe.&lt;arrow@328:13&gt;`

在调用形式「listeners.delete」中提供第 1 个实参「listener」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`apps/client/src/chat-delivery-creator.ts:328`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/132`。

### `apps/client/src/chat-delivery-creator.ts::createChatDeliveryCreator.&lt;object@321:9&gt;.create`

将「input」作为第 1 个实参交给已绑定接口「ts:apps/client/src/chat-delivery-creator#createChatDeliveryCreator.create」，对应捕获形参「input: ChatDeliveryCreateInput」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/chat-delivery-creator.ts:330`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/133`。

### `apps/client/src/chat-delivery-creator.ts::createChatDeliveryCreator.&lt;object@321:9&gt;.reset`

将「'idle'」作为第 1 个实参交给已绑定接口「ts:apps/client/src/chat-delivery-creator#createChatDeliveryCreator.publish」，对应捕获形参「status: ChatDeliveryCreatorState['status']」。该普通调用关系不替代进程或网络协议关系。 对捕获 binding「attempt」存在源更新「attempt = null」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(closed || currentState.status !== 'created')」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「bca509c4f5bf4c0ef928e45a」先于语句位置「1」的操作「3d99ad4f14604de6152e221f」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/chat-delivery-creator.ts:333`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/134`。

### `apps/client/src/chat-delivery-creator.ts::createChatDeliveryCreator.&lt;object@321:9&gt;.cancelPending`

构造捕获记录，字段按源码次序为「kind ← 'cancelled'；code ← 'REQUEST_CANCELLED'；message ← '交付创建已在本地取消。'；requestId ← null；retryable ← false」。不据构造形式推断物理持久化。 将「'error'」作为第 1 个实参交给已绑定接口「ts:apps/client/src/chat-delivery-creator#createChatDeliveryCreator.publish」，对应捕获形参「status: ChatDeliveryCreatorState['status']」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「controller」的初始化来源为「active」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「active」存在源更新「active = null」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 记录消息形状中的固定文本字段「kind」及捕获形式「'cancelled'」。单个文本字段不是跨语言调用或传输成功的证明。

源码：`apps/client/src/chat-delivery-creator.ts:338`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/135`。

### `apps/client/src/chat-delivery-creator.ts::createChatDeliveryCreator.&lt;object@321:9&gt;.close`

将「'closed'」作为第 1 个实参交给已绑定接口「ts:apps/client/src/chat-delivery-creator#createChatDeliveryCreator.publish」，对应捕获形参「status: ChatDeliveryCreatorState['status']」。该普通调用关系不替代进程或网络协议关系。 对捕获 binding「closed」存在源更新「closed = true」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「60a6c105f99fa3ec1034dd7b」先于语句位置「1」的操作「676725c3e708d8aed52bfd8f」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/chat-delivery-creator.ts:361`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/136`。

### `apps/client/src/community-control-plane-client.ts::createControlPlaneClient`

构造捕获记录，字段按源码次序为「generated ← generatedTransport」。不据构造形式推断物理持久化。 将「{\n    ...options,\n    generated: generatedTransport,\n  }」作为第 1 个实参交给已绑定接口「ts:packages/control-plane-client/src/index#createControlPlaneClient」，对应捕获形参「options: ControlPlaneClientOptions&lt;\n  ProductSession,\n  ProductCommandRequest,\n  ProductCommandResponse,\n  ProductQueryRequest,\n  ProductQueryResponse,\n  ProductEventFrame,\n  ProductResetFrame,\n  ProductAuthorizationRevokedFrame,\n  ProductSubscription,\n  ProductSubscriptionId,\n  ProductStartAt,\n  ProductEventReadCursor\n&gt;」。该普通调用关系不替代进程或网络协议关系。 以「return createNeutralControlPlaneClient({\n    ...options,\n    generated: generatedTransport,\n  })」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「generatedTransport」关联路径「generatedTransport」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「options」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。

源码：`apps/client/src/community-control-plane-client.ts:361`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/137`。

### `apps/client/src/community-control-plane-client.ts::workItemsCreateCommand`

构造捕获记录，字段按源码次序为「schemaVersion ← 'winwincode/v1'；command ← 'workitems.create'；actor ← input.actor；scope ← input.scope；requestId ← input.requestId；expectedRevision ← input.expectedRevision；payload ← {\n      deliveryId: input.deliveryId,\n      expectedRevision: input.expectedRevision,\n      contractRevision: input.contractRevision,\n      items: input.ite…［展示截断；完整操作保留］」。不据构造形式推断物理持久化。 以「return {\n    schemaVersion: 'winwincode/v1',\n    command: 'workitems.create',\n    actor: input.actor,\n    scope: input.scope,\n    requestId: input.requestId,\n    expectedRevision: input.expectedRevision,\n    payload: {\n      deliveryId: input.deliveryId,\n      expectedRevision: input.expectedRevision,\n      contractRevision: input.contractRevision,…［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「input.actor」关联路径「input.actor」；只描述捕获来源，不证明当时的字段值。 记录消息形状中的固定文本字段「schemaVersion」及捕获形式「'winwincode/v1'」。单个文本字段不是跨语言调用或传输成功的证明。

源码：`apps/client/src/community-control-plane-client.ts:418`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/138`。

### `apps/client/src/core/connection-state.ts::observeControlPlaneClient`

构造捕获记录，字段按源码次序为「serverUrl ← options.client.serverUrl」。不据构造形式推断物理持久化。 在调用形式「Object.freeze」中提供第 1 个实参「{\n    client,\n    reconnectAll() {\n      options.monitor.reconnecting()\n      for (const subscription of subscriptions) subscription.reconnect()\n    },\n  }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「subscriptions」的初始化来源为「new Set&lt;ControlPlaneSubscription&gt;()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return Object.freeze({\n    client,\n    reconnectAll() {\n      options.monitor.reconnecting()\n      for (const subscription of subscriptions) subscription.reconnect()\n    },\n  })」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「options.client.serverUrl」关联路径「options.client.serverUrl」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「c24c0ff2c307e33f4551c95e」先于语句位置「2」的操作「aa1baf48def90139315c3829」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/core/connection-state.ts:400`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/139`。

### `apps/client/src/core/connection-state.ts::observeControlPlaneClient.observe`

在调用形式「options.monitor.connected」中提供第 1 个实参「requestId」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「result」的初始化来源为「await operation」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return result」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「c6b92da126bf4fd3cd97451a」先于语句位置「1」的操作「c9fe41f77939d3a73fb02cdf」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/core/connection-state.ts:405`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/140`。

### `apps/client/src/core/connection-state.ts::observeControlPlaneClient.client.restore`

将「options.client.restore(requestOptions)」作为第 1 个实参交给已绑定接口「ts:apps/client/src/core/connection-state#observeControlPlaneClient.observe」，对应捕获形参「operation: Promise&lt;T&gt;」。该普通调用关系不替代进程或网络协议关系。 以「return observe(options.client.restore(requestOptions))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`apps/client/src/core/connection-state.ts:421`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/141`。

### `apps/client/src/core/connection-state.ts::observeControlPlaneClient.client.initializeOwner`

将「options.client.initializeOwner(initialization, requestOptions)」作为第 1 个实参交给已绑定接口「ts:apps/client/src/core/connection-state#observeControlPlaneClient.observe」，对应捕获形参「operation: Promise&lt;T&gt;」。该普通调用关系不替代进程或网络协议关系。 以「return observe(options.client.initializeOwner(initialization, requestOptions))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`apps/client/src/core/connection-state.ts:424`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/142`。

### `apps/client/src/core/connection-state.ts::observeControlPlaneClient.client.login`

将「options.client.login(credentials, requestOptions)」作为第 1 个实参交给已绑定接口「ts:apps/client/src/core/connection-state#observeControlPlaneClient.observe」，对应捕获形参「operation: Promise&lt;T&gt;」。该普通调用关系不替代进程或网络协议关系。 以「return observe(options.client.login(credentials, requestOptions))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`apps/client/src/core/connection-state.ts:427`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/143`。

### `apps/client/src/core/connection-state.ts::observeControlPlaneClient.client.changePassword`

将「options.client.changePassword(change, requestOptions)」作为第 1 个实参交给已绑定接口「ts:apps/client/src/core/connection-state#observeControlPlaneClient.observe」，对应捕获形参「operation: Promise&lt;T&gt;」。该普通调用关系不替代进程或网络协议关系。 以「return observe(options.client.changePassword(change, requestOptions))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`apps/client/src/core/connection-state.ts:430`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/144`。

### `apps/client/src/core/connection-state.ts::observeControlPlaneClient.client.initializationStatus`

在调用形式「options.client.initializationStatus」中提供第 1 个实参「requestOptions」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return options.client.initializationStatus(requestOptions)」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`apps/client/src/core/connection-state.ts:433`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/145`。

### `apps/client/src/core/connection-state.ts::observeControlPlaneClient.client.logout`

将「options.client.logout(requestOptions)」作为第 1 个实参交给已绑定接口「ts:apps/client/src/core/connection-state#observeControlPlaneClient.observe」，对应捕获形参「operation: Promise&lt;T&gt;」。该普通调用关系不替代进程或网络协议关系。 以「return observe(options.client.logout(requestOptions))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`apps/client/src/core/connection-state.ts:438`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/146`。

### `apps/client/src/core/connection-state.ts::observeControlPlaneClient.client.command`

将「command.requestId」作为第 2 个实参交给已绑定接口「ts:apps/client/src/core/connection-state#observeControlPlaneClient.observe」，对应捕获形参「requestId: RequestId | null = null」。该普通调用关系不替代进程或网络协议关系。 以「return observe(options.client.command(command, requestOptions), command.requestId)」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`apps/client/src/core/connection-state.ts:441`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/147`。

### `apps/client/src/core/connection-state.ts::observeControlPlaneClient.client.query`

将「query.requestId」作为第 2 个实参交给已绑定接口「ts:apps/client/src/core/connection-state#observeControlPlaneClient.observe」，对应捕获形参「requestId: RequestId | null = null」。该普通调用关系不替代进程或网络协议关系。 以「return observe(options.client.query(query, requestOptions), query.requestId)」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`apps/client/src/core/connection-state.ts:444`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/148`。

### `apps/client/src/core/connection-state.ts::observeControlPlaneClient.client.subscribe`

构造捕获的空记录「{}」；没有从空记录形式推断额外字段或持久效果。 在调用形式「options.client.subscribe」中提供第 1 个实参「observedOptions」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「onResetRequired」的初始化来源为「subscriptionOptions.onResetRequired」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「raw」存在源更新「raw = options.client.subscribe(observedOptions)」；循环和分支条件见操作上下文，未推执行次数或最终数值。 以「return subscription」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留记录复制/展开来源「subscriptionOptions」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「4adf80d4928d7768a0395fa8」先于语句位置「2」的操作「afc44a1966ddc758a245cbb9」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/core/connection-state.ts:447`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/149`。

### `apps/client/src/core/connection-state.ts::observeControlPlaneClient.client.subscribe.observedOptions.onEvent`

在调用形式「subscriptionOptions.onEvent」中提供第 1 个实参「event」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 保留同一块中的正常源码顺序：语句位置「0」的操作「8c93a6d73298110d2cbd98cc」先于语句位置「1」的操作「a35e1b296e6d24ee25b6813f」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/core/connection-state.ts:453`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/150`。

### `apps/client/src/core/connection-state.ts::observeControlPlaneClient.client.subscribe.observedOptions.&lt;object@459:12&gt;.onResetRequired`

在调用形式「onResetRequired」中提供第 1 个实参「frame」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return onResetRequired(frame)」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「18e528f89de6f7770a3b5447」先于语句位置「1」的操作「1a0b178486fe70d4eb1929a4」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/core/connection-state.ts:460`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/151`。

### `apps/client/src/core/connection-state.ts::observeControlPlaneClient.client.subscribe.observedOptions.onAuthorizationRevoked`

在调用形式「subscriptionOptions.onAuthorizationRevoked」中提供第 1 个实参「frame」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 保留同一块中的正常源码顺序：语句位置「0」的操作「4ef0b21e118caa55f14f26e3」先于语句位置「1」的操作「450108ad389625399c70467a」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/core/connection-state.ts:465`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/152`。

### `apps/client/src/core/connection-state.ts::observeControlPlaneClient.client.subscribe.observedOptions.onError`

在调用形式「options.monitor.failure」中提供第 1 个实参「error」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 保留同一块中的正常源码顺序：语句位置「0」的操作「2f959f5e52a3e2d246dcfee8」先于语句位置「1」的操作「85cd9ff8431e479c975b7de4」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/core/connection-state.ts:470`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/153`。

### `apps/client/src/core/connection-state.ts::observeControlPlaneClient.client.subscribe.subscription.cursor`

以「return raw.cursor」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`apps/client/src/core/connection-state.ts:477`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/154`。

### `apps/client/src/core/connection-state.ts::observeControlPlaneClient.client.subscribe.subscription.resume`

以无显式实参的调用形式「raw.resume」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/core/connection-state.ts:478`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/155`。

### `apps/client/src/core/connection-state.ts::observeControlPlaneClient.client.subscribe.subscription.reconnect`

以无显式实参的调用形式「options.monitor.reconnecting」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。 保留同一块中的正常源码顺序：语句位置「0」的操作「7fcbd45134deab1bc10aa65b」先于语句位置「1」的操作「1449bc5ec4fba55346eb24b5」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/core/connection-state.ts:479`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/156`。

### `apps/client/src/core/connection-state.ts::observeControlPlaneClient.client.subscribe.subscription.close`

在调用形式「subscriptions.delete」中提供第 1 个实参「subscription」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 对捕获 binding「active」存在源更新「active = false」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!active)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「2ed81a7f0348fa4bd5a821ac」先于语句位置「1」的操作「78b7611d9de86e21b7a40339」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/core/connection-state.ts:483`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/157`。

### `apps/client/src/core/connection-state.ts::observeControlPlaneClient.client.close`

以无显式实参的调用形式「subscription.close」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。 保留同一块中的正常源码顺序：语句位置「0」的操作「9f8b1cbe7b4bf25c4a5cedd4」先于语句位置「1」的操作「0691de36848f84360c2780e1」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/core/connection-state.ts:493`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/158`。

### `apps/client/src/core/connection-state.ts::observeControlPlaneClient.&lt;object@499:23&gt;.reconnectAll`

以无显式实参的调用形式「options.monitor.reconnecting」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。 保留同一块中的正常源码顺序：语句位置「0」的操作「35bac07572ddd16dadb8ac4f」先于语句位置「1」的操作「0f2191549dac0e57ab6b503e」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/core/connection-state.ts:501`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/159`。

### `apps/client/src/decision-clarification-view-model.ts::valuesFrom`

构造捕获记录，字段按源码次序为「title ← requirements.title；goal ← requirements.goal；scope ← requirements.scope.join('\n')；outOfScope ← requirements.outOfScope.join('\n')；constraints ← requirements.constraints.join('\n')；acceptanceCriteria ← criteriaJson(requirements.acceptanceCriteria.map(criterion =&gt; ({\n      id: criterion.id,\n      title: criterion.description,\n      required: criterion.requir…［展示截断；完整操作保留］」。不据构造形式推断物理持久化。 将「requirements.acceptanceCriteria.map(criterion =&gt; ({\n      id: criterion.id,\n      title: criterion.description,\n      required: criterion.required,\n      verificationMethod: criterion.verificationMethod,\n    }))」作为第 1 个实参交给已绑定接口「ts:apps/client/src/decision-clarification-view-model#criteriaJson」，对应捕获形参「criteria: readonly ClarificationCriterion[]」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「requirements」的初始化来源为「detail.requirements」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return Object.freeze({\n    title: requirements.title,\n    goal: requirements.goal,\n    scope: requirements.scope.join('\n'),\n    outOfScope: requirements.outOfScope.join('\n'),\n    constraints: requirements.constraints.join('\n'),\n    acceptanceCriteria: criteriaJson(requirements.acceptanceCriteria.map(criterion =&gt; ({\n      id: criterion.id,\n      ti…［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「requirements.title」关联路径「requirements.title」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「bc010250004a8ab1c3238f9b」先于语句位置「1」的操作「32d24c295e06c0d6f6347abf」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/decision-clarification-view-model.ts:155`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/160`。

### `apps/client/src/decision-clarification-view-model.ts::valuesFrom.&lt;object@157:23&gt;.&lt;arrow@163:73&gt;`

构造捕获记录，字段按源码次序为「id ← criterion.id；title ← criterion.description；required ← criterion.required；verificationMethod ← criterion.verificationMethod」。不据构造形式推断物理持久化。 以字段投影形式「criterion.id」关联路径「criterion.id」；只描述捕获来源，不证明当时的字段值。

源码：`apps/client/src/decision-clarification-view-model.ts:163`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/161`。

### `apps/client/src/decision-clarification-view-model.ts::clarificationUpdateCommand`

构造捕获记录，字段按源码次序为「title ← input.values.title.trim()；goal ← input.values.goal.trim()；repositoryId ← scope.repositoryId；baseRevision ← input.source.baseRevision；scope ← lines(input.values.scope)；outOfScope ← lines(input.values.outOfScope)；constraints ← lines(input.values.constraints)；sourceProductSessionId ← input.source.productSessionId；acceptanceCriteria ← criteriaFrom(input.values.acceptanceCriteria).map(criterion =&gt; ({\n          id: criterion.id,\n          title: criterion.title.trim(),\n          required: cr…［展示截断；完整操作保留］；publicationTarget ← input.source.publicationTarget」。不据构造形式推断物理持久化。 将「input.values.scope」作为第 1 个实参交给已绑定接口「ts:apps/client/src/decision-clarification-view-model#lines」，对应捕获形参「value: string」。该普通调用关系不替代进程或网络协议关系。 以「return {\n    schemaVersion: 'winwincode/v1',\n    command: 'delivery.update_spec',\n    actor,\n    scope,\n    requestId: input.requestId,\n    expectedRevision: input.expectedRevision,\n    payload: {\n      deliveryId: input.source.deliveryId,\n      spec: {\n        title: input.values.title.trim(),\n        goal: input.values.goal.trim(),\n        repo…［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「actor」关联路径「actor」；只描述捕获来源，不证明当时的字段值。 记录消息形状中的固定文本字段「schemaVersion」及捕获形式「'winwincode/v1'」。单个文本字段不是跨语言调用或传输成功的证明。

源码：`apps/client/src/decision-clarification-view-model.ts:190`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/162`。

### `apps/client/src/decision-clarification-view-model.ts::clarificationUpdateCommand.&lt;object@195:9&gt;.&lt;object@202:13&gt;.&lt;object@204:12&gt;.&lt;arrow@213:78&gt;`

构造捕获记录，字段按源码次序为「id ← criterion.id；title ← criterion.title.trim()；required ← criterion.required」。不据构造形式推断物理持久化。 以无显式实参的调用形式「criterion.title.trim」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。 以字段投影形式「criterion.id」关联路径「criterion.id」；只描述捕获来源，不证明当时的字段值。

源码：`apps/client/src/decision-clarification-view-model.ts:213`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/163`。

### `apps/client/src/decision-clarification-view-model.ts::createControlPlaneClarificationPort`

构造捕获记录，字段按源码次序为「load ← load」。不据构造形式推断物理持久化。 在调用形式「Object.freeze」中提供第 1 个实参「{\n    load,\n    async save(input: ClarificationSaveInput) {\n      const command = clarificationUpdateCommand(input, options.actor, options.scope)\n      const response = await options.client.command(command)\n      if (response.outcome !== 'completed' || response.command !== 'delivery.update_spec') {\n        throw new Error('控制平面已接收更新，但尚未确认完成；请使用同一草稿重试。'…［展示截断；完整操作保留］」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return Object.freeze({\n    load,\n    async save(input: ClarificationSaveInput) {\n      const command = clarificationUpdateCommand(input, options.actor, options.scope)\n      const response = await options.client.command(command)\n      if (response.outcome !== 'completed' || response.command !== 'delivery.update_spec') {\n        throw new Error('控制平面已接收更…［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「load」关联路径「load」；只描述捕获来源，不证明当时的字段值。

源码：`apps/client/src/decision-clarification-view-model.ts:224`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/164`。

### `apps/client/src/decision-clarification-view-model.ts::createControlPlaneClarificationPort.load`

构造捕获记录，字段按源码次序为「actor ← options.actor；scope ← options.scope；deliveryId ← options.deliveryId；requestId ← options.nextRequestId()」。不据构造形式推断物理持久化。 将「{\n      actor: options.actor,\n      scope: options.scope,\n      deliveryId: options.deliveryId,\n      requestId: options.nextRequestId(),\n    }」作为第 2 个实参交给已绑定接口「ts:apps/client/src/community-control-plane-client#queryDeliveryDetail」，对应捕获形参「input: Pick&lt;WorkRunAggregateQueryInput, 'actor' | 'scope' | 'requestId' | 'deliveryId'&gt;」。该普通调用关系不替代进程或网络协议关系。 以「return snapshotFrom(await queryDeliveryDetail(options.client, {\n      actor: options.actor,\n      scope: options.scope,\n      deliveryId: options.deliveryId,\n      requestId: options.nextRequestId(),\n    }), options.actor)」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「options.actor」关联路径「options.actor」；只描述捕获来源，不证明当时的字段值。

源码：`apps/client/src/decision-clarification-view-model.ts:231`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/165`。

### `apps/client/src/decision-clarification-view-model.ts::createControlPlaneClarificationPort.&lt;object@240:23&gt;.save`

将「input」作为第 1 个实参交给已绑定接口「ts:apps/client/src/decision-clarification-view-model#clarificationUpdateCommand」，对应捕获形参「input: ClarificationSaveInput」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「command」的初始化来源为「clarificationUpdateCommand(input, options.actor, options.scope)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(response.outcome !== 'completed' || response.command !== 'delivery.update_spec')」的捕获提前退出分支为「throw：new Error('控制平面已接收更新，但尚未确认完成；请使用同一草稿重试。')」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new Error('控制平面已接收更新，但尚未确认完成；请使用同一草稿重试。')」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「0f6c0c4dc367bc907b1e794c」先于语句位置「1」的操作「916d0983c4fe015810d6c0a9」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 以无显式实参的调用形式「load」调用已绑定接口「ts:apps/client/src/decision-clarification-view-model#createControlPlaneClarificationPort.load」；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/decision-clarification-view-model.ts:242`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/166`。

### `apps/client/src/decision-clarification-view-model.ts::createClarificationViewModel`

构造捕获记录，字段按源码次序为「revisionSensitive ← true」。不据构造形式推断物理持久化。 将「{ revisionSensitive: true }」作为第 1 个实参交给已绑定接口「ts:apps/client/src/editable-draft#createEditableDraft」，对应捕获形参「options: EditableDraftOptions&lt;Values&gt; = {}」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「draft」的初始化来源为「createEditableDraft&lt;ClarificationValues&gt;({ revisionSensitive: true })」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return model」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「3960fd6ec7a0d7e5e0da3e61」先于语句位置「1」的操作「b28ec72e0276b52bbdeca154」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/decision-clarification-view-model.ts:284`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/167`。

### `apps/client/src/decision-clarification-view-model.ts::createClarificationViewModel.currentState`

构造捕获记录，字段按源码次序为「status ← status；snapshot ← snapshot；values ← values；criteria ← criteriaFrom(values.acceptanceCriteria)；changes ← Object.freeze(changes)；dirty ← draftState.dirtyFields.length &gt; 0；busy ← draftState.submission !== null；offline ← offline；conflicts ← draftState.conflicts；notice ← notice；lastRequestId ← lastRequestId；formRevision ← formRevision」。不据构造形式推断物理持久化。 将「field」作为第 1 个实参交给已绑定接口「ts:apps/client/src/decision-clarification-view-model#displayValue」，对应捕获形参「field: ClarificationField」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「draftState」的初始化来源为「draft.state」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return Object.freeze({\n      status,\n      snapshot,\n      values,\n      criteria: criteriaFrom(values.acceptanceCriteria),\n      changes: Object.freeze(changes),\n      dirty: draftState.dirtyFields.length &gt; 0,\n      busy: draftState.submission !== null,\n      offline,\n      conflicts: draftState.conflicts,\n      notice,\n      lastRequestId,\n    …［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「field」关联路径「field」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「fe65e603f64ae014e3a0f6e7」先于语句位置「1」的操作「69df764b2717acd0814b45cc」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/decision-clarification-view-model.ts:299`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/168`。

### `apps/client/src/decision-clarification-view-model.ts::createClarificationViewModel.emit`

以无显式实参的调用形式「currentState」调用已绑定接口「ts:apps/client/src/decision-clarification-view-model#createClarificationViewModel.currentState」；没有据调用存在断言激活、存储或网络效果。 捕获 binding「next」的初始化来源为「currentState()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「fc63962d045b26b7095e95f5」先于语句位置「1」的操作「8f62c759b3ab0c47cd2d43ca」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/decision-clarification-view-model.ts:330`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/169`。

### `apps/client/src/decision-clarification-view-model.ts::createClarificationViewModel.synchronize`

构造捕获记录，字段按源码次序为「scope ← loaded.deliveryId；revision ← loaded.deliveryRevision；values ← loaded.values」。不据构造形式推断物理持久化。 以无显式实参的调用形式「emit」调用已绑定接口「ts:apps/client/src/decision-clarification-view-model#createClarificationViewModel.emit」；没有据调用存在断言激活、存储或网络效果。 捕获 binding「generation」的初始化来源为「++loadGeneration」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「notice」存在源更新「notice = message」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(closed || generation !== loadGeneration)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「loaded.deliveryId」关联路径「loaded.deliveryId」；只描述捕获来源，不证明当时的字段值。

源码：`apps/client/src/decision-clarification-view-model.ts:336`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/170`。

### `apps/client/src/decision-clarification-view-model.ts::createClarificationViewModel.editCriteria`

以无显式实参的调用形式「emit」调用已绑定接口「ts:apps/client/src/decision-clarification-view-model#createClarificationViewModel.emit」；没有据调用存在断言激活、存储或网络效果。 对捕获 binding「formRevision」存在源更新「formRevision += 1」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(status !== 'editing' || draft.state.submission !== null)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「14b2f5f5a02351c4ab371343」先于语句位置「1」的操作「48ca2bfd4a0362d7aa30fe13」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/decision-clarification-view-model.ts:352`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/171`。

### `apps/client/src/decision-clarification-view-model.ts::createClarificationViewModel.model.state`

以无显式实参的调用形式「currentState」调用已绑定接口「ts:apps/client/src/decision-clarification-view-model#createClarificationViewModel.currentState」；没有据调用存在断言激活、存储或网络效果。 以「return currentState()」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`apps/client/src/decision-clarification-view-model.ts:362`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/172`。

### `apps/client/src/decision-clarification-view-model.ts::createClarificationViewModel.model.subscribe`

在调用形式「listeners.add」中提供第 1 个实参「listener」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return () =&gt; listeners.delete(listener)」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「bc31608fdd14f315912782bf」先于语句位置「1」的操作「b83e0fc023d1925da6df37f2」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/decision-clarification-view-model.ts:363`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/173`。

### `apps/client/src/decision-clarification-view-model.ts::createClarificationViewModel.model.subscribe.&lt;arrow@365:13&gt;`

在调用形式「listeners.delete」中提供第 1 个实参「listener」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`apps/client/src/decision-clarification-view-model.ts:365`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/174`。

### `apps/client/src/decision-clarification-view-model.ts::createClarificationViewModel.model.start`

将「null」作为第 1 个实参交给已绑定接口「ts:apps/client/src/decision-clarification-view-model#createClarificationViewModel.synchronize」，对应捕获形参「message: string | null」。该普通调用关系不替代进程或网络协议关系。 对捕获 binding「status」存在源更新「status = 'failed'」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「663b946510ac7cb56d64045e」先于语句位置「1」的操作「1a75121f6428e440f5225105」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 以无显式实参的调用形式「emit」调用已绑定接口「ts:apps/client/src/decision-clarification-view-model#createClarificationViewModel.emit」；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/decision-clarification-view-model.ts:367`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/175`。

### `apps/client/src/decision-clarification-view-model.ts::createClarificationViewModel.model.refresh`

将「'已读取最新规范。'」作为第 1 个实参交给已绑定接口「ts:apps/client/src/decision-clarification-view-model#createClarificationViewModel.synchronize」，对应捕获形参「message: string | null」。该普通调用关系不替代进程或网络协议关系。 对捕获 binding「notice」存在源更新「notice = errorMessage(error)」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(draft.state.submission !== null)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「110f1f285a6de1ba9a56ded7」先于语句位置「1」的操作「637230e618faac291238a06c」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 以无显式实参的调用形式「emit」调用已绑定接口「ts:apps/client/src/decision-clarification-view-model#createClarificationViewModel.emit」；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/decision-clarification-view-model.ts:377`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/176`。

### `apps/client/src/decision-clarification-view-model.ts::createClarificationViewModel.model.edit`

以无显式实参的调用形式「emit」调用已绑定接口「ts:apps/client/src/decision-clarification-view-model#createClarificationViewModel.emit」；没有据调用存在断言激活、存储或网络效果。 对捕获 binding「pendingRequestId」存在源更新「pendingRequestId = null」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(status !== 'editing' || draft.state.submission !== null)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「2b284ebca68ec5be548c31be」先于语句位置「1」的操作「6926acdaa5de4af70363b1a6」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/decision-clarification-view-model.ts:387`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/177`。

### `apps/client/src/decision-clarification-view-model.ts::createClarificationViewModel.model.markUnknown`

在调用形式「this.edit」中提供第 1 个实参「field」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`apps/client/src/decision-clarification-view-model.ts:394`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/178`。

### `apps/client/src/decision-clarification-view-model.ts::createClarificationViewModel.model.markLater`

在调用形式「this.edit」中提供第 1 个实参「field」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`apps/client/src/decision-clarification-view-model.ts:395`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/179`。

### `apps/client/src/decision-clarification-view-model.ts::createClarificationViewModel.model.addCriterion`

构造捕获记录，字段按源码次序为「id ← options.nextCriterionId()；title ← ''；required ← false；verificationMethod ← null」。不据构造形式推断物理持久化。 将「[...criteria, Object.freeze({\n        id: options.nextCriterionId(),\n        title: '',\n        required: false,\n        verificationMethod: null,\n      })]」作为第 1 个实参交给已绑定接口「ts:apps/client/src/decision-clarification-view-model#createClarificationViewModel.editCriteria」，对应捕获形参「criteria: readonly ClarificationCriterion[]」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「criteria」的初始化来源为「criteriaFrom(draft.state.values.acceptanceCriteria)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「notice」存在源更新「notice = '验收条件数量已达到上限。'」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(criteria.length &gt;= MAX_CRITERIA)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「c272ae75fbd9226bb8ff8c12」先于语句位置「1」的操作「f72ab47ea0d23ff6a7c04eb4」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 以无显式实参的调用形式「emit」调用已绑定接口「ts:apps/client/src/decision-clarification-view-model#createClarificationViewModel.emit」；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/decision-clarification-view-model.ts:396`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/180`。

### `apps/client/src/decision-clarification-view-model.ts::createClarificationViewModel.model.updateCriterion`

将「criteriaFrom(draft.state.values.acceptanceCriteria).map(criterion =&gt; (\n        criterion.id === id ? Object.freeze({ ...criterion, ...patch }) : criterion\n      ))」作为第 1 个实参交给已绑定接口「ts:apps/client/src/decision-clarification-view-model#createClarificationViewModel.editCriteria」，对应捕获形参「criteria: readonly ClarificationCriterion[]」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/decision-clarification-view-model.ts:410`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/181`。

### `apps/client/src/decision-clarification-view-model.ts::createClarificationViewModel.model.updateCriterion.&lt;arrow@411:75&gt;`

具有捕获记录构造「{ ...criterion, ...patch }」；该记录的可枚举字段为空或保留开放形状，未把展开来源补成确定字段。 在调用形式「Object.freeze」中提供第 1 个实参「{ ...criterion, ...patch }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 保留记录复制/展开来源「criterion」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。

源码：`apps/client/src/decision-clarification-view-model.ts:411`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/182`。

### `apps/client/src/decision-clarification-view-model.ts::createClarificationViewModel.model.removeCriterion`

将「criteriaFrom(draft.state.values.acceptanceCriteria).filter(criterion =&gt; (\n        criterion.id !== id\n      ))」作为第 1 个实参交给已绑定接口「ts:apps/client/src/decision-clarification-view-model#createClarificationViewModel.editCriteria」，对应捕获形参「criteria: readonly ClarificationCriterion[]」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/decision-clarification-view-model.ts:415`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/183`。

### `apps/client/src/decision-clarification-view-model.ts::createClarificationViewModel.model.setOffline`

以无显式实参的调用形式「emit」调用已绑定接口「ts:apps/client/src/decision-clarification-view-model#createClarificationViewModel.emit」；没有据调用存在断言激活、存储或网络效果。 对捕获 binding「offline」存在源更新「offline = value」；循环和分支条件见操作上下文，未推执行次数或最终数值。 保留同一块中的正常源码顺序：语句位置「0」的操作「510ea0572709e6b5cdf6516c」先于语句位置「1」的操作「14b524115bbd4d9869fadf43」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/decision-clarification-view-model.ts:420`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/184`。

### `apps/client/src/decision-clarification-view-model.ts::createClarificationViewModel.model.resolveConflicts`

以无显式实参的调用形式「emit」调用已绑定接口「ts:apps/client/src/decision-clarification-view-model#createClarificationViewModel.emit」；没有据调用存在断言激活、存储或网络效果。 对捕获 binding「pendingRequestId」存在源更新「pendingRequestId = null」；循环和分支条件见操作上下文，未推执行次数或最终数值。 保留同一块中的正常源码顺序：语句位置「0」的操作「cdc5fc1268b41a8ed7585d6a」先于语句位置「1」的操作「68b243147b42af5330ea58a8」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/decision-clarification-view-model.ts:426`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/185`。

### `apps/client/src/decision-clarification-view-model.ts::createClarificationViewModel.model.submit`

构造捕获记录，字段按源码次序为「source ← snapshot；expectedRevision ← submission.revision；requestId ← requestId；values ← submission.values」。不据构造形式推断物理持久化。 以无显式实参的调用形式「emit」调用已绑定接口「ts:apps/client/src/decision-clarification-view-model#createClarificationViewModel.emit」；没有据调用存在断言激活、存储或网络效果。 捕获 binding「latest」的初始化来源为「await options.port.load()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「notice」存在源更新「notice = problem」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(status !== 'editing' || snapshot === null || offline)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「snapshot」关联路径「snapshot」；只描述捕获来源，不证明当时的字段值。

源码：`apps/client/src/decision-clarification-view-model.ts:433`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/186`。

### `apps/client/src/decision-clarification-view-model.ts::createClarificationViewModel.model.close`

以无显式实参的调用形式「listeners.clear」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。 对捕获 binding「closed」存在源更新「closed = true」；循环和分支条件见操作上下文，未推执行次数或最终数值。 保留同一块中的正常源码顺序：语句位置「0」的操作「3496aa610b964cb2b466eef8」先于语句位置「1」的操作「2980990efed89d4f86a88591」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/decision-clarification-view-model.ts:496`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/187`。

### `apps/client/src/home-dashboard-page.ts::homeDecisionHash`

将「scopeSelection」作为第 2 个实参交给已绑定接口「ts:packages/browser-core/src/scope-context#scopeHash」，对应捕获形参「selection: ScopeRouteSelection | CompleteRepositorySelection」。该普通调用关系不替代进程或网络协议关系。 条件「(card.kind === 'attention')」的捕获提前退出分支为「return：card.deliveryId === null\n      ? null\n      : scopeHash(`#/home/review?delivery=${encodeURIComponent(card.deliveryId)}`, scopeSelection)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return card.deliveryId === null\n      ? null\n      : scopeHash(`#/home/review?delivery=${encodeURIComponent(card.deliveryId)}`, scopeSelection)」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「1」的操作「ab66daad6f195579d7300fdf」先于语句位置「2」的操作「7342b398adc8a8df50158a70」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/home-dashboard-page.ts:219`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/188`。

### `apps/client/src/home-dashboard-page.ts::mountHomeDashboardPage`

构造捕获记录，字段按源码次序为「root ← root；heading ← heading；count ← count；empty ← empty；cards ← cards；toggle ← toggle；collection ← mountKeyedCollection&lt;HomeCard, string, HTMLLIElement&gt;({\n        parent: cards,\n        key: cardKey,\n        create: createCard,\n        update: updateCard,…［展示截断；完整操作保留］」。不据构造形式推断物理持久化。 将「options.scopeSelection」作为第 2 个实参交给已绑定接口「ts:packages/browser-core/src/scope-context#surfaceHash」，对应捕获形参「selection: ScopeRouteSelection」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「option.textContent = label」，捕获目标为「option.textContent」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「document」的初始化来源为「options.root.ownerDocument」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「toggle」存在源更新「toggle = toggleButton」；循环和分支条件见操作上下文，未推执行次数或最终数值。 以「return {\n    close() {\n      if (closed) return\n      closed = true\n      unsubscribe()\n      for (const section of sections.values()) section.collection.close()\n      statusBadge.close()\n      pageHeader.close()\n      options.root.replaceChildren()\n      if (options.ownsModel !== false) options.model.close()\n    },\n  }」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「document」关联路径「document」；只描述捕获来源，不证明当时的字段值。

源码：`apps/client/src/home-dashboard-page.ts:331`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/189`。

### `apps/client/src/home-dashboard-page.ts::mountHomeDashboardPage.deliveryContextEntries`

在调用形式「presentation.taskLabel」中提供第 1 个实参「card」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return Object.freeze([\n      presentation.taskLabel(card),\n      card.openAttentionCount === 0\n        ? null\n        : `${String(card.openAttentionCount)} 个待处理`,\n      presentation.updatedLabel(card.updatedAt),\n    ].filter((entry): entry is string =&gt; entry !== null &amp;&amp; entry !== ''))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`apps/client/src/home-dashboard-page.ts:390`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/190`。

### `apps/client/src/home-dashboard-page.ts::mountHomeDashboardPage.decisionContextEntries`

在调用形式「String」中提供第 1 个实参「card.attentionCount」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return card.attentionCount !== undefined &amp;&amp; card.attentionCount &gt; 1\n      ? Object.freeze([`${String(card.attentionCount)} 项待处理`])\n      : Object.freeze([])」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`apps/client/src/home-dashboard-page.ts:400`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/191`。

### `apps/client/src/home-dashboard-page.ts::mountHomeDashboardPage.setAction`

在调用形式「parts.action.removeAttribute」中提供第 1 个实参「'aria-disabled'」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 包含赋值/更新「parts.action.href = href」，捕获目标为「parts.action.href」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「6eba08f883de461333782d2e」先于语句位置「1」的操作「46bcce343af35d60c9b04fe6」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/home-dashboard-page.ts:406`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/192`。

### `apps/client/src/home-dashboard-page.ts::mountHomeDashboardPage.disableAction`

在调用形式「parts.action.removeAttribute」中提供第 1 个实参「'href'」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 包含赋值/更新「parts.action.textContent = label」，捕获目标为「parts.action.textContent」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「8ccd4a18bd3cc81f3a5e263e」先于语句位置「1」的操作「e12e13a11ec1f9c90534b682」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/home-dashboard-page.ts:414`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/193`。

### `apps/client/src/home-dashboard-page.ts::mountHomeDashboardPage.fillDecisionCard`

将「card」作为第 1 个实参交给已绑定接口「ts:apps/client/src/home-dashboard-page#mountHomeDashboardPage.decisionContextEntries」，对应捕获形参「card: HomeDecisionCard」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「parts.node.dataset.urgency = card.urgency」，捕获目标为「parts.node.dataset.urgency」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「hash」的初始化来源为「homeDecisionHash(card, options.scopeSelection)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留同一块中的正常源码顺序：语句位置「0」的操作「ade7e01a781f85ff3de80c1a」先于语句位置「1」的操作「575c801d7d6e8e1171e7da69」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「parts」作为第 1 个实参交给已绑定接口「ts:apps/client/src/home-dashboard-page#mountHomeDashboardPage.disableAction」，对应捕获形参「parts: CardParts」。该普通调用关系不替代进程或网络协议关系。 将「card」作为第 1 个实参交给已绑定接口「ts:apps/client/src/home-dashboard-page#homeDecisionHash」，对应捕获形参「card: HomeDecisionCard」。该普通调用关系不替代进程或网络协议关系。 将「parts」作为第 1 个实参交给已绑定接口「ts:apps/client/src/home-dashboard-page#mountHomeDashboardPage.setAction」，对应捕获形参「parts: CardParts」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/home-dashboard-page.ts:422`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/194`。

### `apps/client/src/home-dashboard-page.ts::mountHomeDashboardPage.clearAction`

在调用形式「parts.action.removeAttribute」中提供第 1 个实参「'href'」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 包含赋值/更新「parts.action.tabIndex = -1」，捕获目标为「parts.action.tabIndex」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「d45ab5b87c4d321efe65f015」先于语句位置「1」的操作「2e3555b9ac2e6654a714b90c」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/home-dashboard-page.ts:454`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/195`。

### `apps/client/src/home-dashboard-page.ts::mountHomeDashboardPage.fillVisitedCard`

将「parts」作为第 1 个实参交给已绑定接口「ts:apps/client/src/home-dashboard-page#mountHomeDashboardPage.fillDeliveryCard」，对应捕获形参「parts: CardParts」。该普通调用关系不替代进程或网络协议关系。 保留同一块中的正常源码顺序：语句位置「0」的操作「96df7f8d9ba15beb4f50c6cb」先于语句位置「1」的操作「e2eaff6d1dbabd8bc7a0f631」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/home-dashboard-page.ts:462`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/196`。

### `apps/client/src/home-dashboard-page.ts::mountHomeDashboardPage.fillVisitedCard.&lt;arrow@465:49&gt;`

包含赋值/更新「li.textContent = `访问于 ${card.visitedAt}`」，捕获目标为「li.textContent」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。

源码：`apps/client/src/home-dashboard-page.ts:465`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/197`。

### `apps/client/src/home-dashboard-page.ts::mountHomeDashboardPage.fillDeliveryCard`

将「card」作为第 1 个实参交给已绑定接口「ts:apps/client/src/home-dashboard-page#mountHomeDashboardPage.deliveryContextEntries」，对应捕获形参「card: HomeDeliveryCard」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「parts.node.dataset.status = card.status」，捕获目标为「parts.node.dataset.status」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「f666eef9a6294d2a64e76d17」先于语句位置「1」的操作「4fc7b9205b33a9ad146a0994」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「parts」作为第 1 个实参交给已绑定接口「ts:apps/client/src/home-dashboard-page#mountHomeDashboardPage.setAction」，对应捕获形参「parts: CardParts」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/home-dashboard-page.ts:470`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/198`。

### `apps/client/src/home-dashboard-page.ts::mountHomeDashboardPage.createCard`

构造捕获记录，字段按源码次序为「node ← node；title ← title；status ← status；context ← context；chat ← chat；action ← action」。不据构造形式推断物理持久化。 将「document」作为第 1 个实参交给已绑定接口「ts:apps/client/src/home-dashboard-page#element」，对应捕获形参「document: Document」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「chat.hidden = true」，捕获目标为「chat.hidden」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「index」的初始化来源为「0」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「index」存在源更新「index += 1」；循环和分支条件见操作上下文，未推执行次数或最终数值。 以「return node」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「node」关联路径「node」；只描述捕获来源，不证明当时的字段值。

源码：`apps/client/src/home-dashboard-page.ts:495`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/199`。

### `apps/client/src/home-dashboard-page.ts::mountHomeDashboardPage.updateCard`

将「parts」作为第 1 个实参交给已绑定接口「ts:apps/client/src/home-dashboard-page#mountHomeDashboardPage.fillDecisionCard」，对应捕获形参「parts: CardParts」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「parts」的初始化来源为「cardParts.get(node)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(parts === undefined)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「295a9f9ef18d766f01fbf554」先于语句位置「1」的操作「d96487a911ef8526000ca534」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「parts」作为第 1 个实参交给已绑定接口「ts:apps/client/src/home-dashboard-page#mountHomeDashboardPage.fillVisitedCard」，对应捕获形参「parts: CardParts」。该普通调用关系不替代进程或网络协议关系。 将「parts」作为第 1 个实参交给已绑定接口「ts:apps/client/src/home-dashboard-page#mountHomeDashboardPage.fillDeliveryCard」，对应捕获形参「parts: CardParts」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/home-dashboard-page.ts:511`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/200`。

### `apps/client/src/home-dashboard-page.ts::mountHomeDashboardPage.decisionCountLabel`

在调用形式「String」中提供第 1 个实参「state.decisions.length」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「items」的初始化来源为「state.decisions.reduce(\n      (total, card) =&gt; total + (card.attentionCount ?? 1),\n      0,\n    )」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return `${String(state.decisions.length)} 个任务 · ${String(items)} 项待处理`」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「cd9bae8a4a11b1e603883820」先于语句位置「1」的操作「86c0df084c6527cb757658f7」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/home-dashboard-page.ts:530`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/201`。

### `apps/client/src/home-dashboard-page.ts::mountHomeDashboardPage.sectionCountLabel`

将「state」作为第 1 个实参交给已绑定接口「ts:apps/client/src/home-dashboard-page#mountHomeDashboardPage.decisionCountLabel」，对应捕获形参「state: HomeDashboardState」。该普通调用关系不替代进程或网络协议关系。 以「return id === 'decisions' &amp;&amp; state !== undefined\n      ? decisionCountLabel(state)\n      : id === 'decisions' ? `${String(count)} 个任务`\n        : presentation.countLabel(count)」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`apps/client/src/home-dashboard-page.ts:538`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/202`。

### `apps/client/src/home-dashboard-page.ts::mountHomeDashboardPage.&lt;loop@559:2&gt;.&lt;block@559:34&gt;.&lt;block@573:21&gt;.&lt;arrow@583:45&gt;`

将「id」作为第 1 个实参交给已绑定接口「ts:apps/client/src/home-dashboard-page#mountHomeDashboardPage.sectionCountLabel」，对应捕获形参「id: HomeSectionId」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「cards.hidden = expanded」，捕获目标为「cards.hidden」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「expanded」的初始化来源为「toggleButton.getAttribute('aria-expanded') === 'true'」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留同一块中的正常源码顺序：语句位置「0」的操作「02c9ca9938ba0799e08bab64」先于语句位置「1」的操作「077c37336e95b16318d0716f」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「id」作为第 1 个实参交给已绑定接口「ts:apps/client/src/home-dashboard-page#mountHomeDashboardPage.renderedEmpty」，对应捕获形参「id: HomeSectionId」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/home-dashboard-page.ts:583`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/203`。

### `apps/client/src/home-dashboard-page.ts::mountHomeDashboardPage.renderedEmpty`

捕获 binding「state」的初始化来源为「options.model.state」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return rendered === 0」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「3442e110ddc052cbd48c6072」先于语句位置「1」的操作「a7e6c5c0c8e0d7391a7c1086」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/home-dashboard-page.ts:621`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/204`。

### `apps/client/src/home-dashboard-page.ts::mountHomeDashboardPage.&lt;arrow@647:42&gt;`

将「'decisions'」作为第 1 个实参交给已绑定接口「ts:apps/client/src/home-dashboard-page#mountHomeDashboardPage.renderedEmpty」，对应捕获形参「id: HomeSectionId」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「section.root.hidden = attentionOnlyEnabled」，捕获目标为「section.root.hidden」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「expanded」的初始化来源为「decisions.toggle === null\n        || decisions.toggle.getAttribute('aria-expanded') === 'true'」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「attentionOnlyEnabled」存在源更新「attentionOnlyEnabled = !attentionOnlyEnabled」；循环和分支条件见操作上下文，未推执行次数或最终数值。 保留同一块中的正常源码顺序：语句位置「0」的操作「ff7b50b7f5d5b0ad5061cdf1」先于语句位置「1」的操作「e959e72b8484ce916c5e61eb」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/home-dashboard-page.ts:647`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/205`。

### `apps/client/src/home-dashboard-page.ts::mountHomeDashboardPage.render`

构造捕获记录，字段按源码次序为「label ← homeDashboardAnnouncement(state)；tone ← tone；live ← 'polite'；className ← 'wwc-home-status'」。不据构造形式推断物理持久化。 将「id」作为第 1 个实参交给已绑定接口「ts:apps/client/src/home-dashboard-page#mountHomeDashboardPage.sectionCountLabel」，对应捕获形参「id: HomeSectionId」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「section.count.textContent = sectionCountLabel(id, total, state)」，捕获目标为「section.count.textContent」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「total」的初始化来源为「id === 'decisions'\n        ? state.counts.decisions\n        : id === 'backlog' ? state.counts.backlog\n          : id === 'running' ? state.counts.running\n            : id === 'ready' ? state.counts.ready\n              : id === 'waiting' ? state.counts.waiting\n                : id === 'validating' ? state.counts.validating\n                  : id === 'f…［展示截断；完整操作保留］」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「tone」关联路径「tone」；只描述捕获来源，不证明当时的字段值。 将「id」作为第 1 个实参交给已绑定接口「ts:apps/client/src/home-dashboard-page#mountHomeDashboardPage.renderedEmpty」，对应捕获形参「id: HomeSectionId」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/home-dashboard-page.ts:665`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/206`。

### `apps/client/src/home-dashboard-page.ts::mountHomeDashboardPage.&lt;object@742:9&gt;.close`

以无显式实参的调用形式「unsubscribe」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。 对捕获 binding「closed」存在源更新「closed = true」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「52c7c03cdb0428ef289f5313」先于语句位置「1」的操作「eef0bcbda966e5dfc3cf8009」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/home-dashboard-page.ts:743`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/207`。

### `apps/client/src/my-work-page.ts::mountMyWorkPage`

构造捕获记录，字段按源码次序为「root ← workRoot；model ← options.model.work；scopeSelection ← options.scopeSelection；ownsModel ← false」。不据构造形式推断物理持久化。 将「{\n    root: workRoot,\n    model: options.model.work,\n    scopeSelection: options.scopeSelection,\n    ownsModel: false,\n  }」作为第 1 个实参交给已绑定接口「ts:apps/client/src/home-dashboard-page#mountHomeDashboardPage」，对应捕获形参「options: HomeDashboardPageOptions」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「startLabel.textContent = presentation.startLabel」，捕获目标为「startLabel.textContent」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「document」的初始化来源为「options.root.ownerDocument」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return {\n    close() {\n      if (closed) return\n      closed = true\n      unsubscribe()\n      devices.close()\n      workPage.close()\n      options.root.replaceChildren()\n      if (options.ownsModel !== false) options.model.close()\n    },\n  }」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「workRoot」关联路径「workRoot」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「4513e8699d1da23b699e86f9」先于语句位置「1」的操作「10cef4ed7708ee01ee873a21」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/my-work-page.ts:105`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/208`。

### `apps/client/src/my-work-page.ts::mountMyWorkPage.createDeviceRow`

构造捕获记录，字段按源码次序为「node ← node；name ← name；presence ← presence；state ← state；detail ← detail」。不据构造形式推断物理持久化。 将「document」作为第 1 个实参交给已绑定接口「ts:apps/client/src/my-work-page#element」，对应捕获形参「document: Document」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「node」的初始化来源为「element(document, 'li', 'wwc-clients-card wwc-my-work-clients-device')」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return node」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「node」关联路径「node」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「11350d38c1f5e62791dc898f」先于语句位置「1」的操作「7089d4e31b755d95156a0ea8」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/my-work-page.ts:180`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/209`。

### `apps/client/src/my-work-page.ts::mountMyWorkPage.updateDeviceRow`

将「device」作为第 1 个实参交给已绑定接口「ts:apps/client/src/clients-view-model#deviceStateTone」，对应捕获形参「device: ControlPlaneDeviceSummary」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「parts.name.textContent = device.displayName」，捕获目标为「parts.name.textContent」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「parts」的初始化来源为「rowParts.get(node)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(parts === undefined)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「158f068ae61047d2eb90c145」先于语句位置「1」的操作「58e3d905f15a58d359506e19」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/my-work-page.ts:191`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/210`。

### `apps/client/src/my-work-page.ts::mountMyWorkPage.renderClients`

在调用形式「devices.update」中提供第 1 个实参「zone.devices」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 包含赋值/更新「clientsCount.textContent = presentation.clientsCountLabel(zone.summary.total)」，捕获目标为「clientsCount.textContent」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 条件「(closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「79d0a2d658b8b1643a62b0e8」先于语句位置「1」的操作「6021449682baeb7f63428b60」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/my-work-page.ts:217`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/211`。

### `apps/client/src/my-work-page.ts::mountMyWorkPage.render`

将「state.clients」作为第 1 个实参交给已绑定接口「ts:apps/client/src/my-work-page#mountMyWorkPage.renderClients」，对应捕获形参「zone: MyWorkClientsZone」。该普通调用关系不替代进程或网络协议关系。 条件「(closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「bf57671cbdcce712954e327c」先于语句位置「1」的操作「354db06c56120c56c0bc1380」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/my-work-page.ts:226`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/212`。

### `apps/client/src/my-work-page.ts::mountMyWorkPage.&lt;object@234:9&gt;.close`

以无显式实参的调用形式「unsubscribe」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。 对捕获 binding「closed」存在源更新「closed = true」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「f7d6dc070d1f04727ca707ff」先于语句位置「1」的操作「6a5c4a35d8ebe17b2b220c7a」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/my-work-page.ts:235`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/213`。

### `apps/client/src/settings-page.ts::mountSettingsPage`

构造捕获记录，字段按源码次序为「title ← '模型设置不可用'；message ← ''；actions ← [retry, reconnect]；visible ← false；className ← 'wwc-settings-error'」。不据构造形式推断物理持久化。 将「selectedCategory」作为第 1 个实参交给已绑定接口「ts:apps/client/src/settings-page#mountSettingsPage.showCategory」，对应捕获形参「next: SettingsCategoryId」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「item.dataset.row = key」，捕获目标为「item.dataset.row」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「document」的初始化来源为「options.root.ownerDocument」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return {\n    close() {\n      if (closed) return\n      closed = true\n      unsubscribe()\n      deviceProviders.close()\n      categorySelect.removeEventListener('change', onCategoryChange)\n      generalName.input.removeEventListener('input', onGeneralNameInput)\n      diagnosticsTabs.close()\n      runCheck.close()\n      storagePanel.close()\n      usa…［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「document」关联路径「document」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「(options.fetch === undefined ? {} : { fetch: options.fetch })」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。 将「generalName.input」作为第 3 个实参交给已绑定接口「ts:apps/client/src/settings-page#mountSettingsPage.settingsRow」，对应捕获形参「control: HTMLElement」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/settings-page.ts:241`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/214`。

### `apps/client/src/settings-page.ts::mountSettingsPage.&lt;arrow@269:33&gt;`

构造捕获记录，字段按源码次序为「value ← category.id；label ← category.label」。不据构造形式推断物理持久化。 以字段投影形式「category.id」关联路径「category.id」；只描述捕获来源，不证明当时的字段值。

源码：`apps/client/src/settings-page.ts:269`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/215`。

### `apps/client/src/settings-page.ts::mountSettingsPage.&lt;object@291:34&gt;.&lt;object@293:11&gt;.onActivate`

以无显式实参的调用形式「options.model.refresh」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。 保留同一块中的正常源码顺序：语句位置「0」的操作「5db68eba17e0b5d64674ae2a」先于语句位置「1」的操作「0a11373a86d689e82b4871c9」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/settings-page.ts:296`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/216`。

### `apps/client/src/settings-page.ts::mountSettingsPage.&lt;object@300:38&gt;.&lt;object@302:11&gt;.onActivate`

以无显式实参的调用形式「options.model.reconnect」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/settings-page.ts:305`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/217`。

### `apps/client/src/settings-page.ts::mountSettingsPage.settingsRow`

将「document」作为第 1 个实参交给已绑定接口「ts:apps/client/src/settings-page#element」，对应捕获形参「document: Document」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「(label as HTMLLabelElement).htmlFor = labelFor」，捕获目标为「label.htmlFor」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「row」的初始化来源为「element(document, 'div', `wwc-settings-row ${className}`)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return row」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「18e71b07b0fffb1088972f03」先于语句位置「1」的操作「84d24133cda989a6c947aebd」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/settings-page.ts:324`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/218`。

### `apps/client/src/settings-page.ts::mountSettingsPage.collapsedRow`

将「document」作为第 1 个实参交给已绑定接口「ts:apps/client/src/settings-page#element」，对应捕获形参「document: Document」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「label.textContent = labelText」，捕获目标为「label.textContent」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「root」的初始化来源为「element(document, 'div', `wwc-settings-collapsed ${className}`)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return root」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「32414b0e1663525eaaaec1d4」先于语句位置「1」的操作「1a5452ea33ef2bbcba84affa」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/settings-page.ts:341`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/219`。

### `apps/client/src/settings-page.ts::mountSettingsPage.collapsedRow.&lt;arrow@362:37&gt;`

在调用形式「button.setAttribute」中提供第 1 个实参「'aria-expanded'」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 包含赋值/更新「content.hidden = !next」，捕获目标为「content.hidden」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「next」的初始化来源为「content.hidden」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留同一块中的正常源码顺序：语句位置「0」的操作「1486c18e2fe6c22359637d38」先于语句位置「1」的操作「4a4218b84d40542b8a05c4ed」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/settings-page.ts:362`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/220`。

### `apps/client/src/settings-page.ts::mountSettingsPage.localSaveRow`

构造捕获记录，字段按源码次序为「root ← root；feedback ← feedback」。不据构造形式推断物理持久化。 将「document」作为第 1 个实参交给已绑定接口「ts:apps/client/src/settings-page#element」，对应捕获形参「document: Document」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「save.type = 'button'」，捕获目标为「save.type」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「root」的初始化来源为「element(document, 'div', `wwc-settings-local-save ${className}`)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return { root, feedback }」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「root」关联路径「root」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「5f519bf43ee240876f175b35」先于语句位置「1」的操作「2144606084592e84d055e796」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/settings-page.ts:370`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/221`。

### `apps/client/src/settings-page.ts::mountSettingsPage.&lt;arrow@427:64&gt;`

构造捕获记录，字段按源码次序为「displayName ← generalName.input.value.trim()；appearance ← isThemePreference(generalAppearance.value) ? generalAppearance.value : 'system'；sendKey ← generalSend.value === 'mod-enter' ? 'mod-enter' : 'enter'」。不据构造形式推断物理持久化。 将「{\n        displayName: generalName.input.value.trim(),\n        appearance: isThemePreference(generalAppearance.value) ? generalAppearance.value : 'system',\n        sendKey: generalSend.value === 'mod-enter' ? 'mod-enter' : 'enter',\n      }」作为第 2 个实参交给已绑定接口「ts:apps/client/src/preferences#savePreferences」，对应捕获形参「value: Preferences」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「generalSave.feedback.textContent = '保存失败，请检查浏览器是否允许存储。'」，捕获目标为「generalSave.feedback.textContent」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「cb5d7d0f32a2edee6ef4a60f」先于语句位置「1」的操作「149076d755b4c722215fce6c」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/settings-page.ts:427`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/222`。

### `apps/client/src/settings-page.ts::mountSettingsPage.onGeneralNameInput`

包含赋值/更新「generalSave.feedback.textContent = ''」，捕获目标为「generalSave.feedback.textContent」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。

源码：`apps/client/src/settings-page.ts:437`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/223`。

### `apps/client/src/settings-page.ts::mountSettingsPage.&lt;arrow@506:45&gt;`

构造捕获记录，字段按源码次序为「workerConcurrencyLimit ← Number(concurrencyInput.value)」。不据构造形式推断物理持久化。 将「options.model.state」作为第 1 个实参交给已绑定接口「ts:apps/client/src/settings-page#settingsPagePresentation」，对应捕获形参「state: SettingsViewModelState」。该普通调用关系不替代进程或网络协议关系。 保留同一块中的正常源码顺序：语句位置「0」的操作「7d4ea10bfff414a85cb90e0b」先于语句位置「1」的操作「8df320cd1bcc7f65bad245c6」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/settings-page.ts:506`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/224`。

### `apps/client/src/settings-page.ts::mountSettingsPage.&lt;arrow@545:68&gt;`

在调用形式「executionDraft.set」中提供第 2 个实参「executionMode.value」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 包含赋值/更新「executionSave.feedback.textContent = LOCAL_DRAFT_SAVED_TEXT」，捕获目标为「executionSave.feedback.textContent」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「f169a9717b0dcccdb30b6989」先于语句位置「1」的操作「d03cbed5b58311c6d2c71f75」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/settings-page.ts:545`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/225`。

### `apps/client/src/settings-page.ts::mountSettingsPage.&lt;object@649:36&gt;.&lt;object@651:11&gt;.onSelect`

将「id」作为第 1 个实参交给已绑定接口「ts:apps/client/src/settings-page#mountSettingsPage.showDiagnosticsTab」，对应捕获形参「next: DiagnosticsTabId」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/settings-page.ts:659`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/226`。

### `apps/client/src/settings-page.ts::mountSettingsPage.&lt;object@707:31&gt;.&lt;object@709:11&gt;.onActivate`

以无显式实参的调用形式「options.model.refresh」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。 保留同一块中的正常源码顺序：语句位置「0」的操作「b7388cbfb4b1c0b17e398e7e」先于语句位置「1」的操作「17cf69df1d14a65a65b4d982」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/settings-page.ts:713`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/227`。

### `apps/client/src/settings-page.ts::mountSettingsPage.onUsageFirstOpen`

在调用形式「options.mountUsagePanel」中提供第 1 个实参「usageSlot」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 对捕获 binding「usageMountStarted」存在源更新「usageMountStarted = true」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(usageMountStarted || options.mountUsagePanel === undefined)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「0c72b4c076bed4f6a0e66123」先于语句位置「1」的操作「4906051128a9c2f9dc733699」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/settings-page.ts:751`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/228`。

### `apps/client/src/settings-page.ts::mountSettingsPage.onUsageFirstOpen.&lt;arrow@754:66&gt;`

以无显式实参的调用形式「binding.close」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。 对捕获 binding「usageBinding」存在源更新「usageBinding = binding」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(binding === null)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「6d929597d5b35bb89e938f02」先于语句位置「1」的操作「7dd2aedca3318ca309fb5163」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/settings-page.ts:754`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/229`。

### `apps/client/src/settings-page.ts::mountSettingsPage.showDiagnosticsTab`

构造捕获记录，字段按源码次序为「id ← 'run'；label ← '运行诊断'；panelId ← 'wwc-settings-diagnostics-run'」。不据构造形式推断物理持久化。 以无显式实参的调用形式「onUsageFirstOpen」调用已绑定接口「ts:apps/client/src/settings-page#mountSettingsPage.onUsageFirstOpen」；没有据调用存在断言激活、存储或网络效果。 包含赋值/更新「runPanel.hidden = next !== 'run'」，捕获目标为「runPanel.hidden」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 以字段投影形式「next」关联路径「next」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「cd977250c2df2c1ad4f6aa30」先于语句位置「1」的操作「31ba3f5a82f0b0552e26bd58」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/settings-page.ts:768`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/230`。

### `apps/client/src/settings-page.ts::mountSettingsPage.showDiagnosticsTab.&lt;object@769:27&gt;.onSelect`

将「id」作为第 1 个实参交给已绑定接口「ts:apps/client/src/settings-page#mountSettingsPage.showDiagnosticsTab」，对应捕获形参「next: DiagnosticsTabId」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/settings-page.ts:777`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/231`。

### `apps/client/src/settings-page.ts::mountSettingsPage.showCategory`

构造捕获记录，字段按源码次序为「description ← category.description」。不据构造形式推断物理持久化。 将「next」作为第 1 个实参交给已绑定接口「ts:apps/client/src/settings-page#categoryOf」，对应捕获形参「id: SettingsCategoryId」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「categorySelect.value = next」，捕获目标为「categorySelect.value」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「section」的初始化来源为「candidate.id === 'general'\n        ? generalSection\n        : candidate.id === 'providers'\n          ? providersSection\n          : candidate.id === 'execution'\n            ? executionSection\n            : candidate.id === 'storage' ? storageSection : diagnosticsSection」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「selectedCategory」存在源更新「selectedCategory = next」；循环和分支条件见操作上下文，未推执行次数或最终数值。 以字段投影形式「category.title」关联路径「category.title」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「(CATEGORIES_WITH_DESCRIPTION.has(next) ? { description: category.description } : {})」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。

源码：`apps/client/src/settings-page.ts:789`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/232`。

### `apps/client/src/settings-page.ts::mountSettingsPage.onCategoryChange`

将「next」作为第 1 个实参交给已绑定接口「ts:apps/client/src/settings-page#mountSettingsPage.showCategory」，对应捕获形参「next: SettingsCategoryId」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「next」的初始化来源为「categorySelect.value as SettingsCategoryId」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留同一块中的正常源码顺序：语句位置「0」的操作「3d3d9077c6902be671692ed0」先于语句位置「1」的操作「2e50bbda1967d284726661ca」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/settings-page.ts:810`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/233`。

### `apps/client/src/settings-page.ts::mountSettingsPage.renderDiagnostics`

构造捕获记录，字段按源码次序为「label ← '运行检查'；variant ← 'primary'；className ← 'wwc-settings-diagnostics-run-check'；busy ← presentation.busy」。不据构造形式推断物理持久化。 在调用形式「String」中提供第 1 个实参「state.settings.revision」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 包含赋值/更新「concurrencySave.disabled = concurrencyInput.disabled」，捕获目标为「concurrencySave.disabled」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「deviceOk」的初始化来源为「deviceProviders.online」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以字段投影形式「presentation.busy」关联路径「presentation.busy」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「bbd50e30bfc6b30b5c46ffc4」先于语句位置「1」的操作「86b055233e6c81e389ff2136」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/settings-page.ts:819`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/234`。

### `apps/client/src/settings-page.ts::mountSettingsPage.render`

构造捕获记录，字段按源码次序为「title ← '模型设置不可用'；message ← presentation.errorText ?? ''；actions ← [retry, reconnect]；visible ← presentation.errorText !== null；className ← 'wwc-settings-error'」。不据构造形式推断物理持久化。 将「state」作为第 1 个实参交给已绑定接口「ts:apps/client/src/settings-page#mountSettingsPage.renderDiagnostics」，对应捕获形参「state: SettingsViewModelState」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「retry.hidden = !presentation.retryVisible」，捕获目标为「retry.hidden」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「presentation」的初始化来源为「settingsPagePresentation(state)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「presentation.statusText」关联路径「presentation.statusText」；只描述捕获来源，不证明当时的字段值。

源码：`apps/client/src/settings-page.ts:858`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/235`。

### `apps/client/src/settings-page.ts::mountSettingsPage.&lt;object@893:9&gt;.close`

在调用形式「categorySelect.removeEventListener」中提供第 2 个实参「onCategoryChange」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 对捕获 binding「closed」存在源更新「closed = true」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「65d69661a0950dd7a3963f71」先于语句位置「1」的操作「93cbd7e258e30bb422cc7e66」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/settings-page.ts:894`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/236`。

### `apps/client/src/task-entry-page.ts::mountTaskEntryPage`

具有捕获记录构造「{\n    close() {\n      if (closed) return\n      closed = true\n      unsubscribe()\n      form.removeEventListener('submit', onSubmit)\n      clientSelect.removeEventListener('change', onClientChange)\n      repositorySelect.removeEventListener('change', onRepositoryChange)\n      baseInput.removeEventListener('input', onBaseEdit)\n      descriptionInput.r…［展示截断；完整操作保留］」；该记录的可枚举字段为空或保留开放形状，未把展开来源补成确定字段。 将「clientLabel」作为第 1 个实参交给已绑定接口「ts:apps/client/src/task-entry-page#mountTaskEntryPage.wireSelect」，对应捕获形参「label: HTMLLabelElement」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「baseLabel.htmlFor = baseInput.id」，捕获目标为「baseLabel.htmlFor」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「document」的初始化来源为「options.root.ownerDocument」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return {\n    close() {\n      if (closed) return\n      closed = true\n      unsubscribe()\n      form.removeEventListener('submit', onSubmit)\n      clientSelect.removeEventListener('change', onClientChange)\n      repositorySelect.removeEventListener('change', onRepositoryChange)\n      baseInput.removeEventListener('input', onBaseEdit)\n      description…［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「01bf20252729a2921f4e4f71」先于语句位置「1」的操作「960ef0f02b76a272fe4b490d」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/task-entry-page.ts:54`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/237`。

### `apps/client/src/task-entry-page.ts::mountTaskEntryPage.wireSelect`

包含赋值/更新「select.name = name」，捕获目标为「select.name」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「1cc6f6847171e57bbda2c270」先于语句位置「1」的操作「6c92ef253f7eb2711a2ea269」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/task-entry-page.ts:91`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/238`。

### `apps/client/src/task-entry-page.ts::mountTaskEntryPage.fillSelect`

在调用形式「select.append」中提供第 1 个实参「placeholder」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 包含赋值/更新「placeholder.textContent = emptyText」，捕获目标为「placeholder.textContent」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「option」的初始化来源为「document.createElement('option')」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(select.options.length === entries.length + 1\n      &amp;&amp; select.options[0]?.textContent === emptyText\n      &amp;&amp; entries.every((entry, index) =&gt; select.options[index + 1]?.value === entry.value\n        &amp;&amp; select.options[index + 1]?.textContent === entry.label)\n      &amp;&amp; (select.value === (selected ?? '')))」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「6c2e4625f5b2d416ebc05194」先于语句位置「1」的操作「09787d7f464af45cb77ec20b」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/task-entry-page.ts:141`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/239`。

### `apps/client/src/task-entry-page.ts::mountTaskEntryPage.setFieldError`

在调用形式「control.setAttribute」中提供第 2 个实参「failure.id」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 保留同一块中的正常源码顺序：语句位置「0」的操作「a3d05c7729e601d599718e2f」先于语句位置「1」的操作「af5682834a70a03fe84f6671」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/task-entry-page.ts:168`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/240`。

### `apps/client/src/task-entry-page.ts::mountTaskEntryPage.render`

将「clientSelect」作为第 1 个实参交给已绑定接口「ts:apps/client/src/task-entry-page#mountTaskEntryPage.fillSelect」，对应捕获形参「select: HTMLSelectElement」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「baseInput.value = snapshot.selection.baseBranch」，捕获目标为「baseInput.value」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「anchor」的初始化来源为「snapshot.anchor」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「reportedAnchor」存在源更新「reportedAnchor = anchor」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「06b0a5b09a6d420dafc1235c」先于语句位置「1」的操作「2850d2f4ad0cc0dd5fb4bdc7」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「clientSelect」作为第 1 个实参交给已绑定接口「ts:apps/client/src/task-entry-page#mountTaskEntryPage.setFieldError」，对应捕获形参「control: HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/task-entry-page.ts:178`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/241`。

### `apps/client/src/task-entry-page.ts::mountTaskEntryPage.render.&lt;arrow@193:19&gt;`

构造捕获记录，字段按源码次序为「value ← device.clientId；label ← device.displayName」。不据构造形式推断物理持久化。 以字段投影形式「device.clientId」关联路径「device.clientId」；只描述捕获来源，不证明当时的字段值。

源码：`apps/client/src/task-entry-page.ts:193`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/242`。

### `apps/client/src/task-entry-page.ts::mountTaskEntryPage.render.&lt;arrow@203:32&gt;`

构造捕获记录，字段按源码次序为「value ← repository.repositoryBindingId；label ← repository.displayName」。不据构造形式推断物理持久化。 以字段投影形式「repository.repositoryBindingId」关联路径「repository.repositoryBindingId」；只描述捕获来源，不证明当时的字段值。

源码：`apps/client/src/task-entry-page.ts:203`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/243`。

### `apps/client/src/task-entry-page.ts::mountTaskEntryPage.render.&lt;arrow@219:37&gt;`

构造捕获记录，字段按源码次序为「value ← option.routeId；label ← option.detail === '' ? option.label : `${option.label} — ${option.detail}`」。不据构造形式推断物理持久化。 以字段投影形式「option.routeId」关联路径「option.routeId」；只描述捕获来源，不证明当时的字段值。

源码：`apps/client/src/task-entry-page.ts:219`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/244`。

### `apps/client/src/task-entry-page.ts::mountTaskEntryPage.onSubmit`

以无显式实参的调用形式「event.preventDefault」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。 保留同一块中的正常源码顺序：语句位置「0」的操作「dba518bd7570113b689414d0」先于语句位置「1」的操作「bf9f71e01df3edd22f17b248」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/task-entry-page.ts:257`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/245`。

### `apps/client/src/task-entry-page.ts::mountTaskEntryPage.onClientChange`

将「clientSelect」作为第 1 个实参交给已绑定接口「ts:apps/client/src/task-entry-page#optionValue」，对应捕获形参「select: HTMLSelectElement」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/task-entry-page.ts:261`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/246`。

### `apps/client/src/task-entry-page.ts::mountTaskEntryPage.onRepositoryChange`

将「repositorySelect」作为第 1 个实参交给已绑定接口「ts:apps/client/src/task-entry-page#optionValue」，对应捕获形参「select: HTMLSelectElement」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/task-entry-page.ts:264`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/247`。

### `apps/client/src/task-entry-page.ts::mountTaskEntryPage.onBaseEdit`

在调用形式「options.model.setBaseBranch」中提供第 1 个实参「baseInput.value」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`apps/client/src/task-entry-page.ts:267`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/248`。

### `apps/client/src/task-entry-page.ts::mountTaskEntryPage.onDescriptionEdit`

在调用形式「options.model.setDescription」中提供第 1 个实参「descriptionInput.value」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`apps/client/src/task-entry-page.ts:270`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/249`。

### `apps/client/src/task-entry-page.ts::mountTaskEntryPage.onRouteChange`

将「routeSelect」作为第 1 个实参交给已绑定接口「ts:apps/client/src/task-entry-page#optionValue」，对应捕获形参「select: HTMLSelectElement」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/task-entry-page.ts:273`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/250`。

### `apps/client/src/task-entry-page.ts::mountTaskEntryPage.&lt;object@286:9&gt;.close`

在调用形式「form.removeEventListener」中提供第 2 个实参「onSubmit」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 对捕获 binding「closed」存在源更新「closed = true」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「8f2910696d5d7b402726bb4b」先于语句位置「1」的操作「e11741aa459ba2aee0b8b359」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/task-entry-page.ts:287`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/251`。

### `apps/client/src/task-entry-view-model.ts::createTaskEntryViewModel`

构造捕获记录，字段按源码次序为「clientId ← null；repositoryBindingId ← null；baseBranch ← ''；description ← ''；modelRouteId ← modelRouteOptions[0]?.routeId ?? null」。不据构造形式推断物理持久化。 以无显式实参的调用形式「project」调用已绑定接口「ts:apps/client/src/task-entry-view-model#createTaskEntryViewModel.project」；没有据调用存在断言激活、存储或网络效果。 捕获 binding「clients」的初始化来源为「options.clients」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return {\n    get state() {\n      return currentState\n    },\n    subscribe(listener) {\n      if (closed) return () =&gt; {}\n      listeners.add(listener)\n      listener(currentState)\n      return () =&gt; { listeners.delete(listener) }\n    },\n    selectClient(clientId) {\n      if (closed || status === 'submitting') return\n      const device = clientId =…［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「093fb61af2da7504904fe672」先于语句位置「1」的操作「adad73748f6d95af31b8e6b2」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/task-entry-view-model.ts:80`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/252`。

### `apps/client/src/task-entry-view-model.ts::createTaskEntryViewModel.project`

构造捕获记录，字段按源码次序为「status ← status；occupiedDevices ← Object.freeze(\n        clients.state.devices.filter(deviceSupportsTaskStart),\n      )；devicesStatus ← clients.state.devicesStatus；repositories ← repositories.state.repositories；repositoriesStatus ← repositories.state.status；selection ← selection；modelRouteOptions ← modelRouteOptions；failure ← failure；anchor ← anchor」。不据构造形式推断物理持久化。 在调用形式「Object.freeze」中提供第 1 个实参「{\n      status,\n      occupiedDevices: Object.freeze(\n        clients.state.devices.filter(deviceSupportsTaskStart),\n      ),\n      devicesStatus: clients.state.devicesStatus,\n      repositories: repositories.state.repositories,\n      repositoriesStatus: repositories.state.status,\n      selection,\n      modelRouteOptions,\n      failure,\n      anch…［展示截断；完整操作保留］」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return Object.freeze({\n      status,\n      occupiedDevices: Object.freeze(\n        clients.state.devices.filter(deviceSupportsTaskStart),\n      ),\n      devicesStatus: clients.state.devicesStatus,\n      repositories: repositories.state.repositories,\n      repositoriesStatus: repositories.state.status,\n      selection,\n      modelRouteOptions,\n     …［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「status」关联路径「status」；只描述捕获来源，不证明当时的字段值。

源码：`apps/client/src/task-entry-view-model.ts:108`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/253`。

### `apps/client/src/task-entry-view-model.ts::createTaskEntryViewModel.publish`

以无显式实参的调用形式「project」调用已绑定接口「ts:apps/client/src/task-entry-view-model#createTaskEntryViewModel.project」；没有据调用存在断言激活、存储或网络效果。 对捕获 binding「currentState」存在源更新「currentState = project()」；循环和分支条件见操作上下文，未推执行次数或最终数值。 保留同一块中的正常源码顺序：语句位置「0」的操作「4559c5acba30f6802ef42cd9」先于语句位置「1」的操作「2fb3a974b359419cdb4b7987」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/task-entry-view-model.ts:124`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/254`。

### `apps/client/src/task-entry-view-model.ts::createTaskEntryViewModel.setSelection`

在调用形式「Object.freeze」中提供第 1 个实参「next」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 对捕获 binding「selection」存在源更新「selection = Object.freeze(next)」；循环和分支条件见操作上下文，未推执行次数或最终数值。

源码：`apps/client/src/task-entry-view-model.ts:129`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/255`。

### `apps/client/src/task-entry-view-model.ts::createTaskEntryViewModel.reconcileWithSnapshots`

构造捕获记录，字段按源码次序为「clientId ← null；repositoryBindingId ← null；baseBranch ← ''」。不据构造形式推断物理持久化。 将「{\n        ...selection,\n        clientId: null,\n        repositoryBindingId: null,\n        baseBranch: '',\n      }」作为第 1 个实参交给已绑定接口「ts:apps/client/src/task-entry-view-model#createTaskEntryViewModel.setSelection」，对应捕获形参「next: TaskEntrySelection」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「droppedClient」的初始化来源为「null」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「droppedClient」存在源更新「droppedClient = selection.clientId」；循环和分支条件见操作上下文，未推执行次数或最终数值。 以「return droppedClient」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留记录复制/展开来源「selection」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「8ff79070aad78b045f0ae92c」先于语句位置「1」的操作「1bb668d80de4a0d26acea220」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/task-entry-view-model.ts:139`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/256`。

### `apps/client/src/task-entry-view-model.ts::createTaskEntryViewModel.&lt;arrow@168:47&gt;`

以无显式实参的调用形式「reconcileWithSnapshots」调用已绑定接口「ts:apps/client/src/task-entry-view-model#createTaskEntryViewModel.reconcileWithSnapshots」；没有据调用存在断言激活、存储或网络效果。 捕获 binding「droppedClient」的初始化来源为「reconcileWithSnapshots()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「d637c9637bc23981fb6e0103」先于语句位置「1」的操作「ae7a05bc2645fe08afcce671」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 以无显式实参的调用形式「publish」调用已绑定接口「ts:apps/client/src/task-entry-view-model#createTaskEntryViewModel.publish」；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/task-entry-view-model.ts:168`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/257`。

### `apps/client/src/task-entry-view-model.ts::createTaskEntryViewModel.&lt;arrow@177:57&gt;`

构造捕获记录，字段按源码次序为「repositoryBindingId ← first.repositoryBindingId；baseBranch ← first.defaultBranch」。不据构造形式推断物理持久化。 将「{\n          ...selection,\n          repositoryBindingId: first.repositoryBindingId,\n          baseBranch: first.defaultBranch,\n        }」作为第 1 个实参交给已绑定接口「ts:apps/client/src/task-entry-view-model#createTaskEntryViewModel.setSelection」，对应捕获形参「next: TaskEntrySelection」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「first」的初始化来源为「repositories.state.repositories.find(repositorySupportsTaskStart)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「first.repositoryBindingId」关联路径「first.repositoryBindingId」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「selection」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。 以无显式实参的调用形式「reconcileWithSnapshots」调用已绑定接口「ts:apps/client/src/task-entry-view-model#createTaskEntryViewModel.reconcileWithSnapshots」；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/task-entry-view-model.ts:177`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/258`。

### `apps/client/src/task-entry-view-model.ts::createTaskEntryViewModel.defaultBranchOf`

在调用形式「repositories.state.repositories.find」中提供第 1 个实参「candidate =&gt; candidate.repositoryBindingId === repositoryBindingId」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 条件「(repositoryBindingId === null)」的捕获提前退出分支为「return：''」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return ''」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「3c373dc90c2f4640a0a4930e」先于语句位置「1」的操作「06ab3a52bbb8e973a5d1ea37」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/task-entry-view-model.ts:199`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/259`。

### `apps/client/src/task-entry-view-model.ts::createTaskEntryViewModel.&lt;object@206:9&gt;.state`

以「return currentState」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`apps/client/src/task-entry-view-model.ts:207`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/260`。

### `apps/client/src/task-entry-view-model.ts::createTaskEntryViewModel.&lt;object@206:9&gt;.subscribe`

在调用形式「listeners.add」中提供第 1 个实参「listener」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 条件「(closed)」的捕获提前退出分支为「return：() =&gt; {}」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return () =&gt; {}」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「852ac9cd146cc70943f31520」先于语句位置「1」的操作「b3811229697c3c8277986700」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/task-entry-view-model.ts:210`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/261`。

### `apps/client/src/task-entry-view-model.ts::createTaskEntryViewModel.&lt;object@206:9&gt;.subscribe.&lt;arrow@214:13&gt;`

在调用形式「listeners.delete」中提供第 1 个实参「listener」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`apps/client/src/task-entry-view-model.ts:214`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/262`。

### `apps/client/src/task-entry-view-model.ts::createTaskEntryViewModel.&lt;object@206:9&gt;.selectClient`

构造捕获记录，字段按源码次序为「clientId ← nextClientId；repositoryBindingId ← null；baseBranch ← ''」。不据构造形式推断物理持久化。 将「{\n        ...selection,\n        clientId: nextClientId,\n        repositoryBindingId: null,\n        baseBranch: '',\n      }」作为第 1 个实参交给已绑定接口「ts:apps/client/src/task-entry-view-model#createTaskEntryViewModel.setSelection」，对应捕获形参「next: TaskEntrySelection」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「device」的初始化来源为「clientId === null\n        ? null\n        : clients.state.devices.find(\n            candidate =&gt; candidate.clientId === clientId &amp;&amp; deviceSupportsTaskStart(candidate),\n          ) ?? null」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「failure」存在源更新「failure = null」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(closed || status === 'submitting')」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「nextClientId」关联路径「nextClientId」；只描述捕获来源，不证明当时的字段值。 以无显式实参的调用形式「publish」调用已绑定接口「ts:apps/client/src/task-entry-view-model#createTaskEntryViewModel.publish」；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/task-entry-view-model.ts:216`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/263`。

### `apps/client/src/task-entry-view-model.ts::createTaskEntryViewModel.&lt;object@206:9&gt;.selectClient.&lt;arrow@221:12&gt;`

将「candidate」作为第 1 个实参交给已绑定接口「ts:apps/client/src/task-entry-view-model#deviceSupportsTaskStart」，对应捕获形参「device: ControlPlaneDeviceSummary」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/task-entry-view-model.ts:221`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/264`。

### `apps/client/src/task-entry-view-model.ts::createTaskEntryViewModel.&lt;object@206:9&gt;.selectRepository`

构造捕获记录，字段按源码次序为「repositoryBindingId ← repositoryBindingId；baseBranch ← defaultBranchOf(repositoryBindingId)」。不据构造形式推断物理持久化。 将「{\n        ...selection,\n        repositoryBindingId,\n        // A different target repository restarts the base-branch draft on its\n        // own default; re-selecting the same choice keeps the user's draft.\n        baseBranch: defaultBranchOf(repositoryBindingId),\n      }」作为第 1 个实参交给已绑定接口「ts:apps/client/src/task-entry-view-model#createTaskEntryViewModel.setSelection」，对应捕获形参「next: TaskEntrySelection」。该普通调用关系不替代进程或网络协议关系。 对捕获 binding「failure」存在源更新「failure = null」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(closed || status === 'submitting')」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「repositoryBindingId」关联路径「repositoryBindingId」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「selection」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。 将「repositoryBindingId」作为第 1 个实参交给已绑定接口「ts:apps/client/src/task-entry-view-model#createTaskEntryViewModel.defaultBranchOf」，对应捕获形参「repositoryBindingId: string | null」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/task-entry-view-model.ts:237`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/265`。

### `apps/client/src/task-entry-view-model.ts::createTaskEntryViewModel.&lt;object@206:9&gt;.setBaseBranch`

构造捕获记录，字段按源码次序为「baseBranch ← value」。不据构造形式推断物理持久化。 将「{ ...selection, baseBranch: value }」作为第 1 个实参交给已绑定接口「ts:apps/client/src/task-entry-view-model#createTaskEntryViewModel.setSelection」，对应捕获形参「next: TaskEntrySelection」。该普通调用关系不替代进程或网络协议关系。 条件「(closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「value」关联路径「value」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「selection」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「b8ea8c1763b73876920ceb5f」先于语句位置「1」的操作「60d20ee1c24023f5fdd303fd」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 以无显式实参的调用形式「publish」调用已绑定接口「ts:apps/client/src/task-entry-view-model#createTaskEntryViewModel.publish」；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/task-entry-view-model.ts:250`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/266`。

### `apps/client/src/task-entry-view-model.ts::createTaskEntryViewModel.&lt;object@206:9&gt;.setDescription`

构造捕获记录，字段按源码次序为「description ← value」。不据构造形式推断物理持久化。 将「{ ...selection, description: value }」作为第 1 个实参交给已绑定接口「ts:apps/client/src/task-entry-view-model#createTaskEntryViewModel.setSelection」，对应捕获形参「next: TaskEntrySelection」。该普通调用关系不替代进程或网络协议关系。 条件「(closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「value」关联路径「value」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「selection」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「e080f69041e858e665286250」先于语句位置「1」的操作「e16994d5a574e486c79d3e48」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 以无显式实参的调用形式「publish」调用已绑定接口「ts:apps/client/src/task-entry-view-model#createTaskEntryViewModel.publish」；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/task-entry-view-model.ts:255`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/267`。

### `apps/client/src/task-entry-view-model.ts::createTaskEntryViewModel.&lt;object@206:9&gt;.selectModelRoute`

构造捕获记录，字段按源码次序为「modelRouteId ← nextRouteId」。不据构造形式推断物理持久化。 将「{ ...selection, modelRouteId: nextRouteId }」作为第 1 个实参交给已绑定接口「ts:apps/client/src/task-entry-view-model#createTaskEntryViewModel.setSelection」，对应捕获形参「next: TaskEntrySelection」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「known」的初始化来源为「routeId === null\n        ? null\n        : modelRouteOptions.find(option =&gt; option.routeId === routeId) ?? null」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「failure」存在源更新「failure = null」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(closed || status === 'submitting')」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「nextRouteId」关联路径「nextRouteId」；只描述捕获来源，不证明当时的字段值。 以无显式实参的调用形式「publish」调用已绑定接口「ts:apps/client/src/task-entry-view-model#createTaskEntryViewModel.publish」；没有据调用存在断言激活、存储或网络效果。

源码：`apps/client/src/task-entry-view-model.ts:260`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/268`。

### `apps/client/src/task-entry-view-model.ts::createTaskEntryViewModel.&lt;object@206:9&gt;.submit`

构造捕获记录，字段按源码次序为「clientId ← device.clientId；repositoryBindingId ← repository.repositoryBindingId；baseBranch ← baseBranch；description ← description；modelRouteId ← selection.modelRouteId」。不据构造形式推断物理持久化。 以无显式实参的调用形式「publish」调用已绑定接口「ts:apps/client/src/task-entry-view-model#createTaskEntryViewModel.publish」；没有据调用存在断言激活、存储或网络效果。 捕获 binding「device」的初始化来源为「selection.clientId === null\n        ? undefined\n        : clients.state.devices.find(\n            candidate =&gt; candidate.clientId === selection.clientId\n              &amp;&amp; deviceSupportsTaskStart(candidate),\n          )」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「failure」存在源更新「failure = 'no-occupied-client'」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(closed || status !== 'editing')」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「device.clientId」关联路径「device.clientId」；只描述捕获来源，不证明当时的字段值。

源码：`apps/client/src/task-entry-view-model.ts:271`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/269`。

### `apps/client/src/task-entry-view-model.ts::createTaskEntryViewModel.&lt;object@206:9&gt;.submit.&lt;arrow@276:12&gt;`

将「candidate」作为第 1 个实参交给已绑定接口「ts:apps/client/src/task-entry-view-model#deviceSupportsTaskStart」，对应捕获形参「device: ControlPlaneDeviceSummary」。该普通调用关系不替代进程或网络协议关系。

源码：`apps/client/src/task-entry-view-model.ts:276`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/270`。

### `apps/client/src/task-entry-view-model.ts::createTaskEntryViewModel.&lt;object@206:9&gt;.submit.&lt;arrow@321:35&gt;`

以无显式实参的调用形式「publish」调用已绑定接口「ts:apps/client/src/task-entry-view-model#createTaskEntryViewModel.publish」；没有据调用存在断言激活、存储或网络效果。 对捕获 binding「anchor」存在源更新「anchor = created」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「20afd6992b2c93ed1f96c79d」先于语句位置「1」的操作「a0ef4a5f4d2cc7b4d0dd26c7」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/task-entry-view-model.ts:321`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/271`。

### `apps/client/src/task-entry-view-model.ts::createTaskEntryViewModel.&lt;object@206:9&gt;.submit.&lt;arrow@326:9&gt;`

以无显式实参的调用形式「publish」调用已绑定接口「ts:apps/client/src/task-entry-view-model#createTaskEntryViewModel.publish」；没有据调用存在断言激活、存储或网络效果。 对捕获 binding「status」存在源更新「status = 'editing'」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「c7d6d6cab493ca8b91484bc5」先于语句位置「1」的操作「6d012f99e0275cf83dabfedf」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/task-entry-view-model.ts:326`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/272`。

### `apps/client/src/task-entry-view-model.ts::createTaskEntryViewModel.&lt;object@206:9&gt;.dismissFailure`

以无显式实参的调用形式「publish」调用已绑定接口「ts:apps/client/src/task-entry-view-model#createTaskEntryViewModel.publish」；没有据调用存在断言激活、存储或网络效果。 对捕获 binding「failure」存在源更新「failure = null」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(closed || failure === null)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「310d3b48e963f2ac4b611518」先于语句位置「1」的操作「8366f364ba9b15697a033603」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/task-entry-view-model.ts:335`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/273`。

### `apps/client/src/task-entry-view-model.ts::createTaskEntryViewModel.&lt;object@206:9&gt;.refresh`

在调用形式「Promise.allSettled」中提供第 1 个实参「[clients.refresh(), repositories.refresh()]」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 条件「(closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「13418336a54fcc24155fe92c」先于语句位置「1」的操作「29958120a3a5a2a4c1902834」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/task-entry-view-model.ts:340`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/274`。

### `apps/client/src/task-entry-view-model.ts::createTaskEntryViewModel.&lt;object@206:9&gt;.start`

以无显式实参的调用形式「publish」调用已绑定接口「ts:apps/client/src/task-entry-view-model#createTaskEntryViewModel.publish」；没有据调用存在断言激活、存储或网络效果。 条件「(closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「66153626670de00f0e9ca643」先于语句位置「1」的操作「24f13dd5ef08e7dd6249d049」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/task-entry-view-model.ts:344`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/275`。

### `apps/client/src/task-entry-view-model.ts::createTaskEntryViewModel.&lt;object@206:9&gt;.close`

以无显式实参的调用形式「unsubscribeClients」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。 对捕获 binding「closed」存在源更新「closed = true」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「762f69e314b3138a7455e233」先于语句位置「1」的操作「a0e8ce969051037f2109b3ac」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`apps/client/src/task-entry-view-model.ts:349`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/276`。

### `crates/kernel/src/lib.rs::Kernel.new`

构造捕获记录，字段按源码次序为「options ← options；model_port ← model_port；action_gate ← action_gate；runtime ← Arc::new(Mutex::new(None))；closed ← AtomicBool::new(false)」。不据构造形式推断物理持久化。 在调用形式「std::fs::symlink_metadata」中提供第 1 个实参「&amp;options.helper_executable」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 包含赋值/更新「options.event_capacity = options\n            .event_capacity\n            .clamp(MIN_EVENT_CAPACITY, MAX_EVENT_CAPACITY)」，捕获目标为「options.event_capacity」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「helper_metadata」的初始化来源为「std::fs::symlink_metadata(&amp;options.helper_executable).map_err(|_| {\n                KernelFailure::new(\n                    "HELPER_NOT_FOUND",\n                    format!(\n                        "kernel helper executable does not exist: {}",\n                        options.helper_executable.display()\n                    ),\n                )\n       …［展示截断；完整操作保留］」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「!options.home.is_absolute()」的捕获提前退出分支为「Err_return：Err(KernelFailure::new(\n                "INVALID_HOME",\n                format!("kernel home must be absolute: {}", options.home.display()),\n            ))」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(KernelFailure::new(\n                "INVALID_HOME",\n                format!("kernel home must be absolute: {}", options.home.display()),\n            ))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「options」关联路径「options」；只描述捕获来源，不证明当时的字段值。

源码：`crates/kernel/src/lib.rs:825`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/277`。

### `crates/kernel/src/lib.rs::&lt;closure_expression@846:75&gt;`

在调用形式「KernelFailure::new」中提供第 1 个实参「"HELPER_NOT_FOUND"」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/kernel/src/lib.rs:846`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/278`。

### `crates/kernel/src/lib.rs::&lt;closure_expression@883:56&gt;`

在调用形式「KernelFailure::new」中提供第 1 个实参「"HOME_CREATE_FAILED"」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/kernel/src/lib.rs:883`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/279`。

### `crates/kernel/src/lib.rs::&lt;closure_expression@889:54&gt;`

在调用形式「KernelFailure::new」中提供第 1 个实参「"HOME_PERMISSION_FAILED"」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/kernel/src/lib.rs:889`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/280`。

### `crates/kernel/src/lib.rs::Kernel.create_session`

将「async {\n            let runtime = self.runtime().await?;\n            let config = Self::session_config(&amp;runtime, &amp;options).await?;\n            let thread = runtime\n                .manager\n                .start_thread(StartThreadOptions::new(config.clone()))\n                .await\n                .map_err(|error| KernelFailure::new("SESSION_CREATE_FA…［展示截断；完整操作保留］」作为第 1 个实参交给已绑定接口「rust:crates/kernel/src/lib#Kernel.guard」，对应捕获形参「future: impl Future&lt;Output = KernelResult&lt;T&gt;&gt; + Send + 'a」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「runtime」的初始化来源为「self.runtime().await?」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留同一块中的正常源码顺序：语句位置「0」的操作「3e99b2b9a61252231c3ffd91」先于语句位置「1」的操作「41121ec9e187d82b66bf76b6」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/kernel/src/lib.rs:1220`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/281`。

### `crates/kernel/src/lib.rs::&lt;closure_expression@1228:26&gt;`

在调用形式「KernelFailure::new」中提供第 1 个实参「"SESSION_CREATE_FAILED"」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/kernel/src/lib.rs:1228`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/282`。

### `crates/kernel/src/lib.rs::Kernel.submit_turn`

将「async {\n            if text.trim().is_empty() {\n                return Err(KernelFailure::new(\n                    "EMPTY_INPUT",\n                    "turn input must contain text",\n                ));\n            }\n            let runtime = self.runtime().await?;\n            let session = self.session(&amp;runtime, session_id).await?;\n            self.…［展示截断；完整操作保留］」作为第 1 个实参交给已绑定接口「rust:crates/kernel/src/lib#Kernel.guard」，对应捕获形参「future: impl Future&lt;Output = KernelResult&lt;T&gt;&gt; + Send + 'a」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「runtime」的初始化来源为「self.runtime().await?」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「text.trim().is_empty()」的捕获提前退出分支为「Err_return：Err(KernelFailure::new(\n                    "EMPTY_INPUT",\n                    "turn input must contain text",\n                ))」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(KernelFailure::new(\n                    "EMPTY_INPUT",\n                    "turn input must contain text",\n                ))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「b70b531acd78cb09cd274ead」先于语句位置「1」的操作「526eeb183aa40e7eaa383778」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/kernel/src/lib.rs:1333`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/283`。

### `crates/kernel/src/lib.rs::&lt;closure_expression@1353:26&gt;`

在调用形式「KernelFailure::new」中提供第 1 个实参「"TURN_SUBMIT_FAILED"」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/kernel/src/lib.rs:1353`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/284`。

### `crates/kernel/src/lib.rs::Kernel.reconcile_turn_exact`

构造捕获记录，字段按源码次序为「turn_id ← turn_id；thread_settings ← ThreadSettingsOverrides::default()；trace ← None；submit_change_batch ← options.submit_change_batch」。不据构造形式推断物理持久化。 将「async {\n            if turn_id.trim().is_empty() || text.trim().is_empty() {\n                return Err(KernelFailure::new(\n                    "INVALID_EXACT_TURN",\n                    "exact turn identity and input must be non-empty",\n                ));\n            }\n            let runtime = self.runtime().await?;\n            let session = self.s…［展示截断；完整操作保留］」作为第 1 个实参交给已绑定接口「rust:crates/kernel/src/lib#Kernel.guard」，对应捕获形参「future: impl Future&lt;Output = KernelResult&lt;T&gt;&gt; + Send + 'a」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「recovered」的初始化来源为「matches!(durable, DurableTurnInspection::InProgress)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「turn_id.trim().is_empty() || text.trim().is_empty()」的捕获提前退出分支为「Err_return：Err(KernelFailure::new(\n                    "INVALID_EXACT_TURN",\n                    "exact turn identity and input must be non-empty",\n                ))」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(KernelFailure::new(\n                    "INVALID_EXACT_TURN",\n                    "exact turn identity and input must be non-empty",\n                ))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「turn_id」关联路径「turn_id」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「d1775377834dacaf155ffc61」先于语句位置「1」的操作「508d2a53b0b9ed917e98651e」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/kernel/src/lib.rs:1369`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/285`。

### `crates/kernel/src/lib.rs::&lt;closure_expression@1390:26&gt;`

在调用形式「KernelFailure::new」中提供第 1 个实参「"TURN_HISTORY_LOOKUP_FAILED"」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/kernel/src/lib.rs:1390`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/286`。

### `crates/kernel/src/lib.rs::&lt;closure_expression@1421:30&gt;`

在调用形式「KernelFailure::new」中提供第 1 个实参「"TURN_RECONCILE_SUBMIT_FAILED"」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/kernel/src/lib.rs:1421`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/287`。

### `crates/winwincode-codex/src/adapter.rs::ProductionCodexAdapter.open`

构造捕获记录，字段按源码次序为「config ← config；device_extension_directory ← None；kernel ← kernel；bridge ← bridge；action_gate ← action_gate；store ← store；outbox ← outbox；candidate_artifacts ← candidate_artifacts；diagnostic_artifacts ← diagnostic_artifacts；workrun_projector ← WorkRunRuntimeProjector::new()；installation ← ProductionCodexInstallation {\n                capability_catalog,\n                runtime_trace_outbox: WorkerRuntimeTraceOutbox::new(),\n            }；runs ← HashMap::new()」；其余字段见完整操作。不据构造形式推断物理持久化。 将「action_gate.clone()」作为第 3 个实参交给已绑定接口「rust:crates/kernel/src/lib#Kernel.new」，对应捕获形参「action_gate: Arc&lt;dyn KernelActionGate&gt;」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「config.helper_executable = seal_helper(\n            &amp;config.helper_executable,\n            Some(config.helper_bytes.as_ref()),\n            &amp;config.data_directory,\n            &amp;config.helper_release_manifest,\n        )?」，捕获目标为「config.helper_executable」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「capability_catalog」的初始化来源为「WorkerCapabilityCatalog::discover(\n            &amp;config.registered_capabilities,\n            config.discovered_capabilities.clone(),\n        )\n        .map_err(|_| invalid_configuration())?」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以字段投影形式「config」关联路径「config」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「6c61f600f85c2bbc1739ad94」先于语句位置「1」的操作「a8ec7053537286f52680f2d2」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-codex/src/adapter.rs:412`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/288`。

### `crates/winwincode-codex/src/adapter.rs::&lt;closure_expression@418:66&gt;`

以无显式实参的调用形式「unavailable」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-codex/src/adapter.rs:418`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/289`。

### `crates/winwincode-codex/src/adapter.rs::&lt;closure_expression@419:63&gt;`

以无显式实参的调用形式「unavailable」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-codex/src/adapter.rs:419`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/290`。

### `crates/winwincode-codex/src/adapter.rs::&lt;closure_expression@430:18&gt;`

以无显式实参的调用形式「invalid_configuration」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-codex/src/adapter.rs:430`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/291`。

### `crates/winwincode-codex/src/adapter.rs::&lt;closure_expression@453:22&gt;`

以无显式实参的调用形式「unavailable」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-codex/src/adapter.rs:453`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/292`。

### `crates/winwincode-codex/src/adapter.rs::&lt;closure_expression@464:22&gt;`

在调用形式「ProductionCodexError::new」中提供第 1 个实参「ProductionCodexErrorKind::Kernel」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-codex/src/adapter.rs:464`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/293`。

### `crates/winwincode-codex/src/adapter.rs::ProductionCodexAdapter.session_for_thread`

将「thread_id」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-codex/src/adapter#ProductionCodexAdapter.run_key_for_thread」，对应捕获形参「thread_id: &amp;CodexThreadId」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「run_key」的初始化来源为「self.run_key_for_thread(thread_id)?」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留同一块中的正常源码顺序：语句位置「0」的操作「c277d3edd6782d9be853e675」先于语句位置「1」的操作「c60932743a189f286698cf68」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-codex/src/adapter.rs:561`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/294`。

### `crates/winwincode-codex/src/adapter.rs::&lt;closure_expression@569:18&gt;`

以无显式实参的调用形式「run.record.kernel_session_id.clone」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-codex/src/adapter.rs:569`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/295`。

### `crates/winwincode-codex/src/adapter.rs::ProductionCodexAdapter.persist_run`

在调用形式「self.runs.get」中提供第 1 个实参「run_key」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「run」的初始化来源为「self.runs.get(run_key).ok_or_else(unknown_thread)?」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留同一块中的正常源码顺序：语句位置「0」的操作「3b0517f7461803cfa8aa686c」先于语句位置「1」的操作「6bc1047dee119c3be14a3b82」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-codex/src/adapter.rs:1031`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/296`。

### `crates/winwincode-codex/src/adapter.rs::&lt;ProductionCodexAdapter as CodexCoreAdapter&gt;.ensure_thread`

构造捕获记录，字段按源码次序为「job ← start.job.clone()；workspace_revision ← start.workspace_revision.clone()；canonical_thread_id ← thread_id.clone()；job_digest ← job_digest；workspace ← workspace；repository_rule_pack ← repository_rule_pack；role_policy ← role_policy；agent_config ← agent_config.clone()；kernel_session_id ← session.session_id.clone()；rollout_path ← session.rollout_path.map(PathBuf::from)；submission_id ← Uuid::now_v7().to_string()；submission_digest ← None」；其余字段见完整操作。不据构造形式推断物理持久化。 将「&amp;self.config」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-codex/src/adapter#production_agent_session_config」，对应捕获形参「config: &amp;ProductionCodexConfig」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「frozen_workspace」的初始化来源为「record\n                .final_candidate_freeze\n                .as_ref()\n                .is_some_and(|freeze| freeze.result_revision == *start.workspace_revision)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「let Some(run) = self.runs.get(&amp;run_key)」的捕获提前退出分支为「Err_return：Err(conflict())」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Ok(CodexThreadSession {\n                    thread_id: run.binding.canonical_thread_id.clone(),\n                    agent_config: run.record.agent_config.clone(),\n                })」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「start.lease.clone()」关联路径「start.lease」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「5488042574b3a132fb11740c」先于语句位置「1」的操作「fb16970bfb120b20782524cc」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「start」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-codex/src/adapter#session_identity」，对应捕获形参「start: CodexThreadStart&lt;'_&gt;」。该普通调用关系不替代进程或网络协议关系。

源码：`crates/winwincode-codex/src/adapter.rs:3334`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/297`。

### `crates/winwincode-codex/src/adapter.rs::&lt;closure_expression@3342:22&gt;`

以无显式实参的调用形式「unavailable」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-codex/src/adapter.rs:3342`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/298`。

### `crates/winwincode-codex/src/adapter.rs::&lt;closure_expression@3347:70&gt;`

以无显式实参的调用形式「invalid_job」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-codex/src/adapter.rs:3347`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/299`。

### `crates/winwincode-codex/src/adapter.rs::&lt;closure_expression@3375:22&gt;`

以无显式实参的调用形式「unavailable」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-codex/src/adapter.rs:3375`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/300`。

### `crates/winwincode-codex/src/adapter.rs::&lt;closure_expression@3461:22&gt;`

以无显式实参的调用形式「kernel_error」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-codex/src/adapter.rs:3461`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/301`。

### `crates/winwincode-codex/src/adapter.rs::&lt;ProductionCodexAdapter as CodexCoreAdapter&gt;.submit_turn`

将「&amp;run_key」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-codex/src/adapter#ProductionCodexAdapter.persist_run」，对应捕获形参「run_key: &amp;str」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「run.record.submission_digest = Some(submission_digest)」，捕获目标为「run.record.submission_digest」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「last_tokens」的初始化来源为「terminal\n                    .token_usage\n                    .as_ref()\n                    .map_or(0, |usage| usage.last_token_usage.total_tokens.max(0))」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「goal != expected_goal」的捕获提前退出分支为「Err_return：Err(conflict())」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(conflict())」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「2e6ac8d65d9e5debae595132」先于语句位置「1」的操作「9899d4a08f91adcc6c878c0d」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「thread_id」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-codex/src/adapter#ProductionCodexAdapter.session_for_thread」，对应捕获形参「thread_id: &amp;CodexThreadId」。该普通调用关系不替代进程或网络协议关系。

源码：`crates/winwincode-codex/src/adapter.rs:3511`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/302`。

### `crates/winwincode-codex/src/adapter.rs::&lt;closure_expression@3524:59&gt;`

以无显式实参的调用形式「invalid_job」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-codex/src/adapter.rs:3524`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/303`。

### `crates/winwincode-codex/src/adapter.rs::&lt;closure_expression@3594:32&gt;`

在调用形式「usage.last_token_usage.total_tokens.max」中提供第 1 个实参「0」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-codex/src/adapter.rs:3594`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/304`。

### `crates/winwincode-codex/src/adapter.rs::session_identity`

构造捕获记录，字段按源码次序为「codex_thread_id ← thread_id；product_session_id ← product_session_id；work_run_id ← work_run_id；worker_session_id ← start.worker_session_id.clone()」。不据构造形式推断物理持久化。 在调用形式「Some」中提供第 1 个实参「scope.work_run_id.clone()」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以字段投影形式「thread_id」关联路径「thread_id」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「d863c8fb6715a39b38049f00」先于语句位置「1」的操作「c71314f732b70ffd32da9b94」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-codex/src/adapter.rs:5236`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/305`。

### `crates/winwincode-codex/src/adapter.rs::production_agent_session_config`

构造捕获记录，字段按源码次序为「provider ← job.model_selection.as_ref().map_or_else(\n                || config.provider.clone(),\n                |selection| selection.provider_id.clone(),\n            …［展示截断；完整操作保留］；model ← job.model_selection.as_ref().map_or_else(\n                || config.model.clone(),\n                |selection| selection.model_id.clone(),\n            )；reasoning ← "provider_default".to_owned()；tools ← tools；sandbox ← sandbox.to_owned()；instructions ← role_policy.map(|policy| policy.developer_instructions.clone())」。不据构造形式推断物理持久化。 将「worker_id」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-execution-port/src/agent_config#resolve_agent_session_config」，对应捕获形参「worker_id: &amp;WorkerId」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「tools」的初始化来源为「config\n        .registered_capabilities\n        .features\n        .iter()\n        .map(|feature| {\n            serde_json::to_value(feature)\n                .ok()\n                .and_then(|value| value.as_str().map(|name| format!("worker:{name}")))\n                .ok_or_else(invalid_job)\n        })\n        .collect::&lt;Result&lt;Vec&lt;_&gt;, _&gt;&gt;()?」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以字段投影形式「tools」关联路径「tools」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「46036011c82e8eab34a1795c」先于语句位置「1」的操作「793ae1c4225c29b94afabbc4」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-codex/src/adapter.rs:5269`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/306`。

### `crates/winwincode-codex/src/adapter.rs::&lt;closure_expression@5279:14&gt;`

在调用形式「serde_json::to_value」中提供第 1 个实参「feature」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-codex/src/adapter.rs:5279`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/307`。

### `crates/winwincode-codex/src/adapter.rs::&lt;closure_expression@5282:27&gt;`

在调用形式「value.as_str().map」中提供第 1 个实参「|name| format!("worker:{name}")」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-codex/src/adapter.rs:5282`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/308`。

### `crates/winwincode-codex/src/adapter.rs::&lt;closure_expression@5290:18&gt;`

以无显式实参的调用形式「capability.id().to_owned」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-codex/src/adapter.rs:5290`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/309`。

### `crates/winwincode-codex/src/adapter.rs::&lt;closure_expression@5309:17&gt;`

以无显式实参的调用形式「config.provider.clone」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-codex/src/adapter.rs:5309`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/310`。

### `crates/winwincode-codex/src/adapter.rs::&lt;closure_expression@5310:17&gt;`

以无显式实参的调用形式「selection.provider_id.clone」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-codex/src/adapter.rs:5310`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/311`。

### `crates/winwincode-codex/src/adapter.rs::&lt;closure_expression@5313:17&gt;`

以无显式实参的调用形式「config.model.clone」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-codex/src/adapter.rs:5313`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/312`。

### `crates/winwincode-codex/src/adapter.rs::&lt;closure_expression@5314:17&gt;`

以无显式实参的调用形式「selection.model_id.clone」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-codex/src/adapter.rs:5314`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/313`。

### `crates/winwincode-codex/src/adapter.rs::&lt;closure_expression@5319:43&gt;`

以无显式实参的调用形式「policy.developer_instructions.clone」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-codex/src/adapter.rs:5319`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/314`。

### `crates/winwincode-codex/src/adapter.rs::&lt;closure_expression@5322:14&gt;`

以无显式实参的调用形式「invalid_job」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-codex/src/adapter.rs:5322`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/315`。

### `crates/winwincode-codex/src/contract.rs::CodexRunKey.from_dispatch`

构造捕获记录，字段按源码次序为「job_id ← dispatch.job.job_id.clone()；attempt ← dispatch.job.attempt；fencing_token ← dispatch.lease.fencing_token.clone()；payload_digest ← dispatch.job.payload_digest.clone()」。不据构造形式推断物理持久化。 以无显式实参的调用形式「dispatch.job.job_id.clone」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。 以字段投影形式「dispatch.job.job_id.clone()」关联路径「dispatch.job.job_id」；只描述捕获来源，不证明当时的字段值。

源码：`crates/winwincode-codex/src/contract.rs:46`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/316`。

### `crates/winwincode-codex/src/outbox.rs::ExecutionOutbox.retain_in_transaction`

构造捕获记录，字段按源码次序为「delivery_id ← metadata.delivery_id；message ← message.clone()」。不据构造形式推断物理持久化。 在调用形式「Ok」中提供第 1 个实参「DurableExecutionDelivery {\n            delivery_id: metadata.delivery_id,\n            message: message.clone(),\n        }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「same_original」的初始化来源为「existing_digest == frame_digest &amp;&amp; existing_frame == frame」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「!same_original &amp;&amp; !same_terminal_facts &amp;&amp; !same_replay_facts」的捕获提前退出分支为「Err_return：Err(AdapterStoreError::Conflict)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(AdapterStoreError::Conflict)」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「metadata.delivery_id」关联路径「metadata.delivery_id」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「b7fce16c9193b4e1f388f8fd」先于语句位置「1」的操作「f256a28657f7b34f0102b24e」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-codex/src/outbox.rs:62`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/317`。

### `crates/winwincode-codex/src/outbox.rs::&lt;closure_expression@79:17&gt;`

在调用形式「Ok」中提供第 1 个实参「(\n                        row.get::&lt;_, String&gt;(0)?,\n                        row.get::&lt;_, String&gt;(1)?,\n                        row.get::&lt;_, Vec&lt;u8&gt;&gt;(2)?,\n                    )」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-codex/src/outbox.rs:79`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/318`。

### `crates/winwincode-codex/src/outbox.rs::ExecutionOutbox.acknowledge_response`

在调用形式「accepted_response」中提供第 1 个实参「acknowledgement」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「pending_same_family」的初始化来源为「connection\n                .query_row(\n                    "SELECT 1 FROM execution_outbox\n                     WHERE family = ?1 AND acknowledgement_required = 1 LIMIT 1",\n                    params![family.as_str()],\n                    |_| Ok(()),\n                )\n                .optional()\n                .map_err(|_| AdapterStoreError::Unavail…［展示截断；完整操作保留］」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「let ExecutionPortMessage::RuntimeAckMessage(_) = acknowledgement」的捕获提前退出分支为「Err_return：Err(AdapterStoreError::Conflict)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(AdapterStoreError::Conflict)」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「1」的操作「68f1c9e1c7b890711d3dc3cb」先于语句位置「2」的操作「d11b34ee1849c1d3a904c52a」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-codex/src/outbox.rs:262`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/319`。

### `crates/winwincode-codex/src/outbox.rs::&lt;closure_expression@312:21&gt;`

在调用形式「Ok」中提供第 1 个实参「()」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-codex/src/outbox.rs:312`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/320`。

### `crates/winwincode-codex/src/outbox.rs::metadata`

构造捕获记录，字段按源码次序为「delivery_id ← delivery_id；family ← family.as_str()；correlation_key ← key；acknowledgement_required ← !matches!(family, Family::Transport | Family::SessionBinding)」。不据构造形式推断物理持久化。 在调用形式「Ok」中提供第 1 个实参「Metadata {\n        delivery_id,\n        family: family.as_str(),\n        correlation_key: key,\n        acknowledgement_required: !matches!(family, Family::Transport | Family::SessionBinding),\n    }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「delivery_id」的初始化来源为「message_id(frame)?」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以字段投影形式「delivery_id」关联路径「delivery_id」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「9534023ae8364221521bd6d0」先于语句位置「1」的操作「0a3e1f3dea076fbc330cfb81」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-codex/src/outbox.rs:454`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/321`。

### `crates/winwincode-codex/src/outbox.rs::response_target`

将「&amp;(\n                &amp;message.lease,\n                &amp;message.worker_session_id,\n                &amp;message.session_identity,\n            )」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-codex/src/outbox#correlation」，对应捕获形参「value: &amp;impl Serialize」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「target」的初始化来源为「match message {\n        ExecutionPortMessage::JobOutcomeAckMessage(message) =&gt; Some((\n            Family::Outcome,\n            correlation(&amp;(\n                &amp;message.lease,\n                &amp;message.worker_session_id,\n                &amp;message.session_identity,\n            ))?,\n        )),\n        ExecutionPortMessage::ModelChunkMessage(message) =&gt; S…［展示截断；完整操作保留］」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留同一块中的正常源码顺序：语句位置「0」的操作「bfee1fdea7d46b135c03dbbf」先于语句位置「1」的操作「2b7a826db5bff4363a616d45」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-codex/src/outbox.rs:586`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/322`。

### `crates/winwincode-codex/src/outbox.rs::correlation`

将「&amp;bytes」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-codex/src/outbox#digest」，对应捕获形参「bytes: &amp;[u8]」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「bytes」的初始化来源为「serde_json::to_vec(value).map_err(|_| AdapterStoreError::Corrupt)?」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留同一块中的正常源码顺序：语句位置「0」的操作「93614428fa56683e5a91d878」先于语句位置「1」的操作「e6f527ea256197760df526ce」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-codex/src/outbox.rs:737`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/323`。

### `crates/winwincode-control-plane/src/delivery_application.rs::ControlPlane.delivery_update_spec`

将「&amp;command.actor」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-control-plane/src/delivery_application#map_command」，对应捕获形参「actor: &amp;Actor」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「mapped」的初始化来源为「map_command(\n            &amp;command.actor,\n            CommandName::DeliveryUpdateSpec,\n            command.expected_revision.clone(),\n            &amp;command.payload,\n            &amp;command.request_id,\n            &amp;command.schema_version,\n            &amp;command.scope,\n        )?」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「let Some((receipt, delivery)) =\n            self.delivery_replay(&amp;mapped, &amp;command.scope, &amp;command.payload.delivery_id)?」的捕获提前退出分支为「return：update_response(command, &amp;receipt, &amp;delivery)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return update_response(command, &amp;receipt, &amp;delivery)」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「949cb6cf139e78e9892bcdfc」先于语句位置「1」的操作「fe6d5cb25038ec2b155174a7」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「&amp;mapped」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-control-plane/src/delivery_application#ControlPlane.resolve_specification_authority」，对应捕获形参「command: &amp;CommandEnvelope」。该普通调用关系不替代进程或网络协议关系。

源码：`crates/winwincode-control-plane/src/delivery_application.rs:582`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/324`。

### `crates/winwincode-control-plane/src/delivery_application.rs::ControlPlane.resolve_specification_authority`

构造捕获记录，字段按源码次序为「command ← command；delivery ← delivery」。不据构造形式推断物理持久化。 以无显式实参的调用形式「self.take_delivery_authority」调用已绑定接口「rust:crates/winwincode-control-plane/src/delivery_application#ControlPlane.take_delivery_authority」；没有据调用存在断言激活、存储或网络效果。 包含赋值/更新「self.delivery_authority = Some(port)」，捕获目标为「self.delivery_authority」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「port」的初始化来源为「self.take_delivery_authority()?」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以字段投影形式「command」关联路径「command」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「66d3bf8682c6c57a7f6598ec」先于语句位置「1」的操作「06f042970001dc6365131044」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-control-plane/src/delivery_application.rs:1175`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/325`。

### `crates/winwincode-control-plane/src/delivery_application.rs::ControlPlane.take_delivery_authority`

在调用形式「self.delivery_authority.take().ok_or_else」中提供第 1 个实参「|| {\n            DeliveryApplicationError::TrustedFactsUnavailable(\n                "Delivery authority port is not installed".to_owned(),\n            )\n        }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`crates/winwincode-control-plane/src/delivery_application.rs:1228`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/326`。

### `crates/winwincode-control-plane/src/delivery_application.rs::&lt;closure_expression@1231:51&gt;`

在调用形式「DeliveryApplicationError::TrustedFactsUnavailable」中提供第 1 个实参「"Delivery authority port is not installed".to_owned()」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-control-plane/src/delivery_application.rs:1231`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/327`。

### `crates/winwincode-control-plane/src/delivery_application.rs::map_command`

构造捕获记录，字段按源码次序为「actor ← actor.clone()；command ← command；expected_revision ← expected_revision；payload ← serde_json::to_value(payload).map_err(|error| {\n            DeliveryApplicationError::InvalidRequest(format!(\n                "Delivery command payload cannot…［展示截断；完整操作保留］；request_id ← request_id.clone()；schema_version ← schema_version.clone()；scope ← Scope::RepositoryScope(scope.clone())」。不据构造形式推断物理持久化。 将「&amp;mapped」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-control-plane/src/lib#command_receipt」，对应捕获形参「command: &amp;CommandEnvelope」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「mapped」的初始化来源为「CommandEnvelope {\n        actor: actor.clone(),\n        command,\n        expected_revision,\n        payload: serde_json::to_value(payload).map_err(|error| {\n            DeliveryApplicationError::InvalidRequest(format!(\n                "Delivery command payload cannot be encoded: {error}"\n            ))\n        })?,\n        request_id: request_id.clo…［展示截断；完整操作保留］」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「schema_version != &amp;SchemaVersion::WinwincodeV1」的捕获提前退出分支为「Err_return：Err(DeliveryApplicationError::InvalidRequest(\n            "Delivery command schemaVersion is invalid".to_owned(),\n        ))」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(DeliveryApplicationError::InvalidRequest(\n            "Delivery command schemaVersion is invalid".to_owned(),\n        ))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「actor.clone()」关联路径「actor」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「1」的操作「57eabd0d3026e18458f4690d」先于语句位置「2」的操作「4c1062865795a04d7cd885c2」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-control-plane/src/delivery_application.rs:1358`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/328`。

### `crates/winwincode-control-plane/src/delivery_application.rs::&lt;closure_expression@1376:56&gt;`

在调用形式「DeliveryApplicationError::InvalidRequest」中提供第 1 个实参「format!(\n                "Delivery command payload cannot be encoded: {error}"\n            )」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-control-plane/src/delivery_application.rs:1376`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/329`。

### `crates/winwincode-control-plane/src/delivery_production_adapters.rs::LocalDeliveryAuthority.device_target`

构造捕获记录，字段按源码次序为「client_node_id ← grant.client_node_id；client_id ← node.public_client_id；repository_binding_id ← grant.repository_binding_id；user_id ← grant.holder_user_id」。不据构造形式推断物理持久化。 将「&amp;crate::device_session_gate::DeviceSessionGateInput {\n                user_id: &amp;grant.holder_user_id,\n                client_node_id: &amp;grant.client_node_id,\n                repository_binding_id: &amp;grant.repository_binding_id,\n            }」作为第 2 个实参交给已绑定接口「rust:crates/winwincode-control-plane/src/device_session_gate#authorize_device_session」，对应捕获形参「input: &amp;DeviceSessionGateInput&lt;'_&gt;」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「failure」的初始化来源为「|error: &amp;dyn fmt::Display| DeliveryAuthorityError::new(error.to_string())」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return Ok(None)」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「&amp;grant.holder_user_id」关联路径「grant.holder_user_id」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「1」的操作「594c5e2402759e01f401bac1」先于语句位置「2」的操作「baf4360b9174fbb9f35e5c0e」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-control-plane/src/delivery_production_adapters.rs:252`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/330`。

### `crates/winwincode-control-plane/src/delivery_production_adapters.rs::&lt;closure_expression@259:23&gt;`

在调用形式「DeliveryAuthorityError::new」中提供第 1 个实参「error.to_string()」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-control-plane/src/delivery_production_adapters.rs:259`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/331`。

### `crates/winwincode-control-plane/src/delivery_production_adapters.rs::&lt;closure_expression@262:22&gt;`

在调用形式「failure」中提供第 1 个实参「&amp;e」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-control-plane/src/delivery_production_adapters.rs:262`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/332`。

### `crates/winwincode-control-plane/src/delivery_production_adapters.rs::&lt;closure_expression@274:18&gt;`

在调用形式「failure」中提供第 1 个实参「&amp;e」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-control-plane/src/delivery_production_adapters.rs:274`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/333`。

### `crates/winwincode-control-plane/src/delivery_production_adapters.rs::&lt;closure_expression@278:22&gt;`

在调用形式「failure」中提供第 1 个实参「&amp;e」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-control-plane/src/delivery_production_adapters.rs:278`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/334`。

### `crates/winwincode-control-plane/src/delivery_production_adapters.rs::&lt;closure_expression@280:22&gt;`

在调用形式「failure」中提供第 1 个实参「&amp;e」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-control-plane/src/delivery_production_adapters.rs:280`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/335`。

### `crates/winwincode-control-plane/src/delivery_production_adapters.rs::&lt;closure_expression@281:25&gt;`

在调用形式「DeliveryAuthorityError::new」中提供第 1 个实参「"Device repository is unavailable"」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-control-plane/src/delivery_production_adapters.rs:281`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/336`。

### `crates/winwincode-control-plane/src/delivery_production_adapters.rs::&lt;closure_expression@284:22&gt;`

在调用形式「failure」中提供第 1 个实参「&amp;e」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-control-plane/src/delivery_production_adapters.rs:284`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/337`。

### `crates/winwincode-control-plane/src/delivery_production_adapters.rs::&lt;closure_expression@285:25&gt;`

在调用形式「DeliveryAuthorityError::new」中提供第 1 个实参「"Device is unavailable"」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-control-plane/src/delivery_production_adapters.rs:285`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/338`。

### `crates/winwincode-control-plane/src/delivery_production_adapters.rs::&lt;closure_expression@287:80&gt;`

在调用形式「failure」中提供第 1 个实参「&amp;e」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-control-plane/src/delivery_production_adapters.rs:287`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/339`。

### `crates/winwincode-control-plane/src/delivery_production_adapters.rs::&lt;closure_expression@293:18&gt;`

在调用形式「failure」中提供第 1 个实参「&amp;e」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-control-plane/src/delivery_production_adapters.rs:293`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/340`。

### `crates/winwincode-control-plane/src/delivery_production_adapters.rs::&lt;closure_expression@302:50&gt;`

在调用形式「DeliveryAuthorityError::new」中提供第 1 个实参「"Device repository has no verified HEAD"」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-control-plane/src/delivery_production_adapters.rs:302`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/341`。

### `crates/winwincode-control-plane/src/delivery_production_adapters.rs::&lt;LocalDeliveryAuthority as DeliveryAuthorityPort&gt;.specification`

构造捕获记录，字段按源码次序为「now_millis ← Self::now_millis(request.delivery())?；repository ← repository；source_ref ← request\n                .delivery()\n                .and_then(|delivery| delivery.snapshot().spec.source_ref.clone())；max_rework_attempts ← self.config.max_rework_attempts；criterion_verification_methods ← spec\n                .acceptance_criteria\n                .into_iter()\n                .map(|criterion| (criterion.id, verification.clone()))\n              …［展示截断；完整操作保留］」。不据构造形式推断物理持久化。 将「request.command()」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-control-plane/src/delivery_production_adapters#decode_payload」，对应捕获形参「command: &amp;winwincode_api::generated::CommandEnvelope」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「payload」的初始化来源为「decode_payload(request.command())?」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「_」的捕获提前退出分支为「Err_return：Err(DeliveryAuthorityError::new(\n                    "specification authority received another command",\n                ))」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(DeliveryAuthorityError::new(\n                    "specification authority received another command",\n                ))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「repository」关联路径「repository」；只描述捕获来源，不证明当时的字段值。 记录消息形状中的固定文本字段「kind」及捕获形式「RepositoryKind::LocalGit」。单个文本字段不是跨语言调用或传输成功的证明。 将「spec.source_product_session_id.as_ref()」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-control-plane/src/delivery_production_adapters#LocalDeliveryAuthority.device_target」，对应捕获形参「source: Option&lt;&amp;ProductSessionId&gt;」。该普通调用关系不替代进程或网络协议关系。

源码：`crates/winwincode-control-plane/src/delivery_production_adapters.rs:584`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/342`。

### `crates/winwincode-control-plane/src/delivery_production_adapters.rs::&lt;closure_expression@618:25&gt;`

以无显式实参的调用形式「command.trim」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-control-plane/src/delivery_production_adapters.rs:618`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/343`。

### `crates/winwincode-control-plane/src/delivery_production_adapters.rs::&lt;closure_expression@619:29&gt;`

在调用形式「DeliveryAuthorityError::new」中提供第 1 个实参「"Device delivery requires a confirmed verification command"」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-control-plane/src/delivery_production_adapters.rs:619`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/344`。

### `crates/winwincode-control-plane/src/delivery_production_adapters.rs::&lt;closure_expression@649:27&gt;`

以无显式实参的调用形式「delivery.snapshot().spec.source_ref.clone」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-control-plane/src/delivery_production_adapters.rs:649`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/345`。

### `crates/winwincode-control-plane/src/delivery_production_adapters.rs::&lt;closure_expression@654:22&gt;`

以无显式实参的调用形式「verification.clone」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-control-plane/src/delivery_production_adapters.rs:654`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/346`。

### `crates/winwincode-control-plane/src/delivery_production_adapters.rs::ControlPlane.install_local_delivery_adapters`

将「crate::strongflow_projection::production_sources()」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-control-plane/src/lib#ControlPlane.install_strongflow_projection_sources」，对应捕获形参「sources: strongflow_projection::StrongFlowProjectionSources」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「self.delivery_authority = Some(Box::new(authority))」，捕获目标为「self.delivery_authority」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「repository_scope」的初始化来源为「config.repository_scope.clone()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「self.delivery_authority.is_some()\n            || self.delivery_dispatcher.is_some()\n            || self.strongflow_sources.is_some()\n            || self.git_source_resolver.is_some()\n            || self.git_repository_root.is_some()」的捕获提前退出分支为「Err_return：Err(LocalDeliveryAdapterError::new(\n                "Delivery production adapters are already installed",\n            ))」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(LocalDeliveryAdapterError::new(\n                "Delivery production adapters are already installed",\n            ))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「1a9992035171b57663b970e8」先于语句位置「1」的操作「d268b7546b7ad6a73b1fcb74」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-control-plane/src/delivery_production_adapters.rs:1058`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/347`。

### `crates/winwincode-control-plane/src/delivery_production_adapters.rs::&lt;closure_expression@1076:25&gt;`

在调用形式「LocalDeliveryAdapterError::new」中提供第 1 个实参「"Delivery production adapters require local Control Plane storage"」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-control-plane/src/delivery_production_adapters.rs:1076`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/348`。

### `crates/winwincode-control-plane/src/delivery_production_adapters.rs::&lt;closure_expression@1090:22&gt;`

在调用形式「LocalDeliveryAdapterError::new」中提供第 1 个实参「format!(\n                    "failed to open the local Git candidate resolver: {error}"\n                )」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-control-plane/src/delivery_production_adapters.rs:1090`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/349`。

### `crates/winwincode-control-plane/src/delivery_production_adapters.rs::&lt;closure_expression@1098:18&gt;`

在调用形式「LocalDeliveryAdapterError::new」中提供第 1 个实参「format!(\n                "failed to install StrongFlow projection sources: {error}"\n            )」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-control-plane/src/delivery_production_adapters.rs:1098`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/350`。

### `crates/winwincode-control-plane/src/delivery_production_adapters.rs::decode_payload`

在调用形式「serde_json::from_value」中提供第 1 个实参「command.payload.clone()」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「payload」的初始化来源为「serde_json::from_value(command.payload.clone())\n        .map_err(|error| DeliveryAuthorityError::new(format!("payload is invalid: {error}")))?」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「serde_json::to_value(&amp;payload)\n        .map_err(|error| DeliveryAuthorityError::new(error.to_string()))?\n        != command.payload」的捕获提前退出分支为「Err_return：Err(DeliveryAuthorityError::new("payload is not canonical"))」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(DeliveryAuthorityError::new("payload is not canonical"))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「ae208b53d72ab851460440ee」先于语句位置「1」的操作「ef2dc8d151f7d3cc761ad4b3」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-control-plane/src/delivery_production_adapters.rs:1228`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/351`。

### `crates/winwincode-control-plane/src/delivery_production_adapters.rs::&lt;closure_expression@1232:18&gt;`

在调用形式「DeliveryAuthorityError::new」中提供第 1 个实参「format!("payload is invalid: {error}")」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-control-plane/src/delivery_production_adapters.rs:1232`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/352`。

### `crates/winwincode-control-plane/src/delivery_production_adapters.rs::&lt;closure_expression@1234:18&gt;`

在调用形式「DeliveryAuthorityError::new」中提供第 1 个实参「error.to_string()」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-control-plane/src/delivery_production_adapters.rs:1234`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/353`。

### `crates/winwincode-delivery/src/application/workrun.rs::WorkRunAggregate.validate`

将「&amp;item.id.0」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-domain/src/lib#is_canonical_prefixed_id」，对应捕获形参「value: &amp;str」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「item」的初始化来源为「self\n                .items\n                .iter()\n                .find(|item| item.id == run.work_item_id)\n                .ok_or(WorkRunSchedulingError::InvalidAggregate)?」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「!valid_revision(self.contract.revision.0)\n            || !is_canonical_prefixed_id(&amp;self.contract.id.0, "wct_")\n            || !bounded_text(&amp;self.contract.objective, 1, 65_536)\n            || !valid_created_at(&amp;self.contract.created_at.0)\n            || !valid_text_list(&amp;self.contract.scope, true)\n            || !valid_text_list(&amp;self.contract.protecte…［展示截断；完整操作保留］」的捕获提前退出分支为「Err_return：Err(invalid)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(invalid)」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「1a70c55f01ffaf403a5309ca」先于语句位置「1」的操作「23c5b522c19cfac72100d59a」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-delivery/src/application/workrun.rs:206`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/354`。

### `crates/winwincode-delivery/src/application/workrun.rs::&lt;closure_expression@219:50&gt;`

在调用形式「is_canonical_prefixed_id」中提供第 1 个实参「&amp;criterion.id.0」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/application/workrun.rs:219`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/355`。

### `crates/winwincode-delivery/src/application/workrun.rs::&lt;closure_expression@226:38&gt;`

在调用形式「bounded_text」中提供第 1 个实参「value」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/application/workrun.rs:226`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/356`。

### `crates/winwincode-delivery/src/application/workrun.rs::&lt;closure_expression@258:26&gt;`

在调用形式「criterion_ids.contains」中提供第 1 个实参「id」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/application/workrun.rs:258`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/357`。

### `crates/winwincode-delivery/src/application/workrun.rs::&lt;closure_expression@263:26&gt;`

在调用形式「item_ids.contains」中提供第 1 个实参「id」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/application/workrun.rs:263`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/358`。

### `crates/winwincode-delivery/src/application/workrun.rs::WorkRunAggregate.start_next`

构造捕获记录，字段按源码次序为「expected_contract_revision ← self.contract.revision.clone()；active_work_item_ids ← active」。不据构造形式推断物理持久化。 将「&amp;WorkRunAdvanceInput {\n                expected_contract_revision: self.contract.revision.clone(),\n                active_work_item_ids: active,\n            }」作为第 2 个实参交给已绑定接口「rust:crates/winwincode-delivery/src/application/workrun#start_next_work_run」，对应捕获形参「input: &amp;WorkRunAdvanceInput」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「active」的初始化来源为「self\n            .runs\n            .iter()\n            .filter(|run| {\n                matches!(\n                    run.state,\n                    WorkRunState::Leased | WorkRunState::Running | WorkRunState::CandidateReady\n                )\n            })\n            .map(|run| run.work_item_id.clone())\n            .collect()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以字段投影形式「self.contract.revision.clone()」关联路径「self.contract.revision」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「25eee473cbe1a96754a6dd0c」先于语句位置「1」的操作「b9ae47238986f27fb8e4b123」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「&amp;start.work_item.id」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.start_item」，对应捕获形参「id: &amp;WorkItemId」。该普通调用关系不替代进程或网络协议关系。 以无显式实参的调用形式「self.validate」调用已绑定接口「rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate」；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-delivery/src/application/workrun.rs:391`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/359`。

### `crates/winwincode-delivery/src/application/workrun.rs::&lt;closure_expression@402:18&gt;`

以无显式实参的调用形式「run.work_item_id.clone」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-delivery/src/application/workrun.rs:402`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/360`。

### `crates/winwincode-delivery/src/application/workrun.rs::WorkRunAggregate.start_item`

构造捕获记录，字段按源码次序为「work_item ← work_item；attempt ← attempt」。不据构造形式推断物理持久化。 以无显式实参的调用形式「self.validate」调用已绑定接口「rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate」；没有据调用存在断言激活、存储或网络效果。 包含赋值/更新「work_item.state = WorkItemState::InProgress」，捕获目标为「work_item.state」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「work_item」的初始化来源为「item.clone()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以字段投影形式「work_item」关联路径「work_item」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「5e173ad01344b1922627a8b9」先于语句位置「1」的操作「6ad950fffd5bb1e91d512a0f」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-delivery/src/application/workrun.rs:418`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/361`。

### `crates/winwincode-delivery/src/application/workrun.rs::&lt;closure_expression@423:19&gt;`

在调用形式「work_item_is_runnable」中提供第 1 个实参「item」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/application/workrun.rs:423`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/362`。

### `crates/winwincode-delivery/src/application/workrun.rs::work_item_is_runnable`

将「item」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-delivery/src/application/workrun#effective_work_item_state」，对应捕获形参「item: &amp;WorkItem」。该普通调用关系不替代进程或网络协议关系。

源码：`crates/winwincode-delivery/src/application/workrun.rs:640`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/363`。

### `crates/winwincode-delivery/src/application/workrun.rs::effective_work_item_state`

在调用形式「item.depends_on.iter().any」中提供第 1 个实参「|dependency| {\n        !items\n            .iter()\n            .any(|candidate| candidate.id == *dependency &amp;&amp; candidate.state == WorkItemState::Done)\n    }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/application/workrun.rs:644`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/364`。

### `crates/winwincode-delivery/src/application/workrun.rs::&lt;closure_expression@648:37&gt;`

在调用形式「items\n            .iter()\n            .any」中提供第 1 个实参「|candidate| candidate.id == *dependency &amp;&amp; candidate.state == WorkItemState::Done」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/application/workrun.rs:648`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/365`。

### `crates/winwincode-delivery/src/application/workrun.rs::start_next_work_run`

构造捕获记录，字段按源码次序为「work_item ← started；attempt ← attempt」。不据构造形式推断物理持久化。 在调用形式「Ok」中提供第 1 个实参「WorkRunStart {\n        work_item: started,\n        attempt,\n    }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 包含赋值/更新「started.state = WorkItemState::InProgress」，捕获目标为「started.state」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「started」的初始化来源为「item.clone()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以字段投影形式「started」关联路径「started」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「300c662e303f26b591df56b0」先于语句位置「1」的操作「5e1ff437c1adbe0dc6aa4f9c」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-delivery/src/application/workrun.rs:707`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/366`。

### `crates/winwincode-delivery/src/application/workrun.rs::&lt;closure_expression@713:15&gt;`

在调用形式「work_item_is_runnable」中提供第 1 个实参「item」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/application/workrun.rs:713`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/367`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::resolve_production_verdict`

构造捕获记录，字段按源码次序为「work_run_id ← candidate.producer_work_run_id().clone()；session_binding_id ← candidate.producer_session_binding_id().clone()；source ← EvidenceSource::CandidateCommit；created_at_millis ← produced_at_millis」。不据构造形式推断物理持久化。 将「ResolveDeliveryEvidenceInput {\n            work_run_id: candidate.producer_work_run_id().clone(),\n            session_binding_id: candidate.producer_session_binding_id().clone(),\n            source: EvidenceSource::CandidateCommit,\n            created_at_millis: produced_at_millis,\n        }」作为第 3 个实参交给已绑定接口「rust:crates/winwincode-delivery/src/domain/evidence#resolve_delivery_evidence」，对应捕获形参「input: ResolveDeliveryEvidenceInput&lt;'_&gt;」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「resolved」的初始化来源为「resolve_verification_runtime(delivery, &amp;candidate, &amp;runtime)?」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「produced_at_millis」存在源更新「produced_at_millis = produced_at_millis.max(resolved.finished_at_millis)」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「!roles.insert(resolved.role)」的捕获提前退出分支为「Err_return：Err(error("durable verification repeats one current role"))」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(error("durable verification repeats one current role"))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「required_roles」关联路径「required_roles」；只描述捕获来源，不证明当时的字段值。 将「delivery」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-delivery/src/domain/candidate/verdict_authority#resolve_verification_runtime」，对应捕获形参「delivery: &amp;Delivery」。该普通调用关系不替代进程或网络协议关系。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:206`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/368`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@212:18&gt;`

在调用形式「resolution_error」中提供第 1 个实参「&amp;error_value」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:212`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/369`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@229:38&gt;`

在调用形式「roles.contains」中提供第 1 个实参「role」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:229`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/370`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@235:26&gt;`

在调用形式「role_order」中提供第 1 个实参「session.role」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:235`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/371`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@236:22&gt;`

在调用形式「left.evidence().id.0.cmp」中提供第 1 个实参「&amp;right.evidence().id.0」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:236`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/372`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@237:23&gt;`

以无显式实参的调用形式「left.evidence」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:237`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/373`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@246:14&gt;`

在调用形式「resolution_error」中提供第 1 个实参「&amp;error_value」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:246`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/374`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@249:21&gt;`

在调用形式「error」中提供第 1 个实参「"verdict production time exceeds the durable range"」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:249`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/375`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@265:14&gt;`

在调用形式「error」中提供第 1 个实参「error_value.to_string()」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:265`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/376`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@267:22&gt;`

在调用形式「left.evidence().id.0.cmp」中提供第 1 个实参「&amp;right.evidence().id.0」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:267`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/377`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@268:23&gt;`

以无显式实参的调用形式「left.evidence」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:268`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/378`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::resolve_verification_runtime`

构造捕获记录，字段按源码次序为「role ← role；work_run_id ← binding.work_run_id.clone()；session_binding_id ← binding.id.clone()；workspace_mode ← VerificationWorkspaceMode::CandidateReadOnly；permission_profile ← VerificationPermissionProfile::CandidateReadOnlyRestricted；pre_candidate_snapshot ← Some(snapshot.clone())；post_candidate_snapshot ← Some(snapshot)；accepted_job_outcome ← Some(terminal)；codex_turn_completed ← true；mutation_records ← Vec::new()；findings ← findings」。不据构造形式推断物理持久化。 将「&amp;terminal」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-delivery/src/domain/evidence#checkout_attestation_from_snapshot」，对应捕获形参「terminal: &amp;AcceptedVerificationJobOutcomeFact」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「role」的初始化来源为「runtime.role」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以字段投影形式「role」关联路径「role」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「dfa44ce2a6e4755d415f7942」先于语句位置「1」的操作「093402ce65a984bcd1ee64e5」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「delivery」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-delivery/src/domain/candidate/verdict_authority#resolve_findings」，对应捕获形参「delivery: &amp;Delivery」。该普通调用关系不替代进程或网络协议关系。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:285`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/379`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@295:14&gt;`

在调用形式「resolution_error」中提供第 1 个实参「&amp;error_value」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:295`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/380`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@301:15&gt;`

以无显式实参的调用形式「verified_terminal.execution_job_id」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:301`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/381`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@306:21&gt;`

在调用形式「error」中提供第 1 个实参「"verification terminal SessionBinding is missing"」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:306`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/382`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@320:14&gt;`

在调用形式「resolution_error」中提供第 1 个实参「&amp;error_value」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:320`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/383`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::resolve_findings`

构造捕获记录，字段按源码次序为「finding_ref ← finding.finding_id；criterion_id ← AcceptanceCriterionId::new(criterion_id)\n                .map_err(|error_value| resolution_error(&amp;error_value))?；conclusion ← conclusion；result_sequence ← ExecutionSequence(\n                i64::try_from(result.event.sequence)\n                    .map_err(|_| error("verification result sequence exceeds the durab…［展示截断；完整操作保留］；source_refs ← source_refs；source_sequences ← source_sequences；explanation ← finding.explanation」。不据构造形式推断物理持久化。 将「"verification result repeats one criterion"」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-delivery/src/domain/candidate/verdict_authority#error」，对应捕获形参「message: impl Into&lt;String&gt;」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「criterion_id」的初始化来源为「finding\n            .criterion_id\n            .ok_or_else(|| error("verification finding has no current criterion"))?」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「!criterion_ids.insert(criterion_id.clone())」的捕获提前退出分支为「Err_return：Err(error("verification result repeats one criterion"))」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(error("verification result repeats one criterion"))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「session_binding_id.clone()」关联路径「session_binding_id」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「a32d06a6ec25965b6c2d9e33」先于语句位置「1」的操作「bf9756e47f65e35c771d9355」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:559`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/384`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@577:25&gt;`

在调用形式「error」中提供第 1 个实参「"verification finding has no current criterion"」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:577`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/385`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@621:33&gt;`

在调用形式「error」中提供第 1 个实参「"Evidence time exceeds the durable range"」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:621`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/386`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@638:26&gt;`

在调用形式「error」中提供第 1 个实参「error_value.to_string()」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:638`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/387`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@644:30&gt;`

在调用形式「error」中提供第 1 个实参「"Evidence source sequence exceeds the durable range"」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:644`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/388`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@650:26&gt;`

在调用形式「resolution_error」中提供第 1 个实参「&amp;error_value」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:650`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/389`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@654:30&gt;`

在调用形式「error」中提供第 1 个实参「"verification result sequence exceeds the durable range"」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:654`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/390`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::exact_source_event`

将「"verification finding Evidence source identity is ambiguous"」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-delivery/src/domain/candidate/verdict_authority#error」，对应捕获形参「message: impl Into&lt;String&gt;」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「matching」的初始化来源为「events\n        .iter()\n        .filter(|event| event.event.event_id == *event_id)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「matching.next().is_some()」的捕获提前退出分支为「Err_return：Err(error(\n            "verification finding Evidence source identity is ambiguous",\n        ))」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(error(\n            "verification finding Evidence source identity is ambiguous",\n        ))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「b2e132b4493c13e916d6d685」先于语句位置「1」的操作「3c8dd7a516668af3ccd77ae0」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:664`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/391`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@673:21&gt;`

在调用形式「error」中提供第 1 个实参「"verification finding Evidence source is missing"」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:673`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/392`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::required_roles`

在调用形式「Ok」中提供第 1 个实参「roles」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「roles」的初始化来源为「[\n        VerificationRole::Reviewer,\n        VerificationRole::Verifier,\n        VerificationRole::AdversarialVerifier,\n    ]\n    .into_iter()\n    .filter(|role| roles.contains(role))\n    .collect::&lt;Vec&lt;_&gt;&gt;()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「!matches!(\n        roles.as_slice(),\n        [VerificationRole::Reviewer, VerificationRole::Verifier]\n            | [\n                VerificationRole::Reviewer,\n                VerificationRole::Verifier,\n                VerificationRole::AdversarialVerifier\n            ]\n    )」的捕获提前退出分支为「Err_return：Err(error(\n            "durable verification does not contain the canonical verification roles",\n        ))」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(error(\n            "durable verification does not contain the canonical verification roles",\n        ))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「773cfd07f0a3fe9344c2fb1c」先于语句位置「2」的操作「29f17106945e177818796495」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:759`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/393`。

### `crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs::&lt;closure_expression@768:13&gt;`

在调用形式「roles.contains」中提供第 1 个实参「role」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:768`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/394`。

### `crates/winwincode-delivery/src/domain/evidence.rs::checkout_attestation_from_snapshot`

构造捕获记录，字段按源码次序为「product_session_id ← terminal.product_session_id().clone()；execution_job_id ← terminal.execution_job_id().clone()；work_run_id ← terminal.work_run_id().clone()；role_id ← terminal.role_id().into()；attempt ← terminal.attempt()；lease_id ← terminal.lease_id().clone()；fencing_token ← terminal.fencing_token().clone()；worker_id ← terminal.worker_id().clone()；worker_instance_id ← terminal.worker_instance_id().clone()；worker_session_id ← terminal.worker_session_id().clone()；codex_thread_id ← terminal.codex_thread_id().clone()；repository ← snapshot.repository().clone()」；其余字段见完整操作。不据构造形式推断物理持久化。 以无显式实参的调用形式「terminal.product_session_id」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-delivery/src/domain/evidence.rs:131`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/395`。

### `crates/winwincode-delivery/src/domain/evidence.rs::accepted_runtime_source`

构造捕获记录，字段按源码次序为「source_event_id ← source_event_id；evidence_type ← evidence_type；product_session_id ← terminal.product_session_id().clone()；execution_job_id ← terminal.execution_job_id().clone()；worker_session_id ← terminal.worker_session_id().clone()；codex_thread_id ← terminal.codex_thread_id().clone()；work_run_id ← terminal.work_run_id().clone()；role_id ← terminal.role_id().into()；attempt ← terminal.attempt()；lease_id ← terminal.lease_id().clone()；fencing_token ← terminal.fencing_token().clone()；worker_id ← terminal.worker_id().clone()」；其余字段见完整操作。不据构造形式推断物理持久化。 以无显式实参的调用形式「terminal.product_session_id().clone」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。 以字段投影形式「source_event_id」关联路径「source_event_id」；只描述捕获来源，不证明当时的字段值。

源码：`crates/winwincode-delivery/src/domain/evidence.rs:154`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/396`。

### `crates/winwincode-delivery/src/domain/evidence.rs::resolve_delivery_evidence`

构造捕获记录，字段按源码次序为「schema_version ← super::DELIVERY_SCHEMA_VERSION；id ← evidence_id；delivery_id ← delivery.id().clone()；delivery_spec_id ← delivery.snapshot().spec.id.clone()；delivery_spec_revision ← delivery.snapshot().spec.revision；work_run_id ← work_run.id.clone()；session_binding_id ← binding.id.clone()；candidate_ref ← candidate.candidate_ref().into()；evidence_type ← source.evidence_type；source_ref ← source.source_ref；created_at_millis ← input.created_at_millis」。不据构造形式推断物理持久化。 将「candidate」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-delivery/src/domain/evidence#resolve_runtime_source」，对应捕获形参「candidate: &amp;FrozenDeliveryCandidate」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「source」的初始化来源为「match &amp;input.source {\n        EvidenceSource::Runtime {\n            evidence_type,\n            source_event_id,\n            accepted_sources,\n            terminal,\n            checkout,\n        } =&gt; resolve_runtime_source(\n            candidate,\n            work_run,\n            binding,\n            *evidence_type,\n            source_event_id,\n …［展示截断；完整操作保留］」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以字段投影形式「input.created_at_millis」关联路径「input.created_at_millis」；只描述捕获来源，不证明当时的字段值。 记录消息形状中的固定文本字段「schema_version」及捕获形式「super::DELIVERY_SCHEMA_VERSION」。单个文本字段不是跨语言调用或传输成功的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「529c6cffcb3d068faa534cf2」先于语句位置「1」的操作「aee9412a778dd83e2107aa33」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「candidate」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-delivery/src/domain/evidence#resolve_direct_candidate_source」，对应捕获形参「candidate: &amp;FrozenDeliveryCandidate」。该普通调用关系不替代进程或网络协议关系。

源码：`crates/winwincode-delivery/src/domain/evidence.rs:417`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/397`。

### `crates/winwincode-delivery/src/domain/evidence.rs::&lt;closure_expression@422:66&gt;`

在调用形式「resolution_error」中提供第 1 个实参「EvidenceResolutionErrorCode::CandidateStale」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/evidence.rs:422`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/398`。

### `crates/winwincode-delivery/src/domain/evidence.rs::&lt;closure_expression@482:45&gt;`

在调用形式「resolution_error」中提供第 1 个实参「EvidenceResolutionErrorCode::InvalidEvidence」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/evidence.rs:482`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/399`。

### `crates/winwincode-delivery/src/domain/evidence.rs::resolve_direct_candidate_source`

构造捕获记录，字段按源码次序为「evidence_type ← EvidenceRefType::Commit；source_ref ← format!("git_commit:{}", candidate.candidate_commit_id())；outcome ← VerifiedEvidenceOutcome::Observed；identity ← VerifiedEvidenceSourceIdentity::CandidateCommit {\n                candidate_ref: candidate.candidate_ref().into(),\n                candidate_commit_id: candid…［展示截断；完整操作保留］」。不据构造形式推断物理持久化。 将「candidate」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-delivery/src/domain/evidence#assert_direct_candidate_producer」，对应捕获形参「candidate: &amp;FrozenDeliveryCandidate」。该普通调用关系不替代进程或网络协议关系。 保留同一块中的正常源码顺序：语句位置「0」的操作「95864af16dadc306698bdf11」先于语句位置「1」的操作「0f7443fb35d5c70041e9f47a」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-delivery/src/domain/evidence.rs:531`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/400`。

### `crates/winwincode-delivery/src/domain/evidence.rs::resolve_runtime_source`

构造捕获记录，字段按源码次序为「execution ← expected_identity；source_sequence ← fact.source_sequence；terminal_last_event_sequence ← accepted_terminal_sequence(terminal)；candidate_ref ← fact.candidate_ref.clone()；checkout_commit_id ← checkout.checkout_commit_id.clone()；checkout_tree_id ← checkout.checkout_tree_id.clone()；command_digest ← fact.command_digest.clone()」。不据构造形式推断物理持久化。 在调用形式「portable_identifier」中提供第 1 个实参「&amp;source_event_id.0」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「expected_identity」的初始化来源为「validate_runtime_terminal(\n        candidate,\n        work_run,\n        binding,\n        terminal,\n        evidence_created_at_millis,\n    )?」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「evidence_type == EvidenceRefType::PullRequest」的捕获提前退出分支为「Err_return：Err(resolution_error(\n            EvidenceResolutionErrorCode::InvalidEvidence,\n            "runtime evidence type is unsupported",\n        ))」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(resolution_error(\n            EvidenceResolutionErrorCode::InvalidEvidence,\n            "runtime evidence type is unsupported",\n        ))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「evidence_type」关联路径「evidence_type」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「1」的操作「c519216dd7fba8c82ecc76ed」先于语句位置「2」的操作「b8414a5b8e5ad3faa0249c99」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-delivery/src/domain/evidence.rs:743`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/401`。

### `crates/winwincode-delivery/src/domain/evidence.rs::&lt;closure_expression@760:79&gt;`

在调用形式「resolution_error」中提供第 1 个实参「EvidenceResolutionErrorCode::InvalidEvidence」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/evidence.rs:760`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/402`。

### `crates/winwincode-delivery/src/domain/evidence.rs::&lt;closure_expression@817:83&gt;`

在调用形式「resolution_error」中提供第 1 个实参「EvidenceResolutionErrorCode::InvalidEvidence」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-delivery/src/domain/evidence.rs:817`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/403`。

### `crates/winwincode-delivery/src/domain/evidence.rs::validate_runtime_terminal`

构造捕获记录，字段按源码次序为「product_session_id ← terminal.product_session_id().clone()；execution_job_id ← terminal.execution_job_id().clone()；work_run_id ← terminal.work_run_id().clone()；role_id ← terminal.role_id().into()；attempt ← terminal.attempt()；lease_id ← terminal.lease_id().clone()；fencing_token ← terminal.fencing_token().clone()；worker_id ← terminal.worker_id().clone()；worker_instance_id ← terminal.worker_instance_id().clone()；worker_session_id ← terminal.worker_session_id().clone()；codex_thread_id ← terminal.codex_thread_id().clone()」。不据构造形式推断物理持久化。 将「terminal」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-delivery/src/domain/evidence#accepted_terminal_sequence」，对应捕获形参「terminal: &amp;AcceptedVerificationJobOutcomeFact」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「worker_session_id」的初始化来源为「binding\n        .worker_session_id\n        .as_ref()\n        .expect("complete binding")」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「terminal.product_session_id() != &amp;binding.product_session_id\n        || terminal.execution_job_id() != &amp;binding.execution_job_id\n        || terminal.worker_session_id() != worker_session_id\n        || terminal.codex_thread_id() != codex_thread_id\n        || terminal.work_run_id() != &amp;work_run.id\n        || terminal.attempt() != u64::try_from(work_run.at…［展示截断；完整操作保留］」的捕获提前退出分支为「Err_return：Err(resolution_error(\n            EvidenceResolutionErrorCode::SessionMismatch,\n            "runtime terminal result belongs to another product, job, worker, thread, stage, or role",\n        ))」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(resolution_error(\n            EvidenceResolutionErrorCode::SessionMismatch,\n            "runtime terminal result belongs to another product, job, worker, thread, stage, or role",\n        ))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「a866567697145e4ac93490b1」先于语句位置「1」的操作「d424088319aee1dfec2f35a6」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-delivery/src/domain/evidence.rs:841`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/404`。

### `crates/winwincode-delivery/src/domain/evidence.rs::validate_checkout_attestation`

将「checkout」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-delivery/src/domain/evidence#checkout_identity」，对应捕获形参「fact: &amp;ValidatedCheckoutAttestationFact」。该普通调用关系不替代进程或网络协议关系。 条件「checkout_identity(checkout) != *expected_identity」的捕获提前退出分支为「Err_return：Err(resolution_error(\n            EvidenceResolutionErrorCode::SessionMismatch,\n            "checkout attestation belongs to another fenced execution",\n        ))」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(resolution_error(\n            EvidenceResolutionErrorCode::SessionMismatch,\n            "checkout attestation belongs to another fenced execution",\n        ))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「c3b8972fe318e48c859e5a86」先于语句位置「1」的操作「48289fd1c740a7d1a1c089ca」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-delivery/src/domain/evidence.rs:898`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/405`。

### `crates/winwincode-delivery/src/domain/evidence.rs::runtime_source_identity`

构造捕获记录，字段按源码次序为「product_session_id ← fact.product_session_id.clone()；execution_job_id ← fact.execution_job_id.clone()；work_run_id ← fact.work_run_id.clone()；role_id ← fact.role_id.clone()；attempt ← fact.attempt；lease_id ← fact.lease_id.clone()；fencing_token ← fact.fencing_token.clone()；worker_id ← fact.worker_id.clone()；worker_instance_id ← fact.worker_instance_id.clone()；worker_session_id ← fact.worker_session_id.clone()；codex_thread_id ← fact.codex_thread_id.clone()」。不据构造形式推断物理持久化。 以无显式实参的调用形式「fact.product_session_id.clone」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。 以字段投影形式「fact.product_session_id.clone()」关联路径「fact.product_session_id」；只描述捕获来源，不证明当时的字段值。

源码：`crates/winwincode-delivery/src/domain/evidence.rs:921`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/406`。

### `crates/winwincode-provider/src/device_model.rs::DeviceProviderStore.execute_model`

在调用形式「self.model_cancelled」中提供第 1 个实参「&amp;open.model_exchange_id.0」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「digest」的初始化来源为「format!("{:x}", Sha256::digest(serde_json::to_vec(open)?))」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「original != digest」的捕获提前退出分支为「Err_return：Err(DeviceProviderError)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Ok(Vec::new())」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「77ab72c47e42e39664d03603」先于语句位置「1」的操作「c5d657cc8e474a456185136a」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

条件「self.model_cancelled(&amp;open.model_exchange_id.0)?」的捕获提前退出分支为「return：Ok(Vec::new())」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。

源码：`crates/winwincode-provider/src/device_model.rs:26`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/407`。

### `crates/winwincode-provider/src/device_model.rs::&lt;closure_expression@41:13&gt;`

在调用形式「Ok」中提供第 1 个实参「(row.get(0)?, row.get(1)?)」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-provider/src/device_model.rs:41`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/408`。

### `crates/winwincode-provider/src/device_model.rs::DeviceProviderStore.invoke_model`

构造捕获记录，字段按源码次序为「model_exchange_id ← &amp;open.model_exchange_id；request_id ← &amp;open.request_id；adapter_request_id ← &amp;adapter_request_id；model_id ← model_id；content_type ← &amp;open.request.content_type；payload ← &amp;payload」。不据构造形式推断物理持久化。 将「&amp;config」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-provider/src/device_store#adapter」，对应捕获形参「config: &amp;DeviceProviderConfig」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「payload」的初始化来源为「STANDARD\n            .decode(&amp;open.request.data_base64)\n            .map_err(|_| DeviceProviderError)?」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「open.request.data_base64.len() &gt; 24 * 1024 * 1024\n            || open.request.content_type != "application/json"」的捕获提前退出分支为「Err_return：Err(DeviceProviderError)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(DeviceProviderError)」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「&amp;open.model_exchange_id」关联路径「open.model_exchange_id」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「5de224f4e8fa2e7b9ba8d460」先于语句位置「1」的操作「e8716d85df35edc9af22b4db」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-provider/src/device_model.rs:69`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/409`。

### `crates/winwincode-provider/src/device_model.rs::&lt;closure_expression@158:18&gt;`

在调用形式「Ok」中提供第 1 个实参「chunk」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。 包含赋值/更新「chunk.payload = Some(frame.encoded_payload())」，捕获目标为「chunk.payload」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「chunk」的初始化来源为「model_chunk(\n                    open,\n                    i64::try_from(frame.sequence()).map_err(|_| DeviceProviderError)?,\n                )」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留同一块中的正常源码顺序：语句位置「0」的操作「e6b177ea7104f26c64e41b7e」先于语句位置「1」的操作「5966e62ca4dc0f8c3fb091b9」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-provider/src/device_model.rs:158`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/410`。

### `crates/winwincode-provider/src/device_store.rs::DeviceProviderStore.open`

构造捕获记录，字段按源码次序为「connection ← connection；key ← key」。不据构造形式推断物理持久化。 以无显式实参的调用形式「new_secret_key」调用已绑定接口「rust:crates/winwincode-provider/src/device_store#new_secret_key」；没有据调用存在断言激活、存储或网络效果。 捕获 binding「key」的初始化来源为「new_secret_key()?」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「!meta.is_dir() || meta.permissions().mode() &amp; 0o077 != 0」的捕获提前退出分支为「Err_return：Err(DeviceProviderError)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(DeviceProviderError)」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「connection」关联路径「connection」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「bf2a3db9e8172caaa0d9987e」先于语句位置「1」的操作「b49afabc93b7ed5467cbc082」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-provider/src/device_store.rs:79`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/411`。

### `crates/winwincode-provider/src/device_store.rs::&lt;closure_expression@110:77&gt;`

在调用形式「row.get」中提供第 1 个实参「0」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-provider/src/device_store.rs:110`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/412`。

### `crates/winwincode-provider/src/device_store.rs::&lt;closure_expression@139:13&gt;`

在调用形式「row.get」中提供第 1 个实参「0」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-provider/src/device_store.rs:139`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/413`。

### `crates/winwincode-provider/src/device_store.rs::DeviceProviderStore.resolve`

将「&amp;config」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-provider/src/device_store#valid_device_provider_config」，对应捕获形参「config: &amp;DeviceProviderConfig」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「secret」的初始化来源为「ResolvedSecret::from_bytes(secret).map_err(|_| DeviceProviderError)?」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「!valid_device_provider_config(&amp;config)」的捕获提前退出分支为「Err_return：Err(DeviceProviderError)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(DeviceProviderError)」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「03189aaab2787d3057a997df」先于语句位置「1」的操作「81ac34eb4b306cf9c94bb4d3」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-provider/src/device_store.rs:471`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/414`。

### `crates/winwincode-provider/src/device_store.rs::&lt;closure_expression@478:13&gt;`

在调用形式「Ok」中提供第 1 个实参「(row.get(0)?, row.get(1)?)」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-provider/src/device_store.rs:478`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/415`。

### `crates/winwincode-provider/src/device_store.rs::adapter`

构造捕获记录，字段按源码次序为「connect ← Duration::from_secs(15)；idle ← Duration::from_mins(1)；total ← Duration::from_mins(5)」。不据构造形式推断物理持久化。 将「config.provider_id.clone()」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-provider/src/provider_https_sse#HttpsSseProviderConfig.try_new」，对应捕获形参「provider_id: String」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「transport」的初始化来源为「HttpsSseProviderConfig::try_new(\n        config.provider_id.clone(),\n        config.endpoint.clone(),\n        HttpsSseProviderTimeouts {\n            connect: Duration::from_secs(15),\n            idle: Duration::from_mins(1),\n            total: Duration::from_mins(5),\n        },\n        HttpsSseProviderLimits {\n            response_bytes: 16 * 1024 *…［展示截断；完整操作保留］」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「transport」存在源更新「transport = transport\n            .with_specific_tls_roots(vec![fs::read(path)?])\n            .map_err(|_| DeviceProviderError)?」；循环和分支条件见操作上下文，未推执行次数或最终数值。 保留同一块中的正常源码顺序：语句位置「0」的操作「77a65afd528492cabad2c6ac」先于语句位置「1」的操作「6543b0d409a0ae35091dc246」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-provider/src/device_store.rs:526`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/416`。

### `crates/winwincode-provider/src/provider_https_sse.rs::&lt;HttpsSseProviderAdapter as ProviderAdapterPort&gt;.open`

在调用形式「HttpInvocation::from_adapter」中提供第 1 个实参「invocation」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`crates/winwincode-provider/src/provider_https_sse.rs:796`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/417`。

### `crates/winwincode-provider/src/types.rs::ResolvedSecret.from_bytes`

构造捕获记录，字段按源码次序为「bytes ← bytes」。不据构造形式推断物理持久化。 在调用形式「Ok」中提供第 1 个实参「Self { bytes }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 条件「bytes.is_empty()」的捕获提前退出分支为「Err_return：Err(SecretStoreError::corrupt())」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(SecretStoreError::corrupt())」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「bytes」关联路径「bytes」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「ac9c1a76540800fd17373f13」先于语句位置「1」的操作「ab2c7f85cf2dc399ec1720c6」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-provider/src/types.rs:499`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/418`。

### `crates/winwincode-server/src/application.rs::StandaloneControlPlaneApplication.delivery_command`

将「&amp;mut state.storage」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-control-plane/src/strongflow_device_execution#dispatch_work_run_to_device_worker」，对应捕获形参「storage: &amp;mut SqliteStorage」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「dispatch_now」的初始化来源为「self.clock.now_instant()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「_」的捕获提前退出分支为「Err_return：Err(application_variant_mismatch())」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(application_variant_mismatch())」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「a7db68023b49cceeeb66e6b8」先于语句位置「1」的操作「574be090a55a84f1b2c57bb6」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-server/src/application.rs:620`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/419`。

### `crates/winwincode-server/src/application.rs::&lt;closure_expression@672:22&gt;`

在调用形式「delivery_application_error」中提供第 1 个实参「&amp;error」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-server/src/application.rs:672`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/420`。

### `crates/winwincode-server/src/application.rs::&lt;closure_expression@702:22&gt;`

在调用形式「strongflow_device_dispatch_error」中提供第 1 个实参「&amp;error」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-server/src/application.rs:702`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/421`。

### `crates/winwincode-server/src/application.rs::&lt;closure_expression@706:22&gt;`

以无显式实参的调用形式「error.api_error」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-server/src/application.rs:706`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/422`。

### `crates/winwincode-server/src/application.rs::&lt;StandaloneControlPlaneApplication as TypedControlPlaneApiPort&gt;.command`

将「request」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-server/src/application#StandaloneControlPlaneApplication.delivery_command」，对应捕获形参「request: CommandRequest」。该普通调用关系不替代进程或网络协议关系。

源码：`crates/winwincode-server/src/application.rs:1232`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/423`。

### `crates/winwincode-server/src/dispatcher.rs::&lt;GeneratedContractDispatcher as ControlPlaneApiPort&gt;.command`

将「request.clone()」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-server/src/dispatcher#decode」，对应捕获形参「value: Value」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「envelope」的初始化来源为「decode(request.clone())?」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留同一块中的正常源码顺序：语句位置「0」的操作「77499fab2a917eba5c320682」先于语句位置「1」的操作「b904492525ea1211d9125936」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-server/src/dispatcher.rs:203`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/424`。

### `crates/winwincode-server/src/main.rs::&lt;DeviceModelBoundary as winwincode_control_plane::DurableExecutionPortDelegate&gt;.accept`

在调用形式「Err」中提供第 1 个实参「winwincode_control_plane::DurableExecutionPortError::UnsupportedMessage」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`crates/winwincode-server/src/main.rs:340`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/425`。

### `crates/winwincode-server/src/server.rs::router`

在调用形式「Router::new()\n        .route("/health", get(health))\n        .route(\n            "/api/v1/auth/session",\n            get(get_auth_session)\n                .post(create_auth_session)\n                .delete(close_auth_session)\n                .options(preflight),\n        )\n        .route(\n            "/api/v1/server/initialization",\n            get…［展示截断；完整操作保留］」中提供第 1 个实参「state」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`crates/winwincode-server/src/server.rs:419`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/426`。

### `crates/winwincode-server/src/server.rs::command`

将「request」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-server/src/server#parse_json_body」，对应捕获形参「request: Request&lt;Body&gt;」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「headers」的初始化来源为「request.headers().clone()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「Err(error)」的捕获提前退出分支为「return：error.into_response()」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return error.into_response()」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「23e479158a64b1a256cc2524」先于语句位置「1」的操作「ffb794eb06711218a2c5be03」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-server/src/server.rs:2337`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/427`。

### `crates/winwincode-server/src/server.rs::parse_json_body`

将「origin」作为第 4 个实参交给已绑定接口「rust:crates/winwincode-server/src/server#BoundaryError.new」，对应捕获形参「origin: Option&lt;HeaderValue&gt;」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「request_id」的初始化来源为「request_id_from_value(&amp;value)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「value.get("schemaVersion").and_then(Value::as_str) != Some(SUPPORTED_SCHEMA_VERSION)」的捕获提前退出分支为「Err_return：Err(BoundaryError::new(\n            StatusCode::UPGRADE_REQUIRED,\n            "CLIENT_UPGRADE_REQUIRED",\n            "client protocol is unsupported; upgrade to winwincode/v1",\n            origin,\n        )\n        .with_request_id(request_id))」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(BoundaryError::new(\n            StatusCode::UPGRADE_REQUIRED,\n            "CLIENT_UPGRADE_REQUIRED",\n            "client protocol is unsupported; upgrade to winwincode/v1",\n            origin,\n        )\n        .with_request_id(request_id))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「a0bae9078810013248c3701e」先于语句位置「1」的操作「9d6fe61358c809b96cce74ad」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-server/src/server.rs:2383`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/428`。

### `crates/winwincode-server/src/server.rs::&lt;closure_expression@2389:18&gt;`

在调用形式「BoundaryError::new」中提供第 1 个实参「StatusCode::PAYLOAD_TOO_LARGE」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-server/src/server.rs:2389`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/429`。

### `crates/winwincode-server/src/server.rs::&lt;closure_expression@2397:63&gt;`

在调用形式「BoundaryError::new」中提供第 1 个实参「StatusCode::BAD_REQUEST」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-server/src/server.rs:2397`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/430`。

### `crates/winwincode-worker/src/device_model.rs::DeviceModels.open`

构造捕获记录，字段按源码次序为「directory ← directory.to_owned()；pending ← HashMap::new()；sender ← sender；receiver ← receiver；chunks ← VecDeque::new()；delivered_high_water ← HashMap::new()；owned_exchanges ← HashSet::new()；session_ids ← HashSet::new()；instance_ids ← HashSet::new()；logged_foreign ← HashSet::new()；intake_log ← intake_log」。不据构造形式推断物理持久化。 将「directory」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-provider/src/device_store#DeviceProviderStore.open」，对应捕获形参「directory: &amp;Path」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「intake_log」的初始化来源为「std::env::var_os("WWC_MODEL_INTAKE_LOG")\n            .map(PathBuf::from)\n            .or_else(|| {\n                // Managed workers keep durable diagnostics beside Codex runtime.\n                // The provider directory itself is shared across Worker sessions\n                // on one Device, so prefer an explicit env path when present.\n            …［展示截断；完整操作保留］」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以字段投影形式「directory.to_owned()」关联路径「directory」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「215416d985383f2a0e038dcb」先于语句位置「1」的操作「51fd45a8213ee08522881081」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-worker/src/device_model.rs:41`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/431`。

### `crates/winwincode-worker/src/device_model.rs::DeviceModels.send`

将「&amp;self.directory」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-provider/src/device_store#DeviceProviderStore.open」，对应捕获形参「directory: &amp;Path」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「id」的初始化来源为「open.model_exchange_id.0.clone()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「self.pending.len() &gt;= 16」的捕获提前退出分支为「Err_return：Err(DeviceProviderError)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return if previous == &amp;digest {\n                        Ok(true)\n                    } else {\n                        Err(DeviceProviderError)\n                    }」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「14418c030a00171c1b67b594」先于语句位置「1」的操作「0a8228c1e33bfabdf4030899」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-worker/src/device_model.rs:122`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/432`。

### `crates/winwincode-worker/src/device_model.rs::&lt;closure_expression@149:28&gt;`

在调用形式「DeviceProviderStore::open(&amp;directory)\n                            .and_then(|store| store.execute_model(&amp;open))\n                            .unwrap_or_else」中提供第 1 个实参「|_| {\n                                vec![model_failure(\n                                    &amp;open,\n                                    "DEVICE_MODEL_FAILED: local request could not complete",\n                                )]\n                            }」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。 捕获 binding「chunks」的初始化来源为「DeviceProviderStore::open(&amp;directory)\n                            .and_then(|store| store.execute_model(&amp;open))\n                            .unwrap_or_else(|_| {\n                                vec![model_failure(\n                                    &amp;open,\n                                    "DEVICE_MODEL_FAILED: local request could not complete",\n    …［展示截断；完整操作保留］」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留同一块中的正常源码顺序：语句位置「0」的操作「23b141e460d16e8f95699d91」先于语句位置「1」的操作「290cc343a7d570621ebfacff」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-worker/src/device_model.rs:149`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/433`。

### `crates/winwincode-worker/src/device_model.rs::&lt;closure_expression@151:39&gt;`

在调用形式「store.execute_model」中提供第 1 个实参「&amp;open」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-worker/src/device_model.rs:151`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/434`。

### `crates/winwincode-worker/src/lib.rs::WorkerMain.with_device_providers`

将「directory」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-worker/src/device_model#DeviceModels.open」，对应捕获形参「directory: &amp;Path」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「self.device_models = Some(models)」，捕获目标为「self.device_models」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「models」的初始化来源为「device_model::DeviceModels::open(directory)?」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留同一块中的正常源码顺序：语句位置「0」的操作「8ebde03256f2911af1772fb7」先于语句位置「1」的操作「10467b3aabb7584860923541」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-worker/src/lib.rs:409`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/435`。

### `crates/winwincode-worker/src/lib.rs::WorkerMain.new`

构造捕获记录，字段按源码次序为「device_models ← None；intake_log_path ← None；config ← config；port ← port；codex ← codex；workspaces ← workspaces；lifecycle ← WorkerLifecycleState::Booting；registration_request_id ← None；registration_request_namespace ← None；heartbeat_interval_ms ← None；heartbeat_sequence ← heartbeat_sequence；request_sequence ← 0」；其余字段见完整操作。不据构造形式推断物理持久化。 将「&amp;mut codex」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-worker/src/lib#recover_message_sequence」，对应捕获形参「codex: &amp;mut Codex」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「message_sequence」的初始化来源为「recover_message_sequence(&amp;mut codex)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以字段投影形式「config」关联路径「config」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「75d339f112ca9cb96a8ae994」先于语句位置「1」的操作「aa40137a2b7fdb5d6964145d」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-worker/src/lib.rs:481`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/436`。

### `crates/winwincode-worker/src/lib.rs::WorkerMain.accept_control`

将「dispatch」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-worker/src/lib#WorkerMain.accept_dispatch」，对应捕获形参「dispatch: &amp;JobDispatchMessage」。该普通调用关系不替代进程或网络协议关系。 条件「self\n                    .workspaces\n                    .is_observation_model_exchange(&amp;chunk.model_exchange_id)\n                    .map_err(|_| workspace_error())?」的捕获提前退出分支为「return：self.accept_observation_model_chunk(chunk, &amp;now).await」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return self.accept_observation_model_chunk(chunk, &amp;now).await」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「02907e8fa5db35286be54322」先于语句位置「1」的操作「aa1141197c31566399de6456」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-worker/src/lib.rs:743`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/437`。

### `crates/winwincode-worker/src/lib.rs::&lt;closure_expression@753:30&gt;`

以无显式实参的调用形式「codex_model_error」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-worker/src/lib.rs:753`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/438`。

### `crates/winwincode-worker/src/lib.rs::&lt;closure_expression@775:30&gt;`

以无显式实参的调用形式「workspace_error」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-worker/src/lib.rs:775`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/439`。

### `crates/winwincode-worker/src/lib.rs::&lt;closure_expression@789:30&gt;`

在调用形式「self.log_model_intake」中提供第 3 个实参「chunk」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。 保留同一块中的正常源码顺序：语句位置「0」的操作「6d23e73e0f7ae6bea44c14ce」先于语句位置「2」的操作「045fa7fa27156b00872510ff」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-worker/src/lib.rs:789`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/440`。

### `crates/winwincode-worker/src/lib.rs::&lt;closure_expression@832:30&gt;`

以无显式实参的调用形式「codex_model_error」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-worker/src/lib.rs:832`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/441`。

### `crates/winwincode-worker/src/lib.rs::&lt;closure_expression@835:30&gt;`

以无显式实参的调用形式「codex_model_error」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-worker/src/lib.rs:835`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/442`。

### `crates/winwincode-worker/src/lib.rs::&lt;closure_expression@855:30&gt;`

以无显式实参的调用形式「codex_model_error」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-worker/src/lib.rs:855`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/443`。

### `crates/winwincode-worker/src/lib.rs::WorkerMain.accept_dispatch`

将「dispatch」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-codex/src/contract#CodexRunKey.from_dispatch」，对应捕获形参「dispatch: &amp;JobDispatchMessage」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「status」的初始化来源为「if record.run_key == run_key &amp;&amp; record.job_digest == job_digest {\n                JobDispatchResultMessageStatus::Duplicate\n            } else {\n                JobDispatchResultMessageStatus::Conflict\n            }」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「self.lifecycle != WorkerLifecycleState::Active」的捕获提前退出分支为「Err_return：Err(worker_error(\n                WorkerErrorCode::InvalidLifecycle,\n                "dispatch requires an active registered Worker",\n            ))」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Err(worker_error(\n                WorkerErrorCode::InvalidLifecycle,\n                "dispatch requires an active registered Worker",\n            ))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「5782248bb990cac9314ec7b4」先于语句位置「1」的操作「71d99c876d0fad07311fda06」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「dispatch」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-worker/src/lib#WorkerMain.start_dispatch」，对应捕获形参「dispatch: &amp;JobDispatchMessage」。该普通调用关系不替代进程或网络协议关系。

源码：`crates/winwincode-worker/src/lib.rs:2634`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/444`。

### `crates/winwincode-worker/src/lib.rs::&lt;closure_expression@2652:22&gt;`

在调用形式「worker_error」中提供第 1 个实参「WorkerErrorCode::UnexpectedMessage」；目标绑定为「captured_source_only」，不指定唯一实现或物理效果。

源码：`crates/winwincode-worker/src/lib.rs:2652`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/445`。

### `crates/winwincode-worker/src/lib.rs::WorkerMain.start_dispatch`

构造捕获记录，字段按源码次序为「run_key ← &amp;run_key；worker_id ← &amp;self.config.worker_id；job ← &amp;dispatch.job；lease ← &amp;dispatch.lease；worker_session_id ← &amp;prepared.active.worker_session_id；workspace ← &amp;prepared.checkout；workspace_revision ← &amp;prepared.workspace_revision」。不据构造形式推断物理持久化。 将「dispatch」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-worker/src/lib#WorkerMain.prepare_dispatch_workspace」，对应捕获形参「dispatch: &amp;JobDispatchMessage」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「prepared.active.last_event_sequence =\n            self.recovered_runtime_cursor(&amp;prepared.active.session_identity)?」，捕获目标为「prepared.active.last_event_sequence」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「thread_id」的初始化来源为「thread_session.thread_id」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「Err(_error)」的捕获提前退出分支为「return：Ok(())」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Ok(())」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「&amp;run_key」关联路径「run_key」；只描述捕获来源，不证明当时的字段值。

源码：`crates/winwincode-worker/src/lib.rs:2714`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/446`。

### `crates/winwincode-worker/src/lib.rs::WorkerMain.send_execution_message`

在调用形式「models.send」中提供第 1 个实参「&amp;message」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 条件「let Some(models) = &amp;mut self.device_models\n            &amp;&amp; models.send(&amp;message).map_err(|_| codex_model_error())?」的捕获提前退出分支为「return：Ok(())」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Ok(())」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「01a2874a197f0e045bbdaffe」先于语句位置「1」的操作「be54cba74dfa00ca16375a01」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-worker/src/lib.rs:3953`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/447`。

### `crates/winwincode-worker/src/lib.rs::&lt;closure_expression@3958:46&gt;`

以无显式实参的调用形式「codex_model_error」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-worker/src/lib.rs:3958`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/448`。

### `crates/winwincode-worker/src/lib.rs::&lt;closure_expression@3965:22&gt;`

以无显式实参的调用形式「execution_port_error」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-worker/src/lib.rs:3965`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/449`。

### `crates/winwincode-worker/src/main.rs::main`

将「&amp;config_path」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-worker/src/main#run_managed」，对应捕获形参「config_path: &amp;str」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「args」的初始化来源为「env::args().skip(1)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留同一块中的正常源码顺序：语句位置「0」的操作「4b97acf75e8c29d5cd31fce9」先于语句位置「1」的操作「6d7f9ae653567a9f6cd1be97」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 以无显式实参的调用形式「run_remote」调用已绑定接口「rust:crates/winwincode-worker/src/main#run_remote」；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-worker/src/main.rs:34`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/450`。

### `crates/winwincode-worker/src/main.rs::run_remote`

构造捕获记录，字段按源码次序为「exit_after_work ← false；worker_id ← WorkerId(required("WWC_WORKER_ID")?)；worker_instance_id ← WorkerInstanceId(required("WWC_WORKER_INSTANCE_ID")?)；started_at ← env::var("WWC_WORKER_STARTED_AT").map_or(now_instant()?, Instant)；data_directory ← PathBuf::from(required("WWC_WORKER_DATA_DIRECTORY")?)；provider_directory ← PathBuf::from(required("WWC_DEVICE_PROVIDER_DIRECTORY")?)；source_directory ← PathBuf::from(required("WWC_WORKER_SOURCE_ROOT")?)；server_origin ← required("WWC_WORKER_SERVER_ORIGIN")?；credential_path ← PathBuf::from(required("WWC_WORKER_CREDENTIAL_FILE")?)；model_route ← default_model_route()」。不据构造形式推断物理持久化。 将「bootstrap」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-worker/src/main#run_worker」，对应捕获形参「bootstrap: WorkerBootstrap」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「bootstrap」的初始化来源为「WorkerBootstrap {\n        exit_after_work: false,\n        worker_id: WorkerId(required("WWC_WORKER_ID")?),\n        worker_instance_id: WorkerInstanceId(required("WWC_WORKER_INSTANCE_ID")?),\n        started_at: env::var("WWC_WORKER_STARTED_AT").map_or(now_instant()?, Instant),\n        data_directory: PathBuf::from(required("WWC_WORKER_DATA_DIRECTORY")?),…［展示截断；完整操作保留］」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留同一块中的正常源码顺序：语句位置「0」的操作「769493f4f6c5d08e9254a00a」先于语句位置「1」的操作「f61fd50cb5c7332ba5199110」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-worker/src/main.rs:97`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/451`。

### `crates/winwincode-worker/src/main.rs::run_managed`

构造捕获记录，字段按源码次序为「exit_after_work ← true；worker_id ← config.worker_id.clone()；worker_instance_id ← config.worker_instance_id.clone()；started_at ← now_instant()?；data_directory ← config.data_directory.clone()；provider_directory ← config.provider_directory.clone()；source_directory ← config.source_directory.clone()；server_origin ← config.server_origin.clone()；credential_path ← credential.path().to_path_buf()；model_route ← config\n            .model_route\n            .clone()\n            .unwrap_or_else(default_model_route)」。不据构造形式推断物理持久化。 在调用形式「std::path::Path::new」中提供第 1 个实参「config_path」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「config」的初始化来源为「ManagedSessionConfig::read(std::path::Path::new(config_path))?」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以字段投影形式「config.worker_id.clone()」关联路径「config.worker_id」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「4bdd96c8a1d9f8fe4d654cad」先于语句位置「1」的操作「13b4f74aaf8cfab5e014ee65」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-worker/src/main.rs:118`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/452`。

### `crates/winwincode-worker/src/main.rs::run_worker`

构造捕获记录，字段按源码次序为「worker_id ← worker_id；worker_instance_id ← worker_instance_id.clone()；started_at ← started_at.clone()；capabilities ← capabilities」。不据构造形式推断物理持久化。 将「capabilities.clone()」作为第 4 个实参交给已绑定接口「rust:crates/winwincode-worker/src/main#production_codex」，对应捕获形参「capabilities: WorkerCapabilitySet」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「capabilities」的初始化来源为「worker_capabilities()?」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「worker」存在源更新「worker = worker.with_observation_model(observation_model)」；循环和分支条件见操作上下文，未推执行次数或最终数值。 以字段投影形式「capabilities」关联路径「capabilities」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「1」的操作「00dacdf40f5f2d6591b30067」先于语句位置「2」的操作「02451f8c5cf3f2b183524d9c」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`crates/winwincode-worker/src/main.rs:154`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/453`。

### `crates/winwincode-worker/src/main.rs::production_codex`

构造捕获记录，字段按源码次序为「data_directory ← data_directory.join("codex-runtime")；helper_executable ← PathBuf::from(required("WWC_WORKER_HELPER_EXECUTABLE")?)；helper_release_manifest ← helper_release_manifest；provider ← provider_id；model ← model_id；gateway_route ← model_route；registered_capabilities ← capabilities；discovered_capabilities ← discovered_capabilities；action_signing_key ← ActionEnforcementSigningKey::from_bytes(parse_hex_key(&amp;required(\n            "WWC_WORKER_ACTION_SIGNING_KEY_HEX",\n        )?)?)?；execution_envelope ← ExecutionEnvelopeToken {\n            version: 1,\n            digest: Sha256Digest(required("WWC_WORKER_EXECUTION_ENVELOPE_DIGEST")?),\n        }；execution_mode ← execution_mode；observer_mode ← observer_mode」。不据构造形式推断物理持久化。 将「provider_directory」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-provider/src/device_store#DeviceProviderStore.open」，对应捕获形参「directory: &amp;Path」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「helper_release_manifest」的初始化来源为「HelperReleaseManifest::from_file(&amp;PathBuf::from(required(\n        "WWC_WORKER_HELPER_RELEASE_MANIFEST",\n    )?))?」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以字段投影形式「model_route」关联路径「model_route」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「5f4666ca2536d2a9465c7387」先于语句位置「1」的操作「f42290f6bb4366d3b1decf48」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「ProductionCodexConfig::try_new(options)?」作为第 1 个实参交给已绑定接口「rust:crates/winwincode-codex/src/adapter#ProductionCodexAdapter.open」，对应捕获形参「mut config: ProductionCodexConfig」。该普通调用关系不替代进程或网络协议关系。

源码：`crates/winwincode-worker/src/main.rs:315`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/454`。

### `crates/winwincode-worker/src/main.rs::&lt;closure_expression@349:25&gt;`

以无显式实参的调用形式「default_provider.config.provider_id.clone」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-worker/src/main.rs:349`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/455`。

### `crates/winwincode-worker/src/main.rs::&lt;closure_expression@351:25&gt;`

以无显式实参的调用形式「default_provider.config.model_ids[0].clone」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`crates/winwincode-worker/src/main.rs:351`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/456`。

### `packages/browser-core/src/query-cache.ts::createQueryCache`

构造捕获记录，字段按源码次序为「client ← client；invalidate ← invalidate；revalidate ← revalidate；clear ← clear；close ← close」。不据构造形式推断物理持久化。 在调用形式「Proxy」中提供第 1 个实参「sourceClient」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「sourceClient」的初始化来源为「options.client」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return Object.freeze(cache)」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「sourceClient.serverUrl」关联路径「sourceClient.serverUrl」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「09d8af6eb85a2ffb7c09c05f」先于语句位置「1」的操作「2c525f06e44f104ea75f6006」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:314`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/457`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.entryFor`

构造捕获记录，字段按源码次序为「actor ← actorIdentity(query.actor)；key ← key；query ← query.query；scope ← scopeIdentity(query.scope)；flight ← null；snapshot ← null；version ← 0」。不据构造形式推断物理持久化。 将「query」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/query-cache#queryCacheKey」，对应捕获形参「query: QueryRequest」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「key」的初始化来源为「queryCacheKey(query)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(existing !== undefined)」的捕获提前退出分支为「return：existing」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return existing」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「query.query」关联路径「query.query」；只描述捕获来源，不证明当时的字段值。 记录消息形状中的固定文本字段「query」及捕获形式「query.query」。单个文本字段不是跨语言调用或传输成功的证明。

源码：`packages/browser-core/src/query-cache.ts:349`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/458`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.matches`

将「invalidation.actor」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/query-cache#actorIdentity」，对应捕获形参「actor: Actor」。该普通调用关系不替代进程或网络协议关系。 以「return (invalidation.actor === undefined\n      || entry.actor === actorIdentity(invalidation.actor))\n      &amp;&amp; (invalidation.scope === undefined\n        || entry.scope === scopeIdentity(invalidation.scope))\n      &amp;&amp; (invalidation.queries === undefined\n        || invalidation.queries.some(query =&gt; query === entry.query))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`packages/browser-core/src/query-cache.ts:368`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/459`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.invalidate`

将「invalidation」作为第 2 个实参交给已绑定接口「ts:packages/browser-core/src/query-cache#createQueryCache.matches」，对应捕获形参「invalidation: QueryInvalidation」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「entry.version += 1」，捕获目标为「entry.version」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「7e154c7a1195a43758fbb5c8」先于语句位置「1」的操作「ef6d90d0eaada4c062609898」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:380`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/460`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.revalidate`

将「query」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/query-cache#queryCacheKey」，对应捕获形参「query: QueryRequest」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「key」的初始化来源为「queryCacheKey(query)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留同一块中的正常源码顺序：语句位置「0」的操作「b6b9da3d637039429020e716」先于语句位置「1」的操作「cce7c9781df16f561914bb12」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:399`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/461`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.clear`

以无显式实参的调用形式「entries.values」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。 保留同一块中的正常源码顺序：语句位置「0」的操作「02df3075256962c956645f16」先于语句位置「1」的操作「9ca8e9995c61caeb60aeae34」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:406`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/462`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.executeFlight`

构造捕获记录，字段按源码次序为「response ← response；version ← entry.version」。不据构造形式推断物理持久化。 将「request.requestId」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/query-cache#cancelled」，对应捕获形参「requestId: QueryRequest['requestId']」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「entry.snapshot = { response, version: entry.version }」，捕获目标为「entry.snapshot」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「next」的初始化来源为「flight.nextRequest」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「request」存在源更新「request = next」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(flight.controller.signal.aborted)」的捕获提前退出分支为「throw：cancelled(request.requestId)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw cancelled(request.requestId)」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`packages/browser-core/src/query-cache.ts:411`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/463`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.startFlight`

构造捕获记录，字段按源码次序为「controller ← controller；consumers ← 0；invalidated ← false；nextRequest ← null；promise ← new Promise&lt;ProductQueryResponse&gt;(() =&gt; {})；settled ← false」。不据构造形式推断物理持久化。 将「entry」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/query-cache#createQueryCache.executeFlight」，对应捕获形参「entry: QueryEntry&lt;ProductQueryRequest, ProductQueryResponse&gt;」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「entry.flight = flight」，捕获目标为「entry.flight」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「controller」的初始化来源为「new AbortController()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return flight」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「controller」关联路径「controller」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「bea66f50832cd807d8458be4」先于语句位置「1」的操作「d8ff201fffe962a175fc6baf」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:435`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/464`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.startFlight.&lt;arrow@449:67&gt;`

在调用形式「entries.get」中提供第 1 个实参「entry.key」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 包含赋值/更新「entry.flight = null」，捕获目标为「entry.flight」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「318a303c9d906a1bcd5423fd」先于语句位置「1」的操作「4c71f6e16cf00e889f36c1ea」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:449`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/465`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.consume`

将「query.requestId」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/query-cache#cancelled」，对应捕获形参「requestId: QueryRequest['requestId']」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「flight.consumers += 1」，捕获目标为「flight.consumers」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「signal」的初始化来源为「requestOptions?.signal」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(signal?.aborted === true)」的捕获提前退出分支为「return：Promise.reject(cancelled(query.requestId))」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Promise.reject(cancelled(query.requestId))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「9faa3cfcef06e992b82c3c66」先于语句位置「1」的操作「61c6dca2bcfed96604a76766」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:461`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/466`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.consume.&lt;arrow@470:23&gt;`

构造捕获记录，字段按源码次序为「once ← true」。不据构造形式推断物理持久化。 在调用形式「signal?.addEventListener」中提供第 3 个实参「{ once: true }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「finished」的初始化来源为「false」；保留该声明与初始化表达式，不推任意后续读取的当前值。 保留同一块中的正常源码顺序：语句位置「0」的操作「8992368f8c531b243a69d7f4」先于语句位置「1」的操作「45c579a3097dcd2c723903c5」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:470`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/467`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.consume.&lt;arrow@470:23&gt;.finish`

在调用形式「signal?.removeEventListener」中提供第 2 个实参「onAbort」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 包含赋值/更新「flight.consumers -= 1」，捕获目标为「flight.consumers」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 对捕获 binding「finished」存在源更新「finished = true」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(finished)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「1e9996cf5d2f78fe35a632a1」先于语句位置「1」的操作「c780c84ad9fe3af55be877f1」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:472`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/468`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.consume.&lt;arrow@470:23&gt;.finish.&lt;block@477:82&gt;.&lt;arrow@478:25&gt;`

以无显式实参的调用形式「flight.controller.abort」调用尚未唯一绑定的目标；没有据调用存在断言激活、存储或网络效果。

源码：`packages/browser-core/src/query-cache.ts:478`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/469`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.consume.&lt;arrow@470:23&gt;.onAbort`

以无显式实参的调用形式「finish」调用已绑定接口「ts:packages/browser-core/src/query-cache#createQueryCache.consume.&lt;arrow@470:23&gt;.finish」；没有据调用存在断言激活、存储或网络效果。 保留同一块中的正常源码顺序：语句位置「0」的操作「d30fef103a1a77372426d573」先于语句位置「1」的操作「79d51658b69383afcb2cab58」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:485`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/470`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.consume.&lt;arrow@470:23&gt;.&lt;arrow@490:31&gt;`

以无显式实参的调用形式「finish」调用已绑定接口「ts:packages/browser-core/src/query-cache#createQueryCache.consume.&lt;arrow@470:23&gt;.finish」；没有据调用存在断言激活、存储或网络效果。 条件「(finished)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「7dcba01fb452b185547da393」先于语句位置「1」的操作「24f7bb7f3cd8940fe6e0cfe3」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:490`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/471`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.consume.&lt;arrow@470:23&gt;.&lt;arrow@494:9&gt;`

以无显式实参的调用形式「finish」调用已绑定接口「ts:packages/browser-core/src/query-cache#createQueryCache.consume.&lt;arrow@470:23&gt;.finish」；没有据调用存在断言激活、存储或网络效果。 条件「(finished)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「763abf51be75ba7a72217736」先于语句位置「1」的操作「246fdb62a8bb93988e959bc3」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:494`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/472`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.cachedQuery`

将「query」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/query-cache#createQueryCache.entryFor」，对应捕获形参「query: ProductQueryRequest」。该普通调用关系不替代进程或网络协议关系。 包含赋值/更新「flight.nextRequest = query」，捕获目标为「flight.nextRequest」；这是所选声明的源写操作，不是唯一所有者或写入已发生的证明。 捕获 binding「entry」的初始化来源为「entryFor(query)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(closed)」的捕获提前退出分支为「return：Promise.reject(clientFailure(\n      'QUERY_CACHE_CLOSED',\n      'The query cache is closed.',\n      query.requestId,\n    ))」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Promise.reject(clientFailure(\n      'QUERY_CACHE_CLOSED',\n      'The query cache is closed.',\n      query.requestId,\n    ))」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「8ddb2a062e4c7115a8c0cee2」先于语句位置「1」的操作「142b8387d2a6f8cda46e7081」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「entry」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/query-cache#createQueryCache.startFlight」，对应捕获形参「entry: QueryEntry&lt;ProductQueryRequest, ProductQueryResponse&gt;」。该普通调用关系不替代进程或网络协议关系。 将「entry」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/query-cache#createQueryCache.consume」，对应捕获形参「entry: QueryEntry&lt;ProductQueryRequest, ProductQueryResponse&gt;」。该普通调用关系不替代进程或网络协议关系。

源码：`packages/browser-core/src/query-cache.ts:502`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/473`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.discardScope`

构造捕获记录，字段按源码次序为「scope ← scope；reason ← reason；discard ← true」。不据构造形式推断物理持久化。 将「{ scope, reason, discard: true }」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/query-cache#createQueryCache.invalidate」，对应捕获形参「invalidation: QueryInvalidation」。该普通调用关系不替代进程或网络协议关系。 以字段投影形式「scope」关联路径「scope」；只描述捕获来源，不证明当时的字段值。

源码：`packages/browser-core/src/query-cache.ts:523`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/474`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.close`

以无显式实参的调用形式「clear」调用已绑定接口「ts:packages/browser-core/src/query-cache#createQueryCache.clear」；没有据调用存在断言激活、存储或网络效果。 对捕获 binding「closed」存在源更新「closed = true」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「a6f663935a8a095e8e5b6257」先于语句位置「1」的操作「8b27e102d4d56641f56212a3」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:527`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/475`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.overrides.restore`

将「'authorization-epoch'」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/query-cache#createQueryCache.clear」，对应捕获形参「_reason: QueryInvalidationReason = 'manual'」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「session」的初始化来源为「await sourceClient.restore(requestOptions)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return session」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「b3acd5de00494bc25dfa89d2」先于语句位置「1」的操作「cfab877887c32103e744747f」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:551`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/476`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.overrides.initializeOwner`

将「'authorization-epoch'」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/query-cache#createQueryCache.clear」，对应捕获形参「_reason: QueryInvalidationReason = 'manual'」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「session」的初始化来源为「await sourceClient.initializeOwner(initialization, requestOptions)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return session」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「59717448352bf66380229ea9」先于语句位置「1」的操作「f020bd81242964816475bc19」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:556`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/477`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.overrides.login`

将「'authorization-epoch'」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/query-cache#createQueryCache.clear」，对应捕获形参「_reason: QueryInvalidationReason = 'manual'」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「session」的初始化来源为「await sourceClient.login(credentials, requestOptions)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return session」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「175d5dc215c31909ce978b0f」先于语句位置「1」的操作「0a25593df28557ae2789b519」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:561`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/478`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.overrides.changePassword`

在调用形式「sourceClient.changePassword」中提供第 1 个实参「change」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return sourceClient.changePassword(change, requestOptions)」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`packages/browser-core/src/query-cache.ts:566`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/479`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.overrides.initializationStatus`

在调用形式「sourceClient.initializationStatus」中提供第 1 个实参「requestOptions」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return sourceClient.initializationStatus(requestOptions)」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`packages/browser-core/src/query-cache.ts:569`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/480`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.overrides.logout`

将「'authorization-epoch'」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/query-cache#createQueryCache.clear」，对应捕获形参「_reason: QueryInvalidationReason = 'manual'」。该普通调用关系不替代进程或网络协议关系。 保留同一块中的正常源码顺序：语句位置「0」的操作「fcfdf425a06a5fdde7d5718c」先于语句位置「1」的操作「08ac7ed817143c74d3dc3cd9」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:572`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/481`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.overrides.command`

构造捕获记录，字段按源码次序为「actor ← command.actor；scope ← command.scope；reason ← 'command'」。不据构造形式推断物理持久化。 将「{ actor: command.actor, scope: command.scope, reason: 'command' }」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/query-cache#createQueryCache.invalidate」，对应捕获形参「invalidation: QueryInvalidation」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「response」的初始化来源为「await sourceClient.command(command, requestOptions)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return response」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「command.actor」关联路径「command.actor」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「53bd729d5841e24d97d08894」先于语句位置「1」的操作「ba306013ef867350ef7bf1a2」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:576`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/482`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.overrides.subscribe`

具有捕获记录构造「{\n        ...subscriptionOptions,\n        onEventQueued(frame) {\n          queuedFrames.add(frame)\n          invalidateForEvent(frame)\n          subscriptionOptions.onEventQueued?.(frame)\n        },\n        async onEvent(frame) {\n          if (!queuedFrames.delete(frame)) invalidateForEvent(frame)\n          await subscriptionOptions.onEvent(frame)\n…［展示截断；完整操作保留］」；该记录的可枚举字段为空或保留开放形状，未把展开来源补成确定字段。 在调用形式「subscriptions.add」中提供第 1 个实参「subscription」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「scope」的初始化来源为「subscriptionOptions.subscription.scope」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「raw」存在源更新「raw = sourceClient.subscribe({\n        ...subscriptionOptions,\n        onEventQueued(frame) {\n          queuedFrames.add(frame)\n          invalidateForEvent(frame)\n          subscriptionOptions.onEventQueued?.(frame)\n        },\n        async onEvent(frame) {\n          if (!queuedFrames.delete(frame)) invalidateForEvent(frame)\n          await subscri…［展示截断；完整操作保留］」；循环和分支条件见操作上下文，未推执行次数或最终数值。 以「return subscription」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留记录复制/展开来源「subscriptionOptions」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「09aa5a95a5a788b041614671」先于语句位置「1」的操作「aa727e0e478bede8fe5b794f」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:582`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/483`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.overrides.subscribe.invalidateForEvent`

构造捕获记录，字段按源码次序为「queries ← queries」。不据构造形式推断物理持久化。 将「{ scope, reason: 'event', ...(queries === undefined ? {} : { queries }) }」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/query-cache#createQueryCache.invalidate」，对应捕获形参「invalidation: QueryInvalidation」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「queries」的初始化来源为「reloadQueries(frame)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「authorizationEpoch」存在源更新「authorizationEpoch = frame.authorizationEpoch」；循环和分支条件见操作上下文，未推执行次数或最终数值。 以字段投影形式「scope」关联路径「scope」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「(queries === undefined ? {} : { queries })」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「3cfc59d814a6c574d392105b」先于语句位置「1」的操作「93f2d80a5957c5473038aef1」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「scope」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/query-cache#createQueryCache.discardScope」，对应捕获形参「scope: Scope」。该普通调用关系不替代进程或网络协议关系。

源码：`packages/browser-core/src/query-cache.ts:588`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/484`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.overrides.subscribe.&lt;object@598:35&gt;.onEventQueued`

将「frame」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/query-cache#createQueryCache.overrides.subscribe.invalidateForEvent」，对应捕获形参「frame: ControlPlaneWebSocketEventFrame」。该普通调用关系不替代进程或网络协议关系。 保留同一块中的正常源码顺序：语句位置「0」的操作「91708e8c0fc3610cf9db0171」先于语句位置「1」的操作「7fe0c5a1243432a39e998b37」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:600`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/485`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.overrides.subscribe.&lt;object@598:35&gt;.onEvent`

将「frame」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/query-cache#createQueryCache.overrides.subscribe.invalidateForEvent」，对应捕获形参「frame: ControlPlaneWebSocketEventFrame」。该普通调用关系不替代进程或网络协议关系。 保留同一块中的正常源码顺序：语句位置「0」的操作「862e93b36ad74502fd84fde1」先于语句位置「1」的操作「f0a5d51dcdb7c9f0114d698f」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:605`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/486`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.overrides.subscribe.&lt;object@598:35&gt;.onResetRequired`

将「scope」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/query-cache#createQueryCache.discardScope」，对应捕获形参「scope: Scope」。该普通调用关系不替代进程或网络协议关系。 条件「(subscriptionOptions.onResetRequired === undefined)」的捕获提前退出分支为「throw：clientFailure(\n            'RESET_REQUIRED',\n            'The subscription needs a complete HTTP reload.',\n          )」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw clientFailure(\n            'RESET_REQUIRED',\n            'The subscription needs a complete HTTP reload.',\n          )」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「3a2d471bc4146deea6271afe」先于语句位置「1」的操作「945a191b0732210d27abd07c」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:609`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/487`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.overrides.subscribe.&lt;object@598:35&gt;.onAuthorizationRevoked`

将「scope」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/query-cache#createQueryCache.discardScope」，对应捕获形参「scope: Scope」。该普通调用关系不替代进程或网络协议关系。 保留同一块中的正常源码顺序：语句位置「0」的操作「8b2fb4be3abda27cf73db468」先于语句位置「1」的操作「d41fdd3abf63ee83b9c3375a」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:617`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/488`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.overrides.subscribe.&lt;object@598:35&gt;.onError`

将「scope」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/query-cache#createQueryCache.discardScope」，对应捕获形参「scope: Scope」。该普通调用关系不替代进程或网络协议关系。

源码：`packages/browser-core/src/query-cache.ts:621`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/489`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.overrides.subscribe.subscription.cursor`

以「return raw.cursor」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`packages/browser-core/src/query-cache.ts:629`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/490`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.overrides.subscribe.subscription.resume`

将「scope」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/query-cache#createQueryCache.discardScope」，对应捕获形参「scope: Scope」。该普通调用关系不替代进程或网络协议关系。 保留同一块中的正常源码顺序：语句位置「0」的操作「b3e0bd78f7b17e9caa9e8ffb」先于语句位置「1」的操作「1704ff367b64507dfd3e62cc」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:630`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/491`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.overrides.subscribe.subscription.reconnect`

将「scope」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/query-cache#createQueryCache.discardScope」，对应捕获形参「scope: Scope」。该普通调用关系不替代进程或网络协议关系。 保留同一块中的正常源码顺序：语句位置「0」的操作「d546f97252808ef464958dfc」先于语句位置「1」的操作「135269951f618dc303273624」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:634`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/492`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.overrides.subscribe.subscription.close`

在调用形式「subscriptions.delete」中提供第 1 个实参「subscription」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 对捕获 binding「active」存在源更新「active = false」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(!active)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「3dcbd459beccad16c1029e04」先于语句位置「1」的操作「65daf41d486677b9c53346d5」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:638`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/493`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.&lt;object@651:41&gt;.get`

在调用形式「Reflect.has」中提供第 1 个实参「overrides」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 捕获 binding「value」的初始化来源为「Reflect.get(target, property, receiver)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(Reflect.has(overrides, property))」的捕获提前退出分支为「return：Reflect.get(overrides, property, overrides)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Reflect.get(overrides, property, overrides)」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「d62b033d8c6ee209f3c8719f」先于语句位置「1」的操作「de0b81d33541a22025daa8ad」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:652`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/494`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.&lt;object@651:41&gt;.set`

在调用形式「Reflect.has」中提供第 1 个实参「overrides」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 条件「(Reflect.has(overrides, property))」的捕获提前退出分支为「return：Reflect.set(overrides, property, value, overrides)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return Reflect.set(overrides, property, value, overrides)」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「f53c84d40a64f4b77728cd27」先于语句位置「1」的操作「0d9628a16c600029f2b1c083」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:657`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/495`。

### `packages/browser-core/src/query-cache.ts::createQueryCache.cache.peek`

构造捕获记录，字段按源码次序为「key ← entry.key；response ← entry.snapshot.response；status ← entry.snapshot.version === entry.version ? 'fresh' : 'stale'」。不据构造形式推断物理持久化。 将「query」作为第 1 个实参交给已绑定接口「ts:packages/browser-core/src/query-cache#queryCacheKey」，对应捕获形参「query: QueryRequest」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「entry」的初始化来源为「entries.get(queryCacheKey(query))」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(entry?.snapshot === null || entry?.snapshot === undefined)」的捕获提前退出分支为「return：null」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return null」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「entry.key」关联路径「entry.key」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「46306937a232894b28e1a3db」先于语句位置「1」的操作「9078e98fb6f3997e07b937d2」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/browser-core/src/query-cache.ts:667`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/496`。

### `packages/control-plane-client/src/index.ts::createControlPlaneClient`

构造捕获记录，字段按源码次序为「serverUrl ← location.serverUrl」。不据构造形式推断物理持久化。 将「options.serverUrl」作为第 1 个实参交给已绑定接口「ts:packages/control-plane-client/src/index#parseControlPlaneServerUrl」，对应捕获形参「value: unknown」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「generated」的初始化来源为「options.generated」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「return {\n    serverUrl: location.serverUrl,\n    async restore(requestOptions) {\n      const session = await authSessionRequest('GET', null, requestOptions)\n      if (session === null) throw new ControlPlaneClientError({\n        kind: 'protocol',\n        code: 'INVALID_AUTH_SESSION_RESPONSE',\n        message: 'The authentication server did not return t…［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「location.serverUrl」关联路径「location.serverUrl」；只描述捕获来源，不证明当时的字段值。 保留同一块中的正常源码顺序：语句位置「0」的操作「cf0c7e3a72173b66e9212600」先于语句位置「1」的操作「78a56f0ea4c4367bb6a25c62」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/control-plane-client/src/index.ts:852`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/497`。

### `packages/control-plane-client/src/index.ts::createControlPlaneClient.requireOpen`

构造捕获记录，字段按源码次序为「kind ← 'protocol'；code ← 'CLIENT_CLOSED'；message ← 'The Control Plane client is closed.'；requestId ← requestId；retryable ← false」。不据构造形式推断物理持久化。 在调用形式「ControlPlaneClientError」中提供第 1 个实参「{\n      kind: 'protocol',\n      code: 'CLIENT_CLOSED',\n      message: 'The Control Plane client is closed.',\n      requestId,\n      retryable: false,\n    }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 条件「(!closed)」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「requestId」关联路径「requestId」；只描述捕获来源，不证明当时的字段值。 记录消息形状中的固定文本字段「kind」及捕获形式「'protocol'」。单个文本字段不是跨语言调用或传输成功的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「3a9ec46ef7d08a1c6b8ea050」先于语句位置「1」的操作「0c2b5f2b18ea73b881a78352」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/control-plane-client/src/index.ts:901`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/498`。

### `packages/control-plane-client/src/index.ts::createControlPlaneClient.reportAccessFailure`

在调用形式「options.onAccessFailure」中提供第 1 个实参「error」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 条件「(error.kind !== 'authentication' &amp;&amp; error.kind !== 'authorization')」的捕获提前退出分支为「return：」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「return」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`packages/control-plane-client/src/index.ts:912`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/499`。

### `packages/control-plane-client/src/index.ts::createControlPlaneClient.throwNormalized`

将「normalized」作为第 1 个实参交给已绑定接口「ts:packages/control-plane-client/src/index#createControlPlaneClient.reportAccessFailure」，对应捕获形参「error: ControlPlaneClientError」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「normalized」的初始化来源为「normalizeError(generated, error, requestId)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 以「throw normalized」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「7a749d0a0253ada6bb4f7c7b」先于语句位置「1」的操作「610fd4b59956fb9d4b0cbb27」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/control-plane-client/src/index.ts:921`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/500`。

### `packages/control-plane-client/src/index.ts::createControlPlaneClient.transportRequest`

构造捕获记录，字段按源码次序为「code ← 'TRANSPORT_UNAVAILABLE'；message ← 'The browser HTTP transport is unavailable.'；requestId ← null；retryable ← false；details ← {}」。不据构造形式推断物理持久化。 在调用形式「transportFetch」中提供第 1 个实参「input」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 条件「(transportFetch === undefined)」的捕获提前退出分支为「throw：generated.createError({\n        code: 'TRANSPORT_UNAVAILABLE',\n        message: 'The browser HTTP transport is unavailable.',\n        requestId: null,\n        retryable: false,\n        details: {},\n      })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw generated.createError({\n        code: 'TRANSPORT_UNAVAILABLE',\n        message: 'The browser HTTP transport is unavailable.',\n        requestId: null,\n        retryable: false,\n        details: {},\n      })」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「signal」关联路径「signal」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「init」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。

源码：`packages/control-plane-client/src/index.ts:927`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/501`。

### `packages/control-plane-client/src/index.ts::createControlPlaneClient.authSessionRequest`

构造捕获记录，字段按源码次序为「kind ← 'authentication'；code ← 'BOOTSTRAP_PROOF_INVALID'；message ← 'Enter a valid bootstrap proof.'；requestId ← null；retryable ← false」。不据构造形式推断物理持久化。 将「requestOptions?.signal」作为第 3 个实参交给已绑定接口「ts:packages/control-plane-client/src/index#createControlPlaneClient.transportRequest」，对应捕获形参「signal: AbortSignal | undefined」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「normalized」的初始化来源为「error instanceof ControlPlaneClientError\n        ? error\n        : new ControlPlaneClientError({\n          kind: 'network',\n          code: 'NETWORK_ERROR',\n          message: 'The authentication server could not be reached.',\n          requestId: null,\n          retryable: true,\n        })」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(signalIsAborted(requestOptions?.signal))」的捕获提前退出分支为「throw：cancelledError(null)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw cancelledError(null)」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「method」关联路径「method」；只描述捕获来源，不证明当时的字段值。 保留记录复制/展开来源「(method === 'GET' ? {} : { 'Content-Type': 'application/json' })」；该形式本身不证明全部字段在覆盖和后续写入后仍被保留。 将「normalized」作为第 1 个实参交给已绑定接口「ts:packages/control-plane-client/src/index#createControlPlaneClient.reportAccessFailure」，对应捕获形参「error: ControlPlaneClientError」。该普通调用关系不替代进程或网络协议关系。

源码：`packages/control-plane-client/src/index.ts:948`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/502`。

### `packages/control-plane-client/src/index.ts::createControlPlaneClient.passwordChangeRequest`

构造捕获记录，字段按源码次序为「method ← 'POST'；headers ← { 'Content-Type': 'application/json' }；body ← JSON.stringify({\n            schemaVersion: CONTROL_PLANE_SCHEMA_VERSION,\n            currentPassword: change.currentPassword,\n            newPassword: chang…［展示截断；完整操作保留］；redirect ← 'error'；cache ← 'no-store'；referrerPolicy ← 'no-referrer'」。不据构造形式推断物理持久化。 将「requestOptions?.signal」作为第 3 个实参交给已绑定接口「ts:packages/control-plane-client/src/index#createControlPlaneClient.transportRequest」，对应捕获形参「signal: AbortSignal | undefined」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「normalized」的初始化来源为「error instanceof ControlPlaneClientError\n        ? error\n        : new ControlPlaneClientError({\n            kind: 'network',\n            code: 'NETWORK_ERROR',\n            message: 'The authentication server could not be reached.',\n            requestId: null,\n            retryable: true,\n          })」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(signalIsAborted(requestOptions?.signal))」的捕获提前退出分支为「throw：cancelledError(null)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw cancelledError(null)」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「change.currentPassword」关联路径「change.currentPassword」；只描述捕获来源，不证明当时的字段值。 记录消息形状中的固定文本字段「method」及捕获形式「'POST'」。单个文本字段不是跨语言调用或传输成功的证明。 将「normalized」作为第 1 个实参交给已绑定接口「ts:packages/control-plane-client/src/index#createControlPlaneClient.reportAccessFailure」，对应捕获形参「error: ControlPlaneClientError」。该普通调用关系不替代进程或网络协议关系。

源码：`packages/control-plane-client/src/index.ts:1039`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/503`。

### `packages/control-plane-client/src/index.ts::createControlPlaneClient.requestFetch`

以「return async (input: string, init: ControlPlaneHttpRequestInit) =&gt; {\n      if (signalIsAborted(signal)) throw generated.createError({\n        code: 'REQUEST_CANCELLED',\n        message: 'The Control Plane operation was cancelled.',\n        requestId,\n        retryable: false,\n        details: {},\n      })\n      let response: ControlPlaneHttpResponse\…［展示截断；完整操作保留］」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。

源码：`packages/control-plane-client/src/index.ts:1090`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/504`。

### `packages/control-plane-client/src/index.ts::createControlPlaneClient.requestFetch.&lt;arrow@1091:11&gt;`

构造捕获记录，字段按源码次序为「code ← 'REQUEST_CANCELLED'；message ← 'The Control Plane operation was cancelled.'；requestId ← requestId；retryable ← false；details ← {}」。不据构造形式推断物理持久化。 将「{\n          method: init.method,\n          headers: init.headers,\n          ...(init.body === undefined ? {} : { body: init.body }),\n        }」作为第 2 个实参交给已绑定接口「ts:packages/control-plane-client/src/index#createControlPlaneClient.transportRequest」，对应捕获形参「init: Omit&lt;ControlPlaneTransportRequestInit, 'credentials' | 'signal'&gt;」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「source」的初始化来源为「await response.text()」；保留该声明与初始化表达式，不推任意后续读取的当前值。 对捕获 binding「response」存在源更新「response = await transportRequest(input, {\n          method: init.method,\n          headers: init.headers,\n          ...(init.body === undefined ? {} : { body: init.body }),\n        }, signal)」；循环和分支条件见操作上下文，未推执行次数或最终数值。 条件「(signalIsAborted(signal))」的捕获提前退出分支为「throw：generated.createError({\n        code: 'REQUEST_CANCELLED',\n        message: 'The Control Plane operation was cancelled.',\n        requestId,\n        retryable: false,\n        details: {},\n      })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw generated.createError({\n        code: 'REQUEST_CANCELLED',\n        message: 'The Control Plane operation was cancelled.',\n        requestId,\n        retryable: false,\n        details: {},\n      })」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「requestId」关联路径「requestId」；只描述捕获来源，不证明当时的字段值。

源码：`packages/control-plane-client/src/index.ts:1091`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/505`。

### `packages/control-plane-client/src/index.ts::createControlPlaneClient.execute`

将「requestOptions?.signal」作为第 1 个实参交给已绑定接口「ts:packages/control-plane-client/src/index#createControlPlaneClient.requestFetch」，对应捕获形参「signal: AbortSignal | undefined」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「requestId」的初始化来源为「requestIdentity(request)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(signalIsAborted(requestOptions?.signal))」的捕获提前退出分支为「throw：cancelledError(requestId)」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw cancelledError(requestId)」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 保留同一块中的正常源码顺序：语句位置「0」的操作「60002c998232d097905fc0e7」先于语句位置「1」的操作「e0ca4e95c1288949ee1385ab」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。 将「requestId」作为第 1 个实参交给已绑定接口「ts:packages/control-plane-client/src/index#createControlPlaneClient.requireOpen」，对应捕获形参「requestId: RequestId | null = null」。该普通调用关系不替代进程或网络协议关系。 将「error」作为第 1 个实参交给已绑定接口「ts:packages/control-plane-client/src/index#createControlPlaneClient.throwNormalized」，对应捕获形参「error: unknown」。该普通调用关系不替代进程或网络协议关系。

源码：`packages/control-plane-client/src/index.ts:1121`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/506`。

### `packages/control-plane-client/src/index.ts::createControlPlaneClient.httpClient`

构造捕获记录，字段按源码次序为「baseUrl ← location.serverUrl；fetch ← fetchImplementation；maxNetworkRetries ← maximumRetries」。不据构造形式推断物理持久化。 在调用形式「generated.createHttpClient」中提供第 1 个实参「{\n      baseUrl: location.serverUrl,\n      fetch: fetchImplementation,\n      maxNetworkRetries: maximumRetries,\n      async waitBeforeRetry(attempt) {\n        await waitBeforeRetry(attempt)\n      },\n    }」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。 以「return generated.createHttpClient({\n      baseUrl: location.serverUrl,\n      fetch: fetchImplementation,\n      maxNetworkRetries: maximumRetries,\n      async waitBeforeRetry(attempt) {\n        await waitBeforeRetry(attempt)\n      },\n    })」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 以字段投影形式「fetchImplementation」关联路径「fetchImplementation」；只描述捕获来源，不证明当时的字段值。

源码：`packages/control-plane-client/src/index.ts:1138`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/507`。

### `packages/control-plane-client/src/index.ts::createControlPlaneClient.httpClient.&lt;object@1139:38&gt;.waitBeforeRetry`

在调用形式「waitBeforeRetry」中提供第 1 个实参「attempt」；目标绑定为「captured_call_site_unknown」，不指定唯一实现或物理效果。

源码：`packages/control-plane-client/src/index.ts:1143`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/508`。

### `packages/control-plane-client/src/index.ts::createControlPlaneClient.&lt;object@1149:9&gt;.restore`

构造捕获记录，字段按源码次序为「kind ← 'protocol'；code ← 'INVALID_AUTH_SESSION_RESPONSE'；message ← 'The authentication server did not return the current browser session.'；requestId ← null；retryable ← false」。不据构造形式推断物理持久化。 将「requestOptions」作为第 3 个实参交给已绑定接口「ts:packages/control-plane-client/src/index#createControlPlaneClient.authSessionRequest」，对应捕获形参「requestOptions: ControlPlaneRequestOptions | undefined」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「session」的初始化来源为「await authSessionRequest('GET', null, requestOptions)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(session === null)」的捕获提前退出分支为「throw：new ControlPlaneClientError({\n        kind: 'protocol',\n        code: 'INVALID_AUTH_SESSION_RESPONSE',\n        message: 'The authentication server did not return the current browser session.',\n        requestId: null,\n        retryable: false,\n      })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new ControlPlaneClientError({\n        kind: 'protocol',\n        code: 'INVALID_AUTH_SESSION_RESPONSE',\n        message: 'The authentication server did not return the current browser session.',\n        requestId: null,\n        retryable: false,\n      })」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 记录消息形状中的固定文本字段「kind」及捕获形式「'protocol'」。单个文本字段不是跨语言调用或传输成功的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「e08ca4669a942a49b5277d5b」先于语句位置「1」的操作「74d807036594a98a674d8c85」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/control-plane-client/src/index.ts:1151`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/509`。

### `packages/control-plane-client/src/index.ts::createControlPlaneClient.&lt;object@1149:9&gt;.initializeOwner`

构造捕获记录，字段按源码次序为「kind ← 'protocol'；code ← 'INVALID_AUTH_SESSION_RESPONSE'；message ← 'The authentication server did not create a browser session.'；requestId ← null；retryable ← false」。不据构造形式推断物理持久化。 将「initialization」作为第 2 个实参交给已绑定接口「ts:packages/control-plane-client/src/index#createControlPlaneClient.authSessionRequest」，对应捕获形参「submission: (ControlPlanePasswordCredentials &amp; {\n      readonly bootstrapProof?: string\n    }) | null」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「session」的初始化来源为「await authSessionRequest('POST', initialization, requestOptions)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(session === null)」的捕获提前退出分支为「throw：new ControlPlaneClientError({\n        kind: 'protocol',\n        code: 'INVALID_AUTH_SESSION_RESPONSE',\n        message: 'The authentication server did not create a browser session.',\n        requestId: null,\n        retryable: false,\n      })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new ControlPlaneClientError({\n        kind: 'protocol',\n        code: 'INVALID_AUTH_SESSION_RESPONSE',\n        message: 'The authentication server did not create a browser session.',\n        requestId: null,\n        retryable: false,\n      })」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 记录消息形状中的固定文本字段「kind」及捕获形式「'protocol'」。单个文本字段不是跨语言调用或传输成功的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「68d991c534f76e072578c729」先于语句位置「1」的操作「4c8897a39f6e37b13b685c2a」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/control-plane-client/src/index.ts:1162`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/510`。

### `packages/control-plane-client/src/index.ts::createControlPlaneClient.&lt;object@1149:9&gt;.login`

构造捕获记录，字段按源码次序为「kind ← 'protocol'；code ← 'INVALID_AUTH_SESSION_RESPONSE'；message ← 'The authentication server did not create a browser session.'；requestId ← null；retryable ← false」。不据构造形式推断物理持久化。 将「credentials」作为第 2 个实参交给已绑定接口「ts:packages/control-plane-client/src/index#createControlPlaneClient.authSessionRequest」，对应捕获形参「submission: (ControlPlanePasswordCredentials &amp; {\n      readonly bootstrapProof?: string\n    }) | null」。该普通调用关系不替代进程或网络协议关系。 捕获 binding「session」的初始化来源为「await authSessionRequest('POST', credentials, requestOptions)」；保留该声明与初始化表达式，不推任意后续读取的当前值。 条件「(session === null)」的捕获提前退出分支为「throw：new ControlPlaneClientError({\n          kind: 'protocol',\n          code: 'INVALID_AUTH_SESSION_RESPONSE',\n          message: 'The authentication server did not create a browser session.',\n          requestId: null,\n          retryable: false,\n        })」；正常继续受该分支限制。退出可能是拒绝、复用或返回结果，未从 return 名称猜测其业务含义。 以「throw new ControlPlaneClientError({\n          kind: 'protocol',\n          code: 'INVALID_AUTH_SESSION_RESPONSE',\n          message: 'The authentication server did not create a browser session.',\n          requestId: null,\n          retryable: false,\n        })」返回捕获表达式/记录，向调用方提供结果来源；消费者激活和实际交付效果另行保留。 记录消息形状中的固定文本字段「kind」及捕获形式「'protocol'」。单个文本字段不是跨语言调用或传输成功的证明。 保留同一块中的正常源码顺序：语句位置「0」的操作「8678ec1748bded7b8efdb1c5」先于语句位置「1」的操作「95392616d7f6adfc47e58957」。顺序本身不证明步骤成功、回调激活或前后记录具有同一身份。

源码：`packages/control-plane-client/src/index.ts:1173`；完整正文与操作引用：`/architecture/responsibility_explanations/declaration_explanations/511`。

其余声明的正文保留在完整职责对象；此处仅限制展示数量。

**实际装配与消息接缝**（源模型与运行效果分开）：

- 所选命令「delivery.update_spec」的生成 TypeScript 记录按「DeliveryUpdateSpecCommand → payload:DeliveryUpdateSpecPayload → spec:DeliverySpecInput」组织字段「verificationCommand」（optional=true）。已认证 Serde 模型将它映射到 Rust 字段「verification_command:Option&lt;String&gt;」，缺失值为「None」，源属性为「#[serde(default, skip_serializing_if = "Option::is_none")]；#[serde(rename = "verificationCommand")]」。在原普通 JSON/已认证 Serde 及成功消息模型条件下，实际「POST /api/v1/commands」序列化记录与 Server 的同一路径解码/dispatcher 记录相接，typed variant 为「DeliveryUpdateSpecCommand」。这是所选协议字段与消息关系，不把 HTTP 已发生、所有 query/WS codec 或跨语言普通调用当成已证明。 原分析关系：`/judgments/1/adapter_judgments/0/evidence/0/details`；完整条件与来源：`/architecture/responsibility_explanations/computed_source_contract_seams/0`。

**显式来源交接**（列实际样例，所有关系保留）：

- 「apps/client/src/application.ts::mountWinWinCodeClient」中的实际记录 literal 语法位置直接构成「apps/client/src/application.ts::mountWinWinCodeClient」的调用实参；没有把记录构造解释为持久提交。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/0`。
- 「apps/client/src/application.ts::mountWinWinCodeClient」的捕获记录与「apps/client/src/application.ts::mountWinWinCodeClient」中的字段投影存在显式源关系；当前值和全部覆盖路径另保留。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/1`。
- 「apps/client/src/application.ts::mountWinWinCodeClient」中的实际记录 literal 语法位置直接构成「apps/client/src/application.ts::mountWinWinCodeClient」的调用实参；没有把记录构造解释为持久提交。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/2`。
- 「apps/client/src/application.ts::mountWinWinCodeClient」的捕获记录与「apps/client/src/application.ts::mountWinWinCodeClient」中的字段投影存在显式源关系；当前值和全部覆盖路径另保留。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/3`。
- 「apps/client/src/application.ts::mountWinWinCodeClient」的捕获记录与「apps/client/src/application.ts::mountWinWinCodeClient」中的字段投影存在显式源关系；当前值和全部覆盖路径另保留。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/4`。
- 「apps/client/src/application.ts::mountWinWinCodeClient」中的实际记录 literal 语法位置直接构成「apps/client/src/application.ts::mountWinWinCodeClient」的调用实参；没有把记录构造解释为持久提交。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/5`。
- 「apps/client/src/application.ts::mountWinWinCodeClient」的捕获记录与「apps/client/src/application.ts::mountWinWinCodeClient」中的字段投影存在显式源关系；当前值和全部覆盖路径另保留。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/6`。
- 「apps/client/src/application.ts::mountWinWinCodeClient」的捕获记录与「apps/client/src/application.ts::mountWinWinCodeClient」中的字段投影存在显式源关系；当前值和全部覆盖路径另保留。 完整引用：`/architecture/responsibility_explanations/explicit_source_transfers/7`。

**接口复用**（列实际样例，所有关系保留）：

- 所选的 3 个确切声明通过已绑定调用复用「rust:crates/kernel/src/lib#Kernel.guard」；复用本身不构成职责混乱或唯一资源所有权的判断。 完整引用：`/architecture/responsibility_explanations/authenticated_interface_reuse/0`。
- 所选的 2 个确切声明通过已绑定调用复用「rust:crates/winwincode-codex/src/adapter#ProductionCodexAdapter.run_key_for_thread」；复用本身不构成职责混乱或唯一资源所有权的判断。 完整引用：`/architecture/responsibility_explanations/authenticated_interface_reuse/1`。
- 所选的 2 个确切声明通过已绑定调用复用「rust:crates/winwincode-codex/src/adapter#conflict」；复用本身不构成职责混乱或唯一资源所有权的判断。 完整引用：`/architecture/responsibility_explanations/authenticated_interface_reuse/2`。
- 所选的 2 个确切声明通过已绑定调用复用「rust:crates/winwincode-codex/src/stage_product#stage_product_job_digest」；复用本身不构成职责混乱或唯一资源所有权的判断。 完整引用：`/architecture/responsibility_explanations/authenticated_interface_reuse/3`。
- 所选的 2 个确切声明通过已绑定调用复用「rust:crates/winwincode-codex/src/stage_product#stage_product_prompt」；复用本身不构成职责混乱或唯一资源所有权的判断。 完整引用：`/architecture/responsibility_explanations/authenticated_interface_reuse/4`。
- 所选的 2 个确切声明通过已绑定调用复用「rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate」；复用本身不构成职责混乱或唯一资源所有权的判断。 完整引用：`/architecture/responsibility_explanations/authenticated_interface_reuse/5`。
- 所选的 3 个确切声明通过已绑定调用复用「rust:crates/winwincode-delivery/src/domain/candidate/verdict_authority#error」；复用本身不构成职责混乱或唯一资源所有权的判断。 完整引用：`/architecture/responsibility_explanations/authenticated_interface_reuse/6`。
- 所选的 3 个确切声明通过已绑定调用复用「rust:crates/winwincode-delivery/src/domain/evidence#resolution_error」；复用本身不构成职责混乱或唯一资源所有权的判断。 完整引用：`/architecture/responsibility_explanations/authenticated_interface_reuse/7`。

职责分析仍有明确缺口：`/architecture/responsibility_explanations/analysis_gaps`、`/architecture/responsibility_explanations/explanation_source_gaps`；已有正文不将缺口标为通过。

## 主要功能链、条件与反证

源码顺序只描述同一次调用正常到达的关系；异步完成、消息传输、远端响应和物理持久化均以实际证据范围为准。

### `wwc-browser-continuation-lifecycle`

分析类型：`browser_async_lifecycle`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/0`；保存发现：`cba5af4fec0e40bdd4f77d2f`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| all_async_callbacks_guarded_proven | false | /functional_chains/0/pattern/all_async_callbacks_guarded_proven |
| all_resources_released_proven | false | /functional_chains/0/pattern/all_resources_released_proven |
| all_stale_results_rejected_proven | false | /functional_chains/0/pattern/all_stale_results_rejected_proven |
| closed_result_disposal_consumers/0/condition_token/members | [] | /functional_chains/0/pattern/closed_result_disposal_consumers/0/condition_token/members |
| closed_result_disposal_consumers/0/condition_token/root_declaration_id | 0d7629777cc8b0e6de78212203160b2123bba2cddb98c7a70186375e29b1e657 | /functional_chains/0/pattern/closed_result_disposal_consumers/0/condition_token/root_declaration_id |
| closed_result_disposal_consumers/0/condition_token/root_declaration_location/column | 7 | /functional_chains/0/pattern/closed_result_disposal_consumers/0/condition_token/root_declaration_location/column |
| closed_result_disposal_consumers/0/condition_token/root_declaration_location/column_base | 1 | /functional_chains/0/pattern/closed_result_disposal_consumers/0/condition_token/root_declaration_location/column_base |
| closed_result_disposal_consumers/0/condition_token/root_declaration_location/column_unit | utf8_bytes | /functional_chains/0/pattern/closed_result_disposal_consumers/0/condition_token/root_declaration_location/column_unit |
| closed_result_disposal_consumers/0/condition_token/root_declaration_location/coordinate_space | captured_text_utf8 | /functional_chains/0/pattern/closed_result_disposal_consumers/0/condition_token/root_declaration_location/coordinate_space |
| closed_result_disposal_consumers/0/condition_token/root_declaration_location/end_byte | 17419 | /functional_chains/0/pattern/closed_result_disposal_consumers/0/condition_token/root_declaration_location/end_byte |
| closed_result_disposal_consumers/0/condition_token/root_declaration_location/end_column | 21 | /functional_chains/0/pattern/closed_result_disposal_consumers/0/condition_token/root_declaration_location/end_column |
| closed_result_disposal_consumers/0/condition_token/root_declaration_location/end_line | 483 | /functional_chains/0/pattern/closed_result_disposal_consumers/0/condition_token/root_declaration_location/end_line |
| closed_result_disposal_consumers/0/condition_token/root_declaration_location/file | apps/client/src/settings-page.ts | /functional_chains/0/pattern/closed_result_disposal_consumers/0/condition_token/root_declaration_location/file |
| closed_result_disposal_consumers/0/condition_token/root_declaration_location/grammar | typescript | /functional_chains/0/pattern/closed_result_disposal_consumers/0/condition_token/root_declaration_location/grammar |
| closed_result_disposal_consumers/0/condition_token/root_declaration_location/line | 483 | /functional_chains/0/pattern/closed_result_disposal_consumers/0/condition_token/root_declaration_location/line |
| closed_result_disposal_consumers/0/condition_token/root_declaration_location/original_file_end_byte | 17419 | /functional_chains/0/pattern/closed_result_disposal_consumers/0/condition_token/root_declaration_location/original_file_end_byte |
| closed_result_disposal_consumers/0/condition_token/root_declaration_location/original_file_start_byte | 17405 | /functional_chains/0/pattern/closed_result_disposal_consumers/0/condition_token/root_declaration_location/original_file_start_byte |
| closed_result_disposal_consumers/0/condition_token/root_declaration_location/parser_version | tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14 | /functional_chains/0/pattern/closed_result_disposal_consumers/0/condition_token/root_declaration_location/parser_version |

所有事实及源位置：`/functional_chains/0/source_facts`；配置声明单列于 `/functional_chains/0/policy_declarations`，不作为自动证据。

### `wwc-captured-record-resource-writers`

分析类型：`resource_writer_ownership`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/1`；保存发现：`dd33866bcd25385a8792a37d`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| ownership_assessment | partial_captured_writers_and_consumers | /functional_chains/1/pattern/ownership_assessment |
| all_mutations_authorized_proven | false | /functional_chains/1/pattern/all_mutations_authorized_proven |
| all_storage_resources_bound_proven | false | /functional_chains/1/pattern/all_storage_resources_bound_proven |
| call_record_and_effect_frontiers/0/activation_and_physical_effect_proven | false | /functional_chains/1/pattern/call_record_and_effect_frontiers/0/activation_and_physical_effect_proven |
| call_record_and_effect_frontiers/1/activation_and_physical_effect_proven | false | /functional_chains/1/pattern/call_record_and_effect_frontiers/1/activation_and_physical_effect_proven |
| call_record_and_effect_frontiers/1/arguments/0/construction/fields/now/value/kind | shorthand_property_identifier | /functional_chains/1/pattern/call_record_and_effect_frontiers/1/arguments/0/construction/fields/now/value/kind |
| call_record_and_effect_frontiers/1/arguments/0/construction/fields/now/value/name | now | /functional_chains/1/pattern/call_record_and_effect_frontiers/1/arguments/0/construction/fields/now/value/name |
| call_record_and_effect_frontiers/1/arguments/0/construction/parts/0/value/kind | shorthand_property_identifier | /functional_chains/1/pattern/call_record_and_effect_frontiers/1/arguments/0/construction/parts/0/value/kind |
| call_record_and_effect_frontiers/1/arguments/0/construction/parts/0/value/name | now | /functional_chains/1/pattern/call_record_and_effect_frontiers/1/arguments/0/construction/parts/0/value/name |
| call_record_and_effect_frontiers/1/arguments/0/construction/runtime_object_or_presence_proven | false | /functional_chains/1/pattern/call_record_and_effect_frontiers/1/arguments/0/construction/runtime_object_or_presence_proven |
| call_record_and_effect_frontiers/2/activation_and_physical_effect_proven | false | /functional_chains/1/pattern/call_record_and_effect_frontiers/2/activation_and_physical_effect_proven |
| call_record_and_effect_frontiers/3/activation_and_physical_effect_proven | false | /functional_chains/1/pattern/call_record_and_effect_frontiers/3/activation_and_physical_effect_proven |
| call_record_and_effect_frontiers/3/arguments/0/construction/fields/serverUrl/value/current_referent_value_proven | false | /functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/fields/serverUrl/value/current_referent_value_proven |
| call_record_and_effect_frontiers/3/arguments/0/construction/fields/serverUrl/value/kind | member_expression | /functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/fields/serverUrl/value/kind |
| call_record_and_effect_frontiers/3/arguments/0/construction/fields/serverUrl/value/member | serverUrl | /functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/fields/serverUrl/value/member |
| call_record_and_effect_frontiers/3/arguments/0/construction/fields/transport/value/kind | identifier | /functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/fields/transport/value/kind |
| call_record_and_effect_frontiers/3/arguments/0/construction/fields/transport/value/name | browserTransport | /functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/fields/transport/value/name |
| call_record_and_effect_frontiers/3/arguments/0/construction/parts/0/value/current_referent_value_proven | false | /functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/parts/0/value/current_referent_value_proven |

所有事实及源位置：`/functional_chains/1/source_facts`；配置声明单列于 `/functional_chains/1/policy_declarations`，不作为自动证据。

### `wwc-delivery-evidence-frozen-contract-slice`

分析类型：`guarded_call_sequence`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/2`；保存发现：`12d0ebaf619479cb00cfc62b`。

**canonical_evidence 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `assert_frozen_candidate_current(delivery, candidate).map_err → assert_frozen_candidate_current`；`crates/winwincode-delivery/src/domain/evidence.rs:422`。
- `evidence_work_run_and_binding`；`crates/winwincode-delivery/src/domain/evidence.rs:428`。
- `resolve_runtime_source → resolve_direct_candidate_source`；`crates/winwincode-delivery/src/domain/evidence.rs:430`。
- `deterministic_evidence_id → delivery.id → delivery.snapshot → candidate.candidate_ref`；`crates/winwincode-delivery/src/domain/evidence.rs:458`。
- `delivery.id().clone → delivery.id → delivery.snapshot().spec.id.clone → delivery.snapshot → work_run.id.clone → binding.id.clone → candidate.candidate_ref().into → candidate.candidate_ref`；`crates/winwincode-delivery/src/domain/evidence.rs:469`。
- `validate(&amp;evidence, "evidence").map_err → validate`；`crates/winwincode-delivery/src/domain/evidence.rs:482`。
- `Ok`；`crates/winwincode-delivery/src/domain/evidence.rs:489`。

**checkout_capture 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `terminal.product_session_id().clone → terminal.product_session_id → terminal.execution_job_id().clone → terminal.execution_job_id → terminal.work_run_id().clone → terminal.work_run_id → terminal.role_id().into → terminal.role_id → terminal.attempt → terminal.lease_id().clone → terminal.lease_id → te…［展示截断；完整值见引用］`；`crates/winwincode-delivery/src/domain/evidence.rs:135`。

**checkout_guard 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `checkout_identity → Err → resolution_error`；`crates/winwincode-delivery/src/domain/evidence.rs:903`。
- `candidate.repository → candidate.candidate_commit_id → candidate.candidate_tree_id → Err → resolution_error`；`crates/winwincode-delivery/src/domain/evidence.rs:909`。
- `Ok`；`crates/winwincode-delivery/src/domain/evidence.rs:918`。

**direct_candidate_source 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `assert_direct_candidate_producer`；`crates/winwincode-delivery/src/domain/evidence.rs:539`。
- `Ok → candidate.candidate_ref().into → candidate.candidate_ref → candidate.candidate_commit_id().into → candidate.candidate_commit_id → candidate.diff_sha256().into → candidate.diff_sha256 → resolve_direct_candidate_file → Err → resolution_error`；`crates/winwincode-delivery/src/domain/evidence.rs:546`。

**finding_sources 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `Vec::with_capacity → result.payload.findings.len`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:571`。
- `BTreeMap::new`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:572`。
- `HashSet::with_capacity → result.payload.findings.len`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:573`。
- `finding             .criterion_id             .ok_or_else → criterion_ids.insert → criterion_id.clone → Err → error → finding.evidence_sources.is_empty → Vec::with_capacity → finding.evidence_sources.len → exact_source_event → runtime_outcome → source.event_id.0.clone → evidence_type_order → evidenc…［展示截断；完整值见引用］`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:574`。
- `Ok → evidence_by_source.into_values().collect → evidence_by_source.into_values`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:661`。

**role_requirements 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `[         VerificationRole::Reviewer,         VerificationRole::Verifier,         VerificationRole::AdversarialVerifier,     ]     .into_iter()     .filter(|role| roles.contains(role))     .collect::&lt;Vec&lt;_&gt;&gt; → [         VerificationRole::Reviewer,         VerificationRole::Verifier,         Verifica…［展示截断；完整值见引用］`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:762`。
- `Err → error`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:770`。
- `Ok`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:783`。

**runtime_capture 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `terminal.product_session_id().clone → terminal.product_session_id → terminal.execution_job_id().clone → terminal.execution_job_id → terminal.worker_session_id().clone → terminal.worker_session_id → terminal.codex_thread_id().clone → terminal.codex_thread_id → terminal.work_run_id().clone → terminal.…［展示截断；完整值见引用］`；`crates/winwincode-delivery/src/domain/evidence.rs:164`。

**runtime_identity 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `fact.product_session_id.clone → fact.execution_job_id.clone → fact.work_run_id.clone → fact.role_id.clone → fact.lease_id.clone → fact.fencing_token.clone → fact.worker_id.clone → fact.worker_instance_id.clone → fact.worker_session_id.clone → fact.codex_thread_id.clone`；`crates/winwincode-delivery/src/domain/evidence.rs:922`。

**runtime_source 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `Err → resolution_error`；`crates/winwincode-delivery/src/domain/evidence.rs:754`。
- `portable_identifier(&amp;source_event_id.0, "evidence.sourceEventId").map_err → portable_identifier`；`crates/winwincode-delivery/src/domain/evidence.rs:760`。
- `validate_runtime_terminal`；`crates/winwincode-delivery/src/domain/evidence.rs:766`。
- `validate_checkout_attestation`；`crates/winwincode-delivery/src/domain/evidence.rs:773`。
- `accepted_sources         .iter()         .filter(|fact| fact.source_event_id == *source_event_id)         .collect → accepted_sources         .iter()         .filter → accepted_sources         .iter`；`crates/winwincode-delivery/src/domain/evidence.rs:774`。
- `matches.is_empty → Err → resolution_error`；`crates/winwincode-delivery/src/domain/evidence.rs:778`。
- `matches.len → Err → resolution_error`；`crates/winwincode-delivery/src/domain/evidence.rs:784`。
- `runtime_source_identity → Err → resolution_error`；`crates/winwincode-delivery/src/domain/evidence.rs:791`。
- `Err → resolution_error`；`crates/winwincode-delivery/src/domain/evidence.rs:797`。
- `candidate.candidate_ref → Err → resolution_error`；`crates/winwincode-delivery/src/domain/evidence.rs:803`。
- `validate_runtime_source_position`；`crates/winwincode-delivery/src/domain/evidence.rs:809`。
- `bounded_text(&amp;source_ref, "evidence.sourceRef", MAX_REFERENCE_LENGTH).map_err → bounded_text`；`crates/winwincode-delivery/src/domain/evidence.rs:817`。
- 后续步骤保留在 `/functional_chains/2/pattern/sequences/runtime_source`。

**runtime_terminal 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `binding         .worker_session_id         .as_ref()         .expect → binding         .worker_session_id         .as_ref`；`crates/winwincode-delivery/src/domain/evidence.rs:848`。
- `binding.codex_thread_id.as_ref().expect → binding.codex_thread_id.as_ref`；`crates/winwincode-delivery/src/domain/evidence.rs:852`。
- `terminal.product_session_id → terminal.execution_job_id → terminal.worker_session_id → terminal.codex_thread_id → terminal.work_run_id → terminal.attempt → u64::try_from(work_run.attempt).unwrap_or → u64::try_from → Err → resolution_error`；`crates/winwincode-delivery/src/domain/evidence.rs:853`。
- `terminal.terminal_candidate_tree_id → candidate.candidate_tree_id → Err → resolution_error`；`crates/winwincode-delivery/src/domain/evidence.rs:865`。
- `accepted_terminal_sequence`；`crates/winwincode-delivery/src/domain/evidence.rs:871`。
- `terminal.finished_at_millis → Err → resolution_error`；`crates/winwincode-delivery/src/domain/evidence.rs:872`。
- `Ok → terminal.product_session_id().clone → terminal.product_session_id → terminal.execution_job_id().clone → terminal.execution_job_id → terminal.work_run_id().clone → terminal.work_run_id → terminal.role_id().into → terminal.role_id → terminal.attempt → terminal.lease_id().clone → terminal.lease_id…［展示截断；完整值见引用］`；`crates/winwincode-delivery/src/domain/evidence.rs:883`。

**source_event_lookup 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `events         .iter()         .filter → events         .iter`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:668`。
- `matching         .next()         .ok_or_else → matching         .next`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:671`。
- `matching.next().is_some → matching.next → Err → error`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:674`。
- `Ok`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:679`。

**verdict_root 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `assert_frozen_candidate_current(delivery, &amp;candidate)         .map_err → assert_frozen_candidate_current`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:211`。
- `Vec::with_capacity → verification.len`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:213`。
- `Vec::new`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:214`。
- `HashSet::with_capacity → verification.len`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:215`。
- `candidate.producer_finished_at_millis`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:216`。
- `resolve_verification_runtime → roles.insert → Err → error → produced_at_millis.max → sessions.push → evidence.extend`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:218`。
- `required_roles`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:227`。
- `roles.len → required_roles.len → required_roles.iter().any → required_roles.iter → Err → error`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:228`。
- `sessions.sort_by_key`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:235`。
- `evidence.sort_by`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:236`。
- `evidence.dedup_by`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:237`。
- `validate_independent_verification(         delivery,         &amp;candidate,         &amp;VerificationFacts {             required_roles,             sessions,         },     )     .map_err → validate_independent_verification`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:238`。
- 后续步骤保留在 `/functional_chains/2/pattern/sequences/verdict_root`。

**verification_runtime 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `if runtime.read_only_candidate_source {         validated_git_snapshot_from_candidate(delivery, candidate, &amp;runtime.terminal)     } else {         validated_git_snapshot_from_source(delivery, &amp;runtime.source, &amp;runtime.terminal)     }     .map_err → validated_git_snapshot_from_candidate → validated_g…［展示截断；完整值见引用］`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:290`。
- `delivery         .snapshot()         .session_bindings         .iter()         .find(|binding| {             binding.execution_job_id == *verified_terminal.execution_job_id()                 &amp;&amp; binding.work_run_id == *verified_terminal.work_run_id()                 &amp;&amp; binding.attempt == verified_ter…［展示截断；完整值见引用］`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:297`。
- `if runtime.read_only_candidate_source {         AcceptedVerificationJobOutcomeFact::from_verified_read_only_outcome(             &amp;verified_terminal,             &amp;snapshot,             role.as_str(),         )     } else {         AcceptedVerificationJobOutcomeFact::from_verified_outcome(            …［展示截断；完整值见引用］`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:307`。
- `validated_runtime_events`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:321`。
- `validate_policy_attestation`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:322`。
- `structured_result`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:323`。
- `checkout_attestation_from_snapshot`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:324`。
- `resolve_findings`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:325`。
- `Ok → binding.work_run_id.clone → binding.id.clone → Some → snapshot.clone → Vec::new → verified_terminal.finished_at_millis`；`crates/winwincode-delivery/src/domain/candidate/verdict_authority.rs:335`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| scoped_source_supported | true | /functional_chains/2/pattern/scoped_source_supported |
| sequences/canonical_evidence/conditions | [] | /functional_chains/2/pattern/sequences/canonical_evidence/conditions |
| sequences/canonical_evidence/future_or_callback_activation_proven | false | /functional_chains/2/pattern/sequences/canonical_evidence/future_or_callback_activation_proven |
| sequences/canonical_evidence/orders/0/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/2/pattern/sequences/canonical_evidence/orders/0/conditions |
| sequences/canonical_evidence/orders/0/all_paths_reach_next_proven | false | /functional_chains/2/pattern/sequences/canonical_evidence/orders/0/all_paths_reach_next_proven |
| sequences/canonical_evidence/orders/1/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/2/pattern/sequences/canonical_evidence/orders/1/conditions |
| sequences/canonical_evidence/orders/1/all_paths_reach_next_proven | false | /functional_chains/2/pattern/sequences/canonical_evidence/orders/1/all_paths_reach_next_proven |
| sequences/canonical_evidence/orders/2/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/2/pattern/sequences/canonical_evidence/orders/2/conditions |
| sequences/canonical_evidence/orders/2/all_paths_reach_next_proven | false | /functional_chains/2/pattern/sequences/canonical_evidence/orders/2/all_paths_reach_next_proven |
| sequences/canonical_evidence/orders/3/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/2/pattern/sequences/canonical_evidence/orders/3/conditions |
| sequences/canonical_evidence/orders/3/all_paths_reach_next_proven | false | /functional_chains/2/pattern/sequences/canonical_evidence/orders/3/all_paths_reach_next_proven |
| sequences/canonical_evidence/orders/4/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/2/pattern/sequences/canonical_evidence/orders/4/conditions |
| sequences/canonical_evidence/orders/4/all_paths_reach_next_proven | false | /functional_chains/2/pattern/sequences/canonical_evidence/orders/4/all_paths_reach_next_proven |
| sequences/canonical_evidence/orders/5/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/2/pattern/sequences/canonical_evidence/orders/5/conditions |
| sequences/canonical_evidence/orders/5/all_paths_reach_next_proven | false | /functional_chains/2/pattern/sequences/canonical_evidence/orders/5/all_paths_reach_next_proven |
| sequences/canonical_evidence/steps/0/conditional_normal_reaching_only | true | /functional_chains/2/pattern/sequences/canonical_evidence/steps/0/conditional_normal_reaching_only |
| sequences/canonical_evidence/steps/1/conditional_normal_reaching_only | true | /functional_chains/2/pattern/sequences/canonical_evidence/steps/1/conditional_normal_reaching_only |
| sequences/canonical_evidence/steps/2/conditional_normal_reaching_only | true | /functional_chains/2/pattern/sequences/canonical_evidence/steps/2/conditional_normal_reaching_only |

所有事实及源位置：`/functional_chains/2/source_facts`；配置声明单列于 `/functional_chains/2/policy_declarations`，不作为自动证据。

### `wwc-document-device-provider-deployment-scope`

分析类型：`document_deployment_consistency`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/3`；保存发现：`1014da044f38227217dcb6b9`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| relation_witnesses/device_message_body_connects_local_store_to_model_callback_source | true | /functional_chains/3/pattern/relation_witnesses/device_message_body_connects_local_store_to_model_callback_source |
| relation_witnesses/local_execute_contains_selected_invoke_source | true | /functional_chains/3/pattern/relation_witnesses/local_execute_contains_selected_invoke_source |
| relation_witnesses/local_factory_reads_endpoint_and_constructs_provider_candidate | true | /functional_chains/3/pattern/relation_witnesses/local_factory_reads_endpoint_and_constructs_provider_candidate |
| relation_witnesses/local_resolver_passes_captured_byte_material_to_secret_constructor | true | /functional_chains/3/pattern/relation_witnesses/local_resolver_passes_captured_byte_material_to_secret_constructor |
| relation_witnesses/production_bootstrap_contains_selected_provider_installation_candidate | true | /functional_chains/3/pattern/relation_witnesses/production_bootstrap_contains_selected_provider_installation_candidate |
| relation_witnesses/resolved_config_and_secret_reach_same_local_provider_source | true | /functional_chains/3/pattern/relation_witnesses/resolved_config_and_secret_reach_same_local_provider_source |
| relation_witnesses/secret_container_constructs_owned_byte_material_source | true | /functional_chains/3/pattern/relation_witnesses/secret_container_constructs_owned_byte_material_source |
| relation_witnesses/selected_provider_method_exposes_secret_operand_source | true | /functional_chains/3/pattern/relation_witnesses/selected_provider_method_exposes_secret_operand_source |
| relation_witnesses/server_boundary_retains_unsupported_result_source | true | /functional_chains/3/pattern/relation_witnesses/server_boundary_retains_unsupported_result_source |
| relation_witnesses/worker_installs_captured_local_model_field | true | /functional_chains/3/pattern/relation_witnesses/worker_installs_captured_local_model_field |
| relation_witnesses/worker_local_consumer_guard_precedes_transport_fallback_source | true | /functional_chains/3/pattern/relation_witnesses/worker_local_consumer_guard_precedes_transport_fallback_source |
| comparison/statement | 所选文档描述 Control Plane 内部唯一模型路由及 Worker 仅经模型流；所选 Device 源码另有本地 provider 选择、字节 material 容器与调用来源，表述需要说明部署范围。 | /functional_chains/3/pattern/comparison/statement |
| comparison/classification | selected_document_wording_requires_device_deployment_qualification | /functional_chains/3/pattern/comparison/classification |
| comparison/actual_deployment_or_network_execution_verified | false | /functional_chains/3/pattern/comparison/actual_deployment_or_network_execution_verified |
| comparison/document_control_plane_internal_scope_preserved | true | /functional_chains/3/pattern/comparison/document_control_plane_internal_scope_preserved |
| comparison/global_project_exclusivity_inferred_from_document | false | /functional_chains/3/pattern/comparison/global_project_exclusivity_inferred_from_document |
| comparison/long_term_credential_exclusivity_refuted | unknown | /functional_chains/3/pattern/comparison/long_term_credential_exclusivity_refuted |
| comparison/public_delivery_or_contract_secret_leak_proven | false | /functional_chains/3/pattern/comparison/public_delivery_or_contract_secret_leak_proven |

所有事实及源位置：`/functional_chains/3/source_facts`；配置声明单列于 `/functional_chains/3/policy_declarations`，不作为自动证据。

### `wwc-report-adapter-durable-exact-turn`

分析类型：`guarded_call_sequence`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/4`；保存发现：`884dfadd2ea90efdd48367ed`。

**adapter_submit 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `self.run_key_for_thread(thread_id)?.to_owned → self.run_key_for_thread`；`crates/winwincode-codex/src/adapter.rs:3516`。
- `self.runs.get(&amp;run_key).ok_or_else → self.runs.get → stage_product_prompt(&amp;run.record.job).map_err → stage_product_prompt`；`crates/winwincode-codex/src/adapter.rs:3522`。
- `Err → conflict`；`crates/winwincode-codex/src/adapter.rs:3526`。
- `self.runs.get(&amp;run_key).ok_or_else → self.runs.get → turn_submission_options`；`crates/winwincode-codex/src/adapter.rs:3529`。
- `submission_input_digest`；`crates/winwincode-codex/src/adapter.rs:3533`。
- `self.runs.get_mut(&amp;run_key).ok_or_else → self.runs.get_mut → Err → conflict → Some → run.record.terminal.is_some → run.record.final_candidate_freeze.is_some → run.record.delegated_stop.is_some → run.record.batch_intent.is_some → run.record.format_repair.is_some → run.record.submission_id.clone`；`crates/winwincode-codex/src/adapter.rs:3534`。
- `self.persist_run`；`crates/winwincode-codex/src/adapter.rs:3558`。
- `Ok`；`crates/winwincode-codex/src/adapter.rs:3559`。
- `self.config.submission_faults.pop_front → Some → Err → ProductionCodexError::new`；`crates/winwincode-codex/src/adapter.rs:3563`。
- `self.session_for_thread`；`crates/winwincode-codex/src/adapter.rs:3571`。
- `self             .kernel             .reconcile_turn_exact → submission_id.clone → goal.to_owned`；`crates/winwincode-codex/src/adapter.rs:3572`。
- `self.retain_submission_failure → Err → kernel_error`；`crates/winwincode-codex/src/adapter.rs:3581`。
- 后续步骤保留在 `/functional_chains/4/pattern/sequences/adapter_submit`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| scoped_source_supported | true | /functional_chains/4/pattern/scoped_source_supported |
| sequences/adapter_submit/conditions/0/branch_context | [] | /functional_chains/4/pattern/sequences/adapter_submit/conditions/0/branch_context |
| sequences/adapter_submit/conditions/0/branches/0/abrupt_source_expressions/0/kind | return_expression | /functional_chains/4/pattern/sequences/adapter_submit/conditions/0/branches/0/abrupt_source_expressions/0/kind |
| sequences/adapter_submit/conditions/0/branches/0/abrupt_source_expressions/0/runtime_completion_proven | false | /functional_chains/4/pattern/sequences/adapter_submit/conditions/0/branches/0/abrupt_source_expressions/0/runtime_completion_proven |
| sequences/adapter_submit/conditions/0/branches/0/branch | then | /functional_chains/4/pattern/sequences/adapter_submit/conditions/0/branches/0/branch |
| sequences/adapter_submit/conditions/0/branches/0/branch_all_paths_abrupt_proven | true | /functional_chains/4/pattern/sequences/adapter_submit/conditions/0/branches/0/branch_all_paths_abrupt_proven |
| sequences/adapter_submit/conditions/0/branches/0/call_ids | ["43a51a519543ceb82084d385","a2237b6164fe497df9c8d625"] | /functional_chains/4/pattern/sequences/adapter_submit/conditions/0/branches/0/call_ids |
| sequences/adapter_submit/conditions/0/condition/kind | binary_expression | /functional_chains/4/pattern/sequences/adapter_submit/conditions/0/condition/kind |
| sequences/adapter_submit/conditions/0/condition/operands/0/kind | identifier | /functional_chains/4/pattern/sequences/adapter_submit/conditions/0/condition/operands/0/kind |
| sequences/adapter_submit/conditions/0/condition/operands/0/name | goal | /functional_chains/4/pattern/sequences/adapter_submit/conditions/0/condition/operands/0/name |
| sequences/adapter_submit/conditions/0/condition/operands/1/kind | identifier | /functional_chains/4/pattern/sequences/adapter_submit/conditions/0/condition/operands/1/kind |
| sequences/adapter_submit/conditions/0/condition/operands/1/name | expected_goal | /functional_chains/4/pattern/sequences/adapter_submit/conditions/0/condition/operands/1/name |
| sequences/adapter_submit/conditions/0/condition/operator | != | /functional_chains/4/pattern/sequences/adapter_submit/conditions/0/condition/operator |
| sequences/adapter_submit/conditions/0/condition/runtime_predicate_or_assignment_proven | false | /functional_chains/4/pattern/sequences/adapter_submit/conditions/0/condition/runtime_predicate_or_assignment_proven |
| sequences/adapter_submit/conditions/0/kind | source_guard_and_abrupt_branch | /functional_chains/4/pattern/sequences/adapter_submit/conditions/0/kind |
| sequences/adapter_submit/conditions/0/role | adapter_submit | /functional_chains/4/pattern/sequences/adapter_submit/conditions/0/role |
| sequences/adapter_submit/conditions/0/runtime_predicate_proven | false | /functional_chains/4/pattern/sequences/adapter_submit/conditions/0/runtime_predicate_proven |
| sequences/adapter_submit/conditions/1/branch_context | [] | /functional_chains/4/pattern/sequences/adapter_submit/conditions/1/branch_context |

所有事实及源位置：`/functional_chains/4/source_facts`；配置声明单列于 `/functional_chains/4/policy_declarations`，不作为自动证据。

### `wwc-report-chat-delivery-workrun-requests`

分析类型：`guarded_call_sequence`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/5`；保存发现：`16e57e77d5f8cc51ac46006c`。

**builder 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `clientFailure`；`apps/client/src/chat-delivery-creator.ts:168`。
- `input.title.trim`；`apps/client/src/chat-delivery-creator.ts:175`。
- `input.goal.trim`；`apps/client/src/chat-delivery-creator.ts:176`。
- `input.baseRevision.trim`；`apps/client/src/chat-delivery-creator.ts:177`。
- `Set → input.scope.map(value =&gt; value.trim()).filter → input.scope.map`；`apps/client/src/chat-delivery-creator.ts:178`。
- `Set → input.outOfScope.map(value =&gt; value.trim()).filter → input.outOfScope.map`；`apps/client/src/chat-delivery-creator.ts:179`。
- `Set → input.constraints.map(value =&gt; value.trim()).filter → input.constraints.map`；`apps/client/src/chat-delivery-creator.ts:180`。
- `input.acceptanceCriteria       .map(value =&gt; value.trim())       .filter → input.acceptanceCriteria       .map`；`apps/client/src/chat-delivery-creator.ts:181`。
- `invalid`；`apps/client/src/chat-delivery-creator.ts:184`。
- `invalid`；`apps/client/src/chat-delivery-creator.ts:188`。
- `invalid`；`apps/client/src/chat-delivery-creator.ts:192`。
- `invalid`；`apps/client/src/chat-delivery-creator.ts:196`。
- 后续步骤保留在 `/functional_chains/5/pattern/sequences/builder`。

**entry 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `create`；`apps/client/src/chat-delivery-creator.ts:331`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| scoped_source_supported | true | /functional_chains/5/pattern/scoped_source_supported |
| sequences/builder/conditions/0/branch_context | [] | /functional_chains/5/pattern/sequences/builder/conditions/0/branch_context |
| sequences/builder/conditions/0/branches/0/abrupt_source_expressions/0/kind | throw_statement | /functional_chains/5/pattern/sequences/builder/conditions/0/branches/0/abrupt_source_expressions/0/kind |
| sequences/builder/conditions/0/branches/0/abrupt_source_expressions/0/runtime_completion_proven | false | /functional_chains/5/pattern/sequences/builder/conditions/0/branches/0/abrupt_source_expressions/0/runtime_completion_proven |
| sequences/builder/conditions/0/branches/0/branch | then | /functional_chains/5/pattern/sequences/builder/conditions/0/branches/0/branch |
| sequences/builder/conditions/0/branches/0/branch_all_paths_abrupt_proven | true | /functional_chains/5/pattern/sequences/builder/conditions/0/branches/0/branch_all_paths_abrupt_proven |
| sequences/builder/conditions/0/branches/0/call_ids | ["3ed3aceda7f55985a4208d05"] | /functional_chains/5/pattern/sequences/builder/conditions/0/branches/0/call_ids |
| sequences/builder/conditions/0/condition/kind | identifier | /functional_chains/5/pattern/sequences/builder/conditions/0/condition/kind |
| sequences/builder/conditions/0/condition/name | closed | /functional_chains/5/pattern/sequences/builder/conditions/0/condition/name |
| sequences/builder/conditions/0/kind | source_guard_and_abrupt_branch | /functional_chains/5/pattern/sequences/builder/conditions/0/kind |
| sequences/builder/conditions/0/role | builder | /functional_chains/5/pattern/sequences/builder/conditions/0/role |
| sequences/builder/conditions/0/runtime_predicate_proven | false | /functional_chains/5/pattern/sequences/builder/conditions/0/runtime_predicate_proven |
| sequences/builder/conditions/1/branch_context | [] | /functional_chains/5/pattern/sequences/builder/conditions/1/branch_context |
| sequences/builder/conditions/1/branches/0/abrupt_source_expressions/0/kind | return_statement | /functional_chains/5/pattern/sequences/builder/conditions/1/branches/0/abrupt_source_expressions/0/kind |
| sequences/builder/conditions/1/branches/0/abrupt_source_expressions/0/runtime_completion_proven | false | /functional_chains/5/pattern/sequences/builder/conditions/1/branches/0/abrupt_source_expressions/0/runtime_completion_proven |
| sequences/builder/conditions/1/branches/0/branch | then | /functional_chains/5/pattern/sequences/builder/conditions/1/branches/0/branch |
| sequences/builder/conditions/1/branches/0/branch_all_paths_abrupt_proven | true | /functional_chains/5/pattern/sequences/builder/conditions/1/branches/0/branch_all_paths_abrupt_proven |
| sequences/builder/conditions/1/branches/0/call_ids | [] | /functional_chains/5/pattern/sequences/builder/conditions/1/branches/0/call_ids |

所有事实及源位置：`/functional_chains/5/source_facts`；配置声明单列于 `/functional_chains/5/policy_declarations`，不作为自动证据。

### `wwc-report-chat-retained-request-identities`

分析类型：`message_identity_relations`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/6`；保存发现：`be660f8d000a53b2df3bfe28`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| components/chat_request_identity/supported | true | /functional_chains/6/pattern/components/chat_request_identity/supported |
| components/chat_request_identity/builder_call_relations/0/supported | true | /functional_chains/6/pattern/components/chat_request_identity/builder_call_relations/0/supported |
| components/chat_request_identity/current_attempt_aliases/0/current_heap_alias_proven | false | /functional_chains/6/pattern/components/chat_request_identity/current_attempt_aliases/0/current_heap_alias_proven |
| components/chat_request_identity/delivery_projection/0/current_heap_alias_proven | false | /functional_chains/6/pattern/components/chat_request_identity/delivery_projection/0/current_heap_alias_proven |
| components/chat_request_identity/delivery_record_projections/0/record/fields/actor/expression/current_referent_value_proven | false | /functional_chains/6/pattern/components/chat_request_identity/delivery_record_projections/0/record/fields/actor/expression/current_referent_value_proven |
| components/chat_request_identity/delivery_record_projections/0/record/fields/requestId/expression/callee_source | options.nextRequestId | /functional_chains/6/pattern/components/chat_request_identity/delivery_record_projections/0/record/fields/requestId/expression/callee_source |
| components/chat_request_identity/delivery_record_projections/0/record/fields/requestId/expression/call_effects_or_result_proven | false | /functional_chains/6/pattern/components/chat_request_identity/delivery_record_projections/0/record/fields/requestId/expression/call_effects_or_result_proven |
| components/chat_request_identity/delivery_record_projections/0/record/fields/scope/expression/current_referent_value_proven | false | /functional_chains/6/pattern/components/chat_request_identity/delivery_record_projections/0/record/fields/scope/expression/current_referent_value_proven |
| components/chat_request_identity/delivery_record_projections/0/record/fields/workItemId/expression/runtime_value_proven | false | /functional_chains/6/pattern/components/chat_request_identity/delivery_record_projections/0/record/fields/workItemId/expression/runtime_value_proven |
| components/chat_request_identity/delivery_record_projections/0/record/runtime_record_value_proven | false | /functional_chains/6/pattern/components/chat_request_identity/delivery_record_projections/0/record/runtime_record_value_proven |
| components/chat_request_identity/delivery_record_projections/0/runtime_wire_identity_proven | false | /functional_chains/6/pattern/components/chat_request_identity/delivery_record_projections/0/runtime_wire_identity_proven |
| components/chat_request_identity/delivery_record_projections/1/record/fields/actor/expression/current_referent_value_proven | false | /functional_chains/6/pattern/components/chat_request_identity/delivery_record_projections/1/record/fields/actor/expression/current_referent_value_proven |
| components/chat_request_identity/delivery_record_projections/1/record/fields/contractRevision/expression/current_referent_value_proven | false | /functional_chains/6/pattern/components/chat_request_identity/delivery_record_projections/1/record/fields/contractRevision/expression/current_referent_value_proven |
| components/chat_request_identity/delivery_record_projections/1/record/fields/expectedRevision/expression/current_referent_value_proven | false | /functional_chains/6/pattern/components/chat_request_identity/delivery_record_projections/1/record/fields/expectedRevision/expression/current_referent_value_proven |
| components/chat_request_identity/delivery_record_projections/1/record/fields/items/expression/runtime_array_value_proven | false | /functional_chains/6/pattern/components/chat_request_identity/delivery_record_projections/1/record/fields/items/expression/runtime_array_value_proven |
| components/chat_request_identity/delivery_record_projections/1/record/fields/requestId/expression/callee_source | options.nextRequestId | /functional_chains/6/pattern/components/chat_request_identity/delivery_record_projections/1/record/fields/requestId/expression/callee_source |
| components/chat_request_identity/delivery_record_projections/1/record/fields/requestId/expression/call_effects_or_result_proven | false | /functional_chains/6/pattern/components/chat_request_identity/delivery_record_projections/1/record/fields/requestId/expression/call_effects_or_result_proven |
| components/chat_request_identity/delivery_record_projections/1/record/fields/scope/expression/current_referent_value_proven | false | /functional_chains/6/pattern/components/chat_request_identity/delivery_record_projections/1/record/fields/scope/expression/current_referent_value_proven |

所有事实及源位置：`/functional_chains/6/source_facts`；配置声明单列于 `/functional_chains/6/policy_declarations`，不作为自动证据。

### `wwc-report-device-provider-deployment`

分析类型：`deployment_provider_split`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/7`；保存发现：`f0600517dc7e144b07df96ba`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| boundary_results/0/expression/callee_source | Err | /functional_chains/7/pattern/boundary_results/0/expression/callee_source |
| boundary_results/0/expression/arguments/0/children/0/kind | scoped_identifier | /functional_chains/7/pattern/boundary_results/0/expression/arguments/0/children/0/kind |
| boundary_results/0/expression/arguments/0/children/0/source | winwincode_control_plane::DurableExecutionPortError | /functional_chains/7/pattern/boundary_results/0/expression/arguments/0/children/0/source |
| boundary_results/0/expression/arguments/0/children/1/kind | identifier | /functional_chains/7/pattern/boundary_results/0/expression/arguments/0/children/1/kind |
| boundary_results/0/expression/arguments/0/children/1/name | UnsupportedMessage | /functional_chains/7/pattern/boundary_results/0/expression/arguments/0/children/1/name |
| boundary_results/0/expression/arguments/0/kind | scoped_identifier | /functional_chains/7/pattern/boundary_results/0/expression/arguments/0/kind |
| boundary_results/0/expression/arguments/0/source | winwincode_control_plane::DurableExecutionPortError::UnsupportedMessage | /functional_chains/7/pattern/boundary_results/0/expression/arguments/0/source |
| boundary_results/0/expression/call_effects_or_result_proven | false | /functional_chains/7/pattern/boundary_results/0/expression/call_effects_or_result_proven |
| boundary_results/0/expression/callee_expression/kind | identifier | /functional_chains/7/pattern/boundary_results/0/expression/callee_expression/kind |
| boundary_results/0/expression/callee_expression/name | Err | /functional_chains/7/pattern/boundary_results/0/expression/callee_expression/name |
| boundary_results/0/expression/kind | call_expression | /functional_chains/7/pattern/boundary_results/0/expression/kind |
| boundary_results/0/kind | boundary_result_source | /functional_chains/7/pattern/boundary_results/0/kind |
| boundary_results/0/runtime_result_proven | false | /functional_chains/7/pattern/boundary_results/0/runtime_result_proven |
| deployments_or_provider_implementations_equivalent | false | /functional_chains/7/pattern/deployments_or_provider_implementations_equivalent |
| installation_assignments/0/left/current_referent_value_proven | false | /functional_chains/7/pattern/installation_assignments/0/left/current_referent_value_proven |
| installation_assignments/0/right/callee_source | Some | /functional_chains/7/pattern/installation_assignments/0/right/callee_source |
| installation_assignments/0/right/call_effects_or_result_proven | false | /functional_chains/7/pattern/installation_assignments/0/right/call_effects_or_result_proven |
| installation_assignments/0/runtime_installed_value_proven | false | /functional_chains/7/pattern/installation_assignments/0/runtime_installed_value_proven |

**保留的分析缺口**：

- `deployment_candidate_chain_not_global_dispatch_or_credential_availability`；完整位置与原因见 `/functional_chains/7/analysis_gaps`。

所有事实及源位置：`/functional_chains/7/source_facts`；配置声明单列于 `/functional_chains/7/policy_declarations`，不作为自动证据。

### `wwc-report-kernel-create-session-interface`

分析类型：`guarded_call_sequence`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/8`；保存发现：`196dfa3ccb808a6ae8466128`。

**kernel_create 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `Self::guard → self.runtime → Self::session_config → runtime                 .manager                 .start_thread(StartThreadOptions::new(config.clone()))                 .await                 .map_err → runtime                 .manager                 .start_thread → StartThreadOptions::new → con…［展示截断；完整值见引用］`；`crates/kernel/src/lib.rs:1221`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| nested_source_regions/0/conditions | ["this deferred captured body is activated and the recorded statements are reached normally"] | /functional_chains/8/pattern/nested_source_regions/0/conditions |
| nested_source_regions/0/body_activation_proven | false | /functional_chains/8/pattern/nested_source_regions/0/body_activation_proven |
| nested_source_regions/0/future_fulfillment_proven | false | /functional_chains/8/pattern/nested_source_regions/0/future_fulfillment_proven |
| nested_source_regions/0/sequence/conditions | [] | /functional_chains/8/pattern/nested_source_regions/0/sequence/conditions |
| nested_source_regions/0/sequence/future_or_callback_activation_proven | false | /functional_chains/8/pattern/nested_source_regions/0/sequence/future_or_callback_activation_proven |
| nested_source_regions/0/sequence/orders/0/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/8/pattern/nested_source_regions/0/sequence/orders/0/conditions |
| nested_source_regions/0/sequence/orders/0/all_paths_reach_next_proven | false | /functional_chains/8/pattern/nested_source_regions/0/sequence/orders/0/all_paths_reach_next_proven |
| nested_source_regions/0/sequence/orders/1/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/8/pattern/nested_source_regions/0/sequence/orders/1/conditions |
| nested_source_regions/0/sequence/orders/1/all_paths_reach_next_proven | false | /functional_chains/8/pattern/nested_source_regions/0/sequence/orders/1/all_paths_reach_next_proven |
| nested_source_regions/0/sequence/orders/2/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/8/pattern/nested_source_regions/0/sequence/orders/2/conditions |
| nested_source_regions/0/sequence/orders/2/all_paths_reach_next_proven | false | /functional_chains/8/pattern/nested_source_regions/0/sequence/orders/2/all_paths_reach_next_proven |
| nested_source_regions/0/sequence/steps/0/conditional_normal_reaching_only | true | /functional_chains/8/pattern/nested_source_regions/0/sequence/steps/0/conditional_normal_reaching_only |
| nested_source_regions/0/sequence/steps/1/conditional_normal_reaching_only | true | /functional_chains/8/pattern/nested_source_regions/0/sequence/steps/1/conditional_normal_reaching_only |
| nested_source_regions/0/sequence/steps/2/conditional_normal_reaching_only | true | /functional_chains/8/pattern/nested_source_regions/0/sequence/steps/2/conditional_normal_reaching_only |
| nested_source_regions/0/sequence/steps/3/conditional_normal_reaching_only | true | /functional_chains/8/pattern/nested_source_regions/0/sequence/steps/3/conditional_normal_reaching_only |
| scoped_source_supported | true | /functional_chains/8/pattern/scoped_source_supported |
| sequences/kernel_create/conditions | [] | /functional_chains/8/pattern/sequences/kernel_create/conditions |
| sequences/kernel_create/future_or_callback_activation_proven | false | /functional_chains/8/pattern/sequences/kernel_create/future_or_callback_activation_proven |

所有事实及源位置：`/functional_chains/8/source_facts`；配置声明单列于 `/functional_chains/8/policy_declarations`，不作为自动证据。

### `wwc-report-kernel-reconcile-exact-interface`

分析类型：`guarded_call_sequence`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/9`；保存发现：`913a6055ce2aac727cf43afc`。

**kernel_reconcile 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `Self::guard → turn_id.trim().is_empty → turn_id.trim → text.trim().is_empty → text.trim → Err → KernelFailure::new → self.runtime → self.session → self.enforce_private_permissions → session                 .thread                 .inspect_durable_turn(&amp;turn_id)                 .await                …［展示截断；完整值见引用］`；`crates/kernel/src/lib.rs:1376`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| nested_source_regions/0/conditions | ["this deferred captured body is activated and the recorded statements are reached normally"] | /functional_chains/9/pattern/nested_source_regions/0/conditions |
| nested_source_regions/0/body_activation_proven | false | /functional_chains/9/pattern/nested_source_regions/0/body_activation_proven |
| nested_source_regions/0/future_fulfillment_proven | false | /functional_chains/9/pattern/nested_source_regions/0/future_fulfillment_proven |
| nested_source_regions/0/sequence/conditions/0/branch_context | [] | /functional_chains/9/pattern/nested_source_regions/0/sequence/conditions/0/branch_context |
| nested_source_regions/0/sequence/conditions/0/branches/0/branch | then | /functional_chains/9/pattern/nested_source_regions/0/sequence/conditions/0/branches/0/branch |
| nested_source_regions/0/sequence/conditions/0/branches/0/branch_all_paths_abrupt_proven | true | /functional_chains/9/pattern/nested_source_regions/0/sequence/conditions/0/branches/0/branch_all_paths_abrupt_proven |
| nested_source_regions/0/sequence/conditions/0/branches/0/call_ids | ["e851bcede302eca805d5d6e5","f1aa03754675550611a1b6d6"] | /functional_chains/9/pattern/nested_source_regions/0/sequence/conditions/0/branches/0/call_ids |
| nested_source_regions/0/sequence/conditions/0/condition/kind | binary_expression | /functional_chains/9/pattern/nested_source_regions/0/sequence/conditions/0/condition/kind |
| nested_source_regions/0/sequence/conditions/0/condition/operands/0/callee_source | turn_id.trim().is_empty | /functional_chains/9/pattern/nested_source_regions/0/sequence/conditions/0/condition/operands/0/callee_source |
| nested_source_regions/0/sequence/conditions/0/condition/operands/0/arguments | [] | /functional_chains/9/pattern/nested_source_regions/0/sequence/conditions/0/condition/operands/0/arguments |
| nested_source_regions/0/sequence/conditions/0/condition/operands/0/call_effects_or_result_proven | false | /functional_chains/9/pattern/nested_source_regions/0/sequence/conditions/0/condition/operands/0/call_effects_or_result_proven |
| nested_source_regions/0/sequence/conditions/0/condition/operands/0/kind | call_expression | /functional_chains/9/pattern/nested_source_regions/0/sequence/conditions/0/condition/operands/0/kind |
| nested_source_regions/0/sequence/conditions/0/condition/operands/1/callee_source | text.trim().is_empty | /functional_chains/9/pattern/nested_source_regions/0/sequence/conditions/0/condition/operands/1/callee_source |
| nested_source_regions/0/sequence/conditions/0/condition/operands/1/arguments | [] | /functional_chains/9/pattern/nested_source_regions/0/sequence/conditions/0/condition/operands/1/arguments |
| nested_source_regions/0/sequence/conditions/0/condition/operands/1/call_effects_or_result_proven | false | /functional_chains/9/pattern/nested_source_regions/0/sequence/conditions/0/condition/operands/1/call_effects_or_result_proven |
| nested_source_regions/0/sequence/conditions/0/condition/operands/1/kind | call_expression | /functional_chains/9/pattern/nested_source_regions/0/sequence/conditions/0/condition/operands/1/kind |
| nested_source_regions/0/sequence/conditions/0/condition/operator | \|\| | /functional_chains/9/pattern/nested_source_regions/0/sequence/conditions/0/condition/operator |
| nested_source_regions/0/sequence/conditions/0/condition/runtime_predicate_or_assignment_proven | false | /functional_chains/9/pattern/nested_source_regions/0/sequence/conditions/0/condition/runtime_predicate_or_assignment_proven |

所有事实及源位置：`/functional_chains/9/source_facts`；配置声明单列于 `/functional_chains/9/policy_declarations`，不作为自动证据。

### `wwc-report-kernel-submit-turn-interface`

分析类型：`guarded_call_sequence`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/10`；保存发现：`cb2d5f3a570ce0c9da78a1af`。

**kernel_submit 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `Self::guard → text.trim().is_empty → text.trim → Err → KernelFailure::new → self.runtime → self.session → self.enforce_private_permissions → session                 .thread                 .start_or_steer_turn(user_text_request(text, &amp;options))                 .await                 .map_err → sessi…［展示截断；完整值见引用］`；`crates/kernel/src/lib.rs:1339`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| nested_source_regions/0/conditions | ["this deferred captured body is activated and the recorded statements are reached normally"] | /functional_chains/10/pattern/nested_source_regions/0/conditions |
| nested_source_regions/0/body_activation_proven | false | /functional_chains/10/pattern/nested_source_regions/0/body_activation_proven |
| nested_source_regions/0/future_fulfillment_proven | false | /functional_chains/10/pattern/nested_source_regions/0/future_fulfillment_proven |
| nested_source_regions/0/sequence/conditions/0/branch_context | [] | /functional_chains/10/pattern/nested_source_regions/0/sequence/conditions/0/branch_context |
| nested_source_regions/0/sequence/conditions/0/branches/0/branch | then | /functional_chains/10/pattern/nested_source_regions/0/sequence/conditions/0/branches/0/branch |
| nested_source_regions/0/sequence/conditions/0/branches/0/branch_all_paths_abrupt_proven | true | /functional_chains/10/pattern/nested_source_regions/0/sequence/conditions/0/branches/0/branch_all_paths_abrupt_proven |
| nested_source_regions/0/sequence/conditions/0/branches/0/call_ids | ["e32e3b31b4ffedd76f25d394","51f254793fdb5162872bb911"] | /functional_chains/10/pattern/nested_source_regions/0/sequence/conditions/0/branches/0/call_ids |
| nested_source_regions/0/sequence/conditions/0/condition/callee_source | text.trim().is_empty | /functional_chains/10/pattern/nested_source_regions/0/sequence/conditions/0/condition/callee_source |
| nested_source_regions/0/sequence/conditions/0/condition/arguments | [] | /functional_chains/10/pattern/nested_source_regions/0/sequence/conditions/0/condition/arguments |
| nested_source_regions/0/sequence/conditions/0/condition/call_effects_or_result_proven | false | /functional_chains/10/pattern/nested_source_regions/0/sequence/conditions/0/condition/call_effects_or_result_proven |
| nested_source_regions/0/sequence/conditions/0/condition/callee_expression/current_referent_value_proven | false | /functional_chains/10/pattern/nested_source_regions/0/sequence/conditions/0/condition/callee_expression/current_referent_value_proven |
| nested_source_regions/0/sequence/conditions/0/condition/callee_expression/kind | field_expression | /functional_chains/10/pattern/nested_source_regions/0/sequence/conditions/0/condition/callee_expression/kind |
| nested_source_regions/0/sequence/conditions/0/condition/callee_expression/member | is_empty | /functional_chains/10/pattern/nested_source_regions/0/sequence/conditions/0/condition/callee_expression/member |
| nested_source_regions/0/sequence/conditions/0/condition/callee_expression/member_location/column | 28 | /functional_chains/10/pattern/nested_source_regions/0/sequence/conditions/0/condition/callee_expression/member_location/column |
| nested_source_regions/0/sequence/conditions/0/condition/callee_expression/member_location/column_base | 1 | /functional_chains/10/pattern/nested_source_regions/0/sequence/conditions/0/condition/callee_expression/member_location/column_base |
| nested_source_regions/0/sequence/conditions/0/condition/callee_expression/member_location/column_unit | utf8_bytes | /functional_chains/10/pattern/nested_source_regions/0/sequence/conditions/0/condition/callee_expression/member_location/column_unit |
| nested_source_regions/0/sequence/conditions/0/condition/callee_expression/member_location/coordinate_space | captured_text_utf8 | /functional_chains/10/pattern/nested_source_regions/0/sequence/conditions/0/condition/callee_expression/member_location/coordinate_space |
| nested_source_regions/0/sequence/conditions/0/condition/callee_expression/member_location/end_byte | 49165 | /functional_chains/10/pattern/nested_source_regions/0/sequence/conditions/0/condition/callee_expression/member_location/end_byte |

所有事实及源位置：`/functional_chains/10/source_facts`；配置声明单列于 `/functional_chains/10/policy_declarations`，不作为自动证据。

### `wwc-report-outbox-ack-correlation-fields`

分析类型：`message_identity_relations`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/11`；保存发现：`f2a949272f560b9d0dfb5e46`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| components/outbox_ack_correlation/supported | true | /functional_chains/11/pattern/components/outbox_ack_correlation/supported |
| components/outbox_ack_correlation/ack_gate_sources/0/branch_context/0/condition/kind | unary_expression | /functional_chains/11/pattern/components/outbox_ack_correlation/ack_gate_sources/0/branch_context/0/condition/kind |
| components/outbox_ack_correlation/ack_gate_sources/0/branch_context/0/condition/operator | ! | /functional_chains/11/pattern/components/outbox_ack_correlation/ack_gate_sources/0/branch_context/0/condition/operator |
| components/outbox_ack_correlation/ack_gate_sources/0/branch_context/0/condition/runtime_predicate_or_assignment_proven | false | /functional_chains/11/pattern/components/outbox_ack_correlation/ack_gate_sources/0/branch_context/0/condition/runtime_predicate_or_assignment_proven |
| components/outbox_ack_correlation/ack_gate_sources/0/branch_context/0/condition_truth_proven | false | /functional_chains/11/pattern/components/outbox_ack_correlation/ack_gate_sources/0/branch_context/0/condition_truth_proven |
| components/outbox_ack_correlation/ack_gate_sources/0/caller_supplied_domain_validation_independently_proven | false | /functional_chains/11/pattern/components/outbox_ack_correlation/ack_gate_sources/0/caller_supplied_domain_validation_independently_proven |
| components/outbox_ack_correlation/ack_gate_sources/1/caller_supplied_domain_validation_independently_proven | false | /functional_chains/11/pattern/components/outbox_ack_correlation/ack_gate_sources/1/caller_supplied_domain_validation_independently_proven |
| components/outbox_ack_correlation/ack_return_tuple_sql_bindings/0/supported | true | /functional_chains/11/pattern/components/outbox_ack_correlation/ack_return_tuple_sql_bindings/0/supported |
| components/outbox_ack_correlation/ack_return_tuple_sql_bindings/0/value_or_database_effect_proven | false | /functional_chains/11/pattern/components/outbox_ack_correlation/ack_return_tuple_sql_bindings/0/value_or_database_effect_proven |
| components/outbox_ack_correlation/correlation_codec_sources/0/callee_source | serde_json::to_vec | /functional_chains/11/pattern/components/outbox_ack_correlation/correlation_codec_sources/0/callee_source |
| components/outbox_ack_correlation/correlation_codec_sources/0/codec_runtime_or_digest_collision_proven | false | /functional_chains/11/pattern/components/outbox_ack_correlation/correlation_codec_sources/0/codec_runtime_or_digest_collision_proven |
| components/outbox_ack_correlation/correlation_codec_sources/1/callee_source | digest | /functional_chains/11/pattern/components/outbox_ack_correlation/correlation_codec_sources/1/callee_source |
| components/outbox_ack_correlation/correlation_codec_sources/1/codec_runtime_or_digest_collision_proven | false | /functional_chains/11/pattern/components/outbox_ack_correlation/correlation_codec_sources/1/codec_runtime_or_digest_collision_proven |
| components/outbox_ack_correlation/external_ack_truth_or_exactly_once_proven | false | /functional_chains/11/pattern/components/outbox_ack_correlation/external_ack_truth_or_exactly_once_proven |
| components/outbox_ack_correlation/frame_metadata_sql_insert_joins/0/supported | true | /functional_chains/11/pattern/components/outbox_ack_correlation/frame_metadata_sql_insert_joins/0/supported |
| components/outbox_ack_correlation/frame_metadata_sql_insert_joins/0/metadata_helper_relation/supported | true | /functional_chains/11/pattern/components/outbox_ack_correlation/frame_metadata_sql_insert_joins/0/metadata_helper_relation/supported |
| components/outbox_ack_correlation/frame_metadata_sql_insert_joins/0/metadata_helper_relation/macro_expansion_or_runtime_activation_proven | false | /functional_chains/11/pattern/components/outbox_ack_correlation/frame_metadata_sql_insert_joins/0/metadata_helper_relation/macro_expansion_or_runtime_activation_proven |
| components/outbox_ack_correlation/frame_metadata_sql_insert_joins/0/stored_bytes_or_physical_transaction_success_proven | false | /functional_chains/11/pattern/components/outbox_ack_correlation/frame_metadata_sql_insert_joins/0/stored_bytes_or_physical_transaction_success_proven |

所有事实及源位置：`/functional_chains/11/source_facts`；配置声明单列于 `/functional_chains/11/policy_declarations`，不作为自动证据。

### `wwc-report-production-adapter-embedded-kernel`

分析类型：`guarded_call_sequence`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/12`；保存发现：`3ad1a2c3498a4a08ddb2bcaf`。

**adapter_open 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `ensure_private_directory(&amp;config.data_directory).map_err → ensure_private_directory`；`crates/winwincode-codex/src/adapter.rs:418`。
- `ensure_private_directory(&amp;config.kernel_home).map_err → ensure_private_directory`；`crates/winwincode-codex/src/adapter.rs:419`。
- `seal_helper → Some → config.helper_bytes.as_ref`；`crates/winwincode-codex/src/adapter.rs:420`。
- `WorkerCapabilityCatalog::discover(             &amp;config.registered_capabilities,             config.discovered_capabilities.clone(),         )         .map_err → WorkerCapabilityCatalog::discover → config.discovered_capabilities.clone`；`crates/winwincode-codex/src/adapter.rs:426`。
- `AdapterStore::open(&amp;config.data_directory).map_err → AdapterStore::open`；`crates/winwincode-codex/src/adapter.rs:431`。
- `migrate_stored_run_role_policies_v1_to_v2`；`crates/winwincode-codex/src/adapter.rs:432`。
- `ExecutionOutbox::open(store.clone()).map_err → ExecutionOutbox::open → store.clone`；`crates/winwincode-codex/src/adapter.rs:433`。
- `CandidateArtifactOutbox::open(store.clone()).map_err → CandidateArtifactOutbox::open → store.clone`；`crates/winwincode-codex/src/adapter.rs:434`。
- `DiagnosticArtifactOutbox::open(store.clone()).map_err → DiagnosticArtifactOutbox::open → store.clone`；`crates/winwincode-codex/src/adapter.rs:436`。
- `SharedAuthoritySource::default`；`crates/winwincode-codex/src/adapter.rs:438`。
- `Arc::new → ExecutionPortModelBridge::new → store.clone → outbox.clone → config.gateway_route.clone → config.provider.clone`；`crates/winwincode-codex/src/adapter.rs:439`。
- `Arc::new → ExecutionPortActionGate::open(                 &amp;config.data_directory,                 capability_catalog.clone(),                 config.execution_envelope.clone(),                 config.action_signing_key.clone(),             )             .map_err → ExecutionPortActionGate::open → cap…［展示截断；完整值见引用］`；`crates/winwincode-codex/src/adapter.rs:446`。
- 后续步骤保留在 `/functional_chains/12/pattern/sequences/adapter_open`。

**kernel_constructor 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `options.home.is_absolute → Err → KernelFailure::new`；`crates/kernel/src/lib.rs:830`。
- `options.helper_executable.is_absolute → Err → KernelFailure::new`；`crates/kernel/src/lib.rs:836`。
- `std::fs::symlink_metadata(&amp;options.helper_executable).map_err → std::fs::symlink_metadata`；`crates/kernel/src/lib.rs:845`。
- `helper_metadata.file_type().is_symlink → helper_metadata.file_type → helper_metadata.is_file → Err → KernelFailure::new`；`crates/kernel/src/lib.rs:855`。
- `helper_metadata.permissions().mode → helper_metadata.permissions → Err → KernelFailure::new`；`crates/kernel/src/lib.rs:865`。
- `options             .event_capacity             .clamp`；`crates/kernel/src/lib.rs:874`。
- `options.shutdown_timeout.is_zero → Err → KernelFailure::new`；`crates/kernel/src/lib.rs:877`。
- `std::fs::create_dir_all(&amp;options.home).map_err → std::fs::create_dir_all`；`crates/kernel/src/lib.rs:883`。
- `restrict_private_tree(&amp;options.home).map_err → restrict_private_tree`；`crates/kernel/src/lib.rs:889`。
- `Ok → Arc::new → Mutex::new → AtomicBool::new`；`crates/kernel/src/lib.rs:895`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| scoped_source_supported | true | /functional_chains/12/pattern/scoped_source_supported |
| sequences/adapter_open/conditions | [] | /functional_chains/12/pattern/sequences/adapter_open/conditions |
| sequences/adapter_open/assignment_attempts/0/left/current_referent_value_proven | false | /functional_chains/12/pattern/sequences/adapter_open/assignment_attempts/0/left/current_referent_value_proven |
| sequences/adapter_open/assignment_attempts/0/right/operand/callee_source | seal_helper | /functional_chains/12/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/callee_source |
| sequences/adapter_open/assignment_attempts/0/right/operand/arguments/1/callee_source | Some | /functional_chains/12/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/1/callee_source |
| sequences/adapter_open/assignment_attempts/0/right/operand/arguments/1/call_effects_or_result_proven | false | /functional_chains/12/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/1/call_effects_or_result_proven |
| sequences/adapter_open/assignment_attempts/0/right/operand/call_effects_or_result_proven | false | /functional_chains/12/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/call_effects_or_result_proven |
| sequences/adapter_open/assignment_attempts/0/write_runtime_success_proven | false | /functional_chains/12/pattern/sequences/adapter_open/assignment_attempts/0/write_runtime_success_proven |
| sequences/adapter_open/future_or_callback_activation_proven | false | /functional_chains/12/pattern/sequences/adapter_open/future_or_callback_activation_proven |
| sequences/adapter_open/orders/0/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/12/pattern/sequences/adapter_open/orders/0/conditions |
| sequences/adapter_open/orders/0/all_paths_reach_next_proven | false | /functional_chains/12/pattern/sequences/adapter_open/orders/0/all_paths_reach_next_proven |
| sequences/adapter_open/orders/1/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/12/pattern/sequences/adapter_open/orders/1/conditions |
| sequences/adapter_open/orders/1/all_paths_reach_next_proven | false | /functional_chains/12/pattern/sequences/adapter_open/orders/1/all_paths_reach_next_proven |
| sequences/adapter_open/orders/2/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/12/pattern/sequences/adapter_open/orders/2/conditions |
| sequences/adapter_open/orders/2/all_paths_reach_next_proven | false | /functional_chains/12/pattern/sequences/adapter_open/orders/2/all_paths_reach_next_proven |
| sequences/adapter_open/orders/3/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/12/pattern/sequences/adapter_open/orders/3/conditions |
| sequences/adapter_open/orders/3/all_paths_reach_next_proven | false | /functional_chains/12/pattern/sequences/adapter_open/orders/3/all_paths_reach_next_proven |
| sequences/adapter_open/orders/4/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/12/pattern/sequences/adapter_open/orders/4/conditions |

所有事实及源位置：`/functional_chains/12/source_facts`；配置声明单列于 `/functional_chains/12/policy_declarations`，不作为自动证据。

### `wwc-report-submission-intent-kernel-order`

分析类型：`guarded_call_sequence`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/13`；保存发现：`719c7a3c938f4606d84cb1c9`。

**submission 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `self.run_key_for_thread(thread_id)?.to_owned → self.run_key_for_thread`；`crates/winwincode-codex/src/adapter.rs:3516`。
- `self.runs.get(&amp;run_key).ok_or_else → self.runs.get → stage_product_prompt(&amp;run.record.job).map_err → stage_product_prompt`；`crates/winwincode-codex/src/adapter.rs:3522`。
- `Err → conflict`；`crates/winwincode-codex/src/adapter.rs:3526`。
- `self.runs.get(&amp;run_key).ok_or_else → self.runs.get → turn_submission_options`；`crates/winwincode-codex/src/adapter.rs:3529`。
- `submission_input_digest`；`crates/winwincode-codex/src/adapter.rs:3533`。
- `self.runs.get_mut(&amp;run_key).ok_or_else → self.runs.get_mut → Err → conflict → Some → run.record.terminal.is_some → run.record.final_candidate_freeze.is_some → run.record.delegated_stop.is_some → run.record.batch_intent.is_some → run.record.format_repair.is_some → run.record.submission_id.clone`；`crates/winwincode-codex/src/adapter.rs:3534`。
- `self.persist_run`；`crates/winwincode-codex/src/adapter.rs:3558`。
- `Ok`；`crates/winwincode-codex/src/adapter.rs:3559`。
- `self.config.submission_faults.pop_front → Some → Err → ProductionCodexError::new`；`crates/winwincode-codex/src/adapter.rs:3563`。
- `self.session_for_thread`；`crates/winwincode-codex/src/adapter.rs:3571`。
- `self             .kernel             .reconcile_turn_exact → submission_id.clone → goal.to_owned`；`crates/winwincode-codex/src/adapter.rs:3572`。
- `self.retain_submission_failure → Err → kernel_error`；`crates/winwincode-codex/src/adapter.rs:3581`。
- 后续步骤保留在 `/functional_chains/13/pattern/sequences/submission`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| scoped_source_supported | true | /functional_chains/13/pattern/scoped_source_supported |
| sequences/submission/conditions/0/branch_context | [] | /functional_chains/13/pattern/sequences/submission/conditions/0/branch_context |
| sequences/submission/conditions/0/branches/0/abrupt_source_expressions/0/kind | return_expression | /functional_chains/13/pattern/sequences/submission/conditions/0/branches/0/abrupt_source_expressions/0/kind |
| sequences/submission/conditions/0/branches/0/abrupt_source_expressions/0/runtime_completion_proven | false | /functional_chains/13/pattern/sequences/submission/conditions/0/branches/0/abrupt_source_expressions/0/runtime_completion_proven |
| sequences/submission/conditions/0/branches/0/branch | then | /functional_chains/13/pattern/sequences/submission/conditions/0/branches/0/branch |
| sequences/submission/conditions/0/branches/0/branch_all_paths_abrupt_proven | true | /functional_chains/13/pattern/sequences/submission/conditions/0/branches/0/branch_all_paths_abrupt_proven |
| sequences/submission/conditions/0/branches/0/call_ids | ["96a7a648199bfb3702861465","36054756d00091e4a0c692ee"] | /functional_chains/13/pattern/sequences/submission/conditions/0/branches/0/call_ids |
| sequences/submission/conditions/0/condition/kind | binary_expression | /functional_chains/13/pattern/sequences/submission/conditions/0/condition/kind |
| sequences/submission/conditions/0/condition/operands/0/kind | identifier | /functional_chains/13/pattern/sequences/submission/conditions/0/condition/operands/0/kind |
| sequences/submission/conditions/0/condition/operands/0/name | goal | /functional_chains/13/pattern/sequences/submission/conditions/0/condition/operands/0/name |
| sequences/submission/conditions/0/condition/operands/1/kind | identifier | /functional_chains/13/pattern/sequences/submission/conditions/0/condition/operands/1/kind |
| sequences/submission/conditions/0/condition/operands/1/name | expected_goal | /functional_chains/13/pattern/sequences/submission/conditions/0/condition/operands/1/name |
| sequences/submission/conditions/0/condition/operator | != | /functional_chains/13/pattern/sequences/submission/conditions/0/condition/operator |
| sequences/submission/conditions/0/condition/runtime_predicate_or_assignment_proven | false | /functional_chains/13/pattern/sequences/submission/conditions/0/condition/runtime_predicate_or_assignment_proven |
| sequences/submission/conditions/0/kind | source_guard_and_abrupt_branch | /functional_chains/13/pattern/sequences/submission/conditions/0/kind |
| sequences/submission/conditions/0/role | submission | /functional_chains/13/pattern/sequences/submission/conditions/0/role |
| sequences/submission/conditions/0/runtime_predicate_proven | false | /functional_chains/13/pattern/sequences/submission/conditions/0/runtime_predicate_proven |
| sequences/submission/conditions/1/branch_context | [] | /functional_chains/13/pattern/sequences/submission/conditions/1/branch_context |

所有事实及源位置：`/functional_chains/13/source_facts`；配置声明单列于 `/functional_chains/13/policy_declarations`，不作为自动证据。

### `wwc-report-worker-adapter-record-identities`

分析类型：`message_identity_relations`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/14`；保存发现：`54aa478e9d99f2659cc0022c`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| components/worker_adapter_identity/supported | true | /functional_chains/14/pattern/components/worker_adapter_identity/supported |
| components/worker_adapter_identity/authority_and_result_values_proven | false | /functional_chains/14/pattern/components/worker_adapter_identity/authority_and_result_values_proven |
| components/worker_adapter_identity/components/adapter_ensure_thread/supported | true | /functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/supported |
| components/worker_adapter_identity/components/adapter_ensure_thread/interface_arguments/0/callee_source | production_agent_session_config | /functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/interface_arguments/0/callee_source |
| components/worker_adapter_identity/components/adapter_ensure_thread/interface_arguments/0/runtime_dispatch_proven | false | /functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/interface_arguments/0/runtime_dispatch_proven |
| components/worker_adapter_identity/components/adapter_ensure_thread/interface_arguments/1/callee_source | self<br>            .kernel<br>            .create_session | /functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/interface_arguments/1/callee_source |
| components/worker_adapter_identity/components/adapter_ensure_thread/interface_arguments/1/runtime_dispatch_proven | false | /functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/interface_arguments/1/runtime_dispatch_proven |
| components/worker_adapter_identity/components/adapter_ensure_thread/interface_arguments/2/callee_source | self.store<br>            .save_run | /functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/interface_arguments/2/callee_source |
| components/worker_adapter_identity/components/adapter_ensure_thread/interface_arguments/2/runtime_dispatch_proven | false | /functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/interface_arguments/2/runtime_dispatch_proven |
| components/worker_adapter_identity/components/adapter_persist/supported | true | /functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_persist/supported |
| components/worker_adapter_identity/components/adapter_persist/interface_arguments/0/callee_source | self.store<br>            .save_run | /functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_persist/interface_arguments/0/callee_source |
| components/worker_adapter_identity/components/adapter_persist/interface_arguments/0/runtime_dispatch_proven | false | /functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_persist/interface_arguments/0/runtime_dispatch_proven |
| components/worker_adapter_identity/components/adapter_profile/supported | true | /functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_profile/supported |
| components/worker_adapter_identity/components/adapter_profile/interface_arguments/0/callee_source | resolve_agent_session_config | /functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_profile/interface_arguments/0/callee_source |
| components/worker_adapter_identity/components/adapter_profile/interface_arguments/0/runtime_dispatch_proven | false | /functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_profile/interface_arguments/0/runtime_dispatch_proven |
| components/worker_adapter_identity/components/adapter_session_for_thread/supported | true | /functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_session_for_thread/supported |
| components/worker_adapter_identity/components/adapter_session_for_thread/deferred_callback_projections/0/callback_activation_proven | false | /functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_session_for_thread/deferred_callback_projections/0/callback_activation_proven |
| components/worker_adapter_identity/components/adapter_session_for_thread/interface_arguments/0/callee_source | self.run_key_for_thread | /functional_chains/14/pattern/components/worker_adapter_identity/components/adapter_session_for_thread/interface_arguments/0/callee_source |

所有事实及源位置：`/functional_chains/14/source_facts`；配置声明单列于 `/functional_chains/14/policy_declarations`，不作为自动证据。

### `wwc-report-worker-bootstrap-entries`

分析类型：`guarded_call_sequence`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/15`；保存发现：`31ff1b2904390c31587a11f1`。

**entry 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `env::args().skip → env::args`；`crates/winwincode-worker/src/main.rs:35`。
- `args.next().as_deref → args.next → print_identity → args.next().is_none → run_worker_process → run_remote → run_managed → usage_error`；`crates/winwincode-worker/src/main.rs:36`。

**managed 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `ManagedSessionConfig::read → std::path::Path::new`；`crates/winwincode-worker/src/main.rs:119`。
- `WorkerSessionCredential::load`；`crates/winwincode-worker/src/main.rs:120`。
- `Box::pin → run_worker → config.worker_id.clone → config.worker_instance_id.clone → now_instant → config.data_directory.clone → config.provider_directory.clone → config.source_directory.clone → config.server_origin.clone → credential.path().to_path_buf → credential.path → config             .model_ro…［展示截断；完整值见引用］`；`crates/winwincode-worker/src/main.rs:133`。

**remote 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `WorkerId → required → WorkerInstanceId → env::var("WWC_WORKER_STARTED_AT").map_or → env::var → now_instant → PathBuf::from → default_model_route`；`crates/winwincode-worker/src/main.rs:98`。
- `Box::pin → run_worker`；`crates/winwincode-worker/src/main.rs:110`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| scoped_source_supported | true | /functional_chains/15/pattern/scoped_source_supported |
| sequences/entry/conditions | [] | /functional_chains/15/pattern/sequences/entry/conditions |
| sequences/entry/future_or_callback_activation_proven | false | /functional_chains/15/pattern/sequences/entry/future_or_callback_activation_proven |
| sequences/entry/orders/0/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/15/pattern/sequences/entry/orders/0/conditions |
| sequences/entry/orders/0/all_paths_reach_next_proven | false | /functional_chains/15/pattern/sequences/entry/orders/0/all_paths_reach_next_proven |
| sequences/entry/steps/0/conditional_normal_reaching_only | true | /functional_chains/15/pattern/sequences/entry/steps/0/conditional_normal_reaching_only |
| sequences/entry/steps/1/conditional_normal_reaching_only | true | /functional_chains/15/pattern/sequences/entry/steps/1/conditional_normal_reaching_only |
| sequences/managed/conditions | [] | /functional_chains/15/pattern/sequences/managed/conditions |
| sequences/managed/future_or_callback_activation_proven | false | /functional_chains/15/pattern/sequences/managed/future_or_callback_activation_proven |
| sequences/managed/orders/0/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/15/pattern/sequences/managed/orders/0/conditions |
| sequences/managed/orders/0/all_paths_reach_next_proven | false | /functional_chains/15/pattern/sequences/managed/orders/0/all_paths_reach_next_proven |
| sequences/managed/orders/1/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/15/pattern/sequences/managed/orders/1/conditions |
| sequences/managed/orders/1/all_paths_reach_next_proven | false | /functional_chains/15/pattern/sequences/managed/orders/1/all_paths_reach_next_proven |
| sequences/managed/steps/0/conditional_normal_reaching_only | true | /functional_chains/15/pattern/sequences/managed/steps/0/conditional_normal_reaching_only |
| sequences/managed/steps/1/conditional_normal_reaching_only | true | /functional_chains/15/pattern/sequences/managed/steps/1/conditional_normal_reaching_only |
| sequences/managed/steps/2/conditional_normal_reaching_only | true | /functional_chains/15/pattern/sequences/managed/steps/2/conditional_normal_reaching_only |
| sequences/remote/conditions | [] | /functional_chains/15/pattern/sequences/remote/conditions |
| sequences/remote/future_or_callback_activation_proven | false | /functional_chains/15/pattern/sequences/remote/future_or_callback_activation_proven |

所有事实及源位置：`/functional_chains/15/source_facts`；配置声明单列于 `/functional_chains/15/policy_declarations`，不作为自动证据。

### `wwc-report-worker-production-construction`

分析类型：`guarded_call_sequence`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/16`；保存发现：`592af9e5752f7a582d46b025`。

**adapter_factory 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `HelperReleaseManifest::from_file → PathBuf::from → required`；`crates/winwincode-worker/src/main.rs:323`。
- `winwincode_provider::DeviceProviderStore::open`；`crates/winwincode-worker/src/main.rs:326`。
- `store.snapshot`；`crates/winwincode-worker/src/main.rs:327`。
- `store.restore_extensions → data_directory.join`；`crates/winwincode-worker/src/main.rs:328`。
- `Vec::new`；`crates/winwincode-worker/src/main.rs:329`。
- `discovered_capabilities.push → winwincode_execution_port::capability_adapter::CapabilityDescriptor::mcp → server.digest.trim_start_matches`；`crates/winwincode-worker/src/main.rs:330`。
- `snapshot         .providers         .iter()         .find(|provider| provider.config.enabled &amp;&amp; provider.credential_configured)         .ok_or → snapshot         .providers         .iter()         .find → snapshot         .providers         .iter`；`crates/winwincode-worker/src/main.rs:343`。
- `env::var("WWC_WORKER_MODEL_PROVIDER_ID")         .unwrap_or_else → env::var`；`crates/winwincode-worker/src/main.rs:348`。
- `env::var("WWC_WORKER_MODEL_ID")         .unwrap_or_else → env::var`；`crates/winwincode-worker/src/main.rs:350`。
- `data_directory.join → PathBuf::from → required → ActionEnforcementSigningKey::from_bytes → parse_hex_key → Sha256Digest`；`crates/winwincode-worker/src/main.rs:352`。
- `Ok → ProductionCodexAdapter::open(ProductionCodexConfig::try_new(options)?)?             .with_device_extensions → ProductionCodexAdapter::open → ProductionCodexConfig::try_new → provider_directory.to_path_buf`；`crates/winwincode-worker/src/main.rs:371`。

**shared_loop 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `worker_capabilities`；`crates/winwincode-worker/src/main.rs:167`。
- `configured_execution_mode`；`crates/winwincode-worker/src/main.rs:168`。
- `configured_observer_mode`；`crates/winwincode-worker/src/main.rs:169`。
- `configured_observation_model`；`crates/winwincode-worker/src/main.rs:170`。
- `RemoteWorkerPort::open → fs::read → required → worker_id.clone → worker_instance_id.clone → Duration::from_secs`；`crates/winwincode-worker/src/main.rs:171`。
- `production_codex → capabilities.clone`；`crates/winwincode-worker/src/main.rs:179`。
- `DurableValidationArtifactStore::open → data_directory.join`；`crates/winwincode-worker/src/main.rs:187`。
- `JobWorkspaceRuntime::open(data_directory.join("worker-workspaces"), &amp;source_directory)?             .with_validation_artifact_port → JobWorkspaceRuntime::open → data_directory.join`；`crates/winwincode-worker/src/main.rs:189`。
- `worker_instance_id.clone → started_at.clone`；`crates/winwincode-worker/src/main.rs:192`。
- `data_directory.join("codex-runtime").join → data_directory.join`；`crates/winwincode-worker/src/main.rs:198`。
- `WorkerMain::new(config, port, codex, workspaces)         .with_device_providers(&amp;provider_directory)?         .with_observer_mode(observer_mode)         .with_registration_request_namespace(&amp;worker_instance_id, &amp;started_at)         .with_model_intake_log → WorkerMain::new(config, port, codex, worksp…［展示截断；完整值见引用］`；`crates/winwincode-worker/src/main.rs:199`。
- `worker.with_observation_model`；`crates/winwincode-worker/src/main.rs:204`。
- 后续步骤保留在 `/functional_chains/16/pattern/sequences/shared_loop`。

**worker_constructor 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `recover_message_sequence`；`crates/winwincode-worker/src/lib.rs:487`。
- `recover_heartbeat_sequence`；`crates/winwincode-worker/src/lib.rs:488`。
- `HashMap::new → HashSet::new → VecDeque::new`；`crates/winwincode-worker/src/lib.rs:490`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| scoped_source_supported | true | /functional_chains/16/pattern/scoped_source_supported |
| sequences/adapter_factory/conditions | [] | /functional_chains/16/pattern/sequences/adapter_factory/conditions |
| sequences/adapter_factory/future_or_callback_activation_proven | false | /functional_chains/16/pattern/sequences/adapter_factory/future_or_callback_activation_proven |
| sequences/adapter_factory/orders/0/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/16/pattern/sequences/adapter_factory/orders/0/conditions |
| sequences/adapter_factory/orders/0/all_paths_reach_next_proven | false | /functional_chains/16/pattern/sequences/adapter_factory/orders/0/all_paths_reach_next_proven |
| sequences/adapter_factory/orders/1/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/16/pattern/sequences/adapter_factory/orders/1/conditions |
| sequences/adapter_factory/orders/1/all_paths_reach_next_proven | false | /functional_chains/16/pattern/sequences/adapter_factory/orders/1/all_paths_reach_next_proven |
| sequences/adapter_factory/orders/2/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/16/pattern/sequences/adapter_factory/orders/2/conditions |
| sequences/adapter_factory/orders/2/all_paths_reach_next_proven | false | /functional_chains/16/pattern/sequences/adapter_factory/orders/2/all_paths_reach_next_proven |
| sequences/adapter_factory/orders/3/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/16/pattern/sequences/adapter_factory/orders/3/conditions |
| sequences/adapter_factory/orders/3/all_paths_reach_next_proven | false | /functional_chains/16/pattern/sequences/adapter_factory/orders/3/all_paths_reach_next_proven |
| sequences/adapter_factory/orders/4/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/16/pattern/sequences/adapter_factory/orders/4/conditions |
| sequences/adapter_factory/orders/4/all_paths_reach_next_proven | false | /functional_chains/16/pattern/sequences/adapter_factory/orders/4/all_paths_reach_next_proven |
| sequences/adapter_factory/orders/5/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/16/pattern/sequences/adapter_factory/orders/5/conditions |
| sequences/adapter_factory/orders/5/all_paths_reach_next_proven | false | /functional_chains/16/pattern/sequences/adapter_factory/orders/5/all_paths_reach_next_proven |
| sequences/adapter_factory/orders/6/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/16/pattern/sequences/adapter_factory/orders/6/conditions |
| sequences/adapter_factory/orders/6/all_paths_reach_next_proven | false | /functional_chains/16/pattern/sequences/adapter_factory/orders/6/all_paths_reach_next_proven |
| sequences/adapter_factory/orders/7/conditions | ["both direct statements normally reached in the same invocation","preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"] | /functional_chains/16/pattern/sequences/adapter_factory/orders/7/conditions |

所有事实及源位置：`/functional_chains/16/source_facts`；配置声明单列于 `/functional_chains/16/policy_declarations`，不作为自动证据。

### `wwc-report-worker-typed-dispatch`

分析类型：`guarded_call_sequence`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/17`；保存发现：`1fc26eccb25a192cdd8c7408`。

**control 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `self.accept_registration → self.codex                     .accept_execution_delivery_ack(message)                     .map_err → self.codex                     .accept_execution_delivery_ack → self.flush_durable_execution_deliveries → self.flush_durable_execution_deliveries_with_core_replay → self.a…［展示截断；完整值见引用］`；`crates/winwincode-worker/src/lib.rs:748`。

**dispatch 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `Err → worker_error`；`crates/winwincode-worker/src/lib.rs:2639`。
- `dispatch_authority_rejection → self.send_dispatch_result → Some → Ok`；`crates/winwincode-worker/src/lib.rs:2645`。
- `CodexRunKey::from_dispatch`；`crates/winwincode-worker/src/lib.rs:2650`。
- `winwincode_codex::stage_product::stage_product_job_digest(&amp;dispatch.job)             .map_err → winwincode_codex::stage_product::stage_product_job_digest`；`crates/winwincode-worker/src/lib.rs:2651`。
- `self.dispatches.get(&amp;dispatch.job.job_id.0).cloned → self.dispatches.get → self.send_dispatch_result → Some → Ok`；`crates/winwincode-worker/src/lib.rs:2658`。
- `winwincode_codex::stage_product::stage_product_prompt(&amp;dispatch.job).is_err → winwincode_codex::stage_product::stage_product_prompt → self.send_dispatch_result → Some → port_error → Ok`；`crates/winwincode-worker/src/lib.rs:2674`。
- `usize::try_from(self.config.capabilities.max_concurrent_jobs).unwrap_or → usize::try_from`；`crates/winwincode-worker/src/lib.rs:2689`。
- `self.active.len → self.send_dispatch_result → Ok`；`crates/winwincode-worker/src/lib.rs:2690`。
- `scope_identity`；`crates/winwincode-worker/src/lib.rs:2701`。
- `self.start_dispatch`；`crates/winwincode-worker/src/lib.rs:2702`。

**start 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `self.prepare_dispatch_workspace → self.reject_dispatch_failure → Ok`；`crates/winwincode-worker/src/lib.rs:2723`。
- `self             .codex             .ensure_thread → self.workspaces.prepare_close_job → self.reject_dispatch_failure → Ok`；`crates/winwincode-worker/src/lib.rs:2744`。
- `self.dispatch_thread_conflicts → self.codex.close_thread → self.workspaces.prepare_close_job → self.reject_dispatch_failure → Ok`；`crates/winwincode-worker/src/lib.rs:2777`。
- `self.recovered_runtime_cursor`；`crates/winwincode-worker/src/lib.rs:2795`。
- `self.install_dispatch_binding → runtime_session_context → now.clone`；`crates/winwincode-worker/src/lib.rs:2797`。
- `self.start_bound_job`；`crates/winwincode-worker/src/lib.rs:2810`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| scoped_source_supported | true | /functional_chains/17/pattern/scoped_source_supported |
| sequences/control/conditions/0/branch_context/0/activation_proven | false | /functional_chains/17/pattern/sequences/control/conditions/0/branch_context/0/activation_proven |
| sequences/control/conditions/0/branch_context/0/kind | match_arm | /functional_chains/17/pattern/sequences/control/conditions/0/branch_context/0/kind |
| sequences/control/conditions/0/branches/0/abrupt_source_expressions/0/kind | return_expression | /functional_chains/17/pattern/sequences/control/conditions/0/branches/0/abrupt_source_expressions/0/kind |
| sequences/control/conditions/0/branches/0/abrupt_source_expressions/0/runtime_completion_proven | false | /functional_chains/17/pattern/sequences/control/conditions/0/branches/0/abrupt_source_expressions/0/runtime_completion_proven |
| sequences/control/conditions/0/branches/0/branch | then | /functional_chains/17/pattern/sequences/control/conditions/0/branches/0/branch |
| sequences/control/conditions/0/branches/0/branch_all_paths_abrupt_proven | true | /functional_chains/17/pattern/sequences/control/conditions/0/branches/0/branch_all_paths_abrupt_proven |
| sequences/control/conditions/0/branches/0/call_ids | ["be1a2e9583d2c77591d92cad"] | /functional_chains/17/pattern/sequences/control/conditions/0/branches/0/call_ids |
| sequences/control/conditions/0/condition/kind | try_expression | /functional_chains/17/pattern/sequences/control/conditions/0/condition/kind |
| sequences/control/conditions/0/condition/operand/callee_source | self<br>                    .workspaces<br>                    .is_observation_model_exchange(&amp;chunk.model_exchange_id)<br>                    .map_err | /functional_chains/17/pattern/sequences/control/conditions/0/condition/operand/callee_source |
| sequences/control/conditions/0/condition/operand/arguments/0/kind | closure_expression | /functional_chains/17/pattern/sequences/control/conditions/0/condition/operand/arguments/0/kind |
| sequences/control/conditions/0/condition/operand/arguments/0/runtime_value_proven | false | /functional_chains/17/pattern/sequences/control/conditions/0/condition/operand/arguments/0/runtime_value_proven |
| sequences/control/conditions/0/condition/operand/arguments/0/source | \|_\| workspace_error() | /functional_chains/17/pattern/sequences/control/conditions/0/condition/operand/arguments/0/source |
| sequences/control/conditions/0/condition/operand/arguments/0/source_truncated | false | /functional_chains/17/pattern/sequences/control/conditions/0/condition/operand/arguments/0/source_truncated |
| sequences/control/conditions/0/condition/operand/call_effects_or_result_proven | false | /functional_chains/17/pattern/sequences/control/conditions/0/condition/operand/call_effects_or_result_proven |
| sequences/control/conditions/0/condition/operand/callee_expression/current_referent_value_proven | false | /functional_chains/17/pattern/sequences/control/conditions/0/condition/operand/callee_expression/current_referent_value_proven |
| sequences/control/conditions/0/condition/operand/callee_expression/kind | field_expression | /functional_chains/17/pattern/sequences/control/conditions/0/condition/operand/callee_expression/kind |
| sequences/control/conditions/0/condition/operand/callee_expression/member | map_err | /functional_chains/17/pattern/sequences/control/conditions/0/condition/operand/callee_expression/member |

所有事实及源位置：`/functional_chains/17/source_facts`；配置声明单列于 `/functional_chains/17/policy_declarations`，不作为自动证据。

### `wwc-report-workrun-finite-selection`

分析类型：`rust_finite_state_selection`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/18`；保存发现：`409a9e2d1a7a8b93c1cd532b`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| necessary_gaps | [] | /functional_chains/18/pattern/necessary_gaps |
| all_active_states_or_attempts_proven | false | /functional_chains/18/pattern/all_active_states_or_attempts_proven |
| dependency_blocker_relation/supported | true | /functional_chains/18/pattern/dependency_blocker_relation/supported |
| dependency_blocker_relation/relations/0/dependency_collection/value/kind | name | /functional_chains/18/pattern/dependency_blocker_relation/relations/0/dependency_collection/value/kind |
| dependency_blocker_relation/relations/0/dependency_collection/value/name | item | /functional_chains/18/pattern/dependency_blocker_relation/relations/0/dependency_collection/value/name |
| dependency_blocker_relation/relations/0/dependency_collection/value/span | [23825,23829] | /functional_chains/18/pattern/dependency_blocker_relation/relations/0/dependency_collection/value/span |
| finite_effective_state_relation/supported | true | /functional_chains/18/pattern/finite_effective_state_relation/supported |
| finite_effective_state_relation/symbolic_quantifiers/0/expression/receiver/receiver/value/kind | name | /functional_chains/18/pattern/finite_effective_state_relation/symbolic_quantifiers/0/expression/receiver/receiver/value/kind |
| finite_effective_state_relation/symbolic_quantifiers/0/expression/receiver/receiver/value/name | item | /functional_chains/18/pattern/finite_effective_state_relation/symbolic_quantifiers/0/expression/receiver/receiver/value/name |
| finite_effective_state_relation/symbolic_quantifiers/0/expression/receiver/receiver/value/span | [23825,23829] | /functional_chains/18/pattern/finite_effective_state_relation/symbolic_quantifiers/0/expression/receiver/receiver/value/span |
| finite_source_countercases/countercases_are_symbolic_source_conditions_not_observed_runtime_records | true | /functional_chains/18/pattern/finite_source_countercases/countercases_are_symbolic_source_conditions_not_observed_runtime_records |
| finite_source_countercases/non_runnable_table_rows/0/effective_state | WorkItemState::Done | /functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows/0/effective_state |
| finite_source_countercases/non_runnable_table_rows/0/input_state | WorkItemState::Done | /functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows/0/input_state |
| finite_source_countercases/non_runnable_table_rows/0/runnable | false | /functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows/0/runnable |
| finite_source_countercases/non_runnable_table_rows/0/source_quantifiers/source_quantifier_1 | false | /functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows/0/source_quantifiers/source_quantifier_1 |
| finite_source_countercases/non_runnable_table_rows/1/effective_state | WorkItemState::Done | /functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows/1/effective_state |
| finite_source_countercases/non_runnable_table_rows/1/input_state | WorkItemState::Done | /functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows/1/input_state |
| finite_source_countercases/non_runnable_table_rows/1/runnable | false | /functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows/1/runnable |

**有限源码分区 rows**；`/functional_chains/18/pattern/finite_effective_state_relation/rows`，展示 8/8 行；展示截断=false。

| effective_state | input_state | runnable | source_quantifiers | 完整行引用 |
| --- | --- | --- | --- | --- |
| WorkItemState::Done | WorkItemState::Done | false | {"source_quantifier_1":false} | /functional_chains/18/pattern/finite_effective_state_relation/rows/0 |
| WorkItemState::Done | WorkItemState::Done | false | {"source_quantifier_1":true} | /functional_chains/18/pattern/finite_effective_state_relation/rows/1 |
| WorkItemState::Ready | WorkItemState::Ready | true | {"source_quantifier_1":false} | /functional_chains/18/pattern/finite_effective_state_relation/rows/2 |
| WorkItemState::WaitingDependency | WorkItemState::Ready | false | {"source_quantifier_1":true} | /functional_chains/18/pattern/finite_effective_state_relation/rows/3 |
| WorkItemState::Ready | WorkItemState::WaitingDependency | true | {"source_quantifier_1":false} | /functional_chains/18/pattern/finite_effective_state_relation/rows/4 |
| WorkItemState::WaitingDependency | WorkItemState::WaitingDependency | false | {"source_quantifier_1":true} | /functional_chains/18/pattern/finite_effective_state_relation/rows/5 |
| &lt;other value of this state enum&gt; | &lt;other value of this state enum&gt; | false | {"source_quantifier_1":false} | /functional_chains/18/pattern/finite_effective_state_relation/rows/6 |
| &lt;other value of this state enum&gt; | &lt;other value of this state enum&gt; | false | {"source_quantifier_1":true} | /functional_chains/18/pattern/finite_effective_state_relation/rows/7 |

**有限源码分区 non_runnable_table_rows**；`/functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows`，展示 6/6 行；展示截断=false。

| effective_state | input_state | runnable | source_quantifiers | 完整行引用 |
| --- | --- | --- | --- | --- |
| WorkItemState::Done | WorkItemState::Done | false | {"source_quantifier_1":false} | /functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows/0 |
| WorkItemState::Done | WorkItemState::Done | false | {"source_quantifier_1":true} | /functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows/1 |
| WorkItemState::WaitingDependency | WorkItemState::Ready | false | {"source_quantifier_1":true} | /functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows/2 |
| WorkItemState::WaitingDependency | WorkItemState::WaitingDependency | false | {"source_quantifier_1":true} | /functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows/3 |
| &lt;other value of this state enum&gt; | &lt;other value of this state enum&gt; | false | {"source_quantifier_1":false} | /functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows/4 |
| &lt;other value of this state enum&gt; | &lt;other value of this state enum&gt; | false | {"source_quantifier_1":true} | /functional_chains/18/pattern/finite_source_countercases/non_runnable_table_rows/5 |

**有限源码分区 runnable_table_rows**；`/functional_chains/18/pattern/finite_source_countercases/runnable_table_rows`，展示 2/2 行；展示截断=false。

| effective_state | input_state | runnable | source_quantifiers | 完整行引用 |
| --- | --- | --- | --- | --- |
| WorkItemState::Ready | WorkItemState::Ready | true | {"source_quantifier_1":false} | /functional_chains/18/pattern/finite_source_countercases/runnable_table_rows/0 |
| WorkItemState::Ready | WorkItemState::WaitingDependency | true | {"source_quantifier_1":false} | /functional_chains/18/pattern/finite_source_countercases/runnable_table_rows/1 |

所有事实及源位置：`/functional_chains/18/source_facts`；配置声明单列于 `/functional_chains/18/policy_declarations`，不作为自动证据。

### `wwc-report-workrun-state-guards`

分析类型：`state_guard_sequence`；源码关系：`scoped_source_relations_supported`。

完整关系、条件、边界与证据：`/functional_chains/19`；保存发现：`db018b5abf4fca55e9128fa0`。

**selection 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `self.validate`；`crates/winwincode-delivery/src/application/workrun.rs:392`。
- `self             .runs             .iter()             .filter(|run| {                 matches!(                     run.state,                     WorkRunState::Leased | WorkRunState::Running | WorkRunState::CandidateReady                 )             })             .map(|run| run.work_item_id.clo…［展示截断；完整值见引用］`；`crates/winwincode-delivery/src/application/workrun.rs:393`。
- `start_next_work_run → self.contract.revision.clone`；`crates/winwincode-delivery/src/application/workrun.rs:404`。
- `self.start_item`；`crates/winwincode-delivery/src/application/workrun.rs:411`。

**start 的正常源码顺序**（前序操作正常完成且分支到达时）：

- `self.validate`；`crates/winwincode-delivery/src/application/workrun.rs:419`。
- `self             .items             .iter()             .find(|item| {                 &amp;item.id == id                     &amp;&amp; work_item_is_runnable(item, &amp;self.items)                     &amp;&amp; !self.runs.iter().any(|run| {                         &amp;run.work_item_id == id                             &amp;&amp; ma…［展示截断；完整值见引用］`；`crates/winwincode-delivery/src/application/workrun.rs:420`。
- `item.clone`；`crates/winwincode-delivery/src/application/workrun.rs:439`。
- `Ok`；`crates/winwincode-delivery/src/application/workrun.rs:441`。

| 保存关系／条件 | 实际值 | 完整 JSON Pointer |
| --- | --- | --- |
| all_active_states_or_attempts_proven | false | /functional_chains/19/pattern/all_active_states_or_attempts_proven |
| scoped_source_supported | true | /functional_chains/19/pattern/scoped_source_supported |
| selection_predicate_sources/0/callback_activation_proven | false | /functional_chains/19/pattern/selection_predicate_sources/0/callback_activation_proven |
| selection_predicate_sources/0/expression/runtime_value_proven | false | /functional_chains/19/pattern/selection_predicate_sources/0/expression/runtime_value_proven |
| selection_predicate_sources/0/macro_expansion_or_iterator_effects_proven | false | /functional_chains/19/pattern/selection_predicate_sources/0/macro_expansion_or_iterator_effects_proven |
| selection_predicate_sources/1/callback_activation_proven | false | /functional_chains/19/pattern/selection_predicate_sources/1/callback_activation_proven |
| selection_predicate_sources/1/expression/operands/0/operands/0/runtime_predicate_or_assignment_proven | false | /functional_chains/19/pattern/selection_predicate_sources/1/expression/operands/0/operands/0/runtime_predicate_or_assignment_proven |
| selection_predicate_sources/1/expression/operands/0/operands/1/callee_source | work_item_is_runnable | /functional_chains/19/pattern/selection_predicate_sources/1/expression/operands/0/operands/1/callee_source |
| selection_predicate_sources/1/expression/operands/0/operands/1/call_effects_or_result_proven | false | /functional_chains/19/pattern/selection_predicate_sources/1/expression/operands/0/operands/1/call_effects_or_result_proven |
| selection_predicate_sources/1/expression/operands/0/runtime_predicate_or_assignment_proven | false | /functional_chains/19/pattern/selection_predicate_sources/1/expression/operands/0/runtime_predicate_or_assignment_proven |
| selection_predicate_sources/1/expression/operands/1/operands/0/callee_source | self.runs.iter().any | /functional_chains/19/pattern/selection_predicate_sources/1/expression/operands/1/operands/0/callee_source |
| selection_predicate_sources/1/expression/operands/1/operands/0/call_effects_or_result_proven | false | /functional_chains/19/pattern/selection_predicate_sources/1/expression/operands/1/operands/0/call_effects_or_result_proven |
| selection_predicate_sources/1/expression/operands/1/operands/0/callee_expression/current_referent_value_proven | false | /functional_chains/19/pattern/selection_predicate_sources/1/expression/operands/1/operands/0/callee_expression/current_referent_value_proven |
| selection_predicate_sources/1/expression/operands/1/runtime_predicate_or_assignment_proven | false | /functional_chains/19/pattern/selection_predicate_sources/1/expression/operands/1/runtime_predicate_or_assignment_proven |
| selection_predicate_sources/1/expression/runtime_predicate_or_assignment_proven | false | /functional_chains/19/pattern/selection_predicate_sources/1/expression/runtime_predicate_or_assignment_proven |
| selection_predicate_sources/1/macro_expansion_or_iterator_effects_proven | false | /functional_chains/19/pattern/selection_predicate_sources/1/macro_expansion_or_iterator_effects_proven |
| selection_predicate_sources/2/callback_activation_proven | false | /functional_chains/19/pattern/selection_predicate_sources/2/callback_activation_proven |
| selection_predicate_sources/2/expression/operands/0/operands/0/operand/current_referent_value_proven | false | /functional_chains/19/pattern/selection_predicate_sources/2/expression/operands/0/operands/0/operand/current_referent_value_proven |

**保留的分析缺口**：

- `iterator_selection_and_macro_runtime_semantics_not_fully_proven`；完整位置与原因见 `/functional_chains/19/analysis_gaps`。

所有事实及源位置：`/functional_chains/19/source_facts`；配置声明单列于 `/functional_chains/19/policy_declarations`，不作为自动证据。

## 捕获范围与未审边界

选入 471 份源码，解析 465 份。这是源码捕获与语法解析范围，不能换算成功能完整率。

| 区域 | 文件 | 已解析 |
| --- | --- | --- |
| apps/client | 95 | 95 |
| crates/helper | 1 | 1 |
| crates/kernel | 2 | 2 |
| crates/winwincode-api | 1 | 1 |
| crates/winwincode-audit | 5 | 5 |
| crates/winwincode-cli | 11 | 11 |
| crates/winwincode-client-port | 12 | 12 |
| crates/winwincode-codex | 16 | 16 |
| crates/winwincode-connector-github | 1 | 1 |
| crates/winwincode-connector-jira | 1 | 1 |
| crates/winwincode-connector-linear | 1 | 1 |
| crates/winwincode-connector-slack | 1 | 1 |
| crates/winwincode-connector-teams | 1 | 1 |
| crates/winwincode-connector-webhook | 1 | 1 |
| crates/winwincode-control-plane | 94 | 94 |
| crates/winwincode-data-export | 1 | 1 |
| crates/winwincode-delivery | 25 | 25 |
| crates/winwincode-device-client | 20 | 20 |
| crates/winwincode-domain | 5 | 5 |
| crates/winwincode-evidence-export | 6 | 6 |
| crates/winwincode-execution-port | 26 | 25 |
| crates/winwincode-fusion | 4 | 4 |
| crates/winwincode-integration-core | 5 | 5 |
| crates/winwincode-integration-sqlite | 2 | 2 |
| crates/winwincode-local | 1 | 1 |
| crates/winwincode-observability-core | 1 | 1 |
| crates/winwincode-observability-sqlite | 1 | 1 |
| crates/winwincode-provider | 11 | 11 |
| crates/winwincode-publication | 7 | 7 |
| crates/winwincode-repository-context | 5 | 5 |
| crates/winwincode-s3-artifact-adapter | 1 | 1 |
| crates/winwincode-server | 23 | 22 |
| crates/winwincode-session | 4 | 4 |
| crates/winwincode-storage | 34 | 33 |
| crates/winwincode-worker | 21 | 18 |
| deploy | 1 | 1 |
| docs/engineering-runtime | 1 | 1 |
| jev-runtime-spec/js | 1 | 1 |
| packages/browser-core | 2 | 2 |
| packages/browser-ui | 7 | 7 |
| packages/contracts | 6 | 6 |
| packages/control-plane-client | 1 | 1 |
| packages/strongflow | 2 | 2 |
| schema/winwincode-export | 3 | 3 |
| winwincode-bd-tracks/js | 1 | 1 |

项目声明与依赖：`/project_declarations`；已绑定跨目录图引用：`/architecture/dependencies`。声明存在、路径可达和依赖计数均不证明业务行为通过。

- `crates/winwincode-execution-port/src/diagnostic_parser.rs`：parse_error；Tree-sitter 检测到错误/缺失语法节点；仅提取可识别的局部结构。。
- `crates/winwincode-server/src/worker_session_credentials.rs`：parse_error；Tree-sitter 检测到错误/缺失语法节点；仅提取可识别的局部结构。。
- `crates/winwincode-storage/src/provider_exchange.rs`：parse_error；Tree-sitter 检测到错误/缺失语法节点；仅提取可识别的局部结构。。
- `crates/winwincode-worker/src/managed_session.rs`：parse_error；Tree-sitter 检测到错误/缺失语法节点；仅提取可识别的局部结构。。
- `crates/winwincode-worker/src/probe_evidence.rs`：parse_error；Tree-sitter 检测到错误/缺失语法节点；仅提取可识别的局部结构。。
- `crates/winwincode-worker/src/probe_scheduler.rs`：parse_error；Tree-sitter 检测到错误/缺失语法节点；仅提取可识别的局部结构。。

配置排除：`[".git",".beads",".agents",".codex",".callscope",".analysis-tools",".venv","venv","__pycache__","node_modules","target","dist","build","coverage","third_party","upstream","vendor","generated","tests","test","__tests__","examples","scripts","crates/winwincode-test-assets","**/*.test.ts","**/*.test.ts…［展示截断；完整值见引用］`。

所选局部分析：`/configured_local_assessments`；完整诊断：`/diagnostics`。未建模域保持未审，不保证全仓库无缺陷、所有权或授权完整，也不将未知标为通过。

报告生成组件：`/report_components`；原快照分析组件：`/snapshot/component_versions`。两者分别保存，历史发现不会因生成新版报告而升级。

