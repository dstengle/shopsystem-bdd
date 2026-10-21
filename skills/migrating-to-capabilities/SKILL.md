---
name: migrating-to-capabilities
description: Use when a repository is on the old system and is to move to the final layout - approved Gherkin feature files and design notes under docs/superpowers/specs/ but no spec/ of capability files, capability files whose Behaviour lines have no [r<n>] ids, a ledger spec/decisions.md, top-level decisions/, work/, records/ or adrs/, docs/superpowers/, a living *-slices.md plan, or @holding scenarios - or when model check names scripts/migrate, or when asked to migrate a project to capability files, one feature per capability, or the final layout. Also use when tempted to keep the old feature file names so tests need no changes, or to move, number or re-id files by hand.
---

# Migrating to Capabilities

## Overview

Migration moves a repository onto the final layout in one pass (design-decision/migration-in-one-pass):
**`scripts/migrate` transcribes, the session judges.** `migrate run` makes every mechanical change: the moves, the
decision files from the ledger, the ids, the Behaviour numbers, the `@holding` deprecations and every reference to
what moved. The session asks the context path, holds the one gate, writes the first `spec/` where there is none,
maps scenarios to lines and tags them, and turns what the gate kept into work-items and observations. Never move,
number, re-id or rewrite a reference by hand where `migrate` does it; never edit what `migrate` wrote before its
commit.

**No approved scenario changes meaning, and the suite gives the same answer before and after.** Two commits: the
mechanical move, before the gate (spec-migration r22); then everything the gate led to.

Tools, all this plugin's (`<this skill's base directory>/../../scripts/`): `migrate`, `features`, `model`, `work`.
Format: `docs/capability-format.md`. Each one runs from the repository's top level.

## Preconditions (stop if any fails, before any change, saying why: r1)

- `git status --porcelain` prints nothing: no change, no untracked file. `migrate run` refuses otherwise.
- No work-item is `claimed`: no file under `work/` or `.shop/work/` has a `status: claimed` line
  (`grep -rl '^status: claimed' work .shop/work`).
- `.gitignore` has `.shop/scratch/`. If not, add the line and commit it alone, before the baseline.
- The suite runs by the project's own test command (its `CLAUDE.md`, Makefile or README; `python -m pytest` when
  none is stated). Record the baseline under `.shop/scratch/migration/`: the summary line; the passing tests
  (`-q -rA`); a copy of `features/`; and `features count --by-tag`. A suite that errors in collection or fails is
  not a baseline: stop and say so. Never repair it as part of the migration.

## Process

1. **The context path.** `<owner's domain>/<product>/<context name>`, e.g. `missingmass.io/demo/shelf`. Take it
   from `spec/index.md` when its frontmatter `id` is `bounded-context/<path>` in that form. Otherwise ask the
   person, and stop until they answer (r10): `migrate run` needs it, and nothing changes before it.

2. **The mechanical move.** `python3 <scripts>/migrate run --context <path>`.
   - Exit non-zero: it says `migrate changed nothing` and lists each change it could not make (a file already at a
     destination, a symbolic link, ledger text outside its entries, an uncommitted change, …). Show the list to the
     person and stop. Never work around a refusal by moving files yourself; the person resolves it, then run again.
   - Exit 0: every change is staged and nothing is committed. What `migrate` does not transcribe yet, the session
     does now, and nothing else:
     - each capability with no `retired:` gets `retired: []` (r9);
     - each `## obs/<x>` heading becomes `## observation/<path>/<x>`, and each `obs/<x>` reference
       `observation/<x>` (r14);
     - each scenario migrate deprecated from `@holding` (`git diff --cached -- features/` shows them): a title
       ending ` (held) (deprecated)` ends ` (deprecated)`; a `Held for: <why>` line becomes `Deprecated for: <why>`,
       and the `Deprecated for: removal` line migrate added beside it goes; then
       `features rebind "<old title>" "<new title>"` keeps its test bound (r18).
   - Then check it, against the baseline:
     - `git diff --cached --word-diff -- spec/capabilities/` shows only `[r<n>]` added to Behaviour lines, `id`
       and `retired:` lines and the removed `formulated_as`. A Behaviour line's words changed: stop and report it.
     - The suite: the same summary line (warnings aside) and the same passing scenarios by title, the deprecated
       ones by their ` (deprecated)` titles.
     - `features verify-moved --from .shop/scratch/migration/features` matches every scenario but those deprecated.
     - Each file other than Markdown that `git diff --cached --stat` shows changed (not only renamed): note it with
       each changed line, for the gate (r23).
   - Commit alone: `migrate: final layout`.

