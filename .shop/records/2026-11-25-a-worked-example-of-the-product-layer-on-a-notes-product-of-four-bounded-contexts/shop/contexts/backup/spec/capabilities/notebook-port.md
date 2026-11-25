---
id: capability/example.org/notes/backup/notebook-port
title: Notebook port
narrator: the backup service
group: service
area: notebook
specifies: service notebook
language: codified-2
rests_on: []
retired: []
unbuilt: []
---

# Notebook port

## Purpose

What backup needs of the notebook it reaches.

## Behaviour

### [g1] Exporting returns a bundle
- [r1] When the backup service exports the notes, the notebook service shall return a bundle.

### [g2] A bundle imported completes
- [r2] When the backup service imports a bundle, the notebook service shall complete the request.

## Dropped
