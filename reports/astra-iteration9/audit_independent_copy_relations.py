"""Read saved v11 JSON and source bytes; execute no analyzer or target.

Canonical identities and saved cross-links are independently recomputed.
The saved effect list is sampled, so this file explicitly distinguishes
sample checks and full implementation review from a complete effect replay.
"""
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

ROOT = Path('/workspace/callscope')
HERE = Path(__file__).resolve().parent
INPUTS = {}


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True,
        separators=(',', ':'), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def load(path):
    raw = path.read_bytes()
    INPUTS[str(path.relative_to(ROOT))] = hashlib.sha256(raw).hexdigest()
    return json.loads(raw)


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def location(value):
    return tuple(value.get(key) for key in ('file', 'source_hash', 'start_byte', 'end_byte'))


def occurrence(value):
    return tuple(value.get(key) for key in
        ('file', 'source_hash', 'snapshot_id', 'context_id', 'model_id', 'start_byte', 'end_byte'))


def private(obj):
    return bool(obj and obj['fresh'] and not obj['escaped'] and not obj['external_aliasable']
        and not obj['conditional_allocation'] and obj['construction_guard'])


def guard_supported(guard, evidence, capability):
    return bool(guard and guard['supported'] and guard['model_id'] == evidence['model_id']
        and guard['guard_id'] in evidence['guard_ids'] and capability in guard['capabilities']
        and guard['evidence'] and guard['assumptions'] and all(
            item['model_id'] == guard['model_id'] and len(item['source_hash']) == 64
            and all(char in '0123456789abcdef' for char in item['source_hash'])
            and 0 <= item['start_byte'] <= item['end_byte'] and item['file']
            and item['snapshot_id'] == evidence['snapshot_id'] for item in guard['evidence']))


def selected(obj, key):
    return next((slot for slot in obj['slots'] if slot['key'] == key), None)


freeze = load(HERE / 'CORE_FREEZE.json')
result = {
    'kind': 'independent_saved_copy_boundary_and_source_relation_review',
    'method': 'Standard-library JSON, canonical hashes, saved cross-links and raw source-byte review only.',
    'analyzer_or_target_executed': False, 'tests_run': False,
    'formal_tool_identity': freeze['tool_identity'],
    'source_review': 'reports/astra-iteration9/PREFREEZE_IMPLEMENTATION_REVIEW.md',
    'source_review_sha256': hashlib.sha256((HERE / 'PREFREEZE_IMPLEMENTATION_REVIEW.md').read_bytes()).hexdigest(),
    'canonical_record_checks': [], 'copy_boundary_checks': [], 'copy_retention_checks': [],
    'selected_site_checks': [], 'source_relation_checks': [], 'source_context_checks': [],
    'copy_plan_checks': [], 'source_relation_reference_checks': [],
    'source_bytes_checks': [], 'identity_collisions': [],
    'effect_audit_limit': 'Assessment EffectRef arrays are samples. The independent saved-data audit does not claim to enumerate every IR effect. The frozen implementation was separately read to verify that retention checks every state effect, not an ID difference or output sample; actual suffix effect guards and checkpoint surfaces are checked here.',
    'not_goal_coverage': True,
}
canonical_seen, identity_contents = set(), defaultdict(set)
new_counts, canonical_counts = Counter(), Counter()
source_seen = {}
expected_export_sites = []

