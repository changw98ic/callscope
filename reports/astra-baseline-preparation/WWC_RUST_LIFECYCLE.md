# WinWinCode Rust 执行生命周期来源整理

来源助手：`documentation_examples`。整理日期：2026-10-12。目标源码：`/workspace/winwincode`。

本稿提供给 Astra 独立审查的源码定位、接线证据和反证，不是最终架构评审，也不是目标项目的功能通过证明。本轮只读取生产源码、manifest 和相关合同文档；未导入、执行、构建目标，未运行任何测试。没有检查活动 Cargo feature、运行时配置或部署中的外部消费者。

文中路径均相对于目标仓库；行号来自本轮读取的源码。`generated.rs` 本轮作为合同证据手动读取，与之前 CallScope 真实仓库扫描所排除的生成文件范围不同。

## 1. 核心边界与生产组合

| 边界 | 实际责任与源码证据 | 判读限制 |
| --- | --- | --- |
| API / HTTP Server | `crates/winwincode-server/src/server.rs:433` 挂载 commands、queries、events；`:2354` 将 command 请求送至 API port。`dispatcher.rs:198` 的 `GeneratedContractDispatcher` 实现 `ControlPlaneApiPort`，`:214` 调用 typed application。 | HTTP 路由、trait 和解码不是执行结果证明。 |
| Typed application | `crates/winwincode-server/src/application.rs:1201` 实现 `TypedControlPlaneApiPort`，`:1232` 分派 command；Session、Delivery、Publication 分别进入内部方法。 | 这是具体实现与接口的组合证据，不能要求纯静态工具把所有 trait 调用无条件判为确定边。 |
| Control Plane | `crates/winwincode-control-plane/src/lib.rs:966` 的 `ControlPlane` 管理产品状态、receipt、outbox、Delivery、调度及 Publication。其 Cargo.toml 依赖 domain、delivery、execution-port、storage、provider 等，不依赖 server、worker 或 Codex Core。 | 产品态与 Kernel 运行事实是不同所有者。 |
| Domain / Delivery | domain 提供公共身份和值对象；delivery 的 aggregate、stage transition、candidate 与 verdict 承载交付领域语义。`delivery_production_adapters.rs:817` 使用 `WorkRunStartResult::canonical_workrun_dispatch`。 | 不能把项目内部 reviewer/verifier 功能的存在误认为本轮运行了验证。 |
| ExecutionPort | `crates/winwincode-execution-port/src/transport.rs:452` 定义 `ExecutionPortCore`；`:486` 的 local adapter 与 `:565` 的 remote adapter 都校验方向后调用同一 core.accept。 | 跨进程连接需要消息合同与发送/接收证据，单个调用图路径不覆盖整个协议。 |
| Worker / Kernel | `crates/winwincode-worker/src/main.rs:179` 组合 production Codex，`:199` 组合 WorkerMain、workspace runtime、execution port 与 Device Provider。更深的 Worker→Kernel 生命周期由 Astra 独立审查。 | 本来源稿不重复或替代 Kernel 内部审查。 |
| Provider | 当前 server/worker 生产组合采用 Device 私有 Provider。`worker/main.rs:200`、`worker/lib.rs:409`、`provider/device_store.rs:67` 为明确接线。 | Control Plane 另有 ProviderGateway 模块不等于每种生产组合都通过该模块解析长期凭据。 |
| Storage | `winwincode-storage` 的 `ProductStateStorage` / `SqliteStorage` 保存产品状态、receipt、outbox 与执行队列；PublicationStorageAdapter 复用产品存储。 | 持久受理、队列就绪、执行成功、交付成功需分别观察。 |
| Publication | publication coordinator 管理持久发布意图、操作与外部副作用协调；Control Plane policy seam 控制 publish / resume；production registry 绑定具体 provider。 | `publish` 写入意图与 `resume` 推进外部操作是不同阶段，见候选接线缺口。 |

生产主入口的重要反证：`crates/winwincode-server/src/main.rs:182` 调用 `ControlPlane::start_local_with_production_adapters`，该方法在 `control-plane/src/publication_production.rs:663` 先安装 Delivery，再安装 Publication。Server main `:194` 的注释明确默认 `start_local` 尚无 Artifact catalog，但生产入口 `:198–204` 创建 object store / ArtifactStore 并调用 `install_artifact_store`。不能因默认构造器留空就判生产 Artifact 接线缺失。

