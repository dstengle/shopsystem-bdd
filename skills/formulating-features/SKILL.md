---
name: formulating-features
description: Use when capability files under spec/ have changed and their Behaviour lines are approved, before any work-item, step definition, or code exists for them. Also use when the person rules a scenario an implementer handed back a formulation question, or when a feature file is about to be written for the first time in a project.
---

# Formulating Features

## Overview

Each capability file `spec/capabilities/<name>.md` is formulated as one feature file `features/<name>.feature`, one scenario per Behaviour line. The lines were approved at integrating-a-proposal's gate, so a scenario formulated from an approved line needs no second approval: the person approves decisions, not transcription. Feature files are written from the narrator's side by a dispatch that cannot see the implementation. It decides what gets tested.

A note under `docs/` is not the spec. If lines are not yet in `spec/`, integrating-a-proposal runs first.

## Who Does What

`work run` starts a formulation round: an `initiative-round` of the kind `formulate`, given the changed capability paths, the change list, a drafts path, the round's number, the initiative's name and `Scripts:`. No session writes a feature file.

You are `initiative-round`: steps 1, 2 and 4 are yours. A question is returned in your reply, never decided; step 3 is that reply. You end with your ledger line, appended with `work note` (see the agent's "The ledger").

## Process

1. **Dispatch the `feature-formulator` agent** (this plugin; it reads only the paths its input prompt lists and writes only drafts) with the template below, once per changed capability. Give it no other paths. On a hand-back the person ruled a formulation question, use the hand-back template instead. Choose the drafts path `.shop/scratch/drafts/<date>-<capability name>/`. Each dispatch is a round with its own directory, `<drafts path>/round-<n>/`, named in its input prompt; the hand-back template and a changed line coming back are later rounds. If `.gitignore` lacks `.shop/scratch/`, add it and commit that line alone. Then note `git status --porcelain`.
2. **Verify coverage, both directions, one to one.** First, verify that `git status --porcelain` matches the porcelain noted before dispatch: only an entry new since then is the agent's, and an agent that wrote outside the drafts path goes back with those files removed. Every added or changed Behaviour line has exactly one scenario (or one outline), and every scenario has exactly one `@r<n>` tag, that of the line it formulates (design-decision/a-scenario-names-one-requirement); a scenario with two goes back to the agent. This verification is by hand, before writing, and it stands whatever clingo does: `scripts/model check` (at `<this skill's base directory>/../../scripts/`), run in step 4 once the files are written, finds a line with no scenario (`v_s3` (a requirement has no scenario)) and a scenario that names no line (`v_s1` (a scenario names no requirement)), but not a line with two scenarios. A scenario with no line is removed. A line with no scenario goes back to the agent. A removed line's scenario is removed, or deprecated (step 4). A scenario tagged `@deprecated` formulates no line: it is a line as it was, keeps the `@r<n>` tag it had, and is left out of this check (`model check` reads it as none). Feature files get no tags from this skill but `@r<n>` and `@deprecated`.
3. **Route every question to the spec.** A line the agent returned as a question, because it admits two readings, gets no scenario. The question, with its two readings, goes in the round's reply. Its answer goes to integrating-a-proposal with its question template, which changes the line; the changed line comes back here. The rest of the capability does not wait for it.
4. **Write the files**, round by round in order; a later round's scenario replaces an earlier round's. A new feature file is copied from its draft. In an existing one, only the new and changed scenarios are spliced in and the removed ones taken out; every other scenario, with its tags, stays byte for byte as it was. Verify that before committing: an approved scenario missing or changed in the result goes back to the agent.
   **A scenario that passes today does not leave the suite here.** Its behaviour is still in the code, and stays tested until the work-item that turns its replacement green retires it. Before a changed scenario is spliced over the old one, and before a removed line's scenario is taken out, run the old scenario alone (`python -m pytest -q -k "<its name>"`). This is a run, not a reading: you open no step definition and no code.
   - It passes: deprecate it. `features deprecate "<old title>" --for "<the new scenario's title>"` (`--for-removal` for a removed line), then `features rebind "<old title>" "<old title> (deprecated)"` (both take `--file features/<name>.feature` when several feature files have the title, as the last bullet says), then splice the new scenario in after it. The deprecated scenario keeps every step it had; it gains the tag `@deprecated`, " (deprecated)" on its title and a `Deprecated for:` line.
   - It fails or is not collected, because its behaviour was never built: replace or remove it as before. If its title changed, `features rebind "<old title>" "<new title>"`. A changed line keeps its id; when its new scenario keeps the old title, nothing is rebound.
   - When `features` refuses a title because several files have it, it names them: run the same command again with `--file features/<name>.feature`, the capability's own feature file, and rebind in that file only: `features deprecate "<old title>" --for "<new title>" --file features/<name>.feature`, then `features rebind --file features/<name>.feature "<old title>" "<old title> (deprecated)"`. `tag`, `retire` and `move` take `--file` the same way, and so does a `rebind` after them: `rebind` never refuses an old title that several files have, it rebinds every binding of it, so `--file` limits it to the bindings of that feature file.

   Then `features bindings` must say every binding names a scenario: a binding that names a title no feature has stops its whole test module collecting. Once the files are written, run `scripts/model check --limit 100000` before the commit. It takes no path: it reads all of spec/ and features/. `--limit` is an option: without it, each rule shows ten rows and then `... and <n> more`. The failures that block the commit are `v_s1` (a scenario names no requirement) or `v_t1` (a word the glossary avoids) for a scenario this round wrote; `v_s3` (a requirement has no scenario) for a line this round formulated; a file problem naming a feature file this round wrote (two scenarios with one title, of which pytest-bdd binds one and drops the other without a word); and, for a line the change list removes, its old scenario still named by `v_s1` or by an `unresolved:` line, since this step removes or deprecates it. The rest of its output is not this round's. A scenario it names goes back to its formulator, as the other failures of this step do, and nothing is committed until those are clear. A repository whose Behaviour lines have no `[r<n>]` ids is migrated to ids first (migrating-to-capabilities, "Adding Ids"), before formulation uses `model check`. Where it exits 2 with a message that names clingo and `pip install clingo`, clingo is missing: the reply says so and the hand verification of step 2 stands. Any other exit 2 is a failed run, to be fixed and rerun. Then commit the feature files with the test files `rebind` changed, nothing else. The work-items that turn them green are drafted later, by `delivering-an-initiative`. A `v_t1` row of that run naming a scenario of a capability this round did not formulate is not this round's failure: after the commit, the round rewords each such scenario, as the next section says. The reply lists the rewording it did: the commit, and the scenarios reworded or deprecated.

## A Word the Glossary Avoids

A scenario that uses a word its context's glossary avoids (a word after `Not:` in `spec/index.md`'s Glossary, printed by `model check` as a `v_t1` row naming the scenario) is reworded to its line in a round of the kind `formulate`, without a further gate: the line and the term were approved, and the scenario follows them. For a `v_t1` row naming a scenario of a capability this round did not formulate, the round, after its own commit, dispatches one `feature-formulator` for that capability in a later round directory, with the template below and as change list the named scenario reworded to its line; it then verifies the porcelain and the coverage, splices, deprecates and rebinds as in steps 2 and 4, runs `features bindings` and `model check`, and commits, with no gate. The `v_t1` rows that reword's own check shows are not followed again in this round. Change only the words the term replaces; the scenario keeps its `@r<n>` tag, and its title unless the title contains the word. A rewording that changes only the title is a rebind, `features rebind "<old title>" "<new title>"` (with `--file features/<name>.feature` when several feature files have the old title), and no work-item follows from it: the steps and their test are as they were. A rewording that changes a step's text is a changed scenario: step 4 runs the old one alone and, when it passes, deprecates and rebinds it, splices the reworded one after it; the reworded one is a changed scenario like any other, for a work-item to turn green and retire the old one. A deprecated scenario is no scenario to `model check`, so it prints no `v_t1` for it.

## A Line Every Call Must Keep

A line that every call or command must keep, because it is a property of the boundary they all pass through (a damaged store refused, a busy store refused, a missing role refused), is formulated as one scenario per reason the line gives, each with one representative call, never as an Examples row per call. That every call goes through the boundary is the suite's job: one table-driven test lists every call and command and verifies each answers through it. Rows per call multiply the suite by the number of calls and test one code path that many times.

## The Template

Send this to the agent verbatim, with the paths and lines filled in.

```
Formulate spec/capabilities/<NAME>.md as features/<NAME>.feature.
The approved changes to formulate: <THE CHANGE LIST ROWS, OR "every line">.
You may read anything under spec/ and anything under features/. Nothing else:
not docs/, not the source.

The file has this shape:

- File name: features/<NAME>.feature, the capability's own name.
- Line 1: `# formulated from spec/capabilities/<NAME>.md`
- Line 2: `Feature: <the capability's title>`
- Line 3: `  Narrator: <the capability's narrator>`
- A Background only for a fixed date or shared products, nothing else.
- One scenario per Behaviour line, in the lines' order, and no others.
  Each scenario has one tag `@r<n>`, the id of the one line it formulates, on the scenario's tag line
  directly above `Scenario:`, and never a second `@r<n>`: two lines that need the same setup or check
  get a scenario each, their steps shared in code; its title is free, and restating the line's condition makes a good one. A line with a Where and several
  configurations, or with several cases, is one Scenario Outline with an
  Examples table, never a scenario per case. A table of commands in
  Behaviour is one scenario per row. A boundary the line does not give is
  not a scenario. A line every call or command must keep is one scenario
  per reason it gives, with one representative call, never a row per call.
- Every scenario has a one-line description between its title and its
  first step: what it pins, in plain words. It is not a step and does not
  restate the steps.
- Formulate from Behaviour only. Purpose and Not yet are context.
  Implementation, may change is never formulated, however testable it looks.
- Steps: Given is the world as it stands, in the narrator's words. When is one
  action by one named role, in the third person (`the customer applies`,
  never `I apply` or `my cart`). Then is what the narrator can observe.
  A refusal reads `Then the code is rejected because <the reason the line
  names>`, never the message text, status code, or field name. A command
  exits successfully or exits with an error, never with an exit code.
- Data tables and step arguments use the narrator's words: product, price,
  quantity, code, expiry. Amounts are plain decimals with no currency symbol.
- Use the terms of spec/index.md's Glossary for what they name, and never a
  word an entry lists after `Not:`.
- A line that admits two readings gets no scenario, including one written to
  be true under both. Give it back as a question.

Write to <DRAFTS PATH>/round-<N>/, and nowhere else: (1) for a new feature, the file;
for an existing one, only the new and changed scenarios, each headed by the
line it formulates. Reply with (2) a coverage table with one row per line:
the line's id, the line (quoted) and the scenario title that formulates it; (3) questions:
each line with two readings, quoted, and the two readings, one line each;
(4) cases you noticed that no line mentions, one line each, with no scenario
written for them; and the drafts' paths. Write that same reply, last of all,
to <DRAFTS PATH>/round-<N>/<NAME>.reply.md.
```

## The Hand-back Template

When an implementer handed a scenario back (its outcome `HAND-BACK`, its work-item `awaiting-ruling`) and the person ruled it a formulation question, send this instead, filled in from the implementer's report in the work-item's stage directory, `.shop/work/<initiative>/runs/<work-item>/<k>-implement/report.md`:

```
The scenario "<SCENARIO>" in features/<NAME>.feature was handed back during
implementation. The implementer's report at <REPORT PATH> has the hand-back
with the evidence, and the person's ruling is: <THE RULING, IN THEIR WORDS>.
You may read that report, anything under spec/, and anything under features/.
Nothing else.

Write the rewritten scenario to <DRAFTS PATH>/round-<N>/, and nowhere else, so that it
formulates its line in spec/capabilities/<NAME>.md and is consistent with
the rest of the feature. Change only the lines the evidence requires. Reply
with the draft's path. If the line does not decide it, write no scenario:
reply with the question, in one sentence, with the two readings. Write that
same reply, last of all, to <DRAFTS PATH>/round-<N>/<NAME>.reply.md.
```

The session verifies `git status --porcelain` as in step 2, writes the drafted scenario over the old one and commits; the work-item goes through `work run` again. A question in the reply goes to integrating-a-proposal as in step 3, and the scenario waits for the changed line.

## Why the agent cannot see the code or the note

Given the code, a writer describes what it does. Given only the spec, a writer describes what the narrator needs. The note is a proposal the spec has already absorbed; a writer given both formulates the difference. The restriction is structural: the agent has a path list, no edit or shell tools, and writes only drafts, not a request to pretend.

## Common Mistakes

| Seen in baseline | Fix |
|---|---|
| Formulator read `a note under docs/` beside the capability | The path list is `spec/` and `features/`. The note is not the spec |
| `apply-promotion-code.feature` for the capability `promo-codes` | The capability's own name, on both sides: `features/promo-codes.feature`; no `formulated_as` field names it |
| `So that …, a customer can …` as line 2 | `# formulated from …`, `Feature:`, `Narrator:`. Purpose has the value |
| 11 scenarios for 9 lines, "A cart of exactly 10 items can still take a code" | One scenario per line. A boundary the line doesn't give is a question, not a scenario |
| Two scenarios kept back for "your yes" because each picks a reading | No scenario picks a reading. The line goes back to integrating-a-proposal; the rest is formulated |
| "Applying a second code leaves the cart with one code", deciding replace over refuse | Deciding is the spec's work. Give back the question |
| "Both scenarios use one of each product, so it doesn't matter yet whether items means units or products" | A scenario that is true under both readings pins neither. No scenario; return the question |
| `Then the customer is told "That code has expired"` | `Then the code is rejected because it has expired` |
| Eight scenarios, one per unacceptable input, each with the same Then | One Scenario Outline, eight Examples rows |
| An outline of seventeen rows, one per call, for "every call is refused when the store is damaged" | One scenario with one representative call; a table-driven test verifies every call goes through the boundary |
| A re-worded scenario spliced over one that passes, its steps left bound to a title that is gone: 32 collection errors in one module, and the behaviour untested until its work-item | Deprecate the old one, rebind it, `features bindings` before the commit |
| A scenario with no @r tag, found by its title alone | The tag names the line; the title is free |
| Three new scenarios and a coverage row for every unchanged line returned as text, a 4.8 KB reply, then spliced in by the session | Drafts to the drafts path; the reply is the coverage table, questions and paths |
