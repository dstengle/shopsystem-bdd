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
- [r1] **When** `migrate run --context <path>` is run, `migrate` shall move with git a top-level `decisions/` to `spec/decisions/`, `work/` to `.shop/work/`, and each `records/<x>` to `.shop/records/<x>`.
- [r2] **When** `migrate run` finds a ledger entry `## decision/<nnnn>-<slug>` in `spec/decisions.md`, `migrate` shall replace it with `spec/decisions/<nnnn>-<slug>.md`, whose summary and Decision are the entry's first paragraph, whose status is accepted, and whose `date` and `by` are the entry's date and source.
- [r3] **When** `migrate run` finds a `@holding` scenario, `migrate` shall deprecate it as `features deprecate` does.
- [r4] **When** `migrate run --context <path>` is run, `migrate` shall give `spec/index.md` the id `bounded-context/<path>`.
- [r5] **When** `migrate run` moves a file or changes an id, `migrate` shall rewrite each repository-relative path, relative Markdown link and frontmatter id that names it in the repository's tracked text files.
- [r6] **When** `migrate run` has run on a repository on the old system, `migrate` shall have left it so that `model check` reports no violation, unresolved reference or file problem.
- [r7] **If** `migrate` cannot make every change it was asked to, then `migrate` shall exit non-zero, naming each change it could not make, and change no file.
- [r8] **When** `migrate run` is run, `migrate` shall move with git `docs/superpowers/plans/` to `.shop/records/archive/plans/` and `docs/superpowers/specs/` to `.shop/records/archive/design-notes/`.
- [r9] **When** `migrate run` gives a capability, a decision file or a moved record its id, `migrate` shall write `<kind>/<path>/<name>`, the name being the file's stem and the kind `capability`, `design-decision`, or for a moved plan, design note or test log (a file whose name ends `-test-log.md`) `initiative-archive`, `decision-argument` or `measurement`.
- [r10] **When** `migrate run` finds Behaviour lines with no id, `migrate` shall number them in Behaviour order from one above the highest id their capability has ever used.
- [r11] **When** `migrate run` has replaced every entry of `spec/decisions.md`, `migrate` shall remove `spec/decisions.md`.

## Implementation, may change
- Python 3 with the standard library; moves are `git mv`; it does not commit. Every change is computed first,
  then written. A move onto a file that exists is a change it cannot make.
- The destinations under `.shop/records/` (archive, measurements, decision-arguments) and the record ids are
  design-decision/final-layout's; a decision file is `spec/decisions/<nnnn>-<name>.md` with an id, summary, date
  and status, and `spec/decisions/index.md` as `model decisions` writes it.

## Not yet
- `migrate status`, `migrate plan` (a living plan to work-items and observations), `--dry-run`, and
  product-level repositories (see skeleton-notes.md).
