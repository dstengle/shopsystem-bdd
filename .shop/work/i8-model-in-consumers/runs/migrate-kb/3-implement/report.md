# Report: migrate-kb implement

## Budget
scripts/migrate, scripts/migrate_layout.py, scripts/migrate_ledger.py, scripts/migrate_spec.py,
tests/scenarios/test_migration_tools.py, tests/scenarios/migration_ledger_steps.py, tests/scenarios/migration_spec_steps.py,
tests/scenarios/migration_old.py, tests/scripts/test_migrate_layout.py (9 files, all in the plan's file set).

## What changed
- migrate_ledger: unnumbered `## decision/<slug>` entries are numbered in ledger order from one above the ledger's highest (r13); an entry another entry supersedes gets status superseded (r2); `supersedes` keeps the id alone, the qualifier goes to `by` after the source (r17).
- migrate_layout: moves for `docs/superpowers/requests/` (r8) and `adrs/` (r14); ids for both (r9, r12); every written text is `git add`ed and `spec/decisions/index.md` is written by model's own `render_decisions` and added (r16); `uncommitted()` helper (r15).
- migrate: an uncommitted or untracked path is reported together with the other failures, nothing written (r15, D1); the index is written after `write`.
- migrate_spec: a short capability id becomes the full one and is recorded in `renamed`; `formulated_as` is removed.
- Tests: Givens and Thens in the feature's wording for all 22 red scenarios; bodies in the record Givens long enough for git to see a rename (D9); a `spec/index.md` in the r6 rows 2-4 Givens (D2); the r6 Then asserts the feature's wording only (D10); `record_kind` test for an ADR and a request.

## Red and green
Red: `python3 -m pytest -q -p no:cacheprovider tests/scenarios/test_migration_tools.py -k "supersedes_and_revisit"` failed first with the undefined Then, and after the Then was added with `AssertionError: accepted` (0003-b not superseded). The other scenarios were red as the research notes record: undefined Givens, then, with the steps written and before the code, failing at the Then (`FileNotFoundError` for `.shop/records/archive/requests/q1.md`, `['R  work/i1/w1.md -> .shop/work/i1/w1.md', 'D  spec/decisions.md', '?? spec/']`, `formulated_as is not read`, and so on). Green: `python3 -m pytest -q -p no:cacheprovider tests/scenarios/test_migration_tools.py tests/scripts/test_migrate_layout.py` gave 41 passed.

## Suite records
Starting: Suite: 568 passed, 22 failed at 5dca7d8 in 119 s (the brief's record).
Final: Suite: 591 passed, 0 failed (1 skipped) at 63109eb in 120 s.

## Tests changed under an allowance
Tests first committed after the initiative's base, rewritten to what a plan decision says (step definitions, per the plan's "Tests the decisions break"): none of the base-era tests changed what they assert. Step definitions rewritten as the plan lists: `migration_spec_steps.py` r6 row-1 Given (adds adrs and requests), r9/r12 Givens (new wording, bodies), the r6 Then (wording and D10), `migration_ledger_steps.py` one-entry r7 Given (replaced by the in-order form), the r11 title Given (wording), the "nothing but the entry" Given (now sets `ledger` too), `test_migration_tools.py` the r8 Given and the "plans and specs are gone" / "each of the two" Thens (replaced by the three- and one-file forms). Allowance: setup/wording only.

## Open questions
- D8 (a malformed `retired` crashes with a traceback): not implemented, no scenario asserts it.
- A repository with no `spec/index.md`: model check still reports it missing; migrate creates none (D2).
- A malformed `--context`; an entry with no date or no source (empty `date:`; `by` starting "; supersedes" with no source); a `supersedes` naming a decision outside the ledger, a list, or an unresolved qualified reference; a capability id in another form; rename detection for a very small real record.

## Other
The plan contained no code. No file crossed 300 lines (largest: 209). No Outside the file set edits.

## What someone can now do
Run `migrate run` on a kb-shaped repository: requests and ADRs move, ids and abouts are given, ledger entries without numbers are numbered, superseded entries are marked, a dirty tree is refused with its paths named, and the result is staged with `spec/decisions/index.md` current.

## Surprising
Rows 2-4 of r6 needed a `spec/index.md` in the Givens (D2). The r7 refusal text changed slightly for the unnumbered heading (adds `or ## decision/<slug>`).

## Commits
78af164, 8019602, 63109eb.
