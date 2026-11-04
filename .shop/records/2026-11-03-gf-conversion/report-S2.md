---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-gf-conversion-report-s2
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: done
---

# Report S2: `migrate upgrade` stages its files in batches

Written by the layer 1 gate from the task's result, because the harness refused the subagent's write of this file.

## What changed

- `scripts/migrate_upgrade.py`: `BATCH = 500`. `apply()` writes every text first, then runs one
  `git add -f -- <chunk>` for each 500 paths, in `changes.texts` order. Its contract is unchanged.
- `tests/scripts/test_migrate_upgrade.py`: a new class `TheStaging` with two tests. The first is the plan's mocked
  batch test (1201 texts give adds of 500, 500 and 201). The second runs on a real git repository: three texts, one
  of them a tracked file, all appear in `git diff --cached --name-only`.

## Test runs

- Red first: `pytest -q tests/scripts/test_migrate_upgrade.py` gave 1 failed (1201 adds of 1 path each), 3 passed.
- Green: `pytest -q -n 4 tests/scripts/test_migrate_upgrade*.py --durations=5` gave 30 passed and 4 subtests in
  4.5 s. The setup of `test_migrate_upgrade_codified.py` is now about 3.3 s; it was 13.2 s.
- `tools size --limit 300` exits 0; ruff is clean on both files.

## Open

Nothing. The worktree started at main's head; the task reset `gfr3/S2` to gf-conversion (7694e5aa) first.
