# w231 implement report

## Budget
- tests/scenarios/supervision_merge_steps.py (new)
- tests/scenarios/test_supervision.py (one import line)

## What changed
New step module with three steps (Given p2 for a capability, Given integrate change list on two capabilities, Then p2's three lists as sets of ids) and its import in test_supervision.py. The p2 Given also writes `spec/capabilities/other.md`, since the supervisor refuses a change list naming a capability neither spec nor drafts have (r107). No production change.

## Red and green
- Red (research run, before my edits): `python3 -m pytest -q --work-item w231` -> 1 failed, 180 passed, 1 skipped; StepDefinitionNotFoundError on the p2 Given. Expected: the step was undefined.
- Intermediate reds after adding steps: first "named other, which neither spec/capabilities/ nor its drafts have" (setup), then my id regex matched `[other#r1,` (step bug). Both fixed in the steps.
- Green: `python3 -m pytest -q --work-item w231` -> 181 passed, 1 skipped. `tests/scenarios/test_supervision.py tests/scripts/test_supervise_change.py` -> 4 passed.
- Suite at start: 1065 passed, 2 failed (one of them this scenario) at 156d2b2b; the other failure (not a git repository) is not mine.

## Size
`tools size --limit 300` printed nothing.

## Tests changed under an allowance
none

## Open questions
Those the plan lists (duplicate ids across/within lists, status/Q&A of p2 after a merge, more than one proposal for a capability, no proposal for a capability). Also: the run's stderr in this scenario says the integrate round of p2 gave no change list (the stub default for p2's own round); the scenario does not assert on it.

## Plan code
The plan contained no code.

## Outcome
Someone can now rely on a scenario pinning that an integrate round merges its ids for another capability into that capability's held proposal. Surprise: the capability must exist in spec/. Commit: 4d09af70.
Files changed: the two above. Concerns: none.
