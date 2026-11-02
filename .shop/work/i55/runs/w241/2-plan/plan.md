# Plan of w241 (supervision#r212, supervision#r213)

## 1. What goes green

- **supervision#r212**, scenario "when no node can make a transition, every work-item is green or withdrawn, no capability-proposal is awaiting-answer and no request whose asker is this context is in the asker's turn, `work run` exits successfully, printing each work-item's status". Not red today: the research run passes it; `supervise.py` `show` already gives exit 0 only when every status is green, withdrawn, formulated or merged, and exit 3 on awaiting-answer (notes §1, §2). It stays green; nothing is built for it.
- **supervision#r213**, scenario outline "an initiative whose work-items are <work-items> and whose capability-proposal is <p1>, its delivery otherwise closed, <set>". Red in one example, "w1 is green and w2 is withdrawn / withdrawn / is set done": the Given "i1's capability-proposal p1 is withdrawn" has no step definition (StepDefinitionNotFoundError). The step in `tests/scenarios/supervision_proposal_steps.py` (about line 110) matches only "is <status>, its adds|changes naming …". The code already counts `withdrawn` as closed (`workqueue_done._holds`, CLOSED_PROPOSAL), so the example is expected to pass once the step exists. The other three examples pass today.
- **Retired** (the work-item's Retires section), both removed from `features/supervision.feature`:
  - `@r9 @deprecated` "when every work-item is green or withdrawn and no request whose asker is this context is in the asker's turn, `work run` exits successfully, printing each work-item's status (deprecated)", replaced by r212's scenario;
  - `@r105 @deprecated` outline "an initiative whose work-items are <work-items>, its delivery otherwise closed, <set> (deprecated)", replaced by r213's outline.
  Every step these two use is used by the r212 and r213 scenarios too, so removing them leaves no step definition unused.

## 2. Where the change lands

- `tests/scenarios/supervision_proposal_steps.py`: a Given for a capability-proposal of i1 given with a bare status (no adds/changes clause), writing p1 with that status and the default content the existing step gives. Room 96 lines under the limit.
- `features/supervision.feature`: the two retired deprecated scenarios removed; nothing else in it changes.

Removed from the researcher's set: `scripts/workqueue.py` and `scripts/workqueue_request.py`. They were in it only under reading B of the notes' conflict; the decision below takes reading A, so neither changes. No production file changes.

## 3. Decisions

1. **r213 binds `work run`; `work withdraw` and `work resolve` keep their done condition** (the notes' reading A). r213's subject is `work run` ("When `work run` finds an initiative …"), and the `work` commands' own done condition is a separate requirement, work-queue#r62, which names green work-items, formulated-or-withdrawn proposals and delivered requests, and no branch review or records clause. Adding the review and records guard to `workqueue.moved_to` and `workqueue_request.resolve` would contradict work-queue#r62 and lies outside this work-item's `accepts:`. Rests on supervision#r213 and work-queue#r62.
2. **The new Given is a step of its own, not a widening of the existing step's pattern into an optional clause.** Either is open to the implementer as long as both phrasings bind exactly one step and `features` bindings stay clean; the step writes the proposal the same way the existing step does, so the r213 examples with `formulated` and `awaiting-answer, its ## Questions section …` keep binding where they bind today. Rests on supervision#r213 (its outline's Given at line 1911).
3. **No change to `workqueue_done.py`, `supervise_done.py` or `supervise.py`**: as read by the researcher, they already give r212's exit and r213's conditions (green, withdrawn, formulated-or-withdrawn proposals, kept review listing nothing, committed records, delivered requests). Rests on supervision#r212, supervision#r213.

## 4. Tests the decisions break

None. Verified from the notes §3: `tests/scripts/test_supervise_show.py` (3 tests) still holds under r212; `tests/scripts/test_workqueue_done.py` (6 cases) asserts merged and approved keep an initiative from done, as r213 requires; the withdraw and resolve tests (`work_queue_withdraw_steps.py`, `test_work_queue.py`) do not change since decision 1 leaves those commands as they are. The only tests removed are the two retired deprecated scenarios, by the work-item's Retires section.

## 5. Open cases

- Which statuses the new bare-status Given is meant to accept (the scenarios use only `withdrawn` bare): the implementer names whether it is limited to that or takes any status.
- Whether the bare Given and the step matching "awaiting-answer, its ## Questions section with …" could both match one line: the implementer names how ambiguity is ruled out.
- An initiative whose proposal is `withdrawn` and which `work withdraw` itself makes done (work-queue#r62) before `work run` sees it: no scenario here covers that path; it is left as it is.
