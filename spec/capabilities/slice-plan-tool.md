---
id: missingmass.io/shopsystem/shopsystem-bdd/slice-plan-tool
title: Slice plan tool
narrator: an agent or session editing a living slice plan
group: service
rests_on: [decision/scripts-stdlib-only, decision/slice-budget-refused-by-plan, decision/suite-record-holds]
formulated_as: features/slice-plan-tool.feature
retired: []
---

# Slice plan tool

## Purpose
`scripts/plan` edits and reads a repository's living slice plan: it appends log and backlog entries, sets a
slice's status and `Lands:` line, adds slices, shows open slices, requests and the last suite record, says
whether that record still holds, and archives a batch's green slices. Every read and write validates the plan's
shape and its slice budget. It is not a scheduler and does not run the suite; it only keeps the plan file valid.

## Behaviour
- [r1] **If** the plan is not valid — its title, slice order, section order, a slice's Kind, Status, Scenarios or Check lines — `plan` refuses every command, naming every problem, and leaves the file as it was.
- [r2] **If** an edit would make the plan invalid, `plan` refuses it, naming every problem, and leaves the file as it was.
- [r3] **When** `plan check` is run on a valid plan, `plan` says it is ok and exits 0.
- [r4] A section `plan` does not know is kept byte for byte through every edit.
- [r5] **When** `plan log <text>` or `plan backlog <text>` is run, `plan` appends `- <date> <text>` to the Log or Backlog section, the date being `--date` or today.
- [r6] **Where** the Backlog or Log section is missing, **when** a command needs it, `plan` creates it in its place in the section order.
- [r7] **When** `plan status <n> <status>` is run, `plan` sets slice `<n>`'s Status and changes nothing else.
- [r8] **If** `plan status` is given a status that is not `planned`, `in progress` or `green`, each with an optional `: <note>`, or `blocked: <why>`, `plan` refuses and leaves the file as it was.
- [r9] **If** `plan status` names a slice the plan does not have, `plan` refuses.
- [r10] **When** `plan add-slice <n> <name>` is run, `plan` writes the slice in number order, with Status planned. It compares dotted numbers part by part as whole numbers, so `2.10` follows `2.9` and `1` precedes `1.1`.
- [r11] **If** `plan add-slice` gives a slice the wrong one of Scenarios and Check for its Kind, or a number the plan already has, `plan` refuses and leaves the file as it was.
- [r12] **Where** `plan add-slice` is given no `--lands`, `plan` writes the slice and says on stderr that it has no Lands line and how to set it; with `--lands` it writes the line and says nothing.
- [r13] **If** a slice's Lands line counts more than 8 production or 4 test modules, `plan` refuses, naming the slice, its Lands and the budget, whatever the command, and leaves the file as it was.
- [r14] **If** a slice has more than one Lands line, or a Lands line written any other way than `- Lands: <p> production, <t> test`, `plan` refuses, naming the slice.
- [r15] A slice without a Lands line is valid.
- [r16] **When** `plan lands <n> "<p> production, <t> test"` is run, `plan` sets slice `<n>`'s Lands line, replacing any it had.
- [r17] **When** `plan show --open` is run, `plan` prints each slice that is not green with its name and status.
- [r18] **When** `plan show --requests` is run, `plan` prints the Log's REQUEST entries.
- [r19] **When** `plan show --last-suite` is run, `plan` prints the Log's last `Suite:` entry.
- [r20] **Where** `--current` is given with `--last-suite`, `plan show` prints the record, then `current` and exits 0 when no path outside `docs/superpowers/plans/` has changed since the commit it names, or `stale:` with the reason and exits 1.
- [r21] **If** the suite record names a commit the repository does not have, `plan show --last-suite --current` says it is stale because of that commit and exits 1.
- [r22] **If** `--current` is given without `--last-suite`, `plan` exits 2 as bad usage.
- [r23] **When** `plan archive <batch>` is run, `plan` writes the green slices and the whole Log to `archive/<plan file name without .md>-<batch>.md` beside the plan, so `foo-slices.md` archives to `archive/foo-slices-<batch>.md`, and removes those slices from the plan.
- [r24] **When** `plan archive` is run, `plan` leaves the Log holding the REQUEST, RE-FORMULATE and QUESTION FOR THE SPEC: entries with their continuation lines, one line naming the archive and the last `Suite:` entry, and that `Suite:` entry again, so `plan show --last-suite --current` still finds it.
- [r25] **If** the archive file exists or no slice is green, `plan archive` refuses.
- [r26] `plan` works on the plan `--file` names, or else on the one `docs/superpowers/plans/*-slices.md` under the current directory.
- [r27] **If** no `--file` is given and the current directory holds no `docs/superpowers/plans/*-slices.md` or several, `plan` refuses every command, saying how many it found and to name the plan with `--file`.
- [r28] **If** the plan file cannot be read, `plan` refuses, naming the file.
- [r29] **When** `plan show --backlog` is run, `plan` prints each Backlog entry with its continuation lines, and nothing when the Backlog is empty or missing.
- [r30] **When** `plan show --requests` or `plan show --last-suite` without `--current` is run, `plan` prints each entry with its continuation lines.
- [r31] **If** the Log has no `Suite:` entry, `plan show --last-suite` prints nothing and exits 0, and with `--current` `plan` refuses because there is no suite record.
- [r32] **If** the suite record names no commit, `plan show --last-suite --current` says it is stale because the record names no commit, and exits 1.
- [r33] **When** `plan show --last-suite --current` finds files changed, committed or not, outside `docs/superpowers/plans/` since the record's commit, the stale reason gives how many and names each.
- [r34] **If** `plan lands` names a slice the plan does not have, `plan` refuses and leaves the file as it was.
- [r35] `plan` takes a slice as green, for `show --open` and `archive`, by the word before its Status's colon, so a Status of `green: <note>` is green.
- [r36] **When** `plan archive` is run, `plan` creates the `archive/` directory beside the plan when it is missing, and the archive file begins with the plan's title.
- [r37] **Where** `--date` is given to `plan archive`, the Log's line naming the archive carries that date, and otherwise today's.
- [r38] **If** `plan` refuses a command or an edit, it says why on stderr and exits 1.

## Implementation, may change
- The plan is `--file`, or the one `docs/superpowers/plans/*-slices.md` under the current directory; with none
  or several, `plan` refuses and says to name it with `--file`.
- Shape: a `# ` title, then `## Slice <n>: <name>` blocks, then the sections 'Satisfied by existing
  behaviour', 'Backlog' and 'Log', each at most once, in that order. A slice has `- Kind:` (capability,
  enabling or stack), `- Status:`, and `- Scenarios:` (capability) or `- Check:` (enabling, stack). Only the
  word before a Status's colon decides whether a slice is green.
- `add-slice` writes Kind, Scenarios or Check, Observable, Unknown (default none), Needs (default none),
  Lands when given, and Status, in that order; `lands` puts its line just before Status.
- Staleness uses `git diff --name-only <commit>` and `git status --porcelain`, run in the current directory;
  the commit is the record's `at <hash>`.
- An entry's continuation lines are the indented lines after its bullet.
- Exit status: 0 success, 1 a check failed or an edit was refused, 2 bad usage.

## Not yet
None.
