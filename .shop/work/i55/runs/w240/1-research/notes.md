# research of w240 (work-queue r62)

No `tools` map exists: `tests-of` and `untested` refused ("no map"); not made. Tests named below are found `by search`. `refs` found no name for scripts/workqueue.py.

## 1. Why each scenario is red today

Command: `python3 -m pytest -q --work-item w240` (run, once). Result: 6 failed, 181 passed, 1 skipped (the plugin also ran other scenarios).

Scenario: features/work-queue.feature:92, the Outline "...sets the initiative to done" (@r62), 6 examples. Each fails at its first undefined step, before the Then steps:
- withdraw, p1 withdrawn and p2 formulated, request delivered: `Given "i1's capability-proposal p1 is withdrawn and its capability-proposal p2 is formulated"` undefined.
- withdraw, request names i2 and is accepted: `Given "i1's capability-proposal p1 is formulated"` undefined.
- withdraw, i1 has no capability-proposal: `Given "i1 has no capability-proposal"` undefined.
- withdraw, no request: `Given "i1's capability-proposal p1 is formulated"` undefined.
- retry, no request: `Given "i1's capability-proposal p1 is formulated"` undefined.
- withdraw, request asker another context accepted: `Given "i1's capability-proposal p1 is formulated"` undefined.

Missing: step definitions for the three proposal Given forms in tests/scenarios/ (none matches `i1's capability-proposal p1 is <status>`, `... and its capability-proposal p2 is <status>`, or `i1 has no capability-proposal`). The existing proposal Givens are `an initiative {ident} under .shop/work/ that is {state}, whose capability-proposal ...` (work_queue_status_steps.py:14) and `... whose capability-proposal {name} is {status}` (work_queue_answer_steps.py:48); neither matches.

Read, not run: the code behind the Thens is already in place. scripts/workqueue_done.py `_holds` (lines 34-35) refuses an open proposal, and `moved_to` (scripts/workqueue.py:246-256) calls `becomes` for withdraw and retry. The request Givens (work_queue_start_steps.py:22, :29) and the log Givens (test_work_queue.py:109) exist. Once the steps exist, the code should pass; this is inferred, not run.

## 2. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue_done.py:_holds, lines 13, 34-35 (CLOSED_PROPOSAL = formulated, withdrawn, merged) | refuses done while a proposal is not closed; also counts `merged` as closed | r62 names formulated or withdrawn only. `merged` is a conflict: drop it, or keep it and say so in the spec | tests/scripts/test_workqueue_done.py:test_an_open_proposal_keeps_the_initiative_from_done (asserts merged holds) | by search |
| scripts/workqueue_done.py:becomes, holds (callers: workqueue.py:moved_to, workqueue_request.py:246, supervise_done.py:43) | the proposal clause also holds back the done of a delivered request and of `work run` | r62 speaks of work commands; the request and `work run` callers now also need closed proposals (one reading: keep, as r62's rule is shared). Both readings to the person | none for a request delivery or `work run` with an open proposal (tests/scenarios/supervision_done_steps.py Givens have no proposal) | by search |
| scripts/workqueue_request.py:246-252 (request delivery ends the initiative) | ends the initiative when `becomes` says so | same as above; no test drives delivery with an open proposal | none | by search |
| features/work-queue.feature:60-89 (r23 deprecated scenarios) | pin done with no proposal condition | still hold: they have no proposal Given; deprecated, not removed by r62 | not confirmed (run status of these not read from the run output) | read |

## 3. Tests the requirements make impossible to keep

None found by search. `tests-of` unavailable, so searched by name: tests/scripts/test_workqueue_done.py (formulated and withdrawn True, open statuses False: sound under r62; `merged` True is the only point above), features/work-queue.feature r31 scenario (withdraw leaves started: sound, no proposal), r23 deprecated scenarios (sound, no proposal), tests/scenarios/supervision_done_steps.py and supervision.feature:1880-1890 (sound, no proposal given).

## 4. The file set

Must change:
- tests/scenarios/work_queue_status_steps.py (160 lines, room 140): add the three proposal Givens. Found by reading the existing Givens (above). Room is enough.

Conditional:
- scripts/workqueue_done.py (78 lines, room 222): change line 13 only if the `merged` reading is chosen.

Path modules, edited or not:
- scripts/work (192, room 108): entry; `withdraw`, `retry`. No change.
- scripts/workqueue.py (294, room 6): `moved_to`, `retry`, `withdraw`. No change; nearly full.
- scripts/workqueue_done.py (78, room 222): the condition. Conditional change above.
- scripts/workqueue_request.py (253, room 47): request delivery. No change.
- scripts/supervise_done.py (48, room 252): `work run`'s done. No change.
- tests/scenarios/test_work_queue.py (283, room 17): the Outline's binding. No change needed.
- tests/scripts/test_workqueue_done.py (28, room 272): no change needed.

Git status was not run in this session.
