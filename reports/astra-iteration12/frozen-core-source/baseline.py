"""Compare frozen, data-only observations with saved static-analysis facts.

Only the baseline document and this module's own implementation are opened.
Evaluation reads neither the current repository nor Git and never executes a
source quote. Results are separate from the immutable baseline and snapshot.
An evidence-only observation remains a human observation even when quotes match.
"""

from collections import Counter, deque
from hashlib import sha256
from pathlib import Path, PurePosixPath
import json
import re
from typing import Any

from .graph import GraphIndex
from .models import Edge, GraphSnapshot, Node, SourceFile


EVALUATOR_VERSION = "frozen-static-baseline-1.3"
EVALUATOR_SOURCE_HASH = sha256(Path(__file__).read_bytes()).hexdigest()
MAX_BASELINE_BYTES = 8 * 1024 * 1024
SAMPLE_LIMIT = 5
_COMPLETE = frozenset({"parsed", "complete", "ok", "analyzed"})
_LANGUAGES = frozenset({"python", "typescript", "rust"})
_OUTCOMES = (
    "confirmed_static_call", "confirmed_static_path",
    "no_direct_call_in_explicit_model", "unknown_required", "evidence_only",
)
_STATUSES = (
    "reproduced", "unknown", "mismatch", "evidence_only", "source_changed",
    "source_missing", "evidence_unavailable", "endpoint_missing", "ambiguous",
)
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_COMMIT = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,199}\Z")
_TRAIT_METHOD = re.compile(
    r"(?P<prefix>(?:[A-Za-z_]\w*\.)*)"
    r"<(?P<owner>[A-Za-z_]\w*(?:::[A-Za-z_]\w*)*)\s+as\s+"
    r"[A-Za-z_]\w*(?:::[A-Za-z_]\w*)*>\."
    r"(?P<method>[A-Za-z_]\w*)\Z"
)


def _text(value: Any, label: str, *, maximum: int = 10000) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > maximum or "\x00" in value:
        raise ValueError(f"{label} must be a non-empty string of at most {maximum} characters")
    return value


def _identifier(value: Any, label: str) -> str:
    if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
        raise ValueError(f"{label} must be a stable identifier")
    return value


