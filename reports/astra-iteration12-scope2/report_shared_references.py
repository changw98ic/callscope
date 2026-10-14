"""Validate explicit responsibility-pool references in a real normal report.

This artifact utility does not load databases or construct target data. The
formal publication helper passes its actual in-memory build_project_report
result. Only the new schema's scoped shared-reference fields are resolved.
"""
from collections import Counter
import hashlib
import json
import re

VERSION = "responsibility-shared-reference-structure-1"


def resolve_pointer(document: dict, pointer: str):
    """Resolve only an explicitly declared JSON Pointer; never search strings."""
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise ValueError("explicit reference must be a nonempty JSON Pointer")
    current = document
    for raw_token in pointer[1:].split("/"):
        if re.search(r"~(?![01])", raw_token):
            raise ValueError("invalid JSON Pointer escape")
        token = raw_token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            current = current[token]
        elif isinstance(current, list):
            if not re.fullmatch(r"0|[1-9][0-9]*", token):
                raise ValueError("array reference requires a canonical nonnegative index")
            current = current[int(token)]
        else:
            raise ValueError("reference descends through a scalar")
    return current


def validate_shared_references(report: dict) -> dict:
    """Validate this schema's actual shared refs in the normal memory object.

    Full-pattern/report navigation labels, saved-Evidence pointers and source
    strings are deliberately not interpreted as shared references. No source
    location is rewritten or promoted to a newly verified span by this check.
    """
    root_pointer = "/architecture/responsibility_explanations"
    root = report.get("architecture", {}).get("responsibility_explanations")
    counts = Counter()
    failures = []
    failure_count = 0
    referenced_locations, referenced_evidence, referenced_operations = set(), set(), set()

    def fail(code: str, object_pointer: str, **details):
        nonlocal failure_count
        failure_count += 1
        if len(failures) < 100:
            failures.append({"code": code, "current_report_object_pointer": root_pointer + object_pointer, **details})

    if not isinstance(root, dict):
        fail("responsibility_explanation_object_missing", "")
        root = {}
    root_scope = root.get("source_index_pointer_scope")
    if root_scope != "this_responsibility_explanation_object":
        fail("shared_source_index_scope_missing_or_unsupported", "", actual_scope=root_scope)
    indices = {}
    for name in ("source_location_index", "evidence_reference_index"):
        index = root.get(name)
        if not isinstance(index, dict):
            fail("shared_index_missing_or_not_an_object", "/" + name)
            index = {}
        indices[name] = index
        for key, entry in index.items():
            if not isinstance(entry, dict):
                fail("shared_index_entry_not_an_object", "/" + name + "/" + str(key))
    operations = root.get("operations")
    if not isinstance(operations, list):
        fail("operations_missing_or_not_an_array", "/operations")
        operations = []

    def target(reference: object, prefix: str, object_pointer: str):
        if (not isinstance(reference, str) or not reference.startswith(prefix)
                or not reference[len(prefix):] or "/" in reference[len(prefix):]):
            fail("shared_reference_has_wrong_index_domain", object_pointer,
                reference=reference, expected_prefix=prefix)
            return None
        try:
            result = resolve_pointer(root, reference)
        except (KeyError, IndexError, TypeError, ValueError) as error:
            fail("shared_reference_does_not_resolve", object_pointer, reference=reference,
                reason=type(error).__name__ + ": " + str(error))
            return None
        if not isinstance(result, dict):
            fail("shared_reference_target_not_an_object", object_pointer, reference=reference)
            return None
        return result

    def walk(value, pointer: str):
        if isinstance(value, dict):
            for field, prefix, aliases, referenced in (
                ("location_ref", "/source_location_index/", ("file", "line", "column", "start_byte", "end_byte", "source_hash"), referenced_locations),
                ("evidence_ref", "/evidence_reference_index/", ("rule_id", "goal_id", "reference_role"), referenced_evidence),
            ):
                if field not in value:
                    continue
                counts[field] += 1
                scope = value.get("pointer_scope", root_scope)
                if scope not in {"this_responsibility_explanation_object", "this_responsibility_extraction_or_explanation_object"}:
                    fail("shared_reference_scope_missing_or_unsupported", pointer + "/" + field,
                        reference=value[field], actual_scope=scope)
                    continue
                resolved = target(value[field], prefix, pointer + "/" + field)
                if resolved is None:
                    continue
                referenced.add(value[field])
                for key in aliases:
                    if key in value and (key not in resolved or value[key] != resolved[key]):
                        fail("shared_reference_alias_disagrees_with_target", pointer + "/" + field,
                            reference=value[field], field=key, reference_value=value[key], target_value=resolved.get(key))
                if field == "location_ref":
                    for key in ("file", "source_hash", "start_byte", "end_byte", "span_hash"):
                        if key not in resolved:
                            fail("shared_source_anchor_field_missing", pointer + "/" + field,
                                reference=value[field], field=key)
            if "operation_pointer" in value:
                counts["operation_pointer"] += 1
                if value.get("operation_pointer_scope") != "this_responsibility_explanation_object":
                    fail("operation_reference_scope_missing_or_unsupported", pointer + "/operation_pointer",
                        reference=value["operation_pointer"], actual_scope=value.get("operation_pointer_scope"))
                else:
                    resolved = target(value["operation_pointer"], "/operations/", pointer + "/operation_pointer")
                    if resolved is not None:
                        referenced_operations.add(value["operation_pointer"])
                        if value.get("operation_id") != resolved.get("id"):
                            fail("operation_reference_id_disagrees_with_target", pointer + "/operation_pointer",
                                reference=value["operation_pointer"], operation_id=value.get("operation_id"), target_id=resolved.get("id"))
                        for field, operation_field in (("source_evidence_refs_pointer", "source_evidence_refs"),
                                                       ("source_locations_pointer", "source_locations")):
                            if field not in value:
                                continue
                            counts[field] += 1
                            ref = value[field]
                            if ref != value["operation_pointer"] + "/" + operation_field:
                                fail("operation_child_reference_wrong_domain", pointer + "/" + field, reference=ref)
                                continue
                            try:
                                child = resolve_pointer(root, ref)
                            except (KeyError, IndexError, TypeError, ValueError) as error:
                                fail("operation_child_reference_does_not_resolve", pointer + "/" + field,
                                    reference=ref, reason=type(error).__name__ + ": " + str(error))
                                continue
                            if not isinstance(child, list) or child is not resolved.get(operation_field):
                                fail("operation_child_reference_target_not_the_actual_operation_array", pointer + "/" + field, reference=ref)
            elif "source_evidence_refs_pointer" in value or "source_locations_pointer" in value:
                fail("operation_child_reference_has_no_scoped_operation_parent", pointer)
            for key, child in value.items():
                token = str(key).replace("~", "~0").replace("/", "~1")
                walk(child, pointer + "/" + token)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, pointer + "/" + str(index))

    walk(root, "")
    return {"validator_version": VERSION, "check": "actual_in_memory_responsibility_shared_reference_structure",
        "current_report_object_pointer": root_pointer, "source_index_pointer_scope": root_scope,
        "reference_counts": dict(sorted(counts.items())), "source_location_index_count": len(indices["source_location_index"]),
        "evidence_reference_index_count": len(indices["evidence_reference_index"]), "operation_count": len(operations),
        "distinct_referenced_location_count": len(referenced_locations),
        "distinct_referenced_evidence_count": len(referenced_evidence),
        "distinct_referenced_operation_count": len(referenced_operations),
        "index_canonical_json_sha256": {name: hashlib.sha256(json.dumps(index, ensure_ascii=False,
            sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest() for name, index in indices.items()},
        "source_location_coordinate_space_counts": dict(sorted(Counter(str(item.get("coordinate_space", "unspecified"))
            for item in indices["source_location_index"].values() if isinstance(item, dict)).items())),
        "failure_count": failure_count, "failures": failures, "failure_details_truncated": failure_count > len(failures),
        "all_explicit_shared_references_resolve_and_match": failure_count == 0,
        "full_pattern_labels_and_arbitrary_strings_treated_as_references": False,
        "source_locations_or_utf8_spans_modified": False, "source_span_bytes_revalidated_by_this_structure_check": False,
        "canonical_source_anchor_fields_required_on_each_referenced_location": ["file", "source_hash", "start_byte", "end_byte", "span_hash"],
        "model_or_runtime_guarantees_inferred_from_reference_resolution": False}

