---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-103/review-2
kind: review
batch: batch-103
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/126
head: e34cbb5c330ba8b08ec53ee8c55054b75d84a52d
range: 64c750e7d4a4450f42cbcae2432e1b2983819cfd..e34cbb5c330ba8b08ec53ee8c55054b75d84a52d
result: clean
---

# batch-103 review 2

## Verdict

The fix for f1 works. `dedicate` now refuses a pair that the live group already serves, and a pair that another open item holds. The unlay leaves alone any job the group serves in the file at the batch's base. The new script tests cover both refusals, an unlay over a job the base held, and an unlay of a job the item laid. One minor observation remains, and it does not hold the merge.

## Findings

### f3 Minor observation: `work batch amend` unlays with no base, so a job the base serves is not protected there
- item: b641
- where: scripts/batch_amend.py:108
`batch_amend` calls `batch_start.unlay_lines(tree, [old], COMMAND)` without a base. `backlog_serves.at_base` then returns None, and `unlay` takes the job off even when the batch's base serves it. Usually this changes nothing: the amend lays the item again straight after, and `lay` puts the job back.

The job is lost only in a narrow case:
1. An item dedicates a live group to a job.
2. Main then gains that same job on that group before `work batch start`.
3. The item is amended so that it no longer holds the pair.

The re-lay then does not restore the job, and it disappears from the batch branch. `dedicate`'s new refusal makes this case rare. The fix: pass `batch_parked.base_of(root, batch)` here, as `batch_review` and `batch_parked` already do.

## Earlier findings
- f1: fixed
