---
id: defect/missingmass.io/shopsystem/shopsystem-bdd/batch-147/d1
kind: defect
batch: batch-147
item: b614
date: 2026-11-26
---

# batch-147 d1

batch_reach's _names looks a touched module's stem up with no dot before it, so a test that writes 'from plumbing.shop_files import x' is not reached by a change of scripts/plumbing/shop_files.py (only the review's whole suite runs it), against batches r78. Reproduce: touch scripts/plumbing/shop_files.py in a task; batch_reach.unreached names tests/scripts/test_shop_files.py.
