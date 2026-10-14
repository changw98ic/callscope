"""Extend preserved policies with source locators and declared finite models.

Neither reference-report conclusions nor their proposed source paths become
detector output. Old policies and reports remain untouched.
"""
import hashlib
import json
from pathlib import Path


def main():
    directory=Path(__file__).resolve().parent
    groups={"codepatchbay":(("pipeline","CPB-01"),("status","CPB-02"),("atomicity","CPB-03")),
            "winwincode":(("navigation","WWC-01"),("device","WWC-02"))}
    changes=[]
    for repository,adapters in groups.items():
        original=directory/f"{repository}-base-policy.json"
        policy=json.loads(original.read_text())
        base=json.loads(original.read_text())
        inputs=policy["analysis"].get("support_inputs",[])
        project_inputs=["README.md","package.json"] if repository=="codepatchbay" else ["README.md","docs/architecture.md"]
        policy["analysis"]["support_inputs"]=list(dict.fromkeys([*inputs,*project_inputs]))
        policy["goal_contracts"]=[]
        for analyzer,goal_id in adapters:
            contract=json.loads((directory/f"{analyzer}-rule.json").read_text())
            policy["goal_contracts"].append({"id":contract["id"],"goal_id":goal_id,"analyzer":analyzer,"contract":contract})
        if repository=="winwincode":
            extras=["crates/winwincode-api/Cargo.toml","crates/winwincode-api/src/generated.rs","apps/client/src/generated/contracts.ts",
                    "crates/winwincode-domain/Cargo.toml","crates/winwincode-domain/src/generated.rs"]
            analysis=policy["analysis"]
            analysis["support_inputs"]=list(dict.fromkeys([*analysis["support_inputs"],*extras]))
            profile={"id":"serde-1.0.228-declared-helper-v1","crate_root":"crates/winwincode-api","workspace_manifest":"Cargo.toml"}
            if not any(item["crate_root"]==profile["crate_root"] for item in analysis["rust_helper_profiles"]):
                analysis["rust_helper_profiles"].append(profile)
        report_rules=directory/"report-claims-rule.json"
        if report_rules.exists():
            selected=json.loads(report_rules.read_text()).get(repository,[])
            if selected:
                policy["report_claims"]=selected
        for section in ("rules","static_contracts","value_contracts","field_contracts","navigation_contracts","atomicity_contracts","budget_contracts"):
            if policy.get(section)!=base.get(section):
                raise RuntimeError(f"An existing source-observation contract was altered: {repository}/{section}")
        output=directory/f"{repository}-policy.json"
        output.write_text(json.dumps(policy,ensure_ascii=False,indent=2)+"\n")
        changes.append({"repository":repository,"preserved_base_policy_sha256":hashlib.sha256(original.read_bytes()).hexdigest(),
            "new_policy_sha256":hashlib.sha256(output.read_bytes()).hexdigest(),"changed_sections":[key for key in sorted(set(base)|set(policy)) if base.get(key)!=policy.get(key)],
            "goal_ids":[item["goal_id"] for item in policy["goal_contracts"]],"comparison":"New explicitly declared conditional models and analyzers; not a same-policy precision experiment."})
    (directory/"POLICY_EXTENSION.json").write_text(json.dumps(changes,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(changes,ensure_ascii=False))


if __name__=="__main__":
    main()
