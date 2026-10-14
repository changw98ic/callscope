"""Compare every original frozen observation with final saved v13 publications.

The unchanged CallScope 1.3 evaluator is reused. SQLite is opened read-only;
full saved-source loads are serialized by the shared flock. Only Git commit
metadata and the original 36 referenced raw files are read from target roots.
No target CLI, import, build, installation, test, or reviewer approval occurs.
"""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import closing, contextmanager
import fcntl
import hashlib
import json
from pathlib import Path, PurePosixPath
import sqlite3
import subprocess
import sys
from urllib.parse import quote

from callscope import __version__
from callscope.analysis_inputs import tool_identity
from callscope.baseline import evaluate_baseline, load_baseline, EVALUATOR_VERSION, EVALUATOR_SOURCE_HASH
from callscope.config import load_config
from callscope.models import ANALYZER_VERSION, DETECTOR_VERSION, SCHEMA_VERSION
from callscope.store import _snapshot_from_json
from publication_identity import EXPECTED_VERSIONS, check_contracts

BASELINE_SHA256 = "16b4b05c8818fa1eecf396132ebe2ea29a8f0068801165f0649da379d9041dd7"
CONTRACT_SHA256 = "c1d5c35d65a3adfe16fc14991f086a1914ad11217118508a5eeed3b896db88ff"
EVALUATOR_SHA256 = "db09661e194ca132aed2bf6f4405d3d33ef9ad4157cf690a03f84fb4fe72b905"
REPOSITORIES = ("codepatchbay", "winwincode")
INTERPRETATION = ("All 26 frozen source observations remain in the denominator. Evidence-only and intentional unknown items are preserved. "
    "This comparison is not precision, recall, functional coverage, runtime success, a business judgment, or approval.")


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def json_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f"Comparison artifact already exists; preserve the recorded round: {path}")
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")
    temporary.replace(path)


