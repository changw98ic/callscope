"use strict";

// This UI reads static analysis artifacts only. It never evaluates project code.
const $ = (id) => document.getElementById(id);
const SVG_NS = "http://www.w3.org/2000/svg";
const PAGE_SIZE = 7;
const GRAPH_LIMIT = 110;
const GRAPH_EDGE_LIMIT = 450;
const UNKNOWN_GRAPH_LIMIT = 8;
const LANGUAGE_LABELS = { python: "Python", typescript: "TypeScript / JavaScript", rust: "Rust", unknown: "未标明语言" };
const TYPE_LABELS = {
  required_path: "必需路径约束", required_call: "必需调用约束",
  forbidden_call: "禁止直接调用", forbidden_path: "禁止调用路径",
  circular_dependency: "调用循环", recursion: "递归结构",
  recursive_cycle: "递归结构", unresolved_call: "未解析调用",
  missing_entrypoint: "入口缺失", layer_violation: "分层违规",
  missing_endpoint: "规则端点缺失", rule_endpoint_missing: "规则端点缺失",
  call_cycle: "调用循环", recursive_call: "递归结构", rule_configuration: "规则配置问题",
  rule_scope_missing: "规则范围缺失", entrypoint_missing: "入口缺失",
  suspected_unreachable: "疑似不可达", external_callback_boundary: "外部回调边界",
  static_contract_literal_set_consistency: "源码集合合同差异",
  static_contract_required_object_fields: "对象字段合同待核对",
  static_value_call_argument_value: "调用参数来源合同待核对",
  static_navigation_query_context: "导航参数与消费上下文待核对",
  static_atomicity_protected_deduplication: "查重谓词与保护范围待核对",
  static_parameter_field_flow: "参数字段传递待核对",
  static_local_budget: "局部重试预算来源待核对",
};
const SEVERITIES = { high: "高", medium: "中", low: "低", info: "信息", critical: "严重" };
const RESOLUTIONS = { resolved: "确定调用", external: "外部调用", dynamic: "动态调用", ambiguous: "多个候选", unresolved: "未解析" };
const ACTIONS = { accept_risk: "接受风险", false_positive: "标记误报", fix_planned: "计划修复" };
const state = {
  status: null, versions: [], snapshotId: "", graph: null, findings: [], decisions: [],
  findingsError: "", decisionsError: "", config: null, view: "explore", review: "findings", page: 0,
  selected: null, path: null, subset: null, source: null, busy: false,
  request: 0, sourceRequest: 0, selectionRequest: 0, graphRequest: 0, diffRequest: 0,
  transform: { x: 0, y: 0, scale: 1 }, positions: new Map(), displayNodes: [], displayEdges: [],
  graphWidth: 1100, graphHeight: 680, drag: null, toastTimer: null,
  index: null, findingsSearch: new Map(), findingsLanguages: new Map(), latestDecisions: new Map(),
  decisionsByFinding: new Map(), violationNodeIds: new Set(), violationEdgeIds: new Set(),
  reviewCache: { key: "", items: [] }, displayEdgeIndex: new Map(),
};

