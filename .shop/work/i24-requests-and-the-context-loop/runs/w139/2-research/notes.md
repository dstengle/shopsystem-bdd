# w139 research: measure a finished initiative and start its analysis (r75, r76)

Method: `tools tests-of` answers "no map" (`tools map` not run: it is the suite's own run), so every test list is `by search`. `tools refs` not used (the names are CLI commands and methods). Read at HEAD 544c8d0 (the brief's base f890f2f exists; line numbers here are 544c8d0's). `git status --porcelain` clean at start and at the last check. Probe: `.shop/scratch/w139-2-research/probe_measure.py` (run). Stage 1 (`1-research/notes.md`) ran probes in a scratch directory no longer present; its results are marked "stage 1" below and were not rerun.

## 1. Why each scenario is red today

- **r75** `python3 -m pytest -q -n 0 "tests/scenarios/test_supervision.py::test_when_every_workitem_is_green_or_withdrawn_and_the_kept_branch_review_lists_nothing_to_fix_now_measure_initiative_is_run_on_the_initiative"` (run): `StepDefinitionNotFoundError`, Given at feature line 918 "every worker gives DONE, and the branch reviewer's result lists nothing to fix now". The only reviewer Given, `tests/scenarios/supervision_review_steps.py:21`, accepts `ends` or `writes findings.md beside its brief`. Then at line 920 "`work run` ran `measure initiative` on i1 after the branch review was kept" has no step. Code: `scripts/supervise.py` `Run.run` 189-195 runs `branch_review()` and the fix-work-item step, and nothing after; `grep measure|analy` over `scripts/supervise*.py` finds no line (run by search). `scripts/supervise_review.py` `Reviews.branch_review` 35-78 returns the kept directory and never reads its `result.json`.
- **r76** `...::test_once_measure_initiative_has_written_the_initiatives_measurement_a_session_of_analyzingabatch_writes_its_analysis_record` (run): `StepDefinitionNotFoundError`, Given at line 926 "every worker gives DONE, the branch reviewer's result lists nothing to fix now, and the analyzing-a-batch session writes i1's analysis record". Then lines 928 and 929 have no step either. Code: `scripts/supervise_worker.py` `Workers.session` 199-206 starts only `--agent shopsystem-bdd:<agent>` with `agents/<agent>.md`; `STAGES` (`supervise.py` 28-33), `TOOLS`, `MAX_TURNS` (`supervise_worker.py` 31-39) name no analysis stage; `analyzing-a-batch` is a skill (`skills/analyzing-a-batch/SKILL.md`), no agent (`ls agents/`). `tests/scripts/stub_claude.py` 173-176 refuses an `--agent` with no `agents/<name>.md` (read).

## 2. What the system answers today

Probe `probe_measure.py`, run, in a scratch repository with a `spec/index.md` naming `bounded-context/missingmass.io/shopsystem/shopsystem-bdd`, `.shop/work/i1/log.jsonl` (one line) and cwd at the repository root:
- `measure initiative i1` (first): exit 0, prints `.shop/records/measurements/2026-10-25-i1.md`.
- same day again: exit 1, `the measurement .shop/records/measurements/2026-10-25-i1.md exists; --replace writes over it`.
- `--replace`: exit 0.
- `git status --porcelain` afterwards: `?? .shop/records/`. Nothing committed.
- `measure show <record>`: exit 0; the stage table, work-items table empty (no transitions logged), totals.
- no `log.jsonl`: exit 1, `the initiative i1 has no log.jsonl`.
- `spec/index.md` missing: exit 1, `spec/index.md, which names the context, is missing`; with the file but no bounded-context id: exit 1, `spec/index.md gives no bounded-context id (bounded-context/<owner>/<product>/<context>)` (the second message is from the probe's first version, run).

Nearest cases of the work run, stage 1 runs, not rerun (the stand-in's plan and scratch repositories are gone):
- second `work run` on a finished initiative: no review, no session, exit 0, no measure (`probe_run.py::test_run_twice`).
- reviewer ending at its turn limit with no result: exit 0, `runs/branch-review/1/` kept with `brief.md` and an empty `session.json`, committed (D1).
- initiative whose work-items are all in its base commit: no review, no `log.jsonl`, exit 0 (D2).
- Read alongside those: `Reviews.branch_review` 39-40 returns `None` when no commit is unread, so `kept` is `None` and a hook keyed on `kept` does not run.
- The scenarios' own setups: `every worker gives DONE` sets the stand-in's `default` plan (`stub_claude.py`, `plan.get("default")`, read); the reviewer's `findings.md` Given exists (`supervision_review_steps.py:21-24`); the world writes `spec/index.md` (`supervision_given.py:33`, read). So the setups reach the review; what is missing is the two Thens and the reviewer "nothing to fix now" form.

## 3. Old assumptions

r75 and r76 add behaviour and replace none. The rows are places that assume the run ends after the branch review, or that a finished initiative is never measured twice.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise.py `Run.run` 189-195 | the branch review is the last step of an all-green run; the run then prints and exits | the measure hook goes after the review, and reads the kept review's result | by search: all-green lines of features/supervision.feature (72 lines name all-green or every-worker-DONE) | read, grep |
| scripts/supervise_review.py `branch_review` 39-40 | returns `None` at once when no commit is unread | a second `work run` of a finished initiative reaches no hook; a hook keyed on "a review was kept now" never retries a failed measure | by search: none assert a second run's measure; stage 1 `test_run_twice` (stage 1 run) | read, probe_measure |
| scripts/supervise_review.py `branch_review` 62-68 | keeps the reviewer's directory and commits it whatever the session ended with | r75 must read "nothing to fix now" from a `result.json` that may be absent | by search: `supervision_review_steps.py` 50-64 (kept directory's shape); stage 1 D1 | read, stage 1 run |
| scripts/supervise_draft.py `Drafts.fix_work_item` 60-66 | reads `result.json` `questions` as the fix-now list; a missing or unreadable file gives `False` silently | if r75 reads "nothing to fix now" the same way, a reviewer with no result passes r75 | none found by search (r74's steps not read here) | read |
| scripts/supervise_worker.py `Workers.session` 199-206 | every session is `--agent` of an existing `agents/<agent>.md` | r76 names a skill (`analyzing-a-batch`), not an agent | by search: the r76 scenario only (fails at its Given) | read, grep |
| scripts/supervise_worker.py `STAGE_SCRIPTS` 28-29, `TOOLS` 31-37 | a worker's Bash runs only pytest and `features`, `model`, `tools` by path | the analysis session runs `measure show` and `measure compare`, so `measure` must join its list (r14) | none (no test names STAGE_SCRIPTS: grep) | read, grep |
| tests/scripts/stub_claude.py 173-176 | refuses an `--agent` with no `agents/<name>.md` in the plugin directory | every all-green scenario starts the analysis session once r76 exists, and the stand-in refuses it | by search: every all-green scenario (the stand-in runs for each) | read |
| skills/analyzing-a-batch/SKILL.md Process 1 | the session runs `measure initiative <i>` itself | `work run` has written the measurement the same day, so the skill's step is refused (exit 1) | none | read, probe_measure |
| skills/analyzing-a-batch/SKILL.md Process 1 | `--sessions <dir>` adds the sessions around the initiative | `work run`'s measure takes no `--sessions`; the add-on needs `--replace` | none | read |
| skills/analyzing-a-batch/SKILL.md Process 4 | the session commits its report "with the measurement" | r7 commits only the work-item, its runs and `log.jsonl`; the measurement stays untracked (probe_measure `?? .shop/records/`) | none | read, probe_measure |
| tests/scripts/test_agents.py `test_r1_only_initiative_round_starts_an_agent` 41-43 | asserts the only agent with `Agent` or `Task` tools is `initiative-round` | a new analysis agent is checked by the same role test (conditional on its tools) | the test itself (read) | read |

## 4. Tests the requirements make impossible to keep

Searched by text (no map). Each row says what was verified.

- `tests/scenarios/supervision_review_steps.py` `verified_before_all` 82-91, the step "before each of w1's four workers was started, and before the branch reviewer was started...": it counts 5 `start` lines whose work-item defaults to `w1`, and expects the last to be `branch-review`. The branch review's start (`supervise_review.py` 61) logs no `work-item`, so it counts as w1. An analysis start logged the same way makes 6 and breaks it. Impossible to keep iff the analysis session logs a start with no `work-item` key (r8/r49 pattern). Conditional; read.
- All-green exit-0 scenarios (`test_supervision.py` 93-94, `exits_successfully`; r1, r9, the review family): they stay passing if an analysis failure is not a fault (the reviewer's failed session is not a fault today, `branch_review` ignores `returncode`), and break if it is. Read; not run.
- `tests/scenarios/test_supervision.py` `state` (`supervision_world.py` 139-146), used by "nothing in the repository has changed" (`test_supervision.py:197`): read. It compares every file outside `.git` and `git status --porcelain`. Refusals call it, and every refusal is raised in `check()` or before the hook (`run` 186-190), so the measurement file never exists in those runs. Sound (read).
- Sound (read): `supervision_faults_steps.py:104`, `supervision_review_steps.py:69` and `test_supervision.py:142`, `169`, `208` scope `git status` to `.shop/work`, `README.md`, the worktrees. The `.shop/records/` file does not reach them.
- Sound (read): `tests/scripts/test_measure_runs.py`, `test_batch_measurement.py` and its steps run `measure` in-process, through `measure_write.today` and `os.getcwd` monkeypatching; a subprocess hook in `work run` does not touch them.
- None found: no test counts the sessions of an all-green run other than `supervision_review_steps.py:54` and `:88` (by search: `len(` over `tests/scenarios/supervision*.py` and `tests/scripts/test_*.py`).

## 5. A step the work-item skips

- **The measurement's commit.** r7 commits the work-item file, its runs and `log.jsonl`; r38 only pushes. The measurement stays untracked (probe_measure, run). The skill's Process 4 says to commit the report "with the measurement". Read.
- **cwd.** `scripts/measure` takes its root from `os.getcwd()` (`scripts/measure` 51). `work run` must start it with `cwd` at the repository root. Read.
- **Refusals `work run` would meet.** No `log.jsonl`; no `spec/index.md` or no bounded-context id; a same-day measurement exists (probe_measure, run). A repeated `work run` meets the last one. r75 says nothing about a refused measure (part 8).
- **The analysis session, if it does not go through `Workers.session`.** It would skip what a worker gets: the brief (r2), start and end lines (r8), `session.json` with the transcript (r62), the push verification (r35), the copy into `runs/` and its commit (r47-r48, r15), the tool list and plugin directory (r11-r14). Read: `supervise_review.py` 41-77 and `supervise_worker.py` 149-206.
- **The worktree has no measurement.** The analysis worker's worktree is detached at the initiative branch's head (`supervise_worker.py` 127-141); `.shop/records/measurements/<date>-<i>.md` is untracked in the main checkout, so the worker reads it only by the main checkout's absolute path. Read.
- **The record's place.** A worker's new files are copied only where its result names them (`keep_named` 208-220; the record must be named in `result.json` or copied). Read.
- **Refusal only this step produces.** The stand-in's no-agent refusal (stub 173-176, stage 1 run). Effect only the measure produces: a `.shop/records/measurements/` file outside any commit (probe_measure, run).

## 6. Defects

D1. A branch review that ends with no result is kept and the run exits 0. Stage 1 run: `python3 -m pytest -q -s -n 0 .shop/scratch/w139-1-research/probe_noreview.py::test_reviewer_error_at_turn_limit` (not rerun; its scratch is gone). Output: exit 0; kept directory holds `brief.md` and an empty `session.json`; committed as "branch review 1 of i1". Read: r45 covers workers only; `branch_review` 62-68 keeps the directory whatever it holds. Whether a reviewer's failure is a fault is the person's reading.

D2. An initiative whose work-items are all in its base commit gets no branch review, no `log.jsonl` and no measurement, and exits 0. Stage 1 run (not rerun). Read: `unread()` 19-33 counts commits from the base to HEAD only. r75 needs a kept review, so it never fires here. Whether this is intended is the person's reading.

## 7. The file set

Changed for the scenarios to pass and for what passes today to keep passing:
- scripts/supervise.py: the measure hook after the branch review, when all green or withdrawn and the kept review lists nothing to fix now. Found by read of `run` and by grep (no `measure`).
- scripts/supervise_review.py: read the kept review's result (or a new module). Found by read of `branch_review` 35-78.
- scripts/supervise_worker.py: an analysis stage (agent or skill-loading worker) in `STAGES`/`TOOLS`/`MAX_TURNS`; `measure` in `STAGE_SCRIPTS`. Found by read of `session` and 28-37.
- tests/scenarios/supervision_review_steps.py: the "lists nothing to fix now" Given (line 21 accepts two forms); `verified_before_all` if the analysis logs starts. Found by run of the two scenarios and read.
- tests/scenarios/supervision_measure_steps.py (new): the r75 Then, the r76 Givens and Thens. A new module keeps the other files under 300 (CLAUDE.md's module map gets a row).
- tests/scenarios/test_supervision.py: bind the new step module (`from .supervision_measure_steps import *`).
- tests/scenarios/supervision_world.py: stand-in plan and record for the analysis session (if its steps live there).
- tests/scripts/stub_claude.py: accept the analysis session's `--agent` (no agent file if the plan names a skill session).
- Conditional: agents/<analysing agent>.md (new), with `skills: [shopsystem-bdd:analyzing-a-batch]`, if the plan picks an agent (then `test_agents.py` 41-43 applies); skills/analyzing-a-batch/SKILL.md if the plan changes Process 1 or 4.
- Conditional: a new module `scripts/supervise_measure.py` for the hook, with a row in CLAUDE.md's module map.

Modules on the change's path, edited or not (`wc -l` at 544c8d0; room to 300):
- scripts/supervise.py 228 (72); scripts/supervise_review.py 78 (222); scripts/supervise_worker.py 229 (71); scripts/supervise_draft.py 80 (220); scripts/supervise_pool.py 142 (158); scripts/supervise_brief.py 110 (190); scripts/work 147 (153); scripts/workqueue.py 282 (18, tight); scripts/measure 97 (203); scripts/measure_write.py 41 (259); scripts/measure_build.py 143 (157); scripts/measure_read.py 206 (94); scripts/measure_show.py 112 (188).
- Tests: tests/scripts/stub_claude.py 258 (42); tests/scenarios/supervision_review_steps.py 96 (204); tests/scenarios/supervision_world.py 173 (127); tests/scenarios/test_supervision.py 247 (53); tests/scripts/test_agents.py (if a new agent).
- `tools size --limit 300` printed no file over the limit (read of its output).

## 8. Readings the plan must choose (not decided here)

- **"lists nothing to fix now".** (a) `result.json` `questions` empty, the reading `fix_work_item` uses; `questions` also carries each Critical finding and each unverified check (the reviewer's contract). (b) `status` `DONE`, which also needs no Critical and every check verified. (c) `findings.md` with no finding triaged fix now. They differ when a Critical finding or an unverified check is the only thing listed. A review with no `result.json` (D1) is "nothing" under (a) as `fix_work_item` reads it, and not DONE under (b).
- **Where the analysis session's agent comes from:** a new agent file with `skills:` (then the stand-in's plan key is that agent's name), or a stage of an existing agent. The r76 Given names the session "analyzing-a-batch", so the plan key must match whichever is chosen.
- **Where the analysis record is written and how it reaches git:** r7 commits no file but the work-item's; the skill commits its report. The record may be named in the result, copied to the main checkout, or committed on the branch. Not stated by r76.
- **A failed measure or analysis session:** whether it is a fault (`work run` exits 1 and the work-item... none is named), or ignored as the reviewer's session is today. r75 and r76 are silent.
- **A second `work run` on a finished initiative:** should the measure run again (refused the same day, exit 1, unless the hook is keyed on "a review was kept in this run") or only when a review was kept in this run.
- **D2:** an initiative whose work-items are all in its base commit: no review, so r75 never fires. Intended or not is the person's reading.
