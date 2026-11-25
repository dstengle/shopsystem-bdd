---
id: model/example.org/notes/backup/notebook
area: notebook
kind: port
imports: [backup]
---

# notebook

## Purpose

What backup needs of the notebook: every kept note handed over as a bundle, and a bundle taken in.

```model
object bundle

service notebook
  operation export()  outcomes: returned → the bundle
  operation import(bundle)  outcomes: done
```
