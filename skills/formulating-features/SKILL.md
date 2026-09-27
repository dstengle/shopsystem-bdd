---
name: formulating-features
description: Use when a design spec has been approved and Gherkin feature files must be written for it before any plan, step definition, or code exists. Also use when slicing-into-increments hands back a feature whose scenario meaning must change, or when a feature file is about to be written for the first time in a project.
---

# Formulating Features

## Overview

Feature files are the contract the human approves and the code must satisfy. They are written from the customer's side of the system by someone who cannot see the implementation. This skill produces them and stops at the approval gate. It supersedes superpowers:test-driven-development for deciding what gets tested.

## Process

1. **Dispatch the `feature-formulator` agent** (provided by this plugin, read-only tools) with the brief below. Fill in the spec path. Give it no other paths. On a hand-back from slicing, use the hand-back brief instead.
2. **Check the coverage report** it returns, both directions: every business rule in the spec maps to at least one scenario, and every scenario cites the spec sentence that requires it. A scenario with no citation is removed. A rule with no scenario goes back to the agent. Feature files carry no tags from this skill; slicing adds `@slice-<n>` tags later and owns them.
3. **Write the files** under `features/` exactly as returned, then commit them alone.
4. **Sort the scenarios by what decides them.** A scenario is *settled* when the coverage table cites a spec sentence that requires it and admits one reading; it is *deciding* when it fixes something the spec leaves open, chooses between two readings of the spec, or changes what an approved scenario means. The brief the agent returns marks each row one or the other, and that mark stands: the main agent may move a row from settled to deciding when it sees a second reading, never from deciding to settled, because the agent that could not see the code is the one that judged the spec. Settled scenarios need no approval: hand them to slicing-into-increments now. Deciding scenarios wait.
5. **Stop for approval of the deciding scenarios only.** Show the person those scenarios with the two readings, and wait for an explicit yes on each. Do not write step definitions or code for them until then, and slicing does not place them until then. When nothing is deciding, say so in one line and continue; the person is not asked to approve what the spec already said. When a hand-back from slicing triggered this skill, the changed scenario is settled if the rewrite cites the sentence that decides it, and deciding otherwise.

## The Brief

Send this to the agent verbatim, with the path filled in.

```
Write the Gherkin feature file(s) for the approved spec at <SPEC PATH>.
You may read that file, anything under docs/, and anything under features/. Nothing else.

Each feature file has this shape:

- File name: features/<what-the-customer-does>.feature, a verb phrase in the
  customer's words (redeem-promotion-code, not promo_codes). One file per
  customer-facing capability.
- Line 1: `Feature: <capability>`.
- Line 2: `So that <the value from the spec>, <role> can <capability>.`
- A Background only for a fixed date or shared products, nothing else.
- Scenarios, in this order: the happy path for each business rule in the
  spec's own order, then one boundary scenario per rule whose text states a
  boundary ("inclusive", "at least", "at most"), then the rejections the spec
  lists. A scenario exists because a sentence in the spec requires it; there
  are no others.
- Cases of one rule are one `Scenario Outline` with an `Examples` table,
  never a scenario per case: eight kinds of unacceptable content are one
  outline with eight rows. A scenario of its own is for a rule of its own.
- Every scenario carries a one-line description between its title and its
  first step: what it pins and why, in plain words, so a reader who has not
  seen the spec knows what the scenario is for. It is not a step and does
  not restate the steps.
- Roles are the ones the spec names. Where the spec gives an operator or an
  administrator a command line, the operator is a role and scenarios from
  their perspective are features like any other.
- Steps: Given is the state of the world in the customer's words. When is one
  action by one named role, in the third person (`the customer applies`, never
  `I apply` or `my cart`). Then is an outcome the customer can observe. A
  rejection reads `Then the code is rejected because <reason from the spec>`,
  never the message text, status code, or field name.
- A case the spec does not mention (re-applying the same code, an empty cart,
  removing what isn't there) is not a scenario. It goes in the report under
  questions for the spec.
- Data tables and step arguments use the customer's words: product, price,
  quantity, code, expiry. Column names from the spec's data model do not
  appear. Amounts are plain decimals with no currency symbol.

Return: (1) each file as a fenced block; (2) a coverage table with one row per
scenario: scenario name, the spec sentence (quoted) that requires it, and one
word, `settled` when that sentence admits one reading and the scenario is it,
`deciding` when the scenario fixes something the sentence leaves open or picks
one of two readings (say which two); (3) spec rules with no scenario, if any;
(4) questions for the spec: cases you noticed that the spec does not mention,
one line each, with no scenario written for them.
```

## The Hand-back Brief

When `slicing-into-increments` logged a `RE-FORMULATE` entry, send this instead, filled in from that entry:

```
The scenario "<SCENARIO>" in <FEATURE PATH> was handed back during
implementation. The plan log at <PLAN PATH> has the RE-FORMULATE entry with
the evidence. You may read that feature file, the plan, anything under
docs/, and anything under features/. Nothing else.

Return the scenario rewritten so that it is consistent with the rest of the
feature and cites the spec sentence (or the other approved scenario) that
decides it. Change only the lines the evidence requires. If nothing in the
spec or the approved scenarios decides it, return no scenario: return the
question the human must answer, in one sentence, with the two readings.
```

The returned scenario carries its one-line description like any other. The main agent writes it over the old one, commits, and sorts it as in step 4: settled when it cites the sentence or approved scenario that decides it, and then slicing resumes without approval; deciding otherwise, and then it waits as in step 5. If a question came back instead, log it under the RE-FORMULATE entry as `QUESTION FOR THE SPEC:` and stop; nothing is written to the feature file.

## Why the agent cannot see the code

Given the code, a writer describes what it does. Given only the spec, a writer describes what the customer needs. The second is the contract; the first is a test of the implementation. The restriction is structural: the agent has read-only tools and a path list, not a request to pretend.

## Common Mistakes

| Seen in baseline | Fix in the brief |
|---|---|
| Feature description paraphrases the spec's background paragraph | Line 2 is the value statement, full stop |
| File named after the database table | Verb-phrase name in the customer's words |
| Background table with the schema's column names | Customer's words for columns; data-model names never appear |
| A second feature file for the HTTP API with status codes | One file per customer capability; transport is not a capability |
| Twice as many scenarios as rules, from "checking boundaries the implementer would otherwise guess" | Each scenario cites its spec sentence; boundary scenarios only where the spec states a boundary |
| `Then the customer is told "That code has expired"` | `Then the code is rejected because it has expired` |
| `£` in amounts "to match the UI section" | Plain decimals |
| `When I apply the code`, `my cart` | Third person with the role named: `the customer applies` |
| "Applying the same code again does not discount twice", cited to the one-code rule | Unmentioned cases go under questions for the spec, never as scenarios |
| "The writer marked it deciding, but 'minimum' normally includes the value itself, so I treated it as settled" | That is the second reading being chosen. A deciding mark is the formulator's; the main agent never lowers it. Show the person the two readings |
| Every feature file held for approval, spec-settled and deciding alike | The person approves decisions, not transcription. A scenario whose cited sentence admits one reading is settled and goes to slicing; only what the spec leaves open waits |
| Eight scenarios, one per unacceptable input, each with the same Then | One Scenario Outline, eight Examples rows |
