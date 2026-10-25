# Report w154

## Budget
- scripts/supervise_rounds.py
- tests/scripts/stub_claude.py
- tests/scenarios/supervision_rounds_steps.py
(test_supervision.py not needed: the "p1 is drafted" step went in supervision_rounds_steps.py.)

## Changed
- supervise_rounds.py: `Rounds.round` — a readable result whose status is not DONE calls `keep_round` (commit and push the stage directory and log), makes no `move`, writes nothing under ## Questions (reading B), and raises Refused naming the round, its directory and the outcome.
- stub_claude.py: plans can be keyed `round:<kind>` (kind from the brief's `# <kind> of <name>`), taking precedence over the agent key.
- supervision_rounds_steps.py: Givens (gate at turn limit, apply BLOCKED, formulate without result), Thens (p1 is drafted, apply round started, no transition after apply ended, formulate round named with no result).

## Red and green
- Red 1: `python3 -m pytest -q --work-item w154`: 3 failed, StepDefinitionNotFoundError for the missing Givens (expected: steps missing).
- Red 2 (after steps): r87 scenario failed on its Then: log.jsonl held transitions p1 awaiting-answer->approved and approved->formulated after the apply round (expected: code gap). r86 and r88 passed once their steps existed, as the plan foresaw (code already right).
- Green: `python3 -m pytest -q --work-item w154`: 145 passed, 1 skipped. Also tests/scenarios/test_supervision.py and tests/scripts: 144 passed, 1 skipped.
- Suite at start: 830 passed, 3 failed (these three scenarios) at d12acec.
- Size: `tools size --limit 300` printed nothing.

## Tests changed under an allowance
none

## Open questions
- `work run` with no initiative: whether one initiative's non-DONE round stops the others' sessions; scenarios silent, existing Refused path applies.
- A gate agent giving QUESTION rather than DONE now stops the run each time (as ruled).
- Whether the error message lists the result's questions: it gives the outcome and summary only.
- `Rounds.due` sends an awaiting-answer proposal with no questions to apply (0 >= 0); not reached.

## Other
The plan contained no code. Outside the file set: none. Commit: c437cb4.
