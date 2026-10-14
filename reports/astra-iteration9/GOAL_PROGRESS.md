# v0.11 五个完整目标的实际进展

日期：2026-10-13（Asia/Shanghai）

原五个完整目标仍为 **0/5 达成**。原30个必要义务保留为4个在声明范围内支持、20个局部支持、6个未知。v0.11补上了可追溯的局部结构关系和一个复制时刻的条件保留见证；没有把这些结果算成端到端功能通过。

本轮判断来自两库正式保存快照，依据[原验收合同](../astra-iteration4/GOAL_ACCEPTANCE.md)人工核对[证据账本](goal-ledger.json)。没有运行目标代码、测试、构建或沙箱，也没有自动业务义务求解器。实现身份见[冻结记录](CORE_FREEZE.json)。

| 原完整目标 | 必要义务 | 声明范围内已支持 | 仍未闭合 | 本轮变化与主要缺段 |
| --- | ---: | ---: | ---: | --- |
| CPB-01：pipeline重试选项到有效预算 | 6 | 0 | 6 | P3新增queue/agent结构关系与agent复制时刻条件见证；P4原engine来源形式关系保持。入口字段、共享对象修改、async返回、记录/消息运输和实际预算消费仍缺。 |
| CPB-02：superseded跨层终态分类 | 5 | 0 | 5 | 保持两个初始化集合的有限差异。实际状态生产、具体job谓词、恢复guard及event-store保护关系仍缺。 |
| CPB-03：同键去重与权威写入 | 7 | 1 | 6 | 保持所选保护region的限定支持。实际deps、同资源、状态条件、全写者及模型推导交错仍缺。 |
| WWC-01：看板导航到生产task port | 7 | 2 | 5 | 保持有限参数/返回链和possible query keys关系。公开入口、路由/事件激活、可变端口、完整拒绝链及反证仍缺。 |
| WWC-02：Device条件必填字段 | 5 | 1 | 4 | 保持所选spec构造缺键事实。真实client注入、命令/JSON/Rust映射、authority与条件guard仍缺。 |

五个目标的完整定义、条件、反证、义务次序和`required`保持原样。4个已支持的限定义务仍是CPB-03.A4、WWC-01.N2、WWC-01.N3和WWC-02.D1；它们不能代替所在目标的其余义务。

## 这次新增了什么

正式[字段关系导出](field-relations.json)保存原五个选中位置的41条源码结构关系：实参到目标形参的接线、当前return binding、局部别名、对象构造顺序和显式成员写入范围。每条关系属于实际保存源码、声明身份、上下文和分支，不能据此认定运行值、入口heap或间接副作用已闭合。

agent的`return {...metadata, agents, agent}`位于保存源码的489行。其实际spread正常完成、复制表面满足已声明普通数据属性模型且该时刻自有可枚举`maxRetries`存在时，后续固定`agents`、`agent`定义不会改写该键；复制时的值或引用可保留到这个新字面对象的结束。这一见证从**复制时刻**起算，不证明入口metadata的字段来源、字段存在性、共享子对象当前内容、Promise最终履约值或跨消息运输。

原选中endpoint判断保持：engine的`runJob`实参在正常前缀和声明copy/Get模型内支持`source_form_preserved_when_present`；queue的两个分支及agent的两个return仍为unknown。services helper仍有11个已闭合自有键且缺`maxRetries`。上述scope详见[字段评估](field-assessments.json)，没有用新的copy-time轴覆盖旧来源未知。

## 证据映射与下一段

账本有648个正式证据引用，均保留保存artifact SHA256、JSON pointer、snapshot/finding/contract身份和目标JSON内容的规范SHA256。旧10个数字索引字段事实按operation、owner、目标和原源码hash/span唯一映射到新索引；没有照抄旧数组位置。引用数、结构关系数、选中site数和字段事实数都不是功能覆盖率。

CPB-01下一段应继续闭合输入/返回binding、queue新建与旧记录复用、scheduler与assignment身份、JSON/inbox/broker运输及最终预算读取。当前共享对象Set与callee effects、async履约和运输缺口必须保持可定位unknown；补更多词法关系本身不会使P3或完整目标达成。
