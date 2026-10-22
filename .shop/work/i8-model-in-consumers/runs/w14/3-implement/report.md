## Budget
- tests/scenarios/migration_safety_steps.py

## Changed
The Given "a repository on the old system whose spec/index.md gives the id {ident}" now calls old.commit() after writing spec/index.md.

## Runs
Red: `python3 -m pytest -q --work-item migration-rebind-1` -> 1 failed, 20 passed; the id-bounded-context/shop scenario failed on `assert data.get("id") == ident` (migrate refused the uncommitted tree, r15).
Green: same command -> 21 passed; tests/scenarios/test_migration_tools.py -> 21 passed.
Suite at start: 586 passed, 17 failed (all in test_migration_tools.py; that module passes 21 in my worktree).

## Tests changed under an allowance
tests/scenarios/migration_safety_steps.py Given (setup): added commit; no assert changed.

## Open questions
Index already bounded-context/<path>; reference-style Markdown links; moved path inside a longer path: not covered by scenarios, left unchosen.

Plan contained no code.
Size: scripts/measure 644, tests/scripts/test_measure.py 700 are already over (untouched).
Commit: 4da2253
