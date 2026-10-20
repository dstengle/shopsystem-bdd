# Review of migrate-kb

**Verdict: DONE_WITH_CONCERNS.** One Important finding is triaged fix now. References to an unnumbered ledger entry
(`decision/<slug>`) are not rewritten, and a `supersedes` naming one does not resolve. So on kb (169 such references,
per the trial log) `model check` still reports unresolved references (r6, r5), and a superseded unnumbered entry keeps
`status: accepted` (r2).

## Commits reviewed
I found the `work: migrate-kb ready -> claimed` commit at 5dca7d8. The branch `work/migrate-kb` is gone, so I took the
commits from 5dca7d8 to `work: migrate-kb claimed -> done` (13d870a) on HEAD, leaving out work run's own commit:
- 78af164 migrate_ledger: superseded status, unnumbered entries, qualifier out of supersedes (r2, r13, r17)
- 8019602 ledger steps for r11, r13, r17 and the r7 numbering rows
- 63109eb requests/adrs moves, ids and abouts, dirty-tree refusal, staging and decisions index, short capability id,
  formulated_as removed

These are the three commits the implementer's result.json lists. No commit touches `features/` or `spec/`.

## Removed and weakened tests
I searched the diff of `tests/` for removed `def`/step decorators, removed or changed `assert` lines, removed
parametrize cases and added skip/xfail. No skip or xfail was added, and no test function in `tests/scripts/` was removed.
- `migration_spec_steps.py` r6 Then (was :150): before, it asserted `returncode == 0` and `violations == []` as well
  as `unresolved == []` and `problems == []`. Now it asserts only the last two. **This is weakened, but the plan lists
  it** (section 4, D10), and the feature's wording (line 173) names only unresolved references and file problems.
- `test_migration_tools.py` "git status shows each of the two as renamed" (`len(R) == 2`): removed. The feature
  commit 95851ff, made before the claim, changed the r8 scenario to three directories, and that scenario now uses the
  r1 step "each of the three as renamed" (`len(R) == 3`). The new "shows it as renamed" step (`== 1`) serves r14. The
  report lists this change. It is not weakened: the scenario it served now asserts more.
- `test_migration_tools.py` "plans and specs are gone": replaced by a three-directory form. It is stronger.
- `migration_spec_steps.py` "{first}, {second} and {third} are each about {ref}": generalized to any number of files.
  The assertion is the same, applied to the five files the feature now names.
- `migration_ledger_steps.py` one-entry r7 Given: replaced by the "has, in order, the entries" form. This is
  setup only, and the plan lists it.
- The r11 title Given (wording), the "nothing but the entry" Given (state), and the r9/r12/r6-row-1 Givens (bodies,
  added records) are setup, and the plan lists them.

## Allowances
The report has one row: "setup/wording only" for the Givens and Thens it names. It holds for the Givens and for the
replaced "gone" and "renamed" Thens: none of them drops an expected value from a scenario that still runs. It does not
hold for the r6 Then, which loses two assertions. That Then is listed in the plan's "Tests the decisions break" (D10),
though, so this is not a finding.

## Cannot verify
- The report's suite record ("591 passed, 0 failed, 1 skipped at 63109eb"). work run ran the suite; I did not.
- That `migrate run` on the real kb repository now leaves `model check` with no unresolved reference. The probe below
  shows it does not, for unnumbered references.

## Findings

### 1. Important · fix now: references to an unnumbered ledger entry are not rewritten
- **Where:** `scripts/migrate_ledger.py:101-102` (`plan_ledger`); work-item migrate-kb, commit 78af164.
- **What is wrong:** the renamed map gets only `decision/<assigned nnnn>-<slug>`. It never gets the form the
  repository actually uses for an unnumbered entry, `decision/<slug>`. As a result:
  - a `rests_on`, a frontmatter or a `supersedes` naming `decision/b` is left as it is, and is unresolved;
  - `supersedes_of` falls back to the raw `decision/b`, so the superseded entry's status stays `accepted`.
- **Why it matters:** r6 (model check reports no unresolved reference), r5 (an id it changes is rewritten wherever
  it is named), r2 (status superseded when another entry supersedes it). Plan D3 says "it goes into the renamed map
  like any other entry". kb has 123 unnumbered entries and 169 `decision/<slug>` references (trial log :91, :104).
- **Reproduction:** probe `.shop/scratch/migrate-kb-4-review/test_probe.py`. Its ledger has `## decision/0001-a`,
  `## decision/b`, and `## decision/c` with `supersedes: decision/b (for artifacts)`; its capability has
  `rests_on: [decision/b]`. I ran `python3 -m pytest -q -s -p no:cacheprovider .shop/scratch/migrate-kb-4-review/test_probe.py`.
  It returned:
  - migrate exited 0;
  - 0002-b.md has `status: accepted`;
  - 0003-c.md has `supersedes: decision/b` and `by: "x; supersedes decision/b (for artifacts)"`;
  - the capability still has `rests_on: [decision/b]`;
  - `model check` unresolved: `['spec/capabilities/thing.md: decision/b is not a design-decision in this repository',
    'spec/decisions/0003-c.md: decision/b is not a design-decision in this repository']`.
- **Fix:** in `plan_ledger`, also set `plan.renamed["decision/%s" % slug]` for an entry whose heading had no number.
  `ledger_entries` must keep that fact; the original `heading` is already returned. Add a scenario row, or a
  `tests/scripts` case, where an unnumbered entry is both referenced and superseded.

### 2. Minor · observation: plan decision D8 not implemented
- **Where:** `scripts/migrate_spec.py:39`.
- **What is wrong:** plan section 2 and D8 say a malformed `retired` entry becomes a named refusal. It still raises
  `ValueError` with a traceback (research notes p25: `retired: [rx]` gives rc 1 and a traceback; nothing changed).
  The report states this openly. No scenario covers it, and kb has no `retired` (trial log :28).
- **Fix:** catch the parse error, append a failure naming the capability and the entry, and refuse.

### 3. Minor · drop: new lint finding
- **Where:** `tests/scenarios/migration_ledger_steps.py:3`.
- **What is wrong:** ruff I001 (import block unsorted) after `import re` was added. The other ruff findings are on
  lines these commits did not change, or are the repository's `%`-format style (UP031).

## Checks run
- `git log --format=%H -1 --grep="^work: migrate-kb ready -> claimed$"` gave 5dca7d8. I also ran `git log --stat`
  over 5dca7d8..13d870a and `git diff 5dca7d8 63109eb -- scripts tests`.
- `features/` and `spec/` changes in these commits: none.
- Risk checked: unnumbered-entry references in kb. I grepped the kb trial test log (169 `decision/<slug>`
  references) and ran the probe above. Finding 1 confirmed it.
- Risk checked: the old "each of the two renamed" step removed. I grepped `features/migration-tools.feature` for
  the Then lines in use (:14, :211, :220).
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 5dca7d8`:
  - **ruff:** 57 findings, mostly UP031 (repository style). The only one on a changed line is I001 at
    migration_ledger_steps.py:3.
  - **vulture:** clean.
  - **import-linter:** the project states no import contracts.
- `wc -l`: the largest changed file is 209 lines (migration_spec_steps.py). Every file is under 300.
