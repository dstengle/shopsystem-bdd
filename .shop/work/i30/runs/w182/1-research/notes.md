# Research of w182 (supervision r19, r109, r110)

Tools: `Scripts` = /home/vscode/shopsystem-bdd/scripts. `tools refs` worked. `tools tests-of` and `untested` have no map (`tools: no map: make one with tools map`); a map runs the whole suite, so none was made. Test lists below are `by search`.

Accepted scenarios (4, from features/supervision.feature):
- r19 80 turns (line 405)
- r19 40 turns, `@deprecated`, retired by w182 (line 393)
- r109 initiative set done committed (line 1372)
- r110 next branch review after fix turns green (line 1391)

## 1. Why each scenario is red today

Command for all four: `python3 -m pytest -q --tb=short -rfE` with the four node ids (`tests/scenarios/test_supervision.py::test_...`, found by `--collect-only -k`). Result: 1 passed, 3 failed.

- **r19 40 turns (deprecated)**: PASSES today (`--max-turns 40`). It must go: the work-item retires it.
- **r19 80 turns**: FAILS at the last Then, `the researcher was started with a limit of 80 turns` (tests/scenarios/supervision_then_workers.py:215-218). argv has `--max-turns 40`. Cause: scripts/supervise_worker.py:53-54 `MAX_TURNS = {"research": 40}`, read at :222. The file-set and accepted-scenario Thens come before it and are not reached as a failure (read, by order).
- **r109 set done committed**: FAILS `StepDefinitionNotFoundError` on Given line 1375, `i1 is started and its work-items w1 is green and w2 is withdrawn`. No step text matches (by search of tests/scenarios). Later steps unverified (pytest stops at the first undefined step), read only: line 1376 request Given (supervision_request_steps.py:20 has another wording); line 1379 `the initiative branch has a commit of i1 with its status done` and line 1380 `i1's file is not left uncommitted`: no matching step text found (by search).
  - Code missing: no `work run` path sets an initiative `done`. scripts/supervise.py:200-217 `pull_through` ends at `self.analyse()` (:213) and never calls `workqueue_done`. `mark` callers are supervise_rounds.py:121 (proposed to started), workqueue.py:251 (`moved_to`, the `work` commands) and workqueue_request.py:181. Run.move (supervise.py:111) calls `workqueue.move` (workqueue.py:142), which does not mark done.
- **r110 next branch review**: FAILS `StepDefinitionNotFoundError` on Given line 1395, `every worker gives DONE, the first branch reviewer's result lists two findings ... and the second lists nothing to fix now`. The defined step (tests/scenarios/supervision_proposal_steps.py:44) has no "first" and no "second lists" clause. Later steps, read only: line 1397 `one work-item was drafted ... and it is green` (proposal_steps.py:76 has other wording); line 1398 `after that work-item turned green a second session of bdd-branch-reviewer` (supervision_then_workers.py:268 has `after {name} was green`, and asserts exactly one review start at :274).
  - Code missing: scripts/supervise.py:207-213. `branch_review()` runs once per `pull_through`. A fix (`fix_work_item`, :209) is pulled by `pull(MOVABLE)` (:211), and the method returns. No second review. Plan is per agent (tests/scripts/stub_claude.py:184-190 keys by agent, round kind, question). It cannot give two different branch-reviewer results in one run, so the Given needs a per-session sequence.

## 2. What the system answers today

Probes run: the four scenarios above (command as in part 1). No further probes were written: the nearest cases below are `read`.
- r19 80: the researcher's argv has `--max-turns 40` (run, argv in the failure text).
- r110, read: after a fix turns green, `unread()` (supervise_review.py:19-33) sees new commits, so a review would be due, but `pull_through` never asks again.
- r110, read: `fix_work_item` (supervise_draft.py:58-81) dedupes by findings path. A second review writes runs/branch-review/2/findings.md, a new path, so a second fix would be drafted if its result lists questions.
- r109, read: `workqueue_done.becomes` (workqueue_done.py:41-48) checks the condition: a work-item, every one green or withdrawn, and requests kept here delivered. It does not check the measurement or analysis or the branch review, so the condition can hold before the analysis is committed.
- Nearest cases not given: the requests not delivered (read: `becomes` false, no done); no analysis record (read: analyse() prints and returns, supervise_analysis.py:63-72, so no done path).

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_worker.py:53-54 MAX_TURNS, read at :222 | researcher limit 40 | r19: 80. Change the value | 40-turn scenario (features:393, passes); 80-turn scenario (features:405, fails); by search | grep "turns\|40\|80" in scripts |
| features/supervision.feature:393-404 (40 turns, deprecated) | pins 40 | retired by w182 (Retires): remove the scenario | by search: that scenario only | Read of the features file, grep "limit of 40" |
| scripts/supervise.py:207-213 pull_through, one branch review per run | review once, fix pulled and run ends | r110: a fix that turns green starts a review in the same run | by search: r74 scenario (features:1001), not run; r110 (features:1391) fails | Read of supervise.py |
| scripts/supervise.py:209-213 fix path (`elif` skips analyse) | after a fix no analyse this run | the fix path must re-review, then analyse only on a clean review | by search: r74 (features:1001) and r110 | Read |
| scripts/supervise.py:213 and :200-217, no set-done | no initiative set done by `work run` | r109: set done after analysis, commit initiative.md | by search: r105 (features:1364) and r109 (features:1372), both fail | grep `workqueue_done` callers |
| scripts/supervise.py:101-104 Run.commit (includes initiative.md only when name is the initiative) | commit of initiative.md possible but unused | r109 commit of initiative.md, uses this path | none (no test calls the done path) | Read of supervise.py |
| tests/scripts/stub_claude.py:184-190, tests/scenarios/supervision_given.py plan[...] | one plan result per agent per run | r110 needs different results per session of bdd-branch-reviewer | by search: every given that sets plan["bdd-branch-reviewer"] (supervision_review_steps.py:24, supervision_proposal_steps.py:48) | Read |
| scripts/supervise_review.py:41-46 push verification, log "push verified" | verified before each branch review | the second review also must verify (r35, r51) | by search: supervision_review tests on the push verification | Read |
| scripts/supervise_draft.py:68-69 dedupe by findings path | one fix per findings file | sound for r110: the second review has a new path | by search: r74 scenario | Read |
| scripts/supervise_review.py:19-33 unread() | commits not read by a kept review | sound for r110: fix commits make a review due | by search: review tests | Read |

