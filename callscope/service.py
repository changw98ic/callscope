"""Application boundary: static analysis, immutable publication, and exploration."""

from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
import math
import threading
from typing import Any

from .analyzer import analyze_project
from .config import load_config, save_config
from .detectors import detect
from .graph import diff_snapshots, find_path, subgraph
from .models import GraphSnapshot, project_id_for
from .store import Store
from .cocoindex_runner import CocoIndexRunner, trusted_interpreter
from .analysis_inputs import tool_identity
from .language_catalog import SUPPORTED_LANGUAGES, language_capabilities

_LOADED_TOOL_IDENTITY = tool_identity()


class ScanBusyError(RuntimeError):
    pass


class AnalysisService:
    def __init__(self, root: str | Path, db_path: str | Path, config_path: str | Path | None = None,
                 *, analyzer=analyze_project, detector=detect, engine: str = "auto"):
        self.root = Path(root).resolve()
        if not self.root.is_dir():
            raise ValueError(f"项目目录不存在: {self.root}")
        self.project_id = project_id_for(self.root)
        self.config_path = Path(config_path).absolute() if config_path is not None else self.root / ".callscope.json"
        self._analyzer = analyzer
        self._detector = detector
        if engine not in {"auto", "full", "cocoindex"}:
            raise ValueError("engine 必须为 auto/full/cocoindex")
        if analyzer is not analyze_project and engine == "cocoindex":
            raise ValueError("CocoIndex 只运行固定注册的静态前端")
        use_coco = analyzer is analyze_project and (engine == "cocoindex" or (engine == "auto" and trusted_interpreter()))
        self._frontend_runner = CocoIndexRunner(str(Path(db_path).absolute()) + ".cocoindex") if use_coco else None
        self._engine = "cocoindex" if self._frontend_runner else "full"
        self.store = Store(db_path)
        self._scan_lock = threading.Lock()
        self._state_lock = threading.RLock()
        self._state: dict[str, Any] = {"state": "idle", "last_error": None, "last_started_at": None, "last_finished_at": None}
        self._stop = threading.Event()
        self._watch_thread: threading.Thread | None = None

    def config(self) -> dict[str, Any]:
        # A missing default file uses safe defaults; explicitly supplied missing files are errors.
        default = self.root / ".callscope.json"
        return load_config(self.root, None if self.config_path == default else self.config_path)

    def config_info(self) -> dict[str, Any]:
        return {"config": self.config(), "config_path": str(self.config_path)}

    def update_config(self, value: Any) -> dict[str, Any]:
        if not self._scan_lock.acquire(blocking=False):
            raise ScanBusyError("分析进行中，请稍后保存配置")
        try:
            config = save_config(self.config_path, value)
        finally:
            self._scan_lock.release()
        return {"config": config, "config_path": str(self.config_path), "requires_scan": True}

    def scan(self) -> dict[str, Any]:
        if not self._scan_lock.acquire(blocking=False):
            raise ScanBusyError("已有静态扫描正在进行")
        with self._state_lock:
            self._state.update(state="analyzing", last_error=None, last_started_at=_now())
        try:
            if tool_identity() != _LOADED_TOOL_IDENTITY:
                raise RuntimeError("工具代码已变化；请重启服务后扫描，旧快照保留")
            if self._frontend_runner:
                snapshot = self._analyzer(self.root, self.config(), frontend_runner=self._frontend_runner)
            else:
                snapshot = self._analyzer(self.root, self.config())
            findings = self._detector(snapshot)
            if tool_identity() != _LOADED_TOOL_IDENTITY:
                raise RuntimeError("分析期间工具代码发生变化；未发布快照，请重启服务")
            created = self.store.publish(snapshot, findings)
            maintenance = self._frontend_runner.last_run if self._frontend_runner else {"engine": "full", "global_detection": "full"}
            with self._state_lock:
                self._state.update(state="idle", last_finished_at=_now(), maintenance=maintenance)
            return {"snapshot_id": snapshot.id, "created": created, "status": snapshot.status,
                    "stats": snapshot.stats, "finding_count": len(findings), "maintenance": maintenance}
        except Exception as exc:
            with self._state_lock:
                self._state.update(state="failed", last_error=str(exc), last_finished_at=_now())
            raise
        finally:
            self._scan_lock.release()

    def status(self) -> dict[str, Any]:
        latest = self.store.latest(self.project_id)
        with self._state_lock:
            state = dict(self._state)
        try:
            config = self.config()
            count = (len(config.get("rules", [])) + len(config.get("static_contracts", []))
                     + len(config.get("value_contracts", [])) + len(config.get("navigation_contracts", []))
                     + len(config.get("atomicity_contracts", [])) + len(config.get("field_contracts", []))
                     + len(config.get("budget_contracts", [])) + len(config.get("goal_contracts", []))
                     + len(config.get("report_claims", [])))
            name = config.get("project", {}).get("name") or self.root.name
        except (ValueError, OSError) as exc:
            count = None
            name = self.root.name
            state["config_error"] = str(exc)
        return {
            "project": {"id": self.project_id, "name": name, "root": str(self.root)},
            "latest_snapshot": _metadata(latest) if latest else None,
            "analysis": state,
            "capabilities": {"mode": "static", "languages": list(SUPPORTED_LANGUAGES),
                             "language_catalog": language_capabilities(), "language_runtime_probed": False,
                             "execution": False,
                             "tests": False, "incremental_computation": self._frontend_runner is not None,
                             "incremental_granularity": "language" if self._frontend_runner else None,
                             "maintenance_engine": self._engine, "global_detection": "full",
                             "static_contracts": ["literal_set_consistency", "required_object_fields"],
                             "value_contracts": ["call_argument_value"],
                             "navigation_contracts": ["navigation_query_context"],
                             "port_wiring": ["boot", "factory_branch", "injection", "returned_method_use"],
                             "atomicity_contracts": ["protected_deduplication"],
                             "field_contracts": ["parameter_field_flow"],
                             "budget_contracts": ["bounded_for_loop", "counter_exhaustion_guard"],
                             "goal_contracts": ["status", "pipeline", "navigation", "device", "atomicity"],
                             "report_claims": "captured_source_chains",
                             "source_relations": ["rust_finite_state_selection", "conditional_gate_relations",
                                 "event_index_projection", "trusted_command_lineage", "unsupported_record_retention",
                                 "message_identity_relations", "browser_async_lifecycle", "resource_writer_ownership",
                                 "conditional_state_lineage", "conditional_publication_boundary"],
                             "document_comparisons": ["document_deployment_consistency"],
                             "architecture_explanations": "authenticated_captured_operations_and_handoffs",
                             "semantic_ir": "finite_immutable_field_state",
                             "semantic_environment": "captured_scope_conditional_model",
                             "completion_summaries": "finite_normal_completion_relations",
                             "interleaving_inference": False,
                             "finite_source_interleavings": "registered_two_request_one_scheduler_model",
                             "support_input_capture": True,
                             "graph_backend": "axon-graph-core-1"},
            "constraints_count": count,
            "watching": self._watch_thread is not None and self._watch_thread.is_alive(),
        }

    def snapshot(self, snapshot_id: str | None = None) -> GraphSnapshot:
        if snapshot_id is not None and (not isinstance(snapshot_id, str) or not snapshot_id.strip()):
            raise ValueError("snapshot_id 必须为非空字符串或省略")
        snapshot = self.store.get_snapshot(snapshot_id) if snapshot_id else self.store.latest(self.project_id)
        if snapshot is None:
            raise KeyError("快照不存在，请先进行静态扫描")
        # A server explores its configured project only. CLI diff is separately explicit.
        if snapshot.project_id != self.project_id:
            raise KeyError("快照不属于当前项目")
        return snapshot

    def graph(self, snapshot_id: str | None = None) -> dict[str, Any]:
        snapshot = self.snapshot(snapshot_id)
        return {"snapshot": _metadata(snapshot), "nodes": [asdict(n) for n in snapshot.nodes],
                "edges": [asdict(e) for e in snapshot.edges], "diagnostics": [asdict(d) for d in snapshot.diagnostics],
                "files": [{"path": source.path, "hash": source.hash, "language": source.language,
                           "status": source.status, "error": source.error} for source in snapshot.files],
                "stats": snapshot.stats}

    def project_report(self, snapshot_id: str | None = None) -> dict[str, Any]:
        from .project_report import build_project_report
        snapshot = self.snapshot(snapshot_id)
        return build_project_report(snapshot,self.store.get_findings(snapshot.id))

    def versions(self) -> dict[str, Any]:
        return {"items": self.store.list_snapshots(self.project_id)}

    def findings(self, snapshot_id: str | None = None, *, severity: str = "", kind: str = "", query: str = "") -> dict[str, Any]:
        snapshot = self.snapshot(snapshot_id)
        decisions = self.store.list_decisions(snapshot_id=snapshot.id)
        latest_decisions: dict[str, dict[str, Any]] = {}
        for decision in sorted(decisions, key=lambda d: (d.get("sequence", 0), d.get("created_at", ""))):
            latest_decisions[decision["finding_id"]] = decision
        items = []
        for finding in self.store.get_findings(snapshot.id):
            if severity and finding.severity != severity:
                continue
            if kind and finding.type != kind:
                continue
            value = asdict(finding)
            if query and query.casefold() not in " ".join([finding.title, finding.description, finding.rule_id,
                                                          *finding.node_ids]).casefold():
                continue
            decision = latest_decisions.get(finding.id)
            active = bool(decision)
            if decision and decision.get("expires_at"):
                try:
                    active = datetime.fromisoformat(decision["expires_at"].replace("Z", "+00:00")) > datetime.now(timezone.utc)
                except (ValueError, TypeError):
                    active = False
            value["decision"] = decision
            value["disposition"] = decision["action"] if decision and active else "unreviewed"
            value["decision_expired"] = bool(decision) and not active
            items.append(value)
        return {"snapshot_id": snapshot.id, "items": items}

    def finding(self, finding_id: str, snapshot_id: str | None = None) -> dict[str, Any]:
        if not isinstance(finding_id, str) or not finding_id.strip():
            raise ValueError("finding_id 必须为非空字符串")
        for item in self.findings(snapshot_id)["items"]:
            if item["id"] == finding_id:
                return item
        raise KeyError("当前快照中没有该发现")

    def source(self, file: str, snapshot_id: str | None = None, line: int = 1) -> dict[str, Any]:
        snapshot = self.snapshot(snapshot_id)
        for source in snapshot.files:
            if source.path == file:
                return {"snapshot_id": snapshot.id, "file": source.path, "content": source.content, "hash": source.hash,
                        "line": max(1, line), "status": source.status, "error": source.error}
        captured = snapshot.input_evidence.get(file)
        if captured is not None:
            return {"snapshot_id": snapshot.id, "file": file, "content": captured["content"],
                    "hash": captured["hash"], "line": max(1, line), "status": captured["status"],
                    "error": captured["error"], "kind": "support_input", "text_hash": captured["text_hash"]}
        raise KeyError("文件不在该快照中；源码接口不会读取当前磁盘上的任意路径")

    def path(self, source: str, target: str, snapshot_id: str | None = None) -> dict[str, Any]:
        if any(not isinstance(value, str) or not value.strip() for value in (source, target)):
            raise ValueError("路径端点必须为非空字符串")
        snapshot = self.snapshot(snapshot_id)
        result = find_path(snapshot, source, target)
        return {**result, "snapshot_id": snapshot.id}

    def subgraph(self, node_id: str, snapshot_id: str | None = None, depth: int = 2, direction: str = "both") -> dict[str, Any]:
        if not isinstance(node_id, str) or not node_id.strip():
            raise ValueError("node_id 必须为非空字符串")
        if isinstance(depth, bool) or not isinstance(depth, int) or not 0 <= depth <= 8:
            raise ValueError("探索深度必须为 0 到 8；此限制不用于检测计算")
        if direction not in {"both", "in", "out"}:
            raise ValueError("direction 必须为 both/in/out")
        snapshot = self.snapshot(snapshot_id)
        return {**subgraph(snapshot, node_id, depth, direction), "snapshot_id": snapshot.id}

    def diff(self, old_id: str, new_id: str) -> dict[str, Any]:
        old, new = self.snapshot(old_id), self.snapshot(new_id)
        return diff_snapshots(old, new, self.store.get_findings(old.id), self.store.get_findings(new.id))

    def decide(self, snapshot_id: str, finding_id: str, action: str, reason: str, expires_at: str | None = None) -> dict[str, Any]:
        self.snapshot(snapshot_id)
        return {"decision": self.store.record_decision(snapshot_id, finding_id, action, reason,
                                                        actor="local", expires_at=expires_at)}

    def decisions(self, snapshot_id: str | None = None, finding_id: str | None = None) -> dict[str, Any]:
        if finding_id is not None and (not isinstance(finding_id, str) or not finding_id.strip()):
            raise ValueError("finding_id 必须为非空字符串或省略")
        snapshot = self.snapshot(snapshot_id)
        return {"items": self.store.list_decisions(snapshot_id=snapshot.id, finding_id=finding_id)}

    def start_watch(self, interval: float = 2.0) -> None:
        if not isinstance(interval, (int, float)) or isinstance(interval, bool) or not math.isfinite(interval) or interval < 0.5:
            raise ValueError("监听间隔不得小于 0.5 秒")
        if self._watch_thread is not None and self._watch_thread.is_alive():
            return
        self._stop.clear()

        def watch() -> None:
            while not self._stop.wait(interval):
                try:
                    self.scan()
                except Exception:
                    # scan already records failure; preserve the last published snapshot.
                    continue

        self._watch_thread = threading.Thread(target=watch, name="callscope-static-watch", daemon=True)
        self._watch_thread.start()

    def close(self) -> None:
        self._stop.set()
        if self._watch_thread:
            self._watch_thread.join(timeout=5.0)
        # Wait for a running source reader before releasing the storage connection.
        with self._scan_lock:
            self.store.close()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _metadata(snapshot: GraphSnapshot) -> dict[str, Any]:
    return {key: getattr(snapshot, key) for key in ("id", "project_id", "project_name", "root", "created_at", "status",
                                                    "source_hash", "policy_hash", "analyzer_version", "detector_version", "schema_version", "parser_version")}

