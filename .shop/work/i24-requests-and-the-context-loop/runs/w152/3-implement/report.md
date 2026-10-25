## Budget
- tests/scenarios/supervision_rounds_steps.py

## Changed
One new Given binding, `gate_gives_question`, in tests/scenarios/supervision_rounds_steps.py. No production change.

## Red / green
- Red: `python3 -m pytest -q --work-item w152` → 1 failed (the r69 scenario), 142 passed. It failed at its second Given, which had no step definition (as the plan said).
- Green: same command → 143 passed, 1 skipped. `tests/scenarios/test_supervision.py` run as a module passed.
- Suite at start (brief): 816 passed, 1 failed; the one failing was this scenario.
- Size check: `tools size --limit 300` printed nothing.

## Tests changed under an allowance
none

## Open questions
Zero-question gate (D1), PARTIAL gate result (D4), `work run` exit with only a proposal waiting (D2), `model check` rejecting awaiting-answer (D3), and a failure between move and the Questions write. The scenario is silent on all of them and I left them unchosen.

The plan contained no code.

## Outcome
Someone can now run the r69 scenario, and it passes. The production code already did the work. Commit: c5a7bb1.

Files changed: tests/scenarios/supervision_rounds_steps.py. No concerns.
