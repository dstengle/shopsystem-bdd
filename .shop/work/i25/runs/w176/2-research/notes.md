# w176 research notes (stage 2-research)

Method. Names by `tools refs` (`scripts/tools` at the plugin path). `refs workqueue_answer.asked_from` gave 1 reference (line 40); search found a second, `supervise_answers.py:79` (module attribute), so refs missed it. `tests-of` and `untested`: "no map" (`tools map` not run); tests that execute code are `by search`. Probes: `.shop/scratch/w176-2-research/probe_answer.py` (run `python3 -m pytest -q -s -n 0 .shop/scratch/w176-2-research/probe_answer.py`, 10 passed). Each probe builds its own git repo under `.shop/scratch/w176-2-research/repos/`. Accepted scenarios (work-queue.feature): deprecated outline 285 (4 rows), r14 outline 300 (3 rows), r26 314, r27 322, r28 330. w176.md has no `Retires` section. Earlier stage notes (`.shop/work/i25/runs/w176/1-research/notes.md`) read; I re-ran and re-probed. Where I differ: `scripts/work` is 169 lines (earlier notes said 151).

## 1. Why each scenario is red today

Command for each: `python3 -m pytest -q "<node id>"` (run). Ten node ids, one call.
- r14 outline, 3 rows (researcher, planner, implementer): GREEN (run).
- deprecated outline, 4 rows incl. `[a reviewer-done]`: GREEN for the 3 stage rows; `[a reviewer-done]` is GREEN today and cannot pass under r28 (part 4, Q3).
- r26 "asks for a change ... ready" (feature 315-320): RED (run). `StepDefinitionNotFoundError: When "the session runs \`work answer w1 "Rename the flag"\`, saying that the answer asks for a change"`, line 318. Missing: the When step in `tests/scenarios/work_queue_answer_steps.py`; the flag in `scripts/work` answer subparser (lines 122-124, no flag; cmd_answer 49-50); the reviewer branch in `scripts/workqueue_answer.py:answer` (line 40 uses `asked_from`, which returns `done`, so the answer would land `done`, not `ready`).
- r27 "accepts ... done" (feature 323-328): RED (run). `StepDefinitionNotFoundError` for `saying that the answer accepts the work-item as it is`, line 326. Missing: the When step; the flag; the reviewer branch to `done`.
- r28 "neither ... refused" (feature 330-336): RED (run). `StepDefinitionNotFoundError` for `saying neither that the answer asks for a change nor that it accepts the work-item as it is`, line 334. Missing: the When step; the Then `work exits with an error, saying that the answer must say whether it asks for a change or accepts the work-item as it is` (feature 335; no such step; only `work exits with an error, saying that an answer is one line` exists, work_queue_answer_steps.py:28); the refusal in `workqueue_answer.py:answer` (today a reviewer answer without a flag lands `done`, P1). The Then `{first} and {second} are as they were` exists (test_work_queue.py:266).

## 2. What the system answers today (probes, all run)

