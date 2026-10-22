# Plan: migration-rebind-1 (migration-tools r1, r2, r4, r5)

## 1. What goes green

Accepted: 18 scenarios in `features/migration-tools.feature`, 21 test ids. The research run shows 20 green and 1 red.

- **migration-tools#r1**: green today.
  - `migrate run` relocates decisions/ to spec/decisions/, work/ to .shop/work/ and each records/<x> to .shop/records/<x>, with git
  - `migrate run` relocates a file under records/ that is not text as it is
  - `migrate run` from a subdirectory relocates the repository's top-level directories
- **migration-tools#r2**: green today.
  - `migrate run` replaces a ledger entry with a decision file named by its heading, with its first paragraph, accepted, with its date and source
  - `migrate run` ends an entry's first paragraph at its date or source line, with or without a blank line before it
  - `migrate run` writes a first paragraph and a source that hold <what> so that model reads them as they are (outline, three rows)
  - `migrate run` puts an entry's whole text in its decision file's Decision, its first paragraph also being its summary
  - `migrate run` gives a decision file its entry's supersedes and revisit_when, and the entry it supersedes the status `superseded`
  - `migrate run` keeps both decisions an entry's supersedes names, each by its new id, and supersedes both
- **migration-tools#r4**:
  - `migrate run` gives spec/index.md the id bounded-context/<path>: green today.
  - `migrate run` gives spec/index.md whose id is bounded-context/shop the id bounded-context/<path>: **red**. Its Given ("a repository on the old system whose spec/index.md gives the id {ident}", `tests/scenarios/migration_safety_steps.py`) writes `spec/index.md` but does not commit it. So migrate's uncommitted-tree refusal (r15) fires: exit 1, nothing written, and the Then reads the old id `bounded-context/shop`. The product's rewrite is right: probes P1–P4 pass on a committed tree, and probe U1 reproduces the refusal.
- **migration-tools#r5**: green today.
  - `migrate run` rewrites a repository-relative path, a relative Markdown link and a frontmatter id that name what it relocated or renamed
  - `migrate run` rewrites a frontmatter id and a supersedes that name a ledger entry it numbered
  - `migrate run` rewrites a decision file's by that names <old>, a path it relocated (outline, two rows)
  - `migrate run` rewrites a frontmatter id that names the context id it changed (green only because its second Given, "a tracked notes/n1.md …", commits the tree that the first Given left uncommitted)
  - `migrate run` rewrites nothing through a tracked symbolic link, and leaves the file outside the repository it points to as it was
  - `migrate run` keeps the CRLF line endings of a file in which it rewrites a path

Deprecated scenarios retired: none (the work-item has no Retires section).

## 2. Where the change lands

- `tests/scenarios/migration_safety_steps.py`: the Given "a repository on the old system whose spec/index.md gives the id {ident}" commits the repository after writing `spec/index.md`, using the fixture's existing `commit` (in `tests/scenarios/migration_old.py`), as the other old-system Givens do. The file has 120 lines, well under the 300 limit.

This is the researcher's set, unchanged. The work-item's broader fileset (`scripts/migrate`, `scripts/migrate_*.py`, the other migration step modules and `test_migration_tools.py`) needs no edit. The researcher read and ran them, and they stay green.

## 3. Decisions

- **D1: fix the test step, not the product.** The scenario's Given describes "a repository on the old system", meaning a committed starting tree. Migrate refusing an uncommitted tree is migration-tools#r15 itself, so the refusal is correct and the Given is what is wrong. This decision rests on migration-tools#r15 (refuse on uncommitted changes) and migration-tools#r4 (the id the narrator observes after a successful run). The narrator observes nothing new: the scenario's Then already states the outcome.
- **D2: commit in the Given itself, not in the When.** This keeps the When step that all migration scenarios share unchanged. The r15 scenarios depend on the When leaving the tree as the Givens built it (migration-tools#r15).

## 4. Tests the decisions break

None. Here is what I checked:
- The r5 scenario "rewrites a frontmatter id that names the context id it changed" shares this Given. Its next Given writes `notes/n1.md` and commits again. That second commit still has a change to commit (`notes/n1.md`), so it does not fail on an empty commit, and the scenario stays green.
- The researcher found that no accepted requirement breaks an existing test. `tests/scripts/test_migrate_layout.py` (4 tests) and `tests/scripts/test_migrate_write.py` (3 tests) do not use the scenario steps.
- No other scenario uses the edited Given. Only lines 342 and 349 of the feature file match its text.

## 5. Open cases

- An index whose id is already `bounded-context/<path>`. The researcher read that it is left unchanged but did not probe it, and no scenario covers it.
- Reference-style Markdown links (`[x]: path`). The researcher read that `migrate_spec.rewrite_text` does not rewrite them, and no r5 scenario uses one. The implementer should name this as not covered, not fix it here.
- A moved path that appears inside a longer path is not rewritten, and no scenario covers it.
