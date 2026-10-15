"""Readable views of actual report values, with explicit links to full evidence.

This module performs no detection, source interpretation or benchmark lookup.
Every sentence is either an existing generated statement or display framing.
"""
from __future__ import annotations

import html
import json
from typing import Any

VERSION = "captured-human-report-markdown-2"
_LIMITS = {"semantic_rows": 18, "source_order_steps": 12,
    "declaration_summaries": 512, "conditions": 8, "value_characters": 300}
_HIDDEN = frozenset({"id", "origin", "location", "source_locations", "parse_identity", "parse_provenance",
    "source_excerpt", "source_line", "snapshot_id", "source_hash", "source_evidence_refs",
    "semantic_parse_id", "syntax_projection", "saved_syntax_projection", "reference", "binding",
    "declaration_id", "graph_node_id", "parameter_index", "argument_index", "source_selector"})
_MEANINGFUL = ("statement", "interpretation", "relation_witnesses", "comparison", "assessment",
    "conditions", "condition_source", "counterexamples", "bounds", "limitations", "necessary_gaps",
    "supported", "classification", "source_structure_supported", "ownership_assessment",
    "boolean_result", "unknown", "reason", "rejection", "source_order", "callee_source",
    "command_source", "executable_source", "args_source", "success", "record_fields",
    "expected", "actual", "value", "literal", "producer", "consumer", "status", "result")


def _visible_controls(text: str) -> str:
    return "".join("\\u" + format(ord(character), "04x")
        if ord(character) < 32 and character not in "\n\r\t" else character for character in text)


def _pointer(parent: str, key: Any) -> str:
    return parent + "/" + str(key).replace("~", "~0").replace("/", "~1")


def _text(value: Any, limit: int | None = None) -> str:
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    text = _visible_controls(text)
    bound = _LIMITS["value_characters"] if limit is None else limit
    return text if len(text) <= bound else text[:bound] + "…［展示截断；完整值见引用］"


def _cell(value: Any) -> str:
    text = value if isinstance(value, str) and value.startswith("/") else _text(value)
    return html.escape(text, quote=False).replace("`", "&#96;").replace("|", "\\|").replace("\n", "<br>")


def _code(value: Any) -> str:
    text = value if isinstance(value, str) and value.startswith("/") else _text(value)
    return "`" + html.escape(text, quote=False).replace("`", "&#96;").replace("\n", " ") + "`"


def _location(value: dict) -> str:
    return str(value.get("file", value.get("path", "位置未保留"))) + ":" + str(value.get("line", "?"))


def _paragraph(value: Any) -> str:
    return html.escape(_visible_controls(str(value)), quote=False)


def _semantic_rows(value: Any, pointer: str, maximum: int | None = None) -> list[tuple[str, Any, str]]:
    """Copy actual bounded semantic leaves; omission never changes assessment."""
    maximum = _LIMITS["semantic_rows"] if maximum is None else maximum
    result = []
    visited = 0

    def priority(key: str) -> tuple:
        return (_MEANINGFUL.index(key), key) if key in _MEANINGFUL else (len(_MEANINGFUL), key)

    def visit(item: Any, ref: str, name: str, depth: int, semantic: bool = False):
        nonlocal visited
        visited += 1
        if visited > 8192 or depth > 9 or len(result) >= maximum:
            return
        if isinstance(item, dict):
            for key in sorted(item, key=priority):
                if key in _HIDDEN or key.endswith(("_fact_ids", "_fact_id", "_ref", "_refs", "_sha256")):
                    continue
                selected = key in _MEANINGFUL or any(term in key for term in
                    ("condition", "witness", "interpretation", "boundary", "proven", "counter", "unsupported", "unknown"))
                visit(item[key], _pointer(ref, key), name + "/" + key if name else key,
                    depth + 1, semantic or selected or (depth == 0 and not isinstance(item[key], (dict, list))))
        elif isinstance(item, list):
            if semantic and all(not isinstance(child, (dict, list)) for child in item):
                result.append((name, item, ref))
            else:
                for index, child in enumerate(item[:12]):
                    visit(child, _pointer(ref, index), name + "/" + str(index), depth + 1, semantic)
        elif semantic:
            result.append((name, item, ref))

    visit(value, pointer, "", 0)
    return result


def _value_rows(rows: list[tuple[str, Any, str]]) -> list[str]:
    if not rows:
        return []
    return ["| 保存关系／条件 | 实际值 | 完整 JSON Pointer |", "| --- | --- | --- |",
        *("| " + _cell(name) + " | " + _cell(value) + " | " + _cell(ref) + " |"
          for name, value, ref in rows), ""]


