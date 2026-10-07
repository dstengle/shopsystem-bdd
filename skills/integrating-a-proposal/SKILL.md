---
name: integrating-a-proposal
description: Use when a brainstorming note or design spec has been approved, before any feature file, plan or code is written for it. Also use when formulating-features returns a capability line that admits two readings, when slicing logs a QUESTION FOR THE SPEC, or when a spec/ directory of capability files exists and a new design would otherwise start a second spec.
---

# Integrating a Proposal

## Overview

A bounded context has one spec: `spec/index.md`, `spec/decisions.md`, and `spec/capabilities/<name>.md`, each capability paired by name with `features/<name>.feature`. A brainstorming note is a proposal against that spec. This skill merges it in and stops at the one human gate: the Behaviour lines. Formulation from approved lines needs no second approval. It runs before formulating-features and before superpowers:writing-plans.

Format: `docs/capability-format.md` in this plugin, which the `capability-writer` agent carries.

## Process

1. **Dispatch the `capability-writer` agent** (this plugin; it reads only the brief's paths and writes only drafts) with the brief below. On a question from formulating-features or slicing, use the question brief instead. Choose the drafts path `.superpowers/spec-drafts/<date>-<note name>/`. Each dispatch is a round with its own directory, `<drafts path>/round-<n>/`, named in its brief. If `.gitignore` lacks `.superpowers/`, add it and commit that line alone. Then note `git status --porcelain`.
2. **Check the change list, both directions.** First, check `git status --porcelain` matches the porcelain noted before dispatch: only an entry new since then is the agent's, and an agent that wrote outside the drafts path goes back with those files removed. Every behavioural sentence of the note is a line, a question, or a cut sentence; a sentence that is none goes back to the agent. Every added or changed line quotes the note sentence it comes from; a line with no quote is removed and asked as a question. Then compare each drafted Behaviour section with the committed one: every line that differs has its row in the change list. A difference with no row goes back to the agent.
3. **Stop at the gate.** Show the person the added, changed and removed Behaviour lines (a removed line deletes contract) and the questions, each with the lines its answers would give. Wait for an explicit yes on the lines and an answer to each question. Answers go back to the agent with the question brief, as the next round, and its result is checked as in step 2 and shown again. A line the person rejects is dropped from the drafts. Nothing is written to `spec/` before the yes.
4. **Apply the drafts** exactly as approved, round by round in order: new files copied in, changed sections replaced in place (a later round's section replaces an earlier round's), each round's `decisions.append.md` appended to `spec/decisions.md`; never edit an existing entry. Commit `spec/` alone, with the approval in the message (`spec: <note>, lines approved <date>`): a committed Behaviour line is an approved one.
5. **Hand off.** Invoke formulating-features with the changed capability paths and the change list.

## The Small-Change Path

A change is small when it adds or changes at most two Behaviour lines, all in capabilities that already exist, changes no published contract (no rpc, message, command, rule name or file form a client depends on), and leaves nothing unknown about what the lines mean. A review finding that becomes a line, a refusal the code already makes but no line states, a case added to a line already there: these are small.

A small change skips the note and the `capability-writer`:

1. **Write the lines yourself**, in the capability's narrator voice and `docs/capability-format.md`'s form, with a ledger entry when the change is a decision. Read only `spec/` while you write them, never the code.
2. **Stop at the gate exactly as above**: show the person the added and changed lines; nothing is written to `spec/` before the yes. Where the person has delegated decisions to your recommendations, record it in the commit (`lines approved <date> under the person's delegation`) and in the ledger entry's `source`.
3. **Hand off** to formulating-features' small-change path.

Anything larger, a new capability, any change to the published contract, or a line you cannot write without choosing between two readings, takes the full process above.

## The Brief

```
Integrate the approved note at <NOTE PATH> into this bounded context's spec/.
You may read that note, anything under spec/, anything under features/, and
anything under docs/. Nothing else. spec/ <exists | does not exist yet>.
Write your drafts under <DRAFTS PATH>/round-1/ and nowhere else.

Write the drafts and reply with the parts your definition lists: the change
list, questions, cut sentences, and the drafts' paths.
```

## The Question Brief

```
A question came back against spec/capabilities/<NAME>.md:
<THE QUESTION, WITH ITS READINGS, OR THE PERSON'S ANSWER>
You may read that file, anything under spec/, features/ and docs/, and the
earlier rounds under <DRAFTS PATH>. Nothing else. Write your drafts under
<DRAFTS PATH>/round-<N>/ and nowhere else; a section you change is drafted
whole, with the earlier rounds' drafts of it applied.
Write the drafts and reply with the change list for the lines the answer
decides, and the drafts' paths; if the answer is a decision, draft its ledger
entry. If nothing decides it yet, reply with the question in one sentence
with the two readings.
```

## Common Mistakes

| Seen in baseline | Fix |
|---|---|
| Writer read `cart/__init__.py` and the tests, and wrote a capability from the code | The `capability-writer` agent: a path list, no edit or shell tools, drafts only; never a general-purpose agent |
| `told "That code has expired"` as the Behaviour response | A refusal names its reason; message wording is Implementation |
| "A refused code leaves the total unchanged" written as a line the note never states, and mentioned only in the closing summary | Every line quotes its note sentence. An unstated line is a question at the gate, not a line |
| Rounding half up moved from the note's implementation notes into Behaviour "because a customer can see it" | Promoting Implementation to Behaviour is a question with two readings |
| `formulated_as: features/promo_discount.feature` | Hyphens on both sides: `promo-discount.md` ↔ `promo-discount.feature` |
| Ledger entries with no date | `date:` on every entry, the note's date |
| Whole capability files and the whole ledger returned on every round (checkout.md and all six ledger entries in a 7.5 KB reply, for one added line) | Changed sections and new entries only, to the drafts path; the reply is the change list |
