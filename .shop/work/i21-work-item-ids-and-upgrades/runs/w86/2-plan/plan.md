# Plan: migration-tools-1 (accepts migration-tools#r15, r18-r20, r22-r28)

Taken from the research notes, `.shop/work/i21-work-item-ids-and-upgrades/runs/migration-tools-1/1-research/notes.md`.

## 1. What goes green

All scenarios are in `features/migration-tools.feature`.

- **r15**: "`<command>` on a repository with <change> refuses, naming it, exits with an error and changes no file" (6 rows).
  - The three `migrate run` rows are red at Then "it exits with an error". Only "it exits non-zero" exists as a step. The refusal itself already works (scripts/migrate cmd_run).
  - The three `migrate upgrade` rows are red at their Given "a repository on the final layout whose plugin version is 0.23.1, with a work-item …". There is no such step and no `upgrade` subcommand: argparse accepts only `run`.
  - The deprecated r15 outline (3 rows) passes today and must still pass. This work-item has no Retires section, so nothing is retired.
- **r18**: "`migrate status` prints the repository's plugin version, the plugin's version and each pending upgrade step with its version and description". Red at its Given. There is no `status` subcommand, and nothing reads `.shop/plugin-version`.
- **r19**: "a repository with .shop/ and no .shop/plugin-version is taken to be on 0.23.1". Red at its Given, for the same reason.
- **r20**: "`migrate upgrade` applies the pending upgrade step, records the plugin's version and commits it all in one commit naming the step". Red at its Given. There is no upgrade code.
- **r22**: "a session starting in a repository with a pending upgrade step is told to offer the upgrade and run it only on the person's yes". Red at its Given. There is no `hooks/` directory, no `hooks.json`, and no hook declared.
- **r23**: "a session starting in a repository on a plugin version above the plugin's is told to tell the person to update the plugin". Red for the same reason as r22.
- **r24**: "a session starting in a repository on the plugin's version is told nothing". Red for the same reason as r22.
- **r25**: "the upgrade step "work-items named by ids" numbers every work-item from 1, by its initiative's number and then its file name". Red at its Given. There is no step.
- **r26**: "the upgrade step "work-items named by ids" renames a work-item's file and stage directories and rewrites its name where its initiative names it". Red at its Given.
- **r27**: "`migrate upgrade` with no pending upgrade step says so, exits successfully and changes nothing". Red at its Given.
- **r28**: "a session starting in a repository without .shop/ is told nothing". Red at its Given. There is no hook.

## 2. Where the change lands

- `scripts/migrate` (63 lines): add the `status` and `upgrade` subcommands, plus the hook's mode of `status` (decision D3). The `run` path stays as it is.
- `scripts/migrate_upgrade.py` (new). It holds:
  - the plugin's version, read from `.claude-plugin/plugin.json`;
  - the repository's version: `.shop/plugin-version`, or 0.23.1 when the file is missing;
  - the list of upgrade steps, and what counts as pending;
  - the `status` text and the session text;
  - the upgrade: check uncommitted changes first, apply the steps, write the version, make one commit, and undo everything on failure.
- `scripts/migrate_upgrade_ids.py` (new): the 0.24.0 step "work-items named by ids" (r25, r26). It is split from migrate_upgrade.py so each file stays well under the 300-line limit, and because the steps are a growing list with one module per step.
- `scripts/migrate_write.py` (126 lines): reused for `uncommitted` and `git add -f`. It changes only if the implementer moves the shared rollback into a helper; leave it as is otherwise.
- `hooks/hooks.json` (new): one SessionStart hook. Its command runs `migrate status` in its hook mode from `${CLAUDE_PLUGIN_ROOT}/scripts`, as the coordinator note says.
- `.claude-plugin/plugin.json`: version 0.23.1 → 0.24.0 (decision D1). The plugin's hooks are found by the `hooks/hooks.json` convention. Declare them in plugin.json only if the plugin loader needs it.
- `CLAUDE.md`: in the module map, add a row for `scripts/migrate_upgrade*.py` (upgrades between plugin releases), or widen the `scripts/migrate*.py` row to name them. Also add a row for `hooks/hooks.json`.
- `tests/scenarios/migration_upgrade_steps.py` (new): the Givens, Whens and Thens of r15's upgrade rows and of r18-r28, plus the Then "it exits with an error". A new module, because test_migration_tools.py has only 75 lines of room.
- `tests/scenarios/test_migration_tools.py` (225 lines): import the new step module (1-2 lines).

Removed from the researcher's set:
- `tests/scripts/test_migrate_upgrade.py` (optional in the notes): not needed, because the scenarios pin numbering and renames.
- `scripts/migrate_layout.py`: read only.

Not added: `skills/delivering-an-initiative` (see D8).

## 3. Decisions

- **D1. The plugin's version becomes 0.24.0 in this work-item (settles Q1).**
  - r18 needs the 0.24.0 step pending on a 0.23.1 repository.
  - r20 needs the upgrade to write "the plugin's version" after applying that step.
  - r27 needs no step pending on a repository already on the plugin's version.
  - With the plugin on 0.23.1, r18 and r27 contradict each other. design-decision/upgrades-between-plugin-releases gives each step "the version that introduced it", so the plugin that carries the 0.24.0 step is 0.24.0.
  - The tests read the real plugin.json; they do not substitute a version.
