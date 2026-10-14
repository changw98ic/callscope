# WinWinCode / 项目源码静态调用核对：自动静态分析报告

快照：`cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2`；状态：`partial`。

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
  "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2",
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
  "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2",
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
  "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2",
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
  "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2",
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

保存发现：`8587a3dad0bef1ede9bfd666`；证据：`e8f805eaeedf86b71cf0237b`。

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
    "source_fact_id": "navigation-fact:45a1a4ba4c1ab3b778fbcb30"
  },
  "independent_chat_source": {
    "actual_chat_success_proven": false,
    "fact_ids": [
      "navigation-fact:6e36115a909f14cea8314711"
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "8051b801fc97799b12f28377e6a869ce32371a60f010332866f51998c6da143f",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "8051b801fc97799b12f28377e6a869ce32371a60f010332866f51998c6da143f",
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
              "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
            },
            "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
            "raw_prefix_bytes": 0,
            "semantic_parse_id": "8051b801fc97799b12f28377e6a869ce32371a60f010332866f51998c6da143f",
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
            "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
          },
          "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
          "raw_prefix_bytes": 0,
          "semantic_parse_id": "8051b801fc97799b12f28377e6a869ce32371a60f010332866f51998c6da143f",
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
            "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
          },
          "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
          "raw_prefix_bytes": 0,
          "semantic_parse_id": "8051b801fc97799b12f28377e6a869ce32371a60f010332866f51998c6da143f",
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
                    "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
                  },
                  "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "raw_prefix_bytes": 0,
                  "semantic_parse_id": "8051b801fc97799b12f28377e6a869ce32371a60f010332866f51998c6da143f",
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
                    "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
                  },
                  "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "raw_prefix_bytes": 0,
                  "semantic_parse_id": "8051b801fc97799b12f28377e6a869ce32371a60f010332866f51998c6da143f",
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
                "semantic_parse_id": "8051b801fc97799b12f28377e6a869ce32371a60f010332866f51998c6da143f",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2",
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
            "id": "7f7a482053053cab29a6b903",
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
                  "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
                },
                "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "raw_prefix_bytes": 0,
                "semantic_parse_id": "8051b801fc97799b12f28377e6a869ce32371a60f010332866f51998c6da143f",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "8051b801fc97799b12f28377e6a869ce32371a60f010332866f51998c6da143f",
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
            "id": "215dcda279bca5281f7b2eb4",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "8051b801fc97799b12f28377e6a869ce32371a60f010332866f51998c6da143f",
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
            "id": "5988a1d8afb0e215fda36d0f",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "8051b801fc97799b12f28377e6a869ce32371a60f010332866f51998c6da143f",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "8051b801fc97799b12f28377e6a869ce32371a60f010332866f51998c6da143f",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
              "source_excerpt": "hash: string",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  hash: string,",
              "span_hash": "3d3bc4e4622f3e8cae75cd11dbbc51fe6e135a15891b022a56bb8455db2b6a15",
              "start_byte": 6310
            },
            "id": "46c10263228a253018d4f70d",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "8051b801fc97799b12f28377e6a869ce32371a60f010332866f51998c6da143f",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "8051b801fc97799b12f28377e6a869ce32371a60f010332866f51998c6da143f",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
              "source_excerpt": "selection: ScopeRouteSelection | CompleteRepositorySelection",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  selection: ScopeRouteSelection | CompleteRepositorySelection,",
              "span_hash": "b0b36e61b95584bd54fbcb6f1f99297d9ffd645c3e57da7d0538b7f77f419040",
              "start_byte": 6326
            },
            "id": "410d1adde1009157657706c3",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "8051b801fc97799b12f28377e6a869ce32371a60f010332866f51998c6da143f",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "592e8ba37c931f8a841c6108",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                    "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
                  },
                  "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "raw_prefix_bytes": 0,
                  "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                    "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
                  },
                  "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "raw_prefix_bytes": 0,
                  "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2",
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
            "id": "5f5e7fd6b7e774c1b69fa70c",
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
                  "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
                },
                "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "raw_prefix_bytes": 0,
                "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "62872a78c14a942051efdd08",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "22620a015f9ff563e40e8551",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                    "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
                  },
                  "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "raw_prefix_bytes": 0,
                  "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                    "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
                  },
                  "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "raw_prefix_bytes": 0,
                  "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2",
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
            "id": "e50e2565fed285e85d09471d",
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
                  "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
                },
                "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "raw_prefix_bytes": 0,
                "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "5d3cfb1cd798679fc660d43b",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
              "source_excerpt": "queryIndex < 0",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  const path = queryIndex < 0 ? hash : hash.slice(0, queryIndex)",
              "span_hash": "50bc8c2017e23a65300725a045339d9d7d5d743f93ba61a9306003856f9ee3ff",
              "start_byte": 6454
            },
            "condition_truth": false,
            "id": "2029e4a6a5cae6b1bfd42c26",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "900d139f4c31797fa36ef7ba",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                    "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
                  },
                  "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "raw_prefix_bytes": 0,
                  "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                    "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
                  },
                  "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "raw_prefix_bytes": 0,
                  "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2",
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
            "id": "9d9fc5fc26c5f239a127225e",
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
                  "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
                },
                "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "raw_prefix_bytes": 0,
                "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "d17c417e3dab26163328fb1e",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
              "source_excerpt": "queryIndex < 0",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  const parameters = new URLSearchParams(queryIndex < 0 ? '' : hash.slice(queryIndex + 1))",
              "span_hash": "50bc8c2017e23a65300725a045339d9d7d5d743f93ba61a9306003856f9ee3ff",
              "start_byte": 6545
            },
            "condition_truth": false,
            "id": "cf085cc9a148dcfb04120a4e",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                    "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
                  },
                  "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "raw_prefix_bytes": 0,
                  "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                    "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
                  },
                  "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "raw_prefix_bytes": 0,
                  "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2",
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
            "id": "3cd4794be0dcb2f92284dc00",
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
                  "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
                },
                "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "raw_prefix_bytes": 0,
                "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
              "source_excerpt": "queryIndex < 0 ? '' : hash.slice(queryIndex + 1)",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  const parameters = new URLSearchParams(queryIndex < 0 ? '' : hash.slice(queryIndex + 1))",
              "span_hash": "d5996a931a5cd759f8542906911c87a976856968f8b27150a4f171f7eb4fd8a8",
              "start_byte": 6545
            },
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "id": "d06b49a0406873a4ea64954f",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "025de8e2ae0b1b5c5677ccc2",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "6deb80ef9997f960ac24d824",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "1a42e5f4c258fe3427225c5b",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "363c23217885e9a28f01a494",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "9ebc61324e9a63ba75e85a55",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                    "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
                  },
                  "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "raw_prefix_bytes": 0,
                  "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                    "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
                  },
                  "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                  "raw_prefix_bytes": 0,
                  "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
                "semantic_source_version": "semantic-snapshot-sources-1",
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2",
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
            "id": "b160916dec695a95173a2d8e",
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
                  "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
                },
                "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
                "raw_prefix_bytes": 0,
                "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
              "source_excerpt": "[\n  'organizationId',\n  'workspaceId',\n  'projectId',\n  'repositoryId',\n]",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "const SCOPE_PARAMETER_NAMES = Object.freeze([",
              "span_hash": "f67ed33a2e677cbf4614878ecddb2f057a037109d3c45cc5044a4e5afa9ccf53",
              "start_byte": 236
            },
            "ast_owner_id": "module:ts:packages/browser-core/src/scope-context",
            "id": "7f64ccc819289ee03e28264f",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "a3d0027616f6af55381bdf20",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "d3f851343cae14cd2e0ea457",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "4f6d34cb6ed6043c34e8e9a4",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "3d63073b689c675bb5393453",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "e77c71462f878c36328f5cf0",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "2041a1afdfa3b990d2aee483",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "57a0bb8906a94a7faa07bd75",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "fabf88c4f09ec8ecbe00f834",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "1b9d555ae93642e2943ce351",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "receiver_id": "abstract-40"
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
            "id": "23990f2b962582db51488601",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "15b8214d5b423d647deeee12",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "receiver_id": "abstract-40"
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
            "id": "ded552ca76e166edd239634a",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "bb0bf871481f67ba75b0091d",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "9b1e95b47cdddbf40ffd2586",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "receiver_id": "abstract-70"
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
            "id": "3ef593745f3ac9f136854555",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "7a67d221eab25114c0edd13c",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "receiver_id": "abstract-70"
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
            "id": "3c7eef3c1b2cc0807929347e",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "1b04f1c723486b4d3fbb8b0a",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "c2d8cad735380812a66c2b82",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "receiver_id": "abstract-100"
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
            "id": "5316b12e5b07165fee12a88f",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "b963c8772baaac56c6be16ba",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "receiver_id": "abstract-100"
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
            "id": "e44bf8e060f398d59e853ccc",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "355ef654c26af94dbfdfe94b",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "receiver_id": "abstract-130"
          },
          {
            "ast_owner_id": "ts:packages/browser-core/src/scope-context#scopeHash",
            "id": "dc47adf709ad162462c76275",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "618ea3d2e10536d6b10caa02",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
              "source_excerpt": "query.length === 0",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  return query.length === 0 ? path : `${path}?${query}`",
              "span_hash": "49cfd93bb8ea528f756953145f1848e17ff287033974c70741c9847c5362bcb9",
              "start_byte": 6811
            },
            "condition_truth": false,
            "id": "4724fb102740617f7757d81b",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
              "source_excerpt": "query.length === 0 ? path : `${path}?${query}`",
              "source_excerpt_truncated": false,
              "source_hash": "333d15ba1dd557c23211064915a1265523d753218a33f9fcc6c4d79e1b28565d",
              "source_line": "  return query.length === 0 ? path : `${path}?${query}`",
              "span_hash": "29585299eb43f5c266be20402bd6000fe94f61895a72e420e8040717a52f3ea4",
              "start_byte": 6811
            },
            "id": "9cedf66489b685929fca6dc9",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "8051b801fc97799b12f28377e6a869ce32371a60f010332866f51998c6da143f",
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
                "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "c5a513e9c185b44c6d026227",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "16d1182fe50d63fab1037b080ef9ae4b0dd33539bcf0a6bfd163fb99269af53e",
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
            "id": "7dab3829c77a194913625817",
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
                "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
              },
              "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
              "raw_prefix_bytes": 0,
              "semantic_parse_id": "8051b801fc97799b12f28377e6a869ce32371a60f010332866f51998c6da143f",
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
        "id": "port-fact:5e52a746e395f9096b25b8cc",
        "inputs": [
          "port-fact:6a7c3b529604738956201582",
          "port-fact:991502ed12b4af49da8e4f65"
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
              "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
            },
            "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
            "raw_prefix_bytes": 0,
            "semantic_parse_id": "eeb82a282f3fe2d97f1914c02f9e987e46a0deb2163856888576b101c25d6850",
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
              "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
            },
            "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
            "raw_prefix_bytes": 0,
            "semantic_parse_id": "eeb82a282f3fe2d97f1914c02f9e987e46a0deb2163856888576b101c25d6850",
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
              "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
            },
            "parser_version": "tree-sitter-0.25.2+tree-sitter-typescript-0.23.2+cpython-3.12.14",
            "raw_prefix_bytes": 0,
            "semantic_parse_id": "eeb82a282f3fe2d97f1914c02f9e987e46a0deb2163856888576b101c25d6850",
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
        "snapshot_id": "cb8df7040351543262ead5637b910b0b2764be4d107818080faaf0af274f4da2"
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

保存发现：`7e7dc738afda264f3b24a0d8`；证据：`9144dc2875788bfdba88323b`。

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
    "relation_id": "f983078d1d90f50b1797209703540d7ff65c25b4cfea5e0f1a6e84e6426b72e6",
    "scope": "does not establish every non-Device save succeeds",
    "source_class": "source-derived",
    "status": "supported"
  },
  {
    "kind": "device_target_not_active_or_not_authorized",
    "relation_id": "9c0621593cdc5bb78f2afa08a9f820b3bbe5acf880d798422c2b7551cd331301",
    "source_class": "source-derived",
    "status": "supported"
  },
  {
    "kind": "chat_explicit_command",
    "relation_id": "c2e1f014184230a5bb6cf7f49e4eb28236e2741effb6c7fbfb65e1568feb05fa",
    "source_class": "source-derived",
    "status": "supported"
  },
  {
    "kind": "chat_explicit_command",
    "relation_id": "8a2c54aa495dd5dac580c2db9db50e9b52f517025a515a0e732a934c6e373b98",
    "source_class": "source-derived",
    "status": "supported"
  },
  {
    "kind": "criterion_display_is_not_wire_command",
    "relation_id": "1e1dc4c8a0b92bc00a60411f62a42bb2f88da4a8d6efe6b73e06e1c410e72d14",
    "source_class": "source-derived",
    "status": "supported"
  },
  {
    "kind": "authorized_scope_required",
    "relation_id": "66dd35f6836529520d0d10ae6e914211d2d7cf5606643cd1b00887df7fa76a31",
    "source_class": "source-derived",
    "status": "supported"
  },
  {
    "kind": "existing_exact_receipt_replays_before_authority",
    "relation_id": "4326ae1aad5595be3eb817071cf8dd0a8b83b99558cf46add27914cdf4417efc",
    "source_class": "source-derived",
    "status": "supported"
  },
  {
    "kind": "completed_command_confirmation_required",
    "relation_id": "f78bd4ccac6a98942a5c1884442a3a684001c5aa4b0f29eacd1aad2eb268be8d",
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

关系索引保留实际分析类型、pattern 和证据的 JSON Pointer。下面的摘要与真值表只展示保存值；截断不会删除原始关系，也不会把 partial 改为完整。

| 规则 | 关系类型 | 完整 pattern |
| --- | --- | --- |
| wwc-browser-continuation-lifecycle | browser_async_lifecycle | /functional_chains/0/pattern |
| wwc-captured-record-resource-writers | resource_writer_ownership | /functional_chains/1/pattern |
| wwc-report-adapter-durable-exact-turn | guarded_call_sequence | /functional_chains/2/pattern |
| wwc-report-chat-delivery-workrun-requests | guarded_call_sequence | /functional_chains/3/pattern |
| wwc-report-chat-retained-request-identities | message_identity_relations | /functional_chains/4/pattern |
| wwc-report-device-provider-deployment | deployment_provider_split | /functional_chains/5/pattern |
| wwc-report-kernel-create-session-interface | guarded_call_sequence | /functional_chains/6/pattern |
| wwc-report-kernel-reconcile-exact-interface | guarded_call_sequence | /functional_chains/7/pattern |
| wwc-report-kernel-submit-turn-interface | guarded_call_sequence | /functional_chains/8/pattern |
| wwc-report-outbox-ack-correlation-fields | message_identity_relations | /functional_chains/9/pattern |
| wwc-report-production-adapter-embedded-kernel | guarded_call_sequence | /functional_chains/10/pattern |
| wwc-report-submission-intent-kernel-order | guarded_call_sequence | /functional_chains/11/pattern |
| wwc-report-worker-adapter-record-identities | message_identity_relations | /functional_chains/12/pattern |
| wwc-report-worker-bootstrap-entries | guarded_call_sequence | /functional_chains/13/pattern |
| wwc-report-worker-production-construction | guarded_call_sequence | /functional_chains/14/pattern |
| wwc-report-worker-typed-dispatch | guarded_call_sequence | /functional_chains/15/pattern |
| wwc-report-workrun-finite-selection | rust_finite_state_selection | /functional_chains/16/pattern |
| wwc-report-workrun-state-guards | state_guard_sequence | /functional_chains/17/pattern |

### wwc-browser-continuation-lifecycle

类型：`browser_async_lifecycle`；源码关系评估：`scoped_source_relations_supported`。

保存发现：`87c75b2e07643b48cd81f1d8`；证据：`7f72aef766f31b9517847707`。

- `shell`：`apps/client/src/application.ts` / `mountWinWinCodeClient`。
- `performRender`：`apps/client/src/application.ts` / `mountWinWinCodeClient.performRender`。
- `authenticatedRouteContext`：`apps/client/src/application.ts` / `mountWinWinCodeClient.authenticatedRouteContext`。
- `ensureAttentionMonitor`：`apps/client/src/application.ts` / `mountWinWinCodeClient.ensureAttentionMonitor`。
- `renderChat`：`apps/client/src/application.ts` / `mountWinWinCodeClient.renderChat`。
- `renderProjects`：`apps/client/src/application.ts` / `mountWinWinCodeClient.renderProjects`。
- `renderDevice`：`apps/client/src/application.ts` / `mountWinWinCodeClient.renderDevice`。
- `renderExtensions`：`apps/client/src/application.ts` / `mountWinWinCodeClient.renderExtensions`。
- `renderSettings`：`apps/client/src/application.ts` / `mountWinWinCodeClient.renderSettings`。
- `renderHome`：`apps/client/src/application.ts` / `mountWinWinCodeClient.renderHome`。
- `renderTaskEntry`：`apps/client/src/application.ts` / `mountWinWinCodeClient.renderTaskEntry`。
- `renderTaskRun`：`apps/client/src/application.ts` / `mountWinWinCodeClient.renderTaskRun`。
- `renderDecisionClarification`：`apps/client/src/application.ts` / `mountWinWinCodeClient.renderDecisionClarification`。
- `renderCandidateRunPreview`：`apps/client/src/application.ts` / `mountWinWinCodeClient.renderCandidateRunPreview`。
- `renderReview`：`apps/client/src/application.ts` / `mountWinWinCodeClient.renderReview`。
- `renderOnboarding`：`apps/client/src/application.ts` / `mountWinWinCodeClient.renderOnboarding`。
- `launchRoute`：`apps/client/src/application.ts` / `mountWinWinCodeClient.launchRoute`。
- `settingsShell`：`apps/client/src/settings-page.ts` / `mountSettingsPage`。
- `usageConsumer`：`apps/client/src/settings-page.ts` / `mountSettingsPage.onUsageFirstOpen`。

保存关系的展示摘要（`presentation_only=true`；不新增评级）：

完整 pattern：`/functional_chains/0/pattern`。展示截断：`true`；完整证据与原 pattern 保留。

| 保存字段 | 实际值 | 完整引用 |
| --- | --- | --- |
| all_async_callbacks_guarded_proven | false | /functional_chains/0/pattern/all_async_callbacks_guarded_proven |
| all_resources_released_proven | false | /functional_chains/0/pattern/all_resources_released_proven |
| all_stale_results_rejected_proven | false | /functional_chains/0/pattern/all_stale_results_rejected_proven |
| relation_component_version | captured-lifecycle-ownership-relations-1 | /functional_chains/0/pattern/relation_component_version |
| scoped_source_supported | true | /functional_chains/0/pattern/scoped_source_supported |
| unique_browser_runtime_binding_proven | false | /functional_chains/0/pattern/unique_browser_runtime_binding_proven |

**closed_result_disposal_consumers**：`/functional_chains/0/pattern/closed_result_disposal_consumers`；展示截断：`false`。

```json
[
  {
    "source_fact_refs": [
      "/functional_chains/0/source_facts/983"
    ],
    "close_before_normal_return": true,
    "disposed_effects_reverted_proven": false,
    "id": "c112dca676b65c597bd625be",
    "kind": "lifecycle_truthy_result_disposal_consumer",
    "origin": "source-derived",
    "promise_fulfillment_and_callback_activation_proven": false,
    "relation_component": "captured-lifecycle-ownership-relations-1",
    "selected_role": "settingsShell",
    "source_model": "browser-continuation-guard-source-v1",
    "abrupt_location": {
      "file": "apps/client/src/settings-page.ts",
      "line": 758,
      "column": 9,
      "end_line": 758,
      "start_byte": 29541,
      "end_byte": 29547,
      "full_location_ref": "/functional_chains/0/pattern/closed_result_disposal_consumers/0/abrupt_location"
    },
    "condition_token": {
      "root_declaration_id": "0d7629777cc8b0e6de78212203160b2123bba2cddb98c7a70186375e29b1e657",
      "root_name": "closed",
      "runtime_resource_identity_proven": false,
      "members": [],
      "root_declaration_location": {
        "file": "apps/client/src/settings-page.ts",
        "line": 483,
        "column": 7,
        "end_line": 483,
        "start_byte": 17405,
        "end_byte": 17419,
        "full_location_ref": "/functional_chains/0/pattern/closed_result_disposal_consumers/0/condition_token/root_declaration_location"
      },
      "root_identity": {
        "binding_id": "0d7629777cc8b0e6de78212203160b2123bba2cddb98c7a70186375e29b1e657",
        "declaration_id": "0d7629777cc8b0e6de78212203160b2123bba2cddb98c7a70186375e29b1e657",
        "declaration_kind": "let",
        "file": "apps/client/src/settings-page.ts",
        "identity_api_version": "captured-declaration-identity-only-1",
        "identity_complete": true,
        "import": null,
        "name": "closed",
        "parameter_index": null,
        "reader_version": "static-value-contracts-1",
        "state": "unique",
        "version": "captured-lexical-bindings-3",
        "write_and_effect_review_performed": false,
        "binder_location": {
          "file": "apps/client/src/settings-page.ts",
          "line": 483,
          "column": 7,
          "end_line": 483,
          "start_byte": 17405,
          "end_byte": 17411,
          "full_location_ref": "/functional_chains/0/pattern/closed_result_disposal_consumers/0/condition_token/root_identity/binder_location"
        },
        "binder_span": {
          "end_byte": 17411,
          "node_type": "identifier",
          "start_byte": 17405
        },
        "declaration_location": {
          "file": "apps/client/src/settings-page.ts",
          "line": 483,
          "column": 7,
          "end_line": 483,
          "start_byte": 17405,
          "end_byte": 17419,
          "full_location_ref": "/functional_chains/0/pattern/closed_result_disposal_consumers/0/condition_token/root_identity/declaration_location"
        },
        "declaration_span": {
          "end_byte": 17419,
          "node_type": "variable_declarator",
          "start_byte": 17405
        },
        "gaps": [],
        "limitations": [
          "identity denotes a captured lexical declaration, not an object/resource or alias identity",
          "no reaching values, target activation, hidden calls or external heap mutation are proved",
          "write records include captured syntax and possible effects, not executed writes"
        ],
        "pattern_path": [],
        "scope_location": {
          "file": "apps/client/src/settings-page.ts",
          "line": 241,
          "column": 79,
          "end_line": 913,
          "start_byte": 8923,
          "end_byte": 35585,
          "full_location_ref": "/functional_chains/0/pattern/closed_result_disposal_consumers/0/condition_token/root_identity/scope_location"
        },
        "scope_span": {
          "end_byte": 35585,
          "node_type": "statement_block",
          "start_byte": 8923
        },
        "value": {
          "heap_state_verified": false,
          "model": "captured_declaration_identity_only",
          "runtime_value_known": false,
          "stable": false,
          "reasons": [
            "visible_binding_or_member_write",
            "write_and_effect_review_not_requested"
          ]
        }
      }
    },
    "disposal_location": {
      "file": "apps/client/src/settings-page.ts",
      "line": 757,
      "column": 9,
      "end_line": 757,
      "start_byte": 29517,
      "end_byte": 29532,
      "full_location_ref": "/functional_chains/0/pattern/closed_result_disposal_consumers/0/disposal_location"
    },
    "lexical_source_owner": {
      "graph_node_id": "ts:apps/client/src/settings-page#mountSettingsPage.onUsageFirstOpen.<arrow@754:66>",
      "symbol": "mountSettingsPage.onUsageFirstOpen.<arrow@754:66>",
      "location": {
        "file": "apps/client/src/settings-page.ts",
        "line": 754,
        "column": 67,
        "end_line": 761,
        "start_byte": 29441,
        "end_byte": 29590,
        "full_location_ref": "/functional_chains/0/pattern/closed_result_disposal_consumers/0/lexical_source_owner/location"
      }
    },
    "location": {
      "file": "apps/client/src/settings-page.ts",
      "line": 756,
      "column": 7,
      "end_line": 759,
      "start_byte": 29495,
      "end_byte": 29555,
      "full_location_ref": "/functional_chains/0/pattern/closed_result_disposal_consumers/0/location"
    },
    "returned_result_parameter": {
      "root_declaration_id": "d0c157f3bc8389001ae05908e33d44c70b3ca27b332bde99b86a3d5e7478c34a",
      "root_name": "binding",
      "runtime_resource_identity_proven": false,
      "members": [],
      "root_declaration_location": {
        "file": "apps/client/src/settings-page.ts",
        "line": 754,
        "column": 67,
        "end_line": 754,
        "start_byte": 29441,
        "end_byte": 29448,
        "full_location_ref": "/functional_chains/0/pattern/closed_result_disposal_consumers/0/returned_result_parameter/root_declaration_location"
      },
      "root_identity": {
        "binding_id": "d0c157f3bc8389001ae05908e33d44c70b3ca27b332bde99b86a3d5e7478c34a",
        "declaration_id": "d0c157f3bc8389001ae05908e33d44c70b3ca27b332bde99b86a3d5e7478c34a",
        "declaration_kind": "parameter",
        "file": "apps/client/src/settings-page.ts",
        "identity_api_version": "captured-declaration-identity-only-1",
        "identity_complete": true,
        "import": null,
        "name": "binding",
        "parameter_index": 0,
        "reader_version": "static-value-contracts-1",
        "state": "unique",
        "version": "captured-lexical-bindings-3",
        "write_and_effect_review_performed": false,
        "binder_location": {
          "file": "apps/client/src/settings-page.ts",
          "line": 754,
          "column": 67,
          "end_line": 754,
          "start_byte": 29441,
          "end_byte": 29448,
          "full_location_ref": "/functional_chains/0/pattern/closed_result_disposal_consumers/0/returned_result_parameter/root_identity/binder_location"
        },
        "binder_span": {
          "end_byte": 29448,
          "node_type": "identifier",
          "start_byte": 29441
        },
        "declaration_location": {
          "file": "apps/client/src/settings-page.ts",
          "line": 754,
          "column": 67,
          "end_line": 754,
          "start_byte": 29441,
          "end_byte": 29448,
          "full_location_ref": "/functional_chains/0/pattern/closed_result_disposal_consumers/0/returned_result_parameter/root_identity/declaration_location"
        },
        "declaration_span": {
          "end_byte": 29448,
          "node_type": "identifier",
          "start_byte": 29441
        },
        "gaps": [],
        "limitations": [
          "identity denotes a captured lexical declaration, not an object/resource or alias identity",
          "no reaching values, target activation, hidden calls or external heap mutation are proved",
          "write records include captured syntax and possible effects, not executed writes"
        ],
        "pattern_path": [],
        "scope_location": {
          "file": "apps/client/src/settings-page.ts",
          "line": 754,
          "column": 67,
          "end_line": 761,
          "start_byte": 29441,
          "end_byte": 29590,
          "full_location_ref": "/functional_chains/0/pattern/closed_result_disposal_consumers/0/returned_result_parameter/root_identity/scope_location"
        },
        "scope_span": {
          "end_byte": 29590,
          "node_type": "arrow_function",
          "start_byte": 29441
        },
        "value": {
          "heap_state_verified": false,
          "model": "captured_declaration_identity_only",
          "runtime_value_known": false,
          "stable": false,
          "reasons": [
            "write_and_effect_review_not_requested"
          ]
        }
      }
    }
  }
]
```

**continuation_publication_fact_ids**：`/functional_chains/0/pattern/continuation_publication_fact_ids`；展示截断：`true`。

```json
{
  "shown_items": [
    "67b43452909a6e50eb56db7f",
    "6a9a7c540c81486dd78a0a46",
    "8d52d4679e458148dae15e4c",
    "2024b0a1e493a21672f32e44",
    "5f92d1fb55467194716acbfe",
    "1f153b74d3a030403d9e53cc"
  ],
  "shown_count": 6,
  "total_count": 317,
  "truncated": true,
  "full_value_ref": "/functional_chains/0/pattern/continuation_publication_fact_ids"
}
```

**generation_argument_relations**：`/functional_chains/0/pattern/generation_argument_relations`；展示截断：`true`。

```json
{
  "shown_items": [
    {
      "source_fact_refs": [
        "/functional_chains/0/source_facts/582"
      ],
      "argument_index": 0,
      "authenticated_call_edge_id": "d27bba2c0b064d534a32c1f6",
      "authenticated_call_fact_id": "437eade0172ecd56114efb9e",
      "captured_token_source_fact_id": "0b4dd6e278266d23dd2a78e0",
      "id": "109ccae2a7bb3f2907f8a3d1",
      "kind": "lifecycle_generation_argument_to_selected_callable",
      "origin": "source-derived",
      "relation_component": "captured-lifecycle-ownership-relations-1",
      "runtime_callee_activation_or_generation_freshness_proven": false,
      "selected_role": "performRender",
      "source_model": "browser-continuation-guard-source-v1",
      "target_parameter_declaration_id": "99d53da816ac75312d3cde76332028d104d92a1b68e1aab9e6b41dae58795515",
      "target_role": "ensureAttentionMonitor",
      "target_symbol": "mountWinWinCodeClient.ensureAttentionMonitor",
      "lexical_source_owner": {
        "graph_node_id": "ts:apps/client/src/application#mountWinWinCodeClient.performRender",
        "symbol": "mountWinWinCodeClient.performRender",
        "location": {
          "file": "apps/client/src/application.ts",
          "line": 1782,
          "column": 3,
          "end_line": 1937,
          "start_byte": 74177,
          "end_byte": 81535,
          "full_location_ref": "/functional_chains/0/pattern/generation_argument_relations/0/lexical_source_owner/location"
        }
      },
      "location": {
        "file": "apps/client/src/application.ts",
        "line": 1897,
        "column": 12,
        "end_line": 1897,
        "start_byte": 79358,
        "end_byte": 79429,
        "full_location_ref": "/functional_chains/0/pattern/generation_argument_relations/0/location"
      },
      "target_parameter_location": {
        "file": "apps/client/src/application.ts",
        "line": 856,
        "column": 5,
        "end_line": 856,
        "start_byte": 34338,
        "end_byte": 34348,
        "full_location_ref": "/functional_chains/0/pattern/generation_argument_relations/0/target_parameter_location"
      }
    },
    {
      "source_fact_refs": [
        "/functional_chains/0/source_facts/583"
      ],
      "argument_index": 1,
      "authenticated_call_edge_id": "53c24b507399c861ddf4177e",
      "authenticated_call_fact_id": "c621e958fd24af3468756033",
      "captured_token_source_fact_id": "0b4dd6e278266d23dd2a78e0",
      "id": "7d67b97618ea16228a0eb3e9",
      "kind": "lifecycle_generation_argument_to_selected_callable",
      "origin": "source-derived",
      "relation_component": "captured-lifecycle-ownership-relations-1",
      "runtime_callee_activation_or_generation_freshness_proven": false,
      "selected_role": "performRender",
      "source_model": "browser-continuation-guard-source-v1",
      "target_parameter_declaration_id": "17a6f1f802b7cd5c5b6be8e1e0be0637d2bbaeeff1cb88dce511e1d1ae4dfff6",
      "target_role": "launchRoute",
      "target_symbol": "mountWinWinCodeClient.launchRoute",
      "lexical_source_owner": {
        "graph_node_id": "ts:apps/client/src/application#mountWinWinCodeClient.performRender",
        "symbol": "mountWinWinCodeClient.performRender",
        "location": {
          "file": "apps/client/src/application.ts",
          "line": 1782,
          "column": 3,
          "end_line": 1937,
          "start_byte": 74177,
          "end_byte": 81535,
          "full_location_ref": "/functional_chains/0/pattern/generation_argument_relations/1/lexical_source_owner/location"
        }
      },
      "location": {
        "file": "apps/client/src/application.ts",
        "line": 1912,
        "column": 9,
        "end_line": 1912,
        "start_byte": 79946,
        "end_byte": 80026,
        "full_location_ref": "/functional_chains/0/pattern/generation_argument_relations/1/location"
      },
      "target_parameter_location": {
        "file": "apps/client/src/application.ts",
        "line": 1983,
        "column": 5,
        "end_line": 1983,
        "start_byte": 83313,
        "end_byte": 83323,
        "full_location_ref": "/functional_chains/0/pattern/generation_argument_relations/1/target_parameter_location"
      }
    },
    {
      "source_fact_refs": [
        "/functional_chains/0/source_facts/584"
      ],
      "argument_index": 0,
      "authenticated_call_edge_id": "f18485125bbeb85ec2606b5b",
      "authenticated_call_fact_id": "14c293b6c4fb0315bd4304fc",
      "captured_token_source_fact_id": "0b4dd6e278266d23dd2a78e0",
      "id": "3ecea4134a86782351989786",
      "kind": "lifecycle_generation_argument_to_selected_callable",
      "origin": "source-derived",
      "relation_component": "captured-lifecycle-ownership-relations-1",
      "runtime_callee_activation_or_generation_freshness_proven": false,
      "selected_role": "performRender",
      "source_model": "browser-continuation-guard-source-v1",
      "target_parameter_declaration_id": "ca232fd3cfda8a5b6f27bb37670b6744172ebdc6ed80c8a7ed374e06f61d5e81",
      "target_role": "renderTaskEntry",
      "target_symbol": "mountWinWinCodeClient.renderTaskEntry",
      "lexical_source_owner": {
        "graph_node_id": "ts:apps/client/src/application#mountWinWinCodeClient.performRender",
        "symbol": "mountWinWinCodeClient.performRender",
        "location": {
          "file": "apps/client/src/application.ts",
          "line": 1782,
          "column": 3,
          "end_line": 1937,
          "start_byte": 74177,
          "end_byte": 81535,
          "full_location_ref": "/functional_chains/0/pattern/generation_argument_relations/2/lexical_source_owner/location"
        }
      },
      "location": {
        "file": "apps/client/src/application.ts",
        "line": 1912,
        "column": 21,
        "end_line": 1912,
        "start_byte": 79958,
        "end_byte": 79985,
        "full_location_ref": "/functional_chains/0/pattern/generation_argument_relations/2/location"
      },
      "target_parameter_location": {
        "file": "apps/client/src/application.ts",
        "line": 1307,
        "column": 34,
        "end_line": 1307,
        "start_byte": 53709,
        "end_byte": 53719,
        "full_location_ref": "/functional_chains/0/pattern/generation_argument_relations/2/target_parameter_location"
      }
    },
    {
      "source_fact_refs": [
        "/functional_chains/0/source_facts/585"
      ],
      "argument_index": 1,
      "authenticated_call_edge_id": "a6c6a995c00c20f009f2f15c",
      "authenticated_call_fact_id": "a88f84eae212346f18bfabe0",
      "captured_token_source_fact_id": "0b4dd6e278266d23dd2a78e0",
      "id": "9be0c3a7899d8f8bdbe77112",
      "kind": "lifecycle_generation_argument_to_selected_callable",
      "origin": "source-derived",
      "relation_component": "captured-lifecycle-ownership-relations-1",
      "runtime_callee_activation_or_generation_freshness_proven": false,
      "selected_role": "performRender",
      "source_model": "browser-continuation-guard-source-v1",
      "target_parameter_declaration_id": "17a6f1f802b7cd5c5b6be8e1e0be0637d2bbaeeff1cb88dce511e1d1ae4dfff6",
      "target_role": "launchRoute",
      "target_symbol": "mountWinWinCodeClient.launchRoute",
      "lexical_source_owner": {
        "graph_node_id": "ts:apps/client/src/application#mountWinWinCodeClient.performRender",
        "symbol": "mountWinWinCodeClient.performRender",
        "location": {
          "file": "apps/client/src/application.ts",
          "line": 1782,
          "column": 3,
          "end_line": 1937,
          "start_byte": 74177,
          "end_byte": 81535,
          "full_location_ref": "/functional_chains/0/pattern/generation_argument_relations/3/lexical_source_owner/location"
        }
      },
      "location": {
        "file": "apps/client/src/application.ts",
        "line": 1914,
        "column": 9,
        "end_line": 1914,
        "start_byte": 80080,
        "end_byte": 80156,
        "full_location_ref": "/functional_chains/0/pattern/generation_argument_relations/3/location"
      },
      "target_parameter_location": {
        "file": "apps/client/src/application.ts",
        "line": 1983,
        "column": 5,
        "end_line": 1983,
        "start_byte": 83313,
        "end_byte": 83323,
        "full_location_ref": "/functional_chains/0/pattern/generation_argument_relations/3/target_parameter_location"
      }
    },
    {
      "source_fact_refs": [
        "/functional_chains/0/source_facts/586"
      ],
      "argument_index": 0,
      "authenticated_call_edge_id": "36769631da615cce6caad79e",
      "authenticated_call_fact_id": "dcad3f4e3ec4f2fdb616a8e7",
      "captured_token_source_fact_id": "0b4dd6e278266d23dd2a78e0",
      "id": "6e7292163509ee151d3a88be",
      "kind": "lifecycle_generation_argument_to_selected_callable",
      "origin": "source-derived",
      "relation_component": "captured-lifecycle-ownership-relations-1",
      "runtime_callee_activation_or_generation_freshness_proven": false,
      "selected_role": "performRender",
      "source_model": "browser-continuation-guard-source-v1",
      "target_parameter_declaration_id": "1ef3fd6ee28fce0b250a4becb56a4c2be81a8c6d6886ec69f3fff80ba9c97b87",
      "target_role": "renderTaskRun",
      "target_symbol": "mountWinWinCodeClient.renderTaskRun",
      "lexical_source_owner": {
        "graph_node_id": "ts:apps/client/src/application#mountWinWinCodeClient.performRender",
        "symbol": "mountWinWinCodeClient.performRender",
        "location": {
          "file": "apps/client/src/application.ts",
          "line": 1782,
          "column": 3,
          "end_line": 1937,
          "start_byte": 74177,
          "end_byte": 81535,
          "full_location_ref": "/functional_chains/0/pattern/generation_argument_relations/4/lexical_source_owner/location"
        }
      },
      "location": {
        "file": "apps/client/src/application.ts",
        "line": 1914,
        "column": 21,
        "end_line": 1914,
        "start_byte": 80092,
        "end_byte": 80117,
        "full_location_ref": "/functional_chains/0/pattern/generation_argument_relations/4/location"
      },
      "target_parameter_location": {
        "file": "apps/client/src/application.ts",
        "line": 1352,
        "column": 32,
        "end_line": 1352,
        "start_byte": 55461,
        "end_byte": 55471,
        "full_location_ref": "/functional_chains/0/pattern/generation_argument_relations/4/target_parameter_location"
      }
    },
    {
      "source_fact_refs": [
        "/functional_chains/0/source_facts/587"
      ],
      "argument_index": 1,
      "authenticated_call_edge_id": "a578e45993929b07c28a0f64",
      "authenticated_call_fact_id": "dae932a51c3fa985e72dbdbb",
      "captured_token_source_fact_id": "0b4dd6e278266d23dd2a78e0",
      "id": "f8373bf25a07525cbff0be8b",
      "kind": "lifecycle_generation_argument_to_selected_callable",
      "origin": "source-derived",
      "relation_component": "captured-lifecycle-ownership-relations-1",
      "runtime_callee_activation_or_generation_freshness_proven": false,
      "selected_role": "performRender",
      "source_model": "browser-continuation-guard-source-v1",
      "target_parameter_declaration_id": "17a6f1f802b7cd5c5b6be8e1e0be0637d2bbaeeff1cb88dce511e1d1ae4dfff6",
      "target_role": "launchRoute",
      "target_symbol": "mountWinWinCodeClient.launchRoute",
      "lexical_source_owner": {
        "graph_node_id": "ts:apps/client/src/application#mountWinWinCodeClient.performRender",
        "symbol": "mountWinWinCodeClient.performRender",
        "location": {
          "file": "apps/client/src/application.ts",
          "line": 1782,
          "column": 3,
          "end_line": 1937,
          "start_byte": 74177,
          "end_byte": 81535,
          "full_location_ref": "/functional_chains/0/pattern/generation_argument_relations/5/lexical_source_owner/location"
        }
      },
      "location": {
        "file": "apps/client/src/application.ts",
        "line": 1916,
        "column": 9,
        "end_line": 1916,
        "start_byte": 80219,
        "end_byte": 80316,
        "full_location_ref": "/functional_chains/0/pattern/generation_argument_relations/5/location"
      },
      "target_parameter_location": {
        "file": "apps/client/src/application.ts",
        "line": 1983,
        "column": 5,
        "end_line": 1983,
        "start_byte": 83313,
        "end_byte": 83323,
        "full_location_ref": "/functional_chains/0/pattern/generation_argument_relations/5/target_parameter_location"
      }
    }
  ],
  "shown_count": 6,
  "total_count": 25,
  "truncated": true,
  "full_value_ref": "/functional_chains/0/pattern/generation_argument_relations"
}
```

**initial_synchronous_setup_fact_ids**：`/functional_chains/0/pattern/initial_synchronous_setup_fact_ids`；展示截断：`true`。

```json
{
  "shown_items": [
    "cb223dea72af7c462be2e88f",
    "450914f5c149d683278bba7a",
    "f0c5b76904128b3d6cd1aa02",
    "a132a1841d4579a51a844f79",
    "ebd274d99a22f7c71356ba50",
    "120968ef0c7a80ec76b3f8ea"
  ],
  "shown_count": 6,
  "total_count": 97,
  "truncated": true,
  "full_value_ref": "/functional_chains/0/pattern/initial_synchronous_setup_fact_ids"
}
```

**invalidation_fact_ids**：`/functional_chains/0/pattern/invalidation_fact_ids`；展示截断：`true`。

```json
{
  "shown_items": [
    "57bf3ceea02fc9b5e2c983d4",
    "0356e60a03cb30644bfe5ff1",
    "c33b59da0948047e4fafc5d7",
    "f1edd074fd894fc5da00c99e",
    "e762054ed30f1e0f61f44eb3",
    "5892004959f9b6264f63502f"
  ],
  "shown_count": 6,
  "total_count": 76,
  "truncated": true,
  "full_value_ref": "/functional_chains/0/pattern/invalidation_fact_ids"
}
```

**lifecycle_sources**：`/functional_chains/0/pattern/lifecycle_sources`；展示截断：`true`。

```json
{
  "shown_items": [
    {
      "role": "shell",
      "selected_symbol": "mountWinWinCodeClient",
      "callable_components": [
        {
          "callback_activation_proven": false,
          "nested_callback": true,
          "suspension_count": 1,
          "callable_location": {
            "file": "apps/client/src/application.ts",
            "line": 285,
            "column": 9,
            "end_line": 305,
            "start_byte": 11241,
            "end_byte": 12193,
            "full_location_ref": "/functional_chains/0/pattern/lifecycle_sources/0/callable_components/0/callable_location"
          },
          "controller_fact_ids": [],
          "guard_fact_ids": [],
          "publication_fact_ids": [
            "67b43452909a6e50eb56db7f"
          ]
        },
        {
          "callback_activation_proven": false,
          "nested_callback": true,
          "suspension_count": 0,
          "callable_location": {
            "file": "apps/client/src/application.ts",
            "line": 813,
            "column": 33,
            "end_line": 842,
            "start_byte": 32959,
            "end_byte": 33934,
            "full_location_ref": "/functional_chains/0/pattern/lifecycle_sources/0/callable_components/1/callable_location"
          },
          "controller_fact_ids": [],
          "guard_fact_ids": [
            "1df4fa7373e0fcfa7520524a"
          ],
          "publication_fact_ids": {
            "shown_items": [
              "6a9a7c540c81486dd78a0a46",
              "8d52d4679e458148dae15e4c",
              "2024b0a1e493a21672f32e44",
              "5f92d1fb55467194716acbfe",
              "1f153b74d3a030403d9e53cc",
              "076d1b72163cf6eb759ef64f"
            ],
            "shown_count": 6,
            "total_count": 18,
            "truncated": true,
            "full_value_ref": "/functional_chains/0/pattern/lifecycle_sources/0/callable_components/1/publication_fact_ids"
          }
        },
        {
          "callback_activation_proven": false,
          "nested_callback": true,
          "suspension_count": 0,
          "callable_location": {
            "file": "apps/client/src/application.ts",
            "line": 2068,
            "column": 5,
            "end_line": 2077,
            "start_byte": 86219,
            "end_byte": 86628,
            "full_location_ref": "/functional_chains/0/pattern/lifecycle_sources/0/callable_components/2/callable_location"
          },
          "controller_fact_ids": [],
          "guard_fact_ids": [
            "2450b2f72549f48b8185ff4e"
          ],
          "publication_fact_ids": [
            "6a1ea226bc4c51a3395dc6cc",
            "166653150bd9e7ef36700cfe",
            "f1b827a7cc5670728f417d16",
            "dad4de4bc844f76f4e2f6fcc",
            "85f4e3fab023de92c8e1ebc7"
          ]
        },
        {
          "callback_activation_proven": false,
          "nested_callback": true,
          "suspension_count": 0,
          "callable_location": {
            "file": "apps/client/src/application.ts",
            "line": 2078,
            "column": 5,
            "end_line": 2119,
            "start_byte": 86634,
            "end_byte": 88048,
            "full_location_ref": "/functional_chains/0/pattern/lifecycle_sources/0/callable_components/3/callable_location"
          },
          "controller_fact_ids": [],
          "guard_fact_ids": [
            "b83c64bf07a780e3927a5635"
          ],
          "publication_fact_ids": {
            "shown_items": [
              "0505be13ae762d1d9bb79dba",
              "32a2c1a900d6a9313ffd636d",
              "eae3069c9f0243a7c8a20ee5",
              "6f75037b9e03069ede55893e",
              "e99b48aacff8433db566037f",
              "8b882009c4b870c73c390f63"
            ],
            "shown_count": 6,
            "total_count": 39,
            "truncated": true,
            "full_value_ref": "/functional_chains/0/pattern/lifecycle_sources/0/callable_components/3/publication_fact_ids"
          }
        }
      ]
    },
    {
      "role": "performRender",
      "selected_symbol": "mountWinWinCodeClient.performRender",
      "callable_components": []
    },
    {
      "role": "authenticatedRouteContext",
      "selected_symbol": "mountWinWinCodeClient.authenticatedRouteContext",
      "callable_components": []
    },
    {
      "role": "ensureAttentionMonitor",
      "selected_symbol": "mountWinWinCodeClient.ensureAttentionMonitor",
      "callable_components": [
        {
          "callback_activation_proven": false,
          "nested_callback": false,
          "suspension_count": 2,
          "callable_location": {
            "file": "apps/client/src/application.ts",
            "line": 855,
            "column": 3,
            "end_line": 890,
            "start_byte": 34295,
            "end_byte": 35615,
            "full_location_ref": "/functional_chains/0/pattern/lifecycle_sources/3/callable_components/0/callable_location"
          },
          "controller_fact_ids": [],
          "guard_fact_ids": [
            "2b55ab314b1c73066ca93eac"
          ],
          "publication_fact_ids": {
            "shown_items": [
              "cb223dea72af7c462be2e88f",
              "450914f5c149d683278bba7a",
              "f0c5b76904128b3d6cd1aa02",
              "a132a1841d4579a51a844f79",
              "43c368ee47d701165ad29a72",
              "bf17ec00737587ff6cde4bd2"
            ],
            "shown_count": 6,
            "total_count": 10,
            "truncated": true,
            "full_value_ref": "/functional_chains/0/pattern/lifecycle_sources/3/callable_components/0/publication_fact_ids"
          }
        },
        {
          "callback_activation_proven": false,
          "nested_callback": true,
          "suspension_count": 0,
          "callable_location": {
            "file": "apps/client/src/application.ts",
            "line": 880,
            "column": 7,
            "end_line": 884,
            "start_byte": 35348,
            "end_byte": 35457,
            "full_location_ref": "/functional_chains/0/pattern/lifecycle_sources/3/callable_components/1/callable_location"
          },
          "controller_fact_ids": [],
          "guard_fact_ids": [
            "08593011853c27f07773edd9"
          ],
          "publication_fact_ids": [
            "8f6b5679297767a4a0c8236f",
            "8091100635886d32c03e5cce"
          ]
        }
      ]
    },
    {
      "role": "renderChat",
      "selected_symbol": "mountWinWinCodeClient.renderChat",
      "callable_components": [
        {
          "callback_activation_proven": false,
          "nested_callback": false,
          "suspension_count": 3,
          "callable_location": {
            "file": "apps/client/src/application.ts",
            "line": 940,
            "column": 3,
            "end_line": 1082,
            "start_byte": 37622,
            "end_byte": 44351,
            "full_location_ref": "/functional_chains/0/pattern/lifecycle_sources/4/callable_components/0/callable_location"
          },
          "controller_fact_ids": [
            "c64d2515f412262eab7f2e95"
          ],
          "guard_fact_ids": [
            "5b4a990f3aec8dfc4725f10d",
            "37988b008eb0fa23d0e1884c",
            "dcd81342ab2bb9e446a1c96d",
            "196f35eb54ff6dfda32d52ee"
          ],
          "publication_fact_ids": {
            "shown_items": [
              "ebd274d99a22f7c71356ba50",
              "120968ef0c7a80ec76b3f8ea",
              "309bb61359e5df9c969053f0",
              "d54e939f578621fe5728d8b4",
              "0ebae3c4ed6d53b81cd09abc",
              "e91c5e4deab395f50ca7bc06"
            ],
            "shown_count": 6,
            "total_count": 32,
            "truncated": true,
            "full_value_ref": "/functional_chains/0/pattern/lifecycle_sources/4/callable_components/0/publication_fact_ids"
          }
        },
        {
          "callback_activation_proven": false,
          "nested_callback": true,
          "suspension_count": 2,
          "callable_location": {
            "file": "apps/client/src/application.ts",
            "line": 1003,
            "column": 9,
            "end_line": 1007,
            "start_byte": 40905,
            "end_byte": 41215,
            "full_location_ref": "/functional_chains/0/pattern/lifecycle_sources/4/callable_components/1/callable_location"
          },
          "controller_fact_ids": [],
          "guard_fact_ids": [],
          "publication_fact_ids": [
            "6fb88aa301ea1eb6dacb9b76"
          ]
        },
        {
          "callback_activation_proven": false,
          "nested_callback": true,
          "suspension_count": 0,
          "callable_location": {
            "file": "apps/client/src/application.ts",
            "line": 1013,
            "column": 9,
            "end_line": 1018,
            "start_byte": 41441,
            "end_byte": 41772,
            "full_location_ref": "/functional_chains/0/pattern/lifecycle_sources/4/callable_components/2/callable_location"
          },
          "controller_fact_ids": [],
          "guard_fact_ids": [
            "8bbaa0978fd841ce51ae9f08"
          ],
          "publication_fact_ids": [
            "4227a99872c162fdf2506ea4",
            "6c24c119cf7fe4ab47f9e924",
            "9aa0a2034c5790dd84006e2a",
            "f695fea8ffc4462057ce9766"
          ]
        }
      ]
    },
    {
      "role": "renderProjects",
      "selected_symbol": "mountWinWinCodeClient.renderProjects",
      "callable_components": [
        {
          "callback_activation_proven": false,
          "nested_callback": false,
          "suspension_count": 1,
          "callable_location": {
            "file": "apps/client/src/application.ts",
            "line": 1086,
            "column": 3,
            "end_line": 1113,
            "start_byte": 44512,
            "end_byte": 45854,
            "full_location_ref": "/functional_chains/0/pattern/lifecycle_sources/5/callable_components/0/callable_location"
          },
          "controller_fact_ids": [
            "94ee3c217831faa9cb53eacb"
          ],
          "guard_fact_ids": [
            "70c082c8334a74a2994f9468",
            "00d80cbbed63a2469d13cec5"
          ],
          "publication_fact_ids": {
            "shown_items": [
              "7a08de55ce3e9c02a7a153df",
              "3842c20fa585b4421fb7b14a",
              "f8b6d93e53e4d41ef58716b0",
              "e882f09353803a31a3ebeb7e",
              "6ff9360de252d5d47d823a2d",
              "d2b53f56fcc92ee260a42b5e"
            ],
            "shown_count": 6,
            "total_count": 10,
            "truncated": true,
            "full_value_ref": "/functional_chains/0/pattern/lifecycle_sources/5/callable_components/0/publication_fact_ids"
          }
        }
      ]
    }
  ],
  "shown_count": 6,
  "total_count": 19,
  "truncated": true,
  "full_value_ref": "/functional_chains/0/pattern/lifecycle_sources"
}
```

**locally_guarded_publication_fact_ids**：`/functional_chains/0/pattern/locally_guarded_publication_fact_ids`；展示截断：`true`。

```json
{
  "shown_items": [
    "6a9a7c540c81486dd78a0a46",
    "8d52d4679e458148dae15e4c",
    "2024b0a1e493a21672f32e44",
    "5f92d1fb55467194716acbfe",
    "1f153b74d3a030403d9e53cc",
    "076d1b72163cf6eb759ef64f"
  ],
  "shown_count": 6,
  "total_count": 195,
  "truncated": true,
  "full_value_ref": "/functional_chains/0/pattern/locally_guarded_publication_fact_ids"
}
```

**nullable_context_consumer_relations**：`/functional_chains/0/pattern/nullable_context_consumer_relations`；展示截断：`true`。

```json
{
  "shown_items": [
    {
      "source_fact_refs": [
        "/functional_chains/0/source_facts/571"
      ],
      "authenticated_call_edge_id": "be2019c97a675d8a86ab3984",
      "authenticated_call_fact_id": "568964b19306d2358f6b1885",
      "id": "7ff72d8ccb4acb3fc0ddf199",
      "kind": "lifecycle_nullable_context_consumer_rejection",
      "operator": "===",
      "origin": "source-derived",
      "provider_source_fact_id": "1593851adfff87722fb39964",
      "relation_component": "captured-lifecycle-ownership-relations-1",
      "runtime_scope_authorization_or_selected_scope_validity_proven": false,
      "selected_role": "renderChat",
      "source_model": "browser-continuation-guard-source-v1",
      "abrupt_location": {
        "file": "apps/client/src/application.ts",
        "line": 942,
        "column": 27,
        "end_line": 942,
        "start_byte": 37759,
        "end_byte": 37765,
        "full_location_ref": "/functional_chains/0/pattern/nullable_context_consumer_relations/0/abrupt_location"
      },
      "lexical_source_owner": {
        "graph_node_id": "ts:apps/client/src/application#mountWinWinCodeClient.renderChat",
        "symbol": "mountWinWinCodeClient.renderChat",
        "location": {
          "file": "apps/client/src/application.ts",
          "line": 940,
          "column": 3,
          "end_line": 1082,
          "start_byte": 37622,
          "end_byte": 44351,
          "full_location_ref": "/functional_chains/0/pattern/nullable_context_consumer_relations/0/lexical_source_owner/location"
        }
      },
      "location": {
        "file": "apps/client/src/application.ts",
        "line": 942,
        "column": 5,
        "end_line": 942,
        "start_byte": 37737,
        "end_byte": 37765,
        "full_location_ref": "/functional_chains/0/pattern/nullable_context_consumer_relations/0/location"
      },
      "result_token": {
        "root_declaration_id": "c918697f4a82410a7af4fd5c42ddb06e5dbb278aafe275330aeea5e63d8f93a2",
        "root_name": "context",
        "runtime_resource_identity_proven": false,
        "members": [],
        "root_declaration_location": {
          "file": "apps/client/src/application.ts",
          "line": 941,
          "column": 11,
          "end_line": 941,
          "start_byte": 37695,
          "end_byte": 37732,
          "full_location_ref": "/functional_chains/0/pattern/nullable_context_consumer_relations/0/result_token/root_declaration_location"
        },
        "root_identity": {
          "binding_id": "c918697f4a82410a7af4fd5c42ddb06e5dbb278aafe275330aeea5e63d8f93a2",
          "declaration_id": "c918697f4a82410a7af4fd5c42ddb06e5dbb278aafe275330aeea5e63d8f93a2",
          "declaration_kind": "const",
          "file": "apps/client/src/application.ts",
          "identity_api_version": "captured-declaration-identity-only-1",
          "identity_complete": true,
          "import": null,
          "name": "context",
          "parameter_index": null,
          "reader_version": "static-value-contracts-1",
          "state": "unique",
          "version": "captured-lexical-bindings-3",
          "write_and_effect_review_performed": false,
          "binder_location": {
            "file": "apps/client/src/application.ts",
            "line": 941,
            "column": 11,
            "end_line": 941,
            "start_byte": 37695,
            "end_byte": 37702,
            "full_location_ref": "/functional_chains/0/pattern/nullable_context_consumer_relations/0/result_token/root_identity/binder_location"
          },
          "binder_span": {
            "end_byte": 37702,
            "node_type": "identifier",
            "start_byte": 37695
          },
          "declaration_location": {
            "file": "apps/client/src/application.ts",
            "line": 941,
            "column": 11,
            "end_line": 941,
            "start_byte": 37695,
            "end_byte": 37732,
            "full_location_ref": "/functional_chains/0/pattern/nullable_context_consumer_relations/0/result_token/root_identity/declaration_location"
          },
          "declaration_span": {
            "end_byte": 37732,
            "node_type": "variable_declarator",
            "start_byte": 37695
          },
          "gaps": [],
          "limitations": [
            "identity denotes a captured lexical declaration, not an object/resource or alias identity",
            "no reaching values, target activation, hidden calls or external heap mutation are proved",
            "write records include captured syntax and possible effects, not executed writes"
          ],
          "pattern_path": [],
          "scope_location": {
            "file": "apps/client/src/application.ts",
            "line": 940,
            "column": 64,
            "end_line": 1082,
            "start_byte": 37683,
            "end_byte": 44351,
            "full_location_ref": "/functional_chains/0/pattern/nullable_context_consumer_relations/0/result_token/root_identity/scope_location"
          },
          "scope_span": {
            "end_byte": 44351,
            "node_type": "statement_block",
            "start_byte": 37683
          },
          "value": {
            "heap_state_verified": false,
            "model": "captured_declaration_identity_only",
            "runtime_value_known": false,
            "stable": false,
            "reasons": [
              "binding_not_initialized_before_use",
              "declaration_initializer_or_binder_is_not_initialized_value",
              "write_and_effect_review_not_requested"
            ]
          }
        }
      }
    },
    {
      "source_fact_refs": [
        "/functional_chains/0/source_facts/572"
      ],
      "authenticated_call_edge_id": "465139d52417b615e4eb53c2",
      "authenticated_call_fact_id": "f156181d8054876c1294f42c",
      "id": "390f69c805387ee69786a73a",
      "kind": "lifecycle_nullable_context_consumer_rejection",
      "operator": "===",
      "origin": "source-derived",
      "provider_source_fact_id": "1593851adfff87722fb39964",
      "relation_component": "captured-lifecycle-ownership-relations-1",
      "runtime_scope_authorization_or_selected_scope_validity_proven": false,
      "selected_role": "renderProjects",
      "source_model": "browser-continuation-guard-source-v1",
      "abrupt_location": {
        "file": "apps/client/src/application.ts",
        "line": 1088,
        "column": 27,
        "end_line": 1088,
        "start_byte": 44653,
        "end_byte": 44659,
        "full_location_ref": "/functional_chains/0/pattern/nullable_context_consumer_relations/1/abrupt_location"
      },
      "lexical_source_owner": {
        "graph_node_id": "ts:apps/client/src/application#mountWinWinCodeClient.renderProjects",
        "symbol": "mountWinWinCodeClient.renderProjects",
        "location": {
          "file": "apps/client/src/application.ts",
          "line": 1086,
          "column": 3,
          "end_line": 1113,
          "start_byte": 44512,
          "end_byte": 45854,
          "full_location_ref": "/functional_chains/0/pattern/nullable_context_consumer_relations/1/lexical_source_owner/location"
        }
      },
      "location": {
        "file": "apps/client/src/application.ts",
        "line": 1088,
        "column": 5,
        "end_line": 1088,
        "start_byte": 44631,
        "end_byte": 44659,
        "full_location_ref": "/functional_chains/0/pattern/nullable_context_consumer_relations/1/location"
      },
      "result_token": {
        "root_declaration_id": "f0c097f8d06dfdf750eb344601add83899d8275a7237c8d56f2f2164473736c8",
        "root_name": "context",
        "runtime_resource_identity_proven": false,
        "members": [],
        "root_declaration_location": {
          "file": "apps/client/src/application.ts",
          "line": 1087,
          "column": 11,
          "end_line": 1087,
          "start_byte": 44589,
          "end_byte": 44626,
          "full_location_ref": "/functional_chains/0/pattern/nullable_context_consumer_relations/1/result_token/root_declaration_location"
        },
        "root_identity": {
          "binding_id": "f0c097f8d06dfdf750eb344601add83899d8275a7237c8d56f2f2164473736c8",
          "declaration_id": "f0c097f8d06dfdf750eb344601add83899d8275a7237c8d56f2f2164473736c8",
          "declaration_kind": "const",
          "file": "apps/client/src/application.ts",
          "identity_api_version": "captured-declaration-identity-only-1",
          "identity_complete": true,
          "import": null,
          "name": "context",
          "parameter_index": null,
          "reader_version": "static-value-contracts-1",
          "state": "unique",
          "version": "captured-lexical-bindings-3",
          "write_and_effect_review_performed": false,
          "binder_location": {
            "file": "apps/client/src/application.ts",
            "line": 1087,
            "column": 11,
            "end_line": 1087,
            "start_byte": 44589,
            "end_byte": 44596,
            "full_location_ref": "/functional_chains/0/pattern/nullable_context_consumer_relations/1/result_token/root_identity/binder_location"
          },
          "binder_span": {
            "end_byte": 44596,
            "node_type": "identifier",
            "start_byte": 44589
          },
          "declaration_location": {
            "file": "apps/client/src/application.ts",
            "line": 1087,
            "column": 11,
            "end_line": 1087,
            "start_byte": 44589,
            "end_byte": 44626,
            "full_location_ref": "/functional_chains/0/pattern/nullable_context_consumer_relations/1/result_token/root_identity/declaration_location"
          },
          "declaration_span": {
            "end_byte": 44626,
            "node_type": "variable_declarator",
            "start_byte": 44589
          },
          "gaps": [],
          "limitations": [
            "identity denotes a captured lexical declaration, not an object/resource or alias identity",
            "no reaching values, target activation, hidden calls or external heap mutation are proved",
            "write records include captured syntax and possible effects, not executed writes"
          ],
          "pattern_path": [],
          "scope_location": {
            "file": "apps/client/src/application.ts",
            "line": 1086,
            "column": 68,
            "end_line": 1113,
            "start_byte": 44577,
            "end_byte": 45854,
            "full_location_ref": "/functional_chains/0/pattern/nullable_context_consumer_relations/1/result_token/root_identity/scope_location"
          },
          "scope_span": {
            "end_byte": 45854,
            "node_type": "statement_block",
            "start_byte": 44577
          },
          "value": {
            "heap_state_verified": false,
            "model": "captured_declaration_identity_only",
            "runtime_value_known": false,
            "stable": false,
            "reasons": [
              "binding_not_initialized_before_use",
              "declaration_initializer_or_binder_is_not_initialized_value",
              "write_and_effect_review_not_requested"
            ]
          }
        }
      }
    },
    {
      "source_fact_refs": [
        "/functional_chains/0/source_facts/573"
      ],
      "authenticated_call_edge_id": "42f5930009847b452ea8c50d",
      "authenticated_call_fact_id": "0e08deaab546c9aab1dba0db",
      "id": "348bc3de785125d2d43e2225",
      "kind": "lifecycle_nullable_context_consumer_rejection",
      "operator": "===",
      "origin": "source-derived",
      "provider_source_fact_id": "1593851adfff87722fb39964",
      "relation_component": "captured-lifecycle-ownership-relations-1",
      "runtime_scope_authorization_or_selected_scope_validity_proven": false,
      "selected_role": "renderDevice",
      "source_model": "browser-continuation-guard-source-v1",
      "abrupt_location": {
        "file": "apps/client/src/application.ts",
        "line": 1118,
        "column": 27,
        "end_line": 1118,
        "start_byte": 46074,
        "end_byte": 46080,
        "full_location_ref": "/functional_chains/0/pattern/nullable_context_consumer_relations/2/abrupt_location"
      },
      "lexical_source_owner": {
        "graph_node_id": "ts:apps/client/src/application#mountWinWinCodeClient.renderDevice",
        "symbol": "mountWinWinCodeClient.renderDevice",
        "location": {
          "file": "apps/client/src/application.ts",
          "line": 1116,
          "column": 3,
          "end_line": 1138,
          "start_byte": 45935,
          "end_byte": 46790,
          "full_location_ref": "/functional_chains/0/pattern/nullable_context_consumer_relations/2/lexical_source_owner/location"
        }
      },
      "location": {
        "file": "apps/client/src/application.ts",
        "line": 1118,
        "column": 5,
        "end_line": 1118,
        "start_byte": 46052,
        "end_byte": 46080,
        "full_location_ref": "/functional_chains/0/pattern/nullable_context_consumer_relations/2/location"
      },
      "result_token": {
        "root_declaration_id": "825134f0c64dc652d72da4ba2a0ddee5ce1af703e23e295e81c0d96c237fbda0",
        "root_name": "context",
        "runtime_resource_identity_proven": false,
        "members": [],
        "root_declaration_location": {
          "file": "apps/client/src/application.ts",
          "line": 1117,
          "column": 11,
          "end_line": 1117,
          "start_byte": 46010,
          "end_byte": 46047,
          "full_location_ref": "/functional_chains/0/pattern/nullable_context_consumer_relations/2/result_token/root_declaration_location"
        },
        "root_identity": {
          "binding_id": "825134f0c64dc652d72da4ba2a0ddee5ce1af703e23e295e81c0d96c237fbda0",
          "declaration_id": "825134f0c64dc652d72da4ba2a0ddee5ce1af703e23e295e81c0d96c237fbda0",
          "declaration_kind": "const",
          "file": "apps/client/src/application.ts",
          "identity_api_version": "captured-declaration-identity-only-1",
          "identity_complete": true,
          "import": null,
          "name": "context",
          "parameter_index": null,
          "reader_version": "static-value-contracts-1",
          "state": "unique",
          "version": "captured-lexical-bindings-3",
          "write_and_effect_review_performed": false,
          "binder_location": {
            "file": "apps/client/src/application.ts",
            "line": 1117,
            "column": 11,
            "end_line": 1117,
            "start_byte": 46010,
            "end_byte": 46017,
            "full_location_ref": "/functional_chains/0/pattern/nullable_context_consumer_relations/2/result_token/root_identity/binder_location"
          },
          "binder_span": {
            "end_byte": 46017,
            "node_type": "identifier",
            "start_byte": 46010
          },
          "declaration_location": {
            "file": "apps/client/src/application.ts",
            "line": 1117,
            "column": 11,
            "end_line": 1117,
            "start_byte": 46010,
            "end_byte": 46047,
            "full_location_ref": "/functional_chains/0/pattern/nullable_context_consumer_relations/2/result_token/root_identity/declaration_location"
          },
          "declaration_span": {
            "end_byte": 46047,
            "node_type": "variable_declarator",
            "start_byte": 46010
          },
          "gaps": [],
          "limitations": [
            "identity denotes a captured lexical declaration, not an object/resource or alias identity",
            "no reaching values, target activation, hidden calls or external heap mutation are proved",
            "write records include captured syntax and possible effects, not executed writes"
          ],
          "pattern_path": [],
          "scope_location": {
            "file": "apps/client/src/application.ts",
            "line": 1116,
            "column": 66,
            "end_line": 1138,
            "start_byte": 45998,
            "end_byte": 46790,
            "full_location_ref": "/functional_chains/0/pattern/nullable_context_consumer_relations/2/result_token/root_identity/scope_location"
          },
          "scope_span": {
            "end_byte": 46790,
            "node_type": "statement_block",
            "start_byte": 45998
          },
          "value": {
            "heap_state_verified": false,
            "model": "captured_declaration_identity_only",
            "runtime_value_known": false,
            "stable": false,
            "reasons": [
              "binding_not_initialized_before_use",
              "declaration_initializer_or_binder_is_not_initialized_value",
              "write_and_effect_review_not_requested"
            ]
          }
        }
      }
    },
    {
      "source_fact_refs": [
        "/functional_chains/0/source_facts/574"
      ],
      "authenticated_call_edge_id": "f5d97e594567e24514a1c9e5",
      "authenticated_call_fact_id": "1af92e062ebd86f16753fa1b",
      "id": "9400ebb4b5b102aca74ce327",
      "kind": "lifecycle_nullable_context_consumer_rejection",
      "operator": "===",
      "origin": "source-derived",
      "provider_source_fact_id": "1593851adfff87722fb39964",
      "relation_component": "captured-lifecycle-ownership-relations-1",
      "runtime_scope_authorization_or_selected_scope_validity_proven": false,
      "selected_role": "renderSettings",
      "source_model": "browser-continuation-guard-source-v1",
      "abrupt_location": {
        "file": "apps/client/src/application.ts",
        "line": 1160,
        "column": 27,
        "end_line": 1160,
        "start_byte": 47777,
        "end_byte": 47783,
        "full_location_ref": "/functional_chains/0/pattern/nullable_context_consumer_relations/3/abrupt_location"
      },
      "lexical_source_owner": {
        "graph_node_id": "ts:apps/client/src/application#mountWinWinCodeClient.renderSettings",
        "symbol": "mountWinWinCodeClient.renderSettings",
        "location": {
          "file": "apps/client/src/application.ts",
          "line": 1158,
          "column": 3,
          "end_line": 1223,
          "start_byte": 47636,
          "end_byte": 50073,
          "full_location_ref": "/functional_chains/0/pattern/nullable_context_consumer_relations/3/lexical_source_owner/location"
        }
      },
      "location": {
        "file": "apps/client/src/application.ts",
        "line": 1160,
        "column": 5,
        "end_line": 1160,
        "start_byte": 47755,
        "end_byte": 47783,
        "full_location_ref": "/functional_chains/0/pattern/nullable_context_consumer_relations/3/location"
      },
      "result_token": {
        "remaining_fields_ref": "/functional_chains/0/pattern/nullable_context_consumer_relations/3/result_token"
      }
    }
  ],
  "shown_count": 4,
  "total_count": 10,
  "truncated": true,
  "full_value_ref": "/functional_chains/0/pattern/nullable_context_consumer_relations"
}
```

**post_suspension_without_local_guard_fact_ids**：`/functional_chains/0/pattern/post_suspension_without_local_guard_fact_ids`；展示截断：`true`。

```json
{
  "shown_items": [
    "67b43452909a6e50eb56db7f",
    "93c68d1e1f5ea355fda5f1a0",
    "82bb236573dc58fec2448060",
    "57bfb73007689984cd1dc242",
    "5960009dcecc05e57e9cafad",
    "3f1dffdcc3b631a47ec1b8c4"
  ],
  "shown_count": 6,
  "total_count": 25,
  "truncated": true,
  "full_value_ref": "/functional_chains/0/pattern/post_suspension_without_local_guard_fact_ids"
}
```

**scope_conditions**：`/functional_chains/0/pattern/scope_conditions`；展示截断：`false`。

```json
[
  "selected captured callables and nested callbacks are invoked and their recorded branches are reached normally",
  "generation tokens compare captured lexical declarations, without asserting current counter values",
  "standard AbortController/DOM behavior is an explicit source model, not observed browser behavior",
  "a parent guard is never inherited across a nested callback or an intervening suspension"
]
```

**unreviewed_scope**：`/functional_chains/0/pattern/unreviewed_scope`；展示截断：`false`。

```json
[
  "complete browser event ordering and activation",
  "opaque imported mounts and subscriptions",
  "all DOM effects, underlying network cancellation, hidden aliases and arbitrary callback reentrancy"
]
```

**without_local_guard_publication_fact_ids**：`/functional_chains/0/pattern/without_local_guard_publication_fact_ids`；展示截断：`true`。

```json
{
  "shown_items": [
    "67b43452909a6e50eb56db7f",
    "cb223dea72af7c462be2e88f",
    "450914f5c149d683278bba7a",
    "f0c5b76904128b3d6cd1aa02",
    "a132a1841d4579a51a844f79",
    "ebd274d99a22f7c71356ba50"
  ],
  "shown_count": 6,
  "total_count": 122,
  "truncated": true,
  "full_value_ref": "/functional_chains/0/pattern/without_local_guard_publication_fact_ids"
}
```

自动关系类型：`{"captured_call_step": 475, "lifecycle_conditional_abrupt_guard": 37, "lifecycle_continuation_publication_source": 317, "lifecycle_controller_installed_in_captured_slot": 11, "lifecycle_counter_increment_source": 5, "lifecycle_counter_token_capture_source": 1, "lifecycle_disposal_source_call": 47, "lifecycle_generation_argument_to_selected_callable": 25, "lifecycle_nullable_context_consumer_rejection": 10, "lifecycle_nullable_context_record_provider": 1, "lifecycle_standard_controller_source_construction": 11, "lifecycle_truthy_invalidation_source": 24, "lifecycle_truthy_result_disposal_consumer": 1, "report_source_role": 19}`。

分析缺口：

```json
[]
```

条件与反证声明（单列为配置范围，不冒充源码证据）：

```json
{
  "applicability": {
    "conditions": [
      "Selected captured definitions are activated, recorded branches are reached normally, and explicit finite source models apply."
    ],
    "counterexamples": [
      "Nested callbacks, opaque effects and deployment branches are not promoted to active runtime guarantees."
    ],
    "kind": "conditional"
  },
  "descriptive_counterexamples_are_computed_evidence": false,
  "origin": "policy-declared",
  "provenance": {
    "author_approved": false,
    "authority": "original-full-report-source-scope",
    "note": "Selectors locate saved declarations only; no expected guard, writer, resource or result is supplied.",
    "source_doc": "reports/astra-baseline/WINWINCODE_ANALYSIS.md"
  }
}
```

### wwc-captured-record-resource-writers

类型：`resource_writer_ownership`；源码关系评估：`scoped_source_relations_supported`。

保存发现：`503cd6d9621e80a371620dea`；证据：`270c257e5b3bbfbff83b79b9`。

- `browserShell`：`apps/client/src/application.ts` / `mountWinWinCodeClient`。
- `browserRender`：`apps/client/src/application.ts` / `mountWinWinCodeClient.performRender`。
- `workRunStart`：`crates/winwincode-delivery/src/application/workrun.rs` / `WorkRunAggregate.start_item`。
- `workerDispatch`：`crates/winwincode-worker/src/lib.rs` / `WorkerMain.accept_dispatch`。
- `adapterSubmit`：`crates/winwincode-codex/src/adapter.rs` / `<ProductionCodexAdapter as CodexCoreAdapter>.submit_turn`。
- `adapterPersist`：`crates/winwincode-codex/src/adapter.rs` / `ProductionCodexAdapter.persist_run`。
- `kernelSession`：`crates/kernel/src/lib.rs` / `Kernel.create_session`。
- `kernelTurn`：`crates/kernel/src/lib.rs` / `Kernel.submit_turn`。

保存关系的展示摘要（`presentation_only=true`；不新增评级）：

完整 pattern：`/functional_chains/1/pattern`。展示截断：`true`；完整证据与原 pattern 保留。

| 保存字段 | 实际值 | 完整引用 |
| --- | --- | --- |
| all_mutations_authorized_proven | false | /functional_chains/1/pattern/all_mutations_authorized_proven |
| all_storage_resources_bound_proven | false | /functional_chains/1/pattern/all_storage_resources_bound_proven |
| canonical_authority_proven | false | /functional_chains/1/pattern/canonical_authority_proven |
| ownership_assessment | partial_captured_writers_and_consumers | /functional_chains/1/pattern/ownership_assessment |
| relation_component_version | captured-lifecycle-ownership-relations-1 | /functional_chains/1/pattern/relation_component_version |
| responsibility_interpretation | Selected captured functions write the recorded lexical fields and pass the recorded arguments; directory names assign no responsibility. | /functional_chains/1/pattern/responsibility_interpretation |
| scoped_source_supported | true | /functional_chains/1/pattern/scoped_source_supported |
| unique_fact_owner_proven | false | /functional_chains/1/pattern/unique_fact_owner_proven |
| whole_repository_ownership_inferred | false | /functional_chains/1/pattern/whole_repository_ownership_inferred |

**call_record_and_effect_frontiers**：`/functional_chains/1/pattern/call_record_and_effect_frontiers`；展示截断：`true`。

```json
{
  "shown_items": [
    {
      "activation_and_physical_effect_proven": false,
      "authenticated_call_edge_id": "e3f0645515e3b509073e48cf",
      "authenticated_callee_graph_node_id": "ts:apps/client/src/preferences#mountPreferences",
      "captured_callee_source": "mountPreferences",
      "captured_receiver_token": null,
      "role": "browserShell",
      "source_call_fact_id": "d87fe1e538142cf765f00c18",
      "arguments": [
        {
          "kind": "identifier",
          "name": "browser",
          "location": {
            "file": "apps/client/src/application.ts",
            "line": 195,
            "column": 45,
            "end_line": 195,
            "start_byte": 6970,
            "end_byte": 6977,
            "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/0/arguments/0/location"
          },
          "reference": {
            "declaration_id": "a630274c69c7be85924cdb035d7ad3c07851a1779230f75602892a9483d4b653",
            "declaration_kind": "const",
            "identity_complete": true,
            "parameter_index": null,
            "state": "unique",
            "binder_location": {
              "file": "apps/client/src/application.ts",
              "line": 193,
              "column": 9,
              "end_line": 193,
              "start_byte": 6845,
              "end_byte": 6852,
              "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/0/arguments/0/reference/binder_location"
            },
            "declaration_location": {
              "file": "apps/client/src/application.ts",
              "line": 193,
              "column": 9,
              "end_line": 193,
              "start_byte": 6845,
              "end_byte": 6879,
              "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/0/arguments/0/reference/declaration_location"
            }
          }
        },
        {
          "kind": "identifier",
          "name": "document",
          "location": {
            "file": "apps/client/src/application.ts",
            "line": 195,
            "column": 54,
            "end_line": 195,
            "start_byte": 6979,
            "end_byte": 6987,
            "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/0/arguments/1/location"
          },
          "reference": {
            "declaration_id": "152e4042ad24438e61857ffdd66165398cf74e30c96afc15a8c4e593b527ba11",
            "declaration_kind": "const",
            "identity_complete": true,
            "parameter_index": null,
            "state": "unique",
            "binder_location": {
              "file": "apps/client/src/application.ts",
              "line": 194,
              "column": 9,
              "end_line": 194,
              "start_byte": 6888,
              "end_byte": 6896,
              "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/0/arguments/1/reference/binder_location"
            },
            "declaration_location": {
              "file": "apps/client/src/application.ts",
              "line": 194,
              "column": 9,
              "end_line": 194,
              "start_byte": 6888,
              "end_byte": 6925,
              "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/0/arguments/1/reference/declaration_location"
            }
          }
        }
      ]
    },
    {
      "activation_and_physical_effect_proven": false,
      "authenticated_call_edge_id": "efd491a39a3ab74fa0977289",
      "authenticated_callee_graph_node_id": "ts:apps/client/src/core/connection-state#createConnectionMonitor",
      "captured_callee_source": "createConnectionMonitor",
      "captured_receiver_token": null,
      "role": "browserShell",
      "source_call_fact_id": "17dc2a6d358487f6e1e2b4bc",
      "arguments": [
        {
          "kind": "object",
          "construction": {
            "fixed_data_source_shape_complete": true,
            "runtime_object_or_presence_proven": false,
            "fields": {
              "now": {
                "key": "now",
                "location": {
                  "file": "apps/client/src/application.ts",
                  "line": 197,
                  "column": 48,
                  "end_line": 197,
                  "start_byte": 7098,
                  "end_byte": 7101,
                  "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/1/arguments/0/construction/fields/now/location"
                },
                "value": {
                  "kind": "shorthand_property_identifier",
                  "name": "now",
                  "location": {
                    "file": "apps/client/src/application.ts",
                    "line": 197,
                    "column": 48,
                    "end_line": 197,
                    "start_byte": 7098,
                    "end_byte": 7101,
                    "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/1/arguments/0/construction/fields/now/value/location"
                  },
                  "reference": {
                    "declaration_id": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/1/arguments/0/construction/fields/now/value/reference/declaration_id"
                    },
                    "declaration_kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/1/arguments/0/construction/fields/now/value/reference/declaration_kind"
                    },
                    "identity_complete": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/1/arguments/0/construction/fields/now/value/reference/identity_complete"
                    },
                    "parameter_index": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/1/arguments/0/construction/fields/now/value/reference/parameter_index"
                    },
                    "state": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/1/arguments/0/construction/fields/now/value/reference/state"
                    },
                    "binder_location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/1/arguments/0/construction/fields/now/value/reference/binder_location"
                    },
                    "declaration_location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/1/arguments/0/construction/fields/now/value/reference/declaration_location"
                    }
                  }
                }
              }
            },
            "parts": [
              {
                "key": "now",
                "location": {
                  "file": "apps/client/src/application.ts",
                  "line": 197,
                  "column": 48,
                  "end_line": 197,
                  "start_byte": 7098,
                  "end_byte": 7101,
                  "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/1/arguments/0/construction/parts/0/location"
                },
                "value": {
                  "kind": "shorthand_property_identifier",
                  "name": "now",
                  "location": {
                    "file": "apps/client/src/application.ts",
                    "line": 197,
                    "column": 48,
                    "end_line": 197,
                    "start_byte": 7098,
                    "end_byte": 7101,
                    "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/1/arguments/0/construction/parts/0/value/location"
                  },
                  "reference": {
                    "declaration_id": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/1/arguments/0/construction/parts/0/value/reference/declaration_id"
                    },
                    "declaration_kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/1/arguments/0/construction/parts/0/value/reference/declaration_kind"
                    },
                    "identity_complete": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/1/arguments/0/construction/parts/0/value/reference/identity_complete"
                    },
                    "parameter_index": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/1/arguments/0/construction/parts/0/value/reference/parameter_index"
                    },
                    "state": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/1/arguments/0/construction/parts/0/value/reference/state"
                    },
                    "binder_location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/1/arguments/0/construction/parts/0/value/reference/binder_location"
                    },
                    "declaration_location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/1/arguments/0/construction/parts/0/value/reference/declaration_location"
                    }
                  }
                }
              }
            ]
          },
          "location": {
            "file": "apps/client/src/application.ts",
            "line": 197,
            "column": 46,
            "end_line": 197,
            "start_byte": 7096,
            "end_byte": 7103,
            "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/1/arguments/0/location"
          }
        }
      ]
    },
    {
      "activation_and_physical_effect_proven": false,
      "authenticated_call_edge_id": "a20a95bab05f39373efeeb80",
      "authenticated_callee_graph_node_id": "ts:apps/client/src/application#browserControlPlaneTransport",
      "captured_callee_source": "browserControlPlaneTransport",
      "captured_receiver_token": null,
      "role": "browserShell",
      "source_call_fact_id": "d7fb1a7754231519acb79136",
      "arguments": [
        {
          "kind": "identifier",
          "name": "browser",
          "location": {
            "file": "apps/client/src/application.ts",
            "line": 204,
            "column": 57,
            "end_line": 204,
            "start_byte": 7454,
            "end_byte": 7461,
            "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/2/arguments/0/location"
          },
          "reference": {
            "declaration_id": "a630274c69c7be85924cdb035d7ad3c07851a1779230f75602892a9483d4b653",
            "declaration_kind": "const",
            "identity_complete": true,
            "parameter_index": null,
            "state": "unique",
            "binder_location": {
              "file": "apps/client/src/application.ts",
              "line": 193,
              "column": 9,
              "end_line": 193,
              "start_byte": 6845,
              "end_byte": 6852,
              "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/2/arguments/0/reference/binder_location"
            },
            "declaration_location": {
              "file": "apps/client/src/application.ts",
              "line": 193,
              "column": 9,
              "end_line": 193,
              "start_byte": 6845,
              "end_byte": 6879,
              "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/2/arguments/0/reference/declaration_location"
            }
          }
        }
      ]
    },
    {
      "activation_and_physical_effect_proven": false,
      "authenticated_call_edge_id": "d44e4fd6c56ef0fcaeec750f",
      "authenticated_callee_graph_node_id": "ts:apps/client/src/community-control-plane-client#createControlPlaneClient",
      "captured_callee_source": "createControlPlaneClient",
      "captured_receiver_token": null,
      "role": "browserShell",
      "source_call_fact_id": "4616c032db91ef0fb204b951",
      "arguments": [
        {
          "kind": "object",
          "construction": {
            "fixed_data_source_shape_complete": false,
            "runtime_object_or_presence_proven": false,
            "fields": {
              "serverUrl": {
                "key": "serverUrl",
                "location": {
                  "file": "apps/client/src/application.ts",
                  "line": 206,
                  "column": 5,
                  "end_line": 206,
                  "start_byte": 7544,
                  "end_byte": 7572,
                  "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/fields/serverUrl/location"
                },
                "value": {
                  "current_referent_value_proven": false,
                  "kind": "member_expression",
                  "member": "serverUrl",
                  "location": {
                    "file": "apps/client/src/application.ts",
                    "line": 206,
                    "column": 16,
                    "end_line": 206,
                    "start_byte": 7555,
                    "end_byte": 7572,
                    "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/fields/serverUrl/value/location"
                  },
                  "member_location": {
                    "file": "apps/client/src/application.ts",
                    "line": 206,
                    "column": 24,
                    "end_line": 206,
                    "start_byte": 7563,
                    "end_byte": 7572,
                    "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/fields/serverUrl/value/member_location"
                  },
                  "object": {
                    "kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/fields/serverUrl/value/object/kind"
                    },
                    "name": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/fields/serverUrl/value/object/name"
                    },
                    "location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/fields/serverUrl/value/object/location"
                    },
                    "reference": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/fields/serverUrl/value/object/reference"
                    }
                  }
                }
              },
              "transport": {
                "key": "transport",
                "location": {
                  "file": "apps/client/src/application.ts",
                  "line": 207,
                  "column": 5,
                  "end_line": 207,
                  "start_byte": 7578,
                  "end_byte": 7605,
                  "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/fields/transport/location"
                },
                "value": {
                  "kind": "identifier",
                  "name": "browserTransport",
                  "location": {
                    "file": "apps/client/src/application.ts",
                    "line": 207,
                    "column": 16,
                    "end_line": 207,
                    "start_byte": 7589,
                    "end_byte": 7605,
                    "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/fields/transport/value/location"
                  },
                  "reference": {
                    "declaration_id": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/fields/transport/value/reference/declaration_id"
                    },
                    "declaration_kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/fields/transport/value/reference/declaration_kind"
                    },
                    "identity_complete": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/fields/transport/value/reference/identity_complete"
                    },
                    "parameter_index": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/fields/transport/value/reference/parameter_index"
                    },
                    "state": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/fields/transport/value/reference/state"
                    },
                    "binder_location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/fields/transport/value/reference/binder_location"
                    },
                    "declaration_location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/fields/transport/value/reference/declaration_location"
                    }
                  }
                }
              }
            },
            "parts": [
              {
                "key": "serverUrl",
                "location": {
                  "file": "apps/client/src/application.ts",
                  "line": 206,
                  "column": 5,
                  "end_line": 206,
                  "start_byte": 7544,
                  "end_byte": 7572,
                  "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/parts/0/location"
                },
                "value": {
                  "current_referent_value_proven": false,
                  "kind": "member_expression",
                  "member": "serverUrl",
                  "location": {
                    "file": "apps/client/src/application.ts",
                    "line": 206,
                    "column": 16,
                    "end_line": 206,
                    "start_byte": 7555,
                    "end_byte": 7572,
                    "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/parts/0/value/location"
                  },
                  "member_location": {
                    "file": "apps/client/src/application.ts",
                    "line": 206,
                    "column": 24,
                    "end_line": 206,
                    "start_byte": 7563,
                    "end_byte": 7572,
                    "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/parts/0/value/member_location"
                  },
                  "object": {
                    "kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/parts/0/value/object/kind"
                    },
                    "name": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/parts/0/value/object/name"
                    },
                    "location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/parts/0/value/object/location"
                    },
                    "reference": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/parts/0/value/object/reference"
                    }
                  }
                }
              },
              {
                "key": "transport",
                "location": {
                  "file": "apps/client/src/application.ts",
                  "line": 207,
                  "column": 5,
                  "end_line": 207,
                  "start_byte": 7578,
                  "end_byte": 7605,
                  "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/parts/1/location"
                },
                "value": {
                  "kind": "identifier",
                  "name": "browserTransport",
                  "location": {
                    "file": "apps/client/src/application.ts",
                    "line": 207,
                    "column": 16,
                    "end_line": 207,
                    "start_byte": 7589,
                    "end_byte": 7605,
                    "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/parts/1/value/location"
                  },
                  "reference": {
                    "declaration_id": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/parts/1/value/reference/declaration_id"
                    },
                    "declaration_kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/parts/1/value/reference/declaration_kind"
                    },
                    "identity_complete": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/parts/1/value/reference/identity_complete"
                    },
                    "parameter_index": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/parts/1/value/reference/parameter_index"
                    },
                    "state": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/parts/1/value/reference/state"
                    },
                    "binder_location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/parts/1/value/reference/binder_location"
                    },
                    "declaration_location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/parts/1/value/reference/declaration_location"
                    }
                  }
                }
              },
              {
                "kind": "method_definition",
                "value_unknown": true,
                "location": {
                  "file": "apps/client/src/application.ts",
                  "line": 208,
                  "column": 5,
                  "end_line": 210,
                  "start_byte": 7611,
                  "end_byte": 7699,
                  "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/construction/parts/2/location"
                }
              }
            ]
          },
          "location": {
            "file": "apps/client/src/application.ts",
            "line": 205,
            "column": 76,
            "end_line": 211,
            "start_byte": 7538,
            "end_byte": 7704,
            "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/3/arguments/0/location"
          }
        }
      ]
    },
    {
      "activation_and_physical_effect_proven": false,
      "authenticated_call_edge_id": "f515c1c7ea793b3e30855cd2",
      "authenticated_callee_graph_node_id": "ts:apps/client/src/core/connection-state#observeControlPlaneClient",
      "captured_callee_source": "observeControlPlaneClient",
      "captured_receiver_token": null,
      "role": "browserShell",
      "source_call_fact_id": "111dc7c35942a4729be02f96",
      "arguments": [
        {
          "kind": "object",
          "construction": {
            "fixed_data_source_shape_complete": false,
            "runtime_object_or_presence_proven": false,
            "fields": {
              "client": {
                "key": "client",
                "location": {
                  "file": "apps/client/src/application.ts",
                  "line": 213,
                  "column": 5,
                  "end_line": 213,
                  "start_byte": 7769,
                  "end_byte": 7792,
                  "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/4/arguments/0/construction/fields/client/location"
                },
                "value": {
                  "kind": "identifier",
                  "name": "rawControlPlane",
                  "location": {
                    "file": "apps/client/src/application.ts",
                    "line": 213,
                    "column": 13,
                    "end_line": 213,
                    "start_byte": 7777,
                    "end_byte": 7792,
                    "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/4/arguments/0/construction/fields/client/value/location"
                  },
                  "reference": {
                    "declaration_id": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/4/arguments/0/construction/fields/client/value/reference/declaration_id"
                    },
                    "declaration_kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/4/arguments/0/construction/fields/client/value/reference/declaration_kind"
                    },
                    "identity_complete": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/4/arguments/0/construction/fields/client/value/reference/identity_complete"
                    },
                    "parameter_index": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/4/arguments/0/construction/fields/client/value/reference/parameter_index"
                    },
                    "state": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/4/arguments/0/construction/fields/client/value/reference/state"
                    },
                    "binder_location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/4/arguments/0/construction/fields/client/value/reference/binder_location"
                    },
                    "declaration_location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/4/arguments/0/construction/fields/client/value/reference/declaration_location"
                    }
                  }
                }
              },
              "monitor": {
                "key": "monitor",
                "location": {
                  "file": "apps/client/src/application.ts",
                  "line": 214,
                  "column": 5,
                  "end_line": 214,
                  "start_byte": 7798,
                  "end_byte": 7817,
                  "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/4/arguments/0/construction/fields/monitor/location"
                },
                "value": {
                  "kind": "identifier",
                  "name": "connection",
                  "location": {
                    "file": "apps/client/src/application.ts",
                    "line": 214,
                    "column": 14,
                    "end_line": 214,
                    "start_byte": 7807,
                    "end_byte": 7817,
                    "full_location_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/4/arguments/0/construction/fields/monitor/value/location"
                  },
                  "reference": {
                    "declaration_id": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/4/arguments/0/construction/fields/monitor/value/reference/declaration_id"
                    },
                    "declaration_kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/4/arguments/0/construction/fields/monitor/value/reference/declaration_kind"
                    },
                    "identity_complete": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/4/arguments/0/construction/fields/monitor/value/reference/identity_complete"
                    },
                    "parameter_index": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/4/arguments/0/construction/fields/monitor/value/reference/parameter_index"
                    },
                    "state": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/4/arguments/0/construction/fields/monitor/value/reference/state"
                    },
                    "remaining_fields_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/4/arguments/0/construction/fields/monitor/value/reference"
                  }
                }
              },
              "remaining_fields_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/4/arguments/0/construction/fields"
            },
            "remaining_fields_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/4/arguments/0/construction"
          },
          "remaining_fields_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers/4/arguments/0"
        }
      ]
    }
  ],
  "shown_count": 5,
  "total_count": 231,
  "truncated": true,
  "full_value_ref": "/functional_chains/1/pattern/call_record_and_effect_frontiers"
}
```

**captured_resource_writer_groups**：`/functional_chains/1/pattern/captured_resource_writer_groups`；展示截断：`true`。

```json
{
  "shown_items": [
    {
      "captured_root_declaration_id": "04f2681c5209b73876b181eaaaba94999fb8c19f480bba412bfafa50f68d15cc",
      "unique_owner_or_authorization_proven": false,
      "captured_members": [
        "dataset",
        "surface"
      ],
      "selected_writer_symbols": [
        "mountWinWinCodeClient.performRender"
      ],
      "writer_fact_ids": [
        "c0ab5234263f4b5085600c31"
      ]
    },
    {
      "captured_root_declaration_id": "04f2681c5209b73876b181eaaaba94999fb8c19f480bba412bfafa50f68d15cc",
      "unique_owner_or_authorization_proven": false,
      "captured_members": [
        "id"
      ],
      "selected_writer_symbols": [
        "mountWinWinCodeClient"
      ],
      "writer_fact_ids": [
        "abb780c4daf86061d37cda7d"
      ]
    },
    {
      "captured_root_declaration_id": "04f2681c5209b73876b181eaaaba94999fb8c19f480bba412bfafa50f68d15cc",
      "unique_owner_or_authorization_proven": false,
      "captured_members": [
        "tabIndex"
      ],
      "selected_writer_symbols": [
        "mountWinWinCodeClient"
      ],
      "writer_fact_ids": [
        "e0fd58df0b83235ee2e46228"
      ]
    },
    {
      "captured_root_declaration_id": "09b76f647aeacd6f85d742c5e7ce1164bd1d249d67ab4f40a7c90a201c30b028",
      "unique_owner_or_authorization_proven": false,
      "captured_members": [
        "href"
      ],
      "selected_writer_symbols": [
        "mountWinWinCodeClient"
      ],
      "writer_fact_ids": [
        "d99068bdebd8005a38c1c1ea"
      ]
    },
    {
      "captured_root_declaration_id": "09b76f647aeacd6f85d742c5e7ce1164bd1d249d67ab4f40a7c90a201c30b028",
      "unique_owner_or_authorization_proven": false,
      "captured_members": [
        "textContent"
      ],
      "selected_writer_symbols": [
        "mountWinWinCodeClient"
      ],
      "writer_fact_ids": [
        "6cfc9808bf34c7ba4838d045"
      ]
    },
    {
      "captured_root_declaration_id": "17ada5ae18a50ac7f384473b46d809b5e35327667ff593dbe09ed8e67af42e69",
      "unique_owner_or_authorization_proven": false,
      "captured_members": [
        "state"
      ],
      "selected_writer_symbols": [
        "WorkRunAggregate.start_item"
      ],
      "writer_fact_ids": [
        "f9a984708196740b44a83db1"
      ]
    }
  ],
  "shown_count": 6,
  "total_count": 41,
  "truncated": true,
  "full_value_ref": "/functional_chains/1/pattern/captured_resource_writer_groups"
}
```

**same_token_reference_fact_ids**：`/functional_chains/1/pattern/same_token_reference_fact_ids`；展示截断：`true`。

```json
{
  "shown_items": [
    "20162a6700c02f9a56296eb5",
    "af96bbb607efbe5b1563d708",
    "1fe17a3af88856637455a2b0",
    "82ddeb4a0d6962f4753c6ce2",
    "187765d0c22a86c1c3f52872",
    "6f8777138d1ec87445993efc"
  ],
  "shown_count": 6,
  "total_count": 133,
  "truncated": true,
  "full_value_ref": "/functional_chains/1/pattern/same_token_reference_fact_ids"
}
```

**source_rejection_guard_fact_ids**：`/functional_chains/1/pattern/source_rejection_guard_fact_ids`；展示截断：`false`。

```json
[
  "a449558218872bab9925c3a7"
]
```

**unreviewed_scope**：`/functional_chains/1/pattern/unreviewed_scope`；展示截断：`false`。

```json
[
  "aliases, interprocedural heap identity and external persistence semantics",
  "all writers outside selected declarations",
  "authorization and canonical authority contracts",
  "architectural documentation consistency and all deployment branches"
]
```

**writer_fact_ids**：`/functional_chains/1/pattern/writer_fact_ids`；展示截断：`true`。

```json
{
  "shown_items": [
    "0f1c73637992c47ae8c33b79",
    "78a8949f8a529731f0361286",
    "9db30e059c9e93d4467da217",
    "9d8b7643edc5b5519bba73d3",
    "5f17f4dce880335969f57340",
    "d99068bdebd8005a38c1c1ea"
  ],
  "shown_count": 6,
  "total_count": 52,
  "truncated": true,
  "full_value_ref": "/functional_chains/1/pattern/writer_fact_ids"
}
```

自动关系类型：`{"captured_call_step": 262, "report_source_role": 8, "resource_captured_record_construction": 1, "resource_captured_rejection_guard": 1, "resource_captured_same_token_reference": 133, "resource_captured_writer": 51}`。

分析缺口：

```json
[]
```

条件与反证声明（单列为配置范围，不冒充源码证据）：

```json
{
  "applicability": {
    "conditions": [
      "Selected captured definitions are activated, recorded branches are reached normally, and explicit finite source models apply."
    ],
    "counterexamples": [
      "Nested callbacks, opaque effects and deployment branches are not promoted to active runtime guarantees."
    ],
    "kind": "conditional"
  },
  "descriptive_counterexamples_are_computed_evidence": false,
  "origin": "policy-declared",
  "provenance": {
    "author_approved": false,
    "authority": "original-full-report-source-scope",
    "note": "Selectors locate saved declarations only; no expected guard, writer, resource or result is supplied.",
    "source_doc": "reports/astra-baseline/WINWINCODE_ANALYSIS.md"
  }
}
```

### wwc-report-adapter-durable-exact-turn

类型：`guarded_call_sequence`；源码关系评估：`scoped_source_relations_supported`。

保存发现：`247af23afa4ac8334a582bfa`；证据：`b647b91896ea10fd29a58bcf`。

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

保存关系的展示摘要（`presentation_only=true`；不新增评级）：

完整 pattern：`/functional_chains/2/pattern`。展示截断：`true`；完整证据与原 pattern 保留。

| 保存字段 | 实际值 | 完整引用 |
| --- | --- | --- |
| scoped_source_supported | true | /functional_chains/2/pattern/scoped_source_supported |

**nested_source_regions**：`/functional_chains/2/pattern/nested_source_regions`；展示截断：`false`。

```json
[]
```

**sequences**：`/functional_chains/2/pattern/sequences`；展示截断：`true`。

```json
{
  "adapter_submit": {
    "all_function_paths_or_effects_accounted": false,
    "future_or_callback_activation_proven": false,
    "region_kind": "function_item",
    "role": "adapter_submit",
    "assignment_attempts": [
      {
        "source_fact_refs": [
          "/functional_chains/2/source_facts/79"
        ],
        "id": "90d41e3430ab64ef75530f85",
        "kind": "ordered_source_assignment_attempt",
        "origin": "source-derived",
        "role": "adapter_submit",
        "write_runtime_success_proven": false,
        "branch_context": [
          {
            "activation_proven": false,
            "kind": "match_arm",
            "location": {
              "file": "crates/winwincode-codex/src/adapter.rs",
              "line": 3539,
              "column": 17,
              "end_line": 3539,
              "start_byte": 138925,
              "end_byte": 138988,
              "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/0/branch_context/0/location"
            }
          }
        ],
        "left": {
          "current_referent_value_proven": false,
          "kind": "field_expression",
          "member": "submission_digest",
          "location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 3539,
            "column": 25,
            "end_line": 3539,
            "start_byte": 138933,
            "end_byte": 138961,
            "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/0/left/location"
          },
          "member_location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 3539,
            "column": 36,
            "end_line": 3539,
            "start_byte": 138944,
            "end_byte": 138961,
            "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/0/left/member_location"
          },
          "object": {
            "current_referent_value_proven": false,
            "kind": "field_expression",
            "member": "record",
            "location": {
              "file": "crates/winwincode-codex/src/adapter.rs",
              "line": 3539,
              "column": 25,
              "end_line": 3539,
              "start_byte": 138933,
              "end_byte": 138943,
              "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/0/left/object/location"
            },
            "member_location": {
              "file": "crates/winwincode-codex/src/adapter.rs",
              "line": 3539,
              "column": 29,
              "end_line": 3539,
              "start_byte": 138937,
              "end_byte": 138943,
              "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/0/left/object/member_location"
            },
            "object": {
              "kind": "identifier",
              "name": "run",
              "location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3539,
                "column": 25,
                "end_line": 3539,
                "start_byte": 138933,
                "end_byte": 138936,
                "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/0/left/object/object/location"
              },
              "reference": {
                "declaration_id": "46f19d39a4a44d2dc15f248c582b6169450fe3aa5ae2b4f09e31982a822ef2a4",
                "declaration_kind": "captured_rust_local",
                "identity_scope": "plain captured binder syntax only",
                "macro_namespace_complete": false,
                "runtime_value_identity_proven": false,
                "state": "captured_unique_rust_binder",
                "binder_location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 3535,
                  "column": 17,
                  "end_line": 3535,
                  "start_byte": 138674,
                  "end_byte": 138677,
                  "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/0/left/object/object/reference/binder_location"
                },
                "declaration_location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 3535,
                  "column": 13,
                  "end_line": 3535,
                  "start_byte": 138670,
                  "end_byte": 138736,
                  "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/0/left/object/object/reference/declaration_location"
                }
              }
            }
          }
        },
        "location": {
          "file": "crates/winwincode-codex/src/adapter.rs",
          "line": 3539,
          "column": 25,
          "end_line": 3539,
          "start_byte": 138933,
          "end_byte": 138987,
          "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/0/location"
        },
        "right": {
          "call_effects_or_result_proven": false,
          "callee_source": "Some",
          "kind": "call_expression",
          "arguments": [
            {
              "kind": "identifier",
              "name": "submission_digest",
              "location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3539,
                "column": 61,
                "end_line": 3539,
                "start_byte": 138969,
                "end_byte": 138986,
                "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/0/right/arguments/0/location"
              },
              "reference": {
                "declaration_id": "32221372946c395335a991f6fdb3cbdc9eef00d47d745dd2860ac2c49bb1f12c",
                "declaration_kind": "captured_rust_local",
                "identity_scope": "plain captured binder syntax only",
                "macro_namespace_complete": false,
                "runtime_value_identity_proven": false,
                "state": "captured_unique_rust_binder",
                "binder_location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 3533,
                  "column": 13,
                  "end_line": 3533,
                  "start_byte": 138544,
                  "end_byte": 138561,
                  "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/0/right/arguments/0/reference/binder_location"
                },
                "declaration_location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 3533,
                  "column": 9,
                  "end_line": 3533,
                  "start_byte": 138540,
                  "end_byte": 138616,
                  "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/0/right/arguments/0/reference/declaration_location"
                }
              }
            }
          ],
          "callee_expression": {
            "kind": "identifier",
            "name": "Some",
            "location": {
              "file": "crates/winwincode-codex/src/adapter.rs",
              "line": 3539,
              "column": 56,
              "end_line": 3539,
              "start_byte": 138964,
              "end_byte": 138968,
              "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/0/right/callee_expression/location"
            },
            "reference": {
              "plain_binder_candidates": 0,
              "runtime_value_identity_proven": false,
              "state": "captured_rust_reference",
              "text": "Some",
              "location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3539,
                "column": 56,
                "end_line": 3539,
                "start_byte": 138964,
                "end_byte": 138968,
                "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/0/right/callee_expression/reference/location"
              }
            }
          },
          "location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 3539,
            "column": 56,
            "end_line": 3539,
            "start_byte": 138964,
            "end_byte": 138987,
            "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/0/right/location"
          }
        }
      },
      {
        "source_fact_refs": [
          "/functional_chains/2/source_facts/83"
        ],
        "id": "267f98d484f10511520a5d5d",
        "kind": "ordered_source_assignment_attempt",
        "origin": "source-derived",
        "role": "adapter_submit",
        "write_runtime_success_proven": false,
        "branch_context": [
          {
            "branch": "else",
            "condition_truth_proven": false,
            "kind": "if",
            "condition": {
              "kind": "binary_expression",
              "operator": "||",
              "runtime_predicate_or_assignment_proven": false,
              "location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3541,
                "column": 16,
                "end_line": 3545,
                "start_byte": 139018,
                "end_byte": 139272,
                "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/branch_context/0/condition/location"
              },
              "operands": [
                {
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/branch_context/0/condition/operands/0/kind"
                  },
                  "operator": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/branch_context/0/condition/operands/0/operator"
                  },
                  "runtime_predicate_or_assignment_proven": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/branch_context/0/condition/operands/0/runtime_predicate_or_assignment_proven"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/branch_context/0/condition/operands/0/location"
                  },
                  "operands": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/branch_context/0/condition/operands/0/operands"
                  }
                },
                {
                  "call_effects_or_result_proven": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/branch_context/0/condition/operands/1/call_effects_or_result_proven"
                  },
                  "callee_source": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/branch_context/0/condition/operands/1/callee_source"
                  },
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/branch_context/0/condition/operands/1/kind"
                  },
                  "arguments": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/branch_context/0/condition/operands/1/arguments"
                  },
                  "callee_expression": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/branch_context/0/condition/operands/1/callee_expression"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/branch_context/0/condition/operands/1/location"
                  }
                }
              ]
            },
            "location": {
              "file": "crates/winwincode-codex/src/adapter.rs",
              "line": 3541,
              "column": 13,
              "end_line": 3556,
              "start_byte": 139015,
              "end_byte": 139739,
              "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/branch_context/0/location"
            }
          },
          {
            "branch": "then",
            "condition_truth_proven": false,
            "kind": "if",
            "condition": {
              "kind": "binary_expression",
              "operator": "==",
              "runtime_predicate_or_assignment_proven": false,
              "location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3552,
                "column": 20,
                "end_line": 3552,
                "start_byte": 139530,
                "end_byte": 139574,
                "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/branch_context/1/condition/location"
              },
              "operands": [
                {
                  "current_referent_value_proven": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/branch_context/1/condition/operands/0/current_referent_value_proven"
                  },
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/branch_context/1/condition/operands/0/kind"
                  },
                  "member": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/branch_context/1/condition/operands/0/member"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/branch_context/1/condition/operands/0/location"
                  },
                  "member_location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/branch_context/1/condition/operands/0/member_location"
                  },
                  "object": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/branch_context/1/condition/operands/0/object"
                  }
                },
                {
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/branch_context/1/condition/operands/1/kind"
                  },
                  "source": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/branch_context/1/condition/operands/1/source"
                  },
                  "children": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/branch_context/1/condition/operands/1/children"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/branch_context/1/condition/operands/1/location"
                  }
                }
              ]
            },
            "location": {
              "file": "crates/winwincode-codex/src/adapter.rs",
              "line": 3552,
              "column": 17,
              "end_line": 3554,
              "start_byte": 139527,
              "end_byte": 139667,
              "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/branch_context/1/location"
            }
          }
        ],
        "left": {
          "current_referent_value_proven": false,
          "kind": "field_expression",
          "member": "phase",
          "location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 3553,
            "column": 21,
            "end_line": 3553,
            "start_byte": 139597,
            "end_byte": 139613,
            "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/left/location"
          },
          "member_location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 3553,
            "column": 32,
            "end_line": 3553,
            "start_byte": 139608,
            "end_byte": 139613,
            "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/left/member_location"
          },
          "object": {
            "current_referent_value_proven": false,
            "kind": "field_expression",
            "member": "record",
            "location": {
              "file": "crates/winwincode-codex/src/adapter.rs",
              "line": 3553,
              "column": 21,
              "end_line": 3553,
              "start_byte": 139597,
              "end_byte": 139607,
              "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/left/object/location"
            },
            "member_location": {
              "file": "crates/winwincode-codex/src/adapter.rs",
              "line": 3553,
              "column": 25,
              "end_line": 3553,
              "start_byte": 139601,
              "end_byte": 139607,
              "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/left/object/member_location"
            },
            "object": {
              "kind": "identifier",
              "name": "run",
              "location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3553,
                "column": 21,
                "end_line": 3553,
                "start_byte": 139597,
                "end_byte": 139600,
                "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/left/object/object/location"
              },
              "reference": {
                "declaration_id": "46f19d39a4a44d2dc15f248c582b6169450fe3aa5ae2b4f09e31982a822ef2a4",
                "declaration_kind": "captured_rust_local",
                "identity_scope": "plain captured binder syntax only",
                "macro_namespace_complete": false,
                "runtime_value_identity_proven": false,
                "state": "captured_unique_rust_binder",
                "binder_location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 3535,
                  "column": 17,
                  "end_line": 3535,
                  "start_byte": 138674,
                  "end_byte": 138677,
                  "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/left/object/object/reference/binder_location"
                },
                "declaration_location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 3535,
                  "column": 13,
                  "end_line": 3535,
                  "start_byte": 138670,
                  "end_byte": 138736,
                  "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/left/object/object/reference/declaration_location"
                }
              }
            }
          }
        },
        "location": {
          "file": "crates/winwincode-codex/src/adapter.rs",
          "line": 3553,
          "column": 21,
          "end_line": 3553,
          "start_byte": 139597,
          "end_byte": 139648,
          "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/location"
        },
        "right": {
          "kind": "scoped_identifier",
          "source": "StoredRunPhase::SubmissionIntent",
          "children": [
            {
              "kind": "identifier",
              "name": "StoredRunPhase",
              "location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3553,
                "column": 40,
                "end_line": 3553,
                "start_byte": 139616,
                "end_byte": 139630,
                "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/right/children/0/location"
              },
              "reference": {
                "plain_binder_candidates": 0,
                "runtime_value_identity_proven": false,
                "state": "captured_rust_reference",
                "text": "StoredRunPhase",
                "location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 3553,
                  "column": 40,
                  "end_line": 3553,
                  "start_byte": 139616,
                  "end_byte": 139630,
                  "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/right/children/0/reference/location"
                }
              }
            },
            {
              "kind": "identifier",
              "name": "SubmissionIntent",
              "location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3553,
                "column": 56,
                "end_line": 3553,
                "start_byte": 139632,
                "end_byte": 139648,
                "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/right/children/1/location"
              },
              "reference": {
                "plain_binder_candidates": 0,
                "runtime_value_identity_proven": false,
                "state": "captured_rust_reference",
                "text": "SubmissionIntent",
                "location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 3553,
                  "column": 56,
                  "end_line": 3553,
                  "start_byte": 139632,
                  "end_byte": 139648,
                  "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/right/children/1/reference/location"
                }
              }
            }
          ],
          "location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 3553,
            "column": 40,
            "end_line": 3553,
            "start_byte": 139616,
            "end_byte": 139648,
            "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/1/right/location"
          }
        }
      },
      {
        "source_fact_refs": [
          "/functional_chains/2/source_facts/94"
        ],
        "id": "e6c042f10dd9175e4d525b9f",
        "kind": "ordered_source_assignment_attempt",
        "origin": "source-derived",
        "role": "adapter_submit",
        "write_runtime_success_proven": false,
        "branch_context": [],
        "left": {
          "current_referent_value_proven": false,
          "kind": "field_expression",
          "member": "recovered",
          "location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 3623,
            "column": 9,
            "end_line": 3626,
            "start_byte": 142404,
            "end_byte": 142508,
            "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/2/left/location"
          },
          "member_location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 3626,
            "column": 14,
            "end_line": 3626,
            "start_byte": 142499,
            "end_byte": 142508,
            "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/2/left/member_location"
          },
          "object": {
            "kind": "try_expression",
            "location": {
              "file": "crates/winwincode-codex/src/adapter.rs",
              "line": 3623,
              "column": 9,
              "end_line": 3625,
              "start_byte": 142404,
              "end_byte": 142485,
              "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/2/left/object/location"
            },
            "operand": {
              "call_effects_or_result_proven": false,
              "callee_source": "self.runs\n            .get_mut(&run_key)\n            .ok_or_else",
              "kind": "call_expression",
              "arguments": [
                {
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/2/left/object/operand/arguments/0/kind"
                  },
                  "name": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/2/left/object/operand/arguments/0/name"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/2/left/object/operand/arguments/0/location"
                  },
                  "reference": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/2/left/object/operand/arguments/0/reference"
                  }
                }
              ],
              "callee_expression": {
                "current_referent_value_proven": false,
                "kind": "field_expression",
                "member": "ok_or_else",
                "location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 3623,
                  "column": 9,
                  "end_line": 3625,
                  "start_byte": 142404,
                  "end_byte": 142468,
                  "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/2/left/object/operand/callee_expression/location"
                },
                "member_location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 3625,
                  "column": 14,
                  "end_line": 3625,
                  "start_byte": 142458,
                  "end_byte": 142468,
                  "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/2/left/object/operand/callee_expression/member_location"
                },
                "object": {
                  "call_effects_or_result_proven": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/2/left/object/operand/callee_expression/object/call_effects_or_result_proven"
                  },
                  "callee_source": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/2/left/object/operand/callee_expression/object/callee_source"
                  },
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/2/left/object/operand/callee_expression/object/kind"
                  },
                  "arguments": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/2/left/object/operand/callee_expression/object/arguments"
                  },
                  "callee_expression": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/2/left/object/operand/callee_expression/object/callee_expression"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/2/left/object/operand/callee_expression/object/location"
                  }
                }
              },
              "location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3623,
                "column": 9,
                "end_line": 3625,
                "start_byte": 142404,
                "end_byte": 142484,
                "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/2/left/object/operand/location"
              }
            }
          }
        },
        "location": {
          "file": "crates/winwincode-codex/src/adapter.rs",
          "line": 3623,
          "column": 9,
          "end_line": 3626,
          "start_byte": 142404,
          "end_byte": 142516,
          "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/2/location"
        },
        "right": {
          "kind": "boolean_literal",
          "literal": false,
          "location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 3626,
            "column": 26,
            "end_line": 3626,
            "start_byte": 142511,
            "end_byte": 142516,
            "full_location_ref": "/functional_chains/2/pattern/sequences/adapter_submit/assignment_attempts/2/right/location"
          }
        }
      }
    ],
    "call_result_guard_source_links": [],
    "remaining_fields_ref": "/functional_chains/2/pattern/sequences/adapter_submit"
  }
}
```

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

保存发现：`79ca6cc3908f5919d3b7d573`；证据：`19318bbcec3b472c92535c6f`。

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

保存关系的展示摘要（`presentation_only=true`；不新增评级）：

完整 pattern：`/functional_chains/3/pattern`。展示截断：`true`；完整证据与原 pattern 保留。

| 保存字段 | 实际值 | 完整引用 |
| --- | --- | --- |
| scoped_source_supported | true | /functional_chains/3/pattern/scoped_source_supported |

**nested_source_regions**：`/functional_chains/3/pattern/nested_source_regions`；展示截断：`false`。

```json
[]
```

**sequences**：`/functional_chains/3/pattern/sequences`；展示截断：`true`。

```json
{
  "builder": {
    "all_function_paths_or_effects_accounted": false,
    "future_or_callback_activation_proven": false,
    "region_kind": "function_declaration",
    "role": "builder",
    "assignment_attempts": {
      "shown_items": [
        {
          "source_fact_refs": [
            "/functional_chains/3/source_facts/90"
          ],
          "id": "712074bcce14b56c9ed1a503",
          "kind": "ordered_source_assignment_attempt",
          "origin": "source-derived",
          "role": "builder",
          "write_runtime_success_proven": false,
          "branch_context": [
            {
              "branch": "then",
              "condition_truth_proven": false,
              "kind": "if",
              "condition": {
                "kind": "binary_expression",
                "operator": "===",
                "runtime_predicate_or_assignment_proven": false,
                "location": {
                  "file": "apps/client/src/chat-delivery-creator.ts",
                  "line": 226,
                  "column": 9,
                  "end_line": 226,
                  "start_byte": 7690,
                  "end_byte": 7706,
                  "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/branch_context/0/condition/location"
                },
                "operands": [
                  {
                    "kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/branch_context/0/condition/operands/0/kind"
                    },
                    "name": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/branch_context/0/condition/operands/0/name"
                    },
                    "location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/branch_context/0/condition/operands/0/location"
                    },
                    "reference": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/branch_context/0/condition/operands/0/reference"
                    }
                  },
                  {
                    "kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/branch_context/0/condition/operands/1/kind"
                    },
                    "runtime_value_proven": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/branch_context/0/condition/operands/1/runtime_value_proven"
                    },
                    "source": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/branch_context/0/condition/operands/1/source"
                    },
                    "source_truncated": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/branch_context/0/condition/operands/1/source_truncated"
                    },
                    "location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/branch_context/0/condition/operands/1/location"
                    }
                  }
                ]
              },
              "location": {
                "file": "apps/client/src/chat-delivery-creator.ts",
                "line": 226,
                "column": 5,
                "end_line": 260,
                "start_byte": 7686,
                "end_byte": 8851,
                "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/branch_context/0/location"
              }
            }
          ],
          "left": {
            "kind": "identifier",
            "name": "attempt",
            "location": {
              "file": "apps/client/src/chat-delivery-creator.ts",
              "line": 228,
              "column": 7,
              "end_line": 228,
              "start_byte": 7766,
              "end_byte": 7773,
              "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/left/location"
            },
            "reference": {
              "declaration_id": "aced738e30031213c858a972d61acc4aab8aa48712156a5a9e4d037683191e5d",
              "declaration_kind": "let",
              "identity_complete": true,
              "parameter_index": null,
              "state": "unique",
              "binder_location": {
                "file": "apps/client/src/chat-delivery-creator.ts",
                "line": 130,
                "column": 7,
                "end_line": 130,
                "start_byte": 4155,
                "end_byte": 4162,
                "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/left/reference/binder_location"
              },
              "declaration_location": {
                "file": "apps/client/src/chat-delivery-creator.ts",
                "line": 130,
                "column": 7,
                "end_line": 136,
                "start_byte": 4155,
                "end_byte": 4383,
                "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/left/reference/declaration_location"
              }
            }
          },
          "location": {
            "file": "apps/client/src/chat-delivery-creator.ts",
            "line": 228,
            "column": 7,
            "end_line": 259,
            "start_byte": 7766,
            "end_byte": 8845,
            "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/location"
          },
          "right": {
            "kind": "object",
            "construction": {
              "fixed_data_source_shape_complete": true,
              "runtime_object_or_presence_proven": false,
              "fields": {
                "createRequest": {
                  "key": "createRequest",
                  "location": {
                    "file": "apps/client/src/chat-delivery-creator.ts",
                    "line": 230,
                    "column": 9,
                    "end_line": 257,
                    "start_byte": 7804,
                    "end_byte": 8813,
                    "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/fields/createRequest/location"
                  },
                  "value": {
                    "kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/fields/createRequest/value/kind"
                    },
                    "construction": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/fields/createRequest/value/construction"
                    },
                    "location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/fields/createRequest/value/location"
                    }
                  }
                },
                "created": {
                  "key": "created",
                  "location": {
                    "file": "apps/client/src/chat-delivery-creator.ts",
                    "line": 258,
                    "column": 9,
                    "end_line": 258,
                    "start_byte": 8823,
                    "end_byte": 8836,
                    "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/fields/created/location"
                  },
                  "value": {
                    "kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/fields/created/value/kind"
                    },
                    "runtime_value_proven": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/fields/created/value/runtime_value_proven"
                    },
                    "source": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/fields/created/value/source"
                    },
                    "source_truncated": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/fields/created/value/source_truncated"
                    },
                    "location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/fields/created/value/location"
                    }
                  }
                },
                "inputKey": {
                  "key": "inputKey",
                  "location": {
                    "file": "apps/client/src/chat-delivery-creator.ts",
                    "line": 229,
                    "column": 9,
                    "end_line": 229,
                    "start_byte": 7786,
                    "end_byte": 7794,
                    "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/fields/inputKey/location"
                  },
                  "value": {
                    "kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/fields/inputKey/value/kind"
                    },
                    "name": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/fields/inputKey/value/name"
                    },
                    "location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/fields/inputKey/value/location"
                    },
                    "reference": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/fields/inputKey/value/reference"
                    }
                  }
                }
              },
              "parts": [
                {
                  "key": "inputKey",
                  "location": {
                    "file": "apps/client/src/chat-delivery-creator.ts",
                    "line": 229,
                    "column": 9,
                    "end_line": 229,
                    "start_byte": 7786,
                    "end_byte": 7794,
                    "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/parts/0/location"
                  },
                  "value": {
                    "kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/parts/0/value/kind"
                    },
                    "name": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/parts/0/value/name"
                    },
                    "location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/parts/0/value/location"
                    },
                    "reference": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/parts/0/value/reference"
                    }
                  }
                },
                {
                  "key": "createRequest",
                  "location": {
                    "file": "apps/client/src/chat-delivery-creator.ts",
                    "line": 230,
                    "column": 9,
                    "end_line": 257,
                    "start_byte": 7804,
                    "end_byte": 8813,
                    "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/parts/1/location"
                  },
                  "value": {
                    "kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/parts/1/value/kind"
                    },
                    "construction": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/parts/1/value/construction"
                    },
                    "location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/parts/1/value/location"
                    }
                  }
                },
                {
                  "key": "created",
                  "location": {
                    "file": "apps/client/src/chat-delivery-creator.ts",
                    "line": 258,
                    "column": 9,
                    "end_line": 258,
                    "start_byte": 8823,
                    "end_byte": 8836,
                    "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/parts/2/location"
                  },
                  "value": {
                    "kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/parts/2/value/kind"
                    },
                    "runtime_value_proven": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/parts/2/value/runtime_value_proven"
                    },
                    "source": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/parts/2/value/source"
                    },
                    "source_truncated": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/parts/2/value/source_truncated"
                    },
                    "location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/construction/parts/2/value/location"
                    }
                  }
                }
              ]
            },
            "location": {
              "file": "apps/client/src/chat-delivery-creator.ts",
              "line": 228,
              "column": 17,
              "end_line": 259,
              "start_byte": 7776,
              "end_byte": 8845,
              "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/0/right/location"
            }
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/3/source_facts/91"
          ],
          "id": "806f0f25455cb5a3268b5012",
          "kind": "ordered_source_assignment_attempt",
          "origin": "source-derived",
          "role": "builder",
          "write_runtime_success_proven": false,
          "branch_context": [],
          "left": {
            "kind": "identifier",
            "name": "active",
            "location": {
              "file": "apps/client/src/chat-delivery-creator.ts",
              "line": 265,
              "column": 5,
              "end_line": 265,
              "start_byte": 9027,
              "end_byte": 9033,
              "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/1/left/location"
            },
            "reference": {
              "declaration_id": "052d32ee2f998d5e115084948af227fd282154f123c3a3b6efdb4c31b8c35962",
              "declaration_kind": "let",
              "identity_complete": true,
              "parameter_index": null,
              "state": "unique",
              "binder_location": {
                "file": "apps/client/src/chat-delivery-creator.ts",
                "line": 128,
                "column": 7,
                "end_line": 128,
                "start_byte": 4090,
                "end_byte": 4096,
                "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/1/left/reference/binder_location"
              },
              "declaration_location": {
                "file": "apps/client/src/chat-delivery-creator.ts",
                "line": 128,
                "column": 7,
                "end_line": 128,
                "start_byte": 4090,
                "end_byte": 4127,
                "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/1/left/reference/declaration_location"
              }
            }
          },
          "location": {
            "file": "apps/client/src/chat-delivery-creator.ts",
            "line": 265,
            "column": 5,
            "end_line": 265,
            "start_byte": 9027,
            "end_byte": 9046,
            "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/1/location"
          },
          "right": {
            "kind": "identifier",
            "name": "controller",
            "location": {
              "file": "apps/client/src/chat-delivery-creator.ts",
              "line": 265,
              "column": 14,
              "end_line": 265,
              "start_byte": 9036,
              "end_byte": 9046,
              "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/1/right/location"
            },
            "reference": {
              "declaration_id": "1d0fe195d6b7e51eceb1a32aa4c71782209e95d5ec8a306f21ae81ed28723bc5",
              "declaration_kind": "const",
              "identity_complete": true,
              "parameter_index": null,
              "state": "unique",
              "binder_location": {
                "file": "apps/client/src/chat-delivery-creator.ts",
                "line": 264,
                "column": 11,
                "end_line": 264,
                "start_byte": 8988,
                "end_byte": 8998,
                "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/1/right/reference/binder_location"
              },
              "declaration_location": {
                "file": "apps/client/src/chat-delivery-creator.ts",
                "line": 264,
                "column": 11,
                "end_line": 264,
                "start_byte": 8988,
                "end_byte": 9022,
                "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/1/right/reference/declaration_location"
              }
            }
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/3/source_facts/97"
          ],
          "id": "926b790d203d2868520e9a53",
          "kind": "ordered_source_assignment_attempt",
          "origin": "source-derived",
          "role": "builder",
          "write_runtime_success_proven": false,
          "branch_context": [
            {
              "branch": "then",
              "condition_truth_proven": false,
              "kind": "if",
              "condition": {
                "kind": "binary_expression",
                "operator": "===",
                "runtime_predicate_or_assignment_proven": false,
                "location": {
                  "file": "apps/client/src/chat-delivery-creator.ts",
                  "line": 268,
                  "column": 11,
                  "end_line": 268,
                  "start_byte": 9099,
                  "end_byte": 9130,
                  "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/2/branch_context/0/condition/location"
                },
                "operands": [
                  {
                    "current_referent_value_proven": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/2/branch_context/0/condition/operands/0/current_referent_value_proven"
                    },
                    "kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/2/branch_context/0/condition/operands/0/kind"
                    },
                    "member": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/2/branch_context/0/condition/operands/0/member"
                    },
                    "location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/2/branch_context/0/condition/operands/0/location"
                    },
                    "member_location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/2/branch_context/0/condition/operands/0/member_location"
                    },
                    "object": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/2/branch_context/0/condition/operands/0/object"
                    }
                  },
                  {
                    "kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/2/branch_context/0/condition/operands/1/kind"
                    },
                    "runtime_value_proven": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/2/branch_context/0/condition/operands/1/runtime_value_proven"
                    },
                    "source": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/2/branch_context/0/condition/operands/1/source"
                    },
                    "source_truncated": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/2/branch_context/0/condition/operands/1/source_truncated"
                    },
                    "location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/2/branch_context/0/condition/operands/1/location"
                    }
                  }
                ]
              },
              "location": {
                "file": "apps/client/src/chat-delivery-creator.ts",
                "line": 268,
                "column": 7,
                "end_line": 285,
                "start_byte": 9095,
                "end_byte": 9669,
                "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/2/branch_context/0/location"
              }
            }
          ],
          "left": {
            "current_referent_value_proven": false,
            "kind": "member_expression",
            "member": "created",
            "location": {
              "file": "apps/client/src/chat-delivery-creator.ts",
              "line": 284,
              "column": 9,
              "end_line": 284,
              "start_byte": 9629,
              "end_byte": 9651,
              "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/2/left/location"
            },
            "member_location": {
              "file": "apps/client/src/chat-delivery-creator.ts",
              "line": 284,
              "column": 24,
              "end_line": 284,
              "start_byte": 9644,
              "end_byte": 9651,
              "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/2/left/member_location"
            },
            "object": {
              "kind": "identifier",
              "name": "currentAttempt",
              "location": {
                "file": "apps/client/src/chat-delivery-creator.ts",
                "line": 284,
                "column": 9,
                "end_line": 284,
                "start_byte": 9629,
                "end_byte": 9643,
                "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/2/left/object/location"
              },
              "reference": {
                "declaration_id": "adbd78b5a4673ce6028eccad1ea3a96160bf0dd5edf21edde72771b6b14812a2",
                "declaration_kind": "const",
                "identity_complete": true,
                "parameter_index": null,
                "state": "unique",
                "binder_location": {
                  "file": "apps/client/src/chat-delivery-creator.ts",
                  "line": 261,
                  "column": 11,
                  "end_line": 261,
                  "start_byte": 8862,
                  "end_byte": 8876,
                  "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/2/left/object/reference/binder_location"
                },
                "declaration_location": {
                  "file": "apps/client/src/chat-delivery-creator.ts",
                  "line": 261,
                  "column": 11,
                  "end_line": 261,
                  "start_byte": 8862,
                  "end_byte": 8886,
                  "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/2/left/object/reference/declaration_location"
                }
              }
            }
          },
          "location": {
            "file": "apps/client/src/chat-delivery-creator.ts",
            "line": 284,
            "column": 9,
            "end_line": 284,
            "start_byte": 9629,
            "end_byte": 9661,
            "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/2/location"
          },
          "right": {
            "kind": "identifier",
            "name": "created",
            "location": {
              "file": "apps/client/src/chat-delivery-creator.ts",
              "line": 284,
              "column": 34,
              "end_line": 284,
              "start_byte": 9654,
              "end_byte": 9661,
              "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/2/right/location"
            },
            "reference": {
              "declaration_id": "cb74707071a79a534ece8db3b4e41bd87fe18c0bd87fa9587398fa3df03340ee",
              "declaration_kind": "const",
              "identity_complete": true,
              "parameter_index": null,
              "state": "unique",
              "binder_location": {
                "file": "apps/client/src/chat-delivery-creator.ts",
                "line": 274,
                "column": 15,
                "end_line": 274,
                "start_byte": 9352,
                "end_byte": 9359,
                "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/2/right/reference/binder_location"
              },
              "declaration_location": {
                "file": "apps/client/src/chat-delivery-creator.ts",
                "line": 274,
                "column": 15,
                "end_line": 279,
                "start_byte": 9352,
                "end_byte": 9526,
                "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/2/right/reference/declaration_location"
              }
            }
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/3/source_facts/99"
          ],
          "id": "4fde59d4ae9d6d9b0e8aae7d",
          "kind": "ordered_source_assignment_attempt",
          "origin": "source-derived",
          "role": "builder",
          "write_runtime_success_proven": false,
          "branch_context": [
            {
              "branch": "then",
              "condition_truth_proven": false,
              "kind": "if",
              "condition": {
                "kind": "binary_expression",
                "operator": "===",
                "runtime_predicate_or_assignment_proven": false,
                "location": {
                  "file": "apps/client/src/chat-delivery-creator.ts",
                  "line": 286,
                  "column": 11,
                  "end_line": 286,
                  "start_byte": 9680,
                  "end_byte": 9721,
                  "full_location_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/3/branch_context/0/condition/location"
                },
                "operands": [
                  {
                    "current_referent_value_proven": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/3/branch_context/0/condition/operands/0/current_referent_value_proven"
                    },
                    "kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/3/branch_context/0/condition/operands/0/kind"
                    },
                    "member": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/3/branch_context/0/condition/operands/0/member"
                    },
                    "location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/3/branch_context/0/condition/operands/0/location"
                    },
                    "member_location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/3/branch_context/0/condition/operands/0/member_location"
                    },
                    "object": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/3/branch_context/0/condition/operands/0/object"
                    }
                  },
                  {
                    "remaining_fields_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/3/branch_context/0/condition/operands/1"
                  }
                ]
              },
              "remaining_fields_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/3/branch_context/0"
            }
          ],
          "remaining_fields_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts/3"
        }
      ],
      "shown_count": 4,
      "total_count": 6,
      "truncated": true,
      "full_value_ref": "/functional_chains/3/pattern/sequences/builder/assignment_attempts"
    },
    "remaining_fields_ref": "/functional_chains/3/pattern/sequences/builder"
  },
  "remaining_fields_ref": "/functional_chains/3/pattern/sequences"
}
```

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

### wwc-report-chat-retained-request-identities

类型：`message_identity_relations`；源码关系评估：`scoped_source_relations_supported`。

保存发现：`38c824f8b536a9f7d17dc8ad`；证据：`688bfd252f4e08f62d95fbf5`。

- `chat_create`：`apps/client/src/chat-delivery-creator.ts` / `createChatDeliveryCreator.create`。
- `chat_items_builder`：`apps/client/src/community-control-plane-client.ts` / `workItemsCreateCommand`。

保存关系的展示摘要（`presentation_only=true`；不新增评级）：

完整 pattern：`/functional_chains/4/pattern`。展示截断：`true`；完整证据与原 pattern 保留。

| 保存字段 | 实际值 | 完整引用 |
| --- | --- | --- |
| creates_calls_edge | false | /functional_chains/4/pattern/creates_calls_edge |
| proof_domain | captured lexical binders, finite field/record projections, enum arms and registered literal SQL source bindings | /functional_chains/4/pattern/proof_domain |
| runtime_transport_or_physical_effect_proven | false | /functional_chains/4/pattern/runtime_transport_or_physical_effect_proven |
| scoped_source_supported | true | /functional_chains/4/pattern/scoped_source_supported |
| source_only | true | /functional_chains/4/pattern/source_only |
| version | captured-message-identity-relations-1 | /functional_chains/4/pattern/version |
| whole_project_identity_complete | false | /functional_chains/4/pattern/whole_project_identity_complete |

**budget**：`/functional_chains/4/pattern/budget`；展示截断：`false`。

```json
{
  "incomplete": false,
  "limit": 65536,
  "operations": 901
}
```

**components**：`/functional_chains/4/pattern/components`；展示截断：`true`。

```json
{
  "chat_request_identity": {
    "all_chat_commands_covered": false,
    "runtime_retry_or_transport_proven": false,
    "scope": "one captured Chat create body and its selected fixed-record builder; requests are separate identities linked through the retained delivery field",
    "supported": true,
    "builder_call_relations": [
      {
        "edge_id": "56319ab867fb03c8cb21decd",
        "fact_id": "7e6c19c10b0bf1c4555c769a",
        "kind": "existing_authenticated_call",
        "supported": true,
        "target_role": "chat_items_builder"
      }
    ],
    "builder_field_projections": {
      "shown_items": [
        {
          "source_fact_refs": [
            "/functional_chains/4/source_facts/82"
          ],
          "creates_calls_edge": false,
          "extractor_version": "captured-message-identity-relations-1",
          "field": "actor",
          "id": "68d6295081115e6378f1aa73",
          "kind": "message_builder_field_projection",
          "origin": "source-derived",
          "target_code_executed": false,
          "location": {
            "file": "apps/client/src/community-control-plane-client.ts",
            "line": 424,
            "column": 12,
            "end_line": 424,
            "start_byte": 16586,
            "end_byte": 16597,
            "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/0/location"
          },
          "output_record_location": {
            "file": "apps/client/src/community-control-plane-client.ts",
            "line": 421,
            "column": 10,
            "end_line": 434,
            "start_byte": 16504,
            "end_byte": 16884,
            "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/0/output_record_location"
          },
          "source": {
            "root": "15d3184ed6c720a2dd8b95061ecc892313a7d8ca3b9793a16937868ea127df49",
            "root_name": "input",
            "binding": {
              "declaration_id": "15d3184ed6c720a2dd8b95061ecc892313a7d8ca3b9793a16937868ea127df49",
              "declaration_kind": "parameter",
              "identity_complete": true,
              "parameter_index": 0,
              "state": "unique",
              "binder_location": {
                "file": "apps/client/src/community-control-plane-client.ts",
                "line": 419,
                "column": 3,
                "end_line": 419,
                "start_byte": 16438,
                "end_byte": 16443,
                "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/0/source/binding/binder_location"
              },
              "declaration_location": {
                "file": "apps/client/src/community-control-plane-client.ts",
                "line": 418,
                "column": 39,
                "end_line": 420,
                "start_byte": 16434,
                "end_byte": 16468,
                "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/0/source/binding/declaration_location"
              }
            },
            "copy_operations": [],
            "location": {
              "file": "apps/client/src/community-control-plane-client.ts",
              "line": 424,
              "column": 12,
              "end_line": 424,
              "start_byte": 16586,
              "end_byte": 16597,
              "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/0/source/location"
            },
            "members": [
              "actor"
            ]
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/4/source_facts/83"
          ],
          "creates_calls_edge": false,
          "extractor_version": "captured-message-identity-relations-1",
          "field": "scope",
          "id": "38e1ca2b76494474481d724d",
          "kind": "message_builder_field_projection",
          "origin": "source-derived",
          "target_code_executed": false,
          "location": {
            "file": "apps/client/src/community-control-plane-client.ts",
            "line": 425,
            "column": 12,
            "end_line": 425,
            "start_byte": 16610,
            "end_byte": 16621,
            "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/1/location"
          },
          "output_record_location": {
            "file": "apps/client/src/community-control-plane-client.ts",
            "line": 421,
            "column": 10,
            "end_line": 434,
            "start_byte": 16504,
            "end_byte": 16884,
            "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/1/output_record_location"
          },
          "source": {
            "root": "15d3184ed6c720a2dd8b95061ecc892313a7d8ca3b9793a16937868ea127df49",
            "root_name": "input",
            "binding": {
              "declaration_id": "15d3184ed6c720a2dd8b95061ecc892313a7d8ca3b9793a16937868ea127df49",
              "declaration_kind": "parameter",
              "identity_complete": true,
              "parameter_index": 0,
              "state": "unique",
              "binder_location": {
                "file": "apps/client/src/community-control-plane-client.ts",
                "line": 419,
                "column": 3,
                "end_line": 419,
                "start_byte": 16438,
                "end_byte": 16443,
                "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/1/source/binding/binder_location"
              },
              "declaration_location": {
                "file": "apps/client/src/community-control-plane-client.ts",
                "line": 418,
                "column": 39,
                "end_line": 420,
                "start_byte": 16434,
                "end_byte": 16468,
                "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/1/source/binding/declaration_location"
              }
            },
            "copy_operations": [],
            "location": {
              "file": "apps/client/src/community-control-plane-client.ts",
              "line": 425,
              "column": 12,
              "end_line": 425,
              "start_byte": 16610,
              "end_byte": 16621,
              "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/1/source/location"
            },
            "members": [
              "scope"
            ]
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/4/source_facts/84"
          ],
          "creates_calls_edge": false,
          "extractor_version": "captured-message-identity-relations-1",
          "field": "requestId",
          "id": "f6ccb10bcef4ff04b51687be",
          "kind": "message_builder_field_projection",
          "origin": "source-derived",
          "target_code_executed": false,
          "location": {
            "file": "apps/client/src/community-control-plane-client.ts",
            "line": 426,
            "column": 16,
            "end_line": 426,
            "start_byte": 16638,
            "end_byte": 16653,
            "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/2/location"
          },
          "output_record_location": {
            "file": "apps/client/src/community-control-plane-client.ts",
            "line": 421,
            "column": 10,
            "end_line": 434,
            "start_byte": 16504,
            "end_byte": 16884,
            "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/2/output_record_location"
          },
          "source": {
            "root": "15d3184ed6c720a2dd8b95061ecc892313a7d8ca3b9793a16937868ea127df49",
            "root_name": "input",
            "binding": {
              "declaration_id": "15d3184ed6c720a2dd8b95061ecc892313a7d8ca3b9793a16937868ea127df49",
              "declaration_kind": "parameter",
              "identity_complete": true,
              "parameter_index": 0,
              "state": "unique",
              "binder_location": {
                "file": "apps/client/src/community-control-plane-client.ts",
                "line": 419,
                "column": 3,
                "end_line": 419,
                "start_byte": 16438,
                "end_byte": 16443,
                "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/2/source/binding/binder_location"
              },
              "declaration_location": {
                "file": "apps/client/src/community-control-plane-client.ts",
                "line": 418,
                "column": 39,
                "end_line": 420,
                "start_byte": 16434,
                "end_byte": 16468,
                "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/2/source/binding/declaration_location"
              }
            },
            "copy_operations": [],
            "location": {
              "file": "apps/client/src/community-control-plane-client.ts",
              "line": 426,
              "column": 16,
              "end_line": 426,
              "start_byte": 16638,
              "end_byte": 16653,
              "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/2/source/location"
            },
            "members": [
              "requestId"
            ]
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/4/source_facts/85"
          ],
          "creates_calls_edge": false,
          "extractor_version": "captured-message-identity-relations-1",
          "field": "expectedRevision",
          "id": "5c6ff70c086b4dda8eaa2e5a",
          "kind": "message_builder_field_projection",
          "origin": "source-derived",
          "target_code_executed": false,
          "location": {
            "file": "apps/client/src/community-control-plane-client.ts",
            "line": 427,
            "column": 23,
            "end_line": 427,
            "start_byte": 16677,
            "end_byte": 16699,
            "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/3/location"
          },
          "output_record_location": {
            "file": "apps/client/src/community-control-plane-client.ts",
            "line": 421,
            "column": 10,
            "end_line": 434,
            "start_byte": 16504,
            "end_byte": 16884,
            "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/3/output_record_location"
          },
          "source": {
            "root": "15d3184ed6c720a2dd8b95061ecc892313a7d8ca3b9793a16937868ea127df49",
            "root_name": "input",
            "binding": {
              "declaration_id": "15d3184ed6c720a2dd8b95061ecc892313a7d8ca3b9793a16937868ea127df49",
              "declaration_kind": "parameter",
              "identity_complete": true,
              "parameter_index": 0,
              "state": "unique",
              "binder_location": {
                "file": "apps/client/src/community-control-plane-client.ts",
                "line": 419,
                "column": 3,
                "end_line": 419,
                "start_byte": 16438,
                "end_byte": 16443,
                "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/3/source/binding/binder_location"
              },
              "declaration_location": {
                "file": "apps/client/src/community-control-plane-client.ts",
                "line": 418,
                "column": 39,
                "end_line": 420,
                "start_byte": 16434,
                "end_byte": 16468,
                "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/3/source/binding/declaration_location"
              }
            },
            "copy_operations": [],
            "location": {
              "file": "apps/client/src/community-control-plane-client.ts",
              "line": 427,
              "column": 23,
              "end_line": 427,
              "start_byte": 16677,
              "end_byte": 16699,
              "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/3/source/location"
            },
            "members": [
              "expectedRevision"
            ]
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/4/source_facts/86"
          ],
          "creates_calls_edge": false,
          "extractor_version": "captured-message-identity-relations-1",
          "field": "deliveryId",
          "id": "e591e8e07d2d69ef9fcac28f",
          "kind": "message_builder_field_projection",
          "origin": "source-derived",
          "target_code_executed": false,
          "location": {
            "file": "apps/client/src/community-control-plane-client.ts",
            "line": 429,
            "column": 19,
            "end_line": 429,
            "start_byte": 16734,
            "end_byte": 16750,
            "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/4/location"
          },
          "output_record_location": {
            "file": "apps/client/src/community-control-plane-client.ts",
            "line": 428,
            "column": 14,
            "end_line": 433,
            "start_byte": 16714,
            "end_byte": 16879,
            "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/4/output_record_location"
          },
          "source": {
            "root": "15d3184ed6c720a2dd8b95061ecc892313a7d8ca3b9793a16937868ea127df49",
            "root_name": "input",
            "binding": {
              "declaration_id": "15d3184ed6c720a2dd8b95061ecc892313a7d8ca3b9793a16937868ea127df49",
              "declaration_kind": "parameter",
              "identity_complete": true,
              "parameter_index": 0,
              "state": "unique",
              "binder_location": {
                "file": "apps/client/src/community-control-plane-client.ts",
                "line": 419,
                "column": 3,
                "end_line": 419,
                "start_byte": 16438,
                "end_byte": 16443,
                "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/4/source/binding/binder_location"
              },
              "declaration_location": {
                "file": "apps/client/src/community-control-plane-client.ts",
                "line": 418,
                "column": 39,
                "end_line": 420,
                "start_byte": 16434,
                "end_byte": 16468,
                "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/4/source/binding/declaration_location"
              }
            },
            "copy_operations": [],
            "location": {
              "file": "apps/client/src/community-control-plane-client.ts",
              "line": 429,
              "column": 19,
              "end_line": 429,
              "start_byte": 16734,
              "end_byte": 16750,
              "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/4/source/location"
            },
            "members": [
              "deliveryId"
            ]
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/4/source_facts/87"
          ],
          "creates_calls_edge": false,
          "extractor_version": "captured-message-identity-relations-1",
          "field": "expectedRevision",
          "id": "9e45057cc794c72e8b938742",
          "kind": "message_builder_field_projection",
          "origin": "source-derived",
          "target_code_executed": false,
          "location": {
            "file": "apps/client/src/community-control-plane-client.ts",
            "line": 430,
            "column": 25,
            "end_line": 430,
            "start_byte": 16776,
            "end_byte": 16798,
            "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/5/location"
          },
          "output_record_location": {
            "file": "apps/client/src/community-control-plane-client.ts",
            "line": 428,
            "column": 14,
            "end_line": 433,
            "start_byte": 16714,
            "end_byte": 16879,
            "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/5/output_record_location"
          },
          "source": {
            "root": "15d3184ed6c720a2dd8b95061ecc892313a7d8ca3b9793a16937868ea127df49",
            "root_name": "input",
            "binding": {
              "declaration_id": "15d3184ed6c720a2dd8b95061ecc892313a7d8ca3b9793a16937868ea127df49",
              "declaration_kind": "parameter",
              "identity_complete": true,
              "parameter_index": 0,
              "state": "unique",
              "binder_location": {
                "file": "apps/client/src/community-control-plane-client.ts",
                "line": 419,
                "column": 3,
                "end_line": 419,
                "start_byte": 16438,
                "end_byte": 16443,
                "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/5/source/binding/binder_location"
              },
              "declaration_location": {
                "file": "apps/client/src/community-control-plane-client.ts",
                "line": 418,
                "column": 39,
                "end_line": 420,
                "start_byte": 16434,
                "end_byte": 16468,
                "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/5/source/binding/declaration_location"
              }
            },
            "copy_operations": [],
            "location": {
              "file": "apps/client/src/community-control-plane-client.ts",
              "line": 430,
              "column": 25,
              "end_line": 430,
              "start_byte": 16776,
              "end_byte": 16798,
              "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections/5/source/location"
            },
            "members": [
              "expectedRevision"
            ]
          }
        }
      ],
      "shown_count": 6,
      "total_count": 8,
      "truncated": true,
      "full_value_ref": "/functional_chains/4/pattern/components/chat_request_identity/builder_field_projections"
    },
    "current_attempt_aliases": [
      {
        "source_fact_refs": [
          "/functional_chains/4/source_facts/56"
        ],
        "creates_calls_edge": false,
        "current_heap_alias_proven": false,
        "extractor_version": "captured-message-identity-relations-1",
        "id": "0544698d944b51aea0cf9eec",
        "kind": "message_local_binding_projection",
        "ordinary_record_read_at_initializer_only": true,
        "origin": "source-derived",
        "target_code_executed": false,
        "location": {
          "file": "apps/client/src/chat-delivery-creator.ts",
          "line": 261,
          "column": 11,
          "end_line": 261,
          "start_byte": 8862,
          "end_byte": 8886,
          "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/current_attempt_aliases/0/location"
        },
        "source": {
          "root": "aced738e30031213c858a972d61acc4aab8aa48712156a5a9e4d037683191e5d",
          "root_name": "attempt",
          "binding": {
            "declaration_id": "aced738e30031213c858a972d61acc4aab8aa48712156a5a9e4d037683191e5d",
            "declaration_kind": "let",
            "identity_complete": true,
            "parameter_index": null,
            "state": "unique",
            "binder_location": {
              "file": "apps/client/src/chat-delivery-creator.ts",
              "line": 130,
              "column": 7,
              "end_line": 130,
              "start_byte": 4155,
              "end_byte": 4162,
              "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/current_attempt_aliases/0/source/binding/binder_location"
            },
            "declaration_location": {
              "file": "apps/client/src/chat-delivery-creator.ts",
              "line": 130,
              "column": 7,
              "end_line": 136,
              "start_byte": 4155,
              "end_byte": 4383,
              "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/current_attempt_aliases/0/source/binding/declaration_location"
            }
          },
          "copy_operations": [],
          "location": {
            "file": "apps/client/src/chat-delivery-creator.ts",
            "line": 261,
            "column": 28,
            "end_line": 261,
            "start_byte": 8879,
            "end_byte": 8886,
            "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/current_attempt_aliases/0/source/location"
          },
          "members": []
        },
        "target": {
          "root": "adbd78b5a4673ce6028eccad1ea3a96160bf0dd5edf21edde72771b6b14812a2",
          "root_name": "currentAttempt",
          "binding": {
            "declaration_id": "adbd78b5a4673ce6028eccad1ea3a96160bf0dd5edf21edde72771b6b14812a2",
            "declaration_kind": "const",
            "identity_complete": true,
            "parameter_index": null,
            "state": "unique",
            "binder_location": {
              "file": "apps/client/src/chat-delivery-creator.ts",
              "line": 261,
              "column": 11,
              "end_line": 261,
              "start_byte": 8862,
              "end_byte": 8876,
              "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/current_attempt_aliases/0/target/binding/binder_location"
            },
            "declaration_location": {
              "file": "apps/client/src/chat-delivery-creator.ts",
              "line": 261,
              "column": 11,
              "end_line": 261,
              "start_byte": 8862,
              "end_byte": 8886,
              "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/current_attempt_aliases/0/target/binding/declaration_location"
            }
          },
          "copy_operations": [],
          "location": {
            "file": "apps/client/src/chat-delivery-creator.ts",
            "line": 261,
            "column": 11,
            "end_line": 261,
            "start_byte": 8862,
            "end_byte": 8876,
            "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/current_attempt_aliases/0/target/location"
          },
          "members": []
        }
      }
    ],
    "delivery_projection": [
      {
        "source_fact_refs": [
          "/functional_chains/4/source_facts/57"
        ],
        "creates_calls_edge": false,
        "current_heap_alias_proven": false,
        "extractor_version": "captured-message-identity-relations-1",
        "id": "8d53a719c43d88fbf06a1fd4",
        "kind": "message_local_binding_projection",
        "ordinary_record_read_at_initializer_only": true,
        "origin": "source-derived",
        "target_code_executed": false,
        "location": {
          "file": "apps/client/src/chat-delivery-creator.ts",
          "line": 262,
          "column": 11,
          "end_line": 262,
          "start_byte": 8897,
          "end_byte": 8957,
          "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/delivery_projection/0/location"
        },
        "source": {
          "root": "adbd78b5a4673ce6028eccad1ea3a96160bf0dd5edf21edde72771b6b14812a2",
          "root_name": "currentAttempt",
          "binding": {
            "declaration_id": "adbd78b5a4673ce6028eccad1ea3a96160bf0dd5edf21edde72771b6b14812a2",
            "declaration_kind": "const",
            "identity_complete": true,
            "parameter_index": null,
            "state": "unique",
            "binder_location": {
              "file": "apps/client/src/chat-delivery-creator.ts",
              "line": 261,
              "column": 11,
              "end_line": 261,
              "start_byte": 8862,
              "end_byte": 8876,
              "full_location_ref": "/functional_chains/4/pattern/components/chat_request_identity/delivery_projection/0/source/binding/binder_location"
            },
            "remaining_fields_ref": "/functional_chains/4/pattern/components/chat_request_identity/delivery_projection/0/source/binding"
          },
          "remaining_fields_ref": "/functional_chains/4/pattern/components/chat_request_identity/delivery_projection/0/source"
        },
        "remaining_fields_ref": "/functional_chains/4/pattern/components/chat_request_identity/delivery_projection/0"
      }
    ],
    "remaining_fields_ref": "/functional_chains/4/pattern/components/chat_request_identity"
  }
}
```

**limits**：`/functional_chains/4/pattern/limits`；展示截断：`false`。

```json
[
  "member paths identify source projections, not globally stable heap cells",
  "Rust Clone/borrow projections require ordinary generated data semantics; arbitrary trait behavior is not inferred",
  "generic adapter calls remain contextual source interfaces, never global unique targets",
  "correlation tuple agreement is a field-domain agreement; payload equality is checked by source consumers, not assumed",
  "SQL parameters are captured token positions under the registered literal source model; no database is executed",
  "retries, rejected/replayed acks, all crash windows and external authenticity are not fully proved"
]
```

**models**：`/functional_chains/4/pattern/models`；展示截断：`false`。

```json
[
  "finite-captured-record-message-identities-v1"
]
```

**relation_fact_ids**：`/functional_chains/4/pattern/relation_fact_ids`；展示截断：`true`。

```json
{
  "shown_items": [
    "11a83a64ee2783d227b8a363",
    "d0b08c59f9606128370224d3",
    "e404769d282f4ecaf6f431a3",
    "a6473050b1285eecd839b99f",
    "5a8dea97f13508fa1b869e59",
    "0544698d944b51aea0cf9eec"
  ],
  "shown_count": 6,
  "total_count": 39,
  "truncated": true,
  "full_value_ref": "/functional_chains/4/pattern/relation_fact_ids"
}
```

自动关系类型：`{"captured_call_step": 49, "message_builder_field_projection": 8, "message_captured_record_fields": 18, "message_delivery_identity_record_projection": 3, "message_local_binding_projection": 3, "message_request_emission_projection": 3, "message_response_request_id_comparison": 2, "message_retained_request_assignment": 2, "report_source_role": 2}`。

分析缺口：

```json
[]
```

条件与反证声明（单列为配置范围，不冒充源码证据）：

```json
{
  "applicability": {
    "conditions": [
      "Selected captured declarations are authenticated.",
      "Ordinary generated data retains normal borrowed/copied field semantics; source reaching is conditional, not observed execution."
    ],
    "counterexamples": [
      "Generic dispatch, wire equality, physical storage success and complete crash recovery are not inferred."
    ],
    "kind": "conditional"
  },
  "descriptive_counterexamples_are_computed_evidence": false,
  "origin": "policy-declared",
  "provenance": {
    "author_approved": false,
    "authority": "original-static-report-benchmark",
    "note": "Declaration locators only. Field records and consumers derive from authenticated saved source; no paths or expected outcomes are provided.",
    "source_doc": "reports/astra-baseline/WINWINCODE_ANALYSIS.md"
  }
}
```

### wwc-report-device-provider-deployment

类型：`deployment_provider_split`；源码关系评估：`scoped_source_relations_supported`。

保存发现：`760fc36cee29db794d4056c6`；证据：`e86cf700fe852d931a5420bb`。

- `boundary`：`crates/winwincode-server/src/main.rs` / `<DeviceModelBoundary as winwincode_control_plane::DurableExecutionPortDelegate>.accept`。
- `bootstrap`：`crates/winwincode-worker/src/main.rs` / `run_worker`。
- `installation`：`crates/winwincode-worker/src/lib.rs` / `WorkerMain.with_device_providers`。
- `provider`：`crates/winwincode-worker/src/device_model.rs` / `DeviceModels.open`。

保存关系的展示摘要（`presentation_only=true`；不新增评级）：

完整 pattern：`/functional_chains/5/pattern`。展示截断：`true`；完整证据与原 pattern 保留。

| 保存字段 | 实际值 | 完整引用 |
| --- | --- | --- |
| deployments_or_provider_implementations_equivalent | false | /functional_chains/5/pattern/deployments_or_provider_implementations_equivalent |
| scoped_source_supported | true | /functional_chains/5/pattern/scoped_source_supported |
| unsupported_boundary_implies_project_capability_absent | false | /functional_chains/5/pattern/unsupported_boundary_implies_project_capability_absent |

**argument_sources**：`/functional_chains/5/pattern/argument_sources`；展示截断：`false`。

```json
[]
```

**boundary_results**：`/functional_chains/5/pattern/boundary_results`；展示截断：`true`。

```json
[
  {
    "source_fact_refs": [
      "/functional_chains/5/source_facts/72"
    ],
    "id": "ab2cfada79b8758a58eac49d",
    "kind": "boundary_result_source",
    "origin": "source-derived",
    "runtime_result_proven": false,
    "expression": {
      "call_effects_or_result_proven": false,
      "callee_source": "Err",
      "kind": "call_expression",
      "arguments": [
        {
          "kind": "scoped_identifier",
          "source": "winwincode_control_plane::DurableExecutionPortError::UnsupportedMessage",
          "children": [
            {
              "kind": "scoped_identifier",
              "source": "winwincode_control_plane::DurableExecutionPortError",
              "children": [
                {
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/children/0/children/0/kind"
                  },
                  "name": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/children/0/children/0/name"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/children/0/children/0/location"
                  },
                  "reference": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/children/0/children/0/reference"
                  }
                },
                {
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/children/0/children/1/kind"
                  },
                  "name": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/children/0/children/1/name"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/children/0/children/1/location"
                  },
                  "reference": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/children/0/children/1/reference"
                  }
                }
              ],
              "location": {
                "file": "crates/winwincode-server/src/main.rs",
                "line": 346,
                "column": 13,
                "end_line": 346,
                "start_byte": 13431,
                "end_byte": 13482,
                "full_location_ref": "/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/children/0/location"
              }
            },
            {
              "kind": "identifier",
              "name": "UnsupportedMessage",
              "location": {
                "file": "crates/winwincode-server/src/main.rs",
                "line": 346,
                "column": 66,
                "end_line": 346,
                "start_byte": 13484,
                "end_byte": 13502,
                "full_location_ref": "/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/children/1/location"
              },
              "reference": {
                "plain_binder_candidates": 0,
                "runtime_value_identity_proven": false,
                "state": "captured_rust_reference",
                "text": "UnsupportedMessage",
                "location": {
                  "file": "crates/winwincode-server/src/main.rs",
                  "line": 346,
                  "column": 66,
                  "end_line": 346,
                  "start_byte": 13484,
                  "end_byte": 13502,
                  "full_location_ref": "/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/children/1/reference/location"
                }
              }
            }
          ],
          "location": {
            "file": "crates/winwincode-server/src/main.rs",
            "line": 346,
            "column": 13,
            "end_line": 346,
            "start_byte": 13431,
            "end_byte": 13502,
            "full_location_ref": "/functional_chains/5/pattern/boundary_results/0/expression/arguments/0/location"
          }
        }
      ],
      "callee_expression": {
        "kind": "identifier",
        "name": "Err",
        "location": {
          "file": "crates/winwincode-server/src/main.rs",
          "line": 346,
          "column": 9,
          "end_line": 346,
          "start_byte": 13427,
          "end_byte": 13430,
          "full_location_ref": "/functional_chains/5/pattern/boundary_results/0/expression/callee_expression/location"
        },
        "reference": {
          "plain_binder_candidates": 0,
          "runtime_value_identity_proven": false,
          "state": "captured_rust_reference",
          "text": "Err",
          "location": {
            "file": "crates/winwincode-server/src/main.rs",
            "line": 346,
            "column": 9,
            "end_line": 346,
            "start_byte": 13427,
            "end_byte": 13430,
            "full_location_ref": "/functional_chains/5/pattern/boundary_results/0/expression/callee_expression/reference/location"
          }
        }
      },
      "location": {
        "file": "crates/winwincode-server/src/main.rs",
        "line": 346,
        "column": 9,
        "end_line": 346,
        "start_byte": 13427,
        "end_byte": 13503,
        "full_location_ref": "/functional_chains/5/pattern/boundary_results/0/expression/location"
      }
    },
    "location": {
      "file": "crates/winwincode-server/src/main.rs",
      "line": 346,
      "column": 9,
      "end_line": 346,
      "start_byte": 13427,
      "end_byte": 13503,
      "full_location_ref": "/functional_chains/5/pattern/boundary_results/0/location"
    }
  }
]
```

**installation_assignments**：`/functional_chains/5/pattern/installation_assignments`；展示截断：`false`。

```json
[
  {
    "source_fact_refs": [
      "/functional_chains/5/source_facts/81"
    ],
    "id": "74008c3422900b5efacb5f0b",
    "kind": "provider_installation_assignment_source",
    "origin": "source-derived",
    "role": "installation",
    "runtime_installed_value_proven": false,
    "left": {
      "current_referent_value_proven": false,
      "kind": "field_expression",
      "member": "device_models",
      "location": {
        "file": "crates/winwincode-worker/src/lib.rs",
        "line": 418,
        "column": 9,
        "end_line": 418,
        "start_byte": 16841,
        "end_byte": 16859,
        "full_location_ref": "/functional_chains/5/pattern/installation_assignments/0/left/location"
      },
      "member_location": {
        "file": "crates/winwincode-worker/src/lib.rs",
        "line": 418,
        "column": 14,
        "end_line": 418,
        "start_byte": 16846,
        "end_byte": 16859,
        "full_location_ref": "/functional_chains/5/pattern/installation_assignments/0/left/member_location"
      },
      "object": {
        "kind": "self",
        "name": "self",
        "location": {
          "file": "crates/winwincode-worker/src/lib.rs",
          "line": 418,
          "column": 9,
          "end_line": 418,
          "start_byte": 16841,
          "end_byte": 16845,
          "full_location_ref": "/functional_chains/5/pattern/installation_assignments/0/left/object/location"
        },
        "reference": {
          "declaration_id": "b3fd55289e8050ccd2e4aff9694ba17c17f19be504bf6ae016d27f9c4cbaac6a",
          "declaration_kind": "captured_rust_parameter",
          "identity_scope": "plain captured binder syntax only",
          "macro_namespace_complete": false,
          "runtime_value_identity_proven": false,
          "state": "captured_unique_rust_binder",
          "binder_location": {
            "file": "crates/winwincode-worker/src/lib.rs",
            "line": 410,
            "column": 13,
            "end_line": 410,
            "start_byte": 16424,
            "end_byte": 16428,
            "full_location_ref": "/functional_chains/5/pattern/installation_assignments/0/left/object/reference/binder_location"
          },
          "declaration_location": {
            "file": "crates/winwincode-worker/src/lib.rs",
            "line": 410,
            "column": 9,
            "end_line": 410,
            "start_byte": 16420,
            "end_byte": 16428,
            "full_location_ref": "/functional_chains/5/pattern/installation_assignments/0/left/object/reference/declaration_location"
          }
        }
      }
    },
    "location": {
      "file": "crates/winwincode-worker/src/lib.rs",
      "line": 418,
      "column": 9,
      "end_line": 418,
      "start_byte": 16841,
      "end_byte": 16874,
      "full_location_ref": "/functional_chains/5/pattern/installation_assignments/0/location"
    },
    "right": {
      "call_effects_or_result_proven": false,
      "callee_source": "Some",
      "kind": "call_expression",
      "arguments": [
        {
          "kind": "identifier",
          "name": "models",
          "location": {
            "file": "crates/winwincode-worker/src/lib.rs",
            "line": 418,
            "column": 35,
            "end_line": 418,
            "start_byte": 16867,
            "end_byte": 16873,
            "full_location_ref": "/functional_chains/5/pattern/installation_assignments/0/right/arguments/0/location"
          },
          "reference": {
            "declaration_id": "98410a6f0f960669d5cc89cf571f5516fa51b21564cf5f4d7c9d9cc415cfbc44",
            "declaration_kind": "captured_rust_local",
            "identity_scope": "plain captured binder syntax only",
            "macro_namespace_complete": false,
            "runtime_value_identity_proven": false,
            "state": "captured_unique_rust_binder",
            "binder_location": {
              "file": "crates/winwincode-worker/src/lib.rs",
              "line": 413,
              "column": 17,
              "end_line": 413,
              "start_byte": 16549,
              "end_byte": 16555,
              "full_location_ref": "/functional_chains/5/pattern/installation_assignments/0/right/arguments/0/reference/binder_location"
            },
            "declaration_location": {
              "file": "crates/winwincode-worker/src/lib.rs",
              "line": 413,
              "column": 9,
              "end_line": 413,
              "start_byte": 16541,
              "end_byte": 16603,
              "full_location_ref": "/functional_chains/5/pattern/installation_assignments/0/right/arguments/0/reference/declaration_location"
            }
          }
        }
      ],
      "callee_expression": {
        "kind": "identifier",
        "name": "Some",
        "location": {
          "file": "crates/winwincode-worker/src/lib.rs",
          "line": 418,
          "column": 30,
          "end_line": 418,
          "start_byte": 16862,
          "end_byte": 16866,
          "full_location_ref": "/functional_chains/5/pattern/installation_assignments/0/right/callee_expression/location"
        },
        "reference": {
          "plain_binder_candidates": 0,
          "runtime_value_identity_proven": false,
          "state": "captured_rust_reference",
          "text": "Some",
          "location": {
            "file": "crates/winwincode-worker/src/lib.rs",
            "line": 418,
            "column": 30,
            "end_line": 418,
            "start_byte": 16862,
            "end_byte": 16866,
            "full_location_ref": "/functional_chains/5/pattern/installation_assignments/0/right/callee_expression/reference/location"
          }
        }
      },
      "location": {
        "file": "crates/winwincode-worker/src/lib.rs",
        "line": 418,
        "column": 30,
        "end_line": 418,
        "start_byte": 16862,
        "end_byte": 16874,
        "full_location_ref": "/functional_chains/5/pattern/installation_assignments/0/right/location"
      }
    }
  },
  {
    "source_fact_refs": [
      "/functional_chains/5/source_facts/127"
    ],
    "id": "b77b168fb3f81c401455a46a",
    "kind": "provider_installation_assignment_source",
    "origin": "source-derived",
    "role": "bootstrap",
    "runtime_installed_value_proven": false,
    "left": {
      "kind": "identifier",
      "name": "worker",
      "location": {
        "file": "crates/winwincode-worker/src/main.rs",
        "line": 205,
        "column": 9,
        "end_line": 205,
        "start_byte": 8323,
        "end_byte": 8329,
        "full_location_ref": "/functional_chains/5/pattern/installation_assignments/1/left/location"
      },
      "reference": {
        "declaration_id": "a629bf62724062dbd879ae08e9dd01ffb2bf3d544980a278a7bc2b7d1c0e81d4",
        "declaration_kind": "captured_rust_local",
        "identity_scope": "plain captured binder syntax only",
        "macro_namespace_complete": false,
        "runtime_value_identity_proven": false,
        "state": "captured_unique_rust_binder",
        "binder_location": {
          "file": "crates/winwincode-worker/src/main.rs",
          "line": 199,
          "column": 13,
          "end_line": 199,
          "start_byte": 7980,
          "end_byte": 7986,
          "full_location_ref": "/functional_chains/5/pattern/installation_assignments/1/left/reference/binder_location"
        },
        "declaration_location": {
          "file": "crates/winwincode-worker/src/main.rs",
          "line": 199,
          "column": 5,
          "end_line": 203,
          "start_byte": 7972,
          "end_byte": 8257,
          "full_location_ref": "/functional_chains/5/pattern/installation_assignments/1/left/reference/declaration_location"
        }
      }
    },
    "location": {
      "file": "crates/winwincode-worker/src/main.rs",
      "line": 205,
      "column": 9,
      "end_line": 205,
      "start_byte": 8323,
      "end_byte": 8380,
      "full_location_ref": "/functional_chains/5/pattern/installation_assignments/1/location"
    },
    "right": {
      "call_effects_or_result_proven": false,
      "callee_source": "worker.with_observation_model",
      "kind": "call_expression",
      "arguments": [
        {
          "kind": "identifier",
          "name": "observation_model",
          "location": {
            "file": "crates/winwincode-worker/src/main.rs",
            "line": 205,
            "column": 48,
            "end_line": 205,
            "start_byte": 8362,
            "end_byte": 8379,
            "full_location_ref": "/functional_chains/5/pattern/installation_assignments/1/right/arguments/0/location"
          },
          "reference": {
            "declaration_id": "c33393ca9eda1bb3c0d861a16dbd555f134e0f704808f9d98156e9d508f37c53",
            "declaration_kind": "captured_rust_local",
            "identity_scope": "plain captured binder syntax only",
            "macro_namespace_complete": false,
            "runtime_value_identity_proven": false,
            "state": "captured_unique_rust_binder",
            "binder_location": {
              "file": "crates/winwincode-worker/src/main.rs",
              "line": 170,
              "column": 9,
              "end_line": 170,
              "start_byte": 6860,
              "end_byte": 6877,
              "full_location_ref": "/functional_chains/5/pattern/installation_assignments/1/right/arguments/0/reference/binder_location"
            },
            "declaration_location": {
              "file": "crates/winwincode-worker/src/main.rs",
              "line": 170,
              "column": 5,
              "end_line": 170,
              "start_byte": 6856,
              "end_byte": 6935,
              "full_location_ref": "/functional_chains/5/pattern/installation_assignments/1/right/arguments/0/reference/declaration_location"
            }
          }
        }
      ],
      "callee_expression": {
        "current_referent_value_proven": false,
        "kind": "field_expression",
        "member": "with_observation_model",
        "location": {
          "file": "crates/winwincode-worker/src/main.rs",
          "line": 205,
          "column": 18,
          "end_line": 205,
          "start_byte": 8332,
          "end_byte": 8361,
          "full_location_ref": "/functional_chains/5/pattern/installation_assignments/1/right/callee_expression/location"
        },
        "member_location": {
          "file": "crates/winwincode-worker/src/main.rs",
          "line": 205,
          "column": 25,
          "end_line": 205,
          "start_byte": 8339,
          "end_byte": 8361,
          "full_location_ref": "/functional_chains/5/pattern/installation_assignments/1/right/callee_expression/member_location"
        },
        "object": {
          "kind": "identifier",
          "name": "worker",
          "location": {
            "file": "crates/winwincode-worker/src/main.rs",
            "line": 205,
            "column": 18,
            "end_line": 205,
            "start_byte": 8332,
            "end_byte": 8338,
            "full_location_ref": "/functional_chains/5/pattern/installation_assignments/1/right/callee_expression/object/location"
          },
          "reference": {
            "declaration_id": "a629bf62724062dbd879ae08e9dd01ffb2bf3d544980a278a7bc2b7d1c0e81d4",
            "declaration_kind": "captured_rust_local",
            "identity_scope": "plain captured binder syntax only",
            "macro_namespace_complete": false,
            "runtime_value_identity_proven": false,
            "state": "captured_unique_rust_binder",
            "binder_location": {
              "file": "crates/winwincode-worker/src/main.rs",
              "line": 199,
              "column": 13,
              "end_line": 199,
              "start_byte": 7980,
              "end_byte": 7986,
              "full_location_ref": "/functional_chains/5/pattern/installation_assignments/1/right/callee_expression/object/reference/binder_location"
            },
            "declaration_location": {
              "file": "crates/winwincode-worker/src/main.rs",
              "line": 199,
              "column": 5,
              "end_line": 203,
              "start_byte": 7972,
              "end_byte": 8257,
              "full_location_ref": "/functional_chains/5/pattern/installation_assignments/1/right/callee_expression/object/reference/declaration_location"
            }
          }
        }
      },
      "location": {
        "file": "crates/winwincode-worker/src/main.rs",
        "line": 205,
        "column": 18,
        "end_line": 205,
        "start_byte": 8332,
        "end_byte": 8380,
        "full_location_ref": "/functional_chains/5/pattern/installation_assignments/1/right/location"
      }
    }
  }
]
```

**production_constructions**：`/functional_chains/5/pattern/production_constructions`；展示截断：`true`。

```json
{
  "shown_items": [
    {
      "source_fact_refs": [
        "/functional_chains/5/source_facts/73"
      ],
      "actual_callee_graph_node_id": "rust:crates/winwincode-worker/src/device_model#DeviceModels.open",
      "call_fact_id": "ebfcb005d3546425890b13ea",
      "global_receiver_dispatch_proven": false,
      "id": "93bb642e3f35c2338d533ea2",
      "kind": "production_construction_call_source",
      "model_id": "source-derived-production-construction-v1",
      "origin": "source-derived",
      "role": "installation",
      "arguments": [
        {
          "kind": "identifier",
          "name": "directory",
          "location": {
            "file": "crates/winwincode-worker/src/lib.rs",
            "line": 413,
            "column": 59,
            "end_line": 413,
            "start_byte": 16591,
            "end_byte": 16600,
            "full_location_ref": "/functional_chains/5/pattern/production_constructions/0/arguments/0/location"
          },
          "reference": {
            "declaration_id": "f21cdc8156b7f350b97ba7493dd48c9a299a205729fc27953e6e4e9d8fef955d",
            "declaration_kind": "captured_rust_parameter",
            "identity_scope": "plain captured binder syntax only",
            "macro_namespace_complete": false,
            "runtime_value_identity_proven": false,
            "state": "captured_unique_rust_binder",
            "binder_location": {
              "file": "crates/winwincode-worker/src/lib.rs",
              "line": 411,
              "column": 9,
              "end_line": 411,
              "start_byte": 16438,
              "end_byte": 16447,
              "full_location_ref": "/functional_chains/5/pattern/production_constructions/0/arguments/0/reference/binder_location"
            },
            "declaration_location": {
              "file": "crates/winwincode-worker/src/lib.rs",
              "line": 411,
              "column": 9,
              "end_line": 411,
              "start_byte": 16438,
              "end_byte": 16465,
              "full_location_ref": "/functional_chains/5/pattern/production_constructions/0/arguments/0/reference/declaration_location"
            }
          }
        }
      ],
      "callee": {
        "kind": "scoped_identifier",
        "source": "device_model::DeviceModels::open",
        "children": [
          {
            "kind": "scoped_identifier",
            "source": "device_model::DeviceModels",
            "children": [
              {
                "kind": "identifier",
                "name": "device_model",
                "location": {
                  "file": "crates/winwincode-worker/src/lib.rs",
                  "line": 413,
                  "column": 26,
                  "end_line": 413,
                  "start_byte": 16558,
                  "end_byte": 16570,
                  "full_location_ref": "/functional_chains/5/pattern/production_constructions/0/callee/children/0/children/0/location"
                },
                "reference": {
                  "plain_binder_candidates": 0,
                  "runtime_value_identity_proven": false,
                  "state": "captured_rust_reference",
                  "text": "device_model",
                  "location": {
                    "file": "crates/winwincode-worker/src/lib.rs",
                    "line": 413,
                    "column": 26,
                    "end_line": 413,
                    "start_byte": 16558,
                    "end_byte": 16570,
                    "full_location_ref": "/functional_chains/5/pattern/production_constructions/0/callee/children/0/children/0/reference/location"
                  }
                }
              },
              {
                "kind": "identifier",
                "name": "DeviceModels",
                "location": {
                  "file": "crates/winwincode-worker/src/lib.rs",
                  "line": 413,
                  "column": 40,
                  "end_line": 413,
                  "start_byte": 16572,
                  "end_byte": 16584,
                  "full_location_ref": "/functional_chains/5/pattern/production_constructions/0/callee/children/0/children/1/location"
                },
                "reference": {
                  "plain_binder_candidates": 0,
                  "runtime_value_identity_proven": false,
                  "state": "captured_rust_reference",
                  "text": "DeviceModels",
                  "location": {
                    "file": "crates/winwincode-worker/src/lib.rs",
                    "line": 413,
                    "column": 40,
                    "end_line": 413,
                    "start_byte": 16572,
                    "end_byte": 16584,
                    "full_location_ref": "/functional_chains/5/pattern/production_constructions/0/callee/children/0/children/1/reference/location"
                  }
                }
              }
            ],
            "location": {
              "file": "crates/winwincode-worker/src/lib.rs",
              "line": 413,
              "column": 26,
              "end_line": 413,
              "start_byte": 16558,
              "end_byte": 16584,
              "full_location_ref": "/functional_chains/5/pattern/production_constructions/0/callee/children/0/location"
            }
          },
          {
            "kind": "identifier",
            "name": "open",
            "location": {
              "file": "crates/winwincode-worker/src/lib.rs",
              "line": 413,
              "column": 54,
              "end_line": 413,
              "start_byte": 16586,
              "end_byte": 16590,
              "full_location_ref": "/functional_chains/5/pattern/production_constructions/0/callee/children/1/location"
            },
            "reference": {
              "plain_binder_candidates": 0,
              "runtime_value_identity_proven": false,
              "state": "captured_rust_reference",
              "text": "open",
              "location": {
                "file": "crates/winwincode-worker/src/lib.rs",
                "line": 413,
                "column": 54,
                "end_line": 413,
                "start_byte": 16586,
                "end_byte": 16590,
                "full_location_ref": "/functional_chains/5/pattern/production_constructions/0/callee/children/1/reference/location"
              }
            }
          }
        ],
        "location": {
          "file": "crates/winwincode-worker/src/lib.rs",
          "line": 413,
          "column": 26,
          "end_line": 413,
          "start_byte": 16558,
          "end_byte": 16590,
          "full_location_ref": "/functional_chains/5/pattern/production_constructions/0/callee/location"
        }
      },
      "location": {
        "file": "crates/winwincode-worker/src/lib.rs",
        "line": 413,
        "column": 26,
        "end_line": 413,
        "start_byte": 16558,
        "end_byte": 16601,
        "full_location_ref": "/functional_chains/5/pattern/production_constructions/0/location"
      }
    },
    {
      "source_fact_refs": [
        "/functional_chains/5/source_facts/74"
      ],
      "actual_callee_graph_node_id": null,
      "call_fact_id": "a7169145919072cb5700bf05",
      "global_receiver_dispatch_proven": false,
      "id": "1f12c0ec72c210734fe9d5e4",
      "kind": "production_construction_call_source",
      "model_id": "source-derived-production-construction-v1",
      "origin": "source-derived",
      "role": "installation",
      "arguments": [
        {
          "kind": "reference_expression",
          "location": {
            "file": "crates/winwincode-worker/src/lib.rs",
            "line": 414,
            "column": 40,
            "end_line": 414,
            "start_byte": 16643,
            "end_byte": 16676,
            "full_location_ref": "/functional_chains/5/pattern/production_constructions/1/arguments/0/location"
          },
          "operand": {
            "current_referent_value_proven": false,
            "kind": "field_expression",
            "member": null,
            "location": {
              "file": "crates/winwincode-worker/src/lib.rs",
              "line": 414,
              "column": 41,
              "end_line": 414,
              "start_byte": 16644,
              "end_byte": 16676,
              "full_location_ref": "/functional_chains/5/pattern/production_constructions/1/arguments/0/operand/location"
            },
            "member_location": {
              "file": "crates/winwincode-worker/src/lib.rs",
              "line": 414,
              "column": 72,
              "end_line": 414,
              "start_byte": 16675,
              "end_byte": 16676,
              "full_location_ref": "/functional_chains/5/pattern/production_constructions/1/arguments/0/operand/member_location"
            },
            "object": {
              "current_referent_value_proven": false,
              "kind": "field_expression",
              "member": "worker_instance_id",
              "location": {
                "file": "crates/winwincode-worker/src/lib.rs",
                "line": 414,
                "column": 41,
                "end_line": 414,
                "start_byte": 16644,
                "end_byte": 16674,
                "full_location_ref": "/functional_chains/5/pattern/production_constructions/1/arguments/0/operand/object/location"
              },
              "member_location": {
                "file": "crates/winwincode-worker/src/lib.rs",
                "line": 414,
                "column": 53,
                "end_line": 414,
                "start_byte": 16656,
                "end_byte": 16674,
                "full_location_ref": "/functional_chains/5/pattern/production_constructions/1/arguments/0/operand/object/member_location"
              },
              "object": {
                "current_referent_value_proven": false,
                "kind": "field_expression",
                "member": "config",
                "location": {
                  "file": "crates/winwincode-worker/src/lib.rs",
                  "line": 414,
                  "column": 41,
                  "end_line": 414,
                  "start_byte": 16644,
                  "end_byte": 16655,
                  "full_location_ref": "/functional_chains/5/pattern/production_constructions/1/arguments/0/operand/object/object/location"
                },
                "member_location": {
                  "file": "crates/winwincode-worker/src/lib.rs",
                  "line": 414,
                  "column": 46,
                  "end_line": 414,
                  "start_byte": 16649,
                  "end_byte": 16655,
                  "full_location_ref": "/functional_chains/5/pattern/production_constructions/1/arguments/0/operand/object/object/member_location"
                },
                "object": {
                  "kind": "self",
                  "name": "self",
                  "location": {
                    "file": "crates/winwincode-worker/src/lib.rs",
                    "line": 414,
                    "column": 41,
                    "end_line": 414,
                    "start_byte": 16644,
                    "end_byte": 16648,
                    "full_location_ref": "/functional_chains/5/pattern/production_constructions/1/arguments/0/operand/object/object/object/location"
                  },
                  "reference": {
                    "declaration_id": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/5/pattern/production_constructions/1/arguments/0/operand/object/object/object/reference/declaration_id"
                    },
                    "declaration_kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/5/pattern/production_constructions/1/arguments/0/operand/object/object/object/reference/declaration_kind"
                    },
                    "identity_scope": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/5/pattern/production_constructions/1/arguments/0/operand/object/object/object/reference/identity_scope"
                    },
                    "macro_namespace_complete": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/5/pattern/production_constructions/1/arguments/0/operand/object/object/object/reference/macro_namespace_complete"
                    },
                    "runtime_value_identity_proven": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/5/pattern/production_constructions/1/arguments/0/operand/object/object/object/reference/runtime_value_identity_proven"
                    },
                    "state": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/5/pattern/production_constructions/1/arguments/0/operand/object/object/object/reference/state"
                    },
                    "binder_location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/5/pattern/production_constructions/1/arguments/0/operand/object/object/object/reference/binder_location"
                    },
                    "declaration_location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/5/pattern/production_constructions/1/arguments/0/operand/object/object/object/reference/declaration_location"
                    }
                  }
                }
              }
            }
          }
        }
      ],
      "callee": {
        "current_referent_value_proven": false,
        "kind": "field_expression",
        "member": "note_worker_instance_id",
        "location": {
          "file": "crates/winwincode-worker/src/lib.rs",
          "line": 414,
          "column": 9,
          "end_line": 414,
          "start_byte": 16612,
          "end_byte": 16642,
          "full_location_ref": "/functional_chains/5/pattern/production_constructions/1/callee/location"
        },
        "member_location": {
          "file": "crates/winwincode-worker/src/lib.rs",
          "line": 414,
          "column": 16,
          "end_line": 414,
          "start_byte": 16619,
          "end_byte": 16642,
          "full_location_ref": "/functional_chains/5/pattern/production_constructions/1/callee/member_location"
        },
        "object": {
          "kind": "identifier",
          "name": "models",
          "location": {
            "file": "crates/winwincode-worker/src/lib.rs",
            "line": 414,
            "column": 9,
            "end_line": 414,
            "start_byte": 16612,
            "end_byte": 16618,
            "full_location_ref": "/functional_chains/5/pattern/production_constructions/1/callee/object/location"
          },
          "reference": {
            "declaration_id": "98410a6f0f960669d5cc89cf571f5516fa51b21564cf5f4d7c9d9cc415cfbc44",
            "declaration_kind": "captured_rust_local",
            "identity_scope": "plain captured binder syntax only",
            "macro_namespace_complete": false,
            "runtime_value_identity_proven": false,
            "state": "captured_unique_rust_binder",
            "binder_location": {
              "file": "crates/winwincode-worker/src/lib.rs",
              "line": 413,
              "column": 17,
              "end_line": 413,
              "start_byte": 16549,
              "end_byte": 16555,
              "full_location_ref": "/functional_chains/5/pattern/production_constructions/1/callee/object/reference/binder_location"
            },
            "declaration_location": {
              "file": "crates/winwincode-worker/src/lib.rs",
              "line": 413,
              "column": 9,
              "end_line": 413,
              "start_byte": 16541,
              "end_byte": 16603,
              "full_location_ref": "/functional_chains/5/pattern/production_constructions/1/callee/object/reference/declaration_location"
            }
          }
        }
      },
      "location": {
        "file": "crates/winwincode-worker/src/lib.rs",
        "line": 414,
        "column": 9,
        "end_line": 414,
        "start_byte": 16612,
        "end_byte": 16677,
        "full_location_ref": "/functional_chains/5/pattern/production_constructions/1/location"
      }
    },
    {
      "source_fact_refs": [
        "/functional_chains/5/source_facts/75"
      ],
      "actual_callee_graph_node_id": null,
      "call_fact_id": "58edbeebfb668b068b3910fc",
      "global_receiver_dispatch_proven": false,
      "id": "fc09e12f041064e89ac3cfbf",
      "kind": "production_construction_call_source",
      "model_id": "source-derived-production-construction-v1",
      "origin": "source-derived",
      "role": "installation",
      "arguments": [
        {
          "kind": "string_literal",
          "literal": "WWC_MODEL_INTAKE_LOG",
          "location": {
            "file": "crates/winwincode-worker/src/lib.rs",
            "line": 415,
            "column": 46,
            "end_line": 415,
            "start_byte": 16724,
            "end_byte": 16746,
            "full_location_ref": "/functional_chains/5/pattern/production_constructions/2/arguments/0/location"
          }
        }
      ],
      "callee": {
        "kind": "scoped_identifier",
        "source": "std::env::var_os",
        "children": [
          {
            "kind": "scoped_identifier",
            "source": "std::env",
            "children": [
              {
                "kind": "identifier",
                "name": "std",
                "location": {
                  "file": "crates/winwincode-worker/src/lib.rs",
                  "line": 415,
                  "column": 29,
                  "end_line": 415,
                  "start_byte": 16707,
                  "end_byte": 16710,
                  "full_location_ref": "/functional_chains/5/pattern/production_constructions/2/callee/children/0/children/0/location"
                },
                "reference": {
                  "plain_binder_candidates": 0,
                  "runtime_value_identity_proven": false,
                  "state": "captured_rust_reference",
                  "text": "std",
                  "location": {
                    "file": "crates/winwincode-worker/src/lib.rs",
                    "line": 415,
                    "column": 29,
                    "end_line": 415,
                    "start_byte": 16707,
                    "end_byte": 16710,
                    "full_location_ref": "/functional_chains/5/pattern/production_constructions/2/callee/children/0/children/0/reference/location"
                  }
                }
              },
              {
                "kind": "identifier",
                "name": "env",
                "location": {
                  "file": "crates/winwincode-worker/src/lib.rs",
                  "line": 415,
                  "column": 34,
                  "end_line": 415,
                  "start_byte": 16712,
                  "end_byte": 16715,
                  "full_location_ref": "/functional_chains/5/pattern/production_constructions/2/callee/children/0/children/1/location"
                },
                "reference": {
                  "plain_binder_candidates": 0,
                  "runtime_value_identity_proven": false,
                  "state": "captured_rust_reference",
                  "text": "env",
                  "location": {
                    "file": "crates/winwincode-worker/src/lib.rs",
                    "line": 415,
                    "column": 34,
                    "end_line": 415,
                    "start_byte": 16712,
                    "end_byte": 16715,
                    "full_location_ref": "/functional_chains/5/pattern/production_constructions/2/callee/children/0/children/1/reference/location"
                  }
                }
              }
            ],
            "location": {
              "file": "crates/winwincode-worker/src/lib.rs",
              "line": 415,
              "column": 29,
              "end_line": 415,
              "start_byte": 16707,
              "end_byte": 16715,
              "full_location_ref": "/functional_chains/5/pattern/production_constructions/2/callee/children/0/location"
            }
          },
          {
            "kind": "identifier",
            "name": "var_os",
            "location": {
              "file": "crates/winwincode-worker/src/lib.rs",
              "line": 415,
              "column": 39,
              "end_line": 415,
              "start_byte": 16717,
              "end_byte": 16723,
              "full_location_ref": "/functional_chains/5/pattern/production_constructions/2/callee/children/1/location"
            },
            "reference": {
              "plain_binder_candidates": 0,
              "runtime_value_identity_proven": false,
              "state": "captured_rust_reference",
              "text": "var_os",
              "location": {
                "file": "crates/winwincode-worker/src/lib.rs",
                "line": 415,
                "column": 39,
                "end_line": 415,
                "start_byte": 16717,
                "end_byte": 16723,
                "full_location_ref": "/functional_chains/5/pattern/production_constructions/2/callee/children/1/reference/location"
              }
            }
          }
        ],
        "location": {
          "file": "crates/winwincode-worker/src/lib.rs",
          "line": 415,
          "column": 29,
          "end_line": 415,
          "start_byte": 16707,
          "end_byte": 16723,
          "full_location_ref": "/functional_chains/5/pattern/production_constructions/2/callee/location"
        }
      },
      "location": {
        "file": "crates/winwincode-worker/src/lib.rs",
        "line": 415,
        "column": 29,
        "end_line": 415,
        "start_byte": 16707,
        "end_byte": 16747,
        "full_location_ref": "/functional_chains/5/pattern/production_constructions/2/location"
      }
    },
    {
      "source_fact_refs": [
        "/functional_chains/5/source_facts/76"
      ],
      "actual_callee_graph_node_id": null,
      "call_fact_id": "380658022f8b3d7648ad1ba4",
      "global_receiver_dispatch_proven": false,
      "id": "6fd04577493afe536ec5176d",
      "kind": "production_construction_call_source",
      "model_id": "source-derived-production-construction-v1",
      "origin": "source-derived",
      "role": "installation",
      "arguments": [
        {
          "call_effects_or_result_proven": false,
          "callee_source": "Some",
          "kind": "call_expression",
          "arguments": [
            {
              "call_effects_or_result_proven": false,
              "callee_source": "std::path::PathBuf::from",
              "kind": "call_expression",
              "arguments": [
                {
                  "kind": "identifier",
                  "name": "path",
                  "location": {
                    "file": "crates/winwincode-worker/src/lib.rs",
                    "line": 416,
                    "column": 65,
                    "end_line": 416,
                    "start_byte": 16814,
                    "end_byte": 16818,
                    "full_location_ref": "/functional_chains/5/pattern/production_constructions/3/arguments/0/arguments/0/arguments/0/location"
                  },
                  "reference": {
                    "plain_binder_candidates": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/5/pattern/production_constructions/3/arguments/0/arguments/0/arguments/0/reference/plain_binder_candidates"
                    },
                    "runtime_value_identity_proven": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/5/pattern/production_constructions/3/arguments/0/arguments/0/arguments/0/reference/runtime_value_identity_proven"
                    },
                    "state": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/5/pattern/production_constructions/3/arguments/0/arguments/0/arguments/0/reference/state"
                    },
                    "text": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/5/pattern/production_constructions/3/arguments/0/arguments/0/arguments/0/reference/text"
                    },
                    "location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/5/pattern/production_constructions/3/arguments/0/arguments/0/arguments/0/reference/location"
                    }
                  }
                }
              ],
              "callee_expression": {
                "kind": "scoped_identifier",
                "source": "std::path::PathBuf::from",
                "children": [
                  {
                    "kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/5/pattern/production_constructions/3/arguments/0/arguments/0/callee_expression/children/0/kind"
                    },
                    "source": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/5/pattern/production_constructions/3/arguments/0/arguments/0/callee_expression/children/0/source"
                    },
                    "children": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/5/pattern/production_constructions/3/arguments/0/arguments/0/callee_expression/children/0/children"
                    },
                    "location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/5/pattern/production_constructions/3/arguments/0/arguments/0/callee_expression/children/0/location"
                    }
                  },
                  {
                    "remaining_fields_ref": "/functional_chains/5/pattern/production_constructions/3/arguments/0/arguments/0/callee_expression/children/1"
                  }
                ],
                "remaining_fields_ref": "/functional_chains/5/pattern/production_constructions/3/arguments/0/arguments/0/callee_expression"
              },
              "remaining_fields_ref": "/functional_chains/5/pattern/production_constructions/3/arguments/0/arguments/0"
            }
          ],
          "remaining_fields_ref": "/functional_chains/5/pattern/production_constructions/3/arguments/0"
        }
      ],
      "remaining_fields_ref": "/functional_chains/5/pattern/production_constructions/3"
    }
  ],
  "shown_count": 4,
  "total_count": 67,
  "truncated": true,
  "full_value_ref": "/functional_chains/5/pattern/production_constructions"
}
```

自动关系类型：`{"boundary_result_source": 1, "captured_call_step": 68, "production_construction_call_source": 67, "provider_installation_assignment_source": 2, "report_source_role": 4}`。

分析缺口：

```json
[
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

保存发现：`9e6f9a052635cfe39709cfcb`；证据：`b5c22276425869081b036a8e`。

- `kernel_create`：`crates/kernel/src/lib.rs` / `Kernel.create_session`。

`kernel_create` 的正常源码顺序：

- `Self::guard / self.runtime / Self::session_config / runtime
                .manager
                .start_thread(StartThreadOptions::new(config.clone()))
                .await
                .map_err / runtime
                .manager
                .start_thread / StartThreadOptions::new / config.clone / Box::pin / self.register_session`，`crates/kernel/src/lib.rs:1221`。

保存关系的展示摘要（`presentation_only=true`；不新增评级）：

完整 pattern：`/functional_chains/6/pattern`。展示截断：`true`；完整证据与原 pattern 保留。

| 保存字段 | 实际值 | 完整引用 |
| --- | --- | --- |
| scoped_source_supported | true | /functional_chains/6/pattern/scoped_source_supported |

**nested_source_regions**：`/functional_chains/6/pattern/nested_source_regions`；展示截断：`false`。

```json
[
  {
    "source_fact_refs": [
      "/functional_chains/6/source_facts/24"
    ],
    "body_activation_proven": false,
    "future_fulfillment_proven": false,
    "id": "94663e096f62c84dfd5647eb",
    "kind": "deferred_source_region_sequence",
    "nested_calls_promoted_to_resolved": false,
    "origin": "source-derived",
    "role": "kernel_create",
    "conditions": [
      "this deferred captured body is activated and the recorded statements are reached normally"
    ],
    "location": {
      "file": "crates/kernel/src/lib.rs",
      "line": 1221,
      "column": 21,
      "end_line": 1230,
      "start_byte": 44514,
      "end_byte": 44981,
      "full_location_ref": "/functional_chains/6/pattern/nested_source_regions/0/location"
    },
    "sequence": {
      "all_function_paths_or_effects_accounted": false,
      "future_or_callback_activation_proven": false,
      "region_kind": "async_block",
      "role": "kernel_create",
      "assignment_attempts": [],
      "call_result_guard_source_links": [],
      "conditions": [],
      "guards": [],
      "opaque_direct_control_regions": [],
      "orders": [
        {
          "source_fact_refs": [
            "/functional_chains/6/source_facts/21"
          ],
          "after_step_id": "e5bc9708256c5d88bd42401d",
          "all_paths_reach_next_proven": false,
          "before_step_id": "320a72e058dd618cc4cf5fe7",
          "id": "83d107da963e01963366fab5",
          "kind": "conditional_direct_statement_order",
          "model_id": "captured-normal-statement-control-v1",
          "origin": "source-derived",
          "role": "kernel_create",
          "conditions": [
            "both direct statements normally reached in the same invocation",
            "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
          ],
          "location": {
            "file": "crates/kernel/src/lib.rs",
            "line": 1223,
            "column": 13,
            "end_line": 1223,
            "start_byte": 44583,
            "end_byte": 44644,
            "full_location_ref": "/functional_chains/6/pattern/nested_source_regions/0/sequence/orders/0/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/6/source_facts/22"
          ],
          "after_step_id": "afcd18fd4eb6a6ac643f3830",
          "all_paths_reach_next_proven": false,
          "before_step_id": "e5bc9708256c5d88bd42401d",
          "id": "82c6f28846644bd2fe69cc11",
          "kind": "conditional_direct_statement_order",
          "model_id": "captured-normal-statement-control-v1",
          "origin": "source-derived",
          "role": "kernel_create",
          "conditions": [
            "both direct statements normally reached in the same invocation",
            "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
          ],
          "location": {
            "file": "crates/kernel/src/lib.rs",
            "line": 1224,
            "column": 13,
            "end_line": 1228,
            "start_byte": 44657,
            "end_byte": 44895,
            "full_location_ref": "/functional_chains/6/pattern/nested_source_regions/0/sequence/orders/1/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/6/source_facts/23"
          ],
          "after_step_id": "f34121a33c4e947c3980395e",
          "all_paths_reach_next_proven": false,
          "before_step_id": "afcd18fd4eb6a6ac643f3830",
          "id": "3b70dcf519311b83cea7f642",
          "kind": "conditional_direct_statement_order",
          "model_id": "captured-normal-statement-control-v1",
          "origin": "source-derived",
          "role": "kernel_create",
          "conditions": [
            "both direct statements normally reached in the same invocation",
            "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
          ],
          "location": {
            "file": "crates/kernel/src/lib.rs",
            "line": 1229,
            "column": 13,
            "end_line": 1229,
            "start_byte": 44908,
            "end_byte": 44971,
            "full_location_ref": "/functional_chains/6/pattern/nested_source_regions/0/sequence/orders/2/location"
          }
        }
      ],
      "source_region_location": {
        "file": "crates/kernel/src/lib.rs",
        "line": 1221,
        "column": 21,
        "end_line": 1230,
        "start_byte": 44514,
        "end_byte": 44981,
        "full_location_ref": "/functional_chains/6/pattern/nested_source_regions/0/sequence/source_region_location"
      },
      "steps": [
        {
          "source_fact_refs": [
            "/functional_chains/6/source_facts/14"
          ],
          "conditional_normal_reaching_only": true,
          "id": "320a72e058dd618cc4cf5fe7",
          "kind": "direct_statement_call_step",
          "origin": "source-derived",
          "role": "kernel_create",
          "source_order_index": 0,
          "statement_kind": "let_declaration",
          "call_ids": [
            "8bd18e3f6fe4849819fe5978"
          ],
          "location": {
            "file": "crates/kernel/src/lib.rs",
            "line": 1222,
            "column": 13,
            "end_line": 1222,
            "start_byte": 44534,
            "end_byte": 44570,
            "full_location_ref": "/functional_chains/6/pattern/nested_source_regions/0/sequence/steps/0/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/6/source_facts/15"
          ],
          "conditional_normal_reaching_only": true,
          "id": "e5bc9708256c5d88bd42401d",
          "kind": "direct_statement_call_step",
          "origin": "source-derived",
          "role": "kernel_create",
          "source_order_index": 1,
          "statement_kind": "let_declaration",
          "call_ids": [
            "b70204a6689c25fc84f89fab"
          ],
          "location": {
            "file": "crates/kernel/src/lib.rs",
            "line": 1223,
            "column": 13,
            "end_line": 1223,
            "start_byte": 44583,
            "end_byte": 44644,
            "full_location_ref": "/functional_chains/6/pattern/nested_source_regions/0/sequence/steps/1/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/6/source_facts/16"
          ],
          "conditional_normal_reaching_only": true,
          "id": "afcd18fd4eb6a6ac643f3830",
          "kind": "direct_statement_call_step",
          "origin": "source-derived",
          "role": "kernel_create",
          "source_order_index": 2,
          "statement_kind": "let_declaration",
          "call_ids": [
            "6ecff274f3f11e187423129d",
            "d4e5418c20f92f9cf12c10f5",
            "9a9b9a04ac7ca3204caa8be6",
            "41d75536c8cc265dfb8ae201"
          ],
          "location": {
            "file": "crates/kernel/src/lib.rs",
            "line": 1224,
            "column": 13,
            "end_line": 1228,
            "start_byte": 44657,
            "end_byte": 44895,
            "full_location_ref": "/functional_chains/6/pattern/nested_source_regions/0/sequence/steps/2/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/6/source_facts/17"
          ],
          "conditional_normal_reaching_only": true,
          "id": "f34121a33c4e947c3980395e",
          "kind": "direct_statement_call_step",
          "origin": "source-derived",
          "role": "kernel_create",
          "source_order_index": 3,
          "statement_kind": "await_expression",
          "call_ids": [
            "2ccb5973b6e52ebc22939c6a",
            "2fac46c00fbdf8ca65bfacd0"
          ],
          "location": {
            "file": "crates/kernel/src/lib.rs",
            "line": 1229,
            "column": 13,
            "end_line": 1229,
            "start_byte": 44908,
            "end_byte": 44971,
            "full_location_ref": "/functional_chains/6/pattern/nested_source_regions/0/sequence/steps/3/location"
          }
        }
      ]
    }
  }
]
```

**sequences**：`/functional_chains/6/pattern/sequences`；展示截断：`true`。

```json
{
  "kernel_create": {
    "all_function_paths_or_effects_accounted": false,
    "future_or_callback_activation_proven": false,
    "region_kind": "function_item",
    "role": "kernel_create",
    "assignment_attempts": [],
    "call_result_guard_source_links": [],
    "conditions": [],
    "guards": [],
    "opaque_direct_control_regions": [],
    "orders": [],
    "source_region_location": {
      "file": "crates/kernel/src/lib.rs",
      "line": 1220,
      "column": 5,
      "end_line": 1232,
      "start_byte": 44403,
      "end_byte": 45003,
      "full_location_ref": "/functional_chains/6/pattern/sequences/kernel_create/source_region_location"
    },
    "steps": [
      {
        "source_fact_refs": [
          "/functional_chains/6/source_facts/10"
        ],
        "conditional_normal_reaching_only": true,
        "id": "6bfac8c7f5f86017748e7ba6",
        "kind": "direct_statement_call_step",
        "origin": "source-derived",
        "role": "kernel_create",
        "source_order_index": 0,
        "statement_kind": "await_expression",
        "call_ids": {
          "shown_items": [
            "8695f0ed2ad4822c5421de66",
            "8bd18e3f6fe4849819fe5978",
            "b70204a6689c25fc84f89fab",
            "6ecff274f3f11e187423129d",
            "d4e5418c20f92f9cf12c10f5",
            "9a9b9a04ac7ca3204caa8be6"
          ],
          "shown_count": 6,
          "total_count": 9,
          "truncated": true,
          "full_value_ref": "/functional_chains/6/pattern/sequences/kernel_create/steps/0/call_ids"
        },
        "location": {
          "file": "crates/kernel/src/lib.rs",
          "line": 1221,
          "column": 9,
          "end_line": 1231,
          "start_byte": 44502,
          "end_byte": 44997,
          "full_location_ref": "/functional_chains/6/pattern/sequences/kernel_create/steps/0/location"
        }
      }
    ]
  }
}
```

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

保存发现：`557da6f8cb10a7baed663d3b`；证据：`15fa9079162b552d1f0ad5d1`。

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

保存关系的展示摘要（`presentation_only=true`；不新增评级）：

完整 pattern：`/functional_chains/7/pattern`。展示截断：`true`；完整证据与原 pattern 保留。

| 保存字段 | 实际值 | 完整引用 |
| --- | --- | --- |
| scoped_source_supported | true | /functional_chains/7/pattern/scoped_source_supported |

**nested_source_regions**：`/functional_chains/7/pattern/nested_source_regions`；展示截断：`true`。

```json
[
  {
    "source_fact_refs": [
      "/functional_chains/7/source_facts/55"
    ],
    "body_activation_proven": false,
    "future_fulfillment_proven": false,
    "id": "4b5bfecc921378671ac24ec6",
    "kind": "deferred_source_region_sequence",
    "nested_calls_promoted_to_resolved": false,
    "origin": "source-derived",
    "role": "kernel_reconcile",
    "conditions": [
      "this deferred captured body is activated and the recorded statements are reached normally"
    ],
    "location": {
      "file": "crates/kernel/src/lib.rs",
      "line": 1376,
      "column": 21,
      "end_line": 1432,
      "start_byte": 50583,
      "end_byte": 53102,
      "full_location_ref": "/functional_chains/7/pattern/nested_source_regions/0/location"
    },
    "sequence": {
      "all_function_paths_or_effects_accounted": false,
      "future_or_callback_activation_proven": false,
      "region_kind": "async_block",
      "role": "kernel_reconcile",
      "assignment_attempts": [],
      "call_result_guard_source_links": [],
      "conditions": [
        {
          "source_fact_refs": [
            "/functional_chains/7/source_facts/26",
            "/functional_chains/7/source_facts/41"
          ],
          "id": "8b85ee660787e07af8da6fe8",
          "kind": "source_guard_and_abrupt_branch",
          "origin": "source-derived",
          "role": "kernel_reconcile",
          "runtime_predicate_proven": false,
          "branch_context": [],
          "branches": [
            {
              "branch": "then",
              "branch_all_paths_abrupt_proven": true,
              "abrupt_source_expressions": [
                {
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/conditions/0/branches/0/abrupt_source_expressions/0/kind"
                  },
                  "runtime_completion_proven": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/conditions/0/branches/0/abrupt_source_expressions/0/runtime_completion_proven"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/conditions/0/branches/0/abrupt_source_expressions/0/location"
                  },
                  "returned_expression": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression"
                  }
                }
              ],
              "call_ids": [
                "086e532adbc1ae1f287569aa",
                "def0da47a92040e467535a54"
              ]
            }
          ],
          "condition": {
            "kind": "binary_expression",
            "operator": "||",
            "runtime_predicate_or_assignment_proven": false,
            "location": {
              "file": "crates/kernel/src/lib.rs",
              "line": 1377,
              "column": 16,
              "end_line": 1377,
              "start_byte": 50606,
              "end_byte": 50657,
              "full_location_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/conditions/0/condition/location"
            },
            "operands": [
              {
                "call_effects_or_result_proven": false,
                "callee_source": "turn_id.trim().is_empty",
                "kind": "call_expression",
                "arguments": [],
                "callee_expression": {
                  "current_referent_value_proven": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/conditions/0/condition/operands/0/callee_expression/current_referent_value_proven"
                  },
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/conditions/0/condition/operands/0/callee_expression/kind"
                  },
                  "member": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/conditions/0/condition/operands/0/callee_expression/member"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/conditions/0/condition/operands/0/callee_expression/location"
                  },
                  "member_location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/conditions/0/condition/operands/0/callee_expression/member_location"
                  },
                  "object": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/conditions/0/condition/operands/0/callee_expression/object"
                  }
                },
                "location": {
                  "file": "crates/kernel/src/lib.rs",
                  "line": 1377,
                  "column": 16,
                  "end_line": 1377,
                  "start_byte": 50606,
                  "end_byte": 50631,
                  "full_location_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/conditions/0/condition/operands/0/location"
                }
              },
              {
                "call_effects_or_result_proven": false,
                "callee_source": "text.trim().is_empty",
                "kind": "call_expression",
                "arguments": [],
                "callee_expression": {
                  "current_referent_value_proven": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/conditions/0/condition/operands/1/callee_expression/current_referent_value_proven"
                  },
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/conditions/0/condition/operands/1/callee_expression/kind"
                  },
                  "member": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/conditions/0/condition/operands/1/callee_expression/member"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/conditions/0/condition/operands/1/callee_expression/location"
                  },
                  "member_location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/conditions/0/condition/operands/1/callee_expression/member_location"
                  },
                  "object": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/conditions/0/condition/operands/1/callee_expression/object"
                  }
                },
                "location": {
                  "file": "crates/kernel/src/lib.rs",
                  "line": 1377,
                  "column": 45,
                  "end_line": 1377,
                  "start_byte": 50635,
                  "end_byte": 50657,
                  "full_location_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/conditions/0/condition/operands/1/location"
                }
              }
            ]
          },
          "location": {
            "file": "crates/kernel/src/lib.rs",
            "line": 1377,
            "column": 13,
            "end_line": 1382,
            "start_byte": 50603,
            "end_byte": 50853,
            "full_location_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/conditions/0/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/7/source_facts/32",
            "/functional_chains/7/source_facts/47"
          ],
          "id": "65864286def9c4ffe785a67f",
          "kind": "source_guard_and_abrupt_branch",
          "origin": "source-derived",
          "role": "kernel_reconcile",
          "runtime_predicate_proven": false,
          "branch_context": [
            {
              "activation_proven": false,
              "kind": "match_arm",
              "location": {
                "file": "crates/kernel/src/lib.rs",
                "line": 1403,
                "column": 17,
                "end_line": 1428,
                "start_byte": 51733,
                "end_byte": 53009,
                "full_location_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/conditions/1/branch_context/0/location"
              }
            }
          ],
          "branches": [
            {
              "branch": "then",
              "branch_all_paths_abrupt_proven": false,
              "abrupt_source_expressions": [],
              "call_ids": [
                "40995bc37b4a926b34812d17",
                "68a1a1c5b3d3b315046237d5"
              ]
            },
            {
              "branch": "else",
              "branch_all_paths_abrupt_proven": false,
              "abrupt_source_expressions": [],
              "call_ids": [
                "ec1b59b46ffe80f6c5561608",
                "ad33a6f90c8c2933a90d52ba"
              ]
            }
          ],
          "condition": {
            "kind": "identifier",
            "name": "recovered",
            "location": {
              "file": "crates/kernel/src/lib.rs",
              "line": 1405,
              "column": 41,
              "end_line": 1405,
              "start_byte": 51934,
              "end_byte": 51943,
              "full_location_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/conditions/1/condition/location"
            },
            "reference": {
              "declaration_id": "00b29b274c64d29ec50242d819c6b7b652965c3052251649e6f2b325c4b474a7",
              "declaration_kind": "captured_rust_local",
              "identity_scope": "plain captured binder syntax only",
              "macro_namespace_complete": false,
              "runtime_value_identity_proven": false,
              "state": "captured_unique_rust_binder",
              "binder_location": {
                "file": "crates/kernel/src/lib.rs",
                "line": 1404,
                "column": 25,
                "end_line": 1404,
                "start_byte": 51828,
                "end_byte": 51837,
                "full_location_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/conditions/1/condition/reference/binder_location"
              },
              "declaration_location": {
                "file": "crates/kernel/src/lib.rs",
                "line": 1404,
                "column": 21,
                "end_line": 1404,
                "start_byte": 51824,
                "end_byte": 51893,
                "full_location_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/conditions/1/condition/reference/declaration_location"
              }
            }
          },
          "location": {
            "file": "crates/kernel/src/lib.rs",
            "line": 1405,
            "column": 38,
            "end_line": 1420,
            "start_byte": 51931,
            "end_byte": 52657,
            "full_location_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/conditions/1/location"
          }
        }
      ],
      "guards": [],
      "opaque_direct_control_regions": [],
      "orders": [
        {
          "source_fact_refs": [
            "/functional_chains/7/source_facts/49"
          ],
          "after_step_id": "c6e1bf395af63015f3f83891",
          "all_paths_reach_next_proven": false,
          "before_step_id": "5bfbf1c0bf394e654fed8204",
          "id": "c4c157efdf6a67cbba170028",
          "kind": "conditional_direct_statement_order",
          "model_id": "captured-normal-statement-control-v1",
          "origin": "source-derived",
          "role": "kernel_reconcile",
          "conditions": [
            "both direct statements normally reached in the same invocation",
            "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
          ],
          "location": {
            "file": "crates/kernel/src/lib.rs",
            "line": 1383,
            "column": 13,
            "end_line": 1383,
            "start_byte": 50866,
            "end_byte": 50902,
            "full_location_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/orders/0/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/7/source_facts/50"
          ],
          "after_step_id": "2acc4dbe59df07d4bd7bd22d",
          "all_paths_reach_next_proven": false,
          "before_step_id": "c6e1bf395af63015f3f83891",
          "id": "fa160550cd06a8a31118bf1c",
          "kind": "conditional_direct_statement_order",
          "model_id": "captured-normal-statement-control-v1",
          "origin": "source-derived",
          "role": "kernel_reconcile",
          "conditions": [
            "both direct statements normally reached in the same invocation",
            "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
          ],
          "location": {
            "file": "crates/kernel/src/lib.rs",
            "line": 1384,
            "column": 13,
            "end_line": 1384,
            "start_byte": 50915,
            "end_byte": 50971,
            "full_location_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/orders/1/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/7/source_facts/51"
          ],
          "after_step_id": "a25526effc8822235e6bc81f",
          "all_paths_reach_next_proven": false,
          "before_step_id": "2acc4dbe59df07d4bd7bd22d",
          "id": "4ebc00556137bc8662f2ae20",
          "kind": "conditional_direct_statement_order",
          "model_id": "captured-normal-statement-control-v1",
          "origin": "source-derived",
          "role": "kernel_reconcile",
          "conditions": [
            "both direct statements normally reached in the same invocation",
            "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
          ],
          "location": {
            "file": "crates/kernel/src/lib.rs",
            "line": 1385,
            "column": 13,
            "end_line": 1385,
            "start_byte": 50984,
            "end_byte": 51020,
            "full_location_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/orders/2/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/7/source_facts/52"
          ],
          "after_step_id": "e23c220ea1d3f65386d0da24",
          "all_paths_reach_next_proven": false,
          "before_step_id": "a25526effc8822235e6bc81f",
          "id": "0083f2418aa9a505d9143b25",
          "kind": "conditional_direct_statement_order",
          "model_id": "captured-normal-statement-control-v1",
          "origin": "source-derived",
          "role": "kernel_reconcile",
          "conditions": [
            "both direct statements normally reached in the same invocation",
            "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
          ],
          "location": {
            "file": "crates/kernel/src/lib.rs",
            "line": 1386,
            "column": 13,
            "end_line": 1395,
            "start_byte": 51033,
            "end_byte": 51379,
            "full_location_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/orders/3/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/7/source_facts/53"
          ],
          "after_step_id": "9dd0471c9fd44ac37d39ee4b",
          "all_paths_reach_next_proven": false,
          "before_step_id": "e23c220ea1d3f65386d0da24",
          "id": "5193c5db9fddb187e7395c63",
          "kind": "conditional_direct_statement_order",
          "model_id": "captured-normal-statement-control-v1",
          "origin": "source-derived",
          "role": "kernel_reconcile",
          "conditions": [
            "both direct statements normally reached in the same invocation",
            "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
          ],
          "location": {
            "file": "crates/kernel/src/lib.rs",
            "line": 1396,
            "column": 13,
            "end_line": 1429,
            "start_byte": 51392,
            "end_byte": 53024,
            "full_location_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/orders/4/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/7/source_facts/54"
          ],
          "after_step_id": "cbd16bd874ef08f047293470",
          "all_paths_reach_next_proven": false,
          "before_step_id": "9dd0471c9fd44ac37d39ee4b",
          "id": "396090d5d640a5ad10a79e9f",
          "kind": "conditional_direct_statement_order",
          "model_id": "captured-normal-statement-control-v1",
          "origin": "source-derived",
          "role": "kernel_reconcile",
          "conditions": [
            "both direct statements normally reached in the same invocation",
            "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
          ],
          "location": {
            "file": "crates/kernel/src/lib.rs",
            "line": 1430,
            "column": 13,
            "end_line": 1430,
            "start_byte": 53037,
            "end_byte": 53073,
            "full_location_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/orders/5/location"
          }
        }
      ],
      "source_region_location": {
        "file": "crates/kernel/src/lib.rs",
        "line": 1376,
        "column": 21,
        "end_line": 1432,
        "start_byte": 50583,
        "end_byte": 53102,
        "full_location_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/source_region_location"
      },
      "steps": {
        "shown_items": [
          {
            "source_fact_refs": [
              "/functional_chains/7/source_facts/34"
            ],
            "conditional_normal_reaching_only": true,
            "id": "5bfbf1c0bf394e654fed8204",
            "kind": "direct_statement_call_step",
            "origin": "source-derived",
            "role": "kernel_reconcile",
            "source_order_index": 0,
            "statement_kind": "expression_statement",
            "call_ids": [
              "0e5c13e56d195f5286b5acc4",
              "40dc31cd99f073033724f420",
              "abaddca10a0a8b65f9312f07",
              "eb1f4cb74f20f97298ee4ea3",
              "086e532adbc1ae1f287569aa",
              "def0da47a92040e467535a54"
            ],
            "location": {
              "file": "crates/kernel/src/lib.rs",
              "line": 1377,
              "column": 13,
              "end_line": 1382,
              "start_byte": 50603,
              "end_byte": 50853,
              "full_location_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/steps/0/location"
            }
          },
          {
            "source_fact_refs": [
              "/functional_chains/7/source_facts/35"
            ],
            "conditional_normal_reaching_only": true,
            "id": "c6e1bf395af63015f3f83891",
            "kind": "direct_statement_call_step",
            "origin": "source-derived",
            "role": "kernel_reconcile",
            "source_order_index": 1,
            "statement_kind": "let_declaration",
            "call_ids": [
              "9dd2c935e4c75ad9667a549e"
            ],
            "location": {
              "file": "crates/kernel/src/lib.rs",
              "line": 1383,
              "column": 13,
              "end_line": 1383,
              "start_byte": 50866,
              "end_byte": 50902,
              "full_location_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/steps/1/location"
            }
          },
          {
            "source_fact_refs": [
              "/functional_chains/7/source_facts/36"
            ],
            "remaining_fields_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/steps/2"
          }
        ],
        "shown_count": 3,
        "total_count": 7,
        "truncated": true,
        "full_value_ref": "/functional_chains/7/pattern/nested_source_regions/0/sequence/steps"
      }
    }
  }
]
```

**sequences**：`/functional_chains/7/pattern/sequences`；展示截断：`true`。

```json
{
  "kernel_reconcile": {
    "all_function_paths_or_effects_accounted": false,
    "future_or_callback_activation_proven": false,
    "region_kind": "function_item",
    "role": "kernel_reconcile",
    "assignment_attempts": [],
    "call_result_guard_source_links": [],
    "conditions": [
      {
        "source_fact_refs": [
          "/functional_chains/7/source_facts/26",
          "/functional_chains/7/source_facts/41"
        ],
        "id": "8b85ee660787e07af8da6fe8",
        "kind": "source_guard_and_abrupt_branch",
        "origin": "source-derived",
        "role": "kernel_reconcile",
        "runtime_predicate_proven": false,
        "branch_context": [],
        "branches": [
          {
            "branch": "then",
            "branch_all_paths_abrupt_proven": true,
            "abrupt_source_expressions": [
              {
                "kind": "return_expression",
                "runtime_completion_proven": false,
                "location": {
                  "file": "crates/kernel/src/lib.rs",
                  "line": 1378,
                  "column": 17,
                  "end_line": 1381,
                  "start_byte": 50676,
                  "end_byte": 50838,
                  "full_location_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/0/branches/0/abrupt_source_expressions/0/location"
                },
                "returned_expression": {
                  "call_effects_or_result_proven": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/call_effects_or_result_proven"
                  },
                  "callee_source": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/callee_source"
                  },
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/kind"
                  },
                  "arguments": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/arguments"
                  },
                  "callee_expression": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/callee_expression"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/location"
                  }
                }
              }
            ],
            "call_ids": [
              "086e532adbc1ae1f287569aa",
              "def0da47a92040e467535a54"
            ]
          }
        ],
        "condition": {
          "kind": "binary_expression",
          "operator": "||",
          "runtime_predicate_or_assignment_proven": false,
          "location": {
            "file": "crates/kernel/src/lib.rs",
            "line": 1377,
            "column": 16,
            "end_line": 1377,
            "start_byte": 50606,
            "end_byte": 50657,
            "full_location_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/0/condition/location"
          },
          "operands": [
            {
              "call_effects_or_result_proven": false,
              "callee_source": "turn_id.trim().is_empty",
              "kind": "call_expression",
              "arguments": [],
              "callee_expression": {
                "current_referent_value_proven": false,
                "kind": "field_expression",
                "member": "is_empty",
                "location": {
                  "file": "crates/kernel/src/lib.rs",
                  "line": 1377,
                  "column": 16,
                  "end_line": 1377,
                  "start_byte": 50606,
                  "end_byte": 50629,
                  "full_location_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/0/condition/operands/0/callee_expression/location"
                },
                "member_location": {
                  "file": "crates/kernel/src/lib.rs",
                  "line": 1377,
                  "column": 31,
                  "end_line": 1377,
                  "start_byte": 50621,
                  "end_byte": 50629,
                  "full_location_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/0/condition/operands/0/callee_expression/member_location"
                },
                "object": {
                  "call_effects_or_result_proven": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/0/condition/operands/0/callee_expression/object/call_effects_or_result_proven"
                  },
                  "callee_source": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/0/condition/operands/0/callee_expression/object/callee_source"
                  },
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/0/condition/operands/0/callee_expression/object/kind"
                  },
                  "arguments": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/0/condition/operands/0/callee_expression/object/arguments"
                  },
                  "callee_expression": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/0/condition/operands/0/callee_expression/object/callee_expression"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/0/condition/operands/0/callee_expression/object/location"
                  }
                }
              },
              "location": {
                "file": "crates/kernel/src/lib.rs",
                "line": 1377,
                "column": 16,
                "end_line": 1377,
                "start_byte": 50606,
                "end_byte": 50631,
                "full_location_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/0/condition/operands/0/location"
              }
            },
            {
              "call_effects_or_result_proven": false,
              "callee_source": "text.trim().is_empty",
              "kind": "call_expression",
              "arguments": [],
              "callee_expression": {
                "current_referent_value_proven": false,
                "kind": "field_expression",
                "member": "is_empty",
                "location": {
                  "file": "crates/kernel/src/lib.rs",
                  "line": 1377,
                  "column": 45,
                  "end_line": 1377,
                  "start_byte": 50635,
                  "end_byte": 50655,
                  "full_location_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/0/condition/operands/1/callee_expression/location"
                },
                "member_location": {
                  "file": "crates/kernel/src/lib.rs",
                  "line": 1377,
                  "column": 57,
                  "end_line": 1377,
                  "start_byte": 50647,
                  "end_byte": 50655,
                  "full_location_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/0/condition/operands/1/callee_expression/member_location"
                },
                "object": {
                  "call_effects_or_result_proven": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/0/condition/operands/1/callee_expression/object/call_effects_or_result_proven"
                  },
                  "callee_source": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/0/condition/operands/1/callee_expression/object/callee_source"
                  },
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/0/condition/operands/1/callee_expression/object/kind"
                  },
                  "arguments": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/0/condition/operands/1/callee_expression/object/arguments"
                  },
                  "callee_expression": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/0/condition/operands/1/callee_expression/object/callee_expression"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/0/condition/operands/1/callee_expression/object/location"
                  }
                }
              },
              "location": {
                "file": "crates/kernel/src/lib.rs",
                "line": 1377,
                "column": 45,
                "end_line": 1377,
                "start_byte": 50635,
                "end_byte": 50657,
                "full_location_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/0/condition/operands/1/location"
              }
            }
          ]
        },
        "location": {
          "file": "crates/kernel/src/lib.rs",
          "line": 1377,
          "column": 13,
          "end_line": 1382,
          "start_byte": 50603,
          "end_byte": 50853,
          "full_location_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/0/location"
        }
      },
      {
        "source_fact_refs": [
          "/functional_chains/7/source_facts/32",
          "/functional_chains/7/source_facts/47"
        ],
        "id": "65864286def9c4ffe785a67f",
        "kind": "source_guard_and_abrupt_branch",
        "origin": "source-derived",
        "role": "kernel_reconcile",
        "runtime_predicate_proven": false,
        "branch_context": [
          {
            "activation_proven": false,
            "kind": "match_arm",
            "location": {
              "file": "crates/kernel/src/lib.rs",
              "line": 1403,
              "column": 17,
              "end_line": 1428,
              "start_byte": 51733,
              "end_byte": 53009,
              "full_location_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/1/branch_context/0/location"
            }
          }
        ],
        "branches": [
          {
            "branch": "then",
            "branch_all_paths_abrupt_proven": false,
            "abrupt_source_expressions": [],
            "call_ids": [
              "40995bc37b4a926b34812d17",
              "68a1a1c5b3d3b315046237d5"
            ]
          },
          {
            "branch": "else",
            "branch_all_paths_abrupt_proven": false,
            "abrupt_source_expressions": [],
            "call_ids": [
              "ec1b59b46ffe80f6c5561608",
              "ad33a6f90c8c2933a90d52ba"
            ]
          }
        ],
        "condition": {
          "kind": "identifier",
          "name": "recovered",
          "location": {
            "file": "crates/kernel/src/lib.rs",
            "line": 1405,
            "column": 41,
            "end_line": 1405,
            "start_byte": 51934,
            "end_byte": 51943,
            "full_location_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/1/condition/location"
          },
          "reference": {
            "declaration_id": "00b29b274c64d29ec50242d819c6b7b652965c3052251649e6f2b325c4b474a7",
            "declaration_kind": "captured_rust_local",
            "identity_scope": "plain captured binder syntax only",
            "macro_namespace_complete": false,
            "runtime_value_identity_proven": false,
            "state": "captured_unique_rust_binder",
            "binder_location": {
              "file": "crates/kernel/src/lib.rs",
              "line": 1404,
              "column": 25,
              "end_line": 1404,
              "start_byte": 51828,
              "end_byte": 51837,
              "full_location_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/1/condition/reference/binder_location"
            },
            "declaration_location": {
              "file": "crates/kernel/src/lib.rs",
              "line": 1404,
              "column": 21,
              "end_line": 1404,
              "start_byte": 51824,
              "end_byte": 51893,
              "full_location_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/1/condition/reference/declaration_location"
            }
          }
        },
        "location": {
          "file": "crates/kernel/src/lib.rs",
          "line": 1405,
          "column": 38,
          "end_line": 1420,
          "start_byte": 51931,
          "end_byte": 52657,
          "full_location_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/conditions/1/location"
        }
      }
    ],
    "guards": [],
    "opaque_direct_control_regions": [],
    "orders": [],
    "source_region_location": {
      "file": "crates/kernel/src/lib.rs",
      "line": 1369,
      "column": 5,
      "end_line": 1434,
      "start_byte": 50351,
      "end_byte": 53124,
      "full_location_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/source_region_location"
    },
    "steps": [
      {
        "source_fact_refs": [
          "/functional_chains/7/source_facts/25"
        ],
        "conditional_normal_reaching_only": true,
        "id": "9c285e811f4b69746341edfa",
        "kind": "direct_statement_call_step",
        "origin": "source-derived",
        "role": "kernel_reconcile",
        "source_order_index": 0,
        "statement_kind": "await_expression",
        "call_ids": {
          "shown_items": [
            "bbf3a2043deae32a2415bc2d",
            "0e5c13e56d195f5286b5acc4",
            "40dc31cd99f073033724f420",
            "abaddca10a0a8b65f9312f07",
            "eb1f4cb74f20f97298ee4ea3",
            "086e532adbc1ae1f287569aa"
          ],
          "shown_count": 6,
          "total_count": 24,
          "truncated": true,
          "full_value_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/steps/0/call_ids"
        },
        "location": {
          "file": "crates/kernel/src/lib.rs",
          "line": 1376,
          "column": 9,
          "end_line": 1433,
          "start_byte": 50571,
          "end_byte": 53118,
          "full_location_ref": "/functional_chains/7/pattern/sequences/kernel_reconcile/steps/0/location"
        }
      }
    ]
  }
}
```

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

保存发现：`42977c03f1c8a2a9e2521666`；证据：`0bd42c038dd5d829bbc1821f`。

- `kernel_submit`：`crates/kernel/src/lib.rs` / `Kernel.submit_turn`。

`kernel_submit` 的正常源码顺序：

- `Self::guard / text.trim().is_empty / text.trim / Err / KernelFailure::new / self.runtime / self.session / self.enforce_private_permissions / session
                .thread
                .start_or_steer_turn(user_text_request(text, &options))
                .await
                .map_err / session
                .thread
                .start_or_steer_turn / user_text_request / self.enforce_private_permissions / Ok / submission_info`，`crates/kernel/src/lib.rs:1339`。

保存关系的展示摘要（`presentation_only=true`；不新增评级）：

完整 pattern：`/functional_chains/8/pattern`。展示截断：`true`；完整证据与原 pattern 保留。

| 保存字段 | 实际值 | 完整引用 |
| --- | --- | --- |
| scoped_source_supported | true | /functional_chains/8/pattern/scoped_source_supported |

**nested_source_regions**：`/functional_chains/8/pattern/nested_source_regions`；展示截断：`true`。

```json
[
  {
    "source_fact_refs": [
      "/functional_chains/8/source_facts/41"
    ],
    "body_activation_proven": false,
    "future_fulfillment_proven": false,
    "id": "d9b2044f73f4aae62ce5e783",
    "kind": "deferred_source_region_sequence",
    "nested_calls_promoted_to_resolved": false,
    "origin": "source-derived",
    "role": "kernel_submit",
    "conditions": [
      "this deferred captured body is activated and the recorded statements are reached normally"
    ],
    "location": {
      "file": "crates/kernel/src/lib.rs",
      "line": 1339,
      "column": 21,
      "end_line": 1356,
      "start_byte": 49122,
      "end_byte": 49859,
      "full_location_ref": "/functional_chains/8/pattern/nested_source_regions/0/location"
    },
    "sequence": {
      "all_function_paths_or_effects_accounted": false,
      "future_or_callback_activation_proven": false,
      "region_kind": "async_block",
      "role": "kernel_submit",
      "assignment_attempts": [],
      "call_result_guard_source_links": [],
      "conditions": [
        {
          "source_fact_refs": [
            "/functional_chains/8/source_facts/16",
            "/functional_chains/8/source_facts/29"
          ],
          "id": "b7789aa6094243ca51cbe06a",
          "kind": "source_guard_and_abrupt_branch",
          "origin": "source-derived",
          "role": "kernel_submit",
          "runtime_predicate_proven": false,
          "branch_context": [],
          "branches": [
            {
              "branch": "then",
              "branch_all_paths_abrupt_proven": true,
              "abrupt_source_expressions": [
                {
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/conditions/0/branches/0/abrupt_source_expressions/0/kind"
                  },
                  "runtime_completion_proven": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/conditions/0/branches/0/abrupt_source_expressions/0/runtime_completion_proven"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/conditions/0/branches/0/abrupt_source_expressions/0/location"
                  },
                  "returned_expression": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression"
                  }
                }
              ],
              "call_ids": [
                "b19e75ebcf8d230580c696f7",
                "634724c73797bc9e0ce25309"
              ]
            }
          ],
          "condition": {
            "call_effects_or_result_proven": false,
            "callee_source": "text.trim().is_empty",
            "kind": "call_expression",
            "arguments": [],
            "callee_expression": {
              "current_referent_value_proven": false,
              "kind": "field_expression",
              "member": "is_empty",
              "location": {
                "file": "crates/kernel/src/lib.rs",
                "line": 1340,
                "column": 16,
                "end_line": 1340,
                "start_byte": 49145,
                "end_byte": 49165,
                "full_location_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/conditions/0/condition/callee_expression/location"
              },
              "member_location": {
                "file": "crates/kernel/src/lib.rs",
                "line": 1340,
                "column": 28,
                "end_line": 1340,
                "start_byte": 49157,
                "end_byte": 49165,
                "full_location_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/conditions/0/condition/callee_expression/member_location"
              },
              "object": {
                "call_effects_or_result_proven": false,
                "callee_source": "text.trim",
                "kind": "call_expression",
                "arguments": [],
                "callee_expression": {
                  "current_referent_value_proven": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/conditions/0/condition/callee_expression/object/callee_expression/current_referent_value_proven"
                  },
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/conditions/0/condition/callee_expression/object/callee_expression/kind"
                  },
                  "member": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/conditions/0/condition/callee_expression/object/callee_expression/member"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/conditions/0/condition/callee_expression/object/callee_expression/location"
                  },
                  "member_location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/conditions/0/condition/callee_expression/object/callee_expression/member_location"
                  },
                  "object": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/conditions/0/condition/callee_expression/object/callee_expression/object"
                  }
                },
                "location": {
                  "file": "crates/kernel/src/lib.rs",
                  "line": 1340,
                  "column": 16,
                  "end_line": 1340,
                  "start_byte": 49145,
                  "end_byte": 49156,
                  "full_location_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/conditions/0/condition/callee_expression/object/location"
                }
              }
            },
            "location": {
              "file": "crates/kernel/src/lib.rs",
              "line": 1340,
              "column": 16,
              "end_line": 1340,
              "start_byte": 49145,
              "end_byte": 49167,
              "full_location_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/conditions/0/condition/location"
            }
          },
          "location": {
            "file": "crates/kernel/src/lib.rs",
            "line": 1340,
            "column": 13,
            "end_line": 1345,
            "start_byte": 49142,
            "end_byte": 49337,
            "full_location_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/conditions/0/location"
          }
        }
      ],
      "guards": [],
      "opaque_direct_control_regions": [],
      "orders": [
        {
          "source_fact_refs": [
            "/functional_chains/8/source_facts/35"
          ],
          "after_step_id": "3db4cf0ba69a97071b686daf",
          "all_paths_reach_next_proven": false,
          "before_step_id": "68d0350d80451a2bf6587fc2",
          "id": "853990eb2c3e061cd212fb44",
          "kind": "conditional_direct_statement_order",
          "model_id": "captured-normal-statement-control-v1",
          "origin": "source-derived",
          "role": "kernel_submit",
          "conditions": [
            "both direct statements normally reached in the same invocation",
            "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
          ],
          "location": {
            "file": "crates/kernel/src/lib.rs",
            "line": 1346,
            "column": 13,
            "end_line": 1346,
            "start_byte": 49350,
            "end_byte": 49386,
            "full_location_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/orders/0/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/8/source_facts/36"
          ],
          "after_step_id": "677dbdd8d0ceb2cbf4ad0948",
          "all_paths_reach_next_proven": false,
          "before_step_id": "3db4cf0ba69a97071b686daf",
          "id": "97c5ea97fd4c42d9494a5e2b",
          "kind": "conditional_direct_statement_order",
          "model_id": "captured-normal-statement-control-v1",
          "origin": "source-derived",
          "role": "kernel_submit",
          "conditions": [
            "both direct statements normally reached in the same invocation",
            "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
          ],
          "location": {
            "file": "crates/kernel/src/lib.rs",
            "line": 1347,
            "column": 13,
            "end_line": 1347,
            "start_byte": 49399,
            "end_byte": 49455,
            "full_location_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/orders/1/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/8/source_facts/37"
          ],
          "after_step_id": "82f2ff294d9a75b794c365d9",
          "all_paths_reach_next_proven": false,
          "before_step_id": "677dbdd8d0ceb2cbf4ad0948",
          "id": "2de969d7dfbe3c7a4aaef67f",
          "kind": "conditional_direct_statement_order",
          "model_id": "captured-normal-statement-control-v1",
          "origin": "source-derived",
          "role": "kernel_submit",
          "conditions": [
            "both direct statements normally reached in the same invocation",
            "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
          ],
          "location": {
            "file": "crates/kernel/src/lib.rs",
            "line": 1348,
            "column": 13,
            "end_line": 1348,
            "start_byte": 49468,
            "end_byte": 49504,
            "full_location_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/orders/2/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/8/source_facts/38"
          ],
          "after_step_id": "c1de63cf2e95a6bace6e47c9",
          "all_paths_reach_next_proven": false,
          "before_step_id": "82f2ff294d9a75b794c365d9",
          "id": "cfd95a34ad33416ecc2ecc24",
          "kind": "conditional_direct_statement_order",
          "model_id": "captured-normal-statement-control-v1",
          "origin": "source-derived",
          "role": "kernel_submit",
          "conditions": [
            "both direct statements normally reached in the same invocation",
            "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
          ],
          "location": {
            "file": "crates/kernel/src/lib.rs",
            "line": 1349,
            "column": 13,
            "end_line": 1353,
            "start_byte": 49517,
            "end_byte": 49756,
            "full_location_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/orders/3/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/8/source_facts/39"
          ],
          "after_step_id": "50f6fad772089508d39b690a",
          "all_paths_reach_next_proven": false,
          "before_step_id": "c1de63cf2e95a6bace6e47c9",
          "id": "9116639214d2bb0425787881",
          "kind": "conditional_direct_statement_order",
          "model_id": "captured-normal-statement-control-v1",
          "origin": "source-derived",
          "role": "kernel_submit",
          "conditions": [
            "both direct statements normally reached in the same invocation",
            "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
          ],
          "location": {
            "file": "crates/kernel/src/lib.rs",
            "line": 1354,
            "column": 13,
            "end_line": 1354,
            "start_byte": 49769,
            "end_byte": 49805,
            "full_location_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/orders/4/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/8/source_facts/40"
          ],
          "after_step_id": "bdd393fd638c29aef6fa43e1",
          "all_paths_reach_next_proven": false,
          "before_step_id": "50f6fad772089508d39b690a",
          "id": "fee19cc26f6490baef6c5b6b",
          "kind": "conditional_direct_statement_order",
          "model_id": "captured-normal-statement-control-v1",
          "origin": "source-derived",
          "role": "kernel_submit",
          "conditions": [
            "both direct statements normally reached in the same invocation",
            "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
          ],
          "location": {
            "file": "crates/kernel/src/lib.rs",
            "line": 1355,
            "column": 13,
            "end_line": 1355,
            "start_byte": 49818,
            "end_byte": 49849,
            "full_location_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/orders/5/location"
          }
        }
      ],
      "source_region_location": {
        "file": "crates/kernel/src/lib.rs",
        "line": 1339,
        "column": 21,
        "end_line": 1356,
        "start_byte": 49122,
        "end_byte": 49859,
        "full_location_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/source_region_location"
      },
      "steps": {
        "shown_items": [
          {
            "source_fact_refs": [
              "/functional_chains/8/source_facts/22"
            ],
            "conditional_normal_reaching_only": true,
            "id": "68d0350d80451a2bf6587fc2",
            "kind": "direct_statement_call_step",
            "origin": "source-derived",
            "role": "kernel_submit",
            "source_order_index": 0,
            "statement_kind": "expression_statement",
            "call_ids": [
              "e9018655f0cb5393d58696c5",
              "2a864412d7d29dc02795f31c",
              "b19e75ebcf8d230580c696f7",
              "634724c73797bc9e0ce25309"
            ],
            "location": {
              "file": "crates/kernel/src/lib.rs",
              "line": 1340,
              "column": 13,
              "end_line": 1345,
              "start_byte": 49142,
              "end_byte": 49337,
              "full_location_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/steps/0/location"
            }
          },
          {
            "source_fact_refs": [
              "/functional_chains/8/source_facts/23"
            ],
            "conditional_normal_reaching_only": true,
            "id": "3db4cf0ba69a97071b686daf",
            "kind": "direct_statement_call_step",
            "origin": "source-derived",
            "role": "kernel_submit",
            "source_order_index": 1,
            "statement_kind": "let_declaration",
            "call_ids": [
              "3a808af3e9a27277ad351aec"
            ],
            "location": {
              "file": "crates/kernel/src/lib.rs",
              "line": 1346,
              "column": 13,
              "end_line": 1346,
              "start_byte": 49350,
              "end_byte": 49386,
              "full_location_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/steps/1/location"
            }
          },
          {
            "source_fact_refs": [
              "/functional_chains/8/source_facts/24"
            ],
            "conditional_normal_reaching_only": true,
            "id": "677dbdd8d0ceb2cbf4ad0948",
            "kind": "direct_statement_call_step",
            "origin": "source-derived",
            "role": "kernel_submit",
            "source_order_index": 2,
            "statement_kind": "let_declaration",
            "call_ids": [
              "5255a2cd90447d9e133ecfbd"
            ],
            "location": {
              "file": "crates/kernel/src/lib.rs",
              "line": 1347,
              "column": 13,
              "end_line": 1347,
              "start_byte": 49399,
              "end_byte": 49455,
              "full_location_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/steps/2/location"
            }
          },
          {
            "source_fact_refs": [
              "/functional_chains/8/source_facts/25"
            ],
            "conditional_normal_reaching_only": true,
            "id": "82f2ff294d9a75b794c365d9",
            "kind": "direct_statement_call_step",
            "origin": "source-derived",
            "role": "kernel_submit",
            "source_order_index": 3,
            "statement_kind": "expression_statement",
            "call_ids": [
              "30aab96ce7ad835841c3d332"
            ],
            "location": {
              "file": "crates/kernel/src/lib.rs",
              "line": 1348,
              "column": 13,
              "end_line": 1348,
              "start_byte": 49468,
              "end_byte": 49504,
              "full_location_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/steps/3/location"
            }
          },
          {
            "source_fact_refs": [
              "/functional_chains/8/source_facts/26"
            ],
            "conditional_normal_reaching_only": true,
            "id": "c1de63cf2e95a6bace6e47c9",
            "kind": "direct_statement_call_step",
            "origin": "source-derived",
            "role": "kernel_submit",
            "source_order_index": 4,
            "statement_kind": "let_declaration",
            "call_ids": [
              "644fba7f1a804cc6581243b3",
              "41737897fbb6ca52767d6c70",
              "43295d58f8473f1a6631974b"
            ],
            "location": {
              "file": "crates/kernel/src/lib.rs",
              "line": 1349,
              "column": 13,
              "end_line": 1353,
              "start_byte": 49517,
              "end_byte": 49756,
              "full_location_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/steps/4/location"
            }
          },
          {
            "source_fact_refs": [
              "/functional_chains/8/source_facts/27"
            ],
            "conditional_normal_reaching_only": true,
            "id": "50f6fad772089508d39b690a",
            "kind": "direct_statement_call_step",
            "origin": "source-derived",
            "role": "kernel_submit",
            "source_order_index": 5,
            "statement_kind": "expression_statement",
            "call_ids": [
              "c6929e46bd7d1ad483944007"
            ],
            "location": {
              "file": "crates/kernel/src/lib.rs",
              "line": 1354,
              "column": 13,
              "end_line": 1354,
              "start_byte": 49769,
              "end_byte": 49805,
              "full_location_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/steps/5/location"
            }
          }
        ],
        "shown_count": 6,
        "total_count": 7,
        "truncated": true,
        "full_value_ref": "/functional_chains/8/pattern/nested_source_regions/0/sequence/steps"
      }
    }
  }
]
```

**sequences**：`/functional_chains/8/pattern/sequences`；展示截断：`true`。

```json
{
  "kernel_submit": {
    "all_function_paths_or_effects_accounted": false,
    "future_or_callback_activation_proven": false,
    "region_kind": "function_item",
    "role": "kernel_submit",
    "assignment_attempts": [],
    "call_result_guard_source_links": [],
    "conditions": [
      {
        "source_fact_refs": [
          "/functional_chains/8/source_facts/16",
          "/functional_chains/8/source_facts/29"
        ],
        "id": "b7789aa6094243ca51cbe06a",
        "kind": "source_guard_and_abrupt_branch",
        "origin": "source-derived",
        "role": "kernel_submit",
        "runtime_predicate_proven": false,
        "branch_context": [],
        "branches": [
          {
            "branch": "then",
            "branch_all_paths_abrupt_proven": true,
            "abrupt_source_expressions": [
              {
                "kind": "return_expression",
                "runtime_completion_proven": false,
                "location": {
                  "file": "crates/kernel/src/lib.rs",
                  "line": 1341,
                  "column": 17,
                  "end_line": 1344,
                  "start_byte": 49186,
                  "end_byte": 49322,
                  "full_location_ref": "/functional_chains/8/pattern/sequences/kernel_submit/conditions/0/branches/0/abrupt_source_expressions/0/location"
                },
                "returned_expression": {
                  "call_effects_or_result_proven": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/8/pattern/sequences/kernel_submit/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/call_effects_or_result_proven"
                  },
                  "callee_source": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/8/pattern/sequences/kernel_submit/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/callee_source"
                  },
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/8/pattern/sequences/kernel_submit/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/kind"
                  },
                  "arguments": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/8/pattern/sequences/kernel_submit/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/arguments"
                  },
                  "callee_expression": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/8/pattern/sequences/kernel_submit/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/callee_expression"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/8/pattern/sequences/kernel_submit/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/location"
                  }
                }
              }
            ],
            "call_ids": [
              "b19e75ebcf8d230580c696f7",
              "634724c73797bc9e0ce25309"
            ]
          }
        ],
        "condition": {
          "call_effects_or_result_proven": false,
          "callee_source": "text.trim().is_empty",
          "kind": "call_expression",
          "arguments": [],
          "callee_expression": {
            "current_referent_value_proven": false,
            "kind": "field_expression",
            "member": "is_empty",
            "location": {
              "file": "crates/kernel/src/lib.rs",
              "line": 1340,
              "column": 16,
              "end_line": 1340,
              "start_byte": 49145,
              "end_byte": 49165,
              "full_location_ref": "/functional_chains/8/pattern/sequences/kernel_submit/conditions/0/condition/callee_expression/location"
            },
            "member_location": {
              "file": "crates/kernel/src/lib.rs",
              "line": 1340,
              "column": 28,
              "end_line": 1340,
              "start_byte": 49157,
              "end_byte": 49165,
              "full_location_ref": "/functional_chains/8/pattern/sequences/kernel_submit/conditions/0/condition/callee_expression/member_location"
            },
            "object": {
              "call_effects_or_result_proven": false,
              "callee_source": "text.trim",
              "kind": "call_expression",
              "arguments": [],
              "callee_expression": {
                "current_referent_value_proven": false,
                "kind": "field_expression",
                "member": "trim",
                "location": {
                  "file": "crates/kernel/src/lib.rs",
                  "line": 1340,
                  "column": 16,
                  "end_line": 1340,
                  "start_byte": 49145,
                  "end_byte": 49154,
                  "full_location_ref": "/functional_chains/8/pattern/sequences/kernel_submit/conditions/0/condition/callee_expression/object/callee_expression/location"
                },
                "member_location": {
                  "file": "crates/kernel/src/lib.rs",
                  "line": 1340,
                  "column": 21,
                  "end_line": 1340,
                  "start_byte": 49150,
                  "end_byte": 49154,
                  "full_location_ref": "/functional_chains/8/pattern/sequences/kernel_submit/conditions/0/condition/callee_expression/object/callee_expression/member_location"
                },
                "object": {
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/8/pattern/sequences/kernel_submit/conditions/0/condition/callee_expression/object/callee_expression/object/kind"
                  },
                  "name": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/8/pattern/sequences/kernel_submit/conditions/0/condition/callee_expression/object/callee_expression/object/name"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/8/pattern/sequences/kernel_submit/conditions/0/condition/callee_expression/object/callee_expression/object/location"
                  },
                  "reference": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/8/pattern/sequences/kernel_submit/conditions/0/condition/callee_expression/object/callee_expression/object/reference"
                  }
                }
              },
              "location": {
                "file": "crates/kernel/src/lib.rs",
                "line": 1340,
                "column": 16,
                "end_line": 1340,
                "start_byte": 49145,
                "end_byte": 49156,
                "full_location_ref": "/functional_chains/8/pattern/sequences/kernel_submit/conditions/0/condition/callee_expression/object/location"
              }
            }
          },
          "location": {
            "file": "crates/kernel/src/lib.rs",
            "line": 1340,
            "column": 16,
            "end_line": 1340,
            "start_byte": 49145,
            "end_byte": 49167,
            "full_location_ref": "/functional_chains/8/pattern/sequences/kernel_submit/conditions/0/condition/location"
          }
        },
        "location": {
          "file": "crates/kernel/src/lib.rs",
          "line": 1340,
          "column": 13,
          "end_line": 1345,
          "start_byte": 49142,
          "end_byte": 49337,
          "full_location_ref": "/functional_chains/8/pattern/sequences/kernel_submit/conditions/0/location"
        }
      }
    ],
    "guards": [],
    "opaque_direct_control_regions": [],
    "orders": [],
    "source_region_location": {
      "file": "crates/kernel/src/lib.rs",
      "line": 1333,
      "column": 5,
      "end_line": 1358,
      "start_byte": 48933,
      "end_byte": 49881,
      "full_location_ref": "/functional_chains/8/pattern/sequences/kernel_submit/source_region_location"
    },
    "steps": [
      {
        "source_fact_refs": [
          "/functional_chains/8/source_facts/15"
        ],
        "conditional_normal_reaching_only": true,
        "id": "5bb363630ffe9b7f00da6342",
        "kind": "direct_statement_call_step",
        "origin": "source-derived",
        "role": "kernel_submit",
        "source_order_index": 0,
        "statement_kind": "await_expression",
        "call_ids": {
          "shown_items": [
            "62771ec87a2a5fdd6a28212c",
            "e9018655f0cb5393d58696c5",
            "2a864412d7d29dc02795f31c",
            "b19e75ebcf8d230580c696f7",
            "634724c73797bc9e0ce25309",
            "3a808af3e9a27277ad351aec"
          ],
          "shown_count": 6,
          "total_count": 14,
          "truncated": true,
          "full_value_ref": "/functional_chains/8/pattern/sequences/kernel_submit/steps/0/call_ids"
        },
        "location": {
          "file": "crates/kernel/src/lib.rs",
          "line": 1339,
          "column": 9,
          "end_line": 1357,
          "start_byte": 49110,
          "end_byte": 49875,
          "full_location_ref": "/functional_chains/8/pattern/sequences/kernel_submit/steps/0/location"
        }
      }
    ]
  }
}
```

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

### wwc-report-outbox-ack-correlation-fields

类型：`message_identity_relations`；源码关系评估：`scoped_source_relations_supported`。

保存发现：`4414f1cf6af7cc88a1e0a80f`；证据：`616c459960b976504475b608`。

- `outbox_metadata`：`crates/winwincode-codex/src/outbox.rs` / `metadata`。
- `outbox_response_target`：`crates/winwincode-codex/src/outbox.rs` / `response_target`。
- `outbox_retain`：`crates/winwincode-codex/src/outbox.rs` / `ExecutionOutbox.retain_in_transaction`。
- `outbox_ack`：`crates/winwincode-codex/src/outbox.rs` / `ExecutionOutbox.acknowledge_response`。
- `outbox_correlate`：`crates/winwincode-codex/src/outbox.rs` / `correlation`。

保存关系的展示摘要（`presentation_only=true`；不新增评级）：

完整 pattern：`/functional_chains/9/pattern`。展示截断：`true`；完整证据与原 pattern 保留。

| 保存字段 | 实际值 | 完整引用 |
| --- | --- | --- |
| creates_calls_edge | false | /functional_chains/9/pattern/creates_calls_edge |
| proof_domain | captured lexical binders, finite field/record projections, enum arms and registered literal SQL source bindings | /functional_chains/9/pattern/proof_domain |
| runtime_transport_or_physical_effect_proven | false | /functional_chains/9/pattern/runtime_transport_or_physical_effect_proven |
| scoped_source_supported | true | /functional_chains/9/pattern/scoped_source_supported |
| source_only | true | /functional_chains/9/pattern/source_only |
| version | captured-message-identity-relations-1 | /functional_chains/9/pattern/version |
| whole_project_identity_complete | false | /functional_chains/9/pattern/whole_project_identity_complete |

**budget**：`/functional_chains/9/pattern/budget`；展示截断：`false`。

```json
{
  "incomplete": false,
  "limit": 65536,
  "operations": 2145
}
```

**components**：`/functional_chains/9/pattern/components`；展示截断：`true`。

```json
{
  "outbox_ack_correlation": {
    "all_message_families_covered": false,
    "external_ack_truth_or_exactly_once_proven": false,
    "outcome_helper_tuple_expanded": false,
    "physical_store_commit_proven": false,
    "scope": "only closed enum-arm direct tuple correlations and literal outbox insert/delete source seams",
    "sequence_to_ack_sequence_rename_value_proven": false,
    "supported": true,
    "ack_gate_sources": [
      {
        "source_fact_refs": [
          "/functional_chains/9/source_facts/116"
        ],
        "caller_supplied_domain_validation_independently_proven": false,
        "creates_calls_edge": false,
        "extractor_version": "captured-message-identity-relations-1",
        "id": "ae22eebeb82fe8d73e31d47c",
        "kind": "message_ack_authority_source_guard",
        "origin": "source-derived",
        "target_code_executed": false,
        "arguments": [
          {
            "kind": "identifier",
            "name": "acknowledgement",
            "location": {
              "file": "crates/winwincode-codex/src/outbox.rs",
              "line": 269,
              "column": 31,
              "end_line": 269,
              "start_byte": 11817,
              "end_byte": 11832,
              "full_location_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/ack_gate_sources/0/arguments/0/location"
            },
            "reference": {
              "declaration_id": "224abda657ed34918d471cc46b11b910fe35ee37571c18e233fb0fa967d8ed48",
              "declaration_kind": "captured_rust_parameter",
              "identity_scope": "plain captured binder syntax only",
              "macro_namespace_complete": false,
              "runtime_value_identity_proven": false,
              "state": "captured_unique_rust_binder",
              "binder_location": {
                "file": "crates/winwincode-codex/src/outbox.rs",
                "line": 264,
                "column": 9,
                "end_line": 264,
                "start_byte": 11565,
                "end_byte": 11580,
                "full_location_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/ack_gate_sources/0/arguments/0/reference/binder_location"
              },
              "declaration_location": {
                "file": "crates/winwincode-codex/src/outbox.rs",
                "line": 264,
                "column": 9,
                "end_line": 264,
                "start_byte": 11565,
                "end_byte": 11603,
                "full_location_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/ack_gate_sources/0/arguments/0/reference/declaration_location"
              }
            }
          }
        ],
        "branch_context": [
          {
            "branch": "condition",
            "condition_truth_proven": false,
            "kind": "if",
            "condition": {
              "kind": "unary_expression",
              "operator": "!",
              "runtime_predicate_or_assignment_proven": false,
              "location": {
                "file": "crates/winwincode-codex/src/outbox.rs",
                "line": 269,
                "column": 12,
                "end_line": 269,
                "start_byte": 11798,
                "end_byte": 11833,
                "full_location_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/ack_gate_sources/0/branch_context/0/condition/location"
              },
              "operands": [
                {
                  "call_effects_or_result_proven": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/ack_gate_sources/0/branch_context/0/condition/operands/0/call_effects_or_result_proven"
                  },
                  "callee_source": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/ack_gate_sources/0/branch_context/0/condition/operands/0/callee_source"
                  },
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/ack_gate_sources/0/branch_context/0/condition/operands/0/kind"
                  },
                  "arguments": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/ack_gate_sources/0/branch_context/0/condition/operands/0/arguments"
                  },
                  "callee_expression": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/ack_gate_sources/0/branch_context/0/condition/operands/0/callee_expression"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/ack_gate_sources/0/branch_context/0/condition/operands/0/location"
                  }
                }
              ]
            },
            "location": {
              "file": "crates/winwincode-codex/src/outbox.rs",
              "line": 269,
              "column": 9,
              "end_line": 271,
              "start_byte": 11795,
              "end_byte": 11898,
              "full_location_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/ack_gate_sources/0/branch_context/0/location"
            }
          }
        ],
        "location": {
          "file": "crates/winwincode-codex/src/outbox.rs",
          "line": 269,
          "column": 13,
          "end_line": 269,
          "start_byte": 11799,
          "end_byte": 11833,
          "full_location_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/ack_gate_sources/0/location"
        }
      },
      {
        "source_fact_refs": [
          "/functional_chains/9/source_facts/117"
        ],
        "caller_supplied_domain_validation_independently_proven": false,
        "creates_calls_edge": false,
        "extractor_version": "captured-message-identity-relations-1",
        "id": "fa610ff1d5a4790fba72a578",
        "kind": "message_ack_authority_source_guard",
        "origin": "source-derived",
        "target_code_executed": false,
        "arguments": [
          {
            "kind": "identifier",
            "name": "acknowledgement",
            "location": {
              "file": "crates/winwincode-codex/src/outbox.rs",
              "line": 272,
              "column": 63,
              "end_line": 272,
              "start_byte": 11961,
              "end_byte": 11976,
              "full_location_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/ack_gate_sources/1/arguments/0/location"
            },
            "reference": {
              "declaration_id": "224abda657ed34918d471cc46b11b910fe35ee37571c18e233fb0fa967d8ed48",
              "declaration_kind": "captured_rust_parameter",
              "identity_scope": "plain captured binder syntax only",
              "macro_namespace_complete": false,
              "runtime_value_identity_proven": false,
              "state": "captured_unique_rust_binder",
              "binder_location": {
                "file": "crates/winwincode-codex/src/outbox.rs",
                "line": 264,
                "column": 9,
                "end_line": 264,
                "start_byte": 11565,
                "end_byte": 11580,
                "full_location_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/ack_gate_sources/1/arguments/0/reference/binder_location"
              },
              "declaration_location": {
                "file": "crates/winwincode-codex/src/outbox.rs",
                "line": 264,
                "column": 9,
                "end_line": 264,
                "start_byte": 11565,
                "end_byte": 11603,
                "full_location_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/ack_gate_sources/1/arguments/0/reference/declaration_location"
              }
            }
          }
        ],
        "branch_context": [],
        "location": {
          "file": "crates/winwincode-codex/src/outbox.rs",
          "line": 272,
          "column": 47,
          "end_line": 272,
          "start_byte": 11945,
          "end_byte": 11977,
          "full_location_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/ack_gate_sources/1/location"
        }
      }
    ],
    "ack_return_tuple_sql_bindings": [
      {
        "source_fact_refs": [
          "/functional_chains/9/source_facts/119"
        ],
        "creates_calls_edge": false,
        "extractor_version": "captured-message-identity-relations-1",
        "id": "bd0c13e8c1731828fa2622b2",
        "kind": "message_ack_return_tuple_sql_parameter_binding",
        "origin": "source-derived",
        "restricted_macro_tokens_only": true,
        "returned_correlation_sql_position": 2,
        "returned_family_sql_position": 1,
        "sql_fact_id": "badf58de77821ad6a6e05dc6",
        "supported": true,
        "target_code_executed": false,
        "value_or_database_effect_proven": false,
        "location": {
          "file": "crates/winwincode-codex/src/outbox.rs",
          "line": 272,
          "column": 9,
          "end_line": 274,
          "start_byte": 11907,
          "end_byte": 12049,
          "full_location_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/ack_return_tuple_sql_bindings/0/location"
        },
        "returned_binder_ids": [
          "4e9ed8a7f6c62187275803d7433f8916d5f8fba874881ac8bb947f2c2fbd0ea7",
          "5a83f877ad099c1ff736dcf103a8847d35a59774044af2440ec50ba3c20482f0"
        ],
        "sql_argument_binder_ids": [
          "4e9ed8a7f6c62187275803d7433f8916d5f8fba874881ac8bb947f2c2fbd0ea7",
          "5a83f877ad099c1ff736dcf103a8847d35a59774044af2440ec50ba3c20482f0"
        ],
        "tuple_binders": [
          {
            "file": "crates/winwincode-codex/src/outbox.rs",
            "line": 272,
            "column": 19,
            "end_line": 272,
            "start_byte": 11917,
            "end_byte": 11923,
            "full_location_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/ack_return_tuple_sql_bindings/0/tuple_binders/0"
          },
          {
            "file": "crates/winwincode-codex/src/outbox.rs",
            "line": 272,
            "column": 27,
            "end_line": 272,
            "start_byte": 11925,
            "end_byte": 11940,
            "full_location_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/ack_return_tuple_sql_bindings/0/tuple_binders/1"
          }
        ]
      }
    ],
    "correlation_codec_sources": [
      {
        "source_fact_refs": [
          "/functional_chains/9/source_facts/114"
        ],
        "callee_source": "serde_json::to_vec",
        "codec_runtime_or_digest_collision_proven": false,
        "creates_calls_edge": false,
        "extractor_version": "captured-message-identity-relations-1",
        "id": "d464fc68825104ca6b944888",
        "kind": "message_correlation_codec_operand",
        "origin": "source-derived",
        "target_code_executed": false,
        "arguments": [
          {
            "kind": "identifier",
            "name": "value",
            "location": {
              "file": "crates/winwincode-codex/src/outbox.rs",
              "line": 738,
              "column": 36,
              "end_line": 738,
              "start_byte": 30300,
              "end_byte": 30305,
              "full_location_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/correlation_codec_sources/0/arguments/0/location"
            },
            "reference": {
              "declaration_id": "eddedcd9ceff112f7350221c8b359c7ce48d14a8852067a738f11bc1c41e7df0",
              "declaration_kind": "captured_rust_parameter",
              "identity_scope": "plain captured binder syntax only",
              "macro_namespace_complete": false,
              "runtime_value_identity_proven": false,
              "state": "captured_unique_rust_binder",
              "binder_location": {
                "file": "crates/winwincode-codex/src/outbox.rs",
                "line": 737,
                "column": 16,
                "end_line": 737,
                "start_byte": 30202,
                "end_byte": 30207,
                "full_location_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/correlation_codec_sources/0/arguments/0/reference/binder_location"
              },
              "declaration_location": {
                "file": "crates/winwincode-codex/src/outbox.rs",
                "line": 737,
                "column": 16,
                "end_line": 737,
                "start_byte": 30202,
                "end_byte": 30224,
                "full_location_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/correlation_codec_sources/0/arguments/0/reference/declaration_location"
              }
            }
          }
        ],
        "location": {
          "file": "crates/winwincode-codex/src/outbox.rs",
          "line": 738,
          "column": 17,
          "end_line": 738,
          "start_byte": 30281,
          "end_byte": 30306,
          "full_location_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/correlation_codec_sources/0/location"
        }
      },
      {
        "source_fact_refs": [
          "/functional_chains/9/source_facts/115"
        ],
        "callee_source": "digest",
        "codec_runtime_or_digest_collision_proven": false,
        "creates_calls_edge": false,
        "extractor_version": "captured-message-identity-relations-1",
        "id": "3108f5cbbdcd0b050c7e7594",
        "kind": "message_correlation_codec_operand",
        "origin": "source-derived",
        "target_code_executed": false,
        "arguments": [
          {
            "kind": "reference_expression",
            "location": {
              "file": "crates/winwincode-codex/src/outbox.rs",
              "line": 739,
              "column": 15,
              "end_line": 739,
              "start_byte": 30363,
              "end_byte": 30369,
              "full_location_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/correlation_codec_sources/1/arguments/0/location"
            },
            "operand": {
              "kind": "identifier",
              "name": "bytes",
              "location": {
                "file": "crates/winwincode-codex/src/outbox.rs",
                "line": 739,
                "column": 16,
                "end_line": 739,
                "start_byte": 30364,
                "end_byte": 30369,
                "full_location_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/correlation_codec_sources/1/arguments/0/operand/location"
              },
              "reference": {
                "declaration_id": "cf7a9d21455eec1b1db37c2155fae33c105df1229a58ab6b70a8aafccaff9f78",
                "declaration_kind": "captured_rust_local",
                "identity_scope": "plain captured binder syntax only",
                "macro_namespace_complete": false,
                "runtime_value_identity_proven": false,
                "state": "captured_unique_rust_binder",
                "binder_location": {
                  "file": "crates/winwincode-codex/src/outbox.rs",
                  "line": 738,
                  "column": 9,
                  "end_line": 738,
                  "start_byte": 30273,
                  "end_byte": 30278,
                  "full_location_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/correlation_codec_sources/1/arguments/0/operand/reference/binder_location"
                },
                "declaration_location": {
                  "file": "crates/winwincode-codex/src/outbox.rs",
                  "line": 738,
                  "column": 5,
                  "end_line": 738,
                  "start_byte": 30269,
                  "end_byte": 30348,
                  "full_location_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/correlation_codec_sources/1/arguments/0/operand/reference/declaration_location"
                }
              }
            }
          }
        ],
        "location": {
          "file": "crates/winwincode-codex/src/outbox.rs",
          "line": 739,
          "column": 8,
          "end_line": 739,
          "start_byte": 30356,
          "end_byte": 30370,
          "full_location_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/correlation_codec_sources/1/location"
        }
      }
    ],
    "frame_metadata_sql_insert_joins": [
      {
        "source_fact_refs": [
          "/functional_chains/9/source_facts/118"
        ],
        "creates_calls_edge": false,
        "extractor_version": "captured-message-identity-relations-1",
        "id": "0dab9fa17d70fa96720852ee",
        "kind": "message_frame_metadata_insert_source_join",
        "origin": "source-derived",
        "same_captured_sql_binders": true,
        "same_encoded_frame_binding": true,
        "same_message_parameter": true,
        "sql_fact_id": "a8deb68ca1d0ebf1b25fa715",
        "standard_serde_codec_and_normal_sql_model_required": true,
        "stored_bytes_or_physical_transaction_success_proven": false,
        "supported": true,
        "target_code_executed": false,
        "location": {
          "file": "crates/winwincode-codex/src/outbox.rs",
          "line": 66,
          "column": 21,
          "end_line": 66,
          "start_byte": 2556,
          "end_byte": 2583,
          "full_location_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/frame_metadata_sql_insert_joins/0/location"
        },
        "metadata_and_frame_projections": {
          "correlation_key": true,
          "delivery_id": true,
          "family": true,
          "frame_json": true
        },
        "metadata_helper_relation": {
          "creates_calls_edge": false,
          "kind": "captured_same_module_function_relation",
          "macro_expansion_or_runtime_activation_proven": false,
          "scope": "unique captured top-level declaration and no captured local binder shadows this value name",
          "supported": true,
          "target_role": "outbox_metadata",
          "target_location": {
            "file": "crates/winwincode-codex/src/outbox.rs",
            "line": 454,
            "column": 1,
            "end_line": 584,
            "start_byte": 19604,
            "end_byte": 24746,
            "full_location_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/frame_metadata_sql_insert_joins/0/metadata_helper_relation/target_location"
          }
        },
        "source_column_binder_ids": {
          "acknowledgement_required": null,
          "correlation_key": "ec0f21d6340d8e0c345921dbda1d72079a0e207e528834ce92c811141ee0e4b9",
          "delivery_id": "ec0f21d6340d8e0c345921dbda1d72079a0e207e528834ce92c811141ee0e4b9",
          "family": "ec0f21d6340d8e0c345921dbda1d72079a0e207e528834ce92c811141ee0e4b9",
          "frame_digest": "93cf1f6cd7e497352f95ce974cb0d94c762f29d871b2c668f8093fd6e5bd1358",
          "frame_json": "bea37b095549a8ddf43a449a5f88382f126d79113e48b794814c17338a1c4f04",
          "state": null
        },
        "sql_column_argument_sources": {
          "acknowledgement_required": "i64::from(metadata.acknowledgement_required)",
          "correlation_key": "metadata.correlation_key",
          "delivery_id": "metadata.delivery_id",
          "family": "metadata.family",
          "frame_digest": "frame_digest",
          "frame_json": "frame",
          "state": "PENDING"
        }
      }
    ],
    "projection_agreements": {
      "shown_items": [
        {
          "agreement_domain": "ordered field projections passed to the captured same correlation helper",
          "creates_calls_edge": false,
          "equal_wire_values_or_accepted_response_proven": false,
          "family": "Family::ModelOpen",
          "relation_kind": "request_response_correlation_projection_agreement",
          "request_fact_id": "5559bb639f9df31a2126aa04",
          "request_variant": "ExecutionPortMessage::ModelOpenMessage",
          "response_fact_id": "b137a0497275caa2798e22b3",
          "response_variant": "ExecutionPortMessage::ModelChunkMessage",
          "ordered_field_paths": [
            [
              "model_exchange_id"
            ],
            [
              "lease"
            ],
            [
              "worker_session_id"
            ],
            [
              "session_identity"
            ]
          ]
        },
        {
          "agreement_domain": "ordered field projections passed to the captured same correlation helper",
          "creates_calls_edge": false,
          "equal_wire_values_or_accepted_response_proven": false,
          "family": "Family::ModelOpen",
          "relation_kind": "request_response_correlation_projection_agreement",
          "request_fact_id": "5559bb639f9df31a2126aa04",
          "remaining_fields_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/projection_agreements/1"
        }
      ],
      "shown_count": 2,
      "total_count": 7,
      "truncated": true,
      "full_value_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation/projection_agreements"
    },
    "remaining_fields_ref": "/functional_chains/9/pattern/components/outbox_ack_correlation"
  }
}
```

**limits**：`/functional_chains/9/pattern/limits`；展示截断：`false`。

```json
[
  "member paths identify source projections, not globally stable heap cells",
  "Rust Clone/borrow projections require ordinary generated data semantics; arbitrary trait behavior is not inferred",
  "generic adapter calls remain contextual source interfaces, never global unique targets",
  "correlation tuple agreement is a field-domain agreement; payload equality is checked by source consumers, not assumed",
  "SQL parameters are captured token positions under the registered literal source model; no database is executed",
  "retries, rejected/replayed acks, all crash windows and external authenticity are not fully proved"
]
```

**models**：`/functional_chains/9/pattern/models`；展示截断：`false`。

```json
[
  "captured-literal-sql-positional-bindings-v1",
  "finite-captured-record-message-identities-v1"
]
```

**relation_fact_ids**：`/functional_chains/9/pattern/relation_fact_ids`；展示截断：`true`。

```json
{
  "shown_items": [
    "57f1103c7938842fe91a119a",
    "eccb3dc9274e5cf8f24afc92",
    "492da88c05bb385253d779ef",
    "ee3431cc474529854feca126",
    "5559bb639f9df31a2126aa04",
    "19a4450fef936a34595bf76f"
  ],
  "shown_count": 6,
  "total_count": 29,
  "truncated": true,
  "full_value_ref": "/functional_chains/9/pattern/relation_fact_ids"
}
```

自动关系类型：`{"captured_call_step": 86, "message_ack_authority_source_guard": 2, "message_ack_return_tuple_sql_parameter_binding": 1, "message_correlation_codec_operand": 2, "message_frame_metadata_insert_source_join": 1, "message_literal_sql_positional_source": 3, "message_typed_correlation_projection": 20, "report_source_role": 5}`。

分析缺口：

```json
[]
```

条件与反证声明（单列为配置范围，不冒充源码证据）：

```json
{
  "applicability": {
    "conditions": [
      "Selected captured declarations are authenticated.",
      "Ordinary generated data retains normal borrowed/copied field semantics; source reaching is conditional, not observed execution."
    ],
    "counterexamples": [
      "Generic dispatch, wire equality, physical storage success and complete crash recovery are not inferred."
    ],
    "kind": "conditional"
  },
  "descriptive_counterexamples_are_computed_evidence": false,
  "origin": "policy-declared",
  "provenance": {
    "author_approved": false,
    "authority": "original-static-report-benchmark",
    "note": "Declaration locators only. Field records and consumers derive from authenticated saved source; no paths or expected outcomes are provided.",
    "source_doc": "reports/astra-baseline/WINWINCODE_ANALYSIS.md"
  }
}
```

### wwc-report-production-adapter-embedded-kernel

类型：`guarded_call_sequence`；源码关系评估：`scoped_source_relations_supported`。

保存发现：`c901566eaf1f168ef369c481`；证据：`00c779145d1bc95117d02554`。

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

保存关系的展示摘要（`presentation_only=true`；不新增评级）：

完整 pattern：`/functional_chains/10/pattern`。展示截断：`true`；完整证据与原 pattern 保留。

| 保存字段 | 实际值 | 完整引用 |
| --- | --- | --- |
| scoped_source_supported | true | /functional_chains/10/pattern/scoped_source_supported |

**nested_source_regions**：`/functional_chains/10/pattern/nested_source_regions`；展示截断：`false`。

```json
[]
```

**sequences**：`/functional_chains/10/pattern/sequences`；展示截断：`true`。

```json
{
  "adapter_open": {
    "all_function_paths_or_effects_accounted": false,
    "future_or_callback_activation_proven": false,
    "region_kind": "function_item",
    "role": "adapter_open",
    "assignment_attempts": [
      {
        "source_fact_refs": [
          "/functional_chains/10/source_facts/99"
        ],
        "id": "744db531952c791c40e55a60",
        "kind": "ordered_source_assignment_attempt",
        "origin": "source-derived",
        "role": "adapter_open",
        "write_runtime_success_proven": false,
        "branch_context": [],
        "left": {
          "current_referent_value_proven": false,
          "kind": "field_expression",
          "member": "helper_executable",
          "location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 420,
            "column": 9,
            "end_line": 420,
            "start_byte": 17565,
            "end_byte": 17589,
            "full_location_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/left/location"
          },
          "member_location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 420,
            "column": 16,
            "end_line": 420,
            "start_byte": 17572,
            "end_byte": 17589,
            "full_location_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/left/member_location"
          },
          "object": {
            "kind": "identifier",
            "name": "config",
            "location": {
              "file": "crates/winwincode-codex/src/adapter.rs",
              "line": 420,
              "column": 9,
              "end_line": 420,
              "start_byte": 17565,
              "end_byte": 17571,
              "full_location_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/left/object/location"
            },
            "reference": {
              "declaration_id": "316dfec879dc4d201de95e9480f46380b4bdc66bdb4a95413bc47ed6febac358",
              "declaration_kind": "captured_rust_parameter",
              "identity_scope": "plain captured binder syntax only",
              "macro_namespace_complete": false,
              "runtime_value_identity_proven": false,
              "state": "captured_unique_rust_binder",
              "binder_location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 412,
                "column": 21,
                "end_line": 412,
                "start_byte": 16945,
                "end_byte": 16951,
                "full_location_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/left/object/reference/binder_location"
              },
              "declaration_location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 412,
                "column": 17,
                "end_line": 412,
                "start_byte": 16941,
                "end_byte": 16974,
                "full_location_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/left/object/reference/declaration_location"
              }
            }
          }
        },
        "location": {
          "file": "crates/winwincode-codex/src/adapter.rs",
          "line": 420,
          "column": 9,
          "end_line": 425,
          "start_byte": 17565,
          "end_byte": 17783,
          "full_location_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/location"
        },
        "right": {
          "kind": "try_expression",
          "location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 420,
            "column": 36,
            "end_line": 425,
            "start_byte": 17592,
            "end_byte": 17783,
            "full_location_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/location"
          },
          "operand": {
            "call_effects_or_result_proven": false,
            "callee_source": "seal_helper",
            "kind": "call_expression",
            "arguments": [
              {
                "kind": "reference_expression",
                "location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 421,
                  "column": 13,
                  "end_line": 421,
                  "start_byte": 17617,
                  "end_byte": 17642,
                  "full_location_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/0/location"
                },
                "operand": {
                  "current_referent_value_proven": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/0/operand/current_referent_value_proven"
                  },
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/0/operand/kind"
                  },
                  "member": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/0/operand/member"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/0/operand/location"
                  },
                  "member_location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/0/operand/member_location"
                  },
                  "object": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/0/operand/object"
                  }
                }
              },
              {
                "call_effects_or_result_proven": false,
                "callee_source": "Some",
                "kind": "call_expression",
                "arguments": [
                  {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/1/arguments/0"
                  }
                ],
                "callee_expression": {
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/1/callee_expression/kind"
                  },
                  "name": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/1/callee_expression/name"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/1/callee_expression/location"
                  },
                  "reference": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/1/callee_expression/reference"
                  }
                },
                "location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 422,
                  "column": 13,
                  "end_line": 422,
                  "start_byte": 17656,
                  "end_byte": 17690,
                  "full_location_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/1/location"
                }
              },
              {
                "kind": "reference_expression",
                "location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 423,
                  "column": 13,
                  "end_line": 423,
                  "start_byte": 17704,
                  "end_byte": 17726,
                  "full_location_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/2/location"
                },
                "operand": {
                  "current_referent_value_proven": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/2/operand/current_referent_value_proven"
                  },
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/2/operand/kind"
                  },
                  "member": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/2/operand/member"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/2/operand/location"
                  },
                  "member_location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/2/operand/member_location"
                  },
                  "object": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/2/operand/object"
                  }
                }
              },
              {
                "kind": "reference_expression",
                "location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 424,
                  "column": 13,
                  "end_line": 424,
                  "start_byte": 17740,
                  "end_byte": 17771,
                  "full_location_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/3/location"
                },
                "operand": {
                  "current_referent_value_proven": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/3/operand/current_referent_value_proven"
                  },
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/3/operand/kind"
                  },
                  "member": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/3/operand/member"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/3/operand/location"
                  },
                  "member_location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/3/operand/member_location"
                  },
                  "object": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/arguments/3/operand/object"
                  }
                }
              }
            ],
            "callee_expression": {
              "kind": "identifier",
              "name": "seal_helper",
              "location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 420,
                "column": 36,
                "end_line": 420,
                "start_byte": 17592,
                "end_byte": 17603,
                "full_location_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/callee_expression/location"
              },
              "reference": {
                "plain_binder_candidates": 0,
                "runtime_value_identity_proven": false,
                "state": "captured_rust_reference",
                "text": "seal_helper",
                "location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 420,
                  "column": 36,
                  "end_line": 420,
                  "start_byte": 17592,
                  "end_byte": 17603,
                  "full_location_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/callee_expression/reference/location"
                }
              }
            },
            "location": {
              "file": "crates/winwincode-codex/src/adapter.rs",
              "line": 420,
              "column": 36,
              "end_line": 425,
              "start_byte": 17592,
              "end_byte": 17782,
              "full_location_ref": "/functional_chains/10/pattern/sequences/adapter_open/assignment_attempts/0/right/operand/location"
            }
          }
        }
      }
    ],
    "call_result_guard_source_links": [],
    "conditions": [],
    "guards": [],
    "opaque_direct_control_regions": [],
    "orders": {
      "shown_items": [
        {
          "source_fact_refs": [
            "/functional_chains/10/source_facts/110"
          ],
          "after_step_id": "e4c8a786c0accf0f1c094b6c",
          "all_paths_reach_next_proven": false,
          "before_step_id": "e49716da5c063c711f406b58",
          "id": "e2efb8581d35bb415d6dd2e2",
          "kind": "conditional_direct_statement_order",
          "model_id": "captured-normal-statement-control-v1",
          "origin": "source-derived",
          "role": "adapter_open",
          "conditions": [
            "both direct statements normally reached in the same invocation",
            "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
          ],
          "location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 419,
            "column": 9,
            "end_line": 419,
            "start_byte": 17482,
            "end_byte": 17556,
            "full_location_ref": "/functional_chains/10/pattern/sequences/adapter_open/orders/0/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/10/source_facts/111"
          ],
          "after_step_id": "694cd1b40dbe406914948841",
          "all_paths_reach_next_proven": false,
          "before_step_id": "e4c8a786c0accf0f1c094b6c",
          "id": "a9136f0b1feef123171dbf0c",
          "kind": "conditional_direct_statement_order",
          "model_id": "captured-normal-statement-control-v1",
          "origin": "source-derived",
          "role": "adapter_open",
          "conditions": [
            "both direct statements normally reached in the same invocation",
            "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
          ],
          "location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 420,
            "column": 9,
            "end_line": 425,
            "start_byte": 17565,
            "end_byte": 17784,
            "full_location_ref": "/functional_chains/10/pattern/sequences/adapter_open/orders/1/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/10/source_facts/112"
          ],
          "after_step_id": "ad8135fc9b484a54b05634ba",
          "all_paths_reach_next_proven": false,
          "before_step_id": "694cd1b40dbe406914948841",
          "id": "4903ef592bb58bddd011d642",
          "kind": "conditional_direct_statement_order",
          "model_id": "captured-normal-statement-control-v1",
          "origin": "source-derived",
          "role": "adapter_open",
          "conditions": [
            "both direct statements normally reached in the same invocation",
            "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
          ],
          "location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 426,
            "column": 9,
            "end_line": 430,
            "start_byte": 17793,
            "end_byte": 18007,
            "full_location_ref": "/functional_chains/10/pattern/sequences/adapter_open/orders/2/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/10/source_facts/113"
          ],
          "after_step_id": "496088204fc52ed2b75a0fb7",
          "all_paths_reach_next_proven": false,
          "before_step_id": "ad8135fc9b484a54b05634ba",
          "id": "d1e3aefcd77857d0f8de7c28",
          "kind": "conditional_direct_statement_order",
          "model_id": "captured-normal-statement-control-v1",
          "origin": "source-derived",
          "role": "adapter_open",
          "conditions": [
            "both direct statements normally reached in the same invocation",
            "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
          ],
          "location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 431,
            "column": 9,
            "end_line": 431,
            "start_byte": 18016,
            "end_byte": 18097,
            "full_location_ref": "/functional_chains/10/pattern/sequences/adapter_open/orders/3/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/10/source_facts/114"
          ],
          "after_step_id": "61e70374507a2f8ef86c9809",
          "all_paths_reach_next_proven": false,
          "before_step_id": "496088204fc52ed2b75a0fb7",
          "id": "0875630e2d6e55fb25763a2c",
          "kind": "conditional_direct_statement_order",
          "model_id": "captured-normal-statement-control-v1",
          "origin": "source-derived",
          "role": "adapter_open",
          "conditions": [
            "both direct statements normally reached in the same invocation",
            "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
          ],
          "location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 432,
            "column": 9,
            "end_line": 432,
            "start_byte": 18106,
            "end_byte": 18157,
            "full_location_ref": "/functional_chains/10/pattern/sequences/adapter_open/orders/4/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/10/source_facts/115"
          ],
          "after_step_id": "40a83d62eb26a57b29756e27",
          "all_paths_reach_next_proven": false,
          "before_step_id": "61e70374507a2f8ef86c9809",
          "id": "a991bd76f1265f7827bbc475",
          "kind": "conditional_direct_statement_order",
          "model_id": "captured-normal-statement-control-v1",
          "origin": "source-derived",
          "role": "adapter_open",
          "conditions": [
            "both direct statements normally reached in the same invocation",
            "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
          ],
          "location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 433,
            "column": 9,
            "end_line": 433,
            "start_byte": 18166,
            "end_byte": 18242,
            "full_location_ref": "/functional_chains/10/pattern/sequences/adapter_open/orders/5/location"
          }
        }
      ],
      "shown_count": 6,
      "total_count": 14,
      "truncated": true,
      "full_value_ref": "/functional_chains/10/pattern/sequences/adapter_open/orders"
    },
    "source_region_location": {
      "file": "crates/winwincode-codex/src/adapter.rs",
      "line": 412,
      "column": 5,
      "end_line": 490,
      "start_byte": 16929,
      "end_byte": 20327,
      "full_location_ref": "/functional_chains/10/pattern/sequences/adapter_open/source_region_location"
    },
    "steps": {
      "shown_items": [
        {
          "source_fact_refs": [
            "/functional_chains/10/source_facts/82"
          ],
          "conditional_normal_reaching_only": true,
          "id": "e49716da5c063c711f406b58",
          "kind": "direct_statement_call_step",
          "origin": "source-derived",
          "role": "adapter_open",
          "source_order_index": 0,
          "statement_kind": "expression_statement",
          "call_ids": [
            "5340c3643a9d33b3aa17fdf5",
            "a5333ab1455d1a39282a8fe4"
          ],
          "location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 418,
            "column": 9,
            "end_line": 418,
            "start_byte": 17396,
            "end_byte": 17473,
            "full_location_ref": "/functional_chains/10/pattern/sequences/adapter_open/steps/0/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/10/source_facts/83"
          ],
          "conditional_normal_reaching_only": true,
          "id": "e4c8a786c0accf0f1c094b6c",
          "kind": "direct_statement_call_step",
          "origin": "source-derived",
          "role": "adapter_open",
          "source_order_index": 1,
          "statement_kind": "expression_statement",
          "call_ids": [
            "fe899771ff3d0b17578db9ba",
            "6ceb3d940c380773f23001e0"
          ],
          "location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 419,
            "column": 9,
            "end_line": 419,
            "start_byte": 17482,
            "end_byte": 17556,
            "full_location_ref": "/functional_chains/10/pattern/sequences/adapter_open/steps/1/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/10/source_facts/84"
          ],
          "conditional_normal_reaching_only": true,
          "id": "694cd1b40dbe406914948841",
          "kind": "direct_statement_call_step",
          "origin": "source-derived",
          "role": "adapter_open",
          "source_order_index": 2,
          "statement_kind": "expression_statement",
          "call_ids": [
            "60de924e01c686682f420795",
            "b86a85dc3f96c2ff09de87ce",
            "97702136c1bd15b1fddb9f7e"
          ],
          "location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 420,
            "column": 9,
            "end_line": 425,
            "start_byte": 17565,
            "end_byte": 17784,
            "full_location_ref": "/functional_chains/10/pattern/sequences/adapter_open/steps/2/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/10/source_facts/85"
          ],
          "conditional_normal_reaching_only": true,
          "id": "ad8135fc9b484a54b05634ba",
          "kind": "direct_statement_call_step",
          "origin": "source-derived",
          "role": "adapter_open",
          "source_order_index": 3,
          "remaining_fields_ref": "/functional_chains/10/pattern/sequences/adapter_open/steps/3"
        }
      ],
      "shown_count": 4,
      "total_count": 15,
      "truncated": true,
      "full_value_ref": "/functional_chains/10/pattern/sequences/adapter_open/steps"
    }
  },
  "remaining_fields_ref": "/functional_chains/10/pattern/sequences"
}
```

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

保存发现：`e1a2d1a98046bb6e76d3c181`；证据：`bb269bde2edbbed274bea4e3`。

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

保存关系的展示摘要（`presentation_only=true`；不新增评级）：

完整 pattern：`/functional_chains/11/pattern`。展示截断：`true`；完整证据与原 pattern 保留。

| 保存字段 | 实际值 | 完整引用 |
| --- | --- | --- |
| scoped_source_supported | true | /functional_chains/11/pattern/scoped_source_supported |

**nested_source_regions**：`/functional_chains/11/pattern/nested_source_regions`；展示截断：`false`。

```json
[]
```

**sequences**：`/functional_chains/11/pattern/sequences`；展示截断：`true`。

```json
{
  "submission": {
    "all_function_paths_or_effects_accounted": false,
    "future_or_callback_activation_proven": false,
    "region_kind": "function_item",
    "role": "submission",
    "assignment_attempts": [
      {
        "source_fact_refs": [
          "/functional_chains/11/source_facts/79"
        ],
        "id": "a4a2cb197e3bf7b8ed776cfe",
        "kind": "ordered_source_assignment_attempt",
        "origin": "source-derived",
        "role": "submission",
        "write_runtime_success_proven": false,
        "branch_context": [
          {
            "activation_proven": false,
            "kind": "match_arm",
            "location": {
              "file": "crates/winwincode-codex/src/adapter.rs",
              "line": 3539,
              "column": 17,
              "end_line": 3539,
              "start_byte": 138925,
              "end_byte": 138988,
              "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/0/branch_context/0/location"
            }
          }
        ],
        "left": {
          "current_referent_value_proven": false,
          "kind": "field_expression",
          "member": "submission_digest",
          "location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 3539,
            "column": 25,
            "end_line": 3539,
            "start_byte": 138933,
            "end_byte": 138961,
            "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/0/left/location"
          },
          "member_location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 3539,
            "column": 36,
            "end_line": 3539,
            "start_byte": 138944,
            "end_byte": 138961,
            "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/0/left/member_location"
          },
          "object": {
            "current_referent_value_proven": false,
            "kind": "field_expression",
            "member": "record",
            "location": {
              "file": "crates/winwincode-codex/src/adapter.rs",
              "line": 3539,
              "column": 25,
              "end_line": 3539,
              "start_byte": 138933,
              "end_byte": 138943,
              "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/0/left/object/location"
            },
            "member_location": {
              "file": "crates/winwincode-codex/src/adapter.rs",
              "line": 3539,
              "column": 29,
              "end_line": 3539,
              "start_byte": 138937,
              "end_byte": 138943,
              "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/0/left/object/member_location"
            },
            "object": {
              "kind": "identifier",
              "name": "run",
              "location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3539,
                "column": 25,
                "end_line": 3539,
                "start_byte": 138933,
                "end_byte": 138936,
                "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/0/left/object/object/location"
              },
              "reference": {
                "declaration_id": "46f19d39a4a44d2dc15f248c582b6169450fe3aa5ae2b4f09e31982a822ef2a4",
                "declaration_kind": "captured_rust_local",
                "identity_scope": "plain captured binder syntax only",
                "macro_namespace_complete": false,
                "runtime_value_identity_proven": false,
                "state": "captured_unique_rust_binder",
                "binder_location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 3535,
                  "column": 17,
                  "end_line": 3535,
                  "start_byte": 138674,
                  "end_byte": 138677,
                  "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/0/left/object/object/reference/binder_location"
                },
                "declaration_location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 3535,
                  "column": 13,
                  "end_line": 3535,
                  "start_byte": 138670,
                  "end_byte": 138736,
                  "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/0/left/object/object/reference/declaration_location"
                }
              }
            }
          }
        },
        "location": {
          "file": "crates/winwincode-codex/src/adapter.rs",
          "line": 3539,
          "column": 25,
          "end_line": 3539,
          "start_byte": 138933,
          "end_byte": 138987,
          "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/0/location"
        },
        "right": {
          "call_effects_or_result_proven": false,
          "callee_source": "Some",
          "kind": "call_expression",
          "arguments": [
            {
              "kind": "identifier",
              "name": "submission_digest",
              "location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3539,
                "column": 61,
                "end_line": 3539,
                "start_byte": 138969,
                "end_byte": 138986,
                "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/0/right/arguments/0/location"
              },
              "reference": {
                "declaration_id": "32221372946c395335a991f6fdb3cbdc9eef00d47d745dd2860ac2c49bb1f12c",
                "declaration_kind": "captured_rust_local",
                "identity_scope": "plain captured binder syntax only",
                "macro_namespace_complete": false,
                "runtime_value_identity_proven": false,
                "state": "captured_unique_rust_binder",
                "binder_location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 3533,
                  "column": 13,
                  "end_line": 3533,
                  "start_byte": 138544,
                  "end_byte": 138561,
                  "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/0/right/arguments/0/reference/binder_location"
                },
                "declaration_location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 3533,
                  "column": 9,
                  "end_line": 3533,
                  "start_byte": 138540,
                  "end_byte": 138616,
                  "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/0/right/arguments/0/reference/declaration_location"
                }
              }
            }
          ],
          "callee_expression": {
            "kind": "identifier",
            "name": "Some",
            "location": {
              "file": "crates/winwincode-codex/src/adapter.rs",
              "line": 3539,
              "column": 56,
              "end_line": 3539,
              "start_byte": 138964,
              "end_byte": 138968,
              "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/0/right/callee_expression/location"
            },
            "reference": {
              "plain_binder_candidates": 0,
              "runtime_value_identity_proven": false,
              "state": "captured_rust_reference",
              "text": "Some",
              "location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3539,
                "column": 56,
                "end_line": 3539,
                "start_byte": 138964,
                "end_byte": 138968,
                "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/0/right/callee_expression/reference/location"
              }
            }
          },
          "location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 3539,
            "column": 56,
            "end_line": 3539,
            "start_byte": 138964,
            "end_byte": 138987,
            "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/0/right/location"
          }
        }
      },
      {
        "source_fact_refs": [
          "/functional_chains/11/source_facts/83"
        ],
        "id": "731d9b46e21c5002ce942cdc",
        "kind": "ordered_source_assignment_attempt",
        "origin": "source-derived",
        "role": "submission",
        "write_runtime_success_proven": false,
        "branch_context": [
          {
            "branch": "else",
            "condition_truth_proven": false,
            "kind": "if",
            "condition": {
              "kind": "binary_expression",
              "operator": "||",
              "runtime_predicate_or_assignment_proven": false,
              "location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3541,
                "column": 16,
                "end_line": 3545,
                "start_byte": 139018,
                "end_byte": 139272,
                "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/branch_context/0/condition/location"
              },
              "operands": [
                {
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/branch_context/0/condition/operands/0/kind"
                  },
                  "operator": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/branch_context/0/condition/operands/0/operator"
                  },
                  "runtime_predicate_or_assignment_proven": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/branch_context/0/condition/operands/0/runtime_predicate_or_assignment_proven"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/branch_context/0/condition/operands/0/location"
                  },
                  "operands": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/branch_context/0/condition/operands/0/operands"
                  }
                },
                {
                  "call_effects_or_result_proven": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/branch_context/0/condition/operands/1/call_effects_or_result_proven"
                  },
                  "callee_source": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/branch_context/0/condition/operands/1/callee_source"
                  },
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/branch_context/0/condition/operands/1/kind"
                  },
                  "arguments": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/branch_context/0/condition/operands/1/arguments"
                  },
                  "callee_expression": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/branch_context/0/condition/operands/1/callee_expression"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/branch_context/0/condition/operands/1/location"
                  }
                }
              ]
            },
            "location": {
              "file": "crates/winwincode-codex/src/adapter.rs",
              "line": 3541,
              "column": 13,
              "end_line": 3556,
              "start_byte": 139015,
              "end_byte": 139739,
              "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/branch_context/0/location"
            }
          },
          {
            "branch": "then",
            "condition_truth_proven": false,
            "kind": "if",
            "condition": {
              "kind": "binary_expression",
              "operator": "==",
              "runtime_predicate_or_assignment_proven": false,
              "location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3552,
                "column": 20,
                "end_line": 3552,
                "start_byte": 139530,
                "end_byte": 139574,
                "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/branch_context/1/condition/location"
              },
              "operands": [
                {
                  "current_referent_value_proven": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/branch_context/1/condition/operands/0/current_referent_value_proven"
                  },
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/branch_context/1/condition/operands/0/kind"
                  },
                  "member": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/branch_context/1/condition/operands/0/member"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/branch_context/1/condition/operands/0/location"
                  },
                  "member_location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/branch_context/1/condition/operands/0/member_location"
                  },
                  "object": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/branch_context/1/condition/operands/0/object"
                  }
                },
                {
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/branch_context/1/condition/operands/1/kind"
                  },
                  "source": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/branch_context/1/condition/operands/1/source"
                  },
                  "children": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/branch_context/1/condition/operands/1/children"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/branch_context/1/condition/operands/1/location"
                  }
                }
              ]
            },
            "location": {
              "file": "crates/winwincode-codex/src/adapter.rs",
              "line": 3552,
              "column": 17,
              "end_line": 3554,
              "start_byte": 139527,
              "end_byte": 139667,
              "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/branch_context/1/location"
            }
          }
        ],
        "left": {
          "current_referent_value_proven": false,
          "kind": "field_expression",
          "member": "phase",
          "location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 3553,
            "column": 21,
            "end_line": 3553,
            "start_byte": 139597,
            "end_byte": 139613,
            "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/left/location"
          },
          "member_location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 3553,
            "column": 32,
            "end_line": 3553,
            "start_byte": 139608,
            "end_byte": 139613,
            "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/left/member_location"
          },
          "object": {
            "current_referent_value_proven": false,
            "kind": "field_expression",
            "member": "record",
            "location": {
              "file": "crates/winwincode-codex/src/adapter.rs",
              "line": 3553,
              "column": 21,
              "end_line": 3553,
              "start_byte": 139597,
              "end_byte": 139607,
              "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/left/object/location"
            },
            "member_location": {
              "file": "crates/winwincode-codex/src/adapter.rs",
              "line": 3553,
              "column": 25,
              "end_line": 3553,
              "start_byte": 139601,
              "end_byte": 139607,
              "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/left/object/member_location"
            },
            "object": {
              "kind": "identifier",
              "name": "run",
              "location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3553,
                "column": 21,
                "end_line": 3553,
                "start_byte": 139597,
                "end_byte": 139600,
                "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/left/object/object/location"
              },
              "reference": {
                "declaration_id": "46f19d39a4a44d2dc15f248c582b6169450fe3aa5ae2b4f09e31982a822ef2a4",
                "declaration_kind": "captured_rust_local",
                "identity_scope": "plain captured binder syntax only",
                "macro_namespace_complete": false,
                "runtime_value_identity_proven": false,
                "state": "captured_unique_rust_binder",
                "binder_location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 3535,
                  "column": 17,
                  "end_line": 3535,
                  "start_byte": 138674,
                  "end_byte": 138677,
                  "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/left/object/object/reference/binder_location"
                },
                "declaration_location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 3535,
                  "column": 13,
                  "end_line": 3535,
                  "start_byte": 138670,
                  "end_byte": 138736,
                  "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/left/object/object/reference/declaration_location"
                }
              }
            }
          }
        },
        "location": {
          "file": "crates/winwincode-codex/src/adapter.rs",
          "line": 3553,
          "column": 21,
          "end_line": 3553,
          "start_byte": 139597,
          "end_byte": 139648,
          "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/location"
        },
        "right": {
          "kind": "scoped_identifier",
          "source": "StoredRunPhase::SubmissionIntent",
          "children": [
            {
              "kind": "identifier",
              "name": "StoredRunPhase",
              "location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3553,
                "column": 40,
                "end_line": 3553,
                "start_byte": 139616,
                "end_byte": 139630,
                "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/right/children/0/location"
              },
              "reference": {
                "plain_binder_candidates": 0,
                "runtime_value_identity_proven": false,
                "state": "captured_rust_reference",
                "text": "StoredRunPhase",
                "location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 3553,
                  "column": 40,
                  "end_line": 3553,
                  "start_byte": 139616,
                  "end_byte": 139630,
                  "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/right/children/0/reference/location"
                }
              }
            },
            {
              "kind": "identifier",
              "name": "SubmissionIntent",
              "location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3553,
                "column": 56,
                "end_line": 3553,
                "start_byte": 139632,
                "end_byte": 139648,
                "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/right/children/1/location"
              },
              "reference": {
                "plain_binder_candidates": 0,
                "runtime_value_identity_proven": false,
                "state": "captured_rust_reference",
                "text": "SubmissionIntent",
                "location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 3553,
                  "column": 56,
                  "end_line": 3553,
                  "start_byte": 139632,
                  "end_byte": 139648,
                  "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/right/children/1/reference/location"
                }
              }
            }
          ],
          "location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 3553,
            "column": 40,
            "end_line": 3553,
            "start_byte": 139616,
            "end_byte": 139648,
            "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/1/right/location"
          }
        }
      },
      {
        "source_fact_refs": [
          "/functional_chains/11/source_facts/94"
        ],
        "id": "2f74585cd38be07b79082637",
        "kind": "ordered_source_assignment_attempt",
        "origin": "source-derived",
        "role": "submission",
        "write_runtime_success_proven": false,
        "branch_context": [],
        "left": {
          "current_referent_value_proven": false,
          "kind": "field_expression",
          "member": "recovered",
          "location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 3623,
            "column": 9,
            "end_line": 3626,
            "start_byte": 142404,
            "end_byte": 142508,
            "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/2/left/location"
          },
          "member_location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 3626,
            "column": 14,
            "end_line": 3626,
            "start_byte": 142499,
            "end_byte": 142508,
            "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/2/left/member_location"
          },
          "object": {
            "kind": "try_expression",
            "location": {
              "file": "crates/winwincode-codex/src/adapter.rs",
              "line": 3623,
              "column": 9,
              "end_line": 3625,
              "start_byte": 142404,
              "end_byte": 142485,
              "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/2/left/object/location"
            },
            "operand": {
              "call_effects_or_result_proven": false,
              "callee_source": "self.runs\n            .get_mut(&run_key)\n            .ok_or_else",
              "kind": "call_expression",
              "arguments": [
                {
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/2/left/object/operand/arguments/0/kind"
                  },
                  "name": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/2/left/object/operand/arguments/0/name"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/2/left/object/operand/arguments/0/location"
                  },
                  "reference": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/2/left/object/operand/arguments/0/reference"
                  }
                }
              ],
              "callee_expression": {
                "current_referent_value_proven": false,
                "kind": "field_expression",
                "member": "ok_or_else",
                "location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 3623,
                  "column": 9,
                  "end_line": 3625,
                  "start_byte": 142404,
                  "end_byte": 142468,
                  "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/2/left/object/operand/callee_expression/location"
                },
                "member_location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 3625,
                  "column": 14,
                  "end_line": 3625,
                  "start_byte": 142458,
                  "end_byte": 142468,
                  "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/2/left/object/operand/callee_expression/member_location"
                },
                "object": {
                  "call_effects_or_result_proven": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/2/left/object/operand/callee_expression/object/call_effects_or_result_proven"
                  },
                  "callee_source": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/2/left/object/operand/callee_expression/object/callee_source"
                  },
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/2/left/object/operand/callee_expression/object/kind"
                  },
                  "arguments": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/2/left/object/operand/callee_expression/object/arguments"
                  },
                  "callee_expression": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/2/left/object/operand/callee_expression/object/callee_expression"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/2/left/object/operand/callee_expression/object/location"
                  }
                }
              },
              "location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3623,
                "column": 9,
                "end_line": 3625,
                "start_byte": 142404,
                "end_byte": 142484,
                "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/2/left/object/operand/location"
              }
            }
          }
        },
        "location": {
          "file": "crates/winwincode-codex/src/adapter.rs",
          "line": 3623,
          "column": 9,
          "end_line": 3626,
          "start_byte": 142404,
          "end_byte": 142516,
          "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/2/location"
        },
        "right": {
          "kind": "boolean_literal",
          "literal": false,
          "location": {
            "file": "crates/winwincode-codex/src/adapter.rs",
            "line": 3626,
            "column": 26,
            "end_line": 3626,
            "start_byte": 142511,
            "end_byte": 142516,
            "full_location_ref": "/functional_chains/11/pattern/sequences/submission/assignment_attempts/2/right/location"
          }
        }
      }
    ],
    "call_result_guard_source_links": [],
    "remaining_fields_ref": "/functional_chains/11/pattern/sequences/submission"
  }
}
```

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

### wwc-report-worker-adapter-record-identities

类型：`message_identity_relations`；源码关系评估：`scoped_source_relations_supported`。

保存发现：`476c604a9cc207b991b654d1`；证据：`1f2c773a6c7d0ed56f559e71`。

- `worker_control`：`crates/winwincode-worker/src/lib.rs` / `WorkerMain.accept_control`。
- `worker_dispatch`：`crates/winwincode-worker/src/lib.rs` / `WorkerMain.accept_dispatch`。
- `run_key_from_dispatch`：`crates/winwincode-codex/src/contract.rs` / `CodexRunKey.from_dispatch`。
- `worker_start`：`crates/winwincode-worker/src/lib.rs` / `WorkerMain.start_dispatch`。
- `adapter_ensure_thread`：`crates/winwincode-codex/src/adapter.rs` / `<ProductionCodexAdapter as CodexCoreAdapter>.ensure_thread`。
- `adapter_submit`：`crates/winwincode-codex/src/adapter.rs` / `<ProductionCodexAdapter as CodexCoreAdapter>.submit_turn`。
- `adapter_persist`：`crates/winwincode-codex/src/adapter.rs` / `ProductionCodexAdapter.persist_run`。
- `adapter_session_for_thread`：`crates/winwincode-codex/src/adapter.rs` / `ProductionCodexAdapter.session_for_thread`。
- `session_identity`：`crates/winwincode-codex/src/adapter.rs` / `session_identity`。
- `adapter_profile`：`crates/winwincode-codex/src/adapter.rs` / `production_agent_session_config`。

保存关系的展示摘要（`presentation_only=true`；不新增评级）：

完整 pattern：`/functional_chains/12/pattern`。展示截断：`true`；完整证据与原 pattern 保留。

| 保存字段 | 实际值 | 完整引用 |
| --- | --- | --- |
| creates_calls_edge | false | /functional_chains/12/pattern/creates_calls_edge |
| proof_domain | captured lexical binders, finite field/record projections, enum arms and registered literal SQL source bindings | /functional_chains/12/pattern/proof_domain |
| runtime_transport_or_physical_effect_proven | false | /functional_chains/12/pattern/runtime_transport_or_physical_effect_proven |
| scoped_source_supported | true | /functional_chains/12/pattern/scoped_source_supported |
| source_only | true | /functional_chains/12/pattern/source_only |
| version | captured-message-identity-relations-1 | /functional_chains/12/pattern/version |
| whole_project_identity_complete | false | /functional_chains/12/pattern/whole_project_identity_complete |

**budget**：`/functional_chains/12/pattern/budget`；展示截断：`false`。

```json
{
  "incomplete": false,
  "limit": 65536,
  "operations": 3619
}
```

**components**：`/functional_chains/12/pattern/components`；展示截断：`true`。

```json
{
  "worker_adapter_identity": {
    "all_profile_settings_fully_traced": false,
    "all_worker_messages_covered": false,
    "authority_and_result_values_proven": false,
    "execution_profile_projection_to_selected_consumer_only": true,
    "generic_codex_receiver_globally_bound": false,
    "kernel_session_equals_product_or_worker_session": false,
    "scope": "captured typed JobDispatch arm, explicit borrowed start record, selected adapter run and Kernel session/turn interfaces",
    "supported": true,
    "components": {
      "adapter_ensure_thread": {
        "supported": true,
        "deferred_callback_projections": [],
        "field_projections": {
          "shown_items": [
            {
              "source_fact_refs": [
                "/functional_chains/12/source_facts/299"
              ],
              "creates_calls_edge": false,
              "extractor_version": "captured-message-identity-relations-1",
              "field": "lease",
              "id": "f2284014deea7a05deb92f5f",
              "kind": "message_record_field_projection",
              "ordinary_generated_record_clone_model_required": true,
              "origin": "source-derived",
              "record_type_source": "ModelLeaseAuthority",
              "role": "adapter_ensure_thread",
              "target_code_executed": false,
              "location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3378,
                "column": 20,
                "end_line": 3378,
                "start_byte": 132046,
                "end_byte": 132065,
                "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/0/location"
              },
              "record_location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3377,
                "column": 25,
                "end_line": 3381,
                "start_byte": 132005,
                "end_byte": 132170,
                "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/0/record_location"
              },
              "source": {
                "root": "a7046714bfe5c34851da7fdf1873600f238d49d85efdc3b668a2b740c6320233",
                "root_name": "start",
                "binding": {
                  "declaration_id": "a7046714bfe5c34851da7fdf1873600f238d49d85efdc3b668a2b740c6320233",
                  "declaration_kind": "captured_rust_parameter",
                  "identity_complete": true,
                  "macro_namespace_complete": false,
                  "runtime_value_identity_proven": false,
                  "state": "unique",
                  "binder_location": {
                    "file": "crates/winwincode-codex/src/adapter.rs",
                    "line": 3336,
                    "column": 9,
                    "end_line": 3336,
                    "start_byte": 130183,
                    "end_byte": 130188,
                    "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/0/source/binding/binder_location"
                  },
                  "declaration_location": {
                    "file": "crates/winwincode-codex/src/adapter.rs",
                    "line": 3336,
                    "column": 9,
                    "end_line": 3336,
                    "start_byte": 130183,
                    "end_byte": 130210,
                    "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/0/source/binding/declaration_location"
                  }
                },
                "copy_operations": [
                  {
                    "method": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/0/source/copy_operations/0/method"
                    },
                    "ordinary_generated_data_clone_model_required": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/0/source/copy_operations/0/ordinary_generated_data_clone_model_required"
                    },
                    "location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/0/source/copy_operations/0/location"
                    }
                  }
                ],
                "location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 3378,
                  "column": 20,
                  "end_line": 3378,
                  "start_byte": 132046,
                  "end_byte": 132065,
                  "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/0/source/location"
                },
                "members": [
                  "lease"
                ]
              }
            },
            {
              "source_fact_refs": [
                "/functional_chains/12/source_facts/300"
              ],
              "creates_calls_edge": false,
              "extractor_version": "captured-message-identity-relations-1",
              "field": "worker_session_id",
              "id": "0851697608c62d0cd78d78cf",
              "kind": "message_record_field_projection",
              "ordinary_generated_record_clone_model_required": true,
              "origin": "source-derived",
              "record_type_source": "ModelLeaseAuthority",
              "role": "adapter_ensure_thread",
              "target_code_executed": false,
              "location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3379,
                "column": 32,
                "end_line": 3379,
                "start_byte": 132098,
                "end_byte": 132129,
                "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/1/location"
              },
              "record_location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3377,
                "column": 25,
                "end_line": 3381,
                "start_byte": 132005,
                "end_byte": 132170,
                "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/1/record_location"
              },
              "source": {
                "root": "a7046714bfe5c34851da7fdf1873600f238d49d85efdc3b668a2b740c6320233",
                "root_name": "start",
                "binding": {
                  "declaration_id": "a7046714bfe5c34851da7fdf1873600f238d49d85efdc3b668a2b740c6320233",
                  "declaration_kind": "captured_rust_parameter",
                  "identity_complete": true,
                  "macro_namespace_complete": false,
                  "runtime_value_identity_proven": false,
                  "state": "unique",
                  "binder_location": {
                    "file": "crates/winwincode-codex/src/adapter.rs",
                    "line": 3336,
                    "column": 9,
                    "end_line": 3336,
                    "start_byte": 130183,
                    "end_byte": 130188,
                    "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/1/source/binding/binder_location"
                  },
                  "declaration_location": {
                    "file": "crates/winwincode-codex/src/adapter.rs",
                    "line": 3336,
                    "column": 9,
                    "end_line": 3336,
                    "start_byte": 130183,
                    "end_byte": 130210,
                    "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/1/source/binding/declaration_location"
                  }
                },
                "copy_operations": [
                  {
                    "method": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/1/source/copy_operations/0/method"
                    },
                    "ordinary_generated_data_clone_model_required": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/1/source/copy_operations/0/ordinary_generated_data_clone_model_required"
                    },
                    "location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/1/source/copy_operations/0/location"
                    }
                  }
                ],
                "location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 3379,
                  "column": 32,
                  "end_line": 3379,
                  "start_byte": 132098,
                  "end_byte": 132129,
                  "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/1/source/location"
                },
                "members": [
                  "worker_session_id"
                ]
              }
            },
            {
              "source_fact_refs": [
                "/functional_chains/12/source_facts/301"
              ],
              "creates_calls_edge": false,
              "extractor_version": "captured-message-identity-relations-1",
              "field": "session_identity",
              "id": "882e2a83880632fe2123bee8",
              "kind": "message_record_field_projection",
              "ordinary_generated_record_clone_model_required": true,
              "origin": "source-derived",
              "record_type_source": "ModelLeaseAuthority",
              "role": "adapter_ensure_thread",
              "target_code_executed": false,
              "location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3380,
                "column": 13,
                "end_line": 3380,
                "start_byte": 132143,
                "end_byte": 132159,
                "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/2/location"
              },
              "record_location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3377,
                "column": 25,
                "end_line": 3381,
                "start_byte": 132005,
                "end_byte": 132170,
                "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/2/record_location"
              },
              "source": {
                "root": "7eae6b3ba13248d3e2c58cb9f51b62b8c9311ab040bb39484d89256ef673b959",
                "root_name": "session_identity",
                "binding": {
                  "declaration_id": "7eae6b3ba13248d3e2c58cb9f51b62b8c9311ab040bb39484d89256ef673b959",
                  "declaration_kind": "captured_rust_local",
                  "identity_complete": true,
                  "macro_namespace_complete": false,
                  "runtime_value_identity_proven": false,
                  "state": "unique",
                  "binder_location": {
                    "file": "crates/winwincode-codex/src/adapter.rs",
                    "line": 3376,
                    "column": 13,
                    "end_line": 3376,
                    "start_byte": 131918,
                    "end_byte": 131934,
                    "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/2/source/binding/binder_location"
                  },
                  "declaration_location": {
                    "file": "crates/winwincode-codex/src/adapter.rs",
                    "line": 3376,
                    "column": 9,
                    "end_line": 3376,
                    "start_byte": 131914,
                    "end_byte": 131980,
                    "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/2/source/binding/declaration_location"
                  }
                },
                "copy_operations": [],
                "location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 3380,
                  "column": 13,
                  "end_line": 3380,
                  "start_byte": 132143,
                  "end_byte": 132159,
                  "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/2/source/location"
                },
                "members": []
              }
            },
            {
              "source_fact_refs": [
                "/functional_chains/12/source_facts/302"
              ],
              "creates_calls_edge": false,
              "extractor_version": "captured-message-identity-relations-1",
              "field": "run_key",
              "id": "253b9efeceee1ffbacde439c",
              "kind": "message_record_field_projection",
              "ordinary_generated_record_clone_model_required": true,
              "origin": "source-derived",
              "record_type_source": "ModelRunBinding",
              "role": "adapter_ensure_thread",
              "target_code_executed": false,
              "location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3421,
                "column": 26,
                "end_line": 3421,
                "start_byte": 134007,
                "end_byte": 134022,
                "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/3/location"
              },
              "record_location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3420,
                "column": 27,
                "end_line": 3426,
                "start_byte": 133964,
                "end_byte": 134241,
                "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/3/record_location"
              },
              "source": {
                "root": "a2a4a2465d095ac29e6c69cc80d012a31d0b6da9a9fc2706ca9620636dfcee11",
                "root_name": "run_key",
                "binding": {
                  "declaration_id": "a2a4a2465d095ac29e6c69cc80d012a31d0b6da9a9fc2706ca9620636dfcee11",
                  "declaration_kind": "captured_rust_local",
                  "identity_complete": true,
                  "macro_namespace_complete": false,
                  "runtime_value_identity_proven": false,
                  "state": "unique",
                  "binder_location": {
                    "file": "crates/winwincode-codex/src/adapter.rs",
                    "line": 3339,
                    "column": 13,
                    "end_line": 3339,
                    "start_byte": 130307,
                    "end_byte": 130314,
                    "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/3/source/binding/binder_location"
                  },
                  "declaration_location": {
                    "file": "crates/winwincode-codex/src/adapter.rs",
                    "line": 3339,
                    "column": 9,
                    "end_line": 3343,
                    "start_byte": 130303,
                    "end_byte": 130432,
                    "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/3/source/binding/declaration_location"
                  }
                },
                "copy_operations": [
                  {
                    "method": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/3/source/copy_operations/0/method"
                    },
                    "ordinary_generated_data_clone_model_required": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/3/source/copy_operations/0/ordinary_generated_data_clone_model_required"
                    },
                    "location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/3/source/copy_operations/0/location"
                    }
                  }
                ],
                "location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 3421,
                  "column": 26,
                  "end_line": 3421,
                  "start_byte": 134007,
                  "end_byte": 134022,
                  "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/3/source/location"
                },
                "members": []
              }
            },
            {
              "source_fact_refs": [
                "/functional_chains/12/source_facts/303"
              ],
              "creates_calls_edge": false,
              "extractor_version": "captured-message-identity-relations-1",
              "field": "canonical_thread_id",
              "id": "7e626bba9598c1f3a56222fb",
              "kind": "message_record_field_projection",
              "ordinary_generated_record_clone_model_required": true,
              "origin": "source-derived",
              "record_type_source": "ModelRunBinding",
              "role": "adapter_ensure_thread",
              "target_code_executed": false,
              "location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3422,
                "column": 38,
                "end_line": 3422,
                "start_byte": 134061,
                "end_byte": 134070,
                "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/4/location"
              },
              "record_location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3420,
                "column": 27,
                "end_line": 3426,
                "start_byte": 133964,
                "end_byte": 134241,
                "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/4/record_location"
              },
              "source": {
                "root": "04ff7635431984f3a196589d60785c020b4ad78712804da10af4741cc878dc0d",
                "root_name": "thread_id",
                "binding": {
                  "declaration_id": "04ff7635431984f3a196589d60785c020b4ad78712804da10af4741cc878dc0d",
                  "declaration_kind": "captured_rust_local",
                  "identity_complete": true,
                  "macro_namespace_complete": false,
                  "runtime_value_identity_proven": false,
                  "state": "unique",
                  "binder_location": {
                    "file": "crates/winwincode-codex/src/adapter.rs",
                    "line": 3372,
                    "column": 13,
                    "end_line": 3372,
                    "start_byte": 131790,
                    "end_byte": 131799,
                    "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/4/source/binding/binder_location"
                  },
                  "declaration_location": {
                    "file": "crates/winwincode-codex/src/adapter.rs",
                    "line": 3372,
                    "column": 9,
                    "end_line": 3375,
                    "start_byte": 131786,
                    "end_byte": 131905,
                    "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/4/source/binding/declaration_location"
                  }
                },
                "copy_operations": [],
                "location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 3422,
                  "column": 38,
                  "end_line": 3422,
                  "start_byte": 134061,
                  "end_byte": 134070,
                  "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/4/source/location"
                },
                "members": []
              }
            },
            {
              "source_fact_refs": [
                "/functional_chains/12/source_facts/304"
              ],
              "creates_calls_edge": false,
              "extractor_version": "captured-message-identity-relations-1",
              "field": "authority",
              "id": "243fc840f1c2a6a0b0295599",
              "kind": "message_record_field_projection",
              "ordinary_generated_record_clone_model_required": true,
              "origin": "source-derived",
              "record_type_source": "ModelRunBinding",
              "role": "adapter_ensure_thread",
              "target_code_executed": false,
              "location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3424,
                "column": 17,
                "end_line": 3424,
                "start_byte": 134157,
                "end_byte": 134166,
                "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/5/location"
              },
              "record_location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3420,
                "column": 27,
                "end_line": 3426,
                "start_byte": 133964,
                "end_byte": 134241,
                "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/5/record_location"
              },
              "source": {
                "root": "1b2d431d639cab0b219c84305c8d544f09e5c92bd52859d094905c5b42f1427e",
                "root_name": "authority",
                "binding": {
                  "declaration_id": "1b2d431d639cab0b219c84305c8d544f09e5c92bd52859d094905c5b42f1427e",
                  "declaration_kind": "captured_rust_local",
                  "identity_complete": true,
                  "macro_namespace_complete": false,
                  "runtime_value_identity_proven": false,
                  "state": "unique",
                  "binder_location": {
                    "file": "crates/winwincode-codex/src/adapter.rs",
                    "line": 3377,
                    "column": 13,
                    "end_line": 3377,
                    "start_byte": 131993,
                    "end_byte": 132002,
                    "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/5/source/binding/binder_location"
                  },
                  "declaration_location": {
                    "file": "crates/winwincode-codex/src/adapter.rs",
                    "line": 3377,
                    "column": 9,
                    "end_line": 3381,
                    "start_byte": 131989,
                    "end_byte": 132171,
                    "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/5/source/binding/declaration_location"
                  }
                },
                "copy_operations": [],
                "location": {
                  "file": "crates/winwincode-codex/src/adapter.rs",
                  "line": 3424,
                  "column": 17,
                  "end_line": 3424,
                  "start_byte": 134157,
                  "end_byte": 134166,
                  "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections/5/source/location"
                },
                "members": []
              }
            }
          ],
          "shown_count": 6,
          "total_count": 30,
          "truncated": true,
          "full_value_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/field_projections"
        },
        "interface_arguments": {
          "shown_items": [
            {
              "source_fact_refs": [
                "/functional_chains/12/source_facts/329"
              ],
              "callee_source": "self\n            .kernel\n            .create_session",
              "creates_calls_edge": false,
              "extractor_version": "captured-message-identity-relations-1",
              "id": "bc8be5f52e6c213b93cd3713",
              "kind": "message_interface_argument_projections",
              "method_source_name": "create_session",
              "origin": "source-derived",
              "role": "adapter_ensure_thread",
              "runtime_dispatch_proven": false,
              "target_code_executed": false,
              "arguments": [
                {
                  "record": null,
                  "source_path": null,
                  "location": {
                    "file": "crates/winwincode-codex/src/adapter.rs",
                    "line": 3454,
                    "column": 29,
                    "end_line": 3459,
                    "start_byte": 135484,
                    "end_byte": 135647,
                    "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/interface_arguments/0/arguments/0/location"
                  }
                }
              ],
              "branch_context": [],
              "location": {
                "file": "crates/winwincode-codex/src/adapter.rs",
                "line": 3452,
                "column": 23,
                "end_line": 3459,
                "start_byte": 135431,
                "end_byte": 135648,
                "full_location_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/interface_arguments/0/location"
              }
            },
            {
              "source_fact_refs": [
                "/functional_chains/12/source_facts/330"
              ],
              "callee_source": "production_agent_session_config",
              "creates_calls_edge": false,
              "extractor_version": "captured-message-identity-relations-1",
              "id": "01667492ed247c85fdd6a7ad",
              "kind": "message_interface_argument_projections",
              "method_source_name": "production_agent_session_config",
              "origin": "source-derived",
              "remaining_fields_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/interface_arguments/1"
            }
          ],
          "shown_count": 2,
          "total_count": 3,
          "truncated": true,
          "full_value_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread/interface_arguments"
        },
        "remaining_fields_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components/adapter_ensure_thread"
      },
      "remaining_fields_ref": "/functional_chains/12/pattern/components/worker_adapter_identity/components"
    },
    "remaining_fields_ref": "/functional_chains/12/pattern/components/worker_adapter_identity"
  }
}
```

**limits**：`/functional_chains/12/pattern/limits`；展示截断：`false`。

```json
[
  "member paths identify source projections, not globally stable heap cells",
  "Rust Clone/borrow projections require ordinary generated data semantics; arbitrary trait behavior is not inferred",
  "generic adapter calls remain contextual source interfaces, never global unique targets",
  "correlation tuple agreement is a field-domain agreement; payload equality is checked by source consumers, not assumed",
  "SQL parameters are captured token positions under the registered literal source model; no database is executed",
  "retries, rejected/replayed acks, all crash windows and external authenticity are not fully proved"
]
```

**models**：`/functional_chains/12/pattern/models`；展示截断：`false`。

```json
[
  "finite-captured-record-message-identities-v1"
]
```

**relation_fact_ids**：`/functional_chains/12/pattern/relation_fact_ids`；展示截断：`true`。

```json
{
  "shown_items": [
    "8918b120f8d48c35f8ad0ec2",
    "7be2a596f4b58c62a4498da3",
    "4c77a1b57c3ce9e39735cc29",
    "f10a09209800a8535aa10066",
    "399902f20bd942e722febaaf",
    "d11da50287a276b4cc078a11"
  ],
  "shown_count": 6,
  "total_count": 86,
  "truncated": true,
  "full_value_ref": "/functional_chains/12/pattern/relation_fact_ids"
}
```

自动关系类型：`{"captured_call_step": 257, "message_adapter_job_profile_consumer_source_join": 1, "message_captured_record_fields": 12, "message_deferred_map_field_projection": 1, "message_dispatch_run_key_start_source_join": 1, "message_enum_arm_consumers": 9, "message_interface_argument_projections": 10, "message_record_field_assignment": 3, "message_record_field_projection": 47, "message_stored_submission_identity_reconcile_source_join": 1, "message_submission_intent_persist_reconcile_order": 1, "report_source_role": 10}`。

分析缺口：

```json
[]
```

条件与反证声明（单列为配置范围，不冒充源码证据）：

```json
{
  "applicability": {
    "conditions": [
      "Selected captured declarations are authenticated.",
      "Ordinary generated data retains normal borrowed/copied field semantics; source reaching is conditional, not observed execution."
    ],
    "counterexamples": [
      "Generic dispatch, wire equality, physical storage success and complete crash recovery are not inferred."
    ],
    "kind": "conditional"
  },
  "descriptive_counterexamples_are_computed_evidence": false,
  "origin": "policy-declared",
  "provenance": {
    "author_approved": false,
    "authority": "original-static-report-benchmark",
    "note": "Declaration locators only. Field records and consumers derive from authenticated saved source; no paths or expected outcomes are provided.",
    "source_doc": "reports/astra-baseline/WINWINCODE_ANALYSIS.md"
  }
}
```

### wwc-report-worker-bootstrap-entries

类型：`guarded_call_sequence`；源码关系评估：`scoped_source_relations_supported`。

保存发现：`04ee83bf9ca6e6b33b2656d6`；证据：`9df4cf4113207a99c88623ae`。

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

保存关系的展示摘要（`presentation_only=true`；不新增评级）：

完整 pattern：`/functional_chains/13/pattern`。展示截断：`true`；完整证据与原 pattern 保留。

| 保存字段 | 实际值 | 完整引用 |
| --- | --- | --- |
| scoped_source_supported | true | /functional_chains/13/pattern/scoped_source_supported |

**nested_source_regions**：`/functional_chains/13/pattern/nested_source_regions`；展示截断：`false`。

```json
[]
```

**sequences**：`/functional_chains/13/pattern/sequences`；展示截断：`true`。

```json
{
  "entry": {
    "all_function_paths_or_effects_accounted": false,
    "future_or_callback_activation_proven": false,
    "region_kind": "function_item",
    "role": "entry",
    "assignment_attempts": [],
    "call_result_guard_source_links": [],
    "conditions": [],
    "guards": [],
    "opaque_direct_control_regions": [],
    "orders": [
      {
        "source_fact_refs": [
          "/functional_chains/13/source_facts/56"
        ],
        "after_step_id": "f855d8faeed6db98f32e895e",
        "all_paths_reach_next_proven": false,
        "before_step_id": "84db448869e8ab3a3b5ebc7a",
        "id": "265b4b63d5cc2b515a588ae5",
        "kind": "conditional_direct_statement_order",
        "model_id": "captured-normal-statement-control-v1",
        "origin": "source-derived",
        "role": "entry",
        "conditions": [
          "both direct statements normally reached in the same invocation",
          "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
        ],
        "location": {
          "file": "crates/winwincode-worker/src/main.rs",
          "line": 36,
          "column": 5,
          "end_line": 49,
          "start_byte": 1408,
          "end_byte": 1968,
          "full_location_ref": "/functional_chains/13/pattern/sequences/entry/orders/0/location"
        }
      }
    ],
    "source_region_location": {
      "file": "crates/winwincode-worker/src/main.rs",
      "line": 34,
      "column": 1,
      "end_line": 50,
      "start_byte": 1352,
      "end_byte": 1970,
      "full_location_ref": "/functional_chains/13/pattern/sequences/entry/source_region_location"
    },
    "steps": [
      {
        "source_fact_refs": [
          "/functional_chains/13/source_facts/54"
        ],
        "conditional_normal_reaching_only": true,
        "id": "84db448869e8ab3a3b5ebc7a",
        "kind": "direct_statement_call_step",
        "origin": "source-derived",
        "role": "entry",
        "source_order_index": 0,
        "statement_kind": "let_declaration",
        "call_ids": [
          "03754aa881b2396bcb89406f",
          "1914a85879a9ff98696f4b55"
        ],
        "location": {
          "file": "crates/winwincode-worker/src/main.rs",
          "line": 35,
          "column": 5,
          "end_line": 35,
          "start_byte": 1368,
          "end_byte": 1403,
          "full_location_ref": "/functional_chains/13/pattern/sequences/entry/steps/0/location"
        }
      },
      {
        "source_fact_refs": [
          "/functional_chains/13/source_facts/55"
        ],
        "conditional_normal_reaching_only": true,
        "id": "f855d8faeed6db98f32e895e",
        "kind": "direct_statement_call_step",
        "origin": "source-derived",
        "role": "entry",
        "source_order_index": 1,
        "statement_kind": "expression_statement",
        "call_ids": {
          "shown_items": [
            "4206723097a6278b9dde3432",
            "7faf1e9ebda3aea25b095069",
            "cfb2ff00875535ddcac8ffc2",
            "92511a63cd4369eaba007d4b",
            "d321cc400e6c88439599403d",
            "5e936c5e189f24eda4f0f9c8"
          ],
          "shown_count": 6,
          "total_count": 14,
          "truncated": true,
          "full_value_ref": "/functional_chains/13/pattern/sequences/entry/steps/1/call_ids"
        },
        "location": {
          "file": "crates/winwincode-worker/src/main.rs",
          "line": 36,
          "column": 5,
          "end_line": 49,
          "start_byte": 1408,
          "end_byte": 1968,
          "full_location_ref": "/functional_chains/13/pattern/sequences/entry/steps/1/location"
        }
      }
    ]
  },
  "managed": {
    "all_function_paths_or_effects_accounted": false,
    "future_or_callback_activation_proven": false,
    "region_kind": "function_item",
    "role": "managed",
    "assignment_attempts": [],
    "call_result_guard_source_links": [],
    "conditions": [],
    "guards": [],
    "opaque_direct_control_regions": [],
    "orders": [
      {
        "source_fact_refs": [
          "/functional_chains/13/source_facts/74"
        ],
        "after_step_id": "83cb0b8e2f8f12f77a97a88f",
        "all_paths_reach_next_proven": false,
        "before_step_id": "0225b558710e668351d46e78",
        "id": "06131a4a2993355f17c5c54c",
        "kind": "conditional_direct_statement_order",
        "model_id": "captured-normal-statement-control-v1",
        "origin": "source-derived",
        "role": "managed",
        "conditions": [
          "both direct statements normally reached in the same invocation",
          "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
        ],
        "location": {
          "file": "crates/winwincode-worker/src/main.rs",
          "line": 120,
          "column": 5,
          "end_line": 120,
          "start_byte": 4805,
          "end_byte": 4885,
          "full_location_ref": "/functional_chains/13/pattern/sequences/managed/orders/0/location"
        }
      },
      {
        "source_fact_refs": [
          "/functional_chains/13/source_facts/75"
        ],
        "after_step_id": "2f68b43760563eb6f3d9e6e8",
        "all_paths_reach_next_proven": false,
        "before_step_id": "83cb0b8e2f8f12f77a97a88f",
        "id": "863fb101ec0515e7effe268a",
        "kind": "conditional_direct_statement_order",
        "model_id": "captured-normal-statement-control-v1",
        "origin": "source-derived",
        "role": "managed",
        "conditions": [
          "both direct statements normally reached in the same invocation",
          "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
        ],
        "location": {
          "file": "crates/winwincode-worker/src/main.rs",
          "line": 133,
          "column": 5,
          "end_line": 148,
          "start_byte": 5410,
          "end_byte": 6053,
          "full_location_ref": "/functional_chains/13/pattern/sequences/managed/orders/1/location"
        }
      }
    ],
    "source_region_location": {
      "file": "crates/winwincode-worker/src/main.rs",
      "line": 118,
      "column": 1,
      "end_line": 149,
      "start_byte": 4636,
      "end_byte": 6055,
      "full_location_ref": "/functional_chains/13/pattern/sequences/managed/source_region_location"
    },
    "steps": [
      {
        "source_fact_refs": [
          "/functional_chains/13/source_facts/68"
        ],
        "conditional_normal_reaching_only": true,
        "id": "0225b558710e668351d46e78",
        "kind": "direct_statement_call_step",
        "origin": "source-derived",
        "role": "managed",
        "source_order_index": 0,
        "statement_kind": "let_declaration",
        "call_ids": [
          "9ed734f55105cd88b51fe697",
          "8ee566d2d5d726c65d77fe92"
        ],
        "location": {
          "file": "crates/winwincode-worker/src/main.rs",
          "line": 119,
          "column": 5,
          "end_line": 119,
          "start_byte": 4724,
          "end_byte": 4800,
          "full_location_ref": "/functional_chains/13/pattern/sequences/managed/steps/0/location"
        }
      },
      {
        "source_fact_refs": [
          "/functional_chains/13/source_facts/69"
        ],
        "conditional_normal_reaching_only": true,
        "id": "83cb0b8e2f8f12f77a97a88f",
        "kind": "direct_statement_call_step",
        "origin": "source-derived",
        "role": "managed",
        "source_order_index": 1,
        "statement_kind": "let_declaration",
        "call_ids": [
          "b6e39c3ad7acc40181a57050"
        ],
        "location": {
          "file": "crates/winwincode-worker/src/main.rs",
          "line": 120,
          "column": 5,
          "end_line": 120,
          "start_byte": 4805,
          "end_byte": 4885,
          "full_location_ref": "/functional_chains/13/pattern/sequences/managed/steps/1/location"
        }
      },
      {
        "source_fact_refs": [
          "/functional_chains/13/source_facts/70"
        ],
        "conditional_normal_reaching_only": true,
        "id": "2f68b43760563eb6f3d9e6e8",
        "kind": "direct_statement_call_step",
        "origin": "source-derived",
        "role": "managed",
        "source_order_index": 2,
        "statement_kind": "await_expression",
        "call_ids": {
          "shown_items": [
            "a11c38d59f2b05d5b7b84407",
            "e23d531afc5c9b1341963cc1",
            "04e7ee2de799915d8c2db67a",
            "c466cc3f9c9387849fb0226f",
            "be43319fbb777de039399d86",
            "ae16be53fe7f5afa3a9a6520"
          ],
          "shown_count": 6,
          "total_count": 13,
          "truncated": true,
          "full_value_ref": "/functional_chains/13/pattern/sequences/managed/steps/2/call_ids"
        },
        "location": {
          "file": "crates/winwincode-worker/src/main.rs",
          "line": 133,
          "column": 5,
          "end_line": 148,
          "start_byte": 5410,
          "end_byte": 6053,
          "full_location_ref": "/functional_chains/13/pattern/sequences/managed/steps/2/location"
        }
      }
    ]
  },
  "remote": {
    "all_function_paths_or_effects_accounted": false,
    "future_or_callback_activation_proven": false,
    "region_kind": "function_item",
    "role": "remote",
    "assignment_attempts": [],
    "call_result_guard_source_links": [],
    "conditions": [],
    "guards": [],
    "opaque_direct_control_regions": [],
    "orders": [
      {
        "source_fact_refs": [
          "/functional_chains/13/source_facts/67"
        ],
        "after_step_id": "3d06473a063c3537879241ef",
        "all_paths_reach_next_proven": false,
        "before_step_id": "7c5de1190abf65764940034a",
        "id": "4562d61334e1a5cc4d015a63",
        "kind": "conditional_direct_statement_order",
        "model_id": "captured-normal-statement-control-v1",
        "origin": "source-derived",
        "role": "remote",
        "conditions": [
          "both direct statements normally reached in the same invocation",
          "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
        ],
        "location": {
          "file": "crates/winwincode-worker/src/main.rs",
          "line": 110,
          "column": 5,
          "end_line": 110,
          "start_byte": 4256,
          "end_byte": 4293,
          "full_location_ref": "/functional_chains/13/pattern/sequences/remote/orders/0/location"
        }
      }
    ],
    "source_region_location": {
      "file": "crates/winwincode-worker/src/main.rs",
      "line": 97,
      "column": 1,
      "end_line": 111,
      "start_byte": 3451,
      "end_byte": 4295,
      "full_location_ref": "/functional_chains/13/pattern/sequences/remote/source_region_location"
    },
    "steps": [
      {
        "source_fact_refs": [
          "/functional_chains/13/source_facts/57"
        ],
        "conditional_normal_reaching_only": true,
        "id": "7c5de1190abf65764940034a",
        "kind": "direct_statement_call_step",
        "origin": "source-derived",
        "role": "remote",
        "source_order_index": 0,
        "statement_kind": "let_declaration",
        "call_ids": {
          "shown_items": [
            "77d5fd7f0b67e137d1b0c7cb",
            "0719af6e880b2e21be45098c",
            "de96b18ec859e70c248339ca",
            "b96b760c6da15a3ac32fa7be",
            "fcce0a5db9479897eff532df",
            "ff3b3144df8c58bfa8ec6f24"
          ],
          "shown_count": 6,
          "total_count": 17,
          "truncated": true,
          "full_value_ref": "/functional_chains/13/pattern/sequences/remote/steps/0/call_ids"
        },
        "location": {
          "file": "crates/winwincode-worker/src/main.rs",
          "line": 98,
          "column": 5,
          "end_line": 109,
          "start_byte": 3521,
          "end_byte": 4251,
          "full_location_ref": "/functional_chains/13/pattern/sequences/remote/steps/0/location"
        }
      },
      {
        "source_fact_refs": [
          "/functional_chains/13/source_facts/58"
        ],
        "conditional_normal_reaching_only": true,
        "id": "3d06473a063c3537879241ef",
        "kind": "direct_statement_call_step",
        "origin": "source-derived",
        "role": "remote",
        "source_order_index": 1,
        "statement_kind": "await_expression",
        "call_ids": [
          "3724f44725ff0ad3b56031e2",
          "3677accfe86ce2593a456661"
        ],
        "location": {
          "file": "crates/winwincode-worker/src/main.rs",
          "line": 110,
          "column": 5,
          "end_line": 110,
          "start_byte": 4256,
          "end_byte": 4293,
          "full_location_ref": "/functional_chains/13/pattern/sequences/remote/steps/1/location"
        }
      }
    ]
  }
}
```

自动关系类型：`{"captured_call_step": 51, "conditional_direct_statement_order": 4, "direct_statement_call_step": 7, "report_source_role": 3, "result_try_normal_continuation": 11}`。

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

类型：`guarded_call_sequence`；源码关系评估：`scoped_source_relations_supported`。

保存发现：`ffa5234d6efa3458bf87eb4d`；证据：`3f0ada51f2258a0c6ef4e8d8`。

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

保存关系的展示摘要（`presentation_only=true`；不新增评级）：

完整 pattern：`/functional_chains/14/pattern`。展示截断：`true`；完整证据与原 pattern 保留。

| 保存字段 | 实际值 | 完整引用 |
| --- | --- | --- |
| scoped_source_supported | true | /functional_chains/14/pattern/scoped_source_supported |

**nested_source_regions**：`/functional_chains/14/pattern/nested_source_regions`；展示截断：`false`。

```json
[]
```

**sequences**：`/functional_chains/14/pattern/sequences`；展示截断：`true`。

```json
{
  "adapter_factory": {
    "all_function_paths_or_effects_accounted": false,
    "future_or_callback_activation_proven": false,
    "region_kind": "function_item",
    "role": "adapter_factory",
    "assignment_attempts": [],
    "call_result_guard_source_links": [],
    "conditions": [],
    "guards": [],
    "opaque_direct_control_regions": [],
    "orders": {
      "shown_items": [
        {
          "source_fact_refs": [
            "/functional_chains/14/source_facts/167"
          ],
          "after_step_id": "8c1ecd3ca350be13b4ee01bc",
          "all_paths_reach_next_proven": false,
          "before_step_id": "d9d40a2fc0db59cda153ef67",
          "id": "88d16950f471d8b99dc2a9de",
          "kind": "conditional_direct_statement_order",
          "model_id": "captured-normal-statement-control-v1",
          "origin": "source-derived",
          "role": "adapter_factory",
          "conditions": [
            "both direct statements normally reached in the same invocation",
            "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
          ],
          "location": {
            "file": "crates/winwincode-worker/src/main.rs",
            "line": 326,
            "column": 5,
            "end_line": 326,
            "start_byte": 13491,
            "end_byte": 13571,
            "full_location_ref": "/functional_chains/14/pattern/sequences/adapter_factory/orders/0/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/14/source_facts/168"
          ],
          "after_step_id": "79770f8af7282f716af88112",
          "all_paths_reach_next_proven": false,
          "before_step_id": "8c1ecd3ca350be13b4ee01bc",
          "id": "8a3f65a39d76519f56b6fc27",
          "kind": "conditional_direct_statement_order",
          "model_id": "captured-normal-statement-control-v1",
          "origin": "source-derived",
          "role": "adapter_factory",
          "conditions": [
            "both direct statements normally reached in the same invocation",
            "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
          ],
          "location": {
            "file": "crates/winwincode-worker/src/main.rs",
            "line": 327,
            "column": 5,
            "end_line": 327,
            "start_byte": 13576,
            "end_byte": 13616,
            "full_location_ref": "/functional_chains/14/pattern/sequences/adapter_factory/orders/1/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/14/source_facts/169"
          ],
          "after_step_id": "9a0b3c525219c039345405d7",
          "all_paths_reach_next_proven": false,
          "before_step_id": "79770f8af7282f716af88112",
          "id": "3cdb485af0c8b5d2d5af3530",
          "kind": "conditional_direct_statement_order",
          "model_id": "captured-normal-statement-control-v1",
          "origin": "source-derived",
          "role": "adapter_factory",
          "conditions": [
            "both direct statements normally reached in the same invocation",
            "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
          ],
          "location": {
            "file": "crates/winwincode-worker/src/main.rs",
            "line": 328,
            "column": 5,
            "end_line": 328,
            "start_byte": 13621,
            "end_byte": 13715,
            "full_location_ref": "/functional_chains/14/pattern/sequences/adapter_factory/orders/2/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/14/source_facts/170"
          ],
          "after_step_id": "62c96685baf439252706abea",
          "all_paths_reach_next_proven": false,
          "before_step_id": "9a0b3c525219c039345405d7",
          "id": "b55143cf88778516ef492fd5",
          "kind": "conditional_direct_statement_order",
          "model_id": "captured-normal-statement-control-v1",
          "origin": "source-derived",
          "role": "adapter_factory",
          "conditions": [
            "both direct statements normally reached in the same invocation",
            "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
          ],
          "location": {
            "file": "crates/winwincode-worker/src/main.rs",
            "line": 329,
            "column": 5,
            "end_line": 329,
            "start_byte": 13720,
            "end_byte": 13765,
            "full_location_ref": "/functional_chains/14/pattern/sequences/adapter_factory/orders/3/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/14/source_facts/171"
          ],
          "after_step_id": "27d7177b077eaf7cfc726727",
          "all_paths_reach_next_proven": false,
          "before_step_id": "62c96685baf439252706abea",
          "id": "0a19306779b2faa8acb2145b",
          "kind": "conditional_direct_statement_order",
          "model_id": "captured-normal-statement-control-v1",
          "origin": "source-derived",
          "role": "adapter_factory",
          "conditions": [
            "both direct statements normally reached in the same invocation",
            "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
          ],
          "location": {
            "file": "crates/winwincode-worker/src/main.rs",
            "line": 330,
            "column": 5,
            "end_line": 342,
            "start_byte": 13770,
            "end_byte": 14335,
            "full_location_ref": "/functional_chains/14/pattern/sequences/adapter_factory/orders/4/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/14/source_facts/172"
          ],
          "after_step_id": "1cf4bb8bee9a9fccdc3577d4",
          "all_paths_reach_next_proven": false,
          "before_step_id": "27d7177b077eaf7cfc726727",
          "id": "ea704c0d96d7cc8b47c074ba",
          "kind": "conditional_direct_statement_order",
          "model_id": "captured-normal-statement-control-v1",
          "origin": "source-derived",
          "role": "adapter_factory",
          "conditions": [
            "both direct statements normally reached in the same invocation",
            "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
          ],
          "location": {
            "file": "crates/winwincode-worker/src/main.rs",
            "line": 343,
            "column": 5,
            "end_line": 347,
            "start_byte": 14340,
            "end_byte": 14571,
            "full_location_ref": "/functional_chains/14/pattern/sequences/adapter_factory/orders/5/location"
          }
        }
      ],
      "shown_count": 6,
      "total_count": 10,
      "truncated": true,
      "full_value_ref": "/functional_chains/14/pattern/sequences/adapter_factory/orders"
    },
    "source_region_location": {
      "file": "crates/winwincode-worker/src/main.rs",
      "line": 315,
      "column": 1,
      "end_line": 375,
      "start_byte": 13028,
      "end_byte": 15782,
      "full_location_ref": "/functional_chains/14/pattern/sequences/adapter_factory/source_region_location"
    },
    "steps": {
      "shown_items": [
        {
          "source_fact_refs": [
            "/functional_chains/14/source_facts/141"
          ],
          "conditional_normal_reaching_only": true,
          "id": "d9d40a2fc0db59cda153ef67",
          "kind": "direct_statement_call_step",
          "origin": "source-derived",
          "role": "adapter_factory",
          "source_order_index": 0,
          "statement_kind": "let_declaration",
          "call_ids": [
            "18ea9d36326c3e4b765adeb6",
            "18a64059bfea2023cd5403f1",
            "79867a94a32594d0a55a0121"
          ],
          "location": {
            "file": "crates/winwincode-worker/src/main.rs",
            "line": 323,
            "column": 5,
            "end_line": 325,
            "start_byte": 13342,
            "end_byte": 13486,
            "full_location_ref": "/functional_chains/14/pattern/sequences/adapter_factory/steps/0/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/14/source_facts/142"
          ],
          "conditional_normal_reaching_only": true,
          "id": "8c1ecd3ca350be13b4ee01bc",
          "kind": "direct_statement_call_step",
          "origin": "source-derived",
          "role": "adapter_factory",
          "source_order_index": 1,
          "statement_kind": "let_declaration",
          "call_ids": [
            "c63c84fa721d36d489d8ac9c"
          ],
          "location": {
            "file": "crates/winwincode-worker/src/main.rs",
            "line": 326,
            "column": 5,
            "end_line": 326,
            "start_byte": 13491,
            "end_byte": 13571,
            "full_location_ref": "/functional_chains/14/pattern/sequences/adapter_factory/steps/1/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/14/source_facts/143"
          ],
          "conditional_normal_reaching_only": true,
          "id": "79770f8af7282f716af88112",
          "kind": "direct_statement_call_step",
          "origin": "source-derived",
          "role": "adapter_factory",
          "source_order_index": 2,
          "statement_kind": "let_declaration",
          "call_ids": [
            "fe24852a475de0613c3824ba"
          ],
          "location": {
            "file": "crates/winwincode-worker/src/main.rs",
            "line": 327,
            "column": 5,
            "end_line": 327,
            "start_byte": 13576,
            "end_byte": 13616,
            "full_location_ref": "/functional_chains/14/pattern/sequences/adapter_factory/steps/2/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/14/source_facts/144"
          ],
          "conditional_normal_reaching_only": true,
          "id": "9a0b3c525219c039345405d7",
          "kind": "direct_statement_call_step",
          "origin": "source-derived",
          "role": "adapter_factory",
          "source_order_index": 3,
          "statement_kind": "let_declaration",
          "call_ids": [
            "8b5acb3aaf96438b4dbd6c55",
            "ec8517b67914dba68e6580fd"
          ],
          "location": {
            "file": "crates/winwincode-worker/src/main.rs",
            "line": 328,
            "column": 5,
            "end_line": 328,
            "start_byte": 13621,
            "end_byte": 13715,
            "full_location_ref": "/functional_chains/14/pattern/sequences/adapter_factory/steps/3/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/14/source_facts/145"
          ],
          "conditional_normal_reaching_only": true,
          "id": "62c96685baf439252706abea",
          "kind": "direct_statement_call_step",
          "origin": "source-derived",
          "role": "adapter_factory",
          "source_order_index": 4,
          "statement_kind": "let_declaration",
          "call_ids": [
            "be984c0afe6349c282a7caa0"
          ],
          "location": {
            "file": "crates/winwincode-worker/src/main.rs",
            "line": 329,
            "column": 5,
            "end_line": 329,
            "start_byte": 13720,
            "end_byte": 13765,
            "full_location_ref": "/functional_chains/14/pattern/sequences/adapter_factory/steps/4/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/14/source_facts/146"
          ],
          "conditional_normal_reaching_only": true,
          "id": "27d7177b077eaf7cfc726727",
          "kind": "direct_statement_call_step",
          "origin": "source-derived",
          "role": "adapter_factory",
          "source_order_index": 5,
          "statement_kind": "expression_statement",
          "call_ids": [
            "2b0b6d4e28224b4165f8bd2b",
            "4c302d9ffc58664f12e5c94f",
            "45059eb160cb5001e7ff6924"
          ],
          "location": {
            "file": "crates/winwincode-worker/src/main.rs",
            "line": 330,
            "column": 5,
            "end_line": 342,
            "start_byte": 13770,
            "end_byte": 14335,
            "full_location_ref": "/functional_chains/14/pattern/sequences/adapter_factory/steps/5/location"
          }
        }
      ],
      "shown_count": 6,
      "total_count": 11,
      "truncated": true,
      "full_value_ref": "/functional_chains/14/pattern/sequences/adapter_factory/steps"
    }
  },
  "shared_loop": {
    "all_function_paths_or_effects_accounted": false,
    "future_or_callback_activation_proven": false,
    "region_kind": "function_item",
    "role": "shared_loop",
    "assignment_attempts": [
      {
        "source_fact_refs": [
          "/functional_chains/14/source_facts/121"
        ],
        "id": "d09a8821a5bea56da303b559",
        "kind": "ordered_source_assignment_attempt",
        "origin": "source-derived",
        "role": "shared_loop",
        "write_runtime_success_proven": false,
        "branch_context": [
          {
            "branch": "then",
            "condition_truth_proven": false,
            "kind": "if",
            "condition": {
              "kind": "let_condition",
              "runtime_value_proven": false,
              "source": "let Some(observation_model) = observation_model",
              "source_truncated": false,
              "location": {
                "file": "crates/winwincode-worker/src/main.rs",
                "line": 204,
                "column": 8,
                "end_line": 204,
                "start_byte": 8265,
                "end_byte": 8312,
                "full_location_ref": "/functional_chains/14/pattern/sequences/shared_loop/assignment_attempts/0/branch_context/0/condition/location"
              }
            },
            "location": {
              "file": "crates/winwincode-worker/src/main.rs",
              "line": 204,
              "column": 5,
              "end_line": 206,
              "start_byte": 8262,
              "end_byte": 8387,
              "full_location_ref": "/functional_chains/14/pattern/sequences/shared_loop/assignment_attempts/0/branch_context/0/location"
            }
          }
        ],
        "left": {
          "kind": "identifier",
          "name": "worker",
          "location": {
            "file": "crates/winwincode-worker/src/main.rs",
            "line": 205,
            "column": 9,
            "end_line": 205,
            "start_byte": 8323,
            "end_byte": 8329,
            "full_location_ref": "/functional_chains/14/pattern/sequences/shared_loop/assignment_attempts/0/left/location"
          },
          "reference": {
            "declaration_id": "a629bf62724062dbd879ae08e9dd01ffb2bf3d544980a278a7bc2b7d1c0e81d4",
            "declaration_kind": "captured_rust_local",
            "identity_scope": "plain captured binder syntax only",
            "macro_namespace_complete": false,
            "runtime_value_identity_proven": false,
            "state": "captured_unique_rust_binder",
            "binder_location": {
              "file": "crates/winwincode-worker/src/main.rs",
              "line": 199,
              "column": 13,
              "end_line": 199,
              "start_byte": 7980,
              "end_byte": 7986,
              "full_location_ref": "/functional_chains/14/pattern/sequences/shared_loop/assignment_attempts/0/left/reference/binder_location"
            },
            "declaration_location": {
              "file": "crates/winwincode-worker/src/main.rs",
              "line": 199,
              "column": 5,
              "end_line": 203,
              "start_byte": 7972,
              "end_byte": 8257,
              "full_location_ref": "/functional_chains/14/pattern/sequences/shared_loop/assignment_attempts/0/left/reference/declaration_location"
            }
          }
        },
        "location": {
          "file": "crates/winwincode-worker/src/main.rs",
          "line": 205,
          "column": 9,
          "end_line": 205,
          "start_byte": 8323,
          "end_byte": 8380,
          "full_location_ref": "/functional_chains/14/pattern/sequences/shared_loop/assignment_attempts/0/location"
        },
        "right": {
          "call_effects_or_result_proven": false,
          "callee_source": "worker.with_observation_model",
          "kind": "call_expression",
          "arguments": [
            {
              "kind": "identifier",
              "name": "observation_model",
              "location": {
                "file": "crates/winwincode-worker/src/main.rs",
                "line": 205,
                "column": 48,
                "end_line": 205,
                "start_byte": 8362,
                "end_byte": 8379,
                "full_location_ref": "/functional_chains/14/pattern/sequences/shared_loop/assignment_attempts/0/right/arguments/0/location"
              },
              "reference": {
                "declaration_id": "c33393ca9eda1bb3c0d861a16dbd555f134e0f704808f9d98156e9d508f37c53",
                "declaration_kind": "captured_rust_local",
                "identity_scope": "plain captured binder syntax only",
                "macro_namespace_complete": false,
                "runtime_value_identity_proven": false,
                "state": "captured_unique_rust_binder",
                "binder_location": {
                  "file": "crates/winwincode-worker/src/main.rs",
                  "line": 170,
                  "column": 9,
                  "end_line": 170,
                  "start_byte": 6860,
                  "end_byte": 6877,
                  "full_location_ref": "/functional_chains/14/pattern/sequences/shared_loop/assignment_attempts/0/right/arguments/0/reference/binder_location"
                },
                "declaration_location": {
                  "file": "crates/winwincode-worker/src/main.rs",
                  "line": 170,
                  "column": 5,
                  "end_line": 170,
                  "start_byte": 6856,
                  "end_byte": 6935,
                  "full_location_ref": "/functional_chains/14/pattern/sequences/shared_loop/assignment_attempts/0/right/arguments/0/reference/declaration_location"
                }
              }
            }
          ],
          "callee_expression": {
            "current_referent_value_proven": false,
            "kind": "field_expression",
            "member": "with_observation_model",
            "location": {
              "file": "crates/winwincode-worker/src/main.rs",
              "line": 205,
              "column": 18,
              "end_line": 205,
              "start_byte": 8332,
              "end_byte": 8361,
              "full_location_ref": "/functional_chains/14/pattern/sequences/shared_loop/assignment_attempts/0/right/callee_expression/location"
            },
            "remaining_fields_ref": "/functional_chains/14/pattern/sequences/shared_loop/assignment_attempts/0/right/callee_expression"
          },
          "remaining_fields_ref": "/functional_chains/14/pattern/sequences/shared_loop/assignment_attempts/0/right"
        }
      }
    ],
    "remaining_fields_ref": "/functional_chains/14/pattern/sequences/shared_loop"
  },
  "remaining_fields_ref": "/functional_chains/14/pattern/sequences"
}
```

自动关系类型：`{"captured_call_step": 89, "conditional_direct_statement_order": 28, "direct_statement_call_step": 31, "ordered_source_assignment_attempt": 1, "report_source_role": 3, "result_try_normal_continuation": 28, "source_guard_and_abrupt_branch": 2}`。

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

保存发现：`9c163d82a20d8ba9656b1e41`；证据：`fe08b74d4164f6e85a7e1847`。

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

保存关系的展示摘要（`presentation_only=true`；不新增评级）：

完整 pattern：`/functional_chains/15/pattern`。展示截断：`true`；完整证据与原 pattern 保留。

| 保存字段 | 实际值 | 完整引用 |
| --- | --- | --- |
| scoped_source_supported | true | /functional_chains/15/pattern/scoped_source_supported |

**nested_source_regions**：`/functional_chains/15/pattern/nested_source_regions`；展示截断：`false`。

```json
[]
```

**sequences**：`/functional_chains/15/pattern/sequences`；展示截断：`true`。

```json
{
  "control": {
    "all_function_paths_or_effects_accounted": false,
    "future_or_callback_activation_proven": false,
    "region_kind": "function_item",
    "role": "control",
    "assignment_attempts": [],
    "call_result_guard_source_links": [],
    "conditions": [
      {
        "source_fact_refs": [
          "/functional_chains/15/source_facts/95"
        ],
        "id": "2928b890106a9da4612f7a8b",
        "kind": "source_guard_and_abrupt_branch",
        "origin": "source-derived",
        "role": "control",
        "runtime_predicate_proven": false,
        "branch_context": [
          {
            "activation_proven": false,
            "kind": "match_arm",
            "location": {
              "file": "crates/winwincode-worker/src/lib.rs",
              "line": 771,
              "column": 13,
              "end_line": 827,
              "start_byte": 30873,
              "end_byte": 33570,
              "full_location_ref": "/functional_chains/15/pattern/sequences/control/conditions/0/branch_context/0/location"
            }
          }
        ],
        "branches": [
          {
            "branch": "then",
            "branch_all_paths_abrupt_proven": true,
            "abrupt_source_expressions": [
              {
                "kind": "return_expression",
                "runtime_completion_proven": false,
                "location": {
                  "file": "crates/winwincode-worker/src/lib.rs",
                  "line": 777,
                  "column": 21,
                  "end_line": 777,
                  "start_byte": 31149,
                  "end_byte": 31210,
                  "full_location_ref": "/functional_chains/15/pattern/sequences/control/conditions/0/branches/0/abrupt_source_expressions/0/location"
                },
                "returned_expression": {
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/kind"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/location"
                  },
                  "operand": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/0/branches/0/abrupt_source_expressions/0/returned_expression/operand"
                  }
                }
              }
            ],
            "call_ids": [
              "04d57d6ac85d5335aa44b89e"
            ]
          }
        ],
        "condition": {
          "kind": "try_expression",
          "location": {
            "file": "crates/winwincode-worker/src/lib.rs",
            "line": 772,
            "column": 20,
            "end_line": 775,
            "start_byte": 30944,
            "end_byte": 31110,
            "full_location_ref": "/functional_chains/15/pattern/sequences/control/conditions/0/condition/location"
          },
          "operand": {
            "call_effects_or_result_proven": false,
            "callee_source": "self\n                    .workspaces\n                    .is_observation_model_exchange(&chunk.model_exchange_id)\n                    .map_err",
            "kind": "call_expression",
            "arguments": [
              {
                "kind": "closure_expression",
                "runtime_value_proven": false,
                "source": "|_| workspace_error()",
                "source_truncated": false,
                "location": {
                  "file": "crates/winwincode-worker/src/lib.rs",
                  "line": 775,
                  "column": 30,
                  "end_line": 775,
                  "start_byte": 31087,
                  "end_byte": 31108,
                  "full_location_ref": "/functional_chains/15/pattern/sequences/control/conditions/0/condition/operand/arguments/0/location"
                }
              }
            ],
            "callee_expression": {
              "current_referent_value_proven": false,
              "kind": "field_expression",
              "member": "map_err",
              "location": {
                "file": "crates/winwincode-worker/src/lib.rs",
                "line": 772,
                "column": 20,
                "end_line": 775,
                "start_byte": 30944,
                "end_byte": 31086,
                "full_location_ref": "/functional_chains/15/pattern/sequences/control/conditions/0/condition/operand/callee_expression/location"
              },
              "member_location": {
                "file": "crates/winwincode-worker/src/lib.rs",
                "line": 775,
                "column": 22,
                "end_line": 775,
                "start_byte": 31079,
                "end_byte": 31086,
                "full_location_ref": "/functional_chains/15/pattern/sequences/control/conditions/0/condition/operand/callee_expression/member_location"
              },
              "object": {
                "call_effects_or_result_proven": false,
                "callee_source": "self\n                    .workspaces\n                    .is_observation_model_exchange",
                "kind": "call_expression",
                "arguments": [
                  {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/0/condition/operand/callee_expression/object/arguments/0"
                  }
                ],
                "callee_expression": {
                  "current_referent_value_proven": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/0/condition/operand/callee_expression/object/callee_expression/current_referent_value_proven"
                  },
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/0/condition/operand/callee_expression/object/callee_expression/kind"
                  },
                  "member": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/0/condition/operand/callee_expression/object/callee_expression/member"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/0/condition/operand/callee_expression/object/callee_expression/location"
                  },
                  "member_location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/0/condition/operand/callee_expression/object/callee_expression/member_location"
                  },
                  "object": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/0/condition/operand/callee_expression/object/callee_expression/object"
                  }
                },
                "location": {
                  "file": "crates/winwincode-worker/src/lib.rs",
                  "line": 772,
                  "column": 20,
                  "end_line": 774,
                  "start_byte": 30944,
                  "end_byte": 31057,
                  "full_location_ref": "/functional_chains/15/pattern/sequences/control/conditions/0/condition/operand/callee_expression/object/location"
                }
              }
            },
            "location": {
              "file": "crates/winwincode-worker/src/lib.rs",
              "line": 772,
              "column": 20,
              "end_line": 775,
              "start_byte": 30944,
              "end_byte": 31109,
              "full_location_ref": "/functional_chains/15/pattern/sequences/control/conditions/0/condition/operand/location"
            }
          }
        },
        "location": {
          "file": "crates/winwincode-worker/src/lib.rs",
          "line": 772,
          "column": 17,
          "end_line": 778,
          "start_byte": 30941,
          "end_byte": 31229,
          "full_location_ref": "/functional_chains/15/pattern/sequences/control/conditions/0/location"
        }
      },
      {
        "source_fact_refs": [
          "/functional_chains/15/source_facts/98"
        ],
        "id": "d0402621c6aee7eb9ae48517",
        "kind": "source_guard_and_abrupt_branch",
        "origin": "source-derived",
        "role": "control",
        "runtime_predicate_proven": false,
        "branch_context": [
          {
            "activation_proven": false,
            "kind": "match_arm",
            "location": {
              "file": "crates/winwincode-worker/src/lib.rs",
              "line": 771,
              "column": 13,
              "end_line": 827,
              "start_byte": 30873,
              "end_byte": 33570,
              "full_location_ref": "/functional_chains/15/pattern/sequences/control/conditions/1/branch_context/0/location"
            }
          }
        ],
        "branches": [
          {
            "branch": "then",
            "branch_all_paths_abrupt_proven": false,
            "abrupt_source_expressions": [],
            "call_ids": []
          }
        ],
        "condition": {
          "kind": "binary_expression",
          "operator": "&&",
          "runtime_predicate_or_assignment_proven": false,
          "location": {
            "file": "crates/winwincode-worker/src/lib.rs",
            "line": 799,
            "column": 20,
            "end_line": 801,
            "start_byte": 32289,
            "end_byte": 32467,
            "full_location_ref": "/functional_chains/15/pattern/sequences/control/conditions/1/condition/location"
          },
          "operands": [
            {
              "kind": "binary_expression",
              "operator": "&&",
              "runtime_predicate_or_assignment_proven": false,
              "location": {
                "file": "crates/winwincode-worker/src/lib.rs",
                "line": 799,
                "column": 20,
                "end_line": 800,
                "start_byte": 32289,
                "end_byte": 32392,
                "full_location_ref": "/functional_chains/15/pattern/sequences/control/conditions/1/condition/operands/0/location"
              },
              "operands": [
                {
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/1/condition/operands/0/operands/0/kind"
                  },
                  "operator": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/1/condition/operands/0/operands/0/operator"
                  },
                  "runtime_predicate_or_assignment_proven": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/1/condition/operands/0/operands/0/runtime_predicate_or_assignment_proven"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/1/condition/operands/0/operands/0/location"
                  },
                  "operands": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/1/condition/operands/0/operands/0/operands"
                  }
                },
                {
                  "call_effects_or_result_proven": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/1/condition/operands/0/operands/1/call_effects_or_result_proven"
                  },
                  "callee_source": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/1/condition/operands/0/operands/1/callee_source"
                  },
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/1/condition/operands/0/operands/1/kind"
                  },
                  "arguments": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/1/condition/operands/0/operands/1/arguments"
                  },
                  "callee_expression": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/1/condition/operands/0/operands/1/callee_expression"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/1/condition/operands/0/operands/1/location"
                  }
                }
              ]
            },
            {
              "call_effects_or_result_proven": false,
              "callee_source": "std::env::var_os(\"WWC_WORKER_POLL_DEBUG\").is_some",
              "kind": "call_expression",
              "arguments": [],
              "callee_expression": {
                "current_referent_value_proven": false,
                "kind": "field_expression",
                "member": "is_some",
                "location": {
                  "file": "crates/winwincode-worker/src/lib.rs",
                  "line": 801,
                  "column": 24,
                  "end_line": 801,
                  "start_byte": 32416,
                  "end_byte": 32465,
                  "full_location_ref": "/functional_chains/15/pattern/sequences/control/conditions/1/condition/operands/1/callee_expression/location"
                },
                "member_location": {
                  "file": "crates/winwincode-worker/src/lib.rs",
                  "line": 801,
                  "column": 66,
                  "end_line": 801,
                  "start_byte": 32458,
                  "end_byte": 32465,
                  "full_location_ref": "/functional_chains/15/pattern/sequences/control/conditions/1/condition/operands/1/callee_expression/member_location"
                },
                "object": {
                  "call_effects_or_result_proven": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/1/condition/operands/1/callee_expression/object/call_effects_or_result_proven"
                  },
                  "callee_source": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/1/condition/operands/1/callee_expression/object/callee_source"
                  },
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/1/condition/operands/1/callee_expression/object/kind"
                  },
                  "arguments": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/1/condition/operands/1/callee_expression/object/arguments"
                  },
                  "callee_expression": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/1/condition/operands/1/callee_expression/object/callee_expression"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/1/condition/operands/1/callee_expression/object/location"
                  }
                }
              },
              "location": {
                "file": "crates/winwincode-worker/src/lib.rs",
                "line": 801,
                "column": 24,
                "end_line": 801,
                "start_byte": 32416,
                "end_byte": 32467,
                "full_location_ref": "/functional_chains/15/pattern/sequences/control/conditions/1/condition/operands/1/location"
              }
            }
          ]
        },
        "location": {
          "file": "crates/winwincode-worker/src/lib.rs",
          "line": 799,
          "column": 17,
          "end_line": 807,
          "start_byte": 32286,
          "end_byte": 32694,
          "full_location_ref": "/functional_chains/15/pattern/sequences/control/conditions/1/location"
        }
      },
      {
        "source_fact_refs": [
          "/functional_chains/15/source_facts/99"
        ],
        "id": "d755772940ae398ebc8c04ce",
        "kind": "source_guard_and_abrupt_branch",
        "origin": "source-derived",
        "role": "control",
        "runtime_predicate_proven": false,
        "branch_context": [
          {
            "activation_proven": false,
            "kind": "match_arm",
            "location": {
              "file": "crates/winwincode-worker/src/lib.rs",
              "line": 771,
              "column": 13,
              "end_line": 827,
              "start_byte": 30873,
              "end_byte": 33570,
              "full_location_ref": "/functional_chains/15/pattern/sequences/control/conditions/2/branch_context/0/location"
            }
          }
        ],
        "branches": [
          {
            "branch": "then",
            "branch_all_paths_abrupt_proven": false,
            "abrupt_source_expressions": [],
            "call_ids": []
          }
        ],
        "condition": {
          "kind": "binary_expression",
          "operator": "&&",
          "runtime_predicate_or_assignment_proven": false,
          "location": {
            "file": "crates/winwincode-worker/src/lib.rs",
            "line": 808,
            "column": 20,
            "end_line": 809,
            "start_byte": 32714,
            "end_byte": 32845,
            "full_location_ref": "/functional_chains/15/pattern/sequences/control/conditions/2/condition/location"
          },
          "operands": [
            {
              "call_effects_or_result_proven": false,
              "callee_source": "self.flush_durable_execution_deliveries().await.is_err",
              "kind": "call_expression",
              "arguments": [],
              "callee_expression": {
                "current_referent_value_proven": false,
                "kind": "field_expression",
                "member": "is_err",
                "location": {
                  "file": "crates/winwincode-worker/src/lib.rs",
                  "line": 808,
                  "column": 20,
                  "end_line": 808,
                  "start_byte": 32714,
                  "end_byte": 32768,
                  "full_location_ref": "/functional_chains/15/pattern/sequences/control/conditions/2/condition/operands/0/callee_expression/location"
                },
                "member_location": {
                  "file": "crates/winwincode-worker/src/lib.rs",
                  "line": 808,
                  "column": 68,
                  "end_line": 808,
                  "start_byte": 32762,
                  "end_byte": 32768,
                  "full_location_ref": "/functional_chains/15/pattern/sequences/control/conditions/2/condition/operands/0/callee_expression/member_location"
                },
                "object": {
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/2/condition/operands/0/callee_expression/object/kind"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/2/condition/operands/0/callee_expression/object/location"
                  },
                  "operand": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/2/condition/operands/0/callee_expression/object/operand"
                  }
                }
              },
              "location": {
                "file": "crates/winwincode-worker/src/lib.rs",
                "line": 808,
                "column": 20,
                "end_line": 808,
                "start_byte": 32714,
                "end_byte": 32770,
                "full_location_ref": "/functional_chains/15/pattern/sequences/control/conditions/2/condition/operands/0/location"
              }
            },
            {
              "call_effects_or_result_proven": false,
              "callee_source": "std::env::var_os(\"WWC_WORKER_POLL_DEBUG\").is_some",
              "kind": "call_expression",
              "arguments": [],
              "callee_expression": {
                "current_referent_value_proven": false,
                "kind": "field_expression",
                "member": "is_some",
                "location": {
                  "file": "crates/winwincode-worker/src/lib.rs",
                  "line": 809,
                  "column": 24,
                  "end_line": 809,
                  "start_byte": 32794,
                  "end_byte": 32843,
                  "full_location_ref": "/functional_chains/15/pattern/sequences/control/conditions/2/condition/operands/1/callee_expression/location"
                },
                "member_location": {
                  "file": "crates/winwincode-worker/src/lib.rs",
                  "line": 809,
                  "column": 66,
                  "end_line": 809,
                  "start_byte": 32836,
                  "end_byte": 32843,
                  "full_location_ref": "/functional_chains/15/pattern/sequences/control/conditions/2/condition/operands/1/callee_expression/member_location"
                },
                "object": {
                  "call_effects_or_result_proven": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/2/condition/operands/1/callee_expression/object/call_effects_or_result_proven"
                  },
                  "callee_source": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/2/condition/operands/1/callee_expression/object/callee_source"
                  },
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/2/condition/operands/1/callee_expression/object/kind"
                  },
                  "arguments": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/2/condition/operands/1/callee_expression/object/arguments"
                  },
                  "callee_expression": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/2/condition/operands/1/callee_expression/object/callee_expression"
                  },
                  "location": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/2/condition/operands/1/callee_expression/object/location"
                  }
                }
              },
              "location": {
                "file": "crates/winwincode-worker/src/lib.rs",
                "line": 809,
                "column": 24,
                "end_line": 809,
                "start_byte": 32794,
                "end_byte": 32845,
                "full_location_ref": "/functional_chains/15/pattern/sequences/control/conditions/2/condition/operands/1/location"
              }
            }
          ]
        },
        "location": {
          "file": "crates/winwincode-worker/src/lib.rs",
          "line": 808,
          "column": 17,
          "end_line": 816,
          "start_byte": 32711,
          "end_byte": 33117,
          "full_location_ref": "/functional_chains/15/pattern/sequences/control/conditions/2/location"
        }
      },
      {
        "source_fact_refs": [
          "/functional_chains/15/source_facts/100"
        ],
        "id": "c9d814b0c1d58f91b71a561d",
        "kind": "source_guard_and_abrupt_branch",
        "origin": "source-derived",
        "role": "control",
        "runtime_predicate_proven": false,
        "branch_context": [
          {
            "activation_proven": false,
            "kind": "match_arm",
            "location": {
              "file": "crates/winwincode-worker/src/lib.rs",
              "line": 771,
              "column": 13,
              "end_line": 827,
              "start_byte": 30873,
              "end_byte": 33570,
              "full_location_ref": "/functional_chains/15/pattern/sequences/control/conditions/3/branch_context/0/location"
            }
          }
        ],
        "branches": [
          {
            "branch": "then",
            "branch_all_paths_abrupt_proven": false,
            "abrupt_source_expressions": [],
            "call_ids": []
          }
        ],
        "condition": {
          "kind": "binary_expression",
          "operator": "&&",
          "runtime_predicate_or_assignment_proven": false,
          "location": {
            "file": "crates/winwincode-worker/src/lib.rs",
            "line": 817,
            "column": 20,
            "end_line": 818,
            "start_byte": 33137,
            "end_byte": 33264,
            "full_location_ref": "/functional_chains/15/pattern/sequences/control/conditions/3/condition/location"
          },
          "operands": {
            "shown_items": [
              {
                "call_effects_or_result_proven": false,
                "callee_source": "self.flush_codex_execution_messages().await.is_err",
                "kind": "call_expression",
                "arguments": [],
                "callee_expression": {
                  "current_referent_value_proven": false,
                  "kind": "field_expression",
                  "member": "is_err",
                  "remaining_fields_ref": "/functional_chains/15/pattern/sequences/control/conditions/3/condition/operands/0/callee_expression"
                },
                "remaining_fields_ref": "/functional_chains/15/pattern/sequences/control/conditions/3/condition/operands/0"
              }
            ],
            "shown_count": 1,
            "total_count": 2,
            "truncated": true,
            "full_value_ref": "/functional_chains/15/pattern/sequences/control/conditions/3/condition/operands"
          }
        },
        "remaining_fields_ref": "/functional_chains/15/pattern/sequences/control/conditions/3"
      }
    ],
    "remaining_fields_ref": "/functional_chains/15/pattern/sequences/control"
  },
  "remaining_fields_ref": "/functional_chains/15/pattern/sequences"
}
```

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

### wwc-report-workrun-finite-selection

类型：`rust_finite_state_selection`；源码关系评估：`scoped_source_relations_supported`。

保存发现：`ca3bbdf71c845333fe640b2e`；证据：`ddcf0a91c7456da988fdbe75`。

- `aggregate_selector`：`crates/winwincode-delivery/src/application/workrun.rs` / `WorkRunAggregate.start_next`。
- `item_selector`：`crates/winwincode-delivery/src/application/workrun.rs` / `WorkRunAggregate.start_item`。
- `selector`：`crates/winwincode-delivery/src/application/workrun.rs` / `start_next_work_run`。
- `runnable`：`crates/winwincode-delivery/src/application/workrun.rs` / `work_item_is_runnable`。
- `effective_state`：`crates/winwincode-delivery/src/application/workrun.rs` / `effective_work_item_state`。
- `validator`：`crates/winwincode-delivery/src/application/workrun.rs` / `WorkRunAggregate.validate`。

保存关系的展示摘要（`presentation_only=true`；不新增评级）：

完整 pattern：`/functional_chains/16/pattern`。展示截断：`true`；完整证据与原 pattern 保留。

**rows**：`/functional_chains/16/pattern/finite_effective_state_relation/rows`；显示 8/8 行；展示截断：`false`。

| effective_state | input_state | runnable | source_quantifiers | 完整行引用 |
| --- | --- | --- | --- | --- |
| WorkItemState::Done | WorkItemState::Done | false | {"source_quantifier_1":false} | /functional_chains/16/pattern/finite_effective_state_relation/rows/0 |
| WorkItemState::Done | WorkItemState::Done | false | {"source_quantifier_1":true} | /functional_chains/16/pattern/finite_effective_state_relation/rows/1 |
| WorkItemState::Ready | WorkItemState::Ready | true | {"source_quantifier_1":false} | /functional_chains/16/pattern/finite_effective_state_relation/rows/2 |
| WorkItemState::WaitingDependency | WorkItemState::Ready | false | {"source_quantifier_1":true} | /functional_chains/16/pattern/finite_effective_state_relation/rows/3 |
| WorkItemState::Ready | WorkItemState::WaitingDependency | true | {"source_quantifier_1":false} | /functional_chains/16/pattern/finite_effective_state_relation/rows/4 |
| WorkItemState::WaitingDependency | WorkItemState::WaitingDependency | false | {"source_quantifier_1":true} | /functional_chains/16/pattern/finite_effective_state_relation/rows/5 |
| &lt;other value of this state enum&gt; | &lt;other value of this state enum&gt; | false | {"source_quantifier_1":false} | /functional_chains/16/pattern/finite_effective_state_relation/rows/6 |
| &lt;other value of this state enum&gt; | &lt;other value of this state enum&gt; | false | {"source_quantifier_1":true} | /functional_chains/16/pattern/finite_effective_state_relation/rows/7 |

**non_runnable_table_rows**：`/functional_chains/16/pattern/finite_source_countercases/non_runnable_table_rows`；显示 6/6 行；展示截断：`false`。

| effective_state | input_state | runnable | source_quantifiers | 完整行引用 |
| --- | --- | --- | --- | --- |
| WorkItemState::Done | WorkItemState::Done | false | {"source_quantifier_1":false} | /functional_chains/16/pattern/finite_source_countercases/non_runnable_table_rows/0 |
| WorkItemState::Done | WorkItemState::Done | false | {"source_quantifier_1":true} | /functional_chains/16/pattern/finite_source_countercases/non_runnable_table_rows/1 |
| WorkItemState::WaitingDependency | WorkItemState::Ready | false | {"source_quantifier_1":true} | /functional_chains/16/pattern/finite_source_countercases/non_runnable_table_rows/2 |
| WorkItemState::WaitingDependency | WorkItemState::WaitingDependency | false | {"source_quantifier_1":true} | /functional_chains/16/pattern/finite_source_countercases/non_runnable_table_rows/3 |
| &lt;other value of this state enum&gt; | &lt;other value of this state enum&gt; | false | {"source_quantifier_1":false} | /functional_chains/16/pattern/finite_source_countercases/non_runnable_table_rows/4 |
| &lt;other value of this state enum&gt; | &lt;other value of this state enum&gt; | false | {"source_quantifier_1":true} | /functional_chains/16/pattern/finite_source_countercases/non_runnable_table_rows/5 |

**runnable_table_rows**：`/functional_chains/16/pattern/finite_source_countercases/runnable_table_rows`；显示 2/2 行；展示截断：`false`。

| effective_state | input_state | runnable | source_quantifiers | 完整行引用 |
| --- | --- | --- | --- | --- |
| WorkItemState::Ready | WorkItemState::Ready | true | {"source_quantifier_1":false} | /functional_chains/16/pattern/finite_source_countercases/runnable_table_rows/0 |
| WorkItemState::Ready | WorkItemState::WaitingDependency | true | {"source_quantifier_1":false} | /functional_chains/16/pattern/finite_source_countercases/runnable_table_rows/1 |

| 保存字段 | 实际值 | 完整引用 |
| --- | --- | --- |
| all_active_states_or_attempts_proven | false | /functional_chains/16/pattern/all_active_states_or_attempts_proven |
| graph_calls_repaired_or_promoted | false | /functional_chains/16/pattern/graph_calls_repaired_or_promoted |
| runtime_schedule_or_termination_proven | false | /functional_chains/16/pattern/runtime_schedule_or_termination_proven |
| scoped_source_supported | true | /functional_chains/16/pattern/scoped_source_supported |
| state_table_dependency_quantifier_linked | true | /functional_chains/16/pattern/state_table_dependency_quantifier_linked |
| trusted_model | rust-finite-iterator-enum-source-v1 | /functional_chains/16/pattern/trusted_model |
| version | captured-rust-finite-state-relations-1 | /functional_chains/16/pattern/version |
| whole_domain_state_machine_closed | false | /functional_chains/16/pattern/whole_domain_state_machine_closed |

**boundaries**：`/functional_chains/16/pattern/boundaries`；展示截断：`false`。

```json
[
  "source-mentioned enum alternatives and a symbolic complement are interpreted; no complete enum declaration or arbitrary macro expansion is inferred",
  "quantifiers describe current captured predicates; concrete item records, dependency truth and actual active runs are unknown",
  "selection does not prove persistence, scheduling fairness, concurrency isolation, all state transitions or every attempt identity"
]
```

**dependency_blocker_relation**：`/functional_chains/16/pattern/dependency_blocker_relation`；展示截断：`false`。

```json
{
  "supported": true,
  "relations": [
    {
      "source_fact_refs": [
        "/functional_chains/16/source_facts/113"
      ],
      "actual_dependencies_or_reachability_evaluated": false,
      "empty_dependency_collection_result": false,
      "finite_state_component": "captured-rust-finite-state-relations-1",
      "id": "45b1c2a354c3b89a85844a5c",
      "kind": "rust_finite_dependency_blocker_relation",
      "origin": "source-derived",
      "quantifier": "exists dependency for which no equal-identity candidate has the captured required state",
      "role": "effective_state",
      "candidate_collection": {
        "kind": "name",
        "name": "items",
        "span": [
          23876,
          23881
        ]
      },
      "dependency_collection": {
        "field": "depends_on",
        "kind": "field",
        "span": [
          23825,
          23840
        ],
        "value": {
          "kind": "name",
          "name": "item",
          "span": [
            23825,
            23829
          ]
        }
      },
      "identity_comparison": {
        "candidate_key": [
          "candidate",
          "id"
        ],
        "dependency_value": [
          "dependency"
        ]
      },
      "location": {
        "file": "crates/winwincode-delivery/src/application/workrun.rs",
        "line": 648,
        "column": 10,
        "end_line": 652,
        "start_byte": 23825,
        "end_byte": 24008,
        "full_location_ref": "/functional_chains/16/pattern/dependency_blocker_relation/relations/0/location"
      },
      "required_candidate_state_comparison": {
        "accepted_state": [
          "WorkItemState",
          "Done"
        ],
        "candidate_state": [
          "candidate",
          "state"
        ]
      }
    }
  ]
}
```

**expression_budget**：`/functional_chains/16/pattern/expression_budget`；展示截断：`false`。

```json
{
  "incomplete": false,
  "limit": 131072,
  "operations": 196
}
```

**finite_effective_state_relation**：`/functional_chains/16/pattern/finite_effective_state_relation`；展示截断：`true`。

```json
{
  "fact_id": "8330c9b5101206bc3915770b",
  "full_enum_enumeration": false,
  "runnable_equals": "WorkItemState::Ready",
  "supported": true,
  "rows": {
    "presentation_table_ref": "/source_relation_index/entries/16/presentation/tables/0",
    "full_value_ref": "/functional_chains/16/pattern/finite_effective_state_relation/rows",
    "total_rows": 8,
    "presentation_only": true
  },
  "state_field_path": [
    "item",
    "state"
  ],
  "symbolic_quantifiers": [
    {
      "name": "source_quantifier_1",
      "expression": {
        "kind": "method",
        "method": "any",
        "arguments": [
          {
            "kind": "closure",
            "simple_parameters": true,
            "body": {
              "kind": "block",
              "span": [
                23865,
                24007
              ],
              "statements": [
                {
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/16/pattern/finite_effective_state_relation/symbolic_quantifiers/0/expression/arguments/0/body/statements/0/kind"
                  },
                  "operator": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/16/pattern/finite_effective_state_relation/symbolic_quantifiers/0/expression/arguments/0/body/statements/0/operator"
                  },
                  "span": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/16/pattern/finite_effective_state_relation/symbolic_quantifiers/0/expression/arguments/0/body/statements/0/span"
                  },
                  "value": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/functional_chains/16/pattern/finite_effective_state_relation/symbolic_quantifiers/0/expression/arguments/0/body/statements/0/value"
                  }
                }
              ]
            },
            "parameters": [
              "dependency"
            ],
            "span": [
              23852,
              24007
            ]
          }
        ],
        "receiver": {
          "kind": "method",
          "method": "iter",
          "arguments": [],
          "receiver": {
            "field": "depends_on",
            "kind": "field",
            "span": [
              23825,
              23840
            ],
            "value": {
              "kind": "name",
              "name": "item",
              "span": [
                23825,
                23829
              ]
            }
          },
          "span": [
            23825,
            23847
          ]
        },
        "span": [
          23825,
          24008
        ]
      }
    }
  ]
}
```

**finite_source_countercases**：`/functional_chains/16/pattern/finite_source_countercases`；展示截断：`false`。

```json
{
  "countercases_are_symbolic_source_conditions_not_observed_runtime_records": true,
  "non_runnable_table_rows": {
    "presentation_table_ref": "/source_relation_index/entries/16/presentation/tables/1",
    "full_value_ref": "/functional_chains/16/pattern/finite_source_countercases/non_runnable_table_rows",
    "total_rows": 6,
    "presentation_only": true
  },
  "runnable_table_rows": {
    "presentation_table_ref": "/source_relation_index/entries/16/presentation/tables/2",
    "full_value_ref": "/functional_chains/16/pattern/finite_source_countercases/runnable_table_rows",
    "total_rows": 2,
    "presentation_only": true
  },
  "selection_active_members": [
    [
      "WorkRunState",
      "Leased"
    ],
    [
      "WorkRunState",
      "Running"
    ],
    [
      "WorkRunState",
      "CandidateReady"
    ]
  ],
  "validator_predicates_remain_distinct": [
    {
      "kind": "enum_membership",
      "macro_expanded": false,
      "macro_resolution": "conditional_standard_matches_macro_model",
      "members": [
        [
          "WorkRunState",
          "Leased"
        ],
        [
          "WorkRunState",
          "Running"
        ]
      ],
      "span": [
        11274,
        11339
      ],
      "value": {
        "field": "state",
        "kind": "field",
        "value": {
          "kind": "name",
          "name": "run"
        }
      }
    }
  ]
}
```

**iterator_relation_fact_ids**：`/functional_chains/16/pattern/iterator_relation_fact_ids`；展示截断：`false`。

```json
{
  "aggregate_selector": [
    "839f94aa44d15f35745fa893"
  ],
  "effective_state": [
    "7cb680b6c7fdb6ef7a54b25d",
    "f635d014c13a99b93e9a94f1"
  ],
  "item_selector": [
    "8466a4679c5937f40ea09cf9",
    "5c88837d0461c3839b9493b9"
  ],
  "runnable": [],
  "selector": [
    "0fd47d2c2d1202e8253f9fcf"
  ]
}
```

**necessary_gaps**：`/functional_chains/16/pattern/necessary_gaps`；展示截断：`false`。

```json
[]
```

**persisted_selection_recheck_relation**：`/functional_chains/16/pattern/persisted_selection_recheck_relation`；展示截断：`false`。

```json
{
  "active_collection_computed_from_persisted_runs": true,
  "all_enum_states_or_attempts_proven": false,
  "fact_id": "cbbc904fc499d1f81bc46305",
  "supported": true,
  "active_members": [
    [
      "WorkRunState",
      "Leased"
    ],
    [
      "WorkRunState",
      "Running"
    ],
    [
      "WorkRunState",
      "CandidateReady"
    ]
  ],
  "checks": {
    "active_collection_passed_to_selector_and_selected_id_rechecked": true,
    "active_exclusion_key_equals_exact_find_requested_id": true,
    "aggregate_validation_collect_select_recheck_source_order": true,
    "both_selected_entries_have_fallible_validation_prefix": true,
    "runnable_predicate_in_both_find_conjunctions": true,
    "same_active_state_alternatives": true,
    "same_persisted_run_collection": true,
    "same_projected_item_identity_field": true,
    "same_state_field_on_actual_filter_and_exclusion_elements": true,
    "selected_result_and_active_membership_share_exact_item_key": true
  },
  "find_predicate_source_facts": {
    "item_selector": "8466a4679c5937f40ea09cf9",
    "selector": "0fd47d2c2d1202e8253f9fcf"
  },
  "transfer": {
    "active_key_matches_contains_selected_item_key": true,
    "active_local_binding": "active",
    "active_struct_field": "active_work_item_ids",
    "same_active_struct_field": true,
    "same_item_collection_argument": true,
    "same_selected_result_identity": true,
    "same_selected_result_root": true,
    "selected_id_matches_exact_item_key": true,
    "selected_local_binding": "start",
    "source_statement_pipeline_order_closed": true,
    "membership_argument": [
      [
        "item",
        "id"
      ]
    ],
    "membership_receiver": [
      "input",
      "active_work_item_ids"
    ],
    "selected_recheck_arguments": [
      [
        "start",
        "work_item",
        "id"
      ]
    ],
    "selector_return_identity": {
      "closed_under_plain_selected_clone_source_model": true,
      "selected_binding": "item",
      "contains_selected_key": [
        "item",
        "id"
      ],
      "identity_field_assignments": [],
      "rechecked_result_key": [
        "start",
        "work_item",
        "id"
      ],
      "resolved_selected_path": [
        "item"
      ],
      "returned_record_field_path": [
        "started"
      ]
    }
  },
  "validation_prefixes": [
    {
      "source_fact_refs": [
        "/functional_chains/16/source_facts/114"
      ],
      "finite_state_component": "captured-rust-finite-state-relations-1",
      "id": "a2c9442ed3f95c388e123dd4",
      "kind": "rust_finite_selection_validation_prefix",
      "normal_continuation_requires_ok": true,
      "origin": "source-derived",
      "role": "aggregate_selector",
      "selected_validator_symbol": "WorkRunAggregate.validate",
      "validator_entire_semantics_proven": false,
      "first_statement": {
        "kind": "try",
        "span": [
          14655,
          14671
        ],
        "value": {
          "kind": "method",
          "method": "validate",
          "arguments": [],
          "receiver": {
            "kind": "name",
            "name": "self",
            "span": [
              14655,
              14659
            ]
          },
          "span": [
            14655,
            14670
          ]
        }
      },
      "location": {
        "file": "crates/winwincode-delivery/src/application/workrun.rs",
        "line": 392,
        "column": 9,
        "end_line": 392,
        "start_byte": 14655,
        "end_byte": 14671,
        "full_location_ref": "/functional_chains/16/pattern/persisted_selection_recheck_relation/validation_prefixes/0/location"
      }
    },
    {
      "source_fact_refs": [
        "/functional_chains/16/source_facts/115"
      ],
      "finite_state_component": "captured-rust-finite-state-relations-1",
      "id": "0f66367ae71d1bc4d5c7e477",
      "kind": "rust_finite_selection_validation_prefix",
      "normal_continuation_requires_ok": true,
      "origin": "source-derived",
      "role": "item_selector",
      "selected_validator_symbol": "WorkRunAggregate.validate",
      "validator_entire_semantics_proven": false,
      "first_statement": {
        "kind": "try",
        "span": [
          15641,
          15657
        ],
        "value": {
          "kind": "method",
          "method": "validate",
          "arguments": [],
          "receiver": {
            "kind": "name",
            "name": "self",
            "span": [
              15641,
              15645
            ]
          },
          "span": [
            15641,
            15656
          ]
        }
      },
      "location": {
        "file": "crates/winwincode-delivery/src/application/workrun.rs",
        "line": 419,
        "column": 9,
        "end_line": 419,
        "start_byte": 15641,
        "end_byte": 15657,
        "full_location_ref": "/functional_chains/16/pattern/persisted_selection_recheck_relation/validation_prefixes/1/location"
      }
    }
  ]
}
```

**source_model_conditions**：`/functional_chains/16/pattern/source_model_conditions`；展示截断：`false`。

```json
[
  "selected normal source bodies are reached and their fallible prefixes return Ok",
  "captured plain matches! uses the standard Rust macro, not an external macro override",
  "captured Vec/slice iterator, HashSet membership, field equality and Clone obey their standard source contracts",
  "the recorded unique same-module helper source declarations are the invoked helpers; historical unresolved graph calls remain unchanged"
]
```

**validator_enum_predicate_source_fact_ids**：`/functional_chains/16/pattern/validator_enum_predicate_source_fact_ids`；展示截断：`false`。

```json
[
  "78ff0ca6a0316003ee4ea988"
]
```

自动关系类型：`{"captured_call_step": 94, "report_source_role": 6, "rust_finite_dependency_blocker_relation": 1, "rust_finite_effective_state_table": 1, "rust_finite_iterator_relation": 6, "rust_finite_selected_source_expression": 5, "rust_finite_selection_comparison": 1, "rust_finite_selection_validation_prefix": 2, "rust_finite_validator_enum_predicate_source": 1}`。

分析缺口：

```json
[]
```

条件与反证声明（单列为配置范围，不冒充源码证据）：

```json
{
  "applicability": {
    "conditions": [
      "Captured ordinary WorkRun selection bodies are reached normally; finite standard iterator, enum and matches source model applies."
    ],
    "counterexamples": [
      "No assertion that all WorkRun transitions, concurrent schedules or concrete stored records have been checked."
    ],
    "kind": "conditional"
  },
  "descriptive_counterexamples_are_computed_evidence": false,
  "origin": "policy-declared",
  "provenance": {
    "author_approved": false,
    "authority": "project-source-claim",
    "note": "Locators select captured source only; predicate and finite state values are derived from CST.",
    "source_doc": "reports/astra-baseline/WINWINCODE_ANALYSIS.md:60"
  }
}
```

### wwc-report-workrun-state-guards

类型：`state_guard_sequence`；源码关系评估：`scoped_source_relations_supported`。

保存发现：`0ff85dbba15ccb39ada4a775`；证据：`df35191414060797f247176d`。

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

保存关系的展示摘要（`presentation_only=true`；不新增评级）：

完整 pattern：`/functional_chains/17/pattern`。展示截断：`true`；完整证据与原 pattern 保留。

| 保存字段 | 实际值 | 完整引用 |
| --- | --- | --- |
| all_active_states_or_attempts_proven | false | /functional_chains/17/pattern/all_active_states_or_attempts_proven |
| scoped_source_supported | true | /functional_chains/17/pattern/scoped_source_supported |

**repeated_first_callee**：`/functional_chains/17/pattern/repeated_first_callee`；展示截断：`false`。

```json
{
  "rust:crates/winwincode-delivery/src/application/workrun#WorkRunAggregate.validate": [
    {
      "call_fact_id": "855b44866e7a3bb46e68f8fc",
      "role": "selection",
      "location": {
        "file": "crates/winwincode-delivery/src/application/workrun.rs",
        "line": 392,
        "column": 9,
        "end_line": 392,
        "start_byte": 14655,
        "end_byte": 14670,
        "full_location_ref": "/functional_chains/17/pattern/repeated_first_callee/rust:crates~1winwincode-delivery~1src~1application~1workrun#WorkRunAggregate.validate/0/location"
      }
    },
    {
      "call_fact_id": "00566343142225ed3672799c",
      "role": "start",
      "location": {
        "file": "crates/winwincode-delivery/src/application/workrun.rs",
        "line": 419,
        "column": 9,
        "end_line": 419,
        "start_byte": 15641,
        "end_byte": 15656,
        "full_location_ref": "/functional_chains/17/pattern/repeated_first_callee/rust:crates~1winwincode-delivery~1src~1application~1workrun#WorkRunAggregate.validate/1/location"
      }
    }
  ]
}
```

**selection_predicate_sources**：`/functional_chains/17/pattern/selection_predicate_sources`；展示截断：`true`。

```json
{
  "shown_items": [
    {
      "source_fact_refs": [
        "/functional_chains/17/source_facts/35"
      ],
      "callback_activation_proven": false,
      "id": "994002f9fe93f897c9751421",
      "kind": "state_selection_predicate_source",
      "macro_expansion_or_iterator_effects_proven": false,
      "nested_predicate_callable": true,
      "origin": "source-derived",
      "role": "selection",
      "expression": {
        "kind": "macro_invocation",
        "runtime_value_proven": false,
        "source": "matches!(\n                    run.state,\n                    WorkRunState::Leased | WorkRunState::Running | WorkRunState::CandidateReady\n                )",
        "source_truncated": false,
        "location": {
          "file": "crates/winwincode-delivery/src/application/workrun.rs",
          "line": 397,
          "column": 17,
          "end_line": 400,
          "start_byte": 14781,
          "end_byte": 14935,
          "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/0/expression/location"
        }
      },
      "location": {
        "file": "crates/winwincode-delivery/src/application/workrun.rs",
        "line": 397,
        "column": 17,
        "end_line": 400,
        "start_byte": 14781,
        "end_byte": 14935,
        "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/0/location"
      }
    },
    {
      "source_fact_refs": [
        "/functional_chains/17/source_facts/36"
      ],
      "callback_activation_proven": false,
      "id": "ec8ef37e5d8e429601d9fea2",
      "kind": "state_selection_predicate_source",
      "macro_expansion_or_iterator_effects_proven": false,
      "nested_predicate_callable": true,
      "origin": "source-derived",
      "role": "start",
      "expression": {
        "kind": "binary_expression",
        "operator": "&&",
        "runtime_predicate_or_assignment_proven": false,
        "location": {
          "file": "crates/winwincode-delivery/src/application/workrun.rs",
          "line": 424,
          "column": 17,
          "end_line": 434,
          "start_byte": 15765,
          "end_byte": 16261,
          "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/location"
        },
        "operands": [
          {
            "kind": "binary_expression",
            "operator": "&&",
            "runtime_predicate_or_assignment_proven": false,
            "location": {
              "file": "crates/winwincode-delivery/src/application/workrun.rs",
              "line": 424,
              "column": 17,
              "end_line": 425,
              "start_byte": 15765,
              "end_byte": 15843,
              "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/0/location"
            },
            "operands": [
              {
                "kind": "binary_expression",
                "operator": "==",
                "runtime_predicate_or_assignment_proven": false,
                "location": {
                  "file": "crates/winwincode-delivery/src/application/workrun.rs",
                  "line": 424,
                  "column": 17,
                  "end_line": 424,
                  "start_byte": 15765,
                  "end_byte": 15779,
                  "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/0/operands/0/location"
                },
                "operands": [
                  {
                    "kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/0/operands/0/operands/0/kind"
                    },
                    "location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/0/operands/0/operands/0/location"
                    },
                    "operand": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/0/operands/0/operands/0/operand"
                    }
                  },
                  {
                    "kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/0/operands/0/operands/1/kind"
                    },
                    "name": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/0/operands/0/operands/1/name"
                    },
                    "location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/0/operands/0/operands/1/location"
                    },
                    "reference": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/0/operands/0/operands/1/reference"
                    }
                  }
                ]
              },
              {
                "call_effects_or_result_proven": false,
                "callee_source": "work_item_is_runnable",
                "kind": "call_expression",
                "arguments": [
                  {
                    "kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/0/operands/1/arguments/0/kind"
                    },
                    "name": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/0/operands/1/arguments/0/name"
                    },
                    "location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/0/operands/1/arguments/0/location"
                    },
                    "reference": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/0/operands/1/arguments/0/reference"
                    }
                  },
                  {
                    "kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/0/operands/1/arguments/1/kind"
                    },
                    "location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/0/operands/1/arguments/1/location"
                    },
                    "operand": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/0/operands/1/arguments/1/operand"
                    }
                  }
                ],
                "callee_expression": {
                  "kind": "identifier",
                  "name": "work_item_is_runnable",
                  "location": {
                    "file": "crates/winwincode-delivery/src/application/workrun.rs",
                    "line": 425,
                    "column": 24,
                    "end_line": 425,
                    "start_byte": 15803,
                    "end_byte": 15824,
                    "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/0/operands/1/callee_expression/location"
                  },
                  "reference": {
                    "plain_binder_candidates": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/0/operands/1/callee_expression/reference/plain_binder_candidates"
                    },
                    "runtime_value_identity_proven": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/0/operands/1/callee_expression/reference/runtime_value_identity_proven"
                    },
                    "state": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/0/operands/1/callee_expression/reference/state"
                    },
                    "text": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/0/operands/1/callee_expression/reference/text"
                    },
                    "location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/0/operands/1/callee_expression/reference/location"
                    }
                  }
                },
                "location": {
                  "file": "crates/winwincode-delivery/src/application/workrun.rs",
                  "line": 425,
                  "column": 24,
                  "end_line": 425,
                  "start_byte": 15803,
                  "end_byte": 15843,
                  "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/0/operands/1/location"
                }
              }
            ]
          },
          {
            "kind": "unary_expression",
            "operator": "!",
            "runtime_predicate_or_assignment_proven": false,
            "location": {
              "file": "crates/winwincode-delivery/src/application/workrun.rs",
              "line": 426,
              "column": 24,
              "end_line": 434,
              "start_byte": 15867,
              "end_byte": 16261,
              "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/1/location"
            },
            "operands": [
              {
                "call_effects_or_result_proven": false,
                "callee_source": "self.runs.iter().any",
                "kind": "call_expression",
                "arguments": [
                  {
                    "kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/1/operands/0/arguments/0/kind"
                    },
                    "runtime_value_proven": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/1/operands/0/arguments/0/runtime_value_proven"
                    },
                    "source": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/1/operands/0/arguments/0/source"
                    },
                    "source_truncated": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/1/operands/0/arguments/0/source_truncated"
                    },
                    "location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/1/operands/0/arguments/0/location"
                    }
                  }
                ],
                "callee_expression": {
                  "current_referent_value_proven": false,
                  "kind": "field_expression",
                  "member": "any",
                  "location": {
                    "file": "crates/winwincode-delivery/src/application/workrun.rs",
                    "line": 426,
                    "column": 25,
                    "end_line": 426,
                    "start_byte": 15868,
                    "end_byte": 15888,
                    "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/1/operands/0/callee_expression/location"
                  },
                  "member_location": {
                    "file": "crates/winwincode-delivery/src/application/workrun.rs",
                    "line": 426,
                    "column": 42,
                    "end_line": 426,
                    "start_byte": 15885,
                    "end_byte": 15888,
                    "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/1/operands/0/callee_expression/member_location"
                  },
                  "object": {
                    "call_effects_or_result_proven": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/1/operands/0/callee_expression/object/call_effects_or_result_proven"
                    },
                    "callee_source": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/1/operands/0/callee_expression/object/callee_source"
                    },
                    "kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/1/operands/0/callee_expression/object/kind"
                    },
                    "arguments": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/1/operands/0/callee_expression/object/arguments"
                    },
                    "callee_expression": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/1/operands/0/callee_expression/object/callee_expression"
                    },
                    "location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/1/operands/0/callee_expression/object/location"
                    }
                  }
                },
                "location": {
                  "file": "crates/winwincode-delivery/src/application/workrun.rs",
                  "line": 426,
                  "column": 25,
                  "end_line": 434,
                  "start_byte": 15868,
                  "end_byte": 16261,
                  "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/expression/operands/1/operands/0/location"
                }
              }
            ]
          }
        ]
      },
      "location": {
        "file": "crates/winwincode-delivery/src/application/workrun.rs",
        "line": 424,
        "column": 17,
        "end_line": 434,
        "start_byte": 15765,
        "end_byte": 16261,
        "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/1/location"
      }
    },
    {
      "source_fact_refs": [
        "/functional_chains/17/source_facts/37"
      ],
      "callback_activation_proven": false,
      "id": "6ca4259e7a272dffc0ece22b",
      "kind": "state_selection_predicate_source",
      "macro_expansion_or_iterator_effects_proven": false,
      "nested_predicate_callable": true,
      "origin": "source-derived",
      "role": "start",
      "expression": {
        "kind": "binary_expression",
        "operator": "&&",
        "runtime_predicate_or_assignment_proven": false,
        "location": {
          "file": "crates/winwincode-delivery/src/application/workrun.rs",
          "line": 424,
          "column": 17,
          "end_line": 425,
          "start_byte": 15765,
          "end_byte": 15843,
          "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/2/expression/location"
        },
        "operands": [
          {
            "kind": "binary_expression",
            "operator": "==",
            "runtime_predicate_or_assignment_proven": false,
            "location": {
              "file": "crates/winwincode-delivery/src/application/workrun.rs",
              "line": 424,
              "column": 17,
              "end_line": 424,
              "start_byte": 15765,
              "end_byte": 15779,
              "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/2/expression/operands/0/location"
            },
            "operands": [
              {
                "kind": "reference_expression",
                "location": {
                  "file": "crates/winwincode-delivery/src/application/workrun.rs",
                  "line": 424,
                  "column": 17,
                  "end_line": 424,
                  "start_byte": 15765,
                  "end_byte": 15773,
                  "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/2/expression/operands/0/operands/0/location"
                },
                "operand": {
                  "current_referent_value_proven": false,
                  "kind": "field_expression",
                  "member": "id",
                  "location": {
                    "file": "crates/winwincode-delivery/src/application/workrun.rs",
                    "line": 424,
                    "column": 18,
                    "end_line": 424,
                    "start_byte": 15766,
                    "end_byte": 15773,
                    "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/2/expression/operands/0/operands/0/operand/location"
                  },
                  "member_location": {
                    "file": "crates/winwincode-delivery/src/application/workrun.rs",
                    "line": 424,
                    "column": 23,
                    "end_line": 424,
                    "start_byte": 15771,
                    "end_byte": 15773,
                    "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/2/expression/operands/0/operands/0/operand/member_location"
                  },
                  "object": {
                    "kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/2/expression/operands/0/operands/0/operand/object/kind"
                    },
                    "name": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/2/expression/operands/0/operands/0/operand/object/name"
                    },
                    "location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/2/expression/operands/0/operands/0/operand/object/location"
                    },
                    "reference": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/2/expression/operands/0/operands/0/operand/object/reference"
                    }
                  }
                }
              },
              {
                "kind": "identifier",
                "name": "id",
                "location": {
                  "file": "crates/winwincode-delivery/src/application/workrun.rs",
                  "line": 424,
                  "column": 29,
                  "end_line": 424,
                  "start_byte": 15777,
                  "end_byte": 15779,
                  "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/2/expression/operands/0/operands/1/location"
                },
                "reference": {
                  "plain_binder_candidates": 0,
                  "runtime_value_identity_proven": false,
                  "state": "captured_rust_reference",
                  "text": "id",
                  "location": {
                    "file": "crates/winwincode-delivery/src/application/workrun.rs",
                    "line": 424,
                    "column": 29,
                    "end_line": 424,
                    "start_byte": 15777,
                    "end_byte": 15779,
                    "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/2/expression/operands/0/operands/1/reference/location"
                  }
                }
              }
            ]
          },
          {
            "call_effects_or_result_proven": false,
            "callee_source": "work_item_is_runnable",
            "kind": "call_expression",
            "arguments": [
              {
                "kind": "identifier",
                "name": "item",
                "location": {
                  "file": "crates/winwincode-delivery/src/application/workrun.rs",
                  "line": 425,
                  "column": 46,
                  "end_line": 425,
                  "start_byte": 15825,
                  "end_byte": 15829,
                  "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/2/expression/operands/1/arguments/0/location"
                },
                "reference": {
                  "declaration_id": "f0afda8877672f5488de793fb0b492ffa43dd591c2d9ca89fba9b6f0c04be048",
                  "declaration_kind": "captured_rust_parameter",
                  "identity_scope": "plain captured binder syntax only",
                  "macro_namespace_complete": false,
                  "runtime_value_identity_proven": false,
                  "state": "captured_unique_rust_binder",
                  "binder_location": {
                    "file": "crates/winwincode-delivery/src/application/workrun.rs",
                    "line": 423,
                    "column": 20,
                    "end_line": 423,
                    "start_byte": 15741,
                    "end_byte": 15745,
                    "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/2/expression/operands/1/arguments/0/reference/binder_location"
                  },
                  "declaration_location": {
                    "file": "crates/winwincode-delivery/src/application/workrun.rs",
                    "line": 423,
                    "column": 20,
                    "end_line": 423,
                    "start_byte": 15741,
                    "end_byte": 15745,
                    "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/2/expression/operands/1/arguments/0/reference/declaration_location"
                  }
                }
              },
              {
                "kind": "reference_expression",
                "location": {
                  "file": "crates/winwincode-delivery/src/application/workrun.rs",
                  "line": 425,
                  "column": 52,
                  "end_line": 425,
                  "start_byte": 15831,
                  "end_byte": 15842,
                  "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/2/expression/operands/1/arguments/1/location"
                },
                "operand": {
                  "current_referent_value_proven": false,
                  "kind": "field_expression",
                  "member": "items",
                  "location": {
                    "file": "crates/winwincode-delivery/src/application/workrun.rs",
                    "line": 425,
                    "column": 53,
                    "end_line": 425,
                    "start_byte": 15832,
                    "end_byte": 15842,
                    "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/2/expression/operands/1/arguments/1/operand/location"
                  },
                  "member_location": {
                    "file": "crates/winwincode-delivery/src/application/workrun.rs",
                    "line": 425,
                    "column": 58,
                    "end_line": 425,
                    "start_byte": 15837,
                    "end_byte": 15842,
                    "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/2/expression/operands/1/arguments/1/operand/member_location"
                  },
                  "object": {
                    "kind": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/2/expression/operands/1/arguments/1/operand/object/kind"
                    },
                    "name": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/2/expression/operands/1/arguments/1/operand/object/name"
                    },
                    "location": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/2/expression/operands/1/arguments/1/operand/object/location"
                    },
                    "reference": {
                      "omitted_for_presentation": true,
                      "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/2/expression/operands/1/arguments/1/operand/object/reference"
                    }
                  }
                }
              }
            ],
            "callee_expression": {
              "kind": "identifier",
              "name": "work_item_is_runnable",
              "location": {
                "file": "crates/winwincode-delivery/src/application/workrun.rs",
                "line": 425,
                "column": 24,
                "end_line": 425,
                "start_byte": 15803,
                "end_byte": 15824,
                "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/2/expression/operands/1/callee_expression/location"
              },
              "reference": {
                "plain_binder_candidates": 0,
                "runtime_value_identity_proven": false,
                "state": "captured_rust_reference",
                "text": "work_item_is_runnable",
                "location": {
                  "file": "crates/winwincode-delivery/src/application/workrun.rs",
                  "line": 425,
                  "column": 24,
                  "end_line": 425,
                  "start_byte": 15803,
                  "end_byte": 15824,
                  "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/2/expression/operands/1/callee_expression/reference/location"
                }
              }
            },
            "location": {
              "file": "crates/winwincode-delivery/src/application/workrun.rs",
              "line": 425,
              "column": 24,
              "end_line": 425,
              "start_byte": 15803,
              "end_byte": 15843,
              "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/2/expression/operands/1/location"
            }
          }
        ]
      },
      "location": {
        "file": "crates/winwincode-delivery/src/application/workrun.rs",
        "line": 424,
        "column": 17,
        "end_line": 425,
        "start_byte": 15765,
        "end_byte": 15843,
        "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/2/location"
      }
    },
    {
      "source_fact_refs": [
        "/functional_chains/17/source_facts/38"
      ],
      "callback_activation_proven": false,
      "id": "3607a6eb703e43a0dd93ec10",
      "kind": "state_selection_predicate_source",
      "macro_expansion_or_iterator_effects_proven": false,
      "nested_predicate_callable": true,
      "origin": "source-derived",
      "role": "start",
      "expression": {
        "kind": "binary_expression",
        "operator": "==",
        "runtime_predicate_or_assignment_proven": false,
        "location": {
          "file": "crates/winwincode-delivery/src/application/workrun.rs",
          "line": 424,
          "column": 17,
          "end_line": 424,
          "start_byte": 15765,
          "end_byte": 15779,
          "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/3/expression/location"
        },
        "operands": {
          "shown_items": [
            {
              "kind": "reference_expression",
              "location": {
                "file": "crates/winwincode-delivery/src/application/workrun.rs",
                "line": 424,
                "column": 17,
                "end_line": 424,
                "start_byte": 15765,
                "end_byte": 15773,
                "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/3/expression/operands/0/location"
              },
              "operand": {
                "current_referent_value_proven": false,
                "kind": "field_expression",
                "member": "id",
                "location": {
                  "file": "crates/winwincode-delivery/src/application/workrun.rs",
                  "line": 424,
                  "column": 18,
                  "end_line": 424,
                  "start_byte": 15766,
                  "end_byte": 15773,
                  "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/3/expression/operands/0/operand/location"
                },
                "member_location": {
                  "file": "crates/winwincode-delivery/src/application/workrun.rs",
                  "line": 424,
                  "column": 23,
                  "end_line": 424,
                  "start_byte": 15771,
                  "end_byte": 15773,
                  "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/3/expression/operands/0/operand/member_location"
                },
                "object": {
                  "kind": "identifier",
                  "name": "item",
                  "location": {
                    "file": "crates/winwincode-delivery/src/application/workrun.rs",
                    "line": 424,
                    "column": 18,
                    "end_line": 424,
                    "start_byte": 15766,
                    "end_byte": 15770,
                    "full_location_ref": "/functional_chains/17/pattern/selection_predicate_sources/3/expression/operands/0/operand/object/location"
                  },
                  "reference": {
                    "remaining_fields_ref": "/functional_chains/17/pattern/selection_predicate_sources/3/expression/operands/0/operand/object/reference"
                  }
                }
              }
            }
          ],
          "shown_count": 1,
          "total_count": 2,
          "truncated": true,
          "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources/3/expression/operands"
        }
      },
      "remaining_fields_ref": "/functional_chains/17/pattern/selection_predicate_sources/3"
    }
  ],
  "shown_count": 4,
  "total_count": 8,
  "truncated": true,
  "full_value_ref": "/functional_chains/17/pattern/selection_predicate_sources"
}
```

**sequences**：`/functional_chains/17/pattern/sequences`；展示截断：`true`。

```json
{
  "selection": {
    "all_function_paths_or_effects_accounted": false,
    "future_or_callback_activation_proven": false,
    "region_kind": "function_item",
    "role": "selection",
    "assignment_attempts": [],
    "call_result_guard_source_links": [],
    "conditions": [],
    "guards": [],
    "opaque_direct_control_regions": [],
    "orders": [
      {
        "source_fact_refs": [
          "/functional_chains/17/source_facts/22"
        ],
        "after_step_id": "5039e1da00a8e6ea903a9588",
        "all_paths_reach_next_proven": false,
        "before_step_id": "533dc87f955ba5613850cca0",
        "id": "56bfe2ee8485b441e2eec6d2",
        "kind": "conditional_direct_statement_order",
        "model_id": "captured-normal-statement-control-v1",
        "origin": "source-derived",
        "role": "selection",
        "conditions": [
          "both direct statements normally reached in the same invocation",
          "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
        ],
        "location": {
          "file": "crates/winwincode-delivery/src/application/workrun.rs",
          "line": 393,
          "column": 9,
          "end_line": 403,
          "start_byte": 14681,
          "end_byte": 15023,
          "full_location_ref": "/functional_chains/17/pattern/sequences/selection/orders/0/location"
        }
      },
      {
        "source_fact_refs": [
          "/functional_chains/17/source_facts/23"
        ],
        "after_step_id": "5505521bbaa3fe4563f7483d",
        "all_paths_reach_next_proven": false,
        "before_step_id": "5039e1da00a8e6ea903a9588",
        "id": "7fbdfc1ffbd9776ce639260e",
        "kind": "conditional_direct_statement_order",
        "model_id": "captured-normal-statement-control-v1",
        "origin": "source-derived",
        "role": "selection",
        "conditions": [
          "both direct statements normally reached in the same invocation",
          "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
        ],
        "location": {
          "file": "crates/winwincode-delivery/src/application/workrun.rs",
          "line": 404,
          "column": 9,
          "end_line": 410,
          "start_byte": 15032,
          "end_byte": 15273,
          "full_location_ref": "/functional_chains/17/pattern/sequences/selection/orders/1/location"
        }
      },
      {
        "source_fact_refs": [
          "/functional_chains/17/source_facts/24"
        ],
        "after_step_id": "c8d420e4d1b7b79f4f8b479d",
        "all_paths_reach_next_proven": false,
        "before_step_id": "5505521bbaa3fe4563f7483d",
        "id": "add1b437a5688c20d1fa9d8b",
        "kind": "conditional_direct_statement_order",
        "model_id": "captured-normal-statement-control-v1",
        "origin": "source-derived",
        "role": "selection",
        "conditions": [
          "both direct statements normally reached in the same invocation",
          "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
        ],
        "location": {
          "file": "crates/winwincode-delivery/src/application/workrun.rs",
          "line": 411,
          "column": 9,
          "end_line": 411,
          "start_byte": 15282,
          "end_byte": 15318,
          "full_location_ref": "/functional_chains/17/pattern/sequences/selection/orders/2/location"
        }
      }
    ],
    "source_region_location": {
      "file": "crates/winwincode-delivery/src/application/workrun.rs",
      "line": 391,
      "column": 5,
      "end_line": 412,
      "start_byte": 14572,
      "end_byte": 15324,
      "full_location_ref": "/functional_chains/17/pattern/sequences/selection/source_region_location"
    },
    "steps": [
      {
        "source_fact_refs": [
          "/functional_chains/17/source_facts/16"
        ],
        "conditional_normal_reaching_only": true,
        "id": "533dc87f955ba5613850cca0",
        "kind": "direct_statement_call_step",
        "origin": "source-derived",
        "role": "selection",
        "source_order_index": 0,
        "statement_kind": "expression_statement",
        "call_ids": [
          "855b44866e7a3bb46e68f8fc"
        ],
        "location": {
          "file": "crates/winwincode-delivery/src/application/workrun.rs",
          "line": 392,
          "column": 9,
          "end_line": 392,
          "start_byte": 14655,
          "end_byte": 14672,
          "full_location_ref": "/functional_chains/17/pattern/sequences/selection/steps/0/location"
        }
      },
      {
        "source_fact_refs": [
          "/functional_chains/17/source_facts/17"
        ],
        "conditional_normal_reaching_only": true,
        "id": "5039e1da00a8e6ea903a9588",
        "kind": "direct_statement_call_step",
        "origin": "source-derived",
        "role": "selection",
        "source_order_index": 1,
        "statement_kind": "let_declaration",
        "call_ids": [
          "d66389b0e2e61ccac7894a41",
          "33b3ecb35141bcefbd191a8b",
          "aae14c48c9374c20bf33ef06",
          "8b1e056bbaad5e5d7fcc6a0d"
        ],
        "location": {
          "file": "crates/winwincode-delivery/src/application/workrun.rs",
          "line": 393,
          "column": 9,
          "end_line": 403,
          "start_byte": 14681,
          "end_byte": 15023,
          "full_location_ref": "/functional_chains/17/pattern/sequences/selection/steps/1/location"
        }
      },
      {
        "source_fact_refs": [
          "/functional_chains/17/source_facts/18"
        ],
        "conditional_normal_reaching_only": true,
        "id": "5505521bbaa3fe4563f7483d",
        "kind": "direct_statement_call_step",
        "origin": "source-derived",
        "role": "selection",
        "source_order_index": 2,
        "statement_kind": "let_declaration",
        "call_ids": [
          "6dd5525bf62d46a6003b423e",
          "d458071b3c1faebb1bd72805"
        ],
        "location": {
          "file": "crates/winwincode-delivery/src/application/workrun.rs",
          "line": 404,
          "column": 9,
          "end_line": 410,
          "start_byte": 15032,
          "end_byte": 15273,
          "full_location_ref": "/functional_chains/17/pattern/sequences/selection/steps/2/location"
        }
      },
      {
        "source_fact_refs": [
          "/functional_chains/17/source_facts/19"
        ],
        "conditional_normal_reaching_only": true,
        "id": "c8d420e4d1b7b79f4f8b479d",
        "kind": "direct_statement_call_step",
        "origin": "source-derived",
        "role": "selection",
        "source_order_index": 3,
        "statement_kind": "call_expression",
        "call_ids": [
          "ed235a2f40493949b8d66f6c"
        ],
        "location": {
          "file": "crates/winwincode-delivery/src/application/workrun.rs",
          "line": 411,
          "column": 9,
          "end_line": 411,
          "start_byte": 15282,
          "end_byte": 15318,
          "full_location_ref": "/functional_chains/17/pattern/sequences/selection/steps/3/location"
        }
      }
    ]
  },
  "start": {
    "all_function_paths_or_effects_accounted": false,
    "future_or_callback_activation_proven": false,
    "region_kind": "function_item",
    "role": "start",
    "assignment_attempts": [
      {
        "source_fact_refs": [
          "/functional_chains/17/source_facts/31"
        ],
        "id": "04a1ff3f01e129b209d0ae45",
        "kind": "ordered_source_assignment_attempt",
        "origin": "source-derived",
        "role": "start",
        "write_runtime_success_proven": false,
        "branch_context": [],
        "left": {
          "current_referent_value_proven": false,
          "kind": "field_expression",
          "member": "state",
          "location": {
            "file": "crates/winwincode-delivery/src/application/workrun.rs",
            "line": 440,
            "column": 9,
            "end_line": 440,
            "start_byte": 16502,
            "end_byte": 16517,
            "full_location_ref": "/functional_chains/17/pattern/sequences/start/assignment_attempts/0/left/location"
          },
          "member_location": {
            "file": "crates/winwincode-delivery/src/application/workrun.rs",
            "line": 440,
            "column": 19,
            "end_line": 440,
            "start_byte": 16512,
            "end_byte": 16517,
            "full_location_ref": "/functional_chains/17/pattern/sequences/start/assignment_attempts/0/left/member_location"
          },
          "object": {
            "kind": "identifier",
            "name": "work_item",
            "location": {
              "file": "crates/winwincode-delivery/src/application/workrun.rs",
              "line": 440,
              "column": 9,
              "end_line": 440,
              "start_byte": 16502,
              "end_byte": 16511,
              "full_location_ref": "/functional_chains/17/pattern/sequences/start/assignment_attempts/0/left/object/location"
            },
            "reference": {
              "declaration_id": "17ada5ae18a50ac7f384473b46d809b5e35327667ff593dbe09ed8e67af42e69",
              "declaration_kind": "captured_rust_local",
              "identity_scope": "plain captured binder syntax only",
              "macro_namespace_complete": false,
              "runtime_value_identity_proven": false,
              "state": "captured_unique_rust_binder",
              "binder_location": {
                "file": "crates/winwincode-delivery/src/application/workrun.rs",
                "line": 439,
                "column": 17,
                "end_line": 439,
                "start_byte": 16468,
                "end_byte": 16477,
                "full_location_ref": "/functional_chains/17/pattern/sequences/start/assignment_attempts/0/left/object/reference/binder_location"
              },
              "declaration_location": {
                "file": "crates/winwincode-delivery/src/application/workrun.rs",
                "line": 439,
                "column": 9,
                "end_line": 439,
                "start_byte": 16460,
                "end_byte": 16493,
                "full_location_ref": "/functional_chains/17/pattern/sequences/start/assignment_attempts/0/left/object/reference/declaration_location"
              }
            }
          }
        },
        "location": {
          "file": "crates/winwincode-delivery/src/application/workrun.rs",
          "line": 440,
          "column": 9,
          "end_line": 440,
          "start_byte": 16502,
          "end_byte": 16545,
          "full_location_ref": "/functional_chains/17/pattern/sequences/start/assignment_attempts/0/location"
        },
        "right": {
          "kind": "scoped_identifier",
          "source": "WorkItemState::InProgress",
          "children": [
            {
              "kind": "identifier",
              "name": "WorkItemState",
              "location": {
                "file": "crates/winwincode-delivery/src/application/workrun.rs",
                "line": 440,
                "column": 27,
                "end_line": 440,
                "start_byte": 16520,
                "end_byte": 16533,
                "full_location_ref": "/functional_chains/17/pattern/sequences/start/assignment_attempts/0/right/children/0/location"
              },
              "reference": {
                "plain_binder_candidates": 0,
                "runtime_value_identity_proven": false,
                "state": "captured_rust_reference",
                "text": "WorkItemState",
                "location": {
                  "file": "crates/winwincode-delivery/src/application/workrun.rs",
                  "line": 440,
                  "column": 27,
                  "end_line": 440,
                  "start_byte": 16520,
                  "end_byte": 16533,
                  "full_location_ref": "/functional_chains/17/pattern/sequences/start/assignment_attempts/0/right/children/0/reference/location"
                }
              }
            },
            {
              "kind": "identifier",
              "name": "InProgress",
              "location": {
                "file": "crates/winwincode-delivery/src/application/workrun.rs",
                "line": 440,
                "column": 42,
                "end_line": 440,
                "start_byte": 16535,
                "end_byte": 16545,
                "full_location_ref": "/functional_chains/17/pattern/sequences/start/assignment_attempts/0/right/children/1/location"
              },
              "reference": {
                "plain_binder_candidates": 0,
                "runtime_value_identity_proven": false,
                "state": "captured_rust_reference",
                "text": "InProgress",
                "location": {
                  "file": "crates/winwincode-delivery/src/application/workrun.rs",
                  "line": 440,
                  "column": 42,
                  "end_line": 440,
                  "start_byte": 16535,
                  "end_byte": 16545,
                  "full_location_ref": "/functional_chains/17/pattern/sequences/start/assignment_attempts/0/right/children/1/reference/location"
                }
              }
            }
          ],
          "location": {
            "file": "crates/winwincode-delivery/src/application/workrun.rs",
            "line": 440,
            "column": 27,
            "end_line": 440,
            "start_byte": 16520,
            "end_byte": 16545,
            "full_location_ref": "/functional_chains/17/pattern/sequences/start/assignment_attempts/0/right/location"
          }
        }
      }
    ],
    "call_result_guard_source_links": [],
    "conditions": [],
    "guards": [],
    "opaque_direct_control_regions": [],
    "orders": [
      {
        "source_fact_refs": [
          "/functional_chains/17/source_facts/32"
        ],
        "after_step_id": "047512d2a292ff4839dfa97c",
        "all_paths_reach_next_proven": false,
        "before_step_id": "17d1234316b23ff42411f9cc",
        "id": "2ffd8e9840595f03c8738ebf",
        "kind": "conditional_direct_statement_order",
        "model_id": "captured-normal-statement-control-v1",
        "origin": "source-derived",
        "role": "start",
        "conditions": [
          "both direct statements normally reached in the same invocation",
          "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
        ],
        "location": {
          "file": "crates/winwincode-delivery/src/application/workrun.rs",
          "line": 420,
          "column": 9,
          "end_line": 436,
          "start_byte": 15667,
          "end_byte": 16341,
          "full_location_ref": "/functional_chains/17/pattern/sequences/start/orders/0/location"
        }
      },
      {
        "source_fact_refs": [
          "/functional_chains/17/source_facts/33"
        ],
        "after_step_id": "fe9fcd3c4352fcd496710fad",
        "all_paths_reach_next_proven": false,
        "before_step_id": "047512d2a292ff4839dfa97c",
        "id": "16ae832769ed8fb2d23bca97",
        "kind": "conditional_direct_statement_order",
        "model_id": "captured-normal-statement-control-v1",
        "origin": "source-derived",
        "role": "start",
        "conditions": [
          "both direct statements normally reached in the same invocation",
          "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
        ],
        "location": {
          "file": "crates/winwincode-delivery/src/application/workrun.rs",
          "line": 439,
          "column": 9,
          "end_line": 439,
          "start_byte": 16460,
          "end_byte": 16493,
          "full_location_ref": "/functional_chains/17/pattern/sequences/start/orders/1/location"
        }
      },
      {
        "source_fact_refs": [
          "/functional_chains/17/source_facts/34"
        ],
        "after_step_id": "b9e642aa5e556f913a157cce",
        "all_paths_reach_next_proven": false,
        "before_step_id": "fe9fcd3c4352fcd496710fad",
        "id": "da858f7cbd26d01b21db5ff1",
        "kind": "conditional_direct_statement_order",
        "model_id": "captured-normal-statement-control-v1",
        "origin": "source-derived",
        "role": "start",
        "conditions": [
          "both direct statements normally reached in the same invocation",
          "preceding asynchronous operations complete normally; no claim of completion or whole-program dominance"
        ],
        "location": {
          "file": "crates/winwincode-delivery/src/application/workrun.rs",
          "line": 441,
          "column": 9,
          "end_line": 441,
          "start_byte": 16555,
          "end_byte": 16594,
          "full_location_ref": "/functional_chains/17/pattern/sequences/start/orders/2/location"
        }
      }
    ],
    "source_region_location": {
      "file": "crates/winwincode-delivery/src/application/workrun.rs",
      "line": 418,
      "column": 5,
      "end_line": 442,
      "start_byte": 15541,
      "end_byte": 16600,
      "full_location_ref": "/functional_chains/17/pattern/sequences/start/source_region_location"
    },
    "steps": {
      "shown_items": [
        {
          "source_fact_refs": [
            "/functional_chains/17/source_facts/25"
          ],
          "conditional_normal_reaching_only": true,
          "id": "17d1234316b23ff42411f9cc",
          "kind": "direct_statement_call_step",
          "origin": "source-derived",
          "role": "start",
          "source_order_index": 0,
          "statement_kind": "expression_statement",
          "call_ids": [
            "00566343142225ed3672799c"
          ],
          "location": {
            "file": "crates/winwincode-delivery/src/application/workrun.rs",
            "line": 419,
            "column": 9,
            "end_line": 419,
            "start_byte": 15641,
            "end_byte": 15658,
            "full_location_ref": "/functional_chains/17/pattern/sequences/start/steps/0/location"
          }
        },
        {
          "source_fact_refs": [
            "/functional_chains/17/source_facts/26"
          ],
          "conditional_normal_reaching_only": true,
          "id": "047512d2a292ff4839dfa97c",
          "kind": "direct_statement_call_step",
          "origin": "source-derived",
          "role": "start",
          "source_order_index": 1,
          "statement_kind": "let_declaration",
          "remaining_fields_ref": "/functional_chains/17/pattern/sequences/start/steps/1"
        }
      ],
      "shown_count": 2,
      "total_count": 4,
      "truncated": true,
      "full_value_ref": "/functional_chains/17/pattern/sequences/start/steps"
    }
  }
}
```

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
| crates/winwincode-server | crates/winwincode-control-plane | 16 |
| crates/winwincode-server | crates/winwincode-domain | 6 |
| crates/winwincode-server | crates/winwincode-execution-port | 5 |
| crates/winwincode-server | crates/winwincode-storage | 1 |
| crates/winwincode-storage | crates/winwincode-domain | 1 |
| crates/winwincode-storage | crates/winwincode-publication | 1 |
| crates/winwincode-worker | crates/winwincode-codex | 14 |
| crates/winwincode-worker | crates/winwincode-domain | 1 |
| crates/winwincode-worker | crates/winwincode-execution-port | 13 |
| crates/winwincode-worker | crates/winwincode-provider | 5 |

### 已捕获的写者与消费者引用

以下内容引用保存分析中的词法写者、相同 token 消费者和拒绝守卫。它保留原 `ownership_assessment`；不按目录分配职责，不推断唯一事实所有者、规范权威或全部授权。

| 来源规则 | 保存的所有权范围评估 | 捕获字段组数 | 完整写者组引用 |
| --- | --- | --- | --- |
| wwc-captured-record-resource-writers | partial_captured_writers_and_consumers | 41 | /functional_chains/1/pattern/captured_resource_writer_groups |

- `wwc-captured-record-resource-writers` 的实际写者声明：["&lt;ProductionCodexAdapter as CodexCoreAdapter&gt;.submit_turn","WorkRunAggregate.start_item","mountWinWinCodeClient","mountWinWinCodeClient.performRender"]；相关源码关系：`/source_relation_index/entries/1`。

## 局部分析

| 规则 | 类型 | 结果 | 保存发现 |
| --- | --- | --- | --- |
| wwc-astra-device-spec-field-construction | static_contract_required_object_fields | uncertain | 9afc0a7d3a7db9eca2658e10 |
| wwc-astra-navigation-context | static_navigation_query_context | uncertain | c79fe34c316f44123c48b4c8 |

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