3. **Draft or map**, the agents in `.shop/scratch/drafts/<date>-migration/round-<n>/`, one directory a round. Note
   `git status --porcelain` before each dispatch; afterwards only an entry new since then is the agent's, and an
   agent that wrote outside its round goes back with those files removed.
   - **No `spec/capabilities/` before migration:** dispatch `capability-writer` with the migration brief below. The
     notes are now under `.shop/records/archive/design-notes/`, the ADRs under `.shop/records/decision-arguments/`.
     Check its mapping table: every existing scenario not `@deprecated` maps to exactly one line, named by its id;
     every line cites a note sentence or a scenario. A scenario with no row goes back to the agent.
   - **Capability files already there:** dispatch one `feature-formulator` per capability with this brief:

         Map the scenarios of features/<NAME>.feature to the lines of spec/capabilities/<NAME>.md.
         You may read those two files and nothing else. Write nothing but <ROUND>/<NAME>.reply.md:
         one row per scenario not tagged @deprecated, `<title> | r<n>[, r<m>…]`, each line it formulates;
         then each scenario that formulates no line, with the lines it comes nearest.

     A scenario may formulate several lines (design-decision/a-scenario-may-name-several-requirements): its row names each.

4. **Stop at the gate.** Show the person, in one message (r2, r16, r23):
   - the capabilities, and which old features' scenarios each receives;
   - every line no scenario backs (a note sentence with no scenario behind it: new contract);
   - every scenario that formulates no line, each as a question: a new line, or deprecated for removal;
   - each pair of scenarios with one title that would land in one capability, asking to retitle one (pytest-bdd
     binds one and drops the other without a word);
   - each glossary bullet of `spec/index.md` not in the form `- **<term>**: <one sentence>. Not: <word>.`, asking
     for the person's words;
   - the living plan, now under `.shop/records/archive/plans/`: each open slice (keep as a work-item, or drop), and
     each backlog and log entry that would become an observation (keep, or leave out; offer "all kept" for a long
     list);
   - each non-Markdown file of step 2 with its changed lines;
   - every other question, the writer's included.

   Lines written from approved scenarios are approved already; the mapping rows are transcription and need no
   approval. Wait for an explicit yes and every answer. Until then, change nothing beyond the mechanical move (r26).
   Answers that bear on drafts go back to the agent as another round.

5. **After the gate**, in this order:
   - **The first spec** (no capabilities before): copy the drafts into `spec/`, round by round in order, each
     decision file into `spec/decisions/`; run `model decisions` to rewrite `spec/decisions/index.md`.
   - **Re-pair** (the first spec, or any capability whose scenarios sit in several files): see Re-pairing below.
   - **Tag.** For each row, `features tag "<title>" r<n>`; with several lines, once per line. When `features`
     refuses a title because several files have it, run it again with `--file features/<name>.feature`.
   - **Deprecate** each scenario the answers deprecate: `features deprecate "<title>" --for-removal`, then
     `features rebind "<title>" "<title> (deprecated)"` (both take `--file`). A new line the answers asked for goes
     through integrating-a-proposal, its small-change path when it qualifies, with its own gate and commit, before
     its scenario is tagged; its hand-off to formulation is left out, since the scenario exists.
   - **Retitle** only what the person retitled, and apply each retitle to the baseline too.
   - **Glossary**: each bullet the gate answered, rewritten in the person's words (r21).
   - **Living plan** (r17): each open slice kept becomes a work-item,
     `work add <initiative> <name> --part-of <proposal or initiative id> --under <capability> --accepts <the ids
     its scenarios are tagged with>`. Each backlog and log entry not left out becomes an observation in
     `.shop/records/observations.md`: `## observation/<path>/<date>-<slug>`, then `about:`, `by:` and `date:`
     lines and the entry's text. A dropped slice stays only in the archived plan. (`migrate plan` will do this
     transcription once it exists; until then it is the session's, word for word from the plan.)
   - **Decision sources** (r19): where a decision file's `by` names a file that moved, add `source:` naming by id
     the record it became.
   - **Notes** (r8): head each note under `.shop/records/archive/design-notes/` with
     `Proposal, integrated into spec/ on <date>.`

6. **Verify**, against the baseline; any difference beyond what r5 sets aside: stop and report it (r6). Never edit
   a scenario to make the numbers match, and never a step definition's body (r7).
   - `features verify-moved --from .shop/scratch/migration/features` before the tags, when scenarios moved.
   - The same summary line; the same passing scenarios by title through the mapping (module paths in test ids
     change with rebinding); `features count --by-tag` equal but for the new `@r<n>` tags and the `@deprecated`
     the gate led to. Set aside: the gate's retitles, and the ` (deprecated)` titles of r18 and of the gate.
   - `model check --limit 100000` reports no violation, no unresolved reference and no file problem (none naming
     `scripts/migrate` means nothing is left to migrate), and `v_s3` (a requirement has no scenario) only for lines
     that had no scenario before (r20). Exit 2 with a message naming clingo and `pip install clingo` means clingo is
     missing: check the tags by hand and say so in the reply. Any other exit 2 is a failed run: stop and report it.
   - Nothing of the plugin is left under `docs/superpowers/` or `.superpowers/` (r15).

   Then commit `features/`, the test files, `spec/` and `.shop/` together: `spec: migrated, <n> lines, <m>
   scenarios tagged`.

