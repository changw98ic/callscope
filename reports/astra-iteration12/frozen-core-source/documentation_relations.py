"""Qualified document/deployment comparisons over saved text and Rust CST.

This finite model compares explicit normative document clauses with selected
source routes. It neither executes targets nor treats a keyword, a secret
reference, or a source invocation as a proved security defect/runtime event.
"""
from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from .semantic_sources import unwrap
from .static_contracts import _literal_string

VERSION = 'captured-document-deployment-relations-1'
MODEL = 'captured-document-deployment-qualified-source-v1'
CONTROL_MODEL = 'captured-normal-statement-control-v1'
REQUIRED_ROLES = frozenset({'server_boundary', 'worker_bootstrap', 'worker_installation',
    'worker_route', 'device_send', 'store_open', 'model_execute', 'model_invoke',
    'secret_resolver', 'secret_constructor', 'provider_factory', 'provider_open'})
_LIMIT, _FACT_LIMIT, _DOCUMENT_BYTES = 65536, 8192, 1024 * 1024
_FUNCTIONS = {'function_item', 'closure_expression', 'async_block'}


def _f(node: Any, name: str) -> Any:
    return node.child_by_field_name(name) if node is not None else None


def _c(node: Any) -> list[Any]:
    return [child for child in node.named_children if child.type not in {'line_comment', 'block_comment'}] if node is not None else []


def _u(node: Any) -> Any:
    node = unwrap(node)
    while node is not None and node.type in {'try_expression', 'reference_expression', 'await_expression'}:
        node = unwrap(_f(node, 'value') or _f(node, 'argument') or next(iter(_c(node)), None))
    return node


def _inside(outer: Any, inner: Any) -> bool:
    return bool(outer is not None and inner is not None and outer.start_byte <= inner.start_byte and inner.end_byte <= outer.end_byte)


def _hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def _ancestors(node: Any):
    while node is not None:
        yield node
        node = node.parent


def _binders(node: Any) -> list[Any]:
    if node is None: return []
    if node.type in {'identifier', 'self'}: return [node]
    if node.type in {'tuple_pattern', 'tuple_struct_pattern', 'reference_pattern', 'mut_pattern', 'captured_pattern', 'closure_parameters'}:
        return [binder for child in _c(node) if child != _f(node, 'type') for binder in _binders(child)]
    return []