def _responsibilities(report: dict) -> list[str]:
    source = report.get("architecture", {}).get("responsibility_explanations", {})
    declarations = source.get("declaration_explanations", [])
    lines = ["## 具体职责与接口交接", "",
        "以下正文由所选声明的实际记录字段、赋值、实参接口和提前退出条件生成。目录名只供导航；普通调用、消息字段、执行、交付和投影分别保留。", ""]
    if not declarations:
        return lines + ["当前没有可认证的具体职责解释；结构盘点不能代替职责结论。", ""]
    lines.extend(["完整职责、所有操作和来源：`/architecture/responsibility_explanations`。", ""])
    for index, declaration in enumerate(declarations[:_LIMITS["declaration_summaries"]]):
        owner = declaration.get("actual_owner", {})
        lines.extend(["### " + _code(declaration.get("label", "未命名声明")), "",
            _paragraph(declaration.get("summary", "没有保存可用正文。")), ""])
        guards = [statement for statement in declaration.get("statements", [])
            if statement.get("operation_kind") == "guard_rejection"]
        if guards and guards[0].get("text") not in declaration.get("summary", ""):
            lines.extend([_paragraph(guards[0]["text"]), ""])
        location = owner.get("location", {})
        lines.extend(["源码：" + _code(_location(location)) + "；完整正文与操作引用："
            + _code("/architecture/responsibility_explanations/declaration_explanations/" + str(index)) + "。", ""])
    if len(declarations) > _LIMITS["declaration_summaries"]:
        lines.extend(["其余声明的正文保留在完整职责对象；此处仅限制展示数量。", ""])
    seams = source.get("computed_source_contract_seams", [])
    if seams:
        lines.extend(["**实际装配与消息接缝**（源模型与运行效果分开）：", ""])
        for index, seam in enumerate(seams[:32]):
            lines.append("- " + _paragraph(seam.get("text", "没有保存可用解释。")) + " 原分析关系："
                + _code(seam.get("source_analysis_pointer")) + "；完整条件与来源："
                + _code("/architecture/responsibility_explanations/computed_source_contract_seams/" + str(index)) + "。")
        if len(seams) > 32:
            lines.append("- 其余接缝与完整条件保留于 `/architecture/responsibility_explanations/computed_source_contract_seams`。")
        lines.append("")
    for key, label in (("explicit_source_transfers", "显式来源交接"),
                       ("authenticated_interface_reuse", "接口复用")):
        entries = source.get(key, [])
        if entries:
            lines.extend(["**" + label + "**（列实际样例，所有关系保留）：", ""])
            for index, entry in enumerate(entries[:8]):
                lines.append("- " + _paragraph(entry.get("text", "关系无可用解释。")) + " 完整引用："
                    + _code("/architecture/responsibility_explanations/" + key + "/" + str(index)) + "。")
            lines.append("")
    if source.get("analysis_gaps") or source.get("explanation_source_gaps"):
        lines.extend(["职责分析仍有明确缺口：`/architecture/responsibility_explanations/analysis_gaps`、"
            "`/architecture/responsibility_explanations/explanation_source_gaps`；已有正文不将缺口标为通过。", ""])
    return lines