- **D2. Pending step and version order.**
  - A step is pending when its version is above the repository's version and not above the plugin's (r18, r20, r27).
  - Versions are compared as tuples of numbers, not as text.
  - When the repository's version is above the plugin's, no step is pending (r23, r27).
- **D3. The hook asks `migrate` for its text.**
  - `migrate status` has a hook mode (the implementer names the option). It prints exactly what the session is told and always exits 0:
    - with a pending step (r22): the offer, naming both versions and each step, and the instruction to run `migrate upgrade` only on the person's yes;
    - with the repository above the plugin (r23): the instruction to tell the person to update the plugin;
    - in every other case (r24, r28): nothing at all.
  - Plain `migrate status` prints r18's text.
  - The decision rests on the Implementation note ("The plugin's SessionStart hook runs `migrate status`") and on r22-r24 and r28. It keeps the logic out of shell code in hooks.json.
- **D4. The scenarios "start a session" by running the real hook.**
  - The step reads the SessionStart command from `hooks/hooks.json` and runs it with `CLAUDE_PLUGIN_ROOT` set to the plugin's root and the scenario repository as the working directory.
  - What the session is told is the hook's stdout (r22-r24, r28). This tests the real hook file, as the coordinator note names it.
- **D5. What counts as a work-item, and its number (r25).**
  - A work-item is a `.md` file directly under `.shop/work/<initiative>/` whose frontmatter `kind` is `work-item`. That excludes `initiative.md` and everything under `runs/`.
  - Initiatives are ordered by the number in their directory name `i<n>`, so i2 comes before i10. Within an initiative, work-items are ordered by file name.
  - Every work-item is renumbered from 1, including one already named `w<n>` (r25: "every work-item").
- **D6. How a rename is applied (r26).**
  - Files and `runs/<name>/` directories are renamed with `git mv`, in two phases (to temporary names, then to the final names). Otherwise a `w<n>` already present could collide with a new name (notes part 2).
  - The context path comes from the `bounded-context/<path>` id of `spec/index.md`.
  - The id `work-item/<context path>/w<n>` is written into the frontmatter.
  - An item with no `# ` heading gets one after its frontmatter, holding its old name.
  - In the initiative's `log.jsonl`, only the `work-item` field of a line naming the old name is rewritten. Lines that name nothing renamed are kept byte for byte.
  - In `blocked_by` and `depends_on`, both forms are rewritten: the bare old name and the qualified `work-item/<ctx>/<old>`.
  - Free text, and every file outside the initiative, is left alone (r26).
- **D7. All or none, in one commit (r15, r20, design-decision/upgrades-between-plugin-releases).**
  - The uncommitted-changes check runs before anything else, for both commands (r15 before r27, per the coordinator note).
  - Every change is computed before any is written.
  - Every file written or renamed is added with `git add -f`.
  - Exactly one commit is made. Its message names each applied step with its version.
  - If writing or committing fails, everything is undone. The rollback that migrate_write.py runs today does not cover a failed commit; this one must (notes part 5).
  - With no pending step, the upgrade says so, writes nothing and commits nothing (r27).
- **D8. Q2 (delivering-an-initiative saying `work add <initiative> <title>`) is out of scope here.**
  - No accepted requirement of migration-tools asks for it.
  - `work add` still takes a name and writes name-based ids (defect D1 of the notes, spec work-queue r1 and r12). A skill naming `<title>` would describe a command that does not exist yet.
  - It belongs with the work-queue work-item that fixes `work add`. The coordinator should route it there.

## 4. Tests the decisions break

None. What I checked:
- D1: no test or script names `0.23.1`, `plugin.json` or `plugin-version` (search of `tests/` and `scripts/`). plugin.json is the only file in the repository outside `.shop/` that holds a version.
- D3 and D7 add subcommands; `run` stays unchanged. The deprecated r15 rows exercise only `run` and keep passing (notes part 4).
- D5 and D6 change no existing function. `tests/scripts/test_work_withdraw.py` already uses `w1` (notes part 4).

The rest of test_migration_tools.py, test_migrate_write.py and test_migrate_layout.py cover `run`. The notes did not run them; the implementer runs them at the end.

## 5. Open cases (for the implementer to name, not to choose)

- What plain `migrate status` and `migrate upgrade` do in a repository without `.shop/`, or outside a git repository. The hook mode stays silent and exits 0 there (D3).
- An initiative directory whose name is not `i<n>`, for its place in the order.
- `spec/index.md` missing, or without a `bounded-context/` id, when the step needs the context path.
- A `blocked_by` or `depends_on` that names a work-item of another initiative. r26 rewrites only names within an item's own initiative, so a cross-initiative reference would be left dangling.
- A `runs/<name>/` directory, or a `log.jsonl` line, whose name matches no work-item.
- `.shop/plugin-version` holding text that is not a version.
- A `.shop/` that is ignored by git, for the r15 check and for `git add -f`.
- This repository's own `.shop/` has no plugin-version, so once the hook ships it will offer this repository the upgrade. This work-item does not run that upgrade.
