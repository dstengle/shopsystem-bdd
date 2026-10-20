---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/held-scenarios
summary: "A scenario that passes today is held, tagged @holding, when its line is re-worded or removed, and retired by the slice that turns its replacement green."
date: 2026-10-11
status: accepted
source: "records/archive/design-notes/2026-10-11-green-suite-design.md; 0.14.0"
---

# 0011. Held scenarios

## Decision

Formulation runs the old scenario alone before replacing it; if it passes it gains `@holding`, " (held)" on its title and a `Held for:` line, and stays in the suite. The task that turns its replacement green lists it under `Retires:` and removes it with `features retire`.

## Context

Behaviour went untested between a re-worded line and the slice that built it.

## Alternatives

Replace the scenario at formulation and accept the gap.

## Consequences

Under design-model v3 a scenario names its requirement by id, so a held scenario and its replacement can name the same id; i3 decides what that does to holding.
