# w222 implement report

## Budget
scripts/supervise_change.py, scripts/supervise_rounds.py, tests/scenarios/supervision_integrate_steps.py,
tests/scenarios/supervision_proposal_steps.py, tests/scenarios/spec_integration_steps.py (outside the file set), CLAUDE.md.

## Outside the file set
tests/scenarios/spec_integration_steps.py: `drafts_glossary_change` asserted `.shop/work/i1/glossary.md` does not exist;
D1/D2 of the plan write exactly that file. The plan said no test breaks; it was wrong on this one.

## What changed
- `Changes.write_proposals` also writes `glossary.md`, a drafted glossary-proposal (adds/changes/removes of the glossary entries, drafts-path sentence), returned so the integrate round commits it (D1, D2).
- `Rounds.glossary_proposals()` and the r93 test in `due`: a glossary-proposal counts as the initiative's output (D3).
- Steps: glossary Given, glossary change-list Given, two Thens (r171); awaiting-answer glossary-proposal Given and "no apply round for g1" Then (r172).
- CLAUDE.md module-map row updated.

## Red and green
- Red: `python3 -m pytest -q -k change_list_naming_the_glossary tests/scenarios/test_supervision.py` before steps: undefined first Given (StepDefinitionNotFoundError). After the steps and before the writer I did not get a clean failing assertion: the run did not finish within 120 s, in the background (the loop the plan's D3 predicts; stopped by timeout). I did not capture an assertion failure for the Then.
- r172: red was undefined steps only. With the steps it passes with no production code, as the plan says (no apply route exists for glossary-proposals; passes by absence). Flag: a scenario passing without code.
- Green: `python3 -m pytest -q -n0 --work-item w222`: 182 passed, 1 skipped, 912 deselected.
- Suite at start: 1036 passed, 16 failed. After: test_supervision.py (`--work-item=`) 14 failed, 279 passed; the 14 are all in the start record's failing list (the two others there were r171 and r172, now green). test_spec_integration.py: 5 passed.

## Tests changed under an allowance
- tests/scenarios/spec_integration_steps.py `drafts_glossary_change` (scenario r54, committed 085527d8 after the base): removed the assertion that glossary.md does not exist, per plan D1/D2.

## Open questions
Those of the plan's section 5: a second integrate round naming the glossary when a glossary-proposal exists (the writer overwrites glossary.md); a glossary entry with empty lists; a capability named `glossary`; r107's unknown capability with a glossary entry.

## Other
The plan contained no code. `tools size --limit 300`: nothing printed.
Files: CLAUDE.md, scripts/supervise_change.py, scripts/supervise_rounds.py, tests/scenarios/{supervision_integrate_steps,supervision_proposal_steps,spec_integration_steps}.py.
Now possible: an integrate round's glossary entry becomes a drafted glossary-proposal, and an initiative holding only one is not re-integrated.
