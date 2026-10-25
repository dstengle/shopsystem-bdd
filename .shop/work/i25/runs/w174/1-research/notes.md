# Research of w174: work answer, reviewer's questions (work-queue r14, r26, r27)

Tools: `tools map` has no map, so `tests-of` and `untested` are unavailable: tests are found by search (`by search`) and by running them (`run`). `tools refs asked_from` works (`refs`). `tools refs` on `workqueue_answer.answer` refused its path syntax; the references were found by search.

## 1. Why each accepted scenario is red today

Command for all nine: `python3 -m pytest -q -p no:cacheprovider -n 0 "tests/scenarios/test_work_queue.py::<node>"` (node ids from `--collect-only`). Result (`run`): 7 passed, 2 failed.

- r26 "answer that asks for a change, to a reviewer's question, transitions the work-item to ready" (feature line 315): red. `StepDefinitionNotFoundError` for `When "the session runs `work answer w1 "Rename the flag"`, saying that the answer asks for a change"` (feature line 318). Missing: a step in `tests/scenarios/work_queue_answer_steps.py` that binds this text and passes the change flag to `work`. In `scripts/work` (`main`, the `answer` subparser, lines 112-114) there is no flag. In `scripts/workqueue_answer.py` (`answer`, line 24) there is no flag and no reviewer branch, so a reviewer's question takes `asked_from`'s status (`done`, line 40).
- r27 "answer that accepts the work-item as it is, to a reviewer's question, transitions the work-item to done" (feature line 323): red the same way, at feature line 326 ("saying that the answer accepts the work-item as it is"). Missing: the same step, with `--accept`; the same parser and `answer` gaps.
- r14 "answer to a researcher's, a planner's or an implementer's question" (feature line 301, three examples): green today (`run`): `[a researcher-drafted]`, `[a planner-researched]`, `[an implementer-ready]` all pass.
- r14 deprecated outline (feature line 286, four examples, retired by the Retires section): green today (`run`), including `[a reviewer-done]`. Its reviewer example is the old behaviour r26 and r28 replace (section 4).

## 2. What the system answers today

Probe file: `.shop/scratch/w174-1-research/probe_answer.py`. Command: `python3 -m pytest -q -s -p no:cacheprovider -n 0 .shop/scratch/w174-1-research/probe_answer.py`. Each probe makes a fresh repository in the scratch directory (spec/index.md, initiative i1, its work-items, log.jsonl, one commit) and runs `python3 <worktree>/scripts/work --root <repo> ...`. All `run`.

- Reviewer's question (log: `done` -> `awaiting-answer`), the r26 Given and When with `--change`: `work answer w1 "Rename the flag" --change` gives rc 2, `unrecognized arguments: --change`. w1 stays `awaiting-answer`, log unchanged, no commit. So the r26 scenario fails at the parser, before any step of `answer`.
- The same with `--accept` (r27 Given and When): rc 2, `unrecognized arguments: --accept`; nothing changes.
- Nearest: the reviewer's question with no flag, `work answer w1 "Use the first reading"`: rc 0, stdout `w1 done`. The log gains `before: awaiting-answer, after: done, by: work answer` and a commit `work answer: w1 awaiting-answer -> done`. This is the r14 landing, and r28 (in the capability, line 46) says it must be refused. See defect D1.
- Nearest: both flags at once: rc 2, unrecognized arguments, nothing changes.
- Baseline, implementer's question (log: `claimed` -> `awaiting-answer`), no flag: rc 0, `w1 ready`. Unchanged by the requirements.
- Nearest: the log has no move into `awaiting-answer` for w1: rc 1, stderr `work: log.jsonl gives no transition of w1 to awaiting-answer; work answer has no status to return it to`; w1 stays `awaiting-answer`, no log line, no commit. `asked_from` raises this, and a reviewer branch reaches it too unless it reads the flag first.
- Not probed: the answer given twice (the second `## Answers` bullet), an empty answer string, a proposal's answer under the new flags. The requirements do not name them, and the r14 path is covered by the test run.

