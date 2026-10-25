# w139 research: measure and analyse a finished initiative (r75, r76)

Method: no map (`tools: no map`), so `tests-of` and `untested` were not run; tests found by search. `tools refs` not used: the names are CLI commands and methods. Probes drove this worktree's `scripts/work` and `scripts/measure` with the stand-in claude (`tests/scripts/stub_claude.py`) in scratch repositories under `.shop/scratch/w139-1-research/`. The shell's PYTEST_ADDOPTS limits collection to w139's two scenarios; other scenarios are read, not run. Worktree HEAD is da6d815 (brief says base f890f2f); `git status` clean at start and end.

## 1. Why each scenario is red today

- r75: `python3 -m pytest -q -n 0 "tests/scenarios/test_supervision.py::test_when_every_workitem_is_green_or_withdrawn_and_the_kept_branch_review_lists_nothing_to_fix_now_measure_initiative_is_run_on_the_initiative"` (run). StepDefinitionNotFoundError at Given line 918, "every worker gives DONE, and the branch reviewer's result lists nothing to fix now". The reviewer Given accepts only "ends" or "writes findings.md beside its brief" (`tests/scenarios/supervision_review_steps.py:21`). Line 917 is defined. Behind it, Then line 920 "`work run` ran `measure initiative` on i1 after the branch review was kept" has no step (grep `measure` in `tests/scenarios/supervision_*.py`: none). Code: `scripts/supervise.py` `Run.run` lines 189-190 call `branch_review()` and nothing after it; no `measure` anywhere in `scripts/supervise*.py`; `scripts/supervise_review.py` `Reviews.branch_review` (35-77) never reads the kept `result.json`.
- r76: same command, `...::test_once_measure_initiative_has_written_the_initiatives_measurement_a_session_of_analyzingabatch_writes_its_analysis_record` (run). StepDefinitionNotFoundError at Given line 926, "every worker gives DONE, the branch reviewer's result lists nothing to fix now, and the analyzing-a-batch session writes i1's analysis record". Lines 928 and 929 (the Then steps) have no step either. Code: no analysis session in `scripts/` (grep `analy`: only `measure` text and `tools_env.py`). `supervise_worker.py` `session()` (199-206) starts only `--agent shopsystem-bdd:<agent>`; `agents/` has no analysing agent (`analyzing-a-batch` is a skill, `skills/analyzing-a-batch/`); `STAGES` (supervise.py 27-32), `TOOLS`, `MAX_TURNS` name no analysis stage. The stand-in refuses such an agent (probe_stub, run).

## 2. What the system answers today

- `probe_run.py::test_run_once` (run): work-items w1 green, w2 withdrawn, committed after the initiative's base; stand-in DONE. `work run i1`: exit 0, prints "w1 green / w2 withdrawn"; one session started, `bdd-branch-reviewer`; kept `runs/branch-review/1/` (brief.md, result.json, session.json) committed as "branch review 1 of i1"; `git status` clean; no `.shop/records/`. No measure.
- Nearest, run: `test_run_twice`: second `work run` starts no session, exit 0, no measure. `test_run_reviewer_not_done` (reviewer DONE_WITH_CONCERNS, questions empty): exit 0, no measure.
- Nearest, run `probe_noreview.py::test_reviewer_error_at_turn_limit`: reviewer ends at turn limit with no result: exit 0, same stdout, kept dir holds brief.md and an empty-stdout session.json, no result.json, committed (see D1).
- Nearest, run `probe_noreview.py::test_no_unread_commit_no_review`: work-items in the base commit: no review, no `log.jsonl`, no records, exit 0 (see D2).
- `measure initiative i1` alone (`probe_measure.py`, run, cwd = repo): first run exit 0, writes `.shop/records/measurements/2026-10-25-i1.md`; second same day exit 1 "the measurement ... exists; --replace writes over it"; `--replace` exit 0; no `log.jsonl` exit 1 "has no log.jsonl"; no `spec/index.md` exit 1 "spec/index.md ... is missing", nothing written.
- `measure` after a finished `work run` (`probe_after.py`, run): exit 0; `measure show` prints stages (branch-review row, no figures), work-items table empty (no transitions logged), totals 0; `git status --porcelain` shows `?? .shop/records/measurements/2026-10-25-i1.md`.
- Stand-in with `--agent shopsystem-bdd:analyzing-a-batch` (`probe_stub.py`, run): exit 1, stderr "no agent shopsystem-bdd:analyzing-a-batch in --plugin-dir"; no record, no result.

