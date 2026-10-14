# WinWinCode：真实源码静态调用核对

本报告只读 `/workspace/winwincode` 的项目源码与 manifest，将真实代码作为分析数据。未修改该仓库，未运行其 `pnpm`、`cargo`、Beads、code-index、构建、测试、应用或其他项目执行入口。目标仓库的 `AGENTS.md` 已读取；其中开发执行命令不用于本次只读源码评估。

最终静态快照选入 471 个源码文件。10 项人工选取的真实调用关系中，9 项在确定调用边中重现；另 1 项受 `application.ts` 的语法库覆盖缺口影响，保持不确定。快照状态为 `partial`，这些结果不能用作 WinWinCode 功能完整或业务正确的证明。

## 仓库与范围

根 `package.json`、`pnpm-workspace.yaml` 及各工作区 manifest 显示项目包含 Node.js 24 ESM 的 `apps/client` 与 `packages/*`。根 `Cargo.toml` 显示项目含 Rust 2024 / Rust 1.95 的本地 `crates/*`，并显式将 `third_party/codex/codex-rs` 与 `upstream/vendor/*` 排除在工作区外。这里只读取声明，不执行它们要求的运行环境或构建工具。

配套配置为 [winwincode-policy.json](winwincode-policy.json)，语言范围为 Python、TypeScript/TSX、Rust，源码根为 `.`。生产 Rust crate 保留在扫描范围内，不用仅扫描前端的结果代表整个仓库。Python 被配置支持不表示该项目有 Python 生产实现；实际语言数量应以扫描库存为准。当前 TypeScript 前端也接收选入的 JavaScript/JSX/MJS/CJS 源码，仅解析其显式调用，不执行脚本；专门的 `scripts/` 工具目录按生产范围选择排除。

排除范围及影响：

| 范围 | 原因与边界 |
|---|---|
| `third_party/`、`upstream/`、`vendor/` | 第三方实现与上游副本，不将上千个外部文件计作项目覆盖；调用这些实现仍是外部边界 |
| `node_modules/`、`target/`、`dist/`、`dist-tests/`、`build/`、`coverage/` | 安装依赖、编译或统计产物，不重建也不运行；`dist-tests` 为源码读取器自动排除的工具产物 |
| `generated/`、`*.generated.ts`、`generated.rs` | 生成声明及传输代码本轮不计入人工维护源码覆盖；引用它们的关系可能出现解析缺口，不能隐去这种影响 |
| `tests/`、`test/`、`__tests__/`、`*.test.ts(x)`、`*.spec.ts(x)` | 独立测试源码不作为生产图范围，不执行测试 |
| `examples/`、`crates/winwincode-test-assets/`、`test_support.rs`、`*_tests.rs` | 示例、测试资产及专用测试支持不计入生产实现 |
| `build.rs` | Rust 构建脚本不作为生产运行调用图，本次不触发宏生成或编译 |
| `scripts/` | 构建、发布、检查等开发工具源码不计入本次生产图；这属于已声明的范围取舍，不声称全仓库脚本功能已覆盖 |
| `.git/`、`.beads/`、`.agents/`、`.codex/`、本地工具/虚拟环境目录 | 仓库管理与工具数据不作为目标生产源码 |

部分生产 Rust 文件含 `#[cfg(test)]` 内联模块，路径排除不能切掉这类模块。当前 Rust 前端保留其声明，并标注 `cfg_test` / `conditional_definition`，相关调用保持未知；它不猜实际活动构建配置。图节点总量因此不能直接解释为生产函数覆盖，需单独说明这些条件声明。其他 `cfg`、trait 分派和宏展开也不能凭源码猜测运行活动状态。

配置单文件上限为 4 MiB。若仍有超过上限、无法读取或解析失败的文件，应作为诊断保留并在结果中说明；不把被跳过内容当作已分析。

## 工作区与 crate 映射依据

TypeScript `analysis.module_aliases` 由 `pnpm-workspace.yaml` 和工作区 `package.json` 的名称/exports 对照已存在源码入口，明确映射 `@winwincode/browser-core/query-cache`、`@winwincode/browser-core/scope-context`、`@winwincode/browser-ui`、`@winwincode/control-plane-client`、`@winwincode/contracts`、`@winwincode/contracts/browser-control`、`@winwincode/strongflow`、`@winwincode/client`。

其中 browser-core manifest 只有两个公开子路径，本配置不虚构其不存在的根入口。其余入口映射到各包 `src/index.ts`，没有运行构建来解析 `dist`。ESM 的相对 `.js` 导入，应按实际存在的 `.ts`/`.tsx` 来源进行静态绑定。

