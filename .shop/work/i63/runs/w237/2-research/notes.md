# Notes: w237 (supervision r214, r215, r216)

Tools: `tools refs checkout_changes`: 0 references (misses `self.` calls). `tools tests-of` answers "no map", so every test list is `by search`. `tools size --limit 300` printed nothing (`run`). Prior notes (1-research) are stale: they predate commit d8f57cc8 (r218), which already changed `checkout_changes` (read, `git show d8f57cc8`; an ancestor of HEAD).

Accepted scenarios (features/supervision.feature): r214 line 1993, r215 line 2002, r216 line 2011. All three share one Given (lines 1997, 2006, 2015).

## 1. Why each scenario is red today

Command (`run`): `python3 -m pytest -q --work-item w237`. Result: 3 failed, 180 passed, 1 skipped. All three fail at the same Given, `StepDefinitionNotFoundError`, before any Then runs:
`every round ends and every worker gives DONE, and while i1's researcher works a session of i2 changes .shop/work/i2/initiative.md in the repository's own checkout without committing it`

Missing step definitions (`by search`; pytest stops at the first undefined step, so the Thens are unverified):
- Given (above): no match. Nearest, `two_sessions_change` (tests/scenarios/supervision_faults_steps.py:49), is the r218 wording, changes i1 and i2 both, and stores nothing in `context`.
- r214 Then "w1 is green, nothing recorded of w1 naming .shop/work/i2/initiative.md": no match. `is_green` (test_supervision.py:109) ends at `$`; `nothing_names` (faults_steps:59) says "names", not "naming".
- r215 Then ".shop/work/i2/initiative.md is as i2's session changed it": no match. The "is as it was" steps are for i1 only (test_supervision.py:153, faults_steps:122).
- r216 Then "no session of i1 or of i2 was taken as a fault": no match.
- r216 Then "w1 is not failed and p2 is not failed": no match. `is_failed` (faults_steps:103) needs "is failed, recording/naming".

Code behind them (`read`): the rule is already right. `Faults.checkout_changes` (scripts/supervise_faults.py:104-129) skips each other initiative's `.shop/work/<X>/` path (lines 110, 114), added by d8f57cc8. `Run.worker` (scripts/supervise_worker.py:189-199) raises a Fault only for paths `checkout_changes` returns. Once the steps exist, r214-r216 should hold for i1's researcher. Not verified: nothing ran past the Given.

## 2. Old assumptions

Requirements r214-r216 make one exception: a path under `.shop/work/<X>/` of another initiative X run side by side is not part of the checkout check.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_faults.py:Faults.checkout_changes (104-129) | skips other initiatives' paths (110, 114), since d8f57cc8; docstring says so | already the required rule; no change | supervision_faults_steps.py:35-46, test_supervision.py:158-164 (by search) | `refs` (0), text search "checkout_changes", read |
| scripts/supervise_worker.py:Run.worker docstring (169-177) | says every uncommitted `.shop/work/` change is put back and is the work-item's fault | stale for other initiatives' paths; the code already complies | none (docstring) | read |
| scripts/supervise_worker.py:Run.worker (187-199) | calls checkout_changes; raises a Fault naming what it returns | no Fault for another initiative's path; works through checkout_changes | every worker scenario (by search) | read, text search "checkout_changes" |
| scripts/supervise_all.py:run (46) | sets `run.group` to every open initiative's Run | the source of `others` in checkout_changes; unchanged | supervision_all_steps.py scenarios (by search) | read, text search "group" |
| scripts/supervise.py:Run.check (88-92) | refuses to start while any `.shop/work/` path is uncommitted (r46) | start-time check, not a session's; r214 says "while a session ... worked": unchanged | features/supervision.feature:825 (by search) | read |

Not affected (`read`): supervise_intake.py:Intake.check (45-49, same start-time refusal), supervise_answers.py:Answers.uncommitted (94-98) and ask (117-120), supervise_rounds.py:keep_round (266-275) and undo_round (240-250), supervise_merge.py (56-65, 117-124). Each handles only its own paths or a branch's tree. Tests: none (by search).

## 3. Tests the requirements make impossible to keep

Searched (`by search`: "put back", "checkout_changes", "i2/initiative", "another initiative" in tests/): no existing test asserts that another initiative's uncommitted path is put back. Checked:
- supervision_faults_steps.py:42-46 `another_session_changes` (i1's own path, deprecated scenario line 574): still holds; i1's path is not skipped. Sound.
- supervision_given.py:167-173 and test_supervision.py:158-164 (committed i2 file, scenario line 122): the file is committed, so checkout_changes did not put it back before either. Sound.
- supervision_faults_steps.py:103-112 `is_failed`: its git-status check excludes `.shop/work/i2`, consistent with r214. Sound.
- supervision_faults_steps.py:49-56 `two_sessions_change` (r218, not in w237's set): wants i2 left out and i1 put back. The code gives that. Sound.
- Result: none that the requirements make impossible to keep.

Open conflict for the plan (`read`; not decided here):
- Reading A (as written): `checkout_changes`, run for i2's own runs, does not skip i2's own path, since `others` holds only other runs (line 110). If an i2 session ends while `.shop/work/i2/initiative.md` holds the uncommitted change, that session puts it back and faults. The r216 Then "no session of i1 or of i2 was taken as a fault" then holds only if every i2 session ends before the write.
- Reading B: a change made by another initiative's session is no fault of any session of an initiative beside it, own sessions included. Nothing in the code records who made a change, so B needs a change in `checkout_changes` and a record of the writer.
- Timing (`read`): gate rounds are not among the rounds r95 runs one at a time, so i2's gate can run during i1's researcher. Whether it ends before or after the write depends on the stub's timing (tests/scripts/stub_claude.py:220-225); not run.

## 4. The file set

Must change:
- tests/scenarios/supervision_faults_steps.py (207 lines; room 93): new Given, storing i2's written text; four new Thens for r214-r216.

Production files: none under Reading A. scripts/supervise_faults.py (194 lines; room 106) already has the rule (d8f57cc8). The coordinator's answer names it, but rests on the stale notes. Under Reading B, `checkout_changes` changes: that file.

On the change's path, unchanged (line counts `wc -l`, `read`; room = 300 minus lines):
- scripts/supervise_worker.py (259 lines; room 41): Run.worker, calls checkout_changes (189); docstring (174-177) stale.
- scripts/supervise_faults.py (194 lines; room 106): checkout_changes, above.
- scripts/supervise.py (295 lines; room 5): Run.__init__ sets group (65). Do not add here.
- scripts/supervise_all.py (83 lines; room 217): sets run.group (46).
- tests/scenarios/test_supervision.py (269 lines; room 31): hosts `is_green` (109); the new Thens go in the faults steps, so unchanged.
- tests/scripts/stub_claude.py (282 lines; room 18): `elsewhere` write (220-225) the Given uses.

No tracked Python file is over 300 (`run`: `tools size --limit 300` printed nothing).
