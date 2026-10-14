# 实际保存 WorkRun 关系的展示投影

此为已保存开发查询的展示，不是正式 Findings 报告，不重新分析或评级。

保存关系的展示摘要（`presentation_only=true`；不新增评级）：

完整 pattern：`/pattern`。展示截断：`true`；完整证据与原 pattern 保留。

**rows**：`/pattern/finite_effective_state_relation/rows`；显示 8/8 行；展示截断：`false`。

| input_state | source_quantifiers | effective_state | runnable | 完整行引用 |
| --- | --- | --- | --- | --- |
| WorkItemState::Done | {"source_quantifier_1":false} | WorkItemState::Done | false | /pattern/finite_effective_state_relation/rows/0 |
| WorkItemState::Done | {"source_quantifier_1":true} | WorkItemState::Done | false | /pattern/finite_effective_state_relation/rows/1 |
| WorkItemState::Ready | {"source_quantifier_1":false} | WorkItemState::Ready | true | /pattern/finite_effective_state_relation/rows/2 |
| WorkItemState::Ready | {"source_quantifier_1":true} | WorkItemState::WaitingDependency | false | /pattern/finite_effective_state_relation/rows/3 |
| WorkItemState::WaitingDependency | {"source_quantifier_1":false} | WorkItemState::Ready | true | /pattern/finite_effective_state_relation/rows/4 |
| WorkItemState::WaitingDependency | {"source_quantifier_1":true} | WorkItemState::WaitingDependency | false | /pattern/finite_effective_state_relation/rows/5 |
| &lt;other value of this state enum&gt; | {"source_quantifier_1":false} | &lt;other value of this state enum&gt; | false | /pattern/finite_effective_state_relation/rows/6 |
| &lt;other value of this state enum&gt; | {"source_quantifier_1":true} | &lt;other value of this state enum&gt; | false | /pattern/finite_effective_state_relation/rows/7 |

**non_runnable_table_rows**：`/pattern/finite_source_countercases/non_runnable_table_rows`；显示 6/6 行；展示截断：`false`。

| input_state | source_quantifiers | effective_state | runnable | 完整行引用 |
| --- | --- | --- | --- | --- |
| WorkItemState::Done | {"source_quantifier_1":false} | WorkItemState::Done | false | /pattern/finite_source_countercases/non_runnable_table_rows/0 |
| WorkItemState::Done | {"source_quantifier_1":true} | WorkItemState::Done | false | /pattern/finite_source_countercases/non_runnable_table_rows/1 |
| WorkItemState::Ready | {"source_quantifier_1":true} | WorkItemState::WaitingDependency | false | /pattern/finite_source_countercases/non_runnable_table_rows/2 |
| WorkItemState::WaitingDependency | {"source_quantifier_1":true} | WorkItemState::WaitingDependency | false | /pattern/finite_source_countercases/non_runnable_table_rows/3 |
| &lt;other value of this state enum&gt; | {"source_quantifier_1":false} | &lt;other value of this state enum&gt; | false | /pattern/finite_source_countercases/non_runnable_table_rows/4 |
| &lt;other value of this state enum&gt; | {"source_quantifier_1":true} | &lt;other value of this state enum&gt; | false | /pattern/finite_source_countercases/non_runnable_table_rows/5 |

**runnable_table_rows**：`/pattern/finite_source_countercases/runnable_table_rows`；显示 2/2 行；展示截断：`false`。

| input_state | source_quantifiers | effective_state | runnable | 完整行引用 |
| --- | --- | --- | --- | --- |
| WorkItemState::Ready | {"source_quantifier_1":false} | WorkItemState::Ready | true | /pattern/finite_source_countercases/runnable_table_rows/0 |
| WorkItemState::WaitingDependency | {"source_quantifier_1":false} | WorkItemState::Ready | true | /pattern/finite_source_countercases/runnable_table_rows/1 |

