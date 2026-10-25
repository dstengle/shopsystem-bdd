# Research of w173 (supervision r98)

Brief: no `Accepted scenarios:` line. Searched `features/` and the whole tree (outside `.shop/`) for `@r98` and `r98`: no scenario, no test; hits only in `spec/capabilities/supervision.md:99,154`. `tools tests-of` has no map (`tools: no map`), so every test list is `by search`. Probes ran from the worktree's `scripts/work` (base f582b1bb). Prior stage notes read: `.shop/work/i25/runs/w173/1-research/notes.md`. `git status --porcelain` is empty.

## 1. Why each scenario is red today

No accepted scenario exists: `supervision#r98` has no `@r98` tag in `features/supervision.feature` (its `@r91`-`@r97`, `@r102`-`@r104` only). Spec line added by apply commit `112fe1b6`; the formulate round did not write the scenario (1-research notes; ledger: r98 returned as a question). Nothing can be run for r98 until it exists, so no run of an r98 scenario is possible.

Command run: `python3 -m pytest -q -n 0 --collect-only -k brief_of_a_worker tests/scenarios` is not repeated here; 1-research ran it (read from its notes): `INTERNALERROR ... SystemExit: --work-item w173: w173 accepts none of the scenarios it collected` (r56 refusal printed as a traceback). Not re-run by me.

What the r98 scenario must cover, once written (read): an implementer's brief for a work-item whose reviewer question an answer returned to `ready` names the reviewer's findings file and holds the answer beside its question. Today the reviewer's answer does not return to `ready` (section 2), so the scenario would be red at the `Then` for `ready`, and at the brief's findings line (`scripts/supervise_brief.py:brief`, no findings line).

## 2. What the system answers today

Probe file: `.shop/scratch/w173-2-research/probe_answer.py`; run `python3 -m pytest -q -n 0 -s .shop/scratch/w173-2-research/probe_answer.py` (run: 6 passed). Each repository is a scratch git repo with `.shop/work/i1/w1.md` and a `log.jsonl`.

- Reviewer's question, log `claimed -> done`, `done -> awaiting-answer`; `work answer w1 "Rename the flag"`: rc 0, stdout `w1 done`, file `status: done`, log `before awaiting-answer, after done, by work answer`. (run)
- Same with `--change`: rc 2, `work: error: unrecognized arguments: --change`; file stays `awaiting-answer`. (run)
- Same with `--accept`: rc 2, `unrecognized arguments: --accept`; file stays `awaiting-answer`. (run)
- Implementer's question, log `ready -> claimed`, `claimed -> awaiting-answer`; `work answer w1 "Use the first reading"`: rc 0, `w1 ready`, file `status: ready`. (run, control)
- Work-item `awaiting-answer` in its file, log's last move into `done`: rc 1, stderr `... gives its status as awaiting-answer, but log.jsonl's last transition of w1 is to done; it is not moved`. (run)
- Work-item `done` in its file: rc 1, `w1 is not awaiting-answer; work answer answers only an awaiting-answer work-item or capability-proposal`. (run)

Nearest cases not given by scenarios, read only:
- A brief for a work-item with answers but no `## Questions` pairs: `answer_lines` returns `[]` (zip). (read, `scripts/supervise_brief.py:86-96`)
- Answers fewer than questions: zip pairs only the first; the unanswered question is absent from the brief. (read)
- A reviewer's question text is the reviewer's `questions` joined, or `bdd-task-reviewer gave <status>: <summary>` (`scripts/supervise_worker.py:outcome`, line 240). No findings path in the question. (read)

## 3. Old assumptions

Requirement r98 presumes a reviewer's answer returns the work-item to `ready`. Today `asked_from` returns a reviewer's `done`.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue_answer.py:ASKED_FROM | maps only `claimed -> ready`; a reviewer's `done` comes back as `done` | the reviewer's answer must reach `ready` by the flag route (work-queue r26) | by search: tests/scenarios/test_work_queue.py:79 (deprecated row `a reviewer \| done`) | grep; probe 1 |
| scripts/workqueue_answer.py:answer | takes `(root, name, text)`; no flag, no refusal for a reviewer's question | needs the `--change`/`--accept` flag and the r28 refusal without it (work-queue r26-r28) | by search: tests/scenarios/work_queue_answer_steps.py:12 (line-break case only) | grep; probe 1 |
| scripts/workqueue_answer.py:asked_from | returns `ASKED_FROM` of the last log move into awaiting-answer | for a reviewer's question, the flag decides the status, not the log | by search: called only from answer and supervise_answers.py:79; no test asserts it directly | grep |
| scripts/supervise_answers.py:79 | delegated answers: moves the item to `asked_from`'s status after the last open question | a delegated answer to a reviewer's question must take the flag route too | by search: tests/scenarios/supervision_delegation_steps.py (implementer and planner questions only) | grep (1-research) |
| scripts/supervise_brief.py:brief, `read` list | lists every run directory of the work-item, so the reviewer's directory is readable | r98 names the findings file in the brief; no line names it today | none (by search: no test asserts a findings line in a brief) | read |
| scripts/supervise_brief.py:answer_lines | writes each answer beside its question for every stage (r57) | already what r98 "writes the answer as r57 does"; no change | by search: tests/scenarios/test_supervision.py r57 test (not run) | read |

