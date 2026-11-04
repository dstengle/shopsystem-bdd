---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/telemetry
title: Telemetry
narrator: a session measuring a batch
group: service
language: codified-1
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: []
unbuilt: [r1, r2, r3, r4]
---

# Telemetry

## Purpose
`measure` records, for each batch, its wall time, session time, tokens and cost by role (planning, implementing,
review, fixing), and the defects: those the pull request's review found and those found after the merge, each traced
to its item (design goal 8). The system's goals pull against each other (wall time, token cost, defect rate), and the
knobs (batch size, review depth, the readiness bar) are tuned against these figures.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| defect | of | item | one |
| defect | for | batch | one |
| measurement | of | batch | one |

## Behaviour

### [g1] `measure batch` writes a merged batch's measurement
- [r1] When the person runs `measure batch` on a batch that is `merged`, `measure` shall write a measurement of the
  batch, include "wall time", include "session time", include "tokens" and include "cost by role".

### [g2] The review's findings are counted by grade
- [r2] While a review finding is on the pull request of a batch, when the person runs `measure batch` on the batch,
  `measure` shall include the grade of the review finding.

### [g3] A defect after the merge is traced to its item and batch
- [r3] While an item is `delivered` and the item is in a batch, when the person runs `measure defect` on the item,
  `measure` shall write a defect of the item for the batch.

### [g4] `measure compare` sets two batches side by side
- [r4] When the person runs `measure compare batch-2 batch-3`, `measure` shall print "batch-2" and print "batch-3".
