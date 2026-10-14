# 原五项目标实现的独立开发审查

> 职责调整记录：用户随后要求Astra回到两份原分析报告的完整benchmark差距定位，停止重复把关。本文件是此前开发讨论记录，不是当前版本批准门槛；实现验证由root负责，不等待Astra认可。当前对应见 [REPORT_ALIGNMENT_NOTES.md](REPORT_ALIGNMENT_NOTES.md)。

审查人：Astra；日期：2026-10-13。本文是开发中候选的持续审查记录，不是冻结实现或正式结果的最终认可。只读取 CallScope 实现、目标源码和保存的证据；没有执行目标、导入目标模块、运行测试或构建。原五项目标／30项必要义务、原26项基线及旧冻结报告不变。

验收标准见 [FULL_GOAL_REVIEW_PLAN.md](FULL_GOAL_REVIEW_PLAN.md)。`complete_assessment` 与 `full_goal_supported` 分开：完整自动证据可以反驳原 claim，但局部反证、删去分支或未实现传播都不能算完整裁决。

## 当前结论

尚未认可任何本轮候选为完整目标。下面的源码缺段已逐项发给实现者，正在修补。正常数据、标准 DOM／Set／JSON／Promise 或未被外部替换的源码方法可以是有明确范围的受信模型；模型不能代替实际实参绑定、返回值、控制条件、写入点或捕获源码中的可见修改。

## CPB-02：状态生产、投影、谓词及保护

已阅读全文候选 `callscope/status_analysis.py` 的 producer、predicate、projection_origin、consumer、authority、recoverability 与最终 gate，并对照真实 event-materializer、event-store 和 job-store 源码。

1. `projection_origin` 原先仅记录任意组件返回的 origin call，没有要求无 checkpoint 分支实际到所选 materializer、replayed 分支实际到同 handler 表的 advance；reader→projection→readEvents 的同 root/project/job 参数也没有逐层闭合。仅“记录了一些调用位置”不足以支持 S3。作者已同意补实际分支和参数关系。
2. `authority` 原先以任意后续已绑定调用非空代替真正 append 边界，并只保存 allowlist 实参的位置，没有推导实际 incoming event 的 type 经 normalizer 进入 `.has`。需连接 durable append、其数据／文件实参、callback 提前 return 与 outer written 返回；无需证明整个锁运行环境或其他 journal API。
3. `rejecting_guards`／`function_eval` 原先把递归找到的单个 throw／return 当成必达，可能跳过内部 guard、fallthrough 或前置控制。当前目标的直接分支可以用有限 AST 结构闭合；不支持的控制必须留 unknown。
4. S1 需要实际事件形参→循环项→表索引与 handler 实参，并保留状态写入后的同 handler 覆盖检查。仅表成员闭合、同名写入存在和任意 dispatch 不足。
5. 完整比较与原 claim 匹配必须分开。若将来谓词集合改为包含 superseded，完整比较应产生反驳／需收窄及 `full_goal_supported=false`，不能因为所有关系都解析成功而报告 reproduced。

真正需要的业务范围仍是当前普通投影记录、合法非空 jobId、当前 status=superseded。没有要求“发生 superseded 事件以后状态永远不变”；POST_TERMINAL_ALLOWED 中的审批事件实际可以改状态。终态分类差异也不产生自动恢复授权。

## WWC-01：公开入口、装配及拒绝链

已读 `callscope/navigation_completion.py` 全候选和 `port_wiring.py` 的实际返回方法／端口使用摘要，并对照 home-dashboard-page、application、task-entry-page 与 view-model。

