---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-port-contract-is-the-downstream-s-and-bounded-by-the-core
summary: "A port holds only what core lines use, and each port line names the core lines that rely on it."
date: 2026-11-24
status: accepted
tier: judgement
source: [quote-75, quote-77]
---

# 0116. The port contract is the downstream's and bounded by the core

## Context

Three worked examples (an ordering saga over inventory and payments, the same with swapped providers, and two stock adapters written as adapter specs) settled how a bounded context depends on another; the person accepted the shape (quote-75) and asked for the work to start (quote-77).

## Decision

A port operation no core line requests, a port outcome that no core line handles and no port line excludes, and a port line whose Relied on by names no core line requesting that port are findings of the bound check. Until the item that checks it is delivered this decision is a judgement; that item writes its successor at its own tier, naming its enforcer.
