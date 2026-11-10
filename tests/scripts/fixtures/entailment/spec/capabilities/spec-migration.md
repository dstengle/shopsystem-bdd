---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/spec-migration
title: Spec migration
narrator: the person migrating a repository onto spec/
group: guarantees
rests_on: [design-decision/one-spec-per-context, design-decision/gate-on-behaviour-lines, design-decision/migration-in-one-pass, design-decision/living-plan-to-work-items, design-decision/final-layout, design-decision/workflow-capabilities-are-guarantees]
language: codified-1
retired: [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14]
---

# Spec migration

## Purpose
**Retired in plugin 2.0.0** (design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-old-workflow-retired): every requirement of this capability is retired, and the file is kept as the record of its ids and of where its 0.29 lines went.

Takes a repository onto the final layout of design model v3 (design-decision/final-layout) in one pass,
whatever it has of the old system: design notes and approved feature files with no `spec/`, capability files
without ids, a decision ledger, top-level `decisions/`, `work/` or `records/`, `docs/superpowers/`, a living
slice plan, `@holding` scenarios. It is `migrating-to-capabilities`: the first integration where there is no
`spec/`, re-pairing the existing scenarios, and `scripts/migrate` for every mechanical change, with one gate.
It changes the meaning of no approved scenario.

## Terms

- **`migrating-to-capabilities`** (proper noun): the skill that migrates a repository on the old system to capability files, ids and the final layout.
- **glossary bullet** (noun): a bullet of an old glossary that is not in the glossary's form.
- **slice** (noun): an open slice of an old living plan.
- **backlog entry** (noun): an entry of an old backlog, or of a log, that would become an observation.
- **mechanical commit** (noun): the one commit of a migration's mechanical changes, made before its gate.
- **suite difference** (noun): a difference of the suite's summary, its passing scenarios by title or its count of scenarios per tag from those before the migration, beyond the retitles, tags and deprecations the migration sets aside.
- **rewritten file** (noun): a file other than Markdown in which the migration rewrote a path it relocated.
- **context id** (noun): the id `bounded-context/<context path>` of a migrated context.
- **old reference** (noun): a `decision/<name>` reference, a frontmatter `id` under `spec/decisions/` or `.shop/`, or an observation heading `## obs/<x>`.
- **held scenario** (noun): a scenario tagged `@holding`.
- **decision entry** (noun): an entry of an old ledger of decisions.
- **tag** (verb): a scenario is given the `@r<n>` tag of the one statement it formulates. Forms: tags, tagged. Frame: session tags scenario.

## Behaviour

## Implementation, may change
- None: retired in plugin 2.0.0.

## Not yet
- None.

## Dropped
- r1@0.29: retired with spec-migration#r1, #r2 in 2.0.0 (the-old-workflow-retired).
- r2@0.29: retired with spec-migration#r3 in 2.0.0 (the-old-workflow-retired).
- r4@0.29: retired with spec-migration#r6 in 2.0.0 (the-old-workflow-retired).
- r5@0.29: retired with spec-migration#r6 in 2.0.0 (the-old-workflow-retired).
- r6@0.29: retired with spec-migration#r7 in 2.0.0 (the-old-workflow-retired).
- r7@0.29: retired with spec-migration#r8 in 2.0.0 (the-old-workflow-retired).
- r8@0.29: retired with spec-migration#r6 in 2.0.0 (the-old-workflow-retired).
- r9@0.29: retired with spec-migration#r9 in 2.0.0 (the-old-workflow-retired).
- r10@0.29: retired with spec-migration#r4 in 2.0.0 (the-old-workflow-retired).
- r11@0.29: retired with spec-migration#r10 in 2.0.0 (the-old-workflow-retired).
- r14@0.29: retired with spec-migration#r4 in 2.0.0 (the-old-workflow-retired).
- r15@0.29: retired with spec-migration#r4 in 2.0.0 (the-old-workflow-retired).
- r16@0.29: retired with spec-migration#r3 in 2.0.0 (the-old-workflow-retired).
- r17@0.29: retired with spec-migration#r11 in 2.0.0 (the-old-workflow-retired).
- r18@0.29: retired with spec-migration#r12 in 2.0.0 (the-old-workflow-retired).
- r19@0.29: retired with spec-migration#r13 in 2.0.0 (the-old-workflow-retired).
- r20@0.29: retired with spec-migration#r6 in 2.0.0 (the-old-workflow-retired).
- r21@0.29: retired with spec-migration#r14 in 2.0.0 (the-old-workflow-retired).
- r22@0.29: retired with spec-migration#r4, #r5 in 2.0.0 (the-old-workflow-retired).
- r23@0.29: retired with spec-migration#r6 in 2.0.0 (the-old-workflow-retired).
- r26@0.29: retired with spec-migration#r3 in 2.0.0 (the-old-workflow-retired).