## 4. Tests the requirements make impossible to keep

Searched by `grep` (no map).
- tests/scenarios/test_supervision.py, scenario "...limit of 40 turns (deprecated)" (features:393): will fail once MAX_TURNS is 80. Remove it with the Retires (features file edit).
- tests/scenarios/supervision_then_workers.py:215-218 (`limit of {turns} turns`): parameterised, still sound for 80. Keep.
- tests/scenarios/supervision_then_workers.py:268-274 (`after {name} was green ... bdd-branch-reviewer`): asserts one review start and `green[-1] < review[0]`. Used by features:563 only (by search), which has no fix work-item, so it can still pass. Sound for that use. The r110 Then (features:1398) needs its own step: the one review count would break if reused.
- tests/scenarios/supervision_proposal_steps.py:76-83 (`fix_drafted`, asserts one work-item): used by features:1006 (r74 scenario). Under r110 with the stub's plan unchanged, the second review lists the same two findings again, so a second fix is drafted and the assertion `len(found) == 1` breaks; the run may also not end. The r74 scenario can no longer pass as written, unless its plan gives the second review nothing to fix (read, not run).
- tests/scenarios/supervision_review_steps.py:21-24 and supervision_proposal_steps.py:44-48 (plan per agent): sound for one review; cannot express the r110 sequence. Need a per-session plan.
- tests/scenarios/supervision_analysis_steps.py (r105, r106, r109 givens): r109 needs a step, not the existing ones, for the request and the done commit.

Verified sound (none else): the 40-turn Then and the 80-turn Then in the Outline sense; `unread()`; `fix_work_item`'s dedupe; the push-verification steps.

## 5. A step the work-item skips

- **Set done (r109)**: the existing way is `workqueue.moved_to` (workqueue.py:242-252), which puts initiative.md into the same commit as the move (`committed`, the `rels` with initiative.md when done). Its effects: the initiative's status and its commit. Run.commit can do the same (supervise.py:98-109) and pushes. Probed: no (read). Effects, read: the done check is `becomes`, which skips the measurement and analysis.
- **Second branch review (r110)**: the existing way before every review verifies the push (`git_push("--dry-run")`, supervise_review.py:41-46) and logs `push verified`. The fix path (supervise.py:209-211) pushes (`self.push()`) and pulls, and any new review started from there must do this step as well. Effects only the step gives: the `push verified` line in log.jsonl and the refusal r51 when the dry run fails. Probed: no (read).

## 6. Defects

None shown by a probe. Read only: the r74 scenario's stub plan and the r110 change interact (part 4). Not a defect today.

## 7. The file set

Production:
- scripts/supervise_worker.py: `MAX_TURNS` research 40 to 80 (r19). Read: :53-54, :222. 251 lines, room 49.
- scripts/supervise.py: pull_through loops a second branch review after a fix turns green (r110); after analysis sets done and commits initiative.md (r109). Read: :200-217. 260 lines, room 40.
- scripts/workqueue_done.py: `becomes`/`mark`, probably the condition a set-done step reads (r109). Read. 67 lines, room 233.
- scripts/supervise_review.py: read, the second review's push verification and `unread`. 82 lines, room 218. Probably not edited.
- scripts/supervise_draft.py: read, dedupe by findings path. 81 lines, room 219. Probably not edited.
- scripts/supervise_analysis.py: read, `lists_nothing`, `analyse`. 74 lines, room 226. Possibly edited (the set-done after analysis could go here).
- scripts/workqueue.py: read, `moved_to`, `move`. 290 lines, room 10. Probably not edited.
- scripts/supervise_pool.py: read, `pull` used by the fix path. 143 lines, room 157. Not edited.
- scripts/supervise_faults.py: read, `push`, `push_unpushed`. 161 lines, room 139. Not edited.

Tests (scenario steps and the stub):
- tests/scenarios/supervision_proposal_steps.py: steps for the r110 Given and Then wording, and the r74 scenario's `fix_drafted`. 116 lines, room 184.
- tests/scenarios/supervision_then_workers.py: step for the second review after a green fix. 279 lines, room 21. Tight: a new step may go elsewhere.
- tests/scenarios/supervision_review_steps.py: review plan sequence (first, second). 102 lines, room 198.
- tests/scenarios/supervision_given.py: the per-session plan. 265 lines, room 35.
- tests/scripts/stub_claude.py: per-session plan key (plan lookup :184-190). 270 lines, room 30.
- tests/scenarios/supervision_request_steps.py: the delivered request Given for r109. 29 lines, room 271.
- tests/scenarios/supervision_analysis_steps.py: r109 Then, `i1's file is not left uncommitted`, and the done commit step. 83 lines, room 217.
- tests/scenarios/test_supervision.py: scenarios bound, no change needed. 259 lines, room 41.

Features (not Python, no size limit): features/supervision.feature: remove the 40-turn deprecated scenario (features:393-404), per the Retires.

Spec: none changed by this research.

Size: `CLAUDE.md` limit 300; `wc -l` as above.
