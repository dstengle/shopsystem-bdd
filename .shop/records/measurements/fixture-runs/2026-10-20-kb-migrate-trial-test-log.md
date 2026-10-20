---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-20-kb-migrate-trial-test-log
kind: measurement
about: capability/missingmass.io/shopsystem/shopsystem-bdd/migration-tools
date: 2026-10-20
---

# Test log: the i8 trial, `migrate run` on a fresh clone of shopsystem-kb (refused)

`scripts/migrate run --context missingmass.io/shopsystem/kb` from this repository (branch release-0.21.0 at 3b6b8b5),
run on a fresh clone of https://github.com/dstengle/shopsystem-kb (main at 2eed357, "kb 0.9.0, contract kb.v2").
The trial ran in a clone of its own; migrate was not edited.

**Outcome: refused, exit 1, no file changed.** It named 123 changes it could not make, all of one kind: a ledger
entry with no number. That refusal goes to the person (below). To see what the lines leave uncovered after that
refusal, a **probe**, separate from the trial, ran migrate on a second clone. In that clone the 123 headings were
numbered by hand, 0032 on in ledger order, and committed. Everything after "Probe" comes from that probe. It is
not evidence of how migrate behaves on kb as it stands.

## Before (the trial clone)

- Old layout present: `spec/decisions.md` (a ledger of 154 entries; 31 are `## decision/<nnnn>-<slug>`, numbers
  0001-0031 mirroring `adrs/0001-0031`, and 123 are `## decision/<slug>` with no number); `docs/superpowers/plans/`
  (41 files plus `archive/`, 15 files; the living plan is `2026-09-24-kb-slices.md`); `docs/superpowers/specs/`
  (9 design notes); `docs/superpowers/requests/` (1 file); `adrs/` (31 ADRs and a README). There is no top-level
  `decisions/`, `records/` or `work/`.
- `spec/index.md` has no frontmatter. The 21 capabilities have `id: capability/<name>` (the short form),
  `formulated_as:`, no `retired:`, Behaviour lines with no `[r<n>]`, and `rests_on` naming both `decision/<nnnn>-<slug>` and
  `decision/<slug>`.
- Ledger fields: date 154, source 154, supersedes 31, revisit_when 23, by 0. Some `supersedes` values carry a
  qualifier, such as `decision/0002-ids-minted-from-titles (for artifacts)`, and one names two ids.
- `git status`: clean, on main.
- Suite (README/Makefile: `make dev`, `make test` = `.venv/bin/python -m pytest -q -n auto`; venv in the clone):
  **1603 passed**, 2564 warnings, 34.9 s. `tests/slices.py` reads the living plan by path:
  `PLAN = "docs/superpowers/plans/2026-09-24-kb-slices.md"`.
- Scenarios per feature (21 files, 361 scenarios): answer-a-damaged-file 6, change-the-store 24, check-a-change 23,
  check-the-store 7, define-a-type 29, export-and-import-a-store 34, export-through-the-contract 8, find-the-store
  20, hand-over-content 16, keep-the-history 19, make-several-changes-in-one-go 23, name-artifacts-and-items 24,
  name-what-is-asked-for 16, operate-a-store 48, query-the-store 15, reach-a-served-store 11, read-an-artifact 13,
  serve-a-store-for-tests 4, sign-a-change 1, snapshot-what-work-read 3, start-a-store 17. No `@holding` scenario.
  `features count --by-tag` saved with the baseline.

## The trial's run

```
$ scripts/migrate run --context missingmass.io/shopsystem/kb      # exit 1
migrate changed nothing; it could not make these changes:
  could not replace the ledger entry `## decision/serialization-yaml` of spec/decisions.md: its heading is not `## decision/<nnnn>-<slug>`
  ... (123 lines in all, one per unnumbered entry, from serialization-yaml to the last entry of the ledger)