def _object(value: Any, label: str, keys: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError(f"{label} must contain exactly these fields: {', '.join(sorted(keys))}")
    return value


def _enum(value: Any, label: str, choices: Any) -> str:
    if not isinstance(value, str) or value not in choices:
        raise ValueError(f"{label} must be one of {', '.join(sorted(choices))}")
    return value


def _path(value: Any, label: str, *, absolute: bool = False) -> str:
    value = _text(value, label, maximum=4096)
    if "\\" in value or any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise ValueError(f"{label} must be a canonical POSIX path")
    path = PurePosixPath(value)
    if path.is_absolute() != absolute or ".." in path.parts or str(path) != value or value == ".":
        raise ValueError(f"{label} must be a canonical {'absolute' if absolute else 'repository-relative'} path")
    return value


def _strings(value: Any, label: str) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a string array")
    return [_text(item, f"{label}[{i}]") for i, item in enumerate(value)]


def _selector(value: Any, label: str) -> dict[str, str] | None:
    if value is None:
        return None
    obj = _object(value, label, {"path", "symbol", "language"})
    symbol = _text(obj["symbol"], f"{label}.symbol", maximum=2048)
    if any(ord(char) < 32 or ord(char) == 127 for char in symbol):
        raise ValueError(f"{label}.symbol must be a literal lexical symbol")
    return {
        "path": _path(obj["path"], f"{label}.path"),
        "symbol": symbol,
        "language": _enum(obj["language"], f"{label}.language", _LANGUAGES),
    }


def _validate_baseline(value: Any) -> dict[str, Any]:
    obj = _object(value, "baseline", {"schema_version", "baseline_id", "status", "repositories", "observations"})
    if type(obj["schema_version"]) is not int or obj["schema_version"] != 1:
        raise ValueError("baseline.schema_version must be 1")
    if obj["status"] != "final":
        raise ValueError("Only a frozen final baseline can be evaluated")
    if not isinstance(obj["repositories"], list) or not obj["repositories"]:
        raise ValueError("baseline.repositories must be a non-empty array")
    repositories = []
    repo_by_id = {}
    for i, raw in enumerate(obj["repositories"]):
        label = f"repositories[{i}]"
        repo = _object(raw, label, {"id", "root", "commit", "source_files"})
        repo_id = _identifier(repo["id"], f"{label}.id")
        if repo_id in repo_by_id:
            raise ValueError(f"Duplicate repository ID: {repo_id}")
        commit = _text(repo["commit"], f"{label}.commit", maximum=64)
        if not _COMMIT.fullmatch(commit):
            raise ValueError(f"{label}.commit must be a full hexadecimal Git identity")
        if not isinstance(repo["source_files"], dict) or not repo["source_files"]:
            raise ValueError(f"{label}.source_files must be a non-empty path-to-SHA256 object")
        source_files = {}
        for path, digest in repo["source_files"].items():
            path = _path(path, f"{label}.source_files path")
            if not isinstance(digest, str) or not _SHA256.fullmatch(digest):
                raise ValueError(f"{label}.source_files[{path}] must be a SHA256")
            source_files[path] = digest
        saved = {"id": repo_id, "root": _path(repo["root"], f"{label}.root", absolute=True),
                 "commit": commit, "source_files": source_files}
        repositories.append(saved)
        repo_by_id[repo_id] = saved
    if not isinstance(obj["observations"], list) or not obj["observations"]:
        raise ValueError("baseline.observations must be a non-empty array")
    observations, seen = [], set()
    observation_keys = {"id", "repo", "commit", "category", "claim", "source", "target", "expected_static_outcome",
                        "locations", "reason", "certainty", "conditions", "counterevidence", "priority", "tool_support"}
    for i, raw in enumerate(obj["observations"]):
        label = f"observations[{i}]"
        observation = _object(raw, label, observation_keys)
        observation_id = _identifier(observation["id"], f"{label}.id")
        if observation_id in seen:
            raise ValueError(f"Duplicate observation ID: {observation_id}")
        seen.add(observation_id)
        repo_id = _identifier(observation["repo"], f"{label}.repo")
        if repo_id not in repo_by_id:
            raise ValueError(f"Unknown repository ID: {repo_id}")
        repository = repo_by_id[repo_id]
        if observation["commit"] != repository["commit"]:
            raise ValueError(f"{label}.commit disagrees with its repository")
        outcome = _enum(observation["expected_static_outcome"], f"{label}.expected_static_outcome", _OUTCOMES)
        source, target = _selector(observation["source"], f"{label}.source"), _selector(observation["target"], f"{label}.target")
        if outcome in {"confirmed_static_call", "confirmed_static_path", "no_direct_call_in_explicit_model"} and (source is None or target is None):
            raise ValueError(f"{label} requires both source and target selectors")
        if outcome == "unknown_required" and source is None:
            raise ValueError(f"{label} requires an actual caller selector")
        if not isinstance(observation["locations"], list) or not observation["locations"]:
            raise ValueError(f"{label}.locations must be a non-empty array")
        locations = []
        for j, raw_location in enumerate(observation["locations"]):
            location_label = f"{label}.locations[{j}]"
            location = _object(raw_location, location_label, {"path", "line", "end_line", "role", "quote"})
            line, end_line = location["line"], location["end_line"]
            if type(line) is not int or type(end_line) is not int or not 1 <= line <= end_line <= 2147483647:
                raise ValueError(f"{location_label} must have a positive inclusive line range")
            locations.append({"path": _path(location["path"], f"{location_label}.path"), "line": line, "end_line": end_line,
                              "role": _enum(location["role"], f"{location_label}.role", {"call_site", "definition", "binding", "guard", "contract", "counterevidence"}),
                              "quote": _text(location["quote"], f"{location_label}.quote", maximum=100000)})
        references = {location["path"] for location in locations}
        references.update(selector["path"] for selector in (source, target) if selector)
        if references - repository["source_files"].keys():
            raise ValueError(f"{label} refers to files without frozen SHA256 values")
        call_sites = [location for location in locations if location["role"] == "call_site"]
        if outcome in {"confirmed_static_call", "confirmed_static_path", "unknown_required"} and not call_sites:
            raise ValueError(f"{label} requires call_site evidence")
        if outcome in {"confirmed_static_call", "unknown_required"} and not any(location["path"] == source["path"] for location in call_sites):
            raise ValueError(f"{label} requires a call_site in its caller file")
        support = _object(observation["tool_support"], f"{label}.tool_support", {"version", "state", "required_capabilities", "explanation", "snapshot_id"})
        snapshot_id = support["snapshot_id"]
        if snapshot_id is not None:
            snapshot_id = _identifier(snapshot_id, f"{label}.tool_support.snapshot_id")
        observations.append({
            "id": observation_id, "repo": repo_id, "commit": repository["commit"],
            "category": _enum(observation["category"], f"{label}.category", {"source_fact", "repository_contract", "gap_candidate", "analysis_boundary"}),
            "claim": _text(observation["claim"], f"{label}.claim"), "source": source, "target": target,
            "expected_static_outcome": outcome, "locations": locations,
            "reason": _text(observation["reason"], f"{label}.reason"),
            "certainty": _enum(observation["certainty"], f"{label}.certainty", {"source_confirmed", "conditional_risk", "unresolved"}),
            "conditions": _strings(observation["conditions"], f"{label}.conditions"),
            "counterevidence": _strings(observation["counterevidence"], f"{label}.counterevidence"),
            "priority": _enum(observation["priority"], f"{label}.priority", {"P1", "P2", "P3"}),
            "tool_support": {
                "version": _text(support["version"], f"{label}.tool_support.version", maximum=200),
                "state": _enum(support["state"], f"{label}.tool_support.state", {"supported", "partial", "unsupported", "not_evaluated"}),
                "required_capabilities": _strings(support["required_capabilities"], f"{label}.tool_support.required_capabilities"),
                "explanation": _text(support["explanation"], f"{label}.tool_support.explanation"),
                "snapshot_id": snapshot_id,
            },
        })
    return {"schema_version": 1, "baseline_id": _identifier(obj["baseline_id"], "baseline.baseline_id"),
            "status": "final", "repositories": repositories, "observations": observations}


def _json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON field: {key}")
        result[key] = value
    return result


def _invalid_constant(value: str) -> None:
    raise ValueError(f"Non-JSON numeric constant: {value}")


def load_baseline(path: str | Path) -> dict[str, Any]:
    """Load and validate a final v1 JSON baseline; no target paths are opened."""
    with Path(path).open("rb") as stream:
        content = stream.read(MAX_BASELINE_BYTES + 1)
    if len(content) > MAX_BASELINE_BYTES:
        raise ValueError("Baseline exceeds the 8 MiB data-file limit")
    try:
        raw = json.loads(content.decode("utf-8"), object_pairs_hook=_json_object, parse_constant=_invalid_constant)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise ValueError(f"Invalid baseline JSON: {exc}") from exc
    return _validate_baseline(raw)


def _lexical(node: Node) -> str:
    # Frontend IDs prefix the file/module; remove that exact prefix only.
    if node.qualname.startswith(node.module + "#"):
        return node.qualname[len(node.module) + 1:]
    return node.qualname


def _symbols(node: Node, language: str) -> set[str]:
    lexical = _lexical(node)
    symbols = {lexical}
    if language == "rust":
        trait = _TRAIT_METHOD.fullmatch(lexical)
        if trait:
            symbols.add(trait["prefix"] + trait["owner"] + "." + trait["method"])
    return symbols


def _model_summary(value: dict[str, Any]) -> dict[str, Any]:
    """Keep model premises visible without copying namespaces/provider trees."""
    fields = ("id", "profile_id", "version", "model_version", "receiver_type", "trait", "basis", "registration",
              "standard_library_source_captured", "project_toolchain_verified", "macro_expansion_performed",
              "generated_members_unknown", "complete_within_model", "complete_within_profile", "trait_bodies_known",
              "generated_inherent_and_deref_members_assumed_absent", "actual_macro_expansion_captured",
              "generated_bodies_known")
    summary = {}
    for key in fields:
        item = value.get(key)
        if isinstance(item, str):
            summary[key] = item[:1000]
        elif item is None or type(item) in {bool, int}:
            if key in value:
                summary[key] = item
    assumptions = value.get("assumptions", [])
    if isinstance(assumptions, list):
        sample = [item[:1000] for item in assumptions[:SAMPLE_LIMIT] if isinstance(item, str)]
        summary.update(assumption_count=len(assumptions), assumption_sample=sample,
                       assumptions_truncated=len(assumptions) > len(sample)
                       or any(isinstance(item, str) and len(item) > 1000 for item in assumptions[:SAMPLE_LIMIT]))
    return summary


def _generic_impl_summary(value: dict[str, Any]) -> dict[str, Any]:
    """Keep same-impl declarations and unverified premises, not namespaces."""
    fields = (
        "model_id", "basis", "receiver_form", "source_method", "target_method",
        "generic_instantiation_verified", "bounds_not_verified", "argument_types_verified",
        "execution_verified", "compiler_namespace_complete", "macro_expansion_performed",
        "explicit_argument_count", "target_explicit_parameter_count",
    )
    summary: dict[str, Any] = {}
    for key in fields:
        item = value.get(key)
        if isinstance(item, str):
            summary[key] = item[:1000]
            if len(item) > 1000:
                summary[key + "_truncated"] = True
        elif key in value and (item is None or type(item) in {bool, int}):
            summary[key] = item
    for key in ("assumptions", "residual_boundaries", "source_method_constraint_gaps", "target_method_constraint_gaps"):
        items = value.get(key)
        if isinstance(items, list):
            sample = [item[:1000] for item in items[:SAMPLE_LIMIT] if isinstance(item, str)]
            summary[key] = {"count": len(items), "sample": sample,
                            "truncated": len(items) > len(sample)
                            or any(isinstance(item, str) and len(item) > 1000 for item in items[:SAMPLE_LIMIT])}
    location_fields = ("file", "source_hash", "start_byte", "end_byte", "line", "column", "end_line", "end_column")
    for key in ("same_impl_identity", "source_declaration", "target_declaration"):
        item = value.get(key)
        if not isinstance(item, dict):
            continue
        record: dict[str, Any] = {}
        for name in (*location_fields, "header"):
            part = item.get(name)
            if isinstance(part, str):
                record[name] = part[:1000]
                if len(part) > 1000:
                    record[name + "_truncated"] = True
            elif type(part) is int:
                record[name] = part
        location = item.get("declaration_location")
        if isinstance(location, dict):
            record["declaration_location"] = {
                name: part[:1000] if isinstance(part, str) else part
                for name in location_fields
                if isinstance((part := location.get(name)), str) or type(part) is int
            }
        summary[key] = record
    return summary


def _binding_models(edge: Edge, snapshot_id: str) -> dict[str, Any]:
    helper = edge.metadata.get("receiver_helper_model")
    interfaces = edge.metadata.get("receiver_standard_interface_models")
    generic_impl = edge.metadata.get("generic_impl_binding")
    fields = [key for key, value in (("receiver_helper_model", helper), ("receiver_standard_interface_models", interfaces),
                                    ("generic_impl_binding", generic_impl)) if value]
    if not fields:
        return {"present": False}
    result = {"present": True,
              "interpretation": "Binding depends on registered trusted receiver/interface models; this is not captured macro-body or project-toolchain proof",
              "full_evidence_pointer": {"snapshot_id": snapshot_id, "edge_id": edge.id,
                                        "metadata_fields": fields}}
    if isinstance(helper, dict):
        result["helper_model"] = _model_summary(helper)
        receiver_interface = helper.get("receiver_interface_model")
        if isinstance(receiver_interface, dict):
            result["helper_model"]["receiver_interface"] = _model_summary(receiver_interface)
    if isinstance(interfaces, list):
        sample = [_model_summary(item) for item in interfaces[:SAMPLE_LIMIT] if isinstance(item, dict)]
        result["standard_interface_models"] = {"count": len(interfaces), "sample": sample,
                                               "truncated": len(interfaces) > len(sample)}
    if isinstance(generic_impl, dict):
        result["generic_impl_model"] = _generic_impl_summary(generic_impl)
        result["generic_impl_model"]["edge_resolution"] = edge.resolution
        basis = edge.metadata.get("binding_basis")
        if isinstance(basis, str):
            result["generic_impl_model"]["binding_basis"] = basis[:1000]
            result["full_evidence_pointer"]["metadata_fields"].append("binding_basis")
        result["interpretation"] = (
            "Generic same-impl metadata records finite captured lexical premises; resolution remains the edge's stated result. "
            "Any accompanying receiver/interface models retain their own assumptions. "
            "Generic instantiation, bounds, argument types, compiler namespaces, macro expansion and execution are not verified"
        )
    return result


class _Evaluation:
    def __init__(self, snapshot: GraphSnapshot, repository: dict[str, Any], observations: list[dict[str, Any]]):
        self.snapshot, self.repository = snapshot, repository
        self.index = GraphIndex(snapshot)
        self.files: dict[str, SourceFile] = {}
        self.duplicate_files = set()
        for source in snapshot.files:
            if source.path in self.files:
                self.duplicate_files.add(source.path)
            self.files[source.path] = source
        support_inputs = getattr(snapshot, "input_evidence", {})
        if not isinstance(support_inputs, dict):
            raise ValueError("snapshot.input_evidence must be a path-to-record object")
        self.support_inputs = support_inputs
        self.support_checks: dict[str, tuple[dict[str, Any] | None, str | None]] = {}
        self.duplicate_nodes = {node_id for node_id, count in Counter(node.id for node in snapshot.nodes).items() if count > 1}
        self.nodes_by_file: dict[str, list[Node]] = {}
        for node in snapshot.nodes:
            if node.file in repository["source_files"]:
                self.nodes_by_file.setdefault(node.file, []).append(node)
        self.lines: dict[tuple[str, bool], list[str]] = {}
        self.file_checks = {path: self.file_check(path) for path in repository["source_files"]}
        sites = {(location["path"], location["line"], location["end_line"])
                 for observation in observations for location in observation["locations"] if location["role"] == "call_site"}
        ranges_by_file: dict[str, list[tuple[int, int]]] = {}
        for path, line, end_line in sites:
            ranges_by_file.setdefault(path, []).append((line, end_line))
        self.edges_by_file: dict[str, list[Edge]] = {}
        for edge in snapshot.edges:
            if any(first <= edge.line <= last for first, last in ranges_by_file.get(edge.file, [])):
                self.edges_by_file.setdefault(edge.file, []).append(edge)

    def support_record(self, path: str) -> tuple[dict[str, Any] | None, str | None]:
        """Validate inert support evidence without creating a code SourceFile.

        UTF-8-sig capture preserves raw bytes except one optional initial BOM.
        Check both permitted original-byte forms, as well as the decoded-text
        SHA, before treating a support record as authenticated captured text.
        """
        if path in self.support_checks:
            return self.support_checks[path]
        record = self.support_inputs.get(path)
        error = None
        if not isinstance(record, dict) or record.get("path") != path:
            error = "Support input record does not match its canonical path key"
        elif record.get("kind", "support_input") != "support_input":
            error = "Support input record has a different evidence kind"
        elif record.get("status") != "captured" or record.get("error") is not None:
            error = "Support input has no successful captured-text record"
        elif (not isinstance(record.get("hash"), str) or not _SHA256.fullmatch(record["hash"])
              or not isinstance(record.get("text_hash"), str) or not _SHA256.fullmatch(record["text_hash"])
              or not isinstance(record.get("content"), str)):
            error = "Support input requires original-byte SHA256, text SHA256 and captured text"
        else:
            try:
                raw = record["content"].encode("utf-8")
            except UnicodeError:
                error = "Support input text cannot be represented by its declared UTF-8 capture"
            else:
                text_hash = sha256(raw).hexdigest()
                byte_forms = {text_hash: len(raw), sha256(b"\xef\xbb\xbf" + raw).hexdigest(): len(raw) + 3}
                if text_hash != record["text_hash"]:
                    error = "Support input text SHA256 does not match captured content"
                elif record["hash"] not in byte_forms:
                    error = "Support input original-byte SHA256 does not match UTF-8-sig captured content"
                elif "size_bytes" in record and (type(record["size_bytes"]) is not int
                                                  or record["size_bytes"] != byte_forms[record["hash"]]):
                    error = "Support input byte size disagrees with its original-byte identity"
        checked = (None, error) if error else (record, None)
        self.support_checks[path] = checked
        return checked

    def file_check(self, path: str, *, allow_support: bool = True) -> dict[str, Any]:
        source = self.files.get(path)
        expected = self.repository["source_files"][path]
        result = {"path": path, "expected_hash": expected, "source_hash": source.hash if source else None,
                  "source_status": source.status if source else "not_in_snapshot", "status": "matched",
                  "evidence_origin": "source_file" if source else None}
        if path in self.duplicate_files:
            result.update(status="evidence_unavailable", reason="Snapshot contains multiple source records for this path")
            return result
        if path in self.support_inputs:
            support, error = self.support_record(path)
            result["support_input_available"] = support is not None
            if error:
                result.update(status="evidence_unavailable", reason=error)
                return result
            result["support_source_hash"] = support["hash"]
            result["support_text_hash"] = support["text_hash"]
            if source is not None and (source.hash != support["hash"] or source.content != support["content"]):
                result.update(status="evidence_unavailable", reason="Code and support records disagree on the same path's source identity")
                return result
            if source is None:
                result.update(source_hash=support["hash"], source_status="captured_support_input", evidence_origin="support_input")
                if support["hash"] != expected:
                    result.update(status="source_changed", reason="Captured support byte hash differs from the frozen baseline")
                elif not allow_support:
                    result.update(status="source_missing", reason="Captured support text cannot supply a parsed code source or caller")
                return result
        if source is None:
            result.update(status="source_missing", reason="The baseline file was not captured in this snapshot")
        elif not isinstance(source.hash, str) or not _SHA256.fullmatch(source.hash):
            result.update(status="evidence_unavailable", reason="The snapshot has no usable original-byte SHA256")
        elif source.hash != expected:
            result.update(status="source_changed", reason="Captured source hash differs from the frozen baseline")
        elif not isinstance(source.content, str) or source.status in {"read_error", "too_large"}:
            result.update(status="evidence_unavailable", reason="The source hash is present but captured text is unavailable")
        return result

    def evidence_source(self, path: str, *, allow_support: bool = False) -> dict[str, Any]:
        source = self.files.get(path)
        if source is not None:
            return {"content": source.content, "hash": source.hash,
                    "source_status": source.status, "evidence_origin": "source_file"}
        if allow_support and path in self.support_inputs:
            support, error = self.support_record(path)
            if support is not None and error is None:
                return {"content": support["content"], "hash": support["hash"],
                        "source_status": "captured_support_input", "evidence_origin": "support_input"}
        raise ValueError("Verified captured source evidence is unavailable for this path")

    def source_lines(self, path: str, *, allow_support: bool = False) -> list[str]:
        key = (path, allow_support)
        if key not in self.lines:
            self.lines[key] = self.evidence_source(path, allow_support=allow_support)["content"].splitlines()
        return self.lines[key]

    def line_block(self, location: dict[str, Any], *, allow_support: bool = False) -> str:
        lines = self.source_lines(location["path"], allow_support=allow_support)
        block = "\n".join(lines[location["line"] - 1:location["end_line"]])
        # The terminating newline belongs to the last cited physical line.
        # Some frozen multiline quotes include it (e.g. ensure_thread).
        content = self.evidence_source(location["path"], allow_support=allow_support)["content"]
        if location["end_line"] < len(lines) or content.endswith(("\n", "\r")):
            block += "\n"
        return block

    def location(self, location: dict[str, Any], *, allow_support: bool = False) -> dict[str, Any]:
        source = self.evidence_source(location["path"], allow_support=allow_support)
        result = {**location, "expected_quote": location["quote"], "source_hash": source["hash"],
                  "source_status": source["source_status"], "evidence_origin": source["evidence_origin"],
                  "quote_matched": False, "snapshot_quote": None}
        lines = self.source_lines(location["path"], allow_support=allow_support)
        if location["end_line"] > len(lines):
            result["reason"] = "The baseline line range extends beyond captured source"
            return result
        block = self.line_block(location, allow_support=allow_support)
        quote = location["quote"].replace("\r\n", "\n")
        position = block.find(quote)
        if position < 0:
            result["reason"] = "The quote is absent from its frozen inclusive line range"
        else:
            result.update(quote_matched=True, snapshot_quote=block[position:position + len(quote)])
        return result

    def endpoint(self, selector: dict[str, str] | None) -> dict[str, Any] | None:
        if selector is None:
            return None
        matches = []
        source = self.files.get(selector["path"])
        # Auxiliary text never supplies code nodes, including malicious orphan
        # nodes in a malformed snapshot that has no original SourceFile.
        for node in self.nodes_by_file.get(selector["path"], []) if source is not None else []:
            language = node.metadata.get("language") or (source.language if source else None)
            if language == selector["language"] and selector["symbol"] in _symbols(node, language):
                matches.append(node)
        ambiguous = len(matches) > 1 or any(node.id in self.index.ambiguous_definitions or node.id in self.duplicate_nodes for node in matches)
        return {"selector": dict(selector), "status": "ambiguous" if ambiguous else "matched" if matches else "missing",
                "node_ids": sorted({node.id for node in matches}), "match_count": len(matches),
                "source_status": source.status if source else self.file_checks[selector["path"]]["source_status"]}

    def site_edges(self, location: dict[str, Any], owner: str | None = None) -> list[Edge]:
        """Locate the recorded callee at its byte column inside the actual quote.

        A line range alone cannot distinguish multiple calls. All matching
        anchors remain candidates, and callers must handle that ambiguity.
        Synthetic declaration/activation edges are not source call sites.
        """
        lines = self.source_lines(location["path"])
        block = self.line_block(location)
        quote = location["quote"].replace("\r\n", "\n")
        spans, start = [], 0
        while True:
            position = block.find(quote, start)
            if position < 0:
                break
            spans.append((position, position + len(quote)))
            start = position + 1
        candidates = []
        for edge in self.edges_by_file.get(location["path"], []):
            if not location["line"] <= edge.line <= location["end_line"] or (owner is not None and edge.source != owner):
                continue
            if edge.metadata.get("implicit") or edge.source not in self.index.nodes:
                continue
            if not isinstance(edge.expression, str) or not edge.expression or type(edge.column) is not int or edge.column < 0:
                continue
            line = lines[edge.line - 1]
            raw = line.encode("utf-8")
            if edge.column > len(raw):
                continue
            try:
                prefix = raw[:edge.column].decode("utf-8")
            except UnicodeError:
                continue
            offset = sum(len(value) + 1 for value in lines[location["line"] - 1:edge.line - 1]) + len(prefix)
            expression = edge.expression.replace("\r\n", "\n")
            if block[offset:offset + len(expression)] != expression:
                continue
            if any(first <= offset and offset + len(expression) <= last for first, last in spans):
                candidates.append(edge)
        return sorted(candidates, key=lambda edge: (edge.line, edge.column, edge.id))

    def known(self, edge: Edge) -> bool:
        if (edge.resolution != "resolved" or edge.target not in self.index.nodes
                or edge.source not in self.index.nodes
                or {edge.source, edge.target} & (self.index.ambiguous_definitions | self.duplicate_nodes)):
            return False
        # Partial parsing can leave structurally plausible resolved remnants.
        # Require the two involved files, not unrelated global files, to parse.
        for node_id in (edge.source, edge.target):
            file = self.files.get(self.index.nodes[node_id].file)
            if file is None or file.status not in _COMPLETE or file.path in self.duplicate_files:
                return False
        return True

    def witness(self, edge: Edge) -> dict[str, Any]:
        source = self.files.get(edge.file)
        lines = self.source_lines(edge.file) if source else []
        line = lines[edge.line - 1] if 1 <= edge.line <= len(lines) else ""
        return {"edge_id": edge.id, "source": edge.source, "target": edge.target, "file": edge.file,
                "line": edge.line, "column": edge.column, "expression": edge.expression,
                "resolution": edge.resolution, "effective_internal_binding": self.known(edge),
                "source_hash": source.hash if source else None, "source_line": line[:4000],
                "source_line_truncated": len(line) > 4000, "reason": edge.reason,
                "candidate_count": len(edge.candidates), "candidate_sample": edge.candidates[:SAMPLE_LIMIT],
                "binding_models": _binding_models(edge, self.snapshot.id)}

    def gaps(self, node_ids: set[str]) -> dict[str, Any]:
        unknown = sum(len(self.index.unknown.get(node, [])) for node in node_ids)
        callbacks = sum(len(self.index.callback_boundaries.get(node, [])) for node in node_ids)
        return {"coverage_gap_count": len(self.index.coverage_gaps), "integrity_gap_count": len(self.index.integrity_gaps),
                "scope_unknown_call_count": unknown, "scope_callback_boundary_count": callbacks,
                "snapshot_id": self.snapshot.id, "full_evidence": "snapshot_edges_diagnostics_source_statuses"}


def _finish(item: dict[str, Any], status: str, code: str, reason: str, *, satisfied: bool | None = False) -> dict[str, Any]:
    item.update(status=status, reason_code=code, evaluation_reason=reason, expectation_satisfied=satisfied)
    item["missing_capabilities"] = [] if satisfied is True else list(item["required_capabilities"])
    item["capability_assessment_scope"] = "observation_expectation_only_not_individual_capability_certification"
    return item


def _evaluate_observation(context: _Evaluation, observation: dict[str, Any]) -> dict[str, Any]:
    outcome = observation["expected_static_outcome"]
    item = {key: observation[key] for key in ("id", "repo", "commit", "category", "claim", "source", "target",
            "expected_static_outcome", "certainty", "conditions", "counterevidence", "priority")}
    item.update(baseline_reason=observation["reason"], reference_tool_support=observation["tool_support"],
                required_capabilities=list(observation["tool_support"]["required_capabilities"]),
                snapshot_id=context.snapshot.id, witness=[], locations=[], endpoint_status={"source": None, "target": None},
                automatically_adjudicated=False, target_repository_defect=False)
    paths = {location["path"] for location in observation["locations"]}
    paths.update(selector["path"] for selector in (observation["source"], observation["target"]) if selector)
    allow_support = outcome == "evidence_only"
    checks = [context.file_check(path, allow_support=allow_support) for path in sorted(paths)]
    item["source_checks"] = checks
    # A changed source identity dominates parse/binding gaps and missing files.
    for status in ("source_changed", "source_missing", "evidence_unavailable"):
        if any(check["status"] == status for check in checks):
            item["locations"] = [{**location, "quote_matched": None} for location in observation["locations"]]
            return _finish(item, status, status, "Frozen source identity/evidence does not match this saved snapshot")
    item["locations"] = [context.location(location, allow_support=allow_support) for location in observation["locations"]]
    if any(not location["quote_matched"] for location in item["locations"]):
        return _finish(item, "evidence_unavailable", "quote_not_verified", "At least one frozen quote was not found at its specified captured line range")
    endpoints = {"source": context.endpoint(observation["source"]), "target": context.endpoint(observation["target"])}
    item["endpoint_status"] = endpoints
    if outcome == "evidence_only":
        return _finish(item, "evidence_only", "higher_order_observation", "Captured source evidence is preserved; call-graph matching cannot adjudicate this observation", satisfied=None)
    required_endpoints = [endpoints["source"]]
    if outcome != "unknown_required":
        required_endpoints.append(endpoints["target"])
    if any(endpoint["status"] == "ambiguous" for endpoint in required_endpoints):
        return _finish(item, "ambiguous", "endpoint_ambiguous", "The file-scoped lexical selector does not identify one implementation")
    missing = [endpoint for endpoint in required_endpoints if endpoint["status"] == "missing"]
    if missing:
        parse_incomplete = any(endpoint["source_status"] not in _COMPLETE for endpoint in missing)
        return _finish(item, "unknown" if parse_incomplete else "endpoint_missing",
                       "endpoint_analysis_incomplete" if parse_incomplete else "endpoint_missing",
                       "A required caller/target is absent; absence is not preservation of an unknown call")
    source_id = endpoints["source"]["node_ids"][0]
    target_id = endpoints["target"]["node_ids"][0] if outcome != "unknown_required" else None
    item["gap_summary"] = context.gaps({source_id})
    if outcome == "no_direct_call_in_explicit_model":
        direct = [edge for edge in context.index.outgoing[source_id] if edge.target == target_id and context.known(edge)]
        if direct:
            item["witness"] = [context.witness(edge) for edge in direct[:SAMPLE_LIMIT]]
            return _finish(item, "mismatch", "direct_call_present", "The explicit model contains a direct call to this target")
        if context.index.coverage_gaps or context.index.integrity_gaps or context.index.unknown[source_id] or context.index.callback_boundaries[source_id]:
            return _finish(item, "unknown", "negative_binding_incomplete", "Analysis gaps prevent a definite negative direct-call claim")
        return _finish(item, "reproduced", "no_direct_call", "No direct call exists in the complete explicit static model", satisfied=True)
    locations = [location for location in observation["locations"] if location["role"] == "call_site"]
    if outcome != "confirmed_static_path":
        locations = [location for location in locations if location["path"] == observation["source"]["path"]]
    matches = [context.site_edges(location, None if outcome == "confirmed_static_path" else source_id) for location in locations]
    if any(len(edges) > 1 for edges in matches):
        item["witness"] = [context.witness(edge) for edges in matches for edge in edges[:SAMPLE_LIMIT]][:SAMPLE_LIMIT]
        return _finish(item, "ambiguous", "call_site_ambiguous", "The caller and frozen quote identify multiple calls; a line-only range cannot select one")
    if any(not edges for edges in matches):
        incomplete = any(context.files[location["path"]].status not in _COMPLETE for location, edges in zip(locations, matches) if not edges)
        return _finish(item, "unknown" if incomplete else "mismatch", "call_site_not_captured",
                       "The actual call at the frozen quote/position has no matching graph edge")
    edges = [edges[0] for edges in matches]
    item["witness"] = [context.witness(edge) for edge in edges]
    if outcome == "unknown_required":
        if all(edge.resolution in {"dynamic", "unresolved", "ambiguous"}
               and edge.target is None and isinstance(edge.reason, str) and edge.reason.strip()
               for edge in edges):
            return _finish(item, "unknown", "actual_unknown_preserved", "The unique caller and actual quoted call site retain an unbound internal target and its reason", satisfied=True)
        if any((edge.resolution == "resolved" and not context.known(edge))
               or (edge.resolution in {"dynamic", "unresolved", "ambiguous"}
                   and (edge.target is not None or not isinstance(edge.reason, str) or not edge.reason.strip()))
               for edge in edges):
            return _finish(item, "unknown", "unknown_evidence_invalid", "A dangling/invalid binding or missing unknown reason does not preserve the required uncertainty")
        return _finish(item, "mismatch", "required_unknown_not_preserved", "The quoted call was classified as a definite/internal or external binding rather than the required residual unknown")
    if any(not context.known(edge) for edge in edges):
        return _finish(item, "unknown", "call_binding_incomplete", "At least one quoted call lacks a unique resolved internal target")
    if outcome == "confirmed_static_call":
        if all(edge.source == source_id and edge.target == target_id for edge in edges):
            return _finish(item, "reproduced", "confirmed_call_at_quote", "A unique internal call binding matches the caller, target file and frozen call site", satisfied=True)
        return _finish(item, "mismatch", "different_target_at_quote", "The actual quoted call resolves to a different target")
    # Only frozen, verified call positions may compose this path witness. This
    # avoids satisfying the observation through an unrelated alternative path.
    allowed = {edge.id for edge in edges}
    parents: dict[str, tuple[str, Edge] | None] = {source_id: None}
    queue = deque([source_id])
    path_edges = []
    while queue and not path_edges:
        node = queue.popleft()
        for edge in context.index.outgoing[node]:
            if edge.id not in allowed:
                continue
            if edge.target == target_id:
                path_edges = [edge]
                cursor = node
                while parents[cursor] is not None:
                    cursor, previous_edge = parents[cursor]
                    path_edges.append(previous_edge)
                path_edges.reverse()
                break
            if edge.target not in parents:
                parents[edge.target] = (node, edge)
                queue.append(edge.target)
    item["path"] = {"node_ids": [source_id, *[edge.target for edge in path_edges]] if path_edges else [],
                    "edge_ids": [edge.id for edge in path_edges], "minimum_edges": 1,
                    "length": len(path_edges), "visited_nodes": len(parents), "scope": "frozen_quoted_static_calls"}
    if path_edges:
        item["witness"] = [context.witness(edge) for edge in path_edges]
        return _finish(item, "reproduced", "positive_quoted_path", "Verified explicit calls form a positive-length path between the unique endpoints", satisfied=True)
    return _finish(item, "mismatch", "quoted_path_not_connected", "The verified explicit call positions do not form the claimed positive-length path")


def evaluate_baseline(snapshot: GraphSnapshot, baseline: dict[str, Any], repo_id: str | None = None) -> dict[str, Any]:
    """Evaluate every observation of one repository against one saved snapshot.

    Other repository observations are explicitly counted, not failed against an
    unrelated project. The global denominator and outcome counts retain all
    baseline items; selected counts include evidence-only and unknown items.
    """
    if not isinstance(snapshot, GraphSnapshot):
        raise ValueError("snapshot must be a GraphSnapshot")
    baseline = _validate_baseline(baseline)
    if repo_id is not None:
        repo_id = _identifier(repo_id, "repo_id")
        repositories = [repo for repo in baseline["repositories"] if repo["id"] == repo_id]
    else:
        # Lexical root comparison only; do not resolve/read current target paths.
        repositories = [repo for repo in baseline["repositories"] if repo["root"] == str(PurePosixPath(snapshot.root))]
    if len(repositories) != 1:
        raise ValueError("Choose exactly one baseline repository with repo_id (snapshot root did not identify one)")
    repository = repositories[0]
    selected = [observation for observation in baseline["observations"] if observation["repo"] == repository["id"]]
    context = _Evaluation(snapshot, repository, selected)
    observations = [_evaluate_observation(context, observation) for observation in selected]
    counts = {status: sum(observation["status"] == status for observation in observations) for status in _STATUSES}
    expected_counts = {outcome: sum(observation["expected_static_outcome"] == outcome for observation in baseline["observations"]) for outcome in _OUTCOMES}
    selected_expected_counts = {outcome: sum(observation["expected_static_outcome"] == outcome for observation in selected) for outcome in _OUTCOMES}
    by_outcome = {outcome: {
        "total": selected_expected_counts[outcome],
        "status_counts": {status: sum(observation["expected_static_outcome"] == outcome and observation["status"] == status for observation in observations) for status in _STATUSES},
        "expectation_satisfied": sum(observation["expected_static_outcome"] == outcome and observation["expectation_satisfied"] is True for observation in observations),
    } for outcome in _OUTCOMES}
    return {
        "schema_version": 1, "evaluator_version": EVALUATOR_VERSION,
        "evaluator_source_hash": EVALUATOR_SOURCE_HASH,
        "evaluator_source_hash_scope": "implementation_loaded_at_module_import",
        "baseline_id": baseline["baseline_id"], "baseline_status": baseline["status"],
        "baseline_total": len(baseline["observations"]), "expected_counts": expected_counts,
        "selected_total": len(observations), "selected_expected_counts": selected_expected_counts,
        "remaining_repository_observations": len(baseline["observations"]) - len(observations),
        "repository": {"id": repository["id"], "root": repository["root"], "commit": repository["commit"]},
        "snapshot": {"id": snapshot.id, "project_id": snapshot.project_id, "root": snapshot.root,
                     "source_hash": snapshot.source_hash, "analyzer_version": snapshot.analyzer_version,
                     "detector_version": snapshot.detector_version, "parser_version": snapshot.parser_version,
                     "schema_version": snapshot.schema_version},
        "counts": counts, "by_expected_outcome": by_outcome,
        "expectation_satisfied_count": sum(observation["expectation_satisfied"] is True for observation in observations),
        "confirmed_reproduction_count": counts["reproduced"],
        "intentional_unknown_preserved_count": sum(observation["expected_static_outcome"] == "unknown_required" and observation["expectation_satisfied"] is True for observation in observations),
        "evidence_only_count": counts["evidence_only"],
        "source_checks": list(context.file_checks.values()), "observations": observations,
        "target_executed": False, "target_tests_run": False,
        "interpretation": "This is a frozen static-observation comparison, not project functional coverage, execution success or repository defect adjudication. Evidence-only items and intentional unknowns remain in the denominator.",
    }
