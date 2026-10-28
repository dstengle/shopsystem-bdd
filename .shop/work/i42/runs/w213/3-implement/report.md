## Budget

- scripts/supervise_brief.py
- agents/initiative-round.md
- tests/scenarios/spec_integration_apply_steps.py (new; spec_integration_steps.py left alone)
- tests/scenarios/test_spec_integration.py
- README.md

## What changed

- The apply brief now carries `UNHELD_ANSWERS`: compare each answer with the applied drafts and give each unheld one in `unheld_answers`, also on a partial apply.
- agents/initiative-round.md: the apply contract names `unheld_answers`.
- New steps module for the r46 scenario (7 steps), bound from test_spec_integration.py.
- README bullet names r46.

## Red and green

- Red: `python3 -m pytest -q tests/scenarios/test_spec_integration.py -k kind_apply`: the Then line failed, because the apply brief did not name `unheld_answers` (first an assertion on the formulate stand-in, fixed in setup by using thing#r1).
- Green: same command, 1 passed. Final run: `python3 -m pytest -q --work-item w213`: 177 passed, 1 skipped.
- Suite at start (brief): 1015 passed, 1 failed (this r46 scenario) plus the parked expected failures.
- `--whole-suite` is refused to a worker, so other supervision tests were not run beyond `--work-item w213` (which includes other capabilities' @r46 scenarios).

## Tests changed under an allowance

none

## Open questions

- Whether the brief instruction goes only to proposals with answers (it is given on every apply brief).
- What `work run` does with a non-empty `unheld_answers` (nothing: plan decision 2).

## Other

- The plan contained no code.
- `tools size --limit 300`: prints nothing, no file over.
- Commit: 5482e7e3.
- Concern: the stand-in round supplies `unheld_answers` itself; the comparison by the real agent is not exercised.