```

Afterwards `git status` was clean and HEAD was unchanged, so r7 held. No other kind of failure was named. Every
planner runs before the check (`plan_moves` … `check_moves`), so the moves, ids and references found nothing else
they could not do.

**Judgement: a genuine case for the person, not a defect of migrate.** r2 replaces only entries headed
`## decision/<nnnn>-<slug>`, and r7 requires a refusal for any change migrate cannot make. migrate refused rather
than guess, which is what design-decision/migration-in-one-pass asks. No line says what number an unnumbered entry
gets. Every choice needs judgment: ledger order from 0032, date order, or matching to `adrs/`. kb's 0001-0031 are
ADR numbers, and 0049 lists numbering lines as transcription but says nothing about numbering decisions. The
question for the person: **what number does a ledger entry with none get?** Step 3 of the brief (model check,
suite, diff on the trial) did not happen, because nothing ran.

## Probe (second clone, ledger headings numbered 0032-0154 by hand in ledger order, committed)

### A defect found by accident: migrate writes half of a run when git refuses a step

On the first probe attempt the hand edit was left uncommitted, because the clone had no git identity. migrate's
plan passed `check_moves` and `write` began. It made all **65 `git mv`s**, then
`git rm -q spec/decisions.md` failed because the file had local changes. migrate exited with a Python traceback
(`CalledProcessError`) and left 65 staged renames and nothing else. That breaks r7 ("exit non-zero, naming each
change it could not make, and change no file"). migrate checks neither a clean working tree nor whether a file it
removes has local changes. Each git step runs with `check=True` and nothing rolls it back. The probe clone was then reset.

### The probe's run: exit 0

- `git status`: 65 `RM` (git sees the moves as renames: index R100, with the id frontmatter as an unstaged change),
  25 ` M`, `D  spec/decisions.md`, `?? spec/decisions/` (154 decision files, **written but not added**). The moves:
  56 plans (the `archive/` subdirectory included) to `.shop/records/archive/plans/`, and 9 design notes to
  `.shop/records/archive/design-notes/`. `git diff -M --stat`: 90 files, +1009 -681.
- Suite (kb-trial's venv, `PYTHONPATH=src`): **1603 passed**, the same tests by name as before (diff of the
  `PASSED` lines is empty). r5 rewrote `tests/slices.py` `PLAN` to `.shop/records/archive/plans/2026-09-24-kb-slices.md`,
  and the tests still run. The plan still governs `@slice-<n>` xfails from under `archive/`.
- `features count --by-tag`: identical to the baseline. `features/` unchanged (no `@holding`).
- r10: 371 Behaviour lines numbered `[r1]`… in the 21 capabilities. r4: `spec/index.md` was given a new
  frontmatter block with `id: bounded-context/missingmass.io/shopsystem/kb`.
- Moved records (r9, r12): `2026-09-24-kb-slices.md` got `id: initiative-archive/missingmass.io/shopsystem/kb/2026-09-24-kb-slices`,
  `kind: initiative-archive`, `about: bounded-context/missingmass.io/shopsystem/kb`; `2026-09-23-kb-design.md` got
  `decision-argument/…/2026-09-23-kb-design` with the same about. Both are as r9/r12 say.
- References (r5): `README.md` and `CLAUDE.md` paths rewritten to `.shop/records/archive/…`; numbered refs in
  `rests_on` rewritten to `design-decision/missingmass.io/shopsystem/kb/<slug>`. Unnumbered refs were not rewritten,
  because the probe numbered only the headings, so these are the probe's own doing. Prose ids such as
  `(decision/published-contract-v2)` in CLAUDE.md are untouched. r5 covers only paths, links and frontmatter ids.

`model check --limit 100000` on the probe: exit 1, **1103 violations, 21 warnings, 180 unresolved references,
42 file problems**:

| code | count | what | whose |
|---|---|---|---|
| v_e1 | 371 | every kb Behaviour line is not in an EARS pattern | the person: rewording lines is not transcription |
| v_s1 | 361 | no scenario names a requirement | the session: mapping scenarios to lines (0049) |
| v_s3 | 371 | no requirement has a scenario | the session, same |
| w_unserved_cap | 21 | a capability serves no job | warning |
| unresolved | 169 | `decision/<slug>` refs to the entries the probe numbered | the probe's hand edit, not migrate |
| unresolved | 11 | `supersedes` with a qualifier: `decision/0002-ids-minted-from-titles (for artifacts)`, `decision/files-are-an-export (its clause that …)`, two ids comma-joined in 0100 | migrate: copied the value verbatim, not as a list of ids |
| file | 21 | `id 'capability/<name>' is not 'capability/missingmass.io/shopsystem/kb/<name>'` | **migrate**: `with_id` keeps an existing id, so a short capability id is never made full; contrary to r6 (r9 says "gives … its id") |
| file | 21 | `formulated_as is not read; the feature file is features/<name>.feature` | no line removes it |

Decision files, spot-checked (0001 yaml-1-2-git-canonical, 0022 ids-are-chosen-by-the-client-in-a-namespace):
the number and file name are right, `id` is `design-decision/…/<slug>`, the summary and Decision are the entry's
paragraph, status is accepted, date is right. But:

- **`by:` holds the entry's `source`** (`by: "adrs/0001-yaml-1-2-git-canonical.md"`). kb's ledger has no `by`;
  `decision_text` writes `fields["source"]` into `by`, and the `source` field itself is lost. r2 says `by` is the
  entry's own.
- `supersedes:` is a plain string carrying the qualifier (above). A superseded entry is still `status: accepted`.
  The heading is `# <slug>`, not `# <nnnn>. <Title>` as this repository's decision files have.
- No `spec/decisions/index.md` was written (the Implementation note says one exists "as `model decisions` writes
  it"). model check did not report its absence.

What the skeleton left to this trial:

- **Links inside a moved file to files that stayed**: none in kb (no relative Markdown links in the moved plans or
  notes; `](…)` matches were code). Paths in archived plans to `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`
  name a file of another repository and stay. Mentions of `spec/decisions.md` in archived plans stay as history.
- **Paths naming a moved directory** (no file name): none found.
- **Other old records needing ids**: `docs/superpowers/requests/2026-10-10-requests-to-kb-portable-knowledge.md`
  is not moved (r8 names only `plans/` and `specs/`), so a file is left under `docs/superpowers/`, which 0045 says
  the plugin never writes. model check did not report it. `adrs/` (31 ADRs and a README) stays at the top level,
  and every ledger entry 0001-0031 duplicates one. Neither 0045 nor 0049 says where an `adrs/` goes.

## Candidate lines (EARS), each with its evidence

1. **If** `spec/decisions.md` has an entry `## decision/<slug>` with no number, **then** `migrate` shall refuse,
   naming the entry, unless the person has said how such entries are numbered. *(The trial: 123 of 154 entries. The
   current refusal is right but names no way forward; the rule for numbering is the person's question above.)*
2. **If** the working tree is not clean when `migrate run` starts, **then** `migrate` shall exit non-zero, naming the
   changed files, and change no file. *(Probe: 65 `git mv`s made, then a traceback on `git rm` of a modified ledger,
   against r7.)*
3. **If** a git step of `migrate run`'s writing fails, **then** `migrate` shall undo the steps it has made and exit
   non-zero naming the step. *(Same evidence. The check before writing cannot foresee every git refusal.)*
4. **When** `migrate run` finds a capability whose `id` is not `capability/<path>/<name>`, `migrate` shall rewrite it
   to that id, and every reference to the old id. *(Probe: 21 file problems; `with_id` keeps an existing id.)*
5. **When** `migrate run` finds `formulated_as` in a capability's frontmatter, `migrate` shall remove it. *(Probe: 21
   file problems.)*
6. **When** a ledger entry has a `source` and no `by`, `migrate` shall keep `source` as the decision file's `source`
   and write no `by`. *(Probe: `by: "adrs/0001-…md"` in every one of 154 files.)* Whether `by` may be empty is the
   person's call.
7. **If** a ledger entry's `supersedes` is not a list of decision ids, **then** `migrate` shall refuse, naming the
   entry and the value. *(Probe: 11 unresolved, e.g. `decision/0002-ids-minted-from-titles (for artifacts)`.)*
8. **When** `migrate run` writes a decision file, `migrate` shall `git add` it and write `spec/decisions/index.md` as
   `model decisions` does. *(Probe: `?? spec/decisions/`, no index.md.)*
9. **When** `migrate run` is run, `migrate` shall move every other file under `docs/superpowers/` to
   `.shop/records/archive/<its directory>/`, or refuse naming it. *(Trial and probe: `docs/superpowers/requests/` left.)*
   Where an `adrs/` directory goes is the person's question.
10. r6 as written cannot hold on kb. 371 lines not in EARS, and 361 scenarios with no requirement tag, are judgment
    by 0049, not migrate's to do. Candidate rewording: **When** `migrate run` has run, `migrate` shall have left the
    repository so that `model check` reports no unresolved reference or file problem, and no violation but `v_e1`,
    `v_s1` and `v_s3`. *(Probe table.)*

## Files

Trial clone `/home/vscode/.claude/jobs/3dae44af/tmp/kb-trial/` (unchanged but `.venv/`); probe clone `…/tmp/kb-probe/`;
baseline and outputs in `…/tmp/kb-trial-base/` (features copy, count.txt, pytest.txt, migrate.out,
probe-migrate.out, probe-check.out, probe-pytest.txt).

## Trial 2: `migrate run` on a fresh clone after the fixes (r13-r17)

`scripts/migrate run --context missingmass.io/shopsystem/kb` from this repository (branch release-0.21.0 at 57f6247,
migrate as of 63109eb), run on a fresh clone of shopsystem-kb in `…/tmp/kb-trial-2/`. The clone is at main 2eed357,
the same commit as the first trial. migrate was not edited and nothing was committed in the clone.

**Outcome: exit 0, no output, 1.4 s. r6 fails by one file problem.** The suite is unchanged. The other faults are
in the content of the decision files, and model check does not see them.

### Before

The clone is the commit the first trial recorded, and every count was checked against that record again: ledger
154 entries (31 numbered, 123 not), `docs/superpowers/` 41+15 plans, 9 notes and 1 request, `adrs/` 32 files,
capabilities with short ids and `formulated_as`, `tests/slices.py` PLAN under `docs/superpowers/plans/`, no
`@holding`. `features count --by-tag` is byte-identical to the first trial's `count.txt`. `git status` was clean and
the clone had no git identity. The suite result is copied from the first trial: **1603 passed**, 2564 warnings.

### After

- **git status**: every change is staged and nothing is unstaged or untracked (r16). There are 98 `R`, 155 `A`
  (154 decision files and `index.md`), 25 `M` (21 capabilities, `spec/index.md`, `README.md`, `CLAUDE.md`,
  `tests/slices.py`) and `D spec/decisions.md` (r11). `git diff --cached -M --stat`: 279 files, +3265 -1555.
- **Renames are renames**: there are 98, made up of 56 plans and 1 request to `.shop/records/archive/{plans,requests}/`,
  9 notes to `archive/design-notes/`, and 32 `adrs/` files to `.shop/records/decision-arguments/` (r8, r14). Most
  plans and notes are R94-R99. The ADRs are R50-R79, because each ADR is about 3 lines and gains 5 lines of
  frontmatter. `adrs/0009-resolve-depth-and-cycles.md` is **R050**, exactly at git's default threshold, so an ADR
  one line shorter would show as a delete and an add. The renames hold today, but that one is fragile. `docs/` is gone.
- **model check --limit 100000**: exit 1. **1103 violations, 21 warnings, 0 unresolved references, 1 file problem.**

  | code | count | whose |
  |---|---|---|
  | v_e1 | 371 | the session's judgment work (0049): no kb Behaviour line has a `shall` |
  | v_s1 | 361 | the session's judgment work: no scenario names a requirement |
  | v_s3 | 371 | the session's judgment work: no requirement has a scenario |
  | w_unserved_cap | 21 | warning: no job is served |
  | unresolved | 0 | was 180 in the probe: r13 and r17 hold |
  | file | 1 | **migrate**: `.shop/records/decision-arguments/README.md: id 'decision-argument/missingmass.io/shopsystem/kb/README' is not decision-argument/missingmass.io/shopsystem/kb/<name>` |

  The probe's 21 short capability ids and 21 `formulated_as` problems are gone: every capability now has
  `capability/missingmass.io/shopsystem/kb/<name>`, and `git grep formulated_as -- spec` is empty.
- **Suite** (kb-trial's venv, `PYTHONPATH=src`, which resolves `kb` to this clone's `src/`): **1603 passed**, 2564
  warnings, 33.6 s. The `PASSED` lines are identical by name to the before run (the diff is empty).
  `tests/slices.py` PLAN is now `.shop/records/archive/plans/2026-09-24-kb-slices.md`. conftest reads it through
  `slices.configure`, and the 33 `test_the_suite_is_green_between_slices` tests pass. `features count --by-tag` is
  byte-identical to before.
- **r15**: migrate run again on the migrated tree, which now has staged changes. It exits 1 with "migrate changed
  nothing", 280 lines of `could not start from a tree with an uncommitted change: <move>`, and the status and the
  staged diff have the same md5 before and after.

### Spot-checks

- **r13 numbering**: the 123 unnumbered entries are 0032-0154 in ledger order, and the 31 numbered keep 0001-0031.
  A script compared the expected file set with `spec/decisions/` and found them equal. For example
  `0032-serialization-yaml.md` is the ledger's first unnumbered entry.
- **References to them (r5)**: every `rests_on` now names `design-decision/missingmass.io/shopsystem/kb/<slug>`,
  formerly unnumbered entries included, and nothing is unresolved. Ids in prose are not rewritten, which is still
  outside r5 (paths, links and frontmatter ids): about 32 `(decision/<slug>)` in CLAUDE.md (5), capability Not yet
  lines (9), decision text (6) and src docstrings (12), and about 141 in test docstrings. The other `decision/`
  matches are kb's own data IRIs (`https://shop.example/kb/decision/…`), not references.
- **Superseded statuses (r2)**: 28 files are `status: superseded`, exactly the 28 distinct decisions the ledger's
  `supersedes` values name. A script checked this, with no missing and no extra.
- **Qualifiers to `by` (r17)**: 31 files have `supersedes`, each a single bare
  `design-decision/missingmass.io/shopsystem/kb/<slug>`, and the qualifier sits in `by` as the Implementation says:
  `by: "<source>; supersedes <id> <qualifier>"`. **Defect**: in 0100-batch-rpcs-prefixed the ledger names two
  decisions, `decision/sets-one-kind-at-a-time (its rpc names), decision/references-inside-a-set (its rpc name)`.
  Only the first was written to `supersedes`. The second is lost from `supersedes` and stays in `by` in its old
  form, `decision/references-inside-a-set`. Its status is still right (superseded), because status is computed
  from the ledger.
- **`by` names pre-move paths (defect against r5)**: **105 of 154** decision files have a `by` naming a file migrate
  moved in the same run: 73 `docs/superpowers/specs/…` or `…/requests/…`, and 32 `adrs/<nnnn>-….md` (e.g. 0001 has
  `by: "adrs/0001-yaml-1-2-git-canonical.md"`, and 0055 has `by: "the migration gate; adrs/0020-…md"`). model
  check reads `by` as free text, so it does not report them. r5 says each repository-relative path naming a moved
  file is rewritten, but migrate rewrites the old files' text and not the text it writes itself. The two prose
  `(adrs/0018)` in `src/kb/store.py` and `tests/test_the_published_contract.py` name no file and rightly stay.
- **adrs/ and requests/ moved, with ids and abouts (r9, r12, r14)**:
  `archive/requests/2026-10-10-requests-to-kb-portable-knowledge.md` has `initiative-archive/…`, and
  `decision-arguments/0001-yaml-1-2-git-canonical.md` has `decision-argument/…/0001-yaml-1-2-git-canonical` (the
  number kept, since an ADR is not a decision file). Both have `kind` and `about: bounded-context/missingmass.io/shopsystem/kb`.
  The ADR directory's `README.md` was given an id too, `decision-argument/…/README`, which is the one file problem.
  It describes the directory and is not an ADR.
- **@deprecated (r3)**: kb has no `@holding`, so this was not exercised, and `features/` is unchanged.
- **Decisions index (r16)**: `spec/decisions/index.md` is written (161 lines, 154 rows) and staged. Running
  `model decisions` afterwards rewrites it byte-identical.
- **Other**: `spec/index.md` has `id: bounded-context/missingmass.io/shopsystem/kb` (r4), 371 lines are numbered
  `[r1]`… (r10), and 23 `revisit_when` and 154 `date` are carried over. Decision headings are `# <slug>` rather than
  this repository's `# <nnnn>. <Title>`, which model check does not report.

### Q1: do other old records need ids?

**For kb, no.** After the move, the only tracked Markdown without an id are `README.md`, `CLAUDE.md` and the
generated `spec/decisions/index.md`, and none of them is a record. kb also has no `docs/` left. The question is the
reverse one: **should a directory's README that is moved with it get an id at all?** If it does, the stem
`README` is not a `<name>`.

### Candidate lines (EARS) for what remains

1. **When** `migrate run` moves a directory holding a `README.md`, `migrate` shall move it without giving it an id.
   *(1 file problem: `decision-arguments/README.md`, the only thing between kb and r6.)* The alternative, an id of
   the lowercased stem, is the person's call.
2. **When** `migrate run` writes a decision file whose `by` names a file it moves, `migrate` shall write the moved
   file's new path. *(105 of 154 decision files.)* This could also be r5 reworded: "…in the repository's tracked
   text files and in the files it writes."
3. **When** a ledger entry's `supersedes` names several decisions, `migrate` shall write each decision's id in
   `supersedes` as a list, and each qualifier in `by`. *(0100-batch-rpcs-prefixed: the second id was lost.)* Today
   `supersedes` is a scalar everywhere, as in this repository's own decision files, so model check would need to
   read a list.
4. (person's question) **When** `migrate run` changes a decision's id, `migrate` shall rewrite the old id where it
   stands in prose (`(decision/<slug>)`). *(About 32 outside tests and 141 in test docstrings. These are not
   unresolved, because model check does not read prose. The test docstrings are kb's code, so leaving them may be right.)*
5. (observation, no line) The ADR renames are R50-R79. Writing less frontmatter is not an option (r9 and r12 ask for
   it), so it stays a note: a commit of the migration keeps the renames, but a 2-line ADR would not.

### The session's judgment work left for kb

- **Lines to reword into EARS: 371** (v_e1). The rewording is small for most of them: 356 already open with
  When/If/While/Where, 0 have a `shall`, and none has a second sentence. Most need "the store holds…" turned into
  "kb shall …". About 15 open with no keyword (`A …`, `The …`, `kb …`) and need restructuring. Median line length is
  176 characters, the longest 555.
- **Scenarios to map: 361 scenarios to 371 lines** (v_s1 and v_s3). 15 of 21 features have exactly as many
  scenarios as their capability has lines, which suggests one scenario per line in order. The other 6 have 10 lines
  with no scenario between them: change-the-store 26/24, check-a-change 24/23, keep-the-history 21/19,
  make-several-changes-in-one-go 25/23, query-the-store 16/15, sign-a-change 3/1. Each mapping is still a reading,
  by 0049.
- Also the session's: 21 capabilities that serve no job (w_unserved_cap), and the prose ids of candidate 4 if the
  person wants them.

### Files (trial 2)

Clone `/home/vscode/.claude/jobs/3dae44af/tmp/kb-trial-2/` (migrated, uncommitted). Outputs in `…/tmp/kb-trial-2-out/`:
migrate.out (empty), status.txt, check.out, pytest.txt, rerun.out.
