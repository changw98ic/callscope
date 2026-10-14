# Agent 执行策略的源码报告域

`report_agent_policy_analysis.py` 扩展正常 `report_claims` 的固定类型 `agent_execution_policy`，以原 CPB 全文报告的 Agent/provider 段为范围。它不读取原报告文字来制造证据，也不宣布全部环境变量安全、唯一 pool 实现或真实沙箱隔离已经成立。

[规则片段](agent-policy-rule.json) 只声明 18 个真实源函数/方法角色和 `captured-normal-statement-control-v1`。父分析器已经认证 source snapshot/hash、图声明和完整 AST 位置；本模块经实际 CALLS 或词法声明身份连接实参、回调、guard 和写入源形式。

自动提取的关系包括：

- `allowedAgentsFromEnv` 返回 binding→非 null 且不包含所选 agent 的早退对象→同一注入 pool shape helper 的 receiver.execute；拒绝 guard 的外层直线语句先后及执行后 readonly audit/catch classifier。
- `buildChildEnv` 实际 callback→`_filterEnv` formal predicate→parent/extra 双循环的条件写入尝试→实际 key/provider 规则。默认、额外 allowKeys、provider 凭据配置、父环境特殊键跳过和 extra 覆盖分别保留。
- phase 的 native/none/default 环境赋值与 inherited/off/required/strict/custom、平台 provider 分支；disabled 时 required/strict throw 位于原 command/args fallback 返回前。源码条件不等于平台 probe 已通过或 provider 实际隔离。
- ACP start 与 terminal 的实际 child filter、sandbox wrapper 及 spawn 参数源顺序。start 先经 audit 环境投影赋 `this.childEnv`，terminal 直接使用局部 env；过滤后的显式环境写入和其他传递仍保存，避免宣称最终 env 是完全未变的过滤结果。

未知必要源码绑定、receiver、callback、guard 或关系都通过父分析器 `gap` 保存，并令 `scoped_source_supported=false`。已提取的外部进程调用、注入 pool 实现、环境变量实际值、审计内容、provider/network/process 效果始终保留未运行的边界。

所有事实通过父 `analysis.fact` 保存原 snapshot/hash/span、内容 ID 和来源类别。新模块接口只有 `analyze_pattern(analysis)`，不修改主分派器、目标仓库或既有冻结报告。

正常保存源码查询已对完整 CPB v11 snapshot 提取上述所有组件，`scoped_source_relations_supported=true`，必要 source gaps 为空，315 个 source facts；没有执行目标代码、测试、构建或外部进程。首轮发现的是 TS callback 参数 wrapper 的工具身份识别问题，已改为实际 pattern/name binder 并在同一真实保存源码上复核。完整候选证据在 [AGENT_POLICY_PREFREEZE_OBSERVATIONS.json](AGENT_POLICY_PREFREEZE_OBSERVATIONS.json)。

该证据限当前候选 source-policy 域；不会由 315 个事实或组件布尔值推导整个报告完成率。主代理的统一冻结扫描将形成最终版本证据。
