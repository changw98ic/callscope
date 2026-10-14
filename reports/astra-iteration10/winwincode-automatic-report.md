# WinWinCode / 项目源码静态调用核对：自动静态分析报告

快照：`ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28`；状态：`partial`。

仅使用保存源码、图和分析证据；未执行目标、测试或构建。

## 项目声明与结构

项目声明来自保存的 manifest；依赖和产品描述未被当作运行通过证据。

`Cargo.toml`：

```json
{
  "file": "Cargo.toml",
  "source_file_sha256": "e33d73f372e5e00e361ce7783743c977aceb07107effea3990886e71c0f7a5b4",
  "text_sha256": "e33d73f372e5e00e361ce7783743c977aceb07107effea3990886e71c0f7a5b4",
  "origin": "captured-project-declaration",
  "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28",
  "format": "toml",
  "package_declarations": {},
  "workspace_members": [
    "crates/helper",
    "crates/kernel",
    "crates/winwincode-api",
    "crates/winwincode-audit",
    "crates/winwincode-cli",
    "crates/winwincode-client-port",
    "crates/winwincode-delivery",
    "crates/winwincode-device-client",
    "crates/winwincode-control-plane",
    "crates/winwincode-codex",
    "crates/winwincode-data-export",
    "crates/winwincode-domain",
    "crates/winwincode-execution-port",
    "crates/winwincode-evidence-export",
    "crates/winwincode-fusion",
    "crates/winwincode-connector-github",
    "crates/winwincode-connector-jira",
    "crates/winwincode-connector-linear",
    "crates/winwincode-connector-slack",
    "crates/winwincode-connector-teams",
    "crates/winwincode-connector-webhook",
    "crates/winwincode-integration-core",
    "crates/winwincode-integration-sqlite",
    "crates/winwincode-local",
    "crates/winwincode-observability-core",
    "crates/winwincode-observability-sqlite",
    "crates/winwincode-s3-artifact-adapter",
    "crates/winwincode-provider",
    "crates/winwincode-publication",
    "crates/winwincode-repository-context",
    "crates/winwincode-server",
    "crates/winwincode-session",
    "crates/winwincode-storage",
    "crates/winwincode-test-assets",
    "crates/winwincode-worker"
  ],
  "workspace_exclusions": [
    "third_party/codex/codex-rs",
    "upstream/vendor/i18n-embed-fl-0.9.4",
    "upstream/vendor/rusqlite-0.39.0"
  ],
  "workspace_package": {
    "version": "0.1.0-alpha.2",
    "edition": "2024",
    "rust-version": "1.95",
    "license": "Apache-2.0",
    "repository": "https://github.com/changw98ic/winwincode"
  },
  "declared_dependencies": {},
  "dependency_availability_verified": false
}
```

`crates/winwincode-api/Cargo.toml`：

```json
{
  "file": "crates/winwincode-api/Cargo.toml",
  "source_file_sha256": "d09555f1bf9921e1cc5f5d796150dc7aff5b4aa5a78d67e6f9adee70530f9de7",
  "text_sha256": "d09555f1bf9921e1cc5f5d796150dc7aff5b4aa5a78d67e6f9adee70530f9de7",
  "origin": "captured-project-declaration",
  "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28",
  "format": "toml",
  "package_declarations": {
    "name": "winwincode-api",
    "description": "Generated public HTTP/WebSocket transport types for the WinWinCode Control Plane",
    "version": {
      "workspace": true
    },
    "edition": {
      "workspace": true
    },
    "rust-version": {
      "workspace": true
    },
    "license": {
      "workspace": true
    },
    "repository": {
      "workspace": true
    },
    "include": [
      "src/**",
      "Cargo.toml",
      "README.md"
    ]
  },
  "workspace_members": [],
  "workspace_exclusions": [],
  "workspace_package": {},
  "declared_dependencies": {
    "winwincode-domain": {
      "workspace": true
    },
    "serde": {
      "workspace": true
    },
    "serde_json": {
      "workspace": true
    }
  },
  "dependency_availability_verified": false
}
```

`crates/winwincode-delivery/Cargo.toml`：

```json
{
  "file": "crates/winwincode-delivery/Cargo.toml",
  "source_file_sha256": "698553efb4d8f6f3a7677c624b25acbc0a93e49a1c2e5e3ead5ef055dc7b945c",
  "text_sha256": "698553efb4d8f6f3a7677c624b25acbc0a93e49a1c2e5e3ead5ef055dc7b945c",
  "origin": "captured-project-declaration",
  "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28",
  "format": "toml",
  "package_declarations": {
    "name": "winwincode-delivery",
    "description": "Canonical Delivery domain and append-only journal for the WinWinCode Control Plane",
    "version": {
      "workspace": true
    },
    "edition": {
      "workspace": true
    },
    "rust-version": {
      "workspace": true
    },
    "license": {
      "workspace": true
    },
    "repository": {
      "workspace": true
    },
    "include": [
      "src/**",
      "Cargo.toml",
      "README.md"
    ]
  },
  "workspace_members": [],
  "workspace_exclusions": [],
  "workspace_package": {},
  "declared_dependencies": {
    "base64": {
      "workspace": true
    },
    "serde": {
      "workspace": true
    },
    "serde_json": {
      "workspace": true
    },
    "sha2": {
      "workspace": true
    },
    "time": {
      "workspace": true
    },
    "winwincode-domain": {
      "workspace": true
    }
  },
  "dependency_availability_verified": false
}
```

`crates/winwincode-domain/Cargo.toml`：

```json
{
  "file": "crates/winwincode-domain/Cargo.toml",
  "source_file_sha256": "0f66a8a3d0c5b209a5c89b349e3dcca68b7f3f910935cfae5e48f65123cb087f",
  "text_sha256": "0f66a8a3d0c5b209a5c89b349e3dcca68b7f3f910935cfae5e48f65123cb087f",
  "origin": "captured-project-declaration",
  "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28",
  "format": "toml",
  "package_declarations": {
    "name": "winwincode-domain",
    "description": "Generated shared identifiers and scalar value objects for WinWinCode",
    "version": {
      "workspace": true
    },
    "edition": {
      "workspace": true
    },
    "rust-version": {
      "workspace": true
    },
    "license": {
      "workspace": true
    },
    "repository": {
      "workspace": true
    },
    "include": [
      "src/**",
      "Cargo.toml",
      "README.md"
    ]
  },
  "workspace_members": [],
  "workspace_exclusions": [],
  "workspace_package": {},
  "declared_dependencies": {
    "base64": {
      "workspace": true
    },
    "serde": {
      "workspace": true
    },
    "serde_json": {
      "workspace": true
    },
    "sha2": {
      "workspace": true
    }
  },
  "dependency_availability_verified": false
}
```

## 判断与证据

完整条件判断、局部分析和结构观察分别列出，不从图大小或解析率推断功能完整性。

- **WWC-01**：所选公开导航未提供消费者必需的查询上下文；经真实生产装配与缺值传播，创建在提交命令前被拒绝。有效上下文和替代创建入口是反证。
- **WWC-02**：所选提交对象遗漏条件分支必填字段；经过生成协议、普通 JSON 与 Serde 映射后，权威非空守卫在使用或提交前拒绝。其它分支和显式字段来源是反证。

### WWC-01

评估：`scoped_static_judgment_reproduced`；完整裁决：`true`。

保存发现：`333b5dc5882abce976c0d9dc`；证据：`1f75ceee5eab722beeb2d270`。

源码推导：

```json
"The selected source-derived absent-query path reaches the actual production port callback and rejects its create before command calls, under the retained platform/form conditions."
```

适用条件：

```json
[
  "用户沿所选href导航，提交时当前hash仍是该导航结果。",
  "使用标准浏览器DOM和URLSearchParams语义；不证明运行时改写或外部脚本行为。",
  "The mounted page and its source-returned model methods are used under the declared ordinary DOM/JS model; no external method monkey-patching.",
  "During the relevant route selector and deliveryContext hash reads, the current hash is the selected href navigation result; authentication, access, loading and lifecycle guards permit mounting.",
  "A submit event is delivered to the mounted form and all captured ViewModel form guards permit port.create."
]
```

反证与范围：

