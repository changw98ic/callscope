"""Deterministic queries over the *known* static call graph.

No target code is imported, built, or executed. A resolved path is a structural
witness, not a statement that a path executes or that its behavior is correct.
Unknown calls stay unknown; they are never promoted to definite graph edges.
"""

from collections import deque
from dataclasses import asdict
from typing import Any

from .axon_adapter import AxonCallGraph
from .models import DETECTOR_VERSION, Edge, Finding, GraphSnapshot, Node


UNKNOWN_RESOLUTIONS = frozenset({"unresolved", "dynamic", "ambiguous"})
_COMPLETE_FILE_STATUSES = frozenset({"parsed", "complete", "ok", "analyzed"})
QUERY_GAP_SAMPLE_LIMIT = 20


def _query_gap_summary(
    snapshot: GraphSnapshot, gaps: list[dict[str, Any]],
) -> dict[str, Any]:
    """Bound response evidence without changing the full analysis decision."""
    sample = gaps[:QUERY_GAP_SAMPLE_LIMIT]
    return {
        "gaps": sample,
        "gap_count": len(gaps),
        "gaps_truncated": len(gaps) > len(sample),
        "gap_sample_limit": QUERY_GAP_SAMPLE_LIMIT,
        "gap_snapshot_id": snapshot.id,
        "full_gap_evidence": "snapshot_edges_diagnostics_and_source_statuses",
    }


def _model_scope() -> dict[str, Any]:
    return {
        "kind": "explicit_static_call_model",
        "external_calls": "terminals_unless_callback_boundary_is_identified",
        "unmodeled": ["implicit_magic_calls", "runtime_registration", "external_implementations"],
        "meaning": "完整性仅针对显式静态调用模型，不代表已排除所有运行时可能调用。",
    }


def _coverage_gaps(snapshot: GraphSnapshot) -> list[dict[str, Any]]:
    """Scanning/parsing gaps, separate from per-call resolution gaps.

An unknown call elsewhere in the project must not make a fully analyzed direct
call constraint uncertain. A failed or omitted source file, however, can hide
symbols and registration relationships, so is treated conservatively.
"""
    gaps: list[dict[str, Any]] = []
    for source in sorted(snapshot.files, key=lambda item: item.path):
        if source.status not in _COMPLETE_FILE_STATUSES:
            gaps.append({
                "kind": "source_coverage",
                "file": source.path,
                "status": source.status,
                "reason": source.error or "该文件未完成静态解析。",
            })
    for diagnostic in snapshot.diagnostics:
        if diagnostic.level.lower() in {"error", "fatal"}:
            gaps.append({
                "kind": "diagnostic",
                "code": diagnostic.code,
                "file": diagnostic.file,
                "line": diagnostic.line,
                "reason": diagnostic.message,
            })
    if snapshot.status in {"failed", "pending", "building", "incomplete"}:
        gaps.append({
            "kind": "snapshot_coverage",
            "status": snapshot.status,
            "reason": "该快照未完成静态分析。",
        })
    # An analyzer may report a scan failure that did not create a SourceFile.
    # Do not use stats.incomplete: that also includes unrelated dynamic calls.
    for key in ("scan_incomplete", "coverage_incomplete"):
        if snapshot.stats.get(key):
            gaps.append({
                "kind": "snapshot_coverage",
                "reason": f"分析器标记 {key}，源码扫描范围不完整。",
            })
    # De-duplicate identical analyzer diagnostics without dropping provenance.
    unique: dict[tuple[Any, ...], dict[str, Any]] = {}
    for gap in gaps:
        identity = (
            gap.get("kind"), gap.get("file"), gap.get("line"),
            gap.get("code"), gap.get("status"), gap.get("reason"),
        )
        unique[identity] = gap
    return list(unique.values())


def _edge_gap(edge: Edge) -> dict[str, Any]:
    return {
        "kind": "call_resolution",
        "edge_id": edge.id,
        "source": edge.source,
        "target": edge.target,
        "expression": edge.expression,
        "file": edge.file,
        "line": edge.line,
        "column": edge.column,
        "resolution": edge.resolution,
        "candidates": list(edge.candidates),
        "reason": edge.reason or "调用目标无法静态确定。",
    }


