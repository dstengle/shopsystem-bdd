## Budget
tests/scenarios/supervision_reintegrate_steps.py

## Changed
In the step "a round of the kind integrate is started for g1, redrafts the term ledger ...", g1's stubbed apply round (`round:apply:g1`) now gives `unheld_answers: ["One line an event."]`, so r221 starts the integrate round the Given names. No feature file changed. The plan contained no code that I pasted.

## Runs
Suite at start: 1085 passed, 0 failed at a4b1a295 (the brief's record).
After the change, `python3 -m pytest -q --work-item w238`: 1 failed, 182 passed. The r189 scenario still fails on this branch. The stub's apply round now gives the unheld answer (the brief shows it in the apply round's brief), but `scripts/` on this branch does not have r221. `main` has r221 (w242), and `git merge-base HEAD main` is 7d9fcb88. I may not rebase, so I could not run the scenario green. `work run` rebases the branch onto main before it runs the scenarios.

## Tests changed under an allowance
none

## Open questions
none

## Size
`tools size --limit 300` printed nothing.

## Files changed
tests/scenarios/supervision_reintegrate_steps.py

## Concerns
The r189 scenario is unverified against r221. The person's session said it fails only because the stub's apply round gave no `unheld_answers`.
