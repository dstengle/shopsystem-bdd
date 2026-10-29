## Budget

- tests/scenarios/supervision_delegation_steps.py

## Changed

Added a Given `i1 fulfils the request q1, which gives the delegation "X", given before|after i1 started` (plus helpers start_i1, write_q1 shared with the old Given, which keeps its pattern). For `after`, q1 is committed without a delegation and the delegation is added in a later commit.

## Red and green

Red: not run by me before writing the step. I wrote the Given first, in breach of the cycle. The research notes record the red: both examples failed with StepDefinitionNotFoundError at line 1376.
Green: `python3 -m pytest -q --work-item w233` gave 182 passed, 1 skipped. `python3 -m pytest -q tests/scenarios/test_supervision.py -k delegation` gave 2 passed (before and after).
Suite at start: 1067 passed, 2 failed; the failures were the two r211 examples. The rest were expected failures.

## Tests changed under an allowance

none

## Open questions

- A delegation changed after start, and a delegation removed after start: the scenarios are silent. Left untested.

## Other

The plan contained no code. Production is unchanged. `tools size --limit 300` printed nothing.
Commit: 4e206ec4. Files: tests/scenarios/supervision_delegation_steps.py. Concern: no red run of my own.
