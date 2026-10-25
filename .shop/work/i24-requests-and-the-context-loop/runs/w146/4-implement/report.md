# Report of w146

## Budget
scripts/supervise_rounds.py, scripts/supervise_worker.py, scripts/supervise_brief.py, scripts/supervise.py, tests/scenarios/supervision_rounds_steps.py

## Changed
- `drafted` proposals are due for a `gate` round (moving to awaiting-answer); `gate` joins ROUNDS (tools); the gate brief asks for questions, each a decision with readings and the recommended one marked; `round()` passes the gate result's questions to `move`, which now writes a list as one `## Questions` bullet each, in order.
- New steps in supervision_rounds_steps.py (drafted Given, gate-result Given, gate-started Then, brief-ask Then, Questions-hold Then).

## Runs
- Suite at start: 798 passed, 2 failed (the two gate scenarios among them), per the brief.
- Red: `python3 -m pytest -q --work-item w146` -> 2 failed (undefined Given "i1's capability-proposal p1 is drafted"). After the drafted Given, r68 failed on the Then: no gate round was started (stand-in's only starts were branch-review and analysis). Expected: `due()` never selected a drafted proposal.
- Green: `python3 -m pytest -q --work-item w146` -> 144 passed, 1 skipped. tests/scenarios/test_supervision.py + tests/scripts: 143 passed, 1 skipped.
- r85 was not run alone between its Given and the code; its red was the undefined first Given in the first run.

## Tests changed under an allowance
none

## Open questions
- Gate result with no questions under DONE: proposal goes to awaiting-answer with nothing asked; apply/formulate may follow at once (plan section 5).
- Gate round whose outcome is not DONE: the code does not read the status; only a Fault (session/result problems) keeps the proposal's status. A non-DONE gate result still moves to awaiting-answer.
- A run whose only node is a proposal at awaiting-answer: exit and printout unchosen.
- model_work.py's proposal status set lacks awaiting-answer.
- A question holding newlines is written as an indented-continuation bullet (existing `section()`).

## Other
The plan contained no code. Size check: `tools size --limit 300` printed nothing.
Outside the file set: none (supervise.py is in the work-item's file set).
Commit: c71999a. What someone can now do: a drafted capability-proposal gets a gate round whose questions land in its `## Questions`. Surprise: scenario r69 (awaiting-answer after gate) steps are still undefined (w152's).
