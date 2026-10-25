# w177 report

## Budget
scripts/workqueue_request.py, scripts/work, tests/scenarios/requests_write_steps.py, features/requests.feature (retire only), CLAUDE.md

(Budget used: 5 files; requests_steps.py not needed, the Givens append the sections to the request file.)

## Changed
`work ask <request> <line> <question>` and `work reply <request> <n> <answer>` (workqueue_request.ask/reply, via `_change`, committed, turn-checked); new requests carry empty Questions/Answers; steps for the Givens/Whens/Thens; three deprecated scenarios retired; CLAUDE.md row. Entry forms: question `<n>. line <l>: <words>`, answer `<n>. <words>`.

## Red and green
Red: `python3 -m pytest -q --work-item w177` -> 5 failed (StepDefinitionNotFoundError on the undefined ask/answer/holds steps, as the plan said). Green: same command -> 147 passed, 1 skipped (after retiring 3). test_requests.py + test_supervision.py: 5 passed.
Suite at start: 859 passed, 5 failed (the five w177 scenarios) at 87424bc6; now those pass.
tools size: no output (no file over 300).

## Tests changed under an allowance
none

## Open questions
Plan section 5 cases 1-6 (missing line, reply to absent/answered question, empty text, delivered-state replies, supervise_intake, D1-D5) left unchosen.

## Plan contained code
No.

## Commits
db4d07f2
