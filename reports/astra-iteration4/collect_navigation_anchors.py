"""Independent source-anchor collection for the v0.7 navigation review.

This is a report collector, not a detector or test. Selectors identify reviewed
source sites. All observed AST shapes, arguments, keys, conditions and quotes
are read from original target bytes using the fixed CallScope grammar channel.
It never imports or executes target modules, mutates a target, or edits the
frozen capability baseline. No pass/fail or expected key set is prefilled.
"""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

TOOL_ROOT = Path('/workspace/callscope')
TARGET_ROOT = Path('/workspace/winwincode')
REPORT_ROOT = TOOL_ROOT / 'reports/astra-iteration4'
sys.path.insert(0, str(TOOL_ROOT))

from callscope.parsers import language_parser, parser_version
from callscope.syntax_projection import parse_with_projection

FUNCTIONS = frozenset({
    'function_declaration', 'generator_function_declaration', 'method_definition',
    'function_expression', 'arrow_function', 'generator_function',
})
WRAPPERS = frozenset({
    'parenthesized_expression', 'as_expression', 'satisfies_expression',
    'non_null_expression',
})


def digest(data):
    return hashlib.sha256(data).hexdigest()


def walk(node, prune_functions=False):
    yield node
    if prune_functions and node.type in FUNCTIONS:
        return
    for child in node.named_children:
        yield from walk(child, prune_functions)


