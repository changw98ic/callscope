"""Agent admission, child environment and sandbox source-policy relations.

The report-chain analysis supplies authenticated source roles and call facts.
All predicates, assignments, argument bindings and launch forms below come
from those AST nodes. They do not certify a provider, secret boundary, actual
subprocess, sandbox implementation, native isolation or deployment.
"""
from __future__ import annotations

from typing import Any

from .semantic_sources import unwrap
from .static_contracts import _literal_string

VERSION = "captured-agent-execution-policy-1"
CONTROL_MODEL = "captured-normal-statement-control-v1"
REQUIRED_ROLES = frozenset({"runner", "allowlist", "pool_guard", "phase_policy",
    "readonly_check", "failure_classifier", "child_builder", "child_filter",
    "child_predicate", "child_keys", "provider_credentials", "sandbox_mode",
    "sandbox_policy", "sandbox_launcher", "executable_roots", "acp_child",
    "acp_terminal", "acp_env_projection"})
_ERASED = {"comment", "type_annotation", "type_arguments", "type_parameters", "type_query"}
_FUNCTIONS = {"function_declaration", "function_expression", "arrow_function", "method_definition",
              "generator_function_declaration", "generator_function"}


def _field(node: Any, name: str) -> Any:
    return node.child_by_field_name(name) if node is not None else None


def _children(node: Any) -> list[Any]:
    return [child for child in node.named_children if child.type not in _ERASED and not child.type.endswith("_type")] if node is not None else []


def _arguments(node: Any) -> list[Any]:
    return _children(_field(node, "arguments"))


def _inside(outer: Any, inner: Any) -> bool:
    return bool(outer is not None and inner is not None and outer.start_byte <= inner.start_byte < outer.end_byte)


def _key(document: Any, node: Any) -> str | None:
    node = unwrap(node)
    if node is None:
        return None
    if node.type in {"identifier", "property_identifier", "shorthand_property_identifier", "shorthand_property_identifier_pattern"}:
        name = document.text(node)
        return name if name and "\\" not in name else None
    return _literal_string(document.text(node)) if node.type == "string" else None


def _member(document: Any, original: Any) -> tuple[Any, str | None]:
    node = unwrap(original)
    if node is None or node.type not in {"member_expression", "subscript_expression"}:
        return None, None
    receiver = unwrap(_field(node, "object"))
    property = _field(node, "property") if node.type == "member_expression" else _field(node, "index")
    return receiver, _key(document, property) if node.type == "member_expression" or property is not None and property.type == "string" else None


def _path(document: Any, original: Any) -> list[str] | None:
    node = unwrap(original)
    if node is None:
        return None
    if node.type in {"identifier", "shorthand_property_identifier", "this"}:
        return [document.text(node)]
    receiver, property = _member(document, node)
    prefix = _path(document, receiver)
    return [*prefix, property] if prefix and property else None


def _operator(document: Any, node: Any) -> str:
    return document.text(_field(node, "operator")) if node is not None else ""


def _record(analysis: Any, document: Any, node: Any) -> dict:
    node = unwrap(node)
    if node is None or node.type not in {"identifier", "shorthand_property_identifier", "shorthand_property_identifier_pattern"}:
        return {}
    return analysis.lexical(document).resolve(node)


def _same(analysis: Any, document: Any, first: Any, second: Any) -> bool:
    return analysis.lexical(document).same(_record(analysis, document, first), _record(analysis, document, second))


def _initializer_binding(node: Any) -> Any:
    current = node.parent
    while current is not None:
        if current.type in _FUNCTIONS:
            return None
        if current.type == "variable_declarator" and _inside(_field(current, "value"), node):
            return current
        current = current.parent
    return None


def _statement(node: Any, body: Any) -> Any:
    current = node
    while current is not None and current.parent != body:
        if current.parent is None or current.parent.type in _FUNCTIONS:
            return None
        current = current.parent
    return current if current is not None and current.parent == body else None


