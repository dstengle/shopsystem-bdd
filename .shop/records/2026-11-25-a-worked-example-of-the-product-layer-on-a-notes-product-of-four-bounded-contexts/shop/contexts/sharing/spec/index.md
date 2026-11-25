---
id: bounded-context/example.org/notes/sharing
title: sharing
language: codified-2
imports: [request]
---

# sharing

## Purpose

Inviting a colleague to read one of the owner's notes, the colleague's answer, and the owner taking the invitation
back. It keeps no note; it asks the notebook to show a note to a colleague and to hide it again.

## Composition

| area | kind | capabilities |
|---|---|---|
| sharing | core | invitations |
| notebook | port | notebook-port |

## Upstreams

- bounded-context/example.org/notes/notebook: github: ex/notes-notebook
