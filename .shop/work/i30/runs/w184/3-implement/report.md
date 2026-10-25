# report w184

## Budget

scripts/supervise_worker.py, scripts/supervise_rounds.py, scripts/supervise.py, tests/scenarios/supervision_rounds_steps.py, tests/scenarios/supervision_proposal_steps.py, tests/scripts/stub_claude.py, features/supervision.feature (retire only), tests/scenarios/test_supervision.py (outside the file set, see below)

## Changed

- r19: research `MAX_TURNS` 40 -> 80; the 40-turn deprecated scenario retired with `features retire`.
- r117: `run_round` asks one approval question when a gate gives none. New Given/Then steps in supervision_rounds_steps.py; the quoted-question Then narrowed to text starting with a quote.
- r110: `pull_through` loops: fix -> push -> pull -> if all green/withdrawn, another `branch_review`, until a review has no fix or a fix is not green. Stub claude takes a list per agent (one result per session in start order, last repeats). New Given/Thens in supervision_proposal_steps.py; the r74 Given now gives [findings, nothing].

## Red and green
- Red (before code): r19 `--max-turns 40` assertion; r117 IndexError (no `## Questions` section in p1); r110 AssertionError, only one bdd-branch-reviewer session started (`len(review)==2` failed).
- Green: `python3 -m pytest -q --work-item w184` -> 145 passed, 1 skipped; `tests/scenarios/test_supervision.py tests/scripts` -> 144 passed, 1 skipped.
- Suite at start: 858 passed, 3 failed (the three of this work-item's scenarios among them, plus others listed as expected).

## Outside the file set
tests/scenarios/test_supervision.py: the step `{name} is green` (parse) swallowed the new Then "...and it is green" (nearest step wins); narrowed to `parsers.re(r"(?P<name>w\d+) is green$")`.

## Tests changed under an allowance
- tests/scenarios/supervision_proposal_steps.py `reviewer_lists` (Given of r74 scenario): setup only; reviewer plan is now [findings, nothing]. Asserts unchanged.
- tests/scenarios/test_supervision.py `is_green`: step pattern narrowed, setup/matching only.

## Open questions
- No bound on the re-review loop if reviewers never list nothing.
- A re-review whose result is unreadable / not DONE: follows `branch_review` as it does for a first review.
- Fix that ends awaiting-answer/failed: no next review, no analysis in this run.
- Approval question wording is mine ("Are the lines of pN approved as drafted? Readings: ...").

## Plan contained code: no.

## Size check
`tools size --limit 300` printed nothing.

## Commits
87cdf5a2, 8d0d6bbe, 3d9bca9e

## Files changed
scripts/supervise_worker.py, scripts/supervise_rounds.py, scripts/supervise.py, tests/scenarios/{supervision_rounds_steps,supervision_proposal_steps,test_supervision}.py, tests/scripts/stub_claude.py, features/supervision.feature (retire).
