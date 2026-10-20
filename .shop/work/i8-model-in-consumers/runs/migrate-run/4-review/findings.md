# Review of migrate-run (i8-model-in-consumers)

**Verdict: DONE.** No finding is Critical and none is triaged fix now. The one commit binds the feature lines that the
blind formulator reworded in e963f03, which came before the claim. Every changed step follows a changed feature line.
One assertion is gone: "an about that is there is kept". The feature line it bound was removed before the claim. The
code still keeps such an about.

## Commits reviewed

The claim commit is `7d9c2f3 work: migrate-run ready -> claimed`. There is no branch (a detached checkout), so the
commits are those between the claim and `d697a91 work: migrate-run claimed -> done`, less work run's own:

- `9920c24 migration-tools steps: the formulated wording of r1, r2, r11 and r12 bound`. It changes
  tests/scenarios/migration_ledger_steps.py (+23/-6), tests/scenarios/migration_spec_steps.py (+7/-13) and
  tests/scenarios/test_migration_tools.py (+18).

This matches the implementer's result.json, which lists `9920c24` only. Nothing under `features/` changed, and no
file under `scripts/` changed.

## Removed and weakened tests

I looked in the diff for removed `def`/`@then`/`@given`, removed `assert` lines, loosened comparisons, parametrize
cases, skip and xfail.

1. **migration_spec_steps.py, the `@then("{first} and {second} are about {ref}")` and `@then("{rel} is about {ref}")`
   steps were deleted.** The r12 Given was also rewritten: p2.md (which had an about) became run1-test-log.md.
   - Before: the r12 scenario proved two things. A moved plan and design note with no about get
     `bounded-context/<path>`. A moved plan p2.md that has an about keeps
     `capability/example.org/acme/shop/thing`.
   - Now: p1, s1 and run1-test-log.md each get `bounded-context/<path>`. Nothing asserts that an existing about is
     kept.
   - The cause is e963f03, before the claim: the feature line "And …/p2.md is about capability/…/thing" is gone from
     features/migration-tools.feature.
   - The plan does not list it under "Tests the decisions break". The plan says "None", and it predates r12: it
     accepts r1-r11.
   - Finding F1 below.
2. **migration_ledger_steps.py, the Then `…has the summary "We do a." and a Decision of "We do a." and then "Because b."`
   was split** into `…has the summary "We do a."` and `its Decision has "We do a." and then "Because b."`. The same
   two values are asserted with `==`, so nothing is weakened. A new Then, `its date is 2025-03-01 and its by is alice`,
   also asserts with `==`.
3. **migration_ledger_steps.py, the Then `…a Decision of "We do a."` was respelled `…its Decision has "We do a."`.** It
   is a decorator change only. The body still asserts summary `==` and Decision `==`, so nothing is weakened.
4. **migration_ledger_steps.py, the title-ledger Given was split.** It now stores a template, and the new Given
   `the entry's first paragraph is "We do a."` writes it. The text written is the same: `"%s\ndate"` with
   `"We do a.\n"` gives `"We do a.\n\ndate"`, as before. It adds and removes no assertion.
5. **test_migration_tools.py, a new Then `<new> has the content <was> had, apart from (the id r9 gives it | any id r9
   and about r12 give it)`.** It binds feature lines that used to read `has the content <was> had`. The old exact step
   is still there and still binds w1.md. In the r1 scenario, the assertion on 0001-d0.md and r1.md is looser than
   before because the feature line itself changed. The step is also looser than its line: see F2.

The scenarios also lost some Thens in e963f03, outside these commits. "ends an entry's first paragraph…" no longer
asserts the Decision or the status, and "replaces a ledger that holds a title…" no longer asserts the Decision. The
feature change is binding and the implementer did not do it, so these are not findings against this commit.

## Allowances

The report's rows:

- **The title-ledger Given (setup): holds.** The diff adds, removes and changes no `assert`, no expected value and no
  parametrize case (item 4).
- **The Decision/summary Thens "respelled to the feature's lines": holds in effect.** Items 2 and 3: the same expected
  values, still compared with `==`. The row names no kind (setup or interim). Strictly, splitting a step is more than a
  setup change, but it proves what it proved before.
- **The r12 about Given/Then "replaced by the formulated ones": does not hold as stated.**
  - As setup: an assertion is removed (p2.md keeps its about).
  - As interim: the files were first committed after the base (c8eb7d6 and ce4584c are after 31e9ed3), but the
    plan's decisions say nothing about r12, so the test does not "assert what a decision of the plan says".
  - It is therefore graded as an unlisted removal (F1). What drove it is a person-approved feature change, not the
    implementer.

## Cannot verify

