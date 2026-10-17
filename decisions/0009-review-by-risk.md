---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/review-by-risk
summary: "A per-task review on Opus only for tasks touching concurrency, the published contract, data integrity or stored data; every other task is covered by the batch's branch review."
date: 2026-10-01
status: accepted
revisit_when: "more than half of a measured batch's per-task reviews come back clean"
revisit_signal: measurement/missingmass.io/shopsystem/shopsystem-bdd/kb-batches-32-35
source: "0.9.0 (d0abe14)"
---

# 0009. Review by risk

## Decision

Each task carries `Review:` and `Model:`. Per-task review on Opus for the named risks; `batch-end` and Sonnet for everything else. The branch review runs every batch.

## Context

About half of a batch's agent time went to running the full pipeline around small changes.

## Alternatives

Review every task.

## Consequences

In kb batches 32-35, 7 of 17 per-task reviews were clean and closing was 20-44% of agent time; batch 33 reviewed 8 of 11 tasks per-task against the rule.
