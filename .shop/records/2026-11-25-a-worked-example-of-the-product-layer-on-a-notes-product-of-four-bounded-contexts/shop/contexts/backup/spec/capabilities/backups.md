---
id: capability/example.org/notes/backup/backups
title: Backups
narrator: the person
group: service
area: backup
specifies: service backups
serves: [job/example.org/notes/j4]
language: codified-2
rests_on: []
retired: []
unbuilt: []
---

# Backups

## Purpose

The person saves the notes as a snapshot stored outside the product.

## Behaviour

### [g1] Saving the notes exports them and keeps a snapshot
- [r1] When the person saves the notes, the backup service shall export the notes and keep a snapshot.

### [g2] A bundle returned is stored as a snapshot
- [r2] When the notebook service returns a bundle, the backup service shall store a snapshot that has the bundle.

### [g3] A refused store is kept
- [r3] If the storage service refuses the request, then the backup service shall keep the request.

## Dropped
