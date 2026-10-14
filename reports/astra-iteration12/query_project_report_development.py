"""Read real closed v13 data through current report builders, without fixtures.

Run only after the coordinator confirms the first source queries are finished.
This helper has its own common flock; never wrap it in another flock. It writes
Markdown and compact metadata, never a duplicate full analysis-report JSON.
"""
from __future__ import annotations

import argparse
from collections import Counter
import datetime
import fcntl
import gc
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import sys
import threading
import time
import traceback

from report_shared_references import resolve_pointer, validate_shared_references

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PREVIOUS = HERE.parent / "astra-iteration11"
COMMON_LOCK = ROOT / ".analysis-tools/goal-source-query.lock"


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def core_inventory() -> dict:
    package = ROOT / "callscope"
    return {str(path.relative_to(package)): digest(path) for path in sorted(package.rglob("*.py"))
        if "__pycache__" not in path.parts}


def fingerprint(path: Path) -> dict:
    value = path.stat()
    return {"device": value.st_dev, "inode": value.st_ino, "size_bytes": value.st_size,
        "mtime_ns": value.st_mtime_ns, "ctime_ns": value.st_ctime_ns}


def write_json(path: Path, value: dict) -> None:
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def location_summary(value: dict) -> dict:
    return {key: value[key] for key in ("file", "line", "column", "end_line", "end_column", "column_unit",
        "column_base", "coordinate_space", "start_byte", "end_byte", "source_hash", "span_hash",
        "semantic_parse_id", "raw_prefix_bytes", "original_file_start_byte", "original_file_end_byte",
        "location_ref", "pointer_scope") if key in value}






def boundary_summary(value: dict, pointer: str) -> dict:
    """Keep global unmodeled flags/limits, without copying relation fact trees."""
    retained = {}
    for key, item in value.items():
        if isinstance(item, bool) or item is None:
            retained[key] = item
        elif any(term in key for term in ("unreviewed", "unmodeled", "boundary", "boundaries", "limits", "scope_conditions")):
            retained[key] = item
        elif key in {"components", "groups"} and isinstance(item, dict):
            retained[key] = {name: boundary_summary(child, pointer + "/" + key + "/" + str(name))
                for name, child in item.items() if isinstance(child, dict)}
    return {"retained_global_boundary_fields": retained,
        "complete_source_pattern_remains_in_actual_saved_finding": True,
        "current_report_object_pattern_pointer": pointer,
        "local_relation_trees_not_duplicated": True}


def responsibility_summary(value: dict) -> dict:
    output = {"current_report_object_pointer": "/architecture/responsibility_explanations",
        "schema_keys": sorted(value), "operation_count": len(value.get("operations", [])),
        "operation_kind_counts": dict(sorted(Counter(item.get("operation_kind", "unknown")
            for item in value.get("operations", [])).items())),
        "declaration_explanation_count": len(value.get("declaration_explanations", [])),
        "explicit_source_transfer_count": len(value.get("explicit_source_transfers", [])),
        "normal_source_order_count": len(value.get("normal_source_orders", [])),
        "authenticated_interface_reuse_count": len(value.get("authenticated_interface_reuse", [])),
        "declaration_explanations": []}
    # Preserve all global gaps, scope, flags, models and unknown boundaries.
    for key in ("version", "operation_extractor_version", "snapshot_identity", "operation_extraction_identity",
                "analysis_gaps", "explanation_source_gaps", "operation_extraction_scope", "operation_extraction_flags",
                "operation_extraction_budget", "assessment", "meaning", "unreviewed_scope", "presentation_limits"):
        if key in value:
            output[key] = value[key]
    for index, declaration in enumerate(value.get("declaration_explanations", [])):
        owner = declaration.get("actual_owner", {})
        source_location = owner.get("location", {})
        indexed_location = (resolve_pointer(value, source_location["location_ref"])
            if isinstance(source_location.get("location_ref"), str) else None)
        output["declaration_explanations"].append({"id": declaration.get("id"), "label": declaration.get("label"),
            "summary": declaration.get("summary"), "actual_owner": {key: owner[key]
                for key in ("file", "symbol", "graph_node_id", "function_kind") if key in owner},
            "source_location": location_summary(source_location),
            "shared_source_location_index_entry": location_summary(indexed_location) if isinstance(indexed_location, dict) else None,
            "statement_count": len(declaration.get("statements", [])),
            "statement_source_gap_count": sum(len(statement.get("source_gaps", [])) for statement in declaration.get("statements", [])),
            "current_report_object_pointer": "/architecture/responsibility_explanations/declaration_explanations/" + str(index)})
    # Communication boundaries are lists of operation references. Keep their
    # real counts plus every scalar/model boundary without duplicating all ops.
    communication = value.get("communication_boundaries", {})
    output["communication_boundaries"] = {key: {"count": len(item),
        "current_report_object_pointer": "/architecture/responsibility_explanations/communication_boundaries/" + key}
        if isinstance(item, list) else item for key, item in communication.items()}
    return output


