---
id: capability/example.org/fixture/supervision
title: Supervision
narrator: the person
group: service
language: codified-1
rests_on: []
retired: []
---

# Supervision

## Purpose
The spike's cluster (supervision r66), as codified groups, for the generation tests.

## Behaviour

### [g1] `work run` with no initiative takes the open initiatives side by side
Restates: r66@0.29.
- [r1] When the person runs `work run`, `work run` shall take every initiative whose status is not `done` or `abandoned`.
- [r2] When the person runs `work run`, `work run` shall interleave initiatives.

### [g2] worker slots
- [r3] `work run` shall hold at most `workers` worker slots at a time.

### [g3] a stage is given only a brief
- [r4] When `work run` starts a stage, `work run` shall give only a brief to the stage.

## Not yet
## Dropped
