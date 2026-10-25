# report w194

## Budget
scripts/supervise_analysis.py, scripts/supervise.py, tests/scenarios/supervision_analysis_steps.py, tests/scenarios/supervision_delegation_steps.py, tests/scenarios/supervision_done_steps.py, features/supervision.feature (retire only).

## What changed
- `Analyses.lists_nothing`: status ignored; a readable result with no questions lists nothing (r121).
- `pull_through`: analyse/set_done also need a green work-item (r75). The branch review still runs when all are withdrawn.
- Steps: r121 parameterised Given and a new Then "no work-item was drafted in i1 for the kept branch review" (the plan missed it); r120 Then; r105 parameterised Given, records Given, "i1 is not done".
- Retired the deprecated PARTIAL scenario with `features retire`; its step `reviewer_partial` was replaced by the parameterised one.
- No production change for r105 or r120.

## Red and green
- Red: r121 rows failed on the missing Given, then (after steps) PARTIAL/BLOCKED/NEEDS_CONTEXT failed on "ran measure initiative" (len(found)==0) because `lists_nothing` required DONE. r120: Then then missing; after adding, the brief lacked the verdict ask. r75 withdrawn row: measurement was written. r105: missing Givens/Then.
- Green: `python3 -m pytest -q --work-item w194` -> 155 passed, 1 skipped. `--whole-suite tests/scenarios/test_supervision.py tests/scripts` -> 353 passed, 1 skipped.
- Suite at start: 905 passed, 8 failed (all in w194's scenarios).

## Tests changed under an allowance
- tests/scenarios/supervision_delegation_steps.py `session_answers` (setup, no assertion changed): it no longer rewrites log.jsonl when one exists, so the reviewer's log from r120's Given survives; without this the brief had no verdict ask.
- tests/scenarios/supervision_done_steps.py `started_with_items` (setup): fixed text became a parameterised regex; same text still matches.

## Open questions
The plan's section 5 cases are unchosen: unreadable/missing result.json (still not "lists nothing"); `questions` null/string/missing (null/missing/"" list nothing, a string lists something); date of a committed measurement in r105's Given (I used 2026-10-01); no notice for an initiative with no green work-item.

## Other
Plan contained no code. Size check printed nothing. Commits: e7dd7e78, fdeae6af. The r105 "not done" row is also kept by the new pull_through guard; `workqueue_done.holds` already required a green item.