7. **Hand off.** Approved unbacked lines go to formulating-features.

## Re-pairing

- One file `features/<name>.feature` per capability: `# formulated from spec/capabilities/<name>.md`,
  `Feature: <title>`, `  Narrator: <narrator>`. The old `So that …` line goes: Purpose has it.
- Move each mapped scenario in, in line order, verbatim, with
  `features move "<title>" --to features/<name>.feature --keep-feature-tags` (the old file's feature tags go onto
  the scenario), adding `--inline-background` where the capability's source files did not share one Background.
- A Background stays only if every source file of that capability had the same one. Otherwise each scenario's
  source Background is inlined as its first steps: its Background steps followed by its own are identical before
  and after (r4).
- Test bindings follow the step definitions, which never change. Where every step a capability's scenarios use has
  one body, one test module per capability binds its feature file (`scenarios(...)`), and step definitions from
  old modules move unedited to `conftest.py`. Where one step text has different bodies in different old modules,
  those modules stay, untouched, and each binds its own scenarios from the new file by title
  (`@scenario("<new file>", "<title>")`). A feature file bound by title anywhere is bound by title everywhere:
  each scenario is bound by exactly one module.
- Delete the old feature files, and the old test modules that no longer bind any scenario.

## The Migration Brief

```
Migration: this repository has no spec/capabilities/ yet. Write its first spec/.
The context path is <PATH>: spec/index.md's id is bounded-context/<PATH>.
spec/decisions/ already holds the decision files scripts/migrate wrote; number
yours on from the highest there.
Notes, oldest first (a later note supersedes an earlier one where they differ):
<NOTE PATHS under .shop/records/archive/design-notes/>
ADRs: <.shop/records/decision-arguments/ | none>, each with its record id.
Approved feature files: everything under features/.
You may read those notes, the ADRs, spec/decisions/, anything under features/,
and anything under docs/. Nothing else. Write your drafts under <ROUND>/ and
nowhere else.

Group lines into capabilities by narrator and cluster of behaviour, as if
the feature files had never been split. Their current names and boundaries
are not evidence; keeping them to spare renames is not a reason.

Write the drafts and reply with the parts your definition lists, the drafts'
paths, and the migration mapping table.
```

## Rationalizations

| Seen in baseline | Reality |
|---|---|
| "migrate refused on one file, so I moved that directory with `git mv` myself" | A refusal is the person's to resolve. migrate is all or nothing; a hand move is a second, unchecked migration |
| "Numbered the lines and rewrote the ids by hand: it was only three capabilities" | `migrate run` numbers from the highest id ever used and rewrites every reference; by hand misses both |
| Kept `spec/decisions.md` "for later", or renamed its headings to `## design-decision/…` | `migrate run` replaces the ledger with one file per entry and removes it; a ledger left is a file problem |
| "Named after the existing feature files, so no test had to be renamed" | Then the pairing is a label. Rebinding tests is this skill's job; group by behaviour |
| Unbacked rule written straight into Behaviour, "left unformulated" | A note line with no scenario is new contract. It goes to the gate first |
| The mechanical move and the tags in one commit | The move is its own commit, before the gate, with no line or scenario changed but r18's |
| A backlog entry rewritten as a tidier observation | An observation is the entry's own words; the gate decides only keep or leave out |
| "Eight step texts have two bodies, so re-pairing needs edited step definitions" | Bind by title from the module that owns the bodies |
| A scenario retyped into its new file, "verbatim" checked by test results | Every scenario by `features move`; `features verify-moved` checks them |

## Red Flags

- A file moved, a line numbered, an id or a reference rewritten by hand where `migrate run` does it
- `migrate run`'s staged changes edited before the `migrate: final layout` commit, beyond step 2's list
- A refusal of `migrate run` worked around instead of shown to the person
- Anything changed after the mechanical move and before the person's answers
- A capability file for every old feature file, with the same names
- A diff to any Given, When or Then line, a description, a tag other than the new `@r<n>` and the gate's
  `@deprecated`, or a title the person did not retitle at the gate or deprecate
- A step definition's body edited
- A verify step that compares counts but not the passing scenarios by title
- A suite that did not run cleanly before migration, recorded as the baseline
- A Behaviour line whose words changed
- An `@r<n>` tag on a `Feature:` line, or a scenario tagged that neither the mapping nor an answer placed
