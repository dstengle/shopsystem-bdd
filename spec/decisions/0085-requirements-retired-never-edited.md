---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/requirements-retired-never-edited
summary: "A requirement is never edited in place nor overridden by another; a changed requirement is a new id, and the old id goes to the capability's `retired:`."
date: 2026-11-05
status: accepted
tier: judgement
source: [initiative/missingmass.io/shopsystem/shopsystem-bdd/i39]
by: "the person's ruling on i39, 2026-10-27"
---

# 0085. Requirements are retired, never edited

## Context

The integrate round of i39 drafted Behaviour lines "changed" in place (r3) and standalone lines that overrode the
table rows r115 and r117. A requirement id is cited by requests' resolutions, scenarios, items and decisions; a line
changed under its id changes what each of those citations means without any of them knowing.

## Decision

A requirement under `spec/`, a Behaviour line or a numbered table row, is never edited in place, and no requirement
overrides or edits another. To change one, write its replacement with a new id and put the original's id in the
capability's `retired:` list.

## Alternatives

- Editing a line under its id with the change in git history: every citation of the id silently changes meaning.
- A later line that overrides an earlier one: two lines then hold for the same case and the reader must know which
  wins.
