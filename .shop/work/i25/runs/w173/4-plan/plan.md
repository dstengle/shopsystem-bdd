# Plan of w173 (supervision#r98)

## 1. What goes green

- **supervision#r98**: scenario "an implementer started for a work-item that an answer to its reviewer's question returned to ready is given the reviewer's findings and the answer" (`features/supervision.feature`, `@r98`, written by the formulate round in 46fef129, per the answer in the brief).
  Why red today: its steps are not defined. Neither Given ("i1's work-item w1 was awaiting-answer on its reviewer's question ..., the reviewer having written findings.md beside its brief", "the answer ... returned w1 to ready") nor the Then ("the implementer of w1 was given the reviewer's findings.md, and the question ... with the answer ...") exists in `tests/scenarios/`. Behind them, `supervise_brief.py:brief` writes no line naming a findings file (notes §3, §7). The research notes say the run directories show up only as directories in the brief's `Read` list. The answer beside its question is already written by `answer_lines` (r57).
- No deprecated scenarios: w173 has no Retires section.

## 2. Where the change lands

- `scripts/supervise_brief.py`: for the implement stage of a work-item that an answer to its reviewer's question returned to `ready`, write one brief line that names the findings file of the work-item's last review stage directory. The answers stay as `answer_lines` writes them.
- `tests/scenarios/supervision_answers_steps.py`: the scenario's two Givens and its Then.

Removed from the researcher's set, and why:
- `features/supervision.feature`: the `@r98` scenario is already there (46fef129). w173 does not edit it.
- `tests/scenarios/test_supervision.py`: it binds the whole feature file through `scenarios("supervision.feature")` and already star-imports `supervision_answers_steps`, so it needs no change.
- `scripts/workqueue_answer.py`, `scripts/work`, `scripts/supervise_answers.py`: these are the `--change`/`--accept` flag route of work-queue r26-r28 (w174's). The r98 scenario starts with w1 already at `ready` (decision 3), so r98 needs none of them.

## 3. Decisions

1. **Where the findings path comes from.** It is the `findings.md` of the work-item's last review stage directory: the highest-numbered `<k>-review` under `runs/<work-item>`. It is not the reviewer's result `findings` field. This settles the open reading in notes §7 for reading (b). It rests on the Implementation line for supervision#r98 ("the brief names the findings file of the work-item's last review stage directory"), and on the proposal's answers 1 (a) and 2 (a), which cover a work-item's reviewer only (3-plan summary).
2. **When the line is written.** Only in the brief of the implement stage (the stage `ready` starts, `STAGES` in `supervise.py`). Only when the work-item's log shows the r98 route: its last move into `ready` was from `awaiting-answer`, and the move into `awaiting-answer` before it was from `done`, which marks a reviewer's question (work-queue r14/r26, the same reading `workqueue_answer.asked_from` makes of the log). Implementers on any other route get no findings line, so their briefs stay as they are. This rests on supervision#r98's condition ("a work-item that an answer to the question of a work-item's reviewer returned to `ready`"). Read the log through the existing log-reading helpers. Do not add code to `scripts/workqueue.py`: it is at 290 lines, with 10 lines of room (CLAUDE.md size limit).
3. **How the Givens set up w1.** They write the state directly, the way `work run` and `work answer` would leave it, without running `work answer --change`. That state is:
   - w1's file at `status: ready`, with the question under `## Questions` and the answer under `## Answers`.
   - `log.jsonl` with w1's moves: into `done`, `done` to `awaiting-answer`, then `awaiting-answer` to `ready` by `work answer`. The file and the log must agree, or `work run` refuses the item.
   - a `<k>-review` run directory of w1 holding a `brief.md` and a `findings.md`.

   All of it is committed, as the r57 Given commits its item. The reason: the scenario's Given says the answer "returned w1 to ready", which is a state, not a command; and the flag route is w174's (work-queue r26-r28), which the hook reports as withdrawn.
4. **What the Then checks.** Among the starts of w1, it takes the one `bdd-implementer` brief. That brief must hold a line naming the path of the review directory's `findings.md` (a path ending in `-review/findings.md`). It must also hold the question with the answer within the lines after it, the way `briefs_hold_answers` checks r57. It rests on supervision#r98 and r57.

## 4. Tests the decisions break

None. Checked against the notes and by search:
- No test asserts a findings line, or the exact lines of an implementer's brief (notes §3, §4).
- The r57 scenario's Then (`briefs_hold_answers`) looks only for the question/answer pairs. Its work-item reaches no review that comes back to `ready`, so decision 2 adds no line to its briefs.
- The deprecated work-queue row `a reviewer | done` (`tests/scenarios/test_work_queue.py:79`) runs `work answer`, not `supervise_brief`, so no decision of this plan touches it. Its fate belongs to w174 (r28).
- `test_supervision.py` and `supervision_answers_steps.py` stay well under 300 lines. `supervise_brief.py` is at 143 lines, with 157 of room.

## 5. Open cases (for the implementer to name, not to choose)

- The r98 route in the log, but no `<k>-review` directory, or one without `findings.md`.
- More than one review stage directory, where the last has no `findings.md` but an earlier one does.
- A reviewer's question answered under a delegation (`supervise_answers.py:79`) rather than by `work answer`.
- After the r98 route, a later implementer run of the same work-item reached by another route, such as a second review's answer or a reviewer's FAIL.
- Answers fewer than questions: `answer_lines` drops the unanswered question (notes §2).