## 3. Old assumptions

Requirements r26 and r27 replace "a reviewer's question returns to the status the asking stage started from" (r14's old reading, `done`) with a choice made by a flag. Places that still make the old assumption:

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue_answer.py:asked_from (lines 15-21) | maps the log's last move into `awaiting-answer` to its `before` through `ASKED_FROM`; a reviewer's question gives `done` | for a reviewer's question it is no longer the answer's target: change gives `ready`, accept gives `done` | test_work_queue.py r14 deprecated outline `[a reviewer-done]` (run, passes); delegation scenarios of features/supervision.feature 1010-1036 reach it through supervise_answers.py (`by search`, not run) | refs (1 production reference, 0 test files) and text |
| scripts/workqueue_answer.py:answer, line 40 `status = ... asked_from(...)` | every non-proposal work-item goes to `asked_from` | a reviewer's question needs the flag branch before this line; r28 refuses it without the flag | the r14 outline rows (run) | text |
| scripts/workqueue_answer.py:ASKED_FROM (line 9), `{"claimed": "ready"}` | only the implementer's start is remapped; the reviewer's `done` is the identity | unchanged for the three earlier stages; the reviewer's branch must not reach it | the r14 outline rows (run) | text |
| scripts/work:answer subparser (lines 112-114) | positional `name` and `answer` only; no flag | needs `--change` and `--accept` (r26, r27); r28 refuses neither | the probes above (run) | text |
| scripts/supervise_answers.py:answers, line 79 `self.move(name, before, workqueue_answer.asked_from(...))` | a work-item whose delegated questions are all answered goes to `asked_from`; for a reviewer's question that is `done`, with no change-or-accept decision | the delegation's answer has no flag; a reviewer's question under a delegation would land in `done` unflagged, which r28 refuses | none for the reviewer branch (`by search`: the delegation scenarios use work-items from `drafted`, `researched`, `claimed`); the work-item branch runs in those scenarios (`by search`, not run) | refs (`asked_from` has one production reference) and text |
| scripts/supervise.py:STAGES, line 35 `"done": ("review", "bdd-task-reviewer", "green")` | a work-item in `done` is next run through a review stage, which on DONE makes it `green` | r27 sends an accepted work-item to `done`, so `work run` would review it again; `done` does not mean accepted | features/supervision.feature:61 (`done | bdd-task-reviewer`, `by search`, not run) | text |

## 4. Tests the requirements make impossible to keep

`tools tests-of` is unavailable, so this list is `by search` over `tests/scenarios/`, `tests/scripts/` and `features/`, with the nine node ids run.

- tests/scenarios/test_work_queue.py `test_answer_on_an_awaitinganswer_workitem_transitions_it_to_the_status_the_asking_stage_started_from_deprecated[a reviewer-done]` (feature line 286-298, the r14 form retired): passes today (`run`). After r26 and r28 a reviewer's question answered with no flag is refused (r28) or sent to `ready` or `done` by the flag, so `done` with no flag can no longer be the result. This row cannot pass as it is. Its researcher, planner and implementer rows can keep passing.
- Verified sound (`run`): the r14 outline rows `[a researcher-drafted]`, `[a planner-researched]`, `[an implementer-ready]`, and the deprecated rows of the same three stages: their stages are not changed.
- Verified sound (`by search`): features/work-queue.feature r9 rows (lines 238-269) and the r13, r24 answer rows: they do not touch the reviewer's branch.
- No other test asserts a reviewer's question lands in `done` through `work answer`: by search over tests/, "reviewer" matches test_work_queue.py:79 (the Given of the deprecated outline, `"a reviewer": "done"`) and otherwise the reviewer-worker steps of supervision_*.py and tests/scripts/test_agents.py.

## 5. A step the work-item skips

- The flag decision is the step a reviewer's question needs and the existing way does not take: `asked_from` lands the question in `done` with no decision (`read`, workqueue_answer.py:40). The delegated path skips the decision too: supervise_answers.py:79 moves a reviewer's work-item to `asked_from` with no say which way it goes (`read`).
- Effects only the existing `done` landing produces (`read`, supervise.py:35): `work run` treats `done` as "run the review stage" and makes the work-item `green` on DONE. So an accept that lands in `done` (r27) is reviewed again by `work run` and is not `green` until that review ends. r23 counts only `green` or `withdrawn` work-items for an initiative to be `done`, so an accepted work-item does not close its initiative.
- `work answer` does not call the initiative's done check (`read`: workqueue_answer.py has no call into workqueue_done.py). Nothing else in `answer` is skipped.

## 6. Defects

### D1. A reviewer's question answered with no flag lands in `done`

Reproduction (`run`): `.shop/scratch/w174-1-research/probe_answer.py::test_reviewer_question_no_flag`. Repository with w1 `awaiting-answer`, log line `done -> awaiting-answer`, then `work answer w1 "Use the first reading"`.
Came back: rc 0, stdout `w1 done`; w1's status `done`; the log's last line `before: awaiting-answer, after: done, by: work answer`; commit `work answer: w1 awaiting-answer -> done`.
Expected under the capability text (spec/capabilities/work-queue.md r28, line 46): exit with an error saying the answer must say whether it asks for a change or accepts the work-item as it is, and change nothing. r28 is not in w174's accepts; recorded for the plan. The r28 scenario (feature line 331) has no step definition in tests/ (by search, "saying neither" matches nothing), so it is red as an undefined step; not run.

## 7. The file set

Production:
- scripts/work (151 lines): `answer` gets `--change` and `--accept` (mutually exclusive) and passes the flag to `workqueue_answer.answer`. Found by reading `main` and `cmd_answer`, and by the probes' argparse refusal.
- scripts/workqueue_answer.py (59 lines): `answer` takes the flag; a reviewer's question goes to `ready` for `--change` and to `done` for `--accept`; `asked_from` and `ASKED_FROM` keep the other stages. Found by reading and by the probes.

Decision for the plan, not required by the four accepted scenarios:
- scripts/supervise_answers.py (128 lines): line 79 moves a reviewer's delegated work-item by `asked_from`; it needs the same flag or a refusal. Found by refs.

Tests:
- tests/scenarios/work_queue_answer_steps.py (41 lines): add the two When steps, one for "saying that the answer asks for a change" and one for "accepts the work-item as it is", each passing `--change` or `--accept` to `work`. Found by the red run (section 1).
- Feature rows: the reviewer example of the deprecated outline (features/work-queue.feature 286-298) passes today and cannot pass after r26 and r28. Retires lists it; deleting it is the plan's choice. Found by the run of its node (section 4). No Python file changes for it: tests/scenarios/test_work_queue.py is generated by `scenarios("work-queue.feature")` (line 32) and needs no edit.

Modules on the change's path, edited or not (line counts by `wc -l`; room under the 300-line limit of CLAUDE.md, which gives none, so the limit of `tools size` is used: 300 minus lines):
- scripts/work: 151 lines, room 149 (edited)
- scripts/workqueue_answer.py: 59 lines, room 241 (edited)
- scripts/workqueue.py: 290 lines, room 10 (not edited: `move`, `agrees`, `committed`, `find`, `logged` used by the answer path; if `move` changes, room is 10)
- scripts/workqueue_note.py: 21 lines, room 279 (not edited: imports `LINE_BREAKS` from `workqueue_answer`)
- scripts/supervise_answers.py: 128 lines, room 172 (not edited for the four; decision above)
- scripts/supervise.py: 248 lines, room 52 (not edited: `STAGES`, read in section 3)
- tests/scenarios/work_queue_answer_steps.py: 41 lines, room 259 (edited)
- tests/scenarios/test_work_queue.py: 288 lines, room 12 (not edited)
- features/work-queue.feature: 452 lines; not Python, so no limit under CLAUDE.md (retire decision in section 7)

Git: `git status --porcelain` is empty at the end; the scratch directory is ignored.
