# w176 research notes

Method. Names by `tools refs` (no `.py` suffix: `scripts/work` not counted; `asked_from` reported 1 reference, search found 2). No coverage map (`tools map` runs the whole suite, not run): `tests-of` and `untested` give "no map", so tests that execute code are `by search`. Probes: `.shop/scratch/w176-1-research/probe_answer.py`, run `python3 -m pytest -q -s -n 0 <path>`, 6 passed, each in its own repository under `.shop/scratch/w176-1-research/repos/`.
Accepted scenarios (work-queue.feature): r14 deprecated outline (285), r14 outline (301), r26 (315), r27 (323), r28 (331). w176.md has no `Retires` section.

## 1. Why each scenario is red today

Run: `python3 -m pytest -q "<node id>"` (run).
- r14 outline, researcher/planner/implementer (3 rows): GREEN today (run).
- deprecated outline, 4 rows incl. `[a reviewer-done]`: GREEN today (run). See part 4.
- r26 "asks for a change ... ready": RED, `StepDefinitionNotFoundError` for `the session runs \`work answer w1 "Rename the flag"\`, saying that the answer asks for a change` (feature line 318). Missing: the When step (tests/scenarios/work_queue_answer_steps.py); the flag (scripts/work:112-114 has none; cmd_answer:49-50); the reviewer branch (scripts/workqueue_answer.py:24-59).
- r27 "accepts ... done": RED, StepDefinitionNotFoundError for `saying that the answer accepts the work-item as it is` (line 326). Missing: the When step; the same flag and branch.
- r28 "neither": RED, StepDefinitionNotFoundError for `saying neither that the answer asks for a change nor that it accepts ...` (line 334). Missing: the When step; the Then `work exits with an error, saying that the answer must say whether it asks for a change or accepts the work-item as it is` (no such step text in tests/); the refusal in workqueue_answer.answer (today reviewer answers land `done`, see part 2 P1). The Then `{first} and {second} are as they were` exists (test_work_queue.py:266).

## 2. What the system answers today (probes, run)

Command: `python3 -m pytest -q -s -n 0 .shop/scratch/w176-1-research/probe_answer.py`. The reviewer item: status awaiting-answer, log.jsonl line `before: done, after: awaiting-answer` (as the stage writes it, supervise.py:170).
- P1 reviewer, no flag, `work answer w1 "Rename the flag"`: rc 0, stdout `w1 done`, status done. (The r28 gap.)
- P2 reviewer, `--change` or `--accept`: rc 2, argparse `unrecognized arguments`.
- P3 implementer (log `claimed`): `w1 ready`; researcher (log `drafted`): `w2 drafted`. Both rc 0.
- P4 `work answer i1/w1` (r30), reviewer: `i1/w1 done`, rc 0. A second answer on the now-done item: rc 1, `w1 is not awaiting-answer; ...`.
- P5 awaiting-answer item, log.jsonl empty: rc 1, `log.jsonl gives no transition of w1 to awaiting-answer; ...`. File awaiting-answer, log's last move `done -> ready`: rc 1, `gives its status as awaiting-answer, but log.jsonl's last transition of w1 is to ready; it is not moved`.
- P6 reviewer, neither flag: rc 0, `w1 done` (= P1). Both flags: rc 2 argparse.
- read: line break in a reviewer answer is refused first (workqueue_answer.py:27-28, before any read or write), so r15 holds for every kind of question.
- read: an awaiting-answer item with an empty `## Questions` is answered with no check (workqueue_answer.py:41-58 never reads `## Questions`).

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue_answer.py:asked_from (15-21) | returns the `before` of log.jsonl's last move into awaiting-answer; a reviewer's is `done`, so it returns the reviewer item to `done` | r14 now names only researcher, planner, implementer; reviewer answers need the flag (r26-r28): the reviewer case must not fall through to `done` | r14 outline rows (run); deprecated reviewer row (run) | refs; read |
| scripts/workqueue_answer.py:ASKED_FROM (9) | maps `claimed` to `ready` for the implementer | unchanged | r14 implementer row (run) | read |
| scripts/workqueue_answer.py:answer line 40 (`status = ... asked_from`) | the one transition of `work answer` for every non-proposal work-item | needs the reviewer branch: `--change` to ready, `--accept` to done, neither refused | all r13/r14/r26-r28 answer tests (run for r14) | read |
| scripts/supervise_answers.py:answers line 79 (`self.move(name, before, workqueue_answer.asked_from(...))`) | after a delegation's answers, moves the work-item to the asked-from status, without `work answer` | a reviewer question answered under a delegation lands `done` with no verdict, the r28 refusal skipped | none by search (no test has a reviewer question under a delegation) | search (refs missed it) |
| scripts/work:112-114 (`answer` subparser) and cmd_answer (49-50) | takes `name` and `answer` only | two new flags, `--change` and `--accept` | the answer steps by subprocess (run for r14) | read; search |
| scripts/supervise.py:STAGES `"done"` (35) and MOVABLE (37); pull at supervise_pool.py:87 and supervise.py:205 | `done` is the status an implementer's DONE leaves; `work run` starts the reviewer on it, and DONE then gives `green` | r27 sends an accepted reviewer item to `done`, so the next `work run` starts a review of it again: the verdict does not end the review | by search: test_supervision.py::test_a_workitem_that_is_status_is_given_a_worker_of_agent[done-bdd-task-reviewer] (collected, not run) | read; search |
| scripts/workqueue.py:move (142-167) | writes any status in STATUSES and logs it; no transition table | awaiting-answer to ready or done needs no change here | answer tests (run for r14) | read |
| scripts/workqueue_answer.py:54, 58 (`move`, not `moved_to`) | `work answer` skips the r23 check of workqueue.py:moved_to (242-252) | r23 fires only on green or withdrawn; ready and done cannot make an initiative done | none by search | read |
| features/work-queue.feature:285-298 (deprecated outline, reviewer row `done`) | expects a reviewer answer without a verdict to land `done` | conflicts with r28 (part 4) | test_work_queue.py deprecated[a reviewer-done] (run) | search |
| tests/scenarios/test_work_queue.py:79 (`started` map, "a reviewer": "done") | the fixture's log `before` for a reviewer's question | still the true before-status; stays | every with_items Given with a reviewer (run via r26-r28 Givens) | read |

