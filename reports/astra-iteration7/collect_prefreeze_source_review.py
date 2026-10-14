"""Collect source-only review evidence from already saved development JSON."""
import hashlib
import json
from pathlib import Path

ROOT = Path('/workspace/callscope')
TARGET = Path('/workspace/codepatchbay')
INPUT = ROOT / 'reports/astra-iteration7/RUNTIME_CAPTURE_DEVELOPMENT.json'
OUT = ROOT / 'reports/astra-iteration7/PREFREEZE_PRECISION_SOURCE_REVIEW_EVIDENCE.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


input_hash = sha(INPUT)
data = json.loads(INPUT.read_text())
output = {
    'kind': 'independent_source_only_prefreeze_precision_review',
    'date': '2026-10-12',
    'reviewer': 'Astra independent review agent',
    'method': 'Read current source text, saved development JSON, and target source bytes only.',
    'analyzer_or_target_executed_by_reviewer': False,
    'tool_or_target_tests_run': False,
    'formal_frozen_result': False,
    'prefreeze_source_blocker_found': False,
    'development_input': {'path': str(INPUT.relative_to(ROOT)), 'sha256': input_hash,
        'tool_identity': data.get('current_query_tool_identity')},
    'reviewed_candidate_modules': [
        {'path': name, 'sha256': sha(ROOT / name)}
        for name in ('callscope/field_summaries.py', 'callscope/semantic_ir.py')
    ],
    'identity_caveat': 'Development query predates final constructor/cell-owner evidence changes; its identity is not the later frozen tool identity.',
    'contract': {'goals': 5, 'necessary_obligations': 30,
        'sha256': sha(ROOT / 'reports/astra-iteration4/GOAL_ACCEPTANCE.md'),
        'field_site_or_fact_counts_are_not_goal_coverage': True},
    'sites': [], 'selected_engine_facts': [], 'source_checks': [],
}

for oi, observation in enumerate(data['observations']):
    summary = observation['summary']
    for ai, assessment in enumerate(summary['assessments']):
        base = f'/observations/{oi}/summary/assessments/{ai}'
        result = {key: assessment.get(key) for key in (
            'site_location', 'field_presence', 'selected_field_shape_closed',
            'whole_object_shape_closed', 'source_form_relation',
            'pre_completion_source_form_relation', 'analysis_phase',
            'reaching_value_origin_proven', 'opaque_effects_or_exceptions_excluded',
            'runtime_value_verified', 'conditions', 'gaps')}
        result.update(rule=observation['rule'], json_pointer=base,
            transport_proven=summary['transport_proven'],
            full_functionality_proven=summary['full_functionality_proven'])
        if observation['rule'] == 'cpb-astra-field-engine-options':
            result.update({key: assessment.get(key) for key in (
                'field_sources', 'copy_steps', 'ir_selected_value', 'completion', 'formal')})
        output['sites'].append(result)
    if observation['rule'] != 'cpb-astra-field-engine-options':
        continue
    output['engine_source_assumptions'] = summary['source_assumptions']
    for fi, fact in enumerate(summary['source_facts']):
        op, line = fact['operation'], fact['location']['line']
        if (op == 'object_rest_copy'
            or op == 'actual_helper_selected_return_summary' and line == 155
            or op == 'new_literal_object_shape' and line in (85, 157)
            or op == 'ordered_object_spread' and line in (158, 176)):
            output['selected_engine_facts'].append({
                'json_pointer': f'/observations/{oi}/summary/source_facts/{fi}', 'fact': fact})

seen = set()


def check_refs(value):
    if isinstance(value, dict):
        if all(key in value for key in ('file', 'source_hash', 'start_byte', 'end_byte')):
            key = (value['file'], value['source_hash'], value['start_byte'], value['end_byte'], value.get('span_hash'))
            if key not in seen:
                seen.add(key)
                raw = (TARGET / value['file']).read_bytes()
                start, end = value['start_byte'], value['end_byte']
                span_hash = hashlib.sha256(raw[start:end]).hexdigest()
                output['source_checks'].append({
                    'file': value['file'], 'start_byte': start, 'end_byte': end,
                    'source_sha256_matches': hashlib.sha256(raw).hexdigest() == value['source_hash'],
                    'range_within_source': 0 <= start <= end <= len(raw),
                    'span_sha256': span_hash,
                    'saved_span_hash_matches': span_hash == value['span_hash'] if 'span_hash' in value else None,
                })
        for child in value.values():
            check_refs(child)
    elif isinstance(value, list):
        for child in value:
            check_refs(child)


check_refs(output['sites'])
check_refs(output['selected_engine_facts'])
output['all_checked_source_refs_match'] = all(item['source_sha256_matches'] and item['range_within_source']
    and item['saved_span_hash_matches'] is not False for item in output['source_checks'])
output['saved_input_unchanged_during_collection'] = sha(INPUT) == input_hash
OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'artifact': str(OUT), 'sha256': sha(OUT),
    'source_refs_checked': len(output['source_checks']),
    'all_checked_source_refs_match': output['all_checked_source_refs_match'],
    'saved_input_unchanged_during_collection': output['saved_input_unchanged_during_collection']}))
