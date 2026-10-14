"""Ordinary development query over immutable saved source; no target execution."""
import ast
import json
from pathlib import Path
import sqlite3
import time
import faulthandler
from callscope.store import _snapshot_from_json
from callscope.pipeline_flow import analyze_pipeline_flow
from callscope.pipeline_flow import _Analysis

faulthandler.dump_traceback_later(90, repeat=True)
for name in ("production_assembly", "record_field_relations", "local_record_transport", "budget_judgment"):
    original = getattr(_Analysis, name)
    def timed(self, *args, _name=name, _original=original, **kwargs):
        start = time.monotonic()
        print("source_stage_start", _name, flush=True)
        result = _original(self, *args, **kwargs)
        print("source_stage_end", _name, round(time.monotonic() - start, 3), flush=True)
        return result
    setattr(_Analysis, name, timed)

directory = Path(__file__).resolve().parent
ast.parse((directory.parent.parent / "callscope/pipeline_flow.py").read_text())
connection = sqlite3.connect("file:" + str(directory.parent / "astra-iteration9/codepatchbay-v11.sqlite3") + "?mode=ro&immutable=1", uri=True)
row = connection.execute("SELECT snapshot_json,detector_version,schema_version FROM snapshots ORDER BY sequence DESC LIMIT 1").fetchone()
connection.close()
snapshot = _snapshot_from_json(*row)
print("captured_source_loaded", snapshot.id, flush=True)
rule = json.loads((directory / "pipeline-rule.json").read_text())
details = analyze_pipeline_flow(snapshot, rule)
faulthandler.cancel_dump_traceback_later()
(directory / "PIPELINE_OBSERVATION.json").write_text(json.dumps(details, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"obligations": [{key: item[key] for key in ("id", "status", "necessary_gaps")} for item in details["obligations"]],
    "analysis_gaps": details["analysis_gaps"], "counts": details["evidence_counts"], "budget": details["summary_budget"]}, ensure_ascii=False), flush=True)
assembly = details["obligations"][1]["evidence"]["production_assembly"]
print("assembly", json.dumps({"gaps": assembly["gaps"], "cli_supported": assembly["cli"]["supported"], "request": assembly["request"],
    "worker_variants": assembly["worker_direct_broker_variants"], "process": assembly["worker_process_starts"], "receiver_count": len(assembly["constructor_receiver_assemblies"])}, ensure_ascii=False), flush=True)
relations = details["obligations"][2]["evidence"]["field_relations"]
print("field_profiles", json.dumps({"counts": {key: len(value) for key, value in relations.items() if isinstance(value, list)},
    "parameter_relations": relations["parameter_return_slot_relations"]}, ensure_ascii=False), flush=True)
print("channels", json.dumps({key: {"supported": value.get("supported"), "gaps": value.get("gaps")} for key, value in details["obligations"][2]["evidence"]["channels"].items() if isinstance(value, dict)}, ensure_ascii=False), flush=True)
print("budgets", json.dumps([{key: budget[key] for key in ("budget_kind", "source_complete", "gaps", "decision_guards")} for budget in details["obligations"][4]["evidence"]["budgets"]], ensure_ascii=False), flush=True)