def _external_callback_gap(edge: Edge) -> dict[str, Any]:
    return {
        **_edge_gap(edge),
        "kind": "external_callback_boundary",
        "reason": "外部调用可能通过回调或隐式分派重入本地代码；相关路径不能从外部实现静态确认。",
        "callback_candidates": edge.metadata.get("callback_candidates", []),
        "callable_arguments": edge.metadata.get("callable_arguments", []),
    }


class GraphIndex:
    """A shared immutable index used by queries and detectors.

Only resolved edges with both endpoints in this snapshot enter adjacency.
Recognized external calls are terminals. Calls that may re-enter project code
through external callbacks are outside this first-version graph model.
"""

    def __init__(self, snapshot: GraphSnapshot) -> None:
        self.snapshot = snapshot
        self.nodes: dict[str, Node] = {node.id: node for node in snapshot.nodes}
        self.edges: dict[str, Edge] = {edge.id: edge for edge in snapshot.edges}
        self._call_graph = AxonCallGraph(self.nodes)
        self.unknown: dict[str, list[Edge]] = {node: [] for node in self.nodes}
        self.callback_boundaries: dict[str, list[Edge]] = {node: [] for node in self.nodes}
        self.ambiguous_definitions = {
            node.id for node in snapshot.nodes if node.metadata.get("duplicate_definition")
        }
        self.coverage_gaps = _coverage_gaps(snapshot)
        self.integrity_gaps: list[dict[str, Any]] = []
        for edge in sorted(snapshot.edges, key=lambda item: item.id):
            if edge.source not in self.nodes:
                self.integrity_gaps.append({
                    "kind": "graph_integrity", "edge_id": edge.id,
                    "reason": "调用边的源节点不在此快照中。",
                })
                continue
            if edge.source in self.ambiguous_definitions or (
                edge.resolution == "resolved" and edge.target in self.ambiguous_definitions
            ):
                # Multiple declarations share a logical symbol ID. Combining
                # their outgoing calls would invent one implementation that
                # might not exist; the immutable raw edge is retained as gap.
                self.unknown[edge.source].append(edge)
            elif edge.resolution == "resolved" and edge.target in self.nodes:
                self._call_graph.add_call(edge)
            elif edge.resolution == "external":
                if any(edge.metadata.get(key) for key in (
                    "callback_candidates", "callable_arguments", "callbacks_unknown",
                    "callback_arguments", "may_callback",
                )):
                    self.callback_boundaries[edge.source].append(edge)
            elif edge.resolution != "external":
                # This also makes a dangling 'resolved' edge visibly incomplete.
                self.unknown[edge.source].append(edge)
                if edge.resolution == "resolved":
                    self.integrity_gaps.append({
                        "kind": "graph_integrity", "edge_id": edge.id,
                        "file": edge.file, "line": edge.line,
                        "reason": "标记为已解析的调用边缺少本快照目标节点。",
                    })
        # Queries and detectors consume these lists, which now come from the
        # upstream graph's indexes rather than a parallel adjacency builder.
        self.outgoing: dict[str, list[Edge]]
        self.incoming: dict[str, list[Edge]]
        self.outgoing, self.incoming = self._call_graph.adjacency()

    def resolve_endpoint(self, value: str) -> tuple[str | None, dict[str, Any]]:
        if value in self.nodes:
            if value in self.ambiguous_definitions:
                return None, {"status": "ambiguous_definition", "node_ids": [value]}
            return value, {"status": "matched", "node_ids": [value]}
        matches = sorted(
            node.id for node in self.nodes.values() if node.qualname == value
        )
        if len(matches) == 1:
            if matches[0] in self.ambiguous_definitions:
                return None, {"status": "ambiguous_definition", "node_ids": matches}
            return matches[0], {"status": "matched", "node_ids": matches}
        return None, {
            "status": "ambiguous" if matches else "missing",
            "node_ids": matches,
        }

    def reachable(self, seeds: set[str]) -> set[str]:
        seen = set(seeds) & self.nodes.keys()
        queue = deque(sorted(seen))
        while queue:
            node = queue.popleft()
            for edge in self.outgoing[node]:
                target = edge.target
                if target is not None and target not in seen:
                    seen.add(target)
                    queue.append(target)
        return seen

    def definition_gaps_for(self, node_ids: set[str]) -> list[dict[str, Any]]:
        gaps = []
        for node_id in sorted(node_ids & self.ambiguous_definitions):
            node = self.nodes[node_id]
            gaps.append({
                "kind": "symbol_identity", "node_id": node_id,
                "file": node.file, "line": node.line,
                "definitions": node.metadata.get("definitions", []),
                "reason": "符号包含多个声明，无法把其调用关系合并为一个确定实现。",
            })
        return gaps

    def call_gap(self, edge: Edge) -> dict[str, Any]:
        gap = _edge_gap(edge)
        if edge.source in self.ambiguous_definitions:
            gap.update({
                "effective_resolution": "ambiguous_source",
                "reason": "调用源符号包含多个声明；该调用不能证明某个唯一实现中的连接。",
            })
        elif edge.resolution == "resolved" and edge.target in self.ambiguous_definitions:
            gap.update({
                "effective_resolution": "ambiguous_target",
                "reason": "调用目标包含多个声明，不能确认唯一目标实现。",
            })
        return gap

    def gaps_for(
        self, node_ids: set[str], *, include_callbacks: bool = False,
    ) -> list[dict[str, Any]]:
        gaps = list(self.coverage_gaps) + list(self.integrity_gaps)
        gaps.extend(self.definition_gaps_for(node_ids))
        for node_id in sorted(node_ids):
            gaps.extend(self.call_gap(edge) for edge in self.unknown.get(node_id, []))
            if include_callbacks:
                gaps.extend(
                    _external_callback_gap(edge)
                    for edge in self.callback_boundaries.get(node_id, [])
                )
        return gaps

    def shortest_path(
        self,
        source: str,
        targets: set[str],
        *,
        minimum_edges: int = 0,
        allowed_nodes: set[str] | None = None,
    ) -> tuple[list[str], list[str], set[str]]:
        """One shortest confirmed path, without a hop-depth correctness limit.

minimum_edges=1 is used for policy rules: a node matching both endpoint
patterns does not satisfy a required *call* path merely by existing.
"""
        if source not in self.nodes:
            return [], [], set()
        if source in targets and minimum_edges == 0:
            return [source], [], {source}
        parent: dict[str, tuple[str, str] | None] = {source: None}
        queue = deque([source])
        while queue:
            node = queue.popleft()
            for edge in self.outgoing[node]:
                target = edge.target
                if target is None or (
                    allowed_nodes is not None and target not in allowed_nodes
                ):
                    continue
                if target in targets:
                    # Check the target before `seen` so positive self/cycle
                    # paths are found without revisiting nodes indefinitely.
                    nodes, edges = [node], []
                    cursor = node
                    while parent[cursor] is not None:
                        previous, edge_id = parent[cursor]
                        nodes.append(previous)
                        edges.append(edge_id)
                        cursor = previous
                    nodes.reverse()
                    edges.reverse()
                    nodes.append(target)
                    edges.append(edge.id)
                    return nodes, edges, set(parent) | {target}
                if target not in parent:
                    parent[target] = (node, edge.id)
                    queue.append(target)
        return [], [], set(parent)


