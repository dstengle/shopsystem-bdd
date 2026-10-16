---
id: missingmass.io/shopsystem/shopsystem-bdd/spec-migration
title: Spec migration
narrator: the person migrating a repository onto spec/
group: service
rests_on: [decision/one-spec-per-context, decision/gate-on-behaviour-lines]
formulated_as: features/spec-migration.feature
retired: []
---

# Spec migration

## Purpose
Moves a repository that has design notes and approved feature files, but no `spec/`, onto capability files
paired with feature files. It is `migrating-to-capabilities`: the first integration, plus re-pairing the
existing scenarios. It changes the meaning of no approved scenario.

## Behaviour
- [r1] **If** the working tree is not clean, a slice is in progress, or the suite does not run cleanly, migration stops before any change and says which.
- [r2] **When** migration drafts the spec, the person is shown the capabilities, which old features' scenarios each receives, every line no scenario backs, and every question, and nothing under `spec/` changes before their yes.
- [r3] **If** two scenarios with one title would land in one capability, the person is asked to retitle one at the gate.
- [r4] **When** migration is done, each capability has one feature file named for it, holding the scenarios mapped to it; each scenario's effective tags, title, description and tables, and its Background steps followed by its own steps, are as they were.
- [r5] **When** migration is done, the suite's summary, its passing scenarios by title and its count of scenarios per tag equal those before it, retitles approved at the gate aside.
- [r6] **If** any of those differ, migration stops and reports the difference without editing a scenario.
- [r7] No step definition's body changes in a migration.
- [r8] **When** migration is done, each note is headed as a proposal integrated into `spec/` on its date.
- [r9] **Where** a repository has capability files whose Behaviour lines carry no ids, **when** it is migrated to ids, each line gets `[r<n>]` in its order from r1 with its text unchanged, each capability gets `retired: []`, and each capability's id becomes its context's id, a `/`, and its name.
- [r10] **When** a repository is migrated to ids, its context's id is the owner's domain, product and context name the person gives at the gate, unless `spec/index.md` already names them.
- [r11] **When** a repository is migrated to ids, each scenario that is not held gets the `@r<n>` tag of the line it formulates, and nothing else in any feature file changes.
- [r12] **If** a scenario formulates no line or more than one, migration to ids shows it to the person at the gate as a question and tags nothing before the answer.
- [r13] **When** migration to ids is done, the suite's summary, its passing scenarios by title and its count of scenarios per tag equal those before it, the new `@r<n>` tags aside.

## Implementation, may change
- A baseline under the scratch directory: the summary line, the passing tests (`-q -rA`), a copy of
  `features/`, and `features count --by-tag`.
- `capability-writer` drafts with the migration brief; `features move` (with `--carry-feature-tags`,
  `--inline-background`) moves scenarios; `features verify-moved` compares them.
- Bindings follow step definitions: `scenarios(...)` per capability where every step has one body, otherwise
  `@scenario(<file>, <title>)` from the old modules.

## Not yet
- Migration gives every line a requirement id and every scenario its `@r<n>` tag — trigger: initiative i3 is approved.
