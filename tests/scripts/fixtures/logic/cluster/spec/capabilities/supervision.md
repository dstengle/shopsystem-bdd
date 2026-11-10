---
id: capability/example.org/fixture/logic-cluster/supervision
title: Supervision
narrator: the person
group: service
language: codified-2
retired: []
---

# Supervision

## Purpose

The spike's cluster of supervision lines, in grammar 4, for the tests of `model logic` on fixed ids. g11 and g12 say
opposite things of one trigger (L1, each naming the other). g1, g2 and g5-g8 run stages and take initiatives (no
finding). g3 and g4 say one thing twice (L2, and L8 each by the other). g9 sets a status off the transition table
(L3), and g10's pre-state cannot be reached (L4).

## Behaviour

### [g1] `work run` takes the started initiatives
Restates: r66@0.29.
- [r1] When the person runs `work run`, `work` shall take every initiative whose status is `started`.

### [g2] `work run` starts the waiting stages
Restates: r66@0.29.
- [r2] When the person runs `work run`, `work` shall start every stage whose status is `waiting`.

### [g3] `work next` starts the waiting stages
Restates: r66@0.29.
- [r3] When the person runs `work next`, `work` shall start every stage whose status is `waiting`.

### [g4] `work next` starts the waiting stages, said again
Restates: r95@0.29.
- [r4] When the person runs `work next`, `work` shall start every stage whose status is `waiting`.

### [g5] the stages of an initiative start together
Restates: r59@0.29.
- [r5] When the person runs `work start` on an initiative, `work` shall start every stage for the initiative.

### [g6] an ended stage leaves a result
Restates: r95@0.29.
- [r6] When a session ends a stage, `work` shall print the stage.

### [g7] `work take` takes an initiative
Restates: r66@0.29.
- [r7] When the person runs `work take` on an initiative, `work` shall take the initiative.

### [g8] `work stage` exits successfully
Restates: r20@0.29.
- [r8] When the person runs `work stage`, `work` shall exit successfully.

### [g9] `work abandon` abandons a proposed initiative
- [r9] When the person runs `work abandon` on an initiative whose status is `proposed`, `work` shall set the status of the initiative to `abandoned`.

### [g10] a question for a request awaiting its asker
- [r10] While a request is `awaiting-asker`, when the person runs `work ask`, `work` shall write a question.

### [g11] `work start` starts a proposed initiative
- [r11] When the person runs `work start` on an initiative whose status is `proposed`, `work` shall set the status of the initiative to `started`.

### [g12] `work start` leaves a proposed initiative as it is
- [r12] When the person runs `work start` on an initiative whose status is `proposed`, `work` shall not set the status of the initiative to `started`.

## Dropped
