---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/batch-measurement
title: Measurement of an initiative's deliveries
narrator: a session measuring an initiative's deliveries
group: service
language: codified-2
rests_on: [design-decision/measure-an-initiative, design-decision/measure-refuses-unknown-shapes, design-decision/plugin-takes-the-dependencies-it-needs]
unbuilt: []
retired: [g18, g19, g20, g21, g22, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17, r18, r19, r20, r21, r22, g23, r23, g24, r24, g25, r25, g26, r26, g27, r27]
---

# Measurement of an initiative's deliveries

## Purpose
`scripts/measure` writes one measurement of an initiative's deliveries from what `work run` already records: the
initiative's `log.jsonl`, each stage's `session.json` and the sessions' transcripts. It reads measurements back as
tables and compares two of them. It writes no prompt, reply or tool content, and refuses a file of a shape it does
not know rather than guessing at it.

## Terms

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Relations

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Behaviour

## Implementation, may change
- A measurement is a record whose frontmatter id is of kind `measurement`; its figures are one JSON block in its
  body, which `show` and `compare` read back. `measure initiative`, which wrote an initiative's, was retired in
  plugin 0.31.0 with r1-r17 (the-old-workflow-retired); the records it wrote are still shown and compared.

## Not yet
- Figures beyond what `work run` already records: the skeleton grows from the measurements of 0.21.0's, 0.22.0's
  and 0.23.0's deliveries; a line is added when one of those measurements needs a figure the measurement does not
  give.

## Dropped
- r39@0.29: retired with batch-measurement#r1 in 0.31.0 (the-old-workflow-retired).
- r40@0.29: retired with batch-measurement#r1 in 0.31.0 (the-old-workflow-retired).
- r41@0.29: retired with batch-measurement#r9 in 0.31.0 (the-old-workflow-retired).
- r42@0.29: retired with batch-measurement#r9 in 0.31.0 (the-old-workflow-retired).
- r43@0.29: retired with batch-measurement#r17 in 0.31.0 (the-old-workflow-retired).
- r46@0.29: retired with batch-measurement#r2 in 0.31.0 (the-old-workflow-retired).
- r47@0.29: retired with batch-measurement#r6, #r7 in 0.31.0 (the-old-workflow-retired).
- r48@0.29: retired with batch-measurement#r10 in 0.31.0 (the-old-workflow-retired).
- r49@0.29: retired with batch-measurement#r17 in 0.31.0 (the-old-workflow-retired).
- r50@0.29: retired with batch-measurement#r2 in 0.31.0 (the-old-workflow-retired).
- r51@0.29: retired with batch-measurement#r12 in 0.31.0 (the-old-workflow-retired).
- r52@0.29: retired with batch-measurement#r11 in 0.31.0 (the-old-workflow-retired).
- r53@0.29: retired with batch-measurement#r8 in 0.31.0 (the-old-workflow-retired).
- r55@0.29: retired with batch-measurement#r14 in 0.31.0 (the-old-workflow-retired).
- r57@0.29: retired with batch-measurement#r13 in 0.31.0 (the-old-workflow-retired).
- r58@0.29: retired with batch-measurement#r8 in 0.31.0 (the-old-workflow-retired).
- r59@0.29: retired with batch-measurement#r9 in 0.31.0 (the-old-workflow-retired).
- r60@0.29: retired with batch-measurement#r17 in 0.31.0 (the-old-workflow-retired).
- r63@0.29: retired with batch-measurement#r15 in 0.31.0 (the-old-workflow-retired).
- r64@0.29: retired with batch-measurement#r16 in 0.31.0 (the-old-workflow-retired).
- r65@0.29: retired with batch-measurement#r3 in 0.31.0 (the-old-workflow-retired).
- r66@0.29: retired with batch-measurement#r4 in 0.31.0 (the-old-workflow-retired).
- r67@0.29: retired with batch-measurement#r5 in 0.31.0 (the-old-workflow-retired).
## Moved

Every line moved to a new capability with a new id (the domain contract, 0.38.0).

| old | new |
|---|---|
| g23 | measurement#g5 |
| r23 | measurement#r5 |
| g24 | measurement#g6 |
| r24 | measurement#r6 |
| g25 | measurement#g7 |
| r25 | measurement#r7 |
| g26 | measurement#g8 |
| r26 | measurement#r8 |
| g27 | measurement#g9 |
| r27 | measurement#r9 |
