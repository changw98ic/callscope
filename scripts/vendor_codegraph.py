"""Copy pinned CodeGraph source and compressed grammar bytes; never run target code."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

PIN = '8f1f842b5b828175992d2ce2cdf673b955b2cce9'
DEST = Path(__file__).resolve().parents[1] / 'callscope/_vendor/codegraph'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('checkout', type=Path)
    parser.add_argument('tool_dependencies', type=Path)
    args = parser.parse_args()
    checkout = args.checkout.resolve()
    dependencies = args.tool_dependencies.resolve()
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=checkout).decode().strip()
    if commit != PIN:
        raise ValueError(f'Expected CodeGraph {PIN}, got {commit}')
    DEST.mkdir(parents=True, exist_ok=True)
    copied = []

    def copy(relative):
        source = checkout / relative
        target = DEST / 'upstream' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        copied.append({'path': 'upstream/' + relative, 'upstream_path': relative,
                       'sha256': hashlib.sha256(source.read_bytes()).hexdigest()})

    for directory in ['src', 'codegraph-kernel/src', 'docs/grammars']:
        for source in sorted((checkout / directory).rglob('*')):
            if source.is_file() and source.suffix != '.wasm':
                copy(source.relative_to(checkout).as_posix())
    for relative in ['LICENSE', 'README.md', 'package.json', 'package-lock.json', 'tsconfig.json',
                     'codegraph-kernel/Cargo.toml', 'codegraph-kernel/Cargo.lock']:
        if (checkout / relative).is_file():
            copy(relative)
    for source in sorted((checkout / 'codegraph-kernel/grammars').rglob('LICENSE*')):
        copy(source.relative_to(checkout).as_posix())
    grammar_text = (checkout / 'src/extraction/grammars.ts').read_text()
    mapping = dict(re.findall(r"^  (\w+): '(tree-sitter-[^']+\.wasm)',", grammar_text, re.M))
    resources = DEST / 'grammars'
    resources.mkdir(exist_ok=True)
    grammar_records = {}
    for filename in sorted(set(mapping.values())):
        upstream = checkout / 'src/extraction/wasm' / filename
        source = upstream if upstream.is_file() else dependencies / 'node_modules/tree-sitter-wasms/out' / filename
        data = source.read_bytes()
        compressed = gzip.compress(data, compresslevel=6, mtime=0)
        target = resources / (filename + '.gz')
        target.write_bytes(compressed)
        grammar_records[filename] = {'path': 'grammars/' + target.name,
            'source': 'codegraph:' + source.relative_to(checkout).as_posix() if upstream.is_file()
                      else 'tree-sitter-wasms@0.1.13:out/' + filename,
            'raw_bytes': len(data), 'raw_sha256': hashlib.sha256(data).hexdigest(),
            'sha256': hashlib.sha256(compressed).hexdigest()}
    runtime = DEST / 'runtime/web-tree-sitter'
    runtime.mkdir(parents=True, exist_ok=True)
    for name in ['package.json', 'LICENSE', 'README.md', 'tree-sitter.cjs', 'tree-sitter.js', 'tree-sitter.wasm']:
        shutil.copyfile(dependencies / 'node_modules/web-tree-sitter' / name, runtime / name)
    licenses = DEST / 'dependency-notices'
    licenses.mkdir(exist_ok=True)
    for name in ['jsonc-parser', 'tree-sitter-wasms', 'web-tree-sitter', 'picomatch']:
        package = dependencies / 'node_modules' / name
        for source in package.iterdir():
            if source.is_file() and (source.name.lower().startswith(('license', 'notice', 'copying')) or source.name == 'package.json'):
                shutil.copyfile(source, licenses / (name + '-' + source.name))
    shutil.copyfile(dependencies / 'package-lock.json', DEST / 'tool-dependencies.lock.json')
    provenance = {'repository': 'https://github.com/colbymchenry/codegraph', 'commit': PIN,
        'version': json.loads((checkout / 'package.json').read_text())['version'],
        'license': 'MIT; separate grammar/runtime notices retained',
        'source_modifications': [], 'source_files': copied,
        'grammar_map': mapping, 'grammars': grammar_records,
        'runtime': {'web-tree-sitter': '0.25.10', 'jsonc-parser': '3.3.1',
                    'tree-sitter-wasms': '0.1.13', 'picomatch': '4.0.3', 'esbuild_build_only': '0.21.5'},
        'execution_boundary': 'Only fixed analysis-tool code consumes captured text. No target module loading, commands, tests or builds.',
        'native_kernel': 'Rust sources retained; native addon is disabled. Runtime uses the upstream WASM extractors.'}
    (DEST / 'UPSTREAM.json').write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'source_files': len(copied), 'grammar_languages': len(mapping),
                      'grammar_resources': len(grammar_records), 'destination': str(DEST)}))


if __name__ == '__main__':
    main()
