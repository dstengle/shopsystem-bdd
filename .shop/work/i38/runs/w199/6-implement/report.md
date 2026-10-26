# w199 implement 6

## Budget
scripts/supervise_worker.py, tests/scenarios/supervision_given.py, tests/scenarios/supervision_then_workers.py, features/supervision.feature (retire only).

## Changed
- `outcome()`: a researcher's questions go to the planner's brief whatever its status word (r129 decision 4); only other agents' questions ask.
- New step "the planner gives <status>, asking ..."; "no worker was started for wN after the planner" accepted.
- Retired (features retire): the deprecated r32, r36, r37 researcher scenarios and the deprecated r5 researcher outline (red under decision 4, replaced). Removed the now-unused step researcher_asks (an allowance-changed setup step from part 1).

## Red/green
Start: suite record 3 failed (the r32/r36/r37 scenarios, undefined planner step). Red confirmed by that record (undefined Given); then the step, then decision 4: the deprecated versions went red as expected, and were retired.
Final: `python3 -m pytest -q --work-item w199`: 201 passed, 1 skipped. tests/scenarios/test_supervision.py --whole-suite: 253 passed.

## Tests changed under an allowance
none beyond part 1's (researcher_asks, now removed as unused).

## Open questions
none new. Plan contained no code.

## Size
`tools size --limit 300`: nothing printed.

Commit ae5da7ff. Files: 4.