def _chain(chain: dict, index: int, entry: dict) -> list[str]:
    ref = "/functional_chains/" + str(index)
    lines = ["### " + _code(chain["rule_id"]), "",
        "分析类型：" + _code(chain.get("claim_type")) + "；源码关系："
        + _code(chain.get("assessment", {}).get("state", "unknown")) + "。", "",
        "完整关系、条件、边界与证据：" + _code(ref) + "；保存发现："
        + _code(chain.get("finding_id")) + "。", ""]
    facts = {fact.get("id"): fact for fact in chain.get("source_facts", []) if isinstance(fact, dict)}
    for role, sequence in chain.get("pattern", {}).get("sequences", {}).items():
        steps = sequence.get("steps", [])
        if not steps:
            continue
        lines.extend(["**" + _cell(role) + " 的正常源码顺序**（前序操作正常完成且分支到达时）：", ""])
        for step in steps[:_LIMITS["source_order_steps"]]:
            names = [facts[identifier]["callee_source"] for identifier in step.get("call_ids", [])
                if identifier in facts and facts[identifier].get("callee_source")]
            label = " → ".join(dict.fromkeys(names)) or step.get("statement_kind", "源码步骤")
            lines.append("- " + _code(label) + "；" + _code(_location(step.get("location", {}))) + "。")
        if len(steps) > _LIMITS["source_order_steps"]:
            lines.append("- 后续步骤保留在 " + _code(_pointer(ref + "/pattern/sequences", role)) + "。")
        lines.append("")
    lines.extend(_value_rows(_semantic_rows(chain.get("pattern", {}), ref + "/pattern")))
    for table in entry.get("presentation", {}).get("tables", []):
        lines.extend(["**有限源码分区 " + _cell(table["name"]) + "**；"
            + _code(table["full_table_ref"]) + "，展示 " + str(len(table["rows"])) + "/"
            + str(table["total_rows"]) + " 行；展示截断=" + str(table["truncated"]).lower() + "。", ""])
        columns = table["columns"]
        lines.extend(["| " + " | ".join(_cell(column) for column in [*columns, "完整行引用"]) + " |",
            "| " + " | ".join("---" for _ in range(len(columns) + 1)) + " |"])
        for row in table["rows"]:
            lines.append("| " + " | ".join(_cell(row["cells"].get(column, "展示省略；见完整行")) for column in columns)
                + " | " + _cell(row["full_row_ref"]) + " |")
        lines.append("")
    if chain.get("analysis_gaps"):
        lines.extend(["**保留的分析缺口**：", ""])
        for gap in chain["analysis_gaps"][:12]:
            lines.append("- " + _code(gap.get("code", gap)) + "；完整位置与原因见 " + _code(ref + "/analysis_gaps") + "。")
        lines.append("")
    lines.extend(["所有事实及源位置：" + _code(ref + "/source_facts") + "；配置声明单列于 "
        + _code(ref + "/policy_declarations") + "，不作为自动证据。", ""])
    return lines


def _language_coverage(report: dict) -> list[str]:
    stats, coverage = report.get("stats", {}), report.get("coverage", {})
    lines = ["### 语言、文件状态与发现范围", "",
        "以下使用快照保存的统计与能力登记。注册语言、前端可用、语法解析和功能验证分别记录；"
        "没有保存的字段保持未知，不使用当前环境补写历史结果。", "",
        "`parsed` 表示语法解析完成；`captured_metadata` 仅有文件或元数据；"
        "`structural_extracted` 表示已有结构提取但未建立完整嵌入语法校验；"
        "`parse_error` 表示解析或前端失败，保留的结构只能作为局部证据。", "",
        "| 保存状态 | 文件数 |", "| --- | --- |"]
    lines.extend("| " + _cell(status) + " | " + str(count) + " |"
        for status, count in sorted(coverage.get("file_statuses", {}).items()))
    lines.extend(["", "| 语言 | 文件 | parsed | captured_metadata | structural_extracted | parse_error | 全部状态 | 节点 | 图引用 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"])
    by_language = stats.get("by_language") or {}
    statuses = coverage.get("file_statuses_by_language", {})
    for language in sorted(set(by_language) | set(statuses)):
        counts, states = by_language.get(language, {}), statuses.get(language, {})
        row = [language, counts.get("files_total", sum(states.values())),
            *[states.get(state, 0) for state in ("parsed", "captured_metadata", "structural_extracted", "parse_error")],
            states, counts.get("nodes", "未保存"), counts.get("edges", "未保存")]
        lines.append("| " + " | ".join(_cell(value) for value in row) + " |")
    lines.extend(["", "完整语言统计：`/stats/by_language`；逐语言实际文件状态：`/coverage/file_statuses_by_language`。"
        "旧统计字段 `files_failed` 包含所有非 parsed 状态，不能把元数据捕获或结构提取一概解释为解析错误。", ""])
    capabilities = stats.get("language_capabilities")
    if isinstance(capabilities, list):
        lines.extend(["| 语言 | 前端 | 已注册 | 可用值 / 检查状态 | 项目验证状态 | 能力层次 |",
            "| --- | --- | --- | --- | --- | --- |"])
        for item in capabilities:
            row = [item.get("language"), item.get("frontend"), item.get("registered"),
                {"available": item.get("available"), "status": item.get("availability_status")},
                item.get("verification_status"), item.get("analysis_level")]
            lines.append("| " + " | ".join(_cell(value) for value in row) + " |")
    else:
        lines.append("此快照未保存 language_capabilities。")
    lines.extend(["", "完整登记（含扩展名与上游版本）：`/stats/language_capabilities`。登记或一次结构提取不表示该语言的全部语法和功能已经验证。", ""])
    inventory = stats.get("file_inventory")
    if isinstance(inventory, dict):
        unknown = inventory.get("unrecognized_files", [])
        lines.extend(["文件清单：发现普通文件 " + _code(inventory.get("regular_files_seen"))
            + "；识别为源码 " + _code(inventory.get("recognized_source_files"))
            + "；未识别 " + str(len(unknown)) + "。完整保存值：`/stats/file_inventory`。", "",
            "| 未识别文件示例（最多 24） | 扩展名 | 完整记录 |", "| --- | --- | --- |"])
        lines.extend("| " + _cell(item.get("path")) + " | " + _cell(item.get("extension"))
            + " | " + _cell("/stats/file_inventory/unrecognized_files/" + str(index)) + " |"
            for index, item in enumerate(unknown[:24]))
        lines.extend(["", "文件清单记录扫描范围内的路径；未识别文件没有因此获得源码解析或功能覆盖。", ""])
    else:
        lines.extend(["此快照未保存 file_inventory。", ""])
    return lines


