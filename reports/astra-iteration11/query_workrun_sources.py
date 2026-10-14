"""Inspect captured WorkRun CST; never import or execute target code."""
from dataclasses import asdict
import fcntl
import hashlib
import json
from pathlib import Path
import sqlite3

from callscope.semantic_sources import SemanticSources
from callscope.store import _snapshot_from_json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PATH = "crates/winwincode-delivery/src/application/workrun.rs"


def main():
    module_path = ROOT / "callscope/rust_state_relations.py"
    with (ROOT / ".analysis-tools/goal-source-query.lock").open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        connection = sqlite3.connect("file:" + str(HERE.parent / "astra-iteration10/winwincode-v12.sqlite3") + "?mode=ro&immutable=1", uri=True)
        row = connection.execute("SELECT snapshot_json,detector_version,schema_version FROM snapshots ORDER BY sequence DESC LIMIT 1").fetchone()
        connection.close()
        snapshot = _snapshot_from_json(*row)
        del row
        sources = SemanticSources(snapshot)
        document, issues = sources.load(PATH)
        if issues or document is None:
            raise ValueError(issues)
        print("snapshot", snapshot.id, "source_hash", document.source.hash, flush=True)
        if (HERE / "workrun-rule.json").exists():
            module_before = hashlib.sha256(module_path.read_bytes()).hexdigest()
            from callscope.report_chain_analysis import _Analysis
            from callscope.rust_state_relations import analyze_pattern
            rule = json.loads((HERE / "workrun-rule.json").read_text())
            analysis = _Analysis(snapshot, rule, sources)
            analysis.load()
            pattern = analyze_pattern(analysis)
            result = {"development_query": True, "saved_snapshot_id": snapshot.id,
                "saved_source_hash": snapshot.source_hash, "saved_policy_hash": snapshot.policy_hash,
                "new_rule_not_saved_in_snapshot": True,
                "pattern": pattern, "source_facts": analysis.source_facts,
                "analysis_gaps": analysis.gaps,
                "budget": {"operations": analysis.operations, "incomplete": analysis.incomplete},
                "target_executed": False, "target_tests_run": False, "target_build_run": False}
            result["query_module_sha256"] = module_before
            result["query_module_bytes_stable"] = module_before == hashlib.sha256(module_path.read_bytes()).hexdigest()
            (HERE / "workrun-source-query.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
            print(json.dumps({"supported": pattern.get("scoped_source_supported"),
                "selection_checks": pattern.get("persisted_selection_recheck_relation", {}).get("checks"),
                "table": pattern.get("finite_effective_state_relation", {}).get("rows"),
                "gaps": analysis.gaps, "module_sha256": result["query_module_sha256"],
                "module_bytes_stable": result["query_module_bytes_stable"],
                "facts": len(analysis.source_facts), "operations": analysis.operations,
                "incomplete": analysis.incomplete}, ensure_ascii=False), flush=True)
        else:
            wanted = {"WorkRunAggregate.start_next", "WorkRunAggregate.start_item", "effective_work_item_state", "start_next_work_run"}
            for symbol in sorted(wanted):
                definition = document.definitions[symbol][0]
                def render(node, depth=0):
                    if depth > 20:
                        return {"type": node.type, "truncated": True}
                    return {"type": node.type, "text": document.text(node)[:250],
                        "fields": {node.field_name_for_child(i): child.type for i, child in enumerate(node.children) if node.field_name_for_child(i)},
                        "children": [render(child, depth + 1) for child in node.named_children]}
                (HERE / ("workrun-cst-" + symbol.replace(".", "-") + ".json")).write_text(json.dumps(render(definition.node), ensure_ascii=False, indent=2) + "\n")
                print("captured_cst", symbol, flush=True)


if __name__ == "__main__":
    main()
