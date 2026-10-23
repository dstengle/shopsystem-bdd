# Research notes: w91 (work answer; awaiting-ruling renamed awaiting-answer)

Accepted: work-queue#r9, #r13, #r14. Base dc9ece7. Worktree clean at the end (`git status --porcelain` empty; `.shop/scratch/` is ignored).
Tools: `tools refs` ran (run). `tools tests-of` and `untested` have no map (`tools: no map`); I did not run `tools map` (it writes `.shop/scratch/tools` in the worktree, outside my scratch dir). Every test list below is `by search`.
Probe file: `.shop/scratch/w91-1-research/probe_work.py`.

## 1. Why each accepted scenario is red today

Scenario runs: `python3 -m pytest -q --tb=short -k <name> tests/scenarios/test_work_queue.py`, or by node id. All run.

- **r9 deprecated, 3 examples (add, retry, withdraw)**: PASS (run). Not red.
- **r9, 4 examples**: add, retry, withdraw PASS (run); **answer RED** (run). Failure in the Given, `tests/scenarios/test_work_queue.py:70` in `with_items`: `ValueError: not enough values to unpack (expected 2, got 1)`. The clause `its question asked by an implementer` is split off by `, ` and has no ` is `. Missing: a Given that reads the asker clause (test_work_queue.py:65-71), and a record of the asker (none defined, part 7). Code: `work answer` (scripts/work has no `answer` subcommand; workqueue.py has no answer function).
- **r13**: RED (run). pytest-bdd `StepDefinitionNotFoundError` for the Then at feature line 213 (`.shop/work/i1/w1.md has under its ## Answers the text "Use the first reading", with the date the command was run`). Its Given (line 211) matches `with_items`. Missing: that Then (no step in tests/scenarios), and the code: `work answer`.
- **r14, 4 examples**: all RED (run), each in the same Given at test_work_queue.py:70. Also missing: the transition in `work answer`, and `awaiting-answer` in the status sets (workqueue.py:16, model_work.py:12).

## 2. What the system answers today

Probes, `python3 -m pytest -q -s -n0 .shop/scratch/w91-1-research/probe_work.py` (each test rebuilds its own repo under the scratch dir). All run.

- `work --root R answer w1 "Use the first reading"`, w1 `awaiting-answer`: exit 2, `argument cmd: invalid choice: 'answer' (choose from 'add', 'show', 'withdraw', 'run', 'retry')`. Nothing changed (git status clean; w1 still `awaiting-answer`).
- `work show`, w1 `awaiting-answer`, w2 `awaiting-ruling`: exit 0, lists both with their statuses.
- `work withdraw w1` (awaiting-answer, no log.jsonl): exit 0, `w1 withdrawn`; commit `work withdraw: w1 awaiting-answer -> withdrawn`; log line `before: awaiting-answer, after: withdrawn`. Same for w2 (awaiting-ruling). `before` is not checked against STATUSES; only the target is (workqueue.py:128).
- `work withdraw w3` (ready, log says ready): exit 0; the commit holds exactly `.shop/work/i1/w3.md` and `.shop/work/i1/log.jsonl`; `git status --porcelain` empty after.
- `work withdraw w4` with no git repository: exit 1, `work: git rev-parse failed: fatal: not a git repository`; w4.md unchanged; no log.jsonl created.
- `supervise.Run(root,"i1").questions("w5")`, file with `## Questions` holding `Which module owns the log?`:
  - with `## Rulings` holding `Use the first reading`: `[]`.
  - with `## Answers` holding it instead: `['- Which module owns the log?']` (still open); `held("w5","Rulings")` is `[]`.
- Not probed, read only: an answer already under `## Answers`; `answer` on a file whose log's last move disagrees (r6: `agrees`, workqueue.py:162-175, would refuse).

## 3. Old assumptions

