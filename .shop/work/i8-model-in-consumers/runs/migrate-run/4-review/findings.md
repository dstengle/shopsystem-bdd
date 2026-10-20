# Review of migrate-run: DONE_WITH_CONCERNS

Verdict: the ten scenarios are bound and the commits stay inside the file set. Nothing under `features/` changed and no test was removed or weakened. But probes show `migrate run` loses data and gives wrong answers on realistic old-system input. Four findings are triaged fix now:
- the ledger split drops or merges entries, and the ledger is removed anyway;
- a ledger entry overwrites a decision file that is already there;
- a refused `git mv` leaves a half-done move;
- the r6 green depends on a fixture that no real old-system repository matches.

All findings are in the commits of work-item migrate-run.

## Commits reviewed
The branch `work/migrate-run` is gone. The commits are those between `2a56b96 work: migrate-run ready -> claimed` and `565e14e work: migrate-run claimed -> done` on the checked-out HEAD, less work run's own commits:
c8eb7d6 (r1), 7323d70 (r8), 3b56abe (r2/r11), 4118969 (r4), 1a794a5 (r10), b4ea412 (r9), 20d93ac (r5), 3ca23ed (r3), 588cfc2 (r7), bf3a278 (r6 and the bound list).

These are the same ten commits that the implementer's `result.json` lists. Files changed: `scripts/migrate` (new, 325 lines), `tests/scenarios/test_migration_tools.py` (new, 366 lines) and `tests/scripts/test_bound.py` (+1 list entry, 1 comment changed). All are in the work-item's fileset.

## Removed and weakened tests
None.
- I searched `git diff 2a56b96 bf3a278` for removed `def test`, `assert`, parametrize cases, `skip` and `xfail`.
- The only change to an existing test file is `tests/scripts/test_bound.py`. It gains `features/migration-tools.feature` in `BOUND_BY_PYTEST_BDD` and loses a "joins when i8 adds it" comment. No assertion changed.
- The plan lists no broken tests, and none was broken.

## Allowances
The report says "none", and that holds: every test in the migration module is new.

The report also notes a fixture choice: the r8 fixture's plan and design note already carry ids. This is not an allowance. It is recorded as finding M2.

## Cannot verify
- The suite record "557 passed, 0 failed at bf3a278". I did not run the full suite, because work run did.
- The red runs the report claims for each requirement (r1, r8, ... r6). The commits show green only.

## Findings

### F1. Important, fix now: the ledger split loses or merges entries, and the ledger is removed anyway
`scripts/migrate:63-85` (`ledger_entries`) and `:213-219` (`plan_ledger`).
- **What happens:** a heading that does not match `## decision/<nnnn>-<slug>` is read as more lines of the entry before it. Its `date:` and `source:` overwrite that entry's fields. The heading's own decision is never written. The ledger is then removed unconditionally (`plan.removes.append(LEDGER)`).
  - With an unnumbered entry (`## decision/a`, the form `.shop/records/archive/design-notes/2026-09-29-capability-spec-design.md:80` documents), migrate exits 0 and deletes the ledger with no decision file written (probe p9).
  - With `0001-a` followed by `decision/b`, `0001-a.md` gets b's date and `by: bob`, and b is gone (probe p3).
  - Everything outside the first paragraph is dropped: a preamble, a second paragraph, `supersedes:` and `revisit_when:`.
  - The documented form puts `date:` straight after the line with no blank line. Then `date: … source: …` becomes part of the summary and `date`/`by` come out empty (probe p8).
- **Why it matters:** r11 says to remove `spec/decisions.md` only "when migrate run has replaced every entry". design-decision/migration-in-one-pass says migrate "refuses rather than guesses". As built, decisions are lost silently and exit 0 reports success.
- **Fix:**
  - Treat any `## ` heading as an entry boundary.
  - Refuse, under r7, any entry that is not in the `<nnnn>-<slug>` form, and any ledger text outside the entries.
  - End the first paragraph at a `key:` line.
  - Remove the ledger only when every entry is planned.

### F2. Important, fix now: a ledger entry overwrites a decision file already there
`scripts/migrate:217`, `:122` and `:291-293`.
- **What happens:** the new file `spec/decisions/<nnnn>-<slug>.md` is put in `plan.texts` without a check that the path is free.
  - If `decisions/0007-a.md` is moved to the same path, `plan_ids` takes the ledger text in place of the moved file. The moved file's content is lost (probe p4).
  - If `spec/decisions/0007-a.md` is already tracked, it is overwritten (probe p4b).
- **Why it matters:** data is lost, with exit 0. The capability's Implementation note says a move onto a file that exists is a change migrate cannot make, and r7 applies. The report names this as unchecked.
- **Fix:** in `check_moves`, treat each new file as a destination too. Refuse when its path is tracked, is a move's destination, or is another new file's path.

### F3. Important, fix now: a refused `git mv` leaves a half-done move and a traceback
`scripts/migrate:266-283`.
- **What happens:** `check_moves` checks destinations against tracked files only. An untracked file at a destination passes the check. `git mv` then fails partway through `write`. The earlier moves are already staged, and the user gets a `CalledProcessError` traceback (probe p5: `R work/i1/w1.md -> .shop/work/i1/w1.md`, rc 1, traceback for w2).
- **Why it matters:** r7 says migrate shall name each change it cannot make "and change no file". Here a partial change is left behind.
- **Fix:** check `(root / new).exists()` (and that `new` is not under an existing file) for every move and new text before any write.

