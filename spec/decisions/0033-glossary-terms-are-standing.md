---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/glossary-terms-are-standing
summary: "A bounded context's terms are glossary entries in spec/index.md, standing nodes approved at the gate like Behaviour lines and judged by model check."
date: 2026-10-17
status: accepted
source: [decision-argument/2026-10-17-type-first-ids-and-ubiquitous-language-design]
by: "Part 2"
---

# 0033. Glossary terms are standing

## Decision

Each bullet of `spec/index.md`'s Glossary, `- **<term>**: <definition>. Not: <word>, <word>.`, is a term of the bounded context with the id `term/<context path>/<term>`. A term is approved at the gate like a Behaviour line; renaming one is removing one and adding another. `model check` judges requirements and scenarios against the terms and the words they avoid (`v_t1` to `v_t3`).

## Context

The glossary was prose no tool read, so one thing could carry two names across capabilities without anything noticing.

## Alternatives

A glossary kept as prose, judged only by a reviewing agent (no word is ever refused mechanically); terms as files under `decisions/` (a second place for what the index already holds).

## Consequences

A term change rides with a capability-proposal (`adds: [term/<name>]`) and the spec commit names terms added, changed and removed. Meaning stays a judgment, made by the `spec-checker` agent; only the avoided words are checked mechanically.
