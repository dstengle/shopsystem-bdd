---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/spec-migration
title: Spec migration
narrator: the person migrating a repository onto spec/
group: service
rests_on: [design-decision/one-spec-per-context, design-decision/gate-on-behaviour-lines, design-decision/migration-in-one-pass, design-decision/living-plan-to-work-items, design-decision/final-layout]
retired: []
---

# Spec migration

## Purpose
Moves a repository onto the final layout of design model v3 (design-decision/final-layout) in one pass,
whatever it has of the old system: design notes and approved feature files with no `spec/`, capability files
without ids, a decision ledger, top-level `decisions/`, `work/` or `records/`, `docs/superpowers/`, a living
slice plan, `@holding` scenarios. It is `migrating-to-capabilities`: the first integration where there is no
`spec/`, re-pairing the existing scenarios, and `scripts/migrate` for every mechanical change, with one gate.
It changes the meaning of no approved scenario.

## Behaviour
- [r1] **If** the working tree is not clean, a work-item is `claimed`, or the suite does not run cleanly, migration stops before any change and says which.
- [r2] **When** migration drafts the spec, the person is shown the capabilities, which old features' scenarios each receives, every line no scenario backs, and every question, and nothing under `spec/` changes before their yes.
- [r3] **If** two scenarios with one title would land in one capability, the person is asked to retitle one at the gate.
- [r4] **When** migration is done, each capability has one feature file named for it, with the scenarios mapped to it; each scenario's effective tags, title, description and tables, and its Background steps followed by its own steps, are as they were, the new `@r<n>` tags aside.
- [r5] **When** migration is done, the suite's summary, its passing scenarios by title and its count of scenarios per tag equal those before it, retitles approved at the gate and the new `@r<n>` tags aside.
- [r6] **If** any of those differ beyond what they set aside, migration stops and reports the difference without editing a scenario.
- [r7] No step definition's body changes in a migration.
- [r8] **When** migration is done, each note is headed as a proposal integrated into `spec/` on its date.
- [r9] **Where** a repository has capability files whose Behaviour lines have no ids, **when** it is migrated to ids, each line gets `[r<n>]` in its order from r1 with its text unchanged, each capability gets `retired: []`, and each capability's id becomes `capability/<context path>/<name>`.
- [r10] **When** a repository is migrated to ids, its context's id is `bounded-context/<context path>`, the context path being the owner's domain, product and context name the person gives at the gate, unless `spec/index.md` already names them.
- [r11] **When** a repository is migrated onto `spec/` or to ids, each scenario that is not deprecated gets the `@r<n>` tag of the line it formulates, and nothing else in a scenario changes but the deprecations the gate led to and the renaming of r18.
- [r12] **If** a scenario formulates no line or more than one, migration to ids shows it to the person at the gate as a question and tags nothing before the answer.
- [r13] **When** migration onto `spec/` or to ids is done, the suite's summary, its passing scenarios by title and its count of scenarios per tag equal those before it, the new `@r<n>` tags, the deprecations the gate led to, and the " (deprecated)" titles of those and of r18's renaming aside.
- [r14] **When** a repository is migrated to ids, its `decision/<name>` references become `design-decision/<name>`, every frontmatter `id` under `spec/decisions/` and `.shop/` is written in full, its observation headings `## obs/<x>` become `## observation/<context path>/<x>`, and nothing else in a reference changes.
- [r15] **When** a repository is migrated, it ends on the final layout: decisions one file each in `spec/decisions/` with the generated `index.md`, work and records under `.shop/`, nothing of the plugin under `docs/superpowers/` or `.superpowers/`, and `migrate status` saying there is nothing left to migrate.
- [r16] **When** migration stops at the gate, the person is shown, besides r12's questions, each glossary bullet not in the glossary's form, each open slice of the living plan, and each backlog and log entry that would become an observation, and nothing after the mechanical move is committed before their answers.
- [r17] **When** migration is done, each open slice the person kept is a work-item accepting the requirements its scenarios are tagged with, each slice the person dropped is only in the archived plan, each entry the person did not leave out is an observation, and the plan and its archives are records under `.shop/records/archive/plans/`.
- [r18] **When** migration is done, each scenario that was tagged `@holding` is tagged `@deprecated`, with " (deprecated)" for " (held)" on its title and `Deprecated for:` for `Held for:`, and its test still binds it.
- [r19] **When** migration is done, each decision of the ledger is a decision file with the entry's text as its summary and Decision, and its `source` names by id the records the files it named became.
- [r20] **When** migration is done, `model check` reports no violation, unresolved reference or file problem, and no `v_s3` (a requirement has no scenario) but for lines that had no scenario before.
- [r21] **When** migration is done, each glossary bullet is in the glossary's form, in the words the person gave at the gate.
- [r22] **When** migration is done, the mechanical move is one commit, before the gate, in which no Behaviour line's text and no scenario but its renaming of r18 changes; the tags, work-items and observations the gate allowed are the next.
- [r23] **When** migration is done, the person is shown each file other than Markdown in which the migration rewrote a path it moved, with the line.

## Implementation, may change
- A baseline under `.shop/scratch/migration/`: the summary line, the passing tests (`-q -rA`), a copy of
  `features/`, and `features count --by-tag`.
- `scripts/migrate status`, `run` and `plan` (capability/migration-tools) make the mechanical changes; the
  session asks the context path before `run` when `spec/index.md` lacks it, maps scenarios to lines with
  `feature-formulator`, tags with `features tag`, then runs `plan` with the gate's `--drop` and `--leave`.
- `capability-writer` drafts with the migration brief; `features move` (with `--keep-feature-tags`,
  `--inline-background`) moves scenarios; `features verify-moved` compares them.
- Bindings follow step definitions: `scenarios(...)` per capability where every step has one body, otherwise
  `@scenario(<file>, <title>)` from the old modules.

## Not yet
None.
