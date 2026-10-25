# Research of w155: an answering session that ends other than DONE

Scope: work-item w155 accepts supervision#r89 and supervision#r90. Accepted scenarios: the two in `features/supervision.feature` at lines 997 and 1007, bound in `tests/scenarios/test_supervision.py`.

Method: no coverage map exists (`tools tests-of` and `tools untested` answer "no map"; I did not run `tools map`, which runs the whole suite). Every test list below is `by search`. `tools refs` was not run; callers are `by read` of `scripts/supervise.py` and `grep`. Probes are `run`; reading is `read`.

Probe files (scratch, `.shop/scratch/w155-1-research/`): `probe_delegation.py` (cases A-F), `probe_round.py` (case G). Command for both: `python3 -m pytest -q -s -n 0 <path>`. Each builds its repo in pytest's tmp_path, never the checkout's data, and runs `scripts/work run i1` by path with the stand-in claude.

## 1. Why each scenario is red today

- r89 scenario, "ends at its turn limit": `python3 -m pytest -q "tests/scenarios/test_supervision.py::test_when_a_session_started_under_a_delegation_to_answer_a_question_ends_at_its_turn_limit_the_question_is_left_unanswered_for_the_person"` (run). Fails with `StepDefinitionNotFoundError`: Given "the session answering under the delegation ends at its turn limit, its result file answering "The queue module.", and every worker gives DONE" (feature line 1001). The existing step `session_answers` in `tests/scenarios/supervision_delegation_steps.py:48` matches only "answers "X", and every worker gives DONE". Missing: a step definition. Code behind it already gives the Thens (probe A, section 2): w1 stays awaiting-answer, no Answers section. So this scenario needs the step, not a code change.
- r90 scenario, "ends in an error": `python3 -m pytest -q "tests/scenarios/test_supervision.py::test_when_a_session_started_under_a_delegation_to_answer_a_question_ends_in_an_error_its_stage_directory_and_log_lines_are_committed"` (run). Fails with `StepDefinitionNotFoundError`: Given "the session answering under the delegation ends in an error, having written notes.md beside its brief" (feature line 1011). Missing: the step definition, and the Then "the initiative branch has a commit of the answering session's stage directory ... and of log.jsonl's lines for that session" (feature 1013) and the next Then (1014). Behind them, the code does not commit: after the step exists, probe B (section 2) shows the stage directory and log lines uncommitted. Code: `scripts/supervise_answers.py:ask` (lines 92-98) raises `Refused` on the fault before any commit; `answers` (60-81) commits a question's work-item only after its loop (lines 78 or 80), which a raise skips; `scripts/supervise.py:run` (193-194) calls `answers()` with no handler, so the exit comes first.

## 2. What the system answers today

All run (`run`), from `probe_delegation.py` and `probe_round.py`. Repo: w1 awaiting-answer, `## Questions` "Which module owns the log?", request q1 with delegation "Please get everything delivered. Do not stop to ask me questions or permission.".

