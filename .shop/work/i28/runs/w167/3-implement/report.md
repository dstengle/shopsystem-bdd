## Budget
- scripts/supervise_change.py
- scripts/supervise_draft.py
- tests/scenarios/supervision_integrate_steps.py
- tests/scripts/stub_claude.py

## Changed
- write_proposals: id is `capability-proposal/<context>/<initiative>-<capability>` (decision 1).
- draft_proposals: a proposal's existing work-items matched by the name segment of its id (stem fallback) (decision 2).
- stub_claude: `round:<kind>:<name>` plan key, over `round:<kind>`; docstring updated.
- steps: i2 proposed Given, two-initiative change-list Given, the two Thens.

## Red / green
- Red: `python3 -m pytest -q -n 0 --work-item w167` -> 1 failed: `AssertionError: ['capability-proposal/ex.com/prod/ctx/thing', 'capability-proposal/ex.com/prod/ctx/thing']` (equal ids; expected, code wrote no initiative name).
- Green: same command -> 144 passed, 1 skipped (after the id change). Also `tests/scenarios/test_supervision.py tests/scripts` -> 143 passed, 1 skipped.
- Suite at start: 860 passed, 1 failed (this scenario) at 23423e61.

## Tests changed under an allowance
none

## Open questions
Plan's open cases, left unchosen: a capability named twice in one list (second overwrites); a capability name with `/`; unchecked capability/requirement ids; initiative.md without an id; proposals already written under the old id form.

## Other
Plan contained no code. Size check: `tools size --limit 300` printed nothing. No outside-file-set edits.
Commit: 5fc3ed37.