def find_path(snapshot: GraphSnapshot, source: str, target: str) -> dict[str, Any]:
    """Query one shortest path in the resolved internal-call graph.

`not_found` is an exhaustive result in the supported static model. `unknown`
means a missing endpoint or path may be affected by analysis gaps. `found`
always carries a definite static witness, even when other paths remain unknown.
"""
    index = GraphIndex(snapshot)
    source_id, source_status = index.resolve_endpoint(source)
    target_id, target_status = index.resolve_endpoint(target)
    result: dict[str, Any] = {
        "snapshot_id": snapshot.id,
        "from": source,
        "to": target,
        "status": "not_found",
        "complete": False,
        "completeness_scope": "explicit_static_call_model",
        "model": _model_scope(),
        "node_ids": [],
        "edge_ids": [],
        "nodes": [],
        "edges": [],
        **_query_gap_summary(snapshot, []),
        "reason": "",
        "endpoint_status": {"from": source_status, "to": target_status},
        "interpretation": (
            "静态调用路径存在只说明结构可达，不保证运行或功能正确。"
            "普通外部调用作为图终端；已识别的外部回调边界作为解析缺口。"
        ),
        "search": {
            "scope": "resolved_internal_calls", "exhaustive": False,
            "visited_nodes": 0, "shortest_in_resolved_graph": False,
            "depth_limit": None,
        },
    }
    if source_id is None or target_id is None:
        scope = index.reachable({source_id}) if source_id else set(index.nodes)
        gaps = index.gaps_for(scope, include_callbacks=True)
        ambiguous = any(
            item["status"] in {"ambiguous", "ambiguous_definition"}
            for item in (source_status, target_status)
        )
        result.update({
            "status": "unknown" if gaps or ambiguous else "not_found",
            "complete": not gaps and not ambiguous,
            **_query_gap_summary(snapshot, gaps),
            "reason": "端点匹配存在歧义。" if ambiguous else "源或目标不在已分析节点中。",
        })
        return result
    nodes, edges, visited = index.shortest_path(source_id, {target_id})
    # Assess uncertainty in the full source closure, not an arbitrary 3-hop
    # neighborhood and not only nodes visited before an early BFS success.
    closure = index.reachable({source_id})
    gaps = index.gaps_for(closure, include_callbacks=True)
    found = bool(nodes)
    result.update({
        "status": "found" if found else ("unknown" if gaps else "not_found"),
        "complete": not gaps,
        "node_ids": nodes,
        "edge_ids": edges,
        "nodes": [asdict(index.nodes[node_id]) for node_id in nodes],
        "edges": [asdict(index.edges[edge_id]) for edge_id in edges],
        **_query_gap_summary(snapshot, gaps),
        "reason": (
            "源与目标是同一节点；零长度路径不证明递归调用。" if found and not edges
            else "找到一条最短的确定静态调用路径。" if found
            else "未找到确定路径；相关解析缺口可能隐藏连接。" if gaps
            else "在已完成的确定静态调用图中未找到路径。"
        ),
        "search": {
            "scope": "resolved_internal_calls", "exhaustive": not found,
            "visited_nodes": len(visited), "closure_nodes": len(closure),
            "shortest_in_resolved_graph": found, "depth_limit": None,
        },
    })
    return result