### F4. Important, fix now: r6 goes green only because the fixture's records carry `about:`, which old-system records do not have
`tests/scenarios/test_migration_tools.py:336-340` and `scripts/migrate:94-128`.
- **What happens:** migrate gives moved records `id` and `kind` but no `about`. On an old-system repository with a plain plan and a plain test log, `model check` afterwards reports `v10b a record is about nothing (2)` and rc 1 (probe p7).
  - The r6 fixture works around this by writing `about: bounded-context/<path>` into the old records.
  - The plan's fixture list (D10) does not include `about`.
- **Why it matters:** r6 says that after migrate, `model check` reports no violation on "a repository on the old system". design-decision/references-are-ids requires `id`, `kind` and `about` on every record. The behaviour contradicts r6 on any real repository with records. The report raises this as an open question.
- **Fix, for the person to decide:** either migrate writes `about: bounded-context/<path>` (the same transcription r4 already does), or r6 and its scenario are narrowed.

### F5. Important, fix now: a summary with ` #`, a leading `[` or a quote is misread
`scripts/migrate:88-91`.
- **What happens:** `summary: %s` is written unquoted. model's frontmatter reader strips ` #…` as a comment and reads `[...]` as a list. With the paragraph `[Scripts] read: one #1 form.`, the parsed summary is `'[Scripts] read: one'` (probe p6).
- **Why it matters:** it is a wrong answer for r2 ("whose summary … are the entry's first paragraph") on ordinary prose.
- **Fix:** write `summary` and `by` double-quoted with `"` and `\` escaped, as the repository's own decision files do.

### F6. Important, observation: a relative link from a moved file to a file that stays is left broken
`scripts/migrate:228-236`.
- **What happens:** the code rewrites a link only when its target moved. `work/i1/w1.md` linking `../../spec/index.md` keeps that link once it is `.shop/work/i1/w1.md`, where the link resolves to `.shop/spec/index.md`, which does not exist (probe p2).
- **Why it matters:** the Purpose ("makes the mechanical changes that take a repository … to the final layout") is not met, because links break. r5 itself names only references *to* what moved, so this is hardening beyond the line.
- **Fix:** rewrite every relative link in a moved file against its new directory.

### F7. Minor, observation: a binary file under a moved directory crashes the run
`scripts/migrate:122`.
- **What happens:** `plan_ids` reads every moved file as text before it checks whether the file needs an id. A `records/img/a.png` therefore raises `UnicodeDecodeError` with a traceback and rc 1. No file is changed (probe p1).
- **Why it matters:** an image under `records/` cannot be migrated, and the error names nothing.
- **Fix:** read the file only when `record_kind` or the decision-file branch applies, or skip files that do not decode.

### M1. Minor, drop: `scripts/migrate` is mode 100644
`git ls-files -s`: `scripts/model` and `scripts/features` are 100755. The report says so. Fix: `chmod +x` in the next commit.

### M2. Minor, observation: r8 and r9 pull against each other on plain files
`tests/scenarios/test_migration_tools.py:95-97`.
- **What happens:** the r8 scenario says a moved plan "has the content … had". r9 gives a plain plan an id, which changes its content. The fixture avoids the conflict by putting ids in place in advance.
- **Fix:** this is for the formulator. Reword the r8 Then, or keep the fixture as it is.

### M3. Minor, drop: plan D7's directory-prefix rewriting is not built
`scripts/migrate:239-240` matches whole moved file paths only. Plan D7 said "or to a directory prefix of it". The report mentions it as prose of a directory not being rewritten. No scenario needs it.

### M4. Minor, drop: both new files are over 300 lines
They are 325 and 366 lines, against the 300-line limit that initiative i15 proposes. i15 is not yet binding.

## Checks run
- `git log --all --grep="^work: migrate-run ready -> claimed$"` found 2a56b96. `git log` and `git diff --stat` were run from 2a56b96 to bf3a278 and to 565e14e.
- `git diff 2a56b96 bf3a278 -- features/`: empty.
- `tools check --base 2a56b96`:
  - **ruff:** 13 findings. Twelve are UP031 (percent format) and one is PLW1510, all in the new test module. One more PLW1510, at `tests/scripts/test_bound.py:26`, is in a line that existed before this work-item. `scripts/migrate` has no `.py` extension, so it is not linted.
  - **vulture:** clean.
  - **import-linter:** the project states no import contracts.
- Probes, in `.shop/scratch/migrate-run-4-review/test_probe.py` and `test_probe2.py`, run with `python3 -m pytest -s`:
  - p1: binary file
  - p2: link from a moved file
  - p3 and p9: ledger entries not in `<nnnn>-<slug>` form, and text outside the entries
  - p4 and p4b: a new decision file onto an existing one
  - p5: an untracked file at a destination
  - p6: summary quoting
  - p7: model check after a plain-records migration
  - p8: fields with no blank line before them

  Each one's output is quoted in its finding.
- `git status --short` was clean at the end.
