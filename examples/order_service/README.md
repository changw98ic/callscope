# 订单调用结构示例

这个目录供 CallScope 读取源码，不是要启动的订单应用。不要运行、导入或构建它；没有测试文件、测试套件或执行入口。

从 CallScope 仓库根目录扫描或打开界面：

```sh
python -m callscope scan examples/order_service --json
python -m callscope serve examples/order_service --port 8787 --watch
```

`.callscope.json` 明确声明项目采用的调用结构约束。示例中的规则是人为给定的架构意图，不是从业务逻辑推测出来的。

| 源码结构 | 供界面解释的事实 |
|---|---|
| `submit_order → save_order → write_order` | 提交入口连接到存储入口；满足对应路径约束 |
| `validate_order` 存在但未接入提交入口 | 相对 `submit-validation-connected` 规则的连接缺口 |
| `fetch_order → read_order` | 相对 `api-cannot-read-storage-directly` 规则的直接调用违规 |
| `get_order` 存在但未接入读取入口 | 相对 `fetch-domain-connected` 规则的连接缺口 |
| `refresh_order ↔ retry_notification` | 调用环结构；不证明无法终止，两侧都含条件分支 |
| `dispatch_hook → callback` | 目标来自函数参数，必须显示为未知或动态关系 |

路径存在不证明每次执行都会经过该路径，也不证明顺序、参数、输出或业务结果正确。未知回调不应被标成“缺少实现”；未被规则命中的函数也不应被标成“功能正确”。

可以在界面查看历史版本后，手动修改 `api.py` 的静态调用连接，再扫描一次比较快照。比较的是源码调用结构，没有执行前后版本。
