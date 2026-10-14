"""Readable views of actual report values, with explicit links to full evidence.

This module performs no detection, source interpretation or benchmark lookup.
Every sentence is either an existing generated statement or display framing.
"""
from __future__ import annotations

import html
import json
from typing import Any

VERSION = "captured-human-report-markdown-1"
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
        "这是源码捕获与语法解析范围，不能换算成功能完整率。", "",
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
