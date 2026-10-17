---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/scenario-names-requirement-by-tag
summary: "An acceptance-scenario names its requirement with a tag @r<n> in its capability's own feature file."
date: 2026-10-15
status: proposed
source: "docs/design-model/design-model.md v3 section 2; grammar.md v3 rule 15"
---

# 0023. Scenario names requirement by tag

## Decision

A scenario carries exactly one tag `@r<n>`; the feature file it sits in is its capability's (`formulated_as`), so the tag resolves to `<capability>#r<n>`. Its title is free.

## Context

v3 says a scenario names its requirement by id and leaves the spelling to the files.

## Alternatives

A `# r3` comment line; the id in the title; a `@<capability>#r3` tag (`#` is awkward inside Gherkin tags).

## Consequences

pytest-bdd turns `@r3` into a marker, so `-m r3` runs a requirement's scenarios. Titles stop being the link, so `features rebind` loses most of its reason (i3).
