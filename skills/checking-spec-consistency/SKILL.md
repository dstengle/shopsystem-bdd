---
name: checking-spec-consistency
description: Use when the person asks to check the spec's consistency, its terms or its glossary, or whether its requirements leave anything to infer, in a repository with codified spec/ capability files. Also use when the person asks to fix what such a check found (fix mode). Run on demand only; integration rounds and work run do not run it.
---

# Checking Spec Consistency

## Overview

A codified spec agrees with itself by construction in most of what this check once judged by hand. Every requirement parses to one tree in the context's grammar, using lexicon words only (`model parse`, rules `v_p*`); `model logic` translates each requirement into facts and checks them in one clingo solve of `grammar/check.lp` over the pairs of requirements and universal conditions that share vocabulary: two requirements that fire on one trigger and demand opposite things (a clash naming both ids, L1), statements that repeat each other (L2), a status set that follows no transition (L3), a pre-state value no transition reaches (L4) and an untriggered event obligation (L5); scenarios are read off each requirement's facts, so they cannot drift from it; `model check` reports a group with more than one statement or two groups with one trigger and condition (v15l, v15n), a given line that is not example data (v15m), avoided words in prose and term problems (`v_t*`), and `model lexicon --check` the glossary's own: categories and values (v_t4-v_t6), an entry of more than one sentence (v_t7), a relation entry, where a relation is a row (v_t8), a `Means` field (v_t9) and a duplicate relation row (v_t10). What none of these can judge is meaning: whether a term's definition is clear, whether a response is observable by the narrator, whether a group leaves something to infer. A blind `shopsystem-bdd:spec-checker` judges that, one dispatch for each capability and one for the glossary.

The skill runs when the person asks for it, never otherwise. Scripts: `<this skill's base directory>/../../scripts/`. The session reads only `spec/`, `features/`, its drafts path and the dispatches' replies and findings files, never the source or the step definitions.

**Findings mode** is the default: it ends with one findings file and changes nothing else. **Fix mode** runs only when the person asks for it, on the findings of a check.

A capability file that is not codified (no `language: codified-1`) is upgraded first (`migrate upgrade`); this check reads codified files only.

## The Check

Choose the drafts path `.shop/scratch/drafts/<date>-consistency/`; the check is `round-1/`.

1. **Run the mechanical checks** and keep their output in `<drafts path>/round-1/`: `scripts/model check --limit 100000` (`model-check.txt`; its `v_p*`, `v_t*` and `v15*` rows are findings), `scripts/model logic` (`logic.txt`; every L0-L5 is a finding) and `scripts/model lexicon --check` (`lexicon.txt`). An exit 2 that names a missing tool (gf, clingo) means that check did not run: the findings file says so, and the check goes on. Any other exit 2 is a failed run: stop and tell the person.
2. **Give the count.** Before dispatching anything, tell the person: "This check has run the parser and the logic check, and now dispatches <n + 1> spec-checkers: one for each of the <n> capabilities and one for the glossary." Then note `git status --porcelain`.
3. **Dispatch** the spec-checkers, all in one message so they run together: the capability template once for each capability, the glossary template once. Describe each `consistency: check <capability>`, and the glossary's `consistency: check glossary`. Give them no other paths.
4. **Wait for your dispatches.** After dispatching, wait in one shell command for every reply file to exist, looking every few seconds, for up to nine minutes; run it again if it times out with dispatches still working. A dispatch with no reply file after two waits is started again, once; after that, the check stops and names it.
5. **Verify the porcelain.** `git status --porcelain` matches the porcelain noted in step 2, but for entries under the drafts path: a dispatch that wrote outside it goes back with those files removed.
6. **Write the findings file**, `<drafts path>/findings.md`, in this order: `## Mechanical` (each row and finding of step 1, by rule), `## Terms` (unclear terms, by term), `## Unobservable responses`, `## Left to infer`, `## Missing examples`. Number the findings `F1`, `F2` and on, across the file. Each names its ids (`capability/<name>#r<n>`, `capability/<name>#g<n>`, `term/<term>`) and quotes the words. Two dispatches' findings about one thing are one finding.

