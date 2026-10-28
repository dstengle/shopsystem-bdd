## Budget

- tests/scenarios/supervision_integrate_steps.py
- tests/scenarios/supervision_proposal_steps.py

## Changed

The Then of r159 (`proposals_written`) and of r168 (`gate_names_its_ids`) now take the `and the term "ledger"` clause as an optional group and expect `term/ledger` only when present (plan D2). The deprecated r92 and r104 scenarios still pass through the same steps. No production change.

## Red and green

Red: `python3 -m pytest -q --work-item w224` gave 2 failed, 180 passed, both on an undefined Then (the step regexes required the term clause).
Green: same command after the change: 182 passed, 1 skipped. `tests/scenarios/test_supervision.py` (the two w224 tests): 2 passed.

Suite at start: 1022 passed, 2 failed at e4f50825 (the two w224 scenarios, among the expected failures listed). Final w224 run as above.

`tools size --limit 300`: no output; no file over the limit.

## Tests changed under an allowance

none (two steps widened for new scenarios; no existing assertion loosened — deprecated scenarios still assert `term/ledger`).

## Open questions

none beyond plan §5 (no assertion that the brief omits `term/` ids or that no glossary-proposal was written; the scenarios are silent).

The plan contained no code. Commit: 2b992dad.

## Outside the file set

none.
