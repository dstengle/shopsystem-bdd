# Research of w92: work run carries a work-item's answers and keeps going

Method. Work-item w92 and capability supervision read. No coverage map: `tools tests-of` says "no map", so every test list here is `by search` (grep over tests/). `tools refs` ran (it works without a map). `tools size --limit 300` printed nothing: no tracked Python file is over 300 lines. Scripts: `/home/vscode/shopsystem-bdd/scripts/tools`.
w92 has no `fileset:` and no `Retires` section. Its accepted scenarios: 25 test ids (the 25 in probe_accepted.py), 15 green today, 10 red.

**Caveat, read first (see Part 6, D1).** This research session is itself a worker of w92's `work run`, so `SHOPSYSTEM_WORK_RUN_WORKER=w92` is in the environment. Run as is, `work run` refuses in 21 of 25 scenarios. All results below come from a child pytest with that variable removed (probe_accepted.py), so they show the scenarios' own outcome.

## 1. Why each accepted scenario is red today

Probe: `python3 -m pytest -q -n0 .shop/scratch/w92-1-research/probe_accepted.py` (run; result in accepted_result.txt).

Red today (run):
- r5 `an implementer's DONE whose <tests> fail makes ... awaiting-answer` [the work-item's scenarios], [the whole suite]: `StepDefinitionNotFoundError: Then "w1 is awaiting-answer"` (test_supervision.py:108 defines only `is awaiting-ruling$`). Even with the step, the code writes awaiting-ruling: supervise_merge.py:106 (`self.move(name, "claimed", "awaiting-ruling", question)`).
- r5 `a researcher that gives <outcome> makes ... awaiting-answer` [QUESTION], [BLOCKED], [NEEDS_CONTEXT]: same undefined Then. Code: supervise.py:156 writes `"awaiting-ruling"`.
- r32 `when no work-item can make a transition and one is awaiting-answer ... exits with an error`: AssertionError, `w1 awaiting-ruling`, `  - Which module owns the log?`, `w2 green`; expected awaiting-answer. Code: supervise.py:237 (prints questions only for awaiting-ruling), supervise.py:245 (exit 3 only for awaiting-ruling).
- r32 `work run prints a question that has no answer yet, and not one that has an answer`: undefined Given `i1's work-item w1 is awaiting-answer, its ## Questions section ... and no answer` (supervision_faults_steps.py:125 matches only awaiting-ruling). Code: supervise.py:206-209 `questions()` pairs `## Questions` with `## Rulings`, not `## Answers`.
- r36 `a question goes into the work-item's ## Questions, before a section that follows it`: undefined Given `... and then an Answers section with "Old answer."` (supervision_given.py:114 matches only Rulings). Code: supervise.py:105-118 `section()` is generic, so the step is the only gap (read; the deprecated Rulings twin passes, run).
- r57 `the brief of a worker for a work-item that has answers holds each answer with the question it answers`: undefined Given `... its ## Questions ... and its Answers section with "The queue module." and "No."`. Code: supervise_brief.py:19-50 `brief()` reads no `## Answers` (read).
- r58 `an implementer started for a work-item whose work-item branch was kept works in a worktree on that branch`: undefined Given `i1's work-item w1 is ready, and the branch work/w1 was kept with a commit of kept.txt`. Code: supervise_worker.py:113-125 `worktree()` always adds `-b`; with an existing branch git refuses (probe_kept_branch.py, run: `fatal: a branch named 'work/w1' already exists`, exit 255). Without `-b` git makes the worktree with kept.txt in it (run).

Green today (run; 15 of 25):
- r5 deprecated (awaiting-ruling): implementer [both rows]; researcher [all three rows].
- r32 deprecated exit; r32 deprecated `prints a question that has no ruling yet`.
- r26 awaiting-answer keeps branch, and its deprecated twin.
- r36 deprecated (Rulings twin).
- r37 `no worker ... awaiting-answer` [row], `[failed]`; `no worker ... after its transition to awaiting-answer`; deprecated awaiting-ruling and failed rows.

Note: `no worker is started for a work-item that is awaiting-answer` passes for the wrong reason. The status is never written: workqueue.agrees (workqueue.py:162-175) accepts any string, and the run loop's MOVABLE (supervise.py:33) excludes it. The same holds for the deprecated awaiting-ruling row.

## 2. What the system answers today

Probes, all run through `scripts/work` as the scenario harness runs it (no separate probe needed; their results are in Part 1):
- Researcher QUESTION (deprecated scenario): w1 becomes awaiting-ruling, the question printed, exit nonzero. run.
- Researcher BLOCKED / NEEDS_CONTEXT: same route (run, deprecated rows pass). read: outcome() (supervise_worker.py:203-210) makes the question `"<agent> gave <status>: <summary>"` when no question is given.
- Work-item with `## Questions` and `## Rulings`, one question ruled: printed nothing for it (run; deprecated `no ruling yet` row passes).
- Work-item file says awaiting-answer, log says otherwise: refused by agrees() (read, workqueue.py:172-174). Not run.
- Nearest cases not probed (read only): empty `## Questions`; a `## Answers` with more bullets than questions; a question with continuation lines (held() handles them, supervise.py:193-204).

## 3. Old assumptions

Requirement changes: awaiting-ruling becomes awaiting-answer; `## Rulings` becomes `## Answers` (r5, r32, r36, r57).

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue.py:16 STATUSES | lists awaiting-ruling, not awaiting-answer | move() refuses any other status (workqueue.py:128-129): work run cannot write awaiting-answer until it is listed | none (no test names awaiting-ruling outside test_supervision and batch-measurement) | refs STATUSES; grep awaiting |
| scripts/model_work.py:12 status set | lists awaiting-ruling | the model's work-item statuses need the same name; w91's scope | none by search | refs STATUSES; grep |
| scripts/supervise.py:156 Run.stage | writes awaiting-ruling on a question | must write awaiting-answer (r5) | test_supervision r5 rows (red by step) | grep awaiting |
| scripts/supervise.py:237-239 Run.run | prints open questions for awaiting-ruling | must do so for awaiting-answer (r32) | r32 awaiting-answer exit row (red); r32 deprecated exit (green) | read; run |
| scripts/supervise.py:245 Run.run | exit 3 only for awaiting-ruling | Implementation says 3 for awaiting an answer | none: every test asserts only nonzero (`exits with an error`) | read; grep returncode |
| scripts/supervise.py:206-209 Run.questions | pairs Questions with Rulings | pairs Questions with Answers (r32) | r32 no-answer row (red); deprecated no-ruling row (green) | read; refs questions |
| scripts/supervise.py:105-118 Run.section | writes question before any following heading | unchanged; covers Answers (r36) | r36 deprecated row (green); r36 answer row (red by step) | read; refs section |
| scripts/supervise_merge.py:106 Merge.claimed | tests fail: claimed to awaiting-ruling | must be awaiting-answer (r5, r26) | r5 implementer rows (red by step); r26 row (green) | read; grep |
| scripts/supervise_merge.py:82-91 Merge.failed_claimed | any non-fault error: claimed to awaiting-ruling | must be awaiting-answer | none: no step makes the implementer raise an unclassed error | read; grep |
| scripts/supervise_merge.py:71, 82 docstrings | say awaiting-ruling | text only | none | grep |
| scripts/supervise_brief.py:19-50 Briefs.brief | no answers lines | adds each answer beside its question (r57) | r57 (red by step) | read; grep Answers |
| scripts/supervise_worker.py:113-125 Workers.worktree | `git worktree add -b` always | fails when the kept branch exists (r58) | r58 (red by step); none otherwise | run (git probe); read |
| scripts/measure_build.py:76 | counts transitions to awaiting-ruling | new runs write awaiting-answer, so the count reads 0 | batch_measurement_then_steps.py:110-113 (fixture uses awaiting-ruling: green) | grep |
| scripts/measure_show.py:13 ITEMS | output key awaiting_ruling | same count | batch_measurement tests by search | grep |
| agents/bdd-planner.md:14, agents/bdd-task-reviewer.md:14 | tell the agent to read `## Rulings` | answers now under `## Answers` | none (test_agents.py does not name it) | grep Rulings |
| skills/delivering-an-initiative/SKILL.md:51 | describes awaiting-ruling output | text | none | grep |
| docs/design-model/design-model.md:106,121,203; grammar.md:229; capability-format.md:117,140 | awaiting-ruling in the lifecycle | text | none | grep |
| features/migration-tools.feature:527-533 | upgrade step renames awaiting-ruling and ## Rulings | existing work-items on disk keep the old form until upgraded (not w92's) | migration_upgrade_steps.py, by search | grep |

Unchanged and sound: STAGES and MOVABLE (supervise.py:27-33). awaiting-answer is not movable, so no worker starts (r37, run).

## 4. Tests the requirements make impossible to keep

By search (no map). Every test naming awaiting-ruling, Rulings or the old form:
- test_supervision.py:108-110 `awaiting` step (`is awaiting-ruling$`): kept only for the deprecated rows; the awaiting-answer rows need a new step. With the rename it fails every deprecated row that uses it: the r5 implementer [2 rows] and researcher [3 rows] deprecated tests (run: pass today, fail after the rename, because status is awaiting-answer).
- test_supervision.py:200-207 `sections` step (Questions then Rulings): passes after the rename (section() unchanged), but asserts Rulings. Keep for the deprecated r36 row only.
- r32 deprecated exit row (feature line 228-234): `awaiting-ruling` printed; fails after the rename.
- r32 deprecated no-ruling row (supervision_faults_steps.py:125-130 and test_supervision.py:247-255): prints `Old question?` after the rename, since questions() no longer skips it. Fails.
- supervision_given.py:114-117 `item_with_sections` (Rulings): used only by the deprecated r36 row. Survives.
- supervision_tests_steps.py:98-102 `w2 is awaiting-ruling` (r4 deprecated row, feature line 86): passes today; survives the rename (not MOVABLE).
- Sound, verified (run): the r26 and r37 rows; the r5/r26 branch assertion (`git lists the branch work/w1`) does not depend on the status name.
- The r4 awaiting-answer row (feature line 96): not accepted by w92; red today (no `w2 is awaiting-answer` step, grep tests: no awaiting-answer at all).

## 5. A step the work-item skips

- r58 kept branch (Merge.claimed, supervise_merge.py:93-111): suite_record runs the whole suite on the kept branch before the implementer starts (r24), but the rebase onto the initiative branch happens only in merge() after the worker (supervise_merge.py:117-118). On a kept branch the pre-run suite sees an unrebased branch. Read; not run.
- The same kept branch: under_work (supervise_merge.py:55-66) runs only in merge(). A kept branch that already has .shop/work/ changes is not put back before the pre-run. Read.

## 6. Defects

### D1. A worker's pytest carries the worker guard; the supervision scenarios refuse
Reproduction (run, from this worker session): `python3 -m pytest -q --tb=line -rfE -p no:cacheprovider <the 25 accepted node ids>` gives `21 failed, 4 passed`. Each failure is `assert ... == 'awaiting-ruling'` with stderr `work: it was started by a worker of another \`work run\` (of w92); a worker starts no delivery`. Same ids with SHOPSYSTEM_WORK_RUN_WORKER removed (probe_accepted.py): 15 pass, 10 red as in Part 1.
Mechanism: with_scripts(plugin=True) (supervise_worker.py:67-69) sets the variable for every worker's pytest. test_supervision.py:40-43 builds the scenarios' env with dict(os.environ, ...), so the scenarios' `work run` inherits it. A worker's own check of the supervision scenarios therefore refuses for every work-item.

### D2. A kept branch fails the work-item on git's refusal (not run end to end)
Read: claimed() (supervise_merge.py:93-98) calls worktree(name, name, "work/"+name) outside its try; the GitFailed from `worktree add -b` reaches implement() (supervise_merge.py:75), which fails the work-item. Reached today when a Fault or a git failure in merge() leaves work/<name> behind (merge's Fault path, supervise_merge.py:121-122, keeps the branch) and `work retry` returns the work-item to ready. Git half run: probe_kept_branch.py. End-to-end not run.

## 7. The file set

Production:
- scripts/workqueue.py: STATUSES awaiting-answer for awaiting-ruling (line 16). refs STATUSES. w91's scope (see Questions).
- scripts/supervise.py: move target (156), prints and exit 3 (237, 245), questions() reads Answers (206-209). grep awaiting, Rulings.
- scripts/supervise_merge.py: awaiting-answer at 88 and 106; docstrings. grep awaiting.
- scripts/supervise_brief.py: answers beside questions in brief(), as research_questions does (r57). read.
- scripts/supervise_worker.py: worktree() without `-b` when the branch exists (r58). run (git probe).
- scripts/model_work.py: status set (line 12), if `model` reads it for work-items. refs STATUSES.
- agents/bdd-planner.md, agents/bdd-task-reviewer.md: read `## Answers` (line 14). Not needed for a scenario.
Tests:
- tests/scenarios/test_supervision.py: `is awaiting-answer` Then step; keep or retire the awaiting-ruling rows (Questions).
- tests/scenarios/supervision_given.py (232 lines): Given with Questions and Answers (r36, r57); Answers variant.
- tests/scenarios/supervision_faults_steps.py (186): awaiting-answer Given with and without an answer; kept-branch Given (r58).
- tests/scenarios/supervision_tests_steps.py (163): `w2 is awaiting-answer` Given (r4 row, not w92's).
- New module tests/scenarios/supervision_answers_steps.py (proposed): the brief's answers Then (r57) and the Answers Givens. supervision_then_workers.py has 24 lines of room (276): do not add there.
Not expected to change: scripts/work, scripts/work_items.py, scripts/supervise_faults.py, scripts/supervise_review.py, tests/scenarios/supervision_world.py. Read; no requirement of w92 touches them.

Modules on the change's path, with line count and room under 300 (wc -l):
- scripts/supervise.py: 263 lines, room 37.
- scripts/supervise_merge.py: 132, room 168.
- scripts/supervise_brief.py: 97, room 203.
- scripts/supervise_worker.py: 210, room 90.
- scripts/supervise_faults.py: 160, room 140 (on the path: fail, section, push; not edited).
- scripts/supervise_review.py: 77, room 223 (branch review; not edited).
- scripts/workqueue.py: 255, room 45.
- scripts/model_work.py: 211, room 89.
- scripts/work: 71, room 229 (entry; not edited).
- scripts/work_items.py: 109, room 191 (pytest plugin; not edited).
- tests/scenarios/supervision_faults_steps.py: 186, room 114.
- tests/scenarios/supervision_given.py: 232, room 68.
- tests/scenarios/supervision_tests_steps.py: 163, room 137.
- tests/scenarios/supervision_then_workers.py: 276, room 24.
- tests/scenarios/supervision_world.py: 172, room 128.
- tests/scenarios/test_supervision.py: 236, room 64.

## Questions for the planner (both readings given)

Q1. Who renames awaiting-ruling to awaiting-answer in work run? w91.md Questions says the rename is w91's, and w92 builds on it. w91 is itself awaiting-ruling at its last commit (bb2476d), with that question open. Reading A (w91 renames now): work run writes awaiting-answer, and workqueue STATUSES and supervise*.py change in w91; w92's rows then go green early, and the deprecated rows listed in Part 4 go red. Reading B (w92 renames): w91 leaves work run alone and w92 changes STATUSES, supervise.py and supervise_merge.py. Both readings: the accepted scenarios need STATUSES to list awaiting-answer (workqueue.py:16).
Q2. The accepted list has 10 deprecated rows that assert awaiting-ruling or ## Rulings (feature lines 103, 132, 228, 246, 517, 668, 685, and their twins). w92 has no Retires section. Reading A: retire them (a Retires section, or deleting the deprecated rows). Reading B: keep them as accepted, so they fail after the rename.
Q3. D1: should the scenarios' env drop SHOPSYSTEM_WORK_RUN_WORKER (test_supervision.py:40), or should a worker's pytest not set it? Both readings change the scenarios' result, not the code.
Q4. r41 of batch-measurement (spec) and its awaiting-answer scenario (batch-measurement.feature:107) are not in w92. measure_build.py:76 counts the new name. Is that in w92, or another work-item?
Q5. Exit 3 for awaiting-answer (Implementation) is untested: every scenario asserts only a nonzero exit. Should w92's scenarios assert 3?
