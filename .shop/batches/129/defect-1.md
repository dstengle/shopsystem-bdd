---
id: defect/missingmass.io/shopsystem/shopsystem-bdd/batch-129/d1
kind: defect
batch: batch-129
item: b725
date: 2026-11-26
---

# batch-129 d1

batches#r166 sets the status of the item to in-batch instead of requesting tracking's allocate, which v_m9 reports on main after the merge (decision 0133); the readiness bar and the batch opening let it through.
