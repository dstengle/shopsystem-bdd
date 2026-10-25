# Plan of w139: work run measures a finished initiative and starts its analysis

Work-item `.shop/work/i24-requests-and-the-context-loop/w139.md`, under `supervision`, accepting supervision#r75 and supervision#r76. No `## Retires`, no `## Rulings`. The stage-1 researcher stopped at its turn limit. Stage 2's notes (`runs/w139/2-research/notes.md`) are the ones this plan works from.

## 1. What goes green

- **supervision#r75**, "when every work-item is green or withdrawn and the kept branch review lists nothing to fix now, `measure initiative` is run on the initiative". It is red today because the Given "every worker gives DONE, and the branch reviewer's result lists nothing to fix now" has no step. The only reviewer Given (`supervision_review_steps.py:21`) accepts `ends` or `writes findings.md beside its brief`. The Then "`work run` ran `measure initiative` on i1 after the branch review was kept" has no step either. In the code, `Run.run` (`supervise.py` 189-195) stops after the branch review and the r74 fix step, and nothing in `scripts/supervise*.py` runs `measure` (notes §1).
- **supervision#r76**, "once `measure initiative` has written the initiative's measurement, a session of analyzing-a-batch writes its analysis record". It is red today because its Given (line 926) and both Thens (lines 928 and 929) have no steps. Also, `analyzing-a-batch` is a skill, not an agent, and `Workers.session` starts only `--agent` sessions of an existing `agents/<agent>.md`. The stand-in `claude` refuses any other (notes §1, §3).
- Deprecated scenarios retired: none. The work-item has no `## Retires`.

## 2. Where the change lands

- `scripts/supervise.py`: in `run`, once a branch review was kept in this run, and only when it lists nothing to fix now (decision 1), the new analysis step runs. This is in place of the r74 fix step, never as well as it. `Run` gains the new mixin, and its docstring names it.
- `scripts/supervise_analysis.py` (new): the concern of r75 and r76, one mixin of `Run`:
  - reads whether the kept review lists nothing to fix now;
  - runs `measure initiative <initiative>` as a subprocess from the repository root;
  - starts the analysis session in a detached worktree of its own with one brief;
  - copies the analysis record into the main checkout.

  It is a new module because this is a new concern (CLAUDE.md), and `supervise.py` (228 lines) has too little room.
- `scripts/supervise_worker.py`: a stage `analysis` in `TOOLS`. Its list is Read, Glob, Grep and Bash of `python3 <scripts>/measure *` only (decision 4). It is not added to the shared `STAGE_SCRIPTS`, because that would give `measure` to every stage, against r14. The new agent also gets an entry in `ROLE`.
- `agents/batch-analyst.md` (new): the analysis session's agent (decision 3).
- `CLAUDE.md`: a row in the module map for `scripts/supervise_analysis.py`.
- `tests/scenarios/supervision_analysis_steps.py` (new). It holds:
  - r75's reviewer Given;
  - r75's Then;
  - r76's combined Given, which sets the plan of the stand-in's `batch-analyst` to write a record file beside its brief, using the stand-in's existing `notes` mechanism;
  - r76's two Thens.

  It is a new module so that `supervision_review_steps.py` and `test_supervision.py` stay small.
- `tests/scenarios/test_supervision.py`: binds the new step module with a star import, beside the others.
- `tests/scripts/stub_claude.py`: claimed but expected to stay unchanged. The new agent file satisfies its no-agent refusal (173-176), because the plugin directory is this repository. It is claimed only in case the plan key or the `notes` mechanism does not reach the analysis session as it reaches the reviewer.

Dropped from the researcher's set: `scripts/supervise_review.py`, `tests/scenarios/supervision_review_steps.py` and `tests/scenarios/supervision_world.py`.
- `supervise_review.py`: the reading of the kept review's result lives in the new module.
- `supervision_review_steps.py`: the new Givens are whole sentences of their own and do not touch the regex at line 21. Also, `verified_before_all` is not broken (§4).
- `supervision_world.py`: its helpers (`starts`, `work_item_of`, `log_lines`, `write`) are enough.

## 3. Decisions

1. **"Lists nothing to fix now" means the kept review's `result.json` is readable and its `questions` list is empty or absent.**
   - It is the field r74's `fix_work_item` reads the fix-now list from. r74 and r75 then read one list: a list with lines drafts a fix (r74), and an empty one measures (r75). A result whose questions name no work-item still lists something, so it is not measured.
   - A kept review with no readable result lists nothing at all. It is not "nothing to fix now", so there is no measure. design-decision/worker-results-are-files makes a missing or malformed result a failed stage, not a result that lists nothing.
   - Rests on supervision#r74, supervision#r75 and design-decision/worker-results-are-files.
2. **The measure is triggered by a review kept in this run.** `branch_review()` returns that review's directory. A later `work run` with nothing unread keeps no review, so it does not measure again.
   - r75 is an event ("When … its kept branch review lists nothing"). 0068 starts the measurement "when the initiative's work is done", once.
   - `analyzing-a-batch` counts running `measure initiative` again over an existing measurement as a mistake, because the transcripts may be gone. So `work run` never passes `--replace` or `--sessions`. A same-day measurement that already exists is refused, and then there is no analysis (r76 needs "has written").
   - Rests on supervision#r75, supervision#r76 and design-decision/the-context-runs-without-a-coordinator.
