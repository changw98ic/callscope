"""Publication guards for the reviewed CallScope implementation and policy."""
import hashlib
import json
from callscope.analysis_inputs import tool_identity


BASELINE_SHA256 = "16b4b05c8818fa1eecf396132ebe2ea29a8f0068801165f0649da379d9041dd7"
GOAL_ACCEPTANCE_SHA256 = "9b6f4fda6aa24f055e288690e76405779e36758f8ba986799f78f2f96aa8d118"
GOAL_TEMPLATE_SHA256 = "d33f48b4f0908458b587e3ad4a97d3b40eb46e3b7eb291d04d053155a5c6ad04"


def check_contracts(directory):
    """Authenticate the unchanged observation and full-goal denominators."""
    paths = (
        (directory.parent / "astra-baseline" / "capability-baseline.json", BASELINE_SHA256),
        (directory.parent / "astra-iteration4" / "GOAL_ACCEPTANCE.md", GOAL_ACCEPTANCE_SHA256),
        (directory.parent / "astra-iteration4" / "goal-ledger.template.json", GOAL_TEMPLATE_SHA256),
    )
    for path, expected in paths:
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise RuntimeError(f"Original frozen acceptance bytes changed: {path.name}")
    for name in ("codepatchbay", "winwincode"):
        original = directory.parent / "astra-iteration6" / f"{name}-policy.json"
        previous = directory.parent / "astra-iteration8" / f"{name}-policy.json"
        if previous.read_bytes() != original.read_bytes():
            raise RuntimeError(f"{name}: final v10 policy is not the frozen v9 policy")


def check_identity(directory):
    check_contracts(directory)
    freeze = json.loads((directory / "CORE_FREEZE.json").read_text())
    if tool_identity() != freeze["tool_identity"]:
        raise RuntimeError("Current CallScope implementation differs from the reviewed core freeze")
    for name in ("codepatchbay", "winwincode"):
        original = directory.parent / "astra-iteration6" / f"{name}-policy.json"
        policy = directory / f"{name}-policy.json"
        if policy.read_bytes() != original.read_bytes():
            raise RuntimeError(f"{name}: v11 policy differs from frozen v9/final v10 policy bytes")
    return freeze


def check_snapshot(directory, snapshot):
    freeze = check_identity(directory)
    if snapshot.stats["component_versions"]["tool"] != freeze["tool_identity"]:
        raise RuntimeError("Saved publication does not use the reviewed implementation")
    for key in ("analyzer_version", "detector_version", "schema_version"):
        if getattr(snapshot, key) != freeze[key]:
            raise RuntimeError(f"Saved publication differs from reviewed {key}")


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
