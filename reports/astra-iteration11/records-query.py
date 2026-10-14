"""Ordinary source query over the immutable v0.12 CPB capture; no target IO."""
import ast
import hashlib
import json
from pathlib import Path
import sqlite3
import time
from callscope.store import _snapshot_from_json
from callscope.semantic_sources import SemanticSources
from callscope.report_chain_analysis import _Analysis
from callscope.record_projection_relations import analyze_pattern

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
ADAPTER_START = hashlib.sha256((ROOT / 'callscope/record_projection_relations.py').read_bytes()).hexdigest()
ast.parse((ROOT / 'callscope/record_projection_relations.py').read_text())
file_groups = {
 'event_index_projection': {
 'server/services/job/job-store.ts': {'mutation':'createJob','update':'updateJobsIndexEntry','index_writer':'writeJobsIndex','refresh':'getJobAndUpdateIndex','retry':'retryUpdate','rebuild':'rebuildJobsIndexLocked','rebuild_entry':'rebuildJobsIndex','list':'listJobsFromIndex','get_job':'getJob'},
 'server/services/event/event-store.ts': {'append':'appendEvent','durable_append':'appendSerializedEventDurably','projection':'readJobProjection','locked_projection':'withLockedJobProjection','serializer':'serializeEvent','event_reader':'readEvents'},
 'server/services/event/event-materializer.ts': {'materializer':'materializeJob'},
 'server/services/runtime.ts': {'divergence':'countJobsIndexDivergenceForRoot','classification':'classifyJobsIndexDivergence','health':'collectRuntimeHealth'},
 'cli/commands/doctor.ts': {'doctor':'checkRuntimeHealth'},
 },
 'trusted_command_lineage': {
 'core/workflow/probe-runner.ts': {'loader':'loadTrustedProbePolicy','resolver':'resolveDeclaredCommand','executor':'runDeclaredCommandOnce','command_runner':'runDeclaredCommand','runner':'runChecklistProbes','render':'renderProbeCommand','oracle_paths':'oracleProtectedPaths','oracle_changes':'changedOracleFiles'},
 'core/workflow/trusted-probe-policy.ts': {'policy_parser':'parseTrustedProbePolicy','spec_parser':'trustedProbeSpec'},
 },
 'unsupported_record_retention': {
 'core/workflow/probe-runner.ts': {'runner':'runChecklistProbes'},
 'core/workflow/evidence-probes.ts': {'plan':'buildEvidenceProbePlan','validation':'validateEvidenceObservation'},
 'core/phases/verify.ts': {'ledger':'buildEvidenceLedger','verification':'runVerify'},
 'core/artifacts/artifact-store.ts': {'artifact_writer':'writeArtifact'},
 }
}
rules=[]
for kind, groups in file_groups.items():
 sources=[{'role':role,'file':file,'symbol':symbol} for file, roles in groups.items() for role,symbol in roles.items()]
 rules.append({'id':'cpb-'+kind.replace('_','-'),'type':kind,'severity':'info','sources':sources,
  'models':['captured-normal-statement-control-v1','finite-record-codec-projection-source-v1'],
  'provenance':{'authority':'saved source locators','author_approved':False,'source_doc':'reports/astra-baseline/CODEPATCHBAY_ANALYSIS.md'},
  'applicability':{'kind':'conditional','conditions':['the selected captured source paths are reached normally; ordinary source record/JSON semantics'], 'counterexamples':['opaque execution, physical IO success and all inputs remain unproved']}})
for rule in rules:
 if rule['type'] == 'trusted_command_lineage':
  rule['models'].append('node-structured-execfile-source-contract-v1')
(HERE/'records-rules.json').write_text(json.dumps(rules,ensure_ascii=False,indent=2)+'\n')
connection=sqlite3.connect('file:'+str(ROOT/'reports/astra-iteration10/codepatchbay-v12.sqlite3')+'?mode=ro&immutable=1',uri=True)
row=connection.execute('SELECT snapshot_json,detector_version,schema_version FROM snapshots ORDER BY sequence DESC LIMIT 1').fetchone()
connection.close()
snapshot=_snapshot_from_json(*row)
del row
sources=SemanticSources(snapshot)
print('source_loaded',snapshot.id,flush=True)
for rule in rules:
 started=time.monotonic()
 analysis=_Analysis(snapshot,rule,sources)
 analysis.load()
 print('roles_loaded',rule['type'],len(analysis.roles),'gaps',analysis.gaps,flush=True)
 pattern=analyze_pattern(analysis)
 output={'version':pattern['version'],'snapshot_id':snapshot.id,'source_hash':snapshot.source_hash,
  'capture_tool_hash':snapshot.stats.get('component_versions',{}).get('tool',{}).get('source_hash'),
  'adapter_sha256':ADAPTER_START,
  'adapter_source_stable':ADAPTER_START == hashlib.sha256((ROOT/'callscope/record_projection_relations.py').read_bytes()).hexdigest(),
  'development_query':True,'formal_publication':False,'pattern':pattern,
  'source_facts':analysis.source_facts,'analysis_gaps':analysis.gaps,
  'source_scope':rule['sources'],'query_rule':rule,'query_rule_sha256':hashlib.sha256(json.dumps(rule,sort_keys=True,ensure_ascii=True,separators=(',',':')).encode()).hexdigest(),'operations':analysis.operations,'incomplete':analysis.incomplete,
  'target_executed':False,'target_tests_run':False,'target_build_run':False}
 (HERE/('records-'+rule['type']+'.json')).write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'type':rule['type'],'supported':pattern['scoped_source_supported'], 'witnesses':pattern['relation_witnesses'],
  'gaps':analysis.gaps,'facts':len(analysis.source_facts),'ops':analysis.operations,'seconds':round(time.monotonic()-started,2)},ensure_ascii=False),flush=True)
