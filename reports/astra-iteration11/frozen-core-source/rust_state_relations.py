"""Finite iterator/enum relations from authenticated captured Rust CST.

This is a source interpreter for a deliberately small expression language, not
a Rust executor, macro expander, type checker, or replacement call graph.  Rule
roles locate declarations only; enum members, predicates, map keys and results
are computed from the selected saved bodies.  Unsupported syntax stays unknown.
"""
from __future__ import annotations

from itertools import product
from typing import Any

VERSION = "captured-rust-finite-state-relations-1"
MODEL = "rust-finite-iterator-enum-source-v1"
REQUIRED_ROLES = frozenset({"aggregate_selector", "item_selector", "selector",
    "runnable", "effective_state", "validator"})
_IGNORED = {"line_comment", "block_comment", "attribute_item"}
_WRAPPERS = {"expression_statement", "parenthesized_expression", "else_clause"}
_ITERATORS = {"iter", "filter", "map", "collect", "find", "any", "all"}
_OTHER = "<other value of this state enum>"
_NODE_LIMIT = 131072


def _field(node: Any, name: str) -> Any:
    return node.child_by_field_name(name) if node is not None else None


def _children(node: Any) -> list[Any]:
    return [child for child in node.named_children if child.type not in _IGNORED] if node is not None else []


def _path(expression: dict) -> tuple[str, ...] | None:
    kind = expression.get("kind")
    if kind == "name":
        return (expression["name"],)
    if kind == "field":
        base = _path(expression["value"])
        return (*base, expression["field"]) if base else None
    if kind in {"borrow", "deref", "try"}:
        return _path(expression["value"])
    if kind == "method" and expression["method"] == "clone" and not expression["arguments"]:
        return _path(expression["receiver"])
    return None


def _walk(expression: Any):
    if isinstance(expression, dict):
        yield expression
        for key, value in expression.items():
            if key not in {"span", "source_text"}:
                yield from _walk(value)
    elif isinstance(expression, list):
        for value in expression:
            yield from _walk(value)


def _conjuncts(expression: dict) -> list[dict]:
    if expression.get("kind") == "binary" and expression.get("operator") == "&&":
        return _conjuncts(expression["left"]) + _conjuncts(expression["right"])
    return [expression]


def _strip(expression: dict) -> dict:
    while expression.get("kind") in {"borrow", "deref", "try"}:
        expression = expression["value"]
    return expression


def _chain(expression: dict) -> tuple[dict, list[dict]]:
    expression = _strip(expression)
    steps = []
    while expression.get("kind") == "method" and expression.get("method") in _ITERATORS:
        steps.append(expression)
        expression = _strip(expression["receiver"])
    return expression, list(reversed(steps))


def _closure(expression: dict) -> dict | None:
    arguments = expression.get("arguments", [])
    return arguments[0] if len(arguments) == 1 and arguments[0].get("kind") == "closure" else None


def _single(expression: dict) -> dict:
    if expression.get("kind") == "block" and len(expression.get("statements", [])) == 1:
        return _single(expression["statements"][0])
    return expression


