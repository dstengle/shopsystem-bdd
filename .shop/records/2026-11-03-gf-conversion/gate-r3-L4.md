---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-gf-conversion-gate-r3-l4
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: draft
---

# Revision 3, layer 4 gate

The gate passed on `gf-conversion`. Base caff28e8.

## Merged

- `gfr3/S10` (head daeffa15), `--no-ff`, no conflicts. Its report was refused by the harness; the gate wrote
  `report-S10.md` from the task's notes.

## Review

- **Outside the file list.** S10 changed `scripts/spec_facts.py` (2 lines) and `scripts/spec_steps.py` (1 line),
  which the plan forbids for S10. Accepted: the L2 gate assigned the anaphor defect to "S10 or S11", the lower-case
  letter is forced by the frozen `features_vocab.NAME`, and each fix has a test that pins it (the r2 facts example
  checks the second response's object is `v2` and that no third role is made). The anaphor fix changes the facts
  `check.lp` reads, which S11 should know when it counts clashes.
- **Handlers.** The fixes are defaults in the world for conditions the regenerated Givens state (`closed`,
  `not open`) and a node Given that no longer overwrites relations earlier Givens wrote. No Given added, no feature
  edited, `vocab.py` and `spec/` untouched. No S11 items from S10.
- Size and module map: no new module; every file within 300 lines.

## Fixed by the gate

Nothing beyond writing `report-S10.md`.

## Runs on gf-conversion after the merge

- `python3 scripts/tools size --limit 300`: exit 0.
- `timeout 600 python3 -m pytest -n 8 -q -m "not fixture and not live_logic" --durations=5` (the full suite,
  `test_supervision.py` included for the first time at a gate): 903 passed, 1 skipped, 129 subtests, 20.3 s. Slowest:
  e2e 6.3 s, supervision flaky-scenario 5.1 s; nothing over 10 s.
- `python3 scripts/features generate --check`: exit 0. `python3 scripts/features vocab --check`: OK.
- Not run, by the rules: the `live_logic` tests (S11 once, S12).

## Left

- `$SLOW` is now just `-m "not fixture and not live_logic"`: no file is ignored any more.
- S11 runs the live check on the facts with the corrected anaphora (supervision r39, requests r2 changed).
