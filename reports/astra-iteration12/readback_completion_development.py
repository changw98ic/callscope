"""Read saved development explanation artifacts; never run analysis or a DB."""
from pathlib import Path
import argparse
import json
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'astra-iteration11'))
from render_report_summaries import _SavedJSON

parser=argparse.ArgumentParser()
parser.add_argument('repository',choices=['codepatchbay','winwincode'])
args=parser.parse_args()
path=HERE/('responsibility-explanations-'+args.repository+'-development.json')
selection={
 'development_query':True,'not_formal_v14_result':True,'saved_snapshot_id':True,
 'saved_source_hash':True,'saved_policy_hash':True,'current_module_sha256':True,'query_module_bytes_stable':True,
 'explanations':{'version':True,'operation_extractor_version':True,'snapshot_identity':True,
  'assessment':True,'analysis_gaps':True,'explanation_source_gaps':True,'unreviewed_scope':True,
  'declaration_explanations':[{'id':True,'actual_owner':{'file':True,'symbol':True,'graph_node_id':True},
   'summary':True,'summary_statement_ids':True,'operation_count':True,'presentation_truncated':True,
   'statements':[{'id':True,'text':True,'operation_kind':True,'operation_id':True,'operation_pointer':True,
    'source_evidence_refs':[{'rule_id':True,'goal_id':True,'source_artifact_pointer':True,'fact_id':True,
      'reference_role':True,'old_finding_proves_new_operation':True}]}]}],
  'navigation':True,
  'explicit_source_transfers':[{'id':True,'kind':True,'text':True,'binding_state':True}],
  'authenticated_interface_reuse':[{'target_symbol':True,'target_graph_node_id':True,'source_scope':True,'god_object_inferred':True}],
  'communication_boundaries':{'ordinary_call_count_is_not_wire_coverage':True,'matching_literals_promoted_to_wire_connection':True},
 }}
value,digest=_SavedJSON(path).load(selection)
output={'kind':'saved_development_content_projection_not_completion','source_file':path.name,
 'source_file_sha256':digest,'saved_projection':value,'formal_publication':False,
 'semantic_original_row_coverage_computed':False,'all_original_propositions_completed':False,
 'database_opened':False,'analyzer_run':False,'target_executed':False,'target_tests_run':False,'target_build_run':False}
out=HERE/('COMPLETION_'+args.repository.upper()+'_DEVELOPMENT_PROJECTION.json')
out.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'artifact':out.name,'source_sha256':digest,
 'declarations':len(value['explanations']['declaration_explanations']),
 'assessment':value['explanations']['assessment'],
 'analysis_gaps':value['explanations']['analysis_gaps'],
 'explanation_source_gaps':len(value['explanations']['explanation_source_gaps'])},ensure_ascii=False))
