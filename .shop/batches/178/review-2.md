---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-178/review-2
kind: review
batch: batch-178
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/200
head: 3732eac3da3a0d2779be1c3059c2f4b399385bfd
range: 6652fad235572655f88c97a940785153db3bc236..3732eac3da3a0d2779be1c3059c2f4b399385bfd
result: clean
---

# batch-178 review 2

## Verdict

The fix closes f1. At submit, each path the apply writes that a task changed after its last apply is now three-way merged onto the rebuild. A change that does not merge is refused, naming the path and the item. Two observations remain, neither held as `fix now`.

## Findings

### f4 Important observation: a task branch that merged an earlier task's branch has that task's apply outputs treated as its own changes
- item: b874
- where: scripts/batch_merge.py:97
`_kept` takes every owned path in `git diff since branch`. The brief tells a later task of a context's first batch to merge an earlier task's branch into its own (scripts/batch_driver.py:116-117). After that merge, the diff from the later task's lines commit also holds the earlier item's apply outputs: its requirement lines, its `unbuilt:` and its features, as that task's workspace numbered them.

The risk is two items in one capability. Each workspace numbers its ids from the base, and the rebuild renumbers the later item past the earlier one. The merged branch's copy of that file then differs from both the lines commit and the rebuild, and `git merge-file` most likely conflicts. Submit is then refused, naming the earlier item's capability file as a change of the later task "after its lines". Before this fix, the rebuild's copy was simply kept, so this is a new refusal in a workflow the driver's brief describes.

What I verified: the driver line above, and the fact that `_kept` filters only by `is_owned`, never by which commits made the change. I did not reproduce it, so I cannot rule out a clean merge or duplicated lines in some layouts. Fix: leave out changes that reach the branch through another in-batch item's branch. One way is to diff only the task's own non-merge commits after `since`. Another is to take, as the base for those paths, the merged branch's own last lines commit.

### f5 Minor observation: the rebuild still generates features with the base's generator
- item: b874
- where: scripts/batch_rebuild.py:4
f1's first fix, running the rebuild's generator with the batch's merged code, was not done. Features a task regenerated with its changed generator are now carried over by `_kept`, or refused when they conflict with the rebuild's. So nothing is lost silently, which meets the fallback f1 allowed.

Some cases stay uncovered:
- A feature the task did not regenerate after its last apply is still in the old generator's output.
- So is a feature whose only change comes from another item's lines.

In both cases `features generate --check` can fail after submit, not at submit. At this Head the check exited 0.

## Earlier findings
- f1: fixed
