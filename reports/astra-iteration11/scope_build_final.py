"""Render the scope comparison from closed saved artifact projections only.

The original finite prose scope is compared here; this is not a detector or a
new rating of target code. No target, database or analyzer is opened.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name: str):
    return json.loads((HERE / name).read_text())


def digest(name: str) -> str:
    with (HERE / name).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def cell(value) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def main():
    mapping = load("scope-pointer-map.json")
    observations = {repo: load(f"scope-{repo}-formal-observations.json")
        for repo in ("codepatchbay", "winwincode")}
    reports = {repo: item["formal_projection"] for repo, item in observations.items()}
    ledger = load("scope-ledger-identity.json")
    freeze = load("CORE_FREEZE.json")
    assert mapping["both_formal_repositories_consumed"]
    assert ledger["both_formal_snapshots_match"]
    assert all(all(item["copied_identity_checks"].values()) for item in observations.values())
    assert ledger["freeze_sha256"] == digest("CORE_FREEZE.json")
    chains = {repo: {chain["rule_id"]: chain for chain in report["functional_chains"]}
        for repo, report in reports.items()}
    def ref(repo: str, rule: str, suffix: str = "") -> str:
        return chains[repo][rule]["formal_entry_pointer"] + suffix
    def link(repo: str, pointer: str) -> str:
        return f"[{pointer}]({repo}-automatic-report.json#{pointer})"
    statuses = {repo: Counter(chain["assessment"]["state"] for chain in report["functional_chains"])
        for repo, report in reports.items()}
    for entry in mapping["entries"]:
        entry["original_finite_claim_comparison"] = "formal_saved_source_relation_available"
    for item in mapping["finite_claims_to_compare_after_formal_publication"]:
        repo = item["repository"]
        item["formal_report_file"] = repo + "-automatic-report.json"
        item["formal_report_sha256"] = observations[repo]["report_sha256"]
        if item["original_line_anchor"] == 88:
            item["comparison_status"] = "specific_document_deployment_statement_comparison_not_generated"
            item["formal_evidence_pointers"] = [ref(repo, "wwc-report-device-provider-deployment", "/pattern"),
                ref(repo, "wwc-captured-record-resource-writers", "/pattern/unreviewed_scope")]
        else:
            ownership_rule = "cpb-captured-record-resource-writers" if repo == "codepatchbay" else "wwc-captured-record-resource-writers"
            item["comparison_status"] = "formal_source_references_available_finite_layer_explanation_not_generated"
            item["formal_evidence_pointers"] = ["/architecture/meaning", "/architecture/captured_writer_references/0",
                ref(repo, ownership_rule, "/pattern/responsibility_interpretation")]
        item["gap_scope"] = "Only the original finite report statement; stronger global proof is not required."
    mapping["kind"] = "original_report_scope_pointer_map_formal"
    mapping["formal_artifact_scope_comparison_completed"] = True
    mapping["whole_report_semantic_equivalence_score_computed"] = False
    mapping["tracking_identity_artifact"] = "scope-ledger-identity.json"
    mapping["tracking_identity_artifact_sha256"] = digest("scope-ledger-identity.json")
    (HERE / "scope-pointer-map.json").write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + "\n")

    lines = ["# 原完整报告与 v0.13 正式自动报告的范围差距", "",
        "本轮两库正式扫描和保存产物均已闭合。原五项具体条件判断保持自动承接；CPB 的十三条、WWC 的十八条条件源码关系均保存为 `scoped_source_relations_supported`，其中包含本轮十三条新增查询。原来的三个 WWC partial 也已解除错误的声明属性上下文限制。**这些是真实源关系状态，不是三十一种业务功能通过或全文覆盖率。**", "",
        "原已读内容还存在两类明确距离：Device 架构文档具体绝对声明与真实部署来源的差异，尚未自动作对应比较；两库的有限架构职责说明仍主要保存为结构、写者和接口证据引用，尚未自动汇总成原职责表那样的具体分工解释。后文只将这些原文实际说过的有限命题列作差距，不把唯一 owner、全授权、全协议、完整状态机或物理效果追加为验收目标。", "",
        "## 正式依据与定位", "",
        "依据是 [CodePatchBay 原报告](../astra-baseline/CODEPATCHBAY_ANALYSIS.md)、[WinWinCode 原报告](../astra-baseline/WINWINCODE_ANALYSIS.md) 和 [v0.12 范围差距](../astra-iteration10/REPORT_SCOPE_GAPS.md)。本文件只比较已保存产物，没有重新审查目标代码、调用分析器、打开数据库或增加 Astra 把关。巨大 source_facts 留在正式 JSON；流式投影仅保存数量与原 Pointer。", "",
        "| 项目 | 正式快照 | 正式报告 SHA256 |", "| --- | --- | --- |"]
    for repo in reports:
        lines.append(f"| {repo} | `{reports[repo]['snapshot']['id']}` | `{observations[repo]['report_sha256']}` |")
    lines.extend(["", "原正式文件：[CodePatchBay](codepatchbay-automatic-report.json)、[WinWinCode](winwincode-automatic-report.json)。下文 `C:/…` 与 `W:/…` 分别是两文件的 JSON Pointer；精确 Finding/Evidence ID、文件 SHA、范围、实际 gaps 和开发来源沿革见 [scope-pointer-map.json](scope-pointer-map.json)。", "",
        f"冻结工具身份为 `{freeze['tool_identity']['source_hash']}`。两份 integration 均记录数据库关闭、WAL 为空；cold 创建新快照，warm 返回同一快照且 `created=false`。本轮采用全量前端/检测重算，不能当作与 v0.12 相同维护引擎的性能比较。", "",
        "[账本身份核对](scope-ledger-identity.json) 将五个保存判断与正式快照、source/policy、冻结 tool 和 [goal-ledger.json](goal-ledger.json) 对齐。账本记录五项 `scoped_static_judgment_reproduced`、三十项必要关系 `supported`、无未闭合必要关系；这是原五项判断的实现跟踪，未替代两份完整报告。", "",
        "原 [二十六项冻结观察对照](ORIGINAL_BASELINE_COMPARISON.json) 保留十项 reproduced、三项 unknown、十三项 evidence_only，未重定义旧分母；[PUBLICATION_IDENTITY.json](PUBLICATION_IDENTITY.json) 的 `verified=true`。该对照不等于全文或功能覆盖率。", "",
        "## 一、原已读明确命题尚未同等自动承接", "",
        "| 原文有限命题 | 当前正式保存内容 | 具体剩余距离 |", "| --- | --- | --- |",
        f"| [WWC Device 文档口径差异](../astra-baseline/WINWINCODE_ANALYSIS.md:88) | `W:{ref('winwincode', 'wwc-report-device-provider-deployment', '/pattern')}` 已保存 Server boundary、Worker/Device provider 构造和安装来源；`W:{ref('winwincode', 'wwc-captured-record-resource-writers', '/pattern/unreviewed_scope')}` 明确保留文档一致性范围。 | 尚未自动定位并比较文档中“长期 Credential/Provider 唯属 Control Plane”的具体绝对表述与 Device 生产来源。需要的是原文这个局部说明差异，不是全架构文档规范或所有 credential 安全审计。 |",
        f"| [CPB 有限架构职责表](../astra-baseline/CODEPATCHBAY_ANALYSIS.md:30) | `C:/architecture/meaning` 仍限定目录组成/已认证引用；`C:/architecture/captured_writer_references/0` 和 `C:{ref('codepatchbay', 'cpb-captured-record-resource-writers', '/pattern/responsibility_interpretation')}` 提供 event/job/queue 写者与接口证据。 | 尚未自动汇总原表中的 CLI 提交/投影、orchestrator assignment/attempt、worker/bridge 消息/进程、engine 注入端口与 service 实现等具体分工解释。源链和写者已可下钻，不把这些来源缺少解释等同目标缺实现。 |",
        f"| [WWC 有限职责与身份表](../astra-baseline/WINWINCODE_ANALYSIS.md:30) | `W:/architecture/captured_writer_references/0`、`W:{ref('winwincode', 'wwc-captured-record-resource-writers', '/pattern/responsibility_interpretation')}` 及 `W:{ref('winwincode', 'wwc-report-worker-adapter-record-identities', '/pattern')}` 提供具体 writer/interface 与身份字段。 | 已有所选身份分离来源，但报告尚未自动把它们汇总为原表中 Client 表现/协议、Control Plane/Delivery 产品状态、Worker 执行事实、adapter/Kernel 接线的有限职责说明。 |", "",
        "以上两类差距是原文中的具体比较或报告解释。新写者模式的 `partial_captured_writers_and_consumers` 不是失败判据：只要有限来源足以支持原句，就可以承接原句；不要求证明 canonical 唯一所有者、全部写入者、全堆资源等价或全部授权。", "",
        "## 二、已承接的有限段落与原报告相同的限制", "",
        "### 原五项具体条件判断", "",
        "| 原判断 | 正式位置 | 保存状态 |", "| --- | --- | --- |"])
    for repo, report in reports.items():
        marker = "C" if repo == "codepatchbay" else "W"
        for index, judgment in enumerate(report["judgments"]):
            assert judgment["complete_assessment"] and judgment["full_goal_supported"] and not judgment["necessary_gaps"]
            lines.append(f"| {judgment['goal_id']} | `{marker}:/judgments/{index}`；finding `{judgment['finding_id']}`，evidence `{judgment['evidence_id']}` | `{judgment['assessment']}`；complete/full 均 true，必要 gaps 为空。 |")
    lines.extend(["", "重试预算、终态分类、幂等交错、公开导航缺上下文和 Device 条件字段遗漏各自保留真实条件与反证；没有扩大成所有重试、恢复、双提交或创建入口均失败。完整条件以各 judgment 及其 adapter evidence 为准。", "",
        "### 十三条新增查询对应的正式有限关系", "",
        "下表状态直接来自保存 assessment，十三项均为 `scoped_source_relations_supported`。字段数量和条目数只帮助定位，不作为功能成熟度计量。", "",
        "| 原已读段落 | 新条目与正式 Pointer | 本轮具体承接 | 原文同样保留的范围 |", "| --- | --- | --- | --- |"])
    for entry in mapping["entries"]:
        repo = entry["repository"]
        marker = "C" if repo == "codepatchbay" else "W"
        original = "CODEPATCHBAY_ANALYSIS.md" if repo == "codepatchbay" else "WINWINCODE_ANALYSIS.md"
        lines.append("| " + " | ".join([f"[{repo}:{entry['original_line_anchor']}](../astra-baseline/{original}:{entry['original_line_anchor']})",
            f"`{entry['rule_id']}`；`{marker}:{entry['formal_entry_pointer']}`",
            cell(entry["intended_finite_source_relation"]), cell(entry["model_boundary_not_acceptance_gap"])]) + " |")
    lines.extend(["", "readiness 的普通记录分区与 null/缺值 unknown 分开；completion 的当前门依赖与完整前序路径条件分开，不把 readonly/docs/parent 的 verify 豁免扩大为所有门豁免。access audit 的失败 response 与 job 尾部 best-effort audit 是不同对象。上述区别是原报告有限解释的承接，不要求实际执行外部检查或网络响应。", "",
        "WorkRun 的有限状态表和依赖/活动选择已与所选 ID recheck 相连；这足以承接原文的所选检查，不要求完整领域状态机。Chat 的阶段请求身份保持独立；Worker/adapter 的 job/lease/workspace/thread/session 来源分开；outbox 的字段域一致关系不假定两条线上消息值相同。浏览器 guard 按具体 callback、正常继续和 suspension 边界保存，缺少局部 guard 没有自动归为新缺陷。", "",
        "### 旧主要链与三个 partial 的实际变化", "",
        "原六条 CPB 和十二条 WWC 主要源码规则均仍存在。CPB 的 engine 前置阻断、agent/env/sandbox、finalizer→持久结果→reconcile、job audit、trusted probe 和失败记录来源保持；WWC 的 Chat、typed dispatch、adapter/Kernel、三个不同 Kernel API 和 intent→persist→exact reconcile 保持。", "",
        "| 原 WWC partial | 正式位置与状态 | 仍保留的同等边界 |", "| --- | --- | --- |"])
    for rid in ("wwc-report-worker-bootstrap-entries", "wwc-report-worker-production-construction", "wwc-report-device-provider-deployment"):
        chain = chains["winwincode"][rid]
        lines.append(f"| `{rid}` | `W:{chain['formal_entry_pointer']}`；`{chain['assessment']['state']}`。 | 声明属性上下文修复不等于任意 trait/宏分派、运行启动或 provider 凭据可用。 |")
    lines.extend(["", "这些条目按原规则读取当前正式快照，解除的是 crate 内建编译限制属性被误当成未知宏导致的声明绑定障碍；不是把候选或同名方法强行补成唯一 CALLS。Device 部署仍保留 source-only credential/全分派边界。", "",
        "WWC 的 `wwc-report-adapter-durable-exact-turn` 与 `wwc-report-submission-intent-kernel-order` 选择同一 submit_turn 来源，正式 `/overlapping_source_selections` 已标明重叠；不能把两个条目累计成额外功能。", "",
        "### 正式 source-only gaps 原样保留", "",
        "以下 gaps 不会被 scoped 状态掩盖。它们描述源模型或原文同样未提供的效果保证；不能直接变成原报告新增未完成项。", "",
        "| 正式位置 | 保存的 gap code | 保存边界标记 |", "| --- | --- | --- |"])
    for repo, report in reports.items():
        marker = "C" if repo == "codepatchbay" else "W"
        for chain in report["functional_chains"]:
            for index, gap in enumerate(chain["analysis_gaps"]):
                flags = [f"source_only={str(gap.get('source_only')).lower()}"]
                if "necessary_to_scoped_source_relations" in gap:
                    flags.append("necessary_to_scoped_source_relations=" + str(gap["necessary_to_scoped_source_relations"]).lower())
                lines.append(f"| `{marker}:{chain['formal_entry_pointer']}/analysis_gaps/{index}` | `{gap['code']}` | {'；'.join(flags)} |")
    lines.extend(["", "### 源码范围与原冻结观察", "",
        "CPB 选入 333 份、完整解析 330 份，三份 Shell unsupported；WWC 选入 471 份、完整解析 465 份，六份 Rust parse_error。路径与原因见两正式报告的 `/coverage/unparsed_files`。这是语法捕获范围，不是功能完整率。生成合同的所选 support inputs、测试/第三方和配置排除范围按正式 `/coverage` 保留。", "",
        "旧局部 contract 的 uncertain 和图中的 dynamic/ambiguous/unresolved 继续保留；它们的口径不等于完整 judgment，也不等于目标缺少实现。循环/递归本身没有被升级为不终止缺陷。", "",
        "## 三、原本未审及更强命题边界；不作为本轮剩余目标", "",
        "原 CPB 未逐分支审核所有 CLI/workflow、HTTP/OIDC、备份/发布 provider、全部异常恢复、本地代码索引算法和所有平台/adapter；原 WWC 未穷举所有 HTTP/WS、领域状态机/并发、credential 路径、vendored Kernel、全部 publication/audit/export/connector 副作用、平台/迁移。依据是两原报告的覆盖账本及 WWC 外部交付边界。", "",
        "因此，完整协议、所有入口/分支生命周期、全授权、唯一 canonical owner、所有物理提交/外部 ack/发布/隔离效果、全故障恢复不是原报告已经完成而本轮必须补齐的命题。正式模型的相关 false 值应保留，但不能把它们列作新的验收缺口，更不能为了消除它们要求运行目标或测试。", "",
        "两正式 `/report_scope/whole_report_reproduction_claimed=false`，`/runtime_functionality_verified=false`。前者与第一节的具体报告差距分开解释，后者与原报告未运行验证的范围一致。本轮未执行、导入、测试或构建目标，也没有新增测试套件或 Astra 批准步骤。", ""])
    rendered = "\n".join(lines)
    rendered = re.sub(r"\]\(\.\./astra-baseline/([A-Z_]+\.md):(\d+)\)",
        lambda match: "](" + str(HERE.parent / "astra-baseline" / match[1]) + ":" + match[2] + ")", rendered)
    (HERE / "REPORT_SCOPE_GAPS.md").write_text(rendered, encoding="utf-8")
    print(json.dumps({"output": "REPORT_SCOPE_GAPS.md", "chain_saved_states": {repo: dict(value) for repo, value in statuses.items()},
        "new_rule_mappings": len(mapping["entries"]), "remaining_comparison_categories": ["specific Device documentation/deployment statement", "finite layer responsibility explanation"],
        "new_target_assessment_performed": False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
