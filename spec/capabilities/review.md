---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/review
title: Review
narrator: the script `work run`, closing a work-item or an initiative
group: guarantees
rests_on: [design-decision/review-of-work-items, design-decision/the-v3-agents, design-decision/worker-results-are-files, design-decision/workflow-capabilities-are-guarantees]
language: codified-2
retired: [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17, r18, r19, r20, r21]
---

# Review

## Purpose
**Retired in plugin 0.31.0** (design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-old-workflow-retired): every requirement of this capability is retired, and the file is kept as the record of its ids and of where its 0.29 lines went.

Finds defects in one work-item's commits or in an initiative branch as a whole, against the work-item's plan, the
spec and the repository's rules, and triages them. The reviewers are `bdd-task-reviewer` and `bdd-branch-reviewer`,
started by `work run`, and, when the person asks, `architecture-reviewer`. A reviewer changes nothing: what is to be
fixed now becomes a fix work-item, and the rest an observation.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| work-item | of | initiative | one |

## Behaviour

## Implementation, may change
- None: retired in plugin 0.31.0.

## Not yet
- None.

## Dropped
- r1@0.29: retired with review#r1 in 0.31.0 (the-old-workflow-retired).
- r2@0.29: retired with review#r5 in 0.31.0 (the-old-workflow-retired).
- r3@0.29: retired with review#r8 in 0.31.0 (the-old-workflow-retired).
- r4@0.29: retired with review#r9 in 0.31.0 (the-old-workflow-retired).
- r5@0.29: retired with review#r10 in 0.31.0 (the-old-workflow-retired).
- r6@0.29: retired with review#r11, #r12 in 0.31.0 (the-old-workflow-retired).
- r7@0.29: retired with review#r19 in 0.31.0 (the-old-workflow-retired).
- r8@0.29: retired with review#r18 in 0.31.0 (the-old-workflow-retired).
- r10@0.29: retired with review#r7 in 0.31.0 (the-old-workflow-retired).
- r11@0.29: retired with review#r13, #r14 in 0.31.0 (the-old-workflow-retired).
- r12@0.29: retired with review#r5, #r6 in 0.31.0 (the-old-workflow-retired).
- r13@0.29: retired with review#r2, #r3 in 0.31.0 (the-old-workflow-retired).
- r14@0.29: retired with review#r20 in 0.31.0 (the-old-workflow-retired).
- r28@0.29: retired with review#r21 in 0.31.0 (the-old-workflow-retired).
- r29@0.29: retired with review#r15 in 0.31.0 (the-old-workflow-retired).
- r30@0.29: retired with review#r15, #r16 in 0.31.0 (the-old-workflow-retired).
- r31@0.29: retired with review#r19 in 0.31.0 (the-old-workflow-retired).
- r32@0.29: retired with review#r4 in 0.31.0 (the-old-workflow-retired).
- r33@0.29: retired with review#r17 in 0.31.0 (the-old-workflow-retired).
- r34@0.29: retired with review#r19 in 0.31.0 (the-old-workflow-retired).
