# Review of w96: upgrade hardening from the reviews of i21

**Verdict: DONE_WITH_CONCERNS.** The fixes are correct and tested, and nothing is removed or weakened. One Important
finding, triaged fix now: the F7 behaviour of `migrate status` and of the SessionStart hook on a version file that
holds no version is not in any Behaviour line (r18, r22–r24 and r28 do not cover it). The person's answer of
2026-10-23 settles what it is, but that answer has not been written as a requirement.

## Commits reviewed

Branch `work/w96` is gone. Taken from HEAD, between `bd55621 work: w96 ready -> claimed` and
`7a1e06f work: w96 claimed -> done`:

- `2bf920a` migrate upgrade hardening: version file with no version, missing context id, ordering, narrower
  rewrite, clearer refusals. It touches scripts/migrate_upgrade.py, scripts/migrate_upgrade_ids.py,
  tests/scripts/test_migrate_upgrade.py (new), tests/scripts/test_migrate_upgrade_ids.py and
  tests/scripts/test_migrate_write.py.

This is the one commit the implementer's result.json lists. Every file is in the work-item's fileset. Nothing under
`features/` or `spec/` changed (`git diff --stat bd55621 7a1e06f -- features/ spec/` is empty).

## Removed and weakened tests

None. I read the full test diff, looking for deleted `def test_`, dropped parametrize or subTest cases, `assert*`
lines removed or loosened, `skip` or `xfail` added, and tests rewritten. Every hunk in test_migrate_upgrade_ids.py
and test_migrate_write.py only adds lines: the `atexit`/`shutil` imports, the
`atexit.register(shutil.rmtree, root, True)` line and the new `UpgradeHardening` class. test_migrate_upgrade.py is new.

## Allowances

The report's `## Tests changed under an allowance` says "none". That holds. The F12 edits add a cleanup line to each
`repository` helper and change no assertion, expected value or case.

## Cannot verify

- The report's "12 failed, 15 passed before the code". I did not check out the base to rerun it. I read the new
  tests against the old code instead: the old code crashes on F7 and F8 (ValueError in `number`, AttributeError or
  FileNotFoundError in `context_path`), says "reference" (N4), rewrites `item` in `# item`, and sorts by number
  alone (F9). Each would fail the matching new test.
- The report's full-suite count (659 passed). `work run` ran the suite before the merge.

## Findings

### 1. Important, fix now: F7 behaviour of `status` and the hook is in no Behaviour line
- Where: scripts/migrate_upgrade.py:59-63 (`status` refuses: one stderr line, exit 1) and :75-77 (`session_text`
  returns ".shop/plugin-version holds X, which is no version: tell the person.").
- What is wrong: this is new observable behaviour, an output and an exit status. No line of migration-tools asks
  for it:
  - r18 says only that `status` prints the versions and pending steps and exits successfully.
  - r22, r23, r24 and r28 cover a session that is behind, ahead, level, or without `.shop/`. None covers a version
    file that holds no version.
  - The work-item's "refuse, saying why" and the person's answer (Reading A) decide what the behaviour is. They are
    not a Behaviour line.
  - The `upgrade` refusal (:118-121) and the F8 refusal (migrate_upgrade_ids.py:103-105) are covered by r7 ("cannot
    make every change … exit with an error, naming …"). They are not part of this finding.
- Why it matters: behaviour reaches code only through a line. Without one, no scenario holds the hook's exit-0 line
  or the status refusal, and a later change could drop either with no requirement broken.
- Fix: write the lines first, through integrating-a-proposal. For example:
  - an r-line: "If `.shop/plugin-version` holds no version, then the SessionStart hook shall tell the session that
    it holds no version, naming what it holds, and to tell the person."
  - its `status` counterpart, a refusal that names the file and what it holds.
  - their scenarios.
  The code can stay as it is.

### 2. Minor, drop: ruff style on the touched files
- Where: `tools check` lists 43 ruff findings in the five touched files. Examples are UP031 percent-format at
  migrate_upgrade.py:46 (new) and RUF012 at test_migrate_upgrade.py:46 (new).
- Almost all of them are on lines that were already there. The rest follow the repository's own percent-format
  convention. Fixing them is not cheap across the files and has no behavioural value.

### 3. Minor, drop: a work-item named like a requirement qualifier
- Where: migrate_upgrade_ids.py:51. The lookbehind `(?<![\w/-])` lets a token start right after `#`. So in
  `for: cap#r26`, the `r26` part would be rewritten if a work-item were named `r26`.
- No work-item has such a name, and old names were slugs. I did not probe it.

## Risks checked outside the diff
- Is a repository without `.shop/plugin-version` still unaffected? `no_version` returns None when the file is not
  there (:38-39), so r24 and r28 behave as before.
- The comment cut in `names_in` is `\s#`, so `item#r26` is not treated as a comment. The pattern's lookahead
  `(?![\w#-])` then keeps `item` from matching. The new N5 test asserts this, and it passes.
- `listing` now carries the field's name through block-list items. The N4 test asserts that each field is named once.

## Tool results
- `tools check --base bd55621`: ruff gave 43 findings (finding 2). vulture is clean. import-linter: the project
  states no import contracts.
- `tools size --limit 300`: printed nothing. No file is over the limit.

## Commands run
- `git log --format='%H %s' -1 --grep="^work: w96 ready -> claimed$"` (and the same for `claimed -> done`),
  `git log --format='%h %s' -8`
- `git show --stat 2bf920a`, `git show 2bf920a -- scripts/`, `git show 2bf920a -- tests/`
- `git diff --stat bd55621… 7a1e06f… -- features/ spec/`
- `grep -nE "r7|r18|r2[0-9]|rests_on|Purpose" spec/capabilities/migration-tools.md`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base bd556212e269682c0da23cb68b9d2e8b6afcb0c2`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `python3 -m pytest -q -n 0 tests/scripts/test_migrate_upgrade.py tests/scripts/test_migrate_upgrade_ids.py tests/scripts/test_migrate_write.py`:
  17 passed, 10 subtests passed