def _own_statement(node: Any) -> tuple[Any, Any] | None:
    current = node
    while current is not None and current.parent is not None:
        if current.parent.type == "statement_block":
            return current.parent, current
        if current.parent.type in _FUNCTIONS:
            return None
        current = current.parent
    return None


def _returns(analysis: Any, document: Any, root: Any) -> list[Any]:
    return [node for node in analysis.nodes(document, root) if node.type == "return_statement"]


def _returned_expression(node: Any) -> Any:
    children = _children(node)
    return unwrap(children[0]) if len(children) == 1 else None


def _object(document: Any, original: Any) -> dict[str, Any] | None:
    node = unwrap(original)
    if node is None or node.type != "object":
        return None
    fields = {}
    for item in _children(node):
        if item.type == "pair":
            key, value = _key(document, _field(item, "key")), _field(item, "value")
        elif item.type == "shorthand_property_identifier":
            key, value = _key(document, item), item
        else:
            return None
        if key is None or key in fields or key == "__proto__":
            return None
        fields[key] = value
    return fields


def _literal_values(value: Any) -> set[str]:
    result = set()
    pending = [value]
    while pending:
        item = pending.pop()
        if isinstance(item, dict):
            if isinstance(item.get("literal"), str):
                result.add(item["literal"])
            pending.extend(item.values())
        elif isinstance(item, list):
            pending.extend(item)
    return result


def _actual_calls(analysis: Any, role: str, target_role: str) -> list[dict]:
    target = analysis.roles[target_role][1].graph_node_id
    return [call for call in analysis.calls_by_role.get(role, []) if call.get("actual_callee_graph_node_id") == target]


def _unique_call(analysis: Any, role: str, target_role: str) -> dict | None:
    calls = _actual_calls(analysis, role, target_role)
    if len(calls) != 1:
        analysis.gap("agent_policy_actual_call_not_unique", role=role, target_role=target_role,
                     matching_authenticated_calls=len(calls))
        return None
    return calls[0]


def _node(analysis: Any, call: dict) -> Any:
    return analysis.call_nodes[call["id"]][2]


def _binding_identifier(analysis: Any, call: dict) -> Any:
    declaration = _initializer_binding(_node(analysis, call))
    return _field(declaration, "name")


def _spawn_import(analysis: Any, document: Any, node: Any) -> dict | None:
    callee = unwrap(_field(node, "function"))
    record = _record(analysis, document, callee)
    if record.get("state") != "unique" or not record.get("identity_complete"):
        return None
    declaration = analysis.lexical(document).declaration_for(record)
    current, specifier = declaration, None
    while current is not None:
        if current.type == "import_specifier":
            specifier = current
        if current.type == "import_statement":
            source = _literal_string(document.text(_field(current, "source")))
            imported = _key(document, _field(specifier, "name")) if specifier is not None else None
            if source == "node:child_process" and imported == "spawn":
                return {"declaration_id": record["declaration_id"], "source_specifier": source,
                        "imported_member": imported, "import_location": document.location(current),
                        "external_module_implementation_verified": False}
            return None
        current = current.parent
    return None


def _guard_records(analysis: Any, role: str) -> list[dict]:
    document, _, function = analysis.roles[role]
    result = []
    for guard in analysis.nodes(document, _field(function, "body")):
        if guard.type != "if_statement":
            continue
        result.append(analysis.fact("agent_policy_source_branch", document, guard, role=role,
            condition=analysis.expression(document, _field(guard, "condition")),
            then_returns=[analysis.expression(document, node) for node in _returns(analysis, document, _field(guard, "consequence"))],
            else_returns=[analysis.expression(document, node) for node in _returns(analysis, document, _field(guard, "alternative"))],
            then_abrupt=analysis.simple_abrupt(_field(guard, "consequence")),
            else_abrupt=analysis.simple_abrupt(_field(guard, "alternative")),
            runtime_branch_selected=False))
    return result


