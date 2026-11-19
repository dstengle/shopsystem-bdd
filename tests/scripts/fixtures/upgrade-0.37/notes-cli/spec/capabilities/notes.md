---
id: capability/example.org/notes/notes-cli/notes
title: Notes
narrator: the person
group: service
language: codified-2
rests_on: []
retired: []
unbuilt: []
---

# Notes

## Purpose

Adding, listing and removing notes.

## Behaviour

### [g1] `notes add` adds a note under a tag
- [r1] When the person runs `notes add` with the `--title` option and the `--tag` option, `notes` shall add a note under a tag and exit successfully.

### [g2] `notes add` refuses a note with no title
- [r2] If the person runs `notes add` without the `--title` option, then `notes` shall refuse the command and name `--title`.

### [g3] `notes list` prints every note
- [r3] When the person runs `notes list`, `notes` shall print the title of every note.

```given
the file `notes.json` holds:
  [{"title": "Buy milk", "tags": ["home"]},
   {"title": "Call the bank", "tags": []}]
```

### [g4] `notes remove` deletes a note
- [r4] When the person runs `notes remove` on a note, `notes` shall delete the note.

## Dropped
