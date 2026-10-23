## Budget
- scripts/migrate_upgrade.py
- scripts/migrate_upgrade_ids.py
- tests/scripts/test_migrate_upgrade_ids.py
- tests/scripts/test_migrate_write.py
- tests/scripts/test_migrate_upgrade.py (new)

## What changed
- F7: `no_version` / `refusal` in migrate_upgrade.py. `status` and `upgrade` refuse (stderr, exit 1, nothing changed); the hook prints one line to stdout and exits 0 (Reading A).
- F8: `context_path` returns None; `plan` refuses ("spec/index.md has no bounded-context id") only when there is a work-item; missing index treated the same.
- F9: initiatives sorted by (number, name).
- N4: resolver takes the field per call; the message names blocked_by/depends_on/for; `refused` deduplicated.
- N5: only name values rewritten; text after a ` #` comment and `name#r<n>` tokens left alone.
- N8: docstring corrected. N6: tests of the move check (tracked and ignored runs/w1). F12: temp repos removed via atexit in the two test modules and the new one.

## Red and green
All 10 accepted scenarios were green before the work (they cover code the work changes). The new tests: `python3 -m pytest -q -n 0 tests/scripts/test_migrate_upgrade.py tests/scripts/test_migrate_upgrade_ids.py tests/scripts/test_migrate_write.py` gave `12 failed, 15 passed` before the code (F7 x3, F8, F9, N4, N5 failed: crash / old behaviour; N6 tests passed at once, as the plan said, they guard existing behaviour). After: all pass.
Final: `python3 -m pytest -q tests/scripts/test_migrate_upgrade.py tests/scripts/test_migrate_upgrade_ids.py tests/scripts/test_migrate_write.py tests/scenarios/test_migration_tools.py` -> `33 passed`. `--work-item w96` selected extra tests; the only failures were tests/scripts/test_tools.py map tests ("tools: no map was made", no --cov in this environment), not in my files.
Suite at start: 659 passed, 0 failed (with the expected-failing list in the brief, all test_analysis_tools).

## Tests changed under an allowance
none (F12 added cleanup lines to the two helpers; no assertion touched)

## Open questions
Those of the plan section 5 stay unchosen: versions with a `v`/suffix/extra parts are "no version" only by the pattern `\d+(\.\d+)*` (fullmatch), directory/untracked version file, plugin.json version holding no version, multi-line version file (held is the stripped text, repr'd), indexed id in other forms (quoted), `for:` with qualifier other than `#r<n>` (treated as a qualified token if it has any `#`), same-number initiatives differing in case.

## Other
Plan contained no code. No file outside the file set. `tools size --limit 300`: printed nothing.
Commit: 2bf920a.