def report_summary(report: dict) -> dict:
    responsibilities = report.get("architecture", {}).get("responsibility_explanations", {})
    chains = report.get("functional_chains", [])
    comparison = report.get("documentation_comparisons", [])
    return {"report_version": report.get("version"), "report_components": report.get("report_components"),
        "snapshot": report.get("snapshot"),
        "schema_observations": {"report_components_present": isinstance(report.get("report_components"), dict),
            "responsibility_explanations_present": isinstance(report.get("architecture", {}).get("responsibility_explanations"), dict),
            "documentation_comparisons_present": isinstance(report.get("documentation_comparisons"), list),
            "documentation_comparison_count": len(comparison)},
        "current_report_object_fields": {"report_components": "/report_components",
            "responsibility_explanations": "/architecture/responsibility_explanations",
            "documentation_comparisons": "/documentation_comparisons", "source_relation_index": "/source_relation_index",
            "report_scope": "/report_scope"},
        "report_object_pointers_are_not_pointers_into_a_new_saved_full_json": True,
        "large_patterns_and_operation_arrays_not_duplicated_in_this_metadata": True,
        "responsibility_explanations": responsibility_summary(responsibilities),
        "documentation_comparisons": comparison,
        "saved_document_rule_finding_count": sum(chain.get("claim_type") == "document_deployment_consistency" for chain in chains),
        "new_document_results_not_injected_into_saved_v13_findings": True,
        "empty_documentation_comparison_meaning": "Only actual saved findings are used. An old v13 snapshot lacks new v14 document-rule findings; an empty list is retained, not filled with a fabricated result.",
        "judgments": [{"goal_id": judgment.get("goal_id"), "finding_id": judgment.get("finding_id"),
            "evidence_id": judgment.get("evidence_id"), "assessment": judgment.get("assessment"),
            "complete_assessment": judgment.get("complete_assessment"), "full_goal_supported": judgment.get("full_goal_supported"),
            "necessary_gaps": judgment.get("necessary_gaps"),
            "conditions_count": len(judgment.get("conditions", [])), "refutations_count": len(judgment.get("refutations", [])),
            "current_report_object_pointer": "/judgments/" + str(index),
            "saved_evidence_pointer": judgment.get("saved_evidence_pointer")}
            for index, judgment in enumerate(report.get("judgments", []))],
        "functional_chain_count": len(chains),
        "functional_chain_assessment_counts": dict(sorted(Counter(chain.get("assessment", {}).get("state", "unknown") for chain in chains).items())),
        "functional_chains": [{"rule_id": chain.get("rule_id"), "finding_id": chain.get("finding_id"),
            "evidence_id": chain.get("evidence_id"), "claim_type": chain.get("claim_type"),
            "assessment": chain.get("assessment"), "source_scope": chain.get("source_scope"),
            "analysis_gaps": chain.get("analysis_gaps"), "trusted_models": chain.get("trusted_models"),
            "pattern_boundaries": boundary_summary(chain.get("pattern", {}), "/functional_chains/" + str(index) + "/pattern"),
            "source_fact_count": len(chain.get("source_facts", [])),
            "current_report_object_pointer": "/functional_chains/" + str(index),
            "saved_evidence_pointer": chain.get("saved_evidence_pointer")}
            for index, chain in enumerate(chains)],
        "overlapping_source_selections": report.get("overlapping_source_selections"),
        "report_scope": report.get("report_scope"), "graph_observation_counts": report.get("graph_observation_counts"),
        "configured_local_assessment_count": len(report.get("configured_local_assessments", [])),
        "coverage": {key: report.get("coverage", {}).get(key) for key in ("files_selected", "files_parsed", "file_statuses",
            "unparsed_files", "selection_scope", "excluded", "meaning")},
        "runtime_functionality_verified": report.get("runtime_functionality_verified"),
        "target_executed": report.get("target_executed"), "target_tests_run": report.get("target_tests_run"),
        "target_build_run": report.get("target_build_run")}


