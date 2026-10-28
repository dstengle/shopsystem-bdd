## Budget

scripts/supervise_glossary.py, scripts/supervise_rounds.py, scripts/supervise_brief.py, scripts/workqueue.py, scripts/supervise_done.py, scripts/supervise.py, tests/scenarios/supervision_proposal_steps.py, tests/scenarios/supervision_rounds_steps.py, tests/scenarios/supervision_formulate_steps.py, tests/scenarios/supervision_done_steps.py, tests/scenarios/supervision_reintegrate_steps.py (11; supervision_integrate_steps.py not needed)

## What changed
- A glossary-proposal is routed: drafted -> gate -> awaiting-answer -> (every question answered, at least one) apply -> approved; no further round (`supervise_glossary.route/statuses`, `Rounds.due`).
- The apply round of a glossary-proposal is not withheld its own terms (`withheld(directory, applying)`), other unapproved glossary-proposals still are. `workqueue.move` takes the proposal statuses for a glossary-proposal. Its lists are kept after apply (no `rewrite_lists`).
- Glossary-only done (`supervise_glossary.glossary_only_done`, `Dones.set_glossary_done`, called from `pull_through` when the initiative has no work-item): all proposals are glossary-proposals and approved, the committed spec/index.md holds added/changed terms and none removed, no uncommitted change; no review, measurement or analysis.
- Steps: g1 Givens/Thens added or widened from p1 to [pg]1 in the five step modules above.

## Runs
- Start: Suite record 1054 passed, 8 failed at e786ad99 (the 8 failing are w225's scenarios, plus 12 expected failures in test_requests.py).
- Red: `python3 -m pytest -q --work-item w225`: 8 failed (missing steps); after the steps, 5 failed with `AssertionError: ([], '', '')` (no round started), r161 with `AssertionError: ('', '')` (not done). Expected: nothing routed a glossary-proposal.
- Green: same command, final: 189 passed, 1 skipped, 56 subtests passed. Whole suite not run (refused to the worker, work run runs it).

## Stop-condition note (concern)
r167 ("no formulate round is started for g1") passed as soon as its step definitions existed, before any routing code, because nothing routed a glossary-proposal at all (vacuous). It is only meaningful together with r166, which needed the code. I went on; the person may want to see this.

## Tests changed under an allowance
none (existing steps widened from p1 to [pg]1 by respelling; no assertion changed)

## Open questions
- A gate round giving no question for a glossary-proposal (r117 names the capability-proposal): g1 is asked the approval question as p1 is, since the shared code does that; unspecified for g1.
- A glossary-proposal awaiting-answer with no question at all gets no apply round (kept so the r162/r163 delegation scenarios stay green).
- An apply round of a glossary-proposal giving unheld answers or no change list, and answers that drop a term: unchosen.
- A glossary-only initiative with a request not delivered (r105) : r161 silent, not checked.
- Send-back routes (r149/r150) are not applied to a glossary-proposal.

## Plan
The plan contained no code.

## Size
`tools size --limit 300` printed nothing.

## Surprising
`--whole-suite` is refused to a worker, so the touched modules (test_supervision etc.) were only run through the work-item filter.

## Commits
9ebc483f routing; 58c712f0 glossary-only done.
