# Plan of w163 (accepts supervision#r79, supervision#r84)

Finding: branch review 3's R3-F1 (`runs/branch-review/3/findings.md`). An integrate round that ends DONE leaves its stage directory `.shop/work/<init>/runs/<init>/<k>-integrate/` uncommitted, so the next `work run` is refused under r46.

The 3-plan stage ended `failed` on the fault the work-item records (the research probe repos changed in the checkout), not on an answer to its question. That question, who adds the failing scenario, is settled by the work-item itself (see Decision 1). So this plan does not ask it again.

## 1. What goes green

The four accepted scenarios all pass on base f890f2f today (notes §1: `4 passed`), and they stay green:
- r79 `features/supervision.feature:849` "a proposed initiative is given to an integrate round with the accepted lines of the request it fulfils".
- r79 `:857` "a proposed initiative that fulfils no request is given no integrate round, stays proposed and leaves nothing behind".
- r79 `:870` "a proposed initiative whose fulfils names a request the queue does not hold is given no integrate round, and nothing changes".
- r84 `:1056` "when `work run` starts the integrate round of a proposed initiative, the initiative is started".

The failing case is new, tagged @r84: "an integrate round that ends leaves nothing uncommitted and blocks no later `work run`". It is taken word for word from the findings' keep-as-test. Its steps are:
- the Given of q1, with lines 1 and 3 accepted and line 2 refused;
- every round ends;
- `work run i1`;
- then i1 is started, and nothing under .shop/work/ is left uncommitted;
- `work run i1` a second time;
- then the second `work run` was not refused.

It is red today in two places:
- At "i1 is started": the Then step is not bound. I searched `tests/scenarios/` and only Givens of that text exist (`supervision_all_steps.py:29,40`), not the findings' "every step exists already".
- Once that step is bound, at "nothing under .shop/work/ is left uncommitted": probe A (notes §2 A, §6 D1) gives `?? .shop/work/i1/runs/i1/`, and the second run exits 1 with r46's refusal.

Retires: none. The work-item has no `## Retires`.

## 2. Where the change lands

- `features/supervision.feature`: add the @r84 scenario above, next to `:1056`, as the work-item directs.
- `tests/scenarios/supervision_rounds_steps.py` (242 lines, room 58): a Then "i1 is started", the sibling of `i1_is_proposed` at `:126`. It reads `status: started` in `.shop/work/i1/initiative.md`. The other steps exist: `work_committed` at `:138`, `second_not_refused` at `:144`, and the second-run When at `test_supervision.py:72`.
- `scripts/supervise_rounds.py` (102 lines): in `Rounds.round`, on the DONE path of an integrate round, after its merge, commit the round's stage directory and its `log.jsonl` lines. `keep_round` does this on the fault path and `move` does it for the other kinds.
- `scripts/supervise.py` (247 lines, room 53): it holds the `commit` and `keep_round` helpers. Edit it only if the helper needs a message parameter it lacks.

Dropped from the notes' set:
- `supervise_brief.py`, `supervise_worker.py` and `workqueue_request.py`: they matter only to D2 and D3, which this plan does not take (§5).
- `supervision_world.py` and `test_supervision.py`: read only. `scenarios("supervision.feature")` binds the new scenario with no edit.

## 3. Decisions

1. **The failing scenario goes into `features/supervision.feature` as part of this work-item.** The work-item says to take the keep-as-test "as a scenario of r84 in features/supervision.feature if the formulation is needed, else ask". The formulation is needed, because the scenario is not in the file. So the instruction applies, and asking does not. This is the coordinator's direction under the person's delegation, and it counts as a ruling. The implementer adds the scenario first and sees it red before it changes code.
2. **On DONE, an integrate round commits its stage directory and `log.jsonl` in its own commit, after the round's merge, on the initiative branch.** `start_initiative`'s commit stays where it is, before the session.
   - It rests on supervision#r84 and the `:1056` scenario, which pins the `started` transition before the round's start in the log. Moving that commit after the round would put this at risk.
   - It rests on supervision#r46: a `work run` that exits 0 does not leave `.shop/work/` changes that refuse the next run.
   - It rests on r7: the commit takes the shape r7 gives a transition, stage directories and `log.jsonl` and nothing else, the shape `keep_round` gives on the fault path.
3. **The fault and non-DONE paths are not touched** (`keep_round`, r86–r88). The work-item says to research narrowly, on the one finding.

## 4. Tests the decisions break

None.
- Decision 2 adds a commit after a DONE integrate round, and no test asserts that the stage directory stays untracked. The notes (§4) searched `tests/` for `proposed`, `integrate` and `w_stale_intake`, and found no test that could no longer pass.
- `:1056` (`started_with_round`) reads the order of the log lines and the status in `initiative.md`. Decision 2 keeps `start_initiative` before the session, so both still hold.
- `:849` reads only the round's brief.
- `:857` and `:870` start no round, so the new commit never runs for them.

## 5. Open cases (for the implementer to name, not to choose)

- What the message of the DONE integrate commit says. Whether that commit pushes, as `start_initiative`'s does, or leaves the push to the next commit (notes §5).
- What the second `work run i1` does on a `started` initiative with no work-items (a second branch review, or nothing). The scenario only requires that it is not refused.
- D2 (notes §6): a faulted integrate round leaves the initiative `started`. It depends on whether r84's timing or r86's reading holds, so it is not taken here.
- D3 / review O9: a held request with no accepted line still gets an integrate round with an empty list of lines. It depends on how r79 is read, so it is not taken here.
- An integrate round's `questions` are dropped (`supervise_rounds.py:82`). No requirement covers them.
- A branch review may grade a `features/` change in a work-item commit as Critical. Decision 1 rests on the work-item's direction, and the implementer's report names it so the review can find that direction.
