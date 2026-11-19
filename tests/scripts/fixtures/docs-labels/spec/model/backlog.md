---
id: model/example.org/acme/labels/backlog
area: backlog
kind: supporting
imports: []
---

# The backlog

## Purpose

The items of the backlog and the labels the person gives them.

```model
object item
  attributes: title (text)
  relations: has → label (many)

object label

service backlog
  operation show(item)  outcomes: returned → the item
  operation tag(item, label)  outcomes: done

actor the person kind of agent
```
