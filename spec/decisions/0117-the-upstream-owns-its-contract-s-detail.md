---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-upstream-owns-its-contract-s-detail
summary: "A downstream obtains a published contract pinned at a version and never edits it; what it needs and cannot map becomes a request."
date: 2026-11-24
status: accepted
tier: judgement
source: [quote-75, quote-77]
---

# 0117. The upstream owns its contract's detail

## Context

Three worked examples (an ordering saga over inventory and payments, the same with swapped providers, and two stock adapters written as adapter specs) settled how a bounded context depends on another; the person accepted the shape (quote-75) and asked for the work to start (quote-77).

## Decision

provider/<upstream>/<version>/ is written only by obtaining. A gap the realises check finds is raised as a request to the upstream, in the upstream's words, for the upstream to reword. Until the item that checks it is delivered this decision is a judgement; that item writes its successor at its own tier, naming its enforcer.
