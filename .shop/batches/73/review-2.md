---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-73/review-2
kind: review
batch: batch-73
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/97
head: d86972376ac4dcd96c66217eeb57c3362a2f1555
range: 7a09a3c3bc8b7cd7afd460140f2bc54d2115392a..d86972376ac4dcd96c66217eeb57c3362a2f1555
result: clean
---

# batch-73 review 2

## Verdict

The fix closes f1. `migrate upgrade` now calls `shop_files.refuse_task_branch` before it does anything else, so on a task's branch it refuses, names the task, and commits and pushes nothing. The test now covers the command both on a task's branch and on the base. One `Minor` observation, which does not hold the merge.

## Findings

### f6 Minor observation: `migrate upgrade`'s refusal says "work commits nothing"
- item: b60
- where: scripts/migrate_upgrade.py:160
The refusal reuses the text of `shop_files.refuse_task_branch` (scripts/shop_files.py:213). On a task's branch, `migrate upgrade` therefore prints:

```
migrate changed nothing; batch-1-b1 is the branch of task t2 of batch-1; work commits nothing on a task's branch: run it in the base branch's checkout
```

It names the task and the branch, as U20 requires. But it calls the tool `work` while the person ran `migrate`. Reproduction: check out a task's branch `batch-<n>-b<j>` with `.shop/plugin-version` a release behind the plugin, then run `migrate upgrade`.

## Earlier findings
- f1: fixed
