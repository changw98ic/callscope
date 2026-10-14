# Rust crate 属性上下文：三个旧 partial 的源码根因与修复

本项以原完整 WinWinCode 报告和 v0.12 的三个实际 partial 为依据。未重新审查项目，没有增加模型批准流程，也未修改旧报告、数据库、配置或目标源码。

## 实际根因

`crates/winwincode-worker/src/main.rs:3` 与 `crates/winwincode-server/src/main.rs:3` 都声明 `#![recursion_limit = "256"]`。旧 Rust 前端把不在通用标准属性集合内的该内建编译限制当作未知属性宏，将 `scope.opaque=true` 传播到整个 crate。因而 main、run_remote、run_managed、run_worker、production_codex 和 DeviceModelBoundary.accept 六个真实、唯一的捕获声明都被标成 `attribute_macros_unknown`。`SemanticSources.definition_for_node` 正确保守拒绝它们，但拒绝的上游属性分类错误。

另一个作用域问题是 `sequence` 在预处理 inner attribute 后，仍把它排入下一条 item 的 outer attribute 队列。修复后 inner attribute 只作用于所属 body；outer attribute 继续只作用于自己的 item，未知 inner attribute 继续使整个相应 scope 不透明。

## 实现与接口

新增 `callscope/rust_source_context.py`：

```python
classify_crate_inner_attribute(node, raw, *, is_known_crate_root: bool) -> dict | None
```

只在调用者已经确认配置 crate root、CST 为完整的 source_file 直接 inner attribute、属性名为 `recursion_limit` 或 `type_length_limit`、值为明文十进制字符串时返回模型。外层属性、非 crate root、名称空间属性、cfg_attr、token tree、其他名称及非明文值继续返回 None。不把上述名称加入全局忽略集合。

模型为 `rust-builtin-crate-limit-attribute-v1`，上下文版本为 `rust-captured-source-context-1`，声明其不变更声明名称绑定，并明确 `macro_expansion_performed=false`、`cfg_evaluated=false`、`compilation_validated=false`、`macro_or_trait_target_resolution_closed=false`。每份模型保留原文、source hash、byte span 与 span hash，记录在模块及其继承声明的 `builtin_crate_attribute_models` 中。

`rust_analyzer.py` 在真实 scope 中调用该接口，前端版本为 `rust-tree-sitter-1.8-crate-attribute-context`。未修改 SemanticSources 的身份/唯一性检查或报告的支持判定；确定调用边由既有解析器依据实际 CST 和词法绑定自然生成。

## 真实源码查询

运行的是可信 CallScope 的正常静态分析，输入来自同一个旧 v0.12 policy 的只读源码捕获；不是测试或合成夹具。没有加载目标模块、调用目标程序、运行测试、构建、安装或执行任何目标 probe。

- [修复前查询](RUST_SOURCE_CONTEXT_BEFORE.json)
- [修复后查询](RUST_SOURCE_CONTEXT_AFTER.json)
- [三个原规则的开发查询](RUST_REPORT_CLAIMS_DEVELOPMENT_QUERY.json)
- [可复查查询脚本](query_rust_source_context.py)

前后 351 份 Rust 输入的路径、hash、解析状态全部相同；九个所选声明中错误 opaque 从六个变为零。保留的六份 parse_error、1,776 个条件声明、三个未展开宏、24 个重复声明及 494 个原泛型同 impl 绑定均未改变。全部 opaque 声明由 979 个变为 926 个；这不是功能覆盖率。

开发查询中的图域明确标记 `development-rust-source-query-*`，不冒充已发布的完整多语言快照，原 v0.12 正式结果也未被改写。三项结果均由同一套原规则计算：

| 原条目 | 实际开发查询状态 | 声明认证 | 源事实数 / 操作数 |
| --- | --- | --- | --- |
| wwc-report-worker-bootstrap-entries | scoped_source_relations_supported | 3/3 唯一来源闭合 | 76 / 412 |
| wwc-report-worker-production-construction | scoped_source_relations_supported | 3/3 唯一来源闭合 | 182 / 977 |
| wwc-report-device-provider-deployment | scoped_source_relations_supported | 4/4 唯一来源闭合 | 142 / 696 |

三个条目都未耗尽预算。Device 分流保留 `deployment_candidate_chain_not_global_dispatch_or_credential_availability`，未把部署来源关系扩大为 credential 可用性或任意泛型分派保证。

## 保留的边界

所选调用点仍有 74 个 dynamic。`WorkerMain::new` 在调用点仍为 dynamic，原因为泛型类型/别名/trait 关联目标未推断；没有为了使生产构造条目成立而补一条指向某个泛型实现的 CALLS。某些调用从属性宏 unknown 进入更具体的 unresolved，例如来自未解析 generated domain 声明的 WorkerId/WorkerInstanceId/Sha256Digest；因此 unresolved 数从 1,396 增至 1,407，未被掩盖成确定调用。

这次修复闭合的是原三个条目的有限源码声明身份和已有步骤关系，不证明 worker 实际启动、provider 已配置、generic 端口的唯一运行实现、完整跨消息身份、运行成功或整份报告已完成。
