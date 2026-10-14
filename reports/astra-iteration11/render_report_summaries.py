"""Render small navigation summaries of closed, saved v13 report artifacts.

This artifact utility imports only the standard library. It reads each saved
automatic-report.json and integration.json in sequence, projects selected JSON
fields without retaining the large evidence trees, and copies existing report
statements. It does not open a database, target source, reference report, or
analysis module; it never supplies a new judgment or changes original evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


_SKIP = object()
_COUNT = object()
_STRING_MARK = re.compile(r'["\\]')
_CONTAINER_MARK = re.compile(r'[{}\[\]"]')
_SCALAR_END = re.compile(r'[,}\]\s]')
_SPACE = re.compile(r'\s*')
_CHUNK = 262144


class _OptionalProjection:
    """Skip a differently shaped field in a heterogeneous saved collection.

    The mismatch marker never pretends to be a value/count of the requested
    shape. Relevant report records still require exact matching afterward.
    """
    def __init__(self, selection: Any):
        self.selection = selection


class _SavedJSON:
    """Forward-only projection; discarded source evidence stays on disk."""

    def __init__(self, path: Path):
        self.path = path
        self.stream = path.open("r", encoding="utf-8", newline="")
        self.before = path.stat()
        self.buffer = ""
        self.position = 0
        self.digest = hashlib.sha256()

    def _more(self) -> bool:
        if self.position < len(self.buffer):
            return True
        self.buffer = self.stream.read(_CHUNK)
        self.position = 0
        self.digest.update(self.buffer.encode("utf-8"))
        return bool(self.buffer)

    def _peek(self) -> str:
        return self.buffer[self.position] if self._more() else ""

    def _take(self) -> str:
        char = self._peek()
        if not char:
            raise ValueError(f"Unexpected end of saved JSON: {self.path.name}")
        self.position += 1
        return char

    def _space(self) -> None:
        while self._more():
            self.position = _SPACE.match(self.buffer, self.position).end()
            if self.position < len(self.buffer):
                return

    def _expect(self, char: str) -> None:
        self._space()
        if self._take() != char:
            raise ValueError(f"Expected {char!r} in saved JSON: {self.path.name}")

    def _string(self, keep: bool) -> str | None:
        self._expect('"')
        parts = ['"'] if keep else None
        while self._more():
            mark = _STRING_MARK.search(self.buffer, self.position)
            if mark is None:
                if parts is not None:
                    parts.append(self.buffer[self.position:])
                self.position = len(self.buffer)
                continue
            if parts is not None:
                parts.append(self.buffer[self.position:mark.end()])
            self.position = mark.end()
            if mark.group() == '"':
                return json.loads("".join(parts)) if parts is not None else None
            escaped = self._take()
            if parts is not None:
                parts.append(escaped)
        raise ValueError(f"Unclosed JSON string: {self.path.name}")

    def _scalar(self, keep: bool) -> Any:
        parts = [] if keep else None
        consumed = False
        while self._more():
            end = _SCALAR_END.search(self.buffer, self.position)
            stop = end.start() if end is not None else len(self.buffer)
            consumed = consumed or stop > self.position
            if parts is not None:
                parts.append(self.buffer[self.position:stop])
            self.position = stop
            if end is not None:
                break
        if not consumed:
            raise ValueError(f"Missing JSON value: {self.path.name}")
        return json.loads("".join(parts)) if parts is not None else None

    def _skip(self) -> None:
        self._space()
        char = self._peek()
        if char == '"':
            self._string(False)
        elif char in ("{", "["):
            stack = [self._take()]
            while stack and self._more():
                mark = _CONTAINER_MARK.search(self.buffer, self.position)
                if mark is None:
                    self.position = len(self.buffer)
                    continue
                self.position = mark.start()
                token = mark.group()
                if token == '"':
                    self._string(False)
                    continue
                self.position += 1
                if token in ("{", "["):
                    stack.append(token)
                else:
                    if stack.pop() != ("{" if token == "}" else "["):
                        raise ValueError(f"Unbalanced saved JSON: {self.path.name}")
            if stack:
                raise ValueError(f"Unclosed saved JSON: {self.path.name}")
        else:
            self._scalar(False)

    def value(self, selection: Any, pointer: str = "") -> Any:
        self._space()
        if isinstance(selection, _OptionalProjection):
            requested = selection.selection
            expected = "[" if requested is _COUNT or isinstance(requested, list) else "{" if isinstance(requested, dict) else None
            if expected is not None and self._peek() != expected:
                actual = self._peek()
                self._skip()
                return {"_projection_shape_mismatch": True, "expected_json_prefix": expected,
                        "actual_json_prefix": actual, "actual_value_retained": False}
            selection = requested
        if selection is _SKIP:
            self._skip()
            return None
        char = self._peek()
        if char == "{":
            if selection is not True and not isinstance(selection, dict):
                raise ValueError(f"Object projection does not match: {self.path.name}#{pointer}")
            self._take()
            result = {}
            self._space()
            if self._peek() == "}":
                self._take()
                return result
            while True:
                key = self._string(True)
                self._expect(":")
                child = True if selection is True else selection.get(key, _SKIP)
                item = self.value(child, pointer + "/" + key.replace("~", "~0").replace("/", "~1"))
                if child is not _SKIP:
                    result[key] = item
                self._space()
                token = self._take()
                if token == "}":
                    return result
                if token != ",":
                    raise ValueError(f"Missing object separator: {self.path.name}")
        if char == "[":
            if selection is not True and selection is not _COUNT and not isinstance(selection, list):
                raise ValueError(f"Array projection does not match: {self.path.name}#{pointer}")
            self._take()
            count, result = 0, []
            child = _SKIP if selection is _COUNT else True if selection is True else selection[0]
            self._space()
            if self._peek() == "]":
                self._take()
                return 0 if selection is _COUNT else result
            while True:
                item = self.value(child, pointer + "/" + str(count))
                count += 1
                if selection is not _COUNT:
                    result.append(item)
                self._space()
                token = self._take()
                if token == "]":
                    return count if selection is _COUNT else result
                if token != ",":
                    raise ValueError(f"Missing array separator: {self.path.name}")
        if selection is not True:
            raise ValueError(f"Projection shape does not match: {self.path.name}#{pointer}")
        return self._string(True) if char == '"' else self._scalar(True)

    def load(self, selection: dict) -> tuple[dict, str]:
        try:
            result = self.value(selection)
            self._space()
            if self._peek():
                raise ValueError(f"Trailing saved JSON content: {self.path.name}")
            after = self.path.stat()
            if (self.before.st_size, self.before.st_mtime_ns, self.before.st_ino) != (
                after.st_size, after.st_mtime_ns, after.st_ino
            ):
                raise ValueError(f"Artifact changed while reading: {self.path.name}")
            return result, self.digest.hexdigest()
        finally:
            self.stream.close()


_REPORT_SELECTION = {
    "version": True,
    "snapshot": True,
    "coverage": {"files_selected": True, "files_parsed": True, "file_statuses": True,
        "unparsed_files": True, "support_inputs": _COUNT, "selection_scope": True,
        "excluded": True, "meaning": True},
    "architecture": {"areas": True, "dependencies": _COUNT, "meaning": True},
    "project_declarations": True,
    "judgments": [{"goal_id": True, "finding_id": True, "evidence_id": True,
        "analysis_type": True, "assessment": True, "summary": True,
        "complete_assessment": True, "full_goal_supported": True, "derived_judgment": True,
        "obligations": [{"id": True, "status": True}], "necessary_gaps": True,
        "saved_evidence_pointer": True}],
    "functional_chains": [{"rule_id": True, "finding_id": True, "evidence_id": True,
        "claim_type": True, "assessment": True, "source_scope": True,
        "analysis_gaps": True, "saved_evidence_pointer": True}],
    "source_relation_index": True,
    "overlapping_source_selections": True,
    "configured_local_assessments": _COUNT,
    "graph_observation_counts": True,
    "report_scope": True,
    "diagnostics": _COUNT,
    "target_executed": True, "target_tests_run": True,
    "target_build_run": True, "runtime_functionality_verified": True,
}
_STATS_SELECTION = {key: True for key in (
    "files_total", "files_parsed", "files_failed", "nodes", "edges", "resolved_calls",
    "external_calls", "dynamic_calls", "ambiguous_calls", "unresolved_calls",
    "external_callback_boundaries", "goal_contracts_count", "report_claims_count",
)}
_INTEGRATION_SELECTION = {
    "repository": True, "snapshot_id": True, "package_version": True,
    "publication_series": True, "source_hash": True, "policy_hash": True,
    "analyzer_version": True, "detector_version": True, "comparison": True,
    "stats": _STATS_SELECTION,
    "scans": [{"phase": True, "snapshot_id": True, "created": True, "status": True,
        "maintenance": {"engine": True, "language_updates": True, "detection": True,
            "frontend": True}}],
    "target_executed": True, "target_imported": True, "target_tests_run": True,
    "target_build_run": True,
}
_LABELS = {
    "cpb-report-engine-stage-chain": "runJob 主链与前置阻断",
    "cpb-report-job-audit-best-effort": "audit best-effort 分支",
    "cpb-report-trusted-probe-command-source": "trusted probe 命令来源",
    "cpb-report-unsupported-probe-evidence": "unsupported probe 失败证据",
    "cpb-report-conditional-delivery-result": "finalizer → 结果写入 → reconcile",
    "cpb-report-agent-execution-policy": "agent allowlist / env / sandbox 策略",
    "wwc-report-workrun-state-guards": "WorkRun 校验与重复 guard",
    "wwc-report-submission-intent-kernel-order": "intent → persist → exact reconcile",
    "wwc-report-device-provider-deployment": "Device provider 部署分流",
    "wwc-report-worker-bootstrap-entries": "Worker 入口分支",
    "wwc-report-worker-production-construction": "生产 Worker 构造",
    "wwc-report-worker-typed-dispatch": "Worker typed dispatch",
    "wwc-report-production-adapter-embedded-kernel": "ProductionAdapter → Kernel 构造",
    "wwc-report-adapter-durable-exact-turn": "Adapter durable / exact turn",
    "wwc-report-kernel-create-session-interface": "Kernel create_session 接口",
    "wwc-report-kernel-submit-turn-interface": "Kernel submit_turn 接口",
    "wwc-report-kernel-reconcile-exact-interface": "Kernel reconcile_turn_exact 接口",
    "wwc-report-chat-delivery-workrun-requests": "Chat 请求与 WorkItem / WorkRun",
    "cpb-report-readiness-abrupt-guard": "readiness 提交前保护",
    "cpb-report-completion-gate-conditions": "完成门条件与豁免",
    "cpb-report-access-audit-response": "访问审计与响应字段",
    "cpb-event-index-projection": "事件提交与索引投影",
    "cpb-trusted-command-lineage": "可信命令的字段来源",
    "cpb-unsupported-record-retention": "未支持方法的失败记录",
    "cpb-captured-record-resource-writers": "CodePatchBay 记录与资源写者",
    "wwc-report-workrun-finite-selection": "WorkRun 可运行状态与依赖条件",
    "wwc-report-chat-retained-request-identities": "Chat 请求身份与字段保留",
    "wwc-report-worker-adapter-record-identities": "Worker 与 Adapter 的消息身份",
    "wwc-report-outbox-ack-correlation-fields": "发件记录与确认关联字段",
    "wwc-browser-continuation-lifecycle": "渲染代次与异步回写条件",
    "wwc-captured-record-resource-writers": "WinWinCode 记录与资源写者",
}


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _cell(value: Any) -> str:
    return str(value).replace("|", "&#124;").replace("\n", " ").replace("\r", " ")


def _link(filename: str, pointer: str) -> str:
    return f"[{pointer}]({filename}#{pointer})"


def _gap_codes(gaps: list) -> str:
    # Codes are copied, never interpreted into a new assessment.
    if not gaps:
        return "`[]`"
    return ", ".join("`" + str(item.get("code", _json(item))) + "`" for item in gaps)


def _render_presentation(entry: dict, filename: str, *, table_limit: int = 3,
                         row_limit: int = 12, leaf_limit: int = 24) -> list[str]:
    """Display only the report v2's saved bounded projection; infer no claims."""
    presentation = entry.get("presentation", {})
    if presentation.get("presentation_only") is not True:
        return []
    lines = [f"保存的具体关系（仅展示投影，不增加分析或评分；每链至多 {table_limit} 表、每表 {row_limit} 行及 {leaf_limit} 个字段）：", ""]
    display_truncated = len(presentation.get("tables", [])) > table_limit
    for table in presentation.get("tables", [])[:table_limit]:
        columns = table.get("columns", [])
        lines.extend([f"`{table['name']}`；完整 {_link(filename, table['full_table_ref'])}；保存总行数 `{table['total_rows']}`。", "",
            "| " + " | ".join(_cell(key) for key in [*columns, "完整行"]) + " |",
            "| " + " | ".join("---" for _ in [*columns, "完整行"]) + " |"])
        for row in table.get("rows", [])[:row_limit]:
            cells = []
            for key in columns:
                saved_cells = row.get("cells", {})
                if key not in saved_cells:
                    cells.append("显示投影省略；见完整行")
                    continue
                value = saved_cells[key]
                text = value if isinstance(value, str) else _json(value)
                cells.append(_cell(text[:600] + "…（显示省略）" if len(text) > 600 else text))
            cells.append(_link(filename, row["full_row_ref"]))
            lines.append("| " + " | ".join(cells) + " |")
        if table.get("truncated") or len(table.get("rows", [])) > row_limit:
            lines.append("表格为显示子集；省略项和原条件见完整表指针，不作为分析缺口。")
        if len(table.get("rows", [])) > row_limit:
            display_truncated = True
        lines.append("")
    leaves = []
    def visit(value: Any, path: str, reference: str, depth: int = 0):
        nonlocal display_truncated
        if len(leaves) >= leaf_limit:
            display_truncated = True
            return
        if isinstance(value, dict):
            # Compact projection can introduce shown_items/source_fact_refs.
            # Keep the original containing-value ref, never invent a raw JSON
            # pointer through these presentation-only wrapper fields.
            reference = value.get("full_value_ref", reference)
            if value.get("omitted_for_presentation"):
                leaves.append((path, "显示投影省略", value.get("full_value_ref", reference)))
                return
            for key, child in value.items():
                if key in {"source_fact_refs", "full_value_ref", "full_location_ref", "remaining_fields_ref"}:
                    continue
                visit(child, path + "/" + key, reference, depth + 1)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, path + "/" + str(index), reference, depth + 1)
        else:
            text = value if isinstance(value, str) else _json(value)
            leaves.append((path, text[:600] + "…（显示省略）" if len(text) > 600 else text, reference))
    for section in presentation.get("sections", []):
        visit(section.get("value"), section["name"], section["full_value_ref"])
    if leaves:
        lines.extend(["| 保存关系字段 | 保存值 | 原值位置 |", "| --- | --- | --- |"])
        lines.extend("| " + " | ".join((_cell(path), _cell(value), _link(filename, reference))) + " |"
                     for path, value, reference in leaves)
        lines.append("")
    lines.extend([f"完整关系 {_link(filename, entry['pattern_ref'])}；原 source facts {_link(filename, entry['source_facts_ref'])}。原投影截取标志 `{_json(presentation.get('truncated'))}`；本摘要预算截取标志 `{_json(display_truncated)}`。更多字段、表格及完整条件回原关系指针；所有 unknown/false 依原保存值，显示省略不改变原分析。", ""])
    return lines


