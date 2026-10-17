---
name: formulating-features
description: Use when capability files under spec/ have changed and their Behaviour lines are approved, before any plan, step definition, or code exists for them. Also use when slicing-into-increments hands back a feature whose scenario meaning must change, or when a feature file is about to be written for the first time in a project.
---

# Formulating Features

## Overview

Each capability file `spec/capabilities/<name>.md` is formulated as one feature file `features/<name>.feature`, one scenario per Behaviour line. The lines were approved at integrating-a-proposal's gate, so a scenario formulated from an approved line needs no second approval: the person approves decisions, not transcription. Feature files are written from the narrator's side by an agent that cannot see the implementation. This skill supersedes superpowers:test-driven-development for deciding what gets tested.

A note under `docs/` is not the spec. If lines are not yet in `spec/`, integrating-a-proposal runs first.

## Who Does What

The session the person talks to hands a formulation round to `shopsystem-bdd:spec-round` and reads only its reply, for the reason integrating-a-proposal gives.

**If the person is talking to you:** dispatch one `spec-round` with the job `formulate`, the changed capability paths, the change list, a drafts path, the round's number and `Scripts:`, described `spec <note's name>: formulate round <n>`. It carries out steps 1, 2 and 4 below and commits. Step 3 is yours: each question in its reply goes to the person with its two readings; their answer goes to integrating-a-proposal as a round of its own, and the changed line comes back here as the next formulation round, for that capability alone. You do not dispatch a `feature-formulator`, read a draft or splice a scenario yourself.

**If you are `spec-round`:** steps 1, 2 and 4 are yours. A question is returned in your reply, never shown to anyone and never decided.

The small-change path below has no round: the session writes its scenarios itself.

## Process

1. **Dispatch the `feature-formulator` agent** (this plugin; it reads only the brief's paths and writes only drafts) with the brief below, once per changed capability. Give it no other paths. On a hand-back from slicing, use the hand-back brief instead. Choose the drafts path `.superpowers/spec-drafts/<date>-<capability name>/`. Each dispatch is a round with its own directory, `<drafts path>/round-<n>/`, named in its brief; the hand-back brief and a changed line coming back are later rounds. If `.gitignore` lacks `.superpowers/`, add it and commit that line alone. Then note `git status --porcelain`.
2. **Check coverage, both directions, one to one.** First, check `git status --porcelain` matches the porcelain noted before dispatch: only an entry new since then is the agent's, and an agent that wrote outside the drafts path goes back with those files removed. Every added or changed Behaviour line has exactly one scenario (or one outline), and every scenario carries the `@r<n>` tag of the line it formulates. This check is by hand, before writing, and it stands whatever clingo does: `scripts/model check` (at `<this skill's base directory>/../../scripts/`), run in step 4 once the files are written, finds a line with no scenario (`v_s3`) and a scenario that names no line or two (`v_s1`, `v_s2`), but not a line with two scenarios. A scenario with no line is removed. A line with no scenario goes back to the agent. A removed line's scenario is removed, or held (step 4). A scenario tagged `@holding` formulates no line: it is a line as it was, keeps the `@r<n>` tag it had, and is left out of this check (`model check` reads it as none). Feature files carry no slice tags from this skill; slicing adds `@slice-<n>` tags later and owns them.
3. **Route every question to the spec.** A line the agent returned as a question, because it admits two readings, gets no scenario. Show the person the question with its two readings. Their answer goes to integrating-a-proposal with its question brief, which changes the line; the changed line comes back here. The rest of the capability is not held up.
4. **Write the files**, round by round in order; a later round's scenario replaces an earlier round's. A new feature file is copied from its draft. In an existing one, only the new and changed scenarios are spliced in and the removed ones taken out; every other scenario, with its tags, stays byte for byte as it was. Check that before committing: an approved scenario missing or changed in the result goes back to the agent.
   **A scenario that passes today does not leave the suite here.** Its behaviour is still in the code, and stays tested until a slice makes it untrue. Before a changed scenario is spliced over the old one, and before a removed line's scenario is taken out, run the old scenario alone (`python -m pytest -q -k "<its name>"`). This is a run, not a reading: you open no step definition and no code.
   - It passes: hold it. `features hold "<old title>" --for "<the new scenario's title>"` (`--for-removal` for a removed line), then `features rebind "<old title>" "<old title> (held)"`, then splice the new scenario in after it. The held scenario keeps every step it had; it gains the tag `@holding`, " (held)" on its title and a `Held for:` line.
   - It fails or is not collected, because its slice was never built: replace or remove it as before. If its title changed, `features rebind "<old title>" "<new title>"`. A changed line keeps its id; when its new scenario keeps the old title, nothing is rebound.
   - When `features` refuses a title because several files hold it, it names them: run the same command again with `--file features/<name>.feature`, the capability's own feature file, and rebind in that file only: `features hold "<old title>" --for "<new title>" --file features/<name>.feature`, then `features rebind --file features/<name>.feature "<old title>" "<old title> (held)"`. `tag`, `retire` and `move` take `--file` the same way, and so does a `rebind` after them.

   Then `features bindings` must say every binding names a scenario: a binding that names a title no feature has stops its whole test module collecting. Once the files are written, run `scripts/model check --limit 100000` before the commit. It takes no path: it reads all of spec/ and features/. `--limit` is an option: without it, each rule shows ten rows and then `... and <n> more`. The failures that block the commit are `v_s1`, `v_s2` or `v_t1` for a scenario this round wrote; `v_s3` for a line this round formulated; a file problem naming a feature file this round wrote (two scenarios with one title, of which pytest-bdd binds one and drops the other without a word); and, for a line the change list removes, its old scenario still named by `v_s1` or by an `unresolved:` line, since this step removes or holds it. The rest of its output is not this round's. A scenario it names goes back to its formulator, as the other failures of this step do, and nothing is committed until those are clear. A repository whose Behaviour lines carry no `[r<n>]` ids is migrated to ids first (migrating-to-capabilities, "Adding Ids"), before formulation uses `model check`. Where it exits 2 with a message that names clingo and `pip install clingo`, clingo is missing: the reply says so and the hand check of step 2 stands. Any other exit 2 is a failed run, to be fixed and rerun. Then commit the feature files with the test files `rebind` changed, nothing else, and hand them to slicing-into-increments. A `v_t1` row of that run naming a scenario of a capability this round did not formulate is not this round's failure: after the commit, each such scenario goes through the small-change path below, for a word the glossary avoids. A `spec-round` lists those rows in its reply, and the session the person talks to takes them through that path.