function element(tag, options = {}, children = []) {
  const node = document.createElement(tag);
  if (options.className) node.className = options.className;
  if (options.text !== undefined) node.textContent = String(options.text);
  for (const [key, value] of Object.entries(options.attrs || {})) node.setAttribute(key, String(value));
  for (const child of children) if (child) node.append(child);
  return node;
}
function svgElement(tag, attrs = {}, text) {
  const node = document.createElementNS(SVG_NS, tag);
  for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, String(value));
  if (text !== undefined) node.textContent = String(text);
  return node;
}
function icon(name) {
  const svg = svgElement("svg", { class: "icon", "aria-hidden": "true" });
  svg.append(svgElement("use", { href: `#i-${name}` }));
  return svg;
}
function button(text, className, handler, title) {
  const node = element("button", { text, className, attrs: { type: "button" } });
  if (title) node.title = title;
  if (handler) node.addEventListener("click", handler);
  return node;
}
function badge(text, tone = "neutral") { return element("span", { text, className: `badge badge-${tone}` }); }
function formatTime(value) {
  if (!value) return "时间未知";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? String(value) : `${new Intl.DateTimeFormat("zh-CN", { month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", hour12: false, timeZone: "UTC" }).format(date)} UTC`;
}
function shortId(value) { return String(value || "—").slice(0, 12); }
function count(value) { return new Intl.NumberFormat("zh-CN").format(value || 0); }
function normalizeLanguage(value) {
  const language = String(value || "").toLowerCase();
  return ["typescript", "javascript", "tsx", "jsx", "ts", "js"].includes(language) ? "typescript" : language || "unknown";
}
function languageLabel(value) { return LANGUAGE_LABELS[normalizeLanguage(value)] || String(value); }
function maintenanceRunLabel(maintenance) {
  if (!maintenance) return "";
  const groups = [];
  for (const [field, label] of [["recomputed_languages", "重算"], ["reused_languages", "复用"], ["uncached_languages", "未缓存"]]) {
    if (Array.isArray(maintenance[field])) groups.push(`${label}：${maintenance[field].map(languageLabel).join("、") || "无"}`);
  }
  return groups.join("；") || (maintenance.engine === "full" && maintenance.global_detection === "full" ? "全量解析·全量检测" : "");
}
function fileLanguage(file) {
  if (/\.(py|pyi)$/i.test(file || "")) return "python";
  if (/\.(tsx?|jsx?|mts|cts|mjs|cjs)$/i.test(file || "")) return "typescript";
  if (/\.rs$/i.test(file || "")) return "rust";
  return "unknown";
}
function nodeLanguage(node) {
  if (node.metadata?.language) return normalizeLanguage(node.metadata.language);
  if (/^(module:)?ts:/.test(node.id)) return "typescript";
  if (/^(module:)?rust:/.test(node.id)) return "rust";
  return fileLanguage(node.file);
}
function numericMetric(value) { return typeof value === "number" && Number.isFinite(value) ? count(value) : "未记录"; }
function buildIndexes() {
  const graph = state.graph;
  const index = { nodes: new Map(), degree: new Map(), outgoing: new Map(), incoming: new Map(), unknown: [], edgeLanguages: new Map(), edgeSearch: new Map(), diagnosticSearch: new Map(), languageCounts: new Map(), resolved: 0 };
  for (const node of graph.nodes) {
    index.nodes.set(node.id, node);
    const language = nodeLanguage(node);
    index.languageCounts.set(language, (index.languageCounts.get(language) || 0) + 1);
  }
  for (const edge of graph.edges) {
    index.degree.set(edge.source, (index.degree.get(edge.source) || 0) + 1);
    if (edge.target) index.degree.set(edge.target, (index.degree.get(edge.target) || 0) + 1);
    if (!index.outgoing.has(edge.source)) index.outgoing.set(edge.source, []);
    index.outgoing.get(edge.source).push(edge);
    const source = index.nodes.get(edge.source);
    index.edgeLanguages.set(edge.id, source ? nodeLanguage(source) : fileLanguage(edge.file));
    if (uncertainEdge(edge) || (edge.resolution === "resolved" && (!index.nodes.has(edge.source) || !index.nodes.has(edge.target)))) {
      index.unknown.push(edge);
      index.edgeSearch.set(edge.id, `${edge.expression || ""} ${edge.source || ""} ${edge.file}:${edge.line} ${edge.reason || ""}`.toLocaleLowerCase());
    }
    if (edge.resolution === "resolved" && index.nodes.has(edge.source) && index.nodes.has(edge.target)) {
      index.resolved++;
      if (!index.incoming.has(edge.target)) index.incoming.set(edge.target, []);
      index.incoming.get(edge.target).push(edge);
    }
  }
  for (const diagnostic of graph.diagnostics || []) index.diagnosticSearch.set(diagnostic, `${diagnostic.file}:${diagnostic.line} ${diagnostic.code} ${diagnostic.message}`.toLocaleLowerCase());
  state.index = index;
  state.findingsSearch.clear(); state.findingsLanguages.clear(); state.violationNodeIds.clear(); state.violationEdgeIds.clear();
  for (const finding of state.findings) {
    const locations = (finding.evidence || []).flatMap((evidence) => evidence.locations || []);
    const languageSet = new Set();
    for (const id of finding.node_ids || []) { const node = index.nodes.get(id); if (node) languageSet.add(nodeLanguage(node)); }
    for (const location of locations) { const language = fileLanguage(location.file); if (language !== "unknown") languageSet.add(language); }
    state.findingsLanguages.set(finding.id, languageSet);
    const text = [finding.title, finding.description, finding.rule_id, ...(finding.node_ids || []), ...locations.map((location) => `${location.file}:${location.line}`)].join(" ");
    state.findingsSearch.set(finding.id, text.toLocaleLowerCase());
    if (isRuleViolation(finding)) {
      for (const id of finding.node_ids || []) state.violationNodeIds.add(id);
      for (const id of finding.edge_ids || []) state.violationEdgeIds.add(id);
    }
  }
  indexDecisions();
  state.reviewCache = { key: "", items: [] };
}
function indexDecisions() {
  state.latestDecisions.clear(); state.decisionsByFinding.clear();
  for (const decision of state.decisions) {
    if (!state.decisionsByFinding.has(decision.finding_id)) state.decisionsByFinding.set(decision.finding_id, []);
    state.decisionsByFinding.get(decision.finding_id).push(decision);
    const previous = state.latestDecisions.get(decision.finding_id);
    if (!previous || (decision.sequence || 0) > (previous.sequence || 0) || ((decision.sequence || 0) === (previous.sequence || 0) && String(decision.created_at || decision.timestamp) > String(previous.created_at || previous.timestamp))) state.latestDecisions.set(decision.finding_id, decision);
  }
}
function uncertainEdge(edge) {
  return !["resolved", "external"].includes(edge.resolution) || (edge.resolution === "external" && !!(edge.metadata?.callbacks_unknown || edge.metadata?.callable_arguments?.length));
}
function unknownEdges(graph = state.graph) {
  return graph === state.graph && state.index ? state.index.unknown : (graph?.edges || []).filter(uncertainEdge);
}
function resolutionLabel(edge) {
  if (edge.resolution === "external" && uncertainEdge(edge)) return "外部回调边界";
  if (edge.resolution === "resolved" && state.index && (!state.index.nodes.has(edge.source) || !state.index.nodes.has(edge.target))) return "无效解析关系";
  return RESOLUTIONS[edge.resolution] || "未知关系";
}
function snapshotLabel(snapshot) { return `${formatTime(snapshot.created_at)} · ${shortId(snapshot.id)}${snapshot.is_latest ? " · 当前" : ""}${isPartial(snapshot) ? " · 部分分析" : ""}`; }
function isPartial(snapshot) { return snapshot && (["partial", "incomplete", "failed"].includes(snapshot.status) || snapshot.stats?.incomplete === true || snapshot.stats?.coverage_incomplete === true || snapshot.stats?.call_resolution_incomplete === true); }
function findingLabel(finding) { return TYPE_LABELS[finding.type] || finding.type || "静态发现"; }
function findingStatus(finding) { return finding.status === "uncertain" ? "待确认" : finding.status === "open" ? "已发现" : finding.status || "已发现"; }
function isRuleViolation(finding) {
  return finding.status !== "uncertain" && (!!finding.rule_id || /^(required_|forbidden_|layer_violation)/.test(finding.type));
}
function emptyState(title, message, iconName = "search") {
  return element("div", { className: "empty-state" }, [icon(iconName), element("strong", { text: title }), element("p", { text: message })]);
}
function appendBatched(items, target, renderItem, batch = 30) {
  if (!items.length) return;
  let shown = 0;
  const list = element("div");
  const more = button("", "button button-small", renderNext);
  function renderNext() {
    const stop = Math.min(shown + batch, items.length);
    const fragment = document.createDocumentFragment();
    for (const item of items.slice(shown, stop)) { const node = renderItem(item); if (node) fragment.append(node); }
    list.append(fragment); shown = stop;
    more.textContent = `继续查看 ${Math.min(batch, items.length - shown)} 项（剩余 ${count(items.length - shown)} / 共 ${count(items.length)}）`;
    more.hidden = shown >= items.length;
  }
  target.append(list, more); renderNext();
}
function jsonDetails(value, summary, binding = { snapshot_id: state.snapshotId }, downloadLabel = "下载完整 JSON") {
  const details = element("details", {}, [element("summary", { text: summary })]);
  let rendered = false;
  details.addEventListener("toggle", () => {
    if (!details.open || rendered) return;
    rendered = true;
    const text = JSON.stringify(value, null, 2);
    const limit = 100000;
    details.append(element("pre", { text: text.length > limit ? `${text.slice(0, limit)}\n…（预览已截断）` : text }));
    if (text.length > limit) details.append(element("p", { className: "section-note", text: `详细证据共有 ${count(text.length)} 字符。预览仅展示前 ${count(limit)} 字符，完整数据可下载。` }));
    details.append(button(downloadLabel, "button button-small", () => {
      const payload = JSON.stringify({ binding, data: value }, null, 2);
      const url = URL.createObjectURL(new Blob([payload], { type: "application/json;charset=utf-8" }));
      const link = element("a", { attrs: { href: url, download: `callscope-evidence-${shortId(binding.to_snapshot || binding.snapshot_id)}.json` } });
      document.body.append(link); link.click(); link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
    }));
  });
  return details;
}
function queryGapDetails(result, snapshotId) {
  const gaps = Array.isArray(result.gaps) ? result.gaps : [];
  const hasTotal = Number.isInteger(result.gap_count) && result.gap_count >= 0;
  const truncated = result.gaps_truncated === true || (hasTotal && result.gap_count > gaps.length);
  if (!gaps.length && !(hasTotal && result.gap_count > 0) && !truncated) return null;
  const summary = hasTotal ? `解析缺口总计 ${count(result.gap_count)} 项，展示 ${count(gaps.length)} 项样本${truncated ? "（已截断）" : ""}` : `展示 ${count(gaps.length)} 项解析缺口（总数未记录）`;
  const payload = {
    gap_count: hasTotal ? result.gap_count : null,
    returned_sample_count: gaps.length,
    gaps_truncated: typeof result.gaps_truncated === "boolean" ? result.gaps_truncated : truncated ? true : null,
    gap_sample_limit: result.gap_sample_limit ?? null,
    gap_snapshot_id: result.gap_snapshot_id || snapshotId,
    full_gap_evidence: result.full_gap_evidence ?? null,
    status: result.status,
    complete: result.complete,
    completeness_scope: result.completeness_scope,
    gaps,
  };
  return element("div", {}, [
    element("p", { className: "section-note", text: `缺口证据快照：${payload.gap_snapshot_id}。${truncated ? "本响应仅含展示样本，样本截断不改变基于全量缺口的判定。" : ""}${result.full_gap_evidence === "snapshot_edges_diagnostics_and_source_statuses" ? "完整证据出处是同一快照的调用关系、解析诊断及源码文件状态。" : ""}` }),
    jsonDetails(payload, summary, { snapshot_id: snapshotId }, "下载缺口摘要与样本 JSON"),
  ]);
}
function clearCoverage(message = "尚未读取快照范围。当前没有覆盖结论。") {
  const supported = state.status?.capabilities?.languages;
  $("coverage-scope").textContent = `${message}${Array.isArray(supported) ? ` 当前工具提供 ${supported.map(languageLabel).join("、")} 静态前端；这不是当前项目的覆盖结论。` : ""}`;
  $("coverage-languages").replaceChildren(element("p", { className: "section-note", text: "未解析、未支持和失败的源码不会被标记为正常。" }));
  $("coverage-summary").textContent = "未检出不代表功能正确；未分析的源码不在检查范围内。";
  $("coverage-details").hidden = true; $("coverage-details").open = false;
  $("coverage-details-content").replaceChildren();
}
function renderCoverage() {
  if (!state.graph || !state.index) { clearCoverage(); return; }
  const stats = state.graph.stats || {};
  const selected = $("language-filter").value;
  const roots = Array.isArray(stats.source_roots) ? stats.source_roots.join("、") || "空范围" : "未记录";
  const requested = Array.isArray(stats.languages_requested) ? stats.languages_requested.map(languageLabel).join("、") || "未请求语言" : "未记录";
  $("coverage-scope").textContent = `源码根：${roots} · 快照请求：${requested} · 配置范围以外的源码未纳入。`;
  const languages = [...new Set([...Object.keys(stats.by_language || {}).map(normalizeLanguage), ...(stats.languages_requested || []).map(normalizeLanguage), ...state.index.languageCounts.keys()])].sort();
  $("language-filter").replaceChildren(element("option", { text: "所有语言", attrs: { value: "" } }));
  for (const language of languages) $("language-filter").append(element("option", { text: languageLabel(language), attrs: { value: language } }));
  if (languages.includes(selected)) $("language-filter").value = selected;
  const perLanguage = new Map();
  for (const [language, counts] of Object.entries(stats.by_language || {})) if (!perLanguage.has(normalizeLanguage(language))) perLanguage.set(normalizeLanguage(language), counts);
  const cards = $("coverage-languages"); cards.replaceChildren();
  for (const language of languages) {
    const data = perLanguage.get(language);
    const card = button("", "language-coverage", () => { $("language-filter").value = $("language-filter").value === language ? "" : language; changeLanguageFilter(); });
    card.classList.toggle("active", $("language-filter").value === language);
    card.setAttribute("aria-pressed", String($("language-filter").value === language));
    const failed = data?.files_failed;
    const unknownFields = ["dynamic_calls", "ambiguous_calls", "unresolved_calls", "external_callback_boundaries"];
    const unknown = data && unknownFields.every((field) => typeof data[field] === "number") ? unknownFields.reduce((total, field) => total + data[field], 0) : undefined;
    const title = element("div", { className: "language-coverage-title" }, [element("span", { text: languageLabel(language) }), badge(typeof failed === "number" && failed > 0 ? `${count(failed)} 未解析 / 失败` : data ? "范围已记录" : "覆盖未记录", typeof failed === "number" && failed > 0 ? "warning" : "neutral")]);
    card.append(title, element("p", { className: "language-coverage-stats", text: `${numericMetric(data?.files_parsed)} 已解析 / ${numericMetric(data?.files_total)} 文件 · ${count(state.index.languageCounts.get(language) || 0)} 当前图节点 · ${numericMetric(unknown)} 未知 / 边界` }));
    cards.append(card);
  }
  if (!languages.length) cards.append(element("p", { className: "section-note", text: "没有记录语言覆盖；空图不代表项目没有问题。" }));
  const supported = Array.isArray(stats.supported_languages) ? stats.supported_languages.map(languageLabel).join("、") || "无" : "未记录";
  const unsupported = Array.isArray(stats.unsupported_files) ? count(stats.unsupported_files.length) : "未记录";
  const excluded = Array.isArray(stats.excluded_paths) ? count(stats.excluded_paths.length) : "未记录";
  const links = Array.isArray(stats.symlinks_skipped) ? count(stats.symlinks_skipped.length) : "未记录";
  const ruleCount = numericMetric(stats.rules_count), entryCount = numericMetric(stats.entrypoints_count);
  $("coverage-summary").textContent = `本快照分析器支持：${supported} · 未支持文件 ${unsupported} · 排除路径 ${excluded}（可能为目录） · 跳过链接 ${links} · 显式约束 ${ruleCount} · 配置入口 ${entryCount}。${stats.rules_count === 0 ? " 未配置显式约束，发现限于结构事实与解析诊断。" : ""} 声明解析成功不代表回调、宏、trait/interface 分派或跨语言关系已覆盖。${$("language-filter").value ? ` 当前筛选 ${languageLabel($("language-filter").value)}，统计卡仍表示完整快照；无源码语言的全局发现仍保留。` : ""}`;
  const details = $("coverage-details");
  const hasDetails = (stats.unsupported_files?.length || 0) + (stats.excluded_paths?.length || 0) + (stats.scan_errors?.length || 0) + (stats.symlinks_skipped?.length || 0) + Object.keys(stats.component_versions || {}).length;
  details.hidden = !hasDetails;
  $("coverage-details-content").replaceChildren();
  if (details.open && hasDetails) renderCoverageDetails();
}
function renderCoverageDetails() {
  const target = $("coverage-details-content");
  if (!state.graph || target.childNodes.length) return;
  const stats = state.graph.stats || {};
  if (stats.excluded_paths?.length) {
    target.append(element("h3", { className: "panel-subtitle", text: `排除路径 · ${count(stats.excluded_paths.length)} 项（可能包含未枚举的目录内容）` }));
    appendBatched(stats.excluded_paths, target, (path) => element("div", { className: "coverage-file-row" }, [badge("未分析", "neutral"), element("code", { text: path })]), 40);
  }
  if (stats.unsupported_files?.length) {
    target.append(element("h3", { className: "panel-subtitle", text: `未支持文件 · ${count(stats.unsupported_files.length)}` }));
    appendBatched(stats.unsupported_files, target, (file) => element("div", { className: "coverage-file-row" }, [badge(file.language || "未支持", "neutral"), element("code", { text: file.path || file })]), 40);
  }
  if (stats.symlinks_skipped?.length) {
    target.append(element("h3", { className: "panel-subtitle", text: `跳过符号链接 · ${count(stats.symlinks_skipped.length)} 项` }));
    appendBatched(stats.symlinks_skipped, target, (path) => element("div", { className: "coverage-file-row" }, [badge("未读取", "neutral"), element("code", { text: path })]), 40);
  }
  if (stats.scan_errors?.length) {
    target.append(element("h3", { className: "panel-subtitle", text: `读取 / 扫描错误 · ${count(stats.scan_errors.length)}` }));
    appendBatched(stats.scan_errors, target, (error) => element("div", { className: "coverage-file-row" }, [badge("扫描错误", "warning"), element("span", { text: typeof error === "string" ? error : `${error.file || error.path || ""} ${error.message || error.error || JSON.stringify(error)}` })]), 40);
  }
  if (stats.component_versions) target.append(jsonDetails({ component_versions: stats.component_versions, limitations: stats.limitations || [] }, "快照分析器版本与声明边界"));
}
function changeLanguageFilter() {
  state.page = 0; state.reviewCache.key = "";
  $("module-filter").value = "";
  renderCoverage(); renderFilters(); renderReview(); renderGraph();
}
function showToast(message, error = false) {
  clearTimeout(state.toastTimer);
  $("toast").textContent = message;
  $("toast").classList.toggle("error", error);
  $("toast").hidden = false;
  state.toastTimer = setTimeout(() => { $("toast").hidden = true; }, error ? 6500 : 4000);
}
function showGlobalError(message) {
  $("global-error").textContent = message;
  $("global-error").hidden = !message;
}
async function api(path, options = {}) {
  const response = await fetch(`/api/v1${path}`, { cache: "no-store", ...options, headers: { "Accept": "application/json", ...(options.body ? { "Content-Type": "application/json" } : {}), ...options.headers } });
  let data;
  try { data = await response.json(); } catch (_) { throw new Error(`服务未返回有效 JSON（HTTP ${response.status}）`); }
  if (!response.ok) throw new Error(data.error?.message || (typeof data.error === "string" ? data.error : "") || `请求失败（HTTP ${response.status}）`);
  if (data.error) throw new Error(data.error.message || String(data.error));
  return data;
}
function post(path, payload) { return api(path, { method: "POST", body: JSON.stringify(payload) }); }
function snapshotQuery(extra = {}) { return new URLSearchParams({ snapshot_id: state.snapshotId, ...extra }).toString(); }

