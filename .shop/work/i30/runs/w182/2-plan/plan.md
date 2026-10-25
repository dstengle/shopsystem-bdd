# Plan of w182: researcher limit of 80 turns, a branch review after a green fix, an initiative's done committed

Work-item: .shop/work/i30/w182.md, under supervision, accepts supervision#r19, r109, r110. Its Retires names the 40-turn r19 scenario. It has no `## Rulings`. The capability's frontmatter names no design-decision this work rests on beyond the requirements cited below.

## 1. What goes green

All are in features/supervision.feature and bound by tests/scenarios/test_supervision.py.

- **supervision#r19**, "a researcher is given the work-item's file set and accepted scenarios, and a limit of 80 turns" (line 405). Red at its last Then: the researcher's argv has `--max-turns 40`, because `MAX_TURNS` in scripts/supervise_worker.py gives research 40 (notes §1).
- **supervision#r109**, "an initiative set done is committed on the initiative branch" (line 1442). Red at an undefined Given ("i1 is started and its work-items w1 is green and w2 is withdrawn"). Its other Givens and both Thens also have no step: the delivered q2 request, "the analyzing-a-batch session writes i1's analysis record" (searched in tests/scenarios: not found), "the initiative branch has a commit of i1 with its status done" and "i1's file is not left uncommitted". In code, no `work run` path sets an initiative `done`: `pull_through` ends at `analyse()` (notes §1).
- **supervision#r110**, "when the work-item drafted for a kept branch review's findings turns green, the next branch review of the initiative is started before `work run` exits" (line 1461). Red at an undefined Given: the existing step has no "first … second" clause. The stub's plan is one result per agent, so it cannot give two reviews different results. In code, `pull_through` runs `branch_review()` once. A fix is pulled and the method returns (notes §1).
- **Retired:** "a researcher is given the work-item's file set and accepted scenarios, and a limit of 40 turns (deprecated)" (@r19 @deprecated, line 393). It is removed from the features file.

## 2. Where the change lands

Production:
- `scripts/supervise_worker.py`: `MAX_TURNS` for research goes from 40 to 80 (r19).
- `scripts/supervise.py`: `pull_through` becomes a review loop (decision 2). It calls the done step after the analysis branch (decision 4). `Run` takes the done part. Only a few lines change here, because the file has 40 lines of room.
- `scripts/supervise_done.py` (**new**): the run path's done. It holds r105's condition, the transition and its commit (decisions 3, 4). It is a part of `Run`, as `Analyses` is. It is a new module because the concern is new (CLAUDE.md) and supervise.py has little room.
- `scripts/supervise_analysis.py`: `analyse` commits the measurement and the analysis record it copied, then pushes (decision 5).
- `scripts/workqueue_done.py`: the existing condition (work-items, requests delivered) gets a public name that `supervise_done` calls. What it decides does not change.
- `CLAUDE.md`: a module-map row for `scripts/supervise_done.py`. This file is added to the researcher's set by decision 3.

Tests:
- `tests/scripts/stub_claude.py`: a plan entry for an agent may be a sequence, one result per session in order (decision 6).
- `tests/scenarios/supervision_proposal_steps.py`: the r110 Given (first review with two findings to fix now, second with nothing). The r110 Thens: one work-item drafted for the two findings and green, and a second bdd-branch-reviewer session started after it turned green, before the run's end. The r74 Given is rewritten (part 4).
- `tests/scenarios/supervision_done_steps.py` (**new**): the r109 Givens and Thens. These are the started initiative with w1 green and w2 withdrawn, the delivered q2 request, the analysis-record Given, the commit of i1 with its status done, and i1's file not left uncommitted. It is a new module because `supervision_given.py` (35 lines of room) and `supervision_then_workers.py` (21) are tight.
- `tests/scenarios/test_supervision.py`: one import line for the new steps module.
- `features/supervision.feature`: the 40-turn deprecated scenario (lines 393-404) is removed, per the Retires.

Removed from the researcher's set (read only, not edited): `scripts/supervise_review.py`, `scripts/supervise_draft.py`, `scripts/workqueue.py`, `scripts/supervise_pool.py` and `scripts/supervise_faults.py` (decisions 2 and 4 reuse them as they are). Also `tests/scenarios/supervision_then_workers.py`, `supervision_review_steps.py`, `supervision_given.py`, `supervision_request_steps.py` and `supervision_analysis_steps.py`: their existing steps stay as they are, and the new steps go in the two modules above.

## 3. Decisions

