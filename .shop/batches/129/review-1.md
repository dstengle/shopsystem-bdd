---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-129/review-1
kind: review
batch: batch-129
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/152
head: dedbfd1cbc9a90dcd1a17d5554ee12cec536de73
range: 00584264f3799c0dbc55494bae85f289fab151a4..dedbfd1cbc9a90dcd1a17d5554ee12cec536de73
result: clean
---

# batch-129 review 1

## Verdict

The batch builds all three items: b726 (parsing#r27), b725 (batches#r166, r167) and b727 (parsing#r28, r29). Every run exits 0 at the head and at the base. The only test that goes is r160's scenario, and it goes because r167 retires r160. No test is weakened. One minor observation, nothing to fix.

## Findings

### f1 Minor observation: the module map's readiness_bound row does not name its new `before`
- item: b725
- where: CLAUDE.md:235
b725 gives `scripts/readiness_bound.py` a new function, `before`. It returns the bound check's violations of the base before the lay. It reads the readiness bar's result kept by readiness_before, or solves `model.lp` on the tree when nothing is kept, and `work batch start`'s `violating` now takes those away from its own. The module's docstring says this. Its row in the module map, and the `batch_start.py` row, still say only that `violating` reads the module. Neither names `before`, nor says that `work batch start` now counts only the violations a lay adds. Fix: name `before` in the readiness_bound row (b725, batches r166) and say in the batch_start row that `violating` leaves out the base's violations.

What I checked for the risk this raised: whether the violations kept by readiness_before have the same shape as those `violating` builds. Both are `(name, tuple(str(a) ...))`: `readiness_bar._violations` builds them that way, and `readiness_before._in` turns the stored lists back into tuples. So the set difference in `violating` compares like with like, and nothing breaks here.