for repository in ('codepatchbay', 'winwincode'):
    summary = load(HERE / f'{repository}-summary.json')
    if summary['stats']['component_versions']['tool'] != freeze['tool_identity']:
        raise ValueError(f'{repository}: summary identity differs from freeze')
    for finding in summary['rule_findings']:
        if finding['type'] != 'static_parameter_field_flow':
            continue
        details = next(item['details'] for item in finding['evidence'] if 'assessments' in item.get('details', {}))
        facts = details['source_facts']
        new_records = {}
        for record in walk(details):
            tag = record.get('record')
            primary = {'CopyBoundaryObservation': 'observation_id', 'CopyRetentionWitness': 'witness_id',
                'ModelGuard': 'guard_id', 'ObjectVersion': 'version_id', 'EffectRef': 'effect_id'}.get(tag)
            if tag in {'CopyBoundaryObservation', 'CopyRetentionWitness'}:
                new_counts[tag] += 1
                new_records[(tag, record[primary])] = record
            if primary:
                encoded = canonical(record)
                key = (repository, tag, record[primary], encoded)
                identity_contents[(repository, tag, record[primary])].add(encoded)
                if key not in canonical_seen:
                    canonical_seen.add(key)
                    canonical_counts[tag] += 1
                    recomputed = digest({**record, primary: ''})
                    result['canonical_record_checks'].append({'repository': repository, 'record': tag,
                        'id': record[primary], 'recomputed_id': recomputed,
                        'matches': recomputed == record[primary]})
            if all(key in record for key in ('file', 'source_hash', 'start_byte', 'end_byte')):
                key = (repository, *location(record), record.get('span_hash'))
                if key not in source_seen:
                    raw = (ROOT.parent / repository / record['file']).read_bytes()
                    start, end = record['start_byte'], record['end_byte']
                    source_seen[key] = {'repository': repository, 'file': record['file'],
                        'start_byte': start, 'end_byte': end,
                        'hash_matches': hashlib.sha256(raw).hexdigest() == record['source_hash'],
                        'range_valid': 0 <= start <= end <= len(raw),
                        'span_matches': 'span_hash' not in record or hashlib.sha256(raw[start:end]).hexdigest() == record['span_hash']}

        for (tag, identifier), record in new_records.items():
            if tag == 'CopyBoundaryObservation':
                src, dst, after = record['source_snapshot'], record['destination_snapshot'], record['destination_after_copy']
                ev, value = record['evidence'], record['source_value']
                spread_facts = [fact for fact in facts if fact['operation'] == 'ordered_object_spread'
                    and fact['call_context'] == ev['context_id'] and location(fact['location']) == location(ev)
                    and fact['source_value_id'] == record['source_value_id']]
                source_identity = (src is None and record['source_allocation'] == record['source_version'] == '') or bool(
                    src and src['alloc_id'] == record['source_allocation'] and src['version_id'] == record['source_version']
                    and value['object_ref'] and value['object_ref']['alloc_id'] == src['alloc_id'])
                checks = {
                    'source_value_id_matches': record['source_value_id'] == value['value_id'],
                    'source_snapshot_identity_matches': source_identity,
                    'destination_before_identity_matches': bool(dst and dst['alloc_id'] == record['destination_allocation']
                        and dst['version_id'] == record['destination_version']),
                    'actual_copy_matches_observation_evidence': record['actual_copy_evidence'] == ev,
                    'copy_checkpoint_same_allocation': bool(after and after['alloc_id'] == record['destination_allocation']),
                    'copy_checkpoint_contains_actual_operation': bool(after and ev in after['evidence']),
                    'actual_ordered_spread_fact_found': bool(spread_facts),
                    'supported_requires_no_gaps': not record['supported'] or not record['gaps'],
                    'supported_excludes_known_absent': not record['supported'] or record['source_presence'] != 'absent',
                    'supported_requires_registered_copy_guard': not record['supported'] or (
                        guard_supported(record['surface_guard'], ev, 'own_data_copy')
                        and record['surface_guard']['model_id'] in {model['id'] for model in details['models']}),
                    'supported_requires_private_constructor': not record['supported'] or bool(private(dst)
                        and dst['construction_guard'] == record['construction_guard']
                        and any(guard_supported(record['construction_guard'], at, 'private_literal_construction') for at in dst['evidence'])),
                    'supported_has_no_direct_self_alias': not record['supported'] or bool(
                        value['object_ref'] != {'record': 'ObjectRef', 'alloc_id': record['destination_allocation']}
                        and {'record': 'ObjectRef', 'alloc_id': record['destination_allocation']} not in value['alias_roots']),
                }
                result['copy_boundary_checks'].append({'repository': repository, 'rule_id': finding['rule_id'],
                    'observation_id': identifier, 'supported': record['supported'], 'gaps': record['gaps'],
                    'source_presence': record['source_presence'], 'location': ev, 'checks': checks,
                    'all_saved_checks_match': all(checks.values())})
            else:
                obs, dst = record['observation'], record['destination_snapshot']
                cp, key = obs['destination_after_copy'], obs['selected_key']
                allowed = {occurrence(ev) for ev in record['suffix_evidence']}
                operations = bool(dst and cp) and all(ev in cp['evidence'] or occurrence(ev) in allowed for ev in dst['evidence'])
                surface = bool(dst and cp) and all(dst[k] == cp[k] for k in ('barriers', 'copy_layers', 'base_closed_shape'))
                slot = bool(dst and cp) and selected(dst, key) == selected(cp, key)
                shapes = [fact for fact in facts if fact['operation'] == 'new_literal_object_shape'
                    and fact['call_context'] == record['evidence']['context_id']
                    and location(fact['location']) == location(record['evidence'])
                    and fact['allocation'] and fact['allocation']['alloc_id'] == obs['destination_allocation']]
                suffixes = []
                for shape in shapes:
                    for index, part in enumerate(shape['parts']):
                        if part['kind'] == 'spread' and location(part['location']) == location(obs['evidence']):
                            suffixes.append(shape['parts'][index + 1:])
                suffix_matches = any(
                    all(part['kind'] == 'property' and not part['accessor'] for part in parts)
                    and [part['name'] for part in parts] == record['later_definition_keys']
                    and [location(part['location']) for part in parts] == [location(ev) for ev in record['suffix_evidence']]
                    for parts in suffixes)
                checks = {
                    'destination_endpoint_identity_matches': bool(dst and dst['version_id'] == record['destination_version']
                        and dst['alloc_id'] == obs['destination_allocation']),
                    'actual_literal_shape_found': bool(shapes),
                    'supported_requires_supported_observation': not record['supported'] or obs['supported'],
                    'supported_requires_no_gaps': not record['supported'] or not record['gaps'],
                    'supported_requires_same_private_constructor': not record['supported'] or bool(private(dst)
                        and dst['construction_guard'] == obs['construction_guard']),
                    'supported_requires_ordered_suffix_guard': not record['supported'] or guard_supported(
                        record['suffix_guard'], record['evidence'], 'ordered_data_definition_suffix'),
                    'supported_suffix_matches_actual_literal_parts': not record['supported'] or suffix_matches,
                    'supported_suffix_key_disjoint': not record['supported'] or key not in record['later_definition_keys'],
                    'supported_preserves_checkpoint_surface': not record['supported'] or surface,
                    'supported_preserves_checkpoint_selected_slot': not record['supported'] or slot,
                    'supported_accounts_for_all_new_destination_operations': not record['supported'] or operations,
                }
                result['copy_retention_checks'].append({'repository': repository, 'rule_id': finding['rule_id'],
                    'witness_id': identifier, 'supported': record['supported'], 'gaps': record['gaps'],
                    'checks': checks, 'all_saved_checks_match': all(checks.values())})

        for assessment in details['assessments']:
            expected_export_sites.append({'repository': repository, 'snapshot_id': summary['id'],
                'rule_id': finding['rule_id'], 'finding_id': finding['id'],
                **{key: assessment[key] for key in ('site_location', 'branch_conditions', 'source_form_relation',
                    'source_relations', 'local_copy_retention', 'local_copy_retention_supported')},
                'entry_value_origin_proven': False, 'runtime_value_verified': False,
                'fulfilled_value_proven': False, 'transport_proven': False, 'full_goal_acceptance_computed': False})
            relations = assessment['source_relations']
            site, version = relations['site_location'], relations['version']
            context = digest({'version': version, 'snapshot': summary['id'], 'source': site['source_hash'],
                'owner': details['subject_graph_node_id'], 'site': [site['start_byte'], site['end_byte']],
                'subject': details['subject_parameter']['declaration_id'], 'sink': details['sink'],
                'field_path': details['field_path'], 'branch_conditions': assessment['branch_conditions']})[:24]
            result['source_context_checks'].append({'repository': repository, 'rule_id': finding['rule_id'],
                'source_context': relations['source_context'], 'recomputed': context,
                'matches': context == relations['source_context']})
            by_id = {item['id']: item for item in relations['relations']}
            for relation in relations['relations']:
                computed = digest({'version': version, **{key: value for key, value in relation.items() if key != 'id'}})[:24]
                identity_contents[(repository, 'source_relation', relation['id'])].add(canonical(relation))
                result['source_relation_checks'].append({'repository': repository, 'rule_id': finding['rule_id'],
                    'id': relation['id'], 'kind': relation['kind'], 'matches': computed == relation['id'],
                    'context_matches': relation['source_context'] == context,
                    'no_heap_or_runtime_upgrade': relation['selected_heap_projection_upgraded'] is False and relation['runtime_value_verified'] is False})
                for payload in walk(relation['payload']):
                    for name, value in payload.items():
                        if name.endswith('_relation_id') and value is not None:
                            result['source_relation_reference_checks'].append({'repository': repository,
                                'id': relation['id'], 'field': name, 'target': value, 'found': value in by_id})
            for plan in relations['copy_plans']:
                computed = digest({'version': version, 'source_context': context, **{key: value for key, value in plan.items() if key != 'id'}})[:24]
                identity_contents[(repository, 'copy_plan', plan['id'])].add(canonical(plan))
                result['copy_plan_checks'].append({'repository': repository, 'rule_id': finding['rule_id'],
                    'id': plan['id'], 'matches': computed == plan['id'],
                    'construction_relation_found': plan['construction_relation_id'] in by_id,
                    'structure_only': all(plan[key] is False for key in ('local_copy_value_theorem_proven',
                        'copy_surface_model_applied', 'original_parameter_value_identity_proven', 'selected_field_presence_proven'))})
            locals_ = assessment['local_copy_retention']
            selected_checks = []
            for local in locals_:
                witness, obs = local['witness'], local['witness']['observation']
                suffix_effects = [fact for fact in facts if fact['operation'] == 'registered_effect_scope_guard'
                    and fact['call_context'] == witness['evidence']['context_id']
                    and fact['location']['file'] == obs['evidence']['file']
                    and obs['evidence']['end_byte'] <= fact['location']['start_byte']
                    and fact['location']['end_byte'] <= witness['evidence']['end_byte']]
                sampled_affected = [effect['effect_id'] for effect in assessment['effect_barriers']
                    if obs['destination_allocation'] in effect['affected_allocations']
                    and effect['evidence']['file'] == obs['evidence']['file']
                    and effect['evidence']['end_byte'] <= witness['evidence']['end_byte']]
                checks = {
                    'observation_at_actual_spread': location(obs['evidence']) == location(local['spread_location']),
                    'endpoint_at_actual_literal': location(witness['evidence']) == location(local['literal_location']),
                    'independent_axes_not_upgraded': all(local[key] is False for key in (
                        'initial_parameter_origin_proven', 'presence_proven', 'runtime_value_verified', 'fulfilled_value_proven', 'transport_proven')),
                    'conditional_antecedents_preserved': local['antecedents'] == [
                        'this actual registered whole-surface copy completes normally', 'selected current own-enumerable data slot exists at this copy'],
                    'supported_has_no_sampled_destination_effect_before_endpoint': not witness['supported'] or not sampled_affected,
                    'suffix_effect_guards_are_source_conditional': all(fact['model_guard']['runtime_verified'] is False
                        and fact['model_guard']['evidence'] and fact['model_guard']['assumptions'] for fact in suffix_effects),
                }
                selected_checks.append({'witness_id': witness['witness_id'], 'supported': witness['supported'],
                    'checks': checks, 'all_saved_checks_match': all(checks.values()),
                    'suffix_effect_scope_guards': [{'id': fact['id'], 'line': fact['location']['line'],
                        'guard_id': fact['model_guard']['guard_id'], 'roots_complete': fact['roots_complete'],
                        'reflection': fact['reflection'], 'actual_roots': fact['actual_roots'],
                        'effect_ids': fact['effect_ids']} for fact in suffix_effects],
                    'sampled_destination_effect_ids_before_endpoint': sampled_affected,
                    'full_effect_list_independently_replayed': False})
            scan = relations['direct_write_scan']
            negative_sound = scan is None or scan['payload']['verdict'] != 'no_explicit_static_target_match' or (
                scan['payload']['scoped_enumeration_complete'] and not scan['payload']['dynamic_possible_target_ids']
                and not scan['payload']['unresolved_target_locations'] and not scan['payload']['unmodeled_control_or_write_regions']
                and not relations['coverage']['incomplete'])
            result['selected_site_checks'].append({'repository': repository, 'rule_id': finding['rule_id'],
                'line': assessment['site_location']['line'], 'branch_conditions': assessment['branch_conditions'],
                'source_form_relation': assessment['source_form_relation'],
                'local_copy_retention_supported': assessment['local_copy_retention_supported'],
                'local_support_matches_witnesses': assessment['local_copy_retention_supported'] == any(item['witness']['supported'] for item in locals_),
                'source_relation_negative_scan_supported': negative_sound,
                'source_relation_complete_claim_is_not_all_paths': relations['coverage']['all_function_paths_or_callee_effects_accounted'] is False,
                'local_copy_checks': selected_checks,
                'effect_sample_truncated': assessment['effect_barriers_truncated'],
                'effect_count': assessment['effect_barrier_count'], 'effect_sample_count': len(assessment['effect_barriers'])})

