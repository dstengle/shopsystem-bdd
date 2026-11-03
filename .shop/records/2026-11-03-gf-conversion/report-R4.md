---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-report-r4
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: done
---

# R4: the &tel translation and `model logic` (revision 2, layer 2)

Commit 8b222524 on `gfr/R4`, off 65dbc79a. The package could not write this file (the harness refuses report files
from a subagent); the layer 2 gate wrote it from the package's returned notes.

## Files

`scripts/spec_logic.py` (rewritten), `scripts/spec_logic_np.py` (new), `scripts/spec_logic_vocab.py`,
`scripts/spec_solve.py` (rewritten), `grammar/background.lp` (rewritten), `tests/scripts/test_spec_logic.py`,
`tests/scripts/test_spec_solve.py`, and the cluster fixture (`## Relations`, a `Def` for open, g12 added).
`scripts/model_report.py` needed no change.

## Checks (on R4's base)

- `test_spec_logic` + `test_spec_solve`: 32 passed: `test_statement_is_a_tel_constraint`, a test for each row of
  design-r2 §5.2–5.5, `test_labels`, `test_signatures`, `test_contrast_in_witness`, a `Def` definition rule, L3 through
  a `T:` guard, L4 asked of the solver, and `test_seeded_conflict` (built from the live spec; one L1 naming both ids).
- `grep 'HORIZON = \|def _ground\|_reachable\|def _edges' scripts/spec_solve.py`: nothing; `HORIZON = ` in
  `scripts/`: nothing.
- `time model logic`: 94 s wall (7m44s CPU on 32 cores), against 310 s at layer 0; context and parse 14 s of it.
- `model logic --json` against `logic-baseline-r2.json`: 8 new L1s, all supervision, all real (below); the 7 L2s
  unchanged; nothing disappeared.
- `tools size --limit 300`: exit 0 (`spec_logic.py`, `spec_solve.py` 298 lines each). `tools check`: clean.
- Full suite: 17 failed, 802 passed, 3 errors; the common check prints nothing. 36 allowed ids now pass.

## Calls made

1. The label is `no(i)`, not `not(i)`: `not` is a clingo keyword.
2. The witness labels the trigger's and the subject's restrictions `mod(0,j)`.
3. Signatures name the doer (`does(a_x)`/`does(k_x)`); `does(anyone)` triggers are expanded by `spec_solve.anyone`.
   Without this, cones held ~160 statements.
4. A pool is the most NPs of a kind in one part, plus 1 (design said the sum over the cone; the sum ran >800 s). An
   UNSAT cone is confirmed on its core with the engine's n*imax+1 retry, sound because the core is a subset. Only
   when the core is SAT is the whole cone retried.
5. Groups are solved in parallel in forked processes, in fixed order.
6. An unbound `the X` object is existential.
7. `only a K` as an object is a restriction.
8. A quoted text becomes its bare words, because telingo mis-reads `\"` in theory atoms.
9. A condition is defined iff its gloss parses as `Def`. On R4's base all were primitive (R5 adds the `Def`s).

## The 8 new L1s (real; layer 4 moves the given-block conditions into the statements)

- g2 and g40: r2 against r53, drafted start / not start.
- g6: r2 and r53.
- g34: r2, because r2 has no "remote not unpushable".
- g35: r54 against r47.
- g42: r54 against r58.
- g50 and g51: r52 against r72 and r73.

## Interface for R6

Label parts are `feat(i)`, `cond(i)`, `trig`, `mod(0,j)` (the trigger's and subject's restrictions), `resp(i)`,
`mod(i,j)` and `no(i)`. A negative leaf is `neg(A)`. Trigger atoms may be `set_to`/`done_to`/`ran_any`. Use
`program(parts, optimise=True)`; use `spec_solve.Context`/`solve` for the cone. `cond(c_free,R)` is shown for every
resource.

## Module-map rows (for R14)

| `scripts/spec_logic.py` with `scripts/spec_logic_np.py` | the &tel translation of a requirement tree, its labels and signatures, the witness of a group, condition definitions |
| `scripts/spec_logic_vocab.py` | the lexicon's facts for the logic, guarded transitions, pool sizes |
| `scripts/spec_solve.py` | `model logic`: L1–L4 on spec_engine, groups solved side by side |
