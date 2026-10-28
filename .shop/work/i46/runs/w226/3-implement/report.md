## Budget
- features/supervision.feature

## Changed
`features retire` of the three scenarios in Retires (r77 outline, r92, r104). 40 lines deleted. No code, no step definitions removed. The plan held no code.

## Red/green
No red: the accepted scenarios (r159, r168) were already green before any work (`pytest -q --work-item w226`: 183 passed, 1 skipped). The work-item exists only to retire the deprecated scenarios (plan sections 1, 3); I read that as the work, not as the HAND-BACK "already passes" stop. Say so if you read it otherwise.
Final: `pytest -q --work-item w226`: 183 passed, 1 skipped; test_supervision.py and test_bound.py: 3 passed. `features bindings --unbound`: every binding names a scenario.
Suite at start: 1070 passed, 0 failed (with the listed expected failures).

## Tests changed under an allowance
none

## Open questions
none (plan cases 1-3: no tool objected; the @r92 scenario "for removal" stays, per D2).

## Size
`tools size --limit 300` printed nothing.

## Outside the file set
none

## Result
Commit 93531c6a. Surprise: nothing to build; the scenarios were already green.
