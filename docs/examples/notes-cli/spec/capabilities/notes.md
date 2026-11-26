---
id: capability/example.org/notes/notes-cli/notes
title: Notes
narrator: the person
group: service
area: notes-cli
specifies: service notes
language: codified-2
rests_on: []
retired: []
unbuilt: []
---

# Notes

## Purpose

Adding, listing and removing notes.

## Behaviour

### [g1] A note added with a title and a tag is kept
serves: keep-notes
- [r1] When the person adds a note with a title and a tag, the notes service shall keep the note under the tag.

### [g2] A note added without a title is refused
serves: keep-notes
- [r2] If the person adds a note without a title, then the notes service shall refuse the request and name the title.

### [g3] Listing the notes returns every note
serves: find-notes
- [r3] When the person lists the notes, the notes service shall return every note.

### [g4] Removing a note sets its status to removed
serves: clear-notes
- [r4] When the person removes a note, the notes service shall set the status of the note to `removed`.

### [g5] A removed note is not removed again
serves: clear-notes
- [r5] If the person removes a note whose status is `removed`, then the notes service shall refuse the request.

## Dropped
