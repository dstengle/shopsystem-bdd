---
id: model/missingmass.io/shopsystem/shopsystem-bdd/execution
area: execution
kind: supporting
imports: [tracking, specification, upgrades, measurement]
---

# Work execution

## Purpose

Work being done: batches of ready items, their tasks and workspaces, the change put up for review, its reviews and their findings.

```model
object review kind of text
  relations: holds → review finding (many)

object review finding kind of text
  attributes: grade: Critical | Important | Minor; triage: fix now | observation | drop
  relations: on → proposed change (many)

object workspace
  relations: holds → file | repository | kept change | requirement (many); has → workspace name | shared workspace (many)

object kept change
  relations: for → review finding (many); touches → file (many); cites → item (many)
  relations: conflicts with → kept change (many)

object batch kind of file
  attributes: status: building | in-review | awaiting-merge | merged | abandoned
  lifecycle status: building → in-review; in-review → building; in-review → awaiting-merge; awaiting-merge → merged; in-review → merged; building → abandoned; in-review → abandoned
  relations: holds → item (many); has → task | proposed change | review folder | batch plan | kept change | measurement | wall time | session time | token | role | workspace | review (many)
  lifecycle status: awaiting-merge → in-review
  lifecycle status: awaiting-merge → building
  relations: has → batch summary (many)
  relations: has → batch brief (one)

object batch plan kind of file

object task
  attributes: status: pending | running | done | failed
  relations: has → workspace (many)

object proposed change
  relations: holds → kept change (many); has → review (many)

object batch brief kind of file
  relations: holds → chore (many)
  relations: holds → batch rule (many)
  relations: holds → batch summary form (many)

object review folder kind of file
  relations: holds → findings file (one)

object pr-reviewer kind of dispatch

object shared workspace kind of workspace

service batches
  operation open(batch)  outcomes: done → the batch
  operation resume(batch)  outcomes: done
  operation finish(task)  outcomes: done | refused: chore breaking, file outside the chore
  operation park(item)  outcomes: done
  operation submit(batch)  outcomes: done → the proposed change | refused: task not done, kept change citing no item, batch with no base merge
  operation merge(proposed change)  outcomes: done
  operation abandon(batch)  outcomes: done
  operation monitor(batch)  outcomes: returned → the batch
  operation amend(item, review finding)  outcomes: done | refused: item not in batch
  operation configure(setting, setting value)
    outcomes: done → the settings file | refused: setting outside the delivery settings form, setting value outside the delivery settings form
  operation reopen(batch, review finding)  outcomes: done → the review | refused: batch not awaiting merge
  operation poll(batch)  outcomes: returned → the batch step

service reviews
  operation review(change)  outcomes: done → the review
  operation conclude(review)  outcomes: done

object capability form kind of artifact

object index form kind of artifact

object virtual environment kind of file

object setting kind of text

object setting value kind of text

object settings file kind of file
  relations: holds → setting (many)
  relations: holds → batch rule (many)

object delivery settings form kind of artifact

object base merge kind of kept change

object batch rule kind of text

object batch summary kind of text

object batch summary form kind of text

object review limit

object amendment kind of kept change

service shop
  operation keep(bounded context, id)  outcomes: done → the bounded context | refused: id outside the product id, id kept already
  operation list(shop)  outcomes: returned → every bounded context

object shop
  relations: holds → bounded context (many); has → product id (one)

object product id kind of text
  relations: covers → id (many)

actor the driver kind of agent

object batch step
  attributes: instruction: prepare task | build task | finish task | submit batch | review change | fix finding | park item | stop
  relations: holds → task | batch brief | review folder | findings file | review finding (many)

object findings file kind of file
```