Rust `analysis.rust_crates` 来自每个项目 `Cargo.toml` 的 package/lib 名称，将导入名的连字符规范为下划线。例如 `winwincode_kernel` 对应 `crates/kernel`，`winwincode_kernel_helper` 对应 `crates/helper`，`winwincode_cli` 对应 `crates/winwincode-cli`。35 份本地 crate manifest 均已映射，8 个 TypeScript 别名的源码入口均在磁盘存在；这里只核对静态文本与文件，不运行 manifest 命令。映射值是项目内 crate 根目录，不包含任何第三方 crate 路径。被排除的测试资产 crate 即使保留 manifest 映射也不恢复其源码覆盖。

## 10 项源码关系基准

以下全部是**当前源码中可定位的关系核对项**，不是新增项目规范。规则 ID 使用 `baseline-wwc-*`，严重度为 `info`；若未重现这些关系，应先检查 CallScope 前端、作用域、导入映射和分析范围，不能直接把工具发现当成 WinWinCode 功能缺陷。

节点格式为 `ts:<相对文件去扩展名>#<词法限定名>` 或 `rust:<同>#<限定名>`，模块节点前缀为 `module:`。文件身份不能因函数同名而丢失。

| ID 后缀 | 源 → 目标 | 原始源码依据 | 需要核对的解析能力 |
|---|---|---|---|
| `ts-scope-selection` | `ts:packages/browser-core/src/scope-context#resolveScopeContext` → 同文件 `scopeSelectionFromHash` | `scope-context.ts:217` 声明，`:222` 调用，`:184` 目标声明 | 同文件显式函数调用 |
| `ts-surface-hash` | `ts:packages/browser-core/src/scope-context#surfaceHash` → 同文件 `scopeHash` | `scope-context.ts:271–272`，目标声明 `:197` | 同文件调用，不判断 URL 业务语义 |
| `ts-auth-format` | `ts:apps/client/src/auth-page#statusText` → `ts:apps/client/src/format-instant#formatInstant` | `auth-page.ts:3` 导入、`:35` 调用；`format-instant.ts:9` 声明 | 相对 ESM `.js` 路径到源码绑定 |
| `ts-workspace-path` | `ts:apps/client/src/application#mountWinWinCodeClient.diagnosticScope` → `resolveScopeContext` → `scopeSelectionFromHash` | `application.ts:58–66` 工作区导入，`:356–363` 调用；`scope-context.ts:222` 第二跳 | 嵌套词法限定名、包子路径别名、两跳路径 |
| `ts-nested-import` | `ts:packages/browser-ui/src/status-badge#mountStatusBadge.update` → `ts:packages/browser-ui/src/mounted-view#assertMounted` | `status-badge.ts:3` 导入、`:46–47` 调用；`mounted-view.ts:9` 声明 | 嵌套函数与相对导入 |
| `rust-canonical-id` | `rust:crates/winwincode-domain/src/lib#is_canonical_delivery_id` → 同文件 `is_canonical_prefixed_id` | `domain/src/lib.rs:25–26` 调用，`:32` 目标声明 | Rust 自由函数同文件调用 |
| `rust-local-function` | `rust:crates/winwincode-device-client/src/connect_code#generate_connect_code` → 同文件 `random_digits` | `connect_code.rs:190–192` 调用，`:204` 目标声明 | 自由函数、`?` 表达式中的调用 |
| `rust-module-use` | `rust:crates/winwincode-device-client/src/connect_code#publish_connect_code` → `rust:crates/winwincode-device-client/src/identity#generate_prefixed_id` | `connect_code.rs:35` 导入、`:292` 调用；`identity.rs:638` 声明 | `crate::identity` 跨模块 `use` 解析 |
| `rust-crate-root` | `rust:crates/winwincode-device-client/src/connect_code#rfc3339` → `rust:crates/winwincode-device-client/src/lib#canonical_rfc3339` | `connect_code.rs:484–485` 调用，`lib.rs:104` 声明 | `crate::` 根函数绑定 |
| `rust-binary-library` | `rust:crates/winwincode-cli/src/main#main` → `rust:crates/winwincode-cli/src/launcher#default_state_root` | `main.rs:1/4` 导入与调用；`lib.rs:22` 重导出；`launcher.rs:274` 声明 | 包规范导入名、同包 binary 到 lib、显式重导出 |

`rust-binary-library` 中的 `default_state_root` 读取环境变量只是目标函数的源码内容。本次没有调用它，也没有读取它所查找的状态目录。

所有基准均检查显式静态连接，不证明调用会在任意输入下发生，也不证明它们的输出、业务规则、安全性质或功能结果。所选路径存在，不代表其他调用或功能完整。

## 最终快照与逐项结果

