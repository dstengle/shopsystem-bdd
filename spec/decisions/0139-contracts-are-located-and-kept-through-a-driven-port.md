---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/contracts-are-located-and-kept-through-a-driven-port
summary: "Where a published or obtained contract is kept, and how one is found, is an adapter's mechanism behind a driven port of the specification; no line or core code names a file location."
date: 2026-11-25
status: accepted
tier: judgement
source: [quote-94]
---

# 0139. Contracts are located and kept through a driven port

## Context

The notes product worked example proposed one folder per shop for published contracts; the person said locating contracts must go through a port and adapter because the mechanism will change early.

## Decision

Publishing, fetching and obtaining a contract request a driven port of the specification (a contract registry in the context's terms); where contracts are kept and how they are located (a folder of the shop, another repository, a registry service) is an adapter of that port, chosen as a technical architecture decision (0125) and described in its adapter decisions (0124). Requirement lines and the core never name a path. Until the item that delivers the port is delivered this decision is a judgement; that item writes its successor at its own tier.

## Alternatives

A fixed folder layout in the core (.shop/contracts/<context>/<version>/, provider/<id>/<version>/): rejected, the mechanism is expected to change.
