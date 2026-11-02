## Budget

- tests/scenarios/supervision_proposal_steps.py
- features/supervision.feature (features retire of two scenarios)

## Changed

- New Given `i1's capability-proposal p1 is withdrawn` (bare status, anchored with `$`; the other phrasings need a comma and a clause, so no ambiguity). Limited to `withdrawn`, the only bare status the scenarios use.
- Retired the two deprecated scenarios (r9, r105) with `features retire`; `features bindings` clean.

## Runs

- Red: `python3 -m pytest -q --work-item w241 -x` failed on the r213 example "w1 is green and w2 is withdrawn" (undefined Given, as the plan expected).
- Green: `python3 -m pytest -q --work-item w241`: 186 passed, 1 skipped, 56 subtests passed. `tests/scenarios/test_supervision.py` passes.
- Suite at start: 1089 passed, 0 failed (with expected failures listed in the brief, which include this r213 example).
- r212 scenario passed before any work, as the plan said (it is already green and not red-expected).
- `tools size --limit 300`: nothing over.

## Tests changed under an allowance

none

## Open questions

none (the plan's open cases: Given limited to withdrawn; no ambiguity with the comma phrasings; the withdraw-sets-done path left as is).

The plan contained no code. Commit: 153518ea.
