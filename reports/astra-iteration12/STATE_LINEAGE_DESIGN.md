# 条件状态沿袭与发布边界

本扩展只承接原 CodePatchBay 分析 `CODEPATCHBAY_ANALYSIS.md:80` 中的两项有限源码关系，不把原报告文字或规则的职责名称当作证据。正常分析入口是 `state_lineage_relations.analyze_pattern(analysis)`，模块版本为 `captured-conditional-lineage-publication-1`，模型为 `finite-conditional-event-lineage-publication-source-v1`。

## 输入与证据

`state-lineage-rules.json` 只选取声明，未配置期望的事件、guard、成功值或调用序列。`_Analysis.load()` 认证保存源码、声明、图节点及实际 CALLS。语法通过保存源码的 Tree-sitter CST 读取。表达式词法身份、调用绑定与普通记录/有限布尔解释复用已有公共实现，没有复制目标函数作为夹具，也没有执行目标函数。

分析只接受实际绑定到所选目标声明的内部调用。注入函数或条件选择的外部 transport 没有唯一绑定时，明确保存为 opaque frontier，保留其真实声明、调用点和控制条件，不补造 CALLS。

## `conditional_state_lineage`

规则 `cpb-review-fixed-state-lineage` 选择 `completeRemediation`、其 callback runner、状态 parser、superseder、event writer、lineage builder，以及实际 event/queue authority。

分析从已绑定的 callback 注册调用读取实际 callback，查找其真实 if 分支内的两项已绑定调用。if 操作数必须通过同一词法声明的 initializer 绑定到所选 status parser；不是凭 `FIXED` 字面量或函数名称猜测分支。保存实际条件文字及符号表达式、两项调用的 await、同一语句块中的正常先后次序。先后次序本身不证明回调必然激活或分支可达。

外层实参按位置和对象字段绑定到 helper 形参，继而组合 event writer 到 event authority 的实参。事件字段中的实际字面量、queue 对象与 metadata 的实际字段保留。只有相同外层词法声明身份才记录为共享来源；对象属性名称相同不算同一 job。保存 lineage record 的实际加载表达式，并列出缺少输入、已有完成任务等提前 return/throw 条件。因此，分析陈述的是到达所选分支且前置操作正常完成时的源码关系，不声称每次都会入队。

## `conditional_publication_boundary`

规则 `cpb-finalizer-conditional-publication` 选择 finalizer、PR boundary、controlled push、两处 Git executor 和 review-bundle helper。实际 local/remote/pr/dry-run 字符串从源码的严格枚举比较提取，实际布尔 plan 字段从同一个 const record 提取，未在规则里写入模式表。

有限模型只解释 literal、稳定词法输入、`!`、短路 `&&`/`||`、严格 `===`/`!==` 和未被遮蔽的标准 `Boolean()`。布尔可选项限制为普通布尔值；其他值、调用结果、取属性、副作用和算术结果保持 unknown。当前实际表包含源枚举单元与 other 单元及两个布尔输入的组合；它只说明源 plan 和前缀模式/opt-in guard，不说明真实副作用已发生。依赖工作区状态的 commit plan 等仍保存 unknown 及原表达式。

PR 选项按真实同一对象词法身份重放未被遮蔽的 `Object.assign` 的普通固定字段补丁。未知 spread/patch 清除之前可知字段；后续明确字段才重新变为已知。预览调用的显式覆盖单独保留。实际参数字段映射到 callee 解构形参身份，再读取真正消费这些形参的直接 if/return，保存组合表达式和该 guard 在源语句次序中早于 transport 的事实。没有因此断言此前没有本地 IO，也不把顺序冒充所有路径上的支配关系。

对象字面量也按实际 CST 成员次序应用；未知 spread 清除之前的已知字段，之后的显式字段才恢复已知，嵌套对象相同。实际 queue 的来源字段位于相关 spread 之后，但模型不依赖这一特定源码布局。超过表达式/记录深度预算保持 unknown。

Push 边界保存实际 Git 参数首字面量及其真实 executor 链；仅协议字面量 `push` 被标为远端命令接口。Git executor 中对 `runCommand("git", ...)` 的未知执行接口保持 opaque。可空 callback 的形参默认值、实际调用条件以及选中 caller 是否提供该字段，均从源码读取；通用 helper 的可选 authorizer 与当前 finalizer 提供的 authorizer 分开呈现。

