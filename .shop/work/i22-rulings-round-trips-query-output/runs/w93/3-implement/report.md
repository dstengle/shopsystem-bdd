# w93 report

## Budget
- scripts/migrate_upgrade.py
- scripts/migrate_upgrade_answers.py (new)
- tests/scenarios/migration_upgrade_answers_steps.py (new)
- tests/scenarios/migration_upgrade_steps.py
- tests/scenarios/test_migration_tools.py
- tests/scripts/test_migrate_upgrade_answers.py (new)

## What changed
- New step module `scripts/migrate_upgrade_answers.py`: `plan(root)` renames the frontmatter status awaiting-ruling and the `## Rulings` heading in work-items, and `before`/`after` in logs. It writes only the files it changes.
- `migrate_upgrade.py`: the 0.25.0 step "answers, not rulings" in STEPS. `upgrade` now plans each step after applying the ones before it. A refusal resets the tree, prints the failures and exits 1.
- Steps: r29 Givens/Thens in the new module. The shared When runs `migrate` from the plugin copy a Given put in the context, if there is one. The copy has plugin.json at 0.25.0. plugin.json in the repository stays 0.24.0 (plan decision 1).
- Tests for the step on trees the scenario does not build: `tests/scripts/test_migrate_upgrade_answers.py`.
- No CLAUDE.md module-map row was added. The map's `scripts/migrate_upgrade*.py` row already covers the new module.

## Red and green
- Red: `python3 -m pytest -q --work-item w93 -n 0`: the r29 scenario failed with StepDefinitionNotFoundError, "a repository on the final layout whose .shop/plugin-version is 0.24.0". Expected: no step definitions and no step existed.
- After the first steps were written, the Then failed on an unchanged file. The cause was my scratch plugin copy inside the repository's tmp dir, which made the tree uncommitted. I moved the copy elsewhere.
- Green: `python3 -m pytest -q --work-item w93 --whole-suite tests/scenarios/test_migration_tools.py tests/scripts/test_migrate_upgrade_answers.py tests/scripts/test_migrate_upgrade_ids.py`: 67 passed, 16 xpassed. `--work-item w93` alone shows the r29 scenario passing; its only failures are two tests in tests/scripts/test_tools.py that do not touch my files.
- Suite at start (brief's Suite record): 612 passed, 2 failed. The failures were a migration-tools scenario (this one) and a supervision scenario. The rest was listed as expected-red.

## Tests changed under an allowance
none

## Open questions
- A `## Rulings` heading beside a `## Answers` heading in one file: both are kept, so the file ends with two `## Answers`. The scenarios do not say.
- The two test_tools.py failures under `--work-item w93` were not investigated; they are outside my files.

## Plan code
The plan contained no code.

## Size check
`tools size --limit 300` printed nothing.

## Result
Someone can now run `migrate upgrade` with a plugin at 0.25.0 and get awaiting-ruling and `## Rulings` renamed. Raising plugin.json to 0.25.0 is left to a release. The surprising part was that the scenario needs a plugin copy at 0.25.0, because the repository's plugin.json stays at 0.24.0.
Commit: 5eb628a.
