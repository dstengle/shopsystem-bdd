---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-08-cnl-research-phase-3
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-08
---

# CNL research phase 3: every line and term sorted

## What was done

Phase 3 of b112's research (`.shop/backlog/b112.md`), after phase 1 (`2026-11-08-cnl-research-phase-1.md`) and
phase 2 (`2026-11-08-cnl-research-phase-2.md`). Phase 2 rewrote 27 sample lines in the owner's direction and fixed a
list of named constructs (`2026-11-08-cnl-research-phase-2/sample-rewrites.md` §1.3). Phase 3 applied the same
analysis, lighter per line, to **every** line: four researchers took the 265 requirement lines (260 in 16
capabilities, 5 universal statements) in four shares, and a fifth took the vocabulary (all 170 adjective entries, and
a lighter pass over nouns, verbs, attributes, resources and relation rows). Each line got a pattern, a verification
route, the constructs its rewrite needs, the adjective it removes, whether it carries example data, and a candidate
rewrite. Beside this record, in `2026-11-08-cnl-research-phase-3/`: `a.tsv`/`a.md` (design-model-check,
decision-tiers, pr-review, brainstorming), `b.*` (requests, intake, conversation, readiness), `c.*` (analysis-tools,
feature-file-tools, trials, universal), `d.*` (migration-tools, backlog, batches, batch-measurement, telemetry),
`terms.*` (the vocabulary). The candidates are research material, not proposed lines: no line is changed.

## The lines, counted

| Pattern | Lines | | Route | Lines |
|---|---|---|---|---|
| effect (trigger, response at the next step) | 167 | | scenario | 246 |
| refusal (If ... exit with an error, change nothing) | 83 | | judgement (design-decision) | 15 |
| invariant | 7 | | check after each scenario | 3 |
| transition (every event of a kind) | 6 | | static check | 1 |
| bounded (within a time) | 1 | | runtime monitor | 0 |
| liveness | 1 | | | |

**This repository's spec is almost entirely next-step effect rules about commands.** Time, modality and runtime
monitoring, which phases 1 and 2 found to be the big theoretical gaps, matter to 16 of 265 lines here. They will
matter more to a consumer that specifies a running service (feed); this repository specifies a command-line tool.
The design must not size the time and modality work from this repository's lines alone.

| Construct (phase 2's names) | Lines | What it is |
|---|---|---|
| OF | 77 | "the X of Y" in any slot ("the release of a repository is `own`") |
| EXAMPLE-DATA-OUT | 66 | example data moved from the line into the group's given block (a writing rule) |
| SENSE | 56 | a second frame of a word already in the glossary ("a measurement names" beside "an agent names") |
| NEG-EXIST | 53 | "no X" as a subject or after has/with ("has no frame") |
| HAS | 49 | has / holds as a relation verb |
| STATE-MOVE | 45 | a state moved out of the trigger's noun phrase into While (a writing rule) |
| WITH-ARG | 36 | a command's argument as a noun phrase ("runs `work request` with no origin option") |
| RC-OBJ | 35 | object relative clause ("a comment that a session posts") |
| RC-SUBJ | 32 | subject relative clause from any verb ("a measurement that names the target") |
| WHOSE-REL | 30 | "whose" over a relation noun ("a branch whose upstream branch ...") |
| COMPARE | 24 | order or difference between values ("after `1.0.0`", "another name") |
| ADJUNCT-PP | 24 | a frame's extra prepositional role ("remove X from Y") |
| POSS | 17 | its |
| NP-LIST | 16 | a list of objects inside a clause |
| CONFORMS | 16 | conformance to a named artifact (schema, format) |
| VP-COORD-NEG | 14 | one subject, a positive and a negated verb phrase |
| EXISTS | 14 | "X exists" |
| THIS | 12 | "this bounded context": the context the command runs in |
| COUNT, COUNT-CMP | 13 | exactly n; more than / at least n |
| ONLY, REL-COPULA, OR-NP, HISTORY, AGGREGATE, NEVER/ALWAYS, TRIGGER-AS-ACTION, VALUE-SET | 1-4 each | |

- **137 lines lose a coined adjective; 33 stay as they are; 42 need no new construct**, only the two writing rules or
  a reword. 68 lines carry example data; in feature-file-tools 19 of 20, and in about half of those the rule is stated
  only by the example.
- The noun phrase is where the work is: OF, NEG-EXIST, HAS, the two relative clauses and WHOSE-REL together cover
  most rewrites. This confirms phase 1's main finding with counts.
- **SENSE is a tension with plugin 3.0.** 56 lines want a verb in a second meaning (a document that names, lists or
  uses something, where the frame says an agent does). b84's answer settled one `Frame:` per verb, "no several-Frame
  lines". Many SENSE cases are a word used in two meanings, which the owner's direction and the "one word, one
  meaning" practice (phase 1) both reject: the alternative to a second frame is a second verb (record beside keep,
  cite beside name). An open question for the design.

## The vocabulary, counted

Of 170 adjective entries (25 defined in the controlled language, 145 prose):

| Verdict | Entries | Line uses |
|---|---|---|
| structure: replaced by a sentence structure in the line | 74 | 104 |
| dead: used by no line | 66 | 0 |
| artifact: a format test, conformance to a named schema | 17 | 19 |
| keep: a domain notion that deserves a term | 7 | 20 |
| value: a status or attribute value | 5 | 7 |
| merge: another term covers it | 1 | 1 |

