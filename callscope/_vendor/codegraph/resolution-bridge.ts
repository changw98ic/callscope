/**
 * Captured-input adapter for CodeGraph's exported resolution strategies.
 *
 * This is candidate evidence, never a proof of a call. Project reads made by
 * the supplied context AND the worker's fs facade must use the same captured
 * snapshot. No database-backed ReferenceResolver is constructed here.
 *
 * Dispatch and the small outer guards follow upstream resolution/index.ts;
 * matching, visibility, type inference and import parsing remain upstream.
 */
import type { Node } from './upstream/src/types';
import type { ResolvedRef, ResolutionContext, UnresolvedRef } from './upstream/src/resolution/types';
import {
  CPP_DEFINE_SIGNATURE, isImportableKind, isInheritanceRef, isSupertypeTarget,
} from './upstream/src/resolution/types';
import {
  gateLanguageMatch, goTypePositionTarget, GO_STDLIB_PACKAGES, GO_TYPE_KINDS,
  isDartAnnotation, isDartChainLink, isDartMemberRead, isGoAssertedLocal,
  isGoBareName, isGoProjectLocalCall, isGoUnknownQualified, isPythonSelfCall,
  isRustNameInScope, isStdMethodName, isUnresolvedJsMemberCall,
  isVisibleAcrossFiles, matchDartAnnotation, matchDartChainLink,
  matchDartMemberRead, matchFunctionRef, matchGoAssertedCall,
  matchObjectPathCall, matchReference, thisScopeCaller,
} from './upstream/src/resolution/name-matcher';
import {
  isBoundToOutOfRepoImport, isCobolCopybookRef, isDartImportRef,
  isJsPathImportRef, isLuaRequireRef, isNixPathImportRef, isPhpIncludePathRef,
  resolveJvmImport, resolvePhpImportedStaticCall, resolvePhpQualifiedClassRef,
  resolveViaImport,
} from './upstream/src/resolution/import-resolver';
import { isVisibleCppMacro } from './upstream/src/resolution/cpp-macro-visibility';
import { isCppConstructorRef, matchCppConstructor } from './upstream/src/resolution/cpp-constructor';
import { isCppSupertypeRef, matchCppSupertype } from './upstream/src/resolution/cpp-supertypes';
import { gateSwiftTypeTarget } from './upstream/src/resolution/swift-type-visibility';
import { gateTypeParameter } from './upstream/src/resolution/type-parameters';
import { gateDartLocal } from './upstream/src/resolution/dart-local-scope';
import {
  isVbMemberRead, isVbPathCall, matchVbMemberRead, matchVbPathCall,
} from './upstream/src/resolution/vbnet-receivers';
import { matchShopifyThemeFile } from './upstream/src/resolution/shopify-themes';
import { resolveAliasBinding } from './upstream/src/resolution/alias-binding';

export const CAPTURED_RESOLUTION_BOUNDARIES = [
  'candidate-only; upstream confidence is not a measured correctness probability',
  'no framework discovery, framework routes or cross-file synthesis passes',
  'no database-backed deferred conformance or inherited callback pass',
  'no private Razor-using or qualified CFML-component resolver',
  'no complete private upstream builtin/external prefilter',
  'Dart conditional imports retain alternatives without choosing a runtime platform',
  'unknown Dart library scope can make upstream visibility permissive',
] as const;

const OWNER_KINDS = new Set<string>([
  'class', 'struct', 'interface', 'trait', 'protocol', 'enum', 'module',
]);
const CALLABLE_KINDS = new Set<string>(['function', 'method', 'class', 'constant', 'variable']);
const CHAIN_SHAPE = /^(.+)\(\)\.(\w+)$/;
const JS_PYTHON_CHAINS = new Set<string>(['typescript', 'javascript', 'tsx', 'jsx', 'python']);
const RESOLUTION_METHODS: ReadonlySet<string> = new Set([
  'exact-match', 'import', 'qualified-name', 'framework', 'fuzzy',
  'instance-method', 'file-path', 'function-ref',
]);

