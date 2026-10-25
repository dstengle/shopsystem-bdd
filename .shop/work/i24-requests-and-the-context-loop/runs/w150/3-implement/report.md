## Budget
- scripts/supervise_draft.py
- tests/scenarios/supervision_proposal_steps.py

## Changed
- `Drafts.retires` expands accepted ranges with `model_parse.expand`.
- Step helper `named` keeps a trailing `-r<m>`.

## Runs
- Suite at start: 812 passed, 1 failed (the range scenario, the work-item's own).
- Red: `python3 -m pytest -q --work-item w150` -> 1 failed, 143 passed: the range scenario failed at the Then (the deprecated scenario was missing from Retires). Expected: equality match on `r3-r6` and the fixture reading it as `r3`.
- Green: same command after the change -> 2 passed (the work-item's two scenarios); test_supervision.py module run: 2 passed.
- Size check: no file printed.

## Tests changed under an allowance
none (the `named` helper is fixture setup; its single-id output is unchanged)

## Open questions
- A deprecated scenario with two @r tags in the accepted set is listed once per tag.
- Reversed/malformed range: follows `model_parse.expand`.
- Accepted entry of a capability other than `under`.

The plan contained no code. Commit: 6cee628.
Files changed: scripts/supervise_draft.py, tests/scenarios/supervision_proposal_steps.py.
