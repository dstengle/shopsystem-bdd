---
id: capability/example.org/notes/backup/restores
title: Restores
narrator: the person
group: service
area: backup
specifies: service backups
serves: [job/example.org/notes/j6]
language: codified-2
rests_on: []
retired: []
unbuilt: []
---

# Restores

## Purpose

The person restores the notes from a stored snapshot, on this device or a new one.

## Behaviour

### [g1] Restoring a snapshot fetches it
- [r1] When the person restores a snapshot, the backup service shall fetch the snapshot.

### [g2] A snapshot fetched is imported
- [r2] When the storage service returns a snapshot, the backup service shall import the bundle of the snapshot.

### [g3] A lost snapshot is not restored
- [r3] If the person restores a snapshot whose status is `lost`, then the backup service shall refuse the request and name the snapshot.

## Dropped
