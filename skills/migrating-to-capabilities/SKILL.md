---
name: migrating-to-capabilities
description: Use when a repository has approved Gherkin feature files and design notes under docs/superpowers/specs/ but no spec/ directory of capability files, or when asked to migrate a project to capability files, one feature per capability, or the stage-1 layout. Also use when tempted to keep the old feature file names so tests need no changes. Also use when a repository has spec/capabilities/ files whose Behaviour lines carry no [r<n>] ids.
---

# Migrating to Capabilities

## Overview

Migration is the first integration: `spec/` starts empty, every note is a proposal, and the approved feature files are evidence of behaviour the notes may not state. Its one piece of unique work is re-pairing: each capability gets one feature file, the existing scenarios move into it verbatim, and the tests and plan follow. **No approved scenario changes meaning, and the suite gives the same answer before and after.**

Format: `docs/capability-format.md` in this plugin. The gate is integrating-a-proposal's.

## Preconditions (stop if any fails)

- The working tree is clean, and no slice in the living `*-slices.md` is `in progress`.
- The suite runs by the project's own test command (its `CLAUDE.md`, Makefile or README; `python -m pytest` when none is stated). Record the baseline in a directory of its own under the scratch directory: the summary line; the passing tests (`-q -rA`); a copy of `features/` in the baseline directory; and `features count --by-tag` (this plugin's `scripts/features`, at `<this skill's base directory>/../../scripts/`). A suite that errors in collection or fails is not a baseline: stop and say so. Never repair it as part of the migration.

## Process

