---
name: migrating-to-capabilities
description: Use when a repository has approved Gherkin feature files and design notes under docs/superpowers/specs/ but no spec/ directory of capability files, or when asked to migrate a project to capability files, one feature per capability, or the stage-1 layout. Also use when tempted to keep the old feature file names so tests need no changes.
---

# Migrating to Capabilities

## Overview

Migration is the first integration: `spec/` starts empty, every note is a proposal, and the approved feature files are evidence of behaviour the notes may not state. Its one piece of unique work is re-pairing: each capability gets one feature file, the existing scenarios move into it verbatim, and the tests and plan follow. **No approved scenario changes meaning, and the suite gives the same answer before and after.**

Format: `docs/capability-format.md` in this plugin. The gate is integrating-a-proposal's.

## Preconditions (stop if any fails)

- The working tree is clean, and no slice in the living `*-slices.md` is `in progress`.
- The suite runs by the project's own test command (its `CLAUDE.md`, Makefile or README; `python -m pytest` when none is stated). Record the baseline in a directory of its own under the scratch directory: the summary line; the passing tests (`-q -rA`); a copy of `features/` in the baseline directory; and `features count --by-tag` (this plugin's `scripts/features`, at `<this skill's base directory>/../../scripts/`). A suite that errors in collection or fails is not a baseline: stop and say so. Never repair it as part of the migration.

## Process

1. **Dispatch the `capability-writer` agent** with the migration brief below. Choose the drafts path `.superpowers/spec-drafts/<date>-migration/`, inside the repository; each dispatch is a round in its own `<drafts path>/round-<n>/`, named in its brief, as integrating-a-proposal's rounds are. If `.gitignore` lacks `.superpowers/`, add it and commit that line alone.
2. **Check the mapping table.** First, check `git status --porcelain` shows nothing but that `.gitignore` line: an agent that wrote outside the drafts path goes back with its files removed. Every existing scenario maps to exactly one line; every line cites a note sentence or a scenario. A scenario with no row goes back to the agent. Two scenarios with one title that land in one capability are a question for the gate: pytest-bdd binds one of them and drops the other without a word. The person's retitle is the one title change migration makes, and it is applied to the baseline too.
3. **Stop at the gate.** Show the person: the capabilities and which old features' scenarios each receives; every unbacked line (a note sentence with no scenario behind it: new contract); every question. Lines written from approved scenarios are approved already. Wait for an explicit yes and the answers; answers go back to the agent. Then copy the drafts into `spec/` round by round in order, `decisions.append.md` as `spec/decisions.md` under a `# Decisions` heading, and commit `spec/` alone.
4. **Re-pair**, the main agent:
   - One file `features/<name>.feature` per capability: `# formulated from spec/capabilities/<name>.md`, `Feature: <title>`, `  Narrator: <narrator>`. The old `So that …` line goes: Purpose carries it.
   - Move each mapped scenario in, in line order, verbatim: its tags (`@slice-<n>` included), title, description, steps, tables and Examples, with `features move "<title>" --to features/<name>.feature`, adding `--inline-background` where the capability's source files did not share one Background.
   - A Background stays only if every source file of that capability had the same one. Otherwise each scenario's source Background is inlined as its first steps. The test: each scenario's Background steps followed by its own steps are identical before and after.
   - Test bindings follow the step definitions, which never change. Where every step a capability's scenarios use has one body, one test module per capability binds its feature file (`scenarios(...)`), and step definitions from old modules move unedited to `conftest.py`. Where one step text has different bodies in different old modules, those old modules stay, with their definitions, fixtures and constants untouched, and each binds its own scenarios from the new file by title (`@scenario("<new file>", "<title>")`) in place of `scenarios(...)`. A feature file bound by title anywhere is bound by title everywhere, since `scenarios(...)` would bind its scenarios a second time: each scenario is bound by exactly one module.
   - Rewrite the feature half of `Scenarios:` lines in the living `*-slices.md` and log the migration there. Batch implementation plans are history: leave them.
   - Delete the old feature files, and the old test modules that no longer bind any scenario.
5. **Verify** against the baseline: `features verify-moved --from <baseline>/features` prints `<n> scenarios match`; the same summary line (warnings aside); the same passing scenarios by title through the mapping table (module paths in test ids change with the rebinding; gate-approved retitles are applied to the baseline); `features count --by-tag` equal to the baseline's. Any difference: stop and report it. Never edit a scenario to make the numbers match. Commit features, tests and the slice plan together.
6. **Hand off.** Head each note with `Proposal, integrated into spec/ on <date>.` and commit. Approved unbacked lines go to formulating-features, then slicing.

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
