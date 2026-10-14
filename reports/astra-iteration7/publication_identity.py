"""Publication guards for the reviewed CallScope implementation and policy."""
import hashlib
import json
from pathlib import Path
from callscope.analysis_inputs import tool_identity


BASELINE_SHA256 = "16b4b05c8818fa1eecf396132ebe2ea29a8f0068801165f0649da379d9041dd7"


def check_identity(directory):
    freeze = json.loads((directory / "CORE_FREEZE.json").read_text())
    if tool_identity() != freeze["tool_identity"]:
        raise RuntimeError("Current CallScope implementation differs from the reviewed core freeze")
    baseline = directory.parent / "astra-baseline" / "capability-baseline.json"
    if hashlib.sha256(baseline.read_bytes()).hexdigest() != BASELINE_SHA256:
        raise RuntimeError("Original frozen 26-observation baseline bytes changed")
    for name in ("codepatchbay", "winwincode"):
        original = directory.parent / "astra-iteration6" / f"{name}-policy.json"
        policy = directory / f"{name}-policy.json"
        if policy.read_bytes() != original.read_bytes():
            raise RuntimeError(f"{name}: v10 policy differs from frozen v9 policy bytes")
    return freeze


def check_snapshot(directory, snapshot):
    freeze = check_identity(directory)
    if snapshot.stats["component_versions"]["tool"] != freeze["tool_identity"]:
        raise RuntimeError("Saved publication does not use the reviewed implementation")


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
