# Report: migration-tools-1

## Budget
scripts/migrate, scripts/migrate_upgrade.py (new), scripts/migrate_upgrade_ids.py (new), hooks/hooks.json (new), .claude-plugin/plugin.json, CLAUDE.md, tests/scenarios/migration_upgrade_steps.py (new), tests/scenarios/test_migration_tools.py. (8 files)

## Suite at the start
Brief's record: 615 passed, 16 failed at b4a211e (this work-item's scenarios plus design_model_check and work_queue ones that belong to other work-items).

## What changed
- `migrate status [--hook]` and `migrate upgrade` (scripts/migrate, scripts/migrate_upgrade.py); step 0.24.0 "work-items named by ids" in scripts/migrate_upgrade_ids.py.
- hooks/hooks.json: SessionStart runs `migrate status --hook`; plugin.json 0.23.1 → 0.24.0 (plan D1).
- CLAUDE.md: module-map rows for migrate_upgrade*.py and hooks/hooks.json.
- Steps in tests/scenarios/migration_upgrade_steps.py (new module; test_migration_tools.py imports it, +1 line).
- The plan contained no code.

## Red and green
Red: `python3 -m pytest -q -n 0 --work-item migration-tools-1 -p no:warnings` after writing the steps, before any production code: the six `migrate upgrade`/`status` scenarios and the others failed with argparse "invalid choice: 'status' (choose from 'run')" / missing hook file (the 3 `migrate run` r15 rows went green with the new Then "it exits with an error" step alone). Expected: no subcommand, no hooks.json.
Green: final `python3 -m pytest -q -n 0 --work-item migration-tools-1 -p no:warnings`: 130 passed, 2 failed. The 2 are tests/scripts/test_tools.py map tests, which fail only because `--work-item` leaks into their nested pytest ("no such work-item"); unrelated to my change and not in the scenario set. `tests/scenarios/test_migration_tools.py` alone: 19 passed (all work-item scenarios); with test_migrate_write.py and test_migrate_layout.py: 26 passed.

## Tests changed under an allowance
none

## Open questions
- Plain `migrate status`/`upgrade` outside a git repo refuses ("could not find a git repository", exit 1) by following `run`'s convention; in a repo without `.shop/` they run as on version 0.23.1 — unchosen beyond that.
- An initiative directory not named `i<n>` is skipped by the step.
- `spec/index.md` missing or without a bounded-context id: the step raises (uncaught) — unchosen.
- blocked_by/depends_on naming a work-item of another initiative is left as is.
- `.shop/plugin-version` not a version: uncaught ValueError.
- A `.shop/` ignored by git: untested.
- This repository itself has no plugin-version, so the hook will offer it the upgrade; not run here.
- Q2 (delivering-an-initiative skill saying `work add <initiative> <title>`) not done (plan D8).

## Outside the file set
none. `tools size --limit 300` printed nothing.

## Surprises
Subprocess `migrate upgrade` commits need a git identity; the When step supplies GIT_* env vars.

Commit: ff22a77. Files: those in the Budget.
