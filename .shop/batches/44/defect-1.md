---
id: defect/missingmass.io/shopsystem/shopsystem-bdd/batch-44/d1
kind: defect
batch: batch-44
item: b316
date: 2026-11-26
---

# batch-44 d1

work batch done runs a chore's check with the session's own environment, not the tests' (batch_git's, the plugin's scripts on PYTHONPATH), so a check 'python3 -m pytest -p work_items ...' fails to find work_items in the task's worktree, against batches r66 (batch-147, b763's chore). Reproduce: a chore whose check is 'python3 -m pytest -p work_items -q tests/scripts/test_batch_reached.py', run by work batch done with no PYTHONPATH set.
