---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/tracking-and-execution-are-one-work-management-context-with-two-modules
summary: "Work tracking and work execution share one meaning of item, so they are one bounded context with two modules, tracking owning the item's lifecycle; a split waits on a second tracker or executor."
date: 2026-11-25
status: accepted
tier: judgement
source: [quote-86]
---

# 0133. Tracking and execution are one work management context with two modules

## Context

The disentangling worked example walked a split of tracking out of execution through a port supply and the word assignment; asked whether the split has value, the language test found item means the same in both.

## Decision

Work tracking and work execution are one bounded context of the work management subdomain, with two modules. The tracking module owns the lifecycle of an item and of a request: the execution module changes them only through tracking's operations, never by writing their files. No driven port, adapter or word of execution's own (such as assignment) stands between them. The split into two contexts is taken up when execution must work from another tracker, or tracking must feed another executor.

## Alternatives

Two bounded contexts now, with the supply port, assignment and an in-process adapter: rejected as more machinery than one shop and one language need; kept as the path for when a second tracker or executor appears.
