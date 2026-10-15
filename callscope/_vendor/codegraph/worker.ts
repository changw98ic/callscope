/** Fixed CodeGraph analysis tool: captured text in, structural/candidate evidence out. */
import * as fs from 'node:fs';
import * as path from 'node:path';
import { createHash } from 'node:crypto';
import { gunzipSync } from 'node:zlib';
import { initGrammars, loadGrammarsForLanguages, getParser, detectLanguage,
  isFileLevelOnlyLanguage } from './upstream/src/extraction/grammars';
import { extractFromSource } from './upstream/src/extraction/tree-sitter';
import { EXTRACTORS } from './upstream/src/extraction/languages';
import { extractImportMappings, extractReExports, resolveViaImport } from './upstream/src/resolution/import-resolver';
import { resolveCapturedReference, CAPTURED_RESOLUTION_BOUNDARIES } from './resolution-bridge';

const PROTOCOL = 'callscope-codegraph-1';
const ROOT = '/__callscope_captured__';
const sha = (text: string | Buffer) => createHash('sha256').update(text).digest('hex');
// A native addon and project package loading are deliberately not part of this bridge.
process.env.CODEGRAPH_KERNEL = '0';
process.env.CODEGRAPH_VALUE_REFS = '1';

function relative(value: string): string | null {
  if (typeof value !== 'string' || value.includes('\0') || value.includes('\\')) return null;
  if (value === ROOT || value === ROOT + '/') return '';
  const raw = value.startsWith(ROOT + '/') ? value.slice(ROOT.length + 1) : value;
  if (path.posix.isAbsolute(raw)) return null;
  const normalized = path.posix.normalize(raw);
  return normalized === '..' || normalized.startsWith('../') ? null : normalized === '.' ? '' : normalized;
}

function virtualFs(texts: Map<string, string>): void {
  const read = (name: any, options?: any) => {
    const key = relative(String(name));
    if (key === null || !texts.has(key)) throw Object.assign(new Error('Uncaptured input'), { code: 'ENOENT' });
    const data = Buffer.from(texts.get(key)!, 'utf8');
    return typeof options === 'string' || options?.encoding ? data.toString(typeof options === 'string' ? options : options.encoding) : data;
  };
  const directory = (name: any) => {
    const key = relative(String(name));
    return key !== null && [...texts.keys()].some((p) => key === '' || p.startsWith(key + '/'));
  };
  const stat = (name: any) => {
    const key = relative(String(name));
    const file = key !== null && texts.has(key);
    const dir = !file && directory(name);
    if (!file && !dir) throw Object.assign(new Error('Uncaptured input'), { code: 'ENOENT' });
    return { size: file ? Buffer.byteLength(texts.get(key!)!) : 0,
      isFile: () => file, isDirectory: () => dir, isSymbolicLink: () => false };
  };
  const entries = (name: any, options?: any) => {
    const key = relative(String(name));
    if (key === null || !directory(name)) throw Object.assign(new Error('Uncaptured directory'), { code: 'ENOENT' });
    const prefix = key ? key + '/' : '';
    const names = [...new Set([...texts.keys()].filter((p) => p.startsWith(prefix))
      .map((p) => p.slice(prefix.length).split('/')[0]))].sort();
    return options?.withFileTypes ? names.map((n) => ({ name: n,
      isFile: () => texts.has(prefix + n), isDirectory: () => directory(prefix + n), isSymbolicLink: () => false })) : names;
  };
  // Modules and grammars are loaded before this facade is installed. Upstream
  // project helpers then see ONLY captured files, including direct fs helpers.
  const moduleFs = require('fs');
  Object.assign(moduleFs, { readFileSync: read, existsSync: (p: any) => {
    const key = relative(String(p)); return key !== null && (texts.has(key) || directory(p));
  }, statSync: stat, lstatSync: stat, readdirSync: entries,
  realpathSync: (p: any) => { if (relative(String(p)) === null) throw new Error('Uncaptured path'); return String(p); } });
}

