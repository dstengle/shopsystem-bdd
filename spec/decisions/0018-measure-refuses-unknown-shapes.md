---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/measure-refuses-unknown-shapes
summary: "measure refuses a transcript whose shape it does not know, naming the file and what was missing, rather than guess a number."
date: 2026-10-11
status: accepted
source: [decision-argument/2026-10-11-measuring-a-batch-design]
by: "0.12.0"
---

# 0018. Measure refuses unknown shapes

## Decision

Claude Code's transcripts are not a published format. A row whose shape is unknown is refused; no number is estimated.

## Context

A wrong number in a facts file would decide a release.

## Alternatives

Best-effort parsing with warnings.

## Consequences

A harness upgrade can stop measurement until the script learns the new shape.
