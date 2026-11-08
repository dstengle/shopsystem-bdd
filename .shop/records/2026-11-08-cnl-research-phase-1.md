---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-08-cnl-research-phase-1
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-08
---

# CNL research phase 1: the field and where this CNL sits

## What was done

Phase 1 of b112's research (`.shop/backlog/b112.md`): five researchers in parallel, each given the brainstorming's
conclusions, wrote one report each, kept beside this record in `2026-11-08-cnl-research-phase-1/`:

| Report | Strand |
|---|---|
| `cnl-practices.md` | CNL best practices; Kuhn's PENS classification (2014); requirements CNLs; failure modes |
| `logic-cnls.md` | Attempto (ACE), SBVR Structured English, PENG / PENG-ASP, OWL CNLs; their semantics and time |
| `requirement-cnls.md` | NASA FRET / FRETish, EARS and its formalisations, Dwyer's specification patterns, requirements-to-test and monitors |
| `gf-cnls.md` | GF's own CNL work, the Resource Grammar Library (RGL), and a compiled spike of an RGL-based typed grammar |
| `our-cnl.md` | this repository's CNL end to end, with file:line references and measured usage of its 265 lines |

Sources the researchers could not read in full are marked in each report (FRET 2021/2022 full texts, EARS-CTRL, Rimay,
Stimulus, Wyner et al. 2010, the SBVR standard; APE's web service was down, so ACE examples come from its manuals).

## Where this CNL sits

On Kuhn's PENS scale (provisional, `cnl-practices.md` §1.5): **P4 (P5 parts), E2 or a weak E3, N4, S3**. Precise and
natural enough; low in expressiveness. Its nearest relatives score: ACE P4E3N4S3, PENG P5E3N4S3, SBVR Structured
English P3E4N4S2, Gherkin P5E3N4S3. The literature's name for the core problem is poor **habitability**: writers cannot
say what they need, so they work around it ("easy to read, hard to write"). The 170 condition entries, 145 of them
prose, measure the workaround.

Where it is ahead of every system surveyed: a typed vocabulary with verb frames enforced in the grammar, and Gherkin
generated from the same facts the logic checks. No other system found does both.

## The eight suspected weaknesses, tested

| # | Weakness | Verdict | Evidence |
|---|---|---|---|
| 1 | No formal semantics | confirmed in substance | One written translation per fun exists, but a line means something only through `check.lp`'s pairwise clash search: no formula with truth conditions, so "is this already entailed?" (needed to leave entailed Thens out) has no basis. ACE: sentence -> DRS -> first-order logic; PENG-ASP: DRS-like form -> ASP, round-trip. GF gives no semantics by itself (`gf-cnls.md` §1). |
| 2 | "a"/"the" under negation and in While | confirmed | "a" in While reads as "any" (right). "does not hold a K" reads as "some K not held", unlike "holds no K"; "the" with no antecedent reads as the only one of its kind. ACE fixes all of these with written scope and accessibility rules. |
| 3 | Time: two states only | confirmed, narrower than feared | Past-time constructs ("only after", "once", "since") compile to history fluents one event sets: fits the two-state check. Future time ("eventually", "within N") needs traces: monitors. The owner's "background task always running" is safety (an invariant), not liveness. |
| 4 | Modality: shall / shall not only | confirmed | SBVR: necessity vs obligation vs permission; ACE: can/must/may. "may" and "never" are refused here. |
| 5 | Number and quantity | confirmed | "at most one" and "one" mean the same as "a"; no counts, "empty", comparisons. |
| 6 | Collections | confirmed | ACE plurals, "each of", "at least/at most/exactly n"; PENG-ASP maps "exactly one" to a clingo cardinality rule. |
| 7 | Vocabulary model | partly | Since 3.0 actors sit in the kind hierarchy (19 of 27 have `Kind of:`). Still: one word with several meanings (`closed` x4, `malformed` x4, `open` x2), dead terms unreported (9 resources, 55 prose conditions used by no line). |
| 8 | Noun phrases | confirmed, the main finding | Every logic CNL has relative clauses from any verb ("a customer that owns a card", "every country that borders no body of water"). That construction is what removes coined adjectives. Here: only "that is <condition>" and "whose <attribute> is <value>". |

Weaknesses found that were not on the list (`our-cnl.md` §6):

- **Triggers are command strings.** 93% of triggers are "X runs `cmd`", 92% of lines hold a code, 74 lines put
  arguments or example data in it: the language describes a CLI's test cases more than its behaviour, and the check can
  pair only lines with byte-identical commands.
- **The fixed response verbs** (print, exit with an error naming, change nothing, exit successfully) are 246 of 443
  response conjuncts and have no frame.
- **Silent prose:** a definition that fails to parse becomes prose with no diagnostic.
- **Gherkin and the logic disagree** on `every`, `only` and negated objects: the generator reads them, `check.lp` does
  not.
- **Hand-written surface forms:** no RGL; 4,841 generated funs, 672 of them only to say "not"; a live agreement defect
  ("When sessions writes a file" parses; "When sessions write a file" is refused with a misleading message).
- A blank cardinality on a preposition row silently means "exactly one" in the check.

## Why it is where it is

The design rules of the GF conversion, read together (`our-cnl.md` §7): **one tree or refused** kept out every
construct that multiplies trees (relative clauses, "of", possessives); **no escape hatch** forbade free text in lines;
the **growth rule** ("a core fun only for a construct that recurs in two capabilities"; "a target project grows its
language by glossary entries only") left consumers one open slot, the glossary. A missing structure therefore became a
term: the coined adjective is the escape hatch, moved into the lexicon. The design-r3 speed fix (two states, one
generic instance per noun phrase; 227 s down to 4 ms) fixed time at two states and left plurals and counts unread.

## What the field offers, by weakness

| Need | Proven answer | Source |
|---|---|---|
| Meaning of a line | A DRS-like intermediate form between tree and facts: referents, fixed atomic predicates, boxes for not, if, or and modality; translated once to clingo; read by the clash check, the steps and an entailment check | ACE, PENG-ASP (`logic-cnls.md` §7) |
| Reading rules | Written interpretation rules (scope, accessibility of "the" and "it", "a" under "not") and a paraphrase back to the writer | ACE, CLCE |
| Noun phrases | Relative clauses from any verb frame, "of" and the genitive, "no" inside them; counts | ACE, PENG; RGL gives the surface forms |
| Modality | Necessity (always/never: invariants), obligation (shall), permission (may), each with a fixed reading | SBVR, ACE |
| Time | Fixed time fields, not vocabulary: FRET's scope / condition (edge vs level) / timing; Dwyer's patterns and scopes; event calculus (While = fluent holds, When = event happens, shall = initiates/terminates, inertia) on clingo | FRET, Dwyer et al. 1999, PENG-ASP, Hall et al. 2021 (EARS -> event calculus in s(CASP)) |
| Verification routes | Pattern decides route: next-step response = scenario; invariant or bounded response = monitor or check after each scenario; precedence = invariant over a history fluent; unbounded liveness = judgement until bounded. FRET generates monitors from past-time formulas (Ogma, Copilot) | FRET, `requirement-cnls.md` §1 |
| Surface grammar | An application grammar over GF's RGL, keeping this repository's typed categories per kind and frame: agreement, negation, relative clauses, genitives from the library | Ranta & Angelov 2009; ACE-in-GF; spike in `gf-cnls.md` §4 |
| Writing support | Predictive (look-ahead) authoring: GF's incremental parser offers the next words | PENG, AceWiki; GF runtime |

The GF spike (compiled with this repository's gf 3.12 and gf-rgl 20250812): "a channel that a viewer subscribes to",
"the credentials of the request" / "the request's credentials" and "does not conform to the comment schema" each parse
to one tree with typing intact; a plural subject with a singular verb and a channel subscribing to a viewer are
refused. A generated RGL grammar of 320 kinds and 160 verbs compiled in 6.1 s (this repository's: 0.7 s, absorbed by
the PGF cache) and parsed 20-30-token lines in about 4 ms. The RGL's defaults need overriding ("doesn't", no comma
after a While clause, "which").

## Questions for phase 2

1. How does each sample line read in ACE, SBVR Structured English, FRETish and an EARS-with-patterns form, and what
   does each need from the vocabulary?
2. Which sample lines would a DRS-like intermediate form and written reading rules change in meaning (H1, H2)?
3. Which coined adjectives disappear with relative clauses, "of", conformance to a named artifact and a modal set?
4. Which lines are really invariants, precedence rules or bounded responses, and what verification route each gets?
5. A PENS score of the current language and of a candidate design.

## Bugs found on the way

Filed as backlog ideas, apart from b112's redesign: the subject-verb agreement defect; the readings the check and the
Gherkin generator disagree on (`every` on an object, `only`, "at most one", a negated indefinite); and the silent
"exactly one" of a blank cardinality.
