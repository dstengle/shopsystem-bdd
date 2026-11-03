---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-report-p9
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# Report: P9, the 11 guarantees capabilities converted

Branch `gfc/P9`, commits b9caeea1, f284511a. Written by the layer 3 merge from the package's returned notes: the harness refused the package's own write of this file. done=false only for two checks resting on files outside P9; both
were settled at the merge (`gate-L3.md`).

## What was converted

All 11 files, each with its marker, `retired: []`, fresh ids, Restates, Terms and Dropped: 120 groups and 204
statements from 156 lines. Wording the grammar cannot carry went to prose under "Implementation, may change".

| capability | groups | statements |
|---|---|---|
| code-research | 7 | 14 |
| delivery | 11 | 19 |
| formulation | 0 | 0 |
| planning | 7 | 11 |
| red-green | 15 | 22 |
| review | 22 | 37 |
| role-boundaries | 6 | 22 |
| spec-consistency | 17 | 20 |
| spec-integration | 16 | 22 |
| spec-migration | 14 | 31 |
| trials | 5 | 6 |

Deleted `features/spec-consistency.feature`, `features/spec-integration.feature`, `spec_integration_steps.py`,
`spec_integration_apply_steps.py`, `test_spec_integration.py`. New: `tests/scripts/test_spec_guarantees.py`.

## Moves and drops

- formulation: r1, r2, r6, r7, r11, r22 moved to supervision (P12 restates them); r3, r4, r5, r9, r10, r13, r14, r23
  dropped with reasons.
- spec-integration: r44, r45, r46, r54, r55 moved to supervision; r16 and r22 moved to design-model-check (P11
  restates them); r13 dropped (v5 C18). No line names `features`.

## Calls

- Shared roles and events in role-boundaries' Terms (at the merge, the ones P10/P11 also gave moved to `spec/index.md`).
- review adds `of (commit → work-item)`; `belongs to` parsed as a preposition relation and read badly.
- `t_ThatIs` takes one value, so value lists went to prose.

## Checks on the branch

`model logic` and `model restates` exit 0 for all 11; `test_spec_guarantees.py` 59 passed; lexicon 242 terms, 0
problems; size and ruff clean. Failed on the branch, fixed at the merge: `model parse --file` (raw lines),
`LiveRestatesTest` (asserted spec-migration unconverted), `v15i role-boundaries#r8` (i59's open proposal adds that id).

No new module.
