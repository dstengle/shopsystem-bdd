## Budget
scripts/supervise_outputs.py, scripts/work_items.py, tests/scenarios/supervision_session_faults_steps.py

## Changed
- supervise_outputs.py: `is_guarantees(root, capability)`; `unformulated` skips guarantees capabilities' ids.
- work_items.py: `guarantees` uses `is_guarantees` (one reader).
- supervision_session_faults_steps.py: Given "spec/capabilities/steady.md is a guarantees capability, and i1's capability-proposal p1 is awaiting-answer, ..." (writes steady as guarantees, then the answered proposal).

## Red / green
- Red: `python3 -m pytest -q tests/scenarios/test_supervision.py -k guarantees`: first StepDefinitionNotFound; after the step, the Then failed: p1 stayed awaiting-answer with "the formulate round's scenario for steady#r4 is missing" (expected: guarantees ids were counted as lacking).
- Green: same command, 1 passed. Final: `--work-item w201`: 209 passed, 1 skipped; test_supervision.py 65 passed; tests/scripts 143 passed.
- Suite at start: 946 passed, 1 failed (this very row, undefined step).

## Tests changed under an allowance
none
## Open questions
Plan section 5: mixed ids, quoted group line, range ids of a guarantees capability (skipped by capability), absent spec file (not guarantees) — behaviour only as the code reads, no scenario.
## Other
Plan contained no code. `tools size`: prints nothing. Commit b27e0e2c. Prior commit 32a16402 did decision 4 (import order).
Files: scripts/supervise_outputs.py, scripts/work_items.py, tests/scenarios/supervision_session_faults_steps.py
