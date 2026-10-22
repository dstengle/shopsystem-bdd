# Plan: migrate-kb (migration-tools r1-r17)

From the research notes (`runs/migrate-kb/1-research/notes.md`), the feature `features/migration-tools.feature`, the
capability and the design-decisions it rests on. The 38 scenarios: 22 are red and 16 pass (the notes' run).
`features/migration-tools.feature` does not change. No work-item rulings; no Retires section; nothing deprecated.
Where the work-item's labels differ from the spec (r7/r15, r6/r16, r2/r17; notes C3), the spec's labels are used.

## 1. What goes green

Already passing, and they must keep passing: r1 x2, r2 (entry/first paragraph; date or source line; outline x3; whole text), r3, r4, r5,
r7 ledger text x2, r7 two changes, r7 untracked .shop/work file, r10.

Red today, and why:
- **migration-tools#r2**: "run gives a decision file its entry's supersedes and revisit_when, and the entry it supersedes the status superseded". The Then "...'s status is accepted" has no step definition, and `decision_text` always writes `status: accepted` (p01).
- **migration-tools#r17**: "run writes a qualified supersedes as the decision's id alone, the qualifier going to by beside the source". Its Given has no step definition, and the raw `decision/0003-b (for artifacts)` is written, with `by` holding only the source (p02).
- **migration-tools#r11**: "run removes a ledger that holds nothing but <what> ...", both rows. Row "its entries" fails in the test: the "nothing but the entry" Given sets `context["entry"]`, and the next Given reads `context["ledger"]`, giving a KeyError. In row "a title and its entries", the Given's wording ("starts with the title") does not match the feature's ("has the title ... and a blank line"). The code already does both (p03, p03b).
- **migration-tools#r13**: "run numbers each ledger entry with no number ...", both rows. The "has, in order, the entries" Given has no step definition, and `ENTRY`/`ledger_entries` refuse a heading with no number (p04, p05).
- **migration-tools#r7**: "run whose ledger entry's decision file would land on <there> ...", all four rows. The Given takes one entry only, so it is undefined for this wording. Rows 1-3 already refuse correctly (p06-p08). Row 4 refuses for the wrong reason, the missing r13 numbering (p09).
- **migration-tools#r6**: "after run on a repository with <what>, model check reports no unresolved reference or file problem", all four rows.
  - The Givens have no step definitions, and the Then's wording differs from the feature's (step says "no violation, ...").
  - Row 1 already passes in code (p12).
  - Row 2 keeps `formulated_as` (p13).
  - Row 3 keeps `capability/thing` (p14).
  - Row 4 leaves a qualified supersedes unresolved (p15).
  - Rows 2-4 also get "spec/index.md is missing" (p13b; see decision D2).
- **migration-tools#r8**: "run moves docs/superpowers/plans/, specs/ and requests/ under .shop/records/archive/, with git". The Given has no step definition, and `DIRECTORY_MOVES` has no requests entry (p16).
- **migration-tools#r14**: "run moves adrs/ to .shop/records/decision-arguments/, with git". The Given has no step definition, and there is no `adrs/` move (p18).
- **migration-tools#r9**:
  - "run gives a capability, a decision file, a plan, a request, a design note, an ADR and a test log the type-first id of its kind": the Given has no step definition. Requests and ADRs are not moved, so they get no id (p17).
  - "run gives a capability whose id is the short form capability/<name> its full id": the Given has no step definition, and `with_id` keeps an existing id (p14).
- **migration-tools#r12**: "run gives each moved record kind with no about the context as its about". The Given has no step definition (it now includes requests and ADRs), and those are not moved.
- **migration-tools#r15**: "run on a repository with <change> refuses, naming it, ...", both rows. The Givens have no step definitions, and there is no check for a dirty tree (p19, p20).
- **migration-tools#r16**: "run adds every file it wrote or moved to git and writes spec/decisions/index.md". The Given has no step definition. Written texts are never staged (p16 `RM`, p22 `?? spec/`), and no index is written.

## 2. Where the change lands

- `scripts/migrate`: `cmd_run` gathers the uncommitted changes before planning (r15) and reports them together with every failure from planning and from `check_moves` (D1). After `write()`, it has the decisions index written and staged (r16, D7).
- `scripts/migrate_layout.py`:
  - adds the `docs/superpowers/requests/` move (r8) and the `adrs/` move (r14) to `DIRECTORY_MOVES`;
  - `record_kind` gives `decision-argument` under `.shop/records/decision-arguments/` and `initiative-archive` under `archive/requests/` (r9);
  - `with_id` rewrites a short capability id and records the rename (r9, r5);
  - `write()` runs `git add` on every text it writes (r16);
  - a helper reads `git status --porcelain` (r15).
- `scripts/migrate_ledger.py`:
  - unnumbered entries are accepted and numbered (r13);
  - an entry gets status superseded when another entry supersedes it (r2);
  - the qualifier is split out of `supersedes` (r17).
- `scripts/migrate_spec.py`: `formulated_as` is removed (r6, D5); a crash on a malformed `retired` becomes a named refusal (D8). `plan_index` does not change (D2).
- `tests/scenarios/test_migration_tools.py`: new Then steps for r8 and r14 (rename), r15 (refusal naming), r16 (staged and nothing untracked; `model decisions --check`), and the r2 status Then. It has the most room (147 lines), so new steps go here first.
- `tests/scenarios/migration_ledger_steps.py`:
  - the "has, in order, the entries ..." Given, shared by the r13 rows and the r7 "<there>" rows (it replaces the one-entry Given at :47-49);
  - the r17 Given;
  - the r11 title wording (:111);
  - the "nothing but the entry" state fix (:7-9, :117-119).
- `tests/scenarios/migration_spec_steps.py`:
  - Givens with the feature's wording for r6 rows 1-4, r8, r14, r9 (both scenarios), r12 and r15;
  - the r6 Then's wording (:150).
- `tests/scenarios/migration_old.py`: a helper the Givens share, for a repository's `spec/index.md` (D2), and one for a tracked file changed after the commit (r15).
- `tests/scripts/test_migrate_layout.py`: a `record_kind` case for an ADR and one for a request. The four existing cases stay.

This is the researcher's set; no file is added or removed. Every module stays under 300 lines (work-item). If `migration_spec_steps.py` (176 lines) or `migration_ledger_steps.py` (140 lines) would pass 300, its new steps go to `test_migration_tools.py`, not to a new file.

## 3. Decisions

- **D1. A dirty tree is refused together with every other failure, not in place of them.** `migrate run` names each uncommitted path (tracked changes and untracked files; files git ignores are not counted). It still plans and checks, and names every change it could not make. It exits non-zero and writes nothing. This rests on migration-tools#r15 together with migration-tools#r7 ("naming each change it could not make"). Two scenarios need both. "run that would move a file onto an untracked file" leaves an untracked file, which r15 counts as uncommitted, and its Then wants the move named. r7's row "an untracked spec/decisions/0007-a.md" wants the ledger write named. A refusal that named only the uncommitted file would break both (notes C1).
- **D2. migrate does not create `spec/index.md`; the r6 Givens give the repository one.** A repository on the old system has a `spec/index.md`:
  - migration-tools#r4 gives an id to an index that already exists and never creates one;
  - design-decision/migration-in-one-pass leaves "the context path when spec/index.md lacks it" to the session, and migrate "refuses rather than guesses";
  - the existing Given for row 1 already writes `spec/index.md`.

  So in rows 2-4 the repository on the old system has an index (notes C2, reading B). migrate does nothing new here, so the narrator sees no change.
- **D3. r13 numbering counts the ledger alone.** The highest number is the highest among the ledger's numbered entries, or 0 if there are none. Unnumbered entries take numbers in ledger order. A number that lands on a file in `decisions/` that moves to `spec/decisions/` is an r7 refusal and is not skipped over. This rests on migration-tools#r13 ("the ledger's highest entry number") and the fourth r7 row, which expects `## decision/b` to be refused at `0008-b.md`. An unnumbered entry's id is `design-decision/<path>/<slug>`, and it goes into the renamed map like any other entry (r9, r5).
- **D4. Superseded and qualified supersedes.**
  - An entry's qualifier is the text after the first whitespace that follows its reference, kept as written (parentheses included).
  - `supersedes` gets the resolved id alone.
  - `by` gets the source, then `; supersedes <id> <qualifier>`. This rests on migration-tools#r17 and its Implementation line, and the scenario's expected `by`.
  - An entry is `superseded` when another entry's `supersedes` (after the qualifier is removed) resolves to it. Otherwise it is `accepted`. This rests on migration-tools#r2.
- **D5. `formulated_as` is removed from a capability's frontmatter.** This rests on migration-tools#r6 (model check reports it, scripts/model:550-552) and design-decision/references-are-ids ("formulated_as is gone").
- **D6. A capability id is rewritten only when it is the short form `capability/<name>` (the name being the file's stem).** The new id is `capability/<path>/<name>`, and the old-to-new pair goes into the renamed map, so references to it are rewritten. Any other existing id is kept, as today; r1's decision file depends on that. This rests on migration-tools#r9, migration-tools#r5 and design-decision/capability-ids-are-context-scoped (the short form is `<kind>/<name>`; the frontmatter id is the full form).
- **D7. r16:**
  - `write()` stages every text it writes (moves are already staged by `git mv`, the ledger's removal by `git rm`).
  - After the decision files are on disk, `spec/decisions/index.md` is written, and staged, by scripts/model's own decisions-index writer (the one `model decisions` uses, loaded by path as migrate already loads model), not by a copy of it.
  - It is written on every successful run, even when there are no decision files, because r16 has no condition.

  This rests on migration-tools#r16 and its Implementation line ("as `model decisions` writes it").
- **D8. A `retired` entry that is not `r<n>` is a named refusal, not a traceback.** It is a change migrate cannot make, so it exits non-zero, names it, and changes nothing. This rests on migration-tools#r7 (notes D2, p25). No scenario covers it, so a case in `tests/scripts/` is optional and not part of this plan's fileset.
- **D9 (test side). The record files in the r8, r14, r9 and r12 Givens have bodies long enough that, after r9/r12 add id and about frontmatter and r16 stages the result, git still detects the rename.** git's default similarity threshold is 50%, and a one-line body such as "A plan." would show as deleted plus added. This rests on migration-tools#r8 and migration-tools#r14 ("git sees each move as a rename") together with migration-tools#r16. The implementer confirms this when the r8 scenario first goes red.
- **D10 (test side). The r6 Then asserts only what the scenario and r6 name: the report's unresolved references and file problems are empty.** It does not assert that there are no violations, and does not depend on the exit code that violations would change. This rests on migration-tools#r6. Its wording becomes the feature's.

## 4. Tests the decisions break

- `tests/scenarios/test_migration_tools.py::test_run_that_would_move_a_file_onto_an_untracked_file_names_the_move_exits_nonzero_and_changes_no_file`: under D1 it keeps passing. The refusal names `.shop/work/i1/w2.md` as untracked and also the move. Nothing is rewritten.
- `tests/scenarios/migration_spec_steps.py`:
  - the Then at :150 ("no violation, no unresolved reference and no file problem") is rewritten to the feature's wording and asserts what D10 says;
  - the row-1 Given at :117-136 is rewritten to the feature's wording, adding `adrs/0001-use-x.md` and `docs/superpowers/requests/q1.md`. It keeps `spec/index.md` (D2);
  - the Givens at :39-44 (r9) and :164-170 (r12) are rewritten to the feature's wording, which now includes the request and the ADR, with bodies that follow D9.
- `tests/scenarios/migration_ledger_steps.py`:
  - the one-entry Given at :47-59 is replaced by the "has, in order, the entries ..., and <there>" form (D3);
  - the title Given at :111 is reworded to "has the title `# Decisions` and a blank line, then the entry ...";
  - the "nothing but the entry" Given (:7-9) is made to leave the state the "first paragraph" Given (:117-119) reads.

  These are wording and state fixes; what each asserts does not change.
- Checked and unaffected:
  - the r1 git-status test: three `R` entries remain, and staging the written ids does not change that, because records/logs/r1.md gets no id;
  - the r2 "status accepted" Then: nothing supersedes that entry;
  - r3, r4, r5 and r10;
  - the r7 two-changes test: its Givens commit, so the tree is clean;
  - the r3 copy, which is made outside the repository root and so is not untracked dirt under D1;
  - `tests/scripts/test_migrate_layout.py`'s four cases (D6 and the new `record_kind` branches leave them as they are);
  - `tests/scenarios/test_design_model_check.py` (model unchanged).

## 5. Open cases

Left for the implementer to name; none is chosen here:
- A repository with no `spec/index.md`: after D2, model check still reports it missing.
- A malformed `--context` such as `shop` (notes D4, p24) is accepted and written into ids.
- An entry with no date or no source writes empty `date:` and `by: ""` (notes D6, p28). Under r17, with no source, `by` would start with "; supersedes".
- A `supersedes` that names a decision outside the ledger (a moved `decisions/` file), a list of several, or a qualified reference that resolves to nothing. r2 says nothing of a moved file's status.
- A capability id in a form other than `capability/<name>` or the full form (e.g. another context's path).
- Rename detection for a very small real record (D9 holds in the tests, not in every repository).