## 3. Old assumptions

Requirements r75 and r76 add behaviour and replace none; the rows are the places that assume the session or the review ends where it does today.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise.py `Run.run` 189-190 | branch review is the last step of an all-green run | the measure hook goes after it, and must not depend on a new review | by search: all-green scenarios of features/supervision.feature (r1, r9, r27-r51, r74-r76) | read, probe_run |
| scripts/supervise_review.py `branch_review` 39-41 | returns at once when no commit is unread | a second run of a finished initiative reaches the hook again, and `measure` refuses (exists) | none, by search: no test runs a second `work run` after a review | probe_run `test_run_twice`, probe_measure |
| scripts/supervise_review.py `branch_review` 65-74 | keeps the reviewer's directory and commits it whatever the session ended with | r75 must read "nothing to fix now" from a result that may be absent | supervision_review_steps.py scenarios (by search) | probe_noreview |
| scripts/supervise_worker.py `session` 199-206 and TOOLS/STAGES | every session is `--agent` of an existing agents/<agent>.md | r76 names a skill, not an agent | by search: the r76 scenario (fails at its Given) | read, probe_stub |
| tests/scripts/stub_claude.py 173-176 | refuses an agent with no file in the plugin directory | every all-green scenario starts the analysis session once r76 exists | by search: all-green scenarios | probe_stub |
| skills/analyzing-a-batch/SKILL.md, Process 1 | the session runs `measure initiative` itself | after r75 wrote the measurement the skill's step is refused the same day | none | probe_measure |
| skills/analyzing-a-batch/SKILL.md, Process 4 | the session commits its report "with the measurement" | r7 commits only the work-item, its runs and log.jsonl; the measurement stays untracked | none | probe_after |
| skills/analyzing-a-batch/SKILL.md, Process 1 | `--sessions <dir>` adds the sessions around the initiative | a `work run` measure has no `--sessions`; the skill's add-on needs `--replace` | none | read |

## 4. Tests the requirements make impossible to keep

Searched by text (no map). Each row says what was verified.

- `tests/scenarios/supervision_review_steps.py` `verified_before_all` (lines 82-91): counts 5 `start` lines whose work-item defaults to w1. A logged analysis start (the r8/r49 pattern, no work-item key) makes 6, and line 89 expects the last start to be branch-review. Impossible to keep iff the analysis session logs its start. Conditional, read. The count of 5 and the push-verified order are sound today (read).
- All-green scenarios that assert exit 0: `features/supervision.feature` line 208-213 (r9, "it exits successfully"), r1 (w1 and w2 green), and the review family. Under r76 the analysis session starts after the review; the stand-in refuses it (stub 173-176, probe_stub), `Run.run` 205-207 then exits 1 unless the session's failure is ignored, which today's `branch_review` also does for the reviewer (probe_noreview). Impossible to keep as they are unless the stand-in learns the analysis agent. Read, not run.
- Sound (read): `tests/scenarios/test_supervision.py:141` and `:207`, `supervision_faults_steps.py:104`, `supervision_review_steps.py:69`, `supervision_world.py:145` all scope `git status` to `.shop/work`, the worktrees or README; the `.shop/records/` file of a measure does not reach them.
- Sound (read): `tests/scenarios/test_batch_measurement.py` and its steps run `measure initiative` in-process; a hook in `work run` does not touch them.
- No test asserts a whole-repository `git status` after an all-green run: searched `porcelain` in `tests/`, none.

## 5. A step the work-item skips