```json
{
  "alternate_factory": {
    "actual_binding": {
      "edge_id": "6aa8ad69bfe3b940e77c65a2",
      "kind": "snapshot_calls",
      "source_graph_node_id": "ts:apps/client/src/application#mountWinWinCodeClient",
      "target_graph_node_id": "ts:apps/client/src/community-control-plane-client#createControlPlaneTaskFake"
    },
    "source_fact_id": "navigation-fact:a3173d6a150ac307093bea76"
  },
  "independent_chat_source": {
    "actual_chat_success_proven": false,
    "fact_ids": [
      "navigation-fact:bfc82874eff4f87d8fd9ae50"
    ],
    "supported": true
  },
  "scope_exclusion_is_not_independent_chat_success_proof": true,
  "scope_exclusions": [
    "manual URL containing a valid required key is outside this producer's absent-key premise",
    "independent Chat creation uses a separate source entrance and is outside this navigation claim"
  ],
  "source_derived": [
    {
      "kind": "valid_seed_preserved",
      "producer": {
        "abstract_value": {
          "exact_text": null,
          "kind": "string",
          "runtime_execution_proven": false,
          "segments": [
            {
              "kind": "literal",
              "text": "#/home/review"
            },
            {
              "kind": "literal",
              "text": "?"
            },
            {
              "kind": "serialized",
              "source_value_id": "abstract-152"
            }
          ],
          "source_value_id": "abstract-158"
        },
        "analysis_gaps": [],
        "assignment_target_receiver_not_executed": true,
        "branch_conditions": [
          {
            "branch": "else",
            "condition": "card.deliveryId === null",
            "location": {
              "column": 12,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 8729,
              "end_column": 36,
              "end_line": 224,
              "file": "apps/client/src/home-dashboard-page.ts",
              "grammar": "typescript",
              "line": 224,
              "original_file_end_byte": 8729,
              "original_file_start_byte": 8705,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "709b4728fef637f15f8e0f4d0d42bd14002b4c594b473f770a337a40db908062",
              "source_excerpt": "card.deliveryId === null",
              "source_excerpt_truncated": false,
              "source_hash": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
              "source_line": "    return card.deliveryId === null",
              "span_hash": "bd185895278c25b39254a1378079df274f05389582eba8ed8ac7ef6cb8938398",
              "start_byte": 8705
            }
          },
          {
            "branch": "then",
            "condition": "(card.kind === 'attention')",
            "location": {
              "column": 6,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 8691,
              "end_column": 33,
              "end_line": 223,
              "file": "apps/client/src/home-dashboard-page.ts",
              "grammar": "typescript",
              "line": 223,
              "original_file_end_byte": 8691,
              "original_file_start_byte": 8664,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "709b4728fef637f15f8e0f4d0d42bd14002b4c594b473f770a337a40db908062",
              "source_excerpt": "(card.kind === 'attention')",
              "source_excerpt_truncated": false,
              "source_hash": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
              "source_line": "  if (card.kind === 'attention') {",
              "span_hash": "311d18d145c2f689f4c29566067dfaef46d7b81a24457e44853bdc170c270136",
              "start_byte": 8664
            }
          }
        ],
        "declaration": {
          "graph_node_id": "ts:apps/client/src/home-dashboard-page#homeDecisionHash",
          "location": {
            "column": 8,
            "column_base": 1,
            "column_unit": "utf8_bytes",
            "coordinate_space": "captured_text_utf8",
            "end_byte": 8958,
            "end_column": 2,
            "end_line": 230,
            "file": "apps/client/src/home-dashboard-page.ts",
            "grammar": "typescript",
            "line": 219,
            "original_file_end_byte": 8958,
            "original_file_start_byte": 8548,
            "parse_identity": {
              "coordinate_space": "captured_text_utf8",
              "derived_text_utf8_sha256": null,
              "literal_authority": "original_saved_source_text_only",
              "original_text_utf8_sha256": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
              "position_map": "identity_utf8_bytes_and_line_columns",
              "projection_mode": "original",
              "projection_version": "ts-syntax-projection-1",
              "raw_prefix_bytes": 0,
              "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "semantic_source_version": "semantic-snapshot-sources-1",
              "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
            },
            "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
            "raw_prefix_bytes": 0,
            "semantic_parse_id": "709b4728fef637f15f8e0f4d0d42bd14002b4c594b473f770a337a40db908062",
            "source_excerpt": "function homeDecisionHash(\n  card: HomeDecisionCard,\n  scopeSelection: ScopeRouteSelection,\n): string | null {\n  if (card.kind === 'attention') {\n    return card.deliveryId === null\n      ? null\n      : scopeHash(`#/home/review?delivery=${encodeURIComponent(card.deliveryId)}`, scopeSelection)\n  }\n  if (card.productSessionId === null) return null\n  return homeChatHash(card.productSessionId, scopeSelection)\n}",
            "source_excerpt_truncated": false,
            "source_hash": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
            "source_line": "export function homeDecisionHash(",
            "span_hash": "c6aa85d0a4e9851011c34454eac7379adc3ffc6e9c165148952c6b6e772a767c",
            "start_byte": 8548
          },
          "symbol": "homeDecisionHash"
        },
        "expression_location": {
          "column": 9,
          "column_base": 1,
          "column_unit": "utf8_bytes",
          "coordinate_space": "captured_text_utf8",
          "end_byte": 8841,
          "end_column": 99,
          "end_line": 226,
          "file": "apps/client/src/home-dashboard-page.ts",
          "grammar": "typescript",
          "line": 226,
          "original_file_end_byte": 8841,
          "original_file_start_byte": 8751,
          "parse_identity": {
            "coordinate_space": "captured_text_utf8",
            "derived_text_utf8_sha256": null,
            "literal_authority": "original_saved_source_text_only",
            "original_text_utf8_sha256": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
            "position_map": "identity_utf8_bytes_and_line_columns",
            "projection_mode": "original",
            "projection_version": "ts-syntax-projection-1",
            "raw_prefix_bytes": 0,
            "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
            "semantic_source_version": "semantic-snapshot-sources-1",
            "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
          },
          "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
          "raw_prefix_bytes": 0,
          "semantic_parse_id": "709b4728fef637f15f8e0f4d0d42bd14002b4c594b473f770a337a40db908062",
          "source_excerpt": "scopeHash(`#/home/review?delivery=${encodeURIComponent(card.deliveryId)}`, scopeSelection)",
          "source_excerpt_truncated": false,
          "source_hash": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
          "source_line": "      : scopeHash(`#/home/review?delivery=${encodeURIComponent(card.deliveryId)}`, scopeSelection)",
          "span_hash": "37a6bb71e84d60b80259cbb25cd94d9beb10b1074cd93640d12f965106f0bc82",
          "start_byte": 8751
        },
        "query_domain": {
          "guaranteed_keys": [
            "delivery"
          ],
          "invariant": "guaranteed subset actual subset possible only when keyset_closed",
          "keyset_closed": true,
          "possible_keys": [
            "delivery",
            "organizationId",
            "projectId",
            "repositoryId",
            "workspaceId"
          ],
          "unknown_keys": false,
          "unknown_reasons": []
        },
        "scope": "RHS value on normal return of the selected expression; not observed DOM navigation",
        "selector": {
          "callee": "scopeHash",
          "file": "apps/client/src/home-dashboard-page.ts",
          "site": "call",
          "symbol": "homeDecisionHash"
        },
        "site_location": {
          "column": 9,
          "column_base": 1,
          "column_unit": "utf8_bytes",
          "coordinate_space": "captured_text_utf8",
          "end_byte": 8841,
          "end_column": 99,
          "end_line": 226,
          "file": "apps/client/src/home-dashboard-page.ts",
          "grammar": "typescript",
          "line": 226,
          "original_file_end_byte": 8841,
          "original_file_start_byte": 8751,
          "parse_identity": {
            "coordinate_space": "captured_text_utf8",
            "derived_text_utf8_sha256": null,
            "literal_authority": "original_saved_source_text_only",
            "original_text_utf8_sha256": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
            "position_map": "identity_utf8_bytes_and_line_columns",
            "projection_mode": "original",
            "projection_version": "ts-syntax-projection-1",
            "raw_prefix_bytes": 0,
            "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
            "semantic_source_version": "semantic-snapshot-sources-1",
            "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
          },
          "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
          "raw_prefix_bytes": 0,
          "semantic_parse_id": "709b4728fef637f15f8e0f4d0d42bd14002b4c594b473f770a337a40db908062",
          "source_excerpt": "scopeHash(`#/home/review?delivery=${encodeURIComponent(card.deliveryId)}`, scopeSelection)",
          "source_excerpt_truncated": false,
          "source_hash": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
          "source_line": "      : scopeHash(`#/home/review?delivery=${encodeURIComponent(card.deliveryId)}`, scopeSelection)",
          "span_hash": "37a6bb71e84d60b80259cbb25cd94d9beb10b1074cd93640d12f965106f0bc82",
          "start_byte": 8751
        },
        "source_complete": true,
        "source_trace": [
          {
            "ast_owner_id": "ts:apps/client/src/home-dashboard-page#homeDecisionHash",
            "environment_audit": {
              "host_aliases": {
                "count": 0,
                "model": "finite-captured-may-host-alias-1",
                "propagation_complete_within_model": true,
                "round_budget": 64,
                "runtime_receiver_verified": false,
                "same_runtime_object_verified": false,
                "samples": [],
                "supported_storage": "unique simple lexical destination; transparent/??/||/conditional possible origins",
                "truncated": false,
                "unsupported_container_storage_is_barrier": true
              },
              "lexical_absence": {
                "gaps": [],
                "limitations": [
                  "no captured local binding is not proof of a standard runtime value",
                  "global/member/alias effects and external mutation need separate effect guards"
                ],
                "local_declaration_absent": true,
                "location": {
                  "column": 45,
                  "column_base": 1,
                  "column_unit": "utf8_bytes",
                  "coordinate_space": "captured_text_utf8",
                  "end_byte": 8805,
                  "end_column": 63,
                  "end_line": 226,
                  "file": "apps/client/src/home-dashboard-page.ts",
                  "grammar": "typescript",
                  "line": 226,
                  "original_file_end_byte": 8805,
                  "original_file_start_byte": 8787,
                  "parse_identity": {
                    "coordinate_space": "captured_text_utf8",
                    "derived_text_utf8_sha256": null,
                    "literal_authority": "original_saved_source_text_only",
                    "original_text_utf8_sha256": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
                    "position_map": "identity_utf8_bytes_and_line_columns",
                    "projection_mode": "original",
                    "projection_version": "ts-syntax-projection-1",
                    "raw_prefix_bytes": 0,
                    "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                    "semantic_source_version": "semantic-snapshot-sources-1",
                    "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
                  },
                  "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "raw_prefix_bytes": 0,
                  "semantic_parse_id": "709b4728fef637f15f8e0f4d0d42bd14002b4c594b473f770a337a40db908062",
                  "source_excerpt": "encodeURIComponent",
                  "source_excerpt_truncated": false,
                  "source_hash": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
                  "source_line": "      : scopeHash(`#/home/review?delivery=${encodeURIComponent(card.deliveryId)}`, scopeSelection)",
                  "span_hash": "16269fce93c5c595be466d29e410f128e3dfd3c02730eebc729d708a457cf62b",
                  "start_byte": 8787
                },
                "name": "encodeURIComponent",
                "runtime_builtin_verified": false,
                "state": "unbound",
                "unbound": true,
                "version": "captured-lexical-bindings-3"
              },
              "lexical_model_version": "captured-lexical-bindings-3",
              "locations": [],
              "member": null,
              "model": {
                "allowed_prototype_member_interfaces": [],
                "allowed_static_member_interfaces": [],
                "assumptions": [
                  "the explicitly registered host interfaces retain their standard behavior",
                  "opaque calls, host transport and other captured documents do not replace the modeled standard interfaces",
                  "captured alias/prototype/write barriers may not be overridden by this premise"
                ],
                "member_argument_effects_verified": false,
                "member_call_purity_verified": false,
                "member_registration_semantics": "fixed syntax interface occurrence only; argument and receiver effects require separate consumer guards",
                "profile_id": "encode-uri-component-standard-function-1",
                "provider_or_external_mutation_verified": false,
                "registry_version": "standard-host-syntax-environment-v1",
                "runtime_builtin_verified": false,
                "standard_host_environment": "assumption"
              },
              "name": "encodeURIComponent",
              "opaque_effects": {
                "count": 0,
                "effects_verified": false,
                "fixed_standard_host_premise_required": true,
                "outside_document_effects_verified": false,
                "samples": [],
                "truncated": false
              },
              "policy": {
                "consumer_registration_required": true,
                "invocation": "explicit_fixed_interface_audit",
                "role_configuration_consulted": false,
                "semantic_contract_registration_verified": false
              },
              "scope_identity": {
                "file": "apps/client/src/home-dashboard-page.ts",
                "id": "776faf1fd38aedf357cb54c59adaa2a5bd379e2af011496781a90ec7d5b069dc",
                "scope_span": {
                  "end_byte": 8845,
                  "node_type": "statement_block",
                  "start_byte": 8692
                },
                "source_hash": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f"
              },
              "source": {
                "at_location": {
                  "column": 45,
                  "column_base": 1,
                  "column_unit": "utf8_bytes",
                  "coordinate_space": "captured_text_utf8",
                  "end_byte": 8805,
                  "end_column": 63,
                  "end_line": 226,
                  "file": "apps/client/src/home-dashboard-page.ts",
                  "grammar": "typescript",
                  "line": 226,
                  "original_file_end_byte": 8805,
                  "original_file_start_byte": 8787,
                  "parse_identity": {
                    "coordinate_space": "captured_text_utf8",
                    "derived_text_utf8_sha256": null,
                    "literal_authority": "original_saved_source_text_only",
                    "original_text_utf8_sha256": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
                    "position_map": "identity_utf8_bytes_and_line_columns",
                    "projection_mode": "original",
                    "projection_version": "ts-syntax-projection-1",
                    "raw_prefix_bytes": 0,
                    "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                    "semantic_source_version": "semantic-snapshot-sources-1",
                    "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
                  },
                  "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "raw_prefix_bytes": 0,
                  "semantic_parse_id": "709b4728fef637f15f8e0f4d0d42bd14002b4c594b473f770a337a40db908062",
                  "source_excerpt": "encodeURIComponent",
                  "source_excerpt_truncated": false,
                  "source_hash": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
                  "source_line": "      : scopeHash(`#/home/review?delivery=${encodeURIComponent(card.deliveryId)}`, scopeSelection)",
                  "span_hash": "16269fce93c5c595be466d29e410f128e3dfd3c02730eebc729d708a457cf62b",
                  "start_byte": 8787
                },
                "audit_scope": "authenticated_document",
                "budget_exceeded": false,
                "decision_computed_before_sampling": true,
                "file": "apps/client/src/home-dashboard-page.ts",
                "node_budget": 100000,
                "nodes_reviewed": 4661,
                "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "scan_complete": true,
                "semantic_parse_id": "709b4728fef637f15f8e0f4d0d42bd14002b4c594b473f770a337a40db908062",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28",
                "source_hash": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f"
              },
              "state": "supported_in_registered_model",
              "supported": true,
              "unresolved": {
                "barrier_count": 0,
                "reason_codes": [],
                "samples": [],
                "truncated": false
              },
              "version": "captured-builtin-environment-1"
            },
            "id": "a99218f8e65c851e5d31aeb5",
            "lexical_absence": {
              "gaps": [],
              "limitations": [
                "no captured local binding is not proof of a standard runtime value",
                "global/member/alias effects and external mutation need separate effect guards"
              ],
              "local_declaration_absent": true,
              "location": {
                "column": 45,
                "column_base": 1,
                "column_unit": "utf8_bytes",
                "coordinate_space": "captured_text_utf8",
                "end_byte": 8805,
                "end_column": 63,
                "end_line": 226,
                "file": "apps/client/src/home-dashboard-page.ts",
                "grammar": "typescript",
                "line": 226,
                "original_file_end_byte": 8805,
                "original_file_start_byte": 8787,
                "parse_identity": {
                  "coordinate_space": "captured_text_utf8",
                  "derived_text_utf8_sha256": null,
                  "literal_authority": "original_saved_source_text_only",
                  "original_text_utf8_sha256": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
                  "position_map": "identity_utf8_bytes_and_line_columns",
                  "projection_mode": "original",
                  "projection_version": "ts-syntax-projection-1",
                  "raw_prefix_bytes": 0,
                  "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "semantic_source_version": "semantic-snapshot-sources-1",
                  "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
                },
                "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "raw_prefix_bytes": 0,
                "semantic_parse_id": "709b4728fef637f15f8e0f4d0d42bd14002b4c594b473f770a337a40db908062",
                "source_excerpt": "encodeURIComponent",
                "source_excerpt_truncated": false,
                "source_hash": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
                "source_line": "      : scopeHash(`#/home/review?delivery=${encodeURIComponent(card.deliveryId)}`, scopeSelection)",
                "span_hash": "16269fce93c5c595be466d29e410f128e3dfd3c02730eebc729d708a457cf62b",
                "start_byte": 8787
              },
              "name": "encodeURIComponent",
              "runtime_builtin_verified": false,
              "state": "unbound",
              "unbound": true,
              "version": "captured-lexical-bindings-3"
            },
            "lexical_model_version": "captured-lexical-bindings-3",
            "location": {
              "column": 45,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 8805,
              "end_column": 63,
              "end_line": 226,
              "file": "apps/client/src/home-dashboard-page.ts",
              "grammar": "typescript",
              "line": 226,
              "original_file_end_byte": 8805,
              "original_file_start_byte": 8787,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "709b4728fef637f15f8e0f4d0d42bd14002b4c594b473f770a337a40db908062",
              "source_excerpt": "encodeURIComponent",
              "source_excerpt_truncated": false,
              "source_hash": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
              "source_line": "      : scopeHash(`#/home/review?delivery=${encodeURIComponent(card.deliveryId)}`, scopeSelection)",
              "span_hash": "16269fce93c5c595be466d29e410f128e3dfd3c02730eebc729d708a457cf62b",
              "start_byte": 8787
            },
            "member": null,
            "name": "encodeURIComponent",
            "opaque_host_effects_proven": false,
            "operation": "captured_standard_api_environment",
            "owner": "homeDecisionHash",
            "runtime_builtin_verified": false,
            "semantic_environment_version": "captured-builtin-environment-1",
            "standard_implementation_assumed": true,
            "visible_api_audit_scope": "authenticated_document"
          },
          {
            "ast_owner_id": "ts:apps/client/src/home-dashboard-page#homeDecisionHash",
            "delimiter_injection_excluded_under_model": true,
            "id": "720905801518e34e6e5d9d3a",
            "location": {
              "column": 45,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 8822,
              "end_column": 80,
              "end_line": 226,
              "file": "apps/client/src/home-dashboard-page.ts",
              "grammar": "typescript",
              "line": 226,
              "original_file_end_byte": 8822,
              "original_file_start_byte": 8787,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "709b4728fef637f15f8e0f4d0d42bd14002b4c594b473f770a337a40db908062",
              "source_excerpt": "encodeURIComponent(card.deliveryId)",
              "source_excerpt_truncated": false,
              "source_hash": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
              "source_line": "      : scopeHash(`#/home/review?delivery=${encodeURIComponent(card.deliveryId)}`, scopeSelection)",
              "span_hash": "ef0d9b7a8d9a75c2e8cc04e79bc6f3e7487c4de525c14d5da88ed35fa5bb767d",
              "start_byte": 8787
            },
            "model": "js-string-url-slicing-v1",
            "operation": "encoded_template_component",
            "owner": "homeDecisionHash"
          },
          {
            "ast_owner_id": "ts:apps/client/src/home-dashboard-page#homeDecisionHash",
            "id": "71fc291bf7bc4eec1fece19a",
            "location": {
              "column": 19,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 8824,
              "end_column": 82,
              "end_line": 226,
              "file": "apps/client/src/home-dashboard-page.ts",
              "grammar": "typescript",
              "line": 226,
              "original_file_end_byte": 8824,
              "original_file_start_byte": 8761,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "709b4728fef637f15f8e0f4d0d42bd14002b4c594b473f770a337a40db908062",
              "source_excerpt": "`#/home/review?delivery=${encodeURIComponent(card.deliveryId)}`",
              "source_excerpt_truncated": false,
              "source_hash": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
              "source_line": "      : scopeHash(`#/home/review?delivery=${encodeURIComponent(card.deliveryId)}`, scopeSelection)",
              "span_hash": "54323c5bd818b092c4ccabb3a91bc2ac625378642a2601587848393f31d1f2c0",
              "start_byte": 8761
            },
            "operation": "template_construction",
            "owner": "homeDecisionHash",
            "segments": [
              {
                "kind": "literal",
                "text": "#/home/review?delivery="
              },
              {
                "kind": "encoded",
                "source_value_id": "abstract-3"
              }
            ]
          },
          {
            "argument_index": 0,
            "argument_location": {
              "column": 19,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 8824,
              "end_column": 82,
              "end_line": 226,
              "file": "apps/client/src/home-dashboard-page.ts",
              "grammar": "typescript",
              "line": 226,
              "original_file_end_byte": 8824,
              "original_file_start_byte": 8761,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "709b4728fef637f15f8e0f4d0d42bd14002b4c594b473f770a337a40db908062",
              "source_excerpt": "`#/home/review?delivery=${encodeURIComponent(card.deliveryId)}`",
              "source_excerpt_truncated": false,
              "source_hash": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
              "source_line": "      : scopeHash(`#/home/review?delivery=${encodeURIComponent(card.deliveryId)}`, scopeSelection)",
              "span_hash": "54323c5bd818b092c4ccabb3a91bc2ac625378642a2601587848393f31d1f2c0",
              "start_byte": 8761
            },
            "ast_owner_id": "ts:apps/client/src/home-dashboard-page#homeDecisionHash",
            "edge_id": "1844b932fd9c78f229cffad4",
            "formal_parameter_location": {
              "column": 3,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6322,
              "end_column": 15,
              "end_line": 198,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 198,
              "original_file_end_byte": 6322,
              "original_file_start_byte": 6310,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "hash: string",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  hash: string,",
              "span_hash": "3d3bc4e4622f3e8cae75cd11dbbc51fe6e135a15891b022a56bb8455db2b6a15",
              "start_byte": 6310
            },
            "id": "e3f8d8560d81b3110a32de7d",
            "location": {
              "column": 9,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 8841,
              "end_column": 99,
              "end_line": 226,
              "file": "apps/client/src/home-dashboard-page.ts",
              "grammar": "typescript",
              "line": 226,
              "original_file_end_byte": 8841,
              "original_file_start_byte": 8751,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "709b4728fef637f15f8e0f4d0d42bd14002b4c594b473f770a337a40db908062",
              "source_excerpt": "scopeHash(`#/home/review?delivery=${encodeURIComponent(card.deliveryId)}`, scopeSelection)",
              "source_excerpt_truncated": false,
              "source_hash": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
              "source_line": "      : scopeHash(`#/home/review?delivery=${encodeURIComponent(card.deliveryId)}`, scopeSelection)",
              "span_hash": "37a6bb71e84d60b80259cbb25cd94d9beb10b1074cd93640d12f965106f0bc82",
              "start_byte": 8751
            },
            "operation": "argument_binds_parameter",
            "owner": "homeDecisionHash",
            "parameter_name": "hash",
            "target_declaration": {
              "column": 8,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6859,
              "end_column": 2,
              "end_line": 211,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 197,
              "original_file_end_byte": 6859,
              "original_file_start_byte": 6288,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "function scopeHash(\n  hash: string,\n  selection: ScopeRouteSelection | CompleteRepositorySelection,\n): string {\n  const queryIndex = hash.indexOf('?')\n  const path = queryIndex < 0 ? hash : hash.slice(0, queryIndex)\n  const parameters = new URLSearchParams(queryIndex < 0 ? '' : hash.slice(queryIndex + 1))\n  for (const name of SCOPE_PARAMETER_NAMES) {\n    const value = selection[name]\n    if (value === null) parameters.delete(name)\n    else parameters.set(name, value)\n  }\n  const query = parameters.toString()\n  return query.length === 0 ? path : `${path}?${query}`\n}",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "export function scopeHash(",
              "span_hash": "af14adff0c0198833642e881fa069b1facd3b5a4f91eb04afdd5ef428fb4e38f",
              "start_byte": 6288
            },
            "target_node_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "value": {
              "exact_text": null,
              "kind": "string",
              "runtime_execution_proven": false,
              "segments": [
                {
                  "kind": "literal",
                  "text": "#/home/review?delivery="
                },
                {
                  "kind": "encoded",
                  "source_value_id": "abstract-3"
                }
              ],
              "source_value_id": "abstract-4"
            }
          },
          {
            "argument_index": 1,
            "argument_location": {
              "column": 84,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 8840,
              "end_column": 98,
              "end_line": 226,
              "file": "apps/client/src/home-dashboard-page.ts",
              "grammar": "typescript",
              "line": 226,
              "original_file_end_byte": 8840,
              "original_file_start_byte": 8826,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "709b4728fef637f15f8e0f4d0d42bd14002b4c594b473f770a337a40db908062",
              "source_excerpt": "scopeSelection",
              "source_excerpt_truncated": false,
              "source_hash": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
              "source_line": "      : scopeHash(`#/home/review?delivery=${encodeURIComponent(card.deliveryId)}`, scopeSelection)",
              "span_hash": "0e20a611ef71faf02702036c8a62901f9c19132ee82415da496e9cce37e2fd88",
              "start_byte": 8826
            },
            "ast_owner_id": "ts:apps/client/src/home-dashboard-page#homeDecisionHash",
            "edge_id": "1844b932fd9c78f229cffad4",
            "formal_parameter_location": {
              "column": 3,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6386,
              "end_column": 63,
              "end_line": 199,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 199,
              "original_file_end_byte": 6386,
              "original_file_start_byte": 6326,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "selection: ScopeRouteSelection | CompleteRepositorySelection",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  selection: ScopeRouteSelection | CompleteRepositorySelection,",
              "span_hash": "b0b36e61b95584bd54fbcb6f1f99297d9ffd645c3e57da7d0538b7f77f419040",
              "start_byte": 6326
            },
            "id": "7450140e19e874920b15a250",
            "location": {
              "column": 9,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 8841,
              "end_column": 99,
              "end_line": 226,
              "file": "apps/client/src/home-dashboard-page.ts",
              "grammar": "typescript",
              "line": 226,
              "original_file_end_byte": 8841,
              "original_file_start_byte": 8751,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "709b4728fef637f15f8e0f4d0d42bd14002b4c594b473f770a337a40db908062",
              "source_excerpt": "scopeHash(`#/home/review?delivery=${encodeURIComponent(card.deliveryId)}`, scopeSelection)",
              "source_excerpt_truncated": false,
              "source_hash": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
              "source_line": "      : scopeHash(`#/home/review?delivery=${encodeURIComponent(card.deliveryId)}`, scopeSelection)",
              "span_hash": "37a6bb71e84d60b80259cbb25cd94d9beb10b1074cd93640d12f965106f0bc82",
              "start_byte": 8751
            },
            "operation": "argument_binds_parameter",
            "owner": "homeDecisionHash",
            "parameter_name": "selection",
            "target_declaration": {
              "column": 8,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6859,
              "end_column": 2,
              "end_line": 211,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 197,
              "original_file_end_byte": 6859,
              "original_file_start_byte": 6288,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "function scopeHash(\n  hash: string,\n  selection: ScopeRouteSelection | CompleteRepositorySelection,\n): string {\n  const queryIndex = hash.indexOf('?')\n  const path = queryIndex < 0 ? hash : hash.slice(0, queryIndex)\n  const parameters = new URLSearchParams(queryIndex < 0 ? '' : hash.slice(queryIndex + 1))\n  for (const name of SCOPE_PARAMETER_NAMES) {\n    const value = selection[name]\n    if (value === null) parameters.delete(name)\n    else parameters.set(name, value)\n  }\n  const query = parameters.toString()\n  return query.length === 0 ? path : `${path}?${query}`\n}",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "export function scopeHash(",
              "span_hash": "af14adff0c0198833642e881fa069b1facd3b5a4f91eb04afdd5ef428fb4e38f",
              "start_byte": 6288
            },
            "target_node_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "value": {
              "kind": "unknown",
              "runtime_execution_proven": false,
              "source_value_id": "abstract-5"
            }
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "id": "f633b5a8b47dda16ad81564c",
            "location": {
              "column": 35,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6437,
              "end_column": 38,
              "end_line": 201,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 201,
              "original_file_end_byte": 6437,
              "original_file_start_byte": 6434,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "'?'",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  const queryIndex = hash.indexOf('?')",
              "span_hash": "5de5d569b500c4fe44490d51f458d2821b96fdfea4b73ef817272ae41fd8e473",
              "start_byte": 6434
            },
            "operation": "literal_seed",
            "owner": "scopeHash",
            "text": "?",
            "value": {
              "exact_text": "?",
              "kind": "string",
              "runtime_execution_proven": false,
              "segments": [
                {
                  "kind": "literal",
                  "text": "?"
                }
              ],
              "source_value_id": "abstract-6"
            }
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "environment_audit": {
              "host_aliases": {
                "count": 0,
                "model": "finite-captured-may-host-alias-1",
                "propagation_complete_within_model": true,
                "round_budget": 64,
                "runtime_receiver_verified": false,
                "same_runtime_object_verified": false,
                "samples": [],
                "supported_storage": "unique simple lexical destination; transparent/??/||/conditional possible origins",
                "truncated": false,
                "unsupported_container_storage_is_barrier": true
              },
              "lexical_absence": {
                "gaps": [],
                "limitations": [
                  "no captured local binding is not proof of a standard runtime value",
                  "global/member/alias effects and external mutation need separate effect guards"
                ],
                "local_declaration_absent": true,
                "location": {
                  "column": 22,
                  "column_base": 1,
                  "column_unit": "utf8_bytes",
                  "coordinate_space": "captured_text_utf8",
                  "end_byte": 6433,
                  "end_column": 34,
                  "end_line": 201,
                  "file": "packages/browser-core/src/scope-context.ts",
                  "grammar": "typescript",
                  "line": 201,
                  "original_file_end_byte": 6433,
                  "original_file_start_byte": 6421,
                  "parse_identity": {
                    "coordinate_space": "captured_text_utf8",
                    "derived_text_utf8_sha256": null,
                    "literal_authority": "original_saved_source_text_only",
                    "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                    "position_map": "identity_utf8_bytes_and_line_columns",
                    "projection_mode": "original",
                    "projection_version": "ts-syntax-projection-1",
                    "raw_prefix_bytes": 0,
                    "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                    "semantic_source_version": "semantic-snapshot-sources-1",
                    "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
                  },
                  "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "raw_prefix_bytes": 0,
                  "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
                  "source_excerpt": "hash.indexOf",
                  "source_excerpt_truncated": false,
                  "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                  "source_line": "  const queryIndex = hash.indexOf('?')",
                  "span_hash": "d77fdbcdbe4c9c77394d0c4d0be0b5f6109cde49e773dc21486a5c507d89f4be",
                  "start_byte": 6421
                },
                "name": "String",
                "runtime_builtin_verified": false,
                "state": "unbound",
                "unbound": true,
                "version": "captured-lexical-bindings-3"
              },
              "lexical_model_version": "captured-lexical-bindings-3",
              "locations": [],
              "member": "indexOf",
              "model": {
                "allowed_prototype_member_interfaces": [
                  "indexOf",
                  "slice"
                ],
                "allowed_static_member_interfaces": [
                  "fromCharCode",
                  "fromCodePoint",
                  "raw"
                ],
                "assumptions": [
                  "the explicitly registered host interfaces retain their standard behavior",
                  "opaque calls, host transport and other captured documents do not replace the modeled standard interfaces",
                  "captured alias/prototype/write barriers may not be overridden by this premise"
                ],
                "member_argument_effects_verified": false,
                "member_call_purity_verified": false,
                "member_registration_semantics": "fixed syntax interface occurrence only; argument and receiver effects require separate consumer guards",
                "profile_id": "string-standard-interface-1",
                "provider_or_external_mutation_verified": false,
                "registry_version": "standard-host-syntax-environment-v1",
                "runtime_builtin_verified": false,
                "standard_host_environment": "assumption"
              },
              "name": "String",
              "opaque_effects": {
                "count": 0,
                "effects_verified": false,
                "fixed_standard_host_premise_required": true,
                "outside_document_effects_verified": false,
                "samples": [],
                "truncated": false
              },
              "policy": {
                "consumer_registration_required": true,
                "invocation": "explicit_fixed_interface_audit",
                "role_configuration_consulted": false,
                "semantic_contract_registration_verified": false
              },
              "scope_identity": {
                "file": "packages/browser-core/src/scope-context.ts",
                "id": "1295eeb007d425a18356ea8961c05fea811c0d5399d9140668a5063e03967f2b",
                "scope_span": {
                  "end_byte": 6859,
                  "node_type": "statement_block",
                  "start_byte": 6398
                },
                "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d"
              },
              "source": {
                "at_location": {
                  "column": 22,
                  "column_base": 1,
                  "column_unit": "utf8_bytes",
                  "coordinate_space": "captured_text_utf8",
                  "end_byte": 6433,
                  "end_column": 34,
                  "end_line": 201,
                  "file": "packages/browser-core/src/scope-context.ts",
                  "grammar": "typescript",
                  "line": 201,
                  "original_file_end_byte": 6433,
                  "original_file_start_byte": 6421,
                  "parse_identity": {
                    "coordinate_space": "captured_text_utf8",
                    "derived_text_utf8_sha256": null,
                    "literal_authority": "original_saved_source_text_only",
                    "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                    "position_map": "identity_utf8_bytes_and_line_columns",
                    "projection_mode": "original",
                    "projection_version": "ts-syntax-projection-1",
                    "raw_prefix_bytes": 0,
                    "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                    "semantic_source_version": "semantic-snapshot-sources-1",
                    "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
                  },
                  "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "raw_prefix_bytes": 0,
                  "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
                  "source_excerpt": "hash.indexOf",
                  "source_excerpt_truncated": false,
                  "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                  "source_line": "  const queryIndex = hash.indexOf('?')",
                  "span_hash": "d77fdbcdbe4c9c77394d0c4d0be0b5f6109cde49e773dc21486a5c507d89f4be",
                  "start_byte": 6421
                },
                "audit_scope": "authenticated_document",
                "budget_exceeded": false,
                "decision_computed_before_sampling": true,
                "file": "packages/browser-core/src/scope-context.ts",
                "node_budget": 100000,
                "nodes_reviewed": 1484,
                "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "scan_complete": true,
                "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28",
                "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d"
              },
              "state": "supported_in_registered_model",
              "supported": true,
              "unresolved": {
                "barrier_count": 0,
                "reason_codes": [],
                "samples": [],
                "truncated": false
              },
              "version": "captured-builtin-environment-1"
            },
            "id": "4a0092c8bc9220f9d843c319",
            "lexical_absence": {
              "gaps": [],
              "limitations": [
                "no captured local binding is not proof of a standard runtime value",
                "global/member/alias effects and external mutation need separate effect guards"
              ],
              "local_declaration_absent": true,
              "location": {
                "column": 22,
                "column_base": 1,
                "column_unit": "utf8_bytes",
                "coordinate_space": "captured_text_utf8",
                "end_byte": 6433,
                "end_column": 34,
                "end_line": 201,
                "file": "packages/browser-core/src/scope-context.ts",
                "grammar": "typescript",
                "line": 201,
                "original_file_end_byte": 6433,
                "original_file_start_byte": 6421,
                "parse_identity": {
                  "coordinate_space": "captured_text_utf8",
                  "derived_text_utf8_sha256": null,
                  "literal_authority": "original_saved_source_text_only",
                  "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                  "position_map": "identity_utf8_bytes_and_line_columns",
                  "projection_mode": "original",
                  "projection_version": "ts-syntax-projection-1",
                  "raw_prefix_bytes": 0,
                  "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "semantic_source_version": "semantic-snapshot-sources-1",
                  "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
                },
                "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "raw_prefix_bytes": 0,
                "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
                "source_excerpt": "hash.indexOf",
                "source_excerpt_truncated": false,
                "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "source_line": "  const queryIndex = hash.indexOf('?')",
                "span_hash": "d77fdbcdbe4c9c77394d0c4d0be0b5f6109cde49e773dc21486a5c507d89f4be",
                "start_byte": 6421
              },
              "name": "String",
              "runtime_builtin_verified": false,
              "state": "unbound",
              "unbound": true,
              "version": "captured-lexical-bindings-3"
            },
            "lexical_model_version": "captured-lexical-bindings-3",
            "location": {
              "column": 22,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6433,
              "end_column": 34,
              "end_line": 201,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 201,
              "original_file_end_byte": 6433,
              "original_file_start_byte": 6421,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "hash.indexOf",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  const queryIndex = hash.indexOf('?')",
              "span_hash": "d77fdbcdbe4c9c77394d0c4d0be0b5f6109cde49e773dc21486a5c507d89f4be",
              "start_byte": 6421
            },
            "member": "indexOf",
            "name": "String",
            "opaque_host_effects_proven": false,
            "operation": "captured_standard_api_environment",
            "owner": "scopeHash",
            "runtime_builtin_verified": false,
            "semantic_environment_version": "captured-builtin-environment-1",
            "standard_implementation_assumed": true,
            "visible_api_audit_scope": "authenticated_document"
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "id": "891af9cac75b34e909a63fd2",
            "location": {
              "column": 22,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6438,
              "end_column": 39,
              "end_line": 201,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 201,
              "original_file_end_byte": 6438,
              "original_file_start_byte": 6421,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "hash.indexOf('?')",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  const queryIndex = hash.indexOf('?')",
              "span_hash": "3c57cafec2c7a832259486780a753497f62646311dcf0bc87685ce9108b91b5e",
              "start_byte": 6421
            },
            "model": "js-string-url-slicing-v1",
            "operation": "query_separator_index",
            "owner": "scopeHash",
            "receiver_id": "abstract-4"
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "id": "ec36a1285c3fe2127e73272c",
            "location": {
              "column": 9,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6438,
              "end_column": 39,
              "end_line": 201,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 201,
              "original_file_end_byte": 6438,
              "original_file_start_byte": 6408,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "queryIndex = hash.indexOf('?')",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  const queryIndex = hash.indexOf('?')",
              "span_hash": "9abf2e9fc718d35381d532bc337e486359e282d4bf8cfb7e190470f60ca252e5",
              "start_byte": 6408
            },
            "name": "queryIndex",
            "operation": "local_value_binding",
            "owner": "scopeHash",
            "value": {
              "kind": "query_index",
              "runtime_execution_proven": false,
              "source_value_id": "abstract-7"
            }
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "environment_audit": {
              "host_aliases": {
                "count": 0,
                "model": "finite-captured-may-host-alias-1",
                "propagation_complete_within_model": true,
                "round_budget": 64,
                "runtime_receiver_verified": false,
                "same_runtime_object_verified": false,
                "samples": [],
                "supported_storage": "unique simple lexical destination; transparent/??/||/conditional possible origins",
                "truncated": false,
                "unsupported_container_storage_is_barrier": true
              },
              "lexical_absence": {
                "gaps": [],
                "limitations": [
                  "no captured local binding is not proof of a standard runtime value",
                  "global/member/alias effects and external mutation need separate effect guards"
                ],
                "local_declaration_absent": true,
                "location": {
                  "column": 40,
                  "column_base": 1,
                  "column_unit": "utf8_bytes",
                  "coordinate_space": "captured_text_utf8",
                  "end_byte": 6488,
                  "end_column": 50,
                  "end_line": 202,
                  "file": "packages/browser-core/src/scope-context.ts",
                  "grammar": "typescript",
                  "line": 202,
                  "original_file_end_byte": 6488,
                  "original_file_start_byte": 6478,
                  "parse_identity": {
                    "coordinate_space": "captured_text_utf8",
                    "derived_text_utf8_sha256": null,
                    "literal_authority": "original_saved_source_text_only",
                    "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                    "position_map": "identity_utf8_bytes_and_line_columns",
                    "projection_mode": "original",
                    "projection_version": "ts-syntax-projection-1",
                    "raw_prefix_bytes": 0,
                    "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                    "semantic_source_version": "semantic-snapshot-sources-1",
                    "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
                  },
                  "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "raw_prefix_bytes": 0,
                  "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
                  "source_excerpt": "hash.slice",
                  "source_excerpt_truncated": false,
                  "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                  "source_line": "  const path = queryIndex < 0 ? hash : hash.slice(0, queryIndex)",
                  "span_hash": "9298c87234bdbc644d398ef1a579bad86c1115a29a9a134d5fcce05a88d06f1f",
                  "start_byte": 6478
                },
                "name": "String",
                "runtime_builtin_verified": false,
                "state": "unbound",
                "unbound": true,
                "version": "captured-lexical-bindings-3"
              },
              "lexical_model_version": "captured-lexical-bindings-3",
              "locations": [],
              "member": "slice",
              "model": {
                "allowed_prototype_member_interfaces": [
                  "indexOf",
                  "slice"
                ],
                "allowed_static_member_interfaces": [
                  "fromCharCode",
                  "fromCodePoint",
                  "raw"
                ],
                "assumptions": [
                  "the explicitly registered host interfaces retain their standard behavior",
                  "opaque calls, host transport and other captured documents do not replace the modeled standard interfaces",
                  "captured alias/prototype/write barriers may not be overridden by this premise"
                ],
                "member_argument_effects_verified": false,
                "member_call_purity_verified": false,
                "member_registration_semantics": "fixed syntax interface occurrence only; argument and receiver effects require separate consumer guards",
                "profile_id": "string-standard-interface-1",
                "provider_or_external_mutation_verified": false,
                "registry_version": "standard-host-syntax-environment-v1",
                "runtime_builtin_verified": false,
                "standard_host_environment": "assumption"
              },
              "name": "String",
              "opaque_effects": {
                "count": 0,
                "effects_verified": false,
                "fixed_standard_host_premise_required": true,
                "outside_document_effects_verified": false,
                "samples": [],
                "truncated": false
              },
              "policy": {
                "consumer_registration_required": true,
                "invocation": "explicit_fixed_interface_audit",
                "role_configuration_consulted": false,
                "semantic_contract_registration_verified": false
              },
              "scope_identity": {
                "file": "packages/browser-core/src/scope-context.ts",
                "id": "1295eeb007d425a18356ea8961c05fea811c0d5399d9140668a5063e03967f2b",
                "scope_span": {
                  "end_byte": 6859,
                  "node_type": "statement_block",
                  "start_byte": 6398
                },
                "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d"
              },
              "source": {
                "at_location": {
                  "column": 40,
                  "column_base": 1,
                  "column_unit": "utf8_bytes",
                  "coordinate_space": "captured_text_utf8",
                  "end_byte": 6488,
                  "end_column": 50,
                  "end_line": 202,
                  "file": "packages/browser-core/src/scope-context.ts",
                  "grammar": "typescript",
                  "line": 202,
                  "original_file_end_byte": 6488,
                  "original_file_start_byte": 6478,
                  "parse_identity": {
                    "coordinate_space": "captured_text_utf8",
                    "derived_text_utf8_sha256": null,
                    "literal_authority": "original_saved_source_text_only",
                    "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                    "position_map": "identity_utf8_bytes_and_line_columns",
                    "projection_mode": "original",
                    "projection_version": "ts-syntax-projection-1",
                    "raw_prefix_bytes": 0,
                    "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                    "semantic_source_version": "semantic-snapshot-sources-1",
                    "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
                  },
                  "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "raw_prefix_bytes": 0,
                  "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
                  "source_excerpt": "hash.slice",
                  "source_excerpt_truncated": false,
                  "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                  "source_line": "  const path = queryIndex < 0 ? hash : hash.slice(0, queryIndex)",
                  "span_hash": "9298c87234bdbc644d398ef1a579bad86c1115a29a9a134d5fcce05a88d06f1f",
                  "start_byte": 6478
                },
                "audit_scope": "authenticated_document",
                "budget_exceeded": false,
                "decision_computed_before_sampling": true,
                "file": "packages/browser-core/src/scope-context.ts",
                "node_budget": 100000,
                "nodes_reviewed": 1484,
                "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "scan_complete": true,
                "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28",
                "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d"
              },
              "state": "supported_in_registered_model",
              "supported": true,
              "unresolved": {
                "barrier_count": 0,
                "reason_codes": [],
                "samples": [],
                "truncated": false
              },
              "version": "captured-builtin-environment-1"
            },
            "id": "17c235c97f075cea7e1b525f",
            "lexical_absence": {
              "gaps": [],
              "limitations": [
                "no captured local binding is not proof of a standard runtime value",
                "global/member/alias effects and external mutation need separate effect guards"
              ],
              "local_declaration_absent": true,
              "location": {
                "column": 40,
                "column_base": 1,
                "column_unit": "utf8_bytes",
                "coordinate_space": "captured_text_utf8",
                "end_byte": 6488,
                "end_column": 50,
                "end_line": 202,
                "file": "packages/browser-core/src/scope-context.ts",
                "grammar": "typescript",
                "line": 202,
                "original_file_end_byte": 6488,
                "original_file_start_byte": 6478,
                "parse_identity": {
                  "coordinate_space": "captured_text_utf8",
                  "derived_text_utf8_sha256": null,
                  "literal_authority": "original_saved_source_text_only",
                  "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                  "position_map": "identity_utf8_bytes_and_line_columns",
                  "projection_mode": "original",
                  "projection_version": "ts-syntax-projection-1",
                  "raw_prefix_bytes": 0,
                  "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "semantic_source_version": "semantic-snapshot-sources-1",
                  "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
                },
                "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "raw_prefix_bytes": 0,
                "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
                "source_excerpt": "hash.slice",
                "source_excerpt_truncated": false,
                "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "source_line": "  const path = queryIndex < 0 ? hash : hash.slice(0, queryIndex)",
                "span_hash": "9298c87234bdbc644d398ef1a579bad86c1115a29a9a134d5fcce05a88d06f1f",
                "start_byte": 6478
              },
              "name": "String",
              "runtime_builtin_verified": false,
              "state": "unbound",
              "unbound": true,
              "version": "captured-lexical-bindings-3"
            },
            "lexical_model_version": "captured-lexical-bindings-3",
            "location": {
              "column": 40,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6488,
              "end_column": 50,
              "end_line": 202,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 202,
              "original_file_end_byte": 6488,
              "original_file_start_byte": 6478,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "hash.slice",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  const path = queryIndex < 0 ? hash : hash.slice(0, queryIndex)",
              "span_hash": "9298c87234bdbc644d398ef1a579bad86c1115a29a9a134d5fcce05a88d06f1f",
              "start_byte": 6478
            },
            "member": "slice",
            "name": "String",
            "opaque_host_effects_proven": false,
            "operation": "captured_standard_api_environment",
            "owner": "scopeHash",
            "runtime_builtin_verified": false,
            "semantic_environment_version": "captured-builtin-environment-1",
            "standard_implementation_assumed": true,
            "visible_api_audit_scope": "authenticated_document"
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "id": "68faf5270f2235698d924cc6",
            "location": {
              "column": 40,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6503,
              "end_column": 65,
              "end_line": 202,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 202,
              "original_file_end_byte": 6503,
              "original_file_start_byte": 6478,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "hash.slice(0, queryIndex)",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  const path = queryIndex < 0 ? hash : hash.slice(0, queryIndex)",
              "span_hash": "60371d8f58e333661ce89849ea28b6de96171f8111ac50c6939cd42382a66169",
              "start_byte": 6478
            },
            "model": "js-string-url-slicing-v1",
            "operation": "string_slice",
            "owner": "scopeHash",
            "receiver_id": "abstract-4",
            "result": {
              "exact_text": "#/home/review",
              "kind": "string",
              "runtime_execution_proven": false,
              "segments": [
                {
                  "kind": "literal",
                  "text": "#/home/review"
                }
              ],
              "source_value_id": "abstract-12"
            }
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "condition_location": {
              "column": 16,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6468,
              "end_column": 30,
              "end_line": 202,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 202,
              "original_file_end_byte": 6468,
              "original_file_start_byte": 6454,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "queryIndex < 0",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  const path = queryIndex < 0 ? hash : hash.slice(0, queryIndex)",
              "span_hash": "50bc8c2017e23a65300725a045339d9d7d5d743f93ba61a9306003856f9ee3ff",
              "start_byte": 6454
            },
            "condition_truth": false,
            "id": "f568d0e5c355fd49110bd3be",
            "input_value_ids": [
              "abstract-12"
            ],
            "location": {
              "column": 16,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6503,
              "end_column": 65,
              "end_line": 202,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 202,
              "original_file_end_byte": 6503,
              "original_file_start_byte": 6454,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "queryIndex < 0 ? hash : hash.slice(0, queryIndex)",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  const path = queryIndex < 0 ? hash : hash.slice(0, queryIndex)",
              "span_hash": "b6af743ef71d467fc1bbeca3d79ed7a5b1f2047779a19648af01e0d29f2843cf",
              "start_byte": 6454
            },
            "operation": "conditional_value_join",
            "owner": "scopeHash",
            "result": {
              "exact_text": "#/home/review",
              "kind": "string",
              "runtime_execution_proven": false,
              "segments": [
                {
                  "kind": "literal",
                  "text": "#/home/review"
                }
              ],
              "source_value_id": "abstract-12"
            }
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "id": "a519839c33a6a07b87a49e24",
            "location": {
              "column": 9,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6503,
              "end_column": 65,
              "end_line": 202,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 202,
              "original_file_end_byte": 6503,
              "original_file_start_byte": 6447,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "path = queryIndex < 0 ? hash : hash.slice(0, queryIndex)",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  const path = queryIndex < 0 ? hash : hash.slice(0, queryIndex)",
              "span_hash": "e444a8cd839bdd1d8340b5a99d38e53f4266889b80a415e1a16afb2880a1bc0d",
              "start_byte": 6447
            },
            "name": "path",
            "operation": "local_value_binding",
            "owner": "scopeHash",
            "value": {
              "exact_text": "#/home/review",
              "kind": "string",
              "runtime_execution_proven": false,
              "segments": [
                {
                  "kind": "literal",
                  "text": "#/home/review"
                }
              ],
              "source_value_id": "abstract-12"
            }
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "environment_audit": {
              "host_aliases": {
                "count": 0,
                "model": "finite-captured-may-host-alias-1",
                "propagation_complete_within_model": true,
                "round_budget": 64,
                "runtime_receiver_verified": false,
                "same_runtime_object_verified": false,
                "samples": [],
                "supported_storage": "unique simple lexical destination; transparent/??/||/conditional possible origins",
                "truncated": false,
                "unsupported_container_storage_is_barrier": true
              },
              "lexical_absence": {
                "gaps": [],
                "limitations": [
                  "no captured local binding is not proof of a standard runtime value",
                  "global/member/alias effects and external mutation need separate effect guards"
                ],
                "local_declaration_absent": true,
                "location": {
                  "column": 64,
                  "column_base": 1,
                  "column_unit": "utf8_bytes",
                  "coordinate_space": "captured_text_utf8",
                  "end_byte": 6577,
                  "end_column": 74,
                  "end_line": 203,
                  "file": "packages/browser-core/src/scope-context.ts",
                  "grammar": "typescript",
                  "line": 203,
                  "original_file_end_byte": 6577,
                  "original_file_start_byte": 6567,
                  "parse_identity": {
                    "coordinate_space": "captured_text_utf8",
                    "derived_text_utf8_sha256": null,
                    "literal_authority": "original_saved_source_text_only",
                    "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                    "position_map": "identity_utf8_bytes_and_line_columns",
                    "projection_mode": "original",
                    "projection_version": "ts-syntax-projection-1",
                    "raw_prefix_bytes": 0,
                    "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                    "semantic_source_version": "semantic-snapshot-sources-1",
                    "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
                  },
                  "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "raw_prefix_bytes": 0,
                  "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
                  "source_excerpt": "hash.slice",
                  "source_excerpt_truncated": false,
                  "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                  "source_line": "  const parameters = new URLSearchParams(queryIndex < 0 ? '' : hash.slice(queryIndex + 1))",
                  "span_hash": "9298c87234bdbc644d398ef1a579bad86c1115a29a9a134d5fcce05a88d06f1f",
                  "start_byte": 6567
                },
                "name": "String",
                "runtime_builtin_verified": false,
                "state": "unbound",
                "unbound": true,
                "version": "captured-lexical-bindings-3"
              },
              "lexical_model_version": "captured-lexical-bindings-3",
              "locations": [],
              "member": "slice",
              "model": {
                "allowed_prototype_member_interfaces": [
                  "indexOf",
                  "slice"
                ],
                "allowed_static_member_interfaces": [
                  "fromCharCode",
                  "fromCodePoint",
                  "raw"
                ],
                "assumptions": [
                  "the explicitly registered host interfaces retain their standard behavior",
                  "opaque calls, host transport and other captured documents do not replace the modeled standard interfaces",
                  "captured alias/prototype/write barriers may not be overridden by this premise"
                ],
                "member_argument_effects_verified": false,
                "member_call_purity_verified": false,
                "member_registration_semantics": "fixed syntax interface occurrence only; argument and receiver effects require separate consumer guards",
                "profile_id": "string-standard-interface-1",
                "provider_or_external_mutation_verified": false,
                "registry_version": "standard-host-syntax-environment-v1",
                "runtime_builtin_verified": false,
                "standard_host_environment": "assumption"
              },
              "name": "String",
              "opaque_effects": {
                "count": 0,
                "effects_verified": false,
                "fixed_standard_host_premise_required": true,
                "outside_document_effects_verified": false,
                "samples": [],
                "truncated": false
              },
              "policy": {
                "consumer_registration_required": true,
                "invocation": "explicit_fixed_interface_audit",
                "role_configuration_consulted": false,
                "semantic_contract_registration_verified": false
              },
              "scope_identity": {
                "file": "packages/browser-core/src/scope-context.ts",
                "id": "1295eeb007d425a18356ea8961c05fea811c0d5399d9140668a5063e03967f2b",
                "scope_span": {
                  "end_byte": 6859,
                  "node_type": "statement_block",
                  "start_byte": 6398
                },
                "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d"
              },
              "source": {
                "at_location": {
                  "column": 64,
                  "column_base": 1,
                  "column_unit": "utf8_bytes",
                  "coordinate_space": "captured_text_utf8",
                  "end_byte": 6577,
                  "end_column": 74,
                  "end_line": 203,
                  "file": "packages/browser-core/src/scope-context.ts",
                  "grammar": "typescript",
                  "line": 203,
                  "original_file_end_byte": 6577,
                  "original_file_start_byte": 6567,
                  "parse_identity": {
                    "coordinate_space": "captured_text_utf8",
                    "derived_text_utf8_sha256": null,
                    "literal_authority": "original_saved_source_text_only",
                    "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                    "position_map": "identity_utf8_bytes_and_line_columns",
                    "projection_mode": "original",
                    "projection_version": "ts-syntax-projection-1",
                    "raw_prefix_bytes": 0,
                    "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                    "semantic_source_version": "semantic-snapshot-sources-1",
                    "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
                  },
                  "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "raw_prefix_bytes": 0,
                  "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
                  "source_excerpt": "hash.slice",
                  "source_excerpt_truncated": false,
                  "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                  "source_line": "  const parameters = new URLSearchParams(queryIndex < 0 ? '' : hash.slice(queryIndex + 1))",
                  "span_hash": "9298c87234bdbc644d398ef1a579bad86c1115a29a9a134d5fcce05a88d06f1f",
                  "start_byte": 6567
                },
                "audit_scope": "authenticated_document",
                "budget_exceeded": false,
                "decision_computed_before_sampling": true,
                "file": "packages/browser-core/src/scope-context.ts",
                "node_budget": 100000,
                "nodes_reviewed": 1484,
                "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "scan_complete": true,
                "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28",
                "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d"
              },
              "state": "supported_in_registered_model",
              "supported": true,
              "unresolved": {
                "barrier_count": 0,
                "reason_codes": [],
                "samples": [],
                "truncated": false
              },
              "version": "captured-builtin-environment-1"
            },
            "id": "b5a6588fbf048e0ac86553e0",
            "lexical_absence": {
              "gaps": [],
              "limitations": [
                "no captured local binding is not proof of a standard runtime value",
                "global/member/alias effects and external mutation need separate effect guards"
              ],
              "local_declaration_absent": true,
              "location": {
                "column": 64,
                "column_base": 1,
                "column_unit": "utf8_bytes",
                "coordinate_space": "captured_text_utf8",
                "end_byte": 6577,
                "end_column": 74,
                "end_line": 203,
                "file": "packages/browser-core/src/scope-context.ts",
                "grammar": "typescript",
                "line": 203,
                "original_file_end_byte": 6577,
                "original_file_start_byte": 6567,
                "parse_identity": {
                  "coordinate_space": "captured_text_utf8",
                  "derived_text_utf8_sha256": null,
                  "literal_authority": "original_saved_source_text_only",
                  "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                  "position_map": "identity_utf8_bytes_and_line_columns",
                  "projection_mode": "original",
                  "projection_version": "ts-syntax-projection-1",
                  "raw_prefix_bytes": 0,
                  "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "semantic_source_version": "semantic-snapshot-sources-1",
                  "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
                },
                "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "raw_prefix_bytes": 0,
                "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
                "source_excerpt": "hash.slice",
                "source_excerpt_truncated": false,
                "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "source_line": "  const parameters = new URLSearchParams(queryIndex < 0 ? '' : hash.slice(queryIndex + 1))",
                "span_hash": "9298c87234bdbc644d398ef1a579bad86c1115a29a9a134d5fcce05a88d06f1f",
                "start_byte": 6567
              },
              "name": "String",
              "runtime_builtin_verified": false,
              "state": "unbound",
              "unbound": true,
              "version": "captured-lexical-bindings-3"
            },
            "lexical_model_version": "captured-lexical-bindings-3",
            "location": {
              "column": 64,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6577,
              "end_column": 74,
              "end_line": 203,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 203,
              "original_file_end_byte": 6577,
              "original_file_start_byte": 6567,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "hash.slice",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  const parameters = new URLSearchParams(queryIndex < 0 ? '' : hash.slice(queryIndex + 1))",
              "span_hash": "9298c87234bdbc644d398ef1a579bad86c1115a29a9a134d5fcce05a88d06f1f",
              "start_byte": 6567
            },
            "member": "slice",
            "name": "String",
            "opaque_host_effects_proven": false,
            "operation": "captured_standard_api_environment",
            "owner": "scopeHash",
            "runtime_builtin_verified": false,
            "semantic_environment_version": "captured-builtin-environment-1",
            "standard_implementation_assumed": true,
            "visible_api_audit_scope": "authenticated_document"
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "id": "e462bc13c56de11108151188",
            "location": {
              "column": 64,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6593,
              "end_column": 90,
              "end_line": 203,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 203,
              "original_file_end_byte": 6593,
              "original_file_start_byte": 6567,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "hash.slice(queryIndex + 1)",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  const parameters = new URLSearchParams(queryIndex < 0 ? '' : hash.slice(queryIndex + 1))",
              "span_hash": "c65459250590aaba603b577d510c2968c6b3938e523f4b33720fcae69d3cebb3",
              "start_byte": 6567
            },
            "model": "js-string-url-slicing-v1",
            "operation": "string_slice",
            "owner": "scopeHash",
            "receiver_id": "abstract-4",
            "result": {
              "exact_text": null,
              "kind": "string",
              "query_domain": {
                "guaranteed_keys": [
                  "delivery"
                ],
                "invariant": "guaranteed subset actual subset possible only when keyset_closed",
                "keyset_closed": true,
                "possible_keys": [
                  "delivery"
                ],
                "unknown_keys": false,
                "unknown_reasons": []
              },
              "runtime_execution_proven": false,
              "segments": [
                {
                  "kind": "literal",
                  "text": "delivery="
                },
                {
                  "kind": "encoded",
                  "source_value_id": "abstract-3"
                }
              ],
              "source_value_id": "abstract-21"
            }
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "condition_location": {
              "column": 42,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6559,
              "end_column": 56,
              "end_line": 203,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 203,
              "original_file_end_byte": 6559,
              "original_file_start_byte": 6545,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "queryIndex < 0",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  const parameters = new URLSearchParams(queryIndex < 0 ? '' : hash.slice(queryIndex + 1))",
              "span_hash": "50bc8c2017e23a65300725a045339d9d7d5d743f93ba61a9306003856f9ee3ff",
              "start_byte": 6545
            },
            "condition_truth": false,
            "id": "7a32d0d53cd314ec70addde1",
            "input_value_ids": [
              "abstract-21"
            ],
            "location": {
              "column": 42,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6593,
              "end_column": 90,
              "end_line": 203,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 203,
              "original_file_end_byte": 6593,
              "original_file_start_byte": 6545,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "queryIndex < 0 ? '' : hash.slice(queryIndex + 1)",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  const parameters = new URLSearchParams(queryIndex < 0 ? '' : hash.slice(queryIndex + 1))",
              "span_hash": "d5996a931a5cd759f8542906911c87a976856968f8b27150a4f171f7eb4fd8a8",
              "start_byte": 6545
            },
            "operation": "conditional_value_join",
            "owner": "scopeHash",
            "result": {
              "exact_text": null,
              "kind": "string",
              "query_domain": {
                "guaranteed_keys": [
                  "delivery"
                ],
                "invariant": "guaranteed subset actual subset possible only when keyset_closed",
                "keyset_closed": true,
                "possible_keys": [
                  "delivery"
                ],
                "unknown_keys": false,
                "unknown_reasons": []
              },
              "runtime_execution_proven": false,
              "segments": [
                {
                  "kind": "literal",
                  "text": "delivery="
                },
                {
                  "kind": "encoded",
                  "source_value_id": "abstract-3"
                }
              ],
              "source_value_id": "abstract-21"
            }
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "environment_audit": {
              "host_aliases": {
                "count": 0,
                "model": "finite-captured-may-host-alias-1",
                "propagation_complete_within_model": true,
                "round_budget": 64,
                "runtime_receiver_verified": false,
                "same_runtime_object_verified": false,
                "samples": [],
                "supported_storage": "unique simple lexical destination; transparent/??/||/conditional possible origins",
                "truncated": false,
                "unsupported_container_storage_is_barrier": true
              },
              "lexical_absence": {
                "gaps": [],
                "limitations": [
                  "no captured local binding is not proof of a standard runtime value",
                  "global/member/alias effects and external mutation need separate effect guards"
                ],
                "local_declaration_absent": true,
                "location": {
                  "column": 26,
                  "column_base": 1,
                  "column_unit": "utf8_bytes",
                  "coordinate_space": "captured_text_utf8",
                  "end_byte": 6544,
                  "end_column": 41,
                  "end_line": 203,
                  "file": "packages/browser-core/src/scope-context.ts",
                  "grammar": "typescript",
                  "line": 203,
                  "original_file_end_byte": 6544,
                  "original_file_start_byte": 6529,
                  "parse_identity": {
                    "coordinate_space": "captured_text_utf8",
                    "derived_text_utf8_sha256": null,
                    "literal_authority": "original_saved_source_text_only",
                    "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                    "position_map": "identity_utf8_bytes_and_line_columns",
                    "projection_mode": "original",
                    "projection_version": "ts-syntax-projection-1",
                    "raw_prefix_bytes": 0,
                    "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                    "semantic_source_version": "semantic-snapshot-sources-1",
                    "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
                  },
                  "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "raw_prefix_bytes": 0,
                  "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
                  "source_excerpt": "URLSearchParams",
                  "source_excerpt_truncated": false,
                  "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                  "source_line": "  const parameters = new URLSearchParams(queryIndex < 0 ? '' : hash.slice(queryIndex + 1))",
                  "span_hash": "85c6cac623ea5e381dc34b8b0be265d53fe4e77795b08297e198f73e1b47882f",
                  "start_byte": 6529
                },
                "name": "URLSearchParams",
                "runtime_builtin_verified": false,
                "state": "unbound",
                "unbound": true,
                "version": "captured-lexical-bindings-3"
              },
              "lexical_model_version": "captured-lexical-bindings-3",
              "locations": [],
              "member": null,
              "model": {
                "allowed_prototype_member_interfaces": [],
                "allowed_static_member_interfaces": [],
                "assumptions": [
                  "the explicitly registered host interfaces retain their standard behavior",
                  "opaque calls, host transport and other captured documents do not replace the modeled standard interfaces",
                  "captured alias/prototype/write barriers may not be overridden by this premise"
                ],
                "member_argument_effects_verified": false,
                "member_call_purity_verified": false,
                "member_registration_semantics": "fixed syntax interface occurrence only; argument and receiver effects require separate consumer guards",
                "profile_id": "url-search-params-standard-constructor-1",
                "provider_or_external_mutation_verified": false,
                "registry_version": "standard-host-syntax-environment-v1",
                "runtime_builtin_verified": false,
                "standard_host_environment": "assumption"
              },
              "name": "URLSearchParams",
              "opaque_effects": {
                "count": 0,
                "effects_verified": false,
                "fixed_standard_host_premise_required": true,
                "outside_document_effects_verified": false,
                "samples": [],
                "truncated": false
              },
              "policy": {
                "consumer_registration_required": true,
                "invocation": "explicit_fixed_interface_audit",
                "role_configuration_consulted": false,
                "semantic_contract_registration_verified": false
              },
              "scope_identity": {
                "file": "packages/browser-core/src/scope-context.ts",
                "id": "1295eeb007d425a18356ea8961c05fea811c0d5399d9140668a5063e03967f2b",
                "scope_span": {
                  "end_byte": 6859,
                  "node_type": "statement_block",
                  "start_byte": 6398
                },
                "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d"
              },
              "source": {
                "at_location": {
                  "column": 26,
                  "column_base": 1,
                  "column_unit": "utf8_bytes",
                  "coordinate_space": "captured_text_utf8",
                  "end_byte": 6544,
                  "end_column": 41,
                  "end_line": 203,
                  "file": "packages/browser-core/src/scope-context.ts",
                  "grammar": "typescript",
                  "line": 203,
                  "original_file_end_byte": 6544,
                  "original_file_start_byte": 6529,
                  "parse_identity": {
                    "coordinate_space": "captured_text_utf8",
                    "derived_text_utf8_sha256": null,
                    "literal_authority": "original_saved_source_text_only",
                    "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                    "position_map": "identity_utf8_bytes_and_line_columns",
                    "projection_mode": "original",
                    "projection_version": "ts-syntax-projection-1",
                    "raw_prefix_bytes": 0,
                    "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                    "semantic_source_version": "semantic-snapshot-sources-1",
                    "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
                  },
                  "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "raw_prefix_bytes": 0,
                  "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
                  "source_excerpt": "URLSearchParams",
                  "source_excerpt_truncated": false,
                  "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                  "source_line": "  const parameters = new URLSearchParams(queryIndex < 0 ? '' : hash.slice(queryIndex + 1))",
                  "span_hash": "85c6cac623ea5e381dc34b8b0be265d53fe4e77795b08297e198f73e1b47882f",
                  "start_byte": 6529
                },
                "audit_scope": "authenticated_document",
                "budget_exceeded": false,
                "decision_computed_before_sampling": true,
                "file": "packages/browser-core/src/scope-context.ts",
                "node_budget": 100000,
                "nodes_reviewed": 1484,
                "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "scan_complete": true,
                "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28",
                "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d"
              },
              "state": "supported_in_registered_model",
              "supported": true,
              "unresolved": {
                "barrier_count": 0,
                "reason_codes": [],
                "samples": [],
                "truncated": false
              },
              "version": "captured-builtin-environment-1"
            },
            "id": "30fdd2012553aa5b0929ae63",
            "lexical_absence": {
              "gaps": [],
              "limitations": [
                "no captured local binding is not proof of a standard runtime value",
                "global/member/alias effects and external mutation need separate effect guards"
              ],
              "local_declaration_absent": true,
              "location": {
                "column": 26,
                "column_base": 1,
                "column_unit": "utf8_bytes",
                "coordinate_space": "captured_text_utf8",
                "end_byte": 6544,
                "end_column": 41,
                "end_line": 203,
                "file": "packages/browser-core/src/scope-context.ts",
                "grammar": "typescript",
                "line": 203,
                "original_file_end_byte": 6544,
                "original_file_start_byte": 6529,
                "parse_identity": {
                  "coordinate_space": "captured_text_utf8",
                  "derived_text_utf8_sha256": null,
                  "literal_authority": "original_saved_source_text_only",
                  "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                  "position_map": "identity_utf8_bytes_and_line_columns",
                  "projection_mode": "original",
                  "projection_version": "ts-syntax-projection-1",
                  "raw_prefix_bytes": 0,
                  "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "semantic_source_version": "semantic-snapshot-sources-1",
                  "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
                },
                "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "raw_prefix_bytes": 0,
                "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
                "source_excerpt": "URLSearchParams",
                "source_excerpt_truncated": false,
                "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "source_line": "  const parameters = new URLSearchParams(queryIndex < 0 ? '' : hash.slice(queryIndex + 1))",
                "span_hash": "85c6cac623ea5e381dc34b8b0be265d53fe4e77795b08297e198f73e1b47882f",
                "start_byte": 6529
              },
              "name": "URLSearchParams",
              "runtime_builtin_verified": false,
              "state": "unbound",
              "unbound": true,
              "version": "captured-lexical-bindings-3"
            },
            "lexical_model_version": "captured-lexical-bindings-3",
            "location": {
              "column": 26,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6544,
              "end_column": 41,
              "end_line": 203,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 203,
              "original_file_end_byte": 6544,
              "original_file_start_byte": 6529,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "URLSearchParams",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  const parameters = new URLSearchParams(queryIndex < 0 ? '' : hash.slice(queryIndex + 1))",
              "span_hash": "85c6cac623ea5e381dc34b8b0be265d53fe4e77795b08297e198f73e1b47882f",
              "start_byte": 6529
            },
            "member": null,
            "name": "URLSearchParams",
            "opaque_host_effects_proven": false,
            "operation": "captured_standard_api_environment",
            "owner": "scopeHash",
            "runtime_builtin_verified": false,
            "semantic_environment_version": "captured-builtin-environment-1",
            "standard_implementation_assumed": true,
            "visible_api_audit_scope": "authenticated_document"
          },
          {
            "argument_location": {
              "column": 42,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6593,
              "end_column": 90,
              "end_line": 203,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 203,
              "original_file_end_byte": 6593,
              "original_file_start_byte": 6545,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "queryIndex < 0 ? '' : hash.slice(queryIndex + 1)",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  const parameters = new URLSearchParams(queryIndex < 0 ? '' : hash.slice(queryIndex + 1))",
              "span_hash": "d5996a931a5cd759f8542906911c87a976856968f8b27150a4f171f7eb4fd8a8",
              "start_byte": 6545
            },
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "id": "3b5b2e20fda8ab79cdd3d831",
            "input_value_id": "abstract-21",
            "key_domain": {
              "guaranteed_keys": [
                "delivery"
              ],
              "invariant": "guaranteed subset actual subset possible only when keyset_closed",
              "keyset_closed": true,
              "possible_keys": [
                "delivery"
              ],
              "unknown_keys": false,
              "unknown_reasons": []
            },
            "location": {
              "column": 22,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6594,
              "end_column": 91,
              "end_line": 203,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 203,
              "original_file_end_byte": 6594,
              "original_file_start_byte": 6525,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "new URLSearchParams(queryIndex < 0 ? '' : hash.slice(queryIndex + 1))",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  const parameters = new URLSearchParams(queryIndex < 0 ? '' : hash.slice(queryIndex + 1))",
              "span_hash": "4a2b073e1b94cbbb306fe090e565caf6d807b8785a7293b736837fbe15ef11a5",
              "start_byte": 6525
            },
            "model": "url-search-params-v1",
            "operation": "url_search_params_seed",
            "owner": "scopeHash",
            "query_projection": null,
            "receiver_id": "abstract-26"
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "id": "5808f300380b0772a71be727",
            "location": {
              "column": 9,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6594,
              "end_column": 91,
              "end_line": 203,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 203,
              "original_file_end_byte": 6594,
              "original_file_start_byte": 6512,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "parameters = new URLSearchParams(queryIndex < 0 ? '' : hash.slice(queryIndex + 1))",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  const parameters = new URLSearchParams(queryIndex < 0 ? '' : hash.slice(queryIndex + 1))",
              "span_hash": "f9bed51206603680fa85672b72aa9a75c32d7ad79a06678e7a69bacc6caffa59",
              "start_byte": 6512
            },
            "name": "parameters",
            "operation": "local_value_binding",
            "owner": "scopeHash",
            "value": {
              "kind": "params",
              "query_domain": {
                "guaranteed_keys": [
                  "delivery"
                ],
                "invariant": "guaranteed subset actual subset possible only when keyset_closed",
                "keyset_closed": true,
                "possible_keys": [
                  "delivery"
                ],
                "unknown_keys": false,
                "unknown_reasons": []
              },
              "runtime_execution_proven": false,
              "source_value_id": "abstract-26"
            }
          },
          {
            "ast_owner_id": "module:ts:packages/browser-core/src/scope-context",
            "id": "8611565c65ad309103e450a5",
            "location": {
              "column": 3,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 256,
              "end_column": 19,
              "end_line": 13,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 13,
              "original_file_end_byte": 256,
              "original_file_start_byte": 240,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "'organizationId'",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  'organizationId',",
              "span_hash": "582bd2a1e335da02e14e5c24e3f99c86929bcbdd3a04a7286314a7c4a74321fe",
              "start_byte": 240
            },
            "operation": "literal_seed",
            "owner": "scopeHash",
            "text": "organizationId",
            "value": {
              "exact_text": "organizationId",
              "kind": "string",
              "runtime_execution_proven": false,
              "segments": [
                {
                  "kind": "literal",
                  "text": "organizationId"
                }
              ],
              "source_value_id": "abstract-27"
            }
          },
          {
            "ast_owner_id": "module:ts:packages/browser-core/src/scope-context",
            "id": "f66b9420b837af5d3032ea30",
            "location": {
              "column": 3,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 273,
              "end_column": 16,
              "end_line": 14,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 14,
              "original_file_end_byte": 273,
              "original_file_start_byte": 260,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "'workspaceId'",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  'workspaceId',",
              "span_hash": "5a4653694212bc251f515ba112dfe622f64a21c2970ca15e972fd46fe1886678",
              "start_byte": 260
            },
            "operation": "literal_seed",
            "owner": "scopeHash",
            "text": "workspaceId",
            "value": {
              "exact_text": "workspaceId",
              "kind": "string",
              "runtime_execution_proven": false,
              "segments": [
                {
                  "kind": "literal",
                  "text": "workspaceId"
                }
              ],
              "source_value_id": "abstract-28"
            }
          },
          {
            "ast_owner_id": "module:ts:packages/browser-core/src/scope-context",
            "id": "eb6beaacd8c5119198ccf094",
            "location": {
              "column": 3,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 288,
              "end_column": 14,
              "end_line": 15,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 15,
              "original_file_end_byte": 288,
              "original_file_start_byte": 277,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "'projectId'",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  'projectId',",
              "span_hash": "fedb0daae7cf185916a74d54fb96b3ed5a7c438f00967df0262dce7c1b5b3c61",
              "start_byte": 277
            },
            "operation": "literal_seed",
            "owner": "scopeHash",
            "text": "projectId",
            "value": {
              "exact_text": "projectId",
              "kind": "string",
              "runtime_execution_proven": false,
              "segments": [
                {
                  "kind": "literal",
                  "text": "projectId"
                }
              ],
              "source_value_id": "abstract-29"
            }
          },
          {
            "ast_owner_id": "module:ts:packages/browser-core/src/scope-context",
            "id": "f656366937ab9ba67cf544a1",
            "location": {
              "column": 3,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 306,
              "end_column": 17,
              "end_line": 16,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 16,
              "original_file_end_byte": 306,
              "original_file_start_byte": 292,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "'repositoryId'",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  'repositoryId',",
              "span_hash": "0db950830155f2e452795cf79a341041261e3985b64c3ffb1cb0e1fd8142e723",
              "start_byte": 292
            },
            "operation": "literal_seed",
            "owner": "scopeHash",
            "text": "repositoryId",
            "value": {
              "exact_text": "repositoryId",
              "kind": "string",
              "runtime_execution_proven": false,
              "segments": [
                {
                  "kind": "literal",
                  "text": "repositoryId"
                }
              ],
              "source_value_id": "abstract-30"
            }
          },
          {
            "ast_owner_id": "module:ts:packages/browser-core/src/scope-context",
            "environment_audit": {
              "host_aliases": {
                "count": 0,
                "model": "finite-captured-may-host-alias-1",
                "propagation_complete_within_model": true,
                "round_budget": 64,
                "runtime_receiver_verified": false,
                "same_runtime_object_verified": false,
                "samples": [],
                "supported_storage": "unique simple lexical destination; transparent/??/||/conditional possible origins",
                "truncated": false,
                "unsupported_container_storage_is_barrier": true
              },
              "lexical_absence": {
                "gaps": [],
                "limitations": [
                  "no captured local binding is not proof of a standard runtime value",
                  "global/member/alias effects and external mutation need separate effect guards"
                ],
                "local_declaration_absent": true,
                "location": {
                  "column": 31,
                  "column_base": 1,
                  "column_unit": "utf8_bytes",
                  "coordinate_space": "captured_text_utf8",
                  "end_byte": 235,
                  "end_column": 44,
                  "end_line": 12,
                  "file": "packages/browser-core/src/scope-context.ts",
                  "grammar": "typescript",
                  "line": 12,
                  "original_file_end_byte": 235,
                  "original_file_start_byte": 222,
                  "parse_identity": {
                    "coordinate_space": "captured_text_utf8",
                    "derived_text_utf8_sha256": null,
                    "literal_authority": "original_saved_source_text_only",
                    "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                    "position_map": "identity_utf8_bytes_and_line_columns",
                    "projection_mode": "original",
                    "projection_version": "ts-syntax-projection-1",
                    "raw_prefix_bytes": 0,
                    "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                    "semantic_source_version": "semantic-snapshot-sources-1",
                    "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
                  },
                  "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "raw_prefix_bytes": 0,
                  "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
                  "source_excerpt": "Object.freeze",
                  "source_excerpt_truncated": false,
                  "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                  "source_line": "const SCOPE_PARAMETER_NAMES = Object.freeze([",
                  "span_hash": "2bbb3c54a145ccc36198b5292862cd9107d2ec63a27a3b03186fbd68b9ceed07",
                  "start_byte": 222
                },
                "name": "Object",
                "runtime_builtin_verified": false,
                "state": "unbound",
                "unbound": true,
                "version": "captured-lexical-bindings-3"
              },
              "lexical_model_version": "captured-lexical-bindings-3",
              "locations": [],
              "member": "freeze",
              "model": {
                "allowed_prototype_member_interfaces": [
                  "hasOwnProperty",
                  "isPrototypeOf",
                  "propertyIsEnumerable",
                  "toLocaleString",
                  "toString",
                  "valueOf"
                ],
                "allowed_static_member_interfaces": [
                  "assign",
                  "entries",
                  "freeze",
                  "fromEntries",
                  "getOwnPropertyNames",
                  "getOwnPropertySymbols",
                  "getPrototypeOf",
                  "hasOwn",
                  "is",
                  "keys",
                  "values"
                ],
                "assumptions": [
                  "the explicitly registered host interfaces retain their standard behavior",
                  "opaque calls, host transport and other captured documents do not replace the modeled standard interfaces",
                  "captured alias/prototype/write barriers may not be overridden by this premise"
                ],
                "member_argument_effects_verified": false,
                "member_call_purity_verified": false,
                "member_registration_semantics": "fixed syntax interface occurrence only; argument and receiver effects require separate consumer guards",
                "profile_id": "object-standard-interface-1",
                "provider_or_external_mutation_verified": false,
                "registry_version": "standard-host-syntax-environment-v1",
                "runtime_builtin_verified": false,
                "standard_host_environment": "assumption"
              },
              "name": "Object",
              "opaque_effects": {
                "count": 0,
                "effects_verified": false,
                "fixed_standard_host_premise_required": true,
                "outside_document_effects_verified": false,
                "samples": [],
                "truncated": false
              },
              "policy": {
                "consumer_registration_required": true,
                "invocation": "explicit_fixed_interface_audit",
                "role_configuration_consulted": false,
                "semantic_contract_registration_verified": false
              },
              "scope_identity": {
                "file": "packages/browser-core/src/scope-context.ts",
                "id": "56781938f2409dee8b5da9557980968840cb81e7d9e6f3dddc26a9bd8187df4d",
                "scope_span": {
                  "end_byte": 9247,
                  "node_type": "program",
                  "start_byte": 0
                },
                "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d"
              },
              "source": {
                "at_location": {
                  "column": 31,
                  "column_base": 1,
                  "column_unit": "utf8_bytes",
                  "coordinate_space": "captured_text_utf8",
                  "end_byte": 235,
                  "end_column": 44,
                  "end_line": 12,
                  "file": "packages/browser-core/src/scope-context.ts",
                  "grammar": "typescript",
                  "line": 12,
                  "original_file_end_byte": 235,
                  "original_file_start_byte": 222,
                  "parse_identity": {
                    "coordinate_space": "captured_text_utf8",
                    "derived_text_utf8_sha256": null,
                    "literal_authority": "original_saved_source_text_only",
                    "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                    "position_map": "identity_utf8_bytes_and_line_columns",
                    "projection_mode": "original",
                    "projection_version": "ts-syntax-projection-1",
                    "raw_prefix_bytes": 0,
                    "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                    "semantic_source_version": "semantic-snapshot-sources-1",
                    "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
                  },
                  "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "raw_prefix_bytes": 0,
                  "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
                  "source_excerpt": "Object.freeze",
                  "source_excerpt_truncated": false,
                  "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                  "source_line": "const SCOPE_PARAMETER_NAMES = Object.freeze([",
                  "span_hash": "2bbb3c54a145ccc36198b5292862cd9107d2ec63a27a3b03186fbd68b9ceed07",
                  "start_byte": 222
                },
                "audit_scope": "authenticated_document",
                "budget_exceeded": false,
                "decision_computed_before_sampling": true,
                "file": "packages/browser-core/src/scope-context.ts",
                "node_budget": 100000,
                "nodes_reviewed": 1484,
                "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "scan_complete": true,
                "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28",
                "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d"
              },
              "state": "supported_in_registered_model",
              "supported": true,
              "unresolved": {
                "barrier_count": 0,
                "reason_codes": [],
                "samples": [],
                "truncated": false
              },
              "version": "captured-builtin-environment-1"
            },
            "id": "362f13ade68328f69e43d4a0",
            "lexical_absence": {
              "gaps": [],
              "limitations": [
                "no captured local binding is not proof of a standard runtime value",
                "global/member/alias effects and external mutation need separate effect guards"
              ],
              "local_declaration_absent": true,
              "location": {
                "column": 31,
                "column_base": 1,
                "column_unit": "utf8_bytes",
                "coordinate_space": "captured_text_utf8",
                "end_byte": 235,
                "end_column": 44,
                "end_line": 12,
                "file": "packages/browser-core/src/scope-context.ts",
                "grammar": "typescript",
                "line": 12,
                "original_file_end_byte": 235,
                "original_file_start_byte": 222,
                "parse_identity": {
                  "coordinate_space": "captured_text_utf8",
                  "derived_text_utf8_sha256": null,
                  "literal_authority": "original_saved_source_text_only",
                  "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                  "position_map": "identity_utf8_bytes_and_line_columns",
                  "projection_mode": "original",
                  "projection_version": "ts-syntax-projection-1",
                  "raw_prefix_bytes": 0,
                  "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "semantic_source_version": "semantic-snapshot-sources-1",
                  "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
                },
                "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "raw_prefix_bytes": 0,
                "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
                "source_excerpt": "Object.freeze",
                "source_excerpt_truncated": false,
                "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "source_line": "const SCOPE_PARAMETER_NAMES = Object.freeze([",
                "span_hash": "2bbb3c54a145ccc36198b5292862cd9107d2ec63a27a3b03186fbd68b9ceed07",
                "start_byte": 222
              },
              "name": "Object",
              "runtime_builtin_verified": false,
              "state": "unbound",
              "unbound": true,
              "version": "captured-lexical-bindings-3"
            },
            "lexical_model_version": "captured-lexical-bindings-3",
            "location": {
              "column": 31,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 235,
              "end_column": 44,
              "end_line": 12,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 12,
              "original_file_end_byte": 235,
              "original_file_start_byte": 222,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "Object.freeze",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "const SCOPE_PARAMETER_NAMES = Object.freeze([",
              "span_hash": "2bbb3c54a145ccc36198b5292862cd9107d2ec63a27a3b03186fbd68b9ceed07",
              "start_byte": 222
            },
            "member": "freeze",
            "name": "Object",
            "opaque_host_effects_proven": false,
            "operation": "captured_standard_api_environment",
            "owner": "scopeHash",
            "runtime_builtin_verified": false,
            "semantic_environment_version": "captured-builtin-environment-1",
            "standard_implementation_assumed": true,
            "visible_api_audit_scope": "authenticated_document"
          },
          {
            "array_location": {
              "column": 45,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 309,
              "end_column": 2,
              "end_line": 17,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 12,
              "original_file_end_byte": 309,
              "original_file_start_byte": 236,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "[\n  'organizationId',\n  'workspaceId',\n  'projectId',\n  'repositoryId',\n]",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "const SCOPE_PARAMETER_NAMES = Object.freeze([",
              "span_hash": "f67ed33a2e677cbf4614878ecddb2f057a037109d3c45cc5044a4e5afa9ccf53",
              "start_byte": 236
            },
            "ast_owner_id": "module:ts:packages/browser-core/src/scope-context",
            "id": "69362f1792fc7631a29bcf72",
            "keys": [
              "organizationId",
              "workspaceId",
              "projectId",
              "repositoryId"
            ],
            "location": {
              "column": 31,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 319,
              "end_column": 12,
              "end_line": 17,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 12,
              "original_file_end_byte": 319,
              "original_file_start_byte": 222,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "Object.freeze([\n  'organizationId',\n  'workspaceId',\n  'projectId',\n  'repositoryId',\n] as const)",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "const SCOPE_PARAMETER_NAMES = Object.freeze([",
              "span_hash": "a34afa614f0392bd4e4907ab9c5d82d79924e9597f2002195fa3f2cafd742cd3",
              "start_byte": 222
            },
            "model": "object-freeze-inert-v1",
            "operation": "frozen_literal_key_array",
            "owner": "scopeHash"
          },
          {
            "ast_owner_id": "module:ts:packages/browser-core/src/scope-context",
            "binding_id": "929e9977faf050b6e46d2a24917e19a26ba8318fcd89b8d4b7546c13008900d2",
            "id": "ad8f360166799f26b0ba3e57",
            "location": {
              "column": 7,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 319,
              "end_column": 12,
              "end_line": 17,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 12,
              "original_file_end_byte": 319,
              "original_file_start_byte": 198,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "SCOPE_PARAMETER_NAMES = Object.freeze([\n  'organizationId',\n  'workspaceId',\n  'projectId',\n  'repositoryId',\n] as const)",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "const SCOPE_PARAMETER_NAMES = Object.freeze([",
              "span_hash": "bdc7d13dda04760b0656106289deb0889cac1a24b42daf6583bd6c909585f026",
              "start_byte": 198
            },
            "operation": "lexical_const_origin",
            "owner": "scopeHash",
            "value": {
              "kind": "array",
              "runtime_execution_proven": false,
              "source_value_id": "abstract-31"
            }
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "id": "bf77390847ad0c004ff93ea8",
            "key_source_location": {
              "column": 22,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6637,
              "end_column": 43,
              "end_line": 204,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 204,
              "original_file_end_byte": 6637,
              "original_file_start_byte": 6616,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "SCOPE_PARAMETER_NAMES",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  for (const name of SCOPE_PARAMETER_NAMES) {",
              "span_hash": "025bd1d83cc8f5b411c2cde77855f904bf09471b61fe339602a798d5d8348a2f",
              "start_byte": 6616
            },
            "keys": [
              "organizationId",
              "workspaceId",
              "projectId",
              "repositoryId"
            ],
            "literal_array_location": {
              "column": 45,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 309,
              "end_column": 2,
              "end_line": 17,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 12,
              "original_file_end_byte": 309,
              "original_file_start_byte": 236,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "[\n  'organizationId',\n  'workspaceId',\n  'projectId',\n  'repositoryId',\n]",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "const SCOPE_PARAMETER_NAMES = Object.freeze([",
              "span_hash": "f67ed33a2e677cbf4614878ecddb2f057a037109d3c45cc5044a4e5afa9ccf53",
              "start_byte": 236
            },
            "location": {
              "column": 3,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6763,
              "end_column": 4,
              "end_line": 208,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 204,
              "original_file_end_byte": 6763,
              "original_file_start_byte": 6597,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "for (const name of SCOPE_PARAMETER_NAMES) {\n    const value = selection[name]\n    if (value === null) parameters.delete(name)\n    else parameters.set(name, value)\n  }",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  for (const name of SCOPE_PARAMETER_NAMES) {",
              "span_hash": "7c9a107a45f8e7342de027412f7d054bff259b1b66bcc4a37e67b0d29b1acc79",
              "start_byte": 6597
            },
            "operation": "finite_key_loop",
            "operator": "of",
            "owner": "scopeHash"
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "id": "6b75b23ef9c1a49dbf86cc6d",
            "location": {
              "column": 11,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6674,
              "end_column": 34,
              "end_line": 205,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 205,
              "original_file_end_byte": 6674,
              "original_file_start_byte": 6651,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "value = selection[name]",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    const value = selection[name]",
              "span_hash": "5f18b2654b22f6760328a960ff159f9038f60bf560b7c2252e32946162dea306",
              "start_byte": 6651
            },
            "name": "value",
            "operation": "local_value_binding",
            "owner": "scopeHash",
            "value": {
              "kind": "unknown",
              "runtime_execution_proven": false,
              "source_value_id": "abstract-33"
            }
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "id": "79c0582bd626affae1752eab",
            "key": "organizationId",
            "key_argument_location": {
              "column": 43,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6721,
              "end_column": 47,
              "end_line": 206,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 206,
              "original_file_end_byte": 6721,
              "original_file_start_byte": 6717,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "name",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    if (value === null) parameters.delete(name)",
              "span_hash": "82a3537ff0dbce7eec35d69edc3a189ee6f17d82f353a553f9aa96cb0be3ce89",
              "start_byte": 6717
            },
            "key_domain": {
              "guaranteed_keys": [
                "delivery"
              ],
              "invariant": "guaranteed subset actual subset possible only when keyset_closed",
              "keyset_closed": true,
              "possible_keys": [
                "delivery"
              ],
              "unknown_keys": false,
              "unknown_reasons": []
            },
            "location": {
              "column": 25,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6722,
              "end_column": 48,
              "end_line": 206,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 206,
              "original_file_end_byte": 6722,
              "original_file_start_byte": 6699,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "parameters.delete(name)",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    if (value === null) parameters.delete(name)",
              "span_hash": "47aef089e6d7878b0959c25ee22617f1269cdf2cd3ff8e795f5bceba9d5068c4",
              "start_byte": 6699
            },
            "method": "delete",
            "model": "url-search-params-v1",
            "operation": "query_key_mutation",
            "owner": "scopeHash",
            "receiver_id": "abstract-26"
          },
          {
            "action": null,
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "branch": true,
            "branch_continues": true,
            "branch_result_ids": [],
            "branch_result_kinds": [],
            "condition_text": "(value === null)",
            "condition_truth": null,
            "condition_value_id": "abstract-35",
            "consequent_coverage_complete": false,
            "factory_callback_contexts": [],
            "id": "8cbd4463e884b682835bab86",
            "location": {
              "column": 8,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6698,
              "end_column": 24,
              "end_line": 206,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 206,
              "original_file_end_byte": 6698,
              "original_file_start_byte": 6682,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "(value === null)",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    if (value === null) parameters.delete(name)",
              "span_hash": "cdbf37f515a6d8f9515accf5a86bc053e2e0d00553594bf09259989927c4aed9",
              "start_byte": 6682
            },
            "lookup_dependencies": [],
            "operation": "branch_guard",
            "owner": "scopeHash"
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "id": "e22e007d3e4ad9b9eb1c9502",
            "key": "organizationId",
            "key_argument_location": {
              "column": 25,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6751,
              "end_column": 29,
              "end_line": 207,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 207,
              "original_file_end_byte": 6751,
              "original_file_start_byte": 6747,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "name",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    else parameters.set(name, value)",
              "span_hash": "82a3537ff0dbce7eec35d69edc3a189ee6f17d82f353a553f9aa96cb0be3ce89",
              "start_byte": 6747
            },
            "key_domain": {
              "guaranteed_keys": [
                "delivery",
                "organizationId"
              ],
              "invariant": "guaranteed subset actual subset possible only when keyset_closed",
              "keyset_closed": true,
              "possible_keys": [
                "delivery",
                "organizationId"
              ],
              "unknown_keys": false,
              "unknown_reasons": []
            },
            "location": {
              "column": 10,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6759,
              "end_column": 37,
              "end_line": 207,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 207,
              "original_file_end_byte": 6759,
              "original_file_start_byte": 6732,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "parameters.set(name, value)",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    else parameters.set(name, value)",
              "span_hash": "a4f78ab3c37c381fb78ea38b2bacb075d356da0df6ddf60a2fee77c2fbfa8536",
              "start_byte": 6732
            },
            "method": "set",
            "model": "url-search-params-v1",
            "operation": "query_key_mutation",
            "owner": "scopeHash",
            "receiver_id": "abstract-26"
          },
          {
            "action": null,
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "branch": false,
            "branch_continues": true,
            "branch_result_ids": [],
            "branch_result_kinds": [],
            "condition_text": "(value === null)",
            "condition_truth": null,
            "condition_value_id": "abstract-35",
            "consequent_coverage_complete": false,
            "factory_callback_contexts": [],
            "id": "ec70a038838e560516535c4d",
            "location": {
              "column": 8,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6698,
              "end_column": 24,
              "end_line": 206,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 206,
              "original_file_end_byte": 6698,
              "original_file_start_byte": 6682,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "(value === null)",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    if (value === null) parameters.delete(name)",
              "span_hash": "cdbf37f515a6d8f9515accf5a86bc053e2e0d00553594bf09259989927c4aed9",
              "start_byte": 6682
            },
            "lookup_dependencies": [],
            "operation": "branch_guard",
            "owner": "scopeHash"
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "id": "6486581fcfe3738be7b6c093",
            "location": {
              "column": 11,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6674,
              "end_column": 34,
              "end_line": 205,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 205,
              "original_file_end_byte": 6674,
              "original_file_start_byte": 6651,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "value = selection[name]",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    const value = selection[name]",
              "span_hash": "5f18b2654b22f6760328a960ff159f9038f60bf560b7c2252e32946162dea306",
              "start_byte": 6651
            },
            "name": "value",
            "operation": "local_value_binding",
            "owner": "scopeHash",
            "value": {
              "kind": "unknown",
              "runtime_execution_proven": false,
              "source_value_id": "abstract-63"
            }
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "id": "d4b5912cac1552071de6a0e7",
            "key": "workspaceId",
            "key_argument_location": {
              "column": 43,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6721,
              "end_column": 47,
              "end_line": 206,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 206,
              "original_file_end_byte": 6721,
              "original_file_start_byte": 6717,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "name",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    if (value === null) parameters.delete(name)",
              "span_hash": "82a3537ff0dbce7eec35d69edc3a189ee6f17d82f353a553f9aa96cb0be3ce89",
              "start_byte": 6717
            },
            "key_domain": {
              "guaranteed_keys": [
                "delivery"
              ],
              "invariant": "guaranteed subset actual subset possible only when keyset_closed",
              "keyset_closed": true,
              "possible_keys": [
                "delivery",
                "organizationId"
              ],
              "unknown_keys": false,
              "unknown_reasons": []
            },
            "location": {
              "column": 25,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6722,
              "end_column": 48,
              "end_line": 206,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 206,
              "original_file_end_byte": 6722,
              "original_file_start_byte": 6699,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "parameters.delete(name)",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    if (value === null) parameters.delete(name)",
              "span_hash": "47aef089e6d7878b0959c25ee22617f1269cdf2cd3ff8e795f5bceba9d5068c4",
              "start_byte": 6699
            },
            "method": "delete",
            "model": "url-search-params-v1",
            "operation": "query_key_mutation",
            "owner": "scopeHash",
            "receiver_id": "abstract-55"
          },
          {
            "action": null,
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "branch": true,
            "branch_continues": true,
            "branch_result_ids": [],
            "branch_result_kinds": [],
            "condition_text": "(value === null)",
            "condition_truth": null,
            "condition_value_id": "abstract-65",
            "consequent_coverage_complete": false,
            "factory_callback_contexts": [],
            "id": "e3b9b5942502973ea1020635",
            "location": {
              "column": 8,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6698,
              "end_column": 24,
              "end_line": 206,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 206,
              "original_file_end_byte": 6698,
              "original_file_start_byte": 6682,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "(value === null)",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    if (value === null) parameters.delete(name)",
              "span_hash": "cdbf37f515a6d8f9515accf5a86bc053e2e0d00553594bf09259989927c4aed9",
              "start_byte": 6682
            },
            "lookup_dependencies": [],
            "operation": "branch_guard",
            "owner": "scopeHash"
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "id": "71d1c03653dcc60173333d58",
            "key": "workspaceId",
            "key_argument_location": {
              "column": 25,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6751,
              "end_column": 29,
              "end_line": 207,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 207,
              "original_file_end_byte": 6751,
              "original_file_start_byte": 6747,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "name",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    else parameters.set(name, value)",
              "span_hash": "82a3537ff0dbce7eec35d69edc3a189ee6f17d82f353a553f9aa96cb0be3ce89",
              "start_byte": 6747
            },
            "key_domain": {
              "guaranteed_keys": [
                "delivery",
                "workspaceId"
              ],
              "invariant": "guaranteed subset actual subset possible only when keyset_closed",
              "keyset_closed": true,
              "possible_keys": [
                "delivery",
                "organizationId",
                "workspaceId"
              ],
              "unknown_keys": false,
              "unknown_reasons": []
            },
            "location": {
              "column": 10,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6759,
              "end_column": 37,
              "end_line": 207,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 207,
              "original_file_end_byte": 6759,
              "original_file_start_byte": 6732,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "parameters.set(name, value)",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    else parameters.set(name, value)",
              "span_hash": "a4f78ab3c37c381fb78ea38b2bacb075d356da0df6ddf60a2fee77c2fbfa8536",
              "start_byte": 6732
            },
            "method": "set",
            "model": "url-search-params-v1",
            "operation": "query_key_mutation",
            "owner": "scopeHash",
            "receiver_id": "abstract-55"
          },
          {
            "action": null,
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "branch": false,
            "branch_continues": true,
            "branch_result_ids": [],
            "branch_result_kinds": [],
            "condition_text": "(value === null)",
            "condition_truth": null,
            "condition_value_id": "abstract-65",
            "consequent_coverage_complete": false,
            "factory_callback_contexts": [],
            "id": "934b49769461fbcced682ed2",
            "location": {
              "column": 8,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6698,
              "end_column": 24,
              "end_line": 206,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 206,
              "original_file_end_byte": 6698,
              "original_file_start_byte": 6682,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "(value === null)",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    if (value === null) parameters.delete(name)",
              "span_hash": "cdbf37f515a6d8f9515accf5a86bc053e2e0d00553594bf09259989927c4aed9",
              "start_byte": 6682
            },
            "lookup_dependencies": [],
            "operation": "branch_guard",
            "owner": "scopeHash"
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "id": "6d2b317e58caad7fb6f1c4f1",
            "location": {
              "column": 11,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6674,
              "end_column": 34,
              "end_line": 205,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 205,
              "original_file_end_byte": 6674,
              "original_file_start_byte": 6651,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "value = selection[name]",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    const value = selection[name]",
              "span_hash": "5f18b2654b22f6760328a960ff159f9038f60bf560b7c2252e32946162dea306",
              "start_byte": 6651
            },
            "name": "value",
            "operation": "local_value_binding",
            "owner": "scopeHash",
            "value": {
              "kind": "unknown",
              "runtime_execution_proven": false,
              "source_value_id": "abstract-93"
            }
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "id": "fe9b1a16210a0b792a46f5ff",
            "key": "projectId",
            "key_argument_location": {
              "column": 43,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6721,
              "end_column": 47,
              "end_line": 206,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 206,
              "original_file_end_byte": 6721,
              "original_file_start_byte": 6717,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "name",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    if (value === null) parameters.delete(name)",
              "span_hash": "82a3537ff0dbce7eec35d69edc3a189ee6f17d82f353a553f9aa96cb0be3ce89",
              "start_byte": 6717
            },
            "key_domain": {
              "guaranteed_keys": [
                "delivery"
              ],
              "invariant": "guaranteed subset actual subset possible only when keyset_closed",
              "keyset_closed": true,
              "possible_keys": [
                "delivery",
                "organizationId",
                "workspaceId"
              ],
              "unknown_keys": false,
              "unknown_reasons": []
            },
            "location": {
              "column": 25,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6722,
              "end_column": 48,
              "end_line": 206,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 206,
              "original_file_end_byte": 6722,
              "original_file_start_byte": 6699,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "parameters.delete(name)",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    if (value === null) parameters.delete(name)",
              "span_hash": "47aef089e6d7878b0959c25ee22617f1269cdf2cd3ff8e795f5bceba9d5068c4",
              "start_byte": 6699
            },
            "method": "delete",
            "model": "url-search-params-v1",
            "operation": "query_key_mutation",
            "owner": "scopeHash",
            "receiver_id": "abstract-85"
          },
          {
            "action": null,
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "branch": true,
            "branch_continues": true,
            "branch_result_ids": [],
            "branch_result_kinds": [],
            "condition_text": "(value === null)",
            "condition_truth": null,
            "condition_value_id": "abstract-95",
            "consequent_coverage_complete": false,
            "factory_callback_contexts": [],
            "id": "a951e4f8b3e405f580968be8",
            "location": {
              "column": 8,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6698,
              "end_column": 24,
              "end_line": 206,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 206,
              "original_file_end_byte": 6698,
              "original_file_start_byte": 6682,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "(value === null)",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    if (value === null) parameters.delete(name)",
              "span_hash": "cdbf37f515a6d8f9515accf5a86bc053e2e0d00553594bf09259989927c4aed9",
              "start_byte": 6682
            },
            "lookup_dependencies": [],
            "operation": "branch_guard",
            "owner": "scopeHash"
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "id": "b7166c149793391cc788aa2a",
            "key": "projectId",
            "key_argument_location": {
              "column": 25,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6751,
              "end_column": 29,
              "end_line": 207,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 207,
              "original_file_end_byte": 6751,
              "original_file_start_byte": 6747,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "name",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    else parameters.set(name, value)",
              "span_hash": "82a3537ff0dbce7eec35d69edc3a189ee6f17d82f353a553f9aa96cb0be3ce89",
              "start_byte": 6747
            },
            "key_domain": {
              "guaranteed_keys": [
                "delivery",
                "projectId"
              ],
              "invariant": "guaranteed subset actual subset possible only when keyset_closed",
              "keyset_closed": true,
              "possible_keys": [
                "delivery",
                "organizationId",
                "projectId",
                "workspaceId"
              ],
              "unknown_keys": false,
              "unknown_reasons": []
            },
            "location": {
              "column": 10,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6759,
              "end_column": 37,
              "end_line": 207,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 207,
              "original_file_end_byte": 6759,
              "original_file_start_byte": 6732,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "parameters.set(name, value)",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    else parameters.set(name, value)",
              "span_hash": "a4f78ab3c37c381fb78ea38b2bacb075d356da0df6ddf60a2fee77c2fbfa8536",
              "start_byte": 6732
            },
            "method": "set",
            "model": "url-search-params-v1",
            "operation": "query_key_mutation",
            "owner": "scopeHash",
            "receiver_id": "abstract-85"
          },
          {
            "action": null,
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "branch": false,
            "branch_continues": true,
            "branch_result_ids": [],
            "branch_result_kinds": [],
            "condition_text": "(value === null)",
            "condition_truth": null,
            "condition_value_id": "abstract-95",
            "consequent_coverage_complete": false,
            "factory_callback_contexts": [],
            "id": "ee01aecce1b2d13f3170f7be",
            "location": {
              "column": 8,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6698,
              "end_column": 24,
              "end_line": 206,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 206,
              "original_file_end_byte": 6698,
              "original_file_start_byte": 6682,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "(value === null)",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    if (value === null) parameters.delete(name)",
              "span_hash": "cdbf37f515a6d8f9515accf5a86bc053e2e0d00553594bf09259989927c4aed9",
              "start_byte": 6682
            },
            "lookup_dependencies": [],
            "operation": "branch_guard",
            "owner": "scopeHash"
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "id": "e8758cc1816a309e14321750",
            "location": {
              "column": 11,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6674,
              "end_column": 34,
              "end_line": 205,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 205,
              "original_file_end_byte": 6674,
              "original_file_start_byte": 6651,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "value = selection[name]",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    const value = selection[name]",
              "span_hash": "5f18b2654b22f6760328a960ff159f9038f60bf560b7c2252e32946162dea306",
              "start_byte": 6651
            },
            "name": "value",
            "operation": "local_value_binding",
            "owner": "scopeHash",
            "value": {
              "kind": "unknown",
              "runtime_execution_proven": false,
              "source_value_id": "abstract-123"
            }
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "id": "38fbf0c2d8ac778a4d753547",
            "key": "repositoryId",
            "key_argument_location": {
              "column": 43,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6721,
              "end_column": 47,
              "end_line": 206,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 206,
              "original_file_end_byte": 6721,
              "original_file_start_byte": 6717,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "name",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    if (value === null) parameters.delete(name)",
              "span_hash": "82a3537ff0dbce7eec35d69edc3a189ee6f17d82f353a553f9aa96cb0be3ce89",
              "start_byte": 6717
            },
            "key_domain": {
              "guaranteed_keys": [
                "delivery"
              ],
              "invariant": "guaranteed subset actual subset possible only when keyset_closed",
              "keyset_closed": true,
              "possible_keys": [
                "delivery",
                "organizationId",
                "projectId",
                "workspaceId"
              ],
              "unknown_keys": false,
              "unknown_reasons": []
            },
            "location": {
              "column": 25,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6722,
              "end_column": 48,
              "end_line": 206,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 206,
              "original_file_end_byte": 6722,
              "original_file_start_byte": 6699,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "parameters.delete(name)",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    if (value === null) parameters.delete(name)",
              "span_hash": "47aef089e6d7878b0959c25ee22617f1269cdf2cd3ff8e795f5bceba9d5068c4",
              "start_byte": 6699
            },
            "method": "delete",
            "model": "url-search-params-v1",
            "operation": "query_key_mutation",
            "owner": "scopeHash",
            "receiver_id": "abstract-115"
          },
          {
            "action": null,
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "branch": true,
            "branch_continues": true,
            "branch_result_ids": [],
            "branch_result_kinds": [],
            "condition_text": "(value === null)",
            "condition_truth": null,
            "condition_value_id": "abstract-125",
            "consequent_coverage_complete": false,
            "factory_callback_contexts": [],
            "id": "da44798991cd55798d8726e4",
            "location": {
              "column": 8,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6698,
              "end_column": 24,
              "end_line": 206,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 206,
              "original_file_end_byte": 6698,
              "original_file_start_byte": 6682,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "(value === null)",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    if (value === null) parameters.delete(name)",
              "span_hash": "cdbf37f515a6d8f9515accf5a86bc053e2e0d00553594bf09259989927c4aed9",
              "start_byte": 6682
            },
            "lookup_dependencies": [],
            "operation": "branch_guard",
            "owner": "scopeHash"
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "id": "b56d00275b116e86fd49b2bf",
            "key": "repositoryId",
            "key_argument_location": {
              "column": 25,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6751,
              "end_column": 29,
              "end_line": 207,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 207,
              "original_file_end_byte": 6751,
              "original_file_start_byte": 6747,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "name",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    else parameters.set(name, value)",
              "span_hash": "82a3537ff0dbce7eec35d69edc3a189ee6f17d82f353a553f9aa96cb0be3ce89",
              "start_byte": 6747
            },
            "key_domain": {
              "guaranteed_keys": [
                "delivery",
                "repositoryId"
              ],
              "invariant": "guaranteed subset actual subset possible only when keyset_closed",
              "keyset_closed": true,
              "possible_keys": [
                "delivery",
                "organizationId",
                "projectId",
                "repositoryId",
                "workspaceId"
              ],
              "unknown_keys": false,
              "unknown_reasons": []
            },
            "location": {
              "column": 10,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6759,
              "end_column": 37,
              "end_line": 207,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 207,
              "original_file_end_byte": 6759,
              "original_file_start_byte": 6732,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "parameters.set(name, value)",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    else parameters.set(name, value)",
              "span_hash": "a4f78ab3c37c381fb78ea38b2bacb075d356da0df6ddf60a2fee77c2fbfa8536",
              "start_byte": 6732
            },
            "method": "set",
            "model": "url-search-params-v1",
            "operation": "query_key_mutation",
            "owner": "scopeHash",
            "receiver_id": "abstract-115"
          },
          {
            "action": null,
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "branch": false,
            "branch_continues": true,
            "branch_result_ids": [],
            "branch_result_kinds": [],
            "condition_text": "(value === null)",
            "condition_truth": null,
            "condition_value_id": "abstract-125",
            "consequent_coverage_complete": false,
            "factory_callback_contexts": [],
            "id": "0c666d9dfdb82d3e7423df02",
            "location": {
              "column": 8,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6698,
              "end_column": 24,
              "end_line": 206,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 206,
              "original_file_end_byte": 6698,
              "original_file_start_byte": 6682,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "(value === null)",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "    if (value === null) parameters.delete(name)",
              "span_hash": "cdbf37f515a6d8f9515accf5a86bc053e2e0d00553594bf09259989927c4aed9",
              "start_byte": 6682
            },
            "lookup_dependencies": [],
            "operation": "branch_guard",
            "owner": "scopeHash"
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "id": "a640baeaf0317da082e25f52",
            "key_domain": {
              "guaranteed_keys": [
                "delivery"
              ],
              "invariant": "guaranteed subset actual subset possible only when keyset_closed",
              "keyset_closed": true,
              "possible_keys": [
                "delivery",
                "organizationId",
                "projectId",
                "repositoryId",
                "workspaceId"
              ],
              "unknown_keys": false,
              "unknown_reasons": []
            },
            "location": {
              "column": 17,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6801,
              "end_column": 38,
              "end_line": 209,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 209,
              "original_file_end_byte": 6801,
              "original_file_start_byte": 6780,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "parameters.toString()",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  const query = parameters.toString()",
              "span_hash": "361b75b42ceb78b734efc3f939d3284e960325a7c99bb05a98dfc8faa30d8280",
              "start_byte": 6780
            },
            "model": "url-search-params-v1",
            "operation": "query_serialization",
            "owner": "scopeHash",
            "receiver_id": "abstract-145"
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "id": "e48c29bc88e4ad912ebaebf9",
            "location": {
              "column": 9,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6801,
              "end_column": 38,
              "end_line": 209,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 209,
              "original_file_end_byte": 6801,
              "original_file_start_byte": 6772,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "query = parameters.toString()",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  const query = parameters.toString()",
              "span_hash": "72e28e073a0129a9957ac7e4911bfc164cf6e68a85e8b8797aa0130cf69b1121",
              "start_byte": 6772
            },
            "name": "query",
            "operation": "local_value_binding",
            "owner": "scopeHash",
            "value": {
              "kind": "serialized",
              "query_domain": {
                "guaranteed_keys": [
                  "delivery"
                ],
                "invariant": "guaranteed subset actual subset possible only when keyset_closed",
                "keyset_closed": true,
                "possible_keys": [
                  "delivery",
                  "organizationId",
                  "projectId",
                  "repositoryId",
                  "workspaceId"
                ],
                "unknown_keys": false,
                "unknown_reasons": []
              },
              "runtime_execution_proven": false,
              "source_value_id": "abstract-152"
            }
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "id": "152c35ea299a2130bd16a304",
            "location": {
              "column": 38,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6857,
              "end_column": 56,
              "end_line": 210,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 210,
              "original_file_end_byte": 6857,
              "original_file_start_byte": 6839,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "`${path}?${query}`",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  return query.length === 0 ? path : `${path}?${query}`",
              "span_hash": "7238cc0530cc78504c48fdd385829f6db1894a0a64d01eb0bfb72ab30829811e",
              "start_byte": 6839
            },
            "operation": "template_construction",
            "owner": "scopeHash",
            "segments": [
              {
                "kind": "literal",
                "text": "#/home/review"
              },
              {
                "kind": "literal",
                "text": "?"
              },
              {
                "kind": "serialized",
                "source_value_id": "abstract-152"
              }
            ]
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "condition_location": {
              "column": 10,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6829,
              "end_column": 28,
              "end_line": 210,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 210,
              "original_file_end_byte": 6829,
              "original_file_start_byte": 6811,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "query.length === 0",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  return query.length === 0 ? path : `${path}?${query}`",
              "span_hash": "49cfd93bb8ea528f756953145f1848e17ff287033974c70741c9847c5362bcb9",
              "start_byte": 6811
            },
            "condition_truth": false,
            "id": "1a9604e6fcb0790f09cc4ca8",
            "input_value_ids": [
              "abstract-158"
            ],
            "location": {
              "column": 10,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6857,
              "end_column": 56,
              "end_line": 210,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 210,
              "original_file_end_byte": 6857,
              "original_file_start_byte": 6811,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "query.length === 0 ? path : `${path}?${query}`",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  return query.length === 0 ? path : `${path}?${query}`",
              "span_hash": "29585299eb43f5c266be20402bd6000fe94f61895a72e420e8040717a52f3ea4",
              "start_byte": 6811
            },
            "operation": "conditional_value_join",
            "owner": "scopeHash",
            "result": {
              "exact_text": null,
              "kind": "string",
              "runtime_execution_proven": false,
              "segments": [
                {
                  "kind": "literal",
                  "text": "#/home/review"
                },
                {
                  "kind": "literal",
                  "text": "?"
                },
                {
                  "kind": "serialized",
                  "source_value_id": "abstract-152"
                }
              ],
              "source_value_id": "abstract-158"
            }
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "expression_location": {
              "column": 10,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6857,
              "end_column": 56,
              "end_line": 210,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 210,
              "original_file_end_byte": 6857,
              "original_file_start_byte": 6811,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "query.length === 0 ? path : `${path}?${query}`",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  return query.length === 0 ? path : `${path}?${query}`",
              "span_hash": "29585299eb43f5c266be20402bd6000fe94f61895a72e420e8040717a52f3ea4",
              "start_byte": 6811
            },
            "id": "d0af050f648adb58be7989d6",
            "location": {
              "column": 3,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6857,
              "end_column": 56,
              "end_line": 210,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 210,
              "original_file_end_byte": 6857,
              "original_file_start_byte": 6804,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "return query.length === 0 ? path : `${path}?${query}`",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  return query.length === 0 ? path : `${path}?${query}`",
              "span_hash": "0e48c287b42b5f1098b33039ea5e0afb6b3ab4085525c08321e839bfbceaebf3",
              "start_byte": 6804
            },
            "normal_return_only": true,
            "operation": "return_expression",
            "owner": "scopeHash",
            "value": {
              "exact_text": null,
              "kind": "string",
              "runtime_execution_proven": false,
              "segments": [
                {
                  "kind": "literal",
                  "text": "#/home/review"
                },
                {
                  "kind": "literal",
                  "text": "?"
                },
                {
                  "kind": "serialized",
                  "source_value_id": "abstract-152"
                }
              ],
              "source_value_id": "abstract-158"
            }
          },
          {
            "ast_owner_id": "module:ts:packages/browser-core/src/scope-context",
            "caller_call_location": {
              "column": 9,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 8841,
              "end_column": 99,
              "end_line": 226,
              "file": "apps/client/src/home-dashboard-page.ts",
              "grammar": "typescript",
              "line": 226,
              "original_file_end_byte": 8841,
              "original_file_start_byte": 8751,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "709b4728fef637f15f8e0f4d0d42bd14002b4c594b473f770a337a40db908062",
              "source_excerpt": "scopeHash(`#/home/review?delivery=${encodeURIComponent(card.deliveryId)}`, scopeSelection)",
              "source_excerpt_truncated": false,
              "source_hash": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
              "source_line": "      : scopeHash(`#/home/review?delivery=${encodeURIComponent(card.deliveryId)}`, scopeSelection)",
              "span_hash": "37a6bb71e84d60b80259cbb25cd94d9beb10b1074cd93640d12f965106f0bc82",
              "start_byte": 8751
            },
            "completion_summaries_version": "captured-completion-summaries-1",
            "helper_function_kind": {
              "async": false,
              "body_activation_proved": false,
              "body_throw_effect": "synchronous_throw",
              "generator": false,
              "invocation_result": "arbitrary_value_or_throw",
              "kind": "ordinary_sync",
              "location": {
                "column": 8,
                "column_base": 1,
                "column_unit": "utf8_bytes",
                "coordinate_space": "captured_text_utf8",
                "end_byte": 6859,
                "end_column": 2,
                "end_line": 211,
                "file": "packages/browser-core/src/scope-context.ts",
                "line": 197,
                "original_file_end_byte": 6859,
                "original_file_start_byte": 6288,
                "raw_prefix_bytes": 0,
                "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
                "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "span_hash": "af14adff0c0198833642e881fa069b1facd3b5a4f91eb04afdd5ef428fb4e38f",
                "start_byte": 6288
              },
              "ordinary": true,
              "own_yield_present": false,
              "reason": null,
              "runtime_verified": false,
              "thenable_identity_not_inferred": true,
              "version": "captured-completion-summaries-1"
            },
            "id": "b242e24a0391588654b04dbe",
            "location": {
              "column": 8,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 6859,
              "end_column": 2,
              "end_line": 211,
              "file": "packages/browser-core/src/scope-context.ts",
              "grammar": "typescript",
              "line": 197,
              "original_file_end_byte": 6859,
              "original_file_start_byte": 6288,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "5c96019d177c7c1bacdf6f45052e5e51741f14cccd832a3030db19f38795ba33",
              "source_excerpt": "function scopeHash(\n  hash: string,\n  selection: ScopeRouteSelection | CompleteRepositorySelection,\n): string {\n  const queryIndex = hash.indexOf('?')\n  const path = queryIndex < 0 ? hash : hash.slice(0, queryIndex)\n  const parameters = new URLSearchParams(queryIndex < 0 ? '' : hash.slice(queryIndex + 1))\n  for (const name of SCOPE_PARAMETER_NAMES) {\n    const value = selection[name]\n    if (value === null) parameters.delete(name)\n    else parameters.set(name, value)\n  }\n  const query = parameters.toString()\n  return query.length === 0 ? path : `${path}?${query}`\n}",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "export function scopeHash(",
              "span_hash": "af14adff0c0198833642e881fa069b1facd3b5a4f91eb04afdd5ef428fb4e38f",
              "start_byte": 6288
            },
            "normal_return_only": true,
            "operation": "helper_normal_return",
            "owner": "scopeHash",
            "result": {
              "exact_text": null,
              "kind": "string",
              "runtime_execution_proven": false,
              "segments": [
                {
                  "kind": "literal",
                  "text": "#/home/review"
                },
                {
                  "kind": "literal",
                  "text": "?"
                },
                {
                  "kind": "serialized",
                  "source_value_id": "abstract-152"
                }
              ],
              "source_value_id": "abstract-158"
            }
          },
          {
            "ast_owner_id": "ts:apps/client/src/home-dashboard-page#homeDecisionHash",
            "id": "4332aec6484abfae0611af9c",
            "location": {
              "column": 9,
              "column_base": 1,
              "column_unit": "utf8_bytes",
              "coordinate_space": "captured_text_utf8",
              "end_byte": 8841,
              "end_column": 99,
              "end_line": 226,
              "file": "apps/client/src/home-dashboard-page.ts",
              "grammar": "typescript",
              "line": 226,
              "original_file_end_byte": 8841,
              "original_file_start_byte": 8751,
              "parse_identity": {
                "coordinate_space": "captured_text_utf8",
                "derived_text_utf8_sha256": null,
                "literal_authority": "original_saved_source_text_only",
                "original_text_utf8_sha256": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
                "position_map": "identity_utf8_bytes_and_line_columns",
                "projection_mode": "original",
                "projection_version": "ts-syntax-projection-1",
                "raw_prefix_bytes": 0,
                "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "709b4728fef637f15f8e0f4d0d42bd14002b4c594b473f770a337a40db908062",
              "source_excerpt": "scopeHash(`#/home/review?delivery=${encodeURIComponent(card.deliveryId)}`, scopeSelection)",
              "source_excerpt_truncated": false,
              "source_hash": "e0d08218021a360f0fb9c39ef18e40c6e7242c42fa6bda3207264827db6e806f",
              "source_line": "      : scopeHash(`#/home/review?delivery=${encodeURIComponent(card.deliveryId)}`, scopeSelection)",
              "span_hash": "37a6bb71e84d60b80259cbb25cd94d9beb10b1074cd93640d12f965106f0bc82",
              "start_byte": 8751
            },
            "operation": "selected_navigation_source",
            "owner": "homeDecisionHash",
            "query_domain": {
              "guaranteed_keys": [
                "delivery"
              ],
              "invariant": "guaranteed subset actual subset possible only when keyset_closed",
              "keyset_closed": true,
              "possible_keys": [
                "delivery",
                "organizationId",
                "projectId",
                "repositoryId",
                "workspaceId"
              ],
              "unknown_keys": false,
              "unknown_reasons": []
            },
            "selector": {
              "callee": "scopeHash",
              "file": "apps/client/src/home-dashboard-page.ts",
              "site": "call",
              "symbol": "homeDecisionHash"
            }
          }
        ],
        "source_trace_complete": true
      }
    },
    {
      "actual_branch_fact": {
        "id": "port-fact:7698ba2f501c86ad561a6893",
        "inputs": [
          "port-fact:06569fb7beea3598f04019e6",
          "port-fact:17dd0f4ed381bab8909e3fa9"
        ],
        "locations": [
          {
            "column": 9,
            "column_base": 1,
            "column_unit": "utf8_bytes",
            "coordinate_space": "captured_text_utf8",
            "end_byte": 12354,
            "end_column": 9,
            "end_line": 310,
            "file": "apps/client/src/application.ts",
            "grammar": "typescript",
            "line": 277,
            "original_file_end_byte": 12354,
            "original_file_start_byte": 10816,
            "parse_identity": {
              "coordinate_space": "captured_text_utf8",
              "derived_text_utf8_sha256": "8d7e28af6ec3d6c522c31dde15f5a4e887fa8a147b2e6d847e9b8f7983a9ef9b",
              "literal_authority": "original_saved_source_text_only",
              "original_text_utf8_sha256": "fa99231ab15cabe394bbfaac6d7baa59313c4da44c47e5f39101d617c95aa520",
              "position_map": "identity_utf8_bytes_and_line_columns",
              "projection_mode": "adapted",
              "projection_version": "ts-syntax-projection-1",
              "raw_prefix_bytes": 0,
              "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "semantic_source_version": "semantic-snapshot-sources-1",
              "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
            },
            "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
            "raw_prefix_bytes": 0,
            "semantic_parse_id": "3f313b5b2b2a3bcfbddb945b29af40a31210da369f5655a53da97ec48d67b7ab",
            "source_excerpt": "taskPort = options.taskSeed === undefined\n    ? createControlPlaneTaskPort({\n        client: controlPlane,\n        actor: () => authenticatedRouteContext()?.actor ?? null,\n        scope: () => authenticatedRouteContext()?.scope ?? null,\n        nextRequestId: () => contractId('req', browser.crypto) as RequestId,\n        nextWorkItemId: () => contractId('wit', browser.crypto) as WorkItemId,\n        workerSessions,\n        async deliveryContext() {\n          const context = authenticatedRouteContext()\n          const deliveryId = routeParameters(browser.location.hash).get('delivery') as DeliveryId | null\n          if (context === null || deliveryId === null) return null\n          const aggregate = await queryWorkRunAggregate(controlPlane, {\n            actor: context.actor,\n            scope: context.scope,\n            requestId: contractId('req', browser.crypto) as RequestId,\n            workItemId: null,\n            deliveryId,\n          })\n          const criterion = aggregate.contract.criteria.find(candidate => candidate.required)\n            ?? aggregate.contract.criteria[0]\n          if (criterion === undefined) return null\n          return {\n            deliveryId,\n            expectedRevision: aggregate.readCursor.deliveryRevision,\n            contractRevision: aggregate.contract.revision,\n            criterionId: criterion.id,\n          }\n        },\n      })\n    : createControlPlaneTaskFake({\n        nextTaskId: () => contractId('wit', browser.crypto) as WorkItemId,\n        seed: options.taskSeed,\n      })",
            "source_excerpt_truncated": false,
            "source_hash": "fa99231ab15cabe394bbfaac6d7baa59313c4da44c47e5f39101d617c95aa520",
            "source_line": "  const taskPort = options.taskSeed === undefined",
            "span_hash": "7f392d760f527f4c5cc59b32f2eeed81e9e82f067454db369c3285affb5a8216",
            "start_byte": 10816
          },
          {
            "column": 20,
            "column_base": 1,
            "column_unit": "utf8_bytes",
            "coordinate_space": "captured_text_utf8",
            "end_byte": 10857,
            "end_column": 50,
            "end_line": 277,
            "file": "apps/client/src/application.ts",
            "grammar": "typescript",
            "line": 277,
            "original_file_end_byte": 10857,
            "original_file_start_byte": 10827,
            "parse_identity": {
              "coordinate_space": "captured_text_utf8",
              "derived_text_utf8_sha256": "8d7e28af6ec3d6c522c31dde15f5a4e887fa8a147b2e6d847e9b8f7983a9ef9b",
              "literal_authority": "original_saved_source_text_only",
              "original_text_utf8_sha256": "fa99231ab15cabe394bbfaac6d7baa59313c4da44c47e5f39101d617c95aa520",
              "position_map": "identity_utf8_bytes_and_line_columns",
              "projection_mode": "adapted",
              "projection_version": "ts-syntax-projection-1",
              "raw_prefix_bytes": 0,
              "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "semantic_source_version": "semantic-snapshot-sources-1",
              "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
            },
            "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
            "raw_prefix_bytes": 0,
            "semantic_parse_id": "3f313b5b2b2a3bcfbddb945b29af40a31210da369f5655a53da97ec48d67b7ab",
            "source_excerpt": "options.taskSeed === undefined",
            "source_excerpt_truncated": false,
            "source_hash": "fa99231ab15cabe394bbfaac6d7baa59313c4da44c47e5f39101d617c95aa520",
            "source_line": "  const taskPort = options.taskSeed === undefined",
            "span_hash": "bab9a2bf052ead1267e5146d6d9dc6972a494110f0ea7457ae25e2cae69f1cf9",
            "start_byte": 10827
          },
          {
            "column": 7,
            "column_base": 1,
            "column_unit": "utf8_bytes",
            "coordinate_space": "captured_text_utf8",
            "end_byte": 12203,
            "end_column": 9,
            "end_line": 306,
            "file": "apps/client/src/application.ts",
            "grammar": "typescript",
            "line": 278,
            "original_file_end_byte": 12203,
            "original_file_start_byte": 10864,
            "parse_identity": {
              "coordinate_space": "captured_text_utf8",
              "derived_text_utf8_sha256": "8d7e28af6ec3d6c522c31dde15f5a4e887fa8a147b2e6d847e9b8f7983a9ef9b",
              "literal_authority": "original_saved_source_text_only",
              "original_text_utf8_sha256": "fa99231ab15cabe394bbfaac6d7baa59313c4da44c47e5f39101d617c95aa520",
              "position_map": "identity_utf8_bytes_and_line_columns",
              "projection_mode": "adapted",
              "projection_version": "ts-syntax-projection-1",
              "raw_prefix_bytes": 0,
              "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "semantic_source_version": "semantic-snapshot-sources-1",
              "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
            },
            "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
            "raw_prefix_bytes": 0,
            "semantic_parse_id": "3f313b5b2b2a3bcfbddb945b29af40a31210da369f5655a53da97ec48d67b7ab",
            "source_excerpt": "createControlPlaneTaskPort({\n        client: controlPlane,\n        actor: () => authenticatedRouteContext()?.actor ?? null,\n        scope: () => authenticatedRouteContext()?.scope ?? null,\n        nextRequestId: () => contractId('req', browser.crypto) as RequestId,\n        nextWorkItemId: () => contractId('wit', browser.crypto) as WorkItemId,\n        workerSessions,\n        async deliveryContext() {\n          const context = authenticatedRouteContext()\n          const deliveryId = routeParameters(browser.location.hash).get('delivery') as DeliveryId | null\n          if (context === null || deliveryId === null) return null\n          const aggregate = await queryWorkRunAggregate(controlPlane, {\n            actor: context.actor,\n            scope: context.scope,\n            requestId: contractId('req', browser.crypto) as RequestId,\n            workItemId: null,\n            deliveryId,\n          })\n          const criterion = aggregate.contract.criteria.find(candidate => candidate.required)\n            ?? aggregate.contract.criteria[0]\n          if (criterion === undefined) return null\n          return {\n            deliveryId,\n            expectedRevision: aggregate.readCursor.deliveryRevision,\n            contractRevision: aggregate.contract.revision,\n            criterionId: criterion.id,\n          }\n        },\n      })",
            "source_excerpt_truncated": false,
            "source_hash": "fa99231ab15cabe394bbfaac6d7baa59313c4da44c47e5f39101d617c95aa520",
            "source_line": "    ? createControlPlaneTaskPort({",
            "span_hash": "4c419ffca1e96250533fa1997f17ad9e95836b562cc58837f7059e658d7900d9",
            "start_byte": 10864
          }
        ],
        "observed": {
          "boot_literal_property_present": false,
          "boot_property_is_undefined_in_model": true,
          "factory_selected_for_this_boot": true,
          "guard_property_derived": "taskSeed",
          "guard_truth_in_model": true,
          "operator": "===",
          "parameter_declaration_id": "9007a9c777edb6a76654b81d5edb7d0fbfd69d5420f3b2bdb1bb1a1f9e81e520",
          "port_declaration_id": "8e7521371f98e8122a3a359def00d0caf9254ae1be3c68e93a9413caca2e1179",
          "requested_factory_branch": "consequence",
          "selected_branch": "consequence"
        },
        "operation": "boot_undefined_guard_selects_port_branch",
        "owner": "apps/client/src/application.ts",
        "semantic_source_version": "semantic-snapshot-sources-1",
        "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
      },
      "kind": "nondefault_seed_uses_alternate_factory"
    }
  ],
  "supported": true
}
```

必要缺口：

```json
[]
```

| 必要关系 | 结果 |
| --- | --- |
| N1 | supported |
| N2 | supported |
| N3 | supported |
| N4 | supported |
| N5 | supported |
| N6 | supported |
| N7 | supported |

### WWC-02

评估：`scoped_static_judgment_reproduced`；完整裁决：`true`。

保存发现：`89fc6bad0b0557c4623dd65b`；证据：`3a311ed2a8291589c7016d8c`。

源码推导：

```json
"Under the explicitly retained normal production, JSON/Serde and active Device conditions, the closed UI command field omission reaches None and the nonblank authority guard rejects before criterion use/commit."
```

适用条件：

```json
{
  "items": [
    "Normal production clarification route; options.controlPlane override is absent, literal module imports complete normally, and form prerequisites permit save.",
    "Protocol values are ordinary JSON data and the versioned native JSON/Serde provider model applies; successful delivery of that request is a condition, not an observed network execution.",
    "Actor/scope authorization, catalog/revision/source-session/baseline guards permit reaching authority, and the update is not an earlier exact receipt replay.",
    "The source product session resolves to an authorized active Device repository target. Non-Device and independent Chat paths remain counterexamples."
  ],
  "kind": "true_environment_and_model_conditions",
  "provenance": {
    "author_approved": false,
    "authority": "Astra original WWC-02 source report, conditional code judgment",
    "source_doc": "reports/astra-baseline/WINWINCODE_ANALYSIS.md#wwc-02"
  },
  "source_class": "policy-declared"
}
```

反证与范围：

```json
[
  {
    "kind": "non_device_repository",
    "relation_id": "77c0b1231e1b6559274db3aa630bd39eb49cae3bf1d3cc455b6f673bced6d1bb",
    "scope": "does not establish every non-Device save succeeds",
    "source_class": "source-derived",
    "status": "supported"
  },
  {
    "kind": "device_target_not_active_or_not_authorized",
    "relation_id": "d5c7cc195763826b9932be899f8a067641b1a29c42f190fecb30e92a3d5d6874",
    "source_class": "source-derived",
    "status": "supported"
  },
  {
    "kind": "chat_explicit_command",
    "relation_id": "5dc0d4ee3371e346349dbee6bd0047d00f77749139cb945550520f392f68c1c8",
    "source_class": "source-derived",
    "status": "supported"
  },
  {
    "kind": "chat_explicit_command",
    "relation_id": "818d39f65da046b5a4b4448f5204fe8f97ffa9c33db122141a06ba0479afd000",
    "source_class": "source-derived",
    "status": "supported"
  },
  {
    "kind": "criterion_display_is_not_wire_command",
    "relation_id": "d4e66a9a5676d080a86e7e57ce11ec22989eb6715bcb9cb804818b6d55ded120",
    "source_class": "source-derived",
    "status": "supported"
  },
  {
    "kind": "authorized_scope_required",
    "relation_id": "c6386d2f52d90830c13816ae8bee36e83631da9bb7836a0a23b1ce9862a83e34",
    "source_class": "source-derived",
    "status": "supported"
  },
  {
    "kind": "existing_exact_receipt_replays_before_authority",
    "relation_id": "ab79ced271b6723af025700f7bf2e1afad669dacdf99668d2242889ca4424f0b",
    "source_class": "source-derived",
    "status": "supported"
  },
  {
    "kind": "completed_command_confirmation_required",
    "relation_id": "178c067bd4d619f139d2713012edbee4b90ed297e292c3323268d46729fdab8b",
    "source_class": "source-derived",
    "status": "supported"
  }
]
```

必要缺口：

```json
[]
```

| 必要关系 | 结果 |
| --- | --- |
| D1 | supported |
| D2 | supported |
| D3 | supported |
| D4 | supported |
| D5 | supported |

## 主要功能链与源码边界

以下结论描述所选声明内的调用、保护和装配关系。源码顺序成立仍以该分支到达、前序操作正常完成为条件。

同一源码被这些规则选中：`wwc-report-adapter-durable-exact-turn`、`wwc-report-submission-intent-kernel-order`；它们不累计为额外功能覆盖。

### wwc-report-adapter-durable-exact-turn

类型：`guarded_call_sequence`；源码关系评估：`scoped_source_relations_supported`。

保存发现：`a69caa6dc6cf3b4f882a90e0`；证据：`7bdcbe863990b55a37f4e094`。

- `adapter_submit`：`crates/winwincode-codex/src/adapter.rs` / `<ProductionCodexAdapter as CodexCoreAdapter>.submit_turn`。

`adapter_submit` 的正常源码顺序：

- `self.run_key_for_thread(thread_id)?.to_owned / self.run_key_for_thread`，`crates/winwincode-codex/src/adapter.rs:3516`。
- `self.runs.get(&run_key).ok_or_else / self.runs.get / stage_product_prompt(&run.record.job).map_err / stage_product_prompt`，`crates/winwincode-codex/src/adapter.rs:3522`。
- `Err / conflict`，`crates/winwincode-codex/src/adapter.rs:3526`。
- `self.runs.get(&run_key).ok_or_else / self.runs.get / turn_submission_options`，`crates/winwincode-codex/src/adapter.rs:3529`。
- `submission_input_digest`，`crates/winwincode-codex/src/adapter.rs:3533`。
- `self.runs.get_mut(&run_key).ok_or_else / self.runs.get_mut / Err / conflict / Some / run.record.terminal.is_some / run.record.final_candidate_freeze.is_some / run.record.delegated_stop.is_some / run.record.batch_intent.is_some / run.record.format_repair.is_some / run.record.submission_id.clone / Err / conflict / run.record.submission_id.clone`，`crates/winwincode-codex/src/adapter.rs:3534`。
- `self.persist_run`，`crates/winwincode-codex/src/adapter.rs:3558`。
- `Ok`，`crates/winwincode-codex/src/adapter.rs:3559`。
- `self.config.submission_faults.pop_front / Some / Err / ProductionCodexError::new`，`crates/winwincode-codex/src/adapter.rs:3563`。
- `self.session_for_thread`，`crates/winwincode-codex/src/adapter.rs:3571`。
- `self
            .kernel
            .reconcile_turn_exact / submission_id.clone / goal.to_owned`，`crates/winwincode-codex/src/adapter.rs:3572`。
- `self.retain_submission_failure / Err / kernel_error`，`crates/winwincode-codex/src/adapter.rs:3581`。
- `terminal
                    .token_usage
                    .as_ref()
                    .map_or / terminal
                    .token_usage
                    .as_ref / complete_reconciled_turn / terminal.duration_ms.unwrap_or(0).max / terminal.duration_ms.unwrap_or / self.store
                    .commit_provider_final_model_calls(&run_key)
                    .map_err / self.store
                    .commit_provider_final_model_calls / self
                    .runs
                    .get(&run_key)
                    .ok_or_else(unknown_thread)?
                    .record
                    .last_activity_at
                    .clone / self
                    .runs
                    .get(&run_key)
                    .ok_or_else / self
                    .runs
                    .get / self.retain_failed_terminal / self.retain_submission_failure / Err / kernel_error`，`crates/winwincode-codex/src/adapter.rs:3585`。
- `self.runs
            .get_mut(&run_key)
            .ok_or_else / self.runs
            .get_mut`，`crates/winwincode-codex/src/adapter.rs:3623`。
- `Ok`，`crates/winwincode-codex/src/adapter.rs:3627`。

自动关系类型：`{"captured_call_step": 56, "conditional_direct_statement_order": 14, "direct_statement_call_step": 15, "ordered_source_assignment_attempt": 3, "report_source_role": 1, "result_try_normal_continuation": 15, "source_guard_and_abrupt_branch": 6}`。

分析缺口：

```json
[]
```

条件与反证声明（单列为配置范围，不冒充源码证据）：

```json
{
  "applicability": {
    "conditions": [
      "Selected definitions and raw source are authenticated in the same snapshot.",
      "Recorded source structure and conditional normal reaching are the evidence scope; target execution, all-path completion, generic runtime activation and physical side effects are not established."
    ],
    "counterexamples": [
      "Submission-intent/persist_run and exact-turn reconciliation are distinct source operations.",
      "Captured cfg test-support branches and durable/recovered state guards are preserved; no crash-consistency exercise has been performed."
    ],
    "kind": "conditional"
  },
  "descriptive_counterexamples_are_computed_evidence": false,
  "origin": "policy-declared",
  "provenance": {
    "author_approved": false,
    "authority": "independent-static-report-benchmark",
    "note": "Source locators only; the detector derives calls, guards, construction operands and normal source order. No generic target or precomputed path is declared.",
    "reviewer": "captured-source-report-expansion",
    "source_doc": "reports/astra-baseline/WINWINCODE_ANALYSIS.md"
  }
}
```

### wwc-report-chat-delivery-workrun-requests

类型：`guarded_call_sequence`；源码关系评估：`scoped_source_relations_supported`。

保存发现：`5286c33493869864db5cae8a`；证据：`4becc4c2c83ad6d40f0abb96`。

- `builder`：`apps/client/src/chat-delivery-creator.ts` / `createChatDeliveryCreator.create`。
- `entry`：`apps/client/src/chat-delivery-creator.ts` / `createChatDeliveryCreator.<object@321:9>.create`。

`builder` 的正常源码顺序：

- `clientFailure`，`apps/client/src/chat-delivery-creator.ts:168`。
- `input.title.trim`，`apps/client/src/chat-delivery-creator.ts:175`。
- `input.goal.trim`，`apps/client/src/chat-delivery-creator.ts:176`。
- `input.baseRevision.trim`，`apps/client/src/chat-delivery-creator.ts:177`。
- `Set / input.scope.map(value => value.trim()).filter / input.scope.map`，`apps/client/src/chat-delivery-creator.ts:178`。
- `Set / input.outOfScope.map(value => value.trim()).filter / input.outOfScope.map`，`apps/client/src/chat-delivery-creator.ts:179`。
- `Set / input.constraints.map(value => value.trim()).filter / input.constraints.map`，`apps/client/src/chat-delivery-creator.ts:180`。
- `input.acceptanceCriteria
      .map(value => value.trim())
      .filter / input.acceptanceCriteria
      .map`，`apps/client/src/chat-delivery-creator.ts:181`。
- `invalid`，`apps/client/src/chat-delivery-creator.ts:184`。
- `invalid`，`apps/client/src/chat-delivery-creator.ts:188`。
- `invalid`，`apps/client/src/chat-delivery-creator.ts:192`。
- `invalid`，`apps/client/src/chat-delivery-creator.ts:196`。
- `invalid`，`apps/client/src/chat-delivery-creator.ts:200`。
- `JSON.stringify / input.verificationCommand?.trim`，`apps/client/src/chat-delivery-creator.ts:207`。
- `invalid`，`apps/client/src/chat-delivery-creator.ts:218`。
- `options.nextDeliveryId / options.nextRequestId / acceptanceCriteria.map / input.verificationCommand?.trim / input.verificationCommand.trim`，`apps/client/src/chat-delivery-creator.ts:226`。
- `active?.abort`，`apps/client/src/chat-delivery-creator.ts:263`。
- `AbortController`，`apps/client/src/chat-delivery-creator.ts:264`。
- `publish`，`apps/client/src/chat-delivery-creator.ts:266`。
- `options.client.command / completedDelivery / publish / queryWorkRunAggregate / options.nextRequestId / workItemsCreateCommand / options.nextRequestId / deliveryId.replace / aggregate.contract.criteria.map / options.client.command / clientFailure / options.nextRequestId / options.client.command / clientFailure / publish / options.onCreated / publish / normalizedError`，`apps/client/src/chat-delivery-creator.ts:267`。

`entry` 的正常源码顺序：

- `create`，`apps/client/src/chat-delivery-creator.ts:331`。

自动关系类型：`{"call_result_binding_guard_source": 12, "captured_call_step": 50, "conditional_direct_statement_order": 19, "direct_statement_call_step": 21, "normal_reaching_excludes_abrupt_guard_branch": 3, "ordered_source_assignment_attempt": 6, "report_source_role": 2, "source_guard_and_abrupt_branch": 20}`。

分析缺口：

```json
[]
```

条件与反证声明（单列为配置范围，不冒充源码证据）：

```json
{
  "applicability": {
    "conditions": [
      "Selected definitions and raw source are authenticated in the same snapshot.",
      "Recorded source structure and conditional normal reaching are the evidence scope; target execution, all-path completion, generic runtime activation and physical side effects are not established."
    ],
    "counterexamples": [
      "The Chat creation path is an independent counterexample to blanket task-creation failure.",
      "Command confirmations, authorization, request identities and subsequent work-item/run failures are retained; injected client target is not determined by method name."
    ],
    "kind": "conditional"
  },
  "descriptive_counterexamples_are_computed_evidence": false,
  "origin": "policy-declared",
  "provenance": {
    "author_approved": false,
    "authority": "independent-static-report-benchmark",
    "note": "Source locators only; the detector derives calls, guards, construction operands and normal source order. No generic target or precomputed path is declared.",
    "reviewer": "captured-source-report-expansion",
    "source_doc": "reports/astra-baseline/WINWINCODE_ANALYSIS.md"
  }
}
```

### wwc-report-device-provider-deployment

类型：`deployment_provider_split`；源码关系评估：`partial_source_relations`。

保存发现：`6326ace38185675d203f5809`；证据：`09b8a912de95ed026ccc5725`。

- `boundary`：`crates/winwincode-server/src/main.rs` / `<DeviceModelBoundary as winwincode_control_plane::DurableExecutionPortDelegate>.accept`。
- `bootstrap`：`crates/winwincode-worker/src/main.rs` / `run_worker`。
- `installation`：`crates/winwincode-worker/src/lib.rs` / `WorkerMain.with_device_providers`。
- `provider`：`crates/winwincode-worker/src/device_model.rs` / `DeviceModels.open`。

自动关系类型：`{"boundary_result_source": 1, "captured_call_step": 68, "production_construction_call_source": 67, "provider_installation_assignment_source": 2, "report_source_role": 4}`。

分析缺口：

```json
[
  {
    "code": "report_source_role_graph_binding_limited",
    "declaration_binding_limits": {
      "attribute_macros_unknown": true
    },
    "location": {
      "column": 5,
      "column_base": 1,
      "column_unit": "utf8_bytes",
      "coordinate_space": "captured_text_utf8",
      "end_byte": 13509,
      "end_column": 6,
      "end_line": 347,
      "file": "crates/winwincode-server/src/main.rs",
      "grammar": "rust",
      "line": 340,
      "original_file_end_byte": 13509,
      "original_file_start_byte": 13130,
      "parse_identity": {
        "coordinate_space": "captured_text_utf8",
        "derived_text_utf8_sha256": null,
        "literal_authority": "original_saved_source_text_only",
        "original_text_utf8_sha256": "43916fbf990bb8e272b2d04cf07ee5ba955390acf8a9f968ca3731b4e245fb26",
        "position_map": "identity_utf8_bytes_and_line_columns",
        "projection_mode": "original",
        "projection_version": null,
        "raw_prefix_bytes": 0,
        "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-rust-0.24.0+cpython-3.12.14",
        "semantic_source_version": "semantic-snapshot-sources-1",
        "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
      },
      "parser_version": "tree-sitter-0.25.2+tree-sitter-rust-0.24.0+cpython-3.12.14",
      "raw_prefix_bytes": 0,
      "semantic_parse_id": "35341a0a4625dd23dca0d5dcadbeec868a809a4918d658f0be296353372a2466",
      "source_excerpt": "fn accept(\n        &mut self,\n        _context: winwincode_control_plane::DurableExecutionPortContext<'_>,\n        _message: winwincode_control_plane::DurableExecutionPortSupplement<'_>,\n    ) -> Result<Vec<ExecutionPortMessage>, winwincode_control_plane::DurableExecutionPortError>\n    {\n        Err(winwincode_control_plane::DurableExecutionPortError::UnsupportedMessage)\n    }",
      "source_excerpt_truncated": false,
      "source_hash": "43916fbf990bb8e272b2d04cf07ee5ba955390acf8a9f968ca3731b4e245fb26",
      "source_line": "    fn accept(",
      "span_hash": "7d944a347d86b109437b7240f2a86fa8144f974bc260f37f5d18ab30cd6d125d",
      "start_byte": 13130
    },
    "origin": "unresolved",
    "role": "boundary",
    "source_body_available": true,
    "source_gaps": [
      {
        "code": "graph_declaration_not_unique",
        "file": "crates/winwincode-server/src/main.rs",
        "line": 340,
        "message": "图声明不是唯一、完整的捕获函数/方法。"
      }
    ]
  },
  {
    "code": "report_source_role_graph_binding_limited",
    "declaration_binding_limits": {
      "attribute_macros_unknown": true
    },
    "location": {
      "column": 1,
      "column_base": 1,
      "column_unit": "utf8_bytes",
      "coordinate_space": "captured_text_utf8",
      "end_byte": 10828,
      "end_column": 2,
      "end_line": 262,
      "file": "crates/winwincode-worker/src/main.rs",
      "grammar": "rust",
      "line": 154,
      "original_file_end_byte": 10828,
      "original_file_start_byte": 6268,
      "parse_identity": {
        "coordinate_space": "captured_text_utf8",
        "derived_text_utf8_sha256": null,
        "literal_authority": "original_saved_source_text_only",
        "original_text_utf8_sha256": "b411e70451b7dfd76fd59cdedba9f7bab7a40b694fb47bc6299da7709b28690d",
        "position_map": "identity_utf8_bytes_and_line_columns",
        "projection_mode": "original",
        "projection_version": null,
        "raw_prefix_bytes": 0,
        "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-rust-0.24.0+cpython-3.12.14",
        "semantic_source_version": "semantic-snapshot-sources-1",
        "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
      },
      "parser_version": "tree-sitter-0.25.2+tree-sitter-rust-0.24.0+cpython-3.12.14",
      "raw_prefix_bytes": 0,
      "semantic_parse_id": "9b1b6a5da0112fe2c51a6fb79d5a27871960f56673e992fefecf2eef97a8e7fe",
      "source_excerpt": "async fn run_worker(bootstrap: WorkerBootstrap) -> Result<(), Box<dyn std::error::Error>> {\n    let WorkerBootstrap {\n        exit_after_work,\n        worker_id,\n        worker_instance_id,\n        started_at,\n        data_directory,\n        provider_directory,\n        source_directory,\n        server_origin,\n        credential_path,\n        model_route,\n    } = bootstrap;\n    let capabilities = worker_capabilities()?;\n    let execution_mode = configured_execution_mode(\"WWC_WORKER_EXECUTION_MODE\")?;\n    let observer_mode = configured_observer_mode(\"WWC_WORKER_OBSERVER_MODE\")?;\n    let observation_model = configured_observation_model(observer_mode, required)?;\n    let (port, handle) = RemoteWorkerPort::open(\n        &server_origin,\n        &fs::read(required(\"WWC_WORKER_TLS_ROOT_DER_FILE\")?)?,\n        credential_path,\n        worker_id.clone(),\n        worker_instance_id.clone(),\n        Duration::from_secs(15),\n    )?;\n    let codex = production_codex(\n        &data_directory,\n        &provider_directory,\n        model_route,\n        capabilities.clone(),\n        execution_mode,\n        observer_mode,\n    )?;\n    let validation_artifacts =\n        DurableValidationArtifactStore::open(data_directory.join(\"worker-validation-artifacts\"))?;\n    let workspaces =\n        JobWorkspaceRuntime::open(data_directory.join(\"worker-workspaces\"), &source_directory)?\n            .with_validation_artifact_port(validation_artifacts);\n    let config = WorkerConfig {\n        worker_id,\n        worker_instance_id: worker_instance_id.clone(),\n        started_at: started_at.clone(),\n        capabilities,\n    };\n    let intake_log = data_directory.join(\"codex-runtime\").join(\"model-intake.log\");\n    let mut worker = WorkerMain::new(config, port, codex, workspaces)\n        .with_device_providers(&provider_directory)?\n        .with_observer_mode(observer_mode)\n        .with_registration_request_namespace(&worker_instance_id, &started_at)\n        .with_model_intake_log(&intake_log);\n    if let Some(observation_model) = observation_model {\n        worker = worker.with_observation_model(observation_model);\n    }\n\n    while worker.lifecycle() == WorkerLifecycleState::Booting\n        || worker.lifecycle() == WorkerLifecycleState::Registering\n    {\n        match Box::pin(worker.start(started_at.clone())).await {\n            Ok(()) => {\n                Box::pin(drain_controls(&mut worker, &handle)).await?;\n            }\n            Err(error) => {\n                // Secret-safe lifecycle category only: a Device StrongFlow\n                // Worker that silently retries registration forever is\n                // indistinguishable from a hung process in production logs.\n                eprintln!(\n                    \"winwincode-worker: registration/start retry category={:?} reason={} lifecycle={:?}\",\n                    error.code,\n                    error.reason,\n                    worker.lifecycle()\n                );\n            }\n        }\n        if worker.lifecycle() != WorkerLifecycleState::Active {\n            tokio::time::sleep(Duration::from_millis(250)).await;\n        }\n    }\n\n    let mut heartbeat = tokio::time::interval(Duration::from_secs(1));\n    let mut drive = tokio::time::interval(Duration::from_millis(25));\n    loop {\n        tokio::select! {\n            _ = tokio::signal::ctrl_c() => break,\n            _ = heartbeat.tick() => {\n                let now = now_instant()?;\n                if Box::pin(worker.heartbeat(now.clone())).await.is_ok() {\n                    Box::pin(drain_controls(&mut worker, &handle)).await?;\n                }\n            }\n            _ = drive.tick() => {\n                let now = now_instant()?;\n                Box::pin(drain_controls(&mut worker, &handle)).await?;\n                // Retry pending Worker→Server evidence every drive tick so a\n                // Server restart / Connection-refused window cannot strand\n                // runtime.event / artifact.chunk / JobOutcome in the outbox.\n                if worker.lifecycle() == WorkerLifecycleState::Active\n                    && Box::pin(worker.flush_",
      "source_excerpt_truncated": true,
      "source_hash": "b411e70451b7dfd76fd59cdedba9f7bab7a40b694fb47bc6299da7709b28690d",
      "source_line": "async fn run_worker(bootstrap: WorkerBootstrap) -> Result<(), Box<dyn std::error::Error>> {",
      "span_hash": "ab106e71bf791a0283412d398b3b36bdc13d453808b0b2a0c49ccb285c8b5982",
      "start_byte": 6268
    },
    "origin": "unresolved",
    "role": "bootstrap",
    "source_body_available": true,
    "source_gaps": [
      {
        "code": "graph_declaration_not_unique",
        "file": "crates/winwincode-worker/src/main.rs",
        "line": 154,
        "message": "图声明不是唯一、完整的捕获函数/方法。"
      }
    ]
  },
  {
    "code": "deployment_candidate_chain_not_global_dispatch_or_credential_availability",
    "full_provider_flow_proven": false,
    "origin": "unresolved",
    "source_only": true
  }
]
```

条件与反证声明（单列为配置范围，不冒充源码证据）：

```json
{
  "applicability": {
    "conditions": [
      "Selected declarations and saved source are authenticated in the same snapshot.",
      "Relations describe captured source structure and selected normal reaching, not target execution, completion or whole-repository correctness."
    ],
    "counterexamples": [
      "One server boundary result does not imply an absent provider in a separate Worker deployment.",
      "This does not prove credentials are configured, every provider is usable or generic dispatch has one global target."
    ],
    "kind": "conditional"
  },
  "descriptive_counterexamples_are_computed_evidence": false,
  "origin": "policy-declared",
  "provenance": {
    "author_approved": false,
    "authority": "independent-static-report-benchmark",
    "note": "Locator-only source selection; original report wording is not consumed by the detector.",
    "reviewer": "source-derived-report-chains",
    "source_doc": "reports/astra-baseline/WINWINCODE_ANALYSIS.md"
  }
}
```

### wwc-report-kernel-create-session-interface

类型：`guarded_call_sequence`；源码关系评估：`scoped_source_relations_supported`。

保存发现：`2476c0ba1c86c52e734c626b`；证据：`a8e64f975a826512eb66659e`。

- `kernel_create`：`crates/kernel/src/lib.rs` / `Kernel.create_session`。

`kernel_create` 的正常源码顺序：

- `Self::guard / self.runtime / Self::session_config / runtime
                .manager
                .start_thread(StartThreadOptions::new(config.clone()))
                .await
                .map_err / runtime
                .manager
                .start_thread / StartThreadOptions::new / config.clone / Box::pin / self.register_session`，`crates/kernel/src/lib.rs:1221`。

自动关系类型：`{"captured_call_step": 9, "conditional_direct_statement_order": 3, "deferred_source_region_sequence": 1, "direct_statement_call_step": 5, "report_source_role": 1, "result_try_normal_continuation": 6}`。

分析缺口：

```json
[]
```

条件与反证声明（单列为配置范围，不冒充源码证据）：

```json
{
  "applicability": {
    "conditions": [
      "Selected definitions and raw source are authenticated in the same snapshot.",
      "Recorded source structure and conditional normal reaching are the evidence scope; target execution, all-path completion, generic runtime activation and physical side effects are not established."
    ],
    "counterexamples": [
      "The async operand to Self::guard and its runtime manager calls are source evidence; the current pattern may not close future activation/inner statement order."
    ],
    "kind": "conditional"
  },
  "descriptive_counterexamples_are_computed_evidence": false,
  "origin": "policy-declared",
  "provenance": {
    "author_approved": false,
    "authority": "independent-static-report-benchmark",
    "note": "Source locators only; the detector derives calls, guards, construction operands and normal source order. No generic target or precomputed path is declared.",
    "reviewer": "captured-source-report-expansion",
    "source_doc": "reports/astra-baseline/WINWINCODE_ANALYSIS.md"
  }
}
```

### wwc-report-kernel-reconcile-exact-interface

类型：`guarded_call_sequence`；源码关系评估：`scoped_source_relations_supported`。

保存发现：`eb4241aadc167972eb15203c`；证据：`e5f427d3e22c0abe60aab073`。

- `kernel_reconcile`：`crates/kernel/src/lib.rs` / `Kernel.reconcile_turn_exact`。

`kernel_reconcile` 的正常源码顺序：

- `Self::guard / turn_id.trim().is_empty / turn_id.trim / text.trim().is_empty / text.trim / Err / KernelFailure::new / self.runtime / self.session / self.enforce_private_permissions / session
                .thread
                .inspect_durable_turn(&turn_id)
                .await
                .map_err / session
                .thread
                .inspect_durable_turn / Ok / ExactTurnReconciliation::Completed / Ok / ExactTurnReconciliation::Failed / if recovered {
                        session
                            .thread
                            .recover_turn_if_idle(RecoverTurnRequest {
                                turn_id,
                                thread_settings: ThreadSettingsOverrides::default(),
                                trace: None,
                                submit_change_batch: options.submit_change_batch,
                            })
                            .await
                    } else {
                        session
                            .thread
                            .start_turn_with_id_if_idle(user_text_request(text, &options), turn_id)
                            .await
                    }
                    .map_err / session
                            .thread
                            .recover_turn_if_idle / ThreadSettingsOverrides::default / session
                            .thread
                            .start_turn_with_id_if_idle / user_text_request / Ok / exact_turn_submission / self.enforce_private_permissions`，`crates/kernel/src/lib.rs:1376`。

自动关系类型：`{"captured_call_step": 24, "conditional_direct_statement_order": 6, "deferred_source_region_sequence": 1, "direct_statement_call_step": 8, "report_source_role": 1, "result_try_normal_continuation": 12, "source_guard_and_abrupt_branch": 4}`。

分析缺口：

```json
[]
```

条件与反证声明（单列为配置范围，不冒充源码证据）：

```json
{
  "applicability": {
    "conditions": [
      "Selected definitions and raw source are authenticated in the same snapshot.",
      "Recorded source structure and conditional normal reaching are the evidence scope; target execution, all-path completion, generic runtime activation and physical side effects are not established."
    ],
    "counterexamples": [
      "Completed/Failed/Absent/InProgress and recover/start-if-idle branches remain distinct source conditions, not observed history facts."
    ],
    "kind": "conditional"
  },
  "descriptive_counterexamples_are_computed_evidence": false,
  "origin": "policy-declared",
  "provenance": {
    "author_approved": false,
    "authority": "independent-static-report-benchmark",
    "note": "Source locators only; the detector derives calls, guards, construction operands and normal source order. No generic target or precomputed path is declared.",
    "reviewer": "captured-source-report-expansion",
    "source_doc": "reports/astra-baseline/WINWINCODE_ANALYSIS.md"
  }
}
```

### wwc-report-kernel-submit-turn-interface

类型：`guarded_call_sequence`；源码关系评估：`scoped_source_relations_supported`。

保存发现：`c4c6a41c714f4ac6670821b9`；证据：`1743f4e539c0d17068c2785a`。

- `kernel_submit`：`crates/kernel/src/lib.rs` / `Kernel.submit_turn`。

`kernel_submit` 的正常源码顺序：

- `Self::guard / text.trim().is_empty / text.trim / Err / KernelFailure::new / self.runtime / self.session / self.enforce_private_permissions / session
                .thread
                .start_or_steer_turn(user_text_request(text, &options))
                .await
                .map_err / session
                .thread
                .start_or_steer_turn / user_text_request / self.enforce_private_permissions / Ok / submission_info`，`crates/kernel/src/lib.rs:1339`。

自动关系类型：`{"captured_call_step": 14, "conditional_direct_statement_order": 6, "deferred_source_region_sequence": 1, "direct_statement_call_step": 8, "report_source_role": 1, "result_try_normal_continuation": 10, "source_guard_and_abrupt_branch": 2}`。

分析缺口：

```json
[]
```

条件与反证声明（单列为配置范围，不冒充源码证据）：

```json
{
  "applicability": {
    "conditions": [
      "Selected definitions and raw source are authenticated in the same snapshot.",
      "Recorded source structure and conditional normal reaching are the evidence scope; target execution, all-path completion, generic runtime activation and physical side effects are not established."
    ],
    "counterexamples": [
      "Ordinary start-or-steer is not exact-turn reconciliation; the async helper boundary is retained."
    ],
    "kind": "conditional"
  },
  "descriptive_counterexamples_are_computed_evidence": false,
  "origin": "policy-declared",
  "provenance": {
    "author_approved": false,
    "authority": "independent-static-report-benchmark",
    "note": "Source locators only; the detector derives calls, guards, construction operands and normal source order. No generic target or precomputed path is declared.",
    "reviewer": "captured-source-report-expansion",
    "source_doc": "reports/astra-baseline/WINWINCODE_ANALYSIS.md"
  }
}
```

### wwc-report-production-adapter-embedded-kernel

类型：`guarded_call_sequence`；源码关系评估：`scoped_source_relations_supported`。

保存发现：`bd05f66a1f61c19a19ca9800`；证据：`ff7fe3d0f3133e2b4c683fb5`。

- `adapter_open`：`crates/winwincode-codex/src/adapter.rs` / `ProductionCodexAdapter.open`。
- `kernel_constructor`：`crates/kernel/src/lib.rs` / `Kernel.new`。

`adapter_open` 的正常源码顺序：

- `ensure_private_directory(&config.data_directory).map_err / ensure_private_directory`，`crates/winwincode-codex/src/adapter.rs:418`。
- `ensure_private_directory(&config.kernel_home).map_err / ensure_private_directory`，`crates/winwincode-codex/src/adapter.rs:419`。
- `seal_helper / Some / config.helper_bytes.as_ref`，`crates/winwincode-codex/src/adapter.rs:420`。
- `WorkerCapabilityCatalog::discover(
            &config.registered_capabilities,
            config.discovered_capabilities.clone(),
        )
        .map_err / WorkerCapabilityCatalog::discover / config.discovered_capabilities.clone`，`crates/winwincode-codex/src/adapter.rs:426`。
- `AdapterStore::open(&config.data_directory).map_err / AdapterStore::open`，`crates/winwincode-codex/src/adapter.rs:431`。
- `migrate_stored_run_role_policies_v1_to_v2`，`crates/winwincode-codex/src/adapter.rs:432`。
- `ExecutionOutbox::open(store.clone()).map_err / ExecutionOutbox::open / store.clone`，`crates/winwincode-codex/src/adapter.rs:433`。
- `CandidateArtifactOutbox::open(store.clone()).map_err / CandidateArtifactOutbox::open / store.clone`，`crates/winwincode-codex/src/adapter.rs:434`。
- `DiagnosticArtifactOutbox::open(store.clone()).map_err / DiagnosticArtifactOutbox::open / store.clone`，`crates/winwincode-codex/src/adapter.rs:436`。
- `SharedAuthoritySource::default`，`crates/winwincode-codex/src/adapter.rs:438`。
- `Arc::new / ExecutionPortModelBridge::new / store.clone / outbox.clone / config.gateway_route.clone / config.provider.clone`，`crates/winwincode-codex/src/adapter.rs:439`。
- `Arc::new / ExecutionPortActionGate::open(
                &config.data_directory,
                capability_catalog.clone(),
                config.execution_envelope.clone(),
                config.action_signing_key.clone(),
            )
            .map_err / ExecutionPortActionGate::open / capability_catalog.clone / config.execution_envelope.clone / config.action_signing_key.clone`，`crates/winwincode-codex/src/adapter.rs:446`。
- `bridge
            .attach_action_gate(action_gate.clone())
            .map_err / bridge
            .attach_action_gate / action_gate.clone`，`crates/winwincode-codex/src/adapter.rs:455`。
- `Arc::new / Kernel::new(
                KernelOptions::new(config.kernel_home.clone(), config.helper_executable.clone()),
                bridge.model_port(),
                action_gate.clone(),
            )
            .map_err / Kernel::new / KernelOptions::new / config.kernel_home.clone / config.helper_executable.clone / bridge.model_port / action_gate.clone`，`crates/winwincode-codex/src/adapter.rs:458`。
- `Ok / WorkRunRuntimeProjector::new / WorkerRuntimeTraceOutbox::new / HashMap::new / HashMap::new`，`crates/winwincode-codex/src/adapter.rs:471`。

`kernel_constructor` 的正常源码顺序：

- `options.home.is_absolute / Err / KernelFailure::new`，`crates/kernel/src/lib.rs:830`。
- `options.helper_executable.is_absolute / Err / KernelFailure::new`，`crates/kernel/src/lib.rs:836`。
- `std::fs::symlink_metadata(&options.helper_executable).map_err / std::fs::symlink_metadata`，`crates/kernel/src/lib.rs:845`。
- `helper_metadata.file_type().is_symlink / helper_metadata.file_type / helper_metadata.is_file / Err / KernelFailure::new`，`crates/kernel/src/lib.rs:855`。
- `helper_metadata.permissions().mode / helper_metadata.permissions / Err / KernelFailure::new`，`crates/kernel/src/lib.rs:865`。
- `options
            .event_capacity
            .clamp`，`crates/kernel/src/lib.rs:874`。
- `options.shutdown_timeout.is_zero / Err / KernelFailure::new`，`crates/kernel/src/lib.rs:877`。
- `std::fs::create_dir_all(&options.home).map_err / std::fs::create_dir_all`，`crates/kernel/src/lib.rs:883`。
- `restrict_private_tree(&options.home).map_err / restrict_private_tree`，`crates/kernel/src/lib.rs:889`。
- `Ok / Arc::new / Mutex::new / AtomicBool::new`，`crates/kernel/src/lib.rs:895`。

自动关系类型：`{"captured_call_step": 80, "conditional_direct_statement_order": 23, "direct_statement_call_step": 25, "ordered_source_assignment_attempt": 2, "report_source_role": 2, "result_try_normal_continuation": 15, "source_guard_and_abrupt_branch": 5}`。

分析缺口：

```json
[]
```

条件与反证声明（单列为配置范围，不冒充源码证据）：

```json
{
  "applicability": {
    "conditions": [
      "Selected definitions and raw source are authenticated in the same snapshot.",
      "Recorded source structure and conditional normal reaching are the evidence scope; target execution, all-path completion, generic runtime activation and physical side effects are not established."
    ],
    "counterexamples": [
      "Directory/helper/store/outbox/action-gate and Kernel construction can fail; source presence does not certify a running deployment.",
      "Installed Codex CLI execution is not part of this captured production constructor chain."
    ],
    "kind": "conditional"
  },
  "descriptive_counterexamples_are_computed_evidence": false,
  "origin": "policy-declared",
  "provenance": {
    "author_approved": false,
    "authority": "independent-static-report-benchmark",
    "note": "Source locators only; the detector derives calls, guards, construction operands and normal source order. No generic target or precomputed path is declared.",
    "reviewer": "captured-source-report-expansion",
    "source_doc": "reports/astra-baseline/WINWINCODE_ANALYSIS.md"
  }
}
```

### wwc-report-submission-intent-kernel-order

类型：`guarded_call_sequence`；源码关系评估：`scoped_source_relations_supported`。

保存发现：`a6f2eb12778d309024deb758`；证据：`792d494a7d4547952c04d4ab`。

- `submission`：`crates/winwincode-codex/src/adapter.rs` / `<ProductionCodexAdapter as CodexCoreAdapter>.submit_turn`。

`submission` 的正常源码顺序：

- `self.run_key_for_thread(thread_id)?.to_owned / self.run_key_for_thread`，`crates/winwincode-codex/src/adapter.rs:3516`。
- `self.runs.get(&run_key).ok_or_else / self.runs.get / stage_product_prompt(&run.record.job).map_err / stage_product_prompt`，`crates/winwincode-codex/src/adapter.rs:3522`。
- `Err / conflict`，`crates/winwincode-codex/src/adapter.rs:3526`。
- `self.runs.get(&run_key).ok_or_else / self.runs.get / turn_submission_options`，`crates/winwincode-codex/src/adapter.rs:3529`。
- `submission_input_digest`，`crates/winwincode-codex/src/adapter.rs:3533`。
- `self.runs.get_mut(&run_key).ok_or_else / self.runs.get_mut / Err / conflict / Some / run.record.terminal.is_some / run.record.final_candidate_freeze.is_some / run.record.delegated_stop.is_some / run.record.batch_intent.is_some / run.record.format_repair.is_some / run.record.submission_id.clone / Err / conflict / run.record.submission_id.clone`，`crates/winwincode-codex/src/adapter.rs:3534`。
- `self.persist_run`，`crates/winwincode-codex/src/adapter.rs:3558`。
- `Ok`，`crates/winwincode-codex/src/adapter.rs:3559`。
- `self.config.submission_faults.pop_front / Some / Err / ProductionCodexError::new`，`crates/winwincode-codex/src/adapter.rs:3563`。
- `self.session_for_thread`，`crates/winwincode-codex/src/adapter.rs:3571`。
- `self
            .kernel
            .reconcile_turn_exact / submission_id.clone / goal.to_owned`，`crates/winwincode-codex/src/adapter.rs:3572`。
- `self.retain_submission_failure / Err / kernel_error`，`crates/winwincode-codex/src/adapter.rs:3581`。
- `terminal
                    .token_usage
                    .as_ref()
                    .map_or / terminal
                    .token_usage
                    .as_ref / complete_reconciled_turn / terminal.duration_ms.unwrap_or(0).max / terminal.duration_ms.unwrap_or / self.store
                    .commit_provider_final_model_calls(&run_key)
                    .map_err / self.store
                    .commit_provider_final_model_calls / self
                    .runs
                    .get(&run_key)
                    .ok_or_else(unknown_thread)?
                    .record
                    .last_activity_at
                    .clone / self
                    .runs
                    .get(&run_key)
                    .ok_or_else / self
                    .runs
                    .get / self.retain_failed_terminal / self.retain_submission_failure / Err / kernel_error`，`crates/winwincode-codex/src/adapter.rs:3585`。
- `self.runs
            .get_mut(&run_key)
            .ok_or_else / self.runs
            .get_mut`，`crates/winwincode-codex/src/adapter.rs:3623`。
- `Ok`，`crates/winwincode-codex/src/adapter.rs:3627`。

自动关系类型：`{"captured_call_step": 56, "conditional_direct_statement_order": 14, "direct_statement_call_step": 15, "ordered_source_assignment_attempt": 3, "report_source_role": 1, "result_try_normal_continuation": 15, "source_guard_and_abrupt_branch": 6}`。

分析缺口：

```json
[]
```

条件与反证声明（单列为配置范围，不冒充源码证据）：

```json
{
  "applicability": {
    "conditions": [
      "Selected declarations and saved source are authenticated in the same snapshot.",
      "Relations describe captured source structure and selected normal reaching, not target execution, completion or whole-repository correctness."
    ],
    "counterexamples": [
      "Settled and cfg-controlled fault branches can return before the exact Kernel interface.",
      "Source assignment/persist order does not verify durable crash consistency or Kernel completion."
    ],
    "kind": "conditional"
  },
  "descriptive_counterexamples_are_computed_evidence": false,
  "origin": "policy-declared",
  "provenance": {
    "author_approved": false,
    "authority": "independent-static-report-benchmark",
    "note": "Locator-only source selection; original report wording is not consumed by the detector.",
    "reviewer": "source-derived-report-chains",
    "source_doc": "reports/astra-baseline/WINWINCODE_ANALYSIS.md"
  }
}
```

### wwc-report-worker-bootstrap-entries

类型：`guarded_call_sequence`；源码关系评估：`partial_source_relations`。

保存发现：`d234bfcfd8c964ba2d0ec7bd`；证据：`32cfa45a045584054f5b9a10`。

- `entry`：`crates/winwincode-worker/src/main.rs` / `main`。
- `remote`：`crates/winwincode-worker/src/main.rs` / `run_remote`。
- `managed`：`crates/winwincode-worker/src/main.rs` / `run_managed`。

`entry` 的正常源码顺序：

- `env::args().skip / env::args`，`crates/winwincode-worker/src/main.rs:35`。
- `args.next().as_deref / args.next / print_identity / args.next().is_none / args.next / run_worker_process / run_remote / args.next / args.next().is_none / args.next / run_worker_process / run_managed / usage_error / usage_error`，`crates/winwincode-worker/src/main.rs:36`。

`managed` 的正常源码顺序：

- `ManagedSessionConfig::read / std::path::Path::new`，`crates/winwincode-worker/src/main.rs:119`。
- `WorkerSessionCredential::load`，`crates/winwincode-worker/src/main.rs:120`。
- `Box::pin / run_worker / config.worker_id.clone / config.worker_instance_id.clone / now_instant / config.data_directory.clone / config.provider_directory.clone / config.source_directory.clone / config.server_origin.clone / credential.path().to_path_buf / credential.path / config
            .model_route
            .clone()
            .unwrap_or_else / config
            .model_route
            .clone`，`crates/winwincode-worker/src/main.rs:133`。

`remote` 的正常源码顺序：

- `WorkerId / required / WorkerInstanceId / required / env::var("WWC_WORKER_STARTED_AT").map_or / env::var / now_instant / PathBuf::from / required / PathBuf::from / required / PathBuf::from / required / required / PathBuf::from / required / default_model_route`，`crates/winwincode-worker/src/main.rs:98`。
- `Box::pin / run_worker`，`crates/winwincode-worker/src/main.rs:110`。

自动关系类型：`{"captured_call_step": 51, "conditional_direct_statement_order": 4, "direct_statement_call_step": 7, "report_source_role": 3, "result_try_normal_continuation": 11}`。

分析缺口：

```json
[
  {
    "code": "report_source_role_graph_binding_limited",
    "declaration_binding_limits": {
      "attribute_macros_unknown": true
    },
    "location": {
      "column": 1,
      "column_base": 1,
      "column_unit": "utf8_bytes",
      "coordinate_space": "captured_text_utf8",
      "end_byte": 1970,
      "end_column": 2,
      "end_line": 50,
      "file": "crates/winwincode-worker/src/main.rs",
      "grammar": "rust",
      "line": 34,
      "original_file_end_byte": 1970,
      "original_file_start_byte": 1352,
      "parse_identity": {
        "coordinate_space": "captured_text_utf8",
        "derived_text_utf8_sha256": null,
        "literal_authority": "original_saved_source_text_only",
        "original_text_utf8_sha256": "b411e70451b7dfd76fd59cdedba9f7bab7a40b694fb47bc6299da7709b28690d",
        "position_map": "identity_utf8_bytes_and_line_columns",
        "projection_mode": "original",
        "projection_version": null,
        "raw_prefix_bytes": 0,
        "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-rust-0.24.0+cpython-3.12.14",
        "semantic_source_version": "semantic-snapshot-sources-1",
        "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
      },
      "parser_version": "tree-sitter-0.25.2+tree-sitter-rust-0.24.0+cpython-3.12.14",
      "raw_prefix_bytes": 0,
      "semantic_parse_id": "9b1b6a5da0112fe2c51a6fb79d5a27871960f56673e992fefecf2eef97a8e7fe",
      "source_excerpt": "fn main() {\n    let mut args = env::args().skip(1);\n    match args.next().as_deref() {\n        Some(\"--version\") => println!(\"winwincode-worker {}\", env!(\"CARGO_PKG_VERSION\")),\n        Some(\"--check\") | None => print_identity(),\n        Some(\"--remote\") if args.next().is_none() => {\n            run_worker_process(run_remote());\n        }\n        Some(\"--managed-session\") => match args.next() {\n            Some(config_path) if args.next().is_none() => {\n                run_worker_process(run_managed(&config_path));\n            }\n            _ => usage_error(),\n        },\n        Some(_) => usage_error(),\n    }\n}",
      "source_excerpt_truncated": false,
      "source_hash": "b411e70451b7dfd76fd59cdedba9f7bab7a40b694fb47bc6299da7709b28690d",
      "source_line": "fn main() {",
      "span_hash": "b46fbedf51136152dafe28f5b7614bd17f17598b7cf7bfba6adc99cd7ed65a4c",
      "start_byte": 1352
    },
    "origin": "unresolved",
    "role": "entry",
    "source_body_available": true,
    "source_gaps": [
      {
        "code": "graph_declaration_not_unique",
        "file": "crates/winwincode-worker/src/main.rs",
        "line": 34,
        "message": "图声明不是唯一、完整的捕获函数/方法。"
      }
    ]
  },
  {
    "code": "report_source_role_graph_binding_limited",
    "declaration_binding_limits": {
      "attribute_macros_unknown": true
    },
    "location": {
      "column": 1,
      "column_base": 1,
      "column_unit": "utf8_bytes",
      "coordinate_space": "captured_text_utf8",
      "end_byte": 4295,
      "end_column": 2,
      "end_line": 111,
      "file": "crates/winwincode-worker/src/main.rs",
      "grammar": "rust",
      "line": 97,
      "original_file_end_byte": 4295,
      "original_file_start_byte": 3451,
      "parse_identity": {
        "coordinate_space": "captured_text_utf8",
        "derived_text_utf8_sha256": null,
        "literal_authority": "original_saved_source_text_only",
        "original_text_utf8_sha256": "b411e70451b7dfd76fd59cdedba9f7bab7a40b694fb47bc6299da7709b28690d",
        "position_map": "identity_utf8_bytes_and_line_columns",
        "projection_mode": "original",
        "projection_version": null,
        "raw_prefix_bytes": 0,
        "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-rust-0.24.0+cpython-3.12.14",
        "semantic_source_version": "semantic-snapshot-sources-1",
        "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
      },
      "parser_version": "tree-sitter-0.25.2+tree-sitter-rust-0.24.0+cpython-3.12.14",
      "raw_prefix_bytes": 0,
      "semantic_parse_id": "9b1b6a5da0112fe2c51a6fb79d5a27871960f56673e992fefecf2eef97a8e7fe",
      "source_excerpt": "async fn run_remote() -> Result<(), Box<dyn std::error::Error>> {\n    let bootstrap = WorkerBootstrap {\n        exit_after_work: false,\n        worker_id: WorkerId(required(\"WWC_WORKER_ID\")?),\n        worker_instance_id: WorkerInstanceId(required(\"WWC_WORKER_INSTANCE_ID\")?),\n        started_at: env::var(\"WWC_WORKER_STARTED_AT\").map_or(now_instant()?, Instant),\n        data_directory: PathBuf::from(required(\"WWC_WORKER_DATA_DIRECTORY\")?),\n        provider_directory: PathBuf::from(required(\"WWC_DEVICE_PROVIDER_DIRECTORY\")?),\n        source_directory: PathBuf::from(required(\"WWC_WORKER_SOURCE_ROOT\")?),\n        server_origin: required(\"WWC_WORKER_SERVER_ORIGIN\")?,\n        credential_path: PathBuf::from(required(\"WWC_WORKER_CREDENTIAL_FILE\")?),\n        model_route: default_model_route(),\n    };\n    Box::pin(run_worker(bootstrap)).await\n}",
      "source_excerpt_truncated": false,
      "source_hash": "b411e70451b7dfd76fd59cdedba9f7bab7a40b694fb47bc6299da7709b28690d",
      "source_line": "async fn run_remote() -> Result<(), Box<dyn std::error::Error>> {",
      "span_hash": "c312bb11fbf5c818b667fb722ee53d785f571bbde7e79940b84c773ebd9472ec",
      "start_byte": 3451
    },
    "origin": "unresolved",
    "role": "remote",
    "source_body_available": true,
    "source_gaps": [
      {
        "code": "graph_declaration_not_unique",
        "file": "crates/winwincode-worker/src/main.rs",
        "line": 97,
        "message": "图声明不是唯一、完整的捕获函数/方法。"
      }
    ]
  },
  {
    "code": "report_source_role_graph_binding_limited",
    "declaration_binding_limits": {
      "attribute_macros_unknown": true
    },
    "location": {
      "column": 1,
      "column_base": 1,
      "column_unit": "utf8_bytes",
      "coordinate_space": "captured_text_utf8",
      "end_byte": 6055,
      "end_column": 2,
      "end_line": 149,
      "file": "crates/winwincode-worker/src/main.rs",
      "grammar": "rust",
      "line": 118,
      "original_file_end_byte": 6055,
      "original_file_start_byte": 4636,
      "parse_identity": {
        "coordinate_space": "captured_text_utf8",
        "derived_text_utf8_sha256": null,
        "literal_authority": "original_saved_source_text_only",
        "original_text_utf8_sha256": "b411e70451b7dfd76fd59cdedba9f7bab7a40b694fb47bc6299da7709b28690d",
        "position_map": "identity_utf8_bytes_and_line_columns",
        "projection_mode": "original",
        "projection_version": null,
        "raw_prefix_bytes": 0,
        "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-rust-0.24.0+cpython-3.12.14",
        "semantic_source_version": "semantic-snapshot-sources-1",
        "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
      },
      "parser_version": "tree-sitter-0.25.2+tree-sitter-rust-0.24.0+cpython-3.12.14",
      "raw_prefix_bytes": 0,
      "semantic_parse_id": "9b1b6a5da0112fe2c51a6fb79d5a27871960f56673e992fefecf2eef97a8e7fe",
      "source_excerpt": "async fn run_managed(config_path: &str) -> Result<(), Box<dyn std::error::Error>> {\n    let config = ManagedSessionConfig::read(std::path::Path::new(config_path))?;\n    let credential = WorkerSessionCredential::load(&config.worker_credential_path)?;\n    eprintln!(\n        \"winwincode-worker: managed session {} for worker {} instance {} under lease {} with fencing token {} on {} (client {} instance {}); worker session credential digest {}\",\n        config.worker_session_id.0,\n        config.worker_id.0,\n        config.worker_instance_id.0,\n        config.occupancy_lease_id.0,\n        config.occupancy_fencing_token,\n        config.repository_binding_id.0,\n        config.client_node_id.0,\n        config.client_instance_id.0,\n        credential.digest().0,\n    );\n    Box::pin(run_worker(WorkerBootstrap {\n        exit_after_work: true,\n        worker_id: config.worker_id.clone(),\n        worker_instance_id: config.worker_instance_id.clone(),\n        started_at: now_instant()?,\n        data_directory: config.data_directory.clone(),\n        provider_directory: config.provider_directory.clone(),\n        source_directory: config.source_directory.clone(),\n        server_origin: config.server_origin.clone(),\n        credential_path: credential.path().to_path_buf(),\n        model_route: config\n            .model_route\n            .clone()\n            .unwrap_or_else(default_model_route),\n    }))\n    .await\n}",
      "source_excerpt_truncated": false,
      "source_hash": "b411e70451b7dfd76fd59cdedba9f7bab7a40b694fb47bc6299da7709b28690d",
      "source_line": "async fn run_managed(config_path: &str) -> Result<(), Box<dyn std::error::Error>> {",
      "span_hash": "6d80bf35a9aa9f813aeb2156617f055c780dd04bd306d0c83218ed1a704eb4f1",
      "start_byte": 4636
    },
    "origin": "unresolved",
    "role": "managed",
    "source_body_available": true,
    "source_gaps": [
      {
        "code": "graph_declaration_not_unique",
        "file": "crates/winwincode-worker/src/main.rs",
        "line": 118,
        "message": "图声明不是唯一、完整的捕获函数/方法。"
      }
    ]
  }
]
```

条件与反证声明（单列为配置范围，不冒充源码证据）：

```json
{
  "applicability": {
    "conditions": [
      "Selected definitions and raw source are authenticated in the same snapshot.",
      "Recorded source structure and conditional normal reaching are the evidence scope; target execution, all-path completion, generic runtime activation and physical side effects are not established."
    ],
    "counterexamples": [
      "The remote and managed-session command branches remain separate source-selected entry conditions."
    ],
    "kind": "conditional"
  },
  "descriptive_counterexamples_are_computed_evidence": false,
  "origin": "policy-declared",
  "provenance": {
    "author_approved": false,
    "authority": "independent-static-report-benchmark",
    "note": "Source locators only; the detector derives calls, guards, construction operands and normal source order. No generic target or precomputed path is declared.",
    "reviewer": "captured-source-report-expansion",
    "source_doc": "reports/astra-baseline/WINWINCODE_ANALYSIS.md"
  }
}
```

### wwc-report-worker-production-construction

类型：`guarded_call_sequence`；源码关系评估：`partial_source_relations`。

保存发现：`f566fd359f7b0d297f9b6d40`；证据：`a143612edb49ee3dbb90ff42`。

- `shared_loop`：`crates/winwincode-worker/src/main.rs` / `run_worker`。
- `adapter_factory`：`crates/winwincode-worker/src/main.rs` / `production_codex`。
- `worker_constructor`：`crates/winwincode-worker/src/lib.rs` / `WorkerMain.new`。

`adapter_factory` 的正常源码顺序：

- `HelperReleaseManifest::from_file / PathBuf::from / required`，`crates/winwincode-worker/src/main.rs:323`。
- `winwincode_provider::DeviceProviderStore::open`，`crates/winwincode-worker/src/main.rs:326`。
- `store.snapshot`，`crates/winwincode-worker/src/main.rs:327`。
- `store.restore_extensions / data_directory.join`，`crates/winwincode-worker/src/main.rs:328`。
- `Vec::new`，`crates/winwincode-worker/src/main.rs:329`。
- `discovered_capabilities.push / winwincode_execution_port::capability_adapter::CapabilityDescriptor::mcp / server.digest.trim_start_matches`，`crates/winwincode-worker/src/main.rs:330`。
- `snapshot
        .providers
        .iter()
        .find(|provider| provider.config.enabled && provider.credential_configured)
        .ok_or / snapshot
        .providers
        .iter()
        .find / snapshot
        .providers
        .iter`，`crates/winwincode-worker/src/main.rs:343`。
- `env::var("WWC_WORKER_MODEL_PROVIDER_ID")
        .unwrap_or_else / env::var`，`crates/winwincode-worker/src/main.rs:348`。
- `env::var("WWC_WORKER_MODEL_ID")
        .unwrap_or_else / env::var`，`crates/winwincode-worker/src/main.rs:350`。
- `data_directory.join / PathBuf::from / required / ActionEnforcementSigningKey::from_bytes / parse_hex_key / required / Sha256Digest / required`，`crates/winwincode-worker/src/main.rs:352`。
- `Ok / ProductionCodexAdapter::open(ProductionCodexConfig::try_new(options)?)?
            .with_device_extensions / ProductionCodexAdapter::open / ProductionCodexConfig::try_new / provider_directory.to_path_buf`，`crates/winwincode-worker/src/main.rs:371`。

`shared_loop` 的正常源码顺序：

- `worker_capabilities`，`crates/winwincode-worker/src/main.rs:167`。
- `configured_execution_mode`，`crates/winwincode-worker/src/main.rs:168`。
- `configured_observer_mode`，`crates/winwincode-worker/src/main.rs:169`。
- `configured_observation_model`，`crates/winwincode-worker/src/main.rs:170`。
- `RemoteWorkerPort::open / fs::read / required / worker_id.clone / worker_instance_id.clone / Duration::from_secs`，`crates/winwincode-worker/src/main.rs:171`。
- `production_codex / capabilities.clone`，`crates/winwincode-worker/src/main.rs:179`。
- `DurableValidationArtifactStore::open / data_directory.join`，`crates/winwincode-worker/src/main.rs:187`。
- `JobWorkspaceRuntime::open(data_directory.join("worker-workspaces"), &source_directory)?
            .with_validation_artifact_port / JobWorkspaceRuntime::open / data_directory.join`，`crates/winwincode-worker/src/main.rs:189`。
- `worker_instance_id.clone / started_at.clone`，`crates/winwincode-worker/src/main.rs:192`。
- `data_directory.join("codex-runtime").join / data_directory.join`，`crates/winwincode-worker/src/main.rs:198`。
- `WorkerMain::new(config, port, codex, workspaces)
        .with_device_providers(&provider_directory)?
        .with_observer_mode(observer_mode)
        .with_registration_request_namespace(&worker_instance_id, &started_at)
        .with_model_intake_log / WorkerMain::new(config, port, codex, workspaces)
        .with_device_providers(&provider_directory)?
        .with_observer_mode(observer_mode)
        .with_registration_request_namespace / WorkerMain::new(config, port, codex, workspaces)
        .with_device_providers(&provider_directory)?
        .with_observer_mode / WorkerMain::new(config, port, codex, workspaces)
        .with_device_providers / WorkerMain::new`，`crates/winwincode-worker/src/main.rs:199`。
- `worker.with_observation_model`，`crates/winwincode-worker/src/main.rs:204`。
- `worker.lifecycle / worker.lifecycle / Box::pin / worker.start / started_at.clone / Box::pin / drain_controls / worker.lifecycle / tokio::time::sleep / Duration::from_millis`，`crates/winwincode-worker/src/main.rs:208`。
- `tokio::time::interval / Duration::from_secs`，`crates/winwincode-worker/src/main.rs:232`。
- `tokio::time::interval / Duration::from_millis`，`crates/winwincode-worker/src/main.rs:233`。
- `Box::pin / worker.shutdown / now_instant`，`crates/winwincode-worker/src/main.rs:260`。
- `Ok`，`crates/winwincode-worker/src/main.rs:261`。

`worker_constructor` 的正常源码顺序：

- `recover_message_sequence`，`crates/winwincode-worker/src/lib.rs:487`。
- `recover_heartbeat_sequence`，`crates/winwincode-worker/src/lib.rs:488`。
- `HashMap::new / HashMap::new / HashMap::new / HashSet::new / HashSet::new / HashSet::new / HashSet::new / HashSet::new / VecDeque::new / HashMap::new / HashSet::new`，`crates/winwincode-worker/src/lib.rs:490`。

自动关系类型：`{"captured_call_step": 89, "conditional_direct_statement_order": 28, "direct_statement_call_step": 31, "ordered_source_assignment_attempt": 1, "report_source_role": 3, "result_try_normal_continuation": 28, "source_guard_and_abrupt_branch": 2}`。

分析缺口：

```json
[
  {
    "code": "report_source_role_graph_binding_limited",
    "declaration_binding_limits": {
      "attribute_macros_unknown": true
    },
    "location": {
      "column": 1,
      "column_base": 1,
      "column_unit": "utf8_bytes",
      "coordinate_space": "captured_text_utf8",
      "end_byte": 10828,
      "end_column": 2,
      "end_line": 262,
      "file": "crates/winwincode-worker/src/main.rs",
      "grammar": "rust",
      "line": 154,
      "original_file_end_byte": 10828,
      "original_file_start_byte": 6268,
      "parse_identity": {
        "coordinate_space": "captured_text_utf8",
        "derived_text_utf8_sha256": null,
        "literal_authority": "original_saved_source_text_only",
        "original_text_utf8_sha256": "b411e70451b7dfd76fd59cdedba9f7bab7a40b694fb47bc6299da7709b28690d",
        "position_map": "identity_utf8_bytes_and_line_columns",
        "projection_mode": "original",
        "projection_version": null,
        "raw_prefix_bytes": 0,
        "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-rust-0.24.0+cpython-3.12.14",
        "semantic_source_version": "semantic-snapshot-sources-1",
        "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
      },
      "parser_version": "tree-sitter-0.25.2+tree-sitter-rust-0.24.0+cpython-3.12.14",
      "raw_prefix_bytes": 0,
      "semantic_parse_id": "9b1b6a5da0112fe2c51a6fb79d5a27871960f56673e992fefecf2eef97a8e7fe",
      "source_excerpt": "async fn run_worker(bootstrap: WorkerBootstrap) -> Result<(), Box<dyn std::error::Error>> {\n    let WorkerBootstrap {\n        exit_after_work,\n        worker_id,\n        worker_instance_id,\n        started_at,\n        data_directory,\n        provider_directory,\n        source_directory,\n        server_origin,\n        credential_path,\n        model_route,\n    } = bootstrap;\n    let capabilities = worker_capabilities()?;\n    let execution_mode = configured_execution_mode(\"WWC_WORKER_EXECUTION_MODE\")?;\n    let observer_mode = configured_observer_mode(\"WWC_WORKER_OBSERVER_MODE\")?;\n    let observation_model = configured_observation_model(observer_mode, required)?;\n    let (port, handle) = RemoteWorkerPort::open(\n        &server_origin,\n        &fs::read(required(\"WWC_WORKER_TLS_ROOT_DER_FILE\")?)?,\n        credential_path,\n        worker_id.clone(),\n        worker_instance_id.clone(),\n        Duration::from_secs(15),\n    )?;\n    let codex = production_codex(\n        &data_directory,\n        &provider_directory,\n        model_route,\n        capabilities.clone(),\n        execution_mode,\n        observer_mode,\n    )?;\n    let validation_artifacts =\n        DurableValidationArtifactStore::open(data_directory.join(\"worker-validation-artifacts\"))?;\n    let workspaces =\n        JobWorkspaceRuntime::open(data_directory.join(\"worker-workspaces\"), &source_directory)?\n            .with_validation_artifact_port(validation_artifacts);\n    let config = WorkerConfig {\n        worker_id,\n        worker_instance_id: worker_instance_id.clone(),\n        started_at: started_at.clone(),\n        capabilities,\n    };\n    let intake_log = data_directory.join(\"codex-runtime\").join(\"model-intake.log\");\n    let mut worker = WorkerMain::new(config, port, codex, workspaces)\n        .with_device_providers(&provider_directory)?\n        .with_observer_mode(observer_mode)\n        .with_registration_request_namespace(&worker_instance_id, &started_at)\n        .with_model_intake_log(&intake_log);\n    if let Some(observation_model) = observation_model {\n        worker = worker.with_observation_model(observation_model);\n    }\n\n    while worker.lifecycle() == WorkerLifecycleState::Booting\n        || worker.lifecycle() == WorkerLifecycleState::Registering\n    {\n        match Box::pin(worker.start(started_at.clone())).await {\n            Ok(()) => {\n                Box::pin(drain_controls(&mut worker, &handle)).await?;\n            }\n            Err(error) => {\n                // Secret-safe lifecycle category only: a Device StrongFlow\n                // Worker that silently retries registration forever is\n                // indistinguishable from a hung process in production logs.\n                eprintln!(\n                    \"winwincode-worker: registration/start retry category={:?} reason={} lifecycle={:?}\",\n                    error.code,\n                    error.reason,\n                    worker.lifecycle()\n                );\n            }\n        }\n        if worker.lifecycle() != WorkerLifecycleState::Active {\n            tokio::time::sleep(Duration::from_millis(250)).await;\n        }\n    }\n\n    let mut heartbeat = tokio::time::interval(Duration::from_secs(1));\n    let mut drive = tokio::time::interval(Duration::from_millis(25));\n    loop {\n        tokio::select! {\n            _ = tokio::signal::ctrl_c() => break,\n            _ = heartbeat.tick() => {\n                let now = now_instant()?;\n                if Box::pin(worker.heartbeat(now.clone())).await.is_ok() {\n                    Box::pin(drain_controls(&mut worker, &handle)).await?;\n                }\n            }\n            _ = drive.tick() => {\n                let now = now_instant()?;\n                Box::pin(drain_controls(&mut worker, &handle)).await?;\n                // Retry pending Worker→Server evidence every drive tick so a\n                // Server restart / Connection-refused window cannot strand\n                // runtime.event / artifact.chunk / JobOutcome in the outbox.\n                if worker.lifecycle() == WorkerLifecycleState::Active\n                    && Box::pin(worker.flush_",
      "source_excerpt_truncated": true,
      "source_hash": "b411e70451b7dfd76fd59cdedba9f7bab7a40b694fb47bc6299da7709b28690d",
      "source_line": "async fn run_worker(bootstrap: WorkerBootstrap) -> Result<(), Box<dyn std::error::Error>> {",
      "span_hash": "ab106e71bf791a0283412d398b3b36bdc13d453808b0b2a0c49ccb285c8b5982",
      "start_byte": 6268
    },
    "origin": "unresolved",
    "role": "shared_loop",
    "source_body_available": true,
    "source_gaps": [
      {
        "code": "graph_declaration_not_unique",
        "file": "crates/winwincode-worker/src/main.rs",
        "line": 154,
        "message": "图声明不是唯一、完整的捕获函数/方法。"
      }
    ]
  },
  {
    "code": "report_source_role_graph_binding_limited",
    "declaration_binding_limits": {
      "attribute_macros_unknown": true
    },
    "location": {
      "column": 1,
      "column_base": 1,
      "column_unit": "utf8_bytes",
      "coordinate_space": "captured_text_utf8",
      "end_byte": 15782,
      "end_column": 2,
      "end_line": 375,
      "file": "crates/winwincode-worker/src/main.rs",
      "grammar": "rust",
      "line": 315,
      "original_file_end_byte": 15782,
      "original_file_start_byte": 13028,
      "parse_identity": {
        "coordinate_space": "captured_text_utf8",
        "derived_text_utf8_sha256": null,
        "literal_authority": "original_saved_source_text_only",
        "original_text_utf8_sha256": "b411e70451b7dfd76fd59cdedba9f7bab7a40b694fb47bc6299da7709b28690d",
        "position_map": "identity_utf8_bytes_and_line_columns",
        "projection_mode": "original",
        "projection_version": null,
        "raw_prefix_bytes": 0,
        "semantic_parser_version": "tree-sitter-0.25.2+tree-sitter-rust-0.24.0+cpython-3.12.14",
        "semantic_source_version": "semantic-snapshot-sources-1",
        "snapshot_id": "ee8ab91784696fc72e3101ca3887d86b45932a83832fb48875f2fd7ec54fca28"
      },
      "parser_version": "tree-sitter-0.25.2+tree-sitter-rust-0.24.0+cpython-3.12.14",
      "raw_prefix_bytes": 0,
      "semantic_parse_id": "9b1b6a5da0112fe2c51a6fb79d5a27871960f56673e992fefecf2eef97a8e7fe",
      "source_excerpt": "fn production_codex(\n    data_directory: &std::path::Path,\n    provider_directory: &std::path::Path,\n    model_route: ModelGatewayRoute,\n    capabilities: WorkerCapabilitySet,\n    execution_mode: ExecutionMode,\n    observer_mode: ObserverMode,\n) -> Result<ProductionCodexAdapter, Box<dyn std::error::Error>> {\n    let helper_release_manifest = HelperReleaseManifest::from_file(&PathBuf::from(required(\n        \"WWC_WORKER_HELPER_RELEASE_MANIFEST\",\n    )?))?;\n    let store = winwincode_provider::DeviceProviderStore::open(provider_directory)?;\n    let snapshot = store.snapshot(\"local\")?;\n    let extensions = store.restore_extensions(&data_directory.join(\"codex-runtime/kernel-home\"))?;\n    let mut discovered_capabilities = Vec::new();\n    for server in extensions {\n        for tool in server.tools {\n            discovered_capabilities.push(\n                winwincode_execution_port::capability_adapter::CapabilityDescriptor::mcp(\n                    &server.server,\n                    &tool,\n                    server.digest.trim_start_matches(\"sha256:\"),\n                    winwincode_execution_port::capability_adapter::CapabilityHealth::Healthy,\n                    winwincode_execution_port::capability_adapter::CapabilityOrigin::CodexCoreMcp,\n                )?,\n            );\n        }\n    }\n    let default_provider = snapshot\n        .providers\n        .iter()\n        .find(|provider| provider.config.enabled && provider.credential_configured)\n        .ok_or(\"configure a Provider on this Device before starting a Worker\")?;\n    let provider_id = env::var(\"WWC_WORKER_MODEL_PROVIDER_ID\")\n        .unwrap_or_else(|_| default_provider.config.provider_id.clone());\n    let model_id = env::var(\"WWC_WORKER_MODEL_ID\")\n        .unwrap_or_else(|_| default_provider.config.model_ids[0].clone());\n    let options = ProductionCodexOptions {\n        data_directory: data_directory.join(\"codex-runtime\"),\n        helper_executable: PathBuf::from(required(\"WWC_WORKER_HELPER_EXECUTABLE\")?),\n        helper_release_manifest,\n        provider: provider_id,\n        model: model_id,\n        gateway_route: model_route,\n        registered_capabilities: capabilities,\n        discovered_capabilities,\n        action_signing_key: ActionEnforcementSigningKey::from_bytes(parse_hex_key(&required(\n            \"WWC_WORKER_ACTION_SIGNING_KEY_HEX\",\n        )?)?)?,\n        execution_envelope: ExecutionEnvelopeToken {\n            version: 1,\n            digest: Sha256Digest(required(\"WWC_WORKER_EXECUTION_ENVELOPE_DIGEST\")?),\n        },\n        execution_mode,\n        observer_mode,\n    };\n    Ok(\n        ProductionCodexAdapter::open(ProductionCodexConfig::try_new(options)?)?\n            .with_device_extensions(provider_directory.to_path_buf())?,\n    )\n}",
      "source_excerpt_truncated": false,
      "source_hash": "b411e70451b7dfd76fd59cdedba9f7bab7a40b694fb47bc6299da7709b28690d",
      "source_line": "fn production_codex(",
      "span_hash": "b272e828de1bffb3cc79d3615a702afdaf04bab16da6525157bf1f2564bec563",
      "start_byte": 13028
    },
    "origin": "unresolved",
    "role": "adapter_factory",
    "source_body_available": true,
    "source_gaps": [
      {
        "code": "graph_declaration_not_unique",
        "file": "crates/winwincode-worker/src/main.rs",
        "line": 315,
        "message": "图声明不是唯一、完整的捕获函数/方法。"
      }
    ]
  }
]
```

条件与反证声明（单列为配置范围，不冒充源码证据）：

```json
{
  "applicability": {
    "conditions": [
      "Selected definitions and raw source are authenticated in the same snapshot.",
      "Recorded source structure and conditional normal reaching are the evidence scope; target execution, all-path completion, generic runtime activation and physical side effects are not established."
    ],
    "counterexamples": [
      "Generic WorkerMain methods are not globally bound to the production Codex adapter by this construction evidence.",
      "Provider/helper/TLS/configuration and allocation errors can prevent later statements."
    ],
    "kind": "conditional"
  },
  "descriptive_counterexamples_are_computed_evidence": false,
  "origin": "policy-declared",
  "provenance": {
    "author_approved": false,
    "authority": "independent-static-report-benchmark",
    "note": "Source locators only; the detector derives calls, guards, construction operands and normal source order. No generic target or precomputed path is declared.",
    "reviewer": "captured-source-report-expansion",
    "source_doc": "reports/astra-baseline/WINWINCODE_ANALYSIS.md"
  }
}
```

### wwc-report-worker-typed-dispatch

类型：`guarded_call_sequence`；源码关系评估：`scoped_source_relations_supported`。

保存发现：`0a29aee5f115a4f749fffe8a`；证据：`5666ac49d3b01d2f3f7d103f`。

- `control`：`crates/winwincode-worker/src/lib.rs` / `WorkerMain.accept_control`。
- `dispatch`：`crates/winwincode-worker/src/lib.rs` / `WorkerMain.accept_dispatch`。
- `start`：`crates/winwincode-worker/src/lib.rs` / `WorkerMain.start_dispatch`。

`control` 的正常源码顺序：

- `self.accept_registration / self.codex
                    .accept_execution_delivery_ack(message)
                    .map_err / self.codex
                    .accept_execution_delivery_ack / self.flush_durable_execution_deliveries / self.flush_durable_execution_deliveries_with_core_replay / self.accept_dispatch / self.accept_cancel / self.accept_candidate_artifact_ack / self
                    .workspaces
                    .is_observation_model_exchange(&chunk.model_exchange_id)
                    .map_err / self
                    .workspaces
                    .is_observation_model_exchange / self.accept_observation_model_chunk / self.codex
                    .accept_model_chunk(chunk, &now)
                    .await
                    .map_err / self.codex
                    .accept_model_chunk / self.codex.accept_execution_delivery_ack(message).is_err / self.codex.accept_execution_delivery_ack / std::env::var_os("WWC_WORKER_POLL_DEBUG").is_some / std::env::var_os / self.flush_durable_execution_deliveries().await.is_err / self.flush_durable_execution_deliveries / std::env::var_os("WWC_WORKER_POLL_DEBUG").is_some / std::env::var_os / self.flush_codex_execution_messages().await.is_err / self.flush_codex_execution_messages / std::env::var_os("WWC_WORKER_POLL_DEBUG").is_some / std::env::var_os / Ok / self.codex
                    .accept_action_receipt(receipt, &now)
                    .await
                    .map_err / self.codex
                    .accept_action_receipt / self.codex
                    .accept_execution_delivery_ack(message)
                    .map_err / self.codex
                    .accept_execution_delivery_ack / self.flush_durable_execution_deliveries / self.flush_codex_execution_messages / self.accept_approval_decision / self.flush_durable_execution_deliveries / self.flush_codex_execution_messages / self.accept_input_response / self.flush_durable_execution_deliveries / self.flush_codex_execution_messages / self.codex
                    .accept_execution_delivery_ack(message)
                    .map_err / self.codex
                    .accept_execution_delivery_ack / self.flush_durable_execution_deliveries / self.replay_runtime / Err / worker_error`，`crates/winwincode-worker/src/lib.rs:748`。

`dispatch` 的正常源码顺序：

- `Err / worker_error`，`crates/winwincode-worker/src/lib.rs:2639`。
- `dispatch_authority_rejection / self.send_dispatch_result / Some / Ok`，`crates/winwincode-worker/src/lib.rs:2645`。
- `CodexRunKey::from_dispatch`，`crates/winwincode-worker/src/lib.rs:2650`。
- `winwincode_codex::stage_product::stage_product_job_digest(&dispatch.job)
            .map_err / winwincode_codex::stage_product::stage_product_job_digest`，`crates/winwincode-worker/src/lib.rs:2651`。
- `self.dispatches.get(&dispatch.job.job_id.0).cloned / self.dispatches.get / self.send_dispatch_result / Some / Ok`，`crates/winwincode-worker/src/lib.rs:2658`。
- `winwincode_codex::stage_product::stage_product_prompt(&dispatch.job).is_err / winwincode_codex::stage_product::stage_product_prompt / self.send_dispatch_result / Some / port_error / Ok`，`crates/winwincode-worker/src/lib.rs:2674`。
- `usize::try_from(self.config.capabilities.max_concurrent_jobs).unwrap_or / usize::try_from`，`crates/winwincode-worker/src/lib.rs:2689`。
- `self.active.len / self.send_dispatch_result / Ok`，`crates/winwincode-worker/src/lib.rs:2690`。
- `scope_identity`，`crates/winwincode-worker/src/lib.rs:2701`。
- `self.start_dispatch`，`crates/winwincode-worker/src/lib.rs:2702`。

`start` 的正常源码顺序：

- `self.prepare_dispatch_workspace / self.reject_dispatch_failure / Ok`，`crates/winwincode-worker/src/lib.rs:2723`。
- `self
            .codex
            .ensure_thread / self.workspaces.prepare_close_job / self.reject_dispatch_failure / Ok`，`crates/winwincode-worker/src/lib.rs:2744`。
- `self.dispatch_thread_conflicts / self.codex.close_thread / self.workspaces.prepare_close_job / self.reject_dispatch_failure / Ok`，`crates/winwincode-worker/src/lib.rs:2777`。
- `self.recovered_runtime_cursor`，`crates/winwincode-worker/src/lib.rs:2795`。
- `self.install_dispatch_binding / runtime_session_context / now.clone`，`crates/winwincode-worker/src/lib.rs:2797`。
- `self.start_bound_job`，`crates/winwincode-worker/src/lib.rs:2810`。

自动关系类型：`{"captured_call_step": 88, "conditional_direct_statement_order": 14, "direct_statement_call_step": 17, "ordered_source_assignment_attempt": 1, "report_source_role": 3, "result_try_normal_continuation": 23, "source_guard_and_abrupt_branch": 11}`。

分析缺口：

```json
[]
```

条件与反证声明（单列为配置范围，不冒充源码证据）：

```json
{
  "applicability": {
    "conditions": [
      "Selected definitions and raw source are authenticated in the same snapshot.",
      "Recorded source structure and conditional normal reaching are the evidence scope; target execution, all-path completion, generic runtime activation and physical side effects are not established."
    ],
    "counterexamples": [
      "Generic CodexCoreAdapter ensure_thread/submit_turn remain source invocation candidates; no unique production CALLS edge is manufactured.",
      "Replay, lifecycle, authority, stage-contract, capacity, checkout and start errors keep their branches; this is not all-failure resource cleanup proof."
    ],
    "kind": "conditional"
  },
  "descriptive_counterexamples_are_computed_evidence": false,
  "origin": "policy-declared",
  "provenance": {
    "author_approved": false,
    "authority": "independent-static-report-benchmark",
    "note": "Source locators only; the detector derives calls, guards, construction operands and normal source order. No generic target or precomputed path is declared.",
    "reviewer": "captured-source-report-expansion",
    "source_doc": "reports/astra-baseline/WINWINCODE_ANALYSIS.md"
  }
}
```

### wwc-report-workrun-state-guards

类型：`state_guard_sequence`；源码关系评估：`scoped_source_relations_supported`。

保存发现：`cf8f7d136865ae065a81d04f`；证据：`fba2a1501b574cd345f61de9`。

- `selection`：`crates/winwincode-delivery/src/application/workrun.rs` / `WorkRunAggregate.start_next`。
- `start`：`crates/winwincode-delivery/src/application/workrun.rs` / `WorkRunAggregate.start_item`。

`selection` 的正常源码顺序：

- `self.validate`，`crates/winwincode-delivery/src/application/workrun.rs:392`。
- `self
            .runs
            .iter()
            .filter(|run| {
                matches!(
                    run.state,
                    WorkRunState::Leased | WorkRunState::Running | WorkRunState::CandidateReady
                )
            })
            .map(|run| run.work_item_id.clone())
            .collect / self
            .runs
            .iter()
            .filter(|run| {
                matches!(
                    run.state,
                    WorkRunState::Leased | WorkRunState::Running | WorkRunState::CandidateReady
                )
            })
            .map / self
            .runs
            .iter()
            .filter / self
            .runs
            .iter`，`crates/winwincode-delivery/src/application/workrun.rs:393`。
- `start_next_work_run / self.contract.revision.clone`，`crates/winwincode-delivery/src/application/workrun.rs:404`。
- `self.start_item`，`crates/winwincode-delivery/src/application/workrun.rs:411`。

`start` 的正常源码顺序：

- `self.validate`，`crates/winwincode-delivery/src/application/workrun.rs:419`。
- `self
            .items
            .iter()
            .find(|item| {
                &item.id == id
                    && work_item_is_runnable(item, &self.items)
                    && !self.runs.iter().any(|run| {
                        &run.work_item_id == id
                            && matches!(
                                run.state,
                                WorkRunState::Leased
                                    | WorkRunState::Running
                                    | WorkRunState::CandidateReady
                            )
                    })
            })
            .ok_or / self
            .items
            .iter()
            .find / self
            .items
            .iter`，`crates/winwincode-delivery/src/application/workrun.rs:420`。
- `item.clone`，`crates/winwincode-delivery/src/application/workrun.rs:439`。
- `Ok`，`crates/winwincode-delivery/src/application/workrun.rs:441`。

自动关系类型：`{"captured_call_step": 14, "conditional_direct_statement_order": 6, "direct_statement_call_step": 8, "ordered_source_assignment_attempt": 1, "report_source_role": 2, "result_try_normal_continuation": 4, "state_selection_predicate_source": 8}`。

分析缺口：

```json
[
  {
    "code": "iterator_selection_and_macro_runtime_semantics_not_fully_proven",
    "origin": "unresolved",
    "source_only": true
  }
]
```

条件与反证声明（单列为配置范围，不冒充源码证据）：

```json
{
  "applicability": {
    "conditions": [
      "Selected declarations and saved source are authenticated in the same snapshot.",
      "Relations describe captured source structure and selected normal reaching, not target execution, completion or whole-repository correctness."
    ],
    "counterexamples": [
      "No candidate or a Result error can prevent a later call.",
      "Iterator/matches source predicates are preserved without claiming all runtime states or expanding macros."
    ],
    "kind": "conditional"
  },
  "descriptive_counterexamples_are_computed_evidence": false,
  "origin": "policy-declared",
  "provenance": {
    "author_approved": false,
    "authority": "independent-static-report-benchmark",
    "note": "Locator-only source selection; original report wording is not consumed by the detector.",
    "reviewer": "source-derived-report-chains",
    "source_doc": "reports/astra-baseline/WINWINCODE_ANALYSIS.md"
  }
}
```

## 覆盖账本

选入 471 份源码，解析 465 份。该数量描述捕获范围，不是功能覆盖率。

| 区域 | 文件 | 已解析 |
| --- | --- |
| apps/client | 95 | 95 |
| crates/helper | 1 | 1 |
| crates/kernel | 2 | 2 |
| crates/winwincode-api | 1 | 1 |
| crates/winwincode-audit | 5 | 5 |
| crates/winwincode-cli | 11 | 11 |
| crates/winwincode-client-port | 12 | 12 |
| crates/winwincode-codex | 16 | 16 |
| crates/winwincode-connector-github | 1 | 1 |
| crates/winwincode-connector-jira | 1 | 1 |
| crates/winwincode-connector-linear | 1 | 1 |
| crates/winwincode-connector-slack | 1 | 1 |
| crates/winwincode-connector-teams | 1 | 1 |
| crates/winwincode-connector-webhook | 1 | 1 |
| crates/winwincode-control-plane | 94 | 94 |
| crates/winwincode-data-export | 1 | 1 |
| crates/winwincode-delivery | 25 | 25 |
| crates/winwincode-device-client | 20 | 20 |
| crates/winwincode-domain | 5 | 5 |
| crates/winwincode-evidence-export | 6 | 6 |
| crates/winwincode-execution-port | 26 | 25 |
| crates/winwincode-fusion | 4 | 4 |
| crates/winwincode-integration-core | 5 | 5 |
| crates/winwincode-integration-sqlite | 2 | 2 |
| crates/winwincode-local | 1 | 1 |
| crates/winwincode-observability-core | 1 | 1 |
| crates/winwincode-observability-sqlite | 1 | 1 |
| crates/winwincode-provider | 11 | 11 |
| crates/winwincode-publication | 7 | 7 |
| crates/winwincode-repository-context | 5 | 5 |
| crates/winwincode-s3-artifact-adapter | 1 | 1 |
| crates/winwincode-server | 23 | 22 |
| crates/winwincode-session | 4 | 4 |
| crates/winwincode-storage | 34 | 33 |
| crates/winwincode-worker | 21 | 18 |
| deploy | 1 | 1 |
| docs/engineering-runtime | 1 | 1 |
| jev-runtime-spec/js | 1 | 1 |
| packages/browser-core | 2 | 2 |
| packages/browser-ui | 7 | 7 |
| packages/contracts | 6 | 6 |
| packages/control-plane-client | 1 | 1 |
| packages/strongflow | 2 | 2 |
| schema/winwincode-export | 3 | 3 |
| winwincode-bd-tracks/js | 1 | 1 |

## 架构关系

以下是已绑定的跨目录引用。边数表示源码图记录数，未推断执行频率或职责。

| 来源 | 目标 | 图引用数 |
| --- | --- |
| apps/client | packages/browser-core | 51 |
| apps/client | packages/browser-ui | 55 |
| apps/client | packages/control-plane-client | 10 |
| crates/kernel | crates/winwincode-execution-port | 1 |
| crates/winwincode-cli | crates/winwincode-device-client | 19 |
| crates/winwincode-cli | crates/winwincode-repository-context | 2 |
| crates/winwincode-codex | crates/kernel | 2 |
| crates/winwincode-codex | crates/winwincode-domain | 4 |
| crates/winwincode-codex | crates/winwincode-execution-port | 37 |
| crates/winwincode-codex | crates/winwincode-provider | 1 |
| crates/winwincode-connector-github | crates/winwincode-integration-core | 3 |
| crates/winwincode-connector-jira | crates/winwincode-integration-core | 3 |
| crates/winwincode-connector-slack | crates/winwincode-integration-core | 3 |
| crates/winwincode-connector-teams | crates/winwincode-integration-core | 3 |
| crates/winwincode-connector-webhook | crates/winwincode-integration-core | 4 |
| crates/winwincode-control-plane | crates/winwincode-audit | 29 |
| crates/winwincode-control-plane | crates/winwincode-delivery | 28 |
| crates/winwincode-control-plane | crates/winwincode-domain | 4 |
| crates/winwincode-control-plane | crates/winwincode-execution-port | 16 |
| crates/winwincode-control-plane | crates/winwincode-fusion | 1 |
| crates/winwincode-control-plane | crates/winwincode-provider | 7 |
| crates/winwincode-control-plane | crates/winwincode-publication | 6 |
| crates/winwincode-control-plane | crates/winwincode-repository-context | 1 |
| crates/winwincode-control-plane | crates/winwincode-session | 9 |
| crates/winwincode-control-plane | crates/winwincode-storage | 26 |
| crates/winwincode-delivery | crates/winwincode-domain | 7 |
| crates/winwincode-device-client | crates/winwincode-provider | 3 |
| crates/winwincode-integration-sqlite | crates/winwincode-integration-core | 19 |
| crates/winwincode-local | crates/winwincode-control-plane | 1 |
| crates/winwincode-local | crates/winwincode-execution-port | 2 |
| crates/winwincode-observability-sqlite | crates/winwincode-observability-core | 1 |
| crates/winwincode-provider | crates/winwincode-domain | 1 |
| crates/winwincode-server | crates/winwincode-client-port | 3 |
| crates/winwincode-server | crates/winwincode-control-plane | 7 |
| crates/winwincode-server | crates/winwincode-domain | 6 |
| crates/winwincode-server | crates/winwincode-execution-port | 3 |
| crates/winwincode-server | crates/winwincode-storage | 1 |
| crates/winwincode-storage | crates/winwincode-domain | 1 |
| crates/winwincode-storage | crates/winwincode-publication | 1 |
| crates/winwincode-worker | crates/winwincode-codex | 13 |
| crates/winwincode-worker | crates/winwincode-domain | 1 |
| crates/winwincode-worker | crates/winwincode-execution-port | 11 |
| crates/winwincode-worker | crates/winwincode-provider | 4 |

## 局部分析

| 规则 | 类型 | 结果 | 保存发现 |
| --- | --- | --- | --- |
| wwc-astra-device-spec-field-construction | static_contract_required_object_fields | uncertain | 44146d8ef55c66642d14f83e |
| wwc-astra-navigation-context | static_navigation_query_context | uncertain | 15997f307b3cb9f209f1a8aa |

## 未解析与未审范围

未建模的功能域继续作为分析缺口，不因已有判断通过而标为已审。

- `crates/winwincode-execution-port/src/diagnostic_parser.rs`：parse_error；Tree-sitter 检测到错误/缺失语法节点；仅提取可识别的局部结构。
- `crates/winwincode-server/src/worker_session_credentials.rs`：parse_error；Tree-sitter 检测到错误/缺失语法节点；仅提取可识别的局部结构。
- `crates/winwincode-storage/src/provider_exchange.rs`：parse_error；Tree-sitter 检测到错误/缺失语法节点；仅提取可识别的局部结构。
- `crates/winwincode-worker/src/managed_session.rs`：parse_error；Tree-sitter 检测到错误/缺失语法节点；仅提取可识别的局部结构。
- `crates/winwincode-worker/src/probe_evidence.rs`：parse_error；Tree-sitter 检测到错误/缺失语法节点；仅提取可识别的局部结构。
- `crates/winwincode-worker/src/probe_scheduler.rs`：parse_error；Tree-sitter 检测到错误/缺失语法节点；仅提取可识别的局部结构。

配置排除：`.git, .beads, .agents, .codex, .callscope, .analysis-tools, .venv, venv, __pycache__, node_modules, target, dist, build, coverage, third_party, upstream, vendor, generated, tests, test, __tests__, examples, scripts, crates/winwincode-test-assets, **/*.test.ts, **/*.test.tsx, **/*.spec.ts, **/*.spec.tsx, **/*.generated.ts, **/generated.rs, **/*_tests.rs, **/test_support.rs, **/build.rs`。

不保证运行通过、全仓库无缺陷或完整复现参考人工报告。