def read_repository(repository: str, tag: str, loaded_inventory: dict) -> dict:
    # Import only trusted CallScope implementation; never target modules.
    from callscope.store import Store, _snapshot_from_json
    from callscope.project_report import build_project_report, render_markdown

    class ReadOnlySavedStore(Store):
        """Use real inherited reads with an explicitly read-only constructor.

        Ordinary Store.__init__ changes WAL/schema. This constructor only opens
        the actual closed publication with SQLite mode=ro&immutable=1; it does
        not fabricate records or replace Store.get_findings deserialization.
        """
        def __init__(self, database: Path):
            self.path = str(database)
            self._lock = threading.RLock()
            self._connection = sqlite3.connect("file:" + database.as_posix() + "?mode=ro&immutable=1",
                uri=True, timeout=30, isolation_level=None, check_same_thread=False)
            self._connection.row_factory = sqlite3.Row

    database = PREVIOUS / (repository + "-v13.sqlite3")
    integration_path = PREVIOUS / (repository + "-integration.json")
    markdown_path = HERE / (repository + "-" + tag + ".md")
    metadata_path = HERE / (repository + "-" + tag + "-metadata.json")
    if markdown_path.exists() or metadata_path.exists():
        raise FileExistsError("Refuse to overwrite existing development output; use a new --tag")
    before_modules = core_inventory()
    before_database = fingerprint(database)
    metadata = {"kind": "normal_current_report_development_readback", "repository": repository,
        "development_query": True, "not_a_formal_v14_result": True, "saved_snapshot_identity_not_upgraded": True,
        "new_findings_or_fixture_records_injected": False, "normal_build_project_report_called": False,
        "normal_render_markdown_called": False, "saved_store_reads": "inherited Store.get_findings on actual mode=ro&immutable=1 connection",
        "database": str(database), "database_connection_readonly_immutable": True,
        "database_content_sha256_not_recomputed": True, "database_fingerprint_before": before_database,
        "current_module_sha256_before": before_modules,
        "loaded_source_inventory_matches_before": loaded_inventory == before_modules,
        "current_report_source_interpretation_is_development": True,
        "snapshot_findings_detection_recomputed": False,
        "tool_test_suite_run": False, "target_executed": False, "target_imported": False,
        "target_tests_run": False, "target_build_run": False,
        "helper_source_sha256": digest(Path(__file__)), "started_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    start = time.monotonic()
    try:
        integration = json.loads(integration_path.read_text())
        wal = Path(str(database) + "-wal")
        if not integration.get("database_closed") or not integration.get("database_wal_empty_or_absent") or wal.exists() and wal.stat().st_size:
            raise ValueError("v13 publication is not closed/checkpointed")
        metadata["saved_integration_sha256"] = digest(integration_path)
        with ReadOnlySavedStore(database) as store:
            row = store._connection.execute("SELECT snapshot_json,detector_version,schema_version FROM snapshots ORDER BY sequence DESC LIMIT 1").fetchone()
            if row is None:
                raise ValueError("real saved store has no snapshot")
            snapshot = _snapshot_from_json(row["snapshot_json"], row["detector_version"], row["schema_version"])
            del row
            if snapshot.id != integration["snapshot_id"]:
                raise ValueError("saved snapshot differs from closed v13 integration")
            metadata["saved_identity"] = {"snapshot_id": snapshot.id, "source_hash": snapshot.source_hash,
                "policy_hash": snapshot.policy_hash, "analyzer_version": snapshot.analyzer_version,
                "detector_version": snapshot.detector_version, "schema_version": snapshot.schema_version,
                "parser_version": snapshot.parser_version, "component_versions": snapshot.stats.get("component_versions", {})}
            findings = store.get_findings(snapshot.id)
        metadata["actual_saved_finding_count"] = len(findings)
        print("saved_data_loaded", repository, snapshot.id, "findings", len(findings), flush=True)
        report = build_project_report(snapshot, findings)
        metadata["normal_build_project_report_called"] = True
        identity_unchanged = (report["snapshot"]["id"] == snapshot.id and report["snapshot"]["source_hash"] == snapshot.source_hash
            and report["snapshot"]["policy_hash"] == snapshot.policy_hash
            and report["snapshot"]["component_versions"] == snapshot.stats.get("component_versions", {}))
        metadata["saved_identity_and_snapshot_components_unchanged_in_report"] = identity_unchanged
        if not identity_unchanged:
            raise ValueError("normal report builder upgraded or changed saved snapshot identity")
        metadata["shared_reference_validation"] = validate_shared_references(report)
        if not metadata["shared_reference_validation"]["all_explicit_shared_references_resolve_and_match"]:
            raise ValueError("normal responsibility report contains " + str(metadata["shared_reference_validation"]["failure_count"])
                + " invalid scoped shared references; see shared_reference_validation.failures")
        rendered = render_markdown(report)
        metadata["normal_render_markdown_called"] = True
        with markdown_path.open("x", encoding="utf-8") as stream:
            stream.write(rendered)
        metadata["markdown"] = {"file": markdown_path.name, "sha256": digest(markdown_path),
            "utf8_bytes": markdown_path.stat().st_size, "logical_line_count": len(rendered.splitlines()),
            "exact_normal_render_markdown_output_without_injected_banner": True}
        metadata["report_summary"] = report_summary(report)
        metadata["status"] = "normal_saved_data_report_rendered"
        del report, rendered, findings, snapshot
    except Exception as error:
        metadata["status"] = "normal_saved_data_report_exception_preserved"
        metadata["exception"] = {"type": type(error).__name__, "message": str(error), "traceback": traceback.format_exc()}
        print("report_readback_exception", repository, type(error).__name__, str(error), flush=True)
    finally:
        metadata["current_module_sha256_after"] = core_inventory()
        metadata["query_core_bytes_stable"] = before_modules == metadata["current_module_sha256_after"]
        metadata["loaded_source_inventory_matches_after"] = loaded_inventory == metadata["current_module_sha256_after"]
        metadata["database_fingerprint_after"] = fingerprint(database)
        metadata["database_physical_metadata_unchanged"] = before_database == metadata["database_fingerprint_after"]
        metadata["elapsed_seconds"] = round(time.monotonic() - start, 3)
        metadata["finished_at_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        metadata["normal_readback_observation_current_and_stable"] = (metadata.get("status") == "normal_saved_data_report_rendered"
            and metadata["query_core_bytes_stable"] and metadata["loaded_source_inventory_matches_before"]
            and metadata["loaded_source_inventory_matches_after"])
        write_json(metadata_path, metadata)
        gc.collect()
    summary = metadata.get("report_summary", {}).get("responsibility_explanations", {})
    print(json.dumps({"repository": repository, "status": metadata["status"],
        "core_stable": metadata["normal_readback_observation_current_and_stable"],
        "responsibility_operations": summary.get("operation_count"),
        "responsibility_declarations": summary.get("declaration_explanation_count"),
        "analysis_gaps": len(summary.get("analysis_gaps", [])),
        "exception": metadata.get("exception", {}).get("message")}, ensure_ascii=False), flush=True)
    return {"repository": repository, "status": metadata["status"],
        "metadata_file": metadata_path.name, "metadata_sha256": digest(metadata_path),
        "normal_readback_observation_current_and_stable": metadata["normal_readback_observation_current_and_stable"],
        "markdown": metadata.get("markdown"), "exception": metadata.get("exception")}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true", help="Run only after coordinator confirms source-query/core editing coordination")
    parser.add_argument("--tag", default="current-report-development")
    parser.add_argument("--repositories", nargs="+", choices=("codepatchbay", "winwincode"), default=["codepatchbay", "winwincode"])
    args = parser.parse_args()
    if not args.run:
        parser.error("helper prepared only; --run is required after coordinator notification")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", args.tag):
        parser.error("--tag must be a plain lowercase artifact label")
    aggregate_path = HERE / ("PROJECT_REPORT_DEVELOPMENT_QUERY.json" if args.tag == "current-report-development"
        else "PROJECT_REPORT_DEVELOPMENT_QUERY-" + args.tag + ".json")
    if aggregate_path.exists():
        raise FileExistsError("Refuse to overwrite existing development query summary")
    with COMMON_LOCK.open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        loaded_inventory = core_inventory()
        results = []
        for repository in args.repositories:
            try:
                results.append(read_repository(repository, args.tag, loaded_inventory))
            except Exception as error:
                error_path = HERE / (repository + "-" + args.tag + "-startup-error.json")
                failure = {"repository": repository, "status": "development_readback_startup_exception_preserved",
                    "development_query": True, "not_formal_v14_publication": True,
                    "exception": {"type": type(error).__name__, "message": str(error), "traceback": traceback.format_exc()},
                    "current_module_sha256": core_inventory(), "normal_readback_observation_current_and_stable": False}
                write_json(error_path, failure)
                results.append({**{key: failure[key] for key in ("repository", "status", "exception", "normal_readback_observation_current_and_stable")},
                    "metadata_file": error_path.name, "metadata_sha256": digest(error_path)})
                print("report_readback_startup_exception", repository, type(error).__name__, str(error), flush=True)
            gc.collect()
        aggregate = {"kind": "normal_current_report_development_readback_summary", "development_query": True,
            "not_formal_v14_publication": True, "common_lock_acquired_once_internally": True,
            "repositories_processed_sequentially": args.repositories, "results": results,
            "all_normal_reads_current_and_stable": all(item["normal_readback_observation_current_and_stable"] for item in results),
            "new_full_report_json_written": False, "target_executed": False,
            "target_tests_run": False, "target_build_run": False, "tool_test_suite_run": False}
        write_json(aggregate_path, aggregate)
    if any(item["status"] != "normal_saved_data_report_rendered" for item in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
