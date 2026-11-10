---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/decisions-carry-their-tier
summary: "A decision file's frontmatter gives its tier, check, requirement or judgement, and for a check or requirement decision the tests or requirements that enforce it; it replaces light-decisions' list of fields."
date: 2026-11-05
status: accepted
supersedes: [design-decision/light-decisions]
tier: requirement
enforced_by: [decision-tiers#r13, decision-tiers#r14, decision-tiers#r15]
source: [record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-design]
by: "workflow simplification plan 6"
---

# 0075. Decisions carry their tier

## Decision

A decision file's frontmatter is id, summary, date, status, supersedes, revisit_when, source, by, tier and, for a
`check` or `requirement` decision, enforced_by naming the tests or the requirements that enforce it; a decision in
force gives its tier, and a superseded or rejected one needs none. It replaces 0046's list of fields.
