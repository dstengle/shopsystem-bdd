---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/slice-budget-refused-by-plan
summary: "A slice lands in at most 8 production and 4 test modules, and `plan` refuses a slice whose Lands: line is over that."
date: 2026-10-10
status: accepted
revisit_when: "the Lands count is exceeded in more than half of a measured batch's slices"
revisit_signal: measurement/kb-batches-32-35
source: [decision-argument/2026-10-10-small-slices-and-steps-design]
by: "0.11.0"
---

# 0008. Slice budget refused by plan

## Decision

Every slice of the batch about to be planned has `Lands: <p> production, <t> test`, counting the migration it forces, probed for a slice that changes an existing form. Over 8 or 4 the slice is cut again; `plan` refuses it.

## Context

One kb slice ran as one implementer over 72 files and 426k tokens.

## Alternatives

No budget; a budget per dispatch instead (which 0.11.1 also added).

## Consequences

In kb batches 32-35 the Lands count was exceeded in 15 of 23 slices and sizing scouts cost about 790k tokens, while the written dispatch budget was kept in 13 of 14 runs. The revisit signal has fired; initiative i6 proposes demoting the refusal to an estimate.
