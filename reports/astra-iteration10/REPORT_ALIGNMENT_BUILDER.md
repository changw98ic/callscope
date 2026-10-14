# 全文范围对照账本生成器

[build_report_alignment.py](build_report_alignment.py) 只读取固定的 [REPORT_ALIGNMENT_CATALOG.json](REPORT_ALIGNMENT_CATALOG.json)、两库正式 `*-automatic-report.json` / `*-configured-findings.json` 和正式 `goal-ledger.json`。它不执行检测器、SQLite 查询、目标、测试或构建，不用 benchmark 原文生成机器证据，也不增加 Astra 审批。

待正式产物存在后运行受信 Python：

```bash
/workspace/callscope/.analysis-tools/runtime/bin/python /workspace/callscope/reports/astra-iteration10/build_report_alignment.py
```

默认输出为本轮新文件 `REPORT_ALIGNMENT_RESULTS.json`，已有输出拒绝覆盖。脚本保留原目录的32个章节和130个段落／表格行／列表项，核对两份固定报告的字节和全部 span hash。章节到既有分析 ID 的固定映射只提供导航，不能替代结论。

五项具体判断只复制保存的 registry judgment，并对齐实际 Finding / Evidence / goal ledger 内容及快照、源码、策略和合同身份。主要链只复制真实 source-chain assessment、完整 facts 指针、模型、scope 和 gaps。每份引用保留 artifact SHA、JSON pointer、目标值 canonical SHA、Finding / Evidence ID 和 source context；定位到同一文件或 selector 不算复现。

架构和覆盖章节引用实际声明、目录、依赖与解析／排除账本，同时明确职责及事实所有权语义没有被全面自动解释。原未审范围始终未审。每个原段落保存对应域的证据入口，段落全部文字、建议和反证的语义等价不由本脚本评级；不生成新的功能通过率。

最终 `report_scope.whole_report_reproduction_claimed=false`，也不声称全文已超越。具体代码判断与主要链能够支持描述接近原报告的范围，不能据此覆盖全部职责、安全、部署或运行行为。

写脚本时正式产物尚未存在，因此先只检查 AST 语法；正式两库报告、findings 与 goal ledger 发布后，脚本已正常执行并生成 [REPORT_ALIGNMENT_RESULTS.json](REPORT_ALIGNMENT_RESULTS.json)，退出码为 0，没有使用 fixture、开发近似结果或人工标签填账本。

只读产物核对确认：32 个章节和130条段落记录与原 catalog 完全相同；245个独立引用涉及6个实际产物文件，全部文件哈希和 JSON pointer 目标值哈希匹配，其中83个引用具有已核对的正式快照身份。5项 goal assessment 原样保存，18项 source-chain assessment 原样保存，WWC 的3项 partial source relations 未被升级；WWC 的1组重叠 source selection 仍明确不计作额外功能覆盖。`whole_report_reproduction_claimed=false`。

生成器 SHA-256 为 `717a711f3fc612acc7bd884f0ded9e14db670f84e9e9cfa282561e4885b4f930`；结果产物为6,410,321字节，SHA-256 为 `ab0546941a0b30f46167742cca029bfd43aad57276d3b54c70a1805cb650c45d`。缺失正式输入仍直接失败，已有输出仍禁止覆盖。
