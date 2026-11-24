---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/which-adapter-is-wired-in-is-a-technical-architecture-decision
summary: "A downstream records which adapter of a port it runs as a technical architecture decision; it may start hard-wired and later be made configuration."
date: 2026-11-24
status: accepted
tier: judgement
source: [quote-76, quote-77]
---

# 0125. Which adapter is wired in is a technical architecture decision

## Context

Three worked examples (an ordering saga over inventory and payments, the same with swapped providers, and two stock adapters written as adapter specs) settled how a bounded context depends on another; the person accepted the shape (quote-75) and asked for the work to start (quote-77).

## Decision

The choice of adapter for a port is not a requirement line. It is recorded as a decision of the downstream (an adr), first hard-wired in code; moving it to configuration is a later decision of its own.
