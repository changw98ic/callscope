"""Normal read-only saved-source queries; no target import or execution."""
from __future__ import annotations

import argparse
from dataclasses import asdict
import fcntl
import hashlib
import json
from pathlib import Path
import sqlite3
from urllib.parse import quote

from callscope.report_chain_analysis import _Analysis
from callscope.semantic_sources import SemanticSources
from callscope.store import _snapshot_from_json

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
LOCK = ROOT / ".analysis-tools/goal-source-query.lock"
MODULE = ROOT / "callscope/lifecycle_ownership_relations.py"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", choices=("codepatchbay", "winwincode"))
    parser.add_argument("--discover", action="store_true")
    parser.add_argument("--rules", type=Path)
    options = parser.parse_args()
    database = ROOT / f"reports/astra-iteration10/{options.repository}-v12.sqlite3"
    with LOCK.open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        from callscope.lifecycle_ownership_relations import VERSION, analyze_pattern
        imported_module_sha256 = hashlib.sha256(MODULE.read_bytes()).hexdigest()
        connection = sqlite3.connect("file:" + quote(str(database), safe="/") + "?mode=ro&immutable=1", uri=True)
        row = connection.execute("SELECT snapshot_json,detector_version,schema_version FROM snapshots ORDER BY sequence DESC LIMIT 1").fetchone()
        connection.close()
        snapshot = _snapshot_from_json(row[0], row[1], row[2])
        del row
        sources = SemanticSources(snapshot)
        result = {"kind": "development_saved_snapshot_source_query", "module_version": VERSION,
            "module_sha256": imported_module_sha256, "base_snapshot_id": snapshot.id,
            "base_source_hash": snapshot.source_hash, "base_policy_hash": snapshot.policy_hash,
            "old_snapshot_republished": False, "formal_frozen_scan": False,
            "target_executed": False, "target_tests_run": False, "target_build_run": False}
        if options.discover:
            paths = (["apps/client/src/application.ts", "apps/client/src/settings-page.ts",
                "crates/winwincode-control-plane/src/delivery_production_adapters.rs",
                "crates/winwincode-delivery/src/application/workrun.rs", "crates/winwincode-worker/src/lib.rs",
                "crates/winwincode-codex/src/adapter.rs", "crates/kernel/src/lib.rs"]
                if options.repository == "winwincode" else ["server/services/event/event-store.ts",
                    "server/services/event/event-materializer.ts", "server/services/job/job-store.ts",
                    "server/services/hub/hub-queue.ts"])
            result["definitions"] = {}
            for path in paths:
                document, problems = sources.load(path)
                result["definitions"][path] = {"issues": problems, "symbols": [
                    {"symbol": symbol, "line": definition.node.start_point.row + 1,
                        "callable": definition.callable, "graph_node_id": definition.graph_node_id}
                    for symbol, values in document.definitions.items() for definition in values] if document else []}
            output = OUT / f"{options.repository}-lifecycle-ownership-selectors.json"
        else:
            rules = json.loads(options.rules.read_text(encoding="utf-8"))
            result["rules_sha256"] = hashlib.sha256(options.rules.read_bytes()).hexdigest()
            result["analyses"] = []
            for rule in rules:
                analysis = _Analysis(snapshot, rule, sources)
                analysis.load()
                pattern = analyze_pattern(analysis)
                result["analyses"].append({"id": rule["id"], "type": rule["type"],
                    "source_roles_loaded": list(analysis.roles), "source_graph_bindings_closed": analysis.role_binding_closed,
                    "source_facts": analysis.source_facts, "analysis_gaps": analysis.gaps, "pattern": pattern,
                    "budgets": {"operations": analysis.operations, "incomplete": analysis.incomplete},
                    "selectors": rule["sources"], "models": rule["models"]})
            output = OUT / ("lifecycle-source-query.json" if options.rules.name.startswith("lifecycle")
                else f"ownership-{options.repository}-source-query.json")
        result["module_bytes_stable_during_query"] = hashlib.sha256(MODULE.read_bytes()).hexdigest() == imported_module_sha256
        if not result["module_bytes_stable_during_query"]:
            raise RuntimeError("module changed during this development query; refusing to publish mixed-code observations")
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"output": str(output), "snapshot_id": snapshot.id,
            "summaries": [{"id": item["id"], "scope_supported": item["pattern"]["scoped_source_supported"],
                "source_facts": len(item["source_facts"]), "gaps": item["analysis_gaps"],
                "budgets": item["budgets"]} for item in result.get("analyses", [])]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