class _Documents:
    def __init__(self, analysis: Any):
        self.a = analysis
        self.necessary = []
        self.records = []
        self.authenticated_documents = []
        self.document_operations = 0

    def gap(self, code: str, **details: Any):
        item = {'code': code, **details}
        self.necessary.append(item)
        self.a.gap(code, **details)

    def fact(self, kind: str, document: Any, node: Any, **details: Any) -> dict:
        return self.a.fact(kind, document, node, documentation_relation_version=VERSION, **details)

    def text_fact(self, kind: str, role: str, path: str, capture: dict, text: str,
                  start: int, end: int, **details: Any) -> dict:
        raw = text.encode('utf-8'); prefix = text[:start].encode('utf-8'); selected = text[start:end].encode('utf-8')
        if len(self.a.source_facts) >= _FACT_LIMIT:
            self.a.incomplete = True
            self.gap('documentation_fact_budget_exhausted')
            return {}
        location = {'file': path, 'line': text.count('\n', 0, start) + 1,
            'end_line': text.count('\n', 0, end) + 1, 'start_byte': len(prefix), 'end_byte': len(prefix) + len(selected),
            'coordinate_space': 'captured_document_text_utf8', 'source_hash': capture['hash'],
            'text_sha256': capture['text_hash'], 'span_hash': hashlib.sha256(selected).hexdigest(),
            'source_excerpt': text[start:end], 'source_excerpt_truncated': False,
            'original_file_byte_offset': 0 if hashlib.sha256(raw).hexdigest() == capture['hash'] else 3}
        location['column'] = len(prefix.rsplit(b'\n', 1)[-1]) + 1
        location['end_column'] = len(raw[:location['end_byte']].rsplit(b'\n', 1)[-1]) + 1
        location['column_unit'] = 'utf8_bytes'
        location['original_file_start_byte'] = location['start_byte'] + location['original_file_byte_offset']
        location['original_file_end_byte'] = location['end_byte'] + location['original_file_byte_offset']
        record = {'kind': kind, 'origin': 'captured-document-text', 'snapshot_id': self.a.snapshot.id,
            'document_role': role, 'location': location, 'document_is_ast_or_calls_evidence': False,
            'documentation_relation_version': VERSION, **details}
        record['id'] = _hash(record)[:24]
        self.a.source_facts.append(record)
        self.records.append(record)
        return record

    def blocks(self, text: str) -> list[dict]:
        lines = text.splitlines(keepends=True)
        records, headings, pending = [], [], []
        offset, fence = 0, None
        def flush():
            if pending:
                start, end = pending[0][0], pending[-1][1]
                content = text[start:end].rstrip('\r\n')
                records.append({'kind': 'paragraph', 'start': start, 'end': start + len(content),
                    'text': content, 'headings': list(headings), 'quoted': all(line.lstrip().startswith('>') for _, _, line in pending)})
                pending.clear()
        for line in lines:
            stripped = line.strip()
            marker = re.match(r'^(`{3,}|~{3,})', stripped)
            if marker:
                flush()
                if fence is None: fence = (marker.group()[0], len(marker.group()))
                elif (marker.group()[0] == fence[0] and len(marker.group()) >= fence[1]
                        and not stripped[len(marker.group()):].strip()): fence = None
            elif fence is not None:
                pass
            else:
                heading = re.match(r'^(#{1,6})\s+(.+?)\s*#*\s*$', line.rstrip('\r\n'))
                if heading:
                    flush(); level = len(heading.group(1))
                    headings[:] = [item for item in headings if item['level'] < level]
                    headings.append({'level': level, 'text': heading.group(2), 'line': text.count('\n', 0, offset) + 1})
                elif not stripped: flush()
                elif stripped.startswith('|') and stripped.endswith('|'):
                    flush()
                    if not re.fullmatch(r'[|:\-\s]+', stripped):
                        records.append({'kind': 'table_row', 'start': offset, 'end': offset + len(line.rstrip('\r\n')),
                            'text': line.rstrip('\r\n'), 'headings': list(headings), 'quoted': False})
                else: pending.append((offset, offset + len(line), line))
            offset += len(line)
        flush()
        return records

    def documents(self) -> list[dict]:
        claims = []
        selectors = self.a.rule.get('documents', [])
        if not selectors:
            self.gap('documentation_selectors_missing')
            return claims
        for selector in selectors:
            path, role = selector['file'], selector['role']
            capture = self.a.snapshot.input_evidence.get(path)
            if not isinstance(capture, dict) or capture.get('status') != 'captured' or not isinstance(capture.get('content'), str):
                self.gap('documentation_input_not_captured', document_role=role, file=path)
                continue
            text = capture['content']; raw = text.encode('utf-8')
            if (len(raw) > _DOCUMENT_BYTES or hashlib.sha256(raw).hexdigest() != capture.get('text_hash')
                    or not any(capture.get('hash') == hashlib.sha256(prefix + raw).hexdigest() and capture.get('size_bytes') == len(prefix + raw)
                    for prefix in (b'', b'\xef\xbb\xbf'))):
                self.gap('documentation_text_identity_or_size_unknown', document_role=role, file=path)
                continue
            self.authenticated_documents.append({'role': role, 'file': path, 'source_hash': capture['hash'],
                'text_hash': capture['text_hash'], 'size_bytes': capture['size_bytes'],
                'raw_prefix_bytes': capture['size_bytes'] - len(raw), 'evidence_kind': 'captured_document_text_not_ast'})
            blocks = self.blocks(text)
            for index, block in enumerate(blocks):
                # Explicit finite clause grammar, not keyword co-occurrence.
                # A quoted/negated/qualified occurrence remains evidence but is
                # not promoted to an unconditional project-wide assertion.
                delimiters = r'(?<!\\)\||[。！？!?]' if block['kind'] == 'table_row' else r'[。！？!?]'
                spans, cursor = [], 0
                for delimiter in re.finditer(delimiters, block['text']):
                    spans.append((cursor, delimiter.start())); cursor = delimiter.end()
                spans.append((cursor, len(block['text'])))
                for sentence_start, sentence_end in spans:
                    part = block['text'][sentence_start:sentence_end]
                    sentence = part.strip(' >\r\n|')
                    if not sentence: continue
                    clause_quoted = block['quoted'] or any(line.lstrip().startswith('>') for line in part.splitlines() if line.strip())
                    sentence_start += len(part) - len(part.lstrip(' >\r\n|'))
                    sentence_end = sentence_start + len(sentence)
                    self.document_operations += 1
                    self.a.operations += 1
                    if self.document_operations > _LIMIT:
                        self.a.incomplete = True
                        self.gap('documentation_clause_budget_exhausted', limit=_LIMIT)
                        return claims
                    compact = re.sub(r'\s+', ' ', sentence).strip()
                    gateway = re.fullmatch(r'Provider Gateway\s*(是|不是|并非)\s*(Control Plane)\s*内部的(唯一|非唯一)模型路由和(长期)\s*Credential\s*使用者', compact)
                    worker = re.match(r'^Worker\s*(只|不只|并非只|并不只)通过\s*`(execution-port-model-stream)`\s*请求模型并接收流(?:[；;].*)?$', compact)
                    if not gateway and not worker: continue
                    previous = blocks[index - 1] if index and blocks[index - 1]['headings'] == block['headings'] else None
                    following = blocks[index + 1] if index + 1 < len(blocks) and blocks[index + 1]['headings'] == block['headings'] else None
                    context = '\n'.join([*(heading['text'] for heading in block['headings']), *(value['text'] for value in [previous, block, following] if value)])
                    negations = re.findall(r'不是|并非|不再|不能|不一定|并不|不只|非唯一|\bnot\b|\bnever\b', compact, flags=re.I)
                    exceptions = re.findall(r'除了|除外|除非|例外|但|不过|\bexcept\b|\bunless\b', context, flags=re.I)
                    heading_qualifiers = [heading['text'] for heading in block['headings'] if re.search(r'(?:Device|Server|Worker|企业|本地|云端)\s*(?:部署|模式)', heading['text'])]
                    scope_terms = re.findall(r'(?:仅在|仅限|只在|针对|对于|限于)(?:[^。；;\n]{0,28})(?:部署|模式|Device|Worker|Server|Control Plane)', context) + heading_qualifiers
                    paragraph = self.text_fact('documentation_normative_block', role, path, capture, text,
                        block['start'], block['end'], block_kind=block['kind'], heading_context=block['headings'],
                        previous_same_heading_block=previous['text'] if previous else None,
                        following_same_heading_block=following['text'] if following else None,
                        quoted=block['quoted'], document_semantics_model=MODEL)
                    clause = self.text_fact('documentation_explicit_exclusive_clause', role, path, capture, text,
                        block['start'] + sentence_start, block['start'] + sentence_end,
                        sentence=sentence, block_fact_id=paragraph.get('id'), heading_context=block['headings'],
                        clause_kind='control_plane_internal_gateway_exclusivity' if gateway else 'worker_model_stream_only',
                        actor='Provider Gateway' if gateway else 'Worker', exclusive_quantifier=gateway[3] if gateway else worker[1],
                        explicit_scope='Control Plane 内部' if gateway else None,
                        credential_duration='long_term_in_document' if gateway else
                            'short_term_reference_in_request_clause' if '请求中只带短期引用' in compact else 'unknown',
                        negations=negations, exception_markers=exceptions, explicit_deployment_qualifiers=scope_terms,
                        quoted=clause_quoted,
                        eligible_unqualified_clause=not (clause_quoted or negations or exceptions or scope_terms),
                        claim_is_source_runtime_or_security_fact=False)
                    claims.append(clause)
        if not claims: self.gap('documentation_supported_explicit_clause_not_found')
        return claims

    def nodes(self, role: str, nested: bool = False) -> list[Any]:
        document, _, function = self.a.roles[role]
        return self.a.nodes(document, _f(function, 'body'), nested=nested)

    def call_name(self, document: Any, call: Any) -> str:
        function = _f(call, 'function')
        while function is not None and function.type == 'generic_function': function = _f(function, 'function')
        return document.text(_f(function, 'field') or _f(function, 'name') or function)

    def name(self, role: str) -> str:
        document, _, function = self.a.roles[role]
        return document.text(_f(function, 'name'))

    def calls(self, role: str, target: str | None = None, nested: bool = False) -> list[Any]:
        document = self.a.roles[role][0]
        return [node for node in self.nodes(role, nested) if node.type == 'call_expression'
            and (target is None or self.call_name(document, node) == self.name(target))]

    def args(self, node: Any) -> list[Any]: return _c(_f(node, 'arguments'))

    def binder(self, role: str, node: Any) -> dict | None:
        document, _, function = self.a.roles[role]
        node = _u(node)
        if node is None or node.type not in {'identifier', 'self'}: return None
        name = document.text(node); ancestors = list(_ancestors(node)); ancestor_ids = {item.id for item in ancestors}
        candidates = []
        # Rust's initializer sees previous bindings; the newly shadowing let
        # becomes visible only after its complete declaration. No writes are
        # erased, and this is lexical source identity rather than heap identity.
        for owner in ancestors:
            if owner.type not in _FUNCTIONS: continue
            parameters = _f(owner, 'parameters')
            for parameter in _c(parameters):
                pattern = _f(parameter, 'pattern') or parameter
                names = _binders(pattern)
                if parameter.type == 'self_parameter': names = [item for item in self.a.nodes(document, parameter) if item.type == 'self']
                for binder in names:
                    if document.text(binder) == name: candidates.append((owner, parameter, binder))
        for declaration in self.nodes(role, nested=True):
            if declaration.type != 'let_declaration' or declaration.end_byte > node.start_byte: continue
            scope = next((item for item in _ancestors(declaration.parent) if item.type == 'block'), None)
            if scope is None or scope.id not in ancestor_ids: continue
            for binder in _binders(_f(declaration, 'pattern')):
                if document.text(binder) == name: candidates.append((scope, declaration, binder))
        if not candidates: return None
        size = min(scope.end_byte - scope.start_byte for scope, _, _ in candidates)
        candidates = [value for value in candidates if value[0].end_byte - value[0].start_byte == size]
        latest = max(declaration.end_byte for _, declaration, _ in candidates)
        candidates = [value for value in candidates if value[1].end_byte == latest]
        if len(candidates) != 1: return None
        scope, declaration, binder = candidates[0]
        return {'name': name, 'file': document.source.path, 'declaration_span': [declaration.start_byte, declaration.end_byte],
            'binder_span': [binder.start_byte, binder.end_byte], 'lexical_source_only': True}

    def path(self, role: str, node: Any) -> dict | None:
        document = self.a.roles[role][0]; node = _u(node)
        if node is None: return None
        if node.type in {'identifier', 'self'}:
            root = self.binder(role, node)
            return {'root': root, 'members': []} if root else None
        if node.type == 'field_expression':
            root = self.path(role, _f(node, 'value'))
            key = _f(node, 'field')
            return {**root, 'members': [*root['members'], document.text(key)]} if root and key is not None else None
        return None

    def same(self, role: str, left: Any, right: Any) -> bool:
        a, b = self.path(role, left), self.path(role, right)
        return bool(a and b and a == b)

    def binding(self, role: str, call: Any, target: str) -> dict:
        document, definition, _ = self.a.roles[role]
        edge, issues = self.a.sources.call_binding(call, document, definition)
        expected = self.a.roles[target][1].graph_node_id
        raw_sites = self.a.sources.edges.get((document.source.path, call.start_point.row + 1, call.start_point.column), [])
        raw_matches = []
        for site in raw_sites:
            anchor = f'{document.source.path}:{site.source}:{call.start_byte}:{call.end_byte}'
            if site.id == 'rust-call:' + hashlib.sha256(anchor.encode()).hexdigest()[:24]: raw_matches.append(site)
        raw = raw_matches[0] if len(raw_matches) == 1 else None
        actual = self.a.sources.nodes.get(expected, [])
        caller = self.a.sources.nodes.get(definition.graph_node_id, [])
        selected_type = actual[0].metadata.get('impl_type_id') if len(actual) == 1 else None
        caller_type = caller[0].metadata.get('impl_type_id') if len(caller) == 1 else None
        function = _f(call, 'function')
        receiver = _f(function, 'value')
        same_receiver = bool(len(actual) == len(caller) == 1 and receiver is not None
            and document.text(receiver) == 'self' and selected_type
            and selected_type == caller_type
            and actual[0].metadata.get('crate_root') == caller[0].metadata.get('crate_root')
            and not actual[0].metadata.get('impl_trait_implementation')
            and not caller[0].metadata.get('impl_trait_implementation')
            and self.call_name(document, call) == self.name(target))
        qualifier = _f(function, 'path')
        qualified_receiver = bool(len(actual) == 1 and qualifier is not None
            and document.text(qualifier).split('::')[-1] == actual[0].metadata.get('impl_type_name')
            and actual[0].metadata.get('static_method') and not actual[0].metadata.get('impl_trait_implementation'))
        candidate = bool(raw and expected in [raw.target, *raw.candidates])
        selected_types = self.a.sources.nodes.get(selected_type, []) if selected_type else []
        receiver_candidate = bool(raw and (same_receiver or qualified_receiver)
            and selected_type in raw.candidates and len(selected_types) == 1
            and selected_types[0].kind == 'type' and not selected_types[0].metadata.get('type_alias_unknown'))
        contextual = bool(candidate or receiver_candidate)
        return {'authenticated_target': bool(edge and edge.target == expected),
            'captured_contextual_source_reference': contextual,
            'contextual_reference_basis': 'exact_saved_candidate' if candidate else 'explicit_self_or_qualified_inherent_type_and_saved_receiver_candidate' if receiver_candidate else None,
            'selected_receiver_type_id': selected_type, 'caller_receiver_type_id': caller_type,
            'saved_edge': {'id': raw.id, 'resolution': raw.resolution, 'target': raw.target, 'candidates': raw.candidates, 'reason': raw.reason} if raw else None,
            'callee_activation_or_unique_trait_dispatch_proven': False,
            'edge_id': edge.id if edge else None, 'expected_selected_declaration': expected,
            'gaps': issues, 'callee_source': document.text(_f(call, 'function')),
            'creates_or_repairs_calls_edge': False}

    def source(self) -> tuple[dict, list[dict]]:
        witnesses, facts = {}, []
        def record(key: str, role: str, node: Any, supported: bool, **details: Any):
            document = self.a.roles[role][0]
            fact = self.fact('document_deployment_source_relation', document, node,
                relation=key, supported=supported, selected_role=role, source_model=MODEL,
                runtime_activation_or_effect_proven=False, **details)
            facts.append(fact); witnesses[key] = bool(supported)
        # Installation and the early local-consumption guard use the same
        # recorded self field. Generic instance selection is explicitly scoped.
        installation, _, install_fn = self.a.roles['worker_installation']
        device_open = [node for node in self.calls('worker_installation') if self.call_name(installation, node) == 'open']
        assignments = [node for node in self.nodes('worker_installation') if node.type == 'assignment_expression'
            and _f(node, 'left') is not None and installation.text(_f(node, 'left')).startswith('self.')]
        # Resolve the actual initializer target, then its local use in Some(...).
        candidate_installs = []
        for call in device_open:
            callee = _u(_f(call, 'function'))
            if callee is None: continue
            edge, issues = self.a.sources.call_binding(call, installation, self.a.roles['worker_installation'][1])
            if edge is None: continue
            targets = self.a.sources.nodes.get(edge.target, [])
            expected = self.a.sources.nodes.get(self.a.roles['device_send'][1].graph_node_id, [])
            if (len(targets) != 1 or len(expected) != 1 or targets[0].file != expected[0].file
                    or targets[0].metadata.get('impl_type_name') != expected[0].metadata.get('impl_type_name')): continue
            declarations = [node for node in self.nodes('worker_installation') if node.type == 'let_declaration' and _inside(_f(node, 'value'), call)]
            for declaration in declarations:
                binders = _binders(_f(declaration, 'pattern'))
                if len(binders) != 1: continue
                for assignment in assignments:
                    right = _u(_f(assignment, 'right'))
                    args = self.args(right) if right is not None and right.type == 'call_expression' else []
                    if len(args) == 1 and self.call_name(installation, right) == 'Some':
                        token = self.binder('worker_installation', args[0])
                        if token and token['binder_span'] == [binders[0].start_byte, binders[0].end_byte]:
                            candidate_installs.append((assignment, call, edge, token))
        install_ok = len(candidate_installs) == 1
        field_name = None
        if install_ok:
            assignment, call, edge, token = candidate_installs[0]
            field_name = installation.text(_f(_f(assignment, 'left'), 'field'))
            record('worker_installs_captured_local_model_field', 'worker_installation', assignment, True,
                initialized_from_authenticated_call=edge.id, initialized_type_declaration=edge.target,
                field_name=field_name, installed_local_binder=token, generic_instance_globally_bound=False)
        else: witnesses['worker_installs_captured_local_model_field'] = False
        route_doc, _, route_fn = self.a.roles['worker_route']
        route_nodes = self.a.sources.nodes.get(self.a.roles['worker_route'][1].graph_node_id, [])
        install_nodes = self.a.sources.nodes.get(self.a.roles['worker_installation'][1].graph_node_id, [])
        same_worker_type = bool(len(route_nodes) == len(install_nodes) == 1
            and route_nodes[0].metadata.get('impl_type_id')
            and route_nodes[0].metadata.get('impl_type_id') == install_nodes[0].metadata.get('impl_type_id'))
        message_type_sources = [route_doc.text(_f(parameter, 'type')) for parameter in _c(_f(route_fn, 'parameters'))
            if re.fullmatch(r'(?:[A-Za-z_]\w*::)*ExecutionPortMessage', route_doc.text(_f(parameter, 'type')).strip())]
        route_candidates = []
        for node in self.nodes('worker_route'):
            if node.type != 'if_expression': continue
            condition, consequence = _f(node, 'condition'), _f(node, 'consequence')
            fields = [value for value in self.a.nodes(route_doc, condition) if value.type == 'field_expression'
                and route_doc.text(_f(value, 'field')) == field_name and route_doc.text(_f(value, 'value')) == 'self']
            sends = [call for call in self.calls('worker_route') if _inside(condition, call)
                and self.call_name(route_doc, call) == self.name('device_send')]
            returns = [value for value in self.a.nodes(route_doc, consequence) if value.type == 'return_expression']
            later = [call for call in self.calls('worker_route') if call.start_byte > node.end_byte and self.call_name(route_doc, call) == self.name('device_send')]
            let_conditions = [value for value in self.a.nodes(route_doc, condition) if value.type == 'let_condition'
                and any(_inside(_f(value, 'value'), field) for field in fields)]
            guarded_binders = [binder for value in let_conditions for binder in _binders(_f(value, 'pattern'))]
            method_sends = [call for call in sends if any(route_doc.text(binder) == route_doc.text(_f(_f(call, 'function'), 'value')) for binder in guarded_binders)]
            parameter_links = [self.same('worker_route', self.args(call)[0], self.args(fallback)[0])
                for call in method_sends for fallback in later if len(self.args(call)) == len(self.args(fallback)) == 1]
            ok_returns = [value for value in returns if any(self.call_name(route_doc, call) == 'Ok' for call in self.a.nodes(route_doc, value) if call.type == 'call_expression')]
            if fields and method_sends and ok_returns and any(parameter_links): route_candidates.append((node, method_sends, later))
        record('worker_local_consumer_guard_precedes_transport_fallback_source', 'worker_route', route_fn,
            same_worker_type and len(route_candidates) == 1 and len(message_type_sources) == 1, field_name=field_name,
            same_saved_worker_receiver_type=same_worker_type,
            message_type_sources=message_type_sources,
            guard_sources=[route_doc.location(node) for node, _, _ in route_candidates],
            same_runtime_instance_or_actual_message_routing_proven=False,
            execution_port_typed_message_compatibility_not_refuted=True)
        bootstrap_doc, _, bootstrap_fn = self.a.roles['worker_bootstrap']
        bootstrap_calls = self.calls('worker_bootstrap', 'worker_installation')
        bootstrap_sources = []
        selected_installations = self.a.sources.nodes.get(self.a.roles['worker_installation'][1].graph_node_id, [])
        installation_type = selected_installations[0].metadata.get('impl_type_id') if len(selected_installations) == 1 else None
        for call in bootstrap_calls:
            binding = self.binding('worker_bootstrap', call, 'worker_installation')
            receiver = _u(_f(_f(call, 'function'), 'value'))
            constructor = None
            if receiver is not None and receiver.type == 'call_expression':
                edge, issues = self.a.sources.call_binding(receiver, bootstrap_doc, self.a.roles['worker_bootstrap'][1])
                targets = self.a.sources.nodes.get(edge.target, []) if edge else []
                if len(targets) == 1 and installation_type and targets[0].metadata.get('impl_type_id') == installation_type and targets[0].metadata.get('static_method'):
                    constructor = {'edge_id': edge.id, 'target': edge.target,
                        'receiver_type_id': installation_type, 'location': bootstrap_doc.location(receiver)}
            if binding['authenticated_target'] or binding['captured_contextual_source_reference'] or constructor:
                bootstrap_sources.append({'installation_reference': binding, 'authenticated_receiver_constructor': constructor,
                    'unique_generic_method_dispatch_proven': False})
        record('production_bootstrap_contains_selected_provider_installation_candidate', 'worker_bootstrap', bootstrap_fn,
            len(bootstrap_calls) == len(bootstrap_sources) == 1, invocation_sources=[bootstrap_doc.location(call) for call in bootstrap_calls],
            installation_source_candidates=bootstrap_sources,
            unique_generic_method_dispatch_proven=False)
        # A Device ModelOpen source branch supplies a local store to an
        # and_then callback; deferred activation is not promoted to execution.
        device_doc, _, device_fn = self.a.roles['device_send']
        store_calls = self.calls('device_send', 'store_open', nested=True)
        execute_calls = self.calls('device_send', 'model_execute', nested=True)
        callback_pairs = []
        for execute in execute_calls:
            callback = next((node for node in _ancestors(execute.parent) if node.type == 'closure_expression'), None)
            if callback is None: continue
            parent = callback.parent
            outer = parent.parent if parent is not None else None
            while outer is not None and outer.type != 'call_expression': outer = outer.parent
            function = _f(outer, 'function')
            receiver = _u(_f(function, 'value'))
            if outer is None or self.call_name(device_doc, outer) != 'and_then' or receiver not in store_calls: continue
            binders = _binders(_f(callback, 'parameters'))
            callee_receiver = _f(_f(execute, 'function'), 'value')
            if len(binders) == 1 and callee_receiver is not None and device_doc.text(binders[0]) == device_doc.text(callee_receiver):
                store_binding = self.binding('device_send', receiver, 'store_open')
                store_nodes = self.a.sources.nodes.get(self.a.roles['store_open'][1].graph_node_id, [])
                execute_nodes = self.a.sources.nodes.get(self.a.roles['model_execute'][1].graph_node_id, [])
                receiver_type_same = bool(len(store_nodes) == len(execute_nodes) == 1
                    and store_nodes[0].metadata.get('impl_type_id')
                    and store_nodes[0].metadata.get('impl_type_id') == execute_nodes[0].metadata.get('impl_type_id'))
                if receiver_type_same and (store_binding['authenticated_target'] or store_binding['captured_contextual_source_reference']):
                    callback_pairs.append((receiver, execute, callback, store_binding))
        record('device_message_body_connects_local_store_to_model_callback_source', 'device_send', device_fn,
            len(callback_pairs) == 1,
            callback_sources=[device_doc.location(callback) for _, _, callback, _ in callback_pairs],
            store_constructor_bindings=[binding for _, _, _, binding in callback_pairs],
            callback_activation_proven=False, ordinary_result_and_then_source_model_required=True,
            callback_to_unique_runtime_callee_proven=False)
        execute_doc, _, execute_fn = self.a.roles['model_execute']
        invoke_calls = self.calls('model_execute', 'model_invoke')
        invoke_bindings = [self.binding('model_execute', call, 'model_invoke') for call in invoke_calls]
        record('local_execute_contains_selected_invoke_source', 'model_execute', execute_fn,
            len(invoke_calls) == 1 and (invoke_bindings[0]['authenticated_target'] or invoke_bindings[0]['captured_contextual_source_reference']), call_bindings=invoke_bindings,
            replay_cancelled_error_and_interrupted_branches_preserved=True)
        # Same tuple binder supplies config to the actual factory and material
        # to the selected provider invocation operand. No name-only flow.
        invoke_doc, _, invoke_fn = self.a.roles['model_invoke']
        resolves = self.calls('model_invoke', 'secret_resolver')
        factories = self.calls('model_invoke', 'provider_factory')
        provider_calls = self.calls('model_invoke', 'provider_open')
        tuple_joins = []
        for resolver in resolves:
            declaration = next((node for node in _ancestors(resolver.parent) if node.type == 'let_declaration'), None)
            binders = _binders(_f(declaration, 'pattern'))
            if len(binders) != 2: continue
            for factory in factories:
                arguments = self.args(factory)
                factory_decl = next((node for node in _ancestors(factory.parent) if node.type == 'let_declaration'), None)
                factory_binders = _binders(_f(factory_decl, 'pattern'))
                if len(arguments) != 1 or len(factory_binders) != 1: continue
                config = self.binder('model_invoke', arguments[0])
                for opened in provider_calls:
                    args = self.args(opened); receiver = _f(_f(opened, 'function'), 'value')
                    secret = self.binder('model_invoke', args[1]) if len(args) == 2 else None
                    adapter = self.binder('model_invoke', receiver)
                    if (config and secret and adapter and config['binder_span'] == [binders[0].start_byte, binders[0].end_byte]
                            and secret['binder_span'] == [binders[1].start_byte, binders[1].end_byte]
                            and adapter['binder_span'] == [factory_binders[0].start_byte, factory_binders[0].end_byte]):
                        tuple_joins.append({'resolver_binding': self.binding('model_invoke', resolver, 'secret_resolver'),
                            'factory_binding': self.binding('model_invoke', factory, 'provider_factory'),
                            'config': config, 'secret': secret, 'adapter': adapter,
                            'provider_call_location': invoke_doc.location(opened),
                            'ordinary_provider_trait_dispatch_proven': False})
        record('resolved_config_and_secret_reach_same_local_provider_source', 'model_invoke', invoke_fn,
            len(tuple_joins) == 1 and all(tuple_joins[0][key]['authenticated_target'] or tuple_joins[0][key]['captured_contextual_source_reference'] for key in ('resolver_binding', 'factory_binding')),
            tuple_source_joins=tuple_joins, secret_ttl_or_long_term_status_proven=False)
        resolver_doc, _, resolver_fn = self.a.roles['secret_resolver']
        queries = [node for node in self.calls('secret_resolver') if self.call_name(resolver_doc, node) == 'query_row']
        constructors = self.calls('secret_resolver', 'secret_constructor')
        material = []
        for call in queries:
            args = self.args(call)
            sql = _literal_string(resolver_doc.text(_u(args[0]))) if args else None
            declaration = next((node for node in _ancestors(call.parent) if node.type == 'let_declaration'), None)
            binders = _binders(_f(declaration, 'pattern'))
            if not sql or len(binders) != 2: continue
            columns = re.fullmatch(r'\s*SELECT\s+([A-Za-z_][A-Za-z_0-9]*)\s*,\s*([A-Za-z_][A-Za-z_0-9]*)\s+FROM\s+([A-Za-z_][A-Za-z_0-9]*)\s+WHERE\s+([A-Za-z_][A-Za-z_0-9]*)\s*=\s*\?1\s*', sql, flags=re.I)
            if columns is None: continue
            query_type = _f(declaration, 'type')
            tuple_types = _c(query_type) if query_type is not None and query_type.type == 'tuple_type' else []
            callback = _u(args[2]) if len(args) == 3 else None
            callback_binders = _binders(_f(callback, 'parameters')) if callback is not None and callback.type == 'closure_expression' else []
            body = _u(_f(callback, 'body'))
            result_args = self.args(body) if body is not None and body.type == 'call_expression' and self.call_name(resolver_doc, body) == 'Ok' else []
            row_tuple = _u(result_args[0]) if len(result_args) == 1 else None
            row_values = _c(row_tuple) if row_tuple is not None and row_tuple.type == 'tuple_expression' else []
            row_indices = []
            for value in row_values:
                get = _u(value)
                arguments = self.args(get) if get is not None and get.type == 'call_expression' else []
                token = self.binder('secret_resolver', _f(_f(get, 'function'), 'value'))
                if (get is not None and self.call_name(resolver_doc, get) == 'get' and len(arguments) == 1
                        and token and len(callback_binders) == 1
                        and token['binder_span'] == [callback_binders[0].start_byte, callback_binders[0].end_byte]
                        and arguments[0].type == 'integer_literal'):
                    row_indices.append(resolver_doc.text(arguments[0]))
            if row_indices != ['0', '1'] or len(tuple_types) != 2: continue
            for constructor in constructors:
                argument = self.args(constructor)
                token = self.binder('secret_resolver', argument[0]) if len(argument) == 1 else None
                if token and token['binder_span'] == [binders[1].start_byte, binders[1].end_byte]:
                    material.append({'sql_source': sql, 'selected_columns': [columns[1], columns[2]],
                        'source_material_column': columns[2], 'declared_tuple_type': resolver_doc.text(query_type),
                        'material_type_source': resolver_doc.text(tuple_types[1]),
                        'row_projection_indices': row_indices, 'row_callback_source': resolver_doc.location(callback),
                        'constructor_binding': self.binding('secret_resolver', constructor, 'secret_constructor'),
                        'material_binder': token, 'database_read_executed': False})
        record('local_resolver_passes_captured_byte_material_to_secret_constructor', 'secret_resolver', resolver_fn,
            len(material) == 1 and (material[0]['constructor_binding']['authenticated_target'] or material[0]['constructor_binding']['captured_contextual_source_reference'])
                and bool(re.fullmatch(r'Vec\s*<\s*u8\s*>', material[0]['material_type_source'].strip())),
            material_sources=material, credential_reference_id_not_equated_with_secret_bytes=True,
            actual_secret_contents_and_credential_lifetime_proven=False)
        constructor_doc, _, constructor_fn = self.a.roles['secret_constructor']
        parameters = _c(_f(constructor_fn, 'parameters'))
        byte_parameters = [parameter for parameter in parameters if re.fullmatch(r'Vec\s*<\s*u8\s*>', constructor_doc.text(_f(parameter, 'type')).strip())]
        owned_fields = []
        for node in self.nodes('secret_constructor'):
            if node.type != 'struct_expression' or constructor_doc.text(_f(node, 'name')) != 'Self': continue
            for field in _c(_f(node, 'body')):
                value = next(iter(_c(field)), None) if field.type == 'shorthand_field_initializer' else _f(field, 'value')
                token = self.binder('secret_constructor', value)
                if token and any(token['binder_span'] == [binder.start_byte, binder.end_byte]
                        for parameter in byte_parameters for binder in _binders(_f(parameter, 'pattern'))):
                    owned_fields.append({'field_source': constructor_doc.text(field), 'value_binder': token,
                        'struct_source': constructor_doc.location(node)})
        record('secret_container_constructs_owned_byte_material_source', 'secret_constructor', constructor_fn,
            len(byte_parameters) == 1 and len(owned_fields) == 1,
            parameter_types=[constructor_doc.text(_f(item, 'type')) for item in byte_parameters], owned_field_sources=owned_fields,
            secret_duration_classification='unknown', in_memory_container_does_not_establish_long_lived_credential=True)
        factory_doc, _, factory_fn = self.a.roles['provider_factory']
        fields = [node for node in self.nodes('provider_factory') if node.type == 'field_expression']
        endpoint_fields = [node for node in fields if factory_doc.text(_f(node, 'field')) == 'endpoint']
        config_parameters = [parameter for parameter in _c(_f(factory_fn, 'parameters'))
            if re.fullmatch(r'&\s*(?:[A-Za-z_]\w*::)*DeviceProviderConfig', factory_doc.text(_f(parameter, 'type')).strip())]
        provider_nodes = self.a.sources.nodes.get(self.a.roles['provider_open'][1].graph_node_id, [])
        provider_type = provider_nodes[0].metadata.get('impl_type_name') if len(provider_nodes) == 1 else None
        endpoint_joins = []
        for field in endpoint_fields:
            root = self.binder('provider_factory', _f(field, 'value'))
            if not root or not any(root['binder_span'] == [binder.start_byte, binder.end_byte]
                    for parameter in config_parameters for binder in _binders(_f(parameter, 'pattern'))): continue
            for constructor in self.calls('provider_factory'):
                function = _f(constructor, 'function')
                if function is None or function.type != 'scoped_identifier' or not any(_inside(arg, field) for arg in self.args(constructor)): continue
                declaration = next((node for node in _ancestors(constructor.parent) if node.type == 'let_declaration'), None)
                binders = _binders(_f(declaration, 'pattern'))
                if len(binders) != 1: continue
                for provider in self.calls('provider_factory'):
                    callee = _f(provider, 'function'); args = self.args(provider)
                    qualifier = factory_doc.text(_f(callee, 'path'))
                    operand = self.binder('provider_factory', args[0]) if len(args) == 1 else None
                    if (qualifier.split('::')[-1] == provider_type and operand
                            and operand['binder_span'] == [binders[0].start_byte, binders[0].end_byte]):
                        endpoint_joins.append({'config_parameter': root,
                            'endpoint_source': factory_doc.location(field), 'transport_construction_source': factory_doc.location(constructor),
                            'provider_construction_source': factory_doc.location(provider),
                            'transport_local_binder': operand, 'transport_mutations_or_runtime_endpoint_value_proven': False})
        concrete_return = factory_doc.text(_f(factory_fn, 'return_type'))
        record('local_factory_reads_endpoint_and_constructs_provider_candidate', 'provider_factory', factory_fn,
            len(endpoint_joins) == 1,
            endpoint_sources=[factory_doc.location(node) for node in endpoint_fields],
            endpoint_parameter_construction_joins=endpoint_joins,
            return_type_source=concrete_return, actual_network_destination_or_success_proven=False)
        provider_doc, _, provider_fn = self.a.roles['provider_open']
        provider_parameters = _c(_f(provider_fn, 'parameters'))
        parameter_types = [provider_doc.text(_f(parameter, 'type')) for parameter in provider_parameters]
        secret_parameters = [parameter for parameter in provider_parameters
            if re.fullmatch(r"&\s*(?:'[A-Za-z_]\w*\s+)?(?:[A-Za-z_]\w*::)*ResolvedSecret", provider_doc.text(_f(parameter, 'type')).strip())]
        expose = []
        for call in self.calls('provider_open'):
            if self.call_name(provider_doc, call) != 'expose': continue
            receiver = self.binder('provider_open', _f(_f(call, 'function'), 'value'))
            if receiver and any(receiver['binder_span'] == [binder.start_byte, binder.end_byte]
                    for parameter in secret_parameters for binder in _binders(_f(parameter, 'pattern'))): expose.append(call)
        record('selected_provider_method_exposes_secret_operand_source', 'provider_open', provider_fn,
            len(expose) == 1 and len(secret_parameters) == 1,
            parameter_type_sources=parameter_types, exposure_sources=[provider_doc.location(call) for call in expose],
            selected_trait_implementation_runtime_activation_proven=False)
        boundary_doc, _, boundary_fn = self.a.roles['server_boundary']
        unsupported = [call for call in self.calls('server_boundary')
            if self.call_name(boundary_doc, call) == 'Err' and len(self.args(call)) == 1
            and boundary_doc.text(_u(self.args(call)[0])).endswith('::UnsupportedMessage')]
        record('server_boundary_retains_unsupported_result_source', 'server_boundary', boundary_fn,
            bool(unsupported), boundary_result_sources=[boundary_doc.location(node) for node in unsupported],
            one_boundary_does_not_establish_all_deployments_absent=True)
        return witnesses, facts