- A, turn limit, result file answers "The queue module.": exit 1. stderr: `work: the session answering w1's question faulted: its answerer's session ended at its turn limit (error_max_turns, 26 turns, exit code 1); work run takes no outcome from it, whatever its result file says`. w1 awaiting-answer, no Answers section. `git status --porcelain`: ` M .shop/work/i1/log.jsonl`, `?? .shop/work/i1/runs/`. No commit after the setup commit. runs/w1/1-answer holds brief.md, result.json, session.json.
- B, error during execution, notes.md beside brief: exit 1. stderr: `... ended on an error during execution (error_during_execution, 1 turns, exit code 1); ...`. w1 unchanged. Same uncommitted status. runs/w1/1-answer also holds notes.md.
- C, B, then a second `work run i1` with the answering session now DONE with an answer: exit 1, no session started. stderr: `work: .shop/work/i1/log.jsonl, .shop/work/i1/runs/w1/1-answer/brief.md, ... notes.md, result.json, session.json under .shop/work are not committed; commit them before work run starts`. The start refuses (`supervise.py:check`, 82-86, the r46 guard).
- D, baseline DONE with answer "The queue module.": exit 0, `w1 green`. w1 Answers: `- 2026-10-25: The queue module.` then `by: work run, under the delegation "..."`. The commit `work: w1 ...` holds runs/w1/1-answer. stderr also says `measure initiative i1 was refused` because the stand-in's session.json has no usage; this is the stand-in's output shape, not a defect.
- E, baseline DONE without answer: exit 3; stdout `w1 awaiting-answer` and `  - Which module owns the log?`. The commit `work: w1 awaiting-answer -> awaiting-answer` holds runs/w1/1-answer and log.jsonl. So on DONE the stage directory IS committed; only the fault path skips it.
- F, turn limit with no result file (the "absent" and "empty data" case): exit 1, same refusal as A. runs/w1/1-answer holds brief.md and session.json only; uncommitted.
- G, existing way: a gate round of drafted p1 ends in an error, after w1 was answered (in the same run): exit 1. stderr: `work: the gate round of p1 (.shop/work/i1/runs/p1/1-gate) faulted, and p1 keeps its status drafted: ...`. Commit `work: p1 gate round 1-gate faulted` holds runs/p1/1-gate and log.jsonl; `git status --porcelain` empty afterwards. The round path (`supervise_rounds.py:round` line 69 -> `keep_round` 83-92) commits and pushes the stage directory with no transition.

Nearest cases: "twice" is C; "the scenario's own data empty" is F; "absent" (no answering session result) is F. Not probed: two open questions, one faulting (the rest of the loop is `read`, see section 5).

## 3. Old assumptions

The change makes an answering session's fault keep its record (r90), the way a round's fault does. The old assumption is that a fault in `answers()` ends the run before anything is committed.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_answers.py:ask (83-102) | a Fault or GitFailed from the worker becomes `Refused`, so the session's stage directory and log lines are left uncommitted | it must keep the record (r90) and still give no answer (r89; already true, probe A/B) | r77, r78 rows of `supervision_delegation_steps.py` and the two red scenarios, by search | read; probes A, B, F |
| scripts/supervise_answers.py:answers (60-81) | commits a work-item only after its loop (`move` at 78, `commit` at 80); a raise skips both and the `push()` at 81 | the fault path needs its own commit before the run ends | r77, r78 scenarios, by search (DONE paths only) | read; probe E |
| scripts/supervise.py:run (193-194, 206-209) | `answers()` has no handler; the `finally` only removes worktrees | r89 is silent on whether the run goes on; r90 needs the record kept before the exit | none: no scenario asserts the run stops or goes on after a faulted answer, by search | read; probe A |
| scripts/supervise.py:commit (94-105) | the one commit of run directories and log lines for a move; it clears `self.own` and `self.unlogged` | the fault path needs the same commit without a transition | every transition scenario, by search (not counted) | read |
| scripts/supervise_rounds.py:keep_round (83-92) | commits the round's stage directory and log lines with no transition, then `git_push()`; the existing way for a fault | the answering fault should take this way | none asserts its commit, by search (features 1050 asserts status only); it runs under the round-fault scenarios, not verified | read; probe G |
| scripts/supervise_worker.py:worker (181-184) | adds the run directory to `self.own` and log start/end to `self.unlogged`, expecting a later commit | the answering fault must make that commit, or these stay pending | every worker scenario, by search (not counted) | read |
| scripts/supervise.py:check (82-86) | refuses a `work run` while anything under .shop/work is uncommitted (r46) | today's answer fault leaves it so; the next run is refused (probe C) | r46 scenario not searched | read; probe C |
| scripts/supervise_faults.py:checkout_changes (91-112) | keeps `own` and `unlogged` paths as the run's own writes | not reached on the answer-fault path: the run exits first | none: not reached in this path, read | read |

## 4. Tests the requirements make impossible to keep

No map, so `by search`. Searched the tests for `delegation`, `answer`, `faulted`, `keeps its status`, `awaiting-answer -> awaiting-answer`, `keep_round`.