def _admission(analysis: Any) -> dict:
    document, _, function = analysis.roles["runner"]
    allow_call = _unique_call(analysis, "runner", "allowlist")
    pool_call = _unique_call(analysis, "runner", "pool_guard")
    if allow_call is None or pool_call is None:
        return {"supported": False}
    allowed, pool = _binding_identifier(analysis, allow_call), _binding_identifier(analysis, pool_call)
    executes = []
    for call in analysis.calls_by_role["runner"]:
        call_node = _node(analysis, call)
        receiver, member = _member(document, _field(call_node, "function"))
        if member == "execute" and _same(analysis, document, receiver, pool):
            executes.append(call)
    if len(executes) != 1:
        analysis.gap("agent_policy_execute_receiver_unknown", matching_source_calls=len(executes))
        return {"supported": False}
    execute = executes[0]
    execute_node = _node(analysis, execute)
    execute_args = _arguments(execute_node)
    guards = []
    body = _field(function, "body")
    execute_statement = _statement(execute_node, body)
    for guard in _children(body):
        if guard.type != "if_statement" or execute_statement is None or guard.end_byte >= execute_statement.start_byte:
            continue
        condition = unwrap(_field(guard, "condition"))
        if condition is None or condition.type != "binary_expression" or _operator(document, condition) != "&&":
            continue
        nonnull, denial = unwrap(_field(condition, "left")), unwrap(_field(condition, "right"))
        if nonnull is None or nonnull.type != "binary_expression" or _operator(document, nonnull) != "!==":
            continue
        if (not _same(analysis, document, _field(nonnull, "left"), allowed)
                or unwrap(_field(nonnull, "right")).type != "null"
                or denial is None or denial.type != "unary_expression" or _operator(document, denial) != "!"):
            continue
        includes = unwrap(_field(denial, "argument"))
        receiver, method = _member(document, _field(includes, "function"))
        args = _arguments(includes) if includes is not None and includes.type == "call_expression" else []
        if (method != "includes" or not _same(analysis, document, receiver, allowed) or len(args) != 1 or not execute_args
                or not _same(analysis, document, args[0], execute_args[0])
                or not analysis.simple_abrupt(_field(guard, "consequence"))):
            continue
        returns = _returns(analysis, document, _field(guard, "consequence"))
        result = _object(document, _returned_expression(returns[0])) if len(returns) == 1 else None
        if result is None or "ok" not in result or unwrap(result["ok"]).type != "false":
            continue
        guards.append((guard, result))
    if len(guards) != 1:
        analysis.gap("agent_policy_allowlist_abrupt_guard_unknown", matching_guard_count=len(guards))
        return {"supported": False}
    guard, rejection = guards[0]
    allow_document, _, allow_function = analysis.roles["allowlist"]
    policy_returns = [analysis.expression(allow_document, node) for node in _returns(analysis, allow_document, _field(allow_function, "body"))]
    pool_document, _, pool_function = analysis.roles["pool_guard"]
    fact = analysis.fact("agent_allowlist_binding_rejects_before_injected_pool_execute", document, guard,
        allowlist_call_fact_id=allow_call["id"], pool_shape_call_fact_id=pool_call["id"],
        execute_call_fact_id=execute["id"], allowed_binding=analysis.identity(document, allowed),
        injected_pool_binding=analysis.identity(document, pool),
        agent_argument=analysis.expression(document, execute_args[0]),
        rejection_fields={key: analysis.expression(document, value) for key, value in rejection.items()},
        normal_reaching_excludes_rejection_branch=True, model_id=CONTROL_MODEL,
        allowlist_source_returns=policy_returns,
        pool_shape_source_guards=_guard_records(analysis, "pool_guard"),
        pool_shape_source_location=pool_document.location(pool_function),
        unique_pool_implementation_proven=False,
        actual_pool_method_value_or_runtime_type_proven=False,
        original_execute_binding_state=execute["binding_state"],
        policy_absence_and_malformed_input_are_distinct_source_branches=True)
    readonly = _unique_call(analysis, "runner", "readonly_check")
    classified = _unique_call(analysis, "runner", "failure_classifier")
    post_order = False
    if readonly is not None:
        before, after = _own_statement(execute_node), _own_statement(_node(analysis, readonly))
        post_order = bool(before and after and before[0] == after[0] and before[1].end_byte <= after[1].start_byte)
    if not post_order or classified is None:
        analysis.gap("agent_policy_post_execution_review_chain_unknown")
    else:
        analysis.fact("agent_execution_then_readonly_audit_and_catch_classification", document, _node(analysis, readonly),
            execute_call_fact_id=execute["id"], readonly_call_fact_id=readonly["id"], classifier_call_fact_id=classified["id"],
            same_try_body_source_statement_order=True,
            readonly_guard_returns=_guard_records(analysis, "readonly_check"),
            catch_classifier_branch_context=classified["branch_context"],
            audit_file_or_external_agent_effect_verified=False,
            read_failure_or_non_readonly_phase_is_a_source_counterexample=True)
    return {"supported": bool(post_order and classified is not None), "admission_fact_id": fact["id"],
            "execute_binding": execute, "readonly_audit_activation_or_success_proven": False,
            "unique_pool_implementation_proven": False}


