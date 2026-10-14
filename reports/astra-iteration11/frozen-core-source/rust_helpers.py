"""Data-only, explicitly configured Rust derive-helper classification.

Inputs must be captured, identity-bound policy evidence. This module never
opens Cargo files, invokes Cargo, imports dependencies or expands macros.
An explicit versioned profile models helper registration, not generated code.
"""

from __future__ import annotations

import fnmatch
import hashlib
import posixpath
import re
import tomllib
from typing import Any, Mapping

MODEL_VERSION = "rust-derive-helper-model-1"
HELPER_MODEL_VERSION = MODEL_VERSION
SERDE_PROFILE = "serde-1.0.228-declared-helper-v1"
_PACKAGE_IDENTITIES = {
    "serde": "9a8e94ea7f378bd32cbbd37198a4a91436180c5bb472411e48b5ec2e2124ae9e",
    "serde_derive": "d540f220d3187173da220f885ab66608367b6574e925011a9353e4badda91d79",
}
_REGISTRY_SOURCE = "registry+https://github.com/rust-lang/crates.io-index"
_DERIVES = {"serde::Serialize", "serde::Deserialize"}
_BUILTIN_DERIVES = {"Debug": ["fmt"], "Clone": ["clone", "clone_from"], "PartialEq": ["eq", "ne"]}
_STANDARD = {
    "derive", "must_use", "inline", "allow", "warn", "deny", "forbid", "doc", "cold", "repr",
    "non_exhaustive", "deprecated", "track_caller", "automatically_derived", "expect", "rustfmt::skip",
}
_PATH = r"[A-Za-z_][A-Za-z_0-9]*(?:::[A-Za-z_][A-Za-z_0-9]*)*"


class _Unknown(ValueError):
    pass


def validate_helper_profiles(value: Any) -> list[dict[str, str]]:
    """Policy schema: explicit profile IDs, empty by default, no name whitelist."""
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError("analysis.rust_helper_profiles 必须为显式profile记录列表")
    result: list[dict[str, str]] = []
    roots: set[str] = set()
    for profile in value:
        if not isinstance(profile, dict) or set(profile) != {"id", "crate_root", "workspace_manifest"}:
            raise ValueError("helper profile必须仅含id/crate_root/workspace_manifest")
        if profile.get("id") != SERDE_PROFILE:
            raise ValueError("analysis.rust_helper_profiles 包含未支持profile")
        try:
            crate_root = _relative(profile["crate_root"])
            workspace_manifest = _relative(profile["workspace_manifest"])
        except _Unknown as error:
            raise ValueError(str(error)) from error
        if crate_root in roots or posixpath.basename(workspace_manifest) != "Cargo.toml":
            raise ValueError("helper profile的crate_root重复或workspace_manifest不是Cargo.toml")
        roots.add(crate_root)
        result.append({"id": SERDE_PROFILE, "crate_root": crate_root, "workspace_manifest": workspace_manifest})
    return sorted(result, key=lambda profile: (profile["crate_root"], profile["id"], profile["workspace_manifest"]))


validate_profiles = validate_helper_profiles


