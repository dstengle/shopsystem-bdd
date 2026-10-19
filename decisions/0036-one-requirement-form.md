---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/one-requirement-form
summary: "A requirement is written and read in one form only, capability/<name>#r<n>; #behaviour/r<n> is no longer accepted."
date: 2026-10-19
status: accepted
source: "the person, 2026-10-19"
---

# 0036. One requirement form

## Decision

A requirement is written `capability/<context path>/<name>#r<n>`, or its short forms, and in no other way. `#behaviour/r<n>` is not accepted: `model check` reports it as unresolved. This replaces the sentence of design-decision/capability-ids-are-context-scoped that reads both as one requirement.
