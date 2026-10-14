"""Normal development query of captured source; no target execution."""
import ast
import fcntl
import hashlib
import json
from pathlib import Path
import sqlite3

from callscope.conditional_gate_relations import VERSION, analyze_pattern
from callscope.report_chain_analysis import _Analysis
from callscope.semantic_sources import SemanticSources
from callscope.store import _snapshot_from_json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def main():
    module = ROOT / "callscope/conditional_gate_relations.py"
    ast.parse(module.read_text())
    before = hashlib.sha256(module.read_bytes()).hexdigest()
    with (ROOT / ".analysis-tools/goal-source-query.lock").open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        database = HERE.parent / "astra-iteration10/codepatchbay-v12.sqlite3"
        connection = sqlite3.connect("file:" + str(database) + "?mode=ro&immutable=1", uri=True)
        row = connection.execute("SELECT snapshot_json,detector_version,schema_version FROM snapshots ORDER BY sequence DESC LIMIT 1").fetchone()
        connection.close()
        snapshot = _snapshot_from_json(*row)
        del row
        sources = SemanticSources(snapshot)
        rows = []
        for rule in json.loads((HERE / "gates-rules.json").read_text()):
            analysis = _Analysis(snapshot, rule, sources)
            analysis.load()
            pattern = analyze_pattern(analysis)
            result = {"rule_id": rule["id"], "version": VERSION,
                "development_query": True, "not_a_formal_v13_saved_finding": True,
                "saved_v12_snapshot_id": snapshot.id, "saved_source_hash": snapshot.source_hash,
                "saved_policy_hash": snapshot.policy_hash, "rule_not_saved_in_old_snapshot": True,
                "pattern": pattern, "source_facts": analysis.source_facts,
                "analysis_gaps": analysis.gaps,
                "budget": {"operations": analysis.operations, "incomplete": analysis.incomplete},
                "target_executed": False, "target_tests_run": False, "target_build_run": False}
            rows.append(result)
            print(json.dumps({"rule": rule["id"], "supported": pattern["scoped_source_supported"],
                "gaps": analysis.gaps, "facts": len(analysis.source_facts), "operations": analysis.operations,
                "groups": list(pattern["groups"])}, ensure_ascii=False), flush=True)
        after = hashlib.sha256(module.read_bytes()).hexdigest()
        output = {"development_query": True, "module_sha256_before": before, "module_sha256_after": after,
            "module_bytes_stable": before == after, "saved_v12_snapshot_id": snapshot.id,
            "saved_source_hash": snapshot.source_hash, "saved_policy_hash": snapshot.policy_hash, "results": rows}
        (HERE / "gates-source-query.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
