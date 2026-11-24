---
id: model/missingmass.io/shopsystem/shopsystem-bdd/supply
area: supply
kind: port
imports: [execution]
---

# The work supply

## Purpose

What execution needs of the work it is given: assignments claimed for a batch, fulfilled when the batch is merged, relinquished when it is abandoned, suspended when a task waits on a question.

```model
object claim kind of request
  relations: for → assignment (one)

service supply
  operation claim(assignment)  outcomes: done → the claim | refused: assignment not claimable
  operation fulfil(assignment)  outcomes: done
  operation relinquish(assignment)  outcomes: done
  operation suspend(assignment)  outcomes: done
```
