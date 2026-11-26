---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/an-obtained-contract-is-kept-in-its-provider-s-adapter-spec-checked
summary: "spec obtain keeps an upstream's contract in each adapter spec of that provider, under the provider's whole id and the version, never at the repository root."
date: 2026-11-25
status: superseded
tier: requirement
enforced_by: [checking#r91]
verified_by: [scenario]
supersedes: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/an-obtained-contract-is-kept-in-the-adapter-spec-of-its-provider-under-the-provider-s-whole-id]
---

# 0137. An obtained contract is kept in its provider's adapter spec, checked

## Context

Decision 0136 was a judgement until b593 was delivered in batch-95.

## Decision

An obtained contract is kept in each adapter spec that names its provider, at provider/<the provider's whole id after bounded-context/>/<version>/contract.toml, and nowhere else; checking r91 (b593) enforces it.
