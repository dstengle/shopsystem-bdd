---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-gate-L6
kind: report
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
---

# The GF conversion: the layer 6 gate

## What merged

- gfc/P15 (9784da60), merged with --no-ff as 48ef7bd4. It adds `tests/scripts/test_e2e_codified.py` (228 lines), the
  fixture context in `tests/scripts/fixtures/e2e/repo/`, and report-P15.md. No plugin code changed.
- gfc/P16 (e9dd4570), merged with --no-ff as 99a9a493. It adds only `e2e.md` and report-P16.md, as the plan's
  ownership says. The live run's other commits stay on the scratch branch gfc/P16-live (in the scratchpad clone),
  which was never pushed.
- Neither merge had a conflict.

## The gate

The plan gives layer 6 no gate of its own, so this gate is the two packages' accepts and the common checks. All were
run on the merged branch with SHOPSYSTEM_GF unset.

| check | outcome |
|---|---|
| P15 accept: `test_e2e_codified.py` passes, and the full suite stays green | passes, as part of the full suite run |
| full suite (`pytest -q -p no:randomly`) | 771 passed, 1 skipped, 0 failed (395 s); comm against baseline-failures.txt prints nothing |
| P16 accept: the grep finds the q- and i- ids in e2e.md | exit 0 |
| `tools size --limit 300` | exit 0 |
| `tools check` | exit 0 (nothing to check) |
| ruff on test_e2e_codified.py | clean |
| P14 `model check` grep (v_p*, v15[g-k], v_t[4-6], v_s[1-3], v15f) | no rows, also after q47 was raised |

## Shared changes (P16's ask)

P16 asked for its defects to go to the queue. They are raised as **q47** (commit 9fa7ae8b), "Defects the GF
conversion's live run showed in work run". Its source is the e2e record, it carries the conversion's delegation, and
its six codified lines each parse on the first try:

1. While a term is duplicated, when a session ends an `integrate` stage, `work run` drafts no glossary-proposal
   (defect 1).
2. `work answer` on an `awaiting-answer` glossary-proposal does not set its status to `drafted` (defect 2).
3. `work run` sets no initiative `done` while a glossary-proposal of it is `awaiting-answer` (defect 2).
4. `work run` ends the integrate session when it gives its result (defect 3).
5. `work run` writes the request's resolution when the initiative is done (defect 7).
6. The research stage does not use `--whole-suite` (defect 6, its research half).

The live repo's q47 is not the live run's q47: that one, and its i67, exist only on the scratch branch.

## Fixes

None. Nothing failed.

## Carried forward

- From e2e.md, still to be written as requirement lines, with the person or in a later request:
  - defect 4: nothing limits `work run` with no initiative to one request's intake;
  - defect 5: the error for an ambiguous `work answer <capability>` could name the matching initiatives;
  - defect 6, its other half: the suite runs four times in one delivery.
- From layer 5, unchanged:
  - 25 open proposals in 0.29 lines need re-integration;
  - v16a's date cutoff stays;
  - the optional fixes (spec_grammar helpers, features_generate resolve/Means, vocab bind_all) were not done;
  - `model check` still exits 1 on violations that came before the conversion.
- The conversion's plan is complete: all 16 packages are merged into gf-conversion. Merging gf-conversion into main
  is for the person.
