# target：自动静态分析报告

快照：`7165ea038f8a8783b2f1a0c8f0075d9cd84e784ebde6a9f84c10e850076b7dea`；仅使用保存源码、图和静态分析证据，未执行目标、测试或构建。

## 主要发现

此快照没有配置完整条件判断；不从结构规模推断功能正确。

原始完整 JSON 保留所有条件、反证、未知项、source facts 和保存发现身份。以下限制仅影响展示，不改变分析结果。

## 具体职责与接口交接

以下正文由所选声明的实际记录字段、赋值、实参接口和提前退出条件生成。目录名只供导航；普通调用、消息字段、执行、交付和投影分别保留。

当前没有可认证的具体职责解释；结构盘点不能代替职责结论。

## 主要功能链、条件与反证

源码顺序只描述同一次调用正常到达的关系；异步完成、消息传输、远端响应和物理持久化均以实际证据范围为准。

## 捕获范围与未审边界

选入 927 份源码，解析 881 份。这是源码捕获与语法解析范围，不能换算成功能完整率。

### 语言、文件状态与发现范围

以下使用快照保存的统计与能力登记。注册语言、前端可用、语法解析和功能验证分别记录；没有保存的字段保持未知，不使用当前环境补写历史结果。

`parsed` 表示语法解析完成；`captured_metadata` 仅有文件或元数据；`structural_extracted` 表示已有结构提取但未建立完整嵌入语法校验；`parse_error` 表示解析或前端失败，保留的结构只能作为局部证据。

| 保存状态 | 文件数 |
| --- | --- |
| captured_metadata | 7 |
| parse_error | 35 |
| parsed | 881 |
| unsupported | 4 |

| 语言 | 文件 | parsed | captured_metadata | structural_extracted | parse_error | 全部状态 | 节点 | 图引用 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arkts | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| astro | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| c | 5 | 2 | 0 | 0 | 3 | {"parse_error":3,"parsed":2} | 10 | 2 |
| cfml | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| cfquery | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| cfscript | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| cobol | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| cpp | 10 | 5 | 0 | 0 | 5 | {"parse_error":5,"parsed":5} | 97 | 200 |
| csharp | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| dart | 891 | 864 | 0 | 0 | 27 | {"parse_error":27,"parsed":864} | 18943 | 94335 |
| erlang | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| go | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| java | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| kotlin | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| liquid | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| lua | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| luau | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| nix | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| objc | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| pascal | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| php | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| properties | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| python | 5 | 5 | 0 | 0 | 0 | {"parsed":5} | 37 | 262 |
| r | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| razor | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| ruby | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| rust | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| scala | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| shell | 4 | 0 | 0 | 0 | 0 | {"unsupported":4} | 未保存 | 未保存 |
| solidity | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| svelte | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| swift | 4 | 4 | 0 | 0 | 0 | {"parsed":4} | 25 | 32 |
| terraform | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| twig | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| typescript | 1 | 1 | 0 | 0 | 0 | {"parsed":1} | 7 | 20 |
| vbnet | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| vue | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| xml | 0 | 0 | 0 | 0 | 0 | {} | 0 | 0 |
| yaml | 7 | 0 | 7 | 0 | 0 | {"captured_metadata":7} | 7 | 0 |

完整语言统计：`/stats/by_language`；逐语言实际文件状态：`/coverage/file_statuses_by_language`。旧统计字段 `files_failed` 包含所有非 parsed 状态，不能把元数据捕获或结构提取一概解释为解析错误。

| 语言 | 前端 | 已注册 | 可用值 / 检查状态 | 项目验证状态 | 能力层次 |
| --- | --- | --- | --- | --- | --- |
| python | native | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | bounded_static_relations |
| typescript | native | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | bounded_static_relations |
| rust | native | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | bounded_static_relations |
| arkts | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| go | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| java | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| c | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| cpp | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| csharp | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| razor | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| php | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| ruby | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| swift | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| kotlin | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| dart | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| svelte | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| vue | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| astro | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| liquid | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| pascal | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| scala | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| lua | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| luau | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| objc | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| r | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| solidity | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| nix | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| yaml | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | file_or_metadata |
| twig | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | file_or_metadata |
| xml | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | file_or_metadata |
| properties | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | file_or_metadata |
| cfml | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| cfscript | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| cfquery | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| cobol | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| vbnet | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| erlang | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |
| terraform | codegraph | true | {"available":null,"status":"runtime_not_checked"} | not_validated_for_this_project | structural_extraction |

