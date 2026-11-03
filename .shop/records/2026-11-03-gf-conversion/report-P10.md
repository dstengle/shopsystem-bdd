---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-report-p10
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# Report: P10, small service capabilities and `features`' editing commands removed

Branch `gfc/P10`, 10 commits, HEAD 422736d0. Written by the layer 3 merge from the package's returned notes: the harness refused the package's own write of this file. done=false only for `model parse --file`, settled at the merge.

## What was converted

analysis-tools, batch-measurement, feature-file-tools and migration-tools are codified, each with Terms, Restates,
Dropped, a generated feature and handler modules; old step modules deleted, world helpers trimmed, each
`test_<cap>.py` a single `scenarios()` call. `features tag|move|deprecate|retire|rebind|verify-moved`, their code
(`features_edit.py`, `cmd_rebind`, `cmd_verify`) and tests are removed; feature-file-tools gains groups for
`generate`, `generate --check` and `vocab --check`.

Restates: analysis-tools 24 restated; batch-measurement 29; feature-file-tools 14 restated, 14 dropped;
migration-tools 32 restated, 1 dropped.

## Calls

- Givens use kinds of each capability's own Terms; ThenDoes uses only its own events, so handler keys stay apart.
- `Python interpreter` and attribute `standing` avoid clashes with P11.
- migration-tools skips r37–r45 (i59's open proposal adds them; reuse would be v15i). Next free: r53, g29.
- migration-tools g11 (r19) restates r6@0.29: ThenExitsOk runs `model check --json` after each successful migrate run.

## Checks on the branch

logic, restates, `features generate --check` exit 0 for all four; 125 passed on the named tests; vocab check exit 0;
the removed commands exit 2; suite at baseline; size, ruff, `tools check` clean.

## Asks carried

- `features_generate`: `Scenario.precondition` raises StopIteration when a While names a K with no instance yet; a
  condition's value set on a given-block instance is lost; the instance letter is `kind[0]` without lower().
- Steps ambiguity: a Do Then on an instance named with a backticked code parses as SDoes and SDoesTo; spec_tree's
  DoTo guard is not applied to SDoesTo.
- vocab: a ThenDoes on a typed NP that is not an instance matches no step; common events need one dispatching handler
  in `world_*.py`.
- `migrate_spec.plan_holding` still runs `features deprecate` (P13/P14).
- `requests_session_steps.py` imports PLUGIN from the `migration_upgrade_steps.py` shim (P14 deletes the shim).
- The removed commands are still named in skills/bdd-red-green, formulating-features, migrating-to-capabilities,
  agents/bdd-implementer.md and README.md; `features_gherkin.locate/locate_in` are dead; CLAUDE.md's features row says
  'editing' (P14).

## Module-map rows

- `tests/scenarios/analysis_tools_handlers.py`, `analysis_tools_world.py` (renamed from analysis_tools_project.py),
  `batch_measurement_handlers.py`, `feature_file_tools_handlers.py`, `migration_tools_handlers.py`: each capability's
  generated-feature handlers. `scripts/features_edit.py` deleted.
