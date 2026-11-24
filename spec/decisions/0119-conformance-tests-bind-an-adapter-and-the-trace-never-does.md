---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/conformance-tests-bind-an-adapter-and-the-trace-never-does
summary: "An adapter is accepted by passing the port contract's scenarios with its provider; its trace is evidence and impact analysis only."
date: 2026-11-24
status: accepted
tier: judgement
source: [quote-75, quote-77]
---

# 0119. Conformance tests bind an adapter and the trace never does

## Context

Three worked examples (an ordering saga over inventory and payments, the same with swapped providers, and two stock adapters written as adapter specs) settled how a bounded context depends on another; the person accepted the shape (quote-75) and asked for the work to start (quote-77).

## Decision

Every adapter of a port runs the same conformance scenarios. No declarative operation mapping binds an adapter: a table mapping port operations one to one onto upstream operations is not adopted. Until the item that checks it is delivered this decision is a judgement; that item writes its successor at its own tier, naming its enforcer.
