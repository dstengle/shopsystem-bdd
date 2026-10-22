# Review: migrate-kb-2

**Verdict: DONE.** No Critical finding and nothing triaged fix now. One Important observation: `supersedes_of` now
splits a qualifier that itself names a decision. That input is a regression on r17 but no scenario names it. There
are also two Minor items.

## Commits reviewed

The branch `work/migrate-kb-2` is gone. The commits are those between `58fa5e6 work: migrate-kb-2 ready -> claimed`
and `e5a1159 work: migrate-kb-2 claimed -> done` on the checked-out HEAD:

- f897853 migrate: the status step reads a backticked status, and two files' status in one line
- 38c6496 migrate: steps for the moved README.md scenario
- 225b787 migrate run: a decision file's by and body go through the reference rewrite
- c023c75 migrate run: a supersedes naming two decisions keeps and supersedes both

These are exactly the four in the implementer's result.json. The files changed are the four in the report's
Budget, and all four are in the work-item's fileset. Line counts are 122, 132, 226 and 224, all under 300. Nothing
under `features/` changed (`git diff --stat 58fa5e6 e5a1159 -- features/` is empty).

## Removed and weakened tests

**None.** What I searched: every `-` line of `git diff 58fa5e6 c023c75` under `tests/`.

There is exactly one: the decorator `@then(parsers.parse("spec/decisions/{name}.md's status is {status}"))` in
`tests/scenarios/migration_ledger_steps.py`. It is replaced by a regex form at line 202:
`spec/decisions/(?P<name>[\w-]+)\.md's status is `?(?P<status>\w+)`?$`.

- **Before:** it compared the status field with the feature's text, backticks included. So it could not pass on
  feature lines 70 and 186, for any code.
- **After:** it compares the same field with the same word, backticks stripped. The assert line is unchanged.
- **Coverage kept:** all four feature lines that use it (69, 70, 79 via the new two-file step, 186) match the new
  patterns.

No test function was deleted, no parametrize case was dropped, and no skip or xfail was added. The `its by is`
step only gained a second decorator, `spec/decisions/0007-a.md's by is "{by}"`, and its assert is unchanged.

## Allowances

- **The status step in `migration_ledger_steps.py`, a `setup` (step repair) row under plan decision 4: holds.**
  The diff changes no `assert` and no parametrize case. The expected value still comes from the unchanged feature
  text; only its decoration is stripped. The plan names this repair as decision 4.

## Cannot verify

- The report's red and green counts: 6 failed and 37 passed at the start, 43 passed at the end, and "Suite: 596
  passed, 6 failed at 58fa5e6". I did not run the suite, as the brief says not to.
- Whether the kb ledger, which was the trial's source, has a `supersedes` whose qualifier names another decision,
  or whose targets are separated by commas or in a `[...]` list. Whether Finding 1 is reached in practice depends
  on this.
- Whether `model check` (r6) resolves each id of a `supersedes: [a, b]` list. The plan leaves this open, and no r6
  row has two targets.

## Findings

### 1. A qualifier that names a decision is split into a bogus target (Important, triage: observation)

- **Work-item:** migrate-kb-2, commit c023c75. Location: `scripts/migrate_ledger.py:73-83` (`supersedes_of`).
- **What is wrong:** any whitespace-delimited word matching `decision/\S+` now starts a new target, even inside a
  qualifier.
  - `supersedes: decision/0003-b (in part; see decision/0004-c)` gives the targets `[('…/b', '(in part; see'),
    ('decision/0004-c)', None)]`.
  - So `supersedes` is written as `[design-decision/…/b, decision/0004-c)]`.
  - The qualifier's tail is lost from `by`.
  - 0004-c is not marked superseded, because the key `decision/0004-c)` is not in `plan.renamed`.
  - Before this commit, the same input gave target b with the whole qualifier, which is r17's answer. So this is a
    regression on that input.
- **Related inputs:**
  - Leading text is dropped silently. `partly decision/0003-b` gives b with no qualifier.
  - A list form loses targets:
    - `[decision/0003-b, decision/0004-c]` gives only `decision/0004-c]`, not renamed.
    - `decision/0003-b, decision/0004-c` gives `decision/0003-b,`, not renamed and not marked superseded.
  - These were also wrong before the commit, though differently. The plan lists the separators as open cases.
