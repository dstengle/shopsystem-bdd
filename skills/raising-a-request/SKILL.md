---
name: raising-a-request
description: Use when the person states, in English, behaviour they want of a bounded context with a codified spec (spec/index.md with `language: codified-1`), before running `work request` or `work propose`. Also use when an upstream's offer has come back on a request's issue, when `work outcome` or `model parse` refuses a line, when an integrate round needs lines for an upstream, or when a word the person uses is not in the glossary.
---

# Raising a Request

## Overview

A request is a conversation on one GitHub issue on the upstream's repository, and every step is a comment a `work` command posts. It opens with the asker's need in its own words (`work request`); the upstream offers the capabilities that may serve, with its glossary; then the asker either says one fits (`work fits`) or proposes lines (`work propose`). A request's lines are codified requirements: each parses to one tree in the grammar of the context it goes to, built from that context's glossary, and the upstream refuses to accept one that does not. This skill turns the person's English into lines in the upstream's terms. It writes no spec and decides nothing: a line is a proposal, and the upstream judges it.

Scripts: `<this skill's base directory>/../../scripts/`. The upstream's terms are the glossary its offer quotes (under the request's `## Offer`). Where the upstream's spec is at hand, run every `model` command with `--root <the upstream's repository>`; its glossary is the lexicon, never ours. Nothing reads or writes the upstream's repository.

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
While an item is `shaped`, when the person runs `work ready` on the item, `work` shall set the status of the item to `ready`.
When the person runs `work idea`, `work` shall write an item and commit the item.
```

`shall A, B and C` lists more; `shall not A or B` forbids both; `R1, and R2` joins responses whose subjects differ. A condition's clauses join by `and` or `or`. A preposition (`for`, `on`, `with`) means the one relation the context's `## Relations` table gives for the two kinds it joins (`model lexicon` lists the rows); where two readings typecheck, the line is refused as ambiguous and reworded. Exits are in words (`shall exit successfully`, `shall exit with an error naming …`). Never restate what `spec/universal.md` holds (a refusal changes nothing, `--json` prints one object).

## Process

1. **Find the words.** `python3 <scripts>/model lexicon` lists the context's terms by category: actors (the subject of `shall`), kinds, attributes with their values, relation rows, events, resources, conditions. Use a value only in its own attribute's slot (`an initiative that is `started``). Commands, paths and options are backticked codes; message texts are double-quoted strings.
2. **Write the lines**, one per line in a file, in the person's order: `<scratch>/request-lines.md`.
3. **Check every line** with `python3 <scripts>/model parse --file <scratch>/request-lines.md`. Each line prints its tree, or its refusal with the token, its position, the longest prefix that parsed and the nearest lexicon words.
4. **Reword from the refusal.** Reword at the refused token, starting from the prefix that parsed, with one of the nearest words when it means what the person meant. A line that parses to more than one tree ("ambiguous") is split or made specific. Run step 3 again until every line parses.
5. **A missing word is a glossary entry, never a synonym.** When the person means a thing the lexicon has no word for, do not bend the line onto a nearby word that means something else. Tell the person which word is missing, and write the entry the context would need, in the glossary's form, one sentence (`- **archive** (event): <one sentence>. Forms: archives, archived.`), or the `## Relations` row (`| request | archived in | initiative |`) for a missing relation. In this repository that entry goes into an item as a term bullet (`work line <item> --into <cap> --term "<bullet>"`) or a relation row (`--relation "<row>"` in place of `--term`); for an upstream, ask the person to raise it with its owner, and give the entry in the request's `--source` note. The line that needs the word waits until the term exists, since the upstream cannot accept it until then.
6. **Show the person the lines** beside their English, each with its normal form (the tree written back, which `model parse` prints), and change what they say. The lines are the person's.
7. **Ask first**, in this repository: `python3 <scripts>/work request "<title>" --from <this context's id> --thread <job-thread> --ask "<the need, in the person's words>"` (`--to <upstream>` when there are several). It opens the issue on the upstream's GitHub repository (its `github: <owner>/<name>` under `## Upstreams`) and writes `.shop/requests/q<n>.md`. `python3 <scripts>/work sync` records the upstream's offer when it comes.
8. **Wait on the upstream with a watch.** While a request waits on the other side (`work sync` prints `waiting on the other side`), start `python3 <scripts>/work watch --forward` with the Monitor tool (its timeout at the maximum), in place of Bash `run_in_background`: it takes GitHub's events on each repository the account administers (`gh webhook forward`, the cli/gh-webhook extension, installed if missing), polls GitHub's notifications for the others (an upstream's repository) and says which on stderr, and ends, printing one line for each, when the other side posts a comment a request does not hold or a new ask arrives. When it ends, run `python3 <scripts>/work sync`, then this skill's step for each request it named, then start the Monitor again; start it again too when it times out, and after each `work sync`. Stop once no request waits on the other side. A comment it has printed once is not printed again, and it writes nothing. Say to the person that the session is watching.
9. **Answer the offer.** When an offered requirement serves the need: `python3 <scripts>/work fits q<n> --serves <capability>#r<n>`, which delivers the request and closes the issue. Otherwise write the lines (steps 1-6) in the offer's terms and propose them: `python3 <scripts>/work propose q<n> --line "<line>"` (once a line), answer questions with `python3 <scripts>/work reply q<n> <k> "<answer>"`, and post the turn with `python3 <scripts>/work turn q<n>`. A line the upstream refuses or rewrites comes back with `work sync`; go back to step 4.

## Red Flags

| Seen | Fix |
|---|---|
| A line proposed without `model parse` run on it, the upstream's spec at hand | Step 3 first; the upstream refuses to accept what does not parse |
| The person asked to nudge the session when the upstream answers | Start `work watch --forward` with the Monitor tool (step 8) |
| Lines given at `work request` | The ask is words; lines follow the offer, with `work propose` |
| A synonym chosen because the right word is missing | A missing word is a glossary entry (step 5) |
| A value in another attribute's slot (`an initiative that is `drafted``) | `model lexicon`: each value belongs to one attribute of one kind |
| Our glossary used for an upstream's request | `--root <the upstream>`: its lexicon decides |
| Two lines with the same trigger and condition | One line, `shall A and B` |
| Two behaviours in one line joined by "and then" | `and` joins responses to one trigger; a later step is its own trigger and its own line |
| An exit code, a message's exact words, or a field name in a line | Exits in words; wording and fields are implementation |
