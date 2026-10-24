# Review of w125

**Verdict: DONE.** No finding is Critical or triaged fix now. The commit does what the work-item asks for. r65's exit 0 is now decided in `pytest_sessionfinish` from `--work-item` and the spec, on the xdist controller and on each worker, and the stash that only collection set is gone. The new `-n 2` test passes, and so does the rest of `tests/scripts/test_work_items.py` (12 passed).

## Commits reviewed

The branch `work/w125` is gone. The commits on HEAD between `da9ab26 work: w125 ready -> claimed` and `9f769c9 work: w125 claimed -> done`, leaving out work run's `work:` commits:

- `a0b04d1` work_items: decide r65's exit from the work-item and spec at session end, on controller and workers (`scripts/work_items.py` +7/-7, `tests/scripts/test_work_items.py` +7)

The implementer's results (3-implement and 4-implement) list `3cb355a` with the same subject. `git diff 3cb355a a0b04d1 -- scripts tests` is empty, so `a0b04d1` is the same change re-applied onto HEAD. The second implement stage made no commit, and its report says so. The rest of `da9ab26..9f769c9` is work run's own files: the log, the 4-implement stage files and the work-item's status.

The earlier claim (`15a08fa`..`c8ec860`) ended in awaiting-answer with no code commit.

## Removed and weakened tests

None. What I searched: the diff of `tests/` in `a0b04d1`. It adds one test, `test_a_guarantees_work_item_left_with_no_test_exits_successfully_under_xdist`, and removes or changes no line. It has no `-` line under `tests/`, drops no parametrize case, adds no skip or xfail, and loosens no assert. No file under `features/` is changed.

## Allowances

Both reports' `## Tests changed under an allowance` say "none", and this holds: no existing test was changed.

## Cannot verify

- The merge check end to end (`supervise_merge`, `-n auto`) for a guarantees-only work-item. No test drives it, and the plan and both reports say so. The new `-n 2` unit test, which runs the worktree's plugin through `PYTHONPATH=<worktree>/scripts`, is the evidence.
- The report's suite figure at start (761 passed, 13 failed, the 13 being phase B and C scenarios). I did not re-run the whole suite (work run does). The 13 failures in the brief's question all lie in batch-measurement, design-model-check and work-queue scenarios, none in this work-item's files.

## Findings

1. **Minor, drop** (w125). The implementer's results name commit `3cb355a`, but the commit on HEAD is `a0b04d1`. The patch is identical: `git diff 3cb355a a0b04d1 -- scripts tests` is empty. work run re-applied the commit when it merged it. Nothing to fix in the work-item.

Risks checked, with no finding:

- **Exit codes other than 5 are left alone.** In `scripts/work_items.py:128` the hook returns early unless exitstatus is NO_TESTS_COLLECTED, and also under `--whole-suite`. The stash was never set under `--whole-suite` before either, so behaviour there is unchanged (plan D-b).
- **`accepted()` can raise `SystemExit` at `scripts/work_items.py:130`.** The risk was that a missing work-item reaches this line with exit 5 and crashes instead of the refusal. A missing work-item is refused in collection first: exit 3, serially and under `-n 2`, as probed below. So session end never sees exit 5 for a missing work-item.
- **An empty `accepts:`.** `all([])` is True, as it was with the stash. No change.
- **What counts as guarantees.** The test is `group: guarantees` in the capability's frontmatter, through the existing `guarantees()`. That matches decision 0065 and the capability note at `spec/capabilities/supervision.md:124`.
- **No behaviour beyond r65.** The new code only turns exit 5 into 0 for a guarantees-only work-item, which is what r65 asks for.

## Checks

- `tools check --base da9ab26`: ruff: all checks passed. vulture: clean. import-linter: the project states no import contracts.
- `tools size --limit 300`: no output, so no file is over the limit.

## Commands run

- `git log --format=%H -1 --grep="^work: w125 ready -> claimed$" work/w125`: unknown revision, the branch is gone.
- `git log --format=%H -1 --grep="^work: w125 ready -> claimed$"` -> `da9ab26`. The same for `claimed -> done` -> `9f769c9`.
- `git log --format='%h %s' 15a08fa~1..HEAD`, `git show --stat 3cb355a`, `git show --stat a0b04d1`, `git diff 3cb355a a0b04d1 -- scripts tests` (empty), `git show a0b04d1`, `git diff da9ab26 9f769c9 --stat`
- `python3 -m pytest -q -n 0 -p no:cacheprovider tests/scripts/test_work_items.py` -> 12 passed
- `python3 -m pytest -q -n 2 --work-item nosuch .shop/scratch/w125-5-review/empty` -> exit 3 (INTERNALERROR, SystemExit "no such work-item")
- `python3 -m pytest -q -n 0 --work-item nosuch .shop/scratch/w125-5-review/empty` -> exit 3, the same
- `python3 -m pytest -q -n 2 --work-item w125 .shop/scratch/w125-5-review/empty` -> exit 5. That is right, because supervision is `group: service`, not guarantees. These runs from the worktree loaded `/home/vscode/shopsystem-bdd/scripts/work_items.py` through the environment's PYTHONPATH, not the worktree's copy. So they show only collection-time behaviour, which this commit leaves unchanged. The worktree's plugin was exercised by `tests/scripts/test_work_items.py`.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base da9ab26...`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