## 2. Chat 请求 → 持久排队 → Device 执行 → 产品投影

源码链路为：

```text
HTTP command
  → GeneratedContractDispatcher.command
  → StandaloneControlPlaneApplication.session_command
  → Device 会话权限 / 仓库绑定 / model route gate
  → ProductSessionApiService.submit_chat
  → ProductSessionService 的提交路径
  → commit_with_execution_job（catalog + receipt + outbox + job）
  → dispatch_turn_to_device_worker（绑定 grant / admission / execution facts）
  → Device Worker / Kernel 执行
  → ExecutionPort canonical binding / public model frames / terminal outcome
  → ProductSessionExecutionApplication
  → 产品态及事件投影
```

具体接线与条件：

- `crates/winwincode-server/src/application.rs:385` 的 `session_command` 在 `:402` 读取 `product_session_turn_gate`；`:407–413` 对缺 Device anchor 明确返回 `DEVICE_SESSION_REQUIRED`。`:426` 验证 Device 当前模型路由，`:435` 的错误为 `DEVICE_MODEL_UNAVAILABLE`。
- 同文件 `:451` 创建 `ProductSessionApiService`，`:456–458` 对 ChatSubmit 调用 `.submit_chat`；`:477` 在提交后调用 `dispatch_turn_to_device_worker`，`:486` 发布待发送事件。
- `crates/winwincode-control-plane/src/product_session_api.rs:124` 的 `submit_chat` 将 generated command 映射成 `SubmitChatMessageCommand::from_api` 并交给 service。
- `crates/winwincode-control-plane/src/product_session_service.rs:1464` 的内部 `commit` 生成 catalog state 和 mutation outbox；`:1499` 对 execution 追加内部执行 job 事件；`:1516–1518` 使用 `.commit_with_execution_job(&commit, &execution_job.submission)`，普通非执行变更走 `storage.commit`。
- `crates/winwincode-control-plane/src/quick_device_execution.rs:164` 的 `dispatch_turn_to_device_worker` 派生稳定 job id、读取会话 launch grant、检查 grant 状态、建立或重放 Device binding。`:253` 预留 admission，之后通过 DeviceExecutionBindingService attach facts。已有相同 grant/job facts 的分支直接重放，不重新绑定到另一个 Device。
- 同方法的无 anchor 分支返回 `Ok(None)`，但当前 Server ChatSubmit 入口已先拒绝缺 anchor。低层方法允许本地监督路径，不代表当前 Server API 无条件支持无 Device Chat。
- `crates/winwincode-control-plane/src/product_session_execution_application.rs:651` 实现 `DurableExecutionPortDelegate`；`:667` 接收 canonical Worker binding；`:674` 处理产品会话 outcome；`:742–777` 接收并校验 public-only ModelChunk 后投影且产生 ModelAck。
- `product_session_service.rs:862` 的 `continue_session` 从 storage 取 Worker slot / reservation，校验 exact execution identities 和 revision，再更新 binding 与 pending turn 的 Bound 状态。它没有从任意调用者的文本推断执行成功。

该链说明提交和执行已通过 durable identity 关联；仍不能从静态调用存在推导某次请求、模型服务或产品功能已运行成功。

## 3. Device Provider 的实际生产链路与文档反证

```text
worker/main.rs:199–203
  → WorkerMain.with_device_providers
  → DeviceModels::open
  → WorkerMain.send_execution_message
  → DeviceModels.send 的 ModelOpen 分支
  → DeviceProviderStore::open / execute_model
  → resolve(provider_id) 取得 Device 配置与 secret
  → adapter.open / drain_canonical
  → durable ModelChunk / Worker 接收与 Core 消费
```

