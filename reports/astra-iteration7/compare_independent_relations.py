"""Compare complete saved navigation/atomicity findings; execute no analyzer."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

ROOT = Path('/workspace/callscope')
HERE = Path(__file__).resolve().parent
OLD = ROOT / 'reports/astra-iteration6'
ID = re.compile(r'(?:[a-f0-9]{24}|[a-f0-9]{64}|port-(?:fact|gap|model):[a-f0-9]{24}|abstract-[0-9]+)\Z')
ID_LISTS = {'input_value_ids', 'guaranteed_contexts', 'possible_contexts',
    'lookup_dependencies', 'factory_callback_contexts', 'fact_ids', 'gap_ids',
    'input_fact_ids', 'inputs'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


output = {'kind': 'independent_complete_saved_relation_comparison',
    'method': 'Recursive whole-finding comparison, retaining list order, every non-identity value and bijective identity references; only authenticated publication-version fields differ.',
    'analyzer_or_target_executed': False, 'tests_run': False, 'comparisons': []}

for repository, prefix in [('codepatchbay', 'static_atomicity'), ('winwincode', 'static_navigation')]:
    paths = [directory / f'{repository}-summary.json' for directory in (OLD, HERE)]
    hashes = [sha(path) for path in paths]
    summaries = [json.loads(path.read_text()) for path in paths]
    findings = [next(finding for finding in summary['rule_findings'] if finding['type'].startswith(prefix)) for summary in summaries]
    forward, backward, identity_occurrences = {}, {}, Counter()
    differences, publication_changes = [], []

    def compare(before, after, path=()):
        if type(before) != type(after):
            differences.append({'path': '/'.join(path), 'kind': 'type'})
            return
        if isinstance(before, dict):
            if set(before) != set(after):
                differences.append({'path': '/'.join(path), 'kind': 'keys',
                    'removed': sorted(set(before)-set(after)), 'added': sorted(set(after)-set(before))})
            for key in sorted(before.keys() & after.keys()):
                compare(before[key], after[key], (*path, key))
            return
        if isinstance(before, list):
            if len(before) != len(after):
                differences.append({'path': '/'.join(path), 'kind': 'length', 'before': len(before), 'after': len(after)})
            for index, (a, b) in enumerate(zip(before, after)):
                compare(a, b, (*path, str(index)))
            return
        key = path[-1] if path else ''
        identity_field = key == 'id' or key.endswith('_id') or (key.isdigit() and len(path)>1 and path[-2] in ID_LISTS)
        if identity_field and isinstance(before, str) and ID.fullmatch(before) and ID.fullmatch(after):
            # Include unchanged IDs too: a renamed ID cannot collide with an
            # existing unchanged identity, or change the equality relation.
            if before in forward and forward[before] != after or after in backward and backward[after] != before:
                differences.append({'path': '/'.join(path), 'kind': 'identity_bijection_conflict', 'before': before, 'after': after})
            forward[before], backward[after] = after, before
            identity_occurrences[key if not key.isdigit() else path[-2]] += 1
            return
        if before == after:
            return
        if len(path)>1 and path[-2] == 'snapshot_identity' and key in {'analyzer_version','detector_version','parser_version'}:
            if key == 'parser_version':
                valid = json.loads(before) == summaries[0]['stats']['component_versions'] and json.loads(after) == summaries[1]['stats']['component_versions']
            else:
                valid = before == summaries[0][key] and after == summaries[1][key]
            if valid:
                publication_changes.append({'path': '/'.join(path), 'field': key, 'matches_own_summary': True})
                return
        differences.append({'path': '/'.join(path), 'kind': 'semantic_value', 'before': before, 'after': after})

    compare(*findings)
    output['comparisons'].append({
        'repository': repository, 'rule_id': findings[1]['rule_id'],
        'inputs': [{'path': str(path.relative_to(ROOT)), 'sha256': digest} for path, digest in zip(paths, hashes)],
        'input_bytes_stable': [sha(path) for path in paths] == hashes,
        'source_hash_unchanged': summaries[0]['source_hash'] == summaries[1]['source_hash'],
        'policy_hash_unchanged': summaries[0]['policy_hash'] == summaries[1]['policy_hash'],
        'all_non_identity_values_and_relations_preserved': not differences,
        'identity_mapping': [{'before': key, 'after': value} for key, value in sorted(forward.items())],
        'identity_occurrence_counts': dict(identity_occurrences),
        'authenticated_publication_version_changes': publication_changes,
        'differences': differences,
        'graph_node_ids_identical': findings[0]['node_ids'] == findings[1]['node_ids'],
        'graph_edge_ids_identical': findings[0]['edge_ids'] == findings[1]['edge_ids'],
    })

out = HERE / 'INDEPENDENT_RELATION_REVIEW.json'
out.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'artifact': str(out), 'sha256': sha(out), 'comparisons': [
    {'repository': item['repository'], 'relations_preserved': item['all_non_identity_values_and_relations_preserved'],
     'identity_map_count': len(item['identity_mapping']), 'difference_count': len(item['differences'])}
    for item in output['comparisons']]}))