Command: `python3 -m pytest -q -s -n 0 .shop/scratch/w176-2-research/probe_answer.py` (10 passed). Reviewer item: log.jsonl line `before: done, after: awaiting-answer`, as `supervise.py:170` writes it.
- P1 reviewer, no flag, `work answer w1 "Rename the flag"`: rc 0, stdout `w1 done`; file status `done`; log last line `awaiting-answer -> done` by `work answer`; commit `work answer: w1 awaiting-answer -> done`. (The r28 gap, D1.)
- P2 reviewer, `--change`: rc 2, `work: error: unrecognized arguments: --change`; file and log unchanged.
- P3 reviewer, `--accept`: rc 2, `unrecognized arguments: --accept`; unchanged.
- P4 reviewer, `--change --accept`: rc 2, `unrecognized arguments: --change --accept`; unchanged.
- P5 implementer (log `claimed -> awaiting-answer`): rc 0, `w1 ready`.
- P6 researcher (log `drafted -> awaiting-answer`): rc 0, `w1 drafted`.
- P7 reviewer, no flag, file has no `## Questions`: rc 0, `w1 done` (answered with nothing to answer; read: workqueue_answer.py never reads `## Questions`).
- P8 reviewer, no flag, answer `one\ntwo`: rc 1, `the answer has a line break in it; an answer is one line`; unchanged. Line-break check runs first (workqueue_answer.py:27-28), so r15 already holds for every kind of question.
- P9 log `green -> awaiting-answer` (no reviewer shape), no flag: rc 0, `w1 green`. Nearest case: `asked_from` returns whatever `before` was (read: workqueue_answer.py:21).
- P10 second answer on the item P1 made `done`: rc 1, `w1 is not awaiting-answer; work answer answers only an awaiting-answer work-item or capability-proposal`.
- read: `work answer i1/w1` (r30) goes through `answer()` the same way (run earlier stage: `i1/w1 done`, rc 0; not re-run).
- read: the reviewer question is identified only by log `before == "done"`. No other stage starts from `done`: STAGES (supervise.py:31-36) gives `done` only to review. `supervise_merge.py:88,108` moves a `claimed` item to awaiting-answer for a merge failure: asked_from gives `ready` (ASKED_FROM).

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue_answer.py:asked_from (15-21) | returns the `before` of log's last move into awaiting-answer; for a reviewer that is `done` | r14 names only researcher, planner, implementer; a reviewer's answer needs the flag (r26-r28), so `done` must not be the default | deprecated `[a reviewer-done]` (run); r14 rows (run, 3 stage rows) | refs (1 ref); read |
| scripts/workqueue_answer.py:answer line 40 (`status = ... asked_from`) | the one transition of `work answer` for every non-proposal work-item | a reviewer's question (before `done`) needs its own branch: `--change` to `ready`, `--accept` to `done`, neither refused | the 7 answer tests that reach line 40 (run) | read |
| scripts/supervise_answers.py:answers line 79 (`self.move(name, before, workqueue_answer.asked_from(...))`) | after delegated answers leave no open question, moves the item to the asked-from status without `work answer` | a delegated reviewer question lands `done` with no verdict; r28's refusal is skipped (Q2) | none (by search: no test has a reviewer's question under a delegation; supervision_delegation_steps.py has no `reviewer` text) | search (refs missed it); read |
| scripts/work:122-124 (`answer` subparser) and cmd_answer (49-50) | takes `name` and `answer` only | two new flags (`--change`, `--accept`) to pass to `answer` | the r14 answer runs (run, by subprocess) | read; search |
| scripts/supervise.py:STAGES `"done"` (35) and MOVABLE (37); pull at supervise_pool.py:87 and supervise.py:205 | `done` is the status an implementer's DONE leaves; `work run` starts review on it; the review's DONE gives `green` | r27 sends an accepted reviewer item to `done`, so the next `work run` starts a new review of it (Q4) | by search: test_supervision.py `[done-bdd-task-reviewer]` (collected, not run; the work_items plugin deselects it under w176) | read; search |
| scripts/supervise_brief.py:findings_lines (98) | gives the findings line only when the log reads `done -> awaiting-answer` then `awaiting-answer -> ready` | still true under r26 (`--change` gives `ready`); r27 (`done`) gives no line, as it has no route to `ready` | by search: supervision.feature:1044 scenario (its Givens write the state directly; not run) | read |
| scripts/workqueue.py:move (142-167) | writes any status in STATUSES, logs it; no transition table | awaiting-answer to ready or done needs no change here | the r14 answer runs (run) | read |
| scripts/workqueue_answer.py:54, 58 (`move`, not `moved_to`) | `work answer` skips the r23 check (workqueue.py:moved_to 242-252) | r23 fires only on green or withdrawn; `ready` and `done` cannot make an initiative done, so nothing changes | none (no test answers into `done` with a last item to close the initiative) | read |

## 4. Tests the requirements make impossible to keep

`tools tests-of` gave "no map" for every function; this part is `by search`.
- test_work_queue.py::test_answer_on_an_awaitinganswer_workitem_..._deprecated[a reviewer-done] (GREEN today, run). Answers a reviewer's question with no verdict and expects `done`. r28 refuses that answer, so it cannot pass as written. Mechanism: workqueue_answer.py:40 via asked_from (line 21). Decision: Q3.
- Sound, kept (run): deprecated `[a researcher-drafted]`, `[a planner-researched]`, `[an implementer-ready]`; r14 outline 3 rows. They hold under r14 as written and under r26-28 (the reviewer branch does not reach them).
- Sound, read (not run): r13, r15, r24 answer tests use the default asker "an implementer" (test_work_queue.py:70-80), so the flag check does not reach them. r15 probe P8 runs the refusal path.
- test_work_queue.py:79 (`started` map, `"a reviewer": "done"`): still the true before-status; stays.
- test_supervision.py::test_an_implementer_started_for_a_workitem_that_an_answer_to_its_reviewers_question_returned_to_ready_... (supervision.feature:1044): not run. The work_items plugin deselects it under w176 (it accepts none of its collected tests). Read: its Givens (supervision_answers_steps.py:40, 50) write the reviewer state and the `ready` log line directly and never run `work answer`; the flag does not reach it. Sound (read).
- No test runs `work answer` with a reviewer's question under a delegation (supervision_answers_steps.py, supervision_delegation_steps.py searched): none to break; but none to prove Q2 either.

