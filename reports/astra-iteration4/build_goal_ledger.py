"""Create an unassessed five-goal ledger from the frozen acceptance template.

This report helper reads only JSON artifacts and the acceptance Markdown in
CallScope's reports directory. It does not import CallScope or target modules,
read target workspaces, run analyzers, execute code, or infer satisfied goals.
Registered artifacts remain unclassified references: findings, selectors, and
manual AST anchors are not automatically promoted to obligation witnesses.

Usage from the CallScope root:
    python reports/astra-iteration4/build_goal_ledger.py \
        --output reports/astra-iteration4/goal-ledger.json \
        --artifact reports/astra-iteration4/codepatchbay-summary.json

Use after saved artifacts exist. Every assessment remains pending. A later
evaluation must fill evidence and gaps explicitly and recompute the goal
assessment under GOAL_ACCEPTANCE.md. Existing ledgers are never overwritten.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Any


VERSION = "goal-ledger-builder-1"
DIRECTORY = Path(__file__).resolve().parent
REPORTS_ROOT = DIRECTORY.parent
MAX_JSON_BYTES = 16 * 1024 * 1024
GOAL_OBLIGATIONS = {
    "CPB-01": tuple(f"P{i}" for i in range(1, 7)),
    "CPB-02": tuple(f"S{i}" for i in range(1, 6)),
    "CPB-03": tuple(f"A{i}" for i in range(1, 8)),
    "WWC-01": tuple(f"N{i}" for i in range(1, 8)),
    "WWC-02": tuple(f"D{i}" for i in range(1, 6)),
}


def _reject_nonfinite(value: str) -> None:
    raise ValueError(f"Non-finite JSON number is not allowed: {value}")


def _read_report_json(path: Path) -> tuple[Any, bytes, Path]:
    resolved = path.resolve(strict=True)
    if not resolved.is_relative_to(REPORTS_ROOT) or resolved.suffix != ".json":
        raise ValueError("Only saved JSON files inside CallScope/reports are accepted.")
    if resolved.stat().st_size > MAX_JSON_BYTES:
        raise ValueError("Saved JSON exceeds the 16 MiB report-helper limit.")
    raw = resolved.read_bytes()
    if len(raw) > MAX_JSON_BYTES:
        raise ValueError("Saved JSON changed beyond the report-helper size limit.")
    return json.loads(raw, parse_constant=_reject_nonfinite), raw, resolved


def _validate_template(template: Any) -> None:
    if not isinstance(template, dict) or type(template.get("schema_version")) is not int or template.get("schema_version") != 1:
        raise ValueError("Expected a schema-1 goal acceptance template.")
    if template.get("kind") != "full_static_goal_acceptance_ledger":
        raise ValueError("Unexpected goal ledger kind.")
    goals = template.get("goals")
    if (not isinstance(goals, list) or len(goals) != len(GOAL_OBLIGATIONS)
            or not all(isinstance(goal, dict) for goal in goals)
            or [goal.get("id") for goal in goals] != list(GOAL_OBLIGATIONS)):
        raise ValueError("All five fixed claims must be present in their original order.")
    all_ids = []
    for goal in goals:
        expected = [f"{goal['id']}.{suffix}" for suffix in GOAL_OBLIGATIONS[goal["id"]]]
        obligations = goal.get("obligations")
        if (not isinstance(obligations, list) or len(obligations) != len(expected)
                or not all(isinstance(item, dict) for item in obligations)
                or [item.get("id") for item in obligations] != expected):
            raise ValueError(f"Missing or changed required obligations for {goal['id']}.")
        if not isinstance(goal.get("claim"), dict) or goal["claim"].get("source_claim_id") != goal["id"]:
            raise ValueError("Each goal must retain its independent-review claim reference.")
        for item in [goal, *obligations]:
            if not isinstance(item.get("assessment"), dict) or item["assessment"].get("status") != "pending":
                raise ValueError("This initializer accepts pending templates only; no pass state may be prefilled.")
            for key in ("source", "model", "policy", "gaps", "witness"):
                if not isinstance(item.get(key), list):
                    raise ValueError(f"{item['id']} requires a {key} list.")
            if any(item[key] for key in ("source", "model", "policy", "witness")):
                raise ValueError("An initial template cannot prefill inferred evidence.")
        if any(item.get("required") is not True for item in obligations):
            raise ValueError("No required obligation can be removed from acceptance.")
        if goal["assessment"].get("unclosed_required_obligations") != expected:
            raise ValueError("Pending goal assessment must retain all required obligations as unclosed.")
        all_ids.extend(expected)
    if template.get("goal_count") != 5 or template.get("required_obligation_count") != len(all_ids):
        raise ValueError("Goal/obligation counts do not match the complete contract.")
    assessment = template.get("assessment")
    if not isinstance(assessment, dict) or assessment.get("status") != "pending" or assessment.get("unclosed_required_obligations") != all_ids:
        raise ValueError("The overall template must remain pending with all required obligations.")
    if (assessment.get("goal_status_counts") != {"pending": len(goals)}
            or assessment.get("obligation_status_counts") != {"pending": len(all_ids)}):
        raise ValueError("Initial assessment counts must retain all goals and obligations as pending.")
    contract = template.get("acceptance_contract")
    if not isinstance(contract, dict) or contract.get("path") != "GOAL_ACCEPTANCE.md":
        raise ValueError("The initializer requires the adjacent acceptance contract.")
    actual_hash = hashlib.sha256((DIRECTORY / "GOAL_ACCEPTANCE.md").read_bytes()).hexdigest()
    if contract.get("sha256") != actual_hash:
        raise ValueError("Acceptance contract identity changed; do not silently reuse the old template.")


def build_pending_ledger(template_path: Path, artifact_paths: list[Path]) -> dict[str, Any]:
    template, raw_template, template_file = _read_report_json(template_path)
    _validate_template(template)
    ledger = deepcopy(template)
    inventory = []
    seen: set[Path] = set()
    for requested in artifact_paths:
        artifact, raw, path = _read_report_json(requested)
        if not isinstance(artifact, (dict, list)):
            raise ValueError("A registered artifact must be a JSON object or array.")
        if path in seen:
            raise ValueError("Duplicate saved-artifact path; it does not create additional evidence.")
        seen.add(path)
        inventory.append({
            "path": str(path.relative_to(DIRECTORY)) if path.is_relative_to(DIRECTORY) else str(path.relative_to(REPORTS_ROOT)),
            "path_base": "iteration_directory" if path.is_relative_to(DIRECTORY) else "callscope_reports",
            "sha256": hashlib.sha256(raw).hexdigest(),
            "size_bytes": len(raw), "classification": "unclassified_saved_json",
            "used_to_close_obligations": False,
            "interpretation": "Registered saved input only; no automatic or manual origin is inferred.",
        })
    ledger["evaluation"] = {
        "state": "pending", "snapshots": [], "implementation": None,
        "artifact_inventory": inventory,
        "reason": "Artifacts registered without evaluation; all necessary obligations remain pending.",
    }
    ledger["report_builder"] = {
        "version": VERSION,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "template_path": str(template_file.relative_to(REPORTS_ROOT)),
        "template_sha256": hashlib.sha256(raw_template).hexdigest(),
        "automatic_assessment_performed": False,
        "target_workspace_read": False, "target_code_imported_or_executed": False,
    }
    return ledger


def _write_new_ledger(path: Path, ledger: dict[str, Any]) -> None:
    output = path.resolve()
    if output.parent != DIRECTORY or output.suffix != ".json" or output.name == "goal-ledger.template.json":
        raise ValueError("Write a new JSON ledger in this iteration directory; do not overwrite its template.")
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=DIRECTORY,
                                         prefix=".goal-ledger-", suffix=".tmp", delete=False) as handle:
            temporary = handle.name
            json.dump(ledger, handle, ensure_ascii=False, indent=2, allow_nan=False)
            handle.write("\n")
        # Link only after complete writing, atomically refusing an existing output.
        os.link(temporary, output)
    finally:
        if temporary is not None:
            Path(temporary).unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", type=Path, default=DIRECTORY / "goal-ledger.template.json")
    parser.add_argument("--artifact", type=Path, action="append", default=[],
                        help="Register an existing saved JSON artifact; no assessment is inferred.")
    parser.add_argument("--output", type=Path, required=True,
                        help="New JSON ledger in this iteration directory; existing files are refused.")
    args = parser.parse_args()
    try:
        ledger = build_pending_ledger(args.template, args.artifact)
        _write_new_ledger(args.output, ledger)
    except (OSError, ValueError, RecursionError) as exc:
        parser.error(str(exc))
    print(json.dumps({"output": str(args.output), "goal_count": ledger["goal_count"],
                      "required_obligation_count": ledger["required_obligation_count"],
                      "assessment": "pending", "registered_artifacts": len(ledger["evaluation"]["artifact_inventory"]),
                      "automatic_assessment_performed": False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
