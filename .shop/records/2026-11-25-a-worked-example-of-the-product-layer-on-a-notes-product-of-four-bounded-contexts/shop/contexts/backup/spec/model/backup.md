---
id: model/example.org/notes/backup/backup
area: backup
kind: core
imports: [notebook, storage]
---

# backup

## Purpose

The snapshots of the person's notes and where each has got to.

```model
object snapshot
  attributes: status: taken | stored | lost
  lifecycle status: taken → stored; taken → lost
  relations: has → bundle (one)

service backups
  operation save()  outcomes: done → the snapshot
  operation restore(snapshot)  outcomes: done | refused: lost snapshot

actor the person kind of agent
```
