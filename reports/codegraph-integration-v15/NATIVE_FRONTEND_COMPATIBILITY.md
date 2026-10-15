# 原生前端兼容性静态比较

比较结果：全部相同。

同一捕获输入覆盖 801 个真实源码文件、43492 个节点、232510 条边。

比较完整节点/边记录（含 metadata）、文件状态、diagnostics 和 native frontend stats。

| 库 | 语言 | 文件 | 节点 | 边 | 比较 |
| --- | --- | ---: | ---: | ---: | --- |
| codepatchbay | python | 2 | 28 | 74 | 相同 |
| codepatchbay | typescript | 328 | 11057 | 60497 | 相同 |
| winwincode | typescript | 120 | 2936 | 11042 | 相同 |
| winwincode | rust | 351 | 29471 | 160897 | 相同 |

旧工具冻结路径：`/workspace/callscope/reports/astra-iteration12-scope2/frozen-core-source`。
旧工具 source hash：`a198491ce936c91ce7a1c848789cf9fb27c5fc720b90ae81725c2ddf65f779dc`；65 个冻结 Python 文件逐个校验。

历史 snapshot/source_hash 与本次捕获的逐文件哈希详见 JSON 及 *-source-manifest.json。
使用当前真实目标目录，按旧冻结 policy 只读捕获一次；旧/新分析器读取同一份保存的文本。

本次未执行/导入目标代码，未运行测试或构建，未运行 detectors/contracts/goals/report 管线。
这只是既有三类原生语言前端的兼容性比较，不代表旧整体目标重验，也不验证新增语言能力。
已有 parse_error 和 unsupported 状态不因结果相同而视为通过。

本轮追加复核：`.h/.inc` 内容分类接线变更后，仅重跑 4 组当前 native 前端，复用原捕获和旧输出。
本比较直接调用 `execute_frontend`，不声称验证了 source_reader 的分类调度路径；全局工具 hash 仅为 observed。
