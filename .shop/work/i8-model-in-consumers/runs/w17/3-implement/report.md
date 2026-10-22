# Report

## Budget
- tests/scenarios/migration_ledger_steps.py
- tests/scenarios/test_migration_tools.py

## Changed
Two Then steps added: `its by has the qualifier "<q>"` (migration_ledger_steps.py; asserts q in `by`), and a stacked decorator for "spec/decisions/index.md is what `model decisions` would write" on the existing `model decisions --check` step (test_migration_tools.py). No production change.

## Red and green
Red: `python3 -m pytest -q --work-item migration-rebind-4` -> 3 failed, 4 passed; failures StepDefinitionNotFoundError for the two undefined steps (expected).
Green: same command -> 7 passed. test_migration_tools.py run: 7 passed.
Suite at start: 586 passed, 17 failed at 55f3ebd (the failing list in the brief, all in test_migration_tools.py).

## Tests changed under an allowance
none

## Open questions
D1: supersedes naming a decision not in the ledger is written in old form, rc 0. D2: entry with no source and a qualified supersedes gets a `by` starting `; supersedes`. The unused step "supersedes is {ident} alone" is left.

## Other
Plan contained no code. Size: scripts/measure 644, tests/scripts/test_measure.py 700 — already over, untouched.
Commit: a44d3c8. Files: the two above. Outside the file set: none.
