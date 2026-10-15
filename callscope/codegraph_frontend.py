"""Adapt pinned CodeGraph extractors to captured-source structural evidence.

Only the shipped analysis worker is executed. Target paths, modules, commands,
package hooks and tests are never passed to an executable loader. Upstream
resolution is candidate evidence, not a new source of certain CALLS.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import replace
from functools import lru_cache
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

from .models import Diagnostic, Edge, Node

ANALYZER_VERSION = 'codegraph-captured-structure-1'
PROTOCOL = 'callscope-codegraph-1'
VENDOR = Path(__file__).resolve().parent / '_vendor/codegraph'


def _hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def component_versions() -> dict:
    manifest = json.loads((VENDOR / 'UPSTREAM.json').read_text())
    try:
        node_version = _node_version()
    except (OSError, RuntimeError, subprocess.SubprocessError):
        # Unused registered frontends must not make a native-only scan fail.
        # Active CodeGraph inputs still require ensure_runtime before analysis.
        node_version = 'unavailable'
    return {'analyzer': ANALYZER_VERSION, 'parser': 'codegraph-wasm-0.25.10',
            'upstream_commit': manifest['commit'], 'protocol': PROTOCOL,
            'node_runtime': node_version,
            'bridge_sha256': _hash((VENDOR / 'worker.cjs').read_bytes()),
            'resolution_level': 'upstream_candidates_only'}


@lru_cache(maxsize=1)
def _node_version() -> str:
    node = shutil.which('node')
    if not node:
        raise RuntimeError('CodeGraph frontend requires Node.js >=20,<25')
    result = subprocess.run([node, '--version'], cwd=VENDOR, env=_environment(),
                            capture_output=True, text=True, timeout=20, check=True)
    return result.stdout.strip()


@lru_cache(maxsize=1)
def ensure_runtime() -> str:
    node = shutil.which('node')
    if not node or not (VENDOR / 'worker.cjs').is_file():
        raise RuntimeError('CodeGraph frontend requires Node.js >=20,<25 and the shipped worker.cjs')
    try:
        major = int(_node_version().lstrip('v').split('.')[0])
    except ValueError as error:
        raise RuntimeError('Unable to identify the analysis-tool Node.js runtime') from error
    if not 20 <= major < 25:
        raise RuntimeError('CodeGraph frontend requires Node.js >=20,<25')
    return node


def _environment():
    environment = dict(os.environ)
    # Never inherit arbitrary Node startup hooks or project module paths. All
    # proxy/authentication variables retain their inherited values.
    for name in ('NODE_OPTIONS', 'NODE_PATH'):
        environment.pop(name, None)
    environment['CODEGRAPH_KERNEL'] = '0'
    return environment


def runtime_capabilities() -> dict:
    result = subprocess.run([ensure_runtime(), str(VENDOR / 'worker.cjs'), '--capabilities'],
                            cwd=VENDOR, env=_environment(), capture_output=True, text=True,
                            timeout=120, check=True)
    value = json.loads(result.stdout)
    if value.get('protocol') != PROTOCOL:
        raise RuntimeError('CodeGraph runtime capability protocol mismatch')
    return value


def _payload_source(path, content, digest=''):
    return {'path': path, 'content': content, 'hash': digest,
            'text_hash': _hash(content.encode('utf-8'))}


def classify_files(files):
    """Use the unmodified upstream content classifier on captured text only."""
    sources = [{**_payload_source(source.path, source.content, source.hash), 'language': source.language}
               for source in files]
    payload = json.dumps({'files': sources, 'inputs': []}, ensure_ascii=False,
                         sort_keys=True, separators=(',', ':'), allow_nan=False)
    fingerprint = _hash(payload.encode())
    request = json.dumps({'protocol': PROTOCOL, 'payload': payload, 'sha256': fingerprint}, ensure_ascii=False)
    result = subprocess.run([ensure_runtime(), str(VENDOR / 'worker.cjs'), '--classify'], input=request,
                            cwd=VENDOR, env=_environment(), capture_output=True, text=True,
                            encoding='utf-8', timeout=120, check=True)
    data = json.loads(result.stdout)
    expected = {source.path: source.hash for source in files}
    records = data.get('files', [])
    if (data.get('protocol') != PROTOCOL or data.get('request_hash') != fingerprint
            or data.get('upstream_commit') != component_versions()['upstream_commit']
            or len(records) != len(expected)
            or {item['path']: item['hash'] for item in records} != expected):
        raise RuntimeError('CodeGraph classifier input/output identity mismatch')
    return {item['path']: item['upstream_language'] for item in records}


def _byte_column(content: str, line: int, utf16_column: int) -> int:
    lines = content.split('\n')
    if not 1 <= line <= len(lines):
        return 0
    data = lines[line - 1].encode('utf-16-le', errors='surrogatepass')[:max(0, utf16_column) * 2]
    return len(data.decode('utf-16-le', errors='ignore').encode('utf-8'))


def analyze_files(files, project_root: Path, policy: dict):
    language = files[0].language
    selected = [source for source in files if source.status == 'captured']
    if not selected:
        return {'nodes': [], 'edges': [], 'files': files, 'diagnostics': [], 'stats': {}}
    sources = [_payload_source(source.path, source.content, source.hash) for source in selected]
    support = policy['analysis'].get('_captured_codegraph_inputs', {})
    inputs = [_payload_source(p, item['content'], item['hash']) for p, item in sorted(support.items())
              if item.get('status') == 'captured']
    payload = json.dumps({'language': language, 'files': sources, 'inputs': inputs},
                         ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)
    fingerprint = _hash(payload.encode('utf-8'))
    request = json.dumps({'protocol': PROTOCOL, 'payload': payload, 'sha256': fingerprint}, ensure_ascii=False)
    try:
        result = subprocess.run([ensure_runtime(), str(VENDOR / 'worker.cjs')], input=request,
                                cwd=VENDOR, env=_environment(), capture_output=True, text=True,
                                encoding='utf-8', timeout=600, check=False)
    except (OSError, subprocess.SubprocessError) as error:
        raise RuntimeError(f'CodeGraph analysis-tool process unavailable: {error}') from error
    if result.returncode:
        raise RuntimeError('CodeGraph analysis-tool process failed: ' + result.stderr[-4000:])
    try:
        data = json.loads(result.stdout)
    except (ValueError, UnicodeError) as error:
        raise RuntimeError('CodeGraph analysis-tool returned invalid JSON') from error
    if (data.get('protocol') != PROTOCOL or data.get('request_hash') != fingerprint
            or data.get('upstream_commit') != component_versions()['upstream_commit']):
        raise RuntimeError('CodeGraph worker protocol/source/request identity mismatch')
    expected = {source.path: source for source in selected}
    returned = {item['path']: item for item in data['files']}
    if set(returned) != set(expected) or len(returned) != len(data['files']):
        raise RuntimeError('CodeGraph worker changed the captured file set')
    for path, record in returned.items():
        if record.get('hash') != expected[path].hash:
            raise RuntimeError('CodeGraph worker source identity mismatch')
    diagnostics = []
    identities = {}
    duplicates = Counter(item['id'] for item in data['nodes'])
    raw_by_id = {item['id']: item for item in data['nodes']}
    nodes = []
    for identifier, item in sorted(raw_by_id.items()):
        source = expected.get(item['filePath'])
        if source is None:
            raise RuntimeError('CodeGraph node points outside the captured source set')
        node_id = f'cg:{language}:{identifier}'
        identities[identifier] = node_id
        name = item.get('name', '')
        qualname = f"{language}:{source.path}#{item.get('qualifiedName', name)}"
        metadata = {'language': language, 'upstream_language': item['language'],
                    'source_hash': source.hash, 'frontend': 'codegraph',
                    'upstream_id': identifier, 'upstream_kind': item['kind'],
                    'upstream_commit': data['upstream_commit'],
                    'column': _byte_column(source.content, item['startLine'], item.get('startColumn', 0)),
                    'upstream_column_utf16': item.get('startColumn', 0),
                    'call_resolution_model': 'upstream_candidate_only',
                    'is_async': item.get('isAsync', False), 'is_static': item.get('isStatic', False),
                    'visibility': item.get('visibility'), 'return_type': item.get('returnType'),
                    'duplicate_definition': duplicates[identifier] > 1}
        nodes.append(Node(node_id, name, qualname, f'{language}:{source.path}', source.path,
                          item['startLine'], item.get('endLine', item['startLine']),
                          'module' if item['kind'] == 'file' else item['kind'],
                          item.get('signature', ''), metadata=metadata))
    by_id = {node.id: node for node in nodes}
    edges = []
    non_call_relations = 0
    candidate_count = 0
    for index, ref in enumerate(data['references']):
        owner_id = identities.get(ref['fromNodeId'])
        if owner_id is None:
            diagnostics.append(Diagnostic('warning', 'codegraph_missing_owner',
                                          'Upstream reference owner was not captured', ref['filePath'], ref['line']))
            continue
        source = expected[ref['filePath']]
        candidates = sorted({identities[c['target']] for c in ref['candidates'] if c['target'] in identities})
        detail = {'frontend': 'codegraph', 'source_hash': source.hash,
                  'relation_kind': ref['referenceKind'], 'upstream_commit': data['upstream_commit'],
                  'candidate_only': True, 'upstream_column_utf16': ref.get('column', 0),
                  'upstream_candidates': ref['candidates'],
                  'confidence_meaning': 'upstream ranking, not proof or measured correctness probability'}
        candidate_count += len(candidates)
        if ref['referenceKind'] not in {'calls', 'instantiates', 'function_ref'}:
            non_call_relations += 1
            by_id[owner_id].metadata.setdefault('codegraph_relations', []).append({
                'kind': ref['referenceKind'], 'expression': ref['referenceName'],
                'line': ref['line'], 'candidates': candidates, **detail})
            continue
        edge_id = 'edge:cg:' + _hash(f'{language}\0{source.path}\0{index}\0{owner_id}\0{ref["referenceName"]}'.encode())[:28]
        edges.append(Edge(edge_id, owner_id, None, ref['referenceName'], source.path,
                          ref['line'], _byte_column(source.content, ref['line'], ref.get('column', 0)),
                          'ambiguous' if candidates else 'dynamic', candidates,
                          'CodeGraph supplied candidate relations; no deterministic binding proof' if candidates
                          else 'CodeGraph could not bind this source reference within captured inputs', detail))
    for relation in data['structural_edges']:
        owner = by_id.get(identities.get(relation['source']))
        if owner is not None:
            owner.metadata.setdefault('codegraph_structure', []).append(relation)
    final_files = []
    for source in files:
        record = returned.get(source.path)
        if record is None:
            final_files.append(source)
            continue
        status = record['status']
        if status not in {'parsed', 'parse_error', 'captured_metadata', 'structural_extracted'}:
            raise RuntimeError('Unexpected CodeGraph parser status')
        messages = '; '.join(item['message'] for item in record.get('errors', []))
        if status == 'parse_error':
            messages = messages or 'Upstream grammar has syntax errors; retained structural/candidate evidence is partial'
            diagnostics.append(Diagnostic('warning', 'codegraph_syntax_partial', messages, source.path))
        elif status == 'captured_metadata':
            messages = 'File/metadata tracking only; this input has no general symbol-level parser'
            diagnostics.append(Diagnostic('info', 'codegraph_metadata_only', messages, source.path))
        elif status == 'structural_extracted':
            messages = 'Custom/template structural extraction; complete embedded syntax validation is not established'
            diagnostics.append(Diagnostic('info', 'codegraph_structural_only', messages, source.path))
        final_files.append(replace(source, status=status, error=messages or None,
                                   module=f'{language}:{source.path}'))
    resolution_errors = data.get('resolution_errors', [])
    for error in resolution_errors[:20]:
        diagnostics.append(Diagnostic('warning', 'codegraph_resolution_partial', error['message'],
                                      error['file'], error['line']))
    if any(count > 1 for count in duplicates.values()):
        diagnostics.append(Diagnostic('warning', 'codegraph_duplicate_symbols',
                                      'Upstream repeated symbol identities are marked duplicate; candidate relations remain uncertain'))
    return {'nodes': nodes, 'edges': edges, 'files': final_files, 'diagnostics': diagnostics,
            'stats': {'analyzer_version': ANALYZER_VERSION, 'upstream_commit': data['upstream_commit'],
                      'coverage_incomplete': any(s.status != 'parsed' for s in final_files),
                      'call_resolution_incomplete': bool(data['references']),
                      'candidate_relations': candidate_count, 'non_call_relations': non_call_relations,
                      'resolution_errors': len(resolution_errors),
                      'structural_extraction': True, 'deterministic_call_binding': False,
                      'boundaries': data['boundaries'], 'project_reads': data['project_reads'],
                      'target_executed': False, 'native_kernel_used': False}}
