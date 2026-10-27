## Budget
scripts/supervise_brief.py, agents/initiative-round.md, skills/integrating-a-proposal/SKILL.md, tests/scenarios/spec_integration_steps.py (4 files)

## Changed
- supervise_brief.py: ANSWER_LINES sentence, added to the integrate brief when the initiative's answers are given (D1, D2).
- initiative-round.md and the skill: answers in any round; lines drafted from an answer quote the answer and are kept (D3).
- spec_integration_steps.py: the six r45 steps; `run_integrate` shared as the When (D4, D5).

## Red / green
- Red: the plan's run (notes §1) gave StepDefinitionNotFoundError at the first Given. I did not re-run it before writing the steps, so I have no red run of my own. This is a lapse in the cycle. Because the stub writes the drafts, the Then's brief check (the r45 sentence) is what the code change satisfies.
- Green: `python3 -m pytest -q --work-item w203`: 145 passed, 1 skipped. `tests/scenarios/test_supervision.py` and `test_spec_integration.py`: pass.
- Suite at start: 948 passed, 1 failed; the failure was the r45 scenario itself, plus the expected-failing list in the brief.
- `tools size --limit 300`: no output, no file over.

## Tests changed under an allowance
none

## Open questions
The plan's section 5 cases (answer repeating an accepted line, answer naming no or several capabilities, or an existing one, an answer with no question). Defect 1 (notes §6): an integrate round's result `questions` are never written where the person sees them; not fixed.

## Other
The plan contained no code. Commit: 1c351ddc.
