"""Authenticate saved source, policy and implementation identities.

The original project reports are the benchmark. This is artifact bookkeeping,
not another model review or an approval stage.
"""
import hashlib
import json
from pathlib import Path
from callscope.analysis_inputs import tool_identity

BASELINE_SHA256 = "16b4b05c8818fa1eecf396132ebe2ea29a8f0068801165f0649da379d9041dd7"
GOAL_ACCEPTANCE_SHA256 = "9b6f4fda6aa24f055e288690e76405779e36758f8ba986799f78f2f96aa8d118"
GOAL_TEMPLATE_SHA256 = "d33f48b4f0908458b587e3ad4a97d3b40eb46e3b7eb291d04d053155a5c6ad04"


def digest_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def check_contracts(directory):
    for relative,expected in (("astra-baseline/capability-baseline.json",BASELINE_SHA256),
            ("astra-iteration4/GOAL_ACCEPTANCE.md",GOAL_ACCEPTANCE_SHA256),
            ("astra-iteration4/goal-ledger.template.json",GOAL_TEMPLATE_SHA256)):
        if digest_file(directory.parent/relative)!=expected:
            raise RuntimeError(f"Frozen original tracking contract changed: {relative}")


def check_identity(directory):
    check_contracts(directory)
    freeze=json.loads((directory/"CORE_FREEZE.json").read_text())
    if tool_identity()!=freeze["tool_identity"]:
        raise RuntimeError("Implementation changed after the recorded source freeze")
    for relative,expected in freeze["benchmark_reports"].items():
        if digest_file(directory.parent/relative)!=expected:
            raise RuntimeError(f"Original benchmark report changed: {relative}")
    for relative,expected in freeze["policy_files"].items():
        if digest_file(directory/relative)!=expected:
            raise RuntimeError(f"Declared new policy changed after freeze: {relative}")
    return freeze


def check_snapshot(directory,snapshot):
    freeze=check_identity(directory)
    if snapshot.stats["component_versions"]["tool"]!=freeze["tool_identity"]:
        raise RuntimeError("Saved snapshot uses a different implementation")
    for key in ("analyzer_version","detector_version","schema_version"):
        if getattr(snapshot,key)!=freeze[key]:
            raise RuntimeError(f"Saved snapshot uses a different {key}")
    return freeze


def write_json(path,value):
    temporary=path.with_suffix(path.suffix+".tmp")
    temporary.write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    temporary.replace(path)
