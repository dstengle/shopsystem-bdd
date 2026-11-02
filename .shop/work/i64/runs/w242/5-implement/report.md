## Budget
none: no edits this stage.

## Result
Commit 5960964a (supervision r221), from the earlier stage, already holds the work. The two earlier whole-suite failures came from outside w242: i62's r219/r220 scenarios (now accepted by w245) and a flaky git index.lock in the r216 scenario. Neither touches w242's change.

Final run: `python3 -m pytest -q -p work_items --work-item w242` -> 182 passed, 1 skipped.
Suite at start: 1088 passed, 0 failed at 5960964a.
`tools size --limit 300`: no output.
Outside the file set (earlier stage): scripts/supervise_brief.py, named in 3-implement/report.md.

## Tests changed under an allowance
none

## Open questions
Glossary apply giving both questions and unheld_answers: which wins; unchosen.

The plan contained no code.
Commits: 5960964a.
