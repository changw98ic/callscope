"""Record normal saved-snapshot queries without executing analyzed code."""
import json
from pathlib import Path
from callscope.service import AnalysisService
from publication_identity import check_identity, check_snapshot


def main():
    directory = Path(__file__).resolve().parent
    check_identity(directory)
    root = directory.parents[1].parent
    queries = []
    for name, kinds in (
        ('codepatchbay', ('static_contract_literal_set_consistency',
                          'static_value_call_argument_value',
                          'static_atomicity_protected_deduplication',
                          'static_parameter_field_flow',
                          'static_local_budget')),
        ('winwincode', ('static_contract_required_object_fields',
                       'static_navigation_query_context')),
    ):
        service = AnalysisService(root / name, directory / f'{name}-v10.sqlite3',
                                  directory / f'{name}-policy.json', engine='full')
        try:
            snapshot = service.snapshot()
            check_snapshot(directory, snapshot)
            status = service.status()
            result = {'repository':name, 'snapshot_id':snapshot.id,
                      'capabilities':status['capabilities'],
                      'configured_constraints_count':status['constraints_count'],
                      'queries':[]}
            for kind in kinds:
                findings = service.findings(snapshot.id, kind=kind)['items']
                records = []
                for finding in findings:
                    detail = service.finding(finding['id'], snapshot.id)
                    sources = []
                    seen = set()
                    for evidence in detail['evidence']:
                        for location in evidence['locations']:
                            file = location.get('file')
                            if not file or file in seen:
                                continue
                            seen.add(file)
                            saved = service.source(file, snapshot.id, location.get('line',1))
                            sources.append({'file':file,'hash':saved['hash'],
                                            'status':saved['status'],'snapshot_id':saved['snapshot_id'],
                                            'content_returned':bool(saved['content'])})
                    records.append({'id':finding['id'],'rule_id':finding['rule_id'],
                                    'status':finding['status'],'metadata':finding['metadata'],
                                    'saved_sources':sources})
                result['queries'].append({'query_kind':kind,'findings':records})
            queries.append(result)
        finally:
            service.close()
    artifact={'mode':'normal queries of saved snapshots','queries':queries,
              'target_executed':False,'target_tests_run':False,'target_build_run':False}
    (directory/'saved-query-observations.json').write_text(
        json.dumps(artifact,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'repositories':len(queries),
                      'query_count':sum(len(item['queries']) for item in queries)}))


if __name__ == '__main__':
    main()
