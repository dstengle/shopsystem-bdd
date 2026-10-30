# w239 research notes (requests r64)

Method: no coverage map (`tools tests-of` and `untested`: "no map"; I did not run `tools map`). Names via `tools refs`, which
misses `scripts/work` (an extensionless script): its call sites found by search. Tests found by search (by search).

## 1. Why each scenario is red today

- features/requests.feature:481 "list prints, with its date, each observation that the source of no initiative and of no request names" (r64)
  - Command (run once): `python3 -m pytest -q --work-item w239`
  - Result (run): 1 failed, 181 passed, 1 skipped, 56 subtests passed.
  - Failure (run): `StepDefinitionNotFoundError` for When "the session runs `work list`" (feature line 486).
  - Missing (read): no such step in tests/scenarios/requests_show_steps.py (only `runs_show`, `runs_status`).
  - Missing behind it (read, not run): `workqueue_list.listing` (scripts/workqueue_list.py:40) prints initiatives, requests and
    work-items only. The observation scan is `workqueue_status.uncited` (scripts/workqueue_status.py:112), called only by
    `status` (:160). After the step exists, Then "work prints o3 with its date" would fail.

## 2. Old assumptions

Requirement r64 moves the observation listing from `work status` (retired form, requests Retires r14, feature :468) to `work list`.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue_status.py:uncited | lists observations that no initiative's or request's `source` names | moves to `work list` (r64) | tests/scenarios/test_requests.py, retired r14 scenario (by search) | by search; tools refs uncited (1 ref, :160) |
| scripts/workqueue_status.py:status, text and `--json` with initiative None and report True | prints `observation <id> <date>` lines and an `observations` JSON key | stops printing them (retired r14); see question 1 | test_requests.py r14 scenario (by search) | by search; tools refs status (0 prod refs: scripts/work missed) |
| scripts/work:cmd_status (:66-67) | calls `status` for `work status` with no initiative | its observation output goes with status | test_requests.py r14 scenario (by search) | by search |
| features/requests.feature:468-478 r14 scenario | pins status printing o3 and not o1 or o2 | retired by the work-item's Retires | tests/scenarios/test_requests.py (by search) | read of Retires in w239.md |

## 3. Tests the requirements make impossible to keep

tests-of has no map: every entry is by search.

- tests/scenarios/test_requests.py, the r14 scenario "status with no initiative prints ... (deprecated)" (features/requests.feature:468-478):
  asserts `work status` prints o3 with its date and neither o1 nor o2. It fails once status stops printing observations
  (requirement r64, Retires r14). Its feature lines are removed with the Retires.
- Verified sound (by search, read):
  - tests/scripts/test_workqueue_list.py::test_list_json_gives_each_request_and_its_status_and_nothing_besides: asserts only
    `json["requests"]`; a new JSON key keeps it passing.
  - tests/scenarios/work_queue_list_steps.py: `gives_pairs` looks up named pairs only; no observation step.
  - tests/scenarios/work_queue_status_steps.py: no observation assertion.
  - scripts/migrate_session.py:24 (SessionStart hook) calls `open_text`, which calls `status(report=False)`: prints no observation.
    No test found that asserts observations at the hook (by search).
  - tests/scenarios/conftest.py: `observation()` is called only from scenarios that call it (by search); the repo fixture writes none.

## 4. The file set

Production:
- scripts/workqueue_list.py: `listing` prints `observation <id> <date>` for each uncited observation (text mode), from `uncited`.
- scripts/workqueue_status.py: `uncited` moves out (Retires r14); `status` drops its observation output and the `seen`/`report` path.
- scripts/migrate_session.py: edited only if `status`'s `report` parameter is removed (open_text passes report=False). Conditional.

Tests and features:
- tests/scenarios/requests_show_steps.py: add When "the session runs `work list`" (beside `runs_status`).
- features/requests.feature: remove the retired r14 scenario, lines 468-478 (Retires of w239).
- tests/scenarios/test_requests.py: no edit; its scenario binding goes with the feature edit.
- tests/scripts/test_workqueue_list.py: no edit; must keep passing.

On the change's path, not edited (line count `wc -l`; room under the 300-line limit of CLAUDE.md):
- scripts/work: 192 lines, room 108 (cmd_list :31, cmd_status :66).
- scripts/workqueue_list.py: 106 lines, room 194 (edited).
- scripts/workqueue_status.py: 170 lines, room 130 (edited; shrinks).
- scripts/workqueue.py: 294 lines, room 6 (read, frontmatter, requests, items; unchanged).
- scripts/migrate_session.py: line count not read (conditional edit).
- tests/scenarios/requests_show_steps.py: 72 lines, room 228 (edited).
- tests/scenarios/test_requests.py: 12 lines, room 288.

## Questions

1. Does r14's retirement (Retires of w239) remove observations from `work status` (reading A: `uncited` moves to list and status
   loses its observation lines and its `observations` JSON key), or keep them (reading B: list gains them, status unchanged,
   and only the r14 scenario is dropped)? The notes assume A, as the Retires section implies.
2. Should `work list --json` carry an `observations` key? r64 says "print" (text). The JSON test constrains neither reading.
