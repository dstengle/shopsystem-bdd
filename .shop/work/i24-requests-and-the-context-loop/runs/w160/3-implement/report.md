## Budget
scripts/workqueue.py

## Changes
`retry` and `withdraw` now share a helper `moved_to` in scripts/workqueue.py: it asks `workqueue_done.becomes`, moves, marks the initiative done and adds initiative.md to the commit. Plan contained no code.

## Red / green
Red: `python3 -m pytest -q --work-item w160` -> 1 failed (status_is: 'started' == 'done'), as the plan said (retry never ran the done check).
Green: same command after change, and tests/scenarios/test_work_queue.py + tests/scripts/test_work_withdraw.py: 6 passed.
Suite at start: 825 passed, 1 failed (this scenario) plus the brief's listed expected failures.

## Tests changed under an allowance
none

## Open questions
Per plan section 5: initiative.md with no status line; initiative already done when retry runs; retry to a non-green status (becomes expected to answer no). None chosen.

## Size
`tools size --limit 300`: no output (scripts/workqueue.py is 290 lines).

Commit: 9a83476. Files changed: scripts/workqueue.py. Concerns: none. D3: work run's green moves not changed.
