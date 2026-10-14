"""Compact views of closed formal report values; standard-library artifact IO.

Streams saved JSON, copies semantic witnesses before technical provenance,
retains false/unknown and full pointers, and computes no new assessment.
No database, target source, reference report or analyzer module is opened.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import html
import json
from pathlib import Path
import re
from typing import Any

from render_report_summaries import _SavedJSON, _LABELS

DIRECTORY = Path(__file__).resolve().parent
_VERSION = 'saved-static-analysis-brief-1'
_MISSING = object()
_WHOLE_SEMANTIC = {'relation_witnesses', 'checks', 'field_mappings', 'condition_abstract_form', 'condition_source'}
_TEXT_SEMANTIC = {'ownership_assessment', 'responsibility_interpretation', 'interpretation', 'scope',
    'source_delivery_result', 'source_execution_result', 'source_projection_result', 'callee_source',
    'captured_callee_source', 'agreement_domain', 'ordered_fields', 'ordered_field_paths',
    'request_variant', 'response_variant', 'family', 'selected_writer_symbols', 'conditions'}
_META = {'id', 'kind', 'origin', 'version', 'relation_component_version', 'extractor_version',
    'record_relations_version', 'conditional_gate_version', 'finite_state_component', 'source_model',
    'snapshot_id', 'location', 'full_location_ref', 'source_fact_refs', 'full_value_ref', 'remaining_fields_ref',
    'presentation_table_ref', 'presentation_only', 'truncated', 'shown_count', 'total_count', 'shown_items',
    'source_selector', 'role', 'selected_role', 'column', 'line', 'end_line', 'start_byte', 'end_byte',
    'file', 'hash', 'source_hash', 'source_excerpt', 'parse_identity', 'parser_version', 'binder_id',
    'declaration_id', 'binding_id', 'root_declaration_id', 'root', 'parameter_declaration_id',
    'operations', 'operation_limit', 'limit', 'source_order_index', 'normal_source_order_index',
    'binding_path', 'parameter_index', 'macro_namespace_complete', 'reference_dependencies_only',
    'source_structure_complete', 'source_truncated', 'original_characters', 'omitted_fields_for_presentation',
    'result_binding_source', 'actual_target_role', 'region_kind', 'branch', 'branch_kind'}
_SCOPE_KEYS = {'boundaries', 'unproved_relations', 'unreviewed_scope', 'limits', 'scope_conditions', 'source_model_conditions'}
_TABLE_NAMES = {'rows', 'record_partitions', 'absent_input_partitions'}
_TECHNICAL_PATHS = {'location', 'reference', 'references', 'binding', 'root_identity', 'parse_identity', 'assignment_attempts', 'local_bindings', 'record_fields'}
_PATTERN_SELECTION = {
    'relation_witnesses': True, 'ownership_assessment': True, 'responsibility_interpretation': True,
    'record_boundary': True, 'command_boundary': True, 'retention_boundary': True,
    'persisted_selection_recheck_relation': {'checks': True, 'active_members': True},
    'groups': {
        'readiness': {'relations': [{'true_branch_always_abrupt': True,
            'source_order_not_runtime_enqueue_success': True}],
            'readiness_implementation_success_or_external_state_proven': True},
        'completion': {'conditions_directly_depending_on_mutating_predicate': True,
            'conditions_without_direct_mutating_dependency': True, 'statement': True,
            'checklist_internal_checks_proven': True, 'external_verdict_or_evidence_truth_proven': True},
        'access_audit': {'response_value_relations': [{'field_mappings': True,
            'actual_response_delivery_proven': True}],
            'job_audit_subject_equivalence_claimed': True, 'all_http_security_or_business_mutations_proven': True},
    },
}
_REPORT_SELECTION = {
    'version': True, 'snapshot': {'id': True, 'project_name': True, 'source_hash': True, 'policy_hash': True},
    'judgments': [{'goal_id': True, 'summary': True, 'complete_assessment': True,
        'full_goal_supported': True}],
    'functional_chains': [{'rule_id': True, 'claim_type': True, 'assessment': True,
        'analysis_gaps': [{'code': True}], 'pattern': _PATTERN_SELECTION}],
    'source_relation_index': True,
    'report_scope': True, 'target_executed': True, 'target_tests_run': True,
    'target_build_run': True, 'runtime_functionality_verified': True,
}
_INTEGRATION_SELECTION = {key: True for key in ('repository', 'snapshot_id', 'source_hash', 'policy_hash',
    'publication_series', 'database_closed', 'database_wal_empty_or_absent',
    'target_executed', 'target_tests_run', 'target_build_run')}


def pointer(parent: str, key: Any) -> str:
    return parent + '/' + str(key).replace('~', '~0').replace('/', '~1')


def encoded(value: Any) -> str:
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, separators=(',', ':'))


def cell(value: Any) -> str:
    return html.escape(encoded(value), quote=False).replace('|', '&#124;').replace('`', '&#96;').replace('\n', ' ')


def clipped(value: Any, maximum: int = 260) -> str:
    text = encoded(value)
    return cell(text if len(text) <= maximum else text[:maximum] + '…（展示省略）')


def link(repository: str, ref: str, label: str = '保存值') -> str:
    return f'[{label}]({repository}-automatic-report.json#{ref})'


def technical(key: str, value: Any) -> bool:
    return (key in _META or key.endswith(('_id', '_ids', '_sha256', '_fact_refs', '_source_facts'))
        or key.endswith('_location') or key.endswith('_version') or key.startswith('target_')
        or key in {'parameter_index', 'declaration_kind', 'is_parameter', 'source_complete', 'bindings_complete', 'macro_namespace_complete', 'runtime_value_identity_proven'}
        or (isinstance(value, str) and bool(re.fullmatch(r'[a-f0-9]{20,64}', value))))


def boundary(key: str, value: Any) -> bool:
    return (value is False and (key.endswith(('_proven', '_verified', '_inferred', '_complete', '_equivalent'))
        or key.startswith(('all_', 'whole_', 'runtime_', 'unique_', 'external_', 'physical_'))))


def score(path: str, key: str, value: Any) -> int:
    if key == 'ownership_assessment': return 1200
    if 'relation_witnesses' in path: return 1100
    if '/checks' in path: return 1000
    if 'necessary_relation' in path: return 950
    if key in {'ordered_fields', 'ordered_field_paths'}: return 950
    if 'field_mappings' in path: return 900
    if key == 'responsibility_interpretation': return 850
    if 'true_branch_always_abrupt' in path: return 820
    if 'conditions' in path or 'guard' in path: return 760
    if 'generation_argument' in path or 'nullable_context_consumer' in path: return 750
    if 'projection_agreement' in path or 'field_joins' in path: return 730
    if any(word in key for word in ('linked', 'matches', 'connected', 'same_', 'before', 'recheck')): return 700
    if 'relation' in path or 'admission' in path or 'source_derived_conditions' in path: return 680
    if key in {'scope', 'interpretation', 'source_delivery_result', 'source_execution_result', 'source_projection_result'}: return 650
    if key in {'callee_source', 'captured_callee_source'}: return 640
    if any(word in path for word in ('order', 'sequence', 'continuation', 'predicate', 'source_collection_conditions')): return 600
    if key in {'source', 'root_name', 'member', 'members', 'field', 'fields', 'target_field'}: return 500
    if key == 'supported' and 'components' in path: return 800
    if key == 'supported': return 400
    return 200


def semantic_candidates(entry: dict, small_pattern: dict) -> tuple[list[dict], list[dict]]:
    positive, bounds = [], []
    seen = set()
    def clean(value: Any) -> Any:
        if isinstance(value, dict):
            return {k: clean(v) for k, v in value.items() if not technical(k, v) and k not in _TECHNICAL_PATHS}
        if isinstance(value, list): return [clean(v) for v in value]
        return value

    def add(path: str, key: str, value: Any, ref: str, category: str | None = None):
        if technical(key, value) or key in {'scoped_source_supported', 'source_only', 'source_relations_only',
                'creates_calls_edge', 'incomplete', 'runtime_functionality_verified'}:
            return
        if isinstance(value, (dict, list)) and not value:
            return
        marker = (path, encoded(value))
        if marker in seen: return
        seen.add(marker)
        item = {'path': path, 'value': value, 'ref': ref, 'score': score(path, key, value)}
        if category == 'boundary' or boundary(key, value): bounds.append(item)
        elif value is None:
            if key in {'supported', 'state', 'assessment', 'ownership_assessment', 'boolean_result'}:
                positive.append({**item, 'score': max(950, item['score'])})
        elif value == 'unknown' and key in {'supported', 'state', 'assessment', 'ownership_assessment'}:
            positive.append({**item, 'score': max(950, item['score'])})
        elif (key in _WHOLE_SEMANTIC or key in _TEXT_SEMANTIC or key in _SCOPE_KEYS
                or (key == 'supported' and 'components' in path)
                or key.startswith('same_') or any(word in key for word in ('linked', 'connected', 'close_before', 'always_abrupt'))):
            positive.append(item)

    def visit(value: Any, path: str, ref: str, *, projected: bool, depth: int = 0):
        if depth > 14 or any(part in _TECHNICAL_PATHS for part in path.split('/')): return
        key = path.rsplit('/', 1)[-1]
        if technical(key, value) or key in _TABLE_NAMES or key.endswith('_table_rows'): return
        if isinstance(value, dict):
            ref = value.get('full_value_ref', ref) if projected else ref
            if value.get('omitted_for_presentation'): return
            if projected and 'shown_items' in value:
                for i, child in enumerate(value['shown_items']):
                    visit(child, path + '/' + str(i), pointer(ref, i), projected=True, depth=depth + 1)
                return
            if projected and value.get('truncated') and 'text' in value:
                add(path, key, value['text'] + '…（原投影已省略）', ref)
                return
            if isinstance(value.get('file'), str) and isinstance(value.get('line'), int): return
            # Keep computed witness/check maps as one coherent semantic value.
            if key in _WHOLE_SEMANTIC:
                visible = clean(value)
                add(path, key, visible, ref)
                return
            for child_key, child in value.items():
                if technical(child_key, child): continue
                child_path = path + '/' + child_key
                child_ref = pointer(ref, child_key)
                if child_key in _SCOPE_KEYS:
                    if child: add(child_path, child_key, child, child_ref, 'boundary')
                else:
                    visit(child, child_path, child_ref, projected=projected, depth=depth + 1)
        elif isinstance(value, list):
            if key in {'ordered_fields', 'ordered_field_paths'}:
                if value: add(path, key, value, ref)
                return
            if value and all(not isinstance(item, (dict, list)) for item in value):
                if all(technical(key, item) for item in value): return
                add(path, key, value, ref)
            else:
                for i, child in enumerate(value[:12]):
                    visit(child, path + '/' + str(i), pointer(ref, i), projected=projected, depth=depth + 1)
        else:
            add(path, key, value, ref)

    # Small full-pattern fields are genuine saved values, before their bounded
    # presentation counterpart. No rule ID supplies a judgment.
    for key, value in small_pattern.items():
        visit(value, key, pointer(entry['pattern_ref'], key), projected=False)
    for section in entry.get('presentation', {}).get('sections', []):
        visit(section.get('value'), section['name'], section['full_value_ref'], projected=True)
    positive.sort(key=lambda item: (-item['score'], item['path']))
    bounds.sort(key=lambda item: (2 if item['path'].split('/')[-1] in {'all_project_functionality_proven', 'all_function_paths_or_hidden_effects_proven', 'all_function_paths_or_effects_accounted'} else 0,
        0 if '_boundary/' in item['path'] or '/groups/' in '/' + item['path'] else 1,
        0 if not isinstance(item['value'], (dict, list)) else 1, item['path'].count('/'), item['path']))
    return positive, bounds


def selected_items(positive: list[dict], bounds: list[dict]) -> list[tuple[str, dict]]:
    selected = []
    if positive:
        selected.append(('实际关系', positive[0]))
        family = positive[0]['path'].split('/')[0]
        other = next((item for item in positive[1:] if item['path'].split('/')[0] != family and item['score'] >= 600), None)
        # If all data lives in one named component, retain a different semantic
        # leaf within it, rather than substituting provenance or an invented pass.
        if other is None:
            other = next((item for item in positive[1:] if item['path'] != positive[0]['path']), None)
        if other is not None: selected.append(('实际条件/接线', other))
    if bounds: selected.append(('保留边界', bounds[0]))
    return selected[:3]


def render(repository: str, report: dict) -> tuple[str, list[dict]]:
    report_file = f'{repository}-automatic-report.json'
    name = 'CodePatchBay' if repository == 'codepatchbay' else 'WinWinCode'
    chains = report['functional_chains']
    entries = {entry['rule_id']: entry for entry in report['source_relation_index']['entries']}
    states = dict(Counter(chain['assessment'].get('state', 'unknown') for chain in chains))
    lines = [f'# {name} · 代码层静态分析简报', '',
        '只重排已保存正式报告的实际值；没有重新分析或新增评价。章节标题仅供导航，不是结论来源。',
        f'快照 `{report["snapshot"]["id"]}`；[完整报告]({report_file})。',
        f'保存关系状态：`{encoded(states)}`。两库 31 条有限源码关系的支持状态不是功能覆盖率；未知、条件和反证仍按原证据保留。', '',
        '## 原具体问题', '']
    for i, judgment in enumerate(report['judgments']):
        lines.append(f'- **{judgment["goal_id"]}**：{judgment.get("summary", "unknown（没有保存 summary）")} '
            + f'完整判断=`{encoded(judgment.get("complete_assessment", "unknown"))}`；支持=`{encoded(judgment.get("full_goal_supported", "unknown"))}`；'
            + link(repository, f'/judgments/{i}', '条件、反证与证据') + '。')
    lines.extend(['', '## 主要有限源码关系', '',
        '每项最多列两条实际关系和一条边界；大字段、源码位置、hash 与事实 ID 留在原 JSON Pointer。表格仅复制保存的有限输入分区，未执行这些输入。', ''])
    selections = []
    for index, chain in enumerate(chains):
        rule_id = chain['rule_id']; entry = entries.get(rule_id)
        lines.extend([f'### {_LABELS.get(rule_id, rule_id)}', ''])
        if entry is None:
            lines.extend(['- unknown：没有保存的源码关系索引；' + link(repository, f'/functional_chains/{index}', '原关系') + '。', ''])
            selections.append({'rule_id': rule_id, 'state': 'unknown_index_missing'})
            continue
        positive, bounds = semantic_candidates(entry, chain.get('pattern', {}))
        items = selected_items(positive, bounds)
        if not items:
            lines.append('- unknown：未保存可用的简报字段；' + link(repository, entry['pattern_ref'], '原关系') + '。')
        for label, item in items:
            value = item['value']
            omitted = 0
            if isinstance(value, dict) and len(value) > 4:
                omitted = len(value) - 4; value = dict(list(value.items())[:4])
            extra = f'；另 {omitted} 项见原值' if omitted else ''
            lines.append(f'- {label} `{item["path"]}`：`{clipped(value, 500)}`{extra}；' + link(repository, item['ref']) + '。')
        gap_codes = [gap.get('code', 'unknown') for gap in chain.get('analysis_gaps', [])]
        if gap_codes and not bounds:
            lines.append('- 保存缺口：`' + clipped(gap_codes, 250) + '`；' + link(repository, f'/functional_chains/{index}/analysis_gaps', '范围') + '。')
        if not bounds:
            lines.append('- 源码关系受正常到达、模型与不透明调用边界约束；' + link(repository, entry['pattern_ref'], '完整条件及 unknown') + '。')
        # The two small finite domains are identified by saved field structure,
        # not by a benchmark issue ID or an expected truth-table answer.
        tables = []
        for table in entry.get('presentation', {}).get('tables', []):
            ref = table['full_table_ref']
            if ('/mutating_finite_enum_partition/' in ref and table['name'] in {'record_partitions', 'absent_input_partitions'}) \
                    or (ref.endswith('/finite_effective_state_relation/rows') and table['name'] == 'rows'):
                tables.append(table)
        for table in tables:
            columns = table.get('columns', [])
            lines.extend(['', f'保存的 `{table["name"]}`：{link(repository, table["full_table_ref"], "完整表")}；{len(table.get("rows", []))}/{table["total_rows"]} 行。', '',
                '| ' + ' | '.join(cell(column) for column in columns) + ' |',
                '| ' + ' | '.join('---' for _ in columns) + ' |'])
            for row in table.get('rows', []):
                lines.append('| ' + ' | '.join(cell(row.get('cells', {}).get(column, 'unknown（展示缺项）')) for column in columns) + ' |')
            if table.get('truncated'):
                lines.append('原展示表已截断；遗漏项保持 unknown，请下钻完整表。')
        lines.append('')
        selections.append({'rule_id': rule_id, 'claim_type': chain['claim_type'],
            'saved_assessment': chain['assessment'], 'pattern_ref': entry['pattern_ref'],
            'semantic_values': [{'label': label, 'saved_path': item['path'], 'full_value_ref': item['ref']}
                for label, item in items],
            'finite_tables': [{'full_table_ref': table['full_table_ref'], 'shown_rows': len(table.get('rows', [])),
                'saved_total_rows': table['total_rows'], 'saved_truncated': table.get('truncated')} for table in tables],
            'display_selection_complete': False})
    lines.extend(['## 阅读边界', '',
        f'- 全文自动复现声明：`{encoded(report["report_scope"].get("whole_report_reproduction_claimed", "unknown"))}`；运行功能验证：`{encoded(report.get("runtime_functionality_verified", "unknown"))}`。',
        '- 写者来源的 partial assessment 不等于唯一事实所有者、规范权威或所有授权完整。',
        '- 这份简报只选有意义保存值；省略的字段、完整条件、反证和必要缺口仍在各条完整 pattern、source facts 与原判断中。',
        '- `unknown` / `false` 不被摘要改成通过；所选源码关系不证明 IO、远端响应、实际调度或全路径运行成功。',
        f'- 未执行目标代码、测试或构建；原始证据、已有 summary 和发布报告未修改。'])
    return '\n'.join(lines) + '\n', selections


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', action='store_true', help='Print selected values/line counts without writing briefs')
    args = parser.parse_args()
    destinations = [DIRECTORY / f'{repo}-analysis-brief.md' for repo in ('codepatchbay', 'winwincode')]
    manifest_path = DIRECTORY / 'BRIEF_INPUTS.json'
    if not args.preview and any(path.exists() for path in [*destinations, manifest_path]):
        raise FileExistsError('Brief outputs already exist; preserve them rather than overwrite')
    manifest = {'version': _VERSION, 'presentation_only': True, 'new_assessment_generated': False,
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'streaming_reader_path': 'render_report_summaries.py',
        'streaming_reader_sha256': hashlib.sha256((DIRECTORY / 'render_report_summaries.py').read_bytes()).hexdigest(),
        'selection_basis': 'Saved semantic witnesses/checks/conditions, finite tables, partial ownership assessment and false boundaries; labels are navigation only.',
        'streaming_fields': list(_REPORT_SELECTION), 'small_pattern_fields': list(_PATTERN_SELECTION),
        'repositories': [], 'database_opened': False, 'target_source_opened': False, 'analyzer_imported': False,
        'target_executed': False, 'target_tests_run': False, 'target_build_run': False}
    rendered = []
    for repository in ('codepatchbay', 'winwincode'):
        report_path = DIRECTORY / f'{repository}-automatic-report.json'
        report, report_hash = _SavedJSON(report_path).load(_REPORT_SELECTION)
        integration, integration_hash = _SavedJSON(DIRECTORY / f'{repository}-integration.json').load(_INTEGRATION_SELECTION)
        if (integration.get('publication_series') != 'v13' or integration.get('database_closed') is not True
                or integration.get('database_wal_empty_or_absent') is not True
                or report['snapshot']['id'] != integration['snapshot_id']
                or any(report['snapshot'][key] != integration[key] for key in ('source_hash', 'policy_hash'))):
            raise ValueError('Expected matching, closed formal v13 report/integration artifacts')
        markdown, selections = render(repository, report)
        output_path = DIRECTORY / f'{repository}-analysis-brief.md'
        entry = {'repository': repository, 'snapshot_id': report['snapshot']['id'],
            'source_hash': report['snapshot']['source_hash'], 'policy_hash': report['snapshot']['policy_hash'],
            'report_path': report_path.name, 'report_sha256': report_hash, 'integration_sha256': integration_hash,
            'output': output_path.name, 'output_sha256': hashlib.sha256(markdown.encode()).hexdigest(),
            'line_count': len(markdown.splitlines()), 'source_relation_count': len(report['functional_chains']),
            'selected_saved_values': selections}
        manifest['repositories'].append(entry)
        rendered.append((output_path, markdown))
        print(json.dumps({'repository': repository, 'line_count': entry['line_count'],
            'source_relation_count': entry['source_relation_count'],
            'selected_fields': [{'rule_id': item['rule_id'], 'paths': [value['saved_path'] for value in item.get('semantic_values', [])]} for item in selections]}, ensure_ascii=False), flush=True)
        del report, integration
    if not args.preview:
        for output_path, markdown in rendered:
            with output_path.open('x', encoding='utf-8') as stream: stream.write(markdown)
        with manifest_path.open('x', encoding='utf-8') as stream:
            json.dump(manifest, stream, ensure_ascii=False, indent=2); stream.write('\n')


if __name__ == '__main__':
    main()
