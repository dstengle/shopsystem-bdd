## Budget
- tests/scenarios/test_migration_tools.py
- tests/scenarios/migration_ledger_steps.py
- tests/scenarios/migration_spec_steps.py

## What changed
The feature file had been re-formulated (r2, r11, r12 wording) after scripts/migrate and its modules were built. Seven scenarios were red only because their step lines had no definition. I rewrote/added step definitions in the three test modules; scripts/migrate* needed no change (r12 `about` and the ledger fields were already implemented).

## Red and green
Red: `python3 -m pytest -q tests/scenarios/test_migration_tools.py` -> 7 failed, 19 passed; each failure StepDefinitionNotFoundError for a new Then/Given line (expected: the feature text changed, the steps had the old wording). Green: same command -> 26 passed.

## Suite records
Start: Suite: 570 passed, 7 failed at 7d9c2f3 in 118 s.
Final: Suite: 577 passed, 0 failed (1 skipped) at 9920c24 in 117 s.

## Tests changed under an allowance
tests/scenarios/migration_ledger_steps.py, the Given for the "title and its entries" ledger: setup (it now stores the ledger and the new "the entry's first paragraph" Given writes it); step wording of the Decision/summary Thens respelled to the feature's lines; tests/scenarios/migration_spec_steps.py, the old r12 about Given/Then replaced by the formulated ones. These are step definitions of this initiative's own scenarios.

## Open questions
none beyond the plan's section 5 (not exercised by any scenario; code leaves them unchosen).

The plan contained no code. 

## Outcome
`migrate run` now passes all 26 migration-tools tests. Surprise: the code was already complete; only the steps lagged the feature. Commit: 9920c24.
Files changed: the three above. Concerns: none.
