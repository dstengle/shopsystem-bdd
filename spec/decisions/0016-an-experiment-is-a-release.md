---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/an-experiment-is-a-release
summary: "One change to the workflow per release, run on a real batch and compared with the batch before."
date: 2026-10-11
status: accepted
source: [decision-argument/2026-10-11-measuring-a-batch-design]
by: "0.12.0"
---

# 0016. An experiment is a release

## Decision

Each version changes one thing; a batch runs on it; `measure compare` sets it against the batch before. Removals count as changes.

## Context

Rules were added after single fixture runs and never removed.

## Alternatives

Change several rules per release and judge the whole.

## Consequences

Six releases (0.13-0.18) have not been measured on a batch; the assessment's first recommendation is a baseline batch on 0.18.0.
