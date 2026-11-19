---
id: bounded-context/example.org/notes/notes-cli
title: notes
language: codified-2
imports: [cli]
---

# notes

## Purpose

A command-line tool that keeps short notes in one file: `notes add` writes a note, `notes list` prints them and
`notes remove` deletes one. It is not an editor and not a sync service.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| note | under | tag | many |
| title | of | note | one |

## Glossary

- **the person** (proper noun): the human at the terminal. Kind of: agent.
- **`notes`** (proper noun): the notes tool. Kind of: tool.
- **note** (noun): one short text the person keeps, with a title.
- **title** (noun): the one line that names a note.
- **tag** (noun): a word the person files a note under.
- **file** (noun): the one file on disk where `notes` keeps every note.
- **add** (verb, action): a tool keeps a new thing. Frame: tool adds note.
- **delete** (verb, action): a tool removes a thing for good. Frame: tool deletes note.
