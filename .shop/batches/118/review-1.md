---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-118/review-1
kind: review
batch: batch-118
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/141
head: cdc0a777879af726974ed2e672932b1dd090ee47
range: ab773a35250b294fb29629d6771f5ae02e79dafc..cdc0a777879af726974ed2e672932b1dd090ee47
result: clean
---

# batch-118 review 1

## Verdict

The batch builds both items. b694 reads the pack kinds again after the lay, and b692 adds prepare task, build or finish according to whether the task has a kept change citing its item, and the findings file. Every run exits 0, the feature files match what `features generate --check` writes, and no test is removed or weakened. The size, 663 changed lines, is under the limit of 1000. Two observations, nothing to fix now.

## Findings

### f1 Minor observation: an amend's relay commit reads as a built task
- item: b692
- where: scripts/batch_next.py:42
`_built` counts any commit on the task's branch after the batch's lines commit that has an `Item: <item>` trailer. `work batch amend` puts such a commit on the task's branch. It is the empty "requirement lines ... amended" commit at scripts/batch_amend.py:140, which carries `Item: <item>`. So a running task whose only commit is an amend's relay commit gets `finish task` in place of `build task`. Read word for word, r145 still holds, because that commit is a kept change citing the item. But the driver would then run `work batch done` on a task where nothing has been built. What I checked: `_cites` reads only the Item trailers, and batch_amend writes that trailer on the task branch's commit. A possible hardening: leave out commits that carry a `Laid:` line.

### f2 Minor observation: the module map row of readiness_handlers_imports does not name r70
- item: b694
- where: CLAUDE.md:383
The row still says only "items#r68's and r69's Givens (b688)". The module now also builds r70's world: it adds the `text` and `page` objects to the fixture's notes model with their terms, and the item imports `base` and retires notes' `text` term (b694). The module's docstring says this, but the binding map does not. Fix: add r70 and b694 to the row.
