---
id: model/example.org/acme/checklists/checklists
area: checklists
kind: core
imports: []
---

# The checklists

## Purpose

The checklists the person keeps, the notes each holds, and the characters of a note.

```model
object checklist
  attributes: title (text)
  relations: holds → note (many)

object note
  attributes: text (text); length (number)
  relations: has → character (many)

object character

service checklists
  operation contents(checklist)  outcomes: returned → every note
  operation list()  outcomes: returned → every checklist
  operation characters(note)  outcomes: returned → every character
  operation length(note)  outcomes: returned → the note
  operation show(note)  outcomes: returned → the note

actor the person kind of agent
```
