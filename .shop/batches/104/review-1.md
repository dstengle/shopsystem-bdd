---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-104/review-1
kind: review
batch: batch-104
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/127
head: efb0fc527ed0acc359cc947983fd5de7c1b497ae
range: 653173b1b96da85486add9ba827bc5d2e0d7f66b..efb0fc527ed0acc359cc947983fd5de7c1b497ae
result: fix-now
---

# batch-104 review 1

## Verdict

The batch builds b600's two lines (batches#r125, reviews#r13), and the chores b640 and b629 do what their notes ask. There are three findings. The first is to fix now: the vulture check fails at Head and passed at the base. The second is the main one to record: b640's new order goes against the live line batches#r101, and the item that made it a chore dropped the lines that were meant to retire r101. The third is the size, which is over the limit.

## Findings

### f1 Minor fix now: `tools check` fails at Head on an unused `kwargs` in docs_testing.py
- item: b629
- where: tests/scripts/docs_testing.py:82
`python3 scripts/tools check --base 653173b1b` exits 1 at Head and exited 0 at the base:

```
== vulture ==
tests/scripts/docs_testing.py:82: unused variable 'kwargs' (100% confidence)
```

The line itself is older than the batch. b629's commit 3bd82d266 changed tests/scripts/docs_testing.py, so the file is now among the changed files `check` reads, and the batch leaves a configured review check failing. The file is in b629's chore files, so the fix belongs on b629. Fix: rename the parameter to `**_kwargs` in `caught(self, *args, **kwargs)` (or drop it), so the check exits 0 again.

### f2 Important observation: an item past the review limit that fails the readiness bar now stays `ready`, against batches#r101
- item: b640
- where: scripts/batch_pick.py:68
b640 moves `batch_estimate.exceeds` ahead of `_alone` (the readiness bar). The new order does what the chore asks. But the live line spec/capabilities/batches.md:154 still says:

```
- [r101] While an item is `ready` and the item does not meet the readiness bar, when the person opens a batch, the batches service shall reopen the item.
```

r101 has no condition on the review limit. With this change, a `ready` item that fails the bar but exceeds the limit is put in `left_out` and stays `ready`. It is never reopened, so `work batch start` now gives the wrong answer to r101 for that state.

b640's notes planned for this: r118, with r101 retired for the items within the limit as r119. Those lines were dropped when the item became a chore, because their scenarios passed on the lay. So the spec and the code now disagree.

b640's own tests show the same narrowing. The b483 f1 test in tests/scripts/test_batch_pick.py was rewritten, and its limit moved from `size = 1` to `size = 100000`. It no longer covers an item over the limit that fails the bar. The behaviour change was intended, so I do not count this as a weakened test. Still, nothing now checks r101's over-the-limit case either way.

This cannot be fixed on b640: a chore may not touch `spec/`. Fix: write a `work idea` item now that retires batches#r101 with a line limited to items within the review limit (r119 as in b640's notes). It can also take the r118 line, if a scenario can be found that fails before the fix.

### f3 Minor observation: the change is over the review limit, mostly from b629's docs
- item: -
- where: -
`## Size` gives 41 files, +1395 -952, against a limit of 1000 changed lines. Most of it is b629: docs/reference/commands.md alone is about 1850 diff lines, plus recipes.md, upgrading.md, concepts.md, troubleshooting.md and tour.md. b629's note had estimated 600-700 changed lines. b600's code and scenarios and b640's two hunks are a small part of the total.
