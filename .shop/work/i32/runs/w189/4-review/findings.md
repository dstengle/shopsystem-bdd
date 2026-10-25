# Review of w189 (review#r31)

**Verdict: DONE.** No findings. The one commit narrows the branch reviewer's `questions` to the findings it triages fix now, which is what review#r31 says. It changes nothing else.

## Commits reviewed

The branch `work/w189` is gone, so the commits are those between `6fa7dc00` (`work: w189 ready -> claimed`) and `72e77945` (`work: w189 claimed -> done`) on the checked-out history, less `work run`'s own `work:` commits:

- `ee81efd0` bdd-branch-reviewer: questions hold only fix-now findings (review#r31). It changes `agents/bdd-branch-reviewer.md`: 2 lines added, 2 removed.

This matches the implementer's `result.json` `commits` list and its report ("Commit: ee81efd0. Files changed: 1."). It is also the work-item's `fileset`.

## What changed, against the plan and the capability

- Line 74, `questions`: it was "each fix-now or Critical finding, and each check you could not verify". It is now "only the findings you triaged fix now". Critical findings not triaged fix now, and checks that could not be verified, stay in `findings.md` and in `status`. This is plan decision 1 and review#r31.
- Line 71, `status` rule: unchanged. That is plan decision 2. The review#r6 "fail the review" is still carried by `DONE_WITH_CONCERNS`.
- Line 76, `NEEDS_CONTEXT`: the reason now goes in the summary, and `questions` is left empty. This is plan decision 3. review#r28's "stop, saying why" is still met by the summary.
- Risk I checked: whether some other text still tells the branch reviewer to put Critical or unverified lines in `questions`. `scripts/supervise_review.py:52-57`, the brief text, names `questions` but gives no rule for what goes in it, so it does not contradict the agent file. In the agent file itself, only lines 74 and 76 mention `questions`, and both are consistent.
- Nothing in the change goes beyond a Behaviour line. It is prompt text that serves r31 and r28. No code was changed.

## Removed and weakened tests

None. No test file was changed: the diff touches only `agents/bdd-branch-reviewer.md`. I searched the diff's file list for `tests/` and `features/` and found neither.

## Allowances

The report's `## Tests changed under an allowance` says "none". The commits agree: no test changed.

## Cannot verify

- The report's run of `tests/scripts/test_agents.py` (8 passed, 18 subtests): I did not re-run it. It checks only the frontmatter, and the frontmatter is unchanged in the diff.
- No scenario can show that r31 holds. review is `group: guarantees`, under decision 0065. The plan names `measure` of a later initiative as the check, and that cannot be verified from these commits.

## Findings

None.

## Tool checks

- `tools check --base 6fa7dc00`: ruff, nothing to check; vulture, nothing to check; import-linter, the project states no import contracts.
- `tools size --limit 300`: printed nothing, so no file is over the limit.

## Commands run

- `git log --format=%H -1 --grep="^work: w189 ready -> claimed$" --all` gave `6fa7dc00`
- `git log --format=%H -1 --grep="^work: w189 claimed -> done$"` gave `72e77945`
- `git log --oneline -15`
- `git log --stat 6fa7dc00..72e77945`
- `git diff 6fa7dc00 ee81efd0`
- `grep -n "questions" agents/bdd-branch-reviewer.md scripts/supervise_review.py`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 6fa7dc00`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `git status --short`: clean
