---
id: bounded-context/example.org/notes/notes-cli
title: notes
language: codified-2
imports: [request]
---

# notes

## Purpose

A command-line tool that keeps short notes: the person adds a note, lists them and removes one. It is not an editor
and not a sync service.

## Composition

| area | kind | capabilities |
|---|---|---|
| notes-cli | core | notes |
