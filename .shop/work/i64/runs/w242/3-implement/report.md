## Budget
scripts/supervise_rounds.py, scripts/supervise_brief.py, tests/scenarios/supervision_proposal_steps.py, tests/scenarios/supervision_reintegrate_steps.py

## Changed
- supervise_rounds.py `due`: a glossary-proposal at awaiting-answer/approved that `sent_back` gets integrate/drafted before `route` (r221).
- Step definitions: answers pattern accepts commas; apply Given and integrate Then take `[pg]1`; Then's `position` now uses the named node.

## Outside the file set
scripts/supervise_brief.py `integrate_lines`: with no request the initiative fulfils, the Request/Accepted lines are omitted instead of Refused ("no request  under .shop/work/requests"). Needed: the scenario's i1 fulfils none, and the integrate round could not start. Plan open case §5 foresaw this.

## Red / green
- Red: the scenario hung (apply repeated, the loop the notes predicted) before the code change; then, with `due` fixed, failed with "work: there is no request  under .shop/work/requests".
- Green: `python3 -m pytest -q --work-item w242` -> 182 passed, 1 skipped. tests/scenarios/test_supervision.py (the run shown 1 passed) .
- Suite at start: 1086 passed, 2 failed (the brief's record; one of the two failures was this scenario's module neighbours, not run by me).
- `tools size`: no output (no file over 300).

## Tests changed under an allowance
none
## Open questions
Glossary apply giving both questions and unheld_answers: which wins; unchosen. Glossary integrate writing (readings A/B) left to r189's work-item.
The plan contained no code.