def _table(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise _Unknown(f"{label}不是可识别TOML table")
    return value


def _strings(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise _Unknown(f"{label}不是完整string array")
    return value


def _relative(path: str) -> str:
    if not isinstance(path, str) or not path or path.startswith("/") or "\\" in path or ":" in path:
        raise _Unknown("support context 不是项目内相对POSIX路径")
    if ".." in path.split("/"):
        raise _Unknown("support context 路径逃逸")
    return posixpath.normpath(path)


def _attribute(text: str) -> tuple[str, str]:
    match = re.fullmatch(r"\s*#\s*\[\s*(" + _PATH + r")\s*(.*?)\s*\]\s*", text, re.DOTALL)
    if not match:
        raise _Unknown("属性不是本profile支持的完整outer attribute语法")
    return match.group(1), match.group(2).strip()


def _derive_paths(tail: str) -> list[str]:
    if not tail.startswith("(") or not tail.endswith(")"):
        raise _Unknown("derive 缺少完整参数列表")
    body = tail[1:-1].strip()
    body = body[:-1].strip() if body.endswith(",") else body
    parts = [part.strip() for part in body.split(",")]
    if not parts or any(not re.fullmatch(_PATH, part) for part in parts):
        raise _Unknown("derive paths存在别名/不支持token形式")
    return parts


def _helper_arguments(tail: str) -> dict[str, Any]:
    # First profile intentionally recognizes only the observed container forms.
    if not tail.startswith("(") or not tail.endswith(")"):
        raise _Unknown("serde helper参数不在当前窄profile内")
    body = tail[1:-1].strip()
    body = body[:-1].strip() if body.endswith(",") else body
    parts = [part.strip() for part in body.split(",")]
    output: dict[str, Any] = {}
    for part in parts:
        if part == "deny_unknown_fields":
            key, value = "deny_unknown_fields", True
        else:
            match = re.fullmatch(r'rename_all\s*=\s*"(camelCase|snake_case|PascalCase|SCREAMING_SNAKE_CASE|lowercase|UPPERCASE|kebab-case|SCREAMING-KEBAB-CASE)"', part)
            if not match:
                raise _Unknown("未知helper选项，不推断其宏行为")
            key, value = "rename_all", match.group(1)
        if key in output:
            raise _Unknown("重复helper选项不能选择有效配置")
        output[key] = value
    return output


def _capture(inputs: Mapping[str, Any], path: str) -> tuple[dict[str, Any], dict[str, Any]]:
    record = inputs.get(path)
    if not isinstance(record, dict) or record.get("status") != "captured" or not isinstance(record.get("content"), str):
        raise _Unknown(f"缺少身份绑定的captured support input: {path}")
    if record.get("path", path) != path or record.get("symlink"):
        raise _Unknown("support input路径/安全读取状态不匹配")
    digest = record.get("hash")
    if not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest):
        raise _Unknown("support input 缺少原始SHA256身份")
    text_digest = hashlib.sha256(record["content"].encode("utf-8")).hexdigest()
    if record.get("text_hash") != text_digest:
        raise _Unknown("support input text_hash缺失或与捕获content不一致")
    try:
        parsed = tomllib.loads(record["content"])
    except (tomllib.TOMLDecodeError, TypeError) as error:
        raise _Unknown(f"support TOML解析失败: {path}") from error
    evidence = {"path": path, "hash": digest, "status": record["status"],
        "text_hash": text_digest, "captured_text_utf8_sha256": text_digest}
    return parsed, evidence


def _forbidden_source(dependency: Any) -> bool:
    return not isinstance(dependency, dict) or any(key in dependency for key in
        {"package", "path", "git", "branch", "tag", "rev", "registry", "registry-index"})


def _contains_target_dependency(manifest: dict[str, Any]) -> bool:
    target = manifest.get("target", {})
    if not isinstance(target, dict):
        return True
    for table in target.values():
        if not isinstance(table, dict):
            return True
        for section in ("dependencies", "dev-dependencies", "build-dependencies"):
            dependencies = table.get(section, {})
            if not isinstance(dependencies, dict) or any(name in dependencies or any(
                    isinstance(entry, dict) and entry.get("package") == name for entry in dependencies.values())
                    for name in _PACKAGE_IDENTITIES):
                return True
    return False


def _declared_provider(inputs: Mapping[str, Any], crate_root: str, workspace_manifest: str,
                       item_file: str) -> dict[str, Any]:
    crate_root, workspace_manifest, item_file = map(_relative, (crate_root, workspace_manifest, item_file))
    prefix = "" if crate_root == "." else crate_root + "/"
    if not item_file.startswith(prefix + "src/"):
        raise _Unknown("item不属于已声明crate root的src上下文")
    crate_path = posixpath.join(crate_root, "Cargo.toml")
    crate_path = _relative(crate_path)
    lock_path = _relative(posixpath.join(posixpath.dirname(workspace_manifest), "Cargo.lock"))
    member, member_evidence = _capture(inputs, crate_path)
    workspace, workspace_evidence = _capture(inputs, workspace_manifest)
    lock, lock_evidence = _capture(inputs, lock_path)
    workspace_data = workspace.get("workspace")
    if not isinstance(workspace_data, dict):
        raise _Unknown("捕获文件未声明所需workspace")
    member_package = _table(member.get("package", {}), "crate package")
    if "workspace" in member_package or "workspace" in member:
        raise _Unknown("成员声明了另指/自带workspace，当前模型不假定父workspace归属")
    workspace_dir = posixpath.dirname(workspace_manifest)
    relative_member = posixpath.relpath(crate_root, workspace_dir or ".")
    if relative_member.startswith("../") or not any(fnmatch.fnmatchcase(relative_member, value)
            for value in _strings(workspace_data.get("members", []), "workspace members")):
        raise _Unknown("crate root 未被捕获workspace members明确包含")
    if any(fnmatch.fnmatchcase(relative_member, value) for value in _strings(workspace_data.get("exclude", []), "workspace exclude")):
        raise _Unknown("crate root 在workspace exclude中")
    for manifest in (member, workspace):
        patch = manifest.get("patch", {})
        if not isinstance(patch, dict):
            raise _Unknown("不支持patch声明")
        for source_table in patch.values():
            if not isinstance(source_table, dict):
                raise _Unknown("patch源不是table")
            for name, entry in source_table.items():
                if not isinstance(entry, dict):
                    raise _Unknown("patch项不是完整dependency table")
                if name in _PACKAGE_IDENTITIES or entry.get("package") in _PACKAGE_IDENTITIES:
                    raise _Unknown("serde provider 存在直接/别名package patch")
        replacements = manifest.get("replace", {})
        if not isinstance(replacements, dict) or any(key.split(":", 1)[0] in _PACKAGE_IDENTITIES for key in replacements):
            raise _Unknown("serde provider 存在replace")
        if _contains_target_dependency(manifest):
            raise _Unknown("serde provider存在target条件依赖，未选择构建配置")
    dependency = _table(member.get("dependencies", {}), "crate dependencies").get("serde")
    if not isinstance(dependency, dict):
        raise _Unknown("crate未显式声明无别名serde dependency")
    if dependency.get("optional"):
        raise _Unknown("serde是optional依赖，未解析feature配置")
    if dependency.get("workspace") is True:
        if set(dependency) - {"workspace", "features", "default-features", "optional"}:
            raise _Unknown("成员serde workspace声明包含未知provider字段")
        resolved = _table(workspace_data.get("dependencies", {}), "workspace dependencies").get("serde")
        if _forbidden_source(resolved):
            raise _Unknown("workspace serde有别名/path/git/registry等不支持来源")
        features = set(_strings(resolved.get("features", []), "workspace serde features")) | set(_strings(dependency.get("features", []), "crate serde features"))
    else:
        resolved = dependency
        if _forbidden_source(resolved):
            raise _Unknown("serde provider不是未改名的默认registry package")
        features = set(_strings(resolved.get("features", []), "serde features"))
    if resolved.get("optional") or resolved.get("version") != "=1.0.228" or "derive" not in features:
        raise _Unknown("当前profile要求显式serde=1.0.228且derive feature非条件启用")
    edition = member_package.get("edition")
    if isinstance(edition, dict) and edition.get("workspace") is True:
        edition = _table(workspace_data.get("package", {}), "workspace package").get("edition")
    if str(edition) not in {"2018", "2021", "2024"}:
        raise _Unknown("extern prelude版本上下文未知或不支持")
    identities = {}
    packages = lock.get("package", [])
    if not isinstance(packages, list):
        raise _Unknown("Cargo.lock package集合未知")
    for name, checksum in _PACKAGE_IDENTITIES.items():
        matches = [package for package in packages if isinstance(package, dict) and package.get("name") == name]
        if len(matches) != 1:
            raise _Unknown("serde provider lock身份不唯一")
        package = matches[0]
        if package.get("version") != "1.0.228" or package.get("source") != _REGISTRY_SOURCE or package.get("checksum") != checksum:
            raise _Unknown("serde provider lock与显式版本profile不匹配")
        identities[name] = {key: package[key] for key in ("name", "version", "source", "checksum")}
    serde_lock = next(package for package in packages if isinstance(package, dict) and package.get("name") == "serde")
    if not any(isinstance(dependency, str) and dependency.split(" ", 1)[0] == "serde_derive"
               for dependency in _strings(serde_lock.get("dependencies", []), "serde lock dependencies")):
        raise _Unknown("serde lock未声明serde_derive provider关联")
    return {"capture_evidence": [member_evidence, workspace_evidence, lock_evidence],
        "packages": identities, "crate_root": crate_root, "workspace_manifest": workspace_manifest,
        "edition": str(edition), "provider_basis": "captured_declared_manifest_and_lock",
        "installed_dependency_or_expansion_verified": False}


def classify_helpers(attributes: list[str], *, profile_id: str | None, support_inputs: Mapping[str, Any],
                     crate_root: str, workspace_manifest: str, item_file: str, item_kind: str,
                     shadowed_names: set[str] | None = None, bindings_complete: bool = False,
                     source_complete: bool = False, generic: bool = False, conditional: bool = False,
                     macro_scope_unknown: bool = True) -> dict[str, Any]:
    """Only supply helper indices to exempt; never globally whitelist serde.

    The caller retains cfg, generics, proc-attribute, deref, trait and generated
    member guards. An accepted result is a source-binding model under explicit
    captured/profile assumptions, not macro expansion or compilation success.
    """
    result: dict[str, Any] = {"model_version": MODEL_VERSION, "profile_id": profile_id,
        "accepted": False, "helper_attribute_indices": [], "helper_attributes": [],
        "generated_members_unknown": True, "macro_expansion_performed": False,
        "original_item_preserved_basis": None}
    try:
        if any(type(value) is not bool for value in
               (bindings_complete, source_complete, generic, conditional, macro_scope_unknown)):
            raise _Unknown("helper上下文完备性/条件标记不是明确bool事实")
        if profile_id != SERDE_PROFILE:
            raise _Unknown("没有显式启用受支持的版本化helper profile")
        if item_kind not in {"struct", "enum", "struct_item", "enum_item"}:
            raise _Unknown("当前helper profile仅支持非泛型struct/enum声明")
        if not source_complete or not bindings_complete or macro_scope_unknown:
            raise _Unknown("源/宏名称绑定范围不完整，不能确认helper provider")
        if generic or conditional:
            raise _Unknown("泛型/cfg条件声明仍保持opaque")
        parsed = [_attribute(attribute) for attribute in attributes]
        if any(name in {"cfg", "cfg_attr"} for name, _ in parsed):
            raise _Unknown("cfg/cfg_attr不得被helper模型消除")
        if any(name not in _STANDARD | {"serde"} for name, _ in parsed):
            raise _Unknown("item还含未知attribute proc macro，不能确认原声明未被变换")
        derives = [path for name, tail in parsed if name == "derive" for path in _derive_paths(tail)]
        if not (_DERIVES & set(derives)):
            raise _Unknown("serde helper未与fully-qualified serde derives同item配对")
        if any(path not in _DERIVES | set(_BUILTIN_DERIVES) for path in derives):
            raise _Unknown("未知derive生成集合/别名路径不在本profile内")
        protected_names = {"serde", *[path for path in derives if path in _BUILTIN_DERIVES]}
        if protected_names & (shadowed_names or set()):
            raise _Unknown("serde或builtin derive名称被本地module/use/macro等遮蔽")
        helpers = [(index, _helper_arguments(tail)) for index, (name, tail) in enumerate(parsed) if name == "serde"]
        if len(helpers) != 1:
            raise _Unknown("当前窄profile要求唯一完整serde容器helper属性")
        provider = _declared_provider(support_inputs, crate_root, workspace_manifest, item_file)
        possible_members = {member for path in derives if path in _BUILTIN_DERIVES for member in _BUILTIN_DERIVES[path]}
        if "serde::Serialize" in derives:
            possible_members.add("serialize")
        if "serde::Deserialize" in derives:
            possible_members.update({"deserialize", "deserialize_in_place"})
        result.update(accepted=True, helper_attribute_indices=[index for index, _ in helpers],
            helper_attributes=[{"index": index, "name": "serde", "arguments": values} for index, values in helpers],
            paired_derives=derives, provider=provider,
            registration={"helper": "serde", "registered_by": sorted(_DERIVES & set(derives)),
                "authority": "explicit_versioned_trusted_profile", "actual_registration_source_captured": False},
            original_item_preserved_basis="Rust derive helper; derives append items rather than replacing the original item",
            generated_member_name_candidates=sorted(possible_members), generated_members_exhaustive=False,
            receiver_interface_model={
                "version": "serde-1.0.228-receiver-interfaces-v1",
                "basis": "explicit_versioned_trusted_profile",
                "scope": "receiver_member_name_conflicts_from_supported_derives",
                "complete_within_profile": True,
                "member_names": sorted(possible_members),
                "trait_interfaces": [{"derive": path, "members": (
                    ["serialize"] if path == "serde::Serialize" else
                    ["deserialize", "deserialize_in_place"] if path == "serde::Deserialize" else
                    _BUILTIN_DERIVES[path])} for path in sorted(set(derives))],
                "default_and_supertrait_members_included": True,
                "generated_inherent_and_deref_members_assumed_absent": True,
                "generated_bodies_known": False, "actual_macro_expansion_captured": False,
                "other_generated_items_unknown": True,
                "assumptions": [
                    "only the listed derive identities and narrow container options are supported",
                    "their original-receiver trait interfaces match this versioned trusted model",
                    "they add no inherent or Deref members on the original receiver in this profile",
                    "macro names are unshadowed and caller-owned binding closure is complete",
                    "declared package identity is captured; actual Cargo resolution and expansion are unverified",
                ],
            },
            assumptions=["profile helper-registration and receiver-interface contracts are trusted, not expanded",
                         "support inputs are identity-bound by the runner",
                         "caller preserves all other unknown macro/cfg/trait/receiver guards"])
    except (_Unknown, TypeError, KeyError, ValueError, AttributeError) as error:
        result["reason"] = str(error)
    return result


def classify_rust_item_helpers(attributes: list[str], *, profiles: list[dict[str, str]], support_inputs: Mapping[str, Any],
                               crate_root: str, workspace_manifest: str, item_file: str, item_kind: str,
                               shadowed_names: set[str], bindings_complete: bool, source_complete: bool,
                               generic: bool, conditional: bool, macro_scope_unknown: bool) -> dict[str, Any]:
    """Stable JSON result consumed by the frontend, with caller-owned closure facts."""
    try:
        enabled = validate_helper_profiles(profiles)
        crate_root, workspace_manifest = _relative(crate_root), _relative(workspace_manifest)
    except ValueError as error:
        return {"model_version": MODEL_VERSION, "accepted": False, "helper_attribute_indices": [],
                "providers": [], "generated_members_unknown": True, "generated_member_names": [],
                "reasons": [str(error)], "macro_expansion_performed": False}
    selected = [profile for profile in enabled if profile["crate_root"] == posixpath.normpath(crate_root)
                and profile["workspace_manifest"] == posixpath.normpath(workspace_manifest)]
    result = classify_helpers(attributes, profile_id=selected[0]["id"] if len(selected) == 1 else None,
        support_inputs=support_inputs, crate_root=crate_root, workspace_manifest=workspace_manifest,
        item_file=item_file, item_kind=item_kind, shadowed_names=shadowed_names,
        bindings_complete=bindings_complete, source_complete=source_complete, generic=generic,
        conditional=conditional, macro_scope_unknown=macro_scope_unknown)
    result["providers"] = [result["provider"]] if result.get("provider") else []
    result["generated_member_names"] = list(result.get("generated_member_name_candidates", []))
    result["reasons"] = [result["reason"]] if result.get("reason") else []
    return result
