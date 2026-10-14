# scope2 正式产物协议

本目录为 `astra-iteration12-scope2`，使用已冻结的 `0.14.0 / static-multilang-14 / call-rules-13-architecture-explanations / schema 2`。真实核心身份为 `a198491ce936c91ce7a1c848789cf9fb27c5fc720b90ae81725c2ddf65f779dc`，共 65 份 Python 源码，见 [CORE_FREEZE.json](CORE_FREEZE.json)。冻结、启动扫描或配置规则增加均不表示原报告目标已经完成。

本 scope 的冻结策略分别配置 CodePatchBay 16、WinWinCode 20 项 report claims。相对 v13 的实际新增、旧 trusted-command 四个 helper 定位及原配置保留情况见 [POLICY_EXTENSION.json](POLICY_EXTENSION.json) 和[精简说明](POLICY_EXTENSION.md)。这不是同策略精度或性能对比，规则数也不是全文功能覆盖率。`SCOPE_PREPARATION.json` 是扩展前的准备记录，其中 copied policy hash 只说明当时复制身份；当前有效策略以本目录 freeze 与实际策略文件 hash 为准。

原 `astra-iteration12` 首尝试、冻结记录、数据库、JSON、日志及旧 v13 产物均留在原目录。首尝试未宣布完成；不能改名、覆盖或把其结果当作本 scope2 的新正式发布。旧 scope API 排队取消记录保留在首尝试目录，取消前进度未知；没有据此产生报告通过结论。开发查询文件及 `*-development-*` 文件只说明其记录的开发选区，不替代当前正式发布。

可信调用环境为工作目录 `/workspace/callscope`，Python `.analysis-tools/runtime/bin/python`，设置 `PYTHONDONTWRITEBYTECODE=1` 与 `PYTHONPATH=/workspace/callscope`。正式入口 `scan_repository.py codepatchbay` 随后 `scan_repository.py winwincode`，各自内部使用唯一共同 `.analysis-tools/goal-source-query.lock`；不得外套第二个 flock 或同时旁路读取正在构建的 DB。使用 full 冷/暖重算，不创建新 CocoIndex memo。冷扫描必须创建快照，未变更的暖扫描必须返回同一身份且不重复创建；失败现场不得覆盖。

正常报告由实际 `build_project_report` / `render_markdown` 生成，写出前在真实内存 report 上核对 `architecture.responsibility_explanations` 的共享位置、证据和 operation scoped references。成功或失败均保留独立 `<repo>-report-shared-reference-check.json`；成功摘要及其文件 hash 写入 integration，失败保留异常并中止报告写出。引用存在不证明模型结论、全部职责或运行时效果。

本工具自己的分析存储在正常报告写出前执行 WAL checkpoint。只在各库 integration 明确数据库已关闭且 WAL 空后，才可进行正式只读后处理：`compare_original_baseline.py --formal-artifacts-closed`、`compile_goal_ledger.py --formal-artifacts-closed`、`build_report_alignment.py --formal-artifacts-closed` 及正常工具 `readback_report_cli.py --run`。这些入口的 DB 锁由 helper 内部管理；不要为本说明增加扫描。JSON 展示摘要不打开 DB，最终发布说明仍须绑定真实报告、scope、账本和读回输入的 hash。当前是否完成以届时保存的实际结果为准。

原两份完整 Astra 报告继续作为有限命题的比较基准，没有新增 Astra 重复审批。原五项/三十关系、26 条观察、36 个引用身份及目录导航只是各自有限跟踪合同，均不能作为全文覆盖率分母。实际 source-only gaps、partial、unknown/false、文档限定语和每个条件边界照实保留；不把原本未审的全授权、全协议或物理效果扩充为剩余验收目标。

所有调用仅运行可信分析工具的纯静态处理。未运行目标代码、目标 CLI、测试、构建、安装、沙箱或夹具；静态目标函数中出现测试/执行名称不表示本系统执行了它们。普通源码结构可支持有限条件关系及具体字段、职责解释，不能独立保证完整运行时业务通过。
