"""Normal source-model query over the real, closed v13 saved publication."""
import fcntl
import hashlib
import json
from pathlib import Path
import sqlite3

from callscope.report_chain_analysis import _Analysis
from callscope.semantic_sources import SemanticSources
from callscope.store import _snapshot_from_json

ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
MODULE=ROOT/'callscope/documentation_relations.py'
with (ROOT/'.analysis-tools/goal-source-query.lock').open('a') as lock:
 fcntl.flock(lock,fcntl.LOCK_EX)
 from callscope.documentation_relations import analyze_pattern, VERSION
 module_before=hashlib.sha256(MODULE.read_bytes()).hexdigest()
 database=ROOT/'reports/astra-iteration11/winwincode-v13.sqlite3'
 wal=Path(str(database)+'-wal')
 if wal.exists() and wal.stat().st_size:raise RuntimeError('Nonempty saved WAL')
 connection=sqlite3.connect('file:'+str(database)+'?mode=ro&immutable=1',uri=True)
 row=connection.execute('SELECT snapshot_json,detector_version,schema_version FROM snapshots ORDER BY sequence DESC LIMIT 1').fetchone()
 connection.close();snapshot=_snapshot_from_json(*row);del row
 rule=json.loads((OUT/'doc-rule.json').read_text());sources=SemanticSources(snapshot)
 analysis=_Analysis(snapshot,rule,sources);analysis.load()
 pattern=analyze_pattern(analysis)
 module_after=hashlib.sha256(MODULE.read_bytes()).hexdigest()
 if module_before!=module_after:raise RuntimeError('Documentation module changed while querying; refusing mixed-byte observation')
 result={'kind':'development_saved_source_document_comparison','version':VERSION,'formal_v14_publication':False,
  'saved_snapshot_id':snapshot.id,'saved_source_hash':snapshot.source_hash,'saved_policy_hash':snapshot.policy_hash,
  'new_rule_not_saved_in_old_snapshot':True,'module_sha256':module_before,'module_bytes_stable':True,
  'rule':rule,'rule_sha256':hashlib.sha256((OUT/'doc-rule.json').read_bytes()).hexdigest(),
  'pattern':pattern,'source_facts':analysis.source_facts,'analysis_gaps':analysis.gaps,
  'source_graph_bindings_closed':analysis.role_binding_closed,
  'budget':{'operations':analysis.operations,'incomplete':analysis.incomplete},
  'target_executed':False,'target_tests_run':False,'target_build_run':False}
 (OUT/'documentation-source-query.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'snapshot_id':snapshot.id,'supported':pattern['scoped_source_supported'],
  'witnesses':pattern['relation_witnesses'],'necessary_gaps':pattern['necessary_gaps'],
  'comparison':pattern['comparison'],'source_facts':len(analysis.source_facts),'budget':result['budget']},ensure_ascii=False),flush=True)
