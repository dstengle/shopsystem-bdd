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
`scripts/migrate` makes every mechanical change that takes a repository from the old system to the final
layout (design-decision/final-layout): requirement and node ids, the moves of the old directories with ids
for the records among them, the decision ledger split into decision files, `@holding` renamed to
`@deprecated`, and a living slice plan turned into work-items and observations. It is the only code in the
plugin that knows the old layout. It decides nothing that needs judgment: it refuses, naming what it cannot
place, and leaves the mapping of scenarios to lines, the context path and the gate to the session.

## Behaviour
- [r1] `migrate` reads and changes files only under `--root`, default the current directory.
- [r2] **When** `migrate status` is run, it prints each thing of the old system the repository has, one a line: `spec/decisions.md`; a `decisions/`, `work/` or `records/` directory at the root; each file under `docs/superpowers/`; a living plan `*-slices.md`; each scenario tagged `@holding`; each capability with `formulated_as`, with an `id` not `capability/<context path>/<file name>`, or without `retired`; each capability with a Behaviour line that has no `[r<n>]`; and `spec/index.md` with no `id`; and it exits 1.
- [r3] **When** `migrate status` finds none of those, it says the repository is on the final layout and exits 0.
- [r4] **If** the root is not a git working tree, `migrate run` and `migrate plan` refuse.
- [r5] **If** `spec/index.md` has no `id` and `migrate run` is given no `--context`, it refuses, saying the context's id is needed, and changes no file.
- [r6] **If** `--context` is not `bounded-context/<owner>/<product>/<context name>`, or is not the `id` `spec/index.md` already has, `migrate run` refuses and changes no file.
- [r7] **Where** `--dry-run` is given, `migrate run` and `migrate plan` print every change they would make and change no file.
- [r8] **When** `migrate run` or `migrate plan` changes files, it prints each change, one a line, under the name of its step, and the number of changes of each step.
- [r9] **If** any change of `migrate run` or `migrate plan` cannot be made, it refuses before changing any file, naming each change it could not make.
- [r10] **When** `migrate run` is run on a repository on the final layout, it changes no file and says there is nothing to migrate.
- [r11] **When** `migrate run` is run, `spec/index.md`'s frontmatter has the context's `id`, written when it had none.
- [r12] **When** `migrate run` is run, each Behaviour bullet with no `[r<n>]` gets one, numbered from one above the highest id its capability has used or retired, in the order the bullets come, and its text is unchanged.
- [r13] **When** `migrate run` is run, each capability with no `retired` gets `retired: []`, and each capability's `id` is `capability/<context path>/<file name>`.
- [r14] **When** `migrate run` is run, each `decision/<name>` reference in frontmatter and each `## decision/<name>` heading becomes `design-decision/<name>`, each `obs/<x>` reference becomes `observation/<x>`, each `## obs/<x>` heading becomes `## observation/<context path>/<x>`, each frontmatter `id` under `spec/decisions/` and `.shop/` is written `<kind>/<context path>/<name>`, and nothing else in a reference changes.
- [r15] **When** `migrate run` is run, `formulated_as` is removed from each capability whose `formulated_as` is `features/<its file name>.feature`.
- [r16] **If** a capability's `formulated_as` names any other file, `migrate run` refuses, naming the capability and the file.
- [r17] **When** `migrate run` is run, it moves with git: `decisions/*.md` to `spec/decisions/`; `work/` to `.shop/work/`; `records/` to `.shop/records/`; `docs/superpowers/specs/` to `.shop/records/archive/design-notes/`; `docs/superpowers/plans/`, with its `archive/`, to `.shop/records/archive/plans/`; `docs/superpowers/requests/` to `.shop/records/archive/requests/`; `docs/superpowers/measurements/` to `.shop/records/measurements/`; `docs/superpowers/reports/` to `.shop/records/archive/reports/`; any other file under `docs/superpowers/` to `.shop/records/archive/` under its path below `docs/superpowers/`; and each other directory a ledger entry's `source` names a file in, such as `adrs/`, to `.shop/records/decision-arguments/`.
- [r18] **If** a file would be moved onto a file that exists, `migrate run` refuses, naming both.
- [r19] **When** `migrate run` is run, each Markdown file under `.shop/records/` but `observations.md` and `README.md` that has no frontmatter `id` gets `id`, `kind`, `about` and `date`: the id `<kind>/<context path>/<its file name without .md>`, lowercased with each run of other characters than letters, digits and hyphens as one hyphen; the kind by its directory (`decision-arguments/` and `archive/design-notes/` decision-argument, `measurements/` measurement, `review-findings/` review-finding, any other under `archive/` initiative-archive); `about` the bounded context; the date its name begins with, or else the date of the commit that added it. Any frontmatter it had is kept.
- [r20] **When** `migrate run` has moved files, each moved path, written in full from the root, is rewritten to its new path in every tracked text file outside `.shop/records/`, and each file other than Markdown it so changed is listed with the line.
- [r21] **When** `migrate run` is run, a `.superpowers/` line of `.gitignore` becomes `.shop/scratch/`, and `.shop/scratch/` is added to `.gitignore` when it has neither.
- [r22] **When** `migrate run` is run, each entry of `spec/decisions.md` becomes the file `spec/decisions/<nnnn>-<name>.md`, `nnnn` its position in the ledger written in four digits, or `<name>.md` when the name already begins with those four digits and a hyphen, and `spec/decisions.md` is removed.
- [r23] A decision file made from a ledger entry has the frontmatter `id` `design-decision/<context path>/<name>`, `summary` the entry's text up to its first blank line or property line with its lines joined by a space, `date`, `status: accepted`, and the entry's `supersedes` and `revisit_when` where it has them; its body is `# <nnnn>. <name with hyphens as spaces>` and a `## Decision` section of the entry's text.
- [r24] **If** a ledger entry has a property line other than `date:`, `revisit_when:`, `supersedes:` or `source:`, or has no `date:`, `migrate run` refuses, naming the entry.
- [r25] **When** `migrate run` writes a decision's `source`, from a ledger entry or a decision file's own `source`, each part of it, split at `;`, that begins with the path of a file the run moved, old or new, becomes that file's record id; each part that is an id of a node kind stays as it is; and the rest of each part, and every other part, is written in `by`, joined with "; ".
- [r26] **When** `migrate run` has written the decision files, `spec/decisions/index.md` is what `model decisions` writes.
- [r27] **When** `migrate run` is run, each scenario tagged `@holding` is tagged `@deprecated`, " (held)" at the end of its title becomes " (deprecated)", its `Held for:` line becomes `Deprecated for:`, and nothing else in it changes.
- [r28] **When** `migrate run` retitles a scenario, each `scenario(<feature>, "<old title>")` binding call under `--tests`, default `tests`, that names it is rewritten to the new title, and nothing else in the module changes.
- [r29] **If** a test module under `--tests` does not parse, or names an old title in a string written over several lines, `migrate run` refuses, naming the module.
- [r30] `migrate plan` reads as the living plan the one `*-slices.md` directly in `.shop/records/archive/plans/`, or the file `--plan` names.
- [r31] **If** there is no living plan or there are several, `migrate plan` refuses, naming those it found.
- [r32] **If** a slice of the plan is `in progress`, `migrate plan` refuses, naming it.
- [r33] **When** `migrate plan` is run, each slice whose status is not green and that `--drop` does not name becomes a `planned` work-item `.shop/work/migrated-plan/slice-<n>.md`, `n` the slice's number with its dots as hyphens, with the id `work-item/<context path>/slice-<n>`, `wkind` capability for a capability slice and enabling for an enabling or stack slice, and as its body the slice's heading, its `Observable:`, `Unknown:`, `Needs:`, `Lands:` and `Status:` lines, and its place in the plan.
- [r34] **When** `migrate plan` writes a capability slice's work-item, it is `under` the capability of its first `Scenarios:` entry's feature, `part_of` `capability-proposal/<context path>/migrated-<that capability>`, and `accepts` `<capability>#r<n>` for each `<feature> / <title>` entry, `@r<n>` being the requirement tag of the scenario of that title in `features/<feature>.feature`.
- [r35] **If** a `Scenarios:` entry names a title no scenario of its feature file has, or a scenario with no `@r<n>` tag, `migrate plan` refuses, naming the slice and the entry.
- [r36] **When** `migrate plan` writes an enabling or stack slice's work-item, its `check` is the slice's `Check:` text, it is `for` the work-item of the first capability slice after it in the plan that becomes a work-item, and it is `part_of` that work-item's capability-proposal.
- [r37] **Where** no capability slice after an enabling or stack slice becomes a work-item, `migrate plan` writes that slice as an observation in place of a work-item.
- [r38] **When** `migrate plan` is run, each entry of the plan's Backlog, and each Log entry that begins `QUESTION FOR THE SPEC:`, `REQUEST` or `RE-FORMULATE` with its continuation lines, that `--leave` does not name, is appended to `.shop/records/observations.md` as `## observation/<context path>/<date>-backlog-<k>` or `<date>-log-<k>`, `k` counting that section's entries of that date from 1, with `about:` the bounded context, `by:` the plan's backlog or log, `date:`, and the entry's text as it was.
- [r39] **When** `migrate plan` writes any work-item, it also writes `.shop/work/migrated-plan/initiative.md`, the initiative `initiative/<context path>/migrated-plan`, kind capability-change, status started, priority 1, dated today, its source an observation `<today>-migrated-plan` it appends, naming the plan and how many slices it migrated; and for each capability a work-item is under, `migrated-<capability>.md`, a capability-proposal `part_of` the initiative, `argues` the capability, status formulated, dated today.
- [r40] **If** `.shop/work/migrated-plan/` exists, `migrate plan` refuses and changes no file.
- [r41] **When** `migrate plan` finds no slice to migrate, it writes no initiative, proposal or work-item and says so, and still writes the observations.
- [r42] **When** `migrate plan` has run, `model check` reports no violation, unresolved reference or file problem in the files it wrote.
- [r43] **When** `migrate plan --dry-run` is run, it lists each slice it would migrate or drop and each entry it would make an observation, by the name `--drop` and `--leave` take.
- [r44] **If** `--drop` or `--leave` names a slice or entry the plan does not have, `migrate plan` refuses, naming it.
- [r45] **If** `migrate` refuses, it says why on stderr, exits 1 and changes no file; bad usage exits 2.

## Implementation, may change
- Python 3 with the standard library; moves are `git mv`, the commit date is `git log --diff-filter=A
  --format=%as -- <path>`. It does not commit.
- `run`'s steps, in order: ids, layout, decisions, deprecated. Every change is computed first, then written;
  a refusal in any step writes nothing.
- The ledger is read by `## (design-)?decision/<name>` headings; an entry ends at the next heading. Property
  lines are `<name>: <value>`, one a line.
- `plan` parses the old plan format (`## Slice <n>: <name>`, `- Kind:`, `- Scenarios: <feature> / <title>;
  …`, `- Check:`, `- Status:`, sections `Backlog` and `Log` of `- <date> <text>` entries); it does not use
  `scripts/plan`. `--drop` takes slice numbers, `--leave` observation names, both comma-separated.
- A slice's `Scenarios:` entry is split at `; ` between entries and at the first ` / ` within one.
- The help text (`--help`) is the contract.
- Exit status: 0 done, 1 refused or something left to migrate (`status`), 2 bad usage.

## Not yet
- Product-level repositories (jobs, a context-map) — trigger: shopsystem-knowledge is migrated.