def _validate_closed(repository: str, report: dict, integration: dict) -> None:
    if integration.get("repository") != repository or integration.get("publication_series") != "v13":
        raise ValueError("Expected the matching formal v13 integration artifact")
    for key in ("source_hash", "policy_hash"):
        if report["snapshot"][key] != integration[key]:
            raise ValueError(f"Saved report/integration {key} differs")
    snapshot_id = report["snapshot"]["id"]
    phases = integration.get("scans", [])
    if (integration.get("snapshot_id") != snapshot_id or len(phases) != 2
        or [item.get("phase") for item in phases] != ["cold", "warm"]
        or any(item.get("snapshot_id") != snapshot_id for item in phases)
        or phases[1].get("created") is not False):
        raise ValueError("Cold/warm saved publications have not closed with one immutable identity")
    for key in ("target_executed", "target_tests_run", "target_build_run"):
        if report.get(key) is not False or integration.get(key) is not False:
            raise ValueError(f"Saved static artifact does not retain {key}=false")


def _render(repository: str, report: dict, integration: dict, hashes: dict[str, str]) -> str:
    name = "CodePatchBay" if repository == "codepatchbay" else "WinWinCode"
    original = "CODEPATCHBAY_ANALYSIS.md" if repository == "codepatchbay" else "WINWINCODE_ANALYSIS.md"
    report_file, integration_file = (f"{repository}-automatic-report.json", f"{repository}-integration.json")
    snapshot, coverage, stats = report["snapshot"], report["coverage"], integration["stats"]
    lines = [f"# {name} · 保存的自动分析摘要", "",
        "此摘要只展示已保存正式报告的结果和证据导航；不重新分析、不新增评价，也不替代完整证据。",
        "五项判断是实现追踪，不是全文报告或项目功能覆盖率。链标题只是规则 ID 的展示标签。", "",
        f"- 固定全文基准：[原分析报告](../astra-baseline/{original})；不设置重复 Astra 审批步骤。",
        f"- 完整自动报告：[Markdown]({repository}-automatic-report.md) / [JSON]({report_file})；[正式 integration]({integration_file})。",
        f"- 快照：`{snapshot['id']}`；状态：`{snapshot['status']}`；报告版本：`{report['version']}`。",
        f"- 实现：`{integration['package_version']}` / `{integration['analyzer_version']}` / `{integration['detector_version']}`。",
        f"- 源码身份：`{snapshot['source_hash']}`。",
        f"- 策略身份：`{snapshot['policy_hash']}`。",
        f"- 保存 JSON SHA256：`{hashes['report']}`；integration SHA256：`{hashes['integration']}`。",
        f"- 保存比较范围：{integration['comparison']}", "",
        "## 保存范围与结构盘点", "",
        f"选入 `{coverage['files_selected']}` 文件，完整解析 `{coverage['files_parsed']}`；文件状态 `{_json(coverage['file_statuses'])}`。",
        f"调用图保存 `{stats['nodes']}` 节点、`{stats['edges']}` 边；确定调用 `{stats['resolved_calls']}`。这些是结构统计。",
        f"外部 `{stats['external_calls']}` / 动态 `{stats['dynamic_calls']}` / 歧义 `{stats['ambiguous_calls']}` / 未解析 `{stats['unresolved_calls']}`；外部回调边界 `{stats['external_callback_boundaries']}`。",
        f"捕获辅助原文 `{coverage['support_inputs']}`；源根 `{_json(coverage['selection_scope'])}`。完整范围见 {_link(report_file, '/coverage')}。", "",
        "下表仅展示文件数最多的 12 个保存目录条目；目录名不是推断出的运行职责。", "",
        "| 保存目录 | 文件 / 解析 | 语言文件数 |",
        "| --- | --- | --- |"]
    areas = sorted(report["architecture"]["areas"], key=lambda item: (-item["files"], item["directory"]))
    lines.extend(f"| `{_cell(item['directory'])}` | {item['files']} / {item['parsed']} | `{_cell(_json(item['languages']))}` |"
        for item in areas[:12])
    lines.extend(["", f"全部目录 `{len(areas)}`，保存的确定跨目录依赖条目 `{report['architecture']['dependencies']}`；来源见 {_link(report_file, '/architecture')}。",
        "依赖样本仅来自已确定图连接，不证明动态可达、执行顺序或职责正确性。", "",
        "## 捕获的项目声明", "",
        "manifest、脚本名称、依赖及文档标题都是捕获声明；没有执行脚本或验证依赖实际可用。", "",
        "| 保存 manifest | 格式 | 保存名称 / 版本 |",
        "| --- | --- | --- |"])
    declarations = report["project_declarations"]
    for manifest in declarations["manifests"]:
        declared = manifest.get("declarations", manifest.get("package_declarations", {}))
        lines.append(f"| `{_cell(manifest['file'])}` | `{manifest['format']}` | `{_cell(_json({'name':declared.get('name'),'version':declared.get('version')}))}` |")
    lines.extend(["", f"声明文档 `{len(declarations['documentation'])}`，声明缺口 `{_json(declarations['gaps'])}`；详见 {_link(report_file, '/project_declarations')}。", "",
        "## 已保存的完整条件判断", "",
        "以下 summary、derived_judgment、完整性/支持性和义务状态直接复制；成立条件与反证保留原 JSON 指针。", ""])
    for index, judgment in enumerate(report["judgments"]):
        pointer = f"/judgments/{index}"
        states = ", ".join(f"{item['id']}={item['status']}" for item in judgment["obligations"])
        lines.extend([f"### `{judgment['goal_id']}`", "", judgment["summary"], "",
            f"derived_judgment：`{_json(judgment['derived_judgment'])}`",
            f"assessment=`{judgment['assessment']}`；complete=`{_json(judgment['complete_assessment'])}`；support=`{_json(judgment['full_goal_supported'])}`。",
            f"必要义务（原状态）：`{states}`；必要缺口：{_gap_codes(judgment['necessary_gaps'])}。",
            f"Finding=`{judgment['finding_id']}`；Evidence=`{judgment['evidence_id']}`；保存 evidence 指针=`{judgment['saved_evidence_pointer']}`（相对于该 Finding）。",
            f"完整 {_link(report_file, pointer)}；条件 {_link(report_file, pointer+'/conditions')}；反证 {_link(report_file, pointer+'/refutations')}；缺口 {_link(report_file, pointer+'/necessary_gaps')}。", ""])
    lines.extend(["## 所选主要源码链", "",
        "显示每条保存规则的实际 assessment 和缺口；source-structure 支持与目标分派闭合分开。", ""])
    for index, chain in enumerate(report["functional_chains"]):
        assessment, pointer = chain["assessment"], f"/functional_chains/{index}"
        label = _LABELS.get(chain["rule_id"], chain["rule_id"])
        lines.extend([f"### {label} · `{chain['rule_id']}`", "",
            f"`{chain['claim_type']}`；state=`{assessment.get('state')}`；scoped_source_supported=`{_json(assessment.get('scoped_source_supported'))}`；captured_source_structure_supported=`{_json(assessment.get('captured_source_structure_supported'))}`。",
            f"保存缺口：{_gap_codes(chain['analysis_gaps'])}；Finding=`{chain['finding_id']}`；Evidence=`{chain['evidence_id']}`。",
            f"源码/关系 {_link(report_file, pointer)}；缺段 {_link(report_file, pointer+'/analysis_gaps')}；模型 {_link(report_file, pointer+'/trusted_models')}；policy {_link(report_file, pointer+'/policy_declarations')}；evidence 指针=`{chain['saved_evidence_pointer']}`（相对于该 Finding）。", ""])
        entry = next((entry for entry in report.get("source_relation_index", {}).get("entries", [])
                      if entry.get("rule_id") == chain["rule_id"]), None)
        if entry:
            lines.extend(_render_presentation(entry, report_file))
    lines.extend(["## 未解析与未审边界", "",
        f"- 全文复现声明：`{_json(report['report_scope']['whole_report_reproduction_claimed'])}`；未建模功能域不视为已覆盖：`{_json(report['report_scope']['unmodeled_functional_domains_are_not_approved'])}`。",
        f"- 局部配置评估 `{report['configured_local_assessments']}` 条；重复源选择 `{len(report['overlapping_source_selections'])}` 组，见 {_link(report_file, '/overlapping_source_selections')}，不合计为新增覆盖。",
        f"- 保存诊断 `{report['diagnostics']}`；文件缺口见 {_link(report_file, '/coverage/unparsed_files')}，诊断见 {_link(report_file, '/diagnostics')}。",
        f"- 源码排除规则：`{_json(coverage['excluded'])}`。",
        "- 标准模型、正常到达和生产装配条件只按各项保存范围成立；未知字段/分派、特殊语言语义及任意并发不被摘要补齐。",
        "- 嵌套 async/callback 的源码正文不是执行轨迹；候选方法不是已验证 runtime provider。",
        f"- 保存 target_executed=`{_json(report['target_executed'])}` / target_tests_run=`{_json(report['target_tests_run'])}` / target_build_run=`{_json(report['target_build_run'])}` / runtime_functionality_verified=`{_json(report['runtime_functionality_verified'])}`。",
        "- 上方 `#/...` 为 JSON Pointer 导航；查看器若不支持该 fragment，请在原 JSON 按指针定位。指针与 Finding/Evidence 身份应一起阅读。", "",
        "## 正式保存轮次", "",
        "| 轮次 | 保存状态 | 新建快照 | 相同快照 ID |",
        "| --- | --- | --- |"])
    lines.extend(f"| `{item['phase']}` | `{item['status']}` | `{_json(item['created'])}` | `{item['snapshot_id']}` |"
        for item in integration["scans"])
    lines.extend(["", f"这张表复制保存发布记录；partial 是图/解析范围状态，不能据此覆盖上方判断结论。完整记录见 [integration]({integration_file})。", ""])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--formal-artifacts-closed", action="store_true",
                        help="Publisher has explicitly closed both formal scan/report artifact sets")
    parser.add_argument("--directory", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    if not args.formal_artifacts_closed:
        parser.error("Run only after the publisher explicitly closes both formal artifact sets; pass --formal-artifacts-closed then")
    directory = args.directory.resolve()
    if directory != Path(__file__).resolve().parent:
        parser.error("Render only into this iteration's own directory")
    repositories = ("codepatchbay", "winwincode")
    # Both integrations must exist before processing either report.
    for repository in repositories:
        for suffix in ("automatic-report.json", "integration.json"):
            if not (directory / f"{repository}-{suffix}").is_file():
                raise SystemExit(f"Both formal artifact sets must close first: {repository}-{suffix}")
        if (directory / f"{repository}-analysis-summary.md").exists():
            raise SystemExit("Existing formal summaries are immutable; choose a new publication directory")
    for repository in repositories:
        report, report_hash = _SavedJSON(directory / f"{repository}-automatic-report.json").load(_REPORT_SELECTION)
        integration, integration_hash = _SavedJSON(directory / f"{repository}-integration.json").load(_INTEGRATION_SELECTION)
        _validate_closed(repository, report, integration)
        markdown = _render(repository, report, integration, {"report": report_hash, "integration": integration_hash})
        destination = directory / f"{repository}-analysis-summary.md"
        destination.write_text(markdown, encoding="utf-8")
        print(_json({"repository": repository, "file": destination.name,
            "lines": len(markdown.splitlines()), "report_sha256": report_hash,
            "integration_sha256": integration_hash, "new_assessment_generated": False}))
        del report, integration, markdown


if __name__ == "__main__":
    main()