- `crates/winwincode-worker/src/lib.rs:409–419` 创建 `DeviceModels`，记录 worker instance，再写入 `self.device_models`。
- 同文件 `:3953–3965` 的 `send_execution_message` 先尝试 `models.send(&message)`；若该 Device handler 接受就直接返回，不发送给 Server execution port。未处理的消息才转发到 port。
- `crates/winwincode-worker/src/device_model.rs:122–165` 的 ModelOpen 分支保存 exchange identity，启动 `device-provider` 线程；`:150–151` 实际调用 `DeviceProviderStore::open` → `execute_model`。该线程及闭包关系是人工确认的组合证据，当前调用解析器不一定完整还原。
- `crates/winwincode-provider/src/device_model.rs:26` 为 `execute_model`，使用 SQLite exchange digest / chunks 重放，并对重启后未知的未完成请求返回 `DEVICE_MODEL_INTERRUPTED`，不无条件再次请求。`:93` 的 `resolve` 得到 config / secret，`:101` 调用 adapter.open，`:140` drain_canonical。
- `crates/winwincode-provider/src/device_store.rs:3` 说明 Server 只转发认证密文；`:67–79` 说明 Device daemon 与其 managed Workers 共用私有数据库。`:113–116` 保存私有 identity、providers、receipts、exchanges。
- `crates/winwincode-server/src/main.rs:292` 组合 `ProductSessionExecutionApplication::new_with_action_issuer(DeviceModelBoundary, ...)`，`:297` 装配 ServerExecutionPortCore。`:339` 的 `DeviceModelBoundary` delegate 拒绝其余消息是明确边界；此处注释说明 model payload / Provider credentials 留在 Device process。

契约/文档差异：`docs/architecture.md:158`、`docs/decisions/0001-upstream-integration.md:54` 和 `docs/decisions/0028-control-plane-worker-dependency-rules.md:76` 使用“长期凭据的唯一使用者是 Control Plane”的绝对表述，与上述当前 server/worker 生产路径不一致。仓库内还保留 Control Plane ProviderGateway/production 模块；因此应要求文档明确各部署模式或更新所有者表述，不能据旧文档把已明确组装的 Device 路径定为模型功能缺失。本稿未逐一确认其它 launcher 的模式。

## 4. Delivery / WorkRun → Worker authority → candidate / verdict

```text
generated workrun.start
  → application.delivery_command
  → ControlPlane.workrun_start
  → LocalDeliveryAuthority.advance
  → canonical_workrun_dispatch + trusted execution config
  → prepare_workrun_start / PendingDeliveryExecution
  → durable Delivery journal + receipt + job intent
  → LocalExecutionJobDispatcher / execution queue
  → scheduler admission / exact lease & fencing / Worker
  → canonical SessionBinding / runtime events / Artifact ACK / JobOutcome
  → terminal_outcome_transaction
  → current writer candidate + read-only verification runtime facts
  → resolve_production_verdict / canonical verdict commit
```

- `crates/winwincode-server/src/application.rs:620` 的 `delivery_command` 分派 create、workrun.start、submit verdict；`:658` 调用 `control_plane.workrun_start`，`:666` 调用 `delivery_submit_verdict`。用户启动 WorkRun 的分支在产品态提交后调用 Device dispatch；不是每种 actor 都走该路径。
- `crates/winwincode-control-plane/src/delivery_application.rs:683` 的 `workrun_start` 优先返回 exact replay，检查 catalog membership，取 current Delivery，`:707` resolve authority，`:713` commit authority。
- 同文件 `:734–767` 的 Dispatch 分支要求 trusted execution config，`:741` `prepare_workrun_start`，`:750` 构造 PendingDeliveryExecution，`:756` 取得已安装的 dispatcher，`:761` `commit_delivery_execution`。Clarify 分支 `:768–779` 明确不创建 execution job。
- `crates/winwincode-control-plane/src/delivery_production_adapters.rs:663` 的 `LocalDeliveryAuthority.advance` 检查 scope、Delivery repository、profile 与 rework authorization。`:781` 为 reviewer/verifier/adversarial-verifier 解析当前冻结 candidate；`:817` canonical WorkRun dispatch；`:832` 生成执行配置。它不会随意伪造 Worker outcome。
- `crates/winwincode-control-plane/src/delivery_execution.rs:413` 定义原子 transaction seam，`:437` 定义 dispatcher seam。`:531–566` 的 `commit_and_dispatch` 先 commit，验证 receipt；重放不再次 dispatch；`:551` dispatch，`:558` 标记 exact outbox event 已发送。Dispatch/ack 失败会保留已提交 receipt 与待恢复意图。
- `crates/winwincode-control-plane/src/delivery_production_adapters.rs:959` 的 `LocalExecutionJobDispatcher` 将稳定 job/payload 写入 execution queue，已有 job 分支检查完全相同的 payload；安装入口 `:1058` 为 `ControlPlane::install_local_delivery_adapters`。
- `crates/winwincode-control-plane/src/workrun_transaction.rs` 的 `execute` 接收 `ExecutionDispatchAuthority` 和 WorkRun proof，检查 job/lease/scope、建立 Leased WorkRun，再通过 journal publication 与 StateCommit 原子提交。authority 参数是调度器已接受的事实，不是 API 可随意提供的成功标记。
- `crates/winwincode-control-plane/src/product_session_execution_application.rs:695–727` 使用 sealed SessionBinding authority 接收 ArtifactOpen / ArtifactChunk，并返回 canonical ArtifactAck。
- `crates/winwincode-control-plane/src/durable_execution_port.rs:771` 的 `terminal_facts` 用 exact dispatch authority 封存 WorkRun terminal facts；`:808` 调用 `commit_delivery_terminal_outcome`。
- `crates/winwincode-control-plane/src/lib.rs:2119` 的 terminal commit 使用 `terminal_outcome_transaction::execute_at`；`:2133` settle/release Worker resources；`:2152` flush outbox。资源或事件发布失败返回带已提交 receipt 的 pending 类错误，不把 durable commit 擦掉。
- `crates/winwincode-control-plane/src/delivery_verdict_authority.rs:37–89` 的 `resolve` 从 current writer、durable terminal、Artifact / Git source 重建 candidate，并读取独立角色的 runtime events，`:81` `resolve_production_verdict`。`:113–162` 的 current candidate read 对 Queued/Leased/Running 明确无候选，对已完成状态读取 exact terminal/source 并 freeze；不退回旧 writer。
- `crates/winwincode-control-plane/src/lib.rs:2195` 的 `commit_delivery_verdict` 负责 Evidence、Verdict、blocking Attention、task state、journal、receipt 和 outbox 的原子更改。

