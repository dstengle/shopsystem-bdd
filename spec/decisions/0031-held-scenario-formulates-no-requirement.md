---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/held-scenario-formulates-no-requirement
summary: "A held scenario keeps the @r<n> tag it had, as the trace of the line it was, and is no acceptance-scenario: model check reads it as none."
date: 2026-10-16
status: accepted
source: "work/i3-requirement-ids/initiative.md (its open question); design-decision/held-scenarios"
---

# 0031. A held scenario formulates no requirement

## Decision

When a line is changed or removed and its old scenario is held (design-decision/held-scenarios), the held scenario keeps its `@r<n>` tag. `@holding` says it formulates no line, so `scripts/model` does not read it as an acceptance-scenario: it neither covers the requirement nor counts as a second scenario of it, and a held scenario whose id was retired is not a dangling reference.

## Context

i3 left open what holding does when a held scenario and its replacement name the same id. A changed line keeps its id, so both carry it; a removed line's id is retired, so the held scenario names an id no line has.

## Alternatives

Strip the tag on hold (the trace of which line it was is lost, and `features holding` cannot show it); a separate tag such as `@was-r<n>` (a second spelling of one id).

## Consequences

`features hold` changes nothing about tags but adding `@holding`, as today.