## The Small-Change Path

For a small change (integrating-a-proposal's small-change path: at most two lines, no new capability, no contract change), write the scenarios yourself instead of dispatching the agent, by the brief's rules below, from the lines alone: read the capability and the feature file, never the code or the step definitions, so the scenario says what the narrator needs rather than what the code does. Check coverage and splice as in steps 2 and 4, then check and commit as step 4 does: `features bindings` and `model check` before the commit, the commit holding the feature files and the test files `rebind` changed.

A scenario that uses a word its context's glossary avoids (a word after `Not:` in `spec/index.md`'s Glossary, reported by `model check` as a `v_t1` row naming the scenario) is reworded to its line through this path, without a further gate: the line and the term were approved, and the scenario follows them. Change only the words the term replaces; the scenario keeps its `@r<n>` tag, and its title unless the title holds the word. A rewording that changes only the title is a rebind, `features rebind "<old title>" "<new title>"`, and nothing is handed to slicing: the steps and their test are as they were. A rewording that changes a step's text is a changed scenario: step 4 runs the old one alone and, when it passes, holds and rebinds it, splices the reworded one after it, and hands the reworded one to slicing-into-increments like any changed scenario. A held scenario is no scenario to `model check`, so it reports no `v_t1` for it.

## A Line Every Call Must Keep

A line that every call or command must keep, because it is a property of the boundary they all pass through (a damaged store refused, a busy store refused, a missing role refused), is formulated as one scenario per reason the line gives, each with one representative call, never as an Examples row per call. That every call goes through the boundary is the suite's job: one table-driven test lists every call and command and checks each answers through it. Rows per call multiply the suite by the number of calls and test one code path that many times.

## The Brief

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
  Each scenario carries the tag `@r<n>`, the id of the line it formulates, on the scenario's tag line
  directly above `Scenario:`; its title is free, and restating the line's condition makes a good one. A line with a Where and several
  configurations, or with several cases, is one Scenario Outline with an
  Examples table, never a scenario per case. A table of commands in
  Behaviour is one scenario per row. A boundary the line does not state is
  not a scenario. A line every call or command must keep is one scenario
  per reason it gives, with one representative call, never a row per call.
- Every scenario carries a one-line description between its title and its
  first step: what it pins, in plain words. It is not a step and does not
  restate the steps.
