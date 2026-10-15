---
id: decision/one-batch-one-session
summary: "The controller stops when a batch is archived and measured; the next batch starts in a new session."
date: 2026-10-11
status: accepted
revisit_when: "the controller's share of a measured batch's cache reads stays above 40%"
revisit_signal: measurement/kb-batches-32-35
source: "records/archive/design-notes/2026-10-11-rules-adjusted-design.md; 0.13.0"
---

# 0013. One batch one session

## Decision

When the batch is archived and measured, the controller tells the person the next batch starts in a new session that reads its plan.

## Context

One session ran kb batches 32-35; its context grew from 412k to 585k and by batch 34 it read more cache than every agent together.

## Alternatives

A controller agent per batch (proposed by the assessment as the structural fix).

## Consequences

It is asked, not structural. Under the pull model there is no controller to stop (initiative i5).
