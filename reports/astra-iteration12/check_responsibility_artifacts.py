"""Read actual development artifacts and authenticate their saved source anchors.

This is an artifact/source readback, not a target execution or a fixture test.
It never loads a database or imports target code.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def walk(value):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", choices=["codepatchbay", "winwincode"])
    args = parser.parse_args()
    artifact_checks = []
    for family, root_key in (("operations", "extraction"), ("explanations", "explanations")):
        path = HERE / f"responsibility-{family}-{args.repository}-development.json"
        raw = path.read_bytes()
        document = json.loads(raw)
        result = document[root_key]
        operations = result["operations"]
        operation_ids = {operation["id"] for operation in operations}
        invalid_operation_content_hashes = []
        for operation in operations:
            content = {key: value for key, value in operation.items() if key != "content_sha256"}
            content_hash = sha256(json.dumps(content, ensure_ascii=True, sort_keys=True,
                separators=(",", ":"), allow_nan=False).encode())
            if content_hash != operation.get("content_sha256"):
                invalid_operation_content_hashes.append(operation["id"])
        locations = result["source_location_index"]
        references = result["evidence_reference_index"]
        unresolved = []
        pointer_counts = Counter()
        relationship_counts = Counter()
        for value in walk(result):
            if not isinstance(value, dict):
                continue
            for key, pool_name, pool in (("location_ref", "source_location_index", locations),
                    ("evidence_ref", "evidence_reference_index", references)):
                pointer = value.get(key)
                if pointer is None:
                    continue
                pointer_counts[key] += 1
                prefix = "/" + pool_name + "/"
                if not isinstance(pointer, str) or not pointer.startswith(prefix) or pointer[len(prefix):] not in pool:
                    unresolved.append({"kind": key, "pointer": pointer})
            if "from_operation_id" in value and "to_operation_id" in value:
                relationship_counts[value.get("kind", "unknown")] += 1
                for key in ("from_operation_id", "to_operation_id"):
                    if value[key] not in operation_ids:
                        unresolved.append({"kind": key, "operation_id": value[key]})
            pointer = value.get("operation_pointer")
            if pointer is not None:
                pointer_counts["operation_pointer"] += 1
                try:
                    prefix, index = pointer.rsplit("/", 1)
                    valid = prefix == "/operations" and 0 <= int(index) < len(operations)
                except (TypeError, ValueError):
                    valid = False
                if not valid:
                    unresolved.append({"kind": "operation_pointer", "pointer": pointer})
        source_cache = {}
        source_anchor_failures = []
        for identity, location in locations.items():
            file = location["file"]
            if file not in source_cache:
                raw_source = (ROOT.parent / args.repository / file).read_bytes()
                source_cache[file] = raw_source
            raw_source = source_cache[file]
            prefix = location.get("raw_prefix_bytes", 0)
            captured_bytes = raw_source[prefix:]
            start, end = location["start_byte"], location["end_byte"]
            checks = {
                "source_hash": sha256(raw_source) == location["source_hash"],
                "span_hash": sha256(captured_bytes[start:end]) == location["span_hash"],
                "valid_span": 0 <= start <= end <= len(captured_bytes),
                "byte_map": location.get("original_file_start_byte", start + prefix) == start + prefix
                    and location.get("original_file_end_byte", end + prefix) == end + prefix,
                "captured_text_coordinate_space": location.get("coordinate_space") == "captured_text_utf8",
            }
            if not all(checks.values()):
                source_anchor_failures.append({"location_id": identity, "file": file, "checks": checks})
        identity_checks = {
            "no_duplicate_operation_ids": len(operation_ids) == len(operations),
            "all_operation_content_hashes_match": not invalid_operation_content_hashes,
            "no_unresolved_pool_or_operation_references": not unresolved,
            "all_source_anchors_match_current_readonly_source": not source_anchor_failures,
            "extractor_module_bytes_stable_during_query": document["query_module_bytes_stable"],
            "extractor_matches_current_module": document["current_module_sha256"] == sha256(
                (ROOT / "callscope/responsibility_operations.py").read_bytes()),
            "target_not_executed": document["target_executed"] is False,
            "target_not_imported": document["target_imported"] is False,
            "target_tests_not_run": document["target_tests_run"] is False,
            "target_build_not_run": document["target_build_run"] is False,
        }
        if family == "explanations":
            identity_checks.update({
                "explanation_module_bytes_stable_during_query": document["explanation_module_bytes_stable"],
                "explanation_matches_current_module": document["explanation_module_sha256"] == sha256(
                    (ROOT / "callscope/architecture_responsibilities.py").read_bytes()),
            })
        artifact_checks.append({"artifact": str(path.relative_to(ROOT)), "artifact_sha256": sha256(raw),
            "artifact_bytes": len(raw), "development_only": document["development_query"],
            "not_formal_v14_result": document["not_formal_v14_result"],
            "snapshot_id": document["saved_snapshot_id"], "current_module_sha256": document["current_module_sha256"],
            "explanation_module_sha256": document.get("explanation_module_sha256"),
            "operations": len(operations), "source_files": len(source_cache), "source_anchors": len(locations),
            "evidence_references": len(references), "pointer_counts": dict(pointer_counts),
            "relationship_reference_occurrences": dict(relationship_counts), "identity_checks": identity_checks,
            "unresolved_references": unresolved, "source_anchor_failures": source_anchor_failures,
            "invalid_operation_content_hashes": invalid_operation_content_hashes,
            "all_checks_passed": all(identity_checks.values())})
        del result, document, operations, raw
    output = {"repository": args.repository, "artifact_checks": artifact_checks,
        "all_checks_passed": all(check["all_checks_passed"] for check in artifact_checks),
        "database_opened": False, "target_executed": False, "target_imported": False,
        "target_tests_run": False, "target_build_run": False}
    (HERE / f"responsibility-{args.repository}-ARTIFACT_READBACK.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(output, ensure_ascii=False))
    if not output["all_checks_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