"Tests that execute it": no map, so `by search` names the test files that name the old form; `none` only where a search also finds no test.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue.py:16 STATUSES | lists `awaiting-ruling`; move refuses a target outside it | must list `awaiting-answer` (the rename) | by search: test_supervision.py:108, supervision_tests_steps.py:98 | refs workqueue.STATUSES |
| scripts/model_work.py:12 STATUSES | `model` flags a work-item status outside the set (model_work.py:204-210, read) | an `awaiting-answer` file is a model problem until the set changes | none (by search: no test under tests/scripts names an awaiting status) | grep, read |
| scripts/supervise.py:156 Run.stage | researcher, planner, reviewer question moves start status to `awaiting-ruling` | target renamed; `before` is drafted, researched, done: matches r14 | by search: test_supervision.py:108, supervision_faults_steps.py:125 | grep, read |
| scripts/supervise.py:237, 245 Run.run | prints questions for `awaiting-ruling`; exit 3 for it | renamed in both | by search: test_supervision.py:108 | grep, read |
| scripts/supervise.py:207-209 Run.questions | open questions: `## Questions` bullets past `## Rulings` ones | r13 writes under `## Answers`; this reads only `## Rulings`: an answer stays open (probe) | by search: supervision_given.py:114-117, test_supervision.py:200-205, supervision.feature:672-675 | probe, grep |
| scripts/supervise_merge.py:88, 106 Merge.failed_claimed, Merge.claimed | an implementer's question moves `claimed` to `awaiting-ruling`; log `before` is `claimed` | r14 wants `ready` for an implementer's question; a rule on the log's `before` would give `claimed` (part 7, question 3) | by search: supervision_faults_steps.py:125 | grep, read |
| scripts/measure_build.py:76 | counts log `to` == `awaiting-ruling` as `awaiting_ruling` | value and key change, or old history stays | by search: batch_measurement_then_steps.py:110-113; batch-measurement.feature:84-102 | grep |
| scripts/measure_show.py:13; scripts/measure:22 | key `awaiting_ruling`; prose | rename or keep | by search: batch_measurement_then_steps.py | grep |
| scripts/work (no answer subcommand) | argparse rejects `answer` (probe) | new subcommand | none (no test runs it) | probe |
| prose: skills/delivering-an-initiative/SKILL.md:51, skills/analyzing-a-batch/SKILL.md:19, skills/formulating-features/SKILL.md:103, agents/bdd-planner.md:14, agents/bdd-task-reviewer.md:14, docs/design-model/design-model.md:106,121,140-142,203, docs/capability-format.md:140 | name `awaiting-ruling` or `## Rulings` | out of date after the rename | not searched for test reads (not run) | grep |

Also: migrate r29 (spec/capabilities/migration-tools.md:49; features/migration-tools.feature:527-529) renames the status and `## Rulings` in existing files. grep finds no `awaiting-answer` in scripts: not built. Read only.

## 4. Tests the requirements make impossible to keep

Not mapped: searched by text (`by search`). Not run: `work_items.py:107` refuses a `-k` subset of the accepted scenarios ("accepts none of the scenarios it collected"), so the supervision tests are `read` only.

