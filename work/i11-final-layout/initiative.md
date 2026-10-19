---
id: initiative/missingmass.io/shopsystem/shopsystem-bdd/i11
title: This repository on the final layout and conventions
summary: This repository moves to the final layout and conventions of design model v3, the ones the plugin teaches and i8 migrates consuming repositories to.
kind: capability-change
owner-level: shopsystem-bdd
status: proposed
priority: 2
source: [observation/2026-10-19-final-state-only]
date: 2026-10-19
---

Covers:
- decisions as `spec/decisions/<n>-<slug>.md`, with a generated index;
- work and records under `.shop/`;
- decisions in the light form: a summary and a Decision section, with Context and Alternatives only for a
  real trade-off;
- ids in place of paths in references: `formulated_as` derived, and `source:` naming record ids;
- a plain label for every model rule, printed by `model check` and used by spec lines and skills;
- "deprecated" in place of held, holding and superseded (the person, 2026-10-19): the tag `@deprecated`,
  `features deprecate` and `features deprecated` for `hold` and `holding`, a `Deprecated for:` line,
  design-decision/held-scenario-formulates-no-requirement reworded, and the glossary entry **deprecated
  scenario** (Not: held, holding, superseded);
- "hold" and "carry" in their other senses reworded in plain words (stays valid, has, contains, enforced
  by, do), with carry added to the Not: lists;
- this repository's scenarios run as pytest-bdd step definitions (design-decision/plugin-scenarios-run-as-unittest
  was rejected 2026-10-19).
