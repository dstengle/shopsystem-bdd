---
id: defect/missingmass.io/shopsystem/shopsystem-bdd/batch-60/d1
kind: defect
batch: batch-60
item: b456
date: 2026-11-26
---

# batch-60 d1

batch_reach leaves tests/scripts/test_bound.py (features vocab --check) unreached when a task's change touches only a handler under tests/scenarios/ or a feature: batch-149 t4 (b761) added a Then handled in a local chain, work batch done passed, and review's whole suite failed test_bound. Reproduce: a task commit touching tests/scenarios/<x>_handlers.py; batch_reach.unreached lists tests/scripts/test_bound.py.
