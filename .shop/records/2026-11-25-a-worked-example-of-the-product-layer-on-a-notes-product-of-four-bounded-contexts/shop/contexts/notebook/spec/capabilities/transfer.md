---
id: capability/example.org/notes/notebook/transfer
title: Transfer
narrator: a client
group: service
area: notes-cli
specifies: service notes
language: codified-2
rests_on: []
retired: []
unbuilt: []
---

# Transfer

## Purpose

Handing every kept note over as a bundle and taking a bundle in.

## Behaviour

### [g1] Exporting returns a bundle of the kept notes
- [r1] When a client exports the notes, the notes service shall return a bundle that holds every note whose status is
  `kept`.

### [g2] A bundle imported is kept
- [r2] When a client imports a bundle, the notes service shall keep every note that the bundle holds.

### [g3] A bundle imported past the allowance is refused
- [r3] While the number of notes is at least `100`, if a client imports a bundle, then the notes service shall refuse
  the request and name an allowance.

## Dropped
