---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/red-green
title: Red-green
narrator: the script `work run`, which started the implementer
group: guarantees
rests_on: [design-decision/feature-files-read-only-in-red-green, design-decision/plans-list-the-tests-they-break, design-decision/worker-results-are-files, design-decision/the-file-set-is-the-claim, design-decision/work-item-lifecycle-as-run, design-decision/workflow-capabilities-are-guarantees]
language: codified-2
retired: [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15]
---

# Red-green

## Purpose
**Retired in plugin 2.0.0** (design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-old-workflow-retired): every requirement of this capability is retired, and the file is kept as the record of its ids and of where its 0.29 lines went.

Implements one ready work-item, one scenario at a time, under `bdd-red-green`, by the `bdd-implementer` that
`work run` starts in the work-item's worktree; or continues one, or does one fix work-item. The scenarios are
the contract; the implementer satisfies them and stops when one cannot be satisfied honestly. It never decides what
a scenario should have said, and it never writes a work-item's transition: `work run` reads its result.

## Terms
- **passing** (adjective of scenario): a scenario that passes when it is run alone with `python3 -m pytest`.

## Behaviour

## Implementation, may change
- None: retired in plugin 2.0.0.

## Not yet
- None.

## Dropped
- r1@0.29: retired with red-green#r1, #r2 in 2.0.0 (the-old-workflow-retired).
- r2@0.29: retired with red-green#r3 in 2.0.0 (the-old-workflow-retired).
- r3@0.29: retired with red-green#r4 in 2.0.0 (the-old-workflow-retired).
- r5@0.29: retired with red-green#r5, #r6 in 2.0.0 (the-old-workflow-retired).
- r6@0.29: retired with red-green#r7 in 2.0.0 (the-old-workflow-retired).
- r7@0.29: retired with red-green#r8 in 2.0.0 (the-old-workflow-retired).
- r9@0.29: retired with red-green#r9 in 2.0.0 (the-old-workflow-retired).
- r10@0.29: retired with red-green#r10 in 2.0.0 (the-old-workflow-retired).
- r11@0.29: retired with red-green#r11 in 2.0.0 (the-old-workflow-retired).
- r15@0.29: retired with red-green#r12 in 2.0.0 (the-old-workflow-retired).
- r16@0.29: retired with red-green#r13 in 2.0.0 (the-old-workflow-retired).
- r17@0.29: retired with red-green#r14 in 2.0.0 (the-old-workflow-retired).
- r18@0.29: retired with red-green#r15 in 2.0.0 (the-old-workflow-retired).
