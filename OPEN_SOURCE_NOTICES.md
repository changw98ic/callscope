# 开源发布与来源声明

CallScope 原创代码与原创文档按根目录 [MIT License](LICENSE) 发布。该许可不改变第三方代码、分析样本或报告中引用源码的原有许可。

- 随包 Axon 图核心保留 MIT 署名、固定提交及完整条款；CocoIndex 可选依赖的 Apache-2.0 声明与条款保留。原来源记录见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
- v0.15 随包复用 CodeGraph 的固定源码和语法资源，保留上游 MIT 以及单项 grammar 的原版权和条款。31 份资源的许可及来源边界见 [逐项清单](callscope/_vendor/codegraph/grammar-license-sources.json)，工具依赖声明见 [第三方声明](THIRD_PARTY_NOTICES.md)。
- CodePatchBay 与 WinWinCode 是独立的公开分析样本，不是本项目运行依赖。报告内的源码引文继续遵循各自原许可和署名。两个固定工作区的 LICENSE 与 NOTICE 原文分别存于 [reports/target-notices](reports/target-notices/README.md)。CodePatchBay 的 LICENSE 与 NOTICE 按其原文分别保留，未在此重写其许可口径。
- n0vel 为同一 GitHub 所有者的公开源码静态分析样本，固定提交及保存范围见 [接入报告](reports/codegraph-integration-v15/REPORT.md)。源码证据不因保存在报告中而改授 CallScope 的 MIT；该样本不作为运行依赖，也未被执行。
- 发布目录保留原报告和冻结源码的字节身份。公开 README 增加了发布说明，原 README 和 gitignore 另存于 [publication/workspace-original](publication/workspace-original/)。
- 本次保存与归档不执行分析样本的代码、测试、构建或安装。有限静态结论不等于全程序正确性或运行成功证明。
