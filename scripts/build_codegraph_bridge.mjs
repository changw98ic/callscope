/** Compile the trusted analysis bridge, without building any analyzed project. */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const vendor = path.join(root, 'callscope/_vendor/codegraph');
const dependencies = path.resolve(process.argv[2] ?? '.analysis-tools/codegraph-build');
const requireDependency = createRequire(path.join(dependencies, 'package.json'));
const esbuild = requireDependency('esbuild');
await esbuild.build({
  absWorkingDir: vendor, entryPoints: ['worker.ts'], outfile: path.join(vendor, 'worker.cjs'),
  bundle: true, platform: 'node', format: 'cjs', target: 'node20',
  nodePaths: [path.join(dependencies, 'node_modules')],
  plugins: [{ name: 'fixed-tree-sitter-runtime', setup(build) {
    build.onResolve({ filter: /^web-tree-sitter$/ }, () => ({
      path: './runtime/web-tree-sitter/tree-sitter.cjs', external: true,
    }));
  } }],
});
// Keep the shipped bridge, resources, source and notices reviewable after each
// rebuild. The manifest excludes itself and contains no machine-specific paths.
const files = [];
function inventory(directory) {
  for (const name of fs.readdirSync(directory).sort()) {
    const filename = path.join(directory, name);
    const stat = fs.lstatSync(filename);
    if (stat.isDirectory()) inventory(filename);
    else if (stat.isFile() && filename !== path.join(vendor, 'ARTIFACTS.json')) {
      const data = fs.readFileSync(filename);
      files.push({ path: path.relative(vendor, filename).split(path.sep).join('/'),
        bytes: data.length, sha256: createHash('sha256').update(data).digest('hex') });
    }
  }
}
inventory(vendor);
files.sort((left, right) => left.path < right.path ? -1 : left.path > right.path ? 1 : 0);
const manifest = JSON.parse(fs.readFileSync(path.join(vendor, 'UPSTREAM.json'), 'utf8'));
fs.writeFileSync(path.join(vendor, 'ARTIFACTS.json'), JSON.stringify({ format: 1,
  upstream_commit: manifest.commit, files }, null, 2) + '\n');
console.log(JSON.stringify({ compiled: 'callscope/_vendor/codegraph/worker.cjs',
  bytes: fs.statSync(path.join(vendor, 'worker.cjs')).size, artifactFiles: files.length, targetCodeBuilt: false }));