def _codegraph_evidence(report: dict) -> list[str]:
    evidence = report.get("codegraph_candidate_evidence")
    if not isinstance(evidence, dict):
        return []
    counts = evidence.get("counts", {})
    lines = ["### CodeGraph 保存的结构与候选关系", "",
        "真实保存节点 " + str(counts.get("nodes", 0)) + "；候选调用类站点 "
        + str(counts.get("candidate_call_sites", 0)) + "；未绑定站点 "
        + str(counts.get("unbound_call_sites", 0)) + "；候选目标关系 "
        + str(counts.get("candidate_targets", 0)) + "。", "",
        "调用类站点包括调用、实例化和函数引用，具体类别保留在 relation_kind。"
        "这些关系只提供候选，不升级为确定调用或功能完成。confidence 是启发式排序分数，不是正确概率。", "",
        "| 节点类型 | 保存数量 |", "| --- | --- |"]
    lines.extend("| " + _cell(kind) + " | " + str(count) + " |"
        for kind, count in evidence.get("node_kinds", {}).items())
    lines.extend(["", "| 真实节点示例 | 源码位置 | 类型 | 完整节点 ID |", "| --- | --- | --- | --- |"])
    lines.extend("| " + _cell(item.get("name")) + " | " + _cell(_location(item)) + " | "
        + _cell(item.get("kind")) + " | " + _cell(item.get("node_id")) + " |"
        for item in evidence.get("node_examples", []))
    lines.extend(["", "最多展示 24 个保存站点，每站点最多 8 个候选目标；按快照顺序取样，并在两类均存在时保留候选与未绑定示例，不代表覆盖率。"
        "完整边使用本报告快照 ID 与下列完整 edge_id 定位，完整表达式与候选仍保留在图中。", "",
        "| 保存表达式 | 源码位置 | 类别 / 保存状态 | 候选数 | 完整 edge_id | 报告样例引用 |",
        "| --- | --- | --- | --- | --- | --- |"])
    for index, item in enumerate(evidence.get("examples", [])):
        ref = "/codegraph_candidate_evidence/examples/" + str(index)
        row = [item.get("expression"), _location(item),
            {"kind": item.get("relation_kind"), "resolution": item.get("resolution")},
            item.get("candidate_count"), item.get("edge_id"), ref]
        lines.append("| " + " | ".join(_cell(value) for value in row) + " |")
    lines.extend(["", "| 站点 edge_id | 候选目标 | 候选位置 | 上游启发式排序 | 完整候选记录 |",
        "| --- | --- | --- | --- | --- |"])
    for index, item in enumerate(evidence.get("examples", [])):
        for target_index, target in enumerate(item.get("targets", [])):
            row = [item.get("edge_id"), {"name": target.get("name"), "node_id": target.get("node_id")},
                _location(target), target.get("upstream_ranking", []),
                "/codegraph_candidate_evidence/examples/" + str(index) + "/targets/" + str(target_index)]
            lines.append("| " + " | ".join(_cell(value) for value in row) + " |")
    lines.extend(["", "非调用关系 " + str(counts.get("non_call_relations_in_node_metadata", 0))
        + " 条、结构关系 " + str(counts.get("structural_relations_in_node_metadata", 0))
        + " 条，保留在节点 metadata.codegraph_relations / metadata.codegraph_structure，未转成调用边。"
        "节点定位示例：`/codegraph_candidate_evidence/metadata_owner_examples`；"
        "完整汇总与采样上限：`/codegraph_candidate_evidence`。", ""])
    return lines