def _child_environment(analysis: Any) -> dict:
    document, _, function = analysis.roles["child_builder"]
    filter_call = _unique_call(analysis, "child_builder", "child_filter")
    if filter_call is None:
        return {"supported": False}
    node = _node(analysis, filter_call)
    args = _arguments(node)
    callback = unwrap(args[2]) if len(args) == 3 else None
    if callback is None or callback.type != "arrow_function":
        analysis.gap("child_environment_predicate_callback_unknown")
        return {"supported": False}
    callback_definition = document.definition_for_ast(callback)
    expected = analysis.roles["child_predicate"][1].graph_node_id
    actual = []
    for call in analysis.nodes(document, _field(callback, "body")):
        if call.type != "call_expression":
            continue
        edge, issues = analysis.sources.call_binding(call, document, callback_definition)
        if edge is not None and edge.target == expected:
            actual.append((call, edge))
    if len(actual) != 1:
        analysis.gap("child_environment_callback_actual_policy_unknown", matching_calls=len(actual))
        return {"supported": False}
    callback_body = unwrap(_field(callback, "body"))
    callback_parameters = _children(_field(callback, "parameters"))
    callback_binders = [_field(parameter, "pattern") or _field(parameter, "name") or parameter for parameter in callback_parameters]
    actual_args = _arguments(actual[0][0])
    if (callback_body is None or callback_body.type != "binary_expression" or _operator(document, callback_body) != "||"
            or unwrap(_field(callback_body, "right")) != actual[0][0]
            or len(callback_parameters) != 2 or len(actual_args) < 2
            or not all(_same(analysis, document, callback_binders[index], actual_args[index]) for index in range(2))):
        analysis.gap("child_environment_callback_return_protocol_unknown")
        return {"supported": False}
    filter_document, _, filter_function = analysis.roles["child_filter"]
    parameters = _children(_field(filter_function, "parameters"))
    predicate = _field(parameters[2], "pattern") or _field(parameters[2], "name") or parameters[2] if len(parameters) == 3 else None
    loops = [item for item in _children(_field(filter_function, "body")) if item.type == "for_in_statement"]
    attempts = []
    for loop in loops:
        writes = [item for item in analysis.nodes(filter_document, _field(loop, "body")) if item.type == "assignment_expression"]
        predicates = [item for item in analysis.nodes(filter_document, _field(loop, "body")) if item.type == "if_statement"]
        for write in writes:
            receiver, member = _member(filter_document, _field(write, "left"))
            if receiver is None:
                continue
            matching = []
            for guard in predicates:
                condition = unwrap(_field(guard, "condition"))
                if condition is not None and condition.type == "call_expression" and _inside(_field(guard, "consequence"), write):
                    arguments = _arguments(condition)
                    index = _field(_field(write, "left"), "index")
                    if (len(arguments) == 2 and _same(analysis, filter_document, _field(condition, "function"), predicate)
                            and _same(analysis, filter_document, arguments[0], index)
                            and _same(analysis, filter_document, arguments[1], _field(write, "right"))):
                        matching.append(guard)
            if len(matching) == 1:
                attempts.append(analysis.fact("child_environment_predicate_guarded_copy_attempt", filter_document, write,
                    loop_source=analysis.expression(filter_document, loop),
                    guard=analysis.expression(filter_document, _field(matching[0], "condition")),
                    target=analysis.expression(filter_document, _field(write, "left")),
                    source=analysis.expression(filter_document, _field(write, "right")),
                    runtime_setter_or_key_copy_success_proven=False))
    policy_link = _unique_call(analysis, "child_predicate", "child_keys")
    credentials = _unique_call(analysis, "child_keys", "provider_credentials")
    if len(loops) != 2 or len(attempts) != 2 or policy_link is None or credentials is None:
        analysis.gap("child_environment_filter_policy_chain_unknown", loop_count=len(loops), conditional_copy_count=len(attempts))
        return {"supported": False}
    fact = analysis.fact("child_environment_actual_callback_to_filter_and_key_policy", document, node,
        filter_call_fact_id=filter_call["id"], callback_location=document.location(callback),
        callback_callee_graph_node_id=actual[0][1].target, callback_call_edge_id=actual[0][1].id,
        callback_condition_source=analysis.expression(document, _field(callback, "body")),
        key_policy_call_fact_id=policy_link["id"], provider_credentials_call_fact_id=credentials["id"],
        parent_then_extra_loop_locations=[filter_document.location(loop) for loop in loops],
        parent_extra_write_attempt_fact_ids=[item["id"] for item in attempts],
        explicit_parent_skip_branches=_guard_records(analysis, "child_filter"),
        provider_credential_branch_counterexamples=_guard_records(analysis, "provider_credentials"),
        runtime_secret_leak_absence_or_env_completeness_proven=False)
    return {"supported": True, "filter_policy_fact_id": fact["id"], "conditional_copy_attempts": attempts,
            "explicit_allow_keys_and_provider_config_are_source_counterexamples_to_universal_secret_denial": True,
            "runtime_environment_or_provider_credential_availability_proven": False}


