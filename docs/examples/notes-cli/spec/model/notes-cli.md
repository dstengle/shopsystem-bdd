---
id: model/example.org/notes/notes-cli/notes-cli
area: notes-cli
kind: core
imports: []
---

# notes

## Purpose

The notes the person keeps, the tags they are filed under, and the notes service that answers the person's requests.

```model
object note
  attributes: title (text); status: kept | removed
  lifecycle status: kept → removed
  relations: under → tag (many)

object tag

service notes
  operation add(title, tag)  outcomes: done → the note | refused: no title
  operation list()  outcomes: returned → every note
  operation remove(note)  outcomes: done

actor the person kind of agent
```
