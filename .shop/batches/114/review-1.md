---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-114/review-1
kind: review
batch: batch-114
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/137
head: b6b03e10d88d008e10e0e2933260a9beb3ff5201
range: 0c650f10b0e481d0d54e8af419886316cde6de4f..b6b03e10d88d008e10e0e2933260a9beb3ff5201
result: fix-now
---

# batch-114 review 1

## Verdict

The batch builds r32 and r33. Their scenarios meet them, and the runs, size and module map are clean. One finding is to fix: in r33's own world, r31's condition also holds, so r31 says `port request` while the code returns `saga`. Either the code answers r31 wrongly or the lines contradict each other.

## Findings

### f1 Important fix now: r31's condition holds in the saga world, where the code returns `saga` instead of `port request`
- item: b680
- where: scripts/product_coordination.py:248
In r33's scenario world all of r31's conditions hold. A group serves the job, and its line r10 uses `stock.reserve`. The port line `stock-port#r1` governs `stock.reserve`. No requirement handles any outcome of it, because `build` adds `HANDLED` only in the transition world. So r31 obliges the product service to return the job whose coordination is `port request`. On the same trigger, r33 obliges `saga`, and `coordination` holds one value only. The code picks `saga` because "the most specific kind wins", but that precedence comes from the item's notes and no line says it. As written, the change gives a wrong answer against r31 whenever a saga's port operation has no outcome handler. That is the normal saga case, and it is the exact world of the r33 scenario.

The r33 scenario passes only because the code puts saga first. No scenario checks r31 in a world that also meets r33.

Fix: make the lines say the precedence, so that r31 no longer holds where r33 does. For example, reword r31 on b680 (`work line --reword`, then `work batch amend`) to add "and the operation does not have a property that refers to an operation" or an equivalent exclusion. Then check that `spec logic` reads the pair clean. Do the same for r32 against r33 if a saga world can also meet r32's condition. Alternatively, return `port request` whenever r31's condition holds, but that would break r33.

### f2 Minor observation: outcome handlers are matched by the operation's object, not by the operation
- item: b680
- where: scripts/product_coordination.py:252
`handlers` collects each line whose `on_outcome` names `ops[o].object`. Two port operations whose `done →` outcome is the same object (say `reserve` and `allocate`, both returning a reservation) share one set of handlers. A line on one operation's outcome then counts as handling the other's too. As a result, a trace that r31 says is a `port request` (the second operation's outcome handled by no line) can be read as handled, giving `None` or `long-running process`. No world in this batch has two operations with one object: `allocate` in the saga world has no `→` object. Reproduction: give `stock.allocate` the outcome `done → the reservation`, request only `allocate` from the serving group, and keep notebook's g11 on the completed reservation. The code treats `allocate`'s outcome as handled. What I read: model_bound's `on_outcome` keys a fact by object (`("on_outcome", ident, k, obj)`, model_bound.py:70), and its docstring says model.lp joins it on `op_object`, so the ambiguity comes from the fact itself, not from this change.
