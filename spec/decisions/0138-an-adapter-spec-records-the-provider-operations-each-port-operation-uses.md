---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/an-adapter-spec-records-the-provider-operations-each-port-operation-uses
summary: "For each port operation an adapter spec names the set of provider operations used to realise it, of one provider or several; the relation is many-to-many, never one port operation to one provider operation."
date: 2026-11-25
status: superseded
tier: judgement
source: [quote-93]
---

# 0138. An adapter spec records the provider operations each port operation uses

## Context

The notes product worked example found traces stopping at the adapter because only prose in its adapter decisions said which provider operations it calls; the person rejected a one-to-one mapping.

## Decision

An adapter spec records, as data, which provider operations are used to realise each port operation: a set, possibly of several providers, and a provider operation may be used by several port operations. Its realisation lines say how they are combined; a trace follows every provider operation used. Until the item that checks it is delivered this decision is a judgement; that item writes its successor at its own tier, naming its enforcer.

## Alternatives

One provider operation per port operation: rejected, adapters combine several calls, of several providers, and sagas exist (quote-71's concern).