## 4. Tests the requirements make impossible to keep

`tools tests-of` has no map; by search and read (1-research, not re-opened by me unless stated):
- `features/work-queue.feature:286-298`, deprecated outline "answer on an awaiting-answer work-item transitions it to the status the asking stage started from (deprecated)", row `a reviewer | done`; bound at `tests/scenarios/test_work_queue.py:79`. It pins the plain-answer route that r28 refuses; it cannot pass once w174's r28 lands. It is tagged `@deprecated`, so the replacement rows (r26-r28) carry the behaviour. (read)
- `tests/scenarios/work_queue_answer_steps.py`: the line-break step is sound under r26-r28 (the flag does not touch it). (read this stage)
- `tests/scripts/`: no test asserts `asked_from` or `ASKED_FROM` (by search, this stage: no hit). Sound.
- `tests/scenarios/test_supervision.py` r57 test: sound under r98 (checked by read). Sound.
- r98 itself: no test (by search, this stage: none).

## 5. A step the work-item skips

The reviewer's answer skips the flag step that work-queue r26-r28 add. The existing way (`work answer`, probe 1 above) has no such step, so a reviewer's question is answered and moved to `done` with no choice recorded. The refusal only the flag step produces: `work answer` without the flag exits with an error and changes nothing (r28). Shown by probe 1 (run): plain answer returns rc 0 and status `done`. The delegated path, `scripts/supervise_answers.py:79`, skips it too (read).

## 6. Defects

### D1: a reviewer's question answered without the flag lands at `done`
Reproduction (run): `python3 -m pytest -q -n 0 -s .shop/scratch/w173-2-research/probe_answer.py::test_reviewer_plain_answer`. Came back: `w1 done`, rc 0, file `status: done`, log `before awaiting-answer, after done, by work answer`. The spec (work-queue r28, in `spec/capabilities/work-queue.md:46`, at base) says it shall exit with an error and change nothing. The question is answered as if a choice were made.

Not a defect, a gap the work-item depends on (run): `--change` and `--accept` are unknown options (rc 2) because work-queue r26-r27 are not in code yet (w174).

## 7. The file set

Files r98's scenario needs (none exists yet; the formulate round writes it, not w173):
- `scripts/supervise_brief.py` (143 lines, room 157): name the findings file of the work-item's last review stage directory in an implementer's brief. The answers are already written by `answer_lines`.
- `tests/scenarios/supervision_answers_steps.py` (52 lines, room 248): a Then for the findings line in the brief.
- `tests/scenarios/test_supervision.py` (258 lines, room 42): the binding for the new scenario, if bindings are listed in the file.
- `features/supervision.feature`: the `@r98` scenario (written by the formulate round, not by w173). It is a feature file; the 300-line limit covers Python only.

Open reading (both kept; no choice made here): where the findings path comes from. (a) the reviewer's `findings` result field (`agents/bdd-task-reviewer.md:62`: "the findings file's path"); (b) the newest `<k>-review` directory under `runs/<name>`, listed by `supervise_brief`'s `read` list. The reviewer's question text carries neither.

Files r98 needs only if its scenario reaches `ready` through `work answer` (work-queue r26-r28, the w174 item):
- `scripts/workqueue_answer.py` (59 lines, room 241): the flag, the `ready`/`done` routing and the r28 refusal.
- `scripts/work` (151 lines, room 149): the `--change`/`--accept` option on the `answer` subparser.
- `scripts/supervise_answers.py` (128 lines, room 172): the delegated path's `asked_from` call, if a delegated reviewer answer is in scope.

Modules on the change's path, not edited (lines, room): `scripts/supervise.py` (248, room 52; `held`, line 173), `scripts/supervise_worker.py` (247, room 53; `outcome`, `worker`), `scripts/workqueue.py` (290, room 10; `move`, `agrees`, `append`, `add` takes `findings=`). Limit 300 (CLAUDE.md).
