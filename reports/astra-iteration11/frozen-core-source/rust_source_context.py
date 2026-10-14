"""Narrow source-context models for Rust's built-in crate attributes.

This module never expands a macro or evaluates cfg.  In particular, a
recursion/type-length limit constrains compilation; it is not an attribute
macro that rewrites every declaration in the enclosing crate.  Recognition
requires a complete CST node at a configured crate root, rather than a global
attribute-name whitelist.
"""

from __future__ import annotations

import hashlib
import re
from typing import Any

SOURCE_CONTEXT_VERSION = "rust-captured-source-context-1"
BUILTIN_CRATE_LIMIT_MODEL = "rust-builtin-crate-limit-attribute-v1"
_LIMIT_ATTRIBUTES = {"recursion_limit", "type_length_limit"}


def classify_crate_inner_attribute(node: Any, raw: bytes, *,
                                   is_known_crate_root: bool) -> dict | None:
    """Return an inert-name-binding model only for explicit built-in limits.

    The caller must establish the configured crate-root identity.  The CST
    must independently establish a direct source-file inner attribute and a
    plain decimal string value.  Outer attributes, misplaced inner attributes,
    cfg_attr, namespaced attributes, token-tree values and unknown attributes
    deliberately have no model.  No compiler acceptance is asserted.
    """
    if (not is_known_crate_root or node is None or node.type != "inner_attribute_item"
            or node.parent is None or node.parent.type != "source_file" or node.has_error):
        return None
    named = list(node.named_children)
    if len(named) != 1 or named[0].type != "attribute":
        return None
    parts = list(named[0].named_children)
    if len(parts) != 2 or parts[0].type != "identifier" or parts[1].type != "string_literal":
        return None
    name = raw[parts[0].start_byte:parts[0].end_byte].decode("utf-8", "strict")
    if name not in _LIMIT_ATTRIBUTES:
        return None
    literal = raw[parts[1].start_byte:parts[1].end_byte].decode("utf-8", "strict")
    # Do not interpret escapes, raw strings, expressions or target-width limits.
    # An uninterpreted non-negative decimal literal is enough for this model's
    # name-binding distinction; it is not enough to certify successful compile.
    if not re.fullmatch(r'"[0-9]{1,10}"', literal):
        return None
    text = raw[node.start_byte:node.end_byte].decode("utf-8", "strict")
    if not re.fullmatch(r'#\s*!\s*\[\s*' + re.escape(name) + r'\s*=\s*' + re.escape(literal) + r'\s*\]', text):
        return None
    return {
        "model_id": BUILTIN_CRATE_LIMIT_MODEL,
        "source_context_version": SOURCE_CONTEXT_VERSION,
        "attribute_name": name,
        "literal_source": literal,
        "source": text,
        "start_byte": node.start_byte,
        "end_byte": node.end_byte,
        "line": node.start_point.row + 1,
        "end_line": node.end_point.row + 1,
        "span_sha256": hashlib.sha256(raw[node.start_byte:node.end_byte]).hexdigest(),
        "applies_to": "configured_crate_root_compilation_limit",
        "declaration_name_binding_transformed": False,
        "macro_expansion_performed": False,
        "cfg_evaluated": False,
        "compilation_validated": False,
        "macro_or_trait_target_resolution_closed": False,
    }
