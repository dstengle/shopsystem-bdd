---
id: capability/example.org/notes/backup/storage-port
title: Storage port
narrator: the backup service
group: service
area: storage
specifies: service storage
language: codified-2
rests_on: []
retired: []
unbuilt: []
---

# Storage port

## Purpose

What backup needs of the storage provider it reaches.

## Behaviour

### [g1] A snapshot stored completes
- [r1] When the backup service stores a snapshot, the storage service shall complete the request.

### [g2] A snapshot fetched is returned
- [r2] When the backup service fetches a snapshot, the storage service shall return the snapshot.

## Dropped
