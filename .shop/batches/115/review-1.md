---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-115/review-1
kind: review
batch: batch-115
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/138
head: 74a081752d915909172530e8c972dde751cee976
range: 682da3473dbb9ac40da11b29fc575e0c399cea56..74a081752d915909172530e8c972dde751cee976
result: clean
---

# batch-115 review 1

## Verdict

The batch builds both items. b686's chore changes only its three named files, and its check covers a usage error and both kinds of refusal. b683's `work batch next` returns the step each of r135-r141 names, in the order the item's notes give. Nothing needs fixing now. Two observations follow about where the code departs from the literal text of the lines, and one about how the lines overlap.

## Findings

### f1 Minor observation: the poll leaves out cited findings and parked items' tasks, which the lines do not say
- item: b683
- where: scripts/batch_next.py:338
r137 says "a review of the batch holds a review finding whose triage is `fix now`", and r138 says "a task of the batch is `failed`". Neither line says "open", "uncited" or "of an in-batch item". The code narrows both:
```python
cited = batch_fix.for_finding(root, batch)
return [f for f in batch_findings.open_findings(root, batch.name) if not cited.get(f.fid)]
...
tasks = [t for t in batch.tasks if _in_batch(root, t)]
```
So a building batch whose `fix now` finding already has a commit citing it gets `submit batch`, not `fix finding`. A batch with a failed task whose item was parked gets no `park item`.

I checked that `batch_findings.open_findings` already drops findings a later review marked fixed and findings of items no longer in-batch, and that `batch_plan.TASK_STATUSES` is pending, running, done and failed. Read literally, r137 and r138 still hold in these states, so the observable answer differs from the lines. The narrowing is sensible: without it the driver would loop on a finding that is already fixed, or on an item that is already parked. But it is recorded only in the module map and in commands.md.

Fix (later item): add the qualifiers to the lines ("an open review finding that no commit cites", "a task of an in-batch item"), retiring r137 and r138.

### f2 Minor observation: the order between the steps is in no line
- item: b683
- where: spec/capabilities/batches.md:445
Several of r137-r141 can apply in one state. For example, a building batch with one failed task and one pending task meets both r138 (`park item`) and r139 (`build task`). Each line asks for "a batch step" with a different instruction, yet the service returns one step. The order that picks it (stop, review change, fix finding, park item, finish task, build task, submit batch) lives only in `pick`, the module map and the item's notes.

Every scenario sets up only one condition at a time, so none can fail on a wrong order. `tests/scripts/test_batch_next.py::test_the_order` is the only check of the order. That is checkable, but it does not trace to any requirement.

Fix (later item): say the precedence in the lines, for example with an "If" or "unless" form or a "no task of the batch is `failed`" condition on r139 and r140, so that the scenarios cover it.

### f3 Minor observation: a building batch with no in-batch task gets `stop`, which no line names
- item: b683
- where: scripts/batch_next.py:357
`pick` returns `("stop", None, None)` for a building batch whose tasks belong to no in-batch item. `test_a_batch_with_no_task_in_it_stops` asserts this. r135 gives `stop` only for `awaiting-merge`. If every task of the batch has been filtered out, r141's "every task of the batch is `done`" would read as true with nothing to check, and the line would ask for `submit batch`.

Reproduction: park every item of a building batch, then run `shop work batch next <batch>`. It prints `stop`, and no command is named under `report:`.

The answer is reasonable, because there is nothing left to submit. But it is behaviour no line asks for. A later line could name it, or the case could be taken out of the code.
