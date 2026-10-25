# Research of w173 (supervision r98)

Brief: no `Accepted scenarios:` line; searched `features/` for `@r98` (none). No `fileset:` in w173. No `tools map` (no coverage map): `tests-of` unavailable, so test lists are `by search`. `refs` used for names.

## 1. Why each scenario is red today

No accepted scenario exists. `grep @r98 features/` finds nothing; `features/supervision.feature` has `@r91`-`@r97`, `@r102`-`@r104` and no `@r98`. Commit `112fe1b6` (apply, i25) added spec line r98 only; no features commit followed. The proposal `.shop/work/i25/supervision.md` is `formulated` with `adds: [supervision#r98]`, so the formulate round's scenario is missing.

Run: none. No scenario can be run in this worker's environment. `PYTEST_ADDOPTS` carries `--work-item w173` (run: `python3 -m pytest -q -n 0 --collect-only -k brief_of_a_worker tests/scenarios` gave `INTERNALERROR ... SystemExit: --work-item w173: w173 accepts none of the scenarios it collected`, the r56 refusal). Dropping the plugin with `-p no:work_items` fails at argparse (`unrecognized arguments: --work-item`). A node id therefore cannot be run.

Nearest existing scenario, read only: `features/supervision.feature:826` (@r57, brief holds each answer beside its question), bound at `tests/scenarios/test_supervision.py::test_the_brief_of_a_worker_for_a_workitem_that_has_answers_holds_each_answer_with_the_question_it_answers`. Code it exercises: `scripts/supervise_brief.py:answer_lines` (r57, written for every stage).

## 2. What the system answers today

Probe 1: `tests/…` none; probe file `.shop/scratch/w173-1-research/probe_answer.py`, run `python3 -m pytest -q -n 0 -s .shop/scratch/w173-1-research/probe_answer.py` (run; `-n 0` needed to show output under xdist).

- Reviewer's question (log: `done -> awaiting-answer`), `work answer w1 "Rename the flag"`:
  `rc=0 stdout='w1 done'`; file `status: done`; log last line `before awaiting-answer, after done, by work answer`. The answer goes to `done`, not `ready`. (run)
- Same with `--change` (the flag work-queue r26 names): `rc=2 stderr='work: error: unrecognized arguments: --change'`. The option does not exist. (run)
- Implementer's question (log `claimed -> awaiting-answer`), `work answer w1 "Use the first reading"`: `rc=0 stdout='w1 ready'`. (run; control)

Nearest cases not given by scenarios, read only:
- A work-item with answers but no `## Questions` pairs: `answer_lines` returns `[]` (zip of two lists). (read)
- Answers with fewer entries than questions: `zip` pairs only the first; the unanswered question is not in the brief. Supervise's `held(...)` gives the open list. (read)
- A reviewer's question text is the reviewer's `questions` joined, or `"bdd-task-reviewer gave <status>: <summary>"` (`supervise_worker.py:outcome`). No findings path appears in the question. (read)

## 3. Old assumptions

Requirement r98 presumes a reviewer's answer returns to `ready`. Today the answer returns to the status the log's last move came from (`done`). Work-queue r26 (the flag route to `ready`) and r28 (refusal without flag) are spec'd in commit `1c0c4fb6` but not in code. r98 depends on work-queue r26 (w174).

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue_answer.py:ASKED_FROM | maps only `claimed -> ready`; a reviewer's `done` is returned to `done` | reviewer's answer must reach `ready` via the flag (work-queue r26) | none (`tests-of` has no map; by search: only work-queue.feature deprecated outline, test_work_queue.py:79) | refs, read, probe 1 |
| scripts/workqueue_answer.py:answer | takes `(root,name,text)`; no flag; returns asked_from | needs `--change`/`--accept` and refusal without (r26-r28) | by search: tests/scenarios/work_queue_answer_steps.py:16 (line-break case only) | refs (0 refs: `scripts/work` is not .py, so refs misses it), probe 1 |
| scripts/supervise_answers.py:79 (answers, delegated) | writes the delegated answer and moves to `workqueue_answer.asked_from` | a delegated answer to a reviewer's question must also take the flag route (r26/r28) | by search: tests/scenarios/supervision_delegation_steps.py (implementer/planner questions only) | read; refs missed it |
| scripts/supervise_brief.py:answer_lines | writes answers in every stage's brief (r57) | already writes answers for an implementer: r98's "writes the answer as r57 does" is current behaviour | by search: test_supervision.py r57 test (not run) | read |
| scripts/supervise_brief.py:brief (`read` list) | lists every run dir of the work-item, so the reviewer's directory is already readable | r98 wants the findings file named in the brief; the directory listing does not name it | none by search for findings in brief | read |

