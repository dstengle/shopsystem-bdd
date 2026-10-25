## Budget
scripts/supervise_answers.py, scripts/workqueue_answer.py

## Report
Changed: `answers()` moves a reviewer's question's item to ready (verdict change) or done (accept); verdict is the `verdict` field of the answering session's result; brief asks for it only for reviewer's questions; no/invalid verdict leaves question for the person. Rule shared via `workqueue_answer.reviewer_status`.
Suite at start: 884 passed, 1 failed (the r118 test). Red: `python3 -m pytest -q -n 0 --work-item w190` -> 1 failed (moved to done, not ready). Green: 145 passed, 1 skipped.
r119 kept as pinning test (person's answer). Plan had no code. Size tool: no output.
## Tests changed under an allowance
none
## Open questions
The plan's section 5 cases (no awaiting-answer log move; two questions mixed; verdict on non-reviewer question ignored; commit message) left unchosen.
## Outside the file set
none
