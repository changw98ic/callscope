"""Ordinary full saved-source channel query; never executes target code."""
from pathlib import Path
import hashlib
import json
import sqlite3

from callscope.store import _snapshot_from_json
from callscope.pipeline_flow import _Analysis, validate_pipeline_flow_rule
from callscope.pipeline_channels import VERSION, analyze_pipeline_channels

directory = Path(__file__).resolve().parent
connection = sqlite3.connect("file:" + str(directory.parent / "astra-iteration9/codepatchbay-v11.sqlite3") + "?mode=ro&immutable=1", uri=True)
row = connection.execute("SELECT snapshot_json,detector_version,schema_version FROM snapshots ORDER BY sequence DESC LIMIT 1").fetchone()
connection.close()
snapshot = _snapshot_from_json(*row)
rule = json.loads((directory / "pipeline-rule.json").read_text())
validate_pipeline_flow_rule(rule)
analysis = _Analysis(snapshot, rule)
details = analyze_pipeline_channels(analysis)
details["query_identity"] = {
    "version": VERSION,
    "module_sha256": hashlib.sha256((directory.parent.parent / "callscope/pipeline_channels.py").read_bytes()).hexdigest(),
    "query_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "source_snapshot_database": "reports/astra-iteration9/codepatchbay-v11.sqlite3",
    "source_snapshot_complete_metadata_retained": True,
    "query_kind": "ordinary_saved_source_query",
    "analysis_gaps": analysis.gaps,
}
(directory / "PIPELINE_CHANNEL_OBSERVATION.json").write_text(json.dumps(details, ensure_ascii=False, indent=2) + "\n")
compact = {
    "snapshot_id": details["snapshot_id"],
    "supported": details["supported"],
    "gaps": [{"code": item["code"], "states": item.get("states")} for item in details["gaps"]],
    "analysis_gaps": analysis.gaps,
    "sections": {key: {"supported": details[key]["supported"], "states": {name: item.get("supported") for name, item in details[key].items() if isinstance(item, dict) and "supported" in item}}
        for key in ("queue", "inbox", "broker", "counter_transport")},
    "query_identity": details["query_identity"],
}
print(json.dumps(compact, ensure_ascii=False), flush=True)