function setBusy(busy) {
  state.busy = busy;
  $("scan-button").disabled = busy;
  $("snapshot-select").disabled = busy;
  $("config-rescan").disabled = busy;
  $("scan-button").querySelector("span").textContent = busy ? "正在扫描源码" : "扫描项目";
  $("scan-button").querySelector("svg").classList.toggle("spinning", busy);
}
function switchView(view) {
  state.view = view;
  for (const section of document.querySelectorAll(".view")) section.hidden = section.id !== `view-${view}`;
  for (const nav of document.querySelectorAll("[data-view]")) {
    const selected = nav.dataset.view === view;
    nav.classList.toggle("active", selected);
    if (selected) nav.setAttribute("aria-current", "page"); else nav.removeAttribute("aria-current");
  }
  $("breadcrumb").textContent = { explore: "调用结构", history: "版本对比", rules: "分析规则" }[view];
  closeDrawer(false);
}
function renderStatus() {
  const status = state.status;
  const analyzing = ["running", "analyzing"].includes(status?.analysis?.state);
  const failed = status?.analysis?.state === "failed";
  const configError = status?.analysis?.config_error || status?.config_error;
  $("connection-state").textContent = !status ? "服务未连接" : failed ? "上次分析失败" : configError ? "项目配置异常" : analyzing ? "分析进行中" : "本地服务已连接";
  $("connection-state").classList.toggle("error", !status || failed || !!configError);
  $("side-project").textContent = status?.project?.name || state.graph?.snapshot?.project_name || "未连接项目";
  $("side-root").textContent = status?.project?.root || state.graph?.snapshot?.root || "检查服务是否已启动";
  $("side-root").title = $("side-root").textContent;
  const messages = [];
  if (analyzing) messages.push("正在只读扫描源码。当前页面展示的是此前已发布的快照。");
  if (failed || status?.analysis?.last_error) messages.push(`上次分析失败，已发布快照仍可查看。${status.analysis.last_error || "请查看服务日志。"}`);
  if (configError) messages.push(`项目配置无法读取：${configError}`);
  $("service-warning").textContent = messages.join(" ");
  $("service-warning").hidden = !messages.length;
  const capabilities = status?.capabilities;
  const engine = capabilities?.maintenance_engine;
  const detection = capabilities?.global_detection === "full" ? "全量检测" : "检测方式未记录";
  const mode = engine === "full" ? `全量解析·${detection}` : engine === "cocoindex" ? `${capabilities.incremental_granularity === "language" ? "语言缓存" : "缓存粒度未记录"}·${capabilities.global_detection === "full" ? "检测全量" : "检测方式未记录"}` : "";
  const lastRun = maintenanceRunLabel(status?.analysis?.maintenance);
  $("maintenance-status").textContent = mode ? `当前服务：${mode}。${lastRun ? ` 最近成功维护：${lastRun}。` : " 尚未记录成功维护。"} 维护运行信息不属于所选快照统计。` : "";
  $("maintenance-status").hidden = !mode;
}
async function refreshStatus() {
  try { state.status = await api("/status"); renderStatus(); return state.status; }
  catch (error) { state.status = null; renderStatus(); throw error; }
}
function fillVersions() {
  const selected = state.snapshotId;
  const previousDiff = { from: $("diff-from").value, to: $("diff-to").value };
  for (const id of ["snapshot-select", "diff-from", "diff-to"]) {
    const select = $(id);
    select.replaceChildren();
    if (!state.versions.length) select.append(element("option", { text: "尚无分析快照", attrs: { value: "" } }));
    else for (const snapshot of state.versions) select.append(element("option", { text: snapshotLabel(snapshot), attrs: { value: snapshot.id } }));
  }
  if (selected && state.versions.some((item) => item.id === selected)) $("snapshot-select").value = selected;
  if (state.versions.length) {
    $("diff-to").value = state.versions.some((item) => item.id === previousDiff.to) ? previousDiff.to : state.versions[0].id;
    $("diff-from").value = state.versions.some((item) => item.id === previousDiff.from) ? previousDiff.from : (state.versions[1]?.id || state.versions[0].id);
  }
  $("diff-button").disabled = state.versions.length < 2;
  $("version-count").textContent = `${count(state.versions.length)} 个不可变快照`;
  renderVersionList();
}
async function refreshVersions() {
  const data = await api("/versions");
  state.versions = Array.isArray(data.items) ? data.items.sort((a, b) => String(b.created_at).localeCompare(String(a.created_at))) : [];
  fillVersions();
  return state.versions;
}
function renderVersionList() {
  const target = $("version-list");
  target.replaceChildren();
  if (!state.versions.length) { target.append(emptyState("暂无快照", "先扫描项目，创建第一份静态分析记录。", "clock")); return; }
  for (const snapshot of state.versions) {
    const meta = element("div", { className: "version-meta" }, [
      element("code", { text: shortId(snapshot.id) }),
      document.createTextNode(` · ${count(snapshot.stats?.nodes)} 节点 · ${count(snapshot.finding_count)} 发现 · ${snapshot.analyzer_version || "分析器版本未知"}`),
    ]);
    const info = element("div", {}, [element("div", { className: "version-title", text: `${formatTime(snapshot.created_at)} · ${snapshot.project_name || "项目"}` }), meta]);
    const open = button("查看快照", "button button-small", () => { switchView("explore"); loadSnapshot(snapshot.id); });
    const row = element("div", { className: "version-row" }, [element("span", { className: "version-mark" }, [icon("clock")]), info, open]);
    target.append(row);
  }
}

