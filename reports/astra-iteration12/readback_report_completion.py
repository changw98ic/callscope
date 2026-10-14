"""Stream saved reports and verify finite report-content references.

Artifact readback only: no target files, database, analysis engine or tests.
The output is evidence for reconciling the original finite report clauses,
never a target-code judgment or completion inferred from a version/count.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'astra-iteration11'))
from render_report_summaries import _SavedJSON, _OptionalProjection


def pointer(root, path):
    if not isinstance(path,str) or not path.startswith('/'):
        raise ValueError('Expected an absolute JSON pointer')
    current=root
    for token in path.split('/')[1:]:
        token=token.replace('~1','/').replace('~0','~')
        current=current[int(token)] if isinstance(current,list) else current[token]
    return current


def digest(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=True,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()


def source_location(location, block):
    if not isinstance(location,dict): raise ValueError('Source location is not an object')
    actual=pointer(block,location['location_ref']) if location.get('location_ref') else location
    if not isinstance(actual,dict) or not all(k in actual for k in ('file','source_hash','start_byte','end_byte','span_hash')):
        raise ValueError('Source location lacks identity fields')
    if not isinstance(actual['start_byte'],int) or not isinstance(actual['end_byte'],int) or actual['start_byte']>actual['end_byte']:
        raise ValueError('Invalid source span')
    for key in ('file','source_hash','start_byte','end_byte'):
        if key in location and location[key]!=actual[key]: raise ValueError('Thin location disagrees: '+key)
    return actual


def evidence_reference(reference, block):
    if not isinstance(reference,dict): raise ValueError('Evidence reference is not an object')
    actual=pointer(block,reference['evidence_ref']) if reference.get('evidence_ref') else reference
    if not isinstance(actual,dict) or not actual.get('reference_role'):
        raise ValueError('Evidence reference lacks role')
    for key in ('rule_id','goal_id','reference_role'):
        if key in reference and reference[key]!=actual.get(key): raise ValueError('Thin evidence disagrees: '+key)
    if actual.get('old_finding_proves_new_operation') is True:
        raise ValueError('Selection context was promoted to proof of a new operation')
    return actual


OP_SELECTION={k:True for k in ('id','operation_kind','actual_owner','subject','operands','guards','source_order','source_locations',
    'source_evidence_refs','relationships','limitations','source_evidence_references_truncated')}
ARCH_SELECTION={k:True for k in ('version','snapshot_identity','assessment','analysis_gaps','explanation_source_gaps',
    'source_location_index','evidence_reference_index','operation_extraction_flags','operation_extraction_budget',
    'computed_source_contract_seams','unreviewed_scope')}
ARCH_SELECTION.update({'operations':[OP_SELECTION], 'declaration_explanations':[{
    k:True for k in ('id','actual_owner','summary','summary_statement_ids','statements','all_operation_refs','presentation_truncated')}],
    'explicit_source_transfers':True,'normal_source_orders':True,'authenticated_interface_reuse':True})
FACT_SELECTION={'id':True,'kind':True,'location':_OptionalProjection({k:True for k in ('file','line','start_byte','end_byte','source_hash','span_hash')})}
PATTERN_SELECTION={k:True for k in ('version','scoped_source_supported','relation_witnesses','necessary_gaps','conditions','bounds',
    'comparison','documentation_comparisons','document_claims','document_scope','source_relation_fact_ids','derived_explanation',
    'lineage_relations','finite_mode_permission_relation','report_explanation','source_explanation','conditional_effect_interfaces',
    'execution_delivery_projection_distinct','retention_boundary','command_boundary','record_boundary','model','statement',
    'interpretation','source_statement_relation_closed','source_conditions')}
CHAIN_SELECTION={'rule_id':True,'claim_type':True,'finding_id':True,'evidence_id':True,'assessment':True,
    'source_scope':True,'analysis_gaps':True,'pattern':_OptionalProjection(PATTERN_SELECTION),'source_facts':[FACT_SELECTION],
    'presentation':True,'trusted_models':True,'policy_declarations':True}
GOAL_SELECTION={k:True for k in ('goal_id','finding_id','evidence_id','assessment','complete_assessment','full_goal_supported','derived_judgment','conditions','refutations','necessary_gaps')}
GOAL_SELECTION['obligations']=[{k:True for k in ('id','status','necessary_gaps')}]
FORMAL_SELECTION={'snapshot':True,'report_components':True,'report_scope':True,'target_executed':True,'target_tests_run':True,
    'target_build_run':True,'runtime_functionality_verified':True,'version':True,
    'coverage':{k:True for k in ('files_selected','files_parsed','file_statuses','unparsed_files','support_inputs','selection_scope','excluded','meaning')},
    'project_declarations':True,'diagnostics':True,
    'judgments':[GOAL_SELECTION],'functional_chains':[CHAIN_SELECTION],
    'architecture':{'responsibility_explanations':ARCH_SELECTION},'documentation_comparisons':True,'overlapping_source_selections':True}
DEV_SELECTION={'development_query':True,'not_formal_v14_result':True,'saved_snapshot_id':True,'saved_source_hash':True,
    'saved_policy_hash':True,'current_module_sha256':True,'query_module_bytes_stable':True,'explanation_module_sha256':True,
    'explanation_module_bytes_stable':True,'explanations':ARCH_SELECTION}


def validate_architecture(block):
    issues=[]; operations=block.get('operations',[]); checked=[]; by_id={}; statements=[]
    for index,op in enumerate(operations):
        try:
            if not op.get('id') or op['id'] in by_id: raise ValueError('Missing/duplicate operation id')
            by_id[op['id']]=(index,op)
            locations=[source_location(v,block) for v in op.get('source_locations',[])]
            refs=[evidence_reference(v,block) for v in op.get('source_evidence_refs',[])]
            if not locations or not refs: raise ValueError('Operation lacks actual source/ref identity')
            if op.get('source_evidence_references_truncated'): raise ValueError('Operation evidence references truncated')
            checked.append(op['id'])
        except (KeyError,ValueError,IndexError,TypeError) as error:
            issues.append({'kind':'operation_reference_gap','index':index,'operation_id':op.get('id'),'reason':str(error)})
    for di,declaration in enumerate(block.get('declaration_explanations',[])):
        actual_statement_ids={s.get('id') for s in declaration.get('statements',[])}
        if not declaration.get('summary') or any(sid not in actual_statement_ids for sid in declaration.get('summary_statement_ids',[])):
            issues.append({'kind':'summary_statement_link_missing','declaration_index':di})
        selected={s.get('id'):s.get('text') for s in declaration.get('statements',[])}
        summary_text=' '.join(selected[sid] for sid in declaration.get('summary_statement_ids',[]) if sid in selected)
        if declaration.get('summary')!=summary_text:
            issues.append({'kind':'summary_body_does_not_equal_selected_actual_statements','declaration_index':di})
        for si,statement in enumerate(declaration.get('statements',[])):
            try:
                op=pointer(block,statement['operation_pointer'])
                if op.get('id')!=statement.get('operation_id') or op.get('operation_kind')!=statement.get('operation_kind'):
                    raise ValueError('Statement/operation identity mismatch')
                if not statement.get('text') or statement.get('runtime_effect_proven') is not False:
                    raise ValueError('Statement lacks text or changed runtime boundary')
                if statement.get('source_evidence_refs_pointer'):
                    if pointer(block,statement['source_evidence_refs_pointer'])!=op['source_evidence_refs']:
                        raise ValueError('Statement evidence pointer mismatch')
                for loc in statement.get('source_locations',[]):source_location(loc,block)
                statements.append({'declaration_index':di,'statement_index':si,'declaration_id':declaration.get('id'),
                    'actual_owner':declaration.get('actual_owner'),'text':statement['text'],'operation_id':op['id'],
                    'operation_kind':op['operation_kind'],'operation_pointer':statement['operation_pointer'],
                    'source_evidence_refs':[evidence_reference(v,block) for v in op['source_evidence_refs']],
                    'operand_source_text':op.get('operands',{}).get('source_text'),
                    'formal_statement_pointer':f'/architecture/responsibility_explanations/declaration_explanations/{di}/statements/{si}'})
            except (KeyError,ValueError,IndexError,TypeError) as error:
                issues.append({'kind':'declaration_statement_gap','declaration_index':di,'statement_index':si,'reason':str(error)})
    for key in ('explicit_source_transfers','normal_source_orders'):
        for index,relation in enumerate(block.get(key,[])):
            for end in ('from','to'):
                try:
                    ref=relation[end]; actual=pointer(block,ref['operation_pointer'])
                    if actual.get('id')!=ref.get('operation_id'):raise ValueError('Relation endpoint mismatch')
                except (KeyError,ValueError,IndexError,TypeError) as error:
                    issues.append({'kind':'explicit_relation_reference_gap','collection':key,'index':index,'reason':str(error)})
    return {'reference_issues':issues,'checked_operation_ids':checked,'actual_statements':statements,
        'operation_count_is_not_responsibility_completion':True,
        'reported_analysis_gaps':block.get('analysis_gaps',[]),'reported_explanation_source_gaps':block.get('explanation_source_gaps',[])}


def merge_selection(left,right):
    if left is True or right is True:return True
    if isinstance(left,list) and isinstance(right,list):return [merge_selection(left[0],right[0])]
    if isinstance(left,dict) and isinstance(right,dict):
        return {k:merge_selection(left[k],right[k]) if k in left and k in right else left.get(k,right.get(k)) for k in left.keys()|right.keys()}
    raise ValueError('Incompatible JSON projection selectors')


def pointer_selection(path,selection):
    tokens=[t.replace('~1','/').replace('~0','~') for t in path.split('/')[1:]]
    for token in reversed(tokens):selection=[selection] if token.isdigit() else {token:selection}
    return selection


def validate_computed_seams(path,report,sha):
    """Read the actual finite source objects targeted by saved seam pointers."""
    seams=report.get('architecture',{}).get('responsibility_explanations',{}).get('computed_source_contract_seams',[])
    selector={}; marker={k:True for k in ('supported','selected_paths','other_path_choices','standard_spawn_binding',
        'worker_source_path_choices','model','statement','interpretation','source_statement_relation_closed',
        'scoped_source_supported','relation_witnesses','source_conditions','necessary_gaps','kind')}
    marker['binding']={'targets':True,'all_captured_receiver_variants_resolved':True}
    for seam in seams:
        path_value=seam.get('source_analysis_pointer')
        if not isinstance(path_value,str) or not path_value.startswith('/'):continue
        selected={**marker}
        if seam.get('kind')=='finite_generated_json_serde_message_source_relation':
            selected.update({k:True for k in ('snapshot_id','source_hash','policy_hash','conditions','scope_boundaries')})
            selected['relations']=[{k:True for k in ('relation_id','kind','source_class','obligation_id','command_type',
                'payload_type','spec_type','wire_field','field_optional','rust_field','rust_type','source_attributes',
                'absent_wire_value','command_path','method','message_path','typed_request_variant','model_record_id')}]
            selected['models']=[{k:True for k in ('model_id','version','model_record_id','applicability')}]
            selected['obligations']=[{k:True for k in ('id','status','complete','necessary_gaps','evidence_relation_ids','transport_model')}]
        selected.update({k:{'supported':True} for k in seam.get('source_part_states',{})})
        selected.setdefault('writer',{}).update({'receipt_keys':True})
        selected.setdefault('response',{}).update({'handler_fields':True})
        selector=merge_selection(selector,pointer_selection(path_value,selected))
        if '/channels/' in path_value:
            channel_path=path_value.rsplit('/',1)[0]
            selector=merge_selection(selector,pointer_selection(channel_path,{k:True for k in (
                'snapshot_id','source_hash','policy_hash','source_only','creates_calls_edges')}))
    if not selector:return []
    actual,second_sha=_SavedJSON(path).load(selector)
    if second_sha!=sha:raise ValueError('Formal report changed between reference and source readback')
    rows=[]
    for i,seam in enumerate(seams):
        issues=[]; value=None;path_value=seam.get('source_analysis_pointer')
        try:
            value=pointer(actual,path_value)
            if not isinstance(value,dict):raise ValueError('Seam target is not a finite source object')
            kind=seam.get('kind')
            if not seam.get('text') or seam.get('creates_calls_edge') is not False:issues.append('missing actual text or source-only edge boundary')
            if kind=='finite_dynamic_command_source_assembly':
                if not value.get('selected_paths') or seam.get('supported_source_relation')!=(value.get('supported') is True):issues.append('dynamic import finite relation differs')
            elif kind=='captured_standard_node_worker_process_seam':
                if value.get('standard_spawn_binding') is not True or not value.get('worker_source_path_choices'):issues.append('standard Node process assembly source differs')
            elif kind=='conditional_captured_receiver_assembly':
                binding=value.get('binding',{})
                if seam.get('captured_targets')!=[v.get('selector') for v in binding.get('targets',[])]:issues.append('conditional receiver targets differ')
                if seam.get('supported_source_relation')!=(binding.get('all_captured_receiver_variants_resolved') is True):issues.append('conditional receiver support differs')
            elif kind=='finite_conditional_state_or_publication_source_relation':
                if value.get('statement')!=seam.get('text') or value.get('source_statement_relation_closed') is not True or value.get('scoped_source_supported') is not True or not value.get('relation_witnesses'):
                    issues.append('conditional lineage/publication explanation differs from actual finite pattern')
            elif kind=='finite_generated_json_serde_message_source_relation':
                identity=report.get('snapshot',{})
                for key,seam_key in [('snapshot_id','id'),('source_hash','source_hash'),('policy_hash','policy_hash')]:
                    if value.get(key)!=identity.get(seam_key):issues.append('finite protocol context identity differs: '+key)
                obligation=pointer(actual,seam['source_obligation_pointer'])
                if obligation.get('id')!=seam.get('obligation_id') or obligation.get('status')!=seam.get('obligation_status') or obligation.get('transport_model')!=seam.get('transport_model'):
                    issues.append('finite protocol obligation/transport condition differs')
                if obligation.get('status')!='supported' or obligation.get('complete') is not True or obligation.get('necessary_gaps'):
                    issues.append('finite protocol necessary obligation no longer closed')
                if value.get('conditions')!=seam.get('conditions') or value.get('scope_boundaries')!=seam.get('scope_boundaries'):
                    issues.append('finite protocol source conditions or boundaries differ')
                kinds=set();relations=[]
                for reference in seam.get('source_relation_refs',[]):
                    relation=pointer(actual,reference['source_pointer']);relations.append(relation);kinds.add(relation.get('kind'))
                    if any(relation.get(k)!=reference.get(k) for k in ('relation_id','kind','source_class')) or relation.get('obligation_id')!=obligation.get('id') or relation.get('relation_id') not in obligation.get('evidence_relation_ids',[]):
                        issues.append('finite protocol relation identity/obligation differs')
                    for key in ('command_type','payload_type','spec_type','wire_field','rust_field','rust_type','absent_wire_value','command_path','method','typed_request_variant'):
                        if relation.get(key) is not None and str(relation[key]) not in seam['text']:issues.append('finite protocol actual source value missing from body: '+key)
                if not {'generated_typescript_wire_record_path','wire_record_field_mapping_and_default','command_json_http_record_transport',
                        'server_json_body_to_dispatcher','typed_application_family_dispatch','typed_command_update_dispatch'}<=kinds:
                    issues.append('finite protocol semantic source relation missing')
                model_ids=set()
                for reference in seam.get('models',[]):
                    model=pointer(actual,reference['source_pointer'])
                    model_ids.add(model.get('model_record_id'))
                    if model.get('model_id')!=reference.get('id') or model.get('version')!=reference.get('version') or model.get('model_record_id')!=reference.get('model_record_id') or model.get('applicability',{}).get('accepted') is not True or reference.get('applicability_accepted') is not True:
                        issues.append('finite protocol model identity or applicability differs')
                if not model_ids or any(r.get('model_record_id') is not None and r['model_record_id'] not in model_ids for r in relations):
                    issues.append('finite protocol source relations do not share accepted model records')
                if seam.get('network_success_verified') is not False or seam.get('generated_support_upgraded_to_implementation') is not False:
                    issues.append('finite protocol runtime or support-only boundary changed')
            else:
                if value.get('kind')!=kind or seam.get('supported_source_relation')!=(value.get('supported') is True):issues.append('channel kind/source support differs')
                for part,state in seam.get('source_part_states',{}).items():
                    if value.get(part,{}).get('supported')!=state:issues.append('channel part state differs: '+part)
                envelope=pointer(actual,path_value.rsplit('/',1)[0]); identity=report.get('snapshot',{})
                for key,seam_key in [('snapshot_id','id'),('source_hash','source_hash'),('policy_hash','policy_hash')]:
                    if envelope.get(key)!=identity.get(seam_key):issues.append('channel identity differs: '+key)
                if envelope.get('source_only') is not True or envelope.get('creates_calls_edges') is not False:issues.append('channel source-only boundary differs')
        except (KeyError,ValueError,IndexError,TypeError) as error:issues.append(str(error))
        rows.append({'pointer':f'/architecture/responsibility_explanations/computed_source_contract_seams/{i}',
            'actual_seam':seam,'actual_source_pointer_target':value,'source_reference_issues':issues,
            'pointer_verification_is_not_runtime_or_full_architecture_proof':True})
    return rows


def match_statements(block, check):
    """Locate actual typed operations and their generated body, not labels."""
    matches=[]
    for i,op in enumerate(block.get('operations',[])):
        if check(op):
            matches.append({'operation_id':op['id'],'operation_pointer':f'/architecture/responsibility_explanations/operations/{i}',
                'actual_owner':op.get('actual_owner'), 'operation_kind':op.get('operation_kind'),
                'operand_source_text':op.get('operands',{}).get('source_text'),
                'source_evidence_refs':op.get('source_evidence_refs',[]),'source_locations':op.get('source_locations',[])})
    return matches


def critical_source_content(block, repo):
    if repo!='codepatchbay':return {}
    def owner(op,symbol):return op.get('actual_owner',{}).get('symbol')==symbol
    def text(op):return str(op.get('operands',{}).get('source_text',''))
    def kind(op,value):return op.get('operation_kind')==value
    dynamic=match_statements(block,lambda o:owner(o,'main') and kind(o,'call_argument_transfer')
        and o.get('operands',{}).get('callee',{}).get('source_text')=='import' and 'COMMANDS[cmd]' in text(o))
    environment=match_statements(block,lambda o:owner(o,'resolveExecutorRoot') and kind(o,'return_transfer')
        and 'CPB_EXECUTOR_ROOT' in text(o) and 'fallbackRoot' in text(o))
    ports=match_statements(block,lambda o:owner(o,'buildServices') and kind(o,'record_construction')
        and {'createJob','appendEvent','startPhase','completePhase'}.issubset({f.get('name') for f in o.get('operands',{}).get('record_fields',[])}))
    count_init=match_statements(block,lambda o:owner(o,'scopeMatches') and kind(o,'binding_initializer')
        and re.search(r'\bcount\b',text(o)) is not None and ('0' in text(o)))
    count_update=match_statements(block,lambda o:owner(o,'scopeMatches') and kind(o,'binding_update')
        and '+=' in text(o))
    count_return=match_statements(block,lambda o:owner(o,'scopeMatches') and kind(o,'return_transfer')
        and re.search(r'\bcount\b',text(o)) is not None)
    return {'dynamic_command_source_operations':dynamic,'executor_root_source_operations':environment,
        'conditional_port_record_operations':ports,'scope_counter_initializer_operations':count_init,
        'scope_counter_update_operations':count_update,'scope_counter_return_operations':count_return,
        'source_form_queries_are_not_runtime_or_whole_paragraph_proofs':True}


def documentation_readback(report,development=None):
    chains={c.get('rule_id'):c for c in report.get('functional_chains',[])}
    comparisons=report.get('documentation_comparisons',[])
    if development:
        # The wrapper is an artifact-reading adapter, not a new system result.
        rid=development['rule']['id'];chains={rid:development}
        comparisons=[{'rule_id':rid,'aspects':development['pattern']['documentation_comparisons'],
            'comparison':development['pattern']['comparison'],'development_pattern_adapter':True}]
    rows=[]
    for index,comparison in enumerate(comparisons):
        issues=[]; chain=chains.get(comparison.get('rule_id')); aspects=[]
        if chain is None:issues.append('comparison has no actual saved source-chain entry')
        if not development and chain is not None:
            for name,expected in [('full_pattern_ref',chain.get('pattern')),('document_claims_ref',chain.get('pattern',{}).get('document_claims')),
                    ('source_scope_ref',chain.get('source_scope')),('source_facts_ref',chain.get('source_facts'))]:
                try:
                    if pointer(report,comparison[name])!=expected:issues.append('top-level documentation pointer differs: '+name)
                except (KeyError,ValueError,IndexError,TypeError) as error:issues.append('top-level documentation pointer missing: '+name+': '+str(error))
            if comparison.get('aspects')!=chain.get('pattern',{}).get('documentation_comparisons'):issues.append('top-level aspects differ from saved finite source pattern')
        facts={f.get('id'):f for f in (chain or {}).get('source_facts',[])}
        claims={c.get('id'):c for c in (chain or {}).get('pattern',{}).get('document_claims',[])}
        for claim in claims.values():
            location=claim.get('location',{}); sentence=claim.get('sentence')
            if not isinstance(sentence,str) or hashlib.sha256(sentence.encode()).hexdigest()!=location.get('span_hash'):
                issues.append('document literal byte identity does not match saved span: '+str(claim.get('id')))
            if not claim.get('heading_context') or not location.get('source_hash'):issues.append('document scope/context identity missing')
        for ai,aspect in enumerate(comparison.get('aspects',[])):
            missing=[fid for fid in aspect.get('source_fact_ids',[]) if fid not in facts]
            doc_missing=[fid for fid in aspect.get('document_fact_ids',[]) if fid not in claims]
            if missing or doc_missing:issues.append({'aspect_index':ai,'missing_source_ids':missing,'missing_document_ids':doc_missing})
            aspects.append({'pointer':f'/pattern/documentation_comparisons/{ai}' if development else f'/documentation_comparisons/{index}/aspects/{ai}',**aspect,
                'resolved_source_facts':[facts[fid] for fid in aspect.get('source_fact_ids',[]) if fid in facts],
                'resolved_document_claims':[claims[fid] for fid in aspect.get('document_fact_ids',[]) if fid in claims]})
        expected={'documented_control_plane_scope_and_device_source_route','credential_material_reference_and_lifetime','worker_stream_protocol_and_local_consumer'}
        if {a.get('aspect') for a in aspects}!=expected:issues.append('missing/duplicate expected finite comparison aspects')
        if any(not a.get('statement') or not a.get('source_fact_ids') or not a.get('document_fact_ids') for a in aspects):
            issues.append('aspect lacks actual explanation or source/document IDs')
        by_aspect={a.get('aspect'):a for a in aspects}
        credential=by_aspect.get('credential_material_reference_and_lifetime',{})
        stream=by_aspect.get('worker_stream_protocol_and_local_consumer',{})
        if credential and credential.get('credential_lifetime')!='unknown':issues.append('credential lifetime boundary changed')
        if stream and stream.get('protocol_bypass_proven') is not False:issues.append('protocol-bypass boundary changed')
        rows.append({'rule_id':comparison.get('rule_id'),'actual_comparison':comparison.get('comparison'),
            'input_context':'actual_saved_development_query' if development else 'actual_saved_formal_report',
            'source_assessment':comparison.get('assessment'),'actual_aspects':aspects,'reference_or_scope_issues':issues,
            'necessary_gaps':(chain or {}).get('pattern',{}).get('necessary_gaps',[]),
            'all_required_source_aspects_supported':len(aspects)==3 and all(a.get('scoped_source_supported') is True for a in aspects),
            'comparison_is_not_security_or_runtime_judgment':True})
    return rows


def load_formal(path):
    report, sha=_SavedJSON(path).load(FORMAL_SELECTION)
    return report,sha


def publication_identity_readback(report,freeze,repo):
    snapshot=report.get('snapshot',{});components=report.get('report_components',{});issues=[]
    saved_tool=snapshot.get('component_versions',{}).get('tool',{})
    generated_tool=components.get('generating_tool_identity',{})
    for origin,tool in [('saved_snapshot',saved_tool),('report_generation',generated_tool)]:
        if tool.get('source_hash')!=freeze.get('tool_identity',{}).get('source_hash'):
            issues.append(origin+' tool source hash differs from formal freeze')
    if snapshot.get('policy_hash')!=freeze.get('effective_policy_sha256',{}).get(repo):
        issues.append('effective policy hash differs from formal freeze')
    block=report.get('architecture',{}).get('responsibility_explanations',{})
    for explanation_key,snapshot_key in (('snapshot_id','id'),('source_hash','source_hash'),('policy_hash','policy_hash')):
        if block.get('snapshot_identity',{}).get(explanation_key)!=snapshot.get(snapshot_key):issues.append('explanation/saved identity differs: '+explanation_key)
    for key in ('target_executed','target_tests_run','target_build_run','runtime_functionality_verified'):
        if report.get(key) is not False:issues.append('original source-only report boundary missing: '+key)
    if report.get('report_scope',{}).get('whole_report_reproduction_claimed') is not False:
        issues.append('unqualified whole-report reproduction boundary changed')
    return {'snapshot':snapshot,'generating_components':components,'coverage':report.get('coverage'),
        'project_declarations':report.get('project_declarations'),'diagnostics':report.get('diagnostics'),
        'report_scope':report.get('report_scope'),'identity_or_scope_issues':issues,
        'whole_original_finite_content_completion_not_inferred_from_identity':True}


def prior_entry_readback(contract, reports):
    result=[]
    for entry in contract['prior_five_judgments_and_source_relations']:
        if entry['repository'] not in reports:continue
        report=reports.get(entry['repository'],{}); key='goal_id' if entry['kind']=='registered_condition_judgment' else 'rule_id'
        collection='judgments' if key=='goal_id' else 'functional_chains'
        matches=[(i,r) for i,r in enumerate(report.get(collection,[])) if r.get(key)==entry['id']]
        row={'id':entry['id'],'repository':entry['repository'],'kind':entry['kind'],'new_formal_readback':None}
        if len(matches)==1:
            i,value=matches[0]; assessment=value.get('assessment',{})
            row['new_formal_readback']={'pointer':f'/{collection}/{i}','finding_id':value.get('finding_id'),
                'evidence_id':value.get('evidence_id'),'assessment':assessment,
                'complete_assessment':value.get('complete_assessment'),'full_goal_supported':value.get('full_goal_supported'),
                'necessary_gaps':value.get('necessary_gaps',[]),'analysis_gaps':value.get('analysis_gaps',[]),
                'actual_derived_judgment':value.get('derived_judgment'),
                'actual_conditions':value.get('conditions'),'actual_refutations':value.get('refutations'),
                'actual_pattern_scope':value.get('pattern'),
                'actual_saved_presentation_values':value.get('presentation'),
                'source_fact_refs':[{'id':f.get('id'),'kind':f.get('kind'),'location':f.get('location')} for f in value.get('source_facts',[])]}
        else:row['missing_or_duplicate_current_entry']=len(matches)
        result.append(row)
    return result


def original_row_candidates(contract, reports, architecture):
    rows=[]
    for entry in contract['pending_original_explanations']:
        if entry['kind']!='finite_architecture_responsibility_explanation':continue
        repo=entry['repository']; related=set(entry['prior_related_entries']); candidates=[]
        for statement in architecture.get(repo,{}).get('actual_statements',[]):
            contexts={r.get('goal_id') or r.get('rule_id') for r in statement['source_evidence_refs']}
            if related & contexts:
                candidates.append(statement)
        rows.append({'id':entry['id'],'repository':repo,'original_anchors':entry['original_anchors'],
            'actual_candidate_statements':candidates,
            'candidates_selected_by_existing_evidence_context_not_business_label':True,
            'actual_statement_and_operation_refs_checked':True,
            'semantic_sufficiency_not_inferred_from_candidate_count':True,
            'formal_original_row_completion':None})
    return rows


def additional_original_finite_clause_content(reports,architecture):
    """Actual later source scopes for original clauses, without a new score."""
    identifiers={'cpb-task-read-projection','wwc-delivery-evidence-frozen-contract-slice',
        'cpb-review-fixed-state-lineage','cpb-finalizer-conditional-publication',
        'wwc-document-device-provider-deployment-scope'}
    rows=[]
    for repo,report in reports.items():
        for index,chain in enumerate(report.get('functional_chains',[])):
            rid=chain.get('rule_id')
            if rid not in identifiers:continue
            bodies=[s for s in architecture[repo]['actual_statements'] if any(r.get('rule_id')==rid for r in s['source_evidence_refs'])]
            rows.append({'repository':repo,'rule_id':rid,'actual_chain_pointer':f'/functional_chains/{index}',
                'actual_chain':chain,'actual_derived_body_statements_with_checked_refs':bodies,
                'scope_selector_or_body_count_is_not_semantic_completion':True,'formal_original_clause_completion':None})
    return rows


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--directory',type=Path,default=HERE)
    ap.add_argument('--mode',choices=['formal','development'],default='formal')
    ap.add_argument('--contract',type=Path,default=HERE/'REPORT_COMPLETION_CONTRACT.json')
    ap.add_argument('--output',type=Path)
    ap.add_argument('--freeze',type=Path,default=HERE/'CORE_FREEZE.json')
    ap.add_argument('--repository',action='append',choices=['codepatchbay','winwincode'])
    args=ap.parse_args(); contract=json.loads(args.contract.read_text()); reports={}; manifest=[]; architecture={}; source_content={}; issues=[];seam_readbacks={};identities={}
    freeze=json.loads(args.freeze.read_text()) if args.mode=='formal' else None
    for repo in args.repository or ('codepatchbay','winwincode'):
        filename=(repo+'-automatic-report.json') if args.mode=='formal' else ('responsibility-explanations-'+repo+'-development.json')
        path=args.directory/filename
        if not path.exists():issues.append({'repository':repo,'missing_actual_input':str(path)});continue
        if args.mode=='formal':report,sha=load_formal(path)
        else:
            dev,sha=_SavedJSON(path).load(DEV_SELECTION)
            report={'architecture':{'responsibility_explanations':dev.get('explanations',{})},
                'snapshot':dev.get('explanations',{}).get('snapshot_identity',{}),'development_metadata':{k:v for k,v in dev.items() if k!='explanations'}}
        reports[repo]=report
        manifest.append({'repository':repo,'file':str(path),'sha256':sha,'mode':args.mode,'snapshot':report.get('snapshot'),
            'generating_components':report.get('report_components'),'development_metadata':report.get('development_metadata')})
        block=report.get('architecture',{}).get('responsibility_explanations',{})
        architecture[repo]=validate_architecture(block)
        source_content[repo]=critical_source_content(block,repo)
        if args.mode=='formal':
            seam_readbacks[repo]=validate_computed_seams(path,report,sha)
            identities[repo]=publication_identity_readback(report,freeze,repo)
    document_development=None
    if args.mode=='development' and 'winwincode' in reports and (args.directory/'documentation-source-query.json').exists():
        path=args.directory/'documentation-source-query.json'
        doc_selection={k:True for k in ('kind','rule','saved_snapshot_id','saved_source_hash','saved_policy_hash','module_sha256',
            'module_bytes_stable','formal_v14_publication','analysis_gaps','source_graph_bindings_closed','budget')}
        doc_selection.update({'pattern':PATTERN_SELECTION,'source_facts':[FACT_SELECTION]})
        document_development,sha=_SavedJSON(path).load(doc_selection)
        manifest.append({'repository':'winwincode','file':str(path),'sha256':sha,'mode':'development_document_comparison',
            'saved_snapshot_id':document_development.get('saved_snapshot_id'),'module_sha256':document_development.get('module_sha256'),
            'module_bytes_stable':document_development.get('module_bytes_stable')})
    result={'kind':'actual_saved_finite_report_content_readback','mode':args.mode,'inputs':manifest,
        'input_issues':issues,'responsibility_reference_validation':architecture,'critical_source_content':source_content,
        'formal_freeze_identity_and_scope_readback':identities,
        'prior_five_and_31_current_results':prior_entry_readback(contract,reports) if args.mode=='formal' else [],
        'additional_original_finite_clause_content':additional_original_finite_clause_content(reports,architecture),
        'original_responsibility_row_candidates':original_row_candidates(contract,reports,architecture),
        'documentation_aspects':documentation_readback(reports.get('winwincode',{}),document_development),
        'computed_source_contract_seams':{repo:report.get('architecture',{}).get('responsibility_explanations',{}).get('computed_source_contract_seams',[]) for repo,report in reports.items()},
        'computed_seam_actual_source_pointer_readback':seam_readbacks,
        'original_ten_domain_reconciliation':[{**g,'actual_v14_clause_readback':None} for g in contract['original_main_chain_reconciliation']],
        'completion_assessment':{'complete':False,'state':'actual_content_collected_requires_original_clause_reconciliation',
            'reason':'Reference validation and actual statements are evidence. Neither version, field presence nor candidate counts decide original finite content equivalence.'},
        'target_source_read':False,'database_read':False,'analyzer_run':False,'target_executed':False,'target_tests_run':False,'target_build_run':False,
        'astra_re_review_or_approval':False,'original_unreviewed_added_as_requirements':False}
    output=args.output or args.directory/('REPORT_COMPLETION_'+('FORMAL' if args.mode=='formal' else 'DEVELOPMENT')+'_READBACK.json')
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'output':str(output),'mode':args.mode,'input_issues':issues,
        'responsibility_ref_issues':{repo:len(r['reference_issues']) for repo,r in architecture.items()},
        'comparison_aspects':[len(r['actual_aspects']) for r in result['documentation_aspects']],
        'completion_inferred_from_counts':False},ensure_ascii=False))

if __name__=='__main__':main()