result['source_bytes_checks'] = list(source_seen.values())
result['identity_collisions'] = [{'repository': key[0], 'record': key[1], 'id': key[2], 'distinct_contents': len(values)}
    for key, values in identity_contents.items() if len(values) > 1]
result['canonical_record_unique_counts'] = dict(canonical_counts)
result['new_typed_record_occurrence_counts'] = dict(new_counts)
result['all_canonical_ids_match'] = all(item['matches'] for item in result['canonical_record_checks'])
result['all_copy_saved_checks_match'] = all(item['all_saved_checks_match'] for key in ('copy_boundary_checks', 'copy_retention_checks') for item in result[key])
result['all_source_bytes_match'] = all(all(item[key] for key in ('hash_matches', 'range_valid', 'span_matches')) for item in result['source_bytes_checks'])
result['all_source_relation_checks_match'] = (all(item['matches'] and item['context_matches'] and item['no_heap_or_runtime_upgrade'] for item in result['source_relation_checks'])
    and all(item['matches'] for item in result['source_context_checks'])
    and all(item['matches'] and item['construction_relation_found'] and item['structure_only'] for item in result['copy_plan_checks'])
    and all(item['found'] for item in result['source_relation_reference_checks']))
result['all_selected_site_checks_match'] = all(item['local_support_matches_witnesses'] and item['source_relation_negative_scan_supported']
    and item['source_relation_complete_claim_is_not_all_paths'] and all(cp['all_saved_checks_match'] for cp in item['local_copy_checks']) for item in result['selected_site_checks'])
