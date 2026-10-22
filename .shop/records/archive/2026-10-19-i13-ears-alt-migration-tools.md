---
id: initiative-archive/missingmass.io/shopsystem/shopsystem-bdd/2026-10-19-i13-ears-alt-migration-tools
kind: initiative-archive
about: capability/missingmass.io/shopsystem/shopsystem-bdd/migration-tools
date: 2026-10-19
---

# 0.21.0 EARS restructure (i13): unused alternative migration-tools draft

An alternative round-1 EARS draft of capability migration-tools with its map (45 lines became 85, every 'and changes no file' and exit status its own line where possible), not used: SUMMARY.md says alt/ is not part of the round. The round-1 draft that was used is in the round-1 capabilities record; migration-tools later became a walking skeleton.

Archived from git-ignored scratch; each file's text as it was.

## `.shop/scratch/ears/alt/migration-tools.md`

~~~~~~
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
- [r1] `migrate` shall read and change files only under `--root`, default the current directory.
- [r2] **When** `migrate status` is run, `migrate status` shall print each thing of the old system the repository has, one a line: `spec/decisions.md`; a `decisions/`, `work/` or `records/` directory at the root; each file under `docs/superpowers/`; a living plan `*-slices.md`; each scenario tagged `@holding`; each capability with `formulated_as`, with an `id` not `capability/<context path>/<file name>`, or without `retired`; each capability with a Behaviour line that has no `[r<n>]`; and `spec/index.md` with no `id`.
- [r46] **When** `migrate status` finds a thing of the old system, `migrate status` shall exit 1.
- [r3] **When** `migrate status` finds none of the things of the old system, `migrate status` shall say the repository is on the final layout.
- [r47] **When** `migrate status` finds none of the things of the old system, `migrate status` shall exit 0.
- [r4] **If** the root is not a git working tree, then `migrate` shall refuse `run` and `plan`.
- [r5] **If** `spec/index.md` has no `id` and `migrate run` is given no `--context`, then `migrate run` shall refuse, saying the context's id is needed.
- [r6] **If** `--context` is not `bounded-context/<owner>/<product>/<context name>`, then `migrate run` shall refuse.
- [r48] **If** `--context` is not the `id` `spec/index.md` already has, then `migrate run` shall refuse.
- [r7] **Where** `--dry-run` is given to `run` or `plan`, `migrate` shall print every change it would make.
- [r49] **Where** `--dry-run` is given to `run` or `plan`, `migrate` shall change no file.
- [r8] **When** `migrate run` or `migrate plan` changes files, `migrate` shall print each change, one a line, under the name of its step, with the number of changes of each step.
- [r9] **If** any change of `migrate run` or `migrate plan` cannot be made, then `migrate` shall refuse before changing any file, naming each change it could not make.
- [r10] **When** `migrate run` is run on a repository on the final layout, `migrate run` shall change no file.
- [r50] **When** `migrate run` is run on a repository on the final layout, `migrate run` shall say there is nothing to migrate.
- [r11] **When** `migrate run` is run on a repository whose `spec/index.md` has no `id`, `migrate run` shall write the context's `id` into its frontmatter.
- [r12] **When** `migrate run` is run on a capability with Behaviour bullets that have no `[r<n>]`, `migrate run` shall give each of those bullets one, numbered from one above the highest id its capability has used or retired, in the order the bullets come.
- [r51] **When** `migrate run` gives a Behaviour bullet an id, `migrate run` shall leave the bullet's text unchanged.
- [r13] **When** `migrate run` is run on a capability with no `retired`, `migrate run` shall give it `retired: []`.
- [r52] **When** `migrate run` is run, `migrate run` shall write each capability's `id` as `capability/<context path>/<file name>`.
- [r14] **When** `migrate run` is run on a `decision/<name>` reference in frontmatter or a `## decision/<name>` heading, `migrate run` shall rewrite it as `design-decision/<name>`.
- [r53] **When** `migrate run` is run on an `obs/<x>` reference, `migrate run` shall rewrite it as `observation/<x>`.
- [r54] **When** `migrate run` is run on a `## obs/<x>` heading, `migrate run` shall rewrite it as `## observation/<context path>/<x>`.
- [r55] **When** `migrate run` is run, `migrate run` shall write each frontmatter `id` under `spec/decisions/` and `.shop/` as `<kind>/<context path>/<name>`.
- [r56] **When** `migrate run` rewrites a reference, `migrate run` shall change nothing else in it.
- [r15] **When** `migrate run` is run on a capability whose `formulated_as` is `features/<its file name>.feature`, `migrate run` shall remove its `formulated_as`.
- [r16] **If** a capability's `formulated_as` names any other file, then `migrate run` shall refuse, naming the capability and the file.
- [r17] **When** `migrate run` is run, `migrate run` shall move with git: `decisions/*.md` to `spec/decisions/`; `work/` to `.shop/work/`; `records/` to `.shop/records/`; `docs/superpowers/specs/` to `.shop/records/archive/design-notes/`; `docs/superpowers/plans/`, with its `archive/`, to `.shop/records/archive/plans/`; `docs/superpowers/requests/` to `.shop/records/archive/requests/`; `docs/superpowers/measurements/` to `.shop/records/measurements/`; `docs/superpowers/reports/` to `.shop/records/archive/reports/`; any other file under `docs/superpowers/` to `.shop/records/archive/` under its path below `docs/superpowers/`; and each other directory a ledger entry's `source` names a file in, such as `adrs/`, to `.shop/records/decision-arguments/`.
- [r18] **If** a file would be moved onto a file that exists, then `migrate run` shall refuse, naming both.
- [r19] **When** `migrate run` is run on a Markdown file under `.shop/records/`, other than `observations.md` and `README.md`, that has no frontmatter `id`, `migrate run` shall give it the frontmatter `id`, `kind`, `date` and `about` the bounded context.
- [r58] **When** `migrate run` gives a record an `id`, `migrate run` shall write it `<kind>/<context path>/<its file name without .md>`, lowercased, with each run of characters other than letters, digits and hyphens as one hyphen.
- [r59] **When** `migrate run` gives a record a `kind`, `migrate run` shall choose it by the record's directory: `decision-arguments/` and `archive/design-notes/` decision-argument, `measurements/` measurement, `review-findings/` review-finding, any other under `archive/` initiative-archive.
- [r60] **When** `migrate run` gives a `date` to a record whose name begins with a date, `migrate run` shall write that date.
- [r61] **When** `migrate run` gives a `date` to a record whose name begins with no date, `migrate run` shall write the date of the commit that added it.
- [r57] **When** `migrate run` gives a record frontmatter, `migrate run` shall keep any frontmatter the record had.
- [r20] **When** `migrate run` has moved files, `migrate run` shall rewrite each moved path, written in full from the root, to its new path in every tracked text file outside `.shop/records/`.
- [r62] **When** `migrate run` rewrites a moved path in a file other than Markdown, `migrate run` shall list the file with the line.
- [r21] **When** `migrate run` is run on a `.gitignore` with a `.superpowers/` line, `migrate run` shall rewrite that line as `.shop/scratch/`.
- [r63] **When** `migrate run` is run on a `.gitignore` with neither a `.superpowers/` nor a `.shop/scratch/` line, `migrate run` shall add `.shop/scratch/` to it.
- [r22] **When** `migrate run` is run on `spec/decisions.md`, `migrate run` shall write each entry whose name does not begin with four digits and a hyphen as the file `spec/decisions/<nnnn>-<name>.md`, `nnnn` its position in the ledger written in four digits.
- [r64] **When** `migrate run` is run on `spec/decisions.md`, `migrate run` shall write each entry whose name begins with four digits and a hyphen as the file `spec/decisions/<name>.md`.
- [r65] **When** `migrate run` has written `spec/decisions.md`'s entries as decision files, `migrate run` shall remove `spec/decisions.md`.
- [r23] **When** `migrate run` writes a decision file from a ledger entry, `migrate run` shall give it the frontmatter `id` `design-decision/<context path>/<name>`, `summary` the entry's text up to its first blank line or property line with its lines joined by a space, `date`, `status: accepted`, and each of the entry's `supersedes` and `revisit_when` the entry has.
- [r66] **When** `migrate run` writes a decision file from a ledger entry, `migrate run` shall write as its body `# <nnnn>. <name with hyphens as spaces>` and a `## Decision` section of the entry's text.
- [r24] **If** a ledger entry has a property line other than `date:`, `revisit_when:`, `supersedes:` or `source:`, then `migrate run` shall refuse, naming the entry.
- [r67] **If** a ledger entry has no `date:`, then `migrate run` shall refuse, naming the entry.
- [r25] **When** `migrate run` writes a decision's `source`, from a ledger entry or a decision file's own `source`, `migrate run` shall write as that file's record id each part of it, split at `;`, that begins with the path of a file the run moved, old or new.
- [r68] **When** `migrate run` writes a decision's `source`, `migrate run` shall keep as it is each part of it that is an id of a node kind.
- [r69] **When** `migrate run` writes a decision's `source`, `migrate run` shall write in `by`, joined with "; ", the rest of each part and every other part.
- [r26] **When** `migrate run` has written the decision files, `migrate run` shall write `spec/decisions/index.md` as `model decisions` writes it.
- [r27] **When** `migrate run` is run on a scenario tagged `@holding`, `migrate run` shall tag it `@deprecated` in place of `@holding`.
- [r70] **When** `migrate run` retags a scenario `@deprecated`, `migrate run` shall rewrite " (held)" at the end of its title as " (deprecated)".
- [r71] **When** `migrate run` retags a scenario `@deprecated`, `migrate run` shall rewrite its `Held for:` line as `Deprecated for:`.
- [r72] **When** `migrate run` retags a scenario `@deprecated`, `migrate run` shall change nothing else in it.
- [r28] **When** `migrate run` retitles a scenario, `migrate run` shall rewrite to the new title each `scenario(<feature>, "<old title>")` binding call under `--tests`, default `tests`, that names it.
- [r73] **When** `migrate run` rewrites a binding call, `migrate run` shall change nothing else in the module.
- [r29] **If** a test module under `--tests` does not parse, then `migrate run` shall refuse, naming the module.
- [r74] **If** a test module under `--tests` names an old title in a string written over several lines, then `migrate run` shall refuse, naming the module.
- [r30] **When** `migrate plan` is run without `--plan`, `migrate plan` shall read as the living plan the one `*-slices.md` directly in `.shop/records/archive/plans/`.
- [r75] **Where** `--plan` is given, `migrate plan` shall read as the living plan the file it names.
- [r31] **If** there is no living plan, then `migrate plan` shall refuse.
- [r76] **If** there are several living plans, then `migrate plan` shall refuse, naming those it found.
- [r32] **If** a slice of the plan is `in progress`, then `migrate plan` shall refuse, naming it.
- [r33] **When** `migrate plan` is run, `migrate plan` shall write each slice whose status is not green and that `--drop` does not name as a `planned` work-item `.shop/work/migrated-plan/slice-<n>.md`, `n` the slice's number with its dots as hyphens, with the id `work-item/<context path>/slice-<n>`, and `wkind` capability for a capability slice and enabling for an enabling or stack slice.
- [r77] **When** `migrate plan` writes a slice's work-item, `migrate plan` shall write as its body the slice's heading, its `Observable:`, `Unknown:`, `Needs:`, `Lands:` and `Status:` lines, and its place in the plan.
- [r34] **When** `migrate plan` writes a capability slice's work-item, `migrate plan` shall write it `under` the capability of its first `Scenarios:` entry's feature, `part_of` `capability-proposal/<context path>/migrated-<that capability>`, and `accepts` `<capability>#r<n>` for each `<feature> / <title>` entry, `@r<n>` being the requirement tag of the scenario of that title in `features/<feature>.feature`.
- [r35] **If** a `Scenarios:` entry names a title no scenario of its feature file has, then `migrate plan` shall refuse, naming the slice and the entry.
- [r78] **If** a `Scenarios:` entry names a scenario with no `@r<n>` tag, then `migrate plan` shall refuse, naming the slice and the entry.
- [r36] **When** `migrate plan` writes an enabling or stack slice's work-item, `migrate plan` shall write its `check` as the slice's `Check:` text, `for` the work-item of the first capability slice after it in the plan that becomes a work-item, and `part_of` that work-item's capability-proposal.
- [r37] **When** `migrate plan` is run on an enabling or stack slice after which no capability slice becomes a work-item, `migrate plan` shall write that slice as an observation in place of a work-item.
- [r38] **When** `migrate plan` is run, `migrate plan` shall append to `.shop/records/observations.md` each entry of the plan's Backlog, and each Log entry that begins `QUESTION FOR THE SPEC:`, `REQUEST` or `RE-FORMULATE` with its continuation lines, that `--leave` does not name, as `## observation/<context path>/<date>-backlog-<k>` or `<date>-log-<k>`, `k` counting that section's entries of that date from 1, with `about:` the bounded context, `by:` the plan's backlog or log, `date:`, and the entry's text as it was.
- [r39] **When** `migrate plan` writes any work-item, `migrate plan` shall write `.shop/work/migrated-plan/initiative.md`, the initiative `initiative/<context path>/migrated-plan`, kind capability-change, status started, priority 1, dated today, its source the observation `<today>-migrated-plan`.
- [r79] **When** `migrate plan` writes the initiative, `migrate plan` shall append the observation `<today>-migrated-plan`, naming the plan and how many slices it migrated.
- [r80] **When** `migrate plan` writes any work-item, `migrate plan` shall write, for each capability a work-item is under, `.shop/work/migrated-plan/migrated-<capability>.md`, a capability-proposal `part_of` the initiative, `argues` the capability, status formulated, dated today.
- [r40] **If** `.shop/work/migrated-plan/` exists, then `migrate plan` shall refuse.
- [r41] **When** `migrate plan` finds no slice to migrate, `migrate plan` shall write no initiative, proposal or work-item.
- [r81] **When** `migrate plan` finds no slice to migrate, `migrate plan` shall say so.
- [r82] **When** `migrate plan` finds no slice to migrate, `migrate plan` shall still write the observations.
- [r42] **When** `migrate plan` has run, `migrate plan` shall have written files in which `model check` reports no violation, unresolved reference or file problem.
- [r43] **When** `migrate plan --dry-run` is run, `migrate plan` shall list each slice it would migrate or drop and each entry it would make an observation, by the name `--drop` and `--leave` take.
- [r44] **If** `--drop` or `--leave` names a slice or entry the plan does not have, then `migrate plan` shall refuse, naming it.
- [r45] **If** `migrate` refuses, then `migrate` shall say why on stderr.
- [r83] **If** `migrate` refuses, then `migrate` shall exit 1.
- [r84] **If** `migrate` refuses, then `migrate` shall change no file.
- [r85] **If** `migrate` is given bad usage, then `migrate` shall exit 2.

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
~~~~~~

