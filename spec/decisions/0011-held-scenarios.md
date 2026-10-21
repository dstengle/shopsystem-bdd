---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/held-scenarios
summary: "A scenario that passes today is deprecated, tagged @deprecated, when its line is re-worded or removed, and retired by the work that turns its replacement green."
date: 2026-10-11
status: accepted
source: [decision-argument/2026-10-11-green-suite-design]
by: "0.14.0"
---

# 0011. Deprecated scenarios

## Decision

Formulation runs the old scenario alone before replacing it; if it passes, `features deprecate` gives it `@deprecated`, " (deprecated)" on its title and a `Deprecated for:` line, and the scenario stays in the suite. The work-item that turns its replacement green lists it under `Retires:` and removes it with `features retire`.

## Context

Behaviour went untested between a re-worded line and the slice that built it.

## Alternatives

Replace the scenario at formulation and accept the gap.

## Consequences

Under design-model v3 a scenario names its requirement by id, so a deprecated scenario and its replacement can name the same id; i3 decides what that does to deprecation.
