# w244 research: work-queue r47

Map: none (`tools tests-of` says "no map"); tests and callers found by search. `tools refs` ran on `workqueue_done.becomes` (0 refs, it misses in-function imports) and `holds` (nothing).

## 1. Why each scenario is red today

Scenario: features/work-queue.feature:93 "withdraw that leaves every work-item green or withdrawn while a capability-proposal is neither formulated nor withdrawn keeps the initiative started".

- Command run (run): `python3 -m pytest -q --work-item w244`
- Result (run): 182 passed, 1 skipped, 0 failed. The selection includes `tests/scenarios/test_work_queue.py::test_withdraw_that_leaves_every_workitem_green_..._keeps_the_initiative_started`.
- Outcome: not red. The run gives no per-node result, so this node's pass is inferred from the run's zero failures and from read (below), not seen directly.
- Read: Givens bind (`work_queue_status_steps.py:32 two_proposals`, `work_queue_status_steps.py:45 with_state`, `test_work_queue.py:98 last_for`). `workqueue.withdraw` calls `moved_to`, which calls `workqueue_done.becomes`. `_holds` returns False at `workqueue_done.py:35` on the approved p2, so `initiative.md` stays `started`.
- Missing: nothing found in the step definitions or in `scripts/workqueue_done.py` for this scenario. The premise that it is red does not hold on this checkout.

## 2. Old assumptions

none. r47 replaces no existing form; it keeps a state the code already reaches. Searched: `workqueue_done._holds` (only capability-proposal kind blocks, `workqueue_done.py:34`), callers `workqueue.py:249`, `workqueue_request.py:246`, `supervise_done.py:43`, `supervise_rounds.py:262`. Glossary-proposals are not blocked; r47 names only capability-proposals, so this is not a conflict.

## 3. Tests the requirement makes impossible to keep

none. Looked, by search (no map), at:
- `tests/scripts/test_workqueue_done.py::test_an_open_proposal_keeps_the_initiative_from_done` (read): six rows, approved/drafted/awaiting-answer/merged false, formulated/withdrawn true; matches `holds` and r47. Sound.
- `features/work-queue.feature:73-79` r62 outline (read): formulated and withdrawn rows still reach done; the r47 branch does not change them.
- `supervision_done_steps.py` (read): its initiative has only glossary-proposals, which r47 does not touch.

## 4. The file set

Production: none to change; the scenario's code path already works (see part 1).

Tests: none to change; the accepted scenario and the r47 unit test already cover it.

Modules on the path, edited or not (`wc -l`, room under the 300 limit from CLAUDE.md):
- scripts/workqueue.py: 294 lines, room 6 (withdraw/moved_to).
- scripts/workqueue_done.py: 78 lines, room 222 (`_holds`, `becomes`).
- scripts/workqueue_request.py: 253 lines, room 47 (delivered path).
- scripts/supervise_done.py: 48 lines, room 252.
- tests/scenarios/test_work_queue.py: 283 lines, room 17 (binds the feature).
- tests/scenarios/work_queue_withdraw_steps.py: 64 lines, room 236.
- tests/scenarios/work_queue_status_steps.py: 183 lines, room 117 (Givens for proposals).
- tests/scripts/test_workqueue_done.py: 28 lines, room 272.

`tools size --limit 300` printed no file over the limit (run).

Git: `git status --porcelain` was empty at my first check; the stage directory is the only thing I wrote.