1. N1 最初止于看板 formal root，缺 mountMyWorkPage 实际 workRoot→看板 options.root→外层 append→renderHome 生产安装链。实现者正在补 source role locators；这些 locators 只能定位，不能预填链。
2. DOM helper 最初只有“唯一 return”，没有要求普通同步、末尾直接返回；append 图没有要求有效控制位置／顺序。条件 false 的 append、后续 replaceChildren 移除或条件 return 不能形成公开入口证明。
3. N6 最初对 homeSubRoute 的 seed 分支及 activeSurface 的早于 guard 赋值只做位置筛选，缺先行 return／覆盖及支配检查。实际有限直接语句可以自动认证，不需要一般浏览器可达性证明。
4. N4 最初识别任意 `.addEventListener('submit', callback)`，没有关联实际 form 创建与安装；应将真 form 沿 DOM 组合接到 page root。页 options.model 到真实 VM 的当前关系可在明确普通方法调用模型下成立，但捕获源码中的替代写入／alias 逃逸必须扫描，不能全部称外部 monkey patch。
5. N5 的 throw 前单条 lexical statement 应进一步限定唯一 declaration，且 initializer 恰为 await 实际 callback，防同一声明中夹带另一调用或副作用。

不要求公开 VM 对象必须 Object.freeze，也不要求证明所有外部脚本永远不替换方法。用户沿所选 href 导航、提交时 hash 稳定、标准 DOM／URL API、页面已安装且真实表单条件允许提交，都是合理的有限环境条件。实际页面装配、调用和返回传播仍必须由源码生成。

## CPB-03：默认装配、资源、状态转换及交错

已读 `callscope/atomicity_completion.py` 至 operations_from_sources，包括有限交错求解器，并对照 scheduler.nextCandidates 及 readiness 分支。

1. A6 最初以任意 pending filter、任意 helper push、若干未见字段写入完成 candidate_closed；尚未连接实际 allEntries→pending 的每次赋值／筛选→return pending.slice→orchestrator for-of。smart rank／provider gate 的实际返回来源不能由“通过 gate”条件代替。
2. guarded_update 最初扫描 condition 内是否有 includes／版本比较，没有核对整个否定、合取、undefined gate 及分支支配；反向条件也可能通过。expectedStatus 构造也应认证完整有限 AST，而不是存在所需子树。
3. 资源 publish 最初仅识别 rename(tmp, formal path)，缺 save(queue)→JSON.stringify(queue)→同 temporary file write→rename 的数据链。若已有 lifecycle 只认证 callback queue 到 save 实参，仍须闭合保存内容。
4. Promise.all import 的 named child 索引须拒绝 holes／spreads 或准确建模实际索引；唯一 factory／delegate return 需要直接完成路径检查。

目录锁、标准路径与原子发布的正常运行可以显式受信；不能由锁模型假定 façade 整体串行，也不能由字段模型假定没有实际未分析的 candidate 替换。

## WWC-02 与 CPB-01

WWC-02 的 `device_flow.py` 最初仅 D1／D2 foundation，作者明确其余尚未完成。我已指出：factory 内任意同名 command/save 方法不等于 returned client 实际属性；唯一 return 不排 fallthrough；Promise.all 的词法／标准语义、完整 pattern 索引与 export 身份须认证；const 声明身份不能代替成员到达值／可见写入审计。作者正在完成 wrapper、transport、HTTP、Rust dispatcher／authority 链，等待完整候选后复审。

CPB-01 的 `pipeline_flow.py` 当前明确保留 P1..P6 必要 gaps 和 `full_goal_supported=false`，没有把局部参数／预算事实自动升级。所有真实 new/existing、direct/broker、finalizer-only、不同预算及 opaque supervisor 仍需继续连接；前置 early return 反证不能代替剩余链路。

## 统一 registry

已读 `callscope/goal_registry.py` 初版及 config 集成。需在最终冻结前核验：

- 必要 gaps 必须是显式、类型正确的空列表；同时检查 child 与每义务的必要缺口和截断，不能把缺失字段当空。
- child snapshot/source/policy/inner-contract identity 要与当前输入逐一匹配。
- obligation collection 要严格检查元素类型、唯一 ID 及固定集合；mapping 的 value 不能覆盖 key 中的 ID。
- 原五个 goal ID 与 adapter／required IDs 的映射要在 registry 或正式账本验收中强制保持。
- 完整反驳的标题和计数不能仍称“必要缺口”；也不能显示为原 claim 的完整支持。

registry 的标签和布尔二次 gate 只是防御检查；adapter 源码语义和实际自动证书仍须独立审查。正式新结果出现后，将重核 canonical IDs、源码位置／哈希、固定合同、必要关系和所有源式反证，再给最终认可。
