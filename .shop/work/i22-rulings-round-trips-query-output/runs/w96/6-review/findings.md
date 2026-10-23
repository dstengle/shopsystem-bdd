# Review of w96 (round 6): upgrade hardening from the reviews of i21

**Verdict: DONE.** No finding is Critical and none is fix now. The one fix-now finding of the stage-5 review was that
the F7 behaviour (`migrate status`/`upgrade` refusing, the hook's exit-0 line on a version file that holds no version)
is in no Behaviour line. That is now settled: the person answered Reading A, and migration-tools r30 and r31 were
written with scenarios (commit db3ac66). w99 binds them. The code of w96 does what r30 and r31 ask. One Minor
observation remains: the quoting of what the file holds differs from the scenarios' text. It is for w99.

## Commits reviewed

The branch `work/w96` is gone. The commits are taken from HEAD, between `bd55621 work: w96 ready -> claimed` and
`7a1e06f work: w96 claimed -> done` (`git log --ancestry-path`):

- `2bf920a` migrate upgrade hardening: version file with no version, missing context id, ordering, narrower
  rewrite, clearer refusals.
  - It touches 5 files: scripts/migrate_upgrade.py, scripts/migrate_upgrade_ids.py,
    tests/scripts/test_migrate_upgrade.py (new), tests/scripts/test_migrate_upgrade_ids.py and
    tests/scripts/test_migrate_write.py.
  - All 5 are in the fileset.

This is the one commit the implementer's result.json lists. No difference. Nothing under `features/` or `spec/`
changed in the commits (`git diff --stat bd55621 7a1e06f -- features/ spec/` is empty). No later commit touched the
five files (`git diff --stat 2bf920a HEAD -- <files>` is empty).

## Removed and weakened tests

None. I read the whole test diff, looking for:

- a deleted `def test_`;
- a parametrize or subTest case dropped;
- an `assert*` removed or loosened;
- a skip or xfail added;
- a test renamed or rewritten.

Every hunk in test_migrate_upgrade_ids.py and test_migrate_write.py only adds lines: imports, one
`atexit.register(shutil.rmtree, root, True)` line in each `repository` helper, and the new `UpgradeHardening` class.
test_migrate_upgrade.py is new. The plan's "Tests the decisions break" is "none", and that agrees.

## Allowances

The report's `## Tests changed under an allowance` says "none". That holds: the F12 edits add a cleanup line and
change no assertion, expected value or case.

## Cannot verify

- The report says "12 failed, 15 passed before the code". I did not rerun it on the base. I read the new tests
  against the old code instead. The old code would fail each of them:
  - F7: a ValueError in `number`;
  - F8: an AttributeError or FileNotFoundError in `context_path`;
  - N4: the message says "reference" and lines repeat;
  - N5: the old pattern rewrites the `item` of `# item`;
  - F9: the sort is by number alone.
- The report's full-suite count (659 passed). `work run` ran the suite.

## Findings

### 1. Minor, observation (for w99): the hook and refusal quote what the file holds with `'…'`, but r30/r31's scenarios say `"…"`
- **Work-item:** w96 (commit 2bf920a).
- **Where:** scripts/migrate_upgrade.py:42. `no_version` returns `repr(held)`, so `next` is printed as `'next'`.
  The scenarios at features/migration-tools.feature:541 and :554 expect `.shop/plugin-version holds "next", which is
  no version`.
- **Reproduction:** read only, I did not run it. The code builds the message as
  `"%s holds %s, which is no version" % (VERSION_FILE, repr("next"))`, which gives
  `.shop/plugin-version holds 'next', which is no version`.
- **Why it matters:** if the steps of the r30/r31 scenarios match the quoted text exactly, they will be red.
- **Fix:** none in w96. w99 binds r30/r31 and "changes the code only where a scenario shows it differs". This is
  likely such a place.
- r30 and r31 themselves are met:
  - status and upgrade exit 1, name the file and what it holds, and change nothing;
  - the hook exits 0 and tells the session to tell the person, naming what the file holds.

### 2. Minor, drop: ruff style on the touched files
- **Where:** `tools check` lists ruff findings in the five touched files. Most are UP031 (percent format), the
  repository's own convention, on lines that were already there. A few are on new lines, for example RUF012 at
  tests/scripts/test_migrate_upgrade.py:46.
- **Why drop:** they have no behavioural value, and fixing them is not cheap across the files.

### 3. Minor, drop: a work-item named like a requirement qualifier
- **Where:** scripts/migrate_upgrade_ids.py:51. The lookbehind `(?<![\w/-])` allows a token right after `#`.
- **Effect:** in `for: cap#r26`, `r26` would be rewritten if a work-item were named `r26`. No work-item has such a
  name (the old names were slugs).

## Risks checked outside the diff
- **Was the stage-5 fix-now finding (code with no line) still open?** I checked that r30 and r31 are now in
  spec/capabilities/migration-tools.md, with @r30 and @r31 scenarios at features/migration-tools.feature:535-554.
  They ask for exactly the F7 behaviour, so the finding is resolved. The upgrade refusal and the F8 refusal rest on
  r7, and the deduplication of `refused` rests on r7's "naming each change".
- **Does a repository without `.shop/plugin-version` behave as before?** Yes. `no_version` returns None when the
  file is absent, so r19, r24 and r28 are unchanged.

## Tool results
- `tools check --base bd55621`:
  - ruff: 143 findings across the repository, the touched files' ones under finding 2;
  - vulture: clean;
  - import-linter: the project states no import contracts.
- `tools size --limit 300`: printed nothing. No file is over the limit.

## Commands run
- `git log --format='%H %s' -1 --grep="^work: w96 ready -> claimed$"` and the same for `claimed -> done`
- `git log --oneline -15`
- `git branch -a --list work/w96`
- `git log --ancestry-path bd55621..7a1e06f`
- `git show --stat 2bf920a`
- `git show 2bf920a`
- `git diff --stat bd55621 7a1e06f -- features/ spec/`
- `git diff --stat 2bf920a HEAD -- <the five files>`
- `grep -rn -B2 -A12 "holds no version" features/`
- `cat .shop/work/i22-rulings-round-trips-query-output/w99.md`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base bd556212e269682c0da23cb68b9d2e8b6afcb0c2`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `python3 -m pytest -q -n 0 tests/scripts/test_migrate_upgrade.py tests/scripts/test_migrate_upgrade_ids.py tests/scripts/test_migrate_write.py`:
  17 passed, 10 subtests passed
