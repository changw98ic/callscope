"""Capture static cold/warm v10 publications after the reviewed core freeze.

The policy is copied byte for byte from v9. Only trusted CallScope static
analysis runs: target code, tests, builds, installers and CLIs never run.
"""
import argparse
import json
from pathlib import Path
from callscope.service import AnalysisService
from publication_identity import check_identity, check_snapshot, write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", choices=("codepatchbay", "winwincode"))
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    original = directory.parent / "astra-iteration6" / f"{args.repository}-policy.json"
    config = directory / f"{args.repository}-policy.json"
    if not config.exists():
        config.write_bytes(original.read_bytes())
    freeze = check_identity(directory)
    root = directory.parents[2] / args.repository
    database = directory / f"{args.repository}-v10.sqlite3"
    service = AnalysisService(root, database, config, engine="cocoindex")
    try:
        publications = []
        for phase in ("cold", "warm"):
            publication = service.scan()
            publications.append({"phase": phase, **publication})
            print(json.dumps({"repository": args.repository, "phase": phase,
                              "snapshot_id": publication["snapshot_id"], "status": publication["status"],
                              "created": publication["created"], "maintenance": publication["maintenance"]}), flush=True)
        snapshot = service.snapshot()
        check_snapshot(directory, snapshot)
        previous = json.loads((directory.parent / "astra-iteration6" /
                               f"{args.repository}-summary.json").read_text())
        if snapshot.source_hash != previous["source_hash"] or snapshot.policy_hash != previous["policy_hash"]:
            raise RuntimeError("v9-v10 source/policy identity changed; publications cannot be compared as a precision repair")
        report = {"repository": args.repository, "scans": publications,
                  "package_version": freeze["package_version"], "publication_series": "v10",
                  "package_patch_note": freeze.get("package_patch_note"),
                  "source_hash": snapshot.source_hash, "policy_hash": snapshot.policy_hash,
                  "analyzer_version": snapshot.analyzer_version, "detector_version": snapshot.detector_version,
                  "parser_version": snapshot.parser_version,
                  "v9_source_and_policy_identical": True, "policy_bytes_identical_to_v9": True,
                  "target_executed": False, "target_imported": False,
                  "target_tests_run": False, "target_build_run": False,
                  "failed_files": [{"path": source.path, "status": source.status, "language": source.language,
                                    "error": source.error} for source in snapshot.files if source.status != "parsed"]}
        write_json(directory / f"{args.repository}-integration.json", report)
    finally:
        service.close()


if __name__ == "__main__":
    main()