def _sandbox_policy(analysis: Any) -> dict:
    resolve = _unique_call(analysis, "sandbox_policy", "sandbox_mode")
    nested_resolve = _unique_call(analysis, "sandbox_launcher", "sandbox_policy")
    roots = _unique_call(analysis, "sandbox_launcher", "executable_roots")
    if any(call is None for call in (resolve, nested_resolve, roots)):
        return {"supported": False}
    document, _, function = analysis.roles["sandbox_launcher"]
    policy = _binding_identifier(analysis, roots)
    disabled = []
    required = []
    custom = []
    for guard in analysis.nodes(document, _field(function, "body")):
        if guard.type != "if_statement":
            continue
        condition = unwrap(_field(guard, "condition"))
        if condition is not None and condition.type == "unary_expression" and _operator(document, condition) == "!":
            receiver, member = _member(document, _field(condition, "argument"))
            if member == "enabled" and _same(analysis, document, receiver, policy):
                disabled.append(guard)
        if condition is None or condition.type != "binary_expression":
            continue
        if _operator(document, condition) == "||":
            tests = [unwrap(_field(condition, key)) for key in ("left", "right")]
            words = []
            for test in tests:
                receiver, member = _member(document, _field(test, "left"))
                if (test is not None and test.type == "binary_expression" and _operator(document, test) == "==="
                        and member == "mode" and _same(analysis, document, receiver, policy)):
                    words.append(_literal_string(document.text(_field(test, "right"))))
            if set(words) == {"required", "strict"} and analysis.simple_abrupt(_field(guard, "consequence")):
                required.append(guard)
        if _operator(document, condition) == "===":
            receiver, member = _member(document, _field(condition, "left"))
            if member == "provider" and _same(analysis, document, receiver, policy) and _literal_string(document.text(_field(condition, "right"))) == "custom":
                custom.append(guard)
    if len(disabled) != 1 or len(required) != 1 or not _inside(_field(disabled[0], "consequence"), required[0]) or len(custom) != 1:
        analysis.gap("sandbox_required_strict_or_custom_source_guard_unknown")
        return {"supported": False}
    returns = _returns(analysis, document, _field(disabled[0], "consequence"))
    fallback = [(node, _object(document, _returned_expression(node))) for node in returns]
    fallback = [(node, fields) for node, fields in fallback if fields and {"command", "args", "sandbox"} <= set(fields)]
    if len(fallback) != 1 or fallback[0][0].start_byte <= required[0].end_byte:
        analysis.gap("sandbox_disabled_fallback_not_after_required_guard")
        return {"supported": False}
    fact = analysis.fact("sandbox_required_strict_rejection_before_disabled_direct_launch_form", document, disabled[0],
        nested_policy_call_fact_id=nested_resolve["id"], executable_roots_call_fact_id=roots["id"],
        policy_binding=analysis.identity(document, policy),
        required_strict_condition=analysis.expression(document, _field(required[0], "condition")),
        abrupt_throw_branch=analysis.expression(document, _field(required[0], "consequence")),
        fallback_launch_fields={key: analysis.expression(document, value) for key, value in fallback[0][1].items()},
        source_guard_precedes_disabled_launch_return=True, model_id=CONTROL_MODEL,
        mode_field_runtime_propagation_or_sandbox_enforcement_proven=False)
    phase_document, _, phase_function = analysis.roles["phase_policy"]
    assignments = []
    for node in analysis.nodes(phase_document, _field(phase_function, "body")):
        if node.type != "assignment_expression":
            continue
        path = _path(phase_document, _field(node, "left"))
        if path and len(path) > 1 and path[-1].startswith("CPB_AGENT_SANDBOX"):
            assignments.append(analysis.fact("agent_phase_sandbox_environment_assignment_branch", phase_document, node,
                field_path=path, value=analysis.expression(phase_document, _field(node, "right")),
                source_conditions=analysis.branch_context(phase_document, node, phase_function),
                runtime_env_write_or_native_isolation_proven=False))
    policy_document, _, policy_function = analysis.roles["sandbox_policy"]
    policy_shapes = []
    for node in _returns(analysis, policy_document, _field(policy_function, "body")):
        fields = _object(policy_document, _returned_expression(node))
        if fields and {"mode", "enabled", "provider"} <= set(fields):
            policy_shapes.append(analysis.fact("agent_sandbox_provider_return_source_shape", policy_document, node,
                fields={key: analysis.expression(policy_document, value) for key, value in fields.items()},
                source_conditions=analysis.branch_context(policy_document, node, policy_function),
                actual_platform_probe_or_provider_capability_proven=False))
    modes = _guard_records(analysis, "sandbox_mode")
    custom_return = _returns(analysis, document, _field(custom[0], "consequence"))
    phase_conditions = _literal_values([item["source_conditions"] for item in assignments])
    off_shapes = [item for item in policy_shapes if "off" in _literal_values(item["source_conditions"])
                  and item["fields"].get("enabled", {}).get("literal") is False]
    custom_shapes = [item for item in policy_shapes if item["fields"].get("provider", {}).get("literal") == "custom"]
    platform_conditions = _literal_values([item["source_conditions"] for item in policy_shapes])
    if (not {"native", "none"} <= phase_conditions or not modes or not off_shapes or not custom_shapes
            or not {"darwin", "linux"} <= platform_conditions or len(custom_return) != 1):
        analysis.gap("agent_sandbox_boundary_counterexamples_not_accounted")
        return {"supported": False}
    custom_fact = analysis.fact("sandbox_custom_wrapper_command_and_args_source", document, custom_return[0],
        custom_predicate=analysis.expression(document, _field(custom[0], "condition")),
        custom_return=analysis.expression(document, custom_return[0]),
        provider_executable_or_isolation_effect_verified=False)
    return {"supported": True, "required_guard_fact_id": fact["id"],
            "custom_source_fact_id": custom_fact["id"], "phase_assignments": assignments,
            "normalized_mode_branches": modes, "provider_return_shapes": policy_shapes,
            "source_boundary_values": {"phase_policy_conditions": sorted(phase_conditions),
                "platform_conditions": sorted(platform_conditions),
                "off_return_fact_ids": [item["id"] for item in off_shapes],
                "custom_return_fact_ids": [item["id"] for item in custom_shapes]},
            "native_none_off_custom_and_platform_are_conditional_source_boundaries": True,
            "strict_network_process_fallback_source": [call for call in analysis.calls_by_role["sandbox_policy"]
                if any(argument.get("kind") == "ternary_expression" for argument in call.get("arguments", []))],
            "runtime_sandbox_isolation_proven": False}


