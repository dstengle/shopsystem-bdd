# w185 fix report

## Budget
scripts/supervise_rounds.py, scripts/supervise_change.py

## What changed
- An apply round's change list is checked with `unknown` (r107) against spec/capabilities/ and the drafts of the initiative's rounds (`runs=True`). An unknown capability keeps the round (keep_round), writes no list, keeps the status, and raises a Refused naming it.
- `rounds()` holds the first Refused, leaves the faulted proposal out (`due(left)`), runs the other proposals' rounds, then raises it after `draft()` and `pull()` (supervise.pull_through already does that).
- Stale docstring of supervise_change updated.

## Red/green
No scenario pins either fix, so there was no red run; the code was written without one. Final: `python3 -m pytest -q --work-item w185` -> 155 passed, 1 skipped. tests/scenarios/test_supervision.py + tests/scripts -> 154 passed, 1 skipped.
Suite at start: 897 passed, 0 failed at 507d361e.

## Tests changed under an allowance
none

## Open questions
- An apply list naming only other known capabilities still empties the proposal's lists (the answer covers unknown ones only).
- An unreadable apply change list is still ignored.

The plan contained no code. `tools size --limit 300` printed nothing.

## Commits
407107a3
