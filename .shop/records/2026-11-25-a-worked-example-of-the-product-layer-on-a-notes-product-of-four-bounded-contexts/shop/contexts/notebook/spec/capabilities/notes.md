---
id: capability/example.org/notes/notebook/notes
title: Notes
narrator: the person
group: service
area: notes-cli
specifies: service notes
serves: [job/example.org/notes/j1, job/example.org/notes/j2]
language: codified-2
rests_on: []
retired: []
unbuilt: []
---

# Notes

## Purpose

Adding, listing and removing notes, within the allowance the person has.

## Behaviour

### [g1] A note added with a title and a tag is kept
- [r1] When the person adds a note with a title and a tag, the notes service shall keep the note under the tag.

### [g2] A note added without a title is refused
- [r2] If the person adds a note without a title, then the notes service shall refuse the request and name the title.

### [g3] Listing the notes returns every note
- [r3] When the person lists the notes, the notes service shall return every note.

### [g4] Removing a note sets its status to removed
- [r4] When the person removes a note, the notes service shall set the status of the note to `removed`.

### [g5] Listing the notes with a tag returns the notes under it
- [r5] When the person lists the notes with a tag, the notes service shall return every note under the tag.

### [g6] A note added past the allowance is refused
- [r6] While the number of notes is at least `100`, if the person adds a note, then the notes service shall refuse the
  request and name an allowance.

## Dropped
