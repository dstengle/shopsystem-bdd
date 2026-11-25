---
id: bounded-context/example.org/notes/sharing/adapter/notebook
title: notebook port over the notebook context
kind: adapter
realises: [notebook-port#r1, notebook-port#r2]
providers: [bounded-context/example.org/notes/notebook@1.0.0]
language: codified-2
imports: [request]
---

# notebook port over the notebook context

## Purpose

The adapter that realises sharing's notebook port with the notebook context's published operations: showing a note
is the notebook's opening of the note to the colleague as a reader, hiding it its closing.

## Composition
