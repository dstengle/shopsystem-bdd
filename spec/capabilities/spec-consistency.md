---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/spec-consistency
title: Spec consistency
narrator: the person keeping a spec
group: guarantees
rests_on: [design-decision/the-glossary-is-a-target-of-spec-work, design-decision/consistency-check-on-demand, design-decision/spec-writers-blind-to-code, design-decision/workflow-capabilities-are-guarantees]
language: codified-2
retired: [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17]
---

# Spec consistency

## Purpose
**Retired in plugin 0.31.0** (design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-old-workflow-retired): every requirement of this capability is retired, and the file is kept as the record of its ids and of where its 0.29 lines went.

Verifies a bounded context's spec against itself: that one word means one thing, that one thing has one word,
that a line has one reading, that the lines leave nothing to infer and that a scenario says what its line says. It is `checking-spec-consistency`,
used on demand by the session the person talks to, with a blind `spec-checker` dispatch for each judgment of
meaning. It reads nothing but `spec/` and `features/`, and integration and formulation do not use it.

## Behaviour

## Implementation, may change
- None: retired in plugin 0.31.0.

## Not yet
- None.

## Dropped
- r6@0.29: scenarios are generated from parsed statements, so no scenario uses a word the glossary avoids and none is reworded by hand.
- r7@0.29: no statement has two readings: one that does not parse to exactly one tree is refused (v_p1, v_p2).
- r1@0.29: retired with spec-consistency#r1 in 0.31.0 (the-old-workflow-retired).
- r2@0.29: retired with spec-consistency#r1 in 0.31.0 (the-old-workflow-retired).
- r3@0.29: retired with spec-consistency#r2 in 0.31.0 (the-old-workflow-retired).
- r4@0.29: retired with spec-consistency#r3, #r4, #r17 in 0.31.0 (the-old-workflow-retired).
- r8@0.29: retired with spec-consistency#r6 in 0.31.0 (the-old-workflow-retired).
- r9@0.29: retired with spec-consistency#r7 in 0.31.0 (the-old-workflow-retired).
- r10@0.29: retired with spec-consistency#r8 in 0.31.0 (the-old-workflow-retired).
- r11@0.29: retired with spec-consistency#r9 in 0.31.0 (the-old-workflow-retired).
- r21@0.29: retired with spec-consistency#r10 in 0.31.0 (the-old-workflow-retired).
- r22@0.29: retired with spec-consistency#r11 in 0.31.0 (the-old-workflow-retired).
- r23@0.29: retired with spec-consistency#r12 in 0.31.0 (the-old-workflow-retired).
- r24@0.29: retired with spec-consistency#r13 in 0.31.0 (the-old-workflow-retired).
- r25@0.29: retired with spec-consistency#r14 in 0.31.0 (the-old-workflow-retired).
- r26@0.29: retired with spec-consistency#r15 in 0.31.0 (the-old-workflow-retired).
- r27@0.29: retired with spec-consistency#r16 in 0.31.0 (the-old-workflow-retired).
- r28@0.29: retired with spec-consistency#r5 in 0.31.0 (the-old-workflow-retired).
