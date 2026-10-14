"""Validated static policies. Configuration never contains executable hooks."""

from copy import deepcopy
import json
from pathlib import Path
from typing import Any

DEFAULT_CONFIG: dict[str, Any] = {
    "schema_version": 1,
    "project": {"name": ""},
    "analysis": {
        "languages": ["python"],
        "source_roots": ["."],
        "exclude": [".git", ".venv", "venv", "__pycache__", "node_modules", ".callscope", "build", "dist"],
        "max_file_bytes": 1048576,
    },
    "layers": {},
    "entrypoints": [],
    "rules": [],
    "value_contracts": [],
    "navigation_contracts": [],
    "atomicity_contracts": [],
    "field_contracts": [],
    "budget_contracts": [],
}
RULE_KINDS = {"required_path", "required_call", "forbidden_call", "forbidden_path"}
SEVERITIES = {"high", "medium", "low", "info"}


def _strings(value: Any, label: str, *, nonempty: bool = False) -> list[str]:
    if not isinstance(value, list) or (nonempty and not value):
        raise ValueError(f"{label} 必须为{'非空' if nonempty else ''}字符串数组")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValueError(f"{label} 不能包含空值或非字符串")
    return list(value)


def validate_config(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("配置必须为 JSON 对象")
    if type(value.get("schema_version", 1)) is not int or value.get("schema_version", 1) != 1:
        raise ValueError("仅支持 schema_version=1")
    result = deepcopy(DEFAULT_CONFIG)
    project = value.get("project", {})
    if not isinstance(project, dict) or not isinstance(project.get("name", ""), str):
        raise ValueError("project.name 必须为字符串")
    result["project"].update(project)
    analysis = value.get("analysis", {})
    if not isinstance(analysis, dict):
        raise ValueError("analysis 必须为对象")
    result["analysis"].update(analysis)
    section = result["analysis"]
    languages = _strings(section["languages"], "analysis.languages", nonempty=True)
    if len(languages) != len(set(languages)) or any(language not in {"python", "typescript", "rust"} for language in languages):
        raise ValueError("languages 仅支持 python/typescript/rust，不能重复；typescript 包含 JS/TSX")
    section["languages"] = languages
    roots = _strings(section["source_roots"], "analysis.source_roots", nonempty=True)
    for item in roots:
        path = Path(item)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("source_roots 必须是项目内的相对目录，不能包含 ..")
    section["source_roots"] = roots
    section["exclude"] = _strings(section["exclude"], "analysis.exclude")
    for field in ("module_aliases", "rust_crates"):
        mappings = section.get(field, {})
        if not isinstance(mappings, dict):
            raise ValueError(f"analysis.{field} 必须为名称到项目内相对路径的对象")
        for name, relative in mappings.items():
            if not isinstance(name, str) or not name.strip() or not isinstance(relative, str) or not relative.strip():
                raise ValueError(f"analysis.{field} 名称和路径必须为非空字符串")
            path = Path(relative)
            if path.is_absolute() or ".." in path.parts:
                raise ValueError(f"analysis.{field} 路径必须位于项目内")
        section[field] = dict(mappings)
    size = section["max_file_bytes"]
    if isinstance(size, bool) or not isinstance(size, int) or not 1 <= size <= 16777216:
        raise ValueError("max_file_bytes 必须为 1 到 16777216 的整数")
    from .input_capture import _validate_paths
    support_inputs = section.get("support_inputs", [])
    if isinstance(support_inputs, list) and len(support_inputs) > 128:
        raise ValueError("support_inputs 最多声明 128 个辅助输入")
    section["support_inputs"] = _validate_paths(support_inputs)
    profiles = section.get("rust_helper_profiles", [])
    if not isinstance(profiles, list):
        raise ValueError("rust_helper_profiles 必须为静态数据数组")
    seen_profiles = set()
    for profile in profiles:
        if not isinstance(profile, dict) or set(profile) != {"id", "crate_root", "workspace_manifest"}:
            raise ValueError("helper profile 必须包含 id/crate_root/workspace_manifest")
        if not isinstance(profile["id"], str) or not profile["id"].strip():
            raise ValueError("helper profile id 必须为非空字符串")
        _validate_paths([profile["crate_root"], profile["workspace_manifest"]])
        key = profile["crate_root"]
        if key in seen_profiles:
            raise ValueError("同一 crate_root 不能重复注册 helper profile")
        seen_profiles.add(key)
    from .rust_helpers import validate_helper_profiles
    section["rust_helper_profiles"] = validate_helper_profiles(profiles)
    section["rust_interface_models"] = _strings(section.get("rust_interface_models", []), "analysis.rust_interface_models")
    layers = value.get("layers", {})
    if not isinstance(layers, dict):
        raise ValueError("layers 必须为层名称到 glob 数组的对象")
    result["layers"] = {}
    for name, patterns in layers.items():
        if not isinstance(name, str) or not name.strip():
            raise ValueError("layer 名称不能为空")
        result["layers"][name] = _strings(patterns, f"layers.{name}", nonempty=True)
    result["entrypoints"] = _strings(value.get("entrypoints", []), "entrypoints")
    rules = value.get("rules", [])
    if not isinstance(rules, list):
        raise ValueError("rules 必须为数组")
    seen: set[str] = set()
    result["rules"] = []
    for rule in rules:
        if not isinstance(rule, dict):
            raise ValueError("每条 rule 必须为对象")
        for key in ("id", "kind", "from", "to"):
            if not isinstance(rule.get(key), str) or not rule[key].strip():
                raise ValueError(f"rule.{key} 必须为非空字符串")
        if rule["id"] in seen:
            raise ValueError(f"重复规则 ID: {rule['id']}")
        seen.add(rule["id"])
        if rule["kind"] not in RULE_KINDS:
            raise ValueError(f"不支持的规则 kind: {rule['kind']}")
        severity = rule.get("severity", "high")
        if not isinstance(severity, str) or severity not in SEVERITIES:
            raise ValueError(f"不支持的 severity: {severity}")
        if not isinstance(rule.get("description", ""), str):
            raise ValueError("rule.description 必须为字符串")
        result["rules"].append({**rule, "severity": severity, "description": rule.get("description", "")})
    contracts = value.get("static_contracts", [])
    if not isinstance(contracts, list) or len(contracts) > 256:
        raise ValueError("static_contracts 必须为最多 256 项的静态数据数组")
    from .static_contracts import _validate_rule
    seen_contracts = set()
    for contract in contracts:
        _validate_rule(contract)
        if contract["id"] in seen_contracts:
            raise ValueError(f"重复静态合同 ID: {contract['id']}")
        seen_contracts.add(contract["id"])
    result["static_contracts"] = deepcopy(contracts)
    value_contracts = value.get("value_contracts", [])
    if not isinstance(value_contracts, list) or len(value_contracts) > 256:
        raise ValueError("value_contracts 必须为最多 256 项的静态数据数组")
    seen_values: set[str] = set()
    if value_contracts:
        from .value_analysis import validate_value_rule
        for contract in value_contracts:
            validate_value_rule(contract)
            if contract["id"] in seen | seen_contracts | seen_values:
                raise ValueError(f"重复值来源合同 ID: {contract['id']}")
            seen_values.add(contract["id"])
    result["value_contracts"] = deepcopy(value_contracts)
    seen_semantic = seen | seen_contracts | seen_values
    for key, module_name, validator_name in (
        ("navigation_contracts", "navigation_analysis", "validate_navigation_rule"),
        ("atomicity_contracts", "atomicity_analysis", "validate_atomicity_rule"),
        ("field_contracts", "field_analysis", "validate_field_rule"),
        ("budget_contracts", "budget_analysis", "validate_budget_rule"),
    ):
        ruleset = value.get(key, [])
        if not isinstance(ruleset, list) or len(ruleset) > 256:
            raise ValueError(f"{key} 必须为最多 256 项的静态数据数组")
        if ruleset:
            if module_name == "navigation_analysis":
                from .navigation_analysis import validate_navigation_rule as validator
            elif module_name == "atomicity_analysis":
                from .atomicity_analysis import validate_atomicity_rule as validator
            elif module_name == "budget_analysis":
                from .budget_analysis import validate_budget_rule as validator
            else:
                from .field_analysis import validate_field_rule as validator
            for contract in ruleset:
                validator(contract)
                if contract["id"] in seen_semantic:
                    raise ValueError(f"重复语义合同 ID: {contract['id']}")
                seen_semantic.add(contract["id"])
        result[key] = deepcopy(ruleset)
    # Preserve data-only extension fields for forward-compatible adapters.
    for key, item in value.items():
        if key not in result:
            result[key] = deepcopy(item)
    return result


def load_config(root: str | Path, config_path: str | Path | None = None) -> dict[str, Any]:
    path = Path(config_path) if config_path is not None else Path(root) / ".callscope.json"
    if not path.exists():
        if config_path is not None:
            raise ValueError(f"配置文件不存在: {path}")
        return validate_config({})
    if path.is_symlink():
        raise ValueError("配置文件不能是符号链接")
    if path.stat().st_size > 1048576:
        raise ValueError("配置文件超过 1 MiB")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"无法读取配置: {exc}") from exc
    return validate_config(value)


def save_config(path: str | Path, value: Any) -> dict[str, Any]:
    config = validate_config(value)
    destination = Path(path)
    if destination.is_symlink():
        raise ValueError("配置文件不能是符号链接")
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + ".tmp")
    if temporary.is_symlink():
        raise ValueError("配置临时文件不能是符号链接")
    temporary.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(destination)
    return config

