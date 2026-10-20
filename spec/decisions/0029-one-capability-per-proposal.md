---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/one-capability-per-proposal
summary: "A capability-proposal argues exactly one capability; a capability-change initiative may have several, each passing the gate and reaching formulated on its own."
date: 2026-10-16
status: accepted
source: [observation/2026-10-15-proposal-argues-many]
by: "the person, 2026-10-16"
---

# 0029. One capability per proposal

## Decision

A capability-proposal argues exactly one capability. An initiative of kind capability-change may have several first parts, all capability-proposals; initiatives of other kinds keep one first part. A first spec, or any change touching several capabilities, is one initiative with one proposal per capability. `scripts/model.lp` checks both, with FIX notes against grammar.md v3 (g:72 `argues` 1..n; g:171 v_k5 one first part); the grammar text is the person's to change.

## Context

design-model.md v3 says a capability-proposal argues one capability, while grammar.md's edge table allows `argues` 1..n and v_k5 gives an initiative one first part. i1, this repository's first spec, was one proposal arguing thirteen capabilities, so no capability could pass the gate or reach `formulated` without the others. i3 touches four capabilities and meets the same choice.

## Alternatives

One migration proposal arguing many capabilities, as a stated exception; one initiative per capability, which splits one piece of work across thirteen ranked intake rows.

## Consequences

i1 has thirteen proposals, `capability-proposal/first-spec-<capability>`. A capability whose question is open (how workflow capabilities get scenarios) no longer delays the script capabilities.
