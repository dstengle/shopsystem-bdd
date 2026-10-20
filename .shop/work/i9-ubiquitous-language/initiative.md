---
id: initiative/missingmass.io/shopsystem/shopsystem-bdd/i9
title: A ubiquitous language for the bounded context
summary: A context's terms are standing glossary entries that model check judges, a skill checks a spec's consistency on demand, model finds clingo behind a virtualenv, and features takes --file.
kind: capability-change
owner-level: shopsystem-bdd
status: started
priority: 8
source: [observation/2026-10-15-design-model-v3]
date: 2026-10-17
---

Design: .shop/records/archive/design-notes/2026-10-17-type-first-ids-and-ubiquitous-language-design.md, Part 2.

Reaches: `spec/index.md`'s Glossary; design-model-check (glossary entries as terms, `v_t1` to `v_t3`, the clingo
search), feature-file-tools (`--file`), spec-integration (a term rides with its capability-proposal and the
commit names terms), formulation (a scenario follows a term), and a new capability, spec-consistency (its
scenarios come as fixture sessions with i4: design-decision/workflow-scenarios-run-as-fixture-sessions).
One capability-proposal per capability, `capability-proposal/ubiquitous-language-<capability>`. Released as 0.20.0.

Decisions: design-decision/glossary-terms-are-standing, design-decision/consistency-check-on-demand.
Not in this release: the check wired into rounds; seam translations between contexts' terms; stemming beyond a
plural "s"; checking step text against definitions.
