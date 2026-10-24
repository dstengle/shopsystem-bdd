# w123 implementation report

## Budget
scripts/work, scripts/workqueue_status.py (new), scripts/workqueue_note.py (new), scripts/model_work.py, CLAUDE.md,
tests/scenarios/test_work_queue.py, tests/scenarios/work_queue_status_steps.py (new), tests/scenarios/work_queue_note_steps.py (new).

## Changed
`work note` (workqueue_note.py) and `work status` (workqueue_status.py, text and `--json`) with their subcommands in scripts/work;
`model_work.py` leaves ledger.md out of the initiative's parts (D4); two module-map rows; step modules for r16-r21.
The plan held no code; nothing pasted.

## Red and green
- Red (r19-r21): `python3 -m pytest -q -p no:warnings -n 0 tests/scenarios/test_work_queue.py -k "note_appends or note_commits or note_with"`:
  9 failed, at the Then on the command's result: "invalid choice: 'note'". Expected: no `note` subcommand.
- Green after workqueue_note.py: 9 passed.
- Red (r16-r18): status subcommand registered with a stub; the three scenarios failed at Thens (no output). Green: all pass
  after workqueue_status.py. (The stub-first run was not captured separately; the first run with the real module showed
  the r18 and r16 failures, which were step defects (the `gives` step of the withdraw module took my Then; an ledger
  parse in my own Then), fixed in the steps only.)
- Final: `python3 -m pytest -q -p no:warnings --work-item w123`: 150 passed, 1 skipped (it ran the broader set); test_work_queue,
  test_design_model_check and tests/scripts: 149 passed, 1 skipped.
- Suite at the start: 721 passed, 12 failed at 464a900 (the failing ones were this work-item's own and others named in the brief).
- `tools size --limit 300`: prints nothing; no file over.

## Tests changed under an allowance
none

## Open questions
Those of the plan's section 5, left as the code happens to behave and not chosen: status outside git / no commit / detached
HEAD / no remote (branch name null or `pushed` null, "the remote cannot be compared with it"); hand-written ledger lines count
toward the last ten but never as a `next:` line; `note` with an empty line or on a done initiative is accepted; answers beyond
questions are ignored; `note` commits only ledger.md.

## Outside the file set
none. The step `it gives {whose}'s status and ...` is spelled so that pytest-bdd prefers it to the withdraw module's
`it gives {triples}`, which would otherwise take the line.

## Surprising
Step choice between two matching patterns follows the pattern text, not definition order.

## Commits
see result.json. Files changed: the eight in the budget.