本次结果绑定快照 `6819e89b03661687e4e7c56654c20cd69f23a4c573bc218ae834eb82e41ee1e5`，生成时间为 `2026-10-11T11:03:21.991714+00:00`。分析器为 `static-multilang-2`，检测器为 `call-rules-2`，模型版本为 `1`。TypeScript 前端为 `typescript-tree-sitter-call-1`，Rust 前端为 `rust-tree-sitter-1.3`；工具使用 Tree-sitter `0.25.2`、TypeScript 语法库 `0.23.2`、Rust 语法库 `0.24.0` 和 CPython `3.12.14`。组件身份已进入快照版本信息。

可直接阅读 [快照摘要](winwincode-summary.json) 与 [规则逐项见证](winwincode-rule-witnesses.json)。见证保存边 ID、节点 ID、源码行和源文件哈希，均来自这次快照；不能拿以后改变的工作区源码替代这些证据。完整产物为 [静态快照](winwincode-snapshot.json)。

| 语言前端 | 选入文件 | 完整语法解析 | 未完整解析 | 节点 | 调用边 |
|---|---:|---:|---:|---:|---:|
| Python | 0 | 0 | 0 | 0 | 0 |
| TypeScript / JS-family | 120 | 114 | 6 | 2,470 | 9,235 |
| Rust | 351 | 345 | 6 | 29,471 | 160,941 |
| 合计 | 471 | 459 | 12 | 31,941 | 170,176 |

Python 文件数为零只是本次范围没有选入 Python 实现。Rust 已实际分析，未用前端文件数量替代全项目范围。语法解析数量不是语义覆盖或功能正确率。

| 语言前端 | 确定内部调用 | 外部调用 | 动态调用 | 歧义调用 | 未绑定调用 |
|---|---:|---:|---:|---:|---:|
| TypeScript / JS-family | 3,673 | 1,566 | 3,967 | 4 | 25 |
| Rust | 12,684 | 22,703 | 124,110 | 48 | 1,396 |

外部调用作为模型边界；其中识别到的回调边界另有不确定性。大量动态调用反映对象、trait、闭包、宏及其他未建模关系，不能按调用名字猜出实现，也不能解释成大量代码错误。Rust 前端记录 1,776 个条件声明，其中 1,512 个节点标有 `cfg_test`；这些文本没有执行，且节点总量不等于活动生产函数数量。

| 基准 ID 后缀 | 最终核对结果 | 快照见证 |
|---|---|---|
| `ts-scope-selection` | 确定直接调用已重现 | `scope-context.ts:222`，与人工源码依据一致 |
| `ts-surface-hash` | 确定直接调用已重现 | `scope-context.ts:272` |
| `ts-auth-format` | 确定直接调用已重现 | `auth-page.ts:35`，目标为 `format-instant.ts` 的函数 |
| `ts-workspace-path` | `uncertain`；未重现完整路径 | `application.ts` 未完整解析，源端点未进入图；保留 `scopeSelectionFromHash` 目标 |
| `ts-nested-import` | 确定直接调用已重现 | `status-badge.ts:47`，源限定名包含 `mountStatusBadge.update` |
| `rust-canonical-id` | 确定直接调用已重现 | `domain/src/lib.rs:26` |
| `rust-local-function` | 确定直接调用已重现 | `connect_code.rs:192` |
| `rust-module-use` | 确定直接调用已重现 | `connect_code.rs:292`，目标为 `identity.rs` 的函数 |
| `rust-crate-root` | 确定直接调用已重现 | `connect_code.rs:485`，目标为 crate 根 `lib.rs` 的函数 |
| `rust-binary-library` | 确定直接调用已重现 | `main.rs:4`，经 lib 重导出绑定到 `launcher.rs` |

9 条确定关系均已对照保存的边和源码见证逐项核对，而不是仅凭“没有规则发现”推断成立。部分源函数仍有其他未知出边；一条确定连接不会让整个函数变成完整分析。

唯一基准规则发现为 `finding:672eec2bc315d47cd7bad349af8f78db`，类型 `required_path`、严重度 `info`、状态 `uncertain`。`application.ts:966` 使用 `let project: import('./chat-page.js').ChatPageOptions['project']`；固定语法库在此生成缺失分号节点，前端独立核对将这个特定现象归为语法库覆盖缺口。CallScope 保留整个文件的 `parse_error`，没有把人工确认的调用补成确定边。这会影响客户端组合入口分析，是工具当前的重要限制，不是 WinWinCode 缺少这条调用的证据。

## 12 个未完整解析文件

下表逐项保留诊断位置。`parse_error` 是 CallScope 语法前端的解析状态，不能直接等同于目标编译器确认的语法错误。除上述 `application.ts` 特定覆盖缺口外，本轮未将其余报错根因判定为目标语法错误或已确认的语法库问题；不对它们作“源码合法”或“仓库有错”的绝对结论。

