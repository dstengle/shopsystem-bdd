---
id: model/missingmass.io/shopsystem/shopsystem-bdd/execution
area: execution
kind: supporting
imports: [tracking, specification]
---

# Work execution

## Purpose

Work being done: batches of ready items, their tasks and workspaces, the change put up for review, its reviews and their findings.

```model
object review kind of text

object review finding kind of text
  attributes: grade: Critical | Important | Minor; triage: fix now | observation | drop
  relations: on → proposed change (many)

object workspace
  relations: holds → file | repository | kept change | requirement (many); has → workspace name | shared workspace (many)

object kept change
  relations: for → review finding (many); touches → file (many); cites → item (many)

object batch kind of file
  attributes: status: building | in-review | awaiting-merge | merged | abandoned
  lifecycle status: building → in-review; in-review → building; in-review → awaiting-merge; awaiting-merge → merged; in-review → merged; building → abandoned; in-review → abandoned
  relations: holds → item (many); has → task | proposed change | review folder | batch plan | kept change | measurement | wall time | session time | token | role | workspace | review (many)

object batch plan kind of file

object task
  attributes: status: pending | running | done | failed
  relations: has → workspace (many)

object proposed change
  relations: holds → kept change (many); has → review (many)

object batch brief kind of file
  relations: holds → chore (many)

object review folder kind of file

object pr-reviewer kind of dispatch

object shared workspace kind of workspace

service batches
  operation open(batch)  outcomes: done → the batch
  operation resume(batch)  outcomes: done
  operation finish(task)  outcomes: done | refused: chore breaking, file outside the chore
  operation park(item)  outcomes: done
  operation submit(batch)  outcomes: done → the proposed change | refused: task not done, kept change citing no item
  operation merge(proposed change)  outcomes: done
  operation abandon(batch)  outcomes: done
  operation monitor(batch)  outcomes: returned → the batch

service reviews
  operation review(change)  outcomes: done → the review
  operation conclude(review)  outcomes: done
```
