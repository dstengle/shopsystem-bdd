---
name: integrating-a-proposal
description: Use when a brainstorming note or design spec has been approved, before any feature file, plan or code is written for it. Also use when formulating-features returns a capability line that admits two readings, when slicing logs a QUESTION FOR THE SPEC, or when a spec/ directory of capability files exists and a new design would otherwise start a second spec.
---

# Integrating a Proposal

## Overview

A bounded context has one spec: `spec/index.md`, `spec/decisions.md`, and `spec/capabilities/<name>.md`, each capability paired by name with `features/<name>.feature`. A brainstorming note is a proposal against that spec. This skill merges it in and stops at the one human gate: the Behaviour lines. Formulation from approved lines needs no second approval. It runs before formulating-features and before superpowers:writing-plans.

Format: `docs/capability-format.md` in this plugin, which the `capability-writer` agent carries.

## Process

1. **Dispatch the `capability-writer` agent** (this plugin, read-only tools) with the brief below. On a question from formulating-features or slicing, use the question brief instead.
2. **Check the change list, both directions.** Every behavioural sentence of the note is a line, a question, or a cut sentence; a sentence that is none goes back to the agent. Every added or changed line quotes the note sentence it comes from; a line with no quote is removed and asked as a question.
3. **Write the files** exactly as returned. Append the ledger entries; never edit an existing entry. Commit `spec/` alone.
4. **Stop at the gate.** Show the person the added, changed and removed Behaviour lines (a removed line deletes contract) and the questions, each with the lines its answers would give. Wait for an explicit yes on the lines and an answer to each question. Answers go back to the agent with the question brief; its result is written, committed and shown again. Nothing is formulated while a line awaits approval.
5. **Hand off.** Invoke formulating-features with the changed capability paths and the change list.

## The Brief

```
Integrate the approved note at <NOTE PATH> into this bounded context's spec/.
You may read that note, anything under spec/, anything under features/, and
anything under docs/. Nothing else. spec/ <exists | does not exist yet>.

Return the five parts your definition lists: changed files, the change list,
ledger entries, questions, cut sentences.
```

## The Question Brief

```
A question came back against spec/capabilities/<NAME>.md:
<THE QUESTION, WITH ITS READINGS, OR THE PERSON'S ANSWER>
You may read that file, anything under spec/, features/ and docs/. Nothing
else. Return the changed files and the change list for the lines the answer
decides; if the answer is a decision, its ledger entry. If nothing decides
it yet, return the question in one sentence with the two readings.
```

## Common Mistakes

| Seen in baseline | Fix |
|---|---|
| Writer read `cart/__init__.py` and the tests, and wrote a capability from the code | The `capability-writer` agent: read-only tools and a path list, never a general-purpose agent |
| `told "That code has expired"` as the Behaviour response | A refusal names its reason; message wording is Implementation |
| "A refused code leaves the total unchanged" written as a line the note never states, and mentioned only in the closing summary | Every line quotes its note sentence. An unstated line is a question at the gate, not a line |
| Rounding half up moved from the note's implementation notes into Behaviour "because a customer can see it" | Promoting Implementation to Behaviour is a question with two readings |
| `formulated_as: features/promo_discount.feature` | Hyphens on both sides: `promo-discount.md` ↔ `promo-discount.feature` |
| Ledger entries with no date | `date:` on every entry, the note's date |
