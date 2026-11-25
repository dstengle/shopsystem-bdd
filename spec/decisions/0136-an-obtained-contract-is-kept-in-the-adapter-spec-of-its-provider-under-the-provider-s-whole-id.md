---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/an-obtained-contract-is-kept-in-the-adapter-spec-of-its-provider-under-the-provider-s-whole-id
summary: "spec obtain keeps a provider's contract inside the adapter spec that names the provider, at provider/<the provider's id after bounded-context/>/<version>/contract.toml, never at the repository root nor keyed by the id's last word."
date: 2026-11-25
status: accepted
tier: judgement
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/an-adapter-is-a-nested-context-with-its-own-spec-checked]
source: [item/missingmass.io/shopsystem/shopsystem-bdd/b593]
---

# 0136. An obtained contract is kept in the adapter spec of its provider, under the provider's whole id

## Context

spec obtain (b587) keeps a contract at provider/<last word of the id>/<version>/ at the repository root, a stopgap until adapter specs existed. b540 delivered adapter specs, which hold their providers' contracts under provider/<upstream>/<version>/contract.toml (decision 0135, checking r86). Two upstreams whose ids end in the same word would share one folder.

## Decision

An obtained contract is kept in the adapter spec whose providers: names the bounded context it was obtained from, at provider/<the provider's whole id after bounded-context/>/<version>/contract.toml under that adapter spec's folder, where the adapter spec's provider check reads it. Nothing is kept at the repository root. This is a judgement until b593 is delivered; b593 writes its successor at requirement tier, enforced by its checking line.

## Alternatives

The repository-root provider/ folder keyed by the id's last word (b587): two upstreams can collide and the adapter spec does not read it. A cache outside the repository: the contract an adapter relies on would not be reviewed with it.
