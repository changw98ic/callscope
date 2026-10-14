"""Normal development query of saved v13 source, not a target test/fixture."""
import argparse
import ast
import fcntl
import hashlib
import json
from pathlib import Path
import sqlite3

from callscope.report_chain_analysis import _Analysis
from callscope.semantic_sources import SemanticSources
from callscope.state_lineage_relations import VERSION, analyze_pattern
from callscope.store import _snapshot_from_json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=HERE / 'state-lineage-source-query.json')
    parser.add_argument('--include-probe-source-authentication', action='store_true',
                        help='Authenticate the current development policy probe roles in the same loaded snapshot')
    args = parser.parse_args()
    if args.output.resolve().parent != HERE or args.output.exists():
        parser.error('Choose a new development artifact inside this iteration; existing outputs are preserved')
    module = ROOT / 'callscope/state_lineage_relations.py'
    ast.parse(module.read_text())
    before = hashlib.sha256(module.read_bytes()).hexdigest()
    with (ROOT / '.analysis-tools/goal-source-query.lock').open('a+') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        database = HERE.parent / 'astra-iteration11/codepatchbay-v13.sqlite3'
        connection = sqlite3.connect('file:' + str(database) + '?mode=ro&immutable=1', uri=True)
        row = connection.execute('SELECT snapshot_json,detector_version,schema_version FROM snapshots ORDER BY sequence DESC LIMIT 1').fetchone()
        connection.close()
        snapshot = _snapshot_from_json(*row)
        del row
        print(json.dumps({'state': 'captured_source_loaded', 'saved_v13_snapshot_id': snapshot.id}), flush=True)
        sources = SemanticSources(snapshot)
        results = []
        for rule in json.loads((HERE / 'state-lineage-rules.json').read_text()):
            analysis = _Analysis(snapshot, rule, sources)
            details = analysis.analyze()
            pattern = details['pattern']
            fact_ids = {fact['id'] for fact in analysis.source_facts}
            references = []
            def source_references(value):
                if isinstance(value, dict):
                    if value.get('kind') == 'source_fact_reference':
                        references.append(value['source_fact_id'])
                    for child in value.values():
                        source_references(child)
                elif isinstance(value, list):
                    for child in value:
                        source_references(child)
            source_references(pattern)
            source_references(analysis.source_facts)
            missing_refs = sorted(set(references) - fact_ids)
            if missing_refs:
                raise ValueError('Source fact references do not resolve in this real analysis: ' + repr(missing_refs))
            results.append({'rule_id': rule['id'], 'pattern': pattern, 'source_facts': analysis.source_facts,
                'analysis_gaps': analysis.gaps, 'operations': analysis.operations, 'incomplete': analysis.incomplete,
                'role_binding_closed': analysis.role_binding_closed, 'assessment': details['assessment'],
                'scope': details['scope'], 'source_fact_reference_readback': {
                    'all_references_resolve': not missing_refs, 'reference_occurrences': len(references),
                    'unique_referenced_fact_ids': len(set(references)), 'unique_fact_ids': len(fact_ids)}})
            print(json.dumps({'rule_id': rule['id'], 'supported': pattern['scoped_source_supported'],
                'gaps': analysis.gaps, 'facts': len(analysis.source_facts), 'operations': analysis.operations,
                'incomplete': analysis.incomplete}, ensure_ascii=False), flush=True)
        probe = None
        if args.include_probe_source_authentication:
            policy_path = HERE / 'codepatchbay-policy.json'
            policy_bytes = policy_path.read_bytes()
            policy = json.loads(policy_bytes)
            rules = policy['report_claims']
            matches = [rule for rule in rules if rule['id'] == 'cpb-report-trusted-probe-command-source']
            if len(matches) != 1:
                raise ValueError('Current development probe rule is not unique')
            rule = matches[0]
            analysis = _Analysis(snapshot, rule, sources)
            analysis.load()
            probe = {'rule_id': rule['id'], 'development_policy_path': str(policy_path.relative_to(ROOT)),
                'development_policy_file_sha256': hashlib.sha256(policy_bytes).hexdigest(),
                'not_the_saved_snapshot_policy': True, 'source_role_authentication_only': True,
                'pattern_not_run_or_reinterpreted': True, 'selectors': rule['sources'],
                'loaded_roles': sorted(analysis.roles), 'role_binding_closed': analysis.role_binding_closed,
                'all_selected_declarations_authenticated': len(analysis.roles) == len(rule['sources']),
                'all_selected_graph_bindings_closed': all(analysis.role_binding_closed.values()),
                'source_facts': analysis.source_facts, 'gaps': analysis.gaps}
            print(json.dumps({'probe_source_authentication': probe['all_selected_declarations_authenticated'],
                'bindings_closed': probe['all_selected_graph_bindings_closed'],
                'roles': len(analysis.roles), 'gaps': analysis.gaps}), flush=True)
        after = hashlib.sha256(module.read_bytes()).hexdigest()
        output = {'development_query': True, 'not_a_formal_v14_finding': True, 'version': VERSION,
            'module_sha256_before': before, 'module_sha256_after': after, 'module_bytes_stable': before == after,
            'saved_v13_snapshot_id': snapshot.id, 'saved_source_hash': snapshot.source_hash,
            'saved_policy_hash': snapshot.policy_hash, 'new_rules_not_in_old_saved_policy': True,
            'results': results, 'additional_probe_source_authentication': probe,
            'target_executed': False, 'target_tests_run': False, 'target_build_run': False}
        with args.output.open('x') as stream:
            json.dump(output, stream, ensure_ascii=False, indent=2)
            stream.write('\n')


if __name__ == '__main__':
    main()