class _Finite:
    def __init__(self, analysis: Any):
        self.a = analysis
        self.expressions: dict[str, dict] = {}
        self.documents: dict[str, Any] = {}
        self.source_nodes: dict[tuple[str, int, int], Any] = {}
        self.facts: dict[str, dict] = {}
        self.unknown: list[dict] = []
        self.operations = 0

    def gap(self, code: str, **details: Any) -> None:
        gap = {"code": code, **details}
        if gap not in self.unknown:
            self.unknown.append(gap)
            self.a.gap(code, **details)

    def fact(self, kind: str, role: str, selected_expression: dict, **details: Any) -> dict:
        span = selected_expression.get("span")
        document = self.documents[role]
        node = self.source_nodes.get((role, *(span or [])))
        if node is None:
            node = self.a.roles[role][2]
        return self.a.fact(kind, document, node, role=role,
            finite_state_component=VERSION, **details)

    def parse(self, role: str, node: Any, depth: int = 0) -> dict:
        self.operations += 1
        if self.operations > _NODE_LIMIT:
            self.a.incomplete = True
            self.gap("rust_finite_expression_budget_exceeded", operation_limit=_NODE_LIMIT)
            return {"kind": "unknown", "reason": "finite_expression_budget_exceeded"}
        if node is None or depth > 64:
            return {"kind": "unknown", "reason": "missing_or_expression_depth"}
        document = self.documents[role]
        span = [node.start_byte, node.end_byte]
        self.source_nodes[(role, *span)] = node
        def p(child):
            return self.parse(role, child, depth + 1)
        children = _children(node)
        kind = node.type
        value: dict
        if kind in _WRAPPERS and len(children) == 1:
            return p(children[0])
        if kind in {"identifier", "self", "field_identifier", "type_identifier"}:
            value = {"kind": "name", "name": document.text(node)}
        elif kind == "scoped_identifier":
            value = {"kind": "enum_or_path", "path": document.text(node).split("::")}
        elif kind == "field_expression":
            value = {"kind": "field", "value": p(_field(node, "value")),
                "field": document.text(_field(node, "field"))}
        elif kind in {"reference_expression", "try_expression"} and len(children) == 1:
            value = {"kind": "borrow" if kind == "reference_expression" else "try", "value": p(children[0])}
        elif kind == "unary_expression" and len(children) == 1:
            operator = document.data[node.start_byte:children[0].start_byte].decode("utf-8").strip()
            value = {"kind": "deref" if operator == "*" else "unary", "operator": operator, "value": p(children[0])}
        elif kind == "binary_expression":
            operator = _field(node, "operator")
            value = {"kind": "binary", "operator": document.text(operator),
                "left": p(_field(node, "left")), "right": p(_field(node, "right"))}
        elif kind == "assignment_expression":
            value = {"kind": "assignment", "left": p(_field(node, "left")),
                "right": p(_field(node, "right"))}
        elif kind == "closure_expression":
            parameters = _children(_field(node, "parameters"))
            value = {"kind": "closure", "parameters": [document.text(param) for param in parameters],
                "simple_parameters": all(param.type == "identifier" for param in parameters),
                "body": p(_field(node, "body"))}
        elif kind == "call_expression":
            function = _field(node, "function")
            arguments = [p(child) for child in _children(_field(node, "arguments"))]
            if function is not None and function.type == "field_expression":
                value = {"kind": "method", "receiver": p(_field(function, "value")),
                    "method": document.text(_field(function, "field")), "arguments": arguments}
            else:
                value = {"kind": "call", "function": document.text(function), "arguments": arguments}
        elif kind == "macro_invocation":
            value = self.macro(role, node)
        elif kind == "block":
            value = {"kind": "block", "statements": [p(child) for child in children]}
        elif kind == "if_expression":
            value = {"kind": "if", "condition": p(_field(node, "condition")),
                "consequence": p(_field(node, "consequence")), "alternative": p(_field(node, "alternative"))}
        elif kind == "let_declaration":
            pattern = _field(node, "pattern")
            value = {"kind": "let", "name": document.text(pattern),
                "simple_binding": pattern is not None and pattern.type == "identifier",
                "value": p(_field(node, "value"))}
        elif kind == "struct_expression":
            fields = {}
            body = _field(node, "body")
            for child in _children(body):
                if child.type != "field_initializer":
                    fields[document.text(child)] = {"kind": "unknown", "reason": "struct_update_or_shorthand"}
                    continue
                field = _field(child, "field")
                fields[document.text(field)] = p(_field(child, "value"))
            value = {"kind": "struct", "type": document.text(_field(node, "name")), "fields": fields}
        elif kind in {"integer_literal", "boolean_literal", "string_literal"}:
            value = {"kind": "literal", "text": document.text(node)}
        else:
            value = {"kind": "unknown", "syntax": kind, "source_text": document.text(node)[:256]}
        value["span"] = span
        return value

    def macro(self, role: str, node: Any) -> dict:
        document = self.documents[role]
        name = document.text(_field(node, "macro"))
        tree = next((child for child in _children(node) if child.type == "token_tree"), None)
        if name != "matches" or tree is None:
            return {"kind": "unknown", "syntax": "macro_invocation", "macro": name}
        # Rust token trees preserve punctuation even though pattern/expression
        # subtrees are not expanded. Accept only field paths and | enum paths.
        tokens = [document.text(child) for child in tree.children if child.type not in _IGNORED][1:-1]
        if tokens and tokens[-1] == ",":
            tokens.pop()
        if tokens.count(",") != 1:
            return {"kind": "unknown", "reason": "matches_argument_or_guard_not_finite"}
        comma = tokens.index(",")
        subject, patterns = tokens[:comma], tokens[comma + 1:]
        identifier = lambda text: text.isidentifier() or text.startswith("r#") and text[2:].isidentifier()
        if not subject or any(not identifier(text) if index % 2 == 0 else text != "."
                for index, text in enumerate(subject)) or len(subject) % 2 != 1:
            return {"kind": "unknown", "reason": "matches_subject_not_simple_field_path"}
        expression = {"kind": "name", "name": subject[0]}
        for field in subject[2::2]:
            expression = {"kind": "field", "value": expression, "field": field}
        parts, current = [], []
        for token in [*patterns, "|"]:
            if token == "|":
                if len(current) < 3 or len(current) % 2 != 1 or any(
                        not identifier(text) if index % 2 == 0 else text != "::"
                        for index, text in enumerate(current)):
                    return {"kind": "unknown", "reason": "matches_pattern_not_plain_enum_alternative"}
                parts.append(current[::2])
                current = []
            else:
                current.append(token)
        return {"kind": "enum_membership", "value": expression, "members": parts,
            "macro_resolution": "conditional_standard_matches_macro_model", "macro_expanded": False}

    def load(self) -> bool:
        missing = sorted(REQUIRED_ROLES - self.a.roles.keys())
        if missing:
            self.gap("rust_state_source_roles_missing", roles=missing)
            return False
        for role in sorted(REQUIRED_ROLES):
            document, definition, function = self.a.roles[role]
            if document.kind != "rust":
                self.gap("rust_state_non_rust_role", role=role)
                return False
            self.documents[role] = document
            if role == "validator":
                continue
            expression = self.parse(role, _field(function, "body"))
            self.expressions[role] = expression
            self.facts[role] = self.fact("rust_finite_selected_source_expression", role, expression,
                expression=expression, source_selector={"file": document.source.path, "symbol": definition.symbol},
                target_function_executed=False)
        return True

    def iterations(self) -> dict[str, list[dict]]:
        result = {}
        for role, body in self.expressions.items():
            values = []
            for expression in _walk(body):
                if expression.get("kind") != "method" or expression.get("method") not in {"collect", "find", "any"}:
                    continue
                origin, steps = _chain(expression)
                record = self.fact("rust_finite_iterator_relation", role, expression,
                    origin_expression=origin, steps=steps,
                    eager_predicate_execution_proven=False,
                    interpretation="conditional standard slice/Vec iterator and HashSet source model")
                values.append(record)
            result[role] = values
        return result

    def validator_memberships(self) -> list[dict]:
        document, _, function = self.a.roles["validator"]
        result = []
        for node in self.a.nodes(document, _field(function, "body"), nested=True):
            if node.type != "macro_invocation":
                continue
            expression = self.parse("validator", node)
            if expression.get("kind") != "enum_membership":
                continue
            result.append(self.fact("rust_finite_validator_enum_predicate_source", "validator", expression,
                expression=expression, compared_to_selection_membership_as_distinct_predicate=True,
                predicate_purpose_or_all_validator_transitions_proven=False))
        return result

    def _helper(self, role: str, expression: dict, owner_role: str) -> bool:
        document, definition, function = self.a.roles[role]
        name = document.text(_field(function, "name"))
        owner_document = self.documents[owner_role]
        if expression.get("kind") != "call" or expression.get("function") != name or document is not owner_document:
            return False
        # Only unique module-local free declarations; no receiver/trait guesses.
        definitions = document.definitions.get(name, [])
        return len(definitions) == 1 and definitions[0] is definition

    def parameters(self, role: str) -> list[str] | None:
        document, _, function = self.a.roles[role]
        parameters = _children(_field(function, "parameters"))
        result = []
        for parameter in parameters:
            if parameter.type == "self_parameter":
                result.append("self")
                continue
            pattern = _field(parameter, "pattern")
            if pattern is None or pattern.type != "identifier":
                return None
            result.append(document.text(pattern))
        return result

    def finite_table(self) -> dict:
        runnable = _single(self.expressions["runnable"])
        effective = _single(self.expressions["effective_state"])
        equality = runnable if runnable.get("kind") == "binary" and runnable.get("operator") == "==" else {}
        call = equality.get("left", {})
        expected = equality.get("right", {})
        if expected.get("kind") != "enum_or_path":
            call, expected = expected, call
        if not self._helper("effective_state", call, "runnable") or expected.get("kind") != "enum_or_path":
            self.gap("rust_runnable_effective_state_comparison_not_closed")
            return {"supported": False}
        runnable_parameters = self.parameters("runnable")
        effective_parameters = self.parameters("effective_state")
        argument_paths = [_path(argument) for argument in call.get("arguments", [])]
        if (not runnable_parameters or not effective_parameters or len(runnable_parameters) != len(effective_parameters)
                or argument_paths != [(parameter,) for parameter in runnable_parameters]):
            self.gap("rust_runnable_to_effective_parameter_identity_unknown")
            return {"supported": False}
        if effective.get("kind") != "if":
            self.gap("rust_effective_state_not_finite_if_expression")
            return {"supported": False}
        memberships = [expr for expr in _walk(effective["condition"]) if expr.get("kind") == "enum_membership"]
        if len(memberships) != 1:
            self.gap("rust_effective_state_subject_not_unique")
            return {"supported": False}
        state_path = _path(memberships[0]["value"])
        enum_prefix = expected["path"][:-1]
        variants = sorted({"::".join(expr["path"]) for expr in _walk(effective)
            if expr.get("kind") == "enum_or_path" and expr["path"][:-1] == enum_prefix}
            | {"::".join(member) for expr in _walk(effective) if expr.get("kind") == "enum_membership"
                for member in expr["members"] if member[:-1] == enum_prefix}
            | {"::".join(expected["path"])})
        atom_expressions = []
        def atoms(expr):
            if not isinstance(expr, dict):
                return
            if expr.get("kind") == "method" and expr.get("method") in {"any", "all"}:
                atom_expressions.append(expr)
                return
            for value in expr.values():
                if isinstance(value, dict):
                    atoms(value)
                elif isinstance(value, list):
                    for child in value:
                        atoms(child)
        atoms(effective)
        unique_atoms = {tuple(expr["span"]): expr for expr in atom_expressions}
        if not state_path or not variants or len(variants) > 32 or len(unique_atoms) > 3:
            self.gap("rust_finite_state_domain_budget_or_subject_unknown")
            return {"supported": False}
        def evaluate(expr, state, values):
            kind = expr.get("kind")
            if tuple(expr.get("span", [])) in values:
                return values[tuple(expr["span"])]
            if _path(expr) == state_path:
                return state
            if kind == "enum_or_path":
                return "::".join(expr["path"])
            if kind == "enum_membership":
                return evaluate(expr["value"], state, values) in ["::".join(member) for member in expr["members"]]
            if kind == "binary":
                left = evaluate(expr["left"], state, values)
                right = evaluate(expr["right"], state, values)
                if expr["operator"] == "==":
                    return left == right
                if expr["operator"] == "!=":
                    return left != right
                if expr["operator"] == "&&" and type(left) is bool and type(right) is bool:
                    return left and right
                if expr["operator"] == "||" and type(left) is bool and type(right) is bool:
                    return left or right
            if kind == "unary" and expr.get("operator") == "!":
                value = evaluate(expr["value"], state, values)
                if type(value) is bool:
                    return not value
            if kind == "if":
                condition = evaluate(expr["condition"], state, values)
                if type(condition) is bool:
                    return evaluate(expr["consequence"] if condition else expr["alternative"], state, values)
            if kind == "block" and len(expr["statements"]) == 1:
                return evaluate(expr["statements"][0], state, values)
            if kind == "method" and expr["method"] == "clone" and not expr["arguments"]:
                return evaluate(expr["receiver"], state, values)
            raise ValueError("unsupported finite expression " + str(kind))
        atom_names = ["source_quantifier_" + str(index + 1) for index in range(len(unique_atoms))]
        rows = []
        try:
            for state, bools in product([*variants, _OTHER], product([False, True], repeat=len(unique_atoms))):
                values = dict(zip(unique_atoms, bools))
                output = evaluate(effective, state, values)
                if not isinstance(output, str):
                    raise ValueError("effective state output is not a finite enum value")
                rows.append({"input_state": state, "source_quantifiers": dict(zip(atom_names, bools)),
                    "effective_state": output, "runnable": output == "::".join(expected["path"])})
        except ValueError as error:
            self.gap("rust_effective_state_interpreter_unknown", reason=str(error))
            return {"supported": False}
        fact = self.fact("rust_finite_effective_state_table", "effective_state", effective,
            state_field_path=list(state_path), state_values_from_captured_expressions=variants,
            other_state_is_symbolic_complement=True, full_enum_declaration_enumerated=False,
            symbolic_quantifiers=[{"name": name, "expression": expr} for name, expr in zip(atom_names, unique_atoms.values())],
            runnable_equals_captured_state=expected, rows=rows,
            helper_parameter_slots={"runnable": runnable_parameters, "effective": effective_parameters,
                "call_argument_paths": argument_paths},
            actual_item_values_or_dependency_results_known=False)
        return {"supported": True, "fact_id": fact["id"], "rows": rows,
            "symbolic_quantifiers": fact["symbolic_quantifiers"], "state_field_path": list(state_path),
            "runnable_equals": "::".join(expected["path"]), "full_enum_enumeration": False}

    def dependency(self) -> dict:
        body = self.expressions["effective_state"]
        candidates = []
        for outer in _walk(body):
            if outer.get("kind") != "method" or outer.get("method") != "any":
                continue
            outer_closure = _closure(outer)
            if not outer_closure or not outer_closure["simple_parameters"] or len(outer_closure["parameters"]) != 1:
                continue
            predicate = _single(outer_closure["body"])
            if predicate.get("kind") != "unary" or predicate.get("operator") != "!":
                continue
            inner = predicate["value"]
            inner_closure = _closure(inner)
            if inner.get("kind") != "method" or inner.get("method") != "any" or not inner_closure:
                continue
            clauses = _conjuncts(_single(inner_closure["body"]))
            if len(clauses) != 2 or any(clause.get("kind") != "binary" or clause.get("operator") != "==" for clause in clauses):
                continue
            identity, completed = None, None
            for clause in clauses:
                left, right = _strip(clause["left"]), _strip(clause["right"])
                if _path(left) == (outer_closure["parameters"][0],):
                    left, right = right, left
                if _path(right) == (outer_closure["parameters"][0],):
                    identity = {"candidate_key": _path(left), "dependency_value": _path(right)}
                elif left.get("kind") == "enum_or_path" or right.get("kind") == "enum_or_path":
                    if left.get("kind") == "enum_or_path":
                        left, right = right, left
                    completed = {"candidate_state": _path(left), "accepted_state": right.get("path")}
            origin, steps = _chain(outer["receiver"])
            pool, pool_steps = _chain(inner["receiver"])
            if identity and completed and origin.get("kind") == "field" and len(steps) == len(pool_steps) == 1 and steps[0]["method"] == pool_steps[0]["method"] == "iter":
                fact = self.fact("rust_finite_dependency_blocker_relation", "effective_state", outer,
                    dependency_collection=origin, candidate_collection=pool, identity_comparison=identity,
                    required_candidate_state_comparison=completed,
                    quantifier="exists dependency for which no equal-identity candidate has the captured required state",
                    empty_dependency_collection_result=False, actual_dependencies_or_reachability_evaluated=False)
                candidates.append(fact)
        if len(candidates) != 1:
            self.gap("rust_finite_dependency_relation_not_unique", candidate_count=len(candidates))
        return {"supported": len(candidates) == 1, "relations": candidates}

    def guards(self, iterations: dict) -> dict:
        aggregate = self.expressions["aggregate_selector"]
        item = self.expressions["item_selector"]
        selector = self.expressions["selector"]
        statements = aggregate.get("statements", [])
        active_lets = [stmt for stmt in statements if stmt.get("kind") == "let" and _chain(stmt["value"])[1]
            and _chain(stmt["value"])[1][-1]["method"] == "collect"]
        find_records = {}
        for role in ("item_selector", "selector"):
            records = [record for record in iterations[role] if record["steps"][-1]["method"] == "find"]
            find_records[role] = records
        if len(active_lets) != 1 or any(len(values) != 1 for values in find_records.values()):
            self.gap("rust_state_selection_collection_or_find_not_unique")
            return {"supported": False}
        active = active_lets[0]
        origin, steps = _chain(active["value"])
        if [step["method"] for step in steps] != ["iter", "filter", "map", "collect"]:
            self.gap("rust_state_active_collection_pipeline_unknown")
            return {"supported": False}
        filter_closure, map_closure = _closure(steps[1]), _closure(steps[2])
        if not filter_closure or not map_closure:
            self.gap("rust_state_active_pipeline_closures_unknown")
            return {"supported": False}
        membership = _single(filter_closure["body"])
        if membership.get("kind") != "enum_membership":
            self.gap("rust_state_active_filter_not_finite_membership")
            return {"supported": False}
        map_key = _path(_single(map_closure["body"]))
        item_find = find_records["item_selector"][0]
        selector_find = find_records["selector"][0]
        item_predicate = _closure(item_find["steps"][-1])
        selector_predicate = _closure(selector_find["steps"][-1])
        if not item_predicate or not selector_predicate or not map_key:
            self.gap("rust_state_find_predicate_or_map_key_unknown")
            return {"supported": False}
        item_expression = _single(item_predicate["body"])
        selector_expression = _single(selector_predicate["body"])
        active_exclusions = [clause for clause in _conjuncts(item_expression) if clause.get("kind") == "unary"
            and clause.get("operator") == "!" and clause.get("value", {}).get("kind") == "method"
            and clause["value"].get("method") == "any"]
        if len(active_exclusions) != 1:
            self.gap("rust_state_item_active_exclusion_not_unique")
            return {"supported": False}
        active_any = active_exclusions[0]["value"]
        active_closure = _closure(active_any)
        any_origin, any_steps = _chain(active_any["receiver"])
        active_memberships = [expr for expr in _walk(active_closure["body"] if active_closure else {}) if expr.get("kind") == "enum_membership"]
        active_equalities = [expr for expr in _conjuncts(_single(active_closure["body"]))
            if expr.get("kind") == "binary" and expr.get("operator") == "=="] if active_closure else []
        same_states = len(active_memberships) == 1 and sorted(active_memberships[0]["members"]) == sorted(membership["members"])
        filter_state = _path(membership.get("value", {}))
        exclusion_state = _path(active_memberships[0].get("value", {})) if len(active_memberships) == 1 else None
        state_subject_closed = bool(filter_state and exclusion_state and filter_closure["parameters"] == [filter_state[0]]
            and active_closure and active_closure["parameters"] == [exclusion_state[0]] and filter_state[1:] == exclusion_state[1:])
        key_relative = map_key[1:] if map_closure["parameters"] == [map_key[0]] else None
        equality_key = None
        equality_id = None
        if len(active_equalities) == 1 and active_closure and len(active_closure["parameters"]) == 1:
            equality = active_equalities[0]
            left, right = _path(equality["left"]), _path(equality["right"])
            param = active_closure["parameters"][0]
            if right and right[0] == param:
                left, right = right, left
            if left and left[0] == param:
                equality_key, equality_id = left[1:], right
        same_origin = _path(origin) == _path(any_origin) and [step["method"] for step in any_steps] == ["iter"]
        key_closed = bool(key_relative and key_relative == equality_key and equality_id)
        exact_id_clauses = [clause for clause in _conjuncts(item_expression) if clause.get("kind") == "binary" and clause.get("operator") == "=="]
        exact_item_id = False
        item_key = None
        if len(exact_id_clauses) == 1 and len(item_predicate["parameters"]) == 1:
            left, right = _path(exact_id_clauses[0]["left"]), _path(exact_id_clauses[0]["right"])
            if right and right[0] == item_predicate["parameters"][0]:
                left, right = right, left
            if left and left[0] == item_predicate["parameters"][0]:
                item_key = left[1:]
                exact_item_id = bool(right and right == equality_id)
        helper_calls = {}
        runnable_argument_checks = {}
        for role, predicate in (("item_selector", item_expression), ("selector", selector_expression)):
            helper_calls[role] = [expr for expr in _conjuncts(predicate) if self._helper("runnable", expr, role)]
            closure = item_predicate if role == "item_selector" else selector_predicate
            record = item_find if role == "item_selector" else selector_find
            runnable_argument_checks[role] = bool(len(helper_calls[role]) == 1
                and len(closure["parameters"]) == 1 and closure["simple_parameters"]
                and [_path(arg) for arg in helper_calls[role][0]["arguments"]] == [
                    (closure["parameters"][0],), _path(record["origin_expression"])])
        runnable_selected = all(runnable_argument_checks.values())
        # Selection helper receives the collected active IDs in a real struct
        # field; its negated contains must reference that field and selected ID.
        selection_calls = [stmt for stmt in statements if stmt.get("kind") == "let" and self._helper("selector", _strip(stmt["value"]), "aggregate_selector")]
        transfer = None
        if len(selection_calls) == 1:
            chosen = selection_calls[0]
            call = _strip(chosen["value"])
            structs = [_strip(arg) for arg in call["arguments"] if _strip(arg).get("kind") == "struct"]
            if len(structs) == 1:
                matching = [field for field, value in structs[0]["fields"].items() if _path(value) == (active["name"],)]
                contains = [expr["value"] for expr in _conjuncts(selector_expression) if expr.get("kind") == "unary"
                    and expr.get("operator") == "!" and expr.get("value", {}).get("kind") == "method"
                    and expr["value"].get("method") == "contains"]
                final = _single(statements[-1]) if statements else {}
                method = self.a.roles["item_selector"][1].symbol.rsplit(".", 1)[-1]
                if len(matching) == 1 and len(contains) == 1 and final.get("kind") == "method" and final.get("method") == method and _path(final["receiver"]) == ("self",):
                    transfer = {"active_local_binding": active["name"], "active_struct_field": matching[0],
                        "membership_receiver": _path(contains[0]["receiver"]),
                        "membership_argument": [_path(arg) for arg in contains[0]["arguments"]],
                        "selected_local_binding": chosen["name"],
                        "selected_recheck_arguments": [_path(arg) for arg in final["arguments"]],
                        "same_active_struct_field": bool(_path(contains[0]["receiver"]) and _path(contains[0]["receiver"])[-1] == matching[0]),
                        "same_selected_result_root": len(final["arguments"]) == 1 and bool(_path(final["arguments"][0])) and _path(final["arguments"][0])[0] == chosen["name"],
                        "same_item_collection_argument": bool(call["arguments"] and _path(call["arguments"][0]) == _path(item_find["origin_expression"]))}
                    # Recover returned selection identity through plain local
                    # clones and a record field; unrelated state assignments
                    # cannot silently replace the selected identity.
                    selector_statements = selector.get("statements", [])
                    selector_bindings = {stmt["name"]: stmt for stmt in selector_statements if stmt.get("kind") == "let" and stmt.get("simple_binding")}
                    selector_binding_names = [stmt["name"] for stmt in selector_statements if stmt.get("kind") == "let"]
                    selected_bindings = [stmt for stmt in selector_statements if stmt.get("kind") == "let"
                        and any(expr.get("span") == selector_find["steps"][-1].get("span") for expr in _walk(stmt["value"]))]
                    final_args = final.get("arguments", [])
                    recheck = _path(final_args[0]) if len(final_args) == 1 else None
                    contains_args = contains[0].get("arguments", [])
                    contains_key = _path(contains_args[0]) if len(contains_args) == 1 else None
                    selector_tail = selector_statements[-1] if selector_statements else {}
                    result_structs = [expr for expr in selector_tail.get("arguments", []) if expr.get("kind") == "struct"] if selector_tail.get("kind") == "call" and selector_tail.get("function") == "Ok" else []
                    returned_path = None
                    if recheck and len(recheck) >= 3 and len(result_structs) == 1:
                        returned_path = _path(result_structs[0]["fields"].get(recheck[1], {}))
                    resolved_path = returned_path
                    visited = set()
                    while resolved_path and resolved_path[0] in selector_bindings and resolved_path[0] not in visited:
                        visited.add(resolved_path[0])
                        bound = selector_bindings[resolved_path[0]]["value"]
                        target = _path(bound)
                        if not target:
                            break
                        resolved_path = (*target, *resolved_path[1:])
                    selected_name = selected_bindings[0]["name"] if len(selected_bindings) == 1 else None
                    return_identity_closed = bool(recheck and contains_key and len(selected_bindings) == 1
                        and resolved_path == (selected_name,) and len(recheck[2:]) == 1
                        and contains_key == (selector_predicate["parameters"][0], recheck[-1]))
                    changed_identity_fields = [expr for expr in _walk(selector) if expr.get("kind") == "assignment"
                        and (left := _path(expr["left"])) and left[0] in visited | {selected_name}
                        and recheck and (len(left) == 1 or left[-1] == recheck[-1])]
                    transfer["selector_return_identity"] = {"selected_binding": selected_name,
                        "returned_record_field_path": returned_path, "resolved_selected_path": resolved_path,
                        "contains_selected_key": contains_key, "rechecked_result_key": recheck,
                        "identity_field_assignments": changed_identity_fields,
                        "closed_under_plain_selected_clone_source_model": return_identity_closed and not changed_identity_fields}
                    transfer["same_selected_result_identity"] = return_identity_closed and not changed_identity_fields and len(selector_binding_names) == len(set(selector_binding_names))
                    transfer["selected_id_matches_exact_item_key"] = bool(recheck and tuple(recheck[2:]) == item_key)
                    transfer["active_key_matches_contains_selected_item_key"] = bool(contains_key and tuple(contains_key[1:]) == item_key)
                    transfer["source_statement_pipeline_order_closed"] = bool(len(statements) == 4
                        and statements[1] is active and statements[2] is chosen and statements[-1] is final)
        guard_records = []
        validator_name = self.a.roles["validator"][1].symbol.rsplit(".", 1)[-1]
        for role, expression in (("aggregate_selector", aggregate), ("item_selector", item)):
            top = expression.get("statements", [])
            first = top[0] if top else {}
            candidate = first.get("value", {}) if first.get("kind") == "try" else {}
            closed = (candidate.get("kind") == "method" and candidate.get("method") == validator_name
                and _path(candidate["receiver"]) == ("self",) and not candidate["arguments"])
            guard_records.append(self.fact("rust_finite_selection_validation_prefix", role, first or expression,
                first_statement=first, selected_validator_symbol=self.a.roles["validator"][1].symbol,
                normal_continuation_requires_ok=closed, validator_entire_semantics_proven=False))
        checks = {"same_active_state_alternatives": same_states,
            "same_persisted_run_collection": same_origin, "same_projected_item_identity_field": key_closed,
            "same_state_field_on_actual_filter_and_exclusion_elements": state_subject_closed,
            "active_exclusion_key_equals_exact_find_requested_id": exact_item_id,
            "runnable_predicate_in_both_find_conjunctions": runnable_selected,
            "active_collection_passed_to_selector_and_selected_id_rechecked": bool(transfer and transfer["same_active_struct_field"] and transfer["same_selected_result_root"]
                and transfer["same_item_collection_argument"] and transfer.get("same_selected_result_identity")),
            "selected_result_and_active_membership_share_exact_item_key": bool(transfer
                and transfer.get("selected_id_matches_exact_item_key") and transfer.get("active_key_matches_contains_selected_item_key")),
            "aggregate_validation_collect_select_recheck_source_order": bool(transfer and transfer.get("source_statement_pipeline_order_closed")),
            "both_selected_entries_have_fallible_validation_prefix": all(record["normal_continuation_requires_ok"] for record in guard_records)}
        for check, supported in checks.items():
            if not supported:
                self.gap("rust_finite_selection_relation_unclosed", relation=check)
        relation = self.fact("rust_finite_selection_comparison", "aggregate_selector", aggregate,
            active_members=membership["members"], active_origin=origin, projected_key=map_key,
            item_find_fact_id=item_find["id"], selector_find_fact_id=selector_find["id"],
            active_id_comparison=equality_id, actual_transfer=transfer, checks=checks,
            runnable_argument_identity_checks=runnable_argument_checks,
            helper_call_binding="unique selected same-module source declarations; conditional standard source model; no CALLS promotion",
            unknown_dynamic_dispatch_or_macro_expansion_repaired=False)
        return {"supported": all(checks.values()), "fact_id": relation["id"], "checks": checks,
            "active_members": membership["members"], "transfer": transfer,
            "validation_prefixes": guard_records,
            "find_predicate_source_facts": {role: values[0]["id"] for role, values in find_records.items()},
            "active_collection_computed_from_persisted_runs": same_origin,
            "all_enum_states_or_attempts_proven": False}


