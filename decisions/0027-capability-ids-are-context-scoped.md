---
id: decision/capability-ids-are-context-scoped
summary: "A capability's id is <context>/<name>; this context is shopsystem-bdd."
date: 2026-10-15
status: proposed
source: "docs/design-model/grammar.md v3 section 6 (CAP = CTX '/' NAME)"
---

# 0027. Capability ids are context scoped

## Decision

The capability `spec/capabilities/<name>.md` has id `shopsystem-bdd/<name>`; a requirement is `shopsystem-bdd/<name>#r<n>`. Inside this context `<name>#r<n>` is accepted as a reference.

## Context

The grammar's CAP is context-qualified; the format kb uses (`capability/<name>`) is not.

## Alternatives

Keep `capability/<name>`.

## Consequences

Consuming repositories move to the same form through i3.
