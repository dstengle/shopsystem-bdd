# w244 plan: work-queue r47

## 1. What goes green

- work-queue#r47, scenario `features/work-queue.feature:93` "withdraw that leaves every work-item green or withdrawn while a capability-proposal is neither formulated nor withdrawn keeps the initiative started".
  - Red today: no. The research notes (part 1) say `python3 -m pytest -q --work-item w244` gave 182 passed, 1 skipped, 0 failed. That run includes this scenario's node in `tests/scenarios/test_work_queue.py`. Every Given binds. `work withdraw` calls `moved_to`, which calls `workqueue_done.becomes`. `_holds` in `scripts/workqueue_done.py` returns false while the capability-proposal p2 is `approved`, so the initiative stays `started`.
  - The notes say the run did not show this node's result on its own. They inferred the pass from zero failures and from reading the code. The implementer confirms the node passes by running it alone, and does not change anything.
- Deprecated scenarios retired: none. The work-item has no Retires section and no Rulings.

## 2. Where the change lands

The file set is empty: no production or test file changes. The researcher's file set was also empty, and no decision here adds a file.

The notes list the modules on the code path and their room under the 300-line limit. None of them is edited: `scripts/workqueue.py`, `scripts/workqueue_done.py`, `scripts/workqueue_request.py`, `scripts/supervise_done.py`, `tests/scenarios/test_work_queue.py`, `tests/scenarios/work_queue_withdraw_steps.py`, `tests/scenarios/work_queue_status_steps.py` and `tests/scripts/test_workqueue_done.py`.

## 3. Decisions

- No code change for r47. work-queue#r47 says an initiative stays `started` while a capability-proposal is neither `formulated` nor `withdrawn`. That is the condition `_holds` already checks, and work-queue#r62's condition for `done` already requires the same thing. The implementer runs the scenario, sees it green, and reports the work done with no change. It does not write a test that would only repeat what is already covered.
- Glossary-proposals do not keep an initiative open under this check. r47 names only capability-proposals (notes, part 2). This plan does not widen it.

## 4. Tests the decisions break

None. The notes (part 3) checked these and found them consistent with r47:
- `tests/scripts/test_workqueue_done.py::test_an_open_proposal_keeps_the_initiative_from_done`: approved, drafted, awaiting-answer and merged hold the initiative open; formulated and withdrawn do not.
- The r62 outline at `features/work-queue.feature:73-79`.
- `tests/scenarios/supervision_done_steps.py`.

No decision in this plan changes code, so no test breaks.

## 5. Open cases

- The scenarios do not say what happens to the initiative when the last open capability-proposal later becomes `formulated` or `withdrawn` after every work-item is already green or withdrawn. That is r62's case, from another command's change, and not this work-item's.
- The scenarios do not cover a capability-proposal in `awaiting-answer` or `merged` keeping the initiative open. The unit test covers those states; no scenario does.