- The suite records in the report (start 570 passed / 7 failed, final 577 passed / 0 failed / 1 skipped): I did not
  run the whole suite. The 26 migration-tools tests pass here.
- "scripts/migrate needed no change (r12 `about` and the ledger fields were already implemented)": this is true for
  this commit, since scripts/ is untouched. That the earlier fix commits were reviewed is outside this run.
- The plan is stale. It accepts r1-r11 and ten scenarios, while the work-item accepts r1-r12 and the feature now
  gives 26 tests. I cannot check the r12 and reworded-r2/r11 bindings against a plan decision, because there is none.

## Findings

### F1. Important (per the rule for an unlisted removed assertion). Triage: observation

- **Where:** tests/scenarios/migration_spec_steps.py:164-176 (commit 9920c24). The step
  `{rel} is about {ref}` was deleted, along with the p2.md fixture that had an about.
- **What is wrong:** no test now asserts that a moved record which already has an `about` keeps it. The plan does not
  list the removal, and the report's allowance row does not hold (see Allowances).
- **Why it matters:** r12 applies only "when … the record has no `about`". Overwriting an existing about would be data
  lost, and no scenario would catch it.
- **What I checked:** `scripts/migrate_layout.py:52-64`, `with_id`. It adds `about:` only when
  `not re.search(r"^about:", <frontmatter>)`, and returns the text unchanged when it already has an id. So today the
  about is kept, and nothing is wrong now.
- **Reproduction:** read `with_id` (lines 52-64). The p2 case of the old scenario, before e963f03, passed against the
  same code at ce4584c..5eaf500.
- **Fix:** if the person wants that pin back, the formulator adds a scenario line (the feature is read-only here).
  Also, the next plan should list such removals.

### F2. Minor. Triage: observation

- **Where:** tests/scenarios/test_migration_tools.py:52-62. This is the new `has the content … apart from …` step.
- **What is wrong:** it strips any `id:`, `kind:` and `about:` line from the migrated file before comparing. It does
  not check that those lines are the ones r9/r12 give, with the right kind and the right value.
  - For records/logs/r1.md, r9 gives no id (it is not a plan, a design note or a test log). Yet the step would also
    pass if migrate wrongly gave it `id: measurement/…`, `kind:` and `about:` frontmatter.
  - For 0001-d0.md, it would pass if migrate replaced its existing id with any other id.
- **Why it matters:** the line promises "apart from the id r9 gives it", but the step accepts any id.
- **What I checked:** `record_kind` (`scripts/migrate_layout.py:67-77`) returns None for `.shop/records/logs/r1.md`,
  and `with_id` leaves a file that has an id unchanged. So today both files are byte-for-byte equal and the loose
  branch is not reached. Reproduction: read those two functions. The tests pass with the files unchanged.
- **Fix:** compare the stripped lines against the expected ones: none for r1.md, and the file's own id for 0001-d0.md.

### F3. Minor. Triage: drop

- **Where:** work-item `fileset:`.
- **What is wrong:** it lists scripts/migrate, test_migration_tools.py and test_bound.py. The commit changes
  tests/scenarios/migration_ledger_steps.py and migration_spec_steps.py, which are outside it. Those modules were made
  by the split in ce4584c, and the fileset was never updated.
- **Fix:** add the two step modules (and scripts/migrate_*.py) to the fileset.

### F4. Minor. Triage: drop

- **What:** ruff reports 15 issues (I001, UP031, RUF100) in the three changed files.
- **What I checked:** none is on a line this commit added (the flagged lines are 3, 28, 52, 140; 2, 28, 64, 83, 121,
  130; and 10, 12, 18, 91, 133). They predate the commit, and the new lines follow the files' existing `%` style.

## Checks run

- `git log --grep "^work: migrate-run ready -> claimed$"` gives 7d9c2f3. `git log --stat 7d9c2f3..d697a91` gives the
  one implementer commit. Then `git diff 7d9c2f3 9920c24`.
- `git show e963f03 -- features/migration-tools.feature`: the feature rewording, before the claim.
- `git log --diff-filter=A` on the three test files: first committed in c8eb7d6 and ce4584c, after the base 31e9ed3.
- `tools check --base 7d9c2f3` gives:
  - **ruff:** 15 issues, all predating the commit (F4).
  - **vulture:** clean.
  - **import-linter:** the project states no import contracts.
- `python3 -m pytest -q tests/scenarios/test_migration_tools.py`: 26 passed.
- I read `scripts/migrate_layout.py` `with_id` and `record_kind`. The risks were that an existing about is overwritten
  (F1) and that r1.md gets an id (F2). Neither happens.
- `git status --short`: clean. Nothing in the checkout was changed.