async function loadSnapshot(id) {
  const request = ++state.request;
  state.graphRequest++;
  closeDrawer(false);
  if ($("source-dialog").open) $("source-dialog").close();
  state.snapshotId = id || "";
  state.graph = null; state.findings = []; state.decisions = []; state.path = null; state.subset = null;
  state.index = null; state.reviewCache = { key: "", items: [] };
  state.latestDecisions.clear(); state.decisionsByFinding.clear();
  state.findingsError = ""; state.decisionsError = ""; state.page = 0;
  $("path-result").replaceChildren();
  $("module-filter").value = "";
  clearCoverage("正在读取所选快照的扫描范围…");
  if (!id) { renderEmptySnapshot(); return; }
  $("review-list").replaceChildren(element("div", { className: "loading-text", text: "正在读取快照和静态证据…" }));
  $("graph-empty").hidden = false;
  $("graph-empty").querySelector("strong").textContent = "正在读取调用图";
  $("graph-empty").querySelector("p").textContent = "读取完成后显示该版本的静态调用关系。";
  $("graph-content").replaceChildren();
  for (const metric of ["metric-nodes", "metric-edges", "metric-findings", "metric-unknown"]) $(metric).textContent = "—";
  const query = new URLSearchParams({ snapshot_id: id }).toString();
  const results = await Promise.allSettled([api(`/graph?${query}`), api(`/anomalies?${query}`), api(`/decisions?${query}`)]);
  if (request !== state.request) return;
  if (results[0].status !== "fulfilled") {
    showGlobalError(`无法读取快照：${results[0].reason.message}`);
    renderEmptySnapshot("快照读取失败", "检查服务连接后重新选择快照或扫描。");
    return;
  }
  const graph = results[0].value;
  if (!graph.snapshot || graph.snapshot.id !== id || !Array.isArray(graph.nodes) || !Array.isArray(graph.edges)) {
    showGlobalError("图响应缺少快照、节点或边，无法安全呈现分析结果。");
    renderEmptySnapshot("分析响应不完整", "请检查本地服务日志。");
    return;
  }
  state.graph = graph;
  if (results[1].status === "fulfilled" && results[1].value.snapshot_id === id && Array.isArray(results[1].value.items) && results[1].value.items.every((item) => !item.snapshot_id || item.snapshot_id === id)) state.findings = results[1].value.items;
  else state.findingsError = results[1].status === "rejected" ? results[1].reason.message : "发现响应缺少 items";
  if (results[2].status === "fulfilled" && Array.isArray(results[2].value.items) && results[2].value.items.every((item) => !item.snapshot_id || item.snapshot_id === id)) state.decisions = results[2].value.items;
  else state.decisionsError = results[2].status === "rejected" ? results[2].reason.message : "人工处置响应不完整";
  showGlobalError("");
  $("snapshot-select").value = id;
  buildIndexes();
  renderCoverage(); renderMetrics(); renderFilters(); renderReview(); renderGraph(); renderStatus();
}
function renderEmptySnapshot(title = "尚无分析快照", message = "点击「扫描项目」，只读源码并建立调用关系。") {
  $("snapshot-status").textContent = "等待分析";
  $("snapshot-status").className = "badge badge-neutral";
  $("snapshot-time").textContent = "—";
  $("snapshot-id").textContent = "—";
  $("analysis-warning").hidden = true;
  clearCoverage();
  for (const metric of ["metric-nodes", "metric-edges", "metric-findings", "metric-unknown"]) $(metric).textContent = "—";
  $("metric-findings").classList.remove("danger");
  $("metric-files").textContent = "等待源码分析";
  $("metric-severity").textContent = "事实与人工处置分别保留";
  $("findings-count").textContent = "—";
  $("review-list").replaceChildren(emptyState(title, message));
  $("list-summary").textContent = "尚无可展示结果";
  $("page-prev").disabled = true; $("page-next").disabled = true;
  $("graph-empty").hidden = false;
  $("graph-empty").querySelector("strong").textContent = title;
  $("graph-empty").querySelector("p").textContent = message;
  $("graph-content").replaceChildren();
  $("graph-coverage").textContent = "未分析区域不会被标记为正常";
  $("graph-back").hidden = true;
  $("node-options").replaceChildren();
}
function effectiveDecision(finding) {
  const latest = state.latestDecisions.get(finding.id) || finding.decision || finding.latest_decision;
  if (!latest || !Object.hasOwn(ACTIONS, latest.action) || (latest.expires_at && new Date(latest.expires_at).getTime() <= Date.now())) return null;
  return latest;
}
function renderMetrics() {
  const graph = state.graph;
  if (!graph) return;
  const stats = graph.stats || {};
  const snapshot = graph.snapshot;
  $("snapshot-id").textContent = shortId(snapshot.id);
  $("snapshot-id").title = snapshot.id;
  $("snapshot-time").textContent = formatTime(snapshot.created_at);
  const partial = isPartial({ ...snapshot, stats });
  $("snapshot-status").textContent = partial ? "部分分析" : "已完成 · 限定范围";
  $("snapshot-status").className = `badge badge-${partial ? "warning" : "neutral"}`;
  $("metric-nodes").textContent = count(graph.nodes.length);
  $("metric-files").textContent = `${numericMetric(stats.files_parsed)} 已解析 / ${numericMetric(stats.files_total)} 个源码文件`;
  $("metric-edges").textContent = count(state.index?.resolved ?? graph.edges.filter((edge) => edge.resolution === "resolved").length);
  $("metric-unknown").textContent = count(unknownEdges().length);
  const pending = state.findings.filter((item) => !effectiveDecision(item)).length;
  $("metric-findings").textContent = state.findingsError ? "—" : count(pending);
  $("metric-findings").classList.toggle("danger", !state.findingsError && state.findings.some((item) => isRuleViolation(item) && !effectiveDecision(item)));
  const high = state.findings.filter((item) => ["high", "critical"].includes(item.severity)).length;
  $("metric-severity").textContent = state.findingsError ? "发现数据读取失败" : `共 ${count(state.findings.length)} 项 · ${count(high)} 项高严重度`;
  const warnings = [];
  if (stats.coverage_incomplete || stats.files_failed > 0 || stats.scan_errors?.length) warnings.push("当前源码覆盖不完整，请查看失败文件、跳过路径与分析日志。");
  else if (partial && !unknownEdges().length) warnings.push("快照标记为部分分析，请结合扫描范围与分析日志解释结果。");
  if (unknownEdges().length) warnings.push(`${count(unknownEdges().length)} 处未知调用或外部边界；无确定路径不能直接解释为功能缺失。`);
  if (stats.rules_count === 0) warnings.push("此快照没有显式调用约束。未检出规则违规不表示调用结构完整。");
  if (state.findingsError) warnings.push(`发现未成功读取：${state.findingsError}`);
  if (state.decisionsError) warnings.push("人工处置未成功读取，部分处置状态可能暂时不可见。");
  const banner = $("analysis-warning");
  banner.replaceChildren(icon("warning"), element("span", { text: warnings.join(" ") }));
  banner.hidden = !warnings.length;
}
function renderFilters() {
  const type = $("type-filter").value;
  $("type-filter").replaceChildren(element("option", { text: "所有类型", attrs: { value: "" } }));
  for (const value of [...new Set(state.findings.map((item) => item.type))].sort()) $("type-filter").append(element("option", { text: TYPE_LABELS[value] || value, attrs: { value } }));
  if ([...$("type-filter").options].some((option) => option.value === type)) $("type-filter").value = type;
  const currentModule = $("module-filter").value;
  const language = $("language-filter").value;
  $("module-filter").replaceChildren(element("option", { text: "所有模块", attrs: { value: "" } }));
  for (const module of [...new Set(state.graph.nodes.filter((node) => !language || nodeLanguage(node) === language).map((item) => item.module))].filter(Boolean).sort()) $("module-filter").append(element("option", { text: module, attrs: { value: module } }));
  if ([...$("module-filter").options].some((option) => option.value === currentModule)) $("module-filter").value = currentModule;
  $("node-options").replaceChildren();
  // Native suggestions are bounded; manually entered IDs still query the entire snapshot.
  const fragment = document.createDocumentFragment();
  for (const node of state.graph.nodes.slice(0, 3000)) fragment.append(element("option", { attrs: { value: node.id }, text: node.signature || node.name }));
  $("node-options").append(fragment);
  $("path-form").querySelector("p").textContent = `查询一条最短静态确定路径，不受工作台语言筛选影响；无路径不一定代表无法调用。${state.graph.nodes.length > 3000 ? " 候选建议仅列前 3,000 个符号；输入完整符号 ID 可查询所有节点。" : ""}`;
}
function reviewItems() {
  const q = $("finding-search").value.trim().toLocaleLowerCase();
  const language = $("language-filter").value;
  const key = JSON.stringify([state.snapshotId, state.review, q, language, $("type-filter").value, $("severity-filter").value]);
  if (state.reviewCache.key === key) return state.reviewCache.items;
  let items;
  if (state.review === "findings") items = state.findings.filter((item) => {
    if ($("type-filter").value && item.type !== $("type-filter").value) return false;
    if ($("severity-filter").value && item.severity !== $("severity-filter").value) return false;
    const languages = state.findingsLanguages.get(item.id);
    if (language && languages?.size && !languages.has(language) && !languages.has("unknown")) return false;
    return !q || (state.findingsSearch.get(item.id) || "").includes(q);
  });
  else items = (state.review === "unknown" ? unknownEdges() : state.graph?.diagnostics || []).filter((item) => {
    const itemLanguage = state.review === "unknown" ? state.index?.edgeLanguages.get(item.id) : fileLanguage(item.file);
    if (language && itemLanguage && itemLanguage !== "unknown" && itemLanguage !== language) return false;
    const search = state.review === "unknown" ? state.index?.edgeSearch.get(item.id) : state.index?.diagnosticSearch.get(item);
    return !q || (search || "").includes(q);
  });
  state.reviewCache = { key, items };
  return items;
}
function renderReview() {
  if (!state.graph) return;
  $("finding-selects").hidden = state.review !== "findings";
  for (const tab of document.querySelectorAll("[data-review]")) {
    const active = tab.dataset.review === state.review;
    tab.classList.toggle("active", active); tab.setAttribute("aria-selected", String(active)); tab.tabIndex = active ? 0 : -1;
  }
  $("review-list").setAttribute("aria-labelledby", `tab-${state.review}`);
  const items = reviewItems();
  state.page = Math.min(state.page, Math.max(0, Math.ceil(items.length / PAGE_SIZE) - 1));
  const offset = state.page * PAGE_SIZE;
  const list = $("review-list");
  list.replaceChildren();
  const failed = state.review === "findings" && !!state.findingsError;
  $("findings-count").textContent = failed ? "—" : count(items.length);
  if (state.review === "findings" && state.findingsError) list.append(emptyState("发现读取失败", state.findingsError));
  else if (!items.length) {
    const filtered = $("finding-search").value || $("type-filter").value || $("severity-filter").value || $("language-filter").value;
    const titles = { findings: filtered ? "没有匹配的发现" : "本次未检出发现", unknown: "没有匹配的未解析调用", diagnostics: "没有分析诊断" };
    const notes = { findings: filtered ? "调整筛选条件，查看其他结果。" : "结论限于当前分析范围与已配置规则，不等于功能正确。", unknown: "普通外部调用是显式模型的终点；存在未知回调的外部调用仍列为分析边界。", diagnostics: "当前快照未记录文件解析问题。" };
    list.append(emptyState(titles[state.review], notes[state.review]));
  } else for (const item of items.slice(offset, offset + PAGE_SIZE)) {
    if (state.review === "findings") list.append(findingCard(item));
    else if (state.review === "unknown") list.append(callCard(item));
    else list.append(diagnosticCard(item));
  }
  $("list-summary").textContent = failed ? "发现读取失败，数量未知" : items.length ? `${offset + 1}–${Math.min(offset + PAGE_SIZE, items.length)} / ${count(items.length)} 项${$("language-filter").value ? " · 语言筛选" : ""}` : "0 项";
  $("page-prev").disabled = state.page === 0;
  $("page-next").disabled = offset + PAGE_SIZE >= items.length;
  list.scrollTop = 0;
}
function findingCard(item) {
  const card = button("", "finding-item", () => selectFinding(item));
  card.classList.toggle("selected", state.selected?.kind === "finding" && state.selected.id === item.id);
  const top = element("div", { className: "finding-topline" }, [badge(`${SEVERITIES[item.severity] || item.severity}严重度`, isRuleViolation(item) ? "danger" : "neutral"), element("span", { text: findingStatus(item) })]);
  const disposition = effectiveDecision(item);
  if (disposition) top.append(element("span", { className: "decision-label", text: ACTIONS[disposition.action] || disposition.action }));
  top.append(element("span", { className: "finding-type", text: findingLabel(item) }));
  card.append(top, element("div", { className: "finding-title" }, [element("i", { className: `indicator${isRuleViolation(item) ? " high" : ""}` }), element("span", { text: item.title })]));
  const location = item.evidence?.flatMap((entry) => entry.locations || []).find((entry) => entry.file);
  const label = location ? `${location.file}:${location.line || 1}` : item.node_ids?.[0] || item.rule_id || "查看静态证据";
  card.append(element("div", { className: "finding-location" }, [element("code", { text: label })]));
  return card;
}
function callCard(edge) {
  const card = button("", "finding-item", () => selectCall(edge));
  card.classList.toggle("selected", state.selected?.kind === "call" && state.selected.id === edge.id);
  card.append(element("div", { className: "finding-topline" }, [badge(resolutionLabel(edge), "neutral"), element("span", { className: "finding-type", text: "解析依据待确认" })]), element("div", { className: "finding-title" }, [element("i", { className: "indicator" }), element("code", { text: edge.expression || "调用表达式" })]), element("div", { className: "finding-location", text: `${edge.file}:${edge.line} · ${edge.source}` }));
  return card;
}
function diagnosticCard(item) {
  return element("div", { className: "diagnostic-item" }, [badge(item.code || item.level || "诊断", ["error", "warning"].includes(item.level) ? "warning" : "neutral"), element("p", { text: item.message }), item.file ? button(`${item.file}${item.line ? `:${item.line}` : ""}`, "location-link", () => { openSourceOnly(item.file, item.line || 1); }) : null]);
}

