## Budget
No new edits this stage. Files touched earlier (commit 440352d6): scripts/supervise_change.py, tests/scenarios/supervision_reintegrate_steps.py, tests/scripts/test_supervise_change.py.

## Stop: HAND-BACK
Condition: going green needs work no scenario of the work-item describes and the plan does not name.
Evidence (run `python3 -m pytest -q --work-item w238`): 1 failed, 181 passed.
Failing: test_an_integrate_round_started_for_a_glossaryproposal_that_redrafts_some_of_its_terms_leaves_the_proposal_with_the_terms_its_change_list_does_not_name
Assertion: `assert len(rounds(repo, "integrate", "g1")) == 1` fails: only an apply round for g1 started (brief of 1-apply for g1 in the output).
The person's answer: a spec line [r190] is needed (an apply round whose answers the drafts do not hold, for a glossary-proposal, is followed by an integrate round). Spec lines and features are written by formulating-features, not by me; supervise_glossary.ROUTES says "no further round" (r167) today. Building that route now would be code no accepted scenario/requirement describes.
Green: r188 scenario. Red: r189 scenario.
Next: add r190 to spec/capabilities/supervision.md, formulate its scenario, work-item for the route (supervise_glossary.ROUTES / supervise_rounds.due), then the r189 merge into g1 (glossary branch of write_proposals in scripts/supervise_change.py, plan decision 3).

## Suite at start
Suite: 1084 passed, 0 failed at 440352d6 (with listed expected failures).

## Size
`tools size` printed nothing: no file over the limit.

## Tests changed under an allowance
none (the p1 assertion in test_supervise_change.py was rewritten at 440352d6 as plan part 4 says).

## Open questions
Plan part 5 cases remain: glossary written fresh when round not started for a glossary-proposal; same id in two lists.

The plan contained no code.
