"""Restore or verify saved report JSON; never execute analyzed project code."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CURRENT = 'reports/astra-iteration12-scope2/'


def safe_path(relative: str, prefix: str) -> Path:
    path = PurePosixPath(relative)
    if not isinstance(relative, str) or path.is_absolute() or '..' in path.parts or str(path) != relative or not relative.startswith(prefix):
        raise ValueError('Invalid archive path')
    result = ROOT.joinpath(*path.parts)
    for parent in (result, *result.parents):
        if parent == ROOT:
            break
        if parent.is_symlink():
            raise ValueError('Archive paths cannot traverse symlinks')
    if not result.resolve().is_relative_to(ROOT):
        raise ValueError('Archive path escapes the repository')
    return result


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def restore(item: dict, verify_only: bool) -> str:
    destination = safe_path(item['file'], 'reports/')
    if destination.suffix != '.json':
        raise ValueError('Only report JSON can be restored')
    if destination.exists() and (destination.stat().st_size != item['bytes'] or file_hash(destination) != item['sha256']):
        raise FileExistsError('Refusing to overwrite different data: ' + item['file'])
    write_output = not verify_only and not destination.exists()
    temporary = None
    output = None
    h = hashlib.sha256()
    count = 0
    try:
        if write_output:
            destination.parent.mkdir(parents=True, exist_ok=True)
            output = tempfile.NamedTemporaryFile(mode='wb', dir=destination.parent, prefix='.restore-', delete=False)
            temporary = Path(output.name)
        for part in item['parts']:
            compressed = safe_path(part['file'], 'publication/compressed-reports/')
            if compressed.stat().st_size != part['bytes'] or file_hash(compressed) != part['sha256']:
                raise ValueError('Compressed bytes differ: ' + part['file'])
            part_size = 0
            with gzip.open(compressed, 'rb') as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b''):
                    part_size += len(block)
                    count += len(block)
                    if part_size > part['uncompressed_bytes'] or count > item['bytes']:
                        raise ValueError('Archive exceeds declared size')
                    h.update(block)
                    if output is not None:
                        output.write(block)
            if part_size != part['uncompressed_bytes']:
                raise ValueError('Archive part size differs')
        if count != item['bytes'] or h.hexdigest() != item['sha256']:
            raise ValueError('Restored bytes differ: ' + item['file'])
        if output is not None:
            output.close()
            output = None
            os.link(temporary, destination)
        return 'restored' if write_output else 'verified'
    finally:
        if output is not None:
            output.close()
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--all', action='store_true', help='Include archived historical JSON metadata')
    parser.add_argument('--verify-only', action='store_true', help='Verify gzip parts and original SHA256 without restoring files')
    parser.add_argument('--list', action='store_true', help='List selected original artifact paths and byte sizes')
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'publication/COMPRESSED_REPORT_ARTIFACTS.json').read_text(encoding='utf-8'))
    if manifest.get('version') != 1:
        raise ValueError('Unsupported archive version')
    artifacts = [item for item in manifest['artifacts'] if args.all or item['file'].startswith(CURRENT)]
    for item in artifacts:
        status = 'listed' if args.list else restore(item, args.verify_only)
        print(json.dumps({'file': item['file'], 'bytes': item['bytes'], 'status': status}), flush=True)
    print(json.dumps({'artifacts': len(artifacts), 'verified_or_listed_original_bytes': sum(item['bytes'] for item in artifacts),
                      'target_code_executed': False, 'target_tests_run': False}), flush=True)


if __name__ == '__main__':
    main()
