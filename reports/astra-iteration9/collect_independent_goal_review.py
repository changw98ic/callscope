"""Review saved goal-ledger identities and references without running analysis."""
from collections import Counter
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
cache, artifacts = {}, {}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
        separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def load(path):
    path = path.resolve()
    if path not in cache:
        artifacts[str(path.relative_to(ROOT))] = sha(path)
        cache[path] = json.loads(path.read_text())
    return cache[path]


def walk(value, path=()):
    if isinstance(value, dict):
        yield value, path
        for key, child in value.items():
            yield from walk(child, (*path, key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, (*path, str(index)))


def at_pointer(value, pointer):
    for part in pointer.lstrip('/').split('/') if pointer else []:
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


ledger = load(HERE / 'goal-ledger.json')
old = load(ROOT / 'reports/astra-iteration8/goal-ledger.json')
template = load(ROOT / 'reports/astra-iteration4/goal-ledger.template.json')
freeze = load(HERE / 'CORE_FREEZE.json')
refs, failures = [], []
for record, path in walk(ledger):
    if not all(key in record for key in ('artifact', 'artifact_sha256', 'json_pointer')):
        continue
    artifact_path = (HERE / record['artifact']).resolve()
    artifact = load(artifact_path)
    item = {'ledger_json_pointer': '/'+'/'.join(path), 'artifact': record['artifact'],
        'json_pointer': record['json_pointer'],
        'artifact_hash_matches': sha(artifact_path) == record['artifact_sha256']}
    try:
        target = at_pointer(artifact, record['json_pointer'])
        item['pointer_resolves'] = True
        item['pointer_content_hash_matches'] = digest(target) == record.get('target_value_sha256')
    except (KeyError, ValueError, IndexError, TypeError):
        item['pointer_resolves'] = False
    if 'snapshot_id' in record:
        item['snapshot_matches'] = artifact.get('id', artifact.get('snapshot_id')) == record['snapshot_id']
    if 'finding_id' in record:
        parts = record['json_pointer'].strip('/').split('/')
        if parts[:1] == ['rule_findings'] and len(parts)>1:
            finding = artifact['rule_findings'][int(parts[1])]
        else:
            finding = next((x for x in artifact.get('rule_findings',[]) if x.get('id')==record['finding_id']), {})
        item['finding_id_matches'] = finding.get('id') == record['finding_id']
        item['rule_id_matches'] = finding.get('rule_id') == record.get('rule_id')
        if 'contract_hash' in record:
            item['contract_hash_matches'] = any(e.get('details',{}).get('contract_hash')==record['contract_hash'] for e in finding.get('evidence',[]))
    if not all(value for key,value in item.items() if isinstance(value,bool)):
        failures.append(item)
    refs.append(item)

checks = []
statuses = Counter()
for goal in ledger['goals']:
    original = next(item for item in template['goals'] if item['id']==goal['id'])
    previous = next(item for item in old['goals'] if item['id']==goal['id'])
    required = []
    for obligation in goal['obligations']:
        source = next(item for item in original['obligations'] if item['id']==obligation['id'])
        prior = next(item for item in previous['obligations'] if item['id']==obligation['id'])
        statuses.update([obligation['assessment']['status']])
        required.append({'id':obligation['id'],
            'original_requirement_identical': all(obligation[key]==source[key] for key in ('id','title','required','requirement')),
            'assessment_status':obligation['assessment']['status'],
            'assessment_status_unchanged_from_v10':obligation['assessment']['status']==prior['assessment']['status']})
    checks.append({'goal_id':goal['id'], 'claim_identical_to_original':goal['claim']==original['claim'],
        'original_obligation_identity_set_preserved':{item['id'] for item in goal['obligations']}=={item['id'] for item in original['obligations']},
        'assessment':goal['assessment'], 'obligations':required})

contracts_match = all(goal['claim_identical_to_original'] and goal['original_obligation_identity_set_preserved']
    and all(item['original_requirement_identical'] and item['assessment_status_unchanged_from_v10']
            for item in goal['obligations']) for goal in checks)
result = {'kind':'independent_saved_goal_ledger_reference_review',
    'method':'Read saved original template, v10 and v11 ledgers and resolve every formal evidence reference including canonical pointed-to content hashes; no analyzer/target execution or tests.',
    'analyzer_or_target_executed':False, 'tests_run':False,
    'automatic_obligation_solver_used':ledger['evaluation']['automatic_obligation_solver_used'],
    'goal_count':ledger['goal_count'], 'required_obligation_count':ledger['required_obligation_count'],
    'goal_checks':checks, 'assessment':ledger['assessment'],
    'recomputed_obligation_status_counts':dict(statuses),
    'reference_count':len(refs),
    'unique_artifact_pointer_count':len({(item['artifact'],item['json_pointer']) for item in refs}),
    'references':refs, 'all_references_match':not failures, 'failures':failures,
    'all_original_contracts_match':contracts_match,
    'current_implementation_matches_freeze':ledger['evaluation']['implementation']['source_hash']==freeze['tool_identity']['source_hash'],
    'original_acceptance_contract_matches':sha(ROOT/'reports/astra-iteration4/GOAL_ACCEPTANCE.md')==ledger['acceptance_contract']['sha256'],
    'original_template_matches':sha(ROOT/'reports/astra-iteration4/goal-ledger.template.json')==ledger['evaluation']['source_template']['sha256'],
    'recomputed_status_counts_match':dict(statuses)==ledger['assessment']['obligation_status_counts'],
    'artifact_sha256':artifacts,
    'inputs_stable_during_review':all(sha(ROOT/path)==expected for path,expected in artifacts.items()),
    'reference_or_fact_count_is_not_goal_coverage':True}
out=HERE/'INDEPENDENT_GOAL_REVIEW.json'
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'artifact':str(out),'sha256':sha(out),'references':len(refs),
    'unique_pointers':result['unique_artifact_pointer_count'],'all_references_match':not failures,
    'goals':ledger['goal_count'],'required_obligations':ledger['required_obligation_count'],
    'obligation_status_counts':dict(statuses)}))