Kept: settled, closed (of request), blocked, downstream, received, sent, prepositional. All but one dead entry belong
to plugin 1.x kinds or retired capabilities. 94 of 166 kinds, 18 of 43 verbs and all 9 resources are unused. About 15
words carry several meanings (`open` four, `closed` four plus the verb, `present` three, `malformed` four forms,
`passing`, `uncommitted`, `uncited`, `untested`, `unparsed` two each); about 30 live entries give a common English
word a narrow domain meaning, some against a technical meaning (sound, clean, tracking, ahead). Some verbs' glosses
disagree with their frames (merge, name, list), and include, note and log have frames bent to fit a line. Some
relation rows use verb words (adds, changes, removes) or nouns (asker, upstream).

## What the candidate form still cannot say

Each with the lines that need it (details in the share reports):

1. **An ordered choice or default**: "the first of these that exists", "300 when none is given" (analysis r2-r6, r33).
2. **Distribution**: "for each X, its Y" (analysis r18; feature-file-tools r2).
3. **Transitive closure**: "however deep" (feature-file-tools r4).
4. **Counterfactual or plan-based states**: "what `features generate` would write", "would relocate" (feature-file-tools
   r18; migration-tools r7).
5. **Output layout**: headings, one line per item; belongs in a named format artifact (CONFORMS), as the owner proposed
   for schemas.
6. **Ordered values**: a release as a version, not an enum (migration-tools r10, r17, r25).
7. **Aggregates**: the next id, the highest (backlog, batch-measurement).
8. **Binding an argument to a value**: "set the value to the one given" (backlog r4); sameness and distinctness of two
   referents (batch-measurement r22; design-model-check r6).
9. **Attributes on relations**: "supersedes in part" (migration-tools r4).
10. **Time bounds**: "no answer within the push timeout" (backlog r19).
11. **Ability, history, the indexical**: "cannot import", "has written", "this bounded context".
12. **Meta-level lines**: design-model-check is one refusal template repeated 47 times about the spec's own parts
    (requirements, terms, frames, ids). Written out, its lines run 25-40 words of meta-vocabulary. The alternative is
    to treat the rule catalogue (`model.lp`'s labels) as a named artifact a line says a thing violates (CONFORMS turned
    round). The same holds for the nine grammar-finding adjectives (objectless, recipientless, mistyped ...): better
    named findings (codes) a line cites than adjectives of "requirement". **A choice for the owner.**

## The spec's own faults, found on the way

Writing the lines out exposed faults the adjectives hid. A selection (full lists in the share reports):

- **Wrong meaning:** requests r16 says "downstream" where it means a sent request (r51's sense).
- **Wrong agents:** pr-review r5, r7, r9 and brainstorming r3 (the agent that acts is `work` or the batch session);
  telemetry r1 (`measure` as the subject of include); conversation r2 (keep used for store).
- **Clashes hidden by the If precedence:** requests r18 and r49; feature-file-tools r15 and r16; backlog r20 and r21
  (b117).
- **Entailed or empty lines:** requests r8 (adds nothing to r6); decision-tiers r8 (r9 with `--tier`); analysis r6's
  positive half (r2); Thens repeated from a verb's gloss (batches r2, r6: park, pick).
- **States only in the group title, or lines thinner than their group:** design-model-check r44, r52; analysis r17,
  r20, r33; feature-file-tools f1, f17, f19; batches r1, r18; migration-tools r13, r20.
- **Two rules in one line:** design-model-check r36, pr-review r3; migration-tools r13, r16, r24 (several upgrade steps).
- **Inconsistent refusals:** six refusals in requests leave out "change nothing"; r45-r47 have no error clause.
- **"exit with an error" in two senses:** refused (U11) versus found something (analysis r28, r32; feature-file-tools
  r13, r15, r18, r19).
- **"the" with no antecedent:** "naming the term" with no term in the line (7 design-model-check lines);
  migration-tools r13-r16, r24, r25 ("the repository").
- **Retired words in live lines:** U5, U7 still speak of `work run`'s worker; design-model-check r11, r19 name 1.x
  things.

These go to the backlog as one idea (fix the line faults phase 3 found, citing this record), apart from b112's
redesign: they are wrong today, whatever grammar comes.

## What this means for the design

1. **The order of work is clear from the counts:** the noun phrase first (OF, NEG-EXIST, HAS, RC-SUBJ, RC-OBJ,
   WHOSE-REL, POSS: present in most rewrites), then WITH-ARG and THIS (the command and the context as things a line
   can name), then CONFORMS with named artifacts, then COMPARE and ordered values, then counts. Time, modality and
   monitors next, sized from a consumer such as feed, not from this repository.
2. **Two writing rules are free and large:** example data out of the line (66 lines) and states out of the trigger
   into While (45). They need no grammar, only the authoring skills and a check.
3. **The vocabulary shrinks by about half before any grammar work:** 66 dead adjectives, 94 unused kinds, 18 unused
   verbs, 9 unused resources; most of the rest of the adjectives become structure.
4. **Reading rules must be written per construct and tested against real lines.** requests r53 needs today's reading
   of a negated indefinite (some comment not held); ACE's reading ("holds no comment") would break it. requests r37
   guards against a vacuous `every`. The rules phase 1 recommends cannot be copied from ACE wholesale.
5. **Open choices for the owner:** a second frame per verb versus a second verb (SENSE); the meta-level lines as
   written-out rules versus a named rule catalogue; Where for a command option versus WITH-ARG in the trigger (EARS's
   Where is for a product feature); named composite states (requests r36, r39) as defined conditions whose definitions
   parse.
