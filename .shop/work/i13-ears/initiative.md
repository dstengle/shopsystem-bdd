---
id: initiative/missingmass.io/shopsystem/shopsystem-bdd/i13
title: Requirements in EARS
summary: Every Behaviour line in this context is written in EARS's patterns with "shall", one response and one sentence, and model check reports a line that is not.
kind: capability-change
owner-level: shopsystem-bdd
status: proposed
priority: 0
source: [observation/2026-10-19-lines-not-ears]
date: 2026-10-19
---

Ahead of everything else (the person, 2026-10-19). design-decision/behaviour-lines-are-ears.

Covers:
- `model check`, formulation and the feature-file tools accepting a scenario that names several requirements;
- `model check` reports a Behaviour line that is not in an EARS pattern, or that has more than one "shall"
  or more than one sentence;
- docs/capability-format.md, the capability-writer, the feature-formulator and the spec-checker teach and
  check the strict form;
- every capability's Behaviour lines restructured to it, not only given a "shall": each line's pattern chosen
  by what starts the behaviour (a command or input: When; a refusal or fault: If … then; a period: While;
  an option: Where; no trigger: ubiquitous), one response per line, `If` lines only where design-decision/behaviour-lines-are-ears allows them, the capabilities not yet built cut to walking skeletons, the drafted lines of i10, i11 and i8 included: a line
  whose meaning is unchanged keeps its id; a line split in two keeps its id for one part and takes a new id
  for the other, named by the old line's scenario, so the number of scenarios does not change
  (design-decision/a-scenario-may-name-several-requirements); a form or data shape is written as what the named system shall do
  with it.

After the migration release: the strict form goes back to the design model in shopsystem-knowledge
(initiative/i14).
