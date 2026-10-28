# report of w214

## Budget

scripts/supervise_rounds.py, scripts/supervise_outputs.py, scripts/supervise_brief.py, agents/initiative-round.md,
tests/scenarios/supervision_formulate_steps.py, tests/scenarios/supervision_reintegrate_steps.py,
features/supervision.feature (features retire only), tests/scenarios/test_supervision.py (only if the retired scenario has a binding; it had none).

## Changed
- supervise_outputs.py: `gives_nothing` moved here, plus `formulated_nothing` and `sent_back` (apply: nothing_applied or non-empty unheld_answers; formulate: nothing_formulated).
- supervise_rounds.py: `route` sends an awaiting-answer or approved proposal whose latest round sent it back to integrate (`applied_nothing` became `sent_back`). The formulate branch takes `nothing_formulated` as its output: commit at the same status, no move, no question.
- supervise_brief.py, agents/initiative-round.md: the formulate round is told the `nothing_formulated` field.
- Steps: the Given for the formulate-nothing round; the Thens for r149, r151, r152, r153.
- features: `features retire` of the r140 deprecated scenario (`features bindings` clean).

## Red / green
- Suite at start (brief's record): 1017 passed, 4 failed (w214 scenarios among them).
- Red: `python3 -m pytest -q --work-item w214 -n auto` after the steps, before any code: 3 failed (r149, r152, r153) on their Then assertions. For r149 the integrate round was not started; only the formulate round ran. Expected: `route` sent an answered formulate proposal back to formulate.
- r151 passed once its Then existed. It was red before only for the undefined step; the flow already held, as the plan said.
- Green, final run of the same command: 181 passed, 1 skipped. With test_spec_integration.py, test_supervision.py and tests/scripts: 180 passed, 1 skipped.

## Tests changed under an allowance

none

## Open questions

- A `nothing_formulated` result that also gives questions (treated as not nothing-formulated, by the field's definition), or has committed scenarios; `unheld_answers` beside questions; a non-list `unheld_answers`: no scenario covers them.
- The widening of r150 to `unheld_answers` beside `changes` is the plan's decision 2, not asserted by a scenario.

## Other

- The plan contained no code; nothing pasted.
- `tools size --limit 300` printed nothing.
- README release notes for r149-r153 not touched (outside the file set).
- Commit: 2b4cbe78.
