# n0vel：自动静态分析报告

快照：`3b37d1364b982bf3ddde3ff89db3b3d426a8b40b25dae818d9070b68cf8ace7c`；仅使用保存源码、图和静态分析证据，未执行目标、测试或构建。

## 主要发现

此快照没有配置完整条件判断；不从结构规模推断功能正确。

原始完整 JSON 保留所有条件、反证、未知项、source facts 和保存发现身份。以下限制仅影响展示，不改变分析结果。

## 具体职责与接口交接

以下正文由所选声明的实际记录字段、赋值、实参接口和提前退出条件生成。目录名只供导航；普通调用、消息字段、执行、交付和投影分别保留。

当前没有可认证的具体职责解释；结构盘点不能代替职责结论。

## 主要功能链、条件与反证

源码顺序只描述同一次调用正常到达的关系；异步完成、消息传输、远端响应和物理持久化均以实际证据范围为准。

## 捕获范围与未审边界

选入 29 份源码，解析 6 份。这是源码捕获与语法解析范围，不能换算成功能完整率。

| 区域 | 文件 | 已解析 |
| --- | --- | --- |
| artifacts/sample_chapters | 1 | 1 |
| docs/assets | 1 | 1 |
| linux/flutter | 2 | 0 |
| linux/runner | 3 | 0 |
| macos/Flutter | 1 | 0 |
| macos/Runner | 2 | 0 |
| macos/RunnerTests | 1 | 0 |
| scripts | 8 | 4 |
| windows/flutter | 2 | 0 |
| windows/runner | 8 | 0 |

项目声明与依赖：`/project_declarations`；已绑定跨目录图引用：`/architecture/dependencies`。声明存在、路径可达和依赖计数均不证明业务行为通过。

- `linux/flutter/generated_plugin_registrant.cc`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `linux/flutter/generated_plugin_registrant.h`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `linux/runner/main.cc`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `linux/runner/my_application.cc`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `linux/runner/my_application.h`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `macos/Flutter/GeneratedPluginRegistrant.swift`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `macos/Runner/AppDelegate.swift`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `macos/Runner/MainFlutterWindow.swift`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `macos/RunnerTests/RunnerTests.swift`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `scripts/macos_clang_wrapper.sh`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `scripts/macos_flutter_assemble.sh`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `scripts/package_macos_preview.sh`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `scripts/verify_macos.sh`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `windows/flutter/generated_plugin_registrant.cc`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `windows/flutter/generated_plugin_registrant.h`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `windows/runner/flutter_window.cpp`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `windows/runner/flutter_window.h`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `windows/runner/main.cpp`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `windows/runner/resource.h`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `windows/runner/utils.cpp`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `windows/runner/utils.h`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `windows/runner/win32_window.cpp`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `windows/runner/win32_window.h`：unsupported；此源码语言不在当前分析能力或配置范围中。

配置排除：`[".git",".venv","venv","__pycache__","node_modules",".callscope","build","dist"]`。

所选局部分析：`/configured_local_assessments`；完整诊断：`/diagnostics`。未建模域保持未审，不保证全仓库无缺陷、所有权或授权完整，也不将未知标为通过。

报告生成组件：`/report_components`；原快照分析组件：`/snapshot/component_versions`。两者分别保存，历史发现不会因生成新版报告而升级。

