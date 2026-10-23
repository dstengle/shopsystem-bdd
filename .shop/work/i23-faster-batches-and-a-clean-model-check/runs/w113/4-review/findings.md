# Review of w113: work answer refuses every Unicode mandatory line break

**Verdict: DONE.** No Critical finding and none triaged fix now. One Minor finding: a lint error the commit introduced.

## Commits reviewed

The branch `work/w113` is gone, so the commits are those on the checked-out history between `56ecb28 work: w113 ready -> claimed` and `1df4fea work: w113 claimed -> done`:

- `a3cb90e work answer refuses every Unicode mandatory line break, first`

This is the one commit the implementer's `result.json` lists. They match.

Files: `features/work-queue.feature` (-9), `scripts/workqueue_answer.py` (+5/-2), `tests/scenarios/test_work_queue.py` (+2), `tests/scenarios/work_queue_answer_steps.py` (+9/-3).

## Changes under features/

- Removed only the scenario "answer with a newline in it is refused, and nothing changes (deprecated)" (@r15 @deprecated). The work-item's `## Retires` lists it under delivery#r17. `test_work_queue.py` binds the feature through `scenarios()`, so the binding is gone with the scenario, and its own When step ("with an answer of two lines" with nothing after it) was removed with it. Nothing else under `features/` changed. This removal is allowed.

## Removed and weakened tests

I searched the diff for removed `def test_`, removed or loosened `assert` lines, dropped parametrize or Examples rows, and added skip or xfail.

- The deprecated scenario's node and its When step `answer_of_two_lines` (the old form) were removed. This is the retirement the work-item lists. The plan calls it a retirement in part 4, not a break. What it proved (LF refused, nothing changed) is still proved by the Outline's "a newline" example.
- Nothing else. No assertion was changed or removed and no skip or xfail was added.

## Allowances

- `tests/scenarios/test_work_queue.py`, `with_items` (Given), **setup**: **holds.** The diff adds two lines that write a `planned -> ready` log line for a ready item when the initiative has no log yet. It adds, removes or changes no `assert`, no expected value and no parametrize case. It is needed because the shared Then "... are as they were" reads `log.jsonl`.

## Cannot verify

- The report's figures "144 passed, 1 skipped" for `--work-item w113`, and its claim that the starting suite had 8 failures. I did not run the whole suite: `work run` ran it before the merge.
- Whether the new ready-item log line changes any other scenario that uses the "ready" Given. I found no named risk in the diff, and the full suite run by `work run` covers it.

## Findings

### F1. Minor: ruff I001 in tests/scenarios/work_queue_answer_steps.py:2 (observation)

- **What is wrong:** `tools check --base 56ecb28` reports `I001 Import block is un-sorted or un-formatted`.
- **Cause:** before the commit, the import block was followed by a `def`, and two blank lines are right for that. Now it is followed by the module-level assignment `BREAKS = ...` (line 7), and isort's default wants one blank line before an assignment. The commit introduced the error.
- **Why it matters:** `check` is no longer clean for this file. The initiative's aim is a clean check.
- **Fix:** remove one blank line before `BREAKS`, or run `ruff --fix`.
- **Reproduction:** `python3 <Scripts>/tools check --base 56ecb2806ae1ba06bbf60e47f3f21910c0055ec6` gives the I001 line above, with "Found 1 error."
- **Work-item:** w113.

### Behaviour checked, no finding

- `LINE_BREAKS` holds exactly the seven code points r15 lists. I confirmed U+2028 and U+2029 in the literal with `grep -P '\x{2028}\x{2029}'`. The check is a membership test, not `splitlines`, so FS, GS and RS are not refused, as the plan's D1 decides.
- The check runs first in `answer()`, before `find`, `agrees` and `asked_from`, and nothing is written before it (r15, and the plan's D2). As a result, a two-line answer to a missing work-item is refused as more than one line, which agrees with D2's "before any other reason to refuse".
- The refusal message ("the answer has a line break in it; an answer is one line") says that an answer is one line (r15, D4).
- No code that no line asks for: the only behaviour added is r15's refusal.
- `work add`'s LF/CR check was left unchanged, as the plan's D3 decides.

## Commands run

- `git log --format=%H -1 --grep="^work: w113 ready -> claimed$" work/w113`: failed, the branch is gone.
- `git log --format='%H %s' -1 --grep=...` for ready -> claimed and claimed -> done, and `git log --oneline -12`.
- `git show --stat a3cb90e`, `git show a3cb90e`.
- `grep -nP 'LINE_BREAKS = .*\x{2028}\x{2029}"' scripts/workqueue_answer.py`: matched line 12.
- `grep -n r15 spec/capabilities/work-queue.md`, and `sed -n 205,250p features/work-queue.feature`.
- `python3 -m pytest -q -p no:cacheprovider tests/scenarios/test_work_queue.py -k "line_break or two_lines or answer"`: 8 passed.
- `python3 <Scripts>/tools check --base 56ecb28...`: ruff gave 1 error (F1); vulture clean; import-linter found no contracts.
- `python3 <Scripts>/tools size --limit 300`: nothing over the limit.
- `git show 56ecb28:tests/scenarios/work_queue_answer_steps.py`, to compare the imports before and after.
- `git status --porcelain`: clean.
