---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-66/review-1
kind: review
batch: batch-66
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/90
head: 9c16653e89842a0fac01aa44ad5c1c4a2ee157f3
range: e425d4fbe2568ecf4b65ef24c19b9c6e51830342..9c16653e89842a0fac01aa44ad5c1c4a2ee157f3
result: clean
---

# batch-66 review 1

## Verdict

The batch builds all three items: b480's r46 and r47, b486's r96 and b488's r97. All five runs exit 0, and the change is under the size limit (22 files, +502 -45 against a limit of 1000). I found no test removed or weakened and no `.feature` file written by hand. Nothing needs fixing before the merge; two hardening observations follow.

- **b480:** `backlog_note._open` already refuses an item that is not `idea`, `shaped`, `ready` or `needs-input`, and its message gives the item's label. So adding the lines and binding their scenarios to the backlog's handlers (`requested.py`) is enough.
- **b486:** `relay` runs `_bar` after the old lines are taken out and before the new ones are laid. That happens in the batch worktree, before `_based` makes the base's commit. So a refusal resets only the branches, removes any worktree it made, and leaves the base untouched, as r96's "change nothing" asks.
- **b488:** `batch_laid.passing` runs alongside `violating` in `_build`. It skips each line that retires an id. `work_items` keeps only the unbuilt scenarios of the laid ids, and only the xdist controller writes the report, which the new script test checks with and without xdist.
- **Module map:** `CLAUDE.md` is updated for `batch_laid`, `batch_start`, `batch_amend` and `work_items`.

## Findings

### f1 Minor observation: a failed amend now runs `git clean -fdq` in a batch worktree no check covers
- item: b486
- where: scripts/batch_amend.py:305
The new rollback runs `git clean -fdq` in every worktree in `heads`, and that includes the batch's own worktree `.shop/worktrees/batch-<n>`. `_checked` (scripts/batch_amend.py:155-159) only checks the task's worktree for loose files, using `uncommitted`, and that check skips `.shop/scratch`. So a failed amend deletes any untracked, unignored file a person left in the batch worktree, and anything unignored under `.shop/scratch` in the task worktree. This is the risk I checked: neither path is refused beforehand. Reproduction: create an untracked file in the batch worktree, then make an amend fail after the lay, for example with the commit-msg hook from `test_a_failed_amend_puts_back_the_bases_commit_with_the_branches`; the file is gone. Hardening: clean only the paths the relay changed, or refuse an amend while the batch worktree has uncommitted changes.

### f2 Minor observation: the start's run of the laid scenarios ignores the run's exit code
- item: b488
- where: scripts/batch_laid.py:402
`passed` throws away the result of `batch_tasks.run_tests` and reads only the report file. If `[batch] tests` fails before any scenario runs (an import error in the laid tree, a bad `[batch] tests` command), there is no report and every item goes into the batch without a word. The line r97 still holds, because no scenario succeeded. But the person is never told the check did not run. Hardening: when the run exits with an error other than pytest's "no tests collected" (5) and wrote no report, say so in the output.
