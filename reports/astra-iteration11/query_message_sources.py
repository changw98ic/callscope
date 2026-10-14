"""Normal source query of the saved v12 graph; no target code is executed."""
import fcntl
import hashlib
import json
from pathlib import Path
import sqlite3
from callscope.semantic_sources import SemanticSources
from callscope.store import _snapshot_from_json
from callscope.report_chain_analysis import _Analysis

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def main():
    with (ROOT / ".analysis-tools/goal-source-query.lock").open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        connection = sqlite3.connect("file:" + str(HERE.parent / "astra-iteration10/winwincode-v12.sqlite3") + "?mode=ro&immutable=1", uri=True)
        row = connection.execute("SELECT snapshot_json,detector_version,schema_version FROM snapshots ORDER BY sequence DESC LIMIT 1").fetchone()
        connection.close()
        snapshot = _snapshot_from_json(*row)
        del row
        sources = SemanticSources(snapshot)
        results = []
        module_path = ROOT / "callscope/message_identity_relations.py"
        module_sha = hashlib.sha256(module_path.read_bytes()).hexdigest()
        from callscope.message_identity_relations import analyze_pattern, VERSION
        for rule in json.loads((HERE / "messages-rules.json").read_text()):
            print("source_query_started", rule["id"], flush=True)
            analysis = _Analysis(snapshot, rule, sources)
            analysis.load()
            pattern = analyze_pattern(analysis)
            result = {"rule": rule, "pattern": pattern, "source_facts": analysis.source_facts,
                "analysis_gaps": analysis.gaps, "budget": {"operations": analysis.operations, "incomplete": analysis.incomplete}}
            results.append(result)
            print(json.dumps({"rule": rule["id"], "supported": pattern["scoped_source_supported"],
                "components": {name: value["supported"] for name, value in pattern["components"].items()},
                "facts": len(analysis.source_facts), "gaps": analysis.gaps,
                "budget": pattern["budget"]}, ensure_ascii=False), flush=True)
        output = {"development_query": True, "not_formal_v13_result": True,
            "saved_snapshot_id": snapshot.id, "saved_source_hash": snapshot.source_hash,
            "saved_policy_hash": snapshot.policy_hash, "module_version": VERSION,
            "current_module_sha256": module_sha,
            "query_core_bytes_stable": module_sha == hashlib.sha256(module_path.read_bytes()).hexdigest(),
            "new_rules_not_saved_in_snapshot": True, "results": results,
            "target_executed": False, "target_tests_run": False, "target_build_run": False}
        (HERE / "messages-source-query.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
        print("source_query_saved", len(results), flush=True)


if __name__ == "__main__":
    main()