class Document:
    def __init__(self, path):
        self.path = path
        self.data = (TARGET_ROOT / path).read_bytes()
        self.hash = digest(self.data)
        self.tree, self.projection = parse_with_projection(
            self.data, language_parser('typescript'), 'typescript',
        )

    def text(self, node):
        return self.data[node.start_byte:node.end_byte].decode('utf-8') if node is not None else None

    def field(self, node, name):
        return node.child_by_field_name(name) if node is not None else None

    def unwrap(self, node):
        while node is not None and node.type in WRAPPERS:
            node = self.field(node, 'expression') or next(
                (child for child in node.named_children if child.type != 'comment'), None,
            )
        return node

    def function_name(self, node):
        name = self.field(node, 'name')
        if name is not None:
            return self.text(name)
        parent = node.parent
        if parent is not None and parent.type in {'variable_declarator', 'pair'}:
            name = self.field(parent, 'name') or self.field(parent, 'key')
            if name is not None:
                return self.text(name)
        return f'<anonymous@{node.start_point.row + 1}:{node.start_point.column + 1}>'

    def owner(self, node, include_self=False):
        current = node if include_self else node.parent
        names = []
        while current is not None:
            if current.type in FUNCTIONS:
                names.append(self.function_name(current))
            current = current.parent
        return '.'.join(reversed(names)) or '<module>'

    def site(self, node):
        raw = self.data[node.start_byte:node.end_byte]
        limit = 2400
        return {
            'id': 'ast:' + digest((self.path + ':' + self.hash + ':' + str(node.start_byte)
                + ':' + str(node.end_byte) + ':' + node.type).encode())[:24],
            'file': self.path, 'source_hash': self.hash,
            'start_byte': node.start_byte, 'end_byte': node.end_byte,
            'line': node.start_point.row + 1, 'column': node.start_point.column + 1,
            'end_line': node.end_point.row + 1, 'end_column': node.end_point.column + 1,
            'column_unit': 'utf8_bytes', 'node_type': node.type,
            'lexical_owner': self.owner(node), 'span_hash': digest(raw),
            'quote': raw[:limit].decode('utf-8', 'ignore'),
            'quote_truncated': len(raw) > limit,
        }

    def shape(self, node, depth=4):
        if node is None:
            return None
        result = {'node_type': node.type, 'site_id': self.site(node)['id']}
        if depth < 0:
            result['shape_truncated'] = True
            result['text'] = (self.text(node) or '')[:140]
            return result
        if node.type in {'identifier', 'property_identifier', 'type_identifier', 'null',
                         'undefined', 'number', 'true', 'false'}:
            result['text'] = self.text(node)
        elif node.type in {'string', 'string_fragment'}:
            raw = self.text(node)
            result['raw'] = raw
            if node.type == 'string' and len(raw) >= 2 and raw[0] in {'"', "'"} and raw[-1] == raw[0] and '\\' not in raw:
                result['literal_value'] = raw[1:-1]
                result['literal_decode'] = 'unescaped_string'
            else:
                result['literal_decode'] = 'not_decoded_by_anchor_collector'
        elif node.type in {'call_expression', 'new_expression'}:
            callee = self.field(node, 'function') or self.field(node, 'constructor')
            result['callee'] = self.shape(callee, depth - 1)
            arguments = self.field(node, 'arguments')
            result['arguments'] = [self.shape(child, depth - 1) for child in
                (arguments.named_children if arguments is not None else []) if child.type != 'comment']
        elif node.type == 'variable_declarator':
            result['name'] = self.shape(self.field(node, 'name'), depth - 1)
            result['initializer'] = self.shape(self.field(node, 'value'), depth - 1)
        elif node.type == 'assignment_expression':
            result['left'] = self.shape(self.field(node, 'left'), depth - 1)
            result['right'] = self.shape(self.field(node, 'right'), depth - 1)
        elif node.type in {'member_expression', 'subscript_expression'}:
            result['object'] = self.shape(self.field(node, 'object'), depth - 1)
            result['property'] = self.shape(self.field(node, 'property') or self.field(node, 'index'), depth - 1)
        elif node.type in FUNCTIONS:
            result['name'] = self.function_name(node)
            result['defined_symbol'] = self.owner(node, True)
            parameters = self.field(node, 'parameters')
            result['parameters'] = [self.shape(child, depth - 1) for child in
                (parameters.named_children if parameters is not None else []) if child.type != 'comment']
            result['body_site'] = self.site(self.field(node, 'body')) if self.field(node, 'body') is not None else None
        elif node.type in {'required_parameter', 'optional_parameter'}:
            pattern = self.field(node, 'pattern') or self.field(node, 'name')
            result['binding_pattern'] = self.shape(pattern, depth - 1)
            result['signature'] = self.text(node)
        elif node.type == 'object':
            result['properties'] = [self.shape(child, depth - 1) for child in node.named_children if child.type != 'comment']
        elif node.type == 'pair':
            result['key'] = self.shape(self.field(node, 'key'), depth - 1)
            result['value'] = self.shape(self.field(node, 'value'), depth - 1)
        elif node.type == 'shorthand_property_identifier':
            result['key_and_value_identifier'] = self.text(node)
        elif node.type == 'if_statement':
            result['condition'] = self.shape(self.field(node, 'condition'), depth - 1)
            result['consequence'] = self.shape(self.field(node, 'consequence'), depth - 1)
            result['alternative'] = self.shape(self.field(node, 'alternative'), depth - 1)
        elif node.type in {'for_in_statement', 'for_statement'}:
            for name in ('kind', 'left', 'operator', 'right', 'initializer', 'condition', 'increment'):
                value = self.field(node, name)
                if value is not None:
                    result[name] = self.shape(value, depth - 1)
            result['body_site'] = self.site(self.field(node, 'body')) if self.field(node, 'body') is not None else None
        elif node.type in {'ternary_expression', 'binary_expression'}:
            for name in ('condition', 'consequence', 'alternative', 'left', 'operator', 'right'):
                value = self.field(node, name)
                if value is not None:
                    result[name] = self.shape(value, depth - 1)
        else:
            result['text'] = (self.text(node) or '')[:500]
            result['children'] = [self.shape(child, depth - 1) for child in node.named_children
                if child.type != 'comment']
        return result

    def ancestors(self, node):
        result = []
        current = node.parent
        while current is not None:
            if current.type in {'if_statement', 'ternary_expression', 'call_expression', 'return_statement'}:
                item = self.site(current)
                if current.type in {'if_statement', 'ternary_expression'}:
                    item['condition'] = self.text(self.field(current, 'condition'))
                    for role in ('consequence', 'alternative'):
                        branch = self.field(current, role)
                        if branch is not None and branch.start_byte <= node.start_byte and node.end_byte <= branch.end_byte:
                            item['selected_branch'] = role
                if current.type == 'call_expression':
                    item['callee'] = self.text(self.field(current, 'function'))
                    arguments = self.field(current, 'arguments')
                    item['containing_argument_indices'] = [index for index, argument in
                        enumerate(arguments.named_children if arguments is not None else [])
                        if argument.start_byte <= node.start_byte and node.end_byte <= argument.end_byte]
                result.append(item)
            current = current.parent
        return result

    def binding_audit(self, names):
        observed = {name: {'bindings': [], 'writes': []} for name in names}
        for node in walk(self.tree.root_node):
            pattern = None
            if node.type in {'variable_declarator', 'function_declaration', 'class_declaration'}:
                pattern = self.field(node, 'name')
            elif node.type in {'required_parameter', 'optional_parameter'}:
                pattern = self.field(node, 'pattern') or self.field(node, 'name')
            elif node.type == 'catch_clause':
                pattern = self.field(node, 'parameter')
            elif node.type in {'import_specifier', 'namespace_import', 'import_clause'}:
                if node.type == 'import_specifier':
                    pattern = self.field(node, 'alias') or self.field(node, 'name')
                else:
                    pattern = node
            if pattern is not None:
                for candidate in walk(pattern):
                    if candidate.type in {'identifier', 'shorthand_property_identifier_pattern'} and self.text(candidate) in observed:
                        observed[self.text(candidate)]['bindings'].append(self.site(candidate))
            if node.type in {'assignment_expression', 'augmented_assignment_expression', 'update_expression'}:
                left = self.field(node, 'left') or self.field(node, 'argument')
                raw = self.text(left) or ''
                for name in names:
                    if raw == name or raw.startswith(name + '.') or raw in {'globalThis.' + name, 'window.' + name}:
                        observed[name]['writes'].append(self.site(node))
        return {'scope': 'conservative_whole_file_runtime_binding_and_explicit_write_inventory',
            'observed': observed, 'runtime_global_identity': 'not_proved',
            'limitations': ['No target or dependency execution', 'Host/global monkeypatches are not excluded',
                'This inventory alone is not a production lexical binding resolver']}