def analyze_pattern(analysis: Any) -> dict:
    """Return source pattern; append authenticated facts/gaps to report analysis.

    Expected source roles are REQUIRED_ROLES. The caller registers MODEL and
    validates the ordinary source-only locator rule; no expected enum members,
    paths, predicates, truth-table rows or success flags are accepted in rules.
    """
    finite = _Finite(analysis)
    if MODEL not in analysis.rule.get("models", []):
        finite.gap("rust_finite_source_model_not_registered", required_model=MODEL)
        return {"version": VERSION, "scoped_source_supported": False}
    if not finite.load():
        return {"version": VERSION, "scoped_source_supported": False}
    iterations = finite.iterations()
    validator_memberships = finite.validator_memberships()
    table = finite.finite_table()
    dependency = finite.dependency()
    selection = finite.guards(iterations)
    table_quantifiers = table.get("symbolic_quantifiers", [])
    dependency_relations = dependency.get("relations", [])
    quantifier_linked = bool(len(table_quantifiers) == len(dependency_relations) == 1
        and table_quantifiers[0]["expression"].get("span") == [
            dependency_relations[0]["location"]["start_byte"], dependency_relations[0]["location"]["end_byte"]])
    if not quantifier_linked:
        finite.gap("rust_finite_state_table_dependency_quantifier_not_closed")
    supported = bool(table.get("supported") and dependency.get("supported") and selection.get("supported")
        and not finite.unknown and not analysis.incomplete)
    return {"version": VERSION, "trusted_model": MODEL,
        "finite_effective_state_relation": table, "dependency_blocker_relation": dependency,
        "state_table_dependency_quantifier_linked": quantifier_linked,
        "persisted_selection_recheck_relation": selection,
        "validator_enum_predicate_source_fact_ids": [fact["id"] for fact in validator_memberships],
        "finite_source_countercases": {"non_runnable_table_rows": [row for row in table.get("rows", []) if row.get("runnable") is False],
            "runnable_table_rows": [row for row in table.get("rows", []) if row.get("runnable") is True],
            "selection_active_members": selection.get("active_members", []),
            "validator_predicates_remain_distinct": [fact.get("expression") for fact in validator_memberships],
            "countercases_are_symbolic_source_conditions_not_observed_runtime_records": True},
        "iterator_relation_fact_ids": {role: [record["id"] for record in records] for role, records in iterations.items()},
        "scoped_source_supported": supported, "all_active_states_or_attempts_proven": False,
        "whole_domain_state_machine_closed": False, "runtime_schedule_or_termination_proven": False,
        "graph_calls_repaired_or_promoted": False,
        "source_model_conditions": ["selected normal source bodies are reached and their fallible prefixes return Ok",
            "captured plain matches! uses the standard Rust macro, not an external macro override",
            "captured Vec/slice iterator, HashSet membership, field equality and Clone obey their standard source contracts",
            "the recorded unique same-module helper source declarations are the invoked helpers; historical unresolved graph calls remain unchanged"],
        "boundaries": ["source-mentioned enum alternatives and a symbolic complement are interpreted; no complete enum declaration or arbitrary macro expansion is inferred",
            "quantifiers describe current captured predicates; concrete item records, dependency truth and actual active runs are unknown",
            "selection does not prove persistence, scheduling fairness, concurrency isolation, all state transitions or every attempt identity"],
        "expression_budget": {"operations": finite.operations, "limit": _NODE_LIMIT,
            "incomplete": finite.operations > _NODE_LIMIT},
        "necessary_gaps": finite.unknown}
