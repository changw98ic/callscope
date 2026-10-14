"""Publish frozen v13 static reports with full cold and warm recomputation.

Uses the full engine to avoid a second LMDB/CocoIndex cache in this publication
round. This engine change is recorded and is not a same-engine precision or
performance comparison. No target code, tests, builds or installers are run.

The shared full-source query lock is acquired internally. Do not wrap this
helper in a second flock on the same lock file.
"""
import argparse
from collections import Counter
from dataclasses import asdict
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil

from callscope.service import AnalysisService
from callscope.project_report import build_project_report, render_markdown
from publication_identity import check_identity, check_snapshot, query_lock, write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repository', choices=('codepatchbay', 'winwincode'))
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    root = directory.parents[2] / args.repository
    config = directory / f'{args.repository}-policy.json'
    database = directory / f'{args.repository}-v13.sqlite3'
    products = [directory / f'{args.repository}-{suffix}' for suffix in (
        'automatic-report.json', 'automatic-report.md', 'configured-findings.json', 'integration.json')]
    # A failed first attempt must remain inspectable. Never relabel a rerun of
    # an existing store as a fresh cold publication or overwrite saved results.
    with query_lock(directory) as lock_path:
        if any(path.exists() for path in [database, *products]):
            raise FileExistsError('This publication already has a database/artifact; preserve it and identify the retry explicitly')
        freeze = check_identity(directory)
        disk_before = shutil.disk_usage(directory).free
        service = AnalysisService(root, database, config, engine='full')
        publications = []
        try:
            for phase in ('cold', 'warm'):
                check_identity(directory)
                print(json.dumps({'repository': args.repository, 'phase': phase, 'state': 'started',
                    'engine': 'full', 'frontends_recomputed': True, 'global_detection': 'full'}), flush=True)
                publication = service.scan()
                if publication['maintenance'] != {'engine': 'full', 'global_detection': 'full'}:
                    raise RuntimeError('Publication unexpectedly used a cached/other maintenance engine')
                publications.append({'phase': phase, **publication})
                print(json.dumps({'repository': args.repository, 'phase': phase,
                    'snapshot_id': publication['snapshot_id'], 'status': publication['status'],
                    'created': publication['created'], 'maintenance': publication['maintenance']}), flush=True)
            snapshot = service.snapshot()
            check_snapshot(directory, snapshot)
            if not publications[0]['created']:
                raise RuntimeError('The fresh cold publication did not create a snapshot')
            if publications[0]['snapshot_id'] != publications[1]['snapshot_id'] or publications[1]['created']:
                raise RuntimeError('Unchanged full recomputation changed or republished immutable analysis identity')
            findings = service.store.get_findings(snapshot.id)
            report = build_project_report(snapshot, findings)
            write_json(products[0], report, exclusive=True)
            with products[1].open('x', encoding='utf-8') as stream:
                stream.write(render_markdown(report))
            write_json(products[2], [asdict(item) for item in findings if item.rule_id], exclusive=True)
            summary = {'repository': args.repository, 'scans': publications, 'snapshot_id': snapshot.id,
                'package_version': freeze['package_version'], 'publication_series': 'v13',
                'source_hash': snapshot.source_hash, 'policy_hash': snapshot.policy_hash,
                'analyzer_version': snapshot.analyzer_version, 'detector_version': snapshot.detector_version,
                'schema_version': snapshot.schema_version, 'parser_version': snapshot.parser_version, 'stats': snapshot.stats,
                'publication_maintenance_engine': 'full', 'cold_and_warm_frontends_recomputed': True,
                'cold_and_warm_global_detection': 'full', 'incremental_cache_reuse_claimed': False,
                'previous_publication': 'astra-iteration10/v12',
                'comparison': freeze['engine_comparison_scope'],
                'query_lock': str(lock_path), 'disk_free_before_bytes': disk_before,
                'target_executed': False, 'target_imported': False, 'target_tests_run': False,
                'target_build_run': False, 'tool_test_suite_run': False}
            judgment_summary = [{'goal_id': item['goal_id'], 'complete': item['complete_assessment'],
                'supported': item['full_goal_supported'], 'gaps': len(item['necessary_gaps'])} for item in report['judgments']]
            chain_summary = dict(Counter(item['assessment']['state'] for item in report['functional_chains']))
        finally:
            service.close()
        wal = Path(str(database) + '-wal')
        if wal.exists() and wal.stat().st_size:
            raise RuntimeError('Service closed but database WAL is nonempty; preserve before any immutable read')
        check_identity(directory)
        summary.update(database_closed=True, database_wal_empty_or_absent=True,
            completed_at=datetime.now(timezone.utc).isoformat(), disk_free_after_bytes=shutil.disk_usage(directory).free)
        write_json(products[3], summary, exclusive=True)
        print(json.dumps({'repository': args.repository, 'judgments': judgment_summary,
            'functional_chain_status_counts': chain_summary, 'database_closed': True,
            'integration_artifact': str(products[3])}), flush=True)


if __name__ == '__main__':
    main()