function graphSelection() {
  const fullNodes = state.graph?.nodes || [];
  const fullEdges = state.graph?.edges || [];
  const module = $("module-filter").value;
  const language = $("language-filter").value;
  const pool = state.subset?.nodes || fullNodes;
  const edges = state.subset?.edges || fullEdges;
  const degree = state.subset ? new Map() : state.index?.degree || new Map();
  if (state.subset) for (const edge of edges) {
      degree.set(edge.source, (degree.get(edge.source) || 0) + 1);
      if (edge.target) degree.set(edge.target, (degree.get(edge.target) || 0) + 1);
  }
  const violations = state.violationNodeIds;
  const pathNodes = new Set(state.path?.node_ids || []);
  const selectedNodes = new Set(state.selected?.nodeIds || []);
  const filtered = pool.filter((node) => (!module || node.module === module) && (!language || nodeLanguage(node) === language));
  const scores = new Map();
  for (const node of filtered) scores.set(node.id, (pathNodes.has(node.id) ? 1e7 : 0) + (node.id === state.selected?.id || selectedNodes.has(node.id) ? 1e6 : 0) + (violations.has(node.id) ? 1e5 : 0) + (degree.get(node.id) || 0));
  const ranked = [...filtered].sort((a, b) => {
    return scores.get(b.id) - scores.get(a.id) || a.id.localeCompare(b.id);
  });
  const chosen = ranked.slice(0, GRAPH_LIMIT);
  const chosenIds = new Set(chosen.map((node) => node.id));
  const internalEdges = edges.filter((edge) => chosenIds.has(edge.source) && chosenIds.has(edge.target));
  const pathEdgeIds = new Set(state.path?.edge_ids || []);
  const edgeScore = (edge) => (pathEdgeIds.has(edge.id) ? 1e6 : 0) + (state.violationEdgeIds.has(edge.id) ? 1e5 : 0) + (selectedNodes.has(edge.source) || selectedNodes.has(edge.target) ? 1e4 : 0);
  internalEdges.sort((a, b) => edgeScore(b) - edgeScore(a) || a.id.localeCompare(b.id));
  const selectedEdges = internalEdges.slice(0, GRAPH_EDGE_LIMIT);
  const unknown = edges.filter((edge) => chosenIds.has(edge.source) && uncertainEdge(edge) && !chosenIds.has(edge.target));
  unknown.sort((a, b) => Number(b.id === state.selected?.id) - Number(a.id === state.selected?.id) || a.id.localeCompare(b.id));
  const ghosts = $("show-unknown").checked ? unknown.slice(0, UNKNOWN_GRAPH_LIMIT).map((edge) => ({ id: `unknown:${edge.id}`, name: edge.expression, module: state.index?.nodes.get(edge.source)?.module || "未解析", kind: "unknown", edge, qualname: edge.expression })) : [];
  for (const ghost of ghosts) selectedEdges.push({ ...ghost.edge, target: ghost.id });
  return { nodes: [...chosen, ...ghosts], edges: selectedEdges, totalNodes: fullNodes.length, totalEdges: fullEdges.length, eligible: filtered.length, chosen: chosen.length, hiddenUnknown: Math.max(0, unknown.length - ghosts.length), violations };
}
function renderGraph(reset = true) {
  const content = $("graph-content");
  content.replaceChildren();
  if (!state.graph) return;
  const selection = graphSelection();
  state.displayNodes = selection.nodes;
  state.displayEdges = selection.edges;
  state.displayEdgeIndex = new Map(selection.edges.map((edge) => [edge.id, edge]));
  state.positions.clear();
  $("graph-empty").hidden = !!selection.nodes.length;
  if (!selection.nodes.length) {
    $("graph-empty").querySelector("strong").textContent = "当前范围没有代码节点";
    $("graph-empty").querySelector("p").textContent = "调整模块筛选，或查看分析日志确认源码解析范围。";
  }
  const modules = new Map();
  for (const node of selection.nodes) {
    const module = node.module || "未分组";
    if (!modules.has(module)) modules.set(module, []);
    modules.get(module).push(node);
  }
  const sortedModules = [...modules.entries()].sort((a, b) => b[1].length - a[1].length || a[0].localeCompare(b[0]));
  const columns = [35, 380, 725];
  const bottoms = [30, 30, 30];
  const backgrounds = svgElement("g", { "aria-hidden": "true" });
  const edgeGroup = svgElement("g", { "aria-hidden": "true" });
  const nodeGroup = svgElement("g");
  content.append(backgrounds, edgeGroup, nodeGroup);
  for (const [module, nodes] of sortedModules) {
    const column = bottoms.indexOf(Math.min(...bottoms));
    const x = columns[column];
    const y = bottoms[column];
    nodes.sort((a, b) => a.id.localeCompare(b.id));
    const height = 55 + nodes.length * 35;
    backgrounds.append(svgElement("rect", { x, y, width: 305, height, class: "graph-group-box", rx: 12 }), svgElement("text", { x: x + 17, y: y + 25, class: "graph-group-label" }, truncate(module, 38)));
    nodes.forEach((node, index) => state.positions.set(node.id, { x: x + 152, y: y + 53 + index * 35 }));
    bottoms[column] += height + 20;
  }
  state.graphWidth = 1065;
  state.graphHeight = Math.max(600, ...bottoms);
  $("graph-svg").setAttribute("viewBox", `0 0 ${state.graphWidth} ${state.graphHeight}`);
  const violationEdges = state.violationEdgeIds;
  const pathEdges = new Set(state.path?.edge_ids || []);
  const selectedNodeIds = new Set(state.selected?.nodeIds || []);
  for (const edge of selection.edges) {
    const classes = ["graph-edge"];
    if (edge.resolution !== "resolved") classes.push("unknown");
    if (violationEdges.has(edge.id)) classes.push("violation");
    if (pathEdges.has(edge.id)) classes.push("path");
    else if (pathEdges.size) classes.push("dimmed");
    const marker = pathEdges.has(edge.id) ? "path" : violationEdges.has(edge.id) ? "danger" : "neutral";
    const path = svgElement("path", { class: classes.join(" "), "data-edge-id": edge.id, "marker-end": `url(#arrow-${marker})`, d: edgePath(edge) });
    path.append(svgElement("title", {}, `${edge.source} → ${edge.target} · ${RESOLUTIONS[edge.resolution] || "未知"} · ${edge.file}:${edge.line}`));
    edgeGroup.append(path);
  }
  for (const node of selection.nodes) {
    const p = state.positions.get(node.id);
    const classes = ["graph-node"];
    if (node.kind === "unknown") classes.push("unknown");
    if (selection.violations.has(node.id)) classes.push("violation");
    if (state.path?.node_ids?.includes(node.id)) classes.push("path");
    if (state.selected?.id === node.id || selectedNodeIds.has(node.id) || node.edge?.id === state.selected?.id) classes.push("selected");
    const name = node.kind === "module" || node.kind === "module_init" ? "⟨模块顶层⟩" : node.name || node.id;
    const group = svgElement("g", { class: classes.join(" "), transform: `translate(${p.x},${p.y})`, "data-node-id": node.id, tabindex: "0", role: "button", "aria-label": node.kind === "unknown" ? `未知调用：${node.name}` : `查看 ${node.qualname || node.id}，${node.file}:${node.line}` });
    group.append(svgElement("title", {}, node.kind === "unknown" ? `${node.name}\n${node.edge.reason}` : `${node.qualname || node.id}\n${node.file}:${node.line}`), svgElement("rect", { x: -129, y: -13, width: 258, height: 27, rx: 5, class: "node-back" }), svgElement("circle", { cx: -112, cy: 0, r: 4.5, class: "node-dot" }), svgElement("text", { x: -100, y: 3.5, class: "node-name" }, truncate(name, 33)));
    group.addEventListener("click", (event) => {
      // Assistive technology can activate SVG buttons using a synthetic click.
      if (event.detail === 0) { if (node.kind === "unknown") selectCall(node.edge); else selectNode(node.id); }
    });
    group.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") { event.preventDefault(); if (node.kind === "unknown") selectCall(node.edge); else selectNode(node.id); }
    });
    nodeGroup.append(group);
  }
  if (reset) state.transform = { x: 0, y: 0, scale: 1 };
  applyTransform();
  const omitted = selection.totalNodes - selection.chosen;
  const omittedEdges = Math.max(0, selection.totalEdges - selection.edges.length);
  $("graph-coverage").textContent = `节点 ${count(selection.chosen)} / ${count(selection.totalNodes)}（${count(omitted)} 未显示）；边 ${count(selection.edges.length)} / ${count(selection.totalEdges)}（${count(omittedEdges)} 未显示）；未知占位 ${selection.nodes.length - selection.chosen}。绘图上限 ${GRAPH_LIMIT} 节点 / ${GRAPH_EDGE_LIMIT} 内部边；全部未知关系可在列表查看。`;
  if (state.subset) {
    const parts = ["两跳关联子图", "浏览范围不改变检测范围"];
    if (state.subset.truncated) parts.push("已达深度展示边界");
    if (Number.isInteger(state.subset.gap_count) && state.subset.gap_count > 0) parts.push(`解析缺口总计 ${count(state.subset.gap_count)} 项，响应展示 ${count(state.subset.gaps?.length || 0)} 项样本${state.subset.gaps_truncated ? "（已截断）" : ""}`);
    $("graph-subtitle").textContent = parts.join(" · ");
  } else $("graph-subtitle").textContent = $("module-filter").value || $("language-filter").value ? "筛选视图 · 边仅包含两端均显示的关系" : "模块分组 · 绘图截取不改变完整快照的检测结果";
  $("graph-back").hidden = !state.subset && !state.path;
}
function truncate(text, length) { const value = String(text || ""); return value.length > length ? `${value.slice(0, length - 1)}…` : value; }
function edgePath(edge) {
  const from = state.positions.get(edge.source), to = state.positions.get(edge.target);
  if (!from || !to) return "";
  if (edge.source === edge.target) return `M ${from.x + 124} ${from.y - 4} C ${from.x + 167} ${from.y - 30}, ${from.x + 167} ${from.y + 30}, ${from.x + 124} ${from.y + 6}`;
  if (Math.abs(from.x - to.x) < 10) {
    const right = from.y <= to.y;
    const sign = right ? 1 : -1;
    const sx = from.x + sign * 125, tx = to.x + sign * 125;
    const cx = sx + sign * (20 + Math.min(65, Math.abs(from.y - to.y) / 5));
    return `M ${sx} ${from.y} C ${cx} ${from.y}, ${cx} ${to.y}, ${tx} ${to.y}`;
  }
  const sign = to.x > from.x ? 1 : -1;
  const sx = from.x + 126 * sign, tx = to.x - 131 * sign;
  const bend = Math.max(30, Math.abs(tx - sx) * .55);
  return `M ${sx} ${from.y} C ${sx + bend * sign} ${from.y}, ${tx - bend * sign} ${to.y}, ${tx} ${to.y}`;
}
function applyTransform() {
  const t = state.transform;
  $("graph-content").setAttribute("transform", `translate(${t.x},${t.y}) scale(${t.scale})`);
}
function svgPoint(event) {
  const point = $("graph-svg").createSVGPoint(); point.x = event.clientX; point.y = event.clientY;
  const matrix = $("graph-svg").getScreenCTM();
  return matrix ? point.matrixTransform(matrix.inverse()) : { x: 0, y: 0 };
}
function zoomGraph(multiplier, position) {
  const t = state.transform;
  const scale = Math.max(.06, Math.min(32, t.scale * multiplier));
  const center = position || { x: state.graphWidth / 2, y: state.graphHeight / 2 };
  const ratio = scale / t.scale;
  state.transform = { x: center.x - (center.x - t.x) * ratio, y: center.y - (center.y - t.y) * ratio, scale };
  applyTransform();
}
function bindGraphInteractions() {
  const svg = $("graph-svg");
  svg.addEventListener("keydown", (event) => {
    if (!["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown", "+", "=", "-", "Home"].includes(event.key)) return;
    event.preventDefault();
    const offsets = { ArrowLeft: [45, 0], ArrowRight: [-45, 0], ArrowUp: [0, 45], ArrowDown: [0, -45] };
    if (offsets[event.key]) { state.transform.x += offsets[event.key][0]; state.transform.y += offsets[event.key][1]; applyTransform(); }
    else if (event.key === "Home") { state.transform = { x: 0, y: 0, scale: 1 }; applyTransform(); }
    else zoomGraph(event.key === "-" ? .8 : 1.25);
  });
  svg.addEventListener("wheel", (event) => { if (!state.graph) return; event.preventDefault(); zoomGraph(event.deltaY < 0 ? 1.13 : .885, svgPoint(event)); }, { passive: false });
  svg.addEventListener("pointerdown", (event) => {
    if (event.button !== 0 || !state.graph) return;
    const node = event.target.closest(".graph-node");
    const id = node?.dataset.nodeId;
    const point = svgPoint(event);
    state.drag = { pointer: event.pointerId, start: point, last: point, id, position: id ? { ...state.positions.get(id) } : null, transform: { ...state.transform }, moved: false };
    svg.setPointerCapture(event.pointerId); svg.classList.add("dragging");
  });
  svg.addEventListener("pointermove", (event) => {
    const drag = state.drag;
    if (!drag || drag.pointer !== event.pointerId) return;
    const point = svgPoint(event);
    const dx = point.x - drag.start.x, dy = point.y - drag.start.y;
    if (Math.abs(dx) + Math.abs(dy) > 3) drag.moved = true;
    if (drag.id) {
      const position = { x: drag.position.x + dx / state.transform.scale, y: drag.position.y + dy / state.transform.scale };
      state.positions.set(drag.id, position);
      for (const node of svg.querySelectorAll(".graph-node")) if (node.dataset.nodeId === drag.id) node.setAttribute("transform", `translate(${position.x},${position.y})`);
      for (const path of svg.querySelectorAll(".graph-edge")) {
        const edge = state.displayEdgeIndex.get(path.dataset.edgeId);
        if (edge && (edge.source === drag.id || edge.target === drag.id)) path.setAttribute("d", edgePath(edge));
      }
    } else { state.transform.x = drag.transform.x + dx; state.transform.y = drag.transform.y + dy; applyTransform(); }
  });
  const release = (event) => {
    if (state.drag?.pointer !== event.pointerId) return;
    const wasDrag = state.drag;
    if (svg.hasPointerCapture(event.pointerId)) svg.releasePointerCapture(event.pointerId);
    svg.classList.remove("dragging");
    if (!wasDrag.moved && wasDrag.id) {
      const node = state.displayNodes.find((entry) => entry.id === wasDrag.id);
      // Pointer capture retargets clicks to the canvas. Explicitly select here.
      if (node?.kind === "unknown") selectCall(node.edge); else if (node) selectNode(node.id);
    }
    setTimeout(() => { if (state.drag === wasDrag) state.drag = null; }, 0);
  };
  svg.addEventListener("pointerup", release);
  svg.addEventListener("pointercancel", (event) => { if (state.drag?.pointer === event.pointerId) { state.drag = null; svg.classList.remove("dragging"); } });
}

