# plan of w240 (work-queue r62)

## 1. What goes green

- **work-queue#r62**: the Outline "a command whose change leaves an initiative with a green work-item, every work-item green or withdrawn, every capability-proposal formulated or withdrawn, and every request this context asked naming it delivered, sets the initiative to done" (features/work-queue.feature:92), six examples (withdraw ×5, retry ×1).
  Red today (notes §1): every example fails at its first undefined step, before any Then. No step definition matches `i1's capability-proposal p1 is <status>`, `i1's capability-proposal p1 is <status> and its capability-proposal p2 is <status>`, or `i1 has no capability-proposal`. The existing proposal Givens (work_queue_status_steps.py:14, work_queue_answer_steps.py:48) are phrased as part of the initiative Given and do not match. The notes found the code behind the Thens already in place (workqueue_done `_holds` refuses an open proposal; `moved_to` calls `becomes` for withdraw and retry). They inferred this from reading and did not run it.
- **Retired** (the work-item's Retires; both tagged `@r23 @deprecated`, features/work-queue.feature:60-89):
  - "a command whose change leaves an initiative with a green work-item, every work-item green or withdrawn, and every request this context asked naming it delivered, sets the initiative to done (deprecated)"
  - "retry that makes an initiative's last open work-item green again sets the initiative to done (deprecated)"

  These retire as the `work run` process retires deprecated scenarios. They have no proposal Given, so they still pass in the meantime (notes §2).

## 2. Where the change lands

- `tests/scenarios/work_queue_status_steps.py` (160 lines, room 140): the three new proposal Givens. Each writes a capability-proposal file in i1's directory with the given status (two files for the two-proposal form). The "no capability-proposal" form makes sure i1's directory holds none. This file comes from the researcher's set.
- `scripts/workqueue_done.py` (78 lines): `merged` comes out of the closed proposal statuses (decision D1). The module docstring is brought in line, so it says r62 and formulated or withdrawn. Added by D1.
- `tests/scripts/test_workqueue_done.py` (28 lines): the `merged` case of the parametrized test and the module docstring are rewritten (§4). Added by D1.

The following stay unchanged (notes §4): `scripts/work`, `scripts/workqueue.py` (294 lines, room 6: do not touch), `scripts/workqueue_request.py`, `scripts/supervise_done.py` and `tests/scenarios/test_work_queue.py` (the Outline is already bound).

## 3. Decisions

- **D1. A capability-proposal at `merged` is not closed for the done condition.** It holds its initiative from done, like any status other than `formulated` or `withdrawn`.
  - Rests on: work-queue#r62, which names only "`formulated` or `withdrawn`", and work-queue#r47, which says that if a proposal "is neither `formulated` nor `withdrawn`" `work` shall keep the initiative `started`. Together they settle the narrator's observation, so this needs no question.
  - Support: design-decision/workflow-capabilities-are-guarantees (0065) already turned the closed initiatives' `merged` proposals into `formulated` "so their closings stand". `merged` is a legacy status.
  - Verified: every proposal still at `merged` under `.shop/work/` belongs to an initiative from i1–i19. None of the started or proposed initiatives (i39, i45, i47–i49, i52–i56, i58–i62) has one. `becomes` skips an initiative already done. So no real initiative changes how it is observed.
- **D2. The shared rule stays shared.** `becomes` and `holds` keep serving request delivery (workqueue_request.py:246) and `work run`'s done (supervise_done.py:43) as well as withdraw and retry, with the same proposal clause. r62 speaks of "a `work` command's change", and request delivery is a `work` command (`work reply`/`resolve`). Supervision's done already shares this condition (its r105, cited in `holds`' docstring). This work changes no caller, so what the narrator sees through those paths stays as it is, apart from D1's `merged`. That is why the notes' question needs no ruling here.
- **D3. The new Givens are separate steps from the existing initiative Given.** They are not folded into it. The Outline gives them as their own `And <proposals>` line (work-queue r62 scenario). Following the existing proposal Givens, each proposal file carries kind `capability-proposal`, a `part_of` naming i1 and its status, so `_holds` reads it.

## 4. Tests the decisions break

- `tests/scripts/test_workqueue_done.py::test_an_open_proposal_keeps_the_initiative_from_done`, the `("merged", True)` case. D1 breaks it. It is rewritten to assert that `holds` is False for a `merged` proposal, alongside awaiting-answer, drafted and approved. The case is kept, not removed, because it pins r47 for the legacy status. The module docstring stops citing r23 and "nor merged" and cites r62 and r47.
- No other test breaks. The notes searched by name (no tools map exists) and found none: the r31 scenario, the r23 deprecated scenarios, supervision_done_steps.py and supervision.feature:1880-1890 have no proposal Given, so D1 and D2 leave them as they are. The formulated and withdrawn True cases and the open-status False cases of the test above still hold.

## 5. Open cases

- **Step-pattern overlap.** The single-proposal phrasing is a prefix of the two-proposal phrasing. A loose pattern for the first would also match the second, reading its status as "withdrawn and its capability-proposal p2 is formulated". The implementer must make the two step definitions match only their own form, and should confirm that with the red run.
- **Proposal file names and ids.** The scenarios do not say how p1 and p2 are named on disk or in their ids beyond "p1" and "p2". The implementer names them, following the existing proposal Givens.
- **A proposal at `merged`.** No scenario pins `merged` (or any other status) holding an initiative open on withdraw or retry. Only r47's own scenario and the unit test of §4 do. The implementer should say whether r47's scenario covers it.
- **The deprecated r23 examples.** They write no proposal, so the condition still holds for them. The implementer should confirm that on the run rather than assume it (the notes did not read their run status).