## 5. A step the work-item skips

- The delegated answer path (supervise_answers.py:answers, line 79) does not call `work answer`. So it skips: the r28 refusal (no verdict required), and the flag itself. Shared: the one-line check (supervise_answers.py:110 uses LINE_BREAKS, read; the same set as workqueue_answer.py:11). It commits with `self.commit` (read), not `workqueue.committed`. The existing way is `work answer` (P1 shows its effect: a reviewer answer lands `done`). Delegated path not run (needs a claude session).
- `work answer` does not run the r23 done-check (workqueue_answer.py:54, 58, read). No effect for `ready` or `done` targets (see part 3).

## 6. Defects

### D1 reviewer's answer without a verdict lands `done`
Reproduction (run, probe P1): `work answer w1 "Rename the flag"` on a reviewer's awaiting-answer item (log `done -> awaiting-answer`) prints `w1 done`, rc 0, the file's status becomes `done`, and the log gets `awaiting-answer -> done`. Accepted r28 says this must exit with an error and change nothing. This is the gap r28 tests, not a regression. Not fixed here.

No other defect found. P2 to P4 are the missing flags (argparse rc 2), which is the r26-r28 gap, not a bug. P9 (log `green` before) is a nearest case with no spec line; not counted.

## 7. The file set

Production:
- scripts/work: add `--change` and `--accept` to the `answer` subparser (122-124) and pass them through cmd_answer (49-50). Search: text in scripts/work.
- scripts/workqueue_answer.py: `answer()` takes the flags; for a reviewer's question (log before `done`), refuse unless exactly one flag is given (Q1), `--change` to `ready`, `--accept` to `done`; the line-break check stays first; `asked_from` gets no reviewer default. Read; refs; P1-P4.
- scripts/supervise_answers.py: line 79 only if delegated reviewer answers are in scope (Q2). Search; read.

Tests:
- tests/scenarios/work_queue_answer_steps.py (41 lines, room 259): three When steps (asks for a change, accepts, neither) and the Then `work exits with an error, saying that the answer must say whether it asks for a change or accepts the work-item as it is`. Search: no step text for `saying that the answer` and no step for `exits with an error, saying that the answer must`.
- tests/scenarios/test_work_queue.py (288 lines, room 12): only if the deprecated reviewer row changes (Q3). Keep new steps out of it.
- features/work-queue.feature (not Python): deprecated reviewer row, lines 285-298, only if Q3 (a) or (b).

Path, edited or not (`wc -l`; room under 300; `tools size --limit 300` printed nothing):
- scripts/work, 169 (room 131): edited.
- scripts/workqueue_answer.py, 59 (room 241): edited.
- scripts/workqueue.py, 290 (room 10): on the path (move, agrees, find, committed), not edited.
- scripts/supervise_answers.py, 128 (room 172): on the path, edited only per Q2.
- scripts/supervise.py, 248 (room 52): on the path (STAGES), not edited.
- scripts/supervise_pool.py, 143 (room 157): on the path (pull), not edited.
- tests/scenarios/test_work_queue.py, 288 (room 12): test file, edited only per Q3.
- tests/scenarios/work_queue_answer_steps.py, 41 (room 259): edited.
- spec/capabilities/work-queue.md: already has r26-r28 and the changed r14; not edited.

## Questions for the plan (both readings; not decided here)

Q1 Both `--change` and `--accept` given. (a) refuse with an error, change nothing (r28's "which" suggests one); (b) the spec is silent. No scenario covers it.
Q2 A delegated reviewer question (supervise_answers.py:79). (a) the answer session must give the verdict, and the path refuses a verdict-less answer, as `work answer` does (a change to the delegation's output); (b) keep asked_from, so a delegated reviewer answer lands `done` with no verdict (the r28 gap stays on that path). The spec's r26-r28 name `work answer` only.
Q3 The deprecated reviewer row (feature 285-298, test `deprecated[a reviewer-done]`) is in the accepted list and conflicts with r28. (a) retire it: w176.md needs a `Retires` section naming it; (b) keep the row and change its expectation to a refusal (a change to the feature file). The work-item cannot pass both as written.
Q4 `--accept` sends the item to `done`, which `work run` starts a review on (supervise.py:35, 37, 205). (a) implement r27 as written: the next `work run` reviews the accepted item again; (b) the supervision capability gives accepted items another status. Out of w176's scope as the spec reads; flagged here.
