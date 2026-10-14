"""Read captured v13 documentation and lexical declarations; never target code."""
import fcntl
import hashlib
import json
from pathlib import Path
import sqlite3

from callscope.store import _snapshot_from_json
from callscope.semantic_sources import SemanticSources

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
with (ROOT/'.analysis-tools/goal-source-query.lock').open('a') as lock:
 fcntl.flock(lock,fcntl.LOCK_EX)
 database=ROOT/'reports/astra-iteration11/winwincode-v13.sqlite3'
 wal=Path(str(database)+'-wal')
 if wal.exists() and wal.stat().st_size:raise RuntimeError('Saved publication still has WAL')
 connection=sqlite3.connect('file:'+str(database)+'?mode=ro&immutable=1',uri=True)
 row=connection.execute('SELECT snapshot_json,detector_version,schema_version FROM snapshots ORDER BY sequence DESC LIMIT 1').fetchone()
 connection.close()
 snapshot=_snapshot_from_json(*row);del row
 sources=SemanticSources(snapshot)
 result={'snapshot_id':snapshot.id,'source_hash':snapshot.source_hash,'policy_hash':snapshot.policy_hash,'saved_documentation':{},'source_roles':{},'target_executed':False}
 for path in ['docs/architecture.md']:
  record=snapshot.input_evidence.get(path,{})
  text=record.get('content','')
  result['saved_documentation'][path]={k:record.get(k) for k in ['status','hash','text_hash']}
  result['saved_documentation'][path]['selected_lines']=[{'line':i,'text':line} for i,line in enumerate(text.splitlines(),1) if 135<=i<=180]
 paths=['crates/winwincode-worker/src/device_model.rs','crates/winwincode-worker/src/main.rs','crates/winwincode-worker/src/lib.rs','crates/winwincode-provider/src/device_store.rs','crates/winwincode-provider/src/provider_anthropic.rs','crates/winwincode-provider/src/lib.rs','crates/winwincode-server/src/main.rs']
 for path in paths:
  document,issues=sources.load(path)
  entry={'issues':issues,'definitions':[]}
  if document:
   for symbol,definitions in document.definitions.items():
    for definition in definitions:
     if not definition.callable:continue
     node=definition.node
     text=document.text(node)
     selected=(any(term in text for term in ['credential','Credential','secret','Secret','api_key','API_KEY','Authorization','authorization','provider_directory']) and len(text)<45000) or symbol in ['DeviceModels.send','DeviceModels.open','WorkerMain.with_device_providers','run_worker','production_codex','<DeviceModelBoundary as winwincode_control_plane::DurableExecutionPortDelegate>.accept']
     if selected:
      entry['definitions'].append({'symbol':symbol,'graph_node_id':definition.graph_node_id,'location':document.location(node),'source':text[:45000]})
  result['source_roles'][path]=entry
 (OUT/'DOCUMENTATION_SOURCE_DISCOVERY.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'snapshot_id':snapshot.id,'doc':result['saved_documentation'],'roles':{path:[item['symbol'] for item in e['definitions']] for path,e in result['source_roles'].items()}},ensure_ascii=False),flush=True)