## `.shop/scratch/ears/alt/migration-tools.map.md`

~~~~~~
# migration-tools: map

Highest id before: r45 (retired: none). New ids: r46–r85. Lines 45 → 85.

| old id | new ids | pattern(s) | note |
|---|---|---|---|
| r1 | r1 | Ubiquitous | unchanged meaning |
| r2 | r2, r46 | Event-Driven, Event-Driven | print (r2) and exit 1 (r46) split; r46's trigger is "finds a thing of the old system" (see Q1) |
| r3 | r3, r47 | Event-Driven, Event-Driven | say (r3) and exit 0 (r47) split |
| r4 | r4 | Unwanted Behavior | system named `migrate`, refusing `run` and `plan` |
| r5 | r5 | Unwanted Behavior | "and changes no file" left to r84 (Q2) |
| r6 | r6, r48 | Unwanted Behavior ×2 | two conditions: malformed `--context` (r6), `--context` other than the existing `id` (r48); "changes no file" left to r84 (Q2) |
| r7 | r7, r49 | Optional ×2 | print (r7) and change no file (r49) split |
| r8 | r8 | Event-Driven | unchanged meaning; the per-step counts are part of the one printed response |
| r9 | r9 | Unwanted Behavior | unchanged meaning |
| r10 | r10, r50 | Event-Driven ×2 | change no file (r10), say nothing to migrate (r50) |
| r11 | r11 | Event-Driven | trigger made explicit: run on an index with no `id` |
| r12 | r12, r51 | Event-Driven ×2 | numbering (r12), text unchanged (r51) |
| r13 | r13, r52 | Event-Driven ×2 | `retired: []` (r13), capability `id` (r52) |
| r14 | r14, r53, r54, r55, r56 | Event-Driven ×5 | decision refs and headings (r14), obs refs (r53), obs headings (r54), frontmatter ids in full (r55), nothing else in a reference changes (r56) |
| r15 | r15 | Event-Driven | unchanged meaning |
| r16 | r16 | Unwanted Behavior | unchanged meaning |
| r17 | r17 | Event-Driven | one response, the list of moves kept |
| r18 | r18 | Unwanted Behavior | unchanged meaning |
| r19 | r19, r58, r59, r60, r61, r57 | Event-Driven ×6 | fields given (r19, `about` kept in it), id form (r58), kind by directory (r59), date from the name (r60), date from the adding commit (r61, the "or else"), existing frontmatter kept (r57) |
| r20 | r20, r62 | Event-Driven ×2 | rewrite (r20), list non-Markdown files with the line (r62) |
| r21 | r21, r63 | Event-Driven ×2 | `.superpowers/` line rewritten (r21), `.shop/scratch/` added when neither (r63) |
| r22 | r22, r64, r65 | Event-Driven ×3 | `<nnnn>-<name>.md` (r22), `<name>.md` when the name begins with four digits (r64), `spec/decisions.md` removed (r65) |
| r23 | r23, r66 | Event-Driven ×2 | was ubiquitous; trigger "writes a decision file from a ledger entry"; frontmatter (r23), body (r66); "where it has them" written as "each … the entry has" |
| r24 | r24, r67 | Unwanted Behavior ×2 | unknown property line (r24), no `date:` (r67) |
| r25 | r25, r68, r69 | Event-Driven ×3 | moved paths to record ids (r25), node ids kept (r68), the rest to `by` (r69) (Q3) |
| r26 | r26 | Event-Driven | unchanged meaning |
| r27 | r27, r70, r71, r72 | Event-Driven ×4 | tag (r27), title (r70), `Held for:` line (r71), nothing else changes (r72) |
| r28 | r28, r73 | Event-Driven ×2 | binding calls (r28), nothing else in the module (r73) |
| r29 | r29, r74 | Unwanted Behavior ×2 | module does not parse (r29), old title in a multi-line string (r74) |
| r30 | r30, r75 | Event-Driven, Optional | was ubiquitous with "or": default plan (r30), `--plan` (r75) |
| r31 | r31, r76 | Unwanted Behavior ×2 | no plan (r31), several (r76) (Q4) |
| r32 | r32 | Unwanted Behavior | unchanged meaning |
| r33 | r33, r77 | Event-Driven ×2 | the work-item and its fields (r33), its body (r77) |
| r34 | r34 | Event-Driven | one response, the fields listed |
| r35 | r35, r78 | Unwanted Behavior ×2 | unknown title (r35), scenario with no `@r<n>` (r78) |
| r36 | r36 | Event-Driven | one response, the fields listed |
| r37 | r37 | Event-Driven | was Optional (`Where`): the condition is an input, not an option |
| r38 | r38 | Event-Driven | one response, the observation form listed |
| r39 | r39, r79, r80 | Event-Driven ×3 | initiative (r39), the observation it appends (r79), the capability-proposals (r80) |
| r40 | r40 | Unwanted Behavior | "and changes no file" left to r84 (Q2) |
| r41 | r41, r81, r82 | Event-Driven ×3 | writes none (r41), says so (r81), still writes observations (r82) |
| r42 | r42 | Event-Driven | system named `migrate plan`; the response is the files it wrote, as `model check` reads them |
| r43 | r43 | Event-Driven | unchanged meaning |
| r44 | r44 | Unwanted Behavior | unchanged meaning |
| r45 | r45, r83, r84, r85 | Unwanted Behavior ×4 | why on stderr (r45), exit 1 (r83), change no file (r84), bad usage exits 2 (r85) |

