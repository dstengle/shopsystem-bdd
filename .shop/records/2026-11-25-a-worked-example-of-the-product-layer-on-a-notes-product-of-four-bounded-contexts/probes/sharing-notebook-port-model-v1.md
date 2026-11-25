---
id: model/example.org/notes/sharing/notebook
area: notebook
kind: port
imports: []
---

# notebook

## Purpose

What sharing needs of the notebook it reaches: a note shown to a colleague and hidden again.

```model
object note

service notebook
  operation show(note)  outcomes: done | refused: removed note
  operation hide(note)  outcomes: done
```
