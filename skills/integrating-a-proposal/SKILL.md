---
name: integrating-a-proposal
description: Use when a brainstorming note or design spec has been approved, before any feature file, work-item or code is written for it. Also use when a generated scenario shows a requirement is wrong, when the person rules a work-item's question a question for the spec, or when a spec/ directory of capability files exists and a new design would otherwise start a second spec.
---

# Integrating a Proposal

## Overview

A bounded context has one spec: `spec/index.md` (its glossary is the lexicon), `spec/universal.md`, `spec/decisions/` (one file per decision, with a generated `index.md`), and `spec/capabilities/<name>.md`, whose Behaviour is codified requirement groups; a service capability's `features/<name>.feature` is generated from them by `features generate`. A brainstorming note is a proposal against that spec. This skill merges it in and stops at the one human gate: the requirements and glossary entries, each group shown with the scenario it generates. Generation needs no second approval. It runs before `work run`'s formulate script and before `delivering-an-initiative`.

Format: `docs/capability-format.md` in this plugin, which the `capability-writer` agent has in its context.

## Who Does What

`work run` starts each round as a fresh `shopsystem-bdd:initiative-round`: `integrate`, `gate`, `apply`; then it formulates by script (formulating-features). No session writes spec, dispatches a writer, verifies a change list or keeps the gate; a round made in a session that talks to the person costs every later turn a re-reading of it.

