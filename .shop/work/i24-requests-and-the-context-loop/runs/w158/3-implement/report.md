## Budget

- scripts/supervise_rounds.py
- tests/scenarios/supervision_rounds_steps.py
- tests/scenarios/test_supervision.py (the second-run When, beside run_work; importing it into the steps module would be circular)

## Changed

- `Rounds.due`: an integrate round is due only for a `proposed` initiative with a `fulfils`.
- New steps: Given "i1 is proposed and fulfils no request"; Thens for no integrate round, i1 is proposed, no round branch, nothing uncommitted under .shop/work, second run not refused; When "a second time".

## Red / green

- Red: `python3 -m pytest -q "tests/scenarios/test_supervision.py::test_a_proposed_initiative_that_fulfils_no_request_..."` failed at Then "i1 is proposed": status was `started`, stderr `work: there is no request  under .shop/work/requests`. Expected: due gave an integrate round to every proposed initiative.
- Green: `python3 -m pytest -q --work-item w158`: 144 passed, 1 skipped.
- Suite at start (brief): 822 passed, 1 failed (this scenario) plus expected failures listed in the brief.

## Tests changed under an allowance
none

## Open questions
Plan section 5 cases, left unchosen: fulfils naming an unkept request; request with no accepted lines; branch review over an initiative with zero work-items (the scenario passed, so not hit); faulted integrate round leaves `started`; no-fulfils initiative with capability-proposals; `work run` with no initiative.

## Other
The plan contained no code. `tools size --limit 300`: no output (no file over).

Commit: 00095da. Files: the three above.
