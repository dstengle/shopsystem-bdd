---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-core-orchestrates-and-an-adapter-never-decides-business
summary: "Every step with a business outcome (refuse, retry for the business, compensate, wait) is a core line; an adapter only translates and carries."
date: 2026-11-24
status: accepted
tier: judgement
source: [quote-75, quote-77]
---

# 0115. The core orchestrates and an adapter never decides business

## Context

Three worked examples (an ordering saga over inventory and payments, the same with swapped providers, and two stock adapters written as adapter specs) settled how a bounded context depends on another; the person accepted the shape (quote-75) and asked for the work to start (quote-77).

## Decision

Sagas are core lines over the core's own lifecycle. An adapter may emulate (a hold record, a timer, a dedupe store), never chooses an outcome the port does not declare, never compensates on its own account, and fails as broken, never refused, when the provider cannot answer. A reviewer checks each realisation line and adapter decision against this.