完整登记（含扩展名与上游版本）：`/stats/language_capabilities`。登记或一次结构提取不表示该语言的全部语法和功能已经验证。

文件清单：发现普通文件 `1075`；识别为源码 `927`；未识别 148。完整保存值：`/stats/file_inventory`。

| 未识别文件示例（最多 24） | 扩展名 | 完整记录 |
| --- | --- | --- |
| .gitignore |  | /stats/file_inventory/unrecognized_files/0 |
| .metadata |  | /stats/file_inventory/unrecognized_files/1 |
| AGENTS.md | .md | /stats/file_inventory/unrecognized_files/2 |
| FLOW.md | .md | /stats/file_inventory/unrecognized_files/3 |
| Makefile |  | /stats/file_inventory/unrecognized_files/4 |
| README.md | .md | /stats/file_inventory/unrecognized_files/5 |
| agent-experience/index.jsonl | .jsonl | /stats/file_inventory/unrecognized_files/6 |
| artifacts/real_validation/three_chapter_repaired/README.md | .md | /stats/file_inventory/unrecognized_files/7 |
| artifacts/real_validation/three_chapter_repaired/chapters/chapter-01.md | .md | /stats/file_inventory/unrecognized_files/8 |
| artifacts/real_validation/three_chapter_repaired/chapters/chapter-02.md | .md | /stats/file_inventory/unrecognized_files/9 |
| artifacts/real_validation/three_chapter_repaired/chapters/chapter-03.md | .md | /stats/file_inventory/unrecognized_files/10 |
| artifacts/real_validation/three_chapter_repaired/manifest.json | .json | /stats/file_inventory/unrecognized_files/11 |
| artifacts/real_validation/three_chapter_repaired/outline/three_chapter_outline.md | .md | /stats/file_inventory/unrecognized_files/12 |
| artifacts/real_validation/three_chapter_repaired/reports/deterministic-repair-audit.json | .json | /stats/file_inventory/unrecognized_files/13 |
| artifacts/real_validation/three_chapter_repaired/reports/deterministic-repair-audit.md | .md | /stats/file_inventory/unrecognized_files/14 |
| artifacts/real_validation/three_chapter_repaired/reports/production-pre-quality-evidence.json | .json | /stats/file_inventory/unrecognized_files/15 |
| artifacts/real_validation/three_chapter_run/chapters/chapter-01.md | .md | /stats/file_inventory/unrecognized_files/16 |
| artifacts/real_validation/three_chapter_run/chapters/chapter-02.md | .md | /stats/file_inventory/unrecognized_files/17 |
| artifacts/real_validation/three_chapter_run/chapters/chapter-03.md | .md | /stats/file_inventory/unrecognized_files/18 |
| artifacts/real_validation/three_chapter_run/outline/three_chapter_outline.md | .md | /stats/file_inventory/unrecognized_files/19 |
| artifacts/real_validation/three_chapter_run/reports/quality-report.json | .json | /stats/file_inventory/unrecognized_files/20 |
| artifacts/real_validation/three_chapter_run/reports/quality-report.md | .md | /stats/file_inventory/unrecognized_files/21 |
| artifacts/sample_chapters/qidian_main/01_xuanhuan.md | .md | /stats/file_inventory/unrecognized_files/22 |
| artifacts/sample_chapters/qidian_main/02_qihuan.md | .md | /stats/file_inventory/unrecognized_files/23 |

文件清单记录扫描范围内的路径；未识别文件没有因此获得源码解析或功能覆盖。

### CodeGraph 保存的结构与候选关系

真实保存节点 19082；候选调用类站点 39508；未绑定站点 55061；候选目标关系 39508。

调用类站点包括调用、实例化和函数引用，具体类别保留在 relation_kind。这些关系只提供候选，不升级为确定调用或功能完成。confidence 是启发式排序分数，不是正确概率。

| 节点类型 | 保存数量 |
| --- | --- |
| class | 1868 |
| constant | 1094 |
| enum | 195 |
| enum_member | 926 |
| function | 3006 |
| import | 5373 |
| method | 5658 |
| module | 917 |
| struct | 3 |
| type_alias | 42 |

