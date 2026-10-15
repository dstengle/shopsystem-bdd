---
id: shopsystem-bdd/design-model-check
title: Design model check
narrator: a person or agent checking a repository against the design model
group: service
rests_on: [decision/plugin-adopts-the-design-model, decision/model-check-solves-with-clingo, decision/scenario-names-requirement-by-tag, decision/retired-ids-in-capability-frontmatter, decision/work-file-forms, decision/capability-ids-are-context-scoped]
formulated_as: features/design-model-check.feature
retired: []
---

# Design model check

## Purpose
`scripts/model` reads a bounded context's files — spec, feature files, decisions, work and records — as the
facts of `docs/design-model/grammar.md`, and reports what the grammar refuses. It also writes the generated
decisions index and traces a requirement to why it exists. It does not edit the spec, the work or the
records, and it checks one bounded context: product-level artifacts are read only where the files hold them.

## Behaviour
- [r1] **When** `model check` finds no violation, unresolved reference or file problem, it says so with the counts and exits 0.
- [r2] **When** `model check` finds violations, it prints each violated relation by its grammar.md name, with its rows, and exits 1.
- [r3] **If** a requirement bullet in a capability's Behaviour has no `[r<n>]`, `model check` reports it under v15a.
- [r4] **If** two requirements of one capability carry the same id, `model check` reports them under v15b.
- [r5] **If** a capability uses an id it lists as retired, `model check` reports it under v15c.
- [r6] **If** a capability-proposal changes a requirement no capability has, `model check` reports it under v15e.
- [r7] **If** a capability-proposal is `formulated` while a requirement it adds or changes has no scenario, and the capability is not guarantees, `model check` reports it under v15f.
- [r8] **If** a requirement of a capability that is not guarantees has no scenario naming it, `model check` reports it under v_s3.
- [r9] **If** a scenario names a requirement its capability does not have, or a capability rests on a decision that does not exist, `model check` reports the unresolved reference and exits 1.
- [r10] **If** a part has no `part_of`, or its `part_of` chain does not reach an initiative, `model check` reports it under v9a or v9c.
- [r11] **When** `model check` finds warnings, it prints each warning relation with its count and they alone do not change the exit status.
- [r12] **If** the clingo package is missing, `model check` says so with the command that installs it and exits 2.
- [r13] **When** `model facts` is run, it prints the facts read, one a line in clingo's syntax, using only the standard library.
- [r14] **When** `model decisions` is run, `spec/decisions.md` lists every decision under `decisions/` with its summary, status, what it supersedes and when to revisit it.
- [r15] **When** `model decisions --check` is run and `spec/decisions.md` is not what `model decisions` would write, it says so, exits 1 and writes nothing.
- [r16] **When** `model why <capability>#r<n>` is run, it prints the requirement, each capability-proposal that adds or changes it, the `part_of` chain to its initiative and the initiative's sources.
- [r17] **If** no capability-proposal adds or changes the requirement, `model why` says so and exits 1.
- [r18] **Where** a proposal's or work-item's list names `<capability>#r<a>-r<b>`, `model` reads it as every id from a to b.

## Implementation, may change
- `scripts/model.lp` is grammar.md v3 sections 1, 3 and 4 in clingo, with FIX notes where grammar.md does not
  compile as written; facts use grammar.md's relation names.
- Node ids: the bounded-context is spec/index.md's `id`; a requirement without an id is `<capability>#line<k>`;
  a scenario is `<feature path>:<title>`.
- The frontmatter reader is a YAML subset: scalars, `[a, b]` lists and `- x` block lists.

## Not yet
- Product-level artifacts (jobs, the context-map, seams, pins) read from a product repository — trigger: a second bounded context is checked together with this one.
- A work-queue view (ready items, claims) — trigger: initiative i5 is approved.
