# Plan of w159: model check takes awaiting-answer proposals and withdrawn requests as the statuses they are

Work-item: .shop/work/i24-requests-and-the-context-loop/w159.md, accepts design-model-check#r27 (fix of branch review 1, F3). From the research notes at runs/w159/1-research/notes.md.

## 1. What goes green

design-model-check#r27 (a status missing or not in its kind's lifecycle is a file problem; and so on). Its five accepted scenarios in features/design-model-check.feature:

- **a status in its kind's lifecycle is no file problem** (outline, 2 rows): red, both rows.
  - Row "a work directory .shop/work/i1 has the part p1.md with the kind capability-proposal and the status awaiting-answer": red in the step. The Given "a repository in which {case}" (`malformed_record`, tests/scenarios/design_model_check_problems.py) has no branch for the row and fails its last assert. It is red in the code too: the capability-proposal's lifecycle in `STATUSES` (scripts/model_work.py) leaves out awaiting-answer, so `model check` prints `status 'awaiting-answer' is not one of ...` naming p1.md (probe P1).
  - Row "a request in .shop/work/requests/q1.md, of the form `work request` writes, has the status withdrawn": red the same way in the step. In the code, the request's lifecycle in `STATUSES` leaves out withdrawn, so `model check` prints a file problem naming q1.md (probe P1).
- **a malformed work directory or work file is a file problem** (9 rows): green today, and must stay green. The row "status built" keeps the capability-proposal's set closed.
- **a work-item accepting a requirement no scenario names is a file problem**: green today.
- **a work-item accepting a requirement of a guarantees capability that no scenario names is no file problem**: green today.
- **a green work-item accepting a retired id is no file problem**: green today.

The work-item retires no deprecated scenario.

## 2. Where the change lands

- `scripts/model_work.py`: add awaiting-answer to the capability-proposal's lifecycle and withdrawn to the request's lifecycle in `STATUSES`. `status()` and the other code that reads `STATUSES` stay as they are.
- `tests/scenarios/design_model_check_problems.py` (300 lines, so no room left): take the Given "a repository in which {case}" (`malformed_record`) out of this module and change nothing else in it. The module gets shorter. Any helpers and imports that only `malformed_record` used (such as `re`) leave with it.
- `tests/scenarios/design_model_check_records.py` (new): the moved `malformed_record` with all of its current branches, plus a branch for each of the two new rows. The awaiting-answer row writes an initiative i1 with a capability-proposal p1 in the status awaiting-answer, through the world's proposal and initiative helpers (tests/scenarios/conftest.py). The withdrawn row writes .shop/work/requests/q1.md in the form `work request` writes, in the status withdrawn, through the request-text helper of tests/scenarios/design_model_check_requests.py.
- `tests/scenarios/test_design_model_check.py`: one star-import line for the new module, among the other step modules.
- `CLAUDE.md`: no row needed. The module map has one row for `tests/scenarios/`, and that row covers the new module.

The researcher's set, with the new module named (the notes left the choice to the plan, see D2).

## 3. Decisions

- **D1. The two lifecycles take the statuses the glossary gives.** A capability-proposal may be awaiting-answer and a request may be withdrawn. No other status goes into either lifecycle, and no other kind's lifecycle changes. A capability-proposal in the status built is still a file problem. Rests on design-model-check#r27 ("a status ... not in its kind's lifecycle"), on the glossary in spec/index.md (a request's lines are "accepted, refused or withdrawn", and the statuses the glossary gives each kind), and on the scenario's own Pins line ("awaiting-answer a capability-proposal's and withdrawn a request's").
- **D2. `malformed_record` moves to its own module, not split.** The Given pattern "a repository in which {case}" can only be bound once, so the two new rows cannot get a second step with the same pattern somewhere else. design_model_check_problems.py is at the 300-line limit, so the whole step moves out to a new module. Rests on CLAUDE.md's size limit (no change pushes a file over 300 lines).
- **D3. The `done` rules do not change.** A done initiative with a kept withdrawn request of its own is still v_d1, because a withdrawn request is not `delivered`. `work`'s done condition (scripts/workqueue_done.py) stays as it is too. This settles the researcher's first question. design-model-check#r114 says "is not `delivered`", and that has one reading. This work-item does not accept r114. Making a withdrawn request close would need a change to r114 through its own request, not this fix. The narrator sees the same v_d1 as today.
- **D4. A work-item accepting a requirement its capability does not have stays a file problem.** This is what `model check` prints today (probe P2, W6), and the plan does not change it. This settles the researcher's second question. design-model-check#r27 covers a work-item that "accepts a requirement ... and no scenario names it yet", and no scenario names a requirement that does not exist. design-model-check#r9 makes a missing requirement an unresolved reference only when a scenario names it. design-model-check#r24 does not list `accepts`. The narrator sees the same output as today.

## 4. Tests the decisions break

None. Checked by the notes' search, by grep under tests/ for "is not one of", "awaiting-answer" and "withdrawn":
- No test asserts that an awaiting-answer capability-proposal or a withdrawn request is a file problem.
- tests/scripts/test_model_reading.py `test_failed_is_a_work_item_status` is about `failed` on a work-item, which D1 leaves alone. It keeps passing.
- tests/scripts/test_model_withdrawn.py, tests/scripts/test_model.py `WithdrawnTest`, and the design_model_check_requests.py request rows (v16a, v_d1, v_d3, v17) have no withdrawn request and no awaiting-answer proposal. They keep passing.
- D2 moves `malformed_record` without changing what it builds for its existing rows. So the scenarios that use it (the work-item file-name rows of r110, the record and decision rows of r29) keep their Givens. Running the whole feature after the move checks this.
- D3 and D4 change nothing.

## 5. Open cases

- Neither the scenarios nor the code give a `work` command that writes a request's status withdrawn (scripts/workqueue_request.py writes none). This work-item only makes `model check` accept the status. It does not make anything write it.
- A capability-proposal in awaiting-answer under a done initiative is still v_d1 (probe P2, D4), because awaiting-answer is not closed under design-model-check#r36. The scenarios do not cover this case.
- scripts/workqueue.py already lets a capability-proposal take awaiting-answer. After this change, `model` and `work` give a proposal the same statuses for awaiting-answer, but `work` still allows more than `model` does. The scenarios do not cover where else they differ.