1. **r109 cannot go green without a done, so this work sets done.** r109 is "when `work run` sets an initiative's status to done". Its scenario reaches a done only if `work run` sets one. No code does today, and r105 (setting done) and r106 (the records committed, part of r105's condition) are accepted by w181 in i29. w181 is `awaiting-answer` and not merged into this base. So w182 carries the r105 condition and the r106 commit as far as r109 needs them. It follows w181's plan (.shop/work/i29/runs/w181/2-plan/plan.md, decisions 1, 5, 6, 7): the same modules, the same condition, the same commit. Whichever of the two merges second then meets the same intent. Rests on supervision#r109 and r105, r106.
2. **The review loop (r110).** After a kept branch review lists findings to fix now, `work run` drafts the fix (`fix_work_item`, as now) and pulls it. When that work-item turns `green`, `work run` goes back to the same branch-review step. That step verifies the push and logs `push verified` (r35, r51), and it starts the next review in a new `runs/branch-review/<n>/`. It loops until a review lists nothing to fix now or the fix does not turn green. When the fix does not turn green (awaiting-answer, failed, not pulled), no next review starts and the run ends as it does today. The analysis (r75) runs only after a review that lists nothing to fix now. Rests on supervision#r110, r74, r75, r35, r51.
3. **The run path's done condition.** The condition is the existing one in `workqueue_done` (at least one work-item, each green or withdrawn, every request this context asked that names the initiative delivered). Two more are added: the kept branch review lists nothing to fix now, as `lists_nothing` reads it, and the measurement and analysis record are committed. The command path's `_holds`, `becomes` and `mark` keep what they decide. Rests on supervision#r105 and work-queue r23.
4. **The done transition and its commit.** It mirrors `start_initiative`. `workqueue_done.mark` sets `done`, and a log line records the move to `done` by `work run`. `Run.commit` for the initiative commits `initiative.md` and `log.jsonl` on the initiative branch (message `work: <initiative> <before> -> done`), then pushes. It runs only after the analysis branch of `pull_through`, when decision 3 holds. Rests on supervision#r109, r105, r38.
5. **The records' commit.** There is one commit on the initiative branch, of the measurement `measure initiative` wrote and the analysis record copied into `.shop/records/`, then the push. Whether they are "committed" is read from git: the files are tracked at HEAD and unmodified. Rests on supervision#r106, r105, r38.
6. **The stub's per-session plan.** A plan entry may be a sequence. The n-th session of that agent gets the n-th entry, and sessions past the end get the last. The stub counts sessions per agent in a state file beside its calls log. A single entry, as every existing Given writes it, gives every session the same result, as today. This is test support only: it rests on r110's scenario, which needs two reviews to give two results.

## 4. Tests the decisions break

- **features/supervision.feature, the 40-turn r19 scenario (deprecated)** fails once `MAX_TURNS` is 80. It is removed, per the work-item's Retires.
- **r74 scenario (line 1027), its Given in tests/scenarios/supervision_proposal_steps.py (`reviewer_lists`).** Under decision 2, the fix it drafts turns green (every worker DONE) and a second review starts. With the plan unchanged, that review lists the same two findings again, a second fix is drafted, and the loop does not end. The Then `fix_drafted` (exactly one work-item) also breaks. The step is rewritten with decision 6 to give the findings to the first review session and nothing to fix now to the ones after it. The scenario still asserts what r74 pins: one work-item for the first review's findings, part of p1, naming its findings.md. The wording of the step stays.
- Verified sound, kept as they are:
  - `branch_reviewer` in supervision_then_workers.py asserts exactly one review start. It is used only by a scenario with no fix-now findings, so there is no second review there.
  - The other bdd-branch-reviewer plans (supervision_review_steps.py:24, supervision_analysis_steps.py:19 and :40, supervision_faults_steps.py:170) list no findings to fix now, so decision 2 starts no second review for them.
  - The `limit of {turns} turns` Then is parameterised.
  - The r75/r76 analysis steps assert only that the measurement, the record and the analyst session are there. A commit (decision 5) and a done (decision 4) change none of that. This is w181's verification, and these were read here.

## 5. Open cases (for the implementer to name, not to choose)

- A review that keeps listing findings after each fix turns green. r110 gives no bound, so the loop of decision 2 goes on as long as the fixes go green. Does anything in the run's budget stop it?
- The fix work-item turning `awaiting-answer` or `failed`: what the run prints. Decision 2 says no next review starts.
- The analysis session cut short or writing no record. The measurement is then written but uncommitted, and the done does not follow.
- A later run of an initiative whose records were committed earlier but whose request was delivered only since. Is `measure initiative` refused or written again, and how does decision 3 read it?
- The push after the records' commit or the done's commit failing (follow `Run.commit`'s push path).
- The merge with w181's branch, which adds the same new modules: an add/add conflict to resolve at merge, with the same intent on both sides.
- `work run` with no initiative printing an initiative it has just set done (r82).
