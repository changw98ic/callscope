"""Add real source-locator relation queries without altering frozen history."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXTENSIONS = {
    "codepatchbay": ("gates-rules.json", "records-rules.json", "ownership-codepatchbay-rules.json"),
    "winwincode": ("workrun-rule.json", "messages-rules.json", "lifecycle-rules.json", "ownership-winwincode-rules.json"),
}


def main():
    from callscope.config import load_config
    from callscope.report_chain_analysis import validate_report_claim

    changes = []
    for repository, names in EXTENSIONS.items():
        original = HERE.parent / "astra-iteration10" / (repository + "-policy.json")
        policy = json.loads(original.read_text())
        preserved = json.loads(original.read_text())
        existing = list(policy.get("report_claims", []))
        added = []
        for name in names:
            value = json.loads((HERE / name).read_text())
            rules = value if isinstance(value, list) else [value]
            for rule in rules:
                validate_report_claim(rule)
                added.append(rule)
        policy["report_claims"] = [*existing, *added]
        identifiers = [rule["id"] for rule in policy["report_claims"]]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("Duplicate source relationship rule ID: " + repository)
        if any(policy.get(key) != value for key, value in preserved.items() if key != "report_claims"):
            raise ValueError("A preserved source observation configuration changed")
        output = HERE / (repository + "-policy.json")
        if (HERE / "CORE_FREEZE.json").exists():
            raise ValueError("Frozen policies cannot be reassembled")
        output.write_text(json.dumps(policy, ensure_ascii=False, indent=2) + "\n")
        normalized = load_config(HERE.parents[2] / repository, output)
        changes.append({"repository": repository,
            "previous_policy_sha256": hashlib.sha256(original.read_bytes()).hexdigest(),
            "policy_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
            "preserved_report_claims": len(existing), "added_rule_ids": [rule["id"] for rule in added],
            "normalized_report_claims": len(normalized["report_claims"]),
            "changed_sections": ["report_claims"], "target_source_edited": False,
            "comparison": "Same configured source capture; additional conditional relation models and full publication engine."})
    (HERE / "POLICY_EXTENSION.json").write_text(json.dumps(changes, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(changes, ensure_ascii=False))


if __name__ == "__main__":
    main()
