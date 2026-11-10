---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/u7-is-a-judgement
summary: "U7 (a worker shall change only files in its worktree) is verified by judgement: the implementer and the reviewer."
date: 2026-11-10
status: accepted
tier: judgement
verified_by: [judgement]
rests_on: [U7]
by: "the session for b169, 2026-11-10"
---

# 0090. U7 is a judgement

## Decision

U7 is verified by judgement: a batch task's subagent changes only files in its task's worktree; work batch done's check that a task's commits leave .shop/ alone covers part of it, and the rest is put before every implementer and reviewer.
