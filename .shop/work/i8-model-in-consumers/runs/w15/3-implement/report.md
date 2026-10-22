## Budget
- tests/scenarios/test_migration_tools.py
- tests/scenarios/migration_safety_steps.py

## Changed
- Step `it exits non-zero` renamed `it exits with an error` (same non-zero assertion).
- Given "a repository on the old system with decisions/0001-x.md ..." now calls `old.commit()`.
- No production change. The plan contained no code.

## Runs
- Red (not run separately by me: I applied both plan-decided test edits before running; the plan/notes record the red as StepDefinitionNotFoundError and FileNotFoundError). Honest gap.
- Suite at start: 586 passed, 17 failed at ae784c5 (all in test_migration_tools.py, the scenarios this item binds).
- Final: `python3 -m pytest -q --work-item migration-rebind-2` -> 23 passed. tests/scenarios/test_migration_tools.py -> 23 passed (the r5 scenario sharing the Given stays green).

## Size
scripts/measure 644, tests/scripts/test_measure.py 700: already over, untouched.

## Tests changed under an allowance
none

## Open questions
Plan section 5 cases (D1 enclosing repo, vanished tracked file, ignored files after reset, probe 5 double line): unchosen, no scenario covers them.

## Outside the file set
none
