"""Read saved JSON and source bytes only; never import CallScope or target code."""
import hashlib
import json
from pathlib import Path

ROOT = Path('/workspace/callscope')
TARGET = Path('/workspace/codepatchbay')
OUT = ROOT / 'reports/astra-iteration7/PRECISION_SOURCE_REVIEW_EVIDENCE.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked_location(location):
    if not location:
        return None
    path = TARGET / location['file']
    body = path.read_bytes()
    start, end = location['start_byte'], location['end_byte']
    return {
        'location': location,
        'actual_source_sha256': hashlib.sha256(body).hexdigest(),
        'source_sha256_matches': hashlib.sha256(body).hexdigest() == location['source_hash'],
        'range_within_source': 0 <= start <= end <= len(body),
        'span_sha256_matches': hashlib.sha256(body[start:end]).hexdigest() == location.get('span_hash'),
    }


result = {
    'kind': 'independent_source_only_precision_development_review',
    'date': '2026-10-12',
    'reviewer': 'Astra independent review agent',
    'method': 'Read frozen v8/v9 saved evidence and original source bytes; no analyzer or target import/execution, tests, builds, installs, CLI or browser.',
    'target_executed': False,
    'target_tests_run': False,
    'analyzer_executed_by_reviewer': False,
    'tool_test_suite_run': False,
    'formal_v10_result': False,
    'artifacts': [],
    'formal_field_sites': [],
    'selected_saved_source_facts': [],
    'source_files': [],
    'contract': {
        'path': 'reports/astra-iteration4/GOAL_ACCEPTANCE.md',
        'sha256': sha(ROOT / 'reports/astra-iteration4/GOAL_ACCEPTANCE.md'),
        'goals': 5,
        'necessary_obligations': 30,
        'contract_unchanged': True,
        'formal_v9_fully_supported_goals': 0,
        'field_fact_count_is_not_coverage': True,
    },
}

for iteration in (5, 6):
    rel = f'reports/astra-iteration{iteration}/field-assessments.json'
    artifact = ROOT / rel
    before = sha(artifact)
    data = json.loads(artifact.read_text())
    result['artifacts'].append({'path': rel, 'sha256': before})
    for fi, finding in enumerate(data['repositories'][0]['assessments']):
        details = finding['evidence'][0]['details']
        base = f'/repositories/0/assessments/{fi}/evidence/0/details'
        for ai, assessment in enumerate(details['assessments']):
            result['formal_field_sites'].append({
                'iteration': iteration,
                'artifact': rel,
                'json_pointer': f'{base}/assessments/{ai}',
                'rule_id': finding['rule_id'],
                'snapshot_id': finding['snapshot_id'],
                'source_location': checked_location(assessment['site_location']),
                'field_presence': assessment['field_presence'],
                'selected_field_shape_closed': assessment['selected_field_shape_closed'],
                'source_form_relation': assessment['source_form_relation'],
                'pre_completion_source_form_relation': assessment['pre_completion_source_form_relation'],
                'effect_count': assessment['effect_barrier_count'],
                'effect_sample_truncated': assessment['effect_barriers_truncated'],
            })
        if finding['rule_id'] != 'cpb-astra-field-engine-options':
            continue
        for si, fact in enumerate(details['source_facts']):
            op = fact['operation']
            line = fact['location']['line']
            selected = (
                op == 'object_rest_copy'
                or op == 'actual_helper_selected_return_summary' and line == 155
                or op == 'new_literal_object_shape' and fact.get('owner') == 'buildServices' and line == 85
                or iteration == 6 and op == 'bounded_external_value_domain' and line in (142, 143)
                or iteration == 6 and op in ('registered_actual_get_model', 'registered_effect_scope_guard') and line == 141
                or iteration == 6 and op == 'registered_effect_scope_guard' and line == 126
            )
            if selected:
                result['selected_saved_source_facts'].append({
                    'iteration': iteration,
                    'artifact': rel,
                    'json_pointer': f'{base}/source_facts/{si}',
                    'rule_id': finding['rule_id'],
                    'snapshot_id': finding['snapshot_id'],
                    'fact': fact,
                    'source_check': checked_location(fact['location']),
                })
    if sha(artifact) != before:
        raise RuntimeError('Frozen input changed during independent collection: ' + rel)

for rel in ('server/services/engine-runner.ts', 'server/services/agent/agent-config.ts', 'server/services/hub/hub-queue.ts'):
    result['source_files'].append({'repository': 'codepatchbay', 'path': rel, 'sha256': sha(TARGET / rel)})

freeze = json.loads((ROOT / 'reports/astra-iteration6/CORE_FREEZE.json').read_text())
result['v9_frozen_core_identity'] = {
    'tool_source_hash': freeze['tool_identity']['source_hash'],
    'modules': {name: freeze['package_source_sha256'][name] for name in ('field_summaries.py', 'semantic_ir.py')},
    'note': 'The source audit read these v9 functions before the parent began editing. Current source may already contain development fixes; final frozen-source review is pending.',
}
result['frozen_inputs_stable_during_collection'] = True
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'artifact': str(OUT), 'sha256': sha(OUT), 'sites': len(result['formal_field_sites']), 'selected_facts': len(result['selected_saved_source_facts'])}, ensure_ascii=False))
