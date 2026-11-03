---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-report-r2
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: done
---

# R2: the lexicon, the readers and the model rules (revision 2, layer 1)

Branch `gfr/R2`, off `gf-conversion` at 864f61e9. Built test first: each test was written and failed before its code.

## What was built

- **`scripts/spec_read_given.py` (new).** First commit: the given-block reading (`Block`, the fence's lines) moved out
  of `spec_read.py` with no change in behaviour (`test_spec_read`, `test_model_spec` green before and after).
  Second: `example(line, block)`, the shape test of example data with no grammar: `the <words> <name> holds:` with
  a docstring or table under it, or `the <words> <name> holds` followed by exactly one code span or quoted string.
  `spec_read.Block` is still importable.
- **`scripts/spec_relations.py` (new).** It reads the `## Relations` tables of `spec/index.md` and of every
  capability (`Row(k1, word, k2, cardinality, where)`, header and rule skipped, backticks stripped). Legacy
  relation entries count as rows. `Kind of:` is expanded at any depth, and the supertype keeps its own row. It also
  gives v_t4 for a row or `Kind of:` naming no kind, v_t8 and v_t10.
- **`scripts/spec_lexicon.py`.** `Term.supertype` (from the new `Kind of:` field), `Lexicon.rows`,
  `Lexicon.relations()` -> sorted `(k1, word, k2, rid)`, `Lexicon.definition(term)` (a name or a `Term`; the gloss
  of a condition, "" if none), `gloss(text)`, `one_sentence(text)` (design-r2 §8's counting rule), v_t7 and v_t9.
  `words()` adds the row words. `Means:` is still read into `Term.means` for the old logic, and is now v_t9.
  `Lexicon(terms)` still builds positionally, because `rows` defaults to empty.
- **`scripts/model_spec.py`, `scripts/model.lp`.** Two new facts: `given_condition(G, Line)` for a given line that is
  not example data, and `#defined given_condition/2`. Three new rules: v15l (a group with more than one statement),
  v15m (`given_condition`) and v15n (two groups of one capability whose statements have equal `pre` keys, the same
  normalised features|condition|trigger trees that v15k compares). `term_word` now keys a term `<term> of <kind>`
  when an attribute or condition entry has no gloss, instead of when it "opens with Values: or Means:". Every term
  id is unchanged today.
- **`scripts/model`.** The contract no longer says `Means:`. It now names the relations table, `Kind of:`,
  v15l/v15m/v15n and v_t4–v_t10. `parse --grammar` takes `Req`, `Steps` or `Def`; `Def` is built by R1's
  `spec_grammar`, so on this branch alone it exits 2 with "no grammar Def".

## Interfaces for the other packages

- **`rid`** is `r_<k1>_<word>_<k2>` (slugged) of the row *before* expansion. Every expanded row shares it:
  (stage, for, node) gives `r_stage_for_node` for the node, work-item, ... rows. Legacy entries get the same form,
  and do **not** use the old `lex.ids()` relation id (`r_for_2`, ...). R1's `rel_<k1>_<word>_<k2>` funs come from the
  expanded triple, and R4's `rel/3` should use this `rid`.
- `spec_relations.expansion(lex)` also returns the source row of each expanded triple, if a package needs to know
  where a relation came from.

## Acceptance

| check | result |
|---|---|
| `pytest tests/scripts/test_spec_lexicon.py test_spec_relations.py test_spec_read.py test_model_spec.py` | 62 passed |
| tests v_t7–v_t10, v15l, v15m, v15n fire on a fixture and stay silent on a clean one | yes (`test_spec_lexicon`, `test_spec_relations`, `test_model_spec`) |
| v_t7's cases: a code span holding `.`, `e.g.`, a `:` gloss and a trailing field pass; two sentences and a `;` fail | yes (also `!`, and a quoted string holding `.`) |
| v15m's cases (`holds:` + docstring and `holds "x"` pass; `a result r1`, `the result r1 is outputless` fire) | yes |
| `relations()` expands a `Kind of: node` row to each subkind and keeps the node row | yes |
| `model lexicon --check` on the live spec | exit 1: 386 terms, 134 problems: **v_t7 22, v_t8 28, v_t9 84**, v_t10 0 (R5 clears them) |
| `model check --json` rules among v15l/m/n | `['v15l', 'v15m', 'v15n']`: **v15l 145, v15m 361, v15n 217** rows (layer 4 clears them) |
| v15m's count equals the given lines that are not example data | 441 given lines − 80 `holds` lines = 361, which equals v15m's 361 rows; supervision has 65 groups with v15m (its 65 blocks) |
| `wc -l` spec_lexicon 229, spec_read 202, model_spec 195 (spec_relations 117, spec_read_given 63) | each ≤ 300 |
| `tools size --limit 300` | exit 0 |

v15l rows for each capability: supervision 39, analysis-tools 12, migration-tools 12, batch-measurement 11, review 9,
requests 8, red-green 7, spec-migration 7, work-queue 7, delivery 6, role-boundaries 6, spec-integration 5,
planning 4, code-research 3, design-model-check 3, feature-file-tools 3, spec-consistency 2, trials 1.
v15m: supervision 156, design-model-check 86, batch-measurement 39, analysis-tools 31, requests 20, work-queue 17,
feature-file-tools 12.
v15n (pairs): migration-tools 111, batch-measurement 73, analysis-tools 18, feature-file-tools 6, supervision 5,
code-research, design-model-check, requests and review 1 each.

## The full suite: three new failures, for the layer 1 allowance

Running `pytest -q -p no:randomly` gives 3 failed, 783 passed, 1 skipped. Nothing fails in the scenario suite. The
baseline-failures.txt entries pass on this base. The three failures are outside the traceback rule
(`spec_logic*`, `spec_solve`, `features_generate`), but each one follows from this package's own acceptance:

1. `tests/scripts/test_spec_guarantees.py::test_the_lexicon_has_no_problem`: the live lexicon now has
   v_t7/v_t8/v_t9, which the plan says R5 clears.
2. `tests/scripts/test_model_output.py::LanguageCommandsTest::test_lexicon_lists_terms_by_category`: it expects
   `lexicon --check` to exit 0 on `tests/scripts/fixtures/glossary/`. That fixture keeps `Means:` and preposition
   relation entries (v_t9, v_t8), and the old logic still reads them.
3. `tests/scripts/test_e2e_codified.py::test_a_request_goes_through_the_requirements_system_into_delivery`: its
   fixture `work-queue` has two-statement groups and condition given lines (v15l, v15m), so `model check` exits 1.
   The plan already lets this file stay through layer 3.

**Ask:** put these three in `gate-r2-L1-allowed.txt`. They clear when the glossary fixture and the live glossary are
rewritten (R5, and whoever owns `tests/scripts/fixtures/glossary/` once R4 stops reading `Means:`), and when the
e2e fixture is rewritten (layer 4, R12).

## Calls made under the delegation

- **v_t7–v_t10 are `model lexicon --check` problems only. They are not `model check` rules yet.** Several suites
  (the design-model-check, requests and supervision scenarios, `test_model`) build repositories from the glossary
  fixture and expect `model check` to be clean there. Making the legacy fixture's `Means:`/preposition entries
  violations would turn the scenario suite red, and it must stay green in every layer. design-r2 §9.2 step 6 says
  "`model check`: no ... v_t7–v_t10 rows". **Ask (R14):** once the fixture is rewritten, emit them as facts
  (`lex_problem(Code, Term, Message)` and a rule for each code) so that `model check` shows them.
- **v15n leaves out ubiquitous statements**, because they have no `pre` key, as in v15k. Two trigger-less,
  condition-less groups would otherwise always be "the same (features, condition, trigger)" and be merged into one.
- **An empty gloss passes v_t7.** An attribute that opens with `Values:` has no sentence to count. A gloss without
  a final full stop counts as one sentence.
- **v_t8 is a relation entry whose term is exactly a preposition** (`spec_typed.PREPOSITIONS`: for, on, in, of,
  with, outside, under, ...). Verb relation entries (fulfils, blocked by, part of, ...) are rows read from the
  legacy entry. They are not v_t8, and R5 moves them to the table.
- **v_t10 counts after expansion, and across tables and legacy entries.** So a local row that a supertype row
  already covers is caught.

## Module map rows (for R14 to write into CLAUDE.md)

| Module | Concern |
|---|---|
| `scripts/spec_relations.py` | the relations of a context: the `## Relations` tables, `Kind of:` expanded to subkinds, and v_t8 and v_t10 (design-r2 §4.2, §8) |
| `scripts/spec_read_given.py` | a codified group's given block read for spec_read, and the shape test of example data (v15m; design-r2 §9.1) |