Review bundle 调用是否早于所选 mode/permission guards 用实际字节位置比较，并附实际 branch 条件。它是反证边界，防止把后面的发布模式检查推广成整个 finalizer 的无 IO 保证。权限 validator、lease、capability、principal、journal 等调用及提前 return/throw 均作为源码前置条件保留；未证明注入 callback 激活、授权服务认可、外写完成、恢复穷尽或远端后置条件。

## 输出结构与体积

`source_facts` 是唯一完整 fact 存储；派生 fact 引用既有 fact 时使用 `source_fact_id`，pattern 中的关系也使用相同 ID。ID 只在本次分析的 `source_facts[].id` 内解析，不是图边。`relation_witnesses`、实际 mode guard、有限表实际值/unknown、选项到形参的绑定等保留可直接阅读的关系数据，避免只有类型名称。

初次开发查询确实成功，但旧表示反复内嵌完整 guard 与 parse identity，生成约 379 MB JSON。该次结果的原始 SHA、模块 SHA、旧 snapshot 身份和实际日志保存在 `STATE_LINEAGE_INITIAL_QUERY_RECORD.json`；原始字节压缩保存，未修改任何既有正式轮次。随后改为单次 fact 存储和引用，并缓存相同源码查询。压缩初次文件本身不被视为正式结构问题的修复。

第二次实际查询为 `state-lineage-source-query-compact.json`，88,179,748 bytes；两个模式均实际 scoped、全部所选角色绑定闭合，probe 的 11 个角色也完成认证。其 pattern 只保留约 0.34 MB，剩余主体是已有调用 fact 自带的源位置/parser provenance。读回还发现有限表误纳入嵌套 catch 的 return 和局部 capability 状态，产生 40 个组合。最终模型因此只解释函数体的直接前缀 guard，额外布尔单元只从实际具有布尔默认值的形参提取；局部 capability、嵌套分支等保留为未执行前置条件。第二次产物不覆盖、不冒充修复后的正式结果；最终查询另存 `state-lineage-source-query-final.json`。

## 开发查询协议

`query_state_lineage.py` 内部独占公共 flock，只装载一次 iteration11 CPB v13 只读快照。当前模块和新 rule 在旧快照上查询，元数据显式标为开发来源，不是 v14 正式结果。它记录模块前后 SHA、原 snapshot/source/policy identity、实际认证角色、绑定闭合状态、gaps 和模型结果。可同时加载当前新 policy 的 probe rule，仅读取并认证声明，不重解释其 command pattern；新 policy 与旧 snapshot policy 的区别明确记录。

本轮不执行目标代码、测试、构建、安装或夹具。v14 正式 freeze/scan 和发布产物仍等待 root 明确授权。

## 最后读回与交接

`state-lineage-source-query-final.json` 实际保存两个 scoped 关系，8/6 个所选角色均绑定闭合、statement 闭合、必要 gaps 为空。实际模式表为 20 行，只有源码中默认 false 的 `allowLiveFinalize`、`allowLive` 两个布尔形参；两个直接前缀 guard 是实际 unsupported-mode 条件和 `!dryRun && !liveAllowed`。所有引用都解析到同次 source facts：lineage 为 22 处引用、20 个不同目标；publication 为 613 处引用、139 个不同目标。额外 probe 的 11 个角色全部认证并绑定闭合。查询明确使用旧 v13 快照和新开发 policy，不是正式 v14 结果。

随后新模块仅补默认保守分支：不支持的对象成员使整个 record unknown；preview 对象 shorthand 从实际 CST 读取，未知成员/计算 key 清空已有已知字段。这些分支不改变本题已读的对象形状。root 要求下次验证使用正式 v14 正常分析，故停止刚开始的 final2 开发进程；仅保留 `captured_source_loaded` 日志，没有 final2 结果文件，也不宣称最新两分支已完成开发查询。最后已完成查询模块 SHA 与最终待冻结模块 SHA 分别保存在 `STATE_LINEAGE_FINAL_HANDOFF.json`，最终模块和相关 helper 的 AST 已核对。不会另开开发快照或改旧模型、旧正式产物。
