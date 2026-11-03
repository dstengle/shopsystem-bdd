---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/requirement-ids-spec-integration
kind: capability-proposal
part_of: initiative/i3
status: merged
date: 2026-10-16
argues: [spec-integration]
adds: [spec-integration#r12@0.29, spec-integration#r13@0.29, spec-integration#r14@0.29, spec-integration#r15@0.29, spec-integration#r16@0.29]
changes: [spec-integration#r1@0.29]
---

# Spec integration: requirement ids

The gate shows ids, a new line takes the next free id, a changed line keeps its id, a removed line's id is
retired, the commit names the ids, and `model check` runs after apply. Implemented in
`docs/capability-format.md`, `agents/capability-writer.md`, `skills/integrating-a-proposal/SKILL.md` and
`agents/initiative-round.md`. Decisions: capability-ids-are-context-scoped, retired-ids-in-capability-frontmatter.