| 真实节点示例 | 源码位置 | 类型 | 完整节点 ID |
| --- | --- | --- | --- |
| generated_plugin_registrant.h | linux/flutter/generated_plugin_registrant.h:1 | module | cg:c:file:linux/flutter/generated_plugin_registrant.h |
| my_application.h | linux/runner/my_application.h:1 | module | cg:c:file:linux/runner/my_application.h |
| generated_plugin_registrant.h | windows/flutter/generated_plugin_registrant.h:1 | module | cg:c:file:windows/flutter/generated_plugin_registrant.h |
| resource.h | windows/runner/resource.h:1 | module | cg:c:file:windows/runner/resource.h |
| utils.h | windows/runner/utils.h:1 | module | cg:c:file:windows/runner/utils.h |
| vector | windows/runner/utils.h:5 | import | cg:c:import:50fcfdf940adaaf81ca91d63fa41a41f |
| gtk/gtk.h | linux/runner/my_application.h:4 | import | cg:c:import:51490c8d8f8e69e3a8a82fcc1d4d2bcf |
| flutter_linux/flutter_linux.h | linux/flutter/generated_plugin_registrant.h:10 | import | cg:c:import:53656577b253f52cbed39da8bb6a03c7 |
| string | windows/runner/utils.h:4 | import | cg:c:import:8fc649967821c48317be4b35ca8324ce |
| flutter/plugin_registry.h | windows/flutter/generated_plugin_registrant.h:10 | import | cg:c:import:d4980aa63d2b825ee5e93e9852a59e58 |
| FlutterWindow | windows/runner/flutter_window.h:12 | class | cg:cpp:class:0f8e91898116242da89b2df17f84e7c4 |
| WindowClassRegistrar | windows/runner/win32_window.cpp:59 | class | cg:cpp:class:b9739a6128c7210a9bcdea98d5861cf2 |

最多展示 24 个保存站点，每站点最多 8 个候选目标；按快照顺序取样，并在两类均存在时保留候选与未绑定示例，不代表覆盖率。完整边使用本报告快照 ID 与下列完整 edge_id 定位，完整表达式与候选仍保留在图中。

