---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/a-scenario-may-name-several-requirements
summary: "A scenario names one or more requirements by @r<n> tags; every requirement is named by at least one scenario."
date: 2026-10-19
status: proposed
supersedes: design-decision/scenario-names-requirement-by-tag
source: "observation/2026-10-19-lines-not-ears; the person, 2026-10-19"
---

# 0052. A scenario may name several requirements

## Decision

A scenario names the requirements it shows by `@r<n>` tags, one or more, in the feature file of their capability. Every requirement is named by at least one scenario, and a scenario's tags are all of one capability. When a line is restructured into several EARS lines (design-decision/behaviour-lines-are-ears), its scenario names each of them and the number of scenarios does not change (the person, 2026-10-19).
