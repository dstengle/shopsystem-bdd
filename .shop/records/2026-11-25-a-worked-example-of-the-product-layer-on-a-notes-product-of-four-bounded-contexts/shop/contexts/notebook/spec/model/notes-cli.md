---
id: model/example.org/notes/notebook/notes-cli
area: notes-cli
kind: core
imports: []
---

# notes

## Purpose

The notes the person keeps, the tags they are filed under, the readers a note is open to, the allowance of notes the
person's plan gives, and the notes service that answers the person's and the other contexts' requests.

```model
object note
  attributes: title (text); status: kept | removed
  lifecycle status: kept → removed
  relations: under → tag (many); has → reader (many)

object tag
  attributes: spelling (text)

object reader

object allowance
  attributes: size (number)

object bundle
  relations: holds → note (many)

service notes
  operation add(title, tag)  outcomes: done → the note | refused: no title | refused: allowance used up
  operation list(tag)  outcomes: returned → every note
  operation remove(note)  outcomes: done
  operation rename(tag, spelling)  outcomes: done
  operation open(note, reader)  outcomes: done | refused: removed note
  operation close(note, reader)  outcomes: done
  operation enlarge(allowance)  outcomes: done
  operation reduce(allowance)  outcomes: done
  operation export()  outcomes: returned → the bundle
  operation import(bundle)  outcomes: done | refused: allowance used up

actor the person kind of agent
actor a client kind of agent
```
