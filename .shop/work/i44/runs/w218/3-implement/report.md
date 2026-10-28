## Budget
- agents/bdd-branch-reviewer.md
- tests/scripts/test_agents.py
- README.md

## Changed
Bash removed from the bdd-branch-reviewer's tools; README row matches; new test `test_r7_branch_reviewer_has_no_shell` (docstring r1-r7).

## Runs
Red: `python3 -m pytest -q tests/scripts/test_agents.py -k r7` -> `AssertionError: {'Bash'} is not false` (the definition granted Bash).
Green/final: same module, 9 passed, 18 subtests passed. No scenarios exist for r7 (checked by reading agents/).
Suite record at start: 1033 passed, 0 failed (11 expected failures, parked w212 scenarios). I did not run the whole suite.
`tools size --limit 300`: prints nothing (no file over).

## Tests changed under an allowance
none

## Open questions
none (plan's open cases: architecture-reviewer and bdd-task-reviewer still hold Bash; r7 does not cover them. Agent body not changed.)

The plan contained no code.

## Now possible
The branch reviewer definition has no shell tool. Commit: ae666f39.

Files changed: the three above. Concerns: none.
