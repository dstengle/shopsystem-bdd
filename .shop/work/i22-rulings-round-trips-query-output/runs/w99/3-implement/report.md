## Budget
- scripts/migrate_upgrade.py
- tests/scenarios/migration_version_steps.py (new)
- tests/scenarios/test_migration_tools.py

## Changed
- `no_version` in scripts/migrate_upgrade.py names the held text in double quotes (D1), not through `repr`.
- New step module tests/scenarios/migration_version_steps.py: the Given, "a session starts in the repository", "migrate exits with an error", "it says that ...", "no file of the repository has changed", and the r31 Then. One import line added to test_migration_tools.py.

## Red and green
- Suite at start (brief): 690 passed, 3 failed at 6941c6e. The 3 failures were r30 (status, upgrade) and r31.
- Red 1: `python3 -m pytest -q --work-item w99`: 3 failed, 139 passed. StepDefinitionNotFoundError on the Given "a repository on the final layout whose .shop/plugin-version holds "next"". Expected: no step existed.
- Red 2, after writing the steps: the 3 still failed, now on the Then. `AssertionError: .shop/plugin-version holds 'next', which is no version` (single quotes; the scenario says `"next"`). Expected: the message used `repr`.
- Green: after the one-line code change, `--work-item w99` gives 142 passed, 1 skipped. test_migration_tools.py and tests/scripts/test_migrate_upgrade.py also pass (8 passed, 6 subtests; the `--work-item` option, not the module list, appears to select which tests run).

## Tests changed under an allowance
none

## Open questions
- Held text containing a double quote, backslash or newline: how the double-quoted form shows it is unchosen. The code prints it raw; a newline in the held text would break the one-line hook output.
- A dotted but short value such as `0.24` is not refused. r30 and r31 do not say whether it is a version.
- `upgrade` with a non-version file and a dirty tree reports only the version refusal.

## Other
- The plan contained no code, so nothing was pasted.
- Size check: `tools size --limit 300` printed nothing (no file over). No file I touched is over.
- Now: a version file holding no version is refused by `migrate status`, `migrate upgrade` and the SessionStart hook, with the held text in double quotes. This is covered by scenarios.
- Surprising: the code already refused. Only the message quoting differed.
- Commit: 52141df "migrate: name a version file's held text in double quotes; bind r30, r31".
- Files changed: scripts/migrate_upgrade.py, tests/scenarios/migration_version_steps.py, tests/scenarios/test_migration_tools.py.
- Concerns: none.
