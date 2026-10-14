# WinWinCode：Astra 独立静态分析 v1

分析对象：`/workspace/winwincode`，提交 `da407e4f3df3719718b23bd8913b73fe3ff73857`。本报告于 2026-10-12 固定第一版。只读项目源码、声明和已有图证据；没有执行、导入、构建或测试目标代码，也没有触发 Beads、仓库索引、Node/Cargo 脚本或外部服务。

## 判断

WinWinCode 已有真实的纵向产品结构：浏览器表现层通过生成合同访问 Server，产品状态由 Control Plane/Delivery 应用服务推进，Worker 通过 ExecutionPort 承担工作区和执行事实，ProductionCodexAdapter 接入嵌入式 Kernel。对象、角色、候选、lease/fencing 和证据身份并非只有架构图中的名字，源码中有相应检查、持久化和恢复分支。

但“链条存在”与“每个公开入口可完成用户任务”不同。本轮独立复核了两处具体接口接线缺口：看板的“新建任务”导航没有携带生产 task port 所需的 delivery 上下文；Device 交付的需求编辑命令遗漏服务器条件分支必需的 verificationCommand。两者都有可定位的生产挂接和反证，不依赖运行失败猜测，也不意味着 Chat 创建或所有本地交付均失效。

当前 CallScope 对 Rust 大量方法/trait 和前端组合入口的覆盖不足，远不能代替这份跨文件、合同和条件分支的人工分析。第一阶段值得补齐的是合法语法、明确 Self/具体类型方法、带来源的组合候选与基准核对；不能承诺仅靠调用图自动推出所有产品缺口。

## 覆盖账本

| 区域 | 本轮阅读层次与代表来源 | 边界 |
| --- | --- | --- |
| 产品与工作区 | `README.md`、`AGENTS.md`、`docs/architecture.md`、workspace/package/crate 清单 | 确认单一 Client/Rust 服务路径和嵌入式 Kernel 意图；未运行文档中的验证命令 |
| 浏览器组合入口 | `boot.ts`、`application.ts`、scope/context helper、runtime config | 重点检查真实生产组合、登录/范围、路由、lazy import、TaskPort 注入 |
| 任务创建与需求编辑 | `home-dashboard-page.ts`、`my-work-page.ts`、`task-entry-view-model.ts`、`community-control-plane-client.ts`、`chat-delivery-creator.ts`、`decision-clarification-view-model.ts` | 深读两个缺口涉及的生产链和 Chat/local 分支反证；不是全 UI 可用性或浏览器验收 |
| HTTP/WS 与 Control Plane | client facade、Server main/dispatcher 的接口和组合来源、Control Plane authority 段落 | 检查协议、状态所有权和生产挂接；未逐一审完全部命令/查询/WS 路由 |
| Delivery/WorkRun | `delivery/src/application/workrun.rs`、`control-plane/src/delivery_production_adapters.rs` 及关联合同 | 重点检查 runnable/active/revision、候选与规格 authority；完整领域状态机和所有并发交错未穷举 |
| Worker | `worker/src/main.rs`、`lib.rs` 的控制消息、dispatch、工作区/adapter 调用段落，managed session 接口 | 检查本地/远程共用 typed boundary、生产组装和泛型端口；没有运行租约或故障恢复 |
| Codex/Kernel | `codex/src/adapter.rs` 的 open、submit/reconcile、持久化边界；`kernel/src/lib.rs` 的 session/turn 入口 | 核对嵌入式主路径和精确自身方法绑定样本；未复审全部 vendored Codex 内核、工具与沙箱 |
| Provider/Device | worker 与 device provider 的组装来源、Server DeviceModelBoundary | 确认存在 Device 本地凭据/模型路径；没有调用模型、读取真实凭据或验证运行部署 |
| 其余领域 crate | storage、publication、audit、integration、connectors、export、repository-context 等的职责/manifest 与接口盘点 | 不把目录完整盘点当作每个 adapter 的完整行为审计；外部 provider/connector 副作用未实测 |
| 未审 | 测试全部行为、构建脚本执行、所有生成文件一致性、第三方副本、所有平台和迁移路径 | 生成合同仅按相关字段和引用只读核对；不运行生成器或编译器 |

此前工具选入 471 份文件，459 份完整解析，含 TypeScript/JS 120/114、Rust 351/345；Python 配置存在但选入为 0。图含 31,941 个节点、170,176 条边，16,357 条已绑定内部调用约占全部记录边 9.61%。这是边类别分布，不是函数覆盖率或内部调用召回率；Rust cfg/test 声明也影响图总量。生成源码和第三方实现的排除与 12 个解析缺口不能藏在“97.45% 文件解析率”后面。

## 架构与职责

