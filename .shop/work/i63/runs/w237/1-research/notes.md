# Notes: w237 (supervision r214, r215, r216)

Tools: `tools refs` ran (`checkout_changes`: 0 references, it misses the `self.` call; text search found the caller). `tools map` was never made: `tests-of` and `untested` answer "no map", so every test list below is `by search`. `tools size --limit 300` printed nothing (`run`).

Accepted scenarios (features/supervision.feature): r214 line 1993, r215 line 2002, r216 line 2011.

## 1. Why each scenario is red today

Command (`run`): `python3 -m pytest -q --work-item w237`. Result: 3 failed, 180 passed, 1 skipped. All three accepted scenarios fail at the same Given, with `StepDefinitionNotFoundError`:
`every round ends and every worker gives DONE, and while i1's researcher works a session of i2 changes .shop/work/i2/initiative.md in the repository's own checkout without committing it`

Missing step definitions (`by search`; pytest stops at the first undefined step, so the Thens are not yet run):
- the Given above: no match. Nearest is `another_session_changes` (tests/scenarios/supervision_faults_steps.py:42), which hard-codes i1's path and has no "every round ends" text.
- r214 Then "w1 is green, nothing recorded of w1 naming .shop/work/i2/initiative.md": no match. `is_green` (tests/scenarios/test_supervision.py:109) ends at `$`.
- r215 Then ".shop/work/i2/initiative.md is as i2's session changed it": no match. The two "as it was" steps are for i1 only (test_supervision.py:153, supervision_faults_steps.py:103).
- r216 Then "no session of i1 or of i2 was taken as a fault": no match.
- r216 Then "w1 is not failed and p2 is not failed": no match. `is_failed` (supervision_faults_steps.py:86) needs ", recording/naming".

Code behind them (`read`): the rule itself is wrong, not only the steps. `Faults.checkout_changes` (scripts/supervise_faults.py:104-125) leaves out only the group's own run directories (line 112) and matching log.jsonl lines (line 114). i2's initiative.md is neither, so line 121 `git checkout HEAD -- <path>` puts it back, and it is returned. `Run.worker` (scripts/supervise_worker.py:189-199) then raises a Fault naming it, for i1's researcher. Once the Given exists, r214 fails (fault names the i2 path), r215 fails (file restored) and r216 fails (fault raised).

## 2. Old assumptions

Requirement r214-r216 makes an exception: a path under `.shop/work/<X>/` of another initiative X run side by side is not part of the checkout check.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_faults.py:Faults.checkout_changes (104-125) | puts back every uncommitted path under .shop/work/ except own run directories and matching logs | must skip each path under `.shop/work/<X>/` for each other initiative X in `self.group` (r214, r215) | features/supervision.feature:574 (deprecated, i1's path, supervision_faults_steps.py:42) | read of the function; text search "checkout_changes", "put back" |
| scripts/supervise_worker.py:Run.worker (169-199) | calls checkout_changes (189) and raises a Fault naming each changed path (197-199) | unchanged code; no Fault for another initiative's path once checkout_changes leaves it out (r216) | features/supervision.feature:574, and the three accepted scenarios (red) | read; text search "checkout_changes" |
| scripts/supervise_all.py:run (46) | sets `run.group` to every open initiative's Run | unchanged; the fix needs each group member's `initiative` (scripts/supervise.py:50) | supervision_all_steps scenarios (`by search`) | read |
| scripts/supervise.py:Run.check (88-90) | refuses to start while any `.shop/work/` path is uncommitted (r46) | unchanged: a start-time check, not a session's (r214 says "while a session ... worked") | features/supervision.feature:825 (`by search`) | read |
| scripts/supervise_intake.py:Intake.check (45-49) | same start-time refusal as Run.check, for intake | unchanged, as above | none (`by search`: no test names it) | read |
| scripts/supervise_answers.py:Answers.uncommitted (94-98), ask (117-120) | per-item check on own paths; a session's changed tree paths | unchanged: own item only; the session's worker still goes through Run.worker | none (`by search`) | read |
| scripts/supervise_rounds.py:keep_round (266-275), undo_round (240-250) | commits or removes own stage directories and own log lines | unchanged: own paths only | none (`by search`) | read |
| scripts/supervise_merge.py (56-65, 117-124) | puts an implementer branch's changes under .shop/work/ back on the branch | unchanged: a branch's tree, not the main checkout | none (`by search`) | read |

The "found by" column records the search. `refs` found no caller of `checkout_changes`, so the caller was found by text.

## 3. Tests the requirements make impossible to keep

Searched (`by search`: "put back", "own checkout", "changed in the repository", "checkout_changes" in tests/): no existing test asserts that another initiative's uncommitted path is put back. Results:
- features/supervision.feature:574 (deprecated, i1's path; steps supervision_faults_steps.py:42-46, Then 103 and 108): still holds after the fix, since i1's path is not skipped. Sound.
- features/supervision.feature:122 (committed i2 file; steps supervision_given.py:168-173, test_supervision.py:158-164): the file is committed, so checkout_changes does not put it back today either. Sound, unchanged.
- features/supervision.feature:2021 (r218, not in w237's accepted set): wants the i2 path left out and the i1 path put back. The fix gives that. Its steps are undefined (no "a session of i2 changes" step found), so it is not run here.

Conflict for the plan (`read`, not decided here): i2's own path is not "another initiative's" for i2's own sessions.
- Reading A (as written): when an i2 session ends while `.shop/work/i2/initiative.md` still holds the uncommitted change, checkout_changes, run for i2, puts it back and faults that i2 session. The r216 Then "no session of i1 or of i2 was taken as a fault" then holds only if every i2 session ends before the write.
- Reading B: a change to a path made while another initiative's session worked is no fault of that initiative's sessions. This needs knowing who made a change. Nothing in the code records that.
- Timing (`read`): gate rounds are not among the rounds r95 runs one at a time, so i2's gate can run while i1's researcher works. Whether it ends before or after the write depends on the stub's timing; not run.

## 4. The file set

Production and test files the change touches:
- scripts/supervise_faults.py (190 lines; room 110): checkout_changes also skips paths under `.shop/work/<X>/` for each other initiative X in `self.group` (r214-r216). Found by read of lines 104-125.
- tests/scenarios/supervision_faults_steps.py (188 lines; room 112): one Given for i1's researcher working a session of i2, and four Thens for r214-r216, beside `another_session_changes` (line 42). Found by read; no existing step matches.

Modules on the change's path, unchanged:
- scripts/supervise_worker.py (259 lines; room 41): Run.worker calls checkout_changes (189) and raises the Fault (197-199). Unchanged.
- scripts/supervise.py (295 lines; room 5): Run.__init__ sets initiative (50) and group (65). Unchanged. Room is tight; do not add here.
- scripts/supervise_all.py (83 lines; room 217): sets run.group (46). Unchanged.
- tests/scenarios/test_supervision.py (269 lines; room 31): the scenario host for the existing steps. Unchanged.

Rooms are 300 minus the line count, from `wc -l` (`read`). No tracked Python file is over 300 (`run`).
