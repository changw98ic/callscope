"""Render the release report from closed formal artifacts, without analysis.

This script reads saved JSON and frozen file identities. It does not open a
database, invoke an analyzer, read a target worktree, or compute new ratings.
Run only after the publisher has closed both scans and artifact builders.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import tempfile
from typing import Any

from render_report_summaries import _SavedJSON, _COUNT, _render_presentation

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parents[1]
VERSION = "saved-formal-release-report-2"
REPOSITORIES = ("codepatchbay", "winwincode")
REQUIRED = (
    "CORE_FREEZE.json", "codepatchbay-integration.json", "winwincode-integration.json",
    "codepatchbay-automatic-report.json", "winwincode-automatic-report.json", "goal-ledger.json",
    "ORIGINAL_BASELINE_COMPARISON.json", "PUBLICATION_IDENTITY.json", "REPORT_ALIGNMENT_RESULTS.json",
    "CLI_REPORT_READBACK.json",
)
_MODEL_FIELDS = {key: True for key in ("models", "model", "model_applications", "assembly_model_applications")}
_REPORT_FIELDS = {
    "snapshot": True, "coverage": True,
    "judgments": [{"goal_id": True, "finding_id": True, "evidence_id": True,
        "assessment": True, "complete_assessment": True, "full_goal_supported": True,
        "derived_judgment": True, "obligations": [{"id": True, "status": True}],
        "adapter_judgments": [{"evidence": [{"details": _MODEL_FIELDS}]}]}],
    "functional_chains": [{key: True for key in ("rule_id", "claim_type", "assessment",
        "analysis_gaps", "trusted_models", "policy_declarations")}],
    "source_relation_index": True,
    "overlapping_source_selections": True, "configured_local_assessments": _COUNT,
    "target_executed": True, "target_tests_run": True, "target_build_run": True,
}
_LEDGER_FIELDS = {
    "goals": [{"id": True, "assessment": {key: True for key in ("status", "complete_assessment", "full_goal_supported")},
        "obligations": [{"id": True, "assessment": {"status": True}}]}],
    "assessment": True,
}


def reject_constant(value: str):
    raise ValueError("Non-finite JSON constant: " + value)


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def compact(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def table_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def require(condition: bool, message: str):
    if not condition:
        raise ValueError(message)


class Inputs:
    def __init__(self):
        self.hashes: dict[str, str] = {}
        self.sizes: dict[str, int] = {}
        self.documents: dict[str, dict] = {}

    def load(self, name: str) -> dict:
        path = HERE / name
        before = path.stat()
        selection = _REPORT_FIELDS if name.endswith("-automatic-report.json") else _LEDGER_FIELDS if name == "goal-ledger.json" else None
        if selection is not None:
            document, digest = _SavedJSON(path).load(selection)
        else:
            raw = path.read_bytes()
            document = json.loads(raw.decode("utf-8"), parse_constant=reject_constant)
            digest = hashlib.sha256(raw).hexdigest()
        after = path.stat()
        require((before.st_size, before.st_mtime_ns) == (after.st_size, after.st_mtime_ns), "Input changed while reading: " + name)
        require(isinstance(document, dict), "Expected an object artifact: " + name)
        self.hashes[name], self.sizes[name] = digest, before.st_size
        self.documents[name] = document
        return document

    def unchanged(self):
        for name, expected in self.hashes.items():
            require(file_hash(HERE / name) == expected, "Input changed during release rendering: " + name)

    def observe_file(self, name: str) -> str:
        """Track a saved Markdown artifact without parsing it as JSON."""
        path = HERE / name
        require(path.resolve().parent == HERE and path.is_file(), "Expected a saved artifact in this publication: " + name)
        before = path.stat()
        digest = file_hash(path)
        after = path.stat()
        require((before.st_size, before.st_mtime_ns, before.st_ino) == (after.st_size, after.st_mtime_ns, after.st_ino),
                "Saved artifact changed while hashing: " + name)
        if name in self.hashes:
            require(self.hashes[name] == digest and self.sizes[name] == before.st_size,
                    "Previously observed saved artifact changed: " + name)
        self.hashes[name], self.sizes[name] = digest, before.st_size
        return digest


def source_inventory(freeze: dict) -> dict:
    checks = []
    for relative, expected in freeze["package_source_sha256"].items():
        path = (WORKSPACE / "callscope" / relative).resolve(strict=True)
        require(path.is_relative_to(WORKSPACE / "callscope"), "Frozen package path escapes the package")
        actual = file_hash(path)
        require(actual == expected, "Frozen core file changed: " + relative)
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        archived = HERE / "frozen-core-source" / relative
        require(archived.is_file() and file_hash(archived) == expected, "Archived core differs or is missing: " + relative)
        checks.append({"file": relative, "sha256": actual, "python_ast_parsed": True})
    benchmarks = []
    for relative, expected in freeze["benchmark_reports"].items():
        path = (HERE.parent / relative).resolve(strict=True)
        require(path.is_relative_to(HERE.parent / "astra-baseline"), "Benchmark path escapes the frozen reports")
        require(file_hash(path) == expected, "Original report bytes changed: " + relative)
        benchmarks.append({"file": relative, "sha256": expected})
    return {"file_count": len(checks), "checks": checks, "benchmark_reports": benchmarks, "new_behavior_assessment": False,
        "test_suite_run": False, "meaning": "Frozen byte identity and syntax bookkeeping only"}


def saved_model_ids(judgment: dict) -> list[str]:
    """Copy names from explicit saved model records, not source expressions."""
    identifiers = set()

    def records(value: Any):
        if isinstance(value, str):
            identifiers.add(value)
        elif isinstance(value, list):
            for item in value:
                records(item)
        elif isinstance(value, dict):
            names = [value[key] for key in ("model_id", "model") if isinstance(value.get(key), str)]
            if not names and isinstance(value.get("id"), str):
                names = [value["id"]]
            identifiers.update(names)
            for key in ("applications", "versioned_registry"):
                if key in value:
                    records(value[key])

    for adapter in judgment.get("adapter_judgments", []):
        for evidence in adapter.get("evidence", []):
            details = evidence.get("details", {})
            for key in ("models", "model", "model_applications", "assembly_model_applications"):
                if key in details:
                    records(details[key])
    return sorted(identifiers)


def gap_navigation(gaps: list[dict]) -> list[dict]:
    """Short saved code/role/locator projection; keep full gaps in manifest."""
    result = []
    for gap in gaps:
        item = {key: gap[key] for key in ("code", "role", "source_only", "source_body_available") if key in gap}
        location = gap.get("location", {})
        if location:
            item["location"] = {key: location[key] for key in ("file", "line") if key in location}
        if gap.get("source_gaps"):
            item["source_gap_codes"] = [record.get("code") for record in gap["source_gaps"]]
        result.append(item)
    return result


def validate_identity(inputs: Inputs) -> dict:
    freeze = inputs.documents["CORE_FREEZE.json"]
    require(freeze.get("package_version") == "0.13.0" and freeze.get("publication_series") == "v13",
            "Expected the formal v0.13 source freeze")
    identity = inputs.documents["PUBLICATION_IDENTITY.json"]
    comparison = inputs.documents["ORIGINAL_BASELINE_COMPARISON.json"]
    alignment = inputs.documents["REPORT_ALIGNMENT_RESULTS.json"]
    require(identity.get("verified") is True and identity.get("same_shared_component_versions") is True, "Formal publication identity is not verified")
    require(comparison.get("publication_identity_verified") is True, "Original comparison has no verified publication identity")
    require(comparison.get("baseline_total") == identity.get("observation_count"), "Original observation denominator differs")
    require(alignment.get("report_scope", {}).get("whole_report_reproduction_claimed") is False, "Alignment claims unsupported whole-report reproduction")
    repositories = {entry["repository"]: entry for entry in identity["repositories"]}
    require(set(repositories) == set(REPOSITORIES), "Publication identity must preserve both repositories")
    for repository in REPOSITORIES:
        integration = inputs.documents[repository + "-integration.json"]
        report = inputs.documents[repository + "-automatic-report.json"]
        snapshot, metadata = report["snapshot"], repositories[repository]["metadata"]
        require(snapshot["id"] == integration["snapshot_id"] == metadata["id"], "Snapshot ID differs: " + repository)
        for key in ("source_hash", "policy_hash"):
            require(snapshot[key] == integration[key] == metadata[key], "Snapshot context differs: " + repository + ":" + key)
        for key in ("analyzer_version", "detector_version"):
            require(integration[key] == freeze[key] == metadata[key], "Frozen analyzer version differs: " + repository + ":" + key)
        require(snapshot["component_versions"]["tool"] == freeze["tool_identity"], "Report uses another frozen tool: " + repository)
        require(integration["stats"]["component_versions"]["tool"] == freeze["tool_identity"], "Integration uses another frozen tool: " + repository)
        scans = integration["scans"]
        require(len(scans) == 2 and [item["phase"] for item in scans] == ["cold", "warm"], "Formal cold/warm publications are missing: " + repository)
        require(scans[0]["snapshot_id"] == scans[1]["snapshot_id"] == snapshot["id"] and scans[1]["created"] is False, "Warm publication is not the same immutable snapshot: " + repository)
        for artifact in (integration, report):
            for key in ("target_executed", "target_tests_run", "target_build_run"):
                require(artifact.get(key) is False, "Unexpected target execution in formal artifact: " + repository + ":" + key)
    # Match saved ledger statuses to the automatic reports; this copies results
    # rather than evaluating source, gate conditions, or business correctness.
    saved = {judgment["goal_id"]: judgment for repository in REPOSITORIES for judgment in inputs.documents[repository + "-automatic-report.json"]["judgments"]}
    goals = inputs.documents["goal-ledger.json"]["goals"]
    require(len(saved) == len(goals) and {goal["id"] for goal in goals} == set(saved), "Goal ledger and saved reports differ")
    for goal in goals:
        require(goal["assessment"]["status"] == saved[goal["id"]]["assessment"], "Ledger status differs: " + goal["id"])
        for key in ("complete_assessment", "full_goal_supported"):
            require(goal["assessment"][key] == saved[goal["id"]][key], "Ledger flag differs: " + goal["id"] + ":" + key)
        recorded = {item["id"].rsplit(".", 1)[-1]: item["assessment"]["status"] for item in goal["obligations"]}
        actual = {item["id"]: item["status"] for item in saved[goal["id"]]["obligations"]}
        require(recorded == actual, "Ledger obligation statuses differ: " + goal["id"])
    return repositories


def validate_cli_readback(inputs: Inputs, readback: dict) -> None:
    """Check the saved normal CLI protocol; never reopen its database or CLI."""
    repository = readback.get("repository")
    require(repository in REPOSITORIES and readback.get("kind") == "normal_saved_report_cli_readback",
            "CLI readback repository/kind is not a supported saved report")
    publication = inputs.documents[repository + "-integration.json"]
    snapshot = inputs.documents[repository + "-automatic-report.json"]["snapshot"]
    freeze = inputs.documents["CORE_FREEZE.json"]
    require(readback.get("returncode") == 0, "Normal saved-report CLI did not return successfully")
    for key in ("successful_readback", "markdown_bytes_equal", "markdown_sha256_equal",
                "logical_database_rows_schema_and_identity_unchanged", "freeze_identity_unchanged",
                "integration_and_prerequisite_state_unchanged", "formal_markdown_unchanged"):
        require(readback.get(key) is True, "CLI readback did not preserve its recorded invariant: " + key)
    for key in ("analysis_rescanned", "target_worktree_opened", "target_executed", "target_imported",
                "target_tests_run", "target_build_run", "tool_test_suite_run", "synthetic_fixture_used"):
        require(readback.get(key) is False, "CLI readback has an unexpected action flag: " + key)
    for key in ("source_hash", "policy_hash"):
        require(readback.get(key) == publication[key] == snapshot[key], "CLI readback saved context differs: " + key)
    require(readback.get("snapshot_id") == publication["snapshot_id"] == snapshot["id"], "CLI readback snapshot differs")
    identity = readback.get("identity", {})
    for key in ("package_version", "publication_series", "analyzer_version", "detector_version", "schema_version",
                "tool_identity", "pyproject_sha256", "policy_files", "effective_policy_sha256"):
        require(identity.get(key) == freeze.get(key), "CLI readback frozen identity differs: " + key)
    require(identity.get("freeze_sha256") == inputs.hashes["CORE_FREEZE.json"], "CLI readback freeze bytes differ")
    require(identity.get("package_module_count") == len(freeze["package_source_sha256"]), "CLI readback package inventory differs")
    for collection in ("formal_publications", "formal_publications_after_cli"):
        records = readback.get(collection, {})
        require(set(records) == set(REPOSITORIES), "CLI readback lacks both formal publication prerequisites")
        for repo in REPOSITORIES:
            recorded, formal = records[repo], inputs.documents[repo + "-integration.json"]
            require(recorded.get("integration_sha256") == inputs.hashes[repo + "-integration.json"],
                    "CLI readback integration bytes differ: " + repo)
            require(all(recorded.get(key) == formal[key] for key in ("snapshot_id", "source_hash", "policy_hash")),
                    "CLI readback publication metadata differs: " + repo)
            require(recorded.get("database_closed") is True and recorded.get("wal", {}).get("empty_or_absent") is True,
                    "CLI readback prerequisite database was not recorded closed: " + repo)
            require(Path(recorded.get("database", "")).resolve() == HERE / (repo + "-v13.sqlite3"),
                    "CLI readback refers to a different saved database: " + repo)
    reference_name, exported_name = repository + "-automatic-report.md", repository + "-cli-report-readback.md"
    require(Path(readback.get("reference_artifact", "")).resolve() == HERE / reference_name,
            "CLI readback formal Markdown path differs from its actual repository")
    require(Path(readback.get("exported_artifact", "")).resolve() == HERE / exported_name,
            "CLI readback exported Markdown path differs from its actual repository")
    reference_hash, exported_hash = inputs.observe_file(reference_name), inputs.observe_file(exported_name)
    require(readback.get("reference_sha256") == reference_hash == exported_hash == readback.get("exported_sha256"),
            "CLI saved Markdown bytes/hash differ from the formal publication")
    before, after = readback.get("database_before", {}), readback.get("database_after", {})
    for key in ("logical_content_sha256", "table_records", "schema_sha256", "application_id", "user_version"):
        require(key in before and before[key] == after.get(key), "CLI database logical fingerprint differs: " + key)
    require(before.get("wal", {}).get("empty_or_absent") is True and after.get("wal", {}).get("empty_or_absent") is True,
            "CLI readback left or began with an unclosed WAL")
    require(isinstance(before.get("database_file_sha256"), str) and isinstance(after.get("database_file_sha256"), str),
            "CLI readback physical database fingerprints are missing")
    require(readback.get("database_physical_bytes_unchanged") is (before["database_file_sha256"] == after["database_file_sha256"]),
            "CLI readback physical-change flag disagrees with its saved fingerprints")
    initialization = readback.get("ordinary_tool_store_initialization", {})
    require(initialization.get("normal_store_constructor_invoked") is True
            and initialization.get("connection_was_not_readonly") is True
            and initialization.get("initialization_physical_effects_were_permitted_and_measured") is True
            and initialization.get("publish_scan_or_decision_command_invoked") is False,
            "CLI readback must preserve its ordinary Store initialization boundary")


def summarize(inputs: Inputs, identities: dict, syntax: dict) -> dict:
    freeze, ledger = inputs.documents["CORE_FREEZE.json"], inputs.documents["goal-ledger.json"]
    comparison, alignment = inputs.documents["ORIGINAL_BASELINE_COMPARISON.json"], inputs.documents["REPORT_ALIGNMENT_RESULTS.json"]
    goals, chains, projects = [], [], []
    for repository in REPOSITORIES:
        report, integration = inputs.documents[repository + "-automatic-report.json"], inputs.documents[repository + "-integration.json"]
        goals.extend({"repository": repository, **{key: item.get(key) for key in ("goal_id", "assessment", "complete_assessment", "full_goal_supported", "derived_judgment", "finding_id", "evidence_id")},
            "saved_model_ids": saved_model_ids(item),
            "obligation_statuses": dict(Counter(obligation["status"] for obligation in item["obligations"])), "obligation_count": len(item["obligations"])} for item in report["judgments"])
        chains.extend({"repository": repository, "rule_id": item["rule_id"], "claim_type": item["claim_type"],
            "assessment": item["assessment"], "analysis_gaps": item["analysis_gaps"],
            "trusted_models": item["trusted_models"], "policy_declarations": item["policy_declarations"],
            "saved_relation_presentation": next((entry for entry in report.get("source_relation_index", {}).get("entries", [])
                if entry.get("rule_id") == item["rule_id"]), None)} for item in report["functional_chains"])
        projects.append({"repository": repository, "snapshot": report["snapshot"], "coverage": report["coverage"],
            "scans": [{key: item[key] for key in ("phase", "snapshot_id", "created", "status")} for item in integration["scans"]],
            "node_count": integration["stats"]["nodes"], "edge_count": integration["stats"]["edges"],
            "scope_changes": identities[repository]["scope_changes"],
            "overlapping_source_selections": report.get("overlapping_source_selections", []),
            "configured_local_assessment_count": report["configured_local_assessments"]})
    baseline_counts = Counter()
    for repository in comparison["repositories"]:
        baseline_counts.update(repository["counts"])
    chain_states = Counter(item["assessment"].get("state", "unknown") for item in chains)
    return {"builder_version": VERSION, "generated_at": datetime.now(timezone.utc).isoformat(), "freeze": {
        "package_version": freeze["package_version"], "publication_series": freeze["publication_series"],
        "analyzer_version": freeze["analyzer_version"], "detector_version": freeze["detector_version"],
        "schema_version": freeze["schema_version"], "tool_identity": freeze["tool_identity"]},
        "projects": projects, "goals": goals, "goal_count": len(goals),
        "complete_assessment_count": sum(item["complete_assessment"] is True for item in goals),
        "original_claim_supported_count": sum(item["full_goal_supported"] is True for item in goals),
        "obligation_count": sum(item["obligation_count"] for item in goals), "recorded_goal_status_counts": ledger["assessment"]["goal_status_counts"],
        "recorded_obligation_status_counts": ledger["assessment"]["obligation_status_counts"],
        "chains": chains, "chain_count": len(chains), "chain_states": dict(chain_states),
        "captured_source_structure_supported_count": sum(item["assessment"].get("captured_source_structure_supported") is True for item in chains),
        "scoped_source_supported_count": sum(item["assessment"].get("scoped_source_supported") is True for item in chains),
        "baseline_total": comparison["baseline_total"], "selected_baseline_total": comparison["selected_total"], "baseline_counts": dict(baseline_counts),
        "baseline_change_count": sum(len(item["changes"]) for item in comparison["repositories"]),
        "referenced_raw_file_count": inputs.documents["PUBLICATION_IDENTITY.json"]["referenced_raw_file_count"],
        "target_commit_checks": [{"repository": repository, **{key: identities[repository]["target_identity"][key]
            for key in ("frozen_commit", "actual_commit", "commit_matches", "live_referenced_source_hashes_match", "saved_referenced_source_hashes_match", "working_tree_clean_claimed")}}
            for repository in REPOSITORIES],
        "alignment_catalog": alignment["catalog_preservation"], "alignment_report_scope": alignment["report_scope"],
        "identity_verified": inputs.documents["PUBLICATION_IDENTITY.json"]["verified"], "syntax_bookkeeping": syntax,
        "input_artifacts": [{"file": name, "sha256": inputs.hashes[name], "bytes": inputs.sizes[name]} for name in inputs.hashes],
        "stream_projection": {"file": "render_report_summaries.py", "sha256": file_hash(HERE / "render_report_summaries.py"),
            "retained": "report summaries, explicit model slots and ledger statuses only; original evidence unchanged"},
        "normal_cli_report_readback": inputs.documents.get("CLI_REPORT_READBACK.json"),
        "scope_gap_navigation_available": (HERE / "REPORT_SCOPE_GAPS.md").is_file(),
        "behavior": {"only_saved_artifacts_and_frozen_core_read": True, "database_opened": False, "analyzer_invoked": False,
            "new_rating_computed": False, "reviewer_approval_added": False, "target_workspace_read": False,
            "target_imported_or_executed": False, "target_tests_run": False, "target_build_run": False, "tool_test_suite_run": False}}


def render(summary: dict) -> str:
    freeze = summary["freeze"]
    lines = [f"# CallScope v{freeze['package_version']}：原报告范围内的自动静态判断", "",
        "本轮以原 [CodePatchBay](../astra-baseline/CODEPATCHBAY_ANALYSIS.md) 和 [WinWinCode](../astra-baseline/WINWINCODE_ANALYSIS.md) 分析报告为功能基准。具体判断、主要链的源码关系、项目结构盘点和全文范围对照分别保存；没有新增重复 Astra 审批。", "",
        f"正式保存结果包含 {summary['goal_count']} 项原判断、{summary['obligation_count']} 项关系：{summary['complete_assessment_count']} 项完整裁决，{summary['original_claim_supported_count']} 项完整支持原 claim。这是本题样本的实际结果，不是全项目功能覆盖率或缺陷通过率。", "",
        "目标未导入、执行、测试、构建或安装；工具测试套件未运行。结果来自受信工具的正常静态冷/暖扫描和保存产物。", "",
        "## 配置判断的保存结果", "", "| 仓库 | 原判断 | 保存评估 | 完整裁决 | 支持原 claim | 必要关系状态 |", "| --- | --- | --- | --- | --- | --- |"]
    for item in summary["goals"]:
        row = (item["repository"], item["goal_id"], item["assessment"], item["complete_assessment"], item["full_goal_supported"], compact(item["obligation_statuses"]))
        lines.append("| " + " | ".join(table_cell(value) for value in row) + " |")
    lines.extend(["", "以下结论逐字复制正式报告的 `derived_judgment` 字段；条件、反证、policy 不变量与模型适用范围保存在两库自动报告和 [goal-ledger.json](goal-ledger.json)。账本复制正式保存状态，没有重新评分。", ""])
    for item in summary["goals"]:
        judgment = item["derived_judgment"]
        lines.append(f"- **{item['goal_id']}**：{judgment if isinstance(judgment, str) else compact(judgment)}")
    lines.extend(["", "旧 pending/assignment、finalizer、不同重试预算、opaque supervisor、导航与提交环境、Device/Chat/local 分支及失败操作仍各自限制结论。", "",
        "## 主要链、结构与全文范围", "",
        f"正式报告有 {summary['chain_count']} 个所选主要链条目；源码关系状态为 `{compact(summary['chain_states'])}`。其中 `captured_source_structure_supported=true` 为 {summary['captured_source_structure_supported_count']} 项，`scoped_source_supported=true` 为 {summary['scoped_source_supported_count']} 项。结构抽取与包含实际装配/guard 的源码支持是不同字段；partial 条目保留具体缺段。", "",
        "这些条目描述所选声明和正常分支的静态关系，均不自动证明完整运行功能。相同源 selector 的重叠在自动报告单列，不累计为额外能力；目录、依赖图、解析文件及 AST anchor 数量也不构成功能覆盖率。", ""])
    boundaries = [item for item in summary["chains"] if item["analysis_gaps"]]
    relation_types = {"conditional_gate_relations", "event_index_projection", "trusted_command_lineage",
        "unsupported_record_retention", "browser_async_lifecycle", "resource_writer_ownership",
        "rust_finite_state_selection", "message_identity_relations"}
    specific = [item for item in summary["chains"] if item["claim_type"] in relation_types]
    if specific:
        lines.extend(["## 本轮保存的具体条件与字段关系", "",
            "以下只复制正式报告 v2 的关系投影，包含实际门条件、状态枚举、记录字段与必要未知；不是根据规则名生成新结论。完整表达式、source facts 与反证以相应 JSON Pointer 为准。", ""])
        for item in specific:
            lines.extend([f"### `{item['rule_id']}`", "",
                f"保存状态 `{item['assessment'].get('state')}`；保存缺口 `{compact(gap_navigation(item['analysis_gaps']))}`。", ""])
            if item["saved_relation_presentation"]:
                lines.extend(_render_presentation(item["saved_relation_presentation"], item["repository"] + "-automatic-report.json",
                    table_limit=2, row_limit=12, leaf_limit=24))
            else:
                lines.extend(["此项未保存关系展示索引；不由摘要补造，参阅完整自动报告。", ""])
    if boundaries:
        lines.extend(["`scoped_source_relations_supported` 也不表示全部 `analysis_gaps` 为空；以下既含 partial，也含已支持条目保留的 source-only 边界。表中只复制 gap code、角色和文件位置，完整记录保存在自动报告与输入清单。", "", "| 保留边界的链 | 保存状态 | 保存分析缺段导航 |", "| --- | --- | --- |"])
        for item in boundaries:
            lines.append("| " + " | ".join(table_cell(value) for value in (item["rule_id"], item["assessment"].get("state"), compact(gap_navigation(item["analysis_gaps"])))) + " |")
        lines.append("")
    catalog = summary["alignment_catalog"]
    lines.extend([f"[全文范围对照](REPORT_ALIGNMENT_RESULTS.json) 保留原目录的 {catalog['section_count']} 个章节、{catalog['statement_count']} 个段落/表格行/列表项。该数量是证据导航清单，未给每段文字、建议或业务职责重新评级。`whole_report_reproduction_claimed={str(summary['alignment_report_scope']['whole_report_reproduction_claimed']).lower()}`；更广职责、安全、部署和原未审范围仍不能由五项判断或所选链替代。", "",
        "## 正式来源与捕获范围", "", "| 仓库 | 正式快照 | 状态 | 选入 / 解析 | 图节点 / 边 | 冷 / 暖创建 |", "| --- | --- | --- | --- | --- | --- |"])
    for project in summary["projects"]:
        snapshot, coverage, scans = project["snapshot"], project["coverage"], project["scans"]
        lines.append("| " + " | ".join(table_cell(value) for value in (project["repository"], "`" + snapshot["id"] + "`", snapshot["status"], f"{coverage['files_selected']} / {coverage['files_parsed']}", f"{project['node_count']} / {project['edge_count']}", f"{scans[0]['created']} / {scans[1]['created']}")) + " |")
    lines.extend(["", "两库冷、暖扫描各自保持同一不可变 snapshot，暖扫描 `created=false`。缓存情况由 integration 中的 maintenance 记录保存；不能据此宣称每文件增量依赖分析。源码捕获/解析状态仍与功能判断分开。", "",
        "## 模型、policy 与 input scope 的变化", "",
        "下列 model ID 从保存判断的显式模型记录复制，既不是运行验证，也不是新增能力计数。模型的实际源码适用关系、条件和 policy 条目以原 evidence 为准；主要链自己的 `trusted_models` 与 `policy_declarations` 另存于自动报告。", "", "| 配置判断 | 保存的显式模型 |", "| --- | --- |"])
    for item in summary["goals"]:
        lines.append("| " + " | ".join(table_cell(value) for value in (item["goal_id"], compact(item["saved_model_ids"]))) + " |")
    lines.extend(["", "policy 和 inert 支持输入的实际变化如下，本轮不作同条件精度或缺陷率比较。", ""])
    for project in summary["projects"]:
        scope = project["scope_changes"]
        changed = [entry["section"] for entry in scope.get("changed_sections", [])]
        support = project["coverage"].get("support_inputs", [])
        lines.append(f"- **{project['repository']}**：policy 字节相同=`{str(scope['policy_bytes_identical']).lower()}`；变化 section=`{compact(changed)}`；捕获 source hash 与 v12 相同=`{str(not scope['repository_source_hash_changed_since_previous']).lower()}`。inert 支持输入 {len(support)} 项；原引用源文件 hash 与 target commit 由 publication identity 单独核对。")
    lines.extend(["", "输入捕获范围改变不等于目标代码发生修改。受信模型和环境条件不填补尚未建立的源连接；旧 field/IR 的 unknown 不因新局部 record 关系被升级。无运行、浏览器、网络、并发或业务验收证明。", "",
        "## 原 26 条观察与交付身份", "",
        f"原冻结观察保留 {summary['baseline_total']} 条，总计比较 {summary['selected_baseline_total']} 条，状态为 `{compact(summary['baseline_counts'])}`；相对 v12 的保存变化记录为 {summary['baseline_change_count']} 项。evidence_only 和指定 unknown 仍遵循原 evaluator；观察重现数量不是完整功能判断数量。", "",
        f"包版本 `{freeze['package_version']}`，analyzer `{freeze['analyzer_version']}`，detector `{freeze['detector_version']}`，schema `{freeze['schema_version']}`。冻结 tool source hash：`{freeze['tool_identity']['source_hash']}`。", "",
        f"[CORE_FREEZE.json](CORE_FREEZE.json) 的 {summary['syntax_bookkeeping']['file_count']} 份核心 Python 源码 live/archive hash 一致，AST 可解析；此项只是身份/语法核对。正式身份产物记录原引用的 {summary['referenced_raw_file_count']} 份文件 saved/live hash 一致，两库 target commit 一致；没有宣称工作区 clean。两库和共有组件的正式 publication identity 已验证；本报告没有再次执行检测器或读取数据库。", "",
        "- [CodePatchBay 自动报告](codepatchbay-automatic-report.md)与[扫描记录](codepatchbay-integration.json)。",
        "- [WinWinCode 自动报告](winwincode-automatic-report.md)与[扫描记录](winwincode-integration.json)。",
        "- [CodePatchBay 简明分析](codepatchbay-analysis-summary.md)、[WinWinCode 简明分析](winwincode-analysis-summary.md)。",
        "- [原五项结果账本](goal-ledger.json)、[原 26 条比较](ORIGINAL_BASELINE_COMPARISON.json)、[正式身份](PUBLICATION_IDENTITY.json)。",
        "- [全文范围对照](REPORT_ALIGNMENT_RESULTS.json)、[本报告输入与核对记录](RELEASE_REPORT_INPUTS.json)。", ""])
    if summary["normal_cli_report_readback"] is not None:
        readback = summary["normal_cli_report_readback"]
        repository = readback["repository"]
        name = {"codepatchbay": "CodePatchBay", "winwincode": "WinWinCode"}[repository]
        lines.extend([f"[正常 report CLI 读回记录](CLI_REPORT_READBACK.json) 确认 {name} 的 [导出 Markdown]({repository}-cli-report-readback.md) 与[正式 Markdown]({repository}-automatic-report.md) 字节一致，属于保存快照 `{readback['snapshot_id']}`。该 CLI 没有重扫或重算检测器；普通 Store 初始化已记录，其连接不是只读连接，前后逻辑行/Schema/身份指纹保持一致。数据库物理字节相同=`{str(readback['database_physical_bytes_unchanged']).lower()}`，不把初始化视为无物理效果。本生成器只核对保存记录及 Markdown hash，没有重跑 CLI 或打开数据库。", ""])
    if summary["scope_gap_navigation_available"]:
        lines.extend(["[原全文与当前自动报告的具体差距](REPORT_SCOPE_GAPS.md) 分列原已读但尚无同等自动结论的段落、源码边界与原明确未审范围；其导航不增加新评分或审批。", ""])
    return "\n".join(lines)


def write_atomic(path: Path, data: bytes):
    require(path.resolve().parent == HERE and not path.exists(), "Write a new artifact in this iteration only: " + str(path))
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=HERE, prefix=".release-report-", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--formal-artifacts-closed", action="store_true", help="Publisher has finished both scans and formal artifact builders")
    parser.add_argument("--output", type=Path, default=HERE / "REPORT.md")
    parser.add_argument("--manifest", type=Path, default=HERE / "RELEASE_REPORT_INPUTS.json")
    args = parser.parse_args()
    missing = [name for name in REQUIRED if not (HERE / name).is_file()]
    if not args.formal_artifacts_closed or missing:
        print(compact({"state": "not_ready", "formal_artifacts_closed": args.formal_artifacts_closed, "missing_artifacts": missing, "formal_report_written": False}))
        return 2
    for destination in (args.output, args.manifest):
        require(destination.resolve().parent == HERE and not destination.exists(), "Expected a new artifact in this iteration: " + str(destination))
    text_inputs = ("codepatchbay-automatic-report.md", "winwincode-automatic-report.md",
        "codepatchbay-analysis-summary.md", "winwincode-analysis-summary.md", "REPORT_SCOPE_GAPS.md")
    for name in text_inputs:
        require((HERE / name).is_file(), "Closed report navigation file is missing: " + name)
    inputs = Inputs()
    for name in REQUIRED:
        inputs.load(name)
    for name in text_inputs:
        inputs.observe_file(name)
    validate_cli_readback(inputs, inputs.documents["CLI_REPORT_READBACK.json"])
    identities = validate_identity(inputs)
    syntax = source_inventory(inputs.documents["CORE_FREEZE.json"])
    summary = summarize(inputs, identities, syntax)
    markdown = render(summary).encode("utf-8")
    summary["report"] = {"file": args.output.name, "sha256": hashlib.sha256(markdown).hexdigest(), "bytes": len(markdown)}
    summary["builder_source_sha256"] = file_hash(Path(__file__))
    inputs.unchanged()
    write_atomic(args.manifest, (json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8"))
    write_atomic(args.output, markdown)
    print(compact({"state": "written", "report": str(args.output), "manifest": str(args.manifest), "goal_count": summary["goal_count"],
        "obligation_count": summary["obligation_count"], "chain_count": summary["chain_count"], "new_rating_computed": False}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