3. **The analysis session is a `claude -p --agent shopsystem-bdd:batch-analyst` session.**
   - The new agent lists `skills: [shopsystem-bdd:analyzing-a-batch]`. Its tools are Read, Glob, Grep, Bash, Write and Skill: no Edit and no Agent. Its model is opus, as for the other judging roles. Its text tells it to write its result file first, with `PARTIAL`, and keep it current.
   - r12 already lets it load its skill, by `Skill(shopsystem-bdd:analyzing-a-batch)`.
   - The stand-in's plan key for "the analyzing-a-batch session" is `batch-analyst`.
   - Rests on design-decision/the-v3-agents (each role is an agent with its own tools and model; only `initiative-round` has Agent), supervision#r11, supervision#r12 and supervision#r76.
4. **What the session is given.** It is started through `Workers.session` with stage `analysis`, in a detached worktree at the initiative branch's head, like the reviewer's.
   - Its tools are r14's: `measure` by path, and no git command, because it commits nothing (decision 5).
   - Its brief is one file in the worktree's `.shop/scratch/analysis/`. The brief:
     - names the initiative, the scripts directory, its worktree, its run directory and its result file;
     - names the measurement by its absolute path in the main checkout, and the main checkout's `.shop/records/measurements/` for `measure compare`;
     - says the measurement is already written, so the session reads it with `measure show` and does not run `measure initiative`;
     - asks for the analysis record as `analysis.md` in the run directory, and says not to commit it;
     - has no `Work-item:` line.
   - Rests on supervision#r2, supervision#r11, supervision#r14, supervision#r17, supervision#r44 and design-decision/worker-results-are-files. `skills/analyzing-a-batch/SKILL.md` is left as it is: the brief overrides its Process steps 1 and 4 for this session.
5. **Where the record goes, and what is committed.**
   - When the session ends, `work run` copies the `analysis.md` from its run directory, if it wrote one, to the main checkout's `.shop/records/<date>-<initiative>-analysis.md`. The date is the measurement's date, and the place is the one the i22 analysis record has.
   - The measurement and the record stay uncommitted, as `measure` leaves its record today. The analysis session logs no line to `log.jsonl` and leaves no directory under `.shop/work/`. Its worktree and scratch are removed with the run's (r33).
   - The reasons:
     - r27 and r50 would start a new branch review for any commit on the initiative branch other than a review's own commit. A committed record would therefore set off a review, a measure and an analysis on every later `work run`.
     - r46 refuses the next run if `log.jsonl` under `.shop/work/` is left uncommitted.
     - r8 and r49 log the workers of work-items and the branch reviewer, and neither is this session.
   - Rests on supervision#r27, supervision#r50, supervision#r46, supervision#r8, supervision#r49 and supervision#r33.
6. **A refused measure or a failed analysis session is not a fault.** The work-items are all green or withdrawn, so `work run` exits as r9 says (0).
   - It writes to stderr why the measure was refused (its message) or what the analysis session ended with, and that no record was kept. Stdout stays r9's statuses.
   - The same holds for the branch reviewer's session today. A failed analysis is not a work-item's stage, so r42 and r45 do not apply.
   - Rests on supervision#r9.
7. **No push verification before the analysis session.** r35 names the work-items' workers and the branch reviewer, and this session pushes and commits nothing. Rests on supervision#r35 and decision 5.

## 4. Tests the decisions break

None. What was verified:
- `supervision_review_steps.py` `verified_before_all` (82-91) counts `start` lines in `log.jsonl`. Decision 5 logs none for the analysis session, so the count stays 5. The notes give this as conditional; it is not triggered.
- Every all-green scenario whose reviewer's result is readable and has no questions now also runs `measure` and starts the stand-in `batch-analyst`. The result:
  - Exit 0 stays (decision 6).
  - `.shop/records/` is untracked in the test repository. The scoped `git status` checks (`supervision_faults_steps.py:104`, `supervision_review_steps.py:69`, `test_supervision.py` 142/169/208) do not reach it, and `state()` is used only by refusals, which happen before the review (notes §4).
  - The commit-subject checks (`test_supervision.py` 110/122, `supervision_parallel_steps.py` 113, `supervision_faults_steps.py` 109, `work_commits`) see no new commit.
  - `work_item_of` gives None for the analysis brief, because it has no `Work-item:` line. So `supervision_parallel_steps.py` 136/141 are unaffected.
  - `reviewer_calls` filters by agent, so the counts at `supervision_review_steps.py:54` hold.
- `tests/scripts/test_agents.py`:
  - r1 holds, because the new agent has no Agent or Task.
  - r2 lists named agents only, and the new one has no Edit anyway.
  - r5's expected map does not list it.
  - `ResultFirst` names four agents.
- `test_measure_runs.py` and `test_batch_measurement.py` run `measure` in-process. A subprocess started by `work run` does not touch them (notes §4).

## 5. Open cases (for the implementer to name in the report, not to choose)

- How the r75 Then shows "after the branch review was kept". One possibility is the measurement listing the review's session from `log.jsonl` together with the kept directory. Another is the order of the stand-in's calls and the measurement file.
- How r76's first Then shows "once `measure initiative` had written": the measurement exists, and the analysis brief names it.
- Whether the stand-in's default `DONE` reviewer writes a result with no `questions`, so that every all-green scenario reaches the measure. Run the suite and name the scenarios that now do.
- A review kept with no result (notes D1): no measure under decision 1, and `work run` exits 0 as today. Whether that should be a fault is the person's call, outside this work-item.
- An initiative whose work-items are all in its base commit (notes D2): no review, and so no measure. This is unchanged and left for the person.
- A re-review after a fix work-item on the same day: the same-day measurement exists, `measure` refuses, and there is no analysis (decision 2). Name it if a scenario reaches it.
- The analysis session's own cost goes unrecorded, because it has no `session.json` kept under `.shop/work/`.
