"""Static call-structure facts and explicitly configured constraints.

The detectors do not execute tests or target code. Every conclusion is scoped
to the source snapshot and the analyzer's resolved-call model. There is no
universal risk score, and human review state belongs to the separate store.
"""

from fnmatch import fnmatchcase
from hashlib import sha256
import json
from typing import Any

from .graph import GraphIndex, _edge_gap, _external_callback_gap
from .models import DETECTOR_VERSION, Evidence, Finding, GraphSnapshot


GAP_EVIDENCE_SAMPLE_LIMIT = 8


def _gap_evidence_summary(gaps: list[dict[str, Any]]) -> dict[str, Any]:
    """Bound presentation evidence, never the gap set used for a decision.

The immutable snapshot retains full call edges, diagnostics and source states.
Serializing every entrypoint gap for every unreachable node previously created
quadratic reports; a count and explicit sample preserve uncertainty and scope.
"""
    sample = gaps[:GAP_EVIDENCE_SAMPLE_LIMIT]
    return {
        "gaps": sample,
        "gap_count": len(gaps),
        "gaps_truncated": len(gaps) > len(sample),
        "gap_sample_limit": GAP_EVIDENCE_SAMPLE_LIMIT,
        "full_gap_evidence": "snapshot_edges_diagnostics_and_source_statuses",
    }


