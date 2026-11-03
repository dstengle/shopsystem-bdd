---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-report-p6
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# Report: P6, the logic check

Branch `gfc/P6`, commit db653147. Written by the layer 2 merge from the package's returned notes: the harness refused
the package's own write of this file.

## What was built

- `scripts/spec_logic.py` (286 lines): one rule per core and typed fun, a statement as a constraint guarded by `on/1`,
  a group's witness, the program with `grammar/background.lp` (design §12.1).
- `scripts/spec_logic_vocab.py` (155 lines, outside P6's list, accepted at the merge): `spec_logic.py` was 322 lines,
  so the vocabulary and `facts()` moved out; P2's `spec_typed.py` is the precedent.
- `scripts/spec_solve.py` (265 lines): telingo's grounding loop (copied, MIT notice kept), one solve per group with its
  minimised core, L1–L4, text and JSON reports (design §12.3).
- `grammar/background.lp`; `tests/scripts/test_spec_logic.py`, `test_spec_solve.py`,
  `tests/scripts/fixtures/logic/cluster/`.
- Interface: `spec_solve.run(root, capability=None, extra=None) -> [Finding(code, ids, text)]` and
  `spec_solve.report(findings, as_json) -> (text, exit)`; exit 1 on L1/L3. `run` reads only codified capability files
  plus `spec/universal.md`, leaves out lines that don't parse or are ambiguous, and lets an extra draft replace the
  spec capability of the same name. On the live repo today it gives no findings.

## Calls made

1. Noun phrases are read universally; the/it bind the last noun phrase of that kind. An existential object of a
   `shall` response is a new thing `n(id,k)`, and "shall … no X" reads as "shall not".
2. Witness: a plural or "every" is two things. The pre-state holds at step 0, pre-state and trigger at step 1, the
   responses are due at step 2. Only the witness's trigger and the responses statements ask for happen (choice rules).
3. Deviation from design §12.2: the background does not refuse an off-table Set. L3 reports it statically, so it is not
   also an L1.
4. `free` means a resource's running holders are within capacity (1 if exclusive, 3 if counted by a code). Lexicon
   resources are bridged to the kind `resource`, and to `needs`, through holds, so U2 alone carries exclusivity and is
   named in the core. The L1 carry for P6 ("a resource cannot be a noun phrase") needed no grammar change.
5. `on/1` is per step (telingo). The core is mapped back to ids and minimised one id at a time.
6. A Means of the form "its <attr> is [not] values" becomes a rule; any other Means leaves the condition free.

## Checks (P1's install, SHOPSYSTEM_GF unset)

- pytest `test_spec_logic.py`, `test_spec_solve.py`: 27 passed.
- L2 `supervision#r3 and supervision#r4 say the same thing` (r66/r95). L1 `supervision#g5 (r5) cannot happen:
  conflicts with supervision#r2, U2`, ids [g5, r5, r2, U2]. No L1 names g6–g8/r6–r8 (resource formulation); the
  cluster without g2 gives no L1. L3 finds r9 (`proposed`→`abandoned`), not r11. L4 finds g10 (`awaiting-asker`).
- The 40-group fixture finishes in under 10 s (asserted); the cluster takes about 0.3 s, about 0.15 s per group with
  180 statements in the background. Horizon 3; no `--horizon` flag needed.
- Outside the suite: P2's 182 corpus lines, each as its own group against all of them, give no L1 in 27 s.
- `tools size --limit 300`: exit 0. Suite at baseline. ruff and `tools check` clean.

## For later packages

- P8: `## Terms` in a drafted extra file are not added to the lexicon.

## Module-map rows

- `scripts/spec_logic.py` | `model logic`'s translation: one rule per core and typed fun, a statement as a constraint
  guarded by `on/1`, a group's witness, the program with `grammar/background.lp` (design §12.1)
- `scripts/spec_logic_vocab.py` | the lexicon's side of the logic: typed funs traced to their lexicon entries, a
  condition's `Means:` values, the context's facts for the background theory
- `scripts/spec_solve.py` | `model logic`'s checks L1–L4: telingo's grounding loop (copied, MIT notice kept), one
  solve per group with its minimised core, the text and JSON reports (design §12.3)
- `grammar/background.lp` | the background theory: frame axioms, running sessions, resources and `free`
