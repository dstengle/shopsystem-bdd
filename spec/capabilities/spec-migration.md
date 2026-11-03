---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/spec-migration
title: Spec migration
narrator: the person migrating a repository onto spec/
group: guarantees
rests_on: [design-decision/one-spec-per-context, design-decision/gate-on-behaviour-lines, design-decision/migration-in-one-pass, design-decision/living-plan-to-work-items, design-decision/final-layout, design-decision/workflow-capabilities-are-guarantees]
language: codified-1
retired: []
---

# Spec migration

## Purpose
Takes a repository onto the final layout of design model v3 (design-decision/final-layout) in one pass,
whatever it has of the old system: design notes and approved feature files with no `spec/`, capability files
without ids, a decision ledger, top-level `decisions/`, `work/` or `records/`, `docs/superpowers/`, a living
slice plan, `@holding` scenarios. It is `migrating-to-capabilities`: the first integration where there is no
`spec/`, re-pairing the existing scenarios, and `scripts/migrate` for every mechanical change, with one gate.
It changes the meaning of no approved scenario.

## Terms

- **`migrating-to-capabilities`** (actor): the skill that migrates a repository on the old system to capability files, ids and the final layout.
- **glossary bullet** (kind): a bullet of an old glossary that is not in the glossary's form.
- **slice** (kind): an open slice of an old living plan.
- **backlog entry** (kind): an entry of an old backlog, or of a log, that would become an observation.
- **mechanical commit** (kind): the one commit of a migration's mechanical changes, made before its gate.
- **suite difference** (kind): a difference of the suite's summary, its passing scenarios by title or its count of scenarios per tag from those before the migration, beyond the retitles, tags and deprecations the migration sets aside.
- **rewritten file** (kind): a file other than Markdown in which the migration rewrote a path it relocated.
- **context id** (kind): the id `bounded-context/<context path>` of a migrated context.
- **old reference** (kind): a `decision/<name>` reference, a frontmatter `id` under `spec/decisions/` or `.shop/`, or an observation heading `## obs/<x>`.
- **held scenario** (kind): a scenario tagged `@holding`.
- **decision entry** (kind): an entry of an old ledger of decisions.
- **tag** (event): a scenario is given the `@r<n>` tag of the one statement it formulates. Forms: tags, tagged.

## Behaviour

### [g1] A claimed work-item stops the migration before any change
Restates: r1@0.29.
- [r1] While a work-item is `claimed`, if the person runs `migrating-to-capabilities`, then
  `migrating-to-capabilities` shall change nothing and show the reason.

### [g2] A suite that does not pass stops the migration before any change
Restates: r1@0.29.
- [r2] While a scenario is not passing, if the person runs `migrating-to-capabilities`, then
  `migrating-to-capabilities` shall change nothing and show the reason.

### [g3] The gate shows what the migration would do and what it asks
Restates: r2@0.29, r16@0.29, r26@0.29.
- [r3] When `migrating-to-capabilities` starts a gate, `migrating-to-capabilities` shall show every capability, show
  every scenario, show every question, show every glossary bullet, show every slice and show every backlog entry, and
  `migrating-to-capabilities` shall not commit a file.

### [g4] A migration starts with its mechanical commit on the final layout
Restates: r10@0.29, r14@0.29, r15@0.29, r22@0.29.
- [r4] When the person runs `migrating-to-capabilities` on a bounded context, `migrating-to-capabilities` shall write
  a mechanical commit, write a context id, change every old reference and relocate `docs/superpowers/`.

### [g5] No statement's text changes
Restates: r22@0.29.
- [r5] `migrating-to-capabilities` shall not change a requirement.

### [g6] A complete migration keeps every scenario and every passing one
Restates: r4@0.29, r5@0.29, r8@0.29, r20@0.29, r23@0.29.
- [r6] When `migrating-to-capabilities` ends, `migrating-to-capabilities` shall keep every scenario, keep every
  scenario that is passing, show every rewritten file and change every design note, and `model` shall print no
  violation.

### [g7] A suite difference stops the migration
Restates: r6@0.29.
- [r7] If `migrating-to-capabilities` finds a suite difference, then `migrating-to-capabilities` shall show the suite
  difference, and `migrating-to-capabilities` shall not change a scenario.

### [g8] No step definition changes
Restates: r7@0.29.
- [r8] `migrating-to-capabilities` shall not change a step.

### [g9] Ids are given from r1
Restates: r9@0.29.
- [r9] When `migrating-to-capabilities` writes a capability, `migrating-to-capabilities` shall give every requirement
  a fresh id.

### [g10] Every scenario is tagged with its one statement
Restates: r11@0.29.
- [r10] `migrating-to-capabilities` shall tag every scenario.

### [g11] A kept slice becomes a work-item
Restates: r17@0.29.
- [r11] When `migrating-to-capabilities` finds a slice, `migrating-to-capabilities` shall write a work-item that is
  `drafted`.

### [g12] A held scenario is deprecated
Restates: r18@0.29.
- [r12] When `migrating-to-capabilities` finds a held scenario, `migrating-to-capabilities` shall write `@deprecated`.

### [g13] A ledger's decisions become decision files
Restates: r19@0.29.
- [r13] When `migrating-to-capabilities` finds a decision entry, `migrating-to-capabilities` shall write a
  design-decision and write a decision source.

### [g14] A glossary bullet is put in the glossary's form
Restates: r21@0.29.
- [r14] When `migrating-to-capabilities` finds a glossary bullet, `migrating-to-capabilities` shall write a term.

## Implementation, may change
- `skills/migrating-to-capabilities/` and `scripts/migrate`. A migration produces the 0.29 format, and `migrate upgrade`
  takes it on to codified statements.
- The migration also stops on a working tree that is not clean. Its gate shows which old features' scenarios each
  capability receives, every statement no scenario backs, every scenario that formulates no statement or more than
  one, and each pair of scenarios with one title that would land in one capability, asking to retitle one; until the
  person answers, nothing changes beyond the mechanical commit.
- The mechanical commit changes no statement's text and no scenario but the renaming of held scenarios. Each scenario
  goes, as it was, into the one feature file named for its capability. A note is headed as a proposal integrated into
  `spec/` on its date. The final layout has decisions one file each in `spec/decisions/` with the generated
  `index.md`, work and records under `.shop/`, and nothing of the plugin under `docs/superpowers/` or `.superpowers/`.
- A held scenario gets " (deprecated)" for " (held)" on its title and `Deprecated for:` for `Held for:`, and stays
  bound by its test. The living plan and its archives go to `.shop/records/archive/plans/`.

## Not yet
- None.

## Dropped
