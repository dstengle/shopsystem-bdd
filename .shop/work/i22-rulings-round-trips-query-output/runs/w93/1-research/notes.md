# w93 research: the 0.25.0 step renames awaiting-ruling and ## Rulings

Tools: `tools refs` and `tools size` ran from the Scripts path. `tools tests-of` has no map (`no map: make one with tools map`), so test lists are `by search`. Probes are in `.shop/scratch/w93-1-research/` (`probe_upgrade_today.py`, `probe_sequence.py`), ignored by git.

Accepted: `migration-tools#r29`, scenario `features/migration-tools.feature` line 524.

## 1. Why each scenario is red today

Scenario: the upgrade step of the plugin version after 0.24.0 renames the old status and the old heading in work-items and logs.

Command (run): `python3 -m pytest -q "tests/scenarios/test_migration_tools.py::test_the_upgrade_step_of_the_plugin_version_after_0240_renames_the_old_status_and_the_old_heading_in_workitems_and_logs"`

Fails (run): `StepDefinitionNotFoundError` for Given "a repository on the final layout whose .shop/plugin-version is 0.24.0" (feature line 526). pytest-bdd stops at the first undefined step.

Other undefined steps (read; search of `tests/scenarios/` finds no step for them):
- feature lines 527-528: work-item files with a status and a `## Rulings` heading. Existing `item` steps match only `work-items <rels>` (`migration_upgrade_steps.py:75`) and the blocked_by/depends_on forms (`:82`, `:88`).
- feature line 529: a log.jsonl line naming awaiting-ruling.
- feature lines 531-533: the three Thens (status awaiting-answer, heading `## Answers`, log line).
- Step modules load by `from .migration_upgrade_steps import *` (`test_migration_tools.py:14`); a new module needs that import too.

Code missing (read):
- `scripts/migrate_upgrade.py:16` `STEPS` has only the 0.24.0 step.
- No module holds an r29 plan (`plan(root)` returning a `Changes`, as `scripts/migrate_upgrade_ids.py:94` does).
- `.claude-plugin/plugin.json` is 0.24.0, so `pending()` (`migrate_upgrade.py:32-35`) returns no 0.25.0 step. Even with the steps defined, the When prints "no upgrade step is pending" (probe 1, run), and the Thens fail.

## 2. What the system answers today

Probe 1: `probe_upgrade_today.py::test_at_0_24_0_status_and_upgrade_leave_awaiting_ruling` (run). Givens: plugin-version 0.24.0; `.shop/work/i1/w1.md` status awaiting-ruling with `## Rulings`; `w2.md` status done with `## Rulings`; `log.jsonl` with w1's line (after awaiting-ruling).
- `migrate status`: rc 0; repository 0.24.0, plugin 0.24.0; no pending step.
- `migrate upgrade`: rc 0, "no upgrade step is pending". Nothing changed; `git status` empty.
- So the When changes nothing unless the plugin's version is above 0.24.0 (section 7).

Probe 2: `test_at_0_23_1_the_0_24_0_step_leaves_awaiting_ruling_and_rulings` (run). Same files at 0.23.1.
- `migrate status`: pending 0.24.0 "work-items named by ids".
- `migrate upgrade`: "upgraded to 0.24.0". Status still awaiting-ruling, `## Rulings` still there, log line still awaiting-ruling. The 0.24.0 step does not touch status or heading (correct for r25/r26).
- Second `migrate upgrade`: "no upgrade step is pending" (r27 holds).

Probe 3: `test_model_check_on_a_file_holding_awaiting_answer` (run). A work-item file with status awaiting-answer and `## Answers`, plus its initiative.md:
- `model check` rc 1: `file: .shop/work/i1/w1.md: status 'awaiting-answer' is not one of awaiting-ruling, claimed, done, drafted, failed, green, planned, ready, researched, withdrawn`; "1 file problems".

Probe 4: `test_model_check_on_the_file_as_it_is_today` (run). Same with awaiting-ruling: no file problem. Its 8 violations (v8, v9a, v9c, v_w4 on w1 and w2) come from my minimal work-items (no `under:`, no `accepts:`), not from the status.

Nearest cases the scenarios do not give:
- Initiative with no `log.jsonl`: handled by `migrate_upgrade_ids.py:116-118` (read).
- Upgrade run twice: probe 2 (run); the second run says none pending.
- A done work-item with `## Rulings` (w2): the scenario wants its heading renamed; probe 1 and 2 show today's 0.24.0 step does not rename it (not the step under test).

## 3. Old assumptions

