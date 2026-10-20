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
