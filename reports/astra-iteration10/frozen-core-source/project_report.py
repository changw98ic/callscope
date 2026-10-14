"""Generate a project report from captured graph and analysis evidence.

Reference reports are benchmarks, never a source of generated findings. A
directory inventory or a resolved path is not labeled functional coverage.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict
import hashlib
import json
from pathlib import PurePosixPath
import tomllib
from typing import Any

from .models import Finding, GraphSnapshot

VERSION = "captured-project-analysis-report-1"


def _judgment_summary(judgment: dict) -> str:
    if not judgment.get("complete_assessment"):
        return "所选判断尚有必要分析缺口，局部源码事实不替代完整结论。"
    if not judgment.get("full_goal_supported"):
        return "自动证据要求反驳或收窄原判断；具体范围见保存推导与反证。"
    kind=judgment.get("analysis_type")
    if kind=="status":
        result=judgment.get("derived_judgment",{})
        if isinstance(result,dict) and result.get("classification_differs") is True:
            return f"状态 `{result.get('status')}` 在所选身份条件下的终态谓词结果为 `{result.get('valid_identity_predicate_result')}`，权威终态集合成员关系为 `{result.get('authority_terminal_membership')}`；消费者据此进入拒绝分支。恢复政策和权威写入保护分别保存。"
    descriptions={
        "pipeline":"提交选项与所读执行预算之间存在接线差异；参数构造、消息关系、消费者及不同重试预算分别得到源码证据，适用分支和不透明消费者保留。",
        "navigation":"所选公开导航未提供消费者必需的查询上下文；经真实生产装配与缺值传播，创建在提交命令前被拒绝。有效上下文和替代创建入口是反证。",
        "device":"所选提交对象遗漏条件分支必填字段；经过生成协议、普通 JSON 与 Serde 映射后，权威非空守卫在使用或提交前拒绝。其它分支和显式字段来源是反证。",
        "atomicity":"预查与权威写入的去重口径不同；从实际保护区和状态转换生成的有限交错可产生重复非终态记录，同时保存可以复用的顺序和失败条件。",
    }
    return descriptions.get(kind,"所选判断在已保存源码和注册模型的明确条件内成立；边界与反证见下方证据。")


def _project_declarations(snapshot: GraphSnapshot) -> dict:
    """Summarize authenticated inert manifests; never resolve or run scripts."""
    manifests=[]
    documentation=[]
    gaps=[]
    for path,record in sorted(snapshot.input_evidence.items()):
        selected=path=="package.json" or path=="README.md" or path=="docs/architecture.md" or path.endswith("Cargo.toml")
        if not selected:
            continue
        text=record.get("content","")
        if (record.get("status")!="captured" or not isinstance(text,str)
                or hashlib.sha256(text.encode("utf-8")).hexdigest()!=record.get("text_hash")):
            gaps.append({"file":path,"reason":"Project declaration input is not authenticated captured text"})
            continue
        identity={"file":path,"source_file_sha256":record["hash"],"text_sha256":record["text_hash"],
            "origin":"captured-project-declaration","snapshot_id":snapshot.id}
        try:
            if path=="package.json":
                data=json.loads(text)
                if not isinstance(data,dict):
                    raise ValueError("Package manifest is not an object")
                manifests.append({**identity,"format":"json","declarations":{key:data.get(key)
                    for key in ("name","version","description","license","type","bin","engines")},
                    "declared_script_names":sorted(data.get("scripts",{})) if isinstance(data.get("scripts",{}),dict) else [],
                    "declared_dependencies":data.get("dependencies",{}),"dependency_availability_verified":False})
            elif path.endswith("Cargo.toml"):
                data=tomllib.loads(text)
                workspace=data.get("workspace",{})
                manifests.append({**identity,"format":"toml","package_declarations":data.get("package",{}),
                    "workspace_members":workspace.get("members",[]) if isinstance(workspace,dict) else [],
                    "workspace_exclusions":workspace.get("exclude",[]) if isinstance(workspace,dict) else [],
                    "workspace_package":workspace.get("package",{}) if isinstance(workspace,dict) else {},
                    "declared_dependencies":data.get("dependencies",{}),"dependency_availability_verified":False})
            else:
                headings=[{"line":number,"text":line} for number,line in enumerate(text.splitlines(),1)
                    if line.startswith("# ") or line.startswith("## ")]
                documentation.append({**identity,"headings":headings,"content_is_instructions_for_analyzer":False,
                    "product_statements_independently_proven":False})
        except (ValueError,TypeError) as error:
            gaps.append({**identity,"reason":str(error)})
    return {"manifests":manifests,"documentation":documentation,"gaps":gaps,
        "meaning":"Captured declarations and headings describe project inputs, not verified products, installed dependencies or executed commands."}


def build_project_report(snapshot: GraphSnapshot, findings: list[Finding]) -> dict[str, Any]:
    by_id = defaultdict(list)
    for node in snapshot.nodes:
        by_id[node.id].append(node)
    areas: dict[str, dict] = {}

    def area(path: str) -> str:
        parent = PurePosixPath(path).parent.parts
        return "/".join(parent[:2]) if parent else "."

    for source in snapshot.files:
        key = area(source.path)
        entry = areas.setdefault(key,{"directory":key,"files":0,"parsed":0,"languages":Counter(),"node_types":Counter()})
        entry["files"]+=1
        entry["parsed"]+=source.status=="parsed"
        entry["languages"][source.language]+=1
    for node in snapshot.nodes:
        if node.file:
            key=area(node.file)
            if key in areas:
                areas[key]["node_types"][node.kind]+=1
    dependencies=defaultdict(lambda:{"edge_count":0,"examples":[]})
    for edge in snapshot.edges:
        left,right=by_id.get(edge.source,[]),by_id.get(edge.target,[])
        if edge.resolution!="resolved" or len(left)!=1 or len(right)!=1 or not left[0].file or not right[0].file:
            continue
        pair=(area(left[0].file),area(right[0].file))
        if pair[0]==pair[1]:
            continue
        entry=dependencies[pair]
        entry["edge_count"]+=1
        if len(entry["examples"])<3:
            entry["examples"].append({"edge_id":edge.id,"file":edge.file,"line":edge.line,
                "column":edge.column,"source":edge.source,"target":edge.target,"type":"captured_graph_call"})
    goals=[]
    functional_chains=[]
    constraints=[]
    graph_observations=Counter()
    for finding in findings:
        if finding.type=="static_goal_judgment":
            for evidence in finding.evidence:
                if evidence.kind!="static_whole_judgment":
                    continue
                details=evidence.details
                goals.append({"goal_id":details.get("goal_id"),"finding_id":finding.id,"evidence_id":evidence.id,
                    "analysis_type":details.get("analyzer"),"assessment":details.get("assessment"),
                    "complete_assessment":details.get("complete_assessment",False),
                    "full_goal_supported":details.get("full_goal_supported",False),
                    "derived_judgment":details.get("derived_judgment"),"conditions":details.get("conditions",[]),
                    "refutations":details.get("refutations",[]),"obligations":details.get("obligations",[]),
                    "necessary_gaps":details.get("necessary_gaps",[]),
                    "adapter_judgments":details.get("adapter_judgments",[]),
                    "saved_evidence_pointer":"/evidence/"+str(finding.evidence.index(evidence))+"/details"})
        elif finding.type=="static_report_claim":
            for index,evidence in enumerate(finding.evidence):
                if evidence.kind!="static_report_chain_analysis":
                    continue
                details=evidence.details
                functional_chains.append({"rule_id":finding.rule_id,"finding_id":finding.id,"evidence_id":evidence.id,
                    "claim_type":details.get("claim_type",finding.metadata.get("claim_type")),
                    "assessment":details.get("assessment",{}),"pattern":details.get("pattern",{}),
                    "source_facts":details.get("source_facts",[]),"source_scope":details.get("scope",{}),
                    "analysis_gaps":details.get("analysis_gaps",[]),"trusted_models":details.get("trusted_models",[]),
                    "policy_declarations":details.get("policy_declarations",{}),
                    "saved_evidence_pointer":f"/evidence/{index}/details"})
        elif finding.rule_id:
            constraints.append({"finding_id":finding.id,"rule_id":finding.rule_id,"type":finding.type,
                "status":finding.status,"title":finding.title,"metadata":finding.metadata,
                "evidence_ids":[item.id for item in finding.evidence]})
        else:
            graph_observations[(finding.type,finding.status)]+=1
    goals.sort(key=lambda item:str(item["goal_id"]))
    for judgment in goals:
        judgment["summary"]=_judgment_summary(judgment)
    functional_chains.sort(key=lambda item:str(item["rule_id"]))
    source_selections=defaultdict(list)
    for chain in functional_chains:
        selection=(chain["claim_type"],tuple(sorted((source.get("file"),source.get("symbol"))
            for source in chain["source_scope"].get("selected_definitions",[]))))
        source_selections[selection].append(chain["rule_id"])
    overlaps=[{"claim_type":kind,"selected_definitions":[{"file":file,"symbol":symbol} for file,symbol in sources],
        "rule_ids":rules,"meaning":"Same source selected by multiple rules; not additional functional coverage."}
        for (kind,sources),rules in source_selections.items() if len(rules)>1 and sources]
    support=[{key:value for key,value in record.items() if key not in {"content"}}
             for _,record in sorted(snapshot.input_evidence.items())]
    return {"version":VERSION,"snapshot":{"id":snapshot.id,"project_id":snapshot.project_id,
        "project_name":snapshot.project_name,"created_at":snapshot.created_at,"source_hash":snapshot.source_hash,
        "policy_hash":snapshot.policy_hash,"status":snapshot.status,"component_versions":snapshot.stats.get("component_versions",{})},
        "coverage":{"files_selected":len(snapshot.files),"files_parsed":sum(item.status=="parsed" for item in snapshot.files),
            "file_statuses":dict(sorted(Counter(item.status for item in snapshot.files).items())),
            "unparsed_files":[{"file":item.path,"hash":item.hash,"language":item.language,"status":item.status,"error":item.error}
                for item in snapshot.files if item.status!="parsed"],
            "support_inputs":support,"selection_scope":snapshot.stats.get("source_roots",snapshot.config.get("analysis",{}).get("source_roots",[])),
            "excluded":snapshot.config.get("analysis",{}).get("exclude",[]),
            "meaning":"Captured source and parser scope only; no function or business coverage percentage is inferred."},
        "architecture":{"areas":[{**item,"languages":dict(sorted(item["languages"].items())),"node_types":dict(sorted(item["node_types"].items()))}
            for _,item in sorted(areas.items())],
            "dependencies":[{"from":left,"to":right,**item,"examples_are_sampled":item["edge_count"]>len(item["examples"])}
                for (left,right),item in sorted(dependencies.items())],
            "meaning":"Directory composition and authenticated resolved graph references; these do not infer responsibilities or runtime reachability."},
        "project_declarations":_project_declarations(snapshot),
        "judgments":goals,"functional_chains":functional_chains,"overlapping_source_selections":overlaps,"configured_local_assessments":constraints,
        "graph_observation_counts":[{"type":kind,"status":status,"count":count} for (kind,status),count in sorted(graph_observations.items())],
        "report_scope":{"whole_report_reproduction_claimed":False,
            "unmodeled_functional_domains_are_not_approved":True,
            "meaning":"Configured complete judgments, conditional source chains, local assessments and structural inventory remain separate. Missing analysis is not supplied by reference-report text."},
        "diagnostics":[asdict(item) for item in snapshot.diagnostics],
        "target_executed":False,"target_tests_run":False,"target_build_run":False,"runtime_functionality_verified":False}


def render_markdown(report: dict) -> str:
    snapshot=report["snapshot"]
    coverage=report["coverage"]
    lines=["# "+snapshot["project_name"]+"：自动静态分析报告","", "快照：`"+snapshot["id"]+"`；状态：`"+snapshot["status"]+"`。",
        "","仅使用保存源码、图和分析证据；未执行目标、测试或构建。","","## 项目声明与结构","",
        "项目声明来自保存的 manifest；依赖和产品描述未被当作运行通过证据。",""]
    for manifest in report.get("project_declarations",{}).get("manifests",[]):
        lines.extend(["`"+manifest["file"]+"`：", "", "```json",json.dumps(manifest,ensure_ascii=False,indent=2),"```",""])
    lines.extend(["## 判断与证据","",
        "完整条件判断、局部分析和结构观察分别列出，不从图大小或解析率推断功能完整性。",""])
    for judgment in report["judgments"]:
        lines.append("- **"+str(judgment["goal_id"])+"**："+judgment["summary"])
    lines.append("")
    if not report["judgments"]:
        lines.extend(["此快照未配置完整判断分析。已有结构观察不能代替功能结论。",""])
    for judgment in report["judgments"]:
        lines.extend(["### "+str(judgment["goal_id"]),"", "评估：`"+str(judgment["assessment"])+"`；完整裁决：`"+str(judgment["complete_assessment"]).lower()+"`。",
            "", "保存发现：`"+judgment["finding_id"]+"`；证据：`"+judgment["evidence_id"]+"`。", ""])
        for label,key in (("源码推导","derived_judgment"),("适用条件","conditions"),("反证与范围","refutations"),("必要缺口","necessary_gaps")):
            lines.extend([label+"：", "", "```json",json.dumps(judgment[key],ensure_ascii=False,indent=2),"```",""])
        lines.extend(["| 必要关系 | 结果 |","| --- | --- |"])
        lines.extend("| "+str(item.get("id"))+" | "+str(item.get("status"))+" |" for item in judgment["obligations"])
        lines.append("")
    lines.extend(["## 主要功能链与源码边界","", "以下结论描述所选声明内的调用、保护和装配关系。源码顺序成立仍以该分支到达、前序操作正常完成为条件。",""])
    for overlap in report.get("overlapping_source_selections",[]):
        lines.extend(["同一源码被这些规则选中：`"+"`、`".join(overlap["rule_ids"])+"`；它们不累计为额外功能覆盖。",""])
    if not report.get("functional_chains"):
        lines.extend(["此快照未配置功能链报告抽取；目录盘点不替代功能链。",""])
    for chain in report.get("functional_chains",[]):
        lines.extend(["### "+str(chain["rule_id"]),"", "类型：`"+str(chain["claim_type"])+"`；源码关系评估：`"+str(chain["assessment"].get("state","unknown"))+"`。", "",
            "保存发现：`"+chain["finding_id"]+"`；证据：`"+chain["evidence_id"]+"`。", ""])
        for source in chain["source_scope"].get("selected_definitions",[]):
            lines.append("- `"+str(source.get("role"))+"`：`"+str(source.get("file"))+"` / `"+str(source.get("symbol"))+"`。")
        lines.append("")
        sequences=chain["pattern"].get("sequences",{})
        facts_by_id={fact.get("id"):fact for fact in chain["source_facts"] if fact.get("id")}
        for role,sequence in sequences.items():
            lines.extend(["`"+role+"` 的正常源码顺序：", ""])
            for step in sequence.get("steps",[]):
                location=step.get("location",{})
                calls=[facts_by_id.get(identifier,{}) for identifier in step.get("call_ids",[])]
                names=[str(call.get("callee_source")) for call in calls if call.get("callee_source")]
                label=" / ".join(names) or str(step.get("statement_kind",step.get("kind","statement")))
                lines.append("- `"+label+"`，`"+str(location.get("file",location.get("path","")))+":"+str(location.get("line",""))+"`。")
            lines.append("")
        fact_counts=dict(sorted(Counter(item.get("kind","unknown") for item in chain["source_facts"]).items()))
        lines.extend(["自动关系类型：`"+json.dumps(fact_counts,ensure_ascii=False)+"`。","",
            "分析缺口：", "", "```json",json.dumps(chain["analysis_gaps"],ensure_ascii=False,indent=2),"```", "",
            "条件与反证声明（单列为配置范围，不冒充源码证据）：", "", "```json",json.dumps(chain["policy_declarations"],ensure_ascii=False,indent=2),"```", ""])
    lines.extend(["## 覆盖账本","",f"选入 {coverage['files_selected']} 份源码，解析 {coverage['files_parsed']} 份。该数量描述捕获范围，不是功能覆盖率。","",
        "| 区域 | 文件 | 已解析 |","| --- | --- |"])
    lines.extend(f"| {item['directory']} | {item['files']} | {item['parsed']} |" for item in report["architecture"]["areas"])
    lines.extend(["","## 架构关系","","以下是已绑定的跨目录引用。边数表示源码图记录数，未推断执行频率或职责。","",
        "| 来源 | 目标 | 图引用数 |","| --- | --- |"])
    lines.extend(f"| {item['from']} | {item['to']} | {item['edge_count']} |" for item in report["architecture"]["dependencies"])
    lines.extend(["","## 局部分析","","| 规则 | 类型 | 结果 | 保存发现 |","| --- | --- | --- | --- |"])
    lines.extend(f"| {item['rule_id']} | {item['type']} | {item['status']} | {item['finding_id']} |" for item in report["configured_local_assessments"])
    lines.extend(["","## 未解析与未审范围","", "未建模的功能域继续作为分析缺口，不因已有判断通过而标为已审。", ""])
    for source in coverage["unparsed_files"]:
        lines.append("- `"+source["file"]+"`："+str(source["status"])+"；"+str(source["error"]))
    lines.extend(["","配置排除：`"+", ".join(coverage["excluded"])+"`。","", "不保证运行通过、全仓库无缺陷或完整复现参考人工报告。"])
    return "\n".join(lines)+"\n"