| 文件 | 诊断行 | 已知事实与结论边界 |
|---|---|---|
| `apps/client/src/application.ts` | 966 | inline `import(...)` 类型处的缺失分号节点；已确认的工具覆盖缺口 |
| `apps/client/src/candidate-run-preview-control-plane.ts` | 325、333 | 语法库报告 `ERROR` / 缺失分号；目标语法错误未确认 |
| `apps/client/src/community-control-plane-client.ts` | 2935、2946 | 语法库报告 `ERROR`；目标语法错误未确认 |
| `apps/client/src/home-recent-visits.ts` | 135 | 语法库报告 `ERROR`；目标语法错误未确认 |
| `apps/client/src/readiness-view-model.ts` | 473、482、576 | 语法库报告 `ERROR`；目标语法错误未确认 |
| `schema/winwincode-export/v1/validate.js` | 288 | JS-family 输入的语法库报告 `ERROR`；目标语法错误未确认 |
| `crates/winwincode-execution-port/src/diagnostic_parser.rs` | 971 | Rust 语法库报告错误/缺失节点；目标语法错误未确认 |
| `crates/winwincode-server/src/worker_session_credentials.rs` | 497 | Rust 语法库报告错误/缺失节点；目标语法错误未确认 |
| `crates/winwincode-storage/src/provider_exchange.rs` | 1577 | Rust 语法库报告错误/缺失节点；目标语法错误未确认 |
| `crates/winwincode-worker/src/managed_session.rs` | 577 | Rust 语法库报告错误/缺失节点；目标语法错误未确认 |
| `crates/winwincode-worker/src/probe_evidence.rs` | 1818 | Rust 语法库报告错误/缺失节点；目标语法错误未确认 |
| `crates/winwincode-worker/src/probe_scheduler.rs` | 1080 | Rust 语法库报告错误/缺失节点；目标语法错误未确认 |

统一编排器不会将这些文件的调用或端点作为确定连接见证。Rust 可保留可识别的局部结构，但这不使文件成为完整分析；未解析区域继续影响相关规则判断。不能通过删去失败文件改善“覆盖率”。

快照另记录 53 处实际排除路径，包含目录条目而非 53 个文件；完整列表在摘要的 `stats.excluded_paths`。没有扫描读取异常，未支持文件列表为空，符号链接 `CLAUDE.md` 被跳过。被排除的生成源码仍造成明确的 Rust 模块缺口，例如 API、domain 和 execution-port 的 `generated` 模块，不假装其依赖已解析。

## 发现数量的含义

最终保存 137,895 条发现：129,618 条 `unresolved_call`、8,263 条 `external_callback_boundary`、1 条上述不确定必需路径，以及 4 个调用环和 9 个自调用结构事实。前两类主要记录分析未知，调用环/自调用不证明不终止；这些数量都不是架构缺陷数。

本次没有作者批准的功能规格约束，因此不能用这些发现对 WinWinCode 作功能通过或不通过的裁决。人工选取的 10 项源码关系也不是随机样本、缺陷全集或功能清单，不计算检出率、误报率或全项目功能覆盖率。

## 项目规范与未覆盖边界

仓库 `AGENTS.md` 明确 DSH/StrongFlow 共用一个嵌入式 Codex Core 内核，并禁止回退到已安装 Codex CLI 或另一编程代理。这是作者声明的架构意图；本次 10 条关系基准没有将它偷换成已验证约束。未找到足够精确的纯调用图规则之前，不声称证明整个仓库符合该意图。

入口、React/DOM 回调、接口注入、Rust trait/对象方法、宏生成、传输注册及 TS↔Rust 通信关系都可能超出当前显式调用前端。`application.ts` 包含注入对象和事件订阅，Rust integration framework 使用 `dyn` ports；这些不能因方法名称相同就解析到某个唯一实现。

配置 `entrypoints=[]`，不从本次选择的基准函数推断全仓库死代码。配置未增加禁止规则，也未为源码中没有承诺的调用顺序或行为自设要求。

## 再分析与阅读方式

原始扫描、摘要和见证均保存在 CallScope 工具目录，目标仓库保持只读。新增前端语法库、模块映射或解析版本变化后，应保存新的快照身份，并对照原始源码关系重新核对；不能覆盖旧证据。

当前系统已能解释这 9 条明确静态连接，但客户端组合入口的解析失败、未知分派及生成源码范围缺口仍阻止“代码功能完整”的结论。继续完善应优先处理这些前端与静态契约能力，而不是从图的大小推断成熟度。跨语言运行通信、执行顺序、分支、参数及结果仍不在本系统的证明范围内。

本报告没有执行目标代码，没有运行任何测试套件、编译、构建或 E2E 流程，也没有性能或“测试通过”结论。
