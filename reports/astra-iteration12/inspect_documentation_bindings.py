"""Inspect the selected real saved graph metadata and Rust CST shapes."""
import fcntl,json,sqlite3
from pathlib import Path
from callscope.store import _snapshot_from_json
from callscope.semantic_sources import SemanticSources
from callscope.report_chain_analysis import _Analysis
from callscope.documentation_relations import _Documents,_f,_c
root=Path(__file__).resolve().parents[2];out=Path(__file__).resolve().parent
with (root/'.analysis-tools/goal-source-query.lock').open('a') as lock:
 fcntl.flock(lock,fcntl.LOCK_EX)
 db=root/'reports/astra-iteration11/winwincode-v13.sqlite3'
 wal=Path(str(db)+'-wal')
 if wal.exists() and wal.stat().st_size:raise RuntimeError('Nonempty WAL')
 connection=sqlite3.connect('file:'+str(db)+'?mode=ro&immutable=1',uri=True)
 row=connection.execute('SELECT snapshot_json,detector_version,schema_version FROM snapshots ORDER BY sequence DESC LIMIT 1').fetchone();connection.close()
 snapshot=_snapshot_from_json(*row);del row
 sources=SemanticSources(snapshot);analysis=_Analysis(snapshot,json.loads((out/'doc-rule.json').read_text()),sources);analysis.load();reader=_Documents(analysis)
 result={'snapshot_id':snapshot.id,'roles':{},'target_executed':False}
 for role,(document,definition,function) in analysis.roles.items():
  record={'selected':[],'calls':[],'shapes':[]}
  for selected in sources.nodes.get(definition.graph_node_id,[]):record['selected'].append({'id':selected.id,'name':selected.name,'kind':selected.kind,'metadata':selected.metadata})
  if role in {'device_send','model_execute','model_invoke'}:
   for call in reader.calls(role,nested=True):
    if reader.call_name(document,call) not in {'open','execute_model','invoke_model','resolve'}:continue
    record['calls'].append({'text':document.text(call),'type':call.type,'function_type':_f(call,'function').type,'fields':{key:document.text(_f(_f(call,'function'),key)) for key in ['value','path','name','field']},'parent_type':call.parent.type,'bindings':{target:reader.binding(role,call,target) for target in ['store_open','model_execute','model_invoke','secret_resolver'] if reader.call_name(document,call)==reader.name(target)}})
  if role in {'secret_constructor','secret_resolver','provider_factory','provider_open'}:
   for node in reader.nodes(role,nested=True):
    if node.type in {'tuple_expression','struct_expression','field_initializer','shorthand_field_initializer','closure_expression','parameter','field_expression'}:
     record['shapes'].append({'type':node.type,'source':document.text(node),'fields':{key:document.text(_f(node,key)) for key in ['name','type','value','field','body','parameters']},'children':[{'type':n.type,'source':document.text(n)} for n in _c(node)]})
  result['roles'][role]=record
 identifiers={identifier for edge in snapshot.edges if edge.id in {'rust-call:c8b67b3b002a1d9843692e6f','rust-call:5ecd82438458e871abb66487'} for identifier in edge.candidates}
 result['candidate_nodes']=[{'id':node.id,'name':node.name,'kind':node.kind,'metadata':node.metadata} for node in snapshot.nodes if node.id in identifiers]
 (out/'DOCUMENTATION_BINDING_INSPECTION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print('Selected saved graph and CST inspection complete',flush=True)
