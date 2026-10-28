## Budget

No files touched by this session. The work was already on the branch.

# Report w221

## Finding
HEAD of work/w221 is 6a7131c0 "design-model-check: glossary-proposal is a part kind; r122 terms, r123 approved closes, r124 shapes". An earlier implement stage committed it. The 3-implement stage directory is empty, so it left no report. The commit carries:
- scripts/model_work.py and scripts/model.lp
- the steps in tests/scenarios/ (conftest.py, design_model_check_given.py, design_model_check_trace.py, design_model_check_work.py, test_design_model_check.py)
- the retirement of the five deprecated @r124 scenarios (features/design-model-check.feature), with their step branches removed from design_model_check_problems.py

I made no edit and no red-then-green cycle, so there is no red run to show. The scenarios were already green when I started.

## Runs
- Suite at the start (the brief's Suite record): 1053 passed, 14 failed at 6a7131c0. The 14 are supervision's glossary-proposal scenarios, which no work-item accepts yet. The person accepted them as they are (answer in the brief). None of them is w221's.
- Final run: `python3 -m pytest -q --work-item w221` gives 211 passed, 1 skipped, 56 subtests passed. All of r122, r123 and r124 are green.
- Completeness check: `python3 <Scripts>/tools size --limit 300` printed nothing, so no file is over the limit.

## Tests changed under an allowance
None, by me. I did not check the earlier commit's test changes against the allowance.

## Open questions
The plan's open cases stay unchosen by this session:
- A glossary-proposal that names something other than `term/<term>` in adds, changes or removes.
- Whether an approved glossary-proposal's removes also excuses a capability-proposal's `term/` reference (r66).
- Model check's `v_d1` names a drafted or awaiting-answer glossary-proposal under a `done` initiative, while the queue's done condition ignores glossary-proposals.
- A glossary-proposal with an `argues`.

## Other
The plan contained no code. The commits are 6a7131c0 and its parent work-queue commits. Someone can now put a glossary-proposal in `.shop/work/` and have `model check` read it as a part kind with its lifecycle (drafted, awaiting-answer, approved, withdrawn), resolve its `term/` lists, and treat `approved` as closing it.