/** Class-local this.member callback lookup; inherited-only callbacks stay unknown. */
function thisMemberReference(ref: UnresolvedRef, context: ResolutionContext): ResolvedRef | null {
  const written = context.getNodeById?.(ref.fromNodeId);
  if (!written) return null;
  const from = thisScopeCaller(written, context);
  const cut = from.qualifiedName.lastIndexOf('::');
  const owner = OWNER_KINDS.has(from.kind) ? from.qualifiedName
    : cut > 0 ? from.qualifiedName.slice(0, cut) : null;
  if (!owner) return null;
  const members = context.getNodesByQualifiedName(`${owner}::${ref.referenceName.slice(5)}`)
    .filter((n) => (n.kind === 'function' || n.kind === 'method') &&
      n.filePath === ref.filePath && n.id !== ref.fromNodeId);
  if (!members.length) return null;
  const result = (n: Node): ResolvedRef => ({
    original: ref, targetNodeId: n.id, confidence: 0.95, resolvedBy: 'function-ref',
  });
  return combine(members.map(result));
}

/** Upstream target-kind checks, without querying or mutating a graph database. */
function targetKind(result: ResolvedRef | null, ref: UnresolvedRef,
  context: ResolutionContext): ResolvedRef | null {
  if (!result) return null;
  const target = context.getNodeById?.(result.targetNodeId);
  // A dangling target is not useful candidate evidence.
  if (!target) return null;
  if (ref.referenceKind === 'calls') {
    if (target.kind === 'constant' && CPP_DEFINE_SIGNATURE.test(target.signature ?? '')) return null;
    if (ref.language === 'go' && GO_TYPE_KINDS.has(target.kind) &&
      !ref.referenceName.includes('.') && !isGoBareName(ref, context)) return null;
  }
  if (ref.referenceKind === 'imports') {
    if (target.kind === 'import' && target.filePath === ref.filePath) return null;
    return isImportableKind(target.kind) ? result : null;
  }
  if (ref.language === 'go' && ref.referenceKind === 'references' &&
    context.getNodeById?.(ref.fromNodeId)?.kind === 'type_alias' &&
    isGoUnknownQualified(ref, context)) return null;
  if (ref.language === 'go' && (ref.referenceKind === 'instantiates' ||
    (ref.referenceKind === 'references' && context.getNodeById?.(ref.fromNodeId)?.kind !== 'route'))) {
    return goTypePositionTarget(result, ref, context);
  }
  if (!isInheritanceRef(ref)) return result;
  if (!isSupertypeTarget(target)) {
    if ((target.kind !== 'constant' && target.kind !== 'variable') ||
      (target.language !== 'typescript' && target.language !== 'tsx')) return null;
    const types = context.getNodesInFile(target.filePath)
      .filter((n) => n.name === target.name && isSupertypeTarget(n));
    if (types.length !== 1) return null;
    result = { ...result, targetNodeId: types[0]!.id };
  }
  if (isBoundToOutOfRepoImport(ref, context)) return null;
  if (ref.language === 'go' && isGoUnknownQualified(ref, context)) return null;
  return result;
}

function gateSingle(result: ResolvedRef | null, ref: UnresolvedRef,
  context: ResolutionContext): ResolvedRef | null {
  let gated = gateDartLocal(gateTypeParameter(
    gateSwiftTypeTarget(targetKind(result, ref, context), ref, context), ref, context), ref, context);
  if (!gated) return null;
  let target = context.getNodeById?.(gated.targetNodeId);
  if (!target) return null;
  if (ref.language === 'rust' && /^[A-Za-z_]\w*$/.test(ref.referenceName) &&
    !isRustNameInScope(target, ref, context)) return null;
  gated = gateLanguageMatch(gated, ref, context);
  if (!gated) return null;
  // This is the upstream post-selection veto: never try another namesake
  // merely because the selected declaration failed visibility.
  if (!isVisibleAcrossFiles(target, ref, context)) return null;
  if (ref.language === 'nix' && target.filePath !== ref.filePath) return null;
  if (target.language === 'nix' && ref.language !== 'nix') return null;
  if (ref.language === 'dart' && ref.referenceKind === 'references' &&
    gated.targetNodeId === ref.fromNodeId) return null;
  if (ref.referenceKind === 'calls' && gated.targetNodeId === ref.fromNodeId) {
    const name = ref.referenceName.slice(Math.max(ref.referenceName.lastIndexOf('.'),
      ref.referenceName.lastIndexOf(':')) + 1);
    if (/^[A-Za-z_$][\w$]*$/.test(name)) {
      const line = (context.getFileLines?.(ref.filePath) ??
        context.readFile(ref.filePath)?.split(/\r?\n/))?.[ref.line - 1];
      const escaped = name.replace(/\$/g, '\\$');
      if (line && new RegExp(
        String.raw`(?:\b(?:super|base)\s*(?:\(\s*(?:[\w.]+\s*,\s*\w+)?\s*\))?\s*\??\.\s*|\[\s*super\s+|\bparent\s*::\s*)` +
        escaped + String.raw`\b`).test(line)) return null;
    }
  }
  if (ref.referenceKind === 'calls') {
    const dot = ref.referenceName.lastIndexOf('.');
    const forwarded = resolveAliasBinding(target,
      dot >= 0 ? ref.referenceName.slice(dot + 1) : null, context);
    if (forwarded && forwarded.id !== target.id) {
      gated = gateLanguageMatch({ ...gated, targetNodeId: forwarded.id,
        confidence: Math.min(gated.confidence, 0.85),
        metadata: { ...gated.metadata, codegraphAliasSourceId: target.id } }, ref, context);
      if (!gated || !isVisibleAcrossFiles(forwarded, ref, context)) return null;
      target = forwarded;
    }
  }
  return { ...gated, metadata: { ...gated.metadata,
    codegraphCandidateOnly: true, codegraphBridge: 'captured-exported-strategies-v1',
    codegraphResolvedBy: gated.resolvedBy, codegraphConfidence: gated.confidence } };
}

