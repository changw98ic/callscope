# 状态、记录写者和消费界面的有限职责事实

原两份报告以实际状态和事实操作解释架构职责。现有自动架构目录盘点不能替代这些关系。本模块新增 `resource_writer_ownership` 和 `captured-resource-writer-source-v1`，先提供有限、可复用的源码事实；不会从目录名指派职责。

## 输出与含义

`resource_captured_writer` 保存实际赋值/更新的 lexical root 与静态 member 路径、所在确切 callable、右值及分支来源。`resource_captured_record_construction` 单列捕获 record 初始化；局部构造不是持久提交。函数参数、self/this 和局部声明身份分开处理；相同字段名、相同方法名和不同函数的同名参数不自动合并。

`resource_captured_same_token_reference` 只关联相同已捕获 root token 和兼容 member 路径的引用，不声称 read-after-write 或运行时同一对象。实际已绑定 CALLS 和实参表达式保留为接口交接事实；外部、动态与未绑定调用仍为 effect frontier，不通过 API 名称猜测物理写入。

拒绝 guard 的表达式和真实 abrupt branch 与写者分别保存。它们不能单凭存在便证明全部权限、revision、fencing 或领域不变量成立。

## 当前结论范围

`ownership_assessment=partial_captured_writers_and_consumers`。这些事实支持“所选函数写这个捕获字段、向这个真实接口传这个记录”的有限职责解释。`unique_fact_owner_proven`、`canonical_authority_proven`、`all_mutations_authorized_proven`、`all_storage_resources_bound_proven`、`whole_repository_ownership_inferred` 均为 false。

有限职责解释仍缺堆别名、跨过程资源等价、全部写入者、持久接口语义与完整授权合同。原文关于唯一事实权威、跨部署 Credential 所有权以及文档与实现一致性的更强判断，不能用本模式的 scoped source 支持冒充完成。

规则 `ownership-rules.json` 只保存两库 exact 声明 locators 与模型。查询 `query_lifecycle_ownership.py` 对 iteration10 的保存源码执行正常静态查询，串行获取共同 flock，记录旧 snapshot/source/policy 与模块 SHA。没有目标执行、测试、构建或安装。

## 实际保存源码查询

两份查询均使用模块 SHA `6ee0cf1d1434a17869e7f36e66b9c31649e6fb807fbcad18dabe36c8a326d74c`，整个查询期间模块 bytes 稳定：

| 原保存来源 | 实际源码关系 | 源范围 / 预算 |
| --- | --- | --- |
| CPB `7524afef4f9234ebef40eec1d74dbb91a3f56dc76f0191728c42d3bdd3cfb167` | 299 个事实：32 个赋值/更新、4 个 record 构造、16 个拒绝 guard、116 个同 token 引用；113 个调用/effect frontier。 | 10 个 exact 角色和 graph binding 均可认证；1,903 次 AST 操作，未截断，`analysis_gaps=[]`。 |
| WWC `ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28` | 456 个事实：51 个赋值/更新、1 个 record 构造、1 个拒绝 guard、133 个同 token 引用；231 个调用/effect frontier。 | 8 个 exact 角色和 graph binding 均可认证；3,504 次 AST 操作，未截断，`analysis_gaps=[]`。 |

赋值包括局部 binding 更新与 record 字段更新，不能统称为持久事实写入。index 的动态下标保留为带真实源位置的 opaque index site，不把表达式文本相同当作键值相等。query 的 scoped source 支持只覆盖本表列出的有限关系；`ownership_assessment` 仍为 partial，canonical authority、唯一 owner 和全部权限均未证明。

原始证据为 `ownership-codepatchbay-source-query.json` 与 `ownership-winwincode-source-query.json`，共同摘要为 `LIFECYCLE_OWNERSHIP_OBSERVATIONS.json`。这是 development 查询，不能替代统一冻结工具与新策略后的正式扫描。
