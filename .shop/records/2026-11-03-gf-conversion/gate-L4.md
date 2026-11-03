# Layer 4 gate (P12 supervision, P13 the 1.0.0 upgrade step)

Date: 2026-11-03. Branch: gf-conversion. SHOPSYSTEM_GF unset (P1's installer is in use).

## What merged
- gfc/P12 (4f023a79), then gfc/P13 (b75cba1c), in plan order with --no-ff. There were no conflicts: the packages own
  disjoint files.
- P12 converted supervision.md into 86 groups and 139 statements, with a generated feature and handlers
  (`tests/scenarios/supervision_handlers*.py`, `supervision_world.py`, `supervision_build.py`, `supervision_plans.py`).
  Its report is report-P12.md.
- P13 added `scripts/migrate_upgrade_codified.py`, the 1.0.0 step. Its report is report-P13.md.

## Fixes at the merge (test first)
- `tests/scripts/test_model_restates.py`: P12 asked for this. `LiveRestatesTest` asserted the state before P12, when
  supervision was not yet restated. It now asserts that `model restates` with no capability named exits 0 with
  "0 pending, 0 missing".
- `scripts/migrate_spec.plan_holding`: P13 asked for this. It still ran the removed `features deprecate`. It now
  deletes each `@holding` scenario with `migrate_upgrade_codified.without_tagged(text, "@holding")`, which matches
  migration-tools r3@0.29 (dropped). The dead `drop_holding` and its now-unused imports are gone. The new test is
  `tests/scripts/test_migrate_spec_holding.py`.

## Gate outcomes
- `model check`: no `v_p*`, `v15[g-k]` or `v_t[4-6]` row. PASS.
- `model logic`: exits 0, with 7 L2 findings, all notes ("say the same thing") in analysis-tools,
  batch-measurement, feature-file-tools and migration-tools. It takes about 5.6 min on one core. PASS.
- `model restates`: "581 ids: 516 restated, 65 dropped, 0 pending, 0 missing", exit 0. PASS.
- `features generate --check`: exits 0, and nothing is skipped. PASS.
- `pytest -q` (run with -n 8): 761 passed, 1 skipped, 0 failed. All 23 baseline failures and all 11 p8-broken
  scenarios are gone. PASS.
- Common checks: `tools size --limit 300` exits 0, and ruff is clean on the changed files.

## Carried forward (to P14 unless named otherwise)
- Unresolved references: model check prints about 458 unresolved or "names no 0.29 id" lines. They are old
  `.shop/work` references. P14 runs `migrate upgrade` on this repo, which rewrites them to `@0.29`, and makes
  model_facts accept any `@0.29` id as history. About 650 of the rewritten references name 0.29 ids that were already
  retired at 96818f71 and are not in restated.json, such as feature-file-tools#r22. The upgrade step reports the open
  capability-proposals of i45 and i59 for re-integration.
- A work run bug P12 found, not fixed here (it is outside the gate): when an integrate round's raise into an upstream
  is refused (`supervise_rounds.raise_before_merge` → `undo_round`), the following commit of the initiative's
  transition fails with "pathspec .shop/work/i1/runs/i1". It should record a fault that names the refusal. It is to
  be raised as a fix with a test, in P14 or after the release.
- Optional generator and vocabulary fixes P12 worked around:
  - In features_generate, a condition whose Means is not "its <attr> is …" is dropped when it is written before the
    noun ("a faulty session").
  - resolve() picks the relation `for (stage → node)` by term alone.
  - A step that names its kind with no instance still needs `work_queue_world.bind_all` in its test module.
- P13's 1.0.0 step runs only at plugin 1.0.0. Its tests patch the version. Once P14 bumps plugin.json, the scenarios
  can use the plugin itself instead of `migration_old.plugin()`.
- Still open from earlier layers: README, agents and skills that name removed commands; the CLAUDE.md module-map
  rows (`migrate_upgrade_codified.py`, the supervision handler modules, the L1–L3 rows); legacy code; the
  migration_upgrade_steps shim; v16a's date cutoff.
