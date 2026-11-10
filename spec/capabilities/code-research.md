---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/code-research
title: Code research
narrator: the script `work run`, which started the researcher
group: guarantees
rests_on: [design-decision/scout-on-haiku-at-low-effort, design-decision/worker-results-are-files, design-decision/the-file-set-is-the-claim, design-decision/workflow-capabilities-are-guarantees]
language: codified-1
retired: [r1, r2, r3, r4, r5, r6]
---

# Code research

## Purpose
**Retired in plugin 2.0.0** (design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-old-workflow-retired): every requirement of this capability is retired, and the file is kept as the record of its ids and of where its 0.29 lines went.

Reads the code and runs the system for one drafted work-item, so that its planner does not have to: why each
accepted scenario is red today, what the system answers today, the tests the change would break, and the file set
that becomes the work-item's claim. It is `code-scout`, started by `work run` on a `drafted` work-item. It builds
nothing and changes nothing in the checkout.

## Terms

- **module** (noun): a Python file of the repository's code or tests.
- **line count** (noun): the number of lines of a module and its room under the size limit `CLAUDE.md` gives.

## Behaviour

## Implementation, may change
- None: retired in plugin 2.0.0.

## Not yet
- None.

## Dropped
- r1@0.29: retired with code-research#r1, #r2 in 2.0.0 (the-old-workflow-retired).
- r3@0.29: retired with code-research#r3 in 2.0.0 (the-old-workflow-retired).
- r4@0.29: retired with code-research#r3 in 2.0.0 (the-old-workflow-retired).
- r5@0.29: retired with code-research#r3 in 2.0.0 (the-old-workflow-retired).
- r6@0.29: retired with code-research#r3 in 2.0.0 (the-old-workflow-retired).
- r8@0.29: retired with code-research#r4 in 2.0.0 (the-old-workflow-retired).
- r9@0.29: retired with code-research#r5 in 2.0.0 (the-old-workflow-retired).
- r10@0.29: retired with code-research#r1 in 2.0.0 (the-old-workflow-retired).
- r11@0.29: retired with code-research#r1 in 2.0.0 (the-old-workflow-retired).
- r12@0.29: retired with code-research#r6 in 2.0.0 (the-old-workflow-retired).
