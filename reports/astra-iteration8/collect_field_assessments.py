"""Export all configured field assessments from published static snapshots.

This helper reads saved summaries only. It does not decide full goal acceptance,
read a target workspace, or run a target or a test suite.
"""
import json
from pathlib import Path

def main():
    directory = Path(__file__).resolve().parent
    repositories = []
    for name in ('codepatchbay', 'winwincode'):
        summary = json.loads((directory / f'{name}-summary.json').read_text())
        selected = [finding for finding in summary['rule_findings']
                    if finding['type'] == 'static_parameter_field_flow']
        repositories.append({'repository': name, 'snapshot_id': summary['id'],
            'source_hash': summary['source_hash'], 'policy_hash': summary['policy_hash'],
            'component_versions': summary['stats']['component_versions'],
            'configured_field_contracts_count': summary['stats']['field_contracts_count'],
            'assessment_findings_count': len(selected), 'assessments': selected,
            'meaning': 'Each selected field endpoint has a source/model assessment; this is not full pipeline or functional coverage.'})
    artifact = {'kind': 'published_static_field_assessments', 'repositories': repositories,
        'target_executed': False, 'target_tests_run': False, 'target_build_run': False,
        'full_goal_acceptance_computed': False}
    (directory / 'field-assessments.json').write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'configured': sum(item['configured_field_contracts_count'] for item in repositories),
        'assessment_findings': sum(item['assessment_findings_count'] for item in repositories)}))

if __name__ == '__main__':
    main()
