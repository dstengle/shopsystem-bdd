---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/mechanisms-live-in-adapter-decisions
summary: "Transport, retry, stores, timers, webhooks and polling are decided in an adapter's adr/, never in a core or port line."
date: 2026-11-24
status: accepted
tier: judgement
source: [quote-54, quote-75, quote-77]
---

# 0124. Mechanisms live in adapter decisions

## Context

Three worked examples (an ordering saga over inventory and payments, the same with swapped providers, and two stock adapters written as adapter specs) settled how a bounded context depends on another; the person accepted the shape (quote-75) and asked for the work to start (quote-77).

## Decision

A core or port contract line names no transport, protocol, product name or storage. An adapter's realisation lines may name its own technical things (an entry, a deadline); how they are kept is an adapter decision.