You are `initiative-round`: steps 1, 2 and 4 below are yours, as the kind your input prompt gives says. Step 3 is the `gate` round's: it gives the gate as questions in its result, and `work run` writes them on the capability-proposal. The person's answers come back under its `## Answers`, and the next round is started with them. You end with your ledger line, appended with `work note` (see the agent's "The ledger").

## Process

1. **Dispatch the `capability-writer` agent** (this plugin; it reads only the paths its input prompt lists and writes only drafts) with the template below. On a send-back from `work run` (`Refused drafts:`), a requirement a generated scenario showed wrong, or a work-item's question the person ruled a question for the spec, use the question template instead. Choose the drafts path `.shop/scratch/drafts/<date>-<note name>/`. Each dispatch is a round with its own directory, `<drafts path>/round-<n>/`, named in its input prompt. If `.gitignore` lacks `.shop/scratch/`, add it and commit that line alone. Then note `git status --porcelain`.
2. **Check the drafts in the language, then verify the change list, both directions.** First, run `scripts/model parse --file <file>` on the requirements of each drafted capability (one per line, copied from its Behaviour), `scripts/model parse --grammar Def` on each drafted condition sentence meant as a definition, and `scripts/model logic <capability>` on spec/ with the drafts applied in a scratch copy: every requirement parses to one tree and no L1 or L3 is new. Each drafted group is one statement, its responses joined by `and`, and no two drafted groups of a capability share features, condition and trigger; a `given` block holds example data only; a drafted term is one sentence, with no `Means` field, and a relation is a `## Relations` row, not a term entry (`docs/capability-format.md`). A refusal goes back to the writer with its text (the token, how far it parsed, the nearest words); a missing word goes back as a term to draft, never a synonym. `work run` runs the same check when the round ends, sends what still fails back to the round at most twice, then asks the person. First, verify that `git status --porcelain` matches the porcelain noted before dispatch: only an entry new since then is the agent's, and an agent that wrote outside the drafts path goes back with those files removed. Every behavioural sentence of the note is a requirement, a glossary or Terms entry, a question, or a cut sentence; a sentence that is none goes back to the agent. Every added or changed line quotes the note sentence it comes from, or the answer it comes from where an answer asks for lines the note's accepted lines do not (such a line goes under the capability the answer names); a line with no quote is removed and asked as a question. Then compare each drafted Behaviour section with the committed one: every requirement that differs has its row in the change list, a changed one as a removed id and an added one (retire, never edit). A difference with no row goes back to the agent. Compare a drafted `## Glossary` with the committed one the same way: every entry added, changed or removed has its row, named `term/<term>`, and every entry is in the form `docs/capability-format.md` gives; a drafted `## Relations` table is compared row by row the same way. Every drafted decision is a whole file `spec/decisions/<nnnn>-<slug>.md` under the round's drafts, `nnnn` one above the highest number in `spec/decisions/` and in the earlier rounds' drafts, in the light form (a summary and a Decision section; Context and Alternatives only where options were weighed); its `source` has ids only, and the person, a date, a delegation or anything outside the repository is in its `by`. A decision that fails this goes back to the agent. Every requirement row has an id: a removed row the id the requirement has in `spec/`; the added rows of a capability the next free ids in order, counting earlier rounds' drafts: the first one above every id the capability's lines, its `retired` list and the earlier rounds' drafted lines have used, each next added row one above the last. When the brief lists requirement ids that other initiatives' drafts add (its "Ids drafted elsewhere"), the first added row of a capability also goes above every listed id on that same capability; ids listed on other capabilities, and `term/` ids, do not count, and a brief that lists none changes nothing. A row whose id fails this goes back to the agent, and so does a removed row whose id is not in the drafted `retired` list.
3. **Give the gate.** The `gate` round gives, in its result, one question for each decision the person is asked to make, each marking the recommended reading and giving the requirements it concerns in full: the added and removed requirements, each with its id and its group, the group's generated scenario from the brief's `Generated scenarios (preview):` (a removed line deletes contract, and its id is retired), the added, changed and removed glossary entries, each with its `term/<term>` id, each decision as its file (path, summary, `source`, `by` and Decision), and the questions, each with the lines its answers would give. `work run` writes them on the capability-proposal, and nothing proceeds without an explicit yes on the lines and an answer to each question. Answers go back to the writer with the question template, as the next `integrate` round, and its change list is verified as in step 2 and given again. A line the person rejects is dropped from the drafts, and a rejected removal's id from the drafted `retired` list; a rejected glossary entry is dropped the same way. Nothing is written to `spec/` before the yes, glossary entries included.
4. **Apply the drafts** exactly as approved, round by round in order. A capability file that is not codified (no `language: codified-1`) is upgraded first (`migrate upgrade`). First run `scripts/model check --limit 100000` (this plugin's, at `<this skill's base directory>/../../scripts/`; it takes no path and reads all of `spec/` and `features/`; `--limit` is an option, without which each rule shows ten rows and then `... and <n> more`) and keep its output: what it prints now was there before this round and is not this round's. Then apply: new files copied in, changed sections replaced in place (a later round's section replaces an earlier round's; a `frontmatter` draft replaces the file's frontmatter; a `## Glossary` that `spec/index.md` lacks is added after its last section), each round's decision files copied into `spec/decisions/`, then `scripts/model decisions` run to write `spec/decisions/index.md`; never edit an existing decision file (a changed decision is a new file that supersedes it). Run `model check --limit 100000` again and compare the rows it lists with the kept ones. It exits 1 whenever it prints anything, so judge it by the rows that are new, not by its exit code; warnings (`warning w_...`) are not judged. These new rows are expected, because generation is next:
   - `v_s3` (a group or requirement has no scenario) naming an added group or requirement of a service capability.
   - `v_s1` (a scenario names no requirement) naming a removed requirement's scenario, and an `unresolved:` line for its tag. Regeneration drops that scenario.

   No new `v_p` row (a requirement that does not parse, is ambiguous, or a `given` line the step grammar refuses), no new v15l, v15m, v15n or `v_t` row, and no other new `v_s` row is expected: the drafts were parsed in step 2. Anything else that is new, another violation, unresolved reference or file problem, restores `spec/` (`git checkout -- spec/`, and remove the files the apply added), is fixed in the drafts, and the drafts are applied and compared again; a fix that changes a requirement goes back to the gate, a file or reference fix that changes no requirement does not. If either run exits 2 with a message that names clingo and `pip install clingo`, clingo is missing: say so in the reply and go on. Any other exit 2 is a failed run, to be fixed and rerun. Then commit `spec/` alone, decision files and the regenerated `spec/decisions/index.md` in the same commit (`model decisions --check` exits 0 on it), with the approval in the message (`spec: <note>, lines approved <date>; adds <cap>#r<n>, term/<term>, design-decision/<slug>, ...; changes ...; removes ...`), naming the approval and its date, any delegation it was given under, and each id and each term added, changed and removed: a committed requirement or glossary entry is an approved one.
5. **Hand off.** Once the apply is committed, `work run` generates the features by script (formulating-features) and drafts the work-items.

## Terms

A glossary entry (`docs/capability-format.md`, The glossary is the lexicon) is approved at the gate like a requirement, and the spec commit names each term added, changed and removed. In a repository that keeps `.shop/work/`, a term change rides with the capability-proposal that needs it: the proposal lists `term/<term>` in its `adds`, `changes` or `removes`, beside the lines it argues.

## The Template

```
Integrate the approved note at <NOTE PATH> into this bounded context's spec/.
You may read that note, anything under spec/, anything under features/, and
anything under docs/. Nothing else. spec/ <exists | does not exist yet>.
Write your drafts under <DRAFTS PATH>/round-1/ and nowhere else.

Write the drafts and reply with the parts your definition lists: the change
list, questions, cut sentences, and the drafts' paths. Write that same reply,
last of all, to <DRAFTS PATH>/round-1/writer.reply.md.
```

## The Question Template

```
A question came back against spec/capabilities/<NAME>.md:
<THE QUESTION, WITH ITS READINGS, OR THE PERSON'S ANSWER>
You may read that file, anything under spec/, features/ and docs/, and the
earlier rounds under <DRAFTS PATH>. Nothing else. Write your drafts under
<DRAFTS PATH>/round-<N>/ and nowhere else; a section you change is drafted
whole, with the earlier rounds' drafts of it applied.
Write the drafts and reply with the change list for the lines the answer
decides, and the drafts' paths; if the answer is a decision, draft its decision
file. If nothing decides it yet, reply with the question in one sentence
with the two readings. Write that same reply, last of all, to
<DRAFTS PATH>/round-<N>/writer.reply.md.
```

## Common Mistakes

| Seen in baseline | Fix |
|---|---|
| Writer read `cart/__init__.py` and the tests, and wrote a capability from the code | The `capability-writer` agent: a path list, no edit or shell tools, drafts only; never a general-purpose agent |
| `told "That code has expired"` as the Behaviour response | A refusal names its reason; message wording is Implementation |
| "A refused code leaves the total unchanged" written as a line the note never gives, and mentioned only in the closing summary | Every line quotes its note sentence. An unstated line is a question at the gate, not a line |
| Rounding half up taken from the note's implementation notes into Behaviour "because a customer can see it" | Promoting Implementation to Behaviour is a question with two readings |
| `promo_discount.feature` for `promo-discount.md`, or a `formulated_as` field | Hyphens on both sides: `promo-discount.md` generates `features/promo-discount.feature`; no field names it |
| A line inserted between r2 and r3 numbered r3, the rest renumbered | A new line takes the next free id wherever it sits; ids never change |
| A decision file with no `date:`, a `## Consequences` section, or `source: ["the person, 2026-10-19"]` | `date:` on every decision, the note's date; the light form; `source` has ids, the person and the date go in `by` |
| A decision appended to a `decisions.md`, or the index written by hand | One file `spec/decisions/<nnnn>-<slug>.md`; `scripts/model decisions` writes the index |
| Whole capability files and every existing decision returned on every round (checkout.md and all six decisions in a 7.5 KB reply, for one added line) | Changed sections and new decision files only, to the drafts path; the reply is the change list |
