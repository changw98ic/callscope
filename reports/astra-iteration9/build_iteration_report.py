"""Compare final v10 with v11 using saved report artifacts only.

Captured source relations and conditional copy-time retention are independent
axes. Their counts never change the frozen 26 observations or five-goal / 30
obligation acceptance contract and do not imply runtime or business coverage.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path

from publication_identity import check_identity, write_json


def load(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact_fields(summary):
    result = []
    for finding in summary['rule_findings']:
        if finding['type'] != 'static_parameter_field_flow':
            continue
        details = next((item['details'] for item in finding['evidence']
                        if 'assessments' in item.get('details', {})), {})
        sites = []
        for site in details.get('assessments', []):
            relations = site.get('source_relations', {})
            copies = site.get('local_copy_retention', [])
            sites.append({
                'location': {key: site.get('site_location', {}).get(key)
                             for key in ('file', 'line', 'column')},
                'branch_conditions': site.get('branch_conditions', []),
                **{key: site.get(key) for key in (
                    'field_presence', 'selected_field_shape_closed', 'whole_object_shape_closed',
                    'source_form_relation', 'pre_completion_source_form_relation', 'gaps')},
                'source_relations_version': relations.get('version'),
                'source_relations_proof_domain': relations.get('proof_domain'),
                'source_relation_kind_counts': dict(sorted(Counter(
                    item['kind'] for item in relations.get('relations', [])).items())),
                'direct_write_scan': relations.get('direct_write_scan'),
                'source_relation_coverage': relations.get('coverage'),
                'source_relation_gaps': relations.get('analysis_gaps', []),
                'local_copy_retention_supported': site.get('local_copy_retention_supported', False),
                'local_copy_boundaries': [{
                    'spread_location': item.get('spread_location'),
                    'literal_location': item.get('literal_location'),
                    'conclusion': item.get('conclusion'),
                    'antecedents': item.get('antecedents', []),
                    'observation_id': item.get('witness', {}).get('observation', {}).get('observation_id'),
                    'witness_id': item.get('witness', {}).get('witness_id'),
                    'supported': item.get('witness', {}).get('supported', False),
                    'gaps': item.get('witness', {}).get('gaps', []),
                    'later_definition_keys': item.get('witness', {}).get('later_definition_keys', []),
                } for item in copies],
            })
        result.append({
            'rule_id': finding['rule_id'], 'status': finding['status'],
            'metadata': finding['metadata'], 'summary_budget': details.get('summary_budget'),
            'assessment_counts': details.get('assessment_counts'),
            'source_relation_counts': details.get('source_relation_counts', {}),
            'local_copy_retention_supported_site_count': details.get('local_copy_retention_supported_site_count', 0),
            'sites': sites,
            'helper_returns': [{
                'location': {key: fact.get('location', {}).get(key)
                             for key in ('file', 'line', 'column')},
                **{key: fact.get(key) for key in (
                    'target_graph_node_id', 'selected_field_presence',
                    'selected_field_shape_closed', 'whole_object_shape_closed')},
            } for fact in details.get('source_facts', [])
                if fact.get('operation') == 'actual_helper_selected_return_summary'],
        })
    return result


def endpoint_changes(previous, current):
    """Compare old endpoint axes, without treating new local axes as closure."""
    before = {item['rule_id']: item for item in compact_fields(previous)}
    after = {item['rule_id']: item for item in compact_fields(current)}
    if before.keys() != after.keys():
        raise RuntimeError('Configured selected-field endpoints changed')
    changes = []
    for rule_id, item in after.items():
        older = before[rule_id]
        if len(older['sites']) != len(item['sites']):
            raise RuntimeError(f'{rule_id}: selected-site denominator changed')
        for index, (old, new) in enumerate(zip(older['sites'], item['sites'])):
            if old['location'] != new['location']:
                raise RuntimeError(f'{rule_id}: selected-site location changed')
            if old['source_form_relation'] == 'unknown' and new['source_form_relation'] != 'unknown':
                raise RuntimeError(f'{rule_id}: the new local axis upgraded an original unknown endpoint')
            for key in ('source_form_relation', 'pre_completion_source_form_relation',
                        'field_presence', 'selected_field_shape_closed', 'whole_object_shape_closed'):
                if old[key] != new[key]:
                    changes.append({'rule_id': rule_id, 'site_index': index,
                                    'location': new['location'], 'axis': key,
                                    'before': old[key], 'after': new[key]})
        if older['metadata'].get('source_form_complete') and not item['metadata'].get('source_form_complete'):
            raise RuntimeError(f'{rule_id}: previously supported source-form endpoint regressed')
    return changes


def main():
    directory = Path(__file__).resolve().parent
    freeze = check_identity(directory)
    previous_directory = directory.parent / 'astra-iteration8'
    baseline_path = directory.parent / 'astra-baseline' / 'capability-baseline.json'
    baseline = load(baseline_path)
    template_path = directory.parent / 'astra-iteration4' / 'goal-ledger.template.json'
    goal_template = load(template_path)
    acceptance_path = directory.parent / 'astra-iteration4' / 'GOAL_ACCEPTANCE.md'
    if goal_template['goal_count'] != 5 or goal_template['required_obligation_count'] != 30:
        raise RuntimeError('Original five-goal/30-obligation acceptance contract changed')
    counts = Counter()
    repositories, contracts, comparisons = [], [], []
    for name in ('codepatchbay', 'winwincode'):
        summary = load(directory / f'{name}-summary.json')
        previous = load(previous_directory / f'{name}-summary.json')
        integration = load(directory / f'{name}-integration.json')
        comparison = load(directory / f'{name}-baseline-v11-and-v10.json')
        current = comparison['current']
        counts.update(current['counts'])
        if summary['stats']['component_versions']['tool'] != freeze['tool_identity']:
            raise RuntimeError(f'{name}: summary implementation differs from core freeze')
        if summary['source_hash'] != previous['source_hash'] or summary['policy_hash'] != previous['policy_hash']:
            raise RuntimeError(f'{name}: final v10 / v11 source or policy identity changed')
        current_policy = directory / f'{name}-policy.json'
        old_policy = previous_directory / f'{name}-policy.json'
        if current_policy.read_bytes() != old_policy.read_bytes():
            raise RuntimeError(f'{name}: final v10 / v11 policy bytes changed')
        versions = [{
            'version': version, 'snapshot_id': saved['id'],
            'source_hash': saved['source_hash'], 'policy_hash': saved['policy_hash'],
            'policy_bytes_sha256': digest(policy),
            'component_versions': saved['stats']['component_versions'],
            'field_assessments': compact_fields(saved),
        } for version, saved, policy in (
            ('v10', previous, old_policy), ('v11', summary, current_policy))]
        changes = endpoint_changes(previous, summary)
        comparisons.append({
            'repository': name, 'versions': versions,
            'target_source_identical_v10_v11': True,
            'v10_v11_policy_bytes_identical': True, 'v10_v11_policy_hash_identical': True,
            'policy_bytes_identical_to_frozen_v9': True,
            'original_endpoint_axis_changes': changes,
            'original_endpoint_axis_changed': bool(changes),
            'new_axes_do_not_upgrade_entry_or_endpoint_acceptance': True,
        })
        positives = [item for item in current['observations']
                     if item['expected_static_outcome'] in ('confirmed_static_call', 'confirmed_static_path')]
        repositories.append({
            'repository': name, 'snapshot_id': summary['id'], 'status': summary['status'],
            'source_hash': summary['source_hash'], 'policy_hash': summary['policy_hash'],
            'component_versions': summary['stats']['component_versions'],
            'files_total': summary['stats']['files_total'],
            'files_parsed': summary['stats']['files_parsed'],
            'files_failed': summary['stats']['files_failed'],
            'calls_by_resolution': summary['calls_by_resolution'],
            'cold_and_warm': [{key: scan[key] for key in ('phase', 'snapshot_id', 'created', 'maintenance')}
                              for scan in integration['scans']],
            'frozen_positive_total': len(positives),
            'frozen_positive_reproduced': sum(item['status'] == 'reproduced' for item in positives),
            'baseline_counts': current['counts'], 'changes_since_v10': comparison['changes'],
            'source_checks': current['source_checks'],
        })
        contracts.extend({
            'repository': name, 'finding': item,
            'interpretation': 'Configured finite static source/model relations; full goal acceptance remains separate',
        } for item in summary['rule_findings'] if item['type'].startswith('static_'))
    ledger = {
        'schema_version': 1, 'baseline_id': baseline['baseline_id'], 'baseline_status': baseline['status'],
        'package_version': freeze['package_version'], 'publication_series': 'v11',
        'package_patch_note': freeze.get('package_patch_note'),
        'baseline_sha256': digest(baseline_path), 'baseline_total': len(baseline['observations']),
        'status_counts': dict(counts), 'repositories': repositories,
        'configured_finite_contract_findings_count': len(contracts),
        'original_goal_acceptance': {
            'path': '../astra-iteration4/GOAL_ACCEPTANCE.md', 'sha256': digest(acceptance_path),
            'goal_count': 5, 'required_obligation_count': 30,
            'template_path': '../astra-iteration4/goal-ledger.template.json',
            'template_sha256': digest(template_path),
        },
        'field_relation_artifact': 'field-relations.json',
        'full_goal_acceptance_computed': False, 'precision_metric_computed': False,
        'target_executed': False, 'target_imported': False, 'target_tests_run': False,
        'target_build_run': False, 'tool_test_suite_run': False,
        'interpretation': 'Frozen observation reproduction plus separate source-structure and conditional copy-time evidence; no precision, recall, project coverage or full-goal pass rate inferred',
    }
    check_identity(directory)
    write_json(directory / 'capability-ledger.json', ledger)
    write_json(directory / 'finite-contract-witnesses.json', contracts)
    write_json(directory / 'FIELD_VERSION_COMPARISON.json', {
        'repositories': comparisons, 'package_version': freeze['package_version'],
        'package_patch_note': freeze.get('package_patch_note'),
        'precision_metric_computed': False, 'full_goal_acceptance_computed': False,
    })
    print(json.dumps({'baseline_total': ledger['baseline_total'], 'status_counts': ledger['status_counts'],
                      'configured_finite_contract_findings_count': len(contracts)}))


if __name__ == '__main__':
    main()
