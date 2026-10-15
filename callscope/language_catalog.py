"""Fixed frontend selection and honest capability metadata, without runtime probes.

CodeGraph's extension/type inventory is pinned to commit
8f1f842b5b828175992d2ce2cdf673b955b2cce9. JavaScript/JSX/TSX continue
through CallScope's existing TypeScript-family frontend, never a second pass.
"""

from pathlib import PurePosixPath
import re

CODEGRAPH_UPSTREAM_COMMIT = "8f1f842b5b828175992d2ce2cdf673b955b2cce9"
NATIVE_LANGUAGES = ("python", "typescript", "rust")
_CODEGRAPH_ORDER = (
    "arkts", "go", "java", "c", "cpp", "csharp", "razor", "php", "ruby",
    "swift", "kotlin", "dart", "svelte", "vue", "astro", "liquid", "pascal",
    "scala", "lua", "luau", "objc", "r", "solidity", "nix", "yaml", "twig",
    "xml", "properties", "cfml", "cfscript", "cfquery", "cobol", "vbnet",
    "erlang", "terraform",
)
CODEGRAPH_LANGUAGES = frozenset(_CODEGRAPH_ORDER)
SUPPORTED_LANGUAGES = NATIVE_LANGUAGES + _CODEGRAPH_ORDER
METADATA_LANGUAGES = frozenset({"yaml", "twig", "xml", "properties"})

# The complete upstream EXTENSION_MAP, with only the existing TS-family
# normalization. Stub and shell recognition are retained without new frontends.
EXTENSIONS = {
    ".ts": "typescript", ".tsx": "typescript", ".mts": "typescript", ".cts": "typescript",
    ".ets": "arkts", ".js": "typescript", ".mjs": "typescript", ".cjs": "typescript",
    ".xsjs": "typescript", ".xsjslib": "typescript", ".jsx": "typescript",
    ".py": "python", ".pyw": "python", ".pyi": "python-stub", ".go": "go", ".rs": "rust",
    ".java": "java", ".c": "c", ".h": "c", ".cpp": "cpp", ".cc": "cpp",
    ".cxx": "cpp", ".hpp": "cpp", ".hxx": "cpp", ".cs": "csharp",
    ".cshtml": "razor", ".razor": "razor", ".php": "php", ".module": "php",
    ".install": "php", ".theme": "php", ".inc": "php", ".yml": "yaml",
    ".yaml": "yaml", ".twig": "twig", ".rb": "ruby", ".rake": "ruby",
    ".swift": "swift", ".kt": "kotlin", ".kts": "kotlin", ".dart": "dart",
    ".liquid": "liquid", ".svelte": "svelte", ".vue": "vue", ".astro": "astro",
    ".r": "r", ".pas": "pascal", ".dpr": "pascal", ".dpk": "pascal",
    ".lpr": "pascal", ".dfm": "pascal", ".fmx": "pascal", ".scala": "scala",
    ".sc": "scala", ".lua": "lua", ".luau": "luau", ".m": "objc", ".mm": "objc",
    ".sol": "solidity", ".cfc": "cfml", ".cfm": "cfml", ".cfs": "cfscript",
    ".metal": "cpp", ".cu": "cpp", ".cuh": "cpp", ".nix": "nix", ".xml": "xml",
    ".cbl": "cobol", ".cob": "cobol", ".cobol": "cobol", ".cpy": "cobol",
    ".vb": "vbnet", ".erl": "erlang", ".hrl": "erlang", ".escript": "erlang",
    ".properties": "properties", ".tf": "terraform", ".tfvars": "terraform",
    ".tofu": "terraform", ".sh": "shell",
}
LANGUAGE_ALIASES = {
    "py": "python", "ts": "typescript", "javascript": "typescript", "js": "typescript",
    "tsx": "typescript", "jsx": "typescript", "rs": "rust", "golang": "go",
    "c++": "cpp", "c#": "csharp", "objective-c": "objc", "objectivec": "objc",
    "vb.net": "vbnet", "delphi": "pascal", "hcl": "terraform",
}


def normalize_languages(languages: list[str]) -> list[str]:
    """Expand the explicit all selector and reject overlapping frontend aliases."""
    names = [item.strip().lower() for item in languages]
    if names == ["all"]:
        return list(SUPPORTED_LANGUAGES)
    if "all" in names:
        raise ValueError('analysis.languages 的 all 必须单独使用：["all"]')
    result = [LANGUAGE_ALIASES.get(name, name) for name in names]
    if len(result) != len(set(result)):
        raise ValueError("analysis.languages 不能重复；JavaScript/JSX/TSX 与 typescript 使用同一前端")
    unknown = sorted(set(result) - set(SUPPORTED_LANGUAGES))
    if unknown:
        raise ValueError("未注册分析语言：" + ", ".join(unknown) + '；可使用 ["all"] 选择已注册前端')
    return result


def language_for_path(path: str, *, known_paths=(), path_exists=None) -> str | None:
    """Classify fixed extensions and upstream special paths, without opening files.

    known_paths must come from the caller's safe, no-follow inventory. Optional
    path_exists must also enforce no-follow access, including parents, for a
    marker outside selected roots. Arbitrary templates JSON is never Liquid.
    """
    if path == "conf/routes" or path.endswith("/conf/routes") or path.endswith(".routes"):
        return "yaml"
    if re.search(r"\.app(?:\.src)?$", path, re.IGNORECASE):
        return "erlang"
    parts = PurePosixPath(path).parts
    if path.lower().endswith(".json"):
        for index in range(len(parts) - 2, -1, -1):
            if parts[index].lower() not in {"templates", "sections"}:
                continue
            theme = "/".join(parts[:index])
            prefix = theme + "/" if theme else ""
            if any(prefix + marker in known_paths or (path_exists is not None and path_exists(prefix + marker))
                   for marker in ("layout/theme.liquid", "config/settings_schema.json")):
                return "liquid"
    return EXTENSIONS.get(PurePosixPath(path).suffix.lower())


LANGUAGE_CATALOG = {
    language: {
        "language": language,
        "frontend": "native" if language in NATIVE_LANGUAGES else "codegraph",
        "registered": True,
        "available": None,
        "availability_status": "runtime_not_checked",
        "verification_status": "not_validated_for_this_project",
        "analysis_level": ("bounded_static_relations" if language in NATIVE_LANGUAGES
                           else "file_or_metadata" if language in METADATA_LANGUAGES
                           else "structural_extraction"),
        "extensions": sorted(ext for ext, value in EXTENSIONS.items() if value == language),
        "embedded_only": language == "cfquery",
        "functional_completeness_proven": False,
        "upstream_commit": None if language in NATIVE_LANGUAGES else CODEGRAPH_UPSTREAM_COMMIT,
    }
    for language in SUPPORTED_LANGUAGES
}


def language_capabilities() -> list[dict]:
    """Return independent response records; registration never implies validation."""
    return [{**value, "extensions": list(value["extensions"])} for value in LANGUAGE_CATALOG.values()]
