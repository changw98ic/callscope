# 有限职责操作：真实保存源码发展查询

本记录来自两个 v13 已保存快照及明确记录 hash/pointer 的新增 data-only 选择范围，属于后续实现的发展查询。它不是 v14 正式扫描，不是原报告的覆盖率，也不把原报告正文当成预期答案。

实现入口为 `extract_responsibility_operations(snapshot, report)`，模型为 `finite-captured-responsibility-operations-v1`。模型从真实捕获 CST、词法 binder、记录字段和已有普通调用绑定提取十一类操作；`architecture_responsibilities.py` 据此生成限定的职责说明。设计和字段边界见 [OPERATIONS-DESIGN](responsibility-OPERATIONS-DESIGN.md)。

| 实际提取范围 | CodePatchBay | WinWinCode |
| --- | ---: | ---: |
| 选择定位器 | 188 | 98 |
| 唯一源操作 | 14,958 | 9,341 |
| 实际操作关系 | 9,736 | 5,705 |
| 访问 CST 节点 | 65,902 | 47,777 |
| 独立源码文件 | 101 | 76 |
| 独立 source hash/span anchor | 29,786 | 17,245 |
| 独立 Finding/Evidence/选择上下文引用 | 4,311 | 2,802 |
| 提取预算未完成 | false | false |

最终解释组件 `98bae1b6310422a7d749aaf77032592d625128e9fea4d0e117647744f047dd2f` 的两库正常重放均已完成、运行期间字节稳定。解释保留 346 / 489 个实际 callable owner 分组（含嵌套闭包），不是全仓库唯一职责或权限分配证明。CodePatchBay 另复用原已保存生产装配/记录通道模型生成 21 条独立边界说明；WinWinCode 的旧 v13 报告没有这类目标模型，因此该集合为 0。新增 state-lineage 模型应在含其真实新 scope/pattern 的正式报告中解释，未把它补写进旧 v13 报告。

提取组件字节为 `feed013a4e7e6f9114eade4848d4dafb36a8fdc1e3ed0eb8cd66ac0d583c4e72`。解释重放直接复用已存真实 extraction，没有再提取 CST。

CodePatchBay 的操作范围无未闭来源定位。WinWinCode 保留一个明确边界：`apps/client/src/generated/control-plane-client.ts::createControlPlaneHttpClient` 在原保存快照是 `support_input_only`，不充当图内实现，未伪造其 CST 操作或 CALLS。该边界与已有独立模型认证的有限 generated protocol 字段命题分开，不要求整个 generated 实现成为普通调用图。

新增的普通局部 `binding_initializer` / `binding_update` 由真实 binder 和赋值源码识别。例如 CodePatchBay 的 `scopeMatches` 实际包含 `count = 0`、在 `for` / `if` 条件下的 `count += 1` 和 `return count`。其单位需要连同真实 `allowedFiles` 遍历及 `changed.some(...)` 来源理解，不能把这个静态范围信号解释为业务语义验证；嵌套 callback 保留真实独立 owner，未从外层存在推激活。

普通接口说明仅在已有 CALLS 及真实目标/形参认证后称为已绑定接口。`authenticated_argument_parameter_projection` 继续要求确切形参 binder 和被调用声明内的实际引用。source order 只表示同一源 block 的位置先后；同名字段、相邻调用、字符串相同都不能补成身份或运输边。

操作位置与旧来源上下文分别通过 `source_location_index`、`evidence_reference_index` 集中保存。实际产物读回检查操作 ID 唯一性、每个操作内容 SHA、pool/operation Pointer、关系端点，以及当前只读文件 raw hash、UTF-8/BOM byte map、span hash。检查程序不打开数据库、不运行分析器，也不执行或导入目标。正式完成记录以两份 `responsibility-*-ARTIFACT_READBACK.json` 中实际保存的 artifact/module hash 和检查值为准。

源操作产物：

- [CodePatchBay 操作](responsibility-operations-codepatchbay-development.json) / [真实操作样例](responsibility-operation-samples-codepatchbay.json) / [产物读回](responsibility-codepatchbay-ARTIFACT_READBACK.json)
- [WinWinCode 操作](responsibility-operations-winwincode-development.json) / [真实操作样例](responsibility-operation-samples-winwincode.json) / [产物读回](responsibility-winwincode-ARTIFACT_READBACK.json)
- [CodePatchBay 职责解释](responsibility-explanations-codepatchbay-development.json) / [WinWinCode 职责解释](responsibility-explanations-winwincode-development.json)

所有本轮目标执行、目标导入、目标测试、目标构建和安装均未发生；没有夹具或 Astra 复审步骤。原两份完整报告仍是范围基准，职责表导航标签及原判断通过状态都不替代新操作的实际来源。
