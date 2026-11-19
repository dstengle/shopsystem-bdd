---
id: model/example.org/checklists/checklists-cli/checklists
area: checklists
kind: core
imports: []
---

# checklists

## Purpose

The checklists the person keeps, their items, and the checklists service that answers the person's requests.

```model
object checklist
  attributes: title (text)
  relations: holds → item (many)

object item
  attributes: text (text); status: open | done
  lifecycle status: open → done

service checklists
  operation create(title)  outcomes: done → the checklist | refused: no title
  operation add(checklist, text)  outcomes: done → the item | refused: no text
  operation check(item)  outcomes: done
  operation list(checklist)  outcomes: returned → every item

actor the person kind of agent
```
