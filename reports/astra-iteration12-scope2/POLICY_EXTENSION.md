# scope2 策略扩展说明

本文件只核对已冻结策略的实际差异，不读取扫描数据库，也不预先填写分析是否通过。详细定位、逐项保留检查和真实文件 SHA256 见 [POLICY_EXTENSION.json](POLICY_EXTENSION.json)。

| 仓库 | v13 规则数 | scope2 规则数 | 旧规则保留 | 旧规则对象完全不变 |
| --- | ---: | ---: | ---: | ---: |
| codepatchbay | 13 | 16 | 13 | 12 |
| winwincode | 18 | 20 | 18 | 18 |

上述数量是配置清单，不是完整报告覆盖率分母。两库的 `analysis`、排除项、入口、普通规则、静态合同及其他非 `report_claims` 配置，经实际 JSON 值逐项对比全部保留；全部旧源码定位在原规则内按原顺序、原下标保留。没有删除旧规则。

CodePatchBay 新增三项有限源码规则：

- `cpb-review-fixed-state-lineage`（`conditional_state_lineage`，8 个声明定位）。
- `cpb-finalizer-conditional-publication`（`conditional_publication_boundary`，6 个声明定位）。
- `cpb-task-read-projection`（`guarded_call_sequence`，8 个声明定位）。

`cpb-report-trusted-probe-command-source` 是唯一发生内容变化的旧规则：原 7 个定位完整保留，追加同一 `core/workflow/probe-runner.ts` 内 `scopeMatches`、`scopePathMatches`、`posixify`、`text` 四个 helper 定位，成为 11 个。该旧规则的其他字段、模型、适用条件和边界均未改变。

WinWinCode 新增两项有限源码规则：

- `wwc-document-device-provider-deployment-scope`（`document_deployment_consistency`，12 个声明定位，1 个文档定位）。
- `wwc-delivery-evidence-frozen-contract-slice`（`guarded_call_sequence`，14 个声明定位）。

Device 文档比较新增 `docs/architecture.md` 的数据定位，保留 Control Plane 内部与 Device 部署的限定范围。投影、固定候选/角色/证据来源、事件谱系及条件发布规则都只扩大实际源声明选区；策略未配置预期字段集合、guard、调用边或成功答案。实际结论必须由后续正式保存结果读取。

条件、错误前缀、回调激活、端口绑定与各个证据来源继续独立保留。定位增加不证明所有入口、授权、持久化、外部成功或运行时功能；未执行目标、测试、构建、安装或夹具。

| 文件 | 实际 SHA256 |
| --- | --- |
| `reports/astra-iteration11/codepatchbay-policy.json` | `10b62fde7dc4980cfd3ed1a84282497b02b088bc160f39c5d14e5d7c946fcfd9` |
| `reports/astra-iteration12-scope2/codepatchbay-policy.json` | `f3f0ba2eecdeb156eea3d4038e5e8ac2dd03b7ee94f9e989b9ce8d9f994a174f` |
| `reports/astra-iteration11/winwincode-policy.json` | `37012e03e3b276e30d511a5f479e05d6f42a5faddf051486c36b126642c9ea38` |
| `reports/astra-iteration12-scope2/winwincode-policy.json` | `24dd004b2130a963fa2e60724203c60e41c87ee780123bc27eccffc71bae3005` |

scope2 冻结核心身份为 `a198491ce936c91ce7a1c848789cf9fb27c5fc720b90ae81725c2ddf65f779dc`，共 65 份 Python 源码。两份当前策略的实际文件 hash 均与本目录冻结记录相符。此辅助说明未修改策略、核心或原轮次产物。