- `tests/scenarios/supervision_delegation_steps.py` (108 lines): the Then `have_none` (91-95) checks no Answers section and `status: awaiting-answer`; still true after the change. The Then `answer_names_delegation` (98-108) and `have_answer` (85-88) concern DONE paths, which the change does not touch. Verified sound by read.
- `tests/scenarios/test_supervision.py`: the r77 Outline rows (answer / leave) pass with the change: the commit only adds a path to a DONE commit that already has it. Verified by read and probe E.
- Features 1050 (round at turn limit keeps status): asserts `p1 is drafted` only; unaffected by the commit (probe G shows the same status). Verified by read.
- `awaiting-answer -> awaiting-answer` commit: no test asserts it (by search: none). Probe E shows it is made today.
- No test found that asserts the answering fault leaves the tree uncommitted. So: none can no longer pass.

## 5. A step the work-item skips

The fault path of an answering session skips the step the round fault path takes: `keep_round` (`supervise_rounds.py:83-92`). Its effects, read from that function:

- commits the run directory and log.jsonl lines (`git add`, `git commit`), so `git status` is clean and the next `work run` is not refused (probe G shows this for a round; probe C shows its absence for an answer);
- pushes the commit (`git_push()`), so the remote has the record (read; not probed);
- clears `self.own` and `self.unlogged` for the directory (read).

Its refusals: a `git status` or `git commit` failure raises `GitFailed` (read; not probed). The answer path has none of these.

Also `read`: a second faulting question in the same `answers()` loop is never asked, since `Refused` leaves the loop; `answers()` names questions in `asking()` order (sorted by file name). Probe not run.

## 6. Defects

D1. An answering session that ends other than DONE leaves its record uncommitted, and the next `work run` refuses. This is r90's gap, shown by the probes:
- command: `python3 -m pytest -q -s -n 0 .shop/scratch/w155-1-research/probe_delegation.py -k b_error` then `-k c_error_then_second_run` (run)
- came back: exit 1, `git status` ` M .shop/work/i1/log.jsonl`, `?? .shop/work/i1/runs/`; the second run: exit 1, "... are not committed; commit them before work run starts".

D2. A DONE answering session with no answer commits a transition that makes none: `work: w1 awaiting-answer -> awaiting-answer`.
- command: `python3 -m pytest -q -s -n 0 .shop/scratch/w155-1-research/probe_delegation.py -k e_baseline` (run)
- came back: exit 3, and `git log` shows `work: w1 awaiting-answer -> awaiting-answer` after the setup commit. Whether this is wrong is not for me to judge: r7 names transitions, and this commit is not one. Noted, not fixed.

Not a defect: the `measure initiative` refusal in case D comes from the stand-in's session.json shape (run).

## 7. The file set

Production (must change for the scenarios to pass and keep passing):
- `scripts/supervise_answers.py` (120 lines; room 180): a faulted session's stage directory and log lines committed, and the answer left out, before the run ends; ask/answers, lines 83-102 and 60-81.
- `scripts/supervise.py` (237 lines; room 63): if the commit or the error handling is shared, the new call goes here (`run`, 193-194; `commit`, 94-105). Probably only a helper, if any.
- `scripts/supervise_rounds.py` (92 lines; room 208): `keep_round` is the existing way; reuse it, or move it, without changing rounds. Probably unchanged.

Tests (must change):
- `tests/scenarios/supervision_delegation_steps.py` (108 lines; room 192): two Given steps (turn limit with `error_max_turns` and a result answer; error with notes.md beside the brief), and the r90 Thens (commit of the stage directory with notes.md, of the log lines; nothing uncommitted).

On the change's path, not expected to change:
- `scripts/supervise_worker.py` (242 lines; room 58): `worker`, `session`; read only.
- `scripts/supervise_faults.py` (160 lines; room 140): `cut_short`, `checkout_changes`; read only.
- `tests/scenarios/test_supervision.py` (250 lines; room 50): the two scenarios bind here; no change expected.
- `tests/scenarios/supervision_world.py` (173 lines; room 127): helpers only.

`python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300` printed nothing: no tracked Python file is over 300 lines.
