"""Normal static source query against the two actual WWC crate entries.

No target imports, Cargo, executables, build, tests, fixtures, or DB reads.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys
from callscope.input_capture import capture_support_inputs
from callscope.rust_analyzer import analyze_files, ANALYZER_VERSION
from callscope.source_reader import scan_sources

ROOT = Path('/workspace/winwincode')
POLICY = Path('reports/astra-iteration10/winwincode-policy.json')
SELECTORS = {
 'crates/winwincode-worker/src/main.rs': {'main', 'run_remote', 'run_managed', 'run_worker', 'production_codex'},
 'crates/winwincode-worker/src/lib.rs': {'WorkerMain.new', 'WorkerMain.with_device_providers'},
 'crates/winwincode-worker/src/device_model.rs': {'DeviceModels.open'},
 'crates/winwincode-server/src/main.rs': {'<DeviceModelBoundary as winwincode_control_plane::DurableExecutionPortDelegate>.accept'},
}
policy = json.loads(POLICY.read_text())
files, diagnostics, scope = scan_sources(ROOT, policy)
support, support_diagnostics = capture_support_inputs(ROOT, policy['analysis']['support_inputs'], policy['analysis']['max_file_bytes'])
policy['analysis']['_captured_support_inputs'] = support
rust_files = [item for item in files if item.language == 'rust']
result = analyze_files(rust_files, ROOT, policy)
selected = [node for node in result['nodes'] if node.file in SELECTORS and node.qualname.split('#', 1)[-1] in SELECTORS[node.file]]
selected_ids = {node.id for node in selected}
record = {
 'query_kind': 'actual_repository_captured_rust_static_analysis',
 'analyzer_version': ANALYZER_VERSION,
 'rust_analyzer_sha256': hashlib.sha256(Path('callscope/rust_analyzer.py').read_bytes()).hexdigest(),
 'policy_file_sha256': hashlib.sha256(POLICY.read_bytes()).hexdigest(),
 'target_execution_performed': False, 'tests_or_fixtures_performed': False,
 'scope': scope, 'capture_diagnostic_count': len(diagnostics) + len(support_diagnostics),
 'rust_source_inputs': [{'file': item.path, 'sha256': item.hash, 'status': item.status} for item in result['files']],
 'stats': result['stats'],
 'selected_declarations': [{'id': node.id, 'file': node.file, 'line': node.line, 'end_line': node.end_line, 'kind': node.kind, 'metadata': node.metadata} for node in selected],
 'selected_call_sites': [{'id': edge.id, 'source': edge.source, 'target': edge.target, 'file': edge.file, 'line': edge.line, 'expression': edge.expression, 'resolution': edge.resolution, 'reason': edge.reason, 'metadata': edge.metadata} for edge in result['edges'] if edge.source in selected_ids],
 'remaining_opaque_declarations': [{'id': node.id, 'file': node.file, 'line': node.line, 'attributes': node.metadata.get('attributes'), 'cfg_conditions': node.metadata.get('cfg_conditions')} for node in result['nodes'] if node.metadata.get('attribute_macros_unknown')],
 'conditional_declaration_count': sum(bool(node.metadata.get('conditional_definition')) for node in result['nodes']),
}
if '--report-claims' in sys.argv[2:]:
 from datetime import datetime, timezone
 from callscope.models import GraphSnapshot, project_id_for
 from callscope.report_chain_analysis import _Analysis
 from callscope.semantic_sources import SemanticSources
 def digest(value):
  return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()).hexdigest()
 source_hash = digest(record['rust_source_inputs'])
 policy_hash = hashlib.sha256(POLICY.read_bytes()).hexdigest()
 # A development-only query domain, explicitly distinct from any published
 # multi-language snapshot. All graph records come from analyze_files above.
 snapshot = GraphSnapshot(id='development-rust-source-query-' + digest([source_hash, policy_hash, ANALYZER_VERSION]),
  project_id=project_id_for(ROOT), project_name='WinWinCode Rust source-context development query',
  root=str(ROOT), created_at=datetime.now(timezone.utc).isoformat(), source_hash=source_hash,
  analyzer_version=ANALYZER_VERSION, policy_hash=policy_hash, status='development_source_query',
  nodes=result['nodes'], edges=result['edges'], files=result['files'], diagnostics=result['diagnostics'],
  stats={'component_versions': {'rust': {'analyzer': ANALYZER_VERSION, 'parser': result['stats']['parser_version']}}},
  config=policy, input_evidence=support)
 sources = SemanticSources(snapshot)
 rule_ids = {'wwc-report-device-provider-deployment', 'wwc-report-worker-bootstrap-entries', 'wwc-report-worker-production-construction'}
 rules = json.loads(Path('reports/astra-iteration10/report-claims-rule.json').read_text())['winwincode']
 if isinstance(rules, dict):
  rules = rules['report_claims']
 record['development_report_claims'] = []
 for rule in rules:
  if rule['id'] in rule_ids:
   details = _Analysis(snapshot, rule, sources).analyze()
   record['development_report_claims'].append({'id': rule['id'], 'details': details})
 record['query_snapshot_domain'] = {'id': snapshot.id, 'formal_publication': False,
  'scope': 'same actual Rust source capture, not a saved full multi-language snapshot'}
 record['source_context_module_sha256'] = hashlib.sha256(Path('callscope/rust_source_context.py').read_bytes()).hexdigest()
output = Path(sys.argv[1])
with output.open('x') as stream:
 json.dump(record, stream, ensure_ascii=False, indent=2)
 stream.write('\n')
print(json.dumps({'output': str(output), 'rust_files': len(rust_files), 'selected_declarations': len(selected), 'selected_opaque': sum(bool(node.metadata.get('attribute_macros_unknown')) for node in selected), 'stats': result['stats']}, ensure_ascii=False))