documents = {}
anchors = []


def select(label, path, owner, node_type, field_equals=None, text_equals=None, all_matches=False):
    document = documents.setdefault(path, None)
    if document is None:
        document = Document(path)
        documents[path] = document
    candidates = []
    if not document.tree.root_node.has_error:
        for node in walk(document.tree.root_node):
            if node.type != node_type or (owner is not None and document.owner(node) != owner):
                continue
            if field_equals and any(document.text(document.field(node, key)) != value for key, value in field_equals.items()):
                continue
            if text_equals is not None and document.text(node) != text_equals:
                continue
            candidates.append(node)
    anchors.append({
        'id': label, 'selector': {'file': path, 'lexical_owner': owner, 'node_type': node_type,
            'field_equals': field_equals, 'text_equals': text_equals},
        'status': 'observed' if candidates and (all_matches or len(candidates) == 1) else 'unknown',
        'match_count': len(candidates), 'unique_required': not all_matches,
        'parse_has_error': bool(document.tree.root_node.has_error),
        'observations': [{'source': document.site(node), 'ast_shape': document.shape(node),
            'enclosing_syntax': document.ancestors(node)} for node in candidates],
        'semantic_scope': 'AST source observation only; not a target functional outcome',
    })


HOME = 'apps/client/src/home-dashboard-page.ts'
SCOPE = 'packages/browser-core/src/scope-context.ts'
APP = 'apps/client/src/application.ts'
CLIENT = 'apps/client/src/community-control-plane-client.ts'
ENTRY = 'apps/client/src/task-entry-view-model.ts'
CHAT = 'apps/client/src/chat-delivery-creator.ts'
MYWORK = 'apps/client/src/my-work-page.ts'
BOOT = 'apps/client/src/boot.ts'

select('producer.import-scope-builder', HOME, '<module>', 'import_statement',
    {'source': "'@winwincode/browser-core/scope-context'"})
