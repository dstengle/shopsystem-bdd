---
id: decision/spec-writers-blind-to-code
summary: "The capability-writer and feature-formulator read only spec/, features/ and the brief's notes, and write only drafts."
date: 2026-09-27
status: accepted
source: "records/archive/design-notes/2026-09-22-bdd-workflow-design.md; 0.7.0 (a53d21b); 0.10.0"
---

# 0004. Spec writers blind to code

## Decision

The agents that write the spec and the feature files have Read, Glob, Grep and Write, a path list in their brief that excludes source and tests, and a drafts directory as their only write target.

## Context

Given the code, a writer describes what it does; given only the spec, what the narrator needs.

## Alternatives

A general-purpose agent asked not to look.

## Consequences

The restriction is structural for edit and shell tools; the path list is still asked, not enforced.
