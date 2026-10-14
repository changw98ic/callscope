"""Versioned multi-language orchestration over captured source, never execution."""

from collections import Counter
from copy import deepcopy
from dataclasses import replace
from datetime import datetime, timezone
import fnmatch
import hashlib
import json
from pathlib import Path

from .analyzer import analyze_python_project
from .config import load_config, validate_config
from .models import ANALYZER_VERSION, DETECTOR_VERSION, PARSER_VERSION, SCHEMA_VERSION, Diagnostic, Edge, GraphSnapshot, Node, project_id_for
from .parsers import parser_version
from .source_reader import scan_sources
from .analysis_inputs import tool_identity
from .input_capture import capture_support_inputs, INPUT_CAPTURE_VERSION


def _digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def _failed_frontend(files, language, reason):
    changed = [replace(source, status="parse_error", error=reason) if source.status == "captured" else source for source in files]
    return {"nodes": [], "edges": [], "files": changed,
            "diagnostics": [Diagnostic("warning", "language_frontend_failed", f"{language}: {reason}")],
            "stats": {"coverage_incomplete": True}}


def _language_stats(files, nodes, edges):
    counts = Counter(edge.resolution for edge in edges)
    return {
        "files_total": len(files), "files_parsed": sum(source.status == "parsed" for source in files),
        "files_failed": sum(source.status != "parsed" for source in files), "nodes": len(nodes), "edges": len(edges),
        **{f"{state}_calls": counts[state] for state in ("resolved", "external", "dynamic", "ambiguous", "unresolved")},
        "external_callback_boundaries": sum(edge.resolution == "external" and bool(edge.metadata.get("callbacks_unknown") or edge.metadata.get("callable_arguments")) for edge in edges),
    }


def frontend_versions(language):
    if language == "python":
        return {"analyzer": "python-ast-3-captured", "parser": PARSER_VERSION}
    if language == "typescript":
        from . import typescript_analyzer as frontend
    elif language == "rust":
        from . import rust_analyzer as frontend
    else:
        raise ValueError(f"未注册语言前端：{language}")
    versions = {"analyzer": frontend.ANALYZER_VERSION, "parser": parser_version(language)}
    if language == "typescript":
        versions["tsx_parser"] = parser_version("tsx")
    return versions


def execute_frontend(language, files, project_root, policy):
    """Fixed registered code, supplied captured text; no executable plugins."""
    if not files:
        return {"nodes": [], "edges": [], "files": [], "diagnostics": [], "stats": {}}
    if language == "python":
        python_policy = deepcopy(policy)
        python_policy["analysis"]["languages"] = ["python"]
        python = analyze_python_project(project_root, python_policy, captured_files=files)
        return {"nodes": python.nodes, "edges": python.edges, "files": python.files,
                "diagnostics": python.diagnostics, "stats": python.stats}
    if language == "typescript":
        from . import typescript_analyzer as frontend
    elif language == "rust":
        from . import rust_analyzer as frontend
    else:
        raise ValueError(f"未注册语言前端：{language}")
    return frontend.analyze_files(files, project_root, policy)


