---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/held-scenario-formulates-no-requirement
summary: "A deprecated scenario keeps the @r<n> tag it had, as the trace of the line it was, and is no acceptance-scenario: model check reads it as none."
date: 2026-10-16
status: accepted
source: [initiative/i3, design-decision/held-scenarios]
by: "(its open question)"
---

# 0031. A deprecated scenario formulates no requirement

## Decision

When a line is changed or removed and its old scenario is deprecated (design-decision/held-scenarios), the deprecated scenario keeps its `@r<n>` tag. `@deprecated` says it formulates no line, so `scripts/model` does not read it as an acceptance-scenario: it neither covers the requirement nor counts as a second scenario of it, and a deprecated scenario whose id was retired is not a dangling reference.

## Context

i3 left open what deprecation does when a deprecated scenario and its replacement name the same id. A changed line keeps its id, so both have it; a removed line's id is retired, so the deprecated scenario names an id no line has.

## Alternatives

Strip the tag on deprecation (the trace of which line it was is lost, and `features deprecated` cannot show it); a separate tag such as `@was-r<n>` (a second spelling of one id).

## Consequences

`features deprecate` changes nothing about tags but adding `@deprecated`.