def subgraph(
    snapshot: GraphSnapshot,
    node_id: str,
    depth: int = 2,
    direction: str = "both",
) -> dict[str, Any]:
    """A depth-limited *display* neighborhood, never a detector's scope.

Unknown edges originating in displayed nodes are retained as unknown evidence;
their candidates are not used as confirmed neighbors.
"""
    if isinstance(depth, bool) or not isinstance(depth, int) or depth < 0:
        raise ValueError("depth 必须为非负整数。")
    if direction not in {"both", "in", "out", "incoming", "outgoing"}:
        raise ValueError("direction 必须为 both、in 或 out。")
    direction = {"incoming": "in", "outgoing": "out"}.get(direction, direction)
    index = GraphIndex(snapshot)
    root_id, endpoint_status = index.resolve_endpoint(node_id)
    if root_id is None:
        gaps = index.gaps_for(set(endpoint_status["node_ids"]), include_callbacks=True)
        ambiguous = endpoint_status["status"] in {"ambiguous", "ambiguous_definition"}
        return {
            "snapshot_id": snapshot.id, "node_id": node_id,
            "status": "unknown" if ambiguous or gaps else "not_found",
            "nodes": [], "edges": [], **_query_gap_summary(snapshot, gaps),
            "depth": depth, "direction": direction, "complete": not ambiguous and not gaps,
            "completeness_scope": "explicit_static_call_model", "model": _model_scope(),
            "truncated": False, "endpoint_status": endpoint_status,
        }
    distance = {root_id: 0}
    queue = deque([root_id])
    while queue:
        current = queue.popleft()
        if distance[current] == depth:
            continue
        next_nodes: set[str] = set()
        if direction in {"both", "out"}:
            next_nodes.update(edge.target for edge in index.outgoing[current] if edge.target)
        if direction in {"both", "in"}:
            next_nodes.update(edge.source for edge in index.incoming[current])
        for other in sorted(next_nodes):
            if other not in distance:
                distance[other] = distance[current] + 1
                queue.append(other)
    selected = set(distance)
    edges = [
        edge for edge in snapshot.edges
        if edge.source in selected and (
            edge.target in selected or edge.resolution != "resolved"
            or edge.target not in index.nodes
        )
    ]
    truncated = False
    for current in selected:
        if direction in {"both", "out"} and any(
            edge.target not in selected for edge in index.outgoing[current]
        ):
            truncated = True
        if direction in {"both", "in"} and any(
            edge.source not in selected for edge in index.incoming[current]
        ):
            truncated = True
    gaps = index.gaps_for(selected, include_callbacks=True)
    return {
        "snapshot_id": snapshot.id, "node_id": root_id, "status": "found",
        "nodes": [asdict(index.nodes[item]) for item in sorted(selected)],
        "edges": [asdict(item) for item in sorted(edges, key=lambda edge: edge.id)],
        **_query_gap_summary(snapshot, gaps), "depth": depth, "direction": direction,
        "complete": not gaps and not truncated, "truncated": truncated,
        "completeness_scope": "explicit_static_call_model", "model": _model_scope(),
        "endpoint_status": endpoint_status,
        "interpretation": "深度限制仅控制展示范围；未知候选不作为确定调用边。",
    }


