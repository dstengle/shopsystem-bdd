---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-revision-brief
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# The GF conversion, revision 2: the brief

The person reviewed the converted branch on 2026-11-03 and asked for one revision covering all of the following
("yes, include all of it in the revision"). The first brief (`brief.md`) and its delegation still hold: all judgement
on this branch is delegated, the branch is experimental, keep or rewrite code as needed.

## What the person said (verbatim)

1. "Why is there a given block in every requirement? Can there be a grammatical rule that says 'While a work item is
   drafted' -> Given a work item <generated variable> that is drafted."
2. "Why aren't the repetitive statements with the same sentence through the shall portion, like supervision g13,
   just combined into the same simple sentence with 'and'."
3. "The terms section has a few problems. Some of the terms have long definitions which include logic. There has to
   be a better way of defining the lexicon without needing to specify the different meanings of 'on'. It would appear
   that statements using on are too ambiguous or the grammar needs to be defined in a way that makes all of these
   term definitions unnecessary."
4. "The AST created by GF should have no ambiguity and the work is in converting the grammar into telingo
   statements." / "If we have the EARS parsed through GF into a telingo ASP, it should be possible for the solver to
   find conflicts in the requirements."

## What was found (measured on the branch at 7e0684d2)

- Given blocks: 234 in the spec. Removing each one alone: 63 make `features generate` crash (it cannot introduce an
  instance from a While clause, e.g. supervision g2 "While a work-item is `drafted`" -> StopIteration in
  `precondition`), 169 change the scenario (mostly the While condition silently dropped, e.g. g13 "While a result is
  outputless"), 2 are redundant. About 80 lines are real example data (file contents).
- The grammar (`grammar/Req.gf`) allows one response per statement ("one EARS statement, one shall"), so shared
  triggers are restated per response (g13 r16/r17).
- The lexicon defines each preposition per kind pair as a relation (six "for", five "on" in supervision's Terms);
  88 conditions are defined by an English `Means:` that nothing parses; kinds like worker brief, tool list, round
  brief, review brief and events like log carry requirement content in their definitions.
- `features_generate.py` re-derives scenarios with its own Python rules, separate from the logic translation; the
  solver was dropped from generation on an untested assumption that it "breaks determinism".
- `spec_logic.py`/`spec_solve.py` use telingo's program parts (initial/dynamic/always) and the previous operator only:
  no `&tel{}` temporal formulas, one solve at a fixed horizon 3 with a copied grounding loop, and L4 reachability is a
  Python search.

## What the revision does

A. **One translation.** Each grammar fun has one translation into telingo, using its temporal formulas (`&tel{}`):
   When T, X shall R as always(T -> next R); While C as always(C -> R); shall not as a constraint; U1-U10 as always
   formulas. Telingo's own incremental horizon (not a fixed 3), unsat cores that name requirement and U ids, and
   reachability (L4) asked of the solver.
B. **Gherkin read from the trace.** The scenario of a group is read off a minimal trace the solver finds for it
   (state 0 -> Givens, the trigger -> When, the responses -> Thens), each step linearised through the Steps grammar.
   Determinism by construction: minimise instances, fixed tie-breaks, fixed instance naming, sorted output; a test
   proves the same spec gives the same bytes. The Python generator keeps only reading traces and linearising.
   While/Where clauses and defined conditions reach the Givens through the translation; given blocks remain only for
   example data (file contents, tables).
C. **"and" between responses.** The grammar allows `shall A and B` (and lists) under one trigger and condition; one
   requirement id; the logic and the Thens split the conjuncts. The spec merges statements that repeat a trigger.
D. **Prepositions are grammar.** A preposition between two kinds resolves to the one relation the domain model gives
   for that kind pair; the lexicon holds no per-preposition relation entries. Where two relations share a kind pair,
   they get distinct verbs.
E. **Conditions in the language.** A condition's definition is written in the controlled language and parsed into a
   rule (or the condition becomes an attribute value); no prose `Means:`.
F. **Short terms.** A term entry is one sentence. What a brief, list or log contains or does becomes requirements.
G. **The spec rewritten** to all of the above, all 19 capabilities and the universal conditions; given blocks that are
   not example data deleted. The codified spec was never released, so its ids may be renumbered in this revision;
   `restates` to the 0.29 ids must still cover every 0.29 id (`model restates` 0 missing).

## Done means

The person's four points hold on the branch, checked by measurement, not by report: no given block that is not
example data; no two statements in a group that share their trigger and condition; no relation entry that only names
a preposition, no `Means:` in prose, no term entry over one sentence; `model logic` uses `&tel` formulas with
telingo's incremental horizon and finds a seeded conflict between two requirements; `features generate` reads traces
and is byte-stable; a new request raised with `work request` goes through the new system (P15's test still green);
the suite is green; the size limit holds.