def _acp_launch(analysis: Any, role: str) -> dict:
    document, _, function = analysis.roles[role]
    filtered = _unique_call(analysis, role, "child_builder")
    sandbox = _unique_call(analysis, role, "sandbox_launcher")
    if filtered is None or sandbox is None:
        return {"supported": False}
    env, launch = _binding_identifier(analysis, filtered), _binding_identifier(analysis, sandbox)
    candidates = []
    for call in analysis.calls_by_role[role]:
        node = _node(analysis, call)
        args = _arguments(node)
        if len(args) != 3:
            continue
        command_root, command_field = _member(document, args[0])
        args_root, args_field = _member(document, args[1])
        fields = _object(document, args[2])
        spawn_import = _spawn_import(analysis, document, node)
        if (command_field == "command" and args_field == "args"
                and _same(analysis, document, command_root, launch) and _same(analysis, document, args_root, launch)
                and fields is not None and "env" in fields and spawn_import is not None):
            candidates.append((call, fields, spawn_import))
    if len(candidates) != 1:
        analysis.gap("acp_sandbox_launch_to_process_source_unknown", role=role, matching_spawn_forms=len(candidates))
        return {"supported": False}
    process, fields, spawn_import = candidates[0]
    sandbox_node = _node(analysis, sandbox)
    sandbox_args = _arguments(sandbox_node)
    sandbox_fields = _object(document, sandbox_args[2]) if len(sandbox_args) == 3 else None
    if not sandbox_fields or "env" not in sandbox_fields or not _same(analysis, document, sandbox_fields["env"], env):
        analysis.gap("acp_filtered_environment_to_sandbox_argument_unknown", role=role)
        return {"supported": False}
    direct = _same(analysis, document, fields["env"], env)
    projection = None
    if not direct:
        projection = _unique_call(analysis, role, "acp_env_projection")
        projection_node = _node(analysis, projection) if projection is not None else None
        projection_args = _arguments(projection_node)
        assignment = projection_node.parent if projection_node is not None else None
        if (projection is None or len(projection_args) != 1 or not _same(analysis, document, projection_args[0], env)
                or assignment is None or assignment.type != "assignment_expression"
                or _path(document, _field(assignment, "left")) != _path(document, fields["env"])):
            analysis.gap("acp_child_environment_projection_unknown", role=role)
            return {"supported": False}
    order = _node(analysis, filtered).end_byte <= sandbox_node.start_byte < _node(analysis, process).start_byte
    if not order:
        analysis.gap("acp_filter_sandbox_launch_source_order_unknown", role=role)
        return {"supported": False}
    writes = []
    for node in analysis.nodes(document, _field(function, "body")):
        if node.type not in {"assignment_expression", "call_expression"} or node.start_byte <= _node(analysis, filtered).end_byte:
            continue
        if node.type == "assignment_expression":
            root = unwrap(_field(node, "left"))
            while root is not None and root.type in {"member_expression", "subscript_expression"}:
                root = unwrap(_field(root, "object"))
            if _same(analysis, document, root, env):
                writes.append(analysis.expression(document, node))
        else:
            args = _arguments(node)
            if any(_same(analysis, document, argument, env) for argument in args) and node != sandbox_node:
                writes.append(analysis.expression(document, node))
    fact = analysis.fact("acp_child_filter_sandbox_wrapper_to_process_source_forms", document, _node(analysis, process),
        role=role, filter_call_fact_id=filtered["id"], sandbox_call_fact_id=sandbox["id"],
        process_call_fact_id=process["id"], env_binding=analysis.identity(document, env),
        actual_process_import_binding=spawn_import,
        launch_binding=analysis.identity(document, launch), process_env_expression=analysis.expression(document, fields["env"]),
        audit_projection_call_fact_id=projection["id"] if projection else None,
        filter_then_sandbox_then_process_source_positions=True,
        explicit_postfilter_env_write_or_escape_source_forms=writes,
        unmodified_filtered_environment_proven=False,
        actual_child_process_or_sandbox_isolation_verified=False,
        scope="captured normal-prefix argument forms; asynchronous completion and external process effect unobserved")
    return {"supported": True, "source_fact_id": fact["id"], "postfilter_env_writes_accounted": bool(writes),
            "runtime_child_process_or_secret_boundary_proven": False}