| 保存表达式 | 源码位置 | 类别 / 保存状态 | 候选数 | 完整 edge_id | 报告样例引用 |
| --- | --- | --- | --- | --- | --- |
| WidgetsFlutterBinding.ensureInitialized | lib/agent_evaluation_private_holdout_runtime.dart:20 | {"kind":"calls","resolution":"dynamic"} | 0 | edge:cg:10972861529968aa9e5e00b3f4ec | /codegraph_candidate_evidence/examples/0 |
| StateError | lib/agent_evaluation_private_holdout_runtime.dart:23 | {"kind":"calls","resolution":"dynamic"} | 0 | edge:cg:199f1b6a301e27a265a0cee6880b | /codegraph_candidate_evidence/examples/1 |
| trim | lib/agent_evaluation_private_holdout_runtime.dart:26 | {"kind":"calls","resolution":"dynamic"} | 0 | edge:cg:5d018c6f7b53be2683acdd46247e | /codegraph_candidate_evidence/examples/2 |
| trim | lib/agent_evaluation_private_holdout_runtime.dart:26 | {"kind":"calls","resolution":"dynamic"} | 0 | edge:cg:d815aa0c3ed7abb25414f6d3c8c0 | /codegraph_candidate_evidence/examples/3 |
| trim | lib/agent_evaluation_private_holdout_runtime.dart:26 | {"kind":"calls","resolution":"dynamic"} | 0 | edge:cg:db3b076c2bf05444898492d7e47d | /codegraph_candidate_evidence/examples/4 |
| StateError | lib/agent_evaluation_private_holdout_runtime.dart:27 | {"kind":"calls","resolution":"dynamic"} | 0 | edge:cg:25f198d8f711577a3977dbd73393 | /codegraph_candidate_evidence/examples/5 |
| StateError | lib/agent_evaluation_private_holdout_runtime.dart:27 | {"kind":"calls","resolution":"dynamic"} | 0 | edge:cg:70341ef496f509ecdf919e26c5c5 | /codegraph_candidate_evidence/examples/6 |
| StateError | lib/agent_evaluation_private_holdout_runtime.dart:27 | {"kind":"calls","resolution":"dynamic"} | 0 | edge:cg:71fa74b82b3f64180ce40feb49d1 | /codegraph_candidate_evidence/examples/7 |
| agentEvaluationRealReleaseConfigurationFromEnvironment | lib/agent_evaluation_private_holdout_runtime.dart:32 | {"kind":"calls","resolution":"ambiguous"} | 1 | edge:cg:3714a884cd13cb388c53b1e5fe86 | /codegraph_candidate_evidence/examples/8 |
| value | lib/agent_evaluation_private_holdout_runtime.dart:33 | {"kind":"calls","resolution":"ambiguous"} | 1 | edge:cg:e3eeb6ed59afc4928f279bf06b5c | /codegraph_candidate_evidence/examples/9 |
| base64Decode | lib/agent_evaluation_private_holdout_runtime.dart:38 | {"kind":"calls","resolution":"dynamic"} | 0 | edge:cg:b92397641020d95f3e46b40d3764 | /codegraph_candidate_evidence/examples/10 |
| value | lib/agent_evaluation_private_holdout_runtime.dart:39 | {"kind":"function_ref","resolution":"ambiguous"} | 1 | edge:cg:7abec824e6368ad4ade790ea262c | /codegraph_candidate_evidence/examples/11 |
| value | lib/agent_evaluation_private_holdout_runtime.dart:39 | {"kind":"function_ref","resolution":"ambiguous"} | 1 | edge:cg:eae10b481bcd91a0cc525b389dbe | /codegraph_candidate_evidence/examples/12 |
| value | lib/agent_evaluation_private_holdout_runtime.dart:39 | {"kind":"calls","resolution":"ambiguous"} | 1 | edge:cg:a5268e15f45dcba68360d9e65011 | /codegraph_candidate_evidence/examples/13 |
| jsonDecode | lib/agent_evaluation_private_holdout_runtime.dart:41 | {"kind":"calls","resolution":"dynamic"} | 0 | edge:cg:c65cbeb14f6e1a78f767aa635b92 | /codegraph_candidate_evidence/examples/14 |
| value | lib/agent_evaluation_private_holdout_runtime.dart:42 | {"kind":"calls","resolution":"ambiguous"} | 1 | edge:cg:47b7cb106a5e9581d4e59f121cc9 | /codegraph_candidate_evidence/examples/15 |
| int.tryParse | lib/agent_evaluation_private_holdout_runtime.dart:44 | {"kind":"calls","resolution":"dynamic"} | 0 | edge:cg:4d7c0aa6b096af72a214be0797e0 | /codegraph_candidate_evidence/examples/16 |
| value | lib/agent_evaluation_private_holdout_runtime.dart:45 | {"kind":"calls","resolution":"ambiguous"} | 1 | edge:cg:045dc802166419dd7268b8cfbaf0 | /codegraph_candidate_evidence/examples/17 |
| argumentsDecoded.any | lib/agent_evaluation_private_holdout_runtime.dart:49 | {"kind":"calls","resolution":"dynamic"} | 0 | edge:cg:d341ecca8da2b7b2adfb02ed5d27 | /codegraph_candidate_evidence/examples/18 |
| StateError | lib/agent_evaluation_private_holdout_runtime.dart:51 | {"kind":"calls","resolution":"dynamic"} | 0 | edge:cg:8a4c9fc76cda1eeaf26e4d14bd65 | /codegraph_candidate_evidence/examples/19 |
| trim | lib/agent_evaluation_private_holdout_runtime.dart:54 | {"kind":"calls","resolution":"dynamic"} | 0 | edge:cg:d4640bafbb8e494c14f1f25fd3ec | /codegraph_candidate_evidence/examples/20 |
| AgentEvaluationExternalCustodyTrustRegistry.production | lib/agent_evaluation_private_holdout_runtime.dart:56 | {"kind":"calls","resolution":"ambiguous"} | 1 | edge:cg:0b070a73966b25550ec53cd6a2d1 | /codegraph_candidate_evidence/examples/21 |
| AgentEvaluationExternalCustodyAttestationPayload.fromCanonicalJson | lib/agent_evaluation_private_holdout_runtime.dart:58 | {"kind":"calls","resolution":"ambiguous"} | 1 | edge:cg:3157c16412722b6d192e4f07e27b | /codegraph_candidate_evidence/examples/22 |
| value | lib/agent_evaluation_private_holdout_runtime.dart:59 | {"kind":"calls","resolution":"ambiguous"} | 1 | edge:cg:d3a67e30faed653dc64012e0f5f0 | /codegraph_candidate_evidence/examples/23 |

