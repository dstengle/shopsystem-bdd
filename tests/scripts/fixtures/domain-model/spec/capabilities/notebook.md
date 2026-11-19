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

### [g3] A note added with a text and a priority is kept
- [r3] When the person adds a note with a text and the priority `high`, the notes service shall keep the note.

### [g4] A note added without a text is refused
- [r4] If the person adds a note without a text and the reminder, then the notes service shall refuse the request and
  name the text.

### [g5] A tag a note is labelled with is kept
- [r5] When the person labels a note with a tag, the notes service shall keep the tag.

### [g6] Listing the notes completes the request
- [r6] When the person lists the notes, the notes service shall complete the request.