这些是目标仓库自身的执行/验证领域代码。本次没有运行其中的任何方法，也未判断其业务验收标准是否正确。

## 5. Publication 正向接线与待独立核对的推进缺口

已确定的正向链路：

```text
application.publication_command
  → ControlPlane.publication_publish
  → current candidate / user authorization / policy facts
  → LocalPublicationAuthority.resolve
  → PublicationProviderRegistry.resolve → short-lived PublicationPort
  → commit_publication_publish
  → PublicationCoordinator.publish
  → PublicationLedger.create（Pending intent）
```

- `crates/winwincode-server/src/application.rs:769–789` 分派 publish/cancel；`:777` 调用 publication_publish。
- `crates/winwincode-control-plane/src/publication_production.rs:696` 优先读取 exact receipt replay；`:714–735` 重建 current candidate、要求 User actor、prepare_publication，并进入 commit_resolved_publication_publish。
- 同文件 `:749` resolve authority；`:761` resolve provider session；`:765–772` 把 session.port 传给 commit_publication_publish。`:626–654` 确实在生产启动中安装了 authority / provider registry，不能报“没有 Publication provider”。
- `crates/winwincode-control-plane/src/publication_policy.rs:218–261` 校验 policy context、建立 Audit seam，`:252` 调用 coordinator.publish 后记录结果。
- `crates/winwincode-publication/src/coordinator.rs:1052–1085` 的 publish 只授权并构造 initial publication，调用 ledger.create。initial state 定义在 `:250` 为 Pending。
- `crates/winwincode-storage/src/publication.rs:232` 的 PublicationStorageAdapter 实现领域 storage；`:255` 把领域 journal mutation、state 和 outbox 组合到产品 StateCommit。只读 adapter `:221–228` 的 commit 拒绝写入是查询边界，不是发布时误用了只读存储的证据。

**候选 WWC-PUBLICATION-DRIVER：生产组合未见持久意图的 resume 调度接线。** 实际外部操作协调位于 `publication/src/coordinator.rs:1101` 的 resume：`:1134` port.lookup，Absent 分支 `:1157` apply_absent_operation。Control Plane 暴露 `publication_policy.rs:272` 的 `resume_publication`，其 `:290` 调用该领域 resume，并在终态 `:302` finalize candidate retention。

本轮对 `crates/**` 的生产 `*.rs` 做了限定搜索，排除 tests 目录、test_support.rs 与 generated.rs；`resume_publication(` 只出现上述定义，未见 Server、local 或其它生产模块调用。Coordinator 的其它 Control Plane 构造点为只读 detail 与 cancel helper；Server publish 路径终止于 Pending intent。`docs/contracts/control-plane-publication-policy.md:92–95` 规定 recovery Worker 只能调用此 typed seam，当前 HTTP 合同仍为 publish/cancel；`docs/architecture.md:160` 描述了意图落盘后的外部写入，但描述本身不能证明恢复任务已接线。

