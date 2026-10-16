---
name: integrating-a-proposal
description: Use when a brainstorming note or design spec has been approved, before any feature file, plan or code is written for it. Also use when formulating-features returns a capability line that admits two readings, when slicing logs a QUESTION FOR THE SPEC, or when a spec/ directory of capability files exists and a new design would otherwise start a second spec.
---

# Integrating a Proposal

## Overview

A bounded context has one spec: `spec/index.md`, `spec/decisions.md`, and `spec/capabilities/<name>.md`, each capability paired by name with `features/<name>.feature`. A brainstorming note is a proposal against that spec. This skill merges it in and stops at the one human gate: the Behaviour lines. Formulation from approved lines needs no second approval. It runs before formulating-features and before superpowers:writing-plans.

Format: `docs/capability-format.md` in this plugin, which the `capability-writer` agent carries.

## Who Does What

The session the person talks to keeps the gate and hands everything else to `shopsystem-bdd:spec-round`, a fresh one for each round. A round done in that session costs every later turn a re-reading of it: in one measured batch the session that integrated and formulated a note read 30M tokens from cache, eleven times what all its writers and formulators read.

**If the person is talking to you:**

1. Choose the drafts path. Dispatch `spec-round` with the job `integrate`, the note's path, the drafts path, round 1 and `Scripts:`. Describe the dispatch `spec <note's name>: integrate round 1`. It carries out steps 1 and 2 below and replies with the gate's text.
2. Step 3, the gate, is yours: show the person that text as it came, and wait. Their answers go to a new `spec-round`, job `integrate`, round 2, in their own words.
3. On their yes, dispatch `spec-round` with the job `apply`, the rounds, and the approval in their words with its date. It carries out step 4.
4. Step 5: invoke formulating-features.

You do not dispatch the `capability-writer`, open a draft, check a change list or apply a draft yourself. If the gate's text is not enough to show the person, ask the round for what is missing; do not go and read it.

When this session is the one that brainstormed the note, say so before step 1: a new session that is given the note's path integrates it without re-reading the brainstorm at every turn. Carry on here if the person prefers.

**If you are `spec-round`:** steps 1, 2 and 4 below are yours, as your dispatch's job says. Step 3 is never yours.

The small-change path below has no round: the session writes its two lines itself.

## Process

1. **Dispatch the `capability-writer` agent** (this plugin; it reads only the brief's paths and writes only drafts) with the brief below. On a question from formulating-features or slicing, use the question brief instead. Choose the drafts path `.superpowers/spec-drafts/<date>-<note name>/`. Each dispatch is a round with its own directory, `<drafts path>/round-<n>/`, named in its brief. If `.gitignore` lacks `.superpowers/`, add it and commit that line alone. Then note `git status --porcelain`.
2. **Check the change list, both directions.** First, check `git status --porcelain` matches the porcelain noted before dispatch: only an entry new since then is the agent's, and an agent that wrote outside the drafts path goes back with those files removed. Every behavioural sentence of the note is a line, a question, or a cut sentence; a sentence that is none goes back to the agent. Every added or changed line quotes the note sentence it comes from; a line with no quote is removed and asked as a question. Then compare each drafted Behaviour section with the committed one: every line that differs has its row in the change list. A difference with no row goes back to the agent. Every row has an id: a changed or removed row the id the line has in `spec/`, an added row an id no line and no `retired` entry of that capability has. A row whose id fails this goes back to the agent, and so does a removed row whose id is not in the drafted `retired` list.
3. **Stop at the gate.** Show the person the added, changed and removed Behaviour lines, each with its id (a removed line deletes contract, and its id is retired), and the questions, each with the lines its answers would give. Wait for an explicit yes on the lines and an answer to each question. Answers go back to the agent with the question brief, as the next round, and its result is checked as in step 2 and shown again. A line the person rejects is dropped from the drafts. Nothing is written to `spec/` before the yes.
4. **Apply the drafts** exactly as approved, round by round in order: new files copied in, changed sections replaced in place (a later round's section replaces an earlier round's; a `frontmatter` draft replaces the file's frontmatter), each round's `decisions.append.md` appended to `spec/decisions.md`; never edit an existing entry. Then run `scripts/model check` (this plugin's, at `<this skill's base directory>/../../scripts/`) with no arguments (it reads all of spec/) once the drafts are applied: for the capabilities the drafts changed it reports `v_s3` for the added and changed lines, which formulation is next to cover, and nothing else. Anything else in those capabilities, or an unresolved reference or file problem the drafts introduced, restores `spec/` (`git checkout -- spec/`, and remove the files the apply added), is fixed in the drafts, and the drafts are applied again; a fix that changes a Behaviour line goes back to the gate, a file or reference fix that changes no line does not. A repository whose Behaviour lines carry no `[r<n>]` ids is migrated to ids first (migrating-to-capabilities, "Adding Ids"), before this check is used. If it exits 2 with a message that names clingo and the install command, clingo is missing: say so in the reply and go on. Any other exit 2 is a failed run, to be fixed and rerun. Then commit `spec/` alone, with the approval in the message (`spec: <note>, lines approved <date>; adds <cap>#r<n>, ...; changes ...; removes ...`): a committed Behaviour line is an approved one.
5. **Hand off.** Invoke formulating-features with the changed capability paths and the change list.

## The Small-Change Path

A change is small when it adds or changes at most two Behaviour lines, all in capabilities that already exist, changes no published contract (no rpc, message, command, rule name or file form a client depends on), and leaves nothing unknown about what the lines mean. A review finding that becomes a line, a refusal the code already makes but no line states, a case added to a line already there: these are small.

A small change skips the note and the `capability-writer`:

1. **Write the lines yourself**, in the capability's narrator voice and `docs/capability-format.md`'s form, with ids as `docs/capability-format.md` says, with a ledger entry when the change is a decision. Read only `spec/` while you write them, never the code.
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
list, questions, cut sentences, and the drafts' paths. Write that same reply,
last of all, to <DRAFTS PATH>/round-1/writer.reply.md.
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
with the two readings. Write that same reply, last of all, to
<DRAFTS PATH>/round-<N>/writer.reply.md.
```

## Common Mistakes

| Seen in baseline | Fix |
|---|---|
| Writer read `cart/__init__.py` and the tests, and wrote a capability from the code | The `capability-writer` agent: a path list, no edit or shell tools, drafts only; never a general-purpose agent |
| `told "That code has expired"` as the Behaviour response | A refusal names its reason; message wording is Implementation |
| "A refused code leaves the total unchanged" written as a line the note never states, and mentioned only in the closing summary | Every line quotes its note sentence. An unstated line is a question at the gate, not a line |
| Rounding half up moved from the note's implementation notes into Behaviour "because a customer can see it" | Promoting Implementation to Behaviour is a question with two readings |
| `formulated_as: features/promo_discount.feature` | Hyphens on both sides: `promo-discount.md` ↔ `promo-discount.feature` |
| A line inserted between r2 and r3 numbered r3, the rest renumbered | A new line takes the next free id wherever it sits; ids never move |
| Ledger entries with no date | `date:` on every entry, the note's date |
| Whole capability files and the whole ledger returned on every round (checkout.md and all six ledger entries in a 7.5 KB reply, for one added line) | Changed sections and new entries only, to the drafts path; the reply is the change list |
