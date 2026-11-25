---
id: bounded-context/example.org/notes/backup
title: backup
language: codified-2
imports: [request]
---

# backup

## Purpose

Snapshots of the person's notes kept with a storage provider outside the product, and the notes restored from one,
on the same device or a new one. It keeps no note itself.

## Composition

| area | kind | capabilities |
|---|---|---|
| backup | core | backups, restores |
| notebook | port | notebook-port |
| storage | port | storage-port |

## Upstreams

- bounded-context/example.org/notes/notebook: github: ex/notes-notebook