def analyze_pattern(analysis: Any) -> dict:
    missing = sorted(REQUIRED_ROLES - set(analysis.roles))
    if missing:
        analysis.gap("agent_execution_policy_roles_missing", missing_roles=missing)
        return {"version": VERSION, "scoped_source_supported": False, "missing_roles": missing}
    if CONTROL_MODEL not in analysis.rule["models"]:
        analysis.gap("agent_execution_policy_control_model_missing")
        return {"version": VERSION, "scoped_source_supported": False}
    admission = _admission(analysis)
    child = _child_environment(analysis)
    sandbox = _sandbox_policy(analysis)
    launches = {role: _acp_launch(analysis, role) for role in ("acp_child", "acp_terminal")}
    supported = all(item.get("supported") for item in (admission, child, sandbox, *launches.values())) and not analysis.incomplete
    return {"version": VERSION, "admission_and_postexecution_review": admission,
        "child_environment_filter": child, "sandbox_source_policy": sandbox,
        "production_acp_launch_sources": launches, "scoped_source_supported": supported,
        "scope": "selected runAgent admission, injected-port usage, child filter and conditional sandbox/provider launch source policy",
        "source_derived_conditions_and_counterexamples": {
            "allowed_agents_null_and_empty_denial_distinct": admission.get("supported", False),
            "provider_credentials_explicit_allow_keys_and_postfilter_writes_retained": child.get("supported", False),
            "native_none_off_custom_platform_policy_branches_retained": sandbox.get("supported", False),
            "external_agent_audit_file_and_provider_capability_are_not_execution_evidence": True},
        "unique_pool_implementation_proven": False, "all_secrets_denied_proven": False,
        "runtime_sandbox_isolation_proven": False, "target_executed": False,
        "target_tests_run": False, "target_build_run": False, "whole_report_reproduced": False}
