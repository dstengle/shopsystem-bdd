---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/a-port-s-outcomes-are-told-apart-by-the-core-s-statuses
summary: "A reply's meaning for a saga is told by the status of the saga's object, not by the reply."
date: 2026-11-24
status: accepted
tier: judgement
source: [quote-75, quote-77]
---

# 0121. A port's outcomes are told apart by the core's statuses

## Context

Three worked examples (an ordering saga over inventory and payments, the same with swapped providers, and two stock adapters written as adapter specs) settled how a bounded context depends on another; the person accepted the shape (quote-75) and asked for the work to start (quote-77).

## Decision

Each core line triggered by a port outcome is guarded by a status of the saga's object; two lines on one port outcome in one status clash, and spec logic reports the L1. Until the item that checks it is delivered this decision is a judgement; that item writes its successor at its own tier, naming its enforcer.