| 保存字段 | 实际值 | 完整引用 |
| --- | --- | --- |
| version | captured-rust-finite-state-relations-1 | /pattern/version |
| trusted_model | rust-finite-iterator-enum-source-v1 | /pattern/trusted_model |
| state_table_dependency_quantifier_linked | true | /pattern/state_table_dependency_quantifier_linked |
| scoped_source_supported | true | /pattern/scoped_source_supported |
| all_active_states_or_attempts_proven | false | /pattern/all_active_states_or_attempts_proven |
| whole_domain_state_machine_closed | false | /pattern/whole_domain_state_machine_closed |
| runtime_schedule_or_termination_proven | false | /pattern/runtime_schedule_or_termination_proven |
| graph_calls_repaired_or_promoted | false | /pattern/graph_calls_repaired_or_promoted |

**finite_effective_state_relation**：`/pattern/finite_effective_state_relation`；展示截断：`true`。

```json
{
  "supported": true,
  "fact_id": "3cdb186863013a44da128092",
  "runnable_equals": "WorkItemState::Ready",
  "full_enum_enumeration": false,
  "rows": {
    "presentation_table_ref": "/presentation/tables/0",
    "full_value_ref": "/pattern/finite_effective_state_relation/rows",
    "total_rows": 8,
    "presentation_only": true
  },
  "symbolic_quantifiers": [
    {
      "name": "source_quantifier_1",
      "expression": {
        "kind": "method",
        "method": "any",
        "receiver": {
          "kind": "method",
          "method": "iter",
          "receiver": {
            "kind": "field",
            "field": "depends_on",
            "value": {
              "kind": "name",
              "name": "item",
              "span": [
                23825,
                23829
              ]
            },
            "span": [
              23825,
              23840
            ]
          },
          "arguments": [],
          "span": [
            23825,
            23847
          ]
        },
        "arguments": [
          {
            "kind": "closure",
            "simple_parameters": true,
            "parameters": [
              "dependency"
            ],
            "body": {
              "kind": "block",
              "statements": [
                {
                  "kind": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/pattern/finite_effective_state_relation/symbolic_quantifiers/0/expression/arguments/0/body/statements/0/kind"
                  },
                  "operator": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/pattern/finite_effective_state_relation/symbolic_quantifiers/0/expression/arguments/0/body/statements/0/operator"
                  },
                  "value": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/pattern/finite_effective_state_relation/symbolic_quantifiers/0/expression/arguments/0/body/statements/0/value"
                  },
                  "span": {
                    "omitted_for_presentation": true,
                    "full_value_ref": "/pattern/finite_effective_state_relation/symbolic_quantifiers/0/expression/arguments/0/body/statements/0/span"
                  }
                }
              ],
              "span": [
                23865,
                24007
              ]
            },
            "span": [
              23852,
              24007
            ]
          }
        ],
        "span": [
          23825,
          24008
        ]
      }
    }
  ],
  "state_field_path": [
    "item",
    "state"
  ]
}
```

**dependency_blocker_relation**：`/pattern/dependency_blocker_relation`；展示截断：`false`。

```json
{
  "supported": true,
  "relations": [
    {
      "source_fact_refs": [
        "/source_facts/113"
      ],
      "kind": "rust_finite_dependency_blocker_relation",
      "origin": "source-derived",
      "role": "effective_state",
      "finite_state_component": "captured-rust-finite-state-relations-1",
      "quantifier": "exists dependency for which no equal-identity candidate has the captured required state",
      "empty_dependency_collection_result": false,
      "actual_dependencies_or_reachability_evaluated": false,
      "id": "7939b4e9caed8903829ba2a7",
      "location": {
        "file": "crates/winwincode-delivery/src/application/workrun.rs",
        "line": 648,
        "column": 10,
        "end_line": 652,
        "start_byte": 23825,
        "end_byte": 24008,
        "full_location_ref": "/pattern/dependency_blocker_relation/relations/0/location"
      },
      "dependency_collection": {
        "kind": "field",
        "field": "depends_on",
        "value": {
          "kind": "name",
          "name": "item",
          "span": [
            23825,
            23829
          ]
        },
        "span": [
          23825,
          23840
        ]
      },
      "candidate_collection": {
        "kind": "name",
        "name": "items",
        "span": [
          23876,
          23881
        ]
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
      "required_candidate_state_comparison": {
        "candidate_state": [
          "candidate",
          "state"
        ],
        "accepted_state": [
          "WorkItemState",
          "Done"
        ]
      }
    }
  ]
}
```

