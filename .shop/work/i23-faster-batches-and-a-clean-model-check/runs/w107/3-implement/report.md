# Report w107

## Budget
- tests/scenarios/analysis_tools_probe_steps.py

## Changed
`failed_command` Then now checks stdout lines (stripped): `e1`, `e2` are not lines; `e3`..`e5` are. The path in `Tried:` can hold `e1` without effect.

## Red/green
Red was not shown: it appears only in a whole-suite run when pytest's tmp counter is 1 (not run by me). The scenario passes alone before the change. Green: `python3 -m pytest -q --work-item w107`: 137 passed, 1 skipped; tests/scenarios/test_analysis_tools.py passes.
Suite at start: 659 passed, 1 failed (this scenario, plus the expected list).

## Tests changed under an allowance
none (the plan lists `failed_command` as the test the decision rewrites).

## Open questions
none (plan's D1, D2 defects left to the coordinator).

The plan contained no code. `tools size`: prints nothing.
Commit: 753c5a6.
