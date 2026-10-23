# Plan of w92: work run carries a work-item's answers and keeps going on its branch

Accepts supervision#r5, r26, r32, r36, r37, r57, r58. Rests on decisions 0063 (a-ruling-returns-to-the-asking-stage), 0064 (answers-not-rulings), 0011 (held-scenarios), 0006 (feature-files-read-only-in-red-green) and the capability's rests_on. The work-item has no `## Rulings`/`## Answers` and no Retires section; part 1 gives what decision 0011 retires.

## 1. What goes green

The notes found these red today. They ran a child pytest without the worker guard (see decision 5).

- **r5**, "an implementer's DONE whose <tests> fail makes the work-item's transition to awaiting-answer", both rows: the Then "w1 is awaiting-answer" has no step, and supervise_merge.py writes awaiting-ruling when the tests fail.
- **r5**, "a researcher that gives <outcome> makes the work-item's transition to awaiting-answer", rows QUESTION, BLOCKED and NEEDS_CONTEXT: the same missing Then, and Run.stage in supervise.py writes awaiting-ruling.
- **r32**, "when no work-item can make a transition and one is awaiting-answer, `work run` exits with an error, …": work run prints `w1 awaiting-ruling`. It prints open questions, and exits 3, only for awaiting-ruling.
- **r32**, "`work run` prints a question that has no answer yet, and not one that has an answer": the Given for awaiting-answer with an Answers section has no step, and Run.questions pairs `## Questions` with `## Rulings`.
- **r36**, "a question goes into the work-item's ## Questions, before a section that follows it": the Given with an Answers section has no step. Run.section is generic, so the step is the only thing missing.
- **r57**, "the brief of a worker for a work-item that has answers holds each answer with the question it answers": the Given has no step, and Briefs.brief reads no `## Answers`.
- **r58**, "an implementer started for a work-item whose work-item branch was kept works in a worktree on that branch": the kept-branch Given has no step, and Workers.worktree always adds `-b`, which git refuses when the branch already exists (the researcher ran this).
- Already green and must stay green: r26 "a work-item whose transition is to awaiting-answer keeps its work-item branch"; r37 "no worker is started for a work-item that is <status>" (both rows); r37 "no worker is started for a work-item after its transition to awaiting-answer".

**Retired** (decision 0011: "the work-item that turns its replacement green lists it under Retires: and removes it with `features retire`"; decision 0006 lets a task retire a deprecated scenario it lists). w92 turns the replacements of these green, so it retires them with `features retire`:
- "an implementer's DONE whose <tests> fail makes the work-item's transition to awaiting-ruling (deprecated)" (@r5)
- "a researcher that gives <outcome> makes the work-item's transition to awaiting-ruling (deprecated)" (@r5)
- "when no work-item can make a transition and one is awaiting-ruling, `work run` exits with an error, printing each work-item's status and each open question (deprecated)" (@r32)
- "`work run` prints a question that has no ruling yet, and not one that has a ruling (deprecated)" (@r32)
- "a work-item whose transition is to awaiting-ruling keeps its work-item branch (deprecated)" (@r26)
- "a question goes into the work-item's ## Questions, before a section that follows it (deprecated)" (@r36)
- "no worker is started for a work-item that is <status> (deprecated)" (@r37)

Not retired: "an implementer's DONE whose whole suite fails only on a scenario r43 counts as expected is merged (deprecated)" (@r4). r4 is not w92's.

## 2. Where the change lands

- `scripts/supervise.py`: Run.stage writes awaiting-answer. Run.run prints open questions, and exits 3, for awaiting-answer. Run.questions pairs `## Questions` with `## Answers`. 37 lines of room.
- `scripts/supervise_merge.py`: Merge.claimed and Merge.failed_claimed move to awaiting-answer, and the docstrings change to match.
- `scripts/supervise_brief.py`: Briefs.brief writes each answer next to the question it answers (r57).
- `scripts/supervise_worker.py`: Workers.worktree checks out the existing work-item branch, without `-b`, when that branch is already there (r58).
- `scripts/workqueue.py`: STATUSES lists awaiting-answer, if the base does not list it yet (decision 1).
- `features/supervision.feature`: only the `features retire` of the seven scenarios above.
- `tests/scenarios/test_supervision.py`: the scenarios' env leaves out SHOPSYSTEM_WORK_RUN_WORKER (decision 5). The awaiting-ruling Then becomes the awaiting-answer Then. Remove the Questions-then-Rulings step, which only the retired r36 row used. Import the new steps module.
- `tests/scenarios/supervision_given.py`: the Rulings variant of `item_with_sections` becomes an Answers variant (r36).
- `tests/scenarios/supervision_faults_steps.py`: the awaiting-ruling Given with no ruling becomes the awaiting-answer Given with an answer and without one (r32).
- `tests/scenarios/supervision_answers_steps.py` (new): the r57 Given and Then, and the r58 kept-branch Given and its Then, if no existing Then covers it. It is a new module because supervision_then_workers.py has only 24 lines of room.

