"""Publish frozen v14 static reports with full cold and warm recomputation.

Retains the preceding full engine, without a new LMDB/CocoIndex cache. Source,
documentation, model and policy scope can change; this is not a same-policy
precision or performance comparison. No target tests/builds/installers run.

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
import traceback

from callscope.service import AnalysisService
from callscope.project_report import build_project_report, render_markdown
from publication_identity import check_identity, check_snapshot, digest_file, query_lock, write_json
from report_shared_references import VERSION as REFERENCE_VALIDATOR_VERSION, validate_shared_references


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repository', choices=('codepatchbay', 'winwincode'))
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    root = directory.parents[2] / args.repository
    config = directory / f'{args.repository}-policy.json'
    database = directory / f'{args.repository}-v14.sqlite3'
    products = [directory / f'{args.repository}-{suffix}' for suffix in (
        'automatic-report.json', 'automatic-report.md', 'configured-findings.json', 'integration.json')]
    reference_artifact = directory / f'{args.repository}-report-shared-reference-check.json'
    # A failed first attempt must remain inspectable. Never relabel a rerun of
    # an existing store as a fresh cold publication or overwrite saved results.
    with query_lock(directory) as lock_path:
        if any(path.exists() for path in [database, *products, reference_artifact]):
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
            # The only writer is this synchronous publisher. Checkpoint its
            # own analysis store before writing large JSON views, rather than
            # retaining a second WAL-sized copy until report rendering ends.
            with service.store._lock:
                checkpoint = tuple(service.store._connection.execute('PRAGMA wal_checkpoint(TRUNCATE)').fetchone())
            if checkpoint[0] != 0:
                raise RuntimeError('Static analysis-store checkpoint was busy; preserve database before report generation')
            snapshot = service.snapshot()
            check_snapshot(directory, snapshot)
            if not publications[0]['created']:
                raise RuntimeError('The fresh cold publication did not create a snapshot')
            if publications[0]['snapshot_id'] != publications[1]['snapshot_id'] or publications[1]['created']:
                raise RuntimeError('Unchanged full recomputation changed or republished immutable analysis identity')
            findings = service.store.get_findings(snapshot.id)
            report = build_project_report(snapshot, findings)
            try:
                reference_check = validate_shared_references(report)
            except Exception as error:
                # Preserve unexpected structure-check errors before attempting
                # any normal report artifact; never substitute a passing flag.
                write_json(reference_artifact, {'validator_version': REFERENCE_VALIDATOR_VERSION,
                    'repository': args.repository, 'snapshot_id': snapshot.id,
                    'check': 'actual_in_memory_responsibility_shared_reference_structure',
                    'all_explicit_shared_references_resolve_and_match': False,
                    'status': 'unexpected_validation_exception_preserved',
                    'exception': {'type': type(error).__name__, 'message': str(error),
                        'traceback': traceback.format_exc()}}, exclusive=True)
                raise
            write_json(reference_artifact, {'repository': args.repository, 'snapshot_id': snapshot.id,
                **reference_check}, exclusive=True)
            if not reference_check['all_explicit_shared_references_resolve_and_match']:
                raise RuntimeError('Normal report has invalid scoped shared references; inspect ' + str(reference_artifact))
            write_json(products[0], report, exclusive=True)
            with products[1].open('x', encoding='utf-8') as stream:
                stream.write(render_markdown(report))
            write_json(products[2], [asdict(item) for item in findings if item.rule_id], exclusive=True)
            summary = {'repository': args.repository, 'scans': publications, 'snapshot_id': snapshot.id,
                'package_version': freeze['package_version'], 'publication_series': 'v14',
                'source_hash': snapshot.source_hash, 'policy_hash': snapshot.policy_hash,
                'analyzer_version': snapshot.analyzer_version, 'detector_version': snapshot.detector_version,
                'schema_version': snapshot.schema_version, 'parser_version': snapshot.parser_version, 'stats': snapshot.stats,
                'publication_maintenance_engine': 'full', 'cold_and_warm_frontends_recomputed': True,
                'cold_and_warm_global_detection': 'full', 'incremental_cache_reuse_claimed': False,
                'previous_publication': 'astra-iteration11/v13',
                'comparison': freeze['engine_comparison_scope'],
                'query_lock': str(lock_path), 'disk_free_before_bytes': disk_before,
                'shared_reference_validation': reference_check,
                'analysis_store_checkpoint_before_report': {'mode': 'TRUNCATE', 'sqlite_result': checkpoint,
                    'logical_content_modified_by_checkpoint': False},
                'shared_reference_validation_artifact': {'file': reference_artifact.name,
                    'sha256': digest_file(reference_artifact)},
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