function openDrawer(title) {
  if ($("evidence-drawer").hidden) state.drawerFocus = document.activeElement;
  state.selectionRequest++;
  state.sourceRequest++;
  state.source = null;
  $("drawer-title").textContent = title;
  $("drawer-content").replaceChildren();
  $("evidence-drawer").hidden = false;
  $("drawer-close").focus({ preventScroll: true });
}
function closeDrawer(restoreFocus = true) {
  const wasOpen = !$("evidence-drawer").hidden;
  state.selected = null; state.selectionRequest++; state.sourceRequest++; state.source = null;
  $("evidence-drawer").hidden = true;
  for (const node of $("graph-svg").querySelectorAll(".selected")) node.classList.remove("selected");
  for (const card of $("review-list").querySelectorAll(".selected")) card.classList.remove("selected");
  if (restoreFocus && wasOpen) {
    if (state.drawerFocus?.isConnected) state.drawerFocus.focus({ preventScroll: true });
    else if (state.view === "explore") $("finding-search").focus({ preventScroll: true });
  }
}
function detailSection(title) {
  const section = element("section", { className: "detail-section" }, [element("h3", { text: title })]);
  $("drawer-content").append(section);
  return section;
}
function detailFacts(facts, target = $("drawer-content")) {
  const list = element("dl", { className: "detail-facts" });
  for (const [name, value] of facts) if (value !== undefined && value !== null && value !== "") list.append(element("dt", { text: name }), element("dd", {}, [element("code", { text: value })]));
  target.append(list);
}
function locationButton(location, target) {
  if (!location?.file) return;
  const link = button("", "location-link", () => loadSource(location.file, location.line || 1, target));
  link.append(icon("file"), element("span", { text: `${location.file}:${location.line || 1}` }));
  return link;
}
function nodeLink(id) {
  const node = state.index?.nodes.get(id);
  const link = button(node?.qualname || id, "node-link", () => selectNode(id));
  if (!node) { link.disabled = true; link.title = "此符号未在当前快照中定义"; }
  return link;
}
function sourceTarget(section = $("drawer-content")) {
  const container = element("div", { className: "source-preview" }); section.append(container); return container;
}
async function selectFinding(finding) {
  if (!state.graph) return;
  openDrawer("发现与静态证据");
  state.selected = { kind: "finding", id: finding.id, nodeIds: finding.node_ids || [] };
  renderReview(); renderGraph(false);
  const request = state.selectionRequest;
  const snapshotId = state.snapshotId;
  const content = $("drawer-content");
  content.append(element("div", { className: "detail-badges" }, [badge(`${SEVERITIES[finding.severity] || finding.severity}严重度`, isRuleViolation(finding) ? "danger" : "neutral"), badge(findingStatus(finding), finding.status === "uncertain" ? "warning" : "neutral"), badge("纯静态", "outline")]), element("h3", { className: "finding-title", text: finding.title }), element("p", { className: "drawer-intro", text: finding.description }));
  detailFacts([["发现类型", findingLabel(finding)], ["规则", finding.rule_id], ["分析快照", shortId(snapshotId)], ["发现标识", shortId(finding.id)]]);
  const evidenceSection = detailSection("静态证据链");
  const preview = sourceTarget(evidenceSection);
  const evidences = Array.isArray(finding.evidence) ? finding.evidence : [];
  if (!evidences.length) evidenceSection.prepend(element("p", { text: "该发现未附带源码证据。" }));
  for (const evidence of evidences) {
    const card = element("article", { className: "evidence-card" }, [element("strong", { text: evidence.kind || "静态证据" }), element("p", { text: evidence.message })]);
    appendBatched(evidence.locations || [], card, (location) => locationButton(location, preview), 15);
    if (evidence.details && Object.keys(evidence.details).length) {
      card.append(jsonDetails(evidence.details, "解析依据与规则细节"));
    }
    evidenceSection.insertBefore(card, preview);
  }
  if (finding.node_ids?.length) {
    const nodes = detailSection("相关符号");
    appendBatched(finding.node_ids, nodes, nodeLink, 30);
  }
  const decisionSection = detailSection("人工处置");
  renderDecisionForm(finding, decisionSection);
  const initialLocation = evidences.flatMap((entry) => entry.locations || []).find((entry) => entry.file);
  if (initialLocation) loadSource(initialLocation.file, initialLocation.line || 1, preview);
  try {
    const detail = await api(`/anomalies/${encodeURIComponent(finding.id)}?${new URLSearchParams({ snapshot_id: snapshotId })}`);
    if (request !== state.selectionRequest || snapshotId !== state.snapshotId) return;
    // Fetch confirms this finding belongs to the selected immutable snapshot.
    if (detail.snapshot_id && detail.snapshot_id !== snapshotId) showToast("服务返回的证据快照与选中快照不一致。", true);
  } catch (error) { if (request === state.selectionRequest) showToast(`发现详情读取失败：${error.message}`, true); }
}
function selectNode(id) {
  const node = state.index?.nodes.get(id);
  if (!node) { showToast("当前快照中没有该符号。", true); return; }
  openDrawer("符号与调用关系");
  state.selected = { kind: "node", id };
  $("drawer-content").append(element("div", { className: "detail-badges" }, [badge(node.kind, "neutral"), badge(node.layer || "未配置层级", "outline")]), element("p", { className: "drawer-intro mono", text: node.qualname || node.id }));
  detailFacts([["语言", languageLabel(nodeLanguage(node))], ["签名", node.signature], ["模块", node.module], ["源码", `${node.file}:${node.line}`], ["分析快照", shortId(state.snapshotId)]]);
  if (node.metadata?.duplicate_definition) $("drawer-content").append(element("div", { className: "banner banner-warning", text: "该符号记录了重复定义。所示源码位置不是唯一实现依据，相关调用应结合候选与解析证据查看。" }));
  if (node.metadata && Object.keys(node.metadata).length) detailSection("声明依据与分析标记").append(jsonDetails(node.metadata, "查看保存的声明元数据"));
  const actions = element("div", { className: "editor-actions" }, [button("关联子图", "button button-small", () => focusSubgraph(node.id)), button("设为路径起点", "button button-small", () => { $("path-form").hidden = false; $("path-from").value = id; showToast("已设为路径起点，在路径查询中选择终点。 "); })]);
  $("drawer-content").append(actions);
  const source = detailSection("快照源码");
  const preview = sourceTarget(source);
  const location = locationButton(node, preview); if (location) source.insertBefore(location, preview);
  loadSource(node.file, node.line, preview);
  const outgoing = state.index?.outgoing.get(id) || [];
  const incoming = state.index?.incoming.get(id) || [];
  const calls = detailSection(`发起调用 · ${count(outgoing.length)}`);
  if (!outgoing.length) calls.append(element("p", { text: "当前静态分析未记录该符号发起的调用。" }));
  renderCalls(outgoing, calls, "outgoing");
  const callers = detailSection(`确定调用者 · ${count(incoming.length)}`);
  if (!incoming.length) callers.append(element("p", { text: "未记录确定调用者。这不能单独证明符号无用或不被执行。" }));
  renderCalls(incoming, callers, "incoming");
  for (const group of $("graph-svg").querySelectorAll(".graph-node")) group.classList.toggle("selected", group.dataset.nodeId === id);
}
function renderCalls(edges, section, direction) {
  let shown = 0;
  const list = element("div"); section.append(list);
  const renderNext = () => {
    const stop = Math.min(shown + 30, edges.length);
    for (const edge of edges.slice(shown, stop)) {
      const id = direction === "incoming" ? edge.source : edge.target;
      const label = `${resolutionLabel(edge)} · ${id || edge.expression} · ${edge.file}:${edge.line}`;
      list.append(button(label, "node-link", () => selectCall(edge)));
    }
    shown = stop;
    more.textContent = `继续查看 ${Math.min(30, edges.length - shown)} 项（剩余 ${edges.length - shown}）`;
    more.hidden = shown >= edges.length;
  };
  const more = button("", "button button-small", renderNext);
  section.append(more); renderNext();
}
function selectCall(edge) {
  if (!state.graph) return;
  openDrawer("调用解析证据");
  state.selected = { kind: "call", id: edge.id, nodeIds: [edge.source] };
  renderReview(); renderGraph(false);
  $("drawer-content").append(element("div", { className: "detail-badges" }, [badge(resolutionLabel(edge), edge.resolution === "resolved" ? "neutral" : "outline")]), element("p", { className: "drawer-intro mono", text: edge.expression }), element("p", { className: "drawer-intro", text: edge.reason || (edge.resolution === "resolved" ? "该调用目标在静态分析范围内得到确定解析。" : "当前解析器未提供进一步依据。") }));
  detailFacts([["调用者", edge.source], ["目标", edge.target || "未确定"], ["源码位置", `${edge.file}:${edge.line}:${edge.column ?? 0}`], ["分析快照", shortId(state.snapshotId)]]);
  const source = detailSection("调用位置源码");
  loadSource(edge.file, edge.line, sourceTarget(source));
  const related = detailSection("关联符号");
  related.append(nodeLink(edge.source));
  if (edge.target) related.append(nodeLink(edge.target));
  if (edge.candidates?.length) {
    const candidates = detailSection(`候选目标 · ${edge.candidates.length}`);
    candidates.append(element("p", { text: "候选目标不是确定调用关系，不参与确定路径判断。" }));
    appendBatched(edge.candidates, candidates, nodeLink, 30);
  }
  if (edge.metadata && Object.keys(edge.metadata).length) detailSection("解析细节").append(jsonDetails(edge.metadata, "查看调用解析元数据"));
}
function openSourceOnly(file, line) {
  openDrawer("快照源码证据");
  detailFacts([["分析快照", shortId(state.snapshotId)], ["源码位置", `${file}:${line}`]]);
  loadSource(file, line, sourceTarget());
}
async function loadSource(file, line, target) {
  if (!file || !state.snapshotId) { target.replaceChildren(element("p", { text: "此位置没有保存的源码证据。" })); return; }
  const request = ++state.sourceRequest;
  const snapshotId = state.snapshotId;
  target.replaceChildren(element("p", { className: "section-note", text: "正在读取该快照保存的源码…" }));
  try {
    const source = await api(`/evidence/source?${new URLSearchParams({ snapshot_id: snapshotId, file, line: String(line || 1) })}`);
    if (request !== state.sourceRequest || snapshotId !== state.snapshotId || !target.isConnected) return;
    if (source.snapshot_id && source.snapshot_id !== snapshotId) throw new Error("源码证据所属快照不一致");
    if (typeof source.content !== "string") throw new Error(source.error || "该快照没有保存此文件源码");
    state.source = { ...source, file, line: Number(line) || 1, snapshot_id: snapshotId };
    const lines = source.content.split("\n");
    const current = Math.max(1, Math.min(lines.length, Number(line) || 1));
    const start = Math.max(0, current - 6), end = Math.min(lines.length, current + 6);
    const heading = element("div", { className: "source-preview-heading" }, [element("span", { text: `${file}:${current}` }), button("查看完整源码", "text-button", () => showFullSource({ ...source, file, line: current, snapshot_id: snapshotId }))]);
    const code = element("div", { className: "source-code", attrs: { tabindex: "0", "aria-label": `${file} 快照源码片段` } });
    for (let i = start; i < end; i++) code.append(codeLine(lines[i], i + 1, i + 1 === current));
    target.replaceChildren(heading, code, element("p", { className: "section-note", text: `只读快照源码 · ${shortId(snapshotId)} · 文件哈希 ${shortId(source.hash)}${source.status && source.status !== "parsed" ? ` · 文件状态 ${source.status}` : ""}${source.error ? ` · ${source.error}` : ""}` }));
  } catch (error) {
    if (request === state.sourceRequest && target.isConnected) target.replaceChildren(element("p", { className: "section-note", text: `源码证据不可用：${error.message}` }));
  }
}
function codeLine(text, number, active) {
  return element("div", { className: `code-line${active ? " active" : ""}`, attrs: { "data-line": number } }, [element("span", { className: "line-number", text: number }), element("span", { text })]);
}
function showFullSource(source) {
  $("source-title").textContent = source.file;
  $("source-meta").textContent = `分析快照 ${source.snapshot_id} · 文件哈希 ${source.hash || "未提供"} · 只读保存的源码`;
  const full = $("source-full");
  const lines = source.content.split("\n");
  const chunk = 700;
  let start = Math.floor((source.line - 1) / chunk) * chunk;
  const renderPage = (focusLine = false) => {
    const end = Math.min(lines.length, start + chunk);
    const previous = button("← 上一段", "button button-small", () => { start = Math.max(0, start - chunk); renderPage(); });
    const next = button("下一段 →", "button button-small", () => { start += chunk; renderPage(); });
    previous.disabled = start === 0; next.disabled = end >= lines.length;
    const pager = element("div", { className: "source-pager" }, [previous, element("span", { text: `第 ${start + 1}–${end} 行 / 共 ${count(lines.length)} 行` }), next]);
    full.replaceChildren(pager);
    for (let i = start; i < end; i++) full.append(codeLine(lines[i], i + 1, i + 1 === source.line));
    full.scrollTop = 0;
    if (focusLine) requestAnimationFrame(() => {
      const line = [...full.children].find((node) => Number(node.dataset.line) === source.line);
      if (line) full.scrollTop = Math.max(0, line.offsetTop - full.offsetTop - 120);
    });
  };
  renderPage(true);
  $("source-dialog").showModal();
}
function renderDecisionForm(finding, section) {
  section.replaceChildren(element("h3", { text: "人工处置" }), element("p", { className: "section-note", text: "处置独立记录，不改变发现、原始证据或分析结论。" }));
  const entries = [...(state.decisionsByFinding.get(finding.id) || [])].sort((a, b) => (b.sequence || 0) - (a.sequence || 0) || String(b.created_at || b.timestamp).localeCompare(String(a.created_at || a.timestamp)));
  const logs = element("div");
  if (state.decisionsError) logs.append(element("p", { className: "section-note", text: `历史处置读取失败：${state.decisionsError}` }));
  appendBatched(entries, logs, (decision) => element("div", { className: "decision-log" }, [element("strong", { text: `${ACTIONS[decision.action] || decision.action} · ${formatTime(decision.created_at || decision.timestamp)}` }), element("p", { text: decision.reason }), decision.expires_at ? element("p", { text: `有效至 ${formatTime(decision.expires_at)}` }) : null]), 20);
  section.append(logs);
  const form = element("form", { className: "decision-form" });
  const select = element("select", { attrs: { required: "", "aria-label": "人工处置方式" } });
  for (const [value, text] of Object.entries(ACTIONS)) select.append(element("option", { text, attrs: { value } }));
  const reason = element("textarea", { attrs: { required: "", maxlength: "4000", placeholder: "说明判断依据与下一步计划", "aria-label": "处置原因" } });
  const submit = element("button", { className: "button button-primary", text: "记录处置", attrs: { type: "submit" } });
  form.append(element("label", { text: "处置方式" }, [select]), element("label", { text: "原因" }, [reason]), submit);
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!reason.value.trim()) { reason.focus(); return; }
    const snapshotId = state.snapshotId;
    const request = state.selectionRequest;
    submit.disabled = true; submit.textContent = "正在记录…";
    try {
      const data = await post("/decisions", { snapshot_id: snapshotId, finding_id: finding.id, action: select.value, reason: reason.value.trim() });
      if (snapshotId !== state.snapshotId) return;
      if (data.decision) state.decisions.push(data.decision);
      else { const all = await api(`/decisions?${new URLSearchParams({ snapshot_id: snapshotId })}`); state.decisions = all.items || []; }
      state.decisionsError = "";
      indexDecisions();
      renderMetrics(); renderReview();
      if (request === state.selectionRequest) renderDecisionForm(finding, section);
      showToast("处置已记录，原始发现与证据保持不变。");
    } catch (error) { showToast(`处置保存失败：${error.message}`, true); submit.disabled = false; submit.textContent = "记录处置"; }
  });
  section.append(form);
}
async function focusSubgraph(nodeId) {
  const snapshotId = state.snapshotId;
  const request = ++state.graphRequest;
  try {
    const data = await post("/graph/subgraph", { snapshot_id: snapshotId, node_id: nodeId, depth: 2, direction: "both" });
    if (snapshotId !== state.snapshotId || request !== state.graphRequest) return;
    if (data.snapshot_id && data.snapshot_id !== snapshotId) throw new Error("子图与选中快照不一致");
    if (data.gap_snapshot_id && data.gap_snapshot_id !== snapshotId) throw new Error("子图缺口证据与选中快照不一致");
    if (!Array.isArray(data.nodes) || !Array.isArray(data.edges)) throw new Error("子图响应缺少节点或边");
    state.subset = data; state.path = null; $("module-filter").value = ""; $("language-filter").value = "";
    state.reviewCache.key = ""; renderCoverage(); renderFilters(); renderReview();
    renderGraph();
    showToast("已显示两跳关联子图；这是浏览范围，不是检测的影响范围。");
  } catch (error) { showToast(`子图查询失败：${error.message}`, true); }
}
async function queryPath(event) {
  event.preventDefault();
  if (!state.snapshotId || !state.graph) { showToast("先创建或选择分析快照。", true); return; }
  const from = $("path-from").value.trim(), to = $("path-to").value.trim();
  if (!from || !to) return;
  const snapshotId = state.snapshotId;
  const request = ++state.graphRequest;
  const submit = $("path-form").querySelector("button[type=submit]");
  submit.disabled = true; $("path-result").textContent = "正在查询静态调用路径…"; $("path-result").className = "";
  try {
    const result = await post("/query/path", { snapshot_id: snapshotId, from, to });
    if (snapshotId !== state.snapshotId || request !== state.graphRequest) return;
    if (result.snapshot_id && result.snapshot_id !== snapshotId) throw new Error("路径与选中快照不一致");
    if (result.gap_snapshot_id && result.gap_snapshot_id !== snapshotId) throw new Error("路径缺口证据与选中快照不一致");
    state.path = result.status === "found" ? result : null;
    state.subset = null; $("module-filter").value = ""; $("language-filter").value = "";
    state.reviewCache.key = ""; renderCoverage(); renderFilters(); renderReview();
    renderGraph();
    const text = result.status === "found" ? `找到 ${Math.max(0, (result.node_ids || []).length - 1)} 跳确定调用路径。静态可达不代表一定执行。` : result.status === "unknown" ? "当前解析不足以判断是否存在调用路径。" : "在显式静态调用模型中没有找到确定路径。";
    $("path-result").replaceChildren(element("span", { text: `${text}${result.reason ? ` ${result.reason}` : ""}${result.complete === false ? " 分析存在缺口。" : " 完整性仅限显式静态调用模型。"}` }));
    if (result.status === "found") {
      const sequence = element("div", { className: "mono", text: result.node_ids.join(" → ") });
      $("path-result").append(sequence);
    }
    const gapsDetail = queryGapDetails(result, snapshotId);
    if (gapsDetail) $("path-result").append(gapsDetail);
  } catch (error) {
    if (snapshotId === state.snapshotId && request === state.graphRequest) { $("path-result").textContent = `路径查询失败：${error.message}`; $("path-result").className = "error"; }
  } finally { submit.disabled = false; }
}

