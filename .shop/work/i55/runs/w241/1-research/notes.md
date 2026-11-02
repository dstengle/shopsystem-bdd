# w241 research notes (supervision r212, r213)

Tools: `tools refs` ran; `tools tests-of` and `untested` found no map (not made, per brief). Tests and callers found by search, marked `by search`. Tool miss: `refs workqueue_done.holds` reports 0 references, but supervise_done.py:43, workqueue.py:249 and workqueue_request.py:246 call it (read).

## 1. Why each scenario is red today

Command (run once): `python3 -m pytest -q --work-item w241`
Result: 1 failed, 185 passed, 1 skipped (not identified), 56 subtests passed.

- r212, "when no node can make a transition ... exits successfully": passes (run). Not red.
- r213 outline, "w1 is green and w2 is withdrawn / withdrawn / is set done": FAILS (run).
  Undefined step at the Given "i1's capability-proposal p1 is withdrawn" (Line 1911): StepDefinitionNotFoundError.
  Missing: a step for a bare status. tests/scenarios/supervision_proposal_steps.py:110 matches only "is <status>, its adds|changes naming".
  Code behind it: workqueue_done.py `_holds` already closes `withdrawn` (CLOSED_PROPOSAL, :13, :34). Expected to pass once the step exists (read, not run).
- r213 outline, the other three examples: pass (run).

## 2. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue.py:moved_to (245-256) | on `work withdraw`, sets the initiative done when `workqueue_done.becomes` holds, with no branch review or records check | r213 makes done need a kept review listing nothing and committed records; the work command path skips both | none found by search | read; grep for `becomes(` |
| scripts/workqueue_request.py:resolve (246-251) | on `work resolve`, marks an initiative done when its last request becomes delivered, same condition | same as above | none found by search | read; grep for `becomes(` |
| scripts/workqueue_done.py:_holds (25-43) | every proposal formulated or withdrawn, at least one work-item green, every other work-item green or withdrawn, requests delivered; no review or records check | proposal and green rules already match r213; review and records are not in it (checked by callers) | tests/scripts/test_workqueue_done.py:20 (6 cases) by search | read |
| scripts/supervise_done.py:Dones.set_done (39-48) | checks records committed, then `holds`; marks and commits done | matches r213's records and conditions; the review check sits in its caller | none found by search (scenarios only, tests/scenarios/supervision_done_steps.py) | read |
| scripts/supervise.py:pull_through (232-242) | runs the branch review; `lists_nothing` and any green, then analyse and set_done | matches r213's review and green rules | r213 and r109 scenarios by search | read |
| scripts/supervise.py:show (249-268) | statuses include proposals; exit 0 only when all are green, withdrawn, formulated or merged; awaiting-answer gives 3 | matches r212's new clause (no awaiting-answer proposal) | tests/scripts/test_supervise_show.py:31, :37, :41 by search | read |

Conflict for the plan (both readings, no choice made):
- A: r213 binds `work run` only; leave `work withdraw` and `work resolve` as they are.
- B: r213 binds every path that sets an initiative done; then workqueue_done's condition needs the review and records checks for those two callers.
workqueue_done.py's docstring says it is "the part of `work run`'s done that the command's is too (r105)", which points to B.

## 3. Tests the requirements make impossible to keep

None found. Looked at:
- tests/scripts/test_supervise_show.py (3 tests, read): still pass under r212; no test asserts a done or exit without the awaiting-answer clause.
- tests/scripts/test_workqueue_done.py (6 cases, read): "merged" and "approved" keep the initiative from done, as r213's "formulated or withdrawn" requires.
- Work-queue withdraw and resolve tests (by search, `work_queue_withdraw_steps.py`, `test_work_queue.py`): no assertion that an initiative becomes done.
- The r212 and r213 scenarios: the accepted scenarios themselves, which the run covers.

## 4. The file set

Production:
- scripts/workqueue.py: only if conflict B is taken: the review and records guard on `becomes`'s callers. Found by read.
- scripts/workqueue_request.py: same as above, for `resolve`. Found by read.

Tests:
- tests/scenarios/supervision_proposal_steps.py: add a Given for a bare `i1's capability-proposal p1 is withdrawn` (writing p1 with status withdrawn). Found by the run (Line 1911 undefined step).

No change read as needed: scripts/workqueue_done.py, scripts/supervise_done.py, scripts/supervise.py (r212 and r213 already match the code as read).

Modules on the change's path (line count by `wc -l`; room under the 300 limit of CLAUDE.md; `tools size --limit 300` printed none over it):
- scripts/supervise.py: 295 lines, room 5
- scripts/workqueue.py: 294 lines, room 6
- scripts/workqueue_request.py: 253 lines, room 47
- scripts/workqueue_done.py: 78 lines, room 222
- scripts/supervise_done.py: 48 lines, room 252
- scripts/supervise_analysis.py: 80 lines, room 220
- tests/scenarios/supervision_proposal_steps.py: 204 lines, room 96
- tests/scenarios/supervision_done_steps.py: 84 lines, room 216
- tests/scripts/test_supervise_show.py: 41 lines, room 259
- tests/scripts/test_workqueue_done.py: 28 lines, room 272

Git status: clean at the end, apart from the stage directory.
