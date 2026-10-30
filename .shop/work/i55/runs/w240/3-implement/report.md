# report of w240

## Budget

- tests/scenarios/work_queue_status_steps.py
- scripts/workqueue_done.py
- tests/scripts/test_workqueue_done.py
- features/work-queue.feature (only `features retire` of the two listed scenarios)

## Changed

- Three proposal Givens (one, two, none) in work_queue_status_steps.py.
- D1: `merged` no longer closed in workqueue_done.py; docstring cites r62/r47.
- test_workqueue_done.py: the `merged` case now expects False (listed in plan §4); docstring updated.
- Retired the two deprecated r23 scenarios with `features retire` (commit 521b2a43; their binding was a shared Outline binding, `features bindings` is clean).

## Runs

- Suite at start: 1087 passed, 6 failed (the r62 examples among them, plus the listed expected failures).
- Red: `python3 -m pytest -q --work-item w240 -x`: the r62 examples failed on the undefined proposal Givens, as the plan said.
- Green: `python3 -m pytest -q --work-item w240`: 187 passed, 1 skipped, 56 subtests passed. Also tests/scripts/test_workqueue_done.py and tests/scenarios/test_work_queue.py: 12 passed.
- `tools size --limit 300`: no output, no file over.

## Tests changed under an allowance

none (the `merged` case change is listed in the plan §4)

## Open questions

none. No scenario pins `merged` holding an initiative open on withdraw/retry; only the unit test does.

## Plan code

The plan contained no code.

## Outcome

Withdraw and retry now end an initiative only when every capability-proposal is formulated or withdrawn; the r62 Outline passes in all six examples.