def render_markdown(report: dict) -> str:
    snapshot, coverage = report["snapshot"], report["coverage"]
    lines = ["# " + str(snapshot["project_name"]) + "：自动静态分析报告", "",
        "快照：" + _code(snapshot["id"]) + "；仅使用保存源码、图和静态分析证据，未执行目标、测试或构建。", "",
        "## 主要发现", ""]
    for index, judgment in enumerate(report.get("judgments", [])):
        lines.append("- **" + str(judgment["goal_id"]) + "**：" + str(judgment["summary"])
            + " 完整判断=" + _code(judgment.get("complete_assessment", False))
            + "；支持原有限判断=" + _code(judgment.get("full_goal_supported", False))
            + "；条件、反证和来源：" + _code("/judgments/" + str(index)) + "。")
    if not report.get("judgments"):
        lines.append("此快照没有配置完整条件判断；不从结构规模推断功能正确。")
    lines.extend(["", "原始完整 JSON 保留所有条件、反证、未知项、source facts 和保存发现身份。以下限制仅影响展示，不改变分析结果。", ""])
    for index, judgment in enumerate(report.get("judgments", [])):
        ref = "/judgments/" + str(index)
        lines.extend(["### " + str(judgment["goal_id"]), "",
            "保存发现：" + _code(judgment["finding_id"]) + "；证据：" + _code(judgment["evidence_id"]) + "。", ""])
        for label, key in (("推导", "derived_judgment"), ("适用条件", "conditions"),
                           ("反证与范围", "refutations"), ("必要缺口", "necessary_gaps")):
            lines.extend(["**" + label + "**：" + _code(ref + "/" + key) + "。", ""])
            lines.extend(_value_rows(_semantic_rows(judgment.get(key), ref + "/" + key, 8)))
        lines.extend(["| 必要关系 | 实际结果 |", "| --- | --- |"])
        lines.extend("| " + _cell(item.get("id")) + " | " + _cell(item.get("status")) + " |"
            for item in judgment.get("obligations", []))
        lines.append("")
    for comparison in report.get("documentation_comparisons", []):
        lines.extend(["## 文档与实际部署来源", "",
            _paragraph(comparison.get("comparison", {}).get("statement") or "所选文档与部署源码的比较仍不完整。"), "",
            "源码关系评估：" + _code(comparison.get("assessment", {}).get("state", "unknown"))
            + "；完整对照：" + _code(comparison["full_pattern_ref"]) + "。", ""])
        lines.extend(_value_rows(_semantic_rows(comparison.get("comparison", {}), comparison["full_pattern_ref"] + "/comparison", 16)))
        for index, aspect in enumerate(comparison.get("aspects", [])):
            lines.extend(["- " + _paragraph(aspect.get("statement", "未保存对照正文。"))
                + " 结果=" + _code(aspect.get("classification", "unknown")) + "；原文与来源事实："
                + _code(comparison["full_pattern_ref"] + "/documentation_comparisons/" + str(index)) + "。", ""])
    lines.extend(_responsibilities(report))
    lines.extend(["## 主要功能链、条件与反证", "",
        "源码顺序只描述同一次调用正常到达的关系；异步完成、消息传输、远端响应和物理持久化均以实际证据范围为准。", ""])
    entries = report.get("source_relation_index", {}).get("entries", [])
    for index, chain in enumerate(report.get("functional_chains", [])):
        lines.extend(_chain(chain, index, entries[index] if index < len(entries) else {}))
    lines.extend(["## 捕获范围与未审边界", "",
        "选入 " + str(coverage["files_selected"]) + " 份源码，解析 " + str(coverage["files_parsed"]) + " 份。"
        "这是源码捕获与语法解析范围，不能换算成功能完整率。", ""])
    lines.extend(_language_coverage(report))
    lines.extend(_codegraph_evidence(report))
    lines.extend([
        "| 区域 | 文件 | 已解析 |", "| --- | --- | --- |"])
    lines.extend("| " + _cell(item["directory"]) + " | " + str(item["files"]) + " | " + str(item["parsed"]) + " |"
        for item in report["architecture"]["areas"])
    lines.extend(["", "项目声明与依赖：`/project_declarations`；已绑定跨目录图引用：`/architecture/dependencies`。"
        "声明存在、路径可达和依赖计数均不证明业务行为通过。", ""])
    for source in coverage.get("unparsed_files", []):
        lines.append("- " + _code(source["file"]) + "：" + _text(source.get("status")) + "；" + _text(source.get("error")) + "。")
    lines.extend(["", "配置排除：" + _code(coverage.get("excluded", [])) + "。", "",
        "所选局部分析：`/configured_local_assessments`；完整诊断：`/diagnostics`。"
        "未建模域保持未审，不保证全仓库无缺陷、所有权或授权完整，也不将未知标为通过。", "",
        "报告生成组件：`/report_components`；原快照分析组件：`/snapshot/component_versions`。"
        "两者分别保存，历史发现不会因生成新版报告而升级。", ""])
    return "\n".join(lines) + "\n"