## Scenario tags

There is no `features/migration-tools.feature` yet. When it is formulated, under 0052 the scenario of each
old id names the new ids with it (one scenario per old line, the number unchanged):

- r2's scenario: @r2, @r46
- r3's: @r3, @r47
- r6's: @r6, @r48
- r7's: @r7, @r49
- r10's: @r10, @r50
- r12's: @r12, @r51
- r13's: @r13, @r52
- r14's: @r14, @r53, @r54, @r55, @r56
- r19's: @r19, @r57, @r58, @r59, @r60, @r61
- r20's: @r20, @r62
- r21's: @r21, @r63
- r22's: @r22, @r64, @r65
- r23's: @r23, @r66
- r24's: @r24, @r67
- r25's: @r25, @r68, @r69
- r27's: @r27, @r70, @r71, @r72
- r28's: @r28, @r73
- r29's: @r29, @r74
- r30's: @r30, @r75
- r31's: @r31, @r76
- r33's: @r33, @r77
- r35's: @r35, @r78
- r39's: @r39, @r79, @r80
- r41's: @r41, @r81, @r82
- r45's: @r45, @r83, @r84, @r85

No line of this capability stated one tag per scenario.

## Questions

1. r2/r46: the old line said `migrate status` "exits 1" after printing, with no condition, and r3 says it
   exits 0 when it finds nothing. Choice: r46 exits 1 when it finds a thing of the old system, the reading
   r3 implies.
2. r5, r6 (and r48), r40: each ended "and changes no file". Splitting would give four lines saying what r84
   ("If `migrate` refuses, then `migrate` shall change no file") already says for every refusal. Choice: left
   to r84, no new line; the meaning stays in the capability. Say if each refusal should keep its own line.
3. r25/r69: "the rest of each part, and every other part, is written in `by`". Choice: kept the words ("the
   rest of each part"), read as the rest of a part after the moved path it begins with; the old line did not
   say whether a node id part has a "rest".
4. r31/r76: "refuses, naming those it found" applies to both no plan and several; with no plan there is
   nothing to name. Choice: r31 refuses without naming, r76 names the plans found.
5. r23: "the entry's `supersedes` and `revisit_when` where it has them" written as "each of the entry's
   `supersedes` and `revisit_when` the entry has", to keep one response with no second condition.
6. r11: "spec/index.md's frontmatter has the context's `id`, written when it had none" written as a write on
   an index with no `id`; when it has one, r48 already refuses a different `--context`, so nothing is lost.
~~~~~~
