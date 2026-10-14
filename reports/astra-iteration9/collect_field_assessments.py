"""Export all configured field assessments from published static snapshots.

This helper reads saved summaries only. It does not decide full goal acceptance,
read a target workspace, or run a target or a test suite.
"""
import json
from collections import Counter
from pathlib import Path
from publication_identity import check_identity, write_json

def main():
    directory = Path(__file__).resolve().parent
    freeze = check_identity(directory)
    repositories = []
    source_relations = []
    for name in ('codepatchbay', 'winwincode'):
        summary = json.loads((directory / f'{name}-summary.json').read_text())
        if summary['stats']['component_versions']['tool'] != freeze['tool_identity']:
            raise RuntimeError(f'{name}: field export uses a different implementation')
        selected = [finding for finding in summary['rule_findings']
                    if finding['type'] == 'static_parameter_field_flow']
        repositories.append({'repository': name, 'snapshot_id': summary['id'],
            'source_hash': summary['source_hash'], 'policy_hash': summary['policy_hash'],
            'component_versions': summary['stats']['component_versions'],
            'configured_field_contracts_count': summary['stats']['field_contracts_count'],
            'assessment_findings_count': len(selected), 'assessments': selected,
            'meaning': 'Each selected field endpoint has a source/model assessment; this is not full pipeline or functional coverage.'})
        for finding in selected:
            details = next((item['details'] for item in finding['evidence']
                            if 'assessments' in item.get('details', {})), {})
            for site in details.get('assessments', []):
                if any(site.get(key, False) for key in (
                    'reaching_value_origin_proven', 'runtime_value_verified',
                    'fulfilled_value_proven', 'transport_proven')):
                    raise RuntimeError('A local source axis unexpectedly upgrades entry/runtime/transport acceptance')
                for copy in site.get('local_copy_retention', []):
                    if any(copy.get(key, False) for key in (
                        'initial_parameter_origin_proven', 'presence_proven', 'runtime_value_verified',
                        'fulfilled_value_proven', 'transport_proven')):
                        raise RuntimeError('Conditional copy witness unexpectedly upgrades an excluded axis')
                source_relations.append({
                    'repository': name, 'snapshot_id': summary['id'],
                    'rule_id': finding['rule_id'], 'finding_id': finding['id'],
                    'site_location': site.get('site_location'),
                    'branch_conditions': site.get('branch_conditions', []),
                    'source_form_relation': site.get('source_form_relation'),
                    'source_relations': site.get('source_relations', {}),
                    'local_copy_retention': site.get('local_copy_retention', []),
                    'local_copy_retention_supported': site.get('local_copy_retention_supported', False),
                    'entry_value_origin_proven': False, 'runtime_value_verified': False,
                    'fulfilled_value_proven': False, 'transport_proven': False,
                    'full_goal_acceptance_computed': False,
                })
    artifact = {'kind': 'published_static_field_assessments', 'repositories': repositories,
        'target_executed': False, 'target_tests_run': False, 'target_build_run': False,
        'full_goal_acceptance_computed': False}
    relations_artifact = {
        'kind': 'separate_captured_source_and_conditional_copy_retention_axes',
        'package_version': freeze['package_version'],
        'sites': source_relations,
        'source_relation_kind_counts': dict(sorted(Counter(
            relation['kind'] for site in source_relations
            for relation in site['source_relations'].get('relations', [])).items())),
        'conditional_local_copy_supported_sites': sum(
            bool(site['local_copy_retention_supported']) for site in source_relations),
        'interpretation': 'Source structure and copy-time conditional retention are separate from original entry provenance and endpoint acceptance. Their counts are not coverage or a new acceptance denominator.',
        'full_goal_acceptance_computed': False, 'precision_metric_computed': False,
        'target_executed': False, 'target_tests_run': False, 'target_build_run': False,
    }
    check_identity(directory)
    write_json(directory / 'field-assessments.json', artifact)
    write_json(directory / 'field-relations.json', relations_artifact)
    print(json.dumps({'configured': sum(item['configured_field_contracts_count'] for item in repositories),
        'assessment_findings': sum(item['assessment_findings_count'] for item in repositories),
        'source_relation_kind_counts': relations_artifact['source_relation_kind_counts'],
        'conditional_local_copy_supported_sites': relations_artifact['conditional_local_copy_supported_sites']}))

if __name__ == '__main__':
    main()