| 站点 edge_id | 候选目标 | 候选位置 | 上游启发式排序 | 完整候选记录 |
| --- | --- | --- | --- | --- |
| edge:cg:3714a884cd13cb388c53b1e5fe86 | {"name":"agentEvaluationRealReleaseConfigurationFromEnvironment","node_id":"cg:dart:function:df02e933c51faef8851dd5b67fa3eaae"} | lib/features/story_generation/data/evaluation/agent_evaluation_private_holdout_runner.dart:402 | [{"confidence":0.9,"resolved_by":"exact-match"}] | /codegraph_candidate_evidence/examples/8/targets/0 |
| edge:cg:e3eeb6ed59afc4928f279bf06b5c | {"name":"value","node_id":"cg:dart:function:5983fdc87184e2d0cea8488b30f734c9"} | lib/agent_evaluation_private_holdout_runtime.dart:25 | [{"confidence":0.9,"resolved_by":"exact-match"}] | /codegraph_candidate_evidence/examples/9/targets/0 |
| edge:cg:7abec824e6368ad4ade790ea262c | {"name":"value","node_id":"cg:dart:function:5983fdc87184e2d0cea8488b30f734c9"} | lib/agent_evaluation_private_holdout_runtime.dart:25 | [{"confidence":0.9,"resolved_by":"function-ref"}] | /codegraph_candidate_evidence/examples/11/targets/0 |
| edge:cg:eae10b481bcd91a0cc525b389dbe | {"name":"value","node_id":"cg:dart:function:5983fdc87184e2d0cea8488b30f734c9"} | lib/agent_evaluation_private_holdout_runtime.dart:25 | [{"confidence":0.9,"resolved_by":"function-ref"}] | /codegraph_candidate_evidence/examples/12/targets/0 |
| edge:cg:a5268e15f45dcba68360d9e65011 | {"name":"value","node_id":"cg:dart:function:5983fdc87184e2d0cea8488b30f734c9"} | lib/agent_evaluation_private_holdout_runtime.dart:25 | [{"confidence":0.9,"resolved_by":"exact-match"}] | /codegraph_candidate_evidence/examples/13/targets/0 |
| edge:cg:47b7cb106a5e9581d4e59f121cc9 | {"name":"value","node_id":"cg:dart:function:5983fdc87184e2d0cea8488b30f734c9"} | lib/agent_evaluation_private_holdout_runtime.dart:25 | [{"confidence":0.9,"resolved_by":"exact-match"}] | /codegraph_candidate_evidence/examples/15/targets/0 |
| edge:cg:045dc802166419dd7268b8cfbaf0 | {"name":"value","node_id":"cg:dart:function:5983fdc87184e2d0cea8488b30f734c9"} | lib/agent_evaluation_private_holdout_runtime.dart:25 | [{"confidence":0.9,"resolved_by":"exact-match"}] | /codegraph_candidate_evidence/examples/17/targets/0 |
| edge:cg:0b070a73966b25550ec53cd6a2d1 | {"name":"production","node_id":"cg:dart:method:42f5617a4ab863eb524b9e63275fa747"} | lib/features/story_generation/data/evaluation/agent_evaluation_external_custody_trust_store.dart:199 | [{"confidence":0.85,"resolved_by":"qualified-name"}] | /codegraph_candidate_evidence/examples/21/targets/0 |
| edge:cg:3157c16412722b6d192e4f07e27b | {"name":"fromCanonicalJson","node_id":"cg:dart:method:cbf51b6a9940cedb6f1cea14950f18d6"} | lib/features/story_generation/data/evaluation/agent_evaluation_spec_evidence.dart:616 | [{"confidence":0.85,"resolved_by":"qualified-name"}] | /codegraph_candidate_evidence/examples/22/targets/0 |
| edge:cg:d3a67e30faed653dc64012e0f5f0 | {"name":"value","node_id":"cg:dart:function:5983fdc87184e2d0cea8488b30f734c9"} | lib/agent_evaluation_private_holdout_runtime.dart:25 | [{"confidence":0.9,"resolved_by":"exact-match"}] | /codegraph_candidate_evidence/examples/23/targets/0 |

非调用关系 99039 条、结构关系 19526 条，保留在节点 metadata.codegraph_relations / metadata.codegraph_structure，未转成调用边。节点定位示例：`/codegraph_candidate_evidence/metadata_owner_examples`；完整汇总与采样上限：`/codegraph_candidate_evidence`。