select('producer.dashboard-href', HOME, 'mountHomeDashboardPage', 'assignment_expression', {'left': 'newTask.href'})
select('producer.link-insertion', HOME, 'mountHomeDashboardPage', 'call_expression', {'function': 'topActions.append'})
select('builder.scope-key-initializer', SCOPE, '<module>', 'variable_declarator', {'name': 'SCOPE_PARAMETER_NAMES'})
select('builder.surface-signature', SCOPE, '<module>', 'function_declaration', {'name': 'surfaceHash'})
select('builder.surface-return', SCOPE, 'surfaceHash', 'return_statement')
select('builder.scope-signature', SCOPE, '<module>', 'function_declaration', {'name': 'scopeHash'})
select('builder.query-index', SCOPE, 'scopeHash', 'variable_declarator', {'name': 'queryIndex'})
select('builder.base-path', SCOPE, 'scopeHash', 'variable_declarator', {'name': 'path'})
select('builder.query-receiver', SCOPE, 'scopeHash', 'variable_declarator', {'name': 'parameters'})
select('builder.finite-key-loop', SCOPE, 'scopeHash', 'for_in_statement', {'right': 'SCOPE_PARAMETER_NAMES'})
select('builder.scope-value', SCOPE, 'scopeHash', 'variable_declarator', {'name': 'value'})
select('builder.null-value-branch', SCOPE, 'scopeHash', 'if_statement', {'condition': '(value === null)'})
select('builder.receiver-delete', SCOPE, 'scopeHash', 'call_expression', {'function': 'parameters.delete'})
select('builder.receiver-set', SCOPE, 'scopeHash', 'call_expression', {'function': 'parameters.set'})
select('builder.receiver-serialize', SCOPE, 'scopeHash', 'variable_declarator', {'name': 'query'})
select('builder.output-return', SCOPE, 'scopeHash', 'return_statement')
select('builder.selection-from-hash', SCOPE, '<module>', 'function_declaration', {'name': 'scopeSelectionFromHash'})
select('composition.factory-import', APP, '<module>', 'import_statement', {'source': "'./community-control-plane-client.js'"})
select('composition.scope-import', APP, '<module>', 'import_statement', {'source': "'@winwincode/browser-core/scope-context'"})
select('composition.task-port-choice', APP, 'mountWinWinCodeClient', 'variable_declarator', {'name': 'taskPort'})
select('composition.browser-source', APP, 'mountWinWinCodeClient', 'variable_declarator', {'name': 'browser'})
select('consumer.injected-object-method', APP, 'mountWinWinCodeClient', 'method_definition', {'name': 'deliveryContext'})
select('consumer.auth-value', APP, 'mountWinWinCodeClient.deliveryContext', 'variable_declarator', {'name': 'context'})
select('consumer.query-read', APP, 'mountWinWinCodeClient.deliveryContext', 'variable_declarator', {'name': 'deliveryId'})
select('consumer.missing-key-null-guard', APP, 'mountWinWinCodeClient.deliveryContext', 'if_statement',
    {'condition': '(context === null || deliveryId === null)'})
select('consumer.other-null-guard', APP, 'mountWinWinCodeClient.deliveryContext', 'if_statement',
    {'condition': '(criterion === undefined)'})
select('consumer.callback-all-direct-returns', APP, 'mountWinWinCodeClient.deliveryContext', 'return_statement', all_matches=True)
select('consumer.route-parser-signature', APP, '<module>', 'function_declaration', {'name': 'routeParameters'})
select('consumer.route-parser-return', APP, 'routeParameters', 'return_statement')
select('consumer.factory-signature', CLIENT, '<module>', 'function_declaration', {'name': 'createControlPlaneTaskPort'})
select('consumer.factory-return-object', CLIENT, 'createControlPlaneTaskPort', 'return_statement')
select('consumer.returned-create-method', CLIENT, 'createControlPlaneTaskPort', 'method_definition', {'name': 'create'})
select('consumer.callback-invocation', CLIENT, 'createControlPlaneTaskPort.create', 'variable_declarator', {'name': 'context'})
select('consumer.null-throw-guard', CLIENT, 'createControlPlaneTaskPort.create', 'if_statement', {'condition': '(context === null)'})
select('consumer.first-actual-request', CLIENT, 'createControlPlaneTaskPort.create', 'variable_declarator', {'name': 'response'})
select('counterexample.fake-factory', CLIENT, '<module>', 'function_declaration', {'name': 'createControlPlaneTaskFake'})
select('counterexample.fake-return-object', CLIENT, 'createControlPlaneTaskFake', 'return_statement')
select('counterexample.fake-returned-create', CLIENT, 'createControlPlaneTaskFake', 'method_definition', {'name': 'create'})
select('counterexample.fake-direct-calls', CLIENT, 'createControlPlaneTaskFake.create', 'call_expression', all_matches=True)
select('composition.normal-boot-import', BOOT, '<module>', 'import_statement', {'source': "'./application.js'"})
select('composition.normal-boot-options', BOOT, '<module>', 'call_expression', {'function': 'mountWinWinCodeClient'})
select('composition.entry-model-port-injection', APP, 'mountWinWinCodeClient.renderTaskEntry', 'call_expression',
    {'function': 'createTaskEntryViewModel'})
select('consumer.form-port-call', ENTRY, None, 'call_expression', {'function': 'port.create'})
select('consumer.form-port-binding', ENTRY, 'createTaskEntryViewModel', 'variable_declarator', {'name': 'port'})
select('consumer.form-submit-method', ENTRY, 'createTaskEntryViewModel', 'method_definition', {'name': 'submit'})
select('consumer.form-submit-direct-guards', ENTRY, 'createTaskEntryViewModel.submit', 'if_statement', all_matches=True)
select('composition.home-scope-forwarding', APP, 'mountWinWinCodeClient.renderHome', 'call_expression', {'function': 'mountMyWorkPage'})
select('composition.dashboard-scope-forwarding', MYWORK, 'mountMyWorkPage', 'call_expression', {'function': 'mountHomeDashboardPage'})
select('composition.task-entry-route', APP, 'mountWinWinCodeClient.homeSubRoute', 'if_statement',
    {'condition': "(path === '/home/new-task')"})