| 区域 | 所有权与接口 | 独立判断 |
| --- | --- | --- |
| `apps/client`、`packages/browser-*` | 页面、路由、表单、投影和浏览器状态 | UI 可以组织请求，但产品写入仍要经 canonical command；页面存在不等于其所需上下文已接线 |
| `packages/control-plane-client`、生成合同 | HTTP command/query、WS projection/event | 网络关系应由协议/命令类型连接，不应该伪造成跨语言普通函数调用 |
| `winwincode-server` | 认证、公开网络边界、dispatcher、模块组合 | 不应仅按模块大判断职责混乱；检查是否另建事实所有权更重要 |
| `winwincode-control-plane`、Delivery/domain/session | 产品状态、审批、WorkContract/WorkItem/WorkRun 与候选/证据关联 | revision、来源身份和条件 authority 决定能否写入；调用是否存在只是一部分 |
| `winwincode-worker`、execution-port | Job、Lease、fencing、工作区、运行/结果/产物消息 | generic adapter 是扩展边界，不等于实现缺失；分派需要真实类型和组合证据 |
| `winwincode-codex`、Kernel/helper | durable adapter、嵌入式 Codex session/turn、工具与权限；helper 身份校验 | 生产代码通过 Kernel API，不能用安装的 Codex CLI 作为补缺假设 |
| Device/provider | managed worker、设备本地 provider 配置/凭据和流转发 | 当前生产 Device 路径需要与旧文档“Control Plane 唯一长期凭据使用者”区分 |

产品的 ProductSession、WorkerSession、CodexThread、WorkRun 身份分离有实际意义：重试或换 worker 不能靠一个 session_id 代表全部历史。静态分析应保留这些字段的连接来源，避免只按同名方法拼路径。

## 主要静态功能链

### 1. 浏览器启动、范围和协议

`boot.ts:23` 调用 `mountWinWinCodeClient({root, serverUrl})`，没有注入 fake task seed。`application.ts` 根据 runtime/auth/scope 创建真实端口，使用 lazy import 挂页面并以 render generation/abort 等条件防止旧页面结果回写。`diagnosticScope` 在第 359 行明确调用 `resolveScopeContext`，后者继续调用 `scopeSelectionFromHash`；该跨包关系可以由源码确定。

v0.3 因 `application.ts:966` 的 inline import 类型语法缺口而失去整个组合文件的确定节点。这是严重的工具覆盖问题，不能解释为项目缺少入口。类似语法还在 client/probe 相关文件中出现；部分文件含字符串中的真实 U+0000，修复解析必须保留原始源码和位置映射，不能抹掉 ERROR 后声称语义完整。

Client 的请求经过 typed facade 和生成合同进入 Rust dispatcher，再交给 Control Plane 应用服务。HTTP/WS 的消息名称、requestId、scope、expectedRevision 才是跨语言连接证据。只凭 `client.command` 和某个同名 Rust 方法，不足以确定所有调用目标或授权顺序。

### 2. Chat 到交付与 WorkRun

`chat-delivery-creator.ts` 有实际 `DeliveryCreate` 请求（第 235 行）、规范 spec（第 239–254 行）、后续 WorkItem/WorkRun 请求（约第 299–309 行），并保留请求身份用于重试。该路径是看板新任务缺口的重要反证：不能把一个入口的问题推广成“系统完全不能创建任务”。

Control Plane 的 specification authority 根据命令区分 create/update，验证 scope、repository、Device baseline 和 verification command（`delivery_production_adapters.rs:583–654`）。随后领域 aggregate 负责推进约束。这里存在条件必填字段：TypeScript 类型上 optional 不代表所有运行上下文中都可省略。

`WorkRunAggregate.start_next`（`workrun.rs:391`）先 `self.validate()`，从已持久 runs/items 求候选，再调 `self.start_item`（`:411`）。`start_item`（`:418`）再次验证并排除依赖未满足、Leased/Running/CandidateReady 的活动尝试。这些都是具体自身类型上的固有方法，适合新增有限 Rust 方法解析，不能与任意 trait 对象的分派混在一起。

### 3. 调度消息到 Worker

`worker/main.rs` 的 remote 与 managed-session 两入口最终进入同一个 `run_worker`；构造 RemoteWorkerPort、ProductionCodexAdapter、workspace runtime 和 WorkerMain。managed-session 的配置、租约身份和短期凭据来源，与 Server 产品状态分开。

`WorkerMain.accept_control` 在 `worker/lib.rs:743–766` 按 typed message 分派；JobDispatch 会先处理 durable replay 再交给 `accept_dispatch`。dispatch 检查 job/workspace/profile 和容量，然后 `start_dispatch` 准备 checkout，再调用注入的 `CodexCoreAdapter.ensure_thread`（`:2744–2754`）。失败分支会拒绝并收尾；结构路径存在不能证明所有资源均在所有故障点回收。

