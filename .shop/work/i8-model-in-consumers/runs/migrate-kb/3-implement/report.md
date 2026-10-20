## Budget
- tests/scenarios/migration_ledger_steps.py
- tests/scenarios/migration_spec_steps.py
- scripts/migrate_ledger.py

## What I found
The branch already held earlier commits (63109eb and later) that implement r2, r6, r8, r9, r12, r13, r14, r15, r16 and r17. The starting record had one red scenario, the r5 row for an entry r13 numbers.

## Changed
- migrate_ledger.py: `plan_ledger` also maps `decision/<slug>` to the new id for an entry whose heading had no number, so references and supersedes that name it without the number are rewritten.
- migration_ledger_steps.py: a Given "the entry 0007-a has supersedes: decision/X" and a Then "0007-a.md's supersedes is design-decision/...".
- migration_spec_steps.py: the rests_on Given and Then take the reference as a parameter.

## Red and green
`python3 -m pytest -q tests/scenarios/test_migration_tools.py` went through three reds.
1. Undefined Given "the entry 0007-a has supersedes: decision/b".
2. Then "rests_on names design-decision/.../b": `AssertionError` on `data["rests_on"] == [ref]`. This is the real red. The code did not rewrite `decision/b`.
3. Undefined Then "0007-a.md's supersedes is design-decision/.../b".

After the fix: 39 passed.

## Suite
- Starting: Suite: 591 passed, 1 failed at f483cfe in 120 s; failing: test_run_rewrites_a_frontmatter_id_and_a_supersedes_that_name_a_ledger_entry_it_numbered
- Final: Suite: 592 passed, 0 failed at 8d06d6d in 119 s (1 skipped)

## Tests changed under an allowance
- tests/scenarios/migration_spec_steps.py rests_on Given and Then: setup and wording made parametric (interim). The old literal assertion is the special case `design-decision/example.org/acme/shop/a`.

## Open questions
As in the plan §5. None added. The r2 and r5 scenarios are silent on `decision/<slug>` collisions with numbered entries.

## Plan code
The plan contained no code.

## Surprising
The earlier commits had already done the plan's production work. Only the last scenario was left.

## Commits
8d06d6d

## Files changed
scripts/migrate_ledger.py, tests/scenarios/migration_ledger_steps.py, tests/scenarios/migration_spec_steps.py. All under 300 lines.