**persisted_selection_recheck_relation**：`/pattern/persisted_selection_recheck_relation`；展示截断：`false`。

```json
{
  "supported": true,
  "fact_id": "65bf2f5a523494d767da777e",
  "active_collection_computed_from_persisted_runs": true,
  "all_enum_states_or_attempts_proven": false,
  "checks": {
    "same_active_state_alternatives": true,
    "same_persisted_run_collection": true,
    "same_projected_item_identity_field": true,
    "same_state_field_on_actual_filter_and_exclusion_elements": true,
    "active_exclusion_key_equals_exact_find_requested_id": true,
    "runnable_predicate_in_both_find_conjunctions": true,
    "active_collection_passed_to_selector_and_selected_id_rechecked": true,
    "selected_result_and_active_membership_share_exact_item_key": true,
    "aggregate_validation_collect_select_recheck_source_order": true,
    "both_selected_entries_have_fallible_validation_prefix": true
  },
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
  "transfer": {
    "active_local_binding": "active",
    "active_struct_field": "active_work_item_ids",
    "selected_local_binding": "start",
    "same_active_struct_field": true,
    "same_selected_result_root": true,
    "same_item_collection_argument": true,
    "same_selected_result_identity": true,
    "selected_id_matches_exact_item_key": true,
    "active_key_matches_contains_selected_item_key": true,
    "source_statement_pipeline_order_closed": true,
    "membership_receiver": [
      "input",
      "active_work_item_ids"
    ],
    "membership_argument": [
      [
        "item",
        "id"
      ]
    ],
    "selected_recheck_arguments": [
      [
        "start",
        "work_item",
        "id"
      ]
    ],
    "selector_return_identity": {
      "selected_binding": "item",
      "closed_under_plain_selected_clone_source_model": true,
      "returned_record_field_path": [
        "started"
      ],
      "resolved_selected_path": [
        "item"
      ],
      "contains_selected_key": [
        "item",
        "id"
      ],
      "rechecked_result_key": [
        "start",
        "work_item",
        "id"
      ],
      "identity_field_assignments": []
    }
  },
  "validation_prefixes": [
    {
      "source_fact_refs": [
        "/source_facts/114"
      ],
      "kind": "rust_finite_selection_validation_prefix",
      "origin": "source-derived",
      "role": "aggregate_selector",
      "finite_state_component": "captured-rust-finite-state-relations-1",
      "selected_validator_symbol": "WorkRunAggregate.validate",
      "normal_continuation_requires_ok": true,
      "validator_entire_semantics_proven": false,
      "id": "a9ec0c05542cff634e6c6aac",
      "location": {
        "file": "crates/winwincode-delivery/src/application/workrun.rs",
        "line": 392,
        "column": 9,
        "end_line": 392,
        "start_byte": 14655,
        "end_byte": 14671,
        "full_location_ref": "/pattern/persisted_selection_recheck_relation/validation_prefixes/0/location"
      },
      "first_statement": {
        "kind": "try",
        "value": {
          "kind": "method",
          "method": "validate",
          "receiver": {
            "kind": "name",
            "name": "self",
            "span": [
              14655,
              14659
            ]
          },
          "arguments": [],
          "span": [
            14655,
            14670
          ]
        },
        "span": [
          14655,
          14671
        ]
      }
    },
    {
      "source_fact_refs": [
        "/source_facts/115"
      ],
      "kind": "rust_finite_selection_validation_prefix",
      "origin": "source-derived",
      "role": "item_selector",
      "finite_state_component": "captured-rust-finite-state-relations-1",
      "selected_validator_symbol": "WorkRunAggregate.validate",
      "normal_continuation_requires_ok": true,
      "validator_entire_semantics_proven": false,
      "id": "2809f2f650ed7680d599ae22",
      "location": {
        "file": "crates/winwincode-delivery/src/application/workrun.rs",
        "line": 419,
        "column": 9,
        "end_line": 419,
        "start_byte": 15641,
        "end_byte": 15657,
        "full_location_ref": "/pattern/persisted_selection_recheck_relation/validation_prefixes/1/location"
      },
      "first_statement": {
        "kind": "try",
        "value": {
          "kind": "method",
          "method": "validate",
          "receiver": {
            "kind": "name",
            "name": "self",
            "span": [
              15641,
              15645
            ]
          },
          "arguments": [],
          "span": [
            15641,
            15656
          ]
        },
        "span": [
          15641,
          15657
        ]
      }
    }
  ],
  "find_predicate_source_facts": {
    "item_selector": "32f3f469645563820f507fc3",
    "selector": "84fb9746ec9a592d893e5437"
  }
}
```