def _hash(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256(raw.encode("utf-8")).hexdigest()


def _locations(index: GraphIndex, node_ids: list[str], edge_ids: list[str]) -> list[dict[str, Any]]:
    locations = []
    seen = set()
    for edge_id in edge_ids:
        edge = index.edges[edge_id]
        item = (edge.file, edge.line, edge.column)
        if item not in seen:
            seen.add(item)
            locations.append({"file": edge.file, "line": edge.line, "column": edge.column})
    for node_id in node_ids:
        node = index.nodes.get(node_id)
        if node is None:
            continue
        item = (node.file, node.line, 0)
        if item not in seen:
            seen.add(item)
            locations.append({"file": node.file, "line": node.line, "column": 0})
    return locations


def _finding(
    index: GraphIndex,
    *,
    kind: str,
    severity: str,
    status: str,
    title: str,
    description: str,
    identity: Any,
    node_ids: list[str] | None = None,
    edge_ids: list[str] | None = None,
    rule_id: str = "",
    details: dict[str, Any] | None = None,
) -> Finding:
    nodes = list(dict.fromkeys(node_ids or []))
    edges = list(dict.fromkeys(edge_ids or []))
    fingerprint = _hash({"type": kind, "subject": identity})
    finding_id = "finding:" + _hash([index.snapshot.id, fingerprint])[:32]
    evidence_details = dict(details or {})
    if "gaps" in evidence_details:
        gaps = evidence_details["gaps"]
        original_count = evidence_details.get("gap_count", len(gaps))
        already_truncated = evidence_details.get("gaps_truncated", False)
        evidence_details.update(_gap_evidence_summary(gaps))
        evidence_details["gap_count"] = original_count
        evidence_details["gaps_truncated"] = bool(already_truncated) or original_count > len(evidence_details["gaps"])
        evidence_details["gap_snapshot_id"] = index.snapshot.id
    locations = _locations(index, nodes, edges)
    seen_locations = {
        (item["file"], item["line"], item["column"]) for item in locations
    }
    for gap in evidence_details.get("gaps", []):
        if not gap.get("file"):
            continue
        location = {
            "file": gap["file"], "line": gap.get("line", 1) or 1,
            "column": gap.get("column", 0),
        }
        identity_location = (location["file"], location["line"], location["column"])
        if identity_location not in seen_locations:
            locations.append(location)
            seen_locations.add(identity_location)
    evidence = Evidence(
        id="evidence:" + _hash([index.snapshot.id, fingerprint, "static"])[0:32],
        kind="static_call_graph",
        message=description,
        locations=locations,
        node_ids=nodes,
        edge_ids=edges,
        details={
            "snapshot_id": index.snapshot.id,
            "source_hash": index.snapshot.source_hash,
            "analyzer_version": index.snapshot.analyzer_version,
            "parser_version": getattr(index.snapshot, "parser_version", "unknown"),
            "schema_version": getattr(index.snapshot, "schema_version", "unknown"),
            "detector_version": DETECTOR_VERSION,
            "policy_hash": index.snapshot.policy_hash,
            "executed": False,
            "completeness_scope": "explicit_static_call_model",
            "model_limits": ["implicit_magic_calls", "runtime_registration", "external_implementations"],
            **evidence_details,
        },
    )
    return Finding(
        id=finding_id, type=kind, severity=severity, status=status,
        title=title, description=description, node_ids=nodes, edge_ids=edges,
        evidence=[evidence], rule_id=rule_id, fingerprint=fingerprint,
        snapshot_id=index.snapshot.id,
        metadata={
            "detector_version": DETECTOR_VERSION,
            "interpretation": "仅为静态结构事实或相对显式规则的发现，不保证运行行为。",
        },
    )


def _components(index: GraphIndex) -> list[list[str]]:
    """Iterative Kosaraju SCC; robust to chains longer than Python's stack."""
    outgoing = {
        node: sorted({edge.target for edge in edges if edge.target is not None})
        for node, edges in index.outgoing.items()
    }
    incoming = {
        node: sorted({edge.source for edge in edges})
        for node, edges in index.incoming.items()
    }
    seen: set[str] = set()
    finished = []
    for seed in sorted(index.nodes):
        if seed in seen:
            continue
        seen.add(seed)
        stack = [(seed, 0)]
        while stack:
            node, position = stack[-1]
            neighbors = outgoing[node]
            if position < len(neighbors):
                other = neighbors[position]
                stack[-1] = (node, position + 1)
                if other not in seen:
                    seen.add(other)
                    stack.append((other, 0))
            else:
                stack.pop()
                finished.append(node)
    assigned: set[str] = set()
    components = []
    for seed in reversed(finished):
        if seed in assigned:
            continue
        assigned.add(seed)
        members = []
        stack = [seed]
        while stack:
            node = stack.pop()
            members.append(node)
            for other in reversed(incoming[node]):
                if other not in assigned:
                    assigned.add(other)
                    stack.append(other)
        members.sort()
        if len(members) > 1 or seed in outgoing[seed]:
            components.append(members)
    return sorted(components, key=lambda members: tuple(members))


def _cycle_findings(index: GraphIndex) -> list[Finding]:
    findings = []
    for members in _components(index):
        component = set(members)
        witness_nodes, witness_edges, _ = index.shortest_path(
            members[0], {members[0]}, minimum_edges=1, allowed_nodes=component,
        )
        internal_edges = sorted(
            edge.id for source in members for edge in index.outgoing[source]
            if edge.target in component
        )
        recursive = len(members) == 1
        findings.append(_finding(
            index,
            kind="recursive_call" if recursive else "call_cycle",
            severity="info", status="open",
            title="静态自递归调用" if recursive else f"静态调用环（{len(members)} 个节点）",
            description=(
                "确定调用关系中存在自递归。它可能是正常实现；不能据此判断递归不终止。"
                if recursive else
                "确定调用关系形成强连通分量。它可能是正常协作结构；不能据此判断运行时循环或不终止。"
            ),
            identity={"members": members}, node_ids=members, edge_ids=witness_edges,
            details={
                "fact": "strongly_connected_component", "component_node_ids": members,
                "component_edge_ids": internal_edges,
                "witness_node_ids": witness_nodes, "witness_edge_ids": witness_edges,
                "termination": "not_determined", "policy_violation": False,
            },
        ))
    return findings


def _matching_nodes(index: GraphIndex, pattern: str) -> list[str]:
    return sorted(
        node.id for node in index.nodes.values()
        if fnmatchcase(node.id, pattern) or fnmatchcase(node.qualname, pattern)
    )


def _rule_findings(index: GraphIndex) -> list[Finding]:
    findings = []
    allowed_kinds = {"required_call", "required_path", "forbidden_call", "forbidden_path"}
    rules = index.snapshot.config.get("rules", [])
    for position, rule in enumerate(rules):
        rule_id = str(rule.get("id", f"rule-{position + 1}"))
        kind = rule.get("kind", "")
        from_pattern, to_pattern = rule.get("from", ""), rule.get("to", "")
        severity = rule.get("severity", "high")
        semantic_rule = {
            "id": rule_id, "kind": kind, "from": from_pattern, "to": to_pattern,
        }
        if not isinstance(kind, str) or kind not in allowed_kinds or not isinstance(from_pattern, str) or not from_pattern or (
            not isinstance(to_pattern, str) or not to_pattern
        ):
            findings.append(_finding(
                index, kind="rule_configuration", severity="low", status="uncertain",
                title=f"规则 {rule_id} 无法分析",
                description="规则类型或端点模式无效；未将该规则视为检查通过。",
                identity=semantic_rule, rule_id=rule_id, details={"rule": rule},
            ))
            continue
        sources = _matching_nodes(index, from_pattern)
        targets = _matching_nodes(index, to_pattern)
        target_set = set(targets)
        details: dict[str, Any] = {
            "rule": dict(rule), "matched_source_ids": sources,
            "matched_target_ids": targets,
            "quantifier": "each_source_to_at_least_one_target",
            "minimum_call_edges": 1,
            "call_path_interpretation": "静态结构可达，不代表必然执行或行为正确。",
            "world_assumption": "explicit_static_calls_only",
        }
        if not sources or not targets:
            # A missing target may be hidden behind an unresolved call from an
            # otherwise known source. Missing sources require project scope.
            scope = index.reachable(set(sources)) if sources else set(index.nodes)
            gaps = index.gaps_for(scope, include_callbacks=kind.endswith("_path"))
            missing = []
            if not sources:
                missing.append("source")
            if not targets:
                missing.append("target")
            required = kind.startswith("required_")
            uncertain = bool(gaps) or not required
            findings.append(_finding(
                index, kind=kind if required else "rule_scope_missing",
                severity=severity if required else "low",
                status="uncertain" if uncertain else "open",
                title=f"规则 {rule_id} 的端点未匹配",
                description=(
                    "规则的源或目标未在快照中匹配；解析缺口可能隐藏端点，不能确认实现遗漏。"
                    if gaps else
                    "必需规则的源或目标未在已分析范围内匹配；这是相对配置的结构缺口。"
                    if required else
                    "禁止规则的源或目标未匹配，无法确认规则适用于预期范围；未报告禁止关系存在。"
                ),
                identity={"rule": semantic_rule, "scope": "missing_endpoints"},
                node_ids=sorted(set(sources + targets)), rule_id=rule_id,
                details={
                    **details, "missing_endpoints": missing, "gaps": gaps,
                    "gap_scope": {"kind": "source_closure" if sources else "project", "source_ids": sources},
                },
            ))
            continue
        direct = kind.endswith("_call")
        required = kind.startswith("required_")
        for source in sources:
            if direct:
                matches = [
                    edge for edge in index.outgoing[source] if edge.target in target_set
                ]
                path_nodes = [source, matches[0].target] if matches else []
                path_edges = [matches[0].id] if matches else []
                affected = {source}
            else:
                path_nodes, path_edges, _ = index.shortest_path(
                    source, target_set, minimum_edges=1,
                )
                affected = index.reachable({source})
            found = bool(path_edges)
            if required and found:
                continue
            gaps = index.gaps_for(affected, include_callbacks=not direct)
            gaps.extend(index.definition_gaps_for(target_set - affected))
            if not required and not found and not gaps:
                continue
            if required:
                status = "uncertain" if gaps else "open"
                title = f"{source} 的必需{'调用' if direct else '路径'}未确认"
                description = (
                    "未找到满足规则的确定连接，相关分析缺口可能隐藏连接，不能确认遗漏。"
                    if gaps else
                    "已分析的确定调用关系未满足显式规则；每个源必须连接至少一个匹配目标。"
                )
            else:
                status = "open" if found else "uncertain"
                title = (
                    f"{source} 存在禁止{'调用' if direct else '路径'}" if found
                    else f"{source} 的禁止关系无法完整排除"
                )
                description = (
                    "找到一条违反显式规则的确定静态连接；不表示该路径必然运行。"
                    if found else
                    "未找到禁止的确定连接，但相关解析缺口使检查不完整。"
                )
            observed_nodes = path_nodes if found else [source] + targets
            findings.append(_finding(
                index, kind=kind, severity=severity, status=status,
                title=title, description=description,
                identity={"rule": semantic_rule, "source": source},
                node_ids=observed_nodes, edge_ids=path_edges, rule_id=rule_id,
                details={
                    **details, "source_id": source, "witness_node_ids": path_nodes,
                    "witness_edge_ids": path_edges, "gaps": gaps,
                    "search_complete": not gaps,
                    "proven_violation": found if not required else not gaps,
                    "gap_scope": {
                        "kind": "direct_source" if direct else "source_closure",
                        "source_ids": [source],
                    },
                },
            ))
    return findings


def _entrypoint_findings(index: GraphIndex) -> list[Finding]:
    patterns = index.snapshot.config.get("entrypoints", [])
    if not patterns:
        return []
    roots: set[str] = set()
    findings = []
    for pattern in patterns:
        matches = _matching_nodes(index, pattern)
        roots.update(matches)
        if not matches:
            findings.append(_finding(
                index, kind="entrypoint_missing", severity="low", status="uncertain",
                title=f"入口模式 {pattern} 未匹配",
                description="配置入口未在分析节点中匹配，不能使用它推断其他节点不可达。",
                identity={"pattern": pattern},
                details={
                    "entrypoint_pattern": pattern,
                    "gaps": index.gaps_for(set(index.nodes), include_callbacks=True),
                    "gap_scope": {"kind": "project"},
                },
            ))
    # Missing configured entrypoints can hide entire reachable regions.
    if any(finding.type == "entrypoint_missing" for finding in findings):
        return findings
    reachable = index.reachable(roots)
    gaps = index.gaps_for(reachable, include_callbacks=True)
    gap_evidence = _gap_evidence_summary(gaps)
    callable_kinds = {"function", "async_function", "method", "class"}
    for node_id in sorted(index.nodes.keys() - reachable):
        node = index.nodes[node_id]
        if node.kind not in callable_kinds:
            continue
        findings.append(_finding(
            index, kind="suspected_unreachable", severity="low", status="uncertain",
            title=f"配置入口未确定可达 {node_id}",
            description=(
                "在配置入口的确定调用闭包中未发现该节点。动态调用、外部入口或框架行为可能使用它；不能据此判定死代码。"
            ),
            identity={"node": node_id, "entrypoints": sorted(patterns)},
            node_ids=[node_id],
            details={
                "entrypoint_patterns": sorted(patterns), "entrypoint_ids": sorted(roots),
                "reachable_nodes": len(reachable), **gap_evidence,
                "gap_scope": {"kind": "entrypoint_closure", "entrypoint_ids": sorted(roots)},
                "dead_code": "not_determined",
            },
        ))
    return findings


def _resolution_findings(index: GraphIndex) -> list[Finding]:
    """Expose unresolved calls as analysis limitations, not definite defects."""
    findings = []
    # Semantic ordinal makes fingerprints independent of line numbers while
    # distinguishing repeated identical expressions inside the same caller.
    occurrences: dict[tuple[str, str], int] = {}
    unknown = sorted(
        (edge for edges in index.unknown.values() for edge in edges),
        key=lambda edge: (edge.source, edge.expression, edge.file, edge.line, edge.column, edge.id),
    )
    for edge in unknown:
        semantic = (edge.source, edge.expression)
        ordinal = occurrences.get(semantic, 0)
        occurrences[semantic] = ordinal + 1
        candidates = [candidate for candidate in edge.candidates if candidate in index.nodes]
        finding = _finding(
            index, kind="unresolved_call", severity="info", status="uncertain",
            title=f"调用目标未确定：{edge.expression}",
            description="该调用缺少唯一的静态目标；这是一项分析缺口，不等同于目标不存在或功能缺失。",
            identity={
                "source": edge.source, "expression": edge.expression,
                "ordinal": ordinal,
            },
            node_ids=[edge.source] + candidates, edge_ids=[edge.id],
            details={"call_site": index.call_gap(edge), "candidates_are_confirmed": False},
        )
        finding.metadata["resolution"] = edge.resolution
        findings.append(finding)
    return findings


def _callback_findings(index: GraphIndex) -> list[Finding]:
    findings = []
    occurrences: dict[tuple[str, str], int] = {}
    boundaries = sorted(
        (edge for edges in index.callback_boundaries.values() for edge in edges),
        key=lambda edge: (edge.source, edge.expression, edge.file, edge.line, edge.column, edge.id),
    )
    for edge in boundaries:
        semantic = (edge.source, edge.expression)
        ordinal = occurrences.get(semantic, 0)
        occurrences[semantic] = ordinal + 1
        findings.append(_finding(
            index, kind="external_callback_boundary", severity="info", status="uncertain",
            title=f"外部回调路径未确认：{edge.expression}",
            description="外部符号已识别，但其回调或隐式执行不能由当前源码范围确定；未把候选回调当成确定调用。",
            identity={"source": edge.source, "expression": edge.expression, "ordinal": ordinal},
            node_ids=[edge.source], edge_ids=[edge.id],
            details={"call_site": _external_callback_gap(edge)},
        ))
    return findings


def detect(snapshot: GraphSnapshot) -> list[Finding]:
    """Deterministic findings tied to one immutable analysis snapshot.

All required glob rules quantify each source to at least one target. Rules use
positive-length paths. The analysis has no fixed propagation depth; incomplete
sources and reachable unknown calls produce uncertainty rather than false proof.
"""
    if getattr(snapshot, "detector_version", DETECTOR_VERSION) != DETECTOR_VERSION:
        raise ValueError("检测器版本与快照身份不一致；需创建新快照，不能覆盖原历史结果。")
    index = GraphIndex(snapshot)
    findings = (
        _cycle_findings(index) + _rule_findings(index)
        + _entrypoint_findings(index) + _resolution_findings(index)
        + _callback_findings(index)
    )
    contracts = snapshot.config.get("static_contracts", [])
    if contracts:
        from .static_contracts import analyze_contracts
        findings.extend(analyze_contracts(snapshot, contracts))
    value_contracts = snapshot.config.get("value_contracts", [])
    if value_contracts:
        from .value_analysis import analyze_value_contracts
        findings.extend(analyze_value_contracts(snapshot, value_contracts))
    navigation_contracts = snapshot.config.get("navigation_contracts", [])
    if navigation_contracts:
        from .navigation_analysis import analyze_navigation_contracts
        findings.extend(analyze_navigation_contracts(snapshot, navigation_contracts))
    atomicity_contracts = snapshot.config.get("atomicity_contracts", [])
    if atomicity_contracts:
        from .atomicity_analysis import analyze_atomicity_contracts
        findings.extend(analyze_atomicity_contracts(snapshot, atomicity_contracts))
    field_contracts = snapshot.config.get("field_contracts", [])
    if field_contracts:
        from .field_analysis import analyze_field_contracts
        findings.extend(analyze_field_contracts(snapshot, field_contracts))
    budget_contracts = snapshot.config.get("budget_contracts", [])
    if budget_contracts:
        from .budget_analysis import analyze_budget_contracts
        findings.extend(analyze_budget_contracts(snapshot, budget_contracts))
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    return sorted(
        findings,
        key=lambda item: (severity_order.get(item.severity, 5), item.type, item.fingerprint),
    )
