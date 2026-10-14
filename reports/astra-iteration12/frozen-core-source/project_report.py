"""Generate a project report from captured graph and analysis evidence.

Reference reports are benchmarks, never a source of generated findings. A
directory inventory or a resolved path is not labeled functional coverage.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict
import hashlib
import html
import json
from pathlib import PurePosixPath
import tomllib
from typing import Any

from .models import Finding, GraphSnapshot

VERSION = "captured-project-analysis-report-3"

_PRESENTATION_VERSION = "captured-relation-presentation-2"
_DISPLAY_LIMITS = {"section_nodes": 224, "depth": 8, "list_items": 6,
    "dictionary_fields": 40, "string_characters": 240, "table_rows": 64,
    "table_columns": 12, "tables": 24, "table_search_nodes": 16384}
# These fields remain in the original pattern/source_facts. They are omitted
# only from the extra display projection because the exact pointer preserves
# their full identity and repeated parser/source records obscure the relation.
_DISPLAY_PROVENANCE = frozenset({"parse_identity", "parse_provenance", "text_authentication",
    "syntax_projection", "saved_syntax_projection", "source_excerpt", "source_line",
    "semantic_parse_id", "snapshot_identity", "snapshot_id", "parser_version",
    "source_hash", "span_hash", "coordinate_space", "position_map", "column_unit",
    "original_file_byte_map", "raw_prefix_bytes", "semantic_parser_version"})
_DISPLAY_TECHNICAL = frozenset({"id", "reference", "binding", "declaration_id", "graph_node_id",
    "parameter_index", "argument_index", "source_selector", "resolved_edge_id", "edge_id",
    "source_evidence_refs", "fact_ids", "fact_id", "call_fact_id", "guard_fact_id"})
_SEMANTIC_PRIORITY = ("statement", "interpretation", "comparison", "relation_witnesses",
    "condition", "conditions", "result", "boolean_result", "input_cell", "property_cells", "rows",
    "record_partitions", "absent_input_partitions", "truth_table", "relation", "supported",
    "source_structure_supported", "scoped_source_supported", "unknown", "state", "assessment",
    "rejection", "counterexamples", "bounds", "limitations", "necessary_gaps", "analysis_gaps")


def _display_priority(key: str) -> tuple[int, str]:
    if key in _SEMANTIC_PRIORITY:
        return (_SEMANTIC_PRIORITY.index(key), key)
    if any(word in key for word in ("condition", "witness", "counter", "boundary", "guard", "relation", "result", "interpretation")):
        return (len(_SEMANTIC_PRIORITY), key)
    return (len(_SEMANTIC_PRIORITY) + 1, key)
_TABLE_KEYS = frozenset({"rows", "record_partitions", "absent_input_partitions", "truth_table"})
_LOCATION_FIELDS = frozenset({"file", "line", "column", "end_line", "end_column", "start_byte", "end_byte",
    "original_file_start_byte", "original_file_end_byte", "source_excerpt_truncated", "grammar",
    "column_base", "original_file_byte_offset", *_DISPLAY_PROVENANCE})


def _pointer(parent: str, key: Any) -> str:
    return parent + "/" + str(key).replace("~", "~0").replace("/", "~1")


def _compact_projection(value: Any, pointer: str, fact_refs: dict[str, list[str]],
                        *, limits: dict | None = None, references: dict[str, dict] | None = None) -> dict:
    """Bounded presentation data; never a new analysis or a new assessment.

    All omissions point back into the untouched report pattern. The visitor
    copies actual saved values, including False/None/unknown, rather than
    interpreting field names as success or supplying missing source relations.
    """
    bounds = {**_DISPLAY_LIMITS, **(limits or {})}
    state = {"visited": 0, "truncated": False, "omitted_provenance_fields": 0}

    def visit(item: Any, ref: str, depth: int) -> Any:
        state["visited"] += 1
        if references is not None and ref in references:
            return dict(references[ref])
        if state["visited"] > bounds["section_nodes"] or depth > bounds["depth"]:
            state["truncated"] = True
            return {"omitted_for_presentation": True, "full_value_ref": ref}
        if isinstance(item, str):
            if len(item) > bounds["string_characters"]:
                state["truncated"] = True
                return {"text": item[:bounds["string_characters"]], "truncated": True,
                    "original_characters": len(item), "full_value_ref": ref}
            return item
        if isinstance(item, dict):
            result = {}
            identifier = item.get("id")
            if isinstance(identifier, str) and identifier in fact_refs:
                result["source_fact_refs"] = fact_refs[identifier]
            if (isinstance(item.get("file"), str) and isinstance(item.get("line"), int)
                    and set(item).issubset(_LOCATION_FIELDS)):
                # A location is a display locator, not substitute evidence.
                kept = ("file", "line", "column", "end_line", "start_byte", "end_byte")
                result.update({key: item[key] for key in kept if key in item})
                result["full_location_ref"] = ref
                return result
            visible = [(key, child) for key, child in item.items()
                if key not in _DISPLAY_PROVENANCE | _DISPLAY_TECHNICAL]
            state["omitted_provenance_fields"] += len(item) - len(visible)
            # Scalars and explicit saved scope flags precede large expressions
            # so a long source record cannot hide an existing False boundary.
            visible.sort(key=lambda pair: _display_priority(pair[0]))
            for key, child in visible[:bounds["dictionary_fields"]]:
                if state["visited"] >= bounds["section_nodes"]:
                    state["truncated"] = True
                    result["remaining_fields_ref"] = ref
                    break
                result[key] = visit(child, _pointer(ref, key), depth + 1)
            if len(visible) > bounds["dictionary_fields"]:
                state["truncated"] = True
                result["omitted_fields_for_presentation"] = len(visible) - bounds["dictionary_fields"]
                result["full_value_ref"] = ref
            return result
        if isinstance(item, list):
            selected = []
            for index, child in enumerate(item[:bounds["list_items"]]):
                if state["visited"] >= bounds["section_nodes"]:
                    state["truncated"] = True
                    break
                selected.append(visit(child, _pointer(ref, index), depth + 1))
            if len(selected) != len(item):
                state["truncated"] = True
                return {"shown_items": selected, "shown_count": len(selected), "total_count": len(item),
                    "truncated": True, "full_value_ref": ref}
            return selected
        return item

    result = visit(value, pointer, 0)
    return {"presentation_only": True, "full_value_ref": pointer, "value": result,
        "truncated": state["truncated"], "omitted_provenance_fields": state["omitted_provenance_fields"],
        "visited_nodes": state["visited"]}


def _relation_presentation(chain: dict, chain_pointer: str, *, presentation_pointer: str = "/presentation") -> dict:
    """Expose saved relation patterns, tables and references without new grades."""
    pattern = chain["pattern"]
    pattern_pointer = chain_pointer + "/pattern"
    fact_refs: dict[str, list[str]] = defaultdict(list)
    for index, fact in enumerate(chain["source_facts"]):
        if isinstance(fact.get("id"), str):
            fact_refs[fact["id"]].append(chain_pointer + f"/source_facts/{index}")
    tables = []
    search = {"visited": 0, "truncated": False}

    def find_tables(value: Any, ref: str, depth: int = 0) -> None:
        search["visited"] += 1
        if search["visited"] > _DISPLAY_LIMITS["table_search_nodes"] or depth > _DISPLAY_LIMITS["depth"]:
            search["truncated"] = True
            return
        if isinstance(value, dict):
            for key, child in value.items():
                if key in _DISPLAY_PROVENANCE:
                    continue
                child_ref = _pointer(ref, key)
                table_key = key in _TABLE_KEYS or key.endswith("_table_rows")
                if table_key and isinstance(child, list) and child and all(isinstance(row, dict) for row in child):
                    if len(tables) >= _DISPLAY_LIMITS["tables"]:
                        search["truncated"] = True
                        continue
                    columns = sorted({column for row in child for column in row
                        if column not in _DISPLAY_PROVENANCE | _DISPLAY_TECHNICAL}, key=_display_priority)
                    shown_columns = columns[:_DISPLAY_LIMITS["table_columns"]]
                    rows = []
                    for index, row in enumerate(child[:_DISPLAY_LIMITS["table_rows"]]):
                        row_ref = _pointer(child_ref, index)
                        projection = _compact_projection({key: row[key] for key in shown_columns if key in row}, row_ref,
                            fact_refs, limits={"list_items": 12, "section_nodes": 256})
                        rows.append({"full_row_ref": row_ref, "cells": projection["value"],
                            "truncated": projection["truncated"]})
                    tables.append({"name": key, "full_table_ref": child_ref, "columns": shown_columns,
                        "total_rows": len(child), "rows": rows, "presentation_only": True,
                        "truncated": len(rows) != len(child) or len(columns) != len(shown_columns)
                            or any(row["truncated"] for row in rows)})
                elif not (isinstance(child, dict) and isinstance(child.get("id"), str) and child["id"] in fact_refs):
                    find_tables(child, child_ref, depth + 1)
        elif isinstance(value, list):
            for index, child in enumerate(value[:_DISPLAY_LIMITS["list_items"]]):
                find_tables(child, _pointer(ref, index), depth + 1)
            if len(value) > _DISPLAY_LIMITS["list_items"]:
                search["truncated"] = True

    find_tables(pattern, pattern_pointer)
    table_references = {table["full_table_ref"]: {"presentation_table_ref": presentation_pointer + f"/tables/{index}",
        "full_value_ref": table["full_table_ref"], "total_rows": table["total_rows"],
        "presentation_only": True} for index, table in enumerate(tables)}
    sections = [{"name": key, **_compact_projection(value, _pointer(pattern_pointer, key), fact_refs,
        references=table_references)}
        for key, value in sorted(pattern.items(), key=lambda item: _display_priority(item[0]))
        if key not in _DISPLAY_PROVENANCE | _DISPLAY_TECHNICAL] if isinstance(pattern, dict) else []
    return {"version": _PRESENTATION_VERSION, "presentation_only": True, "full_pattern_ref": pattern_pointer,
        "limits": dict(_DISPLAY_LIMITS), "sections": sections, "tables": tables,
        "truncated": search["truncated"] or any(section["truncated"] for section in sections)
            or any(table["truncated"] for table in tables),
        "table_discovery_truncated": search["truncated"],
        "meaning": "Bounded display of actual saved pattern values. Full pattern and source facts remain unchanged; omissions are not analysis gaps or new conclusions."}


def _source_relation_index(chains: list[dict]) -> tuple[dict, list[dict]]:
    entries, writers = [], []
    for index, chain in enumerate(chains):
        chain_ref = f"/functional_chains/{index}"
        entry_ref = f"/source_relation_index/entries/{index}"
        entry = {"rule_id": chain["rule_id"], "claim_type": chain["claim_type"],
            "finding_id": chain["finding_id"], "evidence_id": chain["evidence_id"],
            "assessment_ref": chain_ref + "/assessment", "pattern_ref": chain_ref + "/pattern",
            "source_facts_ref": chain_ref + "/source_facts", "source_scope_ref": chain_ref + "/source_scope",
            "analysis_gaps_ref": chain_ref + "/analysis_gaps", "saved_evidence_pointer": chain["saved_evidence_pointer"],
            "presentation": _relation_presentation(chain, chain_ref, presentation_pointer=entry_ref + "/presentation")}
        entries.append(entry)
        pattern = chain["pattern"]
        groups = pattern.get("captured_resource_writer_groups") if isinstance(pattern, dict) else None
        if isinstance(groups, list):
            # The writer index copies only saved symbols/assessment and refs.
            # No directory-name responsibility or unique owner is inferred.
            writers.append({"rule_id": chain["rule_id"], "finding_id": chain["finding_id"], "evidence_id": chain["evidence_id"],
                "source_relation_ref": entry_ref, "writer_groups_ref": chain_ref + "/pattern/captured_resource_writer_groups",
                **{key + "_ref": chain_ref + "/pattern/" + key for key in ("writer_fact_ids",
                    "same_token_reference_fact_ids", "source_rejection_guard_fact_ids") if key in pattern},
                "source_assessment": pattern.get("ownership_assessment"),
                "source_assessment_ref": chain_ref + "/pattern/ownership_assessment" if "ownership_assessment" in pattern else None,
                "saved_responsibility_interpretation_ref": chain_ref + "/pattern/responsibility_interpretation" if "responsibility_interpretation" in pattern else None,
                "selected_writer_symbols": sorted({symbol for group in groups if isinstance(group, dict)
                    for symbol in group.get("selected_writer_symbols", []) if isinstance(symbol, str)}),
                "captured_group_count": len(groups), "presentation_only": True,
                "meaning": "References to captured lexical writers and consumers only; unique ownership, canonical authority and authorization are not inferred."})
    return {"version": _PRESENTATION_VERSION, "entries": entries, "presentation_only": True,
        "meaning": "Navigation index into saved source-relation findings; contains no additional assessment or functional coverage claim."}, writers


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
    relation_index, writer_references = _source_relation_index(functional_chains)
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
    report = {"version":VERSION,"snapshot":{"id":snapshot.id,"project_id":snapshot.project_id,
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
            "captured_writer_references": writer_references,
            "meaning":"Directory composition and authenticated resolved graph references; these do not infer responsibilities or runtime reachability."},
        "project_declarations":_project_declarations(snapshot),
        "judgments":goals,"functional_chains":functional_chains,"source_relation_index":relation_index,
        "overlapping_source_selections":overlaps,"configured_local_assessments":constraints,
        "graph_observation_counts":[{"type":kind,"status":status,"count":count} for (kind,status),count in sorted(graph_observations.items())],
        "report_scope":{"whole_report_reproduction_claimed":False,
            "unmodeled_functional_domains_are_not_approved":True,
            "meaning":"Configured complete judgments, conditional source chains, local assessments and structural inventory remain separate. Missing analysis is not supplied by reference-report text."},
        "diagnostics":[asdict(item) for item in snapshot.diagnostics],
        "target_executed":False,"target_tests_run":False,"target_build_run":False,"runtime_functionality_verified":False}
    from .analysis_inputs import tool_identity
    from .architecture_responsibilities import build_responsibility_explanations, VERSION as RESPONSIBILITY_VERSION
    from .responsibility_operations import VERSION as OPERATION_VERSION
    from .report_markdown import VERSION as MARKDOWN_VERSION
    from .parsers import parser_version as semantic_parser_version
    semantic_languages = set()
    for source in snapshot.files:
        if source.language in {"typescript", "javascript", "ts" , "js"}:
            semantic_languages.add("typescript")
        elif source.language in {"tsx", "jsx"}:
            semantic_languages.add("tsx")
        elif source.language == "rust":
            semantic_languages.add("rust")
    report["report_components"] = {"generator": VERSION, "presentation": _PRESENTATION_VERSION,
        "markdown": MARKDOWN_VERSION,
        "responsibility_explanations": RESPONSIBILITY_VERSION, "responsibility_operations": OPERATION_VERSION,
        "current_semantic_parser_versions": {language: semantic_parser_version(language)
            for language in sorted(semantic_languages)},
        "generating_tool_identity": tool_identity(),
        "meaning": "Report generation versions are separate from the saved snapshot's analysis versions. Explanations interpret captured source; existing findings are not upgraded."}
    report["architecture"]["responsibility_explanations"] = build_responsibility_explanations(snapshot, report)
    report["documentation_comparisons"] = [{"rule_id": chain["rule_id"],
        "finding_id": chain["finding_id"], "evidence_id": chain["evidence_id"],
        "assessment": chain["assessment"], "comparison": chain["pattern"].get("comparison", {}),
        "aspects": chain["pattern"].get("documentation_comparisons", []),
        "document_claims_ref": f"/functional_chains/{index}/pattern/document_claims",
        "source_scope_ref": f"/functional_chains/{index}/source_scope",
        "source_facts_ref": f"/functional_chains/{index}/source_facts",
        "full_pattern_ref": f"/functional_chains/{index}/pattern"}
        for index, chain in enumerate(functional_chains)
        if chain["claim_type"] == "document_deployment_consistency"]
    return report


def _markdown_cell(value: Any) -> str:
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return html.escape(text, quote=False).replace("`", "&#96;").replace("|", "\\|").replace("\n", "<br>")


def _json_markdown(value: Any) -> list[str]:
    content = json.dumps(value, ensure_ascii=False, indent=2)
    fence = "```"
    while fence in content:
        fence += "`"
    return [fence + "json", content, fence, ""]


def _render_relation_presentation(presentation: dict) -> list[str]:
    lines = ["保存关系的展示摘要（`presentation_only=true`；不新增评级）：", "",
        "完整 pattern：`" + presentation["full_pattern_ref"] + "`。展示截断：`"
        + str(presentation["truncated"]).lower() + "`；完整证据与原 pattern 保留。", ""]
    for table in presentation["tables"]:
        lines.extend(["**" + table["name"] + "**：`" + table["full_table_ref"] + "`；显示 "
            + str(len(table["rows"])) + "/" + str(table["total_rows"]) + " 行；展示截断：`"
            + str(table["truncated"]).lower() + "`。", ""])
        columns = table["columns"]
        lines.append("| " + " | ".join(_markdown_cell(column) for column in [*columns, "完整行引用"]) + " |")
        lines.append("| " + " | ".join("---" for _ in range(len(columns) + 1)) + " |")
        for row in table["rows"]:
            cells = row["cells"]
            lines.append("| " + " | ".join(_markdown_cell(cells[column]) if column in cells
                else "未显示或原行缺项；见完整引用" for column in columns)
                + " | " + _markdown_cell(row["full_row_ref"]) + " |")
        lines.append("")
    scalar_sections = [section for section in presentation["sections"]
        if not isinstance(section["value"], (dict, list))]
    if scalar_sections:
        lines.extend(["| 保存字段 | 实际值 | 完整引用 |", "| --- | --- | --- |"])
        lines.extend("| " + _markdown_cell(section["name"]) + " | " + _markdown_cell(section["value"])
            + " | " + _markdown_cell(section["full_value_ref"]) + " |" for section in scalar_sections)
        lines.append("")
    for section in presentation["sections"]:
        if section in scalar_sections:
            continue
        lines.extend(["**" + section["name"] + "**：`" + section["full_value_ref"] + "`；展示截断：`"
            + str(section["truncated"]).lower() + "`。", ""])
        lines.extend(_json_markdown(section["value"]))
    return lines


def render_markdown(report: dict) -> str:
    from .report_markdown import render_markdown as render
    return render(report)
