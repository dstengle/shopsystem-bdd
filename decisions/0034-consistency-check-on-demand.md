---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/consistency-check-on-demand
summary: "The spec consistency check runs when the person asks for it; integration and formulation rounds do not run it."
date: 2026-10-17
status: proposed
revisit_when: "a measured batch shows drift the on-demand check would have caught"
source: "docs/superpowers/specs/2026-10-17-type-first-ids-and-ubiquitous-language-design.md, Part 2"
---

# 0034. The consistency check runs on demand

## Decision

`checking-spec-consistency` runs when the person asks for it. Integration and formulation rounds do not dispatch it.

## Context

The check costs one agent dispatch for each capability and one for the whole context. Wired into every round it would add that cost to a workflow whose changes are judged on measured batches, and its worth is not yet measured.

## Alternatives

Run it at the end of every integration round (cost on every change, unmeasured); run it only at release (the drift is found late).

## Consequences

Drift is found when someone asks. `model check`'s `v_t*` rows still run in every round that runs `model check`.