- **Why it matters:** r2 says the supersedes is "the entry's" and r17 says the qualifier goes to `by`, and on these
  inputs the run gives a wrong answer with exit 0. The `model check` of r6 would probably flag the bogus id
  afterwards, which I did not verify. No scenario or Behaviour line names a qualifier that contains a reference, so
  this is triaged as hardening.
- **Fix:**
  - Treat a reference as a new target only at the start of the value, or right after `and` or a `,` separator, and
    strip trailing `,`, `]` and `)` from it before the `renamed` lookup.
  - Keep everything else, including references inside parentheses, as the current target's qualifier.
  - Or refuse (r7) a value it cannot split cleanly.
- **Reproduction:**
  - Probe file: `.shop/scratch/migrate-kb-2-4-review/probe_supersedes.py`.
  - Command: `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/migrate-kb-2-4-review/probe_supersedes.py`.
  - It printed:
    ```
    'decision/0003-b (in part; see decision/0004-c)' -> [('NEW/b', '(in part; see'), ('decision/0004-c)', None)]
    'partly decision/0003-b' -> [('NEW/b', None)]
    '[decision/0003-b, decision/0004-c]' -> [('decision/0004-c]', None)]
    'decision/0003-b, decision/0004-c' -> [('decision/0003-b,', None), ('NEW/c', None)]
    'decision/0003-b  (two  spaces)' -> [('NEW/b', '(two spaces)')]
    ```
  - The old `supersedes_of` was read with `git show 58fa5e6:scripts/migrate_ledger.py`. It split once on whitespace
    and kept the rest as the qualifier.

### 2. The qualifier's whitespace is normalised (Minor, triage: drop)

- **Location:** `scripts/migrate_ledger.py:83`.
- **What is wrong:** `" ".join(rest)` collapses runs of whitespace inside a qualifier, where the old code kept it
  "as written". The same probe shows `(two  spaces)` becoming `(two spaces)`.
- **Why it matters:** this is cosmetic, and no line pins it.

### 3. ruff reports house-style findings on the changed files (Minor, triage: drop)

- **What `tools check` reports:** 41 ruff findings, almost all UP031 (percent format). That is the files' existing
  style, which the new lines follow. It also reports I001 at `tests/scenarios/migration_ledger_steps.py:3` and
  RUF100 at `tests/scenarios/test_migration_tools.py:10,12`; these lines are outside the diff and predate it.
- **Fix:** none needed for this work-item.

## Checks run

- **`python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 58fa5e6…`:**
  - ruff: 41 findings, as in Finding 3, none a defect.
  - vulture: clean.
  - import-linter: "the project states no import contracts".
- **Commits against result.json** (`git log --stat 58fa5e6..e5a1159`): they match.
- **`git diff --stat 58fa5e6 e5a1159 -- features/`:** empty.
- **Line counts** (`wc -l` on the four changed files): 122, 132, 226 and 224, all under 300.
- **Step patterns:** I grepped `features/migration-tools.feature` for `status is`, `by is`, `whose source is`, the
  README lines and `supersedes`. Every feature line touched by the changed steps matches a step.
- **Risk: rewriting a created decision after `quoted()` could break `by`'s quoting.**
  - What I checked: I read `rewrite_text` (`scripts/migrate_spec.py:91-114`).
  - What I found: it replaces a moved path with its new path, and an old id with its new id only in the frontmatter.
    Neither adds a quote character. Its look-behind `(?<![\w./-])` stops `decisions/…` from being matched inside
    `spec/decisions/…`.
  - Verdict: the risk does not hold.
- **Risk: the created-file loop touches files other than decision files.**
  - What I checked: I grepped `scripts/` for `plan.created[`.
  - What I found: only `migrate_ledger.py:119` writes it, for decision files.
- **Risk: a renamed key like `decision/b` matches inside a new id.**
  - What I checked: I read the frontmatter id rewrite.
  - What I found: the look-behind and look-ahead stop it, and the new id `design-decision/<ctx>/b` holds no old key.
- **Probe of `supersedes_of` on nine values:** see Finding 1.
