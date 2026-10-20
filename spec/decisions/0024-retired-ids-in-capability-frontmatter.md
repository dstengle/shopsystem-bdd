---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/retired-ids-in-capability-frontmatter
summary: "A capability's retired requirement ids are listed in its frontmatter as retired: [r<n>, ...]."
date: 2026-10-15
status: accepted
by: "docs/design-model/design-model.md v3 section 2 ('retired ids kept in the capability's ledger')"
---

# 0024. Retired ids in capability frontmatter

## Decision

`retired:` in the capability's frontmatter is its ledger of ids used and removed. A removed requirement's id joins it when the proposal that removes it is merged.

## Context

v3 keeps retired ids in "the capability's ledger" without naming where.

## Alternatives

A `## Retired` section; the ids only in git history.

## Consequences

`model check` reads it as `retired_id` and v15c refuses an id reused from it.
