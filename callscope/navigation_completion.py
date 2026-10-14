"""Conditional navigation judgment assembled from captured source relations.

This adapter completes finite source obligations; it never observes a browser,
imports a target module, or upgrades a dynamic snapshot CALLS edge. Locators
choose source roles. Paths, returned discriminants, callback identities, DOM
composition, and rejection order are extracted from authenticated AST nodes.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from .models import Evidence, Finding, GraphSnapshot
from .semantic_sources import SemanticSources, VERSION as SOURCE_VERSION, unwrap, walk
from .lexical_bindings import LexicalBindings, VERSION as LEXICAL_VERSION
from .completion_summaries import function_kind, VERSION as COMPLETION_VERSION
from .static_contracts import _literal_string, _digest
from . import port_wiring as ports

VERSION = "conditional-navigation-obligations-1"
MODELS = frozenset({"dom-anchor-append-listener-1", "js-hash-path-strip-1",
                    "ordinary-source-method-invocation-1"})
_FUNCTIONS = ports._FUNCTIONS
_MAX_NODES = 40000
_MAX_FACTS = 256


def _children(node: Any) -> list[Any]:
    return ports._children(node)


def _field(node: Any, name: str) -> Any:
    return ports._field(node, name)


def _path(document: Any, original: Any) -> list[str] | None:
    node = unwrap(original)
    if node is None:
        return None
    if node.type in {"identifier", "shorthand_property_identifier"}:
        name = ports._name(document, node)
        return [name] if name else None
    receiver, key = ports._member(document, node)
    prefix = _path(document, receiver) if receiver is not None else None
    return [*prefix, key] if prefix and key else None


def _same_location(first: dict, second: dict) -> bool:
    keys = ("file", "source_hash", "start_byte", "end_byte", "span_hash", "semantic_parse_id")
    return all(key in first and first[key] == second.get(key) for key in keys)


def _node_at(document: Any, location: dict, types: set[str] | None = None) -> Any:
    candidates = [node for node in walk(document.tree.root_node)
                  if node.start_byte == location.get("start_byte")
                  and node.end_byte == location.get("end_byte")
                  and (types is None or node.type in types)]
    matches = [node for node in candidates if _same_location(document.location(node), location)]
    return matches[0] if len(matches) == 1 else None


def validate_completion(rule: dict) -> None:
    value = rule.get("completion")
    allowed = {"route_selector", "route_dispatcher", "page", "page_callee",
               "producer_composition", "producer_host", "producer_host_callee",
               "chat_counterexample",
               "http_boundary_path", "required_query_keys", "models"}
    if not isinstance(value, dict) or set(value) != allowed:
        raise ValueError("completion requires source role locators, required keys and finite models only")
    for role in ("route_selector", "route_dispatcher", "page", "producer_composition", "producer_host", "chat_counterexample"):
        selector = value[role]
        if (not isinstance(selector, dict) or set(selector) != {"file", "symbol"}
                or not ports._path(selector.get("file")) or not ports._text(selector.get("symbol"))):
            raise ValueError("completion source roles require exact file/symbol")
    if not ports._text(value["page_callee"]) or not ports._text(value["producer_host_callee"]):
        raise ValueError("completion page_callee must be a source expression locator")
    for key in ("http_boundary_path", "required_query_keys"):
        if (not isinstance(value[key], list) or not value[key]
                or any(not ports._text(item) for item in value[key])):
            raise ValueError("completion paths/required keys must be nonempty string lists")
    if set(value["models"]) != MODELS or len(value["models"]) != len(MODELS):
        raise ValueError("completion needs all versioned DOM/path/invocation models")


def validate_navigation_completion_rule(rule: dict) -> None:
    from .navigation_analysis import validate_navigation_rule
    validate_navigation_rule({key: value for key, value in rule.items() if key != "completion"})
    validate_completion(rule)


class _Context:
    def __init__(self, snapshot: GraphSnapshot, rule: dict, details: dict):
        self.snapshot, self.rule, self.details = snapshot, rule, details
        self.sources = SemanticSources(snapshot)
        self.bindings: dict[str, LexicalBindings] = {}
        self.facts: list[dict] = []
        self.gaps: list[dict] = []
        self.model_applications: list[dict] = []
        self.node_count = 0
        self.port_context = ports._Context(snapshot, rule)
        self.port_context.sources = self.sources

    def lexical(self, document: Any) -> LexicalBindings:
        if document.source.path not in self.bindings:
            self.bindings[document.source.path] = LexicalBindings(document)
        return self.bindings[document.source.path]

    def direct(self, node: Any) -> list[Any]:
        result = []
        for item in walk(node, skip_functions=True):
            self.node_count += 1
            if self.node_count > _MAX_NODES:
                self.gap("analysis", "completion_source_budget", "AST enumeration exceeded complete budget")
                return []
            result.append(item)
        return result

    def gap(self, obligation: str, code: str, message: str, document: Any = None,
            node: Any = None, **extra: Any) -> str:
        item = {"obligation": obligation, "code": code, "message": message,
                "location": document.location(node) if document is not None and node is not None else None,
                **extra}
        item["id"] = "navigation-gap:" + _digest(item)[:24]
        if item not in self.gaps:
            self.gaps.append(item)
        return item["id"]

    def fact(self, obligation: str, operation: str, document: Any, nodes: list[Any],
             observed: dict, inputs: list[str] | None = None, source: str = "source-derived") -> str:
        if len(self.facts) >= _MAX_FACTS:
            return self.gap(obligation, "completion_fact_budget", "Fact budget exceeded")
        item = {"obligation": obligation, "operation": operation, "source_category": source,
                "snapshot_id": self.snapshot.id, "source_hash": self.snapshot.source_hash,
                "locations": [document.location(node) for node in nodes if node is not None],
                "inputs": list(inputs or []), "observed": deepcopy(observed),
                "version": VERSION, "semantic_source_version": SOURCE_VERSION,
                "runtime_verified": False}
        item["id"] = "navigation-fact:" + _digest(item)[:24]
        self.facts.append(item)
        return item["id"]

    def model(self, model: str, facts: list[str], observed: dict) -> str:
        item = {"model": model, "input_fact_ids": facts, "observed": deepcopy(observed),
                "source_category": "trusted-model", "runtime_environment_verified": False}
        item["id"] = "navigation-model:" + _digest(item)[:24]
        self.model_applications.append(item)
        return item["id"]

    def select(self, obligation: str, selector: dict) -> tuple[Any, Any]:
        document, definition, problems = self.sources.select(selector)
        if problems:
            self.gap(obligation, "source_role_unavailable", "Selected source role is incomplete", problems=problems)
            return document, None
        if definition is None or not definition.callable:
            self.gap(obligation, "source_role_not_callable", "Source role is not a unique callable")
            return document, None
        nodes = self.sources.nodes.get(definition.graph_node_id, [])
        if len(nodes) != 1:
            self.gap(obligation, "source_role_graph_unknown", "Callable graph identity is not unique")
            return document, None
        actual_document, actual, problems = self.sources.definition_for_node(nodes[0])
        if actual_document is not document or actual is not definition or problems:
            self.gap(obligation, "source_role_authentication_unknown", "Source role graph/source identities differ", problems=problems)
            return document, None
        return document, definition

    def record(self, obligation: str, document: Any, identifier: Any, allow_writes: bool = False) -> dict | None:
        if identifier is None or identifier.type not in {"identifier", "shorthand_property_identifier",
                                                          "shorthand_property_identifier_pattern"}:
            self.gap(obligation, "simple_binding_required", "Expected a simple lexical binding", document, identifier)
            return None
        record = self.lexical(document).resolve(identifier)
        if record.get("state") != "unique" or not record.get("identity_complete"):
            self.gap(obligation, "binding_identity_incomplete", "Unique lexical binding required", document, identifier)
            return None
        writes = self.lexical(document).writes(record)
        binding_writes = [write for write in writes if write.get("binding_reassignment")
                          or not write.get("mutation_target_complete", False)]
        if not allow_writes and binding_writes:
            self.gap(obligation, "binding_written", "Selected captured declaration is reassigned or has unresolved mutation identity",
                     document, identifier, writes=binding_writes)
            return None
        return record

    def same(self, document: Any, left: dict | None, right: dict | None) -> bool:
        return bool(left and right and self.lexical(document).same(left, right))

    def actual_target(self, obligation: str, document: Any, call: Any, owner: Any,
                      expected_document: Any = None, expected: Any = None) -> tuple[Any, Any, dict | None]:
        edge, problems = self.sources.call_binding(call, document, owner)
        if edge is not None:
            targets = self.sources.nodes.get(edge.target, [])
            target_document, target, target_problems = self.sources.definition_for_node(targets[0]) if len(targets) == 1 else (None, None, [])
            if target is not None and not target_problems and (expected is None or target is expected):
                identity = {"kind": "snapshot_calls", "edge_id": edge.id,
                            "source_graph_node_id": edge.source, "target_graph_node_id": edge.target}
                return target_document, target, identity
        if expected is not None and expected_document is not None:
            boundary = ports._dynamic_import_boundary(self.port_context, document, call, owner)
            if boundary is not None:
                target, identity = ports._literal_import_target(self.port_context, obligation, document, call,
                    expected_document, expected, owner)
                if target is expected:
                    return expected_document, target, identity
        self.gap(obligation, "actual_call_binding_unknown", "Source call has no authenticated actual target", document, call,
                 original_problems=problems, assembly_gaps=deepcopy(self.port_context.gaps))
        return None, None, None


def _statement_body(node: Any) -> Any:
    return _field(ports._function(node), "body")


def _return_expression(node: Any) -> Any:
    children = _children(node)
    return children[0] if len(children) == 1 else None


def _direct_statement(node: Any, body: Any) -> Any:
    current = node
    while current is not None and current.parent != body:
        if current.parent is None or current.parent.type in _FUNCTIONS or current.parent.type in {
                "if_statement", "for_statement", "for_in_statement", "while_statement", "do_statement",
                "switch_statement", "switch_case", "try_statement", "catch_clause"}:
            return None
        current = current.parent
    return current if current is not None and current.parent == body else None


def _dom_path_gate(ctx: _Context, obligation: str, document: Any, owner: Any,
                   chain: list[Any], chain_ids: set[str]) -> bool:
    body = _statement_body(owner)
    if any((_direct_statement(node, body) is None or _direct_statement(node, body).type != "expression_statement") for node in chain):
        ctx.gap(obligation, "dom_append_control_flow_unknown", "Selected DOM composition calls are not direct normal-body statements")
        return False
    if any(first.start_byte >= second.start_byte for first, second in zip(chain, chain[1:])):
        ctx.gap(obligation, "dom_append_order_unknown", "Selected finite DOM construction does not have ordered inner-to-root appends")
        return False
    for node in ctx.direct(body):
        if node.type not in {"call_expression", "assignment_expression"}:
            continue
        target = _field(node, "function") if node.type == "call_expression" else _field(node, "left")
        path = _path(document, target)
        root = unwrap(target)
        while root is not None and root.type in {"member_expression", "subscript_expression"}:
            root = unwrap(_field(root, "object"))
        candidate = ctx.lexical(document).resolve(root) if root is not None and root.type == "identifier" else {}
        if candidate.get("declaration_id") not in chain_ids:
            continue
        member = path[-1] if path and len(path) > 1 else None
        if node.type == "assignment_expression" and member in {"innerHTML", "outerHTML", "textContent", "hidden"} and node.start_byte > chain[0].start_byte:
            ctx.gap(obligation, "dom_chain_later_destructive_write", "Captured write may remove/hide selected DOM subtree", document, node)
            return False
        if node.type == "call_expression" and member in {"remove", "removeChild", "replaceChild", "replaceChildren"} and node not in chain:
            ctx.gap(obligation, "dom_chain_other_destructive_call", "Captured destructive DOM operation is outside selected finite composition", document, node)
            return False
    return True


def _ast_source_visible(ctx: _Context) -> dict:
    producer = ctx.details.get("producer", {})
    document, owner = ctx.select("N1", ctx.rule["producer"])
    if owner is None:
        return {"supported": False}
    site = _node_at(document, producer.get("site_location", {}), {"assignment_expression"})
    target = unwrap(_field(site, "left"))
    receiver, key = ports._member(document, target)
    anchor_record = ctx.record("N1", document, receiver)
    if anchor_record is not None and not _dom_helper_kind(ctx, "N1", document, owner, anchor_record, "a").get("supported"):
        return {"supported": False}
    declaration = ctx.lexical(document).declaration_for(anchor_record) if anchor_record else None
    initializer = unwrap(_field(declaration, "value"))
    if key != "href" or initializer is None or initializer.type != "call_expression":
        ctx.gap("N1", "anchor_construction_unknown", "href receiver is not a direct const DOM element construction", document, site)
        return {"supported": False}
    helper_document, helper, binding = ctx.actual_target("N1", document, initializer, owner)
    if helper is None:
        return {"supported": False}
    params = _children(_field(ports._function(helper), "parameters"))
    args = ports._arguments(initializer)
    body_nodes = ctx.direct(_statement_body(helper))
    create_calls = [node for node in body_nodes if node.type == "call_expression"
                    and ports._member(helper_document, _field(node, "function"))[1] == "createElement"]
    anchor_tag = None
    if len(create_calls) == 1:
        create_args = ports._arguments(create_calls[0])
        if create_args and unwrap(create_args[0]).type == "identifier":
            tag_record = ctx.record("N1", helper_document, unwrap(create_args[0]))
            for index, parameter in enumerate(params):
                binder = _field(parameter, "pattern") or _field(parameter, "name") or parameter
                if ctx.same(helper_document, tag_record, ctx.record("N1", helper_document, binder)) and len(args) > index:
                    anchor_tag = _literal_string(document.text(args[index]))
    if anchor_tag != "a":
        ctx.gap("N1", "anchor_dom_kind_unproved", "Actual helper/parameter/argument mapping did not produce an anchor", document, initializer)
        return {"supported": False}
    returns = [node for node in body_nodes if node.type == "return_statement"]
    created = create_calls[0].parent if create_calls else None
    while created is not None and created.type != "variable_declarator":
        created = created.parent
    returned_binding = ctx.record("N1", helper_document, unwrap(_return_expression(returns[0]))) if len(returns) == 1 else None
    constructed_binding = ctx.record("N1", helper_document, _field(created, "name")) if created is not None else None
    helper_statements = _children(_statement_body(helper))
    if (not ctx.same(helper_document, returned_binding, constructed_binding)
            or function_kind(helper_document, ports._function(helper)).get("kind") != "ordinary_sync"
            or not returns or returns[0].parent != _statement_body(helper)
            or not helper_statements or helper_statements[-1] != returns[0]):
        ctx.gap("N1", "anchor_helper_return_unproved", "DOM helper does not return the actual created node binding", helper_document, ports._function(helper))
        return {"supported": False}
    nodes = ctx.direct(_statement_body(owner))
    graph: dict[str, list[tuple[str, Any]]] = {}
    roots: list[tuple[str, Any]] = []
    hidden: set[str] = set()
    unknown_composition = []
    owner_parameters = _children(_field(ports._function(owner), "parameters"))
    option_parameter = owner_parameters[0] if len(owner_parameters) == 1 else None
    option_identifier = _field(option_parameter, "pattern") or _field(option_parameter, "name") or option_parameter
    option_record = ctx.record("N1", document, option_identifier)
    def binding_for(node: Any) -> dict | None:
        if node is None or node.type != "identifier":
            return None
        record = ctx.lexical(document).resolve(node)
        return record if record.get("state") == "unique" and record.get("identity_complete") else None
    def identity(record: dict | None) -> str:
        return record.get("declaration_id", record.get("binding_id", "")) if record else ""
    for node in nodes:
        if node.type == "assignment_expression":
            root, member = ports._member(document, _field(node, "left"))
            record = binding_for(root)
            if member == "hidden" and record:
                # Any explicit write is excluded from the visible path. This is
                # conservative even if a false assignment could restore it.
                hidden.add(identity(record))
        if node.type != "call_expression":
            continue
        parent, method = ports._member(document, _field(node, "function"))
        if method not in {"append", "replaceChildren"}:
            continue
        arguments = ports._arguments(node)
        if any(arg.type == "spread_element" for arg in arguments):
            unknown_composition.append(document.location(node))
            continue
        parent_record = binding_for(parent)
        parent_id = identity(parent_record)
        parent_path = _path(document, parent)
        for argument in arguments:
            record = binding_for(unwrap(argument))
            child_id = identity(record)
            if not child_id:
                continue
            if parent_id:
                graph.setdefault(child_id, []).append((parent_id, node))
            elif parent_path and len(parent_path) == 2 and parent_path[-1] == "root":
                root_receiver, _ = ports._member(document, parent)
                if ctx.same(document, option_record, binding_for(root_receiver)):
                    roots.append((child_id, node))
    anchor_id = identity(anchor_record)
    pending, visited, selected = [(anchor_id, [])], set(), None
    while pending:
        current, chain = pending.pop(0)
        if current in visited or current in hidden:
            continue
        visited.add(current)
        for root_id, call in roots:
            if root_id == current:
                selected = [*chain, call]
                break
        if selected:
            break
        pending.extend((parent, [*chain, call]) for parent, call in graph.get(current, []))
    if not selected:
        ctx.gap("N1", "anchor_public_dom_chain_unknown", "Anchor has no explicit nonhidden append chain to page root", document, site,
                hidden_binding_ids=sorted(hidden), unknown_composition=unknown_composition)
        return {"supported": False}
    chain_ids = {anchor_id}
    for node in selected:
        parent, _ = ports._member(document, _field(node, "function"))
        parent_record = binding_for(parent)
        if parent_record:
            chain_ids.add(identity(parent_record))
    if not _dom_path_gate(ctx, "N1", document, owner, selected, chain_ids):
        return {"supported": False}
    expression = unwrap(_field(site, "right"))
    expression_args = ports._arguments(expression) if expression is not None and expression.type == "call_expression" else []
    seed = _literal_string(document.text(expression_args[0])) if expression_args else None
    if seed is None or not seed.startswith("/") or "?" in seed or "#" in seed:
        ctx.gap("N1", "seed_path_not_closed", "Selected public href has no query-free literal path argument", document, expression)
        return {"supported": False}
    fact = ctx.fact("N1", "visible_anchor_helper_return_and_append_chain", document,
        [site, declaration, *selected], {"anchor_binding_id": anchor_id, "seed_path": seed,
        "element_helper_binding": binding, "helper_source": helper_document.location(ports._function(helper)),
        "helper_create_location": helper_document.location(create_calls[0]),
        "helper_return_location": helper_document.location(returns[0]),
        "explicit_hidden_writes_on_selected_chain": False,
        "visibility_scope": "explicit DOM construction/composition; CSS and runtime visibility not observed"})
    ctx.model("dom-anchor-append-listener-1", [fact], {"operation": "ordinary_anchor_and_append_composition"})
    installation = _producer_installation(ctx, document, owner)
    return {"supported": bool(installation.get("supported")), "fact_ids": [fact, *installation.get("fact_ids", [])],
            "seed_path": seed, "production_installation": installation}


def _dom_install_path(ctx: _Context, document: Any, owner: Any, record: dict,
                      parameter_record: dict, obligation: str = "N1") -> tuple[list[Any] | None, list[dict]]:
    """A finite direct owner append graph, preserving actual root identities."""
    graph: dict[str, list[tuple[str, Any]]] = {}
    roots, hidden = [], set()
    def identity(candidate: dict | None) -> str:
        return candidate.get("declaration_id", "") if candidate else ""
    def binding(node: Any) -> dict | None:
        node = unwrap(node)
        if node is None or node.type != "identifier":
            return None
        candidate = ctx.lexical(document).resolve(node)
        return candidate if candidate.get("state") == "unique" and candidate.get("identity_complete") else None
    for node in ctx.direct(_statement_body(owner)):
        if node.type == "assignment_expression":
            receiver, member = ports._member(document, _field(node, "left"))
            if member == "hidden" and unwrap(_field(node, "right")).type != "false":
                hidden.add(identity(binding(receiver)))
        if node.type != "call_expression":
            continue
        parent, member = ports._member(document, _field(node, "function"))
        if member not in {"append", "replaceChildren"}:
            continue
        arguments = ports._arguments(node)
        if any(argument.type == "spread_element" for argument in arguments):
            continue
        parent_record = binding(parent)
        root_receiver, root_property = ports._member(document, parent)
        root_is_formal = root_property == "root" and ctx.same(document, parameter_record, binding(root_receiver))
        for argument in arguments:
            child = identity(binding(argument))
            if not child:
                continue
            if parent_record:
                graph.setdefault(child, []).append((identity(parent_record), node))
            elif root_is_formal:
                roots.append((child, node))
    pending, visited = [(identity(record), [])], set()
    while pending:
        current, chain = pending.pop(0)
        if current in visited or current in hidden:
            continue
        visited.add(current)
        for root, node in roots:
            if root == current:
                selected = [*chain, node]
                chain_ids = {identity(record)}
                for call in selected:
                    receiver, _ = ports._member(document, _field(call, "function"))
                    parent = binding(receiver)
                    if parent:
                        chain_ids.add(identity(parent))
                if _dom_path_gate(ctx, obligation, document, owner, selected, chain_ids):
                    return selected, [{"binding_id": value} for value in sorted(hidden)]
                return None, [{"binding_id": value} for value in sorted(hidden)]
        pending.extend((parent, [*chain, node]) for parent, node in graph.get(current, []))
    return None, [{"binding_id": value} for value in sorted(hidden)]


def _dom_helper_kind(ctx: _Context, obligation: str, document: Any, owner: Any,
                     record: dict, expected_tag: str) -> dict:
    declaration = ctx.lexical(document).declaration_for(record)
    call = unwrap(_field(declaration, "value"))
    if declaration is None or not ports._const(declaration) or call is None or call.type != "call_expression":
        ctx.gap(obligation, "dom_helper_capture_unknown", "DOM receiver is not a const actual helper result")
        return {"supported": False}
    helper_document, helper, binding = ctx.actual_target(obligation, document, call, owner)
    if helper is None:
        return {"supported": False}
    function = ports._function(helper)
    body = _field(function, "body")
    statements = _children(body)
    if (function_kind(helper_document, function).get("kind") != "ordinary_sync" or len(statements) != 3
            or statements[0].type != "lexical_declaration" or statements[1].type != "expression_statement"
            or statements[2].type != "return_statement"):
        ctx.gap(obligation, "dom_helper_body_not_finite", "DOM helper is not ordinary sync create, attribute assignment, direct return")
        return {"supported": False}
    declarations = [node for node in _children(statements[0]) if node.type == "variable_declarator"]
    if len(declarations) != 1:
        ctx.gap(obligation, "dom_helper_creation_statement_unknown", "DOM helper creation statement is not unique")
        return {"supported": False}
    creation = unwrap(_field(declarations[0], "value"))
    create_receiver, create_method = ports._member(helper_document, _field(creation, "function"))
    create_arguments = ports._arguments(creation) if creation is not None and creation.type == "call_expression" else []
    params = _children(_field(function, "parameters"))
    helper_param_ids = []
    for parameter in params:
        binder = _field(parameter, "pattern") or _field(parameter, "name") or parameter
        if binder.type != "identifier" or _field(parameter, "value") is not None or parameter.type == "optional_parameter":
            ctx.gap(obligation, "dom_helper_parameter_unknown", "DOM helper has unsupported default/rest/parameter effects")
            return {"supported": False}
        helper_param_ids.append(ctx.record(obligation, helper_document, binder))
    actual_arguments = ports._arguments(call)
    if (create_method != "createElement" or len(create_arguments) != 1 or len(actual_arguments) != len(params)
            or create_receiver is None or create_receiver.type != "identifier"):
        ctx.gap(obligation, "dom_helper_create_mapping_unknown", "DOM helper createElement argument/receiver shape is not closed")
        return {"supported": False}
    receiver_record = ctx.record(obligation, helper_document, create_receiver)
    tag_record = ctx.record(obligation, helper_document, unwrap(create_arguments[0]))
    receiver_indices = [index for index, parameter in enumerate(helper_param_ids) if ctx.same(helper_document, receiver_record, parameter)]
    tag_indices = [index for index, parameter in enumerate(helper_param_ids) if ctx.same(helper_document, tag_record, parameter)]
    if len(receiver_indices) != 1 or len(tag_indices) != 1 or _literal_string(document.text(actual_arguments[tag_indices[0]])) != expected_tag:
        ctx.gap(obligation, "dom_helper_expected_tag_unproved", "Actual tag argument/formal mapping does not produce the required DOM node")
        return {"supported": False}
    created_record = ctx.record(obligation, helper_document, _field(declarations[0], "name"))
    returned_record = ctx.record(obligation, helper_document, unwrap(_return_expression(statements[2])))
    attribute = unwrap(_return_expression(statements[1]))
    attribute_receiver, attribute_name = ports._member(helper_document, _field(attribute, "left"))
    attribute_value = unwrap(_field(attribute, "right"))
    attribute_record = ctx.record(obligation, helper_document, attribute_receiver)
    if (not ctx.same(helper_document, created_record, returned_record) or not ctx.same(helper_document, created_record, attribute_record)
            or attribute is None or attribute.type != "assignment_expression" or attribute_name != "className"
            or attribute_value is None or attribute_value.type != "identifier"
            or not any(ctx.same(helper_document, ctx.record(obligation, helper_document, attribute_value), parameter) for parameter in helper_param_ids)):
        ctx.gap(obligation, "dom_helper_return_or_attribute_unknown", "DOM helper does not return its created node after a modeled own className assignment")
        return {"supported": False}
    fact = ctx.fact(obligation, "actual_dom_helper_tag_parameter_and_return", document,
        [declaration, call], {"expected_tag": expected_tag, "actual_helper_binding": binding,
        "create_location": helper_document.location(creation), "return_location": helper_document.location(statements[2]),
        "ordinary_sync_finite_body": True, "created_receiver_identity": created_record.get("declaration_id"),
        "document_actual_argument": document.location(actual_arguments[receiver_indices[0]])})
    return {"supported": True, "fact_ids": [fact]}


def _producer_installation(ctx: _Context, producer_document: Any, producer_owner: Any) -> dict:
    config = ctx.rule["completion"]
    document, owner = ctx.select("N1", config["producer_composition"])
    host_document, host = ctx.select("N1", config["producer_host"])
    application_document, application = ctx.select("N1", ctx.rule["consumer"])
    if any(value is None for value in (owner, host, application)):
        return {"supported": False}
    calls = [call for call in ports._calls(document, owner, producer_owner.symbol.rsplit(".", 1)[-1])]
    if len(calls) != 1:
        ctx.gap("N1", "producer_composition_call_unknown", "Actual producer page is not uniquely called in its composition owner")
        return {"supported": False}
    call = calls[0]
    actual_document, actual, binding = ctx.actual_target("N1", document, call, owner)
    if actual is not producer_owner or actual_document is not producer_document:
        ctx.gap("N1", "producer_composition_target_mismatch", "Composition call does not bind the selected producer declaration")
        return {"supported": False}
    args = ports._arguments(call)
    members = ports._properties(ctx.port_context, "N1", document, args[0], data_only=True) if len(args) == 1 else None
    root = unwrap(members["root"]["value"]) if members and "root" in members else None
    root_record = ctx.record("N1", document, root) if root is not None else None
    parameter, parameter_record = ports._parameter(ctx.port_context, "N1", document, owner, 0)
    if root_record is None or parameter_record is None:
        ctx.gap("N1", "producer_composition_root_unknown", "Actual nested root field/formal binding is not closed")
        return {"supported": False}
    chain, hidden = _dom_install_path(ctx, document, owner, root_record, parameter_record)
    if not chain:
        ctx.gap("N1", "producer_composition_not_public", "Actual nested producer root has no nonhidden append path to composition root", document, call,
                hidden_bindings=hidden)
        return {"supported": False}
    host_calls = ports._calls(host_document, host, config["producer_host_callee"])
    if len(host_calls) != 1:
        ctx.gap("N1", "producer_host_call_unknown", "Actual production host page call is not unique")
        return {"supported": False}
    host_call = host_calls[0]
    actual_document, actual, host_binding = ctx.actual_target("N1", host_document, host_call, host, document, owner)
    if actual is not owner or actual_document is not document:
        return {"supported": False}
    host_args = ports._arguments(host_call)
    host_members = ports._properties(ctx.port_context, "N1", host_document, host_args[0], data_only=True) if len(host_args) == 1 else None
    host_root = unwrap(host_members["root"]["value"]) if host_members and "root" in host_members else None
    host_root_record = ctx.record("N1", host_document, host_root) if host_root is not None else None
    application_parameter, application_record = ports._parameter(ctx.port_context, "N1", application_document, application, 0)
    if host_document is not application_document or host_root_record is None or application_record is None:
        ctx.gap("N1", "producer_host_root_capture_unknown", "Production host root is not an actual captured application root binding")
        return {"supported": False}
    shell_chain, shell_hidden = _dom_install_path(ctx, application_document, application, host_root_record, application_record)
    if not shell_chain:
        ctx.gap("N1", "producer_host_shell_root_unproved", "Actual host page root is not composed into the boot application's public root",
                hidden_bindings=shell_hidden)
        return {"supported": False}
    fact = ctx.fact("N1", "nested_producer_root_to_composition_and_actual_production_host", document,
        [call, root, *chain], {"producer_call_binding": binding,
        "composition_formal_root": document.location(parameter),
        "production_host_call": host_document.location(host_call), "production_host_binding": host_binding,
        "production_host_actual_root": host_document.location(host_root),
        "public_application_append_chain": [application_document.location(node) for node in shell_chain],
        "application_formal_root": application_document.location(application_parameter),
        "normal_host_mount_condition": "renderHome mounts normally, authentication/loading/lifecycle guards permit it, and no failure display is active",
        "hidden_siblings_excluded": hidden, "runtime_pixels_observed": False})
    ctx.model("dom-anchor-append-listener-1", [fact], {"operation": "actual_nested_roots_and_public_append_composition"})
    return {"supported": True, "fact_ids": [fact], "actual_host_binding": host_binding}


def _strip_hash_expression(ctx: _Context, document: Any, original: Any) -> tuple[list[str] | None, list[Any]]:
    node = unwrap(original)
    operations = []
    for expected in (r"/\?.*$/u", "/^#/u"):
        if node is None or node.type != "call_expression":
            return None, []
        receiver, member = ports._member(document, _field(node, "function"))
        args = ports._arguments(node)
        if member != "replace" or len(args) != 2 or document.text(args[0]) != expected or _literal_string(document.text(args[1])) != "":
            return None, []
        operations.append(node)
        node = unwrap(receiver)
    return _path(document, node), operations


def _route_dispatch(ctx: _Context, seed: str) -> dict:
    config = ctx.rule["completion"]
    selector_document, selector = ctx.select("N6", config["route_selector"])
    dispatcher_document, dispatcher = ctx.select("N6", config["route_dispatcher"])
    injection_document, injection = ctx.select("N6", ctx.rule["wiring"]["injection"])
    if any(owner is None for owner in (selector, dispatcher, injection)):
        return {"supported": False}
    selector_nodes = ctx.direct(_statement_body(selector))
    declarations = [node for node in selector_nodes if node.type == "variable_declarator"]
    path_declarations = []
    for declaration in declarations:
        origin, operations = _strip_hash_expression(ctx, selector_document, _field(declaration, "value"))
        if origin == ctx.rule["ambient"]["read_path"]:
            path_declarations.append((declaration, operations))
    if len(path_declarations) != 1:
        ctx.gap("N6", "route_path_projection_unknown", "Subroute selector lacks a unique finite ambient hash stripping projection")
        return {"supported": False}
    path_declaration, strip_nodes = path_declarations[0]
    path_record = ctx.record("N6", selector_document, _field(path_declaration, "name"))
    returned_route, branch_node = None, None
    for statement in _children(_statement_body(selector)):
        if statement.type != "if_statement":
            continue
        condition = unwrap(_field(statement, "condition"))
        if condition is None or condition.type != "binary_expression" or selector_document.text(_field(condition, "operator")) != "===":
            continue
        left, right = unwrap(_field(condition, "left")), unwrap(_field(condition, "right"))
        literal = _literal_string(selector_document.text(right))
        if left is not None and left.type == "string":
            left, right = right, left
            literal = _literal_string(selector_document.text(right))
        if literal != seed or left is None or left.type != "identifier":
            continue
        if not ctx.same(selector_document, path_record, ctx.record("N6", selector_document, left)):
            continue
        consequence = _field(statement, "consequence")
        items = _children(consequence) if consequence is not None and consequence.type == "statement_block" else [consequence]
        if len(items) == 1 and items[0] is not None and items[0].type == "return_statement":
            returned_route = _literal_string(selector_document.text(_return_expression(items[0])))
            branch_node = statement
            break
    if returned_route is None:
        ctx.gap("N6", "seed_subroute_result_unknown", "Seed path is not mapped by an actual supported return guard")
        return {"supported": False}
    selector_before = [node for node in _children(_statement_body(selector)) if node.end_byte <= branch_node.start_byte]
    if (selector_before != [path_declaration.parent]
            or path_declaration.parent.parent != _statement_body(selector)
            or len([node for node in _children(path_declaration.parent) if node.type == "variable_declarator"]) != 1):
        ctx.gap("N6", "subroute_guard_prefix_not_complete", "Subroute guard has earlier control/return/initializer effects outside sole path projection")
        return {"supported": False}
    nodes = ctx.direct(_statement_body(dispatcher))
    selector_calls = []
    injection_calls = []
    for call in (node for node in nodes if node.type == "call_expression"):
        function = unwrap(_field(call, "function"))
        if function is None or function.type != "identifier":
            continue
        if dispatcher_document.text(function) == selector.symbol.rsplit(".", 1)[-1]:
            actual_document, actual, binding = ctx.actual_target("N6", dispatcher_document, call, dispatcher)
            if actual is selector and actual_document is selector_document:
                selector_calls.append((call, binding))
        if dispatcher_document.text(function) == injection.symbol.rsplit(".", 1)[-1]:
            actual_document, actual, binding = ctx.actual_target("N6", dispatcher_document, call, dispatcher)
            if actual is injection and actual_document is injection_document:
                injection_calls.append((call, binding))
    if len(selector_calls) != 1 or len(injection_calls) != 1:
        ctx.gap("N6", "route_dispatch_target_unknown", "Dispatcher lacks unique actual selector/injection calls")
        return {"supported": False}
    selector_call, selector_binding = selector_calls[0]
    declaration = selector_call.parent
    if declaration is None or declaration.type != "variable_declarator" or not ports._const(declaration):
        ctx.gap("N6", "subroute_local_result_unknown", "Actual subroute result is not captured by a direct const")
        return {"supported": False}
    route_record = ctx.record("N6", dispatcher_document, _field(declaration, "name"))
    injection_call, injection_binding = injection_calls[0]
    parent = injection_call.parent
    guarded, guard = False, None
    while parent is not None and parent != _statement_body(dispatcher):
        if parent.type == "if_statement":
            condition = unwrap(_field(parent, "condition"))
            consequence = _field(parent, "consequence")
            if (condition is not None and condition.type == "binary_expression"
                    and dispatcher_document.text(_field(condition, "operator")) == "==="
                    and consequence is not None and consequence.start_byte <= injection_call.start_byte < consequence.end_byte):
                left, right = unwrap(_field(condition, "left")), unwrap(_field(condition, "right"))
                if (left is not None and left.type == "identifier"
                        and _literal_string(dispatcher_document.text(right)) == returned_route
                        and ctx.same(dispatcher_document, route_record, ctx.record("N6", dispatcher_document, left))):
                    guarded, guard = True, parent
        parent = parent.parent
    if not guarded:
        ctx.gap("N6", "subroute_dispatch_guard_unknown", "Actual injection call is not in matching returned-discriminant guard")
        return {"supported": False}
    surface = _surface_dispatch(ctx, dispatcher_document, dispatcher, injection_call, guard, seed)
    if not surface.get("supported"):
        return {"supported": False, "surface_selection": surface}
    fact = ctx.fact("N6", "ambient_path_subroute_return_to_actual_dispatch", dispatcher_document,
        [selector_call, declaration, guard, injection_call], {"seed_path": seed, "returned_route": returned_route,
        "selector_declaration": selector_document.location(ports._function(selector)),
        "selector_path_projection": selector_document.location(path_declaration),
        "selector_return_guard": selector_document.location(branch_node),
        "selector_binding": selector_binding, "injection_binding": injection_binding,
        "other_ancestor_conditions": [dispatcher_document.location(parent) for parent in _ancestors(injection_call, _statement_body(dispatcher)) if parent.type == "if_statement" and parent != guard],
        "scope": "selected subroute branch; outer auth/surface/lifecycle guards remain actual applicability conditions"})
    ctx.model("js-hash-path-strip-1", [fact], {"strip_leading_hash_and_query_tail": True,
                                             "regex_receiver_standard_string_premise": True})
    return {"supported": True, "fact_ids": [*surface.get("fact_ids", []), fact], "returned_route": returned_route,
            "surface_selection": surface,
            "outer_conditions": [dispatcher_document.text(_field(parent, "condition")) for parent in _ancestors(injection_call, _statement_body(dispatcher)) if parent.type == "if_statement" and parent != guard]}


def _ancestors(node: Any, boundary: Any) -> list[Any]:
    result = []
    parent = node.parent
    while parent is not None and parent != boundary:
        result.append(parent)
        parent = parent.parent
    return result


def _surface_dispatch(ctx: _Context, document: Any, owner: Any, injection_call: Any,
                      subroute_guard: Any, seed: str) -> dict:
    """Connect the actual outer surface guard to a finite source catalog find."""
    ancestors = [node for node in _ancestors(injection_call, _statement_body(owner))
                 if node.type == "if_statement" and node != subroute_guard]
    candidates = []
    for guard in ancestors:
        condition = unwrap(_field(guard, "condition"))
        if condition is None or condition.type != "binary_expression" or document.text(_field(condition, "operator")) != "===":
            continue
        receiver, field = ports._member(document, _field(condition, "left"))
        expected = _literal_string(document.text(_field(condition, "right")))
        if field == "id" and expected is not None and receiver is not None and receiver.type == "identifier":
            candidates.append((guard, receiver, expected))
    if len(candidates) != 1:
        ctx.gap("N6", "surface_dispatch_guard_unknown", "Outer surface discriminator guard is not unique")
        return {"supported": False}
    guard, receiver, expected = candidates[0]
    receiver_record = ctx.record("N6", document, receiver, allow_writes=True)
    writes = []
    for node in ctx.direct(_statement_body(owner)):
        if node.type != "assignment_expression" or node.end_byte > guard.start_byte:
            continue
        left = unwrap(_field(node, "left"))
        if left is not None and left.type == "identifier" and ctx.same(document, receiver_record, ctx.record("N6", document, left, allow_writes=True)):
            writes.append(node)
    if len(writes) != 1 or unwrap(_field(writes[0], "right")).type != "call_expression":
        ctx.gap("N6", "surface_reaching_assignment_unknown", "Surface guard lacks a unique earlier actual selector assignment")
        return {"supported": False}
    assignment = writes[0]
    if (_direct_statement(assignment, _statement_body(owner)) is None
            or guard.parent != _statement_body(owner)):
        ctx.gap("N6", "surface_assignment_not_direct_guard_prefix", "Actual surface assignment/guard are not normal direct body statements")
        return {"supported": False}
    call = unwrap(_field(assignment, "right"))
    arguments = ports._arguments(call)
    if len(arguments) != 1 or _path(document, arguments[0]) != ctx.rule["ambient"]["read_path"]:
        ctx.gap("N6", "surface_selector_ambient_argument_unknown", "Actual surface selector argument is not selected ambient hash")
        return {"supported": False}
    helper_document, helper, binding = ctx.actual_target("N6", document, call, owner)
    if helper is None:
        return {"supported": False}
    body = _statement_body(helper)
    statements = _children(body)
    if len(statements) != 2 or statements[0].type != "lexical_declaration" or statements[1].type != "return_statement":
        ctx.gap("N6", "surface_selector_prefix_unknown", "Finite catalog selector must have one path declaration and one return")
        return {"supported": False}
    declarations = [node for node in _children(statements[0]) if node.type == "variable_declarator"]
    parameters = _children(_field(ports._function(helper), "parameters"))
    if len(declarations) != 1 or len(parameters) != 1:
        ctx.gap("N6", "surface_selector_parameter_shape_unknown", "Finite selector has unsupported parameter/declaration shape")
        return {"supported": False}
    declaration = declarations[0]
    origin, strip_operations = _strip_hash_expression(ctx, helper_document, _field(declaration, "value"))
    parameter = _field(parameters[0], "pattern") or _field(parameters[0], "name") or parameters[0]
    if origin != [helper_document.text(parameter)]:
        ctx.gap("N6", "surface_path_parameter_unknown", "Surface path projection is not the actual formal parameter")
        return {"supported": False}
    path_record = ctx.record("N6", helper_document, _field(declaration, "name"))
    returned = unwrap(_return_expression(statements[1]))
    if returned is None or returned.type != "binary_expression" or helper_document.text(_field(returned, "operator")) != "??":
        ctx.gap("N6", "surface_catalog_find_shape_unknown", "Surface return is not finite find with explicit fallback")
        return {"supported": False}
    find_call = unwrap(_field(returned, "left"))
    catalog_identifier, find_method = ports._member(helper_document, _field(find_call, "function"))
    find_arguments = ports._arguments(find_call) if find_call is not None and find_call.type == "call_expression" else []
    if find_method != "find" or len(find_arguments) != 1 or unwrap(find_arguments[0]).type != "arrow_function":
        ctx.gap("N6", "surface_catalog_predicate_unknown", "Catalog selection is not one source arrow predicate")
        return {"supported": False}
    predicate = unwrap(find_arguments[0])
    predicate_parameter = _field(predicate, "parameter")
    if predicate_parameter is None:
        predicate_parameters = _children(_field(predicate, "parameters"))
        predicate_parameter = predicate_parameters[0] if len(predicate_parameters) == 1 else None
    predicate_record = ctx.record("N6", helper_document, predicate_parameter)
    expression = unwrap(_field(predicate, "body"))
    if expression is None or expression.type != "binary_expression" or helper_document.text(_field(expression, "operator")) != "||":
        ctx.gap("N6", "surface_predicate_disjunction_unknown", "Catalog predicate is not exact-or-path-prefix")
        return {"supported": False}
    equality, prefix = unwrap(_field(expression, "left")), unwrap(_field(expression, "right"))
    item_receiver, item_property = ports._member(helper_document, _field(equality, "left"))
    compared_path = unwrap(_field(equality, "right"))
    prefix_receiver, prefix_method = ports._member(helper_document, _field(prefix, "function"))
    prefix_arguments = ports._arguments(prefix) if prefix is not None and prefix.type == "call_expression" else []
    if (equality is None or equality.type != "binary_expression" or helper_document.text(_field(equality, "operator")) != "==="
            or item_property != "path" or not ctx.same(helper_document, predicate_record, ctx.record("N6", helper_document, item_receiver))
            or not ctx.same(helper_document, path_record, ctx.record("N6", helper_document, compared_path))
            or prefix_method != "startsWith" or not ctx.same(helper_document, path_record, ctx.record("N6", helper_document, prefix_receiver))
            or len(prefix_arguments) != 1 or prefix_arguments[0].type != "template_string"):
        ctx.gap("N6", "surface_predicate_binding_unknown", "Catalog predicate roots do not match actual item/path declarations")
        return {"supported": False}
    template_parts = _children(prefix_arguments[0])
    if len(template_parts) != 2 or template_parts[0].type != "template_substitution" or helper_document.text(template_parts[1]) != "/":
        ctx.gap("N6", "surface_prefix_template_unknown", "Prefix does not use the finite item path plus slash")
        return {"supported": False}
    substituted = unwrap(_return_expression(template_parts[0]))
    sub_receiver, sub_property = ports._member(helper_document, substituted)
    if sub_property != "path" or not ctx.same(helper_document, predicate_record, ctx.record("N6", helper_document, sub_receiver)):
        ctx.gap("N6", "surface_prefix_item_identity_unknown", "Prefix template uses a different item identity")
        return {"supported": False}
    catalog_record = ctx.record("N6", helper_document, catalog_identifier)
    catalog_declaration = ctx.lexical(helper_document).declaration_for(catalog_record) if catalog_record else None
    catalog = unwrap(_field(catalog_declaration, "value"))
    def frozen(node: Any) -> Any:
        node = unwrap(node)
        if node is None or node.type != "call_expression":
            return None
        root, method = ports._member(helper_document, _field(node, "function"))
        args = ports._arguments(node)
        if method != "freeze" or helper_document.text(root) != "Object" or len(args) != 1 or not ports._builtin(ctx.port_context, "N6", helper_document, root, "freeze"):
            return None
        return unwrap(args[0])
    array = frozen(catalog)
    if array is None or array.type != "array":
        ctx.gap("N6", "surface_catalog_not_closed", "Catalog is not an authenticated freeze literal array")
        return {"supported": False}
    entries, entry_nodes = [], []
    for item in _children(array):
        obj = frozen(item)
        members = ports._properties(ctx.port_context, "N6", helper_document, obj, data_only=True) if obj is not None else None
        if members is None or "id" not in members or "path" not in members:
            ctx.gap("N6", "surface_catalog_entry_unknown", "Catalog entry lacks closed static id/path fields")
            return {"supported": False}
        item_id = _literal_string(helper_document.text(members["id"]["value"]))
        item_path = _literal_string(helper_document.text(members["path"]["value"]))
        if item_id is None or item_path is None:
            ctx.gap("N6", "surface_catalog_literal_unknown", "Catalog id/path are not finite literals")
            return {"supported": False}
        entries.append({"id": item_id, "path": item_path})
        entry_nodes.append(obj)
    matched = [entry for entry in entries if seed == entry["path"] or seed.startswith(entry["path"] + "/")]
    if not matched or matched[0]["id"] != expected:
        ctx.gap("N6", "source_seed_selects_other_surface", "Actual finite find selection does not satisfy outer surface guard")
        return {"supported": False}
    fact = ctx.fact("N6", "actual_ambient_hash_selects_source_catalog_surface", document,
        [assignment, call, guard], {"selector_binding": binding, "seed_path": seed,
        "source_catalog": entries, "selected_first_match": matched[0], "required_guard_surface_id": expected,
        "helper_path_projection": helper_document.location(declaration),
        "predicate": helper_document.location(predicate), "catalog_location": helper_document.location(catalog_declaration),
        "source_catalog_entry_locations": [helper_document.location(item) for item in entry_nodes],
        "find_and_string_prefix_semantics": "standard finite catalog model", "runtime_observed": False})
    ctx.model("js-hash-path-strip-1", [fact], {"operation": "exact_or_slash_prefix_first_find"})
    return {"supported": True, "fact_ids": [fact], "selected_surface": matched[0]}


def _page_submit(ctx: _Context) -> dict:
    selector = ctx.rule["wiring"]["injection"]
    document, owner = ctx.select("N4", selector)
    page_document, page = ctx.select("N4", ctx.rule["completion"]["page"])
    if owner is None or page is None:
        return {"supported": False}
    model_calls = ports._calls(document, owner, selector["callee"])
    page_calls = ports._calls(document, owner, ctx.rule["completion"]["page_callee"])
    if len(model_calls) != 1 or len(page_calls) != 1:
        ctx.gap("N4", "page_model_construction_not_unique", "VM/page constructors are not unique in actual injection owner")
        return {"supported": False}
    model_call, page_call = model_calls[0], page_calls[0]
    actual_document, actual, binding = ctx.actual_target("N4", document, page_call, owner, page_document, page)
    if actual is not page:
        return {"supported": False}
    model_declaration = model_call.parent
    if model_declaration is None or model_declaration.type != "variable_declarator" or not ports._const(model_declaration):
        ctx.gap("N4", "vm_return_capture_unknown", "Actual model result is not captured as a const")
        return {"supported": False}
    model_record = ctx.record("N4", document, _field(model_declaration, "name"))
    arguments = ports._arguments(page_call)
    members = ports._properties(ctx.port_context, "N4", document, arguments[0], data_only=False) if len(arguments) == 1 else None
    if members is None or "model" not in members:
        ctx.gap("N4", "page_actual_model_field_unknown", "Actual page object does not have a closed model data field")
        return {"supported": False}
    actual_model = unwrap(members["model"]["value"])
    if actual_model is None or actual_model.type not in {"identifier", "shorthand_property_identifier"} or not ctx.same(document, model_record, ctx.record("N4", document, actual_model)):
        ctx.gap("N4", "page_model_capture_mismatch", "Page model field is not the VM constructor result binding")
        return {"supported": False}
    parameter, parameter_record = ports._parameter(ctx.port_context, "N4", page_document, page, 0)
    if parameter_record is None:
        ctx.gap("N4", "page_formal_parameter_unknown", "Actual page formal binding is unknown")
        return {"supported": False}
    mutation_audit = _model_mutation_audit(ctx, document, owner, model_record, actual_model,
                                         page_document, page, parameter_record)
    if not mutation_audit.get("supported"):
        return {"supported": False}
    event_registrations = []
    nodes = ctx.direct(_statement_body(page))
    for call in (node for node in nodes if node.type == "call_expression"):
        receiver, key = ports._member(page_document, _field(call, "function"))
        args = ports._arguments(call)
        if key == "addEventListener" and len(args) == 2 and _literal_string(page_document.text(args[0])) == "submit":
            event_registrations.append((call, receiver, args[1]))
    if len(event_registrations) != 1:
        ctx.gap("N4", "submit_listener_not_unique", "Actual page has no unique submit event registration")
        return {"supported": False}
    registration, form, callback_identifier = event_registrations[0]
    form_record = ctx.record("N4", page_document, form)
    if form_record is None:
        return {"supported": False}
    form_kind = _dom_helper_kind(ctx, "N4", page_document, page, form_record, "form")
    form_chain, form_hidden = _dom_install_path(ctx, page_document, page, form_record, parameter_record, "N4")
    if (not form_kind.get("supported") or not form_chain
            or _direct_statement(registration, _statement_body(page)) is None):
        ctx.gap("N4", "submitted_form_installation_unknown", "Submit listener receiver is not a directly installed actual form",
                hidden_bindings=form_hidden)
        return {"supported": False}
    callback_record = ctx.record("N4", page_document, callback_identifier)
    declaration = ctx.lexical(page_document).declaration_for(callback_record) if callback_record else None
    callback = unwrap(_field(declaration, "value"))
    if callback is None or callback.type not in _FUNCTIONS or function_kind(page_document, callback).get("kind") != "ordinary_sync":
        ctx.gap("N4", "submit_event_callback_unknown", "Registered submit callback is not a unique ordinary const function")
        return {"supported": False}
    submit_calls = []
    for call in ctx.direct(_field(callback, "body")):
        if call.type != "call_expression":
            continue
        receiver, method = ports._member(page_document, _field(call, "function"))
        model_receiver, model_property = ports._member(page_document, receiver)
        if method != ctx.rule["wiring"]["use"]["returned_method"] or model_property != "model":
            continue
        if ctx.same(page_document, parameter_record, ctx.record("N4", page_document, model_receiver)):
            submit_calls.append(call)
    if len(submit_calls) != 1:
        ctx.gap("N4", "page_submit_receiver_unknown", "Callback does not invoke the actual mapped options.model method uniquely")
        return {"supported": False}
    submit_call = submit_calls[0]
    statements = _children(_field(callback, "body"))
    submit_statement = next((node for node in statements if node.start_byte <= submit_call.start_byte < node.end_byte), None)
    if submit_statement is None or submit_statement.type != "expression_statement":
        ctx.gap("N4", "submit_callback_control_unknown", "Selected submit call is not a direct callback statement")
        return {"supported": False}
    # DOM event completion is conditional on the callback reaching this call.
    # The only prior statement must be its own event.preventDefault().
    before = [node for node in statements if node.end_byte <= submit_statement.start_byte]
    callback_parameters = _children(_field(callback, "parameters"))
    callback_parameter = callback_parameters[0] if len(callback_parameters) == 1 else None
    callback_parameter = _field(callback_parameter, "pattern") or _field(callback_parameter, "name") or callback_parameter
    event_record = ctx.record("N4", page_document, callback_parameter) if callback_parameter is not None else None
    if len(before) != 1 or before[0].type != "expression_statement":
        ctx.gap("N4", "submit_callback_prefix_unknown", "Event callback has unsupported prior effects/control")
        return {"supported": False}
    before_expression = unwrap(_return_expression(before[0]))
    event_receiver, event_method = ports._member(page_document, _field(before_expression, "function"))
    if (before_expression is None or before_expression.type != "call_expression" or event_method != "preventDefault"
            or ports._arguments(before_expression) or not ctx.same(page_document, event_record, ctx.record("N4", page_document, event_receiver))):
        ctx.gap("N4", "event_prefix_not_dom_prevent_default", "Prior event effect is not modeled preventDefault of the actual event binding")
        return {"supported": False}
    fact = ctx.fact("N4", "actual_vm_result_to_page_submit_callback", document,
        [model_call, model_declaration, page_call, actual_model], {
        "page_actual_binding": binding, "page_formal_location": page_document.location(parameter),
        "submit_registration": page_document.location(registration),
        "form_append_chain": [page_document.location(node) for node in form_chain],
        "submit_callback": page_document.location(callback), "submit_call": page_document.location(submit_call),
        "page_model_declaration_id": model_record.get("declaration_id"),
        "callback_target_method": ctx.rule["wiring"]["use"]["returned_method"],
        "event_registration_scope": "while mounted, before removeEventListener/close",
        "public_vm_mutation_scope": "source-declared mounted page invokes unchanged source-returned model method"})
    ctx.model("dom-anchor-append-listener-1", [fact], {"actual_registration_callback_protocol": True,
        "event_prevent_default_has_no_model_receiver_mutation": True, "actual_event_not_observed": True})
    ctx.model("ordinary-source-method-invocation-1", [fact], {"source_returned_method_identity": True,
        "external_monkey_patching_excluded": True, "callback_execution_not_observed": True})
    return {"supported": True, "fact_ids": [*form_kind.get("fact_ids", []), *mutation_audit.get("fact_ids", []), fact],
            "page_binding": binding}


def _model_mutation_audit(ctx: _Context, document: Any, owner: Any, model_record: dict,
                          mapped_argument: Any, page_document: Any, page: Any,
                          page_parameter: dict) -> dict:
    """Keep the ordinary invocation model separate from visible source writes."""
    caller_writes = ctx.lexical(document).writes(model_record)
    if caller_writes:
        ctx.gap("N4", "captured_model_write_or_alias_effect", "Actual caller model has captured writes or unresolved alias effects",
                writes=caller_writes)
        return {"supported": False}
    caller_references = []
    binder = model_record.get("binder_location", {})
    for node in walk(_statement_body(owner)):
        if node.type not in {"identifier", "shorthand_property_identifier"}:
            continue
        candidate = ctx.lexical(document).resolve(node)
        if not ctx.same(document, model_record, candidate):
            continue
        if node == mapped_argument or node.start_byte == binder.get("start_byte") and node.end_byte == binder.get("end_byte"):
            continue
        parent = node.parent
        if parent is not None and parent.type in {"member_expression", "subscript_expression"} and _field(parent, "object") == node:
            _, key = ports._member(document, parent)
            consumer = parent.parent
            if key is not None and consumer is not None and consumer.type == "call_expression" and unwrap(_field(consumer, "function")) == parent:
                caller_references.append(document.location(parent))
                continue
        ctx.gap("N4", "caller_model_alias_or_escape", "Actual host model escapes its mapped page/declared member invocation", document, node)
        return {"supported": False}
    model_root_name = page_parameter.get("name")
    prefix = [model_root_name, "model"]
    audited = []
    for node in walk(_statement_body(page)):
        path = _path(page_document, node)
        if path != prefix:
            continue
        receiver, _ = ports._member(page_document, node)
        if receiver is None or not ctx.same(page_document, page_parameter, ctx.record("N4", page_document, receiver)):
            continue
        parent = node.parent
        while parent is not None and parent.type in {"as_expression", "satisfies_expression", "parenthesized_expression", "non_null_expression"}:
            parent = parent.parent
        if parent is not None and parent.type in {"member_expression", "subscript_expression"} and _field(parent, "object") == node:
            _, member = ports._member(page_document, parent)
            if member is None:
                ctx.gap("N4", "captured_model_dynamic_member", "Page model has unknown member lookup/effect", page_document, parent)
                return {"supported": False}
            grandparent = parent.parent
            if grandparent is not None and grandparent.type in {"assignment_expression", "augmented_assignment_expression", "update_expression", "unary_expression"} and (
                    _field(grandparent, "left") == parent or _field(grandparent, "argument") == parent):
                ctx.gap("N4", "captured_model_method_written", "Page visibly changes a returned model member", page_document, grandparent)
                return {"supported": False}
            audited.append(page_document.location(parent))
            continue
        ctx.gap("N4", "captured_model_alias_or_escape", "Page passes/copies the model object outside fixed member invocation", page_document, node)
        return {"supported": False}
    for write in ctx.lexical(page_document).writes(page_parameter):
        location = write.get("location", {})
        write_node = _node_at(page_document, location, {"assignment_expression", "augmented_assignment_expression", "update_expression", "unary_expression"})
        target = _field(write_node, "left") or _field(write_node, "argument") if write_node is not None else None
        path = _path(page_document, target)
        if not write.get("mutation_target_complete") or path and path[:2] == prefix:
            ctx.gap("N4", "page_model_field_mutation", "Page actual model field has visible/unknown mutation", writes=[write])
            return {"supported": False}
    fact = ctx.fact("N4", "actual_model_capture_write_alias_and_member_review", document,
        [mapped_argument], {"caller_model_declaration_id": model_record.get("declaration_id"),
        "caller_visible_write_count": 0, "page_parameter_declaration_id": page_parameter.get("declaration_id"),
        "caller_fixed_member_calls": caller_references,
        "page_fixed_member_references": audited, "page_selected_model_writes_or_bare_escapes": False,
        "external_monkey_patch_exclusion_is_separate_model_premise": True})
    return {"supported": True, "fact_ids": [fact]}


def _http_rejection(ctx: _Context) -> dict:
    consumer = ctx.details.get("consumer", {})
    method_selector = consumer.get("returned_method", {})
    identity = method_selector.get("graph_node_id")
    nodes = ctx.sources.nodes.get(identity, [])
    document, method, problems = ctx.sources.definition_for_node(nodes[0]) if len(nodes) == 1 else (None, None, [])
    if method is None or problems:
        ctx.gap("N5", "factory_create_source_unknown", "Returned create method source is incomplete", problems=problems)
        return {"supported": False}
    function = ports._function(method)
    kind = function_kind(document, function)
    body = _field(function, "body")
    statements = _children(body)
    commands = [node for node in ctx.direct(body) if node.type == "call_expression"
                and _path(document, _field(node, "function")) == ctx.rule["completion"]["http_boundary_path"]]
    guards = consumer.get("factory_null_throw_guards", [])
    if not commands or len(guards) != 1 or kind.get("kind") != "ordinary_async":
        ctx.gap("N5", "factory_http_null_guard_unknown", "Actual async method lacks unique propagated null guard or command boundary")
        return {"supported": False}
    condition = _node_at(document, guards[0]["location"])
    guard = condition.parent if condition is not None else None
    while guard is not None and guard.type == "parenthesized_expression":
        guard = guard.parent
    if guard is None or guard.type != "if_statement" or guard.parent != body or _field(guard, "alternative") is not None:
        ctx.gap("N5", "throw_guard_not_direct_statement", "Null throw guard is not a direct complete body statement")
        return {"supported": False}
    consequence = _field(guard, "consequence")
    consequent_statements = _children(consequence) if consequence.type == "statement_block" else [consequence]
    if len(consequent_statements) != 1 or consequent_statements[0].type != "throw_statement":
        ctx.gap("N5", "null_guard_consequent_incomplete", "Null guard branch is not solely an abrupt throw")
        return {"supported": False}
    prefix = [node for node in statements if node.end_byte <= guard.start_byte]
    callback_invocations = consumer.get("callback_invocations", [])
    if len(prefix) != 1 or prefix[0].type != "lexical_declaration" or len(callback_invocations) != 1:
        ctx.gap("N5", "create_prefix_unknown", "Create has unmodeled statements before its propagated null rejection guard")
        return {"supported": False}
    invocation = _node_at(document, callback_invocations[0]["location"], {"call_expression"})
    if invocation is None or not (prefix[0].start_byte <= invocation.start_byte < prefix[0].end_byte):
        ctx.gap("N5", "await_callback_guard_result_unmatched", "Actual awaited callback result is not the guard's preceding declaration")
        return {"supported": False}
    declarations = [node for node in _children(prefix[0]) if node.type == "variable_declarator"]
    initializer = unwrap(_field(declarations[0], "value")) if len(declarations) == 1 else None
    awaited = unwrap(_return_expression(initializer)) if initializer is not None and initializer.type == "await_expression" else None
    if (len(declarations) != 1 or _field(declarations[0], "name").type != "identifier"
            or initializer is None or initializer.type != "await_expression" or awaited != invocation):
        ctx.gap("N5", "callback_await_declaration_not_exact", "Pre-guard declaration is not solely the exact actual awaited callback result")
        return {"supported": False}
    if any(call.start_byte <= guard.end_byte for call in commands):
        ctx.gap("N5", "http_before_null_guard", "A command boundary precedes the rejection guard", document, commands[0])
        return {"supported": False}
    if not callback_invocations[0].get("completion_relation", {}).get("normal_value_relation_closed"):
        ctx.gap("N5", "callback_await_completion_unknown", "Async callback normal value consumption is not closed")
        return {"supported": False}
    fact = ctx.fact("N5", "propagated_callback_null_abrupt_before_all_method_commands", document,
        [prefix[0], guard, *commands], {"method_graph_node_id": identity,
        "callback_context_id": consumer.get("factory_context_id"),
        "callback_invocation_location": document.location(invocation),
        "command_count": len(commands), "all_commands_strictly_after_guard": True,
        "guard_action": "async_body_throw_rejects_promise", "body_prefix_complete": True,
        "scope": "this returned create method; unrelated HTTP/auth/read operations are not denied"})
    return {"supported": True, "fact_ids": [fact], "command_count": len(commands)}


def _counterexamples(ctx: _Context) -> dict:
    rule, details = ctx.rule, ctx.details
    required = set(rule["completion"]["required_query_keys"])
    preserved = [counter for counter in details.get("counterexample_producers", [])
                 if counter.get("source_complete") and counter.get("query_domain", {}).get("keyset_closed")
                 and required <= set(counter.get("query_domain", {}).get("guaranteed_keys", []))]
    if not preserved:
        ctx.gap("N7", "valid_seed_preservation_counterexample_unknown", "No captured valid-key seed preservation counterexample is closed")
    assembly = details.get("port_wiring", {})
    branch_facts = [fact for fact in assembly.get("source_facts", [])
                    if fact.get("operation") == "boot_undefined_guard_selects_port_branch"]
    fake = False
    alternate = None
    consumer_document, consumer_owner = ctx.select("N7", rule["consumer"])
    if consumer_owner is not None:
        factory_call = _node_at(consumer_document, details.get("consumer", {}).get("factory_call_location", {}), {"call_expression"})
        branch = factory_call.parent if factory_call is not None else None
        if branch is not None and branch.type == "ternary_expression":
            selected = next((key for key in ("consequence", "alternative") if unwrap(_field(branch, key)) == factory_call), None)
            other = unwrap(_field(branch, "alternative" if selected == "consequence" else "consequence"))
            if other is not None and other.type == "call_expression":
                alternate_document, alternate_owner, identity = ctx.actual_target("N7", consumer_document, other, consumer_owner)
                if alternate_owner is not None:
                    method, return_info, frozen = ports._returned(ctx.port_context, "N7", alternate_document,
                        alternate_owner, rule["consumer"]["returned_method"])
                    actual_args = ports._arguments(other)
                    actual_members = ports._properties(ctx.port_context, "N7", consumer_document, actual_args[0], data_only=True) if len(actual_args) == 1 else None
                    callback_property = rule["consumer"]["callback_property"]
                    method_calls = [node for node in ctx.direct(_field(method, "body")) if node.type == "call_expression"] if method is not None else []
                    has_same_callback_call = any(ports._member(alternate_document, _field(call, "function"))[1] == callback_property for call in method_calls)
                    fake = bool(method is not None and actual_members is not None and callback_property not in actual_members
                        and not has_same_callback_call and len(branch_facts) == 1
                        and branch_facts[0].get("observed", {}).get("boot_literal_property_present") is False)
                    if fake:
                        fact = ctx.fact("N7", "alternate_seed_factory_has_distinct_create_without_context_callback", consumer_document,
                            [branch, other], {"alternate_binding": identity,
                            "alternate_create_location": alternate_document.location(method),
                            "alternate_argument_keys": sorted(actual_members), "callback_property": callback_property,
                            "alternate_return_object_frozen": frozen, "same_null_context_callback_invoked": False,
                            "scope": "different source create branch; no claim fake execution succeeds"})
                        alternate = {"source_fact_id": fact, "actual_binding": identity}
    if not fake:
        ctx.gap("N7", "fake_branch_counterexample_unknown", "Actual default boot/alternate seed branch relationship is not closed")
    chat = _chat_counterexample(ctx)
    return {"supported": bool(preserved and fake and chat.get("supported")),
        "source_derived": [{"kind": "valid_seed_preserved", "producer": deepcopy(counter)} for counter in preserved]
            + [{"kind": "nondefault_seed_uses_alternate_factory", "actual_branch_fact": deepcopy(fact)} for fact in branch_facts],
        "alternate_factory": alternate,
        "independent_chat_source": chat,
        "scope_exclusions": ["manual URL containing a valid required key is outside this producer's absent-key premise",
                             "independent Chat creation uses a separate source entrance and is outside this navigation claim"],
        "scope_exclusion_is_not_independent_chat_success_proof": True}


def _chat_counterexample(ctx: _Context) -> dict:
    """Locate the distinct create-request source, without proving Chat success."""
    document, owner = ctx.select("N7", ctx.rule["completion"]["chat_counterexample"])
    if owner is None:
        return {"supported": False}
    constructions = []
    calls = []
    for node in ctx.direct(_statement_body(owner)):
        if node.type == "call_expression" and _path(document, _field(node, "function")) == ["options", "client", "command"]:
            calls.append(node)
        if node.type != "assignment_expression":
            continue
        value = unwrap(_field(node, "right"))
        if value is None or value.type != "object":
            continue
        members = ports._properties(ctx.port_context, "N7", document, value, data_only=True)
        request = unwrap(members["createRequest"]["value"]) if members and "createRequest" in members else None
        if request is None or request.type != "object":
            continue
        request_members = ports._properties(ctx.port_context, "N7", document, request, data_only=True)
        payload = unwrap(request_members["payload"]["value"]) if request_members and "payload" in request_members else None
        payload_members = ports._properties(ctx.port_context, "N7", document, payload, data_only=True) if payload is not None else None
        if not request_members or "command" not in request_members or not payload_members or "deliveryId" not in payload_members:
            continue
        delivery = unwrap(payload_members["deliveryId"]["value"])
        delivery_record = ctx.record("N7", document, delivery)
        declaration = ctx.lexical(document).declaration_for(delivery_record) if delivery_record else None
        initializer = unwrap(_field(declaration, "value"))
        if (declaration is not None and ports._const(declaration) and initializer is not None
                and initializer.type == "call_expression" and _path(document, _field(initializer, "function")) == ["options", "nextDeliveryId"]):
            constructions.append((node, request, request_members["command"]["value"], payload_members["deliveryId"]["value"], declaration))
    if len(constructions) != 1 or not calls:
        ctx.gap("N7", "independent_chat_create_source_unknown", "Distinct Chat create-request/id source is not a unique captured construction")
        return {"supported": False}
    assignment, request, command, delivery, declaration = constructions[0]
    fact = ctx.fact("N7", "independent_chat_create_request_has_own_delivery_id_source", document,
        [assignment, request, command, delivery, declaration, *calls], {
        "chat_owner_graph_node_id": owner.graph_node_id,
        "command_source_form": document.text(command),
        "delivery_id_source_form": document.text(_field(declaration, "value")),
        "client_submission_argument_forms": [document.text(ports._arguments(call)[0]) if ports._arguments(call) else None for call in calls],
        "source_entrance_distinct_from_selected_navigation": True,
        "scope": "distinct local request construction/submission forms; not complete Chat transport or successful creation",
        "same_missing_ambient_query_guard_required_by_this_construction": False})
    return {"supported": True, "fact_ids": [fact], "actual_chat_success_proven": False}


def _prior_gap_dispositions(ctx: _Context, observations: dict[str, dict]) -> list[dict]:
    """Explain old local limitations without erasing original evidence gaps."""
    results = []
    for gap in ctx.details.get("analysis_gaps", []):
        code = gap.get("code", "")
        kind, obligation, reason = None, None, None
        if code in {"navigation_effect_not_observed", "ambient_hash_read_timing_unknown"} and observations.get("N6", {}).get("supported"):
            kind, obligation = "explicit_platform_condition", "N6"
            reason = "No browser execution is claimed; the declared href navigation/current-hash stability conditions carry the real platform seam."
        elif code in {"ui_route_dispatch_not_followed", "route_dispatch_not_analyzed"} and observations.get("N6", {}).get("supported"):
            kind, obligation = "additional_source_relation_closed", "N6"
            reason = "Actual path projection, returned subroute, catalog surface and authenticated injection dispatch are now connected."
        elif code == "event_activation_unknown" and observations.get("N4", {}).get("supported") and observations.get("N6", {}).get("supported"):
            kind, obligation = "source_registration_closed_event_delivery_conditional", "N4"
            reason = "Actual installed form registration/callback/model invocation is proved; delivery of a submit event is an explicit platform condition."
        elif code == "snapshot_injection_call_not_resolved" and observations.get("N4", {}).get("supported"):
            kind, obligation = "independent_literal_import_model_closed", "N4"
            reason = "Authenticated literal import/export/namespace position maps the source callee; the historical dynamic CALLS edge remains unchanged."
        elif code == "public_returned_object_not_frozen" and observations.get("N4", {}).get("supported"):
            kind, obligation = "captured_mutation_audit_and_ordinary_invocation_model", "N4"
            reason = "Visible caller/page member writes, aliases and bare escapes are audited; external method monkey-patching is an explicit ordinary invocation model exclusion."
        elif code == "other_port_method_effects_unknown" and observations.get("N4", {}).get("supported") and observations.get("N5", {}).get("supported"):
            kind, obligation = "unrelated_heap_effects_not_part_of_selected_null_judgment", "N5"
            reason = "The existing validated freeze model fixes the selected create method identity; the selected callback reads the then-current hash. Other methods' successful behavior is not claimed."
        elif code == "helper_object_or_effect_semantics_not_modeled" and observations.get("N5", {}).get("supported"):
            lookups = ctx.details.get("consumer", {}).get("query_lookups", [])
            null_guards = ctx.details.get("consumer", {}).get("null_return_guards", [])
            downstream = any(lookup.get("location", {}).get("file") == gap.get("file")
                             and lookup.get("location", {}).get("line", 0) > gap.get("line", 0) for lookup in lookups)
            independent_null = any(guard.get("condition_truth") is True and guard.get("action") == "return_null"
                                   and guard.get("lookup_dependencies") for guard in null_guards)
            if downstream and independent_null:
                kind, obligation = "opaque_auth_result_not_needed_by_selected_boolean_guard", "N5"
                reason = "The missing-key lookup occurs after this normal-prefix helper; its null operand independently forces the actual OR null-return guard. No auth helper object value/effect is proved."
        if kind is None:
            ctx.gap("analysis", "prior_navigation_source_gap_still_required", "A local source limitation has no justified completion disposition", original_gap=deepcopy(gap))
            kind, obligation = "unresolved", "analysis"
        results.append({"original_gap": deepcopy(gap), "disposition": kind, "obligation": obligation,
                        "reason": reason, "original_evidence_preserved": True})
    return results


def analyze_navigation_completion(snapshot: GraphSnapshot, rule: dict) -> dict:
    """Complete N1..N7 within an explicit finite, conditional source scope."""
    from .navigation_analysis import analyze_navigation_contracts
    base_rule = {key: value for key, value in rule.items() if key != "completion"}
    findings = analyze_navigation_contracts(snapshot, [base_rule])
    navigation_details = findings[0].evidence[0].details if findings and findings[0].evidence else {}
    ctx = _Context(snapshot, rule, navigation_details)
    observations: dict[str, dict] = {}
    try:
        validate_navigation_completion_rule(rule)
        visible = _ast_source_visible(ctx)
        observations["N1"] = visible
        producer = navigation_details.get("producer", {})
        trace = navigation_details.get("source_trace", [])
        helper_operations = {event.get("operation") for event in trace}
        observations["N2"] = {"supported": bool(producer.get("source_complete")
            and {"argument_binds_parameter", "helper_normal_return", "query_key_mutation", "query_serialization"} <= helper_operations
            and navigation_details.get("source_trace_complete")), "source_trace_pointer": "/navigation_source/source_trace"}
        required = set(rule["completion"]["required_query_keys"])
        domain = producer.get("query_domain", {})
        missing = sorted(required - set(domain.get("possible_keys", []))) if domain.get("keyset_closed") else []
        observations["N3"] = {"supported": bool(required and missing == sorted(required)
            and domain.get("keyset_closed") and set(domain.get("guaranteed_keys", [])) <= set(domain.get("possible_keys", []))),
            "query_domain": deepcopy(domain), "required_keys": sorted(required), "missing_keys": missing}
        page = _page_submit(ctx)
        assembly = navigation_details.get("port_wiring", {})
        observations["N4"] = {"supported": bool(page.get("supported") and assembly.get("assembly_complete")
            and assembly.get("navigation_context_identity_matched")), "port_assembly_pointer": "/navigation_source/port_wiring", "page_event": page}
        rejection = _http_rejection(ctx)
        consumer = navigation_details.get("consumer", {})
        observations["N5"] = {"supported": bool(rejection.get("supported") and consumer.get("source_complete")
            and consumer.get("callback_relation_closed") and consumer.get("all_consumer_returns_throw")
            and required <= set(consumer.get("required_query_keys", []))),
            "consumer_pointer": "/navigation_source/consumer", "http_rejection": rejection}
        route = _route_dispatch(ctx, visible.get("seed_path", "")) if visible.get("supported") else {"supported": False}
        conditions = [*rule.get("ambient", {}).get("conditions", []),
                      "The mounted page and its source-returned model methods are used under the declared ordinary DOM/JS model; no external method monkey-patching.",
                      "During the relevant route selector and deliveryContext hash reads, the current hash is the selected href navigation result; authentication, access, loading and lifecycle guards permit mounting.",
                      "A submit event is delivered to the mounted form and all captured ViewModel form guards permit port.create."]
        observations["N6"] = {"supported": bool(route.get("supported") and page.get("supported")
            and rule.get("ambient", {}).get("kind") == "navigation_hash_stability"
            and rule.get("ambient", {}).get("conditions")), "route_dispatch": route, "conditions": conditions,
            "conditions_scope": "actual platform/event/form applicability, not substitutes for missing source relations"}
        observations["N7"] = _counterexamples(ctx)
    except (ValueError, TypeError, AttributeError, ImportError, RuntimeError, RecursionError, OverflowError) as error:
        ctx.gap("analysis", "navigation_completion_unknown", "Completion extraction failed conservatively",
                error_kind=type(error).__name__, error=str(error)[:300])
    prior_gaps = _prior_gap_dispositions(ctx, observations)
    obligations = []
    for number in range(1, 8):
        key = f"N{number}"
        observation = observations.get(key, {"supported": False})
        gaps = [gap for gap in ctx.gaps if gap["obligation"] in {key, "analysis"}]
        supported = bool(observation.get("supported") and not gaps)
        obligations.append({"id": key, "status": "supported" if supported else "unknown",
            "assessment": "supported_within_declared_scope" if supported else "unknown",
            "supported": supported, "observation": observation,
            "source_fact_ids": [fact["id"] for fact in ctx.facts if fact["obligation"] == key],
            "gap_ids": [gap["id"] for gap in gaps], "gaps": gaps})
    complete = all(obligation["supported"] for obligation in obligations)
    return {"version": VERSION, "semantic_source_version": SOURCE_VERSION, "lexical_version": LEXICAL_VERSION,
        "completion_summaries_version": COMPLETION_VERSION, "snapshot_id": snapshot.id,
        "source_hash": snapshot.source_hash, "contract_hash": _digest(rule), "policy_hash": snapshot.policy_hash,
        "assessment": "scoped_static_judgment_reproduced" if complete else "partial_obligations_supported",
        "end_to_end_complete": complete, "complete_assessment": complete, "full_goal_supported": complete,
        "full_functionality_proven": False,
        "scope": "conditional default producer navigation through actual mounted task port null rejection before its command calls",
        "obligations": obligations, "source_facts": ctx.facts, "model_applications": ctx.model_applications,
        "navigation_source": deepcopy(navigation_details),
        "prior_local_gap_dispositions": prior_gaps,
        "assembly_model_applications": ctx.port_context.models,
        "necessary_gaps": ctx.gaps, "conditions": observations.get("N6", {}).get("conditions", []),
        "source_conditions": observations.get("N6", {}).get("conditions", []),
        "original_claim": "Default visible board new-task href omits required delivery context; production task creation rejects before its HTTP submission in explicit navigation/form conditions.",
        "derived_judgment": ("The selected source-derived absent-query path reaches the actual production port callback and rejects its create before command calls, under the retained platform/form conditions." if complete else "Only listed source obligations are closed; the full conditional chain has unresolved required relations."),
        "refutations": observations.get("N7", {}),
        "policy_declared": {"completion": deepcopy(rule.get("completion")), "provenance": deepcopy(rule.get("provenance"))},
        "coverage": {"ast_nodes_enumerated": ctx.node_count, "node_budget": _MAX_NODES,
            "fact_count": len(ctx.facts), "fact_budget": _MAX_FACTS, "sampling": False},
        "target_executed": False, "target_tests_run": False, "target_build_run": False,
        "snapshot_calls_edges_created": False, "runtime_proof": False}


def analyze_navigation_completions(snapshot: GraphSnapshot, rules: list[dict]) -> list[Finding]:
    """Normal analyzer entry: source computation produces every obligation."""
    results = []
    for index, rule in enumerate(rules):
        try:
            validate_navigation_completion_rule(rule)
            details = analyze_navigation_completion(snapshot, rule)
        except (ValueError, TypeError, AttributeError, RuntimeError, RecursionError) as error:
            details = {"version": VERSION, "snapshot_id": snapshot.id,
                "assessment": "unknown", "end_to_end_complete": False,
                "obligations": [], "necessary_gaps": [{"code": "navigation_completion_rule_invalid", "message": str(error)}]}
        confirmed = bool(details.get("end_to_end_complete"))
        details["full_goal_supported"] = confirmed
        description = "默认可见导航入口的完整静态条件判断。源码绑定、查询键、装配、事件及 HTTP 前拒绝逐义务保存；真实环境条件另列。"
        fingerprint = _digest({"version": VERSION, "rule": rule, "project_id": snapshot.project_id})
        locations = [location for fact in details.get("source_facts", []) for location in fact.get("locations", [])]
        evidence = Evidence(_digest({"snapshot": snapshot.id, "fingerprint": fingerprint, "details": details})[:24],
            "static_navigation_completion", description, locations=locations, details=details)
        results.append(Finding(id=_digest({"snapshot": snapshot.id, "fingerprint": fingerprint})[:24],
            type="static_navigation_complete_judgment", severity=rule.get("severity", "medium"), status="uncertain",
            title="导航拒绝条件判断已完整支持" if confirmed else "导航完整判断仍有未知义务",
            description=description, evidence=[evidence], rule_id=rule.get("id", f"invalid-navigation-completion-{index}"),
            fingerprint=fingerprint, snapshot_id=snapshot.id,
            metadata={"navigation_completion_version": VERSION, "full_goal_supported": confirmed,
                      "runtime_proof": False, "full_functionality_proven": False}))
    return results
