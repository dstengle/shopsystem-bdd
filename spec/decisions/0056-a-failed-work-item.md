---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/a-failed-work-item
summary: "A fault outside a work-item's work moves it to `failed`, checked for before a stage starts; its work stays committed and pushed, and `work retry` returns it."
date: 2026-10-22
status: accepted
source: [observation/2026-10-21-one-requirement-per-scenario]
by: "the person, 2026-10-22"
---

# 0056. A failed work-item

## Decision

A fault that is not a question for the person (a push or git failure, a worker breaking a rule) moves the work-item to `failed`, never to `awaiting-ruling` and never back to an earlier status as if nothing happened; `work run` exits with an error naming the fault. `work run` verifies it can push the initiative branch before it starts any worker, so most faults are caught before work begins, and it pushes after every commit, so no completed work is lost. `failed` is not final: `work retry` returns the work-item once the fault is remedied. There are no automatic retries; a workflow engine is out of scope. This extends grammar.md v3's work-item lifecycle (`failed` from any stage's status; back to that status by `work retry`).
