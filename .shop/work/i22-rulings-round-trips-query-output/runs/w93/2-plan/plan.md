# Plan of w93: the upgrade step that renames awaiting-ruling

From the research notes (`runs/w93/1-research/notes.md`), the work-item, migration-tools, decisions 0062
(upgrades-between-plugin-releases) and 0064 (answers-not-rulings), and the r29 scenario.

## 1. What goes green

- **migration-tools#r29**: scenario "the upgrade step of the plugin version after 0.24.0 renames the old status and
  the old heading in work-items and logs" (`features/migration-tools.feature` line 524).
  Red today because:
  - its first Given (plugin-version 0.24.0, feature line 526) has no step definition. Its other Givens (527-529) and
    its three Thens (531-533) have none either;
  - `scripts/migrate_upgrade.py` `STEPS` holds only the 0.24.0 step, and no module plans r29's renames;
  - the plugin's version is 0.24.0, so even with the step defined `migrate upgrade` says "no upgrade step is pending"
    (probe 1).
- Retired scenarios: none. The work-item has no Retires section.

## 2. Where the change lands

- `scripts/migrate_upgrade_answers.py` (new; one module per step, as the module map asks): the step's `plan(root)`.
  It returns a `migrate_upgrade_ids.Changes` holding texts only, no moves:
  - each work-item file under `.shop/work/` whose frontmatter status is awaiting-ruling or that has a `## Rulings`
    heading, with the status set to awaiting-answer and the heading changed to `## Answers`;
  - each initiative's `log.jsonl` that names awaiting-ruling in a status field, with that value set to awaiting-answer.
  It writes only the files it changes.
- `scripts/migrate_upgrade.py`:
  - add the step `("0.25.0", <description>, <one line>, migrate_upgrade_answers)` to `STEPS`, with its import;
  - in `upgrade`, plan each step only after the steps before it are applied (decision 3). The module docstring's
    requirement list gains r29.
- `tests/scenarios/migration_upgrade_answers_steps.py` (new): r29's Givens and Thens. `migration_upgrade_steps.py`
  has only 31 lines of room, too few for them.
- `tests/scenarios/migration_upgrade_steps.py`: the shared When "the session runs `migrate …`" runs `migrate` from
  the plugin copy a Given has put in the context, where there is one (decision 2). This adds a few lines and stays
  under 300.
- `tests/scenarios/test_migration_tools.py`: one import line for the new steps module, in the pattern of line 14.
- `tests/scripts/test_migrate_upgrade_answers.py` (new): tests of the step on repositories the scenario does not
  build (decision 3 and the cases of decision 4). Added to the researcher's set.
- Removed from the researcher's set: `.claude-plugin/plugin.json`. It stays at 0.24.0 (decision 1).

## 3. Decisions

1. **The plugin's version stays 0.24.0 in this item.** Only the step's version, 0.25.0, goes into `STEPS`.
   - This rests on the work-item, which says to name the step 0.25.0 and that "it is pending only once the plugin's
     version is raised", so raising the version is left to a later release.
   - It also rests on design-decision/upgrades-between-plugin-releases: a step carries the version of the release
     that introduces it.
   - So for the narrator nothing changes until the release: `migrate status` and the hook show no 0.25.0 step at
     plugin 0.24.0. This settles the researcher's question (notes §7) with reading B for the plugin. Section 1 gives
     how the scenario still goes green.
2. **The scenario runs the real `migrate` from a copy of the plugin whose `plugin.json` names the version after
   0.24.0 (0.25.0).** The scenario's condition is migration-tools#r29's "when `migrate upgrade` applies the upgrade
   step of the plugin version after 0.24.0".
   - The r29 Given builds the repository at plugin-version 0.24.0, makes the copy (the scripts directory and
     `.claude-plugin/plugin.json` with the raised version) in the scenario's temporary space, and records it in the
     context.
   - The shared When runs `migrate` from that copy when the context holds one; otherwise it runs as today.
   - No production code learns a version override.
3. **`upgrade` applies the steps oldest first, each planned from the tree the steps before it left.** This rests on
   migration-tools#r20 ("apply each pending upgrade step, oldest first") and fixes notes §6 defect 1. Without it, a
   repository at 0.23.1 upgraded to 0.25.0 gets a work-item duplicated under its old name, and the renamed item and
   its log keep awaiting-ruling.
   - A later step's refusal (failures or move failures) puts the tree back the way the existing error path does
     (reset and clean). It prints "migrate changed nothing; it could not make every change" with its failures and
     exits 1. `.shop/plugin-version` is not written and nothing is committed (r20 one commit, r7's change no file;
     the tree was clean by r15).
   - The commit and the printed line are unchanged.
4. **What the step renames** (migration-tools#r29):
   - the frontmatter `status:` value awaiting-ruling in every work-item file (kind work-item) under `.shop/work/`;
   - every heading line that is exactly `## Rulings` in every work-item file, whatever its status (the w2 case);
   - in every `log.jsonl` line, each status field (`before` and `after`) that holds awaiting-ruling (notes §5: renaming
     `after` alone leaves the old name in the next line's `before`).
   - Free text in a body or in records that only mentions the word stays as it is. This follows r29's "the status"
     and the "leave free text as it is" of migration-tools#r26.
   - Every other field and line of a log is written back as it was. The log rewrite follows the pattern of
     `migrate_upgrade_ids` (whole text, one JSON object per line).
5. **The step's description** is "answers, not rulings", the name of design-decision/answers-not-rulings, which calls
   for this step. Its one-line text is about renaming awaiting-ruling and `## Rulings` to awaiting-answer and
   `## Answers`.
6. **No STATUSES or `agrees` check in the step** (notes §5). The status lists in `workqueue.py`, `model_work.py` and
   `supervise*.py` are w91's (w91.md: "the status rename … is this work-item's; w92 and w93 build on it"). A file
   and log that already disagree are both renamed and still disagree; the step does not judge them.

## 4. Tests the decisions break

None. What was checked:
- Decision 1 keeps plugin.json at 0.24.0, so the r18, r20, r22, r23, r24, r25-r28 scenarios and the five tests of
  `tests/scripts/test_migrate_upgrade_ids.py` run as today. They see only the 0.24.0 step pending. The notes (§4)
  also read them as passing once the version is raised later.
- Decision 2 changes the shared When only where a plugin copy is in the context, which only the r29 Given sets.
- Decision 3: in `test_a_name_held_by_two_other_initiatives_is_refused_and_nothing_changes` the first step is the
  one refused, before anything is applied. That test still holds: exit not 0, files in place, no plugin-version.
- Decision 4 writes only the files it changes, which is the notes' condition for `test_migrate_upgrade_ids.py`.

## 5. Open cases (for the implementer to name, not to choose)

- A repository at 0.23.1 upgraded by a plugin at 0.25.0, with an awaiting-ruling item whose name the 0.24.0 step
  changes: both steps in one commit, no file left under the old name, the item and its log naming w<n> and
  awaiting-answer (decision 3; a test in `tests/scripts/test_migrate_upgrade_answers.py`).
- A later step that refuses after an earlier step applied: tree back as it was, exit 1, no plugin-version written.
- An initiative with no `log.jsonl`, and a log line with no status field (only `event`): left as they are.
- A work-item file with neither awaiting-ruling nor `## Rulings`: not written, so not in the commit.
- A `## Rulings` heading already beside a `## Answers` heading in one file: the scenarios do not say.
- A file under `.shop/work/` that is not a work-item (`initiative.md`) and holds `## Rulings`: left as it is under
  r29's "each work-item's".
- Running the upgrade twice: the second run says no step is pending (r27).
