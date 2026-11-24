---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/relied-on-by-is-written-only-where-the-bound-check-cannot-see-the-reliance
summary: "A port line carries Relied on by only when no core line's text shows the reliance; the bound check computes it for the others and names each port line that needs one."
date: 2026-11-24
status: accepted
tier: judgement
source: [quote-78]
---

# 0126. Relied on by is written only where the bound check cannot see the reliance

## Context

The port contract's lines rest on core lines in two ways, one a tool can see and one it cannot; the person agreed the citation only where a tool cannot see it.

## Decision

A port line that excludes an outcome no core line handles is relied on by the core lines that request its operation, and the bound check computes that. A port line whose reliance rests on meaning or on how the core is built (idempotency for the core's retries, securing a charge moving no money) carries Relied on by: <core ids>, written unindented on the line after it as Restates: is. The bound check names each port line that needs the citation and has none. Until that check is delivered this decision is a judgement; its item writes its successor at its own tier.
