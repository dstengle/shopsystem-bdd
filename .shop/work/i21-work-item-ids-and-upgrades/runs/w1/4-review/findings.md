# Review of w1 (migration-tools#r26: references from another initiative and `for:` follow the rename)

**Verdict: DONE.** Nothing is Critical and nothing is triaged fix now. The commit does what the plan says for Decisions 1, 2, 3 and 5. Decision 4, the move check, works when probed but has no unit test, though the plan said it would get one. There are four Minor findings: two observations and two drops.

## Commits reviewed

The branch `work/w1` no longer exists, so the commits come from HEAD, between `ec2bbb9 work: w1 ready -> claimed` and `f3b75af work: w1 claimed -> done`:

- `36ad963 migrate upgrade: references from another initiative and for: follow the rename`. It changes scripts/migrate_upgrade.py, scripts/migrate_upgrade_ids.py, tests/scenarios/migration_upgrade_steps.py and tests/scripts/test_migrate_upgrade_ids.py.
- `f3b75af` is `work run`'s own commit: log, report, the status change. It touches no code.

This matches the commit list in the implementer's result.json (`36ad963`). Every changed file is in the work-item's `fileset`, and migrate_write.py was left alone as the plan allowed. Nothing under `features/` changed.

## Removed and weakened tests

None. I read the full diff of both test files, looking for deleted test functions, assertions that were removed or loosened, dropped parametrize cases, and added skip/xfail.

- The diff adds tests in tests/scripts/test_migrate_upgrade_ids.py and removes none. `test_a_blocked_by_written_as_a_block_list_follows_the_rename` is unchanged.
- In tests/scenarios/migration_upgrade_steps.py, the literal Given `work-items .shop/work/i10/a.md, .shop/work/i2/b.md and .shop/work/i2/a.md` became a parsed Given over a list of paths. It builds the same three items and commits. It is a Given with no assertion, and feature line 476 still matches it (S1 passed, per the report). The plan's §4 expected this rewrite. Nothing that was asserted before is asserted any less now.

## Allowances

The report's `## Tests changed under an allowance` says "none". The diff agrees: no assertion or expected value changed in an existing test.

## Cannot verify

- **The work-item's target.** It says `migrate upgrade` on a clone of this repository should leave `model check` with no unresolved reference. Neither the implementer nor I could run this: cloning and running `model check` on a clone are outside the allowed commands. I did one read-only check (grep). Every `for:` and non-empty `blocked_by` value under .shop/work names a work-item in its own initiative, in the form `work-item/<name>`, which the new pattern handles. No `for:` target is held by two initiatives. That makes it likely, but does not prove it.
- **The report's green run** (`7 passed`) and suite figures. `work run` ran the suite; I did not re-run it.

## Findings

1. **Minor · observation: tests/scripts/test_migrate_upgrade_ids.py (no test of Decision 4).** The plan's Decision 4 said the move check on the upgrade path "is covered by a unit test only". No such test was added, so a regression in `move_failures` (scripts/migrate_upgrade.py:81-90) would go unnoticed. My probe shows the code works: a repository with `.shop/work/i1-x/runs/a/` and a tracked `.shop/work/i1-x/runs/w1/` gave rc 1 and `could not move .shop/work/i1-x/runs/a onto .shop/work/i1-x/runs/w1`; `a.md` was left in place and no commit was made. **Fix:** add that probe as a unit test.
2. **Minor · observation: scripts/migrate_upgrade_ids.py:83-93 and :109 (the refusal message).**
   - Every failure says "the reference" (`resolver` is always called with field `"reference"`), so the message does not say whether the name was in `blocked_by`, `depends_on` or `for`. The plan asked for the field.
   - A name that appears in two fields of one item gives two identical lines. The plan's failures are not de-duplicated; only the move failures are.
   - Reproduction: i1-x/a.md, i2-y/a.md, and i3-z/c.md with `blocked_by: [a]` and `for: a`. `migrate upgrade` gave rc 1 and printed `could not rename the reference a of .shop/work/i3-z/c.md: initiatives i1-x and i2-y all hold it` twice.
   - The refusal is still correct (r7: it exits with an error and changes no file); only the wording is weak.
   - **Fix:** pass the field matched in `rewrite_item` into the failure text, and de-duplicate `refused` in `upgrade`.
3. **Minor · observation: scripts/migrate_upgrade_ids.py:50 (token pattern widened to `[\w-]+`).**
   - Any token in a `blocked_by`, `depends_on` or `for:` line that equals the name of some work-item is now rewritten, in any initiative, including tokens that are not work-item references.
   - Reproduction: i1-x/migration-tools.md, and i1-x/b.md with `for: migration-tools#r26`. The upgrade gave `for: w2#r26`.
   - No repository sends this today: every `for:` in this repository is `work-item/<name>`. So this is hardening, not a wrong answer for any current input.
   - **Fix (optional):** require the token to be the whole list element, i.e. followed by `,`, `]` or the end of the line.
4. **Minor · drop: scripts/migrate_upgrade.py:84-88 (redundant duplicate-destination count).**
   - The comment says "two sources to one destination cannot sit in a dict". But the dict is keyed by source, so `check_moves` (migrate_write.py:55-60) already finds two sources with one destination.
   - The extra loop repeats that check. `dict.fromkeys` then hides the repeated message.
   - It is harmless; the cleanup is to remove the loop and the comment.

`tools check` ruff warnings (UP031 percent formatting, FURB167, PLW1510) match the style the files already use, on new lines and old ones alike. They are not graded.

## Commands run

- `git log --oneline -12 HEAD` and the `--grep` lookups for `ready -> claimed` and `claimed -> done`. `work/w1` is gone: "unknown revision".
- `git show --stat 36ad963`, `git diff ec2bbb9 36ad963`, `git diff --stat ec2bbb9 f3b75af`, `git show --stat f3b75af`
- `grep -rhE "^for:" .shop/work`, `grep -rnE "^(blocked_by|depends_on):" .shop/work`, `ls .shop/work/*/*.md | grep ...`: the shape of this repository's references.
- `grep -nE "(Given|And|When|Then) work-items" features/*.feature`: the parsed Given matches lines 476 and 500.
- I read scripts/migrate_write.py `check_moves` (lines 47-75). The risk I checked: whether a SimpleNamespace stand-in and the upgrade's chained renames are judged correctly. They are: `apply` renames through temporary names, and `check_moves` does not count a destination that is also a source.
- `python3 -m pytest -q -s -n 0 -p no:warnings -p no:cacheprovider .shop/scratch/w1-4-review/probe_review.py`: 3 passed, with the outputs quoted above.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base ec2bbb9...`:
  - ruff: 49 style warnings (UP031, FURB167, PLW1510) in the four files, the same style as the existing code
  - vulture: clean
  - import-linter: the project states no import contracts
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: nothing printed. The changed files are 137, 119, 269 and 79 lines.
