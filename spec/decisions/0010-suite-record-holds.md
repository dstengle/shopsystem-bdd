---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/suite-record-holds
summary: "A whole-suite run is recorded once in the plan's log and stands while nothing outside the plans directory has changed since its commit."
date: 2026-10-07
status: accepted
by: "0.10.0 (72d33af)"
---

# 0010. Suite record holds

## Decision

`Suite: <N> passed, <M> failed[, <X> expected] at <hash> in <s> s`. Whoever needs the suite's result and finds a record that holds uses it. `plan show --last-suite --current` says whether it holds.

## Context

One 0.9.0 session ran a 100-206 s suite about 34 times.

## Alternatives

Run the suite at the start and end of every slice.

## Consequences

Installing a dependency without a commit makes every record stale.
