---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/an-upstream-s-may-outcomes-are-handled-downstream-as-when-or-if-lines
summary: "Every outcome an upstream may give on an operation the downstream requests reaches a core line through the port, or is shown unreachable; may lines are a stub's allowed replies, scenarios choose which happens."
date: 2026-11-24
status: accepted
tier: judgement
source: [quote-79]
---

# 0127. An upstream's may outcomes are handled downstream as When or If lines

## Context

The adapter design left open whether a port's stub produces may outcomes on its own; the person agreed that every upstream may becomes a When or an If downstream.

## Decision

For each operation a downstream requests, every outcome the upstream may give is translated by a realisation line into a port outcome or into broken, and every port outcome has a core line triggered on it (When for an outcome or a notification, If for a refusal) in each status the requesting object can be in while the request is outstanding. Exceptions are checked, never assumed: an operation the downstream never requests is ignored; an outcome the downstream cannot provoke is shown unreachable by entailment from its core lines; an upstream notification the downstream does not subscribe to is a warning. A port's may lines are the allowed replies of its generated stub; each scenario chooses the reply; the outcome check makes the set complete. Until that check is delivered this decision is a judgement; its item writes its successor at its own tier.