select('composition.task-entry-dispatch', APP, 'mountWinWinCodeClient.performRender', 'if_statement',
    {'condition': "(homeRoute === 'task-entry')"})
select('counterexample.actual-delivery-query-seed', HOME, 'homeDecisionHash', 'call_expression', {'function': 'scopeHash'})
select('counterexample.run-route-query-copy', APP, None, 'if_statement',
    {'condition': "(deliveryId !== null)"}, text_equals="if (deliveryId !== null) parameters.set('delivery', deliveryId)")
select('counterexample.chat-creator-injection', APP, None, 'call_expression', {'function': 'createChatDeliveryCreator'})
select('counterexample.chat-create-function', CHAT, 'createChatDeliveryCreator', 'function_declaration', {'name': 'create'})
select('counterexample.chat-new-delivery-value', CHAT, 'createChatDeliveryCreator.create', 'variable_declarator', {'name': 'deliveryId'}, all_matches=True)
select('counterexample.chat-create-request-object', CHAT, 'createChatDeliveryCreator.create', 'assignment_expression', {'left': 'attempt'})
select('counterexample.chat-items-request', CHAT, 'createChatDeliveryCreator.create', 'call_expression', {'function': 'workItemsCreateCommand'})
select('counterexample.chat-run-request', CHAT, 'createChatDeliveryCreator.create', 'assignment_expression', {'left': 'currentAttempt.startRequest'})

baseline = TOOL_ROOT / 'reports/astra-baseline/capability-baseline.json'
package = TARGET_ROOT / 'packages/browser-core/package.json'
package_bytes = package.read_bytes()
package_value = json.loads(package_bytes)
output = {
    'schema_version': 1, 'artifact': 'navigation-independent-observed-anchors',
    'created_at': datetime.now(timezone.utc).isoformat(),
    'collector': {'file': str(Path(__file__).relative_to(TOOL_ROOT)), 'hash': digest(Path(__file__).read_bytes()),
        'purpose': 'independent AST source collection; not a detector, test, or expected outcome fixture',
        'target_imported': False, 'target_executed': False, 'target_tests_run': False,
        'target_build_run': False, 'browser_run': False},
    'target_root': str(TARGET_ROOT), 'snapshot_id': None,
    'identity_note': 'Original live source capture; not claimed to be an official immutable snapshot',
    'parser_version': parser_version('typescript'),
    'sources': {path: {'hash': document.hash, 'bytes': len(document.data),
        'final_parser_has_error': bool(document.tree.root_node.has_error),
        'projection': document.projection} for path, document in documents.items()},
    'package_metadata': {'file': 'packages/browser-core/package.json', 'hash': digest(package_bytes),
        'name': package_value.get('name'), 'exports': package_value.get('exports'),
        'source_binding_note': 'The manifest exports dist JS; TS workspace source correspondence is a separate source-resolution model'},
    'frozen_baseline': {'file': str(baseline.relative_to(TOOL_ROOT)), 'hash': digest(baseline.read_bytes()), 'modified_by_collector': False},
    'global_binding_inventories': {path: documents[path].binding_audit(['URLSearchParams', 'Object'])
        for path in (SCOPE, APP, CLIENT)},
    'anchors': anchors,
    'counts': {'total': len(anchors), 'observed': sum(item['status'] == 'observed' for item in anchors),
        'unknown': sum(item['status'] == 'unknown' for item in anchors)},
    'semantic_limits': ['Selectors identify reviewed syntax, not business correctness',
        'No prefilled helper keys, required key, abstract query outcome, null trace, or chain verdict',
        'Platform navigation and submission-time hash stability are not parameter-flow facts',
        'Observed source facts do not establish a consumer path was executed'],
}
REPORT_ROOT.mkdir(parents=True, exist_ok=True)
destination = REPORT_ROOT / 'navigation-observed-anchors.json'
destination.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'output': str(destination), 'counts': output['counts'],
    'source_files': len(documents), 'unknown_anchor_ids': [item['id'] for item in anchors if item['status'] == 'unknown']}, ensure_ascii=False))