因此这是可供 Astra 独立确认的**源码组合缺口候选**：库层有外部发布能力，当前生产入口尚未找到从 Pending intent 到该能力的主动消费者。它不说明持久受理 API 失败，也不说明外部项目不能组合公开 Rust seam；未检查仓库外的部署服务。建议最终结论使用明确仓库/生产入口范围，避免把“未找到消费者”扩大成任何部署都无法发布。

## 6. 重要 trait 与生成合同边界

| Trait / 接口 | 实现或组合证据 | 静态模型应保留的含义 |
| --- | --- | --- |
| `ControlPlaneApiPort` | `server/dispatcher.rs:198` 的 GeneratedContractDispatcher | 运行时 HTTP state 持有该 port；实现关联不等于所有 receiver 自动可绑定。 |
| `TypedControlPlaneApiPort` | `server/application.rs:1201` 的 StandaloneControlPlaneApplication | 生成 command enum 的显式 match 可核对路由覆盖。 |
| `DurableExecutionPortDelegate` | `control-plane/product_session_execution_application.rs:651` 的泛型 decorator；server/main.rs:339 的 DeviceModelBoundary | decorator 显式处理 canonical supplement，其余转给 downstream；拒绝其它消息需结合部署所有权判断。 |
| `ExecutionPortCore` | `execution-port/transport.rs:452`；local/remote adapter 对相同 core.accept 的调用 | 一份核心语义复用多 transport；消息边不能简单等价普通函数边。 |
| `DeliveryAuthorityPort` | LocalDeliveryAuthority 的实现；delivery_production_adapters.rs:663 的 advance | authority-sealed事实来自生产适配器；仍需检查具体 feature/host 是否安装。 |
| `ExecutionJobDispatcher` | `delivery_execution.rs:437`；delivery_production_adapters.rs:959 的 LocalExecutionJobDispatcher | 接受 immutable job 与写队列是派发阶段，不是 job 已完成。 |
| `ProductSessionPersistence` / `ProductStateStorage` | product_session_service.rs:84；SqliteStorage 实现及 commit_with_execution_job | 产品状态与 job 可以同事务落盘，不以 callsite数量衡量原子性。 |
| `ProviderAdapterPort` | provider/types.rs:203；provider_https_sse.rs:791 的 HttpsSseProviderAdapter | Device model 方法调用真实 adapter；其 secret 使用边界不能由旧架构文档直接覆盖。 |
| `PublicationProviderRegistry` | publication_production.rs:354；启动安装 LocalPublicationProviderRegistry | provider 解析存在，消费者推进接线需另证。 |
| `PublicationStorage` | storage/publication.rs:198 的只读adapter与 :232 的可写adapter | 同 trait 下能力有差异；不能把拒绝写入的查询adapter误判为发布路径。 |
| `PublicationPort` | publication/operation.rs:448；production registry 返回 session.port | lookup/apply 只在协调器的推进阶段有意义。 |

`crates/winwincode-api/src/generated.rs:2`、`winwincode-domain/src/generated.rs:2`、`winwincode-execution-port/src/generated.rs:2` 都标注来自 `scripts/generate-contracts.mjs`，并携带同一个 source digest。`execution-port/src/lib.rs:4–8` 声明 canonical schema 是公共 wire shapes 的唯一来源。生成 DTO 既可能被前端/协议解析消费，也可能只定义类型；未执行 generator，本稿不证明当前生成文件与 schema 完全同步。此前静态扫描排除生成代码时，跨该边界的不完整必须披露，不能将它当成仓库遗漏函数。

## 7. 交给 Astra 的收敛结论

1. 可核对的事实包括：生产 typed API 路由、durable Chat job 原子提交、Device dispatch、真实 Device Provider 组装、Delivery authority / journal / outbox / queue、terminal / candidate / verdict join，以及 Publication intent 的持久提交。
2. Artifact 默认空端口、Server DeviceModelBoundary 的 UnsupportedMessage、低层无 anchor fallback、只读 PublicationStorageAdapter 都有生产组合或调用条件反证，不能独立报功能缺口。
3. 需要独立核对的候选是当前仓库生产路径是否缺 Publication resume consumer；Provider长期凭据归属差异应单列文档/契约差异，不当成缺执行能力。
4. 以上不能推出全功能完整、模型正确、业务符合要求、运行恢复成功或性能达标。本轮没有任何目标执行或测试结果。