- Formulate from Behaviour only. Purpose and Not yet are context.
  Implementation, may change is never formulated, however testable it looks.
- Steps: Given is the state of the world in the narrator's words. When is one
  action by one named role, in the third person (`the customer applies`,
  never `I apply` or `my cart`). Then is an outcome the narrator can observe.
  A refusal reads `Then the code is rejected because <the reason the line
  names>`, never the message text, status code, or field name.
- Data tables and step arguments use the narrator's words: product, price,
  quantity, code, expiry. Amounts are plain decimals with no currency symbol.
- Use the terms of spec/index.md's Glossary for what they name, and never a
  word an entry lists after `Not:`.
- A line that admits two readings gets no scenario, including one written to
  hold under both. Return it as a question.

Write to <DRAFTS PATH>/round-<N>/, and nowhere else: (1) for a new feature, the file;
for an existing one, only the new and changed scenarios, each headed by the
line it formulates. Reply with (2) a coverage table with one row per line:
the line's id, the line (quoted) and the scenario title that formulates it; (3) questions:
each line with two readings, quoted, and the two readings, one line each;
(4) cases you noticed that no line mentions, one line each, with no scenario
written for them; and the drafts' paths. Write that same reply, last of all,
to <DRAFTS PATH>/round-<N>/<NAME>.reply.md.
```

## The Hand-back Brief

When `slicing-into-increments` logged a `RE-FORMULATE` entry, send this instead, filled in from that entry:

```
The scenario "<SCENARIO>" in features/<NAME>.feature was handed back during
implementation. The plan log at <PLAN PATH> has the RE-FORMULATE entry with
the evidence. You may read that feature file, the plan, anything under
spec/, and anything under features/. Nothing else.

Write the rewritten scenario to <DRAFTS PATH>/round-<N>/, and nowhere else, so that it
formulates its line in spec/capabilities/<NAME>.md and is consistent with
the rest of the feature. Change only the lines the evidence requires. Reply
with the draft's path. If the line does not decide it, write no scenario:
reply with the question, in one sentence, with the two readings. Write that
same reply, last of all, to <DRAFTS PATH>/round-<N>/<NAME>.reply.md.
```

The main agent checks `git status --porcelain` as in step 2, writes the drafted scenario over the old one, commits, and slicing resumes. A question in the reply goes to integrating-a-proposal as in step 3, and the scenario waits for the changed line.

## Why the agent cannot see the code or the note

Given the code, a writer describes what it does. Given only the spec, a writer describes what the narrator needs. The note is a proposal the spec has already absorbed; a writer given both formulates the difference. The restriction is structural: the agent has a path list, no edit or shell tools, and writes only drafts, not a request to pretend.

## Common Mistakes

| Seen in baseline | Fix |
|---|---|
| Formulator read `docs/superpowers/specs/…-design.md` beside the capability | The path list is `spec/` and `features/`. The note is not the spec |
| `apply-promotion-code.feature` against `formulated_as: features/promo-codes.feature` | The capability's own name, on both sides |
| `So that …, a customer can …` as line 2 | `# formulated from …`, `Feature:`, `Narrator:`. Purpose carries the value |
| 11 scenarios for 9 lines, "A cart of exactly 10 items can still take a code" | One scenario per line. A boundary the line doesn't state is a question, not a scenario |
| Two scenarios held for "your yes" because each picks a reading | No scenario picks a reading. The line goes back to integrating-a-proposal; the rest goes to slicing |
| "Applying a second code leaves the cart with one code", deciding replace over refuse | Deciding is the spec's job. Return the question |
| "Both scenarios use one of each product, so it doesn't matter yet whether items means units or products" | A scenario that holds under both readings pins neither. No scenario; return the question |
| `Then the customer is told "That code has expired"` | `Then the code is rejected because it has expired` |
| Eight scenarios, one per unacceptable input, each with the same Then | One Scenario Outline, eight Examples rows |
| An outline of seventeen rows, one per call, for "every call is refused when the store is damaged" | One scenario with one representative call; a table-driven test checks every call goes through the boundary |
| A re-worded scenario spliced over one that passes, its steps left bound to a title that is gone: 32 collection errors in one module, and the behaviour untested until its slice | Hold the old one, rebind it, `features bindings` before the commit |
| A scenario with no @r tag, found by its title alone | The tag names the line; the title is free |
| Three new scenarios and a coverage row for every unchanged line returned as text, a 4.8 KB reply, then spliced in by the controller | Drafts to the drafts path; the reply is the coverage table, questions and paths |
