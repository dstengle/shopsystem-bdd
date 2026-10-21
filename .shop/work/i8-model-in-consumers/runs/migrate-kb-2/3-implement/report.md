# Report: migrate-kb-2

## Budget
- scripts/migrate_ledger.py
- scripts/migrate_spec.py
- tests/scenarios/migration_ledger_steps.py
- tests/scenarios/test_migration_tools.py

## Changes
- scripts/migrate_ledger.py: `supersedes_of` returns every target (with optional qualifier); two or more written as a `[a, b]` list, one stays scalar; every target marked superseded; `by` gets a qualifier only where there is one.
- scripts/migrate_spec.py: `plan_references` passes each created decision text through `rewrite_text`.
- tests: status step strips backticks (+ two-file form), new Givens/Thens (three-entry, supersedes naming, source, specs/s1.md, README) and Then steps.

## Red and green
- Red (start, `python3 -m pytest -q --work-item migrate-kb-2`): 6 failed, 37 passed: status step `AssertionError: superseded`; undefined Givens/Thens; then after steps: D2 `AssertionError: alice, from adrs/0001-use-x.md` (by not rewritten), D1 `AssertionError: design-decision/example.org/acme/shop/b` (second target lost). README scenario red only for undefined steps; code was already right (as the plan said).
- Green (final): `--work-item migrate-kb-2`: 43 passed; test_migration_tools.py + tests/scripts/test_migrate_layout.py: 47 passed.
- Starting suite record: Suite: 596 passed, 6 failed at 58fa5e6 (the 6 are this work-item's).

## Tests changed under an allowance
- tests/scenarios/migration_ledger_steps.py, the status step `spec/decisions/{name}.md's status is {status}`: setup/step repair per plan decision 4 (strips backticks); not a test, a step. No assert in a test function changed otherwise.

## Open questions
- Two targets with qualifiers: what `by` reads (I append "; supersedes <id> <qualifier>" per qualified target).
- Separators other than "and"; a supersedes naming no ledger entry (D3); `model check` over a list; body prose ids; ledger with existing spec/decisions files.

## Other
- The plan contained no code. No outside-file-set edits. Files changed: the four in Budget (all under 300 lines).
