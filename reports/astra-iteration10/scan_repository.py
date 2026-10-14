"""Publish v12 static analyses against the original report benchmark.

The new policy adds explicit source models and supplemental inert documents.
This is not a same-policy precision comparison. Target code is never invoked.
"""
import argparse
from dataclasses import asdict
import json
from pathlib import Path
from callscope.service import AnalysisService
from callscope.project_report import build_project_report,render_markdown
from publication_identity import check_identity,check_snapshot,write_json


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository",choices=("codepatchbay","winwincode"))
    args=parser.parse_args()
    directory=Path(__file__).resolve().parent
    freeze=check_identity(directory)
    root=directory.parents[2]/args.repository
    config=directory/f"{args.repository}-policy.json"
    database=directory/f"{args.repository}-v12.sqlite3"
    service=AnalysisService(root,database,config,engine="cocoindex")
    try:
        publications=[]
        for phase in ("cold","warm"):
            check_identity(directory)
            publication=service.scan()
            publications.append({"phase":phase,**publication})
            print(json.dumps({"repository":args.repository,"phase":phase,
                "snapshot_id":publication["snapshot_id"],"status":publication["status"],
                "created":publication["created"],"maintenance":publication["maintenance"]}),flush=True)
        snapshot=service.snapshot()
        check_snapshot(directory,snapshot)
        if publications[0]["snapshot_id"]!=publications[1]["snapshot_id"] or publications[1]["created"]:
            raise RuntimeError("Unchanged captured input was republished or changed its immutable identity")
        findings=service.store.get_findings(snapshot.id)
        report=build_project_report(snapshot,findings)
        write_json(directory/f"{args.repository}-automatic-report.json",report)
        (directory/f"{args.repository}-automatic-report.md").write_text(render_markdown(report),encoding="utf-8")
        write_json(directory/f"{args.repository}-configured-findings.json",[asdict(item)
            for item in findings if item.rule_id])
        summary={"repository":args.repository,"scans":publications,"snapshot_id":snapshot.id,
            "package_version":freeze["package_version"],"publication_series":"v12",
            "source_hash":snapshot.source_hash,"policy_hash":snapshot.policy_hash,
            "analyzer_version":snapshot.analyzer_version,"detector_version":snapshot.detector_version,
            "parser_version":snapshot.parser_version,"stats":snapshot.stats,
            "comparison":"New source models and inert support inputs; not a same-policy precision experiment.",
            "target_executed":False,"target_imported":False,"target_tests_run":False,"target_build_run":False}
        write_json(directory/f"{args.repository}-integration.json",summary)
        print(json.dumps({"repository":args.repository,"judgments":[{"goal_id":item["goal_id"],
                "complete":item["complete_assessment"],"supported":item["full_goal_supported"],
                "gaps":len(item["necessary_gaps"])} for item in report["judgments"]],
            "functional_chains":len(report["functional_chains"])}),flush=True)
    finally:
        service.close()


if __name__=="__main__":
    main()