`Codex` 是泛型端口。即使生产 main 组装了 ProductionCodexAdapter，也不能把类定义中 `self.codex.ensure_thread` 全局写成唯一的确定实现边；应保留组合上下文、候选及剩余未知，尤其不能混入测试实现。

### 4. Production adapter 到嵌入式 Kernel

`ProductionCodexAdapter::open`（`adapter.rs:412`）建立私有目录、封存/校验 helper、打开 adapter store/outbox、组装 action/model bridge，并在 `:459` 调用 `Kernel::new`。这是实际生产接线，不是从 README 推断内核存在。

`impl CodexCoreAdapter for ProductionCodexAdapter` 中 `submit_turn` 先比较规范 stage prompt/digest，设置 submission intent，调用 `self.persist_run`（`:3558`），然后调用 Kernel 的 `reconcile_turn_exact`（`:3574`）。这个顺序解释了恢复设计，但本轮不据源码宣称已经做过崩溃一致性演练。

Kernel 的 `create_session`（`kernel/src/lib.rs:1220`）通过 runtime manager 创建线程；`submit_turn`（`:1333`）验证输入并对 session thread 调用 start/steer；`reconcile_turn_exact`（`:1369`）检查指定 turn 的 durable history。普通 `submit_turn` 与精确 reconcile 是不同接口，不能只因名称相近合并成一条链。

### 5. 证据、候选与外部交付

项目将候选、冻结提交、WorkRun/lease/fencing、角色和 evidence source 纳入交付合同；WorkRun 侧有具体 revision/活动 run 检查，adapter 有 durable outbox/ack。静态审查能确认这些机制和接口存在，尚不能证明外部日志、candidate bytes、签名和 provider 结果的真实性。

Publication、audit、export 和 connector 是单列模块，有自己的操作键、receipt 和持久化职责。未逐一审核这些外部副作用适配器，不能从通用架构宣称 exactly-once 发布、完全防泄漏或所有连接器实现完整。

### 6. Provider 的部署分流

当前 Server 的 DeviceModelBoundary 对模型消息返回 unsupported，不能单独判为模型能力缺失。Worker main 会组装设备 provider；`DeviceModels` 打开设备存储，device provider 解析配置/secret 后调用 adapter。此路径有独立实现来源。

`docs/architecture.md` 把长期 Credential/Provider 路由绝对归为 Control Plane，与当前 Device 生产路径至少存在说明口径差异。更稳妥的结论是文档应按 local/Device 部署明确所有权，而不是将 Device 分流判为违反唯一 Kernel 原则：Provider 所在位置与执行 Kernel 是否唯一是不同问题。本轮不提供所有 secret 路径的完整安全审计结论。

## 两项具体产品接线缺口

### WWC-01：看板“新建任务”缺少生产端口要求的 delivery 上下文

**定性：指定公开导航链的确定接线缺口；触发条件是走默认生产端口且 URL 无 delivery。** 可见看板链接在 `home-dashboard-page.ts:360` 调用 `surfaceHash('/home/new-task', scopeSelection)`。`scope-context.ts:271–272` 用新的 route 构造 URL，只附范围信息，不保留旧的 delivery entity 参数。

`application.ts:277–305` 创建生产 task port，其 `deliveryContext` 只从当前 URL 读取 delivery；第 288 行无值即返回 null。`createControlPlaneTaskPort.create`（`community-control-plane-client.ts:2791–2793`）收到 null 立即拒绝。新任务表单输入（`task-entry-view-model.ts:311–321`）包括设备、仓库、分支、描述、模型路由，没有补 delivery 选择或创建；拒绝后只展示 unavailable 并保留草稿。

反证：手工构造带有效 delivery 的链接、注入 taskSeed 的 fake 端口、ChatDeliveryCreator 的独立创建流程都可能避开这一问题。`my-work-page` 另有同类链接但其 start 区被隐藏，本结论以实际看板可见按钮为入口，不靠隐藏元素证明可触达。

建议在此入口明确选择“新建 Delivery”或“在指定 Delivery 新建 WorkItem”，把该上下文带入表单和命令；不要简单改后端为无上下文放行。CallScope 需要 URL/对象字段来源、注入闭包与条件拒绝链才能覆盖它，只有调用路径不足以裁决。

### WWC-02：Device 交付的需求编辑丢失 verificationCommand

