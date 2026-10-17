---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/model-reads-a-ledger
summary: "Where a repository keeps its decisions as a ledger in spec/decisions.md and has no decisions/ directory, model reads each ## design-decision/<slug> heading as a design-decision."
date: 2026-10-16
status: proposed
source: "work/i3-requirement-ids/initiative.md; docs/capability-format.md (the decisions file)"
---

# 0032. Model reads a ledger

## Decision

`scripts/model` reads `decisions/*.md` when that directory exists. Where it does not, it reads `spec/decisions.md` as the ledger `docs/capability-format.md` teaches: each `## design-decision/<slug>` heading is a design-decision, so a capability's `rests_on` resolves.

## Context

0.19.0 brings `model check` to consuming repositories, whose decisions are a ledger today. Decisions as files is a later release, so the check must read the form they have.

## Alternatives

Ship decisions as files in the same release (two workflow changes in one, against design-decision/an-experiment-is-a-release); leave `rests_on` unresolved in consuming repositories (every capability reported).

## Consequences

Removed when consuming repositories move to `decisions/` files.
