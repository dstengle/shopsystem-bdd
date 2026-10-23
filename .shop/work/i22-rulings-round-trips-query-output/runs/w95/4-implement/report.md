## Budget
tests/scenarios/analysis_tools_json_steps.py, tests/scripts/test_tools.py

## Changes
Earlier commits (583db74, e6d39e2) already did the production work. This stage:
- Rewrote the two refs --json Then steps to the corrected r55 scenario text (feature commit d05706e, on main, not yet in this branch): "the references in src/checkout.py and tests/test_cart.py" and "the number of references it gives" (summary.references == len(references)).
- tests/scripts/test_tools.py: its env also drops PYTEST_ADDOPTS (setup only), because the worker's `--work-item` leaked into the mapped project and failed two tests.

## Runs
Suite at start: 617 passed, 2 failed (one is the r55 scenario). Final `--work-item w95`: 127 passed, 1 failed. The failure is the r55 scenario: the feature file on this branch still has the old wording, so the new steps are undefined until `work run` rebases onto d05706e. With the old wording the old step asserted 2 against the real 4 references. I could not run it green here, since I may not touch .feature files.

## Tests changed under an allowance
- tests/scripts/test_tools.py ToolsTest helper env (setup).
- tests/scenarios/analysis_tools_json_steps.py gives_references, gives_summary (initiative's own steps, per the person's answer).

## Open questions
Those in plan part 5; none new.

Plan contained no code. Size check: no file over 300.
Commits: see result.
