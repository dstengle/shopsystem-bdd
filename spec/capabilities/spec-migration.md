---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/spec-migration
title: Spec migration
narrator: the person migrating a repository onto spec/
group: service
rests_on: [design-decision/one-spec-per-context, design-decision/gate-on-behaviour-lines, design-decision/migration-in-one-pass, design-decision/living-plan-to-work-items, design-decision/final-layout]
retired: [r3, r12, r13]
---

# Spec migration

## Purpose
Takes a repository onto the final layout of design model v3 (design-decision/final-layout) in one pass,
whatever it has of the old system: design notes and approved feature files with no `spec/`, capability files
without ids, a decision ledger, top-level `decisions/`, `work/` or `records/`, `docs/superpowers/`, a living
slice plan, `@holding` scenarios. It is `migrating-to-capabilities`: the first integration where there is no
`spec/`, re-pairing the existing scenarios, and `scripts/migrate` for every mechanical change, with one gate.
It changes the meaning of no approved scenario.

## Behaviour
- [r1] **If** the working tree is not clean, a work-item is `claimed`, the suite does not run cleanly, or `migrating-to-capabilities` cannot otherwise do what it was asked, then `migrating-to-capabilities` shall stop before any change, saying why.
- [r2] **When** migration stops at its gate, `migrating-to-capabilities` shall show the person the capabilities, which old features' scenarios each receives, every line no scenario backs, every scenario that formulates no line, each pair of scenarios with one title that would land in one capability (asking to retitle one), and every other question.
- [r16] **When** migration stops at its gate, `migrating-to-capabilities` shall show the person each glossary bullet not in the glossary's form, each open slice of the living plan, and each backlog entry and each entry of a log that would become an observation.
- [r26] **While** the person has not answered at the gate, `migrating-to-capabilities` shall change nothing beyond the mechanical commit.
- [r22] **When** migration is complete, `migrating-to-capabilities` shall have made the mechanical changes one commit, the mechanical commit, before the gate, in which no Behaviour line's text and no scenario but its renaming of r18 changes.
- [r4] **When** migration is complete, `migrating-to-capabilities` shall have put each scenario in the one feature file named for its capability, its effective tags, title, description and tables, and its Background steps followed by its own steps, as they were, the new `@r<n>` tags aside.
- [r5] **When** migration onto `spec/` or to ids is complete, `migrating-to-capabilities` shall have left the suite's summary, its passing scenarios by title and its count of scenarios per tag equal to those before it, the retitles approved at the gate, the new `@r<n>` tags, the deprecations the gate led to, and the " (deprecated)" titles of those and of r18's renaming aside.
- [r6] **If** the suite's summary, its passing scenarios by title or its count of scenarios per tag differ from those before migration beyond what r5 sets aside, then `migrating-to-capabilities` shall stop and show the person the difference without editing a scenario.
- [r7] `migrating-to-capabilities` shall change no step definition's body in a migration.
- [r23] **When** migration is complete, `migrating-to-capabilities` shall show the person each file other than Markdown in which the migration rewrote a path it relocated, with the line.
- [r8] **When** migration is complete, `migrating-to-capabilities` shall have headed each note as a proposal integrated into `spec/` on its date.
- [r9] **Where** a repository has capability files whose Behaviour lines have no ids, **when** it is migrated to ids, `migrating-to-capabilities` shall give each line `[r<n>]` in its order from r1, its text unchanged, and each capability `retired: []` and the id `capability/<context path>/<name>`.
- [r10] **When** a repository is migrated to ids, `migrating-to-capabilities` shall make its context's id `bounded-context/<context path>`, the owner's domain, product and context name that `spec/index.md` names or, where it names none, that the person gives at the gate.
- [r11] **When** a repository is migrated onto `spec/` or to ids, `migrating-to-capabilities` shall give each scenario that is not deprecated the `@r<n>` tag of each line it formulates, and change nothing else in a scenario but the deprecations the gate led to and the renaming of r18.
- [r14] **When** a repository is migrated to ids, `migrating-to-capabilities` shall rewrite its `decision/<name>` references as `design-decision/<name>`, every frontmatter `id` under `spec/decisions/` and `.shop/` in full, and its observation headings `## obs/<x>` as `## observation/<context path>/<x>`, changing nothing else in a reference.
- [r15] **When** a repository is migrated, `migrating-to-capabilities` shall leave it on the final layout: decisions one file each in `spec/decisions/` with the generated `index.md`, work and records under `.shop/`, nothing of the plugin under `docs/superpowers/` or `.superpowers/`, and `model check` printing no file problem that names `scripts/migrate`.
- [r17] **When** migration is complete, `migrating-to-capabilities` shall have turned the living plan into what the person kept at the gate: each open slice kept a work-item accepting the requirements its scenarios are tagged with, each slice dropped only in the archived plan, each entry not left out an observation, and the plan and its archives records under `.shop/records/archive/plans/`.
- [r18] **When** migration is complete, `migrating-to-capabilities` shall have tagged each scenario that was tagged `@holding` `@deprecated`, with " (deprecated)" for " (held)" on its title and `Deprecated for:` for `Held for:`, still bound by its test.
- [r19] **When** migration is complete, `migrating-to-capabilities` shall have made each decision of the ledger a decision file with the entry's text as its summary and Decision, its `source` naming by id the records the files the entry named became.
- [r20] **When** migration is complete, `migrating-to-capabilities` shall have left the repository with no violation, unresolved reference, file problem or `v_s3` (a requirement has no scenario) for `model check` to print, but a `v_s3` for a line that had no scenario before.
- [r21] **When** migration is complete, `migrating-to-capabilities` shall have put each glossary bullet in the glossary's form, in the words the person gave at the gate.

## Implementation, may change
- A baseline under `.shop/scratch/migration/`: the summary line, the passing tests (`-q -rA`), a copy of
  `features/`, and `features count --by-tag`.
- `migrate status`, `migrate run` and `migrate plan` (capability/migration-tools) make the mechanical changes; the
  session asks the context path before `migrate run` when `spec/index.md` lacks it, maps scenarios to lines with
  `feature-formulator`, tags with `features tag`, then runs `migrate plan` with the gate's `--drop` and `--leave`.
- `capability-writer` drafts with the migration template; `features move` (with `--keep-feature-tags`,
  `--inline-background`) relocates scenarios; `features verify-moved` compares them.
- Bindings follow step definitions: `scenarios(...)` per capability where every step has one body, otherwise
  `@scenario(<file>, <title>)` from the old modules.
- The tags, work-items and observations the gate allowed are the commit after the mechanical commit.

## Not yet
None.
