---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/a-shop-is-a-management-and-execution-unit-that-hosts-bounded-contexts
summary: "A shop is the unit work is managed and executed in, configured in .shop, and maps to no DDD concept; a bounded context's id is under the product, not under the shop."
date: 2026-11-25
status: accepted
tier: judgement
source: [quote-82]
---

# 0129. A shop is a management and execution unit that hosts bounded contexts

## Context

The disentangling worked example asked whether hosted contexts get ids nested under the shop or flat under the product (Q1).

## Decision

A shop is a management and execution unit, not a bounded context: it may host any number of bounded contexts, and its contents (the contexts it hosts) are configured in .shop. A bounded context's id is related to the product only (flat under the product), never nested under the shop that hosts it, so a context moves between shops without a new id.

## Alternatives

Ids nested under the shop: rejected, a context's id would change when it moves to another shop.
