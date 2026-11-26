---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/an-adapter-spec-records-the-provider-operations-each-port-operation-uses-checked
summary: "For each port operation an adapter spec names, in its uses:, the set of provider operations used to realise it, of one provider or several; spec check holds them to the held contracts and a job's trace follows each into its provider's requirements."
date: 2026-11-26
status: accepted
tier: requirement
enforced_by: [checking#r135, checking#r136, product#r35]
verified_by: [scenario]
supersedes: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/an-adapter-spec-records-the-provider-operations-each-port-operation-uses]
---

# 0148. An adapter spec records the provider operations each port operation uses, checked

## Context

b637 delivered it in batch-133; decision 0138 was its judgement-tier forerunner.

## Decision

An adapter spec records, as data, which provider operations are used to realise each port operation: its uses: list, one entry a port operation and a provider operation (of a provider when it has several), several entries of one port operation its set, of one provider or several, and a provider operation may be used by several port operations; never one port operation to one provider operation. spec check fails an adapter spec one of whose provider operations no contract it holds declares, and one with a port operation it realises that uses no operation; a job's trace follows each provider operation used into the requirements the held contract lists under it.
