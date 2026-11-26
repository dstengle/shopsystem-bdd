---
id: defect/missingmass.io/shopsystem/shopsystem-bdd/batch-149/d1
kind: defect
batch: batch-149
item: b771
date: 2026-11-26
---

# batch-149 d1

backlog_chore.run takes batch_tasks.interpreter(tree) alone while run_tests takes interpreter(tree, workspace, root): a task worktree with no .venv runs its chore's check under the system python3 where its tests run under the checkout's .venv/bin/python. Reproduce: a checkout holding .venv, a task worktree holding none, a chore check 'python3 -c ...' printing sys.executable.
