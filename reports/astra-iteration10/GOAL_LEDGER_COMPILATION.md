# 正式保存结果的账本整理

2026-10-13，两库正式扫描和正常结果查询均关闭后，`compile_goal_ledger.py` 使用只读事务与公共 source-query 锁完成整理，退出码为 0。

| 原目标 | 实际 adapter | 保存判断 | 完整判断 / 原主张支持 | 保存义务 |
| --- | --- | --- | --- | --- |
| CPB-01 | pipeline | scoped_static_judgment_reproduced | true / true | P1–P6 supported |
| CPB-02 | status | scoped_static_judgment_reproduced | true / true | S1–S5 supported |
| CPB-03 | atomicity | scoped_static_judgment_reproduced | true / true | A1–A7 supported |
| WWC-01 | navigation | scoped_static_judgment_reproduced | true / true | N1–N7 supported |
| WWC-02 | device | scoped_static_judgment_reproduced | true / true | D1–D5 supported |

五目标的 necessary gaps 和未闭合必要义务均为空。上述状态直接来自保存的 `static_goal_judgment`；整理脚本没有重新评级。原两份全文报告仍是功能基准，五目标和三十关系是实施追踪索引。

| 核对项目 | CodePatchBay | WinWinCode |
| --- | ---: | ---: |
| 原文件 SHA 和来源身份核对次数 | 55,995 | 1,822 |
| 原记录声明的 span hash 核对次数 | 27,355 | 1,691 |
| 只声明坐标的 span 记录核对次数 | 27,673 | 0 |
| 来源清单记录 | 335 | 482 |

SourceAnchor 只声明文件 SHA 和 byte coordinates 时，核对这些已有字段及原文本边界，保留原记录，不填造 span hash。位置次数包含重复引用，不是源码、函数、业务或测试覆盖率。704 个 JSON pointer 均核对原内容 digest、证据存档 SHA 和 finding/evidence/contract/snapshot/tool/policy/source 身份，无采样。

- CPB snapshot：`7524afef4f9234ebef40eec1d74dbb91a3f56dc76f0191728c42d3bdd3cfb167`。
- WWC snapshot：`ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28`。
- 两库冻结工具 SHA：`664f0723371e930791f7a69669cdf33e2bde4d85f9342cfd21ac3fcb9c97a44f`。
- `goal-ledger.json` SHA：`20fe301d50a157e2e18440ab1b2e5d6ea735c885c90d65bdd1ec028c4da6f819`，168,797,502 bytes。
- `GOAL_JUDGMENT_EVIDENCE.json` SHA：`9a792a33aca0623b007a88cfc5b6473b2cacfeea3e6fdba02129f8cca7a5489e`，151,899,555 bytes。
- 整理脚本 SHA：`d4c15552c56cfe51c96584176caae8637181846d7e4b52ed4c7348a2112f9ccc`。

两份产物保留完整原 adapter 结果，因此体积较大。账本保留所选静态模型、环境条件和反证；没有执行目标代码、测试或构建，没有证明所有运行时行为或整库功能完整性。冻结 core、policy、目标源码和原报告未修改。
