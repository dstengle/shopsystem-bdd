---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/assumed-provider-lines-are-evidence-only-when-run
summary: "A provider description that is not a published contract is checked only by running its scenarios against the provider, on a schedule."
date: 2026-11-24
status: accepted
tier: judgement
source: [quote-75, quote-77]
---

# 0120. Assumed provider lines are evidence only when run

## Context

Three worked examples (an ordering saga over inventory and payments, the same with swapped providers, and two stock adapters written as adapter specs) settled how a bounded context depends on another; the person accepted the shape (quote-75) and asked for the work to start (quote-77).

## Decision

Static checks over assumed lines show only that the adapter agrees with what its owners believe. Every assumed line has a scenario; its schedule and target (a sandbox, staging) are an adapter decision.