r29 changes the stored form of the status `awaiting-ruling` and the heading `## Rulings`. The status rename in code is w91's (`.shop/work/i22-rulings-round-trips-query-output/w91.md:12`: "The status rename ... in the lifecycle the code keeps (`work`, `model`, `work run`) is this work-item's; w92 and w93 build on it"). w91 is still awaiting-ruling in the initiative log (read), so these rows are w91's and stay as they are.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue.py:16 `STATUSES`, used by `move` (:128) | refuses a move to a status not listed; lists awaiting-ruling, not awaiting-answer | the upgraded files hold awaiting-answer, which `move` does not name; w91 owns it | none by search (no test in tests/scenarios names awaiting-ruling outside supervision and batch measurement) | refs (2 production files), search |
| scripts/workqueue.py:162 `agrees` | refuses a file whose status differs from its log's last `after` | the step renames both, so they agree; the step does not check it (section 5) | none by search (as above) | read |
| scripts/model_work.py:12 `STATUSES["work-item"]`, used by `status` (:208) | model check flags any status not listed | probe 3: awaiting-answer is a file problem; w91 owns it | none by search (as above) | refs (1 production file), probe 3 (run) |
| scripts/supervise.py:156 and :245 (awaiting-ruling written, counted for exit 3) | work run writes awaiting-ruling; returns 3 only when some item has it | an upgraded awaiting item has awaiting-answer: work run prints it and returns 1, not 3; w91 owns it | tests/scenarios/test_supervision.py:108 (by search) | read |
| scripts/supervise.py:237-239 (questions printed for awaiting-ruling) | prints an item's open questions only under the old status | an upgraded item's questions are not printed | test_supervision.py (by search) | read |
| scripts/supervise.py:207-209 `questions()` reads `## Rulings` via `held` (:193) | open questions = `## Questions` bullets past the `## Rulings` bullets | after the rename the heading is `## Answers`; `held("Rulings")` is empty, so every question counts as open again | test_supervision.py:200 (by search) | read |
| scripts/supervise_merge.py:88 and :106 (awaiting-ruling written on a merge refusal) | a merge refusal writes the old status | an item upgraded to awaiting-answer and then refused in merge gets awaiting-ruling: two vocabularies in one initiative until w91 lands | tests/scenarios/supervision_*.py (by search) | read |
| scripts/measure_build.py:76 (`to == "awaiting-ruling"` counts) | counts awaiting transitions from log lines | the step renames every log `after`, so upgraded history counts zero awaiting transitions | tests/scenarios/batch_measurement_then_steps.py:110 (fresh logs only, by search) | read |
| scripts/migrate_upgrade.py:104 and :110 (`upgrade`: all plans, then apply) | every step plans from the tree before any step applies | a step planning text for a file an earlier step renames writes the old path (defect 1) | none (no test runs two steps) | read, probe_sequence (run) |
| scripts/migrate_upgrade.py:16 `STEPS` and `pending` (:32-35) | only 0.24.0 is a step; the plugin's version is 0.24.0 | with 0.25.0 added and plugin.json raised, every repository below 0.25.0 gets it | tests/scenarios/migration_upgrade_steps.py (r18, r20, r22, r27; by search) | read |
| tests/scenarios/migration_upgrade_steps.py:153 (Then "pending upgrade step 0.24.0") | checks the 0.24.0 line is printed | still true with a 0.25.0 line added | r18 scenario (by search) | read |
| agents/bdd-planner.md:14, agents/bdd-task-reviewer.md:14 | the briefs name `## Rulings` | after the rename they read a heading the file no longer has | none (prompt text) | search |
| skills/delivering-an-initiative/SKILL.md:51 | tells the person about awaiting-ruling items | the old status name in prose; w91/w92 scope | none | search |

## 4. Tests the requirements make impossible to keep

`tools tests-of` has no map, so this is `by search`: the tests that run `migrate upgrade` or `migrate status` (`tests/scenarios/migration_upgrade_steps.py` via r18, r20, r22, r25-r27 in `test_migration_tools.py`) and `tests/scripts/test_migrate_upgrade_ids.py` (5 tests). None asserts an old awaiting-ruling form after an upgrade. Only the r29 scenario runs an upgrade over awaiting-ruling data, and it is red.

Verified by reading (read, not run), with plugin.json at 0.25.0:
- r18 "migrate status": still passes; one extra pending line.
- r20 upgrade: the commit still names "work-items named by ids" in its first line; the commit names both steps.
- r22 hook: still passes; the text lists both steps.
- r27 "no pending step": uses `plugin_version()`, so it passes at any version.
- test_migrate_upgrade_ids.py: passes only if the r29 plan writes nothing for a repository with no awaiting-ruling item (a plan that writes every file would rewrite old paths; defect 1).

Result: no test must change its assertion. Condition: the r29 plan writes only the files it changes.

## 5. A step the work-item skips

The existing way (`workqueue.move`, `workqueue.py:120-143`): refuses a status not in STATUSES; writes the file, then appends the log line; restores the file if the append fails (r7). `agrees` (:162) refuses a file that disagrees with its log.

