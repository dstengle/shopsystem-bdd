---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/review-guarantees
title: Review guarantees
narrator: the session that started a review
group: guarantees
area: execution
specifies: guarantees of a review
language: codified-2
retired: []
unbuilt: []
---

# Review guarantees

## Purpose
What `pr-reviewer` reads and writes in reviewing a batch's change, and where its findings send the batch.

## Behaviour

### [g1] A batch submitted is reviewed
- [r1] When the batches service submits a batch, `pr-reviewer` shall review the proposed change of the batch.

### [g2] A review reads every judgement decision
- [r2] While the tier of a design-decision is `judgement`, when `pr-reviewer` reviews a proposed change, `pr-reviewer`
  shall review the design-decision.

### [g3] A review changes nothing but reviews
- [r3] `pr-reviewer` shall change only reviews of a proposed change.

### [g4] A first review reads every line proposed and every kept change
- [r4] While a proposed change of a batch has no review, when `pr-reviewer` reviews the proposed change, `pr-reviewer`
  shall review every requirement that an item in the batch proposes and every kept change of the batch.

### [g5] A review reads only the batch's kept changes
- [r5] When `pr-reviewer` reviews a proposed change of a batch, `pr-reviewer` shall review only kept changes of the
  batch.

### [g6] A review with a finding to fix now sends the batch back to building
- [r6] While the triage of a review finding on the proposed change of a batch is `fix now`, when a session concludes a
  review of the batch, the reviews service shall set the status of the batch to `building`.

### [g7] A re-review reads the kept changes for each finding
- [r7] While the triage of a review finding on a proposed change is `fix now`, when `pr-reviewer` reviews the proposed
  change, `pr-reviewer` shall review every kept change for the review finding.

### [g8] A clean review sends the batch to await its merge
- [r8] While a batch has a proposed change and no review finding on the proposed change whose triage is `fix now`
  exists, when a session concludes a review of the batch, the reviews service shall set the status of the batch to
  `awaiting-merge`.

### [g9] A review finding names its grade and triage
- [r9] When `pr-reviewer` reviews a proposed change, `pr-reviewer` shall name the grade of every review finding on the
  proposed change and the triage of every review finding on the proposed change.
