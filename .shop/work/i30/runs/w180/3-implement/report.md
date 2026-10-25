# w180 report

## Budget
- skills/formulating-features/SKILL.md

## Changed
Process step 4 of the skill now runs the old scenario alone with `python3 -m pytest -q "<node id>"`, or `-k <underscored test name>`, and says to check with `--collect-only` that one test is collected. The plan's decision 2 gives the reason: a spaced `-k` selects as much as no `-k`.

## Red/green
formulation#r23 has no scenario, so there was no red run. formulation is a guarantees capability. Nothing could go red.
Final run: `python3 -m pytest -q --work-item w180` gave 142 passed, 1 skipped.
Suite at start (brief's Suite record): 867 passed, 6 failed, all in test_supervision.py. I did not run the whole suite.

## Tests changed under an allowance
none

## Open questions
Scenario outlines (several examples under one name), and a title carried by several feature files. A deselected `fixture` test. All left unchosen, as in the plan's section 5.

## Other
The plan contained no code. The size check printed nothing. No file already over the limit.

## Outside the file set
none

Commit: a4fd9482
