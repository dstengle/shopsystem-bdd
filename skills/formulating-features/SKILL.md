---
name: formulating-features
description: Use when capability files under spec/ have changed and their codified requirements are approved, before any work-item, step definition, or code exists for them. Also use when the person rules on a scenario an implementer handed back, or when a feature file is about to be written by hand, edited, or deprecated.
---

# Formulating Features

## Overview

A feature file is generated, never written. Each codified service capability `spec/capabilities/<name>.md` gives `features/<name>.feature`, one scenario a group, by `features generate` (`docs/capability-format.md`, The feature file). The requirements were approved at integrating-a-proposal's gate, and the generator is mechanical, so a generated scenario needs no approval and no session.

## Who Does What

`work run` formulates as a script, with no session: for an approved capability-proposal it runs `features generate <capability>` for each service capability the proposal names, then `features generate --check` and `model check` (no row it did not show before), commits `features/`, and sets the proposal `formulated`. It runs under the round lock, one at a time across initiatives. A guarantees capability has no feature. A capability whose file is not codified is refused, naming `migrate upgrade`.

By hand, outside `work run`, the same commands do the same: `python3 <scripts>/features generate <capability>`, `features generate --check`, and `features generate --preview <drafted file>` to see what a draft would give.

## Rules

- **Never write, edit or deprecate a scenario by hand.** The generator owns every feature file it wrote (its header says so); `features generate --check` fails on a hand edit.
- **A wrong scenario is a wrong requirement or a plugin defect.** If the scenario says what its group says, and that is not what is wanted, the requirement is wrong: it goes back to integration (integrating-a-proposal's question path). If the scenario does not say what its group says (a wrong witness, a step the vocabulary words badly, a construct the generator refuses), the grammar or the generator is wrong: raise a request to the plugin with the `raising-a-request` skill, naming the group and the generated text. Neither is fixed in the feature file.
- **A removed requirement's scenario goes with the regeneration.** The work-item drafted from the proposal's `removes` takes out the handlers and code only it used; its check is the whole suite.
- **Step text comes from the step vocabulary** (`features vocab`). An implementer writes handlers for new vocabulary uses (`tests/scenarios/<cap>_handlers*.py`) and never edits a feature.

## When generation refuses

`features generate` exits 1 naming the requirement it has no step for (a `shall not` with a command, an actor holding a resource outside a logic-only group, a condition whose `Means:` is not "its <attribute> is …"). Reword the requirement within the language (integration), or raise the missing construct to the plugin. Exit 2 names a capability that is not codified: run `migrate upgrade` first.

## Common Mistakes

| Seen | Fix |
|---|---|
| A scenario edited to match what the code does | The requirement is the contract: a question for integration, or a red scenario |
| A scenario added for a case no requirement names | Write the requirement; its group generates the scenario |
| `@deprecated` added to keep an old scenario running | Removal is a `removes` work-item; the whole suite is its check |
| A formulator session started for a capability | There is none: `features generate` |
