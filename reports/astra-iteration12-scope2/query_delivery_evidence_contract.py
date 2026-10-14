"""Normal new-rule Finding and report from the real closed v13 WWC source.

No synthetic Finding, target worktree access, target imports or target execution.
This scope-only development query never rewrites a saved snapshot or a policy.
"""
import fcntl
import hashlib
import json
from pathlib import Path
import sqlite3

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
PUBLICATION=ROOT/'reports/astra-iteration12'
PREFIX='winwincode-delivery-evidence-contract'

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def inventory():return {path.relative_to(ROOT/'callscope').as_posix():digest(path) for path in sorted((ROOT/'callscope').rglob('*.py'))}

with (ROOT/'.analysis-tools/goal-source-query.lock').open('a') as lock:
 fcntl.flock(lock,fcntl.LOCK_EX)
 outputs={kind:OUT/(PREFIX+suffix) for kind,suffix in [('query','-query.json'),('report','-report.json'),('markdown','-report.md')]}
 if any(path.exists() for path in outputs.values()):raise FileExistsError('Development outputs already exist; no overwrite')
 before=inventory();freeze=json.loads((PUBLICATION/'CORE_FREEZE.json').read_text())
 if before!=freeze['package_source_sha256']:raise RuntimeError('Core differs from the existing frozen source inventory')
 # Only the trusted analyzer is imported after serialization and identity check.
 from dataclasses import asdict
 from callscope.report_chain_analysis import analyze_report_claims,validate_report_claim
 from callscope.project_report import build_project_report,render_markdown
 from callscope.store import _snapshot_from_json
 database=ROOT/'reports/astra-iteration11/winwincode-v13.sqlite3'
 wal=Path(str(database)+'-wal')
 if wal.exists() and wal.stat().st_size:raise RuntimeError('Closed saved publication has a nonempty WAL')
 connection=sqlite3.connect('file:'+str(database)+'?mode=ro&immutable=1',uri=True)
 row=connection.execute('SELECT snapshot_json,detector_version,schema_version FROM snapshots ORDER BY sequence DESC LIMIT 1').fetchone();connection.close()
 snapshot=_snapshot_from_json(*row);del row
 if snapshot.id!='cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2':raise RuntimeError('Unexpected saved snapshot')
 print('saved_source_loaded',snapshot.id,flush=True)
 rule_path=OUT/'delivery-evidence-contract-rule.json';rule=json.loads(rule_path.read_text());validate_report_claim(rule)
 findings=analyze_report_claims(snapshot,[rule])
 print('normal_finding_generated',len(findings),flush=True)
 report=build_project_report(snapshot,findings);markdown=render_markdown(report)
 after=inventory()
 if before!=after:raise RuntimeError('Frozen core changed during the development query')
 if report['snapshot']['id']!=snapshot.id or report['snapshot']['policy_hash']!=snapshot.policy_hash:raise RuntimeError('Report changed the old snapshot identity')
 for kind,value in [('report',report)]:
  with outputs[kind].open('x',encoding='utf-8') as stream:json.dump(value,stream,ensure_ascii=False,indent=2);stream.write('\n')
 with outputs['markdown'].open('x',encoding='utf-8') as stream:stream.write(markdown)
 details=findings[0].evidence[0].details
 query={'kind':'normal_new_rule_saved_source_development_query','formal_scope2_publication':False,'snapshot_id':snapshot.id,'source_hash':snapshot.source_hash,'saved_policy_hash':snapshot.policy_hash,'old_snapshot_or_policy_modified':False,'new_rule_saved_in_old_snapshot':False,'new_rule_sha256':digest(rule_path),'new_rule':rule,'normal_analyze_report_claims_called':True,'normal_build_project_report_called':True,'normal_render_markdown_called':True,'new_findings_generated_from_actual_sources':True,'finding_or_fixture_records_simulated':False,'only_this_rule_analyzed':True,'full_previous_scope_recomputed':False,'current_core_tool_identity':freeze['tool_identity'],'current_core_source_count':len(before),'frozen_core_bytes_stable':before==after,'current_core_source_sha256':before,'findings':[asdict(finding) for finding in findings],'report':{'file':outputs['report'].name,'sha256':digest(outputs['report'])},'markdown':{'file':outputs['markdown'].name,'sha256':digest(outputs['markdown']),'line_count':len(markdown.splitlines()),'normal_renderer_exact_output':True},'target_executed':False,'target_imported':False,'target_tests_run':False,'target_build_run':False,'tool_test_suite_run':False}
 with outputs['query'].open('x',encoding='utf-8') as stream:json.dump(query,stream,ensure_ascii=False,indent=2);stream.write('\n')
 print(json.dumps({'rule_id':rule['id'],'snapshot_id':snapshot.id,'assessment':details['assessment'],'scope':details['scope'],'facts':len(details['source_facts']),'analysis_gaps':details['analysis_gaps'],'budgets':details['budgets'],'query_sha256':digest(outputs['query']),'normal_report_sha256':digest(outputs['report']),'normal_markdown_lines':len(markdown.splitlines()),'current_core_source_count':len(before),'frozen_core_bytes_stable':before==after},ensure_ascii=False),flush=True)
