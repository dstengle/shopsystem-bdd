---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/feature-files-read-only-in-red-green
summary: "The implementer never edits a feature file; a wrong scenario is a stop condition and a hand-back, never a fix."
date: 2026-09-22
status: accepted
source: [decision-argument/2026-09-22-bdd-workflow-design]
---

# 0006. Feature files read only in red green

## Decision

Under bdd-red-green no `.feature` file is opened for writing; the one exception is `features retire` of a deprecated scenario the task lists under `Retires:`. A stop condition is observed by a test run, and handing back means a HAND-BACK log entry, a commit of what exists, and a report.

## Context

An implementer that corrects a Then line it reads as a typo has changed the approved contract.

## Alternatives

Let the implementer fix obvious typos and flag them.

## Consequences

Slicing decides whether the contract changes; only formulation writes features.
