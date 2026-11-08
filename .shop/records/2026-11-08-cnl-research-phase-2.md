---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-08-cnl-research-phase-2
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-08
---

# CNL research phase 2: a sample rewritten, read and parsed

## What was done

Phase 2 of b112's research (`.shop/backlog/b112.md`), after phase 1 (`2026-11-08-cnl-research-phase-1.md`). A sample
of 27 lines was taken across the EARS forms and 13 capabilities, with every adjective they use and its definition:
requests r33, r38, r6, r24; batches r8, r13, r17, r16; backlog r20, r21; migration-tools r19, r14, r25, r8, r21;
feature-file-tools r3, r14; trials r1, r2, r4; design-model-check r60, r69; conversation r2; telemetry r1; universal
U4, U7, U11. Three pieces of work, kept beside this record in `2026-11-08-cnl-research-phase-2/`:

| Report | What |
|---|---|
| `sample-rewrites.md` | each line written in ACE, SBVR Structured English, FRETish and a candidate form in the owner's direction; a fixed list of named constructs (§1.3); counts, verbosity, the three languages compared |
| `sample-semantics.md` | each line's facts today (dumped from `spec_context.load`), a DRS / first-order reading and an event-calculus reading; verdict, pattern, verification route, the generated scenario's quality, entailment; the minimal logical form that covers all 27 |
| `prototype-grammar.md` | a throwaway GF grammar over the Resource Grammar Library (RGL) that parses the 27 candidates, with measurements, the hard cases, logical forms from three trees, and what a real implementation needs; its grammar files and inputs in `prototype/` |

The ACE, SBVR and FRETish versions were written by hand from those languages' rules, not run through their tools
(APE's web service was down).

## The candidate form

The owner's direction, as phase 2 wrote it: EARS clause order kept; no coined adjectives; a state in While, the
behaviour in When (If for a refusal); the agent explicit; relative clauses from verb frames and relations; "of";
conformance to a named artifact; a small modal set. Two lines as examples:

- requests r33, today: "While a comment is unreadable, when a session runs `work sync`, `work` shall print the comment,
  and `work` shall not write the comment." Candidate: "While a request comment does not conform to the comment schema,
  when a session runs `work sync`, `work` shall print the comment and not write the comment."
- batches r13, today: "While a commit of an item in a batch is uncited, if the person runs `work batch review` on the
  batch, then ..." Candidate: "While a commit of an item in a batch cites no item, if the person runs ..." (this one
  parses today: `uncited` never saved anything).

Results on the 27:

- **All 15 coined adjectives go.** What survives is status and attribute values (`accepted`, `building`, `own`) and
  `open`, whose definition already parses.
- **In this sample the problem is the noun phrase, not time or modality.** Most needed: "of" in any slot (11 lines),
  example data moved out (6), "no X" in more positions (5), a verb's extra prepositional role and a second meaning of
  a word (4 each). None of the 27 needs "may", "always/never", "only after" or timing.
- **Verbosity:** candidates average 26.3 words against 21.9 today (+20%). Counting the definition a reader must look
  up, the 15 lines with an adjective go from 555 to 456 words (-18%).
- **5 of 27 candidates parse with today's grammar** (4 of them unchanged lines).

The three languages on these lines (`sample-rewrites.md` §4): **ACE** handles noun phrases best and exposed real faults
(the scope of "no commit ... an untracked file" in migration-tools r8; "the reason" and "the commit" with nothing to
refer to), but loses the difference between While, When and If. **SBVR** has the best modality but puts the response
first. **FRETish** matches While/When as scope and condition but turns every noun phrase into a boolean variable: it
has the coined-adjective problem by design.

## What the lines mean

Of the 27 lines, compared with a first-order reading (`sample-semantics.md` §3):

| Verdict | Lines |
|---|---|
| same | 5 |
| loses detail | 16 |
| different meaning | 6: requests r6, migration-tools r21, trials r2, conversation r2, U4, U7 |

