---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/an-adapter-is-a-nested-context-with-its-own-spec
summary: "Each adapter is adapters/<port>-<provider>/, a context of kind adapter with its own grammar, where the port's, the provider's and technical words meet."
date: 2026-11-24
status: superseded
tier: judgement
source: [quote-72, quote-75, quote-77]
---

# 0123. An adapter is a nested context with its own spec

## Context

Three worked examples (an ordering saga over inventory and payments, the same with swapped providers, and two stock adapters written as adapter specs) settled how a bounded context depends on another; the person accepted the shape (quote-75) and asked for the work to start (quote-77).

## Decision

Its id is the parent's id with /adapter/<name>. It reads the parent's port area and port contract at the parent's commit, holds its providers, its realisation lines and its adr/, and is never an area of the parent's model. Until the item that checks it is delivered this decision is a judgement; that item writes its successor at its own tier, naming its enforcer.