- Commit of the measurement (r7 names the work-item, runs and log.jsonl only; r38 pushes only commits). Shown by probe_after: the measurement is `??` after `measure`. Read: the skill says the report is committed with the measurement, and the work-item's commits are the only ones `work run` makes on the initiative branch.
- The measure refusals work run would meet: no log.jsonl, no spec/index.md, measurement exists (probe_measure, run). Read: `measure` takes its root from `os.getcwd()` (`scripts/measure` 48), so `work run` must start it with cwd at the repository root.
- The analysis session, if it does not go through `session()`, skips what a worker gets: brief (r2), start and end lines in log.jsonl (r8, r49), `session.json` with the transcript (r62), push verification (r35, r51, as `branch_review` 41-45 does), the copy into `runs/` and its commit (r47, r48), the worktree removal (r15), the tool list and plugin directory (r11-r14). Read from `supervise_review.py` 41-77 and `supervise_worker.py` 199-206.
- Refusal only this step produces: the stand-in's no-agent refusal (probe_stub, run). Effect only it produces: `measure` writes a `.shop/records/measurements/` file outside any commit (probe_after, run).

## 6. Defects

D1. A branch review that ends with no result is kept and the run exits 0.
Reproduction: `python3 -m pytest -q -s -n 0 .shop/scratch/w139-1-research/probe_noreview.py::test_reviewer_error_at_turn_limit` (run). Stand-in plan: reviewer `result: none`, subtype `error_max_turns`. Output: `exit 0`, stdout `w1 green`, `w2 withdrawn`; kept directory holds `brief.md` and `session.json` only (empty); commit "branch review 1 of i1"; `git status` clean. Read: r45 covers workers only; r47 and r48 keep the directory whatever it holds. Whether a reviewer's failure must be a fault is the person's reading.

D2. An initiative whose work-items are all in its base commit gets no branch review, no log.jsonl and no measurement, and exits 0.
Reproduction: `python3 -m pytest -q -s -n 0 .shop/scratch/w139-1-research/probe_noreview.py::test_no_unread_commit_no_review` (run). Output: `RUN1 exit 0`, stdout `w1 green`, `w2 withdrawn`; no runs; no log.jsonl; no records. Read: r27 counts commits after the base; this may be intended. Flagged because r75 would never fire for it.

## 7. The file set

Changed for the scenarios to pass and for the passing to keep passing:
- scripts/supervise.py: call measure after the branch review, when all green or withdrawn and the kept review lists nothing to fix now. Found by read of `run` and by search (no `measure`). Room 82.
- scripts/supervise_review.py: read the kept review's result (questions, status) and say whether it lists fix-now findings. Read of `branch_review`. Room 223. Alternative: a new module `scripts/supervise_measure.py` (new concern, a row in CLAUDE.md's module map).
- scripts/supervise_worker.py: the analysis session (an agent or a skill-loading worker; a stage in TOOLS/STAGES/MAX_TURNS). Read of `session`. Room 71.
- tests/scenarios/supervision_review_steps.py: the "lists nothing to fix now" Given (line 21 accepts only two forms); verified_before_all if the analysis logs starts. Room 204.
- tests/scenarios/supervision_measure_steps.py (new): the r75 Then and the r76 Givens and Thens. A new module keeps the file under 300.
- tests/scenarios/supervision_world.py: stand-in plan and record for the analysis session. Room 127.
- tests/scripts/stub_claude.py: accept the analysis session (no agent file) or its named agent. Room 42.
- tests/scenarios/test_supervision.py: bind the new step module if one is made. Room 54.
- Conditional: agents/<analysing agent>.md (new) if the plan picks an agent; skills/analyzing-a-batch/SKILL.md if the plan changes Process 1 or 4.

Modules on the change's path, edited or not (lines, room to 300):
- scripts/work 147 (153); scripts/supervise.py 218 (82); scripts/supervise_pool.py 142 (158); scripts/supervise_review.py 77 (223); scripts/supervise_worker.py 229 (71); scripts/supervise_brief.py 110 (190); scripts/workqueue.py 279 (21, tight: any growth needs a split); scripts/measure 97 (203); scripts/measure_build.py 143 (157); scripts/measure_read.py 206 (94); scripts/measure_write.py 41 (259).
- Tests: tests/scripts/stub_claude.py 258 (42); tests/scenarios/supervision_review_steps.py 96 (204); tests/scenarios/supervision_world.py 173 (127); tests/scenarios/test_supervision.py 246 (54).
Line counts by `wc -l` at this checkout. Limit: CLAUDE.md, 300 lines.
