# Report of w163 implement

## Budget
None edited. Planned: scripts/supervise_rounds.py, tests/scenarios/supervision_rounds_steps.py (features/supervision.feature is not mine to edit).

## Stop
BLOCKED: the decision the work needs is whose hand writes the scenario.
The plan (Decision 1) tells the implementer to add the @r84 scenario "an integrate round that ends leaves nothing uncommitted and blocks no later `work run`" to features/supervision.feature. My rules forbid any .feature edit or commit (only `features retire` is allowed), and only `formulating-features` writes features. A grep for "leaves nothing uncommitted" in features/ finds no match, so the scenario does not exist and I have no red scenario to work from.
The four accepted scenarios (r79 x3, r84 x1) pass already (plan §1, notes §1), so there is nothing red for me to make green. I did not run them again.

Suite at start: Suite: 849 passed, 0 failed at 37b7dc77 in 19 s.
Plan contained code: no.

## Tests changed under an allowance
none

## Open questions
Plan §5 cases (commit message, push, behaviour of second run) are unchosen.

## Size
Nothing touched, so `tools size` was not needed.

## Files changed
none; no commits.