**validator_enum_predicate_source_fact_ids**：`/pattern/validator_enum_predicate_source_fact_ids`；展示截断：`false`。

```json
[
  "e9b961644f52c1a08b519c1c"
]
```

**finite_source_countercases**：`/pattern/finite_source_countercases`；展示截断：`false`。

```json
{
  "countercases_are_symbolic_source_conditions_not_observed_runtime_records": true,
  "non_runnable_table_rows": {
    "presentation_table_ref": "/presentation/tables/1",
    "full_value_ref": "/pattern/finite_source_countercases/non_runnable_table_rows",
    "total_rows": 6,
    "presentation_only": true
  },
  "runnable_table_rows": {
    "presentation_table_ref": "/presentation/tables/2",
    "full_value_ref": "/pattern/finite_source_countercases/runnable_table_rows",
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
      "macro_resolution": "conditional_standard_matches_macro_model",
      "macro_expanded": false,
      "value": {
        "kind": "field",
        "field": "state",
        "value": {
          "kind": "name",
          "name": "run"
        }
      },
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
      ]
    }
  ]
}
```

**iterator_relation_fact_ids**：`/pattern/iterator_relation_fact_ids`；展示截断：`false`。

```json
{
  "aggregate_selector": [
    "743a22a20070dc4eac2cfe03"
  ],
  "effective_state": [
    "39015ed4994196db5dd6f2a7",
    "45c1a673209d0600d2a3fcc5"
  ],
  "item_selector": [
    "32f3f469645563820f507fc3",
    "aad15d50780db51e76f93cb9"
  ],
  "runnable": [],
  "selector": [
    "84fb9746ec9a592d893e5437"
  ]
}
```

**source_model_conditions**：`/pattern/source_model_conditions`；展示截断：`false`。

```json
[
  "selected normal source bodies are reached and their fallible prefixes return Ok",
  "captured plain matches! uses the standard Rust macro, not an external macro override",
  "captured Vec/slice iterator, HashSet membership, field equality and Clone obey their standard source contracts",
  "the recorded unique same-module helper source declarations are the invoked helpers; historical unresolved graph calls remain unchanged"
]
```

**boundaries**：`/pattern/boundaries`；展示截断：`false`。

```json
[
  "source-mentioned enum alternatives and a symbolic complement are interpreted; no complete enum declaration or arbitrary macro expansion is inferred",
  "quantifiers describe current captured predicates; concrete item records, dependency truth and actual active runs are unknown",
  "selection does not prove persistence, scheduling fairness, concurrency isolation, all state transitions or every attempt identity"
]
```

**expression_budget**：`/pattern/expression_budget`；展示截断：`false`。

```json
{
  "operations": 196,
  "limit": 131072,
  "incomplete": false
}
```

**necessary_gaps**：`/pattern/necessary_gaps`；展示截断：`false`。

```json
[]
```

