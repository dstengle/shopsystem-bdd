---
id: capability/example.org/fixture/logic-cluster/supervision
title: Supervision
narrator: the person
group: service
language: codified-1
retired: []
---

# Supervision

## Purpose

The spike's cluster of supervision lines, codified, for the tests of `model logic` on fixed ids. g11 and g12 say
opposite things of one trigger (L1, each naming the other). g2 and g6–g8 are the old pacing written as the resources
stages and rounds hold (no finding). g3 and g4 restate r66 and r95 with one statement (L2). g9 sets a status off the
transition table (L3, through the transition guard), and g10's pre-state cannot be reached (L4).

## Behaviour

### [g1] `work run` takes the open initiatives
Restates: r66@0.29.
- [r1] When the person runs `work run`, `work run` shall take every open initiative.

### [g2] one stage of an initiative at a time
Restates: r66@0.29.
- [r2] Every stage for an initiative shall hold the initiative lock.

### [g3] one round at a time across initiatives
Restates: r66@0.29.
- [r3] Every integrate round shall hold the spec lock.

### [g4] rounds one at a time
Restates: r95@0.29.
- [r4] Every integrate round shall hold the spec lock.

### [g5] research stages start together
Restates: r59@0.29.
- [r5] While research stages for an initiative are `waiting`, when the person runs `work run`, `work run` shall start every research stage for the initiative.

### [g6] an integrate round holds the spec lock
Restates: r95@0.29.
- [r6] When `work run` starts an integrate round, the round shall hold the spec lock.

### [g7] a round holds its initiative
Restates: r66@0.29.
- [r7] Every round for an initiative shall hold the initiative lock.

### [g8] a research stage holds a worker slot
Restates: r20@0.29.
- [r8] Every research stage shall hold a worker slot.

### [g9] `work abandon` abandons a proposed initiative
- [r9] When the person runs `work abandon` on an initiative that is `proposed`, `work` shall set its status to `abandoned`.

### [g10] a question for a request awaiting its asker
- [r10] While a request is `awaiting-asker`, `work` shall write a question.

### [g11] `work start` starts a proposed initiative
- [r11] When the person runs `work start` on an initiative that is `proposed`, `work` shall set its status to `started`.

### [g12] `work start` leaves a proposed initiative as it is
- [r12] When the person runs `work start` on an initiative that is `proposed`, `work` shall not set its status to `started`.

## Dropped