**Findings mode ends here.** Remove `<drafts path>/round-1/`, so the findings file is the one file the check leaves. Reply to the person with the findings file's path and the count in each group. Nothing outside the drafts path changes and nothing is committed.

## Fix Mode

Fix mode works through a findings file, one finding at a time, each answered before the next is asked. Before it starts the working tree is clean of other work, or fix mode stops and says so. A finding's settlement is written beside it as it is settled: `applied <commit>`, `rejected` or `deferred`.

- **A change to a requirement, a group or a term** goes through integrating-a-proposal, as a proposal of its own (in a repository with `.shop/work/`, a request raised with the `raising-a-request` skill, or a capability-proposal). Ask the person one question: the words, quoted with their ids, what is unclear or left open, and the requirement or entry each answer would give, worded in the requirement language and checked with `model parse`. A changed requirement is retired and replaced under a new id; the features follow by `features generate`, never by hand.
- **A mechanical finding** is settled the same way: the requirement or term it names is reworded, and `model parse`, `model logic` and `model check` run clean on the change before it goes to the gate.
- A finding the person says to leave is `rejected`; one for later is `deferred`, recorded as an observation in `.shop/records/observations.md` (`## observation/<context id>/<date>-consistency-<F<n>>`, then `about:`, `by: the person`, `date:` and the finding in one paragraph with its ids), committed alone.

Fix mode ends when every finding is `applied`, `rejected` or `deferred` and step 1's checks show no row the findings file did not settle. Reply with the commits and the count of findings applied, rejected and deferred.

## The Capability Template

Send this to each dispatch verbatim, with the names and paths filled in.

```
Check the groups of spec/capabilities/<NAME>.md.
You may read that file and spec/index.md. Nothing else: not docs/, not the
source, not the step definitions.

The requirements are codified: they parse, use glossary words only, and
their scenarios are generated from them. Do not judge their form or
wording. Find:
- unobservable response: a requirement whose response the capability's
  narrator cannot observe;
- left to infer: two groups that act on one thing without saying which
  wins, a requirement that leaves to inference which runs, workers or
  commands it applies to, or a status with a way into or out of it that no
  requirement gives;
- missing example: a group whose scenario needs example data (a file's
  contents, a table, a text) its requirement does not carry and that has
  no given block.
Decide nothing and rewrite nothing.

Write your findings to <DRAFTS PATH>/round-<N>/<NAME>.findings.md, and
nowhere else, one per finding: its kind; its ids (capability/<NAME>#r<n> or
#g<n>); the words, quoted; one line saying what is not observable or left
open. Write "none" when you find nothing. Reply with the count of each kind
and the findings file's path, nothing else. Write that same reply, last of
all, to <DRAFTS PATH>/round-<N>/<NAME>.reply.md.
```

## The Glossary Template

```
Check the terms of this bounded context.
You may read spec/index.md and the ## Terms and ## Relations sections of
the files under spec/capabilities/. Nothing else.

Find each unclear term: a sentence that does not say what the word picks
out or says it in words the glossary lacks, a condition's definition that
does not pick out what its word says, or a primitive condition whose
sentence could be a definition in the language.
Decide nothing and rewrite nothing.

Write your findings to <DRAFTS PATH>/round-<N>/glossary.findings.md, one per
finding: the term's id (term/<term>), its entry quoted, and one line saying
what is unclear. Write "none" when you find nothing. Reply with the count and
the findings file's path, nothing else. Write that same reply, last of all,
to <DRAFTS PATH>/round-<N>/glossary.reply.md.
```

## Red Flags

- A spec-checker dispatched before the person was told how many there will be
- The check run because a round finished, not because the person asked
- Findings mode that edited `spec/`, `features/` or the glossary, or committed anything
- A finding without its ids
- A spec-checker asked to judge a requirement's form, its wording or its scenario: the parser and the generator settle those
- A feature file edited to settle a finding
- Two findings asked in one question
