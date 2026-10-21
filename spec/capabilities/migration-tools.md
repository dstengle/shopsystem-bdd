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
(design-decision/final-layout) in one `migrate run`. It is the only code in the plugin that knows the old layout, and it
decides nothing that needs judgment. A walking skeleton (design-decision/behaviour-lines-are-ears): it grows from
what running it shows.

## Behaviour
- [r1] **When** `migrate run --context <path>` is run, `migrate` shall relocate with git a top-level `decisions/` to `spec/decisions/`, `work/` to `.shop/work/`, and each `records/<x>` to `.shop/records/<x>`.
- [r2] **When** `migrate run` finds a ledger entry `## decision/<nnnn>-<slug>` in `spec/decisions.md`, `migrate` shall replace it with `spec/decisions/<nnnn>-<slug>.md`, whose summary is the entry's first paragraph, whose Decision is the entry's whole text, whose status is `superseded` when another entry supersedes it and `accepted` otherwise, and whose `date`, `by`, `supersedes` and `revisit_when` are the entry's.
- [r3] **When** `migrate run` finds a `@holding` scenario, `migrate` shall tag it `@deprecated` with " (deprecated)" for " (held)" on its title and `Deprecated for:` for `Held for:`, rebind each test that names it by title, and leave no `@holding` tag.
- [r4] **When** `migrate run --context <path>` is run, `migrate` shall give `spec/index.md` the id `bounded-context/<path>`.
- [r5] **When** `migrate run` relocates a file or changes an id, `migrate` shall rewrite each repository-relative path, relative Markdown link and frontmatter id that names it in the repository's tracked text files.
- [r6] **When** `migrate run` has run on a repository on the old system, `migrate` shall have left it so that `model check` prints no unresolved reference or file problem.
- [r7] **If** `migrate` cannot make every change it was asked to, then `migrate` shall exit with an error, naming each change it could not make, and change no file.
- [r8] **When** `migrate run` is run, `migrate` shall relocate with git `docs/superpowers/plans/` to `.shop/records/archive/plans/`, `docs/superpowers/specs/` to `.shop/records/archive/design-notes/` and `docs/superpowers/requests/` to `.shop/records/archive/requests/`.
- [r9] **When** `migrate run` gives a capability, a decision file or a relocated record its id, `migrate` shall write `<kind>/<path>/<name>`, the name being the file's stem, without a decision file's number, and the kind `capability`, `design-decision`, or for a relocated plan or request `initiative-archive`, for a relocated design note or ADR `decision-argument`, and for a relocated test log (a file whose name ends `-test-log.md`) `measurement`.
- [r10] **When** `migrate run` finds Behaviour lines with no id, `migrate` shall number them in Behaviour order from one above the highest id their capability has ever used.
- [r11] **When** `migrate run` has replaced every entry of `spec/decisions.md` and the ledger holds nothing but its entries and a title, `migrate` shall remove `spec/decisions.md`.
- [r12] **When** `migrate run` gives a relocated record its id and the record has no `about`, `migrate` shall give it `about: bounded-context/<path>`.
- [r13] **When** `migrate run` finds a ledger entry `## decision/<slug>` with no number, `migrate` shall number it in ledger order from one above the ledger's highest entry number.
- [r14] **When** `migrate run` is run, `migrate` shall relocate with git a top-level `adrs/` to `.shop/records/decision-arguments/`.
- [r15] **If** the repository has uncommitted changes, then `migrate run` shall refuse, naming them, and change no file.
- [r16] **When** `migrate run` has made its changes, `migrate` shall add every file it wrote or relocated to git and write `spec/decisions/index.md`.
- [r17] **When** a ledger entry's `supersedes` names a decision with a qualifier, `migrate` shall write the decision's id alone in `supersedes` and the qualifier in `by`.

## Implementation, may change
- r17's `by`: the entry's source, then `; supersedes <id> <qualifier>`.
- Python 3 with the standard library; it relocates with `git mv`; it does not commit. Every change is computed first,
  then written. A relocation onto a file that exists is a change it cannot make.
- The destinations under `.shop/records/` (archive, measurements, decision-arguments) and the record ids are
  design-decision/final-layout's; a decision file is `spec/decisions/<nnnn>-<name>.md` with an id, summary, date
  and status, and `spec/decisions/index.md` as `model decisions` writes it.

## Not yet
- `migrate status`, `migrate plan` (a living plan to work-items and observations), `--dry-run`, and
  product-level repositories (see skeleton-notes.md).
