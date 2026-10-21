---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/a-scenario-names-one-requirement
summary: "A scenario names exactly one requirement by its @r<n> tag; a requirement has at least one scenario; scenarios share step definitions in code."
date: 2026-10-21
status: accepted
supersedes: design-decision/a-scenario-may-name-several-requirements
source: [observation/2026-10-21-one-requirement-per-scenario]
by: "the person, 2026-10-21"
---

# 0054. A scenario names one requirement

## Decision

A scenario names exactly one requirement, by one `@r<n>` tag in its capability's feature file, and shows that requirement's response; a requirement has at least one scenario. Scenarios that need the same setup or check share step definitions in code; that sharing is an implementation choice and never puts two requirements in one scenario.
