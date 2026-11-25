---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/a-third-party-provider-is-a-bounded-context-of-the-domain-map-that-no-shop-hosts
summary: "An outside provider appears in the product's domain map as a bounded context addressing a subdomain (generic as a rule), hosted by no shop, its contract held in the adapter specs that use it."
date: 2026-11-25
status: accepted
tier: judgement
source: [quote-95]
---

# 0143. A third-party provider is a bounded context of the domain map that no shop hosts

## Context

The notes product's storage and payments providers had no place in the domain map, so subdomains they address looked unaddressed.

## Decision

The domain map lists each third-party provider a context depends on as a bounded context with no shop, with the subdomain it addresses; its contract is the one its adapter specs hold (pinned or assumed, decision 0120), obtained through the contract registry port (0139). Until the item that checks it is delivered this decision is a judgement; that item writes its successor at its own tier, naming its enforcer.
