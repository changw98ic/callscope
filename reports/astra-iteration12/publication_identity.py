"""Authenticate v14 saved-source, policy, archive and implementation identities.

Original reports remain the benchmark. These checks are artifact bookkeeping,
not a recurring model review or approval step. No target code is invoked.
"""
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath

BASELINE_SHA256 = "16b4b05c8818fa1eecf396132ebe2ea29a8f0068801165f0649da379d9041dd7"
GOAL_ACCEPTANCE_SHA256 = "9b6f4fda6aa24f055e288690e76405779e36758f8ba986799f78f2f96aa8d118"
GOAL_TEMPLATE_SHA256 = "d33f48b4f0908458b587e3ad4a97d3b40eb46e3b7eb291d04d053155a5c6ad04"
EXPECTED_VERSIONS = {"package_version": "0.14.0", "publication_series": "v14",
    "analyzer_version": "static-multilang-14", "detector_version": "call-rules-13-architecture-explanations", "schema_version": "2"}
REPOSITORIES = ("codepatchbay", "winwincode")


def digest_file(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def package_inventory(package):
    return {path.relative_to(package).as_posix(): digest_file(path) for path in sorted(package.rglob('*.py'))}


def json_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True,
        separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def check_contracts(directory):
    directory = Path(directory)
    for relative, expected in (("astra-baseline/capability-baseline.json", BASELINE_SHA256),
            ("astra-iteration4/GOAL_ACCEPTANCE.md", GOAL_ACCEPTANCE_SHA256),
            ("astra-iteration4/goal-ledger.template.json", GOAL_TEMPLATE_SHA256)):
        if digest_file(directory.parent / relative) != expected:
            raise RuntimeError(f"Frozen original tracking contract changed: {relative}")
    previous = json.loads((directory.parent / 'astra-iteration11/CORE_FREEZE.json').read_text())
    if previous.get('publication_series') != 'v13' or not previous.get('benchmark_reports'):
        raise RuntimeError('The preceding original-benchmark identity is not the formal v13 record')
    for relative, expected in previous['benchmark_reports'].items():
        if digest_file(directory.parent / relative) != expected:
            raise RuntimeError(f"Original benchmark report differs from the formal v13 record: {relative}")


def check_identity(directory):
    import callscope
    from callscope.analysis_inputs import tool_identity
    from callscope.models import ANALYZER_VERSION, DETECTOR_VERSION, SCHEMA_VERSION
    directory = Path(directory)
    check_contracts(directory)
    freeze = json.loads((directory / 'CORE_FREEZE.json').read_text())
    actual_versions = {"package_version": callscope.__version__, "publication_series": freeze.get('publication_series'),
        "analyzer_version": ANALYZER_VERSION, "detector_version": DETECTOR_VERSION, "schema_version": SCHEMA_VERSION}
    if any(actual_versions[key] != value or freeze.get(key) != value for key, value in EXPECTED_VERSIONS.items()):
        raise RuntimeError('Saved freeze/current implementation is not the requested v14 publication')
    if tool_identity() != freeze['tool_identity']:
        raise RuntimeError('Implementation changed after the recorded source freeze')
    expected = freeze.get('package_source_sha256')
    if not isinstance(expected, dict) or not expected:
        raise RuntimeError('Source freeze has no Python source inventory')
    for relative in expected:
        path = PurePosixPath(relative)
        if path.is_absolute() or '..' in path.parts or str(path) != relative or not relative.endswith('.py'):
            raise RuntimeError('Unsafe package source inventory path')
    package = Path(callscope.__file__).resolve().parent
    if package_inventory(package) != expected or package_inventory(directory / 'frozen-core-source') != expected:
        raise RuntimeError('Current source or frozen archive differs from the exact recursive inventory')
    for relative, expected_hash in freeze['benchmark_reports'].items():
        if digest_file(directory.parent / relative) != expected_hash:
            raise RuntimeError(f'Original benchmark report changed: {relative}')
    for relative, expected_hash in freeze['policy_files'].items():
        if digest_file(directory / relative) != expected_hash:
            raise RuntimeError(f'Declared v14 policy changed after freeze: {relative}')
    pyproject = freeze['pyproject_sha256']
    if (digest_file(package.parent / 'pyproject.toml') != pyproject
            or digest_file(directory / 'frozen-core-source/pyproject.delivery.toml') != pyproject):
        raise RuntimeError('Delivery pyproject differs from the source freeze')
    return freeze


def check_snapshot(directory, snapshot):
    freeze = check_identity(directory)
    if snapshot.stats['component_versions']['tool'] != freeze['tool_identity']:
        raise RuntimeError('Saved snapshot uses a different implementation')
    for key in ('analyzer_version', 'detector_version', 'schema_version'):
        if getattr(snapshot, key) != freeze[key]:
            raise RuntimeError(f'Saved snapshot uses a different {key}')
    if snapshot.stats['component_versions'].get('maintenance') != {'backend': 'full'}:
        raise RuntimeError('This publication must record the actual full maintenance engine')
    repository = Path(snapshot.root).name
    if repository not in REPOSITORIES or snapshot.policy_hash != freeze['effective_policy_sha256'][repository]:
        raise RuntimeError('Saved snapshot policy does not match the frozen normalized policy')
    return freeze


def write_json(path, value, *, exclusive=True):
    path = Path(path)
    if path.exists():
        raise FileExistsError(f'Publication artifact already exists: {path}')
    temporary = path.with_suffix(path.suffix + '.tmp')
    if temporary.exists():
        raise FileExistsError(f'Unfinished artifact requires inspection: {temporary}')
    with temporary.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write('\n')
    os.link(temporary, path)
    temporary.unlink()


@contextmanager
def query_lock(directory):
    path = Path(directory).parents[1] / '.analysis-tools/goal-source-query.lock'
    with path.open('a', encoding='utf-8') as stream:
        fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        try:
            yield path
        finally:
            fcntl.flock(stream.fileno(), fcntl.LOCK_UN)
