"""Shared, serializable contracts. No target program is imported or executed."""

from dataclasses import asdict, dataclass, field
import hashlib
from pathlib import Path
import sys
from typing import Any

SCHEMA_VERSION = "2"
ANALYZER_VERSION = "static-multilang-15-codegraph"
DETECTOR_VERSION = "call-rules-13-architecture-explanations"
PARSER_VERSION = f"{sys.implementation.name}-{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def project_id_for(root: str | Path) -> str:
    return hashlib.sha256(str(Path(root).resolve()).encode("utf-8")).hexdigest()[:20]


@dataclass
class Node:
    id: str
    name: str
    qualname: str
    module: str
    file: str
    line: int
    end_line: int
    kind: str
    signature: str = ""
    layer: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Edge:
    id: str
    source: str
    target: str | None
    expression: str
    file: str
    line: int
    column: int = 0
    resolution: str = "resolved"
    candidates: list[str] = field(default_factory=list)
    reason: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Diagnostic:
    level: str
    code: str
    message: str
    file: str = ""
    line: int = 0


@dataclass
class SourceFile:
    path: str
    hash: str
    content: str
    status: str
    language: str = "python"
    error: str | None = None
    module: str = ""


@dataclass
class GraphSnapshot:
    id: str
    project_id: str
    project_name: str
    root: str
    created_at: str
    source_hash: str
    analyzer_version: str
    policy_hash: str
    status: str
    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)
    files: list[SourceFile] = field(default_factory=list)
    diagnostics: list[Diagnostic] = field(default_factory=list)
    stats: dict[str, Any] = field(default_factory=dict)
    config: dict[str, Any] = field(default_factory=dict)
    detector_version: str = DETECTOR_VERSION
    schema_version: str = SCHEMA_VERSION
    parser_version: str = PARSER_VERSION
    input_evidence: dict[str, dict[str, Any]] = field(default_factory=dict)


@dataclass
class Evidence:
    id: str
    kind: str
    message: str
    locations: list[dict[str, Any]] = field(default_factory=list)
    node_ids: list[str] = field(default_factory=list)
    edge_ids: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class Finding:
    id: str
    type: str
    severity: str
    status: str
    title: str
    description: str
    node_ids: list[str] = field(default_factory=list)
    edge_ids: list[str] = field(default_factory=list)
    evidence: list[Evidence] = field(default_factory=list)
    rule_id: str = ""
    fingerprint: str = ""
    snapshot_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


def to_dict(value: Any) -> dict[str, Any]:
    return asdict(value)