async function scanProject() {
  if (state.busy) return;
  setBusy(true); showGlobalError("");
  try {
    const data = await post("/scan", {});
    const updates = await Promise.allSettled([refreshStatus(), refreshVersions()]);
    for (const update of updates) if (update.status === "rejected") showToast(`扫描完成，刷新元数据失败：${update.reason.message}`, true);
    const id = data.snapshot_id || state.status?.latest_snapshot?.id || state.versions[0]?.id;
    if (!id) throw new Error("扫描未返回可查询的快照");
    await loadSnapshot(id);
    if (!state.graph) throw new Error("扫描完成，但未能读取发布的快照");
    const maintenance = maintenanceRunLabel(data.maintenance);
    showToast(`${data.created === false ? "分析输入未变化，已读取现有快照。" : "静态分析快照已发布。目标代码未被执行。"}${maintenance ? ` ${maintenance}。` : ""}`);
  } catch (error) { showGlobalError(`扫描失败：${error.message}。已有快照保留，可继续查看。`); showToast(`扫描失败：${error.message}`, true); try { await refreshStatus(); } catch (_) { /* The connection state already identifies service failure. */ } }
  finally { setBusy(false); }
}
async function loadConfig() {
  const response = await api("/config");
  if (!response.config || typeof response.config !== "object" || Array.isArray(response.config)) throw new Error("配置响应缺少有效对象");
  state.config = response.config;
  $("config-editor").value = JSON.stringify(response.config, null, 2);
  $("config-path").textContent = response.config_path || "项目分析配置";
  $("config-message").textContent = "配置仅在保存并重新扫描后影响新快照。";
  $("config-message").className = "editor-message";
}
async function saveConfig(rescan = false) {
  let config;
  try {
    config = JSON.parse($("config-editor").value);
    if (!config || typeof config !== "object" || Array.isArray(config)) throw new Error("配置必须为 JSON 对象");
  } catch (error) { $("config-message").textContent = `JSON 无效：${error.message}`; $("config-message").className = "editor-message error"; return; }
  const buttons = [$("config-save"), $("config-rescan"), $("config-reload")];
  buttons.forEach((node) => { node.disabled = true; });
  $("config-message").textContent = "正在保存配置…"; $("config-message").className = "editor-message";
  try {
    const response = await post("/config", { config });
    state.config = response.config || config;
    $("config-editor").value = JSON.stringify(state.config, null, 2);
    $("config-message").textContent = "配置已保存。重新扫描后生效；旧快照保持原有规则。";
    showToast("分析配置已保存。");
    if (rescan) await scanProject();
  } catch (error) { $("config-message").textContent = `保存失败：${error.message}`; $("config-message").className = "editor-message error"; }
  finally { buttons.forEach((node) => { node.disabled = false; }); }
}
async function compareVersions(event) {
  event.preventDefault();
  const from = $("diff-from").value, to = $("diff-to").value;
  if (!from || !to) { showToast("请选择两个分析快照。", true); return; }
  if (from === to) { showToast("请选择不同的基准和目标快照。", true); return; }
  const request = ++state.diffRequest;
  $("diff-button").disabled = true;
  $("diff-from").disabled = true; $("diff-to").disabled = true;
  $("diff-result").replaceChildren(element("div", { className: "loading-text", text: "正在对比不可变快照…" }));
  try {
    const diff = await post("/diff", { from_snapshot: from, to_snapshot: to });
    if (request !== state.diffRequest || $("diff-from").value !== from || $("diff-to").value !== to) return;
    if ((diff.from_snapshot && diff.from_snapshot !== from) || (diff.to_snapshot && diff.to_snapshot !== to)) throw new Error("对比结果版本与所选版本不一致");
    renderDiff({ ...diff, from_snapshot: from, to_snapshot: to });
  }
  catch (error) { if (request === state.diffRequest) $("diff-result").replaceChildren(emptyState("版本对比失败", error.message, "clock")); }
  finally { $("diff-button").disabled = state.versions.length < 2; $("diff-from").disabled = false; $("diff-to").disabled = false; }
}
function renderDiff(diff) {
  const target = $("diff-result"); target.replaceChildren();
  target.append(element("p", { className: "diff-binding mono", text: `结果绑定：${diff.from_snapshot} → ${diff.to_snapshot}` }));
  const comparison = diff.comparison || {};
  const warnings = [];
  if (comparison.same_project === false) warnings.push("两个快照属于不同项目，不能直接解释为演化变化。");
  if (comparison.same_policy === false) warnings.push("规则配置不同，发现变化可能由规则变化引起。");
  if (comparison.same_analyzer === false) warnings.push("分析器版本不同，图结构变化可能由解析能力变化引起。");
  if (comparison.structurally_comparable === false || comparison.findings_comparable === false) warnings.push("比较条件不完整，请结合版本信息解释变化。");
  for (const reason of comparison.reasons || []) if (typeof reason === "string" && !warnings.includes(reason)) warnings.push(reason);
  if (warnings.length) target.append(element("div", { className: "banner banner-warning" }, [icon("warning"), element("span", { text: warnings.join(" ") })]));
  if (diff.summary?.message) target.append(element("p", { className: "section-note", text: diff.summary.message }));
  const stats = element("div", { className: "diff-metrics" });
  for (const [key, name, third] of [["nodes", "代码节点", "changed"], ["edges", "调用关系", "changed"], ["findings", "静态发现", "persisting"]]) {
    const group = diff[key] || {};
    const added = group.added?.length || 0, removed = (group.removed || group.resolved || []).length, changed = group[third]?.length || 0;
    const card = element("div", { className: "diff-stat" }, [element("strong", { text: name }), element("p", { text: `新增 ${count(added)} · ${key === "findings" ? "目标中未再检出" : "删除"} ${count(removed)} · ${third === "persisting" ? "持续" : "变更"} ${count(changed)}` })]);
    stats.append(card);
  }
  target.append(stats);
  for (const [key, title, categories] of [["findings", "发现变化", [["added", "新增"], ["resolved", "未再检出"], ["persisting", "持续"]]], ["nodes", "节点变化", [["added", "新增"], ["removed", "删除"], ["changed", "变更"]]], ["edges", "调用关系变化", [["added", "新增"], ["removed", "删除"], ["changed", "变更"]]]]) {
    const group = diff[key] || {};
    const total = categories.reduce((sum, [category]) => sum + (group[category]?.length || 0), 0);
    const details = element("details", { className: "diff-list" }, [element("summary", { text: `${title} · ${count(total)} 项` })]);
    if (key === "findings") details.open = true;
    const list = element("div"); details.append(list);
    const items = categories.flatMap(([category, label]) => (group[category] || []).map((item) => ({ item, label })));
    let shown = 0;
    const more = button("", "button button-small", () => appendRows());
    function appendRows() {
      const stop = Math.min(shown + 60, items.length);
      for (const { item, label } of items.slice(shown, stop)) {
        const current = item.after || item.before || item;
        const descriptor = typeof current === "string" ? current : current.title || current.qualname || (current.expression ? `${current.source} → ${current.target || current.expression}` : current.id || JSON.stringify(current));
        const body = element("span", {}, [element("code", { text: descriptor })]);
        if (item.changes && Object.keys(item.changes).length) body.append(jsonDetails(item.changes, `变更字段：${Object.keys(item.changes).join("、")}`, { from_snapshot: diff.from_snapshot, to_snapshot: diff.to_snapshot }));
        list.append(element("div", { className: "diff-row" }, [badge(label, label === "新增" && key === "findings" && isRuleViolation(current) ? "danger" : "neutral"), body]));
      }
      shown = stop;
      more.textContent = `继续查看（还有 ${count(items.length - shown)} 项）`;
      more.hidden = shown >= items.length;
    }
    details.append(more); appendRows();
    if (!total) list.append(element("p", { className: "section-note", text: "该类别没有记录变化。" }));
    target.append(details);
  }
  target.append(element("p", { className: "section-note", text: "发现未再检出不自动代表已修复；需结合规则、源码、分析覆盖与人工处置解释。" }));
}

