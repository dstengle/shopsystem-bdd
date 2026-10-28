# w222 implement report

## Budget
No edits by this session. Commit 4e45fc32 (made before this session, on this branch) touched 6 files: CLAUDE.md, scripts/supervise_change.py, scripts/supervise_rounds.py, tests/scenarios/spec_integration_steps.py, tests/scenarios/supervision_integrate_steps.py, tests/scenarios/supervision_proposal_steps.py.

## What this session found
The branch already held the commit "supervision r171, r172: an integrate round's glossary entry is written as a drafted glossary-proposal" (HEAD, 4e45fc32). No report from the earlier session exists (there is no 3-implement stage directory). I saw no red run, because the code was already there. This session did not write the code.

## Runs
- `python3 -m pytest -q --work-item w222`: 182 passed, 1 skipped, 56 subtests passed. Both r171 and r172 scenarios are in it and pass.
- `python3 -m pytest -q tests/scenarios/test_supervision.py -k glossaryproposal`: 2 passed.
- The brief's Suite record (1038 passed, 14 failed) lists failures the person has since ruled belong to w223, w224 and w225 (expected failures until those are green). `work run` runs the whole suite.
- `tools size --limit 300`: prints nothing, so no file is over the limit.

## Tests changed under an allowance
tests/scenarios/spec_integration_steps.py, step `drafts_glossary_change`: commit 4e45fc32 removed `assert not (repo / ".shop/work/i1/glossary.md").exists()`. That assertion was first committed in 085527d8, after Base 134745663, so it belongs to this initiative. Plan decision D1 has the writer now write glossary.md, so the assertion no longer holds. This is the "test this initiative wrote" allowance (interim).

## Open questions
The plan's section 5 cases are unchosen by the scenarios: a second integrate round on an initiative that already has a glossary-proposal, an empty glossary entry, a capability named `glossary`, the form of the term ids, and a glossary entry in a round that names an unknown capability.

## Plan code
The plan contained no code.

## Concerns
This session did not do the red-green cycle (stop condition "passes before any code"). The scenarios pass only because of the earlier commit.
Files changed: none by this session.
