---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-gf-conversion-report-checker-gaps
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: done
---

# The checker's own gaps (after S11 and S12)

Branch `gfr3/checker-gaps` from ce1179d1, head 8cfb9f40, merged as 69d5c872. `spec/` was not edited.

## Counts

| | L1 | L5 | L6 |
|---|---|---|---|
| before | 32 | 6 | 0 |
| after | 25 | 6 | 4 |

By question:

| question | before | after | note |
|---|---|---|---|
| Q_STAGE | 2 | 2 | |
| Q_RELEASE | 3 | 3 | still L1, see gap 4 |
| Q_LINES | 3 | 3 | |
| Q_CLOSED | 4 | 4 | its second half answered |
| Q_ONE | 13 | 13 | |
| Q_RESULT | 6 L1 | 4 L6 | r46/r47 and r57/r63 cleared |
| Q_COMPLETE | 1 | 0 | |

No new finding. `model logic` on the live spec: 1.3 s.

## Gaps and fixes

1. **Q_ONE.** All 13 come from untied indefinites in While clauses, not from an unbound "the" or an anaphor.
   - Under the existential reading they are real clashes. Merging indefinites would undo S11's "no remote is
     unpushable".
   - What was a checker gap is fixed: an unbound definite gives `the/2`, and `check.lp` reads it as the one thing of
     its kind. None of the live spec's 45 unbound definites is among the 13.
2. **Q_RESULT.** `fun(Q)` marks a functional relation: a relation row of cardinality one, or a row with no
   cardinality whose word is a bare preposition (for, with, on, of, in).
   - A thing related to two different things through such a relation is out.
   - r46/r47 and r57/r63 clear; 4 become L6.
3. **Q_COMPLETE, and Q_CLOSED's second half.**
   - "every K … is C" in a clause is a universal (`uall`, `urel`, `uattr`, `ucond`, `uccond`).
   - A `Def` made of literals on its own subject becomes domain facts `dalt`/`dlit` (`spec_facts.def_facts`). It is
     read under `no` (entailed → out), under `every` (refuted → out) and under negation.
   - r5/r7 clears.
4. **Q_RELEASE and design-r3 §3.2.** `prose(C)` marks a condition with no `Def`.
   - `maybe/4` gives an L6 when the witness puts a prose condition from one side on an instance the other side says
     more of. The text comes through the `focusm` external, and witnesses now show conditions (`prec/5`).
   - r13–r16 stay L1. A second witness has two repositories: "a repository" is not tied to the run, which is
     Q_ONE's issue.
   - design-r3 §3.2 is corrected.
5. **Leftovers.**
   - `rnone` is read.
   - The L5 text is worded ("give a review finding a grade").
   - A live test fails when an `EXPECTED` entry stops firing.

## Calls made

- A relation row with no cardinality and a preposition for its word is functional; a verb is not.
- An unbound definite is the unique thing of its kind.
- Indefinites stay existential, so Q_ONE stays a question. Its proposed fixes are to tie the noun to the trigger's
  object, or to say "the K".
- L6 needs the other side to say more of the instance. When both sides say the same things, it stays L1.
- Only a singular "every K" is a universal. Plurals stay roles, so no Givens change.

## Verification

| check | result |
|---|---|
| `pytest -n 8 -q` | 938 passed, 1 skipped, 129 subtests, 19.5 s |
| `features generate --check` | exit 0, no feature changed |
| `tools size --limit 300` | exit 0 |
| `tools check scripts tests` | clean |
