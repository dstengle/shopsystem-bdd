---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/one-spec-per-context
summary: "A bounded context has one spec: spec/index.md, the decisions, and one file per capability, each paired by name with one feature file."
date: 2026-09-29
status: accepted
source: [decision-argument/2026-09-29-capability-spec-design]
by: "0.8.0 (d034b50)"
---

# 0001. One spec per context

## Decision

A bounded context has one spec. A later note is integrated into it; it never starts a second spec. Each capability `spec/capabilities/<name>.md` is formulated as `features/<name>.feature`, paired by name.

## Context

Before 0.8.0 each design note produced its own feature files, and a reader had to merge notes to learn what the system does.

## Alternatives

A spec per note, merged at read time; one spec document per context, not split by capability.

## Consequences

Integration is a merge into existing files. Migration (`migrating-to-capabilities`) is the first integration.
