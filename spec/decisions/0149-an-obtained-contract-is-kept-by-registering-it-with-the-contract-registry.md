---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/an-obtained-contract-is-kept-by-registering-it-with-the-contract-registry
summary: "spec obtain asks the contract registry to register an obtained contract for each adapter spec of its provider, at the version the adapter spec pins, and acts on each reply; no core code names where the contract is kept."
date: 2026-11-26
status: accepted
tier: requirement
enforced_by: [checking#r137, checking#r138, checking#r139, checking#r140, contract-registry#r4, checking#r142, contract-registry#r5]
verified_by: [scenario]
supersedes: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/an-obtained-contract-is-kept-in-its-provider-s-adapter-spec-checked]
---

# 0149. An obtained contract is kept by registering it with the contract registry

## Context

b735 delivered the registry's register operation in batch-134, closing the folder layout decision 0137 had obtain write itself and decision 0147's last sentence named; checking r91, which enforced 0137, is retired by r137.

## Decision

Obtaining a contract from a provider requests the contract registry's register operation once for each adapter spec that has the provider, at the version the adapter spec pins, else the version asked or published. When the registry completes the registration the specification keeps the contract; when it refuses, the specification names the adapter spec and changes nothing. Where an obtained contract is kept (the shop-folder adapter's provider/<id>/<version>/contract.toml) is the adapter's alone, as decision 0147 has it for deposits and retrievals; contract_obtain neither imports a place nor writes provider/ itself.