@contextmanager
def query_lock(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def package_inventory(package: Path) -> dict[str, str]:
    return {path.relative_to(package).as_posix(): digest(path) for path in sorted(package.rglob("*.py"))}


def frozen_file_checks(expected: object, directory: Path, label: str) -> list[dict]:
    if not isinstance(expected, dict) or not expected:
        raise ValueError(f"Formal freeze has no {label} inventory")
    checks = []
    for relative, expected_hash in sorted(expected.items()):
        path = PurePosixPath(relative)
        if (path.is_absolute() or ".." in path.parts or str(path) != relative
                or not isinstance(expected_hash, str) or len(expected_hash) != 64
                or any(character not in "0123456789abcdef" for character in expected_hash)):
            raise ValueError(f"Invalid {label} source-inventory path/hash")
        source = directory / relative
        actual = digest(source) if source.is_file() else None
        checks.append({"path": relative, "actual_path": str(source), "expected_sha256": expected_hash,
            "actual_sha256": actual, "matched": actual == expected_hash})
    return checks


def freeze_identity(freeze_path: Path, archive: Path, *, policy_dir: Path, benchmark_dir: Path) -> tuple[dict, dict]:
    import callscope
    freeze = read_json(freeze_path)
    expected = freeze.get("package_source_sha256")
    if not isinstance(expected, dict) or not expected:
        raise ValueError("CORE_FREEZE.json has no exact Python package source inventory")
    for relative, value in expected.items():
        path = PurePosixPath(relative)
        if path.is_absolute() or ".." in path.parts or str(path) != relative or not relative.endswith(".py") or not isinstance(value, str):
            raise ValueError("Invalid core freeze source-inventory path/hash")
    package = Path(callscope.__file__).resolve().parent
    current = package_inventory(package)
    archived = package_inventory(archive) if archive.is_dir() else {}
    runtime_versions = {"package_version": __version__, "analyzer_version": ANALYZER_VERSION,
        "detector_version": DETECTOR_VERSION, "schema_version": SCHEMA_VERSION}
    version_matches = {key: freeze.get(key) == value for key, value in runtime_versions.items()}
    tool = tool_identity()
    benchmark_checks = frozen_file_checks(freeze.get("benchmark_reports"), benchmark_dir, "benchmark_reports")
    policy_checks = frozen_file_checks(freeze.get("policy_files"), policy_dir, "policy_files")
    pyproject_checks = {"current_matches": digest(package.parent / "pyproject.toml") == freeze.get("pyproject_sha256"),
        "archive_matches": digest(archive / "pyproject.delivery.toml") == freeze.get("pyproject_sha256")}
    result = {"freeze_path": str(freeze_path), "freeze_sha256": digest(freeze_path),
        "archive_path": str(archive), "publication_series": freeze.get("publication_series"),
        "tool_identity": tool, "expected_tool_identity": freeze.get("tool_identity"),
        "tool_identity_matches": tool == freeze.get("tool_identity"),
        "runtime_versions": runtime_versions, "version_matches": version_matches,
        "expected_python_source_count": len(expected), "current_python_source_count": len(current), "archive_python_source_count": len(archived),
        "current_inventory_matches": current == expected, "archive_inventory_matches": archived == expected,
        "current_missing_paths": sorted(set(expected) - set(current)), "current_extra_paths": sorted(set(current) - set(expected)),
        "current_changed_paths": sorted(path for path in expected.keys() & current.keys() if expected[path] != current[path]),
        "archive_missing_paths": sorted(set(expected) - set(archived)), "archive_extra_paths": sorted(set(archived) - set(expected)),
        "archive_changed_paths": sorted(path for path in expected.keys() & archived.keys() if expected[path] != archived[path]),
        "archive_inventory_sha256": json_hash(archived), "current_inventory_sha256": json_hash(current),
        "benchmark_report_checks": benchmark_checks, "frozen_policy_file_checks": policy_checks,
        "pyproject_checks": pyproject_checks,
        "is_review_or_approval": False}
    result["verified"] = bool(result["tool_identity_matches"] and all(version_matches.values())
        and result["current_inventory_matches"] and result["archive_inventory_matches"] and freeze.get("publication_series") == "v13"
        and all(freeze.get(key) == value for key, value in EXPECTED_VERSIONS.items())
        and all(pyproject_checks.values()) and all(check["matched"] for check in [*benchmark_checks, *policy_checks]))
    return freeze, result


def connect_read_only(path: Path) -> sqlite3.Connection:
    # Final publications must be closed/checkpointed. A nonempty WAL is refused
    # rather than silently ignoring rows through immutable SQLite mode.
    wal = Path(str(path) + "-wal")
    if wal.exists() and wal.stat().st_size:
        raise ValueError(f"Publication still has a nonempty WAL; close/checkpoint it before comparison: {path}")
    connection = sqlite3.connect("file:" + quote(str(path.resolve()), safe="/") + "?mode=ro&immutable=1", uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def latest_metadata(connection: sqlite3.Connection, root: str) -> dict:
    row = connection.execute("""SELECT s.id,s.project_id,s.root,s.source_hash,s.policy_hash,s.analyzer_version,
        s.detector_version,s.schema_version,s.stats_json,s.finding_count
        FROM project_latest p JOIN snapshots s ON s.id=p.snapshot_id AND s.project_id=p.project_id
        WHERE s.root=? ORDER BY p.published_at DESC,s.sequence DESC LIMIT 1""", (root,)).fetchone()
    if row is None:
        raise ValueError(f"No published snapshot for root {root}")
    result = dict(row)
    result["stats"] = json.loads(result.pop("stats_json"))
    result["finding_type_counts"] = {row["kind"]: row["total"] for row in connection.execute(
        "SELECT json_extract(finding_json,'$.type') AS kind,COUNT(*) AS total FROM findings WHERE snapshot_id=? GROUP BY kind", (result["id"],))}
    return result


def saved_snapshot(connection: sqlite3.Connection, identifier: str):
    row = connection.execute("SELECT snapshot_json,detector_version,schema_version FROM snapshots WHERE id=?", (identifier,)).fetchone()
    if row is None:
        raise ValueError("Published metadata has no matching saved snapshot")
    return _snapshot_from_json(row["snapshot_json"], row["detector_version"], row["schema_version"])


def changes(previous: dict, current: dict) -> list[dict]:
    before = {item["id"]: item for item in previous["observations"]}
    after = {item["id"]: item for item in current["observations"]}
    if set(before) != set(after):
        raise ValueError("Frozen observation IDs changed between comparison artifacts")
    return [{"id": identifier, "before": before[identifier]["status"], "after": after[identifier]["status"],
        "before_expectation_satisfied": before[identifier].get("expectation_satisfied"), "after_expectation_satisfied": after[identifier].get("expectation_satisfied")}
        for identifier in before if before[identifier]["status"] != after[identifier]["status"]
        or before[identifier].get("expectation_satisfied") != after[identifier].get("expectation_satisfied")]


def policy_scope(previous_path: Path, current_path: Path, snapshot: object, previous_result: dict) -> dict:
    previous = read_json(previous_path)
    current = read_json(current_path)
    sections = []
    for name in sorted(set(previous) | set(current)):
        if previous.get(name) == current.get(name):
            continue
        old, new = previous.get(name), current.get(name)
        entry = {"section": name, "before_sha256": json_hash(old), "after_sha256": json_hash(new)}
        if isinstance(old, list) and isinstance(new, list) and all(isinstance(item, dict) and isinstance(item.get("id"), str) for item in [*old, *new]):
            old_ids, new_ids = {item["id"]: item for item in old}, {item["id"]: item for item in new}
            entry.update(added_ids=sorted(set(new_ids) - set(old_ids)), removed_ids=sorted(set(old_ids) - set(new_ids)),
                changed_ids=sorted(identifier for identifier in old_ids.keys() & new_ids.keys() if old_ids[identifier] != new_ids[identifier]))
        sections.append(entry)
    return {"previous_policy_path": str(previous_path), "previous_policy_sha256": digest(previous_path),
        "current_policy_path": str(current_path), "current_policy_sha256": digest(current_path),
        "policy_bytes_identical": previous_path.read_bytes() == current_path.read_bytes(), "changed_sections": sections,
        "saved_effective_policy_hash": snapshot.policy_hash, "saved_effective_analysis": snapshot.config.get("analysis", {}),
        "changed_models_and_capture_are_explicit": True,
        "maintenance_engine_change": {"previous": "cocoindex", "current": "full",
            "current_cold_and_warm_recompute_all_frontends": True,
            "same_engine_precision_or_performance_comparison_claimed": False},
        "repository_source_hash_changed_since_previous": snapshot.source_hash != previous_result["snapshot"]["source_hash"],
        "current_support_inputs": [{"path": path, "hash": record.get("hash"), "status": record.get("status"), "language": record.get("language")}
            for path, record in sorted(snapshot.input_evidence.items())],
        "current_captured_code_file_status_counts": dict(Counter(source.status for source in snapshot.files)),
        "original_frozen_rule_and_observation_bytes_changed": False}


def target_identity(repository: dict, root: Path, source_checks: list[dict]) -> dict:
    command = subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "-c", "core.fsmonitor=false", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, check=False)
    commit = command.stdout.strip() if command.returncode == 0 else None
    live = []
    for relative, expected in sorted(repository["source_files"].items()):
        path = root / relative
        actual = digest(path) if path.is_file() else None
        live.append({"path": relative, "expected_sha256": expected, "actual_sha256": actual,
            "status": "matched" if actual == expected else "source_missing" if actual is None else "source_changed"})
    return {"root": str(root), "frozen_commit": repository["commit"], "actual_commit": commit,
        "commit_matches": commit == repository["commit"], "git_metadata_read_only": True,
        "git_read_error": command.stderr.strip()[:1000] if command.returncode else None,
        "working_tree_clean_claimed": False, "live_referenced_source_checks": live,
        "live_referenced_source_hashes_match": all(item["status"] == "matched" for item in live),
        "saved_referenced_source_checks": source_checks,
        "saved_referenced_source_hashes_match": all(item["status"] == "matched" for item in source_checks)}


def main() -> int:
    directory = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codepatchbay-db", type=Path, default=directory / "codepatchbay-v13.sqlite3")
    parser.add_argument("--winwincode-db", type=Path, default=directory / "winwincode-v13.sqlite3")
    parser.add_argument("--freeze", type=Path, default=directory / "CORE_FREEZE.json")
    parser.add_argument("--archive", type=Path, default=directory / "frozen-core-source")
    parser.add_argument("--output-dir", type=Path, default=directory)
    parser.add_argument("--policy-dir", type=Path, default=directory)
    parser.add_argument("--benchmark-dir", type=Path, default=directory.parent)
    parser.add_argument("--previous-dir", type=Path, default=directory.parent / "astra-iteration10")
    parser.add_argument("--baseline", type=Path, default=directory.parent / "astra-baseline" / "capability-baseline.json")
    parser.add_argument("--baseline-contract", type=Path, default=directory.parent / "astra-baseline" / "BASELINE_CONTRACT.md")
    parser.add_argument("--query-lock", type=Path, default=directory.parents[1] / ".analysis-tools" / "goal-source-query.lock")
    parser.add_argument("--codepatchbay-root", type=Path)
    parser.add_argument("--winwincode-root", type=Path)
    args = parser.parse_args()
    required = [args.baseline, args.baseline_contract, args.freeze, args.codepatchbay_db, args.winwincode_db,
        *(args.policy_dir / f"{name}-integration.json" for name in REPOSITORIES)]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        print(json.dumps({"state": "not_ready", "missing_paths": missing, "fixtures_created": False}))
        return 2
    check_contracts(directory)
    if digest(args.baseline) != BASELINE_SHA256 or digest(args.baseline_contract) != CONTRACT_SHA256:
        raise ValueError("Original baseline or BASELINE_CONTRACT bytes changed")
    if EVALUATOR_VERSION != "frozen-static-baseline-1.3" or EVALUATOR_SOURCE_HASH != EVALUATOR_SHA256:
        raise ValueError("Original baseline evaluator implementation changed")
    baseline = load_baseline(args.baseline)
    if len(baseline["observations"]) != 26 or len(baseline["repositories"]) != 2:
        raise ValueError("Original 26-observation/two-repository denominator changed")
    identity = {"schema_version": 1, "kind": "original_baseline_publication_identity", "baseline_sha256": BASELINE_SHA256,
        "publication_series": "v13", "previous_publication_series": "v12",
        "artifact_script_path": str(Path(__file__).resolve()), "artifact_script_sha256": digest(Path(__file__).resolve()),
        "artifact_script_is_core_freeze_member": False,
        "baseline_contract_sha256": CONTRACT_SHA256, "baseline_id": baseline["baseline_id"], "observation_count": 26,
        "referenced_raw_file_count": sum(len(item["source_files"]) for item in baseline["repositories"]),
        "evaluator_version": EVALUATOR_VERSION, "evaluator_source_hash": EVALUATOR_SOURCE_HASH,
        "query_lock": {"path": str(args.query_lock), "protocol": "fcntl.flock LOCK_EX; compatible with shell flock"},
        "repositories": [], "target_executed": False, "target_tests_run": False, "tool_test_suite_run": False,
        "is_review_or_approval": False, "interpretation": INTERPRETATION}
    comparisons = []
    with query_lock(args.query_lock):
        freeze, implementation = freeze_identity(args.freeze, args.archive,
            policy_dir=args.policy_dir, benchmark_dir=args.benchmark_dir)
        identity["implementation"] = implementation
        if not implementation["verified"]:
            identity["verified"] = False
            write_json(args.output_dir / "PUBLICATION_IDENTITY.json", identity)
            raise ValueError("Current tool/archive differs from the formal v13 freeze; identity report saved")
        for name in REPOSITORIES:
            repository = next(item for item in baseline["repositories"] if item["id"] == name)
            root = getattr(args, name + "_root") or Path(repository["root"])
            database = getattr(args, name + "_db")
            integration_path = args.policy_dir / f"{name}-integration.json"
            integration = read_json(integration_path)
            phases = integration.get("scans", [])
            if (integration.get("publication_series") != "v13" or integration.get("database_closed") is not True
                    or integration.get("database_wal_empty_or_absent") is not True
                    or integration.get("publication_maintenance_engine") != "full" or len(phases) != 2
                    or [phase.get("phase") for phase in phases] != ["cold", "warm"]
                    or phases[0].get("created") is not True or phases[1].get("created") is not False
                    or any(phase.get("snapshot_id") != integration.get("snapshot_id") for phase in phases)
                    or any(phase.get("maintenance") != {"engine": "full", "global_detection": "full"} for phase in phases)):
                raise ValueError(f"{name} has no completed, closed v13 full cold/warm publication marker")
            previous_path = args.previous_dir / f"{name}-baseline-v12-and-v11.json"
            previous = read_json(previous_path)["current"]
            if previous["snapshot"].get("analyzer_version") != "static-multilang-12":
                raise ValueError("Previous comparison artifact is not the formal v12 result")
            for key, expected in (("baseline_id", baseline["baseline_id"]), ("baseline_total", 26), ("evaluator_version", EVALUATOR_VERSION), ("evaluator_source_hash", EVALUATOR_SOURCE_HASH)):
                if previous.get(key) != expected:
                    raise ValueError(f"Previous frozen comparison differs in {key}")
            with closing(connect_read_only(database)) as connection:
                metadata = latest_metadata(connection, str(root))
                versions = metadata["stats"].get("component_versions", {})
                checks = {key: metadata.get(key) == freeze.get(key) for key in ("analyzer_version", "detector_version", "schema_version")}
                checks["tool_identity"] = versions.get("tool") == freeze["tool_identity"]
                checks["integration_snapshot_matches"] = metadata["id"] == integration["snapshot_id"]
                checks["integration_source_and_policy_matches"] = all(metadata[key] == integration[key] for key in ("source_hash", "policy_hash"))
                checks["integration_tool_matches"] = integration["stats"]["component_versions"]["tool"] == freeze["tool_identity"]
                checks["maintenance_engine_is_full"] = versions.get("maintenance") == {"backend": "full"}
                frozen_policy = load_config(root, args.policy_dir / f"{name}-policy.json")
                checks["effective_policy_hash_matches_frozen_policy"] = metadata["policy_hash"] == json_hash(frozen_policy)
                if not all(checks.values()):
                    identity["repositories"].append({"repository": name, "database": str(database), "metadata": metadata, "publication_identity_checks": checks})
                    identity["verified"] = False
                    write_json(args.output_dir / "PUBLICATION_IDENTITY.json", identity)
                    raise ValueError(f"{name} publication does not match the formal tool freeze")
                snapshot = saved_snapshot(connection, metadata["id"])
                current = evaluate_baseline(snapshot, baseline, name)
                expected_ids = {item["id"] for item in baseline["observations"] if item["repo"] == name}
                if current["baseline_total"] != 26 or {item["id"] for item in current["observations"]} != expected_ids:
                    raise ValueError("Comparison omitted or changed original observations")
                if {item["path"] for item in current["source_checks"]} != set(repository["source_files"]):
                    raise ValueError("Comparison omitted an original referenced file hash")
                scope = policy_scope(args.previous_dir / f"{name}-policy.json", args.policy_dir / f"{name}-policy.json", snapshot, previous)
                live = target_identity(repository, root, current["source_checks"])
                result = {"current": current, "previous": previous, "changes": changes(previous, current),
                    "previous_result_origin": str(previous_path), "previous_artifact_sha256": digest(previous_path),
                    "previous_store_opened": False, "scope_changes": scope, "target_identity": live,
                    "interpretation": INTERPRETATION, "target_executed": False, "target_tests_run": False, "tool_test_suite_run": False}
                write_json(args.output_dir / f"{name}-baseline-v13-and-v12.json", result)
                write_json(args.output_dir / f"{name}-baseline-source-checks.json", {"repository": name, "snapshot_id": snapshot.id,
                    "source_checks": current["source_checks"], "observations": [{"id": item["id"], "source_checks": item["source_checks"]} for item in current["observations"]],
                    "target_identity": live, "interpretation": INTERPRETATION})
                identity["repositories"].append({"repository": name, "database": str(database), "database_sha256": digest(database),
                    "integration_artifact": str(integration_path), "integration_artifact_sha256": digest(integration_path),
                    "metadata": metadata, "publication_identity_checks": checks, "component_versions": versions,
                    "target_identity": live, "scope_changes": scope, "selected_observation_count": current["selected_total"]})
                comparisons.append({"repository": name, "snapshot_id": snapshot.id, "counts": current["counts"], "changes": result["changes"],
                    "selected_total": current["selected_total"], "comparison_artifact": f"{name}-baseline-v13-and-v12.json"})
                del snapshot
        common = set.intersection(*(set(item["component_versions"]) for item in identity["repositories"]))
        shared = {key: {"same_between_databases": identity["repositories"][0]["component_versions"][key] == identity["repositories"][1]["component_versions"][key],
            "values": {item["repository"]: item["component_versions"][key] for item in identity["repositories"]}} for key in sorted(common)}
        if "goal_contracts" in shared:
            declarations=shared["goal_contracts"]["values"]
            left,right=(declarations[item["repository"]] for item in identity["repositories"])
            adapters=set(left.get("adapters",{})) & set(right.get("adapters",{}))
            shared["goal_contracts"].update({
                "same_between_databases": all(left.get(key)==right.get(key) for key in ("registry","policy_schema"))
                    and all(left["adapters"][name]==right["adapters"][name] for name in adapters),
                "comparison_scope":"Shared registry/schema and shared adapter versions; enabled adapter selections legitimately differ by project.",
                "shared_adapter_names":sorted(adapters)})
        identity["shared_component_checks"] = shared
        identity["verified"] = bool(implementation["verified"] and all(item["target_identity"]["commit_matches"]
            and item["target_identity"]["live_referenced_source_hashes_match"] and item["target_identity"]["saved_referenced_source_hashes_match"] for item in identity["repositories"]))
        identity["same_shared_component_versions"] = all(item["same_between_databases"] for item in shared.values())
        identity["verified"] = identity["verified"] and identity["same_shared_component_versions"]
        if tool_identity() != freeze["tool_identity"]:
            identity["verified"] = False
            identity["tool_changed_during_comparison"] = True
        write_json(args.output_dir / "PUBLICATION_IDENTITY.json", identity)
        write_json(args.output_dir / "ORIGINAL_BASELINE_COMPARISON.json", {"schema_version": 1, "kind": "original_26_observation_comparison",
            "baseline_id": baseline["baseline_id"], "baseline_total": 26, "selected_total": sum(item["selected_total"] for item in comparisons),
            "repositories": comparisons, "publication_identity_verified": identity["verified"], "interpretation": INTERPRETATION})
    print(json.dumps({"baseline_total": 26, "repositories": comparisons, "publication_identity_verified": identity["verified"]}, ensure_ascii=False))
    return 0 if identity["verified"] else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, sqlite3.Error, KeyError, StopIteration) as error:
        print(json.dumps({"state": "failed", "error": str(error), "target_executed": False}), file=sys.stderr)
        raise SystemExit(1)