| 区域 | 文件 | 已解析 |
| --- | --- | --- |
| . | 2 | 0 |
| .github/ISSUE_TEMPLATE | 1 | 0 |
| .github/workflows | 4 | 0 |
| artifacts/sample_chapters | 1 | 1 |
| docs/assets | 1 | 1 |
| lib | 3 | 3 |
| lib/app | 202 | 194 |
| lib/domain | 8 | 6 |
| lib/features | 323 | 310 |
| linux/flutter | 2 | 2 |
| linux/runner | 3 | 0 |
| macos/Flutter | 1 | 1 |
| macos/Runner | 2 | 2 |
| macos/RunnerTests | 1 | 1 |
| scripts | 9 | 5 |
| test | 280 | 277 |
| test/app | 2 | 2 |
| test/contracts | 9 | 9 |
| test/fake | 3 | 3 |
| test/pipeline | 7 | 7 |
| test/test_support | 17 | 17 |
| tool | 36 | 35 |
| windows/flutter | 2 | 1 |
| windows/runner | 8 | 4 |

项目声明与依赖：`/project_declarations`；已绑定跨目录图引用：`/architecture/dependencies`。声明存在、路径可达和依赖计数均不证明业务行为通过。

- `.github/ISSUE_TEMPLATE/author-feedback.yml`：captured_metadata；File/metadata tracking only; this input has no general symbol-level parser。
- `.github/workflows/docs-check.yml`：captured_metadata；File/metadata tracking only; this input has no general symbol-level parser。
- `.github/workflows/flutter-analyze-test.yml`：captured_metadata；File/metadata tracking only; this input has no general symbol-level parser。
- `.github/workflows/verify-macos.yml`：captured_metadata；File/metadata tracking only; this input has no general symbol-level parser。
- `.github/workflows/verify-windows.yml`：captured_metadata；File/metadata tracking only; this input has no general symbol-level parser。
- `analysis_options.yaml`：captured_metadata；File/metadata tracking only; this input has no general symbol-level parser。
- `lib/app/llm/app_llm_call_trace.dart`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `lib/app/llm/app_llm_output_schema.dart`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `lib/app/llm/app_llm_prompt_renderer.dart`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `lib/app/llm/app_llm_providers.dart`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `lib/app/llm/gateway_interceptor.dart`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `lib/app/rag/local_rag_storage.dart`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `lib/app/state/ai_request_service.dart`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `lib/app/state/app_workspace_store.dart`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `lib/domain/json_utils.dart`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `lib/domain/settings.dart`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `lib/features/import_export/data/project_transfer_models.dart`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `lib/features/import_export/data/standard_format_exporter.dart`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `lib/features/story_generation/data/evaluation/agent_evaluation_external_signer.dart`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `lib/features/story_generation/data/evaluation/agent_evaluation_metered_client.dart`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `lib/features/story_generation/data/evaluation/agent_evaluation_typed_evidence.dart`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `lib/features/story_generation/data/generation_ledger.dart`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `lib/features/story_generation/data/generation_ledger_models.dart`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `lib/features/story_generation/data/pipeline_stage_runner_impl.dart`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `lib/features/story_generation/data/roleplay_session_store_io.dart`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `lib/features/story_generation/data/scene_brief_builder.dart`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `lib/features/story_generation/data/story_prompt_templates.dart`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `lib/features/story_generation/domain/outline_plan_models.dart`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `lib/features/workbench/presentation/workbench_shell_actions.dart`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `linux/runner/main.cc`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `linux/runner/my_application.cc`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `linux/runner/my_application.h`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `pubspec.yaml`：captured_metadata；File/metadata tracking only; this input has no general symbol-level parser。
- `scripts/macos_clang_wrapper.sh`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `scripts/macos_flutter_assemble.sh`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `scripts/package_macos_preview.sh`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `scripts/verify_macos.sh`：unsupported；此源码语言不在当前分析能力或配置范围中。
- `test/agent_evaluation_report_test.dart`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `test/real_chapter_generation_commit_gate_test.dart`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `test/repaired_three_chapter_artifact_test.dart`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `tool/real_chain_probe.dart`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `windows/flutter/generated_plugin_registrant.h`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `windows/runner/main.cpp`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `windows/runner/utils.h`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `windows/runner/win32_window.cpp`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。
- `windows/runner/win32_window.h`：parse_error；Upstream grammar has syntax errors; retained structural/candidate evidence is partial。

配置排除：`[".git",".venv","venv","__pycache__","node_modules",".callscope","build","dist"]`。

所选局部分析：`/configured_local_assessments`；完整诊断：`/diagnostics`。未建模域保持未审，不保证全仓库无缺陷、所有权或授权完整，也不将未知标为通过。

报告生成组件：`/report_components`；原快照分析组件：`/snapshot/component_versions`。两者分别保存，历史发现不会因生成新版报告而升级。

