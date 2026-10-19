---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/migration-tools
title: Migration tools
narrator: a person or session migrating a repository to the final layout
group: service
rests_on: [design-decision/migration-in-one-pass, design-decision/living-plan-to-work-items, design-decision/final-layout, design-decision/references-are-ids, design-decision/capability-ids-are-context-scoped, design-decision/plugin-takes-the-dependencies-it-needs]
retired: []
---

# Migration tools

## Purpose
`scripts/migrate` makes the mechanical changes that take a repository from the old system to the final layout
(design-decision/final-layout) in one run. It is the only code in the plugin that knows the old layout, and it
decides nothing that needs judgment. A walking skeleton (design-decision/behaviour-lines-are-ears): it grows from
what running it shows.

## Behaviour
- [r1] **When** `migrate run --context <id>` is run, `migrate` shall move with git the old directories to the final layout: the decisions to `spec/decisions/`, `work/` to `.shop/work/`, and `records/` and `docs/superpowers/` to `.shop/records/`.
- [r2] **When** `migrate run` is run, `migrate` shall replace the ledger `spec/decisions.md` with one decision file for each of its entries under `spec/decisions/`.
- [r3] **When** `migrate run` is run, `migrate` shall make each `@holding` scenario a `@deprecated` one, rebinding the tests that name it by title.
- [r4] **When** `migrate run` is run, `migrate` shall give `spec/index.md` the context's id, each Behaviour line without one an `[r<n>]`, and each capability, decision file and moved record its id on the final layout.
- [r5] **When** `migrate run` moves a file or changes an id, `migrate` shall rewrite each reference to it in the repository's tracked text files.
- [r6] **When** `migrate run` has run on a repository on the old system, `migrate` shall have left it so that `model check` reports no violation, unresolved reference or file problem.
- [r7] **If** `migrate` cannot make every change it was asked to, then `migrate` shall exit non-zero, naming each change it could not make, and change no file.

## Implementation, may change
- Python 3 with the standard library; moves are `git mv`; it does not commit. Every change is computed first,
  then written. A move onto a file that exists is a change it cannot make.
- The destinations under `.shop/records/` (archive, measurements, decision-arguments) and the record ids are
  design-decision/final-layout's; a decision file is `spec/decisions/<nnnn>-<name>.md` with an id, summary, date
  and status, and `spec/decisions/index.md` as `model decisions` writes it.

## Not yet
- `migrate status`, `migrate plan` (a living plan to work-items and observations), `--dry-run`, and
  product-level repositories (see skeleton-notes.md).
