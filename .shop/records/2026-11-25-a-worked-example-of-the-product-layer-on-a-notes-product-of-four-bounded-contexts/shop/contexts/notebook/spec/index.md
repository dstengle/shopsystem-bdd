---
id: bounded-context/example.org/notes/notebook
title: notes
language: codified-2
imports: [request]
---

# notes

## Purpose

The person's notes, the tags they are filed under and who may read them, kept for the person and answered to the
other contexts of the notes product. It is not an editor, not a sync service and not a billing system.

## Composition

| area | kind | capabilities |
|---|---|---|
| notes-cli | core | notes, access, allowance, transfer, tags |
