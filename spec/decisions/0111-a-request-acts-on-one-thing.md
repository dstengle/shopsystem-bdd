---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/a-request-acts-on-one-thing
summary: "The object slot of a request, a verb naming an operation, takes one thing's noun phrase, so that one verb's frames on a container and on the service's collection read one way each."
date: 2026-11-20
status: accepted
tier: judgement
source: [quote-63]
---

# 0111. A request acts on one thing

## Context

b420 (quote-63): 'list a checklist' (one container) and 'list the checklists' (the service's collection) are two operations of one verb; with a plural allowed in the first frame's object slot, 'lists the checklists' read two ways and the trial coined the verb browse.

## Decision

A request's object is one thing: grammar 4 gives a request's object slot no plural, quantified or counted noun phrase. A collection a request acts on is said by its frame's fixed words ('lists the checklists', 'lists the characters of a note'); one request on several objects is several requests. Frames of verbs naming no operation keep their plurals.

## Alternatives

The exact fixed words win over a reading through an object slot (a tie-break in spec_meaning): smaller, but a special case leaving other collisions. Guidance only: the line stays refused.
