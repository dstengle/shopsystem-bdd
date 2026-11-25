---
id: capability/example.org/notes/notebook/access
title: Access
narrator: a client
group: service
area: notes-cli
specifies: service notes
language: codified-2
rests_on: []
retired: []
unbuilt: []
---

# Access

## Purpose

Opening a note to a reader and closing it again, as another context of the product asks.

## Behaviour

### [g1] A note opened to a reader has the reader
- [r1] When a client opens a note to a reader, the notes service shall keep a note that has the reader.

### [g2] A removed note is not opened
- [r2] If a client opens a note whose status is `removed` to a reader, then the notes service shall refuse the request
  and name the note.

### [g3] A note closed to its reader completes
- [r3] While a note has a reader, when a client closes the note to the reader, the notes service shall complete the
  request.

## Dropped