1. **Dispatch the `capability-writer` agent** with the migration brief below. Choose the drafts path `.superpowers/spec-drafts/<date>-migration/`, inside the repository; each dispatch is a round in its own `<drafts path>/round-<n>/`, named in its brief, as integrating-a-proposal's rounds are. If `.gitignore` lacks `.superpowers/`, add it and commit that line alone. Then note `git status --porcelain`.
2. **Check the mapping table.** First, check `git status --porcelain` matches the porcelain noted before dispatch: only an entry new since then is the agent's, and an agent that wrote outside the drafts path goes back with those files removed. Every existing scenario maps to exactly one line; every line cites a note sentence or a scenario. A scenario with no row goes back to the agent. Two scenarios with one title that land in one capability are a question for the gate: pytest-bdd binds one of them and drops the other without a word. The person's retitle is the one title change migration makes, and it is applied to the baseline too.
3. **Stop at the gate.** Show the person: the capabilities and which old features' scenarios each receives; every unbacked line (a note sentence with no scenario behind it: new contract); every question. Lines written from approved scenarios are approved already. Wait for an explicit yes and the answers; answers go back to the agent. Then copy the drafts into `spec/` round by round in order, `decisions.append.md` as `spec/decisions.md` under a `# Decisions` heading, and commit `spec/` alone.
4. **Re-pair**, the main agent:
   - One file `features/<name>.feature` per capability: `# formulated from spec/capabilities/<name>.md`, `Feature: <title>`, `  Narrator: <narrator>`. The old `So that …` line goes: Purpose carries it.
   - Move each mapped scenario in, in line order, verbatim: its tags (`@slice-<n>` included), title, description, steps, tables and Examples, with `features move "<title>" --to features/<name>.feature --carry-feature-tags` (the old file's feature tags go onto the scenario), adding `--inline-background` where the capability's source files did not share one Background.
   - A Background stays only if every source file of that capability had the same one. Otherwise each scenario's source Background is inlined as its first steps. The test: each scenario's Background steps followed by its own steps are identical before and after.
   - Test bindings follow the step definitions, which never change. Where every step a capability's scenarios use has one body, one test module per capability binds its feature file (`scenarios(...)`), and step definitions from old modules move unedited to `conftest.py`. Where one step text has different bodies in different old modules, those old modules stay, with their definitions, fixtures and constants untouched, and each binds its own scenarios from the new file by title (`@scenario("<new file>", "<title>")`) in place of `scenarios(...)`. A feature file bound by title anywhere is bound by title everywhere, since `scenarios(...)` would bind its scenarios a second time: each scenario is bound by exactly one module.
   - Rewrite the feature half of `Scenarios:` lines in the living `*-slices.md` and log the migration there. Batch implementation plans are history: leave them.
   - Delete the old feature files, and the old test modules that no longer bind any scenario.
5. **Verify** against the baseline: `features verify-moved --from <baseline>/features` prints `<n> scenarios match`; the same summary line (warnings aside); the same passing scenarios by title through the mapping table (module paths in test ids change with the rebinding; gate-approved retitles are applied to the baseline); `features count --by-tag` equal to the baseline's. Any difference: stop and report it. Never edit a scenario to make the numbers match. Commit features, tests and the slice plan together.
6. **Hand off.** Head each note with `Proposal, integrated into spec/ on <date>.` and commit. Approved unbacked lines go to formulating-features, then slicing.

## Adding Ids

A repository already on capability files, with no `[r<n>]` ids, is migrated to ids. Nothing changes meaning: lines keep their text, scenarios their steps and titles.

1. **Preconditions** as above, and the baseline: the summary line, the passing tests (`-q -rA`) and `features count --by-tag`. Choose the drafts path `.superpowers/spec-drafts/<date>-ids/`, as in Process step 1.
2. **Number the lines.** In each capability, give each Behaviour line `[r<n>]` in its order from r1, add `retired: []` to the frontmatter, and set its `id` to `<context id>/<name>`. The context id is the owner's domain, product and context name: take it from `spec/index.md` if it names them; otherwise stop and ask the person, and number nothing before the answer. Set the `id` in `spec/index.md`'s frontmatter to the context id too, when it is not that already. No line's text changes: `git diff --word-diff` shows only `[r<n>]` added in the Behaviour lines.
3. **Map the scenarios.** Dispatch a `feature-formulator` with this brief, once per capability:

       Map the scenarios of features/<NAME>.feature to the lines of spec/capabilities/<NAME>.md.
       You may read those two files and nothing else. Write nothing but <DRAFTS PATH>/round-1/<NAME>.reply.md:
       one row per scenario not tagged @holding, `<title> | r<n>`, the line it formulates; then each
       scenario that formulates no line or more than one, with the lines it touches.

4. **Stop at the gate.** Show the person the context id and every scenario the mapping could not place, each as a question. Wait for the answers. A scenario that is not placed is tagged by no one before its answer. The rows the mapping placed need no approval: they are transcription. An answer that places a scenario under no line leads one of two ways. The behaviour becomes a new line through integrating-a-proposal, and its scenario is tagged with that line's id once the line is committed. Or the scenario is held for removal, `features hold "<title>" --for-removal`, and `model check` reads a held scenario as none. Do this before step 5 and finish it before step 6.
5. **Tag.** Only after the gate. For each row, and each answer, `features tag "<title>" r<n>`; it makes `@r<n>` the scenario's one requirement tag and keeps its other tags. Held scenarios are left as they are, with no requirement tag. Nothing else in a feature file changes, but for the holds in step 4.
6. **Verify.** Run `scripts/model check` from this plugin, with no arguments: it reads the whole repository. It reports no id mismatch for `spec/index.md` or a capability, no `v15a`, `v_s1`, `v_s2`, and no `v_s3` but for lines that had no scenario before. Exit 2 with a message naming clingo and `pip install clingo` means clingo is missing: do this check by hand and say so in the reply. Any other exit 2 is a failed run: stop and report it. The summary line and passing tests equal the baseline's; `features count --by-tag` equals the baseline's but for the new `r<n>` tags and any `@holding` the gate led to. Then commit `spec/` and `features/` together, never before the gate: `spec: requirement ids, <n> lines, <m> scenarios tagged`.

## The Migration Brief

```
Migration: this repository has no spec/ yet. Write its first spec/.
Notes, oldest first (a later note supersedes an earlier one where they differ):
<NOTE PATHS>
ADRs: <adrs/ | none>. Approved feature files: everything under features/.
You may read those notes, the ADRs, anything under features/, and anything
under docs/. Nothing else. Write your drafts under <DRAFTS PATH>/round-1/ and
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
| "Named after the existing feature files, so no feature, test module or plan reference had to be renamed" | Then the old features are frozen and the pairing is a label. Rebinding tests is this skill's job; group by behaviour |
| Kept `So that …` under the new `Narrator:` line | The header is three lines; Purpose carries the value |
| Unbacked rule written straight into Behaviour, "left unformulated" | A note line with no scenario is new contract. It goes to the gate first |
| `spec/`, features and plan in one commit on the main branch, before anyone saw the lines | `spec/` is committed after the gate, alone. Re-pairing is its own commit, verified |
| "Eight step texts have two bodies, so re-pairing can't happen without editing step definitions" | Bind by title from the module that owns the bodies. Step text and bodies stay as they are |
| Baseline counts from a `--collect-only -q -m slice-<n>` loop, and no copy of `features/` to compare against | A copy of `features/` and `features count --by-tag`: the comparison needs the old scenarios, not only their number |
| The new feature file written whole by a heredoc, four scenarios retyped with their Backgrounds inlined by hand, "verbatim" checked by test results | The header by hand; every scenario by `features move`, `--inline-background` where Backgrounds differed; `features verify-moved` checks them |

## Red Flags

- A capability file for every old feature file, with the same names
- A diff to any Given, When or Then line, a description or a tag, or to a title the person did not retitle at the gate
- A scenario typed into a feature file, by hand or by a heredoc, instead of moved by `features move`
- A step definition's body edited while moving it
- A verify step that compares counts but not the passing scenarios by title
- A suite that did not run cleanly before migration, recorded as the baseline
- A Behaviour line whose words changed while it was numbered
- An @r<n> tag on a Feature: line
- A `features tag` run before the gate, or a scenario tagged that the mapping did not place
