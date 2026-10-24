# Report w130

## Budget
scripts/work, scripts/workqueue.py, scripts/workqueue_start.py (new), scripts/workqueue_done.py (new), scripts/workqueue_request.py, tests/scenarios/test_work_queue.py, tests/scenarios/work_queue_start_steps.py (new), tests/scenarios/work_queue_status_steps.py, CLAUDE.md (9 files)

## Changed
- `work start <request>` (workqueue_start.py): writes a proposed capability-change initiative `.shop/work/i<n>/initiative.md` fulfilling an accepted request, with its source; prints `i<n>`; not committed (D4).
- workqueue_done.py: the r23 condition; `work withdraw` and `work resolve` put initiative.md in their commit with status done when the change makes the condition true. `work run` does not (D7, reading B).
- Steps: work_queue_start_steps.py; CLAUDE.md rows for the two modules.

## Red / green
- Red: `python3 -m pytest -q --work-item w130 -n 0`: 5 failed. r22 `found == []` (no `start`); r23 outline (4 rows) first StepDefinitionNotFound, then after steps `'started' == 'done'`. Expected: no start, no done write.
- Green: same command: 147 passed, 1 skipped. Also test_work_queue.py, test_requests.py, tests/scripts: 146 passed.
- Suite at start: 752 passed, 5 failed (the 5 are these r22/r23 scenarios plus the listed others).
- `tools size --limit 300`: no output; nothing over.

## Tests changed under an allowance
- tests/scenarios/work_queue_status_steps.py `with_state` (Given step): setup only; it now also writes a second work-item named by "and whose work-item w2 is ready" (the existing parse step swallowed that tail). No assert changed.

## Open questions
- retry and answer do not run the done check: their moves (failed->before, awaiting-answer->ready) cannot make the condition true, no scenario asks.
- A request whose origin is `part_of` (not `source`) given to `start`: source written empty.
- `start` twice on one request makes two initiatives; an initiative with no initiative.md is never set done; uncommitted initiative.md after start (supervise refuses uncommitted .shop/work).
- `work resolve` done path has no scenario in this work-item; it is coded from D7 and the requests scenarios still pass.
- v_d1 and done initiatives leaving `work status`.

The plan contained no code. Someone can now run `work start qN` and get an initiative; `work withdraw` of the last open work-item completes the initiative.

Commit: a1b01eb. Files: those in the Budget. Outside the file set: tests/scenarios/work_queue_status_steps.py.
