# Report of w200 implement 6: DONE

## Budget
tests/scenarios/supervision_rounds_steps.py, supervision_delegation_steps.py, supervision_formulate_steps.py.

## What changed
Added `formulate_did_its_work` (a formulate stand-in that commits features/thing.feature with a scenario tagged @r1, as a round that did its work does), used by the r83 formulate scenario's Given and the delegation scenario's Given. No feature line or Then changed. The r131 formulate row was already green and the deprecated outline already retired in 208bb0e9.

## Runs
Suite at start: 944 passed, 2 failed (the r83 formulate scenario and the delegation scenario). Red: both failed as the brief shows (p1 asked a question for the missing scenario instead of becoming formulated). Green: `python3 -m pytest -q --work-item w200`: 208 passed, 1 skipped; tests/scenarios/test_supervision.py: 64 passed.
size --limit 300: nothing printed.

## Tests changed under an allowance
- tests/scenarios/supervision_formulate_steps.py `formulate_no_question` (setup): stand-in now commits the scenario.
- tests/scenarios/supervision_delegation_steps.py `sessions_reply` (setup): same.

## Open questions
none

Plan contained no code pasted. Concerns: none.