def _field_changes(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    return {
        key: {"before": before.get(key), "after": after.get(key)}
        for key in sorted(before.keys() | after.keys())
        if before.get(key) != after.get(key)
    }


def _entity_diff(old_items: list[Any], new_items: list[Any]) -> dict[str, Any]:
    before = {item.id: asdict(item) for item in old_items}
    after = {item.id: asdict(item) for item in new_items}
    changed = []
    for identity in sorted(before.keys() & after.keys()):
        changes = _field_changes(before[identity], after[identity])
        if changes:
            changed.append({
                "id": identity, "before": before[identity],
                "after": after[identity], "changes": changes,
            })
    return {
        "added": [after[item] for item in sorted(after.keys() - before.keys())],
        "removed": [before[item] for item in sorted(before.keys() - after.keys())],
        "changed": changed,
    }


def _finding_view(finding: Finding) -> dict[str, Any]:
    """Exclude per-snapshot evidence IDs when deciding semantic persistence."""
    data = asdict(finding)
    data.pop("id", None)
    data.pop("snapshot_id", None)
    data.pop("evidence", None)
    return data


def diff_snapshots(
    old: GraphSnapshot,
    new: GraphSnapshot,
    old_findings: list[Finding] | None = None,
    new_findings: list[Finding] | None = None,
) -> dict[str, Any]:
    """Structural and finding differences, with explicit comparability limits.

`resolved` means absent from the new detector output; it does not prove a fix.
Source changes, rule changes, analyzer changes and incomplete scans remain
separate explanations. Human decisions never alter these raw observations.
"""
    old_detector = getattr(old, "detector_version", "unknown")
    new_detector = getattr(new, "detector_version", "unknown")
    unavailable = []
    if old_findings is None or new_findings is None:
        # Local implementation code only; this does not import target modules.
        from .detectors import detect

        if old_findings is None:
            if old_detector == DETECTOR_VERSION:
                old_findings = detect(old)
            else:
                unavailable.append("旧快照未提供原始发现，且检测器版本不同；禁止使用当前逻辑冒充历史结果。")
        if new_findings is None:
            if new_detector == DETECTOR_VERSION:
                new_findings = detect(new)
            else:
                unavailable.append("新快照未提供原始发现，且检测器版本不同；禁止沿用原快照身份重新检测。")
    for snapshot, observations in ((old, old_findings), (new, new_findings)):
        if observations is not None and any(
            item.snapshot_id and item.snapshot_id != snapshot.id for item in observations
        ):
            raise ValueError("发现结果必须属于对应的快照。")
    nodes = _entity_diff(old.nodes, new.nodes)
    edges = _entity_diff(old.edges, new.edges)
    # Without both original result sets, absence must not become 'resolved'.
    previous = {} if unavailable else {item.fingerprint or item.id: item for item in old_findings or []}
    current = {} if unavailable else {item.fingerprint or item.id: item for item in new_findings or []}
    persisting = []
    for identity in sorted(previous.keys() & current.keys()):
        changes = _field_changes(_finding_view(previous[identity]), _finding_view(current[identity]))
        persisting.append({
            "fingerprint": identity, "before": asdict(previous[identity]),
            "after": asdict(current[identity]), "changed": bool(changes),
            "changes": changes,
        })
    findings = {
        "added": [asdict(current[item]) for item in sorted(current.keys() - previous.keys())],
        "resolved": [asdict(previous[item]) for item in sorted(previous.keys() - current.keys())],
        "persisting": persisting,
        "available": not unavailable,
        "unavailable_reasons": unavailable,
    }
    same_project = old.project_id == new.project_id
    same_policy = old.policy_hash == new.policy_hash
    same_analyzer = old.analyzer_version == new.analyzer_version
    old_parser = getattr(old, "parser_version", "unknown")
    new_parser = getattr(new, "parser_version", "unknown")
    same_parser = old_parser == new_parser
    same_detector = old_detector == new_detector
    old_schema = getattr(old, "schema_version", "unknown")
    new_schema = getattr(new, "schema_version", "unknown")
    same_schema = old_schema == new_schema
    known_versions = all(
        value not in {"", "unknown", "legacy-unknown", None}
        for value in (
            old.analyzer_version, new.analyzer_version, old_parser, new_parser,
            old_detector, new_detector, old_schema, new_schema,
        )
    )
    same_analysis_config = old.config.get("analysis", {}) == new.config.get("analysis", {})
    old_index, new_index = GraphIndex(old), GraphIndex(new)
    coverage_complete = not (
        old_index.coverage_gaps or new_index.coverage_gaps
        or old_index.integrity_gaps or new_index.integrity_gaps
        or old_index.ambiguous_definitions or new_index.ambiguous_definitions
    )
    reasons = []
    if not same_project:
        reasons.append("项目身份不同；变化不能直接解释为同一项目的演化。")
    if not same_policy:
        reasons.append("分析配置或规则发生变化；发现增减不能直接解释为代码修复。")
    if not same_analyzer:
        reasons.append("分析器版本不同；调用解析能力可能影响图差异。")
    if not same_parser:
        reasons.append("宿主解析器版本不同；语法与 AST 解析结果可能影响图差异。")
    if not same_detector:
        reasons.append("检测器版本不同；发现结果可能来自检测逻辑变化。")
    if not same_schema:
        reasons.append("图模式版本不同；实体与调用边定义可能影响差异。")
    if not same_analysis_config:
        reasons.append("源码根、语言、排除范围或扫描配置变化；图增减可能来自分析范围变化。")
    if not known_versions:
        reasons.append("至少一个快照的解析/分析/检测/模式版本未知，不能建立完整的可比性保证。")
    if not coverage_complete:
        reasons.append("至少一个快照存在源码覆盖缺口；删除项可能只是未能分析。")
    reasons.extend(unavailable)
    uncertain = sum(item.status == "uncertain" for item in new_findings or [])
    return {
        "from_snapshot": old.id, "to_snapshot": new.id,
        "nodes": nodes, "edges": edges, "findings": findings,
        "comparison": {
            "same_project": same_project, "same_policy": same_policy,
            "same_analyzer": same_analyzer, "same_detector": same_detector,
            "same_parser_version": same_parser,
            "same_detector_version": same_detector, "same_schema_version": same_schema,
            "same_analysis_config": same_analysis_config,
            "versions_known": known_versions,
            "same_source": old.source_hash == new.source_hash,
            "coverage_complete": coverage_complete,
            "structurally_comparable": same_project and same_analyzer and same_parser and same_schema
            and same_analysis_config and coverage_complete and known_versions,
            "findings_comparable": same_project and same_policy and same_analyzer and same_parser
            and same_detector and same_schema and same_analysis_config
            and coverage_complete and known_versions and not unavailable,
            "versions": {
                "from": {"analyzer": old.analyzer_version, "parser": old_parser, "detector": old_detector,
                         "schema": old_schema, "policy_hash": old.policy_hash},
                "to": {"analyzer": new.analyzer_version, "parser": new_parser, "detector": new_detector,
                       "schema": new_schema, "policy_hash": new.policy_hash},
            },
            "reasons": reasons,
            "resolved_meaning": "新快照未再报告该发现，不等于已证明修复。",
        },
        "summary": {
            "added_nodes": len(nodes["added"]), "removed_nodes": len(nodes["removed"]),
            "changed_nodes": len(nodes["changed"]), "added_edges": len(edges["added"]),
            "removed_edges": len(edges["removed"]), "changed_edges": len(edges["changed"]),
            "added_findings": len(findings["added"]),
            "resolved_findings": len(findings["resolved"]),
            "persisting_findings": len(findings["persisting"]),
            "uncertain_findings": uncertain,
            "message": "仅比较静态事实与发现；未执行目标代码，也不判断业务正确性。",
        },
    }