**定性：条件必填字段的跨语言契约接线遗漏；只限 Device specification 分支。** `clarificationUpdateCommand`（`decision-clarification-view-model.ts:190–220`）构造 `delivery.update_spec` 的完整 spec，但没有 verificationCommand；展示数据虽然读到 criterion.verificationMethod（`:163–168`），提交时也没有把它恢复为服务端需要的顶层字段。保存逻辑在 `:243–244` 把该命令送往真实 client，application 第 1421–1456 行有生产挂接。

Rust `LocalDeliveryAuthority::specification` 同时处理 create/update（`delivery_production_adapters.rs:589–596`）。Device target 存在时，第 616–623 行要求非空 `spec.verification_command`，否则直接拒绝。输入字段 optional 的 schema 不能替代该分支的业务要求。

反证：本地非 Device 分支在第 638–641 行可从仓库选 verification command，不受这项遗漏同样影响；Chat 的创建请求在 `chat-delivery-creator.ts:246` 能显式携带该字段。因此不能宣称所有规格编辑、所有新建交付都失败。修正时应保留经过确认的命令身份并明确变更授权，不能从任意 UI 文本猜一条可执行命令。

两项结论均未进行浏览器或服务运行复现，属于沿生产源码条件推导的结果。它们在机器基准中是 `evidence_only`，不让现有调用图冒充字段合同验证器。

## 反证与不能得出的结论

- Rust 自调用/环不证明无法终止，不能用普通递归结构凑项目缺陷数。
- generic/trait/宏/cfg 导致未知是当前模型边界；生产具体装配提供候选来源，不允许按方法名字猜唯一实现。
- DeviceModelBoundary 返回 unsupported 有设备侧实际处理链作反证，不代表系统缺模型连接。
- application 文件解析失败与 missing endpoint 是工具能力空白，不代表组合入口源码缺失。
- 代码有 revision、lease、fencing 检查不代表所有并发路径都已证明；反过来，尚未建模的字段关联也不等于缺少检查。
- 创建、更新、重试、取消和恢复是不同功能；其中一个正向链存在不能替另外几个入口验收。

## CallScope 能力推进与验收

| 优先级 | 能力 | 真实样本 | 约束 |
| --- | --- | --- | --- |
| P1 | TypeScript 合法语法与证据定位 | application inline import 类型、其他导入类型/保留字/U+0000 字符串 | 保存原 bytes/hash，派生解析文本独立记录映射；不吞未识别错误 |
| P1 | 明确 Self 的 Rust 固有方法 | WorkRunAggregate.start_item→validate；start_next→start_item；ProductionCodexAdapter.submit_turn→persist_run | 限定接收器实际类型、作用域、条件声明和唯一目标；不把任意 trait 分派提升为确定边 |
| P1 | 冻结基准核对和能力账本 | 原始调用位置/源码 hash/端点/路径及未知原因 | source_changed、unknown、mismatch 和 evidence_only 单列，不能只统计可通过项 |
| P2 | 对象工厂与显式注入 | auth/task/client facade，WorkerMain 生产构造 | 保留条件候选和剩余未知，不按 create/build/validate 命名猜返回对象 |
| P2 | 生成合同与传输关系 | command name、payload、scope/revision、HTTP/ExecutionPort frame | 作为带 schema/version 的协议关系，不伪造成直接 CALLS |
| P2 | 字段保留与条件必填 | delivery URL、verificationCommand | 必须跟踪构造、映射、覆盖和消费者分支，不能仅做同名搜索 |
| P2 | 状态/顺序/身份关联 | WorkRun 活动状态、submission intent→persist→reconcile、候选来源 | 静态证据范围明确，不能越级承诺事务或运行语义 |
| P3 | 性能、分片和更多可视化 | 在稳定语义和输入身份基础上优化 | 图大小与渲染效果不是功能成熟度 |

首轮迭代可以验收语法恢复、具体方法绑定及对冻结观察的诚实核对；要“接近本报告”，还需要保留架构/协议/字段证据，而不是只提高 resolved 比例。要超越人工阅读，应依靠更广一致的重复分析与变化追踪，保留反例和不确定性，而不是把每个未知都消除。

机器基准见 [capability-baseline.json](capability-baseline.json)，协议见 [BASELINE_CONTRACT.md](BASELINE_CONTRACT.md)。本报告没有运行通过、功能覆盖率、性能或全仓库安全保证。

来源整理附录：[浏览器入口与产品链](../astra-baseline-preparation/WWC_FRONTEND.md)、[Rust 生命周期](../astra-baseline-preparation/WWC_RUST_LIFECYCLE.md)、[TypeScript 语法与绑定边界](../astra-baseline-preparation/TS_GAPS.md)。附录中未独立闭环的 publication 等线索不自动成为本报告的确认结论。冻结机器基准含本仓库 13 项观察及所引原文件哈希。
