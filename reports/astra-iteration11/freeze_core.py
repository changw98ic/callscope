"""Freeze actual v13 Python source and policy bytes before static publication.

Run only once, after the root owner explicitly declares the core ready.
No target import, execution, test, build, or installation is performed.
"""
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from callscope import __version__
from callscope.analysis_inputs import tool_identity
from callscope.config import load_config
from callscope.models import ANALYZER_VERSION, DETECTOR_VERSION, SCHEMA_VERSION
from publication_identity import EXPECTED_VERSIONS, REPOSITORIES, check_contracts, digest_file, json_hash, package_inventory, write_json


def main():
    directory = Path(__file__).resolve().parent
    check_contracts(directory)
    versions = {'package_version': __version__, 'publication_series': 'v13',
        'analyzer_version': ANALYZER_VERSION, 'detector_version': DETECTOR_VERSION, 'schema_version': SCHEMA_VERSION}
    if versions != EXPECTED_VERSIONS:
        raise RuntimeError('v13 implementation versions have not been set')
    package = directory.parents[1] / 'callscope'
    archive = directory / 'frozen-core-source'
    if archive.exists() or (directory / 'CORE_FREEZE.json').exists():
        raise FileExistsError('Core freeze/archive already exists; preserve it and identify a new round instead of overwriting')
    tool_before = tool_identity()
    paths = sorted(package.rglob('*.py'))
    if not paths:
        raise RuntimeError('Python package source inventory is empty')
    captures = {}
    for path in paths:
        raw = path.read_bytes()
        ast.parse(raw.decode('utf-8'), filename=str(path))
        captures[path.relative_to(package).as_posix()] = raw
    hashes = {relative: hashlib.sha256(raw).hexdigest() for relative, raw in captures.items()}
    policy_hashes = {f'{repository}-policy.json': digest_file(directory / f'{repository}-policy.json') for repository in REPOSITORIES}
    effective_policies = {repository: json_hash(load_config(directory.parents[2] / repository,
        directory / f'{repository}-policy.json')) for repository in REPOSITORIES}
    pyproject_raw = (package.parent / 'pyproject.toml').read_bytes()
    if tool_identity() != tool_before or package_inventory(package) != hashes:
        raise RuntimeError('Core changed while preparing the freeze; nothing was archived')
    archive.mkdir()
    for relative, raw in captures.items():
        destination = archive / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open('xb') as stream:
            stream.write(raw)
    (archive / 'pyproject.delivery.toml').write_bytes(pyproject_raw)
    if tool_identity() != tool_before or package_inventory(package) != hashes:
        raise RuntimeError('Core changed while archiving; keep this failed archive for inspection')
    if any(digest_file(directory / relative) != expected for relative, expected in policy_hashes.items()):
        raise RuntimeError('Policy changed while archiving; keep the failed archive for inspection')
    freeze = {**versions, 'created_at': datetime.now(timezone.utc).isoformat(),
        'tool_identity': tool_before, 'package_source_sha256': hashes,
        'python_source_file_count': len(hashes),
        'module_sha256': {name[:-3]: value for name, value in hashes.items() if '/' not in name},
        'pyproject_sha256': hashlib.sha256(pyproject_raw).hexdigest(),
        'benchmark_reports': {f'astra-baseline/{name}': digest_file(directory.parent / 'astra-baseline' / name)
            for name in ('CODEPATCHBAY_ANALYSIS.md', 'WINWINCODE_ANALYSIS.md')},
        'policy_files': policy_hashes, 'effective_policy_sha256': effective_policies,
        'previous_publication': {'series': 'v12', 'directory': 'astra-iteration10',
            'freeze_sha256': digest_file(directory.parent / 'astra-iteration10/CORE_FREEZE.json')},
        'publication_maintenance_engine': 'full',
        'engine_comparison_scope': 'v12 used CocoIndex; v13 cold and warm scans both recompute every static frontend and detector. Not a same-engine precision/performance comparison.',
        'freeze_basis': 'Source-derived analyzers and normal actual-source observations; original reports remain the benchmark. No recurring Astra approval gate.',
        'target_executed': False, 'target_imported': False, 'target_tests_run': False,
        'target_build_run': False, 'tool_test_suite_run': False}
    write_json(directory / 'CORE_FREEZE.json', freeze, exclusive=True)
    print(json.dumps({'version': __version__, 'tool_identity': tool_before, 'python_source_files': len(hashes), 'maintenance_engine': 'full'}))


if __name__ == '__main__':
    main()
