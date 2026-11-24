---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/a-port-line-is-met-when-realisation-and-provider-lines-entail-it
summary: "A port line is satisfied when the adapter's realisation lines and its provider's lines together entail it, following each request the adapter makes."
date: 2026-11-24
status: accepted
tier: judgement
source: [quote-75, quote-77]
---

# 0118. A port line is met when realisation and provider lines entail it

## Context

Three worked examples (an ordering saga over inventory and payments, the same with swapped providers, and two stock adapters written as adapter specs) settled how a bounded context depends on another; the person accepted the shape (quote-75) and asked for the work to start (quote-77).

## Decision

The realises check runs entailment with request-following premises. A port line the adapter realises that is not entailed is a finding naming the provider line where the chain stops; one entailed by realisation lines alone, with no provider premise behind a provider request, is reported as claimed, not backed. Until the item that checks it is delivered this decision is a judgement; that item writes its successor at its own tier, naming its enforcer.