- tests/scenarios/test_supervision.py:108-110 (`awaiting` step asserts `awaiting-ruling`): impossible under reading A of part 7 question 1 (rename work run's status now). Under reading B it keeps passing. The supervision.feature scenarios naming awaiting-ruling (lines 86, 111, 139, 228-234, 250-251, 518, 696) follow the same reading.
- tests/scenarios/test_supervision.py:200-205 and supervision.feature:672-675 (`## Rulings`): impossible under reading A of question 2 (questions() reads `## Answers`); under B they keep passing, and r13's answers never close a question (probe 6.1).
- tests/scenarios/supervision_given.py:114-117 (writes `## Rulings`) and supervision_faults_steps.py:125-129 (writes `awaiting-ruling` and `## Rulings`): the same two readings.
- tests/scenarios/supervision_tests_steps.py:98-101 (Given w2 `awaiting-ruling`): still runs under both readings (agrees does not check membership); its data is stale under A.
- tests/scenarios/batch_measurement_then_steps.py:110-113 and features/batch-measurement.feature:84-102 (counts `awaiting-ruling` transitions): impossible under A unless the counter keeps the old value.
- tests/scenarios/test_work_queue.py:65-71 (`with_items`): cannot read `, its question asked by X`; red today for r9 answer and r14, must change.
- tests/scripts/test_work_withdraw.py, test_work_items.py, test_work_add_title.py: by search, name no awaiting status and no Rulings; add, retry and withdraw are unchanged by r13 and r14. Sound by search; not run.

## 5. A step the work-item skips

`work answer` skips `workqueue.committed()` (workqueue.py:229-244) unless it uses it. What only that path produces:
- Refusal before any write when not in a git repository: probe (`work withdraw` in a non-git dir: exit 1, file unchanged, no log). From `git rev-parse --is-inside-work-tree` (workqueue.py:233).
- A commit of only the files named: probe (commit holds w3.md and log.jsonl). r9 needs it.
- Commit failure restores the files: read (workqueue.py:237-244).
- Log-write failure restores the file: read (`move`, workqueue.py:137-143).
- r6 agreement check before a move: read (`agrees`, workqueue.py:162-175). `answer` needs it, or a file whose log disagrees is written.
- The `## Answers` writer is `supervise.Run.section` (supervise.py:105-118), an instance method on Run. `work answer` cannot reuse it without importing supervise into scripts/work. Read.

## 6. Defects

Not fixed, not judged.

### 6.1 A `## Answers` section does not answer a question (run)
Repro: `python3 -m pytest -q -s -n0 .shop/scratch/w91-1-research/probe_work.py` (test_e). A file with `## Questions` holding `Which module owns the log?` and `## Answers` holding `Use the first reading`: `Run.questions("w5")` returns `['- Which module owns the log?']`. With `## Rulings` it returns `[]`. Shows at the new heading; today no code writes `## Answers`.

### 6.2 A Given's clause fails as a ValueError (run)
Repro: `python3 -m pytest -q -n0 -k test_answer_on_an_awaitinganswer_workitem_transitions tests/scenarios/test_work_queue.py`: `tests/scenarios/test_work_queue.py:70: ValueError: not enough values to unpack (expected 2, got 1)`. The asker clause is parsed as a work-item.

## 7. The file set

Production:
- scripts/workqueue.py (255 lines; room 45): STATUSES rename; the answer transition, through `committed`. Shown by refs workqueue.STATUSES and workqueue.committed.
- scripts/work (71; room 229): `answer` subcommand, like cmd_withdraw. Read.
- scripts/model_work.py (211; room 89): status set. Read.
- scripts/supervise.py (263; room 37): `awaiting-ruling` at 156, 237, 245; questions() `## Rulings` at 209 (reading-dependent). Little room: a split may come first (CLAUDE.md).
- scripts/supervise_merge.py (132; room 168): targets at 88, 106. Read.
- scripts/measure_build.py (112; room 188), scripts/measure_show.py (76; room 224), scripts/measure (prose only): the `awaiting_ruling` count. Grep.
- A new module for the answer path, e.g. scripts/workqueue_answer.py: CLAUDE.md says a new concern gets a new module and a module-map row (CLAUDE.md module map). workqueue.py has room 45; the answer transition and the Answers writer may not fit.

Tests:
- tests/scenarios/test_work_queue.py (277; room 23): the `with_items` Given (65-71). Room 23 only: new steps go in a new module, imported as the work_queue_*_steps are (test_work_queue.py:20-23).
- tests/scenarios/work_queue_answer_steps.py (new): the r13 Then and the asker Given.
- tests/scenarios/test_supervision.py (236; room 64): 108-110, 200-205 (reading-dependent).
- tests/scenarios/supervision_given.py (232; room 68), supervision_faults_steps.py (186; room 114), supervision_tests_steps.py (163; room 137): old-name data (reading-dependent).
- tests/scenarios/batch_measurement_then_steps.py (158; room 142): the `awaiting_ruling` assertion (reading-dependent). features/batch-measurement.feature is a feature file.
- features/supervision.feature: scenarios naming awaiting-ruling and Rulings (reading-dependent). A feature file.

Modules on the change path, with line counts (`wc -l`) and room under 300 (CLAUDE.md): scripts/work 71 (229), scripts/workqueue.py 255 (45), scripts/model_work.py 211 (89), scripts/supervise.py 263 (37), scripts/supervise_merge.py 132 (168), scripts/measure_build.py 112 (188), scripts/measure_show.py 76 (224). Tests: test_work_queue.py 277 (23), test_supervision.py 236 (64), supervision_given.py 232 (68).

Open for the plan (both readings; not decided here):
1. Rename scope. (A) rename every `awaiting-ruling` in work, model, supervise and measure now. (B) keep the old name on the supervision path. The work-item says the rename is its own, "in the lifecycle the code keeps (`work`, `model`, `work run`)".
2. Where the answer lives. (A) questions() reads `## Answers` (r13's place). (B) it keeps reading `## Rulings`; then `work answer` answers never close a question in `work run`.
3. The asker. (A) the log line into awaiting-answer records `before`: the stage's start for researcher, planner and reviewer, but `claimed` for an implementer (supervise_merge.py:88, 106), so claimed to ready needs a rule. (B) a record in the file; the scenario's Given "its question asked by X" names none.