/** Keep independent upstream alternatives; no new name/proximity guesses. */
function combine(results: ResolvedRef[]): ResolvedRef | null {
  if (!results.length) return null;
  const expanded: ResolvedRef[] = [];
  for (const result of results) {
    const { alsoTargets, ...primary } = result;
    expanded.push(primary);
    for (const other of alsoTargets ?? []) {
      const metadata = { ...primary.metadata, ...other.metadata };
      const ownConfidence = other.metadata?.codegraphConfidence;
      const ownMethod = other.metadata?.codegraphResolvedBy;
      expanded.push({ ...primary, targetNodeId: other.targetNodeId,
        confidence: typeof ownConfidence === 'number' && Number.isFinite(ownConfidence)
          ? ownConfidence : primary.confidence,
        resolvedBy: typeof ownMethod === 'string' && RESOLUTION_METHODS.has(ownMethod)
          ? ownMethod as ResolvedRef['resolvedBy'] : primary.resolvedBy,
        metadata });
    }
  }
  const unique = new Map<string, ResolvedRef>();
  for (const result of expanded) {
    const key = `${result.targetNodeId}\0${result.edgeKind ?? result.original.referenceKind}`;
    const prior = unique.get(key);
    if (!prior || result.confidence > prior.confidence) unique.set(key, result);
  }
  const ordered = [...unique.values()].sort((a, b) => b.confidence - a.confidence ||
    a.targetNodeId.localeCompare(b.targetNodeId));
  const primary = ordered[0]!;
  const alternatives = ordered.slice(1).map((r) => ({ targetNodeId: r.targetNodeId,
    metadata: { ...r.metadata, codegraphResolvedBy: r.resolvedBy,
      codegraphConfidence: r.confidence, codegraphReferenceKind: r.edgeKind ?? r.original.referenceKind } }));
  return { ...primary, ...(alternatives.length ? { alsoTargets: alternatives } : {}) };
}

function finish(result: ResolvedRef | null, ref: UnresolvedRef,
  context: ResolutionContext): ResolvedRef | null {
  if (!result) return null;
  const { alsoTargets, ...primary } = result;
  const results = [gateSingle(primary, ref, context)];
  for (const other of alsoTargets ?? []) results.push(gateSingle({ ...primary,
    targetNodeId: other.targetNodeId, metadata: { ...primary.metadata, ...other.metadata } }, ref, context));
  return combine(results.filter((r): r is ResolvedRef => r !== null));
}

/**
 * Resolve against one immutable captured snapshot. getNodeById is required by
 * this adapter even though older upstream contexts declared it optional.
 * Every primary / alsoTargets record is candidate evidence only. Consumers
 * must expand alsoTargets and retain its per-target metadata.
 */
