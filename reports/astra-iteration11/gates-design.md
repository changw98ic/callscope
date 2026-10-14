# 条件门的有限纯静态关系

实现文件是 `callscope/conditional_gate_relations.py`，公共适配入口为 `analyze_pattern(analysis)`。调用方先使用 `report_chain_analysis._Analysis.load()` 完成保存源码、声明及图绑定认证，再传入该对象。模块导出 `VERSION=captured-conditional-gate-relations-1`、`MODEL=finite-js-plain-record-gate-conditions-v1`。三个独立规则在 `gates-rules.json`；规则只包含声明定位、模型与适用范围，没有期待的状态值、guard 或成功结果。

## 计算范围

1. readiness 规则定位 `fix.run` 和其实际调用的谓词。通过认证的调用边与词法声明身份关联实参和初始化来源，抽取谓词返回表达式；从同一语句块的真实提前 return/throw 推导 true 分支阻断后续调用。包括 enqueue 在内的后续调用名称来自源码。readiness 的实现和外部环境是否真的可用仍不由该关系证明。
2. completion 规则定位实际 evaluator、mutating predicate 和返回构造函数。有限摘要跟踪局部普通记录字段与声明身份，解释条件分支的正常控制流，保存每个提前返回的路径条件；通过真实调用边和形实参位置把 `gateResult` 返回对象的字段接回各分支。它独立给出每个当前条件的依赖，以及完整路径中先前 guard 的依赖，避免将“前序 mutating 门已放行”和“当前门本身受 mutating 限制”混淆。
3. access-audit 规则关联 `openHubAccessAudit` 返回值、同一声明上的真实 await 方法、catch 中对同一 response 的直接赋值和后续实际 `sendJson` 调用。另由 response writer 的参数声明身份和 member 调用实参，关联失败 response 字段到 writer 参数、再到 `reply.writeHead` 的实参。输出的是条件字段/响应源码关系；并未把 callback 注册当作实际调用，也不证明磁盘持久化、网络发送或先前业务修改回滚。

## 有限条件模型

仅解释捕获 CST 中的普通布尔、逻辑短路、严格字面量相等、普通固定属性、局部 const 初始化和返回构造。mutating 谓词的枚举单元由其实际字面量比较生成；每个属性只包含出现的字面量和“其它值”单元。只有普通稳定记录、严格枚举比较和布尔组合满足闭合词汇表时，才可把这个其它值单元解释为等价类。无运行输入、目标函数、目标源码编译、动态 import 或目标代码 eval。

mutating 谓词还单独解释缺值/null 的真实先返回分支。readiness 谓词只支持普通结果记录的有限比较；其 null/缺值读取保持 unknown，不伪装成谓词会返回 false。输出同时保留 `ordinary_record_partition_complete` 和整个含缺值范围的 `complete`，不混为同一承诺。

checklist evaluator、Set 构造和 has 返回值、外部判定、日志以及其它调用保留为不透明值或正常到达的显式条件。这里能计算 checklist 结果字段如何被优先消费，以及后续每个门的条件和返回；不能推出 checklist 内部每个检查、verdict 内容或证据可信性均正确。未知语句、未支持写入、路径/表达式预算或缺少角色会产生必要 gap 并阻止该组 `scoped_source_supported`。

## 来源和使用边界

每个事实保留 snapshot、文件 hash、原始 UTF-8 span/hash、解析身份和真实词法声明/认证调用身份；不新增 CALLS，不把方法同名当作绑定。source facts、模型假设和规则声明分开。

`gates-query.py` 是对冻结 v0.12 保存源码的普通开发查询：三个新规则不在该旧快照的保存策略内，因此产物明确标注 development、旧 snapshot/source/policy identity 和当前模块 SHA。它不回写旧数据库、旧报告或目标仓库。正式版本仍须在新规则与新工具身份下走正常静态 scan，开发查询不冒充正式 v0.13 finding。

开发查询共用 `.analysis-tools/goal-source-query.lock`，内部仅持有一次 `flock`；不运行测试、构建、安装、夹具或目标程序。
