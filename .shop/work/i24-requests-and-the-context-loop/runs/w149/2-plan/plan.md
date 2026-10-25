# Plan of w149: work turn on a delivered request leaves it delivered

## 1. What goes green

- **requests#r8**
  - "the upstream ending its turn with every line accepted, refused or withdrawn and one accepted sets the status to accepted": green today (notes part 1). It has to stay green.
  - "the upstream ending its turn on a delivered request with every line accepted leaves the status delivered": **red** today. `status_is` (tests/scenarios/requests_steps.py:71) gets `accepted` where it expects `delivered`. The upstream branch of `turn` in scripts/workqueue_request.py (lines 103-107) sets `accepted` or `refused` from the line outcomes whatever the status was before, so it overwrites `delivered`. The step definitions already exist.
- **requests#r9**
  - "the upstream ending its turn with every line refused or withdrawn sets the status to refused": green today. It has to stay green.

Deprecated scenarios retired: none (the work-item has no Retires section).

## 2. Where the change lands

- `scripts/workqueue_request.py`: in `turn`, when the upstream ends its turn, the step that sets the status from the line outcomes (r8/r9) runs only on a request whose status is not `delivered`. A delivered request keeps its status. Everything else on that path is unchanged: the turn still passes (r7) and the request is still committed (r12). The file is 131 lines, so there is ample room under the 300-line limit.

No file is added or removed. The researcher's set stands. The tests need no change: the scenario and its steps are already in features/requests.feature, tests/scenarios/test_requests.py and tests/scenarios/requests_steps.py.

## 3. Decisions

1. **When the upstream ends its turn on a `delivered` request, the status is left as it is. The turn still passes to the asker, and the request is still committed.** Rests on requests#r8 and requests#r9, which hold only for a request "that is not `delivered`", and on requests#r7 and requests#r12, which have no such exception.
2. **r17 is unchanged.** If the upstream passes a delivered request to the asker while one of its lines has an outcome that is unsettled, or none, `turn` still sets `awaiting-asker` as r17 says. r17 has no `delivered` exception, and this work-item accepts only r8 and r9. The guard covers only the r8/r9 branch.
3. **D2, the asker's `work turn` on a delivered request: unchanged.** It sets `awaiting-upstream`, because requests#r18 says that for every request whose turn passes to its upstream. The work-item does not accept r18, and it is not reread here. Consequence for the coordinator: in the real chain (resolve, then the asker's turn, then the upstream's turn) the request is no longer `delivered` when the upstream's turn ends, so r8 still sets it to `accepted` (notes part 2, D1 chain). This work-item fixes only the case its scenario pins: an upstream turn on a request still `delivered`. Closing the chain needs a new line under r18, which this plan does not write.
4. **D3, `work outcome` on a line number beyond the request's lines: unchanged, not decided here.** It concerns requests#r15, which w149 does not accept, and no scenario of w149 touches it. It stays as the researcher found it, reported for a later request or round.
5. **D4, a request with no lines: unchanged, not decided here.** It concerns requests#r1 to r3 and the vacuous case of r9. The vacuous case does not arise for a delivered request, since resolve needs an accepted request and an accepted request needs an accepted line. w149's scenarios do not cover it, so the behaviour stays as it is today (`refused`), reported for a later request or round.

## 4. Tests the decisions break

None. Verified from the notes (part 4, by search, since there is no coverage map): no test asserts that an upstream `turn` on a delivered request sets `accepted`. The other scenarios in features/requests.feature never call `turn` on a `delivered` request: r17 and r18 start from `awaiting-asker` or from no status, and r10 and r11 only resolve. test_work_queue.py, work_queue_start_steps.py, design_model_check_requests.py and requests_show_steps.py give their statuses directly and never reach them through `turn`. The red delivered scenario asserts the new behaviour and stays as written.

## 5. Open cases

- What the narrator sees when the upstream ends its turn on a `delivered` request whose lines are not all accepted (some refused or withdrawn). By decision 1 it stays delivered. No scenario pins it.
- Whether `work outcome` in the upstream's turn should write a line outcome on a `delivered` request at all. No requirement here refuses it.