def analyze_project(root: str | Path, config: dict | None = None, *, frontend_runner=None) -> GraphSnapshot:
    lexical = Path(root).expanduser().absolute()
    if lexical.is_symlink():
        raise ValueError("项目根不能是符号链接")
    project_root = lexical.resolve()
    if not project_root.is_dir():
        raise ValueError(f"项目根不存在：{project_root}")
    policy = deepcopy(load_config(project_root) if config is None else validate_config(config))
    policy["analysis"].pop("_captured_support_inputs", None)
    captured, diagnostics, scope = scan_sources(project_root, policy)
    input_evidence, input_diagnostics = capture_support_inputs(
        project_root, policy["analysis"]["support_inputs"], policy["analysis"]["max_file_bytes"])
    diagnostics.extend(input_diagnostics)
    for source in captured:
        support = input_evidence.get(source.path)
        if support is not None and support["status"] == "captured":
            if source.hash != support["hash"] or source.content != support["content"]:
                raise RuntimeError("同一路径的源码与辅助输入捕获不一致；未发布快照，请重新扫描")
    runtime_policy = deepcopy(policy)
    # This internal value always comes from safe capture, never caller data.
    runtime_policy["analysis"]["_captured_support_inputs"] = input_evidence
    languages = policy["analysis"]["languages"]
    implementation = tool_identity()
    prepared = frontend_runner.run(project_root, runtime_policy, captured, implementation) if frontend_runner else None
    nodes = []
    edges = []
    final_files = {source.path: source for source in captured}
    frontend_stats = {}
    component_versions = {"tool": implementation, "maintenance": prepared["maintenance"] if prepared else {"backend": "full"},
                          "support_input_capture": INPUT_CAPTURE_VERSION}
    if policy.get("static_contracts"):
        from .static_contracts import CONTRACT_ANALYZER_VERSION, CONTRACT_POLICY_VERSION
        component_versions["static_contracts"] = {"analyzer": CONTRACT_ANALYZER_VERSION,
                                                   "policy_schema": CONTRACT_POLICY_VERSION}
    if policy.get("value_contracts"):
        from .value_analysis import VERSION, POLICY_VERSION
        component_versions["value_contracts"] = {"analyzer": VERSION, "policy_schema": POLICY_VERSION}
    if any(policy.get(key) for key in ("navigation_contracts", "atomicity_contracts", "field_contracts", "budget_contracts", "goal_contracts", "report_claims")):
        from .semantic_sources import VERSION as SEMANTIC_SOURCE_VERSION
        from .lexical_bindings import VERSION as LEXICAL_BINDINGS_VERSION
        from .semantic_environment import VERSION as ENVIRONMENT_VERSION
        from .completion_summaries import VERSION as COMPLETION_VERSION
        component_versions["semantic_sources"] = SEMANTIC_SOURCE_VERSION
        component_versions["lexical_bindings"] = LEXICAL_BINDINGS_VERSION
        component_versions["semantic_environment"] = ENVIRONMENT_VERSION
        component_versions["completion_summaries"] = COMPLETION_VERSION
    if policy.get("navigation_contracts"):
        from .navigation_analysis import VERSION, POLICY_VERSION
        component_versions["navigation_contracts"] = {"analyzer": VERSION, "policy_schema": POLICY_VERSION}
        if any(rule.get("wiring") for rule in policy["navigation_contracts"]):
            from .port_wiring import VERSION as PORT_WIRING_VERSION
            component_versions["port_wiring"] = PORT_WIRING_VERSION
    if policy.get("atomicity_contracts"):
        from .atomicity_analysis import VERSION, POLICY_VERSION
        component_versions["atomicity_contracts"] = {"analyzer": VERSION, "policy_schema": POLICY_VERSION}
    if policy.get("field_contracts"):
        from .field_analysis import VERSION, POLICY_VERSION
        from .field_summaries import VERSION as FIELD_SUMMARY_VERSION
        from .semantic_ir import VERSION as SEMANTIC_IR_VERSION
        from .field_relations import VERSION as FIELD_RELATIONS_VERSION
        component_versions["field_contracts"] = {"analyzer": VERSION, "policy_schema": POLICY_VERSION}
        component_versions["field_summaries"] = FIELD_SUMMARY_VERSION
        component_versions["semantic_ir"] = SEMANTIC_IR_VERSION
        component_versions["field_relations"] = FIELD_RELATIONS_VERSION
    if policy.get("budget_contracts"):
        from .budget_analysis import VERSION, POLICY_VERSION
        component_versions["budget_contracts"] = {"analyzer": VERSION, "policy_schema": POLICY_VERSION}
    if policy.get("goal_contracts"):
        from .goal_registry import component_versions as goal_versions
        component_versions["goal_contracts"] = goal_versions(policy["goal_contracts"])
    if policy.get("report_claims"):
        from .report_chain_analysis import VERSION, POLICY_VERSION
        component_versions["report_claims"] = {"analyzer": VERSION, "policy_schema": POLICY_VERSION}
    for language in languages:
        files = [source for source in captured if source.language == language]
        if prepared:
            component_versions[language] = prepared["versions"][language]
            result = prepared["results"][language]
        else:
            try:
                component_versions[language] = frontend_versions(language)
                result = execute_frontend(language, files, project_root, runtime_policy)
            except (ImportError, OSError, ValueError, RuntimeError, RecursionError) as exc:
                component_versions.setdefault(language, {"analyzer": f"{language}-unavailable", "parser": PARSER_VERSION})
                result = _failed_frontend(files, language, str(exc))
        for node in result["nodes"]:
            node.metadata.setdefault("language", language)
        nodes.extend(result["nodes"])
        edges.extend(result["edges"])
        diagnostics.extend(result["diagnostics"])
        frontend_stats[language] = result.get("stats", {})
        for source in result["files"]:
            final_files[source.path] = source
    files = sorted(final_files.values(), key=lambda source: source.path)
    failed_paths = {source.path for source in files if source.status != "parsed"}
    by_id = {node.id: node for node in nodes}
    sanitized = []
    for edge in edges:
        source_node = by_id.get(edge.source)
        target_node = by_id.get(edge.target)
        failed = edge.file in failed_paths or (source_node and source_node.file in failed_paths) or (target_node and target_node.file in failed_paths)
        if edge.resolution == "resolved" and failed:
            metadata = {**edge.metadata, "incomplete_source": True}
            edge = replace(edge, target=None, resolution="ambiguous", candidates=sorted(set(edge.candidates + ([edge.target] if edge.target else []))),
                           reason="调用或端点所在源码未完整解析，不能作为确定见证", metadata=metadata)
        sanitized.append(edge)
    edges = sorted(sanitized, key=lambda edge: (edge.file, edge.line, edge.column, edge.id))
    for node in nodes:
        matched = sorted(layer for layer, patterns in policy.get("layers", {}).items()
                         if any(fnmatch.fnmatchcase(value, pattern) for pattern in patterns for value in (node.id, node.qualname, node.module)))
        node.layer = matched[0] if len(matched) == 1 else None
        if len(matched) > 1:
            if node.metadata.get("candidate_layers") != matched:
                diagnostics.append(Diagnostic("warning", "layer_ambiguous", f"节点 {node.id} 同时匹配多个层：{', '.join(matched)}", node.file, node.line))
            node.metadata["candidate_layers"] = matched
        else:
            node.metadata.pop("candidate_layers", None)
        if any(fnmatch.fnmatchcase(node.id, pattern) or fnmatch.fnmatchcase(node.qualname, pattern) for pattern in policy.get("entrypoints", [])):
            node.metadata["entrypoint"] = True
    nodes.sort(key=lambda node: node.id)
    node_languages = {node.id: ("typescript" if node.metadata.get("language") == "javascript" else node.metadata.get("language")) for node in nodes}
    by_language = {}
    for language in languages:
        by_language[language] = _language_stats(
            [source for source in files if source.language == language],
            [node for node in nodes if node_languages.get(node.id) == language],
            [edge for edge in edges if node_languages.get(edge.source) == language],
        )
    overall = _language_stats(files, nodes, edges)
    support_incomplete = any(record["status"] != "captured" for record in input_evidence.values())
    coverage = bool(failed_paths or support_incomplete or scope["symlinks_skipped"] or scope["scan_errors"] or any(value.get("coverage_incomplete") for value in frontend_stats.values()))
    ambiguous = sum(bool(node.metadata.get("duplicate_definition")) for node in nodes)
    call_incomplete = bool(overall["dynamic_calls"] or overall["ambiguous_calls"] or overall["unresolved_calls"] or overall["external_callback_boundaries"] or ambiguous
                           or any(value.get("call_resolution_incomplete") for value in frontend_stats.values()))
    if not any(source.status == "parsed" for source in files):
        coverage = True
        diagnostics.append(Diagnostic("warning", "no_parsed_sources", "扫描范围没有可完整解析的实现源码，不能认为项目已经分析。"))
    incomplete = coverage or call_incomplete
    versions = json.dumps(component_versions, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    source_hash = _digest({"files": [(source.path, source.hash, source.status, source.module, source.error) for source in files], "scope": scope,
                           "support_inputs": input_evidence})
    policy_hash = _digest(policy)
    project_id = project_id_for(project_root)
    snapshot_id = _digest({"project_id": project_id, "source_hash": source_hash, "policy_hash": policy_hash,
                          "analyzer_version": ANALYZER_VERSION, "detector_version": DETECTOR_VERSION,
                          "schema_version": SCHEMA_VERSION, "parser_version": versions})
    stats = {
        **scope, **overall, "by_language": by_language, "languages_requested": languages,
        "supported_languages": ["python", "typescript", "rust"], "frontend_stats": frontend_stats,
        "component_versions": component_versions, "rules_count": len(policy.get("rules", [])),
        "entrypoints_count": len(policy.get("entrypoints", [])), "ambiguous_symbols": ambiguous,
        "static_contracts_count": len(policy.get("static_contracts", [])),
        "value_contracts_count": len(policy.get("value_contracts", [])),
        "navigation_contracts_count": len(policy.get("navigation_contracts", [])),
        "atomicity_contracts_count": len(policy.get("atomicity_contracts", [])),
        "field_contracts_count": len(policy.get("field_contracts", [])),
        "budget_contracts_count": len(policy.get("budget_contracts", [])),
        "goal_contracts_count": len(policy.get("goal_contracts", [])),
        "report_claims_count": len(policy.get("report_claims", [])),
        "support_input_capture_version": INPUT_CAPTURE_VERSION,
        "support_inputs_count": len(input_evidence), "support_inputs_incomplete": support_incomplete,
        "coverage_incomplete": coverage, "call_resolution_incomplete": call_incomplete, "incomplete": incomplete,
        "resolution_model": "explicit static lexical bindings; no target execution",
        "limitations": ["静态路径不证明条件、调用顺序、值、输出或功能正确性", "回调、对象/trait 分派、宏和跨语言运行机制保留未知",
                        "配置排除的第三方、测试及生成源码不在覆盖承诺中", "快照是读取到的源码集合，不是工作区原子捕获"],
    }
    diagnostics.sort(key=lambda item: (item.file, item.line, item.code, item.message))
    if tool_identity() != implementation:
        raise RuntimeError("分析期间工具代码发生变化；保留旧快照，请重新扫描")
    return GraphSnapshot(snapshot_id, project_id, policy["project"].get("name") or project_root.name,
                         str(project_root), datetime.now(timezone.utc).isoformat(), source_hash, ANALYZER_VERSION,
                         policy_hash, "partial" if incomplete else "complete", nodes, edges, files, diagnostics, stats, policy,
                         detector_version=DETECTOR_VERSION, schema_version=SCHEMA_VERSION, parser_version=versions,
                         input_evidence=input_evidence)
