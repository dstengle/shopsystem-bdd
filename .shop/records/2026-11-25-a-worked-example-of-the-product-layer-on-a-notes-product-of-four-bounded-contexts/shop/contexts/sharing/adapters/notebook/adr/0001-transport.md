---
id: design-decision/example.org/notes/sharing/adapter/notebook/transport
summary: "The adapter calls the notebook's published operations open and close, the colleague's address as the reader."
date: 2026-11-25
status: accepted
tier: judgement
---

# 0001. Transport

## Decision

show(note) is notes.open(note, reader = the invitation's address); hide(note) is notes.close(note, reader). The
notebook context's contract 1.0.0 is the one obtained.
