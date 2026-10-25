# Report of w140

## Budget
- scripts/workqueue_answer.py
- tests/scenarios/work_queue_answer_steps.py
- scripts/work
- README.md

## Changed
- workqueue_answer.py: a capability-proposal (frontmatter kind) skips asked_from and move; status stays awaiting-answer; commit holds the proposal file only (message `work answer: p1`). Refusal text names both kinds.
- work_queue_answer_steps.py: new Given "an initiative {ident} under .shop/work/ whose capability-proposal {name} is {status}" (p1.md with a Questions section, no log.jsonl).
- scripts/work help and README line updated.

## Red / green
- Red: `python3 -m pytest -q --work-item w140` -> 2 failed, 150 passed. r24 and the r9 `answer p1` row failed: `work: log.jsonl gives no transition of p1 to awaiting-answer` (rc 1), the expected refusal of a proposal with no log line (the Given step was added first, so the Given was defined).
- Green: same command -> 152 passed, 1 skipped, 56 subtests passed. `-k answer` in test_work_queue.py: 4 passed.
- Suite at start (brief): 785 passed, 2 failed (those two were these targets, plus many expected-failing listed). Not run whole by me.
- `tools size --limit 300`: prints nothing.

## Tests changed under an allowance
none

## Open questions
- What `work answer` prints for a proposal (prints `awaiting-answer`); commit message wording; whether `## Answers` exists beforehand (handled both ways).
- model_work.py STATUSES for capability-proposal lacks awaiting-answer, so `model check` would flag it; not fixed (outside file set, not a w140 scenario).

The plan contained no code. Commit: 862a5f8.
Now someone can `work answer p1 "..."` on an awaiting-answer proposal.