Patterns: 22 next-step effect rules, 2 bounded responses (batches r16, U4: "before the command exits"), 1 precedence
(trials r4), 2 invariants (trials r2, U7); no true liveness. Routes: 21 scenario (11 well tested, 4 fair, 6 weak:
batches r8's scenario drops "every task is done"), 3 check after each scenario (U11, U4, trials r4), 2 runtime monitor,
1 judgement.

The five main faults:

1. **"only" is lost or reversed.** trials r2's verb and actor vanish; U7's facts oblige a worker to change *every* file
   in its worktree. (b116.)
2. **A line with no trigger reads as "does it in every state"**, and `every` on an object is ignored by the check.
   (b114.)
3. **"the" with no antecedent means the only one in the world** (7 lines), often because the antecedent sits inside an
   adjective's prose definition.
4. **The state's subject is not tied to the run**: in r6 the originless command is not the command run; in r33 the
   comment is not one `work sync` reads. The run's own repository, command and session need to be things a line can
   refer to.
5. **Example data is read as constants**: read literally, migration-tools r21 requires printing "banana" in every
   misversioned repository. Example data must be parameters bound by the scenario.

**Entailment works, with a catch.** With one added rule (refuse = exit with an error), U11 entails the "change nothing"
Then of 6 sample lines, and the check after each scenario already tests it: the owner's idea that entailed Thens need
no scenario holds on real lines. But today's check never pairs U11 with any line, and an If line's hidden precedence
over a When line masks a clash between backlog r20 and r21 (b117).

**The logical form all 27 need** (`sample-semantics.md` §3.5): referents with kinds; parameters for example data;
indexical referents for the run's repository, command and session; about nine atomic predicates (kind, attribute with
an optional order, relation with cardinality and "the R of y", event with roles, run with arguments, output, conforms,
defined condition as a sub-box, initiates / terminates / no change); boxes for the conditional (with a time index and
inertia), negation (with narrow scope), every and only, or, modality (shall, shall not, always/never, may, and a
priority tag for the If form), past-time history and "before the command exits"; and written rules for resolving
"the". With these, every sample line has a formula with truth conditions, and the clash check, the Gherkin generator
and an entailment check can all read the same form.

## The prototype grammar

A throwaway GF application grammar over the RGL, keeping this repository's typed categories per kind and per verb
frame (`prototype-grammar.md`):

- **It parses all 27 candidates without rewording: 26 to one tree, 1 to two** (telemetry r1: whether a list of
  figures belongs to "includes" or to "write"; typing cannot separate them, so a post-parse rule should).
- **Every tree linearises back to its input exactly. All 17 bad sentences are refused**: agreement, a noun of the wrong
  kind, a wrong-kind value, an agentless passive, an undefined coined adjective, an untyped code.
- **Size and speed:** a hand-written core of 28 funs; a 306-line Python generator (about 70 lines of vocabulary data)
  producing 791 funs (504 with determiners as one shared category). Clean compile 0.55-0.7 s, PGF 329 KB, 0.2-6 ms per
  line; at about this repository's vocabulary (4x), 2.1-2.3 s, about 1.2 MB, about 9 ms per line. Today's grammar: 4,841
  funs, 0.7 s.
- **One design choice mattered: verbs split into states and actions.** A state verb goes in While and relative clauses,
  an action verb in When/If and responses. This is the event calculus's fluent/event split arriving in the grammar.
- **What stays for the semantics layer, not the grammar:** whose "its" is, definites with no antecedent, the scope of
  an indefinite under "no" inside While, and implicit comparisons ("a different name"). About 40 generated templates
  each map to one logical condition; logical forms for r33, batches r8 and migration-tools r8 are sketched.
- **A warning:** the first build silently dropped "not" from "and not write the comment"; only the round-trip check
  caught it. A real build must round-trip its whole corpus.
- **What a real implementation needs:** three new fields in the vocabulary (a verb's aspect: state or action; a row's
  word from a small set or a role noun; an order on attributes that are compared), a generator of about 300 lines and
  a core of about 30 funs in place of `spec_typed.py` and `spec_typed_verbs.py`, the RGL pinned beside gf 3.12 by
  `tools install`, post-parse guards, refusal messages rebuilt on the new categories, and a semantics layer written per
  template.

## Where this leaves the language, on Kuhn's PENS scale

My estimate, from the phase 1 scoring (`2026-11-08-cnl-research-phase-1/cnl-practices.md` §1.5): today **P4 E2-3 N4
S3**. The candidate with the prototype's constructs and a written semantics would be about **P4-5 E3 N4 S3**:
expressiveness to ACE's level (relative clauses, "of", quantifiers with scope, negation), naturalness kept (+20% words
per line, -18% counting definitions), simplicity unchanged (a core of about 30 funs plus written reading rules). P5
needs the semantics layer to be defined, not only implemented.

## Questions phase 2 leaves for the design

1. **A second frame per verb, or a second verb?** Verbs with a thing as subject (a measurement names, a requirement
   uses) and words used in two meanings (keep for store) hit 4 of 27 lines here; phase 3 counts them over all lines.
2. **Refusals shortened** to "shall refuse the command and name X", with U11 supplying "exit with an error and change
   nothing": shorter, but it makes those Thens entailed, which needs the entailment check.
3. **Reading rules:** "the" binds to a referent, else the image of a functional relation, else a declared indexical,
   else refused; "no" with narrow scope; "a" in While as "any". Each rule tested against real lines first.
4. **The state/action split of verbs**: in the glossary (an aspect field) or inferred.
