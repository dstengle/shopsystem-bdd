---
name: raising-a-request
description: Use when the person states, in English, behaviour they want of a bounded context with a codified spec (spec/index.md with `language: codified-1`), before running `work request`. Also use when `work request` or `model parse` refuses a line, when an integrate round needs lines for an upstream, or when a word the person uses is not in the glossary.
---

# Raising a Request

## Overview

A request's lines are codified requirements: each parses to one tree in the grammar of the context it goes to, built from that context's glossary. `work request` refuses a line that does not, naming the line, the token and how far it parsed. This skill turns the person's English into lines that parse, before `work request` is run. It writes no spec and decides nothing: a line is a proposal, and the context's intake judges it.

Scripts: `<this skill's base directory>/../../scripts/`. For a request into an upstream, run every `model` command with `--root <the upstream's repository>`; its glossary is the lexicon, never ours.

## The forms

One sentence, the clauses in this order (`docs/capability-format.md`, Writing requirements):

| the person says | form | shape |
|---|---|---|
| it is always so | ubiquitous | `Actor shall V.` |
| when someone runs or something happens | event-driven | `When T, Actor shall V.` |
| while something holds | state-driven | `While C, Actor shall V.` |
| where an option or configuration is given | optional feature | `Where F, Actor shall V.` |
| it refuses, or fails safely | unwanted behaviour | `If T, then Actor shall V.` |
| several of these | complex | `[Where F,] [While C,] When/If T, Actor shall V.` |

The form follows what starts the behaviour, not the person's wording. What happens under one trigger and condition is one line, its verb phrases joined by `and`:

```
While a result is outputless, when a session ends a `plan` stage for a work-item with the result, `work run` shall set the status of the work-item to `awaiting-answer` and ask a question on the work-item.
When the person runs `work start` on an initiative that is `proposed`, `work` shall set the status of the initiative to `started` and print the initiative.
```

`shall A, B and C` lists more; `shall not A or B` forbids both; `R1, and R2` joins responses whose subjects differ. A condition's clauses join by `and` or `or`. A preposition (`for`, `on`, `with`) means the one relation the context's `## Relations` table gives for the two kinds it joins (`model lexicon` lists the rows); where two readings typecheck, the line is refused as ambiguous and reworded. Exits are in words (`shall exit successfully`, `shall exit with an error naming …`). Never restate what `spec/universal.md` holds (a refusal changes nothing, `--json` prints one object).

## Process

1. **Find the words.** `python3 <scripts>/model lexicon` lists the context's terms by category: actors (the subject of `shall`), kinds, attributes with their values, relation rows, events, resources, conditions. Use a value only in its own attribute's slot (`an initiative that is `started``). Commands, paths and options are backticked codes; message texts are double-quoted strings.
2. **Write the lines**, one per line in a file, in the person's order: `<scratch>/request-lines.md`.
3. **Check every line** with `python3 <scripts>/model parse --file <scratch>/request-lines.md`. Each line prints its tree, or its refusal with the token, its position, the longest prefix that parsed and the nearest lexicon words.
4. **Reword from the refusal.** Reword at the refused token, starting from the prefix that parsed, with one of the nearest words when it means what the person meant. A line that parses to more than one tree ("ambiguous") is split or made specific. Run step 3 again until every line parses.
5. **A missing word is a glossary entry, never a synonym.** When the person means a thing the lexicon has no word for, do not bend the line onto a nearby word that means something else. Tell the person which word is missing, and write the entry the context would need, in the glossary's form, one sentence (`- **archive** (event): <one sentence>. Forms: archives, archived.`), or the `## Relations` row (`| request | archived in | initiative |`) for a missing relation. In this repository that entry goes through integrating-a-proposal as a glossary-proposal; for an upstream, ask the person to raise it with its owner, and give the entry in the request's `--source` note. The line that needs the word waits until the term exists, since `work request` refuses it until then.
6. **Show the person the lines** beside their English, each with its normal form (the tree written back, which `model parse` prints), and change what they say. The lines are the person's.
7. **Raise it**, in the repository of the context the request goes to: `python3 <scripts>/work request "<title>" --from <the asking context's id> --lines <scratch>/request-lines.md`. It parses every line again in that context's grammar and writes `.shop/work/requests/q<n>.md`; on a refusal it writes nothing, and the refusal's hint goes back to step 4.

## Red Flags

| Seen | Fix |
|---|---|
| A line raised without `model parse` run on it | Step 3 first; `work request` refuses what does not parse anyway |
| A synonym chosen because the right word is missing | A missing word is a glossary entry (step 5) |
| A value in another attribute's slot (`an initiative that is `drafted``) | `model lexicon`: each value belongs to one attribute of one kind |
| Our glossary used for an upstream's request | `--root <the upstream>`: its lexicon decides |
| Two lines with the same trigger and condition | One line, `shall A and B` |
| Two behaviours in one line joined by "and then" | `and` joins responses to one trigger; a later step is its own trigger and its own line |
| An exit code, a message's exact words, or a field name in a line | Exits in words; wording and fields are implementation |
