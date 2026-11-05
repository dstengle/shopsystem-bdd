---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-gate-r2-l2
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: done
---

# The GF conversion, revision 2: the layer 2 gate

**Passed.** On `gf-conversion`, after the layer 1 gate (`gate-r2-L1.md`, 65dbc79a).

## Merges

`gfr/R4` (8b222524), `gfr/R5` (d71aa6c3), in plan order, `--no-ff`. No conflicts: the packages own disjoint files.

## Shared changes made by the gate

1. **`model logic` under 60 s.** On the merged spec, R4's code took 89 s wall. A profile per group showed the time
   was two groups, supervision g50 and g51 (71 s each, the critical path; every other group under 10 s). Both are
   UNSAT: the whole cone is UNSAT in 1 s, and the confirmation on the core (r52 with r72/r73), with the engine's pool
   retry at n × imax + 1, took 58 s at the cone's imax 5. The core's own edges give imax 3, and the core program
   UNSAT at its own horizon bound is UNSAT at every horizon (design-r2 §6.3's argument, applied to the core), so
   the confirmation now runs at the core's bound: 4 s. Test first:
   `test_an_unsat_core_is_confirmed_at_its_own_horizon_bound` (a cluster copy where r20 lengthens g11's cone to
   imax 4 while its core r11, r12 stays at 3). The findings are byte-identical before and after. The §6.4 sha cache
   is not needed.
2. **Same-named conditions (R5's ask to R4).** `Lexicon.definition` looked a condition up by name, so open
   (work-item) got the open (initiative) `Def`. It now matches the entry when given one, by name otherwise. Test
   first: `test_same_named_conditions_have_their_own_definitions`.
3. **Term ids (R5's ask).** `model_spec.term_word` keys a condition `<term> of <kind>` when another entry has its
   word, not only when it has no gloss. This removes the 4 v_t2 rows (closed, open, termless, unparsed) R5's glosses
   brought. Limited to conditions: a glossed attribute keeps its bare id (`test_model_glossary` fixes that). Test
   first: `tests/scripts/test_model_spec_terms.py` (new; `test_model_spec.py` is at 299 lines).
4. `report-R4.md` and `report-R5.md` written from the packages' notes (kind `design`).
5. **The allowance shrinks** from 56 to 20 ids: the 36 R4 named (all of `test_spec_logic`, `test_spec_solve`,
   `test_supervise_outputs`, `test_spec_guarantees::test_the_logic_check_finds_no_error[*]`) now pass.

## The gate's checks

| Check | Result |
|---|---|
| `time python3 scripts/model logic` (merged spec) | **26.4 s** wall (329 s CPU); 89 s before change 1 |
| `model logic --json` | exit 1: 8 L1 (supervision g2, g6, g34, g35, g40, g42, g50, g51, R4's real ones), 7 L2 (the baseline's); identical before and after change 1 |
| layer tests (`test_spec_logic`, `test_spec_solve`, `test_spec_lexicon`, `test_model_spec_terms`) | 48 passed |
| `tools size --limit 300` | exit 0 (`spec_solve.py` 300) |
| full suite | 20 failed or errored, 805 passed, 1 skipped; each in the new allowance |
| common check against `baseline-failures.txt` + `gate-r2-L1-allowed.txt` | prints nothing |
| scenario suite | only the allowed formulate scenario fails |
| `grep 'HORIZON = \|def _ground\|_reachable\|def _edges' scripts/spec_solve.py` | nothing |
| `grep -rn 'Means:' spec/` | nothing |
| q47 lines, `model parse --file` | exit 0 |
| `unparsed.sh \| comm -13 unparsed-L1.txt -` | nothing |
| `model lexicon --check` | 337 terms, 9 problems (6 v_t8, 3 v_t10; see below) |
| `model check` against 65dbc79a | the same rows and counts (776 violations, 16 warnings, 34 unresolved, 7 file problems) |
| `tools check` on the changed files | clean |

## Left open

- **The lexicon's 9 problems** (R5's accept `0 problems` is not met). They are six preposition entries the
  checked-in features' GivenR steps still need; removing them needs `features_vocab` to build its relation steps
  from `spec_relations.sources(lex)`. That is R6's file in layer 3, and R5's trial broke 38 scenarios, so the gate
  hands it to R6 (or the layer 3 gate) with R5's ask 1 (`report-R5.md`). `test_the_lexicon_has_no_problem` stays in
  the allowance until then.
- The allowance now holds `features_generate` failures (R6), `test_e2e_codified`, and the two lexicon tests.
- Carried from layer 1: the `spec_tree.guard` rule (layer 3 gate, with R6), the fixture glossary
  (`test_lexicon_lists_terms_by_category`), module-map rows for R14 (now also R4's, in `report-R4.md`).