async function main() {
  const manifest = JSON.parse(fs.readFileSync(path.join(__dirname, 'UPSTREAM.json'), 'utf8'));
  const bytes: Record<string, Uint8Array> = {};
  const load = async (languages: string[]) => {
    const expanded = new Set(languages);
    if (languages.some((v) => ['svelte', 'vue', 'astro'].includes(v))) {
      expanded.add('typescript'); expanded.add('javascript');
    }
    if (languages.includes('cfml')) { expanded.add('cfscript'); expanded.add('cfquery'); }
    for (const language of expanded) {
      const filename = manifest.grammar_map[language];
      if (!filename || bytes[language]) continue;
      const record = manifest.grammars[filename];
      const zipped = fs.readFileSync(path.join(__dirname, record.path));
      if (sha(zipped) !== record.sha256) throw new Error('Grammar archive identity mismatch: ' + language);
      const data = gunzipSync(zipped);
      if (sha(data) !== record.raw_sha256) throw new Error('Grammar identity mismatch: ' + language);
      bytes[language] = data;
    }
    await initGrammars();
    await loadGrammarsForLanguages([...expanded] as any, bytes);
  };
  if (process.argv.includes('--capabilities')) {
    const languages = Object.keys(manifest.grammar_map);
    await load(languages);
    process.stdout.write(JSON.stringify({ protocol: PROTOCOL, upstream_commit: manifest.commit,
      runtime_available: true, grammar_availability: Object.fromEntries(languages.map((l) => [l, getParser(l as any) !== null])),
      project_validation_claimed: false }) + '\n');
    return;
  }
  const request = JSON.parse(fs.readFileSync(0, 'utf8'));
  if (request.protocol !== PROTOCOL || typeof request.payload !== 'string' || sha(request.payload) !== request.sha256) {
    throw new Error('Captured-input protocol/fingerprint mismatch');
  }
  const payload = JSON.parse(request.payload);
  const texts = new Map<string, string>();
  for (const source of [...payload.inputs, ...payload.files]) {
    if (relative(source.path) !== source.path || !source.path || typeof source.content !== 'string' || sha(source.content) !== source.text_hash) {
      throw new Error('Invalid captured source identity');
    }
    if (texts.has(source.path) && texts.get(source.path) !== source.content) throw new Error('Conflicting captured source');
    texts.set(source.path, source.content);
  }
  // Theme JSON is classified by CallScope's safely captured theme markers;
  // upstream detectLanguage otherwise needs a live project-root lookup.
  const sourceLanguage = (source: any) => (source.language ?? payload.language) === 'liquid' && source.path.endsWith('.json')
    ? 'liquid' : detectLanguage(source.path, source.content);
  if (process.argv.includes('--classify')) {
    process.stdout.write(JSON.stringify({ protocol: PROTOCOL, request_hash: request.sha256,
      upstream_commit: manifest.commit, files: payload.files.map((source: any) => ({
        path: source.path, hash: source.hash, upstream_language: sourceLanguage(source),
      })) }) + '\n');
    return;
  }
  const languages = payload.files.map(sourceLanguage);
  await load(languages);
  const files: any[] = [], nodes: any[] = [], refs: any[] = [], structural: any[] = [];
  for (const source of payload.files) {
    const language = sourceLanguage(source);
    let parseError = false;
    const errors: any[] = [];
    const parser = getParser(language);
    if (parser) {
      const prepared = EXTRACTORS[language]?.preParse?.(source.content, source.path) ?? source.content;
      const tree = parser.parse(prepared);
      parseError = !tree || tree.rootNode.hasError;
      tree?.delete();
    }
    let result: any;
    try { result = extractFromSource(source.path, source.content, language); }
    catch (error) { throw new Error('CodeGraph extractor failed: ' + String(error)); }
    errors.push(...result.errors);
    const metadataOnly = isFileLevelOnlyLanguage(language) || language === 'xml';
    const status = metadataOnly ? 'captured_metadata'
      : parseError || errors.some((e) => e.severity === 'error' || e.code === 'parse_error') ? 'parse_error'
      : !parser ? 'structural_extracted' : 'parsed';
    files.push({ path: source.path, hash: source.hash, upstream_language: language, status, errors,
      grammar_has_error: parser ? parseError : null, analysis_level: metadataOnly ? 'file_or_metadata' : 'structural_extraction' });
    const extracted = result.nodes.length ? result.nodes : [{ id: 'file:' + source.path, kind: 'file',
      name: path.posix.basename(source.path), qualifiedName: source.path, filePath: source.path,
      language, startLine: 1, endLine: source.content.split('\n').length, startColumn: 0, endColumn: 0 }];
    for (const original of extracted) { const { updatedAt, ...node } = original; nodes.push(node); }
    structural.push(...result.edges);
    refs.push(...result.unresolvedReferences.map((r: any) => ({ ...r, filePath: source.path, language })));
  }
  const byId = new Map(nodes.map((n) => [n.id, n]));
  const index = (key: string) => {
    const out = new Map<string, any[]>();
    for (const node of nodes) { const name = String(node[key] ?? ''); out.set(name, [...(out.get(name) ?? []), node]); }
    return out;
  };
  const byFile = index('filePath'), byName = index('name'), byKind = index('kind'), byQualified = index('qualifiedName');
  const lower = new Map<string, any[]>();
  for (const node of nodes) { const key = node.name.toLowerCase(); lower.set(key, [...(lower.get(key) ?? []), node]); }
  const imports = new Map<string, any>(), reExports = new Map<string, any>(), fileLines = new Map<string, string[] | null>();
  const cached = (cache: Map<string, any>, key: string, compute: () => any) => {
    if (!cache.has(key)) cache.set(key, compute());
    return cache.get(key);
  };
  const context: any = {
    getNodesInFile: (p: string) => byFile.get(relative(p) ?? '') ?? [],
    getNodesByName: (name: string) => byName.get(name) ?? [],
    getNodesByQualifiedName: (name: string) => byQualified.get(name) ?? [],
    getNodesByKind: (kind: string) => byKind.get(kind) ?? [],
    getNodesByLowerName: (name: string) => lower.get(name) ?? [],
    getNodeById: (id: string) => byId.get(id) ?? null,
    fileExists: (p: string) => texts.has(relative(p) ?? '\0'),
    readFile: (p: string) => texts.get(relative(p) ?? '\0') ?? null,
    getProjectRoot: () => ROOT,
    getAllFiles: () => [...texts.keys()],
    getImportMappings: (p: string, l: any) => cached(imports, `${p}\0${l}`, () => extractImportMappings(p, context.readFile(p) ?? '', l)),
    getReExports: (p: string, l: any) => cached(reExports, `${p}\0${l}`, () => extractReExports(context.readFile(p) ?? '', l)),
    getFileLines: (p: string) => cached(fileLines, p, () => context.readFile(p)?.split(/\r?\n/) ?? null),
    fileContains: (p: string, needle: string) => context.readFile(p)?.includes(needle) ?? false,
    getNodesInFileNamed: (p: string, n: string) => context.getNodesInFile(p).filter((v: any) => v.name === n),
    getExportedNodesInFile: (p: string) => context.getNodesInFile(p).filter((v: any) => v.isExported),
    fileHasExportedNode: (p: string) => context.getNodesInFile(p).some((v: any) => v.isExported),
    iterateNodesByKind: (k: string) => (byKind.get(k) ?? [])[Symbol.iterator](),
    getSupertypes: () => [], getSupertypeNodes: () => [], getProjectAliases: () => null,
    getNearestAliases: () => null, getGoPackageDir: () => null, getWorkspacePackages: () => null,
    getCppIncludeDirs: () => [], getCppIncludeNodes: () => [],
    listDirectories: (p: string) => {
      const key = relative(p); if (key === null) return [];
      const prefix = key ? key + '/' : '';
      return [...new Set([...texts.keys()].filter((f) => f.startsWith(prefix) && f.slice(prefix.length).includes('/'))
        .map((f) => prefix + f.slice(prefix.length).split('/')[0]))].sort();
    },
  };
  context.resolveImport = (ref: any) => resolveViaImport(ref, context);
  virtualFs(texts);
  const references: any[] = [], resolutionErrors: any[] = [];
  for (const ref of refs) {
    let result: any = null;
    try { result = resolveCapturedReference(ref, context); }
    catch (error) { resolutionErrors.push({ file: ref.filePath, line: ref.line, message: String(error) }); }
    const candidates: any[] = [];
    if (result && byId.has(result.targetNodeId)) candidates.push({ target: result.targetNodeId,
      confidence: result.confidence, resolved_by: result.resolvedBy, metadata: result.metadata ?? {} });
    for (const alternative of result?.alsoTargets ?? []) if (byId.has(alternative.targetNodeId)) candidates.push({
      target: alternative.targetNodeId, confidence: alternative.metadata?.codegraphConfidence ?? result.confidence,
      resolved_by: alternative.metadata?.codegraphResolvedBy ?? result.resolvedBy, metadata: alternative.metadata ?? {} });
    references.push({ ...ref, candidates });
  }
  process.stdout.write(JSON.stringify({ protocol: PROTOCOL, request_hash: request.sha256, upstream_commit: manifest.commit,
    language: payload.language, files, nodes, structural_edges: structural, references,
    resolution_errors: resolutionErrors, boundaries: CAPTURED_RESOLUTION_BOUNDARIES,
    project_reads: 'captured-text-only; actual target path never provided', native_kernel_used: false }) + '\n');
}

main().catch((error) => { console.error(String(error?.stack ?? error)); process.exitCode = 2; });
