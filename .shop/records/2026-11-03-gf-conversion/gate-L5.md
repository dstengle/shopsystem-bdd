# Layer 5 gate: the release (P14)

## Merged
- gfc/P14 (7fd8adb0) into gf-conversion, --no-ff, with no conflicts. P14 is alone in its layer. Its files outside its
  list are named in report-P14.md: scripts/features, scripts/model, model_work.py, features_gherkin.py, the model
  test fixtures, four scenario handler modules, an agent and two skills. All are accepted.
- `migrate upgrade` (dc05feed): .shop/plugin-version went from 0.25.0 to 1.0.0, and 1715 .shop/work files were rewritten.
  plugin.json is at 1.0.0.

## Shared changes made at the merge (P14's and P12's ask)
- The `work run` fault P12 found is fixed, test first, in tests/scripts/test_supervise_undo_round.py. When an
  integrate round's raise into an upstream was refused, `undo_round` removed the round's stage directory and left an
  empty `runs/<name>` behind. The initiative's next commit named that directory, and git refused it with
  "pathspec .shop/work/i1/runs/i1 did not match any files". `undo_round` now also removes `runs/<name>` when that
  leaves it empty. supervise_rounds.py has 297 lines.

## Gate (SHOPSYSTEM_GF unset)
- `python3 -m pytest -q`: 770 passed, 1 skipped, 0 failed.
- `tools size --limit 300`: exit 0.
- The P14 `model check` grep (v_p*, v15[g-k], v_t[4-6], v_s[1-3], v15f): no rows. model check itself exits 1 with
  52 violations, 16 warnings and 34 unresolved references. None of them is a row the conversion introduced. The rows
  left are v10a, v17, v_d1 and w_uncited_obs, as P14 reported.
- `model logic`: exit 0, with 7 L2 notes.
- `model restates`: 581 ids, 516 restated, 65 dropped, 0 pending, 0 missing, exit 0.
- `features generate --check`: exit 0.
- Common checks: `tools check` exits 0, ruff is clean on the changed files, and every scripts/*.py module has a
  CLAUDE.md row.

Result: the gate passes.

## Carried forward
- 25 open capability-proposals still use 0.29 lines and need re-integration: i45, i47, i52, i53, i55, i56, i58, i59
  and i61. They are listed in dc05feed.
- v16a's date cutoff stays. The codified design-model-check spec defines it (the `unrequested` condition, r14), so
  dropping it needs a spec change through a request.
- model check's remaining rows (v10a, v17, v_d1, w_uncited_obs) and its 34 unresolved references predate the
  conversion.
- Optional and not done: make the spec_grammar helpers public; the features_generate `resolve()` and Means fixes and
  vocab bind_all (gate-L3, gate-L4).
- P15 (the end-to-end test) and P16 (the live run) depend on this layer.