export function resolveCapturedReference(ref: UnresolvedRef,
  context: ResolutionContext): ResolvedRef | null {
  if (!context.getNodeById) return null;
  const done = (r: ResolvedRef | null): ResolvedRef | null => finish(r, ref, context);
  if (isVisibleCppMacro(ref, context)) return null;
  if (isCppConstructorRef(ref)) return done(matchCppConstructor(ref, context));
  if (isCppSupertypeRef(ref)) return done(matchCppSupertype(ref, context));
  if (isDartMemberRead(ref)) return done(matchDartMemberRead(ref, context));
  if (isDartChainLink(ref, context)) return done(matchDartChainLink(ref, context));
  if (isDartAnnotation(ref)) return done(matchDartAnnotation(ref, context));
  const asserted = matchGoAssertedCall(ref, context);
  if (asserted !== undefined) return done(asserted);
  const theme = matchShopifyThemeFile(ref, context);
  if (theme !== undefined) return done(theme);

  // Private resolver-only component path handling is deliberately not guessed.
  if ((ref.language === 'cfml' || ref.language === 'cfscript') &&
    isInheritanceRef(ref) && /[./]/.test(ref.referenceName)) return null;
  const phpQualified = resolvePhpQualifiedClassRef(ref, context);
  if (phpQualified !== undefined) return done(phpQualified);
  if (isVbMemberRead(ref)) return done(matchVbMemberRead(ref, context));
  if (isVbPathCall(ref)) return done(matchVbPathCall(ref, context,
    (name) => isStdMethodName('vbnet', name)));

  if (ref.referenceKind === 'function_ref') {
    if (ref.referenceName.startsWith('this.')) return done(thisMemberReference(ref, context));
    if ((ref.language === 'python' || ref.language === 'go') && ref.referenceName.includes('.')) {
      return done(matchFunctionRef(ref, context));
    }
    const imported = resolveViaImport(ref, context);
    const target = imported && context.getNodeById(imported.targetNodeId);
    if (imported && target && (target.kind === 'function' || target.kind === 'method' ||
      (ref.language === 'python' && target.kind === 'class'))) return done(imported);
    return done(matchFunctionRef(ref, context));
  }
  const jvm = resolveJvmImport(ref, context);
  if (jvm) return done(jvm);
  const phpStatic = resolvePhpImportedStaticCall(ref, context);
  if (phpStatic !== undefined) return done(phpStatic);

  if (isUnresolvedJsMemberCall(ref)) {
    const root = ref.referenceName.slice(0, ref.referenceName.indexOf('.'));
    if (!context.getImportMappings(ref.filePath, ref.language)
      .some((m) => m.isNamespace && m.localName === root)) return done(matchObjectPathCall(ref, context));
    const imported = resolveViaImport(ref, context);
    const target = imported && context.getNodeById(imported.targetNodeId);
    return target && CALLABLE_KINDS.has(target.kind) ? done(imported) : null;
  }
  if (ref.referenceKind === 'calls' && CHAIN_SHAPE.test(ref.referenceName) &&
    JS_PYTHON_CHAINS.has(ref.language)) return done(matchReference(ref, context));

  // Preserve the upstream guard against guessing standard-library Go calls.
  if (ref.language === 'go') {
    const dot = ref.referenceName.indexOf('.');
    const head = dot > 0 ? ref.referenceName.slice(0, dot) : '';
    if (GO_STDLIB_PACKAGES.has(head) && !isGoAssertedLocal(head, ref, context) &&
      !isGoProjectLocalCall(ref, context)) return null;
  }
  const selfCall = ref.language === 'python' && ref.referenceKind === 'calls' &&
    context.getImportMappings(ref.filePath, ref.language).some((m) => m.localName === ref.referenceName) &&
    isPythonSelfCall(ref, context);
  const imported = selfCall ? null : done(resolveViaImport(ref, context));
  // Import/path refs must never guess a same-basename symbol on failure.
  const importOnly = isDartImportRef(ref) || isPhpIncludePathRef(ref) ||
    isCobolCopybookRef(ref) || isNixPathImportRef(ref) || isLuaRequireRef(ref) ||
    isJsPathImportRef(ref) || ref.language === 'terraform' ||
    (ref.referenceKind === 'imports' && (ref.language === 'c' || ref.language === 'cpp'));
  if (importOnly || (imported && imported.confidence >= 0.9)) return imported;
  const named = done(matchReference(ref, context));
  return combine([imported, named].filter((r): r is ResolvedRef => r !== null));
}
