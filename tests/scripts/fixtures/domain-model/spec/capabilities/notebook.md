---
id: capability/example.org/fixture/domain-model/notebook
title: Notebook
narrator: a person keeping notes
group: service
area: notes
specifies: service notes
language: codified-2
retired: []
unbuilt: []
---

# Notebook

## Purpose
A person adds notes, files them and archives them.

## Behaviour

### [g1] A note added is filed
- [r1] When the person adds a note, the notes service shall file the note.

### [g2] A note that carries a tag is archived when it is filed
- [r2] While a note carries a tag, when the person files the note, the notes service shall archive the note.
