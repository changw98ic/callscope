"""Independent review of saved v11 artifacts and original source bytes only.

No analyzer or target import, scan, test, build, installation, or target CLI.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path('/workspace/callscope')
HERE = Path(__file__).resolve().parent
PREVIOUS = ROOT / 'reports/astra-iteration8'
ARTIFACTS = {}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    ARTIFACTS[str(path.relative_to(ROOT))] = sha(path)
    return json.loads(path.read_text())


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


freeze = load(HERE / 'CORE_FREEZE.json')
old_freeze = load(PREVIOUS / 'CORE_FREEZE.json')
package = ROOT / 'callscope'
package_checks = []
aggregate = hashlib.sha256()
for path in sorted(package.rglob('*.py')):
    name = path.relative_to(package).as_posix()
    body = path.read_bytes()
    aggregate.update(name.encode())
    aggregate.update(b'\0')
    aggregate.update(body)
    aggregate.update(b'\0')
    actual = hashlib.sha256(body).hexdigest()
    package_checks.append({'file': name, 'sha256': actual,
        'matches_freeze': actual == freeze['package_source_sha256'].get(name),
        'frozen_archive_matches_freeze': sha(HERE / 'frozen-core-source' / name) == freeze['package_source_sha256'].get(name),
        'unchanged_from_v10': actual == old_freeze['package_source_sha256'].get(name)})

result = {
    'kind': 'independent_frozen_source_and_saved_artifact_review',
    'reviewer': 'Astra independent review agent',
    'date': '2026-10-13',
    'date_timezone': 'Asia/Shanghai',
    'method': 'Read frozen source, saved formal JSON and original target bytes; never import or execute analyzer or target.',
    'analyzer_or_target_executed_by_reviewer': False,
    'tool_or_target_tests_run': False,
    'formal_tool_identity': freeze['tool_identity'],
    'independently_recomputed_tool_source_hash': aggregate.hexdigest(),
    'aggregate_tool_hash_matches_freeze': aggregate.hexdigest() == freeze['tool_identity']['source_hash'],
    'package_source_checks': package_checks,
    'package_source_set_matches_freeze': {item['file'] for item in package_checks} == set(freeze['package_source_sha256']),
    'all_package_hashes_match': all(item['matches_freeze'] for item in package_checks),
    'all_frozen_archive_hashes_match': all(item['frozen_archive_matches_freeze'] for item in package_checks),
    'frozen_archive_source_set_matches_freeze': {path.relative_to(HERE / 'frozen-core-source').as_posix()
        for path in (HERE / 'frozen-core-source').rglob('*.py')} == set(freeze['package_source_sha256']),
    'original_contract': {'goals': 5, 'necessary_obligations': 30,
        'sha256': sha(ROOT / 'reports/astra-iteration4/GOAL_ACCEPTANCE.md'),
        'field_facts_or_sites_are_not_goal_coverage': True},
    'original_26_observation_baseline_sha256': sha(ROOT / 'reports/astra-baseline/capability-baseline.json'),
    'repositories': [], 'field_sites': [], 'source_checks': [],
    'typed_evidence_snapshot_checks': [], 'engine_selected_facts': [],
}

source_checks, evidence_checks, evidence_record_contents = {}, {}, {}
source_bytes = {}
summaries = {}
baseline_counts = Counter()

for repository in ('codepatchbay', 'winwincode'):
    summary = load(HERE / f'{repository}-summary.json')
    previous = load(PREVIOUS / f'{repository}-summary.json')
    integration = load(HERE / f'{repository}-integration.json')
    baseline = load(HERE / f'{repository}-baseline-v11-and-v10.json')
    summaries[repository] = summary
    current_observations = {item['id']: item for item in baseline['current']['observations']}
    old_observations = {item['id']: item for item in baseline['previous']['observations']}
    baseline_counts.update(baseline['current']['counts'])
    baseline_changes = [key for key, item in current_observations.items()
        if key not in old_observations or any(item.get(field) != old_observations[key].get(field)
            for field in ('status', 'expected_static_outcome', 'expectation_satisfied'))]
    policy = HERE / f'{repository}-policy.json'
    old_policy = PREVIOUS / f'{repository}-policy.json'
    repo = {
        'repository': repository, 'snapshot_id': summary['id'],
        'source_hash': summary['source_hash'], 'policy_hash': summary['policy_hash'],
        'status': summary['status'],
        'stats': {key: summary['stats'].get(key) for key in
            ('files_total', 'files_parsed', 'files_failed', 'nodes', 'edges', 'coverage_incomplete')},
        'source_hash_unchanged_from_v10': summary['source_hash'] == previous['source_hash'],
        'policy_hash_unchanged_from_v10': summary['policy_hash'] == previous['policy_hash'],
        'policy_bytes_identical_to_v10': policy.read_bytes() == old_policy.read_bytes(),
        'policy_bytes_sha256': sha(policy),
        'published_tool_identity_matches_freeze': summary['stats']['component_versions']['tool'] == freeze['tool_identity'],
        'both_cold_and_warm_saved': [scan['phase'] for scan in integration['scans']] == ['cold','warm'],
        'all_scan_snapshots_match_publication': all(scan['snapshot_id']==summary['id'] for scan in integration['scans']),
        'all_scan_tool_identities_match_freeze': all(scan['stats']['component_versions']['tool']==freeze['tool_identity'] for scan in integration['scans']),
        'integration': integration,
        'baseline_counts': baseline['current']['counts'],
        'baseline_observation_identity_set_preserved': set(current_observations) == set(old_observations),
        'baseline_status_or_expectation_changes': baseline_changes,
    }
    result['repositories'].append(repo)

    for fi, finding in enumerate(summary['rule_findings']):
        # Validate actual source references in all configured saved findings,
        # including navigation, atomicity and budget evidence.
        for record in walk(finding):
            if all(key in record for key in ('file', 'source_hash', 'start_byte', 'end_byte')):
                file, start, end = record['file'], record['start_byte'], record['end_byte']
                if not file or not isinstance(start, int) or not isinstance(end, int):
                    continue
                key = (repository, file, record['source_hash'], start, end, record.get('span_hash'))
                if key not in source_checks:
                    path = ROOT.parent / repository / file
                    raw = source_bytes.setdefault((repository, file), path.read_bytes())
                    span = hashlib.sha256(raw[start:end]).hexdigest()
                    source_checks[key] = {'repository': repository, 'file': file,
                        'start_byte': start, 'end_byte': end,
                        'source_hash_matches': hashlib.sha256(raw).hexdigest() == record['source_hash'],
                        'range_within_source': 0 <= start <= end <= len(raw),
                        'saved_span_hash_present': 'span_hash' in record,
                        'saved_span_hash_matches': span == record['span_hash'] if 'span_hash' in record else None}
            if record.get('record') == 'EvidenceRef':
                encoded = json.dumps(record,sort_keys=True,separators=(',',':'),ensure_ascii=True)
                evidence_record_contents.setdefault((repository,record['evidence_id']),set()).add(encoded)
                identity = [summary['stats']['component_versions']['semantic_ir'],
                    record['file'],record['source_hash'],record['start_byte'],record['end_byte'],
                    record['model_id'],sorted(set(record['guard_ids'])),record['snapshot_id'],record['context_id'],record['kind']]
                recomputed = hashlib.sha256(json.dumps(identity,sort_keys=True,ensure_ascii=True,
                    separators=(',',':'),allow_nan=False).encode()).hexdigest()
                key = (repository, record['evidence_id'], encoded)
                evidence_checks[key] = {'repository': repository,
                    'evidence_id': record['evidence_id'], 'snapshot_id': record['snapshot_id'],
                    'matches_published_snapshot': record['snapshot_id'] == summary['id'],
                    'evidence_id_matches_record_contents':record['evidence_id']==recomputed,
                    'guard_ids_canonical':record['guard_ids']==sorted(set(record['guard_ids']))}
        if finding['type'] != 'static_parameter_field_flow':
            continue
        details = next(item['details'] for item in finding['evidence'] if 'assessments' in item.get('details', {}))
        for ai, assessment in enumerate(details['assessments']):
            site = {key: assessment.get(key) for key in (
                'site_location', 'call_context', 'branch_conditions', 'field_presence',
                'selected_field_shape_closed', 'whole_object_shape_closed', 'source_form_relation',
                'pre_completion_source_form_relation', 'field_sources', 'copy_steps',
                'analysis_phase', 'reaching_value_origin_proven', 'opaque_effects_or_exceptions_excluded',
                'runtime_value_verified', 'conditions', 'gaps', 'local_copy_retention_supported',
                'local_copy_retention', 'source_relations')}
            site.update(repository=repository, snapshot_id=summary['id'], rule_id=finding['rule_id'],
                finding_id=finding['id'], finding_status=finding['status'],
                json_pointer=f'/rule_findings/{fi}/evidence/0/details/assessments/{ai}',
                source_form_complete=details.get('source_form_complete'),
                selected_shape_complete=details.get('selected_shape_complete'),
                transport_proven=details.get('transport_proven'),
                full_functionality_proven=details.get('full_functionality_proven'))
            result['field_sites'].append(site)
        if finding['rule_id'] == 'cpb-astra-field-engine-options':
            result['engine_source_assumptions'] = details['source_assumptions']
            assessment = details['assessments'][0]
            selected = assessment['ir_selected_value']
            origins = assessment['field_sources']
            steps = assessment['copy_steps']
            result['engine_copy_chain_review'] = {
                'selected_value_id': selected['value_id'],
                'subject_parameter_declaration_id': details['subject_parameter']['declaration_id'],
                'origins_match_actual_subject_parameter': bool(origins) and all(
                    origin['binding_id']==details['subject_parameter']['declaration_id']
                    and origin['parameter_index']==details['parameter_index']
                    and origin['field_path']==details['field_path'] for origin in origins),
                'copy_observations_preserve_same_selected_value': bool(steps) and all(
                    step['captured_value_id']==selected['value_id'] for step in steps),
                'copy_operation_kinds': sorted(step['evidence']['kind'] for step in steps),
                'presence_still_unknown': assessment['field_presence']=='unknown',
                'whole_shape_still_not_closed': assessment['whole_object_shape_closed'] is False,
                'reaching_value_not_claimed': assessment['reaching_value_origin_proven'] is False,
                'runtime_value_not_claimed': assessment['runtime_value_verified'] is False,
                'transport_not_claimed': details['transport_proven'] is False,
                'full_functionality_not_claimed': details['full_functionality_proven'] is False,
            }
            for si, fact in enumerate(details['source_facts']):
                op, line = fact['operation'], fact['location']['line']
                if (op == 'object_rest_copy'
                    or op == 'actual_helper_selected_return_summary' and line == 155
                    or op == 'new_literal_object_shape' and line in (85, 157)
                    or op == 'ordered_object_spread' and line in (158, 176)
                    or op == 'authenticated_module_capture_cell_seed'):
                    result['engine_selected_facts'].append({'fact': fact,
                        'json_pointer': f'/rule_findings/{fi}/evidence/0/details/source_facts/{si}'})

result['baseline_status_counts'] = dict(baseline_counts)
result['source_checks'] = list(source_checks.values())
result['typed_evidence_snapshot_checks'] = list(evidence_checks.values())
result['all_source_refs_match'] = all(item['source_hash_matches'] and item['range_within_source']
    and item['saved_span_hash_matches'] is not False for item in source_checks.values())
result['all_typed_evidence_snapshots_match'] = all(item['matches_published_snapshot'] for item in evidence_checks.values())
result['all_typed_evidence_ids_match_contents'] = all(item['evidence_id_matches_record_contents'] and item['guard_ids_canonical'] for item in evidence_checks.values())
result['typed_evidence_id_collisions'] = [{'repository':key[0],'evidence_id':key[1],'distinct_record_count':len(contents)}
    for key,contents in evidence_record_contents.items() if len(contents)>1]
result['source_reference_totals'] = {
    'unique_locations_or_evidence_refs': len(source_checks),
    'with_saved_span_hash': sum(item['saved_span_hash_present'] for item in source_checks.values()),
    'unique_source_files': len(source_bytes), 'unique_typed_evidence_refs': len(evidence_checks),
    'not_a_coverage_metric': True,
}

fields = load(HERE / 'field-assessments.json')
result['field_export_matches_published_findings'] = all(
    item['snapshot_id'] == summaries[item['repository']]['id']
    and item['assessments'] == [finding for finding in summaries[item['repository']]['rule_findings']
        if finding['type'] == 'static_parameter_field_flow']
    for item in fields['repositories'])
result['saved_input_artifact_sha256'] = ARTIFACTS
result['saved_inputs_stable_during_collection'] = all(sha(ROOT / name) == expected for name, expected in ARTIFACTS.items())
result['package_bytes_stable_during_collection'] = all(sha(package/item['file'])==item['sha256'] for item in package_checks)
out = HERE / 'INDEPENDENT_REVIEW_EVIDENCE.json'
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'artifact': str(out), 'sha256': sha(out),
    'core_matches': result['all_package_hashes_match'],
    'source_checks': result['source_reference_totals'],
    'all_source_refs_match': result['all_source_refs_match'],
    'all_typed_evidence_snapshots_match': result['all_typed_evidence_snapshots_match'],
    'all_typed_evidence_ids_match_contents': result['all_typed_evidence_ids_match_contents'],
    'typed_evidence_id_collision_count': len(result['typed_evidence_id_collisions']),
    'baseline_status_counts': result['baseline_status_counts'],
    'field_site_count': len(result['field_sites'])}))
