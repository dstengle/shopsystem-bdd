## Budget

- scripts/workqueue.py
- scripts/workqueue_done.py
- tests/scenarios/work_queue_add_steps.py

## Changed

- `workqueue.add` reads the initiative's initiative.md status (when the file exists) and refuses `done`/`abandoned`, naming it, before writing.
- `workqueue_done._holds` now needs at least one green work-item.
- New Then step `the add is refused because i1 is <status>, naming <status>` in work_queue_add_steps.py.

## Red and green

- Red: `python3 -m pytest -q -n0 --work-item w192` -> 3 failed (add[done], add[abandoned], withdraw r31). The add one failed on the Then: `returncode=0, stdout='w2\n'` (step written first); withdraw: `assert 'done' == 'started'`.
- Green: same command -> 147 passed, 1 skipped. Also tests/scenarios/test_work_queue.py, test_supervision.py, tests/scripts: 146 passed, 1 skipped.
- Suite at start (brief): 891 passed, 10 failed at ff6fe166; the 10 included these 3 plus supervision done/review tests, which I did not run as a whole suite.

## Tests changed under an allowance

none

## Open questions

- initiative.md with a missing/unknown status: add goes ahead (unchosen).
- `work run` drafting into an already done initiative now gets the refusal; unhandled.
- request resolve / retry / run on an all-withdrawn initiative now leave it unchanged.

## Other

Plan contained no code. Size check: `tools size --limit 300` printed nothing.
Commit: 678b2865.
Files changed: the three above. Concerns: none.