Removed from the researcher's set:
- `scripts/model_work.py`: no requirement of w92 observes `model`. The model's status set is w91's (w91 plan, part 2).
- `agents/bdd-planner.md` and `agents/bdd-task-reviewer.md`: no accepted requirement observes the agents' text. Under r57 the brief carries the answers.
- `tests/scenarios/supervision_tests_steps.py`: its `w2 is awaiting-ruling` Given serves only r4's rows, which are not w92's. It survives the rename.

Out of the set (measure_build.py, measure_show.py): batch-measurement#r41 is w94's.

## 3. Decisions

1. **w92 makes the rename in `work run`** (researcher's Q1). work run writes awaiting-answer and reads `## Answers` wherever supervise*.py wrote awaiting-ruling or read `## Rulings`. This rests on supervision#r5, r26, r32, r36 and 0064: only w92 accepts the scenarios that observe it. If w91 has already merged a part of it when the implementer starts, that part stays as it is. w92 adds awaiting-answer to workqueue STATUSES if it is missing, because move() refuses any status not listed there (r5 cannot be met otherwise). w92 does not remove awaiting-ruling from STATUSES. That set, and how work-items still on disk with awaiting-ruling are treated, are w91's (its open question) and w93's (migration-tools#r29).
2. **The deprecated rows are retired, not kept** (researcher's Q2): decisions 0011 and 0006, as listed in part 1. If they were kept they would contradict r5, r26, r32, r36 and r37, and under r4 `--work-item w92` would never let w92 merge.
3. **Answers pair with questions by position**: the n-th bullet of `## Answers` answers the n-th bullet of `## Questions` (supervision Implementation, design-decision/answers-not-rulings). Run.questions prints a question that has no n-th answer (r32), and Briefs.brief writes each answer with its question (r57). This holds for the brief of every stage's worker (0063: "the brief of every worker it starts for it").
4. **A kept branch is reused, not re-created** (r58, 0063). When work/<name> exists, the implementer's worktree is made on it with its commits. Otherwise the worktree is made as today.
5. **The scenarios' `work run` does not inherit the worker guard** (researcher's Q3, defect D1). The scenario harness builds its env without SHOPSYSTEM_WORK_RUN_WORKER. The r21 scenario still sets it itself, through BY_WORKER in supervision_world.py. Workers keep setting it: r21 needs it in production. This rests on the capability's narrator, the person who started `work run`, who is not a worker. The scenario world is that person's world.
6. **The exit code is not asserted** (researcher's Q5). r32 says only "exit with an error" (design-decision/exits-are-successful-or-errors). Exit 3 is Implementation, which "may change". The code keeps 3, now for awaiting-answer. No scenario is added for it.
7. **Measure is not w92's** (researcher's Q4): batch-measurement#r41 is accepted by w94.

## 4. Tests the decisions break

- test_supervision.py, the `is awaiting-ruling$` Then (around line 108): decision 1 makes it untrue. It is rewritten to assert awaiting-answer. Its users are the retired r5 rows.
- test_supervision.py, the `sections` step for Questions then Rulings (around lines 200-207): only the retired r36 row uses it. It is removed when that row is retired (decision 2).
- supervision_given.py, `item_with_sections` with Rulings (around lines 114-117): it is used only by the retired r36 row. It is rewritten to the Answers form that the r36 replacement needs.
- supervision_faults_steps.py, the awaiting-ruling Given for a question with no ruling (around lines 125-130), and its Then in test_supervision.py (around lines 247-255): decision 3 makes questions() ignore `## Rulings`, so the old row would print "Old question?". The Given is rewritten to awaiting-answer with `## Answers`. Its old row is retired.
- test_supervision.py, the env builder (around line 40): decision 5. It is rewritten to leave the guard out. The r21 scenario is unaffected because it adds the guard itself (verified: BY_WORKER in supervision_world.py is the only place the tests name it).
- supervision_tests_steps.py's `w2 is awaiting-ruling` Given (r4): it is unaffected because the status is not MOVABLE. It is left alone.
- batch_measurement tests: they are unaffected, because measure does not change.

## 5. Open cases (for the implementer to name, not to choose)

- More answers than questions, an empty `## Questions`, and a question or answer bullet with continuation lines (Run.held reads continuation lines for questions).
- The exact text of a question-and-answer pair in the brief, beyond what the r57 Then checks.
- The kept branch and r24: the whole suite runs before the implementer starts, but the rebase onto the initiative branch happens only in merge(). On a kept branch the pre-run sees a branch that has not been rebased (notes, part 5).
- On a kept branch, changes to .shop/work/ that it already holds are put back (under_work) only in merge(), not before the pre-run.
- Merge.failed_claimed's path to awaiting-answer: no scenario reaches it.
- D2: a kept branch left by a Fault in merge(), followed by `work retry`, reaches Workers.worktree. Decision 4 covers that, but no scenario runs it end to end.
