"""Capture static cold/warm publications without running target code."""

import argparse
import json
from pathlib import Path

from callscope.service import AnalysisService


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", choices=("codepatchbay", "winwincode"))
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    tool_root = directory.parents[1]
    root = tool_root.parent / args.repository
    config = directory / f"{args.repository}-policy.json"
    database = directory / f"{args.repository}-v7.sqlite3"
    with_context = AnalysisService(root, database, config, engine="cocoindex")
    try:
        publications = []
        for phase in ("cold", "warm"):
            publication = with_context.scan()
            publications.append({"phase": phase, **publication})
            print(json.dumps({"repository": args.repository, "phase": phase,
                              "snapshot_id": publication["snapshot_id"], "status": publication["status"],
                              "created": publication["created"], "maintenance": publication["maintenance"]}), flush=True)
        snapshot = with_context.snapshot()
        report = {"repository": args.repository, "scans": publications,
                  "source_hash": snapshot.source_hash, "policy_hash": snapshot.policy_hash,
                  "analyzer_version": snapshot.analyzer_version, "detector_version": snapshot.detector_version,
                  "parser_version": snapshot.parser_version,
                  "target_executed": False, "target_tests_run": False,
                  "failed_files": [{"path": source.path, "status": source.status, "language": source.language,
                                    "error": source.error} for source in snapshot.files if source.status != "parsed"]}
        (directory / f"{args.repository}-integration.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    finally:
        with_context.close()


if __name__ == "__main__":
    main()
