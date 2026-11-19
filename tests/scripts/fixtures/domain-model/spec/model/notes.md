---
id: model/example.org/fixture/notes
area: notes
kind: core
imports: []
---

# Notes

## Purpose

The notes a person keeps, and the tags they carry.

```model
object note
  attributes: text (text); priority: low | high
  lifecycle status: draft → active; active → retired; draft → retired
  relations: carries → tag (many)

object tag
  attributes: name (text)
  relations: of → note (one)

service notes
  operation add(text)  outcomes: done → the note
  operation file(note)
    outcomes: done | refused: not a draft
  operation archive(note)  outcomes: done
  operation list()  outcomes: returned → every note

event a note is added: raised by notes.add
actor the person kind of agent
```
