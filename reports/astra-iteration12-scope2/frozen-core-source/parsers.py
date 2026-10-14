"""Fixed analysis-tool grammar imports; never import a target project module."""

from functools import lru_cache
from importlib import metadata, machinery, util
from pathlib import Path
import sys
import sysconfig
import threading

_BUNDLED_TOOLS = Path(__file__).resolve().parent.parent / ".analysis-tools" / "python"
_IMPORT_LOCK = threading.RLock()


def _trusted_roots():
    paths = [_BUNDLED_TOOLS, Path(sysconfig.get_path("purelib")), Path(sysconfig.get_path("platlib"))]
    return tuple(dict.fromkeys(path.resolve() for path in paths if path.is_dir()))


def _trusted_module(name: str):
    # Never search cwd, target folders, or arbitrary PYTHONPATH entries. Relative
    # imports inside these fixed grammar packages use their verified __path__.
    roots = _trusted_roots()
    with _IMPORT_LOCK:
        existing = sys.modules.get(name)
        if existing is not None:
            origin = getattr(getattr(existing, "__spec__", None), "origin", None)
            if not origin or not any(Path(origin).resolve().is_relative_to(root) for root in roots):
                raise RuntimeError(f"拒绝来自工具依赖目录以外的语法模块：{name}")
            return existing
        spec = machinery.PathFinder.find_spec(name, [str(root) for root in roots])
        if spec is None or spec.loader is None or not spec.origin:
            raise ImportError(name)
        if not any(Path(spec.origin).resolve().is_relative_to(root) for root in roots):
            raise RuntimeError(f"语法模块路径不在工具依赖目录：{name}")
        module = util.module_from_spec(spec)
        sys.modules[name] = module
        try:
            spec.loader.exec_module(module)
        except BaseException:
            sys.modules.pop(name, None)
            raise
        return module


@lru_cache(maxsize=3)
def _distribution_version(name: str):
    canonical = name.replace("_", "-").casefold()
    for distribution in metadata.distributions(path=[str(root) for root in _trusted_roots()]):
        found = distribution.metadata.get("Name", "").replace("_", "-").casefold()
        if found == canonical:
            return distribution.version
    raise metadata.PackageNotFoundError(name)

_GRAMMARS = {
    "typescript": ("tree_sitter_typescript", "language_typescript", "tree-sitter-typescript"),
    "tsx": ("tree_sitter_typescript", "language_tsx", "tree-sitter-typescript"),
    "rust": ("tree_sitter_rust", "language", "tree-sitter-rust"),
}


def parser_version(kind: str) -> str:
    if kind not in _GRAMMARS:
        raise ValueError(f"不支持的静态语法：{kind}")
    grammar = _GRAMMARS[kind][2]
    try:
        versions = f"tree-sitter-{_distribution_version('tree-sitter')}+{grammar}-{_distribution_version(grammar)}"
    except metadata.PackageNotFoundError:
        versions = f"{grammar}-unavailable"
    return versions + f"+{sys.implementation.name}-{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


@lru_cache(maxsize=3)
def _language(kind: str):
    if kind not in _GRAMMARS:
        raise ValueError(f"不支持的静态语法：{kind}")
    module, factory, _ = _GRAMMARS[kind]
    try:
        tree_sitter = _trusted_module("tree_sitter")
        grammar = _trusted_module(module)
    except ImportError as exc:
        raise RuntimeError("缺少固定静态语法库；安装 callscope[languages]。目标源码没有被执行。") from exc
    return tree_sitter.Language(getattr(grammar, factory)())


def language_parser(kind: str):
    try:
        tree_sitter = _trusted_module("tree_sitter")
    except ImportError as exc:
        raise RuntimeError("缺少 tree-sitter 静态语法库；安装 callscope[languages]。") from exc
    return tree_sitter.Parser(_language(kind))