## 4. Tests the requirements make impossible to keep

- tests/scenarios/test_work_queue.py::test_answer_on_an_awaitinganswer_workitem_..._deprecated[a reviewer-done] (GREEN today, run). It answers a reviewer's question with no verdict and expects `done`; r28 refuses that. Cannot pass as is. Mechanism: workqueue_answer.py:40 via asked_from (line 21). Decision in Questions below.
- Sound (run, kept): the deprecated researcher, planner and implementer rows, and the r14 outline (6 tests); they hold under r14 as written.
- Sound (read): r13, r15, r24 tests use the default asker "an implementer" (test_work_queue.py:70-80), so the flag check does not reach them. Not run.
- tests/scenarios/test_supervision.py::test_an_implementer_started_for_a_workitem_that_an_answer_to_its_reviewers_question_returned_to_ready_... (collected, not run: the work_items plugin refuses a non-accepted test: "w176 accepts none of the scenarios it collected"). Its Given has no step text found by search, so it is probably red already. Read only; belongs to supervision.
- By search: no test puts a reviewer's question under a delegation (supervision_delegation_steps.py, supervision_given.py searched).

## 5. A step the work-item skips

- The delegated answer path (supervise_answers.py:answers, line 79) skips `work answer`. Only `work answer` produces the r28 refusal (no verdict), and the flag itself. Shared: the one-line check (ask(), supervise_answers.py:110, read) and the `before` check (agrees). The delegated path commits with `self.commit` (read). Probe of the existing way: P1. Delegated path not run (needs a claude session).
- `work answer` does not run the r23 done-check (workqueue_answer.py:54, 58, read). No effect for ready or done targets.

## 6. Defects

### D1 reviewer's answer without a verdict lands `done`
Reproduction (run, P1): reviewer item, log `done -> awaiting-answer`; `work answer w1 "Rename the flag"` gives `w1 done`, rc 0, file status `done`. Accepted r28 says this must exit with an error and change nothing. This is the gap the r28 scenario tests, not a regression. Not fixed here.

No other defect found. P3 to P6 behave as the current spec says.

## 7. The file set

Production:
- scripts/work: add `--change` and `--accept` to the `answer` subparser (112-114) and pass them to answer (cmd_answer 49-50). Search: text, scripts/work:112-114 and 49-50.
- scripts/workqueue_answer.py (59 lines): answer() takes the flag; for a reviewer's question, refuse unless exactly the flag says which, `--change` to ready, `--accept` to done; the line-break check stays first; asked_from's reviewer case. Read; refs.
- scripts/supervise_answers.py (128 lines): line 79 only if delegated reviewer answers are in scope (Questions, reading b). Read; search.

Tests:
- tests/scenarios/work_queue_answer_steps.py (41 lines, room 259): the three When steps, the Then for the refusal message. Search: no step text for "saying that".
- tests/scenarios/test_work_queue.py (288 lines, room 12): only if the deprecated reviewer row is retired or changed (its Examples are the step's table); keep new steps out of it.
- features/work-queue.feature (not Python): the deprecated reviewer row, lines 285-298, if it is retired or changed (Questions).

Path, edited or not (line count by `wc -l`; room under 300; `tools size --limit 300` printed nothing):
- scripts/work, 151 (room 149): edited.
- scripts/workqueue_answer.py, 59 (room 241): edited.
- scripts/workqueue.py, 290 (room 10): on the path (move), not edited.
- scripts/supervise_answers.py, 128 (room 172): on the path, edited only per Questions.
- scripts/supervise.py, 248 (room 52): on the path (STAGES), not edited.
- scripts/supervise_pool.py, 143 (room 157): on the path (pull), not edited.
- tests/scenarios/test_work_queue.py, 288 (room 12): test file, edited only per Questions.
- tests/scenarios/work_queue_answer_steps.py, 41 (room 259): edited.
- spec/capabilities/work-queue.md: already has r26-r28 and the changed r14 (commit 1c0c4fb6); not edited.

## Questions for the plan (both readings, not decided here)

Q1 Both `--change` and `--accept` given. (a) refuse with an error, change nothing (the r28 wording "which" suggests one); (b) the spec is silent: the plan must decide. No scenario covers it.
Q2 A delegated reviewer question (supervise_answers.py:79). (a) the delegation's answer must carry the verdict, the answer session must say change or accept, and the path refuses otherwise (a change to the delegation-answerer's output); (b) keep asked_from, so a delegated reviewer answer lands `done` with no verdict (the r28 gap stays on that path). Spec r26-r28 name `work answer` only.
Q3 The deprecated reviewer row (features/work-queue.feature:298, test deprecated[a reviewer-done]). (a) retire it (tagged @deprecated; w176.md has no `Retires` section, so it needs one); (b) keep the row and change it to refused. Each is a change to the feature file.
Q4 `accept` sends the item to `done`, which work run starts a review on (supervise.py:35, 37, 205). (a) implement r27 as written: the next `work run` reviews the accepted item again; (b) the supervision capability must give accepted items another status. Out of w176's scope as the spec reads; flagged here.