The step's way (`migrate_upgrade.py:66-78` `apply`, `upgrade` :93-123):
- No STATUSES check. It writes awaiting-answer, which only w91's STATUSES accepts (read).
- No `agrees` check: a file and its log that already disagree are both renamed and still disagree (read).
- The log is rewritten as a whole text (pattern of `migrate_upgrade_ids.py:69-78`), not appended; a failure is undone by `git reset --hard` and `git clean -fdq` in `upgrade` (:116-118), not per file (read).
- Effect only the step produces: `## Rulings` renamed to `## Answers` in files. The existing `work answer` (w92) writes under `## Answers` (w92.md; read).
- The log line names the status in two fields, `before` and `after`. The scenario checks only the line's status for w1; a rename of `after` alone leaves `before` as awaiting-ruling on the next transition's line (read).

## 6. Defects

### Defect 1: a later step writes to a path an earlier step renames

Reproduction (run): `python3 -m pytest -q -s -n 0 .shop/scratch/w93-1-research/probe_sequence.py`. The probe adds a stand-in step `("0.25.0", ...)` whose plan renames awaiting-ruling in the text it reads from the tree, with the 0.24.0 step pending in the same run; the plugin version is raised in-process to 0.25.0. Repository at 0.23.1: `.shop/work/i1/size-check.md` (status awaiting-ruling, `# size-check`, `## Rulings`) and its log line.

Came back:
```
upgraded to 0.25.0: work-items named by ids, stand-in
-- .shop/work/i1/size-check.md  (status: awaiting-answer)   <- recreated under the old name
-- .shop/work/i1/w1.md          (status: awaiting-ruling, # size-check, ## Rulings)
-- log.jsonl: "work-item": "w1", "after": "awaiting-ruling"
git log: "migrate upgrade: 0.23.1 to 0.25.0"
```
`upgrade()` computes all plans (`migrate_upgrade.py:104`) before `apply` (:110). The commit succeeds with a duplicate work-item, the renamed item unchanged, and a log naming w1 with the old status. Not triggered today (one step). It is triggered by the r29 step once it ships and a repository at 0.23.1 holds awaiting-ruling items.

Not a defect (run, same probe, first attempt without a git identity): the upgrade printed "migrate put the repository back as it was" and left the tree clean.

## 7. The file set

Must change (read unless marked):
- `scripts/migrate_upgrade.py` (137 lines, room 163): add the 0.25.0 entry and its import to `STEPS` (:16). Possibly the plan-order fix of defect 1, which the scenario does not need but a repository at 0.23.1 does.
- `scripts/migrate_upgrade_answers.py` (new; the plan names it): one module a step; `plan(root)` returns `migrate_upgrade_ids.Changes` for each work-item file under `.shop/work/` with awaiting-ruling (`## Rulings` to `## Answers`) and each log line's `before` and `after`. Expected 50-70 lines.
- `tests/scenarios/migration_upgrade_answers_steps.py` (new): the Givens and Thens of r29. `tests/scenarios/migration_upgrade_steps.py` (269 lines, room 31) is too small for them.
- `tests/scenarios/test_migration_tools.py` (226 lines, room 74): one import line for the new steps module (line 14 pattern).
- `.claude-plugin/plugin.json` (15 lines): version 0.24.0 to 0.25.0, only if the scenario is to pass (section 7 question).

Read, no change needed:
- `scripts/migrate` (71 lines): entry point.
- `scripts/migrate_write.py` (126 lines, room 174): `check_moves`, `uncommitted`, `git`, used by the step.
- `scripts/migrate_upgrade_ids.py` (119 lines, room 181): `Changes` and the log rewrite pattern.
- `tests/scenarios/migration_old.py` (81 lines): `Old` fixture, reused.
- `hooks/hooks.json` (14 lines): runs `migrate status --hook`; unchanged.

On this path, changed by w91 or w92 (not this item's files; room for them):
- `scripts/workqueue.py` (255 lines, room 45): STATUSES.
- `scripts/model_work.py` (211 lines, room 89): STATUSES.
- `scripts/supervise.py` (263 lines, room 37), `scripts/supervise_merge.py` (132 lines, room 168): awaiting-ruling writes, `Rulings` reads.
- `scripts/measure_build.py` (112 lines, room 188): awaiting-ruling counts.

Size check (run): `tools size --limit 300` printed nothing; no tracked Python file is over 300 lines.

Question for the plan (both readings; not chosen here):
- A: raise `.claude-plugin/plugin.json` to 0.25.0 in this item. Then every repository below 0.25.0 is offered the step, and the scenario can pass.
- B: keep 0.24.0. The scenario stays red until the version is raised, which the brief says happens later.
- Raising the version is also a release act (memory: no release for no reason).

Dependency (read): the output (awaiting-answer, `## Answers`) is accepted only once w91 lands its STATUSES and model changes. Until then `model check` and `work` see a status they refuse (probe 3).