exported = load(HERE / 'field-relations.json')
result['source_relation_export_checks'] = {
    'all_selected_sites_match_formal_summaries': exported['sites'] == expected_export_sites,
    'counts_match_formal_summaries': exported['source_relation_kind_counts'] == dict(Counter(
        relation['kind'] for site in expected_export_sites for relation in site['source_relations']['relations'])),
    'conditional_support_count_matches': exported['conditional_local_copy_supported_sites'] == sum(
        site['local_copy_retention_supported'] for site in expected_export_sites),
    'no_coverage_or_full_goal_claim': exported['full_goal_acceptance_computed'] is False and exported['precision_metric_computed'] is False,
}
result['all_source_relation_export_checks_match'] = all(result['source_relation_export_checks'].values())
result['input_artifact_sha256'] = INPUTS
result['inputs_stable'] = all(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected for path, expected in INPUTS.items())
out = HERE / 'INDEPENDENT_COPY_RELATION_REVIEW.json'
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'artifact': str(out), 'sha256': hashlib.sha256(out.read_bytes()).hexdigest(),
    **{key: value for key, value in result.items() if key.startswith('all_')},
    'identity_collision_count': len(result['identity_collisions']),
    'canonical_record_unique_counts': result['canonical_record_unique_counts'],
    'source_relation_count': len(result['source_relation_checks']), 'copy_plan_count': len(result['copy_plan_checks'])}))
