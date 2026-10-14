# Original frozen baseline comparison artifacts

`compare_original_baseline.py` runs after the formal v12 freeze, archived core copy, and both final database publications exist. It reuses the unchanged `frozen-static-baseline-1.3` evaluator and authenticates the original baseline and contract bytes. All 26 observations are compared: thirteen per repository, including evidence-only and intentionally unknown observations. Their source references cover 36 original raw files, rather than 26 files.

The script opens both databases through immutable read-only SQLite, refuses a nonempty WAL, and acquires the shared `goal-source-query.lock` internally with `fcntl.flock`. Do not wrap this command in a second lock acquisition. It first reads small publication metadata and finding-type counts, then loads one complete saved snapshot at a time. Old databases are never opened; prior comparisons and policy JSON are read as preserved artifacts.

Run from the CallScope workspace after publication:

```bash
PYTHONPATH=/workspace/callscope python reports/astra-iteration10/compare_original_baseline.py
```

The default databases are `codepatchbay-v12.sqlite3` and `winwincode-v12.sqlite3` in this directory. CLI arguments can override either database, the freeze/archive, roots, policy/previous/output directories, baseline/contract paths, and the shared lock path. Baseline and evaluator hashes remain fixed even with path overrides. Missing databases return `not_ready`; the script creates no fixture or substitute snapshot.

Generated artifacts:

- `codepatchbay-baseline-v12-and-v11.json` and `winwincode-baseline-v12-and-v11.json` retain current and previous full comparisons, per-observation changes, policy/model/capture scope changes, and target/source identity checks.
- The two `*-baseline-source-checks.json` artifacts retain every original referenced file and every observation's hash checks, preserving source-changed, source-missing, and evidence-unavailable outcomes.
- `ORIGINAL_BASELINE_COMPARISON.json` combines counts with the unchanged global denominator of 26.
- `PUBLICATION_IDENTITY.json` verifies the current Python implementation against the freeze and archived inventory, both database tool/component identities, all 36 original referenced raw-source hashes in saved and live source, and both frozen target commits.

Git is used only for `rev-parse HEAD`; the script does not run repository CLIs or Git hooks and does not claim the entire working tree is clean. Current target source files are read only to authenticate the original referenced bytes. Changed policies, registered models, and support-input capture are shown separately from unchanged frozen observations and evaluator semantics.

These artifacts organize published static evidence. They do not approve a release, rerun an independent source review, interpret the full human reports, or convert observation reproduction counts into precision, functional coverage, defect counts, or complete-goal acceptance. No targets or tests are executed.
