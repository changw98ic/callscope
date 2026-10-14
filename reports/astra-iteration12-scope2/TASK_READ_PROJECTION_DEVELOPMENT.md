# Task 读取与投影：有限源码范围补充

新增 data-only 规则 [cpb-task-read-projection-rule.json](cpb-task-read-projection-rule.json) 选择 8 个实际声明，使用既有 `guarded_call_sequence` 与 `captured-normal-statement-control-v1`；没有新增或修改冻结核心。

本次在 common flock 下加载一次 v13 保存快照，以正常 `analyze_report_claims(snapshot, [rule])` 得到真实 Finding，再调用正常 `build_project_report(snapshot, findings)` 与 `render_markdown`。未运行旧 188 声明全范围，也未将原报告正文作为答案、构造伪 Finding 或使用夹具。这是新增范围的发展查询，不是 scope2 正式扫描。

实际 Finding `a8de27ed8b905f79159044bc` 的状态为 `scoped_source_relations_supported`，219 条 source facts，来源及解释 gaps 均为空。完整正常正文见 [cpb-task-development-report.md](cpb-task-development-report.md)，实际关系及引用见 [cpb-task-development-report.json](cpb-task-development-report.json)。

实际源码限定的分工为：

- `task.run` 保存参数解析、缺 taskId/缺 view 的提前返回、项目选择、动态 import 的捕获表达式、调用与 `renderTaskView(view)` 的实际实参关系。动态 import 不补成已解析普通 CALLS。
- `projectTaskView` 捕获 `loadQueue(hubRoot)`、项目和任务字段筛选、`getJobByQueueEntryId` 的实际接口及异常分支，随后构造 `schemaVersion/taskId/state/summary/progress/checks/changedFiles/nextAction/createdAt/updatedAt`，把 `raw` 交给 `sanitizeTaskView` 并返回。
- `loadQueue` 的实际内部调用目标为 `loadLocalQueue`。后者捕获 bounded-read 接口、`JSON.parse`、`normalizeQueue` 及 `ENOENT`/unsafe-file 分支；不证明底层 I/O 已发生或成功。
- `getJobByQueueEntryId` 捕获 `listJobs(cpbRoot, {project,dataRoot})` 及后续选择表达式，依赖内部的全部行为不在本条规则范围。
- `renderTaskView` 保存实际 `view.summary/state/progress/nextAction` 的输入使用及格式化调用；`sanitizeTaskView` 的实际过滤条件和赋值源事实保留于完整报告。

这些来源解释所选 facade、读取接口和记录投影的有限主链，不宣称所有传递依赖纯、所有副作用已排除、字段实际值相等、动态调用一定激活、权限完整或业务正确。

本条正常报告实际生成 298 个操作、188 条操作关系、10 个 callable owner 分组，访问 1,109 个 CST 节点，预算完整。与同快照、同提取器字节的旧 14,958 操作 ID 集合相比，33 个重叠、265 个净新增，ID 并集为 **15,223 / 16,384**。这是实际集合账目；后续正式全范围仍需正常重算，未将集合并操作冒充完整分析。

[DEVELOPMENT-READBACK](cpb-task-DEVELOPMENT-READBACK.json) 保存真实规则/Finding/快照/工具身份、集合预算和所有共享引用检查：651 个位置 anchor、8 个含实参/形参来源的文件全部 source hash/span/UTF-8 byte map 匹配，共享引用失败数为 0，65 个核心文件字节前后一致。[SOURCE_FACT_READBACK](cpb-task-SOURCE_FACT_READBACK.json) 另外逐条核对 219 条原始 source facts 的 5 个实现文件，全部匹配；该检查只读 JSON 与源码，没有打开数据库或重算分析。

目标执行、目标导入、测试、构建和安装均未发生。正式新范围由 root 在 scope2 policy/freeze 下正常扫描，本记录不改写旧 freeze、旧 DB 或旧报告。
