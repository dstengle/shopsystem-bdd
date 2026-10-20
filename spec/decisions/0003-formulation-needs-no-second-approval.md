---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/formulation-needs-no-second-approval
summary: "Scenarios formulated from approved Behaviour lines need no approval of their own; a line with two readings returns as a question."
date: 2026-09-29
status: accepted
source: "records/archive/design-notes/2026-09-29-capability-spec-design.md; 0.8.0"
---

# 0003. Formulation needs no second approval

## Decision

A scenario formulated from an approved line is not shown for approval. A line that admits two readings gets no scenario; its question goes to the person and back through integration.

## Context

The person approves decisions, not transcription.

## Alternatives

A second gate on the feature files.

## Consequences

Formulation errors surface as hand-backs during implementation; the hand-back path exists for that.
