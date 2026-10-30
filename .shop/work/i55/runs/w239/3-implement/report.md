## Budget

- scripts/workqueue_list.py
- scripts/workqueue_status.py
- tests/scenarios/requests_show_steps.py
- features/requests.feature (features retire only)
- tests/scenarios/test_requests.py (binding of the retired scenario, if it has one)

## Changed
`work list` now prints (text `observation <id> <date>` after work-items; JSON `observations` key) each uncited observation; `uncited` moved from workqueue_status.py to workqueue_list.py; `work status` no longer prints observations and lost its `report` parameter. Added When "the session runs `work list`", removed `runs_status`; retired the deprecated r14 scenario with `features retire`.

## Red/green
Red: test_list_prints_... -> StepDefinitionNotFoundError for When "the session runs `work list`" (expected: step undefined, list had no observations).
Green: `python3 -m pytest -q --work-item w239` -> 182 passed, 1 skipped. test_requests, test_work_queue, test_workqueue_list pass.
Suite at start (brief): 1087 passed, 1 failed (this scenario among the expected-failing list).
`tools size --limit 300`: no output.

## Tests changed under an allowance
none
## Open questions
Observation with no date line (prints None); no observations file; order of observation lines (put last); done/abandoned initiatives' sources count as citing.
The plan contained no code.
Commit: 49317acb
