---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/trials-0-37
title: Trials
narrator: the session that started a trial
group: guarantees
rests_on: [design-decision/the-session-keeps-the-gate, design-decision/the-v3-agents, design-decision/workflow-capabilities-are-guarantees]
language: codified-2
retired: [g1, r1, g2, r2, g3, r3, g4, r4, g5, r5, g6, r6, g7, r7, g8, r8, g9, r9, g10, r10]
---

# Trials

## Purpose
Runs one trial and records what it measured: the agent `trial-runner`, started by a session with a plugin tool or
`work run` to run on a real target or a fixture repository and what to measure. It is not a fix and not a review:
it changes nothing but the measurement record it writes, and what the measurement shows is for the session to
decide on. A walking skeleton (design-decision/behaviour-lines-are-ears): it grows from what using it shows.

## Terms

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Relations

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Behaviour

## Implementation, may change
- `agents/trial-runner.md`; its model (Sonnet) and its having no dispatch are guaranteed by role-boundaries.
- The input names a plugin tool or `work run`, a real target or a fixture repository, and what to measure. The record
  is under `.shop/records/measurements/` and names what the trial ran, on what target, and what it measured.

## Not yet
- None.

## Dropped
## Moved

Every line moved to a new capability with a new id (the domain contract, 0.38.0).

| old | new |
|---|---|
| g6 | trials#g11 |
| r6 | trials#r11 |
| g7 | trials#g12 |
| r7 | trials#r12 |
| g8 | trials#g13 |
| r8 | trials#r13 |
| g9 | trials#g14 |
| r9 | trials#r14 |
| g10 | trials#g15 |
| r10 | trials#r15 |
