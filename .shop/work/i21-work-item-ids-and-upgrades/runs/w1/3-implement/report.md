# Report of w1

## Budget
scripts/migrate_upgrade_ids.py, scripts/migrate_upgrade.py, tests/scenarios/migration_upgrade_steps.py, tests/scripts/test_migrate_upgrade_ids.py (migrate_write.py untouched).

## Changed
- migrate_upgrade_ids.py: names resolve across all initiatives (own first, else the one holder, a name several others hold goes to `Changes.failures`); `for:` rewritten (scalar, inline, block); a name naming nothing is left.
- migrate_upgrade.py: `upgrade` plans every step first, and refuses (naming each change, no file changed, no commit) on plan failures or `check_moves` failures.
- Steps: parsed Givens for S2 (the old literal i10/a.md step is subsumed by it) and two Thens (work-item found by its heading).
- Unit tests: block-list `for:`, name held only elsewhere, ambiguous refusal, dangling name left.

## Red / green
- Red: `python3 -m pytest -q -n 0 tests/scenarios/test_migration_tools.py -k rewrites_a_reference_from_another` after steps were written failed on the Then: `AssertionError: ('blocked_by', '...blocked_by: [size-check]\nfor: size-check...')` (expected, old code did not follow cross-initiative).
- Green: `python3 -m pytest -q --work-item w1 tests/scripts/test_migrate_upgrade_ids.py tests/scenarios/test_migration_tools.py`: 7 passed.
- Suite at start: 623 passed, 1 failed (S2). Not re-run (work run's).

## Tests changed under an allowance
none (the literal Given in migration_upgrade_steps.py was replaced by a parsed one covering the same paths; no assertions touched).

## Open questions
Plan §5 cases are unchosen: self-reference, qualified form with a different context, the combined refusal message. Not run: `migrate upgrade` on a clone of this repository (only `python3 -m pytest` is allowed here).

Plan contained no code. Size check printed nothing (no file over 300).

Commit: 36ad963. Files: the four above.
