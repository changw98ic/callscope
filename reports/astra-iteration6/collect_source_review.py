"""Export a small review artifact from a published CallScope snapshot.

Reads only the tool's database. Source quotes come from captured snapshot text;
this script does not read, import, run or test either target repository.
Run with PYTHONPATH set to the CallScope tool directory.
"""

import argparse
from collections import Counter
from dataclasses import asdict
from fnmatch import fnmatchcase
import json
from pathlib import Path
import sqlite3

from callscope.graph import GraphIndex
from callscope.store import Store


def collect(name, directory):
    database = directory / f"{name}-v9.sqlite3"
    connection = sqlite3.connect("file:" + str(database.resolve()) + "?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    row = connection.execute(
        "SELECT id,project_id,project_name,root,status,source_hash,policy_hash,"
        "analyzer_version,detector_version,schema_version,stats_json,finding_count "
        "FROM snapshots ORDER BY sequence DESC LIMIT 1"
    ).fetchone()
    if row is None:
        raise ValueError("No published snapshot")
    summary = dict(row)
    summary["stats"] = json.loads(summary.pop("stats_json"))
    summary["finding_counts"] = [dict(item) for item in connection.execute(
        'SELECT json_extract(finding_json,"$.type") AS type, '
        'json_extract(finding_json,"$.status") AS status, count(*) AS count '
        'FROM findings WHERE snapshot_id=? GROUP BY type,status', (row["id"],)
    )]
    rule_findings = [json.loads(item[0]) for item in connection.execute(
        'SELECT finding_json FROM findings WHERE snapshot_id=? AND '
        'coalesce(json_extract(finding_json,"$.rule_id"),"") != ""', (row["id"],)
    )]
    summary["rule_findings"] = rule_findings
    connection.close()
    with Store(database) as store:
        snapshot = store.get_snapshot(row["id"])
    summary["problem_files"] = [
        {key: value for key, value in asdict(source).items() if key != "content"}
        for source in snapshot.files if source.status != "parsed"
    ]
    summary["project_diagnostics"] = [asdict(item) for item in snapshot.diagnostics]
    index = GraphIndex(snapshot)
    sources = {source.path: source for source in snapshot.files}

    def quote(edge):
        source = sources.get(edge.file)
        lines = source.content.splitlines() if source is not None else []
        return {"edge_id": edge.id, "file": edge.file, "line": edge.line,
                "column": edge.column, "expression": edge.expression,
                "source_hash": source.hash if source is not None else None,
                "source_line": lines[edge.line - 1] if 0 < edge.line <= len(lines) else ""}

    observations = []
    for rule in snapshot.config["rules"]:
        matching = lambda pattern: sorted(node.id for node in snapshot.nodes
            if fnmatchcase(node.id, pattern) or fnmatchcase(node.qualname, pattern))
        start_ids, target_ids = matching(rule["from"]), matching(rule["to"])
        confirmed_paths = []
        for source in start_ids:
            if rule["kind"].endswith("_call"):
                edges = [edge for edge in index.outgoing[source] if edge.target in target_ids]
                node_path = [source, edges[0].target] if edges else []
                edge_path = [edges[0].id] if edges else []
            else:
                node_path, edge_path, _ = index.shortest_path(source, set(target_ids), minimum_edges=1)
            if edge_path:
                confirmed_paths.append({"source_id": source, "node_ids": node_path,
                    "edge_ids": edge_path, "source_witnesses": [quote(index.edges[eid]) for eid in edge_path]})
        related = [finding for finding in rule_findings if finding["rule_id"] == rule["id"]]
        unknown_edges = [edge for source in start_ids for edge in index.unknown[source]]
        observations.append({
            "rule_id": rule["id"], "kind": rule["kind"], "from": rule["from"], "to": rule["to"],
            "matched_source_ids": start_ids, "matched_target_ids": target_ids,
            "confirmed_paths": confirmed_paths,
            "confirmed_connection_present": bool(confirmed_paths),
            "rule_finding_ids": [item["id"] for item in related],
            "rule_finding_statuses": [item["status"] for item in related],
            "unknown_outgoing_count": len(unknown_edges),
            "unknown_outgoing_samples": [{**quote(edge), "resolution": edge.resolution,
                "reason": edge.reason} for edge in unknown_edges[:20]],
            "unknown_samples_truncated": len(unknown_edges) > 20,
            "repository_approved_requirement": False,
            "interpretation": "source relationship baseline; not a target functional pass/fail",
        })
    summary["rule_observation_counts"] = {
        "total": len(observations),
        "required_connection_reproduced": sum(item["kind"].startswith("required_")
            and bool(item["confirmed_paths"]) for item in observations),
        "rules_with_uncertainty": sum("uncertain" in item["rule_finding_statuses"] for item in observations),
        "forbidden_connection_observed": sum(item["kind"].startswith("forbidden_")
            and bool(item["confirmed_paths"]) for item in observations),
    }
    summary["calls_by_resolution"] = dict(Counter(edge.resolution for edge in snapshot.edges))
    witnesses = {"snapshot_id": snapshot.id, "source_hash": snapshot.source_hash,
        "policy_hash": snapshot.policy_hash, "detector_version": snapshot.detector_version,
        "component_versions": snapshot.stats["component_versions"],
        "target_executed": False, "target_tests_run": False,
        "observations": observations}
    for suffix, value in (("summary", summary), ("rule-witnesses", witnesses)):
        with (directory / f"{name}-{suffix}.json").open("w", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
    print(json.dumps({"repository": name, "snapshot_id": snapshot.id,
                      "status": snapshot.status, "rule_observation_counts": summary["rule_observation_counts"]}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", choices=("codepatchbay", "winwincode"))
    arguments = parser.parse_args()
    collect(arguments.name, Path(__file__).resolve().parent)
