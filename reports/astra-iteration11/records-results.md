# CPB record / projection 开发来源查询结果

这是当前 adapter 对 v0.12 已保存源码的正常静态查询，不是 v0.13 正式发布；旧数据库、policy 和报告没有改写。

当前模块 SHA256：`3e0dcc3ee795ee88eee9583c16bb12be17bcc62e9f62a2e62b3f63c15a6c7432`。三份产物均确认模块字节在查询期间稳定，所有预算未耗尽。

| 类型 | 有限来源关系 | facts / operations |
| --- | --- | --- |
| event_index_projection | 11/11 支持 | 971 / 11484 |
| trusted_command_lineage | 7/7 支持 | 466 / 5847 |
| unsupported_record_retention | 7/7 支持 | 1610 / 18919 |

event 的实际 join 包括 serializer→append 实参、projection callback.state→同一 index.jobs 记录→writer、readEvents→materializer→重建 index writer。独立源码调用边界与正常顺序不证明一次事务、物理持久化或全部恢复。

trusted command 的实际 join 包括 stdout→JSON.parse→policy parser、实际 callback 来源、loaded policy→lookup→command 实参及同一 formal executable/args→shell=false execFile。额外捕获 oracleProtectedPaths/changedOracleFiles：expectedEvidence 仍参与保护路径推导，所以完整 heap/全分支非干扰未证明。

unsupported 的实际 join 包括 true marker record→push→返回数组、true marker 排除所选 invalid skip、claim→返回 evidence、实际 ledger result→JSON.stringify→artifact content。另有 first-wins 的真实 Set.has→continue→后续 Set.add 来源；matching checklist、hardGate 先入、observation spread、abort/异常和 IO 效果分开。

每条产物各保留一条 source_only=true、necessary_to_scoped_source_relations=false 边界；有限来源接缝支持不代表未证明内容已关闭。完整 facts/位置/hash 见三个 JSON，精简身份与指针见 records-observations.json。

开发脚本最初未抽取到 capture tool hash；已将相同 snapshot/source hash 的 v0.12 frozen integration 身份关联回来，每份产物明确记录 post_query_artifact_identity_join 的 provenance、原 JSON hash 与 pointer，分析 facts/结果未改动。

完成自己的 Python AST 语法和 JSON/identity 检查，未执行、导入、测试或构建目标。
