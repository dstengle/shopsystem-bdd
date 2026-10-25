## Budget
- scripts/supervise_brief.py
- tests/scenarios/supervision_answers_steps.py

## Changed
- supervise_brief.py: `findings_lines` writes `Reviewer's findings: <rel path of last <k>-review/findings.md>` in an implement brief when the log's last move into ready is awaiting-answer->ready, preceded by done->awaiting-answer. (`work run` claims the item first, so the claim after that move is skipped.)
- supervision_answers_steps.py: two Givens and the Then of the r98 scenario.

## Red / green
- Red: `python3 -m pytest -q -n 0 --work-item w173`: Then assertion failed, no findings line in the brief (steps defined, brief lacked the line). Expected.
- Green: same command: 143 passed, 1 skipped (final run). test_supervision.py module also run, passing.
- Suite at start: 856 passed, 1 failed (this scenario, plus the listed expected failures).
- Plan contained no code.

## Tests changed under an allowance
none

## Open questions
- No review dir or no findings.md: the line names the path of the last review dir's findings.md without checking it exists; no review dir gives no line.
- Delegated answers to a reviewer's question; later implementer runs by another route after the r98 route (the line follows the last move into ready, so a later FAIL return would not get it); fewer answers than questions.

## Size
`tools size --limit 300` printed nothing.

## Commits
1860fabe
