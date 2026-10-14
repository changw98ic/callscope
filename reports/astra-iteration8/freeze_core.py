"""Record trusted implementation identity after independent source review.

No target workspace or tests are read or run. This records hashes, not approval.
"""
import ast
import hashlib
import json
from pathlib import Path
from callscope.analysis_inputs import tool_identity
from callscope import __version__
from callscope.models import ANALYZER_VERSION, DETECTOR_VERSION, SCHEMA_VERSION

def main():
    directory = Path(__file__).resolve().parent
    package = directory.parents[1] / 'callscope'
    files = sorted(package.rglob('*.py'))
    hashes = {}
    for file in files:
        raw = file.read_bytes()
        ast.parse(raw.decode('utf-8'), filename=str(file))
        hashes[file.relative_to(package).as_posix()] = hashlib.sha256(raw).hexdigest()
    freeze = {'package_version': __version__, 'schema_version': SCHEMA_VERSION,
        'publication_series': 'v10',
        'package_patch_note': 'Final 0.10.1 publication reconstructs module-cell effect EvidenceRef identities through the evidence constructor; iteration7 remains the frozen 0.10.0 candidate.',
        'analyzer_version': ANALYZER_VERSION, 'detector_version': DETECTOR_VERSION,
        'tool_identity': tool_identity(), 'package_source_sha256': hashes,
        'module_sha256': {name[:-3]: value for name, value in hashes.items() if '/' not in name},
        'freeze_basis': 'Independent source review plus normal saved-source observations. Formal scans follow this identity.',
        'target_executed': False, 'target_tests_run': False, 'tool_test_suite_run': False}
    (directory / 'CORE_FREEZE.json').write_text(json.dumps(freeze, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'version': __version__, 'tool_identity': freeze['tool_identity'], 'python_source_files': len(files)}))

if __name__ == '__main__':
    main()