## 4. Tests the requirements make impossible to keep

`tests-of` unavailable (no map). By search:

- `features/work-queue.feature:286-298`, deprecated outline "answer on an awaiting-answer work-item transitions it to the status the asking stage started from (deprecated)", row `a reviewer | done`. Bound at `tests/scenarios/test_work_queue.py:79` (`"a reviewer": "done"`). It pins the old behaviour that r28 refuses (no flag). It is marked `@deprecated` (its replacement r26-r28 rows); cannot pass as bound once r28 lands. (read)
- No test under `tests/scripts/` asserts `asked_from` or `ASKED_FROM` (search: no hit). (by search)
- `tests/scenarios/test_work_queue.py` r14 outline rows (researcher, planner, implementer) remain sound. (read)
- r98 itself: no test yet; the r57 test is sound under r98 (checked by read). (read)

## 5. A step the work-item skips

The reviewer's answer skips the flag step that r26-r28 add. The existing way (`work answer`) has no such step: `ASKED_FROM` maps without the reviewer. Refusal effect only the flag step produces: `work answer` refuses without the flag (r28) and does not write the answer. Today the answer is written and the work-item moves to `done`. Shown by probe 1 (run). The delegated path (`supervise_answers.py:79`) skips it too (read).

## 6. Defects

### D1: a reviewer's question answered without the flag lands at `done`
Reproduction (run, probe 1, `probe_answer.py::test_reviewer_question_plain_answer`):
`work --root <repo> answer w1 "Rename the flag"` with log `claimed -> done`, `done -> awaiting-answer`.
Came back: `w1 done`, rc 0, file `status: done`, log `before awaiting-answer, after done`.
Spec: work-queue r28 says it shall exit with an error and change nothing. (The reviewer's question is then answered as if accepted, though no one said so.)

### D2: the r56 refusal prints as an INTERNALERROR traceback
Reproduction (run): `python3 -m pytest -q -n 0 --collect-only -k brief_of_a_worker tests/scenarios`. Came back: `INTERNALERROR ... SystemExit: --work-item w173: w173 accepts none of the scenarios it collected`. The option refuses (r56 says so), but as a traceback.

## 7. The file set

Files the work-item must change for r98's scenario (none yet exists; the scenario must be written first by the formulate round):
- `scripts/supervise_brief.py` (143 lines, room 157): name the findings file of the work-item's last `runs/<name>/<k>-review` directory in an implementer's brief; answers already written (answer_lines).
- `tests/scenarios/supervision_answers_steps.py` (52 lines, room 248): a Then for the findings line in the brief.
- `features/supervision.feature` (1275 lines; a feature file, not a module): the @r98 scenario. Written by a formulate round, not by w173.
- `tests/scenarios/test_supervision.py` (258 lines, room 42): the generated binding for the new scenario, if the file lists bindings.

Files needed only if the r98 scenario reaches `ready` through `work answer` (work-queue r26, the w174 item):
- `scripts/workqueue_answer.py` (59 lines, room 241): the flag, the `ready`/`done` routing, and the r28 refusal.
- `scripts/work` (line count not measured; the `answer` subparser takes the flag): the `--change`/`--accept` option.
- `scripts/supervise_answers.py` (128 lines, room 172): the delegated path's `asked_from` call, only if a delegated reviewer answer is in scope.

Modules on the change's path, not edited: `scripts/supervise.py` (248, room 52), `scripts/supervise_worker.py` (247, room 53; `outcome` and `worker`, which keep the reviewer's `findings` result key), `scripts/workqueue.py` (290, room 10; `move`, `agrees`, `append` used by `answer`). Size limit: 300 (CLAUDE.md).

Open for the plan (both readings, no choice made here):
- Where the findings path comes from: the reviewer's `findings` result field (`bdd-task-reviewer.md`: "`findings`: the findings file's path"), or the newest `<k>-review` directory listed by `runs/<name>`. The question text does not carry it.
