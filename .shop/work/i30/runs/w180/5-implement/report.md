# w180 report (stage 5, continuation after the whole-suite failures)

## Budget
- none; no edit this stage

## Changed
Nothing this stage. The change is the earlier commit a4fd9482 (rebased as be7b9477 on this branch): step 4 of skills/formulating-features/SKILL.md runs an old scenario alone with `python3 -m pytest -q "<node id>"` or `-k <underscored name>`, checked with `--collect-only`.

## Red and green
formulation#r23 has no scenario (guarantees capability), so no red run exists.
Final run: `python3 -m pytest -q --work-item w180` gave 142 passed, 1 skipped, 56 subtests passed.

## Suite
Suite record at the start: 875 passed, 1 failed. The failing test is the supervision gate-round scenario of i30's r117, which another work-item accepts (w184/w185). The earlier whole-suite failures were scenarios no work-item had accepted. Neither involves skills/formulating-features/SKILL.md. The answers in the brief say to merge again. I did not run the whole suite.

## Size check
`python3 <Scripts>/tools size --limit 300` printed nothing.

## Tests changed under an allowance
none

## Open questions
Scenario outlines, a title carried by several feature files, and a deselected `fixture` test are left unchosen, as in the plan.

## Other
The plan contained no code. Nothing was pasted. Outside the file set: none.
Commits: be7b9477 formulating-features: run an old scenario alone with python3 -m pytest, selected by test name (formulation#r23)