function bindEvents() {
  for (const nav of document.querySelectorAll("[data-view]")) nav.addEventListener("click", () => switchView(nav.dataset.view));
  $("scan-button").addEventListener("click", scanProject);
  $("snapshot-select").addEventListener("change", () => loadSnapshot($("snapshot-select").value));
  for (const tab of document.querySelectorAll("[data-review]")) {
    tab.addEventListener("click", () => { state.review = tab.dataset.review; state.page = 0; renderReview(); });
    tab.addEventListener("keydown", (event) => {
      if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;
      event.preventDefault(); const tabs = [...document.querySelectorAll("[data-review]")];
      const index = event.key === "Home" ? 0 : event.key === "End" ? tabs.length - 1 : (tabs.indexOf(tab) + (event.key === "ArrowRight" ? 1 : -1) + tabs.length) % tabs.length;
      tabs[index].click(); tabs[index].focus();
    });
  }
  let searchTimer;
  $("finding-search").addEventListener("input", () => { clearTimeout(searchTimer); searchTimer = setTimeout(() => { state.page = 0; renderReview(); }, 140); });
  for (const id of ["type-filter", "severity-filter"]) $(id).addEventListener("change", () => { state.page = 0; renderReview(); });
  $("language-filter").addEventListener("change", changeLanguageFilter);
  $("coverage-details").addEventListener("toggle", () => { if ($("coverage-details").open) renderCoverageDetails(); });
  $("page-prev").addEventListener("click", () => { state.page--; renderReview(); });
  $("page-next").addEventListener("click", () => { state.page++; renderReview(); });
  $("module-filter").addEventListener("change", () => renderGraph());
  $("show-unknown").addEventListener("change", () => renderGraph(false));
  $("path-toggle").addEventListener("click", () => { $("path-form").hidden = !$("path-form").hidden; if (!$("path-form").hidden) $("path-from").focus(); });
  $("path-form").addEventListener("submit", queryPath);
  $("zoom-in").addEventListener("click", () => zoomGraph(1.25));
  $("zoom-out").addEventListener("click", () => zoomGraph(.8));
  $("zoom-reset").addEventListener("click", () => { state.transform = { x: 0, y: 0, scale: 1 }; applyTransform(); });
  $("graph-back").addEventListener("click", () => { state.graphRequest++; state.subset = null; state.path = null; $("module-filter").value = ""; $("path-result").replaceChildren(); renderGraph(); });
  $("drawer-close").addEventListener("click", () => { closeDrawer(); renderReview(); });
  $("source-close").addEventListener("click", () => $("source-dialog").close());
  $("source-dialog").addEventListener("click", (event) => { if (event.target === $("source-dialog")) { const r = $("source-dialog").getBoundingClientRect(); if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) $("source-dialog").close(); } });
  $("config-reload").addEventListener("click", async () => { try { await loadConfig(); showToast("已重新读取保存的配置。"); } catch (error) { showToast(`读取失败：${error.message}`, true); } });
  $("config-save").addEventListener("click", () => saveConfig(false));
  $("config-rescan").addEventListener("click", () => saveConfig(true));
  $("config-editor").addEventListener("input", () => { $("config-message").textContent = "存在未保存修改。保存并扫描后才会影响新快照。"; $("config-message").className = "editor-message"; });
  $("config-editor").addEventListener("keydown", (event) => {
    if (event.key !== "Tab") return;
    event.preventDefault(); const input = event.target; const start = input.selectionStart, end = input.selectionEnd;
    input.value = input.value.slice(0, start) + "  " + input.value.slice(end); input.setSelectionRange(start + 2, start + 2); input.dispatchEvent(new Event("input"));
  });
  $("diff-form").addEventListener("submit", compareVersions);
  for (const id of ["diff-from", "diff-to"]) $(id).addEventListener("change", () => { state.diffRequest++; $("diff-result").replaceChildren(emptyState("版本选择已变化", "点击对比版本，读取这两个快照的真实差异。", "clock")); });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !$("source-dialog").open) { closeDrawer(); renderReview(); }
    if (event.key === "/" && !["INPUT", "TEXTAREA", "SELECT"].includes(document.activeElement?.tagName) && state.view === "explore") { event.preventDefault(); $("finding-search").focus(); }
  });
  bindGraphInteractions();
}
async function initialize() {
  bindEvents();
  const results = await Promise.allSettled([refreshStatus(), refreshVersions(), loadConfig()]);
  if (results[0].status === "rejected") showGlobalError(`无法连接本地分析服务：${results[0].reason.message}。启动服务后点击扫描项目重试。`);
  if (results[1].status === "rejected") { $("version-list").replaceChildren(emptyState("快照列表读取失败", results[1].reason.message, "clock")); }
  if (results[2].status === "rejected") { $("config-message").textContent = `配置读取失败：${results[2].reason.message}`; $("config-message").className = "editor-message error"; }
  const id = state.status?.latest_snapshot?.id || state.versions.find((item) => item.is_latest)?.id || state.versions[0]?.id;
  if (id) await loadSnapshot(id); else renderEmptySnapshot();
  // Observe publication/status only. Background scanning belongs to the service.
  let polling = false;
  setInterval(async () => {
    if (polling || state.busy || document.visibilityState === "hidden") return;
    polling = true;
    const previous = state.status?.latest_snapshot?.id;
    try {
      const status = await refreshStatus();
      if (state.busy) return;
      const latest = status.latest_snapshot?.id;
      if (latest && latest !== previous) {
        await refreshVersions();
        if (!state.snapshotId || state.snapshotId === previous) await loadSnapshot(latest);
        else showToast("新的静态快照已发布，当前保留所选历史版本。");
      }
      if (!state.config && !$("config-editor").value.trim()) await loadConfig();
    } catch (_) { /* renderStatus exposes a disconnected service; preserve published data. */ }
    finally { polling = false; }
  }, 15000);
}

initialize().catch((error) => { showGlobalError(`界面初始化失败：${error.message}`); renderEmptySnapshot("无法加载分析结果", "启动本地服务后点击扫描项目重试。"); });
