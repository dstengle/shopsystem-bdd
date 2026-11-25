---
id: model/example.org/notes/backup/storage
area: storage
kind: port
imports: [backup]
---

# storage

## Purpose

What backup needs of a storage provider: a snapshot stored, and a stored snapshot fetched back.

```model
service storage
  operation store(snapshot)  outcomes: done
  operation fetch(snapshot)  outcomes: returned → the snapshot
```