def analyze_pattern(analysis: Any) -> dict:
    reader = _Documents(analysis)
    missing = sorted(REQUIRED_ROLES - set(analysis.roles))
    if missing: reader.gap('documentation_source_roles_missing', roles=missing)
    if not {MODEL, CONTROL_MODEL}.issubset(analysis.rule.get('models', [])):
        reader.gap('documentation_model_not_registered', required_models=[MODEL, CONTROL_MODEL])
    claims = reader.documents()
    witnesses, facts = reader.source() if not missing else ({}, [])
    for key, supported in witnesses.items():
        if not supported: reader.gap('documentation_source_relation_not_closed', relation=key)
    clauses = [claim for claim in claims if claim.get('eligible_unqualified_clause')]
    claim_groups = {}
    for claim in clauses: claim_groups.setdefault((claim['document_role'], claim['location']['file'], claim.get('block_fact_id')), set()).add(claim['clause_kind'])
    explicit = any({'control_plane_internal_gateway_exclusivity', 'worker_model_stream_only'}.issubset(group) for group in claim_groups.values())
    if not explicit: reader.gap('documentation_local_exclusive_clause_scope_not_closed')
    documents_authenticated = bool(analysis.rule.get('documents')) and len(reader.authenticated_documents) == len(analysis.rule['documents'])
    declarations_closed = all(analysis.role_binding_closed.get(role) for role in REQUIRED_ROLES)
    if not declarations_closed: reader.gap('documentation_selected_declaration_binding_not_closed')
    supported = bool(explicit and documents_authenticated and declarations_closed and witnesses
        and all(witnesses.values()) and not reader.necessary and not analysis.incomplete)
    fact_by_relation = {fact['relation']: fact['id'] for fact in facts}
    material_keys = ('local_resolver_passes_captured_byte_material_to_secret_constructor',
        'secret_container_constructs_owned_byte_material_source', 'selected_provider_method_exposes_secret_operand_source')
    stream_keys = ('worker_local_consumer_guard_precedes_transport_fallback_source',
        'device_message_body_connects_local_store_to_model_callback_source')
    material_supported = bool(documents_authenticated and declarations_closed and not analysis.incomplete
        and any(claim['clause_kind'] == 'control_plane_internal_gateway_exclusivity' for claim in clauses)
        and all(witnesses.get(key) for key in material_keys))
    stream_supported = bool(documents_authenticated and declarations_closed and not analysis.incomplete
        and any(claim['clause_kind'] == 'worker_model_stream_only' for claim in clauses)
        and all(witnesses.get(key) for key in stream_keys))
    comparisons = [
        {'aspect': 'documented_control_plane_scope_and_device_source_route',
         'classification': 'selected_document_wording_requires_device_deployment_qualification' if supported else 'unknown_or_partial_source_comparison',
         'statement': '文档明确限定Control Plane内部唯一；所选Device源码另有本地provider装配、消费及凭据字节操作来源，宜补充部署分支说明，不能把内部唯一扩成全项目唯一。' if supported else '所选文档或Device源码关系仍有必要缺口，不能补造部署一致性结论。',
         'document_fact_ids': [claim['id'] for claim in clauses], 'source_fact_ids': list(fact_by_relation.values()),
         'scoped_source_supported': supported,
         'global_project_exclusivity_refuted': False, 'runtime_path_proven': False},
        {'aspect': 'credential_material_reference_and_lifetime',
         'classification': 'material_source_distinguished_lifetime_unknown' if material_supported else 'unknown_or_partial_source_comparison',
         'statement': '文档谈长期Credential；所选代码来源为Vec<u8>/ResolvedSecret字节容器，字节材料与凭据引用须区分，也无法据此确定凭据长期性或公开Delivery密钥泄露。' if material_supported else '所选文档或凭据字节来源关系仍有缺口，凭据材料、引用及长期性对照保留unknown。',
         'document_fact_ids': [claim['id'] for claim in clauses if claim['clause_kind'] == 'control_plane_internal_gateway_exclusivity'],
         'source_fact_ids': [fact_by_relation[key] for key in material_keys if key in fact_by_relation],
         'scoped_source_supported': material_supported,
         'credential_lifetime': 'unknown', 'security_defect_declared': False},
        {'aspect': 'worker_stream_protocol_and_local_consumer',
         'classification': 'local_source_route_does_not_prove_stream_protocol_bypass' if stream_supported else 'unknown_or_partial_source_comparison',
         'statement': 'Worker源码在本地消费者返回Ok(true)时提前返回；正常未消费分支走transport，错误可提前传播。仍使用ExecutionPort消息，不能由本地provider路径推断绕过模型流协议。' if stream_supported else '所选Worker本地消费者或Device回调来源关系仍有缺口，不能补造完整本地路径，协议绕过仍未证明。',
         'document_fact_ids': [claim['id'] for claim in clauses if claim['clause_kind'] == 'worker_model_stream_only'],
         'source_fact_ids': [fact_by_relation[key] for key in stream_keys if key in fact_by_relation],
         'scoped_source_supported': stream_supported,
         'protocol_bypass_proven': False, 'deferred_callback_activation_proven': False},
    ]
    return {'version': VERSION, 'model': MODEL, 'document_claims': claims,
        'document_scope': {'selected_documents': analysis.rule.get('documents', []),
            'authenticated_documents': reader.authenticated_documents,
            'all_selected_documents_authenticated': documents_authenticated},
        'documentation_comparisons': comparisons,
        'relation_witnesses': witnesses, 'source_relation_fact_ids': [fact['id'] for fact in facts],
        'comparison': {'classification': 'selected_document_wording_requires_device_deployment_qualification' if supported else 'unknown_or_partial_source_comparison',
            'statement': '所选文档描述 Control Plane 内部唯一模型路由及 Worker 仅经模型流；所选 Device 源码另有本地 provider 选择、字节 material 容器与调用来源，表述需要说明部署范围。' if supported else None,
            'document_control_plane_internal_scope_preserved': True,
            'global_project_exclusivity_inferred_from_document': False,
            'worker_execution_port_protocol_bypass_proven': False,
            'long_term_credential_exclusivity_refuted': 'unknown',
            'secret_material_lifetime': 'unknown', 'raw_secret_reference_equated_with_material': False,
            'public_delivery_or_contract_secret_leak_proven': False,
            'security_defect_declared': False, 'actual_deployment_or_network_execution_verified': False},
        'scoped_source_supported': supported, 'necessary_gaps': reader.necessary,
        'conditions': ['captured selected production methods and deferred callbacks are activated and reached normally in the selected Device composition',
            'ordinary Rust lexical shadowing, Option/Result callback source contracts and plain captured records apply',
            'literal SQL describes selected columns under ordinary rusqlite source contracts; no query is executed',
            'selected provider implementation is a contextual source candidate; ordinary trait dispatch is not globally repaired'],
        'bounds': ['Finite Chinese clause grammar and whole block/heading context only; arbitrary natural-language equivalence and remote references remain unknown',
            'A local byte-material consumer does not establish credential lifetime, compromise, network success or a violation of public Delivery secret exclusion',
            'Typed ExecutionPort model messages remain compatible with the local source route; this comparison does not prove protocol bypass',
            'Source callback and branch relationships do not prove runtime activation, credential availability, all deployments or all credential paths'],
        'whole_report_reproduction_claimed': False, 'target_executed': False, 'target_tests_run': False, 'target_build_run': False}
